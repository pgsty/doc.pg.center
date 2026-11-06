---
title: "使用 COPY 向 Apache Cloudberry 加载数据"
linkTitle: "使用 COPY 加载数据"
description: "`COPY FROM` 将本地文件系统中的文件或标准输入的数据复制到表中，并将数据追加到表的现有内容中。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-copy.md"
---

`COPY` 不支持并行：数据在单个进程中通过 Apache Cloudberry Coordinator 实例加载。`COPY` 仅建议用于非常小的数据文件。

`COPY` 源文件必须可由 Coordinator 主机上的 `postgres` 进程访问。请指定相对于 Coordinator 主机数据目录的 `COPY` 源文件名，或指定绝对路径。

Apache Cloudberry 使用客户端与 Coordinator 服务器之间的连接，通过 `STDIN` 或 `STDOUT` 复制数据。

## 从文件加载 {#load-from-a-file}

`COPY` 命令要求 `postgres` 后端打开并读取指定文件，然后将文件中的数据追加到目标表。要读取该文件，后端必须拥有文件的读取权限，并且必须使用 Coordinator 主机上的绝对路径，或使用相对于 Coordinator 数据目录的路径来指定文件名。

```sql
COPY <table_name> FROM </path/to/filename>;
```

## 从 STDIN 加载 {#load-from-stdin}

为了避免在加载数据前将数据文件复制到 Coordinator 主机，`COPY FROM STDIN` 使用标准输入通道，将数据直接提供给 `postgres` 后端。`COPY FROM STDIN` 命令启动后，后端会接受数据行，直到遇到仅包含反斜杠句点（`\.`）的单独一行。

```sql
COPY <table_name> FROM <STDIN>;
```

## 在 psql 中使用 `\copy` 加载数据 {#load-data-using-copy-in-psql}

不要将 psql 的 `\copy` 命令与 `COPY` SQL 命令混淆。`\copy` 调用常规的 `COPY FROM STDIN`，并将数据从 psql 客户端发送到后端。因此，任何文件都必须位于运行 psql 客户端的主机上，并且运行客户端的用户必须能够访问该文件。

为了避免在加载数据前将数据文件复制到 Coordinator 主机，`COPY FROM STDIN` 使用标准输入通道，将数据直接提供给 `postgres` 后端。`COPY FROM STDIN` 命令启动后，后端会接受数据行，直到遇到仅包含反斜杠句点（`\.`）的单独一行。psql 将这一过程封装成便捷的 `\copy` 命令。

```sql
\copy <table_name> FROM <filename>;
```

## 输入格式 {#input-format}

`COPY FROM` 接受 `FORMAT` 参数，该参数指定输入数据的格式。可用值为 `TEXT`、`CSV`（逗号分隔值）和 `BINARY`。

```sql
COPY <table_name> FROM </path/to/filename> WITH (FORMAT csv);
```

`FORMAT csv` 会读取逗号分隔值。`FORMAT text` 默认使用制表符分隔值，`DELIMITER` 选项可以指定其他字符作为值分隔符。

```sql
COPY <table_name> FROM </path/to/filename> WITH (FORMAT text, DELIMITER '|');
```

使用客户端的默认编码，你可以使用 `ENCODING` 选项更改编码。当数据来自其他操作系统时，这一选项很有用。

```sql
COPY <table_name> FROM </path/to/filename> WITH (ENCODING 'latin1');
```
