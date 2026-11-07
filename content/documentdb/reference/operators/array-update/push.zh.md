---
title: $push
description: $push 运算符向文档中的数组添加指定值。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$push.md
weight: 100
translation_source_sha256: 6219e7730945fe8fded0e9147e3bb48c12a7a56618704c6470e524b1b26fd66b
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 窗口示例提到“不同销售额”，但其中的 `$push` 表达式只是构建列表。示例没有单独的去重操作。

`$push` 运算符用于向文档中的数组添加指定值。$push 运算符会向现有数组添加新元素，而不影响数组中的其他元素。

## 语法 {#syntax}

```javascript
db.collection.update({
    < query >
}, {
    $push: {
        < field >: < value >
    }
}, {
    < options >
})
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<query>`**| 用于选择待更新文档的条件。|
| **`<field>`**| 要向其末尾追加值的数组字段。|
| **`<value>`**| 要追加到数组字段末尾的值。|
| **`<options>`**| 可选。更新操作的附加选项。|
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

<span id="example-1-add-a-new-sales-category"></span>

### 示例 1：添加新的销售类别 {#example-1---add-a-new-sales-category}

要向 salesByCategory 数组添加新的销售类别，可运行查询，对该字段使用 $push 运算符，并提供一个包含类别名称及其销售额的新 Sales 对象。

```javascript
db.stores.update({
    _id: "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"
}, {
    $push: {
        "sales.salesByCategory": {
            categoryName: "Wine Accessories",
            totalSales: 1000.00
        }
    }
})
```

此查询返回以下结果：

```json
[
  {
    "acknowledged": true,
    "insertedId": null,
    "matchedCount": "1",
    "modifiedCount": "1",
    "upsertedCount": 0
  }
]
```

<span id="example-2-using-push-with-set-window-fields"></span>

### 示例 2：结合 $setWindowFields 使用 $push {#example-2---using-push-with-setwindowfields}

要获取 "First Up Consultants" 公司所有商店的不同销售额，先运行查询，对公司内的商店进行分区。然后使用 $push 运算符，创建包含分区内从第一个商店到当前商店销售额的列表。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $setWindowFields: {
        partitionBy: "$company",
        sortBy: {
            "sales.totalSales": -1
        },
        output: {
            salesByStore: {
                $push: "$sales.totalSales",
                window: {
                    documents: ["unbounded", "current"]
                }
            }
        }
    }
}, {
    $project: {
        company: 1,
        salesByStore: 1
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "a0386810-b6f8-4b05-9d60-e536fb2b0026",
        "company": "First Up Consultants",
        "salesByStore": [
            327583
        ]
    },
    {
        "_id": "ad8af64a-d5bb-4162-9bb6-e5104126566d",
        "company": "First Up Consultants",
        "salesByStore": [
            327583,
            288582
        ]
    },
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "company": "First Up Consultants",
        "salesByStore": [
            327583,
            288582,
            279183
        ]
    }
]
```
