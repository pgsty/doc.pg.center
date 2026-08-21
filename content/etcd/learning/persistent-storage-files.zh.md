---
title: etcd 持久化存储文件
weight: 2650
description: 持久化存储格式与文件参考
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/learning/persistent-storage-files.md"
---

本文介绍了 etcd 持久化存储格式：命名规则、内容结构以及可供开发者用于检查存储内容的工具。后续应随着存储模型的变更持续扩展本文内容。本文面向 etcd 开发者，旨在帮助其满足数据恢复需求。


## 先决条件 {#prerequisites}

以下文章为本文提供了有益的背景信息：

* [etcd 数据模型概述](/zh/etcd/learning/data_model/)
* [Raft 概述](https://raft.github.io/raft.pdf)（特别是“5.3 日志复制”节）。


## 概述 {#overview}

### 长期存在的文件 {#long-leaving-files}

<table>
  <tr>
    <th>文件名</th>
    <th>主要用途</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>bbolt <a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a></strong> 用于存储所有已应用的数据、成员权限信息及元数据。它知晓最新的已应用 WAL 日志索引（<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>）。
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        定期生成的<strong>旧版 v2 存储系统快照</strong>，包含：
        <ul>
          <li>基本成员信息</li>
          <li>etcd 版本</li>
        </ul>
      </p>
      <p>自 etcd v3 起，其内容与 /snap/db 文件的内容重复。</p>
      <p>这些文件会定期（<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>）<a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">清理</a>，仅保留最近的 <code>--max-snapshots=5</code> 个。</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>如果副本严重滞后，则从 etcd 领导者下载完整的<strong>bbolt 快照</strong>。</p>
      <p>其内容类型与 <code>./member/snap/db</code> 文件相同。</p>
      <p>
        该文件用于以下两种场景：
        <ul>
          <li>响应领导者从快照恢复的请求。</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">服务器启动期间</a>，发现最后一个快照（.snap.db 文件），且其索引比当前 <code>snap.db</code> 文件中的 consistent_index 更新时。</li>
        </ul>
        请注意：每个副本定期生成的快照只以 *.snap 文件形式输出，而不是 snap.db 文件。因此，无法保证 WAL 日志中的最新快照存在对应的 *.snap.db 文件。但在这种情况下，后端（snap/db）应比快照更新。
      </p>
      <p>
        恢复完成后，该<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">文件不会被删除</a>（其全部内容会填充到 ./member/snap/db 文件中）。这些文件会定期（<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>）<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">进行</a>清理。
此处同样只保留 <code>--max-snapshots=5</code> 个文件。由于这些文件可能达到 O(GBs) 量级，可能导致磁盘空间耗尽。
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p>Raft 的<strong>预写日志</strong>，包含 Raft 接受的近期事务、定期快照或 CRC 记录。</p>
      <p>保留最近的 <code>--max-wals=5</code> 个文件。每个文件的大小为 <code>~64*10^6</code> 字节。文件超过此硬编码大小时才会被切分，因此实际大小可能略超过该值（所以预分配的 <code>0.tmp</code> 无法完全防止磁盘空间耗尽）。</p>
      <p>如果快照生成频率过低，可能会出现超过 <code>--max-wals=5</code> 个文件的情况，因为文件系统级锁会保护这些文件，防止其过早删除。</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>为下一个预写日志文件预留的空间</strong>。
      用于避免因 WAL 日志容量不足而导致 Raft 卡住，且无法触发告警的情况。
    </td>
  </tr>
</table>


### 临时文件 {#temporary-files}

在 etcd 内部处理过程中，可能会遇到多个生命周期较短的文件：

<table>
  <tr>
    <th>文件</th>
    <th>主要用途</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>当快照文件无法<a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">加载</a>时，会被重命名为“broken”。<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>etcd <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">启动</a>时会尝试加载最新文件。</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>或在执行 etcdctl 的备份/迁移命令期间。</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p>该<a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">临时</a> bbolt 文件由副本创建，用于响应领导者的 msgSnap 请求，按要求从指定快照恢复存储。</p>
      <p>
        完整内容成功获取后，文件将被<a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">重命名</a>为 <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>。若服务器在下载过程中崩溃或被终止，这些文件会保留在磁盘上，且不会自动清理。其体积可能达到数 GB。
      </p>
      <p>参见 <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>。<strong>已在 etcd 3.5 中修复。</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>在<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">碎片整理过程</a>中，该临时文件用于保存后端数据库内容（/member/snap/db）的副本。整理成功后，文件会重命名为 /member/snap/db，替换原后端数据库。</p>
      <p>在 etcd 服务器启动时，这些文件会被<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">清理</a>。</p>
    </td>
  </tr>
</table>

## bbolt B+ 树：**member/snap/db** {#bbolt-btree-membersnapdb}

该文件包含已应用至 Raft 日志某个特定位置的 etcd 主要内容（参见 [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)）。


### 物理组织结构 {#physical-organization}

Bolt 存储系统在物理上按 [B+树](https://en.wikipedia.org/wiki/B%2B_tree) 组织。B+树的物理页永远不会原地修改[^1]。相反，内容会被复制到新页（从空闲页列表中回收）中，一旦没有正在运行的事务可能访问该旧页，该旧页即被加入空闲页列表。得益于这一机制，打开的只读（RO）事务可观察到存储系统一致的历史状态。读写（RW）事务具有排他性，会阻塞其他所有读写事务。
大值存储在多个连续页上。页回收过程与需分配不同大小的连续页区域的需求相结合，可能导致 bbolt 存储系统出现日益严重的碎片化。

bbolt 文件不会自行缩小。只有在执行碎片整理过程中，文件才能被重写为一个新的文件，该文件末尾保留了一定数量的空闲页，并且大小已被截断。


### 逻辑组织 {#logical-organization}

bbolt 存储系统划分为多个桶。每个桶中以字典序存储键（byte[]→value byte[] 键值对）。下表列出了 etcd（截至版本 3.5）所使用的桶及其使用的键。

<table>
  <tr>
    <th>存储桶</th>
    <th>键</th>
    <th>示例值</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>表明其中一个成员已诊断出问题。</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code>（空）或 <code>BigEndian.PutUint64</code></td>
    <td>
      <p>角色或用户任何变更都会在事务提交时递增此字段。</p>
      <p>
        该值仅用于<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">授权过程中的乐观锁</a>。
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] 为字符串</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code> 序列化 </td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] 为字符串</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code> 序列化</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code>（字符串）</td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">次要</a> 版本的共识达成的通用存储版本。</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p> 保存最近一次 <code>Downgrade RPC</code> 请求所配置的意图。</p>
      <p>自 v3.5 版本起</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId] 使用 <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} 编码</p>
      <p>删除的键值对在序列化时会以 't' 结尾，表示“墓碑”（Tombstone）</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> 序列化 proto（<code>key, create_rev, mod_rev, version, value, lease id</code>）</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> 序列化后的 proto（ID、TTL、RemainingTTL）</td>
    <td>
      <p>注意：LeaseCheckpoint 仅扩展 RemainingTTL。TTL 仍来自原始 Grant。</p>
      <p style="text-decoration:underline;">注意 2：我们以秒为单位持久化 TTL（从未定义的“现在”开始计算）。崩溃循环的服务器不会释放租约！</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>以十六进制字符串形式表示的 [memberId]：<code>"8e9e05c52164694d"</code></td>
    <td>
      <em>以字符串形式序列化的 <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">Member</a> 结构：</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>已达成一致的集群成员关系信息。</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>以十六进制字符串形式表示的 [memberId]：<code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>所有已移除成员的 ID。用于验证已移除的成员不会以相同 ID 再次添加。</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">该字段目前（3.4 版本）从 V2 存储系统读取，从不从 V3 读取</a>。详见 <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>uint64 字节（大端序）</td>
    <td>表示最后应用的 WAL 条目在 Bolt DB 存储系统中的偏移量。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">scheduledCompactRev</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} 编码（共 16 字节）。</td>
    <td>在执行压缩请求后发生崩溃时，用于重新初始化压缩。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">finishedCompactRev</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} 编码（共 16 字节）。</td>
    <td>存储系统最近成功完成压缩时的修订版本（<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>）</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">自 etcd 3.5 版本起</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">自 etcd 3.5 版本起</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### 工具 {#tools}


#### bbolt {#bbolt}

bbolt 提供了一个命令行工具，可用于检查文件内容。

使用示例：

##### 列出给定 bbolt 文件中的所有桶： {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### 读取特定键值对： {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-db 可用于列出 v3 etcd 后端数据库（bbolt）的内容。

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

更多示例请参见：[https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL：预写日志 {#wal-write-ahead-log}

预写日志（Write Ahead Log）是 Raft 协议的持久化存储，用于存储提案。首先，领导者将提案写入其日志，然后（并发地）通过 Raft 协议将提案复制到跟随者。每个跟随者在向领导者确认复制之前，会先将其提案持久化到自身的 WAL 中。

etcd 中使用的 WAL 日志与标准 Raft 模型存在两方面的差异：

* 它不仅持久化索引条目，还持久化 Raft 快照（轻量级）和硬状态。因此，仅通过 WAL 日志即可恢复成员的完整 Raft 状态。
* WAL 只支持追加写入。条目不会原地覆盖；后续追加到文件中的同索引条目会取代先前的条目。


### 文件名 {#file-names}

WAL 日志文件的命名遵循以下模式：

```
"%016x-%016x.wal", seq, index
```

示例：`./member/wal/0000000000000010-00000000000bf1e6.wal`

因此，文件名包含十六进制编码：


* WAL 日志文件的顺序编号
* 文件中第一条条目或快照的索引。
  特别地，第一个文件“0000000000000000-0000000000000000.wal”包含索引为 0 的初始快照记录。

### 物理内容 {#physical-content}

WAL 日志文件由一系列“[帧](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)”组成。每个帧包含：


1. 使用 [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] 编码的 uint64，表示序列化后 [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) 的长度（3）。
2. 填充：若干个 0 字节，使整个帧的大小按 8 字节对齐。
3. 序列化后的 [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) 数据：
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - 以整数编码的枚举，用于决定如何解释下述 data 字段
    2. data - 由类型决定，通常是序列化后的 Protocol Buffers 数据
    3. crc - 自 WAL 日志创建以来，该副本上所有日志记录中所有“data”字段（不包含 type）的 RC-32 校验和。请注意，CRC 计算包含所有记录（即使它们未被 Raft 提交）。

当当前文件超过 <code>64*10^6</code> 字节时，会将其切分并开始写入新文件。


### 逻辑内容 {#logical-content}

预写日志文件在逻辑层包含：

* `Raftpb.Entry: ` 由 Raft 领导者复制的最近提案。其中部分提案被视为“已提交”，其余提案可能被逻辑覆盖。
* `Raftpb.HardState(term,commit,vote): ` 关于日志条目索引的周期性（非常频繁）信息，该索引表示条目已“提交”（复制到多数服务器），因此保证不会被更改或覆盖，并可应用于后端（v2、v3）。该信息还包含“任期”（指示是否存在与选举相关的变更）以及投票信息——当前副本在当前任期中投给的成员。
* `walpb.Snapshot(term, index): ` Raft 状态的周期性快照（不包含数据库内容，仅包含快照日志索引和 Raft 任期）
    * v2 存储内容存储在独立的 *.store 文件中。
    * v3 存储内容保存在 bbolt 文件中，一旦条目被应用，该文件即成为隐式快照。
* crc32 校验和记录（位于每个文件开头），用于恢复对文件剩余部分的 CRC 检查。
* `etcdserverpb.Metadata(node_id, cluster_id)` —— 用于标识日志所代表的集群与副本。

每个 WAL 日志文件按以下顺序构建：

1. CRC-32 帧（从之前所有文件延续的 CRC；第一个文件为 0）。
2. 元数据帧（集群 ID 与副本 ID）。
3. 仅初始 WAL 文件包含：

    * 空快照帧（索引：0，任期：0）。
      此帧用于维持一个不变量：所有条目之前均有一个快照。

   对于非初始（第 2 个及后续）WAL 文件：

    * HardState 帧。

4. 条目、硬状态与快照记录的混合

WAL 日志可能包含同一索引的多个条目。这种情况可能出现在 [Raft 论文](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf) 图 7 所描述的场景中。etcd 的 WAL 日志仅支持追加写入，因此当新条目以相同索引写入时，原有条目会被覆盖。

特别是在读取 WAL 时，[逻辑会用新条目覆盖旧条目](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462)。因此，仅当条目索引 entry.index &lt;= HardState.commit 时，才可视为最终版本。索引大于 HardState.commit 的条目可能发生变化。

WAL 日志中的“任期”应保持单调递增。

WAL 日志中的“索引”预期满足以下要求：

1. 从某个快照开始
2. 在该任期期间，索引应持续递增
3. 若任期发生变化，索引可能减少，但必须大于最新的 HardState.commit 值
4. 任意索引大于等于 HardState.commit 的新快照都可能发生，从而开启新的索引序列


![etcd 持久化存储文件](/etcd/learning/img/persistent-storage-files-figure-01.png)


### 工具 {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

etcd 的 WAL 日志可使用 [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs) 工具读取：

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

请注意：

* 该工具仅显示条目，而不显示 WAL 日志文件中的所有记录（如快照、HardState）。
* 该工具会自动应用“覆盖”规则。若某条目被同一索引下更新的条目覆盖，则工具仅输出最终值。
* 该工具还会输出未提交的条目（来自日志尾部），但不包含 HardState.commitIndex 信息，因此无法判断条目是否为最终值。


## Store V2 快照：**member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### 文件名： {#file-names-1}

**member/snap/{term}-{index}.snap**

文件名在 [此处](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) `("%016x-%016x.snap") ` 生成，采用 2 个十六进制编码的组合形式：


* `term` -> 快照生成时的 Raft 任期（两次选举之间的时段）
* `index` -> 快照生成时最后一个已应用提案的索引

### 创建 {#creation}

*.snap 文件由 [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68) 方法创建。

有两个触发器控制这些文件的创建：


* 每处理大约 --snapshotCount=（默认为 100'000）个已应用提案，就会创建一个新文件。这只是近似值：提案可能分批到达，而系统只会在一批处理结束时考虑生成快照，最终的快照过程还会异步调度。
  标志名 --snapshotCount 容易产生误解：它控制[最后一次快照索引与最后一次已应用提案索引之间的索引差](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)。
* Raft 请求副本从快照恢复。副本通过网络接收快照（msgSnap 消息）时，也会将其以轻量方式记录到 WAL 日志中。这可确保 WAL 日志尾部始终存在一个后接日志条目的有效快照，从而避免 WAL 日志中可能出现的不连续。

目前，这些文件大致[^3]与 WAL 日志中的 Snapshot 条目一一对应。随着 v2 存储系统停用，预计将彻底停止写入这些文件（3.5.x 可选启用，3.6.x 强制执行）。


### 内容 {#content}

该文件包含序列化后的 [snapdb.snapshot proto](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)`，

其中 `data` 字段包含 [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31)：

（字节数据，SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} 元数据），

最后，嵌套数据包含序列化为 JSON 格式的 [存储 v2 内容](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files)。


特别是存在：

* 任期
* 索引
* 成员数据：
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"[http://localhost:2379\](http://localhost:2379\)"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* 存储版本：/0/version -> 3.5.0


### 工具 {#tools-2}


#### protoc {#protoc}

以下命令可在 etcd 根目录下执行，用于查看文件内容：


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


类似地，可以提取 `data` 字段，并将其解码为 [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31)。


### etcd 3.4 *.snap 文件中示例 JSON 序列化存储 v2 内容： {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

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

## 变更记录 {#changes}

本节用于描述不同 etcd 版本之间引入的文件格式变更。

[^1]:
     bbolt 文件开头的元数据页会原地修改。

[^2]:
     不一致，因为大多数 uint 的写入格式为大端字节序

[^3]:
     WAL 日志开头的初始快照（索引: 0）不与 *.snap 文件关联。此外，旧的 *.snap 文件（或 WAL 日志）可能已被清除。
