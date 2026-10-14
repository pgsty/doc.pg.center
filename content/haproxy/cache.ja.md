---
title: "6. キャッシュ"
linkTitle: "6. キャッシュ"
weight: 170
description: "キャッシュの制約とcacheおよびproxyセクションでの設定"
icon: fa-solid fa-box-archive
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/cache/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 6"
---

HAProxyは、faviconやcssなどの小さなオブジェクトを対象とするキャッシュを提供します。RAM上で動作する、最小限の保守で済む簡素なキャッシュです。

キャッシュには全スレッドで共有するメモリ領域を使用し、1kBのブロックに分割します。

オブジェクトが使われなくなると、有効期限にかかわらず、新しいオブジェクトを保存するために削除できます。新しいオブジェクトを割り当てる際は、最も古いオブジェクトから削除します。

キャッシュのキーには、hostヘッダーとURIのハッシュを使用します。

Unixソケットの "show cache" コマンドでキャッシュの状態を確認できます。詳細は管理ガイドの[第9.3節](/ja/haproxy/statistics-and-monitoring/#section-9-3)「Unixソケットコマンド」を参照してください。

キャッシュからオブジェクトを配信すると、ログのサーバー名は "`<CACHE>`" に置き換えられます。

## 6.1. 制約 {#section-6-1}

次の場合、キャッシュはオブジェクトを保存せず、配信もしません。

- レスポンスが200ではない場合。

- レスポンスにVaryヘッダーがあり、process-varyオプションが無効になっているか、Varyの値に現在未対応のヘッダーが指定されている場合。現時点で対応しているのはaccept-encoding、referer、originのみです。

- Content-Lengthとヘッダーサイズの合計が "max-object-size" を超える場合。

- レスポンスをキャッシュできない場合。

- レスポンスに明示的な有効期限（Cache-Controlのs-maxageまたはmax-ageディレクティブ、またはExpiresヘッダー）も、検証子（ETagまたはLast-Modifiedヘッダー）もない場合。

- process-varyオプションが有効で、現在のレスポンスと同じプライマリーキーのエントリーがすでにmax-secondary-entries個存在する場合。

- process-varyオプションが有効で、クライアントのaccept-encodingヘッダーによってレスポンスが変化する一方、そのエンコーディングが未知の場合。<https://www.iana.org/assignments/http-parameters/http-parameters.xhtml> に記載されていないエンコーディングが該当します。

- リクエストがGETではない場合。

- リクエストのHTTPバージョンが1.1未満の場合。

- リクエストにAuthorizationヘッダーが含まれる場合。

## 6.2. 設定 {#section-6-2}

キャッシュを設定するには、cacheセクションを定義し、対応するhttp-requestアクションとhttp-responseアクションを使ってプロキシから利用する必要があります。

### 6.2.1. cacheセクション {#section-6-2-1}

<a id="entry-6-2-1-cache"></a>

**`cache <name>`**

```haproxy
cache <name>
```

cacheセクションを宣言し、`<name>` という名前の共有キャッシュメモリを割り当てます。キャッシュサイズの指定は必須です。後述の "total-max-size" キーワードを参照してください。

<a id="entry-6-2-1-max-age"></a>

**`max-age <seconds>`**

```haproxy
max-age <seconds>
```

有効期間の上限を定義します。有効期限には、レスポンスのCache-Controlヘッダーにあるs-maxage、なければmax-ageディレクティブの値と、この設定値のうち小さいほうを使用します。デフォルト値は60秒なので、デフォルトではオブジェクトを60秒より長くキャッシュできません。

<a id="entry-6-2-1-max-object-size"></a>

**`max-object-size <bytes>`**

```haproxy
max-object-size <bytes>
```

キャッシュするオブジェクトの最大サイズを定義します。"total-max-size" の半分を超えてはいけません。未設定の場合はキャッシュサイズの256分の一になります。"max-object-size" より大きいオブジェクトは、すべてキャッシュされません。

<a id="entry-6-2-1-max-secondary-entries"></a>

**`max-secondary-entries <number>`**

```haproxy
max-secondary-entries <number>
```

キャッシュ内で同じプライマリーキーを持つセカンダリーエントリーの同時存在数の上限を定義します。Varyのサポートを有効にする必要があります。デフォルト値は10で、正の整数を指定してください。

<a id="entry-6-2-1-process-vary"></a>

**`process-vary <on/off>`**

```haproxy
process-vary <on/off>
```

Varyヘッダーの処理を有効または無効にします。無効の場合、このヘッダーを含むレスポンスはキャッシュされません。有効の場合は、すべての受信リクエストについて、リクエストヘッダーの一部から予備的なハッシュを計算し、それを使って各リクエストのセカンダリーキーを構成します（RFC 7234#4.1参照）。これにはCPUコストがかかる場合があります。現在、セカンダリーキーは 'accept-encoding'、'referer'、'origin' ヘッダーの内容から構成します。RFCでは 'origin' と 'referer' ヘッダーは単一値とされているため、いずれかを複数含むリクエストは不正な形式とみなすべきです。そのようなリクエストではセカンダリーキーを構成せず、キャッシュからレスポンスを配信することもありません。対処方法をサーバーに判断させるためです。デフォルト値はoff（無効）です。

<a id="entry-6-2-1-total-max-size"></a>

**`total-max-size <megabytes>`**

```haproxy
total-max-size <megabytes>
```

RAM上のキャッシュサイズをメガバイト単位で定義します。この領域は1kBのブロックに分割され、キャッシュエントリーが使用します。最大値は4095です。

### 6.2.2. proxyセクション {#section-6-2-2}

キャッシュを利用するproxyセクションでは、要求されたオブジェクトをキャッシュから検索するため、"http-request" ルールセットに "cache-use" アクションを含める必要があります。また、取得したオブジェクトをキャッシュに保存または更新するため、"http-response" ルールセットに "cache-store" アクションを含める必要があります。いずれのアクションにも任意で条件を指定できます。たとえば、キャッシュできないことがわかっているサブディレクトリでは "cache-use" を省略したり、キャッシュする価値がないcontent-typeでは "cache-store" を省略したりできます。キャッシュのインデックスキーは "cache-use" アクションの実行時に計算されるため、このアクションを省略すると、レスポンス処理時にキャッシュを更新することもありません。

例：

```text
backend bck1
  mode http

  http-request cache-use foobar
  http-response cache-store foobar
  server srv1 127.0.0.1:80

cache foobar
  total-max-size 4
  max-age 240
```
