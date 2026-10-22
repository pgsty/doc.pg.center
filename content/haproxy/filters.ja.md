---
title: "9. 対応するフィルター"
linkTitle: "9. フィルター"
weight: 200
description: "トレース、圧縮、SPOE、キャッシュ、FastCGI、OpenTracing、帯域制限フィルター"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/filters/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 9"
---

ここでは、公式にサポートするフィルターと、それぞれが受け付けるパラメーターを示します。コンパイルオプションによっては、利用できないフィルターもあります。利用可能なフィルターの一覧はhaproxy -vvに表示されます。

関連項目："filter"

## 9.1. トレース {#section-9-1}

filter trace [name `<name>`] [random-forwarding] [max-fwd `<max>`] [hexdump]

引数：

```text
<name>               メッセージに表示する任意の名前です。
                     名前を指定しない場合は、"TRACE"を使います。

<quiet>              トレースメッセージを抑止します。

<random-forwarding>  解析済みデータをランダムな量ずつ転送する機能を有効にします。
                     デフォルトでは、このフィルターは解析済みのデータをすべて転送します。
                     このパラメーターを指定すると、解析済みデータのうち
                     ランダムな量だけを転送します。

<max>                一度に転送できるデータの最大量です。"max-fwd"オプションは
                     ランダム転送と併用できます。
                     <max>は正の整数でなければなりません。
                     0は制限なしを意味します。

<hexdump>             サーバーとクライアントへ転送するデータをすべてダンプします。
```

このフィルターは、新しいフィルターを開発する際のひな形として使えます。すべてのコールバックを定義し、それぞれについて有用な情報を含むメッセージを標準エラーストリーム（stderr）へ出力します。ほかのフィルターの動作や、HAProxy自体の動作のデバッグに役立つ場合があります。

`<random-parsing>`や`<random-forwarding>`パラメーターを使うと、処理に遅延を加え、クライアントとサーバーの間で交換されるデータを解析するフィルターの動作をテストできます。

## 9.2. HTTP圧縮 {#section-9-2}

filter comp-req

"compression"設定に従って、HTTPリクエストの圧縮を明示的に試みるフィルターを有効にします。"compression direction request"を暗黙に設定します。

filter comp-res

"compression"設定に従って、HTTPレスポンスの圧縮を明示的に試みるフィルターを有効にします。"compression direction response"を暗黙に設定します。

filter compression（非推奨）

後方互換性のための別名で、"comp-req"と"comp-res"の両フィルターを有効にするのと機能的に同等です。適切な動作を設定するには、"compression"キーワードを使わなければなりません。

HTTP圧縮は、HAProxy 1.7でフィルターへ移されました。HTTP圧縮を有効化・設定するには、引き続き"compression"キーワードを使わなければなりません。ほかのフィルターを使わない場合は、それだけで十分です。cacheやfcgi-appを有効にして使う場合も、それだけで十分です。この場合、圧縮は常にレスポンスがキャッシュへ保存された後に行われます。ただし、同じリスナー/フロントエンド/バックエンドで、cacheやfcgi-app以外のフィルターを一つでも使う場合は、filter行を明示してHTTP圧縮を有効にしなければなりません。これは、フィルターの評価順を決めるために重要です。

関連項目："compression"、キャッシュフィルターについては[セクション9.4](/ja/haproxy/filters/#section-9-4)、fcgi-appフィルターについては[セクション9.5](/ja/haproxy/filters/#section-9-5)。

## 9.3. Stream Processing Offload Engine（SPOE） {#section-9-3}

filter spoe [engine `<name>`] config `<file>`

引数：

```text
<name>      設定ファイル内で対象のスコープを探すために使うエンジン名です。
            指定しない場合は、ファイル全体を解析します。

<file>      エンジン設定ファイルのパスです。このファイルには、複数の
            エンジンの設定を含められます。その場合、それぞれの設定を
            独自のスコープに置かなければなりません。
```

Stream Processing Offload Engine（SPOE）は、外部コンポーネントと通信するフィルターです。階層型アプリケーションで、ストリームに対する特定の処理を外部へ任せられます。外部コンポーネントと、それらとの間で交換する情報の大部分は、専用ファイルで設定します。また、HAProxy設定内に定義した専用のバックエンドも必要です。

SPOEは、独自のバイナリプロトコルであるStream Processing Offload Protocol（SPOP）を使って外部コンポーネントと通信します。

ストリームでSPOEを使うと、外部コンポーネントとの通信を担当する専用ストリームが作られます。元のストリームは、この"SPOE"ストリームの親ストリームになります。そのため、"SPOE"ストリームから元のストリームの変数を取得できます。詳細は、変数についての[セクション2.8](/ja/haproxy/configuration-basics/#section-2-8)を参照してください。

SPOE設定とSPOP仕様の詳しい情報は、"doc/SPOE.txt"を参照してください。

## 9.4. キャッシュ {#section-9-4}

filter cache `<name>`

引数：

```text
<name>      このフィルターが使うcacheセクションの名前です。
```

キャッシュは、キャッシュ可能なレスポンスを保存するためにフィルターを使います。キャッシュをいつ、どのように使うかは、HTTPルールの"cache-store"と"cache-use"で定義しなければなりません。デフォルトでは、対応するフィルターが暗黙に定義されます。fcgi-appやcompression以外のフィルターを使わない場合は、それだけで十分です。この場合、圧縮フィルターは常にキャッシュフィルターの後に評価されます。ただし、同じリスナー/フロントエンド/バックエンドで、compressionやfcgi-app以外のフィルターを一つでも使う場合は、filter行を明示してキャッシュを使わなければなりません。これは、フィルターの評価順を決めるために重要です。

関連項目：圧縮フィルターについては[セクション9.2](/ja/haproxy/filters/#section-9-2)、fcgi-appフィルターについては[セクション9.5](/ja/haproxy/filters/#section-9-5)、キャッシュについては[セクション6](/ja/haproxy/cache/)。

## 9.5. Fcgi-app {#section-9-5}

filter fcgi-app `<name>`

引数：

```text
<name>      このフィルターが使うfcgi-appセクションの名前です。
```

FastCGIアプリケーションは、リクエスト経路ですべてのカスタムパラメーターを評価し、レスポンス経路でヘッダーを処理するためにフィルターを使います。`<name>`は、既存のfcgi-appセクションを参照しなければなりません。使うアプリケーションの定義には、"use-fcgi-app"ディレクティブを使うことを推奨します。デフォルトでは、対応するフィルターが暗黙に定義されます。cacheやcompression以外のフィルターを使わない場合は、それだけで十分です。ただし、同じバックエンドでcompressionやcache以外のフィルターを一つでも使う場合は、fcgi-app用のfilter行を明示しなければなりません。これは、フィルターの評価順を決めるために重要です。

関連項目："use-fcgi-app"、圧縮フィルターについては[セクション9.2](/ja/haproxy/filters/#section-9-2)、キャッシュフィルターについては[セクション9.4](/ja/haproxy/filters/#section-9-4)、FastCGIアプリケーションについては[セクション10](/ja/haproxy/fastcgi/)。

## 9.6. OpenTracing {#section-9-6}

OpenTracingフィルターは、HAProxyで分散トレースを直接利用できるようにします。Datadog、Jaeger、Lightstep、Zipkinなど、対応するトレーサーへOpenTracing準拠のリクエストを送ることで動作します。トレーサーは推奨順ではなく、アルファベット順に記載している点に注意してください。

この機能は、HAProxyをUSE_OT=1でビルドした場合にのみ有効です。

OpenTracingフィルターは、HAProxyの設定で明示的に指定して有効にします。指定しなければ、OpenTracingフィルターはHAProxyの動作に一切関与しません。

filter opentracing [id `<id>`] config `<file>`

引数：

```text
<id>        設定ファイル内で対象のスコープを探すために使うOpenTracing
            フィルターのIDです。指定しない場合は、デフォルトで'ot-filter'を
            使います。設定ファイルでスコープを指定しない場合は、定義されている
            すべてのOpenTracingフィルターに適用されます。

<file>      OpenTracing設定ファイルのパスです。同じファイルに、複数の
            OpenTracingフィルターの設定を同時に含められます。その場合は、
            スコープを定義せず同じ設定をすべてのフィルターに適用するか、
            各フィルターに独自のスコープを定義しなければなりません。
```

フィルターの動作、設定、使い方に関する詳しいドキュメントは、addons/otディレクトリにあります。

注意：OpenTracing自体が開発元による保守・サポートを終了しているため、新しい設計ではOpenTracingフィルターを使わないことを推奨します。OpenTracingは3.3で非推奨となり、3.5で削除されます。OpenTelemetryに基づく代替フィルターは3.4から利用でき、完全なビルド手順は現在、次の場所にあります。

```text
https://github.com/haproxytech/haproxy-opentelemetry/
```

## 9.7. 帯域制限 {#section-9-7}

```haproxy
filter bwlim-in  <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-out <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-in  <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
filter bwlim-out <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
```

引数：

```text
<name>      'set-bandwidth-limit'アクションが、特定の帯域制限フィルターを
            参照するために使うフィルター名です。

<size>      指定期間内に転送できる最大バイト数です。ストリームごとの
            帯域制限フィルターと共有の帯域制限フィルターの両方で、
            必ず指定しなければなりません。HAProxyのサイズ形式に従い、
            バイト単位で表します。

<pattern>   セクション7.3で説明するサンプル式のルールです。
            どの要素を解析、抽出、結合し、カウンターを更新する
            テーブルエントリーの選択に使うかを定義します。
            共有の帯域制限フィルターでのみ、必ず指定しなければなりません。

<table>     デフォルトのテーブル（現在のプロキシで宣言された
            スティックテーブル）の代わりに使う、任意のテーブルです。
            共有の帯域制限フィルターでのみ指定できます。

<time>      帯域制限のレートの評価に使う、デフォルトの期間です。
            ストリームごとの帯域制限フィルターでのみ指定できます。
            HAProxyの時間形式に従い、ミリ秒単位で表します。

<min-size>  ストリームが一度に転送する最小バイト数です。任意で指定でき、
            最後のパケットはこれより小さくてもかまいません。
            ストリームごと・共有の両方の帯域制限フィルターで指定できます。
            HAProxyのサイズ形式に従い、バイト単位で表します。
```

ストリーム単位でデータの転送速度を制限するには、帯域制限フィルターを使うことを推奨します。ひいては、リソースが消費するネットワーク帯域を制限できます。複数の帯域制限フィルターを使えます。たとえば、クライアントが帯域全体を使い切ってほかのクライアントに不利益を与えないよう、送信元アドレスごとの制限を設け、同じクライアントの複数接続を公平に扱うため、さらにストリームごとの制限を設けられます。

これらのフィルターの定義順序は重要です。一つのストリームで複数の帯域制限フィルターを有効にすると、定義順に適用されます。ほかのフィルターの定義順序も影響することを理解しておく必要があります。たとえば、HTTP圧縮フィルターが帯域制限フィルターの前か後かによって、制限が圧縮後のペイロードに適用されるかどうかが変わります。キャッシュフィルターについても同様です。

帯域制限フィルターには二種類あります。一つはデフォルトの制限をストリームごとに適用します。もう一つはスティックテーブルを使い、同じテーブルエントリーを共有するすべてのストリームに、制限を均等に分配します。

さらに、同じフィルターでも、使うキーワードに応じて、クライアントから受信してサーバーへ転送する入力データか、サーバーから受信してクライアントへ送る出力データのどちらを制限するかが変わります。入力データには"bwlim-in"、出力データには"bwlim-out"キーワードを使わなければなりません。いずれも、転送するデータにストリーム単位で帯域制限を適用します。

帯域制限は、接続単位ではなくストリーム単位で適用します。多重化プロトコル（H2、H3、FastCGI）では、同じ接続内のストリームに異なる制限を設定できます。

ストリームごとの帯域制限フィルターでは、デフォルトの期間と制限を定義しなければなりません。名前のとおり、ストリームの帯域制限レートを設定するためのデフォルト値です。ただし、この種類のフィルターに限り、TCP/HTTPの"set-bandwidth-limit"アクションでフィルターを有効にする際に、サンプル式でこれらの値を再定義できます。

共有の帯域制限フィルターでは、入力・出力のどちらのデータに適用するかに応じて、使うスティックテーブルに対応するバイトレート情報を保存しなければなりません。入力データを制限するには"bytes_in_rate(`<period>`)"カウンターを保存し、出力データを制限するには"bytes_out_rate(`<period>`)"カウンターを使わなければなりません。

最後に、帯域制限フィルターが、特定のストリームで一度に転送できる最小バイト数を設定できます。小さすぎる単位での転送を避け、CPU使用率を下げるために使うことを推奨します。値は慎重に決めなければなりません。小さすぎるとCPU使用率が高くなり、大きすぎるとレイテンシーが増える可能性があります。設定した帯域制限とも密接に関係します。制限値に近すぎると、一度に多くのバイトを消費するため、上限を超えないよう途中で一時停止が入る場合があります。適切な値はフィルターの設定に大きく依存します。まずTCP MSSの約2倍、通常は2896バイト程度から始め、実験して調整するのがよいでしょう。

例：

```text
frontend http
    bind *:80
    mode http

    # If this filter is enabled, the stream will share the download limit
    # of 10m/s with all other streams with the same source address.
    filter bwlim-out limit-by-src key src table limit-by-src limit 10m

    # If this filter is enabled, the stream will be limited to download at 1m/s,
    # independently of all other streams.
    filter bwlim-out limit-by-strm default-limit 1m default-period 1s

    # Limit all streams to 1m/s (the default limit) and those accessing the
    # internal API to 100k/s. Limit each source address to 10m/s. The shared
    # limit is applied first. Both are limiting the download rate.
    http-request set-bandwidth-limit limit-by-strm
    http-request set-bandwidth-limit limit-by-strm limit 100k if { path_beg /internal }
    http-request set-bandwidth-limit limit-by-src
    ...

backend limit-by-src
    # The stickiness table used by <limit-by-src> filter
    stick-table type ip size 1m expire 3600s store bytes_out_rate(1s)
```

関連項目："tcp-request content set-bandwidth-limit"、"tcp-response content set-bandwidth-limit"、"http-request set-bandwidth-limit"、"http-response set-bandwidth-limit"。
