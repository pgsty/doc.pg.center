---
title: Clauses
linkTitle: Clauses
description: One page for each graph query clause.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/index.html
upstream_source: agensgraph
upstream_modified: true
cascade:
  type: docs
no_list: true
---


A Cypher or GQL statement is a pipeline of clauses. These pages are grouped by the job a clause does in that pipeline rather than alphabetically; every page has the same shape.

Clauses marked **GQL** come from ISO/IEC 39075. They are accepted wherever a Cypher statement is accepted — there is no separate mode. See [GQL conformance](/agensgraph/appendix/gql-conformance/) for which parts of the standard are supported.

## Reading {#reading}

- [MATCH](/agensgraph/reference/clauses/match/)
- [OPTIONAL MATCH](/agensgraph/reference/clauses/optional-match/)
- [WHERE](/agensgraph/reference/clauses/where/)
- [LOAD FROM](/agensgraph/reference/clauses/load-from/)

## Projecting {#projecting}

- [RETURN](/agensgraph/reference/clauses/return/)
- [WITH](/agensgraph/reference/clauses/with/)
- [LET](/agensgraph/reference/clauses/let/)
- [ORDER BY](/agensgraph/reference/clauses/order-by/)
- [SKIP and LIMIT](/agensgraph/reference/clauses/skip-and-limit/)

## Writing {#writing}

- [CREATE](/agensgraph/reference/clauses/create/)
- [INSERT](/agensgraph/reference/clauses/insert/)
- [MERGE](/agensgraph/reference/clauses/merge/)
- [SET](/agensgraph/reference/clauses/set/)
- [REMOVE](/agensgraph/reference/clauses/remove/)
- [DELETE](/agensgraph/reference/clauses/delete/)

## Composing {#composing}

- [UNWIND](/agensgraph/reference/clauses/unwind/)
- [FOR](/agensgraph/reference/clauses/for/)
- [FILTER](/agensgraph/reference/clauses/filter/)
- [NEXT](/agensgraph/reference/clauses/next/)
- [FINISH](/agensgraph/reference/clauses/finish/)
- [UNION](/agensgraph/reference/clauses/union/)

## Subqueries {#subqueries}

- [CALL](/agensgraph/reference/clauses/call/)
- [CALL … YIELD](/agensgraph/reference/clauses/call-yield/)
- [CALL { subquery }](/agensgraph/reference/clauses/call-subquery/)
- [OPTIONAL CALL](/agensgraph/reference/clauses/optional-call/)
- [Subquery value expressions](/agensgraph/reference/clauses/subquery-expressions/)
