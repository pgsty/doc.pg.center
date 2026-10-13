---
title: "ロールベースのアクセス制御"
weight: 4100
description: "基本的な認証とロールベースのアクセス制御のガイド"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/authentication/rbac.md"
aliases: [/etcd/op-guide/authentication/rbac/]
---

## 概要 {#overview}

認証はetcd 2.1で追加されました。etcd v3 APIでは、新しいデータモデルに合わせて、認証機能のAPIとユーザーインターフェースを少し変更しています。このガイドは、etcd v3で基本的な認証とロールベースのアクセス制御を設定するためのものです。

## 特別なユーザーとロール {#special-users-and-roles}

特別なユーザー`root`と、特別なロール`root`が1つずつあります。

### ユーザー`root` {#user-root}

etcdへの完全なアクセス権を持つ`root`ユーザーは、認証を有効にする前に作成しなければなりません。`root`ユーザーは、ロールや通常のユーザーを管理するためのものです。`root`ユーザーには`root`ロールが必要で、etcd内のあらゆるものを変更できます。

### ロール`root` {#role-root}

`root`ロールは、rootユーザーに限らず、任意のユーザーに付与できます。`root`ロールを持つユーザーには、全体への読み書きのアクセス権と、クラスターの認証設定を更新する権限があります。また、`root`ロールは、メンバー構成の変更、ストアのデフラグメンテーション、スナップショットの取得など、クラスターの一般的な保守権限も与えます。

## ユーザーの操作 {#working-with-users}

`etcdctl`の`user`サブコマンドは、ユーザーアカウントに関するすべての操作を扱います。

次のコマンドでユーザーを一覧表示できます。

```
$ etcdctl user list
```

ユーザーは、次のように簡単に作成できます。

```
$ etcdctl user add myusername
```

新しいユーザーを作成すると、新しいパスワードの入力を求められます。`--interactive=false`オプションを指定すると、標準入力からパスワードを渡せます。`--new-user-password`を使ってパスワードを指定することもできます。

次のように、パスワードで認証できないユーザーを作成することもできます。

```
$ etcdctl user add myusername --no-password
```

このようなユーザーは、[TLSのCommon Nameによる認証](#using-tls-common-name)だけを使用できます。

> [!NOTE]
> etcdは、`--user username:`による空のパスワードでの認証に対応していません。たとえば、`etcdctl user add anonymous:''`のように空のパスワードで作成したユーザーは、ユーザー名とパスワードを使うリクエストでは認証できません。`etcdctl --user anonymous: get foo`などのリクエストは、`user name is empty`で失敗します。

次のコマンドで、ユーザーにロールを付与したり、取り消したりできます。

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

ユーザーの設定は、次のコマンドで確認できます。

```
$ etcdctl user get myusername
```

ユーザーのパスワードは、次のコマンドで変更できます。

```
$ etcdctl user passwd myusername
```

パスワードの変更時にも、新しいパスワードの入力を求められます。`--interactive=false`オプションを指定すると、標準入力からパスワードを渡せます。

次のコマンドでアカウントを削除します。
```
$ etcdctl user delete myusername
```


## ロールの操作 {#working-with-roles}

`etcdctl`の`role`サブコマンドは、個々のユーザーに付与する各ロールのアクセス制御に関するすべての操作を扱います。

次のコマンドでロールを一覧表示します。

```
$ etcdctl role list
```

次のコマンドで新しいロールを作成します。

```
$ etcdctl role add myrolename
```

ロールにパスワードはありません。新しいアクセス権の集合を定義するだけです。

ロールには、単一のキーまたはキーの範囲へのアクセス権を付与します。

範囲は区間[start-key, end-key)として指定できます。start-keyは、アルファベットの辞書順でend-keyより小さくすることを推奨します。

次の例のように、読み取り、書き込み、または両方のアクセス権を付与できます。

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

付与されている権限は、いつでもロールを参照して確認できます。

```
$ etcdctl role get myrolename
```

権限の取り消しも同様に行います。

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

ロール全体の削除も同様です。

```
$ etcdctl role delete myrolename
```

## 認証の有効化 {#enabling-authentication}

認証を有効にする最小限の手順は次のとおりです。管理者は、認証を有効にする前でも後でも、都合に合わせてユーザーとロールを設定できます。

rootユーザーを作成しておきます。

```
$ etcdctl user add root
Password of root:
```

認証を有効にします。

```
$ etcdctl auth enable
```

これで、etcdは認証が有効な状態で動作します。何らかの理由で無効にする場合は、逆の操作となる次のコマンドを使用します。

```
$ etcdctl --user root:rootpw auth disable
```

## 認証による保護範囲 {#security-scope-of-authentication}

`etcdctl auth enable`で認証を有効にすると、V3 gRPC APIの操作（get、put、delete、watchなど）が保護されます。

HTTPエンドポイント`/metrics`と`/health`は別のハンドラーで動作し、V3 RBAC認証では**保護されません**。この設計により、キー・バリューデータを保護しつつ、PrometheusやロードバランサーはgRPC認証なしでメトリクスを収集できます。

これらの可観測性エンドポイントを保護するには、次の方法があります。

- `--cert-file`、`--key-file`、`--client-cert-auth`でmTLSを有効にする
- または、`--listen-metrics-urls`でメトリクスをプライベートなインターフェースにバインドする
- または、ネットワークポリシーやファイアウォールルールでアクセスを制限する

## `etcdctl`での認証 {#using-etcdctl-to-authenticate}

`etcdctl`は、`curl`と似た認証用フラグをサポートします。

```
$ etcdctl --user user:password get foo
```

パスワードは、プロンプトから入力できます。

```
$ etcdctl --user user get foo
```

コマンドラインフラグ`--password`で指定することもできます。

```
$ etcdctl --user user --password password get foo
```


それ以外は、すべての`etcdctl`コマンドの使い方は変わりません。ユーザーとロールは引き続き作成、変更できますが、rootロールを持つユーザーによる認証が必要です。

## TLSのCommon Nameの利用 {#using-tls-common-name}
v3.2以降、etcdサーバーを`--client-cert-auth=true`オプションで起動すると、クライアントのTLS証明書のCommon Name（CN）フィールドをetcdユーザーとして使用します。この場合、Common Nameがユーザーを認証するため、クライアントにパスワードは不要です。ただし、1. `--client-cert-auth=true`を指定してクライアントがCNを提供し、かつ2. クライアントがユーザー名とパスワードも提供する場合は、ユーザー名とパスワードによる認証が優先されます。この機能はgRPC-proxyとgRPC-gatewayでは使えません。gRPC-proxyはクライアントからのTLSを終端するため、すべてのクライアントでプロキシーの証明書を共有するからです。gRPC-gatewayも、HTTPリクエストをgRPCリクエストに変換するために内部でTLS接続を使うので、同じ制限があります。このため、クライアントは自身のCNをサーバーに正しく提供できません。指定された証明書に空でないCNがあると、gRPC-proxyはエラーで停止します。gRPC-proxyが返すエラーは、クライアントの証明書のCNが空でないことを示します。

## パスワード強度に関する注意 {#notes-on-password-strength}
`etcdctl`とetcd APIは、ユーザーの作成時やパスワードの更新時に、特定のパスワード長を強制しません。こうした要件を適用する責任は管理者にあります。パスワード強度に伴うセキュリティーリスクを避けるには、[TLSのCommon Nameによる認証](#using-tls-common-name)と、`--no-password`オプションで作成したユーザーを利用できます。
