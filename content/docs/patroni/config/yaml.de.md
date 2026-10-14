---
title: "YAML-Konfigurationseinstellungen"
linkTitle: "YAML-Konfiguration"
weight: 20
icon: fa-solid fa-code
description: "Vollständige Referenz der Optionen und Abschnitte der Patroni-YAML-Konfiguration."
module: [PATRONI]
categories: [Referenz]
aliases: [/patroni/config/yaml/]
upstream_link: "https://patroni.readthedocs.io/en/latest/yaml_configuration.html"
---

<a id="yaml"></a>

--------

## Global/Allgemein {#globaluniversal}

- **thread_pool_size**: Größe des Threadpools, mit dem Patroni asynchrone Aufgaben ausführt und während der Leader-Wahl oder bei Failsafe-Prüfungen über die REST API mit anderen Mitgliedern kommuniziert. Mindestwert: `5`, Standardwert: `5`.
- **thread_stack_size**: legt die Stackgröße für von Patroni gestartete Threads fest. Der Wert muss an `64kB` ausgerichtet sein. Mindestwert: `64kB`, Standardwert (von Patroni gesetzt): `512kB`.
- **name**: Name des Hosts. Er muss im Cluster eindeutig sein.
- **namespace**: Pfad im Konfigurationsspeicher, unter dem Patroni Informationen über den Cluster speichert. Standardwert: "/service"
- **scope**: Clustername

<a id="log_settings"></a>

--------

## Protokollierung {#log}

- **type**: legt das Protokollformat fest. Mögliche Werte sind **plain** und **json**. Für das Format **json** muss [jsonlogger](/de/docs/patroni/installation#extras) installiert sein. Der Standardwert ist **plain**.
- **level**: legt die allgemeine Protokollierungsstufe fest. Standardwert: **INFO** (siehe [Dokumentation der Python-Protokollierung](https://docs.python.org/3.6/library/logging.html#levels))
- **traceback_level**: legt die Stufe fest, auf der Tracebacks sichtbar sind. Standardwert: **ERROR**. Auf **DEBUG** setzen, wenn Tracebacks nur bei aktiviertem **log.level=DEBUG** sichtbar sein sollen.
- **format**: legt die Formatzeichenfolge für Protokolle fest. Beim Protokolltyp **plain** sollte das Format eine Zeichenfolge sein. Verfügbare Attribute stehen unter [LogRecord-Attribute](https://docs.python.org/3.6/library/logging.html#logrecord-attributes). Beim Protokolltyp **json** kann das Format neben einer Zeichenfolge auch eine Liste sein. Jeder Listeneintrag sollte einem LogRecord-Attribut entsprechen. Dabei wird nur der Feldname benötigt; **%(** und **)** sollten weggelassen werden. Um ein Protokollfeld unter einem anderen Schlüsselnamen auszugeben, ein Dictionary verwenden: Der Schlüssel bezeichnet das Protokollfeld, der Wert den im Protokoll auszugebenden Feldnamen. Standardwert: **%(asctime)s %(levelname)s: %(message)s**
- **dateformat**: legt die Formatzeichenfolge für Datum und Uhrzeit fest (siehe [Dokumentation zu formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime)).
- **static_fields**: fügt dem Protokoll zusätzliche Felder hinzu. Diese Option ist nur verfügbar, wenn der Protokolltyp auf **json** gesetzt ist.
- **max_queue_size**: Patroni verwendet eine zweistufige Protokollierung. Protokolleinträge werden in eine Warteschlange im Arbeitsspeicher geschrieben; ein separater Thread entnimmt sie und schreibt sie nach stderr oder in eine Datei. Die interne Warteschlange ist standardmäßig auf **1000** Einträge begrenzt, was für die Protokolle der letzten 1h20m ausreicht.
- **dir**: Verzeichnis für die Anwendungsprotokolle. Es muss existieren und für den Benutzer, der Patroni ausführt, beschreibbar sein. Ist dieser Wert gesetzt, bewahrt die Anwendung standardmäßig 4 Protokolldateien mit jeweils 25MB auf. Diese Aufbewahrungswerte lassen sich mit `file_num` und `file_size` anpassen (siehe unten).
- **mode**: Berechtigungen für Protokolldateien (z. B. `0644`). Ohne Angabe werden die Berechtigungen anhand des aktuellen umask-Werts gesetzt.
- **file_num**: Anzahl der aufzubewahrenden Anwendungsprotokolle.
- **file_size**: Größe der Datei patroni.log (in Bytes), bei der eine Protokollrotation ausgelöst wird.
- **loggers**: dieser Abschnitt ermöglicht das Neufestlegen der Protokollierungsstufe je Python-Modul
  - **patroni.postmaster: WARNING**
  - **urllib3: DEBUG**
- **deduplicate_heartbeat_logs**: bei `true` werden aufeinanderfolgende identische Heartbeat-Protokolleinträge nicht ausgegeben. Standardwert: `false`.

> [!WARNING]
> Der Ausführungszeitpunkt der HA-Schleife kann bei der Diagnose von Failovers aufgrund erschöpfter Ressourcen und ähnlicher Probleme sehr wertvoll sein. Ist `deduplicate_heartbeat_logs` auf `true` gesetzt, wird für die Ausführung der HA-Schleife kein Protokolleintrag erzeugt (außer bei einem Leader-Wechsel). Diese möglicherweise nützliche Information steht dann in den Protokollen nicht zur Verfügung.

Das folgende Beispiel konfiguriert Patroni für die Protokollierung im JSON-Format.

```yaml
log:
   type: json
   format:
      - message
      - module
      - asctime: '@timestamp'
      - levelname: level
   static_fields:
      app: patroni
```

<a id="bootstrap_settings"></a>

--------

## Bootstrap-Konfiguration {#bootstrap-configuration}

> [!NOTE]
> Sobald Patroni den Cluster erstmals initialisiert und die Einstellungen im DCS gespeichert hat, haben spätere Änderungen am Abschnitt `bootstrap.dcs` der YAML-Konfiguration keine Wirkung mehr! Zum Ändern dieser Einstellungen entweder [patronictl_edit_config](/de/docs/patroni/patronictl#patronictl_edit_config) oder die [REST API](/de/docs/patroni/rest_api#rest_api) von Patroni verwenden.

- **bootstrap**:
  - **dcs**: dieser Abschnitt wird nach der Initialisierung des neuen Clusters in `/<namespace>/<scope>/config` des angegebenen Konfigurationsspeichers geschrieben. Er enthält die globale dynamische Konfiguration des Clusters. Unter `bootstrap.dcs` können alle unter [Dynamische Konfigurationseinstellungen](/de/docs/patroni/config/dynamic#dynamic) beschriebenen Parameter angegeben werden. Nachdem Patroni den neuen Cluster initialisiert hat (Bootstrap), schreibt es diesen Abschnitt in `/<namespace>/<scope>/config` des Konfigurationsspeichers.

  - **method**: benutzerdefiniertes Skript zur Initialisierung dieses Clusters.

    Einzelheiten enthält die [Dokumentation benutzerdefinierter Bootstrap-Methoden](/de/docs/patroni/replica_bootstrap#custom_bootstrap). Bei Angabe von `initdb` wird der standardmäßige Befehl `initdb` verwendet. `initdb` wird auch aufgerufen, wenn die Konfigurationsdatei keinen Parameter `method` enthält.

  - **initdb**: (optional) Liste der an initdb zu übergebenden Optionen.

    - **- data-checksums**: muss aktiviert sein, wenn pg_rewind unter 9.3 benötigt wird.
    - **- encoding: UTF8**: Standardzeichencodierung für neue Datenbanken.
    - **- locale: UTF8**: Standard-Locale für neue Datenbanken.

  - **post_bootstrap** oder **post_init**: Zusätzliches Skript, das nach der Initialisierung des Clusters ausgeführt wird. Es erhält eine Verbindungs-URL (mit dem Cluster-Superuser als Benutzername). Die Variable PGPASSFILE wird auf den Pfad der pgpass-Datei gesetzt.

<a id="citus_settings"></a>

--------

## Citus {#citus}

Aktiviert die Integration von Patroni mit [Citus](https://docs.citusdata.com). Ist sie konfiguriert, übernimmt Patroni die Registrierung der Citus-Worker-Knoten beim Coordinator. Weitere Informationen zur Citus-Unterstützung stehen [hier](/de/docs/patroni/citus#citus).

- **group**: Citus-Gruppen-ID als Ganzzahl. Für den Coordinator `0` verwenden, für Worker `1`, `2` usw.
- **database**: Datenbank, in der die Erweiterung [citus](/de/docs/patroni/citus#citus) erstellt werden sollte. Sie muss auf dem Coordinator und allen Workern identisch sein. Derzeit wird nur eine Datenbank unterstützt.

<a id="consul_settings"></a>

--------

## Consul {#consul}

Die meisten Parameter sind optional, aber **host** oder **url** muss angegeben werden.

- **host**: host:port des lokalen Consul-Agenten.
- **url**: URL des lokalen Consul-Agenten im Format: http(s)://host:port
- **port**: (optional) Consul-Port
- **scheme**: (optional) **http** oder **https**, Standardwert **http**
- **token**: (optional) ACL-Token
- **verify**: (optional) bestimmt, ob das SSL-Zertifikat bei HTTPS-Anfragen geprüft wird
- **cacert**: (optional) CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **cert**: (optional) Datei mit dem Clientzertifikat
- **key**: (optional) Datei mit dem Clientschlüssel. Kann leer sein, wenn der Schlüssel Bestandteil von **cert** ist.
- **dc**: (optional) Rechenzentrum, mit dem kommuniziert werden soll. Standardmäßig wird das Rechenzentrum des Hosts verwendet.
- **consistency**: (optional) wählt den Konsistenzmodus von Consul. Mögliche Werte: `default`, `consistent` oder `stale` (Einzelheiten in der [Consul-API-Referenz](https://www.consul.io/api/features/consistency.html/))
- **checks**: (optional) Liste der für die Sitzung verwendeten Consul Health Checks. Standardmäßig wird eine leere Liste verwendet.
- **register_service**: (optional) bestimmt, ob ein Dienst registriert wird, dessen Name durch den Parameter scope festgelegt ist und der je nach Knotenrolle das Tag master, primary, replica oder standby-leader erhält. Standardwert **false**
- **service_tags**: (optional) zusätzliche statische Tags für den Consul-Dienst neben der Rolle (`primary`/`replica`/`standby-leader`). Standardmäßig wird eine leere Liste verwendet.
- **service_check_interval**: (optional) Häufigkeit der Health Checks für die registrierte URL. Standardwert: '5s'.
- **service_check_tls_server_name**: (optional) überschreibt den SNI-Host bei TLS-Verbindungen; siehe auch die [API-Referenz für Consul-Agent-Prüfungen](https://www.consul.io/api-docs/agent/check#tlsservername).

`token` benötigt folgende ACL-Berechtigungen:

    service_prefix "${scope}" {
        policy = "write"
    }
    key_prefix "${namespace}/${scope}" {
        policy = "write"
    }
    session_prefix "" {
        policy = "write"
    }

--------

## etcd {#etcd}

Die meisten Parameter sind optional, aber einer der Parameter **host**, **hosts**, **url**, **proxy** oder **srv** muss angegeben werden.

- **host**: host:port des etcd-Endpunkts.
- **hosts**: Liste der etcd-Endpunkte im Format host1:port1,host2:port2,etc... Möglich sind eine durch Kommas getrennte Zeichenfolge oder eine YAML-Liste.
- **use_proxies**: ist dieser Parameter auf true gesetzt, behandelt Patroni **hosts** als Liste von Proxys und ermittelt nicht die Topologie des etcd-Clusters.
- **url**: URL für etcd.
- **proxy**: Proxy-URL für etcd. Bei einer Verbindung zu etcd über einen Proxy diesen Parameter anstelle von **url** verwenden.
- **srv**: Domain, in der nach SRV-Einträgen für die automatische Clustererkennung gesucht wird. Patroni fragt für die angegebene Domain diese SRV-Dienstnamen ab (in dieser Reihenfolge bis zum ersten Erfolg): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Werden SRV-Einträge für `_etcd-server-ssl` oder `_etcd-server` gefunden, wird über das ETCD-Peer-Protokoll bei ETCD nach verfügbaren Mitgliedern gefragt. Andernfalls werden die Hosts aus den SRV-Einträgen verwendet.
- **srv_suffix**: konfiguriert ein Suffix für den bei der Erkennung abgefragten SRV-Namen. Mit diesem Flag lassen sich mehrere etcd-Cluster unter derselben Domain unterscheiden. Es funktioniert nur zusammen mit **srv**. Sind beispielsweise `srv_suffix: foo` und `srv: example.org` gesetzt, wird folgende DNS-SRV-Abfrage ausgeführt: `_etcd-client-ssl-foo._tcp.example.org` (entsprechend für jeden möglichen ETCD-SRV-Dienstnamen).
- **protocol**: (optional) http oder https; ohne Angabe wird http verwendet. Ist **url** oder **proxy** angegeben, wird das Protokoll daraus übernommen.
- **username**: (optional) Benutzername für die etcd-Authentifizierung.
- **password**: (optional) Passwort für die etcd-Authentifizierung.
- **cacert**: (optional) CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **cert**: (optional) Datei mit dem Clientzertifikat
- **key**: (optional) Datei mit dem Clientschlüssel. Kann leer sein, wenn der Schlüssel Bestandteil von **cert** ist.

--------

## Etcdv3 {#etcdv3}

Damit Patroni mit dem etcd-Cluster über Protokollversion 3 arbeitet, muss in der Patroni-Konfigurationsdatei der Abschnitt `etcd3` verwendet werden. Alle Konfigurationsparameter entsprechen denen für `etcd`.

> [!WARNING]
> Mit Protokollversion 2 erstellte Schlüssel sind mit Protokollversion 3 nicht sichtbar und umgekehrt. Daher ist ein Wechsel von `etcd` zu `etcd3` allein durch Ändern der Patroni-Konfigurationsdatei nicht möglich. Zudem verwendet Patroni das gRPC-Gateway (Proxy) von etcd zur Kommunikation mit der V3 API, weshalb eine TLS-Authentifizierung über den Common Name nicht möglich ist.

--------

## ZooKeeper {#zookeeper}

- **hosts**: Liste der ZooKeeper-Clustermitglieder im Format: \['host1:port1', 'host2:port2', 'etc...'\].
- **use_ssl**: (optional) bestimmt, ob SSL verwendet wird. Standardwert: `false`. Bei `false` werden alle SSL-spezifischen Parameter ignoriert.
- **cacert**: (optional) CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **cert**: (optional) Datei mit dem Clientzertifikat.
- **key**: (optional) Datei mit dem Clientschlüssel.
- **key_password**: (optional) Passwort für den Clientschlüssel.
- **verify**: (optional) bestimmt, ob das Zertifikat geprüft wird. Standardwert: `true`.
- **set_acls**: (optional) falls gesetzt, wird Kazoo so konfiguriert, dass es auf jeden neu erstellten ZNode eine Standard-ACL anwendet. ACLs können das Schema `x509` (Standard) oder andere unterstützte ZooKeeper-Schemata wie `digest` verwenden. Sie sollten als Dictionary angegeben werden, dessen Schlüssel der vollständige Principal (optional mit vorangestelltem Schema) und dessen Wert eine Liste von Berechtigungen ist. Als Berechtigungen sind eine oder mehrere aus `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN` oder `ALL` möglich. Beispiel: `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **auth_data**: (optional) Zugangsdaten für die Verbindung. Sollte ein Dictionary mit `scheme` als Schlüssel und `credential` als Wert sein. Standardwert ist ein leeres Dictionary.

> [!NOTE]
> Für SSL-Unterstützung muss `kazoo>=2.6.0` installiert sein.

--------

## Exhibitor {#exhibitor}

- **hosts**: anfängliche Liste der Exhibitor-Knoten (ZooKeeper) im Format: 'host1,host2,etc...'. Diese Liste wird bei jeder Änderung der Topologie des Exhibitor-Clusters (ZooKeeper) automatisch aktualisiert.
- **poll_interval**: Häufigkeit, mit der die Liste der ZooKeeper- und Exhibitor-Knoten von Exhibitor aktualisiert werden sollte.
- **port**: Exhibitor-Port.

<a id="kubernetes_settings"></a>

--------

## Kubernetes {#kubernetes}

- **bypass_api_service**: (optional) bei der Kommunikation mit der Kubernetes API verwendet Patroni normalerweise den Dienst [kubernetes](/de/docs/patroni/kubernetes#kubernetes), dessen Adresse den Pods über die Umgebungsvariable `KUBERNETES_SERVICE_HOST` bereitgestellt wird. Ist `bypass_api_service` auf `true` gesetzt, ermittelt Patroni die Liste der API-Knoten hinter dem Dienst und verbindet sich direkt mit ihnen.
- **namespace**: (optional) Kubernetes-Namespace, in dem der Patroni-Pod läuft. Standardwert: `default`.
- **labels**: Labels im Format `{label1: value1, label2: value2}`. Mit diesen Labels werden vorhandene Objekte (Pods sowie Endpoints oder ConfigMaps) gesucht, die zum aktuellen Cluster gehören. Außerdem setzt Patroni sie auf jedem von ihm erstellten Objekt (Endpoint oder ConfigMap).
- **scope_label**: (optional) Name des Labels mit dem Clusternamen. Standardwert: `cluster-name`.
- **bootstrap_labels**: (optional) Labels im Format `{label1: value1, label2: value2}`. Sie werden einem Patroni-Pod zugewiesen, wenn sein Zustand `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` oder `creating replica` ist.
- **role_label**: (optional) Name des Labels mit der Rolle (`primary`, `replica` oder ein anderer benutzerdefinierter Wert). Patroni setzt dieses Label auf dem Pod, in dem es läuft. Standardwert: `role`.
- **leader_label_value**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `primary` ist. Standardwert: `primary`.
- **follower_label_value**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `replica` ist. Standardwert: `replica`.
- **standby_leader_label_value**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `standby_leader` ist. Standardwert: `primary`.
- **tmp_role_label**: (optional) Name des temporären Labels mit der Rolle (`primary` oder `replica`). Der Wert dieses Labels entspricht immer dem Standardwert der jeweiligen Rolle. Nur bei Bedarf setzen.
- **use_endpoints**: (optional) bei true verwendet Patroni Endpoints anstelle von ConfigMaps für die Leader-Wahl und zum Speichern des Clusterzustands.
- **pod_ip**: (optional) IP-Adresse des Pods, in dem Patroni läuft. Dieser Wert ist erforderlich, wenn `use_endpoints` aktiviert ist, und wird beim Hochstufen von PostgreSQL im Pod zum Befüllen der Subsets des Leader-Endpoints verwendet.
- **ports**: (optional) enthält das Service-Objekt einen Namen für den Port, muss derselbe Name im Endpoint-Objekt erscheinen; andernfalls funktioniert der Dienst nicht. Ist der Dienst beispielsweise als `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}` definiert, muss `kubernetes.ports: [{"name": "postgresql", "port": 5432}]` gesetzt werden. Patroni verwendet dies zum Aktualisieren der Subsets des Leader-Endpoints. Dieser Parameter wird nur verwendet, wenn `kubernetes.use_endpoints` gesetzt ist.
- **cacert**: (optional) gibt die CA_BUNDLE-Datei mit den Zertifikaten vertrauenswürdiger CAs an, die zum Prüfen der SSL-Zertifikate der Kubernetes API verwendet werden. Ohne Angabe verwendet Patroni den Wert aus dem ServiceAccount-Secret.
- **retriable_http_codes**: (optional) Liste der HTTP-Statuscodes der K8s API, bei denen ein erneuter Versuch erfolgt. Standardmäßig wiederholt Patroni die Anfrage bei `500`, `503` und `504` oder wenn die Antwort der K8s API den HTTP-Header `retry-after` enthält.

<a id="raft_settings"></a>

--------

## Raft (veraltet) {#raft-deprecated}

- **self_addr**: `ip:port`, an dem auf Raft-Verbindungen gewartet wird. `self_addr` muss von anderen Clusterknoten aus erreichbar sein. Ohne Angabe nimmt der Knoten nicht am Konsens teil.

- **bind_addr**: (optional) `ip:port`, an dem auf Raft-Verbindungen gewartet wird. Ohne Angabe wird `self_addr` verwendet.

- **partner_addrs**: Liste der anderen Patroni-Knoten im Cluster im Format: \['ip1:port', 'ip2:port', 'etc...'\]

- **data_dir**: Verzeichnis zum Speichern des Raft-Logs und des Snapshots. Ohne Angabe wird das aktuelle Arbeitsverzeichnis verwendet.

- **password**: (optional) verschlüsselt den Raft-Datenverkehr mit dem angegebenen Passwort; erfordert das Python-Modul `cryptography`.
- **min_timeout**: (optional) minimale Zeitüberschreitung für Wahlen in der zugrunde liegenden Raft-Implementierung pysyncobj, in Sekunden. Muss größer als 3 * `append_entries_period` sein. Standardwert: `0.4`.
- **max_timeout**: (optional) maximale Zeitüberschreitung für Wahlen in der zugrunde liegenden Raft-Implementierung pysyncobj, in Sekunden. Muss größer als `min_timeout` sein. Standardwert: `1.4`.
- **connection_timeout**: (optional) Zeit in Sekunden, nach der eine Verbindung ohne Datenempfang als unterbrochen gilt. Muss größer oder gleich `max_timeout` sein. Standardwert: `3.5`.
- **append_entries_period**: (optional) Intervall in Sekunden zum Senden von Heartbeat-Befehlen (append_entries). Muss kleiner als ein Drittel von `min_timeout` sein. Standardwert: `0.1`.
- **connection_retry_time**: (optional) Intervall in Sekunden zwischen erneuten Verbindungsversuchen zu nicht erreichbaren Knoten. Standardwert: `5.0`.
- **leader_fallback_timeout**: (optional) Zeit in Sekunden, nach der ein Leader ohne Antwort von der Mehrheit in den Follower-Zustand zurückkehrt. Muss größer als `append_entries_period` sein. Standardwert: `30.0`.

> [!NOTE]
> Diese Zeitüberschreitungsparameter sind in Netzwerken mit hoher Latenz nützlich, in denen die standardmäßigen Zeitüberschreitungen von pysyncobj zu kurz sind. Folgende Bedingungen müssen erfüllt sein: `min_timeout` > 3 * `append_entries_period`, `max_timeout` > `min_timeout`, `connection_timeout` >= `max_timeout` und `leader_fallback_timeout` > `append_entries_period`. Patroni prüft diese Bedingungen beim Start und verweigert den Start, wenn sie verletzt sind. Diese Werte können nicht zur Laufzeit geändert werden und erfordern einen Neustart.
>
> [!WARNING]
> Diese Einstellungen verlängern lediglich die Zeitüberschreitungen für Wahlen und Verbindungen in pysyncobj; sie verlängern nicht die Frist, die Patroni jedem einzelnen Raft-Befehl setzt. Jeder Raft-Befehl (Aktualisierung der Leader-Sperre, Schreiben des Clusterzustands) muss weiterhin innerhalb von `retry_timeout` (Standardwert `10`) abgeschlossen sein. Bei Verbindungen mit sehr hoher Latenz – ungefähr ab einigen Sekunden Round-Trip-Zeit – kann ein einzelner Befehl `retry_timeout` überschreiten, selbst wenn `connection_timeout` deutlich über die RTT angehoben wurde. Der DCS erscheint dann als nicht erreichbar, und der Primärserver kann herabgestuft werden. Bei solchen Verbindungen müssen auch `retry_timeout` und `ttl` entsprechend angehoben werden; dabei muss `loop_wait + 2 * retry_timeout <= ttl` weiterhin gelten.

  Kurze FAQ zur Raft-Implementierung

  - F: Wie lassen sich alle am Konsens beteiligten Knoten auflisten?

    A: `syncobj_admin -conn host:port -status`, wobei host:port die Adresse eines Clusterknotens ist.

  - F: Ein am Konsens beteiligter Knoten ist ausgefallen, und seine IP-Adresse kann nicht für einen anderen Knoten wiederverwendet werden. Wie lässt sich dieser Knoten aus dem Konsens entfernen?

    A: `syncobj_admin -conn host:port -remove host2:port2`, wobei `host2:port2` die Adresse des Knotens ist, der aus dem Konsens entfernt werden soll.

  - F: Woher bekommt man das Werkzeug `syncobj_admin`?

    A: Es wird zusammen mit dem Modul `pysyncobj` (RAFT-Implementierung in Python) installiert, von dem Patroni abhängt.

  - F: Kann ein Patroni-Knoten betrieben werden, ohne ihn in den Konsens aufzunehmen?

    A: Ja, dazu `raft.self_addr` in der Patroni-Konfiguration auskommentieren oder entfernen.

  - F: Können Patroni und PostgreSQL auf nur zwei Knoten betrieben werden?

    A: Ja, auf dem dritten Knoten kann `patroni_raft_controller` laufen (ohne Patroni und PostgreSQL). Bei dieser Konfiguration kann ein Knoten vorübergehend ausfallen, ohne den Primärserver zu beeinträchtigen.

<a id="postgresql_settings"></a>

--------

## PostgreSQL {#postgresql}

- **postgresql**:
  - **authentication**:

    - **superuser**:
      - **username**: Name des Superusers, der bei der Initialisierung (initdb) festgelegt und später von Patroni für Verbindungen zu Postgres verwendet wird.
      - **password**: Passwort des Superusers, das bei der Initialisierung (initdb) festgelegt wird.
      - **sslmode**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
      - **sslkey**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
      - **sslpassword**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `sslkey` angegebenen geheimen Schlüssel festlegt.
      - **sslcert**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
      - **sslrootcert**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
      - **sslcrl**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslcrldir**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslnegotiation**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
      - **gssencmode**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
      - **channel_binding**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.
    - **replication**:
      - **username**: Benutzername für die Replikation; der Benutzer wird bei der Initialisierung erstellt. Replikate verwenden ihn, um per Streaming-Replikation auf die Replikationsquelle zuzugreifen.
      - **password**: Passwort für die Replikation; der Benutzer wird bei der Initialisierung erstellt.
      - **sslmode**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
      - **sslkey**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
      - **sslpassword**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `sslkey` angegebenen geheimen Schlüssel festlegt.
      - **sslcert**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
      - **sslrootcert**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
      - **sslcrl**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslcrldir**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslnegotiation**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
      - **gssencmode**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
      - **channel_binding**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.
    - **rewind**:
      - **username**: (optional) Name des Benutzers für `pg_rewind`; er wird bei der Initialisierung von Postgres 11+ erstellt und erhält alle erforderlichen [Berechtigungen](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8).
      - **password**: (optional) Passwort des Benutzers für `pg_rewind`; er wird bei der Initialisierung erstellt.
      - **sslmode**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
      - **sslkey**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
      - **sslpassword**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `sslkey` angegebenen geheimen Schlüssel festlegt.
      - **sslcert**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
      - **sslrootcert**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
      - **sslcrl**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslcrldir**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
      - **sslnegotiation**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
      - **gssencmode**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
      - **channel_binding**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.

  - **callbacks**: Callback-Skripte, die bei bestimmten Aktionen ausgeführt werden. Patroni übergibt Aktion, Rolle und Clusternamen. (scripts/aws.py zeigt ein Beispiel für solche Skripte.)

    - **on_reload**: führt dieses Skript aus, wenn das Neuladen der Konfiguration ausgelöst wird.
    - **on_restart**: führt dieses Skript aus, wenn Postgres neu startet (ohne Rollenwechsel).
    - **on_role_change**: führt dieses Skript aus, wenn Postgres hoch- oder herabgestuft wird.
    - **on_start**: führt dieses Skript aus, wenn Postgres startet.
    - **on_stop**: führt dieses Skript aus, wenn Postgres stoppt.

  - **connect_address**: IP-Adresse + Port, über die Postgres für andere Knoten und Anwendungen erreichbar ist.

  - **proxy_address**: IP-Adresse + Port, über die ein neben Postgres laufender Verbindungspool (z. B. PgBouncer) erreichbar ist. Der Wert wird als `proxy_url` in den Mitgliedsschlüssel im DCS geschrieben und kann für die Diensterkennung verwendet werden beziehungsweise nützlich sein.

  - **create_replica_methods**: geordnete Liste der Erstellungsmethoden, mit denen ein Patroni-Knoten zu einem neuen Replikat wird. Die Standardmethode ist "basebackup"; andere Methoden verweisen auf Skripte, die jeweils mit einem eigenen Konfigurationseintrag konfiguriert werden. Weitere Erläuterungen enthält die [Dokumentation benutzerdefinierter Methoden zur Replikaterstellung](/de/docs/patroni/replica_bootstrap#custom_replica_creation).

  - **data_dir**: Pfad zum Postgres-Datenverzeichnis, das [bereits existiert](/de/docs/patroni/existing_data#existing_data) oder von Patroni initialisiert werden soll.

  - **config_dir**: Pfad zum Postgres-Konfigurationsverzeichnis; standardmäßig das Datenverzeichnis. Es muss für Patroni beschreibbar sein.

  - **bin_dir**: (optional) Pfad zu den PostgreSQL-Programmdateien (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). Ohne Angabe oder bei einer leeren Zeichenfolge werden die Programme über die Umgebungsvariable PATH gesucht.

  - **bin_name**: (optional) ermöglicht das Überschreiben der Postgres-Programmnamen bei einer benutzerdefinierten Postgres-Distribution:

    - **pg_ctl**: (optional) benutzerdefinierter Name für die Programmdatei `pg_ctl`.
    - **initdb**: (optional) benutzerdefinierter Name für die Programmdatei `initdb`.
    - **pg_controldata**: (optional) benutzerdefinierter Name für die Programmdatei `pg_controldata`.
    - **pg_basebackup**: (optional) benutzerdefinierter Name für die Programmdatei `pg_basebackup`.
    - **postgres**: (optional) benutzerdefinierter Name für die Programmdatei `postgres`.
    - **pg_isready**: (optional) benutzerdefinierter Name für die Programmdatei `pg_isready`.
    - **pg_rewind**: (optional) benutzerdefinierter Name für die Programmdatei `pg_rewind`.

  - **listen**: IP-Adresse + Port, an denen Postgres auf Verbindungen wartet; bei Streaming-Replikation müssen sie von anderen Clusterknoten aus erreichbar sein. Mehrere durch Kommas getrennte Adressen sind zulässig, sofern der Port nach der letzten Adresse mit einem Doppelpunkt angehängt wird, etwa `listen: 127.0.0.1,127.0.0.2:5432`. Patroni verwendet die erste Adresse dieser Liste, um lokale Verbindungen zum PostgreSQL-Knoten aufzubauen.

  - **use_unix_socket**: legt fest, dass Patroni für die Verbindung zum Cluster bevorzugt Unix-Sockets verwenden sollte. Standardwert: `false`. Ist `unix_socket_directories` definiert, verwendet Patroni daraus den ersten geeigneten Wert für die Verbindung zum Cluster und greift auf TCP zurück, wenn kein Wert geeignet ist. Ist `unix_socket_directories` nicht in `postgresql.parameters` angegeben, nimmt Patroni an, dass der Standardwert verwendet werden sollte, und lässt `host` in den Verbindungsparametern weg.

  - **use_unix_socket_repl**: legt fest, dass Patroni für die Clusterverbindung des Replikationsbenutzers bevorzugt Unix-Sockets verwenden sollte. Standardwert: `false`. Ist `unix_socket_directories` definiert, verwendet Patroni daraus den ersten geeigneten Wert für die Verbindung zum Cluster und greift auf TCP zurück, wenn kein Wert geeignet ist. Ist `unix_socket_directories` nicht in `postgresql.parameters` angegeben, nimmt Patroni an, dass der Standardwert verwendet werden sollte, und lässt `host` in den Verbindungsparametern weg.

  - **pgpass**: Pfad zur Passwortdatei [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni erstellt diese Datei vor dem Ausführen von pg_basebackup, des Skripts post_init und in einigen weiteren Fällen. Der Speicherort muss für Patroni beschreibbar sein.

  - **recovery_conf**: zusätzliche Konfigurationseinstellungen, die beim Konfigurieren eines Followers in recovery.conf geschrieben werden.

  - **custom_conf** : Pfad zu einer optionalen benutzerdefinierten Datei `postgresql.conf`, die anstelle von `postgresql.base.conf` verwendet wird. Sie muss auf allen Clusterknoten existieren, für PostgreSQL lesbar sein und wird von ihrem Speicherort aus in die tatsächliche `postgresql.conf` eingebunden. Patroni überwacht diese Datei weder auf Änderungen noch erstellt es ein Backup davon. Ihre Einstellungen können dennoch durch Patronis eigene Konfigurationsmöglichkeiten überschrieben werden; Einzelheiten stehen unter [Dynamische Konfiguration](/de/docs/patroni/config#config).

  - **parameters**: Konfigurationsparameter (GUCs) für Postgres im Format `{ssl: "on", ssl_cert_file: "cert_file"}`.
  - **parameters_primary**: (optional) rollenspezifische Parameterüberschreibungen für primary. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.
  - **parameters_replica**: (optional) rollenspezifische Parameterüberschreibungen für replica. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.
  - **parameters_standby_leader**: (optional) rollenspezifische Parameterüberschreibungen für standby_leader. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.

  - **pg_hba**: Liste der Zeilen, aus denen Patroni `pg_hba.conf` erzeugt. Patroni ignoriert diesen Parameter, wenn der PostgreSQL-Parameter `hba_file` auf einen anderen Wert als den Standardwert gesetzt ist. Zusammen mit der [dynamischen Konfiguration](/de/docs/patroni/config/dynamic#dynamic) vereinfacht dieser Parameter die Verwaltung von `pg_hba.conf`.

    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: Eine solche Zeile ist für die Replikation erforderlich.
  - **pg_hba_primary**: (optional) rollenspezifische pg_hba-Einträge für primary. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.
  - **pg_hba_replica**: (optional) rollenspezifische pg_hba-Einträge für replica. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.
  - **pg_hba_standby_leader**: (optional) rollenspezifische pg_hba-Einträge für standby_leader. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.

  - **pg_ident**: Liste der Zeilen, aus denen Patroni `pg_ident.conf` erzeugt. Patroni ignoriert diesen Parameter, wenn der PostgreSQL-Parameter `ident_file` auf einen anderen Wert als den Standardwert gesetzt ist. Zusammen mit der [dynamischen Konfiguration](/de/docs/patroni/config/dynamic#dynamic) vereinfacht dieser Parameter die Verwaltung von `pg_ident.conf`.

    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (optional) rollenspezifische pg_ident-Einträge für primary. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.
  - **pg_ident_replica**: (optional) rollenspezifische pg_ident-Einträge für replica. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.
  - **pg_ident_standby_leader**: (optional) rollenspezifische pg_ident-Einträge für standby_leader. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.

  - **pg_ctl_timeout**: Wartezeit für pg_ctl bei `start`, `stop` oder `restart`. Der Standardwert beträgt 60 Sekunden.

  - **use_pg_rewind**: versucht, pg_rewind auf dem bisherigen Leader zu verwenden, wenn er dem Cluster als Replikat beitritt. Der Cluster muss mit `data page checksums` (Option `--data-checksums` für `initdb`) initialisiert worden sein und/oder `wal_log_hints` muss auf `on` gesetzt sein, andernfalls funktioniert `pg_rewind` nicht.

  - **rewind**: (optional) benutzerdefinierte Optionen für den Befehl `pg_rewind`. Sie können als Liste von Zeichenfolgen und/oder Dictionaries mit jeweils einem Schlüssel-Wert-Paar angegeben werden. Zu den nicht zulässigen Optionen gehören: `target-pgdata`, `source-pgdata`, `source-server`, `write-recovery-conf`, `dry-run`, `restore-target-wal`, `config-file`, `no-ensure-shutdown`, `version` und `help`. Beispiel:

    ```yaml
    postgresql:
      rewind:
        - debug
        - progress
        - sync-method: fsync
    ```

  - **remove_data_directory_on_rewind_failure**: ist diese Option aktiviert, entfernt Patroni das PostgreSQL-Datenverzeichnis und erstellt das Replikat neu. Andernfalls versucht es, dem neuen Leader zu folgen. Standardwert: **false**.

  - **remove_data_directory_on_diverged_timelines**: Patroni entfernt das PostgreSQL-Datenverzeichnis und erstellt das Replikat neu, wenn es auseinanderlaufende Timelines erkennt und der bisherige Primärserver nicht mit dem Streaming vom neuen Primärserver beginnen kann. Diese Option ist nützlich, wenn `pg_rewind` nicht verwendet werden kann. Beim Prüfen auf auseinanderlaufende Timelines unter PostgreSQL v10 und älter versucht Patroni, sich mit den Replikationszugangsdaten zur Datenbank "postgres" zu verbinden. Daher sollte dieser Zugriff in pg_hba.conf erlaubt sein. Standardwert: **false**.

  - **replica_method**: für jeden Eintrag in create_replica_methods außer basebackup wird ein gleichnamiger Konfigurationsabschnitt hinzugefügt. Er sollte mindestens "command" mit dem vollständigen Pfad zum auszuführenden Skript enthalten. Andere Konfigurationsparameter werden im Format "parameter=value" an das Skript übergeben.

  - **pre_promote**: Fencing-Skript, das während eines Failovers nach dem Erwerb der Leader-Sperre, aber vor dem Hochstufen des Replikats ausgeführt wird. Endet das Skript mit einem von null verschiedenen Code, stuft Patroni das Replikat nicht hoch und entfernt den Leader-Schlüssel aus dem DCS.

  - **before_stop**: Skript, das unmittelbar vor dem Stoppen von Postgres ausgeführt wird. Anders als ein Callback läuft dieses Skript synchron und blockiert das Herunterfahren bis zu seinem Abschluss. Sein Rückgabecode beeinflusst nicht, ob das Herunterfahren anschließend fortgesetzt wird.

<a id="restapi_settings"></a>

--------

## REST API {#rest-api}

- **restapi**:
  - **thread_pool_size**: Größe des Threadpools, mit dem Patroni REST-API-Anfragen verarbeitet. Mindestwert: `5`, Standardwert: `5`.
  - **connect_address**: IP-Adresse (oder Hostname) und Port für den Zugriff auf die [REST API](/de/docs/patroni/rest_api#rest_api) von Patroni. Alle Clustermitglieder müssen diese Adresse erreichen können. Sofern die Patroni-Installation nicht als lokale Demo gedacht ist, darf daher weder "localhost" noch eine Loopback-Adresse (also "localhost" oder "127.0.0.1") verwendet werden. Die Adresse kann als Endpunkt für HTTP Health Checks (siehe unten den REST-API-Parameter "listen"), für Benutzerabfragen (direkt oder über die REST API) sowie für die Health Checks der Clustermitglieder während der Leader-Wahl dienen (etwa um festzustellen, ob der Leader noch läuft oder ob ein Knoten eine weiter fortgeschrittene WAL-Position hat als der abfragende Knoten). connect_address wird im Mitgliedsschlüssel im DCS gespeichert, sodass sich der Mitgliedsname in die Adresse für den Zugriff auf dessen REST API auflösen lässt.
  - **listen**: IP-Adresse (oder Hostname) und Port, an denen Patroni für die REST API auf Verbindungen wartet, um die oben beschriebenen Health Checks und die Kommunikation zwischen den beteiligten Clusterknoten bereitzustellen. Dient außerdem zum Bereitstellen von Health-Check-Informationen für HAProxy (oder jeden anderen Load-Balancer, der HTTP-Prüfungen mit "OPTIONS" oder "GET" ausführen kann).
  - **authentication**: (optional)
    - **username**: Benutzername für die Basic-Authentifizierung zum Schutz unsicherer REST-API-Endpunkte.
    - **password**: Passwort für die Basic-Authentifizierung zum Schutz unsicherer REST-API-Endpunkte.
  - **certfile**: (optional) gibt die Datei mit dem Zertifikat im PEM-Format an. Ist certfile nicht angegeben oder leer, arbeitet der API-Server ohne SSL.
  - **keyfile**: (optional) gibt die Datei mit dem geheimen Schlüssel im PEM-Format an.
  - **keyfile_password**: (optional) gibt ein Passwort zum Entschlüsseln der Schlüsseldatei an.
  - **cafile**: (optional) gibt die Datei mit dem CA_BUNDLE vertrauenswürdiger CA-Zertifikate an, die zum Prüfen der Clientzertifikate verwendet werden.
  - **ciphers**: (optional) gibt die zulässigen Cipher Suites an (z. B. "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
  - **verify_client**: (optional) `none` (Standard), `optional` oder `required`. Bei `none` prüft die REST API keine Clientzertifikate. Bei `required` sind Clientzertifikate für alle REST-API-Aufrufe erforderlich. Bei `optional` sind sie für alle unsicheren REST-API-Endpunkte erforderlich. Bei `required` ist die Clientauthentifizierung erfolgreich, wenn die Prüfung der Zertifikatssignatur erfolgreich ist. Bei `optional` wird das Clientzertifikat nur bei Anfragen mit `PUT`, `POST`, `PATCH` und `DELETE` geprüft.
  - **allowlist**: (optional): legt die Hosts fest, die unsichere REST-API-Endpunkte aufrufen dürfen. Ein Eintrag kann ein Hostname, eine IP-Adresse oder eine Netzwerkadresse in CIDR-Schreibweise sein. Standardmäßig gilt `allow all`. Ist `allowlist` oder `allowlist_include_members` gesetzt, werden alle nicht enthaltenen Zugriffe abgelehnt.
  - **allowlist_include_members**: (optional): bei `true` dürfen andere im DCS registrierte Clustermitglieder auf unsichere REST-API-Endpunkte zugreifen (IP-Adresse oder Hostname werden aus `api_url` des Mitglieds übernommen). Vorsicht: Das Betriebssystem kann für ausgehende Verbindungen eine andere IP-Adresse verwenden.
  - **http_extra_headers**: (optional) HTTP-Header ermöglichen es dem REST-API-Server, zusätzliche Informationen mit einer HTTP-Antwort zu übertragen.
  - **https_extra_headers**: (optional) HTTPS-Header ermöglichen es dem REST-API-Server, bei aktiviertem TLS zusätzliche Informationen mit einer HTTP-Antwort zu übertragen. Die in `http_extra_headers` festgelegten Zusatzinformationen werden ebenfalls übertragen.
  - **request_queue_size**: (optional): legt die Größe der Anfragewarteschlange für den TCP-Socket der Patroni REST API fest. Ist die Warteschlange voll, erhalten weitere Anfragen den Fehler "Connection denied". Der Standardwert ist 5.
  - **server_tokens**: (optional): konfiguriert den Wert des HTTP-Headers `Server`.
    - `Minimal`: Der Header enthält nur die Patroni-Version, etwa `Patroni/4.0.0`.
    - `ProductOnly`: Der Header enthält nur den Produktnamen, etwa `Patroni`.
    - `Original` (Standard): Der Header behält das ursprüngliche Verhalten bei und zeigt die Versionen von BaseHTTP und Python an, etwa `BaseHTTP/0.6 Python/3.12.3`.

Hier ein Beispiel für **http_extra_headers** und **https_extra_headers**:

```yaml
restapi:
  listen: <listen>
  connect_address: <connect_address>
  authentication:
    username: <username>
    password: <password>
  http_extra_headers:
    'X-Frame-Options': 'SAMEORIGIN'
    'X-XSS-Protection': '1; mode=block'
    'X-Content-Type-Options': 'nosniff'
  cafile: <ca file>
  certfile: <cert>
  keyfile: <key>
  https_extra_headers:
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
```

<div class="warning">

<div class="title">

Warnung

</div>

- `restapi.connect_address` muss von allen Knoten des jeweiligen Patroni-Clusters aus erreichbar sein. Intern verwendet Patroni diese Adresse während der Leader-Wahl, um die Knoten mit dem geringsten Replikationsrückstand zu ermitteln.
- Ist die Prüfung von Clientzertifikaten aktiviert (`restapi.verify_client` auf `required` gesetzt), **müssen** außerdem **gültige Clientzertifikate** in `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password` angegeben werden. Andernfalls funktioniert Patroni nicht korrekt.

</div>

<a id="patronictl_settings"></a>

--------

## CTL {#ctl}

- **ctl**: (optional)
  - **authentication**:
    - **username**: Benutzername für die Basic-Authentifizierung beim Zugriff auf geschützte REST-API-Endpunkte. Ohne Angabe verwendet [patronictl](/de/docs/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "username".
    - **password**: Passwort für die Basic-Authentifizierung beim Zugriff auf geschützte REST-API-Endpunkte. Ohne Angabe verwendet [patronictl](/de/docs/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "password".
  - **insecure**: erlaubt Verbindungen zur REST API ohne Prüfung der SSL-Zertifikate.
  - **cacert**: gibt die CA_BUNDLE-Datei oder das Verzeichnis mit Zertifikaten vertrauenswürdiger CAs an, die zum Prüfen der SSL-Zertifikate der REST API verwendet werden. Ohne Angabe verwendet [patronictl](/de/docs/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "cafile".
  - **certfile**: gibt die Datei mit dem Clientzertifikat im PEM-Format an.
  - **keyfile**: gibt die Datei mit dem geheimen Clientschlüssel im PEM-Format an.
  - **keyfile_password**: gibt ein Passwort zum Entschlüsseln der Clientschlüsseldatei an.

--------

## Watchdog {#watchdog}

- **mode**: `off`, `automatic` oder `required`. Bei `off` ist der Watchdog deaktiviert. Bei `automatic` wird er verwendet, falls verfügbar, andernfalls ignoriert. Bei `required` wird der Knoten nur dann Leader, wenn der Watchdog erfolgreich aktiviert werden kann.
- **device**: Pfad zum Watchdog-Gerät. Standardwert: `/dev/watchdog`.
- **safety_margin**: Sicherheitsabstand in Sekunden zwischen dem Auslösen des Watchdogs und dem Ablauf des Leader-Schlüssels.

<a id="tags_settings"></a>

--------

## Tags {#tags}

- **clonefrom**: `true` oder `false`. Bei `true` bevorzugen andere Knoten möglicherweise diesen Knoten zur Initialisierung (als Quelle für `pg_basebackup`). Haben mehrere Knoten das Tag `clonefrom` auf `true` gesetzt, wird die Quelle für die Initialisierung zufällig ausgewählt. Standardwert: `false`.
- **noloadbalance**: `true` oder `false`. Bei `true` antwortet der Knoten auf den REST-API-Health-Check `GET /replica` mit HTTP-Statuscode 503 und wird dadurch von der Lastverteilung ausgeschlossen. Standardwert: `false`.
- **replicatefrom**: Name eines anderen Replikats, von dem repliziert werden soll. Dient zur Unterstützung kaskadierender Replikation.
- **nosync**: `true` oder `false`. Bei `true` wird der Knoten niemals als synchrones Replikat ausgewählt.
- **sync_priority**: Ganzzahl, die die Priorität dieses Knotens bei der Auswahl synchroner Replikate bestimmt, wenn [synchronous_mode](/de/docs/patroni/replication_modes#synchronous_mode) auf `on` gesetzt ist. Knoten mit höherer Priorität werden gegenüber solchen mit niedrigerer Priorität bevorzugt. Ist `sync_priority` 0 oder negativ, darf dieser Knoten nicht in den PostgreSQL-Parameter `synchronous_standby_names` aufgenommen werden (wie bei `nosync: true`). Beachten Sie, dass dieser Parameter die entgegengesetzte Bedeutung zum Wert `sync_priority` in der Sicht `pg_stat_replication` hat.
- **nofailover**: `true` oder `false`; steuert, ob dieser Knoten an der Leader-Wahl teilnehmen und Leader werden darf. Standardwert: `false`, das heißt, dieser Knoten <span id="can">darf</span>\_ an Leader-Wahlen teilnehmen.
- **failover_priority**: Ganzzahl, die die Priorität dieses Knotens bei einem Failover bestimmt. Knoten mit höherer Priorität werden gegenüber solchen mit niedrigerer Priorität bevorzugt, wenn sie dieselbe Menge WAL empfangen beziehungsweise wiedergegeben haben. Knoten mit höherer Empfangs-/Wiedergabe-LSN werden jedoch unabhängig von ihrer Priorität bevorzugt. Ist `failover_priority` 0 oder negativ, darf dieser Knoten weder an der Leader-Wahl teilnehmen noch Leader werden (wie bei `nofailover: true`). Bekannte Einschränkung: `failover_priority` funktioniert derzeit nicht mit [Quorum-basierter synchroner Replikation](/de/docs/patroni/replication_modes#quorum_mode).
- **nostream**: `true` oder `false`. Bei `true` verwendet der Knoten nicht das Replikationsprotokoll zum Streamen von WAL. Stattdessen nutzt er Archiv-Recovery (falls `restore_command` konfiguriert ist) und fragt `pg_wal`/`pg_xlog` regelmäßig ab. Dies deaktiviert außerdem das Kopieren und Synchronisieren permanenter logischer Replikationsslots auf dem Knoten selbst und allen seinen kaskadierenden Replikaten. Auf einem Primärserver hat dieses Tag keine Wirkung.

> [!WARNING]
> Nur einen der Parameter `nofailover` oder `failover_priority` angeben. `nofailover: true` entspricht `failover_priority: 0`; `nofailover: false` gibt dem Knoten die Priorität 1.

Neben diesen vordefinierten Tags können auch eigene hinzugefügt werden:

- **key1**: `true`
- **key2**: `false`
- **key3**: `1.4`
- **key4**: `"RandomString"`

Tags sind in der [REST API](/de/docs/patroni/rest_api#rest_api) und in [patronictl_list](/de/docs/patroni/patronictl#patronictl_list) sichtbar. Mit diesen Tags lässt sich auch die Funktionsfähigkeit einer Instanz prüfen. Ist das Tag für eine Instanz nicht definiert oder stimmt sein Wert nicht mit dem abgefragten Wert überein, wird HTTP-Statuscode 503 zurückgegeben.
