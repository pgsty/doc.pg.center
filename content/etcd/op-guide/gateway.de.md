---
title: "etcd-Gateway"
weight: 4300
description: "Das etcd-Gateway: Einsatzgebiete und Einrichtung"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/gateway.md"
---

## Was ist das etcd-Gateway? {#what-is-etcd-gateway}

Das etcd-Gateway ist ein einfacher TCP-Proxy, der Netzwerkdaten an den etcd-Cluster weiterleitet. Es ist zustandslos und transparent: Es untersucht weder Clientanfragen noch greift es in Clusterantworten ein. Es terminiert keine TLS-Verbindungen, führt keine TLS-Handshakes im Namen seiner Clients durch und prüft nicht, ob eine Verbindung abgesichert ist.

Das Gateway unterstützt mehrere etcd-Serverendpunkte und verwendet ein einfaches Round-Robin-Verfahren. Es leitet nur an verfügbare Endpunkte weiter und verbirgt Ausfälle vor seinen Clients. Weitere Wiederholungsstrategien, etwa gewichtetes Round-Robin, können künftig unterstützt werden.

## Wann das etcd-Gateway sinnvoll ist {#when-to-use-etcd-gateway}

Jede Anwendung, die auf etcd zugreift, muss zunächst die Adresse eines Clientendpunkts des etcd-Clusters kennen. Greifen mehrere Anwendungen auf demselben Server auf denselben etcd-Cluster zu, muss trotzdem jede Anwendung dessen bekannt gegebene Clientendpunkte kennen. Wird der etcd-Cluster so umkonfiguriert, dass er andere Endpunkte hat, muss möglicherweise auch jede Anwendung ihre Endpunktliste aktualisieren. Diese umfassende Umkonfiguration ist aufwendig und fehleranfällig.

Das etcd-Gateway löst dieses Problem, indem es einen stabilen lokalen Endpunkt bereitstellt. In einer typischen Konfiguration läuft auf jedem Rechner ein Gateway, das auf einer lokalen Adresse lauscht; jede etcd-Anwendung verbindet sich mit ihrem lokalen Gateway. Dadurch muss nur das Gateway seine Endpunkte aktualisieren, statt jede einzelne Anwendung anzupassen.

Um Änderungen der Clusterendpunkte automatisch weiterzugeben, läuft das etcd-Gateway also auf jedem Rechner, auf dem mehrere Anwendungen auf denselben etcd-Cluster zugreifen.

## Wann das etcd-Gateway nicht sinnvoll ist {#when-not-to-use-etcd-gateway}

- Leistungssteigerung

Das Gateway ist nicht dafür ausgelegt, die Leistung eines etcd-Clusters zu verbessern. Es bietet weder Caching noch die Zusammenführung von Watches oder die Bündelung von Anfragen. Das etcd-Team entwickelt einen Caching-Proxy, der die Skalierbarkeit von Clustern verbessern soll.

- Betrieb auf einem Clusterverwaltungssystem

Fortgeschrittene Clusterverwaltungssysteme wie Kubernetes unterstützen Diensterkennung von Haus aus. Anwendungen können über einen DNS-Namen oder eine vom System verwaltete virtuelle IP-Adresse auf einen etcd-Cluster zugreifen. Beispielsweise entspricht kube-proxy dem etcd-Gateway.

## Das etcd-Gateway starten {#start-etcd-gateway}

Als Beispiel dient ein etcd-Cluster mit folgenden statischen Endpunkten:

|Name|Adresse|Hostname|Port|
|------|---------|------------------|----|
|infra0|10.0.1.10|infra0.example.com|2379|
|infra1|10.0.1.11|infra1.example.com|2379|
|infra2|10.0.1.12|infra2.example.com|2379|

Das etcd-Gateway mit folgendem Befehl für diese statischen Endpunkte starten:

```bash
$ etcd gateway start --endpoints=infra0.example.com:2379,infra1.example.com:2379,infra2.example.com:2379
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

Alternativ bei einer Diensterkennung über DNS die folgenden DNS-SRV-Einträge betrachten:

```bash
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```bash
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

Das etcd-Gateway mit folgendem Befehl starten, damit es die Endpunkte aus den DNS-SRV-Einträgen abruft:

```bash
$ etcd gateway start --discovery-srv=example.com
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

## Konfigurationsoptionen {#configuration-flags}

### etcd-Cluster {#etcd-cluster}

#### --endpoints {#endpoints}

 * Kommagetrennte Liste von etcd-Serverzielen, an die Clientverbindungen weitergeleitet werden.
 * Standard: `127.0.0.1:2379`
 * Der Port muss enthalten sein.
 * Ungültiges Beispiel: `https://127.0.0.1:2379` (das Gateway terminiert TLS nicht). Das Gateway prüft weder das HTTP-Schema noch die Anfragen; es leitet Anfragen lediglich an die angegebenen Endpunkte weiter.

#### --discovery-srv {#discovery-srv}

 * DNS-Domäne, über die Clusterendpunkte mithilfe von SRV-Einträgen initialisiert werden.
 * Standard: (nicht gesetzt)

### Netzwerk {#network}

#### --listen-addr {#listen-addr}

 * Schnittstelle und Port, an die gebunden wird, um Clientanfragen anzunehmen.
 * Standard: `127.0.0.1:23790`

#### --retry-delay {#retry-delay}

 * Wartezeit vor einem erneuten Verbindungsversuch zu ausgefallenen Endpunkten.
 * Standard: 1m0s
 * Ungültiges Beispiel: "123" (das Format erwartet eine Zeiteinheit)

### Sicherheit {#security}

#### --insecure-discovery {#insecure-discovery}

 * SRV-Einträge akzeptieren, die unsicher oder für Man-in-the-Middle-Angriffe anfällig sind.
 * Standard: `false`

#### --trusted-ca-file {#trusted-ca-file}

 * Pfad zur TLS-CA-Datei des Clients für den etcd-Cluster, um die bei der SRV-Erkennung zurückgegebenen Endpunkte zu überprüfen. Sie wird NUR zur Authentifizierung der gefundenen Endpunkte verwendet, nicht zum Aufbau von Verbindungen für die Datenübertragung. Das Gateway terminiert niemals TLS-Verbindungen und erstellt keine TLS-Verbindungen im Namen seiner Clients.
 * Standard: (nicht gesetzt)
