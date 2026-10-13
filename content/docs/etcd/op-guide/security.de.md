---
title: "Sicherheitsmodell für den Datentransport"
weight: 4125
description: "Daten während der Übertragung schützen"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/security.md"
aliases: [/etcd/op-guide/security/]
---

etcd unterstützt automatisches TLS sowie die Authentifizierung über Clientzertifikate sowohl für die Kommunikation zwischen Clients und Servern als auch zwischen Peers (Servern bzw. innerhalb des Clusters). **etcd aktiviert weder die [RBAC-basierte Authentifizierung][auth] noch die Authentifizierung auf der Transportschicht standardmäßig, um den Einstieg in die Datenbank zu erleichtern. Eine Änderung dieses Standards würde außerdem die Kompatibilität des seit 2013 bestehenden Projekts brechen. Ein etcd-Cluster ohne aktivierte Sicherheitsfunktionen kann seine Daten beliebigen Clients zugänglich machen.**

Für den Einstieg werden zunächst ein CA-Zertifikat und ein signiertes Schlüsselpaar für ein Mitglied benötigt. Es wird empfohlen, für jedes Clustermitglied ein neues Schlüsselpaar zu erstellen und zu signieren.

Das Werkzeug [cfssl] bietet eine einfache Schnittstelle zur Zertifikatserzeugung; ein Beispiel für seine Verwendung steht [hier][tls-setup]. Alternativ hilft diese [Anleitung zum Erzeugen selbstsignierter Schlüsselpaare][tls-guide].

Die folgende Optionsliste ist aufgrund laufender Entwicklungsänderungen möglicherweise nicht aktuell. Die neuesten verfügbaren Optionen lassen sich mit `etcd --help` oder in der [etcd-Hilfe][etcd help] nachschlagen.

## Grundlegende Einrichtung {#basic-setup}

etcd akzeptiert mehrere zertifikatsbezogene Konfigurationsoptionen, entweder als Befehlszeilenoptionen oder als Umgebungsvariablen:

**Kommunikation zwischen Client und Server:**

`--cert-file=<path>`: Zertifikat für SSL/TLS-Verbindungen **zu** etcd. Ist diese Option gesetzt, kann advertise-client-urls das HTTPS-Schema verwenden.

`--key-file=<path>`: Schlüssel für das Zertifikat. Muss unverschlüsselt sein.

`--client-cert-auth`: Ist diese Option gesetzt, prüft etcd alle eingehenden HTTPS-Anfragen auf ein von der vertrauenswürdigen CA signiertes Clientzertifikat. Anfragen ohne gültiges Clientzertifikat schlagen fehl. Ist die [Authentifizierung][auth] aktiviert, liefert das Zertifikat die Anmeldedaten für den im Feld Common Name angegebenen Benutzernamen.

`--trusted-ca-file=<path>`: Vertrauenswürdige Zertifizierungsstelle.

`--auto-tls`: Automatisch erzeugte, selbstsignierte Zertifikate für TLS-Verbindungen mit Clients verwenden.

**Peer-Kommunikation (zwischen Servern bzw. innerhalb des Clusters):**

Die Peer-Optionen funktionieren genauso wie die Optionen für die Kommunikation zwischen Client und Server:

`--peer-cert-file=<path>`: Zertifikat für SSL/TLS-Verbindungen zwischen Peers. Es wird sowohl beim Lauschen auf der Peer-Adresse als auch beim Senden von Anfragen an andere Peers verwendet.

`--peer-key-file=<path>`: Schlüssel für das Zertifikat. Muss unverschlüsselt sein.

`--peer-client-cert-auth`: Ist diese Option gesetzt, prüft etcd alle eingehenden Peer-Anfragen aus dem Cluster auf gültige Clientzertifikate, die von der angegebenen CA signiert wurden.

`--peer-trusted-ca-file=<path>`: Vertrauenswürdige Zertifizierungsstelle.

`--peer-auto-tls`: Automatisch erzeugte, selbstsignierte Zertifikate für TLS-Verbindungen zwischen Peers verwenden.

Wird ein Zertifikat für Client-Server- oder Peer-Verbindungen angegeben, muss auch der Schlüssel gesetzt sein. Alle diese Konfigurationsoptionen sind ebenfalls über Umgebungsvariablen wie `ETCD_TRUSTED_CA_FILE`, `ETCD_PEER_TRUSTED_CA_FILE` usw. verfügbar.

**Gemeinsame Optionen:**

`--cipher-suites`: Kommagetrennte Liste unterstützter TLS-Cipher-Suites zwischen Server und Client sowie zwischen Peers (bei leerem Wert automatisch von Go befüllt).

`--tls-min-version=<version>` Legt die niedrigste von etcd unterstützte TLS-Version fest.

`--tls-max-version=<version>` Legt die höchste von etcd unterstützte TLS-Version fest. Ohne Angabe wird die höchste von Go unterstützte Version verwendet.

### keyUsage und extendedKeyUsage in TLS-Zertifikaten {#tls-certificate-keyusage-and-extendedkeyusage}

Beim Erzeugen von X.509-Zertifikaten zur Absicherung des etcd-Datentransports sollten die Zertifikate
je nach ihrer Rolle passende Felder für `keyUsage` und
`extendedKeyUsage` enthalten. etcd verwendet zur Zertifikatsprüfung die Go-Bibliotheken
`crypto/tls` und `crypto/x509`,
die diese Verwendungszwecke beim TLS-Handshake durchsetzen.

Die folgende Tabelle fasst die empfohlenen Verwendungszwecke für gängige Zertifikatsrollen zusammen:

| Zertifikatsrolle | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| Server (Client-Server-Verbindung) | digitalSignature, keyEncipherment | serverAuth |
| Client | digitalSignature, keyEncipherment | clientAuth |
| Peer (Server-Server-Verbindung) | digitalSignature, keyEncipherment | serverAuth, clientAuth |

Hinweise:

- Ist `--peer-client-cert-auth` aktiviert, werden Peer-Zertifikate
  für gegenseitiges TLS zwischen etcd-Mitgliedern verwendet und benötigen daher sowohl
  `serverAuth` als auch `clientAuth`.
- Clientzertifikate für `--client-cert-auth` sollten
  `clientAuth` enthalten.

## Beispiel 1: Transportsicherheit zwischen Client und Server mit HTTPS {#example-1-client-to-server-transport-security-with-https}

Dafür ein CA-Zertifikat (`ca.crt`) und ein signiertes Schlüsselpaar (`server.crt`, `server.key`) bereithalten.

etcd schrittweise für einfache HTTPS-Transportsicherheit konfigurieren:

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

Der Start sollte problemlos gelingen. Die Konfiguration lässt sich anschließend durch HTTPS-Kommunikation mit etcd testen:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Der Befehl sollte einen erfolgreichen Handshake anzeigen. Da selbstsignierte Zertifikate mit einer eigenen Zertifizierungsstelle verwendet werden, muss die CA mit der Option `--cacert` an curl übergeben werden. Alternativ kann das CA-Zertifikat zum Verzeichnis der vertrauenswürdigen Systemzertifikate hinzugefügt werden, gewöhnlich `/etc/pki/tls/certs` oder `/etc/ssl/certs`.

**Benutzer von OSX 10.9+**: curl 7.30.0 auf OSX 10.9+ versteht keine auf der Befehlszeile übergebenen Zertifikate.
Stattdessen die Testdatei ca.crt direkt in den Schlüsselbund importieren oder curl die Option `-k` übergeben, um Fehler zu ignorieren.
Für einen Test ohne `-k` den Befehl `open ./tests/fixtures/ca/ca.crt` ausführen und den Anweisungen folgen.
Dieses Zertifikat nach dem Test unbedingt entfernen!
Falls eine andere Lösung bekannt ist, teilen Sie uns diese mit.

## Beispiel 2: Authentifizierung zwischen Client und Server mit HTTPS-Clientzertifikaten {#example-2-client-to-server-authentication-with-https-client-certificates}

Bisher kann der etcd-Client die Serveridentität prüfen und Transportsicherheit herstellen. Mit Clientzertifikaten lässt sich darüber hinaus unbefugter Zugriff auf etcd verhindern.

Die Clients übermitteln ihre Zertifikate an den Server. Dieser prüft, ob das Zertifikat von der angegebenen CA signiert wurde, und entscheidet, ob er die Anfrage bedient.

Dafür werden dieselben Dateien wie im ersten Beispiel benötigt, außerdem ein von derselben Zertifizierungsstelle signiertes Schlüsselpaar für den Client (`client.crt`, `client.key`).

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

Nun dieselbe Anfrage wie oben an diesen Server senden:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Der Server sollte die Anfrage ablehnen:

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

Damit sie erfolgreich ist, muss das von der CA signierte Clientzertifikat an den Server übergeben werden:

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

Die Ausgabe sollte Folgendes enthalten:

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

Außerdem die Antwort des Servers:

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

Cipher-Suites angeben, um [schwache TLS-Cipher-Suites](https://github.com/etcd-io/etcd/issues/8320) zu sperren.

Der TLS-Handshake schlägt fehl, wenn das Client Hello ungültige Cipher-Suites anfordert.

Zum Beispiel:

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

Clientanfragen müssen dann eine der auf dem Server angegebenen Cipher-Suites verwenden:

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## Beispiel 3: Transportsicherheit und Clientzertifikate in einem Cluster {#example-3-transport-security--client-certificates-in-a-cluster}

etcd unterstützt dasselbe Modell für die **Peer-Kommunikation**, also die Kommunikation zwischen etcd-Mitgliedern eines Clusters.

Angenommen, `ca.crt` sowie zwei Mitglieder mit eigenen, von dieser CA signierten Schlüsselpaaren (`member1.crt` & `member1.key`, `member2.crt` & `member2.key`) sind vorhanden. Dann wird etcd wie folgt gestartet:


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Die etcd-Mitglieder bilden einen Cluster. Die gesamte Kommunikation zwischen dessen Mitgliedern wird verschlüsselt und anhand der Clientzertifikate authentifiziert. Die Ausgabe von etcd zeigt, dass die für Verbindungen verwendeten Adressen HTTPS nutzen.

## Beispiel 4: Automatische Transportsicherheit mit selbstsignierten Zertifikaten {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> Werden ClientAutoTLS und PeerAutoTLS angegeben, sind die von etcd automatisch erzeugten Client- und Peer-Zertifikate nur 1 Jahr gültig. Mit der Option --self-signed-cert-validity lässt sich die Gültigkeitsdauer der Zertifikate in Jahren festlegen.

Für Fälle, in denen die Kommunikation verschlüsselt, aber nicht authentifiziert werden muss, kann etcd seine Nachrichten mit automatisch erzeugten, selbstsignierten Zertifikaten verschlüsseln. Dies vereinfacht die Bereitstellung, da Zertifikate und Schlüssel nicht außerhalb von etcd verwaltet werden müssen.
etcd mit den Optionen `--auto-tls` und `--peer-auto-tls` so konfigurieren, dass es selbstsignierte Zertifikate für Client- und Peer-Verbindungen verwendet:

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Selbstsignierte Zertifikate authentifizieren keine Identität, daher gibt curl einen Fehler zurück:

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

Um die Prüfung der Zertifikatskette zu deaktivieren, curl mit der Option `-k` aufrufen:

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## Hinweise zu DNS SRV {#notes-for-dns-srv}

Seit v3.1.0 (außer v3.2.9) authentifiziert die Initialisierung über SRV-Erkennung `ServerName` anhand der Stammdomäne aus der Option `--discovery-srv`. Dies soll Zertifikatsangriffe nach dem Man-in-the-Middle-Prinzip verhindern, indem ein passender Stammdomänenname im Feld Subject Alternative Name (SAN) des Zertifikats verlangt wird. Beispielsweise authentifiziert `etcd --discovery-srv=etcd.local` Peers und Clients nur dann, wenn die bereitgestellten Zertifikate die Stammdomäne `etcd.local` als Eintrag im Feld Subject Alternative Name (SAN) enthalten.

## Hinweise zum etcd-Proxy {#notes-for-etcd-proxy}

> [!NOTE]
> Dieser Abschnitt beschreibt den historischen v2-Proxy, der inzwischen entfernt wurde. Für etcd 3.7 den [v3-gRPC-Proxy](/de/docs/etcd/op-guide/grpc_proxy/) verwenden.

Bei einer abgesicherten Clientverbindung terminiert der etcd-Proxy TLS vom Client und verwendet für die Kommunikation mit etcd-Mitgliedern seinen eigenen Schlüssel und sein eigenes Zertifikat aus `--peer-key-file` und `--peer-cert-file`.

Der Proxy kommuniziert mit etcd-Mitgliedern sowohl über deren `--advertise-client-urls` als auch über deren `--advertise-peer-urls`. Er leitet Clientanfragen an die bekannt gegebenen Client-URLs der Mitglieder weiter und synchronisiert die anfängliche Clusterkonfiguration über deren bekannt gegebene Peer-URLs.

Ist für ein etcd-Mitglied die Clientauthentifizierung aktiviert, muss der Administrator sicherstellen, dass das in `--peer-cert-file` des Proxys angegebene Peer-Zertifikat für diese Authentifizierung gültig ist. Ist auch die Peerauthentifizierung aktiviert, muss das Peer-Zertifikat des Proxys dafür ebenfalls gültig sein.

## Hinweise zur TLS-Authentifizierung {#notes-for-tls-authentication}

Seit [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) werden [TLS-Zertifikate bei jeder Clientverbindung neu geladen](https://github.com/etcd-io/etcd/pull/7829). Dadurch lassen sich ablaufende Zertifikate ersetzen, ohne die etcd-Server zu stoppen: Die alten Zertifikate werden einfach mit neuen überschrieben. Das Aktualisieren bei jeder Verbindung sollte keinen allzu großen Zusatzaufwand verursachen, könnte aber künftig durch eine Caching-Schicht verbessert werden. Beispieltests stehen [hier](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757).

Seit [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) [lehnt der Server eingehende Peer-Zertifikate mit falschem IP-`SAN` ab](https://github.com/etcd-io/etcd/pull/7687). Enthält ein Peer-Zertifikat beispielsweise IP-Adressen im Feld Subject Alternative Name (SAN), authentifiziert der Server einen Peer nur, wenn dessen entfernte IP-Adresse einer dieser Adressen entspricht. Dies soll den Beitritt unbefugter Endpunkte zum Cluster verhindern. Der CSR von Peer B (mit `cfssl`) könnte beispielsweise so aussehen:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

Die tatsächliche IP-Adresse von Peer B ist dabei `10.138.0.2`, nicht `10.138.0.27`. Versucht Peer B dem Cluster beizutreten, lehnt Peer A ihn mit dem Fehler `x509: certificate is valid for 10.138.0.27, not 10.138.0.2` ab, weil Bs entfernte IP-Adresse nicht mit der Adresse im Feld Subject Alternative Name (SAN) übereinstimmt.

Seit [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09) [löst der Server TLS-`DNSNames` bei der Prüfung von `SAN` auf](https://github.com/etcd-io/etcd/pull/7767). Enthält ein Peer-Zertifikat im Feld Subject Alternative Name (SAN) nur DNS-Namen und keine IP-Adressen, authentifiziert der Server den Peer nur, wenn die Vorwärtsauflösung dieser Namen (`dig b.com`) eine zur entfernten IP-Adresse passende Adresse ergibt. Der CSR von Peer B (mit `cfssl`) könnte beispielsweise so aussehen:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

Die entfernte IP-Adresse von Peer B ist dabei `10.138.0.2`. Versucht B dem Cluster beizutreten, löst Peer A den eingehenden Host `b.com` auf, um die Liste seiner IP-Adressen zu erhalten (z. B. mit `dig b.com`). Enthält die Liste die IP-Adresse `10.138.0.2` nicht, lehnt A den Peer B mit dem Fehler `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]` ab.

Seit [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07) [akzeptiert der Server Verbindungen bei passender IP-Adresse ohne Prüfung der DNS-Einträge](https://github.com/etcd-io/etcd/pull/8223). Enthält ein Peer-Zertifikat im Feld Subject Alternative Name (SAN) sowohl IP-Adressen als auch DNS-Namen und stimmt die entfernte IP-Adresse mit einer dieser IP-Adressen überein, akzeptiert der Server die Verbindung ohne weitere Prüfung der DNS-Namen. Der CSR von Peer B (mit `cfssl`) könnte beispielsweise so aussehen:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

Die entfernte IP-Adresse von Peer B ist dabei `10.138.0.2`, und `invalid.domain` ist ein ungültiger Host. Versucht B dem Cluster beizutreten, authentifiziert Peer A ihn erfolgreich, da das Feld Subject Alternative Name (SAN) eine gültige, passende IP-Adresse enthält. Weitere Einzelheiten stehen in [Issue #8206](https://github.com/etcd-io/etcd/issues/8206).

Seit [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04) [unterstützt der Server die Rückwärtsauflösung für DNS-`SAN` mit Platzhaltern](https://github.com/etcd-io/etcd/pull/8281). Enthält ein Peer-Zertifikat im Feld Subject Alternative Name (SAN) nur DNS-Namen und keine IP-Adressen, führt der Server zunächst eine Rückwärtsauflösung der entfernten IP-Adresse durch, um die zugehörigen Namen zu erhalten (z. B. `nslookup IPADDR`). Er akzeptiert die Verbindung, wenn einer dieser Namen exakt oder über einen Platzhalter mit einem DNS-Namen des Peer-Zertifikats übereinstimmt. Andernfalls führt er für jeden DNS-Eintrag des Peer-Zertifikats eine Vorwärtsauflösung durch (z. B. `example.default.svc` bei einem Eintrag `*.example.default.svc`). Er akzeptiert die Verbindung dann nur, wenn die aufgelösten Adressen des Hosts die entfernte IP-Adresse des Peers enthalten. Der CSR von Peer B (mit `cfssl`) könnte beispielsweise so aussehen:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

Die entfernte IP-Adresse von Peer B ist dabei `10.138.0.2`. Versucht B dem Cluster beizutreten, löst Peer A die IP-Adresse `10.138.0.2` rückwärts auf, um die Liste der Hostnamen zu erhalten. Anschließend vergleicht er diese Hostnamen exakt oder über Platzhalter mit den DNS-Namen im Feld Subject Alternative Name (SAN) von Bs Zertifikat. Schlägt sowohl die Rückwärts- als auch die Vorwärtsauflösung fehl, gibt er den Fehler `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]` zurück. Weitere Einzelheiten stehen in [Issue #8268](https://github.com/etcd-io/etcd/issues/8268).

[v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) ergänzt die Option [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616), um eine [CN-basierte Authentifizierung (Common Name) für Verbindungen zwischen Peers](https://github.com/etcd-io/etcd/issues/8262) zu unterstützen. Bei der TLS-Initialisierung von Kubernetes werden dynamische Zertifikate für etcd-Mitglieder und andere Systemkomponenten erzeugt (z. B. API-Server, kubelet usw.). Separate CAs für jede Komponente ermöglichen eine strengere Zugriffskontrolle für den etcd-Cluster, sind aber häufig aufwendig zu pflegen. Mit --peer-cert-allowed-cn kann ein Knoten auch bei gemeinsam genutzten CAs nur mit passendem Common Name beitreten. Der Abgleich ist ein exakter Zeichenfolgenvergleich mit dem Feld Common Name (CN) des Zertifikats; Platzhalter und Präfixvergleiche werden nicht unterstützt. Für die Filterung anhand von Hostnamen mit --peer-cert-allowed-hostname oder --client-cert-allowed-hostname wird die Go-Funktion x509.Certificate.VerifyHostname() verwendet. Sie unterstützt sowohl exakte Hostnamen als auch Platzhaltereinträge (z. B. *.example.com). Beispielsweise wird jedes Mitglied eines Clusters mit 3 Knoten mit folgenden CSRs (mit cfssl) eingerichtet:




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

Wird `--peer-cert-allowed-cn etcd.local` angegeben, werden nur Peers mit passenden Common Names authentifiziert. Knoten mit anderen CNs in ihren CSRs oder einem anderen `--peer-cert-allowed-cn` werden abgelehnt:

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

Jeder Prozess sollte wie folgt gestartet werden:

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) und [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) beheben das erneute Laden von TLS, wenn [das SAN-Feld des Zertifikats nur IP-Adressen und keine Domänennamen enthält](https://github.com/etcd-io/etcd/issues/9541). Ein Mitglied könnte beispielsweise mit folgenden CSRs (mit `cfssl`) eingerichtet sein:

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

In Go ruft der Server `(*tls.Config).GetCertificate` zum erneuten Laden von TLS genau dann auf, wenn sein Feld `(*tls.Config).Certificates` leer ist oder `(*tls.ClientHelloInfo).ServerName` nicht leer ist und eine gültige SNI vom Client enthält. Früher befüllte etcd `(*tls.Config).Certificates` beim ersten TLS-Handshake des Clients immer, sodass es nicht leer war. Daher musste der Client stets eine passende SNI liefern, um die TLS-Prüfung zu bestehen und `(*tls.Config).GetCertificate` zum erneuten Laden der TLS-Dateien auszulösen.

Bei einem Zertifikat, dessen SAN-Feld [keine Domänennamen, sondern nur IP-Adressen enthält](https://github.com/etcd-io/etcd/issues/9541), wird jedoch `*tls.ClientHelloInfo` mit leerem Feld `ServerName` angefordert. Dadurch wird beim ersten TLS-Handshake kein erneutes Laden ausgelöst. Das ist problematisch, wenn abgelaufene Zertifikate im laufenden Betrieb ersetzt werden müssen.

Nun wird `(*tls.Config).Certificates` beim ersten TLS-Handshake des Clients leer angelegt, um zunächst `(*tls.Config).GetCertificate` auszulösen und anschließend die übrigen Zertifikate bei jeder neuen TLS-Verbindung zu laden, selbst wenn die SNI des Clients leer ist, etwa bei Zertifikaten, die nur IP-Adressen enthalten.

## Hinweise zur Host-Zulassungsliste {#notes-for-host-whitelist}

Die Option `etcd --host-whitelist` legt die zulässigen Hostnamen aus HTTP-Clientanfragen fest. Die Richtlinie für Clientursprünge schützt ungesicherte etcd-Server vor [„DNS Rebinding“](https://en.wikipedia.org/wiki/DNS_rebinding). Dabei kann eine beliebige Website einfach einen autorisierten DNS-Namen erstellen und ihn auf `"localhost"` oder eine andere Adresse verweisen lassen. Dadurch werden alle HTTP-Endpunkte eines auf `"localhost"` lauschenden etcd-Servers zugänglich und somit für DNS-Rebinding-Angriffe anfällig. Weitere Einzelheiten stehen in [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2).

Die Richtlinie für Clientursprünge funktioniert wie folgt:

1. Ist die Clientverbindung über HTTPS abgesichert, alle Hostnamen zulassen.
2. Ist die Clientverbindung nicht abgesichert und `"HostWhitelist"` nicht leer, nur HTTP-Anfragen zulassen, deren Host-Feld in der Zulassungsliste steht.

Für strengere Kontrolle wird diese Richtlinie unabhängig davon durchgesetzt, ob die Authentifizierung aktiviert ist.

Standardmäßig verwenden `etcd --host-whitelist` und `embed.Config.HostWhitelist` den Wert `*`, sodass alle Hostnamen zugelassen sind. Eine leere Zulassungsliste erlaubt ebenfalls alle Hostnamen. Bei der Angabe von Hostnamen werden Loopback-Adressen nicht automatisch hinzugefügt. Um Loopback-Schnittstellen zuzulassen, sie manuell in die Zulassungsliste aufnehmen (z. B. `"localhost"`, `"127.0.0.1"` usw.).

## Häufig gestellte Fragen {#frequently-asked-questions}

### Warum erscheint bei der TLS-Clientauthentifizierung ein SSLv3 alert handshake failure? {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

Das Paket `crypto/tls` von `golang` prüft vor der Verwendung des öffentlichen Zertifikatsschlüssels dessen Verwendungszweck.
Damit dieser Schlüssel zur Clientauthentifizierung verwendet werden kann, muss bei seiner Erstellung `clientAuth` zu `Extended Key Usage` hinzugefügt werden.

Dazu wie folgt vorgehen:

Den folgenden Abschnitt zu openssl.cnf hinzufügen:

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

Bei der Zertifikatserstellung unbedingt mit der Option `-extensions` darauf verweisen:

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### Bei der Peerauthentifizierung mit Zertifikaten erscheint "certificate is valid for 127.0.0.1, not $MY_IP" {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
Sicherstellen, dass die Zertifikate mit der öffentlichen IP-Adresse des Mitglieds als Subject Name signiert werden. Das Werkzeug `etcd-ca` bietet beispielsweise die Option `--ip=` für seinen Befehl `new-cert`.

Das Zertifikat muss für den FQDN des Mitglieds im Subject Name signiert werden; die IP-Adresse über Subject Alternative Names (kurz IP SANs) ergänzen. Das Werkzeug `etcd-ca` bietet die Option `--domain=` für seinen Befehl `new-cert`; auch openssl kann [dies][alt-name].

### Verschlüsselt etcd Daten auf Datenträgern? {#does-etcd-encrypt-data-stored-on-disk-drives}
Nein. etcd verschlüsselt keine auf Datenträgern gespeicherten Schlüssel-Wert-Daten. Für die Verschlüsselung von in etcd gespeicherten Daten gibt es unter anderem folgende Möglichkeiten:
* Clientanwendungen die Daten ver- und entschlüsseln lassen
* Eine Funktion des zugrunde liegenden Speichersystems zur Verschlüsselung gespeicherter Daten verwenden, etwa [dm-crypt]

### Warum erscheint die Protokollwarnung "directory X exist without recommended permission -rwx------"? {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
Wenn etcd bestimmte neue Verzeichnisse erstellt, setzt es deren Dateiberechtigungen auf 700, um unberechtigten Zugriff möglichst zu verhindern. Hat der Benutzer ein Verzeichnis bereits mit eigenen Einstellungen angelegt, verwendet etcd dieses vorhandene Verzeichnis und protokolliert eine Warnung, falls die Berechtigungen von 700 abweichen.

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /de/docs/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
