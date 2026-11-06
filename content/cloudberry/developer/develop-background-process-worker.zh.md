---
title: "开发后台工作进程"
description: "可以扩展 Apache Cloudberry，使其在独立进程中运行用户提供的代码。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/develop-background-process-worker.md"
---

这些进程由 `postgres` 启动、停止和监控，因此其生命周期可以与服务器状态紧密关联。这些进程可以选择附加到 Apache Cloudberry 的共享内存区域，并从内部连接数据库；它们还可以像普通的客户端连接服务器进程一样，串行运行多个事务。通过链接 `libpq`，它们也可以连接服务器，像普通客户端应用程序一样运行。

> [!WARNING]
> 使用后台工作进程存在相当大的健壮性和安全风险，因为这些进程以 `C` 语言编写，可以不受限制地访问数据。管理员在启用包含后台工作进程的模块时应极为谨慎。只有经过仔细审计的模块才应获准运行后台工作进程。

将模块名加入服务器配置参数 shared\_preload\_libraries，即可在 Apache Cloudberry 启动时初始化后台工作进程。需要运行后台工作进程的模块可以在其 `_PG_init()` 中调用 `RegisterBackgroundWorker(BackgroundWorker *worker)` 来注册该进程。也可以在系统启动并运行后，通过调用 `RegisterDynamicBackgroundWorker(BackgroundWorker *worker, BackgroundWorkerHandle **handle)` 函数启动后台工作进程。`RegisterBackgroundWorker` 只能从 `postmaster` 内部调用，而 `RegisterDynamicBackgroundWorker` 必须从普通后端调用。

`BackgroundWorker` 结构定义如下：

```c
typedef void (*bgworker_main_type)(Datum main_arg);
typedef struct BackgroundWorker
{
    char        bgw_name[BGW_MAXLEN];
    int         bgw_flags;
    BgWorkerStartTime bgw_start_time;
    int         bgw_restart_time;       /* in seconds, or BGW_NEVER_RESTART */
    bgworker_main_type bgw_main;
    char        bgw_library_name[BGW_MAXLEN];   /* only if bgw_main is NULL */
    char        bgw_function_name[BGW_MAXLEN];  /* only if bgw_main is NULL */
    Datum       bgw_main_arg;
    int         bgw_notify_pid;
} BackgroundWorker;
```

`bgw_name` 是用于日志消息、进程列表和类似场景的字符串。

`bgw_flags` 是通过按位或运算组合的位掩码，表示模块所需的能力。可用值为 `BGWORKER_SHMEM_ACCESS`（请求访问共享内存）和 `BGWORKER_BACKEND_DATABASE_CONNECTION`（请求建立数据库连接，以便随后通过该连接运行事务和查询）。使用 `BGWORKER_BACKEND_DATABASE_CONNECTION` 连接数据库的后台工作进程还必须使用 `BGWORKER_SHMEM_ACCESS` 附加共享内存，否则工作进程将无法启动。

`bgw_start_time` 表示 `postgres` 应在服务器处于何种状态时启动该进程，可以是以下值之一：`BgWorkerStart_PostmasterStart`（在 `postgres` 完成自身初始化后立即启动；请求此状态的进程不能连接数据库）、`BgWorkerStart_ConsistentState`（在热备服务器达到一致状态后立即启动，允许进程连接数据库并运行只读查询）或 `BgWorkerStart_RecoveryFinished`（在系统进入正常读写状态后立即启动）。请注意，对于非热备服务器，后两个值是等效的。此设置只指示何时启动进程；服务器进入其他状态时，这些进程不会停止。

`bgw_restart_time` 是进程崩溃后，`postgres` 在重启该进程之前应等待的时间间隔，单位为秒。它可以是任意正值，也可以是 `BGW_NEVER_RESTART`，后者表示进程崩溃后不重启。

`bgw_main` 是指向进程启动时要运行的函数的指针。该函数必须接受一个 `Datum` 类型的参数，并返回 `void`。`bgw_main_arg` 将作为唯一的参数传给该函数。请注意，全局变量 `MyBgworkerEntry` 指向注册时传入的 `BackgroundWorker` 结构的一个副本。`bgw_main` 可以为 NULL；此时将使用 `bgw_library_name` 和 `bgw_function_name` 确定入口点。这适用于在 postmaster 启动后才启动的后台工作进程，因为此时 postmaster 尚未加载所需的库。

`bgw_library_name` 是用于查找后台工作进程初始入口点的库名。除非 `bgw_main` 为 NULL，否则会忽略此字段。如果 `bgw_main` 为 NULL，工作进程会动态加载指定的库，并使用 `bgw_function_name` 确定要调用的函数。

`bgw_function_name` 是动态加载库中的函数名，该函数用作新后台工作进程的初始入口点。除非 `bgw_main` 为 NULL，否则会忽略此字段。

`bgw_notify_pid` 是一个 Apache Cloudberry 后端进程的 PID；工作进程启动或退出时，postmaster 应向该后端进程发送 `SIGUSR1`。对于在 postmaster 启动时注册的工作进程，或者注册工作进程的后端不希望等待其启动的情况，应将此字段设为 0。否则，应将其初始化为 `MyProcPid`。

进程运行后，可以通过调用 ``BackgroundWorkerInitializeConnection(char *dbname, char *username)`` 连接数据库。这使进程能够通过 `SPI` 接口运行事务和查询。如果 dbname 为 NULL，会话不会连接任何特定数据库，但可以访问共享系统目录。如果 username 为 NULL，进程将以 `initdb` 期间创建的超级用户身份运行。每个后台进程只能调用一次 BackgroundWorkerInitializeConnection，不能切换数据库。

控制权到达 `bgw_main` 函数时，信号最初处于阻塞状态，必须由该函数解除阻塞；这样可以让进程在必要时自定义信号处理器。新进程可以调用 `BackgroundWorkerUnblockSignals` 解除信号阻塞，也可以调用 `BackgroundWorkerBlockSignals` 阻塞信号。

如果后台工作进程的 `bgw_restart_time` 配置为 `BGW_NEVER_RESTART`，或者该进程以退出码 0 退出，或由 `TerminateBackgroundWorker` 终止，postmaster 会在其退出时自动注销它。否则，该进程将在 `bgw_restart_time` 配置的时间间隔后重启；如果 postmaster 因后端故障而重新初始化集群，则会立即重启。只需暂时挂起执行的后端应使用可中断的休眠，而不应退出；这可以通过调用 `WaitLatch()` 实现。调用该函数时，务必设置 `WL_POSTMASTER_DEATH` 标志，并检查返回码，以便在 `postgres` 自身已终止的紧急情况下及时退出。

使用 `RegisterDynamicBackgroundWorker` 函数注册后台工作进程时，执行注册的后端可以获取该工作进程的状态信息。为此，后端应将一个 `BackgroundWorkerHandle *` 的地址作为第二个参数传给 `RegisterDynamicBackgroundWorker`。如果注册成功，此指针将被初始化为一个不透明句柄，随后可将其传给 ``GetBackgroundWorkerPid(BackgroundWorkerHandle *, pid_t *)`` 或 ``TerminateBackgroundWorker(BackgroundWorkerHandle *)``。`GetBackgroundWorkerPid` 可用于轮询工作进程的状态：返回值 `BGWH_NOT_YET_STARTED` 表示 postmaster 尚未启动该工作进程；`BGWH_STOPPED` 表示它曾经启动，但已不再运行；`BGWH_STARTED` 表示它当前正在运行。在最后一种情况下，还会通过第二个参数返回 PID。`TerminateBackgroundWorker` 会使 postmaster 在工作进程仍在运行时向其发送 `SIGTERM`，并在它不再运行时立即注销它。

在某些情况下，注册后台工作进程的进程可能需要等待该工作进程启动。为此，可以将 `bgw_notify_pid` 初始化为 `MyProcPid`，然后将注册时获得的 `BackgroundWorkerHandle *` 传给 `WaitForBackgroundWorkerStartup(`BackgroundWorkerHandle *handle`, `pid_t *`)` 函数。此函数会一直阻塞，直到 postmaster 尝试启动后台工作进程，或 postmaster 终止。如果后台工作进程正在运行，返回值为 `BGWH_STARTED`，并且 PID 会写入提供的地址。否则，返回值为 `BGWH_STOPPED` 或 `BGWH_POSTMASTER_DIED`。

`worker_spi` contrib 模块包含一个可运行的示例，演示了一些实用技巧。

可注册的后台工作进程最大数量受服务器配置参数 `max_worker_processes` 限制。
