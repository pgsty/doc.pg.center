---
title: "gp_stat_progress_dtx_recovery"
description: "`gp_stat_progress_dtx_recovery` 是一个集群级视图，显示 Postgres 启动期间在后台运行的分布式事务（DTX）恢复进程的进度。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-stat-progress-dtx-recovery.md"
---

如果 Coordinator 重启后长时间处于恢复状态，此视图可能会有所帮助。在所有“未决”事务得到处理之前，Apache Cloudberry 不会接受连接。未决事务是已准备但尚未提交的事务。如果 Coordinator 重启前有大量事务正在运行，数据库恢复可能耗时超出预期，此时可使用此视图监控当前恢复阶段。请注意，在这种情况下，Apache Cloudberry 仍在启动中，因此需要以 utility 模式访问数据库才能查看此视图。

|列|类型|说明|
|------|----|-----------|
|`phase`|text |恢复状态。可能的值为：'initializing'、'recovering commited distributed transactions'、'gathering in-doubt transactions'、'aborting in-doubt transactions'、'gathering in-doubt orphaned transactions' 和 'managing in-doubt orphaned transactions'。|
|`recover_commited_dtx_total`|bigint|发现的需要恢复的已提交事务总数。|
|`recover_commited_dtx_completed`|bigint|已恢复的已提交事务数量。|
| `in_doubt_tx_total`|bigint|发现的未决事务总数，用于启动阶段和非启动阶段。|
|`in_doubt_tx_in_progress`|bigint|正在进行中的未决事务数量。|
|`in_doubt_tx_aborted`|bigint|已中止的未决事务数量。|
