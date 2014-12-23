Title: Linux 进程调度策略与top命令的PR NI值
Date: 2013-06-18 18:25
Category: 性能测试与调优
Slug: linux-top-pr-ni

Linux进程有`SCHED_OTHER/SCHED_BATCH/SCHED_IDLE/SHCED_FIFO/SCHED_RR`五种调度策略，前面三种是常规调度策略，后面两种是实时调度策略。具体介绍点击[这里](http://linux.die.net/man/2/sched_setscheduler)。

之前一直不能理解的是：RR是分时间片来调度的，是分时调度常用策略，这里为啥还属于实时调度策略。  

后来了解到：RR是分时调度常用的策略，也就是说`SCHED_OTHER`的底层实现也可能是RR。`SCHED_RR`之所以属于实时调度，是其及时性更高，也就是RR的时间片要比分时的时间片小得多。

Linux的线程也是由进程实现的，只不过是一种可以共享资源的进程（说明[在此](http://www.linuxquestions.org/linux/articles/Technical/Linux_Kernel_Thread)）。
因此Linux上，线程调度策略应该也不外乎这些。Linux平台上，POSIX线程支持：`SCHED_OTHER/SCHED_FIFO/SCHED_RR`这三种调度策略。

`SCHED_RR和SCHED_FIFO`调度的进程属于实时进程，`SCHED_OTHER`调度的进程属于非实时进程。Linux中大部分进程都是分时进程，实时进程是优先于非实时进程调度的。可以使用top查看，如果PR的值为RT，则为实时进程。

### PR和NI的含义

PR 进程的优先级。在Linux 2.6.23之前的版本中PR是一个动态值，在运行的过程中可能出现变化。大体策略是：如果一个进程sleep了比较多的时间，PR值会降低（即优先级提高）；如果一个进程占用了大量的CPU时间，PR值会升高（即优先级降低）。在2.6.23版本之后，由于引进了CFS调度策略，不再简单根据一个进程sleep的时间动态调整其优先级了，PR值就固定为NI+20。CFS期望的目标是每个进程均衡地占用CPU，PR作为权重因子。

NI nice值 可用来调整进程的优先级，默认为0。如上所述，PR=NI+20，且PR越小优先级越高，因此nice值越小进程优先级越高。运行命令的时候可用`nice –n xx cmd`来调整cmd任务的nice值，xx的范围是-20\~19之间。

以上内容参考了如下文章：

<http://www.linux.com/learn/tutorials/42048-uncover-the-meaning-of-tops-statistics>
<http://blog.csdn.net/loyal_baby/article/details/4202083>
<http://www.gnu.org/software/libc/manual/html_node/Realtime-Scheduling.html>

