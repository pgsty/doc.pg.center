---
title: "监控 PXF"
description: "监控 PXF 服务。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/monitor_pxf.md"
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

你可以通过命令行监控 PXF 的状态。

PXF 还通过公开 HTTP 端点提供有关 PXF Service 运行时状态的更多信息，你可以使用这些端点查询正在运行的进程的健康状况、构建信息和各种指标。


## 在命令行查看 PXF 状态 {#viewing-pxf-status-on-the-command-line}

`pxf cluster status` 命令显示 Apache Cloudberry 集群中所有主机上 PXF Service 实例的状态。`pxf status` 显示本地 Apache Cloudberry 主机上 PXF Service 实例的状态。

只有 `gpadmin` 用户可以请求 PXF Service 的状态。

请执行以下步骤，请求 Apache Cloudberry 集群的 PXF 状态。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 运行 `pxf cluster status` 命令：

    ```shell
    gpadmin@coordinator$ pxf cluster status
    ```

## 关于 PXF Service 运行时监控 {#about-pxf-service-runtime-monitoring}

PXF 公开了以下 HTTP 端点，可用于监控本地主机上正在运行的 PXF Service：

- `actuator/health` - 返回 PXF Service 的状态。
- `actuator/info` - 返回 PXF Service 的构建信息。
- `actuator/metrics` - 返回 PXF Service 的 JVM、扩展 Tomcat、系统、进程、Log4j2 以及 PXF 特有的指标。
- `actuator/prometheus` - 以可被 Prometheus 服务器抓取的格式返回所有指标。

任何用户都可以访问这些 HTTP 端点并查看 PXF 返回的监控信息。

你可以在浏览器中查看以下格式的 URL，或使用 `curl` 访问该 URL（默认 PXF 部署拓扑），以查看与特定端点关联的数据：

```text
http://localhost:5888/<endpoint>[/<name>]
```

如果为 PXF 选择了[备选部署拓扑](/cloudberry/pxf/administering/deployment_topos/#alternate-deployment-topology)，则 URL 为：

```text
http://<pxf_listen_address>:<port>/<endpoint>[/<name>]
```

例如，要查看在 `localhost` 上运行的 PXF 服务的构建信息，请查询 `actuator/info` 端点：

```text
http://localhost:5888/actuator/info
```

示例输出：

```text
{"build":{"version":"6.0.0","artifact":"pxf-service","name":"pxf-service","pxfApiVersion":"16","group":"org.apache.cloudberry.pxf","time":"2021-03-29T22:26:22.780Z"}}
```

要查看在本地 Apache Cloudberry 主机上运行的 PXF Service 的状态，请查询 `actuator/health` 端点：

```text
http://localhost:5888/actuator/health
```

示例输出：

```text
{"status":"UP","groups":["liveness","readiness"]}
```

### 检查 PXF 指标 {#examining-pxf-metrics}

PXF 通过与 Spring Boot 的集成公开 JVM、扩展 Tomcat 和系统指标。有关这些指标的更多信息，请参阅 Spring Boot 文档中的 [Supported Metrics](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html#production-ready-metrics-meter)。

PXF 还公开了特定于其处理过程的指标，包括：

| 指标名称 | 说明 |
|---------|-------------|
| pxf.fragments.sent  | 发送的片段数，以及将所有片段发送到 Apache Cloudberry 所花费的总时间。 |
| pxf.records.sent  | PXF 发送到 Apache Cloudberry 的记录数。 |
| pxf.records.received  | PXF 从 Apache Cloudberry 接收的记录数。 |
| pxf.bytes.sent  | PXF 发送到 Apache Cloudberry 的字节数。 |
| pxf.bytes.received  | PXF 从 Apache Cloudberry 接收的字节数。 |
| http.server.requests | 附加了 PXF 标签的标准指标。 |


查询某个指标时，PXF 返回的信息是自 PXF Service 上次（重新）启动以来收集的聚合数据。

要查看 PXF Service 提供的所有指标（名称）的列表，只需查询 `metrics` 端点：

```text
http://localhost:5888/actuator/metrics
```

### 过滤指标数据 {#filtering-metric-data}

PXF 为其返回的所有指标添加 `application` 标签；该标签的值始终为 `pxf-service`。

PXF 还为其特有的指标添加以下额外标签：`user`、`segment`、`profile` 和 `server`。每个 PXF 指标都带有所有这些标签。当无法确定标签值时，PXF 返回标签值 `unknown`。

你可以使用这些标签过滤 PXF 特有指标返回的信息。例如，要检查位于本地主机 `segment` 1 上、名为 `hadoop1` 的 PXF 服务器的 `pxf.records.received` 指标：

```text
http://localhost:5888/actuator/metrics/pxf.records.received?tag=segment:1&tag=server:hadoop1
```

某些指标（例如 `pxf.fragments.sent`）包含一个名为 `outcome` 的额外标签；你可以检查其值（`success` 或 `error`），以确定该片段的所有数据是否已发送。你也可以使用此标签过滤聚合数据。
