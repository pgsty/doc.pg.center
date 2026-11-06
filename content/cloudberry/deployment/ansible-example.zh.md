---
title: "Ansible Playbook 示例"
description: "本示例 Ansible Playbook 将 Apache Cloudberry 软件发行版安装到组成 Apache Cloudberry 系统的各台主机上。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/ansible-example.md"
---

本 Ansible Playbook 展示了如何将[使用 RPM/DEB 软件包安装](/cloudberry/deployment/install_cloudberry/)中描述的任务通过 [Ansible](https://docs.ansible.com) 自动执行。

> [!IMPORTANT] 重要
> 本 Playbook *仅作为示例*，用于说明如何使用 Ansible、Chef 或 Puppet 等部署工具，自动执行 Apache Cloudberry 集群配置和软件安装任务。Apache Cloudberry 社区不为 Ansible 或本示例中的 Playbook 提供支持。

本示例 Playbook 适用于 RHEL/Rocky Linux。它会创建 `gpadmin` 用户，安装 Apache Cloudberry 软件发行版，将已安装软件的所有者和所属组设置为 `gpadmin`，并设置 `gpadmin` 用户的 PAM 安全限制。

可以修改此脚本，使其适用于您的操作系统平台，并执行其他主机配置任务。

以下是使用此 Ansible Playbook 的步骤。

1. 使用包管理器在控制节点上安装 Ansible。有关安装的帮助，请参阅 [Ansible 文档](https://docs.ansible.com)。

2. 配置从控制节点到 Apache Cloudberry 集群所有主机的免密 SSH。可以使用 `ssh-copy-id` 命令，将 SSH 公钥安装到集群中的每台主机上。所用的部署软件也可能提供更方便的方法，将公钥安全地安装到多台主机上。

3. 创建名为 `hosts` 的文件，列出组成 Apache Cloudberry 集群的主机，作为 Ansible 主机清单。例如：

    ```
    cdw
    scdw
    sdw1
    sdw2
    sdw3
    ```

    此文件之后还可以修改，用于 Apache Cloudberry 的 `gpssh-exkeys` 和 `gpinitsystem` 工具。

4. 将下面的 Playbook 代码复制到 Ansible 控制节点上的 `ansible-playbook.yml` 文件中。

5. 编辑 Playbook 开头的变量，例如要创建的 `gpadmin` 管理用户及其密码，以及要安装的 Apache Cloudberry 版本。

6. 运行 Playbook，通过 `package_path` 参数传入要安装的软件包。

    ```bash
    ansible-playbook ansible-playbook.yml -i hosts -e package_path=./apache-cloudberry-db-incubating-2.1.0.el8.x86_64.rpm
    ```

## Ansible Playbook：在 RHEL/Rocky Linux 上安装 Apache Cloudberry {#ansible-playbook---apache-cloudberry-installation-for-rhelrocky-linux}

```yaml
---

- hosts: all
  vars:
    - version: "2.1.0"
    - cloudberry_admin_user: "gpadmin"
    - cloudberry_admin_password: "changeme"
    # - package_path: passed via the command line with: -e package_path=./apache-cloudberry-db-incubating-2.1.0.el8.x86_64.rpm
  remote_user: root
  become: yes
  become_method: sudo
  connection: ssh
  gather_facts: yes
  tasks:
    - name: create cloudberry admin user
      user:
        name: "{{ cloudberry_admin_user }}"
        password: "{{ cloudberry_admin_password | password_hash('sha512', 'DvkPtCtNH+UdbePZfm9muQ9pU') }}"
    - name: copy package to host
      copy:
        src: "{{ package_path }}"
        dest: /tmp
    - name: install package
      yum:
        name: "/tmp/{{ package_path | basename }}"
        state: present
    - name: cleanup package file from host
      file:
        path: "/tmp/{{ package_path | basename }}"
        state: absent
    - name: find install directory
      find:
        paths: /usr/local
        patterns: 'cloudberry*'
        file_type: directory
      register: installed_dir
    - name: change install directory ownership
      file:
        path: '{{ item.path }}'
        owner: "{{ cloudberry_admin_user }}"
        group: "{{ cloudberry_admin_user }}"
        recurse: yes
      with_items: "{{ installed_dir.files }}"
    - name: update pam_limits
      pam_limits:
        domain: "{{ cloudberry_admin_user }}"
        limit_type: '-'
        limit_item: "{{ item.key }}"
        value: "{{ item.value }}"
      with_dict:
        nofile: 524288
        nproc: 131072
    - name: find installed cloudberry version
      shell: . /usr/local/cloudberry-db/cloudberry-env.sh && /usr/local/cloudberry-db/bin/postgres --gp-version
      register: postgres_gp_version
    - name: fail if the correct cloudberry version is not installed
      fail:
        msg: "Expected cloudberry version {{ version }}, but found '{{ postgres_gp_version.stdout }}'"
      when: "version is not defined or version not in postgres_gp_version.stdout"
```

Playbook 成功运行后，可以继续[创建数据存储区域](/cloudberry/deployment/create_data_dirs/)和[初始化 Apache Cloudberry](/cloudberry/deployment/init_cloudberry/)。
