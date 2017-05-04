Title: 压测时本地端口耗尽问题分析
Date: 2017-05-04 20:02
Category: other
Slug: tcp-local-port-exhausted


最近在压测的时候遇到一个问题，python requests库在发起HTTP请求的时候，报错：`Failed to establish a new connection errno 99`。查了一下，这和错误是因为本地TCP端口耗尽导致的。  
因为之前通过打开`tcp_timestamps`和`tcp_tw_reuse`选项解决过这个问题了，这次又出现这个问题，我觉得是时候好好梳理一下这个问题的来龙去脉了。
  
  
### 第一个问题，本地端口有哪些可用？
首先，需要了解到TCP协议中确定一条TCP连接有4要素：`local IP`, `local PORT`, `remote IP`, `remote PORT`。这个四元组应该是唯一的。  
在我们发送HTTP请求的时候，`local IP` `remote IP` `remote PORT`是固定的，只有`local PORT`是可变的，可用的`local PORT`的数量就限制了client和server之间TCP连接数的数量。
    
TCP协议中`PORT`部分是用两个字节来表示的，也就是说可用的端口数量肯定不能超过65536个。  
另外，这其中还有些端口是系统保留的，需要root权限才可以使用的，在CentOS系统中，client端可以使用的端口可以通过`sysctl -a|grep net.ipv4.ip_local_port_range`来查看，比如我在一台机器上看到:
    
    net.ipv4.ip_local_port_range = 32768	61000
表示client可用的端口是[32768, 61000]，共28233个。那么这台机器和另外任意一台机器，**同时**只能建立28233个TCP连接。


### 第二个问题，短连接并不会同时存在大量TCP连接，端口为什么还是耗尽了？
上一步我们分析到，client和server之间只能**同时**存在28233个TCP连接，但是我们的压测用的是短连接，连接用完就释放掉了，端口应该也会释放掉，为啥还会产生端口耗尽的问题呢？

这就需要提到TIME_WAIT这个状态了，TCP连接断开的时候，主动发起连接断开操作的一方，最后会停留在TIME_WAIT状态，会持续2*MSL的时长，这个状态的端口是不能被使用的，准确的说是当新的TCP连接的`local IP` `remote IP`和`remote PORT`和TIME_WAIT状态的连接一致时这个端口不能被使用。  
这个值在CentOS上可以通过`sysctl -a|grep net.ipv4.tcp_fin_timeout`来查看，我这台机器上是：

	net.ipv4.tcp_fin_timeout = 60
表示TIME_WAIT会保持60秒。

**可以推论：**
    
    如果client机器有28233端口可用，TIME_WAIT 60秒，短连接的方式发起请求，那么这个client发起的请求的QPS是不能超过28233/60的。


### 第三个问题，为什么有TIME_WAIT状态？
想象这么一个场景：
> 1. A和B建立了一个TCP连接，A向B发送消息包1 2 3，消息包3传给B的时候延迟了，A又重传了消息包3，A和B完成通信断开连接，双方都很happy。
> 2. A和B又建立一个TCP连接，用了相同的`local IP` `local PORT` `remote IP` `remote PORT`，A向B发送消息包1 2，B收到1 2之后，上一个连接延迟的消息包3来了，B无法区分这个消息包是上一个TCP连接的，SEQ=3刚好排在2后面。**BOOM!**

TIME_WAIT状态主要就是为了解决这个问题：防止延迟的无效消息包被误认为是合法的。

想想看，一个延迟的无效消息包被认为是合法的必须要这个消息包看起来是当前某个TCP连接的，需要：

1. 这个消息包中的`local IP` `local PORT` `remote IP` `remote PORT`和某个TCP连接一致
2. SEQ number也刚好合法，如果是一个已经接受过的seq number，会被认为是一个重传的包丢弃掉

引入TIME_WAIT状态，直接把上述的条件1封死：TIME_WAIT状态持续时间是两倍的MSL，MSL是什么？MSL全称是Maximum Segment Lifetime，是一个TCP包的最大存活时间，一个TCP包一旦在网络上存活超过MSL，会直接被丢弃。  
TIME_WAIT状态持续2倍MSL之后，可以确保老的TCP连接逗留在网络上的消息包已经全部消失了。

到此可以理解，TIME_WAIT这个状态存在的原因了。

### 第四个问题，单台机器发送请求每秒要超过<可用端口数>/60怎么办？
第一个方式很简单，用长连接，这个就不多解释了。
第二个方式，在网上也很容查到，打开`tcp_tw_reuse`。

那么为什么打开`tcp_tw_reuse`就可以使用TIME_WAIT状态的端口呢？不怕延迟的消息包被误认为合法的么？

这里就需要提到另外一个选项了：`tcp_timestamps`，打开这个选项之后，TCP包里面会带上发包机器的当前时间戳。

可以这么想象一下：如果每个TCP包带上原始发包时的时间戳，如果一个延迟的消息包到达B，B可以拿这个消息包的时间和TCP连接建立的时间做一个对比，如果消息包的时间比较早，那么这就是上一个TCP连接延迟的消息包，丢弃掉就好。

通过时间戳的比较，也可以解决延迟消息包被误认为合法的问题。因此同时打开`tcp_timestamps`和`tcp_tw_reuse`之后，client端的TIME_WAIT端口是可以被复用的。

但要注意的是：

1. `tcp_timestamps`需要client和server端同时打开才生效（我们这次遇到端口耗尽的问题就是因为server端没有打开tcp_timestamps选项）
2. `tcp_timestamps`时间戳精确到秒，也就是TIME_WAIT状态的端口也在下一秒才可以重用，如果继续使用短连接的话，发送请求的QPS是不能超过可用端口数的


#### 参考文档
https://vincent.bernat.im/en/blog/2014-tcp-time-wait-state-linux
http://perthcharles.github.io/2015/08/27/timestamp-NAT/
https://saview.wordpress.com/2011/09/27/tcp_tw_recycle%E5%92%8Cnat%E9%80%A0%E6%88%90syn_ack%E9%97%AE%E9%A2%98/
http://www.orczhou.com/index.php/2011/10/tcpip-protocol-start-rto/