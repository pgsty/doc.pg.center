---
title: "PgBouncer のコンパイルとインストール"
linkTitle: "インストール"
weight: 40
description: "PgBouncer のコンパイルとインストール手順"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [チュートリアル]
aliases: [/pgbouncer/install/]
upstream_link: "https://www.pgbouncer.org/install.html"
---

--------

## Building {#building}

PgBouncer はコンパイルするためのいくつかの要素に依存しています：

* [GNU Make] 3.81+
* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+（TLS 機能用）
* (オプション) [c-ares] は Libevent の evdns の代替として利用可能
* (オプション) LDAP ライブラリ
* (オプション) PAM ライブラリ

[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

依存関係をインストールしたら、次のように実行します：

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

Git からビルドする場合、または Windows 用にビルドする場合は、以下の別途のビルド手順を参照してください。

--------

## DNS ルックアップサポート {#dns-lookup-support}

PgBouncer は接続時にホスト名の照合を行いますが、設定の読み込み時に一度だけ行うのではなく、接続ごとに実行します。これには非同期 DNS 実装が必要です。以下の表は、サポートされるバックエンドとその照合順序を示しています。

| バックエンド                    | 平行処理 | EDNS0 (1) | /etc/hosts | SOA ルックアップ (2) | 備考                                  |
|----------------------------|----------|-----------|------------|----------------|---------------------------------------|
| c-ares                     | はい     | はい      | はい       | はい            | 1.10 以前では IPv6+CNAME にバグあり     |
| evdns, libevent 2.x        | はい     | いいえ    | はい       | いいえ           | /etc/hosts の更新を確認しない         |
| getaddrinfo_a, glibc 2.9+  | はい     | はい (3)  | はい       | いいえ           | non-glibc では N/A                     |
| getaddrinfo, libc          | いいえ   | はい (3)  | はい       | いいえ           | pthreads を必要とする                 |

1. EDNS0 は、1 つのホスト名の背後に 8 件以上のアドレスを設定する場合に必要です。
2. SOA の照会は、ゾーンシリアルの変更時にホスト名を再確認するために必要です。
3. EDNS0 を有効にするには、`options edns0` を `/etc/resolv.conf` に追加してください。

c-ares は最も機能が充実しており、ほとんどの用途およびバイナリパッケージング（十分に新しいバージョンが利用可能な場合）に推奨されます。Libevent の組み込み evdns も、記載された制限を除き多くの用途に適しています。他のバックエンドは現在、ほとんどがレガシーな選択肢であり、テストもほとんど行われていません。

デフォルトでは、c-ares が利用可能であればそれを使用します。`configure --with-cares` を指定することで c-ares の使用を強制し、`--without-cares` を指定することで無効化できます。c-ares を使用しない（見つからないか無効化されている）場合、Libevent が使用されます。Libevent の evdns の使用を無効にするには `--disable-evdns` を指定し、libc に基づく実装にフォールバックします。

--------

## PAM 認証 {#pam-authentication}

PAM 認証を有効にするには、`./configure` にフラグ `--with-pam` を設定します（デフォルト値は no）。PAM サポートでコンパイルされた場合、ユーザーを PAM で検証するための新しいグローバル認証タイプ `pam` が利用可能になります。

--------

## LDAP 認証 {#ldap-authentication}

LDAP 認証を有効にするには、`./configure` にフラグ `--with-ldap` を設定します（デフォルト値は no）。LDAP サポート付きでコンパイルされた場合、ユーザーを LDAP を使って検証するための新しいグローバル認証タイプ `ldap` が利用可能になります。

--------

## systemd 統合 {#systemd-integration}

systemd 統合を有効にするには、`configure` オプションを使用してください。これにより、`--with-systemd` を使用できるほか、systemd 253 以降では `Type=notify`（または `Type=notify-reload`）も利用可能です。ソケット活性化も可能です。例については `etc/pgbouncer.service` および `etc/pgbouncer.socket` を参照してください。

--------

## Git からビルドする {#building-from-git}

GitからPgBouncerをビルドするには、`configure` を実行する前にヘッダーおよび設定ファイルを生成する必要があります。

	$ git clone https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

デフォルトでは、すべてのファイルが `/usr/local` にインストールされます。
`configure` に1つ以上のコマンドラインオプションを指定できます。
利用可能なオプションおよび設定をカスタマイズする環境変数を確認するには、`./configure --help` を実行してください。

追加で必要なパッケージ: autoconf, automake, libtool, pandoc

--------

## テスト {#testing}

テストディレクトリ内の [`README.md` ファイル][1] を参照して、テストの実行方法を確認してください。

[1]: https://github.com/pgbouncer/pgbouncer/blob/master/test/README.md

--------

## Windows 上でのビルド {#building-on-windows}

Windows でのみサポートされているビルド環境は MinGW です。Cygwin および Visual $ANYTHING はサポートされていません。

MinGW でビルドするには、通常通り以下を実行します：

	$ ./configure
	$ make

Unix からクロスコンパイルする場合:

	$ ./configure --host=i586-mingw32msvc

LDAP ビルドオプションは現在、Windows ではサポートされていません。

--------

## Windows 上での実行 {#running-on-windows}

コマンドラインから実行する場合は通常通りですが、`-d`（デーモン化）、`-R`（再起動）、`-u`（ユーザー切り替え）のオプションは機能しません。

Windows サービスとして PgBouncer を実行するには、`service_name` パラメータを設定してサービス名を指定する必要があります。その後、以下を実行します。

	$ pgbouncer -regservice config.ini

サービスをアンインストールするには：

	$ pgbouncer -unregservice config.ini

Windows イベントログを使用するには、設定ファイルで `syslog = 1` を設定してください。
ただし、その前に `pgbevent.dll` の登録が必要です。

	$ regsvr32 pgbevent.dll

登録を解除するには、次のようにします：

	$ regsvr32 /u pgbevent.dll
