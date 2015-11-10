Title: Jmeter学习笔记
Date: 2013-10-24 17:22
Category: 杂项
Slug: jmeter-learning-1

最近在学习使用Jmeter完成web的压力测试。

Jmeter是Apache的一款开源的压力测试工具，纯java编写，可用于测试web、SOAP、java service等等接口的压力测试。

具体介绍见[官网](http://jmeter.apache.org/)


下面介绍一个简单常用的web功能的压力测试步骤。

测试需求：登录web，然后进行一些操作，最后退出。需要模拟一些并发，每个并发使用不同的用户登录。很常见的需求是吧？

好，下面是测试准备步骤：

1. 录制登录、操作、退出这一系列操作的脚本（当然也可以直接在Jmeter中添加一个个操作，不过录制的方式比较快）
2. 配置cookie管理器，否则多个请求之间不能共享cookie，登录之后的其他操作还会出于非登录状态
3. 修改并发，并且配置每个并发使用不同用户
 

下面具体介绍上面每个步骤需要的操作：

### 录制脚本

看到有很多人用badboy来录制脚本，可以导入jmeter，不过我是直接使用jmeter自带的http代理录制脚本的，也蛮好用。

1. jmeter中新建一个线程组（测试计划上右击）

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn.png)

2. 工作台上右击，添加一个HTTP代理服务器，配置Test plan content的目标控制器为“测试计划 \> 线程组”，分组为“每个组放入一个新的控制器”（其实选不分组也行）

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn1.png)

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn2.png)

3. 启动代理服务器

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn3.png)
4.  在浏览器中配置使用该代理，然后你通过这个代理的所有操作就被记录了，可劲造吧。。。
5. 停止代理，一份脚本就录制好了。到此，第一步搞定了。


### 配置cookie管理器

这个很简单，右击线程组添加一个HTTP Cookie管理器就好了。操作很简单，但是没这步的话，登录之后的操作全部无效
![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn4.png)

### 修改并发，配置多用户

1. 添加一个" CSV Data Set Config"

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn5.png)

2. 重点是两个区域：`Filename`和`Variable Names`，Filename告诉jmeter从哪个文件读入配置文件，Variable Name告诉jmeter把读取的数据赋给哪些变量（后面登录的时候需要用到这两个变量）。其他的，初级使用不用管。

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn6.png)

3. 找到刚才录制脚本中，登录的部分修改用户名、密码为第二步中设置的变量，注意加上\$，大括号有没有无所谓，变量名字随便取，只要2和3步中的设置一致即可。

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn7.png)

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn8.png)

4. 然后设置并发，选择线程组，配置线程数即可。（csv文件中的记录，会被依次赋值给不同的线程，如果线程数大于csv的记录，则从头循环使用）

![image](http://7xo7ae.com1.z0.glb.clouddn.com/jmeter_learn9.png)

5. 第4步还可以配置循环次数和Ramp-Up Period，循环次数应该很容易理解。Ramp-Up Period稍微解释下：这用来配置一个参数，告诉jmeter在多长时间内全部启动前面配置那么多线程。如果配置了100线程，然后配置了Ramp-Up为50秒，那么jmeter大概会每秒启动2个线程。

6. 到此，所有准备工作完毕。

 

准备工作完成之后，可以直接选择线程组开始执行了。

另外，也可以把这个测试脚本保存为一个.jmx文件，然后用命令行的方式去运行jmeter，命令如下：`./bin/jmeter.sh -n -t xxx.jmx -l result.jtl`

这会把结果文件输出到一个jtl文件中，该文件有两张格式，csv和xml，依赖于bin/jmeter.properties中的jmeter.save.saveservice.output\_format这个配置。

注意，命令行模式中，.jmx中配置的输出文件格式并不生效，而是依赖刚才提到的配置项。这里，曾经踩了个坑。
 
其他方面，比如jtl文件中各个指标含义，UI模式中如何及何时需要添加一个监听器，暂且不提。
