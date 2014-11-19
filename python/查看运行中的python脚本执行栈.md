Title: 查看运行中的python脚本的堆栈
Date: 2012-11-06 16:26
Category: python

对于c/c++程序，我们可以在运行过程中通过pstack来查看程序当前的执行堆栈。

那么对于python脚本呢？

## 方法一

如果脚本是前台运行，可以直接Ctrl+c中止该脚本，即可查看当前的执行堆栈。

如果脚本是后台运行的，可以先`fg jobid`，然后直接Ctrl+c中止脚本。当前的执行堆栈会被打印到脚本后台运行时的输出中
如果是`./test.py &`运行则是输出到前台；如果是`nohup ./test.py &`运行则是输出到nohup.out；如果加了输出重定向，则是打印到重定向的输出文件中

## 方法二：

通过pdb完成，主要是为python脚本设置一个signal\_handler，在其hang住的时候发送信号给它，然后进入debug模式。这时可以用w命令打印出当前执行堆栈。

参考[这篇文章](http://blog.csdn.net/toymaker/article/details/6982131)

不过这个方式，**对后台运行的程序无效**（不管是否先将程序转到前台）。而且需要提前加部分代码，对于已经在运行中的脚本无效。

好处是，如果程序是前台运行的，进入debug模式之后还可以继续运行，而不像方法一直接就终止脚本了。（有一点要注意的是：如果脚本处于sleep状态，经过信号处理之后sleep就被唤醒了）

## 方法三：

使用gdb打印python脚本当前执行堆栈。（不依赖gdb版本）

具体使用方式：

1. 编译带调试符号的python解析器：编译python时使用`make "CFLAGS=-g -fno-inline -fno-strict-aliasing"`
2. 添加gdb中可以使用的函数：从[这里](http://svn.python.org/view/python/branches/release27-maint/Misc/gdbinit)下载文件，将其内容写入到\~/.gdbinit中（gdb 7.\*版本无需此操作）
3. 运行`gdb python <pid>`来attach到python进程
4. 运行pystack即可打印出堆栈

该方式不会终止脚本，所以如果可以的话，推荐使用这种方式。

该方法官方文档在[这里](http://wiki.python.org/moin/DebuggingWithGdb)。

## 方法四：

使用gdb打印python脚本当前执行堆栈。（需要gdb 7.\*版本，未成功尝试）

该方法在[这里](http://my.oschina.net/alphajay/blog/70755)有说明。

尝试时遇到`"RuntimeError: No type named size\_t."`错误，关于该错误的说明，可以查看[这里](http://misspent.wordpress.com/2012/03/24/debugging-cc-and-cpython-using-gdb-7s-new-python-extension-support/)。

