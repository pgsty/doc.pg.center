---
title: "Anleitung zur Clusterbildung"
weight: 4150
description: "Einen etcd-Cluster initialisieren: statisch, mit etcd-Erkennung oder mit DNS-Erkennung"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/clustering.md"
---

## Überblick {#overview}

Der statische Start eines etcd-Clusters setzt voraus, dass jedes Mitglied ein anderes Mitglied des Clusters kennt. In manchen Fällen sind die IP-Adressen der Clustermitglieder im Voraus noch nicht bekannt. Dann lässt sich der etcd-Cluster mithilfe eines Erkennungsdiensts initialisieren.

Sobald ein etcd-Cluster läuft, werden Mitglieder über die [Laufzeitrekonfiguration][runtime-conf] hinzugefügt oder entfernt. Für ein besseres Verständnis des zugrunde liegenden Entwurfs empfehlen wir das [Entwurfsdokument zur Laufzeitkonfiguration][runtime-reconf-design].

Diese Anleitung behandelt folgende Verfahren zur Initialisierung eines etcd-Clusters:

* [Statisch](#static)
* [etcd-Erkennung](#etcd-discovery)
* [DNS-Erkennung](#dns-discovery)

Mit jedem Verfahren wird ein etcd-Cluster aus drei Rechnern mit folgenden Eigenschaften erstellt:

|Name|Adresse|Hostname|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## Statisch {#static}

Da Mitglieder, Adressen und Größe des Clusters vor dem Start bekannt sind, lässt sich mit der Option `initial-cluster` eine Offline-Konfiguration zur Initialisierung verwenden. Auf jedem Rechner werden entweder die folgenden Umgebungsvariablen oder Befehlszeilenoptionen gesetzt:

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

Die in `initial-cluster` angegebenen URLs sind die _bekannt gegebenen Peer-URLs_. Sie sollten also dem Wert von `initial-advertise-peer-urls` auf den jeweiligen Knoten entsprechen.

Werden zu Testzwecken mehrere Cluster mit derselben Konfiguration gestartet oder ein einzelner Cluster wiederholt erstellt und gelöscht, wird dringend empfohlen, jedem Cluster einen eindeutigen `initial-cluster-token` zuzuweisen. Dadurch kann etcd eindeutige Cluster- und Mitglieds-IDs erzeugen, selbst wenn die Konfigurationen ansonsten exakt übereinstimmen. Dies kann etcd vor Wechselwirkungen zwischen Clustern schützen, die diese beschädigen könnten.

etcd lauscht auf [`listen-client-urls`][conf-listen-client], um Clientverkehr anzunehmen. Ein etcd-Mitglied gibt die unter [`advertise-client-urls`][conf-adv-client] angegebenen URLs an andere Mitglieder, Proxys und Clients weiter. Sicherstellen, dass die vorgesehenen Clients die `advertise-client-urls` erreichen können. Ein häufiger Fehler ist, `advertise-client-urls` auf localhost zu setzen oder den Standardwert beizubehalten, obwohl entfernte Clients etcd erreichen sollen.

Auf jedem Rechner etcd mit diesen Optionen starten:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

Die mit `--initial-cluster` beginnenden Befehlszeilenparameter werden bei späteren Starts von etcd ignoriert. Nach der Erstinitialisierung können die Umgebungsvariablen oder Befehlszeilenoptionen entfernt werden. Muss die Konfiguration später geändert werden, etwa um Mitglieder hinzuzufügen oder zu entfernen, hilft die Anleitung zur [Laufzeitkonfiguration][runtime-conf].

### TLS {#tls}

etcd unterstützt verschlüsselte Kommunikation über das TLS-Protokoll. TLS-Kanäle können sowohl den internen Clusterverkehr zwischen Peers als auch den Clientverkehr verschlüsseln. Dieser Abschnitt zeigt Beispiele zur Einrichtung eines Clusters mit TLS für Peers und Clients. Weitere Einzelheiten zur TLS-Unterstützung von etcd enthält die [Sicherheitsanleitung][security-guide].

#### Selbstsignierte Zertifikate {#self-signed-certificates}

Ein Cluster mit selbstsignierten Zertifikaten verschlüsselt den Verkehr und authentifiziert seine Verbindungen. Für den Start eines solchen Clusters sollte jedes Mitglied ein eigenes Schlüsselpaar (`member.crt`, `member.key`) besitzen, das von einem gemeinsamen CA-Zertifikat des Clusters (`ca.crt`) signiert wurde, sowohl für Peer- als auch für Clientverbindungen. Zertifikate können nach dem etcd-Beispiel zur [TLS-Einrichtung][tls-setup] erzeugt werden.

Auf jedem Rechner würde etcd mit diesen Optionen gestartet:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### Automatisch erzeugte Zertifikate {#automatic-certificates}

Benötigt der Cluster verschlüsselte Kommunikation, aber keine authentifizierten Verbindungen, kann etcd so konfiguriert werden, dass es seine Schlüssel automatisch erzeugt. Bei der Initialisierung erstellt jedes Mitglied eigene Schlüssel anhand seiner bekannt gegebenen IP-Adressen und Hosts.

Auf jedem Rechner würde etcd mit diesen Optionen gestartet:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### Fehlerfälle {#error-cases}

Im folgenden Beispiel fehlt der neue Host in der Liste der aufgeführten Knoten. Handelt es sich um einen neuen Cluster, _muss_ der Knoten zur Liste der anfänglichen Clustermitglieder hinzugefügt werden.

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

In diesem Beispiel soll ein Knoten (infra0) einer anderen Adresse (127.0.0.1:2380) zugeordnet werden als der in der Clusterliste aufgeführten (10.0.1.10:2380). Soll dieser Knoten auf mehreren Adressen lauschen, _müssen_ alle Adressen in der Konfigurationsanweisung "initial-cluster" enthalten sein.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

Ist ein Peer mit anderen Konfigurationsargumenten eingerichtet und versucht, diesem Cluster beizutreten, meldet etcd eine abweichende Cluster-ID und beendet sich.

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## Erkennung {#discovery}

In manchen Fällen sind die IP-Adressen der Cluster-Peers im Voraus noch nicht bekannt. Dies ist bei Cloud-Anbietern oder Netzwerken mit DHCP üblich. Dann wird anstelle einer statischen Konfiguration ein bestehender etcd-Cluster verwendet, um einen neuen zu initialisieren. Dieser Vorgang heißt „Erkennung“ (Discovery).

Für die Erkennung stehen zwei Verfahren zur Verfügung:

* etcd-Erkennungsdienst
* DNS-SRV-Einträge

### etcd-Erkennung {#etcd-discovery}

> [!NOTE]
> Die Beispiele für den Erkennungsdienst in diesem Abschnitt beschreiben das ältere v2-Protokoll, das in etcd 3.7 entfernt wurde. Für einen neuen v3.7-Cluster [v3-Discovery](/de/etcd/dev-internal/discovery_protocol/) oder die statische Initialisierung bzw. DNS-SRV-Verfahren in dieser Anleitung verwenden.

Für ein besseres Verständnis des Protokollentwurfs empfehlen wir die [Dokumentation][discovery-proto] zum Protokoll des Erkennungsdiensts.

#### Lebensdauer einer Erkennungs-URL {#lifetime-of-a-discovery-url}

Eine Erkennungs-URL identifiziert einen eindeutigen etcd-Cluster. Für die Initialisierung eines neuen Clusters verwenden alle etcd-Instanzen gemeinsam eine neue Erkennungs-URL, statt eine vorhandene wiederzuverwenden.

Erkennungs-URLs sollten außerdem NUR für die Erstinitialisierung eines Clusters verwendet werden. Wie die Mitgliedschaft eines bereits laufenden Clusters geändert wird, beschreibt die Anleitung zur [Laufzeitrekonfiguration][runtime-conf].

#### Eigener etcd-Erkennungsdienst {#custom-etcd-discovery-service}

Die Erkennung verwendet einen vorhandenen Cluster zur Initialisierung. Bei Verwendung eines privaten etcd-Clusters eine URL wie folgt erstellen:

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

Durch Setzen des Schlüssels size unter der URL wird eine Erkennungs-URL mit der erwarteten Clustergröße 3 erstellt.

In diesem Fall lautet die zu verwendende URL `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`. Die etcd-Mitglieder verwenden beim Start das Verzeichnis `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` zur Registrierung.

**Für jedes Mitglied muss die Namensoption einen anderen Wert angeben. `Hostname` oder `machine-id` können eine gute Wahl sein. Andernfalls scheitert die Erkennung an doppelten Namen.**

Nun etcd für jedes Mitglied mit den entsprechenden Optionen starten:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

Dadurch registriert sich jedes Mitglied beim eigenen etcd-Erkennungsdienst. Sobald alle Rechner registriert sind, startet der Cluster.

#### Öffentlicher etcd-Erkennungsdienst {#public-etcd-discovery-service}

Ist kein bestehender Cluster verfügbar, den öffentlichen Erkennungsdienst unter `discovery.etcd.io` verwenden. Mit folgendem Befehl über den Endpunkt "new" eine private Erkennungs-URL erstellen:

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Dies erstellt den Cluster mit einer anfänglichen Größe von 3 Mitgliedern. Wird keine Größe angegeben, gilt der Standardwert 3.

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**Für jedes Mitglied muss die Namensoption einen anderen Wert angeben, andernfalls scheitert die Erkennung an doppelten Namen. `Hostname` oder `machine-id` können eine gute Wahl sein.**

Nun etcd für jedes Mitglied mit den entsprechenden Optionen starten:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Dadurch registriert sich jedes Mitglied beim Erkennungsdienst. Sobald alle Mitglieder registriert sind, startet der Cluster.

Mit der Umgebungsvariablen `ETCD_DISCOVERY_PROXY` lässt sich etcd anweisen, einen HTTP-Proxy für die Verbindung zum Erkennungsdienst zu verwenden.

#### Fehler- und Warnfälle {#error-and-warning-cases}

##### Fehler des Erkennungsservers {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### Warnungen {#warnings}

Diese harmlose Warnung zeigt an, dass die Erkennungs-URL auf diesem Rechner ignoriert wird.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### DNS-Erkennung {#dns-discovery}

DNS-[SRV-Einträge][rfc-srv] können als Erkennungsverfahren verwendet werden.
Mit der Option `--discovery-srv` lässt sich die DNS-Domäne festlegen, unter der die SRV-Einträge für die Erkennung liegen.
Mit `--discovery-srv example.com` werden DNS-SRV-Einträge in der angegebenen Reihenfolge gesucht:

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

Wird `_etcd-server-ssl._tcp.example.com` gefunden, versucht etcd die Initialisierung über TLS.

Damit Clients den etcd-Cluster finden, werden folgende DNS-SRV-Einträge in der angegebenen Reihenfolge gesucht:

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

Wird `_etcd-client-ssl._tcp.example.com` gefunden, versuchen Clients, über SSL/TLS mit dem etcd-Cluster zu kommunizieren.

Verwendet etcd TLS, muss der SRV-Eintrag für die Erkennung (z. B. `example.com`) zusammen mit dem Hostnamen im DNS-SAN des SSL-Zertifikats enthalten sein. Andernfalls scheitert die Clusterbildung mit Protokollmeldungen wie dieser:

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

Verwendet etcd TLS ohne eine eigene Zertifizierungsstelle, muss die Erkennungsdomäne (z. B. example.com) zur Domäne des SRV-Eintrags (z. B. infra1.example.com) passen. Dies erschwert Angriffe mit gefälschten SRV-Einträgen, die auf eine andere Domäne verweisen. Diese Domäne könnte zwar ein gültiges PKI-Zertifikat besitzen, aber von einem unbekannten Dritten kontrolliert werden.

Die Option `-discovery-srv-name` legt zusätzlich ein Suffix für den während der Erkennung abgefragten SRV-Namen fest.
Mit ihr lassen sich mehrere etcd-Cluster unter derselben Domäne unterscheiden.
Sind beispielsweise `discovery-srv=example.com` und `-discovery-srv-name=foo` gesetzt, werden folgende DNS-SRV-Abfragen gestellt:

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### DNS-SRV-Einträge erstellen {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### Den etcd-Cluster über DNS initialisieren {#bootstrap-the-etcd-cluster-using-dns}

etcd-Clustermitglieder können Domänennamen oder IP-Adressen bekannt geben; die Initialisierung löst DNS-A-Einträge auf.
Seit 3.2 lehnen `--listen-peer-urls` und `--listen-client-urls` Domänennamen für die Bindung an Netzwerkschnittstellen ab (3.1 gibt Warnungen aus).

Die aufgelöste Adresse in `--initial-advertise-peer-urls` *muss mit einer der aufgelösten Adressen der SRV-Ziele übereinstimmen*. Das etcd-Mitglied liest die aufgelöste Adresse, um festzustellen, ob es zu dem in den SRV-Einträgen definierten Cluster gehört.

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

Der Cluster kann auch mit IP-Adressen anstelle von Domänennamen initialisiert werden:

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

Seit v3.1.0 (außer v3.2.9) authentifiziert der Server bei TLS-Konfiguration von `etcd --discovery-srv=example.com` Peers und Clients nur dann, wenn die angegebenen Zertifikate die Stammdomäne `example.com` als Eintrag im Feld Subject Alternative Name (SAN) enthalten. Siehe [Hinweise zu DNS SRV][security-guide-dns-srv].

### Gateway {#gateway}

Das etcd-Gateway ist ein einfacher TCP-Proxy, der Netzwerkdaten an den etcd-Cluster weiterleitet. Weitere Informationen bietet die [Gateway-Anleitung][gateway].

### Proxy {#proxy}

Frühere etcd-Versionen unterstützten über `--proxy` einen [Proxymodus][proxy] nur für v2. Dieser Modus wurde entfernt und kann mit etcd 3.7 nicht verwendet werden. Für die v3-API den [gRPC-Proxy](/de/etcd/op-guide/grpc_proxy/) verwenden.

Historische v2-Proxy-Installationen beschreibt die [Clusterdokumentation der etcd-Version 2.3][clustering_etcd2].

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /de/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /de/etcd/op-guide/configuration/#member
[discovery-proto]: /de/etcd/dev-internal/discovery_protocol/
[gateway]: /de/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /de/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /de/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /de/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /de/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
