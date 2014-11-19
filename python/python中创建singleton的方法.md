Title: python中创建singleton的方法
Date: 2014-09-11 17:40
Category: python

### 名称覆盖
-----------

```python
class MyClass(object):
    pass

MyClass = MyClass()
```

这是最简单粗暴的方法，直接用MyClass对象覆盖了同名的类，这样后面的代码就看不到MyClass类了也就不能继续生成这个类对应的对象了。


### 保存已经存在的类对象
-----------------------

```python
G_INSTANCES = {}

def get_ins(cls, *args, **kwargs):
    if cls not in G_INSTANCES:
        G_INSTANCES[cls] = cls(*args, **kwargs)
    return G_INSTANCES[cls]

class MyClass(object):
    pass

c1 = get_ins(MyClass)
c2 = get_ins(MyClass)
assert id(c1) == id(c2)
```

使用全局dict保存已经创建过的类对象，下次创建时如果已经存在直接返回。

 

### 使用闭包优化上一个方法
-------------------------

```python
def singleton(cls):
    instances = {}
    def get_ins(*args, **kwargs):
        if cls not in instances:
             instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_ins

class MyClass(object):
    pass
MyClass = singleton(MyClass)

c1 = MyClass()
c2 = MyClass()
assert id(c1) == id(c2)
```

闭包的含义和作用可以看参考材料，该例子中将全局的`G_INSTANCES`定义放到了singleton函数内。
这种方式还可以用python decorator的简写模式来写，MyClass类定义三行可以改为

```python
@singleton
class MyClass(object):
    pass
```

 

### 上一个例子的误区
-------------------

很多人第一次使用上面例子代码的时候，会认为假设有多个类都使用singleton方法，那么他们的对象存在同一个instance dict中，其实不然，每调用一次singleton函数，就会生成一个新的instance，因此假设上例的代码改为如下的样子，就会生成两个MyClass对象：

```python
def singleton(cls):
    instances = {}
    def get_ins(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_ins

class MyClass(object):
    pass

c1 = singleton(MyClass)()
c2 = singleton(MyClass)()
assert id(c1) == id(c2)
```

不过要解决这个问题也很简单，使用函数默认参数定义instances即可（又发现了一个函数默认参数的使用场景），将singleton定义改为：

```python
def singleton(cls, instances={}):
```

### 使用meta class
-----------------

meta class号称class的class，用来定义singleton实在是小菜一碟了，请看如下代码：

```python
class Singleton(type):
    instance = None
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class MyClass(object):
    __metaclass__ = Singleton
```

meta class的用法和含义，这里就不展开介绍了。
 

### 参考材料
-----------

http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python  
http://stackoverflow.com/questions/4020419/closures-in-python  
http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python

