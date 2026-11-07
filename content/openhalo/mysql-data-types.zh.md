---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16；2026-11-07 文档快照"
upstream_notice: /zh/attribution/#halodb
title: 兼容的 MySQL 数据类型
linkTitle: MySQL 数据类型
description: Halo 文档列出的 MySQL 数字、字符、日期时间、ENUM、SET 和 YEAR 类型。
weight: 50
---

Halo 1.0.16 的 MySQL 参考资料说明兼容常用的数字、字符、日期时间和特殊 MySQL 类型。接受某个类型名称，并不代表所有取值范围、转换、排序规则或自动值行为都与原生 MySQL 完全相同；请验证应用真正依赖的值和语义。

## 数字类型 {#numeric}

文档列出的整数类型包括 `TINYINT`、`SMALLINT`、`MEDIUMINT`、`INT` 和 `BIGINT`，还包括 `FLOAT`、`DOUBLE`、`NUMERIC` 和 `DECIMAL`。支持的数字形式可以使用 `SIGNED` 和 `UNSIGNED` 修饰符。

```sql
CREATE TABLE int_example (
  id INT,
  id_signed INT SIGNED,
  id_unsigned INT UNSIGNED,
  amount DECIMAL(12, 2) UNSIGNED
);
```

迁移 `UNSIGNED` 字段时，请测试溢出、负数、类型转换和应用层校验。PostgreSQL 派生存储在数字边界行为上可能有所不同。

## 字符类型 {#character}

文档列出的字符类型包括 `CHAR`、`VARCHAR`、`TINYTEXT`、`TEXT`、`MEDIUMTEXT` 和 `LONGTEXT`：

```sql
CREATE TABLE profile (
  id INT,
  display_name VARCHAR(200),
  bio TEXT
);

INSERT INTO profile VALUES (1, 'Alice', 'A short bio');
```

请使用代表性数据验证字符编码、排序规则、比较顺序、最大长度和客户端驱动的参数处理。

## `ENUM` 与 `SET` {#enum-and-set}

当前参考资料展示了原生内联的 `ENUM` 和 `SET` 定义。`ENUM` 将字段限制为列出的成员；`SET` 可以存储声明列表中的零个或多个成员。

```sql
CREATE TABLE preference (
  id INT,
  status ENUM('active', 'inactive', 'pending'),
  channels SET('email', 'sms', 'push')
);

INSERT INTO preference VALUES (1, 'active', 'email,push');
```

迁移依赖 MySQL 特殊类型语义的 schema 前，请测试非法成员、空值、排序、比较以及 dump/restore 行为。

## 日期时间类型 {#date-and-time}

文档覆盖 `DATE`、`DATETIME`、`TIMESTAMP` 和 `YEAR`。`DATETIME` 与 `TIMESTAMP` 接受文档描述的 `YYYY-MM-DD HH:MM:SS` 形式。当前 Halo 参考资料说明 `TIMESTAMP` 不会隐式添加 MySQL 的自动更新行为；应用需要时应显式指定：

```sql
CREATE TABLE audit_event (
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  event_year YEAR
);

INSERT INTO audit_event VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2026);
```

`YEAR` 接受 `1901` 至 `2155` 的四位年份。它不会执行 MySQL 的两位年份转换，因此应始终使用四位年份，并测试范围外的输入：

```sql
CREATE TABLE year_example (event_year YEAR);
INSERT INTO year_example VALUES (2026), ('1999');
```

请结合应用的 session 时区和驱动测试时区转换、默认值和自动更新行为。

完整的上游示例见 [Halo MySQL 数据类型参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types)。

## 资料来源 {#sources}

本页为 [Halo Database MySQL 兼容参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types)的原创摘要。上游未明确公开文档许可证；版本、版权与引用方式见[来源说明](/attribution/#halodb)。
