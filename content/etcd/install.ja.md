---
title: "インストール"
weight: 1150
description: "ビルド済みバイナリーまたはソースからetcdをインストールする手順。"
icon: fa-solid fa-download
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## 要件 {#requirements}

etcdをインストールする前に、次のページを参照してください。

- [対応プラットフォーム][Supported platforms]
- [推奨ハードウェア][Hardware recommendations]

## ビルド済みバイナリーのインストール {#install-pre-built-binaries}

etcdを最も簡単にインストールする方法は、ビルド済みバイナリーを使用することです。

 1. [リリース一覧][Releases]から、使用するプラットフォームの圧縮アーカイブをダウンロードします。
    リリースは[v3.7.2][tagged-release]以降を選択してください。
 2. アーカイブを展開します。バイナリーを含むディレクトリが作成されます。
 3. 実行可能バイナリーにパスを通します。たとえば、必要に応じてバイナリーの名前を変更して
    パスの通ったディレクトリ（`/usr/local/bin`など）へ移動するか、
    前の手順で作成されたディレクトリをパスに追加します。
 4. シェルから、`etcd`にパスが通っていることを確認します。

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

## ソースからのビルド {#build-from-source}

etcd v3.7.2では、[Goバージョン1.26以降][go]を使用してください。このリリースはGo 1.26.8のツールチェーンを指定しています。
次の手順でソースからetcdをビルドできます。

 1. [etcdリポジトリをzipファイルとしてダウンロード][download]して展開するか、
    次のコマンドでリポジトリをクローンします。

    ```sh
    $ git clone -b v3.7.2 https://github.com/etcd-io/etcd.git
    ```
    `main@HEAD`からビルドするには、`-b v3.7.2`フラグを省略します。

 2. ディレクトリを移動します。

    ```sh
    $ cd etcd
    ```
 3. ビルドスクリプトを実行します。

    ```sh
    $ ./scripts/build.sh
    ```

    バイナリーは`bin`ディレクトリに生成されます。

 4. `bin`ディレクトリの絶対パスをパスに追加します。例：

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. `etcd`にパスが通っていることを確認します。

    ```sh
    $ etcd --version
    ```

## OSパッケージによるインストール {#installation-via-os-packages}
*免責事項：OSのパッケージマネージャーによるetcdのインストールでは、古いバージョンが提供される場合があります。これらは自動的に保守されておらず、etcdプロジェクトの公式サポート対象でもありません。そのため、OSパッケージは慎重に使用してください。*

オペレーティングシステムごとにさまざまなetcdのインストール方法があります。以下はその一例です。

### MacOS（Homebrew） {#macos-homebrew}

1. Homebrewを更新します。
```sh
$ brew update
```

2. etcdをインストールします。
```sh
$ brew install etcd
```

3. インストールを確認します。
```sh
$ etcd --version
```

## Linux {#linux}

多くの主要なLinuxディストリビューションでは、公式リポジトリとパッケージマネージャーからetcdをインストールできますが、公開されているバージョンが大幅に古い場合があります。そのため、この方法でのインストールは避けることを強く推奨します。

Linuxへのetcdのインストールには、[ビルド済みバイナリー](#install-pre-built-binaries)またはHomebrewの使用を推奨します。

### LinuxでのHomebrew {#homebrew-on-linux}

[HomebrewはLinuxでも動作][Homebrew can run on Linux]し、新しいバージョンのソフトウェアを提供できます。

- 前提条件
  - Homebrewを更新します。

    ```sh
    $ brew update
    ```

- 手順
  - `brew`でインストールします。

    ```sh
    $ brew install etcd
    ```

- 結果
  - バージョンを取得してインストールを確認します。

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

    上記の出力は一例です。Homebrewが提供するパッチバージョンは異なる場合があるため、`etcd --version`で実際にインストールされたバージョンを確認してください。

## Docker {#docker}

etcdは、主なコンテナーレジストリとして[`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd)を、
副次的なレジストリとして[`quay.io/coreos/etcd`](https://quay.io/coreos/etcd)を使用します。

Dockerでetcdを実行するには、次のコマンドを使用します。

```sh
ETCD_VER=v3.7.2

rm -rf /tmp/etcd-data.tmp && mkdir -p /tmp/etcd-data.tmp && \
  docker rmi gcr.io/etcd-development/etcd:${ETCD_VER} || true && \
  docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
  --name etcd-gcr-${ETCD_VER} \
  gcr.io/etcd-development/etcd:${ETCD_VER} \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster s1=http://0.0.0.0:2380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --log-level info \
  --logger zap \
  --log-outputs stderr

docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcd --version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdutl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl endpoint health
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl put foo bar
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl get foo
```

## Kubernetesのインストールの一環としてのインストール {#installation-as-part-of-kubernetes-installation}

- [KubernetesのStatefulSetとしてetcdを実行する][Running etcd as a Kubernetes StatefulSet]

## インストールの確認 {#installation-check}

インストールが正常に行われたことをもう少し詳しく確認するには、[クイックスタート][Quickstart]を参照してください。

[download]: https://github.com/etcd-io/etcd/archive/v3.7.2.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /ja/etcd/op-guide/hardware/
[Quickstart]: /ja/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /ja/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.2
[Supported platforms]: /ja/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
