---
title: etcdの永続ストレージファイル
weight: 2650
description: "永続ストレージの形式とファイルのリファレンス"
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/persistent-storage-files.md"
---

このドキュメントでは、etcdの永続ストレージの形式、つまり命名、内容、開発者が内容を調べるためのツールを説明します。今後、ストレージモデルの変更に合わせて内容を拡充することを想定しています。etcd開発者のデータリカバリーに役立つことを目的としています。


## 前提知識 {#prerequisites}

次の記事は、このドキュメントを読むための背景知識として役立ちます。

* [etcdのデータモデルの概要](/ja/etcd/learning/data_model/)
* [Raftの概要](https://raft.github.io/raft.pdf)（特に「5.3 ログの複製」のセクション）。


## 概要 {#overview}

### 長期間保持されるファイル {#long-leaving-files}

<table>
  <tr>
    <th>ファイル名</th>
    <th>主な用途</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>bboltの<a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a></strong>です。適用済みのすべてのデータ、メンバーシップの認可情報、メタデータを保存します。最後に適用したWALログのインデックス（<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>）を把握しています。
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        定期的に作成する<strong>旧v2ストアのスナップショット</strong>で、次を含みます。
        <ul>
          <li>基本的なメンバーシップ情報</li>
          <li>etcd-version</li>
        </ul>
      </p>
      <p>etcd v3以降、その内容は/snap/dbファイルの内容と重複しています。</p>
      <p>定期的（<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>）にファイルを<a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">削除</a>し、直近の<code>--max-snapshots=5</code>個を保持します。</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>レプリカが大きく遅れた場合に、etcdリーダーから<strong>ダウンロードする完全なbboltスナップショット</strong>です。</p>
      <p>内容の種類は、<code>./member/snap/db</code>ファイルと同じです。</p>
      <p>
        このファイルは、次の2つの場合に使用します。
        <ul>
          <li>スナップショットからのリカバリーを求める、リーダーの要求に応じる場合。</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">サーバーの起動時</a>に、最後のスナップショット（.snap.dbファイル）が見つかり、そのインデックスが現在の<code>snap.db</code>ファイルのconsistent_indexより新しいと分かった場合。</li>
        </ul>
        注意：各レプリカが定期的に生成するスナップショットは、*.snapファイルとしてだけ出力され、snap.dbファイルにはなりません。そのため、WALログ内の最新のスナップショットに、対応する*.snap.dbファイルがあるとは限りません。ただし、その場合はバックエンド（snap/db）がスナップショットより新しいはずです。
      </p>
      <p>
        このファイルは、<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">リカバリーが完了しても削除されません</a>（全内容が./member/snap/dbファイルに反映されます）。定期的（<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>）にファイルを<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">削除します</a>。
ここでも、直近の<code>--max-snapshots=5</code>個を保持します。これらのファイルはO(GBs)のサイズになる可能性があるため、ディスク領域が枯渇するおそれがあります。
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Raftの先行書き込みログ</strong>で、Raftが受け付けた最近のトランザクション、定期的なスナップショット、CRCレコードを含みます。</p>
      <p>直近の<code>--max-wals=5</code>個のファイルを保持します。各ファイルのサイズは<code>~64*10^6</code>バイトです。この固定サイズを超えた時点でファイルを分割するため、実際のサイズは少し超えることがあります。そのため、事前に割り当てる<code>0.tmp</code>だけでは、ディスク容量の超過を完全には防げません。</p>
      <p>スナップショットの作成頻度が低すぎると、<code>--max-wals=5</code>を超えるファイルが残ることがあります。ファイルシステムのロックが、早すぎる削除を防ぐためにファイルを保護しているためです。</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      次の先行書き込みログファイルのために<strong>事前に割り当てる領域</strong>です。
      WALログの容量不足により、アラームを発報することもできずにRaftが停止するのを防ぎます。
    </td>
  </tr>
</table>


### 一時ファイル {#temporary-files}

etcdの内部処理中には、短時間だけ存在する次のようなファイルが見られることがあります。

<table>
  <tr>
    <th>ファイル</th>
    <th>主な用途</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>スナップショットファイルを<a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">読み込めない</a>場合、ファイル名を‘broken’に変更します。<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>最新のファイルの読み込みは、etcdの<a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">起動時</a>に試みます。</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>または、etcdctlのbackup/migrateコマンド実行時にも行います。</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p>リーダーのmsgSnapリクエスト、つまり指定したスナップショットからストレージをリカバリーする要求に応じて、レプリカ上に作成する<a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">一時的な</a>bboltファイルです。</p>
      <p>
        内容の取得が正常に完了すると、ファイルを<a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">リネーム</a>し、<code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>にします。ファイルのダウンロード中にサーバーが停止したり強制終了されたりすると、ファイルはディスク上に残り、自動的には削除されません。サイズはGB単位になることがあります。
      </p>
      <p><a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>を参照してください。<strong>etcd 3.5で修正されています。</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">デフラグメンテーション処理</a>中に、バックエンドの内容（/member/snap/db）のコピーを保持する一時ファイルです。処理が正常に完了すると、/member/snap/dbにリネームし、元のバックエンドを置き換えます。</p>
      <p>etcdサーバーの起動時に、これらのファイルを<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">削除します</a>。</p>
    </td>
  </tr>
</table>

## bbolt b+tree: **member/snap/db** {#bbolt-btree-membersnapdb}

このファイルは、Raftログの特定の時点まで適用された、etcdの主要な内容を保持します（[consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)を参照）。


### 物理的な構成 {#physical-organization}

bboltストレージは、物理的には[b+tree](https://en.wikipedia.org/wiki/B%2B_tree)として構成されます。b-treeの物理ページをその場で変更することはありません[^1]。代わりに、空きページ一覧から回収した新しいページへ内容をコピーし、古いページにアクセスする可能性のある未終了のトランザクションがなくなった時点で、そのページを空きページ一覧に追加します。この処理により、未終了のROトランザクションは、一貫した過去のストレージ状態を参照できます。RWトランザクションは排他的であり、他のすべてのRWトランザクションをブロックします。  \
大きな値は、複数の連続したページに保存します。ページの回収処理と、異なる大きさの連続したページ領域を割り当てる必要性が組み合わさり、bboltストレージの断片化が進むことがあります。

bboltファイルが自動で縮小することはありません。デフラグメンテーション時にだけ、末尾に一定の空きページ領域を確保した、サイズを切り詰めた新しいファイルに書き換えられます。


### 論理的な構成 {#logical-organization}

bboltストレージはバケットに分かれています。各バケットには、キー（byte[]->value byte[]のペア）を辞書順に保存します。以下は、etcd（バージョン3.5時点）で使用するバケットとキーの一覧です。

<table>
  <tr>
    <th>バケット</th>
    <th>キー</th>
    <th>値の例</th>
    <th>説明</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>いずれかのメンバーで問題が検出されたことを示します。</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code>（空）または<code>BigEndian.PutUint64</code></td>
    <td>
      <p>RolesまたはUsersを変更すると、トランザクションのコミット時にこのフィールドが増加します。</p>
      <p>
        この値は、認可処理中の<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">楽観的ロックにだけ</a>使用します。
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>文字列の[roleName]</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code>をマーシャリングした値</td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>文字列の[userName]</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code>をマーシャリングした値</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code>（文字列）</td>
    <td>コンセンサスで合意した共通ストレージバージョンの<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">マイナー</a>バージョンです。</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>直近の<code>Downgrade RPC</code>リクエストで設定された意図を永続化します。</p>
      <p>v3.5以降</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId]を<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}でエンコードしたものです。</p>
      <p>キー・バリューの削除は、末尾に't'を付けてマーシャリングします（「トゥームストーン」として）。</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a>をマーシャリングしたproto（<code>key, create_rev, mod_rev, version, value, lease id</code>）</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a>をマーシャリングしたproto（ID, TTL, RemainingTTL）</td>
    <td>
      <p>注意：LeaseCheckpointが延長するのはRemainingTTLだけです。TTLは元のGrantの値です。</p>
      <p style="text-decoration:underline;">注意2：TTLは、未定義の「現在」からの秒数として永続化します。クラッシュを繰り返すサーバーは、リースを解放しません！！！</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId]を16進数の文字列にしたもの：<code>"8e9e05c52164694d"</code></td>
    <td>
      <em>JSON文字列にシリアライズした<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">Member</a>構造体：</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>合意済みのクラスターのメンバーシップ情報です。</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId]を16進数の文字列にしたもの：<code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>削除されたすべてのメンバーのIDです。削除済みのメンバーが、同じIDで再び追加されないことを確認するために使います。</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">このフィールドは現在（3.4）、V2ストアから読み取り、V3からは読み取りません</a>。<a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a>を参照してください。</p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>uint64のバイト列（BigEndian）</td>
    <td>bolt DBストレージに最後に適用したWALエントリーのオフセットを表します。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}でエンコードした値（16バイト）</td>
    <td>コンパクションリクエストの後にクラッシュした場合に、コンパクションを再初期化するために使います。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}でエンコードした値（16バイト）</td>
    <td>ストアで直近にコンパクションが正常に完了したリビジョン（<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>）</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">etcd 3.5以降</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">etcd 3.5以降</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### ツール {#tools}


#### bbolt {#bbolt}

bboltには、ファイルの内容を調べるためのコマンドラインツールがあります。

使用例：

##### 指定したbboltファイルのすべてのバケットを列挙する {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### 特定のキー・バリューペアを読み取る {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-dbは、etcd v3のバックエンド（bbolt）の内容を列挙するために使用できます。

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

その他の例は、[https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)を参照してください。


## WAL：先行書き込みログ {#wal-write-ahead-log}

先行書き込みログは、提案を保存するためのRaftの永続ストレージです。リーダーはまず自分のログに提案を保存し、その後、Raftプロトコルでフォロワーに並行して複製します。各フォロワーは、リーダーに複製の完了を応答する前に、自身のWALに提案を永続化します。

etcdで使用するWALログは、標準的なRaftモデルと次の2点で異なります。

* インデックス付きのエントリーだけでなく、Raftの軽量なスナップショットとhard-stateも永続化します。そのため、WALログだけで、そのメンバーのRaft状態全体をリカバリーできます。
* 追記専用です。エントリーをその場で上書きせず、ファイルに後から追記した同じインデックスのエントリーが、以前のエントリーを置き換えます。


### ファイル名 {#file-names}

WALログファイルは、次のパターンで命名します。

```
"%016x-%016x.wal", seq, index
```

例：`./member/wal/0000000000000010-00000000000bf1e6.wal`

つまり、ファイル名には次の情報が16進数で含まれます。


* WALログファイルの連番
* ファイル内の最初のエントリーまたはスナップショットのインデックス
  特に、最初のファイル“0000000000000000-0000000000000000.wal”には、index=0の初期スナップショットレコードが含まれます。

### 物理的な内容 {#physical-content}

WALログファイルは、一連の「[フレーム](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)」を含みます。各フレームには、次のものが含まれます。


1. マーシャリングした[walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11)（3）の長さを格納する、[LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2]でエンコードしたuint64。
2. パディング：フレーム全体のサイズを整列（mod 8）させるための、必要な数の0バイト。
3. マーシャリングした[walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11)のデータ：
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - 下記のdataフィールドの解釈を決める、intでエンコードされた列挙値。
    2. data - typeによって異なり、通常はマーシャリングしたproto。
    3. crc - WALログの作成以降、このレプリカ上のすべてのログレコードの“data”フィールドを連結したもの（typeは含まない）のCRC-32チェックサム。CRCは、Raftでコミットされなかったものも含め、すべてのレコードを対象とすることに注意してください。

現在のファイルが<code>64*10^6</code>バイトを超えると、ファイルを「分割」し、新しいファイルを開始します。


### 論理的な内容 {#logical-content}

先行書き込みログファイルは、論理的には次を含みます。

* `Raftpb.Entry: `Raftリーダーが複製した最近の提案です。一部は「コミット済み」と見なされ、残りは論理的に上書きされる可能性があります。
* `Raftpb.HardState(term,commit,vote): `「コミット済み」、つまり過半数のサーバーに複製されたログエントリーのインデックスに関する、定期的で非常に頻繁な情報です。このエントリーは、変更・上書きされないことが保証され、バックエンド（v2、v3）に適用できます。また、選挙に関する変更があったかを示す“term”と、現在の任期でこのレプリカが投票したメンバーを表すvoteも含みます。
* `walpb.Snapshot(term, index): `Raft状態の定期的なスナップショットです。DBの内容は含まず、スナップショットのログインデックスとRaftの任期だけを保持します。
    * V2ストアの内容は、別の*.storeファイルに保存します。
    * V3ストアの内容はbboltファイルに保持し、エントリーが適用されると、その内容が暗黙のスナップショットになります。
* crc32チェックサムレコード（各ファイルの先頭）。ファイルの残りの部分のCRC検査を再開するために使用します。
* `etcdserverpb.Metadata(node_id, cluster_id)` - ログが表すクラスターとレプリカを識別します。

各WALログファイルは、次の順序で構成されます。

1. CRC-32フレーム。それ以前のすべてのファイルからの累積crcで、最初のファイルでは0です。
2. Metadataフレーム（クラスターとレプリカのID）
3. 最初のWALファイルの場合だけ：

    * 空のSnapshotフレーム（Index:0, Term: 0）。
      すべてのエントリーに「先行する」スナップショットがある、という不変条件を維持するためのフレームです。

   最初以外のWALファイル（2番目以降）の場合：

    * HardStateフレーム。

4. entry、hard-state、snapshotレコードの混在

WALログは、同じインデックスのエントリーを複数含むことがあります。これは、[Raftの論文](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf)の図7で説明される状況で発生します。etcdのWALログは追記専用なので、同じインデックスの新しいエントリーを追記することで、以前のエントリーを上書きします。

特に、WALの読み取り時には、[古いエントリーを新しいエントリーで上書きする処理](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462)が行われます。そのため、entry.index &lt;= HardState.commitを満たすエントリーの最後のバージョンだけが確定済みと見なせます。index > HardState.commitのエントリーは変更される可能性があります。

WALログの“term”は、単調であることが想定されています。

WALログのインデックスには、次の性質が想定されています。

1. いずれかのスナップショットから始まる。
2. 同じ‘term’に属する間は、そのスナップショット以降、順に増加する。
3. 任期が変わるとインデックスが減少することもあるが、新しい値は、最新のHardState.commitより大きい。
4. index >= HardState.commitを満たす任意のインデックスで新しいスナップショットが作られることがあり、そこからインデックスの新しい列が始まる。


![etcdの永続ストレージファイル](/etcd/learning/img/persistent-storage-files-figure-01.png)


### ツール {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

etcdのWALログは、[etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs)ツールで読み取れます。

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

次の点に注意してください。

* このツールが表示するのはEntriesだけです。WALログファイル内のすべてのレコード（Snapshots、HardStates）を表示するわけではありません。
* エントリーの「上書き」は自動的に適用されます。同じインデックスの新しいエントリーで上書きされた場合、このツールは最後の値だけを表示します。
* このツールは、ログ末尾の未コミットのエントリーも表示します。HardState.commitIndexの情報は表示しないため、エントリーが確定済みかどうかは分かりません。


## ストアV2のスナップショット：**member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### ファイル名 {#file-names-1}

**member/snap/{term}-{index}.snap**

ファイル名は[ここ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78)で、`("%016x-%016x.snap") `の形式で生成されます。16進数でエンコードした次の2つの要素を使います。


* term -> スナップショット出力時のRaftの任期（選挙間の期間）
* index -> スナップショット出力時に最後に適用した提案のインデックス

### 作成 {#creation}

*.snapファイルは、[Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68)メソッドによって作成されます。

このファイルの作成には、次の2つの契機があります。


* およそ--snapshot-count=（v3.7.0のデフォルトは10,000）件の提案を適用するたびに、新しいファイルを作成します。提案をバッチで受け取り、バッチの最後でのみスナップショットの作成を検討し、最終的な作成処理も非同期でスケジュールするため、件数は概数です。
  --snapshot-countというフラグ名は、かなり誤解を招きやすいものです。制御するのは、[最後のスナップショットのインデックスと、最後に適用した提案のインデックスとの差](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)だからです。
* Raftがレプリカに、スナップショットからのリストアを要求した場合です。レプリカはネットワークでスナップショット（msgSnapメッセージ）を受信すると、WALログにも軽量なチェックポイントとして記録します。これにより、WALログの末尾には、常に有効なスナップショットがあり、その後にエントリーが続くことが保証されます。これによって、WALログに連続性の欠落が生じるのを防ぎます。

現在、このファイルはWALログのSnapshotエントリーと、おおむね[^3]1-1で対応しています。v2ストアの廃止に伴い、ファイルの書き込みは完全に停止される見込みです（3.5.xでは任意、3.6.xでは必須）。


### 内容 {#content}

ファイルは、マーシャリングした[snapdb.snapshot proto](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)`を含みます。

その'data'フィールドには、[Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31)が格納されます。

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata),

最後に、入れ子になったdataには、JSONにシリアライズした[v2ストアの内容](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files)が格納されます。


具体的には、次の内容を含みます。

* Term
* Index
* メンバーシップのデータ：
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* ストレージのバージョン：/0/version-> 3.5.0


### ツール {#tools-2}


#### protoc {#protoc}

etcdのルートディレクトリで次のコマンドを実行すると、ファイルの内容を確認できます。


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


同様に、'data'フィールドを取り出し、[Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31)としてデコードできます。


### etcd 3.4の*.snapファイルにある、JSONにシリアライズしたv2ストアの内容の例 {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

```json
{
  "Root":{
    "Path":"/",
    "CreatedIndex":0,
    "ModifiedIndex":0,
    "ExpireTime":"0001-01-01T00:00:00Z",
    "Value":"",
    "Children":{
      "0":{
        "Path":"/0",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{
          "members":{
            "Path":"/0/members",
            "CreatedIndex":1,
            "ModifiedIndex":1,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"",
            "Children":{
              "8e9e05c52164694d":{
                "Path":"/0/members/8e9e05c52164694d",
                "CreatedIndex":1,
                "ModifiedIndex":1,
                "ExpireTime":"0001-01-01T00:00:00Z",
                "Value":"",
                "Children":{
                  "attributes":{
                    "Path":"/0/members/8e9e05c52164694d/attributes",
                    "CreatedIndex":2,
                    "ModifiedIndex":2,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
                    "Children":null
                  },
                  "RaftAttributes":{
                    "Path":"/0/members/8e9e05c52164694d/RaftAttributes",
                    "CreatedIndex":1,
                    "ModifiedIndex":1,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
                    "Children":null
                  }
                }
              }
            }
          },
          "version":{
            "Path":"/0/version",
            "CreatedIndex":3,
            "ModifiedIndex":3,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"3.5.0",
            "Children":null
          }
        }
      },
      "1":{
        "Path":"/1",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{


        }
      }
    }
  },
  "WatcherHub":{
    "EventHistory":{
      "Queue":{
        "Events":[
          {
            "action":"create",
            "node":{
              "key":"/0/members/8e9e05c52164694d/RaftAttributes",
              "value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
              "modifiedIndex":1,
              "createdIndex":1
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/members/8e9e05c52164694d/attributes",
              "value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
              "modifiedIndex":2,
              "createdIndex":2
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/version",
              "value":"3.5.0",
              "modifiedIndex":3,
              "createdIndex":3
            }
          }
        ]
      }
    }
  }
}
```

## 変更 {#changes}

このセクションは、etcdのバージョン間で導入されたファイル形式の変更を記載するために設けています。

[^1]:
     bboltファイルの先頭にあるメタデータページは、その場で変更されます。

[^2]:
     uintの大半はビッグエンディアンで書き込まれるため、一貫していません。

[^3]:
     WALログの先頭にある初期スナップショット（index:0）には、対応する*.snapファイルがありません。また、古い*.snapファイルやWALログは削除されることがあります。
