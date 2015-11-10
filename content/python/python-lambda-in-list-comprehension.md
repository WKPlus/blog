Title: 在python列表推导中使用lambda可能遇到的问题
Date: 2015-10-11 19:28
Category: python
Slug: python-lambda-in-list-comprehension

相信python代码写多了人应该都会遇到或见过下面这种情况：

```
functions = [lambda x: i*x for i in xrange(5)]
[f(2) for f in functions]
```
输出结果：`[8,8,8,8,8]`，而并不是`[0,2,4,6,8]`。

---
原因是：
使用lambda生成的匿名函数的时候，并没有立即查找`i`并求值，在函数被调用时才会查找`i`并求值，而在函数被调用的时候`i`的值是4。

比如你定义一个函数，引用一个不存在的变量，在函数定义的时候并不会报错，只有函数被调用的时候才会提示找不到变量：

```
f = lambda x: nonexist_i*x
f(1)
```
只有在执行`f(1)`的时候才会报：`NameError: global name 'nonexist_i' is not defined`。

[Stackoverflow上面](http://stackoverflow.com/questions/28268439/python-list-comprehension-with-lambdas)也有人问过类似的问题。

---
因此可以想到，解决这个问题的办法是：使得在定义函数的时候，查找i并求值。

stackoverflow上很多人推荐这种方式：

```
functions = [lambda x, j=i: j*x for i in xrange(5)]
[f(2) for f in functions]
```

我认为这样写可能更容易理解一点：

```
def create_function(i): return lambda x: i*x
functions = [create_function(i) for i in xrange(5)]
[f(2) for f in functions]
```

---


最近看ruby代码的时候发现collect和block的组合用法，可以用来做类似的事情：

```
functions = (0..4).collect{|x| lambda{|y| y*x}}
functions.each {|f| print f.call(2)}
```
输出结果：`02468`。

因此模仿ruby的方式，用python写了一个类似的实现：

```
functions = map(lambda x: (lambda y:y*x), xrange(5))
[f(2) for f in functions]
```
输出结果：`[0,2,4,6,8]`
