---
title: OrioleDB development quickstart
linkTitle: Local builds
description: Build patched PostgreSQL and OrioleDB on Linux and macOS, with debugger and test setup.
weight: 20
type: docs
search_keywords: ["OrioleDB", "local builds", "build from source", "源码编译"]
upstream_link: https://www.orioledb.com/docs/contributing/local-builds
upstream_source: orioledb
upstream_modified: true
upstream_notice: /orioledb/attribution/
icon: fa-solid fa-hammer
---


This guide will help you to build and run OrioleDB on your local machine from the source code.

## Linux {#linux}

### Install prerequisites {#install-prerequisites}

``` bash
sudo apt-get update
sudo apt install git build-essential flex bison pkg-config libreadline-dev make gdb libipc-run-perl libicu-dev python3 python3-dev python3-pip python3-setuptools python3-testresources libzstd1 libzstd-dev valgrind libssl-dev libcurl4-openssl-dev wget
```

### Download and install PostgreSQL 17 with patches {#download-and-install-postgresql-17-with-patches}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### Checkout to required patchset {#checkout-to-required-patchset}

Always read [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) for the commit (or `patches17_N` tag) you must check out — pinning a specific value here would go stale. The build verifies this and refuses to compile against any other patchset.

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### Enable Valgrind support in PostgreSQL code (optional) {#enable-valgrind-support-in-postgresql-code-optional}

``` bash
sed -i.bak "s/\/\* #define USE_VALGRIND \*\//#define USE_VALGRIND/g" src/include/pg_config_manual.h
```

### Configure and build {#configure-and-build}

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

### Install python requirements {#install-python-requirements}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### Download and build the OrioleDB extension {#download-and-build-the-orioledb-extension}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### Download and install Visual Studio Code {#download-and-install-visual-studio-code}

``` bash
cd ..
wget --content-disposition "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
sudo apt install ./code_*.deb
# Install Python and C++ extension
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code orioledb
```

### Check installation {#check-installation}

#### Run automated tests {#run-automated-tests}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### Manual installation and running {#manual-installation-and-running}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
sed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```

## MacOS {#macos}

### Disable System Integrity Protection {#disable-system-integrity-protection}

Follow [the instruction to disable System Integrity Protection](http://osxdaily.com/2015/10/05/disable-rootless-system-integrity-protection-mac-os-x/).

### Install Homebrew {#install-homebrew}

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install prerequisites {#install-prerequisites-1}

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

### Download and install PostgreSQL 17 with patches {#download-and-install-postgresql-17-with-patches-1}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### Checkout to required patchset {#checkout-to-required-patchset-1}

Always read [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) for the commit (or `patches17_N` tag) you must check out — pinning a specific value here would go stale. The build verifies this and refuses to compile against any other patchset.

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### Configure and build {#configure-and-build-1}

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

### Install python requirements {#install-python-requirements-1}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### Download and build the OrioleDB extension {#download-and-build-the-orioledb-extension-1}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### Download and install Visual Studio Code {#download-and-install-visual-studio-code-1}

``` bash
cd ..
brew install --cask visual-studio-code
exec zsh -l
# Install Python and C++ extension
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code orioledb
```

### Check installation {#check-installation-1}

#### Run automated tests {#run-automated-tests-1}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### Manual installation and running {#manual-installation-and-running-1}

``` bash
cd orioledb
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
gsed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```

## Windows {#windows}

### Install ubuntu in WSL {#install-ubuntu-in-wsl}

``` bat
wsl --install -d Ubuntu
```

Then reboot, start Ubuntu from start menu, and choose login/password.

``` bat
wsl --shutdown
```

Start Ubuntu from start menu again.

### Install prerequisites {#install-prerequisites-2}

``` bash
sudo hwclock --hctosys
sudo apt-get update
sudo apt install git build-essential flex bison pkg-config libreadline-dev make gdb libipc-run-perl libicu-dev python3 python3-dev python3-pip python3-setuptools python3-testresources libzstd1 libzstd-dev valgrind libssl-dev libcurl4-openssl-dev wget
```

### Download and install PostgreSQL 17 with patches {#download-and-install-postgresql-17-with-patches-2}

``` bash
git clone https://github.com/orioledb/postgres.git --branch patches17 --single-branch postgres-patches17
cd postgres-patches17/
```

### Checkout to required patchset {#checkout-to-required-patchset-2}

Always read [`.pgtags`](https://github.com/orioledb/orioledb/blob/main/.pgtags) for the commit (or `patches17_N` tag) you must check out — pinning a specific value here would go stale. The build verifies this and refuses to compile against any other patchset.

``` bash
# Pull the value for line "17:" out of orioledb/.pgtags.  It is either
# a commit SHA or a tag name like patches17_14.
PATCHSET=$(curl -fsSL https://raw.githubusercontent.com/orioledb/orioledb/main/.pgtags | awk -F': ' '/^17: /{print $2}')
# Make sure tags are fetched too, in case .pgtags points to a tag.
git fetch --tags origin
git checkout "$PATCHSET"
```

### Enable Valgrind support in PostgreSQL code (optional) {#enable-valgrind-support-in-postgresql-code-optional-1}

``` bash
sed -i.bak "s/\/\* #define USE_VALGRIND \*\//#define USE_VALGRIND/g" src/include/pg_config_manual.h
```

### Configure and build {#configure-and-build-2}

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

### Install python requirements {#install-python-requirements-2}

``` bash
# create venv if needed
python -m venv venv
# activate venv if needed
source ./venv/bin/activate
pip3 install -r requirements.txt
sudo pip3 install compiledb
```

### Download and build the OrioleDB extension {#download-and-build-the-orioledb-extension-2}

``` bash
cd ..
git clone https://github.com/orioledb/orioledb.git
cd orioledb
# Build with compiledb, because it creates compile_commands.json needed for VSCode C/C++ extension
compiledb make USE_PGXS=1 IS_DEV=1
# Exclude compile_commands.json from the Git tracking
echo "compile_commands.json" >> .git/info/exclude
```

### Download and install Visual Studio Code {#download-and-install-visual-studio-code-2}

<https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user>

### Install Python and C++ VSCode extensions {#install-python-and-c-vscode-extensions}

``` bat
code --install-extension ms-vscode-remote.remote-wsl
code --remote wsl+ubuntu /home/USERNAME/orioledb
```

In VSCode terminal:

``` bash
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
```

### Check installation {#check-installation-2}

#### Run automated tests {#run-automated-tests-2}

``` bash
make USE_PGXS=1 IS_DEV=1 installcheck
```

#### Manual installation and running {#manual-installation-and-running-2}

``` bash
make USE_PGXS=1 IS_DEV=1 install
initdb --no-locale -D $HOME/pgdata
sed -i 's/#shared_preload_libraries = '\'''\''/shared_preload_libraries = '\''orioledb'\''/' $HOME/pgdata/postgresql.conf
pg_ctl -D $HOME/pgdata/ start -l $HOME/log
psql -c "CREATE EXTENSION IF NOT EXISTS orioledb; SELECT orioledb_commit_hash();" -d postgres
```
