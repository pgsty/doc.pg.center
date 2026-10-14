---
title: "Umgebungskonfiguration"
linkTitle: "Umgebungskonfiguration"
weight: 30
icon: fa-solid fa-sliders
description: "Umgebungsvariablen zum Überschreiben der Patroni-Konfigurationsparameter."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
Einige in der Patroni-Konfigurationsdatei definierte Parameter können über Systemumgebungsvariablen überschrieben werden. Dieses Dokument listet alle von Patroni verarbeiteten Umgebungsvariablen auf. Die über diese Variablen gesetzten Werte haben stets Vorrang vor den Werten in der Patroni-Konfigurationsdatei.

--------

## Global/Allgemein {#globaluniversal}

- **PATRONI_CONFIGURATION**: die gesamte Patroni-Konfiguration kann über die Umgebungsvariable [PATRONI_CONFIGURATION](/de/patroni/config#config) festgelegt werden. In diesem Fall werden alle anderen Umgebungsvariablen ignoriert!
- **PATRONI_THREAD_POOL_SIZE**: Größe des Threadpools, mit dem Patroni asynchrone Aufgaben ausführt und während der Leader-Wahl oder bei Failsafe-Prüfungen über die REST API mit anderen Mitgliedern kommuniziert. Mindestwert: `5`, Standardwert: `5`.
- **PATRONI_THREAD_STACK_SIZE**: legt die Stackgröße für von Patroni gestartete Threads fest. Der Wert muss an `64kB` ausgerichtet sein. Mindestwert: `64kB`, Standardwert (von Patroni gesetzt): `512kB`.
- **PATRONI_NAME**: Name des Knotens, auf dem die aktuelle Patroni-Instanz läuft. Er muss im Cluster eindeutig sein.
- **PATRONI_NAMESPACE**: Pfad im Konfigurationsspeicher, unter dem Patroni Informationen über den Cluster speichert. Standardwert: "/service"
- **PATRONI_SCOPE**: Clustername
- **PG_MALLOC_ARENA_MAX**: benutzerdefinierter Wert für die Umgebungsvariable `MALLOC_ARENA_MAX` des Prozesses `postmaster`. Ist er nicht gesetzt, erbt `postmaster` den Wert von `MALLOC_ARENA_MAX`.

--------

## Protokollierung {#log}

- **PATRONI_LOG_TYPE**: legt das Protokollformat fest. Mögliche Werte sind **plain** und **json**. Für das Format **json** muss [jsonlogger](/de/patroni/installation#extras) installiert sein. Der Standardwert ist **plain**.
- **PATRONI_LOG_LEVEL**: legt die allgemeine Protokollierungsstufe fest. Standardwert: **INFO** (siehe [Dokumentation der Python-Protokollierung](https://docs.python.org/3.6/library/logging.html#levels))
- **PATRONI_LOG_TRACEBACK_LEVEL**: legt die Stufe fest, auf der Tracebacks sichtbar sind. Standardwert: **ERROR**. Auf **DEBUG** setzen, wenn Tracebacks nur bei aktiviertem **PATRONI_LOG_LEVEL=DEBUG** sichtbar sein sollen.
- **PATRONI_LOG_FORMAT**: legt die Formatzeichenfolge für Protokolle fest. Beim Protokolltyp **plain** sollte das Format eine Zeichenfolge sein. Verfügbare Attribute stehen unter [LogRecord-Attribute](https://docs.python.org/3.6/library/logging.html#logrecord-attributes). Beim Protokolltyp **json** kann das Format neben einer Zeichenfolge auch eine Liste sein. Jeder Listeneintrag sollte einem LogRecord-Attribut entsprechen. Dabei wird nur der Feldname benötigt; **%(** und **)** sollten weggelassen werden. Um ein Protokollfeld unter einem anderen Schlüsselnamen auszugeben, ein Dictionary verwenden: Der Schlüssel bezeichnet das Protokollfeld, der Wert den im Protokoll auszugebenden Feldnamen. Standardwert: **%(asctime)s %(levelname)s: %(message)s**
- **PATRONI_LOG_DATEFORMAT**: legt die Formatzeichenfolge für Datum und Uhrzeit fest (siehe [Dokumentation zu formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime)).
- **PATRONI_LOG_STATIC_FIELDS**: fügt dem Protokoll zusätzliche Felder hinzu. Diese Option ist nur beim Protokolltyp **json** verfügbar. Beispiel: `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE**: Patroni verwendet eine zweistufige Protokollierung. Protokolleinträge werden in eine Warteschlange im Arbeitsspeicher geschrieben; ein separater Thread entnimmt sie und schreibt sie nach stderr oder in eine Datei. Die interne Warteschlange ist standardmäßig auf **1000** Einträge begrenzt, was für die Protokolle der letzten 1h20m ausreicht.
- **PATRONI_LOG_DIR**: Verzeichnis für die Anwendungsprotokolle. Es muss existieren und für den Benutzer, der Patroni ausführt, beschreibbar sein. Ist diese Umgebungsvariable gesetzt, bewahrt die Anwendung standardmäßig 4 Protokolldateien mit jeweils 25MB auf. Diese Aufbewahrungswerte lassen sich mit `PATRONI_LOG_FILE_NUM` und `PATRONI_LOG_FILE_SIZE` anpassen (siehe unten).
- **PATRONI_LOG_MODE**: Berechtigungen für Protokolldateien (z. B. `0644`). Ohne Angabe werden die Berechtigungen anhand des aktuellen umask-Werts gesetzt.
- **PATRONI_LOG_FILE_NUM**: Anzahl der aufzubewahrenden Anwendungsprotokolle.
- **PATRONI_LOG_FILE_SIZE**: Größe der Datei patroni.log (in Bytes), bei der eine Protokollrotation ausgelöst wird.
- **PATRONI_LOG_LOGGERS**: definiert die Protokollierungsstufe je Python-Modul neu. Beispiel: `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS**: bei `true` werden aufeinanderfolgende identische Heartbeat-Protokolleinträge nicht ausgegeben. Standardwert: `false`.

> [!WARNING]
> Der Ausführungszeitpunkt der HA-Schleife kann bei der Diagnose von Failovers aufgrund erschöpfter Ressourcen und ähnlicher Probleme sehr wertvoll sein. Ist `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` auf `true` gesetzt, wird für die Ausführung der HA-Schleife kein Protokolleintrag erzeugt (außer bei einem Leader-Wechsel). Diese möglicherweise nützliche Information steht dann in den Protokollen nicht zur Verfügung.

--------

## Citus {#citus}

Aktiviert die Integration von Patroni mit [Citus](https://docs.citusdata.com). Ist sie konfiguriert, übernimmt Patroni die Registrierung der Citus-Worker-Knoten beim Coordinator. Weitere Informationen zur Citus-Unterstützung stehen [hier](/de/patroni/citus#citus).

- **PATRONI_CITUS_GROUP**: Citus-Gruppen-ID als Ganzzahl. Für den Coordinator `0` verwenden, für Worker `1`, `2` usw.
- **PATRONI_CITUS_DATABASE**: Datenbank, in der die Erweiterung [citus](/de/patroni/citus#citus) erstellt werden sollte. Sie muss auf dem Coordinator und allen Workern identisch sein. Derzeit wird nur eine Datenbank unterstützt.

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST**: host:port des lokalen Consul-Agenten.
- **PATRONI_CONSUL_URL**: URL des lokalen Consul-Agenten im Format: http(s)://host:port
- **PATRONI_CONSUL_PORT**: (optional) Consul-Port
- **PATRONI_CONSUL_SCHEME**: (optional) **http** oder **https**, Standardwert **http**
- **PATRONI_CONSUL_TOKEN**: (optional) ACL-Token
- **PATRONI_CONSUL_VERIFY**: (optional) bestimmt, ob das SSL-Zertifikat bei HTTPS-Anfragen geprüft wird
- **PATRONI_CONSUL_CACERT**: (optional) CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **PATRONI_CONSUL_CERT**: (optional) Datei mit dem Clientzertifikat
- **PATRONI_CONSUL_KEY**: (optional) Datei mit dem Clientschlüssel. Kann leer sein, wenn der Schlüssel Bestandteil des Zertifikats ist.
- **PATRONI_CONSUL_DC**: (optional) Rechenzentrum, mit dem kommuniziert werden soll. Standardmäßig wird das Rechenzentrum des Hosts verwendet.
- **PATRONI_CONSUL_CONSISTENCY**: (optional) wählt den Konsistenzmodus von Consul. Mögliche Werte: `default`, `consistent` oder `stale` (Einzelheiten in der [Consul-API-Referenz](https://www.consul.io/api/features/consistency.html/))
- **PATRONI_CONSUL_CHECKS**: (optional) Liste der für die Sitzung verwendeten Consul Health Checks. Standardmäßig wird eine leere Liste verwendet.
- **PATRONI_CONSUL_REGISTER_SERVICE**: (optional) bestimmt, ob ein Dienst registriert wird, dessen Name durch den Parameter scope festgelegt ist und der je nach Knotenrolle das Tag master, primary, replica oder standby-leader erhält. Standardwert **false**
- **PATRONI_CONSUL_SERVICE_TAGS**: (optional) zusätzliche statische Tags für den Consul-Dienst neben der Rolle (`primary`/`replica`/`standby-leader`). Standardmäßig wird eine leere Liste verwendet.
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL**: (optional) Häufigkeit der Health Checks für die registrierte URL
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME**: (optional) überschreibt den SNI-Host bei TLS-Verbindungen; siehe auch die [API-Referenz für Consul-Agent-Prüfungen](https://www.consul.io/api-docs/agent/check#tlsservername).

--------

## etcd {#etcd}

- **PATRONI_ETCD_PROXY**: Proxy-URL für etcd. Bei einer Verbindung zu etcd über einen Proxy diesen Parameter anstelle von **PATRONI_ETCD_URL** verwenden.
- **PATRONI_ETCD_URL**: URL für etcd im Format: http(s)://(username:password@)host:port
- **PATRONI_ETCD_HOSTS**: Liste der etcd-Endpunkte im Format 'host1:port1','host2:port2',etc...
- **PATRONI_ETCD_USE_PROXIES**: ist dieser Parameter auf true gesetzt, behandelt Patroni **hosts** als Liste von Proxys und ermittelt nicht die Topologie des etcd-Clusters, sondern bleibt bei der festen Liste **hosts**.
- **PATRONI_ETCD_PROTOCOL**: http oder https; ohne Angabe wird http verwendet. Ist **url** oder **proxy** angegeben, wird das Protokoll daraus übernommen.
- **PATRONI_ETCD_HOST**: host:port des etcd-Endpunkts.
- **PATRONI_ETCD_SRV**: Domain, in der nach SRV-Einträgen für die automatische Clustererkennung gesucht wird. Patroni fragt für die angegebene Domain diese SRV-Dienstnamen ab (in dieser Reihenfolge bis zum ersten Erfolg): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Werden SRV-Einträge für `_etcd-server-ssl` oder `_etcd-server` gefunden, wird über das ETCD-Peer-Protokoll bei ETCD nach verfügbaren Mitgliedern gefragt. Andernfalls werden die Hosts aus den SRV-Einträgen verwendet.
- **PATRONI_ETCD_SRV_SUFFIX**: konfiguriert ein Suffix für den bei der Erkennung abgefragten SRV-Namen. Mit diesem Flag lassen sich mehrere etcd-Cluster unter derselben Domain unterscheiden. Es funktioniert nur zusammen mit **PATRONI_ETCD_SRV**. Sind beispielsweise `PATRONI_ETCD_SRV_SUFFIX=foo` und `PATRONI_ETCD_SRV=example.org` gesetzt, wird folgende DNS-SRV-Abfrage ausgeführt: `_etcd-client-ssl-foo._tcp.example.org` (entsprechend für jeden möglichen ETCD-SRV-Dienstnamen).
- **PATRONI_ETCD_USERNAME**: Benutzername für die etcd-Authentifizierung.
- **PATRONI_ETCD_PASSWORD**: Passwort für die etcd-Authentifizierung.
- **PATRONI_ETCD_CACERT**: CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **PATRONI_ETCD_CERT**: Datei mit dem Clientzertifikat.
- **PATRONI_ETCD_KEY**: Datei mit dem Clientschlüssel. Kann leer sein, wenn der Schlüssel Bestandteil des Zertifikats ist.

--------

## Etcdv3 {#etcdv3}

Die Namen der Umgebungsvariablen für Etcdv3 entsprechen denen für etcd; im Variablennamen muss lediglich `ETCD` durch `ETCD3` ersetzt werden. Beispiele: `PATRONI_ETCD3_HOST`, `PATRONI_ETCD3_CACERT` usw.

> [!WARNING]
> Mit Protokollversion 2 erstellte Schlüssel sind mit Protokollversion 3 nicht sichtbar und umgekehrt. Daher ist ein Wechsel von etcd zu Etcdv3 allein durch Ändern der Patroni-Konfiguration nicht möglich. Zudem verwendet Patroni das gRPC-Gateway (Proxy) von etcd zur Kommunikation mit der V3 API, weshalb eine TLS-Authentifizierung über den Common Name nicht möglich ist.

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS**: durch Kommas getrennte Liste der ZooKeeper-Clustermitglieder: "'host1:port1','host2:port2','etc...'". Jeder einzelne Eintrag muss in Anführungszeichen stehen!
- **PATRONI_ZOOKEEPER_USE_SSL**: (optional) bestimmt, ob SSL verwendet wird. Standardwert: `false`. Bei `false` werden alle SSL-spezifischen Parameter ignoriert.
- **PATRONI_ZOOKEEPER_CACERT**: (optional) CA-Zertifikat. Falls vorhanden, wird die Validierung aktiviert.
- **PATRONI_ZOOKEEPER_CERT**: (optional) Datei mit dem Clientzertifikat.
- **PATRONI_ZOOKEEPER_KEY**: (optional) Datei mit dem Clientschlüssel.
- **PATRONI_ZOOKEEPER_KEY_PASSWORD**: (optional) Passwort für den Clientschlüssel.
- **PATRONI_ZOOKEEPER_VERIFY**: (optional) bestimmt, ob das Zertifikat geprüft wird. Standardwert: `true`.
- **PATRONI_ZOOKEEPER_SET_ACLS**: (optional) falls gesetzt, wird Kazoo so konfiguriert, dass es auf jeden neu erstellten ZNode eine Standard-ACL anwendet. ACLs können das Schema `x509` (Standard) oder andere unterstützte ZooKeeper-Schemata wie `digest` verwenden. Sie sollten als Dictionary angegeben werden, dessen Schlüssel der vollständige Principal (optional mit vorangestelltem Schema) und dessen Wert eine Liste von Berechtigungen ist. Als Berechtigungen sind eine oder mehrere aus `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN` oder `ALL` möglich. Beispiel: `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **PATRONI_ZOOKEEPER_AUTH_DATA**: (optional) Zugangsdaten für die Verbindung. Sollte ein Dictionary mit `scheme` als Schlüssel und `credential` als Wert sein. Standardwert ist ein leeres Dictionary.

> [!NOTE]
> Für SSL-Unterstützung muss `kazoo>=2.6.0` installiert sein.

--------

## Exhibitor {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS**: anfängliche Liste der Exhibitor-Knoten (ZooKeeper) im Format: 'host1,host2,etc...'. Diese Liste wird bei jeder Änderung der Topologie des Exhibitor-Clusters (ZooKeeper) automatisch aktualisiert.
- **PATRONI_EXHIBITOR_PORT**: Exhibitor-Port.

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE**: (optional) bei der Kommunikation mit der Kubernetes API verwendet Patroni normalerweise den Dienst [kubernetes](/de/patroni/kubernetes#kubernetes), dessen Adresse den Pods über die Umgebungsvariable `KUBERNETES_SERVICE_HOST` bereitgestellt wird. Ist `PATRONI_KUBERNETES_BYPASS_API_SERVICE` auf `true` gesetzt, ermittelt Patroni die Liste der API-Knoten hinter dem Dienst und verbindet sich direkt mit ihnen.
- **PATRONI_KUBERNETES_NAMESPACE**: (optional) Kubernetes-Namespace, in dem der Patroni-Pod läuft. Standardwert: `default`.
- **PATRONI_KUBERNETES_LABELS**: Labels im Format `{label1: value1, label2: value2}`. Mit diesen Labels werden vorhandene Objekte (Pods sowie Endpoints oder ConfigMaps) gesucht, die zum aktuellen Cluster gehören. Außerdem setzt Patroni sie auf jedem von ihm erstellten Objekt (Endpoint oder ConfigMap).
- **PATRONI_KUBERNETES_SCOPE_LABEL**: (optional) Name des Labels mit dem Clusternamen. Standardwert: `cluster-name`.
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS**: (optional) Labels im Format `{label1: value1, label2: value2}`. Sie werden einem Patroni-Pod zugewiesen, wenn sein Zustand `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` oder `creating replica` ist.
- **PATRONI_KUBERNETES_ROLE_LABEL**: (optional) Name des Labels mit der Rolle (`primary`, `replica` oder ein anderer benutzerdefinierter Wert). Patroni setzt dieses Label auf dem Pod, in dem es läuft. Standardwert: `role`.
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `primary` ist. Standardwert: `primary`.
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `replica` ist. Standardwert: `replica`.
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE**: (optional) Wert des Pod-Labels, wenn die Postgres-Rolle `standby_leader` ist. Standardwert: `primary`.
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL**: (optional) Name des temporären Labels mit der Rolle (`primary` oder `replica`). Der Wert dieses Labels entspricht immer dem Standardwert der jeweiligen Rolle. Nur bei Bedarf setzen.
- **PATRONI_KUBERNETES_USE_ENDPOINTS**: (optional) bei true verwendet Patroni Endpoints anstelle von ConfigMaps für die Leader-Wahl und zum Speichern des Clusterzustands.
- **PATRONI_KUBERNETES_POD_IP**: (optional) IP-Adresse des Pods, in dem Patroni läuft. Dieser Wert ist erforderlich, wenn `PATRONI_KUBERNETES_USE_ENDPOINTS` aktiviert ist, und wird beim Hochstufen von PostgreSQL im Pod zum Befüllen der Subsets des Leader-Endpoints verwendet.
- **PATRONI_KUBERNETES_PORTS**: (optional) enthält das Service-Objekt einen Namen für den Port, muss derselbe Name im Endpoint-Objekt erscheinen; andernfalls funktioniert der Dienst nicht. Ist der Dienst beispielsweise als `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}` definiert, muss `PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'` gesetzt werden. Patroni verwendet dies zum Aktualisieren der Subsets des Leader-Endpoints. Dieser Parameter wird nur verwendet, wenn `PATRONI_KUBERNETES_USE_ENDPOINTS` gesetzt ist.
- **PATRONI_KUBERNETES_CACERT**: (optional) gibt die CA_BUNDLE-Datei mit den Zertifikaten vertrauenswürdiger CAs an, die zum Prüfen der SSL-Zertifikate der Kubernetes API verwendet werden. Ohne Angabe verwendet Patroni den Wert aus dem ServiceAccount-Secret.
- **PATRONI_RETRIABLE_HTTP_CODES**: (optional) Liste der HTTP-Statuscodes der K8s API, bei denen ein erneuter Versuch erfolgt. Standardmäßig wiederholt Patroni die Anfrage bei `500`, `503` und `504` oder wenn die Antwort der K8s API den HTTP-Header `retry-after` enthält.

--------

## Raft (veraltet) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR**: `ip:port`, an dem auf Raft-Verbindungen gewartet wird. `self_addr` muss von anderen Clusterknoten aus erreichbar sein. Ohne Angabe nimmt der Knoten nicht am Konsens teil.
- **PATRONI_RAFT_BIND_ADDR**: (optional) `ip:port`, an dem auf Raft-Verbindungen gewartet wird. Ohne Angabe wird `self_addr` verwendet.
- **PATRONI_RAFT_PARTNER_ADDRS**: Liste der anderen Patroni-Knoten im Cluster im Format `"'ip1:port1','ip2:port2'"`. Jeder einzelne Eintrag muss in Anführungszeichen stehen!
- **PATRONI_RAFT_DATA_DIR**: Verzeichnis zum Speichern des Raft-Logs und des Snapshots. Ohne Angabe wird das aktuelle Arbeitsverzeichnis verwendet.
- **PATRONI_RAFT_PASSWORD**: (optional) verschlüsselt den Raft-Datenverkehr mit dem angegebenen Passwort; erfordert das Python-Modul `cryptography`.
- **PATRONI_RAFT_MIN_TIMEOUT**: (optional) minimale Zeitüberschreitung für Wahlen in der zugrunde liegenden Raft-Implementierung pysyncobj, in Sekunden. Muss größer als 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD` sein. Standardwert: `0.4`.
- **PATRONI_RAFT_MAX_TIMEOUT**: (optional) maximale Zeitüberschreitung für Wahlen in der zugrunde liegenden Raft-Implementierung pysyncobj, in Sekunden. Muss größer als `PATRONI_RAFT_MIN_TIMEOUT` sein. Standardwert: `1.4`.
- **PATRONI_RAFT_CONNECTION_TIMEOUT**: (optional) Zeit in Sekunden, nach der eine Verbindung ohne Datenempfang als unterbrochen gilt. Muss größer oder gleich `PATRONI_RAFT_MAX_TIMEOUT` sein. Standardwert: `3.5`.
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD**: (optional) Intervall in Sekunden zum Senden von Heartbeat-Befehlen. Muss kleiner als ein Drittel von `PATRONI_RAFT_MIN_TIMEOUT` sein. Standardwert: `0.1`.
- **PATRONI_RAFT_CONNECTION_RETRY_TIME**: (optional) Intervall in Sekunden zwischen erneuten Verbindungsversuchen zu nicht erreichbaren Knoten. Standardwert: `5.0`.
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT**: (optional) Zeit in Sekunden, nach der ein Leader ohne Antwort von der Mehrheit in den Follower-Zustand zurückkehrt. Muss größer als `PATRONI_RAFT_APPEND_ENTRIES_PERIOD` sein. Standardwert: `30.0`.

> [!NOTE]
> Patroni prüft diese Bedingungen beim Start und verweigert den Start, wenn sie verletzt sind. Diese Werte können nicht zur Laufzeit geändert werden und erfordern einen Neustart. Einzelheiten einschließlich der Einschränkungen bei hoher Latenz stehen unter [Raft-Einstellungen](/de/patroni/config/yaml#raft_settings).

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN**: IP-Adresse + Port, an denen Postgres auf Verbindungen wartet. Mehrere durch Kommas getrennte Adressen sind zulässig, sofern der Port nach der letzten Adresse mit einem Doppelpunkt angehängt wird, etwa `listen: 127.0.0.1,127.0.0.2:5432`. Patroni verwendet die erste Adresse dieser Liste, um lokale Verbindungen zum PostgreSQL-Knoten aufzubauen.
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS**: IP-Adresse + Port, über die Postgres für andere Knoten und Anwendungen erreichbar ist.
- **PATRONI_POSTGRESQL_PROXY_ADDRESS**: IP-Adresse + Port, über die ein neben Postgres laufender Verbindungspool (z. B. PgBouncer) erreichbar ist. Der Wert wird als `proxy_url` in den Mitgliedsschlüssel im DCS geschrieben und kann für die Diensterkennung verwendet werden beziehungsweise nützlich sein.
- **PATRONI_POSTGRESQL_DATA_DIR**: Pfad zum Postgres-Datenverzeichnis, das bereits existiert oder von Patroni initialisiert werden soll.
- **PATRONI_POSTGRESQL_CONFIG_DIR**: Pfad zum Postgres-Konfigurationsverzeichnis; standardmäßig das Datenverzeichnis. Es muss für Patroni beschreibbar sein.
- **PATRONI_POSTGRESQL_BIN_DIR**: Pfad zu den PostgreSQL-Programmdateien (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). Der Standardwert ist eine leere Zeichenfolge; dann werden die Programme über die Umgebungsvariable PATH gesucht.
- **PATRONI_POSTGRESQL_BIN_PG_CTL**: (optional) benutzerdefinierter Name für die Programmdatei `pg_ctl`.
- **PATRONI_POSTGRESQL_BIN_INITDB**: (optional) benutzerdefinierter Name für die Programmdatei `initdb`.
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA**: (optional) benutzerdefinierter Name für die Programmdatei `pg_controldata`.
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP**: (optional) benutzerdefinierter Name für die Programmdatei `pg_basebackup`.
- **PATRONI_POSTGRESQL_BIN_POSTGRES**: (optional) benutzerdefinierter Name für die Programmdatei `postgres`.
- **PATRONI_POSTGRESQL_BIN_IS_READY**: (optional) benutzerdefinierter Name für die Programmdatei `pg_isready`.
- **PATRONI_POSTGRESQL_BIN_PG_REWIND**: (optional) benutzerdefinierter Name für die Programmdatei `pg_rewind`.
- **PATRONI_POSTGRESQL_PGPASS**: Pfad zur Passwortdatei [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni erstellt diese Datei vor dem Ausführen von pg_basebackup und in einigen weiteren Fällen. Der Speicherort muss für Patroni beschreibbar sein.
- **PATRONI_REPLICATION_USERNAME**: Benutzername für die Replikation; der Benutzer wird bei der Initialisierung erstellt. Replikate verwenden ihn, um per Streaming-Replikation auf die Replikationsquelle zuzugreifen.
- **PATRONI_REPLICATION_PASSWORD**: Passwort für die Replikation; der Benutzer wird bei der Initialisierung erstellt.
- **PATRONI_REPLICATION_SSLMODE**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
- **PATRONI_REPLICATION_SSLKEY**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
- **PATRONI_REPLICATION_SSLPASSWORD**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `PATRONI_REPLICATION_SSLKEY` angegebenen geheimen Schlüssel festlegt.
- **PATRONI_REPLICATION_SSLCERT**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
- **PATRONI_REPLICATION_SSLROOTCERT**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
- **PATRONI_REPLICATION_SSLCRL**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_REPLICATION_SSLCRLDIR**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_REPLICATION_SSLNEGOTIATION**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
- **PATRONI_REPLICATION_GSSENCMODE**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
- **PATRONI_REPLICATION_CHANNEL_BINDING**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.
- **PATRONI_SUPERUSER_USERNAME**: Name des Superusers, der bei der Initialisierung (initdb) festgelegt und später von Patroni für Verbindungen zu Postgres verwendet wird. Auch pg_rewind verwendet diesen Benutzer.
- **PATRONI_SUPERUSER_PASSWORD**: Passwort des Superusers, das bei der Initialisierung (initdb) festgelegt wird.
- **PATRONI_SUPERUSER_SSLMODE**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
- **PATRONI_SUPERUSER_SSLKEY**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
- **PATRONI_SUPERUSER_SSLPASSWORD**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `PATRONI_SUPERUSER_SSLKEY` angegebenen geheimen Schlüssel festlegt.
- **PATRONI_SUPERUSER_SSLCERT**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
- **PATRONI_SUPERUSER_SSLROOTCERT**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
- **PATRONI_SUPERUSER_SSLCRL**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_SUPERUSER_SSLCRLDIR**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_SUPERUSER_SSLNEGOTIATION**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
- **PATRONI_SUPERUSER_GSSENCMODE**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
- **PATRONI_SUPERUSER_CHANNEL_BINDING**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.
- **PATRONI_REWIND_USERNAME**: (optional) Name des Benutzers für `pg_rewind`; er wird bei der Initialisierung von Postgres 11+ erstellt und erhält alle erforderlichen [Berechtigungen](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8).
- **PATRONI_REWIND_PASSWORD**: (optional) Passwort des Benutzers für `pg_rewind`; er wird bei der Initialisierung erstellt.
- **PATRONI_REWIND_SSLMODE**: (optional) entspricht dem Verbindungsparameter [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), der dem Client die Auswahl des Modus für die TLS-Aushandlung mit dem Server erlaubt. Einzelheiten zur Funktionsweise der einzelnen Modi stehen in der [PostgreSQL-Dokumentation](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Der Standardmodus ist `prefer`.
- **PATRONI_REWIND_SSLKEY**: (optional) entspricht dem Verbindungsparameter [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), der den Speicherort des geheimen Schlüssels für das Clientzertifikat angibt.
- **PATRONI_REWIND_SSLPASSWORD**: (optional) entspricht dem Verbindungsparameter [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), der das Passwort für den in `PATRONI_REWIND_SSLKEY` angegebenen geheimen Schlüssel festlegt.
- **PATRONI_REWIND_SSLCERT**: (optional) entspricht dem Verbindungsparameter [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), der den Speicherort des Clientzertifikats angibt.
- **PATRONI_REWIND_SSLROOTCERT**: (optional) entspricht dem Verbindungsparameter [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), der den Pfad zu einer Datei mit einem oder mehreren Zertifikaten von Zertifizierungsstellen (CA) angibt, mit denen der Client ein Serverzertifikat prüft.
- **PATRONI_REWIND_SSLCRL**: (optional) entspricht dem Verbindungsparameter [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), der den Pfad zu einer Datei mit einer Zertifikatsperrliste angibt. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_REWIND_SSLCRLDIR**: (optional) entspricht dem Verbindungsparameter [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), der den Pfad zu einem Verzeichnis mit Dateien angibt, die eine Zertifikatsperrliste enthalten. Ein Client lehnt Verbindungen zu Servern ab, deren Zertifikat in dieser Liste enthalten ist.
- **PATRONI_REWIND_SSLNEGOTIATION**: (optional) entspricht dem Verbindungsparameter [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), der steuert, wie die SSL-Verschlüsselung mit dem Server ausgehandelt wird, falls SSL verwendet wird.
- **PATRONI_REWIND_GSSENCMODE**: (optional) entspricht dem Verbindungsparameter [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), der bestimmt, ob und mit welcher Priorität eine sichere GSS-Verbindung über TCP/IP mit dem Server ausgehandelt wird.
- **PATRONI_REWIND_CHANNEL_BINDING**: (optional) entspricht dem Verbindungsparameter [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), der die Verwendung von Channel Binding durch den Client steuert.

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE**: Größe des Threadpools, mit dem Patroni REST-API-Anfragen verarbeitet. Mindestwert: `5`, Standardwert: `5`.
- **PATRONI_RESTAPI_CONNECT_ADDRESS**: IP-Adresse und Port für den Zugriff auf die REST API.
- **PATRONI_RESTAPI_LISTEN**: IP-Adresse und Port, an denen Patroni auf Verbindungen wartet, um Health-Check-Informationen für HAProxy bereitzustellen.
- **PATRONI_RESTAPI_USERNAME**: Benutzername für die Basic-Authentifizierung zum Schutz unsicherer REST-API-Endpunkte.
- **PATRONI_RESTAPI_PASSWORD**: Passwort für die Basic-Authentifizierung zum Schutz unsicherer REST-API-Endpunkte.
- **PATRONI_RESTAPI_CERTFILE**: gibt die Datei mit dem Zertifikat im PEM-Format an. Ist certfile nicht angegeben oder leer, arbeitet der API-Server ohne SSL.
- **PATRONI_RESTAPI_KEYFILE**: gibt die Datei mit dem geheimen Schlüssel im PEM-Format an.
- **PATRONI_RESTAPI_KEYFILE_PASSWORD**: gibt ein Passwort zum Entschlüsseln der Schlüsseldatei an.
- **PATRONI_RESTAPI_CAFILE**: gibt die Datei mit dem CA_BUNDLE vertrauenswürdiger CA-Zertifikate an, die zum Prüfen der Clientzertifikate verwendet werden.
- **PATRONI_RESTAPI_CIPHERS**: (optional) gibt die zulässigen Cipher Suites an (z. B. "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (Standard), `optional` oder `required`. Bei `none` prüft die REST API keine Clientzertifikate. Bei `required` sind Clientzertifikate für alle REST-API-Aufrufe erforderlich. Bei `optional` sind sie für alle unsicheren REST-API-Endpunkte erforderlich. Bei `required` ist die Clientauthentifizierung erfolgreich, wenn die Prüfung der Zertifikatssignatur erfolgreich ist. Bei `optional` wird das Clientzertifikat nur bei Anfragen mit `PUT`, `POST`, `PATCH` und `DELETE` geprüft.
- **PATRONI_RESTAPI_ALLOWLIST**: (optional): legt die Hosts fest, die unsichere REST-API-Endpunkte aufrufen dürfen. Ein Eintrag kann ein Hostname, eine IP-Adresse oder eine Netzwerkadresse in CIDR-Schreibweise sein. Standardmäßig gilt `allow all`. Ist `allowlist` oder `allowlist_include_members` gesetzt, werden alle nicht enthaltenen Zugriffe abgelehnt.
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS**: (optional): bei `true` dürfen andere im DCS registrierte Clustermitglieder auf unsichere REST-API-Endpunkte zugreifen (IP-Adresse oder Hostname werden aus `api_url` des Mitglieds übernommen). Vorsicht: Das Betriebssystem kann für ausgehende Verbindungen eine andere IP-Adresse verwenden.
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS**: (optional) HTTP-Header ermöglichen es dem REST-API-Server, zusätzliche Informationen mit einer HTTP-Antwort zu übertragen.
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS**: (optional) HTTPS-Header ermöglichen es dem REST-API-Server, bei aktiviertem TLS zusätzliche Informationen mit einer HTTP-Antwort zu übertragen. Die in `http_extra_headers` festgelegten Zusatzinformationen werden ebenfalls übertragen.
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE**: (optional): legt die Größe der Anfragewarteschlange für den TCP-Socket der Patroni REST API fest. Ist die Warteschlange voll, erhalten weitere Anfragen den Fehler "Connection denied". Der Standardwert ist 5.
- **PATRONI_RESTAPI_SERVER_TOKENS**: (optional) konfiguriert den Wert des HTTP-Headers `Server`. `Original` (Standard) behält das ursprüngliche Verhalten bei und zeigt die Versionen von BaseHTTP und Python an, etwa `BaseHTTP/0.6 Python/3.12.3`. `Minimal`: Der Header enthält nur die Patroni-Version, etwa `Patroni/4.0.0`. `ProductOnly`: Der Header enthält nur den Produktnamen, etwa `Patroni`.

<div class="warning">

<div class="title">

Warnung

</div>

- `PATRONI_RESTAPI_CONNECT_ADDRESS` muss von allen Knoten des jeweiligen Patroni-Clusters aus erreichbar sein. Intern verwendet Patroni diese Adresse während der Leader-Wahl, um die Knoten mit dem geringsten Replikationsrückstand zu ermitteln.
- Ist die Prüfung von Clientzertifikaten aktiviert (`PATRONI_RESTAPI_VERIFY_CLIENT` auf `required` gesetzt), **müssen** außerdem **gültige Clientzertifikate** in `PATRONI_CTL_CERTFILE`, `PATRONI_CTL_KEYFILE`, `PATRONI_CTL_KEYFILE_PASSWORD` angegeben werden. Andernfalls funktioniert Patroni nicht korrekt.

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE**: (optional) Pfad zur Konfigurationsdatei.
- **PATRONI_CTL_USERNAME**: (optional) Benutzername für die Basic-Authentifizierung beim Zugriff auf geschützte REST-API-Endpunkte. Ohne Angabe verwendet [patronictl](/de/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "username".
- **PATRONI_CTL_PASSWORD**: (optional) Passwort für die Basic-Authentifizierung beim Zugriff auf geschützte REST-API-Endpunkte. Ohne Angabe verwendet [patronictl](/de/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "password".
- **PATRONI_CTL_INSECURE**: (optional) erlaubt Verbindungen zur REST API ohne Prüfung der SSL-Zertifikate.
- **PATRONI_CTL_CACERT**: (optional) gibt die CA_BUNDLE-Datei oder das Verzeichnis mit Zertifikaten vertrauenswürdiger CAs an, die zum Prüfen der SSL-Zertifikate der REST API verwendet werden. Ohne Angabe verwendet [patronictl](/de/patroni/patronictl#patronictl) den Wert des REST-API-Parameters "cafile".
- **PATRONI_CTL_CERTFILE**: (optional) gibt die Datei mit dem Clientzertifikat im PEM-Format an.
- **PATRONI_CTL_KEYFILE**: (optional) gibt die Datei mit dem geheimen Clientschlüssel im PEM-Format an.
- **PATRONI_CTL_KEYFILE_PASSWORD**: (optional) gibt ein Passwort zum Entschlüsseln der Clientschlüsseldatei an.
