---
title: pg_tde_change_key_provider
linkTitle: Change key provider
description: Change provider configuration in an offline data directory.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-change-key-provider.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 740
upstream_source: percona
---

A tool for modifying the configuration of a key provider, possibly also changing its type.

This tool edits the configuration files directly, ignoring permissions or running `postgres` processes.

Its only intended use is to fix servers that can't start up because of inaccessible key providers.

For example, you restore from an old backup and the address of the key provider changed in the meantime. You can use this tool to correct the configuration, allowing the server to start up.

**Warning:** Use this tool **only when the server is offline.** To modify the key provider configuration when the server is up and running, use the [`pg_tde_change_(global/database)_key_provider_<type>`](/percona/functions/#change-an-existing-provider) SQL functions.

## Example usage {#example-usage}

To modify the key provider configuration, specify all parameters depending on the provider type in the same way as you do when using the [`pg_tde_change_(global/database)_key_provider_<type>`](/percona/functions/#change-an-existing-provider) SQL functions.

The general syntax is as follows:

```sh
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> <new_provider_type> <provider_parameters...>
```

## Parameter description {#parameter-description}

* [optional] `<datadir>` is the data directory.`pg_tde` uses the `$PGDATA` environment variable if this is not specified
* `<provider_name>` is the name you assigned to the key provider
* `<new_provider_type>` can be a `file`, `vault` or `kmip`
* `<dbOid>`

Depending on the provider type, the additional parameters are:

```sh
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> file <filename>
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> vault-v2 <url> <mount_path> <token_path> [<ca_path>]
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> kmip <host> <port> <cert_path> <key_path> [<ca_path>] 
```
