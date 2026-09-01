# 日本語翻訳規約

この文書は pgsql.cc の日本語版で使用する用語と文体の基準です。英語版を
唯一の原文とし、日本語訳は同じディレクトリに `.ja.md` 接尾辞で配置します。

## 翻訳範囲と構造

- タイトル、説明、要約、ナビゲーション、本文、説明用リスト、表見出し、
  リンクテキスト、画像の代替テキストをすべて翻訳します。
- 製品名、プロトコル名、コマンド、オプション、設定キーワード、API/RPC、
  メッセージ、フィールド、環境変数、メトリクス、ファイル名、パス、URL、
  バージョン、プレースホルダーは原文のまま保持します。
- コピー可能なコマンド、設定、ソースコード、出力、ログ、エラーメッセージ、
  ライセンス本文は翻訳しません。
- コードフェンス、shortcode、脚注、HTML タグ、参照定義、明示的アンカー、
  数値を厳密に保持します。
- 明示的アンカーのない翻訳見出しには、英語ページで実際にレンダリングされた
  ID を追加し、言語をまたぐディープリンクを維持します。
- 翻訳済みページへのリンクには `/ja/` を付けます。画像などの共有アセットは
  言語接頭辞のないパスを維持します。

## 文体

- Linux、ネットワーク、PostgreSQL、分散システムの運用担当者を対象に、
  正確で自然、簡潔な日本語を使用します。
- 情報を省略、要約、補足せず、直接的な文にします。
- `must` は明確な義務、`should` は推奨、`may/can` は可能性として訳し、
  原文の規範強度を変えません。
- `Patroni`、`pgBackRest`、`PgBouncer`、`pgBadger`、`HAProxy`、`etcd`、
  `PostgreSQL`、`Prometheus`、`Grafana`、`Kubernetes`、`OpenSSL` の表記を
  変更しません。
- 日本語の句読点を使用し、日本語と製品名、コマンド、数値の間に不要な空白を
  入れません。

## site 用語集

| 英語 | 日本語 |
| --- | --- |
| documentation | ドキュメント |
| upstream | アップストリーム |
| release notes | リリースノート |
| search | 検索 |
| section | セクション |
| page | ページ |
| language | 言語 |
| translation | 翻訳 |

## patroni 用語集

| 英語 | 日本語 |
| --- | --- |
| cluster | クラスター |
| leader | リーダー |
| primary | プライマリー |
| replica | レプリカ |
| failover | フェイルオーバー |
| switchover | スイッチオーバー |
| distributed configuration store | 分散構成ストア |
| high availability | 高可用性 |
| synchronous mode | 同期モード |
| standby cluster | スタンバイクラスター |
| watchdog | ウォッチドッグ |
| bootstrap | ブートストラップ |

## pgbackrest 用語集

| 英語 | 日本語 |
| --- | --- |
| backup | バックアップ |
| restore | リストア |
| repository | リポジトリ |
| stanza | stanza |
| archive | アーカイブ |
| retention | 保持 |
| full backup | フルバックアップ |
| differential backup | 差分バックアップ |
| incremental backup | 増分バックアップ |
| point-in-time recovery | ポイントインタイムリカバリー |
| checksum | チェックサム |

## pgbouncer 用語集

| 英語 | 日本語 |
| --- | --- |
| connection pooler | コネクションプーラー |
| connection pool | コネクションプール |
| session pooling | セッションプーリング |
| transaction pooling | トランザクションプーリング |
| statement pooling | ステートメントプーリング |
| authentication | 認証 |
| client | クライアント |
| server | サーバー |
| routing | ルーティング |
| console | 管理コンソール |

## pgbadger 用語集

| 英語 | 日本語 |
| --- | --- |
| log analyzer | ログアナライザー |
| log file | ログファイル |
| report | レポート |
| query | クエリー |
| slow query | スロークエリー |
| lock | ロック |
| checkpoint | チェックポイント |
| incremental report | 増分レポート |
| output format | 出力形式 |

## HAProxy 用語集

| 英語 | 日本語 |
| --- | --- |
| frontend | フロントエンド |
| backend | バックエンド |
| proxy | プロキシ |
| load balancer | ロードバランサー |
| load balancing | 負荷分散 |
| health check | ヘルスチェック |
| stick table | スティックテーブル |
| sample fetch | サンプル取得 |
| access control list | アクセス制御リスト |
| listener | リスナー |
| listening socket | リッスンソケット |
| graceful shutdown | グレースフルシャットダウン |
| graceful reload | グレースフルリロード |
| runtime API | ランタイム API |
| runtime CLI | ランタイム CLI |
| troubleshooting | トラブルシューティング |
| request | リクエスト |
| response | レスポンス |
| header | ヘッダー |
| throughput | スループット |
| timeout | タイムアウト |

## etcd 用語集

| 英語 | 日本語 |
| --- | --- |
| cluster | クラスター |
| member | メンバー |
| leader | リーダー |
| follower | フォロワー |
| learner | 学習者メンバー |
| key-value store | キー・バリューストア |
| keyspace | キー空間 |
| lease | リース |
| watch | 監視 |
| watcher | ウォッチャー |
| revision | リビジョン |
| compaction | コンパクション |
| defragmentation | デフラグメンテーション |
| quorum | クォーラム |
| consensus | コンセンサス |
| snapshot | スナップショット |
| rolling upgrade | ローリングアップグレード |
| recovery | リカバリー |
| linearizable read | 線形化可能読み取り |
| serializable read | シリアライズ可能読み取り |
| write-ahead log | 先行書き込みログ |

## 検証

すべての英語ページに、同じ論理パスの日本語ページがちょうど 1 つ必要です。
ルーティング用メタデータ、アップストリームリンク、アンカー、コードフェンス、
shortcode、アセット、参照の構造を一致させます。最後に Hugo の本番ビルドと
内部リンク検査を実行します。
