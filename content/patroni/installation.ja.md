---
title: "インストール"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "サポート対象プラットフォームにおけるPatroniのインストールとアップグレードの手順。"
module: [PATRONI]
categories: [チュートリアル]
aliases: [/docs/patroni/installation/]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## Mac OSの前提条件 {#pre-requirements-for-mac-os}

Macに必要なソフトウェアをインストールするには、次を実行します。

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

[psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/)以降、psycopg2のバイナリー版はデフォルトではインストールされなくなりました。ソースコードからインストールするには、Cコンパイラーとpostgresおよびpythonの開発用パッケージが必要です。Pythonでは依存関係を`psycopg2 OR psycopg2-binary`として指定できないため、インストール方法を選択する必要があります。

次の選択肢があります。

1. ディストリビューションのパッケージマネージャーを使用する

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2. pipでPatroniをインストールするときに、[依存関係の一覧](/ja/patroni/installation#extras)に`psycopg`、`psycopg2`、`psycopg2-binary`のいずれかを指定する。

<a id="extras"></a>

--------

## pipによる一般的なインストール {#general-installation-for-pip}

Patroniはpipでインストールできます。

```bash
pip install patroni[dependencies]
```

ここで`dependencies`は空にするか、次のうち一つ以上を指定します。

etcdまたはetcd3  
DCS（分散構成ストア）としてetcdを使用するための`python-etcd`モジュール

consul  
DCSとしてConsulを使用するための`py-consul`モジュール

zookeeper  
DCSとしてZookeeperを使用するための`kazoo`モジュール

exhibitor  
DCSとしてExhibitorを使用するための`kazoo`モジュール（Zookeeperと同じ依存関係）

kubernetes  
PatroniでDCSとしてKubernetesを使用するための[kubernetes](/ja/patroni/kubernetes#kubernetes)モジュール

raft  
DCSとしてPythonのRaft実装を使用するための`pysyncobj`モジュール

aws  
AWSコールバックを使用するための`boto3`

jsonlogger  
JSON形式の[ログ出力](/ja/patroni/config/yaml#log_settings)を有効にするための`python-json-logger`モジュール

systemd  
sd_notify連携を使用するための`systemd-python`

all  
上記のすべて（psycopg系を除く）

psycopg3  
`psycopg\[binary\]\>=3.0.0`モジュール

psycopg2  
`psycopg2\>=2.5.4`モジュール

psycopg2-binary  
`psycopg2-binary`モジュール

たとえば、psycopg3、DCSとしてのetcdの依存関係、AWSコールバックとともにPatroniをインストールするコマンドは、次のとおりです。

```bash
pip install patroni[psycopg3,etcd3,aws]
```

レプリカ作成スクリプトや独自のブートストラップスクリプトから呼び出す外部ツール（WAL-Eなど）は、Patroniとは別にインストールすることを推奨します。

<a id="package_installation"></a>

--------

## Linuxへのパッケージのインストール {#package-installation-on-linux}

使用するオペレーティングシステム向けのPatroniパッケージが提供されている場合があります。Postgresコミュニティーは、次のシステム向けにパッケージを作成しています。

- RHEL、RockyLinux、AlmaLinux。
- DebianとUbuntu。
- SUSE Enterprise Linux。

オペレーティングシステムの公式リポジトリにはないPythonモジュールなど、Patroniの直接の依存関係のパッケージもあります。

詳しくは、[PGDGリポジトリ](https://www.postgresql.org/download/linux/)のドキュメントを参照してください。

RedHat Enterprise Linux派生のオペレーティングシステムでは、EPELのパッケージも必要になる場合があります。[EPELリポジトリ](https://docs.fedoraproject.org/en-US/epel/)のドキュメントを参照してください。

OS用のPGDGリポジトリをインストールしたら、Patroniをインストールできます。

> [!NOTE]
> PatroniパッケージはPatroni開発者ではなく、Postgresコミュニティーがメンテナンスしています。サポートが必要な場合は、まず[Postgres Slack](http://pgtreats.info/slack-invite)で相談してください。

### Debian派生システムへのインストール {#installing-on-debian-derivatives}

[上記](/ja/patroni/installation#package_installation)のとおりPGDGリポジトリをインストールしたら、次を実行してaptでPatroniをインストールします。

```bash
apt-get install patroni
```

### RedHat派生システムへのインストール {#installing-on-redhat-derivatives}

[上記](/ja/patroni/installation#package_installation)のとおりPGDGリポジトリをインストールしたら、RHEL 9とその派生システムで次を実行し、dnfを使用してetcd DCS付きのPatroniをインストールします。

```bash
dnf install patroni patroni-etcd
```

使用するRedHat派生ディストリビューションがetcdパッケージを提供していない場合は、PGDGからインストールできます。DCSを配置するノードで次を実行します。

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

必要であれば、リポジトリ名のRHELのバージョンを`8`に置き換えて、`pgdg-rhel8-extras`にできます。RockyLinux、AlmaLinux、Oracle Linuxなどでも、リポジトリ名は`pgdg-rhelN-extras`のままです。

### SUSE Enterprise Linuxへのインストール {#installing-on-suse-enterprise-linux}

一部の依存関係のために、SUSE PackageHubリポジトリを有効にする必要がある場合があります。[SUSE PackageHub](https://packagehub.suse.com/how-to-use/)のドキュメントを参照してください。

SLES 15で、[上記](/ja/patroni/installation#package_installation)のとおりPGDGリポジトリをインストールしている場合、次のコマンドでPatroniをインストールできます。

```bash
zypper install patroni patroni-etcd
```

SUSE PackageHubリポジトリを有効にすると、etcdもインストールできます。

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## アップグレード {#upgrading}

Patroniのアップグレードは非常に簡単です。ソフトウェアを更新し、クラスターの各ノードでPatroniデーモンを再起動するだけです。

ただし、Patroniデーモンを再起動すると、Postgresデータベースも再起動します。状況によってはクラスターのプライマリーノードでフェイルオーバーが発生する可能性があるため、Patroniデーモンの再起動が完了するまでクラスターをメンテナンスモードにすることを推奨します。

クラスターをメンテナンスモードにするには、Patroniノードのいずれかで次のコマンドを実行します。

```bash
patronictl pause --wait
```

次に、クラスターの各ノードでOSに応じたパッケージのアップグレードを実行します。

```bash
apt-get update && apt-get install patroni patroni-etcd
```

各ノードでPatroniデーモンのプロセスを再起動します。

```bash
systemctl restart patroni
```

最後に、PatroniによるPostgresの監視を再開して、メンテナンスモードを終了します。

```bash
patronictl resume --wait
```

これでクラスターは、新しいバージョンのPatroniで完全に稼働する状態になります。
