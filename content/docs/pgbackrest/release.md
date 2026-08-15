---
title: "Release Notes"
linkTitle: "Releases"
weight: 60
description: "pgBackRest release history with detailed changelog for every version."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [Reference]
---


--------

## Introduction

pgBackRest release numbers consist of two parts, major and minor. A major release *may* break compatibility with the prior major release, but v2 releases are fully compatible with v1 repositories and will accept all v1 options. Minor releases can include bug fixes and features but do not change the repository format and strive to avoid changing options and naming. Documentation for the v1 release can be found [here](https://pgbackrest.org/1). The notes for a release may also contain "Additional Notes" but changes in this section are only to documentation or the test suite and have no direct impact on the pgBackRest codebase.


--------

## Current Stable Release


### v2.59.0 Release Notes

*PostgreSQL 19 Support*

*Released July 20, 2026*

**NOTE TO PACKAGERS**: A new distribution tarball is available which simplifies the build process by providing pregenerated HTML documentation, man page, and code. The tarball is attached to each release as an asset and is named `pgbackrest-{version}.tar.gz`. See the `README.md` in the tarball for details. Please use the new distribution tarball to avoid the additional build tooling required to generate code in future releases. See [New Distribution Tarball](/docs/pgbackrest/news/#distribution-tarball) for more information. **NOTE TO PACKAGERS**: There is a new optional dependency on `libsystemd`. **IMPORTANT NOTE**: Starting with this release, only the `restore` command may be run as root by default. Use `allow-root` to run other commands as root (though this is not recommended).

**Bug Fixes:**

- Fix `expire` removing a backup in progress on another host. (*Reviewed by Douglas J Hunley. Reported by Dmitrii.*)
- Fix `archive-push-queue-max` not enforced when a WAL file errors. (*Reviewed by Stefan Fercot. Reported by vut12.*)
- Fix async `archive-get` failure during recovery across a timeline switch. (*Reviewed by Douglas J Hunley. Reported by Jimmy Yih.*)
- Fix potential buffer overrun in error module. (*Fixed by Christophe Pettus. Reviewed by David Steele.*)
- Fix use-after-free of parallel protocol client. (*Reviewed by Douglas J Hunley. Reported by Georgy Shelkovy.*)
- Fix heap overflow when a pg option is set without pg1. (*Reviewed by Douglas J Hunley. Reported by Naveen.*)

**Features:**

- PostgreSQL 19beta2 support. (*Reviewed by Stefan Fercot.*)
- Add `archive-expire-before` option to clean up WAL archive. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Add batch delete for Azure storage. (*Reviewed by Douglas J Hunley, Crispy.*)
- Add support for S3 Outposts. (*Contributed by Shiva Kumar Ambigi. Reviewed by David Steele, Roberto Mello.*)
- Add S3 process authentication. (*Reviewed by Andrew Charlton. Suggested by Andrew Charlton.*)

**Improvements:**

- Reconnect SFTP storage after the server drops an idle connection. (*Reviewed by Stefan Fercot. Suggested by mustafa0x, tisserat.*)
- Add user/group caching for faster manifest build. (*Contributed by Gunnar Lindholm. Reviewed by David Steele.*)
- Add per-repo backup progress to `info` command output. (*Contributed by Will Morland. Reviewed by David Steele, Stefan Fercot.*)
- Add `backup.info` checks to `verify` command. (*Contributed by Denis Garsh. Reviewed by David Steele, Douglas J Hunley.*)
- Allow the S3 STS endpoint to be configured. (*Contributed by Simon Gratton. Reviewed by David Steele.*)
- Add `archive-push-batch-size` to limit WAL pushed per asynchronous run. (*Reviewed by Stefan Fercot.*)
- Exit async `archive-push` on first error. (*Reviewed by Stefan Fercot. Suggested by Lardière Sébastien.*)
- Harden HTTP chunked response parsing. (*Contributed by Shubham. Reviewed by David Steele.*)
- Error when running as root unless `allow-root` is enabled. (*Reviewed by Douglas J Hunley.*)
- Fewer binary searches when building manifest. (*Contributed by Gunnar Lindholm. Reviewed by David Steele.*)
- Improve seek performance during block incremental delta restore. (*Reviewed by David Christensen, Douglas J Hunley.*)
- Bundle backup files in order rather than scanning for a better fit. (*Reviewed by Stefan Fercot.*)
- Report the underlying error when a query fails to complete. (*Reviewed by Andrew Pogrebnoi. Suggested by Marco Fontana.*)
- Report the actual error when an S3 credential request fails. (*Reviewed by Douglas J Hunley. Suggested by Mitchell Grice.*)
- Report `archive-push` spool path errors to the PostgreSQL log. (*Reviewed by Douglas J Hunley. Suggested by Don Seiler.*)
- Hint that pgBackRest may be out of date when a version is unsupported.
- Add systemd notify integration. (*Contributed by Andrew Jackson. Reviewed by David Steele.*)
- Suppress `unused parameter` errors in meson compiler probes. (*Contributed by Jörg Plate. Reviewed by David Steele.*)
- C11 is now the minimum C standard. (*Reviewed by Mohammad Ali Nazir Kosar.*)

**Documentation Improvements:**

- Make `stanza` option internal for the `repo-*` commands. (*Reviewed by Stefan Fercot.*)
- Document that info reads encryption settings from global section. (*Reviewed by Stefan Fercot. Suggested by Ron Johnson.*)
- Document that `expire-auto` uses the `backup` command configuration. (*Reviewed by Stefan Fercot. Suggested by Lardière Sébastien.*)
- Document adjusting the logrotate `su` directive for a dedicated user. (*Reviewed by Douglas J Hunley. Suggested by lkanbus.*)
- Document that end-of-line comments are not supported in config files. (*Reviewed by Douglas J Hunley. Suggested by Alex Richman.*)

**Test Suite Improvements:**

- Fix Alpine group conflicts in CI containers. (*Contributed by Artur Zakirov. Reviewed by David Steele.*)


--------

## Stable Releases


### v2.58.0 Release Notes

*Object Storage Improvements*

*Released January 19, 2026*

**IMPORTANT NOTE**: The minimum values for the `repo-storage-upload-chunk-size` option have increased. They now represent the minimum allowed by the vendors.

**Bug Fixes:**

- Fix deadlock due to logging in signal handler. (*Fixed by Maxim Michkov. Reviewed by David Steele.*)

**Features:**

- HTTP support for S3, GCS, and Azure. (*Contributed by Will Morland. Reviewed by David Steele.*)
- Allow expiration of oldest full backup regardless of current retention. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Ron Johnson.*)
- Support for Azure managed identities. (*Contributed by Moiz Ibrar, Matthew Mols. Reviewed by David Steele.*)
- ***Experimental*** support for S3 EKS pod identity. (*Contributed by Pierre BOUTELOUP. Reviewed by David Steele.*)
- Allow configuration of TLS cipher suites. (*Contributed by Gunnar "Nick" Bluth. Reviewed by David Steele.*)
- Allow process priority to be set. (*Reviewed by Douglas J Hunley.*)

**Improvements:**

- Allow dots in S3 bucket names when using path-style URIs. (*Contributed by Joakim Hindersson. Reviewed by David Steele.*)
- Require TLS >= 1.2 unless verification is disabled. (*Reviewed by Douglas J Hunley, Gunnar "Nick" Bluth.*)
- Dynamically size S3/GCS/Azure chunks for large uploads. (*Reviewed by Douglas J Hunley. Suggested by Timothée Peignier.*)
- Optimize S3/GCS/Azure chunk size for small files. (*Reviewed by Douglas J Hunley.*)
- Remove support for PostgreSQL `9.5`. (*Reviewed by Douglas J Hunley.*)
- Improve logging of default for options with an unresolved dependency. (*Reviewed by Stefan Fercot.*)

**Documentation Improvements:**

- Remove explicit `max_wal_senders`/`wal_level` configuration from user guide. (*Suggested by Jamie Nguyen.*)
- Clarify that bundling is useful for filesystems with large block sizes. (*Suggested by Ron Johnson.*)


### v2.57.0 Release Notes

*Suppress Repository Symlinks*

*Released October 18, 2025*

**Bug Fixes:**

- Unnest HTTP/TLS/socket timeouts. (*Reviewed by David Christensen.*)
- Fix possible segfault in page checksum error message. (*Fixed by Zsolt Parragi. Reviewed by David Steele.*)

**Features:**

- Add `repo-symlink` option to suppress creation of repository symlinks. (*Reviewed by Douglas J Hunley. Suggested by Ron Johnson.*)

**Improvements:**

- Add HTTP retries for 408 and 429 errors. (*Reviewed by David Christensen.*)


### v2.56.0 Release Notes

*Progress Info Improvements*

*Released July 21, 2025*

**Bug Fixes:**

- Fix issue with adhoc expiration when no backups in a repository. (*Reviewed by Stefan Fercot. Reported by Anup Gupta.*)

**Features:**

- Add restore progress to `info` command output. (*Contributed by Denis Garsh, Maxim Michkov. Reviewed by David Steele.*)
- Add progress-only detail level for `info` command output. (*Contributed by Denis Garsh. Reviewed by David Steele, Stefan Fercot.*)

**Improvements:**

- Retry failed reads on object stores. (*Reviewed by David Christensen.*)
- Fix defaults in command-line help. (*Reviewed by David Christensen, Chris Bandy.*)

**Documentation Improvements:**

- Describe discrete option values in a list where appropriate. (*Contributed by Anton Kurochkin. Reviewed by David Steele.*)
- Fix "less than" in help output for `archive-mode` option. (*Contributed by Anton Kurochkin. Reviewed by David Steele.*)


### v2.55.1 Release Notes

*Bug Fixes*

*Released May 5, 2025*

**Bug Fixes:**

- Revert "calculate content-md5 on S3 only when required". (*Reviewed by David Christensen. Reported by Frank Brendel.*)
- Fix lower bounds checking for option keys. (*Reviewed by David Christensen, Wolfgang Walther. Reported by Wolfgang Walther.*)


### v2.55.0 Release Notes

*Verification Improvements and PostgreSQL 18 Support*

*Released April 21, 2025*

**Bug Fixes:**

- Fix block incremental restore issue on non-default repository. (*Reviewed by David Christensen, Aleksander Łukasz. Reported by Aleksander Łukasz.*)
- Do not set `recovery_target_timeline=current` for PostgreSQL < 12. (*Reviewed by Stefan Fercot.*)
- Fix expire archive range logging. (*Reviewed by Stefan Fercot. Reported by Aleš Zelený.*)
- Fix error reporting for queries with no results. (*Reviewed by Stefan Fercot. Reported by Susantha Bathige.*)

**Features:**

- Verify recovery target timeline. (*Reviewed by Stefan Fercot.*)
- Allow verification of a specified backup. (*Contributed by Maxim Michkov. Reviewed by David Steele.*)
- Add support for S3/GCS requester pays. (*Contributed by Timothée Peignier. Reviewed by David Steele.*)
- PostgreSQL 18 support. (*Reviewed by Stefan Fercot.*)
- Allow connections to PostgreSQL on abstract domain sockets. (*Reviewed by Chris Bandy. Suggested by Chris Bandy.*)
- Add numeric output to `version` command. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)

**Improvements:**

- Allow backup command to operate on remote repositories. (*Reviewed by Stefan Fercot.*)
- Use lz4 for protocol compression. (*Reviewed by Stefan Fercot.*)
- Calculate `content-md5` on S3 only when required. (*Reviewed by David Christensen.*)
- Warn when a value for a multi-key option is overwritten. (*Reviewed by David Christensen, Stefan Fercot.*)
- Add detail logging for expired archive path. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Remove support for PostgreSQL `9.4`. (*Reviewed by Stefan Fercot.*)
- Remove autoconf/make build. (*Reviewed by David Christensen.*)

**Documentation Improvements:**

- Fix documentation for specifying multiple stanzas with `tls-server-auth`. (*Reviewed by David Christensen, Stefan Fercot. Suggested by Terry MacAndrew.*)
- Clarify incremental backup expiration. (*Reviewed by Stefan Fercot.*)
- Clarify requirement for local/remote pgBackRest versions to match. (*Contributed by Greg Clough. Reviewed by David Steele.*)
- Add FAQ about exporting self-contained cluster. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Caveat `--tablespace-map-all` regarding tablespace creation. (*Reviewed by Stefan Fercot, Christophe Courtois. Suggested by Christophe Courtois.*)
- Clarify behavior of `--repo-retention-full-type`. (*Reviewed by Antoine Beaupré. Suggested by Antoine Beaupré.*)
- Change `--process-max` recommendation for object stores to `--repo-bundle`. (*Reviewed by Stefan Fercot.*)
- Update `unix_socket_directory` to `unix_socket_directories`. (*Contributed by hyunkyu han. Reviewed by David Steele.*)
- Recommend not placing `spool-path` within `pg_xlog`/`pg_wal`. (*Reviewed by Martín Marqués, Don Seiler. Suggested by Martín Marqués.*)


### v2.54.2 Release Notes

*Bug Fix*

*Released January 20, 2025*

**Bug Fixes:**

- Fix issue after disabling bundling with block incremental enabled. (*Reviewed by David Christensen.*)

**Documentation Improvements:**

- Clarify behavior of multiple configuration files. (*Reviewed by Paul Bierly. Suggested by Paul Bierly.*)


### v2.54.1 Release Notes

*Bug Fix*

*Released December 16, 2024*

**Bug Fixes:**

- Fix issue with `version`/`help` commands attempting to load `pgbackrest.conf`. (*Reviewed by Stefan Fercot. Reported by Bradford Boyle, Julian.*)

**Test Suite Improvements:**

- Stabilize async archiving in integration tests. (*Contributed by Viktor Kurilko. Reviewed by David Steele.*)


### v2.54.0 Release Notes

*Target Time for Versioned Storage*

*Released October 21, 2024*

**NOTE TO PACKAGERS**: This is last feature release to support the autoconf/make build. Please migrate to meson if you have not already done so. 2.54.X patch releases (if any) will continue to support autoconf/make.

**Bug Fixes:**

- Fix PostgreSQL query performance for large datasets. (*Fixed by Thibault Vincent, David Steele. Reviewed by David Christensen, Antoine Millet. Reported by Antoine Millet.*)

**Features:**

- Allow repositories on versioned storage to be read at a target time. (*Reviewed by Stefan Fercot, David Christensen.*)
- Allow requested standby backup to proceed with no standby. (*Reviewed by Stefan Fercot.*)

**Improvements:**

- Summarize backup reference list for `info` command text output. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Refresh web-id token for each S3 authentication. (*Contributed by Brent Graveland. Reviewed by David Steele.*)
- Correctly display current values for indexed options in help. (*Reviewed by David Christensen.*)
- Save `backup.info` only when contents have changed. (*Reviewed by Stefan Fercot.*)
- Remove limitation on reading files in parallel during restore. (*Reviewed by David Christensen.*)
- Improve SFTP error messages. (*Contributed by Reid Thompson. Reviewed by David Steele.*)

**Documentation Features:**

- Add performance tuning section to user guide. (*Reviewed by Stefan Fercot.*)

**Documentation Improvements:**

- Clarify source for `data_directory`. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Matthias.*)
- Better logic for deciding when a summary should be lower-cased. (*Suggested by Daniel Westermann.*)


### v2.53.1 Release Notes

*PostgreSQL 17 Support*

*Released August 19, 2024*

**Bug Fixes:**

- Fix permissions when `restore` run as root user. (*Reviewed by Stefan Fercot. Reported by Will M.*)
- Fix segfault on delayed connection errors. (*Reviewed by David Christensen. Reported by Anton Glushakov.*)
- Skip local repository duplicate check for SFTP. (*Fixed by Reid Thompson. Reviewed by David Steele. Reported by Anton Kurochkin.*)

**Improvements:**

- PostgreSQL 17 support.


### v2.53 Release Notes

*Concurrent Backups*

*Released July 22, 2024*

**IMPORTANT NOTE**: The `log-level-stderr` option default has been changed from `warn` to `off`. This makes it easier to capture errors when only redirecting `stdout`. To preserve the prior behavior set `log-level-stderr=warn`. **NOTE TO PACKAGERS**: The lz4 library is now required by the meson build. **NOTE TO PACKAGERS**: Compiler support for `__builtin_clzl()` and `__builtin_bswap64()` is now required by the meson build.

**Bug Fixes:**

- Fix SFTP renaming failure when file already exists. (*Fixed by Reid Thompson. Reviewed by David Steele. Reported by ahmed112212.*)

**Features:**

- Allow backups to run concurrently on different repositories. (*Reviewed by Reid Thompson, Stefan Fercot.*)
- Support IP-based SANs for TLS certificate validation. (*Contributed by David Christensen. Reviewed by David Steele.*)

**Improvements:**

- Default `log-level-stderr` option to `off`. (*Reviewed by Greg Sabino Mullane, Stefan Fercot.*)
- Allow alternative WAL segment sizes for PostgreSQL ≤ 10. (*Contributed by Viktor Kurilko. Reviewed by David Steele.*)
- Add hint to check SFTP authorization log. (*Contributed by Vitalii Zurian. Reviewed by Reid Thompson, David Steele.*)

**Documentation Improvements:**

- Clarify `archive-push` multi-repo behavior. (*Reviewed by Stefan Fercot.*)


### v2.52.1 Release Notes

*Bug Fix*

*Released June 25, 2024*

**Bug Fixes:**

- Fix issue with files larger on the replica than on the primary. (*Reviewed by Stefan Fercot. Reported by Nicolas Lassimonne.*)


### v2.52 Release Notes

*PostgreSQL 17beta1 Support*

*Released May 27, 2024*

**NOTE TO PACKAGERS**: The build system for pgBackRest is now meson. The autoconf/make build will not receive any new features and will be removed after a few releases.

**Features:**

- Add GCS batch delete support. (*Reviewed by Reid Thompson.*)
- S3 `SSE-C` encryption support. (*Reviewed by Tim Jones. Suggested by Tim Jones.*)
- PostgreSQL 17beta1 support. (*Reviewed by Stefan Fercot.*)

**Improvements:**

- Allow explicit disabling of optional dependencies in meson builds. (*Contributed by Michael Schout. Reviewed by David Steele.*)
- Dynamically find python in meson build. (*Contributed by Michael Schout. Reviewed by David Steele.*)
- Tag `pgbackrest` build target in meson as installable. (*Contributed by Bradford Boyle. Reviewed by David Steele.*)

**Documentation Improvements:**

- Update `start`/`stop` documentation to reflect actual functionality. (*Reviewed by Stefan Fercot.*)


### v2.51 Release Notes

*Meson Build System*

*Released March 25, 2024*

**Bug Fixes:**

- Skip zero-length files for block incremental delta restore. (*Reviewed by Sebastian Krause, René Højbjerg Larsen. Reported by Sebastian Krause.*)
- Fix performance regression in storage list. (*Reviewed by Stephen Frost. Reported by Maksym Boguk.*)
- Fix progress logging when file size changes during backup. (*Reviewed by Stephen Frost. Reported by samkingno.*)

**Improvements:**

- Improved support for dual stack connections. (*Reviewed by Stephen Frost. Suggested by Timothée Peignier.*)
- Make meson the primary build system. (*Reviewed by Stephen Frost.*)
- Detect files that have not changed during non-delta incremental backup. (*Reviewed by Stephen Frost.*)
- Prevent invalid recovery when `backup_label` removed. (*Reviewed by Stephen Frost.*)
- Improve `archive-push` WAL segment queue handling. (*Reviewed by Stephen Frost.*)
- Limit resume functionality to full backups. (*Reviewed by Stephen Frost, Stefan Fercot.*)
- Update resume functionality for block incremental. (*Reviewed by Stephen Frost.*)
- Allow `--version` and `--help` for version and help. (*Reviewed by Greg Sabino Mullane. Suggested by Greg Sabino Mullane.*)
- Add detailed backtrace to autoconf/make build. (*Reviewed by Stephen Frost.*)

**Documentation Improvements:**

- Update references to `recovery.conf`. (*Reviewed by Stefan Fercot. Suggested by Stephen Frost.*)


### v2.50 Release Notes

*Performance Improvements and Bug Fixes*

*Released January 22, 2024*

**Bug Fixes:**

- Fix short read in block incremental restore. (*Reviewed by Stephen Frost, Brent Graveland. Reported by Adol Rodriguez, Brent Graveland.*)
- Fix overflow suppressing backup progress in `info` output. (*Fixed by Robert Donovan. Reviewed by Joe Wildish.*)

**Improvements:**

- Preserve partial files during block incremental delta restore. (*Reviewed by Stephen Frost.*)
- Add support for alternate compile-time page sizes. (*Contributed by Viktor Kurilko. Reviewed by David Steele.*)
- Skip files truncated during backup when bundling. (*Contributed by Georgy Shelkovy. Reviewed by David Steele.*)
- Improve SFTP storage error messages. (*Contributed by Reid Thompson. Reviewed by David Steele.*)


### v2.49 Release Notes

*Remove PostgreSQL 9.3 Support*

*Released November 27, 2023*

**Bug Fixes:**

- Fix regression in retries. (*Reviewed by Stephen Frost. Reported by Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)
- Fix recursive path remove in SFTP storage driver. (*Fixed by Reid Thompson. Reviewed by Stephen Frost. Reported by Luc.*)

**Improvements:**

- Remove support for PostgreSQL `9.3`. (*Reviewed by Stephen Frost.*)

**Documentation Features:**

- Document maintainer options. (*Reviewed by Stefan Fercot.*)
- Update point-in-time recovery documentation for PostgreSQL >= 13.

**Test Suite Improvements:**

- Allow `config/load` unit test to run without `libssh2` installed. (*Contributed by Reid Thompson. Reviewed by David Steele. Suggested by Wu Ning.*)


### v2.48 Release Notes

*Repository Storage Tags*

*Released September 25, 2023*

**Bug Fixes:**

- Fix issue restoring block incremental without a block list. (*Reviewed by Stephen Frost, Burak Yurdakul. Reported by Burak Yurdakul.*)

**Features:**

- Add `--repo-storage-tag` option to create object tags. (*Reviewed by Stephen Frost, Stefan Fercot, Timothée Peignier.*)
- Add known hosts checking for SFTP storage driver. (*Contributed by Reid Thompson. Reviewed by Stephen Frost, David Steele.*)
- Support for dual stack connections. (*Reviewed by Stephen Frost.*)
- Add backup size completed/total to `info` command JSON output. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)

**Improvements:**

- Multi-stanza check command. (*Reviewed by Stephen Frost.*)
- Retry reads of `pg_control` until checksum is valid. (*Reviewed by Stefan Fercot, Stephen Frost.*)
- Optimize WAL segment check after successful backup. (*Reviewed by Stephen Frost.*)
- Improve GCS multi-part performance. (*Reviewed by Reid Thompson.*)
- Allow `archive-get` command to run when stanza is stopped. (*Reviewed by Tom Swartz, David Christensen, Reid Thompson.*)
- Accept leading tilde in paths for SFTP public/private keys. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Reload GCS credentials before renewing authentication token. (*Reviewed by Stephen Frost. Suggested by Daniel Farina.*)

**Documentation Bug Fixes:**

- Fix configuration reference example for the `tls-server-address` option. (*Fixed by Hartmut Goebel. Reviewed by David Steele.*)
- Fix command reference example for the `filter` option.

**Test Suite Improvements:**

- Allow `storage/sftp` unit test to run without `libssh2` installed. (*Contributed by Reid Thompson. Reviewed by David Steele. Suggested by Wu Ning.*)


### v2.47 Release Notes

*Performance Improvements and Bug Fixes*

*Released July 24, 2023*

**Bug Fixes:**

- Preserve block incremental info in manifest during delta backup. (*Reviewed by Stephen Frost. Reported by Francisco Miguel Biete Banon.*)
- Fix block incremental file names in `verify` command. (*Reviewed by Reid Thompson. Reported by Francisco Miguel Biete Banon.*)
- Fix spurious automatic delta backup on backup from standby. (*Reviewed by Stephen Frost. Reported by krmozejko, Don Seiler.*)
- Skip `recovery.signal` for PostgreSQL >= 12 when recovery `type=none`. (*Reviewed by Stefan Fercot. Reported by T.Anastacio.*)
- Fix unique label generation for diff/incr backup. (*Fixed by Andrey Sokolov. Reviewed by David Steele.*)
- Fix time-based archive expiration when no backups are expired. (*Reviewed by Stefan Fercot.*)

**Improvements:**

- Improve performance of SFTP storage driver. (*Contributed by Stephen Frost, Reid Thompson. Reviewed by David Steele.*)
- Add timezone offset to `info` command date/time output. (*Reviewed by Stefan Fercot, Philip Hurst. Suggested by Philip Hurst.*)
- Centralize error handling for unsupported features. (*Reviewed by Stefan Fercot.*)

**Documentation Improvements:**

- Clarify preference to install from packages in the user guide. (*Reviewed by Stefan Fercot. Suggested by dr-kd.*)


### v2.46 Release Notes

*Block Incremental Backup and SFTP Storage*

*Released May 22, 2023*

**Features:**

- Block incremental backup. (*Reviewed by John Morris, Stephen Frost, Stefan Fercot.*)
- SFTP support for repository storage. (*Contributed by Reid Thompson. Reviewed by Stephen Frost, David Steele.*)
- PostgreSQL 16 support. (*Reviewed by Stefan Fercot.*)

**Improvements:**

- Allow page header checks to be skipped. (*Reviewed by David Christensen. Suggested by David Christensen.*)
- Avoid `chown()` on recovery files during restore. (*Reviewed by Stefan Fercot, Marcelo Henrique Neppel. Suggested by Marcelo Henrique Neppel.*)
- Add error retry detail for HTTP retries.

**Documentation Improvements:**

- Add warning about using recovery `type=none`. (*Reviewed by Stefan Fercot.*)
- Add note about running `stanza-create` on already-created repositories.


### v2.45 Release Notes

*Block Incremental Backup (BETA)*

*Released March 20, 2023*

**Bug Fixes:**

- Skip writing `recovery.signal` by default for restores of offline backups. (*Reviewed by Stefan Fercot. Reported by Marcel Borger.*)

**Features:**

- Block incremental backup (BETA). (*Reviewed by John Morris, Stephen Frost, Stefan Fercot.*)

**Improvements:**

- Keep only one all-default group index. (*Reviewed by Stefan Fercot.*)

**Documentation Improvements:**

- Add explicit instructions for upgrading between `2.x` versions. (*Contributed by Christophe Courtois. Reviewed by David Steele.*)
- Remove references to SSH made obsolete when TLS was introduced.


### v2.44 Release Notes

*Remove PostgreSQL 9.0/9.1/9.2 Support*

*Released January 30, 2023*

**Improvements:**

- Remove support for PostgreSQL `9.0`/`9.1`/`9.2`. (*Reviewed by Stefan Fercot.*)
- Restore errors when no backup matches the current version of PostgreSQL. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Soulou.*)
- Add `compress-level` range checking for each `compress-type`. (*Reviewed by Stefan Fercot. Suggested by gkleen, ViperRu.*)

**Documentation Improvements:**

- Add warning about enabling "hierarchical namespace" on Azure storage. (*Reviewed by Stefan Fercot. Suggested by Vojtech Galda, Pluggi, asjonos.*)
- Add replacement for linefeeds in monitoring example. (*Reviewed by Stefan Fercot. Suggested by rudonx, gmustdie, Ivan Shelestov.*)
- Clarify `target-action` behavior on various PostgreSQL versions. (*Contributed by Chris Bandy. Reviewed by David Steele, Anton Kurochkin, Stefan Fercot. Suggested by Anton Kurochkin, Chris Bandy.*)
- Updates and clarifications to index page. (*Reviewed by Stefan Fercot.*)
- Add dark mode to the website. (*Suggested by Stephen Frost.*)


### v2.43 Release Notes

*Bug Fix*

*Released November 28, 2022*

**Bug Fixes:**

- Fix missing reference in diff/incr backup. (*Reviewed by Stefan Fercot. Reported by Marcel Borger, ulfedf, jaymefSO.*)

**Improvements:**

- Add hint when an option is specified without an index. (*Reviewed by Stefan Fercot.*)


### v2.42 Release Notes

*Bug Fixes*

*Released November 22, 2022*

**Bug Fixes:**

- Fix memory leak in file bundle `backup`/`restore`. (*Reviewed by John Morris, Oscar. Reported by Oscar.*)
- Fix protocol error on short read of remote file. (*Reviewed by Stephen Frost.*)

**Improvements:**

- Do not store references for zero-length files when bundling. (*Reviewed by Stefan Fercot.*)
- Use more generic descriptions for `pg_start_backup()`/`pg_stop_backup()`. (*Reviewed by Greg Sabino Mullane, David Christensen. Suggested by Greg Sabino Mullane.*)

**Test Suite Improvements:**

- Update `test.pl` `--psql-bin` option to match command-line help. (*Contributed by Koshi Shibagaki. Reviewed by David Steele.*)


### v2.41 Release Notes

*Backup Annotations*

*Released September 19, 2022*

**Bug Fixes:**

- Fix incorrect time expiration being used for non-default repositories. (*Reviewed by Stefan Fercot. Reported by Adam Brusselback.*)
- Fix issue when listing directories recursively with a filter. (*Reviewed by Stephen Frost. Reported by Efremov Egor.*)

**Features:**

- Backup key/value annotations. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Adam Berlin.*)

**Improvements:**

- Support `--set` in JSON output for `info` command. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Anton Kurochkin.*)
- Allow upload chunk size to be configured for object stores. (*Reviewed by Stefan Fercot. Suggested by Anton Glushakov.*)
- Update archive.info timestamps after a successful backup. (*Reviewed by Stefan Fercot. Suggested by Alex Richman.*)
- Move standby timeline check after checkpoint. (*Reviewed by Stefan Fercot, Keith Fiske. Suggested by Keith Fiske.*)
- Improve warning message on backup resume. (*Suggested by Cynthia Shang.*)

**Documentation Improvements:**

- Add absolute path for `kill` in `pgbackrest.service`. (*Suggested by Don Seiler.*)


### v2.40 Release Notes

*OpenSSL 3 Support*

*Released July 18, 2022*

**NOTE TO PACKAGERS**: An experimental meson build has been added but packagers should continue to use the autoconf/make build for the foreseeable future.

**Improvements:**

- OpenSSL 3 support. (*Reviewed by Stephen Frost.*)
- Create snapshot when listing contents of a path. (*Reviewed by John Morris, Stephen Frost.*)
- Force `target-timeline=current` when restore `type=immediate`. (*Reviewed by Stephen Frost.*)
- Truncate files during delta `restore` when they are larger than expected. (*Reviewed by Stephen Frost.*)
- Disable incremental manifest save when `resume=n`. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Set backup percent complete to zero before copy start. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Use S3 `IsTruncated` flag to determine list continuation. (*Reviewed by John Morris, Soulou. Suggested by Christian Montagne.*)

**Documentation Bug Fixes:**

- Skip internal options in the configuration reference. (*Reported by Francisco Miguel Biete Banon.*)

**Documentation Improvements:**

- Add link to PostgreSQL configuration in repository host section. (*Reviewed by Stefan Fercot. Suggested by Julien Cigar.*)

**Test Suite Improvements:**

- Add experimental Meson build. (*Reviewed by Eli Schwartz, Sam Bassaly.*)
- Allow any path to be passed to the `--test-path` option. (*Contributed by Andrey Sokolov. Reviewed by David Steele.*)
- Fix compile error when `DEBUG_EXEC_TIME` is defined without `DEBUG`. (*Contributed by Andrey Sokolov. Reviewed by David Steele.*)


### v2.39 Release Notes

*Verify and File Bundling*

*Released May 16, 2022*

**Bug Fixes:**

- Fix error thrown from `FINALLY()` causing an infinite loop. (*Reviewed by Stephen Frost.*)
- Error on all lock failures except another process holding the lock. (*Reviewed by Reid Thompson, Geir Råness. Reported by Geir Råness.*)

**Features:**

- Backup file bundling for improved small file support. (*Reviewed by Reid Thompson, Stefan Fercot, Chris Bandy.*)
- Verify command to validate the contents of a repository. (*Contributed by Cynthia Shang, Reid Thompson. Reviewed by David Steele, Stefan Fercot.*)
- PostgreSQL 15 support. (*Reviewed by Stefan Fercot.*)
- Show backup percent complete in `info` output. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Auto-select backup for `restore` command `--type=lsn`. (*Contributed by Reid Thompson. Reviewed by Stefan Fercot, David Steele.*)
- Suppress existing WAL warning when `archive-mode-check` is disabled. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Add AWS IMDSv2 support. (*Contributed by Nuno Pires. Reviewed by David Steele.*)

**Improvements:**

- Allow `repo-hardlink` option to be changed after full backup. (*Reviewed by Reid Thompson.*)
- Increase precision of percent complete logging for `backup` and `restore`. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Improve path validation for `repo-*` commands. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Improve `stop` command to honor `stanza` option. (*Contributed by Reid Thompson. Reviewed by David Steele. Suggested by ragaoua.*)
- Improve error message for invalid `repo-azure-key`. (*Contributed by Reid Thompson. Reviewed by David Steele. Suggested by Seth Daniel.*)
- Add hint to check the log on `archive-get`/`archive-push` async error. (*Reviewed by Reid Thompson.*)
- Add `ClockError` for unexpected clock skew and timezone changes. (*Reviewed by Greg Sabino Mullane, Stefan Fercot. Suggested by Greg Sabino Mullane.*)
- Strip extensions from history manifest before showing in error message. (*Reviewed by Stefan Fercot.*)
- Add user:group to lock permission error. (*Reviewed by Reid Thompson.*)

**Documentation Bug Fixes:**

- Fix incorrect reference to `stanza-update` in the user guide. (*Fixed by Abubakar Mohammed. Reviewed by David Steele.*)
- Fix example for `repo-gcs-key-type` option in configuration reference. (*Reviewed by Reid Thompson.*)
- Fix `tls-server-auth` example and add clarifications. (*Reviewed by Reid Thompson.*)

**Documentation Improvements:**

- Simplify messaging around supported versions in the documentation. (*Reviewed by Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)
- Add option type descriptions. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Add FAQ about backup types and restore speed. (*Contributed by David Christensen. Reviewed by Reid Thompson.*)
- Document required base branch for pull requests. (*Contributed by David Christensen. Reviewed by Reid Thompson.*)


### v2.38 Release Notes

*Minor Bug Fixes and Improvements*

*Released March 6, 2022*

**IMPORTANT NOTE**: Repository size reported by the `info` command is now entirely based on what pgBackRest has written to storage. Previously, in certain cases, pgBackRest could detect if additional compression was being applied by the storage but this is no longer supported.

**Bug Fixes:**

- Retry errors in S3 batch file delete. (*Reviewed by Reid Thompson. Reported by Alex Richman.*)
- Allow case-insensitive matching of HTTP `connection` header values. (*Reviewed by Reid Thompson. Reported by Rémi Vidier.*)

**Features:**

- Add support for AWS S3 server-side encryption using KMS. (*Contributed by Christoph Berg. Reviewed by David Steele, Tharindu Amila.*)
- Add `archive-missing-retry` option. (*Reviewed by Stefan Fercot.*)
- Add backup type filter to `info` command. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)

**Improvements:**

- Retry on page validation failure during `backup`. (*Reviewed by Stephen Frost, David Christensen.*)
- Handle TLS servers that do not close connections gracefully. (*Reviewed by Rémi Vidier, David Christensen, Stephen Frost.*)
- Add backup LSNs to `info` command output. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Automatically strip trailing slashes for `repo-ls` paths. (*Contributed by David Christensen. Reviewed by David Steele.*)
- Do not retry fatal errors. (*Reviewed by Reid Thompson.*)
- Remove support for PostgreSQL `8.3`/`8.4`. (*Reviewed by Reid Thompson, Stefan Fercot.*)
- Remove logic that tried to determine additional file system compression. (*Reviewed by Reid Thompson, Stefan Fercot.*)

**Documentation Bug Fixes:**

- Move `repo` options in TLS documentation to the `global` section. (*Reported by Anton Kurochkin.*)
- Remove unused `backup-standby` option from stanza commands. (*Reported by Stefan Fercot.*)
- Fix typos in help and release notes. (*Fixed by Daniel Gustafsson. Reviewed by David Steele.*)

**Documentation Improvements:**

- Add aliveness check to systemd service configuration. (*Suggested by Yogesh Sharma.*)
- Add FAQ explaining WAL archive suffix. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Note that replications slots are not restored. (*Contributed by Reid Thompson. Reviewed by David Steele, Stefan Fercot. Suggested by Christophe Courtois.*)


### v2.37 Release Notes

*TLS Server*

*Released January 3, 2022*

**IMPORTANT NOTE**: If the `restore` command is unable to find a backup that matches a specified time target then an error will be thrown, whereas before a warning was logged.

**Bug Fixes:**

- Fix `restore` delta link mapping when path/file already exists. (*Reviewed by Reid Thompson. Reported by Younes Alhroub.*)
- Fix socket leak on connection retries. (*Reviewed by Reid Thompson. Reported by James Coleman.*)

**Features:**

- Add TLS server. (*Reviewed by Stephen Frost, Reid Thompson, Andrew L'Ecuyer.*)
- Add `--cmd` option. (*Contributed by Reid Thompson. Reviewed by Stefan Fercot, David Steele. Suggested by Virgile CREVON.*)

**Improvements:**

- Check archive immediately after backup start. (*Reviewed by Reid Thompson, David Christensen.*)
- Add timeline and checkpoint checks to backup. (*Reviewed by Stefan Fercot, Reid Thompson.*)
- Check that clusters are alive and correctly configured during a backup. (*Reviewed by Stefan Fercot.*)
- Error when `restore` is unable to find a backup to match the time target. (*Reviewed by Reid Thompson, Douglas J Hunley. Suggested by Douglas J Hunley.*)
- Parse protocol/port in S3/Azure endpoints. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Add warning when checkpoint_timeout exceeds `db-timeout`. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Add verb to HTTP error output. (*Contributed by Christoph Berg. Reviewed by David Steele.*)
- Allow y/n arguments for boolean command-line options. (*Contributed by Reid Thompson. Reviewed by David Steele.*)
- Make backup size logging exactly match `info` command output. (*Contributed by Reid Thompson. Reviewed by David Steele. Suggested by Mahomed Hussein.*)

**Documentation Improvements:**

- Display size option default and allowed values with appropriate units. (*Reviewed by Reid Thompson.*)
- Fix typos and improve documentation for the `tablespace-map-all` option. (*Reviewed by Reid Thompson. Suggested by Reid Thompson.*)
- Remove obsolete statement about future multi-repository support. (*Suggested by David Christensen.*)


### v2.36 Release Notes

*Minor Bug Fixes and Improvements*

*Released November 1, 2021*

**Bug Fixes:**

- Allow "global" as a stanza prefix. (*Reviewed by Stefan Fercot. Reported by Younes Alhroub.*)
- Fix segfault on invalid GCS key file. (*Reviewed by Stephen Frost. Reported by Henrik Feldt.*)

**Improvements:**

- Allow `link-map` option to create new links. (*Reviewed by Don Seiler, Stefan Fercot, Chris Bandy. Suggested by Don Seiler.*)
- Increase max index allowed for `pg`/`repo` options to 256. (*Reviewed by Cynthia Shang.*)
- Add `WebIdentity` authentication for AWS S3. (*Reviewed by James Callahan, Reid Thompson, Benjamin Blattberg, Andrew L'Ecuyer.*)
- Report backup file validation errors in `backup.info`. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Add recovery start time to online backup restore log. (*Reviewed by Tom Swartz, Stefan Fercot. Suggested by Tom Swartz.*)
- Report original error and retries on local job failure. (*Reviewed by Stefan Fercot.*)
- Rename page checksum error to error list in info text output. (*Reviewed by Stefan Fercot.*)
- Add hints to standby replay timeout message. (*Reviewed by Cynthia Shang, Stefan Fercot. Suggested by Leigh Downs.*)


### v2.35 Release Notes

*Binary Protocol*

*Released August 23, 2021*

**IMPORTANT NOTE**: The log level for copied files in the `backup`/`restore` commands has been changed to `detail`. This makes the `info` log level less noisy but if these messages are required then set the log level for the `backup`/`restore` commands to `detail`

**Bug Fixes:**

- Detect errors in S3 multi-part upload finalize. (*Reviewed by Cynthia Shang, Marco Montagna. Reported by Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)
- Fix detection of circular symlinks. (*Reviewed by Stefan Fercot. Reported by Rohit Raveendran.*)
- Only pass selected `repo` options to the remote. (*Reviewed by David Christensen, Cynthia Shang. Reported by Greg Sabino Mullane, David Christensen.*)

**Improvements:**

- Binary protocol. (*Reviewed by Cynthia Shang.*)
- Automatically create data directory on `restore`. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Chris Bandy.*)
- Allow `restore` `--type=lsn`. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang. Suggested by James Coleman.*)
- Change level of `backup`/`restore` copied file logging to detail. (*Reviewed by Stefan Fercot. Suggested by Jens Wilke.*)
- Loop while waiting for checkpoint LSN to reach replay LSN. (*Contributed by Stefan Fercot. Reviewed by David Steele. Suggested by Fatih Mencutekin.*)
- Log `backup` file total and `restore` size/file total. (*Reviewed by Cynthia Shang.*)

**Documentation Bug Fixes:**

- Fix incorrect host names in user guide. (*Reviewed by Stefan Fercot. Reported by Greg Sabino Mullane.*)

**Documentation Improvements:**

- Update contributing documentation and add pull request template. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Rearrange backup documentation in user guide. (*Reviewed by Cynthia Shang.*)
- Clarify `restore` `--type` behavior in command reference. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Fix documentation and comment typos. (*Contributed by Eric Radman. Reviewed by David Steele.*)

**Test Suite Improvements:**

- Add check for test path inside repo path. (*Reviewed by Greg Sabino Mullane. Suggested by Greg Sabino Mullane.*)
- Add CodeQL static code analysis. (*Reviewed by Cynthia Shang.*)
- Update tests to use standard patterns. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.34 Release Notes

*PostgreSQL 14 Support*

*Released June 7, 2021*

**Bug Fixes:**

- Fix issues with leftover spool files from a prior `restore`. (*Reviewed by Cynthia Shang, Stefan Fercot, Floris van Nee. Reported by Floris van Nee.*)
- Fix issue when checking links for large numbers of tablespaces. (*Reviewed by Cynthia Shang, Avinash Vallarapu. Reported by Avinash Vallarapu.*)
- Free no longer needed remotes so they do not timeout during `restore`. (*Reviewed by Cynthia Shang. Reported by Francisco Miguel Biete Banon.*)
- Fix `help` when a valid option is invalid for the specified command. (*Reviewed by Stefan Fercot. Reported by Cynthia Shang.*)

**Features:**

- Add PostgreSQL 14 support. (*Reviewed by Cynthia Shang.*)
- Add automatic GCS authentication for GCE instances. (*Reviewed by Jan Wieck, Daniel Farina.*)
- Add `repo-retention-history` option to expire backup history. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang, David Steele.*)
- Add `db-exclude` option. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang.*)

**Improvements:**

- Change archive expiration logging from detail to info level. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Remove stanza archive spool path on `restore`. (*Reviewed by Cynthia Shang, Stefan Fercot.*)
- Do not write files atomically or sync paths during `backup` copy. (*Reviewed by Stephen Frost, Stefan Fercot, Cynthia Shang.*)

**Documentation Improvements:**

- Update contributing documentation. (*Contributed by Cynthia Shang. Reviewed by David Steele, Stefan Fercot.*)
- Consolidate RHEL/CentOS user guide into a single document. (*Reviewed by Cynthia Shang.*)
- Clarify that `repo-s3-role` is not an `ARN`. (*Contributed by Isaac Yuen. Reviewed by David Steele.*)


### v2.33 Release Notes

*Multi-Repository and GCS Support*

*Released April 5, 2021*

**Bug Fixes:**

- Fix option warnings breaking async `archive-get`/`archive-push`. (*Reviewed by Cynthia Shang. Reported by Lev Kokotov.*)
- Fix memory leak in backup during archive copy. (*Reviewed by Cynthia Shang. Reported by Christian ROUX, Efremov Egor.*)
- Fix stack overflow in cipher passphrase generation. (*Reviewed by Cynthia Shang. Reported by bsiara.*)
- Fix `repo-ls` `/` on S3 repositories. (*Reviewed by Cynthia Shang. Reported by Lesovsky Alexey.*)

**Features:**

- Multiple repository support. (*Contributed by Cynthia Shang, David Steele. Reviewed by Stefan Fercot, Stephen Frost.*)
- GCS support for repository storage. (*Reviewed by Cynthia Shang, Daniel Farina.*)
- Add `archive-header-check` option. (*Reviewed by Stephen Frost, Cynthia Shang. Suggested by Hans-Jürgen Schönig.*)

**Improvements:**

- Include recreated system databases during selective restore. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang.*)
- Exclude `content-length` from S3 signed headers. (*Reviewed by Cynthia Shang. Suggested by Brian P Bockelman.*)
- Consolidate less commonly used repository storage options. (*Reviewed by Cynthia Shang.*)
- Allow custom `config-path` default with `./configure --with-configdir`. (*Contributed by Michael Schout. Reviewed by David Steele.*)
- Log archive copy during `backup`. (*Reviewed by Cynthia Shang, Stefan Fercot.*)

**Documentation Improvements:**

- Update reference to include links to user guide examples. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Update selective restore documentation with caveats. (*Reviewed by Cynthia Shang, Stefan Fercot.*)
- Add `compress-type` clarification to `archive-copy` documentation. (*Reviewed by Cynthia Shang, Stefan Fercot.*)
- Add `compress-level` defaults per `compress-type` value. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Add note about required NFS settings being the same as PostgreSQL. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.32 Release Notes

*Repository Commands*

*Released February 8, 2021*

**Bug Fixes:**

- Fix resume after partial delete of backup by prior resume. (*Reviewed by Cynthia Shang. Reported by Tom Swartz.*)

**Features:**

- Add `repo-ls` command. (*Reviewed by Cynthia Shang, Stefan Fercot.*)
- Add `repo-get` command. (*Contributed by Stefan Fercot, David Steele. Reviewed by Cynthia Shang.*)
- Add `archive-mode-check` option. (*Contributed by Stefan Fercot. Reviewed by David Steele, Michael Banck.*)

**Improvements:**

- Improve `archive-get` performance. (*Reviewed by Cynthia Shang.*)

**Documentation Improvements:**

- Improve `expire` command documentation. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.31 Release Notes

*Minor Bug Fixes and Improvements*

*Released December 7, 2020*

**Bug Fixes:**

- Allow `[`, `#`, and `space` as the first character in database names. (*Reviewed by Stefan Fercot, Cynthia Shang. Reported by Jefferson Alexandre.*)
- Create `standby.signal` only on PostgreSQL 12 when `restore` type is `standby`. (*Fixed by Stefan Fercot. Reviewed by David Steele. Reported by Keith Fiske.*)

**Features:**

- Expire history files. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)
- Report page checksum errors in `info` command `text` output. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang.*)
- Add `repo-azure-endpoint` option. (*Reviewed by Cynthia Shang, Brian Peterson. Suggested by Brian Peterson.*)
- Add `pg-database` option. (*Reviewed by Cynthia Shang.*)

**Improvements:**

- Improve `info` command output when a stanza is specified but missing. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang, David Steele. Suggested by uspen.*)
- Improve performance of large file lists in `backup`/`restore` commands. (*Reviewed by Cynthia Shang, Oscar.*)
- Add retries to PostgreSQL sleep when starting a backup. (*Reviewed by Cynthia Shang. Suggested by Vitaliy Kukharik.*)

**Documentation Improvements:**

- Replace RHEL/CentOS 6 documentation with RHEL/CentOS 8.


### v2.30 Release Notes

*PostgreSQL 13 Support*

*Released October 5, 2020*

**Bug Fixes:**

- Error with hints when backup user cannot read `pg_settings`. (*Reviewed by Stefan Fercot, Cynthia Shang. Reported by Mohamed Insaf K.*)

**Features:**

- PostgreSQL 13 support. (*Reviewed by Cynthia Shang.*)

**Improvements:**

- Improve PostgreSQL version identification. (*Reviewed by Cynthia Shang, Stephen Frost.*)
- Improve working directory error message. (*Reviewed by Stefan Fercot.*)
- Add hint about starting the stanza when WAL segment not found. (*Contributed by David Christensen. Reviewed by David Steele.*)
- Add hint for protocol version mismatch. (*Reviewed by Cynthia Shang. Suggested by loop-evgeny.*)

**Documentation Improvements:**

- Add note that pgBackRest versions must match when running remotely. (*Reviewed by Cynthia Shang. Suggested by loop-evgeny.*)
- Move info command text to the reference and link to user guide. (*Reviewed by Cynthia Shang. Suggested by Christophe Courtois.*)
- Update yum repository path for CentOS/RHEL user guide. (*Contributed by Heath Lord. Reviewed by David Steele.*)


### v2.29 Release Notes

*Auto S3 Credentials on AWS*

*Released August 31, 2020*

**Bug Fixes:**

- Suppress errors when closing `local`/`remote` processes. Since the command has completed it is counterproductive to throw an error but still **warn** to indicate that something unusual happened. (*Reviewed by Cynthia Shang. Reported by argdenis.*)
- Fix issue with `=` character in file or database names. (*Reviewed by Bastian Wegge, Cynthia Shang. Reported by Brad Nicholson, Bastian Wegge.*)

**Features:**

- Automatically retrieve temporary S3 credentials on AWS instances. (*Contributed by David Steele, Stephen Frost. Reviewed by Cynthia Shang, David Youatt, Aleš Zelený, Jeanette Bromage.*)
- Add `archive-mode` option to disable archiving on restore. (*Reviewed by Stephen Frost. Suggested by Stephen Frost.*)

**Improvements:**

- PostgreSQL 13 beta3 support. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace.
- Asynchronous `list`/`remove` for S3/Azure storage. (*Reviewed by Cynthia Shang, Stephen Frost.*)
- Improve memory usage of unlogged relation detection in manifest build. (*Reviewed by Cynthia Shang, Stephen Frost, Brad Nicholson, Oscar. Suggested by Oscar, Brad Nicholson.*)
- Proactively close file descriptors after forking async process. (*Reviewed by Stephen Frost, Cynthia Shang.*)
- Delay backup remote connection close until after archive check. (*Contributed by Floris van Nee. Reviewed by David Steele.*)
- Improve detailed error output. (*Reviewed by Cynthia Shang.*)
- Improve TLS error reporting. (*Reviewed by Cynthia Shang, Stephen Frost.*)

**Documentation Bug Fixes:**

- Add `none` to `compress-type` option reference and fix example. (*Reported by Ugo Bellavance, Don Seiler.*)
- Add missing `azure` type in `repo-type` option reference. (*Fixed by Don Seiler. Reviewed by David Steele.*)
- Fix typo in `repo-cipher-type` option reference. (*Fixed by Don Seiler. Reviewed by David Steele.*)

**Documentation Improvements:**

- Clarify that `expire` must be run regularly when `expire-auto` is disabled. (*Reviewed by Douglas J Hunley. Suggested by Douglas J Hunley.*)


### v2.28 Release Notes

*Azure Repository Storage*

*Released July 20, 2020*

**Bug Fixes:**

- Fix `restore` `--force` acting like `--force --delta`. This caused `restore` to replace files based on timestamp and size rather than overwriting, which meant some files that should have been updated were left unchanged. Normal `restore` and `restore` `--delta` were not affected by this issue. (*Reviewed by Cynthia Shang.*)

**Features:**

- Azure support for repository storage. (*Reviewed by Cynthia Shang, Don Seiler.*)
- Add `expire-auto` option. This allows automatic expiration after a successful backup to be disabled. (*Contributed by Stefan Fercot. Reviewed by Cynthia Shang, David Steele.*)

**Improvements:**

- Asynchronous S3 multipart upload. (*Reviewed by Stephen Frost.*)
- Automatic retry for `backup`, `restore`, `archive-get`, and `archive-push`. (*Reviewed by Cynthia Shang.*)
- Disable query parallelism in PostgreSQL sessions used for backup control. (*Reviewed by Stefan Fercot.*)
- PostgreSQL 13 beta2 support. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace.
- Improve handling of invalid HTTP response status. (*Reviewed by Cynthia Shang.*)
- Improve error when `pg1-path` option missing for `archive-get` command. (*Reviewed by Cynthia Shang.*)
- Add hint when checksum delta is enabled after a timeline switch. (*Reviewed by Matt Bunter, Cynthia Shang.*)
- Use PostgreSQL instead of `postmaster` where appropriate. (*Reviewed by Cynthia Shang.*)

**Documentation Bug Fixes:**

- Fix incorrect example for `repo-retention-full-type` option. (*Reported by Höseyin Sönmez.*)
- Remove internal commands from HTML and man command references. (*Reported by Cynthia Shang.*)

**Documentation Improvements:**

- Update PostgreSQL versions used to build user guides. Also add version ranges to indicate that a user guide is accurate for a range of PostgreSQL versions even if it was built for a specific version. (*Reviewed by Stephen Frost.*)
- Update FAQ for expiring a specific backup set. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Update FAQ to clarify default PITR behavior. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.27 Release Notes

*Expiration Improvements and Compression Drivers*

*Released May 26, 2020*

**Bug Fixes:**

- Fix issue checking if file links are contained in path links. (*Reviewed by Cynthia Shang. Reported by Christophe Cavallié.*)
- Allow `pg-path1` to be optional for synchronous `archive-push`. (*Reviewed by Cynthia Shang. Reported by Jerome Peng.*)
- The `expire` command now checks if a stop file is present. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Handle missing reason phrase in HTTP response. (*Reviewed by Cynthia Shang. Reported by Tenuun.*)
- Increase buffer size for lz4 compression flush. (*Reviewed by Cynthia Shang. Reported by Eric Radman.*)
- Ignore `pg-host*` and `repo-host*` options for the `remote` command. (*Reviewed by Cynthia Shang. Reported by Pavel Suderevsky.*)
- Fix possibly missing `pg1-*` options for the `remote` command. (*Reviewed by Cynthia Shang. Reported by Andrew L'Ecuyer.*)

**Features:**

- Time-based retention for full backups. The `--repo-retention-full-type` option allows retention of full backups based on a time period, specified in days. (*Contributed by Cynthia Shang, Pierre Ducroquet. Reviewed by David Steele.*)
- Ad hoc backup expiration. Allow the user to remove a specified backup regardless of retention settings. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Zstandard compression support. Note that setting `compress-type=zst` will make new backups and archive incompatible (unrestorable) with prior versions of pgBackRest. (*Reviewed by Cynthia Shang.*)
- bzip2 compression support. Note that setting `compress-type=bz2` will make new backups and archive incompatible (unrestorable) with prior versions of pgBackRest. (*Contributed by Stephen Frost. Reviewed by David Steele, Cynthia Shang.*)
- Add `backup`/`expire` running status to the `info` command. (*Contributed by Stefan Fercot. Reviewed by David Steele.*)

**Improvements:**

- Expire WAL archive only when `repo-retention-archive` threshold is met. WAL prior to the first full backup was previously expired after the first full backup. Now it is preserved according to retention settings. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Add local MD5 implementation so S3 works when FIPS is enabled. (*Reviewed by Cynthia Shang, Stephen Frost. Suggested by Brian Almeida, John Kelly.*)
- PostgreSQL 13 beta1 support. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace. (*Reviewed by Cynthia Shang.*)
- Reduce `buffer-size` default to `1MiB`. (*Reviewed by Stephen Frost.*)
- Throw user-friendly error if `expire` is not run on repository host. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.26 Release Notes

*Non-blocking TLS*

*Released April 20, 2020*

**Bug Fixes:**

- Remove empty subexpression from manifest regular expression. MacOS was not happy about this though other platforms seemed to work fine. (*Fixed by David Raftis. Reviewed by David Steele.*)

**Improvements:**

- Non-blocking TLS implementation. (*Reviewed by Slava Moudry, Cynthia Shang, Stephen Frost.*)
- Only limit backup copy size for WAL-logged files. The prior behavior could possibly lead to `postgresql.conf` or `postgresql.auto.conf` being truncated in the backup. (*Reviewed by Cynthia Shang.*)
- TCP keep-alive options are configurable. (*Suggested by Marc Cousin.*)
- Add `io-timeout` option. (*Reviewed by Cynthia Shang.*)


### v2.25 Release Notes

*LZ4 Compression Support*

*Released March 26, 2020*

**Features:**

- Add lz4 compression support. Note that setting `compress-type=lz4` will make new backups and archive incompatible (unrestorable) with prior versions of pgBackRest. (*Reviewed by Cynthia Shang.*)
- Add `--dry-run` option to the `expire` command. Use dry-run to see which backups/archive would be removed by the `expire` command without actually removing anything. (*Contributed by Cynthia Shang, Luca Ferrari. Reviewed by David Steele. Suggested by Marc Cousin.*)

**Improvements:**

- Improve performance of remote manifest build. (*Suggested by Jens Wilke.*)
- Fix detection of keepalive options on Linux. (*Contributed by Marc Cousin. Reviewed by David Steele.*)
- Add configure host detection to set standards flags correctly. (*Contributed by Marc Cousin. Reviewed by David Steele.*)
- Remove `compress`/`compress-level` options from commands where unused. These commands (e.g. `restore`, `archive-get`) never used the compress options but allowed them to be passed on the command line. Now they will error when these options are passed on the command line. If these errors occur then remove the unused options. (*Reviewed by Cynthia Shang.*)
- Limit backup file copy size to size reported at backup start. If a file grows during the backup it will be reconstructed by WAL replay during recovery so there is no need to copy the additional data. (*Reviewed by Cynthia Shang.*)


### v2.24 Release Notes

*Auto-Select Backup Set for Time Target*

*Released February 25, 2020*

**Bug Fixes:**

- Prevent defunct processes in asynchronous archive commands. (*Reviewed by Stephen Frost. Reported by Adam Brusselback, ejberdecia.*)
- Error when `archive-get`/`archive-push`/`restore` are not run on a PostgreSQL host. (*Reviewed by Stephen Frost. Reported by Jesper St John.*)
- Read HTTP content to eof when size/encoding not specified. (*Reviewed by Cynthia Shang. Reported by Christian ROUX.*)
- Fix resume when the resumable backup was created by Perl. In this case the resumable backup should be ignored, but the C code was not able to load the partial manifest written by Perl since the format differs slightly. Add validations to catch this case and continue gracefully. (*Reported by Kacey Holston.*)

**Features:**

- Auto-select backup set on restore when time target is specified. Auto-selection is performed only when `--set` is not specified. If a backup set for the given target time cannot not be found, the latest (default) backup set will be used. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Improvements:**

- Skip `pg_internal.init` temp file during backup. (*Reviewed by Cynthia Shang. Suggested by Michael Paquier.*)
- Add more validations to the manifest on `backup`. (*Reviewed by Cynthia Shang.*)

**Documentation Improvements:**

- Prevent lock-bot from adding comments to locked issues. (*Suggested by Christoph Berg.*)


### v2.23 Release Notes

*Bug Fix*

*Released January 27, 2020*

**Bug Fixes:**

- Fix missing files corrupting the manifest. If a file was removed by PostgreSQL during the backup (or was missing from the standby) then the next file might not be copied and updated in the manifest. If this happened then the backup would error when restored. (*Reviewed by Cynthia Shang. Reported by Vitaliy Kukharik.*)

**Improvements:**

- Use `pkg-config` instead of `xml2-config` for libxml2 build options. (*Contributed by David Steele, Adrian Vondendriesch.*)
- Validate checksums are set in the manifest on `backup`/`restore`. (*Reviewed by Cynthia Shang.*)


### v2.22 Release Notes

*Bug Fix*

*Released January 21, 2020*

**Bug Fixes:**

- Fix error in timeline conversion. The timeline is required to verify WAL segments in the archive after a backup. The conversion was performed base `10` instead of `16`, which led to errors when the timeline was ≥ `0xA`. (*Reported by Lukas Ertl, Eric Veldhuyzen.*)


### v2.21 Release Notes

*C Migration Complete*

*Released January 15, 2020*

**Bug Fixes:**

- Fix options being ignored by asynchronous commands. The asynchronous `archive-get`/`archive-push` processes were not loading options configured in command configuration sections, e.g. `[global:archive-get]`. (*Reviewed by Cynthia Shang. Reported by Urs Kramer.*)
- Fix handling of `\` in filenames. `\` was not being properly escaped when calculating the manifest checksum which prevented the manifest from loading. Since instances of `\` in cluster filenames should be rare to nonexistent this does not seem likely to be a serious problem in the field.

**Features:**

- pgBackRest is now pure C.
- Add `pg-user` option. Specifies the database user name when connecting to PostgreSQL. If not specified pgBackRest will connect with the local OS user or `PGUSER`, which was the previous behavior. (*Contributed by Mike Palmiotto. Reviewed by David Steele.*)
- Allow path-style URIs in S3 driver.

**Improvements:**

- The `backup` command is implemented entirely in C. (*Reviewed by Cynthia Shang.*)


### v2.20 Release Notes

*Bug Fixes*

*Released December 12, 2019*

**Bug Fixes:**

- Fix archive-push/archive-get when `PGDATA` is symlinked. These commands tried to use `cwd()` as `PGDATA` but this would disagree with the path configured in pgBackRest if `PGDATA` was symlinked. If `cwd()` does not match the pgBackRest path then `chdir()` to the path and make sure the next `cwd()` matches the result from the first call. (*Reported by Stephen Frost, Milosz Suchy.*)
- Fix reference list when `backup.info` is reconstructed in `expire` command. Since the `backup` command is still using the Perl version of reconstruct this issue will not express unless **1)** there is a backup missing from `backup.info` and **2)** the `expire` command is run directly instead of running after `backup` as usual. This unlikely combination of events means this is probably not a problem in the field.
- Fix segfault on unexpected EOF in gzip decompression. (*Reported by Stephen Frost.*)


### v2.19 Release Notes

*C Migrations and Bug Fixes*

*Released November 12, 2019*

**Bug Fixes:**

- Fix remote timeout in delta restore. When performing a delta restore on a largely unchanged cluster the remote could timeout if no files were fetched from the repository within `protocol-timeout`. Add keep-alives to prevent remote timeout. (*Reported by James Sewell, Jens Wilke.*)
- Fix handling of repeated HTTP headers. When HTTP headers are repeated they should be considered equivalent to a single comma-separated header rather than generating an error, which was the prior behavior. (*Reported by donicrosby.*)

**Improvements:**

- JSON output from the `info` command is no longer pretty-printed. Monitoring systems can more easily ingest the JSON without linefeeds. External tools such as `jq` can be used to pretty-print if desired. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- The `check` command is implemented entirely in C. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Documentation Improvements:**

- Document how to contribute to pgBackRest. (*Contributed by Cynthia Shang, David Steele.*)
- Document maximum version for `auto-stop` option. (*Contributed by Brad Nicholson. Reviewed by David Steele.*)

**Test Suite Improvements:**

- Fix container test path being used when `--vm=none`. (*Suggested by Stephen Frost.*)
- Fix mismatched timezone in expect test. (*Suggested by Stephen Frost.*)
- Don't autogenerate embedded libc code by default. (*Suggested by Stephen Frost.*)


### v2.18 Release Notes

*PostgreSQL 12 Support*

*Released October 1, 2019*

**Features:**

- PostgreSQL 12 support.
- Add `info` command `set` option for detailed text output. The additional details include databases that can be used for selective restore and a list of tablespaces and symlinks with their default destinations. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Stephen Frost, ejberdecia.*)
- Add `standby` restore type. This restore type automatically adds standby_mode=on to recovery.conf for PostgreSQL < 12 and creates `standby.signal` for PostgreSQL ≥ 12, creating a common interface between PostgreSQL versions. (*Reviewed by Cynthia Shang.*)

**Improvements:**

- The `restore` command is implemented entirely in C. (*Reviewed by Cynthia Shang.*)

**Documentation Improvements:**

- Document the relationship between `db-timeout` and `protocol-timeout`. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by James Chanco Jr.*)
- Add documentation clarifications regarding standby repositories. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Add FAQ for time-based Point-in-Time Recovery. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v2.17 Release Notes

*C Migrations and Bug Fixes*

*Released September 3, 2019*

**Bug Fixes:**

- Improve slow manifest build for very large quantities of tables/segments. (*Reported by Jens Wilke.*)
- Fix exclusions for special files. (*Reported by CluelessTechnologist, Janis Puris, Rachid Broum.*)

**Improvements:**

- The `stanza-create/update/delete` commands are implemented entirely in C. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- The `start`/`stop` commands are implemented entirely in C. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Create log directories/files with `0750`/`0640` mode. (*Suggested by Damiano Albani.*)

**Documentation Bug Fixes:**

- Fix `yum.p.o` package being installed when custom package specified. (*Reported by Joe Ayers, John Harvey.*)

**Documentation Improvements:**

- Build pgBackRest as an unprivileged user. (*Suggested by Laurenz Albe.*)


### v2.16 Release Notes

*C Migrations and Bug Fixes*

*Released August 5, 2019*

**Bug Fixes:**

- Retry S3 `RequestTimeTooSkewed` errors instead of immediately terminating. (*Reported by sean0101n, Tim Garton, Jesper St John, Aleš Zelený.*)
- Fix incorrect handling of `transfer-encoding` response to `HEAD` request. (*Reported by Pavel Suderevsky.*)
- Fix scoping violations exposed by optimizations in gcc 9. (*Reported by Christian Lange, Ned T. Crigler.*)

**Features:**

- Add `repo-s3-port` option for setting a non-standard S3 service port.

**Improvements:**

- The `local` command for `backup` is implemented entirely in C. (*Contributed by David Steele, Cynthia Shang.*)
- The `check` command is implemented partly in C. (*Reviewed by Cynthia Shang.*)


### v2.15 Release Notes

*C Implementation of Expire*

*Released June 25, 2019*

**Bug Fixes:**

- Fix archive retention expiring too aggressively. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Mohamad El-Rifai.*)

**Improvements:**

- The `expire` command is implemented entirely in C. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- The `local` command for restore is implemented entirely in C.
- Remove hard-coded PostgreSQL user so `$PGUSER` works. (*Suggested by Julian Zhang, Janis Puris.*)
- Honor configure `--prefix` option. (*Suggested by Daniel Westermann.*)
- Rename `repo-s3-verify-ssl` option to `repo-s3-verify-tls`. The new name is preferred because pgBackRest does not support any SSL protocol versions (they are all considered to be insecure). The old name will continue to be accepted.

**Documentation Improvements:**

- Add FAQ to the documentation. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Use `wal_level=replica` in the documentation for PostgreSQL ≥ 9.6. (*Suggested by Patrick McLaughlin.*)


### v2.14 Release Notes

*Bug Fix and Improvements*

*Released May 20, 2019*

**Bug Fixes:**

- Fix segfault when `process-max` > 8 for `archive-push`/`archive-get`. (*Reported by Jens Wilke.*)

**Improvements:**

- Bypass database checks when `stanza-delete` issued with `force`. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by hatifnatt.*)
- Add `configure` script for improved multi-platform support.

**Documentation Features:**

- Add user guides for CentOS/RHEL 6/7.


### v2.13 Release Notes

*Bug Fixes*

*Released April 18, 2019*

**Bug Fixes:**

- Fix zero-length reads causing problems for IO filters that did not expect them. (*Reported by brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru.*)
- Fix reliability of error reporting from `local`/`remote` processes.
- Fix Posix/CIFS error messages reporting the wrong filename on write/sync/close.


### v2.12 Release Notes

*C Implementation of Archive Push*

*Released April 11, 2019*

**IMPORTANT NOTE**: The new TLS/SSL implementation forbids dots in S3 bucket names per RFC-2818. This security fix is required for compliant hostname verification.

**Bug Fixes:**

- Fix issues when a path option is / terminated. (*Reported by Marc Cousin.*)
- Fix issues when `log-level-file=off` is set for the `archive-get` command. (*Reported by Brad Nicholson.*)
- Fix C code to recognize `host:port` option format like Perl does. (*Reported by Kyle Nevins.*)
- Fix issues with `remote`/`local` command logging options.

**Improvements:**

- The `archive-push` command is implemented entirely in C.
- Increase `process-max` limit to `999`. (*Suggested by Rakshitha-BR.*)
- Improve error message when an S3 bucket name contains dots.

**Documentation Improvements:**

- Clarify that S3-compatible object stores are supported. (*Suggested by Magnus Hagander.*)


### v2.11 Release Notes

*C Implementation of Archive Get*

*Released March 11, 2019*

**Bug Fixes:**

- Fix possible truncated WAL segments when an error occurs mid-write. (*Reported by blogh.*)
- Fix info command missing WAL min/max when stanza specified. (*Fixed by Stefan Fercot. Reviewed by David Steele.*)
- Fix non-compliant JSON for options passed from C to Perl. (*Reported by Leo Khomenko.*)

**Improvements:**

- The `archive-get` command is implemented entirely in C.
- Enable socket keep-alive on older Perl versions. (*Contributed by Marc Cousin. Reviewed by David Steele.*)
- Error when parameters are passed to a command that does not accept parameters. (*Suggested by Jason O'Donnell.*)
- Add hints when unable to find a WAL segment in the archive. (*Suggested by Hans-Jürgen Schönig.*)
- Improve error when hostname cannot be found in a certificate. (*Suggested by James Badger.*)
- Add additional options to `backup.manifest` for debugging purposes. (*Contributed by blogh. Reviewed by David Steele.*)

**Documentation Improvements:**

- Update default documentation version to PostgreSQL 10.


### v2.10 Release Notes

*Bug Fixes*

*Released February 9, 2019*

**Bug Fixes:**

- Add unimplemented S3 driver method required for `archive-get`. (*Reported by mibiio.*)
- Fix check for improperly configured `pg-path`. (*Reported by James Chanco Jr.*)


### v2.09 Release Notes

*Minor Improvements and Bug Fixes*

*Released January 30, 2019*

**Bug Fixes:**

- Fix issue with multiple async status files causing a hard error. (*Reported by Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley.*)

**Improvements:**

- The `info` command is implemented entirely in C. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Simplify `info` command text message when no stanzas are present. Replace the repository path with "the repository".
- Add `_DARWIN_C_SOURCE` flag to Makefile for MacOS builds. (*Contributed by Douglas J Hunley. Reviewed by David Steele.*)
- Update address lookup in C TLS client to use modern methods. (*Suggested by Bruno Friedmann.*)
- Include Posix-compliant header for `strcasecmp()` and `fd_set`. (*Suggested by ucando.*)

**Documentation Bug Fixes:**

- Fix hard-coded repository path. (*Reported by Heath Lord.*)

**Documentation Improvements:**

- Clarify that encryption is always performed client-side. (*Suggested by Bruce Burdick.*)
- Add examples for building a documentation host.
- Allow `if` in manifest variables, lists, and list items.


### v2.08 Release Notes

*Minor Improvements and Bug Fixes*

*Released January 2, 2019*

**Bug Fixes:**

- Remove request for S3 object info directly after putting it. (*Reported by Matt Kunkel.*)
- Correct `archive-get-queue-max` to be `size` type. (*Reported by Ronan Dunklau.*)
- Add error message when current user `uid`/`gid` does not map to a name. (*Reported by Camilo Aguilar.*)
- Error when `--target-action=shutdown` specified for PostgreSQL < 9.5.

**Improvements:**

- Set TCP keepalives on S3 connections. (*Suggested by Ronan Dunklau.*)
- Reorder `info` command text output so most recent backup is output last. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Ryan Lambert.*)
- Change file ownership only when required.
- Redact `authentication` header when throwing S3 errors. (*Suggested by Brad Nicholson.*)

**Documentation Improvements:**

- Clarify when `target-action` is effective and PostgreSQL version support. (*Suggested by Keith Fiske.*)
- Clarify that region/endpoint must be configured correctly for the bucket. (*Suggested by Pritam Barhate.*)
- Add documentation for building the documentation.


### v2.07 Release Notes

*Automatic Backup Checksum Delta*

*Released November 16, 2018*

**Bug Fixes:**

- Fix issue with `archive-push-queue-max` not being honored on connection error. (*Reported by Lardière Sébastien.*)
- Fix static WAL segment size used to determine if `archive-push-queue-max` has been exceeded.
- Fix error after log file open failure when processing should continue. (*Reported by vthriller.*)

**Features:**

- Automatically enable backup checksum delta when anomalies (e.g. timeline switch) are detected. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Improvements:**

- Retry all S3 `5xx` errors rather than just `500` internal errors. (*Suggested by Craig A. James.*)


### v2.06 Release Notes

*Checksum Delta Backup and PostgreSQL 11 Support*

*Released October 15, 2018*

**Bug Fixes:**

- Fix missing URI encoding in S3 driver. (*Reported by Dan Farrell.*)
- Fix incorrect error message for duplicate options in configuration files. (*Reported by Jesper St John.*)
- Fix incorrectly reported error return in `info` logging. A return code of 1 from the `archive-get` was being logged as an error message at `info` level but otherwise worked correctly.

**Features:**

- Add checksum delta for incremental backups. Checksum delta backups uses checksums rather than timestamps to determine if files have changed. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- PostgreSQL 11 support, including configurable WAL segment size.

**Improvements:**

- Ignore all files in a linked tablespace directory except the subdirectory for the current version of PostgreSQL. Previously an error would be generated if other files were present and not owned by the PostgreSQL user.
- Improve `info` command to display the stanza cipher type. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Douglas J Hunley.*)
- Improve support for special characters in filenames.
- Allow `delta` option to be specified in the pgBackRest configuration file. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Documentation Improvements:**

- Use `command` in `authorized_hosts` to improve SSH security. (*Suggested by Stephen Frost, Magnus Hagander.*)
- List allowable values for the `buffer-size` option in the configuration reference. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Stéphane Schildknecht.*)


### v2.05 Release Notes

*Environment Variable Options and Exclude Temporary/Unlogged Relations*

*Released August 31, 2018*

**Bug Fixes:**

- Fix issue where *relative* links in `$PGDATA` could be stored in the backup with the wrong path. This issue did not affect absolute links and relative tablespace links were caught by other checks. (*Reported by Cynthia Shang.*)
- Remove incompletely implemented `online` option from the `check` command. Offline operation runs counter to the purpose of this command, which is to check if archiving and backups are working correctly. (*Reported by Jason O'Donnell.*)
- Fix issue where errors raised in C were not logged when called from Perl. pgBackRest properly terminated with the correct error code but lacked an error message to aid in debugging. (*Reported by Douglas J Hunley.*)
- Fix issue when a boolean option (e.g. `delta`) was specified more than once. (*Reported by Yogesh Sharma.*)

**Features:**

- Allow any option to be set in an environment variable. This includes options that previously could only be specified on the command line, e.g. `stanza`, and secret options that could not be specified on the command-line, e.g. `repo1-s3-key-secret`.
- Exclude temporary and unlogged relation (table/index) files from backup. Implemented using the same logic as the patches adding this feature to PostgreSQL, [8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25) and [920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f). Temporary relation exclusion is enabled in PostgreSQL ≥ `9.0`. Unlogged relation exclusion is enabled in PostgreSQL ≥ `9.1`, where the feature was introduced. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Allow arbitrary directories and/or files to be excluded from a backup. Misuse of this feature can lead to inconsistent backups so read the `--exclude` documentation carefully before using. (*Reviewed by Cynthia Shang.*)
- Add `log-subprocess` option to allow file logging for `local` and `remote` subprocesses.
- PostgreSQL 11 Beta 3 support.

**Improvements:**

- Allow zero-size files in backup manifest to reference a prior manifest regardless of timestamp delta. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Improve asynchronous `archive-get`/`archive-push` performance by directly checking status files. (*Contributed by Stephen Frost. Reviewed by David Steele.*)
- Improve error message when a command is missing the `stanza` option. (*Suggested by Sarah Conway.*)

**Documentation Bug Fixes:**

- Fix invalid log level in `log-path` option reference. (*Reported by Camilo Aguilar.*)

**Documentation Improvements:**

- Stop trying to arrange contributors in `release.xml` by last/first name. Contributor names have always been presented in the release notes exactly as given, but we tried to assign internal IDs based on last/first name which can be hard to determine and ultimately doesn't make sense. Inspired by Christophe's PostgresOpen 2017 talk, "Human Beings Do Not Have a Primary Key". (*Suggested by Christophe Pettus.*)

**Test Suite Improvements:**

- Error if LibC build is performed outside the test environment. LibC is no longer required for production builds.


### v2.04 Release Notes

*Critical Bug Fix for Backup Resume*

*Released July 5, 2018*

**IMPORTANT NOTE**: This release fixes a critical bug in the backup resume feature. All resumed backups prior to this release should be considered inconsistent. A backup will be resumed after a prior backup fails, unless `resume=n` has been specified. A resumed backup can be identified by checking the backup log for the message "aborted backup of same type exists, will be cleaned to remove invalid files and resumed". If the message exists, do not use this backup or any backup in the same set for a restore and check the restore logs to see if a resumed backup was restored. If so, there may be inconsistent data in the cluster.

**Bug Fixes:**

- Fix critical bug in resume that resulted in inconsistent backups. A regression in `v0.82` removed the timestamp comparison when deciding which files from the aborted backup to keep on resume. See note above for more details. (*Reported by David Youatt, Yogesh Sharma, Stephen Frost.*)
- Fix error in selective restore when only one user database exists in the cluster. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Nj Baliyan.*)
- Fix non-compliant ISO-8601 timestamp format in S3 authorization headers. AWS and some gateways were tolerant of space rather than zero-padded hours while others were not. (*Fixed by Andrew Schwartz. Reviewed by David Steele.*)

**Features:**

- PostgreSQL 11 Beta 2 support.

**Improvements:**

- Improve the HTTP client to set `content-length` to 0 when not specified by the server. S3 (and gateways) always set `content-length` or `transfer-encoding` but `HTTP 1.1` does not require it and proxies (e.g. HAProxy) may not include either. (*Suggested by Adam K. Sumner.*)
- Set `search_path = 'pg_catalog'` on PostgreSQL connections. (*Suggested by Stephen Frost.*)

**Documentation Improvements:**

- Create a new section to describe building pgBackRest and build on a separate host.
- Add sample S3 policy to restrict bucket privileges. (*Suggested by Douglas J Hunley, Jason O'Donnell.*)


### v2.03 Release Notes

*Single Executable to Deploy*

*Released May 22, 2018*

**Bug Fixes:**

- Fix potential buffer overrun in error message handling. (*Reported by Lætitia.*)
- Fix archive write lock being taken for the synchronous `archive-get` command. (*Reported by uspen.*)

**Improvements:**

- Embed exported C functions and Perl modules directly into the pgBackRest executable.
- Use `time_t` instead of `__time_t` for better portability. (*Suggested by Nick Floersch.*)
- Print total runtime in milliseconds at command end.


### v2.02 Release Notes

*Parallel Asynchronous Archive Get and Configuration Includes*

*Released May 6, 2018*

**Bug Fixes:**

- Fix directory syncs running recursively when only the specified directory should be synced. (*Reported by Craig A. James.*)
- Fix `archive-copy` throwing "path not found" error for incr/diff backups. (*Reported by yummyliu, Vitaliy Kukharik.*)
- Fix failure in manifest build when two or more files in `PGDATA` are linked to the same directory. (*Reported by Vitaliy Kukharik.*)
- Fix delta restore failing when a linked file is missing.
- Fix rendering of key/value and list options in help. (*Reported by Clinton Adams.*)

**Features:**

- Add asynchronous, parallel `archive-get`. This feature maintains a queue of WAL segments to help reduce latency when PostgreSQL requests a WAL segment with restore_command.
- Add support for additional pgBackRest configuration files. The directory is specified by the `--config-include-path` option. Add `--config-path` option for overriding the default base path of the `--config` and `--config-include-path` option. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Add `repo-s3-token` option to allow temporary credentials tokens to be configured. pgBackRest currently has no way to request new credentials so the entire command (e.g. `backup`, `restore`) must complete before the credentials expire. (*Contributed by Yogesh Sharma. Reviewed by David Steele.*)

**Improvements:**

- Update the `archive-push-queue-max`, `manifest-save-threshold`, and `buffer-size` options to accept values in `KB`, `MB`, `GB`, `TB`, or `PB` where the multiplier is a power of `1024`. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Make backup/restore path sync more efficient. Scanning the entire directory can be very expensive if there are a lot of small tables. The backup manifest contains the path list so use it to perform syncs instead of scanning the backup/restore path.
- Show command parameters as well as command options in initial info log message.
- Rename archive-queue-max option to archive-push-queue-max. This is consistent with the new `archive-get-queue-max` option. The old option name will continue to be accepted.

**Documentation Bug Fixes:**

- Update docs with 32-bit support and caveats. 32-bit support was added in v1.26. (*Reported by Viorel Tabara.*)

**Documentation Improvements:**

- Add monitoring examples using PostgreSQL and jq. (*Suggested by Stephen Frost, Brian Faherty.*)
- Add example of command section usage to archiving configuration. (*Suggested by Christophe Courtois.*)
- Remove documentation describing `info --output=json` as experimental.
- Update out-of-date description for the `spool-path` option.

**Test Suite Features:**

- Use lcov for C unit test coverage reporting. Switch from Devel::Cover because it would not report on branch coverage for reports converted from gcov. Incomplete branch coverage for a module now generates an error. Coverage of unit tests is not displayed in the report unless they are incomplete for either statement or branch coverage.


### v2.01 Release Notes

*Minor Bug Fixes and Improvements*

*Released March 19, 2018*

**Bug Fixes:**

- Fix `--target-action` and `--recovery-option` options being reported as invalid when restoring with `--type=immediate`. (*Reported by Brad Nicholson.*)
- Immediately error when a secure option (e.g. `repo1-s3-key`) is passed on the command line. Since pgBackRest would not pass secure options on to sub-processes an obscure error was thrown. The new error is much clearer and provides hints about how to fix the problem. Update command documentation to omit secure options that cannot be specified on the command-line. (*Reported by Brad Nicholson.*)
- Fix issue passing `--no-config` to embedded Perl. (*Reported by Ibrahim Edib Kokdemir.*)
- Fix issue where specifying `log-level-stderr` > `warn` would cause a `local`/`remote` process to error on exit due to output found on stderr when none was expected. The max value for a `local`/`remote` process is now `error` since there is no reason for these processes to emit warnings. (*Reported by Clinton Adams.*)
- Fix manifest test in the `check` command when tablespaces are present. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Thomas Flatley.*)

**Improvements:**

- Error when multiple arguments are set in the config file for an option that does not accept multiple arguments. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Remove extraneous sudo commands from `src/Makefile`. (*Contributed by Adrian Vondendriesch. Reviewed by David Steele.*)

**Documentation Improvements:**

- Show index in examples for indexed options, i.e. `repo-*`, `pg-*`. (*Suggested by Stephen Frost.*)
- Simplify table of contents on command page by only listing commands. (*Suggested by Stephen Frost.*)
- Remove references to the C library being optional.

**Test Suite Features:**

- Add CentOS/RHEL package builds.
- Use clang for static code analysis. Nothing found initially except for some functions that should have been marked `__noreturn__`.


### v2.00 Release Notes

*Performance Improvements for Archive Push*

*Released February 23, 2018*

**Features:**

- The `archive-push` command is now partially coded in C which allows the PostgreSQL `archive_command` to run significantly faster when processing status messages from the asynchronous archive process. (*Reviewed by Cynthia Shang.*)

**Improvements:**

- Improve `check` command to verify that the backup manifest can be built. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Improve performance of HTTPS client. Buffering now takes the `pending` bytes on the socket into account (when present) rather than relying entirely on `select()`. In some instances the final bytes would not be flushed until the connection was closed.
- Improve S3 delete performance. The constant `S3_BATCH_MAX` had been replaced with a hard-coded value of 2, probably during testing.
- Allow any non-command-line option to be reset to default on the command-line. This allows options in `pgbackrest.conf` to be reset to default which reduces the need to write new configuration files for specific needs.
- The C library is now required. This eliminates conditional loading and eases development of new library features.
- The `pgbackrest` executable is now a C binary instead of Perl. This allows certain time-critical commands (like async `archive-push`) to run more quickly.
- Rename `db-*` options to `pg-*` and `backup-*` options to `repo-*` to improve consistency. `repo-*` options are now indexed although currently only one is allowed.

**Documentation Features:**

- All clusters in the documentation are initialized with checksums.

**Documentation Improvements:**

- List deprecated option names in documentation and command-line help.
- Clarify that S3 buckets must be created by the user. (*Suggested by David Youatt.*)


### v1.29 Release Notes

*Critical Bug Fix for Backup Resume*

*Released July 5, 2018*

**IMPORTANT NOTE**: This release fixes a critical bug in the backup resume feature. All resumed backups prior to this release should be considered inconsistent. A backup will be resumed after a prior backup fails, unless `resume=n` has been specified. A resumed backup can be identified by checking the backup log for the message "aborted backup of same type exists, will be cleaned to remove invalid files and resumed". If the message exists, do not use this backup or any backup in the same set for a restore and check the restore logs to see if a resumed backup was restored. If so, there may be inconsistent data in the cluster.

**Bug Fixes:**

- Fix critical bug in resume that resulted in inconsistent backups. A regression in `v0.82` removed the timestamp comparison when deciding which files from the aborted backup to keep on resume. See note above for more details. (*Reported by David Youatt, Yogesh Sharma, Stephen Frost.*)
- Fix non-compliant ISO-8601 timestamp format in S3 authorization headers. AWS and some gateways were tolerant of space rather than zero-padded hours while others were not. (*Fixed by Andrew Schwartz. Reviewed by David Steele.*)
- Fix directory syncs running recursively when only the specified directory should be synced. (*Reported by Craig A. James.*)
- Fix `--target-action` and `--recovery-option` options being reported as invalid when restoring with `--type=immediate`. (*Reported by Brad Nicholson.*)
- Fix `archive-copy` throwing "path not found" error for incr/diff backups. (*Reported by yummyliu, Vitaliy Kukharik.*)
- Fix failure in manifest build when two or more files in `PGDATA` are linked to the same directory. (*Reported by Vitaliy Kukharik.*)
- Fix delta restore failing when a linked file was missing.
- Fix error in selective restore when only one user database exists in the cluster. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Nj Baliyan.*)

**Improvements:**

- Improve the HTTP client to set `content-length` to 0 when not specified by the server. S3 (and gateways) always set `content-length` or `transfer-encoding` but `HTTP 1.1` does not require it and proxies (e.g. HAProxy) may not include either. (*Suggested by Adam K. Sumner.*)
- Improve performance of HTTPS client. Buffering now takes the `pending` bytes on the socket into account (when present) rather than relying entirely on `select()`. In some instances the final bytes would not be flushed until the connection was closed.
- Improve S3 delete performance. The constant `S3_BATCH_MAX` had been replaced with a hard-coded value of 2, probably during testing.
- Make backup/restore path sync more efficient. Scanning the entire directory can be very expensive if there are a lot of small tables. The backup manifest contains the path list so use it to perform syncs instead of scanning the backup/restore path. Remove recursive path sync functionality since it is no longer used.

**Documentation Bug Fixes:**

- Update docs with 32-bit support and caveats. 32-bit support was added in v1.26. (*Reported by Viorel Tabara.*)

**Documentation Improvements:**

- Clarify that S3 buckets must be created by the user. (*Suggested by David Youatt.*)
- Update out-of-date description for the `spool-path` option.


### v1.28 Release Notes

*Stanza Delete*

*Released February 1, 2018*

**Bug Fixes:**

- Fixed inability to restore a single database contained in a tablespace using --db-include. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Chiranjeevi Ravilla.*)
- Ensure latest `db-id` is selected on when matching `archive.info` to `backup.info`. This provides correct matching in the event there are `system-id` and `db-version` duplicates (e.g. after reverting a `pg_upgrade`). (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Adam K. Sumner.*)
- Fixed overly chatty error message when reporting an invalid command. (*Reported by Jason O'Donnell.*)

**Features:**

- Add `stanza-delete` command to cleanup unused stanzas. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Magnus Hagander.*)

**Improvements:**

- Improve `stanza-create` command so that it does not error when the stanza already exists. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Documentation Improvements:**

- Update `stanza-create --force` documentation to urge caution when using. (*Suggested by Jason O'Donnell.*)


### v1.27 Release Notes

*Bug Fixes and Documentation*

*Released December 19, 2017*

**Bug Fixes:**

- Fixed an issue that suppressed locality errors for `backup` and `restore`. When a backup host is present, backups should only be allowed on the backup host and restores should only be allowed on the database host unless an alternate configuration is created that ignores the remote host. (*Reported by Lardière Sébastien.*)
- Fixed an issue where WAL was not expired on PostgreSQL 10. This was caused by a faulty regex that expected all PostgreSQL major versions to be X.X. (*Reported by Adam Brusselback.*)
- Fixed an issue where the `--no-config` option was not passed to child processes. This meant the child processes would still read the local config file and possibly cause unexpected behaviors.
- Fixed `info` command to eliminate `"db (prior)"` output if no backups or archives exist for a prior version of the cluster. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Stephen Frost.*)

**Documentation Features:**

- Document the relationship between the `archive-copy` and `archive-check` options. (*Suggested by Markus Nullmeier.*)
- Improve `archive-copy` reference documentation.


### v1.26 Release Notes

*Repository Encryption*

*Released November 21, 2017*

**Bug Fixes:**

- Fixed an issue that could cause copying large manifests to fail during restore. (*Reported by Craig A. James.*)
- Fixed incorrect WAL offset for 32-bit architectures. (*Fixed by Javier Wilson. Reviewed by David Steele.*)
- Fixed an issue retrieving WAL for old database versions. After a `stanza-upgrade` it should still be possible to restore backups from the previous version and perform recovery with `archive-get`. However, archive-get only checked the most recent db version/id and failed. Also clean up some issues when the same db version/id appears multiple times in the history. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Clinton Adams.*)
- Fixed an issue with invalid backup groups being set correctly on restore. If the backup cannot map a group to a name it stores the group in the manifest as `false` then uses either the owner of $PGDATA to set the group during restore or failing that the group of the current user. This logic was not working correctly because the selected group was overwriting the user on restore leaving the group undefined and the user incorrectly set to the group. (*Reported by Jeff McCormick.*)
- Fixed an issue passing parameters to remotes. When more than one db was specified the path, port, and socket path would for db1 were passed no matter which db was actually being addressed. (*Reported by uspen.*)

**Features:**

- Repository encryption support. (*Contributed by Cynthia Shang, David Steele.*)

**Improvements:**

- Disable gzip filter when `--compress-level-network=0`. The filter was used with compress level set to 0 which added overhead without any benefit.
- Inflate performance improvement for gzip filter.

**Documentation Features:**

- Add template to improve initial information gathered for issue submissions. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Documentation Improvements:**

- Clarify usage of the `archive-timeout` option and describe how it is distinct from the PostgreSQL archive_timeout setting. (*Contributed by Cynthia Shang. Reviewed by David Steele. Suggested by Keith Fiske.*)

**Test Suite Features:**

- Automated tests for 32-bit i386/i686 architecture.


### v1.25 Release Notes

*S3 Performance Improvements*

*Released October 24, 2017*

**Bug Fixes:**

- Fix custom settings for `compress-level` option being ignored. (*Reported by Jens Wilke.*)
- Remove error when overlapping timelines are detected. Overlapping timelines are valid in many Point-in-Time-Recovery (PITR) scenarios. (*Reported by blogh.*)
- Fix instances where `database-id` was not rendered as an integer in JSON info output. (*Fixed by Cynthia Shang. Reviewed by David Steele. Reported by Jason O'Donnell.*)

**Features:**

- Improve performance of list requests on S3. Any beginning literal portion of a filter expression is used to generate a search prefix which often helps keep the request small enough to avoid rate limiting. (*Suggested by Mihail Shvein.*)

**Test Suite Features:**

- Add I/O performance tests.


### v1.24 Release Notes

*New Backup Exclusions*

*Released September 28, 2017*

**Bug Fixes:**

- Fixed an issue where warnings were being emitted in place of lower priority log messages during backup from standby initialization. (*Reported by uspen.*)
- Fixed an issue where some `db-*` options (e.g. `db-port`) were not being passed to remotes. (*Reported by uspen.*)

**Features:**

- Exclude contents of `pg_snapshots`, `pg_serial`, `pg_notify`, and `pg_dynshmem` from backup since they are rebuilt on startup.
- Exclude `pg_internal.init` files from backup since they are rebuilt on startup.

**Improvements:**

- Open log file after async process is completely separated from the main process to prevent the main process from also logging to the file. (*Suggested by Jens Wilke.*)

**Documentation Features:**

- Add passwordless SSH configuration.

**Documentation Improvements:**

- Rename master to primary in documentation to align with PostgreSQL convention.


### v1.23 Release Notes

*Multiple Standbys and PostgreSQL 10 Support*

*Released September 3, 2017*

**Bug Fixes:**

- Fixed an issue that could cause compression to abort on growing files. (*Reported by Jesper St John, Aleksandr Rogozin.*)
- Fixed an issue with keep-alives not being sent to the remote from the local process. (*Reported by William Cox.*)

**Features:**

- Up to seven standbys can be configured for backup from standby. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- PostgreSQL 10 support.
- Allow `content-length` (in addition to chunked encoding) when reading XML data to improve compatibility with third-party S3 gateways. (*Suggested by Victor Gdalevich.*)

**Improvements:**

- Increase HTTP timeout for S3.
- Add HTTP retries to harden against transient S3 network errors.

**Documentation Bug Fixes:**

- Fixed document generation to include section summaries on the Configuration page. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)


### v1.22 Release Notes

*Fixed S3 Retry*

*Released August 9, 2017*

**Bug Fixes:**

- Fixed authentication issue in S3 retry.


### v1.21 Release Notes

*Improved Info Output and SSH Port Option*

*Released August 8, 2017*

**Bug Fixes:**

- The `archive_status` directory is now recreated on restore to support PostgreSQL 8.3 which does not recreate it automatically like more recent versions do. (*Reported by Stephen Frost.*)
- Fixed an issue that could cause the empty archive directory for an old PostgreSQL version to be left behind after a `stanza-upgrade`. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)

**Features:**

- Modified the `info` command (both text and JSON output) to display the archive ID and minimum/maximum WAL currently present in the archive for the current and prior, if any, database cluster version. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Added `--backup-ssh-port` and `--db-ssh-port` options to support non-default SSH ports. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Improvements:**

- Retry when S3 returns an internal error (500).

**Documentation Bug Fixes:**

- Fix description of `--online` based on the command context.

**Documentation Features:**

- Add creation of `/etc/pgbackrest.conf` to manual installation instructions.

**Documentation Improvements:**

- Move repository options into a separate section in command/command-line help. (*Suggested by Stephen Frost.*)


### v1.20 Release Notes

*Critical 8.3/8.4 Bug Fix*

*Released June 27, 2017*

**IMPORTANT NOTE**: PostgreSQL 8.3 and 8.4 installations utilizing tablespaces should upgrade immediately from any v1 release and run a full backup. A bug prevented tablespaces from being backed up on these versions only. PostgreSQL ≥ 9.0

**Bug Fixes:**

- Fixed an issue that prevented tablespaces from being backed up on PostgreSQL ≤ 8.4.
- Fixed missing flag in C library build that resulted in a mismatched binary on 32-bit systems. (*Reported by Adrian Vondendriesch.*)

**Features:**

- Add `s3-repo-ca-path` and `s3-repo-ca-file` options to accommodate systems where CAs are not automatically found by `IO::Socket::SSL`, i.e. RHEL7, or to load custom CAs. (*Suggested by Scott Frazer.*)

**Test Suite Features:**

- Add documentation builds to CI.


### v1.19 Release Notes

*S3 Support*

*Released June 12, 2017*

**Bug Fixes:**

- Fixed the `info` command so the WAL archive min/max displayed is for the current database version. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Fixed the `backup` command so the `backup-standby` option is reset (and the backup proceeds on the primary) if the standby is not configured and/or reachable. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Fixed config warnings raised from a remote process causing errors in the master process. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)

**Features:**

- Amazon S3 repository support. (*Reviewed by Cynthia Shang.*)

**Documentation Bug Fixes:**

- Changed invalid `max-archive-mb` option in configuration reference to `archive-queue-max`.
- Fixed missing `sudo` in installation section. (*Fixed by Lætitia. Reviewed by David Steele.*)


### v1.18 Release Notes

*Stanza Upgrade, Refactoring, and Locking Improvements*

*Released April 12, 2017*

**Bug Fixes:**

- Fixed an issue where read-only operations that used local worker processes (i.e. `restore`) were creating write locks that could interfere with parallel `archive-push`. (*Reported by Jens Wilke.*)

**Features:**

- Added the stanza-upgrade command to provide a mechanism for upgrading a stanza after upgrading to a new major version of PostgreSQL. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Added validation of `pgbackrest.conf` to display warnings if options are not valid or are not in the correct section. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Improvements:**

- Simplify locking scheme. Now, only the master process will hold write locks (for `archive-push` and `backup` commands) and not all local and remote worker processes as before.
- Do not set timestamps of files in the backup directories to match timestamps in the cluster directory. This was originally done to enable backup resume, but that process is now implemented with checksums.
- Improved error message when the `restore` command detects the presence of `postmaster.pid`. (*Suggested by Yogesh Sharma.*)
- Renumber return codes between 25 and 125 to avoid PostgreSQL interpreting some as fatal signal exceptions. (*Suggested by Yogesh Sharma.*)


### v1.17 Release Notes

*Page Checksum Bug Fix*

*Released March 13, 2017*

**Bug Fixes:**

- Fixed an issue where newly initialized (but unused) pages would cause page checksum warnings. (*Reported by Stephen Frost.*)


### v1.16 Release Notes

*Page Checksum Improvements, CI, and Package Testing*

*Released March 2, 2017*

**Bug Fixes:**

- Fixed an issue where tables over 1GB would report page checksum warnings after the first segment. (*Reported by Stephen Frost.*)
- Fixed an issue where databases created with a non-default tablespace would raise bogus warnings about `pg_filenode.map` and `pg_internal.init` not being page aligned. (*Reported by blogh.*)

**Test Suite Features:**

- Continuous integration using `travis-ci`.
- Automated builds of Debian packages for all supported distributions.


### v1.15 Release Notes

*Refactoring and Bug Fixes*

*Released February 13, 2017*

**Bug Fixes:**

- Fixed a regression introduced in v1.13 that could cause backups to fail if files were removed (e.g. tables dropped) while the manifest was being built. (*Reported by Navid Golpayegani.*)


### v1.14 Release Notes

*Refactoring and Bug Fixes*

*Released February 13, 2017*

**Bug Fixes:**

- Fixed an issue where an archive-push error would not be retried and would instead return errors to PostgreSQL indefinitely (unless the `.error` file was manually deleted). (*Reported by Jens Wilke.*)
- Fixed a race condition in parallel archiving where creation of new paths generated an error when multiple processes attempted to do so at the same time. (*Reported by Jens Wilke.*)

**Improvements:**

- Improved performance of `wal archive min/max` provided by the `info` command. (*Suggested by Jens Wilke.*)

**Documentation Features:**

- Updated async archiving documentation to more accurately describe how the new method works and how it differs from the old method. (*Suggested by Jens Wilke.*)


### v1.13 Release Notes

*Parallel Archiving, Stanza Create, Improved Info and Check*

*Released February 5, 2017*

**IMPORTANT NOTE**: The new implementation of asynchronous archiving no longer copies WAL to a separate queue. If there is any WAL left over in the old queue after upgrading to `1.13`, it will be abandoned and **not** pushed to the repository. To prevent this outcome, stop archiving by setting `archive_command = false`. Next, drain the async queue by running `pgbackrest --stanza=[stanza-name] archive-push` and wait for the process to complete. Check that the queue in `[spool-path]/archive/[stanza-name]/out` is empty. Finally, install `1.13` and restore the original `archive_command`. **IMPORTANT NOTE**: The `stanza-create` command is not longer optional and must be executed before backup or archiving can be performed on a **new** stanza. Pre-existing stanzas do not require `stanza-create` to be executed.

**Bug Fixes:**

- Fixed const assignment giving compiler warning in C library. (*Fixed by Adrian Vondendriesch. Reviewed by David Steele.*)
- Fixed a few directory syncs that were missed for the `--repo-sync` option.
- Fixed an issue where a missing user/group on restore could cause an "uninitialized value" error in `File->owner()`. (*Reported by Leonardo GG Avellar.*)
- Fixed an issue where protocol mismatch errors did not output the expected value.
- Fixed a spurious `archive-get` log message that indicated an exit code of 1 was an abnormal termination.

**Features:**

- Improved, multi-process implementation of asynchronous archiving.
- Improved `stanza-create` command so that it can repair broken repositories in most cases and is robust enough to be made mandatory. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Improved `check` command to run on a standby, though only basic checks are done because `pg_switch_xlog()` cannot be executed on a replica. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Added archive and backup WAL ranges to the `info` command.
- Added warning to update `pg_tablespace.spclocation` when remapping tablespaces in PostgreSQL < 9.2. (*Contributed by blogh. Reviewed by David Steele.*)
- Remove remote lock requirements for the `archive-get`, `restore`, `info`, and `check` commands since they are read-only operations. (*Suggested by Michael Vitale.*)

**Improvements:**

- Log file banner is not output until the first log entry is written. (*Suggested by Jens Wilke.*)
- Reduced the likelihood of torn pages causing a false positive in page checksums by filtering on start backup LSN.
- Remove Intel-specific optimization from C library build flags. (*Contributed by Adrian Vondendriesch. Reviewed by David Steele.*)
- Remove `--lock` option. This option was introduced before the lock directory could be located outside the repository and is now obsolete.
- Added `--log-timestamp` option to allow timestamps to be suppressed in logging. This is primarily used to avoid filters in the automated documentation.
- Return proper error code when unable to convert a relative path to an absolute path. (*Suggested by Yogesh Sharma.*)

**Documentation Features:**

- Added documentation to the User Guide for the `process-max` option. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v1.12 Release Notes

*Page Checksums, Configuration, and Bug Fixes*

*Released December 12, 2016*

**IMPORTANT NOTE**: In prior releases it was possible to specify options on the command-line that were invalid for the current command without getting an error. An error will now be generated for invalid options so it is important to carefully check command-line options in your environment to prevent disruption.

**Bug Fixes:**

- Fixed an issue where options that were invalid for the specified command could be provided on the command-line without generating an error. The options were ignored and did not cause any change in behavior, but it did lead to some confusion. Invalid options will now generate an error. (*Reported by Nikhilchandra Kulkarni.*)
- Fixed an issue where internal symlinks were not being created for tablespaces in the repository. This issue was only apparent when trying to bring up clusters in-place manually using filesystem snapshots and did not affect normal backup and restore.
- Fixed an issue that prevented errors from being output to the console before the logging system was initialized, i.e. while parsing options. Error codes were still being returned accurately so this would not have made a process look like it succeeded when it did not. (*Reported by Adrian Vondendriesch.*)
- Fixed an issue where the `db-port` option specified on the backup server would not be properly passed to the remote unless it was from the first configured database. (*Reported by Michael Vitale.*)

**Features:**

- Added the `--checksum-page` option to allow pgBackRest to validate page checksums in data files when checksums are enabled on PostgreSQL >= 9.3. Note that this functionality requires a C library which may not initially be available in OS packages. The option will automatically be enabled when the library is present and checksums are enabled on the cluster. (*Suggested by Stephen Frost.*)
- Added the `--repo-link` option to allow internal symlinks to be suppressed when the repository is located on a filesystem that does not support symlinks. This does not affect any pgBackRest functionality, but the convenience link `latest` will not be created and neither will internal tablespace symlinks, which will affect the ability to bring up clusters in-place manually using filesystem snapshots.
- Added the `--repo-sync` option to allow directory syncs in the repository to be disabled for file systems that do not support them, e.g. NTFS.
- Added a predictable log entry to signal that a command has completed successfully. For example a backup ends successfully with: `INFO: backup command end: completed successfully`. (*Suggested by Jens Wilke.*)

**Improvements:**

- For simplicity, the `pg_control` file is now copied with the rest of the files instead of by itself of at the end of the process. The `backup` command does not require this behavior and the `restore` copies to a temporary file which is renamed at the end of the restore.

**Documentation Bug Fixes:**

- Fixed an issue that suppressed exceptions in PDF builds.
- Fixed regression in section links introduced in v1.10.

**Documentation Features:**

- Added Retention to QuickStart section.


### v1.11 Release Notes

*Bug Fix for Asynchronous Archiving Efficiency*

*Released November 17, 2016*

**Bug Fixes:**

- Fixed an issue where asynchronous archiving was transferring one file per execution instead of transferring files in batches. This regression was introduced in v1.09 and affected efficiency only, all WAL segments were correctly archived in asynchronous mode. (*Reported by Stephen Frost.*)


### v1.10 Release Notes

*Stanza Creation and Minor Bug Fixes*

*Released November 8, 2016*

**Bug Fixes:**

- Fixed an issue where a backup could error if no changes were made to a database between backups and only `pg_control` changed.
- Fixed an issue where tablespace paths with the same prefix would cause an invalid link error. (*Reported by Nikhilchandra Kulkarni.*)

**Features:**

- Added the `stanza-create` command to formalize creation of stanzas in the repository. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Improvements:**

- Removed extraneous `use lib` directives from Perl modules. (*Suggested by Devrim Gündüz.*)


### v1.09 Release Notes

*9.6 Support, Configurability, and Bug Fixes*

*Released October 10, 2016*

**Bug Fixes:**

- Fixed the `check` command to prevent an error message from being logged if the backup directory does not exist. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Fixed error message to properly display the archive command when an invalid archive command is detected. (*Reported by Jason O'Donnell.*)
- Fixed an issue where the async archiver would not be started if `archive-push` did not have enough space to queue a new WAL segment. This meant that the queue would never be cleared without manual intervention (such as calling `archive-push` directly). PostgreSQL now receives errors when there is not enough space to store new WAL segments but the async process will still be started so that space is eventually freed. (*Reported by Jens Wilke.*)
- Fixed a remote timeout that occurred when a local process generated checksums (during resume or restore) but did not copy files, allowing the remote to go idle. (*Reported by Jens Wilke.*)

**Features:**

- Non-exclusive backups will automatically be used on PostgreSQL 9.6.
- Added the `cmd-ssh` option to allow the ssh client to be specified. (*Suggested by Jens Wilke.*)
- Added the `log-level-stderr` option to control whether console log messages are sent to `stderr` or `stdout`. By default this is set to `warn` which represents a change in behavior from previous versions, even though it may be more intuitive. Setting `log-level-stderr=off` will preserve the old behavior. (*Suggested by Sascha Biberhofer.*)
- Set `application_name` to `"pgBackRest [command]"` for database connections. (*Suggested by Jens Wilke.*)
- Check that archive_mode is enabled when `archive-check` option enabled.

**Improvements:**

- Clarified error message when unable to acquire pgBackRest advisory lock to make it clear that it is not a PostgreSQL backup lock. (*Suggested by Jens Wilke.*)
- pgBackRest version number included in command start INFO log output.
- Process ID logged for local process start/stop INFO log output.

**Documentation Features:**

- Added `archive-timeout` option documentation to the user guide. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v1.08 Release Notes

*Bug Fixes and Log Improvements*

*Released September 14, 2016*

**Bug Fixes:**

- Fixed an issue where local processes were not disconnecting when complete and could later timeout. (*Reported by Todd Vernick.*)
- Fixed an issue where the protocol layer could timeout while waiting for WAL segments to arrive in the archive. (*Reported by Todd Vernick.*)

**Improvements:**

- Cache file log output until the file is created to create a more complete log.


### v1.07 Release Notes

*Thread to Process Conversion and Bug Fixes*

*Released September 7, 2016*

**Bug Fixes:**

- Fixed an issue where tablespaces were copied from the primary during standby backup.
- Fixed the `check` command so backup info is checked remotely and not just locally. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Fixed an issue where `retention-archive` was not automatically being set when `retention-archive-type=diff`, resulting in a less aggressive than intended expiration of archive. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)

**Features:**

- Converted Perl threads to processes to improve compatibility and performance.
- Exclude contents of `$PGDATA/pg_replslot` directory so that replication slots on the primary do not become part of the backup.
- The `archive-start` and `archive-stop` settings are now filled in `backup.manifest` even when `archive-check=n`. (*Suggested by Jens Wilke.*)
- Additional warnings when archive retention settings may not have the intended effect or would allow indefinite retention. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Experimental support for non-exclusive backups in PostgreSQL 9.6 rc1. Changes to the control/catalog/WAL versions in subsequent release candidates may break compatibility but pgBackRest will be updated with each release to keep pace.

**Documentation Bug Fixes:**

- Fixed minor documentation reproducibility issues related to binary paths.

**Documentation Features:**

- Documentation for archive retention. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v1.06 Release Notes

*Backup from Standby and Bug Fixes*

*Released August 25, 2016*

**Bug Fixes:**

- Fixed an issue where a tablespace link that referenced another link would not produce an error, but instead skip the tablespace entirely. (*Reported by Michael Vitale.*)
- Fixed an issue where options that should not allow multiple values could be specified multiple times in `pgbackrest.conf` without an error being raised. (*Reported by Michael Vitale.*)
- Fixed an issue where the `protocol-timeout` option was not automatically increased when the `db-timeout` option was increased. (*Reported by Todd Vernick.*)

**Features:**

- Backup from a standby cluster. A connection to the primary cluster is still required to start/stop the backup and copy files that are not replicated, but the vast majority of files are copied from the standby in order to reduce load on the primary.
- More flexible configuration for databases. Master and standby can both be configured on the backup server and pgBackRest will automatically determine which is the primary. This means no configuration changes for backup are required after failing over from a primary to standby when a separate backup server is used.
- Exclude directories during backup that are cleaned, recreated, or zeroed by PostgreSQL at startup. These include `pgsql_tmp` and `pg_stat_tmp`. The `postgresql.auto.conf.tmp` file is now excluded in addition to files that were already excluded: `backup_label.old`, `postmaster.opts`, `postmaster.pid`, `recovery.conf`, `recovery.done`.
- Experimental support for non-exclusive backups in PostgreSQL 9.6 beta4. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace.

**Improvements:**

- Improve error message for links that reference links in manifest build.
- Added hints to error message when relative paths are detected in `archive-push` or `archive-get`.
- Improve backup log messages to indicate which host the files are being copied from.


### v1.05 Release Notes

*Bug Fix for Tablespace Link Checking*

*Released August 9, 2016*

**Bug Fixes:**

- Fixed an issue where tablespace paths that had $PGDATA as a substring would be identified as a subdirectories of $PGDATA even when they were not. Also hardened relative path checking a bit. (*Reported by Chris Fort.*)

**Documentation Features:**

- Added documentation for scheduling backups with cron. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)

**Documentation Improvements:**

- Moved the backlog from the pgBackRest website to the GitHub repository wiki. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v1.04 Release Notes

*Various Bug Fixes*

*Released July 30, 2016*

**Bug Fixes:**

- Fixed an issue an where an extraneous remote was created causing threaded backup/restore to possibly timeout and/or throw a lock conflict. (*Reported by Michael Vitale.*)
- Fixed an issue where db-path was not required for the `check` command so an assert was raised when it was missing rather than a polite error message. (*Reported by Michael Vitale.*)
- Fixed `check` command to throw an error when database version/id does not match that of the archive. (*Fixed by Cynthia Shang. Reviewed by David Steele.*)
- Fixed an issue where a remote could try to start its own remote when the `backup-host` option was not present in `pgbackrest.conf` on the database server. (*Reported by Lardière Sébastien.*)
- Fixed an issue where the contents of `pg_xlog` were being backed up if the directory was symlinked. This didn't cause any issues during restore but was a waste of space.
- Fixed an invalid `log()` call in lock routines.

**Features:**

- Experimental support for non-exclusive backups in PostgreSQL 9.6 beta3. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace.

**Improvements:**

- Suppress banners on SSH protocol connections.
- Improved remote error messages to identify the host where the error was raised.
- All remote types now take locks. The exceptions date to when the test harness and pgBackRest were running in the same VM and no longer apply.

**Documentation Features:**

- Added clarification on why the default for the `backrest-user` option is `backrest`. (*Suggested by Michael Vitale.*)
- Updated information about package availability on supported platforms. (*Suggested by Michael Vitale.*)


### v1.03 Release Notes

*Check Command and Bug Fixes*

*Released July 2, 2016*

**Bug Fixes:**

- Fixed an issue where `keep-alives` could be starved out by lots of small files during multi-threaded `backup`. They were also completely absent from single/multi-threaded `backup` resume and `restore` checksumming. (*Reported by Janice Parkinson, Chris Barber.*)
- Fixed an issue where the `expire` command would refuse to run when explicitly called from the command line if the `db-host` option was set. This was not an issue when `expire` was run automatically after a `backup` (*Reported by Chris Barber.*)
- Fixed an issue where validation was being running on archive_command even when the `archive-check` option was disabled.

**Features:**

- Added `check` command to validate that pgBackRest is configured correctly for archiving and backups. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Added the `protocol-timeout` option. Previously `protocol-timeout` was set as `db-timeout` + 30 seconds.
- Failure to shutdown remotes at the end of the backup no longer throws an exception. Instead a warning is generated that recommends a higher `protocol-timeout`.
- Experimental support for non-exclusive backups in PostgreSQL 9.6 beta2. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace.

**Improvements:**

- Improved handling of users/groups captured during backup that do not exist on the restore host. Also explicitly handle the case where user/group is not mapped to a name.
- Option handling is now far more strict. Previously it was possible for a command to use an option that was not explicitly assigned to it. This was especially true for the `backup-host` and `db-host` options which are used to determine locality.

**Documentation Improvements:**

- Allow a static date to be used for documentation to generate reproducible builds. (*Suggested by Adrian Vondendriesch.*)
- Added documentation for asynchronous archiving to the user guide. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Recommended install location for pgBackRest modules is now `/usr/share/perl5` since `/usr/lib/perl5` has been removed from the search path in newer versions of Perl.
- Added instructions for removing prior versions of pgBackRest.


### v1.02 Release Notes

*Bug Fix for Perl 5.22*

*Released June 2, 2016*

**Bug Fixes:**

- Fix usage of sprintf() due to new constraints in Perl 5.22. Parameters not referenced in the format string are no longer allowed. (*Fixed by Adrian Vondendriesch. Reviewed by David Steele.*)

**Documentation Bug Fixes:**

- Fixed syntax that was not compatible with Perl 5.2X. (*Fixed by Christoph Berg, Adrian Vondendriesch. Reviewed by David Steele.*)
- Fixed absolute paths that were used for the PDF logo. (*Reported by Adrian Vondendriesch.*)

**Documentation Features:**

- Release notes are now broken into sections so that bugs, features, and refactors are clearly delineated. An "Additional Notes" section has been added for changes to documentation and the test suite that do not affect the core code.
- Added man page generation. (*Contributed by Adrian Vondendriesch, David Steele.*)
- The change log was the last piece of documentation to be rendered in Markdown only. Wrote a converter so the document can be output by the standard renderers. The change log will now be located on the website and has been renamed to "Releases". (*Contributed by Cynthia Shang. Reviewed by David Steele.*)


### v1.01 Release Notes

*Enhanced Info, Selective Restore, and 9.6 Support*

*Released May 17, 2016*

**Features:**

- Enhanced text output of `info` command to include timestamps, sizes, and the reference list for all backups. (*Contributed by Cynthia Shang. Reviewed by David Steele.*)
- Allow selective restore of databases from a cluster backup. This feature can result in major space and time savings when only specific databases are restored. Unrestored databases will not be accessible but must be manually dropped before they will be removed from the shared catalogue. (*Reviewed by Cynthia Shang, Greg Smith, Stephen Frost. Suggested by Stephen Frost.*)
- Experimental support for non-exclusive backups in PostgreSQL 9.6 beta1. Changes to the control/catalog/WAL versions in subsequent betas may break compatibility but pgBackRest will be updated with each release to keep pace. (*Reviewed by Cynthia Shang.*)


### v1.00 Release Notes

*New Repository Format and Configuration Scheme, Link Support*

*Released April 14, 2016*

**IMPORTANT NOTE**: This flag day release breaks compatibility with older versions of pgBackRest. The manifest format, on-disk structure, configuration scheme, and the exe/path names have all changed. You must create a new repository to hold backups for this version of pgBackRest and keep your older repository for a time in case you need to do a restore. Restores from the prior repository will require the prior version of pgBackRest but because of name changes it is possible to have `1.00` and a prior version of pgBackRest installed at the same time. See the notes below for more detailed information on what has changed.

**Features:**

- Implemented a new configuration scheme which should be far simpler to use. See the User Guide and Configuration Reference for details but for a simple configuration all options can now be placed in the `stanza` section. Options that are shared between stanzas can be placed in the `[global]` section. More complex configurations can still make use of command sections though this should be a rare use case. (*Suggested by Michael Renner.*)
- The `repo-path` option now always refers to the repository where backups and archive are stored, whether local or remote, so the `repo-remote-path` option has been removed. The new `spool-path` option can be used to define a location for queueing WAL segments when archiving asynchronously. A local repository is no longer required.
- The default configuration filename is now `pgbackrest.conf` instead of `pg_backrest.conf`. This was done for consistency with other naming changes but also to prevent old config files from being loaded accidentally when migrating to `1.00`. (*Suggested by Michael Renner, Stephen Frost.*)
- The default repository name was changed from `/var/lib/backup` to `/var/lib/pgbackrest`. (*Suggested by Michael Renner, Stephen Frost.*)
- Lock files are now stored in `/tmp/pgbackrest` by default. These days `/run/pgbackrest` is the preferred location but that would require init scripts which are not part of this release. The `lock-path` option can be used to configure the lock directory.
- Log files are now stored in `/var/log/pgbackrest` by default and no longer have the date appended so they can be managed with `logrotate`. The `log-path` option can be used to configure the log directory. (*Suggested by Stephen Frost.*)
- Executable filename changed from `pg_backrest` to `pgbackrest`. (*Suggested by Michael Renner, Stephen Frost.*)
- All files and directories linked from PGDATA are now included in the backup. By default links will be restored directly into PGDATA as files or directories. The `--link-all` option can be used to restore all links to their original locations. The `--link-map` option can be used to remap a link to a new location.
- Removed `--tablespace` option and replaced with `--tablespace-map-all` option which should more clearly indicate its function.
- Added `detail` log level which will output more information than `info` without being as verbose as `debug`.


--------

## Pre-Stable Releases


### v0.92 Release Notes

*Command-line Repository Path Fix*

*Released April 6, 2016*

**Bug Fixes:**

- Fixed an issue where the master process was passing `--repo-remote-path` instead of `--repo-path` to the remote and causing the lock files to be created in the default repository directory (`/var/lib/backup`), generally ending in failure. This was only an issue when `--repo-remote-path` was defined on the command line rather than in `pg_backrest.conf`. (*Reported by Jan Wieck.*)


### v0.91 Release Notes

*Tablespace Bug Fix and Minor Enhancements*

*Released March 22, 2016*

**IMPORTANT BUG FIX FOR TABLESPACES**: A change to the repository format was accidentally introduced in 0.90 which means the on-disk backup was no longer a valid PostgreSQL cluster when the backup contained tablespaces. This only affected users who directly copied the backups to restore PostgreSQL clusters rather than using the restore command. However, the fix breaks compatibility with older backups that contain tablespaces no matter how they are being restored (pgBackRest will throw errors and refuse to restore). New full backups should be taken immediately after installing version 0.91 for any clusters that contain tablespaces. If older backups need to be restored then use a version of pgBackRest that matches the backup version.

**Bug Fixes:**

- Fixed repository incompatibility introduced in pgBackRest 0.90. (*Reported by Evan Benoit.*)

**Features:**

- Copy `global/pg_control` last during backups.
- Write `.info` and `.manifest` files to temp before moving them to their final locations and fsync'ing.
- Rename `--no-start-stop` option to `--no-online`.

**Test Suite Features:**

- Static source analysis using Perl-Critic, currently passes on gentle.


### v0.90 Release Notes

*9.5 Support, Various Enhancements, and Minor Bug Fixes*

*Released February 7, 2016*

**Bug Fixes:**

- Fixed an issue where specifying `--no-archive-check` would throw a configuration error. (*Reported by Jason O'Donnell.*)
- Fixed an issue where a temp WAL file left over after a well-timed system crash could cause the next `archive-push` to fail.
- The `retention-archive` option can now be safely set to less than backup retention (`retention-full` or `retention-diff`) without also specifying `archive-copy=n`. The WAL required to make the backups that fall outside of archive retention consistent will be preserved in the archive. However, in this case PITR will not be possible for the backups that fall outside of archive retention.

**Features:**

- When backing up and restoring tablespaces pgBackRest only operates on the subdirectory created for the version of PostgreSQL being run against. Since multiple versions can live in a tablespace (especially during a binary upgrade) this prevents too many files from being copied during a backup and other versions possibly being wiped out during a restore. This only applies to PostgreSQL >= 9.0 — prior versions of PostgreSQL could not share a tablespace directory.
- Generate an error when `archive-check=y` but `archive_command` does not execute `pg_backrest`. (*Contributed by Jason O'Donnell. Reviewed by David Steele.*)
- Improved error message when `repo-path` or `repo-remote-path` does not exist.
- Added checks for `--delta` and `--force` restore options to ensure that the destination is a valid $PGDATA directory. pgBackRest will check for the presence of `PG_VERSION` or `backup.manifest` (left over from an aborted restore). If neither file is found then `--delta` and `--force` will be disabled but the restore will proceed unless there are files in the $PGDATA directory (or any tablespace directories) in which case the operation will be aborted.
- When restore `--set=latest` (the default) the actual backup restored will be output to the log.
- Support for PostgreSQL 9.5 partial WAL segments and `recovery_target_action` setting. The `archive_mode = 'always'` setting is not yet supported.
- Support for `recovery_target = 'immediate'` recovery setting introduced in PostgreSQL 9.4.
- The following tablespace checks have been added: paths or files in pg_tblspc, relative links in pg_tblspc, tablespaces in $PGDATA. All three will generate errors.


### v0.89 Release Notes

*Timeout Bug Fix and Restore Read-Only Repositories*

*Released December 24, 2015*

**Bug Fixes:**

- Fixed an issue where longer-running backups/restores would timeout when remote and threaded. Keepalives are now used to make sure the remote for the main process does not timeout while the thread remotes do all the work. The error message for timeouts was also improved to make debugging easier. (*Reported by Stephen Frost.*)

**Features:**

- Allow restores to be performed on a read-only repository by using `--no-lock` and `--log-level-file=off`. The `--no-lock` option can only be used with restores.


### v0.88 Release Notes

*Documentation and Minor Bug Fixes*

*Released November 22, 2015*

**Bug Fixes:**

- Fixed an issue where the `start`/`stop` commands required the `--config` option. (*Reported by Dmitry Didovicher.*)
- Fixed an issue where log files were being overwritten instead of appended. (*Reported by Stephen Frost, Dmitry Didovicher.*)
- Fixed an issue where `backup-user` was not optional.

**Features:**

- Symlinks are no longer created in backup directories in the repository. These symlinks could point virtually anywhere and potentially be dangerous. Symlinks are still recreated during a restore. (*Suggested by Stephen Frost.*)
- Added better messaging for backup expiration. Full and differential backup expirations are logged on a single line along with a list of all dependent backups expired.
- Archive retention is automatically set to full backup retention if not explicitly configured.

**Documentation Features:**

- Added documentation in the user guide for delta restores, expiration, dedicated backup hosts, starting and stopping pgBackRest, and replication.


### v0.87 Release Notes

*Website and User Guide*

*Released October 28, 2015*

**Features:**

- The `backup_label.old` and `recovery.done` files are now excluded from backups.

**Documentation Features:**

- Added a new user guide that covers pgBackRest basics and some advanced topics including PITR. Much more to come, but it's a start. (*Contributed by David Steele, Stephen Frost. Reviewed by Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher.*)


### v0.85 Release Notes

*Start/Stop Commands and Minor Bug Fixes*

*Released October 8, 2015*

**Bug Fixes:**

- Fixed an issue where an error could be returned after a backup or restore completely successfully.
- Fixed an issue where a resume would fail if temp files were left in the root backup directory when the backup failed. This scenario was likely if the backup process got terminated during the copy phase.

**Features:**

- Added `stop` and `start` commands to prevent pgBackRest processes from running on a system where PostgreSQL is shutdown or the system needs to be quiesced for some other reason.
- Experimental support for PostgreSQL 9.5 beta1. This may break when the control version or WAL magic changes in future versions but will be updated in each pgBackRest release to keep pace. All regression tests pass except for `--target-resume` tests (this functionality has changed in 9.5) and there is no testing yet for `.partial` WAL segments.


### v0.82 Release Notes

*Refactoring, Command-line Help, and Minor Bug Fixes*

*Released September 14, 2015*

**Bug Fixes:**

- Fixed an issue where resumed compressed backups were not preserving existing files.
- Fixed an issue where resume and incr/diff would not ensure that the prior backup had the same compression and hardlink settings.
- Fixed an issue where a cold backup using `--no-start-stop` could be started on a running PostgreSQL cluster without `--force` specified.
- Fixed an issue where a thread could be started even when none were requested.
- Fixed an issue where the pgBackRest version number was not being updated in `backup.info` and `archive.info` after an upgrade/downgrade.
- Fixed an issue where the `info` command was throwing an exception when the repository contained no stanzas. (*Reported by Stephen Frost.*)
- Fixed an issue where the PostgreSQL `pg_stop_backup()` NOTICEs were being output to `stderr`. (*Reported by Stephen Frost.*)

**Features:**

- Experimental support for PostgreSQL 9.5 alpha2. This may break when the control version or WAL magic changes in future versions but will be updated in each pgBackRest release to keep pace. All regression tests pass except for `--target-resume` tests (this functionality has changed in 9.5) and there is no testing yet for `.partial` WAL segments.

**Improvements:**

- Renamed `recovery-setting` option and section to `recovery-option` to be more consistent with pgBackRest naming conventions.
- Added dynamic module loading to speed up commands, especially asynchronous archiving.

**Documentation Features:**

- Command-line help is now extracted from the same XML source that is used for the other documentation and includes much more detail.


### v0.80 Release Notes

*DBI Support, Stability, and Convenience Features*

*Released August 9, 2015*

**Bug Fixes:**

- Fixed an issue that caused the formatted timestamp for both the oldest and newest backups to be reported as the current time by the `info` command. Only `text` output was affected -- `json` output reported the correct epoch values. (*Reported by Michael Renner.*)
- Fixed protocol issue that was preventing ssh errors (especially on connection) from being logged.

**Features:**

- The repository is now created and updated with consistent directory and file modes. By default `umask` is set to `0000` but this can be disabled with the `neutral-umask` setting. (*Suggested by Cynthia Shang.*)
- Added the `stop-auto` option to allow failed backups to automatically be stopped when a new backup starts.
- Added the `db-timeout` option to limit the amount of time pgBackRest will wait for `pg_start_backup()` and `pg_stop_backup()` to return.
- Remove `pg_control` file at the beginning of the restore and copy it back at the very end. This prevents the possibility that a partial restore can be started by PostgreSQL.
- Added checks to be sure the `db-path` setting is consistent with `db-port` by comparing the `data_directory` as reported by the cluster against the `db-path` setting and the version as reported by the cluster against the value read from `pg_control`. The `db-socket-path` setting is checked to be sure it is an absolute path.
- Experimental support for PostgreSQL 9.5 alpha1. This may break when the control version or WAL magic changes in future versions but will be updated in each pgBackRest release to keep pace. All regression tests pass except for `--target-resume` tests (this functionality has changed in 9.5) and there is no testing yet for `.partial` WAL segments.

**Improvements:**

- Now using Perl `DBI` and `DBD::Pg` for connections to PostgreSQL rather than `psql`. The `cmd-psql` and `cmd-psql-option` settings have been removed and replaced with `db-port` and `db-socket-path`. Follow the instructions in the Installation Guide to install `DBD::Pg` on your operating system.

**Test Suite Features:**

- Added vagrant test configurations for Ubuntu 14.04 and CentOS 7.


### v0.78 Release Notes

*Remove CPAN Dependencies, Stability Improvements*

*Released July 13, 2015*

**Improvements:**

- Removed dependency on CPAN packages for multi-threaded operation. While it might not be a bad idea to update the `threads` and `Thread::Queue` packages, it is no longer necessary.
- Modified wait backoff to use a Fibonacci rather than geometric sequence. This will make wait time grow less aggressively while still giving reasonable values.

**Test Suite Features:**

- Added vagrant test configurations for Ubuntu 12.04 and CentOS 6.


### v0.77 Release Notes

*CentOS/RHEL 6 Support and Protocol Improvements*

*Released June 30, 2015*

**Features:**

- Added file and directory syncs to the `File` object for additional safety during backup/restore and archiving. (*Suggested by Andres Freund.*)
- Added support for Perl 5.10.1 and OpenSSH 5.3 which are default for CentOS/RHEL 6. (*Suggested by Eric Radman.*)
- Improved error message when backup is run without `archive_command` set and without `--no-archive-check` specified. (*Suggested by Eric Radman.*)


### v0.75 Release Notes

*New Repository Format, Info Command and Experimental 9.5 Support*

*Released June 14, 2015*

**IMPORTANT NOTE**: This flag day release breaks compatibility with older versions of pgBackRest. The manifest format, on-disk structure, and the binary names have all changed. You must create a new repository to hold backups for this version of pgBackRest and keep your older repository for a time in case you need to do a restore. The `pg_backrest.conf` file has not changed but you'll need to change any references to `pg_backrest.pl` in cron (or elsewhere) to `pg_backrest` (without the `.pl` extension).

**Features:**

- Added the `info` command.
- Logging now uses unbuffered output. This should make log files that are being written by multiple threads less chaotic. (*Suggested by Michael Renner.*)
- Experimental support for PostgreSQL 9.5. This may break when the control version or WAL magic changes but will be updated in each release.

**Improvements:**

- More efficient file ordering for `backup`. Files are copied in descending size order so a single thread does not end up copying a large file at the end. This had already been implemented for `restore`.


### v0.70 Release Notes

*Stability Improvements for Archiving, Improved Logging and Help*

*Released June 1, 2015*

**Bug Fixes:**

- Fixed an issue where `archive-copy` would fail on an incr/diff backup when `hardlink=n`. In this case the `pg_xlog` path does not already exist and must be created. (*Reported by Michael Renner.*)
- Fixed an issue in async archiving where `archive-push` was not properly returning 0 when `archive-max-mb` was reached and moved the async check after transfer to avoid having to remove the stop file twice. Also added unit tests for this case and improved error messages to make it clearer to the user what went wrong. (*Reported by Michael Renner.*)
- Fixed a locking issue that could allow multiple operations of the same type against a single stanza. This appeared to be benign in terms of data integrity but caused spurious errors while archiving and could lead to errors in backup/restore. (*Reported by Michael Renner.*)

**Features:**

- Allow duplicate WAL segments to be archived when the checksum matches. This is necessary for some recovery scenarios.
- Allow comments/disabling in `pg_backrest.conf` using the `#` character. Only `#` characters in the first character of the line are honored. (*Suggested by Michael Renner.*)
- Better logging before `pg_start_backup()` to make it clear when the backup is waiting on a checkpoint. (*Suggested by Michael Renner.*)
- Various command behavior and logging fixes. (*Reviewed by Michael Renner. Suggested by Michael Renner.*)

**Improvements:**

- Replaced `JSON` module with `JSON::PP` which ships with core Perl.

**Documentation Bug Fixes:**

- Various help fixes. (*Reviewed by Michael Renner. Reported by Michael Renner.*)


### v0.65 Release Notes

*Improved Resume and Restore Logging, Compact Restores*

*Released May 11, 2015*

**Bug Fixes:**

- Fixed an issue where an absolute path was not written into `recovery.conf` when the restore was run with a relative path.

**Features:**

- Better resume support. Resumed files are checked to be sure they have not been modified and the manifest is saved more often to preserve checksums as the backup progresses. More unit tests to verify each resume case.
- Resume is now optional. Use the `resume` setting or `--no-resume` from the command line to disable.
- More info messages during restore. Previously, most of the restore messages were debug level so not a lot was output in the log.
- Added `tablespace` setting to allow tablespaces to be restored into the `pg_tblspc` path. This produces compact restores that are convenient for development, staging, etc. Currently these restores cannot be backed up as pgBackRest expects only links in the `pg_tblspc` path.


### v0.61 Release Notes

*Bug Fix for Uncompressed Remote Destination*

*Released April 21, 2015*

**Bug Fixes:**

- Fixed a buffering error that could occur on large, highly-compressible files when copying to an uncompressed remote destination. The error was detected in the decompression code and resulted in a failed backup rather than corruption so it should not affect successful backups made with previous versions.


### v0.60 Release Notes

*Better Version Support and WAL Improvements*

*Released April 19, 2015*

**Bug Fixes:**

- Pushing duplicate WAL now generates an error. This worked before only if checksums were disabled.

**Features:**

- Database System IDs are used to make sure that all WAL in an archive matches up. This should help prevent misconfigurations that send WAL from multiple clusters to the same archive.

**Test Suite Features:**

- Regression tests working back to PostgreSQL 8.3.


### v0.50 Release Notes

*Restore and Much More*

*Released March 25, 2015*

**Bug Fixes:**

- Fixed broken checksums and now they work with normal and resumed backups. Finally realized that checksums and checksum deltas should be functionally separated and this simplified a number of things. Issue #28 has been created for checksum deltas.
- Fixed an issue where a backup could be resumed from an aborted backup that didn't have the same type and prior backup.

**Features:**

- Added restore functionality.
- All options can now be set on the command-line making `pg_backrest.conf` optional.
- De/compression is now performed without threads and checksum/size is calculated in stream. That means file checksums are no longer optional.
- Added option `--no-start-stop` to allow backups when Postgres is shut down. If `postmaster.pid` is present then `--force` is required to make the backup run (though if Postgres is running an inconsistent backup will likely be created). This option was added primarily for the purpose of unit testing, but there may be applications in the real world as well.
- Checksum for `backup.manifest` to detect a corrupted/modified manifest.
- Link `latest` always points to the last backup. This has been added for convenience and to make restores simpler.

**Test Suite Features:**

- More comprehensive unit tests in all areas.


### v0.30 Release Notes

*Core Restructuring and Unit Tests*

*Released October 5, 2014*

**Documentation Features:**

- Added much needed documentation

**Test Suite Features:**

- Fairly comprehensive unit tests for all the basic operations. More work to be done here for sure, but then there is always more work to be done on unit tests.


### v0.19 Release Notes

*Improved Error Reporting/Handling*

*Released May 13, 2014*

**Bug Fixes:**

- Found and squashed a nasty bug where `file_copy()` was defaulted to ignore errors. There was also an issue in `file_exists()` that was causing the test to fail when the file actually did exist. Together they could have resulted in a corrupt backup with no errors, though it is very unlikely.


### v0.18 Release Notes

*Return Soft Error When Archive Missing*

*Released April 13, 2014*

**Bug Fixes:**

- The `archive-get` command now returns a 1 when the archive file is missing to differentiate from hard errors (ssh connection failure, file copy error, etc.) This lets PostgreSQL know that the archive stream has terminated normally. However, this does not take into account possible holes in the archive stream. (*Reported by Stephen Frost.*)


### v0.17 Release Notes

*Warn When Archive Directories Cannot Be Deleted*

*Released April 3, 2014*

**Bug Fixes:**

- If an archive directory which should be empty could not be deleted backrest was throwing an error. There's a good fix for that coming, but for the time being it has been changed to a warning so processing can continue. This was impacting backups as sometimes the final archive file would not get pushed if the first archive file had been in a different directory (plus some bad luck).


### v0.16 Release Notes

*RequestTTY=yes for SSH Sessions*

*Released April 1, 2014*

**Bug Fixes:**

- Added `RequestTTY=yes` to ssh sessions. Hoping this will prevent random lockups.


### v0.15 Release Notes

*Added archive-get*

*Released March 29, 2014*

**Features:**

- Added `archive-get` functionality to aid in restores.
- Added option to force a checkpoint when starting the backup, `start-fast=y`.


### v0.11 Release Notes

*Minor Fixes*

*Released March 26, 2014*

**Bug Fixes:**

- Removed `master_stderr_discard` option on database SSH connections. There have been occasional lockups and they could be related to issues originally seen in the file code. (*Reported by Stephen Frost.*)
- Changed lock file conflicts on `backup` and `expire` commands to `ERROR`. They were set to `DEBUG` due to a copy-and-paste from the archive locks.


### v0.10 Release Notes

*Backup and Archiving are Functional*

*Released March 5, 2014*

**Features:**

- No restore functionality, but the backup directories are consistent PostgreSQL data directories. You'll need to either uncompress the files or turn off compression in the backup. Uncompressed backups on a ZFS (or similar) filesystem are a good option because backups can be restored locally via a snapshot to create logical backups or do spot data recovery.
- Archiving is single-threaded. This has not posed an issue on our multi-terabyte databases with heavy write volume. Recommend a large WAL volume or to use the async option with a large volume nearby.
- Backups are multi-threaded, but the `Net::OpenSSH` library does not appear to be 100% thread-safe so it will very occasionally lock up on a thread. There is an overall process timeout that resolves this issue by killing the process. Yes, very ugly.
- Checksums are lost on any resumed backup. Only the final backup will record checksum on multiple resumes. Checksums from previous backups are correctly recorded and a full backup will reset everything.
- The `backup.manifest` is being written as `Storable` because `Config::IniFile` does not seem to handle large files well. Would definitely like to save these as human-readable text.

**Documentation Features:**

- Absolutely no documentation (outside the code). Well, excepting these release notes.
