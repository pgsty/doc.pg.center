---
title: etcd v3のベンチマーク
weight: 5375
description: etcd v3の性能測定
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
aliases: [/etcd/benchmarks/etcd-3-demo-benchmarks/]
---

## 物理マシン {#physical-machines}

GCE n1-highcpu-2マシンタイプ

- /var/lib/etcdにマウントした専用ローカルSSD × 1
- OS用の専用低速ディスク × 1
- メモリー1.8 GB
- CPU × 2
- etcdバージョン2.2.0

## etcd クラスター {#etcd-cluster}

v3デモモードで稼働するetcdメンバー1つ

## テスト {#testing}

[etcd v3ベンチマークツール][etcd-v3-benchmark]を使用します。

## 性能 {#performance}

### 単一キーの読み取り {#reading-one-single-key}

| キーサイズ（バイト） | クライアント数 | 読み取りQPS | 90パーセンタイルのレイテンシー（ms） |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2716  | 0.4      |
| 256               | 64                | 16623 | 6.1      |
| 256               | 256               | 16622 | 21.7     |

空のサーバーハンドラーを使用した場合と、ほぼ同じ性能です。

### 書き込み後の単一キーの読み取り {#reading-one-single-key-after-putting}

| キーサイズ（バイト） | クライアント数 | 読み取りQPS | 90パーセンタイルのレイテンシー（ms） |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2269  | 0.5      |
| 256               | 64                | 13582 | 8.6      |
| 256               | 256               | 13262 | 47.5     |

空のサーバーハンドラーを使用した場合、1回のputによって性能は変わりません。したがって、性能低下の原因はストレージパッケージにあると考えられます。

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
