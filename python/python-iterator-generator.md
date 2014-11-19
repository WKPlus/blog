Title: python iterator 和 generator
Date: 2014-09-23 15:57
Category: python

 

### iterator

[iterator](https://docs.python.org/2/library/stdtypes.html#iterator-types)是一个概念（或者认为是类型集合），而非某个具体类型，是指实现了如下两个方法的类型：

1. `__iter__()` 返回iterator对象本身
2. `next()` 返回下一个元素

例如，存在一些属于iterator的类型，但并没有iterator这种类型

```python
>>> l=[]
>>> type(l.__iter__())
<type 'listiterator'>
>>> d={}
>>> type(d.iterkeys())
<type 'dictionary-keyiterator'>
>>> type(d.iteritems())
<type 'dictionary-itemiterator'>
>>> type(d.itervalues())
<type 'dictionary-valueiterator'>
```

### generator

[generator](https://docs.python.org/2/library/stdtypes.html#generator-types)属于iterator，因为其实现了`__iter__`和`next`方法：

```python
>>> type(g)
<type 'generator'>
>>> dir(g)
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'next', 'send', 'throw']
```

我们可以使用[yield](https://docs.python.org/2/reference/expressions.html#yieldexpr)关键词来创建generator，yield关键词可以用在函数中，一个包含了yield关键词的函数就不再是普通函数了，而是一个generator函数了，每次调用函数都会返回一个generator，比如：

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = a + b, a

fib = fibonacci()
for i in xrange(10):
    print fib.next()
```

另外，python有个很强大的生成iterator的库[itertools](https://docs.python.org/2/library/itertools.html)，真的很强大，后面会写一篇文章来总结itertools的用法。

