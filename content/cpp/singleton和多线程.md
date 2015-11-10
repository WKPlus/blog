Title: Singleton和多线程
Date: 2013-02-27 20:38
Category: 杂项

最简单的Singleton代码如下：

```cpp
class Singleton
{
public:
    Singleton & getInstance()
    {
        static Singleton _s;
        return _s;
    }
private:
    Singleton(){}
};
```

或者

```cpp
class Singleton
{
public:
    static Singleton * getInstance()
    {
        if(_s == NULL)
            _s = new Singleton();
        return _s;
    }
private:
    Singleton(){}
    static Singleton * _s;
};
Singleton * Singleton::_s=NULL;
```

 

如果getInstance会被多线程执行呢？第二种方式中，很明显if判断处是个race condition。那么第一种方式会不会有问题呢？可以想象，static变量只初始化一次肯定也是通过某个条件判断实现的。就要看编译器实现这个判断的时候有没有加锁了。很可惜，没有从编译器的文档中找到该说明，不过从msdn博客看到[一篇文章](http://blogs.msdn.com/b/oldnewthing/archive/2004/03/08/85901.aspx)说明了静态变量初始化在多线程情况下也是存在race condition。

网上也有人说，在C++11标准中已经规定本地的静态变量是多线程安全的，笔者未确认，而且目前来说也不可能所有编译器都支持了该规则。

那么既然上述的两种实现方式都不是多线程安全的，那么如何实现一个多线程安全的Singleton呢？

最简单的实现方式，如下：

```cpp
class Singleton
{
public:
    static Singleton * getInstance()
    {
        pthread_mutex_lock(&_mutex);
        if(_s == NULL)
            _s = new Singleton();
        pthread_mutex_unlock(&_mutex);
        return _s;
    }
private:
    Singleton(){}
    static Singleton * _s;
    static pthread_mutex_t _mutex;
};
Singleton * Singleton::_s=NULL;
pthread_mutex_t Singleton::_mutex;
pthread_mutex_init(_mutex);
```

不过这种实现方式有个缺点，每次调用getInstance的时候都需要加锁，其实只有当\_s==NULL才需要加锁，因此有个改进版本实现如下：

```cpp
class Singleton
{
public:
    static Singleton * getInstance()
    {
        if(_s == NULL)
        {
            pthread_mutex_lock(&_mutex);
            if (_s == NULL)
                _s = new Singleton();
            pthread_mutex_unlock(&_mutex);
        }       
        return _s;
    }
private:
    Singleton(){}
    static Singleton * _s;
    static pthread_mutex_t _mutex; 
};
Singleton * Singleton::_s=NULL;
pthread_mutex_t Singleton::_mutex;
pthread_mutex_init(_mutex);
```

 

另外，最近看到boost代码中singleton的实现比较巧妙，是不需要加锁的，它建立在一个前提上“进入main函数之前，程序是单线程的”，简化一下实现如下：

```cpp
class Singleton
{
public:
    static Singleton _s;
    static Singleton & getInstance()
    {
        return _s;
    }
private:
    Singleton(){}
};
Singleton Singleton::_s;
```

这种实现方式和最原始的实现的区别就是\_s这个静态变量的位置，原始的实现中\_s是函数本地变量，它在函数调用的时候被初始化，可能被多线程执行；而该版本的\_s是类静态变量，是在程序启动的时候初始化的，在main函数之前，是单线程执行的。

