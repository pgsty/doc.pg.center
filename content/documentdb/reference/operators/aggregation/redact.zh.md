---
title: $redact
description: $redact 运算符根据访问权限过滤文档内容。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/operators/aggregation/$redact.md
weight: 240
translation_source_sha256: 6fc154b7d55421c4b27464b7b47ae3840b9a24576b0a19adfe04ee1e6cddfa7a
translation_review: AI-assisted bilingual review; 2026-11-07
---

聚合流水线中的 `$redact` 流水线阶段用于根据访问权限或其他条件动态过滤集合中文档的字段。该阶段会处理流水线中的每个文档，并根据指定逻辑保留或移除字段。

## 语法 {#syntax}

```javascript
{
  $redact: <expression>
}
```

## 参数 {#parameters}

| 参数 | 描述 |
| --- | --- |
| **`<expression>`** | 一个有效的 MongoDB 表达式，其求值结果为以下之一：`$$DESCEND`、`$$PRUNE` 或 `$$KEEP`。这些变量决定了是否保留字段、移除字段，或继续深入文档内部进行遍历。 |
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

### 示例 1：屏蔽敏感信息 {#example-1-redacting-sensitive-information}

此查询会筛选出促销活动中 `discountPercentage` 超过 15% 的文档的 `promotionEvents` 字段。

```javascript
db.stores.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $gt: ["$promotionEvents.discounts.discountPercentage", 15]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```

此查询返回的前两个结果如下：

```json
[
    {
        "_id": "new-store-001",
        "name": "Adatum Corporation - Downtown Branch",
        "sales": {
            "totalSales": 5000
        },
        "createdDate": "2025-06-11T11:11:32.262Z",
        "status": "new",
        "staff": {
            "totalStaff": {
                "fullTime": 0,
                "partTime": 0
            }
        },
        "version": 1,
        "storeOpeningDate": "2025-06-11T11:11:32.262Z",
        "storeFeatures": 213
    },
    {
        "_id": "gaming-store-mall-001",
        "name": "Trey Research | Gaming Paradise - Mall Location",
        "location": {
            "lat": 35.6762,
            "lon": 139.6503
        },
        "createdDate": "2025-06-11T11:13:27.180Z",
        "status": "active",
        "staff": {
            "totalStaff": {
                "fullTime": 8,
                "partTime": 12
            },
            "manager": "Alex Johnson",
            "departments": [
                "gaming",
                "accessories",
                "repairs"
            ]
        },
        "sales": {
            "totalSales": 0,
            "salesByCategory": []
        },
        "operatingHours": {
            "weekdays": "10:00-22:00",
            "weekends": "09:00-23:00"
        },
        "metadata": {
            "version": 1,
            "source": "store-management-system"
        },
        "storeOpeningDate": "2025-06-11T11:11:32.262Z",
        "storeFeatures": 189
    }
]
```

### 示例 2：基于标签限制访问 {#example-2-restricting-access-based-on-tags}

此查询会移除所有包含标签 `#MembershipDeals` 的文档。

```javascript
db.stores.aggregate([
  {
    $redact: {
      $cond: {
        if: {
          $in: ["#MembershipDeals", "$tag"]
        },
        then: "$$PRUNE",
        else: "$$DESCEND"
      }
    }
  }
])
```
