Title: mac删除目录需要目录的执行权限
Date: 2016-02-22 20:02
Category: linux
Slug: mac-directory-delete-need-execute-permission


最后，遇到一件有意思的事情，在删除一个非空的可读写目录时，发现竟然删除不了：

```
mkdir tmp
echo "1" > tmp/1
chmod 666 tmp
rm -fr tmp
rm: tmp/1: Permission denied
```

看了一下错误提示，是在删除`tmp/1`文件的提示没有权限了，但是这个文件明明是有可读写权限的。

google了一下发现一个解释：

目录其实也是一个文件，这个文件是其他文件的列表，其读、写、执行权限分别控制：

1. 读：你可以阅读这个文件列表，可以用ls列出所有文件或者可以使用命令补全来补全文件名
2. 写：可以修改、增加、删除这个列表上的内容
3. 执行：可以cd进这个目录，可以访问（读、写、执行）这个目录中的子文件


回想了一下刚才删除失败的原因，应该是rm在删除`tmp/1`的时候，因为没有`tmp`的执行权限，所以不能访问其子文件`tmp/1`导致的。

在没有这个目录的执行权限时，用`ls tmp`命令都会报错，因为没有权限去访问子文件：

```
# ll tmp
gls: cannot access tmp/1: Permission denied
total 0
-????????? ? ? ? ?           ? 1
```

[参考文章](http://unix.stackexchange.com/questions/21251/how-do-directory-permissions-in-linux-work)

但是奇怪的是，我在一台CentOS 6.0的机器上做同样的实验时，情况完全不一样，不管是cd/ls/rm这个目录，都不会有权限错误的提示，操作都可以进行。