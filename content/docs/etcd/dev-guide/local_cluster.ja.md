---
title: ローカルクラスターの構築
weight: 3125
description: "テストと開発用のローカルクラスターを構成する"
categories: [チュートリアル]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/local_cluster.md"
aliases: [/etcd/dev-guide/local_cluster/]
---

テストや開発用にデプロイする場合、最も手早く簡単なのはローカルクラスターの構成です。本番環境へのデプロイについては、[クラスター構成][clustering]のセクションを参照してください。

## ローカルの単独クラスター {#local-standalone-cluster}

### クラスターの起動 {#starting-a-cluster}

etcdを単独クラスターとしてデプロイするには、次を実行します。

```
$ ./etcd
...
```

現在の作業ディレクトリに`etcd`バイナリーがない場合、`$GOPATH/bin/etcd`または`/usr/local/bin/etcd`にある可能性があります。その場所に合わせてコマンドを実行してください。

起動したetcdメンバーは、`localhost:2379`でクライアントリクエストを待ち受けます。

### クラスターの操作 {#interacting-with-the-cluster}

`etcdctl`で実行中のクラスターを操作します。

1. 例としてキー・バリューペアをクラスターに保存します。

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    OKと表示されれば、キー・バリューペアの保存は成功です。

2. `foo`の値を取得します。

    ```
    $ ./etcdctl get foo
    bar
    ```

    `bar`が返れば、etcdクラスターとのやり取りは正常に動作しています。

## ローカルの複数メンバークラスター {#local-multi-member-cluster}

### クラスターの起動 {#starting-a-cluster-1}

etcdのGitリポジトリのルートには、ローカルで複数メンバーのクラスターを簡単に構成するための`Procfile`があります。複数メンバーのクラスターを起動するには、etcdのソースツリーのルートに移動して、次の操作を行います。

1. Procfileに基づくアプリケーションを制御するため、`goreman`をインストールします。

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. etcdに付属するProcfileを使い、`goreman`でクラスターを起動します。

    ```
    $ goreman -f Procfile start
    ```

    メンバーが起動し、それぞれ`localhost:2379`、`localhost:22379`、`localhost:32379`でクライアントリクエストを待ち受けます。

### クラスターの操作 {#interacting-with-the-cluster-1}

`etcdctl`で実行中のクラスターを操作します。

1. メンバーの一覧を表示します。

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    etcdメンバーの一覧が次のように表示されます。

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. 例としてキー・バリューペアをクラスターに保存します。

    ```
    $ etcdctl put foo bar
    OK
    ```

    OKと表示されれば、キー・バリューペアの保存は成功です。

### 耐障害性のテスト {#testing-fault-tolerance}

etcdの耐障害性を試すため、メンバーを停止してからキーを取得します。

1. 停止するメンバーのプロセス名を確認します。

    `Procfile`には、複数メンバーのクラスターのプロパティが記載されています。ここでは、プロセス名が`etcd2`のメンバーを例にします。

2. メンバーを停止します。

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. キーを保存します。

    ```
    $ etcdctl put key hello
    OK
    ```

4.  前の手順で保存したキーを取得します。

    ```
    $ etcdctl get key
    hello
    ```

5. 停止したメンバーからキーを取得します。

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    このコマンドでは、接続失敗によるエラーが表示されるはずです。

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. 停止したメンバーを再起動します。

    ```
    $ goreman run restart etcd2
    ```

7. 再起動したメンバーからキーを取得します。

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    メンバーを再起動すると接続が再確立され、`etcdctl`でキーを正常に取得できるようになります。etcdの操作について詳しくは、[etcdの操作][interacting]のセクションを参照してください。

[clustering]: /ja/docs/etcd/op-guide/clustering/
[interacting]: /ja/docs/etcd/dev-guide/interacting_v3/
