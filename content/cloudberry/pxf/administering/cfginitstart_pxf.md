---
title: "Starting, Stopping, and Restarting PXF"
description: "Starting, stopping, and restarting the PXF service."
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/cfginitstart_pxf.md"
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->


PXF provides two management commands:

- [`pxf cluster`](/cloudberry/pxf/ref/pxf-cluster/) - manage all PXF Service instances in the Apache Cloudberry cluster
- [`pxf`](/cloudberry/pxf/ref/pxf/) - manage the PXF Service instance on a specific Apache Cloudberry host

> <b>Note:</b> The procedures in this topic assume that you have added the <code>&lt;PXF_INSTALL_DIR>/bin</code> directory to your `$PATH`.


## Starting PXF {#starting-pxf}

After configuring PXF, you must start PXF on each host in your Apache Cloudberry cluster. The PXF Service, once started, runs as the `gpadmin` user on default port 5888. Only the `gpadmin` user can start and stop the PXF Service.

If you want to change the default PXF configuration, you must update the configuration before you start PXF, or restart PXF if it is already running. See [About the PXF Configuration Files](/cloudberry/pxf/administering/configuring/config_files/) for information about the user-customizable PXF configuration properties and the configuration update procedure.


### Prerequisites {#prerequisites}

Before you start PXF in your Apache Cloudberry cluster, ensure that:

- Your Apache Cloudberry cluster is up and running.
- You have previously configured PXF.
 
### Procedure {#procedure}

Perform the following procedure to start PXF on each host in your Apache Cloudberry cluster.

1. Log in to the Apache Cloudberry coordinator host:

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

3. Run the `pxf cluster start` command to start PXF on each host:

    ```shell
    gpadmin@coordinator$ pxf cluster start
    ```

## Stopping PXF {#stopping-pxf}

If you must stop PXF, for example if you are upgrading PXF, you must stop PXF on each host in your Apache Cloudberry cluster. Only the `gpadmin` user can stop the PXF Service.

### Prerequisites {#prerequisites-1}

Before you stop PXF in your Apache Cloudberry cluster, ensure that your Apache Cloudberry cluster is up and running.
 
### Procedure {#procedure-1}

Perform the following procedure to stop PXF on each host in your Apache Cloudberry cluster.

1. Log in to the Apache Cloudberry coordinator host:

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

3. Run the `pxf cluster stop` command to stop PXF on each host:

    ```shell
    gpadmin@coordinator$ pxf cluster stop
    ```

## Restarting PXF {#restarting-pxf}

If you must restart PXF, for example if you updated PXF user configuration files in `$PXF_BASE/conf`, you run `pxf cluster restart` to stop, and then start, PXF on all hosts in your Apache Cloudberry cluster.

Only the `gpadmin` user can restart the PXF Service.

### Prerequisites {#prerequisites-2}

Before you restart PXF in your Apache Cloudberry cluster, ensure that your Apache Cloudberry cluster is up and running.
 
### Procedure {#procedure-2}

Perform the following procedure to restart PXF in your Apache Cloudberry cluster.

1. Log in to the Apache Cloudberry coordinator host:

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. Restart PXF:

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```
