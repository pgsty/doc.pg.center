---
title: KMIP configuration
linkTitle: KMIP setup
description: Configure a KMIP endpoint, client credentials, and key provider.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/kmip-server.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 350
upstream_source: percona
---

> [!NOTE] Editorial correction
> This overview retains an older qualification of Vault KMIP. The 2.2.2 release notes explicitly announce Vault Enterprise KMIP support; consult those notes for the version-specific status. See [site errata](/percona/site/errata/).

To use a Key Management Interoperability Protocol (KMIP) server with `pg_tde`, you must configure it as a global key provider. This setup enables `pg_tde` to securely fetch and manage encryption keys from a centralized key management appliance.

> [!IMPORTANT]
> When using HashiCorp Vault as a KMIP server, this configuration is not a validated deployment model for `pg_tde` and is not recommended for production use.
>
> For Vault-based key management, use the [KV v2 integration](/percona/global-key-provider-configuration/vault/) instead.

> [!NOTE]
> You need the root certificate of the KMIP server and a client key/certificate pair with permissions to create and read keys on the server.

For testing purposes, you can use a Eviden KMS server, which enables easy certificate generation and basic KMIP behavior. If you're using a production-grade KMIP server, ensure you obtain valid, trusted certificates from the key management appliance.

## Example usage {#example-usage}

```sql
SELECT pg_tde_add_global_key_provider_kmip(
    'provider-name',
    'kmip-IP', 
    `port`,
    '/path_to/server_certificate.pem', 
    '/path_to/client_cert.pem',
    '/path_to/client_key.pem'
);
```

## Parameter descriptions {#parameter-descriptions}

* `provider-name` is the name of the provider. You can specify any name, it's for you to identify the provider
* `kmip-IP` is the IP address of a domain name of the KMIP server
* `port` is the port to communicate with the KMIP server. Typically used port is 5696
* `server-certificate` is the path to the certificate file for the KMIP server
* `client_cert` is the path to the client certificate.
* `client_key` is the path to the client key.

The following example is for testing purposes only.

```sql
SELECT pg_tde_add_global_key_provider_kmip(
    'kmip','127.0.0.1', 
    5696, 
    '/tmp/server_certificate.pem', 
    '/tmp/client_cert_jane_doe.pem',
    '/tmp/client_key_jane_doe.pem'
);
```

For more information on related functions, see the link below:

[Percona pg_tde Function Reference](/percona/functions/)

## Next steps {#next-steps}

[Global Principal Key Configuration ](/percona/global-key-provider-configuration/set-principal-key/)
