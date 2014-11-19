Title: 非root使用源码安装mysql
Date: 2012-09-27 20:02
Category: 杂项

安装步骤：

1. 从mysql官网下载源码。[5.5.24源码地址](http://downloads.mysql.com/archives/mysql-5.5/mysql-5.5.24.tar.gz)
2. 下载并安装cmake，用来生成makefile。[2.8.9地址](http://www.kitware.com/news/home/browse/CMake?2012_08_09&CMake+2.8.9+is+Now+Available%21)。
3. 解压mysql-5.5.24.tar.gz，进入解压后的目录
4. 运行`cmake -i`，
   - 设置三个变量：`CMAKE_INSTALL_PREFIX`,`MYSQL_DATADIR`,`SYSCONFDIR`，其他默认即可。
   - 这三个值默认是/usr/local/mysql作为根目录，可以设置为/home/$USER/mysql或者其他地址
   - 或者直接运行`cmake -D CMAKE_INSTALL_PREFIX=/$HOME/tools/mysql -D MYSQL_DATADIR=/$HOME/tools/mysql/data –D SYSCONFDIR=/$HOME/tools/mysql/etc .`
5. 运行`make && make install`
6. 进入mysql安装目录，即`CMAKE_INSTALL_PREFIX`指定地址，运行`nohup ./bin/mysqld &启动mysql`

如果安装后，启动mysql的时候报类似`“Can't open the mysql.plugin table.  Please run mysql\_upgrade to create it.”`这样的错误，执行 `cd /$HOME/tools/mysql && scripts/mysql_install_db --user=work --basedir=/$HOME/tools/mysql --datadir=/$HOME/tools/mysql/data` 即可解决该问题。

如果不小心忘记了root密码，可按如下的步骤恢复：

1. 停掉mysql：`killall mysqld`
2. 以skip-grant-table 方式启动`mysql：./mysqld\_safe –skip-grant-table &`
3. 登录`mysql：./mysql –uroot mysql`
4. 修改root密码：`UPDATE user SET password=password('root_password') WHERE user='root';flush privileges;exit;`
5. 重启mysql（非skip-grant-table方式）

顺便补充几个mysql数据库管理命令：

1. 创建用户名为user1/密码为password的用户：`create user 'user1'@'%' identified by 'password'`
2. 删除用户`drop user 'user1'@'%'`
3. 用户权限相关：
   - `grant all on *.* to 'user1'@'%'` 给用户user1开通所有数据库所有表的全部权限
   - `grant all on *.* to 'user1'@localhost` 给本地登录的用户user1开通所有数据库所有表的全部权限
   - `grant select on db_a.table_b to 'user1'@'%'` 给用户user1开通数据库db\_a中table\_b表的select权限
   - `show grants for user1` 查看user1用户的权限
   - `revoke all on *.* from 'user1'@'%'` 撤销用户user1所有数据库所有表的全部权限
4. 创建/删除数据库： `create database database1; drop database database1;`
5. 查询主从库状态：`show slave/master status;`
6. 查询从库设置：`show variables like '%slave%';`

另外，如果新创建的用户使用密码无法登录，不使用密码反而可以登录的情况，是因为mysql中存在可以本地登录的匿名用户。
删除本地登录的匿名用户即可解决这个问题（`drop user ''@localhost`）。 
具体原因如下：

1. mysql中用来标示用户的不仅仅有用户名，还有登录地址。如：'user1'@localhost'和'user1'@'ip1'是不同的（ip1为一个远程地址）
2. 用户登录的时候，是从mysql.user表从前往后匹配的
3. 如果创建一个'user1'@'%'的用户，在mysql.user表中会排在''@localhost'（表示本地登录的匿名用户）之后
4. 本地登录使用`mysql –uuser1 –ppassword`时，实际上是通过`mysql –hlocalhost –uuser1 –ppassword`在登录，会首先匹配到`''@localhost'`这条记录。因此就变成了本地使用匿名账户登录，而本地匿名用户一般是不需要密码的，这时就出现了使用密码不能登录，不使用密码反而可以登录。
5. 聪明的人应该已经可以想到，再创建一个`'user1'@localhost`也可以解决这个问题

