Title: python MySQLdb的初步使用
Date: 2012-09-03 20:51
Category: python

MySQLdb库使用还是比较简单的，了解了几个API就可以开始捣腾了。

这里有一些[API的说明](http://mysql-python.sourceforge.net/MySQLdb.html#connection-objects)

基本使用步骤：

1.  导入MySQLdb库：`import MySQLdb`
2.  建立一个DB连接：`db_con = MySQLdb.connect(DB_host,DB_user,DB_password,DB_database)`
3.  执行命令：`db_con.query(sql_cmd)` 或者 `cursor = db_con.cursor(); cursor.excute(sql_cmd); cursor.close()`
4.  获取返回值：`db_con.store_result().fetch_row()`，这个返回值是一个二元元组。比如要获取返回值的第一列第一行就是`db_con.store_result().fetch_row()[0][0]`
5.  关闭连接：`db_con.close()`

**有一点比较需要注意的是：**

`store_result()`和`fetch_row()`函数并不仅是返回某个值这么简单，而是有副作用的，调用一次之后会清除原来的结果。
比如第一次调用`store_result()`之后，之间没有query操作，再次调用`store_result()`的结果则是None，`fetch_row()`也类似，不过结果不是None而是空元组。

因此如果需要多次使用这两个函数的返回值，需要用临时变量保存。

**update:**

更新MySQL版本之后发现`query("insert...")`之后，表格中并没有增加数据，发现是query的insert的操作没有被立刻执行（我理解是缓存了）。 
需要调用一下`db_con.commit()`或者建立连接之后调用`db_con.autocommit(True)`

