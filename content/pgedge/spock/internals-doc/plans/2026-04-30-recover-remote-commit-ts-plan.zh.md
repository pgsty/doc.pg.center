---
title: "扫描 pg_commit_ts 恢复 remote_commit_ts 的实现计划"
description: "通过扫描 pg_commit_ts 恢复远端提交时间戳。ReconcileResult 仅在本文件内使用，无须修改头文件。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/plans/2026-04-30-recover-remote-commit-ts-plan.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



> **给自动化开发工具的说明**：原计划要求使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans，逐项实现计划。步骤以复选框（`- [ ]`）跟踪。

**目标**：崩溃恢复后，向后扫描 `pg_commit_ts`，恢复每个复制来源最近的 `remote_commit_ts`，使 `spock.progress` 在崩溃后也显示准确值。恢复的 `prev_remote_ts` 还计划用于今后重做的并行应用机制。

**架构**：在 `src/spock_apply.c` 内新增文件作用域的静态函数 `recover_progress_timestamps_from_commit_ts()`。`spock_apply_main` 在 `reconcile_progress_with_origin` 之后、`spock_start_replication` 之前调用它。通过新的 `ReconcileResult` 枚举控制，仅在已加载的 `resource.dat` 过期或缺失时扫描。每个来源观察到 1000 次提交或累计扫描 100 万个 xid 后停止。若 `track_commit_timestamp` 关闭则报错。

**技术栈**：C 语言 PostgreSQL 扩展、PostgreSQL SLRU API（`TransactionIdGetCommitTsData`），以及基于现有 `SpockTest` 模块的 Perl TAP 测试。

**开始前的检查**

```bash
source ~/bin/env17.sh                # activates pg_config / PATH
cd /home/msharp/dev/pgedge7/spock
git status                           # working tree clean
make -j4 install                     # baseline build OK
```

---

## 文件结构 {#file-structure}

| 文件 | 用途 | 改动 |
|---|---|---|
| `src/spock_apply.c` | 应用工作进程的主函数、进度核对及新增恢复函数 | 修改 |
| `tests/tap/t/027_remote_commit_ts_recovery.pl` | 正常恢复路径 | 新建 |
| `tests/tap/t/029_remote_commit_ts_recovery_clean_shutdown.pl` | 验证跳过扫描的路径 | 新建 |
| `tests/tap/t/030_remote_commit_ts_recovery_track_commit_ts_off.pl` | 验证错误路径 | 新建 |
{.wide .expand}

头文件无须修改。`ReconcileResult` 仅在当前文件内使用。

---

## 任务 1：重构 `reconcile_progress_with_origin`，使其返回 `ReconcileResult` {#task-1-refactor-reconcile_progress_with_origin-to-return-reconcileresult}

**先处理此项的原因**：恢复函数需要知道执行了哪个核对分支，以便在文件已同步时跳过扫描。传递枚举只调整结构，不改变行为，可以先完成。

**涉及文件**
- 修改 `src/spock_apply.c`。在前向声明附近（约 245–260 行）添加枚举，在 `src/spock_apply.c:2937-2938` 处修改函数签名，在 `src/spock_apply.c:4216` 处更新调用方。

- [ ] **步骤 1.1：在现有前向声明旁添加枚举**

找到 `src/spock_apply.c:248-257` 的前向声明。

```c
static void UpdateWorkerStats(XLogRecPtr last_received, XLogRecPtr last_inserted);
...
static void request_initial_status_update(PGconn *conn, XLogRecPtr startpos);
static void reconcile_progress_with_origin(XLogRecPtr origin_lsn);
```

将最后一行替换为枚举和更新后的声明。

```c
typedef enum ReconcileResult
{
	RECONCILE_FILE_IN_SYNC,		/* file_lsn == origin_lsn; recovery scan can skip */
	RECONCILE_FILE_STALE,		/* file_lsn <  origin_lsn; recovery scan needed */
	RECONCILE_FILE_ANOMALY,		/* file_lsn >  origin_lsn; recovery scan needed */
	RECONCILE_FILE_ABSENT		/* no entry was loaded; recovery scan needed */
} ReconcileResult;

static ReconcileResult reconcile_progress_with_origin(XLogRecPtr origin_lsn);
```

- [ ] **步骤 1.2：更新函数定义，返回枚举值**

在 `src/spock_apply.c:2937` 处，将以下代码：

```c
static void
reconcile_progress_with_origin(XLogRecPtr origin_lsn)
```

改成：

```c
static ReconcileResult
reconcile_progress_with_origin(XLogRecPtr origin_lsn)
```

在函数体（当前为 `src/spock_apply.c:2944-3043`）中，每个分支都须用 `return` 返回相应枚举值。

- 开头提前返回的分支（`!SpockGroupHash || !SpockCtx`）改为 `return RECONCILE_FILE_ABSENT;`。哈希表尚未建立，按缺失处理。
- 在 `entry == NULL`（哈希表已满）分支，将 `return;` 改成 `return RECONCILE_FILE_ABSENT;`，并保留原有 WARNING。
- 在 `if (!found)` 分支已有的日志之后设置 `result = RECONCILE_FILE_ABSENT;`。
- 在 `else if (entry->progress.remote_commit_lsn == origin_lsn)` 分支设置 `result = RECONCILE_FILE_IN_SYNC;`。
- 在 `else if (entry->progress.remote_commit_lsn < origin_lsn)` 分支设置 `result = RECONCILE_FILE_STALE;`。
- 在最后的 `else`（异常）分支设置 `result = RECONCILE_FILE_ANOMALY;`。

具体做法是在函数开头附近声明 `ReconcileResult result;`，每个分支为它赋值，调用 `LWLockRelease` 后将其返回。

```c
static ReconcileResult
reconcile_progress_with_origin(XLogRecPtr origin_lsn)
{
	SpockGroupKey	key;
	SpockGroupEntry *entry;
	bool			found;
	ReconcileResult	result;

	if (!SpockGroupHash || !SpockCtx)
	{
		elog(WARNING, "SPOCK %s: SpockGroupHash is not initialized; reconcile skipped",
			 MySubscription->name);
		return RECONCILE_FILE_ABSENT;
	}

	key.dbid = MyDatabaseId;
	key.node_id = MySubscription->target->id;
	key.remote_node_id = MySubscription->origin->id;

	LWLockAcquire(SpockCtx->apply_group_master_lock, LW_EXCLUSIVE);

	entry = (SpockGroupEntry *) hash_search(SpockGroupHash, &key,
											HASH_ENTER, &found);
	if (entry == NULL)
	{
		LWLockRelease(SpockCtx->apply_group_master_lock);
		elog(WARNING, "SpockGroupHash is full, cannot reconcile progress for "
			 "(dbid=%u, node_id=%u, remote_node_id=%u)",
			 key.dbid, key.node_id, key.remote_node_id);
		return RECONCILE_FILE_ABSENT;
	}

	if (!found)
	{
		/* ...existing init body unchanged... */
		result = RECONCILE_FILE_ABSENT;
	}
	else if (entry->progress.remote_commit_lsn == origin_lsn)
	{
		/* ...existing body unchanged... */
		result = RECONCILE_FILE_IN_SYNC;
	}
	else if (entry->progress.remote_commit_lsn < origin_lsn)
	{
		/* ...existing stale body unchanged... */
		result = RECONCILE_FILE_STALE;
	}
	else
	{
		/* ...existing anomaly body unchanged... */
		result = RECONCILE_FILE_ANOMALY;
	}

	LWLockRelease(SpockCtx->apply_group_master_lock);
	return result;
}
```

- [ ] **步骤 1.3：让调用方接收结果**

在 `src/spock_apply.c:4216` 处，将以下代码：

```c
reconcile_progress_with_origin(origin_startpos);
```

改成：

```c
ReconcileResult reconcile_result = reconcile_progress_with_origin(origin_startpos);
```

暂时不会使用该变量，到任务 4 才接入。在调用下方加上 `(void) reconcile_result;` 和注释 `/* used in Task 4 */`，以免出现未使用变量警告。

- [ ] **步骤 1.4：构建并检查原有行为**

```bash
make -j4 install
```

预期构建成功，且没有新增警告。

```bash
cd tests/tap && ./run_tests.sh t/022_rmgr_progress_post_checkpoint_crash.pl
```

预期全部子测试通过。这项测试对进度核对路径的覆盖最充分。

- [ ] **步骤 1.5：提交**

```bash
git add src/spock_apply.c
git commit -m "refactor: reconcile_progress_with_origin returns ReconcileResult

Threads a typed result back to the caller so a follow-up commit can
gate post-reconcile work on whether the loaded resource.dat was in
sync, stale, anomalous, or absent. Pure refactor -- no behavior
change."
```

---

## 任务 2：添加恢复常量 {#task-2-add-the-recovery-constants}

**涉及文件**
- 修改 `src/spock_apply.c`，在文件顶部的已有宏或包含指令之后加入 `#define`。

- [ ] **步骤 2.1：添加三个 `#define`**

在 `src/spock_apply.c` 顶部选定位置，放在包含指令之后。有应用端相关 `#define` 时放在其附近，否则放在前向声明之前。添加以下代码。

```c
/*
 * Constants governing the post-crash scan of pg_commit_ts that recovers
 * remote_commit_ts per origin. Plain #defines for now; convert to GUCs
 * only if a deployment ever needs to tune them.
 */
#define SPOCK_TS_RECOVERY_MIN_SEEN_PER_ORIGIN	1000
#define SPOCK_TS_RECOVERY_SCAN_LIMIT			1000000
#define SPOCK_TS_RECOVERY_BATCH_SIZE			1000
```

- [ ] **步骤 2.2：构建验证**

```bash
make -j4 install
```

预期构建成功。宏已定义，此时尚无使用位置。

- [ ] **步骤 2.3：提交**

```bash
git add src/spock_apply.c
git commit -m "feat: add SPOCK_TS_RECOVERY_* constants for commit_ts scan

Adds the three tunables (min commits per origin, hard scan limit,
batch size) for the upcoming pg_commit_ts recovery scan. Defined as
plain #defines; conversion to GUCs is a follow-up if profiling
motivates tuning."
```

---

## 任务 3：编写预期先失败的正常恢复测试（027） {#task-3-write-the-failing-happy-path-test-027}

**先写测试的原因**：明确回归目标。在 `main` 分支或完成任务 2 后运行必须失败，完成任务 4 后必须通过。

**涉及文件**
- 新建 `tests/tap/t/027_remote_commit_ts_recovery.pl`。

- [ ] **步骤 3.1：创建测试文件**

将以下内容写入 `tests/tap/t/027_remote_commit_ts_recovery.pl`。

```perl
#!/usr/bin/perl
# =============================================================================
# Test: 027_remote_commit_ts_recovery.pl
#       Verify that after a crash, remote_commit_ts is recovered from the
#       subscriber's pg_commit_ts SLRU rather than left NULL. The recovered
#       values are also intended to be useful for the planned parallel-apply
#       rework.
#
# Topology:  n1 (provider) -> n2 (subscriber)
#
# Sequence:
#   1. Apply commits, clean restart (writes resource.dat).
#   2. Apply more commits (origin advances; resource.dat stale).
#   3. SIGKILL subscriber.
#   4. Restart. Apply worker reconcile detects stale, calls the new
#      recover_progress_timestamps_from_commit_ts which scans pg_commit_ts
#      backward and populates remote_commit_ts.
#   5. Assert remote_commit_ts is NOT NULL.
# =============================================================================

use strict;
use warnings;
use Test::More;
use lib '.';
use SpockTest qw(
    create_cluster destroy_cluster system_or_bail
    command_ok get_test_config scalar_query psql_or_bail
    wait_for_sub_status wait_for_pg_ready
);

sub wait_until {
    my ($timeout_s, $probe) = @_;
    my $deadline = time() + $timeout_s;
    while (time() < $deadline) {
        return 1 if $probe->();
        select(undef, undef, undef, 0.25);
    }
    return 0;
}

create_cluster(2, 'Create 2-node cluster');

my $conf      = get_test_config();
my $host      = $conf->{host};
my $pg_bin    = $conf->{pg_bin};
my $ports     = $conf->{node_ports};
my $datadirs  = $conf->{node_datadirs};
my $dbname    = $conf->{db_name};
my $user      = $conf->{db_user};

my $prov_port = $ports->[0];
my $sub_port  = $ports->[1];
my $sub_dir   = $datadirs->[1];

my $prov_dsn = "host=$host port=$prov_port dbname=$dbname user=$user";

psql_or_bail(1, "CREATE TABLE public.ts_recovery (id int primary key, val text)");
psql_or_bail(2, "CREATE TABLE public.ts_recovery (id int primary key, val text)");

psql_or_bail(2, "SELECT spock.sub_create('test_sub', '$prov_dsn', ARRAY['default'], false, false)");
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'subscription is replicating');

# --- Round 1: apply, clean restart so resource.dat is written. ---
psql_or_bail(1, "INSERT INTO public.ts_recovery SELECT g, 'r1_' || g FROM generate_series(1,50) g");
ok(wait_until(30, sub { scalar_query(2, "SELECT count(*) FROM public.ts_recovery") eq '50' }),
   'round-1 50 rows replicated');

system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-m', 'fast', 'stop';
ok(-f "$sub_dir/spock/resource.dat", 'resource.dat written on clean stop');

system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-o', "-p $sub_port", '-w', 'start';
ok(wait_for_pg_ready($host, $sub_port, $pg_bin, 30), 'subscriber back up');
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'replicating after clean restart');

# --- Round 2: apply more so origin advances past resource.dat's snapshot. ---
psql_or_bail(1, "INSERT INTO public.ts_recovery SELECT g, 'r2_' || g FROM generate_series(51,100) g");
ok(wait_until(30, sub { scalar_query(2, "SELECT count(*) FROM public.ts_recovery") eq '100' }),
   'round-2 50 rows replicated');

# Confirm remote_commit_ts is non-NULL pre-crash (sanity).
my $pre_ts = scalar_query(2, "SELECT remote_commit_ts::text FROM spock.progress LIMIT 1");
ok($pre_ts ne '', "pre-crash remote_commit_ts populated: $pre_ts");

# --- SIGKILL subscriber. ---
my $pid_file = "$sub_dir/postmaster.pid";
open(my $fh, '<', $pid_file) or die "Cannot open $pid_file: $!";
my $sub_pid = <$fh>;
chomp($sub_pid);
close($fh);
kill 'KILL', $sub_pid;
pass('subscriber SIGKILLed');

select(undef, undef, undef, 2.0);

# --- Restart. Reconcile detects stale; recovery scan populates remote_commit_ts. ---
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-o', "-p $sub_port", '-w', 'start';
ok(wait_for_pg_ready($host, $sub_port, $pg_bin, 30), 'subscriber accepting connections after crash');

# Wait for the apply worker to start, run reconcile, run recovery scan.
ok(wait_until(30, sub {
    my $ts = scalar_query(2, q{
        SELECT remote_commit_ts::text FROM spock.progress LIMIT 1
    });
    defined $ts && $ts ne '' && $ts ne '0/0'
}), 'spock.progress.remote_commit_ts populated by recovery scan');

# --- Assertions ---
my $post_ts = scalar_query(2, "SELECT remote_commit_ts::text FROM spock.progress LIMIT 1");
ok($post_ts ne '',
   "post-crash remote_commit_ts is NOT NULL (recovered via pg_commit_ts scan): $post_ts");

# remote_commit_ts must be a valid timestamp (parses as such).
my $ts_valid = scalar_query(2,
    "SELECT '$post_ts'::timestamptz IS NOT NULL");
is($ts_valid, 't', "post-crash remote_commit_ts parses as a valid timestamptz");

psql_or_bail(2, "SELECT spock.sub_drop('test_sub')");
destroy_cluster('Destroy 2-node cluster');
done_testing();
```

赋予文件可执行权限。

```bash
chmod +x tests/tap/t/027_remote_commit_ts_recovery.pl
```

- [ ] **步骤 3.2：运行测试并确认按预期失败**

```bash
cd tests/tap && ./run_tests.sh t/027_remote_commit_ts_recovery.pl
```

预期「post-crash remote_commit_ts is NOT NULL」断言失败。在当前行为下，没有恢复扫描，崩溃后该字段仍为 NULL。

- [ ] **步骤 3.3：提交**

```bash
git add tests/tap/t/027_remote_commit_ts_recovery.pl
git commit -m "test: add 027 (remote_commit_ts post-crash recovery, currently failing)

Asserts the regression target for the pg_commit_ts scan: after a crash
that leaves resource.dat stale relative to the replication origin,
remote_commit_ts must be recovered (non-NULL) rather than left blank.
Currently fails -- implementation lands in the next commit."
```

---

## 任务 4：实现扫描并接入调用点 {#task-4-implement-the-scan-and-wire-the-call-site}

**涉及文件**
- 修改 `src/spock_apply.c`，新增 `recover_progress_timestamps_from_commit_ts`，由 `spock_apply_main` 调用，并添加 INFO 日志。

- [ ] **步骤 4.1：添加前向声明**

在已有前向声明附近（`src/spock_apply.c:248-260`，即任务 1 添加 `ReconcileResult` 的位置）加上：

```c
static void recover_progress_timestamps_from_commit_ts(SpockGroupEntry *entry,
													   RepOriginId target_origin);
```

- [ ] **步骤 4.2：包含 `commit_ts.h`**

在 `src/spock_apply.c` 顶部的 `#include` 区域添加：

```c
#include "access/commit_ts.h"
```

- [ ] **步骤 4.3：实现扫描函数**

在 `reconcile_progress_with_origin` 之后添加函数，即当前结束于 `src/spock_apply.c:3043` 的代码段之后。

```c
/*
 * recover_progress_timestamps_from_commit_ts
 *
 * After reconcile detects that resource.dat is stale (or absent) for this
 * origin, scan pg_commit_ts backward from the latest xid to recover the
 * most-recent remote_commit_ts for this origin. The recovered values are
 * also intended to be useful for the planned parallel-apply rework.
 *
 * Termination: stop after observing SPOCK_TS_RECOVERY_MIN_SEEN_PER_ORIGIN
 * commits for this origin (any older commit is guaranteed to have a smaller
 * commit_ts under realistic concurrency widths) or after scanning
 * SPOCK_TS_RECOVERY_SCAN_LIMIT total xids.
 *
 * Caller must have ensured the entry exists in SpockGroupHash (reconcile
 * does this).
 */
static void
recover_progress_timestamps_from_commit_ts(SpockGroupEntry *entry,
										   RepOriginId target_origin)
{
	TransactionId	xid_high;
	TimestampTz		running_max_ts = 0;
	int				seen_count = 0;
	int64			total_scanned = 0;

	xid_high = ReadNextTransactionId();
	if (TransactionIdPrecedes(xid_high, FirstNormalTransactionId + 1))
	{
		elog(LOG, "SPOCK %s: ts recovery: no normal transactions yet; skipping",
			 MySubscription->name);
		return;
	}
	xid_high = xid_high - 1;

	while (seen_count < SPOCK_TS_RECOVERY_MIN_SEEN_PER_ORIGIN
		   && total_scanned < SPOCK_TS_RECOVERY_SCAN_LIMIT)
	{
		TransactionId	xid_low;
		TransactionId	xid;
		int64			batch_count;

		CHECK_FOR_INTERRUPTS();

		/* Compute batch lower bound, clamped at FirstNormalTransactionId. */
		if (TransactionIdPrecedes(xid_high,
								  FirstNormalTransactionId + SPOCK_TS_RECOVERY_BATCH_SIZE))
			xid_low = FirstNormalTransactionId;
		else
			xid_low = xid_high - SPOCK_TS_RECOVERY_BATCH_SIZE + 1;

		batch_count = (int64) xid_high - (int64) xid_low + 1;

		for (xid = xid_low; TransactionIdPrecedes(xid, xid_high + 1); xid++)
		{
			TimestampTz		ts;
			RepOriginId		origin;

			if (!TransactionIdGetCommitTsData(xid, &ts, &origin))
				continue;					/* aborted, vacuumed, or no commit_ts */
			if (origin != target_origin)
				continue;					/* local writes / other origins */

			seen_count++;
			if (ts > running_max_ts)
				running_max_ts = ts;
		}

		total_scanned += batch_count;

		if (xid_low == FirstNormalTransactionId)
			break;						/* wraparound floor */

		xid_high = xid_low - 1;
	}

	if (running_max_ts > 0)
	{
		LWLockAcquire(SpockCtx->apply_group_master_lock, LW_EXCLUSIVE);
		if (entry->progress.remote_commit_ts < running_max_ts)
		{
			entry->progress.remote_commit_ts = running_max_ts;
			entry->progress.prev_remote_ts = running_max_ts;
		}
		LWLockRelease(SpockCtx->apply_group_master_lock);

		elog(INFO, "SPOCK %s: ts recovery: scanned %lld xids, found %d commits, "
			 "recovered remote_commit_ts",
			 MySubscription->name, (long long) total_scanned, seen_count);
	}
	else
	{
		elog(WARNING, "SPOCK %s: ts recovery: scanned %lld xids, no commits found "
			 "for origin %u; remote_commit_ts remains NULL until next applied commit",
			 MySubscription->name, (long long) total_scanned, target_origin);
	}
}
```

- [ ] **步骤 4.4：在 `spock_apply_main` 中接入调用**

在 `src/spock_apply.c:4216` 处（任务 1 引入 `reconcile_result` 的位置），将以下代码：

```c
ReconcileResult reconcile_result = reconcile_progress_with_origin(origin_startpos);
(void) reconcile_result;	/* used in Task 4 */
```

替换为：

```c
ReconcileResult reconcile_result = reconcile_progress_with_origin(origin_startpos);

if (reconcile_result == RECONCILE_FILE_IN_SYNC)
{
	elog(INFO, "SPOCK %s: ts recovery: file in sync with origin, skipping scan",
		 MySubscription->name);
}
else
{
	SpockGroupKey		key;
	SpockGroupEntry	   *entry;
	bool				found;
	RepOriginId			target_origin = replorigin_session_origin;

	key.dbid = MyDatabaseId;
	key.node_id = MySubscription->target->id;
	key.remote_node_id = MySubscription->origin->id;

	LWLockAcquire(SpockCtx->apply_group_master_lock, LW_SHARED);
	entry = (SpockGroupEntry *) hash_search(SpockGroupHash, &key,
											HASH_FIND, &found);
	LWLockRelease(SpockCtx->apply_group_master_lock);

	if (entry != NULL)
		recover_progress_timestamps_from_commit_ts(entry, target_origin);
}
```

关于 `target_origin`：`replorigin_session_origin` 是 PostgreSQL 的标准全局变量，在 `src/spock_apply.c:4212` 处由 `replorigin_session_setup(originid)` 设置，位置在核对调用之前两行。它正是过滤所需的 `RepOriginId`。

- [ ] **步骤 4.5：构建并运行测试 027**

```bash
make -j4 install
cd tests/tap && ./run_tests.sh t/027_remote_commit_ts_recovery.pl
```

预期全部子测试通过，「post-crash remote_commit_ts is NOT NULL」断言现在应当成立。

- [ ] **步骤 4.6：运行已有的崩溃恢复回归测试**

```bash
./run_tests.sh t/022_rmgr_progress_post_checkpoint_crash.pl t/008_rmgr.pl
```

两项测试最终都应通过。注意，022 中的断言 `is($post_commit_ts, '', "remote_commit_ts is NULL post-crash...")` 已不符合新行为，因为恢复过程会填入该字段。**须在本任务中同步更新 022。**

- [ ] **步骤 4.7：更新测试 022 以反映新行为**

在 `tests/tap/t/022_rmgr_progress_post_checkpoint_crash.pl` 中找到断言（约 191–197 行），将以下代码：

```perl
my $post_commit_ts = scalar_query(2, q{
    SELECT remote_commit_ts::text FROM spock.progress LIMIT 1
});
is($post_commit_ts, '',
   "remote_commit_ts is NULL post-crash (reconcile cleared stale ts)");

diag("post-crash: remote_commit_lsn=$post_commit_lsn remote_commit_ts='$post_commit_ts' (expected NULL)");
```

改成：

```perl
my $post_commit_ts = scalar_query(2, q{
    SELECT remote_commit_ts::text FROM spock.progress LIMIT 1
});
ok($post_commit_ts ne '',
   "remote_commit_ts is NOT NULL post-crash (recovered via pg_commit_ts scan)");

diag("post-crash: remote_commit_lsn=$post_commit_lsn remote_commit_ts='$post_commit_ts'");
```

文件头部注释中的 `remote_commit_ts is NULL post-crash` 也须改为恢复后的行为。

- [ ] **步骤 4.8：重新运行 022 核实修改**

```bash
./run_tests.sh t/022_rmgr_progress_post_checkpoint_crash.pl
```

预期全部子测试通过。

- [ ] **步骤 4.9：提交**

```bash
git add src/spock_apply.c tests/tap/t/022_rmgr_progress_post_checkpoint_crash.pl
git commit -m "feat: recover remote_commit_ts via pg_commit_ts scan on crash restart

After reconcile_progress_with_origin detects that resource.dat is stale
or absent for an origin, scan pg_commit_ts backward from the latest xid
and populate remote_commit_ts with the max ts found for this origin.
The recovered values are also intended to be useful for the planned
parallel-apply rework.

Termination: 1000 commits seen for this origin (concurrency width is
bounded well below this by max_connections / poolers) or 1M xids total.
Logs INFO on completion (skip path or run path) so startup behavior is
grep-able.

Updates test 022 to reflect that remote_commit_ts is now recovered
rather than NULL after crash."
```

---

## 任务 5：编写关闭 `track_commit_timestamp` 时预期先失败的测试（030） {#task-5-write-the-failing-track_commit_timestamp-off-test-030}

**涉及文件**
- 新建 `tests/tap/t/030_remote_commit_ts_recovery_track_commit_ts_off.pl`。

- [ ] **步骤 5.1：创建测试**

将以下内容写入 `tests/tap/t/030_remote_commit_ts_recovery_track_commit_ts_off.pl`。

```perl
#!/usr/bin/perl
# =============================================================================
# Test: 030_remote_commit_ts_recovery_track_commit_ts_off.pl
#       Verify that the apply worker errors out at startup if
#       track_commit_timestamp is off and the recovery scan would otherwise
#       run (i.e., resource.dat is stale or absent). Spock requires
#       track_commit_timestamp = on for conflict resolution; making the
#       failure mode loud at apply-worker start is intentional.
# =============================================================================

use strict;
use warnings;
use Test::More;
use lib '.';
use SpockTest qw(
    create_cluster destroy_cluster system_or_bail
    command_ok get_test_config scalar_query psql_or_bail
    wait_for_sub_status wait_for_pg_ready
);

sub wait_until {
    my ($timeout_s, $probe) = @_;
    my $deadline = time() + $timeout_s;
    while (time() < $deadline) {
        return 1 if $probe->();
        select(undef, undef, undef, 0.25);
    }
    return 0;
}

sub log_contains {
    my ($logfile, $pattern) = @_;
    return 0 unless -f $logfile;
    open(my $fh, '<', $logfile) or return 0;
    while (my $line = <$fh>) {
        return 1 if $line =~ /$pattern/;
    }
    close($fh);
    return 0;
}

create_cluster(2, 'Create 2-node cluster');

my $conf      = get_test_config();
my $host      = $conf->{host};
my $pg_bin    = $conf->{pg_bin};
my $ports     = $conf->{node_ports};
my $datadirs  = $conf->{node_datadirs};
my $dbname    = $conf->{db_name};
my $user      = $conf->{db_user};

my $prov_port = $ports->[0];
my $sub_port  = $ports->[1];
my $sub_dir   = $datadirs->[1];

my $prov_dsn = "host=$host port=$prov_port dbname=$dbname user=$user";

psql_or_bail(1, "CREATE TABLE public.ts_off (id int primary key, val text)");
psql_or_bail(2, "CREATE TABLE public.ts_off (id int primary key, val text)");

psql_or_bail(2, "SELECT spock.sub_create('test_sub', '$prov_dsn', ARRAY['default'], false, false)");
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'subscription is replicating');

psql_or_bail(1, "INSERT INTO public.ts_off SELECT g, 'r1_' || g FROM generate_series(1,50) g");
ok(wait_until(30, sub { scalar_query(2, "SELECT count(*) FROM public.ts_off") eq '50' }),
   '50 rows replicated');

# Clean restart so resource.dat is current.
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-m', 'fast', 'stop';
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-o', "-p $sub_port", '-w', 'start';
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'replicating after clean restart');

# Apply more so resource.dat goes stale.
psql_or_bail(1, "INSERT INTO public.ts_off SELECT g, 'r2_' || g FROM generate_series(51,100) g");
ok(wait_until(30, sub { scalar_query(2, "SELECT count(*) FROM public.ts_off") eq '100' }),
   '100 rows replicated');

# Disable track_commit_timestamp -- requires a postmaster restart, but our
# next step is going to crash and restart anyway.
psql_or_bail(2, "ALTER SYSTEM SET track_commit_timestamp = off");

# SIGKILL.
my $pid_file = "$sub_dir/postmaster.pid";
open(my $fh, '<', $pid_file) or die "Cannot open $pid_file: $!";
my $sub_pid = <$fh>;
chomp($sub_pid);
close($fh);
kill 'KILL', $sub_pid;
pass('subscriber SIGKILLed');

select(undef, undef, undef, 2.0);

# Restart -- track_commit_timestamp is now off; reconcile sees stale file;
# recovery scan must error out.
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-o', "-p $sub_port", '-w', 'start';
ok(wait_for_pg_ready($host, $sub_port, $pg_bin, 30), 'subscriber back up');

# Wait for the apply worker to attempt start, then check the log for the
# expected ERROR. The bgworker manager will respawn it; we just need to
# verify the message appears.
my $logfile = "$sub_dir/log/postgresql-1.log";
# SpockTest may put logs elsewhere; adjust path if needed by reading test
# config or scanning $sub_dir/log/.
ok(wait_until(30, sub {
    log_contains($logfile, qr/track_commit_timestamp.*on/i)
}), "apply worker logged ERROR about track_commit_timestamp being off");

# Restore for cleanup.
psql_or_bail(2, "ALTER SYSTEM SET track_commit_timestamp = on");
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-m', 'fast', 'restart';

destroy_cluster('Destroy 2-node cluster');
done_testing();
```

注意，日志路径取决于 `SpockTest` 如何配置 `log_directory` 和 `log_filename`，可能需要调整。如果 `$sub_dir/log/postgresql-1.log` 与实际路径不符，请检查 `tests/tap/SpockTest.pm`。错误消息采用宽松匹配，不区分大小写，只要求「track_commit_timestamp」附近出现「on」。

```bash
chmod +x tests/tap/t/030_remote_commit_ts_recovery_track_commit_ts_off.pl
```

- [ ] **步骤 5.2：运行测试并确认按预期失败**

```bash
./run_tests.sh t/030_remote_commit_ts_recovery_track_commit_ts_off.pl
```

预期「logged ERROR about track_commit_timestamp」检查失败，因为任务 4 尚未检查该参数。没有这项检查时，恢复扫描调用 `TransactionIdGetCommitTsData`，对于每个 xid 都会得到 false（没有 commit_ts 数据），因而记录「no commits found」而不会报错。

- [ ] **步骤 5.3：提交**

```bash
git add tests/tap/t/030_remote_commit_ts_recovery_track_commit_ts_off.pl
git commit -m "test: add 030 (track_commit_timestamp off, currently failing)

Asserts the apply worker errors at startup if track_commit_timestamp
is off when the recovery scan would otherwise run. Currently fails --
guard lands in the next commit."
```

---

## 任务 6：增加 `track_commit_timestamp` 检查 {#task-6-add-the-track_commit_timestamp-guard}

**涉及文件**
- 修改 `src/spock_apply.c`，在 `recover_progress_timestamps_from_commit_ts` 开头检查该配置。

- [ ] **步骤 6.1：添加检查**

在任务 4.3 添加的 `recover_progress_timestamps_from_commit_ts` 开头，紧接变量声明插入：

```c
if (!track_commit_timestamps)
	ereport(ERROR,
			(errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
			 errmsg("SPOCK %s: track_commit_timestamp must be on for spock.progress recovery",
					MySubscription->name),
			 errhint("Set track_commit_timestamp = on in postgresql.conf and restart.")));
```

`track_commit_timestamps`（注意复数词尾）是 PostgreSQL 的标准 GUC 全局变量，声明于 `access/commit_ts.h`，任务 4.2 已包含此文件。

- [ ] **步骤 6.2：构建**

```bash
make -j4 install
```

预期构建成功。

- [ ] **步骤 6.3：运行测试 030，此时应通过**

```bash
./run_tests.sh t/030_remote_commit_ts_recovery_track_commit_ts_off.pl
```

预期全部子测试通过。

- [ ] **步骤 6.4：运行测试 027，确认原有行为正常**

```bash
./run_tests.sh t/027_remote_commit_ts_recovery.pl
```

预期全部子测试通过。

- [ ] **步骤 6.5：提交**

```bash
git add src/spock_apply.c
git commit -m "feat: error if track_commit_timestamp is off during ts recovery

Spock already requires track_commit_timestamp = on for conflict
resolution. Making the failure mode loud at apply-worker start (rather
than silently returning a degraded NULL state) is consistent with that
existing requirement and catches misconfiguration early."
```

---

## 任务 7：添加正常关闭后跳过扫描的测试（029） {#task-7-add-the-clean-shutdown-skip-path-test-029}

**涉及文件**
- 新建 `tests/tap/t/029_remote_commit_ts_recovery_clean_shutdown.pl`。

- [ ] **步骤 7.1：创建测试**

将以下内容写入 `tests/tap/t/029_remote_commit_ts_recovery_clean_shutdown.pl`。

```perl
#!/usr/bin/perl
# =============================================================================
# Test: 029_remote_commit_ts_recovery_clean_shutdown.pl
#       Verify that on a CLEAN restart (resource.dat in sync with origin),
#       the recovery scan is SKIPPED and the loaded remote_commit_ts is
#       preserved. Confirmed by checking the apply-worker INFO log for the
#       "file in sync, skipping scan" line.
# =============================================================================

use strict;
use warnings;
use Test::More;
use lib '.';
use SpockTest qw(
    create_cluster destroy_cluster system_or_bail
    command_ok get_test_config scalar_query psql_or_bail
    wait_for_sub_status wait_for_pg_ready
);

sub wait_until {
    my ($timeout_s, $probe) = @_;
    my $deadline = time() + $timeout_s;
    while (time() < $deadline) {
        return 1 if $probe->();
        select(undef, undef, undef, 0.25);
    }
    return 0;
}

sub log_grep_count {
    my ($logfile, $pattern) = @_;
    return 0 unless -f $logfile;
    open(my $fh, '<', $logfile) or return 0;
    my $count = 0;
    while (my $line = <$fh>) {
        $count++ if $line =~ /$pattern/;
    }
    close($fh);
    return $count;
}

create_cluster(2, 'Create 2-node cluster');

my $conf      = get_test_config();
my $host      = $conf->{host};
my $pg_bin    = $conf->{pg_bin};
my $ports     = $conf->{node_ports};
my $datadirs  = $conf->{node_datadirs};
my $dbname    = $conf->{db_name};
my $user      = $conf->{db_user};

my $prov_port = $ports->[0];
my $sub_port  = $ports->[1];
my $sub_dir   = $datadirs->[1];

my $prov_dsn = "host=$host port=$prov_port dbname=$dbname user=$user";

psql_or_bail(1, "CREATE TABLE public.ts_clean (id int primary key, val text)");
psql_or_bail(2, "CREATE TABLE public.ts_clean (id int primary key, val text)");

psql_or_bail(2, "SELECT spock.sub_create('test_sub', '$prov_dsn', ARRAY['default'], false, false)");
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'subscription is replicating');

psql_or_bail(1, "INSERT INTO public.ts_clean SELECT g, 'r_' || g FROM generate_series(1,50) g");
ok(wait_until(30, sub { scalar_query(2, "SELECT count(*) FROM public.ts_clean") eq '50' }),
   '50 rows replicated');

# Capture pre-shutdown ts.
my $pre_ts = scalar_query(2, "SELECT remote_commit_ts::text FROM spock.progress LIMIT 1");
ok($pre_ts ne '', "pre-shutdown remote_commit_ts: $pre_ts");

# Establish baseline: count "skipping scan" log lines before restart.
my $logfile = "$sub_dir/log/postgresql-1.log";
my $skip_before = log_grep_count($logfile, qr/ts recovery: file in sync, skipping scan/);

# CLEAN shutdown + restart. resource.dat should match origin LSN.
system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-m', 'fast', 'stop';
ok(-f "$sub_dir/spock/resource.dat", 'resource.dat written on clean stop');

system_or_bail "$pg_bin/pg_ctl", '-D', $sub_dir, '-o', "-p $sub_port", '-w', 'start';
ok(wait_for_pg_ready($host, $sub_port, $pg_bin, 30), 'subscriber back up');
ok(wait_for_sub_status(2, 'test_sub', 'replicating', 30), 'replicating after clean restart');

# Wait for the new "skipping scan" log line.
ok(wait_until(15, sub {
    log_grep_count($logfile, qr/ts recovery: file in sync, skipping scan/) > $skip_before
}), 'apply worker logged "file in sync, skipping scan" on clean restart');

# Confirm scan was NOT run (no "scanned ... xids" line for this restart).
my $scan_run = log_grep_count($logfile, qr/ts recovery: scanned \d+ xids/);
# We only count NEW occurrences relative to baseline, but since baseline is 0
# for a fresh cluster, any positive count would indicate the scan ran.
# Capture before/after to be precise:
# (For simplicity, this test asserts the skip log appeared. A run log alongside
#  it would also appear, indicating the skip path was NOT taken; the assertion
#  below covers that case.)
is(log_grep_count($logfile, qr/ts recovery: scanned \d+ xids.*recovered remote_commit_ts/),
   0,
   'scan did NOT run on clean restart (no "recovered remote_commit_ts" log line)');

# remote_commit_ts should still match pre-shutdown.
my $post_ts = scalar_query(2, "SELECT remote_commit_ts::text FROM spock.progress LIMIT 1");
is($post_ts, $pre_ts, "remote_commit_ts preserved across clean restart");

psql_or_bail(2, "SELECT spock.sub_drop('test_sub')");
destroy_cluster('Destroy 2-node cluster');
done_testing();
```

```bash
chmod +x tests/tap/t/029_remote_commit_ts_recovery_clean_shutdown.pl
```

- [ ] **步骤 7.2：运行测试**

```bash
./run_tests.sh t/029_remote_commit_ts_recovery_clean_shutdown.pl
```

预期全部子测试通过。任务 4 已添加跳过扫描的 INFO 日志，且遇到 `RECONCILE_FILE_IN_SYNC` 会跳过恢复函数，此时两个条件均已具备。

- [ ] **步骤 7.3：提交**

```bash
git add tests/tap/t/029_remote_commit_ts_recovery_clean_shutdown.pl
git commit -m "test: add 029 (clean-shutdown skip path for ts recovery)

Verifies that on a clean restart, when resource.dat matches the origin
LSN, the recovery scan is skipped and the loaded remote_commit_ts is
preserved. Asserted via the INFO log line and absence of any 'scanned
xids' line for the restart."
```

---

## 任务 8：最终回归测试 {#task-8-final-regression-sweep}

- [ ] **步骤 8.1：运行完整 TAP 测试集**

```bash
cd tests/tap && ./run_tests.sh
```

预期全部测试通过，包括 008、022、023、026 和三个新增测试（027、029、030）。

- [ ] **步骤 8.2：核对提交历史**

```bash
git log --oneline main..HEAD | head -20
```

预期为清晰的线性提交顺序：重构、常量、测试 027（此时失败）、实现、测试 030（此时失败）、参数检查、测试 029。

- [ ] **步骤 8.3：工作完成，无须再提交。**

若以 PR 交付，是否纳入设计文档由用户决定。编写本计划时，该文档尚在工作树中，未提交。

---

## 计划自查 {#self-review}

- **规格覆盖**：枚举与跳过扫描对应任务 1 和 4，常量对应任务 2，扫描逻辑对应任务 4，`track_commit_timestamp` 检查对应任务 6，INFO 日志对应任务 4 和 7，测试 027、029、030 分别对应任务 3、7、5。按规格讨论，暂缓测试 028（空闲或空集群）。要在 TAP 中触发「no commits found」，须覆盖常量或产生超过 100 万个无关 xid，对第一版都过于繁重。
- **类型一致性**：任务 1 的 `ReconcileResult` 枚举在任务 4 的调用点使用。`target_origin` 是 `RepOriginId`，`running_max_ts` 是 `TimestampTz`；通过 `(int64) total_scanned` 强制转换，常量可安全地按 `int64` 运算。
- **占位内容检查**：每一步都有可执行代码或命令。只有测试 029、030 的日志路径可能因环境而异，注释已说明默认路径不匹配时应核对 `SpockTest.pm`。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/plans/2026-04-30-recover-remote-commit-ts-plan.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
