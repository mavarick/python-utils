#!/usr/bin/env python
#encoding:utf8

import os
import sys
import re
import getopt
import ConfigParser
from collections import OrderedDict
import pdb
import commands

from subprocess import Popen
from subprocess import PIPE
from subprocess import CalledProcessError

USAGE="""
USAGE:
    1, 解析模板文件
        python {0} parse -c [conf_file_template] -o [conf_file]
    2，根据模板文件运行
        python {0} run -c [conf_file]
    3，合并1，2运行
        python {0} merge -c [config_file]
""".format(__file__)


run_type_tags = [
    "parse",
    "run",
    "merge"
]


register_buildin_section_names = [
    "jobs",  #
    "hadoop", # set hadoop dir
    "pylib", # for import python lib
    "vars",  # global vars
    "job_default_opts",  # job default opts
]


register_non_job_opts=[
    "download", # download file name. if you want to download output hdfs, then set it
                # in case the output is too large, you'd better not use it
    "log",      # log file
    "depend",   # depend={job_name}
    "script",   # run script
]

MR_JOB_FILE_TAG = ["Streaming Job Failed", "Job not Successful"]
MR_JOB_SUCCESS_TAG = "Job complete"


def parse_opts():
    """get options"""
    config = {}
    tag = sys.argv[1]
    if tag not in run_type_tags:
        print USAGE
        sys.exit(-1)

    try:
        options, args = getopt.getopt(sys.argv[2:], "c:o:", ["help", "conf="])
    except getopt.GetoptError:
        print USAGE
        sys.exit(-1)

    config['type'] = tag

    for k, v in options:
        if k in ['-c', '--conf']:
            config['conf'] = v
        if k in ['-o']:
            config['output'] = v
        if k in ['-h', '--help']:
            print USAGE
            sys.exit(0)

    if 'conf' not in config:
        print "error occur"
        print USAGE
        sys.exit(-1)

    return config


config = parse_opts()
config_file = config['conf']
run_type = config['type']

######################################################## loading pylib
cf = ConfigParser.ConfigParser()
cf.read(config_file)
cf.optionxform = str
if "pylib" in cf.sections():
    if "name" in cf.options('pylib'):
        pylibs = cf.get('pylib', 'name')
        pylib_names = [t.strip().strip('.py') for t in pylibs.split(',')]
        for pylib_name in pylib_names:
            print("Loading module [{0}]".format(pylib_name))
            exec('{0} = __import__("{0}")'.format(pylib_name))
######################################################## done


def main():
    if run_type == "parse":
        output_file = config.get("output", "")
        output = open(output_file, 'w') if output_file else sys.stdout
        mrjobs = MRJobs(config_file)
        mrjobs.parse_default()
        mrjobs.parse_jobs()
        mrjobs.rewrite(output)
    if run_type == 'run':
        mrjobs = MRJobs(config_file)
        mrjobs.parse_jobs()
        mrjobs.run()
    if run_type == "merge":
        mrjobs = MRJobs(config_file)
        mrjobs.parse_default()
        mrjobs.parse_jobs()
        mrjobs.run()


class MRJobs(object):
    """mrjobs"""
    def __init__(self, config_file):
        self.config_file = config_file
        self.cf = ConfigParser.ConfigParser()
        self.cf.optionxform = str
        self.cf.read(config_file)

        # 这个变量保存每个job所需要的默认的变量，具有唯一性
        self.job_default_conf_map = OrderedDict()

        # 这个里面保存的是job所需要的变量的，可以在job中累加，比如cacheArchive, file
        self.job_default_var_map = OrderedDict()

        # 这个里面保存用于job配置的非运行相关的变量，例如download, log
        self.job_default_other_conf_map = OrderedDict()

        # 这个里面保存了包括各个变量在内的所有的非累计的变量的信息，各个job1️以{job_name}##开头
        # 例如: input={{job1##output}}
        self.total_conf_map = OrderedDict()

        self.hadoop_bin = None

        self.job_names = []  # section_names
        self.jobs = []

    def rewrite(self, fp=sys.stdout):
        """生成新的配置文件。把模板配置都替换成明文"""
        cf2 = ConfigParser.ConfigParser()
        cf2.optionxform = str
        cf2.add_section("jobs")
        cf2.set('jobs', 'name', self.cf.get("jobs", "name"))
        cf2.add_section("hadoop")
        cf2.set("hadoop", "hadoop_bin", self.hadoop_bin)
        for job in self.jobs:
            section_name = job.section_name
            cf2.add_section(section_name)
            for k, v in job.job_conf_map.iteritems():
                cf2.set(section_name, k, v)
            for k, v in job.job_var_map.iteritems():
                cf2.set(section_name, k, v)
            for k, v in job.job_other_conf_map.iteritems():
                cf2.set(section_name, k, v)
        cf2.write(fp)

    def parse_default(self):
        """解析全局的变量"""
        # load vars
        self.__load_vars("vars")

        # load job default jobconf, vars
        job_conf_map, job_var_map, job_other_conf_map = self.__parse_job_config("job_default_opts")
        self.job_default_conf_map = job_conf_map
        self.job_default_var_map = job_var_map
        self.job_default_other_conf_map = job_other_conf_map

        self.total_conf_map.update(job_conf_map)
        self.total_conf_map.update(job_other_conf_map)

    def parse_jobs(self):
        """对jobs进行解析"""
        job_names = filter(lambda x: x, [t.strip() for t in self.cf.get("jobs", "name").split(",")])
        self.__check_job_names(job_names)
        self.job_names = job_names

        # check hadoop_bin
        self.hadoop_bin = self.__parse_hadoop_bin()

        # job list
        self.jobs = []
        for job_name in self.job_names:
            # pdb.set_trace()
            job_conf_map, job_var_map, job_other_conf_map = self.__parse_job(job_name)
            mrjob = MRJob(job_name, self.hadoop_bin, job_conf_map, job_var_map, job_other_conf_map)
            self.jobs.append(mrjob)

    def run(self):
        """运行jobs列表中的任务，这个地方可以设计成并行，暂时是串行的跑任务"""
        job_map = {}
        for job in self.jobs:
            section_name = job.section_name
            job_map[section_name] = job

        for job in self.jobs:
            job_section_name = job.section_name
            if job.status == 1:
                continue
            if job.status == 0:
                # 检查依赖
                depend_job_names = job.parse_depend_jobs()
                for d_job_name in depend_job_names:
                    d_job = job_map[d_job_name]
                    if d_job.status != 1:
                        raise Exception("Error: running job[%s], depend on job[%s]"
                                        " not finished, with status[%d]" % (
                                        job_section_name, d_job_name, d_job.status))
                # 开始任务
                job.run()
            if job.status == -1:
                print("WARNNING: job[%s], status == -1", job_section_name)

    def __load_vars(self, section_name):
        """解析全局的变量"""
        # get section and return dict of vars
        items = self.cf.items(section_name)
        for k, v in items:
            k, v = k.strip(), v.strip()
            # parse key
            # new_key = "-"+k.replace("__", " ")
            new_key = k
            # parse value
            new_val = self.__parse_value(v)
            # add to global variables
            self.total_conf_map[new_key] = new_val

            self.cf.set(section_name, k, new_val)

    def __parse_hadoop_bin(self):
        """根据[hadoop]的section来解析hadoop_bin"""
        section_name = "hadoop"
        hadoop_bin = "bin/hadoop"
        if section_name not in self.cf.sections():
            print ("warn: hadoop section is not define, and use default: ''")
        else:
            keys = self.cf.options(section_name)
            if "hadoop_bin" in keys:
                hadoop_bin = self.cf.get(section_name, 'hadoop_bin')
                print("use defined hadoop bin: %s" % hadoop_bin)
                return hadoop_bin
            if "hadoop_home" in keys:
                hadoop_home = self.cf.get(section_name, 'hadoop_home')
                print("use defined hadoop home: %s + './bin/hadoop' as hadoop bin" % hadoop_home)
                return os.path.join(hadoop_home, hadoop_bin)
            print("warn: hadoop_home and hadoop_bin are both not set, use 'bin/hadoop' as default")

        self.cf.set(section_name, "hadoop_bin", hadoop_bin)
        return hadoop_bin

    def __parse_job(self, job_name):
        """对job配置进行解析，同时组合默认的配置项"""
        job_conf_map = self.job_default_conf_map.copy()
        job_var_map = self.job_default_var_map.copy()
        job_other_conf_map = self.job_default_other_conf_map.copy()

        _job_conf_map, _job_var_map, _job_other_conf_map = \
            self.__parse_job_config(job_name, job_name)
        job_conf_map.update(_job_conf_map)
        job_var_map = merge_dict_value(job_var_map, _job_var_map)
        job_other_conf_map.update(_job_other_conf_map)

        return job_conf_map, job_var_map, job_other_conf_map

    def __check_job_names(self, job_names):
        """检查job1中的配置项是否存在sections"""
        section_names = self.cf.sections()
        for job_name in job_names:
            if job_name in register_buildin_section_names:
                raise Exception("jobname[%s] is buildin, change another..")
            if job_name not in section_names:
                raise Exception("no section named [%s]")

    def __parse_job_config(self, section_name, job_name=""):
        """解析section中的配置信息，job_name用来更新全局配置字典"""
        items = self.cf.items(section_name)
        job_conf_map = OrderedDict()
        job_var_map = OrderedDict()
        job_other_conf_map = OrderedDict()  # not used

        for k, v in items:
            k, v = k.strip(), v.strip()
            if not v:
                continue
            # parse key
            new_key = k
            # parse value
            new_val = self.__parse_value(v)

            if new_key in register_non_job_opts:
                job_other_conf_map[new_key] = new_val
            elif "__" in new_key:
                job_conf_map[new_key] = new_val
            else:
                job_var_map[new_key] = new_val

            if job_name:
                map_key = "%s##%s" % (job_name, new_key)
                self.total_conf_map[map_key] = new_val

            self.cf.set(section_name, k, new_val)

        return job_conf_map, job_var_map, job_other_conf_map

    def __parse_key(self, key):
        """对key进行解析"""
        return '-'+key.strip().replace("__", " ")

    def __parse_value(self, value):
        """ parse value, for some specical cases:
        a, var, like: {{username}}, {{job1##output}}
        b, shell_code(), like: shell{date 'date +%Y%m%d'}
        c, python_code(), like: python{','.join(['/user/kga-rec-rd/liuxufeng/temp/%d'%date for date in range(10)])}
        d, python_functions, like: python{import jobpylib; jobpylib.gen_job1_input()}
        
        :return: var, str.
        """
        # check vars
        VAR_PATTERN = r"{{(.+?)}}"
        matches = re.finditer(VAR_PATTERN, value)
        new_val_list = []
        last_end = 0
        for match in matches:
            start, end = match.start(), match.end()
            new_val_list.append(value[last_end:start])
            match_var = match.groups()[0]
            match_val = self.total_conf_map[match_var]
            new_val_list.append(match_val)
            
            last_end = end
        new_val_list.append(value[last_end:])
        value = ''.join(new_val_list)

        # check shell,
        SHELL_PATTERN = r"shell{(.+?)}"
        matches = re.finditer(SHELL_PATTERN, value)
        new_val_list = []
        last_end = 0
        for match in matches:
            start, end = match.start(), match.end()
            new_val_list.append(value[last_end:start])
            match_var = match.groups()[0]
            match_val = ShellTools.execute(match_var)
            new_val_list.append(match_val)

            last_end = end
        new_val_list.append(value[last_end:])
        value = ''.join(new_val_list)

        # check python, TODO
        PYTHON_PATTERN = r"python{(.+?)}"
        matches = re.finditer(PYTHON_PATTERN, value)
        new_val_list = []
        last_end = 0
        for match in matches:
            start, end = match.start(), match.end()
            new_val_list.append(value[last_end:start])
            match_var = match.groups()[0]
            match_val = eval(match_var)
            new_val_list.append(match_val)

            last_end = end
        new_val_list.append(value[last_end:])
        value = ''.join(new_val_list)

        return value

    def print_conf(self, fp=sys.stdout):
        """输出任务"""
        self.cf.write(fp)


def merge_dict_value(var_map, merge_var_map):
    """mergedict，不替换，值用逗号进行拼接"""
    for k, v in merge_var_map.iteritems():
        if k in var_map:
            new_v = ','.join([v, var_map[k]])
            var_map[k] = new_v
        else:
            var_map[k] = v
    return var_map


class MRJob(object):
    """实际的一个mrjobs"""
    def __init__(self, section_name, hadoop_bin, job_conf_map, job_var_map, job_other_conf_map):
        self.section_name = section_name
        self.hadoop_bin = hadoop_bin
        self.job_conf_map = job_conf_map
        self.job_var_map = job_var_map
        self.job_other_conf_map = job_other_conf_map

        self.streaming_args = []
        self.log_handler = None

        # depend map
        self.depend_jobs = self.parse_depend_jobs()

        # build running streaming args
        self.build_runner()

        # running status, 0, not start; 1, done; -1, error; 10, running
        self.status = 0

    def build_runner(self):
        """拼接执行的streaming args"""
        streaming_args = []
        hadoop_bin = self.hadoop_bin
        streaming_args.append(hadoop_bin)
        streaming_args.append("streaming")

        for k, v in self.job_conf_map.iteritems():
            if not v:
                continue
            key_list = k.split("__", 1)
            job_conf_tag = '-' + key_list[0]
            job_conf_val = ''.join([key_list[1], '=', v])
            streaming_args.append(job_conf_tag)
            streaming_args.append(job_conf_val)

        for k, v_str in self.job_var_map.iteritems():
            job_opt = '-' + k
            vs = filter(lambda x: x, [t.strip() for t in v_str.split(',')])
            for job_opt_val in vs:
                # 如果值中包含空格
                if " " in job_opt_val:
                    job_opt_val = job_opt_val.strip('"').strip("'")
                    job_opt_val = '"' + job_opt_val + '"'
                streaming_args.append(job_opt)
                streaming_args.append(job_opt_val)
        self.streaming_args = streaming_args

    def run(self):
        """对外执行的接口"""
        if not self.streaming_args:
            self.build_runner()
        print("[MRJOB_RUNNING]:%s" % self.section_name)
        print self.streaming_args
        print " ".join(self.streaming_args)
        self.status = self.execute()

    def execute(self):
        """执行hadoop任务流"""
        # 检查output是否存在
        output_path = self.job_var_map['output']
        log_file = self.job_other_conf_map.get("log", "")
        if log_file:
            fp = open(log_file, 'w')
            # check output exists
            print("[CHECK_PATH]:%s" % output_path)
            rc = HadoopTools(self.hadoop_bin).check_exists(output_path, out_pipe=fp, err_pipe=fp)
            if rc == 0:
                print("[DELETE_PATH]: [%s]" % output_path)
                HadoopTools(self.hadoop_bin).rmr(output_path, out_pipe=fp, err_pipe=fp)

            p = Popen(self.streaming_args, shell=False, stdout=fp, stderr=fp)
            p.wait()
            fp.close()
            log = open(log_file).read()
            if not log.find(MR_JOB_SUCCESS_TAG):
                return -1
        else:
            # 利用系统的sys.stdout, sys.stderr来进行处理
            print("[CHECK_PATH]:%s" % output_path)
            rc = HadoopTools(self.hadoop_bin).check_exists(output_path, out_pipe=sys.stdout, err_pipe=sys.stdout)
            if rc == 0:
                print("[DELETE_PATH]: [%s]" % output_path)
                HadoopTools(self.hadoop_bin).rmr(output_path, out_pipe=sys.stdout, err_pipe=sys.stdout)

            p = Popen(self.streaming_args, shell=False, stdout=sys.stdout, stderr=sys.stdout)
            p.wait()
            return_code = p.returncode
            #return_code = 0
            print("[simple_mrjob]_%s_rc_%s", self.section_name, return_code)
            if return_code != 0:
                return -1
        return 1

    def parse_depend_jobs(self):
        """解析依赖的任务"""
        depend_jobs_str = self.job_other_conf_map.get("depend", "")
        return filter(lambda x: x, [t.strip() for t in depend_jobs_str.split(',')])

    def __str__(self):
        # 把配置信息输出
        data = []
        data.append("[%s]" % self.section_name)
        for k, v in self.job_conf_map.iteritems():
            data.append("%s=%s" % (k, v))
        for k, v in self.job_var_map.iteritems():
            data.append("%s=%s" % (k, v))
        for k, v in self.job_other_conf_map.iteritems():
            data.append("%s=%s" % (k, v))
        return '\n'.join(data)


class HadoopTools(object):
    """针对hadoop的一些工具"""
    def __init__(self, hadoop_bin):
        self.hadoop_bin = hadoop_bin

    def check_exists(self, hdfs_path, out_pipe=sys.stdout, err_pipe=sys.stderr):
        """检查hdfs路径是否存在"""
        run_args = []
        run_args.append(self.hadoop_bin)
        run_args.extend(['dfs', '-test', '-e'])
        run_args.append(hdfs_path)
        return self.execute(run_args, out_pipe=out_pipe, err_pipe=err_pipe)

    def rmr(self, hdfs_path, out_pipe=sys.stdout, err_pipe=sys.stderr):
        """删除hdfs"""
        run_args = []
        run_args.append(self.hadoop_bin)
        run_args.extend(['fs', '-rmr'])
        run_args.append(hdfs_path)
        return self.execute(run_args, out_pipe=out_pipe, err_pipe=err_pipe)

    def execute(self, args, out_pipe=sys.stdout, err_pipe=sys.stderr):
        """执行hadoop的程序"""
        p = Popen(self.args, shell=False, stdout=out_pipe, stderr=err_pipe)
        p.wait()
        if p.returncode != 0:
            msg = "[WARN][check_hdfs_exists] shell: [%s], returncode: [%s]" \
                  % (' '.join(args), p.returncode)
            print(msg)
        return p.returncode


class ShellTools(object):
    """用来执行shell命令，可以写成单例模式"""
    @staticmethod
    def execute(cmd):
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            raise Exception("shell running [%s], with rc [%s], output: [%s]"%(cmd, status, output))
        return output



if __name__ == "__main__":
    main()
