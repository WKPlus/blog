Title: N NP问题理解
Date: 2013-11-11 18:24
Category: 杂项
Slug: n-np


###决定性问题
[decision problem](http://en.wikipedia.org/wiki/Decision_problem)，是指那些可以用是或者否可以回答的问题，比如：

> x可以被y整除吗？
> x是质数吗？
> 从A点到B点有长度小于10的路径吗？

与决定性问题相对应的是功能性问题[function problem](http://en.wikipedia.org/wiki/Function_problem)，这类问题的答案不能是简单的YES or NO，比如：

> x除以y的商和余数是多少？
> x的质因子有哪些？
> 从A点到B点长度小于10的路径有哪些？


因为已经存在标准的方法可以将功能性问题转换为决定性问题而且不会显著改变其计算的复杂度，因此，计算性的理论性研究集中在决定性问题上面。

[Wiki](http://en.wikipedia.org/wiki/Decision_problem) 原文如下：

> There are standard techniques for transforming function and optimization
problems into decision problems, and vice versa, that do not significantly
change the computational difficulty of these problems. For this reason, research
in computability theory and complexity theory have typically focused on decision
problems.


[P和NP](http://en.wikipedia.org/wiki/Time_complexity)的定义：

> P: The complexity class of decision problems that can be solved on a deterministic Turing machine in polynomial time.
> NP: The complexity class of decision problems that can be solved on a non-deterministic Turing machine in polynomial time

###P
P类问题是指，在多项式时间内可以
