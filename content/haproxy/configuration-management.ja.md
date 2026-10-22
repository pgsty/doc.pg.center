---
title: "10. 設定管理を容易にする方法"
linkTitle: "10. 設定管理"
weight: 340
description: "大規模なHAProxy設定の保守を容易にする方法"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [タスク]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 10"
---

クラスターを構成する2つのHAProxyノードが、少数のアドレスを除いてまったく同じ設定を共有することはよくあります。ノードごとに設定の複製を管理すると、その内容は必然的に食い違っていきます。設定に環境変数を組み込めば、システム全体の環境変数をいくつか変えるだけで、複数の設定でまったく同じファイルを共有できます。この機能はバージョン1.5で導入され、当初はアドレスにのみ環境変数を含めることができました。1.6では対応範囲が広がり、どこでも環境変数を使用できます。構文はUNIXシェルと同じで、変数はドル記号 ('\$')、開き波括弧 ('{')、変数名、閉じ波括弧 ('}') の順に記述します。アドレスを除き、環境変数は二重引用符で囲まれた引数の中でのみ解釈されます。これは、ドル記号を含む正規表現を使用する既存の設定を壊さないために必要な制限です。

環境変数を使用すると、アドレスだけが異なる複数の拠点で動作する設定を簡単に記述できます。一部の設定からパスワードを取り除くためにも利用できます。次の例では、起動時にinitスクリプトが "site1.env" ファイルを読み込みます。

```shell
$ cat site1.env
LISTEN=192.168.1.1
CACHE_PFX=192.168.11
SERVER_PFX=192.168.22
LOGGER=192.168.33.1
STATSLP=admin:pa$$w0rd
ABUSERS=/etc/haproxy/abuse.lst
TIMEOUT=10s

$ cat haproxy.cfg
global
    log "${LOGGER}:514" local0

defaults
    mode http
    timeout client "${TIMEOUT}"
    timeout server "${TIMEOUT}"
    timeout connect 5s

frontend public
    bind "${LISTEN}:80"
    http-request reject if { src -f "${ABUSERS}" }
    stats uri /stats
    stats auth "${STATSLP}"
    use_backend cache if { path_end .jpg .css .ico }
    default_backend server

backend cache
    server cache1 "${CACHE_PFX}.1:18080" check
    server cache2 "${CACHE_PFX}.2:18080" check

backend server
    server cache1 "${SERVER_PFX}.1:8080" check
    server cache2 "${SERVER_PFX}.2:8080" check
```
