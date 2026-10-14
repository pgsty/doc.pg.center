---
title: "他のツールとの統合"
linkTitle: "ツール統合"
weight: 150
icon: fas fa-puzzle-piece
description: "Patroniを外部のバックアップおよびオーケストレーションツールと統合する。"
module: [PATRONI]
categories: [概念]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroniは、スタック内の他のツールと統合できます。このセクションでは、Patroniが他のツールと統合する方法についてのアイデアを提供する例を示します。ただし、すべての例を網羅しているわけではありません。

--------

## Barman {#barman}

Patroniは`patroni_barman`というアプリケーションを提供しており、`pg-backup-api`と通信するためのロジックを備えているため、リモートでBarman操作を実行できます。

このアプリケーションには現在、`recover`と`config-switch`の2つのサブコマンドがあります。

### patroni_barman recover {#patroni_barman-recover}

`recover`サブコマンドは、カスタムブートストラップまたはカスタムレプリカ作成方法として使用できます。詳細については、[レプリカの作成とブートストラップ](/ja/patroni/replica_bootstrap#replica_imaging_and_bootstrap)を参照してください。

### patroni_barman config-switch {#patroni_barman-config-switch}

`config-switch`サブコマンドは、Patroniにおける`on_role_change`コールバックとして使用されるように設計されています。たとえば、現在のプライマリーからBarmanホストへのWALのストリーミングを実行しているとします。クラスターでのフェイルオーバーが発生した場合、新しいプライマリーからWALのストリーミングを開始したいとします。この目的を達成するには、`patroni_barman config-switch`を`on_role_change`コールバックとして使用できます。

> [!NOTE]
> このサブコマンドは、`barman config-switch`コマンドに依存しており、このコマンドは事前に定義されたモデルを適用することで、Barmanサーバーの設定を上書きする役割を担います。このコマンドはBarman 3.10以降で利用可能です。詳細についてはBarmanのドキュメントを参照してください。

この例は、このPatroniノードがプライマリーに昇格した場合に設定モデルを適用するよう、Patroniを構成する方法を示しています。

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> `patroni_barman config-switch`では、Barmanと`pg-backup-api`をBarmanホストに設定しておく必要があります。これにより、バックアップAPIを通じてリモートの`barman config-switch`を実行できるようになります。また、適用するBarmanモデルを事前に設定しておく必要があります。上記の例では利用可能なパラメータの一部を使用しています。詳細な情報は`patroni_barman config-switch --help`を実行するか、Barmanのドキュメントを参照してください。
