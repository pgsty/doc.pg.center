---
title: 监控 etcd
weight: 4500
description: 监控 etcd 系统健康状况并调试集群
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/monitoring.md"
---

每个 etcd 服务器通过其客户端端口上的 HTTP 端点提供本地监控信息。监控数据对于系统健康检查和集群调试均具有实用价值。

## 调试端点 {#debug-endpoint}

若设置 `--log-level=debug`，etcd 服务器将在其客户端端口的 `/debug` 路径下导出调试信息。设置 `--log-level=debug` 时需谨慎，因为会导致性能下降并产生过于冗长的日志。

`/debug/pprof` 端点是标准的 Go 运行时性能分析端点。该端点可用于分析 CPU、堆、互斥锁和协程的使用情况。例如，以下命令通过 `go tool pprof` 获取 etcd 花费时间最多的前 10 个函数：

```sh
$ go tool pprof http://localhost:2379/debug/pprof/profile
Fetching profile from http://localhost:2379/debug/pprof/profile
Please wait... (30s)
Saved profile in /home/etcd/pprof/pprof.etcd.localhost:2379.samples.cpu.001.pb.gz
Entering interactive mode (type "help" for commands)
(pprof) top10
310ms of 480ms total (64.58%)
Showing top 10 nodes out of 157 (cum >= 10ms)
    flat  flat%   sum%        cum   cum%
   130ms 27.08% 27.08%      130ms 27.08%  runtime.futex
    70ms 14.58% 41.67%       70ms 14.58%  syscall.Syscall
    20ms  4.17% 45.83%       20ms  4.17%  github.com/coreos/etcd/vendor/golang.org/x/net/http2/hpack.huffmanDecode
    20ms  4.17% 50.00%       30ms  6.25%  runtime.pcvalue
    20ms  4.17% 54.17%       50ms 10.42%  runtime.schedule
    10ms  2.08% 56.25%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).AuthInfoFromCtx
    10ms  2.08% 58.33%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).Lead
    10ms  2.08% 60.42%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/pkg/wait.(*timeList).Trigger
    10ms  2.08% 62.50%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/prometheus/client_golang/prometheus.(*MetricVec).hashLabelValues
    10ms  2.08% 64.58%       10ms  2.08%  github.com/coreos/etcd/vendor/golang.org/x/net/http2.(*Framer).WriteHeaders
```

端点 `/debug/requests` 通过网页浏览器提供 gRPC 跟踪信息和性能统计数据。例如，以下是一个针对键 `abc` 的 `Range` 请求：

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## 指标端点 {#metrics-endpoint}

每个 etcd 服务器在其客户端端口上通过 `/metrics` 路径导出指标，并可选地通过 `--listen-metrics-urls` 指定的位置导出。

指标可通过 `curl` 获取：

```sh
$ curl -L http://localhost:2379/metrics | grep -v debugging # ignore unstable debugging metrics

# HELP etcd_disk_backend_commit_duration_seconds The latency distributions of commit called by backend.
# TYPE etcd_disk_backend_commit_duration_seconds histogram
etcd_disk_backend_commit_duration_seconds_bucket{le="0.002"} 72756
etcd_disk_backend_commit_duration_seconds_bucket{le="0.004"} 401587
etcd_disk_backend_commit_duration_seconds_bucket{le="0.008"} 405979
etcd_disk_backend_commit_duration_seconds_bucket{le="0.016"} 406464
...
```

## 健康检查 {#health-check}

自 v3.3.0 起，除了响应 `/metrics` 端点外，任何由 `--listen-metrics-urls` 指定的位置也将响应 `/health` 端点。若标准端点配置了双向（客户端） TLS 身份认证，但负载均衡器或监控服务仍需访问健康检查时，此功能可提供便利。

从 v3.4 版本起，新增了两个端点 `/livez` 和 `/readyz`。

* `/livez` 端点反映进程是否正常运行，或是否需要重启。
* `/readyz` 端点反映进程是否已就绪，可接收流量。

端点的设计细节在 [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz) 中有详细记录。

每个端点包含多个独立的健康检查，可以使用 `verbose` 参数打印出检查详情及其状态，例如

```bash
curl -k http://localhost:2379/readyz?verbose
```

将看到类似以下的响应：

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

HTTP API 还支持排除特定检查，例如

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

运行 [Prometheus][prometheus] 监控服务是采集和记录 etcd 指标最简便的方式。

首先，安装 Prometheus：

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

将 Prometheus 的抓取器配置为指向 etcd 集群端点：

```sh
cat > /tmp/test-etcd.yaml <<EOF
global:
  scrape_interval: 10s
scrape_configs:
  - job_name: test-etcd
    static_configs:
    - targets: ['10.240.0.32:2379','10.240.0.33:2379','10.240.0.34:2379']
EOF
cat /tmp/test-etcd.yaml
```

设置 Prometheus 处理程序：

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

现在 Prometheus 每 10 秒采集一次 etcd 指标。


### 告警 {#alerting}

etcd v3 集群为 Prometheus 提供了一组 [默认告警](https://github.com/etcd-io/etcd/tree/main/contrib/mixin)。

> [!NOTE]
> 请注意，`job` 标签可能需要根据特定需求进行调整。规则编写时仅适用于单个集群，因此建议选择仅属于特定集群的标签。

### Grafana {#grafana}

[Grafana][grafana] 内置了 Prometheus 支持；只需添加一个 Prometheus 数据源：

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

然后导入默认的 [etcd 仪表板模板][template] 并进行自定义。例如，若 Prometheus 数据源名称为 `my-etcd`，则 JSON 中的 `datasource` 字段值也需相应设置为 `my-etcd`。

示例仪表板：

![](/etcd/op-guide/etcd-sample-grafana.png)

## 分布式跟踪 {#distributed-tracing}

在 v3.5 版本中，etcd 已添加对使用 [OpenTelemetry](https://github.com/open-telemetry) 的分布式追踪支持。

> [!NOTE]
> 在 etcd 3.7 中，请使用以下跟踪标志，不要使用旧的实验性前缀。

要启用分布式跟踪，请向 etcd 服务器传递 `--enable-distributed-tracing=true`，并配合 `--distributed-tracing-sampling-rate=<number>` 标志以选择每百万跨度收集的采样数量，默认采样率为 `0`。

通过以下可选标志启动 etcd 服务器，以配置分布式追踪：

- `--distributed-tracing-address` - （可选） - "localhost:4317" - 跟踪收集器的地址。

- `--distributed-tracing-service-name` - （可选） - "etcd" - 分布式追踪服务名称，所有 etcd 实例之间必须保持一致。

- `--distributed-tracing-instance-id` - （可选） - 实例 ID，虽然可选，但强烈建议设置，每个 etcd 实例必须唯一。

启用分布式追踪前，请确保已配置 OpenTelemetry 端点。若该地址与默认值不同，请使用 `--distributed-tracing-address` 标志进行覆盖。由于 OpenTelemetry 存在多种运行方式，请参阅 [收集器文档](https://opentelemetry.io/docs/collector/getting-started/) 以获取更多信息。

> [!NOTE]
> 与任何可观测性信号一样，存在资源开销。根据我们的初步测量，CPU 开销可能为 2% 至 4%。

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /etcd/op-guide/grafana.json
