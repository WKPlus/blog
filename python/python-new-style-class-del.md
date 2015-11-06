Title: python解释器退出时new style class的类属性的__del__方法不会被调用
Date: 2015-04-09 19:04
Category: python
Slug: python-new-style-class-del

先看看如下一段代码输出什么：

```python
class A(object):
    def __init__(self):
        print "A init"

    def __del__(self):
        print "A del"


class B(object):
    a = A()
    #def __init__(self, a=A()):
    #    self.a = a

print "test"
```

输出：

```
A init
test
```

就因为这个问题，导致我的一个程序资源泄露了:( 而之前这个程序已经正常运行了半年了，只是某次升级的时候，我顺手把A和B从old style class改成new style class了。

**以后切记**：不要把资源释放的工作放在\__del__方法中，这个方法的会不会被调用、会被调用几次，实在有太多的不确定因素了。python 2.5之后用`with`来释放资源。

下面我们再来研究一下，为什么只有new style class会有这种情况呢？

在[\__del__方法的官方文档](https://docs.python.org/2/reference/datamodel.html#object.\__del__)里发现一个关键说明：

> It is not guaranteed that __del__() methods are called for objects that still exist when the interpreter exits.

那么也就是说，在python解释器退出时，`B.a`还是处于被引用状态的，也就是说`B`还是处于被引用状态的。

那么为什么old style class在退出的时候就不会处于被引用，但是new style class在退出的时候会处于被引用呢？

[StackOverFlow](http://stackoverflow.com/questions/29511332/why-do-new-style-class-and-old-style-class-have-different-behavior-in-this-case/29519325#29519325)上有一个答案，是因为CPython的new style class是有循环引用的，通过下面的命令也可以看出new style class和old style class的引用数的区别：

```python
>>> import sys
>>> class A():
...     pass
...
>>> sys.getrefcount(A)
2
>>> class B(object):
...     pass
...
>>> sys.getrefcount(B)
5
```
为啥A的引用数是2而不是1呢？[这里](http://stackoverflow.com/questions/10302133/why-does-sys-getrefcount-return-2)有一个答案：因为`getrefcount`函数执行的时候，其参数又多了一次对A的引用。

总之，`__del__`方法能不能被调用，是不确定的，最好不要把资源释放的操作放在这里做。

