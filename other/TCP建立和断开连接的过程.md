Title: TCP建立和断开连接过程中的状态转换
Date: 2013-11-29 18:57
Category: 杂项
Slug: tcp-connect-disconnect

最近看到netstat中的一些状态，比较好奇，整理了一下tcp连接建立和断开过程中的状态转换。

为了简单起见，这里没有包含一些异常情况。

另外有些状态转换具体是发生在收包还是收包+发包后，还没有搞清楚，比如TCP建立过程中，Server从LISTEN到SYN\_RCVD状态的变化，是在接受到SYN包的时候还是在接受的SYN包然后发出ACK+SYN之后。但因为收包+发包都是在一台机器做的，轻载的情况下这两者之间的时间应该可以忽略，暂且把它们画在一起，认为几乎同时发生且状态转换在此之后。

 

TCP建立过程，如下图：

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/11/NewImage.png "NewImage.png")

 

TCP断开过程，如下图：（断开过程的状态转换可能有两种情况）

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/11/NewImage1.png "NewImage.png")

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/11/NewImage2.png "NewImage.png")


**备注：**

MSL=Maximum Segment Lifetime
