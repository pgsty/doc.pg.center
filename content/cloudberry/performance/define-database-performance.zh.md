---
title: "定义数据库性能"
description: "系统性能管理包括衡量性能、查明性能问题的原因，以及使用现有工具和技术解决问题。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/define-database-performance.md"
---

Apache Cloudberry 根据数据库管理系统（DBMS）向请求方提供信息的速率来衡量数据库性能。

## 了解性能影响因素 {#understand-the-performance-factors}

数据库性能受若干关键因素影响。了解这些因素有助于发现性能改进空间并避免问题：

- [系统资源](#system-resources)
- [工作负载](#workload)
- [吞吐量](#throughput)
- [争用](#contention)
- [优化](#optimization)

### 系统资源 {#system-resources}

数据库性能很大程度上取决于磁盘 I/O 和内存使用情况。要准确设定性能预期，需要了解部署 DBMS 的硬件的基准性能。CPU、硬盘、磁盘控制器、RAM 和网络接口等硬件组件的性能都会显著影响数据库的运行速度。

> [!NOTE]
> 如果在 Apache Cloudberry 主机上使用终端安全软件，可能会影响数据库的性能和稳定性。详情参见[关于终端安全软件](/cloudberry/security/#about-endpoint-security-software)。

### 工作负载 {#workload}

工作负载是对 DBMS 的全部需求之和，会随时间变化。总工作负载由任一时刻经由 DBMS 处理的用户查询、应用程序、批处理作业、事务和系统命令共同组成。例如，运行月末报表时工作负载可能增加，而周末大部分用户不在办公室时可能减少。工作负载对数据库性能影响很大。了解工作负载及其需求高峰时段，有助于规划最有效的系统资源使用方式，从而处理尽可能多的工作负载。

### 吞吐量 {#throughput}

系统吞吐量表示其整体数据处理能力。DBMS 吞吐量以每秒查询数、每秒事务数或平均响应时间衡量。DBMS 吞吐量与底层系统的处理能力（磁盘 I/O、CPU 速度、内存带宽等）密切相关，因此设定 DBMS 吞吐量目标时，需要了解硬件的吞吐能力。

### 争用 {#contention}

争用是指两个或多个工作负载组件以相互冲突的方式使用系统，例如多个查询尝试同时更新同一份数据，或多个大型工作负载竞争系统资源。争用加剧时，吞吐量会下降。

### 优化 {#optimization}

DBMS 优化会影响系统的整体性能。SQL 写法、数据库配置参数、表设计、数据分布等都会影响数据库查询优化器，使其能够生成最高效的访问计划。

## 确定可接受的性能 {#determine-acceptable-performance}

开始性能调优时，应了解系统预期达到的性能水平，并定义可衡量的性能要求，以便准确评估系统性能。设定性能目标时，请考虑以下方面：

- [硬件基准性能](#baseline-hardware-performance)
- [性能基准测试](#performance-benchmarks)

### 硬件基准性能 {#baseline-hardware-performance}

大多数数据库性能问题源于数据库运行的底层系统，而非数据库本身。I/O 瓶颈、内存问题和网络问题都可能显著降低数据库性能。了解硬件和操作系统（OS）的基准能力，有助于在着手数据库级或查询级调优之前，识别并排查硬件相关问题。

### 性能基准测试 {#performance-benchmarks}

要维持良好的性能或解决性能问题，应了解 DBMS 处理特定工作负载的能力。基准测试是一种预先定义、能够产生已知结果集的工作负载。定期运行相同的基准测试，有助于识别随时间推移出现的系统性能下降。还可以使用基准测试比较工作负载，找出需要优化的查询或应用程序。

许多第三方组织为数据库行业提供基准测试工具，例如事务处理性能委员会（TPC）。TPC 提供的 TPC-H 是一套决策支持系统基准测试，用于检查大量数据、运行复杂度较高的查询，并回答关键业务问题。有关 TPC-H 的更多信息，请访问：[http://www.tpc.org/tpch](http://www.tpc.org/tpch)
