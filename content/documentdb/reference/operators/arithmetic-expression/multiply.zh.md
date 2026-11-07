---
title: $multiply
description: $multiply 运算符对输入的数值进行乘法运算
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/arithmetic-expression/$multiply.md
weight: 100
translation_source_sha256: 0d2cfcb559b43201448721748d9e003d9d48da29fcd17e11c5e8d6c2679ff13e
translation_review: AI-assisted bilingual review; 2026-11-07
---

`$multiply` 运算符计算指定输入数值的乘积。

## 语法 {#syntax}

```javascript
{
  $multiply: [ <listOfValues> ]
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
|**`<listOfValues>`**| 用逗号分隔的数值列表。
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

### 示例 1：将字段乘以常量 {#example-1-multiply-a-field-by-a-constant}

要将名为“First Up Consultants”的公司旗下所有门店的总销售额翻倍，首先运行一个查询以筛选公司名称。然后，在 totalSales 字段上使用 $multiply 运算符，返回所需结果。

```javascript
db.stores.aggregate([{
    $match: {
        company: {
            $in: ["First Up Consultants"]
        }
    }
}, {
    $project: {
        company: 1,
        "sales.revenue": 1,
        salesVolumeDoubled: {
            $multiply: ["$sales.revenue", 2]
        }
    }
}])
```

此查询返回的前三个结果如下：

```json
[
    {
        "_id": "39acb3aa-f350-41cb-9279-9e34c004415a",
        "sales": {
            "revenue": 279183
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 558366
    },
    {
        "_id": "26afb024-53c7-4e94-988c-5eede72277d5",
        "sales": {
            "revenue": 50000
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 100000
    },
    {
        "_id": "62438f5f-0c56-4a21-8c6c-6bfa479494ad",
        "sales": {
            "revenue": 68508
        },
        "company": "First Up Consultants",
        "salesVolumeDoubled": 137016
    }
]
```

## 限制条件 {#limitations}

- `$multiply` 运算符仅适用于数值表达式。对非数值值使用该运算符将导致错误。
- 处理大数值或浮点数运算时，请注意溢出或精度问题。
