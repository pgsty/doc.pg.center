---
title: "Apache Cloudberry 范围函数和操作符"
linkTitle: "范围函数和操作符"
description: "下表列出范围类型可用的操作符。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/range-functions-and-operators.md"
---

|操作符|描述|示例|结果|
|--------|-----------|-------|------|
|`=`|相等|`int4range(1,5) = '[1,4]'::int4range`|`t`|
|`<>`|不相等|`numrange(1.1,2.2) <> numrange(1.1,2.3)`|`t`|
|`<`|小于|`int4range(1,10) < int4range(2,3)`|`t`|
|`>`|大于|`int4range(1,10) > int4range(1,5)`|`t`|
|`<=`|小于或等于|`numrange(1.1,2.2) <= numrange(1.1,2.2)`|`t`|
|`>=`|大于或等于|`numrange(1.1,2.2) >= numrange(1.1,2.0)`|`t`|
|`@>`|包含范围|`int4range(2,4) @> int4range(2,3)`|`t`|
|`@>`|包含元素|`'[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::timestamp`|`t`|
|`<@`|范围被包含于|`int4range(2,4) <@ int4range(1,7)`|`t`|
|`<@`|元素被包含于|`42 <@ int4range(1,7)`|`f`|
|`&&`|重叠（有共同的点）|`int8range(3,7) && int8range(4,12)`|`t`|
|`<<`|严格位于左侧|`int8range(1,10) << int8range(100,110)`|`t`|
|`>>`|严格位于右侧|`int8range(50,60) >> int8range(20,30)`|`t`|
|`&<`|不超出其右侧|`int8range(1,20) &< int8range(18,20)`|`t`|
|`&>`|不超出其左侧|`int8range(7,20) &> int8range(5,10)`|`t`|
|`-\|-`|与之相邻|`numrange(1.1,2.2) -\|- numrange(2.2,3.3)`|`t`|
|`+`|并集|`numrange(5,15) + numrange(10,20)`|`[5,20)`|
|`*`|交集|`int8range(5,15) * int8range(10,20)`|`[10,15)`|
|`-`|差集|`int8range(5,15) - int8range(10,20)`|`[5,10)`|

简单比较操作符 `<`、`>`、`<=` 和 `>=` 首先比较下界，只有下界相等时才比较上界。这些比较对于范围通常用处不大，提供它们是为了允许在范围上构建 B-树索引。

只要涉及空范围，左于、右于和相邻操作符就始终返回 false；也就是说，空范围既不被视为位于任何其他范围之前，也不被视为位于其后。

如果结果范围需要包含两个不相交的子范围，并集和差集操作符就会失败，因为这种范围无法表示。

下表列出范围类型可用的函数。

|函数|返回类型|描述|示例|结果|
|--------|-----------|-----------|-------|------|
|`lower(anyrange)`|范围的元素类型|范围的下界|`lower(numrange(1.1,2.2))`|`1.1`|
|`upper(anyrange)`|范围的元素类型|范围的上界|`upper(numrange(1.1,2.2))`|`2.2`|
|`isempty(anyrange)`|`boolean`|范围是否为空？|`isempty(numrange(1.1,2.2))`|`false`|
|`lower_inc(anyrange)`|`boolean`|是否包含下界？|`lower_inc(numrange(1.1,2.2))`|`true`|
|`upper_inc(anyrange)`|`boolean`|是否包含上界？|`upper_inc(numrange(1.1,2.2))`|`false`|
|`lower_inf(anyrange)`|`boolean`|下界是否为无穷？|`lower_inf('(,)'::daterange)`|`true`|
|`upper_inf(anyrange)`|`boolean`|上界是否为无穷？|`upper_inf('(,)'::daterange)`|`true`|
|`range_merge(anyrange, anyrange)`|`anyrange`|包含给定两个范围的最小范围|`range_merge('[1,2)'::int4range, '[3,4)'::int4range)`|`[1,4)`|

如果范围为空或所请求的界限为无穷，`lower` 和 `upper` 函数返回空值。对于空范围，`lower_inc`、`upper_inc`、`lower_inf` 和 `upper_inf` 函数均返回 false。
