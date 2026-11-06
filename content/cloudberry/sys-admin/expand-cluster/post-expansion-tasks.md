---
title: "Post Expansion Tasks"
description: "After the expansion is completed, you must perform different tasks depending on your environment."
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/post-expansion-tasks.md"
---

- [Removing the Expansion Schema](#remove-the-expansion-schema)
- [Setting Up PXF on the New Host](#set-up-pxf-on-the-new-host)

## Remove the expansion schema {#remove-the-expansion-schema}

You must remove the existing expansion schema before you can perform another expansion operation on the Cloudberry system.

You can safely remove the expansion schema after the expansion operation is complete and verified. To run another expansion operation on a Cloudberry system, first remove the existing expansion schema.

1. Log in on the coordinator host as the user who will be running your Apache Cloudberry system (for example, `gpadmin`).
2. Run the `gpexpand` utility with the `-c` option. For example:

    ```shell
    $ gpexpand -c
    ```

    > [!NOTE]
    > Some systems require you to press Enter twice.

## Set up PXF on the new host {#set-up-pxf-on-the-new-host}

> [!TIP]
> You can visit [PXF](https://cloudberry.apache.org/pxf) guides for more details.

If you are using PXF in your Apache Cloudberry cluster, you must perform some configuration steps on the new hosts.

There are different steps to follow depending on your PXF version and the type of installation.

### Apache Cloudberry PXF 2.x {#apache-cloudberry-pxf-2x}

- You must install the same version of the PXF `rpm` or `deb` on the new hosts.
- Log into the Cloudberry Coordinator and run the following commands:

    ```shell
    gpadmin@gpcoordinator$ pxf cluster register
    gpadmin@gpcoordinator$ pxf cluster sync
    ```
