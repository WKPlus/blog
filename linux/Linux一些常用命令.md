Title: Linux常用命令
Date: 2012-04-18 20:46
Category: Linux

## 系统软硬件、配置查看：

操作系统版本：uname, lsb\_release

CPU信息查看：cat /proc/cpuinfo

core相关配置：/proc/sys/kernel/core\_pattern，/proc/sys/kernel/core\_uses\_pid
 
系统core/栈大小/进程句柄数等等配置：ulimit
 
查看内存页大小：/usr/bin/getconf PAGE\_SIZE/PAGESIZE

查看系统加载的动态库：/sbin/ldconfig

## 系统实时信息查看：

ps：查看系统当前进程相关信息

netstat：查看系统tcp连接、端口占用等信息

top：查看系统CPU、进程使用内存、CPU等等信息

sar：查看机器CPU、网络等等信息

free：查看机器内存相关信息

vmstat：查看机器内存、swap相关信息

dmesg：查看系统启动相关信息，还可以查看本机是否有程序core过

lsof: 查看系统打开的句柄，lsof位于/usr/sbin/lsof

## 进程相关信息：

/proc/$pid/ 下面各种信息：包括进程对应的可执行程序所在路径、程序执行路径、进程实存/虚存、进程内存地址空间相关信息

查看应用依赖的动态库：usr/bin/ldd \<your\_app\>

恢复打开的被删除的文件：

```bash
[root]#lsof|grep "t.txt" less 21186
work 4r REG 8,3 18 101302483 /home/work/performance_test/t.txt (deleted) 
[root]#cat /proc/21186/fd/4 > t.txt
```

如果是一个vim打开的文件，lsof显示的句柄是.t.txt.swp文件，没法用此办法恢复出t.txt。但是可以在.t.txt.swp目录再次用vim打开t.txt，然后选择recover，最后保存。

