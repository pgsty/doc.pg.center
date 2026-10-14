---
title: "增量报告"
linkTitle: "增量报告"
weight: 60
description: "生成每日与每周报告，控制保留期，重建输出并添加月度汇总"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [任务]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

增量模式先以二进制形式保存解析统计，再生成每日 HTML 报告、每周累计报告，以及把它们组织起来的日历式索引。它适合反复处理轮转日志，同时避免重复统计相同记录。

## 生成每日与每周报告 {#daily-and-weekly}

在每日轮转完成后运行 pgBadger，并指定一个持久化输出目录：

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I` 启用增量模式，`-O` 指定保存二进制状态、日历索引和生成报告的目录。pgBadger 会在该目录自行维护增量状态；只有明确希望把状态文件放到其他位置时，才需要 `--last-parsed`。

也可以把 HTML 放到单独目录，同时在原目录保留二进制状态：

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

二进制文件是未来重建报告的源数据。如果报告必须能够重新生成，应备份这些文件，或保留原始日志。

## 保留策略 {#retention}

只保留指定周数：

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

更早的周与日目录会被自动删除。不要直接在唯一一份报告历史上首次试用该策略，应先在非生产副本上验证。

## 把公共资源单独写出 {#shared-assets}

默认情况下，每份 HTML 报告都内嵌 JavaScript 与 CSS。增量目录包含大量报告时，`-X` / `--extra-files` 会把公共资源单独写出，减少重复数据：

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

移动报告时，必须把所有 HTML 与对应版本的资源目录一起移动。

## 重建已有报告 {#rebuild}

升级 pgBadger 或应用报告生成修复后，可以从保留的二进制数据重建 HTML：

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

如果原报告按数据库拆分生成，请在重建时再次加入 `-E` / `--explode`。

> 请使用长选项 `--rebuild`。当前命令参考中的 `-R` 表示 `--retention`；把 `-R` 当作重建缩写会执行错误的选项。

## 添加月度报告 {#monthly-reports}

每日与每周报告会自动生成。月度汇总需要显式执行，因为很长的历史可能使计算开销很大：

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

生成的月份会加入日历索引。再次运行命令会从现有二进制数据重建该月份。按数据库拆分的历史需要继续使用 `-E`：

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

完整命令参考还提供 `--day-report YYYY-MM-DD`、`--no-week`、`--noreport`、`--start-monday` 和 `--iso-week-number`，可用于更特殊的调度策略。

可以直接打开随站点打包的[增量报告示例](/third_party/pgbadger/examples/report/index.html)，离线查看日历、周链接与每日报告的目录层级。
