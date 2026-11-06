---
title: "Create and configure the gpadmin User"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/create-gpadmin-user.md"
---

## Install `sudo` & `git` (if missing) {#install-sudo--git-if-missing}

If `sudo` & `git` command is not already installed, run the following command to install it:

```bash {tab="For Rocky Linux 8+"}
dnf install -y sudo git
```
```bash {tab="For Ubuntu 22.04+"}
apt update && apt install -y sudo git
```

> [!NOTE]
> In environments like Docker, the `root` user will be able to use `sudo` without a password prompt once it is installed.

## Create and configure the `gpadmin` user {#create-and-configure-the-gpadmin-user}

To prepare the environment for Apache Cloudberry development, we need to create and configure a dedicated `gpadmin` user.

1. Create a user 'gpadmin' with matching group, home directory, and bash shell:

    ```bash
    sudo useradd -U -m -s /bin/bash gpadmin
    ```

2. Grant password-less sudo access to `gpadmin`:

    ```bash
    echo 'gpadmin ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/90-gpadmin
    ```

3. Verify the `gpadmin` user setup:

    ```bash
    sudo -u gpadmin sudo whoami
    ```

    If the output is `root`, the configuration is correct.

## Required configuration {#required-configuration}

This script performs three main tasks as the `gpadmin` user:

- Updates `.bashrc` to source Cloudberry environment variables
- Sets up SSH key pair for passwordless login (if not already present)
- Configures proper SSH directory permissions for security

The script uses a heredoc (EOF) block to execute multiple commands under the `gpadmin` user context. This will be used multiple time throughout these instructions.

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
