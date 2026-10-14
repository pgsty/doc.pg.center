---
title: "Konfigurationsoptionen"
weight: 4050
description: "Konfigurationsdateien, Optionen und Umgebungsvariablen von etcd"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/configuration.md"
---

etcd lässt sich auf folgende Arten konfigurieren:

- **[Befehlszeilenoptionen](#command-line-flags)**
- **Umgebungsvariablen**: Zu jeder Option gehört eine gleichnamige Umgebungsvariable,
  deren Name jedoch mit `ETCD_` beginnt und in Großbuchstaben mit
  [Unterstrichen als Worttrennern][snake case] geschrieben wird. Beispielsweise entspricht `--some-flag` der Variablen `ETCD_SOME_FLAG`.
- **[Konfigurationsdatei](#configuration-file)**

> [!WARNING]
> **Achtung**: Werden verschiedene Konfigurationsarten kombiniert, gelten die folgenden
> Regeln.
>
> - Befehlszeilenoptionen haben Vorrang vor Umgebungsvariablen.
> - Wird eine _Konfigurationsdatei_ angegeben, werden alle Befehlszeilenoptionen und Umgebungsvariablen **ignoriert**.

## Befehlszeilenoptionen {#command-line-flags}

Die Optionen werden im Folgenden im Format `--flag-name DEFAULT_VALUE` dargestellt.

> [!NOTE]
> Diese importierte Referenz enthält einige ältere v2-Optionen als Kontext für die Migration. In etcd 3.7 sind `--enable-v2` und der v2-Proxy-Modus nicht verfügbar. Die veraltete Option `--v2-deprecation` ignoriert Benutzereingaben und erzwingt ihren Standardwert. Vor der Verwendung älterer Optionen die Ausgabe von `etcd --help` für die installierte Version prüfen.


Die folgende Optionsliste ist aufgrund laufender Entwicklungsänderungen möglicherweise nicht aktuell. Die neuesten verfügbaren Optionen lassen sich mit `etcd --help` oder in der [etcd-Hilfe][etcd help] nachschlagen.

> [!NOTE]
>   **Hinweis**: Einzelheiten zu neuen, aktualisierten und als veraltet markierten Optionen in v3.7
>   stehen in [CHANGELOG-3.7.md][changelog].
>   <!-- markdownlint-disable-next-line MD034 -->
>   [changelog]:  https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md

### Mitglied {#member}

```text
--name 'default'
  Human-readable name for this member.
--data-dir '${name}.etcd'
  Path to the data directory.
--wal-dir ''
  Path to the dedicated wal directory.
--snapshot-count '10000'
  Number of committed transactions to trigger a snapshot to disk.
--heartbeat-interval '100'
  Time (in milliseconds) of a heartbeat interval.
--election-timeout '1000'
  Time (in milliseconds) for an election to timeout. See tuning documentation for details.
--initial-election-tick-advance 'true'
  Whether to fast-forward initial election ticks on boot for faster election.
--listen-peer-urls 'http://localhost:2380'
  List of URLs to listen on for peer traffic.
--listen-client-urls 'http://localhost:2379'
  List of URLs to listen on for client grpc traffic and http as long as --listen-client-http-urls is not specified.
--listen-client-http-urls ''
  List of URLs to listen on for http only client traffic. Enabling this flag removes http services from --listen-client-urls.
--max-snapshots '5'
  Maximum number of snapshot files to retain (0 is unlimited).
--max-wals '5'
  Maximum number of wal files to retain (0 is unlimited).
--memory-mlock
  Enable to enforce etcd pages (in particular bbolt) to stay in RAM.
--quota-backend-bytes '0'
  Raise alarms when backend size exceeds the given quota (0 defaults to low space quota).
--backend-bbolt-freelist-type 'map'
  BackendFreelistType specifies the type of freelist that boltdb backend uses(array and map are supported types).
--backend-batch-interval ''
  BackendBatchInterval is the maximum time before commit the backend transaction.
--backend-batch-limit '0'
  BackendBatchLimit is the maximum operations before commit the backend transaction.
--max-txn-ops '128'
  Maximum number of operations permitted in a transaction.
--max-request-bytes '1572864'
  Maximum client request size in bytes the server will accept.
--grpc-keepalive-min-time '5s'
  Minimum duration interval that a client should wait before pinging server.
--grpc-keepalive-interval '2h'
  Frequency duration of server-to-client ping to check if a connection is alive (0 to disable).
--grpc-keepalive-timeout '20s'
  Additional duration of wait before closing a non-responsive connection (0 to disable).
--socket-reuse-port 'false'
  Enable to set socket option SO_REUSEPORT on listeners allowing rebinding of a port already in use.
--socket-reuse-address 'false'
  Enable to set socket option SO_REUSEADDR on listeners allowing binding to an address in TIME_WAIT state.
```

### Clusterbildung {#clustering}

```text
--initial-advertise-peer-urls 'http://localhost:2380'
  List of this member's peer URLs to advertise to the rest of the cluster.
--initial-cluster 'default=http://localhost:2380'
  Initial cluster configuration for bootstrapping.
--initial-cluster-state 'new'
  Initial cluster state ('new' or 'existing').
--initial-cluster-token 'etcd-cluster'
  Initial cluster token for the etcd cluster during bootstrap.
  Specifying this can protect you from unintended cross-cluster interaction when running multiple clusters.
--advertise-client-urls 'http://localhost:2379'
  List of this member's client URLs to advertise to the public.
  The client URLs advertised should be accessible to machines that talk to etcd cluster. etcd client libraries parse these URLs to connect to the cluster.
--discovery ''
  Discovery URL used to bootstrap the cluster.
--discovery-fallback 'proxy'
  Expected behavior ('exit' or 'proxy') when discovery services fails.
  "proxy" supports v2 API only.
--discovery-proxy ''
  HTTP proxy to use for traffic to discovery service.
--discovery-srv ''
  DNS srv domain used to bootstrap the cluster.
--discovery-srv-name ''
  Suffix to the dns srv name queried when bootstrapping.
--strict-reconfig-check 'true'
  Reject reconfiguration requests that would cause quorum loss.
--pre-vote 'true'
  Enable the raft Pre-Vote algorithm to prevent disruption when a node that has been partitioned away rejoins the cluster.
--auto-compaction-retention '0'
  Auto compaction retention length. 0 means disable auto compaction.
--auto-compaction-mode 'periodic'
  Interpret 'auto-compaction-retention' one of: periodic|revision. 'periodic' for duration based retention, defaulting to hours if no time unit is provided (e.g. '5m'). 'revision' for revision number based retention.
--enable-v2 'false'
  Accept etcd V2 client requests. Deprecated and to be decommissioned in v3.6.
--v2-deprecation 'not-yet'
  Phase of v2store deprecation. Allows to opt-in for higher compatibility mode.
  Supported values:
    'not-yet'                // Issues a warning if v2store have meaningful content (default in v3.5)
    'write-only'             // Custom v2 state is not allowed (default in v3.6 and v3.7)
    'write-only-skip-check'  // Custom v2 state is not supported and, if present, will be ignored (available in v3.5.32+, v3.6.13+, and v3.7.0+). Use this option at your own risk.
    'write-only-drop-data'   // Custom v2 state will get DELETED ! (planned default in v3.8)
    'gone'                   // v2store is not maintained any longer.
```

### Sicherheit {#security}

```text
--cert-file ''
  Path to the client server TLS cert file.
--key-file ''
  Path to the client server TLS key file.
--client-cert-auth 'false'
  Enable client cert authentication.
  It's recommended to enable client cert authentication to prevent attacks from unauthenticated clients (e.g. CVE-2023-44487), especially when running etcd as a public service.
--client-crl-file ''
  Path to the client certificate revocation list file.
--client-cert-allowed-hostname ''
  Comma-separated list of SAN hostnames for client cert authentication.
--trusted-ca-file ''
  Path to the client server TLS trusted CA cert file.
  Note setting this parameter will also automatically enable client cert authentication no matter what value is set for `--client-cert-auth`.
--auto-tls 'false'
  Client TLS using generated certificates.
--peer-cert-file ''
  Path to the peer server TLS cert file.
--peer-key-file ''
  Path to the peer server TLS key file.
--peer-client-cert-auth 'false'
  Enable peer client cert authentication.
  It's recommended to enable peer client cert authentication to prevent attacks from unauthenticated forged peers (e.g. CVE-2023-44487).
--peer-trusted-ca-file ''
  Path to the peer server TLS trusted CA file.
--peer-cert-allowed-cn ''
  Comma-separated list of allowed CNs for inter-peer TLS authentication.
--peer-cert-allowed-hostname ''
  Comma-separated list of allowed SAN hostnames for inter-peer TLS authentication.
--peer-auto-tls 'false'
  Peer TLS using self-generated certificates if --peer-key-file and --peer-cert-file are not provided.
--self-signed-cert-validity '1'
  The validity period of the client and peer certificates that are automatically generated by etcd when you specify ClientAutoTLS and PeerAutoTLS, the unit is year, and the default is 1.
--peer-crl-file ''
  Path to the peer certificate revocation list file.
--cipher-suites ''
  Comma-separated list of supported TLS cipher suites between client/server and peers (empty will be auto-populated by Go).
--cors '*'
  Comma-separated whitelist of origins for CORS, or cross-origin resource sharing, (empty or * means allow all).
--host-whitelist '*'
  Acceptable hostnames from HTTP client requests, if server is not secure (empty or * means allow all).
--tls-min-version 'TLS1.2'
  Minimum TLS version supported by etcd.
--tls-max-version ''
  Maximum TLS version supported by etcd (empty will be auto-populated by Go).
```

### Authentifizierung {#auth}

```text
--auth-token 'simple'
  Specify a v3 authentication token type and its options ('simple' or 'jwt').
--bcrypt-cost 10
  Specify the cost / strength of the bcrypt algorithm for hashing auth passwords. Valid values are between 4 and 31.
--auth-token-ttl 300
  Time (in seconds) of the auth-token-ttl.
```

### Profiling und Überwachung {#profiling-and-monitoring}

```text
--enable-pprof 'false'
  Enable runtime profiling data via HTTP server. Address is at client URL + "/debug/pprof/"
--metrics 'basic'
  Set level of detail for exported metrics, specify 'extensive' to include server side grpc histogram metrics.
--listen-metrics-urls ''
  List of URLs to listen on for the metrics and health endpoints.
```

### Protokollierung {#logging}

```text
--logger 'zap'
  Currently only supports 'zap' for structured logging.
--log-outputs 'default'
  Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd, or list of comma separated output targets.
--log-level 'info'
  Configures log level. Only supports debug, info, warn, error, panic, or fatal.
--log-format 'json'
  Configures log format. Only supports json, console.
--enable-log-rotation 'false'
  Enable log rotation of a single log-outputs file target.
--log-rotation-config-json '{"maxsize": 100, "maxage": 0, "maxbackups": 0, "localtime": false, "compress": false}'
  Configures log rotation if enabled with a JSON logger config. MaxSize(MB), MaxAge(days,0=no limit), MaxBackups(0=no limit), LocalTime(use computers local time), Compress(gzip)".
--warning-unary-request-duration '300ms'
  Set time duration after which a warning is logged if a unary request takes more than this duration.
```

> [!NOTE]
>   **Hinweis**: Mehrere `--experimental-*`-Optionen wurden in v3.7 in stabile Optionen überführt oder umbenannt.
> Veraltete Optionen unbedingt durch die unten aufgeführten stabilen Entsprechungen ersetzen.

### Verteiltes Tracing {#distributed-tracing}

```text
--enable-distributed-tracing 'false'
  Enable distributed tracing.
--distributed-tracing-address 'localhost:4317'
  Distributed tracing collector address.
--distributed-tracing-service-name 'etcd'
  Distributed tracing service name, must be the same across all etcd instances.
--distributed-tracing-instance-id ''
  Distributed tracing instance ID, must be unique for each etcd instance.
--distributed-tracing-sampling-rate '0'
  Number of samples to collect per million spans for distributed tracing.
```

### v2-Proxy {#v2-proxy}

> [!WARNING]
> Der v2-Proxy wurde vor v3.7 entfernt. Die folgenden Optionen bleiben nur als historische Migrationsreferenz erhalten und dürfen nicht an einen etcd-v3.7-Server übergeben werden.

```text
--proxy 'off'
  Proxy mode setting ('off', 'readonly' or 'on').
--proxy-failure-wait 5000
  Time (in milliseconds) an endpoint will be held in a failed state.
--proxy-refresh-interval 30000
  Time (in milliseconds) of the endpoints refresh interval.
--proxy-dial-timeout 1000
  Time (in milliseconds) for a dial to timeout.
--proxy-write-timeout 5000
  Time (in milliseconds) for a write to timeout.
--proxy-read-timeout 0
  Time (in milliseconds) for a read to timeout.
```

### Funktionen {#features}

```text
--corrupt-check-time '0s'
  Duration of time between cluster corruption check passes.
--compact-hash-check-time '1m'
  Duration of time between leader checks followers compaction hashes.
--compaction-batch-limit 1000
  CompactionBatchLimit sets the maximum revisions deleted in each compaction batch.
--peer-skip-client-san-verification 'false'
  Skip verification of SAN field in client certificate for peer connections.
--watch-progress-notify-interval '10m'
  Duration of periodical watch progress notification.
--warning-apply-duration '100ms'
  Warning is generated if requests take more than this duration.
--bootstrap-defrag-threshold-megabytes
  Enable the defrag during etcd server bootstrap on condition that it will free at least the provided threshold of disk space. Needs to be set to non-zero value to take effect.
--max-learners '1'
  Set the max number of learner members allowed in the cluster membership.
--compaction-sleep-interval
  Sets the sleep interval between each compaction batch.
--downgrade-check-time
  Duration of time between two downgrade status checks.
--snapshot-catchup-entries
  Number of entries for a slow follower to catch up after compacting the raft storage entries.
```

### Funktionsschalter {#feature-gates}

```text
--feature-gates=AllAlpha=true|false
  Enables or disables all alpha features. Default is false.
--feature-gates=AllBeta=true|false
  Enables or disables all beta features. Default is false.
--feature-gates=CompactHashCheck=true
  Enables leader to periodically check follower compaction hashes.
  Replaces: --experimental-compact-hash-check-enabled
--feature-gates=InitialCorruptCheck=true
  Enables corruption check before serving client/peer traffic.
  Replaces: --experimental-initial-corrupt-check
--feature-gates=LeaseCheckpoint=true
  ExperimentalEnableLeaseCheckpoint enables primary lessor to persist lease remainingTTL to prevent indefinite auto-renewal of long lived leases.
  Replaces: --experimental-enable-lease-checkpoint
--feature-gates=LeaseCheckpointPersist=true
  Enable persisting remainingTTL to prevent indefinite auto-renewal of long lived leases. Always enabled in v3.6. Should be used to ensure smooth upgrade from v3.5 clusters with this feature enabled.
  Replaces: --experimental-enable-lease-checkpoint-persist
--feature-gates=SetMemberLocalAddr=true
  Allows setting a member’s local address.
--feature-gates=StopGRPCServiceOnDefrag=true
  Enable etcd gRPC service to stop serving client requests on defragmentation.
  Replaces: --experimental-stop-grpc-service-on-defrag
--feature-gates=TxnModeWriteWithSharedBuffer=true
  Enable the write transaction to use a shared buffer in its readonly check operations.
  Replaces: --experimental-txn-mode-write-with-shared-buffer
```

### Unsichere Funktionen {#unsafe-features}

> [!WARNING]
> **Warnung**: Die Verwendung unsicherer Funktionen kann die Garantien des Konsensprotokolls außer Kraft setzen!

```text
--force-new-cluster 'false'
  Force to create a new one-member cluster.
--unsafe-no-fsync 'false'
  Disables fsync, unsafe, will cause data loss.
```

## Konfigurationsdatei {#configuration-file}

Eine etcd-Konfigurationsdatei besteht aus einer YAML-Map. Ihre Schlüssel sind die Namen der Befehlszeilenoptionen und ihre Werte die jeweiligen Optionswerte.
Um diese Datei zu verwenden, ihren Pfad als Wert der Option `--config-file` oder der Umgebungsvariablen `ETCD_CONFIG_FILE` angeben.

Ein Beispiel bietet die [etcd.conf.yml-Beispieldatei][etcd.conf.yml sample].

> [!NOTE]
> Zeitdauerfelder wie `--grpc-keepalive-min-time`, `--grpc-keepalive-interval`,
> `--grpc-keepalive-timeout`, `--backend-batch-interval`, `--corrupt-check-time`,
> `--compact-hash-check-time`, `--compaction-sleep-interval`,
> `--watch-progress-notify-interval`, `--warning-apply-duration`,
> `--warning-unary-request-duration` und `--downgrade-check-time` akzeptieren
> als Befehlszeilenoptionen menschenlesbare Zeichenfolgen (z. B. `10m`, `5s`),
> in einer Konfigurationsdatei jedoch nur **ganzzahlige Werte in
> Nanosekunden**. Dies ist eine [bekannte Einschränkung der Go-Standardbibliothek](https://github.com/golang/go/issues/10275),
> bei der `time.Duration` als einfache Ganzzahl deserialisiert wird.
>
> Beispiel für ein Intervall von 10 Minuten für Watch-Fortschrittsmeldungen in einer Konfigurationsdatei:
>
> ```yaml
> # Correct: 10 minutes in nanoseconds
> watch-progress-notify-interval: 600000000000
>
> # Incorrect: will produce an unmarshal error
> watch-progress-notify-interval: '10m'
> ```

[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
[etcd.conf.yml sample]: https://github.com/etcd-io/etcd/blob/main/etcd.conf.yml.sample
[snake case]: https://en.wikipedia.org/wiki/Snake_case
