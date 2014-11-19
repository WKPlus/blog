Title: 问号 ( ? ) 在python正则分组中的用法
Date: 2014-01-17 18:24
Category: python

## 非捕获分组 (Non-capturing Groups)：

首先是上次文章提到一个非捕获分组的用法：

```python
>>> print a
a123b123b
>>> print re.match(r"a(123)", a).groups()
('123',)
>>> print re.match(r"a(?:123)", a).groups()
()
>>> print re.match(r"a(?:123)", a).group()
a123
```

非捕获分组，即该分组不记录在最终的groups中，但是还是会匹配的


## 命名分组 (Named Groups)：

```python
>>> print a
a123b123b
>>> print re.match(r"a(?P<namedgroup1>[1-3]+)b",a).groups()
('123',)
>>> print re.match(r"a(?P<namedgroup1>[1-3]+)b",a).group("namedgroup1")
123
>>> print re.match(r"a(?P<namedgroup1>[1-3]+)b",a).group(1)
123
```

可以使用命名去访问分组的内容，这个才正则表达式比较复杂、分组比较多的时候比较好用。

另外一个官方的命名分组的用法案例是：（**其中(?P=word)表示引用word这个命名分组的内容**）

```python
>>> p = re.compile(r'(?P<word>\b\w+)\s+(?P=word)')
>>> print re.search(p,'Paris in the the spring').group()
the the
>>> print re.sub(p,'the2 \g<word> the2','Paris in the the spring')
Paris in the2 the the2 spring
```

这样，在整个正则表达式中，表达式后面可以使用前面的分组内容。另外，re.sub中也可以使用命名分组的内容，用法是：`\g<group name>`。

 

## 向后断言 (positive lookbehind assertion)：

```python
>>> print a
a123b123b
>>> print re.findall(r"123b",a)
['123b', '123b']
>>> print re.findall(r"(?<=a)123b",a)
['123b']
```

即匹配以`(?\<…)`中…开头的字符串（案例中是123b）。可以看到，没有加向后断言之前，可以匹配到两个123b，加了a作为前缀之后，只能匹配到第一个123b了。

为啥叫向后断言呢？明明是增加了一个匹配的前缀呀！个人认为是因为正则匹配是从字符串前端往后端匹配的，其前缀反而就成了behind了。

其实个人感觉，如果不实用向后断言，使用分组的方式，也可以把需要的内容提取出来，比如上例可以改为`print re.findall(r"a(123b)",a)`


## 向前断言 (lookahead assertion)：

有了向后断言的例子，这个应该很好理解了，即多了一个后缀的匹配。

其实，向前向后断言，比如`(?\<=abc)123(?=d)`和abc123d其匹配的区域应该是一致的，区别就是返回的匹配串中是否包含abc和d。

 
**需要注意的一点是：**向前、向后断言，只是修改了限定了原来匹配串的前后缀，但是并没有匹配前后缀，看下面代码就清楚了：

```python
>>> print s
a-b-
>>> print re.match(r"\w(?=-)",s).group()
a
>>> print re.match(r"\w(?=-)\w",s)
None
>>> print re.match(r"\w(?=-)-",s).group()
a-
```

 

## 否定向后断言 (negative lookbehind assertion)：

顾名思义，和向后断言相反，匹配前缀不是`(?\<!…)`中…的字符串。

 

## 条件匹配

用法：`(?(id/name)yes-pattern|no-pattern)`

此处的id/name代表之前匹配的分组号或者分组名（还记得使用?P=可以设置分组名么:) ）。

简单的案例：

```python
>>> print a
abc123efg<456ghi<789>
>>> for i in re.finditer(r"(?<=[a-z])(<)?\d+(?(1)>)",a):
... print i.group()
...
123
<789>
```

上述案例是为了找出字母串中的数字数字串或以位于成对的尖括号中间的数字串，但需要排除破损的尖括号对中的数字串。这里就需要使用到条件匹配了。

另外，实验官方的那个email地址提取的时候，有个坑，看起来好像是条件匹配不生效：

```python
>>> print re.search(r"(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'user@host.com').group()
user@host.com
>>> print re.search(r"(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'<user@host.com>').group()
<user@host.com>
>>> print re.search(r"(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'<user@host.com').group()
user@host.com
```

从上面的输出可以看到，不管尖括号是否成对，可以可以匹配到。

其实不是这样的：

```python
>>> print re.search(r"(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'<user@host.com').groups()
(None, 'user@host.com')
```

把所有匹配的groups打印出来可以看不到，`'\<user@host.com'`的时候，第一个group是None，说明了在匹配的时候，没有认为`(\<)?`匹配到了，所以最后的条件匹配`(?(1)\>)`也就没生效。

要解决这个问题，在正则串的前面加上一个开始符号‘\^’就可以了：

```python
>>> print re.search(r"^(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'<user@host.com')
None
>>> print re.search(r"^(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'<user@host.com>')
<_sre.SRE_Match object at 0x1005e4e00>
>>> print re.search(r"^(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)$",'user@host.com')
<_sre.SRE_Match object at 0x1005e4e00>
```

以上所有用法的解释，都可以参见[官方文档](http://docs.python.org/2/library/re.html)

 

