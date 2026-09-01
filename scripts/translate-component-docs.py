#!/usr/bin/env python3
"""Translate component Markdown while preserving executable and link structure.

This helper intentionally uses the locally installed Ollama model. It writes each
target atomically only after every protected token has survived translation.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
CHINESE_STYLE_GUIDE = PROJECT / "TRANSLATION.md"
FRENCH_STYLE_GUIDE = PROJECT / "TRANSLATION.fr.md"
JAPANESE_STYLE_GUIDE = PROJECT / "TRANSLATION.ja.md"
STYLE_GUIDE = CHINESE_STYLE_GUIDE
DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache.json"
DEFAULT_MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"
DEFAULT_SCALAR_MODEL = "qwen2.5:7b"
CACHE_SCHEMA_VERSION = "16"
CHINESE_COMPONENTS = ("haproxy", "etcd")
DOCUMENT_COMPONENTS = (
    "patroni",
    "pgbackrest",
    "pgbouncer",
    "pgbadger",
    "haproxy",
    "etcd",
)
SUPPORTED_COMPONENTS = DOCUMENT_COMPONENTS + ("site",)
LOCALIZABLE_ROOTS = DOCUMENT_COMPONENTS + ("attribution", "search")
TARGET_LANGUAGE = "zh"
TARGET_SUFFIX = ".zh.md"
USABLE_IN_TRANSLATION = "适用范围："

MANUAL_TRANSLATIONS = {
    (
        "Before beginning, [download the snapshot backup](/etcd/op-guide/maintenance/#snapshot-backup). Should something go wrong with the upgrade, it is possible to use this backup to [rollback](#rollback) back to existing etcd version. Please note that the `snapshot` command only backs up the v3 data."
    ): (
        "开始前，请先 [下载快照备份](/etcd/op-guide/maintenance/#snapshot-backup)。如果升级出现问题，可以使用此备份 [回滚](#rollback)到现有 etcd 版本。请注意，`snapshot` 命令只备份 v3 数据。"
    ),
    (
        "However, a certificate whose SAN field does [not include any domain names but only IP addresses](https://github.com/etcd-io/etcd/issues/9541) would request `*tls.ClientHelloInfo` with an empty `ServerName` field, thus failing to trigger the TLS reload on initial TLS handshake; this becomes a problem when expired certificates need to be replaced online."
    ): (
        "不过，如果证书的 SAN 字段 [不包含任何域名而只有 IP 地址](https://github.com/etcd-io/etcd/issues/9541)，请求中的 `*tls.ClientHelloInfo` 会带有空的 `ServerName` 字段，导致初始 TLS 握手无法触发 TLS 重载；需要在线替换过期证书时，这就会成为问题。"
    ),
    (
        "Before [starting a downgrade](#downgrade-procedure), read through the rest of this guide to prepare."
    ): "开始 [降级](#downgrade-procedure)前，请阅读本指南其余内容并做好准备。",
    (
        "Since v3.2, the default value of `--snapshot-count` has [changed from from 10,000 to 100,000](https://github.com/etcd-io/etcd/pull/7160)."
    ): (
        "自 v3.2 起，`--snapshot-count` 的默认值已 [从 10,000 改为 100,000](https://github.com/etcd-io/etcd/pull/7160)。"
    ),
    (
        "There is a set of [default alerts](https://github.com/etcd-io/etcd/tree/main/contrib/mixin) for etcd v3 clusters for Prometheus."
    ): "etcd v3 集群为 Prometheus 提供了一组 [默认告警](https://github.com/etcd-io/etcd/tree/main/contrib/mixin)。",
    (
        "Before beginning, [backup the etcd data directory](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore). Should something go wrong with the upgrade, it is possible to use this backup to [downgrade](#downgrade) back to existing etcd version."
    ): (
        "开始前，请先 [备份 etcd 数据目录](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore)。"
        "如果升级出现问题，可以使用此备份 [降级](#downgrade)回现有 etcd 版本。"
    ),
    (
        "> [!WARNING]\n"
        "> When [migrating from v2 with no v3 data](https://github.com/etcd-io/etcd/issues/9480), etcd server v3.2+ panics when etcd restores from existing snapshots but no v3 `ETCD_DATA_DIR/member/snap/db` file. This happens when the server had migrated from v2 with no previous v3 data. This also prevents accidental v3 data loss (e.g. `db` file might have been moved). etcd requires that post v3 migration can only happen with v3 data. Do not upgrade to newer v3 versions until v3.0 server contains v3 data."
    ): (
        "> [!WARNING]\n"
        "> 从 [没有 v3 数据的 v2 迁移](https://github.com/etcd-io/etcd/issues/9480)时，如果 etcd 从现有快照恢复，但不存在 v3 `ETCD_DATA_DIR/member/snap/db` 文件，etcd v3.2+ 服务器会发生崩溃。这种情况出现在服务器由 v2 迁移且此前没有 v3 数据时。此限制也可防止意外丢失 v3 数据（例如 `db` 文件可能已被移动）。etcd 要求 v3 迁移后的操作必须有 v3 数据。v3.0 服务器包含 v3 数据之前，请勿升级到更新的 v3 版本。"
    ),
    "Get etcd up and running in less than 5 minutes!": "不到 5 分钟即可启动并运行 etcd！",
    (
        "Defines the number `<nb>` of queries to send to resolve a server name before giving up. Default\n"
        "value: 3"
    ): "定义解析服务器名称时，在放弃前发送的查询次数 `<nb>`。默认值：3",
    (
        "Extracts the substring at the given index counting from the beginning (positive index) or from the\n"
        "end (negative index) considering given delimiters from an input string. Indexes start at 1 or -1 and\n"
        "delimiters are a string formatted list of chars. Optionally you can specify `<count>` of fields to\n"
        "extract (default: 1). Value of 0 indicates extraction of all remaining fields."
    ): (
        "使用给定的分隔符切分输入字符串，并提取指定索引处的子串。正索引从开头计数，负索引从结尾计数。"
        "索引从 1 或 -1 开始；分隔符为格式化字符列表。可以指定要提取的字段数 `<count>`（默认值：1）。"
        "值 0 表示提取所有剩余字段。"
    ),
    "  Algorithms mentioned in [section 3.1](/haproxy/global/#section-3-1) of RFC7518 are managed:": (
        "  支持 RFC7518 [第 3.1 节](/haproxy/global/#section-3-1)中列出的算法："
    ),
    (
        "  Algorithms mentioned in [section 3.1](/haproxy/global/#section-3-1) of RFC7518 are managed "
        "(apart from HMAC ones):"
    ): "  支持 RFC7518 [第 3.1 节](/haproxy/global/#section-3-1)中列出的算法（HMAC 算法除外）：",
    (
        "Extracts the nth word counting from the beginning (positive index) or from the end (negative index)\n"
        "considering given delimiters from an input string. Indexes start at 1 or -1 and delimiters are a\n"
        "string formatted list of chars. Empty words are skipped. This means that delimiters at the start or\n"
        "end of the input string are ignored and consecutive delimiters within the input string are\n"
        "considered to be a single delimiter. Optionally you can specify `<count>` of words to extract\n"
        "(default: 1). Value of 0 indicates extraction of all remaining words."
    ): (
        "使用给定分隔符切分输入字符串，并提取从开头（正索引）或结尾（负索引）数起的第 n 个词。"
        "索引从 1 或 -1 开始；分隔符为格式化字符列表。空词会被跳过：输入字符串开头或结尾的分隔符将被忽略，"
        "连续分隔符视为单个分隔符。可以指定要提取的词数 `<count>`（默认值：1）。值 0 表示提取所有剩余词。"
    ),
    '''  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        Periodic <strong>snapshots of legacy v2 store</strong>, containing:
        <ul>
          <li>basic membership information</li>
          <li>etcd-version</li>
        </ul>
      </p>
      <p>As of etcd v3, the content is redundant to the content of /snap/db files.</p>
      <p>Periodically (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) these files <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">are purged</a>, and the last <code>--max-snapshots=5</code> are preserved.</p>
   </td>
  </tr>''': '''  <tr>
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
  </tr>''',
    '''  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>A complete <strong>bbolt snapshot downloaded</strong> from the etcd leader if the replica was lagging too much.</p>
      <p>Has the same type of content as (<code>./member/snap/db</code>) file.</p>
      <p>
        The file is used in 2 scenarios:
        <ul>
          <li>In response to the leader's request to recover from the snapshot.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">During the server startup</a>, when the last snapshot (.snap.db file) is found and detected to be having a newer index than the consistent_index in the current <code>snap.db</code> file.</li>
        </ul>
        Note: Periodic snapshots generated on each replica are only emitted in the form of *.snap file (not snap.db file). So there is no guarantee the most recent snapshot (in WAL log) has the *.snap.db file. But in such a case the backend (snap/db) is expected to be newer than the snapshot.
      </p>
      <p>
        The file <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">is not being deleted when the recovery is over</a> (so whole content is populated to ./member/snap/db file). Periodically (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) the files <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">are</a> purged.
Here also <code>--max-snapshots=5</code> are preserved. As these files can be O(GBs) this might create a risk of disk space exhaustion.
    </td>
  </tr>''': '''  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>如果副本严重滞后，则从 etcd 领导者下载完整的<strong>bbolt 快照</strong>。</p>
      <p>其内容类型与 <code>./member/snap/db</code> 文件相同。</p>
      <p>
        该文件用于以下 2 种场景：
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
  </tr>''',
    '''  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Raft’s Write Ahead Logs</strong>, containing recent transactions accepted by Raft, periodic snapshots or CRC records.</p>
      <p>Recent <code>--max-wals=5</code> files are being preserved. Each of these files is <code>~64*10^6</code> bytes. The file is cut when it exceeds this hardcoded size, so the files might slightly exceed that size (so the preallocated <code>0.tmp</code> does not offer full disk-exceeded protection).</p>
      <p>If the snapshots are too infrequent, there can be more than <code>--max-wals=5</code>, as file-system level locks are protecting the files preventing them from being deleted too early.</p>
    </td>
  </tr>''': '''  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p>Raft 的<strong>预写日志</strong>，包含 Raft 接受的近期事务、定期快照或 CRC 记录。</p>
      <p>保留最近的 <code>--max-wals=5</code> 个文件。每个文件的大小为 <code>~64*10^6</code> 字节。文件超过此硬编码大小时才会被切分，因此实际大小可能略超过该值（所以预分配的 <code>0.tmp</code> 无法完全防止磁盘空间耗尽）。</p>
      <p>如果快照生成频率过低，可能会出现超过 <code>--max-wals=5</code> 个文件的情况，因为文件系统级锁会保护这些文件，防止其过早删除。</p>
    </td>
  </tr>''',
    '<p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">The field is currently (3.4) read from store V2 and never from V3</a>. See <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>': (
        '<p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">'
        '该字段目前（3.4 版本）从 V2 存储系统读取，从不从 V3 读取</a>。详见 '
        '<a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>'
    ),
    '<td>Revision at which store was recently successfully compacted (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>': (
        '<td>存储系统最近成功完成压缩时的修订版本（'
        '<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">'
        'https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>）</td>'
    ),
    (
        "    * Empty Snapshot frame (Index:0, Term: 0).\n"
        "      The purpose of this frame is to hold an invariant that all entries are ‘preceded’ by a snapshot."
    ): (
        "    * 空快照帧（索引：0，任期：0）。\n"
        "      此帧用于维持一个不变量：所有条目之前均有一个快照。"
    ),
    "    * HardState frame.": "    * HardState 帧。",
    (
        "* A new file is created every (approximately) --snapshotCount=(by default 100'000) applied proposals. It’s an approximation as we might receive proposals in batches and we consider snapshotting only at the end of batch, finally the snapshotting process is asynchronously scheduled.\n"
        "  The flag name (--snapshotCount) is pretty misleading as it drives [differences in index value between ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)last snapshot index and last applied proposal index.\n"
        "* Raft requests the replica to restore from the snapshot. As a replica is receiving the snapshot over wire (msgSnap) message, it also checkpoints (lightweight) it into WAL log. This guarantees that in the WAL logs tail there is always a valid snapshot followed by entries. So it suppresses potential lack of continuity in the WAL logs."
    ): (
        "* 每处理大约 --snapshotCount=（默认为 100'000）个已应用提案，就会创建一个新文件。这只是近似值：提案可能分批到达，而系统只会在一批处理结束时考虑生成快照，最终的快照过程还会异步调度。\n"
        "  标志名 --snapshotCount 容易产生误解：它控制[最后一次快照索引与最后一次已应用提案索引之间的索引差](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)。\n"
        "* Raft 请求副本从快照恢复。副本通过网络接收快照（msgSnap 消息）时，也会将其以轻量方式记录到 WAL 日志中。这可确保 WAL 日志尾部始终存在一个后接日志条目的有效快照，从而避免 WAL 日志中可能出现的不连续。"
    ),
    (
        "Currently the files are roughly[^3] associated 1-1 with WAL logs Snapshot entries. With store v2 decommissioning we expect the files to stop being written at all (opt-in: 3.5.x,  mandatory 3.6.x)."
    ): (
        "目前，这些文件大致[^3]与 WAL 日志中的 Snapshot 条目一一对应。"
        "随着 v2 存储系统停用，预计将彻底停止写入这些文件（3.5.x 可选启用，3.6.x 强制执行）。"
    ),
}

TRANSLATABLE_META = {"title", "linkTitle", "description"}
CATEGORY_MAP = {
    "Concept": "概念",
    "Task": "任务",
    "Reference": "参考",
    "Tutorial": "教程",
}
CHINESE_MANUAL_TRANSLATIONS = MANUAL_TRANSLATIONS
CHINESE_CATEGORY_MAP = CATEGORY_MAP
EXACT_SCALAR_TRANSLATIONS = {
    "ja": {
        "Show commands": "SHOW コマンド",
        "Usage: pgbouncer command": "PgBouncer コマンドの使用法",
    },
}
JAPANESE_MANUAL_TRANSLATIONS = {
    (
        "1. Create a pgbouncer.ini file.  Details in **pgbouncer(5)**.  Simple example:"
    ): (
        "1. pgbouncer.ini ファイルを作成します。詳細は **pgbouncer(5)** を参照してください。簡単な例："
    ),
    (
        "When the connected user has the user name \"pgbouncer\", connects through the Unix socket\n"
        "and has same the UID as the running process, the actual FDs are passed over the connection.\n"
        "This mechanism is used to do an online restart.\n"
        "Note: This does not work on Windows."
    ): (
        "接続ユーザー名が \"pgbouncer\" で、Unix ソケット経由で接続し、実行中のプロセスと同じ UID を持つ場合、実際の FD が接続経由で渡されます。\n"
        "この仕組みはオンライン再起動に使用されます。\n"
        "注意：Windows では動作しません。"
    ),
    "- It is not tied to one backend server. The destination databases can reside on different hosts.": (
        "- 単一のバックエンドサーバーに固定されません。接続先データベースは異なるホストに配置できます。"
    ),
    "- Supports online reconfiguration for most settings.": (
        "- ほとんどの設定をオンラインで再構成できます。"
    ),
    "- Supports online restart/upgrade without dropping client connections.": (
        "- クライアント接続を切断せずにオンラインで再起動またはアップグレードできます。"
    ),
    (
        "* the entry in the `[database]` section for the pool has a value set for the `user` key (aka forced user)"
    ): (
        "* プールに対応する `[database]` セクションのエントリで、`user` キー（強制ユーザー）に値が設定されている"
    ),
    "* there is at least one client connected to the pool": (
        "* プールに少なくとも 1 つのクライアントが接続している"
    ),
    (
        "* this entry in the `[database]` section has a value set for the `user` key (aka forced user)"
    ): (
        "* `[database]` セクションのこのエントリで、`user` キー（強制ユーザー）に値が設定されている"
    ),
    (
        "    * Allow `KILL` to not take any database, which now means to `KILL` all databases. ([#1317])"
    ): (
        "    * `KILL` をデータベース指定なしで実行できるようにしました。この場合、すべてのデータベースに対して `KILL` を実行します。([#1317])"
    ),
    "  * Add `test_load_balance_hosts.py` to the tarball. ([#1282])": (
        "  * `test_load_balance_hosts.py` をリリース tarball に追加しました。([#1282])"
    ),
    (
        '2022-03-23  -  PgBouncer 1.17.0  -  "A line has been drawn"'
    ): (
        "2022-03-23  -  PgBouncer 1.17.0  -  「一線が引かれた」"
    ),
    (
        '2016-02-18 - PgBouncer 1.7.1 - "Forward To Five Friends Or Else"'
    ): (
        "2016-02-18 - PgBouncer 1.7.1 - 「5人の友人に転送しないと……」"
    ),
    (
        '2016-02-18  -  PgBouncer 1.7.1  -  "Forward To Five Friends Or Else"'
    ): (
        "2016-02-18  -  PgBouncer 1.7.1  -  「5人の友人に転送しないと……」"
    ),
    (
        '2011-04-01  -  PgBouncer 1.4.1  -  "It Was All An Act"'
    ): (
        "2011-04-01  -  PgBouncer 1.4.1  -  「すべては演技だった」"
    ),
    (
        '**2016-02-18  -  PgBouncer 1.7.1  -  "Forward To Five Friends Or Else"**'
    ): (
        "**2016-02-18  -  PgBouncer 1.7.1  -  「5人の友人に転送しないと……」**"
    ),
    (
        "If you use more than 8 IPs behind one DNS name, you now need to\n"
        "use EDNS0 protocol to query.  Only getaddrinfo_a()/getaddrinfo()\n"
        "and UDNS backends support it, libevent 1.x/2.x does not.\n"
        "To enable it for libc, add 'options edns0' to /etc/resolv.conf."
    ): (
        "1 つの DNS 名に 8 個を超える IP アドレスを関連付ける場合、EDNS0 プロトコルで照会する必要があります。\n"
        "この機能をサポートするのは getaddrinfo_a()/getaddrinfo() と UDNS バックエンドだけで、libevent 1.x/2.x はサポートしません。\n"
        "libc で有効にするには、/etc/resolv.conf に 'options edns0' を追加してください。"
    ),
    (
        '  * Console: Support ident quoting with "".  Originally we did not\n'
        '    have any commands that took database names, so no quoting was needed.'
    ): (
        '  * 管理コンソールで "" を使った識別子の引用をサポートしました。当初はデータベース名を引数に取るコマンドがなかったため、引用は不要でした。'
    ),
    "  * Default to --enable-evdns if libevent 2.x is used.": (
        "  * libevent 2.x を使用する場合、--enable-evdns をデフォルトで有効にします。"
    ),
    (
        "  * Set default server_reset_query to DISCARD ALL to be compatible\n"
        "    with Postgres by default."
    ): (
        "  * Postgres との互換性を保つため、server_reset_query のデフォルトを DISCARD ALL に設定しました。"
    ),
}
FRENCH_MANUAL_TRANSLATIONS = {
    (
        "enable diagnostic mode. This mode will output extra warnings about "
        "suspicious configuration\n"
        "statements. This will never prevent startup even in \"zero-warning\" "
        "mode nor change the exit status\n"
        "code."
    ): (
        "active le mode diagnostic. Ce mode affiche des avertissements "
        "supplémentaires sur les instructions de configuration suspectes. Il "
        "n'empêche jamais le démarrage, même en mode « sans avertissement », et "
        "ne modifie pas le code de sortie."
    ),
    (
        "adds `<cfgfile>` to the list of configuration files to be loaded. If "
        "`<cfgdir>` is a directory, all\n"
        "the files (and only files) it contains are added in lexical order "
        "(using LC_COLLATE=C) to the list\n"
        "of configuration files to be loaded; only files with \".cfg\" extension "
        "are added, only non hidden\n"
        "files (not prefixed with \".\") are added. Configuration files are loaded "
        "and processed in their\n"
        "declaration order. This option may be specified multiple times to load "
        "multiple files. See also\n"
        "\"--\". The difference between \"--\" and \"-f\" is that one \"-f\" "
        "must be placed before each file name,\n"
        "while a single \"--\" is needed before all file names. Both options can "
        "be used together, the command\n"
        "line ordering still applies. When more than one file is specified, each "
        "file must start on a section\n"
        "boundary, so the first keyword of each file must be one of \"global\", "
        "\"defaults\", \"peers\", \"listen\",\n"
        "\"frontend\", \"backend\", and so on. A file cannot contain just a "
        "server list for example."
    ): (
        "ajoute `<cfgfile>` à la liste des fichiers de configuration à charger. "
        "Si `<cfgdir>` est un répertoire, tous les fichiers qu'il contient, et "
        "uniquement les fichiers, sont ajoutés à la liste dans l'ordre lexical "
        "(avec LC_COLLATE=C). Seuls les fichiers portant l'extension \".cfg\" et "
        "les fichiers non cachés, sans préfixe \".\", sont ajoutés. Les fichiers "
        "de configuration sont chargés et traités dans leur ordre de déclaration. "
        "Cette option peut être répétée pour charger plusieurs fichiers. Voir "
        "aussi \"--\". Avec \"-f\", chaque nom de fichier doit être précédé de "
        "l'option, tandis qu'un seul \"--\" suffit avant tous les noms. Ces options "
        "peuvent être combinées et l'ordre de la ligne de commande continue de "
        "s'appliquer. Lorsque plusieurs fichiers sont indiqués, chacun doit "
        "commencer à une frontière de section ; son premier mot-clé doit donc être "
        "\"global\", \"defaults\", \"peers\", \"listen\", \"frontend\", \"backend\", "
        "etc. Un fichier ne peut pas contenir uniquement une liste de serveurs."
    ),
    (
        "all the arguments following \"--\" are paths to configuration "
        "file/directory to be loaded and\n"
        "processed in the declaration order. It is mostly useful when relying "
        "on the shell to load many files\n"
        "that are numerically ordered. See also \"-f\". The difference between "
        "\"--\" and \"-f\" is that one \"-f\"\n"
        "must be placed before each file name, while a single \"--\" is needed "
        "before all file names. Both\n"
        "options can be used together, the command line ordering still applies. "
        "When more than one file is\n"
        "specified, each file must start on a section boundary, so the first "
        "keyword of each file must be one\n"
        "of \"global\", \"defaults\", \"peers\", \"listen\", \"frontend\", "
        "\"backend\", and so on. A file cannot contain\n"
        "just a server list for example."
    ): (
        "Tous les arguments qui suivent \"--\" sont des chemins de fichiers ou "
        "de répertoires de configuration, chargés et traités dans l'ordre de "
        "déclaration. Cette forme est surtout utile lorsque le shell charge de "
        "nombreux fichiers ordonnés numériquement. Voir aussi \"-f\". Avec \"-f\", "
        "chaque nom de fichier doit être précédé de l'option, tandis qu'un seul "
        "\"--\" suffit avant l'ensemble des noms. Ces options peuvent être "
        "combinées et l'ordre de la ligne de commande continue de s'appliquer. "
        "Lorsque plusieurs fichiers sont indiqués, chacun doit commencer à une "
        "frontière de section ; son premier mot-clé doit donc être \"global\", "
        "\"defaults\", \"peers\", \"listen\", \"frontend\", \"backend\", etc. Un "
        "fichier ne peut pas contenir uniquement une liste de serveurs."
    ),
    (
        "Response headers work exactly like request headers, and as such, HAProxy "
        "uses the same parsing\n"
        "function for both. Please refer to paragraph 1.3.2 for more details."
    ): (
        "Les en-têtes de réponse fonctionnent exactement comme les en-têtes de "
        "requête ; HAProxy utilise donc la même fonction pour les analyser. "
        "Reportez-vous au paragraphe 1.3.2 pour plus de détails."
    ),
    (
        "An HTTP response looks very much like an HTTP request. Both are called "
        "HTTP messages. Let's consider\n"
        "this HTTP response:"
    ): (
        "Une réponse HTTP ressemble beaucoup à une requête HTTP. Ces éléments "
        "sont appelés des messages HTTP. Considérons la réponse suivante :"
    ),
    "- close : the connection is actively closed after end of response on both sides.": (
        "- close : la connexion est activement fermée de part et d'autre après la "
        "fin de la réponse."
    ),
    (
        "By default HAProxy operates in keep-alive mode with regards to persistent "
        "connections: for each\n"
        "connection it processes each request and response, and leaves the "
        "connection idle on both sides\n"
        "between the end of a response and the start of a new request. When it "
        "receives HTTP/2 connections\n"
        "from a client, it processes all the requests in parallel and leaves the "
        "connection idling, waiting\n"
        "for new requests, just as if it was a keep-alive HTTP connection."
    ): (
        "Par défaut, HAProxy utilise le mode keep-alive pour les connexions "
        "persistantes : il traite chaque requête et chaque réponse, puis laisse "
        "la connexion inactive de part et d'autre entre la fin d'une réponse et "
        "le début de la requête suivante. Lorsqu'un client établit une connexion "
        "HTTP/2, HAProxy traite les requêtes en parallèle puis laisse la connexion "
        "inactive en attendant de nouvelles requêtes, comme pour une connexion "
        "HTTP keep-alive."
    ),
    (
        "The next improvement is the multiplexed mode, as implemented in HTTP/2 "
        "and HTTP/3. In this mode,\n"
        "multiple transactions (i.e. request-response pairs) are transmitted in "
        "parallel over a single\n"
        "connection, and they all progress at their own speed, independent from "
        "each other. With multiplexed\n"
        "protocols, a new notion of \"stream\" was introduced, to represent these "
        "parallel communications\n"
        "happening over the same connection. Each stream is generally assigned "
        "a unique identifier for a\n"
        "given connection, that is used by both endpoints to know where to deliver "
        "the data. It is fairly\n"
        "common for clients to start many (up to 100, sometimes more) streams in "
        "parallel over a same\n"
        "connection, and let the server sort them out and respond in any order "
        "depending on what response is\n"
        "available. The main benefit of the multiplexed mode is that it significantly "
        "reduces the number of\n"
        "round trips, and speeds up page loading time over high latency networks. "
        "It is sometimes visible on\n"
        "sites using many images, where all images appear to load in parallel."
    ): (
        "L'amélioration suivante est le mode multiplexé, tel qu'il est implémenté "
        "dans HTTP/2 et HTTP/3. Plusieurs transactions, c'est-à-dire des paires "
        "requête-réponse, sont transmises en parallèle sur une seule connexion et "
        "progressent chacune à leur propre rythme. Les protocoles multiplexés ont "
        "introduit la notion de « flux » pour représenter ces communications "
        "parallèles. Chaque flux reçoit généralement un identifiant unique pour la "
        "connexion, utilisé par chaque extrémité pour acheminer les données. Les "
        "clients ouvrent couramment de nombreux flux, jusqu'à 100 ou davantage, "
        "sur la même connexion et laissent le serveur répondre dans l'ordre de "
        "disponibilité. Le multiplexage réduit fortement les allers-retours et "
        "accélère le chargement des pages sur les réseaux à forte latence. Sur les "
        "sites riches en images, celles-ci semblent alors se charger en parallèle."
    ),
    "- Support different protocol families on both sides (e.g. IPv4/IPv6/Unix);": (
        "- Prendre en charge différentes familles de protocoles de part et d'autre "
        "(par exemple IPv4, IPv6 ou Unix) ;"
    ),
    (
        "In addition, for a given filter, depending on the filter keyword used, "
        "the limitation can be applied\n"
        "on incoming data, received from the client and forwarded to a server, "
        "or on outgoing data, received\n"
        "from a server and sent to the client. To apply a limit on incoming data, "
        "\"bwlim-in\" keyword must be\n"
        "used. To apply it on outgoing data, \"bwlim-out\" keyword must be used. "
        "In both cases, the bandwidth\n"
        "limitation is applied on forwarded data, at the stream level."
    ): (
        "En outre, selon le mot-clé utilisé pour un filtre, la limitation peut "
        "s'appliquer aux données entrantes, reçues du client puis transmises au "
        "serveur, ou aux données sortantes, reçues du serveur puis envoyées au "
        "client. Utilisez « bwlim-in » pour limiter les données entrantes et "
        "« bwlim-out » pour les données sortantes. Dans chaque cas, la limitation "
        "s'applique aux données transmises, au niveau du flux."
    ),
    (
        "Other methods consist in sampling the production traffic sent to a "
        "destination to observe if it is\n"
        "processed correctly or not, and to evict the components which return "
        "inappropriate responses.\n"
        "However this requires to sacrifice a part of the production traffic "
        "and this is not always\n"
        "acceptable. A combination of these two mechanisms provides the best of "
        "both worlds, with both of\n"
        "them being used to detect a fault, and only health checks to detect the "
        "end of the fault. A last\n"
        "method involves centralized reporting: a central monitoring agent "
        "periodically updates all load\n"
        "balancers about all components' state. This gives a global view of the "
        "infrastructure to all\n"
        "components, though sometimes with less accuracy or responsiveness. It's "
        "best suited for environments\n"
        "with many load balancers and many servers."
    ): (
        "D'autres méthodes échantillonnent le trafic de production envoyé à une "
        "destination pour vérifier son traitement et écarter les composants qui "
        "renvoient des réponses inappropriées. Cela sacrifie toutefois une partie "
        "du trafic de production, ce qui n'est pas toujours acceptable. Combiner "
        "ces deux mécanismes offre le meilleur de chaque approche : ils servent "
        "ensemble à détecter une panne, tandis que les contrôles d'état seuls en "
        "détectent la fin. Une dernière méthode repose sur un rapport centralisé : "
        "un agent de supervision met périodiquement à jour tous les répartiteurs "
        "avec l'état des composants. Chacun dispose ainsi d'une vue globale de "
        "l'infrastructure, parfois moins précise ou moins réactive. Cette approche "
        "convient surtout aux environnements comportant de nombreux répartiteurs "
        "et serveurs."
    ),
    (
        "The first one acts at the packet level and processes packets more or "
        "less individually. There is a\n"
        "1-to-1 relation between input and output packets, so it is possible to "
        "follow the traffic on both\n"
        "sides of the load balancer using a regular network sniffer. This "
        "technology can be very cheap and\n"
        "extremely fast. It is usually implemented in hardware (ASICs) allowing "
        "to reach line rate, such as\n"
        "switches doing ECMP. Usually stateless, it can also be stateful "
        "(consider the session a packet\n"
        "belongs to and called layer4-LB or L4), may support DSR (direct server "
        "return, without passing\n"
        "through the LB again) if the packets were not modified, but provides "
        "almost no content awareness.\n"
        "This technology is very well suited to network-level load balancing, "
        "though it is sometimes used for\n"
        "very basic server load balancing at high speed."
    ): (
        "La première agit au niveau des paquets et les traite plus ou moins "
        "individuellement. La relation entre paquets d'entrée et de sortie est de "
        "1 à 1 ; un analyseur réseau classique peut donc suivre le trafic de part "
        "et d'autre du répartiteur. Cette technologie peut être très peu coûteuse "
        "et extrêmement rapide. Elle est généralement implémentée dans le matériel "
        "(ASIC), ce qui permet d'atteindre le débit de ligne, par exemple avec des "
        "commutateurs ECMP. Habituellement sans état, elle peut aussi conserver un "
        "état en tenant compte de la session du paquet ; on parle alors de "
        "layer4-LB ou L4. Elle peut prendre en charge le DSR (retour direct du "
        "serveur sans repasser par le répartiteur) lorsque les paquets ne sont pas "
        "modifiés, mais n'offre presque aucune connaissance du contenu. Cette "
        "technologie convient particulièrement à la répartition de charge réseau, "
        "bien qu'elle serve parfois à une répartition serveur très simple à haut "
        "débit."
    ),
    (
        "- a TCP normalizer: since connections are locally terminated by the "
        "operating system, there is no\n"
        "  relation between both sides, so abnormal traffic such as invalid "
        "packets, flag combinations,\n"
        "  window advertisements, sequence numbers, incomplete connections "
        "(SYN floods), or so will not be\n"
        "  passed to the other side. This protects fragile TCP stacks from "
        "protocol attacks, and also allows\n"
        "  to optimize the connection parameters with the client without having "
        "to modify the servers' TCP\n"
        "  stack settings."
    ): (
        "- un normalisateur TCP : puisque le système d'exploitation termine les "
        "connexions localement, il n'existe aucune relation entre les extrémités. "
        "Le trafic anormal, tel que des paquets invalides, des combinaisons de "
        "drapeaux, des annonces de fenêtre, des numéros de séquence ou des "
        "connexions incomplètes (SYN flood), n'est donc pas transmis à l'autre "
        "extrémité. Cela protège les piles TCP fragiles contre les attaques de "
        "protocole et permet d'optimiser les paramètres de connexion côté client "
        "sans modifier ceux de la pile TCP des serveurs."
    ),
    (
        "- an SSL terminator / initiator / offloader: SSL/TLS may be used on "
        "the connection coming from the\n"
        "  client, on the connection going to the server, or even on both "
        "connections. A lot of settings can\n"
        "  be applied per name (SNI), and may be updated at runtime without "
        "restarting. Such setups are\n"
        "  extremely scalable and deployments involving tens to hundreds of "
        "thousands of certificates were\n"
        "  reported."
    ): (
        "- un terminateur, initiateur ou déchargeur SSL : SSL/TLS peut être "
        "utilisé sur la connexion provenant du client, sur celle allant vers le "
        "serveur, ou simultanément sur ces connexions. De nombreux paramètres "
        "peuvent être appliqués par nom (SNI) et mis à jour à l'exécution sans "
        "redémarrage. Ces configurations passent extrêmement bien à l'échelle ; "
        "des déploiements comportant des dizaines ou des centaines de milliers de "
        "certificats ont été signalés."
    ),
    (
        "- a TCP proxy: it can accept a TCP connection from a listening socket, "
        "connect to a server and\n"
        "  attach these sockets together allowing traffic to flow in both "
        "directions; IPv4, IPv6 and even\n"
        "  UNIX sockets are supported on either side, so this can provide an "
        "easy way to translate addresses\n"
        "  between different families."
    ): (
        "- un proxy TCP : il peut accepter une connexion TCP sur un socket "
        "d'écoute, se connecter à un serveur et associer ces sockets afin que "
        "le trafic circule dans chaque direction. Les sockets IPv4, IPv6 et même "
        "UNIX sont pris en charge de part et d'autre, ce qui permet de traduire "
        "facilement les adresses entre différentes familles."
    ),
    (
        "HAProxy is written as \"HAProxy\" to designate the product, and as "
        "\"haproxy\" to designate the\n"
        "executable program, software package or a process. However, both are "
        "commonly used for both\n"
        "purposes, and are pronounced H-A-Proxy. Very early, \"haproxy\" used to "
        "stand for \"high availability\n"
        "proxy\" and the name was written in two separate words, though by now "
        "it means nothing else than\n"
        "\"HAProxy\"."
    ): (
        "La graphie « HAProxy » désigne le produit, tandis que « haproxy » "
        "désigne le programme exécutable, le paquet logiciel ou un processus. "
        "Ces graphies sont toutefois couramment utilisées dans chaque contexte "
        "et se prononcent H-A-Proxy. À l'origine, « haproxy » signifiait « high "
        "availability proxy » et le nom s'écrivait en deux mots distincts ; "
        "aujourd'hui, il ne signifie plus rien d'autre que « HAProxy »."
    ),
    (
        "For environments where SNMP is mandatory, at least two agents exist, "
        "one is provided with the\n"
        "HAProxy sources and relies on the Net-SNMP Perl module. Another one is "
        "provided with the commercial\n"
        "packages and doesn't require Perl. Both are roughly equivalent in "
        "terms of coverage."
    ): (
        "Dans les environnements où SNMP est obligatoire, il existe au moins deux "
        "agents. L'un est fourni avec les sources HAProxy et repose sur le module "
        "Perl Net-SNMP. L'autre accompagne les paquets commerciaux et ne requiert "
        "pas Perl. Ils offrent une couverture globalement équivalente."
    ),
    (
        "If it is observed that a lot of time is spent in interrupt/softirq, "
        "it is important to ensure that\n"
        "they don't run on the same CPU. Most systems tend to pin the tasks on "
        "the CPU where they receive the\n"
        "network traffic because for certain workloads it improves things. But "
        "with heavily network-bound\n"
        "workloads it is the opposite as the haproxy process will have to fight "
        "against its kernel\n"
        "counterpart. Pinning haproxy to one CPU core and the interrupts to "
        "another one, all sharing the same\n"
        "L3 cache tends to sensibly increase network performance because in "
        "practice the amount of work for\n"
        "haproxy and the network stack are quite close, so they can almost fill "
        "an entire CPU each. On Linux\n"
        "this is done using taskset (for haproxy) or using cpu-map (from the "
        "haproxy config), and the\n"
        "interrupts are assigned under /proc/irq. Many network interfaces "
        "support multiple queues and\n"
        "multiple interrupts. In general it helps to spread them across a small "
        "number of CPU cores provided\n"
        "they all share the same L3 cache. Please always stop irq_balance which "
        "always does the worst\n"
        "possible thing on such workloads."
    ): (
        "Si une grande partie du temps est consacrée aux interruptions et "
        "softirq, assurez-vous qu'elles ne s'exécutent pas sur le même processeur. "
        "La plupart des systèmes fixent les tâches sur le processeur qui reçoit le "
        "trafic réseau, car cela améliore certaines charges. Pour les charges très "
        "liées au réseau, c'est l'inverse : le processus HAProxy doit concurrencer "
        "la pile noyau. Fixer HAProxy sur un cœur et les interruptions sur un "
        "autre, partageant le même cache L3, améliore sensiblement les performances "
        "réseau. En pratique, HAProxy et la pile réseau ont des quantités de travail "
        "proches et peuvent presque saturer chacun un cœur. Sous Linux, utilisez "
        "taskset pour HAProxy ou cpu-map dans sa configuration ; les interruptions "
        "sont affectées sous /proc/irq. De nombreuses interfaces réseau prennent "
        "en charge plusieurs files et interruptions. Il est généralement utile de "
        "les répartir sur quelques cœurs partageant le même cache L3. Arrêtez "
        "toujours irq_balance, qui effectue le pire choix pour ce type de charge."
    ),
    (
        "Once it is certain that the system will allow the haproxy process to "
        "use the requested number of\n"
        "file descriptors, two new system-specific limits may be encountered. "
        "The first one is the\n"
        "system-wide file descriptor limit, which is the total number of file "
        "descriptors opened on the\n"
        "system, covering all processes. When this limit is reached, accept() "
        "or socket() will typically\n"
        "return ENFILE. The second one is the per-process hard limit on the "
        "number of file descriptors, it\n"
        "prevents setrlimit() from being set higher. Both are very dependent on "
        "the operating system. On\n"
        "Linux, the system limit is set at boot based on the amount of memory. "
        "It can be changed with the\n"
        "\"fs.file-max\" sysctl. And the per-process hard limit is set to 1048576 "
        "by default, but it can be\n"
        "changed using the \"fs.nr_open\" sysctl."
    ): (
        "Une fois certain que le système autorise le processus HAProxy à utiliser "
        "le nombre demandé de descripteurs de fichiers, deux nouvelles limites "
        "propres au système peuvent apparaître. La première est la limite globale "
        "du nombre de descripteurs ouverts sur le système, tous processus "
        "confondus. Lorsqu'elle est atteinte, accept() ou socket() renvoie "
        "généralement ENFILE. La seconde est la limite stricte par processus, qui "
        "empêche setrlimit() de fixer une valeur supérieure. Ces limites dépendent "
        "fortement du système d'exploitation. Sous Linux, la limite globale est "
        "fixée au démarrage en fonction de la mémoire et peut être modifiée avec "
        "le sysctl \"fs.file-max\". La limite stricte par processus vaut 1048576 "
        "par défaut et peut être modifiée avec le sysctl \"fs.nr_open\"."
    ),
    (
        "Both of these signals may be sent by the new haproxy process itself "
        "during a reload or restart, so\n"
        "that they are sent at the latest possible moment and only if absolutely "
        "required. This is what is\n"
        "performed by the \"-st\" (hard) and \"-sf\" (graceful) options respectively."
    ): (
        "Ces signaux peuvent être envoyés par le nouveau processus HAProxy lui-"
        "même pendant un rechargement ou un redémarrage, afin de ne les émettre "
        "qu'au dernier moment et seulement s'ils sont indispensables. C'est ce "
        "que font respectivement les options \"-st\" (arrêt brutal) et \"-sf\" "
        "(arrêt gracieux)."
    ),
    (
        "Pound is another well-known load balancer. It's much simpler and has "
        "much less features than HAProxy\n"
        "but for many very basic setups both can be used. Its author has always "
        "focused on code auditability\n"
        "first and wants to maintain the set of features low. Its thread-based "
        "architecture scales less well\n"
        "with high connection counts, but it's a good product."
    ): (
        "Pound est un autre répartiteur de charge bien connu. Il est beaucoup "
        "plus simple et offre nettement moins de fonctionnalités que HAProxy, "
        "mais Pound comme HAProxy peuvent convenir à de nombreuses configurations "
        "élémentaires. Son auteur a toujours privilégié l'auditabilité du code et "
        "souhaite conserver un ensemble restreint de fonctionnalités. Son "
        "architecture à base de threads passe moins bien à l'échelle avec un "
        "grand nombre de connexions, mais le produit reste solide."
    ),
    (
        "NGINX is the second de-facto standard HTTP server. Just like Apache, "
        "it covers a wide range of\n"
        "features. NGINX is built on a similar model as HAProxy so it has no "
        "problem dealing with tens of\n"
        "thousands of concurrent connections. When used as a gateway to some "
        "applications (e.g. using the\n"
        "included PHP FPM) it can often be beneficial to set up some frontend "
        "connection limiting to reduce\n"
        "the load on the PHP application. HAProxy will clearly be useful there "
        "both as a regular load\n"
        "balancer and as the traffic regulator to speed up PHP by decongesting "
        "it. Also since both products\n"
        "use very little CPU thanks to their event-driven architecture, it's "
        "often easy to install both of\n"
        "them on the same system. NGINX implements HAProxy's PROXY protocol, "
        "thus it is easy for HAProxy to\n"
        "pass the client's connection information to NGINX so that the "
        "application gets all the relevant\n"
        "information. Some benchmarks have also shown that for large static "
        "file serving, implementing\n"
        "consistent hash on HAProxy in front of NGINX can be beneficial by "
        "optimizing the OS' cache hit\n"
        "ratio, which is basically multiplied by the number of server nodes."
    ): (
        "NGINX est le second serveur HTTP de facto. Comme Apache, il couvre un "
        "large éventail de fonctionnalités. Conçu selon un modèle similaire à "
        "HAProxy, il gère sans difficulté des dizaines de milliers de connexions "
        "simultanées. Lorsqu'il sert de passerelle vers des applications, par "
        "exemple avec PHP FPM, limiter les connexions en frontal peut réduire la "
        "charge de l'application PHP. HAProxy est alors utile tant comme "
        "répartiteur de charge classique que comme régulateur de trafic pour "
        "désengorger PHP. Comme ces produits consomment très peu de CPU grâce à "
        "leur architecture événementielle, il est souvent facile d'installer "
        "HAProxy et NGINX sur le même système. NGINX implémente le protocole PROXY "
        "de HAProxy ; HAProxy peut donc lui transmettre les informations de "
        "connexion du client afin que l'application dispose de tout le contexte "
        "utile. Des benchmarks ont aussi montré que, pour servir de gros fichiers "
        "statiques, un hachage cohérent dans HAProxy devant NGINX peut améliorer le "
        "taux de succès du cache du système d'exploitation, qui est essentiellement "
        "multiplié par le nombre de nœuds serveurs."
    ),
    (
        "- about 5000 concurrent end-to-end TLS connections (both sides) per "
        "GB of RAM including the memory\n"
        "  required for system buffers;"
    ): (
        "- environ 5000 connexions TLS de bout en bout simultanées, côté client "
        "et côté serveur, par Go de RAM, y compris la mémoire requise pour les "
        "tampons système ;"
    ),
    (
        "The complete pinned inputs and SHA-256 checksums are retained under "
        "`sources/haproxy/`. The\n"
        "[upstream license notice](/third_party/haproxy/LICENSE) and [GPLv2 "
        "text](/third_party/haproxy/GPL-2.0)\n"
        "are published beside the manuals. A reviewed Simplified Chinese "
        "companion edition is available for\n"
        "every page."
    ): (
        "Les sources complètes épinglées et leurs sommes de contrôle SHA-256 "
        "sont conservées sous `sources/haproxy/`. La [notice de licence "
        "amont](/third_party/haproxy/LICENSE) et le [texte "
        "GPLv2](/third_party/haproxy/GPL-2.0) sont publiés avec les manuels. Une "
        "édition complémentaire relue en chinois simplifié est disponible pour "
        "chaque page."
    ),
    (
        "Both the primary and standby databases are required to perform the "
        "backup, though the vast majority of the files will be copied from the "
        "standby to reduce load on the primary. The database hosts can be "
        "configured in any order. pgBackRest will automatically determine which "
        "is the primary and which is the standby."
    ): (
        "La base primaire comme la base standby sont nécessaires pour effectuer "
        "la sauvegarde, bien que l'immense majorité des fichiers soient copiés "
        "depuis le standby afin de réduire la charge du primaire. Les hôtes de "
        "base de données peuvent être configurés dans n'importe quel ordre ; "
        "pgBackRest détermine automatiquement lequel est primaire et lequel est "
        "standby."
    ),
    (
        "Backup `repo1-retention-diff=1` so two differentials will need to be "
        "performed before one is expired. An incremental backup is added to "
        "demonstrate incremental expiration, which in this case depends on the "
        "differential expiration."
    ): (
        "Avec `repo1-retention-diff=1`, deux sauvegardes différentielles doivent "
        "être effectuées avant que l'une d'elles n'expire. Une sauvegarde "
        "incrémentielle est ajoutée pour illustrer l'expiration incrémentielle, qui "
        "dépend ici de l'expiration de la sauvegarde différentielle."
    ),
    (
        "**Differential Backup**: pgBackRest copies only those database cluster "
        "files that have changed since the last full backup. pgBackRest restores "
        "a differential backup by copying all of the files in the chosen "
        "differential backup and the appropriate unchanged files from the previous "
        "full backup. The advantage of a differential backup is that it requires "
        "less disk space than a full backup, however, the differential backup and "
        "the full backup must both be valid to restore the differential backup."
    ): (
        "**Sauvegarde différentielle** : pgBackRest copie uniquement les fichiers "
        "du cluster de base de données modifiés depuis la dernière sauvegarde "
        "complète. Pour restaurer une sauvegarde différentielle, pgBackRest copie "
        "tous les fichiers de celle-ci ainsi que les fichiers inchangés requis de "
        "la sauvegarde complète précédente. Une sauvegarde différentielle occupe "
        "moins d'espace disque qu'une sauvegarde complète, mais elle et la "
        "sauvegarde complète doivent chacune être valides pour permettre la "
        "restauration."
    ),
    (
        "- No restore functionality, but the backup directories are consistent "
        "PostgreSQL data directories. You'll need to either uncompress the files "
        "or turn off compression in the backup. Uncompressed backups on a ZFS "
        "(or similar) filesystem are a good option because backups can be "
        "restored locally via a snapshot to create logical backups or do spot "
        "data recovery.\n"
        "- Archiving is single-threaded. This has not posed an issue on our "
        "multi-terabyte databases with heavy write volume. Recommend a large WAL "
        "volume or to use the async option with a large volume nearby.\n"
        "- Backups are multi-threaded, but the `Net::OpenSSH` library does not "
        "appear to be 100% thread-safe so it will very occasionally lock up on a "
        "thread. There is an overall process timeout that resolves this issue by "
        "killing the process. Yes, very ugly."
    ): (
        "- La restauration n'est pas encore implémentée, mais les répertoires de "
        "sauvegarde sont des répertoires de données PostgreSQL cohérents. Vous "
        "devrez décompresser les fichiers ou désactiver la compression de la "
        "sauvegarde. Les sauvegardes non compressées sur ZFS, ou un système de "
        "fichiers similaire, peuvent être restaurées localement par instantané "
        "pour créer des sauvegardes logiques ou récupérer ponctuellement des "
        "données.\n"
        "- L'archivage est monothread. Cela n'a posé aucun problème sur nos bases "
        "de plusieurs téraoctets soumises à un fort volume d'écritures. Un grand "
        "volume WAL est recommandé, ou l'option asynchrone avec un volume proche "
        "de grande capacité.\n"
        "- Les sauvegardes sont multithreadées, mais la bibliothèque "
        "`Net::OpenSSH` ne semble pas sûre à 100% avec les threads et peut très "
        "occasionnellement en bloquer un. Un délai global tue le processus et "
        "résout le problème. Oui, c'est assez laid."
    ),
    (
        "- Backup from a standby cluster. A connection to the primary cluster "
        "is still required to start/stop the backup and copy files that are not "
        "replicated, but the vast majority of files are copied from the standby "
        "in order to reduce load on the primary.\n"
        "- More flexible configuration for databases. Master and standby can "
        "both be configured on the backup server and pgBackRest will automatically "
        "determine which is the primary. This means no configuration changes for "
        "backup are required after failing over from a primary to standby when a "
        "separate backup server is used.\n"
        "- Exclude directories during backup that are cleaned, recreated, or "
        "zeroed by PostgreSQL at startup. These include `pgsql_tmp` and "
        "`pg_stat_tmp`. The `postgresql.auto.conf.tmp` file is now excluded in "
        "addition to files that were already excluded: `backup_label.old`, "
        "`postmaster.opts`, `postmaster.pid`, `recovery.conf`, `recovery.done`."
    ): (
        "- Sauvegarder depuis un cluster standby. Une connexion au cluster "
        "primaire reste nécessaire pour démarrer ou arrêter la sauvegarde et "
        "copier les fichiers non répliqués, mais l'immense majorité des fichiers "
        "est copiée depuis le standby afin de réduire la charge du primaire.\n"
        "- Assouplir la configuration des bases de données. Le primaire comme le "
        "standby peuvent être configurés sur le serveur de sauvegarde ; pgBackRest "
        "détermine automatiquement lequel est primaire. Avec un serveur de "
        "sauvegarde distinct, aucun changement de configuration n'est donc requis "
        "après un basculement du primaire vers le standby.\n"
        "- Exclure pendant la sauvegarde les répertoires que PostgreSQL nettoie, "
        "recrée ou remet à zéro au démarrage. Cela comprend `pgsql_tmp` et "
        "`pg_stat_tmp`. Le fichier `postgresql.auto.conf.tmp` est désormais exclu, "
        "en plus de `backup_label.old`, `postmaster.opts`, `postmaster.pid`, "
        "`recovery.conf` et `recovery.done`."
    ),
    (
        "- Fixed an issue where a backup could error if no changes were made "
        "to a database between backups and only `pg_control` changed.\n"
        "- Fixed an issue where tablespace paths with the same prefix would "
        "cause an invalid link error. (*Reported by Nikhilchandra Kulkarni.*)"
    ): (
        "- Corriger un problème pouvant faire échouer une sauvegarde lorsqu'aucune "
        "modification n'avait été apportée à la base de données depuis la "
        "sauvegarde précédente et que seul `pg_control` avait changé.\n"
        "- Corriger un problème où des chemins de tablespace partageant le même "
        "préfixe provoquaient une erreur de lien invalide. (*Signalé par "
        "Nikhilchandra Kulkarni.*)"
    ),
    "- Retry all S3 `5xx` errors rather than just `500` internal errors. (*Suggested by Craig A. James.*)": (
        "- Réessayer toutes les erreurs S3 `5xx`, et non plus seulement les "
        "erreurs internes `500`. (*Suggéré par Craig A. James.*)"
    ),
    (
        "- Retry S3 `RequestTimeTooSkewed` errors instead of immediately "
        "terminating. (*Reported by sean0101n, Tim Garton, Jesper St John, Aleš "
        "Zelený.*)\n"
        "- Fix incorrect handling of `transfer-encoding` response to `HEAD` "
        "request. (*Reported by Pavel Suderevsky.*)\n"
        "- Fix scoping violations exposed by optimizations in gcc 9. (*Reported "
        "by Christian Lange, Ned T. Crigler.*)"
    ): (
        "- Réessayer les erreurs S3 `RequestTimeTooSkewed` au lieu de terminer "
        "immédiatement. (*Signalé par sean0101n, Tim Garton, Jesper St John et "
        "Aleš Zelený.*)\n"
        "- Corriger le traitement incorrect de la réponse `transfer-encoding` à "
        "une requête `HEAD`. (*Signalé par Pavel Suderevsky.*)\n"
        "- Corriger les violations de portée révélées par les optimisations de "
        "gcc 9. (*Signalé par Christian Lange et Ned T. Crigler.*)"
    ),
    (
        "- PostgreSQL 12 support.\n"
        "- Add `info` command `set` option for detailed text output. The "
        "additional details include databases that can be used for selective "
        "restore and a list of tablespaces and symlinks with their default "
        "destinations. (*Contributed by Cynthia Shang. Reviewed by David Steele. "
        "Suggested by Stephen Frost, ejberdecia.*)\n"
        "- Add `standby` restore type. This restore type automatically adds "
        "standby_mode=on to recovery.conf for PostgreSQL < 12 and creates "
        "`standby.signal` for PostgreSQL ≥ 12, creating a common interface "
        "between PostgreSQL versions. (*Reviewed by Cynthia Shang.*)"
    ): (
        "- Prise en charge de PostgreSQL 12.\n"
        "- Ajouter l'option `set` de la commande `info` pour produire une sortie "
        "texte détaillée. Les informations supplémentaires comprennent les bases "
        "de données utilisables pour une restauration sélective, ainsi qu'une "
        "liste des tablespaces et des liens symboliques avec leurs destinations "
        "par défaut. (*Contribution de Cynthia Shang. Révisé par David Steele. "
        "Suggéré par Stephen Frost et ejberdecia.*)\n"
        "- Ajouter le type de restauration `standby`. Il ajoute automatiquement "
        "standby_mode=on à recovery.conf pour PostgreSQL < 12 et crée "
        "`standby.signal` pour PostgreSQL ≥ 12, fournissant ainsi une interface "
        "commune aux versions de PostgreSQL. (*Révisé par Cynthia Shang.*)"
    ),
    (
        "- Skip `pg_internal.init` temp file during backup. (*Reviewed by "
        "Cynthia Shang. Suggested by Michael Paquier.*)\n"
        "- Add more validations to the manifest on `backup`. (*Reviewed by "
        "Cynthia Shang.*)"
    ): (
        "- Ignorer le fichier temporaire `pg_internal.init` pendant la sauvegarde. "
        "(*Révisé par Cynthia Shang. Suggéré par Michael Paquier.*)\n"
        "- Ajouter davantage de validations du manifeste lors de `backup`. "
        "(*Révisé par Cynthia Shang.*)"
    ),
    (
        "- Fix `restore` delta link mapping when path/file already exists. "
        "(*Reviewed by Reid Thompson. Reported by Younes Alhroub.*)\n"
        "- Fix socket leak on connection retries. (*Reviewed by Reid Thompson. "
        "Reported by James Coleman.*)"
    ): (
        "- Corriger le mappage des liens delta de `restore` lorsque le chemin ou "
        "le fichier existe déjà. (*Révisé par Reid Thompson. Signalé par Younes "
        "Alhroub.*)\n"
        "- Corriger la fuite de socket lors des nouvelles tentatives de connexion. "
        "(*Révisé par Reid Thompson. Signalé par James Coleman.*)"
    ),
    (
        "- Default `log-level-stderr` option to `off`. (*Reviewed by Greg Sabino "
        "Mullane, Stefan Fercot.*)\n"
        "- Allow alternative WAL segment sizes for PostgreSQL ≤ 10. "
        "(*Contributed by Viktor Kurilko. Reviewed by David Steele.*)\n"
        "- Add hint to check SFTP authorization log. (*Contributed by Vitalii "
        "Zurian. Reviewed by Reid Thompson, David Steele.*)"
    ): (
        "- Définir l'option `log-level-stderr` sur `off` par défaut. (*Révisé "
        "par Greg Sabino Mullane et Stefan Fercot.*)\n"
        "- Autoriser d'autres tailles de segment WAL pour PostgreSQL ≤ 10. "
        "(*Contribution de Viktor Kurilko. Révisé par David Steele.*)\n"
        "- Ajouter une indication invitant à consulter le journal d'autorisation "
        "SFTP. (*Contribution de Vitalii Zurian. Révisé par Reid Thompson et "
        "David Steele.*)"
    ),
    (
        "- Suppress `unused parameter` errors in meson compiler probes. "
        "(*Contributed by Jörg Plate. Reviewed by David Steele.*)\n"
        "- C11 is now the minimum C standard. (*Reviewed by Mohammad Ali Nazir "
        "Kosar.*)"
    ): (
        "- Supprimer les erreurs `unused parameter` des sondes du compilateur "
        "meson. (*Contribution de Jörg Plate. Révisé par David Steele.*)\n"
        "- C11 est désormais la norme C minimale. (*Révisé par Mohammad Ali "
        "Nazir Kosar.*)"
    ),
    (
        "- Fix `expire` removing a backup in progress on another host. "
        "(*Reviewed by Douglas J Hunley. Reported by Dmitrii.*)\n"
        "- Fix `archive-push-queue-max` not enforced when a WAL file errors. "
        "(*Reviewed by Stefan Fercot. Reported by vut12.*)\n"
        "- Fix async `archive-get` failure during recovery across a timeline "
        "switch. (*Reviewed by Douglas J Hunley. Reported by Jimmy Yih.*)\n"
        "- Fix potential buffer overrun in error module. (*Fixed by Christophe "
        "Pettus. Reviewed by David Steele.*)\n"
        "- Fix use-after-free of parallel protocol client. (*Reviewed by Douglas "
        "J Hunley. Reported by Georgy Shelkovy.*)\n"
        "- Fix heap overflow when a pg option is set without pg1. (*Reviewed by "
        "Douglas J Hunley. Reported by Naveen.*)"
    ): (
        "- Corriger la suppression par `expire` d'une sauvegarde en cours sur un "
        "autre hôte. (*Révisé par Douglas J Hunley. Signalé par Dmitrii.*)\n"
        "- Corriger la non-application de `archive-push-queue-max` lorsqu'un "
        "fichier WAL provoque une erreur. (*Révisé par Stefan Fercot. Signalé par "
        "vut12.*)\n"
        "- Corriger l'échec asynchrone de `archive-get` pendant une récupération "
        "traversant un changement de timeline. (*Révisé par Douglas J Hunley. "
        "Signalé par Jimmy Yih.*)\n"
        "- Corriger un possible dépassement de tampon dans le module d'erreur. "
        "(*Corrigé par Christophe Pettus. Révisé par David Steele.*)\n"
        "- Corriger une utilisation après libération du client du protocole "
        "parallèle. (*Révisé par Douglas J Hunley. Signalé par Georgy Shelkovy.*)\n"
        "- Corriger un dépassement de tas lorsqu'une option pg est définie sans "
        "pg1. (*Révisé par Douglas J Hunley. Signalé par Naveen.*)"
    ),
    (
        "Bundle (combine) smaller files to reduce the total number of files "
        "written to the repository. Writing fewer files is generally more "
        "efficient, especially on object stores such as S3. In addition, "
        "zero-length files are not stored (except in the manifest), which saves "
        "time and space."
    ): (
        "Regrouper les petits fichiers afin de réduire le nombre total de "
        "fichiers écrits dans le dépôt. Écrire moins de fichiers est généralement "
        "plus efficace, en particulier sur les magasins d'objets tels que S3. "
        "En outre, les fichiers vides ne sont pas stockés, sauf dans le manifeste, "
        "ce qui économise du temps et de l'espace."
    ),
    (
        "- `y` - Standby is required for backup.\n"
        "- `prefer` - Backup from standby if available otherwise backup from "
        "primary.\n"
        "- `n` - Backup from primary only."
    ): (
        "- `y` - un serveur standby est obligatoire pour la sauvegarde.\n"
        "- `prefer` - effectuer la sauvegarde depuis le serveur standby s'il est "
        "disponible, sinon depuis le primaire.\n"
        "- `n` - effectuer la sauvegarde uniquement depuis le primaire."
    ),
    (
        "The asynchronous `archive-push` command writes acknowledgements into "
        "the spool path when it has successfully stored WAL in the archive (and "
        "errors on failure) so the foreground process can quickly notify "
        "PostgreSQL. Acknowledgement files are very small (zero on success and a "
        "few hundred bytes on error)."
    ): (
        "La commande asynchrone `archive-push` écrit des accusés de réception "
        "dans le répertoire de spool après avoir correctement stocké le WAL dans "
        "l'archive, ou une erreur en cas d'échec, afin que le processus au premier "
        "plan puisse informer rapidement PostgreSQL. Ces fichiers sont très "
        "petits : vides en cas de succès et de quelques centaines d'octets en cas "
        "d'erreur."
    ),
    (
        "The '`database size`' is the full uncompressed size of the database "
        "while '`database backup size`' is the amount of data in the database "
        "to actually back up (these will be the same for full backups)."
    ): (
        "La '`database size`' correspond à la taille totale non compressée de "
        "la base de données, tandis que la '`database backup size`' représente la "
        "quantité de données à sauvegarder réellement ; elles sont identiques pour "
        "les sauvegardes complètes."
    ),
    (
        "[Percona](https://percona.com) is an open source database software, "
        "support, and services company focused on helping organizations maintain "
        "full control over their data infrastructure. They help businesses run "
        "MySQL, PostgreSQL, MongoDB, Valkey, and Redis securely and efficiently "
        "through freely available open source software, 24/7 expert support, and "
        "hands-on database expertise."
    ): (
        "[Percona](https://percona.com) est une entreprise de logiciels, "
        "d'assistance et de services open source qui aide les organisations à "
        "conserver le contrôle total de leur infrastructure de données. Elle leur "
        "permet d'exploiter MySQL, PostgreSQL, MongoDB, Valkey et Redis de manière "
        "sûre et efficace grâce à des logiciels open source librement accessibles, "
        "une assistance experte 24/7 et une expertise pratique des bases de "
        "données."
    ),
    (
        "[pgEdge](https://pgedge.com) is an enterprise-class open source "
        "Postgres platform for AI, high availability and more, with Agentic AI "
        "native tooling and DBA workbench, monitoring and incident response, "
        "flexible deployment, and zero downtime maintenance. It scales from a "
        "single node to active-active multi-master within the cloud, on-premises, "
        "or air-gapped environments."
    ): (
        "[pgEdge](https://pgedge.com) est une plateforme PostgreSQL open source "
        "de classe entreprise pour l'IA, la haute disponibilité et bien plus "
        "encore. Elle propose des outils natifs d'IA agentique, un atelier DBA, "
        "la supervision et la réponse aux incidents, un déploiement flexible et "
        "une maintenance sans interruption. Elle s'étend d'un nœud unique à une "
        "architecture multimaître active-active dans le cloud, sur site ou dans "
        "des environnements isolés."
    ),
    (
        "The push and get commands both ensure that the database and repository "
        "match by comparing PostgreSQL versions and system identifiers. This "
        "virtually eliminates the possibility of misconfiguring the WAL archive "
        "location."
    ): (
        "Les commandes push et get garantissent chacune la correspondance entre "
        "la base de données et le dépôt en comparant les versions de PostgreSQL "
        "et les identifiants système. Cela élimine pratiquement tout risque de "
        "configurer incorrectement l'emplacement de l'archive WAL."
    ),
    (
        "Dedicated commands are included for pushing WAL to the archive and "
        "getting WAL from the archive. Both commands support parallelism to "
        "accelerate processing and run asynchronously to provide the fastest "
        "possible response time to PostgreSQL."
    ): (
        "Des commandes dédiées permettent d'envoyer le WAL vers l'archive et "
        "de le récupérer. Ces commandes prennent en charge le parallélisme afin "
        "d'accélérer le traitement et s'exécutent de manière asynchrone pour offrir "
        "à PostgreSQL le temps de réponse le plus court possible."
    ),
    (
        "- misconfigured `archive_command`\n"
        "- misconfigured pgBackRest configuration files\n"
        "- network or permissions issue\n"
        "- third party product (e.g. S3, Swift or Minio) configuration issue\n"
        "- large amount of WAL queueing to be archived"
    ): (
        "- `archive_command` mal configuré\n"
        "- fichiers de configuration pgBackRest incorrectement configurés\n"
        "- problème de réseau ou d'autorisations\n"
        "- problème de configuration d'un produit tiers, par exemple S3, Swift "
        "ou MinIO\n"
        "- grande quantité de WAL en attente d'archivage"
    ),
    (
        "  Previously, when stopping Patroni, *systemd* also sent a signal to "
        "PostgreSQL. Since Patroni also tried to stop PostgreSQL by itself, it "
        "resulted in sending to different shutdown requests (the smart shutdown, "
        "followed by the fast shutdown). That resulted in replicas disconnecting "
        "too early and a former master not being able to rejoin after demote. "
        "Fix by Jan with prior research by Alexander."
    ): (
        "  Auparavant, lors de l'arrêt de Patroni, *systemd* envoyait également "
        "un signal à PostgreSQL. Comme Patroni tentait lui aussi d'arrêter "
        "PostgreSQL, des demandes d'arrêt différentes étaient envoyées : l'arrêt "
        "intelligent, puis l'arrêt rapide. Les réplicas se déconnectaient alors "
        "trop tôt et l'ancien primaire ne pouvait plus rejoindre le cluster après "
        "sa rétrogradation. Correctif de Jan, fondé sur les recherches préalables "
        "d'Alexander."
    ),
    "  Both changes make Patroni connections to DCS more robust in the face of network issues.": (
        "  Ces modifications rendent les connexions de Patroni au DCS plus "
        "robustes face aux problèmes réseau."
    ),
    (
        "  Patroni has a lot of logic in place to prevent failover in such "
        "case; it can also restore all keys back; however, until this change an "
        "accidental removal of /config key was switching off pause mode for 1 "
        "cycle of HA loop."
    ): (
        "  Patroni dispose de nombreux mécanismes pour empêcher un basculement "
        "dans ce cas et peut aussi restaurer toutes les clés. Toutefois, avant "
        "cette modification, la suppression accidentelle de la clé /config "
        "désactivait le mode pause pendant un cycle de la boucle HA."
    ),
    (
        "  If `register_service` parameter in the consul "
        "[configuration](/patroni/config/yaml#consul_settings) is enabled, the "
        "node will register a service with the name `scope` and the tag "
        "`master`, `replica` or `standby-leader`."
    ): (
        "  Si le paramètre `register_service` de la "
        "[configuration Consul](/patroni/config/yaml#consul_settings) est "
        "activé, le nœud enregistre un service nommé `scope` avec le tag "
        "`master`, `replica` ou `standby-leader`."
    ),
    "- Do a smart comparison of actual and desired `primary_conninfo` values on replicas (Alexander Kukushkin)": (
        "- Comparer intelligemment les valeurs réelles et souhaitées de "
        "`primary_conninfo` sur les réplicas (Alexander Kukushkin)"
    ),
    "- Use `spawn` multiprocessing start method on python 3.4+ (Maciej Kowalczyk)": (
        "- Utiliser la méthode de démarrage multiprocessing `spawn` avec Python "
        "3.4+ (Maciej Kowalczyk)"
    ),
    "- Put `*` into `pgpass` instead of missing or empty values (Alexander Kukushkin)": (
        "- Insérer `*` dans `pgpass` à la place des valeurs absentes ou vides "
        "(Alexander Kukushkin)"
    ),
    (
        "  The IPv6 address is supposed to be enclosed into square brackets, "
        "but Patroni was expecting to get it plain. Now both formats are "
        "supported."
    ): (
        "  L'adresse IPv6 est censée être placée entre crochets, alors que "
        "Patroni s'attendait à la recevoir sans crochets. Ces formats sont "
        "désormais tous pris en charge."
    ),
    (
        "  Unlike callbacks, the `pre_promote` script is called synchronously "
        "after acquiring the leader lock, but before promoting Postgres. If the "
        "script fails or exits with a non-zero exitcode, the current node will "
        "release the leader lock."
    ): (
        "  Contrairement aux callbacks, le script `pre_promote` est appelé de "
        "manière synchrone après l'acquisition du verrou de leader, mais avant la "
        "promotion de PostgreSQL. Si le script échoue ou renvoie un code de sortie "
        "non nul, le nœud actuel libère le verrou de leader."
    ),
    (
        "  On Windows it would be the `more.com`. In addition to that, `cdiff` "
        "was changed to `ydiff` in `requirements.txt`, but "
        "[patronictl](/patroni/patronictl#patronictl) still supports both for "
        "compatibility."
    ): (
        "  Sous Windows, il s'agit de `more.com`. En outre, `cdiff` a été "
        "remplacé par `ydiff` dans `requirements.txt`, mais "
        "[patronictl](/patroni/patronictl#patronictl) continue de prendre en "
        "charge chacun d'eux à des fins de compatibilité."
    ),
    "  There were chances that Patroni was sleeping up to twice longer between running HA code.": (
        "  Patroni pouvait dormir jusqu'à deux fois plus longtemps entre les "
        "exécutions du code HA."
    ),
    (
        "  It is possible to specify `wal_keep_segments` as a string in the "
        "global [dynamic configuration](/patroni/config/dynamic#dynamic) and "
        "due to Python being a dynamically typed language the string was simply "
        "multiplied. Example: `wal_keep_segments: \"100\"` was converted to "
        "`100100100100100100100100100100100100100100100100MB`."
    ): (
        "  Il est possible de définir `wal_keep_segments` sous forme de chaîne "
        "dans la [configuration dynamique](/patroni/config/dynamic#dynamic) "
        "globale. Python étant un langage à typage dynamique, la chaîne était "
        "simplement multipliée. Par exemple, `wal_keep_segments: \"100\"` était "
        "converti en `100100100100100100100100100100100100100100100100MB`."
    ),
    (
        "  Provide extended information about the PostgreSQL parameters that "
        "caused `pending_restart` flag to be set. Both `patronictl list` and "
        "`/patroni` REST API endpoint now show the parameters names and their "
        "\"diff\" as `pending_restart_reason`."
    ): (
        "  Fournit des informations détaillées sur les paramètres PostgreSQL "
        "ayant déclenché l'indicateur `pending_restart`. Aussi bien `patronictl "
        "list` que le point de terminaison REST `/patroni` affichent désormais "
        "les noms des paramètres et leur « diff » dans "
        "`pending_restart_reason`."
    ),
    "- Check that `postgresql.parameters` is a dictionary (Alexander Kukushkin)": (
        "- Vérifier que `postgresql.parameters` est un dictionnaire "
        "(Alexander Kukushkin)"
    ),
    "`--group`  \nRebuild a replica member of the given Citus group.": (
        "`--group`  \nReconstruit un membre réplica du groupe Citus indiqué."
    ),
    "`TIME` is the interval between re-runs, in seconds.": (
        "`TIME` indique, en secondes, l'intervalle séparant les réexécutions."
    ),
    (
        "> [!WARNING]\n"
        "> Provide only one of `nofailover` or `failover_priority`. Providing "
        "`nofailover: true` is the same as `failover_priority: 0`, and providing "
        "`nofailover: false` will give the node priority 1."
    ): (
        "> [!WARNING]\n"
        "> Renseignez uniquement `nofailover` ou `failover_priority`. "
        "`nofailover: true` équivaut à `failover_priority: 0`, tandis que "
        "`nofailover: false` attribue au nœud la priorité 1."
    ),
    (
        "- **mode**: `off`, `automatic` or `required`. When `off` watchdog is "
        "disabled. When `automatic` watchdog will be used if available, but "
        "ignored if it is not. When `required` the node will not become a "
        "leader unless watchdog can be successfully enabled.\n"
        "- **device**: Path to watchdog device. Defaults to `/dev/watchdog`.\n"
        "- **safety_margin**: Number of seconds of safety margin between "
        "watchdog triggering and leader key expiration."
    ): (
        "- **mode** : `off`, `automatic` ou `required`. Avec `off`, le watchdog "
        "est désactivé. Avec `automatic`, il est utilisé s'il est disponible et "
        "ignoré sinon. Avec `required`, le nœud ne devient leader que si le "
        "watchdog peut être activé.\n"
        "- **device** : chemin du périphérique watchdog. Valeur par défaut : "
        "`/dev/watchdog`.\n"
        "- **safety_margin** : marge de sécurité, en secondes, entre le "
        "déclenchement du watchdog et l'expiration de la clé de leader."
    ),
    (
        "- **cacert**: (optional) Specifies the file with the CA_BUNDLE file "
        "with certificates of trusted CAs to use while verifying Kubernetes API "
        "SSL certs. If not provided, patroni will use the value provided by the "
        "ServiceAccount secret.\n"
        "- **retriable_http_codes**: (optional) list of HTTP status codes from "
        "K8s API to retry on. By default Patroni is retrying on `500`, `503`, "
        "and `504`, or if K8s API response has `retry-after` HTTP header."
    ): (
        "- **cacert** : (facultatif) indique le fichier CA_BUNDLE contenant les "
        "certificats des autorités de certification approuvées pour vérifier les "
        "certificats SSL de l'API Kubernetes. En l'absence de valeur, Patroni "
        "utilise celle du secret ServiceAccount.\n"
        "- **retriable_http_codes** : (facultatif) liste des codes d'état HTTP "
        "de l'API K8s pour lesquels une nouvelle tentative doit être effectuée. "
        "Par défaut, Patroni réessaie pour `500`, `503` et `504`, ou lorsque la "
        "réponse de l'API K8s contient l'en-tête HTTP `retry-after`."
    ),
    (
        "  - **pg_hba**: list of lines that Patroni will use to generate "
        "`pg_hba.conf`. Patroni ignores this parameter if `hba_file` PostgreSQL "
        "parameter is set to a non-default value. Together with "
        "[dynamic configuration](/patroni/config/dynamic#dynamic) this parameter "
        "simplifies management of `pg_hba.conf`."
    ): (
        "  - **pg_hba** : liste des lignes que Patroni utilisera pour générer "
        "`pg_hba.conf`. Patroni ignore ce paramètre si le paramètre PostgreSQL "
        "`hba_file` possède une valeur différente de celle par défaut. Associé à "
        "la [configuration dynamique](/patroni/config/dynamic#dynamic), ce "
        "paramètre simplifie la gestion de `pg_hba.conf`."
    ),
    (
        "- **self_addr**: `ip:port` to listen on for Raft connections. The "
        "`self_addr` must be accessible from other nodes of the cluster. If not "
        "set, the node will not participate in consensus."
    ): (
        "- **self_addr** : adresse `ip:port` d'écoute des connexions Raft. "
        "`self_addr` doit être accessible depuis les autres nœuds du cluster. "
        "Sans cette valeur, le nœud ne participe pas au consensus."
    ),
    (
        "Most of the parameters are optional, but you have to specify one of "
        "the **host** or **url**"
    ): (
        "La plupart des paramètres sont facultatifs, mais vous devez renseigner "
        "**host** ou **url**."
    ),
    (
        "- **PATRONI_CTL_CACERT**: (optional) Specifies the file with the "
        "CA_BUNDLE file or directory with certificates of trusted CAs to use "
        "while verifying REST API SSL certs. If not provided "
        "[patronictl](/patroni/patronictl#patronictl) will use the value provided "
        "for REST API \"cafile\" parameter.\n"
        "- **PATRONI_CTL_CERTFILE**: (optional) Specifies the file with the "
        "client certificate in the PEM format.\n"
        "- **PATRONI_CTL_KEYFILE**: (optional) Specifies the file with the client "
        "secret key in the PEM format."
    ): (
        "- **PATRONI_CTL_CACERT** : (facultatif) indique le fichier CA_BUNDLE "
        "ou le répertoire contenant les certificats des autorités de certification "
        "approuvées pour vérifier les certificats SSL de l'API REST. En l'absence "
        "de valeur, [patronictl](/patroni/patronictl#patronictl) utilise le "
        "paramètre \"cafile\" de l'API REST.\n"
        "- **PATRONI_CTL_CERTFILE** : (facultatif) indique le fichier du "
        "certificat client au format PEM.\n"
        "- **PATRONI_CTL_KEYFILE** : (facultatif) indique le fichier de la clé "
        "secrète du client au format PEM."
    ),
    (
        "- **PATRONI_RESTAPI_CAFILE**: Specifies the file with the CA_BUNDLE "
        "with certificates of trusted CAs to use while verifying client certs.\n"
        "- **PATRONI_RESTAPI_CIPHERS**: (optional) Specifies the permitted "
        "cipher suites (e.g. \"ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-"
        "SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:"
        "!SSLv2:!SSLv3:!TLSv1:!TLSv1.1\")"
    ): (
        "- **PATRONI_RESTAPI_CAFILE** : indique le fichier CA_BUNDLE contenant "
        "les certificats des autorités de certification approuvées pour vérifier "
        "les certificats clients.\n"
        "- **PATRONI_RESTAPI_CIPHERS** : (facultatif) indique les suites de "
        "chiffrement autorisées, par exemple \"ECDHE-RSA-AES256-GCM-SHA384:DHE-"
        "RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-"
        "SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1\"."
    ),
    (
        "- **PATRONI_KUBERNETES_CACERT**: (optional) Specifies the file with "
        "the CA_BUNDLE file with certificates of trusted CAs to use while "
        "verifying Kubernetes API SSL certs. If not provided, patroni will use "
        "the value provided by the ServiceAccount secret.\n"
        "- **PATRONI_RETRIABLE_HTTP_CODES**: (optional) list of HTTP status "
        "codes from K8s API to retry on. By default Patroni is retrying on "
        "`500`, `503`, and `504`, or if K8s API response has `retry-after` HTTP "
        "header."
    ): (
        "- **PATRONI_KUBERNETES_CACERT** : (facultatif) indique le fichier "
        "CA_BUNDLE contenant les certificats des autorités de certification "
        "approuvées pour vérifier les certificats SSL de l'API Kubernetes. En "
        "l'absence de valeur, Patroni utilise celle du secret ServiceAccount.\n"
        "- **PATRONI_RETRIABLE_HTTP_CODES** : (facultatif) liste des codes "
        "d'état HTTP de l'API K8s pour lesquels une nouvelle tentative doit être "
        "effectuée. Par défaut, Patroni réessaie pour `500`, `503` et `504`, ou "
        "lorsque la réponse de l'API K8s contient l'en-tête HTTP `retry-after`."
    ),
    (
        "- **PATRONI_RESTAPI_CAFILE**: Specifies the file with the CA_BUNDLE "
        "with certificates of trusted CAs to use while verifying client certs.\n"
        "- **PATRONI_RESTAPI_CIPHERS**: (optional) Specifies the permitted "
        "cipher suites (e.g. \"ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-"
        "SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:"
        "!SSLv2:!SSLv3:!TLSv1:!TLSv1.1\")\n"
        "- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (default), `optional` or "
        "`required`. When `none` REST API will not check client certificates. "
        "When `required` client certificates are required for all REST API "
        "calls. When `optional` client certificates are required for all unsafe "
        "REST API endpoints. When `required` is used, then client authentication "
        "succeeds, if the certificate signature verification succeeds. For "
        "`optional` the client cert will only be checked for `PUT`, `POST`, "
        "`PATCH`, and `DELETE` requests."
    ): (
        "- **PATRONI_RESTAPI_CAFILE** : indique le fichier CA_BUNDLE contenant "
        "les certificats des autorités de certification approuvées pour vérifier "
        "les certificats clients.\n"
        "- **PATRONI_RESTAPI_CIPHERS** : (facultatif) indique les suites de "
        "chiffrement autorisées, par exemple \"ECDHE-RSA-AES256-GCM-SHA384:DHE-"
        "RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-"
        "SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1\".\n"
        "- **PATRONI_RESTAPI_VERIFY_CLIENT** : `none` (valeur par défaut), "
        "`optional` ou `required`. Avec `none`, l'API REST ne vérifie pas les "
        "certificats clients. Avec `required`, ils sont obligatoires pour tous "
        "les appels à l'API REST. Avec `optional`, ils ne sont obligatoires que "
        "pour les points de terminaison REST non sécurisés. Lorsque `required` "
        "est utilisé, l'authentification réussit si la signature du certificat "
        "est valide. Avec `optional`, le certificat client n'est vérifié que pour "
        "les requêtes `PUT`, `POST`, `PATCH` et `DELETE`."
    ),
    (
        "- **PATRONI_RAFT_SELF_ADDR**: `ip:port` to listen on for Raft "
        "connections. The `self_addr` must be accessible from other nodes of "
        "the cluster. If not set, the node will not participate in consensus.\n"
        "- **PATRONI_RAFT_BIND_ADDR**: (optional) `ip:port` to listen on for "
        "Raft connections. If not specified the `self_addr` will be used.\n"
        "- **PATRONI_RAFT_PARTNER_ADDRS**: list of other Patroni nodes in the "
        "cluster in format `\"'ip1:port1','ip2:port2'\"`. It is important to "
        "quote every single entity!\n"
        "- **PATRONI_RAFT_DATA_DIR**: directory where to store Raft log and "
        "snapshot. If not specified the current working directory is used.\n"
        "- **PATRONI_RAFT_PASSWORD**: (optional) Encrypt Raft traffic with a "
        "specified password, requires `cryptography` python module.\n"
        "- **PATRONI_RAFT_MIN_TIMEOUT**: (optional) minimum election timeout in "
        "seconds for the underlying pysyncobj Raft implementation. Must be "
        "greater than 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Default: `0.4`."
    ): (
        "- **PATRONI_RAFT_SELF_ADDR** : adresse `ip:port` d'écoute des "
        "connexions Raft. `self_addr` doit être accessible depuis les autres "
        "nœuds du cluster. Sans cette valeur, le nœud ne participe pas au consensus.\n"
        "- **PATRONI_RAFT_BIND_ADDR** : (facultatif) adresse `ip:port` d'écoute "
        "des connexions Raft. En l'absence de valeur, `self_addr` est utilisé.\n"
        "- **PATRONI_RAFT_PARTNER_ADDRS** : liste des autres nœuds Patroni du "
        "cluster au format `\"'ip1:port1','ip2:port2'\"`. Chaque élément doit "
        "impérativement être placé entre guillemets !\n"
        "- **PATRONI_RAFT_DATA_DIR** : répertoire de stockage du journal et des "
        "instantanés Raft. Le répertoire de travail courant est utilisé par défaut.\n"
        "- **PATRONI_RAFT_PASSWORD** : (facultatif) chiffre le trafic Raft avec "
        "le mot de passe indiqué ; requiert le module Python `cryptography`.\n"
        "- **PATRONI_RAFT_MIN_TIMEOUT** : (facultatif) délai minimal d'élection, "
        "en secondes, pour l'implémentation Raft pysyncobj sous-jacente. Il doit "
        "être supérieur à 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Valeur par "
        "défaut : `0.4`."
    ),
    (
        "How can I change my local configuration?  \n"
        "You need to change the configuration file of the corresponding "
        "Patroni member and signal the Patroni agent with `SIHGUP`. You can do "
        "that using either of these approaches:"
    ): (
        "Comment puis-je modifier ma configuration locale ?  \n"
        "Vous devez modifier le fichier de configuration du membre Patroni "
        "concerné, puis envoyer `SIHGUP` à l'agent Patroni. Vous pouvez utiliser "
        "l'une des deux méthodes suivantes :"
    ),
    (
        "As you may noticed, both examples have `citus-group` label set. This "
        "label allows Patroni to identify object as belonging to a certain "
        "Citus group. In addition to that, there is also `PATRONI_CITUS_GROUP` "
        "environment variable, which has the same value as the `citus-group` "
        "label. When Patroni creates new Kubernetes objects ConfigMaps or "
        "Endpoints, it automatically puts the "
        "`citus-group: ${env.PATRONI_CITUS_GROUP}` label on them:"
    ): (
        "Comme vous l'avez peut-être remarqué, les deux exemples définissent "
        "le libellé `citus-group`. Celui-ci permet à Patroni d'identifier "
        "l'appartenance d'un objet à un groupe Citus donné. La variable "
        "d'environnement `PATRONI_CITUS_GROUP` porte la même valeur que ce "
        "libellé. Lorsque Patroni crée de nouveaux objets Kubernetes, ConfigMaps "
        "ou Endpoints, il leur ajoute automatiquement le libellé "
        "`citus-group: ${env.PATRONI_CITUS_GROUP}` :"
    ),
    (
        "5.  Current superuser [credentials]"
        "(/patroni/config/yaml#postgresql_settings) will be added to the "
        "`pg_dist_authinfo` table to allow cross-node communication. Don't "
        "forget to update them if later you decide to change superuser "
        "username/password/sslcert/sslkey!\n"
        "6.  The coordinator primary node will automatically discover worker "
        "primary nodes and add them to the `pg_dist_node` table using the "
        "`citus_add_node()` function.\n"
        "7.  Patroni will also maintain `pg_dist_node` in case "
        "failover/switchover on the coordinator or worker clusters occurs."
    ): (
        "5.  Les [identifiants](/patroni/config/yaml#postgresql_settings) "
        "actuels du superutilisateur seront ajoutés à la table "
        "`pg_dist_authinfo` pour permettre la communication entre les nœuds. "
        "N'oubliez pas de les mettre à jour si vous modifiez ensuite le nom "
        "d'utilisateur, le mot de passe, le certificat SSL ou la clé SSL du "
        "superutilisateur !\n"
        "6.  Le nœud primaire du coordinateur découvrira automatiquement les "
        "nœuds primaires workers et les ajoutera à la table `pg_dist_node` au "
        "moyen de la fonction `citus_add_node()`.\n"
        "7.  Patroni maintiendra également `pg_dist_node` lors des basculements "
        "automatiques ou planifiés des clusters coordinateur ou workers."
    ),
    (
        "Generate a Patroni configuration in `yaml` format for the locally "
        "running PostgreSQL instance. Either the provided DSN (takes "
        "precedence) or PostgreSQL [environment variables]"
        "(https://www.postgresql.org/docs/current/libpq-envars.html) will be "
        "used for the PostgreSQL connection. If the password is not provided, "
        "it should be entered via prompt."
    ): (
        "Générez une configuration Patroni au format `yaml` pour l'instance "
        "PostgreSQL exécutée localement. Le DSN fourni, qui est prioritaire, ou "
        "les [variables d'environnement]"
        "(https://www.postgresql.org/docs/current/libpq-envars.html) de "
        "PostgreSQL serviront à la connexion. Si aucun mot de passe n'est fourni, "
        "vous devrez le saisir à l'invite."
    ),
    (
        "1.  **Last known sync nodes are available in the `/sync` key in DCS**: "
        "Patroni sets or keeps `synchronous_standby_names` to the nodes stored "
        "there. For example, if `/sync` contains "
        "`leader=node1, sync_standby=node2,node3` and both standbys stop "
        "streaming, Patroni will continue using:"
    ): (
        "1.  **Les derniers nœuds synchrones connus sont disponibles dans la "
        "clé `/sync` du DCS** : Patroni définit ou conserve "
        "`synchronous_standby_names` avec les nœuds qui y sont enregistrés. "
        "Par exemple, si `/sync` contient "
        "`leader=node1, sync_standby=node2,node3` et que les deux réplicas "
        "cessent leur réplication, Patroni continuera d'utiliser :"
    ),
    (
        "Using PostgreSQL synchronous replication does not guarantee zero lost "
        "transactions under all circumstances. When the primary and the "
        "secondary that is currently acting as a synchronous replica fail "
        "simultaneously a third node that might not contain all transactions "
        "will be promoted."
    ): (
        "L'utilisation de la réplication synchrone PostgreSQL ne garantit pas "
        "l'absence totale de transactions perdues en toutes circonstances. Si "
        "le primaire et le secondaire servant actuellement de réplica synchrone "
        "tombent en panne simultanément, un troisième nœud ne contenant peut-être "
        "pas toutes les transactions sera promu."
    ),
    (
        "2.  Specify one of `psycopg`, `psycopg2`, or `psycopg2-binary` in "
        "the [list of dependencies](/patroni/installation#extras) when "
        "installing Patroni with pip."
    ): (
        "2.  Indiquez `psycopg`, `psycopg2` ou `psycopg2-binary` dans la "
        "[liste des dépendances](/patroni/installation#extras) lors de "
        "l'installation de Patroni avec pip."
    ),
    (
        "  Before enabling the `failsafe_mode` please make sure that Patroni "
        "version on all members is up-to-date. After that, you can use either "
        "the `PATCH /config` [REST API](/patroni/rest_api#rest_api) or "
        "[patronictl edit-config -s failsafe_mode=true]"
        "(/patroni/patronictl#patronictl_edit_config_parameters)"
    ): (
        "  Avant d'activer `failsafe_mode`, assurez-vous que tous les membres "
        "utilisent une version à jour de Patroni. Vous pouvez ensuite employer "
        "soit l'[API REST](/patroni/rest_api#rest_api) `PATCH /config`, soit "
        "[patronictl edit-config -s failsafe_mode=true]"
        "(/patroni/patronictl#patronictl_edit_config_parameters)."
    ),
    (
        "We introduce a new special option, the `failsafe_mode`. It could be "
        "enabled only via global [dynamic configuration](/patroni/config/dynamic#dynamic) "
        "stored in the DCS `/config` key. If the failsafe mode is enabled and "
        "the leader lock update in DCS failed due to reasons different from the "
        "version/value/index mismatch, Postgres may continue to run as a primary "
        "if it can access all known members of the cluster via Patroni REST API."
    ): (
        "Nous introduisons une option spéciale, `failsafe_mode`. Elle ne peut être "
        "activée que par la [configuration dynamique](/patroni/config/dynamic#dynamic) "
        "globale stockée dans la clé DCS `/config`. Si le mode de secours est "
        "activé et que la mise à jour du verrou de leader dans le DCS échoue pour "
        "une raison autre qu'une discordance de version, de valeur ou d'index, "
        "PostgreSQL peut continuer à fonctionner comme primaire s'il peut joindre "
        "tous les membres connus du cluster via l'API REST de Patroni."
    ),
    (
        "- Add the standby_cluster section back and it will trigger `pg_rewind`; "
        "however, for `pg_rewind` to function properly, either the cluster must "
        "be initialized with `data page checksums` (`--data-checksums` option "
        "for `initdb`) and/or `wal_log_hints` must be set to `on`, but there are "
        "still chances that `pg_rewind` might fail due to other factors.\n"
        "- Rebuild the standby cluster from scratch."
    ): (
        "- Rétablissez la section standby_cluster ; cela déclenchera `pg_rewind`. "
        "Pour que `pg_rewind` fonctionne correctement, le cluster doit avoir été "
        "initialisé avec `data page checksums` (option `--data-checksums` de "
        "`initdb`) et/ou `wal_log_hints` doit être défini sur `on`. D'autres "
        "facteurs peuvent toutefois encore faire échouer `pg_rewind`.\n"
        "- Reconstruisez entièrement le cluster standby."
    ),
    (
        "Continue with the [command-line reference](command-line/) and "
        "[PostgreSQL logging configuration](postgresql-logging/)."
    ): (
        "Poursuivez avec la [référence de la ligne de commande](command-line/) "
        "et la [configuration de la journalisation PostgreSQL](postgresql-logging/)."
    ),
    (
        "- Features\n"
        "  * Support hot reloading of TLS settings.  When the configuration\n"
        "    file is reloaded, changed TLS settings automatically take effect.\n"
        "  * Add support for abstract Unix-domain sockets.  Prefix a\n"
        "    Unix-domain socket path with `@` to use a socket in the abstract\n"
        "    namespace.  This matches the corresponding PostgreSQL 14 feature.\n"
        "  * The maximum lengths of passwords and user names have been\n"
        "    increased to 996 and 128, respectively.  Various cloud services\n"
        "    require this.\n"
        "  * The minimum pool size can now be set per database, similar to the\n"
        "    regular pool size and the reserve pool size.\n"
        "  * The number of pending query cancellations is shown in `SHOW\n"
        "    POOLS`."
    ): (
        "- Fonctionnalités\n"
        "  * Prise en charge du rechargement à chaud des paramètres TLS. Lorsque le fichier\n"
        "    de configuration est rechargé, les paramètres TLS modifiés prennent automatiquement effet.\n"
        "  * Ajout de la prise en charge des sockets de domaine Unix abstraits. Préfixez le\n"
        "    chemin d'un socket de domaine Unix par `@` pour utiliser l'espace de noms abstrait.\n"
        "    Cette fonction correspond à celle introduite dans PostgreSQL 14.\n"
        "  * Les longueurs maximales des mots de passe et des noms d'utilisateur ont été\n"
        "    portées respectivement à 996 et 128. Plusieurs services cloud l'exigent.\n"
        "  * La taille minimale du pool peut désormais être définie par base de données, comme\n"
        "    la taille normale du pool et celle du pool de réserve.\n"
        "  * Le nombre d'annulations de requêtes en attente est affiché dans `SHOW\n"
        "    POOLS`."
    ),
    (
        "The administration interface of **pgbouncer** consists of some new\n"
        "`SHOW` commands available when connected to a special \"virtual\"\n"
        "database **pgbouncer**."
    ): (
        "L’interface d’administration de **pgbouncer** propose de nouvelles "
        "commandes `SHOW`, disponibles lorsque l’on se connecte à une base "
        "de données « virtuelle » spéciale nommée **pgbouncer**."
    ),
    (
        "- Fixes\n"
        "  * Fail `sbuf_send_pending` operation if destination socket is closed\n"
        "    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))\n"
        "  * Fix a few possible crashes\n"
        "    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),\n"
        "    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))\n"
        "  * Fix for overflow bug in comma-separated host list feature, causing\n"
        "    connection to get re-routed to Unix socket\n"
        "    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))\n"
        "  * Don't evict connections to achieve `min_pool_size`\n"
        "    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))\n"
        "  * Fix `SHOW HELP` with PostgreSQL 15\n"
        "    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))\n"
        "  * Fix race condition in query cancellation handling.  It was possible\n"
        "    that a query cancellation for one client canceled a query for\n"
        "    another one.  This could happen when a cancel request was received\n"
        "    by PgBouncer when the query it was meant to cancel already\n"
        "    completed by itself.\n"
        "    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))"
    ): (
        "- Correctifs\n"
        "  * Faire échouer l'opération `sbuf_send_pending` si le socket de destination est fermé\n"
        "    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))\n"
        "  * Corriger plusieurs plantages possibles\n"
        "    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),\n"
        "    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))\n"
        "  * Corriger un dépassement dans la liste d'hôtes séparés par des virgules, qui\n"
        "    redirigeait la connexion vers un socket Unix\n"
        "    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))\n"
        "  * Ne pas évincer de connexions pour atteindre `min_pool_size`\n"
        "    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))\n"
        "  * Corriger `SHOW HELP` avec PostgreSQL 15\n"
        "    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))\n"
        "  * Corriger une condition de concurrence dans la gestion de l'annulation des requêtes.\n"
        "    L'annulation d'une requête d'un client pouvait annuler celle d'un autre client\n"
        "    lorsque PgBouncer recevait la demande d'annulation après que la requête visée\n"
        "    s'était déjà terminée.\n"
        "    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))"
    ),
    (
        "- us: microseconds. 1 microsecond = 1/1000000 second\n"
        "- ms: milliseconds. 1 millisecond = 1/1000 second. This is the default.\n"
        "- s : seconds. 1s = 1000ms\n"
        "- m : minutes. 1m = 60s = 60000ms\n"
        "- h : hours. 1h = 60m = 3600s = 3600000ms\n"
        "- d : days. 1d = 24h = 1440m = 86400s = 86400000ms"
    ): (
        "- us : microsecondes. 1us = 1/1000000s\n"
        "- ms : millisecondes. 1ms = 1/1000s. Il s'agit de l'unité par défaut.\n"
        "- s : secondes. 1s = 1000ms\n"
        "- m : minutes. 1m = 60s = 60000ms\n"
        "- h : heures. 1h = 60m = 3600s = 3600000ms\n"
        "- d : jours. 1d = 24h = 1440m = 86400s = 86400000ms"
    ),
    (
        "'sockpair@`<n>`' following address is the file descriptor of a connected unix socket or of a\n"
        "socketpair. During a connection, the initiator creates a pair of connected sockets, and passes one\n"
        "of them over the FD to the other end. The listener waits to receive the FD from the unix socket and\n"
        "uses it as if it were the FD of an accept(). Should be used carefully."
    ): (
        "'sockpair@`<n>`' : l'adresse qui suit est le descripteur de fichier d'un socket Unix connecté ou "
        "d'une paire de sockets. Lors d'une connexion, l'initiateur crée une paire de sockets connectés et "
        "transmet l'un d'eux à l'autre extrémité via le descripteur. L'écouteur attend de recevoir ce "
        "descripteur depuis le socket Unix et l'utilise comme celui renvoyé par accept(). Cette option doit "
        "être utilisée avec précaution."
    ),
    (
        "'unix@`<path>`' following string is considered as a UNIX socket `<path>`. this prefix is useful to\n"
        "declare an UNIX socket path which don't start by slash '/'."
    ): (
        "'unix@`<path>`' : la chaîne qui suit est considérée comme le chemin `<path>` d'un socket Unix. "
        "Ce préfixe permet de déclarer un chemin de socket Unix qui ne commence pas par une barre oblique '/'."
    ),
    (
        "'uxdg@`<path>`' following string is considered as a unix socket `<path>` but transport method is\n"
        "forced to \"datagram\". It is considered as an alias of 'dgram+unix@'."
    ): (
        "'uxdg@`<path>`' : la chaîne qui suit est considérée comme le chemin `<path>` d'un socket Unix, "
        "mais la méthode de transport est forcée à \"datagram\". Ce préfixe est un alias de 'dgram+unix@'."
    ),
    (
        "'uxst@`<path>`' following string is considered as a unix socket `<path>` but transport method is\n"
        "forced to \"stream\". It is considered as an alias of 'stream+unix@'."
    ): (
        "'uxst@`<path>`' : la chaîne qui suit est considérée comme le chemin `<path>` d'un socket Unix, "
        "mais la méthode de transport est forcée à \"stream\". Ce préfixe est un alias de 'stream+unix@'."
    ),
    (
        "Delete a CRL file tree entry from HAProxy. The CRL file must be unused and removed from any\n"
        "crt-list. \"show ssl crl-file\" displays the status of the CRL files. The deletion doesn't work with a\n"
        "certificate referenced directly with the \"crl-file\" directive in the configuration."
    ): (
        "Supprime une entrée de l'arborescence des fichiers CRL de HAProxy. Le fichier CRL doit être "
        "inutilisé et retiré de toute crt-list. La commande « show ssl crl-file » affiche l'état des "
        "fichiers CRL. La suppression ne fonctionne pas avec un certificat référencé directement par la "
        "directive « crl-file » dans la configuration."
    ),
    (
        "This setting is only available when support for OpenSSL was built in. It sets the default string\n"
        "describing the list of signature algorithms related to client authentication for all \"bind\" lines\n"
        "which do not explicitly define theirs. The format of the string is a colon-delimited list of\n"
        "signature algorithms. Each signature algorithm can use one of two forms: TLS1.3 signature scheme\n"
        "names (\"rsa_pss_rsae_sha256\") or the public key algorithm + digest form (\"ECDSA+SHA256\"). A list can\n"
        "contain both forms. For more information on the format, see SSL_CTX_set1_client_sigalgs(3). A list\n"
        "of signature algorithms is also available in RFC8446 section 4.2.3 and in OpenSSL in the\n"
        "ssl/t1_lib.c file. This setting is not applicable to TLSv1.1 and earlier versions of the protocol as\n"
        "the signature algorithms aren't separately negotiated in these versions. It is not recommended to\n"
        "change this setting unless compatibility with a middlebox is required."
    ): (
        "Ce paramètre n'est disponible que si la prise en charge d'OpenSSL a été intégrée. Il définit la "
        "chaîne par défaut décrivant les algorithmes de signature liés à l'authentification du client pour "
        "toutes les lignes \"bind\" qui ne définissent pas explicitement leur propre liste. La chaîne est une "
        "liste d'algorithmes de signature séparés par des deux-points. Chaque algorithme peut prendre l'une "
        "des deux formes suivantes : un nom de schéma de signature TLS1.3 (\"rsa_pss_rsae_sha256\") ou la "
        "forme algorithme de clé publique + condensat (\"ECDSA+SHA256\"). Une même liste peut contenir les "
        "deux formes. Pour plus d'informations sur le format, consultez SSL_CTX_set1_client_sigalgs(3). Une "
        "liste d'algorithmes de signature figure également dans la section 4.2.3 de RFC8446 et dans le "
        "fichier ssl/t1_lib.c d'OpenSSL. Ce paramètre ne s'applique pas à TLSv1.1 ni aux versions antérieures "
        "du protocole, car les algorithmes de signature n'y sont pas négociés séparément. Il est déconseillé "
        "de le modifier, sauf si la compatibilité avec un boîtier intermédiaire l'exige."
    ),
    (
        "This setting is only available when support for OpenSSL was built in. It sets the default string\n"
        "describing the list of signature algorithms that are negotiated during the TLSv1.2 and TLSv1.3\n"
        "handshake for all \"bind\" lines which do not explicitly define theirs. The format of the string is a\n"
        "colon-delimited list of signature algorithms. Each signature algorithm can use one of two forms:\n"
        "TLS1.3 signature scheme names (\"rsa_pss_rsae_sha256\") or the public key algorithm + digest form\n"
        "(\"ECDSA+SHA256\"). A list can contain both forms. For more information on the format, see\n"
        "SSL_CTX_set1_sigalgs(3). A list of signature algorithms is also available in RFC8446 section 4.2.3\n"
        "and in OpenSSL in the ssl/t1_lib.c file. This setting is not applicable to TLSv1.1 and earlier\n"
        "versions of the protocol as the signature algorithms aren't separately negotiated in these versions.\n"
        "It is not recommended to change this setting unless compatibility with a middlebox is required."
    ): (
        "Ce paramètre n'est disponible que si la prise en charge d'OpenSSL a été intégrée. Il définit la "
        "chaîne par défaut décrivant les algorithmes de signature négociés pendant les échanges TLSv1.2 et "
        "TLSv1.3 pour toutes les lignes \"bind\" qui ne définissent pas explicitement leur propre liste. La "
        "chaîne est une liste d'algorithmes de signature séparés par des deux-points. Chaque algorithme peut "
        "prendre l'une des deux formes suivantes : un nom de schéma de signature TLS1.3 "
        "(\"rsa_pss_rsae_sha256\") ou la forme algorithme de clé publique + condensat (\"ECDSA+SHA256\"). Une "
        "même liste peut contenir les deux formes. Pour plus d'informations sur le format, consultez "
        "SSL_CTX_set1_sigalgs(3). Une liste d'algorithmes de signature figure également dans la section "
        "4.2.3 de RFC8446 et dans le fichier ssl/t1_lib.c d'OpenSSL. Ce paramètre ne s'applique pas à "
        "TLSv1.1 ni aux versions antérieures du protocole, car les algorithmes de signature n'y sont pas "
        "négociés séparément. Il est déconseillé de le modifier, sauf si la compatibilité avec un boîtier "
        "intermédiaire l'exige."
    ),
    (
        "This setting is only available when support for OpenSSL was built in. It sets the default string\n"
        "describing the list of signature algorithms related to client authentication for all \"server\" lines\n"
        "which do not explicitly define theirs. The format of the string is a colon-delimited list of\n"
        "signature algorithms. Each signature algorithm can use one of two forms: TLS1.3 signature scheme\n"
        "names (\"rsa_pss_rsae_sha256\") or the public key algorithm + digest form (\"ECDSA+SHA256\"). A list can\n"
        "contain both forms. For more information on the format, see SSL_CTX_set1_client_sigalgs(3). A list\n"
        "of signature algorithms is also available in RFC8446 section 4.2.3 and in OpenSSL in the\n"
        "ssl/t1_lib.c file. This setting is not applicable to TLSv1.1 and earlier versions of the protocol as\n"
        "the signature algorithms aren't separately negotiated in these versions. It is not recommended to\n"
        "change this setting unless compatibility with a middlebox is required."
    ): (
        "Ce paramètre n'est disponible que si la prise en charge d'OpenSSL a été intégrée. Il définit la "
        "chaîne par défaut décrivant les algorithmes de signature liés à l'authentification du client pour "
        "toutes les lignes \"server\" qui ne définissent pas explicitement leur propre liste. La chaîne est "
        "une liste d'algorithmes de signature séparés par des deux-points. Chaque algorithme peut prendre "
        "l'une des deux formes suivantes : un nom de schéma de signature TLS1.3 "
        "(\"rsa_pss_rsae_sha256\") ou la forme algorithme de clé publique + condensat (\"ECDSA+SHA256\"). Une "
        "même liste peut contenir les deux formes. Pour plus d'informations sur le format, consultez "
        "SSL_CTX_set1_client_sigalgs(3). Une liste d'algorithmes de signature figure également dans la "
        "section 4.2.3 de RFC8446 et dans le fichier ssl/t1_lib.c d'OpenSSL. Ce paramètre ne s'applique pas "
        "à TLSv1.1 ni aux versions antérieures du protocole, car les algorithmes de signature n'y sont pas "
        "négociés séparément. Il est déconseillé de le modifier, sauf si la compatibilité avec un boîtier "
        "intermédiaire l'exige."
    ),
    (
        "This setting is only available when support for OpenSSL was built in. It sets the default string\n"
        "describing the list of signature algorithms that are negotiated during the TLSv1.2 and TLSv1.3\n"
        "handshake for all \"server\" lines which do not explicitly define theirs. The format of the string is\n"
        "a colon-delimited list of signature algorithms. Each signature algorithm can use one of two forms:\n"
        "TLS1.3 signature scheme names (\"rsa_pss_rsae_sha256\") or the public key algorithm + digest form\n"
        "(\"ECDSA+SHA256\"). A list can contain both forms. For more information on the format, see\n"
        "SSL_CTX_set1_sigalgs(3). A list of signature algorithms is also available in RFC8446 section 4.2.3\n"
        "and in OpenSSL in the ssl/t1_lib.c file. This setting is not applicable to TLSv1.1 and earlier\n"
        "versions of the protocol as the signature algorithms aren't separately negotiated in these versions.\n"
        "It is not recommended to change this setting unless compatibility with a middlebox is required."
    ): (
        "Ce paramètre n'est disponible que si la prise en charge d'OpenSSL a été intégrée. Il définit la "
        "chaîne par défaut décrivant les algorithmes de signature négociés pendant les échanges TLSv1.2 et "
        "TLSv1.3 avec le serveur pour toutes les lignes \"server\" qui ne définissent pas explicitement leur "
        "propre liste. La chaîne est une liste d'algorithmes de signature séparés par des deux-points. Chaque "
        "algorithme peut prendre l'une des deux formes suivantes : un nom de schéma de signature TLS1.3 "
        "(\"rsa_pss_rsae_sha256\") ou la forme algorithme de clé publique + condensat (\"ECDSA+SHA256\"). Une "
        "même liste peut contenir les deux formes. Pour plus d'informations sur le format, consultez "
        "SSL_CTX_set1_sigalgs(3). Une liste d'algorithmes de signature figure également dans la section "
        "4.2.3 de RFC8446 et dans le fichier ssl/t1_lib.c d'OpenSSL. Ce paramètre ne s'applique pas à TLSv1.1 "
        "ni aux versions antérieures du protocole, car les algorithmes de signature n'y sont pas négociés "
        "séparément. Il est déconseillé de le modifier, sauf si la compatibilité avec un boîtier intermédiaire "
        "l'exige."
    ),
    (
        "This converter also manages tokens that have an algorithm (\"alg\" field of the JOSE header) in the\n"
        "RSA family (RSA-OAEP or RSA-OAEP-256) when provided an 'RSA' JWK, or in the ECDH family (ECDH-ES,\n"
        "ECDH-ES+A128KW, ECDH-ES+A192KW or ECDH-ES+A256KW) when provided an 'EC' JWK. The RSA1_5 algorithm is\n"
        "implemented but disabled by default following what is suggested in [section 3.2](/haproxy/global/#section-3-2) of RFC 8725. It can\n"
        "be reenabled if needed thanks to 'jwt.decrypt_alg_list' global option."
    ): (
        "Ce convertisseur gère également les jetons dont l'algorithme (champ \"alg\" de l'en-tête JOSE) "
        "appartient à la famille RSA (RSA-OAEP ou RSA-OAEP-256) lorsqu'une JWK 'RSA' est fournie, ou à la "
        "famille ECDH (ECDH-ES, ECDH-ES+A128KW, ECDH-ES+A192KW ou ECDH-ES+A256KW) lorsqu'une JWK 'EC' est "
        "fournie. L'algorithme RSA1_5 est implémenté, mais désactivé par défaut conformément à la "
        "[section 3.2](/haproxy/global/#section-3-2) de RFC 8725. Il peut être réactivé si nécessaire grâce "
        "à l'option globale 'jwt.decrypt_alg_list'."
    ),
    (
        "Converts RFC7239 node (provided by 'for' or 'by' 7239 header fields) into its corresponding nodename\n"
        "final form: - ipv4 address - ipv6 address - 'unknown' - '\\_obfs' identifier"
    ): (
        "Convertit le nœud RFC7239, fourni par les champs d'en-tête 7239 'for' ou 'by', dans la forme "
        "finale correspondante de son nom de nœud : - adresse IPv4 - adresse IPv6 - 'unknown' - "
        "identifiant '\\_obfs'"
    ),
    (
        "Converts RFC7239 node (provided by 'for' or 'by' 7239 header fields) into its corresponding nodeport\n"
        "final form: - unsigned integer - '\\_obfs' identifier"
    ): (
        "Convertit le nœud RFC7239, fourni par les champs d'en-tête 7239 'for' ou 'by', dans la forme "
        "finale correspondante de son port de nœud : - entier non signé - identifiant '\\_obfs'"
    ),
    "int: refer to the SPOE documentation for the encoding str: ``` <int:length>``<bytes> ```": (
        "int : consultez la documentation SPOE pour le codage ; str : ``` <int:length>``<bytes> ```"
    ),
    (
        "    * In H1 only, tests on the HTTP version will be relaxed. It will allow\n"
        "      HTTP/0.9 GET requests to pass through (no version specified), as well as\n"
        "      different protocol names (e.g. RTSP), and multiple digits for both the\n"
        "      major and the minor version."
    ): (
        "    * Dans H1 uniquement, les contrôles de la version HTTP seront assouplis. Les requêtes GET "
        "HTTP/0.9 pourront ainsi être transmises sans version spécifiée, tout comme les requêtes utilisant "
        "d'autres noms de protocole, par exemple RTSP, ou plusieurs chiffres pour les versions majeure et "
        "mineure."
    ),
    (
        " 1. Install etcd from pre-built binaries or from source. For details, see\n"
        "    [Install][]."
    ): (
        " 1. Installez etcd à partir de binaires précompilés ou du code source. Pour plus de détails, "
        "consultez [Installation][Install]."
    ),
    (
        "The `etcdctl` and etcd API do not enforce a specific password length during user creation or user password update operations. It is the responsibility of the administrator to enforce these requirements. For avoiding security risks related to password strength, [TLS Common Name based authentication](#using-tls-common-name) and users created with `--no-password` option can be utilized."
    ): (
        "Les API `etcdctl` et etcd n'imposent aucune longueur de mot de passe particulière lors de la "
        "création d'un utilisateur ou de la mise à jour de son mot de passe. Il incombe à l'administrateur "
        "d'appliquer ces exigences. Pour réduire les risques liés aux mots de passe faibles, utilisez "
        "[l'authentification fondée sur le nom commun TLS](#using-tls-common-name) ainsi que des utilisateurs "
        "créés avec l'option `--no-password`."
    ),
    (
        "Increasing the cluster size can enhance [failure tolerance][fault tolerance table] and provide better read performance. Since clients can read from any member, increasing the number of members increases the overall serialized read throughput."
    ): (
        "L'augmentation de la taille du cluster peut améliorer la [tolérance aux pannes][fault tolerance table] "
        "et les performances de lecture. Comme les clients peuvent lire depuis n'importe quel membre, "
        "l'augmentation du nombre de membres accroît le débit global des lectures sérialisées."
    ),
    (
        " * Add the new member to the cluster via the [HTTP members API][member-api], the [gRPC members API][member-api-grpc], or the `etcdctl member add` command.\n"
        " * Start the new member with the new cluster configuration, including a list of the updated members (existing members + the new member)."
    ): (
        " * Ajoutez le nouveau membre au cluster au moyen de l'[API HTTP des membres][member-api], de "
        "l'[API gRPC des membres][member-api-grpc] ou de la commande `etcdctl member add`.\n"
        " * Démarrez le nouveau membre avec la nouvelle configuration du cluster, y compris la liste "
        "actualisée des membres (membres existants + nouveau membre)."
    ),
    " * Add the new member as learner via [gRPC members API][member-api-grpc] or the `etcdctl member add --learner` command.": (
        " * Ajoutez le nouveau membre comme apprenant au moyen de l'[API gRPC des membres][member-api-grpc] "
        "ou de la commande `etcdctl member add --learner`."
    ),
    (
        "> [!NOTE]\n"
        "> Duration fields such as `--grpc-keepalive-min-time`, `--grpc-keepalive-interval`,\n"
        "> `--grpc-keepalive-timeout`, `--backend-batch-interval`, `--corrupt-check-time`,\n"
        "> `--compact-hash-check-time`, `--compaction-sleep-interval`,\n"
        "> `--watch-progress-notify-interval`, `--warning-apply-duration`,\n"
        "> `--warning-unary-request-duration`, and `--downgrade-check-time` accept\n"
        "> human-readable strings (e.g. `10m`, `5s`) when passed as command-line flags, but\n"
        "> in a configuration file they only accept **integer values representing\n"
        "> nanoseconds**. This is a [known Go standard library limitation](https://github.com/golang/go/issues/10275)\n"
        "> where `time.Duration` is unmarshaled as a plain integer.\n"
        ">\n"
        "> For example, to set a 10-minute watch progress notify interval in a config file:\n"
        ">\n"
        "> ```yaml\n"
        "> # Correct: 10 minutes in nanoseconds\n"
        "> watch-progress-notify-interval: 600000000000\n"
        ">\n"
        "> # Incorrect: will produce an unmarshal error\n"
        "> watch-progress-notify-interval: '10m'\n"
        "> ```"
    ): (
        "> [!NOTE]\n"
        "> Les champs de durée tels que `--grpc-keepalive-min-time`, `--grpc-keepalive-interval`,\n"
        "> `--grpc-keepalive-timeout`, `--backend-batch-interval`, `--corrupt-check-time`,\n"
        "> `--compact-hash-check-time`, `--compaction-sleep-interval`,\n"
        "> `--watch-progress-notify-interval`, `--warning-apply-duration`,\n"
        "> `--warning-unary-request-duration` et `--downgrade-check-time` acceptent\n"
        "> des chaînes lisibles (par exemple `10m`, `5s`) comme options de ligne de commande, mais\n"
        "> dans un fichier de configuration, ils n'acceptent que des **valeurs entières représentant\n"
        "> des nanosecondes**. Il s'agit d'une [limitation connue de la bibliothèque standard Go](https://github.com/golang/go/issues/10275),\n"
        "> où `time.Duration` est désérialisé comme un entier simple.\n"
        ">\n"
        "> Par exemple, pour définir un intervalle de notification de progression de 10 minutes dans un fichier de configuration :\n"
        ">\n"
        "> ```yaml\n"
        "> # Correct : 10 minutes en nanosecondes\n"
        "> watch-progress-notify-interval: 600000000000\n"
        ">\n"
        "> # Incorrect : provoque une erreur de désérialisation\n"
        "> watch-progress-notify-interval: '10m'\n"
        "> ```"
    ),
    (
        "How this applies to membership: If a 3-member cluster has 1 downed member, it can still make forward progress because the quorum is 2 and 2 members are still live. However, adding a new member to a 3-member cluster will increase the quorum to 3 because 3 votes are required for a majority of 4 members. Since the quorum increased, this extra member buys nothing in terms of fault tolerance; the cluster is still one node failure away from being unrecoverable."
    ): (
        "Application à la gestion des membres : si un cluster de 3 membres compte 1 membre hors service, "
        "il peut encore progresser, car le quorum est de 2 et 2 membres restent actifs. Toutefois, l'ajout "
        "d'un membre à un cluster de 3 membres porte le quorum à 3, puisque 3 voix sont nécessaires pour "
        "obtenir la majorité parmi 4 membres. Ce membre supplémentaire n'améliore donc pas la tolérance aux "
        "pannes : le cluster reste à 1 panne de nœud de devenir irrécupérable."
    ),
    (
        "Only [old versions of gRPC](https://github.com/grpc/grpc-go/issues/1362) log this. etcd [>=v3.2.13 by default log this with DEBUG level](https://github.com/etcd-io/etcd/pull/9080), thus only visible with `--log-level=debug` flag enabled."
    ): (
        "Seules les [anciennes versions de gRPC](https://github.com/grpc/grpc-go/issues/1362) "
        "journalisent cet avertissement. [À partir de v3.2.13, etcd le journalise par défaut au niveau "
        "DEBUG](https://github.com/etcd-io/etcd/pull/9080) ; il n'est donc visible que lorsque l'option "
        "`--log-level=debug` est activée."
    ),
    (
        "[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) and [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) fixes TLS reload when [certificate SAN field only includes IP addresses but no domain names](https://github.com/etcd-io/etcd/issues/9541). For example, a member is set up with CSRs (with `cfssl`) as below:"
    ): (
        "[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) et "
        "[v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) corrigent le "
        "rechargement TLS lorsque [le champ SAN du certificat ne contient que des adresses IP, sans nom "
        "de domaine](https://github.com/etcd-io/etcd/issues/9541). Par exemple, un membre est configuré "
        "avec les CSR suivantes (avec `cfssl`) :"
    ),
    "<p style=\"text-decoration:underline;\">Note2: We persist TTLs in seconds (from the undefined 'now'). Crash-looping server does not release leases!!!</p>": (
        "<p style=\"text-decoration:underline;\">Note2 : les TTL sont conservés en secondes (à partir "
        "de la valeur « now » non définie). Un serveur pris dans une boucle de redémarrage ne libère pas "
        "les baux !!!</p>"
    ),
    (
        "* A new file is created every (approximately) --snapshotCount=(by default 100'000) applied proposals. It’s an approximation as we might receive proposals in batches and we consider snapshotting only at the end of batch, finally the snapshotting process is asynchronously scheduled.\n"
        "  The flag name (--snapshotCount) is pretty misleading as it drives [differences in index value between ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)last snapshot index and last applied proposal index."
    ): (
        "* Un nouveau fichier est créé toutes les --snapshotCount= propositions appliquées environ "
        "(100'000 par défaut). Cette valeur est approximative : les propositions peuvent arriver par lots, "
        "la création d'un instantané n'est envisagée qu'à la fin du lot et le processus est finalement "
        "planifié de manière asynchrone.\n"
        "  Le nom de l'option (--snapshotCount) est assez trompeur : elle contrôle la [différence de valeur "
        "d'index entre ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)le dernier index d'instantané et le dernier index de proposition appliquée."
    ),
    (
        "> [!IMPORTANT]\n"
        "> pgBadger embeds a modified `SQL::Beautify` module under Artistic License 2.0, and its\n"
        "> generated-report resources include MIT, GPL-2.0, and SIL Open Font License 1.1 components. The\n"
        "> complete upstream resource inventory is retained as\n"
        "> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).\n"
        "> The [sample reports](/pgbadger/sample-reports/) published here are historical generated\n"
        "> artifacts and keep their original embedded notices."
    ): (
        "> [!IMPORTANT]\n"
        "> pgBadger intègre un module `SQL::Beautify` modifié sous Artistic License 2.0 ; les ressources\n"
        "> de ses rapports générés comprennent aussi des composants sous licence MIT, GPL-2.0 et SIL Open\n"
        "> Font License 1.1. L'inventaire complet des ressources en amont est conservé dans\n"
        "> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).\n"
        "> Les [rapports d'exemple](/pgbadger/sample-reports/) publiés ici sont des artefacts historiques\n"
        "> générés qui conservent leurs mentions d'origine."
    ),
    (
        "[^0]: Startup parameters are: `client_encoding`, `DateStyle`, `IntervalStyle`, `Timezone`, `standard_conforming_strings`, and `application_name`. PgBouncer detects their changes and so it can guarantee they remain consistent for the client. If you need PgBouncer to support more than these, take a look at [`track_extra_parameters`](/pgbouncer/config/#track_extra_parameters) and [`ignore_startup_parameters`](/pgbouncer/config/#ignore_startup_parameters)."
    ): (
        "[^0]: Les paramètres de démarrage sont `client_encoding`, `DateStyle`, `IntervalStyle`, `Timezone`, "
        "`standard_conforming_strings` et `application_name`. PgBouncer détecte leurs modifications et peut "
        "ainsi garantir leur cohérence pour le client. Pour prendre en charge d'autres paramètres, consultez "
        "[`track_extra_parameters`](/pgbouncer/config/#track_extra_parameters) et "
        "[`ignore_startup_parameters`](/pgbouncer/config/#ignore_startup_parameters)."
    ),
    (
        "[^1]: You need to change [`max_prepared_statements`](/pgbouncer/config/#max_prepared_statements) to a non-zero value to enable this support."
    ): (
        "[^1]: Vous devez définir [`max_prepared_statements`](/pgbouncer/config/#max_prepared_statements) "
        "sur une valeur non nulle pour activer cette prise en charge."
    ),
}


def configure_language(language: str) -> None:
    """Select language-specific prompts, paths, and small source rewrites."""

    global STYLE_GUIDE
    global DEFAULT_CACHE
    global TARGET_LANGUAGE
    global TARGET_SUFFIX
    global USABLE_IN_TRANSLATION
    global MANUAL_TRANSLATIONS
    global CATEGORY_MAP

    TARGET_LANGUAGE = language
    if language == "zh":
        STYLE_GUIDE = CHINESE_STYLE_GUIDE
        DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache.json"
        TARGET_SUFFIX = ".zh.md"
        USABLE_IN_TRANSLATION = "适用范围："
        MANUAL_TRANSLATIONS = CHINESE_MANUAL_TRANSLATIONS
        CATEGORY_MAP = CHINESE_CATEGORY_MAP
        return
    if language == "fr":
        STYLE_GUIDE = FRENCH_STYLE_GUIDE
        DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache-fr.json"
        TARGET_SUFFIX = ".fr.md"
        USABLE_IN_TRANSLATION = "Utilisable dans :"
        MANUAL_TRANSLATIONS = FRENCH_MANUAL_TRANSLATIONS
        CATEGORY_MAP = {
            "Concept": "Concept",
            "Task": "Tâche",
            "Reference": "Référence",
            "Tutorial": "Tutoriel",
        }
        return
    if language == "ja":
        STYLE_GUIDE = JAPANESE_STYLE_GUIDE
        DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache-ja.json"
        TARGET_SUFFIX = ".ja.md"
        USABLE_IN_TRANSLATION = "使用可能なセクション："
        MANUAL_TRANSLATIONS = JAPANESE_MANUAL_TRANSLATIONS
        CATEGORY_MAP = {
            "Concept": "概念",
            "Task": "タスク",
            "Reference": "リファレンス",
            "Tutorial": "チュートリアル",
        }
        return
    raise RuntimeError(f"unsupported target language: {language}")

ASCII_WORD_RE = re.compile(r"[A-Za-z]{2,}")
NUMBER_TOKEN_RE = re.compile(
    r"(?<!\w)(?:"
    r"(?:v|V)\d+(?:\.\d+)*(?:[-+][A-Za-z0-9.-]+)?"
    r"|\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?"
    r"(?!\s?(?:(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB)\b|%))"
    r"|\d+(?:\.\d+)?(?:\s?(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|纳秒|微秒|毫秒|秒|分钟|小时|天|字节|%))?"
    r")(?!\w)"
)
HEADING_RE = re.compile(
    r"^(?P<marks>#{1,6})(?P<space>\s+)(?P<title>.*?)(?P<anchor>\s+\{#[^}]+\})?\s*$"
)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
REFERENCE_DEF_RE = re.compile(r"^\s*\[(?!\^)[^]]+\]:\s+\S+")
ANCHOR_ONLY_RE = re.compile(r'^\s*<a\s+(?:id|name)="[^"]+"\s*></a>\s*$')
ATTRIBUTION_RE = re.compile(r"^[ \t]+\([A-Z][A-Za-z .'-]+\)[ \t]*$")


@dataclass
class Cache:
    path: Path
    entries: dict[str, str]

    @classmethod
    def load(cls, path: Path) -> "Cache":
        if not path.is_file():
            return cls(path, {})
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(f"cannot read translation cache {path}: {exc}") from exc
        if not isinstance(payload, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in payload.items()
        ):
            raise RuntimeError(f"invalid translation cache format: {path}")
        return cls(path, payload)

    def get(self, key: str) -> str | None:
        return self.entries.get(key)

    def put(self, key: str, value: str) -> None:
        self.entries[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(self.entries, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        os.replace(temporary, self.path)


def alpha_index(number: int) -> str:
    """Return an all-letter base-26 index so number protection cannot match it."""
    chars: list[str] = []
    number += 1
    while number:
        number, remainder = divmod(number - 1, 26)
        chars.append(chr(ord("A") + remainder))
    return "".join(reversed(chars))


class Protector:
    def __init__(self) -> None:
        self.values: list[str] = []

    def token(self, value: str) -> str:
        token = f"__PGSQL_P{alpha_index(len(self.values))}__"
        self.values.append(value)
        return token

    def substitute(self, pattern: re.Pattern[str] | str, text: str) -> str:
        regex = re.compile(pattern) if isinstance(pattern, str) else pattern
        return regex.sub(lambda match: self.token(match.group(0)), text)

    def protect(self, text: str) -> str:
        # Protect larger Markdown constructs before their nested literals.
        # List and quote prefixes are syntax, not prose. Protect them before
        # translating short fragments so the model cannot drop or renumber a
        # one-line list or flatten an admonition.
        text = re.sub(
            r"(?m)^[ \t]*(?:>+[ \t]*)?(?:[-+*]|\d{1,2}[.)])[ \t]+",
            lambda match: self.token(match.group(0)),
            text,
        )
        text = re.sub(
            r"(?m)^(?P<label>[A-Za-z_][A-Za-z0-9_.-]*)"
            r"(?=\n[ \t]*:[ \t]+)",
            lambda match: self.token(match.group(0)),
            text,
        )
        text = re.sub(
            r"(?m)^[ \t]*:[ \t]+",
            lambda match: self.token(match.group(0)),
            text,
        )
        text = re.sub(
            r"(?m)^[ \t]*\[\^[^\]\n]+\]:[ \t]+",
            lambda match: self.token(match.group(0)),
            text,
        )
        text = re.sub(
            r"(?m)^[ \t]*>+[ \t]?",
            lambda match: self.token(match.group(0)),
            text,
        )
        text = self.substitute(
            r"'(?=[^'\n]*@)[^'\n]*`[^`\n]*`[^'\n]*'",
            text,
        )
        text = self.substitute(r"`+[^`]*`+", text)
        text = self.substitute(r"\{#[A-Za-z0-9_.:-]+\}", text)
        text = self.substitute(r"\{\{[%<].*?[>%]\}\}", text)
        text = self.substitute(r"<(?:code|kbd)\b[^>\n]*>.*?</(?:code|kbd)>", text)
        text = self.substitute(
            re.compile(r"\[(?P<url>https?://[^\]\n]+)\]\((?P=url)\)"),
            text,
        )
        text = self.substitute(
            re.compile(
                r'<a\b[^>\n]*href="(?P<url>https?://[^"]+)"[^>]*>'
                r'(?P=url)</a>'
            ),
            text,
        )
        text = self.substitute(r"</?[A-Za-z][^>\n]*>", text)
        text = self.substitute(
            r'(["\'])(?=[A-Za-z0-9_.\\-]*[_.\\])[A-Za-z0-9_.\\-]+\1',
            text,
        )
        text = self.substitute(r"([\"'])[*?@#;]\1", text)
        text = self.substitute(r"&(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);", text)
        text = self.substitute(r"\[![A-Za-z]+\]", text)
        text = self.substitute(r"\[\^[^\]\n]+\]", text)
        # Keep link labels translatable while making both Markdown boundaries
        # mandatory. Protecting only the destination lets models drop labels.
        inline_link_re = re.compile(r"(?P<image>!?)\[(?P<label>[^]\n]*)\]\((?P<dest>[^)\n]+)\)")
        text = inline_link_re.sub(
            lambda match: (
                self.token(f'{match.group("image")}[')
                + match.group("label")
                + self.token(f']({match.group("dest")})')
            ),
            text,
        )
        reference_link_re = re.compile(r"(?P<image>!?)\[(?P<label>[^]\n]*)\]\[(?P<ref>[^]\n]*)\]")
        text = reference_link_re.sub(
            lambda match: (
                self.token(f'{match.group("image")}[')
                + match.group("label")
                + self.token(f'][{match.group("ref")}]')
            ),
            text,
        )
        text = self.substitute(r"https?://[^\s)>\]}]+", text)
        text = self.substitute(r"mailto:[^\s)>\]}]+", text)

        text = self.substitute(
            r"(?<![\w/])(?:"
            r"(?:\.\.?/)+(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+|"
            r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9_.-]+|"
            r"(?:[A-Za-z0-9_.-]+/){2,}[A-Za-z0-9_.-]+"
            r")",
            text,
        )
        text = self.substitute(
            r"(?<![\w/])[A-Za-z0-9_.-]+\."
            r"(?:ini|conf|cfg|yaml|yml|json|toml|txt|service|socket|pid|log|"
            r"pem|crt|key|sql|py|go|c|h|md)\b",
            text,
        )

        # Unquoted protobuf/RPC field labels are part of the API surface, not prose.
        field_label_re = re.compile(
            r"(?m)^(?P<marker>\s*[-+*]\s+)"
            r"(?P<label>[A-Z][A-Za-z0-9_]*(?:,\s*[A-Z][A-Za-z0-9_]*)*)"
            r"(?=\s+-\s+)"
        )
        text = field_label_re.sub(
            lambda match: match.group("marker") + self.token(match.group("label")),
            text,
        )

        # Preserve operational literals that are often not marked as code upstream.
        text = self.substitute(r"(?<![\w-])--?[A-Za-z0-9][A-Za-z0-9_.-]*(?:=[^\s,;]+)?", text)
        text = self.substitute(r"(?<!\w)/[A-Za-z0-9_./${}*?+-]+", text)
        text = self.substitute(r"\b(?:[A-Z][A-Z0-9]*_)+[A-Z0-9]+\b", text)
        text = self.substitute(r"\b[A-Z]{2,}\d+(?:\.\d+)*\b", text)
        text = self.substitute(r"\b(?:db|repo|pg)\d+\b", text)
        text = self.substitute(r"\bL[2-7]\b", text)
        text = self.substitute(r"\b(?i:layer)[2-7](?:-[A-Za-z]+)?\b", text)
        return text

    def restore(self, text: str, *, protected_source: str | None = None) -> str:
        text = re.sub(
            r"(__PGSQL_P[A-Z]+__)PGSQL_(P[A-Z]+__)",
            r"\1__PGSQL_\2",
            text,
        )
        # Later substitutions may wrap earlier placeholders (for example a
        # protected path containing a protected filename). Unwrap from the
        # outside in so nested literals become visible before validation.
        for index, value in reversed(list(enumerate(self.values))):
            token = f"__PGSQL_P{alpha_index(index)}__"
            count = text.count(token)
            structural_prefix = bool(
                re.fullmatch(
                    r"[ \t]*(?:(?:>+[ \t]*)?(?:[-+*]|\d{1,2}[.)])[ \t]+|>+[ \t]?)",
                    value,
                )
            )
            if count == 1 and structural_prefix:
                token_offset = text.index(token)
                line_start = text.rfind("\n", 0, token_offset) + 1
                if text[line_start:token_offset].strip():
                    # A model may retain a protected list marker but move it
                    # after the translated subject. Put that exact marker back
                    # at the start of the same line.
                    text = text[:token_offset] + text[token_offset + len(token):]
                    text = text[:line_start] + token + text[line_start:]
            if (
                count == 0
                and structural_prefix
                and protected_source is not None
                and re.match(rf"^\s*{re.escape(token)}", protected_source)
            ):
                # Models occasionally omit a leading one-line list or quote
                # marker even when it is protected. Reinsert only that exact
                # source prefix; literals elsewhere still fail closed.
                leading_newlines = len(text) - len(text.lstrip("\n"))
                text = text[:leading_newlines] + token + text[leading_newlines:]
                count = 1
            repeatable = bool(re.fullmatch(r"--?[A-Za-z0-9][A-Za-z0-9_.-]*(?:=[^\s,;]+)?", value))
            if count < 1 or (count > 1 and not repeatable):
                raise ValueError(f"placeholder {token} occurred {count} times")
            text = text.replace(token, value)
        if "__PGSQL_P" in text:
            raise ValueError("translation contains an unknown placeholder")
        return text


def restore_missing_named_placeholder(
    protected_source: str,
    translated: str,
    protector: Protector,
) -> str:
    """Reinsert a dropped placeholder from "`X` command/setting" phrases."""

    if TARGET_LANGUAGE != "ja":
        return translated
    noun_map = {
        "command": "コマンド",
        "setting": "設定",
        "parameter": "パラメータ",
        "option": "オプション",
        "function": "関数",
    }
    def is_technical_literal(value: str) -> bool:
        return bool(
            re.fullmatch(
                r"(?:`+[^`\n]*`+|[\"'][A-Za-z0-9_.-]+[\"']|"
                r"--?[A-Za-z0-9][A-Za-z0-9_.-]*|[A-Za-z_][A-Za-z0-9_]*\(\))",
                value,
            )
        )

    for index, value in enumerate(protector.values):
        token = f"__PGSQL_P{alpha_index(index)}__"
        if token in translated or not is_technical_literal(value):
            continue
        match = re.search(
            rf"{re.escape(token)}\s+"
            r"(?P<noun>command|setting|parameter|option|function)s?\b",
            protected_source,
            flags=re.IGNORECASE,
        )
        if not match:
            direct_object = re.search(
                rf"(?:Add|Allow|Change|Clarify|Correct|Disable|Enable|Expose|Fix|"
                rf"Handle|Improve|Increase|Log|Remove|Return|Set|Stop|Update|Use)\s+"
                rf"{re.escape(token)}",
                protected_source,
                flags=re.IGNORECASE,
            )
            if direct_object:
                structural_token = next(
                    (
                        f"__PGSQL_P{alpha_index(prefix_index)}__"
                        for prefix_index, prefix_value in enumerate(protector.values)
                        if re.fullmatch(
                            r"[ \t]*(?:[-+*]|\d{1,2}[.)])[ \t]+",
                            prefix_value,
                        )
                        and f"__PGSQL_P{alpha_index(prefix_index)}__" in translated
                    ),
                    None,
                )
                if structural_token:
                    translated = translated.replace(
                        structural_token,
                        f"{structural_token}{token}",
                        1,
                    )
            continue
        target_noun = noun_map[match.group("noun").lower()]
        if target_noun in translated:
            translated = translated.replace(target_noun, f"{token} {target_noun}", 1)
    remaining_inline = [
        f"__PGSQL_P{alpha_index(index)}__"
        for index, value in enumerate(protector.values)
        if is_technical_literal(value)
        and f"__PGSQL_P{alpha_index(index)}__" not in translated
    ]
    if len(remaining_inline) == 1:
        structural_token = next(
            (
                f"__PGSQL_P{alpha_index(index)}__"
                for index, value in enumerate(protector.values)
                if re.fullmatch(r"[ \t]*(?:[-+*]|\d{1,2}[.)])[ \t]+", value)
                and f"__PGSQL_P{alpha_index(index)}__" in translated
            ),
            None,
        )
        if structural_token and re.search(
            rf"{re.escape(structural_token)}[ \t]*(?:が|を|は|の|に|で)",
            translated,
        ):
            translated = translated.replace(
                structural_token,
                structural_token + remaining_inline[0],
                1,
            )
    return translated


def glossary_entries(component: str) -> list[tuple[str, str]]:
    guide = STYLE_GUIDE.read_text(encoding="utf-8")
    display_name = "HAProxy" if component == "haproxy" else component
    headings = {
        "zh": f"## {display_name} 术语表",
        "fr": f"## Glossaire {display_name}",
        "ja": f"## {display_name} 用語集",
    }
    heading = headings[TARGET_LANGUAGE]
    try:
        section = guide.split(heading, 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise RuntimeError(f"missing glossary section {heading!r}") from exc
    entries: list[tuple[str, str]] = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| ---")
            or "英文" in line
            or "Anglais" in line
            or "英語" in line
        ):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2:
            entries.append((cells[0], cells[1]))
    return entries


def parse_glossary(component: str, source: str) -> str:
    entries = glossary_entries(component)
    source_lower = source.lower()
    selected: list[str] = []
    for english_term, target_term in entries:
        candidates = [
            re.sub(r"\s*\([^)]*\)\s*", "", candidate).strip()
            for candidate in english_term.lower().split("/")
        ]
        matched = False
        for candidate in candidates:
            if not candidate:
                continue
            forms = {candidate, candidate + "s", candidate + "es", candidate + "ed", candidate + "ing"}
            if candidate.endswith("y"):
                forms.add(candidate[:-1] + "ies")
            if any(
                re.search(rf"(?<![a-z0-9]){re.escape(form)}(?![a-z0-9])", source_lower)
                for form in forms
            ):
                matched = True
                break
        if matched:
            selected.append(f"{english_term} => {target_term}")
    return ("；" if TARGET_LANGUAGE in {"zh", "ja"} else "; ").join(selected)


def exact_glossary_translation(component: str, source: str) -> str | None:
    direct = EXACT_SCALAR_TRANSLATIONS.get(TARGET_LANGUAGE, {}).get(source.strip())
    if direct is not None:
        return direct
    normalized = source.strip().casefold()
    for english_term, target_term in glossary_entries(component):
        candidates = [candidate.strip().casefold() for candidate in english_term.split("/")]
        if normalized in candidates:
            return target_term
    return None


def system_prompt(component: str, source: str, mode: str) -> str:
    if TARGET_LANGUAGE == "fr":
        if mode == "scalar":
            return f"""Tu es un rédacteur technique francophone expérimenté. Traduis cette courte métadonnée de page {component} en français de France précis, naturel, professionnel et concis.
N'émets que la traduction de l'expression, sans clé YAML, guillemets, préambule ni explication. Conserve à l'identique les numéros de section, noms de produits, commandes, mots-clés de configuration, noms d'API, sigles, versions et espaces réservés.
Terminologie pertinente : {parse_glossary(component, source)}"""
        return f"""Tu es un rédacteur technique francophone expérimenté chargé de traduire le manuel officiel de {component}.

Exigences :
1. Traduis l'intégralité du langage naturel en français de France précis, idiomatique, fluide, professionnel et concis. N'omets aucune phrase, ne résume pas, n'explique pas et n'ajoute aucune information.
2. Conserve strictement la structure Markdown, les sauts de ligne structurels, les niveaux de liste, le nombre de colonnes des tableaux et les marques d'emphase. Chaque espace réservé protégé doit apparaître à l'identique et exactement une fois.
3. Conserve à l'identique les commandes, mots-clés de configuration, noms d'API/RPC/messages/champs, variables d'environnement, noms de fichiers, chemins, métriques, protocoles, noms de produits, sigles et versions.
4. Traduis aussi le langage naturel des titres, tout en conservant les numéros de section.
5. Rends must par une obligation explicite, should par une recommandation, et may/can par une possibilité. Ne modifie jamais les négations, conditions, valeurs par défaut, états d'obsolescence, nombres, unités ni avertissements de sécurité.
6. Emploie la terminologie technique française consacrée, une typographie française soignée et un ton direct adapté aux administrateurs Linux, réseau, bases de données et systèmes distribués.
7. Ne laisse aucun texte explicatif en anglais, même s'il ne contient qu'un mot ou un libellé comme « Install », « where », « Note » ou « Warning ». Seuls les littéraux techniques protégés restent en anglais.
8. N'émets que le fragment traduit, sans guillemets, bloc de code, préambule ni commentaire.

Terminologie obligatoire : {parse_glossary(component, source)}"""
    if TARGET_LANGUAGE == "ja":
        if mode == "scalar":
            return f"""あなたは経験豊富な日本語の技術文書編集者です。次の {component} ページの短いメタデータを、正確で自然、簡潔な日本語に翻訳してください。
訳文だけを出力し、YAML キー、引用符、前置き、説明は出力しないでください。章番号、製品名、コマンド、設定キーワード、API 名、略語、バージョン、プレースホルダーは原文のまま保持してください。
関連用語：{parse_glossary(component, source)}"""
        return f"""あなたは {component} 公式マニュアルを担当する経験豊富な日本語の技術文書編集者です。

要件：
1. 自然言語をすべて、正確で自然、簡潔な日本語に翻訳してください。文を省略、要約、説明したり、原文にない情報を追加したりしないでください。
2. Markdown 構造、構造上の改行、リスト階層、表の列数、強調記号を厳密に保持してください。保護された各プレースホルダーは、同一の形でちょうど 1 回だけ出現させてください。
3. コマンド、設定キーワード、API/RPC/メッセージ/フィールド名、環境変数、ファイル名、パス、メトリクス、プロトコル、製品名、略語、バージョンは原文のまま保持してください。
4. 見出しの自然言語も翻訳し、章番号は保持してください。
5. must は明確な義務、should は推奨、may/can は可能性として訳してください。否定、条件、デフォルト値、非推奨状態、数値、単位、安全上の警告を変更しないでください。
6. Linux、ネットワーク、データベース、分散システムの運用担当者に適した定着した技術用語と直接的な文体を使ってください。操作手順は自然な述語文にし、技術リテラルの前後に必要な助詞を補って、英語語順のまま置かないでください。日本語と製品名・コマンドの間に不要な空白を追加しないでください。
7. `Install`、`where`、`Note`、`Warning` のような 1 語だけの指示やラベルも含め、説明用の英語を残さないでください。保護された技術リテラルだけを英語のまま保持してください。
8. 翻訳した断片だけを出力し、引用符、コードフェンス、前置き、注釈は付けないでください。

必須用語：{parse_glossary(component, source)}"""
    if mode == "scalar":
        return f"""你是资深中文技术文档编辑。把下面的 {component} 页面元数据短语翻译成准确、地道、专业、干练的简体中文。
只输出短语译文，不输出 YAML 键、引号、前言或说明。章节编号、产品名、命令、配置关键字、API 名、缩写、版本和占位符保持原样。
固定表达：This document/guide/section=本文/本指南/本节，禁止“本文件”；administration skills=系统管理能力；troubleshoot X=排查 X 故障，禁止“故障排查 X”。
相关术语：{parse_glossary(component, source)}"""
    return f"""你是资深中文技术文档编辑，正在翻译 {component} 官方手册。

要求：
1. 将片段中的全部自然语言完整翻译为准确、地道、流畅、专业、干练的简体中文，不遗漏句子，不总结，不解释，不添加原文没有的信息。
2. 严格保留 Markdown 结构、换行层级、列表层级、表格列数、强调符号；若片段包含保护占位符，每个占位符必须原样出现且恰好一次。
3. 命令、配置关键字、API/RPC/消息/字段名、环境变量、文件名、路径、指标名、协议名、产品名和缩写保持原样。
4. 标题中的自然语言也必须翻译；章节编号保持原样。
5. must=必须或务必，should=应或建议，may/can=可以；不得改变否定、条件、默认值、弃用状态、数值和安全警告。
6. 中文与英文缩写、数字、占位符之间留一个半角空格。使用“请注意”而非“请注意到”，使用无主句，避免“您”和逐词硬译。
7. 只输出翻译后的片段，不要加引号、代码围栏、前言或说明。
8. 固定表达：This document/guide/section=本文/本指南/本节，禁止“本文件”；administration skills=系统管理能力；troubleshoot X=排查 X 故障或对 X 进行故障排查，禁止“故障排查 X”。

强制术语：{parse_glossary(component, source)}"""


def post_ollama(model: str, prompt: str, *, timeout: int = 600) -> str:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": model == "qwen3:30b-a3b",
            "keep_alive": "30m",
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "repeat_penalty": 1.0,
                "num_ctx": 32768,
                "num_predict": 8192,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    translated = result.get("response")
    if not isinstance(translated, str) or not translated.strip():
        raise RuntimeError(f"Ollama returned no translation: {result}")
    return translated


def normalize_model_output(source: str, translated: str) -> str:
    # Some Qwen3 Ollama templates still emit hidden reasoning when the generate
    # endpoint is called with think=false. Only text after the final marker is
    # the requested answer.
    if "</think>" in translated:
        translated = translated.rsplit("</think>", 1)[1]
    translated = translated.strip()
    if translated.startswith("```markdown") and translated.endswith("```"):
        translated = translated[len("```markdown") : -3].strip("\n")
    elif translated.startswith("```") and translated.endswith("```"):
        translated = translated[3:-3].strip("\n")
    leading = len(source) - len(source.lstrip("\n"))
    trailing = len(source) - len(source.rstrip("\n"))
    return "\n" * leading + translated + "\n" * trailing


def repair_continuation_indentation(source: str, translated: str) -> str:
    """Indent model-created continuation lines when the source is a list item."""

    source_lines = [line for line in source.splitlines() if line.strip()]
    target_lines = translated.splitlines(keepends=True)
    if not source_lines or len(target_lines) < 2:
        return translated

    definition = next(
        (
            match
            for line in source_lines
            if (match := re.match(r"^(?P<indent>[ \t]*):[ \t]+", line))
        ),
        None,
    )
    list_item = re.match(
        r"^(?P<indent>[ \t]*)(?:[-+*]|\d{1,2}[.)])[ \t]+",
        source_lines[0],
    )
    if definition:
        marker_index = next(
            (index for index, line in enumerate(target_lines) if re.match(r"^[ \t]*:[ \t]+", line)),
            None,
        )
        continuation_indent = len(definition.group("indent").expandtabs(4)) + 4
    elif list_item:
        marker_index = next(
            (
                index
                for index, line in enumerate(target_lines)
                if re.match(r"^[ \t]*(?:[-+*]|\d{1,2}[.)])[ \t]+", line)
            ),
            None,
        )
        continuation_indent = len(list_item.group("indent").expandtabs(4)) + 4
    else:
        return translated
    if marker_index is None:
        return translated

    for index in range(marker_index + 1, len(target_lines)):
        line = target_lines[index]
        if (
            not line.strip()
            or line.startswith((" ", "\t", ">"))
            or re.match(r"^[ \t]*(?:[-+*]|\d{1,2}[.)]|:)[ \t]+", line)
        ):
            continue
        target_lines[index] = " " * continuation_indent + line
    return "".join(target_lines)


def remove_added_code_for_plain_identifiers(source: str, translated: str) -> str:
    """Undo code styling added around identifiers that were plain in English."""

    if TARGET_LANGUAGE == "fr" and "advertised initial_max_streams_bidi" in source:
        translated = re.sub(
            r"`?advertised_initial_max_streams_bidi`?",
            "initial_max_streams_bidi annoncé",
            translated,
        )
    source_without_code = re.sub(r"`+[^`]*`+", "", source)
    identifiers = set(
        re.findall(r"(?<!\w)[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?!\w)", source_without_code)
    )
    identifiers.update(
        re.findall(
            r"(?<!\w)[A-Za-z_][A-Za-z0-9_.-]*=[A-Za-z0-9_./:${}-]*(?!\w)",
            source_without_code,
        )
    )
    identifiers.update(
        re.findall(
            r"(?<!\w)[A-Za-z_][A-Za-z0-9_.-]*[ \t]+=[ \t]+"
            r"[A-Za-z0-9_./:${}-]+(?!\w)",
            source_without_code,
        )
    )
    identifiers.update(
        re.findall(r"(?<![\w-])--?[A-Za-z0-9][A-Za-z0-9_.-]*(?!\w)", source_without_code)
    )
    identifiers.update(
        re.findall(r"(?<!\w)[A-Za-z_][A-Za-z0-9_.]*\(\)(?!\w)", source_without_code)
    )
    identifiers.update(
        re.findall(r"(?<!\w)struct[ \t]+[A-Za-z_][A-Za-z0-9_]*(?!\w)", source_without_code)
    )
    for literal in re.findall(r"`+[^`]*`+", translated):
        inner = literal.strip("`")
        if (
            re.fullmatch(r"[a-z][a-z0-9_.-]*", inner)
            and re.search(rf"(?<!\w){re.escape(inner)}(?!\w)", source_without_code)
        ):
            identifiers.add(inner)
        if (
            re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*(?:[ \t]+[A-Za-z0-9_.-]+)+", inner)
            and re.search(rf"(?<!\w){re.escape(inner)}(?!\w)", source_without_code)
        ):
            identifiers.add(inner)
    for identifier in identifiers:
        source_count = len(re.findall(rf"`+{re.escape(identifier)}`+", source))
        target_count = len(re.findall(rf"`+{re.escape(identifier)}`+", translated))
        extra = max(0, target_count - source_count)
        if not extra:
            continue

        def unwrap(match: re.Match[str]) -> str:
            nonlocal extra
            if extra:
                extra -= 1
                return identifier
            return match.group(0)

        translated = re.sub(rf"`+{re.escape(identifier)}`+", unwrap, translated)
    for literal in re.findall(r"`([^`\n]+)`", translated):
        closed = f"`{literal}`"
        if closed not in source and f"`{literal}" in source:
            # Preserve a malformed but intentional upstream literal instead of
            # letting the model silently add a missing closing backtick.
            translated = translated.replace(closed, f"`{literal}", 1)
    return translated


def repair_french_numeric_expansions(source: str, translated: str) -> str:
    """Remove a target-side numeric expansion that is only implicit upstream."""

    if TARGET_LANGUAGE != "fr":
        return translated
    if "wrap at the end" in source:
        translated = re.sub(
            r"\bqui (?:reviennent|retournent) à zéro à la fin\b",
            "qui bouclent en fin de plage",
            translated,
            flags=re.IGNORECASE,
        )
    return translated


def normalize_inline_code_wrappers(source: str, translated: str) -> str:
    """Collapse extra backtick layers around literals protected from source."""

    for literal in re.findall(r"`+[^`]*`+", source):
        inner = literal.strip("`")
        translated = re.sub(
            rf"`+{re.escape(inner)}`+",
            lambda _match, replacement=literal: replacement,
            translated,
        )
    return translated


def repair_dangling_japanese_list_particle(translated: str) -> str:
    if TARGET_LANGUAGE != "ja":
        return translated
    translated = re.sub(
        r"(?m)^(?P<prefix>[ \t]*[-+*][ \t]+)(?:の|と|を|が|は)[ \t]*"
        r"(?=\S)",
        r"\g<prefix>",
        translated,
    )
    translated = re.sub(
        r"(?m)^(?P<prefix>[ \t]*[-+*][ \t]+)の機能\b",
        r"\g<prefix>機能",
        translated,
    )
    return translated


def restore_named_technical_literal(source: str, translated: str) -> str:
    """Restore a dropped literal in phrases such as "the `RELOAD` command"."""

    if TARGET_LANGUAGE != "ja":
        return translated
    noun_map = {
        "command": "コマンド",
        "setting": "設定",
        "parameter": "パラメータ",
        "option": "オプション",
        "function": "関数",
    }
    target_codes = Counter(re.findall(r"`+[^`\n]*`+", translated))
    for match in re.finditer(
        r"(?P<literal>`+[^`\n]*`+)\s+"
        r"(?P<noun>command|setting|parameter|option|function)s?\b",
        source,
        flags=re.IGNORECASE,
    ):
        literal = match.group("literal")
        if target_codes[literal]:
            target_codes[literal] -= 1
            continue
        target_noun = noun_map[match.group("noun").lower()]
        if target_noun not in translated:
            continue
        translated = translated.replace(target_noun, f"{literal} {target_noun}", 1)
    return translated


def normalize_chinese_spacing(value: str) -> str:
    """Apply target-language typography normalization outside fenced blocks."""
    if TARGET_LANGUAGE != "zh":
        return re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"([\u3400-\u9fff])([A-Za-z0-9])", r"\1 \2", value)
    value = re.sub(r"([A-Za-z0-9])([\u3400-\u9fff])", r"\1 \2", value)
    value = re.sub(r"(?<=[\u3400-\u9fff]),\s*(?=[\u3400-\u9fff])", "、", value)
    value = re.sub(r"(?<=[\u3400-\u9fff]):\s*(?=[\u3400-\u9fff])", "：", value)
    value = re.sub(r"([，。；：、！？（【])\s+(?=[A-Za-z0-9`])", r"\1", value)
    value = re.sub(r"(?<=[A-Za-z0-9`])\s+([，。；：、！？）】])", r"\1", value)
    value = re.sub(r"\[\s*段\s*(\d+(?:\.\d+)*)\s*\]", r"[第 \1 节]", value)
    value = re.sub(r"\[\s*第\s*(\d+(?:\.\d+)*)\s*(?:段|节)\s*\]", r"[第 \1 节]", value)
    value = re.sub(r"\[\s*(\d+(?:\.\d+)*)\s*(?:段|节)\s*\]", r"[第 \1 节]", value)
    value = re.sub(r"[ \t]+\n", "\n", value)
    return value


def normalize_brand_spelling(value: str) -> str:
    brands = {
        r"\bpatroni\b": "Patroni",
        r"\bpgbackrest\b": "pgBackRest",
        r"\bpgbadger\b": "pgBadger",
        r"\bhaproxy\b": "HAProxy",
        r"\bnginx\b": "NGINX",
        r"\betcd\b": "etcd",
        r"\bopenssl\b": "OpenSSL",
        r"\bpostgresql\b": "PostgreSQL",
    }
    parts = re.split(r'("[^"\n]*"|\'[^\'\n]*\')', value)
    for index in range(0, len(parts), 2):
        for pattern, spelling in brands.items():
            parts[index] = re.sub(pattern, spelling, parts[index], flags=re.IGNORECASE)
    return "".join(parts)


def cache_key(model: str, component: str, mode: str, prompt: str, source: str) -> str:
    style_digest = hashlib.sha256(STYLE_GUIDE.read_bytes()).hexdigest()
    payload = "\0".join(
        (
            CACHE_SCHEMA_VERSION,
            TARGET_LANGUAGE,
            model,
            component,
            mode,
            style_digest,
            prompt,
            source,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def translate_text(
    source: str,
    *,
    component: str,
    model: str,
    cache: Cache,
    mode: str = "markdown",
    retries: int = 4,
) -> str:
    core = source.strip("\n")
    manual = MANUAL_TRANSLATIONS.get(core)
    if manual is not None:
        leading = len(source) - len(source.lstrip("\n"))
        trailing = len(source) - len(source.rstrip("\n"))
        return "\n" * leading + manual + "\n" * trailing
    if not ASCII_WORD_RE.search(source):
        return source
    protector = Protector()
    protected = protector.protect(source)
    instruction = system_prompt(component, source, mode)
    placeholders = re.findall(r"__PGSQL_P[A-Z]+__", protected)
    if placeholders:
        if TARGET_LANGUAGE == "zh":
            instruction += "\n本片段中的占位符必须逐字各保留一次：" + "、".join(placeholders)
        elif TARGET_LANGUAGE == "fr":
            instruction += (
                "\nChaque espace réservé suivant doit être conservé tel quel "
                "et apparaître exactement une fois : " + ", ".join(placeholders)
            )
        else:
            instruction += (
                "\n次の各プレースホルダーを同一の形でちょうど 1 回ずつ保持してください："
                + "、".join(placeholders)
            )
    else:
        instruction += {
            "zh": "\n本片段没有占位符，禁止添加任何占位符。",
            "fr": "\nCe fragment ne contient aucun espace réservé ; n'en ajoute aucun.",
            "ja": "\nこの断片にはプレースホルダーがありません。追加しないでください。",
        }[TARGET_LANGUAGE]
    fragment_label = {
        "zh": "待翻译片段",
        "fr": "Fragment à traduire",
        "ja": "翻訳対象の断片",
    }[TARGET_LANGUAGE]
    prompt = f"{instruction}\n\n{fragment_label}：\n{protected}"
    key = cache_key(model, component, mode, prompt, source)
    errors: list[str] = []
    cached_validation_error: str | None = None
    cached = cache.get(key)
    if cached is not None:
        cached = normalize_chinese_spacing(cached)
        cached = normalize_inline_code_wrappers(source, cached)
        cached = remove_added_code_for_plain_identifiers(source, cached)
        cached = repair_french_numeric_expansions(source, cached)
        cached = repair_dangling_japanese_list_particle(cached)
        cached = restore_named_technical_literal(source, cached)
        cached = repair_continuation_indentation(source, cached)
        try:
            validate_fragment_structure(source, cached)
            validate_target_language(cached)
            return cached
        except ValueError as exc:
            errors.append(f"cached translation: {exc}")
            cached_validation_error = str(exc)

    attempt_limit = 1 if os.environ.get("TRANSLATION_DEBUG") else retries
    attempt_prompt = prompt
    if cached_validation_error:
        if TARGET_LANGUAGE == "zh":
            attempt_prompt += (
                "\n\n现有译文未通过结构校验："
                + cached_validation_error
                + "。每个列表项必须单独成行，并严格保留原有缩进；不得合并、拆分或展平列表。"
            )
        elif TARGET_LANGUAGE == "fr":
            attempt_prompt += (
                "\n\nLa traduction en cache a échoué au contrôle structurel : "
                + cached_validation_error
                + ". Chaque élément de liste doit rester sur sa propre ligne avec "
                "son retrait exact ; ne fusionne, ne scinde et n'aplatis aucune liste."
            )
        else:
            attempt_prompt += (
                "\n\nキャッシュ済みの訳文が構造検証に失敗しました："
                + cached_validation_error
                + "。各リスト項目を個別の行に置き、元のインデントを厳密に保持してください。"
                "リストを結合、分割、平坦化しないでください。"
            )
    for attempt in range(1, attempt_limit + 1):
        raw = ""
        try:
            raw = post_ollama(model, attempt_prompt)
            normalized = normalize_model_output(protected, raw)
            normalized = normalize_brand_spelling(normalized)
            normalized = restore_missing_named_placeholder(protected, normalized, protector)
            restored = protector.restore(normalized, protected_source=protected)
            restored = normalize_inline_code_wrappers(source, restored)
            restored = remove_added_code_for_plain_identifiers(source, restored)
            restored = repair_french_numeric_expansions(source, restored)
            restored = repair_dangling_japanese_list_particle(restored)
            restored = restore_named_technical_literal(source, restored)
            restored = repair_continuation_indentation(source, restored)
            added_heading = re.match(
                r"^(\s*)(\d+(?:\.\d+)+)\.\s+[^\n]{1,100}\n\s*\n",
                restored,
            )
            source_number_set = set(NUMBER_TOKEN_RE.findall(source))
            if added_heading and added_heading.group(2) not in source_number_set:
                restored = restored[added_heading.end() :]
            added_prefix = re.match(r"^(\s*)(\d+(?:\.\d+)+)\.?\s+", restored)
            if added_prefix and added_prefix.group(2) not in source_number_set:
                restored = added_prefix.group(1) + restored[added_prefix.end() :]
            if not NUMBER_TOKEN_RE.search(source):
                restored = re.sub(
                    r"^(\s*)\d+(?:\.\d+)+\.\s+",
                    r"\1",
                    restored,
                    count=1,
                )
                if not re.match(r"^\s*\d+[.)]\s+", source):
                    restored = re.sub(r"^(\s*)\d+[.)]\s+", r"\1", restored, count=1)
            if not re.search(r"(?m)^\s*[-+*]\s+", source) and re.search(
                r"(?m)^\s*[-+*]\s+", restored
            ):
                restored = re.sub(r"\n\s*[-+*]\s+", " - ", restored)
            source_lines_all = source.splitlines()
            target_lines_all = restored.splitlines()
            if (
                len(source_lines_all) == len(target_lines_all)
                and source_lines_all
                and all(not line.strip() or line.lstrip().startswith("|") for line in source_lines_all)
            ):
                repaired_lines: list[str] = []
                for source_line, target_line in zip(source_lines_all, target_lines_all, strict=True):
                    if source_line.lstrip().startswith("|") and not target_line.lstrip().startswith("|"):
                        indent = re.match(r"^\s*", target_line).group(0)  # type: ignore[union-attr]
                        target_line = indent + "| " + target_line.lstrip()
                    if source_line.rstrip().endswith("|") and not target_line.rstrip().endswith("|"):
                        target_line = target_line.rstrip() + " |"
                    repaired_lines.append(target_line)
                restored = "\n".join(repaired_lines) + ("\n" if restored.endswith("\n") else "")
            source_nonblank = [line for line in source.splitlines() if line.strip()]
            if source_nonblank and all(line.lstrip().startswith(">") for line in source_nonblank):
                quote_indent = re.match(r"^\s*", source_nonblank[0]).group(0)  # type: ignore[union-attr]
                restored = "\n".join(
                    quote_indent + line.lstrip() if line.strip() else line
                    for line in restored.splitlines()
                ) + ("\n" if restored.endswith("\n") else "")
            validate_fragment_structure(source, restored)
            validate_target_language(restored)
            if mode == "scalar":
                restored = restored.strip().strip('"').strip("'")
                if "\n" in restored:
                    raise ValueError("scalar translation contains a newline")
            restored = normalize_chinese_spacing(restored)
            cache.put(key, restored)
            return restored
        except (RuntimeError, ValueError) as exc:
            if os.environ.get("TRANSLATION_DEBUG"):
                print(f"debug attempt {attempt} raw output: {raw!r}", file=sys.stderr)
                print(f"debug source fragment: {source!r}", file=sys.stderr)
                if "restored" in locals():
                    print(f"debug restored fragment: {restored!r}", file=sys.stderr)
            errors.append(f"attempt {attempt}: {exc}")
            source_numbers = NUMBER_TOKEN_RE.findall(source)
            placeholder_map = list(zip(placeholders, protector.values))
            placeholder_count_note = ""
            if len(placeholders) != len(protector.values):
                placeholder_count_note = {
                    "zh": (
                        f" 保护占位符计数不一致：片段中 {len(placeholders)} 个，"
                        f"原始字面量 {len(protector.values)} 个。"
                    ),
                    "fr": (
                        f" Nombre incohérent : {len(placeholders)} espaces réservés "
                        f"pour {len(protector.values)} littéraux protégés."
                    ),
                    "ja": (
                        f" プレースホルダー数が一致しません：{len(placeholders)} 個に対し、"
                        f"保護対象リテラルは {len(protector.values)} 個です。"
                    ),
                }[TARGET_LANGUAGE]
            if TARGET_LANGUAGE == "zh":
                attempt_prompt = (
                    prompt
                    + "\n\n上一次译文未通过校验："
                    + str(exc)
                    + "。请重新翻译，禁止增删或重复任何信息。"
                    + "原文中的数字、版本和单位依次为："
                    + repr(source_numbers)
                    + "。本段实际占位符依次为："
                    + repr(placeholders)
                    + "，对应的原始字面量为："
                    + repr(placeholder_map)
                    + placeholder_count_note
                    + "。原始字面量仅用于理解位置；输出仍须使用对应占位符，且必须逐项一致。"
                )
            elif TARGET_LANGUAGE == "fr":
                attempt_prompt = (
                    prompt
                    + "\n\nLa traduction précédente a échoué au contrôle : "
                    + str(exc)
                    + ". Retraduis sans ajouter, supprimer ni répéter d'information. "
                    + "Nombres, versions et unités de la source : "
                    + repr(source_numbers)
                    + ". Espaces réservés attendus : "
                    + repr(placeholders)
                    + ". Correspondance avec les littéraux protégés : "
                    + repr(placeholder_map)
                    + placeholder_count_note
                    + ". Les littéraux servent uniquement à comprendre le contexte ; "
                    "la sortie doit toujours employer chaque espace réservé correspondant."
                )
            else:
                attempt_prompt = (
                    prompt
                    + "\n\n前回の訳文は検証に失敗しました："
                    + str(exc)
                    + "。情報を追加、省略、重複させずに再翻訳してください。"
                    + "原文の数値、バージョン、単位："
                    + repr(source_numbers)
                    + "。必要なプレースホルダー："
                    + repr(placeholders)
                    + "。保護対象リテラルとの対応："
                    + repr(placeholder_map)
                    + placeholder_count_note
                    + "。リテラルは文脈理解のためだけに示しています。出力では対応する"
                    "プレースホルダーを必ず使用してください。"
                )
            time.sleep(min(attempt, 3))
    raise RuntimeError("; ".join(errors))


def validate_fragment_structure(source: str, translated: str) -> None:
    """Reject common model rewrites that would damage Markdown semantics."""

    inline_code_re = re.compile(r"`+[^`]*`+")
    source_inline_code = inline_code_re.findall(source)
    target_inline_code = inline_code_re.findall(translated)
    if Counter(source_inline_code) != Counter(target_inline_code):
        raise ValueError(
            "inline code literals changed "
            f"source={source_inline_code!r} translated={target_inline_code!r}"
        )

    footnote_definition_re = re.compile(r"(?m)^[ \t]*\[\^[^\]\n]+\]:[ \t]+")
    if footnote_definition_re.findall(source) != footnote_definition_re.findall(translated):
        raise ValueError("footnote definition prefixes changed")

    def table_signature(value: str) -> list[int]:
        return [
            len(re.findall(r"(?<!\\)\|", line))
            for line in value.splitlines()
            if line.lstrip().startswith("|")
        ]

    source_table = table_signature(source)
    target_table = table_signature(translated)
    if source_table != target_table:
        raise ValueError(f"Markdown table shape changed source={source_table} translated={target_table}")

    def marker_count(value: str, pattern: str) -> int:
        lines = [line for line in value.splitlines() if line.strip()]
        return sum(bool(re.match(pattern, line)) for line in lines)

    def list_signature(value: str) -> list[tuple[int, str]]:
        signature: list[tuple[int, str]] = []
        active_ordered_indents: set[int] = set()
        for line in value.splitlines():
            match = re.match(r"^(\s*)([-+*]|\d{1,2}[.)])\s+", line)
            if not match:
                if line.strip() and not line.startswith((" ", "\t", ">")):
                    active_ordered_indents.clear()
                continue
            indent = len(match.group(1).expandtabs(4))
            if indent <= 1:
                indent = 0
            marker = match.group(2)
            if marker in "-+*":
                signature.append((indent, "unordered"))
            elif int(marker[:-1]) == 1 or indent in active_ordered_indents:
                signature.append((indent, marker))
                active_ordered_indents.add(indent)
        return signature

    structures = {
        "unordered list": r"^\s*[-+*]\s+",
        "blockquote": r"^\s*>\s?",
    }
    for label, pattern in structures.items():
        if label == "blockquote":
            source_lines = [line for line in source.splitlines() if line.strip()]
            target_lines = [line for line in translated.splitlines() if line.strip()]
            source_is_quote = bool(source_lines) and all(re.match(pattern, line) for line in source_lines)
            target_is_quote = bool(target_lines) and all(re.match(pattern, line) for line in target_lines)
            if source_is_quote != target_is_quote:
                raise ValueError("blockquote structure changed")
            continue
        if marker_count(source, pattern) != marker_count(translated, pattern):
            raise ValueError(f"{label} marker count changed")
    if list_signature(source) != list_signature(translated):
        raise ValueError("Markdown list marker sequence or nesting changed")

    def definition_signature(value: str) -> list[int]:
        return [
            len(match.group(1).expandtabs(4))
            for line in value.splitlines()
            if (match := re.match(r"^([ \t]*):[ \t]+", line))
        ]

    if definition_signature(source) != definition_signature(translated):
        raise ValueError("Markdown definition-list indentation changed")

    def number_tokens(value: str) -> list[str]:
        if TARGET_LANGUAGE == "fr":
            # French articles such as "un" and "une" are indistinguishable
            # from the number one without sentence-level context. Validate all
            # explicit numeric literals strictly and canonicalize only written
            # unit names; do not invent numeric tokens from ordinary prose.
            unit_aliases = {
                "nanoseconds": "ns", "nanosecond": "ns",
                "microseconds": "us", "microsecond": "us",
                "milliseconds": "ms", "millisecond": "ms",
                "seconds": "s", "second": "s",
                "minutes": "min", "minute": "min",
                "hours": "h", "hour": "h",
                "days": "d", "day": "d",
                "ns": "ns", "us": "us", "ms": "ms", "s": "s",
                "min": "min", "h": "h", "d": "d",
                "bytes": "B", "byte": "B",
                "kilobytes": "kB", "kilobyte": "kB", "kb": "kB", "k": "kB",
                "megabytes": "MB", "megabyte": "MB",
                "gigabytes": "GB", "gigabyte": "GB",
                "terabytes": "TB", "terabyte": "TB",
                "mb": "MB", "gb": "GB", "g": "GB", "tb": "TB",
                "nanosecondes": "ns", "nanoseconde": "ns",
                "microsecondes": "us", "microseconde": "us",
                "millisecondes": "ms", "milliseconde": "ms",
                "secondes": "s", "seconde": "s",
                "heures": "h", "heure": "h",
                "jours": "d", "jour": "d",
                "octets": "B", "octet": "B",
                "kilo-octets": "kB", "kilo-octet": "kB", "ko": "kB",
                "mégaoctets": "MB", "mégaoctet": "MB", "mo": "MB",
                "gigaoctets": "GB", "gigaoctet": "GB", "go": "GB",
                "téraoctets": "TB", "téraoctet": "TB",
            }
            value = re.sub(
                r"\b(\d+)k(?=\s+(?:(?:total\s+)?(?:concurrent\s+)?connections?|outgoing address\+port couples)\b)",
                lambda match: str(int(match.group(1)) * 1000),
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(\d+(?:\.\d+)?)\s+(?=[KMGT]?bps\b)",
                r"\1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"(?<!\d)\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?!\d)",
                lambda match: re.sub(r"[ \u00a0\u202f]", "", match.group(0)),
                value,
            )
            value = re.sub(
                r"(?<!\d)\d{1,3}(?:,\d{3})+(?!\d)",
                lambda match: match.group(0).replace(",", ""),
                value,
            )
            value = re.sub(r"\bRFC\s+(\d+)\b", r"RFC\1", value, flags=re.IGNORECASE)
            value = re.sub(r"(?<=\d),(?=\d{1,2}(?!\d))", ".", value)
            value = re.sub(
                r"(?<!\w)(\d+(?:\.\d+)?)\s+(?:à|to|vers|through)\s+(?:(?:la|le)\s+)?(\d+(?:\.\d+)?)(?!\w)",
                r"\1-\2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bentre\s+(\d+(?:\.\d+)?)\s+et\s+(\d+(?:\.\d+)?)(?!\w)",
                r"\1-\2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"(?<=\d)\s+s'", " si'", value, flags=re.IGNORECASE)
            value = re.sub(
                r"(?<=\d)\s+d['’]",
                " de ",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bmoins d['’]une?\b",
                "moins de 1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bdepuis zéro\b",
                "from-scratch",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\bend-2-end\b", "end-to-end", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\b(v?\d+(?:\.\d+)?)-only\b",
                r"\1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bv(\d+(?:\.\d+)?)-on-v(\d+(?:\.\d+)?)\b",
                r"v\1 v\2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\b(?:u?int)(\d+)\b", r"\1", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\ben double\b",
                "duplicate",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bdouble[ -]check\b",
                "verify",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\bdoubler\b", "2x", value, flags=re.IGNORECASE)
            value = re.sub(r"\ba couple of\b", "2", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\bentre deux (tentatives|révisions)\b",
                r"entre les \1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\btriplets?\b", "3-tuple", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\bun (million|milliard)\b",
                r"1 \1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\ba (million|billion)\b",
                r"1 \1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:a|an|one|un|une)\s+(?=(?:(?:nano|micro|milli)?second(?:e)?s?|minutes?|heures?|hours?|jours?|days?|octets?|bytes?)\b)",
                "1 ",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:a single|any single|one|un seul|une seule)\s+(?=(?:nodes?|n[œo]uds?|members?|membres?)\b)",
                "1 ",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\b(\d+)x\b", r"\1", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\b(\d+)\s+extra\s+bytes?\b",
                r"\1 bytes",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(replies|responses?|codes?)\s+([1-5]\d{2})s\b",
                r"\1 \2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(\d+)\s+or more\s+(seconds?|minutes?|hours?|days?)\b",
                r"\1 \2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(\d{1,2})\s*h\s*(\d{2})\b",
                r"\1:\2",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(\d+)\s*(?:m|min)\s*(\d+)\s*s\s*(\d+)\s*ms\b",
                r"\1m\2s\3ms",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\bdeux[ -]points?\b", "colon", value, flags=re.IGNORECASE)
            value = re.sub(
                r"\b(?:de )?(?:taille|longueur)(?:s)? nulle(?:s)?\b",
                "0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bvaleurs? nulles?\b",
                "0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:il|elle) est nul(?:le)?\b",
                "0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bla valeur est nulle\b",
                "0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\badresses?(?: source et destination)? sont nulles?\b",
                "0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bpages? nulles?\b",
                "0 pages",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bpoids nul\b",
                "poids 0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:le )?temps rapporté sera nul\b",
                "temps rapporté 0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:transfert|acheminement) sans copie\b",
                "0-copy",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bnon[- ]?(?:nul(?:le)?s?|null|zero)\b",
                "non-0",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\bMay(?=\s+\d{1,2}\b)", "05", value)
            month_numbers = {
                "january": "01", "janvier": "01",
                "february": "02", "février": "02",
                "march": "03", "mars": "03",
                "april": "04", "avril": "04",
                "mai": "05",
                "june": "06", "juin": "06",
                "july": "07", "juillet": "07",
                "august": "08", "août": "08",
                "september": "09", "septembre": "09",
                "october": "10", "octobre": "10",
                "november": "11", "novembre": "11",
                "december": "12", "décembre": "12",
            }
            value = re.sub(
                r"\b(" + "|".join(map(re.escape, month_numbers)) + r")\b",
                lambda match: month_numbers[match.group(1).lower()],
                value,
                flags=re.IGNORECASE,
            )
            word_numbers = {
                "zero": 0, "zeros": 0, "zeroes": 0, "zeroed": 0,
                "zéro": 0, "zéros": 0,
                "two": 2, "twice": 2, "dual": 2, "double": 2,
                "doubles": 2, "deux": 2,
                "three": 3, "trois": 3,
                "four": 4, "quatre": 4,
                "five": 5, "cinq": 5,
                "six": 6,
                "seven": 7, "sept": 7,
                "eight": 8, "huit": 8,
                "nine": 9, "neuf": 9,
                "ten": 10, "dix": 10,
                "eleven": 11, "onze": 11,
                "twelve": 12, "dozen": 12, "douze": 12, "douzaine": 12,
                "thirteen": 13, "treize": 13,
                "fourteen": 14, "quatorze": 14,
                "fifteen": 15, "quinze": 15,
                "sixteen": 16, "seize": 16,
                "seventeen": 17, "dix-sept": 17,
                "eighteen": 18, "dix-huit": 18,
                "nineteen": 19, "dix-neuf": 19,
                "twenty": 20, "vingt": 20,
                "thirty": 30, "trente": 30,
                "forty": 40, "quarante": 40,
                "fifty": 50, "cinquante": 50,
                "sixty": 60, "soixante": 60,
            }
            value = re.sub(
                r"\b("
                + "|".join(
                    map(re.escape, sorted(word_numbers, key=len, reverse=True))
                )
                + r")\b",
                lambda match: str(word_numbers[match.group(1).lower()]),
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"(?<=\d)\s+d['’]",
                " de ",
                value,
                flags=re.IGNORECASE,
            )
            for localized, canonical in unit_aliases.items():
                value = re.sub(
                    rf"(?<!\w)(\d+(?:\.\d+)?)\s*-?\s*{localized}\b",
                    rf"\1{canonical}",
                    value,
                    flags=re.IGNORECASE,
                )
            value = re.sub(
                r"\b3rd[ -]part(?:y|ies)\b",
                "third-party",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bdouble-escap(?:e|ed|ing)\b",
                "2-escape",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(?:a|one)\s+(\d+)(?:st|nd|rd|th)\s+of\b",
                r"1/\1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"(?<!\w)(\d+)\s*-?\s*bits?\b",
                r"\1",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"(?<!\w)(\d+)(?:st|nd|rd|th|er|re|e|eme|ème)\b",
                r"\1",
                value,
                flags=re.IGNORECASE,
            )
            tokens: list[str] = []
            for token in NUMBER_TOKEN_RE.findall(value):
                token = re.sub(r"[\s\u00a0\u202f]+", "", token)
                if token.endswith("KB"):
                    token = token[:-2] + "kB"
                if re.fullmatch(
                    r"[vV]\d+(?:\.\d+)*(?:[-+][A-Za-z0-9.-]+)?", token
                ):
                    token = token[1:]
                tokens.append(token)
            if os.environ.get("TRANSLATION_DEBUG"):
                print(
                    f"debug normalized French numbers: {value!r} -> {tokens!r}",
                    file=sys.stderr,
                )
            return sorted(tokens)

        if TARGET_LANGUAGE == "ja":
            english_numbers = {
                "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            }
            counted_nouns = (
                r"parameters?|options?|methods?|ways?|reasons?|cases?|steps?|modes?|"
                r"servers?|connections?|files?|hosts?|names?|databases?|queries?|commands?|"
                r"values?|fields?|interfaces?|members?|nodes?|items?|levels?|pages?|projects?|"
                r"collections?|processes?|threads?|"
                r"seconds?|minutes?|hours?|days?|bytes?|bits?|addresses?|times?"
            )
            value = re.sub(
                r"\b(two|three|four|five|six|seven|eight|nine|ten)\s+"
                rf"(?=(?:[A-Za-z-]+\s+){{0,2}}(?:{counted_nouns})\b)",
                lambda match: str(english_numbers[match.group(1).lower()]) + " ",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\b(two|three|four|five|six|seven|eight|nine|ten)\s+or\s+more\s+"
                rf"(?=(?:[A-Za-z-]+\s+){{0,2}}(?:{counted_nouns})\b)",
                lambda match: str(english_numbers[match.group(1).lower()]) + " or more ",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bbetween\s+(one|two|three|four|five|six|seven|eight|nine|ten)\s+"
                r"(?:and|to)\s+(one|two|three|four|five|six|seven|eight|nine|ten)\b",
                lambda match: (
                    f"between {english_numbers[match.group(1).lower()]} and "
                    f"{english_numbers[match.group(2).lower()]}"
                ),
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\bfactor\s+of\s+(one|two|three|four|five|six|seven|eight|nine|ten)\b",
                lambda match: f"factor of {english_numbers[match.group(1).lower()]}",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(r"\bzero\b", "0", value, flags=re.IGNORECASE)
            value = value.replace("ゼロ", "0")
            value = re.sub(r"\bonce\b", "1", value, flags=re.IGNORECASE)
            value = re.sub(r"\btwice\b", "2", value, flags=re.IGNORECASE)
            value = re.sub(r"\bthrice\b", "3", value, flags=re.IGNORECASE)
            value = re.sub(r"\bhex(?:adecimal)?\b", "base 16", value, flags=re.IGNORECASE)
            value = re.sub(r"\boctal\b", "base 8", value, flags=re.IGNORECASE)
            japanese_numbers = {
                "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
                "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
            }
            value = re.sub(
                r"([一二三四五六七八九十])\s*"
                r"(?=つ|個|件|台|本|人|項目|種類|段階|方法|理由|場合|ステップ|モード|"
                r"サーバー|接続|ファイル|ホスト|名前|データベース|クエリ|コマンド|値|"
                r"フィールド|メンバー|ノード|レベル|プロセス|スレッド|パラメーター|"
                r"オプション|アドレス)",
                lambda match: str(japanese_numbers[match.group(1)]),
                value,
            )
            value = re.sub(
                r"([\u3040-\u30ff\u3400-\u9fff])(?=[A-Za-z0-9])",
                r"\1 ",
                value,
            )
            value = re.sub(
                r"(?<=[A-Za-z0-9%])([\u3040-\u30ff\u3400-\u9fff])",
                r" \1",
                value,
            )
            unit_aliases = {
                "nanoseconds": "ns", "nanosecond": "ns",
                "microseconds": "us", "microsecond": "us",
                "milliseconds": "ms", "millisecond": "ms",
                "seconds": "s", "second": "s", "秒": "s",
                "minutes": "min", "minute": "min", "分": "min",
                "hours": "h", "hour": "h", "時間": "h",
                "days": "d", "day": "d", "日": "d",
                "bytes": "B", "byte": "B", "バイト": "B",
            }
            for localized, canonical in unit_aliases.items():
                boundary = "" if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", localized) else r"\b"
                value = re.sub(
                    rf"(?<!\w)(\d+(?:\.\d+)?)\s*-?\s*{localized}{boundary}",
                    rf"\1{canonical}",
                    value,
                    flags=re.IGNORECASE,
                )
            value = re.sub(
                r"(?<=[A-Za-z0-9%])([\u3040-\u30ff\u3400-\u9fff])",
                r" \1",
                value,
            )
            tokens: list[str] = []
            for token in NUMBER_TOKEN_RE.findall(value):
                token = re.sub(r"[\s\u00a0\u202f]+", "", token)
                if token.endswith("KB"):
                    token = token[:-2] + "kB"
                if re.fullmatch(r"[vV]\d+(?:\.\d+)*(?:[-+][A-Za-z0-9.-]+)?", token):
                    token = token[1:]
                tokens.append(token)
            if os.environ.get("TRANSLATION_DEBUG"):
                print(
                    f"debug normalized Japanese numbers: {value!r} -> {tokens!r}",
                    file=sys.stderr,
                )
            return sorted(tokens)

        value = re.sub(r"([\u3400-\u9fff])(?=\d)", r"\1 ", value)
        value = re.sub(r"(?<=\d)([\u3400-\u9fff])", r" \1", value)
        cluster_chinese_numbers = {"单": 1, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
        value = re.sub(
            r"(?<![任每某])([单一二两三四五六七八九十])(?=成员|节点|服务器)",
            lambda match: str(cluster_chinese_numbers[match.group(1)]),
            value,
        )
        value = re.sub(r"\betcd(\d+(?:\.\d+)+)", r"etcd \1", value, flags=re.IGNORECASE)
        value = re.sub(r"\bNote(\d+)\b", r"Note \1", value, flags=re.IGNORECASE)
        value = re.sub(r"\bPython(\d+(?:\.\d+)+)", r"Python \1", value, flags=re.IGNORECASE)
        value = re.sub(r"\bday-2\b", "day-two", value, flags=re.IGNORECASE)
        cluster_number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+(?=(?:(?:disconnected|active|voting|non-voting|new|healthy|unhealthy)\s+)?(?:members?|followers?|leaders?|nodes?)\b)",
            lambda match: str(cluster_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        french_number_words = {
            "un": 1,
            "une": 1,
            "deux": 2,
            "trois": 3,
            "quatre": 4,
            "cinq": 5,
            "six": 6,
            "sept": 7,
            "huit": 8,
            "neuf": 9,
            "dix": 10,
        }
        value = re.sub(
            r"\b(un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\s+"
            r"(?=(?:(?:déconnectés?|actifs?|votants?|nouveaux?|sains?)\s+)?"
            r"(?:membres?|suiveurs?|leaders?|n(?:œ|oe)uds?|serveurs?)\b)",
            lambda match: str(french_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(r"\bHTTP/?(\d+(?:\.\d+)*)", r"HTTP \1", value, flags=re.IGNORECASE)
        value = re.sub(r"\bend-2-end\b", "end-to-end", value, flags=re.IGNORECASE)
        value = re.sub(r"(?<!\w)(\d+(?:\.\d+)?)x\b", r"\1", value, flags=re.IGNORECASE)
        value = re.sub(
            r"(?<!\w)(\d+(?:\.\d+)?)\s*(kb|mb|gb|tb)\b",
            lambda match: match.group(1) + {"kb": "kB", "mb": "MB", "gb": "GB", "tb": "TB"}[match.group(2).lower()],
            value,
            flags=re.IGNORECASE,
        )
        hardware_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        value = re.sub(
            r"\b(\d+)x\s+(?:dedicated\s+)?(?=(?:local\s+)?(?:SSDs?|disks?|CPUs?)\b)",
            r"\1 ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:dedicated\s+)?(?=(?:local\s+)?(?:SSDs?|disks?|CPUs?)\b)",
            lambda match: str(hardware_numbers[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\s+"
            r"(?:dédiés?\s+)?(?=(?:locaux?\s+)?(?:SSD|disques?|CPU)\b)",
            lambda match: str(french_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(r"\b([1-5]\d\d)s\b", r"\1 responses", value)
        value = re.sub(r"\bRFC\s*(\d+)\b", r"RFC \1", value, flags=re.IGNORECASE)
        value = re.sub(
            r"\b(TLS|SSL)v?(\d+(?:\.\d+)+)",
            r"\1 \2",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(?<!\w)(\d+)\s+first\s+bytes\b",
            r"\1B first",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(?<!\w)(\d+)\s+to\s+(\d+)\s+extra\s+bytes\b",
            r"\1 to \2B extra",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\badds\s+(\d+)\s+bytes([^.]{0,100}?)\band\s+(\d+)\s+for\b",
            lambda match: f"adds {match.group(1)}B{match.group(2)} and {match.group(3)}B for",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(r"\b0-?rtt\b", "ZERORTT", value, flags=re.IGNORECASE)
        value = re.sub(
            r"(\d+)\s+segments?\s+of\s+(\d+)\s+each",
            r"\1 segments of \2B each",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(?<!\w)(\d+(?:\.\d+)?)\s*-\s*(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)\b",
            r"\1\2",
            value,
        )
        value = re.sub(
            r"(?<!\w)(\d+(?:\.\d+)?)\s*[-~～]\s*(\d+(?:\.\d+)?)\s*(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)",
            r"\1\3-\2\3",
            value,
        )
        months = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12,
            "janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
            "juin": 6, "juillet": 7, "août": 8, "septembre": 9,
            "octobre": 10, "novembre": 11, "décembre": 12,
        }
        value = re.sub(
            r"\b(" + "|".join(months) + r")\b",
            lambda match: str(months[match.group(1)]),
            value,
        )
        value = re.sub(r"\bzero\b", "0", value, flags=re.IGNORECASE)
        value = re.sub(r"\bzéro\b", "0", value, flags=re.IGNORECASE)
        value = re.sub(
            r"\ba\s+(?=seconds?|minutes?|hours?|days?\b)",
            "1 ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(?:un|une)\s+(?=nanosecondes?|microsecondes?|millisecondes?|secondes?|minutes?|heures?|jours?|octets?\b)",
            "1 ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(?<!\w)(\d+(?:\.\d+)?)\s+or\s+more\s+(seconds?|milliseconds?|minutes?|hours?|days?|bytes?)\b",
            r"\1 \2 or more",
            value,
            flags=re.IGNORECASE,
        )
        chinese_unit_numbers = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
        def chinese_tens(match: re.Match[str]) -> str:
            raw = match.group(1)
            before, _, after = raw.partition("十")
            tens = chinese_unit_numbers.get(before, 1) if before else 1
            ones = chinese_unit_numbers.get(after, 0) if after else 0
            return str(tens * 10 + ones)
        value = re.sub(
            r"([一二三四五六七八九]?十[一二三四五六七八九]?)(?=纳秒|微秒|毫秒|秒|分钟|小时|天|字节)",
            chinese_tens,
            value,
        )
        value = re.sub(
            r"([一二两三四五六七八九十])\s*(?=纳秒|微秒|毫秒|秒|分钟|小时|天|字节)",
            lambda match: str(chinese_unit_numbers[match.group(1)]),
            value,
        )
        value = re.sub(r"\bpower\s+of\s+two\b", "power of 2", value, flags=re.IGNORECASE)
        value = re.sub(
            r"(\d+)\s+bytes(\s+[^.]{0,120}?\bor\s+)(\d+)(\s+when\b)",
            r"\1 bytes\2\3B\4",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\bbetween\s+one\s+and\s+two\b",
            "between 1 and 2",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\bentre\s+un\s+et\s+deux\b",
            "between 1 and 2",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\bbetween\s+once\s+to\s+twice\b",
            "between 1 and 2 times",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(\d+(?:\.\d+)?)\s*(纳秒|微秒|毫秒|秒|分钟|小时|天|字节)\s*(或|和|与|、)\s*(\d+(?:\.\d+)?)\s*\2",
            r"\1 \3 \4 \2",
            value,
        )
        unit_words = {
            "nanoseconds": "ns", "nanosecond": "ns",
            "microseconds": "us", "microsecond": "us",
            "milliseconds": "ms", "millisecond": "ms",
            "seconds": "s", "second": "s",
            "minutes": "min", "minute": "min",
            "hours": "h", "hour": "h",
            "days": "d", "day": "d",
            "bytes": "B", "byte": "B",
            "nanosecondes": "ns", "nanoseconde": "ns",
            "microsecondes": "us", "microseconde": "us",
            "millisecondes": "ms", "milliseconde": "ms",
            "secondes": "s", "seconde": "s",
            "heures": "h", "heure": "h",
            "jours": "d", "jour": "d",
            "octets": "B", "octet": "B",
        }
        small_number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\s+(?=(?:" + "|".join(unit_words) + r"|ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB)\b)",
            lambda match: str(small_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\s+"
            r"(?=(?:" + "|".join(unit_words)
            + r"|ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB)\b)",
            lambda match: str(french_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(\d+(?:\.\d+)?)\s+(nanoseconds?|microseconds?|milliseconds?|seconds?|minutes?|hours?|days?|bytes?)\s+(or|and)\s+(\d+(?:\.\d+)?)\s+\2",
            r"\1 \3 \4 \2",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\bbetween\s+(\d+(?:\.\d+)?)\s+(?:and|to)\s+(\d+(?:\.\d+)?)(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)\b",
            lambda match: f"between {match.group(1)}{match.group(3)} and {match.group(2)}{match.group(3)}",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(?<!\w)(\d+(?:\.\d+)?)\s*-?\s*(" + "|".join(unit_words) + r")\b",
            lambda match: match.group(1) + unit_words[match.group(2).lower()],
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(\bstarting\s+(?:at|from)\s+)one\b",
            r"\g<1>1",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"(\b(?:incremented|decremented)\s+)once\b",
            r"\g<1>1",
            value,
            flags=re.IGNORECASE,
        )
        def scaled(match: re.Match[str]) -> str:
            multipliers = {
                "thousand": Decimal(1_000),
                "million": Decimal(1_000_000),
                "billion": Decimal(1_000_000_000),
                "万": Decimal(10_000),
                "亿": Decimal(100_000_000),
            }
            number = Decimal(match.group(1)) * multipliers[match.group(2).lower()]
            return format(number, "f").rstrip("0").rstrip(".") if "." in format(number, "f") else format(number, "f")

        value = re.sub(
            r"\b(?:a|one)\s+(\d+)(?:st|nd|rd|th)\s+of\b",
            lambda match: f"1/{match.group(1)}",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(r"(?<!\w)(\d+)(?:st|nd|rd|th)\b", r"\1", value)
        bit_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight)\s+(?=bits?\b)",
            lambda match: str(bit_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight)\s+((?:upper|lower|high|low)\s+)(?=bits?\b)",
            lambda match: str(bit_words[match.group(1).lower()]) + " " + match.group(2),
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight)\s+((?:upper|lower|high|low)\s+)(?=(?:are|were)\b)",
            lambda match: str(bit_words[match.group(1).lower()]) + " " + match.group(2),
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(
            r"\b(un|une|deux|trois|quatre|cinq|six|sept|huit)\s+(?=bits?\b)",
            lambda match: str(french_number_words[match.group(1).lower()]) + " ",
            value,
            flags=re.IGNORECASE,
        )
        value = re.sub(r"(?<!\w)(\d+)\s*-?\s*bits?\b", r"\1", value, flags=re.IGNORECASE)
        value = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\s*-?\s*(thousand|million|billion|万|亿)(?![A-Za-z])", scaled, value, flags=re.IGNORECASE)
        unit_aliases = {"纳秒": "ns", "微秒": "us", "毫秒": "ms", "秒": "s", "分钟": "min", "小时": "h", "天": "d", "字节": "B"}
        tokens = []
        for token in NUMBER_TOKEN_RE.findall(value):
            token = re.sub(r"[\s\u00a0\u202f]+", "", token)
            if token.endswith("KB"):
                token = token[:-2] + "kB"
            if re.fullmatch(r"[vV]\d+(?:\.\d+)*(?:[-+][A-Za-z0-9.-]+)?", token):
                token = token[1:]
            for localized, canonical in unit_aliases.items():
                if token.endswith(localized):
                    token = token[: -len(localized)] + canonical
                    break
            tokens.append(token)
        if os.environ.get("TRANSLATION_DEBUG"):
            print(f"debug normalized numbers: {value!r} -> {tokens!r}", file=sys.stderr)
        return sorted(tokens)

    source_tokens = number_tokens(source)
    translated_tokens = number_tokens(translated)
    source_counter = Counter(source_tokens)
    translated_counter = Counter(translated_tokens)
    if source_counter != translated_counter:
        chinese_digits = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
        small_units = {"十": 10, "百": 100, "千": 1000}
        big_units = {"万": 10_000, "亿": 100_000_000}

        def parse_chinese_number(raw: str) -> int:
            total = section = digit = 0
            for char in raw:
                if char in chinese_digits:
                    digit = chinese_digits[char]
                elif char in small_units:
                    section += (digit or 1) * small_units[char]
                    digit = 0
                elif char in big_units:
                    section += digit
                    total += section * big_units[char]
                    section = digit = 0
            return total + section + digit

        classifiers = set("个行次年秒倍核位条台名项种套级层字分时端侧份处路方元步")
        chinese_values: list[int] = []
        chinese_values.extend([0] * translated.count("零"))
        chinese_values.extend([0] * translated.count("非零"))
        chinese_values.extend([0] * translated.count("不为零"))
        chinese_values.extend([0] * translated.count("零值"))
        chinese_values.extend([0] * translated.count("空字符"))
        chinese_values.extend([0] * translated.count("空字节"))
        for match in re.finditer(
            r"([零〇一二两三四五六七八九十百千万亿]+)对([零〇一二两三四五六七八九十百千万亿]+)",
            translated,
        ):
            chinese_values.extend(
                (parse_chinese_number(match.group(1)), parse_chinese_number(match.group(2)))
            )
        for match in re.finditer(r"[零〇一二两三四五六七八九十百千万亿]+", translated):
            follows_classifier = match.end() < len(translated) and translated[match.end()] in classifiers
            if len(match.group(0)) > 1 or follows_classifier:
                chinese_values.append(parse_chinese_number(match.group(0)))

        target_counter = Counter(translated_tokens)
        for token, needed in (source_counter - target_counter).items():
            if token.isdigit():
                available = chinese_values.count(int(token))
                target_counter[token] += min(needed, available)
        translated_tokens = sorted(target_counter.elements())

    translated_counter = Counter(translated_tokens)
    if TARGET_LANGUAGE == "ja":
        # Japanese may render English singulars and ordinal words with Arabic
        # digits. Only consume target-side extras backed by those source words;
        # explicit source digits remain mandatory.
        optional_ones = len(re.findall(r"\bone\b", source, flags=re.IGNORECASE))
        optional_ones += 2 * len(re.findall(r"\btwo\b", source, flags=re.IGNORECASE))
        optional_ones += len(re.findall(r"\bone\s+per\b", source, flags=re.IGNORECASE))
        optional_ones += len(re.findall(r"\ba\s+single\b", source, flags=re.IGNORECASE))
        optional_ones += len(
            re.findall(r"\bper\s+[A-Za-z][A-Za-z-]*\b", source, flags=re.IGNORECASE)
        )
        optional_numbers = Counter({"1": optional_ones})
        implicit_units = {
            "nanosecond": "1ns", "microsecond": "1us", "millisecond": "1ms",
            "second": "1s", "minute": "1min", "hour": "1h", "day": "1d",
            "byte": "1B",
        }
        for unit, token in implicit_units.items():
            optional_numbers[token] += len(
                re.findall(rf"\bper\s+{unit}\b", source, flags=re.IGNORECASE)
            )
        ordinal_numbers = {
            "first": "1", "second": "2", "third": "3", "fourth": "4",
            "fifth": "5", "sixth": "6", "seventh": "7", "eighth": "8",
            "ninth": "9", "tenth": "10",
        }
        for word, token in ordinal_numbers.items():
            optional_numbers[token] += len(
                re.findall(rf"\b{word}\b", source, flags=re.IGNORECASE)
            )
        for token, allowance in optional_numbers.items():
            extra_count = max(0, translated_counter[token] - source_counter[token])
            if extra_count and allowance:
                translated_counter[token] -= min(extra_count, allowance)
                if translated_counter[token] == 0:
                    del translated_counter[token]
    if TARGET_LANGUAGE == "fr":
        missing_ones = max(0, source_counter["1"] - translated_counter["1"])
        if missing_ones and re.search(r"\badding one node\b", source, flags=re.IGNORECASE):
            implicit_one_nodes = len(
                re.findall(
                    r"\b(?:l'ajout d'|ajouter )un n[œo]ud\b",
                    translated,
                    flags=re.IGNORECASE,
                )
            )
            translated_counter["1"] += min(missing_ones, implicit_one_nodes)
        missing_ones = max(0, source_counter["1"] - translated_counter["1"])
        if missing_ones and re.search(r"\bone member\b", source, flags=re.IGNORECASE):
            implicit_one_members = len(
                re.findall(r"\bun membre\b", translated, flags=re.IGNORECASE)
            )
            translated_counter["1"] += min(missing_ones, implicit_one_members)
        missing_zeros = max(0, source_counter["0"] - translated_counter["0"])
        missing_zero_bytes = max(0, source_counter["0B"] - translated_counter["0B"])
        if (
            missing_zero_bytes
            and re.search(r"\b(?:zero|0)[- ](?:bytes?|octets?)\b", source, flags=re.IGNORECASE)
        ):
            implicit_zero_bytes = len(
                re.findall(r"\boctets? (?:nuls?|à zéro)\b", translated, flags=re.IGNORECASE)
            )
            translated_counter["0B"] += min(missing_zero_bytes, implicit_zero_bytes)
        implicit_zero_transfers = len(
            re.findall(
                r"\b(?:aucune? (?:transmission|transfert)|sans (?:transmission|transfert)) de données\b",
                translated,
                flags=re.IGNORECASE,
            )
        )
        implicit_zero_terminators = 0
        if re.search(r"\bzero-terminated\b", source, flags=re.IGNORECASE):
            implicit_zero_terminators = len(
                re.findall(r"\boctets? nuls?\b", translated, flags=re.IGNORECASE)
            )
        implicit_zeros = implicit_zero_transfers + implicit_zero_terminators
        if re.search(r"\bzero-downtime\b", source, flags=re.IGNORECASE):
            implicit_zeros += len(
                re.findall(
                    r"\bsans interruption de service\b",
                    translated,
                    flags=re.IGNORECASE,
                )
            )
        if missing_zeros and implicit_zeros:
            translated_counter["0"] += min(missing_zeros, implicit_zeros)
        both_allowance = len(re.findall(r"\bboth\b", source, flags=re.IGNORECASE))
        both_allowance += len(
            re.findall(r"\bonly one of them\b", source, flags=re.IGNORECASE)
        )
        both_allowance += len(
            re.findall(r"\ball of which\b", source, flags=re.IGNORECASE)
        )
        both_allowance += len(
            re.findall(r"\b(?:in )?either direction\b", source, flags=re.IGNORECASE)
        )
        both_allowance += len(
            re.findall(r"\beither way\b", source, flags=re.IGNORECASE)
        )
        extra_twos = max(0, translated_counter["2"] - source_counter["2"])
        if extra_twos and both_allowance:
            translated_counter["2"] -= min(extra_twos, both_allowance)
            if translated_counter["2"] == 0:
                del translated_counter["2"]
    missing = source_counter - translated_counter
    extra = translated_counter - source_counter
    if missing or extra:
        raise ValueError(
            "numbers, versions, or units changed "
            f"source={source_tokens!r} translated={translated_tokens!r}"
        )


def validate_target_language(translated: str) -> None:
    """Reject obvious English prose left in Japanese or French output."""

    if TARGET_LANGUAGE == "zh":
        return
    if TARGET_LANGUAGE == "ja":
        for number, line in enumerate(translated.splitlines(), 1):
            if re.match(r"^[ \t]*[-+*][ \t]+(?:の|と|を|が|は)(?:[ \t]|[A-Za-z`\[])", line):
                raise ValueError(
                    f"Japanese list item starts with a dangling particle on line {number}: {line!r}"
                )
    english_function_words = {
        "a", "an", "and", "are", "as", "be", "been", "but", "by", "can",
        "for", "from", "has", "have", "if", "in", "into", "is", "it", "may",
        "must", "not", "of", "on", "or", "should", "that", "the", "this", "to",
        "was", "were", "when", "where", "which", "will", "with", "you", "your",
    }
    french_function_words = {
        "au", "aux", "avec", "ce", "ces", "cette", "dans", "de", "des", "du",
        "elle", "en", "est", "et", "il", "la", "le", "les", "ne", "ou", "pas",
        "par", "pour", "que", "qui", "sont", "sur", "un", "une",
    }
    short_markers = {
        "ja": {
            "caution", "contents", "download", "example", "examples", "important",
            "install", "introduction", "note", "overview", "prerequisites", "procedure",
            "pooling", "read", "statement", "tip", "usage", "warning",
        },
        "fr": {"caution", "contents", "download", "install", "overview", "prerequisites", "warning"},
    }[TARGET_LANGUAGE]

    for number, line in enumerate(translated.splitlines(), 1):
        clean = re.sub(r"\[![A-Za-z]+\]", "", line)
        clean = re.sub(r"`+[^`]*`+", "", clean)
        clean = re.sub(r"https?://\S+", "", clean)
        clean = re.sub(r"</?[A-Za-z][^>]*>", "", clean)
        clean = re.sub(r"\{#[^}]+\}", "", clean)
        clean = re.sub(r"^[ \t]*(?:>+[ \t]*)?(?:[-+*]|\d{1,2}[.)])[ \t]+", "", clean)
        if re.fullmatch(
            r"/\?\S+\s+(?:->|-\\>)\s+/\?\S+",
            clean.strip(),
        ):
            continue
        if TARGET_LANGUAGE == "fr" and re.search(
            r"[\u3040-\u30ff\u3400-\u9fff]", clean
        ):
            raise ValueError(
                f"non-French CJK text on line {number}: {line!r}"
            )
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", clean.lower())
        if not words:
            continue
        stripped_words = set(words)
        if len(words) <= 3 and stripped_words <= short_markers:
            raise ValueError(f"untranslated English label on line {number}: {line!r}")
        english_score = sum(word in english_function_words for word in words)
        if TARGET_LANGUAGE == "ja":
            japanese_chars = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", clean))
            if len(words) >= 6 and english_score >= 2 and japanese_chars == 0:
                raise ValueError(f"untranslated English prose on line {number}: {line!r}")
        else:
            french_score = sum(word in french_function_words for word in words)
            if len(words) >= 8 and english_score >= 3 and english_score > french_score + 1:
                raise ValueError(f"untranslated English prose on line {number}: {line!r}")


def translate_html_fragment(
    fragment: str,
    *,
    component: str,
    model: str,
    cache: Cache,
) -> str:
    """Translate raw-HTML prose one line at a time while preserving its tags."""

    output: list[str] = []
    in_pre = False
    for line in fragment.splitlines(keepends=True):
        lower = line.lower()
        if in_pre or "<pre" in lower:
            output.append(line)
            if "</pre>" in lower:
                in_pre = False
            elif "<pre" in lower:
                in_pre = True
            continue

        content = line[:-1] if line.endswith("\n") else line
        newline = "\n" if line.endswith("\n") else ""
        leading_match = re.match(r"^[ \t]*", content)
        leading = leading_match.group(0) if leading_match else ""
        core = content[len(leading) :]
        visible = re.sub(r"</?[A-Za-z][^>\n]*>", "", core)
        if not ASCII_WORD_RE.search(visible):
            output.append(line)
            continue
        translated = translate_text(
            core + newline,
            component=component,
            model=model,
            cache=cache,
        )
        output.append(leading + translated)
    return "".join(output)


def translate_scalar_preserving_prefix(
    value: str,
    *,
    component: str,
    model: str,
    cache: Cache,
    fallback_model: str | None = None,
) -> str:
    # Chapter numbers are navigation syntax, not prose. Keeping them outside the
    # model prevents translations such as "Prerequisites 1.".
    number_match = re.match(r"^(\d+(?:\.\d+)*\.\s+)(.+)$", value)
    prefix, prose = number_match.groups() if number_match else ("", value)
    brand_match = re.match(
        r"^((?:HAProxy|etcd)(?:\s+[vV]?\d+(?:\.\d+){1,3})?\s+)(.+)$",
        prose,
    )
    if brand_match:
        brand_prefix, prose = brand_match.groups()
        prefix += brand_prefix
    if prose in {"HAProxy", "etcd", "etcdctl"}:
        return prefix + prose
    if re.fullmatch(r"[a-z][a-z0-9_.-]*", prose):
        return prefix + prose
    command_words = re.findall(r"[A-Za-z_]+", prose)
    if (
        command_words
        and command_words[0].isupper()
        and all(word.isupper() or word in {"db", "id", "key", "arg"} for word in command_words)
    ):
        return prefix + prose
    glossary_translation = exact_glossary_translation(component, prose)
    if glossary_translation is not None:
        return prefix + glossary_translation
    try:
        translated = translate_text(
            prose,
            component=component,
            model=model,
            cache=cache,
            mode="scalar",
        )
    except RuntimeError:
        if not fallback_model or fallback_model == model:
            raise
        translated = translate_text(
            prose,
            component=component,
            model=fallback_model,
            cache=cache,
            mode="scalar",
        )
    return prefix + translated


def rendered_heading_ids(source: Path, expected_levels: list[int] | None = None) -> list[str]:
    relative = source.relative_to(CONTENT)
    if source.name == "_index.md":
        route = relative.parent
    elif source.name == "index.md":
        route = relative.parent
    else:
        route = relative.with_suffix("")
    rendered = PROJECT / "public" / route / "index.html"
    if not rendered.is_file():
        return []
    document = rendered.read_text(encoding="utf-8", errors="replace")
    rendered = [
        (int(level), html.unescape(quoted or single_quoted or bare))
        for level, quoted, single_quoted, bare in re.findall(
            r"<h([1-6])\b[^>]*\sid=(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))",
            document,
        )
    ]
    if expected_levels is not None and len(rendered) != len(expected_levels):
        for start in range(0, len(rendered) - len(expected_levels) + 1):
            window = rendered[start : start + len(expected_levels)]
            if [level for level, _ in window] == expected_levels:
                return [value for _, value in window]
    return [value for _, value in rendered]


def add_heading_anchors(body: str, source: Path) -> str:
    if source.parts[-2] == "haproxy" or "haproxy" in source.parts:
        return body
    lines = body.splitlines(keepends=True)
    flags = verbatim_ranges(lines)
    source_headings = [
        line
        for index, line in enumerate(lines)
        if not flags[index] and HEADING_RE.match(line.rstrip("\n"))
    ]
    explicit_count = sum(
        bool(HEADING_RE.match(line.rstrip("\n")).group("anchor"))  # type: ignore[union-attr]
        for line in source_headings
    )
    if not source_headings:
        return body
    expected_levels = [
        len(HEADING_RE.match(line.rstrip("\n")).group("marks"))  # type: ignore[union-attr]
        for line in source_headings
    ]
    heading_ids = rendered_heading_ids(source, expected_levels)
    if len(heading_ids) != len(source_headings):
        raise RuntimeError(
            f"cannot align rendered heading IDs for {source.relative_to(PROJECT)}: "
            f"source={len(source_headings)}, rendered={len(heading_ids)}, explicit={explicit_count}"
        )

    output: list[str] = []
    heading_index = 0
    for index, line in enumerate(lines):
        newline = "\n" if line.endswith("\n") else ""
        content = line[:-1] if newline else line
        match = None if flags[index] else HEADING_RE.match(content)
        if not match:
            output.append(line)
            continue
        anchor = match.group("anchor") or f" {{#{heading_ids[heading_index]}}}"
        output.append(
            f'{match.group("marks")}{match.group("space")}{match.group("title")}{anchor}{newline}'
        )
        heading_index += 1
    return "".join(output)


def split_front_matter(document: str) -> tuple[str, str]:
    if not document.startswith("---\n"):
        raise RuntimeError("document has no YAML front matter")
    end = document.find("\n---\n", 4)
    if end < 0:
        raise RuntimeError("document has unterminated YAML front matter")
    return document[4:end], document[end + 5 :]


def quote_yaml(value: str, quote: str) -> str:
    if quote == '"':
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if quote == "'":
        return "'" + value.replace("'", "''") + "'"
    if re.search(r"[:#\[\]{}&,*!|>'\"%@`]", value) or value.strip() != value:
        return json.dumps(value, ensure_ascii=False)
    return value


def translate_front_matter(
    front: str,
    *,
    component: str,
    scalar_model: str,
    fallback_model: str,
    cache: Cache,
) -> str:
    output: list[str] = []
    scalar_re = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z][A-Za-z0-9_]*):\s*(?P<value>.*)$")
    lines = front.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = scalar_re.match(line)
        if not match:
            output.append(line)
            index += 1
            continue
        key = match.group("key")
        raw = match.group("value")
        if key == "categories":
            localized = raw
            for english, chinese in CATEGORY_MAP.items():
                localized = re.sub(rf"\b{english}\b", chinese, localized)
            output.append(f'{match.group("indent")}{key}: {localized}')
            index += 1
            continue
        if key in TRANSLATABLE_META and raw.rstrip("+-") in {">", "|"}:
            output.append(line)
            parent_indent = len(match.group("indent"))
            block_lines: list[str] = []
            index += 1
            while index < len(lines):
                child = lines[index]
                child_indent = len(child) - len(child.lstrip())
                if child.strip() and child_indent <= parent_indent:
                    break
                block_lines.append(child)
                index += 1
            nonblank = [child.strip() for child in block_lines if child.strip()]
            if not nonblank:
                output.extend(block_lines)
                continue
            source_value = (
                " ".join(nonblank)
                if raw.startswith(">")
                else "\n".join(nonblank)
            )
            try:
                translated = translate_text(
                    source_value,
                    component=component,
                    model=scalar_model,
                    cache=cache,
                ).strip()
            except RuntimeError:
                translated = translate_text(
                    source_value,
                    component=component,
                    model=fallback_model,
                    cache=cache,
                ).strip()
            child_indent = " " * (parent_indent + 2)
            output.extend(child_indent + child for child in translated.splitlines())
            continue
        if key not in TRANSLATABLE_META or not raw:
            output.append(line)
            index += 1
            continue
        quote = raw[0] if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"} else ""
        value = raw[1:-1] if quote else raw
        translated = translate_scalar_preserving_prefix(
            value,
            component=component,
            model=scalar_model,
            cache=cache,
            fallback_model=fallback_model,
        )
        output.append(
            f'{match.group("indent")}{key}: {quote_yaml(translated, quote)}'
        )
        index += 1
    return "\n".join(output)


def verbatim_ranges(lines: list[str]) -> list[bool]:
    verbatim = [False] * len(lines)
    fence_marker = ""
    in_comment = False
    for index, line in enumerate(lines):
        stripped = line.rstrip("\n")
        if fence_marker:
            verbatim[index] = True
            if stripped.lstrip().startswith(fence_marker):
                fence_marker = ""
            continue
        fence = FENCE_RE.match(stripped)
        if fence:
            verbatim[index] = True
            fence_marker = fence.group(1)
            continue
        if in_comment:
            verbatim[index] = True
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            verbatim[index] = True
            if "-->" not in line:
                in_comment = True
            continue
        if (
            REFERENCE_DEF_RE.match(stripped)
            or ANCHOR_ONLY_RE.match(stripped)
            or ATTRIBUTION_RE.match(stripped)
        ):
            verbatim[index] = True
    if fence_marker:
        raise RuntimeError("unterminated Markdown fence")
    if in_comment:
        raise RuntimeError("unterminated HTML comment")
    return verbatim


def preserve_legal_text(lines: list[str], flags: list[bool], source: Path) -> None:
    """Keep the embedded PostgreSQL License text legally authoritative."""

    if source.relative_to(CONTENT).as_posix() != "pgbadger/license.md":
        return
    in_license = False
    for index, line in enumerate(lines):
        if line.startswith("## PostgreSQL License"):
            in_license = True
            continue
        if in_license and line.startswith("## "):
            break
        if in_license:
            flags[index] = True


def translate_body(
    body: str,
    *,
    source: Path,
    component: str,
    model: str,
    scalar_model: str,
    cache: Cache,
    max_chars: int,
) -> str:
    body = add_heading_anchors(body, source)
    lines = body.splitlines(keepends=True)
    flags = verbatim_ranges(lines)
    preserve_legal_text(lines, flags, source)
    output: list[str] = []
    buffer: list[str] = []
    buffer_size = 0

    def flush() -> None:
        nonlocal buffer, buffer_size
        if not buffer:
            return
        fragment = "".join(buffer)
        nonblank = [line for line in fragment.splitlines() if line.strip()]
        first_line = nonblank[0].lstrip() if nonblank else ""
        quote_lines = [line.lstrip()[1:].strip() for line in fragment.splitlines() if line.lstrip().startswith(">")]
        literal_quote = bool(quote_lines) and all(
            not content or re.fullmatch(r"`.*`", content)
            for content in quote_lines
        )
        config_prefix = re.match(
            r"^(?:\.(?:if|elif|else|endif)|frontend|backend|listen|defaults|global|fcgi-app|cache|peers|ring|resolvers|userlist|stick-table|table|shards|acl|http-request|http-response|tcp-request|tcp-response|http-check|tcp-check|use_backend|default_backend)\b",
            first_line,
        )
        indented_block = bool(nonblank) and all(
            line.startswith(("    ", "\t"))
            and not re.match(r"^\s*(?:>|[-+*]\s+|\d+[.)]\s+)", line)
            for line in nonblank
        )
        prose_function_words = {
            "a", "an", "and", "are", "as", "be", "by", "can", "for", "from",
            "has", "have", "if", "in", "is", "it", "may", "must", "not", "of",
            "on", "or", "should", "that", "the", "this", "to", "when", "which",
            "will", "with",
        }
        visible_indented = re.sub(r"`+[^`]*`+", "", fragment)
        visible_indented = re.sub(r"https?://\S+", "", visible_indented)
        prose_words = re.findall(r"[A-Za-z][A-Za-z'-]*", visible_indented.lower())
        indented_prose = (
            indented_block
            and len(prose_words) >= 6
            and sum(word in prose_function_words for word in prose_words) >= 2
            and not first_line.startswith(("$", "#", "//", "\"", "'", "[", "{"))
        )
        indented_code = indented_block and not indented_prose
        raw_config = bool(config_prefix)
        if first_line.startswith("Usable in:"):
            output.append(
                re.sub(
                    r"^(\s*)Usable in:",
                    rf"\1{USABLE_IN_TRANSLATION}",
                    fragment,
                    count=1,
                )
            )
        elif fragment.strip("\n") in MANUAL_TRANSLATIONS:
            output.append(
                translate_text(
                    fragment,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
        elif component == "etcd" and re.search(
            r"</?(?:table|thead|tbody|tr|th|td|p|ul|li|pre|strong|a)\b",
            fragment,
            flags=re.IGNORECASE,
        ):
            output.append(
                translate_html_fragment(
                    fragment,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
        elif indented_prose:
            dedented = textwrap.dedent(fragment)
            translated = translate_text(
                dedented,
                component=component,
                model=model,
                cache=cache,
            )
            common_indent = min(
                len(re.match(r"^[ \t]*", line).group(0).expandtabs(4))
                for line in fragment.splitlines()
                if line.strip()
            )
            output.append(
                "".join(
                    (" " * common_indent + line if line.strip() else line)
                    for line in translated.splitlines(keepends=True)
                )
            )
        elif (
            re.search(
                r"(?:Active Internet connections|Proto\s+Recv-Q|PID/Program name|"
                r"HAProxy version .*Copyright|Build options:|Default settings:|"
                r"Encrypted password support|Available polling systems:|Total: \d+)",
                fragment,
            )
            or indented_code
            or raw_config
            or literal_quote
        ):
            output.append(fragment)
        else:
            output.append(
                translate_text(
                    fragment,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
        buffer = []
        buffer_size = 0

    for index, line in enumerate(lines):
        if flags[index]:
            flush()
            output.append(line)
            continue
        newline = "\n" if line.endswith("\n") else ""
        content = line[:-1] if newline else line
        emphasis_heading = re.match(
            r"^(?P<indent>\s*)(?P<marker>\*{1,2})(?!\s)"
            r"(?P<title>.+?)(?P=marker)\s*$",
            content,
        )
        if emphasis_heading:
            flush()
            translated_italic = translate_scalar_preserving_prefix(
                emphasis_heading.group("title"),
                component=component,
                model=scalar_model,
                cache=cache,
                fallback_model=model,
            )
            output.append(
                f'{emphasis_heading.group("indent")}{emphasis_heading.group("marker")}'
                f'{translated_italic}{emphasis_heading.group("marker")}{newline}'
            )
            continue
        heading = HEADING_RE.match(content)
        if heading:
            flush()
            translated_title = translate_scalar_preserving_prefix(
                heading.group("title"),
                component=component,
                model=scalar_model,
                cache=cache,
                fallback_model=model,
            )
            output.append(
                f'{heading.group("marks")}{heading.group("space")}{translated_title}'
                f'{heading.group("anchor") or ""}{newline}'
            )
            continue
        if TARGET_LANGUAGE == "ja" and buffer:
            current_item = re.match(r"^(?P<indent>[ \t]*)(?:[-+*]|\d{1,2}[.)])[ \t]+", line)
            first_buffer_line = next((item for item in buffer if item.strip()), "")
            buffered_item = re.match(
                r"^(?P<indent>[ \t]*)(?:[-+*]|\d{1,2}[.)])[ \t]+",
                first_buffer_line,
            )
            if (
                current_item
                and buffered_item
                and len(current_item.group("indent").expandtabs(4))
                >= len(buffered_item.group("indent").expandtabs(4))
            ):
                flush()
        if not line.strip():
            buffer.append(line)
            flush()
            continue
        if (
            buffer
            and buffer_size + len(line) > max_chars
            and re.match(r"^[ \t]*(?:[-+*]|\d{1,2}[.)])[ \t]+", line)
        ):
            flush()
        if buffer and buffer_size + len(line) > max_chars and not line.strip():
            buffer.append(line)
            flush()
            continue
        buffer.append(line)
        buffer_size += len(line)
        if buffer_size >= max_chars and not line.strip():
            flush()
    flush()
    translated = "".join(output)
    return localize_internal_links(translated, component)


def localize_internal_links(document: str, component: str) -> str:
    # Preserve code, literal output, and comments byte-for-byte. The negative
    # lookbehind prevents replacements inside absolute external URLs.
    lines = document.splitlines(keepends=True)
    output: list[str] = []
    fence_marker = ""
    in_comment = False
    for line in lines:
        stripped = line.rstrip("\n")
        if fence_marker:
            output.append(line)
            if stripped.lstrip().startswith(fence_marker):
                fence_marker = ""
            continue
        fence = FENCE_RE.match(stripped)
        if fence:
            fence_marker = fence.group(1)
            output.append(line)
            continue
        if in_comment:
            output.append(line)
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            output.append(line)
            if "-->" not in line:
                in_comment = True
            continue
        localized = line
        localized = re.sub(r"^(?P<indent>[ \t]*):[ \t]+", r"\g<indent>: ", localized)
        localized = localized.replace("**PgBouncer**", "**pgbouncer**")
        if TARGET_LANGUAGE == "ja":
            localized = localized.replace("より重要的是", "さらに重要なのは")
            localized = localized.replace("pbgouncer", "pgbouncer")
            localized = localized.replace("[ 会議発表の録画]", "[会議発表の録画]")
            localized = localized.replace("ローリング方式", "ラウンドロビン方式")
            localized = localized.replace("ユーザー別 equivalent", "ユーザー版")
            localized = localized.replace("examples セクション", "例のセクション")
            localized = re.sub(r"(注意|警告|重要|ヒント|デフォルト):", r"\1：", localized)
            if not localized.startswith(("    ", "\t")):
                localized = re.sub(
                    r"^(?P<prefix>[ \t]*(?:[-+*]|\d{1,2}[.)]))[ \t]+",
                    r"\g<prefix> ",
                    localized,
                )
        label_translations = {
            "zh": {"Note": "注意", "Warning": "警告", "Caution": "注意", "Important": "重要", "Tip": "提示"},
            "fr": {"Note": "Remarque", "Warning": "Avertissement", "Caution": "Attention", "Important": "Important", "Tip": "Conseil"},
            "ja": {"Note": "注意", "Warning": "警告", "Caution": "注意", "Important": "重要", "Tip": "ヒント"},
        }[TARGET_LANGUAGE]
        for english_label, target_label in label_translations.items():
            localized = re.sub(
                rf"^(?P<indent>[ \t]*){english_label}:[ \t]*",
                rf"\g<indent>{target_label}：",
                localized,
            )
        where_label = {
            "zh": "其中：",
            "fr": "où :",
            "ja": "ここで：",
        }[TARGET_LANGUAGE]
        localized = re.sub(
            r"^(?P<prefix>[ \t]*(?:>[ \t]*)?)where:[ \t]*(?P<newline>\n?)$",
            rf"\g<prefix>{where_label}\g<newline>",
            localized,
            flags=re.IGNORECASE,
        )
        if TARGET_LANGUAGE == "ja":
            localized = re.sub(
                r"^(?P<prefix>[ \t]*(?:>[ \t]*)?[-+*][ \t]+)"
                r"インストール[ \t]+(?P<literal>`[^`]+`)[。.]?"
                r"(?P<newline>\n?)$",
                r"\g<prefix>\g<literal> をインストールします\g<newline>",
                localized,
            )
        if TARGET_LANGUAGE == "fr":
            roots = LOCALIZABLE_ROOTS
        elif TARGET_LANGUAGE == "ja":
            roots = ("pgbouncer", "attribution", "search")
        else:
            roots = (component,)
        for root in roots:
            pattern = re.compile(rf'(?<![A-Za-z0-9_:/])/{re.escape(root)}/')
            localized = pattern.sub(f'/{TARGET_LANGUAGE}/{root}/', localized)
            localized = re.sub(
                rf"/{TARGET_LANGUAGE}/{re.escape(root)}/(?P<asset>[A-Za-z0-9_./-]+\.(?:png|gif|svg|json|txt))",
                rf"/{root}/\g<asset>",
                localized,
                flags=re.IGNORECASE,
            )
        output.append(localized)
    return "".join(output)


def validate_pair(source_text: str, translated_text: str, source: Path) -> None:
    source_front, source_body = split_front_matter(source_text)
    target_front, target_body = split_front_matter(translated_text)

    upstream_re = re.compile(r'^upstream_link:\s*(.+)$', re.MULTILINE)
    if upstream_re.findall(source_front) != upstream_re.findall(target_front):
        raise RuntimeError("upstream_link changed")

    source_fences = FENCE_RE.findall(source_body)
    target_fences = FENCE_RE.findall(target_body)
    if source_fences != target_fences:
        raise RuntimeError("Markdown fence sequence changed")

    source_refs = [line for line in source_body.splitlines() if REFERENCE_DEF_RE.match(line)]
    target_refs = []
    for line in target_body.splitlines():
        if not REFERENCE_DEF_RE.match(line):
            continue
        if TARGET_LANGUAGE == "fr":
            roots = LOCALIZABLE_ROOTS
        elif TARGET_LANGUAGE == "ja":
            roots = ("pgbouncer", "attribution", "search")
        else:
            roots = (source.relative_to(CONTENT).parts[0],)
        for root in roots:
            line = line.replace(f"/{TARGET_LANGUAGE}/{root}/", f"/{root}/")
        target_refs.append(line)
    if source_refs != target_refs:
        raise RuntimeError("reference definitions changed")

    source_shortcodes = re.findall(r"\{\{[%<].*?[>%]\}\}", source_body)
    target_shortcodes = re.findall(r"\{\{[%<].*?[>%]\}\}", target_body)
    if len(source_shortcodes) != len(target_shortcodes):
        raise RuntimeError("shortcode count changed")

    footnote_re = re.compile(r"\[\^[^\]\n]+\]")
    if footnote_re.findall(source_body) != footnote_re.findall(target_body):
        raise RuntimeError("footnote references changed")

def translate_file(
    source: Path,
    *,
    component: str,
    model: str,
    scalar_model: str,
    cache: Cache,
    max_chars: int,
    force: bool,
    dry_run: bool,
) -> Path:
    target = source.with_name(source.name.removesuffix(".md") + TARGET_SUFFIX)
    if target.exists() and not force:
        print(f"skip existing {target.relative_to(PROJECT)}", flush=True)
        return target
    source_text = source.read_text(encoding="utf-8")
    front, body = split_front_matter(source_text)
    translated_front = translate_front_matter(
        front,
        component=component,
        scalar_model=scalar_model,
        fallback_model=model,
        cache=cache,
    )
    translated_body = translate_body(
        body,
        source=source,
        component=component,
        model=model,
        scalar_model=scalar_model,
        cache=cache,
        max_chars=max_chars,
    )
    translated_text = f"---\n{translated_front}\n---\n{translated_body}"
    validate_pair(source_text, translated_text, source)
    if dry_run:
        print(translated_text)
        return target
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(translated_text, encoding="utf-8")
    os.replace(temporary, target)
    print(f"wrote {target.relative_to(PROJECT)}", flush=True)
    return target


def discover_sources(component: str, requested: list[str]) -> list[Path]:
    root = CONTENT if component == "site" else CONTENT / component
    if requested:
        sources = []
        for value in requested:
            path = Path(value)
            if not path.is_absolute():
                path = PROJECT / path
            path = path.resolve()
            if not path.is_file():
                raise RuntimeError(f"source does not exist: {value}")
            if path.name.endswith((".zh.md", ".fr.md", ".ja.md", ".de.md", ".ru.md")) or path.suffix != ".md":
                raise RuntimeError(f"not an English Markdown source: {value}")
            try:
                path.relative_to(root.resolve())
            except ValueError as exc:
                location = "content" if component == "site" else f"content/{component}"
                raise RuntimeError(f"source is outside {location}: {value}") from exc
            if component == "site" and path.parent != CONTENT.resolve():
                raise RuntimeError(f"site source is not a top-level content page: {value}")
            sources.append(path)
        return sorted(set(sources))
    candidates = root.glob("*.md") if component == "site" else root.rglob("*.md")
    return sorted(
        (
            path
            for path in candidates
            if not path.name.endswith((".zh.md", ".fr.md", ".ja.md", ".de.md", ".ru.md"))
        ),
        key=lambda path: (path.stat().st_size, str(path)),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("component", choices=SUPPORTED_COMPONENTS)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--language", choices=("zh", "fr", "ja"), default="zh")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--scalar-model", default=DEFAULT_SCALAR_MODEL)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--max-chars", type=int, default=5000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_language(args.language)
    if args.language == "zh" and args.component not in CHINESE_COMPONENTS:
        raise RuntimeError(
            "the Chinese generator is intentionally limited to haproxy and etcd"
        )
    if args.max_chars < 500:
        raise RuntimeError("--max-chars must be at least 500")
    sources = discover_sources(args.component, args.paths)
    if args.limit is not None:
        sources = sources[: args.limit]
    cache = Cache.load(args.cache or DEFAULT_CACHE)
    print(
        f"translating {len(sources)} {args.component} files to {args.language} "
        f"with {args.model}; "
        f"scalar model={args.scalar_model}; cache entries={len(cache.entries)}",
        flush=True,
    )
    for index, source in enumerate(sources, 1):
        print(f"[{index}/{len(sources)}] {source.relative_to(PROJECT)}", flush=True)
        translate_file(
            source,
            component=args.component,
            model=args.model,
            scalar_model=args.scalar_model,
            cache=cache,
            max_chars=args.max_chars,
            force=args.force,
            dry_run=args.dry_run,
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:  # Fail closed; partial targets are never renamed.
        print(f"translation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
