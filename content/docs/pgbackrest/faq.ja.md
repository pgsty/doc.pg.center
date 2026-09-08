---
title: "よくある質問"
linkTitle: "FAQ"
weight: 70
description: "pgBackRestのバックアップ、リストア、構成、トラブルシューティングに関するよくある質問。"
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [リファレンス]
aliases: [/pgbackrest/faq/]
upstream_link: "https://pgbackrest.org/faq.html"
---

--------

## はじめに {#introduction}

よくある質問では、ユーザーガイド、構成リファレンス、コマンドリファレンスで説明されている場合も、されていない場合もある個別の疑問について、詳しく説明します。ここで問題に関する情報が見つからない場合は、pgBackRestの[GitHubのIssue一覧](https://github.com/pgbackrest/pgbackrest/issues)も有用な情報源です。


--------

## 「could not find WAL segment」エラーが発生した場合はどうすればよいですか。 {#what-if-i-get-the-could-not-find-wal-segment-error}

このエラーはさまざまな問題によって発生する可能性があります。たとえば、次のような原因が考えられます。

- `archive_command`の設定ミス
- pgBackRest構成ファイルの設定ミス
- ネットワークまたは権限の問題
- サードパーティー製品（S3、Swift、Minioなど）の設定の問題
- アーカイブ待ちのWALが大量にキューにたまっている

次の確認を推奨します。

- PostgreSQLの`archive_command`を確認する
- 各ホストのpgBackRest構成設定を確認する（たとえば、リポジトリホストに`pg*`の設定、pgホストに`repo*`の設定が指定されているか）
- `--archive-timeout`をpgBackRest構成ファイル内の値（またはデフォルト値）より大きくして`check`コマンドを実行し、WALキューを処理し終えるまでにより長い時間が必要かどうかを確認する。システムで大量のWALを生成している場合は、[非同期アーカイブ](/ja/docs/pgbackrest/user-guide/#asynchronous-archiving)の構成を検討する


--------

## バックアップセットを手動で削除するにはどうすればよいですか。 {#how-do-i-manually-purge-a-backup-set}

[コマンドリファレンス：Expire](/ja/docs/pgbackrest/command/expire/)で説明しているとおり、`--set`オプションを使用してフルバックアップセットを期限切れとして削除できます。


--------

## コマンドごとにオプションを個別に設定するにはどうすればよいですか。 {#how-can-i-configure-options-independently-for-each-command}

pgBackRestでは、構成ファイル内でコマンドごとにオプションを個別に設定できます。[クラスターのstanzaの構成](/ja/docs/pgbackrest/user-guide/#configure-cluster-stanza)で、この機能とオプションの優先順位を詳しく説明しています。

たとえば、コマンドごとに`process-max`オプションを最適化できます。

```ini
[global]
# used where not overridden
process-max=2

[global:backup]
# more cores for backup
process-max=4

[global:restore]
# all the cores for restore
process-max=8

[global:archive-push]
# more cores for archive-push
process-max=3

[global:archive-get]
# fewer cores for archive-get
process-max=1
```


--------

## S3バケット名にドット（ピリオド）を使用できますか。 {#can-i-use-dots-periods-in-my-s3-bucket-name}

RFC-2818では、ワイルドカードをドット（.）に一致させることを認めていないため、S3バケット名にドットを含めてはなりません。S3バケット名にドットが含まれると、「unable to find hostname 'my.backup.bucket.s3.amazonaws.com' in certificate common name or subject alternative names」などのエラーが発生します。

例外は`repo-s3-uri-style=path`です。これは、バケットをホストではなくURIの先頭に付加します。バケットがホスト名の一部ではないため、証明書はエンドポイントのみと照合され、バケット名内のドットは問題になりません。ただし、すべてのS3互換オブジェクトストアがパス形式のURIをサポートしているわけではありません。


--------

## 以前のバージョンのpgBackRestのパッケージはどこにありますか。 {#where-can-i-find-packages-for-older-versions-of-pgbackrest}

[apt.postgresql.org](https://apt.postgresql.org)リポジトリでは、[以前のバージョンのアーカイブ](https://apt-archive.postgresql.org)を管理しています。Debianでも、すべてのテストビルドの[スナップショット](https://snapshot.debian.org/binary/pgbackrest/)を管理しています。


--------

## `backup-standby=y`でスタンバイデータベースが停止していると、バックアップが失敗するのはなぜですか。 {#why-does-a-backup-attempt-fail-when-backup-standbyy-and-the-standby-database-is-down}

スタンバイからのバックアップを構成する主な目的は、プライマリーの負荷を減らすことです。そのため、スタンバイが停止したときにバックアップをプライマリーへ切り替えると、多くの場合、その目的を果たせなくなります。システムですでに障害が発生している状況で、プライマリーにさらに負荷をかけることは推奨しません。比較的新しいバックアップがあれば、バックアップ取得は緊急の作業ではありません。重要なのは、WALのアーカイブを遅れずに続けることです。システムが再び安定してからバックアップを取得する時間は十分にあります。

どうしてもバックアップが必要であれば、スタンバイを増やすか、`backup-standby`を削除することが解決策になります。コマンドラインで`--no-backup-standby`を指定すれば上書きできるため、一度だけのバックアップのために構成を変更する必要はありません。


--------

## リポジトリはスタンバイホストに配置すべきですか。 {#should-i-setup-my-repository-on-a-standby-host}

いいえ。プライマリーとスタンバイのデータベースを構成する場合、フェイルオーバーをシームレスに処理できるように、pgBackRestの構成ファイルは対称にすることを推奨します。そうでなければ、フェイルオーバー時に構成を変更する必要があり、さらに問題が生じる可能性もあります。

詳しくは、ユーザーガイドの[専用リポジトリホスト](/ja/docs/pgbackrest/user-guide/#dedicated-repository-host)のセクションを参照してください。


--------

## 時刻を指定したポイントインタイムリカバリーが動作しないように見えるのはなぜですか。 {#time-based-point-in-time-recovery-does-not-appear-to-work-why}

時刻を指定したポイントインタイムリカバリーで最もよくある間違いは、目標時刻より前のバックアップセットを選び忘れることです。`--set`オプションを指定していない場合、pgBackRestは`--target=`で指定した時刻に向けて再生できるバックアップを見つけようとします。バックアップセットが見つからなければ、デフォルトで最新のバックアップをリストアします。ただし、最新のバックアップが目標時刻より後の場合、PostgreSQLは`--target=`を有効なものとみなさず無視するため、利用可能な最新時刻までWALリカバリーが進みます。

`--set`オプションを使用するには、`info`コマンドを実行し、終了タイムスタンプが目標時刻より前のバックアップを見つけてバックアップセットを選択します。リストアを実行するときに、`--set=BACKUP_LABEL`オプションを指定します。`BACKUP_LABEL`は選択したバックアップセットです。

詳しくは、ユーザーガイドの[ポイントインタイムリカバリー](/ja/docs/pgbackrest/user-guide/#point-in-time-recovery)のセクションを参照してください。


--------

## WALアーカイブの接尾辞は何を意味しますか。 {#what-does-the-wal-archive-suffix-mean}

接尾辞は、ファイルの整合性を検証するためのSHA1チェックサムです。省略する方法はありません。


--------

## バックアップの種類（フル、差分、増分）によってリストアにかかる時間は長くなりますか。 {#does-it-take-longer-to-restore-specific-backup-types-full-differential-incremental}

どの種類のバックアップも、リストアに必要な時間は同じです。リストアではバックアップマニフェストに基づいてファイルを取得します。増分バックアップや差分バックアップの場合、マニフェストが以前のバックアップ内のファイルを参照することがあります。バックアップの種類によって、バックアップの*作成*にかかる時間には差が生じることがありますが、ディスクI/O、ネットワークI/Oなどが同じであれば、リストア時間を決めるのはデータベースのサイズです。


--------

## ネットワークから隔離された環境で使用するために、バックアップをエクスポートするにはどうすればよいですか。 {#how-can-i-export-a-backup-for-use-in-a-network-isolated-environment}

pgBackRestは、バックアップやWALアーカイブの保存だけでなく、圧縮、暗号化、ファイルのバンドル化といった機能に必要な重要なメタデータの維持にもリポジトリを使用します。このため、非常に限定的で厳しい条件を満たさない限り、バックアップとWALファイルの一部を単純にコピーするだけでは、通常は動作しません。

ただし、データベースを単独で利用できる形でエクスポートし、USBなどで転送することが目的であれば、回避策があります。[`--archive-copy`](/ja/docs/pgbackrest/command/backup/#copy-archive-option---archive-copy)オプションを有効にしてバックアップを作成し、必要なWALセグメントがバックアップとともに保存されるようにします。その後、[`--type=none`](/ja/docs/pgbackrest/command/restore/#type-option---type) `--pg1-path=/your/target/path`を使用してリストアします。これにより、必要なWALファイルがすべて`pg_wal`に配置された、リストア済みのPostgreSQLデータディレクトリが生成されます。これは`pg_basebackup`で作成されるものと似ています。

このディレクトリを別のシステムにコピーすれば、PostgreSQLはpgBackRestリポジトリにアクセスせずにリカバリーできるはずです。

このバックアップのリカバリーではタイムラインの切り替えが発生しないため、このクラスターはエクスポート元のリポジトリにWALを送信すべきではないことに注意してください。新しいクラスターがネットワークから隔離された環境にある場合、これは問題にならないはずです。
