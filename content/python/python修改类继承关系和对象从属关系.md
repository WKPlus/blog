title: python修改对象从属关系和类继承关系
Date: 2015-04-22 19:02
Category: python
Slug: python-instancecheck-subclasshook

###修改对象从属关系

其实这里想介绍的一个神奇的函数`__instancecheck__`，它的描述文档在[这里](https://www.python.org/dev/peps/pep-3119/)。

>The primary mechanism proposed here is to allow overloading the built-in functions isinstance() and issubclass() . The overloading works as follows: The call isinstance(x, C) first checks whether C.\__instancecheck\__ exists, and if so, calls C.\__instancecheck\__(x) instead of its normal implementation. Similarly, the call issubclass(D, C) first checks whether C.\__subclasscheck__ exists, and if so, calls C.\__subclasscheck__(D) instead of its normal implementation.


```
class MyMeta(type):
    def __instancecheck__(self, other):
        return True

class MyClass(object):
    __metaclass__ = MyMeta
    

assert isinstance(123, MyClass)
```

但是因为cpython具体实现的关系，`__instancecheck__`并不一定会被调用，如下：

```
class MyMeta(type):
    def __instancecheck__(self, other):
        return False

class MyClass(object):
    __metaclass__ = MyMeta
    

assert not isinstance(123, MyClass)
assert isinstance(MyClass(), MyClass)
```
[这个](http://stackoverflow.com/questions/17731207/why-instancecheck-is-not-always-called-depending-on-argument)问题的答案解释了原因。

可见文档也不一定完全对，代码才是不会骗人的。


###修改类继承关系

这里我们用到了`__subclasshook__`方法，其文档在[这里](https://docs.python.org/2/library/abc.html#abc.ABCMeta.__subclasshook__)。

```
from abc import ABCMeta
class MyClass(object):
    __metaclass__ = ABCMeta
    @classmethod
    def __subclasshook__(cls, C):
        return False

class MyClass2(MyClass):
    pass

assert not issubclass(MyClass2, MyClass)
```

另外，和PEP3119文档描述的不一样的是，`__isinstancecheck__`和`__subclasshook__`定义的位置是不同的：

* 前者是定义在`MyClass`的meta class里面
* 后者是定义在`MyClass`里面，不过`MyClass`还需要同时设置meta class为`abc.ABCMeta`或者其子类