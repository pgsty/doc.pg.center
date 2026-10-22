---
title: "PgBouncer のコンパイルとインストール"
linkTitle: "インストール"
weight: 40
description: "PgBouncer のコンパイルとインストール手順"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [チュートリアル]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/README.md"
---

--------

## ビルド {#building}

PgBouncer は、Autoconf ベースのビルドシステムでも、より新しい、まだ実験的な [Meson] ビルドシステムでもビルドできます。現時点では、本番用のビルドおよびパッケージングには Autoconf が推奨されます。Meson ビルドは将来のリリースでデフォルトになり、Autoconf ビルドは削除される見込みのため、Meson のテストと問題の報告を歓迎します。コンパイルにはいくつかの要素が必要です：

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+（TLS サポート用）
* C11 対応の C コンパイラー
* (オプション) [c-ares] は Libevent の evdns の代替として利用可能
* (オプション) LDAP ライブラリ
* (オプション) PAM ライブラリ

Meson ビルドにはさらに [Meson] 0.58+ と [Ninja] が必要であり、Autoconf ビルドには [GNU Make] 3.81+ が必要です。

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

依存関係がインストールされたら、Autoconf でビルドします：

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

または Meson でビルドします（実験的）：

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

Git からビルドする場合、または Windows 用にビルドする場合は、以下の別途のビルド手順を参照してください。

--------

## DNS ルックアップサポート {#dns-lookup-support}

PgBouncer は、設定の読み込み時に一度だけではなく、接続時にホスト名のルックアップを行います。これには非同期 DNS 実装が必要です。以下の表は、サポートされるバックエンドとその検出順序を示しています。

| バックエンド                    | 並列処理 | EDNS0 (1) | /etc/hosts | SOA ルックアップ (2) | 備考                                  |
|----------------------------|----------|-----------|------------|----------------|---------------------------------------|
| c-ares                     | はい     | はい      | はい       | はい            | 1.10 以前では IPv6+CNAME にバグあり     |
| evdns, libevent 2.x        | はい     | いいえ    | はい       | いいえ           | /etc/hosts の更新を確認しない         |
| getaddrinfo_a, glibc 2.9+  | はい     | はい (3)  | はい       | いいえ           | non-glibc では N/A                     |
| getaddrinfo, libc          | いいえ   | はい (3)  | はい       | いいえ           | pthreads を必要とする                 |

1. EDNS0 は、1 つのホスト名の背後に 8 件を超えるアドレスがある場合に必要です。
2. SOA の照会は、ゾーンシリアルの変更時にホスト名を再確認するために必要です。
3. EDNS0 を有効にするには、`options edns0` を `/etc/resolv.conf` に追加してください。

c-ares は最も機能が充実しており、ほとんどの用途およびバイナリパッケージング（十分に新しいバージョンが利用可能な場合）に推奨されます。Libevent の組み込み evdns も、記載された制限を除き多くの用途に適しています。他のバックエンドは現在、ほとんどがレガシーな選択肢であり、テストもほとんど行われていません。

デフォルトでは、c-ares が見つかった場合に使用されます。使用を強制するには `-Dcares=enabled`（configure の場合は `--with-cares`）、無効化するには `-Dcares=disabled`（configure の場合は `--without-cares`）を指定します。c-ares を使用しない（見つからないか無効化されている）場合、Libevent が使用されます。Libevent の evdns の使用を無効にして libc ベースの実装にフォールバックするには、`-Devdns=false`（configure の場合は `--disable-evdns`）を指定してください。

--------

## オプション機能 {#optional-features}

PAM、LDAP、systemd の各機能は meson によって自動検出されます。`-Dpam`、`-Dldap`、`-Dsystemd` の各オプションのデフォルトは `auto` であり、それぞれのライブラリが存在する場合にその機能がビルドされます。`-D<feature>=enabled` で強制的に有効に、`-D<feature>=disabled` で強制的に無効にできます。Autoconf ビルドはこれらの機能を自動検出しません。`--with-pam`、`--with-ldap`、または `--with-systemd` で明示的に有効にしてください。

--------

## PAM 認証 {#pam-authentication}

PAM サポート付きでコンパイルした場合、PAM を通じてユーザーを検証する新しいグローバル認証タイプ `pam` が利用可能になります。

--------

## LDAP 認証 {#ldap-authentication}

LDAP サポート付きでコンパイルした場合、LDAP を通じてユーザーを検証する新しいグローバル認証タイプ `ldap` が利用可能になります。

--------

## systemd 統合 {#systemd-integration}

systemd サポートでは、`Type=notify`（systemd 253 以降を使用している場合は `Type=notify-reload`）およびソケット活性化を利用できます。例については `etc/pgbouncer.service` および `etc/pgbouncer.socket` を参照してください。

--------

## Git からビルドする {#building-from-git}

Autoconf ビルドでは、`configure` を実行する前にヘッダーファイルおよび設定ファイルを生成する必要があります：

	$ git clone --branch pgbouncer_1_26_1 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

デフォルトでは、すべてのファイルが `/usr/local` にインストールされます。
`configure` に 1 つ以上のコマンドラインオプションを指定できます。
利用可能なオプションおよび設定をカスタマイズする環境変数を確認するには、`./configure --help` を実行してください。

Git からの Autoconf ビルドに追加で必要なパッケージ： autoconf, automake, libtool, pandoc

Meson ビルドでは、チェックアウトから直接ビルドできます。
man ページをビルドするには pandoc が必要です：

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

利用可能な `-D` オプションを一覧表示するには、`meson configure build` を実行してください。

--------

## テスト {#testing}

テストディレクトリ内の [`README.md` ファイル][1] を参照して、テストの実行方法を確認してください。

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/test/README.md

--------

## Windows 上でのビルド {#building-on-windows}

Windows でサポートされている唯一のビルド環境は MinGW です。Cygwin および Visual $ANYTHING はサポートされていません。

MinGW でビルドするには、通常の Autoconf ビルドを行います：

	$ ./configure
	$ make

または実験的な Meson ビルドを行います：

	$ meson setup build
	$ meson compile -C build

Autoconf を使って Unix からクロスコンパイルする場合：

	$ ./configure --host=i586-mingw32msvc

LDAP ビルドオプションは現在、Windows ではサポートされていません。

--------

## Windows 上での実行 {#running-on-windows}

コマンドラインからの実行は通常通りですが、`-d`（デーモン化）と `-u`（ユーザー切り替え）のスイッチは機能しません。

Windows サービスとして PgBouncer を実行するには、`service_name` パラメーターを設定してサービス名を指定する必要があります。その後、以下を実行します。

	$ pgbouncer -regservice config.ini

サービスをアンインストールするには：

	$ pgbouncer -unregservice config.ini

Windows イベントログを使用するには、設定ファイルで `syslog = 1` を設定してください。
ただし、その前に `pgbevent.dll` の登録が必要です。

	$ regsvr32 pgbevent.dll

登録を解除するには、次のようにします：

	$ regsvr32 /u pgbevent.dll
