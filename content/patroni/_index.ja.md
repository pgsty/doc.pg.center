---
title: "Patroni 4.1.5ドキュメント"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "PostgreSQL向けPatroniの高可用性ドキュメントの概要。"
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [概念]
aliases: [/docs/patroni/]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> **Python 3.11+を使用する、メモリー制限のあるシステム**でのPatroniの実行

たとえば`vm.overcommit_memory=2`（PostgreSQLで推奨）を設定したような、メモリー制限が厳しいシステムでPatroniを実行し、Python 3.11以降を使用すると、予期しない動作が見られる場合があります。

- Patroniは正常に見える
- PostgreSQLは動作を継続する
- Patroniの**REST APIが応答しなくなる**
- オペレーティングシステムは、PatroniがREST APIポートでリッスンしていると報告する
- Patroniのログは正常に見える。ただし、次のメッセージが一度表示される場合がある：`Exception ignored in thread started by: <object repr() failed>`、`MemoryError`
- カーネルのログに、`not enough memory for the allocation`などのメッセージが含まれる場合がある

この動作は、[Python 3.11+のバグ](https://github.com/python/cpython/issues/140746)によって発生します。メモリーの条件が厳しく、十分な空きメモリーがない場合、新しいスレッドの起動が無期限にハングする可能性があります。

## 推奨される解決策 {#recommended-solution}

最近のPatroniリリース（4.1.1+、4.0.8+）では、システムのメモリーが逼迫する前に、起動の早い段階で必要なすべてのスレッドを開始することで、この問題の影響を軽減しています。

## 追加の推奨事項（Linux、glibc） {#additional-recommendations-linux-glibc}

`vm.overcommit_memory=2`（PostgreSQLで推奨）を設定して実行する場合は、次の環境変数を設定してPatroniを起動することも推奨します。

- `MALLOC_ARENA_MAX=1` - マルチスレッドアプリケーション向けにglibcが割り当てる仮想メモリーの量を削減する
- `PG_MALLOC_ARENA_MAX=` - Patroniが起動するPostgreSQLプロセスの`MALLOC_ARENA_MAX`の値をリセットする。

さらに、次のPatroni構成パラメーターを調整できます。

- `thread_stack_size` - Patroniが起動するスレッドで使用するスタックサイズ。この値を小さくすると、Patroniプロセスのメモリー使用量が減ります。Patroniが設定するデフォルト値は`512kB`です。Patroniでスタックに関連するクラッシュが発生する場合は、`thread_stack_size`を増やしてください。それ以外の場合はデフォルト値で十分です。
- `thread_pool_size` - リーダー選出やフェイルセーフの確認中に、Patroniが非同期タスクや他のメンバーとのREST API通信に使用するスレッドプールのサイズ。デフォルト値は`5`で、三つのノードからなるクラスターには十分です。
- `restapi.thread_pool_size` - REST APIリクエストの処理に使用するスレッドプールのサイズ。デフォルト値は`5`で、最大五つのREST APIリクエストを並行処理できます。ただし、データベース接続を一つだけ使用するため、SQLクエリーを伴うリクエストは実質的に直列化されます。そのため、この値を増やしても通常は効果がありません。

--------

Patroniは、Pythonを使用した高可用性（HA）PostgreSQLソリューションのテンプレートです。できるだけ幅広い環境で利用できるように、Patroniは[ZooKeeper](https://zookeeper.apache.org/)、[etcd](https://github.com/coreos/etcd)、[Consul](https://github.com/hashicorp/consul)、[Kubernetes](https://kubernetes.io)など、さまざまな分散構成ストアをサポートしています。データセンターをはじめ、あらゆる場所にHA PostgreSQLを迅速にデプロイしたいデータベースエンジニア、DBA、DevOpsエンジニア、SREに役立つことを期待しています。

Patroniを「テンプレート」と呼ぶのは、あらゆる状況に適合したり、導入するだけで使えたりするレプリケーションシステムとは大きく異なるためです。独自の注意点があります。十分に理解して使用してください。PostgreSQLで高可用性を実現する方法はさまざまです。一覧は[PostgreSQLドキュメント](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling)を参照してください。

現在サポートしているPostgreSQLのバージョン：9.3から18。

**Citusユーザーへの注意**：3.0以降のPatroniは、Postgresのデータベース拡張機能である[Citus](https://github.com/citusdata/citus)と円滑に連携します。Patroniの高可用性とCitusの分散クラスターを組み合わせて使用する方法については、Patroniドキュメントの[Citusサポートページ](/ja/patroni/citus#citus)を参照してください。

**Kubernetesユーザーへの注意**：PatroniはKubernetes上でネイティブに動作できます。Patroniドキュメントの[Kubernetes](/ja/patroni/kubernetes#kubernetes)の章を参照してください。

<img src="/img/docs/patroni/patroni-logo.png" width="128" height="128" alt="画像" />
