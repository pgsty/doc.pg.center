---
title: 本地开发与构建
linkTitle: 本地构建
description: 在 Linux、macOS 和 Windows 上从源码构建、测试并运行 OrioleDB。
weight: 20
type: docs
search_keywords: ["OrioleDB", "local builds", "build from source", "源码编译"]
upstream_link: https://www.orioledb.com/docs/contributing/local-builds
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-hammer
---


本指南帮助你在本地机器上从源码构建并运行 OrioleDB。

## Linux {#linux}

### 安装依赖 {#install-prerequisites}

``` bash
sudo apt-get update
sudo apt install git build-essential flex bison pkg-config libreadline-dev make gdb libipc-run-perl libicu-dev python3 python3-dev python3-pip python3-setuptools python3-testresources libzstd1 libzstd-dev valgrind libssl-dev libcurl4-openssl-dev wget
```

### 下载带补丁的 PostgreSQL 17 {#download-and-install-postgresql-17-with-patches}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### 切换到所需补丁集 {#checkout-to-required-patchset}

始终从 [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) 读取必须检出的提交或 `patches17_N` 标签，在这里写死具体值会过时。构建过程会检查补丁集，使用其他版本将拒绝编译。

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### 启用 PostgreSQL 的 Valgrind 支持（可选） {#enable-valgrind-support-in-postgresql-code-optional}

``` bash
sed -i.bak "s/\/\* #define USE_VALGRIND \*\//#define USE_VALGRIND/g" src/include/pg_config_manual.h
```

### 配置与构建 {#configure-and-build}

``` bash
PG_PREFIX=$HOME/pg17
./configure --enable-debug --enable-cassert --enable-tap-tests --with-icu --prefix=$PG_PREFIX
make -j$(nproc)
make -j$(nproc) install
make -C contrib -j$(nproc)
make -C contrib -j$(nproc) install
echo "export PATH=\"$PG_PREFIX/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

### 安装 Python 依赖 {#install-python-requirements}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### 下载并构建 OrioleDB 扩展 {#download-and-build-the-orioledb-extension}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### 下载并安装 Visual Studio Code {#download-and-install-visual-studio-code}

``` bash
cd ..
wget --content-disposition "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
sudo apt install ./code_*.deb
# Install Python and C++ extension
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code orioledb
```

### 检查安装 {#check-installation}

#### 运行自动化测试 {#run-automated-tests}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### 手动安装与运行 {#manual-installation-and-running}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
sed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```

## MacOS {#macos}

### 禁用系统完整性保护 {#disable-system-integrity-protection}

按照[禁用系统完整性保护的说明](http://osxdaily.com/2015/10/05/disable-rootless-system-integrity-protection-mac-os-x/)操作。

### 安装 Homebrew {#install-homebrew}

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 安装依赖 {#install-prerequisites-1}

``` bash
brew install python zstd pkg-config icu4c openssl wget gnu-sed
sudo cpan IPC::Run
echo "export PKG_CONFIG_PATH=\"\$PKG_CONFIG_PATH:$(brew --prefix icu4c)/lib/pkgconfig\"" >> ~/.zshrc

# For Intel chip devices
echo "export CFLAGS=\"$CFLAGS -I/usr/local/include\"" >> ~/.zshrc
echo "export LDFLAGS=\"$LDFLAGS -L/usr/local/lib\"" >> ~/.zshrc
#

# For Apple M chip devices
echo "export CFLAGS=\"$CFLAGS -I/opt/homebrew/include\"" >> ~/.zshrc
echo "export LDFLAGS=\"$LDFLAGS -L/opt/homebrew/lib\"" >> ~/.zshrc
#

exec zsh -l
```

### 下载带补丁的 PostgreSQL 17 {#download-and-install-postgresql-17-with-patches-1}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### 切换到所需补丁集 {#checkout-to-required-patchset-1}

始终从 [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) 读取必须检出的提交或 `patches17_N` 标签，在这里写死具体值会过时。构建过程会检查补丁集，使用其他版本将拒绝编译。

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### 配置与构建 {#configure-and-build-1}

``` bash
PG_PREFIX=$HOME/pg17
./configure --enable-debug --enable-cassert --enable-tap-tests --with-icu --prefix=$PG_PREFIX
make -j$(nproc)
make -j$(nproc) install
make -C contrib -j$(nproc)
make -C contrib -j$(nproc) install
echo "export PATH=\"$PG_PREFIX/bin:\$PATH\"" >> ~/.zshrc
exec zsh -l
```

### 安装 Python 依赖 {#install-python-requirements-1}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### 下载并构建 OrioleDB 扩展 {#download-and-build-the-orioledb-extension-1}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### 下载并安装 Visual Studio Code {#download-and-install-visual-studio-code-1}

``` bash
cd ..
brew install --cask visual-studio-code
exec zsh -l
# Install Python and C++ extension
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code orioledb
```

### 检查安装 {#check-installation-1}

#### 运行自动化测试 {#run-automated-tests-1}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### 手动安装与运行 {#manual-installation-and-running-1}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
gsed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```

## Windows {#windows}

### 在 WSL 中安装 Ubuntu {#install-ubuntu-in-wsl}

``` bat
wsl --install -d Ubuntu
```

然后重启，从开始菜单启动 Ubuntu，设置用户名和密码。

``` bat
wsl --shutdown
```

再次从开始菜单启动 Ubuntu。

### 安装依赖 {#install-prerequisites-2}

``` bash
sudo hwclock --hctosys
sudo apt-get update
sudo apt install git build-essential flex bison pkg-config libreadline-dev make gdb libipc-run-perl libicu-dev python3 python3-dev python3-pip python3-setuptools python3-testresources libzstd1 libzstd-dev valgrind libssl-dev libcurl4-openssl-dev wget
```

### 下载带补丁的 PostgreSQL 17 {#download-and-install-postgresql-17-with-patches-2}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### 切换到所需补丁集 {#checkout-to-required-patchset-2}

始终从 [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) 读取必须检出的提交或 `patches17_N` 标签，在这里写死具体值会过时。构建过程会检查补丁集，使用其他版本将拒绝编译。

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### 启用 PostgreSQL 的 Valgrind 支持（可选） {#enable-valgrind-support-in-postgresql-code-optional-1}

``` bash
sed -i.bak "s/\/\* #define USE_VALGRIND \*\//#define USE_VALGRIND/g" src/include/pg_config_manual.h
```

### 配置与构建 {#configure-and-build-2}

``` bash
PG_PREFIX=$HOME/pg17
./configure --enable-debug --enable-cassert --enable-tap-tests --with-icu --prefix=$PG_PREFIX
make -j$(nproc)
make -j$(nproc) install
make -C contrib -j$(nproc)
make -C contrib -j$(nproc) install
echo "export PATH=\"$PG_PREFIX/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

### 安装 Python 依赖 {#install-python-requirements-2}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### 下载并构建 OrioleDB 扩展 {#download-and-build-the-orioledb-extension-2}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### 下载并安装 Visual Studio Code {#download-and-install-visual-studio-code-2}

<https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user>

### 安装 VSCode 的 Python 和 C++ 扩展 {#install-python-and-c-vscode-extensions}

``` bat
code --install-extension ms-vscode-remote.remote-wsl
code --remote wsl+ubuntu /home/USERNAME/orioledb
```

在 VSCode 终端中执行：

``` bash
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
```

### 检查安装 {#check-installation-2}

#### 运行自动化测试 {#run-automated-tests-2}

``` bash
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### 手动安装与运行 {#manual-installation-and-running-2}

``` bash
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
sed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```
