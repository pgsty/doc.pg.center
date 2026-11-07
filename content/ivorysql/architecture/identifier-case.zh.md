---
title: 引用标识符大小写转换
linkTitle: 大小写转换
description: IvorySQL v5.6 文档：引用标识符大小写转换。
type: docs
weight: 670
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/6.3.9.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

为了满足Oracle的引用标识符大小写兼容，ivorysql设计了三种引用标识符的大小写转换模式。

## 2. 实现说明 {#implementation-details}

如果在数据库初始化时附加了参数 `-C`，值可以为 `normal/interchange/lowercase`，则代码中 `Initdb.c→main()` 函数会处理该参数，根据参数值设置全局变量 `caseswitchmode`。然后 `initdb` 命令会以 `-boot` 模式启动一个 `postgres` 进程用于设置 `template1` 模板数据库，同时赋予参数 `-C ivorysql.identifier_case_switch=caseswitchmode` 给新进程。

这个新启动的后端进程会通过下面的代码将 `identifier_case_switch` 信息写入 `pg_control` 文件：

```
BootstrapModeMain() -> BootStrapXLOG();
    /* save database compatible level value */
    ControlFile->dbmode = bootstrap_database_mode;
    ControlFile->casemode = identifier_case_switch;

    /* some additional ControlFile fields are set in WriteControlFile() */
    WriteControlFile();
```

当用户使用 `pg_ctl` 命令启动数据库时，`postmaster` 进程会读取 `pg_control` 文件的内容，代码调用路径为：

```
PostmasterMain()-->SetCaseGucOption()-->GetCaseSwitchModeFromControl()
```

读取到参数值后调用 `SetConfigOption()` 函数进行赋值。

在每个新的后端进程开始的时候，由于是从 `postmaster` 进程 `fork` 而来，会自动拥有相同的 `ivorysql.identifier_case_switch` 参数值。首先处理 `startup` 包，其中如果包含 `database` 或者 `user` 这两个参数，则根据 `identifier_case_switch` 对参数值做相应的处理。

源代码为：

```
BackendMain()->BackendInitialize()-->ProcessStartupPacket()
```

另外，在处理用户的 SQL 语句时，如果包含标识符，也会进行同样的处理，代码分布在： SplitIdentifierString()，quoteOneName() 和 SplitGUCList() 这几个函数中。
