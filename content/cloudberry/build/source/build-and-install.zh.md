---
title: "构建并安装 Apache Cloudberry 及 contrib 扩展"
description: "编译 Apache Cloudberry 及其 contrib 模块，安装二进制文件并验证安装结果。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/build-and-install.md"
---

## 编译代码 {#compile-the-code}

```bash
# Uses the following command to compile the core components of Apache Cloudberry:
make -j$(nproc) --directory=~/cloudberry

# Compiles additional contrib modules, which provide optional features and extensions:
make -j$(nproc) --directory=~/cloudberry/contrib
```

## 安装编译后的二进制文件 {#install-the-compiled-binaries}

```bash
# Installs the core components to the specified installation directory:
make install --directory=~/cloudberry

# Installs the contrib modules to the specified installation directory:
make install --directory=~/cloudberry/contrib
```

## 验证安装 {#verify-installation}

安装后，按以下步骤验证安装结果：

### 1. 检查 Cloudberry 版本 {#1-check-cloudberry-version}

```bash
/usr/local/cloudberry-db/bin/postgres --gp-version
/usr/local/cloudberry-db/bin/postgres --version
```

### 2. 验证库依赖项 {#2-verify-library-dependencies}

```bash
ldd /usr/local/cloudberry-db/bin/postgres
```

### 3. 检查扩展库 {#3-check-library-extensions}

```bash
ls -al /usr/local/cloudberry-db/share/postgresql/extension
```

### 4. 检查核心工具 {#4-check-core-utilities}

```bash
ls -l /usr/local/cloudberry-db/bin/
```
预期输出应显示 postgres、initdb 等关键二进制文件。

## 常见问题 {#common-issues}

- 配置因缺少依赖项而失败：

    1. 确认已安装所有必需的软件包。
    2. 检查 configure 日志文件中的具体错误。
    3. 确认已正确启用 CRB 软件仓库。

- 构建因编译错误而失败：

    1. 检查 make 日志中的具体错误。
    2. 确认系统资源充足。
    3. 确认 Xerces-C 安装正确。

- 库加载问题：

    1. 确认 `LD_LIBRARY_PATH` 包含所需目录。
    2. 检查库权限。

如需查看详细错误消息，请检查安装过程中创建的带有时间戳的日志文件。

你已在 Rocky Linux 9 上成功构建并安装 Apache Cloudberry。安装目录为 `/usr/local/cloudberry-db`。
