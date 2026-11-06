---
title: "配置 Apache Cloudberry 构建"
description: "准备 Python 源码包，并为 Rocky Linux 或 Ubuntu 配置 Apache Cloudberry 构建。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/configure.md"
---

## 为 `--with-pythonsrc-ext` 预先准备 Python 软件包 {#pre-stage-the-python-packages-for---with-pythonsrc-ext}

> [!NOTE] 注意
> 从 Apache Cloudberry 2.2 起才需要执行此步骤。

`--with-pythonsrc-ext` 使用的 Python 源码包未随代码库提供。为遵守 Apache 发布政策，这些源码包从 Apache Cloudberry 2.0 起不再纳入仓库，过去会在构建过程中即时下载。从 Apache Cloudberry 2.2 起，改为在构建前下载，因此请在运行 `configure` 前预先准备好这些源码包。

构建 PyYAML 需要低于 3.0 的 Cython。在 Ubuntu 上，请先安装匹配的发行版软件包：

```bash
# For Ubuntu 22.04, cython3 is 0.29.x
sudo apt install -y cython3

# For Ubuntu 24.04, cython3 is 3.x and cannot build PyYAML, so use cython3-legacy instead
sudo apt install -y cython3-legacy
```

Rocky Linux 8 和 9 已在[安装所需软件包](/cloudberry/build/source/install-required-packages/)步骤中安装 `python3-Cython`。Rocky Linux 10 的发行版只提供 Cython 3.x，因此以下命令会通过 `pip3` 为你安装兼容版本。

然后下载软件包：

```bash
cd ~/cloudberry
make -C gpMgmt/bin download-python-deps
```

## 配置构建流程 {#configure-the-build-process}

{{< tabs >}}
{{< tab label="适用于 Rocky Linux 8+" >}}
### 准备环境 {#prepare-environment}

构建过程要求必要的库（例如 Xerces-C）位于配置和运行时所需的位置。使用以下命令准备环境：

```bash
sudo rm -rf /usr/local/cloudberry-db
sudo chmod a+w /usr/local
mkdir -p /usr/local/cloudberry-db/lib
sudo cp -v /usr/local/xerces-c/lib/libxerces-c.so \
           /usr/local/xerces-c/lib/libxerces-c-3.*.so \
           /usr/local/cloudberry-db/lib
sudo chown -R gpadmin:gpadmin /usr/local/cloudberry-db
```

### 运行 `configure` {#run-configure}

`configure` 命令会为 Apache Cloudberry 设置构建环境，其中包括若干开发功能和扩展。

> [!NOTE] 注意
> 从 Apache Cloudberry 2.2 起，可以使用新的扩展，包括 `diskquota`、`gp_stats_collector` 和 `yezzey`。使用对应的 `configure` 选项启用这些扩展。

```bash {tab="Cloudberry 2.2"}
cd ~/cloudberry
export LD_LIBRARY_PATH=/usr/local/cloudberry-db/lib:${LD_LIBRARY_PATH:-""}
./configure --prefix=/usr/local/cloudberry-db \
            --disable-external-fts \
            --enable-gpcloud \
            --enable-ic-proxy \
            --enable-mapreduce \
            --enable-orafce \
            --enable-orca \
            --enable-pax \
            --disable-pxf \
            --enable-tap-tests \
            --with-diskquota \
            --with-gp-stats-collector \
            --with-gssapi \
            --with-ldap \
            --with-libxml \
            --with-lz4 \
            --with-pam \
            --with-perl \
            --with-pgport=5432 \
            --with-python \
            --with-pythonsrc-ext \
            --with-ssl=openssl \
            --with-uuid=e2fs \
            --with-yezzey \
            --with-includes=/usr/local/xerces-c/include \
            --with-libraries=/usr/local/cloudberry-db/lib
```
```bash {tab="Cloudberry 2.0/2.1"}
cd ~/cloudberry
export LD_LIBRARY_PATH=/usr/local/cloudberry-db/lib:${LD_LIBRARY_PATH:-""}
./configure --prefix=/usr/local/cloudberry-db \
            --disable-external-fts \
            --enable-gpcloud \
            --enable-ic-proxy \
            --enable-mapreduce \
            --enable-orafce \
            --enable-orca \
            --enable-pax \
            --disable-pxf \
            --enable-tap-tests \
            --with-gssapi \
            --with-ldap \
            --with-libxml \
            --with-lz4 \
            --with-pam \
            --with-perl \
            --with-pgport=5432 \
            --with-python \
            --with-pythonsrc-ext \
            --with-ssl=openssl \
            --with-uuid=e2fs \
            --with-includes=/usr/local/xerces-c/include \
            --with-libraries=/usr/local/cloudberry-db/lib
```
{{< /tab >}}
{{< tab label="适用于 Ubuntu 22.04+" >}}
### 准备环境 {#prepare-environment-1}

使用以下命令准备环境：

```bash
sudo rm -rf /usr/local/cloudberry-db
sudo chmod a+w /usr/local
mkdir -p /usr/local/cloudberry-db
sudo chown -R gpadmin:gpadmin /usr/local/cloudberry-db
```

### 运行 `configure` {#run-configure-1}

`configure` 命令会为 Apache Cloudberry 设置构建环境，其中包括若干开发功能和扩展。

> [!NOTE] 注意
> 从 Apache Cloudberry 2.2 起，可以使用新的扩展，包括 `diskquota`、`gp_stats_collector` 和 `yezzey`。使用对应的 `configure` 选项启用这些扩展。

```bash {tab="Cloudberry 2.2"}
cd ~/cloudberry
./configure --prefix=/usr/local/cloudberry-db \
            --disable-external-fts \
            --enable-gpcloud \
            --enable-ic-proxy \
            --enable-mapreduce \
            --enable-orafce \
            --enable-orca \
            --enable-pax \
            --disable-pxf \
            --enable-tap-tests \
            --with-diskquota \
            --with-gp-stats-collector \
            --with-gssapi \
            --with-ldap \
            --with-libxml \
            --with-lz4 \
            --with-pam \
            --with-perl \
            --with-pgport=5432 \
            --with-python \
            --with-pythonsrc-ext \
            --with-ssl=openssl \
            --with-uuid=e2fs \
            --with-yezzey \
            --with-includes=/usr/include/xercesc
```
```bash {tab="Cloudberry 2.0/2.1"}
cd ~/cloudberry
./configure --prefix=/usr/local/cloudberry-db \
            --disable-external-fts \
            --enable-gpcloud \
            --enable-ic-proxy \
            --enable-mapreduce \
            --enable-orafce \
            --enable-orca \
            --enable-pax \
            --disable-pxf \
            --enable-tap-tests \
            --with-gssapi \
            --with-ldap \
            --with-libxml \
            --with-lz4 \
            --with-pam \
            --with-perl \
            --with-pgport=5432 \
            --with-python \
            --with-pythonsrc-ext \
            --with-ssl=openssl \
            --with-uuid=e2fs \
            --with-includes=/usr/include/xercesc
```
{{< /tab >}}
{{< /tabs >}}

## `configure` 选项 {#configure-options}

`configure` 脚本用于准备 Apache Cloudberry 构建环境。它会检查所需的库，并设置必要的配置选项。

可以运行 `./configure --help` 查看可用于配置 Apache Cloudberry 的完整选项列表。下面列出常用选项及其描述和说明。

> [!NOTE] 注意
> 构建依赖项取决于配置时启用或禁用的功能。虽然[上一节](/cloudberry/build/source/install-required-packages/)列出了基本必需软件包，但根据配置选择，你可能还需要其他软件包。运行 `./configure` 时，它会检查并报告缺失的依赖项；必须安装这些依赖项后才能继续构建。
>
> 此外，不同 Linux 发行版的软件包名称可能不同。

| 选项 | 描述 | 说明 |
|--|--|--|
| `--prefix=PREFIX` | 安装目录。默认值为 `/usr/local/cbdb`。`make install` 会将所有文件安装到 `/usr/local/cbdb/bin`、`/usr/local/cbdb/lib` 等目录。 | 可以使用 `--prefix` 指定不同于 `/usr/local/cbdb` 的安装前缀。本指南使用 `/usr/local/cloudberry-db` 作为安装目录。 |
| `--disable-gpfdist` | 不使用 gpfdist。 | 默认启用 gpfdist。这要求安装 apr 库和 libevent。 |
| `--disable-pxf` | 不构建 PXF。 | 默认启用 PXF。PXF 是查询联邦引擎，可访问 Hadoop、Hive、HBase、关系数据库、S3、Google Cloud Storage 等外部系统中的数据。现在，[cloudberry-pxf](https://github.com/apache/cloudberry-pxf/tree/main/fdw) 将作为 `pxf_fdw` 的最新版本维护。 |
| `--enable-orafce` | 构建 Oracle 兼容函数。 | |
| `--enable-debug` | 为所有程序和库生成调试符号。 | 这样可以在调试器中运行程序，分析问题。这会显著增大已安装可执行文件的体积；对于非 GCC 编译器，通常还会禁用编译器优化，导致运行变慢。不过，保留符号对排查可能出现的问题非常有帮助。目前，只有使用 GCC 时才建议在生产安装中启用此选项；进行开发或运行 beta 版本时则应始终启用。 |
| `--enable-profiling` | 构建时启用性能分析。 | 此选项仅限使用 GCC 进行开发时使用。 |
| `--enable-tap-tests` | 启用使用 Perl TAP 工具的测试。 | 这要求安装 `Perl` 和 Perl 模块 `IPC::Run`。 |
| `--enable-cassert` | 启用断言检查（用于调试）。 | 在服务器中启用断言检查，检查许多“本不应发生”的情况。这对代码开发非常有价值，但这些检查可能显著降低服务器的运行速度。不建议在生产环境中使用此选项；进行开发或运行 beta 版本时应启用。 |
| `--disable-orca` | 禁用 ORCA 优化器。 | ORCA 默认启用。ORCA 要求安装 xerces-c 库。 |
| `--enable-mapreduce` | 启用 Cloudberry MapReduce 支持。 | 这要求安装 libyaml。 |
| `--enable-gpcloud` | 启用 gpcloud 支持。 | |
| `--enable-external-fts` | 启用外部 FTS 支持。 | |
| `--enable-ic-proxy` | 启用 Interconnect 代理模式。 | 这要求安装 libuv 库。 |
| `--enable-pax` | 启用 PAX 支持。 | 需要 gcc/gcc-c++ 11+、cmake3、protobuf 和 ZSTD，详见[这里](https://github.com/apache/cloudberry/blob/main/contrib/pax_storage/doc/README.md#build)。 |
| `--with-includes=DIRS` | 在 DIRS 中查找其他头文件。 | 使用 ORCA 构建时需要 Xerces-C。 |
| `--with-libraries=DIRS` | 在 DIRS 中查找其他库。 | 使用 ORCA 构建时需要 xerces-c 库。 |
| `--with-pgport=PORTNUM` | 设置默认端口号 [5432]。 | 本指南使用 `--with-pgport=5432`。 |
| `--with-llvm` | 启用基于 LLVM 的 JIT 支持。 | 这要求安装 LLVM 库。 |
| `--with-icu` | 构建 ICU 支持。 | 这要求安装 ICU4C 软件包。 |
| `--with-perl` | 构建 Perl 模块（PL/Perl）。 | 这要求安装 Perl 开发软件包。 |
| `--with-python` | 构建 Python 模块（PL/Python）。 | 这要求安装 Python3 开发软件包。 |
| `--with-pythonsrc-ext` | 为 gpMgmt 构建 Python 模块。 | 推荐启用此选项，供 gpMgmt 工具使用。此选项要求安装 `curl`、`python3` 和 `python3-pip`；`curl` 用于下载所需的 Python3 软件包，`python3-pip` 用于安装构建 PyYAML 所需的 Python 软件包。如果不使用此选项构建，安装 Cloudberry 后需要从 Linux 发行版安装指定的 Python 软件包：`psutil`、`pygresql`、`pyyaml`，或者在顶层目录运行 `pip3 install -r python-dependencies.txt`。 |
| `--with-gssapi` | 构建 GSSAPI 支持。 | GSSAPI 系统通常属于 Kerberos 安装的一部分，因此需要安装 krb5 软件包。 |
| `--with-pam` | 构建 PAM（可插拔认证模块）支持。 | 这要求安装 PAM 软件包。 |
| `--with-ldap` | 构建 LDAP 支持，用于认证和连接参数查找。 | 这要求安装 OpenLDAP 软件包。 |
| `--with-uuid=LIB` | 使用 LIB（bsd、e2fs、ossp）构建 contrib/uuid-ossp 模块。 | <ul><li>`bsd`：使用 FreeBSD 和某些其他 BSD 衍生系统中的 UUID 函数</li><li>`e2fs`：使用 e2fsprogs 项目创建的 UUID 库；大多数 Linux 系统和 macOS 都提供该库，其他平台也可以获取</li><li>`ossp`：使用 OSSP UUID 库</li></ul>因此，在 Linux/macOS 上构建时使用 `--with-uuid=e2fs`；这要求安装 uuid 库。 |
| `--with-libxml` | 构建 libxml2 支持，从而启用 SQL/XML 支持。 | 这要求安装 libxml2。 |
| `--with-lz4` | 构建 LZ4 压缩支持。 | 可使用 LZ4 压缩表数据；需要安装 lz4 库。 |
| `--with-ssl=LIB` | 构建 SSL（加密）连接支持。 | 唯一支持的 LIBRARY 是 openssl，因此本指南使用 `--with-ssl=openssl`。这要求安装 OpenSSL 软件包。 |
| `--with-diskquota` | 构建 diskquota 扩展。 | Diskquota 为 Apache Cloudberry 中的数据库对象提供磁盘使用量限制。**从 Cloudberry 2.2 起提供**。 |
| `--with-gp-stats-collector` | 构建统计信息收集器扩展。 | 用于收集查询执行指标并报告给外部代理的扩展。**从 Cloudberry 2.2 起提供**。 |
| `--with-yezzey` | 构建 Yezzey 扩展。 | Yezzey 用于将数据从 Cloudberry 转存到兼容 S3 的外部存储。此选项只构建扩展。如果向 S3 发送的请求很少，则不需要代理；但大量并行数据交换流可能耗尽集群主机的 CPU 和网络资源。为在大流量下获得更好性能，还应部署 [YProxy](https://github.com/open-gpdb/yproxy)，它通过连接池管理到 S3 的连接，并调度请求。**从 Cloudberry 2.2 起提供**。 |
