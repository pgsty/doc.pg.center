---
title: "他のツールとの統合"
linkTitle: "ツール統合"
weight: 150
icon: fas fa-puzzle-piece
description: "Patroni を外部のバックアップおよびオーケストレーションツールと統合する。"
module: [PATRONI]
categories: [概念]
aliases: [/patroni/tools_integration/]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni は、スタック内の他のツールと統合できます。このセクションでは、Patroni が他のツールと統合する方法についてのアイデアを提供する例を示します。ただし、すべての例を網羅しているわけではありません。

--------

## Barman {#barman}

Patroni は `patroni_barman` というアプリケーションを提供しており、`pg-backup-api` と通信するためのロジックを備えているため、リモートで Barman 操作を実行できます。

このアプリケーションには現在、いくつかのサブコマンドがあります：`recover` と `config-switch`。

### patroni_barman recover {#patroni_barman-recover}

`recover` サブコマンドは、カスタムブートストラップまたはカスタムレプリカ作成方法として使用できます。詳細については、[replica_imaging_and_bootstrap](/ja/docs/patroni/replica_bootstrap#replica_imaging_and_bootstrap) を参照してください。

### patroni_barman config-switch {#patroni_barman-config-switch}

`config-switch` サブコマンドは、Patroni における `on_role_change` コールバックとして使用されるように設計されています。たとえば、現在のプライマリーから Barman ホストへの WAL のストリーミングを実行しているとします。クラスターでのフェイルオーバーが発生した場合、新しいプライマリーから WAL のストリーミングを開始したいとします。この目的を達成するには、`patroni_barman config-switch` を `on_role_change` コールバックとして使用できます。

> [!NOTE]
> このサブコマンドは、`barman config-switch` コマンドに依存しており、このコマンドは既定のモデルをサーバーの設定に適用することで、Barman サーバーの設定を上書きする役割を担います。このコマンドは Barman 3.10 以降で利用可能です。詳細については Barman のドキュメントを参照してください。

この例は、Patroni ノードがプライマリーに昇格した場合に、設定モデルを適用する方法を示しています。

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
> `patroni_barman config-switch` では、Barman と `pg-backup-api` を Barman ホストに設定しておく必要があります。これにより、バックアップ API を通じてリモート `barman config-switch` を実行できるようになります。また、事前に適用するための Barman モデルを設定しておく必要があります。上記の例では利用可能なパラメータの一部を使用しています。詳細な情報は `patroni_barman config-switch --help` を実行するか、Barman のドキュメントを参照してください。
