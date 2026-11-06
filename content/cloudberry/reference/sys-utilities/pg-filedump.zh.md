---
title: "pg_filedump"
description: "Filedump，也称为命令行工具 `pg_filedump`，是将 Apache Cloudberry 堆文件、索引文件和控制文件格式化为可读形式的系统工具。"
weight: 360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-filedump.md"
---

使用 filedump，可以按[命令行选项](#command-line-options)一节所述，以多种方式格式化和转储文件，甚至直接转储二进制数据。

Apache Cloudberry 的 filedump 仓库位于：`https://github.com/cloudberry-contrib/filedump`

## 使用场景 {#user-scenarios}

filedump 工具主要用于以下场景：

- **文件分析与调试**：将数据库中的堆文件、索引文件或控制文件转换为可读格式，帮助分析文件内容和调试数据库问题。
- **数据恢复**：在数据库文件损坏时帮助提取和恢复数据。
- **数据库学习与研究**：让开发人员和管理员可以直接检查数据库文件内容，有助于研究数据库内部机制或了解文件格式。

## 编译与安装 filedump {#compile-and-install-filedump}

编译 filedump 前，需要已安装 1.0.0 或更高版本的 Apache Cloudberry 集群。典型的编译步骤如下：

1. 确保能够找到 Cloudberry 软件包：

    ```bash
    su - gpadmin
    source /usr/local/cloudberry/greenplum_path.sh
    ```

2. 将 GitHub 仓库 `cloudberry-contrib/filedump` 克隆到本地环境：

    ```bash
    git clone https://github.com/cloudberry-contrib/filedump.git
    ```

3. 进入仓库目录并运行编译命令：

    ```bash
    cd filedump
    make
    ```

4. 安装 `pg_filedump`：

    ```bash
    make install
    ```

### 配置选项 {#configuration-options}

编译过程中可使用以下配置选项：

- `ENABLE_ZLIB`：允许 `pg_filedump` 处理经 zlib 压缩的数据文件。如果检测到 `zlib` 头文件和库，将自动启用 zlib 支持。可以使用以下命令强制启用 zlib 支持：

    ```bash
    make -f Makefile ENABLE_ZLIB=y
    ```

    也可以将此变量设为 `n`，强制禁用此支持。

- `ENABLE_ZSTD`：对 `zstd` 压缩方法采用类似的设置。

## 使用示例 {#usage-examples}

假定已成功安装 `filedump`，以下是一些常见命令示例：

### 格式化堆文件 {#format-a-heap-file}

```bash
pg_filedump -f /path/to/heap/file
```

示例：

```bash
$ pg_filedump -f /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385

*******************************************************************
* PostgreSQL File/Block Formatted Dump Utility
*
* File: /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385
* Options used: -f
*******************************************************************

Block    0 ********************************************************
<Header> -----
Block Offset: 0x00000000         Offsets: Lower      44 (0x002c)
Block: Size 32768  Version   14            Upper    32568 (0x7f38)
LSN:  logid      0 recoff 0x0c084ef8      Special  32768 (0x8000)
Items:    5                      Free Space: 32524
Checksum: 0x27ac  Prune XID: 0x00000000  Flags: 0x0000 ()
Length (including item array): 44

0000: 00000000 f84e080c ac270000 2c00387f  .....N...'..,.8.
0010: 00800e80 00000000 d8ff4800 b0ff5000  ..........H...P.
0020: 88ff5000 60ff5000 38ff5000           ..P.`.P.8.P.    

<Data> -----
Item   1 -- Length:   36  Offset: 32728 (0x7fd8)  Flags: NORMAL
7fd8: 1b030000 00000000 00000000 00000000  ................
7fe8: 01000300 02081800 02000000 09426f62  .............Bob
7ff8: 19000000                             ....            

Item   2 -- Length:   40  Offset: 32688 (0x7fb0)  Flags: NORMAL
7fb0: 1b030000 00000000 00000000 00000000  ................
7fc0: 02000300 02081800 03000000 11436861  .............Cha
7fd0: 726c6965 23000000                    rlie#...        

Item   3 -- Length:   40  Offset: 32648 (0x7f88)  Flags: NORMAL
7f88: 1c030000 00000000 00000000 00000000  ................
7f98: 03000300 02081800 04000000 0d446176  .............Dav
7fa8: 69640000 1c000000                    id......        

Item   4 -- Length:   40  Offset: 32608 (0x7f60)  Flags: NORMAL
7f60: 1d030000 00000000 00000000 00000000  ................
7f70: 04000300 02081800 07000000 11436861  .............Cha
7f80: 726c6965 23000000                    rlie#...        

Item   5 -- Length:   40  Offset: 32568 (0x7f38)  Flags: NORMAL
7f38: 1d030000 00000000 00000000 00000000  ................
7f48: 05000300 02081800 08000000 0d446176  .............Dav
7f58: 69640000 1c000000                    id......        

*** End of File Encountered. Last Block Read: 0 ***
```

### 查看控制文件内容 {#view-the-content-of-a-control-file}

```bash
pg_filedump -c /path/to/pg_control
```

示例：

```bash
$ pg_filedump -c /home/gpadmin/datadirs/qddir/demoDataDir-1/global/pg_control

*******************************************************************
* PostgreSQL File/Block Formatted Dump Utility
*
* File: /home/gpadmin/datadirs/qddir/demoDataDir-1/global/pg_control
* Options used: -c
*******************************************************************

<pg_control Contents> *********************************************

                        CRC: Correct
        pg_control Version: 13000700
            Catalog Version: 302406171
            System Identifier: 7405502447288557259
                        State: IN PRODUCTION
                Last Mod Time: Wed Aug 21 16:20:06 2024
    Last Checkpoint Record: Log File (0) Offset (0x0c088f80)
Last Checkpoint Record Redo: Log File (0) Offset (0x0c088f48)
        |-       TimeLineID: 1
        |-         Next XID: 0/809
        |-         Next OID: 24576
        |- Next Relfilenode: 24576
        |-       Next Multi: 1
        |-    Next MultiOff: 0
        |-             Time: Wed Aug 21 16:20:06 2024
    Minimum Recovery Point: Log File (0) Offset (0x00000000)
        Backup Start Record: Log File (0) Offset (0x00000000)
            Backup End Record: Log File (0) Offset (0x00000000)
End-of-Backup Record Required: no
    Maximum Data Alignment: 8
        Floating-Point Sample: 1234567
        Database Block Size: 32768
        Blocks Per Segment: 32768
            XLOG Block Size: 32768
            XLOG Segment Size: 67108864
    Maximum Identifier Length: 64
        Maximum Index Keys: 32
            TOAST Chunk Size: 8140
```

### 格式化并显示指定块范围 {#format-and-display-a-specific-block-range}

```bash
pg_filedump -R 0 10 -f /path/to/heap/file
```

示例：

```bash
$ pg_filedump -R 0 10 -f /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385

*******************************************************************
* PostgreSQL File/Block Formatted Dump Utility
*
* File: /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385
* Options used: -R 0 10 -f
*******************************************************************

Block    0 ********************************************************
<Header> -----
Block Offset: 0x00000000         Offsets: Lower      44 (0x002c)
Block: Size 32768  Version   14            Upper    32568 (0x7f38)
LSN:  logid      0 recoff 0x0c084ef8      Special  32768 (0x8000)
Items:    5                      Free Space: 32524
Checksum: 0x27ac  Prune XID: 0x00000000  Flags: 0x0000 ()
Length (including item array): 44

0000: 00000000 f84e080c ac270000 2c00387f  .....N...'..,.8.
0010: 00800e80 00000000 d8ff4800 b0ff5000  ..........H...P.
0020: 88ff5000 60ff5000 38ff5000           ..P.`.P.8.P.    

<Data> -----
Item   1 -- Length:   36  Offset: 32728 (0x7fd8)  Flags: NORMAL
7fd8: 1b030000 00000000 00000000 00000000  ................
7fe8: 01000300 02081800 02000000 09426f62  .............Bob
7ff8: 19000000                             ....            

Item   2 -- Length:   40  Offset: 32688 (0x7fb0)  Flags: NORMAL
7fb0: 1b030000 00000000 00000000 00000000  ................
7fc0: 02000300 02081800 03000000 11436861  .............Cha
7fd0: 726c6965 23000000                    rlie#...        

Item   3 -- Length:   40  Offset: 32648 (0x7f88)  Flags: NORMAL
7f88: 1c030000 00000000 00000000 00000000  ................
7f98: 03000300 02081800 04000000 0d446176  .............Dav
7fa8: 69640000 1c000000                    id......        

Item   4 -- Length:   40  Offset: 32608 (0x7f60)  Flags: NORMAL
7f60: 1d030000 00000000 00000000 00000000  ................
7f70: 04000300 02081800 07000000 11436861  .............Cha
7f80: 726c6965 23000000                    rlie#...        

Item   5 -- Length:   40  Offset: 32568 (0x7f38)  Flags: NORMAL
7f38: 1d030000 00000000 00000000 00000000  ................
7f48: 05000300 02081800 08000000 0d446176  .............Dav
7f58: 69640000 1c000000                    id......        



*** End of File Encountered. Last Block Read: 0 ***
```

### 使用 `-i` 和 `-f` 选项获取详细信息 {#get-detailed-information-using-the--i-and--f-options}

```bash
pg_filedump -i -f /path/to/heap/file
```

示例：

```bash
$ pg_filedump -i -f /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385

*******************************************************************
* PostgreSQL File/Block Formatted Dump Utility
*
* File: /home/gpadmin/datadirs/dbfast1/demoDataDir0/base/13347/16385
* Options used: -i -f
*******************************************************************

Block    0 ********************************************************
<Header> -----
 Block Offset: 0x00000000         Offsets: Lower      44 (0x002c)
 Block: Size 32768  Version   14            Upper    32568 (0x7f38)
 LSN:  logid      0 recoff 0x0c084ef8      Special  32768 (0x8000)
 Items:    5                      Free Space: 32524
 Checksum: 0x27ac  Prune XID: 0x00000000  Flags: 0x0000 ()
 Length (including item array): 44

  0000: 00000000 f84e080c ac270000 2c00387f  .....N...'..,.8.
  0010: 00800e80 00000000 d8ff4800 b0ff5000  ..........H...P.
  0020: 88ff5000 60ff5000 38ff5000           ..P.`.P.8.P.    

<Data> -----
 Item   1 -- Length:   36  Offset: 32728 (0x7fd8)  Flags: NORMAL
  XMIN: 795  XMAX: 0  CID|XVAC: 0
  Block Id: 0  linp Index: 1   Attributes: 3   Size: 24
  infomask: 0x0802 (HASVARWIDTH|XMAX_INVALID) 

  7fd8: 1b030000 00000000 00000000 00000000  ................
  7fe8: 01000300 02081800 02000000 09426f62  .............Bob
  7ff8: 19000000                             ....            

 Item   2 -- Length:   40  Offset: 32688 (0x7fb0)  Flags: NORMAL
  XMIN: 795  XMAX: 0  CID|XVAC: 0
  Block Id: 0  linp Index: 2   Attributes: 3   Size: 24
  infomask: 0x0802 (HASVARWIDTH|XMAX_INVALID) 

  7fb0: 1b030000 00000000 00000000 00000000  ................
  7fc0: 02000300 02081800 03000000 11436861  .............Cha
  7fd0: 726c6965 23000000                    rlie#...        

 Item   3 -- Length:   40  Offset: 32648 (0x7f88)  Flags: NORMAL
  XMIN: 796  XMAX: 0  CID|XVAC: 0
  Block Id: 0  linp Index: 3   Attributes: 3   Size: 24
  infomask: 0x0802 (HASVARWIDTH|XMAX_INVALID) 

  7f88: 1c030000 00000000 00000000 00000000  ................
  7f98: 03000300 02081800 04000000 0d446176  .............Dav
  7fa8: 69640000 1c000000                    id......        

 Item   4 -- Length:   40  Offset: 32608 (0x7f60)  Flags: NORMAL
  XMIN: 797  XMAX: 0  CID|XVAC: 0
  Block Id: 0  linp Index: 4   Attributes: 3   Size: 24
  infomask: 0x0802 (HASVARWIDTH|XMAX_INVALID) 

  7f60: 1d030000 00000000 00000000 00000000  ................
  7f70: 04000300 02081800 07000000 11436861  .............Cha
  7f80: 726c6965 23000000                    rlie#...        

 Item   5 -- Length:   40  Offset: 32568 (0x7f38)  Flags: NORMAL
  XMIN: 797  XMAX: 0  CID|XVAC: 0
  Block Id: 0  linp Index: 5   Attributes: 3   Size: 24
  infomask: 0x0802 (HASVARWIDTH|XMAX_INVALID) 

  7f38: 1d030000 00000000 00000000 00000000  ................
  7f48: 05000300 02081800 08000000 0d446176  .............Dav
  7f58: 69640000 1c000000                    id......        



*** End of File Encountered. Last Block Read: 0 ***
```

### 命令行选项 {#command-line-options}

使用 filedump 工具时，可通过以下命令格式化并转储数据库文件：

```bash
pg_filedump [-abcdfhikxy] [-R startblock [endblock]] [-D attrlist] [-S blocksize] [-s segsize] [-n segnumber] file
```

默认设置为：使用相对寻址，格式化整个文件，并使用文件第 0 块中列出的块大小。

以下选项适用于堆文件和索引文件：

- **-a**：格式化时显示绝对地址。块头信息始终使用相对于块的地址。
- **-b**：显示指定范围内的二进制块映像。此选项会禁用所有其他格式化选项。
- **-d**：显示经过格式化的块内容转储。此选项会禁用所有其他格式化选项。
- **-D**：按照给定的逗号分隔类型列表解码元组。支持的类型包括：
    - bigint
    - bigserial
    - bool
    - char
    - charN -- char(n)
    - date
    - float
    - float4
    - float8
    - int
    - json
    - macaddr
    - name
    - oid
    - real
    - serial
    - smallint
    - smallserial
    - text
    - time
    - timestamp
    - timetz
    - uuid
    - varchar
    - varcharN -- varchar(n)
    - xid
    - xml
    - `~`：忽略元组中所有剩余属性。
- **-f**：显示经过格式化的块内容转储，并附带解析说明。
- **-h**：显示帮助信息。
- **-i**：显示解析后的项详细信息。
- **-k**：验证块校验和。
- **-R**：显示文件中的指定块范围（块编号从 0 开始）。
    - `[startblock]`：起始块。
    - `[endblock]`：结束块（不包含该块）。如果仅指定 `startblock`，则只格式化这一个块。
- **-s**：强制将段大小设为 `[segsize]`。
- **-n**：强制将段编号设为 `[segnumber]`。
- **-S**：强制将块大小设为 `[blocksize]`。
- **-x**：强制将块中的项作为索引项进行解析和格式化。
- **-y**：强制将块中的项作为堆项进行解析和格式化。

以下选项适用于控制文件：

- **-c**：将指定文件解析为控制文件。
- **-f**：显示经过格式化的内容转储，并附带解析说明。
- **-S**：强制将块大小设为 `[blocksize]`。

建议使用 `-i` 和 `-f` 选项，以获得最有用的转储输出。
