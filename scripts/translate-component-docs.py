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
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
STYLE_GUIDE = PROJECT / "TRANSLATION.md"
DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache.json"
DEFAULT_MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"
DEFAULT_SCALAR_MODEL = "qwen2.5:7b"
CACHE_SCHEMA_VERSION = "15"
SUPPORTED_COMPONENTS = ("haproxy", "etcd")

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

ASCII_WORD_RE = re.compile(r"[A-Za-z]{2,}")
NUMBER_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"(?:v|V)?\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?"
    r"|\d+(?:\.\d+)?(?:\s?(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|纳秒|微秒|毫秒|秒|分钟|小时|天|字节|%))?"
    r")(?![A-Za-z0-9])"
)
HEADING_RE = re.compile(
    r"^(?P<marks>#{1,6})(?P<space>\s+)(?P<title>.*?)(?P<anchor>\s+\{#[^}]+\})?\s*$"
)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
REFERENCE_DEF_RE = re.compile(r"^\s*\[[^]]+\]:\s+\S+")
ANCHOR_ONLY_RE = re.compile(r'^\s*<a\s+(?:id|name)="[^"]+"\s*></a>\s*$')


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
        token = f"⟦P{len(self.values) + 1:04d}⟧"
        self.values.append(value)
        return token

    def substitute(self, pattern: re.Pattern[str] | str, text: str) -> str:
        regex = re.compile(pattern) if isinstance(pattern, str) else pattern
        return regex.sub(lambda match: self.token(match.group(0)), text)

    def protect(self, text: str) -> str:
        # Protect larger Markdown constructs before their nested literals.
        text = self.substitute(r"`+[^`\n]*`+", text)
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
        text = self.substitute(r"&(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);", text)
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
        reference_link_re = re.compile(r"(?P<image>!?)\[(?P<label>[^]\n]*)\]\[(?P<ref>[^]\n]+)\]")
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
        return text

    def restore(self, text: str) -> str:
        for index, value in enumerate(self.values):
            token = f"⟦P{index + 1:04d}⟧"
            count = text.count(token)
            repeatable = bool(re.fullmatch(r"--?[A-Za-z0-9][A-Za-z0-9_.-]*(?:=[^\s,;]+)?", value))
            if count < 1 or (count > 1 and not repeatable):
                raise ValueError(f"placeholder {token} occurred {count} times")
            text = text.replace(token, value)
        if "⟦P" in text or "⟧" in text:
            raise ValueError("translation contains an unknown placeholder")
        return text


def parse_glossary(component: str, source: str) -> str:
    guide = STYLE_GUIDE.read_text(encoding="utf-8")
    display_name = "HAProxy" if component == "haproxy" else component
    heading = f"## {display_name} 术语表"
    try:
        section = guide.split(heading, 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise RuntimeError(f"missing glossary section {heading!r}") from exc
    entries: list[tuple[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or "英文" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2:
            entries.append((cells[0], cells[1]))
    source_lower = source.lower()
    selected: list[str] = []
    for english_term, chinese_term in entries:
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
            selected.append(f"{english_term} => {chinese_term}")
    return "；".join(selected)


def system_prompt(component: str, source: str, mode: str) -> str:
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


def normalize_chinese_spacing(value: str) -> str:
    """Apply the repository's Han/ASCII spacing rule outside fenced blocks."""
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
    payload = "\0".join((CACHE_SCHEMA_VERSION, model, component, mode, style_digest, prompt, source))
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
    placeholders = re.findall(r"⟦P\d{4}⟧", protected)
    if placeholders:
        instruction += "\n本片段中的占位符必须逐字各保留一次：" + "、".join(placeholders)
    else:
        instruction += "\n本片段没有占位符，禁止添加任何占位符。"
    prompt = f"{instruction}\n\n待翻译片段：\n{protected}"
    key = cache_key(model, component, mode, prompt, source)
    errors: list[str] = []
    cached_validation_error: str | None = None
    cached = cache.get(key)
    if cached is not None:
        cached = normalize_chinese_spacing(cached)
        try:
            validate_fragment_structure(source, cached)
            return cached
        except ValueError as exc:
            errors.append(f"cached translation: {exc}")
            cached_validation_error = str(exc)

    attempt_limit = 1 if os.environ.get("TRANSLATION_DEBUG") else retries
    attempt_prompt = prompt
    if cached_validation_error:
        attempt_prompt += (
            "\n\n现有译文未通过结构校验："
            + cached_validation_error
            + "。每个列表项必须单独成行，并严格保留原有缩进；不得合并、拆分或展平列表。"
        )
    for attempt in range(1, attempt_limit + 1):
        raw = ""
        try:
            raw = post_ollama(model, attempt_prompt)
            normalized = normalize_model_output(protected, raw)
            normalized = normalize_brand_spelling(normalized)
            restored = protector.restore(normalized)
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
            errors.append(f"attempt {attempt}: {exc}")
            source_numbers = NUMBER_TOKEN_RE.findall(source)
            placeholder_map = list(zip(placeholders, protector.values))
            placeholder_count_note = ""
            if len(placeholders) != len(protector.values):
                placeholder_count_note = (
                    f" 保护占位符计数不一致：片段中 {len(placeholders)} 个，"
                    f"原始字面量 {len(protector.values)} 个。"
                )
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
            time.sleep(min(attempt, 3))
    raise RuntimeError("; ".join(errors))


def validate_fragment_structure(source: str, translated: str) -> None:
    """Reject common model rewrites that would damage Markdown semantics."""

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

    def number_tokens(value: str) -> list[str]:
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
        }
        value = re.sub(
            r"\b(" + "|".join(months) + r")\b",
            lambda match: str(months[match.group(1)]),
            value,
        )
        value = re.sub(r"\bzero\b", "0", value, flags=re.IGNORECASE)
        value = re.sub(
            r"\ba\s+(?=seconds?|minutes?|hours?|days?\b)",
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
        }
        small_number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
        value = re.sub(
            r"\b(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\s+(?=(?:" + "|".join(unit_words) + r"|ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB)\b)",
            lambda match: str(small_number_words[match.group(1).lower()]) + " ",
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
        value = re.sub(r"(?<!\w)(\d+)\s*-?\s*bits?\b", r"\1", value, flags=re.IGNORECASE)
        value = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\s*-?\s*(thousand|million|billion|万|亿)(?![A-Za-z])", scaled, value, flags=re.IGNORECASE)
        unit_aliases = {"纳秒": "ns", "微秒": "us", "毫秒": "ms", "秒": "s", "分钟": "min", "小时": "h", "天": "d", "字节": "B"}
        tokens = []
        for token in NUMBER_TOKEN_RE.findall(value):
            token = token.replace(" ", "")
            if token.endswith("KB"):
                token = token[:-2] + "kB"
            if re.fullmatch(r"[vV]\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?", token):
                token = token[1:]
            for localized, canonical in unit_aliases.items():
                if token.endswith(localized):
                    token = token[: -len(localized)] + canonical
                    break
            tokens.append(token)
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
    missing = source_counter - translated_counter
    new_values = set(translated_counter) - set(source_counter)
    if missing or new_values:
        raise ValueError(
            "numbers, versions, or units changed "
            f"source={source_tokens!r} translated={translated_tokens!r}"
        )


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
        (int(level), html.unescape(value))
        for level, value in re.findall(r'<h([1-6])[^>]*\sid="([^"]+)"', document)
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
    for line in front.splitlines():
        match = scalar_re.match(line)
        if not match:
            output.append(line)
            continue
        key = match.group("key")
        raw = match.group("value")
        if key == "categories":
            localized = raw
            for english, chinese in CATEGORY_MAP.items():
                localized = re.sub(rf"\b{english}\b", chinese, localized)
            output.append(f'{match.group("indent")}{key}: {localized}')
            continue
        if key not in TRANSLATABLE_META or not raw or raw in {">", "|"}:
            output.append(line)
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
        if REFERENCE_DEF_RE.match(stripped) or ANCHOR_ONLY_RE.match(stripped):
            verbatim[index] = True
    if fence_marker:
        raise RuntimeError("unterminated Markdown fence")
    if in_comment:
        raise RuntimeError("unterminated HTML comment")
    return verbatim


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
            r"^(?:frontend|backend|listen|defaults|global|fcgi-app|cache|peers|ring|resolvers|userlist|stick-table|table|shards|acl|http-request|http-response|tcp-request|tcp-response|http-check|tcp-check|use_backend|default_backend)\b",
            first_line,
        )
        indented_code = bool(nonblank) and all(
            line.startswith(("    ", "\t"))
            and not re.match(r"^\s*(?:>|[-+*]\s+|\d+[.)]\s+)", line)
            for line in nonblank
        )
        raw_config = bool(config_prefix)
        if first_line.startswith("Usable in:"):
            output.append(re.sub(r"^(\s*)Usable in:", r"\1适用范围：", fragment, count=1))
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
        italic_heading = re.match(r"^(\s*)\*(?!\s)(.+)\*\s*$", content)
        if italic_heading:
            flush()
            translated_italic = translate_scalar_preserving_prefix(
                italic_heading.group(2),
                component=component,
                model=scalar_model,
                cache=cache,
                fallback_model=model,
            )
            output.append(
                f"{italic_heading.group(1)}*{translated_italic}*{newline}"
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
        if not line.strip():
            buffer.append(line)
            flush()
            continue
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
    pattern = re.compile(rf'(?<![A-Za-z0-9_:/])/{re.escape(component)}/')
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
        localized = pattern.sub(f'/zh/{component}/', line)
        localized = re.sub(
            rf"/zh/{re.escape(component)}/(?P<asset>[A-Za-z0-9_./-]+\.(?:png|gif|svg|json|txt))",
            rf"/{component}/\g<asset>",
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
    target_refs = [
        line.replace(f"/zh/{source.relative_to(CONTENT).parts[0]}/", f"/{source.relative_to(CONTENT).parts[0]}/")
        for line in target_body.splitlines()
        if REFERENCE_DEF_RE.match(line)
    ]
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
    target = source.with_name(source.name.removesuffix(".md") + ".zh.md")
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
    root = CONTENT / component
    if requested:
        sources = []
        for value in requested:
            path = Path(value)
            if not path.is_absolute():
                path = PROJECT / path
            path = path.resolve()
            if not path.is_file():
                raise RuntimeError(f"source does not exist: {value}")
            if path.name.endswith(".zh.md") or path.suffix != ".md":
                raise RuntimeError(f"not an English Markdown source: {value}")
            try:
                path.relative_to(root.resolve())
            except ValueError as exc:
                raise RuntimeError(f"source is outside content/{component}: {value}") from exc
            sources.append(path)
        return sorted(set(sources))
    return sorted(
        (path for path in root.rglob("*.md") if not path.name.endswith(".zh.md")),
        key=lambda path: (path.stat().st_size, str(path)),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("component", choices=SUPPORTED_COMPONENTS)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--scalar-model", default=DEFAULT_SCALAR_MODEL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--max-chars", type=int, default=5000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_chars < 500:
        raise RuntimeError("--max-chars must be at least 500")
    sources = discover_sources(args.component, args.paths)
    if args.limit is not None:
        sources = sources[: args.limit]
    cache = Cache.load(args.cache)
    print(
        f"translating {len(sources)} {args.component} files with {args.model}; "
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
