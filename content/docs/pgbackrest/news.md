---
title: "News"
linkTitle: "News"
weight: 10
description: "Official pgBackRest project news, release announcements, and maintenance updates."
icon: fa-solid fa-newspaper
module: [PGBACKREST]
categories: [Reference]
---

> Source: <https://pgbackrest.org/news.html>

--------

## New Distribution Tarball {#distribution-tarball}

**July 20, 2026**

Starting with pgBackRest 2.59.0, every release includes a distribution tarball that makes building from source simpler. Unlike a checkout of the git repository, the tarball ships the generated source and the rendered documentation pre-built, so pgBackRest builds and installs without the code generation or documentation tooling that a repository checkout requires.

The tarball contains the pgBackRest source with the pre-generated code, the command reference man page, the HTML documentation, and a smoke test to verify the build. It builds with meson and ninja using only the usual pgBackRest libraries.

The tarball is attached to each release as an asset named `pgbackrest-{version}.tar.gz`, along with a matching `.sha256sum` checksum. Download it from the [releases](https://github.com/pgbackrest/pgbackrest/releases) page on GitHub, then see the `README.md` in the tarball for build and test instructions.

Packagers are encouraged to build from the distribution tarball to avoid the extra build tooling that generating code and documentation will require in future releases.


--------

## pgBackRest 2.59.0 Released {#release-2-59-0}

**July 20, 2026**

The pgBackRest community is pleased to announce the release of [pgBackRest](https://pgbackrest.org) 2.59.0, the latest version of the reliable, easy-to-use backup and restore solution that can seamlessly scale up to the largest databases and workloads.

pgBackRest supports a robust set of features for managing your backup and recovery infrastructure, including: parallel backup/restore, full/differential/incremental backups, block incremental backup, multiple repositories, delta restore, parallel asynchronous archiving, malware/ransomware protection, per-file checksums, page checksums (when enabled) validated during backup, multiple compression types, encryption, partial/failed backup resume, backup from standby, tablespace and link support, S3/Azure/GCS/SFTP support, backup expiration, local/remote operation via SSH or TLS, flexible configuration, and more.

pgBackRest can be installed from the [PostgreSQL Yum Repository](https://yum.postgresql.org) or the [PostgreSQL APT Repository](https://apt.postgresql.org) and packages are also available for many other distributions. Source code can be downloaded from [releases](/docs/pgbackrest/release/).

### Significant New Features and Improvements {#feature}

- PostgreSQL 19 support (David Steele)
- Add `archive-expire-before` option to clean up WAL archive (Stefan Fercot)
- Add support for S3 Outposts (Shiva Kumar Ambigi)
- Add S3 process authentication (David Steele)
- Add user/group caching for faster manifest build (Gunnar Lindholm)
- Reconnect SFTP storage after the server drops an idle connection (David Steele)
- Add per-repo backup progress to `info` command output (Will Morland)
- Add batch delete for Azure storage (David Steele)
- Add `backup.info` checks to `verify` command (Denis Garsh)
- Allow the S3 STS endpoint to be configured (Simon Gratton)
- Add systemd notify integration (Andrew Jackson)
- Error when running as root unless `allow-root` is enabled (David Steele)
- Exit async `archive-push` on first error (David Steele)

See the [2.59.0 Release Notes](/docs/pgbackrest/release/#v2590-release-notes) for additional features and improvements.

### Important Notes {#note}

- Only the `restore` command may be run as root by default. Use `allow-root` to run other commands as root (though this is not recommended).
- A new distribution tarball with pregenerated documentation, man page, and code is attached to each release to simplify packaging. See [New Distribution Tarball](#distribution-tarball) for more information.
- There is a new optional dependency on `libsystemd`.

### Links {#link}

- [Website](/docs/pgbackrest/)
- [User Guides](/docs/pgbackrest/user-guide/)
- [Release Notes](/docs/pgbackrest/release/)

### Sponsorship {#sponsorship}

This release was made possible by the generous sponsorship of [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com), and [Data Egret](https://dataegret.com/).


--------

## pgBackRest Will Continue! {#will-continue}

**May 18, 2026**

I am pleased to announce that pgBackRest will continue! Over the last few weeks, a coalition of sponsors has come together to fund ongoing development. Their support means the project is no longer reliant on a single sponsor, giving pgBackRest the stability it needs for the long term.

I'd like to thank each of our sponsors:

[Amazon Web Services](https://aws.amazon.com) provides on-demand cloud computing resources to individuals, companies, and governments. Access computing power, storage, databases, machine learning, and over 200 services, paying only for what you use. Built to grow with you, investing in the communities we share.

[Supabase](https://supabase.com), a complete backend platform built on PostgreSQL, enables developers to build and scale applications quickly without managing infrastructure. It includes a Postgres database, user authentication, real-time subscriptions, file storage, edge functions, and serverless functions, all backed by an active open-source community.

[pgEdge](https://pgedge.com) is an enterprise-class open source Postgres platform for AI, high availability and more, with Agentic AI native tooling and DBA workbench, monitoring and incident response, flexible deployment, and zero downtime maintenance. It scales from a single node to active-active multi-master within the cloud, on-premises, or air-gapped environments.

[Tiger Data](https://tigerdata.com), the creators of TimescaleDB, develops the open-source time-series database built on PostgreSQL and operates Tiger Cloud, a managed platform for time-series, analytics, and AI workloads. Both self-managed and cloud options enable organizations to capture, store, and analyze time-series data at scale, from edge to centralized cloud deployments.

[Percona](https://percona.com) is an open source database software, support, and services company focused on helping organizations maintain full control over their data infrastructure. They help businesses run MySQL, PostgreSQL, MongoDB, Valkey, and Redis securely and efficiently through freely available open source software, 24/7 expert support, and hands-on database expertise.

[Eon.io](https://eon.io) is an intelligent cloud infrastructure for backup, recovery, and data management that helps teams store and access backups more efficiently, making data accessible for analytics and AI workflows. It offers fast, granular recovery and significantly lower storage costs for Postgres and data-intensive workloads across all clouds, including recovery from accidental data loss and AI agent regressions.

These organizations rely on pgBackRest to provide reliable disaster recovery for their products and customers. Their investment reflects the critical role that pgBackRest plays in the PostgreSQL ecosystem, and their collective support ensures the project's long-term sustainability.

I'm looking forward to getting back to work. There are features and optimizations in the pipeline that I'm excited to share in upcoming releases. Thank you to our sponsors for making this possible, and thank you to the community for your patience and support during this transition.


--------

## Maintenance Update {#maintenance-update}

**May 4, 2026**

After I announced that I am no longer maintaining pgBackRest my inbox blew up. It took a while to sort through the messages — many of them were well wishes and thank-yous for my work over the years.

But a pattern soon emerged. It is clear that many pgBackRest users, especially those with pgBackRest users of their own to support, would prefer the project to continue with me as the primary maintainer. I would like nothing more, but after months of fundraising I had just decided it wasn't going to happen.

Now the situation has changed, and it appears all but certain that I will be able to secure enough funding to continue the project. This time pgBackRest will be funded by a coalition of sponsors so that a single acquisition will no longer affect my ability to continue work on the project. We should also be able to bring on another maintainer to distribute the workload and provide continuity in the future.

I know this has been a shock and there is a lot of uncertainty. Please be patient — the current version of pgBackRest works, and there are no critical outstanding bugs or security issues so there is no need to immediately fork the project.

I expect to make a more definitive announcement by the end of the week. Until then, please hold tight and know that we are actively working to revive pgBackRest.


--------

## pgBackRest Is No Longer Being Maintained {#no-longer-maintained}

**April 27, 2026**

TL;DR: pgBackRest is no longer being maintained. If you fork pgBackRest, please select a new name for your project.

After a lot of thought, I have decided to stop working on pgBackRest. I did not come to this decision lightly. pgBackRest has been my passion project for the last thirteen years, and I was fortunate to have corporate sponsorship for much of this time, but there were also many late nights and weekends as I worked to make pgBackRest the project it is today, aided by numerous contributors. Every open-source developer knows exactly what I mean and how much of your life gets devoted to a special project.

Since Crunchy Data was sold, I have been maintaining pgBackRest and looking for a position that would allow me to continue the work, but so far I have not been successful. Likewise, my efforts to secure sponsorship have also fallen far short of what I need to make the project viable.

Like everyone else, I need to make a living, and the range of pgBackRest-related roles is very limited. I can now consider a wider variety of opportunities, but those will not leave me time to work on pgBackRest, which requires a fair amount of time for maintenance, bug fixes, PR reviews, answering issues, etc. That does not even include time to write new features, which is what I really love to do. Rather than do the work poorly and/or sporadically, I think it makes more sense to have a hard stop.

I imagine at some point pgBackRest will be forked, but that will be a new project with new maintainers, and they will need to build trust the same way we did.

Again, many thanks to all the pgBackRest contributors over the years. It was a pleasure working with you!
