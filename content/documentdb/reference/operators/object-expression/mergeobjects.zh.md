---
title: $mergeObjects
description: $mergeObjects 运算符将多个文档合并为一个文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/object-expression/$mergeobjects.md
weight: 10
translation_source_sha256: ff14aaa36311ad4f8e5b31e5b5f5f642e931f6835e9d6da4f1cb4b1a11083fb2
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 标题称按 sales 子文档分组，而说明和代码按城市分组，再合并各组中的 sales 子文档。代码末尾注释写的是三个城市，但实际限制为两个。

`$mergeObjects` 运算符将多个文档合并为一个文档。mergeObjects 操作用于聚合流水线，可合并来自不同文档的字段，或向已有文档添加一个或多个字段。发生冲突时，该运算符使用源文档中的字段覆盖目标文档中的字段。

## 语法 {#syntax}

```javascript
{
  $mergeObjects: [ < document1 > , < document2 > , ...]
}
```

## 参数 {#parameters}

| 参数 | 说明 |
| --- | --- |
| **`document1, document2`** | 要合并的文档。可以用字段路径、子文档或常量指定。 |
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

<span id="example-1-merging-documents-as-an-accumulator-to-group-documents-by-the-sales-subdocument"></span>

### 示例 1 - 将文档合并操作用作累加器，按 sales 子文档对文档分组 {#example-1---merging-documents-as-an-accumulator-to-group-documents-by-the-sales-subdocument}

此查询针对指定公司，按城市合并所有 sales 子文档。

```javascript
db.stores.aggregate([
  {
    $match: {
      company: "Fourth Coffee"
    }
  },
  {
    $group: {
      _id: "$city",
      mergedSales: {
        $mergeObjects: "$sales"
      }
    }
  },
  {
    $limit: 2   // returns only the first 3 grouped cities
  }
])
```

此查询返回的前两个结果如下：

```json
[
  {
      "_id": "Jalonborough",
      "mergedSales": {
          "totalSales": 45747,
          "salesByCategory": [
              {
                  "categoryName": "Bucket Bags",
                  "totalSales": 45747
              }
          ]
      }
  },
  {
      "_id": "Port Vladimir",
      "mergedSales": {
          "totalSales": 32000,
          "salesByCategory": [
              {
                  "categoryName": "DJ Speakers",
                  "totalSales": 24989
              },
              {
                  "categoryName": "DJ Cables",
                  "totalSales": 7011
              }
          ]
      }
  }
]
```
