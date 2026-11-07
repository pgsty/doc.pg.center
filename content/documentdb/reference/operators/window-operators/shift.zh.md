---
title: $shift 在 DocumentDB 中的用法
description: 在分区内偏移值并返回偏移后值的窗口运算符。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/window-operators/$shift.md
weight: 110
translation_source_sha256: 7e8cf4fbd9e638b6cd55e71d1234b99494fed888a5ed887e7660e216eed2e048
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$shift` 是用于聚合流水线的窗口运算符，它在分区内偏移值并返回偏移后的值。需要比较已排序分区中相邻文档的值时，可使用此运算符。

## 语法 {#syntax}

```javascript
{
  $shift: {
    output: <expression>,
    by: <number>,
    default: <expression>
  }
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`output`** | 指定要偏移其值的字段或表达式。 |
| **`by`** | 指定值偏移的位置数。正值偏移到后续位置，负值偏移到先前位置。 |
| **`default`** | 指定偏移操作超出边界时返回的默认值。 |
{.fields}

<span id="example-s"></span>

## 示例 {#examples}

### 示例 1：偏移销售数据 {#example-1-shifting-sales-data}

此示例演示如何使用 `$shift`，为销售数据的已排序分区中的每个文档计算前一个销售值。

```javascript
db.collection.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$sales.salesByCategory.categoryName",
      sortBy: { "sales.salesByCategory.totalSales": 1 },
      output: {
        previousSales: {
          $shift: {
            output: "$sales.salesByCategory.totalSales",
            by: -1,
            default: null
          }
        }
      }
    }
  }
])
```

### 示例 2：偏移促销活动日期 {#example-2-shifting-promotional-event-dates}

此示例按 startDate 对所有活动排序，以计算前一个促销活动的开始日期。由于要将所有活动一起处理，因此不进行分区。

```javascript
db.promotionEvents.aggregate([
  {
    $setWindowFields: {
      partitionBy: null,
      sortBy: { "promotionalDates.startDate": 1 },
      output: {
        previousStartDate: {
          $shift: {
            output: "$promotionalDates.startDate",
            by: -1,
            default: null
          }
        }
      }
    }
  }
])
```
