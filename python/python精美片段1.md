Title: python精美片段之找出list中符合条件的第一个元素
Date: 2014-09-22 16:02
Category: python
Slug: python-pearl-1

### 第一种写法

```python
e = None
for i in l:
    if condition(i):
        e = i
        break
```

缺点：不美观


### 第二种写法

```python
e = [i for i in l if condition(i)][0]
e = filter(condition, l)[0]
```

缺点：没有做list非空判断可能异常；效率不高，只需要一个元素，但是遍历了原始list所有元素


### 第三种写法

```python
e = next((i for i in l if condition(i)), None)
e = next(itertools.ifilter(conditon, l), None)
```

缺点：太优美:-)
