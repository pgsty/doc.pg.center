---
title: "使用 PGRX 开发数据库扩展"
description: "本文介绍如何使用 Rust 和 PGRX 框架开发数据库扩展。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/develop-extensions-using-rust.md"
---

PGRX 是一个用于为 Apache Cloudberry 开发扩展的 Rust 框架，可提供安全高效的开发体验。

有关 PGRX 的核心功能，请参阅 [PGRX 核心功能](#pgrx-core-features)。有关 PGRX 的注意事项，请参阅 [PGRX 的注意事项和最佳实践](#considerations-and-best-practices-for-pgrx)。

## 开发环境要求 {#requirements-for-development-environment}

- 确保操作系统为 Debian/Ubuntu 或 RHEL/CentOS。
- 确保 Apache Cloudberry 集群由源代码编译而来，而不是使用 RPM 软件包安装。

### 基本软件环境 {#basic-software-environment}

所需软件：

- Rust 工具链（`rustc`、`cargo` 和 `rustfmt`），通过 https://rustup.rs 安装
- Git
- libclang 11 或更高版本（用于 bindgen）
- GCC 7 或更高版本

### PostgreSQL 依赖项 {#postgresql-dependencies}

根据操作系统安装所需的 PostgreSQL 依赖项：

对于 Debian/Ubuntu：

```bash
sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison \
    libxml2-dev libxslt-dev libssl-dev libxml2-utils xsltproc ccache pkg-config
```

对于 RHEL/CentOS：

```bash
sudo yum install -y bison-devel readline-devel zlib-devel openssl-devel wget ccache
sudo yum groupinstall -y 'Development Tools'
```

安装依赖项后，即可开始开发扩展。

## PGRX 快速入门 {#quick-start-for-pgrx}

本节介绍使用 PGRX 快速开发扩展的过程，包括：

- 设置并安装 PGRX
- 创建扩展
- 安装和使用扩展

### 设置并安装 PGRX {#set-up-and-install-pgrx}
> [!NOTE]
> PGRX 由 PgCentral Foundation, Inc. 维护；本文使用的是一个[分叉的 PGRX 版本](https://github.com/cloudberry-contrib/pgrx)，与 Cloudberry 具有更好的兼容性。该版本由社区成员贡献并针对 Cloudberry 定制，但请注意，它不是由 Cloudberry 官方项目维护的版本。
1. 设置 Apache Cloudberry 的 `pg_config` 路径环境变量，其中 `<pg_config_path>` 是 Apache Cloudberry 集群中的路径（例如 `/usr/local/cloudberry-db/bin/pg_config`）：

   ```bash
   export PGRX_PG_CONFIG_PATH=<pg_config_path>
   ```

2. 构建 PGRX 框架：

   1. 克隆与 Apache Cloudberry 兼容的 `pgrx` 仓库：

      ```bash
      git clone https://github.com/cloudberry-contrib/pgrx
      cd pgrx
      ```

   2. 启用 `pg14` 和 `cbdb` 功能构建代码：

      ```bash
      cargo build --features "pg14, cbdb"
      ```

3. 安装与 Apache Cloudberry 兼容的 `cargo-pgrx` 工具：

   ```bash
   cargo install --path cargo-pgrx/
   ```

4. 使用数据库内核版本初始化环境：

   ```bash
   cargo pgrx init --pg14=`which pg_config`
   ```

### 创建扩展 {#create-an-extension}

1. 生成扩展模板。以下示例创建名为 `my_extension` 的扩展：

   ```bash
   cargo pgrx new my_extension
   cd my_extension
   ```

   创建的目录结构如下：

   ```bash
   .
   ├── Cargo.toml
   ├── my_extension.control
   ├── sql
   └── src
      ├── bin
      │   └── pgrx_embed.rs
      └── lib.rs
   ```

2. 修改 `Cargo.toml` 中的依赖以使用本地 PGRX：

   - 将 `[dependencies]` 下的 `pgrx = "0.12.7"` 改为指向本地 PGRX 仓库中的 `pgrx` 目录。例如：

      ```toml
      [dependencies]
      pgrx = { path = "/home/gpadmin/pgrx/pgrx/", features = ["pg14", "cbdb"] }
      ```

   - 在 `[dependencies]` 下添加 `pgrx-pg-sys`，使其指向本地 PGRX 仓库中的 `pgrx-pg-sys` 目录。例如：

      ```toml
      [dependencies]
      pgrx-pg-sys = { path = "/home/gpadmin/pgrx/pgrx-pg-sys/", features = ["pg14", "cbdb"] }
      ```

   - 将 `[dev-dependencies]` 下的 `pgrx-tests = "0.12.7"` 改为指向本地 PGRX 仓库中的 `pgrx-tests` 目录：

      ```toml
      [dev-dependencies]
      pgrx-tests = { path = "/home/gpadmin/pgrx/pgrx-tests/" }
      ```

3. 将扩展名 `my_extension` 追加到本地 PGRX 仓库根目录 `Cargo.toml` 文件的 `workspace.members` 数组中。例如：

   ```bash
   vi /home/gpadmin/pgrx/Cargo.toml
   ```

   ```toml
   [workspace]
   resolver = "2"
   members = [
      "cargo-pgrx",
      "pgrx",
      "pgrx-macros",
      "pgrx-pg-config",
      "pgrx-pg-sys",
      "pgrx-sql-entity-graph",
      "pgrx-tests",
      "pgrx-bindgen",
      "my_extension"
   ]
   ```

4. 为当前系统用户授予访问 Apache Cloudberry 目录的权限。例如，当前用户为 `gpadmin`，Apache Cloudberry 目录为 `/usr/local/cloudberrydb`：

   ```bash
   sudo chown -R gpadmin:gpadmin /usr/local/cloudberrydb
   ```

### 安装和使用扩展 {#install-and-use-the-extension}

1. 安装扩展：

   ```bash
   cargo pgrx install
   ```

2. 要在数据库中使用该扩展，请连接数据库并执行以下语句：

   ```sql
   CREATE EXTENSION my_extension;

   -- Tests example function
   SELECT hello_my_extension();
   ```

## PGRX 类型映射 {#pgrx-type-mapping}

下表列出了 Apache Cloudberry（PostgreSQL）数据类型到 Rust 类型的完整映射：

| 数据库数据类型 | Rust 类型（`Option<T>`） |
|-------------------|------------------------|
| `bytea` | `Vec<u8>` 或 `&[u8]`（零拷贝） |
| `text` | `String` 或 `&str`（零拷贝） |
| `varchar` | `String` 或 `&str`（零拷贝）或 `char` |
| `"char"` | `i8` |
| `smallint` | `i16` |
| `integer` | `i32` |
| `bigint` | `i64` |
| `oid` | `u32` |
| `real` | `f32` |
| `double precision` | `f64` |
| `bool` | `bool` |
| `json` | `pgrx::Json(serde_json::Value)` |
| `jsonb` | `pgrx::JsonB(serde_json::Value)` |
| `date` | `pgrx::Date` |
| `time` | `pgrx::Time` |
| `timestamp` | `pgrx::Timestamp` |
| `time with time zone` | `pgrx::TimeWithTimeZone` |
| `timestamp with time zone` | `pgrx::TimestampWithTimeZone` |
| `anyarray` | `pgrx::AnyArray` |
| `anyelement` | `pgrx::AnyElement` |
| `box` | `pgrx::pg_sys::BOX` |
| `point` | `pgrx::pg_sys::Point` |
| `tid` | `pgrx::pg_sys::ItemPointerData` |
| `cstring` | `&core::ffi::CStr` |
| `numeric` | `pgrx::Numeric<P, S>` 或 `pgrx::AnyNumeric` |
| `void` | `()` |
| `ARRAY[]::<type>` | `Vec<Option<T>>` 或 `pgrx::Array<T>`（零拷贝） |
| `int4range` | `pgrx::Range<i32>` |
| `int8range` | `pgrx::Range<i64>` |
| `numrange` | `pgrx::Range<Numeric<P, S>>` 或 `pgrx::Range<AnyRange>` |
| `daterange` | `pgrx::Range<pgrx::Date>` |
| `tsrange` | `pgrx::Range<pgrx::Timestamp>` |
| `tstzrange` | `pgrx::Range<pgrx::TimestampWithTimeZone>` |
| `NULL` | `Option::None` |
| `internal` | `pgrx::PgBox<T>`（其中 `T` 可以是任意 Rust/Postgres 结构体） |
| `uuid` | `pgrx::Uuid([u8; 16])` |

### 自定义类型转换 {#custom-type-conversions}

可以通过以下方式实现额外的类型转换：

- 实现 `IntoDatum` 和 `FromDatum` trait。
- 使用 `#[derive(PostgresType)]` 和 `#[derive(PostgresEnum)]` 自动转换类型。

### 类型映射详情 {#type-mapping-details}

PGRX 将 `text` 和 `varchar` 转换为 `&str` 或 `String`，并验证编码是否为 UTF-8。如果检测到非 UTF-8 编码，PGRX 会触发 panic 来提醒开发者。由于 UTF-8 验证可能影响性能，因此不建议依赖 UTF-8 验证。

PostgreSQL 服务器的默认编码是 `SQL_ASCII`，它既不能保证 ASCII，也不能保证 UTF-8（Apache Cloudberry 会接受但忽略非 ASCII 字节）。为获得最佳结果，请始终在 PGRX 中使用 UTF-8 编码，并在创建数据库时显式设置数据库编码。

## PGRX 核心功能 {#pgrx-core-features}

### 完整管理开发环境 {#complete-management-for-development-environment}

cargo-pgrx 提供完整的命令行工具集：

- `cargo pgrx new`：快速创建新扩展。
- `cargo pgrx init`：安装或注册 Apache Cloudberry（PostgreSQL）实例。
- `cargo pgrx run`：在 psql（或 pgcli）中交互式测试扩展。
- `cargo pgrx test`：在多个 Apache Cloudberry（PostgreSQL）版本上执行单元测试。
- `cargo pgrx package`：创建扩展安装软件包。

### 自动模式生成 {#automatic-mode-generation}

- 完全使用 Rust 实现扩展。
- 自动将各种 Rust 类型映射为 Apache Cloudberry（PostgreSQL）类型。
- 自动生成 SQL 模式（也可以使用 `cargo pgrx schema` 手动生成）。
- 使用 `extension_sql!` 和 `extension_sql_file!` 引入自定义 SQL。

### 安全优先 {#security-first}

- 将 Rust 的 `panic!` 转换为 Apache Cloudberry/PostgreSQL 的 `ERROR`（中止事务，而不是进程）。
- 内存管理遵循 Rust 的 `DROP` 语义，包括处理 `panic!` 和 `elog(ERROR)` 情况。
- 使用 `#[pg_guard]` 过程宏确保安全性。
- Apache Cloudberry 的 `Datum` 表示为 `Option<T> where T: FromDatum`，NULL 值安全地表示为 `Option::<T>::None`。

### UDF 支持 {#udf-supports}

- 使用 `#[pg_extern]` 注解向 Apache Cloudberry 暴露函数。
- 返回 `pgrx::iter::SetOfIterator<'a, T>`，实现 `RETURNS SETOF`。
- 返回 `pgrx::iter::TableIterator<'a, T>`，实现 `RETURNS TABLE (...)`。
- 使用 `#[pg_trigger]` 创建触发器函数。

### 简单自定义类型 {#simple-custom-types}

- 使用 `#[derive(PostgresType)]` 将 Rust 结构体作为 Apache Cloudberry 类型处理。
  - 默认使用 CBOR 编码存储，使用 JSON 作为人类可读格式。
  - 支持自定义内存、磁盘和可读格式。
- 使用 `#[derive(PostgresEnum)]` 将 Rust 枚举作为 Apache Cloudberry（PostgreSQL）枚举处理。
- 通过 `pgrx::composite_type!("Sample")` 宏支持复合类型。

### 服务器编程接口（SPI） {#server-programming-interface-spi}

- 安全访问 SPI。
- 透明地从 SPI 上下文返回 Datum 的所有权。

### 高级功能 {#advanced-features}

- 通过 `pgrx::PgMemoryContexts` 安全访问 Apache Cloudberry 的内存上下文系统。
- 支持执行器、规划器、事务和子事务钩子。
- 使用 `pgrx::PgBox<T>`（类似于 `alloc::boxed::Box<T>`）安全处理 Apache Cloudberry 指针。
- 使用 `#[pg_guard]` 过程宏保护传给 Apache Cloudberry `extern "C"` 的 Rust 函数。
- 通过 `eprintln!` 宏访问 Apache Cloudberry 的日志系统。
- 通过 `pgrx::pg_sys` 模块直接（不安全地）访问 Apache Cloudberry 内部实现。

## PGRX 的注意事项和最佳实践 {#considerations-and-best-practices-for-pgrx}

线程支持：

- Apache Cloudberry 严格遵循单线程模型。
- 自定义线程不能调用内部数据库函数。
- 异步上下文的交互方式仍在探索中。

编码要求：

- 建议使用 UTF-8 编码。
- 服务器默认编码为 SQL_ASCII。
- 建议在创建数据库时显式设置编码。

## 调试和开发提示 {#debugging-and-development-tips}

- 使用 `cargo pgrx test` 进行单元测试。
- 使用 `#[pg_guard]` 确保内存安全。
- 对于自定义类型，使用适当的序列化方法。

## PGRX 学习资源 {#learning-resources-for-pgrx}

以下资源可以帮助你深入了解 PGRX：

- 了解所有可用的 `cargo-pgrx` 子命令和选项：[cargo-pgrx 命令详情](https://github.com/cloudberry-contrib/pgrx/blob/main/cargo-pgrx)
- 了解如何定义和使用自定义数据类型：[自定义类型示例](https://github.com/cloudberry-contrib/pgrx/blob/main/pgrx-examples/custom_types)
- 探索如何实现自定义操作符：[操作符函数和操作符类/族](https://github.com/cloudberry-contrib/pgrx/blob/main/pgrx-examples/operators)
- 了解如何使用共享内存：[共享内存支持](https://github.com/cloudberry-contrib/pgrx/blob/main/pgrx-examples/shmem)
- 浏览示例代码实现：[更多示例代码](https://github.com/cloudberry-contrib/pgrx/blob/main/pgrx-examples)
