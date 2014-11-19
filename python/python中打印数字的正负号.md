Title: python 打印数字的正负号
Date: 2013-11-11 18:10
Category: python

python中使用`print "%d"%i`时，默认是不显示"+"号的：

```python
>>> print "%d"%123  
123  
>>> print "%d"%-123  
-123
```

有没有方法在`print "%d"%123`显示"+123"呢？
很幸运，是有的，使用`print "%+-d"%123`或`print "%+d"%123`即可。 
