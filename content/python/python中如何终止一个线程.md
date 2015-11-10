Title: python中如何中止一个线程
Date: 2012-03-29 21:18
Category: python
Slug: python-thread-interrupt

今天遇到一个需求，希望可以实现一个带时间上限的线程池的功能，需要在到达时间上限的时候，主动kill掉那些slave线程。

找了很久，终于发现一个基本满足需求的实现。

记录在这里，以备不时之需。

```python
class KillableThread(threading.Thread):
    """A subclass of threading.Thread, with a kill() method."""
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """ Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
```

不过这个实现也有一个弊端：如果需要kill的线程正在sleep或者正阻塞在更底层的操作上，是没有办法立即kill掉的。

简单来说，它kill的原理是设置一个flag位，然后线程在执行下一句python语句检测到这个位被设置了之后，就会自行退出，以达到kill的目的。

另外还有一种更容易理解的flag置位的实现方式：

```python
class KillableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.stop = False

        def run(self):
            while not self.stop:
                somefunction()
```

这种方式相比第一种而言，又有一点不足：kill生效的时限，最大等于somefunction执行一遍所花的时间。
而第一种方式，在下一句python语句执行时就会生效。

不过可以料想，第一种实现方式，整体的执行效率会慢一点。因为每次执行一句python语句，都会有一个判断的过程。

