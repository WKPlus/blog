# Linux常用命令介绍

## sed

## awk

## wc
> 计算文件行数、单词数、字符数及最长行的长度                                       

> 用法：                                                                           

> * wc [options] file                                                             
* grep file | wc [options]

> 常用选项：

> * -l 计算行数                                                                      
* -c 计算字符数                                                                    
* -w 计算单词数                                                                    
* -L 计算最长行的长度

## grep
> 文本过滤

> 用法：

> * grep [options] pattern file
> * cat file | grep [options] pattern

> 常用选项：

> * -c 打印匹配的行数
* -i 忽略大小写
* -v 选择没有匹配的行
* -A n 打印匹配行及后续n行
* -B n 打印匹配行及之前n行
* -E 正则扩展
* -l 打印匹配的文件名
* -L 打印没有匹配的文件名
* -H 打印匹配行的同时打印文件名

## cut
> 文本截取

> 用法：

> * cut [options] file
> * cat file | cut [options]

> 常用选项：

> * -d 指定分隔符（只能和-f一起使用）
> * -f 指定截取的区域，可以为单个数值也可以为一个区间
> * -b 截取选定字节
> * -c 截取选定字符（如果字符都是单字节，-b和-c一致）


## sort
> 多行排序

> 用法：

> * sort [options] file
> * cat file | sort [options]

> 常用选项：

> * -u 排序时去重
* -r 倒序排序
* -n 按数值排序，默认是按字符排序
* -k 按哪些区域排序
* -t 指定区域间隔符，默认空白符

## uniq
> 去重

> 用法：

> * uniq [options] file
> * cat file | uniq [options]

> 常用选项：

> * -i 忽略大小写
* -c 打印重复行的个数
* -f 忽略前几个区域进行去重

## tr
> 替换或删除字符

> 用法：

> * cat file | tr [options] SEP1 [SEP2]

> 常用选项：

> * cat file | tr 'a' 'A' 替换文件中的'a'为'A'
> * -d 删除SEP1，此时不需要SEP2
> * -s 替换多个连续的SEP1为一个SEP2

## find
> 查找文件

> 用法：

> * find . -name xxx 查找名字为xxx的文件，支持?*[]通配
> * find . -type [dfl] 查找目录、文件、软连接
> * find . -size [+-]n[bcwkMG] 查找文件大小大于小于等于某个size的文件
> * 上述几种查找类型可以组合使用
> * find . -name xxx -exec command {} \; 查找文件到文件之后，依次对文件执行command命令

## xargs
> 从标准输入读取内容，拼装执行命令

> 用法：

> * find . -size +1G | xargs rm -f 删除超过1G的大文件

## 其他
> yes: yes | yum install xxx

> yum: yum search/install xxx

> touch: 创建文件或者更新文件时间戳

> basename: 获取路径中的文件名

> dirname: 获取路径中的目录

> ps: 查看进程信息

> kill pid: 向进程号为pid的进程发送信号

> killall pname: 向所有名为pname的进程发送信号

> vmstat: 查看cpu、内存等综合系统资源

> sar: 查看cpu、网卡占用

> free: 查看机器内存使用

> netstat: 查看网络连接情况

> iostat: 查看磁盘读写

> top: 查看综合系统资源及各进程的资源占用

> dstat: 查看综合系统资源

> htop: 查看综合系统资源

## man
> 获取命令的帮助信息
用法：

> * man command
> * command [-h|--help]
