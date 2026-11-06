---
title: "处理数据加载错误"
description: "实际数据往往并不完美，可能存在格式错误、值缺失或数据类型不一致等问题。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/handle-data-errors.md"
---

Apache Cloudberry 提供完善的错误处理机制，允许在加载格式正确的数据的同时隔离和管理有问题的行，确保提取、转换、加载（ETL）流程具备容错能力和可靠性。

默认情况下，如果外部表数据包含任何错误，整个加载操作都会失败，不加载任何数据。启用错误处理后，可以加载有效数据，并单独处理有问题的行。

## 错误处理模式 {#error-handling-modes}

Apache Cloudberry 支持两种错误处理方式：

1. 单行错误隔离允许系统跳过个别有问题的行，继续处理其余有效数据，防止个别数据质量问题导致整个操作失败。
2. 错误日志记录功能会捕获有问题数据行的完整详细信息，包括错误说明、行号以及导致失败的实际数据，便于深入分析和修复。

## 单行错误隔离 {#single-row-error-isolation}

### 基本错误隔离 {#basic-error-isolation}

在外部表定义中添加 `SEGMENT REJECT LIMIT`，以启用单行错误隔离：

```sql
CREATE EXTERNAL TABLE sales_data_with_errors (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
SEGMENT REJECT LIMIT 100;
```

此配置允许每个 Segment 最多出现 100 个错误行，超过此数量后操作才会失败。

### 基于百分比的限制 {#percentage-based-limits}

也可以按百分比指定错误上限：

```sql
CREATE EXTERNAL TABLE sales_data (
    transaction_id int,
    product_name text, 
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
SEGMENT REJECT LIMIT 5 PERCENT;
```

此设置允许最多 5% 的行包含错误，超过该比例后操作才会失败。

## 错误日志记录 {#error-logging}

### 启用错误日志记录 {#enable-error-logging}

使用 `LOG ERRORS` 捕获被拒绝行的详细信息：

```sql
CREATE EXTERNAL TABLE sales_data_logged (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
LOG ERRORS 
SEGMENT REJECT LIMIT 50;
```

### 持久化错误日志记录 {#persistent-error-logging}

要进行长期错误分析，请使用持久化错误日志记录：

```sql
CREATE EXTERNAL TABLE sales_data_persistent (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2)
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
LOG ERRORS PERSISTENTLY
SEGMENT REJECT LIMIT 25;
```

## 查看错误信息 {#view-error-information}

### 查询错误日志 {#query-error-logs}

启用错误日志记录后，Apache Cloudberry 会创建可供查询的错误日志表：

```sql
-- View recent errors from the current session
SELECT * FROM gp_read_error_log('sales_data_logged');
```

### 错误日志表结构 {#error-log-table-structure}

错误日志包含以下列：

| 列 | 说明 |
|--------|-------------|
| `cmdtime` | 错误发生时的时间戳 |
| `relname` | 外部表名称 |
| `filename` | 包含错误的源文件 |
| `linenum` | 源文件中的行号 |
| `bytenum` | 源文件中的字节位置 |
| `errmsg` | 错误消息说明 |
| `rawdata` | 导致错误的原始数据 |
| `rawbytes` | 有问题数据的原始字节 |

### 错误分析示例 {#example-error-analysis}

```sql
-- Find the most common error types
SELECT errmsg, COUNT(*) as error_count
FROM gp_read_error_log('sales_data_logged')
GROUP BY errmsg
ORDER BY error_count DESC;

-- View specific error details
SELECT cmdtime, filename, linenum, errmsg, rawdata
FROM gp_read_error_log('sales_data_logged')
WHERE errmsg LIKE '%invalid input syntax%'
ORDER BY cmdtime DESC;
```

## 常见数据错误及解决方法 {#common-data-errors-and-solutions}

### 数据类型转换错误 {#data-type-conversion-errors}

**错误**：`invalid input syntax for type numeric`
**原因**：数值列中含有非数值数据
**解决方法**：清洗数据，或使用文本列并在后续处理中转换

```sql
-- Original problematic data: "N/A" in amount column
-- Solution: Use text type and handle conversion later
CREATE EXTERNAL TABLE sales_flexible (
    transaction_id int,
    product_name text,
    sale_date text,  -- Use text for flexible parsing
    amount text      -- Use text to handle "N/A" values
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
LOG ERRORS SEGMENT REJECT LIMIT 10 PERCENT;
```

### 日期格式问题 {#date-format-issues}

**错误**：`invalid input syntax for type date`
**原因**：日期格式不一致
**解决方法**：统一日期格式，或采用灵活的解析方式

```sql
-- Handle multiple date formats in post-processing
SELECT 
    transaction_id,
    product_name,
    CASE 
        WHEN sale_date ~ '^\d{4}-\d{2}-\d{2}$' THEN sale_date::date
        WHEN sale_date ~ '^\d{2}/\d{2}/\d{4}$' THEN to_date(sale_date, 'MM/DD/YYYY')
        ELSE NULL
    END as parsed_date,
    amount::decimal(10,2)
FROM sales_flexible
WHERE sale_date IS NOT NULL;
```

### 缺少列或存在多余列 {#miss-or-extra-columns}

**错误**：`extra data after last expected column`
**原因**：列数不一致
**解决方法**：使用更灵活的表定义

```sql
-- Add extra optional columns to handle variable column counts
CREATE EXTERNAL TABLE flexible_sales (
    transaction_id int,
    product_name text,
    sale_date date,
    amount decimal(10,2),
    extra_field1 text,  -- Optional fields
    extra_field2 text,
    extra_field3 text
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV' (HEADER)
LOG ERRORS SEGMENT REJECT LIMIT 20 PERCENT;
```

### 字符编码问题 {#character-encoding-issues}

**错误**：`invalid byte sequence`
**原因**：字符编码不匹配
**解决方法**：指定正确的编码

```sql
CREATE EXTERNAL TABLE encoded_data (
    id int,
    description text
)
LOCATION ('gpfdist://etl-server:8081/data/*.txt')
FORMAT 'TEXT' (DELIMITER '|')
ENCODING 'LATIN1'  -- Specify encoding
LOG ERRORS SEGMENT REJECT LIMIT 5 PERCENT;
```

## 错误处理策略 {#error-handling-strategies}

### 两阶段加载 {#two-phase-loading}

对于复杂的数据清洗，可采用中间暂存方式：

```sql
-- Phase 1: Load into staging table with flexible types
CREATE EXTERNAL TABLE sales_staging (
    transaction_id text,
    product_name text,
    sale_date text,
    amount text,
    raw_line text  -- Store entire row for complex cases
)
LOCATION ('gpfdist://etl-server:8081/sales/*.csv')
FORMAT 'CSV'
LOG ERRORS SEGMENT REJECT LIMIT 20 PERCENT;

-- Phase 2: Clean and insert into final table
INSERT INTO sales_final (transaction_id, product_name, sale_date, amount)
SELECT 
    transaction_id::int,
    product_name,
    sale_date::date,
    amount::decimal(10,2)
FROM sales_staging
WHERE transaction_id ~ '^\d+$'  -- Validate numeric ID
  AND sale_date ~ '^\d{4}-\d{2}-\d{2}$'  -- Validate date format
  AND amount ~ '^\d+\.?\d*$';  -- Validate amount format
```

### 错误阈值监控 {#error-threshold-monitoring}

设置错误率监控：

```sql
-- Function to check error rate
CREATE OR REPLACE FUNCTION check_error_rate(table_name text, threshold_percent numeric)
RETURNS boolean AS $$
DECLARE
    error_count int;
    total_count int;
    error_rate numeric;
BEGIN
    SELECT COUNT(*) INTO error_count FROM gp_read_error_log(table_name);
    
    -- Estimate total processed rows (depends on your tracking method)
    SELECT reltuples INTO total_count FROM pg_class WHERE relname = table_name;
    
    IF total_count > 0 THEN
        error_rate := (error_count::numeric / total_count) * 100;
        RETURN error_rate <= threshold_percent;
    END IF;
    
    RETURN true;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT check_error_rate('sales_data_logged', 5.0);  -- Check if error rate is under 5%
```

## 最佳实践 {#best-practices}

### 在设计中考虑错误 {#design-for-errors}

1. 起初使用较宽松的表定义，采用文本数据类型和较高的错误上限，以便在实施严格验证规则之前全面了解数据质量问题。
2. 随着对数据质量的把握逐渐加深，并从错误日志中识别出规律，逐步添加约束和类型转换，推进数据验证。
3. 建立定期监控和审查错误日志的流程，识别系统性的数据质量问题，以及可能反映源系统或数据处理流水线问题的趋势。

### 错误上限指导 {#error-limit-guidelines}

| 数据质量 | 建议的拒绝上限 | 使用场景 |
|--------------|----------------------|----------|
| 高 | 1-10 行 | 生产系统 |
| 中等 | 1-5% | 开发/测试 |
| 差 | 10-20% | 初步数据探索 |
| 未知 | 50% | 数据探查阶段 |

### 操作流程 {#operational-procedures}

1. 制定定期清理旧错误日志的计划，以防止过量占用存储并保持系统性能。
2. 配置监控系统，使其在错误率超过预设阈值时发出告警，以便快速响应数据质量问题。
3. 与数据提供方保持沟通，交流错误规律，并共同改进源数据质量。

### 性能注意事项 {#performance-considerations}

1. 错误日志记录功能会在数据加载过程中引入一定的计算开销，处理大型数据集时应考虑这一影响。
2. 设置较高的 Segment 拒绝上限，可以在操作失败前处理更多行，但也意味着分析有问题数据时会消耗更多资源。
3. 生产环境中的错误日志表可能显著增长，因此应实施监控，跟踪存储使用情况，防止出现磁盘空间问题。

## 故障排查 {#troubleshooting}

### 错误率过高 {#high-error-rates}

如果错误率过高：

1. 分析错误日志条目，识别数据中的规律或系统性问题，例如反复出现的格式问题，或特定列中的值缺失。
2. 与数据提供方合作，核实源数据的质量和一致性，包括检查数据格式或处理方式近期是否发生变化。
3. 仔细审查外部表定义，确保列的数据类型、分隔符和格式说明与实际数据结构准确匹配。
4. 先使用小规模数据样本排查问题，在处理更大的数据集之前快速定位问题。

### 性能问题 {#performance-issues}

如果错误处理影响了性能：

1. 微调 Segment 拒绝上限，在容错性和处理效率之间取得平衡，避免使用不必要的过高阈值而浪费资源。
2. 对于已知存在质量问题的复杂数据，可以考虑采用两阶段加载流程，并使用数据类型灵活的中间暂存表。
3. 将大规模数据加载拆分为较小、易于管理的批次，以减轻内存压力并改善错误隔离效果。
4. 在数据加载过程中持续监控系统资源，包括内存使用情况、磁盘 I/O 和存储占用。

## 进一步了解 {#learn-more}

- [使用 gpfdist 加载数据](/cloudberry/data-loading/files/load-data-using-gpfdist/)
- [使用 COPY 加载数据](/cloudberry/data-loading/files/load-data-using-copy/)
