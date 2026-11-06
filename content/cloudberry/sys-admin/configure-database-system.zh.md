---
title: "配置数据库系统"
description: "服务器配置参数会影响 Apache Cloudberry 的行为。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/configure-database-system.md"
---

这些参数属于 PostgreSQL 的“统一配置（Grand Unified Configuration）”系统，因此有时称为“GUC”。Apache Cloudberry 的大多数服务器配置参数与 PostgreSQL 的配置参数相同，但其中一部分是 Apache Cloudberry 特有的。

## Coordinator 参数和本地参数 {#coordinator-and-local-parameters}

服务器配置文件包含用于配置服务器行为的参数。Apache Cloudberry 的配置文件 `postgresql.conf` 位于数据库实例的数据目录中。

Coordinator 和每个 Segment 实例都有自己的 `postgresql.conf` 文件。有些参数是本地参数：每个 Segment 实例从自己的 `postgresql.conf` 文件中读取该参数的值。应在 Coordinator 和每个 Segment 实例上设置本地参数。

其他参数是 Coordinator 参数，应在 Coordinator 实例上设置。查询运行时，该值会传递给 Segment 实例（某些情况下会被 Segment 实例忽略）。

## 设置配置参数 {#set-configuration-parameters}

许多配置参数会限制修改者，以及可以设置参数的位置或时间。例如，修改某些参数必须使用 Apache Cloudberry 超级用户。其他参数只能在 `postgresql.conf` 文件的系统级别设置，或必须重启系统才能生效。

许多配置参数是会话参数。可以在系统级别、数据库级别、角色级别或会话级别设置会话参数。数据库用户可以在自己的会话中修改大多数会话参数，但有些参数需要超级用户权限。

### 设置本地配置参数 {#set-a-local-configuration-parameter}

要在多个 Segment 上修改本地配置参数，请在每个目标 Segment（包括主 Segment 和镜像 Segment）的 `postgresql.conf` 文件中更新该参数。使用 `gpconfig` 工具可以在所有 Apache Cloudberry 的 `postgresql.conf` 文件中设置参数。例如：

```shell
$ gpconfig -c gp_vmem_protect_limit -v 4096
```

重启 Apache Cloudberry，使配置更改生效：

```shell
$ gpstop -r
```

### 设置 Coordinator 配置参数 {#set-a-coordinator-configuration-parameter}

要设置 Coordinator 配置参数，请在 Apache Cloudberry Coordinator 实例上设置。如果该参数同时也是会话参数，还可以针对特定数据库、角色或会话设置它。如果在多个级别设置同一参数，以粒度最细的级别为准。例如，会话级别覆盖角色级别，角色级别覆盖数据库级别，数据库级别覆盖系统级别。

#### 在系统级别设置参数 {#set-parameters-at-the-system-level}

Coordinator 的 `postgresql.conf` 文件中的参数设置是全系统默认值。设置 Coordinator 参数的步骤如下：

1. 编辑 `$COORDINATOR_DATA_DIRECTORY/postgresql.conf` 文件。
2. 找到要设置的参数，取消其注释（删除前面的 `#` 字符），并输入所需的值。
3. 保存并关闭文件。
4. 对于不需要重启服务器的会话参数，按如下方式加载 `postgresql.conf` 的更改：

    ```shell
    $ gpstop -u
    ```

    对于需要重启服务器的参数更改，按如下方式重启 Apache Cloudberry：

    ```shell
    $ gpstop -r
    ```

#### 在数据库级别设置参数 {#set-parameters-at-the-database-level}

使用 `ALTER DATABASE` 在数据库级别设置参数。例如：

```sql
ALTER DATABASE mydatabase SET search_path TO myschema;
```

在数据库级别设置会话参数后，连接到该数据库的每个会话都会使用该参数设置。数据库级别的设置覆盖系统级别的设置。

#### 在角色级别设置参数 {#set-parameters-at-the-row-level}

使用 `ALTER ROLE` 在角色级别设置参数。例如：

```sql
ALTER ROLE bob SET search_path TO bobschema;
```

在角色级别设置会话参数后，由该角色发起的每个会话都会使用该参数设置。角色级别的设置覆盖数据库级别的设置。

#### 在会话级别设置参数 {#set-parameters-in-a-session-level}

可以在活动数据库会话中使用 `SET` 命令设置任何会话参数。例如：

```sql
SET statement_mem TO '200MB';
```

该参数设置对该会话的剩余时间有效，或持续到执行 `RESET `命令为止。例如：

```sql
RESET statement_mem;
```

会话级别的设置覆盖角色级别的设置。

## 查看服务器配置参数设置 {#view-server-configuration-parameter-settings}

SQL 命令 `SHOW` 可用于查看当前服务器配置参数设置。例如，要查看所有参数的设置：

```shell
$ psql -c 'SHOW ALL;'
```

`SHOW` 只列出 Coordinator 实例的设置。要查看整个系统（包括所有 Segment）中某个参数的值，请使用 `gpconfig` 工具。例如：

```shell
$ gpconfig --show max_connections
```
