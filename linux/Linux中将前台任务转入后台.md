Title: linux会话中将前台任务转入后台
Date: 2012-07-26 20:34
Category: Linux

有时会遇到这样一种情况：在没有使用screen之类的管理会话的软件的时候，需要退出当前运行会话，但会话中有个任务运行了很久了，退出的话这个任务会被kill掉（收到SIGHUP的信号）。

下面的方法可以将这个前台进程转入后台，并指定这个任务不被发送SIGHUP信号：

1.  ctrl+z将任务暂停，这时屏幕会打印这样一句`[1]+  Stopped  ./myserver`
2.  使用`bg 1`将这个任务转入后台运行（1是刚才暂停任务的job号，步骤1中屏幕提示方括号里面的内容，如果忘了也可以用jobs命令查看）
3.  使用`disown –h %1`指定shell退出时不要发送SIGHUP给任务1（注意任务号前面有个%）

关于disown的详细说明，可以查看man bash或man disown搜索disown

当然，如果在启动任务之前意识到这个问题，可以用`nohup ./myserver &`的方式将会话放到后台运行，并通过nohup指定进程不处理SIGHUP信号。

