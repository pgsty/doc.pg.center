---
title: "通信のセキュリティーモデル"
weight: 4125
description: "通信中のデータの保護"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/security.md"
---

etcdは、クライアントとサーバーの通信、およびピア間（サーバー間／クラスター内）の通信の両方で、自動TLSとクライアント証明書による認証に対応しています。**etcdは、データベースを使い始める際の負担を減らすため、[RBACによる認証][auth]も通信層の認証機能も、デフォルトでは有効にしません。また、このデフォルトは2013年のプロジェクト発足以来のもので、変更すると互換性を損ないます。セキュリティー機能を有効にしていないetcdクラスターは、あらゆるクライアントにデータを公開してしまう可能性があります。**

まず、CA証明書と、1メンバー用の署名済み鍵ペアを用意します。クラスターのメンバーごとに新しい鍵ペアを作成し、署名することを推奨します。

[cfssl]ツールを使うと、証明書を簡単に生成できます。このツールを使った例を[こちら][tls-setup]に示しています。また、[自己署名鍵ペアの生成ガイド][tls-guide]も参照できます。

開発による変更が続いているため、以下のフラグ一覧は最新でない場合があります。利用可能な最新のフラグは、`etcd --help`を実行するか、[etcdのヘルプ][etcd help]を参照してください。

## 基本設定 {#basic-setup}

etcdには、コマンドラインフラグまたは環境変数で指定できる、証明書関連の設定オプションがいくつかあります。

**クライアントとサーバーの通信：**

`--cert-file=<path>`：etcd**への**SSL/TLS接続に使う証明書。このオプションを設定すると、advertise-client-urlsでHTTPSスキームを使えます。

`--key-file=<path>`：証明書の鍵。暗号化されていてはなりません。

`--client-cert-auth`：指定すると、etcdはすべての受信HTTPSリクエストについて、信頼するCAが署名したクライアント証明書を確認します。有効なクライアント証明書を提示しないリクエストは失敗します。[認証][auth]が有効な場合、証明書はCommon Nameフィールドに指定されたユーザー名の認証情報を提供します。

`--trusted-ca-file=<path>`：信頼する認証局。

`--auto-tls`：クライアントとのTLS接続に、自動生成した自己署名証明書を使用します。

**ピア間（サーバー間／クラスター内）の通信：**

ピア用のオプションは、クライアントとサーバーの通信のオプションと同様に機能します。

`--peer-cert-file=<path>`：ピア間のSSL/TLS接続に使う証明書。ピアアドレスでのリッスンと、ほかのピアへのリクエスト送信の両方で使用します。

`--peer-key-file=<path>`：証明書の鍵。暗号化されていてはなりません。

`--peer-client-cert-auth`：指定すると、etcdはクラスターから受信するすべてのピアリクエストについて、指定のCAが署名した有効なクライアント証明書を確認します。

`--peer-trusted-ca-file=<path>`：信頼する認証局。

`--peer-auto-tls`：ピア間のTLS接続に、自動生成した自己署名証明書を使用します。

クライアントとサーバーの通信、またはピア間の通信に証明書を指定した場合、鍵も設定しなければなりません。これらの設定オプションはすべて、`ETCD_TRUSTED_CA_FILE`、`ETCD_PEER_TRUSTED_CA_FILE`などの環境変数でも指定できます。

**共通オプション：**

`--cipher-suites`：サーバーとクライアント、およびピア間でサポートするTLS暗号スイートのカンマ区切りの一覧（空の場合はGoが自動設定します）。

`--tls-min-version=<version>`：etcdがサポートするTLSの最小バージョンを設定します。

`--tls-max-version=<version>`：etcdがサポートするTLSの最大バージョンを設定します。未設定の場合、Goがサポートする最大バージョンを使用します。

### TLS証明書のkeyUsageとextendedKeyUsage {#tls-certificate-keyusage-and-extendedkeyusage}

etcdの通信を保護するX.509証明書を生成するときは、その役割に応じた適切な`keyUsage`と`extendedKeyUsage`フィールドを含めることを推奨します。etcdは証明書の検証にGoの`crypto/tls`と`crypto/x509`ライブラリを使用し、これらのライブラリがTLSハンドシェイク中に用途を検証します。

次の表に、一般的な証明書の役割に対する推奨用途を示します。

| 証明書の役割 | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| サーバー（クライアントとサーバーの通信） | digitalSignature, keyEncipherment | serverAuth |
| クライアント | digitalSignature, keyEncipherment | clientAuth |
| ピア（サーバー間の通信） | digitalSignature, keyEncipherment | serverAuth, clientAuth |

注意事項：

- `--peer-client-cert-auth`が有効な場合、ピア証明書はetcdメンバー間の相互TLSに使うため、`serverAuth`と`clientAuth`の両方が必要です。
- `--client-cert-auth`で使うクライアント証明書には、`clientAuth`を含めることを推奨します。

## 例1：HTTPSによるクライアントとサーバー間の通信の保護 {#example-1-client-to-server-transport-security-with-https}

CA証明書（`ca.crt`）と署名済み鍵ペア（`server.crt`、`server.key`）を用意します。

単純なHTTPSによる通信の保護を提供するよう、etcdを順に設定します。

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

これで正常に起動するはずです。HTTPSでetcdにアクセスして設定をテストできます。

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

このコマンドで、ハンドシェイクの成功を確認できるはずです。独自の認証局による自己署名証明書を使用するため、`--cacert`オプションでCAをcurlに渡さなければなりません。CA証明書をシステムの信頼済み証明書ディレクトリ（通常は`/etc/pki/tls/certs`または`/etc/ssl/certs`）に追加する方法もあります。

**OSX 10.9以降のユーザー**：OSX 10.9以降のcurl 7.30.0は、コマンドラインから渡された証明書を認識しません。
代わりに、ダミーのca.crtをキーチェーンに直接インポートするか、curlに`-k`フラグを付けてエラーを無視してください。
`-k`なしでテストするには、`open ./tests/fixtures/ca/ca.crt`を実行し、表示される指示に従います。
テスト後は、この証明書を削除してください。
回避策があれば、お知らせください。

## 例2：HTTPSクライアント証明書によるクライアントとサーバー間の認証 {#example-2-client-to-server-authentication-with-https-client-certificates}

ここまでは、etcdクライアントがサーバーの身元を検証し、通信を保護できるようにしました。クライアント証明書を使って、etcdへの不正アクセスを防ぐこともできます。

クライアントはサーバーに証明書を提示し、サーバーはそれが指定されたCAによる署名かどうかを確認して、リクエストを処理するか判断します。

最初の例のファイルに加えて、同じ認証局が署名したクライアント用鍵ペア（`client.crt`、`client.key`）が必要です。

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

このサーバーに対し、先ほどと同じリクエストを試します。

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

サーバーはリクエストを拒否するはずです。

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

成功させるには、CAが署名したクライアント証明書をサーバーに提示する必要があります。

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

出力には、次の内容が含まれるはずです。

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

サーバーからのレスポンスも含まれます。

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

[弱いTLS暗号スイート](https://github.com/etcd-io/etcd/issues/8320)を拒否するには、暗号スイートを指定します。

無効な暗号スイートを含むClient Helloを送ると、TLSハンドシェイクは失敗します。

例：

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

この場合、クライアントのリクエストは、サーバーに指定された暗号スイートのいずれかを指定しなければなりません。

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## 例3：クラスター内の通信の保護とクライアント証明書 {#example-3-transport-security--client-certificates-in-a-cluster}

etcdは、**ピア間通信**、つまりクラスター内のetcdメンバー間の通信にも、上記と同じモデルをサポートします。

`ca.crt`と、このCAが署名した各メンバーの鍵ペア（`member1.crt`と`member1.key`、`member2.crt`と`member2.key`）を持つ2つのメンバーがあるとします。次のようにetcdを起動します。


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

etcdメンバーはクラスターを構成し、クラスター内のメンバー間通信はすべて暗号化され、クライアント証明書で認証されます。etcdの出力には、接続先のアドレスがHTTPSを使用していることが示されます。

## 例4：自動生成した自己署名証明書による通信の保護 {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> ClientAutoTLSとPeerAutoTLSを指定すると、etcdが自動生成するクライアント証明書とピア証明書の有効期間は1年だけです。--self-signed-cert-validityフラグで、証明書の有効期間を年単位で設定できます。

通信の暗号化は必要でも認証は不要な場合、etcdは自動生成した自己署名証明書でメッセージを暗号化できます。etcdの外で証明書や鍵を管理する必要がないため、配置が簡単になります。
`--auto-tls`と`--peer-auto-tls`フラグで、クライアント接続とピア接続に自己署名証明書を使うよう設定します。

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

自己署名証明書は身元を認証しないため、curlはエラーを返します。

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

証明書チェーンの検証を無効にするには、`-k`フラグを付けてcurlを実行します。

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## DNS SRVに関する注意 {#notes-for-dns-srv}

v3.1.0以降（v3.2.9を除く）、SRVディスカバリーによるブートストラップは、`--discovery-srv`フラグのルートドメイン名で`ServerName`を認証します。証明書のSubject Alternative Name（SAN）フィールドに一致するルートドメイン名を要求することで、証明書を使う中間者攻撃を防ぎます。たとえば、`etcd --discovery-srv=etcd.local`では、提供された証明書のSubject Alternative Name（SAN）フィールドにルートドメイン`etcd.local`が含まれる場合にのみ、ピアやクライアントを認証します。

## etcdプロキシーに関する注意 {#notes-for-etcd-proxy}

> [!NOTE]
> このセクションでは、削除済みの旧v2プロキシーを説明します。etcd 3.7では、[v3 gRPCプロキシー](/ja/etcd/op-guide/grpc_proxy/)を使用してください。

etcdプロキシーは、クライアントとの接続が保護されている場合、そのTLSを終端します。etcdメンバーとの通信には、`--peer-key-file`と`--peer-cert-file`で指定したプロキシー自身の鍵と証明書を使います。

プロキシーは、各メンバーの`--advertise-client-urls`と`--advertise-peer-urls`の両方を使って通信します。クライアントリクエストはメンバーの通知するクライアントURLに転送し、初期クラスター構成はメンバーの通知するピアURLを通じて同期します。

etcdメンバーでクライアント認証が有効な場合、管理者は、プロキシーの`--peer-cert-file`で指定したピア証明書がその認証に有効であることを確認しなければなりません。ピア認証も有効な場合は、プロキシーのピア証明書がピア認証にも有効でなければなりません。

## TLS認証に関する注意 {#notes-for-tls-authentication}

[v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)以降、[クライアント接続ごとにTLS証明書を再読み込みします](https://github.com/etcd-io/etcd/pull/7829)。etcdサーバーを停止せずに期限切れ証明書を交換する際に便利で、古い証明書を新しいものに上書きするだけで対応できます。接続ごとの証明書の更新に大きなオーバーヘッドは生じないはずですが、将来はキャッシュ層で改善することもできます。テスト例は[こちら](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757)を参照してください。

[v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)以降、[サーバーはIPの`SAN`が正しくないピア証明書を拒否します](https://github.com/etcd-io/etcd/pull/7687)。たとえば、ピア証明書のSubject Alternative Name（SAN）フィールドにIPアドレスがある場合、リモートIPアドレスがそのいずれかと一致するときだけ認証します。これは、許可されていないエンドポイントがクラスターに参加することを防ぐためです。たとえば、ピアBのCSR（`cfssl`を使用）が次のとおりだとします。

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

一方、ピアBの実際のIPアドレスは`10.138.0.27`ではなく`10.138.0.2`です。Bがクラスターに参加しようとすると、ピアAは`x509: certificate is valid for 10.138.0.27, not 10.138.0.2`エラーで拒否します。BのリモートIPアドレスがSubject Alternative Name（SAN）フィールドのアドレスと一致しないためです。

[v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)以降、[サーバーは`SAN`の検証時にTLSの`DNSNames`を名前解決します](https://github.com/etcd-io/etcd/pull/7767)。たとえば、ピア証明書のSubject Alternative Name（SAN）フィールドにDNS名だけがあり、IPアドレスがない場合、そのDNS名を正引き（`dig b.com`）したIPがリモートIPアドレスに一致するときだけ、サーバーはピアを認証します。たとえば、ピアBのCSR（`cfssl`を使用）が次のとおりだとします。

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

ピアBのリモートIPアドレスは`10.138.0.2`です。Bがクラスターに参加しようとすると、ピアAは接続してきたホスト`b.com`を名前解決し、IPアドレスの一覧を取得します（`dig b.com`など）。一覧にIPアドレス`10.138.0.2`がなければ、`tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`エラーでBを拒否します。

[v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07)以降、[IPが一致すれば、サーバーはDNSエントリーを確認せずに接続を受け入れます](https://github.com/etcd-io/etcd/pull/8223)。たとえば、ピア証明書のSubject Alternative Name（SAN）フィールドにIPアドレスとDNS名があり、リモートIPアドレスがそのいずれかに一致する場合、サーバーはDNS名を追加で確認せずに接続を受け入れます。たとえば、ピアBのCSR（`cfssl`を使用）が次のとおりだとします。

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

ピアBのリモートIPアドレスは`10.138.0.2`で、`invalid.domain`は無効なホストです。Bがクラスターに参加しようとすると、Subject Alternative Name（SAN）フィールドに一致する有効なIPアドレスがあるため、ピアAはBの認証に成功します。詳しくは、[issue#8206](https://github.com/etcd-io/etcd/issues/8206)を参照してください。

[v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04)以降、[サーバーはワイルドカードDNSの`SAN`の逆引きに対応します](https://github.com/etcd-io/etcd/pull/8281)。たとえば、ピア証明書のSubject Alternative Name（SAN）フィールドにDNS名だけがあり、IPアドレスがない場合、サーバーはまずリモートIPアドレスを逆引きし、そのアドレスに対応する名前の一覧を取得します（`nslookup IPADDR`など）。その名前のいずれかがピア証明書のDNS名と完全一致またはワイルドカード一致すれば、接続を受け入れます。一致しなければ、ピア証明書の各DNSエントリーを正引きし（エントリーが`*.example.default.svc`なら`example.default.svc`を検索）、名前解決したアドレスがピアのリモートIPアドレスと一致するときだけ受け入れます。たとえば、ピアBのCSR（`cfssl`を使用）が次のとおりだとします。

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

ピアBのリモートIPアドレスは`10.138.0.2`です。Bがクラスターに参加しようとすると、ピアAはIPアドレス`10.138.0.2`を逆引きしてホスト名の一覧を取得し、Bの証明書のSubject Alternative Name（SAN）フィールドのDNS名と、完全一致またはワイルドカード一致するかを確認します。逆引きでも正引きでも一致しなければ、`"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]`というエラーを返します。詳しくは、[issue#8268](https://github.com/etcd-io/etcd/issues/8268)を参照してください。

[v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md)では、[`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616)フラグを追加し、[ピア間接続のCN（Common Name）による認証](https://github.com/etcd-io/etcd/issues/8262)に対応しました。KubernetesのTLSブートストラップでは、etcdメンバーやほかのシステムコンポーネント（APIサーバー、kubeletなど）用に証明書を動的に生成します。コンポーネントごとに別のCAを管理するとetcdクラスターへのアクセスを厳しく制御できますが、多くの場合手間がかかります。--peer-cert-allowed-cnを指定すると、CAを共有していても、Common Nameが一致するノードだけが参加できます。照合は、証明書のCommon Name（CN）フィールドとの完全な文字列比較で、ワイルドカードや前方一致には対応しません。--peer-cert-allowed-hostnameや--client-cert-allowed-hostnameによるホスト名のフィルタリングは、Goのx509.Certificate.VerifyHostname()を使い、完全なホスト名とワイルドカード（*.example.comなど）の両方に対応します。たとえば、3ノードクラスターの各メンバーを、次のCSR（cfsslを使用）で設定します。




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

`--peer-cert-allowed-cn etcd.local`を指定すると、Common Nameが一致するピアだけを認証します。CSRのCNや`--peer-cert-allowed-cn`が異なるノードは拒否します。

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

各プロセスを次のように起動します。

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md)と[v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md)では、[証明書のSANフィールドにIPアドレスだけがあり、ドメイン名がない場合](https://github.com/etcd-io/etcd/issues/9541)のTLS再読み込みを修正しています。たとえば、あるメンバーを次のCSR（`cfssl`を使用）で設定します。

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

Goでは、サーバーの`(*tls.Config).Certificates`フィールドが空の場合、またはクライアントからの有効なSNIで`(*tls.ClientHelloInfo).ServerName`が空でない場合に限り、TLS再読み込みのために`(*tls.Config).GetCertificate`を呼び出します。以前のetcdは、最初のクライアントTLSハンドシェイク時に常に`(*tls.Config).Certificates`を設定し、空でない状態にしていました。そのため、TLS検証に合格し、`(*tls.Config).GetCertificate`によるTLSファイルの再読み込みを発生させるには、クライアントが一致するSNIを必ず送ることを想定していました。

しかし、SANフィールドに[ドメイン名がなくIPアドレスしかない証明書](https://github.com/etcd-io/etcd/issues/9541)では、`ServerName`が空の`*tls.ClientHelloInfo`でリクエストするため、最初のTLSハンドシェイクで再読み込みが発生しませんでした。これは、期限切れ証明書をオンラインで置き換える際に問題となります。

現在は、最初のTLSクライアントハンドシェイク時に`(*tls.Config).Certificates`を空で作成し、まず`(*tls.Config).GetCertificate`を呼び出します。その後、新しいTLS接続ごとに残りの証明書を設定するため、クライアントのSNIが空の場合（証明書がIPだけを含む場合など）でも動作します。

## ホスト許可リストに関する注意 {#notes-for-host-whitelist}

`etcd --host-whitelist`フラグは、HTTPクライアントリクエストで許可するホスト名を指定します。クライアントオリジンポリシーは、保護されていないetcdサーバーへの[「DNSリバインディング」](https://en.wikipedia.org/wiki/DNS_rebinding)攻撃を防ぎます。任意のWebサイトが、許可されたDNS名を作成し、そのDNSを`"localhost"`（または任意のアドレス）に向けるだけで、`"localhost"`でリッスンするetcdサーバーのすべてのHTTPエンドポイントにアクセスできてしまい、DNSリバインディング攻撃に対して脆弱になるためです。詳しくは、[CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2)を参照してください。

クライアントオリジンポリシーは、次のように機能します。

1. HTTPSによる保護されたクライアント接続の場合、すべてのホスト名を許可します。
2. 保護されていないクライアント接続で、`"HostWhitelist"`が空でない場合、Hostフィールドが許可リストにあるHTTPリクエストだけを許可します。

制御を厳格にするため、認証が有効かどうかにかかわらず、クライアントオリジンポリシーを適用します。

デフォルトでは、`etcd --host-whitelist`と`embed.Config.HostWhitelist`は`*`に設定され、すべてのホスト名を許可します。許可リストが空の場合も、すべてのホスト名を許可します。ホスト名を指定する場合、ループバックアドレスは自動追加されません。ループバックインターフェースを許可するには、許可リストに手動で追加してください（`"localhost"`、`"127.0.0.1"`など）。

## よくある質問 {#frequently-asked-questions}

### TLSクライアント認証でSSLv3 alert handshake failureが発生する場合 {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

`golang`の`crypto/tls`パッケージは、証明書の公開鍵を使う前に鍵の用途を確認します。
証明書の公開鍵をクライアント認証に使うには、証明書の公開鍵を作成する際に、`Extended Key Usage`へ`clientAuth`を追加する必要があります。

手順は次のとおりです。

openssl.cnfに、次のセクションを追加します。

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

証明書を作成するときは、`-extensions`フラグで必ず参照してください。

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### ピア証明書認証で"certificate is valid for 127.0.0.1, not $MY_IP"が返る場合 {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
メンバーのパブリックIPアドレスをSubject Nameに指定して、証明書に署名してください。たとえば、`etcd-ca`ツールには`new-cert`コマンドの`--ip=`オプションがあります。

証明書はSubject NameにメンバーのFQDNを指定して署名し、Subject Alternative Names（略してIP SAN）でIPアドレスを追加する必要があります。`etcd-ca`ツールには`new-cert`コマンドの`--domain=`オプションがあり、opensslでも[同じこと][alt-name]ができます。

### etcdはディスク上のデータを暗号化するか {#does-etcd-encrypt-data-stored-on-disk-drives}
いいえ。etcdは、ディスクに保存するキー・バリューデータを暗号化しません。etcdに保存するデータを暗号化する必要がある場合は、次の方法があります。
* クライアントアプリケーションでデータを暗号化、復号する
* [dm-crypt]など、基盤となるストレージシステムの保存データ暗号化機能を使う

### "directory X exist without recommended permission -rwx------"という警告ログが出る場合 {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
etcdは特定のディレクトリを新規作成するとき、権限のないアクセスをできる限り防ぐため、ファイルの権限を700に設定します。ただし、ユーザーがすでに独自の設定でディレクトリを作成している場合、etcdは既存のディレクトリを使用し、権限が700と異なれば警告メッセージを記録します。

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /ja/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
