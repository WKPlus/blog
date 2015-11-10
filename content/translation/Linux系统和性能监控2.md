Title: Linux系统和性能监控(2)
Date: 2013-01-01 23:13
Category: 翻译
Slug: linux-system-performance-monitoring-2

原文Linux System and Performance Monitoring，作者Darren Hoch。

## 2.0 安装监控工具

大部分Unix系统发布的时候会自带一系列的监控工具，这些监控工具自Unix诞生起就已经成为系统的一部分了。Linux把这些监控工具作为系统的一部分或者附件发行。基本上，所有的Linux发行版本都有包含这些工具的安装包。尽管类似的开源和第三方的监控工具也不少，这篇文章主要还是介绍这些内建工具的使用。

本文将介绍如何应用下列工具来监控系统性能：

|Tool|Description|Base|Repository|
|-|-|-|-|
|vmstat|all purpose performance tool|yes|yes|
|mpstat|provide statistics per CPU|no|yes|
|sar|all purpose performance monitoring tool|no|yes|
|iostat|provides disk statistics|no|yes|
|netstat|procides network statistics|yes|yes|
|dstat|monitoring statistics aggregator|no|in most distributions|
|iptraf|traffic monitoring dashboard|no|yes|
|netperf|network bandwidth tool|no|in most distributions|
|ethtool|reports on ethernet interface configuration|yes|yes|
|iperf|network bandwidth tool|no|yes|
|tcptrace|packet analysis tool| no|yes|


