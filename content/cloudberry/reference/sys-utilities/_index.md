---
title: "Utility Overview"
linkTitle: "System Utilities"
description: "The command-line utilities provided with Apache Cloudberry."
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/index.md"
---

Apache Cloudberry uses the standard PostgreSQL client and server programs and provides additional management utilities for administering a distributed Apache Cloudberry DBMS.

Several utilities are installed when you install the Apache Cloudberry server. These utilities reside in `$GPHOME/bin`.

Superscripts identify those utilities that require separate downloads, as well as those utilities that are also installed with the Client and Loader Tools Packages. All utilities are installed when you install the Apache Cloudberry server, unless specifically identified by a superscript.

For more information about a utility, see the corresponding topic listed in the System Utilities section.

## Reference for Client Applications {#reference-for-client-applications}

- [clusterdb](/cloudberry/reference/sys-utilities/clusterdb/) — cluster a database
- [createdb](/cloudberry/reference/sys-utilities/createdb/) — create a new database
- [createuser](/cloudberry/reference/sys-utilities/createuser/) — define a new user account
- [dropdb](/cloudberry/reference/sys-utilities/dropdb/) — remove a database
- [dropuser](/cloudberry/reference/sys-utilities/dropuser/) — remove a user account
- [pg_config](/cloudberry/reference/sys-utilities/pg-config/) — retrieve information about the installed version of PostgreSQL
- [pg_dump](/cloudberry/reference/sys-utilities/pg-dump/) — extract a database into a script file or other archive file
- [pg_dumpall](/cloudberry/reference/sys-utilities/pg-dumpall/) — extract a database cluster into a script file
- [pg_restore](/cloudberry/reference/sys-utilities/pg-restore/) — restore a database from an archive file created by pg_dump
- [psql](/cloudberry/reference/sys-utilities/psql/) — interactive terminal
- [reindexdb](/cloudberry/reference/sys-utilities/reindexdb/) — reindex a database
- [vacuumdb](/cloudberry/reference/sys-utilities/vacuumdb/) — garbage-collect and analyze a database

## Reference for Server Applications {#reference-for-server-applications}

- [pg_checksums](/cloudberry/reference/sys-utilities/pg-checksums/) — enable, disable or check data checksums in a database cluster

## Reference for Administrator {#reference-for-administrator}

- [analyzedb](/cloudberry/reference/sys-utilities/analyzedb/) - performs `ANALYZE` operations on tables incrementally and concurrently
- [gpaddmirrors](/cloudberry/reference/sys-utilities/gpaddmirrors/) - add mirror segments to a Apache Cloudberry system that was initially configured without mirroring
- [gpbackup](/cloudberry/reference/sys-utilities/gpbackup/) - create a Apache Cloudberry backup for use with the gprestore utility
- [gpcheckcat](/cloudberry/reference/sys-utilities/gpcheckcat/) - test Apache Cloudberry catalog tables for inconsistencies
- [gpcheckperf](/cloudberry/reference/sys-utilities/gpcheckperf/) - verifiy the baseline hardware performance of the specified hosts
- [gpconfig](/cloudberry/reference/sys-utilities/gpconfig/) - set server configuration parameters on all segments within a Apache Cloudberry system
- [gpdeletesystem](/cloudberry/reference/sys-utilities/gpdeletesystem/) - delete a Apache Cloudberry system that was initialized using gpinitsystem
- [gpdemo](/cloudberry/reference/sys-utilities/gpdemo/) - deploy a small Apache Cloudberry cluster with segments on a single node to make a demo
- [gpexpand](/cloudberry/reference/sys-utilities/gpexpand/) - expand an existing Apache Cloudberry across new hosts in the system
- [gpfdist](/cloudberry/reference/sys-utilities/gpfdist/) - serve data files to or writes data files out from Apache Cloudberry segments
- [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/) - add and/or initialize a standby coordinator host for a Apache Cloudberry system
- [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/) - initialize a Apache Cloudberry system using configuration parameters specified in the gpinitsystem_config file
- [gpload](/cloudberry/reference/sys-utilities/gpload/) - run a load job as defined in a YAML formatted control file
- [gplogfilter](/cloudberry/reference/sys-utilities/gplogfilter/) - search through Apache Cloudberry log files for specified entries
- [gpmemreport](/cloudberry/reference/sys-utilities/gpmemreport/) - interpret the output created by the gpmemwatcher utility and generates output files in a readable format
- [gpmemwatcher](/cloudberry/reference/sys-utilities/gpmemwatcher/) - track the memory usage of each process in a database cluster.
- [gpmovemirrors](/cloudberry/reference/sys-utilities/gpmovemirrors/) - move mirror segment instances to new locations
- [gppkg](/cloudberry/reference/sys-utilities/gppkg/) - package manager to install, upgrade, migrate, and remove extensions in `.gppkg` format
- [gprestore](/cloudberry/reference/sys-utilities/gprestore/) - restore a database backup that was created using the gpbackup utility
- [gpreload](/cloudberry/reference/sys-utilities/gpreload/) - reload table data sorting the data based on specified columns
- [gprecoverseg](/cloudberry/reference/sys-utilities/gprecoverseg/) - recover a primary or mirror segment instance that has been marked as down (if mirroring is enabled)
- [gpshrink](/cloudberry/reference/sys-utilities/gpshrink/) - use `gpshrink` to reduce the size of the cluster, saving server resources
- [gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/) - exchange SSH public keys between hosts
- [gpssh](/cloudberry/reference/sys-utilities/gpssh/) - provide SSH access to multiple hosts at once
- [gpstart](/cloudberry/reference/sys-utilities/gpstart/) - start a Apache Cloudberry system
- [gpstate](/cloudberry/reference/sys-utilities/gpstate/) - show the status of a running Apache Cloudberry system
- [gpstop](/cloudberry/reference/sys-utilities/gpstop/) - stop or restart a Apache Cloudberry system
- [gpsync](/cloudberry/reference/sys-utilities/gpsync/) - copy files between multiple hosts at once
- [gpactivatestandby](/cloudberry/reference/sys-utilities/gpactivatestandby/) - activate a standby coordinator host and makes it the active coordinator
