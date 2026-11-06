---
title: "About the PXF Deployment Topology"
description: "PXF deployment topologies."
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/deployment_topos.md"
---

The default PXF deployment topology is co-located; you install PXF on each Apache Cloudberry host, and the PXF Service starts and runs on each Apache Cloudberry segment host.

You manage the PXF services deployed in a co-located topology using the [pxf cluster](/cloudberry/pxf/ref/pxf-cluster/) commands.


## Alternate Deployment Topology {#alternate-deployment-topology}

Running the PXF Service on non-Apache Cloudberry hosts is an alternate deployment topology. If you choose this topology, you must install PXF on both the non-Apache Cloudberry hosts and on all Apache Cloudberry hosts.

In the alternate deployment topology, you manage the PXF services individually using the [pxf](/cloudberry/pxf/ref/pxf/) command on each host; you can not use the `pxf cluster` commands to collectively manage the PXF services in this topology.

If you choose the alternate deployment topology, you must explicitly configure each Apache Cloudberry host to identify the host and listen address on which the PXF Service is running. These procedures are described in [Configuring the Host](/cloudberry/pxf/administering/advanced-config/cfghostport/#configuring-the-host) and [Configuring the Listen Address](/cloudberry/pxf/administering/advanced-config/cfghostport/#configuring-the-listen-address).
