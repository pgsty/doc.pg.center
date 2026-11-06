---
title: "使用 PL/R"
description: "PL/R 是一种过程语言，允许使用 R 编程语言编写 Apache Cloudberry 函数。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-r.md"
---

使用 PL/R 扩展，可以直接在数据库中执行 R 命令、使用 R 模块和函数并执行分析。

## 启用 PL/R {#enable-plr}

要使用 PL/R，必须先确保系统中已安装 R，然后在数据库中注册 PL/R 语言。

### 安装 R {#install-r}

必须在 Apache Cloudberry 集群的所有主机（Coordinator 和 Segment）上安装 R。

1. 使用系统的软件包管理器安装 R。

    对于 Debian/Ubuntu 系统：

    ```bash
    sudo apt update && sudo apt install r-base
    ```

    对于 RHEL/Rocky Linux 系统：

    ```bash
    sudo yum install R
    ```

2. 配置 `R_HOME` 环境变量。

    查找 R 主目录：

    ```bash
    R RHOME
    # Example output: /usr/lib/R
    ```

    在所有主机的 `$GPHOME/greenplum_path.sh` 中添加 `R_HOME` 变量：

    ```bash
    export R_HOME=/usr/lib/R
    ```

3. 加载更新后的路径文件并重启数据库。

    ```bash
    source $GPHOME/greenplum_path.sh
    gpstop -r
    ```

### 注册 PL/R 扩展 {#register-plr-extension}

PL/R 是不受信任的语言，因此只有超级用户可以注册它。请在需要使用它的每个数据库中启用该语言：

```sql
CREATE EXTENSION plr;
```

## 示例 {#examples}

以下示例演示如何使用 PL/R 执行各种任务。

### 示例 1：使用简单的 R 函数 {#example-1-use-simple-r-functions}

此函数使用 R 函数 `rnorm()` 生成服从正态分布的数字数组。

```sql
CREATE OR REPLACE FUNCTION r_norm(n integer, mean float8, std_dev float8) 
RETURNS float8[] 
AS $$
  x <- rnorm(n, mean, std_dev)
  return(x)
$$ LANGUAGE plr;
```

在查询中使用该函数：

```sql
SELECT r_norm(10, 0, 1) as x 
FROM generate_series(1, 10);
```

### 示例 2：返回 DataFrame {#example-2-return-dataframes}

如果 R 函数返回 `data.frame`，必须在数据库中定义相应的复合类型，或使用 `RECORD`。

1. 创建与 `data.frame` 结构匹配的类型：
   ```sql
   CREATE TYPE t_result AS (name text, value float8);
   ```

2. 定义返回所创建类型 `SETOF` 的 PL/R 函数：
   ```sql
   CREATE OR REPLACE FUNCTION get_data() 
   RETURNS SETOF t_result 
   AS $$
     names <- c("A", "B", "C")
     values <- c(1.1, 2.2, 3.3)
     return(data.frame(names, values))
   $$ LANGUAGE plr;
   ```

3. 调用该函数：
   ```sql
   SELECT * FROM get_data();
   ```

## 安装 R 软件包 {#install-r-packages}

可以通过安装其他 R 软件包扩展 PL/R 的功能。这些软件包必须安装在集群的**所有主机**上。

1. 从 CRAN 下载软件包源文件（`.tar.gz`）。
2. 将文件复制到所有主机。
3. 使用 `R CMD INSTALL` 安装软件包。

    ```bash
    # Example for the 'arm' package
    gpssh -f all_hosts "$R_HOME/bin/R CMD INSTALL arm_1.5-03.tar.gz"
    ```

4. 验证能否在 PL/R 中加载该软件包：

    ```sql
    CREATE OR REPLACE FUNCTION check_pkg(pkgname text) 
    RETURNS boolean 
    AS $$
        return(require(pkgname, character.only=TRUE))
    $$ LANGUAGE plr;

    SELECT check_pkg('arm');
    ```

## 显示 R 库信息 {#display-r-library-information}

可以使用 R 命令或 PL/R 函数检查已安装的软件包和库。

通过 PL/R 列出已安装的软件包：

```sql
CREATE OR REPLACE FUNCTION list_packages() 
RETURNS text[] 
AS $$
  return(rownames(installed.packages()))
$$ LANGUAGE plr;

SELECT list_packages();
```
