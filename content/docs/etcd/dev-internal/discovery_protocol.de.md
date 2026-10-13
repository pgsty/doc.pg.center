---
title: Protokoll des Discovery-Dienstes
weight: 1500
description: Andere etcd-Mitglieder während der Clusterinitialisierung finden
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
aliases: [/etcd/dev-internal/discovery_protocol/]
---

Das Protokoll des Discovery-Dienstes hilft einem neuen etcd-Mitglied, während der Clusterinitialisierung alle anderen Mitglieder über ein gemeinsames Discovery-Token und eine Endpunktliste zu finden.

Das Protokoll des Discovery-Dienstes wird _nur_ während der Clusterinitialisierung verwendet. Es kann nicht zur Neukonfiguration im laufenden Betrieb oder zur Clusterüberwachung genutzt werden.

Das Protokoll verwendet ein neues Discovery-Token, um einen _eindeutigen_ etcd-Cluster zu initialisieren. Ein Discovery-Token kann nur einen etcd-Cluster repräsentieren. Sobald das Discovery-Protokoll mit diesem Token startet, darf es nicht zur Initialisierung eines anderen etcd-Clusters verwendet werden, auch wenn der Vorgang auf halbem Weg fehlschlägt.

Der Rest dieses Artikels erläutert den Discovery-Ablauf anhand von Beispielen für einen selbst betriebenen Discovery-Cluster.

Dieses Dokument behandelt ausschließlich v3-Discovery. Einzelheiten zu [v2-Discovery][v2-discovery] enthält die frühere Dokumentation.

## Protokollablauf {#protocol-workflow}

Das Discovery-Protokoll nutzt einen internen etcd-Cluster, um die Initialisierung eines neuen Clusters zu koordinieren. Zuerst kommunizieren alle neuen Mitglieder mit dem Discovery-Dienst und helfen dabei, die erwartete Mitgliederliste zu erstellen. Anschließend initialisiert jedes neue Mitglied seinen Server anhand dieser Liste. Sie erfüllt dieselbe Funktion wie die Option -initial-cluster.

Im folgenden Beispielablauf wird jeder Protokollschritt zur Veranschaulichung mit einem `etcdctl`-Befehl dargestellt. Dabei wird angenommen, dass unter `http://example.com:2379` ein etcd-Cluster für den Discovery-Dienst läuft.

Das etcd-Discovery-Protokoll verwendet vereinbarungsgemäß das Schlüsselpräfix `/_etcd/registry`.


### Ein neues Discovery-Token erstellen {#creating-a-new-discovery-token}

Ein eindeutiges Token erzeugen, das den neuen Cluster identifiziert. In den folgenden Schritten dient es als eindeutiges Präfix im Discovery-Schlüsselraum. Mit `uuidgen` lässt es sich einfach erzeugen:

```
UUID=$(uuidgen)
```

### Die erwartete Clustergröße angeben {#specifying-the-expected-cluster-size}

Für das Discovery-Token muss eine Clustergröße angegeben werden. Anhand dieser Größe erkennt der Discovery-Dienst, wann er alle Mitglieder gefunden hat, die den Cluster anfänglich bilden sollen.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

Üblicherweise beträgt die Clustergröße 3, 5 oder 7. Weitere Einzelheiten enthält der Abschnitt zur [optimalen Clustergröße][cluster-size].

### etcd-Prozesse starten {#bringing-up-etcd-processes}

Das Discovery-Token `${UUID}` mit der Option `--discovery-token` und die Endpunkte des etcd-Clusters hinter dem Discovery-Dienst mit der Option `--discovery-endpoints` angeben. Damit wird v3-Discovery zur Initialisierung des etcd-Clusters aktiviert.

Wenn die Optionen `--discovery-token` und `--discovery-endpoints` angegeben sind, führt jeder etcd-Prozess intern die folgenden Schritte aus.

Wenn der Discovery-Dienst die Authentifizierung mit Client-Zertifikaten aktiviert hat, die folgenden Optionen konfigurieren. Ihre Verwendung entspricht genau der Verwendung von `etcdctl` zur Kommunikation mit einem etcd-Cluster.
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

Wenn der Discovery-Dienst rollenbasierte Authentifizierung aktiviert hat, die folgenden Optionen konfigurieren. Ihre Verwendung entspricht genau der Verwendung von `etcdctl` zur Kommunikation mit einem etcd-Cluster.
```
--discovery-user
--discovery-password
```

Die Standardwerte für Zeitintervalle und Zeitüberschreitungen können ebenfalls über die folgenden Optionen geändert werden. Ihre Verwendung entspricht genau der Verwendung von `etcdctl` zur Kommunikation mit einem etcd-Cluster.
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### Selbstregistrierung {#registering-itself}

Zuerst registriert sich jeder etcd-Prozess als Mitglied des angegebenen neuen Clusters. Dazu legt er seine Mitglieds-ID als Schlüssel unter dem vollständigen Registrierungsschlüssel an.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### Status prüfen {#checking-the-status}

Er prüft die erwartete Clustergröße und den Registrierungsstatus und entscheidet dann über den nächsten Schritt.

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

Wenn noch nicht genügend Mitglieder registriert sind, wartet er auf weitere Mitglieder.

Wenn die Anzahl registrierter Mitglieder die erwartete Größe N übersteigt, gelten die ersten N registrierten Mitglieder als Mitgliederliste des Clusters. Ist das Mitglied selbst in dieser Liste enthalten, ist der Discovery-Vorgang erfolgreich, und es ermittelt alle Peers anhand der Mitgliederliste. Ist es nicht enthalten, endet der Discovery-Vorgang mit der Fehlermeldung, dass der Cluster bereits voll ist.

Das Mitglied kann den Clusterstatus bereits vor seiner Registrierung prüfen. So kann es frühzeitig mit einem Fehler abbrechen, wenn der Cluster bereits voll ist.

### Auf alle Mitglieder warten {#waiting-for-all-members}

Der Wartevorgang beobachtet das Schlüsselpräfix `/_etcd/registry/${UUID}/members`, bis alle Mitglieder gefunden sind.

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
