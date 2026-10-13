---
title: "よくある質問"
weight: 1200
description: "よくある質問と回答"
icon: fa-solid fa-circle-question
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/faq.md"
aliases: [/etcd/faq/]
---

## etcdの概要 {#etcd-general}

### etcdとは何ですか？ {#what-is-etcd}

etcdは、整合性のある分散キー・バリューストアです。主に分散システム内で、独立した協調サービスとして使用されます。全体をメモリーに収められる少量のデータを保持するように設計されています。

### etcdはどう発音しますか？ {#how-do-you-pronounce-etcd}

etcdの発音は**/ˈɛtsiːdiː/**で、「分散した`etc`ディレクトリ」を意味します。

### クライアントはetcdのリーダーにリクエストを送る必要がありますか？ {#do-clients-have-to-send-requests-to-the-etcd-leader}

[Raft][raft]はリーダーを基盤とする仕組みで、クラスターのコンセンサスが必要なクライアントリクエストはすべてリーダーが処理します。ただし、クライアントはどのノードがリーダーかを知る必要はありません。コンセンサスが必要なリクエストをフォロワーに送信すると、自動的にリーダーへ転送されます。コンセンサスを必要としないリクエスト（直列化可能読み取りなど）は、どのクラスターメンバーでも処理できます。

## 設定 {#configuration}

### listen-<client,peer>-urls、advertise-client-urls、initial-advertise-peer-urlsの違いは何ですか？ {#what-is-the-difference-between-listen-clientpeer-urls-advertise-client-urls-or-initial-advertise-peer-urls}

`listen-client-urls`と`listen-peer-urls`は、etcdサーバーが着信接続を受け付けるためにバインドするローカルアドレスを指定します。すべてのインターフェースのポートで待ち受けるには、待ち受けIPアドレスに`0.0.0.0`を指定します。

`advertise-client-urls`と`initial-advertise-peer-urls`は、etcdクライアントや他のetcdメンバーがetcdサーバーに接続する際に使用するアドレスを指定します。通知するアドレスは、リモートマシンから到達可能でなければなりません。`localhost`や`0.0.0.0`などはリモートマシンから到達できないため、本番環境では通知しないでください。

### `--listen-peer-urls`や`--initial-advertise-peer-urls`を変更しても、`etcdctl member list`に表示されるピアURLが更新されないのはなぜですか？ {#why-doesnt-changing---listen-peer-urls-or---initial-advertise-peer-urls-update-the-advertised-peer-urls-in-etcdctl-member-list}

メンバーが通知するピアURLは、クラスターの初回起動時の`--initial-advertise-peer-urls`から取得されます。メンバーを起動した後に待ち受けピアURLや初期通知ピアURLを変更しても、外部に通知するピアURLは変わりません。メンバーシップ設定のスプリットブレインを避けるため、変更にはクォーラムの合意が必要だからです。メンバーのピアURLを更新するには、`etcdctl member update`を使用します。

## デプロイ {#deployment}

### システム要件 {#system-requirements}

etcdはデータをディスクに書き込むため、その性能はディスクの性能に大きく依存します。このため、SSDを強く推奨します。ディスクがetcdにとって十分に高速かどうかを評価する方法の1つは、[fio][fio]などのディスクベンチマークツールを使用することです。実施例は[こちら][fio-blog-post]を参照してください。性能低下やキー・バリューストアへの意図しない過負荷を防ぐため、etcdは設定可能なストレージサイズのクォータを適用します。デフォルトは2GBです。スワップやメモリー不足を避けるには、少なくともこのクォータを賄える容量のRAMを確保することを推奨します。通常の環境で推奨される最大サイズは8GBで、設定値がこれを超える場合、etcdは起動時に警告します。CoreOSでは通常、*最低でも*デュアルコアプロセッサー、2GBのRAM、80GBのSSDを備えた専用のCoreOS Container Linuxマシンにetcdクラスターを配置しています。**性能は本質的にワークロードに依存するため、本番環境へ配置する前にテストしてください。** その他の推奨事項は[ハードウェア][hardware-setup]を参照してください。

最も安定した本番環境は、amd64アーキテクチャーのLinuxです。詳細は[対応プラットフォーム][supported-platform]を参照してください。

### クラスターのメンバー数を奇数にするのはなぜですか？ {#why-an-odd-number-of-cluster-members}

etcdクラスターの状態を更新するには、ノードの過半数、すなわちクォーラムの合意が必要です。メンバー数がnのクラスターでは、クォーラムは(n/2)+1です。奇数台のクラスターにノードを1台追加すると、クォーラムに必要なノード数は必ず増加します。マシンが増えるため改善に見えますが、クォーラムを失わずに許容できる障害ノード数は変わらず、障害が起こりうるノードだけが増えるため、耐障害性は低下します。これ以上の障害を許容できない状態のクラスターで、ノードを削除する前に追加するのは危険です。アドレスの設定ミスなどで新しいノードがクラスターに登録できない場合、クォーラムが恒久的に失われるためです。

### クラスターの最大サイズはいくつですか？ {#what-is-maximum-cluster-size}

理論上、厳密な上限はありません。ただし、etcdクラスターは7ノード以下にすることが望ましいと考えられます。etcdに似ており、Google内で長年広く利用されている[Google Chubbyロックサービス][chubby]は、5ノードでの稼働を推奨しています。5メンバーのetcdクラスターは2メンバーの障害に耐えられ、ほとんどの場合これで十分です。クラスターを大きくすると耐障害性は高まりますが、より多くのマシンにデータを複製する必要があるため、書き込み性能が低下します。

### 障害許容度とは何ですか？ {#what-is-failure-tolerance}

etcdクラスターは、メンバーのクォーラムを確保できる限り稼働します。ネットワーク分断などの一時的な障害でクォーラムが失われた場合は、ネットワークが復旧してクォーラムが回復すると、自動的かつ安全に再開します。Raftがクラスターの整合性を保証します。電源障害に備え、etcdはRaftログをディスクに永続化します。障害発生時点までログを再生し、クラスターへの参加を再開します。恒久的なハードウェア障害の場合は、[実行時の再構成][runtime reconfiguration]によってノードをクラスターから削除できます。

クラスターのメンバー数は奇数を推奨します。奇数台のクラスターは、偶数台のクラスターより少ないノード数で同じ数の障害に耐えられます。偶数台と奇数台を比較すると、その違いがわかります。

| クラスターサイズ | 過半数 | 許容できる障害数 |
|:-:|:-:|:-:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

メンバーを追加してクラスターサイズを偶数にしても、障害許容度は増えません。同様に、ネットワークが二つに分断された場合、メンバーが奇数なら、処理を継続でき、分断解消時に正しい状態の基準となる過半数の区画が必ず存在します。

### etcdはリージョン間やデータセンター間にまたがる配置で動作しますか？ {#does-etcd-work-in-cross-region-or-cross-data-center-deployments}

etcdを複数のリージョンに配置すると、メンバーが異なる障害ドメインに属するため、耐障害性が向上します。その代償として、データセンターの境界を越えるコンセンサスリクエストのレイテンシーが高くなります。etcdはコンセンサスにメンバーのクォーラムを必要とし、少なくとも過半数のメンバーがリクエストに応答しなければならないため、データセンター間のレイテンシーの影響が目立ちやすくなります。また、クラスターのデータはすべてのピアに複製する必要があるため、帯域幅のコストもかかります。

レイテンシーが長い環境では、etcdのデフォルト設定だと選出やハートビートのタイムアウトが頻発する可能性があります。高レイテンシー環境でのタイムアウトの調整は、[チューニング][tuning]を参照してください。

## 運用 {#operation}

### etcdクラスターをバックアップするにはどうすればよいですか？ {#how-to-backup-a-etcd-cluster}

etcdctlには、バックアップを作成する`snapshot`コマンドがあります。詳細は[バックアップ][backup]を参照してください。

### 異常なメンバーを削除する前に、新しいメンバーを追加すべきですか？ {#should-i-add-a-member-before-removing-an-unhealthy-member}

etcdノードを置き換える場合は、先にメンバーを削除し、その後で代わりのメンバーを追加することが重要です。

etcdは、クォーラムモデルに基づく分散コンセンサスを採用しています。提案をクラスターにコミットするには、過半数にあたる(n/2)+1メンバーの合意が必要です。提案には、キー・バリューの更新とメンバーシップの変更が含まれます。このモデルにより、スプリットブレインによる不整合の可能性を完全に排除します。その反面、クォーラムの恒久的な喪失は致命的です。

これをメンバーシップに当てはめて考えます。3メンバーのクラスターで1メンバーが停止していても、クォーラムは2で、2メンバーが稼働しているため、処理を継続できます。しかし、この3メンバーのクラスターに新しいメンバーを追加すると、4メンバーの過半数には3票が必要となり、クォーラムが3に増えます。クォーラムが増えるため、この追加メンバーによる障害許容度の改善はありません。あと1ノードで障害が起きれば、引き続きクラスターは復旧不能になります。

さらに、新しいメンバーには設定ミスやクラスターへ参加できないリスクがあります。その場合、2メンバーが停止、2メンバーが稼働している一方で、失敗した追加を取り消すメンバーシップ変更には3票が必要となり、クォーラムを回復できません。etcdはデフォルトで、このようにクラスターを停止させるおそれのあるメンバー追加を拒否します。

一方、停止したメンバーを先にクラスターのメンバーシップから削除すれば、メンバー数は2になり、クォーラムは2のままです。その後で新しいメンバーを追加しても、クォーラムは2に保たれます。そのため、新しいノードを起動できなくても、残りの稼働中のメンバーでクォーラムを確保し、その新しいメンバーを削除できます。

### etcdがメンバーシップの変更を受け付けないのはなぜですか？ {#why-wont-etcd-accept-my-membership-changes}

etcdは`strict-reconfig-check`を設定し、クォーラム喪失を招く再構成リクエストを拒否します。クォーラムを放棄するのは、特にクラスターがすでに異常な場合、非常に危険です。クォーラムを失った際、新しいメンバーを追加するためにクォーラムチェックを無効にしたくなるかもしれませんが、クラスター全体の不整合につながる可能性があります。多くのアプリケーションでは問題がさらに悪化し、最も恐ろしい例の1つに「ディスクジオメトリーの破損」があります。

### ディスクレイテンシーが急増するとetcdがリーダーを失うのはなぜですか？ {#why-does-etcd-lose-its-leader-from-disk-latency-spikes}

これは意図した動作です。ディスクレイテンシーも、リーダーが正常に動作しているかを判断する要素です。etcdクラスターの選出タイムアウトが1秒なのに、リーダーがraftログの更新をディスクへfsyncするのに1分かかるとします。リーダーが選出間隔内にハートビートの送信などのネットワークメッセージ処理を行えていても、遅いディスクを待つため新しい提案をコミットできず、実質的に利用不能です。ディスクレイテンシーによって頻繁にリーダーを失う場合は、ディスク設定やetcdの時間パラメーターの[チューニング][tuning]を試してください。

### etcdの警告「request ignored (cluster ID mismatch)」は何を意味しますか？ {#what-does-the-etcd-warning-request-ignored-cluster-id-mismatch-mean}

新しいetcdクラスターは、初期クラスター設定とユーザーが指定した一意の`initial-cluster-token`値に基づいて、新しいクラスターIDを生成します。一意のクラスターIDにより、クラスターを破損しかねないクラスター間の干渉を防ぎます。

この警告は通常、古いクラスターを解体した後、ピアアドレスの一部を新しいクラスターで再利用すると発生します。古いクラスターのetcdプロセスがまだ動いていると、新しいクラスターへの接続を試みます。新しいクラスターはクラスターIDの不一致を検出してリクエストを無視し、この警告を出力します。異なるクラスター間でピアアドレスが重複しないようにすると、多くの場合この警告は解消します。

### 「mvcc: database space exceeded」は何を意味し、どう対処すればよいですか？ {#what-does-mvcc-database-space-exceeded-mean-and-how-do-i-fix-it}

etcdの[多版同時実行制御][api-mvcc]データモデルは、キー空間の正確な履歴を保持します。`--auto-compaction-mode`と`--auto-compaction-retention`の設定などによってこの履歴を定期的にコンパクションしないと、いずれストレージ容量を使い果たします。容量が不足すると、etcdは容量クォータのアラームを発生させ、クラスターへの追加の書き込みを防ぎます。アラームが有効な間、etcdは書き込みリクエストに`mvcc: database space exceeded`エラーを返します。

空き容量不足によるクォータアラームから復旧するには、次の手順を実行します。

1. etcdの履歴を[コンパクション][maintenance-compact]します。
2. すべてのetcdエンドポイントで[デフラグメンテーション][maintenance-defragment]を行います。
3. アラームを[解除][maintenance-disarm]します。

### etcdの警告「etcdserver/api/v3rpc: transport: http2Server.HandleStreams failed to read frame: read tcp 127.0.0.1:2379->127.0.0.1:43020: read: connection reset by peer」は何を意味しますか？ {#what-does-the-etcd-warning-etcdserverapiv3rpc-transport-http2serverhandlestreams-failed-to-read-frame-read-tcp-1270012379-12700143020-read-connection-reset-by-peer-mean}

クライアント側のストリームが途中で閉じられ、サーバーがTCP RSTフラグを受信したときにgRPC側が出す警告です。たとえば、gRPCサーバーがTCPキュー内のすべてのHTTP/2フレームを処理し終える前に、クライアントが接続を閉じた場合に発生します。サーバー側で一部のデータが失われた可能性はありますが、クライアント接続がすでに閉じているなら問題ありません。

これをログに記録するのは、[古いバージョンのgRPC](https://github.com/grpc/grpc-go/issues/1362)だけです。etcdでは、[v3.2.13以降、デフォルトでDEBUGレベルのログに記録](https://github.com/etcd-io/etcd/pull/9080)するため、`--log-level=debug`フラグを有効にした場合にのみ表示されます。

## 性能 {#performance}

### etcdのベンチマークはどのように行えばよいですか？ {#how-should-i-benchmark-etcd}

[benchmarkツール][benchmark]を試してください。比較用に、現在の[ベンチマーク結果][benchmark-result]も公開されています。

### etcdの警告「apply entries took too long」は何を意味しますか？ {#what-does-the-etcd-warning-apply-entries-took-too-long-mean}

etcdメンバーの過半数がリクエストのコミットに合意した後、各etcdサーバーはリクエストをデータストアに適用し、その結果をディスクに永続化します。低速な機械式ディスクや、AmazonのEBS、GoogleのPDなどの仮想化されたネットワークディスクであっても、通常はリクエストの適用に50ミリ秒もかからないはずです。平均適用時間が100ミリ秒を超えると、etcdはエントリーの適用に時間がかかりすぎていると警告します。

この問題は通常、遅いディスクが原因です。etcdと他のアプリケーションの間でディスクの競合が発生しているか、共有仮想ディスクのようにディスク自体が遅すぎる可能性があります。ディスクの遅さが原因でないことを確かめるには、[backend_commit_duration_seconds][backend_commit_metrics]を監視し、十分な速度であることを確認します。p99の所要時間は25ms未満が目安です。ディスクが遅すぎる場合、通常はetcd専用のディスクを割り当てるか、より高速なディスクを使用すると解決します。

次に多い原因は、CPUリソースの不足です。マシンのCPU使用率が高ければ、etcdに十分な計算能力を割り当てられていない可能性があります。etcdを専用マシンに移す、cgroupsによるプロセスのリソース分離を強める、またはetcdサーバープロセスのnice値を変更して優先度を上げることで、通常は解決します。

キー空間全体の取得など、非常に多くのキーにアクセスする高コストなユーザーリクエストも、適用レイテンシーを長くする原因になります。ただし、リクエストあたりのアクセスが数百キー未満であれば、常に良好な性能が得られるはずです。

上記の方法で警告が解消しない場合は、詳細なログ、監視情報、メトリクスと、可能ならワークロード情報を添えて[Issueを作成][new_issue]してください。

### etcdの警告「failed to send out heartbeat on time」は何を意味しますか？ {#what-does-the-etcd-warning-failed-to-send-out-heartbeat-on-time-mean}

etcdは、整合性のあるデータ複製とログの実行のために、リーダーを基盤とするコンセンサスプロトコルを使用します。クラスターメンバーは1つのリーダーを選出し、他のメンバーはすべてフォロワーになります。選出されたリーダーは、リーダーであり続けるために、定期的にフォロワーへハートビートを送信しなければなりません。フォロワーは、選出間隔内にハートビートを受信しなければリーダーに障害が発生したと判断し、選出を開始します。リーダーが稼働しているのに時間どおりにハートビートを送信できない場合、不要な選出が起きており、リソース不足が原因と考えられます。こうした一時的な障害を検出するため、リーダーがハートビート間隔2回分の送信を逃すと、etcdはハートビートを時間どおりに送信できなかったと警告します。

この問題は通常、遅いディスクが原因です。リーダーは、メタデータを付けてハートビートを送信する前に、そのメタデータをディスクに永続化しなければならない場合があります。etcdと他のアプリケーションの間でディスクの競合が発生しているか、共有仮想ディスクのようにディスク自体が遅すぎる可能性があります。ディスクの遅さが原因でないことを確かめるには、[wal_fsync_duration_seconds][wal_fsync_duration_seconds]を監視し、十分な速度であることを確認します。p99の所要時間は10ms未満が目安です。ディスクが遅すぎる場合、通常はetcd専用のディスクを割り当てるか、より高速なディスクを使用すると解決します。etcdに十分な速度があるかを判断するには、[fio][fio]などのベンチマークツールを使用できます。例は[こちら][fio-blog-post]を参照してください。

次に多い原因は、CPUリソースの不足です。マシンのCPU使用率が高ければ、etcdに十分な計算能力を割り当てられていない可能性があります。etcdを専用マシンに移す、cgroupsによるプロセスのリソース分離を強める、またはetcdサーバープロセスのnice値を変更して優先度を上げることで、通常は解決します。

遅いネットワークも、この問題の原因になります。etcdマシン間のネットワークメトリクスに長いレイテンシーや高いパケット損失率が見られる場合、etcdに十分なネットワーク容量がない可能性があります。通常はetcdメンバーを混雑の少ないネットワークへ移すと解決します。ただし、クラスターを複数のデータセンターに配置している場合は、メンバー間の長いレイテンシーが想定されます。その場合は、`heartbeat-interval`をマシン間の往復時間とおおむね同じにし、`election-timeout`を少なくとも5 * `heartbeat-interval`に調整してください。詳細は[チューニングのドキュメント][tuning]を参照してください。

上記の方法で警告が解消しない場合は、詳細なログ、監視情報、メトリクスと、可能ならワークロード情報を添えて[Issueを作成][new_issue]してください。

### etcdの警告「snapshotting is taking more than x seconds to finish ...」は何を意味しますか？ {#what-does-the-etcd-warning-snapshotting-is-taking-more-than-x-seconds-to-finish--mean}

etcdは、遅れたフォロワーを最新の状態にするため、また[バックアップ][backup]のために、キー・バリューストア全体のスナップショットを送信します。転送に時間がかかるとMTTRが増加します。クラスターが高スループットでデータを取り込んでいる場合、遅いフォロワーはスナップショットの受信が終わる前に新しいスナップショットを必要とし、ライブロックに陥る可能性があります。スナップショットの性能低下を検出するため、送信に30秒を超え、かつ1Gbps接続で想定される転送時間を超えた場合、etcdは警告します。


[api-mvcc]: /ja/docs/etcd/learning/api/#revisions
[backend_commit_metrics]: /ja/docs/etcd/metrics/#disk
[backup]: /ja/docs/etcd/op-guide/recovery/#snapshotting-the-keyspace
[benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
[benchmark-result]: /ja/docs/etcd/op-guide/performance/
[chubby]: http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[hardware-setup]: /ja/docs/etcd/op-guide/hardware/
[maintenance-compact]:  /ja/docs/etcd/op-guide/maintenance/#history-compaction-v3-api-key-value-database
[maintenance-defragment]: /ja/docs/etcd/op-guide/maintenance/#defragmentation
[maintenance-disarm]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#alarm-disarm
[new_issue]: https://github.com/etcd-io/etcd/issues/new
[raft]: https://raft.github.io/raft.pdf
[runtime reconfiguration]: /ja/docs/etcd/op-guide/runtime-configuration/
[supported-platform]: /ja/docs/etcd/op-guide/supported-platform/
[tuning]: /ja/docs/etcd/tuning/
[wal_fsync_duration_seconds]: /ja/docs/etcd/metrics/#disk
