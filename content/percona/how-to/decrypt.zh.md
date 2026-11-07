---
title: 移除加密表的加密
linkTitle: 移除加密表的加密
description: 通过更改访问方法或复制为未加密表移除表加密。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/decrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 580
upstream_source: percona
---

## 方法一：更改访问方法 {#method-1-change-the-access-method}

如果使用 `tde_heap` 访问方法加密了表，现在需要移除加密，对目标表（以下示例为 `mytable`）执行：

```sql
ALTER TABLE mytable SET ACCESS METHOD heap;
```

注意，`SET ACCESS METHOD` 会丢弃提示位，可能影响性能。对整个表执行普通的 `SELECT count(*)` 或 `VACUUM`，会检查每个元组的可见性并设置提示位。因此，执行 `ALTER TABLE` 后，请对表运行简单的 `count(*)`：

```sql
SELECT count(*) FROM mytable;
```

确认表已不再加密：

```sql
SELECT pg_tde_is_encrypted('mytable');
```

输出返回 `f`，表示表不再加密。

## 方法二：基于加密表创建新的未加密表 {#method-2-create-a-new-not-encrypted-table-on-the-base-of-the-encrypted-one}

也可以创建结构和数据均与原表相同的未加密表。例如，原加密表为 `EncryptedCustomers`，使用以下命令创建新表 `Customers`：

```sql
CREATE TABLE Customers AS SELECT * FROM EncryptedCustomers;
```

新表 `Customers` 继承 `EncryptedCustomers` 的结构和数据。

（可选）如果不再需要 `EncryptedCustomers`，可以删除它。

```sql
DROP TABLE EncryptedCustomers;
```
