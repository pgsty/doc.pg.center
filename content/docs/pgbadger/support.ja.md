---
title: "サポートと貢献"
linkTitle: "サポート"
weight: 100
description: "バグの報告、機能要望、パッチの提供、およびPostgreSQLの専門サポートの利用"
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [タスク]
aliases: [/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadgerはオープンプロジェクトとして維持されています。バグ報告、機能要望、ドキュメントの修正、パッチは、アップストリームのGitHubリポジトリ経由で処理されます。

## バグおよび機能要望 {#bugs-and-features}

1. 最新リリース版にアップグレードし、動作が依然として発生するか確認してください。
2. 既存の回答を検索するには、[オープンな問題](https://github.com/darold/pgbadger/issues)および [クローズされた問題](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed)を確認してください。
3. 問題を再現する最小限の安全なログサンプルおよびコマンドラインに簡略化してください。
4. 認証情報、機密SQL、バインド値、ホスト名、アドレス、および業務データを削除します。
5. pgBadgerのバージョン、オペレーティングシステム、入力形式、正確なオプション、観測結果、期待結果を含む [新しいIssue](https://github.com/darold/pgbadger/issues/new)を開いてください。

クラッシュやパーサーの誤りの場合、境界を再現するために必要な最小限のサニタイズ済みログ行のみを含めてください。完全な本番ログや生成されたレポートは、公開Issueへの添付にはほとんどの場合適していません。

## パッチを提供する {#contribute-a-patch}

プロジェクトには `.editorconfig`ファイルが含まれており、一貫したスペース設定が行われます。ユーザーが見える動作に影響を与える変更を行う際は、コマンドヘルプ、POD、および生成されたMarkdownドキュメントを同期させてください。

アップストリームドキュメントのワークフローは以下の通りです：

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod`は長形式の主要なソースです。`pgbadger --help`は概要を提供し、READMEファイルは生成されたビューです。プルリクエストを提出する前に、関連するテストを実行してください。

- [ソースリポジトリ](https://github.com/darold/pgbadger)
- [プルリクエスト](https://github.com/darold/pgbadger/pulls)
- [貢献ガイド](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [開発ノート](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## 商用サポート {#commercial-support}

pgBadgerプロジェクトは、ライセンス下で保守またはサポートを保証していません。PostgreSQLのログ処理、パフォーマンス分析、レポート自動化に関する有料サポートが必要な場合は、[PostgreSQLプロフェッショナルサービスディレクトリ](https://www.postgresql.org/support/professional_support/)をご参照ください。

