---
title: find
description: DocumentDB 中的 find 命令返回匹配指定过滤条件的文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/query-and-write/find.md
weight: 20
translation_source_sha256: 81c76d6f468260211e8e65a4fb897d42d034c4c77005af3b31fb5677393a510c
translation_review: AI-assisted bilingual review; 2026-11-07
---

DocumentDB 中的 `find` 命令用于查询集合中的文档。该命令是数据检索操作的基础，可通过过滤器、投影和查询选项进行定制，以精确控制结果。

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`find`** | (必需) 指定集合名称的字符串。 |
| **`filter`** | (可选) 指定匹配过滤器的文档；默认为所有文档。 |
| **`projection`** | (可选) 指定要返回的字段或表达式的文档。 |
| **`sort`** | (可选) 指定结果排序方式的文档。 |
| **`skip`** | (可选) 指定跳过的匹配文档数量的非负整数。 |
| **`limit`** | (可选) 指定最大结果数量的整数；`0` 表示无限制。负值使用其绝对值，不会隐式启用 `singleBatch`。 |
| **`batchSize`** | (可选) 指定首批结果数量的数字，转换为非负整数；默认为 `101`。`0` 会创建空的首批结果。响应大小限制仍然适用。 |
| **`singleBatch`** | (可选) 布尔值，表示在返回首批结果后关闭游标；默认为 `false`。 |
| **`hint`** | (可选) 指定索引名称或键模式的字符串或文档；也接受 `$natural` 提示。非自然提示不能与 `$natural` 排序结合使用。 |
| **`let`** | (可选) 指定命令作用域内表达式变量的文档，可通过 `$$name` 引用。 |
| **`maxTimeMS`** | (可选) 指定执行超时时间的数字，单位为毫秒；`0` 表示无显式超时。 |
| **`collation`** | (可选) 指定比较规则的文档；需要 `documentdb_core.enableCollation`。 |
{.fields}

## 示例：查找延误的出发航班 {#example-find-delayed-departures}

加载 [航空业示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)，然后运行：

```javascript
db.flights.find(
  { delay_minutes: { $gt: 0 } },
  { _id: 0, route_no: 1, arrival_airport: 1, delay_minutes: 1 }
).sort({ route_no: 1 }).batchSize(10).maxTimeMS(5000).toArray()
```

返回的数组为：

```json
[
  { "route_no": "PG0102", "arrival_airport": "KZN", "delay_minutes": 12 },
  { "route_no": "PG0104", "arrival_airport": "LED", "delay_minutes": 5 }
]
```

## 示例：过滤嵌入的机票航段 {#example-filter-embedded-ticket-segments}

```javascript
db.flights.find(
  { "segments.fare_conditions": "Business" },
  { _id: 0, route_no: 1 }
).sort({ route_no: 1 }).toArray()
```

此查询返回航线编号 `PG0102` 和 `PG0103`。点表示法用于选择每个机票航段中的字段；不要求整个 `segments` 数组与过滤条件完全相等。

Shell 游标会按需发出 [`getMore`](/documentdb/reference/commands/query-and-write/getmore/)。使用原始线协议请求的应用程序必须继续使用实际返回的 `cursor.id`。

## Shell 语法 {#shell-syntax}

```javascript
db.collection.find(query, projection, options)
```

## 详细示例 {#detailed-examples}

考虑以下来自 StoreData 数据库中 stores 集合的示例文档。

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

### 示例 1：检索所有文档 {#example-1-retrieve-all-documents}

不带任何查询过滤器的 find() 命令会返回集合中的所有文档。

```javascript
db.stores.find()
```

### 示例 2：使用查询过滤器检索文档 {#example-2-retrieve-documents-with-query-filters}

使用 name 属性上的过滤器检索文档。

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"})
```

### 示例 3：对对象使用查询过滤器检索文档 {#example-3-retrieve-documents-with-query-filters-on-objects}

对 location 对象中的 lat 和 lon 字段使用查询过滤器检索文档。

```javascript
db.stores.find({"location.lat": 13.5236, "location.lon": -82.5707})
```

当不使用点 (.) 表示法引用对象内的字段时，查询过滤器应与整个对象完全匹配，包括字段顺序。

```javascript
db.stores.find({"location": {"lat": 13.5236, "lon": -82.5707}})
```

### 示例 4：对数组使用查询过滤器检索文档 {#example-4-retrieve-documents-with-query-filters-on-arrays}

从 promotionEvents 数组中检索 eventName 为 "Grand Bargain Gala" 的文档。

```javascript
db.stores.find({"promotionEvents.eventName": "Grand Bargain Gala"})
```

从嵌套在 promotionEvents 数组中的 "discounts" 数组检索文档，其中 categoryName 为 "Area Rugs"。

```javascript
db.stores.find({"promotionEvents.discounts.categoryName": "Area Rugs"})
```

## 投影 {#projections}

find 命令中的第二个文档指定响应中要投影的字段列表。

### 在响应中包含特定字段或多个字段 {#include-a-specific-field-or-multiple-fields-in-the-response}

非零整数值或布尔值 true 会将字段包含在响应中。

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"location": 1, "sales": 1})
```

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"location": true, "sales": true})
```

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"location": 1, "sales": true})
```

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"location": 1, "sales": -5})
```

这四个查询等价，均指定在服务器响应中包含 "location" 和 "sales" 字段。

```json
{
    "_id": "b5c9f932-4efa-49fd-86ba-b35624d80d95",
    "location": {
        "lat": 13.5236,
        "lon": -82.5707
    },
    "sales": {
        "totalSales": 35346,
        "salesByCategory": [
            {
                "categoryName": "Rulers",
                "totalSales": 35346
            }
        ]
    }
}
```

### 在响应中排除特定字段或多个字段 {#exclude-a-specific-field-or-multiple-fields-in-the-response}

整数值 0 或布尔值 false 会将指定字段从查询响应中排除。

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"promotionEvents": 0, "location": 0, "sales": 0})
```

```javascript
db.stores.find({"name": "Fourth Coffee | Stationery Haven - New Franco"}, {"promotionEvents": false, "location": false, "sales": false})
```

这两个查询等价，并返回以下响应：

```json
{
    "_id": "b5c9f932-4efa-49fd-86ba-b35624d80d95",
    "name": "Fourth Coffee | Stationery Haven - New Franco",
    "staff": {
        "totalStaff": {
            "fullTime": 17,
            "partTime": 5
        }
    }
}
```

> [!NOTE]
> 默认情况下，_id 字段包含在服务器响应中。投影文档不能同时指定要包含和排除的字段，但 _id 字段是唯一的例外：指定要包含的字段时可以排除 _id，反之亦然。

### 投影匹配查询过滤条件的第一个数组元素 {#project-the-first-element-in-an-array-that-matches-the-query-filter-criteria}

"arrayFieldName".$ 命令仅投影数组中第一个匹配指定查询过滤条件的对象。

```javascript
db.stores.find({"promotionEvents.eventName": "Grand Bargain Gala"}, {"promotionEvents.$": true})
```

返回的文档之一仅显示 promotionEvents 数组中 eventName 为 "Grand Bargain Gala" 的第一个元素，而排除数组中的其他所有元素。

```json
{
    "_id": "d7fe6fb9-57e8-471a-b8d2-714e3579a415",
    "promotionEvents": [
        {
            "eventName": "Grand Bargain Gala",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024,
                    "Month": 3,
                    "Day": 25
                },
                "endDate": {
                    "Year": 2024,
                    "Month": 4,
                    "Day": 1
                }
            },
            "discounts": [
                {
                    "categoryName": "Area Rugs",
                    "discountPercentage": 7
                },
                {
                    "categoryName": "Vinyl Flooring",
                    "discountPercentage": 12
                }
            ]
        }
    ]
}
```

### 投影匹配查询过滤条件的数组中特定元素 {#project-specific-elements-in-an-array-that-match-the-query-filter-criteria}

此查询投影 promotionEvents 数组中的 eventName 属性和嵌套的 Year 属性。

```javascript
db.stores.find({"promotionEvents.eventName": "Grand Bargain Gala"}, {"promotionEvents.eventName": true, "promotionEvents.promotionalDates.startDate.Year": true})
```

返回的文档之一显示了指定的数组元素在响应中被投影。

```json
{
    "_id": "d7fe6fb9-57e8-471a-b8d2-714e3579a415",
    "promotionEvents": [
        {
            "eventName": "Grand Bargain Gala",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024
                }
            }
        },
        {
            "eventName": "Grand Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024
                }
            }
        },
        {
            "eventName": "Epic Bargain Bash",
            "promotionalDates": {
                "startDate": {
                    "Year": 2024
                }
            }
        }
    ]
}
```

## 相关内容 {#related-content}

- [使用 DocumentDB 的 insert](/documentdb/reference/commands/query-and-write/insert/)
- [使用 DocumentDB 的 update](/documentdb/reference/commands/query-and-write/update/)

## 实现 {#implementation}

从集合中选择文档并返回游标。后端应用过滤器、投影、排序和结果限制；网关打包首批结果并保留任何剩余的游标状态。

源码：`pg_documentdb/src/aggregation/bson_aggregation_pipeline.c`, `ParseFindQuery`。有关共享请求元数据，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。
