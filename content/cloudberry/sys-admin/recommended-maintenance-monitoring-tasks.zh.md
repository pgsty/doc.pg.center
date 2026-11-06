---
title: "推荐的监控与维护任务"
description: "本节列出建议执行的监控和维护操作，以确保 Apache Cloudberry 集群具有高可用性并保持稳定性能。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/recommended-maintenance-monitoring-tasks.md"
---

以下各节中的表格建议 Apache Cloudberry 系统管理员定期执行一些操作，以确保系统的所有组件都处于最佳运行状态。监控操作有助于尽早发现和诊断问题。维护操作有助于使系统保持最新状态，并避免性能恶化，例如系统表膨胀或可用磁盘空间逐渐减少。

不必在每个集群中实施所有建议；请将频率和严重性建议作为参考，根据服务要求实施相应措施。

## 数据库状态监控操作 {#database-state-monitoring-operations}

<table>
  <thead>
    <tr>
      <th>操作</th>
      <th>过程</th>
      <th>纠正措施</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        列出当前处于 down 状态的 Segment。如果返回任何行，
        应生成警告或告警。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
        <p>严重性：重要</p>
      </td>
<td>
    在 <code>postgres</code> 数据库中运行以下查询：
    <pre><code>
SELECT *<br />
FROM gp_segment_configuration<br />
WHERE status = 'd';
    </code></pre>
</td>
      <td>
        如果查询返回任何行，请执行以下步骤
        纠正问题：
        <ol>
          <li>验证 down Segment 所在的主机是否有响应。</li>
          <li>
            如果主机正常，请检查已停止运行的 Segment 的主实例和镜像实例
            的日志文件，查明这些 Segment
            停止运行的根本原因。
          </li>
          <li>
            如果没有发现意外错误，请运行
            <code>gprecoverseg</code> 工具，使 Segment 恢复在线。
          </li>
        </ol>
      </td>
    </tr>
    <tr>
      <td>
        检查处于 up 状态但未同步的 Segment。如果返回任何行，
        应生成警告或告警。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
      </td>
      <td>
        <div>
          在 <code>postgres</code> 数据库中执行以下查询：
          <pre>
            <code>SELECT * FROM gp_segment_configuration <br />
WHERE mode = 'n' and status <br />
= 'u' and content &lt;&gt; -1;</code>
          </pre>
        </div>
      </td>
      <td>
        如果查询返回行，则 Segment 可能正在
        从 <code>Not In Sync</code> 模式转为
        <code>Synchronized</code> 模式。使用 <code>gpstate -e</code> 跟踪
        进度。
      </td>
    </tr>
    <tr>
      <td>
        检查未以首选角色运行，但标记为 up
        且处于 <code>Synchronized</code> 状态的 Segment。如果发现此类 Segment，
        集群可能不平衡。如果返回任何行，
        应生成警告或告警。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
        <p>严重性：重要</p>
      </td>
      <td>
        <div>
          在 <code>postgres</code> 数据库中执行以下查询：
          <pre>
            <code>
SELECT * FROM gp_segment_configuration<br />WHERE preferred_role &lt;&gt; <br />role and status = 'u' and mode = 's';
            </code>
          </pre>
        </div>
      </td>
      <td>
        <p>
          当 Segment 未以其首选角色运行时，处理负载
          可能发生倾斜。运行 <code>gprecoverseg -r</code>，
          使 Segment 恢复其首选角色。
        </p>
      </td>
    </tr>
    <tr>
      <td>
        运行分布式查询，测试查询是否在所有 Segment 上运行。
        每个主 Segment 应返回一行。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
        <p>严重性：严重</p>
      </td>
      <td>
        <div>
          在 <code>postgres</code> 数据库中执行以下查询：
          <pre>
            <code>
SELECT gp_segment_id, count(*)<br />
FROM gp_dist_random('pg_class')<br />
GROUP BY 1;
            </code>
          </pre>
        </div>
      </td>
      <td>
        <p>
          如果此查询失败，说明向集群中某些 Segment 派发查询时
          出现了问题。这种情况很少见。检查无法派发到的主机，
          确保不存在硬件或网络问题。
        </p>
      </td>
    </tr>
    <tr>
      <td>
        测试 Apache Cloudberry 上的 Coordinator 镜像状态。如果
        值不是 "STREAMING"，则会产生告警或警告。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
        <p>严重性：重要</p>
      </td>
      <td>
        <div>
          运行以下 <code>psql</code>
          命令：
          <pre>
            <code>
psql &lt;dbname&gt; -c<br />
'SELECT pid, state FROM pg_stat_replication;'
            </code>
          </pre>
        </div>
      </td>
      <td>
        <p>
          检查 Coordinator 和 Standby Coordinator 的日志文件
          是否有错误。如果没有意外错误且机器正常运行，请运行
          <code>gpinitstandby</code> 工具，使 Standby Coordinator 上线。
        </p>
      </td>
    </tr>
    <tr>
      <td>
        执行基本检查，确认 Coordinator 已启动并正常工作。
        <p>建议频率：每 5 到 10 分钟运行一次</p>
        <p>严重性：严重</p>
      </td>
      <td>
        <div>
          在 <code>postgres</code> 数据库中运行以下查询：
          <pre>
            <code>SELECT count(*) FROM<br />
            gp_segment_configuration;</code>
          </pre>
        </div>
      </td>
      <td>
        <p>
          如果此查询失败，活动 Coordinator 可能已停止运行。如果原 Coordinator
          所在的服务器已启动并运行，请尝试在其上启动数据库。
          如果失败，请尝试激活 Standby Coordinator，
          使其作为 Coordinator 运行。
        </p>
      </td>
    </tr>
  </tbody>
</table>

## 硬件和操作系统监控 {#hardware-and-operating-system-monitoring}

<table>
  <thead>
    <tr>
      <th>操作</th>
      <th>过程</th>
      <th>纠正措施</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        检查 Apache Cloudberry 数据存储和操作系统
        使用的卷的磁盘空间使用情况。
        <p>建议频率：每 5 到 30 分钟</p>
        <p>严重性：严重</p>
      </td>
      <td>
        <div>
          <ul>
            <li>
              设置阈值，当磁盘使用量达到容量的某个百分比时生成告警。
              建议阈值为容量的 75%。
            </li>
            <li>
              不建议在磁盘使用量
              接近容量的 100% 时运行系统。
            </li>
          </ul>
        </div>
      </td>
      <td>
        对用户表使用 <code>VACUUM</code>/<code>VACUUM FULL</code>，
        回收死行占用的空间。
      </td>
    </tr>
    <tr>
      <td>
        检查网络接口上的错误或丢包。
        <p>建议频率：每小时</p>
        <p>严重性：重要</p>
      </td>
      <td>设置网络接口检查。</td>
      <td>
        <p>与网络和操作系统团队协作解决错误。</p>
      </td>
    </tr>
    <tr>
      <td>
        检查 RAID 错误或 RAID 性能下降。
        <p>建议频率：每 5 分钟</p>
        <p>严重性：严重</p>
      </td>
      <td>设置 RAID 检查。</td>
      <td>
        <ul>
          <li>尽快更换故障磁盘。</li>
          <li>
            与系统管理团队协作，尽快解决其他 RAID
            或控制器错误。
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        检查 I/O 带宽是否充足以及是否存在 I/O 倾斜。
        <p>
          建议频率：创建集群时，或怀疑
          存在硬件问题时。
        </p>
      </td>
      <td>
        运行 Apache Cloudberry
        <code>gpcheckperf</code> 工具。
      </td>
      <td>
        <div>
          如果数据传输速率与以下数值相差较大，
          集群的硬件配置可能不足：
          <ul>
            <li>磁盘读取每秒 2 GB</li>
            <li>磁盘写入每秒 1 GB</li>
            <li>网络读写每秒 10 Gigabit</li>
          </ul>
          如果传输速率低于预期，请与数据架构师
          讨论性能预期。
        </div>
        <p>
          如果集群中各台机器的性能表现不均衡，
          请与系统管理团队协作修复故障机器。
        </p>
      </td>
    </tr>
  </tbody>
</table>

## 目录监控 {#catalog-monitoring}

<table>
  <thead>
    <tr>
      <th>操作</th>
      <th>过程</th>
      <th>纠正措施</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        在每个数据库中运行目录一致性检查，确保集群中
        每台主机上的目录一致且状态良好。
        <p>可以在数据库运行期间执行此命令。</p>
        <p>建议频率：每周</p>
        <p>严重性：重要</p>
      </td>
      <td>
        在每个数据库中运行 Apache Cloudberry <code>gpcheckcat</code> 工具：
        <pre><code>gpcheckcat -O -p [target_port]</code></pre>
        <div>
          注意：使用
          <code>-O</code> 选项时，<code>gpcheckcat</code> 只运行通常 15 项测试中的 10 项。
        </div>
      </td>
      <td>针对发现的问题运行修复脚本。</td>
    </tr>
    <tr>
      <td>
        检查 <code>pg_class</code> 中是否有条目缺少对应的 <code>pg_attribute</code> 条目。
        <p>建议频率：每月</p>
        <p>严重性：重要</p>
      </td>
      <td>
        在系统没有用户时，在每个数据库中运行 Apache Cloudberry <code>gpcheckcat</code> 工具：
        <pre><code>gpcheckcat -R pgclass -p [target_port]</code></pre>
      </td>
      <td>针对发现的问题运行修复脚本。</td>
    </tr>
    <tr>
      <td>
        检查泄漏的临时模式和缺失的模式定义。
        <p>建议频率：每月</p>
        <p>严重性：重要</p>
      </td>
      <td>
        在停机期间、系统没有用户时，在每个数据库中运行 Apache Cloudberry <code>gpcheckcat</code> 工具：
        <pre><code>gpcheckcat -R namespace -p [target_port]</code></pre>
      </td>
      <td>针对发现的问题运行修复脚本。</td>
    </tr>
    <tr>
      <td>
        检查随机分布表上的约束。
        <p>建议频率：每月</p>
        <p>严重性：重要</p>
      </td>
      <td>
        在系统没有用户时，在每个数据库中运行 Apache Cloudberry <code>gpcheckcat</code> 工具：
        <pre><code>gpcheckcat -R distribution_policy -p [target_port]</code></pre>
      </td>
      <td>针对发现的问题运行修复脚本。</td>
    </tr>
    <tr>
      <td>
        检查对不存在对象的依赖。
        <p>建议频率：每月</p>
        <p>严重性：重要</p>
      </td>
      <td>
        在停机期间、系统没有用户时，在每个数据库中运行 Apache Cloudberry <code>gpcheckcat</code> 工具：
        <pre><code>gpcheckcat -R dependency -p [target_port]</code></pre>
      </td>
      <td>针对发现的问题运行修复脚本。</td>
    </tr>
  </tbody>
</table>

## 数据维护 {#data-maintenance}

<table>
  <thead>
    <tr>
      <th>操作</th>
      <th>过程</th>
      <th>纠正措施</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>检查表中是否缺少统计信息。</td>
      <td>
        检查每个数据库中的 <code>gp_stats_missing</code> 视图：
        <pre><code>SELECT * FROM gp_toolkit.gp_stats_missing;</code></pre>
      </td>
      <td>
        对缺少统计信息的表运行 <code>ANALYZE</code>。
      </td>
    </tr>
    <tr>
      <td>
        检查数据文件中存在膨胀（死空间）、
        且普通 <code>VACUUM</code> 命令无法回收这些空间的表。
        <p>建议频率：每周或每月</p>
        <p>严重性：警告</p>
      </td>
      <td>
        检查每个数据库中的 <code>gp_bloat_diag</code> 视图：
        <pre><code>SELECT * FROM gp_toolkit.gp_bloat_diag;</code></pre>
      </td>
      <td>
        <code>VACUUM FULL</code> 会对表加 <code>ACCESS EXCLUSIVE</code> 锁。
        请在用户和应用不需要访问这些表的时段运行 <code>VACUUM FULL</code>，
        例如运行负载较低时，
        或维护窗口期间。
      </td>
    </tr>
  </tbody>
</table>

## 数据库维护 {#database-maintenance}

<table>
  <thead>
    <tr>
      <th>操作</th>
      <th>过程</th>
      <th>纠正措施</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        回收堆表中已删除行占用的空间，
        使这些空间可以重新使用。<p>建议频率：每天</p>
        <p>严重性：严重</p>
      </td>
      <td>
        清理用户表：
        <pre><code>VACUUM &lt;table&gt;;</code></pre>
      </td>
      <td>定期清理已更新的表，防止膨胀。</td>
    </tr>
    <tr>
      <td>
        更新表统计信息。
        <p>
          建议频率：加载数据后以及执行查询前
        </p>
        <p>严重性：严重</p>
      </td>
      <td>
        分析用户表。可以使用
        <code>analyzedb</code> 管理工具：
        <pre><code>analyzedb -d &lt;database&gt; -a</code></pre>
      </td>
      <td>
        定期分析已更新的表，使优化器能够生成
        高效的查询执行计划。
      </td>
    </tr>
    <tr>
      <td>
        备份数据库数据。
        <p>建议频率：每天，或根据备份计划的要求</p>
        <p>严重性：严重</p>
      </td>
      <td>
        运行 <code>gpbackup</code> 工具，并行创建 Coordinator
        和 Segment 数据库的备份。
      </td>
      <td>
        最佳实践是随时备有最新的备份，
        以备必须恢复数据库时使用。
      </td>
    </tr>
    <tr>
      <td>
        清理系统目录、重建其索引并分析系统目录，
        使其保持高效。
        <p>
          建议频率：每周；如果数据库对象
          频繁创建和删除，则应更频繁地执行
        </p>
      </td>
      <td>
        <ol>
          <li>
            对每个数据库中的系统表执行 <code>VACUUM</code>。
          </li>
          <li>
            在每个数据库中运行 <code>REINDEX SYSTEM</code>，或使用
            <code>reindexdb</code>
            命令行工具并指定 <code>-s</code> 选项：
            <pre><code>reindexdb -s &lt;database&gt;</code></pre>
          </li>
          <li>
            对每个系统表执行 <code>ANALYZE</code>：
            <pre><code>analyzedb -s pg_catalog -d &lt;database&gt;</code></pre>
          </li>
        </ol>
      </td>
      <td>
        优化器从系统表中获取信息以创建
        查询计划。如果放任系统表和索引随时间推移而膨胀，
        扫描系统表就会增加查询执行时间。
        重建索引后务必运行 <code>ANALYZE</code>，因为 <code>REINDEX</code> 会使索引没有统计信息。
      </td>
    </tr>
  </tbody>
</table>

<!-- ## Patching and upgrading

<table>
  <thead>
    <tr>
      <th>Operations</th>
      <th>Procedure</th>
      <th>Corrective Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        Ensure any bug fixes or enhancements are applied to the kernel.
        <p>Recommended frequency: at least every 6 months</p>
        <p>Severity: IMPORTANT</p>
      </td>
      <td>Follow the vendor's instructions to update the Linux kernel.</td>
      <td>
        Keep the kernel current to include bug fixes and security fixes, and to
        avoid difficult future upgrades.
      </td>
    </tr>
    <tr>
      <td>
        <em>x</em>.
        <p>Recommended frequency: quarterly</p>
        <p>Severity: IMPORTANT</p>
      </td>
      <td>
        Follow upgrade instructions in the Apache Cloudberry
        <em>Release Notes</em>. Always upgrade to the latest in the series.
      </td>
      <td>
        Keep the Apache Cloudberry software current to incorporate bug fixes,
        performance enhancements, and feature enhancements into your Apache Cloudberry
        cluster.
      </td>
    </tr>
  </tbody>
</table> -->
