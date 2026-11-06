---
title: "Upgrading PXF"
description: "PXF upgrade paths and considerations."
weight: 100
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/upgrade/upgrade_landing.md"
---

When you install a newer version of PXF, perform the upgrade actions described in:

- [Upgrading PXF](/cloudberry/pxf/upgrade/upgrade_pxf_rpm/)

Additionally, review [OS Upgrade Considerations for PXF](/cloudberry/pxf/upgrade/upgrade_os/) if you are planning to upgrade the operating system on your Apache Cloudberry cluster hosts.

If you plan to perform an in-place major-version upgrade of Apache Cloudberry itself with `cbupgrade`, see the forward-looking [PXF Pre-Upgrade Actions](/cloudberry/pxf/upgrade/pxf_gpupgrade_pre/) and [PXF Post-Upgrade Actions](/cloudberry/pxf/upgrade/pxf_gpupgrade_post/). Note that `cbupgrade` is still under development and is not supported yet.
