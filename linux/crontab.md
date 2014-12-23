Title: crontab使用
Date: 2012-10-08 17:04
Category: Linux
Slug: crontab

crontab格式：

```bash
minute hour day-of-month month-of-year day-of-week [username] command
```

如果某用户使用crontab -e增加了定时任务，那么系统会使用该用户身份执行该任务。所以username不需要填，填了会被认为是command。

附几个常用用法，有助于理解定时任务的配置：

```bash
01 * * * * run_hourly
*/5 * * * * run_every_5mins
02 4 * * * run_daily
22 4 * * 0 run_weekly
42 4 1 * * run_monthly
```

另外：

/etc/crontab中是全局的定时任务配置

/var/log/cron可以查看定时任务的执行记录

/var/spool/cron/work中记录了work用户设置的定时任务

还有一点要注意：crontab是以non-login方式启动任务的，这时环境中会加载`~/.bashrc`的内容，不会加载`~/.bash\_profile`的内容。如果crontab运行的脚本中依赖`.bash_profile`的环境变量，最好在脚本开始处`source ~/.bash_profile`。

