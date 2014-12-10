Title: 将xfe格式的unicode转化为u00fe格式
Date: 2014-12-10 17:55
Category: python

python 2.x中的unicode，如果某个字符位于80和ff之间，默认是用单字节表示的：

```python
>>> s=u'··'
>>> s
u'\xb7\xb7'
>>> print "%r" % s
u'\xb7\xb7'
```

如果想转化`\u00b7`的格式呢？
正像我在[这个问题](http://stackoverflow.com/questions/23253879/escaping-unicode-string-using-u)回答一样，`json.dumps`可以用来做这个事情：

```python
>>> s=u'··'
>>> json.dumps(s)
'"\\u00b7\\u00b7"'
>>> print json.dumps(s)
"\u00b7\u00b7"
```
