---
title: "Goモジュール"
weight: 1650
description: "etcdプロジェクトのGoモジュール構成"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/modules.md"
---

etcdプロジェクトはバージョン3.5以降、[単一のリポジトリ](https://golang.org/ref/mod#vcs-dir)に置かれた複数の[Goモジュール](https://golang.org/ref/mod)で構成されています。

![モジュールの依存関係図](/etcd/dev-internal/img/modules.svg)

次のモジュールがあります。

  - **go.etcd.io/etcd/api/v3** - etcdクライアントとサーバー間の通信プロトコルを定義する
  API定義（protoやprotoから生成されたライブラリーなど）を含みます。

  - **go.etcd.io/etcd/pkg/v3** - etcdで使用する、etcd固有ではないユーティリティーパッケージ群です。
  将来独立したリポジトリに移せる可能性のあるパッケージだけをここに置きます。
  多くの依存関係を持つコードの追加は避けてください。
  それらは自動的にクライアントライブラリーの依存関係にもなり、
  軽量に保つという方針に反するためです。

  - **go.etcd.io/etcd/client/v3** - ネットワーク（grpc）経由でetcdに接続するクライアントライブラリーです。
  etcdの新規利用すべてに推奨します。

  - **go.etcd.io/etcd/client/v2** - HTTPプロトコル経由でetcdに接続する旧クライアントライブラリーです。
  非推奨です。新規利用ではすべて/v3ライブラリーへの依存を推奨します。

  - **go.etcd.io/etcd/raft/v3** - 分散コンセンサスプロトコルの実装です。
  etcd固有のコードを含めないようにしてください。

  - **go.etcd.io/etcd/server/v3** - etcdの実装です。
  このパッケージのコードはetcdの内部実装であり、外部プロジェクトからの利用は推奨しません。
  パッケージ構成やAPIは同じマイナーバージョン内でも変更される場合があります。

  - **go.etcd.io/etcd/etcdctl/v3** - etcdへのアクセスと管理を行うコマンドラインツールです。

  - **go.etcd.io/etcd/tests/v3** - etcdのすべての結合テストを含むモジュールです。
    注意：単体テスト（高速でモジュール間の依存関係を必要としないもの）はすべて、
    テスト対象のコードと同じモジュールに置くことを推奨します。

  - **go.etcd.io/bbolt** - 永続的なB木の実装です。
    独立したリポジトリ https://github.com/etcd-io/bbolt に置かれています。


### 運用 {#operations}

1. etcdのすべてのモジュールは、同じバージョンでリリースすることを推奨します。たとえば、
   `go.etcd.io/etcd/client/v3@v3.5.10`は`go.etcd.io/etcd/api/v3@v3.5.10`に依存しなければなりません。

   バージョンを一貫して更新するには、次のコマンドを使用できます。
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. リリースするモジュールは https://golang.org/ref/mod#vcs-version の規則に従ってタグ付けすることを推奨します。
   つまり、モジュールごとに固有のタグを付けます。
   タグ付けには次のコマンドを使用できます。
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. etcdのすべてのモジュールは、共通の依存先に対して同じバージョンに依存することを推奨します。
   次のコマンドで確認できます。
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. go.modファイルには未使用の依存関係を含めてはならず、
   `go mod tidy`の形式に従わなければなりません。
   次のコマンドで確認します。
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. 全ファイルの自動整形など、すべてのモジュールに対する操作を行うには、
   次のスクリプトを使用または拡張してください。
   ```shell script
   % ./scripts/fix.sh
   ```

### 今後の方向性 {#future}

長期的な目標として、etcdのモジュール構成を次のモデルに近づけたいと考えています。

![将来のモジュール依存関係図](/etcd/dev-internal/img/modules-future.svg)

このモデルは次を前提とします。
  - etcdmigrate/etcdadmをetcdctlバイナリーから分離します。
    これにより、etcdctlはネットワーククライアントAPIを扱う
    コマンドラインのラッパーとして明確に位置付けられ、
    etcdmigrate/etcdadmはetcdのストレージファイルに対する
    直接的な物理操作を担うようになります。
  - etcd-proxyを./etcdバイナリーから分離します。実験的なコードが多く、
    追加のリスクと依存関係を伴うためです。
  - v2プロトコルのサポートを非推奨にします。
