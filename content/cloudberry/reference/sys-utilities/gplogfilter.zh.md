---
title: "gplogfilter"
description: "在 Apache Cloudberry 日志文件中搜索指定条目。"
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gplogfilter.md"
---

## 概要 {#synopsis}

```shell
gplogfilter [<timestamp_options>] [<pattern_options>] 
     [<output_options>] [<input_options>] [<input_file>] 

gplogfilter --help 

gplogfilter --version
```

## 说明 {#description}

`gplogfilter` 工具可用于在 Apache Cloudberry 日志文件中搜索符合指定条件的条目。如果未提供输入文件，`gplogfilter` 将使用 `$COORDINATOR_DATA_DIRECTORY` 环境变量，在标准日志位置查找 Cloudberry Coordinator 日志文件。要从标准输入读取，请将连字符（`-`）用作输入文件名。输入文件可以使用 `gzip` 压缩。输入文件中的日志条目通过格式为 `YYYY-MM-DD [hh:mm[:ss]]` 的时间戳识别。

也可以通过 [gpssh](/cloudberry/reference/sys-utilities/gpssh/) 工具运行 `gplogfilter`，同时搜索所有 Segment 日志文件。例如，显示各 Segment 日志文件的最后三行：

```shell
gpssh -f seg_host_file
=> source /usr/local/cloudberry/greenplum_path.sh
=> gplogfilter -n 3 /gpdata/*/log/gpdb*.csv
```

默认情况下，`gplogfilter` 的输出发送到标准输出。使用 `-o` 选项可将输出发送到文件或目录。如果提供以 `.gz` 结尾的输出文件名，默认会使用最大压缩级别压缩输出文件。如果输出目标是目录，输出文件将采用与输入文件相同的名称。

## 选项 {#options}

**时间戳选项**

**`-b datetime | --begin=datetime`**

指定开始搜索日志条目的起始日期和时间，格式为 `YYYY-MM-DD [hh:mm[:ss]]`。

如果指定时间，必须用单引号或双引号括起日期和时间。以下示例使用单引号：

```shell
gplogfilter -b '2013-05-23 14:33'
```

**`-e datetime | --end=datetime`**

指定停止搜索日志条目的结束日期和时间，格式为 `YYYY-MM-DD [hh:mm[:ss]]`。

如果指定时间，必须用单引号或双引号括起日期和时间。以下示例使用单引号：

```shell
gplogfilter -e '2013-05-23 14:33' 
```

**`-d<time> | --duration=<time>`**

指定搜索日志条目的时间跨度，格式为 `[hh][:mm[:ss]]`。如果既未使用 `-b` 选项，也未使用 `-e` 选项，则以当前时间为基准。

### 模式匹配选项 {#pattern-matching-options}

**`-c i [gnore] | r [espect] | --case=i [gnore] | r [espect]`**

默认情况下，字母匹配区分大小写，除非之前指定了 `--case=ignore` 选项。

**`-C 'string' | --columns='string'`**

从日志文件中选择特定列。用逗号分隔的列号字符串指定所需列，列号从 1 开始，从左边数第二列为 2，第三列为 3，以此类推。

**`-f 'string' | --find='string'`**

查找包含指定字符串的日志条目。

**`-F 'string' | --nofind='string'`**

排除包含指定字符串的日志条目。

**`-m regex | --match=regex`**

查找匹配指定 Python 正则表达式的日志条目。Python 正则表达式语法请参阅 [https://docs.python.org/library/re.html](https://docs.python.org/library/re.html)。

**`-M regex | --nomatch=regex`**

排除匹配指定 Python 正则表达式的日志条目。Python 正则表达式语法请参阅 [https://docs.python.org/library/re.html](https://docs.python.org/library/re.html)。

**`-t | --trouble`**

仅查找第一行包含 `ERROR:`、`FATAL:` 或 `PANIC:` 的日志条目。

### 输出选项 {#output-options}

**`-n <integer> | --tail=<integer>`**

将输出限制为找到的符合条件的日志条目中的最后 `<integer>` 条。

**`-s <offset> [limit] | --slice=<offset> [limit]`**

从符合条件的日志条目列表中，自编号为 `<offset>` 的条目起返回 `<limit>` 条记录。`<offset>` 为零（`0`）表示结果集的第一条记录；`<offset>` 大于零时，则从结果集末尾向前计数。

**`-o <output_file> | --out=<output_file>`**

将输出写入指定文件或目录位置，而不是 `STDOUT`。

**`-z 0-9 | --zip=0-9`**

使用 `gzip` 按指定压缩级别压缩输出文件，`0` 表示不压缩，`9` 表示最大压缩。如果提供以 `.gz` 结尾的输出文件名，默认使用最大压缩级别。

**`-a | --append`**

如果输出文件已存在，则追加到该文件，而不是覆盖它。

**输入选项**

**`input_file`**

要搜索的输入日志文件名。如果未提供输入文件，`gplogfilter` 将使用 `$COORDINATOR_DATA_DIRECTORY` 环境变量查找 Apache Cloudberry Coordinator 日志文件。要从标准输入读取，请将连字符（`-`）用作输入文件名。

**`-u | --unzip`**

使用 `gunzip` 解压输入文件。如果输入文件名以 `.gz` 结尾，默认会解压。

**`--help`**

显示在线帮助。

**`--version`**

显示此工具的版本。

## 示例 {#examples}

显示 Coordinator 日志文件中的最后三条错误消息：

```shell
gplogfilter -t -n 3
```

显示 Coordinator 日志文件中时间戳位于最近 10 分钟内的所有日志消息：

```shell
gplogfilter -d :10
```

显示 Coordinator 日志文件中包含字符串 `|con6 cmd11|` 的日志消息：

```shell
gplogfilter -f '|con6 cmd11|'
```

使用 [gpssh](/cloudberry/reference/sys-utilities/gpssh/) 在 Segment 主机上运行 `gplogfilter`，搜索 Segment 日志文件中包含字符串 `con6` 的日志消息，并将输出保存到文件。

```shell
gpssh -f seg_hosts_file -e 'source 
/usr/local/cloudberry/greenplum_path.sh ; gplogfilter -f 
con6 /gpdata/*/log/gpdb*.csv' > seglog.out
```

## 另请参阅 {#see-also}

[gpssh](/cloudberry/reference/sys-utilities/gpssh/), [gpsync](/cloudberry/reference/sys-utilities/gpsync/)
