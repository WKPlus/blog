Title: dns相关知识和工具
Date: 2016-03-24 20:02
Category: other
Slug: dns-related-knowledge


##Authoritative VS non-authoritative
使用`nslookup`查询域名的时候，经常发现"Non-authoritative answer"这样输出。

那么authoritative/non-authoritative answer分别是什么意思呢？

###Authoritative answer: 
官方dns server返回的域名解析结果，比如ns1.google.com返回的maps.google.com域名解析的结果（你需要把ns1.google.com配置成你的dns resolver）。

###Non-authoritative answer: 
非官方dns server返回的域名解析结果，比如你的路由器或者局域网中的dns server返回的maps.google.com域名解析的结果。


参考文档：

1. [meaning of non-authoritative answer](http://serverfault.com/questions/413124/dns-nslookup-what-is-the-meaning-of-the-non-authoritative-answer)
2. [authoritative answer vs non-authoritatice answer](https://social.technet.microsoft.com/Forums/windowsserver/en-US/89bd7e00-17b1-4fba-a2f2-1f6191d4a1c3/authoritative-dns-server-vs-nonauthoritative-dns-serve?forum=winservergen)



##Cache相关
###nscd
nscd(name service cache daemon)是用来做DNS cache的工具，查看本机有没有打开nscd可以：

1. 通过`service nscd status`查看nscd的状态
2. 通过`ps -ef|grep nscd`查看是否有nscd进程


###DNS resolver
DNS resolver即通常所说的DNS server，*nix系统中配置在/etc/resolv.conf这个文件中。

DNS resolver也会提供cache功能，常见的DNS resolver有：

1. [bind](https://www.isc.org/downloads/bind/)
2. [powerdns](https://www.powerdns.com/)
3. [unbound](https://unbound.net/)
4. [Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html)
5. [Erl-DNS](https://github.com/aetrion/erl-dns/)


###清除dns缓存

1. 清除local cache
   * MAC:  `sudo dscacheutil -flushcache`
   * nscd: `service nscd restart`
2. 清除resolver的缓存
   * bind: `rndc flush` 或者重启bind



参考文档：

1. [how-to-flush-dns-cache](http://unix.stackexchange.com/questions/67592/how-to-flush-local-dns-cache-in-centos)
2. [top-dns-servers](https://blog.dnsimple.com/2015/02/top-dns-servers/)
3. [debian-ubuntu-flush-dns-cache](http://www.cyberciti.biz/faq/rhel-debian-ubuntu-flush-clear-dns-cache/)

##DNS记录类型
###CNAME记录
相当于一个域名的别名，比如`nslookup mail.google.com`里面会看到：

	mail.google.com	canonical name = googlemail.l.google.com
	googlemail.l.google.com	canonical name = mail-china.l.google.com
	

###A记录
一个域名对应的IP，比如`nslookup mail.google.com`里面会看到：

	Name:	mail-china.l.google.com
	Address: 173.194.72.17
	
根据上面两条CNAME记录和一条A记录，最终可以查到mail.google.com这个域名对应的ip是173.194.72.17。

##相关工具
###nslookup
nslookup可用来查询域名对应的ip，使用方式比较简单，直接`nslookup <domain>`就可以了。

###dig
dig工具功能更加多一些，可以用来排查一些DNS解析相关的问题。

	; <<>> DiG 9.8.3-P1 <<>> mail.google.com
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19669
	;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 4, ADDITIONAL: 4

	;; QUESTION SECTION:
	;mail.google.com.		IN	A

	;; ANSWER SECTION:
	mail.google.com.	40958	IN	CNAME	googlemail.l.google.com.
	googlemail.l.google.com. 100	IN	CNAME	mail-china.l.google.com.
	mail-china.l.google.com. 227	IN	A	173.194.72.17
	mail-china.l.google.com. 227	IN	A	173.194.72.19
	mail-china.l.google.com. 227	IN	A	173.194.72.83
	mail-china.l.google.com. 227	IN	A	173.194.72.18

	;; AUTHORITY SECTION:
	google.com.		19631	IN	NS	ns4.google.com.
	google.com.		19631	IN	NS	ns1.google.com.
	google.com.		19631	IN	NS	ns2.google.com.
	google.com.		19631	IN	NS	ns3.google.com.

	;; ADDITIONAL SECTION:
	ns2.google.com.		68122	IN	A	216.239.34.10
	ns1.google.com.		6516	IN	A	216.239.32.10
	ns3.google.com.		178618	IN	A	216.239.36.10
	ns4.google.com.		341366	IN	A	216.239.38.10

	;; Query time: 2020 msec
	;; SERVER: 10.128.16.28#53(10.128.16.28)
	;; WHEN: Thu Mar 24 17:48:43 2016
	;; MSG SIZE  rcvd: 285

