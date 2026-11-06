---
title: "gp_suboverflowed_backend"
description: "The `gp_suboverflowed_backend` view allows administrators to identify sessions in which a backend has subtransaction overflows, which can cause query performance degradation in the system, including catalog queries."
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-suboverflowed-backend.md"
---

|column|type|description|
|------|----|----------|
|`segid`|integer|The id of the segment containing the suboverflowed backend.|
|`pids`|integer[]|A list of the pids of all suboverflowed backends on this segment.|
