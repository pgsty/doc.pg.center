---
title: "Apache Cloudberry Deployment"
linkTitle: "Deploy in Production"
description: "This guide provides instructions for deploying Apache Cloudberry in production environments."
weight: 30
icon: "fa-solid fa-server"
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/index.md"
---

It covers the full deployment lifecycle from hardware planning to cluster initialization and login.

The guide includes the following topics:

- **[Platform Requirements](/cloudberry/deployment/platform-requirements/)** — Hardware and software requirements for Apache Cloudberry hosts.
- **[Estimating Storage Capacity](/cloudberry/deployment/capacity_planning/)** — How to estimate disk space needed for your data.
- **[Configuring Your Systems](/cloudberry/deployment/prepare-to-deploy/)** — OS-level configuration including kernel parameters, SELinux, firewall, NTP, and user setup.
- **[Deploy Using RPM/DEB Package](/cloudberry/deployment/install_cloudberry/)** — Installing the Apache Cloudberry software on all hosts.
- **[Creating the Data Storage Areas](/cloudberry/deployment/create_data_dirs/)** — Setting up data directories for coordinator and segment instances.
- **[Validating Hardware and Network](/cloudberry/deployment/validate/)** — Verifying network, disk I/O, and memory bandwidth performance.
- **[Initialize Apache Cloudberry](/cloudberry/deployment/init_cloudberry/)** — Initializing the database cluster using `gpinitsystem`.
- **[Logging into Apache Cloudberry](/cloudberry/deployment/login_cloudberry/)** — Connecting to the database after deployment.
- **[Deploy with a Single Computing Node](/cloudberry/deployment/single-node/)** — Deploying Apache Cloudberry without segment nodes for development or testing.
