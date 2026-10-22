---
title: "输出格式"
linkTitle: "输出格式"
weight: 70
description: "选择 HTML、文本、二进制、JSON 或原始 CSV 输出，并合并中间数据文件"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [参考]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger 会根据输出文件扩展名，或 `-x` / `--extension` 选项选择格式。同一次解析可多次使用 `-o` / `--outfile`，同时生成多种格式。

| 格式 | 常用扩展名 | 最适合 |
|---|---|---|
| HTML | `.html` | 带图表的交互式人类可读报告 |
| 文本 | `.txt` | 终端查看与纯文本归档 |
| 二进制 | `.bin` | 可合并的中间统计数据与报告重建 |
| JSON | `.json` | 与其他软件集成；需要 `JSON::XS` |
| 原始 CSV | 自选输出文件 | 使用 `--dump-raw-csv` 导出逐行数据 |

## HTML 与文本 {#html-and-text}

默认输出为 `out.html`：

```console
$ pgbadger postgresql.log -o report.html
```

HTML 通常会内嵌独立浏览所需的脚本、样式、字体与报告数据。`-X` / `--extra-files` 会把增量报告的公共 JavaScript 与 CSS 移到外部文件；移动 HTML 目录时必须保留这些资源。

显式生成文本：

```console
$ pgbadger -x text -o report.txt postgresql.log
```

对于支持的格式，可用 `-` 作为输出文件名，把内容写到标准输出。

## 二进制中间数据 {#binary-format}

二进制输出把“解析日志”和“展示报告”分开。可以从一份持续增长的每日日志中生成逐小时增量：

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

把一个或多个二进制文件合并为新报告：

```console
$ pgbadger -o sunday.html sunday/*.bin
```

如果服务器每小时生成一个日志，可为每次轮转生成一份二进制文件，并按需重建累计 HTML：

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

同一个目录中应只混用彼此兼容的 pgBadger 版本生成的二进制文件。升级长期保留的增量目录前，应先查看版本说明中的格式兼容性信息。

## JSON {#json-format}

JSON 输出面向监控或报告流水线等程序化消费者：

```console
$ pgbadger -o report.json postgresql.log
```

需要先安装 `JSON::XS`。如果可读性比文件大小和生成速度更重要，可加入 `--prettify-json`。

## 原始数据与查询导出 {#raw-exports}

命令参考还提供以下专用导出模式：

- `--dump-raw-csv` 解析日志并输出逐行 CSV，不再生成报告；
- `--csv-separator` 修改原始 CSV 分隔符；13.2 默认使用逗号（`,`）；
- `--dump-all-queries` 在替换绑定参数后输出所有查询；
- `--normalized-only` 输出归一化查询；
- `--query-numbering` 为查询类文本输出编号。

这些输出可能包含应用 SQL、标识符、用户、客户端地址或字面量。共享前应先检查内容；如果分析不需要保留字面量，请使用 `--anonymize`。
