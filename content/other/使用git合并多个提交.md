Title: 使用git合并多个提交
Date: 2012-07-30 21:07
Category: 杂项
Slug: git-combine-commmit

假设要合并最后的2个提交，可以按如下命令进行：

1. git rebase –i HEAD\~2  

> 运行完该命令，会出现如下所示内容：
> ![image](http://7xo7ae.com1.z0.glb.clouddn.com/git_merge_commit1.png)

2. 将第二个pick修改为squash或者s，然后输入":wq"退出。
3. 这时git会自动第二个提交合并到第一个中去。并提示输入新的message（就是我们常说的comments），如下：  
![image](http://7xo7ae.com1.z0.glb.clouddn.com/git_merge_commit2.png)

4. 编辑输入新的message，然后输入":wq"退出
5. 此时本地的（HEAD中）最后两次提交已经被合并为一个。git log可以查看。
6. 如果需要提交到远端，运行git push --force origin master即可。

