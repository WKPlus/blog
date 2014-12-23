Title: python print 重定向到文件时编码错误
Date: 2014-06-13 22:35
Category: python
Slug: python-print-encode-error

使用python print的时候经常遇到一个奇怪的问题：

print unicode时，如果unicode包含中文，输出到屏幕时一切正常，但是把屏幕输出重定向到文件时，却报编码错误。错误内容大致如下：

```bash
UnicodeEncodeError: 'ascii' codec can\'t encode characters in position
0-1: ordinal not in range(128)
```
 
原因是这样的：

1. 因为你的屏幕显示编码是utf8格式的，所以python知道使用utf8来对unicode进行编码
2. 重定向到文件时，python并不知道文件格式是什么，所以只能使用默认的ascii来进行编码，而ascii不能对中文进行编码，就会看到前面的异常
3. 其实不仅仅是编码中文时会遇到异常，只要编码的值超过128（ascii表是使用7位的）都会异常

 

怎么快速解决这个问题呢？

1. 在代码中以UTF-8的方式打开文件，然后写文件
2. print unicode之前，显示按str的来源方式编码，比如utf8。原来的print需要改为`print ucontent.encode(‘uft8’)`
3. `env PYTHONIOENCODING=utf-8 python ./script.py > log`

如果是写一个小工具，临时用用，推荐用第三种方式，简单、快捷。

