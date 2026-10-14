---
title: "10. FastCGIアプリケーション"
linkTitle: "10. FastCGI"
weight: 210
description: "FastCGIアプリケーションの設定、パラメーター、例、制限"
icon: fa-solid fa-bolt
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/fastcgi/
  - /docs/haproxy/configuration/fastcgi/
  - /haproxy/fastcgi/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

HAProxyは、Responder型のFastCGIアプリケーションへHTTPリクエストを送れます。この機能はHAProxy 2.1で追加されました。使うには、サーバーでFastCGIプロトコルを使うよう設定し（server行の"proto fcgi"キーワード）、そのサーバーを管理するバックエンドでFastCGIアプリケーションを設定して使用しなければなりません（proxyセクションの"use-fcgi-app"キーワード）。複数のFastCGIアプリケーションを定義できますが、一つのバックエンドが同時に使えるのは一つだけです。

HAProxyは、Responder型アプリケーションに関するFastCGI仕様の全機能を実装しています。特に、単一の接続上で複数のリクエストを多重化できます。

## 10.1. 設定 {#section-10-1}



### 10.1.1. Fcgi-appセクション {#section-10-1-1}

<a id="entry-10-1-1-fcgi-app"></a>

**`fcgi-app <name>`**

```haproxy
fcgi-app <name>
```

`<name>`という名前のFastCGIアプリケーションを宣言します。有効な設定とするには、少なくともドキュメントルートを定義しなければなりません。

<a id="entry-10-1-1-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

アクセスリストを宣言、または既存の宣言を補完します。

詳細は、[セクション4.2](/ja/docs/haproxy/proxies/#section-4-2)の"acl"キーワードと、ACLの使い方についての[セクション7](/ja/docs/haproxy/acls-and-samples/)を参照してください。FastCGIアプリケーション用に定義したACLは、そのアプリケーション専用です。ほかのアプリケーションやプロキシからは使えません。同様に、ほかのセクションで定義したACLも、FastCGIアプリケーションからは使えません。ただし、定義済みACLは利用できます。

<a id="entry-10-1-1-docroot"></a>

**`docroot <path>`**

```haproxy
docroot <path>
```

リモートホスト上のドキュメントルートを定義します。`<path>`は、FastCGIパラメーターSCRIPT_FILENAMEとPATH_TRANSLATEDのデフォルト値の構築に使います。必須の設定です。

<a id="entry-10-1-1-index"></a>

**`index <script-name>`**

```haproxy
index <script-name>
```

スラッシュ（"/"）で終わるURIの後に追加するスクリプト名を定義し、FastCGIパラメーターSCRIPT_NAMEのデフォルト値を設定します。任意の設定です。

例：

```text
index index.php
```

<a id="entry-10-1-1-log-stderr-global"></a>

**`log-stderr global`**

```haproxy
log-stderr global
log-stderr <target> [len <length>] [format <format>]
    [sample <ranges>:<sample_size>] <facility> [<level> [<minlevel>]]
```

FastCGIアプリケーションが出力するSTDERRメッセージのログ記録を有効にします。

詳細は、[セクション4.2](/ja/docs/haproxy/proxies/#section-4-2)の"log"キーワードを参照してください。任意の設定です。デフォルトでは、STDERRメッセージは無視されます。

<a id="entry-10-1-1-pass-header"></a>

**`pass-header <name> [ { if | unless } <condition> ]`**

```haproxy
pass-header <name> [ { if | unless } <condition> ]
```

FastCGIアプリケーションへ渡すリクエストヘッダーの名前を指定します。後ろに任意でACLに基づく条件を付けられ、その場合は、条件が真のときだけ評価されます。

ほとんどのリクエストヘッダーは、すでに"HTTP\_"の接頭辞付きでFastCGIアプリケーションから利用できます。そのため、このディレクティブが必要なのは、意図的に除外されているヘッダーを渡す場合だけです。現在は、"Authorization"、"Proxy-Authorization"、およびホップ単位のヘッダーが除外されています。

"Content-type"と"Content-length"ヘッダーは、すでにパラメーターへ変換されているため、FastCGIアプリケーションへ渡されることはありません。

<a id="entry-10-1-1-path-info"></a>

**`path-info <regex>`**

```haproxy
path-info <regex>
```

URLデコード済みのパスからscript-nameとpath-infoを抽出する正規表現を定義します。`<regex>`は二つのキャプチャーを持つことができ、最初のものはスクリプト名、二番目はpath-infoを取得します。最初のキャプチャーは必須で、二番目は任意です。そのため、path-infoを無視して、パスからscript-nameだけを抽出できます。これは任意の設定です。未定義の場合はパスの照合を行わず、FastCGIパラメーターのPATH_INFOとPATH_TRANSLATEDには値を設定しません。

セキュリティ上の理由から、この正規表現を定義した場合、URLデコード後のパスに改行文字とヌル文字を含めることは禁止されます。これらがあると、HAProxyでの正規表現の実行方法の制限により、照合が必ず失敗するためです。そのため、URLデコード済みのパスにどちらかの文字が見つかった場合は、クライアントへエラーを返します。ここでは驚き最小の原則を適用しています。

例：

```text
path-info ^(/.+\.php)(/.*)?$ # both script-name and path-info may be set
path-info ^(/.+\.php)        # the path-info is ignored
```

<a id="entry-10-1-1-option-get-values"></a>

**`option get-values`**

```haproxy
option get-values
no option get-values
```

接続管理に関する変数の取得を有効または無効にします。

HAProxyは、接続確立時にFCGI_GET_VALUESレコードを送信し、次の変数の値を取得できます。

    * FCGI_MAX_REQS     このアプリケーションが受け付ける同時リクエスト数の上限。

    * FCGI_MPXS_CONNS   このアプリケーションが接続の多重化を行わない場合は"0"、
                        行う場合は"1"。

この機能をサポートしないFastCGIアプリケーションもあります。また、応答を送った直後に接続を閉じるものもあります。そのため、このオプションはデフォルトで無効です。

FastCGIアプリケーションが受け付ける同時リクエスト数の上限は、接続に属する変数であることに注意してください。制限されるのは、接続ごとのストリーム数だけです。アプリケーション全体の負荷を制限する必要がある場合は、サーバーパラメーターの"maxconn"と"pool-max-conn"を設定しなければなりません。また、アプリケーションが接続の多重化をサポートしない場合、同時リクエスト数の上限は自動的に1に設定されます。

<a id="entry-10-1-1-option-keep-conn"></a>

**`option keep-conn`**

```haproxy
option keep-conn
no option keep-conn
```

応答を送信した後も接続を開いたままにするかどうかを、FastCGIアプリケーションへ指示します。

無効にすると、FastCGIアプリケーションはこのリクエストに応答した後、接続を閉じます。デフォルトでは有効です。

<a id="entry-10-1-1-option-max-reqs"></a>

**`option max-reqs <reqs>`**

```haproxy
option max-reqs <reqs>
```

このアプリケーションが受け付ける同時リクエスト数の上限を定義します。

接続確立時に変数FCGI_MAX_REQSを取得すると、このオプションが上書きされる場合があります。また、アプリケーションが接続の多重化をサポートしない場合、このオプションは無視されます。デフォルトは1です。

<a id="entry-10-1-1-option-mpxs-conns"></a>

**`option mpxs-conns`**

```haproxy
option mpxs-conns
no option mpxs-conns
```

接続の多重化のサポートを有効または無効にします。

接続確立時に変数FCGI_MPXS_CONNSを取得すると、このオプションが上書きされる場合があります。デフォルトでは無効です。

<a id="entry-10-1-1-set-param"></a>

**`set-param <name> <fmt> [ { if | unless } <condition> ]`**

```haproxy
set-param <name> <fmt> [ { if | unless } <condition> ]
```

このアプリケーションへ渡すFastCGIパラメーターを設定します。`<fmt>`で定義する値は、カスタムログ形式の規則に従わなければなりません（[セクション8.2.6](/ja/docs/haproxy/configuration-logging/#section-8-2-6)「カスタムログ形式」を参照）。後ろに任意でACLに基づく条件を付けられ、その場合は、条件が真のときだけ評価されます。

このディレクティブで、デフォルトのFastCGIパラメーターの値を上書きできます。評価結果が空文字列になる場合、そのルールは無視されます。これらのディレクティブは、宣言順に評価されます。

例：

```shell
# PHP only, required if PHP was built with --enable-force-cgi-redirect
set-param REDIRECT_STATUS 200

set-param PHP_AUTH_DIGEST %[req.hdr(Authorization)]
```

### 10.1.2. Proxyセクション {#section-10-1-2}

use-fcgi-app `<name>` バックエンドで使うFastCGIアプリケーションを定義します。

引数：

```text
<name>    使用するFastCGIアプリケーションの名前です。
```

このキーワードは、バックエンド機能を持ち、FastCGIサーバーが少なくとも一つあるHTTPプロキシでのみ利用できます。FastCGIサーバーとHTTPサーバーを混在させることはできますが、十分な理由がない限り推奨しません（詳細は制限についての[セクション10.3](/ja/docs/haproxy/fastcgi/#section-10-3)を参照）。一つのバックエンドに対して同時に定義できるアプリケーションは一つだけです。

バックエンドからFastCGIアプリケーションを参照すると、リクエストをFastCGIサーバーへ送らない場合でも、設定によっては一部の処理が行われる点に注意してください。パラメーターの設定や、アプリケーションへヘッダーを渡すためのルールが評価されます。

### 10.1.3. 例 {#section-10-1-3}

```haproxy
frontend front-http
    mode http
    bind *:80

    use_backend back-dynamic if { path_reg ^/.+\.php(/.*)?$ }
    default_backend back-static

backend back-static
    mode http
    server www A.B.C.D:80

backend back-dynamic
    mode http
    use-fcgi-app php-fpm
    server php-fpm A.B.C.D:9000 proto fcgi

fcgi-app php-fpm
    log-stderr global
    option keep-conn

    docroot /var/www/my-app
    index index.php
    path-info ^(/.+\.php)(/.*)?$
```

## 10.2. デフォルトのパラメーター {#section-10-2}

Responder型のFastCGIアプリケーションは、CGI/1.1プログラムと同じ役割を持ちます。CGI/1.1仕様（RFC3875）では、いくつかの変数をスクリプトへ渡さなければなりません。そのため、HAProxyはそれらに加え、FastCGIアプリケーションでよく使われる変数も設定します。これらの変数はすべて上書きできますが、注意が必要です。

```text
  +-------------------+-----------------------------------------------------+
  | AUTH_TYPE         | HAProxyがユーザー認証を行った場合、その方式を示しま |
  |                   | す。対応するのはBASIC認証方式だけです。             |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_LENGTH    | リクエストに付随するメッセージボディーのサイズです  |
  |                   | 。サイズが分かっているリクエストだけを有効と見なし  |
  |                   | 、アプリケーションへ送ります。                      |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_TYPE      | リクエストに付随するメッセージボディーの型です。設  |
  |                   | 定されない場合もあります。                          |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | DOCUMENT_ROOT     | アプリケーション設定で定義した、リモートホスト上の  |
  |                   | ドキュメントルートです。この配下でスクリプトを実行  |
  |                   | します。                                            |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | GATEWAY_INTERFACE | HAProxyがFastCGIアプリケーションとの通信に使うCGIの |
  |                   | 形式です。具体的には"CGI/1.1"に設定します。         |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_INFO         | URIのパス階層のうち、スクリプト自体を示す部分より後 |
  |                   | ろの部分です。設定するには"path-info"ディレクティブ |
  |                   | を定義しなければなりません。                        |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_TRANSLATED   | PATH_INFOが設定されている場合、その変換後の値です。 |
  |                   | DOCUMENT_ROOTとPATH_INFOを連結したものです。        |
  |                   | PATH_INFOが未設定なら、このパラメーターも設定しませ |
  |                   | ん。                                                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | QUERY_STRING      | リクエストのクエリー文字列です。設定されない場合も  |
  |                   | あります。                                          |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_ADDR       | リクエストを送信するクライアントのネットワークアド  |
  |                   | レスです。                                          |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_USER       | クライアントがユーザー認証の一環として提供したユー  |
  |                   | ザー識別文字列です。                                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_METHOD    | スクリプトがリクエストの処理に使うメソッドです。    |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_URI       | リクエストのURIです。                               |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_FILENAME   | スクリプトの絶対パス名です。DOCUMENT_ROOTと         |
  |                   | SCRIPT_NAMEを連結したものです。                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_NAME       | スクリプト名です。"path-info"ディレクティブが定義さ |
  |                   | れている場合は、スクリプト名で終わるURIのパス階層の |
  |                   | 先頭部分です。それ以外はURIのパス全体です。         |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_NAME       | クライアントリクエストの宛先サーバーのホスト名です  |
  |                   | 。"Host"ヘッダーがあればその値、なければクライアン  |
  |                   | ト側接続の宛先アドレスです。                        |
  |                   |                                                     |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PORT       | クライアント側接続の宛先TCPポートです。つまり、クラ |
  |                   | イアントが接続したポートです。                      |
  |                   |                                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PROTOCOL   | リクエストのプロトコルです。                        |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_SOFTWARE   | 文字列"HAProxy"の後に現在のHAProxyバージョンを続け  |
  |                   | た値です。                                          |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | HTTPS             | HTTPSプロトコル経由でスクリプトが呼び出された場合、 |
  |                   | 空でない値（"on"）を設定します。                    |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
```

## 10.3. 制限 {#section-10-3}

現在の実装には、いくつかの制限があります。最初は、一部のリクエストヘッダーをFastCGIアプリケーションへ見せない方法に関するものです。この処理は、接続確立前、バックエンド側のヘッダー解析時に行われます。この段階では、HAProxyはバックエンドがFastCGIアプリケーションを使うことは分かりますが、リクエストがFastCGIサーバーへ送られるかは分かりません。ヘッダーを隠すために、HTXメッセージから単純に削除します。そのため、最終的にHTTPサーバーへ送られた場合、そのサーバーはこれらのヘッダーを受け取りません。これが、同じバックエンドにFastCGIサーバーとHTTPサーバーを混在させることを推奨しない理由です。

同様に、"set-param"と"pass-header"のルールも、リクエストヘッダーの解析時に評価します。そのため、最終的にHTTPサーバーへ転送する場合も、常に評価されます。

"set-param"ルールを適用すると、HTXメッセージへ擬似ヘッダーが追加されます。そのため、HTTPヘッダーの書き換えと同様に、バッファーが満杯の場合は失敗することがあります。"set-param"ルールは、"http-request"ルールと領域を取り合います。

最後に、すべてのFastCGIパラメーターとHTTPヘッダーは、単一のFCGI_PARAMレコードで送ります。このレコードのエンコードは一度で行わなければならず、できなければ処理エラーを返します。つまり、エンコード後のFCGI_PARAMレコードは、バッファーのサイズを超えてはなりません。ただし、ここでは確保しておくべき予約領域はありません。
