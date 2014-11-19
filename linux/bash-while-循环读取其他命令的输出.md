Title: bash while循环读取其他命令的输出
Date: 2014-10-09 17:37
Category: Linux

bash while循环读取其他命令的输出有三种方式：`pipe` 、`here-string`以及`process substitution`。

下面通过三段代码来介绍这三种用法以及其中的坑：假设当前目录下有3个.txt文件，通过看看下面三段代码的输出来理解pipe, here-string和process substitution的不同。

## pipe
----

```bash
var=0
find . -type f -name "*.txt" | while read i
do 
     ((var++)) 
done
echo $var
```

输出：0  

解释：管道左右的命令会在单独的进程中运行，因此while循环是在一个subshell中执行的，没有改变原shell中的var变量。


## here string
----

```bash
var=0
while read i
do 
    ((var++)) 
done <<< "$(find . -type f -name "*.txt")"
echo $var
```

输出：3  
解释：这里不解释here strings是什么了，不了解的可以看[[这里](http://linux.die.net/abs-guide/x15683.html)]。使用here string不会像管道那样在新shell种执行while循环，因此var原shell中的var变量会被改变。

 

## process substitution
----

```bash
var=0
while read i
do 
    ((var++)) 
done < <(find . -type f -name "*.txt")
echo $var
```

输出：3  
解释：  process substitution `<(cmd)`相当于创建了临时文件，将cmd的输出重定向到临时文件中。然后while循环从此临时文件中读取输入。  

但是不是所有的系统或者shell都支持process substitution，哪些情况不支持可以看[[这里](http://wiki.bash-hackers.org/syntax/expansion/proc_subst)]的“Bugs and Portability Considerations”部分。

