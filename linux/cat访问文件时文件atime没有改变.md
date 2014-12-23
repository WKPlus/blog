Title: cat文件时文件访问时间没有改变
Date: 2013-12-24 10:15
Category: Linux
Slug: linux-file-timestamp

Linux文件系统中，每个文件有三个时间属性：atime(access time)、mtime(modify time)、ctime(change time)

其中atime比较容易理解，即文件的最后访问时间，mtime和ctime有点容易混淆。其中mtime是文件内容的最后修改时间，而ctime是文件inode、属性的最后修改时间。

如果有一个文件123：

1. `echo "test" >> 123`会修改文件的mtime和ctime，mtime修改是因为文件内容多了一行"test"，ctime修改是因为文件大小（属性）改变了。
2. `chmod +x 123`则会修改文件的ctime，因为文件属性改变了，但是内容没有变
3. 如果`cat 123`，则会修改文件的atime

操作步骤如下：

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/12/NewImage.png "NewImage.png")


但是，最近发现一个情况：cat一个文件的时候文件的atime有时改变又是不改变。比如上图中最后一次cat并没有使得文件的atime发生改变。

细细研究了一下，原因如下：

如果每次打开文件的时候，都更新文件的atime，这对系统来说，I/O的负担比较大，影响了系统的性能。

因此文件系统增加了一个选项，可以用来控制是否每次访问文件都修改atime。使用命令man mount可以查看：

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/12/NewImage1.png "NewImage.png")

其中relatime的意思是：并不是每次访问文件都会更新最后访问时间，除非文件上一次的访问时间比文件的mtime或ctime要早。

 
那么如何查看自己的系统使用的是哪一个选项呢？可以使用`cat /proc/mounts`查看（因为我的测试目录是挂载在sda2盘的，为了减少输出结果，使用sda2作为关键词过滤了一下）

由下图可以看到，测试目录所在的文件系统使用了relatime的选项，因此不会每次访问都更新访问时间。

![NewImage](http://www.708luo.com/blog/wp-content/uploads/2013/12/NewImage2.png "NewImage.png")

