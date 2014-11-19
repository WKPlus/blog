Title: google cpu profiler二进制结果读取
Date: 2012-05-28 21:12
Category: 杂项

最近一段时间在google cpu profiler做性能热点采样。

用过的人都知道，cpu profiler产出的原始结果是二进制存储的。一般是得到这个结果再使用pprof工具去转化为人可读的文本形式的结果或者图片形式的结果。

但是最近有一些需求：

1.  对两个版本的profiler结果做比较
2.  根据历史数据，对单次profiler结果做一些分析，提示一些可以优化的点

要实现这两个功能，如果是基于pprof转化过的数据进行处理，总会有一些获取不到的信息。所以，最好是基于profiler的原始数据来完成上述的功能。

因为profiler的数据是二进制形式的，所以第一步先来做数据读取的操作。

google了一把，找到了一个profiler[数据格式说明](http://google-perftools.googlecode.com/svn/trunk/doc/cpuprofile-fileformat.html)

有了这个说明，读取这个数据就方便了，写了个python实现，如下：

```python
g_offset = 0
def Print(msg):
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), " %s"%msg
def unpack_buff(fmt,buff):
    global g_offset
    last = g_offset+struct.calcsize(fmt)
    tp = struct.unpack(fmt,buff[g_offset:last])
    g_offset = last
    return tp
     
def unpack_profile_header(buff):
    Print("Unpack profile data header begin...")
    tp = unpack_buff("<5Q",buff)
    Print("Unpack profile data header succeed!")
    return tp
     
def unpack_records(buff):
    Print("Unpack sample records begin...")
    records = []
    while True:
        tp = unpack_buff("<2Q",buff)
        deep = tp[1]
        fmt = "<%sQ" % deep
        address_tp = unpack_buff(fmt,buff)
        if address_tp[0] == 0:
            break
        x_address_tp = [ "%016x"%addr for addr in address_tp[1:] ]
        record = [tp[0],tp[1],x_address_tp]
        records.append(record)
    Print("Unpack sample records succeed!")
    return records
 
def unpack_mapped_libs(buff):
    Print("Unpack mapped libs info begin...")
    global g_offset
    string = str(buff[g_offset:])
    map_list = string.split("\n")
    Print("Unpack mapped libs info succeed!")
    return map_list
 
def read_profile_data(buff):
    Print("Read profile data begin...")
    unpack_profile_header(buff)
    records = unpack_records(buff)
    mapped_libs = unpack_mapped_libs(buff)
    Print("Read profile data succeed!")
    return records,mapped_libs

def main():
    global g_profile_data_file
    if not os.path.exists(g_profile_data_file):
        Print("profile data file[%s] does not exist!"%(g_profile_data_file))
        return 1
    if not os.path.exists(g_execute_file):
        Print("executable file[%s] does not exist!"%(g_execute_file))
        return 1
 
    bin_buff = None
    with open(g_profile_data_file,"rb") as fd:
        bin_buff = fd.read()
    records,mapped_libs = read_profile_data(bin_buff)
```
