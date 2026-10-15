---
title: "リリースノート"
linkTitle: "リリース"
weight: 60
description: "各バージョンの詳細な変更履歴を含むpgBackRestのリリース履歴。"
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## はじめに {#introduction}

pgBackRestのリリース番号は、メジャーとマイナーの2つの部分で構成されます。メジャーリリースでは、以前のメジャーリリースとの互換性が失われる*可能性があります*。ただし、v2リリースはv1リポジトリと完全に互換性があり、すべてのv1オプションを受け付けます。マイナーリリースには不具合修正や新機能が含まれることがありますが、リポジトリ形式は変更せず、オプションや名称の変更も極力避けます。v1リリースのドキュメントは[こちら](https://pgbackrest.org/1)を参照してください。リリースノートには「補足事項」が含まれる場合もありますが、このセクションの変更はドキュメントまたはテストスイートのみを対象とし、pgBackRestのコードには直接影響しません。


--------

## 本ドキュメントの対象となる安定版 {#current-stable-release}

このミラーはv2.59.3を対象としています。より新しいバージョンについては、[アップストリームのリリース履歴](https://pgbackrest.org/release.html)を参照してください。

### v2.59.3リリースノート {#v2593-release-notes}

*脆弱な暗号化サブキーのバグ*

*2026年10月4日リリース*

**重要な注意事項**: 以前のバージョンでは、システムのランダムデータへのアクセス時にエラーが発生すると、脆弱な暗号化サブキーやソルトが生成される可能性がありました。詳細は[脆弱な暗号化サブキーとソルト](/ja/pgbackrest/news/#weak-encryption)を参照してください。

**バグ修正:**

- 暗号化された情報ファイルとマニフェストの読み込み時にチェックサムエラーが発生する可能性がある問題を修正。 (*修正： j0uinim。レビュー： David Steele。*)
- 脆弱な暗号化サブキーやソルトが生成される可能性がある問題を修正。 (*修正： j0uinim。レビュー： David Steele, Stefan Fercot, Douglas J Hunley。*)


--------

## 安定版リリース {#stable-releases}


### v2.59.2リリースノート {#v2592-release-notes}

*PostgreSQL 19beta4のサポート*

*2026年9月27日リリース*

**バグ修正：**

- バックアップ中にファイルがゼロサイズに切り詰められた場合の、空のブロックマップの問題を修正しました。 (*レビュー：Douglas J Hunley。報告：JPCOSTA78。*)
- ドライバーにフィルターが渡された場合、読み取りの再試行を無効にしました。 (*レビュー：Douglas J Hunley。報告：megamaced。*)
- S3バージョン一覧のページ分割を修正しました。 (*レビュー：Douglas J Hunley, guruguruguru。報告：guruguruguru。*)
- SAS認証用のAzureバージョンヘッダーを設定するようにしました。 (*レビュー：Douglas J Hunley。報告：Florian Helmberger。*)
- サイズがゼロのバックアップ履歴ファイルで、非同期`archive-push`が停止する問題を修正しました。 (*修正：Andrew Kroh。レビュー：David Steele, Douglas J Hunley。*)
- リモートの暗号化リポジトリに対する`annotate`コマンドを修正しました。 (*修正：Douglas J Hunley。レビュー：David Steele。*)

**新機能：**

- PostgreSQL 19beta4をサポートしました。



### v2.59.1リリースノート {#v2591-release-notes}

*PostgreSQL 19beta3のサポート*

*2026年8月17日リリース*

**バグ修正：**

- チャンクバッファーが入力バッファーより小さい場合、ハングする問題を修正しました。 (*レビュー：Andrew Pogrebnoi, Douglas J Hunley。報告：crajac66。*)
- 新しいバックアップラベルの比較対象を、そのラベルが属するフルバックアップセットのみに限定しました。 (*レビュー：Douglas J Hunley。報告：Anton Glushakov。*)
- GitHubが生成するソースアーカイブに、ビルドに必要なファイルが含まれない問題を修正しました。 (*報告：aardvarkzed。*)

**新機能：**

- PostgreSQL 19beta3をサポートしました。 (*貢献：Lardière Sébastien。レビュー：David Steele。*)

**ドキュメントの改善：**

- `repo-s3-uri-style=path`の場合の、S3バケット名に含まれるドットの例外を説明しました。
- ユーザーガイドから`hot_standby`の明示的な設定を削除しました。


### v2.59.0リリースノート {#v2590-release-notes}

*PostgreSQL 19beta2のサポート*

*2026年7月20日リリース*

**パッケージ作成者への注意事項**：生成済みのHTMLドキュメント、manページ、コードを提供し、ビルド手順を簡単にする新しい配布用tarアーカイブを用意しました。各リリースに`pgbackrest-{version}.tar.gz`という名前のアセットとして添付されます。詳細はtarアーカイブ内の`README.md`を参照してください。今後のリリースでコード生成に必要となる追加のビルドツールを導入せずに済むよう、新しい配布用tarアーカイブを使用してください。詳しくは[新しい配布用tarアーカイブ](/ja/pgbackrest/news/#distribution-tarball)を参照してください。**パッケージ作成者への注意事項**：新たに`libsystemd`への任意の依存関係が追加されました。**重要な注意事項**：このリリースから、デフォルトでrootとして実行できるのは`restore`コマンドのみです。他のコマンドをrootとして実行するには`allow-root`を使用してください（ただし推奨されません）。

**バグ修正：**

- `expire`が別のホストで実行中のバックアップを削除する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Dmitrii。*)
- WALファイルでエラーが発生した場合、`archive-push-queue-max`が適用されない問題を修正しました。 (*レビュー：Stefan Fercot。報告：vut12。*)
- タイムラインの切り替えをまたぐリカバリー中に、非同期`archive-get`が失敗する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Jimmy Yih。*)
- エラーモジュールでバッファーオーバーランが起こり得る問題を修正しました。 (*修正：Christophe Pettus。レビュー：David Steele。*)
- 並列プロトコルクライアントでの解放済みメモリーの使用を修正しました。 (*レビュー：Douglas J Hunley。報告：Georgy Shelkovy。*)
- pg1を設定せずにpgオプションを設定すると、ヒープオーバーフローが発生する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Naveen。*)

**新機能：**

- PostgreSQL 19beta2をサポートしました。 (*レビュー：Stefan Fercot。*)
- WALアーカイブを整理する`archive-expire-before`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- Azureストレージの一括削除を追加しました。 (*レビュー：Douglas J Hunley, Crispy。*)
- S3 Outpostsのサポートを追加しました。 (*貢献：Shiva Kumar Ambigi。レビュー：David Steele, Roberto Mello。*)
- S3のプロセス認証を追加しました。 (*レビュー：Andrew Charlton。提案：Andrew Charlton。*)

**改善：**

- サーバーがアイドル接続を切断した後、SFTPストレージに再接続するようにしました。 (*レビュー：Stefan Fercot。提案：mustafa0x, tisserat。*)
- マニフェストの作成を高速化するユーザー／グループキャッシュを追加しました。 (*貢献：Gunnar Lindholm。レビュー：David Steele。*)
- `info`コマンドの出力に、リポジトリごとのバックアップ進捗を追加しました。 (*貢献：Will Morland。レビュー：David Steele, Stefan Fercot。*)
- `verify`コマンドに`backup.info`のチェックを追加しました。 (*貢献：Denis Garsh。レビュー：David Steele, Douglas J Hunley。*)
- S3 STSエンドポイントを設定できるようにしました。 (*貢献：Simon Gratton。レビュー：David Steele。*)
- 非同期処理1回あたりに送信するWALを制限する`archive-push-batch-size`を追加しました。 (*レビュー：Stefan Fercot。*)
- 最初のエラーで非同期`archive-push`を終了するようにしました。 (*レビュー：Stefan Fercot。提案：Lardière Sébastien。*)
- HTTPチャンクレスポンスの解析を堅牢にしました。 (*貢献：Shubham。レビュー：David Steele。*)
- `allow-root`が有効でない限り、rootとして実行するとエラーになるようにしました。 (*レビュー：Douglas J Hunley。*)
- マニフェスト作成時の二分探索の回数を減らしました。 (*貢献：Gunnar Lindholm。レビュー：David Steele。*)
- ブロック増分バックアップの差分リストアにおけるシーク性能を改善しました。 (*レビュー：David Christensen, Douglas J Hunley。*)
- より収まりのよいファイルを探すのではなく、順番にバックアップファイルをバンドルするようにしました。 (*レビュー：Stefan Fercot。*)
- クエリーが完了しない場合、原因となったエラーを報告するようにしました。 (*レビュー：Andrew Pogrebnoi。提案：Marco Fontana。*)
- S3認証情報の取得リクエストが失敗した場合、実際のエラーを報告するようにしました。 (*レビュー：Douglas J Hunley。提案：Mitchell Grice。*)
- `archive-push`のスプールパスのエラーを、PostgreSQLのログに報告するようにしました。 (*レビュー：Douglas J Hunley。提案：Don Seiler。*)
- バージョンが未サポートの場合、pgBackRestが古い可能性を示すヒントを追加しました。
- systemd notifyとの連携を追加しました。 (*貢献：Andrew Jackson。レビュー：David Steele。*)
- mesonによるコンパイラーの機能検査で、`unused parameter`エラーを抑制しました。 (*貢献：Jörg Plate。レビュー：David Steele。*)
- Cの最低要件をC11にしました。 (*レビュー：Mohammad Ali Nazir Kosar。*)

**ドキュメントの改善：**

- `repo-*`コマンドの`stanza`オプションを内部用としました。 (*レビュー：Stefan Fercot。*)
- infoがglobalセクションから暗号化設定を読み込むことを説明しました。 (*レビュー：Stefan Fercot。提案：Ron Johnson。*)
- `expire-auto`が`backup`コマンドの設定を使うことを説明しました。 (*レビュー：Stefan Fercot。提案：Lardière Sébastien。*)
- 専用ユーザーを使う場合の、logrotateの`su`ディレクティブの調整を説明しました。 (*レビュー：Douglas J Hunley。提案：lkanbus。*)
- 設定ファイルでは行末コメントをサポートしないことを説明しました。 (*レビュー：Douglas J Hunley。提案：Alex Richman。*)

**テストスイートの改善：**

- CIコンテナ内のAlpineのグループ競合を修正しました。 (*貢献：Artur Zakirov。レビュー：David Steele。*)


### v2.58.0リリースノート {#v2580-release-notes}

*オブジェクトストレージの改善*

*2026年1月19日リリース*

**重要な注意事項**：`repo-storage-upload-chunk-size`オプションの最小値を引き上げました。新しい最小値は、各ベンダーが許可する最小値に対応しています。

**バグ修正：**

- シグナルハンドラー内のログ出力によるデッドロックを修正しました。 (*修正：Maxim Michkov。レビュー：David Steele。*)

**新機能：**

- S3、GCS、AzureでHTTPをサポートしました。 (*貢献：Will Morland。レビュー：David Steele。*)
- 現在の保持設定にかかわらず、最も古いフルバックアップを期限切れにできるようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Ron Johnson。*)
- AzureのマネージドIDをサポートしました。 (*貢献：Moiz Ibrar, Matthew Mols。レビュー：David Steele。*)
- S3 EKS Pod Identityを***試験的に***サポートしました。 (*貢献：Pierre BOUTELOUP。レビュー：David Steele。*)
- TLS暗号スイートを設定できるようにしました。 (*貢献：Gunnar "Nick" Bluth。レビュー：David Steele。*)
- プロセスの優先度を設定できるようにしました。 (*レビュー：Douglas J Hunley。*)

**改善：**

- パス形式のURIを使う場合、S3バケット名にドットを使用できるようにしました。 (*貢献：Joakim Hindersson。レビュー：David Steele。*)
- 検証が無効な場合を除き、TLS >= 1.2を必須にしました。 (*レビュー：Douglas J Hunley, Gunnar "Nick" Bluth。*)
- 大容量のアップロードでは、S3/GCS/Azureのチャンクサイズを動的に設定するようにしました。 (*レビュー：Douglas J Hunley。提案：Timothée Peignier。*)
- 小さなファイルに対して、S3/GCS/Azureのチャンクサイズを最適化しました。 (*レビュー：Douglas J Hunley。*)
- PostgreSQL `9.5`のサポートを削除しました。 (*レビュー：Douglas J Hunley。*)
- 依存関係が未解決のオプションについて、デフォルト値のログ出力を改善しました。 (*レビュー：Stefan Fercot。*)

**ドキュメントの改善：**

- ユーザーガイドから`max_wal_senders`／`wal_level`の明示的な設定を削除しました。 (*提案：Jamie Nguyen。*)
- ブロックサイズの大きなファイルシステムではバンドルが有用であることを明確にしました。 (*提案：Ron Johnson。*)


### v2.57.0リリースノート {#v2570-release-notes}

*リポジトリのシンボリックリンクを抑制*

*2025年10月18日リリース*

**バグ修正：**

- HTTP／TLS／ソケットのタイムアウトの入れ子を解消しました。 (*レビュー：David Christensen。*)
- ページチェックサムのエラーメッセージで、セグメンテーション違反が起こり得る問題を修正しました。 (*修正：Zsolt Parragi。レビュー：David Steele。*)

**新機能：**

- リポジトリのシンボリックリンクの作成を抑制する`repo-symlink`オプションを追加しました。 (*レビュー：Douglas J Hunley。提案：Ron Johnson。*)

**改善：**

- HTTPの408および429エラーに対する再試行を追加しました。 (*レビュー：David Christensen。*)


### v2.56.0リリースノート {#v2560-release-notes}

*進捗情報の改善*

*2025年7月21日リリース*

**バグ修正：**

- リポジトリにバックアップがない場合の、個別の期限切れ処理の問題を修正しました。 (*レビュー：Stefan Fercot。報告：Anup Gupta。*)

**新機能：**

- `info`コマンドの出力にリストアの進捗を追加しました。 (*貢献：Denis Garsh, Maxim Michkov。レビュー：David Steele。*)
- `info`コマンドの出力に、進捗のみを表示する詳細レベルを追加しました。 (*貢献：Denis Garsh。レビュー：David Steele, Stefan Fercot。*)

**改善：**

- オブジェクトストアで失敗した読み取りを再試行するようにしました。 (*レビュー：David Christensen。*)
- コマンドラインヘルプのデフォルト値を修正しました。 (*レビュー：David Christensen, Chris Bandy。*)

**ドキュメントの改善：**

- 適切な場合には、オプションの個々の値を一覧で説明するようにしました。 (*貢献：Anton Kurochkin。レビュー：David Steele。*)
- `archive-mode`オプションのヘルプ出力にある"less than"の記述を修正しました。 (*貢献：Anton Kurochkin。レビュー：David Steele。*)


### v2.55.1リリースノート {#v2551-release-notes}

*不具合修正*

*2025年5月5日リリース*

**バグ修正：**

- 「必要な場合のみS3でcontent-md5を計算する」変更を元に戻しました。 (*レビュー：David Christensen。報告：Frank Brendel。*)
- オプションキーの下限チェックを修正しました。 (*レビュー：David Christensen, Wolfgang Walther。報告：Wolfgang Walther。*)


### v2.55.0リリースノート {#v2550-release-notes}

*検証の改善とPostgreSQL 18のサポート*

*2025年4月21日リリース*

**バグ修正：**

- デフォルト以外のリポジトリでのブロック増分リストアの問題を修正しました。 (*レビュー：David Christensen, Aleksander Łukasz。報告：Aleksander Łukasz。*)
- PostgreSQL < 12では`recovery_target_timeline=current`を設定しないようにしました。 (*レビュー：Stefan Fercot。*)
- アーカイブの期限切れ範囲のログ出力を修正しました。 (*レビュー：Stefan Fercot。報告：Aleš Zelený。*)
- 結果がないクエリーでのエラー報告を修正しました。 (*レビュー：Stefan Fercot。報告：Susantha Bathige。*)

**新機能：**

- リカバリー対象のタイムラインを検証するようにしました。 (*レビュー：Stefan Fercot。*)
- 指定したバックアップを検証できるようにしました。 (*貢献：Maxim Michkov。レビュー：David Steele。*)
- S3/GCSのリクエスター支払いをサポートしました。 (*貢献：Timothée Peignier。レビュー：David Steele。*)
- PostgreSQL 18をサポートしました。 (*レビュー：Stefan Fercot。*)
- 抽象ドメインソケットでPostgreSQLに接続できるようにしました。 (*レビュー：Chris Bandy。提案：Chris Bandy。*)
- `version`コマンドに数値形式の出力を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

**改善：**

- backupコマンドをリモートリポジトリに対して実行できるようにしました。 (*レビュー：Stefan Fercot。*)
- プロトコルの圧縮にlz4を使用するようにしました。 (*レビュー：Stefan Fercot。*)
- 必要な場合のみS3で`content-md5`を計算するようにしました。 (*レビュー：David Christensen。*)
- 複数キーを持つオプションの値が上書きされた場合、警告するようにしました。 (*レビュー：David Christensen, Stefan Fercot。*)
- 期限切れにしたアーカイブパスをdetailログに出力するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- PostgreSQL `9.4`のサポートを削除しました。 (*レビュー：Stefan Fercot。*)
- autoconf/makeによるビルドを削除しました。 (*レビュー：David Christensen。*)

**ドキュメントの改善：**

- `tls-server-auth`で複数のstanzaを指定するための説明を修正しました。 (*レビュー：David Christensen, Stefan Fercot。提案：Terry MacAndrew。*)
- 増分バックアップの期限切れ処理を明確にしました。 (*レビュー：Stefan Fercot。*)
- ローカルとリモートのpgBackRestのバージョンが一致する必要があることを明確にしました。 (*貢献：Greg Clough。レビュー：David Steele。*)
- 単独で動作するクラスターのエクスポートに関するFAQを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- テーブルスペース作成に関する`--tablespace-map-all`の注意事項を追加しました。 (*レビュー：Stefan Fercot, Christophe Courtois。提案：Christophe Courtois。*)
- `--repo-retention-full-type`の動作を明確にしました。 (*レビュー：Antoine Beaupré。提案：Antoine Beaupré。*)
- オブジェクトストアに対する推奨設定を、`--process-max`から`--repo-bundle`に変更しました。 (*レビュー：Stefan Fercot。*)
- `unix_socket_directory`を`unix_socket_directories`に更新しました。 (*貢献：hyunkyu han。レビュー：David Steele。*)
- `spool-path`を`pg_xlog`／`pg_wal`の中に置かないことを推奨する記述を追加しました。 (*レビュー：Martín Marqués, Don Seiler。提案：Martín Marqués。*)


### v2.54.2リリースノート {#v2542-release-notes}

*不具合修正*

*2025年1月20日リリース*

**バグ修正：**

- ブロック増分が有効な状態でバンドルを無効にした後の問題を修正しました。 (*レビュー：David Christensen。*)

**ドキュメントの改善：**

- 複数の設定ファイルを使う場合の動作を明確にしました。 (*レビュー：Paul Bierly。提案：Paul Bierly。*)


### v2.54.1リリースノート {#v2541-release-notes}

*不具合修正*

*2024年12月16日リリース*

**バグ修正：**

- `version`／`help`コマンドが`pgbackrest.conf`を読み込もうとする問題を修正しました。 (*レビュー：Stefan Fercot。報告：Bradford Boyle, Julian。*)

**テストスイートの改善：**

- 統合テストでの非同期アーカイブを安定化しました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)


### v2.54.0リリースノート {#v2540-release-notes}

*バージョン管理されたストレージの対象時刻*

*2024年10月21日リリース*

**パッケージ作成者への注意事項**：autoconf/makeによるビルドをサポートする機能リリースは、これが最後です。まだ移行していない場合はmesonへ移行してください。2.54.Xのパッチリリースがある場合、そちらでは引き続きautoconf/makeをサポートします。

**バグ修正：**

- 大規模なデータセットでのPostgreSQLクエリーの性能を修正しました。 (*修正：Thibault Vincent, David Steele。レビュー：David Christensen, Antoine Millet。報告：Antoine Millet。*)

**新機能：**

- バージョン管理されたストレージ上のリポジトリを、指定時刻の状態で読み取れるようにしました。 (*レビュー：Stefan Fercot, David Christensen。*)
- スタンバイからのバックアップが要求された場合、スタンバイがなくても続行できるようにしました。 (*レビュー：Stefan Fercot。*)

**改善：**

- `info`コマンドのテキスト出力で、バックアップの参照一覧を要約するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- S3認証のたびにweb-idトークンを更新するようにしました。 (*貢献：Brent Graveland。レビュー：David Steele。*)
- ヘルプでインデックス付きオプションの現在値を正しく表示するようにしました。 (*レビュー：David Christensen。*)
- 内容が変更された場合のみ`backup.info`を保存するようにしました。 (*レビュー：Stefan Fercot。*)
- リストア時にファイルを並列で読み取る際の制限を削除しました。 (*レビュー：David Christensen。*)
- SFTPのエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

**ドキュメントの機能：**

- ユーザーガイドに性能調整のセクションを追加しました。 (*レビュー：Stefan Fercot。*)

**ドキュメントの改善：**

- `data_directory`の取得元を明確にしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Matthias。*)
- 概要を小文字にするかどうかの判定ロジックを改善しました。 (*提案：Daniel Westermann。*)


### v2.53.1リリースノート {#v2531-release-notes}

*PostgreSQL 17のサポート*

*2024年8月19日リリース*

**バグ修正：**

- rootユーザーで`restore`を実行した場合のアクセス権限を修正しました。 (*レビュー：Stefan Fercot。報告：Will M。*)
- 接続エラーが遅れて発生した場合のセグメンテーション違反を修正しました。 (*レビュー：David Christensen。報告：Anton Glushakov。*)
- SFTPではローカルリポジトリの重複チェックを省略するようにしました。 (*修正：Reid Thompson。レビュー：David Steele。報告：Anton Kurochkin。*)

**改善：**

- PostgreSQL 17をサポートしました。


### v2.53リリースノート {#v253-release-notes}

*バックアップの同時実行*

*2024年7月22日リリース*

**重要な注意事項**：`log-level-stderr`オプションのデフォルトを`warn`から`off`に変更しました。これにより、`stdout`だけをリダイレクトする場合にも、エラーを収集しやすくなります。以前の動作を維持するには`log-level-stderr=warn`を設定してください。**パッケージ作成者への注意事項**：mesonでのビルドにlz4ライブラリが必須になりました。**パッケージ作成者への注意事項**：mesonでのビルドに、コンパイラーの`__builtin_clzl()`および`__builtin_bswap64()`のサポートが必須になりました。

**バグ修正：**

- ファイルがすでに存在する場合、SFTPで名前の変更に失敗する問題を修正しました。 (*修正：Reid Thompson。レビュー：David Steele。報告：ahmed112212。*)

**新機能：**

- 異なるリポジトリに対してバックアップを同時に実行できるようにしました。 (*レビュー：Reid Thompson, Stefan Fercot。*)
- TLS証明書の検証で、IPアドレスを使うSANをサポートしました。 (*貢献：David Christensen。レビュー：David Steele。*)

**改善：**

- `log-level-stderr`オプションのデフォルトを`off`にしました。 (*レビュー：Greg Sabino Mullane, Stefan Fercot。*)
- PostgreSQL ≤ 10で、標準以外のWALセグメントサイズを使用できるようにしました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)
- SFTP認証ログの確認を促すヒントを追加しました。 (*貢献：Vitalii Zurian。レビュー：Reid Thompson, David Steele。*)

**ドキュメントの改善：**

- 複数リポジトリでの`archive-push`の動作を明確にしました。 (*レビュー：Stefan Fercot。*)


### v2.52.1リリースノート {#v2521-release-notes}

*不具合修正*

*2024年6月25日リリース*

**バグ修正：**

- レプリカ上のファイルがプライマリー上より大きい場合の問題を修正しました。 (*レビュー：Stefan Fercot。報告：Nicolas Lassimonne。*)


### v2.52リリースノート {#v252-release-notes}

*PostgreSQL 17beta1のサポート*

*2024年5月27日リリース*

**パッケージ作成者への注意事項**：pgBackRestのビルドシステムをmesonに変更しました。autoconf/makeによるビルドには今後新機能を追加せず、数回のリリース後に削除します。

**新機能：**

- GCSの一括削除をサポートしました。 (*レビュー：Reid Thompson。*)
- S3の`SSE-C`暗号化をサポートしました。 (*レビュー：Tim Jones。提案：Tim Jones。*)
- PostgreSQL 17beta1をサポートしました。 (*レビュー：Stefan Fercot。*)

**改善：**

- mesonでのビルドで、任意の依存関係を明示的に無効にできるようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)
- mesonでのビルドでpythonを動的に検索するようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)
- mesonで`pgbackrest`ビルドターゲットをインストール可能として指定しました。 (*貢献：Bradford Boyle。レビュー：David Steele。*)

**ドキュメントの改善：**

- 実際の機能に合わせて`start`／`stop`の説明を更新しました。 (*レビュー：Stefan Fercot。*)


### v2.51リリースノート {#v251-release-notes}

*Mesonビルドシステム*

*2024年3月25日リリース*

**バグ修正：**

- ブロック増分バックアップの差分リストアで、長さゼロのファイルをスキップするようにしました。 (*レビュー：Sebastian Krause, René Højbjerg Larsen。報告：Sebastian Krause。*)
- ストレージの一覧取得での性能リグレッションを修正しました。 (*レビュー：Stephen Frost。報告：Maksym Boguk。*)
- バックアップ中にファイルサイズが変わった場合の進捗ログを修正しました。 (*レビュー：Stephen Frost。報告：samkingno。*)

**改善：**

- デュアルスタック接続のサポートを改善しました。 (*レビュー：Stephen Frost。提案：Timothée Peignier。*)
- mesonを主なビルドシステムにしました。 (*レビュー：Stephen Frost。*)
- 差分照合を行わない増分バックアップで、変更されていないファイルを検出するようにしました。 (*レビュー：Stephen Frost。*)
- `backup_label`を削除した場合に、無効なリカバリーが行われることを防ぎました。 (*レビュー：Stephen Frost。*)
- `archive-push`のWALセグメントキューの処理を改善しました。 (*レビュー：Stephen Frost。*)
- 再開機能をフルバックアップのみに制限しました。 (*レビュー：Stephen Frost, Stefan Fercot。*)
- ブロック増分バックアップの再開機能を更新しました。 (*レビュー：Stephen Frost。*)
- バージョンとヘルプの表示に、`--version`と`--help`を使用できるようにしました。 (*レビュー：Greg Sabino Mullane。提案：Greg Sabino Mullane。*)
- autoconf/makeによるビルドに、詳細なバックトレースを追加しました。 (*レビュー：Stephen Frost。*)

**ドキュメントの改善：**

- `recovery.conf`への言及を更新しました。 (*レビュー：Stefan Fercot。提案：Stephen Frost。*)


### v2.50リリースノート {#v250-release-notes}

*性能改善と不具合修正*

*2024年1月22日リリース*

**バグ修正：**

- ブロック増分リストアで、読み取り結果が要求した長さに満たない場合の問題を修正しました。 (*レビュー：Stephen Frost, Brent Graveland。報告：Adol Rodriguez, Brent Graveland。*)
- オーバーフローによって`info`出力のバックアップ進捗が表示されなくなる問題を修正しました。 (*修正：Robert Donovan。レビュー：Joe Wildish。*)

**改善：**

- ブロック増分バックアップの差分リストアで、部分的なファイルを保持するようにしました。 (*レビュー：Stephen Frost。*)
- コンパイル時の標準以外のページサイズをサポートしました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)
- バンドル時に、バックアップ中に切り詰められたファイルをスキップするようにしました。 (*貢献：Georgy Shelkovy。レビュー：David Steele。*)
- SFTPストレージのエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)


### v2.49リリースノート {#v249-release-notes}

*PostgreSQL 9.3のサポート終了*

*2023年11月27日リリース*

**バグ修正：**

- 再試行のリグレッションを修正しました。 (*レビュー：Stephen Frost。報告：Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier。*)
- SFTPストレージドライバーでの再帰的なパス削除を修正しました。 (*修正：Reid Thompson。レビュー：Stephen Frost。報告：Luc。*)

**改善：**

- PostgreSQL `9.3`のサポートを削除しました。 (*レビュー：Stephen Frost。*)

**ドキュメントの機能：**

- メンテナー向けオプションを説明しました。 (*レビュー：Stefan Fercot。*)
- PostgreSQL >= 13向けにポイントインタイムリカバリーの説明を更新しました。

**テストスイートの改善：**

- `libssh2`がインストールされていなくても、`config/load`単体テストを実行できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Wu Ning。*)


### v2.48リリースノート {#v248-release-notes}

*リポジトリストレージのタグ*

*2023年9月25日リリース*

**バグ修正：**

- ブロックリストなしでブロック増分バックアップをリストアする際の問題を修正しました。 (*レビュー：Stephen Frost, Burak Yurdakul。報告：Burak Yurdakul。*)

**新機能：**

- オブジェクトタグを作成する`--repo-storage-tag`オプションを追加しました。 (*レビュー：Stephen Frost, Stefan Fercot, Timothée Peignier。*)
- SFTPストレージドライバーに既知のホストのチェックを追加しました。 (*貢献：Reid Thompson。レビュー：Stephen Frost, David Steele。*)
- デュアルスタック接続をサポートしました。 (*レビュー：Stephen Frost。*)
- `info`コマンドのJSON出力に、バックアップサイズの完了分と合計を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

**改善：**

- 複数のstanzaを対象とするcheckコマンドを追加しました。 (*レビュー：Stephen Frost。*)
- チェックサムが有効になるまで、`pg_control`の読み取りを再試行するようにしました。 (*レビュー：Stefan Fercot, Stephen Frost。*)
- バックアップが成功した後のWALセグメントのチェックを最適化しました。 (*レビュー：Stephen Frost。*)
- GCSのマルチパート処理の性能を改善しました。 (*レビュー：Reid Thompson。*)
- stanzaが停止していても`archive-get`コマンドを実行できるようにしました。 (*レビュー：Tom Swartz, David Christensen, Reid Thompson。*)
- SFTP公開鍵／秘密鍵のパスの先頭に、チルダを使用できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- 認証トークンの更新前に、GCSの認証情報を再読み込みするようにしました。 (*レビュー：Stephen Frost。提案：Daniel Farina。*)

**ドキュメントの不具合修正：**

- 設定リファレンスの`tls-server-address`オプションの例を修正しました。 (*修正：Hartmut Goebel。レビュー：David Steele。*)
- コマンドリファレンスの`filter`オプションの例を修正しました。

**テストスイートの改善：**

- `libssh2`がインストールされていなくても、`storage/sftp`単体テストを実行できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Wu Ning。*)


### v2.47リリースノート {#v247-release-notes}

*性能改善と不具合修正*

*2023年7月24日リリース*

**バグ修正：**

- 差分照合を行うバックアップ中に、マニフェストのブロック増分情報を保持するようにしました。 (*レビュー：Stephen Frost。報告：Francisco Miguel Biete Banon。*)
- `verify`コマンドでのブロック増分ファイル名を修正しました。 (*レビュー：Reid Thompson。報告：Francisco Miguel Biete Banon。*)
- スタンバイからのバックアップで、差分照合を行うバックアップへ自動的に誤って切り替わる問題を修正しました。 (*レビュー：Stephen Frost。報告：krmozejko, Don Seiler。*)
- PostgreSQL >= 12でリカバリーの`type=none`を指定した場合、`recovery.signal`を作成しないようにしました。 (*レビュー：Stefan Fercot。報告：T.Anastacio。*)
- diff/incrバックアップの一意なラベルの生成を修正しました。 (*修正：Andrey Sokolov。レビュー：David Steele。*)
- 期限切れになるバックアップがない場合の、時間に基づくアーカイブの期限切れ処理を修正しました。 (*レビュー：Stefan Fercot。*)

**改善：**

- SFTPストレージドライバーの性能を改善しました。 (*貢献：Stephen Frost, Reid Thompson。レビュー：David Steele。*)
- `info`コマンドの日付／時刻出力にタイムゾーンオフセットを追加しました。 (*レビュー：Stefan Fercot, Philip Hurst。提案：Philip Hurst。*)
- サポートされていない機能のエラー処理を集約しました。 (*レビュー：Stefan Fercot。*)

**ドキュメントの改善：**

- ユーザーガイドで、パッケージからのインストールを優先することを明確にしました。 (*レビュー：Stefan Fercot。提案：dr-kd。*)


### v2.46リリースノート {#v246-release-notes}

*ブロック増分バックアップとSFTPストレージ*

*2023年5月22日リリース*

**新機能：**

- ブロック増分バックアップを追加しました。 (*レビュー：John Morris, Stephen Frost, Stefan Fercot。*)
- リポジトリストレージでSFTPをサポートしました。 (*貢献：Reid Thompson。レビュー：Stephen Frost, David Steele。*)
- PostgreSQL 16をサポートしました。 (*レビュー：Stefan Fercot。*)

**改善：**

- ページヘッダーのチェックを省略できるようにしました。 (*レビュー：David Christensen。提案：David Christensen。*)
- リストア中にリカバリーファイルを`chown()`しないようにしました。 (*レビュー：Stefan Fercot, Marcelo Henrique Neppel。提案：Marcelo Henrique Neppel。*)
- HTTPの再試行で、エラーの再試行に関する詳細を追加しました。

**ドキュメントの改善：**

- リカバリーで`type=none`を使う場合の警告を追加しました。 (*レビュー：Stefan Fercot。*)
- 作成済みのリポジトリに対して`stanza-create`を実行する場合の注意事項を追加しました。


### v2.45リリースノート {#v245-release-notes}

*ブロック増分バックアップ（ベータ版）*

*2023年3月20日リリース*

**バグ修正：**

- オフラインバックアップのリストアでは、デフォルトで`recovery.signal`を書き込まないようにしました。 (*レビュー：Stefan Fercot。報告：Marcel Borger。*)

**新機能：**

- ブロック増分バックアップ（ベータ版）を追加しました。 (*レビュー：John Morris, Stephen Frost, Stefan Fercot。*)

**改善：**

- すべてデフォルト値のグループインデックスは、1つだけ保持するようにしました。 (*レビュー：Stefan Fercot。*)

**ドキュメントの改善：**

- `2.x`バージョン間のアップグレードについて、明示的な手順を追加しました。 (*貢献：Christophe Courtois。レビュー：David Steele。*)
- TLSの導入により不要になったSSHへの言及を削除しました。


### v2.44リリースノート {#v244-release-notes}

*PostgreSQL 9.0/9.1/9.2のサポート終了*

*2023年1月30日リリース*

**改善：**

- PostgreSQL `9.0`/`9.1`/`9.2`のサポートを終了しました。 (*レビュー：Stefan Fercot。*)
- 現在のPostgreSQLバージョンに一致するバックアップがない場合、リストアでエラーを返すようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Soulou。*)
- `compress-type`ごとに`compress-level`の範囲チェックを追加しました。 (*レビュー：Stefan Fercot。提案：gkleen, ViperRu。*)

**ドキュメントの改善：**

- Azureストレージで「階層型名前空間」を有効にする際の警告を追加しました。 (*レビュー：Stefan Fercot。提案：Vojtech Galda, Pluggi, asjonos。*)
- 監視の例に改行を置換する処理を追加しました。 (*レビュー：Stefan Fercot。提案：rudonx, gmustdie, Ivan Shelestov。*)
- PostgreSQLの各バージョンにおける`target-action`の動作を明確にしました。 (*貢献：Chris Bandy。レビュー：David Steele, Anton Kurochkin, Stefan Fercot。提案：Anton Kurochkin, Chris Bandy。*)
- トップページを更新し、説明を明確にしました。 (*レビュー：Stefan Fercot。*)
- ウェブサイトにダークモードを追加しました。 (*提案：Stephen Frost。*)


### v2.43リリースノート {#v243-release-notes}

*不具合修正*

*2022年11月28日リリース*

**バグ修正：**

- 差分／増分バックアップで参照が欠落する問題を修正しました。 (*レビュー：Stefan Fercot。報告：Marcel Borger, ulfedf, jaymefSO。*)

**改善：**

- インデックスを付けずにオプションを指定した場合のヒントを追加しました。 (*レビュー：Stefan Fercot。*)


### v2.42リリースノート {#v242-release-notes}

*不具合修正*

*2022年11月22日リリース*

**バグ修正：**

- ファイルをバンドルする`backup`／`restore`のメモリリークを修正しました。 (*レビュー：John Morris, Oscar。報告：Oscar。*)
- リモートファイルの読み取り量が要求量に満たない場合のプロトコルエラーを修正しました。 (*レビュー：Stephen Frost。*)

**改善：**

- バンドル時に長さゼロのファイルの参照を保存しないようにしました。 (*レビュー：Stefan Fercot。*)
- `pg_start_backup()`／`pg_stop_backup()`の説明をより一般的な表現にしました。 (*レビュー：Greg Sabino Mullane, David Christensen。提案：Greg Sabino Mullane。*)

**テストスイートの改善：**

- `test.pl`の`--psql-bin`オプションをコマンドラインヘルプに合わせて更新しました。 (*貢献：Koshi Shibagaki。レビュー：David Steele。*)


### v2.41リリースノート {#v241-release-notes}

*バックアップの注釈*

*2022年9月19日リリース*

**バグ修正：**

- デフォルト以外のリポジトリで、時刻に基づく期限切れ処理が誤って適用される問題を修正しました。 (*レビュー：Stefan Fercot。報告：Adam Brusselback。*)
- フィルターを指定してディレクトリを再帰的に一覧表示する際の問題を修正しました。 (*レビュー：Stephen Frost。報告：Efremov Egor。*)

**新機能：**

- バックアップにキーと値の組による注釈を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Adam Berlin。*)

**改善：**

- `info`コマンドのJSON出力で`--set`に対応しました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Anton Kurochkin。*)
- オブジェクトストアのアップロードチャンクサイズを設定できるようにしました。 (*レビュー：Stefan Fercot。提案：Anton Glushakov。*)
- バックアップの成功後にarchive.infoのタイムスタンプを更新するようにしました。 (*レビュー：Stefan Fercot。提案：Alex Richman。*)
- スタンバイのタイムラインのチェックをチェックポイントの後に移動しました。 (*レビュー：Stefan Fercot, Keith Fiske。提案：Keith Fiske。*)
- バックアップ再開時の警告メッセージを改善しました。 (*提案：Cynthia Shang。*)

**ドキュメントの改善：**

- `pgbackrest.service`内の`kill`に絶対パスを追加しました。 (*提案：Don Seiler。*)


### v2.40リリースノート {#v240-release-notes}

*OpenSSL 3のサポート*

*2022年7月18日リリース*

**パッケージ作成者への注意事項**：実験的なmesonビルドを追加しましたが、当面は引き続きautoconf/makeでビルドすることを推奨します。

**改善：**

- OpenSSL 3に対応しました。 (*レビュー：Stephen Frost。*)
- パスの内容を一覧表示する際にスナップショットを作成するようにしました。 (*レビュー：John Morris, Stephen Frost。*)
- リストアで`type=immediate`を指定した場合に、`target-timeline=current`を強制するようにしました。 (*レビュー：Stephen Frost。*)
- 差分`restore`で、ファイルが想定より大きい場合に切り詰めるようにしました。 (*レビュー：Stephen Frost。*)
- `resume=n`の場合、マニフェストの増分保存を無効にしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- コピー開始前にバックアップの進捗率をゼロに設定するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- 一覧取得を続けるかどうかの判定にS3の`IsTruncated`フラグを使用するようにしました。 (*レビュー：John Morris, Soulou。提案：Christian Montagne。*)

**ドキュメントの不具合修正：**

- 設定リファレンスに内部オプションを掲載しないようにしました。 (*報告：Francisco Miguel Biete Banon。*)

**ドキュメントの改善：**

- リポジトリホストのセクションにPostgreSQLの設定へのリンクを追加しました。 (*レビュー：Stefan Fercot。提案：Julien Cigar。*)

**テストスイートの改善：**

- 実験的なMesonビルドを追加しました。 (*レビュー：Eli Schwartz, Sam Bassaly。*)
- `--test-path`オプションに任意のパスを渡せるようにしました。 (*貢献：Andrey Sokolov。レビュー：David Steele。*)
- `DEBUG`を定義せずに`DEBUG_EXEC_TIME`を定義した場合のコンパイルエラーを修正しました。 (*貢献：Andrey Sokolov。レビュー：David Steele。*)


### v2.39リリースノート {#v239-release-notes}

*検証とファイルのバンドル化*

*2022年5月16日リリース*

**バグ修正：**

- `FINALLY()`からエラーが送出されると無限ループになる問題を修正しました。 (*レビュー：Stephen Frost。*)
- 他のプロセスがロックを保持している場合を除き、ロックの取得に失敗すると必ずエラーを返すようにしました。 (*レビュー：Reid Thompson, Geir Råness。報告：Geir Råness。*)

**新機能：**

- 小さなファイルを効率的に扱えるよう、バックアップファイルのバンドル化を追加しました。 (*レビュー：Reid Thompson, Stefan Fercot, Chris Bandy。*)
- リポジトリの内容を検証するverifyコマンドを追加しました。 (*貢献：Cynthia Shang, Reid Thompson。レビュー：David Steele, Stefan Fercot。*)
- PostgreSQL 15に対応しました。 (*レビュー：Stefan Fercot。*)
- `info`の出力にバックアップの進捗率を表示するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- `restore`コマンドの`--type=lsn`でバックアップを自動選択するようにしました。 (*貢献：Reid Thompson。レビュー：Stefan Fercot, David Steele。*)
- `archive-mode-check`が無効な場合、既存のWALに関する警告を抑止するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- AWS IMDSv2のサポートを追加しました。 (*貢献：Nuno Pires。レビュー：David Steele。*)

**改善：**

- フルバックアップの後で`repo-hardlink`オプションを変更できるようにしました。 (*レビュー：Reid Thompson。*)
- `backup`と`restore`の進捗率のログの精度を上げました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- `repo-*`コマンドのパス検証を改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- `stop`コマンドが`stanza`オプションに従うように改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：ragaoua。*)
- `repo-azure-key`が無効な場合のエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Seth Daniel。*)
- 非同期の`archive-get`／`archive-push`でエラーが発生した場合に、ログを確認するよう促すヒントを追加しました。 (*レビュー：Reid Thompson。*)
- 予期しないクロックスキューやタイムゾーンの変更に対して`ClockError`を追加しました。 (*レビュー：Greg Sabino Mullane, Stefan Fercot。提案：Greg Sabino Mullane。*)
- 履歴マニフェストをエラーメッセージに表示する前に、拡張子を取り除くようにしました。 (*レビュー：Stefan Fercot。*)
- ロックの権限エラーにuser:groupを追加しました。 (*レビュー：Reid Thompson。*)

**ドキュメントの不具合修正：**

- ユーザーガイドの`stanza-update`への誤った参照を修正しました。 (*修正：Abubakar Mohammed。レビュー：David Steele。*)
- 設定リファレンスの`repo-gcs-key-type`オプションの例を修正しました。 (*レビュー：Reid Thompson。*)
- `tls-server-auth`の例を修正し、説明を補いました。 (*レビュー：Reid Thompson。*)

**ドキュメントの改善：**

- ドキュメント内のサポート対象バージョンに関する説明を簡潔にしました。 (*レビュー：Stefan Fercot, Reid Thompson, Greg Sabino Mullane。*)
- オプションの型の説明を追加しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- バックアップの種類とリストア速度に関するFAQを追加しました。 (*貢献：David Christensen。レビュー：Reid Thompson。*)
- プルリクエストで必須となるベースブランチを明記しました。 (*貢献：David Christensen。レビュー：Reid Thompson。*)


### v2.38リリースノート {#v238-release-notes}

*軽微なバグ修正と改善*

*2022年3月6日リリース*

**重要な注意事項**：`info`コマンドが報告するリポジトリサイズは、pgBackRestがストレージに書き込んだ量だけに基づくようになりました。以前は、ストレージで追加の圧縮が行われているかどうかを検出できる場合がありましたが、この機能はサポートされなくなりました。

**バグ修正：**

- S3でファイルを一括削除する際のエラーで再試行するようにしました。 (*レビュー：Reid Thompson。報告：Alex Richman。*)
- HTTPの`connection`ヘッダーの値を、大文字と小文字を区別せずに照合できるようにしました。 (*レビュー：Reid Thompson。報告：Rémi Vidier。*)

**新機能：**

- KMSを使用したAWS S3のサーバー側暗号化のサポートを追加しました。 (*貢献：Christoph Berg。レビュー：David Steele, Tharindu Amila。*)
- `archive-missing-retry`オプションを追加しました。 (*レビュー：Stefan Fercot。*)
- `info`コマンドにバックアップの種類によるフィルターを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

**改善：**

- `backup`中にページ検証に失敗した場合に再試行するようにしました。 (*レビュー：Stephen Frost, David Christensen。*)
- 接続を正常に終了しないTLSサーバーに対応しました。 (*レビュー：Rémi Vidier, David Christensen, Stephen Frost。*)
- `info`コマンドの出力にバックアップのLSNを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- `repo-ls`のパスの末尾のスラッシュを自動的に取り除くようにしました。 (*貢献：David Christensen。レビュー：David Steele。*)
- 致命的なエラーでは再試行しないようにしました。 (*レビュー：Reid Thompson。*)
- PostgreSQL `8.3`／`8.4`のサポートを終了しました。 (*レビュー：Reid Thompson, Stefan Fercot。*)
- ファイルシステムによる追加の圧縮を判定するロジックを削除しました。 (*レビュー：Reid Thompson, Stefan Fercot。*)

**ドキュメントの不具合修正：**

- TLSのドキュメントで、`repo`オプションを`global`セクションに移動しました。 (*報告：Anton Kurochkin。*)
- stanzaコマンドから未使用の`backup-standby`オプションを削除しました。 (*報告：Stefan Fercot。*)
- ヘルプとリリースノートの誤記を修正しました。 (*修正：Daniel Gustafsson。レビュー：David Steele。*)

**ドキュメントの改善：**

- systemdサービスの設定に死活監視を追加しました。 (*提案：Yogesh Sharma。*)
- WALアーカイブの接尾辞について説明するFAQを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- レプリケーションスロットはリストアされないことを明記しました。 (*貢献：Reid Thompson。レビュー：David Steele, Stefan Fercot。提案：Christophe Courtois。*)


### v2.37リリースノート {#v237-release-notes}

*TLSサーバー*

*2022年1月3日リリース*

**重要な注意事項**：`restore`コマンドで、指定した目標時刻に合うバックアップが見つからない場合、従来は警告をログに記録していましたが、エラーを返すようになりました。

**バグ修正：**

- パスやファイルがすでに存在する場合の、差分`restore`でのリンクのマッピングを修正しました。 (*レビュー：Reid Thompson。報告：Younes Alhroub。*)
- 接続の再試行時にソケットがリークする問題を修正しました。 (*レビュー：Reid Thompson。報告：James Coleman。*)

**新機能：**

- TLSサーバーを追加しました。 (*レビュー：Stephen Frost, Reid Thompson, Andrew L'Ecuyer。*)
- `--cmd`オプションを追加しました。 (*貢献：Reid Thompson。レビュー：Stefan Fercot, David Steele。提案：Virgile CREVON。*)

**改善：**

- バックアップ開始直後にアーカイブをチェックするようにしました。 (*レビュー：Reid Thompson, David Christensen。*)
- バックアップにタイムラインとチェックポイントのチェックを追加しました。 (*レビュー：Stefan Fercot, Reid Thompson。*)
- バックアップ中に、クラスターが稼働しており正しく設定されていることをチェックするようにしました。 (*レビュー：Stefan Fercot。*)
- `restore`で目標時刻に合うバックアップが見つからない場合にエラーを返すようにしました。 (*レビュー：Reid Thompson, Douglas J Hunley。提案：Douglas J Hunley。*)
- S3／Azureエンドポイントのプロトコルとポートを解析するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- checkpoint_timeoutが`db-timeout`を超える場合に警告するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- HTTPエラーの出力にメソッドを追加しました。 (*貢献：Christoph Berg。レビュー：David Steele。*)
- コマンドラインのブール型オプションでy/nの引数を受け付けるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)
- ログに記録するバックアップサイズを、`info`コマンドの出力と正確に一致させました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Mahomed Hussein。*)

**ドキュメントの改善：**

- サイズを指定するオプションのデフォルト値と許容値を適切な単位で表示するようにしました。 (*レビュー：Reid Thompson。*)
- `tablespace-map-all`オプションの誤記を修正し、説明を改善しました。 (*レビュー：Reid Thompson。提案：Reid Thompson。*)
- 複数リポジトリへの将来的な対応に関する古い記述を削除しました。 (*提案：David Christensen。*)


### v2.36リリースノート {#v236-release-notes}

*軽微なバグ修正と改善*

*2021年11月1日リリース*

**バグ修正：**

- stanzaの接頭辞に「global」を使用できるようにしました。 (*レビュー：Stefan Fercot。報告：Younes Alhroub。*)
- 無効なGCSキーファイルによるセグメンテーション違反を修正しました。 (*レビュー：Stephen Frost。報告：Henrik Feldt。*)

**改善：**

- `link-map`オプションで新しいリンクを作成できるようにしました。 (*レビュー：Don Seiler, Stefan Fercot, Chris Bandy。提案：Don Seiler。*)
- `pg`／`repo`オプションに指定できるインデックスの最大値を256に増やしました。 (*レビュー：Cynthia Shang。*)
- AWS S3の`WebIdentity`認証を追加しました。 (*レビュー：James Callahan, Reid Thompson, Benjamin Blattberg, Andrew L'Ecuyer。*)
- バックアップファイルの検証エラーを`backup.info`に記録するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- オンラインバックアップのリストアログに、リカバリーの開始時刻を追加しました。 (*レビュー：Tom Swartz, Stefan Fercot。提案：Tom Swartz。*)
- ローカルジョブの失敗時に、元のエラーと再試行を報告するようにしました。 (*レビュー：Stefan Fercot。*)
- infoのテキスト出力で、ページチェックサムエラーの名称をエラー一覧に変更しました。 (*レビュー：Stefan Fercot。*)
- スタンバイでの再生タイムアウトのメッセージにヒントを追加しました。 (*レビュー：Cynthia Shang, Stefan Fercot。提案：Leigh Downs。*)


### v2.35リリースノート {#v235-release-notes}

*バイナリープロトコル*

*2021年8月23日リリース*

**重要な注意事項**：`backup`／`restore`コマンドでコピーしたファイルを記録するログレベルを`detail`に変更しました。これにより、`info`レベルのログが簡潔になります。これらのメッセージが必要な場合は、`backup`／`restore`コマンドのログレベルを`detail`に設定してください。

**バグ修正：**

- S3のマルチパートアップロードの完了処理でエラーを検出するようにしました。 (*レビュー：Cynthia Shang, Marco Montagna。報告：Marco Montagna, Lev Kokotov, Anderson A. Mallmann。*)
- シンボリックリンクの循環検出を修正しました。 (*レビュー：Stefan Fercot。報告：Rohit Raveendran。*)
- 選択した`repo`のオプションだけをリモートに渡すようにしました。 (*レビュー：David Christensen, Cynthia Shang。報告：Greg Sabino Mullane, David Christensen。*)

**改善：**

- バイナリープロトコルを導入しました。 (*レビュー：Cynthia Shang。*)
- `restore`でデータディレクトリを自動作成するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Chris Bandy。*)
- `restore`で`--type=lsn`を指定できるようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。提案：James Coleman。*)
- `backup`／`restore`でコピーしたファイルを記録するログレベルをdetailに変更しました。 (*レビュー：Stefan Fercot。提案：Jens Wilke。*)
- チェックポイントのLSNが再生LSNに達するのを待つ間、ループするようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Fatih Mencutekin。*)
- `backup`ではファイル総数を、`restore`ではサイズとファイル総数をログに記録するようにしました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの不具合修正：**

- ユーザーガイドの誤ったホスト名を修正しました。 (*レビュー：Stefan Fercot。報告：Greg Sabino Mullane。*)

**ドキュメントの改善：**

- コントリビューションのドキュメントを更新し、プルリクエストのテンプレートを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- ユーザーガイド内のバックアップの説明を再構成しました。 (*レビュー：Cynthia Shang。*)
- コマンドリファレンスで、`restore`の`--type`の動作を明確にしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- ドキュメントとコメントの誤記を修正しました。 (*貢献：Eric Radman。レビュー：David Steele。*)

**テストスイートの改善：**

- テストパスがリポジトリパス内にあるかどうかのチェックを追加しました。 (*レビュー：Greg Sabino Mullane。提案：Greg Sabino Mullane。*)
- CodeQLによる静的コード解析を追加しました。 (*レビュー：Cynthia Shang。*)
- 標準的なパターンを使用するようテストを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.34リリースノート {#v234-release-notes}

*PostgreSQL 14のサポート*

*2021年6月7日リリース*

**バグ修正：**

- 以前の`restore`で残ったスプールファイルに関する問題を修正しました。 (*レビュー：Cynthia Shang, Stefan Fercot, Floris van Nee。報告：Floris van Nee。*)
- 大量のテーブルスペースのリンクをチェックする際の問題を修正しました。 (*レビュー：Cynthia Shang, Avinash Vallarapu。報告：Avinash Vallarapu。*)
- `restore`中にタイムアウトしないよう、不要になったリモート接続を解放するようにしました。 (*レビュー：Cynthia Shang。報告：Francisco Miguel Biete Banon。*)
- 有効なオプションが指定したコマンドでは無効な場合の`help`を修正しました。 (*レビュー：Stefan Fercot。報告：Cynthia Shang。*)

**新機能：**

- PostgreSQL 14のサポートを追加しました。 (*レビュー：Cynthia Shang。*)
- GCEインスタンス向けにGCSの自動認証を追加しました。 (*レビュー：Jan Wieck, Daniel Farina。*)
- バックアップ履歴を期限切れとして削除する`repo-retention-history`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。*)
- `db-exclude`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)

**改善：**

- アーカイブの期限切れ処理のログレベルをdetailからinfoに変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `restore`でstanzaのアーカイブスプールパスを削除するようにしました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)
- `backup`のコピー中は、ファイルのアトミックな書き込みやパスの同期を行わないようにしました。 (*レビュー：Stephen Frost, Stefan Fercot, Cynthia Shang。*)

**ドキュメントの改善：**

- コントリビューションのドキュメントを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele, Stefan Fercot。*)
- RHEL/CentOSのユーザーガイドを1つのドキュメントに統合しました。 (*レビュー：Cynthia Shang。*)
- `repo-s3-role`は`ARN`ではないことを明確にしました。 (*貢献：Isaac Yuen。レビュー：David Steele。*)


### v2.33リリースノート {#v233-release-notes}

*複数リポジトリとGCSのサポート*

*2021年4月5日リリース*

**バグ修正：**

- オプションに関する警告によって非同期の`archive-get`／`archive-push`が動作しなくなる問題を修正しました。 (*レビュー：Cynthia Shang。報告：Lev Kokotov。*)
- バックアップ中のアーカイブコピーで発生するメモリリークを修正しました。 (*レビュー：Cynthia Shang。報告：Christian ROUX, Efremov Egor。*)
- 暗号化パスフレーズの生成時にスタックがオーバーフローする問題を修正しました。 (*レビュー：Cynthia Shang。報告：bsiara。*)
- S3リポジトリでの`repo-ls` `/`を修正しました。 (*レビュー：Cynthia Shang。報告：Lesovsky Alexey。*)

**新機能：**

- 複数リポジトリに対応しました。 (*貢献：Cynthia Shang, David Steele。レビュー：Stefan Fercot, Stephen Frost。*)
- リポジトリストレージとしてGCSに対応しました。 (*レビュー：Cynthia Shang, Daniel Farina。*)
- `archive-header-check`オプションを追加しました。 (*レビュー：Stephen Frost, Cynthia Shang。提案：Hans-Jürgen Schönig。*)

**改善：**

- 選択的リストアの対象に、再作成されたシステムデータベースを含めるようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)
- S3の署名対象ヘッダーから`content-length`を除外しました。 (*レビュー：Cynthia Shang。提案：Brian P Bockelman。*)
- 使用頻度の低いリポジトリストレージオプションを統合しました。 (*レビュー：Cynthia Shang。*)
- `./configure --with-configdir`で`config-path`のデフォルト値を変更できるようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)
- `backup`中のアーカイブコピーをログに記録するようにしました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)

**ドキュメントの改善：**

- リファレンスを更新し、ユーザーガイドの例へのリンクを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 選択的リストアのドキュメントに注意事項を追加しました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)
- `archive-copy`のドキュメントに`compress-type`の説明を補いました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)
- `compress-type`の値ごとに`compress-level`のデフォルト値を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 必要なNFS設定はPostgreSQLと同じであることを明記しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.32リリースノート {#v232-release-notes}

*リポジトリコマンド*

*2021年2月8日リリース*

**バグ修正：**

- 前回の再開処理でバックアップが一部削除された後の再開処理を修正しました。 (*レビュー：Cynthia Shang。報告：Tom Swartz。*)

**新機能：**

- `repo-ls`コマンドを追加しました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)
- `repo-get`コマンドを追加しました。 (*貢献：Stefan Fercot, David Steele。レビュー：Cynthia Shang。*)
- `archive-mode-check`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele, Michael Banck。*)

**改善：**

- `archive-get`の性能を改善しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- `expire`コマンドのドキュメントを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.31リリースノート {#v231-release-notes}

*軽微なバグ修正と改善*

*2020年12月7日リリース*

**バグ修正：**

- データベース名の先頭文字に`[`、`#`、`space`を使用できるようにしました。 (*レビュー：Stefan Fercot, Cynthia Shang。報告：Jefferson Alexandre。*)
- `restore`の種類が`standby`の場合、PostgreSQL 12でのみ`standby.signal`を作成するようにしました。 (*修正：Stefan Fercot。レビュー：David Steele。報告：Keith Fiske。*)

**新機能：**

- 履歴ファイルを期限切れとして削除するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- `info`コマンドの`text`出力でページチェックサムエラーを報告するようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)
- `repo-azure-endpoint`オプションを追加しました。 (*レビュー：Cynthia Shang, Brian Peterson。提案：Brian Peterson。*)
- `pg-database`オプションを追加しました。 (*レビュー：Cynthia Shang。*)

**改善：**

- 指定したstanzaが存在しない場合の`info`コマンドの出力を改善しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。提案：uspen。*)
- `backup`／`restore`コマンドで大きなファイル一覧を扱う際の性能を改善しました。 (*レビュー：Cynthia Shang, Oscar。*)
- バックアップ開始時のPostgreSQLのスリープ処理に再試行を追加しました。 (*レビュー：Cynthia Shang。提案：Vitaliy Kukharik。*)

**ドキュメントの改善：**

- RHEL/CentOS 6のドキュメントをRHEL/CentOS 8のものに置き換えました。


### v2.30リリースノート {#v230-release-notes}

*PostgreSQL 13のサポート*

*2020年10月5日リリース*

**バグ修正：**

- バックアップユーザーが`pg_settings`を読み取れない場合に、ヒント付きのエラーを返すようにしました。 (*レビュー：Stefan Fercot, Cynthia Shang。報告：Mohamed Insaf K。*)

**新機能：**

- PostgreSQL 13に対応しました。 (*レビュー：Cynthia Shang。*)

**改善：**

- PostgreSQLバージョンの識別を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)
- 作業ディレクトリのエラーメッセージを改善しました。 (*レビュー：Stefan Fercot。*)
- WALセグメントが見つからない場合に、stanzaの開始に関するヒントを追加しました。 (*貢献：David Christensen。レビュー：David Steele。*)
- プロトコルバージョンの不一致に関するヒントを追加しました。 (*レビュー：Cynthia Shang。提案：loop-evgeny。*)

**ドキュメントの改善：**

- リモートで実行する場合はpgBackRestのバージョンを一致させる必要があることを明記しました。 (*レビュー：Cynthia Shang。提案：loop-evgeny。*)
- infoコマンドの説明をリファレンスに移動し、ユーザーガイドへのリンクを追加しました。 (*レビュー：Cynthia Shang。提案：Christophe Courtois。*)
- CentOS/RHELユーザーガイドのyumリポジトリのパスを更新しました。 (*貢献：Heath Lord。レビュー：David Steele。*)


### v2.29リリースノート {#v229-release-notes}

*AWSでのS3認証情報の自動取得*

*2020年8月31日リリース*

**バグ修正：**

- `local`／`remote`プロセスを終了する際のエラーを抑止するようにしました。コマンドは完了しているため、エラーを返しても逆効果ですが、通常とは異なる事象が発生したことを示す**警告**は引き続き出力します。 (*レビュー：Cynthia Shang。報告：argdenis。*)
- ファイル名やデータベース名に`=`文字が含まれる場合の問題を修正しました。 (*レビュー：Bastian Wegge, Cynthia Shang。報告：Brad Nicholson, Bastian Wegge。*)

**新機能：**

- AWSインスタンスで一時的なS3認証情報を自動取得するようにしました。 (*貢献：David Steele, Stephen Frost。レビュー：Cynthia Shang, David Youatt, Aleš Zelený, Jeanette Bromage。*)
- リストア時にアーカイブを無効にする`archive-mode`オプションを追加しました。 (*レビュー：Stephen Frost。提案：Stephen Frost。*)

**改善：**

- PostgreSQL 13 beta3に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。
- S3／Azureストレージの`list`／`remove`を非同期化しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)
- マニフェストの作成時に、unloggedリレーションを検出する処理のメモリ使用量を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost, Brad Nicholson, Oscar。提案：Oscar, Brad Nicholson。*)
- 非同期プロセスをforkした後、ファイルディスクリプターを積極的に閉じるようにしました。 (*レビュー：Stephen Frost, Cynthia Shang。*)
- バックアップ時のリモート接続を閉じるタイミングを、アーカイブチェックの後に遅らせました。 (*貢献：Floris van Nee。レビュー：David Steele。*)
- 詳細なエラー出力を改善しました。 (*レビュー：Cynthia Shang。*)
- TLSのエラー報告を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)

**ドキュメントの不具合修正：**

- `compress-type`オプションのリファレンスに`none`を追加し、例を修正しました。 (*報告：Ugo Bellavance, Don Seiler。*)
- `repo-type`オプションのリファレンスに、欠落していた`azure`の種類を追加しました。 (*修正：Don Seiler。レビュー：David Steele。*)
- `repo-cipher-type`オプションのリファレンスの誤記を修正しました。 (*修正：Don Seiler。レビュー：David Steele。*)

**ドキュメントの改善：**

- `expire-auto`が無効な場合は、`expire`を定期的に実行する必要があることを明確にしました。 (*レビュー：Douglas J Hunley。提案：Douglas J Hunley。*)


### v2.28リリースノート {#v228-release-notes}

*Azureリポジトリストレージ*

*2020年7月20日リリース*

**バグ修正：**

- `restore`の`--force`が`--force --delta`と同じ動作をする問題を修正しました。この問題により、`restore`がファイルを上書きせず、タイムスタンプとサイズに基づいて置き換えていたため、更新すべきファイルが変更されずに残る場合がありました。通常の`restore`と`restore`の`--delta`は、この問題の影響を受けませんでした。 (*レビュー：Cynthia Shang。*)

**新機能：**

- リポジトリストレージとしてAzureに対応しました。 (*レビュー：Cynthia Shang, Don Seiler。*)
- `expire-auto`オプションを追加しました。バックアップの成功後に自動実行する期限切れ処理を無効にできます。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。*)

**改善：**

- S3のマルチパートアップロードを非同期化しました。 (*レビュー：Stephen Frost。*)
- `backup`、`restore`、`archive-get`、`archive-push`に自動再試行を追加しました。 (*レビュー：Cynthia Shang。*)
- バックアップの制御に使用するPostgreSQLセッションで、クエリーの並列実行を無効にしました。 (*レビュー：Stefan Fercot。*)
- PostgreSQL 13 beta2に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。
- 無効なHTTPレスポンスステータスの処理を改善しました。 (*レビュー：Cynthia Shang。*)
- `archive-get`コマンドで`pg1-path`オプションがない場合のエラーを改善しました。 (*レビュー：Cynthia Shang。*)
- タイムラインの切り替え後にチェックサムによる差分処理を有効にする場合のヒントを追加しました。 (*レビュー：Matt Bunter, Cynthia Shang。*)
- 適切な箇所で、`postmaster`の代わりにPostgreSQLという名称を使用するようにしました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの不具合修正：**

- `repo-retention-full-type`オプションの誤った例を修正しました。 (*報告：Höseyin Sönmez。*)
- HTMLとmanのコマンドリファレンスから内部コマンドを削除しました。 (*報告：Cynthia Shang。*)

**ドキュメントの改善：**

- ユーザーガイドのビルドに使用するPostgreSQLのバージョンを更新しました。また、特定のバージョンでビルドしたガイドでも一定範囲のPostgreSQLバージョンに適用できることを示すため、バージョン範囲を追加しました。 (*レビュー：Stephen Frost。*)
- 特定のバックアップセットの期限切れ処理に関するFAQを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- デフォルトのPITRの動作を明確にするため、FAQを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.27リリースノート {#v227-release-notes}

*期限切れ処理の改善と圧縮ドライバー*

*2020年5月26日リリース*

**バグ修正：**

- ファイルへのリンクがパスへのリンクに含まれているかを確認する処理を修正しました。 (*レビュー：Cynthia Shang。報告：Christophe Cavallié。*)
- 同期`archive-push`で`pg-path1`を省略できるようにしました。 (*レビュー：Cynthia Shang。報告：Jerome Peng。*)
- `expire`コマンドが停止ファイルの有無を確認するようになりました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- HTTPレスポンスに理由句がない場合に対応しました。 (*レビュー：Cynthia Shang。報告：Tenuun。*)
- lz4圧縮のフラッシュ時のバッファーサイズを増やしました。 (*レビュー：Cynthia Shang。報告：Eric Radman。*)
- `remote`コマンドで`pg-host*`と`repo-host*`オプションを無視するようにしました。 (*レビュー：Cynthia Shang。報告：Pavel Suderevsky。*)
- `remote`コマンドで`pg1-*`オプションが欠落する場合がある問題を修正しました。 (*レビュー：Cynthia Shang。報告：Andrew L'Ecuyer。*)

**新機能：**

- フルバックアップの期間に基づく保持に対応しました。`--repo-retention-full-type`オプションで、日数で指定した期間に基づいてフルバックアップを保持できます。 (*貢献：Cynthia Shang, Pierre Ducroquet。レビュー：David Steele。*)
- バックアップを個別に期限切れとして削除できるようにしました。保持設定に関係なく、ユーザーが指定したバックアップを削除できます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- Zstandard圧縮に対応しました。`compress-type=zst`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*レビュー：Cynthia Shang。*)
- bzip2圧縮に対応しました。`compress-type=bz2`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*貢献：Stephen Frost。レビュー：David Steele, Cynthia Shang。*)
- `info`コマンドに`backup`／`expire`の実行状態を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

**改善：**

- `repo-retention-archive`のしきい値に達した場合にのみ、WALアーカイブを期限切れとして削除するようにしました。従来、最初のフルバックアップより前のWALは、最初のフルバックアップの後に削除されていました。今後は保持設定に従って保持されます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- FIPSが有効な場合でもS3を使用できるよう、独自のMD5実装を追加しました。 (*レビュー：Cynthia Shang, Stephen Frost。提案：Brian Almeida, John Kelly。*)
- PostgreSQL 13 beta1に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。 (*レビュー：Cynthia Shang。*)
- `buffer-size`のデフォルト値を`1MiB`に減らしました。 (*レビュー：Stephen Frost。*)
- リポジトリホスト以外で`expire`を実行した場合に、わかりやすいエラーを返すようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.26リリースノート {#v226-release-notes}

*ノンブロッキングTLS*

*2020年4月20日リリース*

**バグ修正：**

- マニフェストの正規表現から空の部分式を削除しました。他のプラットフォームでは問題なく動作しているようでしたが、MacOSでは問題が発生していました。 (*修正：David Raftis。レビュー：David Steele。*)

**改善：**

- ノンブロッキングTLSを実装しました。 (*レビュー：Slava Moudry, Cynthia Shang, Stephen Frost。*)
- バックアップでコピーするサイズの制限を、WALに記録されるファイルだけに適用するようにしました。以前の動作では、バックアップ内の`postgresql.conf`や`postgresql.auto.conf`が切り詰められる可能性がありました。 (*レビュー：Cynthia Shang。*)
- TCPキープアライブのオプションを設定できるようにしました。 (*提案：Marc Cousin。*)
- `io-timeout`オプションを追加しました。 (*レビュー：Cynthia Shang。*)


### v2.25リリースノート {#v225-release-notes}

*LZ4圧縮のサポート*

*2020年3月26日リリース*

**新機能：**

- lz4圧縮のサポートを追加しました。`compress-type=lz4`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*レビュー：Cynthia Shang。*)
- `expire`コマンドに`--dry-run`オプションを追加しました。dry-runを使用すると、実際には何も削除せずに、`expire`コマンドが削除するバックアップとアーカイブを確認できます。 (*貢献：Cynthia Shang, Luca Ferrari。レビュー：David Steele。提案：Marc Cousin。*)

**改善：**

- リモートでのマニフェスト作成の性能を改善しました。 (*提案：Jens Wilke。*)
- Linuxでのkeepaliveオプションの検出を修正しました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- 標準規格に関するフラグを正しく設定するため、configureにホストの検出を追加しました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- `compress`/`compress-level`オプションを、使用しないコマンドから削除しました。これらのコマンド（`restore`、`archive-get`など）は圧縮オプションを使っていませんでしたが、コマンドラインでの指定を許可していました。今後は、これらのオプションをコマンドラインで指定するとエラーになります。このエラーが発生した場合は、使用しないオプションを削除してください。 (*レビュー：Cynthia Shang。*)
- バックアップでコピーするファイルサイズを、バックアップ開始時に報告されたサイズに制限しました。バックアップ中にファイルが増大しても、リカバリー時のWAL再生で再構築されるため、追加データをコピーする必要はありません。 (*レビュー：Cynthia Shang。*)


### v2.24 リリースノート {#v224-release-notes}

*目標時刻に応じたバックアップセットの自動選択*

*2020年2月25日リリース*

**バグ修正：**

- 非同期アーカイブコマンドでゾンビプロセスが発生しないようにしました。 (*レビュー：Stephen Frost。報告：Adam Brusselback, ejberdecia。*)
- `archive-get`/`archive-push`/`restore`をPostgreSQLホスト以外で実行した場合にエラーを出すようにしました。 (*レビュー：Stephen Frost。報告：Jesper St John。*)
- サイズやエンコーディングの指定がない場合に、HTTPコンテンツをeofまで読み込むようにしました。 (*レビュー：Cynthia Shang。報告：Christian ROUX。*)
- Perlで作成されたバックアップを再開する場合の問題を修正しました。この場合、再開可能なバックアップは無視するのが適切ですが、Perlが書いた部分的なマニフェストは形式がわずかに異なり、Cコードでは読み込めませんでした。この状況を検出して正常に処理を続けられるよう、検証を追加しました。 (*報告：Kacey Holston。*)

**新機能：**

- リストア時に目標時刻を指定した場合、バックアップセットを自動選択するようにしました。自動選択を行うのは`--set`を指定していない場合だけです。指定された目標時刻に対応するバックアップセットが見つからない場合は、最新の（デフォルトの）バックアップセットを使用します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- バックアップ時に`pg_internal.init`の一時ファイルを除外するようにしました。 (*レビュー：Cynthia Shang。提案：Michael Paquier。*)
- `backup`でマニフェストに対する検証を追加しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- lock-botがロック済みのissueにコメントを追加しないようにしました。 (*提案：Christoph Berg。*)


### v2.23 リリースノート {#v223-release-notes}

*不具合修正*

*2020年1月27日リリース*

**バグ修正：**

- ファイルの欠落によってマニフェストが破損する問題を修正しました。バックアップ中にPostgreSQLがファイルを削除した場合（またはスタンバイにファイルがなかった場合）、次のファイルがコピーされず、マニフェストも更新されないことがありました。この場合、そのバックアップをリストアするとエラーが発生していました。 (*レビュー：Cynthia Shang。報告：Vitaliy Kukharik。*)

**改善：**

- libxml2のビルドオプションに、`xml2-config`の代わりに`pkg-config`を使用するようにしました。 (*貢献：David Steele, Adrian Vondendriesch。*)
- `backup`/`restore`で、マニフェストにチェックサムが設定されていることを検証するようにしました。 (*レビュー：Cynthia Shang。*)


### v2.22 リリースノート {#v222-release-notes}

*不具合修正*

*2020年1月21日リリース*

**バグ修正：**

- タイムラインの変換エラーを修正しました。タイムラインは、バックアップ後にアーカイブ内のWALセグメントを検証するために必要です。基数`16`ではなく`10`で変換していたため、タイムラインが`0xA`以上になるとエラーが発生していました。 (*報告：Lukas Ertl, Eric Veldhuyzen。*)


### v2.21 リリースノート {#v221-release-notes}

*Cへの移行完了*

*2020年1月15日リリース*

**バグ修正：**

- 非同期コマンドがオプションを無視する問題を修正しました。非同期の`archive-get`/`archive-push`プロセスは、`[global:archive-get]`などのコマンド別設定セクションに設定されたオプションを読み込んでいませんでした。 (*レビュー：Cynthia Shang。報告：Urs Kramer。*)
- ファイル名の`\`の扱いを修正しました。マニフェストのチェックサム計算時に`\`を正しくエスケープしていなかったため、マニフェストを読み込めませんでした。クラスターのファイル名に`\`が含まれることはほぼないと考えられるため、実運用で深刻な問題になる可能性は低そうです。

**新機能：**

- pgBackRestの実装がすべてCになりました。
- `pg-user`オプションを追加しました。PostgreSQLへの接続時のデータベースユーザー名を指定します。指定しない場合、pgBackRestは従来どおりローカルのOSユーザーまたは`PGUSER`を使って接続します。 (*貢献：Mike Palmiotto。レビュー：David Steele。*)
- S3ドライバーでパス形式のURIを使用できるようにしました。

**改善：**

- `backup`コマンドの実装をすべてCに移行しました。 (*レビュー：Cynthia Shang。*)


### v2.20 リリースノート {#v220-release-notes}

*不具合修正*

*2019年12月12日リリース*

**バグ修正：**

- `PGDATA`がシンボリックリンクの場合のarchive-push/archive-getを修正しました。これらのコマンドは`cwd()`を`PGDATA`として使おうとしていましたが、`PGDATA`がシンボリックリンクの場合、pgBackRestに設定したパスと一致しませんでした。`cwd()`がpgBackRestのパスと一致しない場合は、そのパスに`chdir()`して、次の`cwd()`が最初の呼び出し結果と一致することを確認するようにしました。 (*報告：Stephen Frost, Milosz Suchy。*)
- `expire`コマンドで`backup.info`を再構築する際の参照リストを修正しました。`backup`コマンドはまだPerl版の再構築処理を使っているため、この問題が発生するのは、**1)** `backup.info`に記載されていないバックアップがあり、かつ**2)** 通常のように`backup`の後で実行するのではなく、`expire`コマンドを直接実行する場合だけです。この条件が重なることはまれなため、実運用では問題になっていないと思われます。
- gzipの展開中に予期しないEOFが発生するとセグメンテーション違反になる問題を修正しました。 (*報告：Stephen Frost。*)


### v2.19 リリースノート {#v219-release-notes}

*Cへの移行とバグ修正*

*2019年11月12日リリース*

**バグ修正：**

- deltaリストアでリモートがタイムアウトする問題を修正しました。大部分が変更されていないクラスターにdeltaリストアを行う場合、`protocol-timeout`の時間内にリポジトリからファイルを取得しないと、リモートがタイムアウトすることがありました。これを防ぐため、keepaliveを追加しました。 (*報告：James Sewell, Jens Wilke。*)
- 重複したHTTPヘッダーの扱いを修正しました。HTTPヘッダーが繰り返される場合、従来のようにエラーを出すのではなく、カンマで区切られた単一のヘッダーと同等に扱うようにしました。 (*報告：donicrosby。*)

**改善：**

- `info`コマンドのJSON出力を整形しないようにしました。改行のないJSONのほうが、監視システムで容易に取り込めます。必要に応じて、`jq`などの外部ツールで整形できます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `check`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- pgBackRestへの貢献方法を文書化しました。 (*貢献：Cynthia Shang, David Steele。*)
- `auto-stop`オプションを使用できる最終バージョンを文書化しました。 (*貢献：Brad Nicholson。レビュー：David Steele。*)

**テストスイートの改善：**

- `--vm=none`の場合にもコンテナーテストのパスが使われる問題を修正しました。 (*提案：Stephen Frost。*)
- expectテストでタイムゾーンが一致しない問題を修正しました。 (*提案：Stephen Frost。*)
- デフォルトでは組み込みlibcコードを自動生成しないようにしました。 (*提案：Stephen Frost。*)


### v2.18 リリースノート {#v218-release-notes}

*PostgreSQL 12のサポート*

*2019年10月1日リリース*

**新機能：**

- PostgreSQL 12をサポートしました。
- 詳細なテキスト出力を行うため、`info`コマンドに`set`オプションを追加しました。追加される詳細には、選択的リストアに使用できるデータベース、およびテーブルスペースとシンボリックリンクの一覧と各デフォルトの参照先が含まれます。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Stephen Frost, ejberdecia。*)
- リストアの種類に`standby`を追加しました。PostgreSQL < 12ではrecovery.confにstandby_mode=onを自動追加し、PostgreSQL ≥ 12では`standby.signal`を作成することで、PostgreSQLのバージョンをまたいで共通のインターフェースを提供します。 (*レビュー：Cynthia Shang。*)

**改善：**

- `restore`コマンドの実装をすべてCに移行しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- `db-timeout`と`protocol-timeout`の関係を文書化しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：James Chanco Jr。*)
- スタンバイのリポジトリに関する説明を明確にしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 時刻に基づくポイントインタイムリカバリーのFAQを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.17 リリースノート {#v217-release-notes}

*Cへの移行とバグ修正*

*2019年9月3日リリース*

**バグ修正：**

- テーブルやセグメントが非常に多い場合に、マニフェストの作成が遅くなる問題を改善しました。 (*報告：Jens Wilke。*)
- 特殊ファイルの除外処理を修正しました。 (*報告：CluelessTechnologist, Janis Puris, Rachid Broum。*)

**改善：**

- `stanza-create/update/delete`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `start`/`stop`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- ログディレクトリとログファイルを、それぞれ`0750`/`0640`モードで作成するようにしました。 (*提案：Damiano Albani。*)

**ドキュメントの不具合修正：**

- カスタムパッケージを指定しても`yum.p.o`のパッケージがインストールされる問題を修正しました。 (*報告：Joe Ayers, John Harvey。*)

**ドキュメントの改善：**

- 一般ユーザーでpgBackRestをビルドするようにしました。 (*提案：Laurenz Albe。*)


### v2.16 リリースノート {#v216-release-notes}

*Cへの移行とバグ修正*

*2019年8月5日リリース*

**バグ修正：**

- S3の`RequestTimeTooSkewed`エラーで即時終了せず、再試行するようにしました。 (*報告：sean0101n, Tim Garton, Jesper St John, Aleš Zelený。*)
- `HEAD`リクエストへの応答の`transfer-encoding`を誤って処理する問題を修正しました。 (*報告：Pavel Suderevsky。*)
- gcc 9の最適化で顕在化したスコープ違反を修正しました。 (*報告：Christian Lange, Ned T. Crigler。*)

**新機能：**

- 標準以外のS3サービスポートを設定するため、`repo-s3-port`オプションを追加しました。

**改善：**

- `backup`用の`local`コマンドの実装をすべてCに移行しました。 (*貢献：David Steele, Cynthia Shang。*)
- `check`コマンドの実装を一部Cに移行しました。 (*レビュー：Cynthia Shang。*)


### v2.15 リリースノート {#v215-release-notes}

*expireのC実装*

*2019年6月25日リリース*

**バグ修正：**

- アーカイブの保持処理で過剰に期限切れにしてしまう問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Mohamad El-Rifai。*)

**改善：**

- `expire`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- restore用の`local`コマンドの実装をすべてCに移行しました。
- `$PGUSER`が機能するよう、固定されたPostgreSQLユーザーの指定を削除しました。 (*提案：Julian Zhang, Janis Puris。*)
- configureの`--prefix`オプションを反映するようにしました。 (*提案：Daniel Westermann。*)
- `repo-s3-verify-ssl`オプションを`repo-s3-verify-tls`に改名しました。pgBackRestはいずれのSSLプロトコルバージョンもサポートしていないため（すべて安全でないとみなされています）、新しい名前のほうが適切です。古い名前も引き続き使用できます。

**ドキュメントの改善：**

- ドキュメントにFAQを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL ≥ 9.6のドキュメントで`wal_level=replica`を使用するようにしました。 (*提案：Patrick McLaughlin。*)


### v2.14 リリースノート {#v214-release-notes}

*バグ修正と改善*

*2019年5月20日リリース*

**バグ修正：**

- `archive-push`/`archive-get`で`process-max` > 8の場合にセグメンテーション違反が起きる問題を修正しました。 (*報告：Jens Wilke。*)

**改善：**

- `force`を指定して`stanza-delete`を実行した場合、データベースの確認を省略するようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：hatifnatt。*)
- 複数プラットフォームへの対応を改善するため、`configure`スクリプトを追加しました。

**ドキュメントの機能：**

- CentOS/RHEL 6/7向けのユーザーガイドを追加しました。


### v2.13 リリースノート {#v213-release-notes}

*不具合修正*

*2019年4月18日リリース*

**バグ修正：**

- 長さゼロの読み取りを想定していないI/Oフィルターで、それにより問題が起きる不具合を修正しました。 (*報告：brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru。*)
- `local`/`remote`プロセスからのエラー報告の信頼性に関する問題を修正しました。
- 書き込み、同期、クローズ時にPosix/CIFSのエラーメッセージが誤ったファイル名を報告する問題を修正しました。


### v2.12 リリースノート {#v212-release-notes}

*archive-pushのC実装*

*2019年4月11日リリース*

**重要な注意事項**：新しいTLS/SSL実装では、RFC-2818に従いS3バケット名にドットを使用できません。このセキュリティ修正は、規格に準拠したホスト名の検証に必要です。

**バグ修正：**

- パスオプションが/で終わる場合の問題を修正しました。 (*報告：Marc Cousin。*)
- `archive-get`コマンドに`log-level-file=off`を設定した場合の問題を修正しました。 (*報告：Brad Nicholson。*)
- CコードでもPerlと同様に`host:port`形式のオプションを認識するよう修正しました。 (*報告：Kyle Nevins。*)
- `remote`/`local`コマンドのログオプションの問題を修正しました。

**改善：**

- `archive-push`コマンドの実装をすべてCに移行しました。
- `process-max`の上限を`999`に引き上げました。 (*提案：Rakshitha-BR。*)
- S3バケット名にドットが含まれる場合のエラーメッセージを改善しました。

**ドキュメントの改善：**

- S3互換オブジェクトストアがサポートされることを明確にしました。 (*提案：Magnus Hagander。*)


### v2.11 リリースノート {#v211-release-notes}

*archive-getのC実装*

*2019年3月11日リリース*

**バグ修正：**

- 書き込みの途中でエラーが発生した場合に、WALセグメントが切り詰められる可能性がある問題を修正しました。 (*報告：blogh。*)
- stanzaを指定するとinfoコマンドの出力にWAL min/maxが含まれない問題を修正しました。 (*修正：Stefan Fercot。レビュー：David Steele。*)
- CからPerlへ渡すオプションのJSONが規格に準拠していなかった問題を修正しました。 (*報告：Leo Khomenko。*)

**改善：**

- `archive-get`コマンドの実装をすべてCに移行しました。
- 古いPerlバージョンでソケットのkeepaliveを有効にしました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- パラメーターを受け付けないコマンドにパラメーターを渡した場合、エラーを出すようにしました。 (*提案：Jason O'Donnell。*)
- アーカイブ内にWALセグメントが見つからない場合のヒントを追加しました。 (*提案：Hans-Jürgen Schönig。*)
- 証明書でホスト名が見つからない場合のエラーを改善しました。 (*提案：James Badger。*)
- デバッグ用に、`backup.manifest`に追加のオプションを記録するようにしました。 (*貢献：blogh。レビュー：David Steele。*)

**ドキュメントの改善：**

- ドキュメントのデフォルトの対象バージョンをPostgreSQL 10に更新しました。


### v2.10 リリースノート {#v210-release-notes}

*不具合修正*

*2019年2月9日リリース*

**バグ修正：**

- `archive-get`に必要な、未実装だったS3ドライバーのメソッドを追加しました。 (*報告：mibiio。*)
- `pg-path`の設定が不正な場合の確認処理を修正しました。 (*報告：James Chanco Jr。*)


### v2.09 リリースノート {#v209-release-notes}

*軽微な改善とバグ修正*

*2019年1月30日リリース*

**バグ修正：**

- 非同期の状態ファイルが複数あると、処理を継続できないエラーになる問題を修正しました。 (*報告：Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley。*)

**改善：**

- `info`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- stanzaが存在しない場合の`info`コマンドのテキストメッセージを簡潔にしました。リポジトリのパスを「the repository」に置き換えました。
- MacOSビルド用に、Makefileに`_DARWIN_C_SOURCE`フラグを追加しました。 (*貢献：Douglas J Hunley。レビュー：David Steele。*)
- CのTLSクライアントのアドレス検索を、新しい方式を使うよう更新しました。 (*提案：Bruno Friedmann。*)
- `strcasecmp()`と`fd_set`用に、Posix準拠のヘッダーをインクルードしました。 (*提案：ucando。*)

**ドキュメントの不具合修正：**

- リポジトリパスが固定されていた問題を修正しました。 (*報告：Heath Lord。*)

**ドキュメントの改善：**

- 暗号化は常にクライアント側で行うことを明確にしました。 (*提案：Bruce Burdick。*)
- ドキュメント用ホストを構築する例を追加しました。
- マニフェストの変数、リスト、リスト項目で`if`を使用できるようにしました。


### v2.08 リリースノート {#v208-release-notes}

*軽微な改善とバグ修正*

*2019年1月2日リリース*

**バグ修正：**

- S3オブジェクトの格納直後に、その情報を要求する処理を削除しました。 (*報告：Matt Kunkel。*)
- `archive-get-queue-max`を`size`型に修正しました。 (*報告：Ronan Dunklau。*)
- 現在のユーザーの`uid`/`gid`に対応する名前がない場合のエラーメッセージを追加しました。 (*報告：Camilo Aguilar。*)
- PostgreSQL < 9.5で`--target-action=shutdown`を指定した場合にエラーを出すようにしました。

**改善：**

- S3接続にTCP keepaliveを設定しました。 (*提案：Ronan Dunklau。*)
- 最新のバックアップを最後に表示するよう、`info`コマンドのテキスト出力の順序を変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Ryan Lambert。*)
- 必要な場合だけファイルの所有権を変更するようにしました。
- S3エラーを出す際に`authentication`ヘッダーをマスクするようにしました。 (*提案：Brad Nicholson。*)

**ドキュメントの改善：**

- `target-action`が有効になる条件と、PostgreSQLバージョンごとの対応を明確にしました。 (*提案：Keith Fiske。*)
- バケットに合わせてリージョンとエンドポイントを正しく設定する必要があることを明確にしました。 (*提案：Pritam Barhate。*)
- ドキュメントのビルド方法を文書化しました。


### v2.07 リリースノート {#v207-release-notes}

*バックアップのチェックサムによる差分判定の自動化*

*2018年11月16日リリース*

**バグ修正：**

- 接続エラー時に`archive-push-queue-max`が守られない問題を修正しました。 (*報告：Lardière Sébastien。*)
- `archive-push-queue-max`を超えたかどうかの判定に固定のWALセグメントサイズを使っていた問題を修正しました。
- ログファイルを開けなかった後、処理を続けるべき場合にもエラーになる問題を修正しました。 (*報告：vthriller。*)

**新機能：**

- タイムラインの切り替えなどの異常を検出した場合に、バックアップのチェックサムによる差分判定を自動で有効にするようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- S3の内部エラー`500`だけでなく、すべての`5xx`エラーを再試行するようにしました。 (*提案：Craig A. James。*)


### v2.06 リリースノート {#v206-release-notes}

*チェックサムによる差分判定を使うバックアップとPostgreSQL 11のサポート*

*2018年10月15日リリース*

**バグ修正：**

- S3ドライバーでURIのエンコーディングが欠けていた問題を修正しました。 (*報告：Dan Farrell。*)
- 設定ファイルにオプションが重複した場合のエラーメッセージが誤っていた問題を修正しました。 (*報告：Jesper St John。*)
- `info`レベルのログで、戻り値を誤ってエラーとして報告する問題を修正しました。`archive-get`の戻りコード1が、動作自体は正常であるにもかかわらず、`info`レベルでエラーメッセージとして記録されていました。

**新機能：**

- 増分バックアップに、チェックサムによる差分判定を追加しました。この方式では、タイムスタンプではなくチェックサムを使ってファイルが変更されたかどうかを判断します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- WALセグメントサイズの設定を含め、PostgreSQL 11をサポートしました。

**改善：**

- リンク先のテーブルスペースディレクトリでは、現在のPostgreSQLバージョンのサブディレクトリ以外の全ファイルを無視するようにしました。従来は、ほかのファイルが存在し、その所有者がPostgreSQLユーザーでない場合にエラーが発生していました。
- stanzaの暗号方式を表示するよう、`info`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Douglas J Hunley。*)
- ファイル名の特殊文字への対応を改善しました。
- pgBackRestの設定ファイルで`delta`オプションを指定できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- SSHのセキュリティを高めるため、`authorized_hosts`で`command`を使用するようにしました。 (*提案：Stephen Frost, Magnus Hagander。*)
- 設定リファレンスに、`buffer-size`オプションで指定可能な値を記載しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Stéphane Schildknecht。*)


### v2.05 リリースノート {#v205-release-notes}

*環境変数によるオプション設定と、一時リレーションおよび非ログリレーションの除外*

*2018年8月31日リリース*

**バグ修正：**

- `$PGDATA`内の*相対*リンクが、誤ったパスでバックアップに保存されることがある問題を修正しました。絶対リンクには影響せず、テーブルスペースの相対リンクはほかのチェックで検出されていました。 (*報告：Cynthia Shang。*)
- 不完全な実装だった`online`オプションを`check`コマンドから削除しました。オフライン動作は、アーカイブとバックアップが正しく機能しているかを確認するという、このコマンドの目的に反します。 (*報告：Jason O'Donnell。*)
- Perlから呼び出した際、Cで発生したエラーがログに記録されない問題を修正しました。pgBackRestは正しいエラーコードで終了していましたが、デバッグに役立つエラーメッセージがありませんでした。 (*報告：Douglas J Hunley。*)
- 真偽値のオプション（例：`delta`）を複数回指定した場合の問題を修正しました。 (*報告：Yogesh Sharma。*)

**新機能：**

- すべてのオプションを環境変数で設定できるようにしました。従来はコマンドラインでしか指定できなかった`stanza`などのオプションや、コマンドラインでは指定できなかった`repo1-s3-key-secret`などの機密オプションも含まれます。
- 一時リレーションと非ログリレーション（テーブルとインデックス）のファイルを、バックアップから除外するようにしました。PostgreSQLに同機能を追加したパッチ[8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25)および[920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f)と同じロジックで実装しています。一時リレーションの除外はPostgreSQL ≥ `9.0`で有効です。非ログリレーションの除外は、この機能が導入されたPostgreSQL ≥ `9.1`で有効です。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 任意のディレクトリやファイルをバックアップから除外できるようにしました。この機能の誤用はバックアップの不整合につながるため、使用前に`--exclude`のドキュメントをよく読んでください。 (*レビュー：Cynthia Shang。*)
- `local`と`remote`サブプロセスのファイルへのログ出力を可能にする、`log-subprocess`オプションを追加しました。
- PostgreSQL 11 Beta 3をサポートしました。

**改善：**

- バックアップマニフェスト内のサイズゼロのファイルは、タイムスタンプの差にかかわらず前のマニフェストを参照できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 状態ファイルを直接確認することで、非同期の`archive-get`/`archive-push`の性能を改善しました。 (*貢献：Stephen Frost。レビュー：David Steele。*)
- コマンドに`stanza`オプションがない場合のエラーメッセージを改善しました。 (*提案：Sarah Conway。*)

**ドキュメントの不具合修正：**

- `log-path`オプションのリファレンスに記載された、不正なログレベルを修正しました。 (*報告：Camilo Aguilar。*)

**ドキュメントの改善：**

- `release.xml`で貢献者を姓と名で整理するのをやめました。リリースノートでは、貢献者の名前は常に提供されたとおりに表記してきましたが、内部IDは姓と名に基づいて割り当てようとしていました。姓と名の判別は難しい場合があり、そもそも適切な方法ではありません。ChristopheのPostgresOpen 2017での講演「人間に主キーはない」に着想を得ています。 (*提案：Christophe Pettus。*)

**テストスイートの改善：**

- テスト環境の外でLibCをビルドした場合にエラーを出すようにしました。本番用のビルドにLibCは不要になりました。


### v2.04 リリースノート {#v204-release-notes}

*バックアップの再開に関する重大な不具合修正*

*2018年7月5日リリース*

**重要な注意事項**：このリリースでは、バックアップの再開機能に関する重大な不具合を修正しています。このリリースより前に再開したバックアップは、すべて整合性がないものと見なすことを推奨します。`resume=n`を指定していない限り、前回のバックアップが失敗すると、そのバックアップを再開します。再開したバックアップは、バックアップログにメッセージ"aborted backup of same type exists, will be cleaned to remove invalid files and resumed"があるかどうかで判別できます。このメッセージがある場合、そのバックアップも、同じセット内のほかのバックアップもリストアに使用しないでください。また、リストアログを確認し、再開したバックアップをリストアしていないか調べてください。該当する場合、クラスター内のデータに不整合がある可能性があります。

**バグ修正：**

- 再開時に整合性のないバックアップが作成される重大な不具合を修正しました。`v0.82`でのリグレッションにより、再開時に中断済みバックアップのどのファイルを保持するかを判断する際のタイムスタンプ比較が失われていました。詳細は上記の注意事項を参照してください。 (*報告：David Youatt, Yogesh Sharma, Stephen Frost。*)
- クラスター内のユーザーデータベースが1つだけの場合、選択的リストアでエラーになる問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Nj Baliyan。*)
- S3認証ヘッダーのタイムスタンプがISO-8601に準拠していなかった問題を修正しました。AWSと一部のゲートウェイは、時のゼロ埋めを空白にしても受け付けていましたが、他のゲートウェイは受け付けていませんでした。 (*修正：Andrew Schwartz。レビュー：David Steele。*)

**新機能：**

- PostgreSQL 11 Beta 2をサポートしました。

**改善：**

- サーバーが`content-length`を指定しない場合、0に設定するようHTTPクライアントを改善しました。S3とそのゲートウェイは常に`content-length`または`transfer-encoding`を設定しますが、`HTTP 1.1`では必須ではなく、HAProxyなどのプロキシがどちらも含めない場合があります。 (*提案：Adam K. Sumner。*)
- PostgreSQL接続で`search_path = 'pg_catalog'`を設定するようにしました。 (*提案：Stephen Frost。*)

**ドキュメントの改善：**

- pgBackRestのビルド方法を説明するセクションを新設し、別のホストでビルドするようにしました。
- バケットの権限を制限するS3ポリシーの例を追加しました。 (*提案：Douglas J Hunley, Jason O'Donnell。*)


### v2.03 リリースノート {#v203-release-notes}

*単一の実行ファイルによる配置*

*2018年5月22日リリース*

**バグ修正：**

- エラーメッセージの処理でバッファーオーバーランが起きる可能性を修正しました。 (*報告：Lætitia。*)
- 同期の`archive-get`コマンドでアーカイブの書き込みロックを取得していた問題を修正しました。 (*報告：uspen。*)

**改善：**

- エクスポートするC関数とPerlモジュールを、pgBackRestの実行ファイルに直接組み込みました。
- 移植性を高めるため、`__time_t`の代わりに`time_t`を使用するようにしました。 (*提案：Nick Floersch。*)
- コマンド終了時に、総実行時間をミリ秒単位で表示するようにしました。


### v2.02 リリースノート {#v202-release-notes}

*並列の非同期archive-getと設定ファイルのインクルード*

*2018年5月6日リリース*

**バグ修正：**

- 指定されたディレクトリだけを同期すべき場面で、再帰的にディレクトリを同期していた問題を修正しました。 (*報告：Craig A. James。*)
- incr/diffバックアップで`archive-copy`が"path not found"エラーを発生させる問題を修正しました。 (*報告：yummyliu, Vitaliy Kukharik。*)
- `PGDATA`内の2つ以上のファイルが同じディレクトリへのリンクである場合、マニフェストの作成に失敗する問題を修正しました。 (*報告：Vitaliy Kukharik。*)
- リンク先のファイルがない場合にdeltaリストアが失敗する問題を修正しました。
- ヘルプでのキーと値のペアおよびリスト形式のオプションの表示を修正しました。 (*報告：Clinton Adams。*)

**新機能：**

- 非同期かつ並列の`archive-get`を追加しました。WALセグメントのキューを維持することで、PostgreSQLがrestore_commandでWALセグメントを要求する際の遅延を減らします。
- 追加のpgBackRest設定ファイルをサポートしました。ディレクトリは`--config-include-path`オプションで指定します。`--config`と`--config-include-path`オプションのデフォルトのベースパスを上書きするため、`--config-path`オプションを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 一時認証情報のトークンを設定できるよう、`repo-s3-token`オプションを追加しました。pgBackRestには現時点で新しい認証情報を要求する手段がないため、認証情報の有効期限が切れる前に、コマンド全体（`backup`、`restore`など）が完了する必要があります。 (*貢献：Yogesh Sharma。レビュー：David Steele。*)

**改善：**

- `archive-push-queue-max`、`manifest-save-threshold`、`buffer-size`オプションで、`KB`、`MB`、`GB`、`TB`、`PB`単位の値を指定できるようにしました。倍率には`1024`の累乗を使います。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- バックアップとリストアのパスの同期を効率化しました。小さなテーブルが多数ある場合、ディレクトリ全体の走査には大きなコストがかかります。バックアップとリストアのパスを走査する代わりに、バックアップマニフェストに含まれるパス一覧を使って同期するようにしました。
- 最初のinfoログメッセージに、コマンドオプションだけでなくコマンドパラメーターも表示するようにしました。
- archive-queue-maxオプションをarchive-push-queue-maxに改名しました。新しい`archive-get-queue-max`オプションと一貫した命名になります。古いオプション名も引き続き使用できます。

**ドキュメントの不具合修正：**

- 32ビットのサポートと注意事項をドキュメントに追加しました。32ビットのサポートはv1.26で追加されています。 (*報告：Viorel Tabara。*)

**ドキュメントの改善：**

- PostgreSQLとjqを使った監視の例を追加しました。 (*提案：Stephen Frost, Brian Faherty。*)
- アーカイブ設定にコマンド別セクションの使用例を追加しました。 (*提案：Christophe Courtois。*)
- `info --output=json`を実験的機能とする記述を削除しました。
- `spool-path`オプションの古い説明を更新しました。

**テストスイートの機能：**

- Cのユニットテストのカバレッジ報告にlcovを使用するようにしました。Devel::Coverはgcovから変換したレポートの分岐カバレッジを報告しないため、切り替えました。モジュールの分岐カバレッジが不完全な場合はエラーになります。ユニットテスト自体のカバレッジは、ステートメントまたは分岐のカバレッジが不完全な場合を除き、レポートに表示しません。


### v2.01 リリースノート {#v201-release-notes}

*軽微なバグ修正と改善*

*2018年3月19日リリース*

**バグ修正：**

- `--type=immediate`でのリストア時に、`--target-action`と`--recovery-option`が無効なオプションと報告される問題を修正しました。 (*報告：Brad Nicholson。*)
- 機密オプション（例：`repo1-s3-key`）をコマンドラインで渡した場合、直ちにエラーを出すようにしました。pgBackRestは機密オプションをサブプロセスに渡さないため、以前は分かりにくいエラーが発生していました。新しいエラーははるかに明確で、問題を解決するためのヒントも示します。コマンドラインで指定できない機密オプションは記載しないよう、コマンドのドキュメントも更新しました。 (*報告：Brad Nicholson。*)
- 組み込みPerlに`--no-config`を渡す際の問題を修正しました。 (*報告：Ibrahim Edib Kokdemir。*)
- `log-level-stderr` > `warn`を指定すると、本来出力されないはずのstderrへの出力が検出され、`local`/`remote`プロセスが終了時にエラーになる問題を修正しました。これらのプロセスが警告を出す理由はないため、`local`/`remote`プロセスでの最大値は`error`になりました。 (*報告：Clinton Adams。*)
- テーブルスペースが存在する場合の、`check`コマンドのマニフェストテストを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Thomas Flatley。*)

**改善：**

- 複数の引数を受け付けないオプションに、設定ファイルで複数の引数を設定した場合はエラーを出すようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `src/Makefile`から不要なsudoコマンドを削除しました。 (*貢献：Adrian Vondendriesch。レビュー：David Steele。*)

**ドキュメントの改善：**

- インデックス付きオプション（`repo-*`、`pg-*`）の例に、インデックスを表示するようにしました。 (*提案：Stephen Frost。*)
- コマンドページの目次を、コマンドだけを列挙する簡潔なものにしました。 (*提案：Stephen Frost。*)
- Cライブラリが任意であるという記述を削除しました。

**テストスイートの機能：**

- CentOS/RHELパッケージのビルドを追加しました。
- 静的コード解析にclangを使用するようにしました。初回には、`__noreturn__`を付けるべきだった一部の関数以外に問題は見つかりませんでした。


### v2.00 リリースノート {#v200-release-notes}

*archive-pushの性能改善*

*2018年2月23日リリース*

**新機能：**

- `archive-push`コマンドの一部をCで実装しました。これにより、PostgreSQLの`archive_command`が非同期アーカイブプロセスからの状態メッセージを処理する際、大幅に高速化されます。 (*レビュー：Cynthia Shang。*)

**改善：**

- バックアップマニフェストを作成できることを検証するよう、`check`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- HTTPSクライアントの性能を改善しました。バッファリング時に`select()`だけに依存せず、ソケットの`pending`バイトがあれば考慮するようにしました。場合によっては、接続を閉じるまで最後のバイトがフラッシュされないことがありました。
- S3の削除性能を改善しました。おそらくテスト中に、定数`S3_BATCH_MAX`がハードコードされた値2に置き換えられていました。
- コマンドライン専用ではないすべてのオプションを、コマンドラインでデフォルト値に戻せるようにしました。`pgbackrest.conf`内のオプションをデフォルト値に戻せるため、特定の用途のために新しい設定ファイルを書く必要性が減ります。
- Cライブラリを必須にしました。これにより条件付きの読み込みが不要になり、新しいライブラリ機能を開発しやすくなります。
- `pgbackrest`実行ファイルをPerlからCバイナリーに変更しました。これにより、非同期`archive-push`など、実行時間が重要なコマンドを高速化できます。
- 一貫性を高めるため、`db-*`オプションを`pg-*`に、`backup-*`オプションを`repo-*`に変更しました。`repo-*`オプションにインデックスを付けるようになりましたが、現時点で指定できるのは1つだけです。

**ドキュメントの機能：**

- ドキュメント内のすべてのクラスターを、チェックサムを有効にして初期化するようにしました。

**ドキュメントの改善：**

- ドキュメントとコマンドラインヘルプに、非推奨のオプション名を列挙するようにしました。
- S3バケットはユーザーが作成する必要があることを明記しました。 (*提案：David Youatt。*)


### v1.29リリースノート {#v129-release-notes}

*バックアップの再開に関する重大な不具合修正*

*2018年7月5日リリース*

**重要な注意事項**：このリリースでは、バックアップの再開機能に関する重大な不具合を修正しています。このリリースより前に再開したバックアップは、すべて整合性がないものと見なすことを推奨します。`resume=n`を指定していない限り、前回のバックアップが失敗すると、そのバックアップを再開します。再開したバックアップは、バックアップログにメッセージ"aborted backup of same type exists, will be cleaned to remove invalid files and resumed"があるかどうかで判別できます。このメッセージがある場合、そのバックアップも、同じセット内のほかのバックアップもリストアに使用しないでください。また、リストアログを確認し、再開したバックアップをリストアしていないか調べてください。該当する場合、クラスター内のデータに不整合がある可能性があります。

**バグ修正：**

- 再開時に整合性のないバックアップが作成される重大な不具合を修正しました。`v0.82`でのリグレッションにより、再開時に中断済みバックアップのどのファイルを保持するかを判断する際のタイムスタンプ比較が失われていました。詳細は上記の注意事項を参照してください。 (*報告：David Youatt, Yogesh Sharma, Stephen Frost。*)
- S3認証ヘッダーのタイムスタンプがISO-8601に準拠していなかった問題を修正しました。AWSと一部のゲートウェイは、時のゼロ埋めを空白にしても受け付けていましたが、他のゲートウェイは受け付けていませんでした。 (*修正：Andrew Schwartz。レビュー：David Steele。*)
- 指定されたディレクトリだけを同期すべき場面で、再帰的にディレクトリを同期していた問題を修正しました。 (*報告：Craig A. James。*)
- `--type=immediate`でのリストア時に、`--target-action`と`--recovery-option`が無効なオプションと報告される問題を修正しました。 (*報告：Brad Nicholson。*)
- incr/diffバックアップで`archive-copy`が"path not found"エラーを発生させる問題を修正しました。 (*報告：yummyliu, Vitaliy Kukharik。*)
- `PGDATA`内の2つ以上のファイルが同じディレクトリへのリンクである場合、マニフェストの作成に失敗する問題を修正しました。 (*報告：Vitaliy Kukharik。*)
- リンクされたファイルが存在しない場合、差分リストアが失敗する問題を修正しました。
- クラスター内のユーザーデータベースが1つだけの場合、選択的リストアでエラーになる問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Nj Baliyan。*)

**改善：**

- サーバーが`content-length`を指定しない場合、0に設定するようHTTPクライアントを改善しました。S3とそのゲートウェイは常に`content-length`または`transfer-encoding`を設定しますが、`HTTP 1.1`では必須ではなく、HAProxyなどのプロキシがどちらも含めない場合があります。 (*提案：Adam K. Sumner。*)
- HTTPSクライアントの性能を改善しました。バッファリング時に`select()`だけに依存せず、ソケットの`pending`バイトがあれば考慮するようにしました。場合によっては、接続を閉じるまで最後のバイトがフラッシュされないことがありました。
- S3の削除性能を改善しました。おそらくテスト中に、定数`S3_BATCH_MAX`がハードコードされた値2に置き換えられていました。
- バックアップ／リストア時のパスの同期を効率化しました。小さなテーブルが多い場合、ディレクトリ全体の走査は大きな負荷になります。バックアップマニフェストにはパスの一覧が含まれるため、バックアップ／リストア先のパスを走査せず、その一覧を使って同期します。使われなくなった再帰的なパス同期機能を削除しました。

**ドキュメントの不具合修正：**

- 32ビットのサポートと注意事項をドキュメントに追加しました。32ビットのサポートはv1.26で追加されています。 (*報告：Viorel Tabara。*)

**ドキュメントの改善：**

- S3バケットはユーザーが作成する必要があることを明記しました。 (*提案：David Youatt。*)
- `spool-path`オプションの古い説明を更新しました。


### v1.28リリースノート {#v128-release-notes}

*stanzaの削除*

*2018年2月1日リリース*

**バグ修正：**

- --db-includeを使って、テーブルスペース内の単一データベースをリストアできない問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Chiranjeevi Ravilla。*)
- `archive.info`と`backup.info`を照合するとき、最新の`db-id`を確実に選択するようにしました。これにより、`system-id`と`db-version`が重複している場合（`pg_upgrade`を元に戻した後など）にも正しく照合できます。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Adam K. Sumner。*)
- 無効なコマンドを報告する際のエラーメッセージが冗長すぎる問題を修正しました。 (*報告：Jason O'Donnell。*)

**新機能：**

- 使用していないstanzaを削除する`stanza-delete`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Magnus Hagander。*)

**改善：**

- stanzaがすでに存在していてもエラーにならないよう、`stanza-create`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- `stanza-create --force`のドキュメントを更新し、使用時に注意するよう促しました。 (*提案：Jason O'Donnell。*)


### v1.27リリースノート {#v127-release-notes}

*不具合修正とドキュメント*

*2017年12月19日リリース*

**バグ修正：**

- `backup`と`restore`で実行場所のエラーが抑制されていた問題を修正しました。バックアップホストがある場合、リモートホストを無視する別の設定を用意しない限り、バックアップはバックアップホストでのみ、リストアはデータベースホストでのみ許可する必要があります。 (*報告：Lardière Sébastien。*)
- PostgreSQL 10でWALの期限切れ処理が行われない問題を修正しました。PostgreSQLのすべてのメジャーバージョンがX.X形式であると想定した、誤った正規表現が原因でした。 (*報告：Adam Brusselback。*)
- `--no-config`オプションが子プロセスに渡されない問題を修正しました。子プロセスがローカルの設定ファイルを読み込んでしまい、予期しない動作を引き起こす可能性がありました。
- クラスターの旧バージョンのバックアップもアーカイブも存在しない場合、`"db (prior)"`を出力しないよう`info`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Stephen Frost。*)

**ドキュメントの機能：**

- `archive-copy`と`archive-check`の関係を説明しました。 (*提案：Markus Nullmeier。*)
- `archive-copy`のリファレンスドキュメントを改善しました。


### v1.26リリースノート {#v126-release-notes}

*リポジトリの暗号化*

*2017年11月21日リリース*

**バグ修正：**

- リストア時に、大きなマニフェストのコピーが失敗する場合がある問題を修正しました。 (*報告：Craig A. James。*)
- 32ビットアーキテクチャでWALオフセットが誤っていた問題を修正しました。 (*修正：Javier Wilson。レビュー：David Steele。*)
- 旧バージョンのデータベースのWALを取得する際の問題を修正しました。`stanza-upgrade`の後も、旧バージョンのバックアップをリストアし、`archive-get`でリカバリーできるはずですが、archive-getは最新のdbバージョン／IDしか確認せず、失敗していました。また、同じdbバージョン／IDが履歴に複数回現れる場合の問題も修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Clinton Adams。*)
- バックアップ時の無効なグループを、リストア時に正しく設定できない問題を修正しました。バックアップ時にグループを名前に対応付けられない場合、マニフェストにグループを`false`として保存し、リストア時には$PGDATAの所有者、これが使えなければ現在のユーザーのグループを使ってグループを設定します。この処理が正しく動作せず、選択したグループでユーザーを上書きしていたため、グループが未定義のままになり、ユーザーが誤ってグループに設定されていました。 (*報告：Jeff McCormick。*)
- リモートへのパラメーターの受け渡しを修正しました。複数のdbを指定した場合、実際に対象としているdbにかかわらず、db1のパス、ポート、ソケットパスを渡していました。 (*報告：uspen。*)

**新機能：**

- リポジトリの暗号化をサポートしました。 (*貢献：Cynthia Shang, David Steele。*)

**改善：**

- `--compress-level-network=0`の場合、gzipフィルターを無効にしました。従来は圧縮レベル0でフィルターを使用しており、利点のない負荷が生じていました。
- gzipフィルターの展開性能を改善しました。

**ドキュメントの機能：**

- issueの報告時に最初に収集する情報を充実させるため、テンプレートを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- `archive-timeout`の使い方を明確にし、PostgreSQLのarchive_timeout設定との違いを説明しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Keith Fiske。*)

**テストスイートの機能：**

- 32ビットのi386/i686アーキテクチャ向け自動テストを追加しました。


### v1.25リリースノート {#v125-release-notes}

*S3の性能改善*

*2017年10月24日リリース*

**バグ修正：**

- `compress-level`オプションのカスタム設定が無視される問題を修正しました。 (*報告：Jens Wilke。*)
- タイムラインの重複を検出した場合のエラーを削除しました。タイムラインの重複は、多くのポイントインタイムリカバリー（PITR）で有効な状態です。 (*報告：blogh。*)
- JSON形式のinfo出力で、`database-id`が整数として出力されない場合がある問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Jason O'Donnell。*)

**新機能：**

- S3での一覧取得リクエストの性能を改善しました。フィルター式の先頭にリテラル部分がある場合、そこから検索用プレフィックスを生成します。これにより、レート制限を回避できる程度にリクエストを小さく抑えられることが多くなります。 (*提案：Mihail Shvein。*)

**テストスイートの機能：**

- I/O性能テストを追加しました。


### v1.24リリースノート {#v124-release-notes}

*バックアップから除外する項目の追加*

*2017年9月28日リリース*

**バグ修正：**

- スタンバイからのバックアップの初期化中に、低い優先度のログメッセージではなく警告が出力される問題を修正しました。 (*報告：uspen。*)
- 一部の`db-*`オプション（`db-port`など）がリモートに渡されない問題を修正しました。 (*報告：uspen。*)

**新機能：**

- 起動時に再構築されるため、`pg_snapshots`、`pg_serial`、`pg_notify`、`pg_dynshmem`の内容をバックアップから除外しました。
- 起動時に再構築されるため、`pg_internal.init`ファイルをバックアップから除外しました。

**改善：**

- メインプロセスも同じファイルにログを書き込むことを防ぐため、非同期プロセスがメインプロセスから完全に分離された後にログファイルを開くようにしました。 (*提案：Jens Wilke。*)

**ドキュメントの機能：**

- パスワード不要のSSH設定を追加しました。

**ドキュメントの改善：**

- PostgreSQLの慣例に合わせ、ドキュメント内のmasterをprimaryに変更しました。


### v1.23リリースノート {#v123-release-notes}

*複数のスタンバイとPostgreSQL 10のサポート*

*2017年9月3日リリース*

**バグ修正：**

- サイズが増加中のファイルで、圧縮が中止される場合がある問題を修正しました。 (*報告：Jesper St John, Aleksandr Rogozin。*)
- ローカルプロセスからリモートにキープアライブが送信されない問題を修正しました。 (*報告：William Cox。*)

**新機能：**

- スタンバイからのバックアップ用に、最大7つのスタンバイを設定できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL 10をサポートしました。
- サードパーティーのS3ゲートウェイとの互換性を高めるため、XMLデータの読み取り時にチャンク転送に加えて`content-length`も使えるようにしました。 (*提案：Victor Gdalevich。*)

**改善：**

- S3向けのHTTPタイムアウトを延長しました。
- 一時的なS3ネットワークエラーへの耐性を高めるため、HTTPの再試行を追加しました。

**ドキュメントの不具合修正：**

- 設定ページに各セクションの概要が含まれるよう、ドキュメント生成を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)


### v1.22リリースノート {#v122-release-notes}

*S3の再試行の修正*

*2017年8月9日リリース*

**バグ修正：**

- S3の再試行時の認証問題を修正しました。


### v1.21リリースノート {#v121-release-notes}

*info出力の改善とSSHポートオプション*

*2017年8月8日リリース*

**バグ修正：**

- 新しいバージョンのように`archive_status`ディレクトリを自動再作成しないPostgreSQL 8.3に対応するため、リストア時にこのディレクトリを再作成するようにしました。 (*報告：Stephen Frost。*)
- `stanza-upgrade`後に、旧バージョンのPostgreSQLの空のアーカイブディレクトリが残る場合がある問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- `info`コマンドのテキスト出力とJSON出力を変更しました。現在のデータベースクラスターのバージョンと、存在する場合は以前のバージョンについて、アーカイブID、および現在アーカイブに存在する最小／最大のWALを表示します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- デフォルト以外のSSHポートをサポートするため、`--backup-ssh-port`と`--db-ssh-port`を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- S3が内部エラー（500）を返した場合に再試行するようにしました。

**ドキュメントの不具合修正：**

- コマンドの文脈に応じて、`--online`の説明を修正しました。

**ドキュメントの機能：**

- 手動インストールの手順に、`/etc/pgbackrest.conf`の作成を追加しました。

**ドキュメントの改善：**

- コマンドリファレンスとコマンドラインヘルプで、リポジトリのオプションを独立したセクションに移しました。 (*提案：Stephen Frost。*)


### v1.20リリースノート {#v120-release-notes}

*8.3/8.4の重大な不具合修正*

*2017年6月27日リリース*

**重要な注意事項**：PostgreSQL 8.3および8.4でテーブルスペースを利用している環境では、どのv1リリースからでも直ちにアップグレードし、フルバックアップを実行することを推奨します。これらのバージョンに限り、不具合によってテーブルスペースがバックアップされていませんでした。PostgreSQL ≥ 9.0 はこの問題の影響を受けません。

**バグ修正：**

- PostgreSQL ≤ 8.4でテーブルスペースがバックアップされない問題を修正しました。
- Cライブラリのビルドでフラグが欠けていたため、32ビットシステムで不適合なバイナリーが生成される問題を修正しました。 (*報告：Adrian Vondendriesch。*)

**新機能：**

- `IO::Socket::SSL`がCAを自動検出できないシステム（RHEL7など）に対応し、またカスタムCAを読み込めるよう、`s3-repo-ca-path`と`s3-repo-ca-file`を追加しました。 (*提案：Scott Frazer。*)

**テストスイートの機能：**

- CIにドキュメントのビルドを追加しました。


### v1.19リリースノート {#v119-release-notes}

*S3のサポート*

*2017年6月12日リリース*

**バグ修正：**

- 現在のデータベースバージョンのWALアーカイブの最小／最大を表示するよう、`info`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- スタンバイが未設定、または接続できない場合、`backup-standby`オプションをリセットし、プライマリーでバックアップを続行するよう`backup`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- リモートプロセスが出す設定警告によって、マスタープロセスでエラーが発生する問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- Amazon S3リポジトリをサポートしました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの不具合修正：**

- 設定リファレンスに記載されていた無効な`max-archive-mb`オプションを、`archive-queue-max`に変更しました。
- インストールのセクションで欠けていた`sudo`を追加しました。 (*修正：Lætitia。レビュー：David Steele。*)


### v1.18リリースノート {#v118-release-notes}

*stanzaのアップグレード、リファクタリング、ロックの改善*

*2017年4月12日リリース*

**バグ修正：**

- ローカルのワーカープロセスを使う読み取り専用操作（`restore`など）が書き込みロックを取得し、並列`archive-push`を妨げる場合がある問題を修正しました。 (*報告：Jens Wilke。*)

**新機能：**

- PostgreSQLを新しいメジャーバージョンにアップグレードした後にstanzaを更新できる、stanza-upgradeコマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `pgbackrest.conf`を検証し、オプションが無効な場合や正しいセクションにない場合に警告を表示するようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- ロックの仕組みを簡素化しました。以前のようにすべてのローカルおよびリモートのワーカープロセスが書き込みロックを取得するのではなく、マスタープロセスのみが`archive-push`と`backup`の書き込みロックを保持するようになりました。
- バックアップディレクトリ内のファイルのタイムスタンプを、クラスター内のファイルに合わせて設定しなくなりました。元はバックアップの再開のために必要でしたが、現在の再開処理はチェックサムを使って実装されています。
- `restore`コマンドが`postmaster.pid`の存在を検出した場合のエラーメッセージを改善しました。 (*提案：Yogesh Sharma。*)
- PostgreSQLが一部の戻りコードを致命的なシグナル例外と解釈しないよう、戻りコードを25から125の範囲に振り直しました。 (*提案：Yogesh Sharma。*)


### v1.17リリースノート {#v117-release-notes}

*ページチェックサムの不具合修正*

*2017年3月13日リリース*

**バグ修正：**

- 初期化されたばかりで未使用のページが、ページチェックサムの警告を発生させる問題を修正しました。 (*報告：Stephen Frost。*)


### v1.16リリースノート {#v116-release-notes}

*ページチェックサムの改善、CI、パッケージのテスト*

*2017年3月2日リリース*

**バグ修正：**

- 1GBを超えるテーブルで、最初のセグメントより後にページチェックサムの警告が出る問題を修正しました。 (*報告：Stephen Frost。*)
- デフォルト以外のテーブルスペースに作成したデータベースで、`pg_filenode.map`と`pg_internal.init`がページ境界に整列していないという誤った警告が出る問題を修正しました。 (*報告：blogh。*)

**テストスイートの機能：**

- `travis-ci`を使った継続的インテグレーションを導入しました。
- サポート対象のすべてのディストリビューション向けに、Debianパッケージを自動ビルドするようにしました。


### v1.15リリースノート {#v115-release-notes}

*リファクタリングと不具合修正*

*2017年2月13日リリース*

**バグ修正：**

- マニフェスト作成中にファイルが削除されると（テーブルを削除した場合など）、バックアップが失敗する場合がある、v1.13で導入されたリグレッションを修正しました。 (*報告：Navid Golpayegani。*)


### v1.14リリースノート {#v114-release-notes}

*リファクタリングと不具合修正*

*2017年2月13日リリース*

**バグ修正：**

- archive-pushでエラーが発生しても再試行せず、`.error`ファイルを手動削除しない限り、PostgreSQLにエラーを返し続ける問題を修正しました。 (*報告：Jens Wilke。*)
- 並列アーカイブで複数のプロセスが同時に新しいパスを作成しようとするとエラーになる競合状態を修正しました。 (*報告：Jens Wilke。*)

**改善：**

- `info`コマンドが提供する`wal archive min/max`の性能を改善しました。 (*提案：Jens Wilke。*)

**ドキュメントの機能：**

- 非同期アーカイブのドキュメントを更新し、新しい方式の動作と旧方式との違いをより正確に説明しました。 (*提案：Jens Wilke。*)


### v1.13リリースノート {#v113-release-notes}

*並列アーカイブ、stanzaの作成、infoとcheckの改善*

*2017年2月5日リリース*

**重要な注意事項**：非同期アーカイブの新しい実装では、WALを別のキューにコピーしなくなりました。`1.13`へのアップグレード後に古いキューに残ったWALは処理されずに残り、リポジトリに送信**されません**。これを防ぐには、`archive_command = false`を設定してアーカイブを停止してください。次に`pgbackrest --stanza=[stanza-name] archive-push`を実行して非同期キューを空にし、処理の完了を待ちます。`[spool-path]/archive/[stanza-name]/out`のキューが空であることを確認してください。最後に`1.13`をインストールし、元の`archive_command`を復元します。**重要な注意事項**：`stanza-create`コマンドは任意ではなくなりました。**新しい**stanzaでバックアップまたはアーカイブを行う前に、必ず実行する必要があります。既存のstanzaで`stanza-create`を実行する必要はありません。

**バグ修正：**

- Cライブラリでコンパイラー警告を発生させていたconstへの代入を修正しました。 (*修正：Adrian Vondendriesch。レビュー：David Steele。*)
- `--repo-sync`オプションの対象から漏れていた、いくつかのディレクトリ同期を修正しました。
- リストア時にユーザー／グループが存在しない場合、`File->owner()`で"uninitialized value"エラーになる場合がある問題を修正しました。 (*報告：Leonardo GG Avellar。*)
- プロトコルの不一致エラーで、期待する値が出力されない問題を修正しました。
- 終了コード1を異常終了とする、`archive-get`の誤ったログメッセージを修正しました。

**新機能：**

- 非同期アーカイブを、改善されたマルチプロセス実装に変更しました。
- 多くの場合に壊れたリポジトリを修復でき、必須として使えるだけの堅牢性を持つよう、`stanza-create`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- スタンバイで実行できるよう`check`コマンドを改善しました。ただし、レプリカでは`pg_switch_xlog()`を実行できないため、基本的なチェックのみを行います。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `info`コマンドに、アーカイブとバックアップのWAL範囲を追加しました。
- PostgreSQL < 9.2でテーブルスペースを再マッピングする際、`pg_tablespace.spclocation`の更新を促す警告を追加しました。 (*貢献：blogh。レビュー：David Steele。*)
- 読み取り専用の操作である`archive-get`、`restore`、`info`、`check`について、リモートでのロックを不要にしました。 (*提案：Michael Vitale。*)

**改善：**

- 最初のログエントリが書き込まれるまで、ログファイルのバナーを出力しないようにしました。 (*提案：Jens Wilke。*)
- バックアップ開始LSNでフィルターすることで、不完全な書き込みのページがページチェックサムで誤検出される可能性を減らしました。
- Cライブラリのビルドフラグから、Intel固有の最適化を削除しました。 (*貢献：Adrian Vondendriesch。レビュー：David Steele。*)
- `--lock`オプションを削除しました。このオプションはロックディレクトリをリポジトリ外に配置できるようになる前に導入されたもので、現在は不要です。
- ログのタイムスタンプを非表示にできる`--log-timestamp`オプションを追加しました。主に、自動生成するドキュメントでフィルターを使わずに済むようにするためのものです。
- 相対パスを絶対パスに変換できない場合、適切なエラーコードを返すようにしました。 (*提案：Yogesh Sharma。*)

**ドキュメントの機能：**

- ユーザーガイドに`process-max`オプションの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.12リリースノート {#v112-release-notes}

*ページチェックサム、設定、不具合修正*

*2016年12月12日リリース*

**重要な注意事項**：以前のリリースでは、現在のコマンドに対して無効なオプションをコマンドラインで指定しても、エラーになりませんでした。今後は無効なオプションでエラーが発生するため、運用に支障が出ないよう、環境内のコマンドラインオプションを入念に確認することが重要です。

**バグ修正：**

- 指定したコマンドに対して無効なオプションをコマンドラインで指定しても、エラーにならない問題を修正しました。従来はそのオプションを無視し、動作に変化はありませんでしたが、混乱の原因になっていました。今後は無効なオプションでエラーが発生します。 (*報告：Nikhilchandra Kulkarni。*)
- リポジトリ内のテーブルスペース用の内部シンボリックリンクが作成されない問題を修正しました。この問題が表面化するのは、ファイルシステムのスナップショットを使って、その場でクラスターを手動起動しようとした場合のみです。通常のバックアップとリストアには影響しませんでした。
- ログシステムを初期化する前、つまりオプションの解析中に、エラーをコンソールへ出力できない問題を修正しました。エラーコードは正しく返されていたため、実際には失敗した処理が成功したように見えることはありませんでした。 (*報告：Adrian Vondendriesch。*)
- バックアップサーバーで指定した`db-port`が、最初に設定したデータベースのものでない限り、リモートに正しく渡されない問題を修正しました。 (*報告：Michael Vitale。*)

**新機能：**

- PostgreSQL >= 9.3でチェックサムが有効な場合、データファイルのページチェックサムをpgBackRestで検証できる`--checksum-page`オプションを追加しました。この機能にはCライブラリが必要ですが、当初はOSパッケージで提供されていない場合があります。ライブラリが存在し、クラスターでチェックサムが有効になっている場合、このオプションを自動的に有効にします。 (*提案：Stephen Frost。*)
- シンボリックリンクをサポートしないファイルシステムにリポジトリを置く場合、内部シンボリックリンクを作成しないようにできる`--repo-link`オプションを追加しました。pgBackRestの機能には影響しませんが、利便性のための`latest`リンクと、テーブルスペースの内部シンボリックリンクは作成されません。そのため、ファイルシステムのスナップショットを使い、その場でクラスターを手動起動する際に影響します。
- NTFSなど、ディレクトリ同期をサポートしないファイルシステム向けに、リポジトリ内のディレクトリ同期を無効にできる`--repo-sync`オプションを追加しました。
- コマンドの正常完了を示す、予測可能なログエントリを追加しました。たとえばバックアップが正常に終了すると、`INFO: backup command end: completed successfully`が出力されます。 (*提案：Jens Wilke。*)

**改善：**

- 単純化のため、`pg_control`は処理の最後に単独でコピーするのではなく、他のファイルと一緒にコピーするようにしました。`backup`コマンドには従来の動作は不要であり、`restore`は一時ファイルにコピーしたうえで、リストアの最後に名前を変更します。

**ドキュメントの不具合修正：**

- PDFのビルドで例外が抑制される問題を修正しました。
- v1.10で導入された、セクションリンクのリグレッションを修正しました。

**ドキュメントの機能：**

- クイックスタートに保持の説明を追加しました。


### v1.11リリースノート {#v111-release-notes}

*非同期アーカイブの効率に関する不具合修正*

*2016年11月17日リリース*

**バグ修正：**

- 非同期アーカイブがファイルをまとめて転送せず、1回の実行で1ファイルしか転送しない問題を修正しました。このリグレッションはv1.09で導入され、効率にのみ影響していました。非同期モードでも、すべてのWALセグメントは正しくアーカイブされていました。 (*報告：Stephen Frost。*)


### v1.10リリースノート {#v110-release-notes}

*stanzaの作成と軽微な不具合修正*

*2016年11月8日リリース*

**バグ修正：**

- バックアップ間でデータベースに変更がなく、`pg_control`だけが変化した場合、バックアップがエラーになる場合がある問題を修正しました。
- 同じプレフィックスを持つテーブルスペースパスで、無効なリンクのエラーが発生する問題を修正しました。 (*報告：Nikhilchandra Kulkarni。*)

**新機能：**

- リポジトリでのstanzaの作成を正式な操作にするため、`stanza-create`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- Perlモジュールから余分な`use lib`ディレクティブを削除しました。 (*提案：Devrim Gündüz。*)


### v1.09リリースノート {#v109-release-notes}

*9.6のサポート、設定の柔軟性、不具合修正*

*2016年10月10日リリース*

**バグ修正：**

- バックアップディレクトリが存在しない場合にエラーメッセージを記録しないよう、`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- 無効なarchiveコマンドを検出した場合、そのコマンドを正しく表示するようエラーメッセージを修正しました。 (*報告：Jason O'Donnell。*)
- `archive-push`が新しいWALセグメントをキューに入れるための空き容量を確保できないと、非同期アーカイバーが起動されない問題を修正しました。このため、`archive-push`を直接呼ぶなどの手動操作なしでは、キューが空になりませんでした。今後は、新しいWALセグメントを保存する空き容量がない場合、PostgreSQLにエラーを返しますが、非同期プロセスは起動し、最終的に空き容量を確保できるようにします。 (*報告：Jens Wilke。*)
- ローカルプロセスが再開またはリストア中にチェックサムを計算するものの、ファイルをコピーせず、リモートがアイドル状態になると発生するタイムアウトを修正しました。 (*報告：Jens Wilke。*)

**新機能：**

- PostgreSQL 9.6では、非排他的バックアップを自動的に使用するようにしました。
- sshクライアントを指定できる`cmd-ssh`オプションを追加しました。 (*提案：Jens Wilke。*)
- コンソールログの送信先を`stderr`または`stdout`に制御する`log-level-stderr`オプションを追加しました。デフォルトは`warn`です。こちらのほうが直感的かもしれませんが、以前のバージョンとは動作が変わります。`log-level-stderr=off`を設定すると、以前の動作を維持できます。 (*提案：Sascha Biberhofer。*)
- データベース接続の`application_name`を`"pgBackRest [command]"`に設定するようにしました。 (*提案：Jens Wilke。*)
- `archive-check`オプションが有効な場合、archive_modeが有効であることを確認するようにしました。

**改善：**

- pgBackRestのアドバイザリーロックを取得できない場合のエラーメッセージを明確にし、PostgreSQLのバックアップロックではないことがわかるようにしました。 (*提案：Jens Wilke。*)
- コマンド開始時のINFOログにpgBackRestのバージョン番号を含めるようにしました。
- ローカルプロセスの開始／停止時のINFOログにプロセスIDを記録するようにしました。

**ドキュメントの機能：**

- ユーザーガイドに`archive-timeout`オプションの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.08リリースノート {#v108-release-notes}

*不具合修正とログの改善*

*2016年9月14日リリース*

**バグ修正：**

- ローカルプロセスが完了時に切断せず、後でタイムアウトする場合がある問題を修正しました。 (*報告：Todd Vernick。*)
- WALセグメントがアーカイブに届くのを待っている間に、プロトコル層がタイムアウトする場合がある問題を修正しました。 (*報告：Todd Vernick。*)

**改善：**

- より完全なログを残せるよう、ファイルが作成されるまでファイル向けのログ出力をキャッシュするようにしました。


### v1.07リリースノート {#v107-release-notes}

*スレッドからプロセスへの移行と不具合修正*

*2016年9月7日リリース*

**バグ修正：**

- スタンバイからのバックアップ中に、テーブルスペースをプライマリーからコピーしていた問題を修正しました。
- ローカルだけでなくリモートでもバックアップ情報を確認するよう、`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- `retention-archive-type=diff`の際に`retention-archive`が自動設定されず、アーカイブの期限切れ処理が意図したほど進まない問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- 互換性と性能を高めるため、Perlのスレッドをプロセスに置き換えました。
- プライマリーのレプリケーションスロットがバックアップに含まれないよう、`$PGDATA/pg_replslot`ディレクトリの内容を除外しました。
- `archive-check=n`の場合でも、`backup.manifest`に`archive-start`と`archive-stop`を記録するようにしました。 (*提案：Jens Wilke。*)
- アーカイブの保持設定が意図した効果をもたらさない場合や、無期限の保持を許す場合に警告を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL 9.6 rc1の非排他的バックアップを試験的にサポートしました。以降のリリース候補でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**ドキュメントの不具合修正：**

- バイナリーのパスに関連する、ドキュメントの再現性に関する軽微な問題を修正しました。

**ドキュメントの機能：**

- アーカイブの保持について説明しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.06リリースノート {#v106-release-notes}

*スタンバイからのバックアップと不具合修正*

*2016年8月25日リリース*

**バグ修正：**

- 別のリンクを参照するテーブルスペースのリンクで、エラーを出さずにテーブルスペース全体をスキップしていた問題を修正しました。 (*報告：Michael Vitale。*)
- 複数の値を許可すべきでないオプションを`pgbackrest.conf`で複数回指定しても、エラーにならない問題を修正しました。 (*報告：Michael Vitale。*)
- `db-timeout`を増やしたときに、`protocol-timeout`が自動的に増えない問題を修正しました。 (*報告：Todd Vernick。*)

**新機能：**

- スタンバイクラスターからのバックアップをサポートしました。バックアップの開始／停止や、レプリケーションされないファイルのコピーには、引き続きプライマリーへの接続が必要です。ただし、ファイルの大半をスタンバイからコピーすることで、プライマリーの負荷を減らします。
- データベースの設定をより柔軟にしました。バックアップサーバーにマスターとスタンバイの両方を設定でき、pgBackRestがどちらがプライマリーかを自動判定します。このため、独立したバックアップサーバーを使う場合、プライマリーからスタンバイへフェイルオーバーしても、バックアップの設定を変更する必要がありません。
- PostgreSQLが起動時に消去、再作成、またはゼロ初期化するディレクトリをバックアップから除外しました。`pgsql_tmp`と`pg_stat_tmp`が該当します。また、従来から除外していた`backup_label.old`、`postmaster.opts`、`postmaster.pid`、`recovery.conf`、`recovery.done`に加え、`postgresql.auto.conf.tmp`ファイルも除外しました。
- PostgreSQL 9.6 beta4の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- マニフェストの作成時に、リンクを参照するリンクに対するエラーメッセージを改善しました。
- `archive-push`または`archive-get`で相対パスを検出した場合のエラーメッセージに、ヒントを追加しました。
- ファイルのコピー元ホストがわかるよう、バックアップのログメッセージを改善しました。


### v1.05リリースノート {#v105-release-notes}

*テーブルスペースリンクのチェックに関する不具合修正*

*2016年8月9日リリース*

**バグ修正：**

- パスの一部に$PGDATAを含むテーブルスペースが、実際にはそうでなくても$PGDATAのサブディレクトリと判定される問題を修正しました。相対パスのチェックも少し強化しました。 (*報告：Chris Fort。*)

**ドキュメントの機能：**

- cronによるバックアップのスケジュール設定について説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- バックログをpgBackRestのウェブサイトからGitHubリポジトリのwikiに移しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.04リリースノート {#v104-release-notes}

*各種不具合修正*

*2016年7月30日リリース*

**バグ修正：**

- 余分なリモートプロセスが作成され、マルチスレッドのバックアップ／リストアがタイムアウトしたり、ロック競合を発生させたりする場合がある問題を修正しました。 (*報告：Michael Vitale。*)
- `check`コマンドでdb-pathが必須になっておらず、未指定の場合にわかりやすいエラーメッセージではなくアサーションが発生していた問題を修正しました。 (*報告：Michael Vitale。*)
- データベースのバージョン／IDがアーカイブのものと一致しない場合、エラーになるよう`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- データベースサーバーの`pgbackrest.conf`に`backup-host`オプションがない場合、リモートがさらに自身のリモートを開始しようとする問題を修正しました。 (*報告：Lardière Sébastien。*)
- `pg_xlog`がシンボリックリンクの場合、その内容までバックアップする問題を修正しました。リストア時に問題は起きませんでしたが、容量を無駄にしていました。
- ロック処理内の無効な`log()`呼び出しを修正しました。

**新機能：**

- PostgreSQL 9.6 beta3の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- SSHプロトコル接続でバナーを非表示にしました。
- エラーが発生したホストを識別できるよう、リモートのエラーメッセージを改善しました。
- すべての種類のリモートがロックを取得するようにしました。従来の例外はテストハーネスとpgBackRestが同じVMで動作していた時代のもので、今は該当しません。

**ドキュメントの機能：**

- `backrest-user`オプションのデフォルトが`backrest`である理由を補足しました。 (*提案：Michael Vitale。*)
- サポート対象プラットフォームでのパッケージの提供状況を更新しました。 (*提案：Michael Vitale。*)


### v1.03リリースノート {#v103-release-notes}

*checkコマンドと不具合修正*

*2016年7月2日リリース*

**バグ修正：**

- マルチスレッドの`backup`で多数の小さなファイルを処理すると、`keep-alives`の送信が滞る問題を修正しました。また、シングル／マルチスレッドの`backup`再開時と、`restore`のチェックサム計算時には、キープアライブがまったく送られていませんでした。 (*報告：Janice Parkinson, Chris Barber。*)
- `db-host`オプションを設定した場合、コマンドラインから明示的に呼び出した`expire`が実行を拒否する問題を修正しました。`backup`の後に自動実行する`expire`では、問題はありませんでした (*報告：Chris Barber。*)
- `archive-check`が無効でもarchive_commandを検証していた問題を修正しました。

**新機能：**

- アーカイブとバックアップに向けてpgBackRestが正しく設定されているか検証する`check`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `protocol-timeout`オプションを追加しました。従来の`protocol-timeout`は、`db-timeout`に30秒を加えた値でした。
- バックアップ終了時にリモートの停止に失敗しても、例外を発生させなくなりました。代わりに、`protocol-timeout`を増やすことを推奨する警告を出します。
- PostgreSQL 9.6 beta2の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- バックアップ時に記録したユーザー／グループがリストア先ホストに存在しない場合の処理を改善しました。ユーザー／グループを名前に対応付けられない場合も、明示的に処理するようにしました。
- オプションの処理を大幅に厳格化しました。従来はコマンドに明示的に割り当てられていないオプションでも使用できる場合がありました。特に、実行場所を決める`backup-host`と`db-host`で顕著でした。

**ドキュメントの改善：**

- 再現可能なビルドを生成するため、ドキュメントで固定の日付を使用できるようにしました。 (*提案：Adrian Vondendriesch。*)
- ユーザーガイドに非同期アーカイブの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 新しいPerlでは`/usr/lib/perl5`が検索パスから削除されているため、pgBackRestモジュールの推奨インストール先を`/usr/share/perl5`に変更しました。
- 旧バージョンのpgBackRestを削除する手順を追加しました。


### v1.02リリースノート {#v102-release-notes}

*Perl 5.22の不具合修正*

*2016年6月2日リリース*

**バグ修正：**

- Perl 5.22の新しい制約に合わせて、sprintf()の使い方を修正しました。書式文字列から参照されないパラメーターは、許可されなくなりました。 (*修正：Adrian Vondendriesch。レビュー：David Steele。*)

**ドキュメントの不具合修正：**

- Perl 5.2Xと互換性のない構文を修正しました。 (*修正：Christoph Berg, Adrian Vondendriesch。レビュー：David Steele。*)
- PDFのロゴに使用していた絶対パスを修正しました。 (*報告：Adrian Vondendriesch。*)

**ドキュメントの機能：**

- 不具合、機能、リファクタリングを明確に区別できるよう、リリースノートをセクションに分けました。コアのコードに影響しないドキュメントとテストスイートの変更には、「補足事項」セクションを追加しました。
- manページの生成を追加しました。 (*貢献：Adrian Vondendriesch, David Steele。*)
- 変更履歴は、Markdownのみで出力される最後のドキュメントでした。標準のレンダラーで出力できるよう、変換処理を作成しました。変更履歴はウェブサイトに掲載し、名前を「リリース」に変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.01リリースノート {#v101-release-notes}

*infoの拡充、選択的リストア、9.6のサポート*

*2016年5月17日リリース*

**新機能：**

- `info`コマンドのテキスト出力を拡充し、すべてのバックアップについて、タイムスタンプ、サイズ、参照一覧を含めるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- クラスターのバックアップからデータベースを選んでリストアできるようにしました。特定のデータベースだけをリストアする場合、容量と時間を大幅に削減できます。リストアしなかったデータベースにはアクセスできませんが、共有カタログから除去するには手動で削除する必要があります。 (*レビュー：Cynthia Shang, Greg Smith, Stephen Frost。提案：Stephen Frost。*)
- PostgreSQL 9.6 beta1の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。 (*レビュー：Cynthia Shang。*)


### v1.00リリースノート {#v100-release-notes}

*新しいリポジトリ形式と設定方式、リンクのサポート*

*2016年4月14日リリース*

**重要な注意事項**：この一斉移行が必要なリリースでは、旧バージョンのpgBackRestとの互換性が失われます。マニフェスト形式、ディスク上の構造、設定方式、実行ファイル名とパス名がすべて変更されています。このバージョンのpgBackRestのバックアップを保存するには新しいリポジトリを作成し、リストアが必要になる場合に備えて旧リポジトリをしばらく保持する必要があります。旧リポジトリからのリストアには旧バージョンのpgBackRestが必要ですが、名称が変更されたため、`1.00`と旧バージョンのpgBackRestを同時にインストールできます。変更点の詳細は以下の説明を参照してください。

**新機能：**

- より簡単に使える新しい設定方式を実装しました。詳細はユーザーガイドと設定リファレンスを参照してください。単純な構成では、すべてのオプションを`stanza`セクションに記述できるようになりました。stanza間で共有するオプションは`[global]`セクションに記述できます。より複雑な構成では引き続きコマンド別セクションを使用できますが、必要になるケースはまれなはずです。 (*提案：Michael Renner。*)
- `repo-path`オプションは、ローカルかリモートかにかかわらず、バックアップとアーカイブを保存するリポジトリを常に指すようになりました。このため、`repo-remote-path`オプションを削除しました。非同期アーカイブ時にWALセグメントをキューに入れる場所は、新しい`spool-path`オプションで指定できます。ローカルリポジトリは不要になりました。
- デフォルトの設定ファイル名を`pg_backrest.conf`から`pgbackrest.conf`に変更しました。他の名称変更と一貫させるとともに、`1.00`への移行時に古い設定ファイルを誤って読み込むことを防ぐためです。 (*提案：Michael Renner, Stephen Frost。*)
- デフォルトのリポジトリ名を`/var/lib/backup`から`/var/lib/pgbackrest`に変更しました。 (*提案：Michael Renner, Stephen Frost。*)
- ロックファイルはデフォルトで`/tmp/pgbackrest`に保存するようになりました。現在では`/run/pgbackrest`の使用が推奨されますが、この場所を使うには、本リリースに含まれない初期化スクリプトが必要です。ロックディレクトリは`lock-path`オプションで設定できます。
- ログファイルはデフォルトで`/var/log/pgbackrest`に保存するようになりました。`logrotate`で管理できるよう、日付は付加しなくなりました。ログディレクトリは`log-path`オプションで設定できます。 (*提案：Stephen Frost。*)
- 実行ファイル名を`pg_backrest`から`pgbackrest`に変更しました。 (*提案：Michael Renner, Stephen Frost。*)
- PGDATAからリンクされるすべてのファイルとディレクトリをバックアップに含めるようになりました。デフォルトでは、リンク先をファイルまたはディレクトリとしてPGDATA内に直接リストアします。`--link-all`オプションを使うと、すべてのリンクを元の場所にリストアできます。`--link-map`オプションを使うと、リンク先を新しい場所へ変更できます。
- `--tablespace`オプションを削除し、機能をより明確に示す`--tablespace-map-all`オプションに置き換えました。
- `info`より多くの情報を出力し、`debug`ほど詳細ではない`detail`ログレベルを追加しました。


--------

## 安定版以前のリリース {#pre-stable-releases}


### v0.92リリースノート {#v092-release-notes}

*コマンドラインのリポジトリパスの修正*

*2016年4月6日リリース*

**バグ修正：**

- マスタープロセスがリモートに`--repo-path`ではなく`--repo-remote-path`を渡し、デフォルトのリポジトリディレクトリ（`/var/lib/backup`）にロックファイルが作成されて、通常は失敗に終わる問題を修正しました。この問題は、`--repo-remote-path`を`pg_backrest.conf`ではなくコマンドラインで指定した場合にのみ発生していました。 (*報告：Jan Wieck。*)


### v0.91リリースノート {#v091-release-notes}

*テーブルスペースの不具合修正と軽微な機能拡張*

*2016年3月22日リリース*

**テーブルスペースに関する重要な不具合修正**：0.90でリポジトリ形式を意図せず変更したため、テーブルスペースを含むバックアップは、ディスク上で有効なPostgreSQLクラスターではなくなっていました。影響を受けるのは、restoreコマンドを使用せず、バックアップを直接コピーしてPostgreSQLクラスターをリストアするユーザーのみでした。ただし、この修正により、リストア方法を問わず、テーブルスペースを含む古いバックアップとの互換性が失われます（pgBackRestはエラーを発生させ、リストアを拒否します）。テーブルスペースを含むクラスターでは、バージョン0.91をインストールした直後に新しいフルバックアップを取得することを推奨します。古いバックアップをリストアする必要がある場合は、そのバックアップのバージョンと一致するpgBackRestを使用してください。

**バグ修正：**

- pgBackRest 0.90で導入されたリポジトリの互換性の問題を修正しました。 (*報告：Evan Benoit。*)

**新機能：**

- バックアップ時に`global/pg_control`を最後にコピーするようにしました。
- `.info`ファイルと`.manifest`ファイルを一時ファイルに書き込んでから、最終的な場所へ移動し、fsyncするようにしました。
- `--no-start-stop`オプションの名前を`--no-online`に変更しました。

**テストスイートの機能：**

- Perl-Criticによるソースの静的解析を導入しました。現在はgentleレベルで合格しています。


### v0.90リリースノート {#v090-release-notes}

*9.5のサポート、各種機能拡張、軽微な不具合修正*

*2016年2月7日リリース*

**バグ修正：**

- `--no-archive-check`を指定すると設定エラーが発生する問題を修正しました。 (*報告：Jason O'Donnell。*)
- 特定のタイミングでシステムがクラッシュして一時WALファイルが残ると、次の`archive-push`が失敗する場合がある問題を修正しました。
- `archive-copy=n`を併せて指定しなくても、`retention-archive`をバックアップの保持数（`retention-full`または`retention-diff`）より小さく安全に設定できるようになりました。アーカイブの保持対象外となるバックアップの整合性を確保するために必要なWALは、アーカイブに保持します。ただし、この場合、アーカイブの保持対象外となるバックアップではPITRはできません。

**新機能：**

- テーブルスペースのバックアップとリストアでは、実行対象のPostgreSQLバージョン用に作成されたサブディレクトリのみを操作するようにしました。テーブルスペースには、特にバイナリーアップグレード時などに複数のバージョンが共存できるため、これによりバックアップ時の余分なファイルのコピーや、リストア時の他のバージョンの消去を防ぎます。これはPostgreSQL >= 9.0にのみ適用されます。それ以前のPostgreSQLはテーブルスペースのディレクトリを共有できませんでした。
- `archive-check=y`であるにもかかわらず、`archive_command`が`pg_backrest`を実行しない場合にエラーを発生させるようにしました。 (*貢献：Jason O'Donnell。レビュー：David Steele。*)
- `repo-path`または`repo-remote-path`が存在しない場合のエラーメッセージを改善しました。
- `--delta`および`--force`リストアオプションに、宛先が有効な$PGDATAディレクトリであることを確認するチェックを追加しました。pgBackRestは`PG_VERSION`または`backup.manifest`（中断したリストアで残るファイル）の存在を確認します。どちらもない場合は`--delta`と`--force`を無効にしますが、リストア自体は続行します。ただし、$PGDATAディレクトリまたはいずれかのテーブルスペースディレクトリにファイルがある場合は、処理を中止します。
- リストアで`--set=latest`（デフォルト）を指定した場合、実際にリストアするバックアップをログに出力するようにしました。
- PostgreSQL 9.5の部分WALセグメントと`recovery_target_action`設定をサポートしました。`archive_mode = 'always'`設定はまだサポートしていません。
- PostgreSQL 9.4で導入された`recovery_target = 'immediate'`リカバリー設定をサポートしました。
- テーブルスペースについて、pg_tblspc内のパスまたはファイル、pg_tblspc内の相対リンク、$PGDATA内のテーブルスペースをチェックするようにしました。この3つはいずれもエラーになります。


### v0.89リリースノート {#v089-release-notes}

*タイムアウトの不具合修正と読み取り専用リポジトリからのリストア*

*2015年12月24日リリース*

**バグ修正：**

- リモートかつマルチスレッドで実行する、時間のかかるバックアップやリストアがタイムアウトする問題を修正しました。スレッドのリモートプロセスがすべての処理を行っている間も、メインプロセスのリモートがタイムアウトしないよう、キープアライブを使用するようになりました。デバッグしやすいよう、タイムアウトのエラーメッセージも改善しました。 (*報告：Stephen Frost。*)

**新機能：**

- `--no-lock`と`--log-level-file=off`を使い、読み取り専用リポジトリからリストアできるようにしました。`--no-lock`オプションはリストア時にのみ使用できます。


### v0.88リリースノート {#v088-release-notes}

*ドキュメントと軽微な不具合修正*

*2015年11月22日リリース*

**バグ修正：**

- `start`／`stop`コマンドで`--config`オプションが必須になっていた問題を修正しました。 (*報告：Dmitry Didovicher。*)
- ログファイルに追記せず、上書きしていた問題を修正しました。 (*報告：Stephen Frost, Dmitry Didovicher。*)
- `backup-user`が任意になっていなかった問題を修正しました。

**新機能：**

- リポジトリ内のバックアップディレクトリにはシンボリックリンクを作成しなくなりました。これらのリンクは任意の場所を指すことができ、危険になり得るためです。リストア時には引き続きシンボリックリンクを再作成します。 (*提案：Stephen Frost。*)
- バックアップの期限切れ処理のメッセージを改善しました。フルバックアップと差分バックアップの期限切れ処理を、併せて期限切れとなるすべての依存バックアップの一覧とともに、1行でログに出力します。
- アーカイブの保持数を明示的に設定していない場合、フルバックアップの保持数に自動設定するようにしました。

**ドキュメントの機能：**

- ユーザーガイドに、差分リストア、期限切れ処理、専用バックアップホスト、pgBackRestの起動と停止、レプリケーションの説明を追加しました。


### v0.87リリースノート {#v087-release-notes}

*ウェブサイトとユーザーガイド*

*2015年10月28日リリース*

**新機能：**

- `backup_label.old`ファイルと`recovery.done`ファイルをバックアップから除外するようにしました。

**ドキュメントの機能：**

- pgBackRestの基本と、PITRを含む高度なトピックの一部を扱う、新しいユーザーガイドを追加しました。まだ追加すべき内容は多くありますが、まずは出発点です。 (*貢献：David Steele, Stephen Frost。レビュー：Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher。*)


### v0.85リリースノート {#v085-release-notes}

*起動／停止コマンドと軽微な不具合修正*

*2015年10月8日リリース*

**バグ修正：**

- バックアップまたはリストアが正常に完了した後に、エラーを返す場合がある問題を修正しました。
- バックアップ失敗時にバックアップのルートディレクトリに一時ファイルが残ると、再開に失敗する問題を修正しました。コピー段階でバックアッププロセスを強制終了した場合に起こりやすい状況でした。

**新機能：**

- PostgreSQLが停止しているシステムや、他の理由で処理を休止する必要があるシステムで、pgBackRestプロセスが実行されないようにする`stop`コマンドと`start`コマンドを追加しました。
- PostgreSQL 9.5 beta1を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。


### v0.82リリースノート {#v082-release-notes}

*リファクタリング、コマンドラインヘルプ、軽微な不具合修正*

*2015年9月14日リリース*

**バグ修正：**

- 再開した圧縮バックアップで既存ファイルが保持されない問題を修正しました。
- 再開およびincr/diff時に、前回のバックアップの圧縮設定とハードリンク設定が同じであることを確認していなかった問題を修正しました。
- `--force`を指定せずに、稼働中のPostgreSQLクラスターで`--no-start-stop`によるコールドバックアップを開始できてしまう問題を修正しました。
- スレッドが要求されていなくてもスレッドを開始する場合がある問題を修正しました。
- アップグレード／ダウングレード後に、`backup.info`と`archive.info`内のpgBackRestのバージョン番号が更新されない問題を修正しました。
- リポジトリにstanzaがないと、`info`コマンドが例外を発生させる問題を修正しました。 (*報告：Stephen Frost。*)
- PostgreSQLの`pg_stop_backup()`のNOTICEが`stderr`に出力される問題を修正しました。 (*報告：Stephen Frost。*)

**新機能：**

- PostgreSQL 9.5 alpha2を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。

**改善：**

- pgBackRestの命名規則と一貫させるため、`recovery-setting`オプションとセクションの名前を`recovery-option`に変更しました。
- コマンド、特に非同期アーカイブを高速化するため、モジュールの動的読み込みを追加しました。

**ドキュメントの機能：**

- コマンドラインヘルプは、他のドキュメントと同じXMLソースから抽出するようになり、内容も大幅に詳しくなりました。


### v0.80リリースノート {#v080-release-notes}

*DBIのサポート、安定性、利便性向上の機能*

*2015年8月9日リリース*

**バグ修正：**

- `info`コマンドが最も古いバックアップと最も新しいバックアップの整形済みタイムスタンプを、どちらも現在時刻として報告していた問題を修正しました。影響を受けるのは`text`出力のみで、`json`出力は正しいエポック値を報告していました。 (*報告：Michael Renner。*)
- sshエラー（特に接続時のエラー）がログに記録されないプロトコルの問題を修正しました。

**新機能：**

- リポジトリを作成、更新するときのディレクトリとファイルのモードを統一しました。デフォルトでは`umask`を`0000`に設定しますが、`neutral-umask`設定で無効にできます。 (*提案：Cynthia Shang。*)
- 新しいバックアップの開始時に、失敗したバックアップを自動停止できる`stop-auto`オプションを追加しました。
- pgBackRestが`pg_start_backup()`と`pg_stop_backup()`の戻りを待つ時間を制限する`db-timeout`オプションを追加しました。
- リストア開始時に`pg_control`を削除し、最後にコピーし直すようにしました。これにより、リストアが未完了の状態でPostgreSQLが起動される可能性を防ぎます。
- `db-path`設定と`db-port`の整合性を確認するチェックを追加しました。クラスターが報告する`data_directory`を`db-path`設定と比較し、クラスターが報告するバージョンを`pg_control`から読み取った値と比較します。また、`db-socket-path`設定が絶対パスであることを確認します。
- PostgreSQL 9.5 alpha1を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。

**改善：**

- PostgreSQLへの接続に、`psql`の代わりにPerlの`DBI`と`DBD::Pg`を使用するようにしました。`cmd-psql`設定と`cmd-psql-option`設定を削除し、`db-port`と`db-socket-path`に置き換えました。インストールガイドの手順に従い、使用するOSに`DBD::Pg`をインストールしてください。

**テストスイートの機能：**

- Ubuntu 14.04とCentOS 7向けのvagrantテスト設定を追加しました。


### v0.78リリースノート {#v078-release-notes}

*CPANへの依存の削除と安定性の改善*

*2015年7月13日リリース*

**改善：**

- マルチスレッド動作でのCPANパッケージへの依存を削除しました。`threads`パッケージと`Thread::Queue`パッケージを更新してもよいですが、必須ではなくなりました。
- 待機時間のバックオフを、等比数列からフィボナッチ数列に変更しました。妥当な値を保ちつつ、待機時間の増加を緩やかにします。

**テストスイートの機能：**

- Ubuntu 12.04とCentOS 6向けのvagrantテスト設定を追加しました。


### v0.77リリースノート {#v077-release-notes}

*CentOS/RHEL 6のサポートとプロトコルの改善*

*2015年6月30日リリース*

**新機能：**

- バックアップ／リストアとアーカイブの安全性を高めるため、`File`オブジェクトにファイルとディレクトリの同期処理を追加しました。 (*提案：Andres Freund。*)
- CentOS/RHEL 6のデフォルトであるPerl 5.10.1とOpenSSH 5.3をサポートしました。 (*提案：Eric Radman。*)
- `archive_command`が設定されておらず、`--no-archive-check`も指定されていない状態でバックアップを実行した場合のエラーメッセージを改善しました。 (*提案：Eric Radman。*)


### v0.75リリースノート {#v075-release-notes}

*新しいリポジトリ形式、infoコマンド、9.5の試験的サポート*

*2015年6月14日リリース*

**重要な注意事項**：この一斉移行が必要なリリースでは、旧バージョンのpgBackRestとの互換性が失われます。マニフェスト形式、ディスク上の構造、実行ファイル名がすべて変更されています。このバージョンのpgBackRestのバックアップを保存するには新しいリポジトリを作成し、リストアが必要になる場合に備えて旧リポジトリをしばらく保持する必要があります。`pg_backrest.conf`ファイルは変更されていませんが、cronなどにある`pg_backrest.pl`への参照を、`.pl`拡張子のない`pg_backrest`に変更する必要があります。

**新機能：**

- `info`コマンドを追加しました。
- ログの出力をバッファリングしないようにしました。これにより、複数スレッドから書き込むログファイルの混乱を抑えられるはずです。 (*提案：Michael Renner。*)
- PostgreSQL 9.5を試験的にサポートしました。コントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各リリースで追従します。

**改善：**

- `backup`でのファイルの処理順を効率化しました。サイズの大きい順にコピーすることで、最後に1つのスレッドだけが大きなファイルをコピーする状況を避けます。`restore`ではすでに実装済みでした。


### v0.70リリースノート {#v070-release-notes}

*アーカイブの安定性とログ、ヘルプの改善*

*2015年6月1日リリース*

**バグ修正：**

- `hardlink=n`の場合、incr/diffバックアップで`archive-copy`が失敗する問題を修正しました。この場合は`pg_xlog`パスがまだ存在しないため、作成する必要があります。 (*報告：Michael Renner。*)
- 非同期アーカイブで`archive-max-mb`に達した際、`archive-push`が正しく0を返さない問題を修正しました。また、停止ファイルを2回削除する必要がないよう、非同期処理のチェックを転送後に移しました。このケースの単体テストを追加し、何が起きたかをユーザーが把握しやすいようエラーメッセージも改善しました。 (*報告：Michael Renner。*)
- 1つのstanzaに対して同じ種類の操作を複数実行できてしまう、ロックの問題を修正しました。データの整合性への影響はないようでしたが、アーカイブ時に不要なエラーが発生し、バックアップ／リストアでもエラーにつながる可能性がありました。 (*報告：Michael Renner。*)

**新機能：**

- チェックサムが一致する場合、重複するWALセグメントをアーカイブできるようにしました。一部のリカバリー手順で必要になるためです。
- `pg_backrest.conf`で`#`文字を使ってコメントを記述したり、設定を無効にしたりできるようにしました。行の最初の文字にある`#`のみが有効です。 (*提案：Michael Renner。*)
- バックアップがチェックポイントを待っていることがわかるよう、`pg_start_backup()`の前のログを改善しました。 (*提案：Michael Renner。*)
- コマンドの動作とログを各種修正しました。 (*レビュー：Michael Renner。提案：Michael Renner。*)

**改善：**

- `JSON`モジュールを、Perl本体に同梱される`JSON::PP`に置き換えました。

**ドキュメントの不具合修正：**

- ヘルプを各種修正しました。 (*レビュー：Michael Renner。報告：Michael Renner。*)


### v0.65リリースノート {#v065-release-notes}

*再開とリストアのログの改善、コンパクトなリストア*

*2015年5月11日リリース*

**バグ修正：**

- 相対パスでリストアを実行した場合に、`recovery.conf`に絶対パスが書き込まれない問題を修正しました。

**新機能：**

- 再開機能を改善しました。再開時に既存のファイルが変更されていないことを確認し、バックアップの進行中にチェックサムを保持できるよう、マニフェストをより頻繁に保存します。再開時の各ケースを検証する単体テストも追加しました。
- 再開を任意にしました。無効にするには`resume`設定、またはコマンドラインの`--no-resume`を使用してください。
- リストア時のinfoメッセージを増やしました。以前はリストアのメッセージの大半がdebugレベルだったため、ログへの出力が少なくなっていました。
- テーブルスペースを`pg_tblspc`パスにリストアできる`tablespace`設定を追加しました。これにより、開発やステージングなどに便利な、まとまった配置でリストアできます。現在のpgBackRestは`pg_tblspc`パス内にはリンクのみがあることを前提としているため、このようにリストアしたクラスターをバックアップすることはできません。


### v0.61リリースノート {#v061-release-notes}

*非圧縮のリモート宛先に関する不具合修正*

*2015年4月21日リリース*

**バグ修正：**

- 圧縮率の高い大きなファイルを非圧縮のリモート宛先へコピーすると、バッファリングエラーが発生する場合がある問題を修正しました。このエラーは展開処理で検出され、データ破損ではなくバックアップの失敗として扱われていたため、以前のバージョンで正常に完了したバックアップには影響しないはずです。


### v0.60リリースノート {#v060-release-notes}

*バージョンサポートの拡充とWALの改善*

*2015年4月19日リリース*

**バグ修正：**

- 重複するWALを送信するとエラーになるようにしました。従来、この操作が成功するのはチェックサムが無効な場合のみでした。

**新機能：**

- データベースのシステムIDを使い、アーカイブ内のすべてのWALが同じデータベースに対応することを確認します。これにより、複数クラスターのWALを同じアーカイブに送信してしまう設定ミスを防ぎやすくなります。

**テストスイートの機能：**

- PostgreSQL 8.3までさかのぼって回帰テストが動作するようになりました。


### v0.50リリースノート {#v050-release-notes}

*リストア機能などの追加*

*2015年3月25日リリース*

**バグ修正：**

- チェックサムの不具合を修正し、通常のバックアップと再開したバックアップで動作するようにしました。チェックサムとチェックサムによる差分処理は機能として分離すべきだとようやく気付き、これによりいくつかの処理を簡素化できました。チェックサムによる差分処理についてはissue #28を作成しました。
- バックアップの種類と前回のバックアップが一致しない中断済みバックアップから、バックアップを再開できてしまう問題を修正しました。

**新機能：**

- リストア機能を追加しました。
- すべてのオプションをコマンドラインで指定できるようになり、`pg_backrest.conf`が任意になりました。
- 圧縮／展開処理はスレッドを使わずに実行し、チェックサムとサイズはストリーム内で計算するようになりました。このため、ファイルのチェックサムは必須になりました。
- Postgresが停止している場合にバックアップできる`--no-start-stop`オプションを追加しました。`postmaster.pid`が存在する場合、バックアップを実行するには`--force`が必要です（ただしPostgresが稼働中の場合、整合性のないバックアップが作成される可能性が高くなります）。このオプションは主に単体テストのために追加しましたが、実際の運用でも用途があるかもしれません。
- マニフェストの破損や変更を検出するため、`backup.manifest`にチェックサムを追加しました。
- `latest`リンクは常に最新のバックアップを指します。利便性の向上とリストアの簡略化のために追加しました。

**テストスイートの機能：**

- すべての領域で単体テストを拡充しました。


### v0.30リリースノート {#v030-release-notes}

*コアの再構成と単体テスト*

*2014年10月5日リリース*

**ドキュメントの機能：**

- 不足していたドキュメントを追加しました

**テストスイートの機能：**

- すべての基本操作を対象とする、かなり包括的な単体テストを追加しました。まだ作業が必要なのは確かですが、単体テストには常に改善の余地があります。


### v0.19リリースノート {#v019-release-notes}

*エラーの報告と処理の改善*

*2014年5月13日リリース*

**バグ修正：**

- `file_copy()`がデフォルトでエラーを無視する設定になっていた重大な不具合を発見し、修正しました。また、`file_exists()`には、ファイルが実際に存在していても存在確認に失敗する問題がありました。可能性は非常に低いものの、両者が重なるとエラーを出さずに破損したバックアップが作成されるおそれがありました。


### v0.18リリースノート {#v018-release-notes}

*アーカイブがない場合に軽微なエラーを返す*

*2014年4月13日リリース*

**バグ修正：**

- アーカイブファイルがない場合、`archive-get`コマンドは1を返すようになりました。これにより、重大なエラー（ssh接続の失敗、ファイルコピーエラーなど）と区別できます。PostgreSQLは、これによってアーカイブストリームが正常に終了したことを判断できます。ただし、アーカイブストリームの途中に欠落がある可能性は考慮していません。 (*報告：Stephen Frost。*)


### v0.17リリースノート {#v017-release-notes}

*アーカイブディレクトリを削除できない場合の警告*

*2014年4月3日リリース*

**バグ修正：**

- 空であるはずのアーカイブディレクトリを削除できない場合、backrestはエラーを発生させていました。適切な修正を予定していますが、当面は処理を続けられるよう警告に変更しました。この問題はバックアップにも影響していました。最初のアーカイブファイルが別のディレクトリにある場合、さらに不運な条件が重なると、最後のアーカイブファイルが送信されないことがありました。


### v0.16リリースノート {#v016-release-notes}

*SSHセッションへのRequestTTY=yesの設定*

*2014年4月1日リリース*

**バグ修正：**

- sshセッションに`RequestTTY=yes`を追加しました。これにより、不規則に起きる停止が防げることを期待しています。


### v0.15リリースノート {#v015-release-notes}

*archive-getの追加*

*2014年3月29日リリース*

**新機能：**

- リストアを支援する`archive-get`機能を追加しました。
- バックアップ開始時にチェックポイントを強制する`start-fast=y`オプションを追加しました。


### v0.11リリースノート {#v011-release-notes}

*軽微な修正*

*2014年3月26日リリース*

**バグ修正：**

- データベースへのSSH接続から`master_stderr_discard`オプションを削除しました。時折停止することがあり、ファイル処理で以前に見られた問題と関連している可能性があります。 (*報告：Stephen Frost。*)
- `backup`コマンドと`expire`コマンドでのロックファイルの競合を`ERROR`に変更しました。アーカイブのロック処理からコピーしたため、`DEBUG`になっていました。


### v0.10リリースノート {#v010-release-notes}

*バックアップとアーカイブが動作*

*2014年3月5日リリース*

**新機能：**

- リストア機能はありませんが、バックアップディレクトリは整合性のあるPostgreSQLデータディレクトリです。ファイルを展開するか、バックアップの圧縮を無効にする必要があります。ZFSなどのファイルシステムでは非圧縮バックアップが適しています。スナップショットを使ってローカルにリストアし、論理バックアップの作成や必要なデータの部分的な復旧ができるためです。
- アーカイブはシングルスレッドです。書き込み量の多い、当方の数テラバイト規模のデータベースでは問題になっていません。大容量のWALボリューム、または近くにある大容量ボリュームでasyncオプションを使うことを推奨します。
- バックアップはマルチスレッドですが、`Net::OpenSSH`ライブラリは100%スレッドセーフではないようで、ごくまれにスレッドが停止します。プロセス全体のタイムアウトがあり、プロセスを強制終了することで解消します。確かに、非常に不格好な方法です。
- バックアップを再開するとチェックサムが失われます。複数回再開した場合、最後のバックアップでのみチェックサムが記録されます。前回のバックアップのチェックサムは正しく記録されており、フルバックアップを取得するとすべてリセットされます。
- `Config::IniFile`は大きなファイルをうまく扱えないようなので、`backup.manifest`は`Storable`形式で書き込んでいます。ぜひ人が読めるテキストとして保存できるようにしたいと考えています。

**ドキュメントの機能：**

- ドキュメントはまったくありません（コード内を除きます）。このリリースノートだけは例外です。
