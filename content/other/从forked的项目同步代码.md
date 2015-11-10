Title: 从forked的项目同步代码
Date: 2015-11-6 18:35
Category: other
Slug: git-sync-from-forked-repo

从forked项目的master分支同步代码至fork项目的master分支：

```
1. git remote add upstream \<forked project url>
2. git fetch upstream
3. git checkout master #保证本地处于master分支
4. git merge upstream/master #把forked项目的修改merge到本地
5. git push origin master #把本地修改提交到远端仓库（fork项目）的master分支
```



从forked项目同步新分支到fork项目：

```

1. git remote add upstream \<forked project url>
2. git fetch upstream
3. git checkout -b newbranch upstream/newbranch
4. git push -u origin newbranch

```
注意，第4步加上`-u`之后，会把本地newbranch关联到远端origin的newbranch，这样你在该分支上做修改之后`git push`就会把变更push到origin/newbranch而不是upstream/newbranch。