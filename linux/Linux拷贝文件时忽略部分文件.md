Title: linux cp过程中ignore部分文件
Date: 2012-09-03 20:31
Category: Linux

遇到一个需求，在cp的过程中需要ignore掉部分文件，发现cp没有自带ignore之类的选项。

比较容易的方式是使用rsync，但是折腾的过程中发现，使用find+cp也是可以达到ignore的目的的：

```bash
cd src && find ./ -type f -not -name '12' -not -name '13' -exec cp --parents '{}' './dst/' \;
```

记录一下，免得需要时又到处找。

