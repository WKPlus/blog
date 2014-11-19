Title: python join不响应信号
Date: 2013-11-11 17:55
Category: python

python在写多线程程序时，发现多线程启动之后，用ctrl+c终止不了了，之前也没太关注，因为用kill -9还是可以终止的。

今天在写为一个python程序写一个signal handler的时候，发现竟然不生效。仔细研究了一下才发现，原来是当调用Thread.join之后，程序就不再能响应信号了（-9除外）。这应该就是之前ctrl+c不生效的原因，因为ctrl+c实际就是发了一个SIGINT信号。

 

为了要实现signal handler的问题，不能继续使用Thread.join了，只能使用下面的代码代替了：

```python
while threading.activeCount > 1:
    time.sleep(interval)
```
循环检测剩余的线程数，如果线程数大于1，证明还有子线程未退出，那么进入sleep等待。

这样实现可以绕过Threading.join之后不能响应信号的问题，不过缺点是会占用额外的CPU资源。占用多少CPU资源，要视循环间隔而定（即interval的值大小）。

