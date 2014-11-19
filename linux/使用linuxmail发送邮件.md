Title: 使用linux mail发送邮件及一些问题解决
Date: 2013-11-11 18:57
Category: Linux

使用方式如下：

```bash
echo "test" | env from="fromaddress@yourdomain.com" mail -s "$(echo -e "title\nContent-Type: text/html")" toaddress@dianping.com
```

or

```bash
env from="fromaddress@yourdomain.com" mail -s "$(echo -e "title\nContent-Type: text/html")" toaddress@dianping.com < "context.html"
```

其中：

1. 通过设置from变量来修改邮件的发件人
2. 通过-s指定邮件标题，Content-type指定文件内容格式，chareset指定编码
3. 通过管道`echo "test" |`或者`<`写入邮件内容，可以是文本也可以是html格式


不过在使用过程中遇到两个问题导致邮件发送失败：

第一个问题比较傻，解决也很简单。原因是该机器上的postfix服务没有启动，解决方法很简单，运行`/etc/init.d/postfix start`命令即可。

第二个问题稍微复杂一点，发送之后，查看log文件（/var/log/maillog）发现连接gmail的服务器失败，Log信息如下：

```bash
Nov 11 18:41:45 localhost postfix/smtp[1441]: connect to aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:41:48 localhost postfix/smtp[1447]: connect to aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:42:06 localhost postfix/smtp[1441]: connect to alt2.aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:42:09 localhost postfix/smtp[1447]: connect to alt2.aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:42:27 localhost postfix/smtp[1441]: connect to alt1.aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:42:27 localhost postfix/smtp[1441]: connect to aspmx3.googlemail.com[2607:f8b0:4002:c01::1b]:25: Network is unreachable
Nov 11 18:42:27 localhost postfix/smtp[1441]: connect to aspmx4.googlemail.com[2607:f8b0:400d:c01::1b]:25: Network is unreachable
Nov 11 18:42:27 localhost postfix/smtp[1441]: 0F63760C26: to=<ghost@google.com>, relay=none, delay=79, delays=16/0.01/63/0, dsn=4.4.1, status=deferred (connect to aspmx4.googlemail.com[2607:f8b0:400d:c01::1b]:25: Network is unreachable)
Nov 11 18:42:30 localhost postfix/smtp[1447]: connect to alt1.aspmx.l.google.com[74.125.128.105]:25: Connection timed out 
Nov 11 18:42:30 localhost postfix/smtp[1447]: connect to aspmx2.googlemail.com[2a00:1450:4008:c01::1b]:25: Network is unreachable
Nov 11 18:42:30 localhost postfix/smtp[1447]: connect to aspmx5.googlemail.com[2607:f8b0:400c:c02::1a]:25: Network is unreachable
Nov 11 18:42:30 localhost postfix/smtp[1447]: 1420C60C27: to=<ghost@google.com>, relay=none, delay=63, delays=0.02/0.01/63/0, dsn=4.4.1, status=deferred (connect to aspmx5.googlemail.com[2607:f8b0:400c:c02::1a]:25: Network is unreachable)
```

从另外一些可以发送mail的机器上看log，发现解析的ip并不同，所以有点困惑为啥解析到了连接不上的服务器。甚至，曾一度怀疑是GFW的原因。

后来偶然发现log中有ipv6的地址，google上搜索了ipv6地址那一行信息之后，发现有人建议mail禁用掉ipv6。抱着死马当活马医的心态试了一下，发现竟然可以发出去了。

**解决方式：**

修改/etc/postfix/main.cf中的`inet_protocols = all`为`inet_protocols = ipv4`

发送成功之后，查看了一下成功的log，发现之前的Connection timed out记录还是存在的，不过连接ipv6的操作没有了，取而代之的是连接了其他的ipv4地址，而通过这些地址连接上服务器了。

这个问题解决的有点糊里糊涂。我的感觉是：因为连接重试是有次数限制了，假设是10次，10次里面前面8次尝试的是ipv4的地址，最后两次是ipv6的地址。但很不巧的是，前面连接的8个ipv4地址连接都失败了，最后的两个ipv6地址也失败了。但其实第9个ipv4地址是可以连接成功的，因此禁用掉ipv6之后，会连续10次去连接ipv4，于是，在第9次的时候连接成功了。
