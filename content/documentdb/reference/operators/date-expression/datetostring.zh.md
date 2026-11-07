---
title: $dateToString
description: $dateToString 运算符将日期对象转换为格式化字符串。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/date-expression/$datetostring.md
weight: 70
translation_source_sha256: 8d2c97f9db7ad0dfea92429fae7364c42ece93d5454fd6758c0c82199ce40ba8
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$dateToString` 运算符用于将日期对象转换为指定格式的字符串。它常用于聚合流水线中，格式化日期字段以供报表、查询或显示使用。此运算符用途广泛，允许定义自定义日期格式。

## 语法 {#syntax}

```javascript
{
  $dateToString: {
    format: "<format_string>",
    date: <date_expression>,
    timezone: "<timezone>",
    onNull: "<replacement_value>"
  }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`format`** | 指定输出日期格式的字符串。 |
| **`date`** | 要格式化的日期表达式。 |
| **`timezone`** | （可选）指定时区的字符串。未提供时默认为 UTC。 |
| **`onNull`** | （可选）`date` 字段为 `null` 或缺失时返回的值。 |
{.fields}

## 格式说明符 {#format-specifiers}

| 符号 | 含义                  |
| ------ | ------------------------ |
| `%Y`   | 年份（四位数字）          |
| `%m`   | 月份（两位数字）         |
| `%d`   | 当月的第几天（两位数字）  |
| `%H`   | 小时（24 小时制，两位数字） |
| `%M`   | 分钟（两位数字）        |
| `%S`   | 秒（两位数字）        |
| `%L`   | 毫秒（三位数字）   |

## 示例 {#examples}

以下是 stores 集合中的一个示例文档。

```json
{
    "_id": "0fcc0bf0-ed18-4ab8-b558-9848e18058f4",
    "name": "First Up Consultants | Beverage Shop - Satterfieldmouth",
    "location": {
        "lat": -89.2384,
        "lon": -46.4012
    },
    "staff": {
        "totalStaff": {
            "fullTime": 8,
            "partTime": 20
        }
    },
    "sales": {
        "totalSales": 75670,
        "salesByCategory": [
            {
                "categoryName": "Wine Accessories",
                "totalSales": 34440
            },
            {
                "categoryName": "Bitters",
                "totalSales": 39496
            },
            {
                "categoryName": "Rum",
                "totalSales": 1734
            }
        ]
    },
    "promotionEvents": [
        {
            "eventName": "Unbeatable Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 6,
                    "Day": 23
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 7,
                    "Day": 2
                }
            },
            "discounts": [
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Bitters",
                    "discountPercentage": 15
                },
                {
                    "categoryName": "Brandy",
                    "discountPercentage": 8
                },
                {
                    "categoryName": "Sports Drinks",
                    "discountPercentage": 22
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 19
                }
            ]
        },
        {
            "eventName": "Steal of a Deal Days",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 21
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 9,
                    "Day": 29
                }
            },
            "discounts": [
                {
                    "categoryName": "Organic Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "White Wine",
                    "discountPercentage": 20
                },
                {
                    "categoryName": "Sparkling Wine",
                    "discountPercentage": 19
                },
                {
                    "categoryName": "Whiskey",
                    "discountPercentage": 17
                },
                {
                    "categoryName": "Vodka",
                    "discountPercentage": 23
                }
            ]
        }
    ]
}
```

### 示例 1：将日期字段格式化为类似 ISO 格式的字符串 {#example-1-formatting-a-date-field-to-an-iso-like-string}

此查询使用 `$dateToString` 运算符，将 `lastUpdated` 时间戳格式化为 `YYYY-MM-DD` 字符串。这样可以用便于阅读的格式呈现日期，适用于日志、报表或用户界面。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      formattedDate: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$lastUpdated"
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "formattedDate": "2024-12-04"
  }
]
```

### 示例 2：处理空值 {#example-2-handling-null-values}

此查询使用 `$dateToString`，将不存在的字段 `lastUpdated_new` 中的时间戳格式化为 `YYYY-MM-DD` 字符串。由于日期缺失或为 null，它通过 onNull 选项返回备用字符串 "No date available"。

```javascript
db.stores.aggregate([
  {
    $match: { _id: "e6410bb3-843d-4fa6-8c70-7472925f6d0a" }
  },
  {
    $project: {
      _id: 0,
      formattedDateOrDefault: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$lastUpdated_new", // field doesn't exist
          onNull: "No date available"
        }
      }
    }
  }
])
```

此查询返回以下结果。

```json
[
  {
    "formattedDateOrDefault": "No date available"
  }
]
```
