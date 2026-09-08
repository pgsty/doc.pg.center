---
title: "KubernetesでのPatroniの使用"
linkTitle: "Kubernetesでの使用"
weight: 120
icon: fas fa-dharmachakra
description: "Kubernetesのオブジェクト、ラベル、サービスディスカバリーを使用したPatroniの運用。"
module: [PATRONI]
categories: [タスク]
aliases: [/patroni/kubernetes/]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
PatroniはKubernetesオブジェクトを使用してクラスターの状態を保存し、リーダーキーを管理できます。そのため、整合性ストアを用意せずにKubernetes環境でPostgresを運用できます。つまり、追加のetcdデプロイメントを実行する必要がありません。Patroniがリーダーキーと構成キーの保存に使用できるKubernetesオブジェクトには二種類あり、`kubernetes.use_endpoints`または環境変数`PATRONI_KUBERNETES_USE_ENDPOINTS`で構成します。

--------

## Endpointsの使用 {#use-endpoints}

これは推奨モードですが、互換性のためデフォルトでは無効です。有効にすると、Patroniは作成した各`Endpoints`の`metadata: annotations`フィールドにクラスター構成とリーダーキーを保存します。リーダー情報を含むアノテーションと、実行中のリーダーPodを指す実際のアドレスを同時に一度で更新するため、`ConfigMaps`を使用する場合よりも安全にリーダーを変更できます。

--------

## ConfigMapsの使用 {#use-configmaps}

このモードでは、PatroniはEndpointsの代わりにConfigMapsを作成し、そのメタデータ内にキーを保存します。リーダーの変更には、リーダーのConfigMapと対応するEndpointに対する、少なくとも二回の更新が必要です。

トラフィックをPostgresのリーダーに向けるには、KubernetesのPostgresサービスが（Patroniの構成で設定した）`role_label`によるラベルセレクターを使用するよう構成する必要があります。

OpenShift上で実行する場合など、状況によってはConfigMapsを使用する以外に選択肢がないことに注意してください。

--------

## 構成 {#configuration}

PatroniのKubernetes用の[設定](/ja/docs/patroni/config/yaml#kubernetes_settings)と[環境変数](/ja/docs/patroni/config/env#kubernetes_environment)は、ドキュメントの一般的な章で説明しています。

<a id="kubernetes_role_values"></a>

### ロールラベルのカスタマイズ {#customize-role-label}

デフォルトでは、Patroniはノードのロールに応じて、実行中のPodに`role=primary`などの対応するラベルを設定します。ラベルのキーと値は、`kubernetes.role_label`、`kubernetes.leader_label_value`、`kubernetes.follower_label_value`、`kubernetes.standby_leader_label_value`でカスタマイズできます。

デフォルトのロールラベルから独自のラベルに移行する場合は、次の手順に従うことでダウンタイムを短縮できます。

1. `kubernetes.tmp_role_label`を使用して、元のロール値を持つ一時的なラベル（`tmp_role`など）をPodに追加します。Podを再起動すると、Patroniによって次のラベルが設定されます。

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

2. すべてのPodを更新した後、サービスのセレクターを変更して一時的なラベルを選択するようにします。

> ```yaml
> selector:
>   cluster-name: foo
>   tmp_role: primary
> ```

3. 独自のロールラベルを追加します（たとえば、`kubernetes.leader_label_value=primary`を設定します）。Podを再起動すると、Patroniによって次の新しいラベルが設定されます。

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

4. すべてのPodを再度更新した後、サービスのセレクターを変更して新しいロール値を使用するようにします。

> ```yaml
> selector:
>   cluster-name: foo
>   role: primary
> ```

5. 最後に、構成から一時的なラベルを削除し、すべてのPodを更新します。

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
> ```

--------

## 例 {#examples}

- Patroniリポジトリの[kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes)フォルダーには、PatroniのKubernetes構成をテストするためのDockerイメージとKubernetesマニフェストの例が含まれています。現在の状態では、権限の問題によりPersistentVolumesを使用できないことに注意してください。
- Persistent Volumesを使用できる、すべての機能を備えたDockerイメージは、[Spiloプロジェクト](https://github.com/zalando/spilo)にあります。
- Kubernetesで実行するPatroniを構成したSpiloイメージをデプロイするための[Helmチャート](https://github.com/kubernetes/charts/tree/master/incubator/patroni)もあります。
- PatroniとSpiloを使用してデータベースクラスターを大規模に運用する場合は、[postgres-operator](https://github.com/zalando/postgres-operator)プロジェクトを参照してください。Spiloクラスターを管理するためのOperatorパターンを実装しています。
