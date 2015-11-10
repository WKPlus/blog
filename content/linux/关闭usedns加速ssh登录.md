title: 关闭UseDNS来加速ssh登录
Date: 2015-04-28 20:02
Category: linux
Slug: ssh-dns-slow


最近公司内部几台虚拟器在远程登录的时候特别慢，要等10秒左右才能连接上，开始也没怎么在意，因为公司内部无线网有时候就是很慢。

然后，偶然的机会下，我修改了这几台机器的dns服务器的配置（之前IT调整了dns服务器的ip，这几台远程机器没有我没及时做修改，所以dns服务器配置是错的），发现登录速度又恢复到秒登的级别了。

好奇心使然，我又把dns配置改成之前的，发现登录又要10秒左右了。

我发现这个问题越发有意思了，错误的dns还会影响到ssh的登录过程，之前是万万没想到的。在我的意识里，dns是用来解析域名对应的ip的，我用ssh通过ip来远程登录一台机器，过程中怎么会涉及dns解析呢？

于是做了个实验：先打开一个session，在该session里面一直使用netstat查看网络连接，同时另外一个session发起ssh登录，果然发现在登录过程中有访问dns server的udp连接。

但是为什么ssh登录的过程中为什么会使用到dns呢？google了一圈ssh登录过程，没找到能够解惑的材料。

直接google问题：ssh dns slow

终于找到不少解释，看来这个问题还是蛮普遍的：

http://unix.stackexchange.com/questions/56941/what-is-the-point-of-sshd-usedns-option

http://askubuntu.com/questions/246323/why-does-sshs-password-prompt-take-so-long-to-appear


解决这个问题也很简单，关闭UseDNS选项即可，在CentOS上关闭方法如下：

1. 修改`/etc/ssh/sshd_config`文件，在其中添加`UseDNS no`
2. 运行`service sshd restart`重启sshd
