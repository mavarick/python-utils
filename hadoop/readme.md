# simple_mrjob

  简单跑mapreduce任务的小程序，通过`启动脚本`+`配置文件`的方式，实现hadoop mr多任务的简单调控，功能包括：
  * 多任务放在同一配置文件中。
  * hadoop参数配置
  * shell、python脚本的模板嵌入，实现多路径的解析
  * 配置参数的自动嵌入
  * 多任务依赖检测
 
## 注意：
  * 配置比python的组件基于configparser，但是比其更加强大。不过不要使用其格式`%(var)s`，可能会引起冲突。
 
