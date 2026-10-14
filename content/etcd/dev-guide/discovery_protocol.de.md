---
title: Protokoll des Discovery-Dienstes
weight: 1500
description: Andere etcd-Mitglieder während der Clusterinitialisierung finden
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/discovery_protocol.md"
---

> [!NOTE]
> Diese Seite dokumentiert das ältere v2-Discovery-Protokoll, das in etcd 3.7 entfernt wurde. Für eine neue v3.7-Installation das [v3-Discovery-Protokoll](/de/etcd/dev-internal/discovery_protocol/) verwenden.

Das Protokoll des Discovery-Dienstes hilft einem neuen etcd-Mitglied, während der Clusterinitialisierung alle anderen Mitglieder über eine gemeinsame Discovery-URL zu finden.

Das Protokoll des Discovery-Dienstes wird _nur_ während der Clusterinitialisierung verwendet. Es kann nicht zur Neukonfiguration im laufenden Betrieb oder zur Clusterüberwachung genutzt werden.

Das Protokoll verwendet ein neues Discovery-Token, um einen _eindeutigen_ etcd-Cluster zu initialisieren. Ein Discovery-Token kann nur einen etcd-Cluster repräsentieren. Sobald das Discovery-Protokoll mit diesem Token startet, darf es nicht zur Initialisierung eines anderen etcd-Clusters verwendet werden, auch wenn der Vorgang auf halbem Weg fehlschlägt.

Der Rest dieses Artikels erläutert den Discovery-Ablauf anhand von Beispielen für einen selbst betriebenen Discovery-Cluster. Der öffentliche Discovery-Dienst discovery.etcd.io funktioniert ebenso, bietet jedoch eine zusätzliche Schicht, die unübersichtliche URLs verbirgt, UUIDs automatisch erzeugt und einen gewissen Schutz vor übermäßig vielen Anfragen bietet. Im Kern verwendet auch der öffentliche Discovery-Dienst einen etcd-Cluster als Datenspeicher, wie in diesem Dokument beschrieben.

## Protokollablauf {#protocol-workflow}

Das Discovery-Protokoll nutzt einen internen etcd-Cluster, um die Initialisierung eines neuen Clusters zu koordinieren. Zuerst kommunizieren alle neuen Mitglieder mit dem Discovery-Dienst und helfen dabei, die erwartete Mitgliederliste zu erstellen. Anschließend initialisiert jedes neue Mitglied seinen Server anhand dieser Liste. Sie erfüllt dieselbe Funktion wie die Option -initial-cluster.

Im folgenden Beispielablauf wird jeder Protokollschritt zur Veranschaulichung im curl-Format dargestellt.

Das etcd-Discovery-Protokoll verwendet vereinbarungsgemäß das Schlüsselpräfix `_etcd/registry`. Wenn unter `http://example.com` ein etcd-Cluster für den Discovery-Dienst läuft, lautet die vollständige URL zum Discovery-Schlüsselraum `http://example.com/v2/keys/_etcd/registry`. Sie wird im Beispiel als URL-Präfix verwendet.

### Ein neues Discovery-Token erstellen {#creating-a-new-discovery-token}

Ein eindeutiges Token erzeugen, das den neuen Cluster identifiziert. In den folgenden Schritten dient es als eindeutiges Präfix im Discovery-Schlüsselraum. Mit `uuidgen` lässt es sich einfach erzeugen:

```
UUID=$(uuidgen)
```

### Die erwartete Clustergröße angeben {#specifying-the-expected-cluster-size}

Für das Discovery-Token muss eine Clustergröße angegeben werden. Anhand dieser Größe erkennt der Discovery-Dienst, wann er alle Mitglieder gefunden hat, die den Cluster anfänglich bilden sollen.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size -d value=${cluster_size}
```

Üblicherweise beträgt die Clustergröße 3, 5 oder 7. Weitere Einzelheiten enthält der Abschnitt zur [optimalen Clustergröße][cluster-size].

### etcd-Prozesse starten {#bringing-up-etcd-processes}

Die Discovery-URL mit der Option `-discovery` angeben und die etcd-Prozesse starten. Jeder etcd-Prozess führt intern die folgenden Schritte aus, wenn die Option `-discovery` angegeben ist.

### Selbstregistrierung {#registering-itself}

Zuerst registriert sich der etcd-Prozess unter der Discovery-URL als Mitglied. Dazu legt er die Mitglieds-ID als Schlüssel unter der Discovery-URL an.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/${member_id}?prevExist=false -d value="${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}"
```

### Status prüfen {#checking-the-status}

Er prüft die erwartete Clustergröße und den Registrierungsstatus unter der Discovery-URL und entscheidet dann über den nächsten Schritt.

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}
```

Wenn noch nicht genügend Mitglieder registriert sind, wartet er auf die übrigen Mitglieder.

Wenn die Anzahl registrierter Mitglieder die erwartete Größe N übersteigt, gelten die ersten N registrierten Mitglieder als Mitgliederliste des Clusters. Ist das Mitglied selbst in dieser Liste enthalten, ist der Discovery-Vorgang erfolgreich, und es ermittelt alle Peers anhand der Mitgliederliste. Ist es nicht enthalten, endet der Discovery-Vorgang mit der Fehlermeldung, dass der Cluster bereits voll ist.

In der etcd-Implementierung kann das Mitglied den Clusterstatus bereits vor seiner Registrierung prüfen. So kann es frühzeitig mit einem Fehler abbrechen, wenn der Cluster bereits voll ist.

### Auf alle Mitglieder warten {#waiting-for-all-members}

Der Wartevorgang ist in der [etcd-API-Dokumentation][api] ausführlich beschrieben.

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}?wait=true&waitIndex=${current_etcd_index}
```

Er wartet, bis alle Mitglieder gefunden sind.

## Öffentlicher Discovery-Dienst {#public-discovery-service}

CoreOS Inc. betreibt unter https://discovery.etcd.io/ einen öffentlichen Discovery-Dienst mit einigen Funktionen, die die Nutzung erleichtern.

### Schlüsselpräfix verbergen {#mask-key-prefix}

Der öffentliche Discovery-Dienst leitet `https://discovery.etcd.io/${UUID}` zum dahinterliegenden etcd-Cluster auf den Schlüssel unter `/v2/keys/_etcd/registry` um. Er verbirgt das Registrierungsschlüsselpräfix, damit die Discovery-URL kurz und lesbar bleibt.

### Neues Token abrufen {#get-new-token}

```
GET /new

Sent query:
	size=${cluster_size}
Possible status codes:
	200 OK
	400 Bad Request
200 Body:
	generated discovery url
```

Der Erzeugungsvorgang im Dienst folgt den Schritten von [Ein neues Discovery-Token erstellen][new-discovery-token] bis [Die erwartete Clustergröße angeben][expected-cluster-size].

### Discovery-Status prüfen {#check-discovery-status}

```
GET /${UUID}
```

Der Status dieses Discovery-Tokens einschließlich der registrierten Rechner lässt sich durch Abfragen des Werts der UUID prüfen.

### Open-Source-Repository {#open-source-repository}

Das Repository befindet sich unter https://github.com/coreos/discovery.etcd.io. Damit lässt sich ein eigener Discovery-Dienst erstellen.

[api]: https://etcd.io/docs/v2.3/api#waiting-for-a-change
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
