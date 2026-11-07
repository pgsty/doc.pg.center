---
title: Using OpenBao as a key provider
linkTitle: OpenBao
description: Configure an OpenBao secrets engine, token, and pg_tde key provider.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/openbao.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 340
upstream_source: percona
---

You can configure `pg_tde` to use OpenBao as a global key provider for managing encryption keys securely.

> [!NOTE]
> This guide assumes that your OpenBao server is already set up and accessible. OpenBao configuration is outside the scope of this document, see [OpenBao's official documentation](https://openbao.org/docs/) for more information.

## Example usage {#example-usage}

To register an OpenBao server as a global key provider:

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'provider-name',
    'url',
    'mount',
    'secret_token_path',
    'ca_path',
    'namespace'
);
```

## Parameter descriptions {#parameter-descriptions}

* `provider-name` is the name to identify this key provider
* `secret_token_path` is a path to the file that contains an access token with read and write access to the above mount point
* `url` is the URL of the OpenBao server
* `mount` is the mount point where the keyring should store the keys
* [optional] `ca_path` is the path of the CA file used for SSL verification
* [optional] `namespace` is the namespace within the OpenBao server. Read more about the [namespace support in OpenBao](https://openbao.org/blog/namespaces-announcement/)` (NOTE: You can use a namespace without ca_path. In this case, specify NULL as the ca_path value)

The following example is for testing purposes only. Use secure tokens and proper SSL validation in production environments:

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'my-openbao-provider',
    'https://openbao.example.com:8200',
    'secret/data',
    '/path/to/token_file',
    '/path/to/ca_cert.pem'
);
```

For more information on related functions, see the link below:

[Percona pg_tde Function Reference](/percona/functions/)

## Next steps {#next-steps}

[Global Principal Key Configuration ](/percona/global-key-provider-configuration/set-principal-key/)
