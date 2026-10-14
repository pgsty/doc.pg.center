---
title: "データ破損"
weight: 5000
description: "etcdのデータ破損とリカバリー"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/data_corruption.md"
---

etcdには、メンバー間で状態が分岐することを防ぐため、データ破損の自動検出機能が組み込まれています。

> [!NOTE]
> etcd 3.7では、以下のフィーチャーゲートと時間間隔フラグを使用してください。以前の実験的なデータ破損チェック用フラグは削除されています。[設定オプション](/ja/etcd/op-guide/configuration/#feature-gates)を参照してください。

## データ破損検出の有効化 {#enabling-data-corruption-detection}

データ破損は、次の方法で検出できます。
* 初期チェック。`--feature-gates=InitialCorruptCheck=true`フラグで有効にします。
* 次の定期チェック。
  * コンパクション済みリビジョンのハッシュ。`--feature-gates=CompactHashCheck=true`フラグで有効にします。
  * 最新リビジョンのハッシュ。`--corrupt-check-time`フラグで有効にします。

初期チェックは、etcdメンバーのブートストラップ中に実行します。
メンバーは自身の永続状態をほかのメンバーと比較し、不一致があれば終了します。

両方の定期チェックは、稼働中のクラスターでリーダーが実行します。
リーダーは自身の永続状態をほかのメンバーと比較し、不一致があればCORRUPT ALARMを発報します。
両チェックの目的は同じですが、性能と検出までの時間のバランスを取るため、両方を有効にする価値があります。
* コンパクション済みリビジョンのハッシュチェック - 定期的なコンパクションが必要です。性能への負荷はごく小さく、遅いフォロワーにも対応します。
* 最新リビジョンのハッシュチェック - 性能への負荷が高く、遅いフォロワーや頻繁なコンパクションには対応しません。

### コンパクション済みリビジョンのハッシュチェック {#compacted-revision-hash-check}

`--feature-gates=CompactHashCheck=true`フラグで有効にすると、1分ごとにチェックを実行します。
間隔は`--compact-hash-check-time`フラグで調整できます。形式は`1m`が毎分、`1h`が毎時です。
このチェックはコンパクション処理を拡張し、クラスターメンバー間で比較できるチェックサムも計算します。
データベースの追加スキャンを行わないため負荷は非常に小さいものの、クラスターで定期的にコンパクションを行う必要があります。

### 最新リビジョンのハッシュチェック {#latest-revision-hash-check}

`--corrupt-check-time`フラグで有効にします。実行間隔の指定が必要で、形式は`1m`が毎分、`1h`が毎時です。
性能への負荷が高いため、数時間の間隔を推奨します。
チェックでは、指定リビジョンのetcdの全内容をスキャンしてチェックサムを計算する必要があります。

## 破損したメンバーのリストア {#restoring-a-corrupted-member}

破損したメンバーをリストアする方法は3つあります。
* メンバーの永続状態を消去する
* メンバーを置き換える
* クラスター全体をリストアする

破損したメンバーをリストアした後、CORRUPT ALARMを解除できます。

### メンバーの永続状態の消去 {#purge-member-persistent-state}

次の手順でメンバーの状態を消去できます。
1. etcdインスタンスを停止します。
2. etcdのデータディレクトリをバックアップします。
3. etcdのデータディレクトリから`snap`サブディレクトリを移動します。
6. `--initial-cluster-state=existing`を指定し、`--initial-cluster`にクラスターメンバーを列挙して`etcd`を起動します。

etcdメンバーは、リーダーから最新のスナップショットをダウンロードするはずです。

### メンバーの置き換え {#replace-member}

次の手順でメンバーを置き換えられます。
1. etcdインスタンスを停止します。
2. etcdのデータディレクトリをバックアップします。
3. データディレクトリを削除します。
4. `etcdctl member remove`を実行し、クラスターからメンバーを削除します。
5. `etcdctl member add`を実行し、メンバーを再度追加します。
6. `--initial-cluster-state=existing`を指定し、`--initial-cluster`にクラスターメンバーを列挙して`etcd`を起動します。

### クラスター全体のリストア {#restore-whole-cluster}

現在のリーダーからスナップショットを保存し、すべてのメンバーにリストアすることで、クラスターをリストアできます。
リーダーに対して`etcdctl snapshot save`を実行し、[クラスターのリストア手順](/ja/etcd/op-guide/recovery/)に従ってください。
