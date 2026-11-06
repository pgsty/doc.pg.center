---
title: "创建并配置 gpadmin 用户"
description: "为开发环境创建并配置 gpadmin 用户、sudo 权限、Cloudberry 环境和 SSH 认证。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/create-gpadmin-user.md"
---

## 安装 `sudo` 和 `git`（如果尚未安装） {#install-sudo--git-if-missing}

如果尚未安装 `sudo` 和 `git` 命令，请运行以下命令安装：

```bash {tab="适用于 Rocky Linux 8+"}
dnf install -y sudo git
```
```bash {tab="适用于 Ubuntu 22.04+"}
apt update && apt install -y sudo git
```

> [!NOTE] 注意
> 在 Docker 等环境中，安装 `sudo` 后，`root` 用户即可使用它，且无需输入密码。

## 创建并配置 `gpadmin` 用户 {#create-and-configure-the-gpadmin-user}

为准备 Apache Cloudberry 开发环境，需要创建并配置专用的 `gpadmin` 用户。

1. 创建名为 gpadmin 的用户，同时创建同名组和主目录，并将其 shell 设为 bash：

    ```bash
    sudo useradd -U -m -s /bin/bash gpadmin
    ```

2. 授予 `gpadmin` 免密 sudo 权限：

    ```bash
    echo 'gpadmin ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/90-gpadmin
    ```

3. 验证 `gpadmin` 用户配置：

    ```bash
    sudo -u gpadmin sudo whoami
    ```

    如果输出为 `root`，则配置正确。

## 必要配置 {#required-configuration}

以下脚本以 `gpadmin` 用户身份执行三项主要任务：

- 更新 `.bashrc`，使其加载 Cloudberry 环境变量。
- 配置用于免密登录的 SSH 密钥对（如果尚不存在）。
- 为 SSH 目录设置适当的权限，以确保安全。

脚本通过 heredoc（EOF）块，以 `gpadmin` 用户身份执行多条命令。后续说明中也会多次使用这种方式。

```bash {tab="Apache Cloudberry 2.1.0+"}
sudo -u gpadmin bash <<'EOF'
# Add Cloudberry environment setup to .bashrc
echo -e '\n# Add Cloudberry entries
if [ -f /usr/local/cloudberry-db/cloudberry-env.sh ]; then
  source /usr/local/cloudberry-db/cloudberry-env.sh
fi

# US English with UTF-8 character encoding
export LANG=en_US.UTF-8
' >> /home/gpadmin/.bashrc

# Set up SSH for passwordless access
mkdir -p /home/gpadmin/.ssh
if [ ! -f /home/gpadmin/.ssh/id_rsa ]; then
  ssh-keygen -t rsa -b 2048 -C 'apache-cloudberry-dev' -f /home/gpadmin/.ssh/id_rsa -N ""
fi
cat /home/gpadmin/.ssh/id_rsa.pub >> /home/gpadmin/.ssh/authorized_keys

# Set proper SSH directory permissions
chmod 700 /home/gpadmin/.ssh
chmod 600 /home/gpadmin/.ssh/authorized_keys
chmod 644 /home/gpadmin/.ssh/id_rsa.pub
EOF
```
```bash {tab="Apache Cloudberry 2.0.0"}
sudo -u gpadmin bash <<'EOF'
# Add Cloudberry environment setup to .bashrc
echo -e '\n# Add Cloudberry entries
if [ -f /usr/local/cloudberry-db/greenplum_path.sh ]; then
  source /usr/local/cloudberry-db/greenplum_path.sh
fi

# US English with UTF-8 character encoding
export LANG=en_US.UTF-8
' >> /home/gpadmin/.bashrc

# Set up SSH for passwordless access
mkdir -p /home/gpadmin/.ssh
if [ ! -f /home/gpadmin/.ssh/id_rsa ]; then
  ssh-keygen -t rsa -b 2048 -C 'apache-cloudberry-dev' -f /home/gpadmin/.ssh/id_rsa -N ""
fi
cat /home/gpadmin/.ssh/id_rsa.pub >> /home/gpadmin/.ssh/authorized_keys

# Set proper SSH directory permissions
chmod 700 /home/gpadmin/.ssh
chmod 600 /home/gpadmin/.ssh/authorized_keys
chmod 644 /home/gpadmin/.ssh/id_rsa.pub
EOF
```
