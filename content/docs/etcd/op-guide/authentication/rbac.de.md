---
title: "Rollenbasierte Zugriffskontrolle"
weight: 4100
description: "Eine grundlegende Anleitung zur Authentifizierung und rollenbasierten Zugriffskontrolle"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/authentication/rbac.md"
aliases: [/etcd/op-guide/authentication/rbac/]
---

## Überblick {#overview}

Die Authentifizierung wurde in etcd 2.1 eingeführt. Die etcd-v3-API hat die API und die Benutzeroberfläche der Authentifizierungsfunktion geringfügig angepasst, um dem neuen Datenmodell besser gerecht zu werden. Diese Anleitung hilft dabei, eine grundlegende Authentifizierung und rollenbasierte Zugriffskontrolle in etcd v3 einzurichten.

## Besondere Benutzer und Rollen {#special-users-and-roles}

Es gibt einen besonderen Benutzer, `root`, und eine besondere Rolle, `root`.

### Benutzer `root` {#user-root}

Der Benutzer `root`, der uneingeschränkten Zugriff auf etcd hat, muss vor der Aktivierung der Authentifizierung angelegt werden. Der Benutzer `root` ist für Verwaltungsaufgaben vorgesehen: die Verwaltung von Rollen und gewöhnlichen Benutzern. Der Benutzer `root` muss die Rolle `root` haben und darf alles in etcd ändern.

### Rolle `root` {#role-root}

Die Rolle `root` kann neben dem root-Benutzer jedem Benutzer zugewiesen werden. Ein Benutzer mit der Rolle `root` hat sowohl globalen Lese- und Schreibzugriff als auch die Berechtigung, die Authentifizierungskonfiguration des Clusters zu ändern. Darüber hinaus gewährt die Rolle `root` Rechte für die allgemeine Clusterwartung, einschließlich der Änderung der Clustermitgliedschaft, der Defragmentierung des Speichers und der Erstellung von Snapshots.

## Benutzer verwalten {#working-with-users}

Der Unterbefehl `user` von `etcdctl` übernimmt alle Aufgaben rund um Benutzerkonten.

Benutzer lassen sich wie folgt auflisten:

```
$ etcdctl user list
```

Ein Benutzer lässt sich einfach so anlegen:

```
$ etcdctl user add myusername
```

Beim Anlegen eines neuen Benutzers wird ein neues Passwort abgefragt. Mit der Option `--interactive=false` kann das Passwort über die Standardeingabe übergeben werden. Auch `--new-user-password` kann zur Übergabe des Passworts verwendet werden.

Ein Benutzer, der sich nicht mit einem Passwort authentifizieren kann, lässt sich ebenfalls anlegen:

```
$ etcdctl user add myusername --no-password
```

Ein solcher Benutzer kann sich nur [über den TLS Common Name authentifizieren](#using-tls-common-name).

> [!NOTE]
> etcd unterstützt keine Authentifizierung mit einem leeren Passwort über `--user username:`. Beispielsweise kann sich ein mit leerem Passwort angelegter Benutzer wie `etcdctl user add anonymous:''` nicht über Anfragen mit Benutzername und Passwort authentifizieren; Anfragen wie `etcdctl --user anonymous: get foo` schlagen mit `user name is empty` fehl.

Einem Benutzer lassen sich Rollen wie folgt zuweisen und entziehen:

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

Die Einstellungen des Benutzers lassen sich wie folgt anzeigen:

```
$ etcdctl user get myusername
```

Das Passwort eines Benutzers lässt sich wie folgt ändern:

```
$ etcdctl user passwd myusername
```

Bei der Passwortänderung wird erneut ein neues Passwort abgefragt. Mit der Option `--interactive=false` kann das Passwort über die Standardeingabe übergeben werden.

Ein Konto löschen:
```
$ etcdctl user delete myusername
```


## Rollen verwalten {#working-with-roles}

Der Unterbefehl `role` von `etcdctl` übernimmt alle Aufgaben rund um die Zugriffskontrolle für einzelne Rollen, die Benutzern zugewiesen wurden.

Rollen auflisten:

```
$ etcdctl role list
```

Eine neue Rolle anlegen:

```
$ etcdctl role add myrolename
```

Eine Rolle hat kein Passwort; sie definiert lediglich eine neue Menge von Zugriffsrechten.

Rollen erhalten Zugriff auf einen einzelnen Schlüssel oder einen Schlüsselbereich.

Der Bereich kann als Intervall [start-key, end-key) angegeben werden, wobei start-key in alphabetischer, lexikografischer Reihenfolge kleiner als end-key sein sollte.

Der Zugriff kann zum Lesen, zum Schreiben oder für beides gewährt werden, wie in den folgenden Beispielen:

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

Die gewährten Rechte lassen sich jederzeit anhand der Rolle anzeigen:

```
$ etcdctl role get myrolename
```

Der Entzug von Berechtigungen folgt demselben Prinzip:

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

Ebenso das vollständige Löschen einer Rolle:

```
$ etcdctl role delete myrolename
```

## Authentifizierung aktivieren {#enabling-authentication}

Für die Aktivierung der Authentifizierung sind mindestens die folgenden Schritte erforderlich. Der Administrator kann Benutzer und Rollen nach Belieben vor oder nach der Aktivierung der Authentifizierung einrichten.

Sicherstellen, dass der root-Benutzer angelegt ist:

```
$ etcdctl user add root
Password of root:
```

Authentifizierung aktivieren:

```
$ etcdctl auth enable
```

Danach läuft etcd mit aktivierter Authentifizierung. Um sie aus beliebigem Grund zu deaktivieren, dient der entsprechende Gegenbefehl:

```
$ etcdctl --user root:rootpw auth disable
```

## Schutzumfang der Authentifizierung {#security-scope-of-authentication}

Wenn die Authentifizierung mit `etcdctl auth enable` aktiviert wird, schützt sie die Operationen der V3-gRPC-API (get, put, delete, watch usw.).

Die HTTP-Endpunkte `/metrics` und `/health` verwenden einen separaten Handler und werden **nicht** durch die V3-RBAC-Authentifizierung geschützt. Dadurch können Prometheus und Load-Balancer Metriken ohne gRPC-Authentifizierung abrufen, während die Schlüssel-Wert-Daten weiterhin geschützt sind.

Diese Endpunkte zur Überwachung lassen sich wie folgt absichern:

- mTLS mit `--cert-file`, `--key-file` und `--client-cert-auth` aktivieren
- Oder die Metriken mit `--listen-metrics-urls` an eine private Schnittstelle binden
- Oder den Zugriff durch Netzwerkrichtlinien/Firewallregeln beschränken

## Mit `etcdctl` authentifizieren {#using-etcdctl-to-authenticate}

`etcdctl` unterstützt zur Authentifizierung eine ähnliche Option wie `curl`.

```
$ etcdctl --user user:password get foo
```

Das Passwort kann interaktiv abgefragt werden:

```
$ etcdctl --user user get foo
```

Das Passwort kann auch mit der Befehlszeilenoption `--password` übergeben werden:

```
$ etcdctl --user user --password password get foo
```


Ansonsten bleiben alle `etcdctl`-Befehle unverändert. Benutzer und Rollen können weiterhin angelegt und geändert werden; dafür ist jedoch die Authentifizierung durch einen Benutzer mit der root-Rolle erforderlich.

## TLS Common Name verwenden {#using-tls-common-name}
Ab Version v3.2 wird beim Start eines etcd-Servers mit der Option `--client-cert-auth=true` das Feld Common Name (CN) im TLS-Zertifikat des Clients als etcd-Benutzer verwendet. In diesem Fall authentifiziert der Common Name den Benutzer, und der Client benötigt kein Passwort. Wenn sowohl 1. `--client-cert-auth=true` übergeben wird und der Client einen CN bereitstellt als auch 2. der Client Benutzername und Passwort übergibt, hat die Authentifizierung mit Benutzername und Passwort Vorrang. Diese Funktion kann nicht mit gRPC-proxy und gRPC-gateway verwendet werden. gRPC-proxy terminiert TLS vom Client, sodass alle Clients ein Zertifikat des Proxys gemeinsam nutzen. gRPC-gateway verwendet intern eine TLS-Verbindung, um HTTP-Anfragen in gRPC-Anfragen umzuwandeln, und unterliegt daher derselben Einschränkung. Die Clients können ihren CN deshalb nicht korrekt an den Server übermitteln. gRPC-proxy meldet einen Fehler und beendet sich, wenn ein angegebenes Zertifikat einen nicht leeren CN enthält. gRPC-proxy gibt einen Fehler zurück, der auf den nicht leeren CN im Zertifikat des Clients hinweist.

## Hinweise zur Passwortstärke {#notes-on-password-strength}
`etcdctl` und die etcd-API erzwingen beim Anlegen von Benutzern oder beim Ändern ihrer Passwörter keine bestimmte Passwortlänge. Die Durchsetzung solcher Anforderungen liegt in der Verantwortung des Administrators. Um Sicherheitsrisiken durch schwache Passwörter zu vermeiden, können die [Authentifizierung über den TLS Common Name](#using-tls-common-name) und Benutzer verwendet werden, die mit der Option `--no-password` angelegt wurden.
