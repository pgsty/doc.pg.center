---
title: クイックスタート
weight: 900
description: 5分足らずでetcdを起動して使い始めましょう！
icon: fa-solid fa-rocket
categories: [チュートリアル]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
---

次の手順に従って、単一メンバーのetcdクラスターをローカルにインストールし、実行してテストします。

 1. ビルド済みのバイナリーまたはソースからetcdをインストールします。詳細は[インストール][Install]を参照してください。

    > [!WARNING]
    > **重要**：インストール手順の最後のステップを必ず実行し、`etcd`が検索パスに含まれていることを確認してください。

 2. `etcd`を起動します。

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **注意**：`etcd`の出力は[ログ](/ja/etcd/op-guide/configuration/#logging)です&mdash;infoレベルのログは無視できます。

 3. **別のターミナル**から、`etcdctl`を使用してキーを設定します。

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. 同じターミナルからキーを取得します。

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## 次のステップ {#whats-next}

etcdの構成方法と使用方法について、詳しくは次のページを参照してください。

- 開発者向け：
  - gRPC [API][api]を確認します。
  - [言語バインディングとツール][integrations]を探します。

- 運用担当者または管理者向け：
  - [複数マシンのクラスター][clustering]をセットアップします。
  - etcdの[構成方法][configure]を学びます。
  - TLSを使用して[etcdクラスターを保護][security]します。
  - [etcdをチューニング][tuning]します。

[api]: /ja/etcd/learning/api
[clustering]: /ja/etcd/op-guide/clustering
[configure]: /ja/etcd/op-guide/configuration
[integrations]: /ja/etcd/integrations
[security]: /ja/etcd/op-guide/security
[tuning]: /ja/etcd/tuning
[Install]: /ja/etcd/install/
