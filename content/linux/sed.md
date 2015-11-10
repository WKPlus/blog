# sed使用帮助文档

## 替换
```shell
# cat text
    <span class="tagline">爱生活，爱点评！</span>
#
# sed 's/span/SPAN/' text
    <SPAN class="tagline">爱生活，爱点评！</span>
#
# sed 's/span/SPAN/g' text
    <SPAN class="tagline">爱生活，爱点评！</SPAN>
# sed 's/span/SPAN/2' text
    <span class="tagline">爱生活，爱点评！</SPAN>
#
```
替换模式下，还有一些命令，比如小写转大写`\u`，大写转小写`\l`，详见[官方文档](https://www.gnu.org/software/sed/manual/html_node/The-_0022s_0022-Command.html)

## 筛选
### 行号筛选
```shell
# cat text
1a
2a
3a
# sed '1s/a/A/' text
1A
2a
3a
# sed '1,2s/a/A/' text
1A
2A
3a
# sed '1,+1s/a/A/' text
1A
2A
3a
# sed '1!s/a/A/' text
1a
2A
3A
#
```

### 匹配筛选
```shell
# cat text
xa
ya
za
# sed '/x/s/a/A/' text
xA
ya
za
# sed '/x/,/y/s/a/A/' text
xA
yA
za
# sed '/x/,+1s/a/A/' text
xA
yA
za
#
```

## 常用的选项
### `-i` 修改源文件
`sed`默认是不修改源文件的，如果要修改可以将输出重定向到另外一个文件然后覆盖现在的文件或者直接使用-i选项。
```shell
# cat text
    <span class="tagline">爱生活，爱点评！</span>
# sed 's/span/SPAN/' text
    <SPAN class="tagline">爱生活，爱点评！</span>
# cat text
    <span class="tagline">爱生活，爱点评！</span>
#
# cat text
    <span class="tagline">爱生活，爱点评！</span>
#
# sed -i 's/span/SPAN/' text
    <SPAN class="tagline">爱生活，爱点评！</span>
# cat text
    <SPAN class="tagline">爱生活，爱点评！</span>
```

### `-n` 默认不输出，`p` 输出当前行
`sed`默认是输出所有行，使用`-n`选项会关闭输出。和`p`命令一起使用，可以有效控制输出。
```shell
# cat text
1a
2b
3c
# sed -n '/a/p' text
1a
# sed -n 's/a/A/p' text
1A
# sed -n '2,3p' text
2b
3c
```


## 插入、删除与替换
### `a` 命令：在当前行之后插入
```shell
# cat text
1a
2a
3a
# sed '1a A new line' text
1a
A new line
2a
3a
# sed '1a\ A new line' text #如果插入或替换的行，开头有空格，需要使用\
1a
 A new line
2a
3a
```

### `i` 命令：在当前行之前插入
```shell
# cat text
1a
2a
3a
# sed '1i A new line' text
A new line
1a
2a
3a
```

### `d` 命令：删除当前行
```shell
# cat text
1a
2a
3a
# sed '1d' text #删除第一行
2a
3a
# sed '/2/d' text #删除包含"2"的行
1a
3a
```

### `c`命令：替换当前行
```shell
# cat text
1a
2a
3a
# sed '2c A new line' text
1a
A new line
3a
```

## 多模匹配
多条命令一起运行，从前往后
```shell
# cat text
1a
2a
3a
# sed '1s/a/A/;s/a/B/' text
1A
2B
3B
# sed -e '1s/a/A/' -e 's/a/B/' text
1A
2B
3B
```


## 提取
### 圆括号保留匹配内容，可以使用`\1` `\2`引用
```shell
# cat text
1a
# sed -r 's/1(.)/\1/' text
a
```

### `-r`选项，打开正则，和圆括号配合使用
```shell
# cat text
<span class="tagline">爱生活，爱点评！</span>
# sed -r 's/.*>(.*)<.*/\1/' text
爱生活，爱点评！
```

## 嵌套命令
```shell
# cat t
1*2=2
2*2=4
3*2=6
# sed '/2/{/4/d}' t
1*2=2
3*2=6
```

## PatternSpace和HoldSpace
 - Patternspace `sed`处理文本的工作空间
 - Holdspace `sed`处理文本的临时空间
 - `g` 将HoldSpace内容覆盖到Patternspace
 - `G` 将Holdspace内容添加到Patternspace
 - `h` 将Patternspace内容覆盖到Holdspace
 - `H` 将Patternspace内容添加到Holdspace
 - `x` 交换Patternspace和Holdspace的内容
```shell
# cat sequence
1
2
3
4
5
# sed -n 'G;h;$p' sequence
5
4
3
2
1

# sed -n '1!G;h;$p' sequence
5
4
3
2
1
```


## 正则特殊字符
 - `.` 任意字符
 - `*` 重复0或多次
 - `+` 重复1或多次
 - `?` 重复0或1次
 - `[]` 字符集合，比如`[abc]`表示匹配abc其中任意一个，支持区间表示法`[a-zA-Z]`
 - `[^]` 字符集合非，比如`[^abc]`表示不匹配abc其中任意一个字符
 - `{}` 重复次数，比如`{3}`表示重复3次，`{3,5}`重复3-5次，`{3,}`重复3次以上
 - `()` 分组，可供后续引用
 - `^` 匹配行开头
 - `$` 匹配行结尾
 - `\w` 匹配字母和数字，即`[a-zA-Z0-9_]`
 - `\s` 匹配空白字符，即`[ \t\n\r]`等
 - `\b` 单词边界，即`\w`和非`\w`的交界处，匹配的是位置不是字符，长度为0
 - `\W` `\S` `\B`分别是`[^\w]` `[^\s]` `[^\b]`的含义

