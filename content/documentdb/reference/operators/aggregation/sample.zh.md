---
title: $sample
description: DocumentDB 中的 $sample 运算符返回随机选取的若干文档
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$sample.md
weight: 270
translation_source_sha256: 330d7db7695b54352052443703f7ce47f69804537a0acb40ad61ccf9c8818c97
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$sample` 流水线阶段用于在聚合流水线中从集合中随机选择指定数量的文档。`$sample` 命令在测试、数据分析以及为机器学习生成随机数据子集时非常有用。

## 语法 {#syntax}

```javascript
{
  $sample: { size: <number> }
}
```

### 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`size`** | 从集合中随机选择的文档数量 |
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

<span id="example-1-randomly-select-five-documents-and-project-the-corresponding-document-i-ds"></span>

### 示例 1 - 随机选择五个文档并投影对应的文档 ID {#example-1---randomly-select-five-documents-and-project-the-corresponding-document-ids}

```javascript
 db.stores.aggregate([{
     $sample: {
         size: 5
     }
 }, {
     $project: {
         _id: 1
     }
 }])
```

此查询返回以下结果：

```json
[
  { "_id": "f7ae8b40-0c66-4e80-9261-ab31bbabffb4" },
  { "_id": "25350272-6797-4f98-91f8-fe79084755c7" },
  { "_id": "c7fd1d22-1a29-4cb0-9155-1ad71d600c2b" },
  { "_id": "e602b444-9519-42e3-a2e1-b5a3da5f6e64" },
  { "_id": "189c239a-edca-434b-baae-aada3a27a2c5" }
]
```
