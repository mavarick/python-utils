词法自动解析
======
指定正则解析路径, 对路径上的tokens进行解析

支持:
---

1. 支持正则的全解析;
2. 支持重复字段解析;
3. 支持优先解析; (一般正则无法支持)

格式说明:
-----

<path:score:path_name1>::=<title:2:title_name><delimiter:0:><series:3:series_name><title:2:title_name>...;
<token:title>::={regex}
<output:path_name1>::={title_name}||{series_name} 
<output>::={path_name1}:{path_name1:score}|{path_name2}:{path_name2:score}


<path:score:path_name>
path: 路径标志
score: 权重值
path_name: 路径的名称
tips:
    1, 所有的一切都从path开始;
    2, 路径的name应该不一样;
    3, score可以不写, 默认为5;


<token:priority:token_name>
<词规则名:优先级:解析名称>
tips: 
    1, token: 规则名, 每个规则名会对应一个正则表达式;
    2, priority: 优先级;
    3, token_name: 解析结果名称. 
        a. 如果规则名和解析结果名一样, 那么解析的结果应该是一样的;
        b. 如果只是规则名一样, 那么只是解析结果一样

<output:path_name1>:={title_name}||{series_name} 
output: 输出标志
path_name1: 输出标志名称
title_name, series_name: 为token规则的名字
||: 自定义的分隔符

<output>::={path_name1}:{path_name1:score}|{path_name2}:{path_name2:score}
定义为各个path的输出结果的组合
path_name1:score  表示path_name1的定义.

