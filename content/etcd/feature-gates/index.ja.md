---
title: "フィーチャーゲート"
weight: 1175
icon: fa-solid fa-toggle-on
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
---

<!-- overview -->
このページでは、管理者がetcdに指定できる各種フィーチャーゲートの概要を説明します。

機能の各段階については、[機能の段階](#feature-stages)を参照してください。

<!-- body -->
## 概要 {#overview}

フィーチャーゲートは、etcdの機能を表すkey=valueペアの集合です。
etcdのコマンドラインフラグ`--feature-gates`で、各機能を有効または無効にできます。

etcdでは、一連のフィーチャーゲートを有効または無効にできます。
すべてのフィーチャーゲートを確認するには、`-h`フラグを使用します。
フィーチャーゲートを設定するには、コマンドラインで`--feature-gates`フラグに機能のペアのリストを指定します。

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

または、YAML設定ファイルで`feature-gates`を指定します。

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### `embed.Config`構造体の変更 {#change-in-embedetcdserver-struct}

3.6では、`embed.Config`に`ServerFeatureGate`フィールドが追加されました。以下の実験的なフィールドは、このフィールドに置き換えることを推奨します。

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### AlphaまたはBeta機能のフィーチャーゲート {#feature-gates-for-alpha-or-beta-features}

etcdに設定できるフィーチャーゲートを、次の表にまとめます。

| 機能 | デフォルト | 段階 | 詳細 |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck | false | Alpha |リーダーがフォロワーのコンパクションハッシュを定期的に確認できるようにします。|
| InitialCorruptCheck | false | Alpha |クライアントやピアからのトラフィックを処理する前に、データの破損を確認できるようにします。|
| LeaseCheckpoint | false | Alpha |リーダーが他のメンバーに定期的にチェックポイントを送信し、リーダー変更時に残りのTTLがリセットされるのを防ぎます。|
| LeaseCheckpointPersist | false | Alpha |remainingTTLを永続化し、長期間有効なリースが無期限に自動更新されるのを防ぎます。|
| SetMemberLocalAddr | false | Alpha |ピアとの通信時に、initial-advertise-peer-urlsで最初に指定されたループバック以外のローカルアドレスを、ローカルアドレスとして使用できるようにします。|
| StopGRPCServiceOnDefrag | false | Alpha |デフラグメンテーション中、etcdのgRPCサービスがクライアントリクエストの処理を停止できるようにします。|
| TxnModeWriteWithSharedBuffer | true | Beta |書き込みトランザクションが読み取り専用の確認処理で共有バッファーを使用できるようにします。|

## 機能の使用 {#using-a-feature}

### 機能の段階 {#feature-stages}

機能の段階には、*Alpha*、*Beta*、*GA*、*Deprecated*があります。
*Alpha*の機能には、次の特性があります。

* デフォルトでは無効です。
* バグがある可能性があります。有効にするとバグが表面化する場合があります。
* 予告なく、いつでもサポートが打ち切られる可能性があります。
* 後のソフトウェアリリースで、APIが予告なく互換性のない形で変更される可能性があります。
* バグのリスクが高く、長期的なサポートもないため、
  短期間のテスト用クラスターでのみ使用することを推奨します。

*Beta*の機能には、次の特性があります。

* デフォルトで有効です。
* 十分にテストされており、有効にしても安全と考えられています。
* 詳細が変わることはあっても、機能全体のサポートが打ち切られることはありません。
* 利用が広がることで、見つけにくい新たなバグが発見される可能性があるため、
  業務上重要ではない用途に限って使用することを推奨します。

> [!NOTE]
> *Beta*機能を試し、フィードバックをお寄せください。
> Beta段階を終えた後では、それ以上の変更が現実的でなくなる可能性があります。

*一般提供*（GA）の機能は、*安定版*の機能とも呼ばれます。次の特性があります。

* 常に有効で、無効にはできません。
* 対応するフィーチャーゲートは不要になります。
* 安定版の機能は、その後の多くのバージョンのリリースでも提供されます。

*非推奨*（Deprecated）の機能には、次の特性があります。

* フィーチャーゲートは使用されなくなっています。
* 機能はGAに移行したか、削除されています。
