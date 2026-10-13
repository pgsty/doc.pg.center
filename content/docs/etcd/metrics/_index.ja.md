---
title: "メトリクス"
weight: 1350
description: "リアルタイムの監視とデバッグに使用するメトリクス"
icon: fa-solid fa-chart-line
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/metrics/_index.md"
aliases: [/etcd/metrics/]
---

etcdはメトリクスの報告に[Prometheus][prometheus]を使用します。メトリクスはリアルタイムの監視やデバッグに利用できます。etcdはメトリクスを永続化しないため、メンバーを再起動するとメトリクスはリセットされます。

利用可能なメトリクスを確認する最も簡単な方法は、メトリクスのエンドポイント`/metrics`にcURLでアクセスすることです。形式は[Prometheusのドキュメント](http://prometheus.io/docs/instrumenting/exposition_formats/)に記載されています。

[Prometheusの入門ドキュメント][prometheus-getting-started]に従ってPrometheusサーバーを起動し、etcdのメトリクスを収集してください。

メトリクスの命名は、推奨される[Prometheusのベストプラクティス][prometheus-naming]に従っています。メトリクス名には、名前空間を表す`etcd`または`etcd_debugging`プレフィックスと、サブシステムを表すプレフィックス（`wal`や`etcdserver`など）が付きます。

## etcd名前空間のメトリクス {#etcd-namespace-metrics}

`etcd`プレフィックスのメトリクスは、監視とアラートのためのものです。安定した高水準のメトリクスであり、変更がある場合はリリースノートに記載されます。

etcd2に関連するメトリクスは、[v2メトリクスガイド][v2-http-metrics]に記載されています。

### サーバー {#server}

これらのメトリクスはetcdサーバーの状態を表します。障害や問題を検出して対処できるよう、本番環境のすべてのetcdクラスターでサーバーメトリクスを注意深く監視することを推奨します。

これらのメトリクスには、すべて`etcd_server_`プレフィックスが付きます。

| 名前 | 説明 | 型 |
|---------------------------|----------------------------------------------------------|---------|
| has_leader | リーダーが存在するかどうか。1は存在し、0は存在しないことを示します。| Gauge |
| leader_changes_seen_total | 観測したリーダー変更の回数。| Counter |
| proposals_committed_total | コミットされたコンセンサス提案の総数。| Gauge |
| proposals_applied_total | 適用されたコンセンサス提案の総数。| Gauge |
| proposals_pending | 現在保留中の提案数。| Gauge |
| proposals_failed_total | 観測した失敗した提案の総数。| Counter |

`has_leader`は、メンバーにリーダーが存在するかどうかを示します。メンバーにリーダーが存在しない場合、そのメンバーは完全に利用不能です。クラスター内のすべてのメンバーにリーダーが存在しない場合、クラスター全体が完全に利用不能です。

`leader_changes_seen_total`は、メンバーが起動してから観測したリーダー変更の回数です。リーダーが頻繁に変わると、etcdの性能に大きく影響します。また、ネットワーク接続の問題やetcdクラスターへの過剰な負荷などによって、リーダーが不安定であることも示します。

`proposals_committed_total`は、コミットされたコンセンサス提案の総数を記録します。クラスターが正常なら、このゲージは時間とともに増加するはずです。etcdクラスター内の複数の正常なメンバーで、同じ時点のコミット済み提案の総数が異なる場合があります。これは、起動後にピアから復旧していること、リーダーより遅れていること、または自身がリーダーで最も多くのコミットを保持していることが原因と考えられます。クラスター内のすべてのメンバーでこのメトリクスを監視することが重要です。特定のメンバーとそのリーダーの間に大きな遅れが続く場合、そのメンバーの処理が遅いか、正常ではないことを示します。

`proposals_applied_total`は、適用されたコンセンサス提案の総数を記録します。etcdサーバーは、コミットされたすべての提案を非同期に適用します。通常、`proposals_committed_total`と`proposals_applied_total`の差は小さく、高負荷時でも数千以内に収まるはずです。この差が増え続ける場合は、etcdサーバーが過負荷であることを示します。負荷の高い範囲クエリーや大規模なtxn操作など、処理コストの高いクエリーを適用するときに起こる可能性があります。

`proposals_pending`は、コミット待ちのキューに入っている提案数を示します。保留中の提案が増加している場合は、クライアントからの負荷が高いか、メンバーが提案をコミットできていないと考えられます。

`proposals_failed_total`は、通常、リーダー選出に伴う一時的な失敗、またはクラスターのクォーラム喪失による長い停止時間という2つの問題に関連します。

### ディスク {#disk}

これらのメトリクスは、ディスク操作の状態を表します。

これらのメトリクスには、すべて`etcd_disk_`プレフィックスが付きます。

| 名前 | 説明 | 型 |
|------------------------------------|-------------------------------------------------------|-----------|
| wal_fsync_duration_seconds | walが呼び出すfsyncのレイテンシー分布。| Histogram |
| backend_commit_duration_seconds | backendが呼び出すcommitのレイテンシー分布。| Histogram |

`wal_fsync`は、etcdがログエントリーを適用する前にディスクへ永続化するときに呼び出されます。

`backend_commit`は、etcdが直近の変更の増分スナップショットをディスクにコミットするときに呼び出されます。

ディスク操作のレイテンシー（`wal_fsync_duration_seconds`または`backend_commit_duration_seconds`）が高い場合は、多くの場合、ディスクの問題を示しています。リクエストのレイテンシーが高くなったり、クラスターが不安定になったりする可能性があります。

### ネットワーク {#network}

これらのメトリクスは、ネットワークの状態を表します。

これらのメトリクスには、すべて`etcd_network_`プレフィックスが付きます。

| 名前 | 説明 | 型 |
|---------------------------------|--------------------------------------------------------------------|---------------|
| peer_sent_bytes_total | IDが`To`のピアへ送信した総バイト数。| Counter(To) |
| peer_received_bytes_total | IDが`From`のピアから受信した総バイト数。| Counter(From) |
| peer_sent_failures_total | IDが`To`のピアへの送信失敗の総数。| Counter(To) |
| peer_received_failures_total | IDが`From`のピアからの受信失敗の総数。| Counter(From) |
| peer_round_trip_time_seconds | ピア間の往復時間のヒストグラム。| Histogram(To) |
| client_grpc_sent_bytes_total | grpcクライアントへ送信した総バイト数。| Counter |
| client_grpc_received_bytes_total | grpcクライアントから受信した総バイト数。| Counter |

`peer_sent_bytes_total`は、特定のピアへ送信した総バイト数です。通常、リーダーメンバーはレプリケーションデータの送信を担うため、他のメンバーより多くのデータを送信します。

`peer_received_bytes_total`は、特定のピアから受信した総バイト数です。通常、フォロワーメンバーはリーダーメンバーからのみデータを受信します。

### gRPCリクエスト {#grpc-requests}

これらのメトリクスは、[go-grpc-prometheus][go-grpc-prometheus]を通じて公開されます。

## etcd_debugging名前空間のメトリクス {#etcd_debugging-namespace-metrics}

`etcd_debugging`プレフィックスのメトリクスは、デバッグ用です。実装への依存度が高く、変更されやすいものです。新しいetcdリリースで、予告なく変更または削除される場合があります。一部のメトリクスは、より安定した段階で`etcd`プレフィックスへ移される場合があります。

### スナップショット {#snapshot}

| 名前 | 説明 | 型 |
|--------------------------------------------|------------------------------------------------------------|-----------|
| snapshot_save_total_duration_seconds | snapshotが呼び出すsaveの合計レイテンシーの分布。| Histogram |

スナップショットの所要時間（`snapshot_save_total_duration_seconds`）が異常に長い場合は、ディスクの問題を示しており、クラスターが不安定になる可能性があります。

## Prometheusが提供するメトリクス {#prometheus-supplied-metrics}

Prometheusのクライアントライブラリーは、`go`および`process`名前空間にいくつものメトリクスを提供します。特に注目すべきものをいくつか挙げます。

| 名前 | 説明 | 型 |
|-----------------------------------|--------------------------------------------|--------------|
| process_open_fds | 開いているファイルディスクリプターの数。| Gauge |
| process_max_fds | 開くことのできるファイルディスクリプターの最大数。| Gauge |

> [!NOTE]
> `process_open_fds`や`process_max_fds`などのプロセスメトリクスは、現時点ではDarwin（macOS）システムでサポートされていません。

ファイルディスクリプターの使用量（`process_open_fds`）が多く、プロセスの上限である`process_max_fds`に近い場合は、ファイルディスクリプターが枯渇する可能性があります。枯渇すると、新しいWALファイルを作成できないため、etcdがパニックを起こす場合があります。

## 自動生成されたメトリクス一覧 {#generated-list-of-metrics}

[go-grpc-prometheus]: https://github.com/grpc-ecosystem/go-grpc-prometheus
[prometheus]: https://prometheus.io/
[prometheus-getting-started]: https://prometheus.io/docs/introduction/getting_started/
[prometheus-naming]: https://prometheus.io/docs/practices/naming/
[v2-http-metrics]: https://etcd.io/docs/v2.3/metrics/#http-requests
