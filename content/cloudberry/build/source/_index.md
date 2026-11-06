---
title: "Build Apache Cloudberry from Source: Complete Guide"
linkTitle: "Build from Source (Complete Guide)"
description: "This document is intended for developers interested in exploring and potentially contributing to Apache Cloudberry."
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/index.md"
---

The build environment described here is optimized for development and testing purposes only.

## Target audience {#target-audience}

- Developers interested in contributing to Apache Cloudberry.
- PostgreSQL developers wanting to explore Cloudberry's extensions.
- Database enthusiasts interested in learning about distributed query processing.
- Anyone considering joining the Apache Cloudberry community.

The build process described here enables development activities such as:

- Debugging and testing new features.
- Exploring the codebase with development tools.
- Running test suites and validation checks.
- Making and testing code modifications.

> [!TIP]
> If you are new to Apache Cloudberry or PostgreSQL development:
>
> - Consider building PostgreSQL first to understand the basic workflow
> - Join the project's [mailing lists](https://cloudberry.apache.org/community/mailing-lists) to connect with other developers
> - Review the project's issue tracker to understand current development priorities
> - Be prepared for longer build times and iterative testing as you explore the codebase

## Process of building Apache Cloudberry {#process-of-building-apache-cloudberry}

The build process for Apache Cloudberry (Incubating) closely resembles that of PostgreSQL. If you have previously set up development environments for PostgreSQL, you'll find the steps for Cloudberry very familiar.

For those new to Cloudberry or PostgreSQL, we recommend starting with a PostgreSQL build first. The PostgreSQL development community has established excellent documentation and tooling to guide you through the process. Familiarizing yourself with PostgreSQL's build process will make transitioning to Cloudberry significantly easier.

## Prerequisites {#prerequisites}

### Provision a Rocky Linux 8+ / Ubuntu 22.04+ Environment {#provision-a-rocky-linux-8--ubuntu-2204-environment}

> [!NOTE]
> Since Apache Cloudberry 2.2, Ubuntu 20.04 support has been dropped, and support for Rocky Linux 10 and Ubuntu 24.04 has been added.

- Use any platform to create a virtual machine or container:

    - **Cloud providers**: You can use the Rocky Linux 8+ or Ubuntu 22.04+ images provided by the cloud providers, such as AWS, Google Cloud, Microsoft Azure, and more.
    - **VirtualBox**: Use the official [Rocky Linux 8+](https://rockylinux.org/download) / [Ubuntu 22.04+](https://ubuntu.com/download) ISO or Vagrant boxes.
    - **Docker**: These instructions were validated under Rocky Linux 8+ and Ubuntu 22.04 official base docker images, but should work with any of their based container.
      - For example, you can run the following command to start a Rocky Linux 8 container:

        ```bash
        docker run -it --shm-size=2gb -h cdw rockylinux/rockylinux:8

        # Start a Ubuntu 22.04 container:
        # docker run -it --shm-size=2gb -h cdw ubuntu:22.04
        ```

        The hostname `cdw` (Coordinator Data Warehouse) is just an example of how we started the container for testing.

        To ensure test suites run successfully, you may need to increase the container's shared memory using `--shm-size=2gb`. Test failures can occur when the Cloudberry cluster lacks sufficient shared memory resources.

- Ensure the VM or container has:
    - Internet connectivity for package installation.
    - SSH or console access for user interaction.
    - Sufficient resources (CPU, memory, and storage) for a development environment.

> [!NOTE]
> Specific steps to provision the environment are not covered in this guide because they vary by platforms. This guide assumes you have successfully created a VM or container and can log in as the default user (for example, `rocky` for Rocky Linux on AWS).

### System requirements {#system-requirements}

Minimum requirements for development environment:

- CPU: 4 cores recommended (2 cores minimum)
  - CPU architecture: x86, x86_64, ARM, MIPS
- RAM: 8GB recommended (4GB minimum)
- Storage: 20GB free space recommended
- Network: Broadband internet connection for package downloads

## Build Apache Cloudberry from source code {#build-apache-cloudberry-from-source-code}

The following steps guide you through building Apache Cloudberry from source code on Rocky Linux 8+ or Ubuntu 22.04+. The process is similar for both operating systems, with minor differences in package management, dependencies and software versions between these two distributions.

Just go ahead and follow the steps below to build Apache Cloudberry from source code:
