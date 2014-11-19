Title: maven dependency:tree中反斜杠的含义
Date: 2013-11-11 18:24
Category: 杂项

一个mvn dependency:tree命令执行的输出如下：

```bash
[INFO] +- junit:junit:jar:3.8.1:test (scope not updated to compile)  
[INFO] +- com.dianping:easyUtil:jar:0.0.2-SNAPSHOT:compile  
[INFO] | +- org.slf4j:slf4j-api:jar:1.5.8:compile  
[INFO] | +- org.slf4j:slf4j-log4j12:jar:1.5.8:compile  
[INFO] | | \- log4j:log4j:jar:1.2.14:compile  
[INFO] | +- commons-collections:commons-collections:jar:3.2.1:compile  
[INFO] | +- commons-beanutils:commons-beanutils:jar:1.8.0:compile  
[INFO] | | \- commons-logging:commons-logging:jar:1.1.1:compile
```

这是一个树形结构，展示了各个包之间的依赖关系，不过令我比较好奇的是，为什么有些包前面是`\-`。

为了搞清楚这个问题，google了半天也没找到正确答案，差点抑郁了:)

后来在看另外一个文章的时候，有人提到最好用`\-`来表示同一层依赖的最后一个节点，一下子意识到上面的mvn命令输出中的`\-`应该就是这个意思。

何为同一层依赖的最后一个节点？打个可能不太恰当的比喻：他是他爸最小的儿子（如果把依赖树看成家族树，依赖树的根节点看作“老祖宗”的话）。另外，即使他有儿子了，他的标示符还是`\-`。

