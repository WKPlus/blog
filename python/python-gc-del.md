Title: 慎用python的__del__方法
Date: 2015-04-10 19:02
Category: python
Slug: python-del-method

python的\__del__方法是什么？

和C++的destructor有点类似，在对象销毁的时候，会调用对象的\__del__方法，**但是，但是**有些区别。

有哪些区别呢？

### 调用时机

在C++里面，对象是用户手工管理的，用户通过显示地调用`delete obj`来销毁对象`obj`，对象销毁时对象的destructor会被调用。

而在python里面，用户不需要手工管理对象，python自带的垃圾回收机制会通过**引用计数**来判断对象是否可以销毁。当一个对象的引用计数为0时，python解析器会自动销毁该对象，同时调用该对象的`__del__`方法。

也就是说`del obj`在python里面并不一定会销毁一个对象，只是让该对象的引用计数减一。

> "del x" doesn't directly call x.\__del__() — the former decrements the reference count for x by one, and the latter is only called when x's reference count reaches zero. Some common situations that may prevent the reference count of an object from going to zero include: circular references between objects


### 可靠性
在C++里面，一个对象销毁时，不管是因为用户显示调用了`delete obj`，还是栈对象退出其作用区域时，或者是全局对象在程序退出时销毁，他的destructor都一定会被调用。因此，C++里面经常在destructor里面(比如RAII模式)做一些资源释放或者刷buffer的操作。

但是在python里面，对象的destructor则不一定会被调用，如果把重要的操作放在destructor里面并期待它一直会执行，你可能会踩大坑。

首先我们先来猜猜：什么情况下destructor不会执行呢？

destructor是在对象销毁之后才会执行的，那么如果对象不会被销毁呢？那么有可能对象不被销毁么？我们知道，python使用的引用计数是否为0来判断对象是否需要销毁，对于引用计数这种方式，循环引用是其大敌。

下面写一个循环引用的代码，看看会怎样：

```python
class A(object):
    def __init__(self, parent):
        print "A init"
        self.parent = parent

    def __del__(self):
        print "A del"


class B(object):
    def __init__(self):
        print "B init"
        self.child = A(self)

    def __del__(self):
        print "B del"


b = B()
```
这段代码执行的输出是：

```
B init
A init
```

可以看到A和B的对象的destructor都没有执行，即使python都退出了也没有执行。

我想，python[官方文档](https://docs.python.org/2/reference/datamodel.html#object.__del__)这里已经做过*免责声明*了：

> It is not guaranteed that \__del__() methods are called for objects that still exist when the interpreter exits.

这一句说的是：如果python解析器退出时，有些对象还存在（没有被销毁），不保证这些对象的`__del__`方法会被调用。

> Circular references which are garbage are detected when the option cycle detector is enabled (it’s on by default), but can only be cleaned up if there are no Python-level \__del__() methods involved.

这一句说的是：如果循环引用检查器打开了（默认是打开的），循环引用的对象是可以检查到的，但是只有没有定义`__del__`方法的对象会被销毁。

我们再看看[python gc的文档](https://docs.python.org/2/library/gc.html#gc.garbage)：

> A list of objects which the collector found to be unreachable but could not be freed (uncollectable objects). By default, this list contains only objects with \__del__() methods. 

这一段说明：`gc.garbage`是一个list，里面存的都是一些不可达也不能释放的对象，默认情况下都是定义了`__del__`的对象。

> Python doesn’t collect such cycles automatically because, in general, it isn’t possible for Python to guess a safe order in which to run the \__del__() methods. 

这一段解释了原因：因为循环引用，python不知道正确的调用这些对象的`__del__`方法的顺序。

> It’s generally better to avoid the issue by not creating cycles containing objects with \__del__() methods, and garbage can be examined in that case to verify that no such cycles are being created.

最后一段说：最好不要在造出循环引用的同时还为处在循环引用中的对象定义`__del__`方法。

### 后话
到这里，应该是真相大白了，循环引用和`__del__`同时使用就会出现问题。看到这里，也许有人会说：谁让你自己定义一个循环引用呢，这种设计模式本身就有问题，如果程序设计的好，没有循环引用，那么`__del__`还是可以顺便用。

那么我提供一个[case](http://www.708luo.com/posts/2015/04/python-new-style-class-del/)给你看看，并不是你不定义循环引用，它就不存在了。

总之，`__del__`不是那么可控和可靠，有些重要操作还是不能依赖它。
