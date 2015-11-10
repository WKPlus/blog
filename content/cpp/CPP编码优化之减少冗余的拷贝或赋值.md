Title: C++编码优化之减少冗余拷贝或赋值
Date: 2012-07-06 13:31
Category: 性能测试与调优
Slug: cpp-code-tuning-1

开始尝试写一些技术上的blog之后，发现一些好处，写的时候可以把一些零散的知识点梳理清楚，而且有空还可以回顾。

最近做了一些模块的性能优化工作，虽然基本都是一些编码上的优化和少量的设计优化，但是优化方式还是比较多且杂的，因此想写个编码优化的系列，把之前曾经遇到过的一些情况记录下来。

当然，在说到某个具体的优化手段时也有可能补充一些书本上介绍的优化方法。

=========背景介绍结束，正文开始=========

之所以说减少拷贝或赋值，而不是减少临时变量，因为有几个情况，并不是临时变量引入的。但目前看来，减少临时变量的产生确是减少冗余拷贝构造的一大途径。

因此，减少冗余拷贝构造准备先简单从两个方面来叙述：临时变量&&非临时变量

## 临时变量

目前遇到的一些产生临时变量的情况：函数实参、函数返回值、隐式类型转换、多余的拷贝

### 1. 函数实参

这点应该比较容易理解，函数参数，如果是实参传递的话，函数体里的修改并不会影响调用时传入的参数的值。那么函数体里操作的对象肯定是函数调用的过程中产生出来的。

那么这种情况我们该怎么办呢？

如果callee中确实要修改这个对象，但是caller又不想callee的修改影响到原来的值，那么这个临时变量就是必须的了，不需要也没办法避免。

如果callee中根本没有修改这个对象，或者callee中这个参数本身就是const型的，那么将实参传递改为引用传递是个不错的选择（如果是基本类型的函数实参，则没有必要改为引用），可以减少一个临时变量而且不会带来任何损失。

另外，推荐一个静态代码检查工具[cppcheck](http://sourceforge.net/apps/mediawiki/cppcheck/index.php?title=Main_Page)，这个工具可以提示非基本类型的const实参改为引用。

### 2. 函数返回值（返回对象）

函数返回值的情况比较复杂，因为编译器在这方面做了很多优化，编译器优化到何种程度我也没追根究底研究过。

前面有篇文章中就提到了，在没开任何优化选项的时候，gcc也优化了一些简单的返回对象的情况。

先看一段代码：

```cpp
A createA(int a)
{
    A tmp; 
    tmp._a=a;
    return tmp;
}
```

抛开所有优化不谈，函数中createA应该有一个构造操作（tmp对象生成）和一个拷贝构造操作（tmp对象返回时）。

于是有些编译器尝试对函数返回时的拷贝构造进行优化：

```cpp
A createA(int a)
{
    return A(a);
}
```

第一步可以被优化的拷贝构造就是上面的这种情况，即RVO(return value optimization)，这时候只能在函数返回一个未命名变量的时候进行优化。

后来更进一步，可以在函数返回命名变量的时候也进行优化了，这就是NRVO(named return value optimization)。

但是这时候，还有一种情况不能优化的情况是：如果createA函数内部不同的分支返回不同的对象


```cpp
A createA(int a)
{
    if(a%2==0)
    {
        A tmp; 
        tmp._a = 2;
        return tmp;
    }
    else   
    {
        A tmp; 
        tmp._a = 1;
        return tmp;
    }
}
```

比如上面这段代码，我在gcc 3.4.5的情况下测试，发现这种情况是不能优化的。

但是也不排除gcc更高的版本或者某些在这方面做得更优秀的编译器已经可以优化这种情况。

### 3. 隐式类型转换

代码中的一些类型的隐式转换也会产生临时变量，比如：

```cpp
class A
{
public:
    A(int a=0):_a(a)
    {
        cout<<"constructor"<<endl;
    }
    A(const A &a)
    {
        cout<<"copy constructor"<<endl;
        this->_a = a._a;
    }
    A& operator=(const A&a)
    {
        cout<<"operator="<<endl;
        this->_a = a._a;
        return *this;
    }
    int _a;
};
int main()
{
    A a1;
    a1 = 3;
    return 0;
}
```

在`a1 = 3`执行时会首先调用`A(3)`产生一个临时对象，然后调用`operator=(const A& a)`

这种情况下，我们只要实现一个`A::operator=(int)`函数就可以避免这个临时对象的产生了。

当然，这只是一个最简单的例子，不过思路是差不多的。

### 4. 多余的拷贝

这种情况应该比较少，也比较简单，个人感觉，这种情况主要是疏忽引起的。

是这样一种情况： 有个线程级的结构体`thread_data_t *pthread_data`，里面包含请求包的各种数据，在几处使用的使用使用了`const A a = pthread_data->getA()`。

`getA()`的实现简单来说是返回了`thread_data_t`内部的A成员。

因为在一次请求的处理过程中`thread_data_t`内部的A的成员不会改变，调用者用`const A a`来接收这个对象就表明调用者也不会改变返回的A成员。

因此，其实完全可以让`getA()`返回A成员的引用，调用者同样用引用来接收：`const A & a = pthread_data->getA()`。

这样就完全就避免了一次多余的拷贝。

## 非临时变量

遇到的一些非临时变量情况有：`stl vector`的增长引起拷贝构造、`vector`的赋值、`std::sort`操作

### 1. vector的增长

先简单介绍一下vector的增长机制：每次push\_back时，如果发现原来vector的空间用完，会把vector调整到原来的2倍（sgi的实现，visual studio的实现好像是1.5倍）。因为vector空间是连续存储的，这里就有一个问题，如果原来vector地址后面空余的空间没有被使用，那么vector继续把后面的地址申请来就可以扩展其空间了。但是如果后面的空间不够了呢？那就要重新申请一个2\*current\_size大小的空间，然后把vector当前，也就是current\_size的内容拷贝到刚申请的那块空间中去，**这时就引起了对象的拷贝操作了**。

假设vector初始大小是0，我们通过push\_back加入了10个对象，以sgi实现的两倍增长为例，再假设每次调整vector空间的时候都需要调整地址，一共引入了多少次无用的拷贝？

因为vector空间是1-\>2-\>4-\>8-\>16增长的，拷贝的次数一共是四次，每次拷贝对象分别是1、2、4、8个。所以答案是1+2+4+8=15。

很容易看出规律，拷贝对象的个数等于最终vector空间大小减一。

那么如果vector大小最终会涨到1000，1W呢？数据就很可观了。

我接触过好几个服务，最终vector可能会增长到10W左右的。如果vector要放入10W个元素，那么就会开辟131072的空间，也就是说最多会引入13W次的对象拷贝，而这个拷贝操作是无效的、是可以避免的。

其实要避免vector增长引入的拷贝也很简单，在push\_back之前先调用reserve申请一个估算的最大空间。

比如我们之前优化的一些服务，预期vector最大可能会增长到10W，那么直接调用`v.reserve(100000)`就可以了。

当然，这也许会引起一些内存使用的浪费，这就需要使用时注意权衡了。

但如果你的服务是一直运行的，而且这个vector对象也是常驻内存的，个人觉得完全可以reserve一个最大的空间。因为vector空间增长之后，就算调用clear清除所有元素，内存也是不会释放的。除非使用和空vector交换的方式强制释放它的内存。

### 2. vector的赋值

遇到过这样一种情况，在一个函数接受一个`vector &`作为输入，经过一系列处理得到一个临时的vector，并在函数返回前将这个临时的vector赋值给作为参数的`vector &`作为返回值。简化一下代码如下：

```cpp
void cal_result(vector<int> &input_ret)
{
    vector<int> tmp;
    for(...)
    {
        ... // input_ret will be used   
        //fill tmp
    }
    input_ret = tmp;
}
```

这里，我们可以注意到函数返回后tmp对象也就消失了，不会被继续使用，所以如果可以的话，我们根本不需要返回tmp的拷贝，直接返回tmp占用的空间就可以了。

那么怎么可以直接返回tmp而不引起拷贝呢？是不是可以这样想，我们把tmp这个vector指向的地址赋值给input\_ret，把tmp指向的空间和大小设置为0就可以了？

那么我们完全可以使用vector的swap操作。它只是将两个vector指向空间等等信息交换了一下，而不会引起元素的拷贝，它的操作是常数级的，和交互对象中元素数目无关。

因此将上述代码改为：

```
void cal_result(vector<int> &input_ret)
{
    vector<int> tmp;
    for(...)
    {
        ... // input_ret will be used   
        //fill tmp
    }
    input_ret.swap(tmp);
}
```

可以减少tmp元素的拷贝操作，大大提高了该函数的处理效率。（提高多少，要看tmp中所有元素拷贝的代价多大）

### 3. std::sort操作

在为一个模块做性能优化的时候，发现一个vector的sort的操作十分消耗性能，占了整个模块消耗CPU 10%以上。

使用[gperftools](http://code.google.com/p/gperftools/)的cpu profiler分析了一下数据，发现sort操作调用了元素的拷贝构造和赋值函数，这才是消耗性能的原因。

进一步分析，vector中的元素对象特别庞大，对象中又嵌套了其他对象且嵌套了好几层，因此函数的拷贝和赋值的操作代价会比较大。

而std::sort采用的是[内省排序](http://zh.wikipedia.org/wiki/Introsort)+插入排序的方式（sgi的实现），不可避免地会引入对象的交换和移动。（其实不管怎么排序都避免不了交换和移动的）

因此，要优化这句`std::sort`操作，还需要减少对象交换或者提高交换的效率上入手。

#### 3.1. 减少对象的交换

我们采用的减少对象交换的方式是：先使用index的方式进行排序，排序好了之后，把原来的vector中的对象按照index排序的结果最终做一次拷贝，拷贝到这个对象排序后应该在的位置。

或者直接vector里面不要放大对象，如果遇到大对象，可以考虑在vector放`shared_ptr`

#### 3.2. 提高交换的效率

如果对象的实现是如下这样的：

```cpp
class A
{
public:
    A(const char* src)
    {
        _len = strlen(src);
        _content = new char[_len];
        memcpy(_content,src,_len);
    }
    A(const A &a)
    {
        *this = a;
    }
    A& operator=(const A&a)
    {
        _len = a._len;
        _content = new char[_len];
        memcpy(_content,src,_len);
    }
private:
    char *_content;
    int _len;
};
```

这里为了保持代码简短，省略了部分实现且没考虑一些安全性的校验。

那么在对象交换的时候，其实是没有必要调用拷贝构造函数和赋值函数的（std::swap的默认实现），直接交换两个对象的\_content和 \_len值就好了。如果调用拷贝构造函数和赋值函数的话，不可避免还要引入new、memcpy、strlen、delete等等操作。

这种情况下，我们完全可以针对A的实现，重载全局的swap操作。这样sort的过程中就可以调用我们自己实现的高效的swap了。

如下代码可以重载我们A函数的swap实现：

```cpp
namespace std
{
template<>
void swap<A>(A &a1,A& a2)
{
    cout<<"swap A"<<endl;
    int tmp = a1._a;
    a1._a = a2._a;
    a2._a = tmp;
}
}
```

因为调用堆精度问题和编译优化的问题，有时候也可能分析不到sort是因为调用了元素对象的拷贝构造和赋值函数所以才效率比较低。所以发现sort消耗性能的时候，可以看看是否是因为sort对象过大造成的，积累一个common sense吧。
