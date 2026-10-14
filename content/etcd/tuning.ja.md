---
title: "チューニング"
weight: 1450
description: "ハートビート間隔と選出タイムアウトの設定を調整するタイミング"
icon: fa-solid fa-sliders
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tuning.md"
---

etcdのデフォルト設定は、平均ネットワークレイテンシーが低いローカルネットワークであれば、通常は問題なく機能します。ただし、複数のデータセンターにまたがる環境やレイテンシーの高いネットワークでetcdを使用する場合は、ハートビート間隔と選出タイムアウトの調整が必要になることがあります。

レイテンシーの原因はネットワークだけではありません。各リクエストとレスポンスは、リーダーとフォロワー双方の遅いディスクの影響を受けることがあります。それぞれのタイムアウトは、リクエストの送信から、相手のマシンから正常なレスポンスが返るまでの合計時間を表します。

## 時間に関するパラメーター {#time-parameters}

基盤となる分散コンセンサスプロトコルは、2つの独立した時間パラメーターを使い、ノードの処理が停止したりオフラインになったりした場合にリーダーを引き継げるようにしています。1つ目は*ハートビート間隔*です。リーダーがフォロワーに対して、自身が引き続きリーダーであることを通知する頻度を表します。
ベストプラクティスとして、メンバー間の往復時間に近い値を設定することを推奨します。etcdのデフォルトのハートビート間隔は`100ms`です。

2つ目は*選出タイムアウト*です。フォロワーノードがハートビートを受信しなくなってから、自らリーダーになろうとするまでの時間を表します。etcdのデフォルトの選出タイムアウトは`1000ms`です。

これらの値の調整にはトレードオフがあります。ハートビート間隔は、メンバー間の平均往復時間（RTT）の最大値に近い値、通常は往復時間の0.5～1.5倍程度を推奨します。ハートビート間隔が短すぎると、etcdは不要なメッセージを送信し、CPUとネットワークリソースの使用量が増えます。一方、ハートビート間隔が長すぎると、選出タイムアウトも長くなります。選出タイムアウトが長いほど、リーダーの障害検出に時間がかかります。往復時間（RTT）を測る最も簡単な方法は、[PINGユーティリティー][ping]を使用することです。

選出タイムアウトは、ハートビート間隔とメンバー間の平均往復時間に基づいて設定することを推奨します。ネットワークの変動を考慮できるよう、選出タイムアウトは往復時間の少なくとも10倍でなければなりません。たとえば、メンバー間の往復時間が10msの場合は、選出タイムアウトを少なくとも100msにすることを推奨します。

選出タイムアウトの上限は50000ms（50s）で、この値は世界規模に分散したetcdクラスターを配置する場合にのみ使用することを推奨します。米国本土内の妥当な往復時間は130ms、米国と日本の間では350～400ms程度です。ネットワーク性能が不均一な場合や、パケットの遅延・損失が頻繁に発生する場合は、パケットの送信を成功させるために何度か再試行が必要になる可能性があります。そのため、世界規模の往復時間の安全な上限は5sです。選出タイムアウトはブロードキャスト時間より1桁大きくすることを推奨するため、世界規模の分散クラスターで約5sの場合、50秒が妥当な上限になります。

同じクラスター内のすべてのメンバーで、ハートビート間隔と選出タイムアウトを同じ値にすることを推奨します。etcdメンバーごとに異なる値を設定すると、クラスターの安定性を損なう可能性があります。

デフォルト値はコマンドラインで上書きできます。

```sh
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

値はミリ秒単位で指定します。

## スナップショット {#snapshots}

etcdはキーに対するすべての変更をログファイルに追記します。このログは増え続け、キーに加えられたあらゆる変更の完全な一連の履歴となります。利用が少ないクラスターでは完全な履歴を保持しても問題ありませんが、頻繁に利用されるクラスターでは大きなログを抱えることになります。

ログが巨大になるのを避けるため、etcdは定期的にスナップショットを作成します。システムの現在の状態を保存し、古いログを削除することで、ログのコンパクションを行えます。

### スナップショットの調整 {#snapshot-tuning}

Raftスナップショットは、設定された数のエントリーが適用された後に作成します。etcd 3.7ではV2バックエンドを使用しません。デフォルトでは、10,000回の変更ごとに作成します。etcdのメモリー使用量とディスク使用量が多すぎる場合は、コマンドラインで次のように設定し、スナップショットのしきい値を下げてみてください。

```sh
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## ディスク {#disk}

etcdクラスターは、ディスクのレイテンシーに非常に敏感です。etcdは提案をログに永続化しなければならないため、他のプロセスによるディスク操作が`fsync`のレイテンシーを長くする場合があります。その結果、etcdがハートビートを逃し、リクエストのタイムアウトや一時的なリーダー喪失につながることがあります。etcdサーバーのディスク優先度を高くすると、こうしたプロセスと共存して安定稼働できる場合があります。

Linuxでは、`ionice`でetcdのディスク優先度を設定できます。

```sh
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

## ネットワーク {#network}

etcdのリーダーが大量のクライアントリクエストを同時に処理している場合、ネットワークの輻輳により、フォロワーピアのリクエスト処理が遅れる可能性があります。この場合、フォロワーノードに送信バッファーのエラーメッセージが表示されます。

```
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
```

クライアントのトラフィックよりもetcdのピア間トラフィックを優先することで、これらのエラーが解消する場合があります。Linuxでは、トラフィック制御の仕組みを使ってピア間トラフィックを優先できます。

```
tc qdisc add dev eth0 root handle 1: prio bands 3
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1
```

[ping]: https://en.wikipedia.org/wiki/Ping_(networking_utility)


`tc`の設定を解除するには、次のコマンドを実行します。

```
tc qdisc del dev eth0 root
```

## CPU {#cpu}

etcdはレイテンシーに非常に敏感なため、LinuxシステムではCPUガバナーをperformanceまたはconservativeモードに設定することで、さらに性能を最適化できます。

Linuxでは、次のようにCPUガバナーをperformanceモードに設定できます。
```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
