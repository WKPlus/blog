Title: 如何用C/C++扩展Python的功能
Date: 2013-02-18 18:58
Category: python
Slug: python-c-extension

用c/c++扩展Python功能，说简单点就是python中调用c/c++代码，比较基础的有两种方式：

1. 使用Python的C语言接口，即通过PyObject，[这篇文章](http://www.ibm.com/developerworks/cn/linux/l-pythc/)介绍比较详细。
2. 使用ctypes直接导入c/c++动态库，如何使用点[这里](https://code.google.com/p/program-think/wiki/OpensourcePython#2.1_%E6%95%B4%E5%90%88_C_/_C++_%E8%AF%AD%E8%A8%80)

第一种方式编写c/c++接口稍微麻烦一点，但是在python代码中使用该接口会十分方便，如同使用内置模块一般；第二种方式则可以直接使用原有的c/c++动态库，即使没有源文件也可以使用。

两种使用方式在其他方面，比如效率，是否还有区别，目前还没有研究过。

