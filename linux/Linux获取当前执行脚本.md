Title: linux获取当前执行脚本
Date: 2012-06-01 12:04
Category: Linux
Slug: linux-current-script

今天遇到一个需求，获取当前执行脚本：
- 如果是`sh test.sh`或者`./test.sh`的运行方式，那么很简单，直接使用`$0`就可以了。  
- 如果是`source test.sh`或者`. ./test.sh`的方式运行，`$0`就变成了`-bash`了。  
google了一下，这个时候就需要使用`$BASH_SOURCE`了。（bash版本>=3.0）

```bash
[u1@localhost test]$ cat test.sh
echo $0
echo $BASH_SOURCE
[u1@localhost test]$ sh test.sh
test.sh
test.sh
[u1@localhost test]$ source test.sh
-bash
test.sh
```

另外在测试source运行脚本时，有些误操作，导致在执行命令时，都会首先输出一下当前运行命令。


如下所示：

```
[u1@localhost performance]$ cd tools/
cd tools/
[u1@localhost tools]$ cd ..
cd ..
[u1@localhost performance]$
```

看起来实在是有点多余，作为一个有轻微洁癖的人，当然想办法要消除它。不过一时竟不知如何下手，而且这个现象也不好描述，就算想google也不行呀。

不过我看到另外打开的一个section是没有这个问题的，因此想到对比两个section的env。

一对比还真发现有些不同，SHLVL这个变量正常的section为1，会首先输出执行命令的section为3。

所以怀疑到是在section运行了bash的原因，在会首先输出执行命令section里面连续输入两次exit之后，现象消失了。

再次在该section里面输入bash，并没有重现之前的现象。

运行`bash –help`看了一下，怀疑是`bash –v/—verbose`的原因。再次尝试输入`bash -v`，现象重现。 

前后花了不少时间，藉此记录一下~ 
