Title: 采坑记录：python json不支持int类型key
Date: 2014-12-10 17:55
Category: python
Slug: json-int-key


最近踩了一个很好玩的坑：

在python中将key为int类型的dict通过`json.dumps`出来之后，再用`json.loads`转为为dict时，发现原来int类型的key变成了str类型

```python
>>> d={1:2}
>>> dump = json.dumps(d)
>>> d
{1: 2}
>>> dump
'{"1": 2}'
>>> d1 = json.loads(dump)
>>> d1
{u'1': 2}
```

后来google搜了一下，发现和我踩过同样坑的人还不少：

http://stackoverflow.com/questions/17099556/why-do-int-keys-of-a-python-dict-turn-into-strings-when-using-json-dumps
http://stackoverflow.com/questions/1450957/pythons-json-module-converts-int-dictionary-keys-to-strings
