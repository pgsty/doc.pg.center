---
title: $objectToArray
description: objectToArray 命令用于将文档（对象）转换为键值对数组。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/object-expression/$objectToArray.md
weight: 20
translation_source_sha256: 5b7e1387400f0da3e30d8aca35500a1155f0251329ed1bf150116d77eddb9fba
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$objectToArray` 运算符用于将文档（对象）转换为键值对数组。结果数组中的每个键值对都表示为一个包含 `k` 和 `v` 字段的文档。需要操作或分析集合中文档的结构时，可使用此运算符。

## 语法 {#syntax}

```javascript
{
  $objectToArray: <object>
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`<object>`** | 要转换为键值对数组的文档（对象）。 |
{.fields}

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

### 示例 1：转换 `location` 对象 {#example-1-transforming-the-location-object}

此查询将 `location` 对象转换为键值对数组。

```javascript
db.stores.aggregate([
  {
    $project: {
      locationArray: { $objectToArray: "$location" }
    }
  },
  {
    $limit: 2  // Limit output to first 5 documents
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "locationArray": [
      {
        "k": "lat",
        "v": -74.0427
      },
      {
        "k": "lon",
        "v": 160.8154
      }
    ]
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "locationArray": [
      {
        "k": "lat",
        "v": 61.3945
      },
      {
        "k": "lon",
        "v": -3.6196
      }
    ]
  }
]
```

<span id="example-2-transforming-the-sales-by-category-array"></span>

### 示例 2：转换 `salesByCategory` 数组 {#example-2-transforming-the-salesbycategory-array}

要转换 `salesByCategory` 数组，先展开该数组，再应用 `$objectToArray` 运算符。

```javascript
db.stores.aggregate([
  { $unwind: "$sales.salesByCategory" },
  {
    $project: {
      salesByCategoryArray: { $objectToArray: "$sales.salesByCategory" }
    }
  },
  { 
    $limit: 2
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
    "_id": "a715ab0f-4c6e-4e9d-a812-f2fab11ce0b6",
    "salesByCategoryArray": [
      {
        "k": "categoryName",
        "v": "Stockings"
      },
      {
        "k": "totalSales",
        "v": 25731
      }
    ]
  },
  {
    "_id": "923d2228-6a28-4856-ac9d-77c39eaf1800",
    "salesByCategoryArray": [
      {
        "k": "categoryName",
        "v": "Lamps"
      },
      {
        "k": "totalSales",
        "v": 19880
      }
    ]
  }
]
```

需要动态处理字段名称时，常将子文档转换为键值对，尤其适用于以下情况：
- 构建通用流水线。
- 将字段名称映射到键值结构，以便灵活转换或进一步处理。
