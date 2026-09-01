# German translation guide

This document defines the terminology, style, and fidelity requirements for the
German edition in `content/**/*.de.md`. English pages are authoritative. German
translations live beside them and use the suffix `.de.md`; section indexes use
`_index.de.md`.

## Scope and fidelity

- Translate titles, descriptions, navigation labels, prose, explanatory lists,
  table headings and cells, callouts, and link text completely into natural
  professional German. Do not summarize, omit, or add information.
- Preserve product names, protocol names, commands, configuration keywords,
  API/RPC/message/field names, environment variables, filenames, paths, URLs,
  metrics, log fields, placeholders, and established abbreviations exactly.
- Keep copyable commands, configuration, source code, protocol messages,
  program output, logs, and error messages byte-for-byte identical. Explanatory
  comments inside code fences also remain unchanged so examples stay copyable.
- Keep upstream source, version, commit, aliases, weight, icon, module, and
  licensing metadata unchanged. Do not translate verbatim licence text.
- Preserve every explicit English anchor exactly. When an English heading has
  no explicit anchor, append its rendered English anchor to the translated
  heading so existing fragment links continue to work.
- Localize links between component pages to `/de/<component>/...`. Images,
  downloads, JSON, SVG, and other shared assets retain their language-neutral
  paths.
- Preserve all numbers, versions, units, defaults, deprecation states,
  negations, conditions, and warning strength. Keep digits as digits; never
  spell them out during translation.

## German style

- Use standard German for technically experienced readers working with Linux,
  networking, distributed systems, and database operations.
- Prefer clear, compact sentences and established German technical usage over
  literal word-for-word translation. Avoid unnecessary Anglicisms, but retain
  product-specific English terms when translating them would obscure the API
  or operational concept.
- Translate `must` as `muss` or `müssen`, `should` as `sollte` or `sollten`, and
  `may/can` as `kann` or `können`. Never weaken or strengthen normative force.
- Use direct, impersonal instructions where possible. When the reader must be
  addressed, use formal `Sie` consistently; never switch to `du`.
- Use German quotation marks only in prose that is not a literal. Preserve
  original punctuation inside code, command output, filenames, URLs, and
  quoted API values.
- Keep brand spelling fixed: `PostgreSQL`, `Patroni`, `pgBackRest`, `PgBouncer`,
  `pgBadger`, `HAProxy`, `etcd`, `etcdctl`, `Prometheus`, `Grafana`,
  `Kubernetes`, `OpenSSL`, and `NGINX`.
- Keep common abbreviations unchanged, including ACL, API, CA, CLI, DCS, DDoS,
  DNS, gRPC, HTTP, MVCC, PITR, QUIC, Raft, RPC, SNI, SPOE, TCP, TLS, TTL, and WAL.
- Preserve chapter numbers, command names, API names, and configuration keys in
  headings; translate the remaining heading text and link labels.

## Required terminology

| English | German |
| --- | --- |
| high availability | Hochverfügbarkeit |
| automatic failover | automatisches Failover |
| switchover | Switchover |
| distributed configuration store (DCS) | verteilter Konfigurationsspeicher (DCS) |
| connection pool / pooling | Verbindungspool / Verbindungs-Pooling |
| backup / restore / recovery | Backup / Wiederherstellung / Recovery |
| archive / write-ahead log | Archiv / Write-Ahead-Log |
| point-in-time recovery | Point-in-Time-Recovery |
| primary / standby / replica | Primärserver / Standby / Replikat |
| leader / follower | Leader / Follower |
| learner member | Learner-Mitglied |
| quorum | Quorum |
| consensus | Konsens |
| lease | Lease |
| key-value store | Schlüssel-Wert-Speicher |
| keyspace | Schlüsselraum |
| revision | Revision |
| compaction | Kompaktierung |
| defragmentation | Defragmentierung |
| snapshot | Snapshot |
| watch / watcher | Watch / Watcher |
| rolling upgrade | Rolling Upgrade |
| mixed-version cluster | Cluster mit gemischten Versionen |
| single-member cluster | Ein-Mitglied-Cluster |
| multi-machine cluster | Cluster mit mehreren Rechnern |
| load balancer / load balancing | Load-Balancer / Lastverteilung |
| reverse proxy | Reverse-Proxy |
| frontend / backend | Frontend / Backend |
| request / response | Anfrage / Antwort |
| HTTP header | HTTP-Header |
| health check | Health Check |
| graceful shutdown | geordnetes Herunterfahren |
| graceful reload | unterbrechungsfreies Neuladen |
| runtime API / runtime CLI | Runtime-API / Runtime-CLI |
| access control list | Zugriffskontrollliste |
| stick table | Stick Table |
| sample fetch | Sample-Abruf |
| rate limit | Ratenbegrenzung |
| timeout | Zeitüberschreitung |
| logging | Protokollierung |
| troubleshooting | Fehlerbehebung |
| tune / tuning | optimieren / Optimierung |
| file descriptor | Dateideskriptor |
| Unix socket | Unix-Socket |
| throughput / latency | Durchsatz / Latenz |
| source address | Quelladresse |
| command line | Befehlszeile |
| configuration | Konfiguration |
| installation | Installation |
| user guide | Benutzerhandbuch |
| release notes / changelog | Versionshinweise / Änderungsprotokoll |

Product-specific command names and configuration keywords that resemble any
term in this table remain unchanged when they are literals, for example
`leader`, `backend`, `watch`, `backup`, `restore`, `timeout`, and `stick-table`.

## Acceptance criteria

- Every English Markdown page has exactly one same-directory German page.
- German and English pages preserve `upstream_link`, explicit anchors, fenced
  code blocks, shortcodes, images, reference definitions, internal link
  destinations, HTML tags, list nesting, table shape, and numeric facts.
- German pages contain no untranslated English prose except protected literals,
  names, code, output, logs, errors, and verbatim legal text.
- After source validation, run a production Hugo build and verify German routes,
  fragments, navigation order, Markdown/LLMS outputs, search, and local links.
