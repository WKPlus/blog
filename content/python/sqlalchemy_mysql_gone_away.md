Title: SQLAlchemy数据库连接被关闭
Date: 2016-03-15 11:02
Category: python
Slug: sqlalchemy-mysql-gone-way


最近在使用SQLAlchemy做一个后台server时，发现server启动一段时间之后偶尔会出现`"MySQL has gone away"`的错误。


研究了一下发现是因为[MySQL默认会关掉空闲的连接](http://dev.mysql.com/doc/refman/5.0/en/server-system-variables.html#sysvar_wait_timeout)，默认是28800秒，即8小时。

而后台server起来之后，如果8小时没有请求没有数据库操作，那么8小时之后原来的数据库连接就被MySQL关闭了，后面SQLAlchemy再使用该连接操作数据库的时候就会报`"MySQL has gone away"`的错误。

需要解决此问题，只需要在`create_engine`时加上`pool-recycle`即可，详细说明可参考[官方文档](http://docs.sqlalchemy.org/en/latest/core/pooling.html#setting-pool-recycle)
