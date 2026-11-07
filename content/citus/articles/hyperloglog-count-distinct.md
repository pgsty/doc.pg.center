---
title: Distributed distinct count with HyperLogLog on PostgreSQL
description: Learn how to use HyperLogLog for distributed distinct count on PostgreSQL so you can efficiently estimate unique values.
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/hyperloglog-count-distinct?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
linkTitle: HLL distinct counts
---

**Original article:** [Burak Yucesoy · April 4, 2017](https://www.citusdata.com/blog/2017/04/04/distributed-count-distinct-with-postgresql/).

Running `SELECT COUNT(DISTINCT)` on your database is all too common. Some applications have analytics dashboard highlighting the number of unique items such as unique users, unique products, unique visits. While traditional `SELECT COUNT(DISTINCT)` queries work well in single machine setups, it's a difficult problem to solve in distributed systems. When you have this type of query, you can't push query to the workers and add up results because there are overlapping records in different workers. Instead you can:

- Pull all distinct data to one machine and count there. (Doesn't scale)
- Do a map/reduce. (Scales but it's slow)

Approximation algorithms or sketches help in these scenarios. Sketches are probabilistic algorithms that can generate approximate results efficiently within mathematically provable error bounds. There are a many of them out there, but today we're just going to focus on one, HyperLogLog ([HLL](https://github.com/aggregateknowledge/postgresql-hll)). HLL is effective for estimating unique number of elements in a list. Understanding the internals of the HLL can help show why the HLL algorithm is useful to solve distinct count problem in a scalable way. This article shows how HLL can be applied in a distributed fashion alongside examples of HLL usage.

## What does HLL do behind the curtains? {#what-does-hll-do-behind-the-curtains}

### Hash all elements {#hash-all-elements}

HLL and almost all other probabilistic counting algorithms depend on uniform distribution of the data. Since in the real world, data isn't distributed uniformly, HLL first hashes each element to make the data distribution more uniform. Uniform distribution means that each bit of the element has a 0.5 probability of being 0 or 1. Apart from uniformity, hashing allows HLL to treat all data types same. As long as you have a hash function for your data type, you can use HLL for cardinality estimation.

### Observe the data for rare patterns {#observe-the-data-for-rare-patterns}

After you hash all the elements, HLL looks for the binary representation of each hashed element. HLL mainly finds if there are bit patterns that are less likely to occur. Existence of such rare patterns means that you're dealing with large dataset.

For this purpose, HLL looks number of leading zero bits in the hash value of each element and finds maximum number of leading zero bits. Basically, to be able to observe k leading zeros, you need \(2^{k+1}\) trials (that is, hashed numbers). Therefore, if maximum number of leading zeros is k in a data set, HLL concludes that there are approximately \(2^{k+1}\) distinct elements.

- HLL has a low memory footprint. For maximum number "n," you need to store just *log log n* bits. For example; if you hash elements into 64-bit integers, you just need to store 6 bits to make an estimation. This process saves memory especially compared with approach where you need to remember all the values.
- You only need to do one pass on the data to find maximum number of leading zeros.
- You can work with streaming data. After you calculate the maximum number of leading zeros, if some new data arrives, you can include them into calculation without going over whole data set. You only need to find number of leading zeros of each new element, compare them with maximum number of leading zeros of whole dataset and update maximum number of leading zeros if necessary.
- You can merge estimations of two separate datasets efficiently. You only need to pick bigger number of leading zeros as maximum number of leading zeros of combined dataset. You can then separate the data into shards, estimate their cardinality and merge the results. This action is called additivity, and it allow us to use HLL in distributed systems.

### Stochastic Averaging {#stochastic-averaging}

While these predictions might not be exact, they're always in the form of \(2^k\). Estimates can differ if the data distribution isn't uniform enough.

One possible fix for these problems could be just repeating the process with different hash functions and taking the average. This fix could be effective, but hashing all the data multiple times is expensive. HLL fixes this problem with something called stochastic averaging. Basically, you divide your data into buckets and use the previously mentioned algorithm for each bucket separately. Then you take the average of the results. You use first few bits of the hash value to determine which bucket a particular element belongs to and use remaining bits to calculate maximum number of leading zeros.

Moreover, you can configure precision by choosing number of buckets to divide the data. You need to store *log log n* bits for each bucket. Since you can store each estimation in *log log n* bits, you can create lots of buckets and still use insignificant amount of memory. Having such small memory footprint is especially important while operating on large scale data. To merge two estimations, you merge each bucket then take the average. Therefore, if you plan to do the merge operation, you should keep each bucket's maximum number of leading zeros.

### More? {#more}

HLL does some other things too to increase accuracy of the estimation, however observing bit patterns and stochastic averaging is the key points of HLL. After these optimizations, HLL can estimate cardinality of a dataset with a typical error rate of 2% by using 1.5 kB of memory. You can increase accuracy by using more memory.

## HLL in distributed systems {#hll-in-distributed-systems}

As previously mentioned, HLL has additivity property. This means you can divide your dataset into several parts and operate on them with HLL algorithm to find unique element count of each part. Then you can merge intermediate HLL results efficiently to find unique element count of all data without looking back to original data.

If you work on large scale data and you keep parts of your data in different physical machines, you can use HLL to calculate unique count over all your data without pulling whole data to one place. In fact, Citus can do this operation for you. There's a [HLL extension](https://github.com/aggregateknowledge/postgresql-hll) developed for PostgreSQL, and it's fully compatible with Citus. If you have HLL extension installed and want to run COUNT(DISTINCT) query on a distributed table, Citus automatically uses HLL. You don't need to do anything extra once you configured it.

## Hands on with HLL {#hands-on-with-hll}

> [!NOTE]
> This article mentions the Citus Cloud service. You can no longer onboard to Citus Cloud on Amazon Web Service (AWS). If you're new to Citus, Citus is still available to you. Citus is now open source and in the cloud on Microsoft Azure, as a fully integrated deployment option in Azure Database for PostgreSQL.
> 
> For more information, see [Managed service](/citus/installation/citus-cloud/).

### Setup {#setup}

To use with HLL, use Citus Cloud and GitHub events data. You can see and learn more about Citus Cloud and this data set from [Getting started with GitHub event data on Citus](https://www.citusdata.com/blog/2017/01/27/getting-started-with-github-events-data/). If you created your Citus Cloud instance and connected it via psql, you can create HLL extension by running the following command from the coordinator;

```sql
CREATE EXTENSION hll;
```

Then enable count distinct approximations by setting the `citus.count_distinct_error_rate` configuration value. Lower values for this configuration setting are expected to give more accurate results but take more time and use more memory for computation. You should set this value to 0.005.

```sql
SET citus.count_distinct_error_rate TO 0.005;
```

You can use the `github_events` table.

```psql
CREATE TABLE github_events
(
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    user_id bigint,
    org jsonb,
    created_at timestamp
);

SELECT create_distributed_table('github_events', 'user_id');

\COPY github_events FROM large_events.csv CSV
```

### Examples {#examples}

After distributing the table, you can use a regular COUNT(DISTINCT) query to find out how many unique users created an event;

```sql
SELECT
    COUNT(DISTINCT user_id)
FROM
    github_events;
```

It should return something like this:

```text
    .
     count
    --------
     264227

    (1 row)
```

It looks like this query doesn't have anything with HLL. However if you set `citus.count_distinct_error_rate` to something bigger than 0 and issue `COUNT(DISTINCT)` query; Citus automatically uses HLL. For simple use-cases like this, you don't even need to change your queries. Exact distinct count of users who created an event is 264198, so the error rate is little bigger than 0.0001.

You can also use constraints to filter out some results. For example, you can query number of unique users who created a PushEvent;

```sql
SELECT
    COUNT(DISTINCT user_id)
FROM
    github_events
WHERE
    event_type = 'PushEvent'::text;
```

It would return;

```text
    .
     count
    --------
     157471

    (1 row)
```

Similarly, an exact distinct count for this query is 157154, and the error rate is bigger than 0.002.

### Conclusion {#conclusion}

If you're having trouble scaling `COUNT(DISTINCT)` in PostgreSQL, give HLL a look it might be useful if close enough counts are acceptable.

## Related content {#related-content}

- [Guides overview](/citus/articles/)
- [Real-time event aggregation](/citus/articles/aggregation/)
