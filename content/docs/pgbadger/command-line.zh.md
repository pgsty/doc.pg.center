---
title: "命令行参考"
linkTitle: "命令行"
weight: 30
description: "完整的 pgBadger 命令语法、选项、远程输入、返回码与示例"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [参考]
aliases: [/pgbadger/command-line/]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## 用法与选项 {#usage-and-options}

用法：pgbadger [options] logfile [...]

```text
PostgreSQL 日志分析器，生成详细报告和图表。
```

参数：

```text
logfile 可以是单个日志文件、文件列表，或返回文件列表的 shell 命令。
若要从标准输入传入日志内容，请使用 - 作为文件名。
注意：csvlog 不支持从标准输入读取。
```

选项：

```text
-a | --average minutes : 查询与连接平均值图表的时间粒度，单位为分钟。默认 5 分钟。
-A | --histo-average min: 查询直方图的时间粒度，单位为分钟。默认 60 分钟。
-b | --begin datetime  : 待解析日志的起始日期/时间，可以是完整时间戳或仅时间。
-c | --dbclient host   : 只报告指定客户端主机的记录。
-C | --nocomment       : 从查询中删除 /* ... */ 一类的注释。
-d | --dbname database : 只报告指定数据库的记录。
-D | --dns-resolv      : 将客户端 IP 地址替换为 DNS 名称；可能显著降低解析速度。
-e | --end datetime    : 待解析日志的结束日期/时间，可以是完整时间戳或仅时间。
-E | --explode         : 按数据库拆分主报告，每个数据库生成一份报告。
                         与数据库无关的全局信息放入 postgres 数据库的报告。
-f | --format logtype  : 可选值：syslog、syslog2、stderr、jsonlog、csv、pgbouncer、
                         logplex、rds、redshift。无法自动识别格式时使用此选项。
-G | --nograph         : 禁用 HTML 输出中的图表；默认会生成图表。
-h | --help            : 显示帮助信息并退出。
-H | --html-outdir path: 增量模式下 HTML 报告的输出目录；二进制文件仍保存在
                         -O / --outdir 指定的目录。
-i | --ident name      : 用作 syslog 标识的程序名称。默认：postgres。
-I | --incremental     : 启用增量模式，按天在独立目录中生成报告。必须设置 --outdir。
-j | --jobs number     : 单个日志文件同时运行的解析进程数。
                         默认使用单进程；csvlog 格式也使用单进程。
-J | --Jobs number     : 并行解析的日志文件数。默认一次处理一个文件。
-l | --last-parsed file: 记录最后解析的日期/时间与行位置，以支持增量解析。
                         适合只查看上次运行后的错误，或为按周轮转的日志生成日报。
-L | --logfile-list file:包含待解析日志文件列表的文件。
-m | --maxlength size  : 查询的最大长度，超过此长度会截断。默认截断长度为 100000。
-M | --no-multiline    : 不收集多行语句，避免混入无关内容，尤其是错误导致的巨大报告。
-N | --appname name    : 只报告指定应用名称的记录。
-o | --outfile filename: 输出文件名。默认名称取决于格式：out.html、out.txt、out.bin
                         或 out.json。可多次指定，生成多种格式。
                         JSON 输出需要 Perl 模块 JSON::XS。
                         使用 - 作为文件名可输出到标准输出。
-O | --outdir path     : 输出文件的保存目录。
-p | --prefix string   : postgresql.conf 中自定义 log_line_prefix 的原始值。
                         只在未使用文档列出的标准前缀时需要指定，例如前缀额外包含
                         客户端 IP 或应用名称。必须包含时间占位符（%t、%m 或 %n）
                         和进程/会话占位符（%p 或 %c）。参见下文示例。
-P | --no-prettify     : 禁用 SQL 查询格式化。
-q | --quiet           : 不向标准输出打印任何内容，包括进度条。
-Q | --query-numbering : 使用 --dump-all-queries 或 --normalized-only 时为查询编号。
-r | --remote-host ip  : 指定远程主机，在该主机上执行 cat 读取日志并在本地解析。
-R | --retention N     : 增量模式的保留周数。默认 0，表示禁用清理。
                         超出保留期限的周目录和日目录会自动删除。
-s | --sample number   : 保存的查询样本数量。默认：3。
-S | --select-only     : 只报告 SELECT 查询。
-t | --top number      : 保存/显示的查询数量。默认：20。
-T | --title string    : 修改 HTML 报告的页面标题。
-u | --dbuser username : 只报告指定用户的记录。
-U | --exclude-user username : 从报告中排除指定用户的记录，可多次指定。
-v | --verbose         : 启用详细输出或调试模式，默认禁用。
-V | --version         : 显示 pgBadger 版本并退出。
-w | --watch-mode      : 只报告错误，类似 logwatch。
-W | --wide-char       : 将查询的 HTML 输出编码为 UTF8，避免 Perl 的
                         "Wide character in print" 提示。
-x | --extension       : 输出格式。可选值：text、html、bin、json。默认：html。
-X | --extra-files     : 增量模式下，将 CSS 和 JS 作为独立文件写入输出目录。
-z | --zcat exec_path  : 解压程序的完整路径；zcat、bzcat 或 unzip 不在 PATH 中时使用。
-Z | --timezone +/-XX  : 以相对 GMT 的小时偏移调整 JavaScript 图表的日期/时间。
                         可以是整数（例如 2）或小数（例如 2.5）。
--anonymize            : 隐藏查询中的所有字面量，用于隐藏机密数据。
--charset              : HTML 使用的字符集。默认：utf-8。
--command CMD          : 执行此命令，从其标准输出获取日志记录。
                         pgBadger 打开通向该命令的管道并解析它生成的日志。
--csv-separator        : CSV 字段分隔符。默认：,
--day-report YYYY-MM-DD: 为指定日期生成 HTML 报告；需要增量输出目录及全部必要的
                         二进制数据文件。
--disable-autovacuum   : 不生成 autovacuum 报告。
--disable-checkpoint   : 不生成 checkpoint/restartpoint 报告。
--disable-connection   : 不生成连接报告。
--disable-error        : 不生成错误报告。
--disable-hourly       : 不生成逐小时报告。
--disable-lock         : 不生成锁报告。
--disable-query        : 不生成查询报告，例如最慢、最频繁、按用户或按数据库统计的查询。
--disable-session      : 不生成会话报告。
--disable-temporary    : 不生成临时文件报告。
--disable-type         : 不生成按类型、数据库或用户统计的查询报告。
--dump-all-queries     : 导出日志中的全部查询，将绑定参数替换到各自的占位符位置。
--dump-raw-csv         : 解析日志并以 CSV 格式导出数据，不再进一步处理或生成报告。
--enable-checksum      : 在每份查询报告下添加 MD5 校验值。
--exclude-appname name : 从报告中排除指定应用的记录，例如 "pg_dump"。可多次指定。
--exclude-client name  : 排除指定客户端 IP 的日志记录，可多次指定。
--exclude-db name      : 从报告中排除指定数据库的记录，例如 "postgres"。可多次指定。
--exclude-file filename: 包含查询排除规则的文件，每行一个正则表达式。
--exclude-line regex   : 排除匹配此正则表达式的日志记录，可多次指定。
--exclude-query regex  : 排除匹配此正则表达式的查询，例如 "^(VACUUM|COMMIT)"。
                         可多次指定。
--exclude-time  regex  : 排除时间戳匹配此正则表达式的记录，例如 "2013-04-12 .*"。
                         可多次指定。
--explain-url URL      : 覆盖图形化执行计划工具的 URL。
                         默认：https://explain.depesz.com/
--histogram-query VAL  : 自定义查询耗时直方图的分组边界，默认值（毫秒）：
                         0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: 自定义会话耗时直方图的分组边界，默认值（毫秒）：
                         0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: 包含查询纳入规则的文件，每行一个正则表达式。
--include-query regex  : 不匹配此正则表达式的查询会被排除，例如 "(tbl1|tbl2)"。
                         可多次指定。
--include-pid PID      : 只报告指定会话进程 ID（%p）的事件，可多次指定。
--include-session ID   : 只报告指定会话 ID（%c）的事件，可多次指定。
--include-time  regex  : 只纳入时间戳匹配此正则表达式的记录，例如 "2013-04-12 .*"。
                         可多次指定。
--iso-week-number      : 增量模式下，每周从周一开始，并采用 ISO 8601 周编号。
                         编号范围为 01 至 53，第 1 周是新年中至少含 4 天的第一周。
--keep-comments        : 保留归一化查询中的注释，便于区分归一化结果相同的查询。
--journalctl command   : 调用 journalctl 替代 PostgreSQL 日志文件，例如：
                         journalctl -u postgresql-9.5
--log-duration         : 强制关联 log_duration = on 和 log_statement = 'all'
                         各自生成的日志记录。
--log-timezone +/-XX   : 以相对 GMT 的小时偏移调整从日志读取的日期/时间，再进行解析。
                         使用此选项会增加按日期/时间查找原始日志的难度。
                         可以是整数（例如 2）或小数（例如 2.5）。
--month-report YYYY-MM : 为指定月份生成累计 HTML 报告；需要增量输出目录及全部必要的
                         二进制数据文件。
--noexplain            : 不处理 auto_explain 生成的日志行。
--no-fork              : 不创建任何子进程，用于调试。
--no-process-info      : 不修改进程标题以标识 pgbadger 进程；部分系统不支持此操作。
--no-progressbar       : 禁用进度条。
--noreport             : 增量模式下不创建报告。
--no-week              : 增量模式下不生成周报，适合周报耗时过长的情况。
--normalized-only      : 只把全部归一化查询导出到 out.txt。
--pgbouncer-only       : 页头只显示与 PgBouncer 相关的菜单。
--pid-dir path         : PID 文件的存放目录。默认：/tmp。
--pid-file file        : 用于管理 pgBadger 并发执行的 PID 文件名。默认：pgbadger.pid。
--pie-limit num        : 饼图中低于 num% 的数据合并显示。
--prettify-json        : 对 JSON 输出进行排版，便于阅读。
--rebuild              : 根据增量输出目录中保留的二进制数据，重建全部 HTML 报告。
--start-monday         : 增量日历默认每周从周日开始；使用此选项改为周一。
--tempdir DIR          : 临时文件的写入目录。默认：File::Spec->tmpdir() || '/tmp'
```

pgBadger 可以通过免密 SSH 连接解析远程日志文件。使用 -r 或 --remote-host 指定
主机 IP 地址或主机名。另有若干附加选项，可对 SSH 连接进行完整控制。

```text
--ssh-identity file      使用的身份密钥文件路径。
--ssh-option  options    SSH 连接所使用的 -o 选项列表。
                         始终使用以下选项：
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          SSH 连接端口。默认：22。
--ssh-program ssh        SSH 程序的路径。默认：ssh。
--ssh-timeout second     SSH 连接超时，单位为秒。默认：10 秒。
--ssh-user username      连接用户名，默认使用运行 pgBadger 的用户。
```

`--ssh-sudo` 在远程列出文件和读取日志的命令前加上 `sudo`。远程 SSH 用户必须能够通过 `sudo` 执行这些命令，且不需要交互提示。

待解析的日志文件也可以用 URI 指定，支持 http[s] 与 [s]ftp 协议。文件由 curl
命令下载，并在下载过程中同步解析。ssh 协议同样受支持，与远程主机模式一样
使用 ssh 命令。参见下文示例。

返回码：

```text
0: 成功
1: 出错并终止
2: 执行被中断，例如按下 Ctrl+C
3: PID 文件已存在或无法创建
4: 命令行未指定日志文件
```

示例：

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# stderr 输出使用的日志行前缀
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# syslog 输出使用的日志行前缀
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# 使用 8 个 CPU 加快解析 10GB 日志文件
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

对远程日志文件使用 URI 写法：

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

可以同时解析本地 PostgreSQL 日志与远程 pgbouncer 日志文件：

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

通过 cron 任务每周报告错误：

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

利用增量机制每周生成报告：

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

这要求日志文件和 HTML 报告同样按周轮转。

更好的做法是使用自动生成的增量报告：

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

上述命令会按天和按周分别生成报告。

在增量模式下，还可以指定报告中保留的周数：

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

如果 pg_dump 每天 23:00 和 13:00 各运行半小时，可以按下面的方式把
这两个时段从报告中排除：

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

上面的表达式会排除这两个完整小时；可以按备份的实际运行时段进一步限定分钟部分。

这样可以避免 pg_dump 生成的 COPY 语句占据最慢查询列表的顶部。也可以用
更简单的 --exclude-appname "pg_dump" 解决该问题。

journalctl 的输出也可以像日志文件一样直接解析：

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

也可以从远程主机调用它：

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

此时命令行无需指定日志文件；若还有其他 PostgreSQL 日志需要解析，照常追加即可。

之后若要重建全部增量 HTML 报告，步骤如下：

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

该命令同时会更新全部资源文件（JS 与 CSS）。若报告当初使用该选项生成，
此处也应加上 -E 或 --explode。

pgBadger 还支持 logplex 格式的 Heroku PostgreSQL 日志：

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

该命令通过标准输入把 Heroku PostgreSQL 日志流式传给 pgbadger。

pgBadger 可以按 rds 格式自动识别 RDS 与 CloudWatch PostgreSQL 日志：

```text
pgbadger -f rds -o rds_out.html rds.log
```

每份 CloudSQL PostgreSQL 日志本质上是封装成 JSON 格式的普通 PostgreSQL 日志。
pgBadger 会自动识别；若需强制指定日志格式，使用 `jsonlog`：

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

这与 jsonlog 扩展的情形相同：JSON 格式有所不同，但 pgBadger 都能解析。

pgBadger 还支持 Kubernetes 上 CloudNativePG Postgres Operator 生成的日志：

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

使用以下命令创建月度累计报告：

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

该命令会在增量报告的日历视图中为月份名称添加链接，用于查看 2019 年 5 月的
报告。若报告当初使用该选项生成，此处也应加上 -E 或 --explode。
