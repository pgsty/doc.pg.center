---
title: "安装后操作"
description: "通过回归测试验证 Apache Cloudberry 构建，并运行功能和扩展的可选测试。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/post-installation.md"
---

## 验证基本功能 {#validate-basic-functionalities}

运行 installcheck 测试套件以验证基本功能。建议分别在启用和禁用 Orca（查询优化器）的情况下进行测试：

```bash
# Run tests with Orca optimizer enabled
PGOPTIONS='-c optimizer=on' make --directory=~/cloudberry installcheck

# Run tests with Orca optimizer disabled
PGOPTIONS='-c optimizer=off' make --directory=~/cloudberry installcheck
```

> [!TIP] 提示
> 虽然 Orca 是 Cloudberry 的默认优化器，但运行 installcheck 时必须显式设置 `optimizer=on`。如果不设置，`explain` 测试会因缺少显式配置选项而失败。

### 1. 测试结果 {#1-test-results}

installcheck 目标提供基本的功能测试。执行期间，你将看到类似以下的输出：

```bash
test tablespace                   ... ok         3236 ms (diff   76 ms)
parallel group (20 tests):  pg_lsn oid txid name char varchar int2 regproc text ...
     boolean                      ... ok          862 ms (diff   56 ms)
     char                         ... ok          419 ms (diff   87 ms)
     explain                      ... FAILED      310 ms (diff  139 ms)
```

最后会看到类似以下的摘要：

```
========================
 1 of 658 tests failed. 
========================
```

如果有测试失败：

- `regression.diffs`：显示实际结果与预期结果之间的差异。
- `regression.out`：包含完整的测试执行输出。

文件位于 `/home/gpadmin/cloudberry/src/test/regress/`。

> [!NOTE] 注意
> installcheck 只是几种可用测试方案之一。本指南着重介绍基本开发环境的搭建和验证。

### 2. 排查测试失败 {#2-troubleshoot-test-failures}

如果测试失败，可能需要检查各个集群组件的日志文件。可以查询 Segment 配置，找到包含这些日志的数据目录：

```bash
psql -P pager=off template1 -c 'SELECT * from gp_segment_configuration'
```

这会显示完整的集群配置，其中 `content = -1` 标识 Coordinator 节点：

```sql
 dbid | content | role | preferred_role | mode | status | port | hostname | address |                                  datadir                                   | warehouseid 
------+---------+------+----------------+------+--------+------+----------+---------+----------------------------------------------------------------------------+-------------
    1 |      -1 | p    | p              | n    | u      | 7000 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/qddir/demoDataDir-1         |           0
    8 |      -1 | m    | m              | s    | u      | 7001 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/standby                     |           0
    2 |       0 | p    | p              | s    | u      | 7002 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast1/demoDataDir0        |           0
    5 |       0 | m    | m              | s    | u      | 7005 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast_mirror1/demoDataDir0 |           0
    3 |       1 | p    | p              | s    | u      | 7003 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast2/demoDataDir1        |           0
    6 |       1 | m    | m              | s    | u      | 7006 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast_mirror2/demoDataDir1 |           0
    4 |       2 | p    | p              | s    | u      | 7004 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast3/demoDataDir2        |           0
    7 |       2 | m    | m              | s    | u      | 7007 | cdw      | cdw     | /home/gpadmin/cloudberry/gpAux/gpdemo/datadirs/dbfast_mirror3/demoDataDir2 |           0
```

每个 `datadir` 都包含有助于诊断测试失败的日志文件。根据失败的测试，检查相关组件目录中的日志。
