---
title: $addToSet
description: addToSet 运算符会在元素不存在时将其添加到数组中，同时确保集合内元素的唯一性。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/array-update/$addtoset.md
weight: 40
translation_source_sha256: 2424a95401c1742ed881966dfa42c9a5b24b5ff2513ef5a0a29d28219abc89ca
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 编者注
> 示例 3 的标题写的是 `$setWindowOperators`，说明写的是 `$addToSet`，但代码实际在 `$setWindowFields` 中使用 `$push`。这段代码并未演示用 `$addToSet` 去重。

`$addToSet` 运算符会向数组中添加元素，前提是这些元素尚不存在，同时确保集合内元素的唯一性。

## 语法 {#syntax}

```javascript
{
  $addToSet: { <field1>: <value1> }
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<field1>`** | 要添加元素的字段。 |
| **`<value1>`** | 要添加到数组中的值。 |
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

### 示例 1：向 `tag` 数组中添加新的标签 {#example-1-add-a-new-tag-to-the-tag-array}

此查询将新标签添加到标签数组中；运行查询时，使用 $addToSet 运算符添加新值。

```javascript
db.stores.updateOne({
    _id: "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"
}, {
    $addToSet: {
        tag: "#ShopLocal"
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
    "modifiedCount": "0",
    "upsertedCount": 0
  }
]
```

<span id="example-2-adding-a-new-promotional-event-to-the-promotion-events-array"></span>

### 示例 2：向 `promotionEvents` 数组中添加新的促销活动 {#example-2-adding-a-new-promotional-event-to-the-promotionevents-array}

此查询将新活动添加到 `promotionEvents` 数组中；运行查询时，使用 $addToSet 运算符，并传入要添加的新促销对象。

```javascript
db.stores.updateOne({
    _id: "0fcc0bf0-ed18-4ab8-b558-9848e18058f4"
}, {
    $addToSet: {
        promotionEvents: {
            eventName: "Summer Sale",
            promotionalDates: {
                startDate: {
                    Year: 2024,
                    Month: 6,
                    Day: 1
                },
                endDate: {
                    Year: 2024,
                    Month: 6,
                    Day: 15
                }
            },
            discounts: [{
                categoryName: "DJ Speakers",
                discountPercentage: 20
            }]
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

<span id="example-3-using-add-to-set-with-set-window-operators"></span>

### 示例 3：结合 $setWindowOperators 使用 $addToSet {#example-3---using-addtoset-with-setwindowoperators}

要获取 "First Up Consultants" 公司中每个商店对应的城市列表，先运行查询，按公司对商店分区。然后使用 $addToSet 运算符，将分区内各商店所在的城市去重后添加到列表中。

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
            citiesForCompany: {
                $push: "$city",
                window: {
                    documents: ["unbounded", "current"]
                }
            }
        }
    }
}, {
    $project: {
        company: 1,
        name: 1,
        citiesForCompany: 1
    }
}])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "a1713bed-4c8b-46e7-bb68-259045dffdb4",
        "name": "First Up Consultants | Bed and Bath Collection - Jaskolskiside",
        "company": "First Up Consultants",
        "citiesForCompany": [
            "South Thelma",
            "South Carmenview",
            "Port Antone",
            "Charlotteville",
            "South Lenorafort",
            "Jaskolskiside"
        ]
    },
    {
        "_id": "6b8585ab-4357-4da7-8625-f6a1cd5796c5",
        "name": "First Up Consultants | Computer Depot - West Zack",
        "company": "First Up Consultants",
        "citiesForCompany": [
            "South Thelma",
            "South Carmenview",
            "Port Antone",
            "Charlotteville",
            "South Lenorafort",
            "Jaskolskiside",
            "West Zack"
        ]
    }
]
```
