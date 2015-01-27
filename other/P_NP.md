Title: P NP问题理解
Date: 2014-12-23 18:24
Category: 杂项
Slug: p-np


##P和NP的定义
要理解P和NP问题，让我们首先来看看[P和NP](http://en.wikipedia.org/wiki/Time_complexity)的定义：

> P: The complexity class of decision problems that can be solved on a deterministic Turing machine in polynomial time.
> 
> NP: The complexity class of decision problems that can be solved on a non-deterministic Turing machine in polynomial time

翻译一下就是：
> P类问题是指确定型图灵机可以在多项式时间内解决的问题
> 
> NP类问题是指非确定型图灵机可以在多项式时间内解决的问题
> 

关键词：确定型/非确定型图灵机、多项式时间，要理解P和NP问题，还得先搞清楚这两个关键词的含义。


##多项式时间
要理解多项式时间，把**多项式时间**和**指数时间**一起看会比较容易理解

> **[多项式时间](http://zh.wikipedia.org/wiki/%E5%A4%9A%E9%A0%85%E5%BC%8F%E6%99%82%E9%96%93)**： m(n) = O(n^k)，k为常数

> **指数时间**： m(n) = O(k^n)，k为大于1的常数

*之前一直理解错误，认为O(n^2)这种属于指数时间。*


##确定型和非确定型图灵机
图灵机是一个抽象模型，由以下几个组成部分：

1. 一条无限长的纸带
2. 一个读写头，可以在纸带上左右移动并读写内容
3. 一个状态寄存器，用来存储图灵机当前的状态
4. 一套控制规则，根据图灵机当前状态和纸带当前内容来确定下一步操作

简直就是一个终极简化版的计算机，或者可以认为是一个状态机+input/output。这是确定型状态机，一般我们提到图灵机就是指这个。

而非确定型图灵机和确定型图灵机只有一点差别，就是：控制规则这里，根据当前状态和纸带内容确定下一步操作的时候，都可能有N个分支，N个分支中只有一个可以得到最终结果或者告知输入有错。

而对于确定型图灵机，特定的状态和纸带内容，下一步操作只能有一个。


##理解P和NP
看完P和NP、多项式时间和指数时间的定义，了解了什么是确定型和非确定型图灵机，现在对理解P和NP还是没有太直观的感觉。

那么再看看NP的另外一个定义：

>  the class NP consists of all those decision problems whose positive solutions can be verified in polynomial time given the right information, or equivalently, whose solution can be found in polynomial time on a non-deterministic machine.

翻译一下就是：

> NP类问题是指 解的正确性可以在多项式时间内（在确定型图灵机上）被验证的决定性问题，或者说，在非确定型图灵机上可以在多项式时间内求解的问题


这里涉及到一个新概念：决定性问题。那让我们先来了解一下什么是决定性问题。

[决定性问题](http://en.wikipedia.org/wiki/Decision_problem)是指那些可以用是或者否可以回答的问题，比如：

> x可以被y整除吗？
> 
> x是质数吗？
> 
> 从A点到B点有长度小于10的路径吗？

与决定性问题相对应的是功能性问题[function problem](http://en.wikipedia.org/wiki/Function_problem)，这类问题的答案不能是简单的YES or NO，比如：

> x除以y的商和余数是多少？
> 
> x的质因子有哪些？
> 
> 从A点到B点最短的路径是什么？


因为已经存在标准的方法可以将功能性问题和决定性问题相互转化而且不会显著改变其计算的复杂度，因此，计算性的理论性研究集中在决定性问题上面。

[Wiki](http://en.wikipedia.org/wiki/Decision_problem) 原文如下：

> There are standard techniques for transforming function and optimization
problems into decision problems, and vice versa, that do not significantly
change the computational difficulty of these problems. For this reason, research
in computability theory and complexity theory have typically focused on decision
problems.

这一句很重要：

> 已经存在标准的方法可以将功能性问题和决定性问题相互转化而且不会显著改变其计算的复杂度

因为后面在举例说明NP问题的时候，我们需要将问题先转化为决定性问题。

比如背包问题

> 有N件物品和一个容量为W的背包。第i件物品的重量是w[i]，价值是v[i]。求解将哪些物品装入背包可使这些物品的费用总和不超过背包容量，且价值总和最大。

改为决定性问题可以是：

> 有N件物品和一个容量为W的背包。第i件物品的费用是w[i]，价值是v[i]。在总容量不超过W的情况下，总价值能否达到V？

对于改为决定性问题后的背包问题我们要验证一个解是不是正确的，很简单，只要把一个解的总容量和价值算出来，看看是否满足总容量小于等于W且总价值大于等于V。O(n)时间（多项式时间）内可以验证，所以它属于NP类问题（解的正确性在多项式时间内被验证）。

但是如果我们要计算这个解呢？如果有个算法可以在多项式时间内计算出**在总容量不超过V的情况下，总价值能否达到V？**这个问题的解，那么这就是P类问题了。这个算法目前还没找到，找到就不得了，因为背包问题还是个NPC问题，如果这个问题被证明为P类问题，那么就可以证明NP=P了。至于什么是NPC问题，下次再仔细掰扯掰扯~


