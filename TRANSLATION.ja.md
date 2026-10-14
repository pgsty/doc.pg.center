# 日本語翻訳規約

この文書は doc.pg.center の日本語版で使用する用語と文体の基準です。英語版を
唯一の原文とし、日本語訳は同じディレクトリに `.ja.md` 接尾辞で配置します。

## 翻訳範囲と構造

- タイトル、説明、要約、ナビゲーション、本文、説明用リスト、表見出し、
  リンクテキスト、画像の代替テキストをすべて翻訳します。
- 製品名、プロトコル名、コマンド、オプション、設定キーワード、API/RPC、
  メッセージ、フィールド、環境変数、メトリクス、ファイル名、パス、URL、
  バージョン、プレースホルダーは原文のまま保持します。
- コピー可能なコマンド、設定、ソースコード、出力、ログ、エラーメッセージ、
  ライセンス本文は翻訳しません。
- 以下の登録済み pgBadger・HAProxy 説明ブロックを除き、コードフェンスとインデント付き
  コードブロックはコメントも含めてバイト単位で保持します。shortcode、脚注、
  HTML タグ、参照定義、明示的アンカー、数値を厳密に保持します。
- `content/docs/pgbadger/` の説明用 `text` フェンスのうち、独立したレビューと
  登録を済ませたものに限り、引数ヘルプ、終了コードの説明、アルゴリズムの
  擬似コード内の自然言語による手順、ディレクトリの説明、およびその中の例を
  説明するコメントを翻訳します。実際の CLI シグネチャ、オプション、許容値、
  デフォルト値、コマンド、SQL、設定、正規表現、診断、法律原文、人名、数値、
  数式はそのまま保持します。この例外は実際のコードのコメントには適用しません。
- 各例外を `data/translation-fences/pgbadger.ja/` に登録し、原文と訳文の正確な
  SHA-256（`source_sha256`、`target_sha256`）、保護対象のリテラル
  （`protected_literals`）、実際のコマンド行または出力行（`protected_lines`）を
  記録します。独立したレビュアーが意味とリテラルを確認します。未登録または
  ハッシュが変わったフェンスはバイト単位の保護対象です。`text` ラベルだけでは
  例外になりません。
- HAProxy のフェンスまたはインデント付きブロックでは、引数の説明、表のラベル、
  自然言語の説明だけを翻訳できます。`data/translation-checks/haproxy-ja.json` に
  正確な原文・訳文ハッシュ、説明の分類、独立レビューの理由、保護対象の
  リテラルと行を登録します。実際の設定、コマンド、ソースコード、プロトコルの
  メッセージ、出力、診断、コードのコメントは、説明と混在する場合もそのまま
  保持します。未登録またはハッシュが変わったブロックは例外として扱いません。
- HAProxy のサンプルのシグネチャと旧エイリアスの宣言では、戻り値の型名
  `integer`、`boolean`、`bool`、`string`、`binary`、`ip` をそのまま保持します。
  本文中の自然言語による型の説明は通常どおり翻訳します。
- 読者向け本文には製品の使用に必要な情報だけを記載します。翻訳方針、訳者注、
  「このページは原文を保持しています」といった案内、編集上の訂正作業の経緯を
  追加しません。出典・帰属データと法律原文は保持します。
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
shortcode、アセット、参照の構造を一致させます。コードブロックはバイト単位で
一致させ、例外は上記の手順で正確なハッシュとリテラルを登録し、独立レビューを
済ませた pgBadger・HAProxy の説明ブロックに限ります。実際のコードとその
コメントは引き続き保護します。読者向け本文に翻訳方針、訳者注、編集作業の経緯が
ないことも確認します。最後に Hugo の本番ビルドと内部リンク検査を実行します。
