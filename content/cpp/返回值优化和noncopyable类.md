Title: 返回值优化和noncopyable class
Date: 2012-06-21 18:17
Category: 编译器
Slug: rvo-noncopyable

今天上班，遇到件比较有意思的事情。有同事叫我看一段代码，这段代码在gcc上可以编译通过，但是用bullseye cover编译用于统计覆盖率的时候，链接阶段报错了。

我简化一下这段代码如下：

```cpp
class Integer
{
public:
    Integer(int x=0):_x(x){}
    Integer operator+(const Integer& rhs)
    {
        Integer tmp;
        tmp._x += rhs._x;
        return tmp;
    }
    ~Integer(){}
private:
    Integer(const Integer&);
    int _x;
};
```

我看了一下bullseye cover链接阶段报的错误，其实就是说找不到`"Integer(const Integer&)"`函数的定义，而这个函数在`"Integer operator+(const Integer& rhs)"`中调用了。

我一看，bullseye cover的行为是对的，operator+中函数返回的是对象，而非引用，理应有次拷贝构造的操作。

那为什么gcc可以链接通过呢？第一反应就是返回值优化，把这次拷贝构造的操作优化掉了。

写了段代码测试一下（代码我就不贴，就是定义个拷贝构造函数，打印点提示，然后调用一下operator+），果然是返回值优化的原因。而且**竟然在优化选项-O0的就开启返回值优化了，这点倒有点让我意外**。

本来我还认为，NonCopyable class的拷贝构造函数只要声明为private就行了，至于定义不定义倒无所谓，反正依赖的是访问权限的控制。

这次经历之后才意识到，**将NonCopyable class的拷贝构造函数定义为空是很危险的一件事**。因为它也可能被成员函数来调用，这个时候访问权限也无能为力了，只能靠函数未定义来提示了。

至于对错，我觉得两个编译器的行为都是可接受的，要修改的是这种代码的编写方式：既是Noncopy class，成员函数又要返回对象实例。

不过gcc确实做得优秀，不仅仅优化消除了一些函数调用，还因为消除了一些不必要的函数调用让摇摇欲坠的代码编译通过了。

本来问题到这里也就结束了，我觉得在gcc中还会有个比较好玩的现象：

> 如果调用NonCopyable class拷贝构造是个非成员函数，那么编译阶段会提示访问权限的错误。但是因为编译优化的原因，这个函数实际又不会被调用到，似乎有点
> “冤”。如果绕过权限访问控制，比如把那个非成员函数声明为NonCopyable class的友元函数，程序就可以正常工作了。

如下代码：

```cpp
class Integer
{
public:
    friend Integer add(const Integer&,const Integer&);
    Integer(int x=0):_x(x){}
    ~Integer(){}
    int get()const{return _x;}
    void set(int x){_x=x;}
    Integer& operator=(const Integer& rhs)
    {
        this->_x = rhs._x;
        return *this;
    }
private:
    Integer(const Integer&);
    int _x;
};

Integer add(const Integer& lhs,const Integer& rhs)
{
    Integer tmp;
    tmp.set(lhs.get()+rhs.get());
    return tmp;
}
```

上面的代码，如果注释掉第4行，编译阶段就会有`'Integer::Integer(const Integer&)' is private`这样的错误。如果反注释第4行，编译、链接都是通过的。

其实上面这段代码，还没写全面，如果有地方调用了add函数，在那里也会报一个`'Integer::Integer(const Integer&)' is private`这样的错误，需要把调用处的代码也绕过权限控制。

我觉得如果能把代码优化操作放到检查代码访问权限操作之前，就可以避免这个问题了。不过对编译器底层实现不太了解，不知道这个调整是否可行。

**或者我们在写NonCopyable class的时候，不是声明私有的拷贝构造函数，而是声明公有的拷贝构造函数，但是不定义它。**

不知道这样会有什么弊端，除了错误提示会晚一点。但是这样有个好处是，前面说的“冤”的情况可以避免。

