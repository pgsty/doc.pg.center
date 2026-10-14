---
title: "13. セキュリティに関する考慮事項"
linkTitle: "13. セキュリティ"
weight: 370
description: "権限の分離、攻撃対象領域、Linux capabilities、安全な運用"
icon: fa-solid fa-shield-halved
module: [HAPROXY]
categories: [タスク]
aliases:
  - /haproxy/management/security/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 13"
---

HAProxyは、非常に限られた権限で動作するよう設計されています。標準的な使用方法は、chroot jailに隔離したうえで、jail内で何の権限も持たない非rootユーザーに権限を落とすことです。これにより、将来脆弱性が発見されても、侵害がシステムの他の部分に影響しないようにします。

chrootを実行するには、最初にrootユーザーとして起動する必要があります。手作業でchroot環境を構築し、その中でプロセスを起動するのは意味がありません。そのような環境の構築は面倒で、適切に保守されることがなく、メインのファイルシステムよりはるかに多くの問題を抱えがちです。侵害された場合、侵入者はその専用のファイルシステムを利用できます。残念ながら、多くの管理者が「rootとして起動する」ことと「rootとして動作する」ことを混同し、haproxyの起動前にuidを変更してしまうため、実際のセキュリティ制限が弱くなっています。

HAProxyは、次の処理を行うためにrootとして起動する必要があります。

- ファイル記述子の上限を調整する。
- 特権ポート番号にバインドする。
- 特定のネットワークインターフェースにバインドする。
- 他のホストのアドレスで透過的にリッスンする。
- chroot jail内に自身を隔離する。
- 別の非特権UIDに切り替える。

次の処理を行うには、HAProxyをrootとして動作させる必要がある場合があります。

- 送信接続を特定のインターフェースにバインドする。
- 送信接続を特権送信元ポートにバインドする。
- 送信接続を他のホストのアドレスに透過的にバインドする。

ほとんどのユーザーは「rootとして動作する」必要はありません。一方、ほとんどの用途では「rootとして起動する」必要があります。

安全な設定には、次の要素を含めます。

- アクセス権限が一切ない空の場所を指すchroot文。UNIXのコマンドラインでは、次のように準備できます。

```shell
# mkdir /var/empty && chmod 0 /var/empty || echo "Failed"
```

HAProxy設定のglobalセクションでは、次のように参照します。

```text
chroot /var/empty
```

- globalセクション内のuid/user文とgid/group文の両方。

```text
user haproxy
group haproxy
```

- CLIへのアクセスを許可するユーザーまたはグループに合わせてmode、uid、gidを設定したstatsソケット。これにより、他のユーザーからのアクセスを防ぎます。

```text
stats socket /var/run/haproxy.stat uid hatop gid hatop mode 600
```

## 13.1. Linux capabilitiesのサポート {#section-13-1}

バージョンv2.9以降、haproxyはLinux capabilitiesをサポートしています。バイナリーがUSE_LINUX_CAP=1でコンパイルされている場合、rootユーザーから非rootユーザーに切り替える際に、'setcap' キーワードで指定されたcapabilityを保持できます。

バージョンv3.1以降では、'setcap' キーワードで指定されたcapabilityが、管理者によってバイナリーファイルのPermittedセットに設定されているかも確認します（capgetシステムコール）。設定されていれば、非rootユーザーとして動作しながら、それらをプロセスのEffectiveセットに移します（capsetシステムコール）。

これは、透過プロキシモードや特権ポートへのバインドなど、haproxyをrootとして起動し、動作させる必要があるすべての用途をなくすための対応です。

'setcap' キーワードは、次のネットワークcapabilityをサポートします。

- cap_net_admin: 透過プロキシ、特定のネットワークインターフェースへのソケットのバインド、set-markアクションの使用。
- cap_net_raw（cap_net_adminのサブセット）: 透過プロキシ。
- cap_net_bind_service: 特権ポートへのソケットのバインド。
- cap_sys_admin: 特定のネットワーク名前空間内でのソケットの作成。

HAProxyは、これらのcapabilityが 'setcap' の引数に列挙されていない限り、PermittedセットからEffectiveセットへ移しません。'setcap' キーワードとサポートされるcapabilityの詳細は、設定ガイドの第3.1章「プロセス管理とセキュリティ」を参照してください。

管理者は、次のコマンドでhaproxyバイナリーファイルのPermittedセットに必要なcapabilityを追加できます。

例：

```haproxy
# setcap cap_net_admin,cap_net_bind_service=p /usr/local/sbin/haproxy
```

追加したcapabilityは、プロセスの起動後にそのPermittedセットで確認できます。同じcapabilityを 'setcap' キーワードの引数に指定していれば、プロセスのEffectiveセットでも確認できる場合があります。次のコマンドで確認できます。

例：

```haproxy
# grep Cap /proc/<haproxy PID>/status
```

    CapInh: 0000000000000000
    CapPrm: 0000000000001400
    CapEff: 0000000000001400
    CapBnd: 000001ffffffffff
    CapAmb: 0000000000000000

setcapとcapabilityのセットの詳細は、Linuxのマニュアルページcapabilities(7) を参照してください。

透過プロキシや、特定のネットワーク名前空間内でのソケットの作成などの用途では、設定ファイルのパーサーがcap_net_raw、cap_sys_admin、その他のサポート対象capabilityが必要であることを検出します。その後、初期化段階でhaproxyプロセスが、それらを自身のEffectiveセットに設定できるか確認します。SELinuxやSeccompなどのセキュリティモジュールによるシステムコール制限のためcapgetやcapsetが失敗するなど、設定できない場合は、診断用の警告を出力します（-dDを指定して起動します）。

システム設定の異なる多数のプラットフォームをサポートしているため、特権ポートへのバインドが行われるかどうかを、パーサーが設定ファイルだけから判断することはできません。そのため、非rootでの動作など権限が不足する場合は、次のようなアラートメッセージを出してプロセスが終了するだけです。設定とhaproxyバイナリーのcapabilityセットは、ユーザー自身が再確認する必要があります。

例：

```shell
$ haproxy -dD -f haproxy.cfg
...
[ALERT]    (96797): Binding [haproxy.cfg:36] for frontend fe: cannot bind socket (Permission denied) for [0.0.0.0:80]
[ALERT]    (96797): [haproxy.main()] Some protocols failed to start their listeners! Exiting.
```
