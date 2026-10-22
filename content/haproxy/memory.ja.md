---
title: "6. メモリ管理"
linkTitle: "6. メモリ"
weight: 300
description: "メモリ割り当て、制限、プール、バッファ、プロセスのサイジング"
icon: fa-solid fa-memory
module: [HAPROXY]
categories: [タスク]
aliases:
  - /haproxy/management/memory/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 6"
---

HAProxyは、単純で高速なプール方式のメモリ管理を使用します。扱うオブジェクトの種類が少ないため、サイズごとにmalloc()を呼び出すより、適切なサイズのオブジェクトを持つプールから取得するほうがはるかに効率的です。プールはスタック、つまりLIFOとして構成されます。このため、新たに割り当てるオブジェクトには、解放されたばかりでCPUキャッシュにまだ残っているものを使用します。メモリの断片化を抑えるため、サイズが近いプールは統合されます。

デフォルトでは性能を重視し、解放された各オブジェクトを元のプールに戻します。すぐに再利用すると想定しているため、割り当て済みのオブジェクトのメモリは解放しません。

CLIの「show pools」コマンドで、プールのメモリ使用状況を確認できます。

```shell
> show pools
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool cache_st (16 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccc40=03 [SHARED]
  - Pool pipe (32 bytes): 5 allocated (160 bytes), 5 used, 0 failures, 2 users, @0x9ccac0=00 [SHARED]
  - Pool comp_state (48 bytes): 3 allocated (144 bytes), 3 used, 0 failures, 5 users, @0x9cccc0=04 [SHARED]
  - Pool filter (64 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 3 users, @0x9ccbc0=02 [SHARED]
  - Pool vars (80 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccb40=01 [SHARED]
  - Pool uniqueid (128 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9cd240=15 [SHARED]
  - Pool task (144 bytes): 55 allocated (7920 bytes), 55 used, 0 failures, 1 users, @0x9cd040=11 [SHARED]
  - Pool session (160 bytes): 1 allocated (160 bytes), 1 used, 0 failures, 1 users, @0x9cd140=13 [SHARED]
  - Pool h2s (208 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccec0=08 [SHARED]
  - Pool h2c (288 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cce40=07 [SHARED]
  - Pool spoe_ctx (304 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccf40=09 [SHARED]
  - Pool connection (400 bytes): 2 allocated (800 bytes), 2 used, 0 failures, 1 users, @0x9cd1c0=14 [SHARED]
  - Pool hdr_idx (416 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd340=17 [SHARED]
  - Pool dns_resolut (480 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccdc0=06 [SHARED]
  - Pool dns_answer_ (576 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccd40=05 [SHARED]
  - Pool stream (960 bytes): 1 allocated (960 bytes), 1 used, 0 failures, 1 users, @0x9cd0c0=12 [SHARED]
  - Pool requri (1024 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd2c0=16 [SHARED]
  - Pool buffer (8030 bytes): 3 allocated (24090 bytes), 2 used, 0 failures, 1 users, @0x9cd3c0=18 [SHARED]
  - Pool trash (8062 bytes): 1 allocated (8062 bytes), 1 used, 0 failures, 1 users, @0x9cd440=19
Total: 19 pools, 42296 bytes allocated, 34266 used.
```

プール名は目安であり、そのプールを最初に使用したオブジェクト型の名前です。括弧内のサイズは、そのプールのオブジェクトサイズです。オブジェクトサイズは常に16バイトの倍数に切り上げられます。現在割り当てられているオブジェクト数と総バイト数が表示されるため、どのプールが最も多くのメモリを使用しているかを簡単に把握できます。現在使用中のオブジェクト数は「used」フィールドに表示されます。"allocated"と"used"の差は、解放済みですぐに再利用できるオブジェクトの数です。行末のアドレスはプールのアドレスで、続く数値はプールのインデックスです。インデックスが割り当てられていなければ-1と表示されます。

コマンドラインオプション「-m」に続けてメガバイト数を指定すると、プロセスごとに割り当てるメモリ量を制限できます。プロセスがアドレス指定できる空間全体が対象となるため、一部のライブラリやスタックが使うメモリも含まれますが、リソースに制約のあるシステムでは確実な上限として利用できます。「ulimit -v」があるシステムではそれと同じように、それ以外では「ulimit -d」と同じように機能します。

メモリ上限に達した場合やシステムのメモリが不足した場合に割り当てが失敗すると、haproxyはまずすべてのプールから未使用のオブジェクトをすべて解放し、その後メモリの割り当てを再試行します。この未使用メモリの解放処理は、haproxyプロセスにSIGQUITシグナルを送ることでも実行できます。

リロード時にグレースフルシャットダウン状態に移ったプロセスは、接続を解放するたびに自動的にメモリの解放処理も行います。これにより、解放可能なメモリをすべて解放し、新しいプロセスが利用できるようにします。
