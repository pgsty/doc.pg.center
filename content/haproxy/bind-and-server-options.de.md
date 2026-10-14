---
title: "5. Bind- und Server-Optionen"
linkTitle: "5. Bind- und Server-Optionen"
weight: 160
description: "Listener, Server, default-server und DNS-Auflösungsoptionen"
icon: fa-solid fa-network-wired
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/bind-and-server-options/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 5"
---

Die Schlüsselwörter "bind", "server" und "default-server" unterstützen je nach Build-Optionen und der Systemumgebung, auf der HAProxy gebaut wurde, eine Reihe von Einstellungen. Diese Einstellungen bestehen in der Regel aus einem Wort, gegebenenfalls gefolgt von einem Wert, und werden in derselben Zeile wie die "bind"- oder "server"-Zeile angegeben. Alle diese Optionen werden in diesem Abschnitt beschrieben.

## 5.1. Bind-Optionen {#section-5-1}
Das Schlüsselwort "bind" unterstützt eine bestimmte Anzahl von Einstellungen, die alle als Argumente in derselben Zeile übergeben werden. Die Reihenfolge, in der diese Argumente erscheinen, ist ohne Bedeutung, solange sie nach der Bind-Adresse stehen. Alle diese Parameter sind optional. Einige bestehen aus einem einzelnen Wort (Boolescher Wert), während andere danach einen Wert erwarten. In diesem Fall muss der Wert unmittelbar nach dem Einstellungsnamen angegeben werden.

Die derzeit unterstützten Einstellungen sind die folgenden.

<a id="entry-5-1-accept-netscaler-cip"></a>

**`accept-netscaler-cip <magic number>`**

```haproxy
accept-netscaler-cip <magic number>
```

Erzwingt die Verwendung des NetScaler Client IP Insertion-Protokolls für jede Verbindung, die von einem der auf derselben Zeile deklarierten TCP-Sockets akzeptiert wird. Das NetScaler Client IP Insertion-Protokoll legt die Layer-3/4-Adressen der eingehenden Verbindung fest, die überall dort verwendet werden, wo eine Adresse benötigt wird, mit der Ausnahme von „tcp-request connection“-Regeln, die nur die echte Verbindungsadresse sehen. Die Protokollausgaben spiegeln die in diesem Protokoll angegebenen Adressen wider, sofern das Protokoll nicht verletzt wird; in diesem Fall wird weiterhin die echte Adresse verwendet. Dieses Schlüsselwort, kombiniert mit Unterstützung durch externe Komponenten, kann als effizienter und zuverlässiger Ersatz für das X-Forwarded-For-Verfahren dienen, das nicht immer zuverlässig ist und nicht einmal immer verwendbar ist. Siehe auch „tcp-request connection expect-netscaler-cip“ für eine feinere Einstellung, welche Clients das Protokoll nutzen dürfen.

<a id="entry-5-1-accept-proxy"></a>

**`accept-proxy`**

```haproxy
accept-proxy
```

Erzwingt die Verwendung des PROXY-Protokolls für jede Verbindung, die von einem der auf derselben Zeile deklarierten Sockets akzeptiert wird. Versionen 1 und 2 des PROXY-Protokolls werden unterstützt und korrekt erkannt. Das PROXY-Protokoll legt die Layer-3/4-Adressen der eingehenden Verbindung fest, die überall dort verwendet werden, wo eine Adresse benötigt wird, mit der Ausnahme von „tcp-request connection“-Regeln, die nur die echte Verbindungsadresse sehen. Die Protokollausgaben spiegeln die in diesem Protokoll angegebenen Adressen wider, sofern das Protokoll nicht verletzt wird; in diesem Fall wird weiterhin die echte Adresse verwendet. Dieses Schlüsselwort, kombiniert mit Unterstützung durch externe Komponenten, kann als effizienter und zuverlässiger Ersatz für das X-Forwarded-For-Verfahren dienen, das nicht immer zuverlässig ist und nicht einmal immer verwendbar ist. Siehe auch „tcp-request connection expect-proxy“ für eine feinere Einstellung, welche Clients das Protokoll nutzen dürfen.

<a id="entry-5-1-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Erlaubt den Empfang früher Daten bei Verwendung von TLSv1.3. Dies ist aus Sicherheitsgründen standardmäßig deaktiviert. Da es anfällig für Replay-Angriffe ist, sollten Sie dies nur für Anfragen zulassen, die sicher wiederholt werden können, also für idempotente Anfragen. Sie können die Aktion "wait-for-handshake" für jede Anfrage verwenden, die mit frühen Daten nicht sicher ist. Bei QUIC wird 0rtt mit QuicTLS, OpenSSL \>= 3.5.2 und AWS-LC unterstützt. Bei TCP/TLS wird 0rtt nur mit OpenSSL unterstützt und erfordert, dass der Client ein ALPN sendet, andernfalls werden frühe Daten vor dem Handshake nicht berücksichtigt.

<a id="entry-5-1-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Aktiviert die TLS-ALPN-Erweiterung und meldet die angegebene Protokollliste als unterstützte Protokolle über ALPN. Die Protokollliste besteht aus einer durch Kommas getrennten Liste von Protokollnamen, beispielsweise: "http/1.1,http/1.0" (ohne Anführungszeichen). Dies erfordert, dass die SSL-Bibliothek mit Unterstützung für TLS-Erweiterungen gebaut wurde (überprüfen Sie mit haproxy -vv). Die ALPN-Erweiterung ersetzt die ursprüngliche NPN-Erweiterung. Auf Protokollebene ist ALPN erforderlich, um HTTP/2 auf einem HTTPS-Frontend und HTTP/3 auf einem QUIC-Frontend zu aktivieren. Wenn bei solchen Frontends keine der Einstellungen "npn", "alpn" und "no-alpn" gesetzt ist, wird für ein reguläres HTTPS-Frontend standardmäßig "h2,http/1.1" und für ein QUIC-Frontend "h3" verwendet. Versionen von OpenSSL vor 1.0.2 unterstützten ALPN nicht und unterstützten lediglich die mittlerweile veraltete NPN-Erweiterung. Zum Zeitpunkt der Erstellung dieses Dokuments unterstützen die meisten Browser weiterhin sowohl ALPN als auch NPN für HTTP/2, sodass ein Fallback auf NPN noch eine Weile funktionieren könnte. ALPN muss jedoch, wann immer möglich, verwendet werden. Protokolle, die nicht angeboten werden, werden nicht verhandelt. Es ist beispielsweise möglich, nur HTTP/2-Verbindungen zu akzeptieren:

```text
bind :443 ssl crt pub.pem alpn h2  # explicitly disable HTTP/1.1
```

QUIC unterstützt nur h3 und hq-interop als ALPN. h3 steht für HTTP/3 und hq-interop wird für http/0.9 und den QUIC-Interop-Runner verwendet (siehe <https://interop.seemann.io>). Jede "alpn"-Anweisung ersetzt die vorherige. Um sie zu entfernen, verwenden Sie "no-alpn".

Beachten Sie, dass einige ältere Browser wie Firefox 88 Probleme mit WebSocket über H2 hatten. Falls ein solcher Einsatz vorliegt, kann es erforderlich sein, entweder HTTP/2 in der "alpn"-Zeichenkette explizit zu deaktivieren, indem Sie es auf "http/1.1" oder "no-alpn" setzen, oder "h2-workaround-bogus-websocket-clients" global zu aktivieren.

<a id="entry-5-1-backlog"></a>

**`backlog <backlog>`**

```haproxy
backlog <backlog>
```

Legt die Backlog-Einstellung des Sockets auf diesen Wert fest. Wenn nicht angegeben oder 0, wird stattdessen der Backlog des Frontends verwendet, der in der Regel auf den Wert von maxconn festgelegt ist.

<a id="entry-5-1-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt eine PEM-Datei fest, aus der CA-Zertifikate geladen werden, die zur Überprüfung des Clientzertifikats verwendet werden. Es ist möglich, ein Verzeichnis mit mehreren CAs zu laden; in diesem Fall versucht HAProxy, jede Datei mit den Endungen ".pem", ".crt", ".cer" und .crl" im Verzeichnis zu laden. Dateien, die mit einem Punkt beginnen, werden ignoriert.

Warnung: Der Parameter "@system-ca" kann anstelle von cafile verwendet werden, um die vertrauenswürdigen CAs Ihres Systems zu nutzen, wie dies bei der server-Anweisung geschieht. Sie dürfen ihn jedoch nur verwenden, wenn Sie wissen, was Sie tun. Die Konfiguration auf diese Weise bedeutet im Wesentlichen, dass der mit bind konfigurierte Listener jedes Clientzertifikat akzeptiert, das von einer der CAs auf Ihrem System generiert wurde, was äußerst unsicher ist.

<a id="entry-5-1-ca-ignore-err"></a>

**`ca-ignore-err [all|<errorID>,...]`**

```haproxy
ca-ignore-err [all|<errorID>,...]
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Legt eine durch Kommas getrennte Liste von Fehler-IDs fest, die bei der Überprüfung auf Tiefe > 0 ignoriert werden sollen. Es kann sich um eine numerische ID oder um den Konstantennamen (X509_V_ERR) handeln, der in der OpenSSL-Dokumentation verfügbar ist:
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES> Es wird empfohlen, den Konstantennamen zu verwenden, da der numerische Wert in neuen OpenSSL-Versionen geändert werden kann. Wenn auf 'all' gesetzt, werden alle Fehler ignoriert. Der SSL-Handshake wird nicht abgebrochen, wenn ein Fehler ignoriert wird.

<a id="entry-5-1-ca-sign-file"></a>

**`ca-sign-file <cafile>`**

```haproxy
ca-sign-file <cafile>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt eine PEM-Datei fest, die sowohl das CA-Zertifikat als auch den CA-Privatschlüssel enthält, der zur Erstellung und Signierung von Serverzertifikaten verwendet wird. Dies ist eine obligatorische Einstellung, wenn die dynamische Generierung von Zertifikaten aktiviert ist. Weitere Details finden Sie unter 'generate-certificates'.

<a id="entry-5-1-ca-sign-pass"></a>

**`ca-sign-pass <passphrase>`**

```haproxy
ca-sign-pass <passphrase>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt die Passphrase für den CA-Privatschlüssel an. Diese Einstellung ist optional und wird nur verwendet, wenn die dynamische Generierung von Zertifikaten aktiviert ist. Weitere Details finden Sie unter 'generate-certificates'.

<a id="entry-5-1-ca-verify-file"></a>

**`ca-verify-file <cafile>`**

```haproxy
ca-verify-file <cafile>
```

Diese Einstellung legt eine PEM-Datei fest, aus der CA-Zertifikate geladen werden, die zur Überprüfung des Clientzertifikats verwendet werden. Sie legt CA-Zertifikate fest, die nicht in den in der Server-Hello-Nachricht gesendeten CA-Namen enthalten sein dürfen. Typischerweise muss "ca-file" mit Zwischenzertifikaten und "ca-verify-file" mit Zertifikaten definiert werden, die die Kette abschließen, wie beispielsweise die Root-CA.

<a id="entry-5-1-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Diese Einstellung ist nur auf Systemen verfügbar, die TCP_CONGESTION definieren, und wurde unter Linux
und FreeBSD überprüft. Sie übernimmt den Namen eines TCP-Überlastungssteuerungsalgorithmus und richtet
den Listener so ein, dass er diesen Algorithmus für alle von ihm angenommenen Verbindungen verwendet.
Typische Namen sind "reno" und "cubic"; sie hängen vom Betriebssystem ab. Auf manchen Systemen können
besondere Berechtigungen erforderlich sein, um bestimmte Algorithmen zu konfigurieren. Unter Linux
steht die Liste verfügbarer Algorithmen im sysctl "net.ipv4.tcp_available_congestion_control"; die ohne
besondere Rechte zulässigen Algorithmen stehen in "net.ipv4.tcp_allowed_congestion_control". Für
Algorithmen, die zusätzliche Berechtigungen benötigen, kann die Capability "cap_net_admin" erforderlich
sein (siehe "setcap" im global-Abschnitt). Kann ein bestimmter Überlastungssteuerungsalgorithmus nicht
konfiguriert werden, bleibt der Standardalgorithmus unverändert und eine Warnung meldet das Problem.
Siehe auch das server-Schlüsselwort "cc" ([Abschnitt 5.2](/de/haproxy/bind-and-server-options/#section-5-2)).
Beispiel:

```text
frontend public
    bind :443 cc bbr   # use the BBR algorithm for high bandwidths
```

<a id="entry-5-1-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der Verschlüsselungsalgorithmen ("Cipher-Suite") fest, die beim
SSL/TLS-Handshake bis einschließlich TLSv1.2 ausgehandelt werden. Das Format der Zeichenfolge ist in
"man 1 ciphers" in den OpenSSL-Handbuchseiten definiert. Hintergrundinformationen und Empfehlungen
finden Sie beispielsweise unter (<https://wiki.mozilla.org/Security/Server_Side_TLS>) und
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Zur Konfiguration der
Verschlüsselungsalgorithmen für TLSv1.3 siehe das Schlüsselwort "ciphersuites".

<a id="entry-5-1-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde und
HAProxy mit OpenSSL 1.1.1 oder neuer gebaut wurde. Sie legt die Zeichenfolge mit der Liste der
Verschlüsselungsalgorithmen ("Cipher-Suite") fest, die beim TLSv1.3-Handshake ausgehandelt werden.
Das Format der Zeichenfolge ist im Abschnitt "ciphersuites" von "man 1 ciphers" in den
OpenSSL-Handbuchseiten definiert. Zur Konfiguration der Verschlüsselungsalgorithmen für TLSv1.2
und ältere Versionen siehe das Schlüsselwort "ciphers". Diese Einstellung akzeptiert möglicherweise
TLSv1.2-Cipher-Suites; dieses Verhalten ist jedoch nicht dokumentiert und wird nicht empfohlen,
da es inkonsistent oder fehlerhaft sein könnte. Die standardmäßigen TLSv1.3-Cipher-Suites von OpenSSL sind:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 unterstützt nur 5 Cipher-Suites:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Beispiel:

```text
ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-5-1-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der ausgehandelten Signaturalgorithmen für die Clientauthentifizierung
fest. Das Format der Zeichenfolge ist in "man 3 SSL_CTX_set1_client_sigalgs" in den OpenSSL-Handbuchseiten
definiert. Ohne konkreten Anwendungsfall wird von dieser Einstellung abgeraten.

<a id="entry-5-1-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt
eine PEM-Datei an, aus der die zur Überprüfung des Clientzertifikats verwendete Zertifikatssperrliste
geladen wird. Für jedes Zertifikat in Ihrer Zertifizierungsstellenkette muss eine Zertifikatssperrliste
bereitgestellt werden.

<a id="entry-5-1-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde.

HAProxy verwendet einen Cache: Dateien werden nur einmal in den Zertifikatsspeicher geladen;
jedes weitere Schlüsselwort "crt" verwendet diese zwischengespeicherte Version. Wurde das Zertifikat
in einem "crt-store" deklariert, wird der Zertifikatsspeicher von dort befüllt. Es wird dann nicht
versucht, anhand von Dateierweiterungen zusätzliche Dateien zu laden.

Die Einstellung gibt eine PEM-Datei an, die sowohl die erforderlichen Zertifikate als auch die
zugehörigen privaten Schlüssel enthält. Diese Datei kann durch Zusammenfügen mehrerer PEM-Dateien
erstellt werden (z. B. cat cert.pem key.pem \>
combined.pem). Benötigt Ihre CA ein Zwischenzertifikat, kann dieses ebenfalls an die Datei angehängt
werden. Zwischenzertifikate können auch über die Direktive "issuers-chain-path" gemeinsam in einem
Verzeichnis bereitgestellt werden.

Enthält die Datei keinen privaten Schlüssel, versucht HAProxy, den Schlüssel unter demselben Pfad
mit der angehängten Endung ".key" zu laden.

Unterstützt die verwendete OpenSSL-Version Diffie-Hellman, werden die in dieser Datei enthaltenen
Parameter geladen.

Wird statt einer PEM-Datei ein Verzeichnisname verwendet, werden alle Dateien dieses Verzeichnisses
in alphabetischer Reihenfolge geladen, außer ihre Namen enden auf '.key', '.issuer', '.ocsp' oder
'.sctl' (reservierte Erweiterungen). Dateien, deren Namen mit einem Punkt beginnen, werden ebenfalls
ignoriert. Die Direktive kann mehrfach angegeben werden, um Zertifikate aus mehreren Dateien oder
Verzeichnissen zu laden. Die Zertifikate werden Clients präsentiert, die ein gültiges TLS-Feld
Server Name Indication übermitteln, das zu einem ihrer CN oder alternativen Subjektnamen passt.
Platzhalter werden unterstützt; dabei ersetzt das Platzhalterzeichen '\*' den ersten Bestandteil
des Hostnamens (z. B. passt \*.example.org zu [www.example.org](http://www.example.org), aber nicht
zu [www.sub.example.org](http://www.sub.example.org)). Bei einem leeren Verzeichnis startet HAProxy
nur, wenn das Schlüsselwort "strict-sni" verwendet wird.

Übermittelt der Client keine SNI, unterstützt die SSL-Bibliothek keine TLS-Erweiterungen oder
übermittelt der Client einen SNI-Hostnamen, der zu keinem Zertifikat passt, wird das zuerst geladene
Zertifikat präsentiert. Beim Laden von Zertifikaten aus einem Verzeichnis wird daher dringend
empfohlen, das Standardzertifikat zuerst als Datei zu laden oder sicherzustellen, dass es stets
die erste Datei im Verzeichnis ist. Zur Auswahl mehrerer Standardzertifikate (1 rsa und 1 ecdsa)
gibt es 3 Möglichkeiten:

- Ein Zertifikatsbündel kann als erstes Zertifikat konfiguriert werden (`crt foobar.pem` in der
  Konfiguration, wobei die vorhandenen Dateien `foobar.pem.ecdsa` und `foobar.pem.rsa` sind).
- Oder für jedes Zertifikat ein Filter '\*' in einer crt-list-Zeile.
- Das Schlüsselwort 'default-crt' kann verwendet werden.

Dasselbe Zertifikat kann ohne Nebenwirkungen mehrfach geladen werden.

Einige CAs (wie GoDaddy) bieten beim Bezug eines Zertifikats eine Auswahlliste von Servertypen an,
in der HAProxy fehlt. Wählen Sie in diesem Fall unbedingt einen Webserver, für den die CA ein
Zwischenzertifikat voraussetzt (bei GoDaddy liefert die Auswahl Apache Tomcat das richtige Bündel;
viele andere, z. B. NGINX, ergeben dagegen ein falsches Bündel, das bei manchen Clients nicht funktioniert).

HAProxy prüft für jede PEM-Datei, ob eine Datei unter demselben Pfad mit der angehängten Endung
".ocsp" vorhanden ist. Wird eine solche Datei gefunden, wird die Unterstützung für die TLS-Erweiterung
Certificate Status Request (auch als "OCSP stapling" bekannt) automatisch aktiviert. Der Inhalt dieser
Datei ist optional. Ist sie nicht leer, muss sie eine gültige OCSP-Antwort im DER-Format enthalten.
Eine gültige OCSP-Antwort muss folgende Regeln erfüllen: Sie muss den Status good anzeigen, eine
einzelne Antwort für das Zertifikat der PEM-Datei enthalten und zum Zeitpunkt des Hinzufügens gültig
sein. Werden diese Regeln nicht eingehalten, wird die OCSP-Antwort ignoriert und eine Warnung
ausgegeben. Um festzustellen, für welches Zertifikat eine OCSP-Antwort gilt, wird das Zertifikat des
Ausstellers benötigt. Wird dieses in der PEM-Datei nicht gefunden, wird es aus einer Datei mit dem
Pfad der PEM-Datei und der angehängten Endung ".issuer" geladen, sofern diese vorhanden ist.
Andernfalls schlägt der Vorgang mit einem Fehler fehl.

HAProxy prüft für jede PEM-Datei außerdem, ob eine Datei unter demselben Pfad mit der angehängten
Endung ".sctl" vorhanden ist. Wird eine solche Datei gefunden, wird die Unterstützung für die
TLS-Erweiterung Certificate Transparency (RFC6962) aktiviert. Die Datei muss eine gültige Signed
Certificate Timestamp List enthalten, wie im RFC beschrieben. Beim Einlesen wird die grundlegende
Syntax geprüft, jedoch werden keine Signaturen verifiziert.

In manchen Fällen ist es sinnvoll, in den für Clients angebotenen Cipher-Suites mehrere
Schlüsseltypen zu unterstützen, etwa RSA und ECDSA. So können Clients, die EC-Zertifikate
unterstützen, EC-Verschlüsselungsalgorithmen nutzen, während zugleich ältere Clients unterstützt
werden, die nur RSA beherrschen.

Dafür ist OpenSSL 1.1.1 erforderlich. Sie können dieses Verhalten konfigurieren, indem Sie für
jeden Zertifikatstyp einen crt-Eintrag angeben oder ein Zertifikatsbündel konfigurieren, wie es vor
HAProxy 1.8 erforderlich war. Siehe "ssl-load-extra-files".

<a id="entry-5-1-crt-ignore-err"></a>

**`crt-ignore-err <errors>`**

```haproxy
crt-ignore-err <errors>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
eine durch Kommas getrennte Liste von Fehler-IDs fest, die bei der Überprüfung in der Tiefe == 0
ignoriert werden. Dies kann eine numerische ID oder der Konstantenname (X509_V_ERR) aus der
OpenSSL-Dokumentation sein:
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES> Es wird
empfohlen, den Konstantennamen zu verwenden, da sich der numerische Wert in neuen OpenSSL-Versionen
ändern kann. Beim Wert 'all' werden alle Fehler ignoriert. Wird ein Fehler ignoriert, wird der
SSL-Handshake nicht abgebrochen.

<a id="entry-5-1-crt-list"></a>

**`crt-list <file>`**

```haproxy
crt-list <file>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt
eine Liste von PEM-Dateien mit einer optionalen ssl-Konfiguration und einem SNI-Filter pro Zertifikat
an. Jede Zeile hat das folgende Format:

```text
<crtfile> [\[<sslbindconf> ...\]] [[!]<snifilter> ...]
```

Leerzeilen und Zeilen, die mit einem Rautezeichen ('#') beginnen, werden ignoriert.

Die crt-list kann dynamisch über den Statistik-Socket bearbeitet werden. (Siehe "add ssl crt-list",
"del ssl crt-list" und "show ssl crt-list" im Verwaltungshandbuch.)

crt-list sind normalerweise eigene Dateien. Ein über die Direktive "crt" geladenes Verzeichnis
wird intern jedoch ebenfalls als crt-list dargestellt. Die Direktive "ssl-f-use" in einem Frontend
deklariert außerdem eine mit diesem Frontend verknüpfte crt-list.

crtfile:

```text
Dies ist der Dateiname des Zertifikats oder ein Bezeichner, wenn es
an anderer Stelle deklariert wurde (beispielsweise über die CLI oder
mit einem Alias in einem crt-store).

Dieselbe <crtfile> kann in mehreren Zeilen mit unterschiedlichen
Optionen und Filtern verwendet werden.

Zertifikatsbündel (siehe "ssl-load-extra-files") werden in einer
crt-list unterstützt, sofern in <crtfile> nur der Basisname angegeben
wird. HAProxy dupliziert die crt-list-Zeile intern und fügt beim Laden
der Datei eine Algorithmus-Erweiterung (.rsa, .ecdsa, .dsa) hinzu.
```

sslbindconf:

```text
 <sslbindconf> unterstützt die folgenden Schlüsselwörter der bind-Zeile
 (siehe Abschnitt 5.1. Bind-Optionen):

 - allow-0rtt
 - alpn
 - ca-file
 - ca-verify-file
 - ciphers
 - ciphersuites
 - client-sigalgs
 - crl-file
 - curves
 - ecdhe
 - no-alpn
 - no-ca-names
 - npn
 - sigalgs
 - ssl-min-ver
 - ssl-max-ver
 - verify

 <sslbindconf> unterstützt außerdem die folgenden Schlüsselwörter von
 load in crt-store (siehe Abschnitt 12.7.1. Ladeoptionen):

 - crt
 - key
 - ocsp
 - issuer
 - sctl
 - ocsp-update

Die Parameter der bind-Zeile werden in <sslbindconf> übernommen. Sind
keine angegeben, werden die Standardoptionen übernommen. Die in
<sslbindconf> angegebenen Parameter überschreiben diese übernommenen
Einstellungen.
```

snifilter:

```text
Wird der Parameter <snifilter> in einer crt-list-Zeile verwendet, werden
CN und SAN bei der Auswahl des Zertifikats dieser Zeile während des
Handshakes nicht mehr verwendet. Stattdessen wird <snifilter> verwendet.

<snifilter> ist eine durch Leerzeichen getrennte Liste von Einträgen.
Diese Liste kann Domains oder Platzhalter enthalten. Die Platzhalter
entsprechen dem DNS-Platzhalterformat mit einem einzelnen Sternchen
als erstem Zeichen des Eintrags. Eine Domain kann durch einen negativen
Filter von einem Platzhalter ausgeschlossen werden, indem der einzelnen
Domain ein '!' vorangestellt wird. Ein ! vor einem * wird ignoriert.
Negative Filter ohne Platzhalter in derselben Zeile werden ebenfalls
nicht unterstützt. Mit dem besonderen Eintrag '*' werden Standardzertifikate
angegeben, auf die zurückgegriffen wird, wenn keine Domain übereinstimmt.

Die Zertifikate werden Clients präsentiert, die ein gültiges TLS-Feld
Server Name Indication übermitteln, das mit einem der SNI-Filter oder
mit CN und SAN einer <crtfile> übereinstimmt. Der Abgleichalgorithmus
sucht zunächst nach einem positiven Domain-Eintrag in der Liste. Wird
keiner gefunden, sucht er nach einem Platzhalter. Stimmt ein Platzhalter
überein, prüft haproxy auf einen negativen Filter in derselben Zeile und
verwirft die Übereinstimmung gegebenenfalls. Bei mehreren Schlüsselalgorithmen
(RSA,ECDSA,DSA) versucht HAProxy, pro Typ ein passendes Zertifikat zu
finden, und wählt das passende anhand der Unterstützung des Clients aus.

Übermittelt der Client keine SNI oder passt kein Zertifikat, wird auf
eines der Standardzertifikate zurückgegriffen. Mit der Option 'strict-sni'
kann dieser Rückgriff auf ein Standardzertifikat deaktiviert werden.
Sind mehrere Standardzertifikate definiert, kann HAProxy abhängig von
der Unterstützung des Clients das passende ECDSA- oder RSA-Zertifikat wählen.

Das erste in einer bind-Zeile deklarierte Zertifikat wird als
Standardzertifikat verwendet, unabhängig davon, ob es über die Option
crt oder crt-list angegeben wurde.
Es kann auch ein Filter '*' deklariert werden, der dieses Zertifikat
zur Liste der Standardzertifikate hinzufügt. Für eine übersichtlichere
Konfiguration können Standardzertifikate explizit (mit einem Filter '*')
am Listenanfang stehen, sodass davor kein implizites Standardzertifikat
hinzugefügt wird.
Da Zertifikatsbündel in der crt-list für jeden Algorithmus dupliziert
werden, belegt nur ein Algorithmus die erste Zeile der crt-list und
wird als Standard betrachtet. Deklarieren Sie entweder '*' als Filter,
um das gesamte Bündel als Standard festzulegen, oder legen Sie es in
der bind-Zeile fest.

Der Befehl "show ssl sni" am Statistik-Socket kann zur Fehlersuche in
Ihrer Konfiguration verwendet werden. (Siehe "show ssl sni" im
Verwaltungshandbuch.)
```

Beispiel:

```shell
# comment
default.pem.rsa *
default.pem.ecdsa *
cert2.pem [alpn h2,http/1.1]
certW.pem *.domain.tld !secure.domain.tld
certS.pem [curves X25519:P-256 ciphers ECDHE-ECDSA-AES256-GCM-SHA384] secure.domain.tld
foo.crt [key bar.pem ocsp foo.ocsp ocsp-update on] foo.bar.com
```

<a id="entry-5-1-default-crt"></a>

**`default-crt <cert>`**

```haproxy
default-crt <cert>
```

Diese Option wirkt wie die Option "crt"; zusätzlich wird dieses Zertifikat jedoch als
Standardzertifikat verwendet. Es können mehrere Standardzertifikate hinzugefügt werden, um sowohl
ein ECDSA- als auch ein RSA-Zertifikat bereitzustellen. Weitere Zertifikate sind kaum sinnvoll.

Diese Option deaktiviert implizite Standardzertifikate nicht. Wird zuerst ein 'crt'-Zertifikat
vor allen 'default-crt'- oder weiteren 'crt'-Angaben deklariert, wird es weiterhin als
Standardzertifikat verwendet.

Ein Standardzertifikat wird verwendet, wenn in der bind-Zeile keine Option "strict-sni" angegeben
ist. Es wird bereitgestellt, wenn der Client die servername-Erweiterung nicht verwendet hat oder
wenn servername zu keinem konfigurierten Zertifikat passt.

Beispiel:

```shell
# this bind line has 2 default certificates
bind *:443 default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa crt website.pem.rsa

# this bind line has 3 default certificates
bind *:443 crt website.pem.rsa default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa
```

Siehe auch das Schlüsselwort "crt".

<a id="entry-5-1-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste elliptischer Kurvenalgorithmen ("Kurvensuite") fest, die beim
SSL/TLS-Handshake mit ECDHE ausgehandelt werden. Die Zeichenfolge ist eine durch Doppelpunkte
getrennte Liste von Kurvennamen, beispielsweise "X25519:P-256" (ohne Anführungszeichen).
Ist "curves" gesetzt, wird der Parameter "ecdhe" ignoriert.

<a id="entry-5-1-defer-accept"></a>

**`defer-accept`**

```haproxy
defer-accept
```

Ist ein optionales Schlüsselwort, das nur auf bestimmten Linux-Kerneln unterstützt wird. Es legt fest, dass eine Verbindung erst akzeptiert wird, sobald Daten eintreffen, oder spätestens nach der ersten Neuübertragung. Dies sollte nur bei Protokollen verwendet werden, bei denen der Client zuerst Daten sendet (z. B. HTTP). Es kann die Leistung leicht verbessern, indem sichergestellt wird, dass der Großteil der Anfrage bereits verfügbar ist, wenn die Verbindung akzeptiert wird. Andererseits kann es keine Verbindungen erkennen, über die keine Daten gesendet werden. Es ist wichtig zu beachten, dass diese Option in allen Kerneln bis einschließlich 2.6.31 fehlerhaft ist, da die Verbindung erst akzeptiert wird, wenn der Client Daten sendet. Dies kann Probleme mit vorgeschalteten Firewalls verursachen, die eine aufgebaute Verbindung sehen, während der Proxy sie nur im Zustand SYN_RECV sieht. Diese Option wird nur auf TCPv4/TCPv6-Sockets unterstützt und von anderen ignoriert.

<a id="entry-5-1-ecdhe"></a>

**`ecdhe <named curve>`**

```haproxy
ecdhe <named curve>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt die benannte Kurve (RFC 4492) fest, die zum Generieren von ephemeren ECDH-Schlüsseln verwendet wird. Standardmäßig wird die benannte Kurve prime256v1 verwendet.

<a id="entry-5-1-ech"></a>

**`ech <dir> [ EXPERIMENTAL ]`**

```haproxy
ech <dir> [ EXPERIMENTAL ]
```

Wendet alle ECH-Schlüssel aus `<dir>` auf die bind-Zeile an. Die Dateien müssen die Erweiterung .ech haben und das PEM-Dateiformat für ECH verwenden. ( <https://datatracker.ietf.org/doc/draft-farrell-tls-pemesni/> )

Dieses Schlüsselwort aktiviert ECH im Shared-Modus, wobei HAProxy sowohl TLS-Endpunkt als auch ECH-Endpunkt ist. Siehe <https://datatracker.ietf.org/doc/draft-ietf-tls-esni/>

Dies ist eine experimentelle Funktion, die die Option "expose-experimental-directives" im globalen Abschnitt erfordert. Außerdem wird eine OpenSSL-Version benötigt, die ECH unterstützt ( <https://github.com/openssl/openssl/tree/feature/ech>), und HAProxy muss mit USE_ECH=1 kompiliert sein. Die ECH-API von AWS-LC wird nicht unterstützt.

Beispiel:

```shell
$ openssl ech -public_name foobar.com -out /etc/haproxy/echkeydir/foobar.com.ech

$ cat haproxy.cfg
[...]
bind :443 ech /etc/haproxy/echkeydir/ ssl crt example.com.pem

// Use the ECHCONFIG section of your .ech file
$ openssl s_client -tls1_3 -connect example.com:443 -servername example.com \
-ech_config_list AD3+DQA5cwAgACB6ybtgtFYoM5r8nJSotus4c7K0EG..9vYmFyLmNvbQAA
```

<a id="entry-5-1-expose-fd-listeners"></a>

**`expose-fd listeners`**

```haproxy
expose-fd listeners
```

Diese Option ist nur mit dem Statistik-Socket verwendbar. Sie ermöglicht dem Statistik-Socket, Dateideskriptoren (FD) der Listener an einen anderen HAProxy-Prozess weiterzuleiten. Im Master-Worker-Modus ist dies nicht mehr erforderlich, da die Listener über interne Socket-Paare zwischen Master und Workern übertragen werden. Siehe auch "-x" im Verwaltungshandbuch.

<a id="entry-5-1-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Erzwingt für die von diesem Listener aufgebauten SSL-Verbindungen die ausschließliche Verwendung von SSLv3. SSLv3 ist im Allgemeinen weniger kostspielig als die TLS-Gegenstücke bei hohen Verbindungsraten. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Erzwingt für die von diesem Listener aufgebauten SSL-Verbindungen die ausschließliche Verwendung von TLSv1.0. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Erzwingt für die von diesem Listener aufgebauten SSL-Verbindungen die ausschließliche Verwendung von TLSv1.1. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Erzwingt für die von diesem Listener aufgebauten SSL-Verbindungen die ausschließliche Verwendung von TLSv1.2. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Erzwingt für die von diesem Listener aufgebauten SSL-Verbindungen die ausschließliche Verwendung von TLSv1.3. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-generate-certificates"></a>

**`generate-certificates`**

```haproxy
generate-certificates
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie aktiviert die dynamische Generierung von SSL-Zertifikaten. Ein CA-Zertifikat und dessen privater Schlüssel sind erforderlich (siehe 'ca-sign-file'). Wenn HAProxy als transparenter Forward-Proxy konfiguriert ist, treten bei SSL-Anfragen Fehler auf, weil der Common Name des dem Client präsentierten Zertifikats nicht übereinstimmt. Mit dieser Option versucht HAProxy, ein Zertifikat unter Verwendung des vom Client angegebenen SNI-Hostnamens zu erzeugen. Dies geschieht nur, wenn kein Zertifikat zum SNI-Hostnamen passt (siehe 'crt-list').

Im Fall eines Fehlers bei der Zertifikaterzeugung fällt die Verbindung auf das Standardzertifikat zurück. Wenn 'strict-sni' verwendet wird, wird das Standardzertifikat nicht verwendet, und die Verbindung führt zu einem Handshake-Fehler.

Sie kann auch verwendet werden, wenn HAProxy als Reverse-Proxy konfiguriert ist, um die Bereitstellung einer Architektur mit vielen Backends zu vereinfachen.

Das Erstellen eines SSL-Zertifikats ist eine aufwändige Operation, daher wird ein LRU-Cache verwendet, um nachgebildete Zertifikate zu speichern (siehe 'tune.ssl.ssl-ctx-cache-size'). Dies erhöht den Speicherverbrauch von HAProxy, um die Latenz zu reduzieren, wenn dasselbe Zertifikat häufig verwendet wird.

<a id="entry-5-1-gid"></a>

**`gid <gid>`**

```haproxy
gid <gid>
```

Legt die Gruppe der Unix-Sockets auf die angegebene System-GID fest. Sie kann auch standardmäßig im globalen Abschnitt über die "unix-bind"-Anweisung gesetzt werden. Beachten Sie, dass einige Plattformen dies ignorieren. Diese Einstellung ist äquivalent zur "group"-Einstellung, unterscheidet sich jedoch dadurch, dass die Gruppen-ID anstelle des Namens verwendet wird. Diese Einstellung wird von nicht-Unix-Sockets ignoriert.

<a id="entry-5-1-group"></a>

**`group <group>`**

```haproxy
group <group>
```

Legt die Gruppe der Unix-Sockets auf die angegebene Systemgruppe fest. Sie kann auch standardmäßig im globalen Abschnitt über die "unix-bind"-Anweisung gesetzt werden. Beachten Sie, dass einige Plattformen dies ignorieren. Diese Einstellung ist äquivalent zur "gid"-Einstellung, unterscheidet sich jedoch dadurch, dass der Gruppenname anstelle der GID verwendet wird. Diese Einstellung wird von nicht-Unix-Sockets ignoriert.

<a id="entry-5-1-guid-prefix"></a>

**`guid-prefix <string>`**

```haproxy
guid-prefix <string>
```

Erzeugt für jeden dieser bind-Zeile zugewiesenen lauschenden Socket global eindeutige IDs, bei denen Groß- und Kleinschreibung unterschieden wird. Das Präfix wird mit dem Index der Listenerposition auf der aktuellen bind-Zeile verbunden, getrennt durch das Zeichen '-'. Weitere Informationen zum Format finden Sie in der Beschreibung des proxy-Schlüsselworts "guid". Siehe auch "shm-stats-file".

<a id="entry-5-1-id"></a>

**`id <id>`**

```haproxy
id <id>
```

Fixiert die Socket-ID. Standardmäßig werden Socket-IDs automatisch zugewiesen, aber manchmal ist es zweckmäßiger, sie festzulegen, um die Überwachung zu erleichtern. Der Wert muss strikt positiv und innerhalb des Listeners/Frontends eindeutig sein. Diese Option kann nur verwendet werden, wenn nur ein einzelner Socket definiert wird.

<a id="entry-5-1-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Definiert ein Intervall für regelmäßige Erreichbarkeitsprüfungen bei inaktiven Frontend-Verbindungen. Wenn die Gegenstelle vor der nächsten geplanten Prüfung nicht antworten kann, wird die Verbindung geschlossen. Andernfalls wird der Timer für die Client-Zeitüberschreitung neu gestartet und die Verbindung bleibt bestehen. Beachten Sie, dass http-request/http-keep-alive-Timer parallel laufen und nicht durch idle-ping zurückgesetzt werden.

Diese Funktion beruht auf spezifischer Unterstützung durch das zugrundeliegende Protokoll. Derzeit implementiert nur der H2-Multiplexer diese Funktion. idle-ping wird von anderen Protokollen einfach ignoriert.

Diese Option ist besonders nützlich bei der Verwendung von Reverse-HTTP. Die Einstellung auf der bind-Zeile ist nützlich für den Peer, der für die aktive Herstellung von Verbindungen verantwortlich ist und dann eingehenden Datenverkehr über sie empfängt.

<a id="entry-5-1-interface"></a>

**`interface <interface>`**

```haproxy
interface <interface>
```

Beschränkt den Socket auf eine bestimmte Schnittstelle. Wenn angegeben, werden nur Pakete, die von dieser spezifischen Schnittstelle empfangen wurden, vom Socket verarbeitet. Dies wird derzeit nur unter Linux unterstützt. Die Schnittstelle muss eine primäre Systemschnittstelle sein, keine aliasierte Schnittstelle. Es ist auch möglich, mehrere Frontends an dieselbe Adresse zu binden, wenn sie an unterschiedliche Schnittstellen gebunden sind. Beachten Sie, dass die Bindung an eine Netzwerkschnittstelle root-Rechte erfordert. Dieser Parameter ist nur mit TCPv4/TCPv6-Sockets kompatibel. Wenn angegeben, verwendet der Rückverkehr dieselbe Schnittstelle wie der eingehende Verkehr und deren zugehörige Routing-Tabelle, selbst wenn explizite Routen über verschiedene Schnittstellen konfiguriert sind. Dies kann nützlich sein, um asymmetrische Routing-Probleme zu beheben, wenn dieselben Client-IP-Adressen auf Frontends auf unterschiedlichen Schnittstellen zugreifen müssen.

<a id="entry-5-1-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Aktiviert oder deaktiviert kTLS für diese Sockets. Wenn aktiviert, wird kTLS verwendet, falls der Kernel dies unterstützt und der Verschlüsselungsalgorithmus kompatibel ist. Dies ist nur auf Linux-Kerneln ab 4.17 verfügbar. Bitte beachten Sie, dass einige Netztreiber und/oder TLS-Stacks die Verwendung von kTLS auf TLS v1.2 beschränken können. Siehe auch "force-tlsv12".

<a id="entry-5-1-label"></a>

**`label <label>`**

```haproxy
label <label>
```

Legt ein optionales Label für diese Sockets fest. Es kann verwendet werden, um Sockets nach Label zu gruppieren, unabhängig davon, wo die bind-Zeilen deklariert wurden.

<a id="entry-5-1-level"></a>

**`level <level>`**

```haproxy
level <level>
```

Diese Einstellung wird ausschließlich mit Statistik-Sockets verwendet, um die Art der Befehle zu beschränken, die auf dem Socket ausgeführt werden dürfen. Sie wird von anderen Sockets ignoriert. `<level>` kann einer der folgenden Werte sein:

- "user" ist die geringste Berechtigungsstufe; nur nicht sensible Statistiken können gelesen werden, und keine Änderungen sind erlaubt. Dies ist auf Systemen sinnvoll, bei denen der Zugriff auf den Socket nicht einfach eingeschränkt werden kann.
- "operator" ist die Standardstufe und eignet sich für die meisten gängigen Anwendungsfälle. Alle Daten können gelesen werden, und nur nicht sensible Änderungen sind erlaubt (z. B. Zurücksetzen der Max-Zähler).
- "admin" sollte mit Vorsicht verwendet werden, da alles erlaubt ist (z. B. Zurücksetzen aller Zähler).

<a id="entry-5-1-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Beschränkt die Sockets auf diese Anzahl gleichzeitiger Verbindungen. Zusätzliche Verbindungen verbleiben im Backlog des Systems, bis eine Verbindung freigegeben wird. Wenn nicht angegeben, entspricht der Grenzwert dem Wert von maxconn des Frontends. Beachten Sie, dass bei Portbereichen oder mehreren Adressen der gleiche Wert für jeden Socket angewendet wird. Diese Einstellung ermöglicht unterschiedliche Beschränkungen für kostspielige Sockets, beispielsweise SSL-Einträge, die leicht den gesamten Speicher verbrauchen können.

<a id="entry-5-1-mode"></a>

**`mode <mode>`**

```haproxy
mode <mode>
```

Legt die oktale Berechtigungsstufe für den Unix-Socket fest. Sie kann auch standardmäßig in der globalen Abschnitt mittels der "unix-bind"-Anweisung gesetzt werden. Beachten Sie, dass einige Plattformen diese Einstellung einfach ignorieren. Diese Einstellung wird von nicht-Unix-Sockets ignoriert.

<a id="entry-5-1-mss"></a>

**`mss <maxseg>`**

```haproxy
mss <maxseg>
```

Legt den TCP-Maximum-Segment-Size (MSS)-Wert fest, der bei eingehenden Verbindungen angeboten wird. Dies kann verwendet werden, um eine niedrigere MSS für bestimmte Ports zu erzwingen, beispielsweise für Verbindungen, die durch ein VPN laufen. Beachten Sie, dass dies von einer Kernel-Funktion abhängt, die theoretisch unter Linux unterstützt wird, aber in allen Versionen vor 2.6.28 fehlerhaft war. Es kann auf anderen Betriebssystemen funktionieren oder nicht. Es kann auch vorkommen, dass sich der angebotene Wert nicht ändert, sondern nur die tatsächliche Größe ausgehender Segmente. Der üblicherweise angebotene Wert für TCPv4 über Ethernet-Netzwerke beträgt 1460 = 1500(MTU) - 40(IP+TCP). Wenn dieser Wert positiv ist, wird er als angebotene MSS verwendet. Wenn er negativ ist, gibt er an, um wie viel die angebotene MSS der eingehenden Verbindung für ausgehende Segmente reduziert werden soll. Dieser Parameter ist nur mit TCP v4/v6-Sockets kompatibel.

<a id="entry-5-1-name"></a>

**`name <name>`**

```haproxy
name <name>
```

Legt einen optionalen Namen für diese Sockets fest, der auf der Statistikseite angezeigt wird.

<a id="entry-5-1-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

Unter Linux ist es möglich, anzugeben, welchem Netzwerknamensraum ein Socket angehört. Diese Anweisung ermöglicht es, einen Listener explizit an einen anderen Namensraum als den Standardnamensraum zu binden. Weitere Informationen zu Netzwerknamensräumen finden Sie in der Dokumentation Ihres Betriebssystems.

<a id="entry-5-1-nbconn"></a>

**`nbconn <nbconn> [ EXPERIMENTAL ]`**

```haproxy
nbconn <nbconn> [ EXPERIMENTAL ]
```

Diese Einstellung ist nur für Listener-Instanzen gültig, die Reverse HTTP verwenden. Sie definiert die Anzahl der Verbindungen, die parallel aufgebaut werden. Wenn nicht angegeben, wird ein Standardwert von 1 verwendet.

Reverse HTTP ist derzeit noch in aktiver Entwicklung. Die Konfigurationsmechanismus kann sich zukünftig ändern. Aus diesem Grund ist sie intern als experimentell markiert, was bedeutet, dass "expose-experimental-directives" vor dieser Anweisung auf einer Zeile stehen muss.

<a id="entry-5-1-nice"></a>

**`nice <nice>`**

```haproxy
nice <nice>
```

Legt die 'niceness' der von diesem Socket initiierten Verbindungen fest. Der Wert muss im Bereich -1024..1024 inklusive liegen und hat standardmäßig den Wert null. Positive Werte bedeuten, dass solche Verbindungen anderen gegenüber freundlicher sind und leichter ihren Platz im Scheduler abgeben. Im Gegensatz dazu bedeuten negative Werte, dass Verbindungen eine höhere Priorität als andere haben möchten. Der Unterschied tritt nur unter hoher Last auf, wenn das System nahe an der Sättigung ist. Negative Werte sind für Low-Latency- oder Verwaltungsdienste geeignet, und hohe Werte werden allgemein für CPU-intensive Aufgaben wie SSL-Verarbeitung oder Massentransfers empfohlen, die weniger empfindlich gegenüber Latenz sind. Beispielsweise könnte es sinnvoll sein, einen positiven Wert für einen SMTP-Socket und einen negativen Wert für einen RDP-Socket zu verwenden.

<a id="entry-5-1-no-alpn"></a>

**`no-alpn`**

```haproxy
no-alpn
```

Deaktiviert die ALPN-Verarbeitung (technisch gesehen wird die ALPN-Zeichenkette auf eine leere Zeichenkette gesetzt, die nicht angeboten wird). Damit kann eine vorherige Einstellung von "alpn" rückgängig gemacht und die Aushandlung des Anwendungsprotokolls deaktiviert werden. Es kann auch verwendet werden, um zu verhindern, dass ein Listener mit einem Client auf einem HTTPS- oder QUIC-Listener ALPN aushandelt; standardmäßig bieten HTTPS-Listener "h2,http/1.1" an und QUIC-Listener bieten "h3". Siehe auch "alpn" oben. Beachten Sie, dass bei Verwendung von "crt-list" ein Zertifikat die "alpn"-Einstellung überschreiben und die Verarbeitung wieder aktivieren kann.

<a id="entry-5-1-no-ca-names"></a>

**`no-ca-names`**

```haproxy
no-ca-names
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie verhindert, dass CA-Namen in der Server-Hello-Nachricht gesendet werden, wenn ca-file verwendet wird. Verwenden Sie "ca-verify-file" anstelle von "ca-file" mit "no-ca-names".

<a id="entry-5-1-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie deaktiviert die Unterstützung für SSLv3 auf allen Sockets, die vom Listener erzeugt werden, wenn SSL unterstützt wird. Beachten Sie, dass SSLv2 im Code zwangsweise deaktiviert ist und nicht durch eine Konfigurationseinstellung aktiviert werden kann. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-no-strict-sni"></a>

**`no-strict-sni`**

```haproxy
no-strict-sni
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie deaktiviert die strikte SNI-Prüfung, die durch eine vorherige "strict-sni"-Anweisung festgelegt wurde. Dies kann erforderlich sein, um die strikte SNI-Nutzung selektiv auf einer "bind"-Zeile zu deaktivieren, wenn sie bereits global über "ssl-default-bind-options" erzwungen wurde. Siehe auch die bind-Option "strict-sni".

<a id="entry-5-1-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie deaktiviert die zustandslose Sitzungswiederaufnahme (RFC 5077 TLS Ticket-Erweiterung) und zwingt zur zustandsbasierten Sitzungswiederaufnahme. Die zustandslose Sitzungswiederaufnahme ist rechenintensiver. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar. Der TLS-Ticket-Mechanismus wird nur bis zu TLS 1.2 verwendet. Forward Secrecy ist mit TLS-Tickets beeinträchtigt, es sei denn, die Ticket-Schlüssel werden regelmäßig rotiert (durch Neuladen oder durch Verwendung von "tls-ticket-keys").

<a id="entry-5-1-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert bei SSL-Unterstützung TLSv1.0 auf allen vom Listener erzeugten Sockets. Beachten Sie,
dass SSLv2 im Code zwangsweise deaktiviert ist und durch keine Konfigurationsoption aktiviert werden
kann. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar.
Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert bei SSL-Unterstützung TLSv1.1 auf allen vom Listener erzeugten Sockets. Beachten Sie,
dass SSLv2 im Code zwangsweise deaktiviert ist und durch keine Konfigurationsoption aktiviert werden
kann. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar.
Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert bei SSL-Unterstützung TLSv1.2 auf allen vom Listener erzeugten Sockets. Beachten Sie,
dass SSLv2 im Code zwangsweise deaktiviert ist und durch keine Konfigurationsoption aktiviert werden
kann. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar.
Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert bei SSL-Unterstützung TLSv1.3 auf allen vom Listener erzeugten Sockets. Beachten Sie,
dass SSLv2 im Code zwangsweise deaktiviert ist und durch keine Konfigurationsoption aktiviert werden
kann. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar.
Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

<a id="entry-5-1-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Aktiviert die TLS-Erweiterung NPN und bietet die angegebene Protokollliste über NPN als unterstützt
an. Die Protokollliste besteht aus durch Kommas getrennten Protokollnamen, beispielsweise
"http/1.1,http/1.0" (ohne Anführungszeichen). Dafür muss die SSL-Bibliothek mit aktivierter
Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Beachten Sie, dass
die NPN-Erweiterung durch die ALPN-Erweiterung ersetzt wurde (siehe das Schlüsselwort "alpn"), die
allerdings erst ab OpenSSL 1.0.2 verfügbar ist. Wird HTTP/2 mit einer älteren OpenSSL-Version
gewünscht, kann weiterhin NPN verwendet werden, da die meisten Clients es zum Zeitpunkt der
Erstellung dieses Textes noch unterstützen. NPN und ALPN lassen sich auch gemeinsam aktivieren,
was außerhalb von Tests jedoch vermutlich nicht sinnvoll ist.

<a id="entry-5-1-prefer-client-ciphers"></a>

**`prefer-client-ciphers`**

```haproxy
prefer-client-ciphers
```

Verwendet bei der Auswahl der Cipher-Suite die Präferenz des Clients; standardmäßig wird die
Präferenz des Servers durchgesetzt. Diese Option ist auch in der globalen Anweisung
"ssl-default-bind-options" verfügbar.

Beachten Sie, dass mit OpenSSL \>= 1.1.1 ChaCha20-Poly1305 ohnehin höher priorisiert wird (auch ohne
diese Option), wenn ein ChaCha20-Poly1305-Cipher an erster Stelle der Cipher-Liste des Clients steht.

Bei einer Konfiguration mit zwei Algorithmen (RSA + ECDSA) wählt der Auswahlalgorithmus zwischen
RSA und ECDSA und bevorzugt dabei immer ECDSA. Sobald das passende Zertifikat gewählt wurde,
überlässt er der SSL-Bibliothek die Priorisierung von Ciphers, Kurven usw. Diese Option kann somit
nicht verwendet werden, um ein RSA-Zertifikat gegenüber einem ECDSA-Zertifikat zu bevorzugen.

<a id="entry-5-1-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Erzwingt das Multiplexer-Protokoll für eingehende Verbindungen. Es muss mit dem Modus des Frontends
(TCP oder HTTP) kompatibel sein. Außerdem muss es auf der Frontend-Seite verwendbar sein. Die Liste
verfügbarer Protokolle wird von haproxy -vv ausgegeben. Angezeigt werden die Protokolleigenschaften:
der Modus (TCP/HTTP), die Seite (FE/BE), der Name des Multiplexers und seine Flags.

Bei manchen Protokollen kann auf der Serverseite Head-of-Line-Blocking auftreten (flag=HOL_RISK).
Einige Protokolle unterstützen außerdem keine Upgrades (flag=NO_UPG). Auch die HTX-Kompatibilität
wird angegeben (flag=HTX).

Die folgenden Protokolle können als Argument einer "proto"-Direktive in einer bind-Zeile verwendet
werden:

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
 qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
 h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
 h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
 none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
```

Mit dieser Option wird für alle von diesem lauschenden Socket erzeugten Verbindungen die Auswahl
des am besten geeigneten Multiplexer-Protokolls umgangen. Beispielsweise lässt sich http/2 über
unverschlüsseltem TCP erzwingen, indem in der bind-Zeile "proto h2" angegeben wird.

Wenn ALPN oder NPN konfiguriert ist, sollten die angegebenen Protokolle mit dem Multiplexer-Protokoll
kompatibel sein, um Probleme zu vermeiden. Ist beispielsweise "proto h1" gesetzt, sollte ALPN nicht
auf "h2" gesetzt werden.

QMux ist eine Teilmenge von QUIC, die über TCP läuft. Sie entspricht dem folgenden Protokollentwurf:
<https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. In haproxy gilt sie derzeit als
experimentell.

<a id="entry-5-1-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Diese QUIC-spezifische Einstellung wählt den Algorithmus zur Überlastkontrolle für alle
Verbindungsversuche zu den konfigurierten QUIC-Listenern. Die Algorithmen ähneln denen von TCP.

Zusätzlich zum Algorithmus zur Überlastkontrolle ist Pacing aktiviert, um Paketverluste zu verringern
und den Durchsatz zu verbessern. Es kann mit dem globalen Schlüsselwort "tune.quic.fe.tx.pacing"
deaktiviert werden. In den meisten Fällen sollte Pacing aktiviert bleiben, insbesondere bei BBR,
da dessen ordnungsgemäße Funktion davon abhängt. BBR ohne Pacing kann bei Übertragungen zu
Verlangsamungen oder hohen Verlustraten führen.

Standardwert: cubic

Zur weiteren Anpassung kann nach dem Algorithmus eine Liste von Parametern angegeben werden.
Sie muss in Klammern und durch Kommas getrennt geschrieben werden. Jedes Argument ist optional
und kann bei Bedarf leer bleiben. Die Parameter müssen in folgender Reihenfolge stehen:

- maximale Fenstergröße in Bytes. Sie muss größer als 10k und kleiner als 4g sein. Standardmäßig
  wird der Wert von "tune.quic.fe.cc.max-win-size" verwendet.

Beispiel:

```shell
# newreno congestion control algorithm
quic-cc-algo newreno
# cubic congestion control algorithm with one megabytes as window
quic-cc-algo cubic(1m)
```

Mit dem besonderen Wert "nocc" kann ein festes Überlastfenster erzwungen werden, das immer auf die
maximale Größe gesetzt ist. Dies ist für die Fehlersuche vorgesehen, um alle Nebeneffekte des
Algorithmus zur Überlastkontrolle auszuschließen. Es darf nicht in der Produktion verwendet werden,
da es schnell zu Netzwerkproblemen wie hohen Verlustraten führen kann.

<a id="entry-5-1-quic-force-retry"></a>

**`quic-force-retry`**

```haproxy
quic-force-retry
```

Diese QUIC-spezifische Einstellung erzwingt die Verwendung der QUIC-Retry-Funktion für alle
Verbindungsversuche zu den konfigurierten QUIC-Listenern. Dabei wird überprüft, ob die Gegenstellen
an der Transportadresse, von der aus sie eine neue Verbindung eingeleitet haben, Pakete empfangen
können. Dazu wird ihnen ein Retry-Paket mit einem Token gesendet. Dieses Token muss an den Absender
des Retry-Pakets zurückgesendet werden, da nur dieser das Token validieren kann. Beachten Sie, dass
QUIC Retry damit immer verwendet wird, selbst wenn ein Retry-Schwellenwert gesetzt wurde (siehe
"tune.quic.fe.sec.retry-threshold").

Diese Einstellung setzt voraus, dass das Cluster-Geheimnis festgelegt ist; andernfalls wird beim
Start ein Fehler gemeldet (siehe "cluster-secret").

Weitere Informationen zu QUIC Retry finden Sie unter
<https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2>.

<a id="entry-5-1-quic-socket"></a>

**`quic-socket [ connection | listener ]`**

```haproxy
quic-socket [ connection | listener ]
```

Mit dieser QUIC-spezifischen Einstellung wird der Modus für die Socket-Zuweisung für die jeweiligen
Listener festgelegt. Eine vollständige Beschreibung der Vor- und Nachteile der einzelnen Modi
finden Sie unter "tune.quic.fe.sock-per-conn".

Diese Einstellung wirkt zusammen mit der globalen Option "tune.quic.fe.sock-per-conn". Ist global
der Modus "default-on" aktiv (der Standardwert), verwendet jede QUIC-Verbindung ihren eigenen
Socket; ausgenommen sind Listener mit "quic-socket listener". Ist der globale Modus hingegen auf
"force-off" gesetzt, wird die Konfiguration der einzelnen Listener ignoriert.

<a id="entry-5-1-severity-output"></a>

**`severity-output <format>`**

```haproxy
severity-output <format>
```

Diese Einstellung wird nur bei Statistik-Sockets verwendet. Sie legt fest, wie der Schweregrad vor
informativen Rückmeldungen ausgegeben wird. Der Schweregrad einer Meldung kann gemäß Syslog rfc5424
zwischen 0 und 7 liegen. Bei gültigen, erfolgreich ausgeführten Socket-Befehlen zur Datenabfrage
(etwa "show map", "get acl foo" usw.) wird niemals ein Schweregrad vorangestellt. Bei anderen
Sockets wird die Einstellung ignoriert. `<format>` kann einer der folgenden Werte sein:

- "none" (Standard): Rückmeldungen wird kein Schweregrad vorangestellt.
- "number": Der Schweregrad wird als Zahl vorangestellt.
- "string": Der Schweregrad wird als Zeichenfolge gemäß rfc5424 vorangestellt.

<a id="entry-5-1-shards"></a>

**`shards { <number> | by-thread | by-group }`**

```haproxy
shards { <number> | by-thread | by-group }
```

Im Multithread-Modus erzeugt diese Einstellung auf Betriebssystemen, die mehrere Listener auf
derselben Kombination IP:port unterstützen, automatisch die angegebene Anzahl identischer
Listener für dieselbe Zeile. Jedem wird ein gleich großer Anteil der diesem Listener zugeordneten
Threads zugewiesen. Das kann bei sehr vielen Threads nützlich sein, wenn die Sperren im Kernel
für einen einzigen Socket erheblichen Zusatzaufwand verursachen. Eingehender Datenverkehr wird dann
auf mehrere Sockets verteilt, wodurch die Konkurrenz um gemeinsame Ressourcen abnimmt. Beachten Sie,
dass dies leicht die CPU-Auslastung erhöhen kann, weil mehr Threads jeweils etwas Arbeit leisten.

Ist die Anzahl der Shards größer als die Anzahl verfügbarer Threads, wird sie automatisch auf die
Anzahl der Threads begrenzt (also ein Shard pro Thread). Auch der besondere Wert "by-thread" erzeugt
so viele Shards, wie der "bind"-Zeile Threads zugeordnet sind. Da das System den eingehenden
Datenverkehr gleichmäßig auf diese Shards verteilt, ist es wichtig, dass deren Anzahl ein
ganzzahliger Teiler der Thread-Anzahl ist. Alternativ erzeugt der besondere Wert "by-group" einen Shard pro Thread-Gruppe.
Das kann bei vielen Threads nützlich sein, wenn nicht zu viele Sockets erzeugt werden sollen.
Die Lastverteilung ist dann etwas weniger optimal, aber die Konkurrenz um gemeinsame Ressourcen
(insbesondere im System) ist weiterhin geringer als bei einem einzigen Socket.

Auf Betriebssystemen, die nicht mehrere an dieselbe Adresse gebundene Sockets unterstützen, fallen
"by-thread" und "by-group" automatisch auf einen einzigen Shard zurück. Bei "by-group" geschieht
dies ohne Warnung, da es für eine einzelne Gruppe nichts ändert und die Sockets ohnehin für jede
Gruppe dupliziert werden. Bei "by-thread" wird in diesem Fall jedoch eine Diagnosewarnung
ausgegeben, da die resultierende Anzahl von Listenern nicht der erwarteten Anzahl entspricht.

<a id="entry-5-1-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der Signaturalgorithmen fest, die beim TLSv1.2- und TLSv1.3-Handshake
ausgehandelt werden. Das Format der Zeichenfolge ist in "man 3 SSL_CTX_set1_sigalgs" in den
OpenSSL-Handbuchseiten beschrieben. Von dieser Einstellung wird abgeraten, sofern keine
Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-5-1-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
aktiviert die SSL-Entschlüsselung für die von diesem Listener erzeugten Verbindungen. Ein Zertifikat
ist erforderlich (siehe "crt" oben). Alle Inhalte in den Puffern liegen im Klartext vor, sodass
ACLs und HTTP-Verarbeitung nur auf entschlüsselte Inhalte zugreifen. SSLv3 ist standardmäßig
deaktiviert; verwenden Sie "ssl-min-ver SSLv3", um es zu aktivieren.

<a id="entry-5-1-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Diese Option erzwingt für die von diesem Listener erzeugten SSL-Verbindungen die Verwendung von
`<version>` oder einer niedrigeren Version. Diese Einstellung ohne "ssl-min-ver" zu verwenden, kann
mehrdeutig sein, da sich der Standardwert von ssl-min-ver in zukünftigen HAProxy-Versionen ändern
könnte. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options" verfügbar.
Siehe auch "ssl-min-ver".

<a id="entry-5-1-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Diese Option erzwingt für die von diesem Listener erzeugten SSL-Verbindungen die Verwendung von
`<version>` oder einer höheren Version. Der Standardwert ist "TLSv1.2". Diese Option ist auch in der
globalen Anweisung "ssl-default-bind-options" verfügbar. Siehe auch "ssl-max-ver".

<a id="entry-5-1-strict-sni"></a>

**`strict-sni`**

```haproxy
strict-sni
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Die
SSL/TLS-Aushandlung ist nur zulässig, wenn der Client eine zu einem Zertifikat passende SNI angegeben
hat. Das Standardzertifikat wird nicht verwendet. Mit dieser Option kann eine bind-Zeile auch ohne
Zertifikat gestartet werden; so lässt sich ein leeres Verzeichnis verwenden und später über den
Statistik-Socket füllen. Diese Option ist auch in der globalen Anweisung "ssl-default-bind-options"
verfügbar und kann in einer "bind"-Zeile gezielt mit "no-strict-sni" deaktiviert werden. Weitere
Informationen finden Sie bei der Option "crt". Siehe auch den Befehl "add ssl crt-list" im
Verwaltungshandbuch.

<a id="entry-5-1-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Aktiviert die TCP-MD5-Signatur (RFC 2385 Schutz von BGP-Sitzungen mithilfe der TCP-MD5-Signaturoption)
für alle eingehenden Verbindungen, die von diesem lauschenden Socket erzeugt werden. Diese Option
ist nur unter Linux verfügbar. Wenn sie aktiviert ist, wird die Zeichenfolge `<password>` verwendet,
um jedes TCP-Segment mit einem 16-Byte-MD5-Digest zu signieren. Dies schützt die TCP-Verbindung vor
Spoofing. Der wichtigste Anwendungsfall ist der Schutz von BGP gegen das Einschleusen gefälschter
TCP-Segmente in den Verbindungsstrom. Die Option kann aber für alle sehr langlebigen
TCP-Verbindungen nützlich sein.

<a id="entry-5-1-tcp-ss"></a>

**`tcp-ss <mode>`**

```haproxy
tcp-ss <mode>
```

Setzt die Option TCP Save SYN für alle eingehenden Verbindungen, die von diesem lauschenden Socket
erzeugt werden. Diese Option ist unter Linux seit Version 4.3 verfügbar. Sie weist den Kernel an,
eine Kopie des eingehenden IP-Pakets mit dem TCP-SYN-Flag nach Möglichkeit aufzubewahren, damit es
später mit der Sample-Abruffunktion "fc_saved_syn" untersucht werden kann. Die Option kennt 3 Modi: - 0 Das Speichern von SYN-Paketen ist deaktiviert; dies ist der Standard - 1 Das Speichern von
SYN-Paketen ist aktiviert und umfasst IP- und TCP-Header - 2 Das Speichern von SYN-Paketen ist
aktiviert und umfasst ETH-, IP- und TCP-Header

Dies funktioniert nur bei regulären TCP-Verbindungen und wird bei anderen Protokollen (z. B.
UNIX-Sockets) ignoriert. Siehe auch "fc_saved_syn".

<a id="entry-5-1-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Setzt den TCP User Timeout für alle eingehenden Verbindungen, die von diesem lauschenden Socket
erzeugt werden. Diese Option ist unter Linux seit Version 2.6.37 verfügbar. Damit kann HAProxy eine
Zeitüberschreitung für Sockets konfigurieren, deren Daten innerhalb der angegebenen Zeit keine
Bestätigung erhalten. Dies ist besonders für langlebige Verbindungen mit langen Leerlaufzeiten
nützlich, etwa Remote-Terminals oder Datenbank-Verbindungspools. Dort müssen die
Zeitüberschreitungen für Client und Server hoch bleiben, um lange Leerlaufzeiten zu ermöglichen;
zugleich ist es wichtig, das Verschwinden eines Clients zu erkennen, um alle Ressourcen seiner Verbindung
(und der Serversitzung) freizugeben. Das Argument ist eine Zeitspanne, standardmäßig in Millisekunden.
Dies funktioniert nur bei regulären TCP-Verbindungen und wird bei anderen Protokollen ignoriert.

<a id="entry-5-1-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Ein optionales Schlüsselwort, das nur auf Linux-Kerneln \>= 3.7 unterstützt wird. Es aktiviert TCP
Fast Open auf dem lauschenden Socket. Clients, die diese Funktion unterstützen, können damit ab der
zweiten Verbindung bereits während des 3-Wege-Handshakes eine Anfrage senden und eine Antwort
empfangen. Nach der ersten Verbindung wird dadurch jeweils ein Roundtrip eingespart. Dies ist nur
bei Protokollen mit hohen Verbindungsraten sinnvoll, bei denen jeder Roundtrip zählt. Die Option
kann Probleme mit vielen Firewalls verursachen, die keine Daten in SYN-Paketen akzeptieren. Sie
sollte deshalb erst nach gründlichen Tests aktiviert werden. Sie wird nur für TCPv4/TCPv6-Sockets
unterstützt und bei anderen Sockets ignoriert. Möglicherweise müssen Sie HAProxy mit USE_TFO=1
bauen, wenn Ihre libc TCP_FASTOPEN nicht definiert.

<a id="entry-5-1-thread"></a>

**`thread [<thread-group>/]<thread-set>[,...]`**

```haproxy
thread [<thread-group>/]<thread-set>[,...]
```

Beschränkt die Liste der Threads, auf denen dieser Listener ausgeführt werden darf. Dabei wird
keiner dieser Threads erzwungen; lediglich nicht passende Threads werden ausgeschlossen. Die
Einstellung begrenzt die Threads, die eingehende Verbindungen dieses Listeners verarbeiten dürfen.

Es gibt zwei Nummerierungsschemata. Standardmäßig sind Thread-Nummern innerhalb des Prozesses
absolut und liegen zwischen 1 und dem in global.nbthread angegebenen Wert. Ein Thread kann auch
über seine relative Nummer innerhalb seiner Thread-Gruppe bezeichnet werden. Dazu wird zuerst die
Nummer der Thread-Gruppe angegeben, gefolgt von einem Schrägstrich ('/') und den relativen
Thread-Nummern. In diesem Fall beginnen die Thread-Nummern ebenfalls bei 1 und enden je nach
Plattform bei 32 oder 64. Absolute Thread-Nummern werden automatisch in relative Nummern umgewandelt,
sobald die Thread-Gruppen bekannt sind. Üblicherweise werden absolute Nummern für einfache
Konfigurationen bevorzugt und relative Nummern für komplexe Konfigurationen, bei denen die
CPU-Anordnung für die Leistung entscheidend ist.

Nach der optionalen Thread-Gruppennummer muss die "thread-set"-Angabe folgendes Format verwenden:

```text
"all" | "odd" | "even" | [number][-[number]]
```

Wie die Namen nahelegen, wählt "all" alle Threads der Menge aus (entweder alle Threads der Gruppe,
wenn eine Gruppe angegeben ist, oder alle Threads des Prozesses). "odd" wählt alle ungeradzahligen
Threads aus (jeden zweiten Thread, beginnend bei 1), entweder im Prozess oder in der Gruppe;
"even" wählt alle geradzahligen Threads aus (jeden zweiten Thread, beginnend bei 2). Werden
stattdessen Bereiche von Thread-Nummern verwendet, werden alle Threads von der ersten bis zur
letzten Thread-Nummer des Bereichs ausgewählt. Je nachdem, ob eine Thread-Gruppennummer angegeben
ist, sind die Nummern relativ zur Gruppe oder absolut. Fehlt die erste Thread-Nummer, wird "1"
verwendet, also der erste Thread der Gruppe oder des Prozesses. Fehlt die letzte Thread-Nummer,
wird entweder die letzte Thread-Nummer der Gruppe (32 oder 64) oder die letzte Thread-Nummer des
Prozesses (global.nbthread) verwendet.

Diese Bereiche können, durch Kommas getrennt, mehrfach angegeben werden, um nicht zusammenhängende
Thread-Mengen zu definieren. Eine gegebenenfalls verwendete Gruppe muss für jeden neuen Bereich
erneut angegeben werden. Beachten Sie, dass gruppenrelative und absolute Angaben nicht gemischt
werden dürfen: Die gesamte "bind"-Zeile muss entweder absolute oder relative Notation verwenden,
da nicht gesetzte Werte erst am Ende des Parsens aufgelöst werden.

Dabei ist wichtig, dass jeder durch eine "bind"-Zeile beschriebene Listener mindestens einen Socket
erzeugt, der durch mindestens einen Dateideskriptor repräsentiert wird. Da Dateideskriptoren sich
nicht über mehrere Thread-Gruppen erstrecken können, werden automatisch mehrere Dateideskriptoren
erzeugt, wenn der Thread-Bereich einer "bind"-Zeile mehr als eine Gruppe umfasst. So ist für jede
Gruppe mindestens einer vorhanden. Technisch verweisen sie alle auf denselben Socket im Kernel,
erhalten in haproxy aber jeweils eine eigene Kennung und bei Verwendung von "option socket-stats"
sogar einen eigenen Statistikeintrag.

Der Hauptzweck besteht darin, mehrere bind-Zeilen in einem Listener mit derselben Kombination
IP:port, aber verschiedenen Threads zu verwenden. Das System kann eingehende Verbindungen dann auf
mehrere Warteschlangen verteilen und damit die interne Lastverteilung der Warteschlangen von haproxy
umgehen. Derzeit ist bekannt, dass Linux ab 3.9 dies unterstützt. Siehe auch das oben beschriebene
Schlüsselwort "shards", das die Duplizierung von "bind"-Zeilen und ihre Zuweisung zu mehreren
Thread-Gruppen automatisiert.

Dieses Schlüsselwort ist mit Reverse-HTTP-bind-Zeilen kompatibel. Für einen solchen Listener darf
jedoch keine Thread-Menge angegeben werden, die mehrere Thread-Gruppen umfasst, da "nbconn" sonst
möglicherweise nicht wie vorgesehen funktioniert.

<a id="entry-5-1-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
aktiviert die zustandslose Sitzungswiederaufnahme (RFC 5077 TLS-Ticket-Erweiterung). Dies ist der
Standard; die Option kann jedoch nötig sein, um die Funktion gezielt in einer "bind"-Zeile erneut
zu aktivieren, wenn sie global durch "no-tls-tickets" in "ssl-default-bind-options" deaktiviert
wurde. Siehe auch das bind-Schlüsselwort "no-tls-tickets".

<a id="entry-5-1-tls-ticket-keys"></a>

**`tls-ticket-keys <keyfile>`**

```haproxy
tls-ticket-keys <keyfile>
```

Legt die Datei fest, aus der die TLS-Ticket-Schlüssel geladen werden. Die Schlüssel müssen je nach
Verwendung von aes128 oder aes256 48 oder 80 Bytes lang und base64-codiert sein, mit einer Zeile
pro Schlüssel (z. B. openssl rand
80 \| openssl base64 -A \| xargs echo). Der erste Schlüssel bestimmt die Schlüssellänge der folgenden
Schlüssel; aes128- und aes256-Schlüssel können nicht gemischt werden. Die Anzahl der Schlüssel wird
mit der Build-Option TLS_TICKETS_NO festgelegt (Standard 3), und die Datei muss mindestens so viele
Schlüssel enthalten. Die letzten TLS_TICKETS_NO Schlüssel werden zur Entschlüsselung verwendet,
der vorletzte zur Verschlüsselung. Das ermöglicht einen einfachen Schlüsselwechsel: Ein neuer
Schlüssel wird an die Datei angehängt und der Prozess neu geladen. Die Schlüssel müssen regelmäßig
gewechselt werden (z. B. alle 12h), sonst ist Perfect Forward Secrecy gefährdet. Es empfiehlt sich
auch, die Schlüssel nicht auf dauerhaftem Speicher wie Festplatten abzulegen (Tipp: tmpfs verwenden
und diese Dateien nicht auslagern). Der Hinweis auf die Lebensdauer kann mit tune.ssl.timeout
geändert werden.

<a id="entry-5-1-transparent"></a>

**`transparent`**

```haproxy
transparent
```

Ein optionales Schlüsselwort, das nur auf bestimmten Linux-Kerneln unterstützt wird. Es bewirkt,
dass die Adressen auch dann gebunden werden, wenn sie nicht zum lokalen Rechner gehören. An diese
Adressen gerichtete Pakete werden dann so abgefangen, als wären die Adressen lokal konfiguriert.
Dafür muss normalerweise IP-Weiterleitung aktiviert sein. Achtung! Verwenden Sie dies nicht mit der
Standardadresse '\*', da dadurch jeglicher Datenverkehr für den angegebenen Port umgeleitet würde.
Dieses Schlüsselwort ist nur verfügbar, wenn HAProxy mit USE_LINUX_TPROXY=1 gebaut wurde. Der
Parameter ist je nach Kernel-Version nur mit TCPv4- und TCPv6-Sockets kompatibel. Einige
Distributionskernel enthalten Rückportierungen dieser Funktion; erkundigen Sie sich daher bei Ihrem
Anbieter nach der Unterstützung.

<a id="entry-5-1-uid"></a>

**`uid <uid>`**

```haproxy
uid <uid>
```

Setzt den Eigentümer der UNIX-Sockets auf die angegebene System-UID. Der Standardwert kann auch mit
der Anweisung "unix-bind" im globalen Abschnitt gesetzt werden. Beachten Sie, dass manche Plattformen
dies einfach ignorieren. Diese Einstellung entspricht "user", verwendet aber die numerische ID des
Benutzers anstelle seines Namens. Bei anderen als UNIX-Sockets wird sie ignoriert.

<a id="entry-5-1-user"></a>

**`user <user>`**

```haproxy
user <user>
```

Setzt den Eigentümer der UNIX-Sockets auf den angegebenen Systembenutzer. Der Standardwert kann auch
mit der Anweisung "unix-bind" im globalen Abschnitt gesetzt werden. Beachten Sie, dass manche
Plattformen dies einfach ignorieren. Diese Einstellung entspricht "uid", verwendet aber den
Benutzernamen anstelle seiner uid. Bei anderen als UNIX-Sockets wird sie ignoriert.

<a id="entry-5-1-v4v6"></a>

**`v4v6`**

```haproxy
v4v6
```

Ein optionales Schlüsselwort, das nur auf neueren Systemen einschließlich Linux-Kerneln \>= 2.4.21
unterstützt wird. Es bindet einen Socket sowohl an IPv4 als auch an IPv6, wenn dieser die
Standardadresse verwendet. Dies ist manchmal auf Systemen erforderlich, die standardmäßig nur an
IPv6 binden. Auf anderen als IPv6-Sockets hat es keine Wirkung und wird von der Option "v6only"
überschrieben.

<a id="entry-5-1-v6only"></a>

**`v6only`**

```haproxy
v6only
```

Ein optionales Schlüsselwort, das nur auf neueren Systemen einschließlich Linux-Kerneln \>= 2.4.21
unterstützt wird. Es bindet einen Socket nur an IPv6, wenn dieser die Standardadresse verwendet.
Da es pro Listener wirkt, wird dies manchmal einer systemweiten Einstellung vorgezogen. Auf
anderen als IPv6-Sockets hat es keine Wirkung und hat Vorrang vor der Option "v4v6".

<a id="entry-5-1-verify"></a>

**`verify [none|optional|required]`**

```haproxy
verify [none|optional|required]
```

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Bei 'none'
wird kein Client-Zertifikat angefordert; dies ist der Standard. In allen anderen Fällen wird ein
Client-Zertifikat angefordert. Liefert der Client nach der Anforderung kein Zertifikat und ist
'verify' auf 'required' gesetzt, wird der Handshake abgebrochen; mit 'optional' wäre er dagegen
erfolgreich. Ein vom Client geliefertes Zertifikat wird immer mit den CAs aus 'ca-file' und optionalen
CRLs aus 'crl-file' überprüft. Schlägt die Überprüfung fehl, wird der Handshake unabhängig von der
Option 'verify' abgebrochen, es sei denn, der Fehlercode stimmt exakt mit einem der unter
'ca-ignore-err' oder 'crt-ignore-err' aufgeführten Codes überein.

## 5.2. Server- und default-server-Optionen {#section-5-2}

Die Schlüsselwörter "server" und "default-server" unterstützen verschiedene Einstellungen, die
alle als Argumente in der server-Zeile übergeben werden. Die Reihenfolge dieser Argumente spielt
keine Rolle, und alle sind optional. Einige Einstellungen bestehen aus einzelnen Wörtern
(boolesche Werte), andere erwarten dahinter einen oder mehrere Werte. In diesem Fall müssen die
Werte unmittelbar auf den Einstellungsnamen folgen. Außer bei default-server müssen alle diese
Einstellungen, sofern verwendet, nach der Serveradresse angegeben werden:

```text
server <name> <address>[:port] [settings ...]
default-server [settings ...]
```

Beachten Sie, dass alle diese Einstellungen sowohl von "server" als auch von "default-server"
unterstützt werden, außer "id", das nur von "server" unterstützt wird.

Derzeit werden die folgenden Einstellungen unterstützt.

<a id="entry-5-2-addr"></a>

**`addr <ipv4|ipv6>`**

```haproxy
addr <ipv4|ipv6>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Mit dem Parameter "addr" kann eine andere IP-Adresse zum Senden von Health Checks oder zum
Abfragen des Agent-Checks verwendet werden. Auf manchen Servern kann es sinnvoll sein, einer
bestimmten Komponente eine eigene IP-Adresse zuzuweisen, wenn diese komplexe Tests ausführen kann,
die für Health Checks besser geeignet sind als die Anwendung selbst. Dieser Parameter wird
ignoriert, wenn "check" nicht gesetzt ist. Siehe auch den Parameter "port".

<a id="entry-5-2-agent-check"></a>

**`agent-check`**

```haproxy
agent-check
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Aktiviert einen zusätzlichen Agent-Check, der unabhängig von einem regulären Health Check
ausgeführt wird. Für einen Agent-Health-Check wird eine TCP-Verbindung zum durch "agent-port"
festgelegten Port hergestellt und eine ASCII-Zeichenfolge gelesen, die mit dem ersten gefundenen
'&#92;r' oder '&#92;n' endet. Die Zeichenfolge besteht aus Wörtern in beliebiger Reihenfolge, die
durch Leerzeichen, Tabulatoren oder Kommas getrennt sind. Jedes Wort hat eine der folgenden Formen:

- Die ASCII-Darstellung einer positiven ganzzahligen Prozentangabe, z. B. "75%". Werte in diesem
  Format setzen das Gewicht proportional zum anfänglichen Gewicht des Servers, das beim Start von
  HAProxy konfiguriert war. Beachten Sie, dass ein Gewicht von null auf der Statistikseite als
  "DRAIN" angezeigt wird, da es dieselbe Wirkung auf den Server hat (er wird aus der LB-Farm
  entfernt). Dies ist die ältere Methode, das Servergewicht zu setzen. Die Verwendung des Präfixes
  "weight:" wird bevorzugt.

- Die Zeichenfolge "weight:", unmittelbar gefolgt von einer positiven Ganzzahl oder einer
  positiven ganzzahligen Prozentangabe, ohne Leerzeichen. Endet der Wert mit '%', ist das neue
  Gewicht proportional zum anfänglichen Servergewicht. Andernfalls gilt der Wert als absolutes
  Gewicht und muss zwischen 0 und 256 liegen. Für Server in einer Farm mit einem statischen
  Lastverteilungsalgorithmus gelten strengere Grenzen, da das einmal gesetzte Gewicht nicht
  geändert werden kann. Für diese Server sind daher nur 0 und 100% zulässig (oder 0 und das
  anfängliche Gewicht). Änderungen wirken sofort, obwohl manche LB-Algorithmen eine gewisse Anzahl
  von Anfragen benötigen, um Änderungen zu berücksichtigen. Beachten Sie, dass ein Gewicht von null
  auf der Statistikseite als "DRAIN" angezeigt wird, da es dieselbe Wirkung auf den Server hat
  (er wird aus der LB-Farm entfernt).

- Die Zeichenfolge "maxconn:", unmittelbar gefolgt von einer Ganzzahl (ohne Leerzeichen). Werte in
  diesem Format setzen maxconn für einen Server. Die angegebene maximale Verbindungsanzahl muss mit
  der Anzahl der Load-Balancer und der unterschiedlichen Backends multipliziert werden, die diesen
  Health Check verwenden, um die Gesamtzahl der Verbindungen zu erhalten, die der Server empfangen
  könnte. Beispiel: maxconn:30

- Das Wort "ready". Es setzt den administrativen Zustand des Servers auf READY und hebt damit
  jeden DRAIN- oder MAINT-Zustand auf.

- Das Wort "drain". Es setzt den administrativen Zustand des Servers auf DRAIN. Der Server nimmt
  dann nur noch neue Verbindungen an, die aufgrund von Persistenz zugelassen werden.

- Das Wort "maint". Es setzt den administrativen Zustand des Servers auf MAINT. Der Server nimmt
  dann keinerlei neue Verbindungen an, und Health Checks werden eingestellt.

- Die Wörter "down", "fail" oder "stopped", optional gefolgt von einer Beschreibung nach einem
  Rautezeichen ('#'). Alle setzen den Betriebszustand des Servers auf DOWN. Da jedoch das Wort
  selbst auf der Statistikseite angezeigt wird, kann ein Administrator daran erkennen, ob die
  Situation erwartet war: Der Dienst kann absichtlich gestoppt sein, scheinbar laufen, aber einige
  Gültigkeitsprüfungen nicht bestehen, oder als ausgefallen gelten (z. B. weil der Prozess fehlt
  oder der Port nicht antwortet).

- Das Wort "up" setzt den Betriebszustand des Servers wieder auf UP, sofern auch die Health Checks
  melden, dass der Dienst erreichbar ist.

Parameter, die der Agent nicht übermittelt, werden nicht geändert. Ein Agent könnte beispielsweise
die CPU-Auslastung überwachen und nur ein relatives Gewicht melden, ohne jemals den Betriebszustand
zu beeinflussen. Ebenso könnte ein Agent als Benutzeroberfläche mit 3 Optionsfeldern gestaltet sein,
mit denen ein Administrator ausschließlich den administrativen Zustand ändert. Dabei ist jedoch
zu beachten, dass nur der Agent seine eigenen Aktionen rückgängig machen kann. Wenn ein Server
über den Agenten auf DRAIN oder DOWN gesetzt wird, muss der Agent daher auch die entsprechenden
Gegenaktionen implementieren, um den Dienst wieder in Betrieb nehmen zu können.

Wenn keine Verbindung zum Agenten hergestellt werden kann, gilt dies nicht als Fehler, da die
Erreichbarkeit durch den regulären, mit "check" aktivierten Health Check getestet wird. Achtung:
Es ist keine gute Idee, einen Agenten zu stoppen, nachdem er "down" gemeldet hat. Nur ein Agent,
der "up" meldet, kann den Server wieder aktivieren. Beachten Sie, dass die CLI am Unix-Statistik-Socket
ebenfalls das Ergebnis eines Agenten erzwingen kann, um bei Bedarf einen fehlerhaften Agenten zu
umgehen.

Der Parameter "agent-port" muss gesetzt sein. Siehe auch "agent-inter" und "no-agent-check".

<a id="entry-5-2-agent-send"></a>

**`agent-send <string>`**

```haproxy
agent-send <string>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Wenn diese Option angegeben ist, sendet HAProxy beim Verbindungsaufbau die angegebene Zeichenfolge
unverändert an den Agent-Server. Sie könnten darin beispielsweise den Backend-Namen codieren,
damit der Agent je nach Backend unterschiedliche Antworten senden kann. Fügen Sie ein '&#92;n'
ein, wenn die Anfrage mit einem Zeilenumbruch enden soll.

<a id="entry-5-2-agent-inter"></a>

**`agent-inter <delay>`**

```haproxy
agent-inter <delay>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der Parameter "agent-inter" setzt das Intervall zwischen zwei Agent-Checks auf `<delay>`
Millisekunden. Ist er nicht angegeben, beträgt das Intervall standardmäßig 2000 ms.

Wie bei allen zeitbasierten Parametern kann explizit eine andere Einheit aus { us, ms, s, m, h, d }
angegeben werden. Der Parameter "agent-inter" dient auch als Zeitüberschreitung für Agent-Checks,
wenn "timeout
check" nicht gesetzt ist. Um "Resonanz"-Effekte bei mehreren Servern auf derselben Hardware zu
verringern, werden die Agent- und Health Checks aller Server mit einem kleinen zeitlichen Versatz
zueinander gestartet. Mit dem globalen Schlüsselwort "spread-checks" kann den Intervallen der
Agent- und Health Checks außerdem eine zufällige Abweichung hinzugefügt werden. Das ist
beispielsweise sinnvoll, wenn viele Backends dieselben Server verwenden.

Siehe auch die Parameter "agent-check" und "agent-port".

<a id="entry-5-2-agent-addr"></a>

**`agent-addr <addr>`**

```haproxy
agent-addr <addr>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der Parameter "agent-addr" legt die Adresse für den Agent-Check fest.

Sie können den Agent-Check auf ein anderes Ziel auslagern und so Status und Gewichte der in HAProxy
definierten Server zentral verwalten, falls sich die Dienste nicht selbst überwachen und verwalten
können. Es kann sowohl eine IP-Adresse als auch ein Hostname angegeben werden; dieser wird aufgelöst.

<a id="entry-5-2-agent-port"></a>

**`agent-port <port>`**

```haproxy
agent-port <port>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der Parameter "agent-port" legt den TCP-Port für Agent-Checks fest.

Siehe auch die Parameter "agent-check" und "agent-inter".

<a id="entry-5-2-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Erlaubt beim Einsatz von TLS 1.3 das Senden früher Daten an den Server. Beachten Sie, dass frühe
Daten nur gesendet werden, wenn der Client frühe Daten verwendet hat oder das Backend "retry-on"
mit dem Schlüsselwort "0rtt-rejected" verwendet. Bei QUIC wird 0rtt von QuicTLS, OpenSSL \>= 3.5.2
und AWS-LC unterstützt. Bei TCP/TLS wird 0rtt nur von OpenSSL unterstützt.

<a id="entry-5-2-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Aktiviert die TLS-Erweiterung ALPN und bietet die angegebene Protokollliste über ALPN als unterstützt
an. Die Protokollliste besteht aus durch Kommas getrennten Protokollnamen, beispielsweise
"http/1.1,http/1.0" (ohne Anführungszeichen). Dafür muss die SSL-Bibliothek mit aktivierter
Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Die ALPN-Erweiterung
ersetzt die ursprüngliche NPN-Erweiterung. ALPN ist für Verbindungen zu HTTP/2-Servern erforderlich.
Sie ist auch erforderlich, um HTTP/3 über einen QUIC-Server verwenden zu können; für QUIC-Server
ohne "alpn"-Einstellung ist "h3" der Standardwert. OpenSSL-Versionen vor 1.0.2 unterstützten ALPN
nicht, sondern nur die inzwischen veraltete NPN-Erweiterung. Wenn sowohl HTTP/2 als auch HTTP/1.1
unterstützt werden sollen, können beide Versionen in der gewünschten Präferenzreihenfolge angeboten
werden, wie unten gezeigt:

```text
server 127.0.0.1:443 ssl crt pub.pem alpn h2,http/1.1
```

Siehe auch "ws", um eine alternative ALPN-Angabe für Websocket-Streams zu verwenden.

<a id="entry-5-2-backup"></a>

**`backup`**

```haproxy
backup
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Steht "backup" in einer server-Zeile, wird der Server nur dann für die Lastverteilung verwendet,
wenn alle anderen Server ohne backup-Option nicht verfügbar sind. Anfragen mit einem
Persistenz-Cookie, das auf diesen Server verweist, werden jedoch immer bedient. Standardmäßig wird
nur der erste betriebsbereite Backup-Server verwendet, sofern nicht die Option "allbackups" im
Backend gesetzt ist. Siehe auch die Optionen "no-backup" und "allbackups".

<a id="entry-5-2-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt
eine PEM-Datei an, aus der CA-Zertifikate zur Überprüfung des Serverzertifikats geladen werden.
Es kann auch ein Verzeichnis mit mehreren CAs geladen werden. In diesem Fall versucht HAProxy,
alle Dateien mit den Endungen ".pem", ".crt", ".cer" und ".crl" aus dem Verzeichnis zu laden.
Dateien, deren Name mit einem Punkt beginnt, werden ignoriert.

Um die vertrauenswürdigen CAs des Systems zu verwenden, kann anstelle der cafile der Parameter
"@system-ca" angegeben werden. Der Pfad dieses Verzeichnisses kann durch Setzen der
Umgebungsvariablen SSL_CERT_DIR überschrieben werden.

<a id="entry-5-2-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur auf Systemen verfügbar, die TCP_CONGESTION definieren, und wurde unter
Linux und FreeBSD geprüft. Sie nimmt den Namen eines TCP-Algorithmus zur Überlastkontrolle entgegen
und konfiguriert ausgehende Verbindungen für dessen Verwendung. Typische Namen sind "reno" und
"cubic"; die Auswahl hängt vom Betriebssystem ab. Auf manchen Systemen können für bestimmte
Algorithmen besondere Berechtigungen erforderlich sein. Unter Linux listet die Sysctl-Einstellung
"net.ipv4.tcp_available_congestion_control" die verfügbaren Algorithmen auf und
"net.ipv4.tcp_allowed_congestion_control" die ohne Privilegien zulässigen Algorithmen. Für
Algorithmen mit zusätzlichen Berechtigungsanforderungen kann die Capability "cap_net_admin"
erforderlich sein (siehe "setcap" im globalen Abschnitt). Kann ein bestimmter Algorithmus nicht
konfiguriert werden, bleibt der Standardalgorithmus unverändert. Siehe auch das bind-Schlüsselwort
"cc" ([Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1)).

<a id="entry-5-2-check"></a>

**`check`**

```haproxy
check
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option aktiviert Health Checks für einen Server: - Ist sie nicht gesetzt, werden keine
Health Checks durchgeführt und der Server gilt immer als verfügbar. - Ist sie gesetzt und keine
andere Prüfmethode konfiguriert, gilt der Server als verfügbar, wenn auf der höchsten konfigurierten
Transportschicht eine Verbindung aufgebaut werden kann. Standardmäßig ist dies TCP, bei gesetztem
"ssl" oder "check-ssl" dagegen SSL/TLS. Beides kann mit Verbindungspräfixen wie einem
PROXY-Protokoll-Header kombiniert werden, wenn "send-proxy" oder "check-send-proxy" gesetzt ist.
Für dynamische Server weicht dieses Verhalten etwas ab; Einzelheiten stehen in den folgenden
Absätzen. - Ist die Option gesetzt und ein Health Check auf Anwendungsebene definiert, wird der
Datenaustausch auf Anwendungsebene über der konfigurierten Transportschicht durchgeführt. Der Server
gilt als verfügbar, wenn der gesamte Datenaustausch erfolgreich ist.

Standardmäßig verwenden Health Checks dieselbe Adresse und denselben Port wie die
Serverkonfiguration sowie dieselben Kapselungsparameter (SSL/TLS, Proxy-Protokoll-Header usw.).
Die Zieladresse kann mit "addr" und der Port mit "port" geändert werden. In diesem Fall wird
angenommen, dass der Server nicht am Dienstport geprüft wird, und die konfigurierten
Kapselungsparameter werden nicht übernommen. Zum Senden von Verbindungsheadern muss "check-send-proxy"
explizit gesetzt werden, für SSL/TLS entsprechend "check-ssl".

Beachten Sie, dass für dynamische Server keine implizite Konfiguration von ssl und PROXY-Protokoll
erfolgt. Hier müssen "check-ssl" und "check-send-proxy" bei Bedarf explizit verwendet werden, selbst
wenn der Prüfport nicht überschrieben wird.

Wenn "sni" oder "alpn" in der server-Zeile gesetzt sind, werden ihre Werte nicht für Health Checks
verwendet; dafür müssen "check-sni" bzw. "check-alpn" verwendet werden.

Die standardmäßige Quelladresse für Health-Check-Datenverkehr entspricht der im Backend
definierten Adresse. Sie kann mit dem Schlüsselwort "source" geändert werden.

Das Intervall zwischen Prüfungen kann mit "inter" gesetzt werden. Mit "rise" und "fall" kann
festgelegt werden, wie viele erfolgreiche bzw. fehlgeschlagene Health Checks erforderlich sind,
um einen Server als verfügbar bzw. nicht verfügbar zu markieren.

Optionale Health Checks auf Anwendungsebene können mit "option httpchk", "option
mysql-check", "option smtpchk", "option pgsql-check", "option ldap-check" oder "option redis-check"
konfiguriert werden.

Beispiel:

```shell
# simple tcp check
backend foo
  server s1 192.168.0.1:80 check
# this does a tcp connect + tls handshake
backend foo
  server s1 192.168.0.1:443 ssl check
# simple tcp check is enough for check success
backend foo
  option tcp-check
  tcp-check connect
  server s1 192.168.0.1:443 ssl check
```

<a id="entry-5-2-check-reuse-pool"></a>

**`check-reuse-pool`**

```haproxy
check-reuse-pool
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option erlaubt Prüfungen, vorhandene ungenutzte Verbindungen wiederzuverwenden, anstatt eine
eigene Verbindung zu öffnen. Nach Abschluss der Prüfung wird die Verbindung wieder in den Pool
aufgenommen. Das Hauptziel ist, die Anzahl der Verbindungsaufbauten und -schließungen zu einem
bestimmten Server zu begrenzen. Diese Funktion ist nur mit http-check-Regelsätzen kompatibel.
Bei anderen Prüftypen wird sie ohne Meldung ignoriert. Außerdem sollte die Wiederverwendungsrichtlinie
im Backend auf aggressive gesetzt sein, da jeder Prüfversuch in einer eigenen Sitzung erfolgt.

Zur Vereinfachung der Konfiguration wird diese Option ohne Meldung ignoriert, wenn eine spezielle
Verbindungsoption für Prüfungen definiert ist, entweder in der server-Zeile oder über eine
benutzerdefinierte Regel tcp-check connect.

Diese Option wird automatisch für Server aktiviert, die als passives Reverse-HTTP-Gateway dienen,
da bei diesen Servern ein Verbindungsaufbau nur durch Wiederverwendung unterstützt wird.

Siehe auch: "check-pool-conn-name"

<a id="entry-5-2-check-send-proxy"></a>

**`check-send-proxy`**

```haproxy
check-send-proxy
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option erzwingt das Senden einer PROXY-Protokollzeile bei ausgehenden Health Checks,
unabhängig davon, ob der Server send-proxy für den normalen Datenverkehr verwendet. Standardmäßig
ist das PROXY-Protokoll für Health Checks aktiviert, wenn es bereits für den normalen Datenverkehr
aktiviert ist und weder eine "port"- noch eine "addr"-Direktive vorhanden ist. Ist eine solche
Direktive vorhanden, muss jedoch "check-send-proxy" verwendet werden, um die Verwendung des
Protokolls zu erzwingen. Weitere Informationen finden Sie bei der Option "send-proxy".

<a id="entry-5-2-check-alpn"></a>

**`check-alpn <protocols>`**

```haproxy
check-alpn <protocols>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Legt fest, welche Protokolle über ALPN angeboten werden. Die Protokollliste besteht aus durch
Kommas getrennten Protokollnamen, beispielsweise "http/1.1,http/1.0" (ohne Anführungszeichen).
Ist dies nicht gesetzt, wird die ALPN-Einstellung des Servers verwendet.

<a id="entry-5-2-check-pool-conn-name"></a>

**`check-pool-conn-name <name>`**

```haproxy
check-pool-conn-name <name>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Wenn für Prüfungen Verbindungen wiederverwendet werden, wird `<name>`, sofern gesetzt, als
Verbindungskennung verwendet, um eine passende Verbindung im Pool zu finden. Dies entspricht dem
Server-Schlüsselwort "pool-conn-name". Wird diese Option nicht verwendet, dient auch "check-sni"
als Rückfallwert.

Siehe auch: "check-reuse-pool"

<a id="entry-5-2-check-proto"></a>

**`check-proto <name>`**

```haproxy
check-proto <name>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Erzwingt das Multiplexer-Protokoll für die Health-Check-Verbindungen des Servers. Es muss mit dem
Health-Check-Typ (TCP oder HTTP) kompatibel und auf der Backend-Seite verwendbar sein. Die Liste
verfügbarer Protokolle wird von haproxy -vv ausgegeben. Angezeigt werden die Protokolleigenschaften:
der Modus (TCP/HTTP), die Seite (FE/BE), der Name des Multiplexers und seine Flags.

Bei manchen Protokollen kann auf der Serverseite Head-of-Line-Blocking auftreten (flag=HOL_RISK).
Einige Protokolle unterstützen außerdem keine Upgrades (flag=NO_UPG). Auch die HTX-Kompatibilität
wird angegeben (flag=HTX).

Die folgenden Protokolle können als Argument einer "check-proto"-Direktive in einer server-Zeile
verwendet werden:

```text
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

Mit dieser Option wird die Auswahl des am besten geeigneten Multiplexer-Protokolls für
Health-Check-Verbindungen zu diesem Server umgangen. Ist sie nicht definiert, wird das Protokoll
des Servers verwendet, sofern es gesetzt ist.

Wenn ALPN oder NPN konfiguriert ist, sollten die angegebenen Protokolle mit dem Multiplexer-Protokoll
kompatibel sein, um Probleme zu vermeiden. Ist beispielsweise "proto h1" gesetzt, sollte ALPN nicht
auf "h2" gesetzt werden.

Die Konfiguration von QUIC-Prüfungen ist noch nicht vollständig implementiert. Erstens können
QUIC-Prüfungen nur für QUIC-Server durchgeführt werden. Zweitens fällt das Prüfprotokoll auf TCP
zurück, wenn für einen QUIC-Server mindestens ein prüfungsspezifischer Verbindungsparameter
angegeben ist.

<a id="entry-5-2-check-sni-auto"></a>

**`check-sni-auto`**

```haproxy
check-sni-auto
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option aktiviert die automatische SNI-Auswahl bei Health Checks über SSL, sofern noch kein
Wert gesetzt wurde. Sie ist standardmäßig aktiviert. Als "server"-Einstellung kann dieser Parameter
jedoch eine über die Direktive "default-server" geerbte Standardeinstellung "no-check-sni-auto"
zurücksetzen. Er kann auch als "default-server"-Einstellung verwendet werden, um eine frühere
"no-check-sni-auto"-Einstellung aus "default-server" zurückzusetzen.

Für HTTPS-Verbindungen wird die SNI automatisch ausgewählt, allerdings nur, wenn keine Regel
"http-check
connect" vorhanden ist. In diesem Fall richtet sich die SNI nach dem Wert des Host-Headers, der
über "option httpchk" oder eine Regel "http-check send" angegeben wurde. Für Regeln "http-check connect"
erfolgt keine automatische Auswahl. Bei anderen Protokollen wird die Option ignoriert.

Wenn die automatische SNI-Auswahl für Health Checks verwendet wird und "check-reuse-pool" gesetzt
ist, wird der Wert dem Verbindungsnamen zugewiesen, sofern er nicht durch das Server-Schlüsselwort
"check-pool-conn-name" überschrieben wird.

Siehe die Option "sni-auto", um die automatische SNI-Auswahl für weitergeleiteten Datenverkehr
zu aktivieren.

<a id="entry-5-2-check-sni"></a>

**`check-sni <sni>`**

```haproxy
check-sni <sni>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Mit dieser Option wird die SNI für Health Checks über SSL angegeben. `<sni>` kann nur mit einer
Zeichenfolge gesetzt werden. Soll die SNI für weitergeleiteten Datenverkehr gesetzt werden, siehe
"sni".

<a id="entry-5-2-check-ssl"></a>

**`check-ssl`**

```haproxy
check-ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option erzwingt die SSL-Verschlüsselung aller Health Checks, unabhängig davon, ob der Server
SSL für den normalen Datenverkehr verwendet. Sie wird üblicherweise verwendet, wenn explizit eine
"port"- oder "addr"-Direktive angegeben ist und SSL-Health-Checks deshalb nicht geerbt werden.
Dabei ist wichtig, dass diese Option eine SSL-Transportschicht unter den Prüfungen einfügt: Aus
einer einfachen TCP-Verbindungsprüfung wird damit eine SSL-Verbindungsprüfung, die das frühere
ssl-hello-chk ersetzt. Am häufigsten wird "httpchk" mit SSL-Prüfungen kombiniert, um HTTPS-Prüfungen
zu senden. Alle SSL-Einstellungen gelten gemeinsam für Health Checks und Datenverkehr (z. B.
Ciphers). Weitere Informationen finden Sie bei "ssl"; mit "no-check-ssl" wird diese Option
deaktiviert.

<a id="entry-5-2-check-via-socks4"></a>

**`check-via-socks4`**

```haproxy
check-via-socks4
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option aktiviert ausgehende Health Checks über einen vorgeschalteten socks4-Proxy.
Standardmäßig durchlaufen Health Checks den socks-Tunnel nicht, auch wenn er für normalen
Datenverkehr aktiviert ist.

<a id="entry-5-2-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der Verschlüsselungsalgorithmen fest, die beim SSL/TLS-Handshake mit
dem Server ausgehandelt werden. Das Format ist in "man 1 ciphers" in den OpenSSL-Handbuchseiten
beschrieben. Hintergrundinformationen und Empfehlungen finden Sie beispielsweise unter
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) und
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Zur Konfiguration der
Verschlüsselungsalgorithmen für TLSv1.3 siehe das Schlüsselwort "ciphersuites".

<a id="entry-5-2-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde und
HAProxy mit OpenSSL 1.1.1 oder neuer gebaut wurde. Sie legt die Zeichenfolge mit der Liste der
Verschlüsselungsalgorithmen fest, die beim TLS-1.3-Handshake mit dem Server ausgehandelt werden.
Das Format ist in "man
1 ciphers" in den OpenSSL-Handbuchseiten im Abschnitt "ciphersuites" beschrieben. Zur Konfiguration
der Verschlüsselungsalgorithmen für TLSv1.2 und älter siehe das Schlüsselwort "ciphers".

<a id="entry-5-2-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der auszuhandelnden Signaturalgorithmen für die Client-Authentifizierung
fest. Das Format ist in "man 3 SSL_CTX_set1_client_sigalgs" in den OpenSSL-Handbuchseiten beschrieben.
Von dieser Einstellung wird abgeraten, sofern kein konkreter Anwendungsfall dafür besteht.

<a id="entry-5-2-cookie"></a>

**`cookie <value>`**

```haproxy
cookie <value>
```

Kann in folgenden Kontexten verwendet werden: http

Der Parameter "cookie" setzt den dem Server zugeordneten Cookie-Wert auf `<value>`. Dieser Wert
wird in eingehenden Anfragen geprüft; ausgewählt wird der erste betriebsbereite Server mit demselben
Wert. Im Gegenzug wird dieser Wert im Modus zum Einfügen oder Umschreiben von Cookies dem Cookie
zugewiesen, das an den Client gesendet wird. Mehrere Server können problemlos denselben Cookie-Wert
verwenden; bei normalen und Backup-Servern ist dies sogar recht üblich. Siehe auch das Schlüsselwort
"cookie" im Backend-Abschnitt.

<a id="entry-5-2-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt
eine PEM-Datei an, aus der die Zertifikatssperrliste zur Überprüfung des Serverzertifikats geladen
wird.

<a id="entry-5-2-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie gibt
eine PEM-Datei an, aus der sowohl ein Zertifikat als auch der zugehörige private Schlüssel geladen
werden. Die Datei kann durch Aneinanderhängen beider PEM-Dateien erzeugt werden. Dieses Zertifikat
wird gesendet, wenn der Server ein Client-Zertifikat anfordert.

Enthält die Datei keinen privaten Schlüssel, versucht HAProxy, den Schlüssel vom selben Pfad mit
der angehängten Endung ".key" zu laden (sofern "ssl-load-extra-files" entsprechend gesetzt ist).

<a id="entry-5-2-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt die Zeichenfolge fest, die die Liste der elliptischen Kurvenalgorithmen ("Kurvensuite") beschreibt, die während des SSL/TLS-Handshakes mit ECDHE vereinbart werden. Das Format der Zeichenfolge ist eine durch Doppelpunkte getrennte Liste von Kurvennamen. Beispiel: "X25519:P-256" (ohne Anführungszeichen)

<a id="entry-5-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Das Schlüsselwort "disabled" startet den Server im Zustand "disabled". Das bedeutet, dass er im Wartungsmodus als down markiert ist, und keine Verbindung außer denjenigen, die durch den Persistenzmodus erlaubt sind, erreicht ihn. Es eignet sich sehr gut zum Einrichten neuer Server, da normaler Datenverkehr sie niemals erreichen wird, während es dennoch möglich ist, den Dienst über den force-persist-Mechanismus zu testen. Siehe auch die "enabled"-Einstellung.

<a id="entry-5-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als 'server'-Einstellung verwendet werden, um jede 'disabled'-Einstellung zurückzusetzen, die als Standardwert von der 'default-server'-Anweisung geerbt wurde. Sie kann auch als 'default-server'-Einstellung verwendet werden, um jede vorherige 'default-server' 'disabled'-Einstellung zurückzusetzen.

<a id="entry-5-2-error-limit"></a>

**`error-limit <count>`**

```haproxy
error-limit <count>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Wenn die Zustandsüberwachung aktiviert ist, legt der "error-limit"-Parameter die Anzahl aufeinanderfolgender Fehler fest, die ein Ereignis auslösen, das durch die "on-error"-Option ausgewählt wurde. Standardmäßig ist dieser Wert auf 10 aufeinanderfolgende Fehler festgelegt.

Siehe auch "check", "error-limit" und "on-error".

<a id="entry-5-2-fall"></a>

**`fall <count>`**

```haproxy
fall <count>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der "fall"-Parameter legt fest, dass ein Server nach `<count>` aufeinanderfolgenden fehlgeschlagenen Health Checks als ausgefallen gilt. Ohne Angabe beträgt dieser Wert standardmäßig 3. Siehe auch die Parameter "check", "inter" und "rise".

<a id="entry-5-2-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die ausschließliche Verwendung von SSLv3, wenn die Kommunikation mit dem Server über SSL erfolgt. SSLv3 ist im Allgemeinen weniger kostspielig als die TLS-Gegenstücke bei hohen Verbindungsraten. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver" und ssl-max-ver".

<a id="entry-5-2-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die ausschließliche Verwendung von TLSv1.0, wenn die Kommunikation mit dem Server über SSL erfolgt. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver" und ssl-max-ver".

<a id="entry-5-2-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die ausschließliche Verwendung von TLSv1.1, wenn die Kommunikation mit dem Server über SSL erfolgt. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver" und ssl-max-ver".

<a id="entry-5-2-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die ausschließliche Verwendung von TLSv1.2, wenn die Kommunikation mit dem Server über SSL erfolgt. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver" und ssl-max-ver".

<a id="entry-5-2-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die ausschließliche Verwendung von TLSv1.3, wenn die Kommunikation mit dem Server über SSL erfolgt. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver" und ssl-max-ver".

<a id="entry-5-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Geben Sie eine global eindeutige ID, bei der Groß- und Kleinschreibung unterschieden wird, für diesen Server an. Diese ID muss innerhalb der gesamten haproxy-Konfiguration über alle Objekttypen hinweg eindeutig sein. Weitere Informationen zum Format finden Sie in der Beschreibung des Proxy-Schlüsselworts "guid". Siehe auch "shm-stats-file".

<a id="entry-5-2-hash-key"></a>

**`hash-key <key>`**

```haproxy
hash-key <key>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Geben Sie an, wie "hash-type consistent"-Knotenschlüssel berechnet werden.

Argumente:

```text
<key>   <key> kann einen der folgenden Werte haben:

  id         Die Knotenschlüssel werden aus dem numerischen Bezeichner
             des Servers abgeleitet, der mit "id" festgelegt wird oder
             standardmäßig seiner Position in der Serverliste entspricht.
             Dies ist die Standardeinstellung. Es werden nur die 20
             niedrigsten Bits der ID verwendet (also (id % 1048576)).
             Um Überschneidungen zu vermeiden, sollten daher nur Werte
             zwischen 1 und diesem Wert verwendet werden.

  id32       Die Knotenschlüssel werden aus dem numerischen Bezeichner
             des Servers abgeleitet, der mit "id" festgelegt wird oder
             standardmäßig seiner Position in der Serverliste entspricht.
             Hier werden jedoch alle 32 Bits der ID verwendet, sodass
             keine Kollision entsteht. Dieser Wert wird nicht wie "id"
             skaliert. Daher empfiehlt es sich, ihn stets entweder mit
             einer Hashfunktion (siehe "hash-key") oder mit explizit
             zugewiesenen ID-Werten zu verwenden, die gleichmäßig über
             den 32-Bit-Raum verteilt sind.

  guid       Die Knotenschlüssel werden aus der guid des Servers
             abgeleitet, sofern vorhanden; andernfalls wird auf "id"
             zurückgegriffen. Der Vorteil ist, dass dies überhaupt nicht
             von der Reihenfolge abhängt, sondern nur von einem internen,
             stabilen Bezeichner, der auf vielen Load-Balancern
             repliziert werden kann.

  addr       Die Knotenschlüssel werden aus der Adresse des Servers
             abgeleitet, sofern vorhanden; andernfalls wird auf "id"
             zurückgegriffen.

  addr-port  Die Knotenschlüssel werden aus Adresse und Port des Servers
             abgeleitet, sofern vorhanden; andernfalls wird auf "id"
             zurückgegriffen.
```

Die Optionen "addr" und "addr-port" können in Szenarien nützlich sein, in denen mehrere HAProxy-Prozesse den Datenverkehr an die gleiche Gruppe von Servern verteilen. Wenn die Serverreihenfolge jedes Prozesses unterschiedlich ist (z. B. weil DNS-Einträge in unterschiedlicher Reihenfolge aufgelöst wurden), ermöglicht dies jedem unabhängigen HAProxy-Prozess, sich auf Routing-Entscheidungen zu einigen. Hinweis: "balance random" verwendet ebenfalls "hash-type consistent", und die Qualität der Verteilung hängt von der Qualität der Schlüssel ab.

<a id="entry-5-2-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Geben Sie den Health-Check-Abschnitt an, der zum Durchführen des Checks auf dem Server verwendet werden soll.

Argument:

```text
<name>    ist der Name des health-check-Abschnitts.
```

Dank dieser Option ist es möglich, eine serverspezifische Health-Check-Konfiguration anstelle der Proxy-Konfiguration zu verwenden. Siehe auch "healthcheck section".

<a id="entry-5-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Legen Sie eine persistente ID für den Server fest. Diese ID muss eine positive Zahl mit 32 Bit sein und innerhalb des Proxys eindeutig sein. Wenn nicht gesetzt, wird automatisch eine nicht verwendete ID zugewiesen. Der erste zugewiesene Wert ist 1. Diese ID wird derzeit nur in der Statistik zurückgegeben und wird verwendet, um bei konsistenten Hash-Algorithmen LB-Knoten zu platzieren, wenn "hash-key" auf "id" (Standard) gesetzt ist. In diesem Fall werden nur die 20 niedrigsten Bits des Werts verwendet (d. h. (id % 1048576)), sodass es besser ist, Werte im Bereich zwischen 1 und diesem Wert zu verwenden, um Überlappungen zu vermeiden.

<a id="entry-5-2-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Definieren Sie ein Intervall für regelmäßige Erreichbarkeitsprüfungen bei ungenutzten Backend-Verbindungen. Wenn die Gegenstelle vor der nächsten geplanten Prüfung nicht antwortet, wird die Verbindung geschlossen. Dieses Schlüsselwort bezieht sich auf die Backend-Seite, sodass es nützlich ist, um sicherzustellen, dass ungenutzte Verbindungen weiterhin verwendbar sind. Beachten Sie, dass dies das Schließen der Verbindung beim Bereinigen des Pools ungenutzter Verbindungen nicht verhindert.

Diese Funktion basiert auf spezifischer Protokollunterstützung. Derzeit wird sie nur vom H2-Multiplexer unterstützt. Idle-ping wird von anderen Protokollen einfach ignoriert.

Diese Option ist besonders bei Reverse HTTP nützlich. In der server-Zeile hilft sie der
Gegenstelle, die auf eingehende Verbindungen lauscht und diese einem passenden Server zuordnet,
damit sie später zur Weiterleitung von Datenverkehr wiederverwendet werden können.

<a id="entry-5-2-init-addr"></a>

**`init-addr {last | libc | none | <ip>},[...]*`**

```haproxy
init-addr {last | libc | none | <ip>},[...]*
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Gibt an, in welcher Reihenfolge die Serveradresse beim Start aufgelöst werden soll, wenn sie einen
FQDN verwendet. Die Methoden der durch Kommas getrennten Liste werden nacheinander zur Auflösung
angewendet. Verwendet wird die erste erfolgreiche Methode. Wird das Listenende ohne erfolgreiche
Methode erreicht, wird ein Fehler ausgelöst. Die Methode "last" verwendet die im Statusdatei
angegebene Adresse (siehe "server-state-file"). "libc" verwendet den internen Resolver der libc
(gethostbyname() oder getaddrinfo(), abhängig von Betriebssystem und Build-Optionen). Die Methode
"none" gibt ausdrücklich an, dass der Server ohne gültige IP-Adresse im Zustand down starten soll.
Dies kann nützlich sein, um DNS-Probleme beim Start zu ignorieren und auf ihre spätere Behebung zu
warten. Schließlich kann auch eine IP-Adresse (IPv4 oder IPv6) angegeben werden. Das kann die
aktuell bekannte Serveradresse sein (z. B. von einem Konfigurationsgenerator eingetragen) oder die
Adresse eines Dummy-Servers, der alte Sitzungen abfängt und ihnen beispielsweise eine verständliche
Fehlermeldung liefert. Beim Lastverteilungsalgorithmus "first" könnte die IP-Adresse auf einen
Dummy-Server verweisen, der bei Bedarf die Erzeugung neuer Instanzen auslöst. Der Standardwert ist
"last,libc": Zunächst wird die frühere Adresse aus dem Statusdatei verwendet, sofern vorhanden,
andernfalls der Resolver der libc. Dies erhält die Kompatibilität mit dem bisherigen Verhalten.
Bei internen Resolvern wird allgemein empfohlen, die libc-basierte Auflösung entweder zu
deaktivieren oder explizit zu machen (Einzelheiten in [Abschnitt 5.3](/de/haproxy/bind-and-server-options/#section-5-3)).

Beispiel 1:

```text
defaults
    # never fail on address resolution
    default-server init-addr last,libc,none
```

Beispiel 2:

```text
defaults
    # disable libc resolution in combination with resolvers
    default-server init-addr last,none
```

<a id="entry-5-2-inter"></a>

**`inter <delay>`**

```haproxy
inter <delay>
fastinter <delay>
downinter <delay>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der Parameter "inter" setzt das Intervall zwischen zwei aufeinanderfolgenden Health Checks auf
`<delay>` Millisekunden. Ist er nicht angegeben, beträgt das Intervall standardmäßig 2000 ms.
Mit "fastinter" und "downinter" können die Prüfintervalle außerdem abhängig vom Serverzustand
optimiert werden:

```text
             Serverzustand                  |         Verwendetes Intervall
    ----------------------------------------+----------------------------------
     UP 100% (kein Übergangszustand)         | "inter"
    ----------------------------------------+----------------------------------
     UP im Übergang (zu DOWN, "fall"),       | "fastinter", falls gesetzt,
     DOWN im Übergang (zu UP, "rise"),       | andernfalls "inter".
     oder noch nicht geprüft.               |
    ----------------------------------------+----------------------------------
     DOWN 100% (kein Übergangszustand)       | "downinter", falls gesetzt,
                                            | andernfalls "inter".
    ----------------------------------------+----------------------------------
```

Wie bei allen zeitbasierten Parametern kann explizit eine andere Einheit aus { us, ms, s, m, h, d }
angegeben werden. Der Parameter "inter" dient auch als Zeitüberschreitung für Health Checks an
Server, wenn "timeout check" nicht gesetzt ist. Um "Resonanz"-Effekte bei mehreren Servern auf
derselben Hardware zu verringern, werden die Agent- und Health Checks aller Server mit einem kleinen
zeitlichen Versatz zueinander gestartet. Mit dem globalen Schlüsselwort "spread-checks" kann den
Intervallen der Agent- und Health Checks außerdem eine zufällige Abweichung hinzugefügt werden.
Das ist beispielsweise sinnvoll, wenn viele Backends dieselben Server verwenden. Ist die globale
Einstellung "tune.max-checks-per-thread" auf einen Wert ungleich null gesetzt, begrenzt sie die
Anzahl gleichzeitig ausgeführter Prüfungen pro Thread. Dazu stellt haproxy Prüfungen, die auf einem
Thread mit bereits erreichtem Limit starten sollten, in eine Warteschlange, bis eine andere Prüfung
endet. Dadurch verlängert sich das tatsächliche Prüfintervall. In diesem Fall hat eine Verringerung
von "inter" nur eine sehr begrenzte Wirkung, da sie die Wartezeit in der Warteschlange nicht
verkürzen kann.

<a id="entry-5-2-init-state"></a>

**`init-state { fully-up | up | down | fully-down | none }`**

```haproxy
init-state { fully-up | up | down | fully-down | none }
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Die Option "init-state" setzt den anfänglichen Serverzustand: - Bei 'fully-up' gilt der Server
sofort als verfügbar. Sind Health Checks für diesen Server aktiviert, wechselt er in den Zustand
DOWN, wenn ALLE Health Checks fehlschlagen. - Bei 'up' gilt der Server sofort als verfügbar. Sind
Health Checks aktiviert, wechselt er sofort nach der nächsten fehlgeschlagenen Prüfung in den
Zustand DOWN. - Bei 'down' gilt der Server zunächst als nicht verfügbar. Sind Health Checks
aktiviert, kann er nach der nächsten erfolgreichen Prüfung in den Zustand UP wechseln. - Bei
'fully-down' gilt der Server zunächst als nicht verfügbar. Sind Health Checks aktiviert, wechselt
er in den Zustand UP, wenn ALLE Health Checks erfolgreich sind. - Bei 'none' (dem Standardwert)
ist die Verwaltung von init-state deaktiviert. Damit kann das Standardverhalten wiederhergestellt
werden, wenn der Parameter von einer 'default-server'-Direktive geerbt wurde.

Der init-state eines Servers wird berücksichtigt, wenn die HAProxy-Instanz (neu) gestartet wird,
ein neuer Server erkannt wird (beispielsweise durch Diensterkennung / DNS-Auflösung), ein dynamischer
Server aktiviert wird, ein Server den Wartungsmodus verlässt usw. Diese Direktive kann nicht
verwendet werden, wenn der Server einen anderen Server verfolgt.

Beispiele:

```shell
# pass client traffic ONLY to Redis "master" node
backend redis-master
  mode tcp
  balance first
  option tcp-check
  tcp-check send role\r\n
  tcp-check expect string master
  server-template redis 3 _redis._tcp.redis-headless-service.sandbox.svc.cluster.local:6379 check ... init-state down

# pass traffic to the server only after 3 successful health checks
backend google-backend
  mode http
  server srv1 google.com:80 check init-state fully-down rise 3
  server srv2 google.com:80 check init-state fully-down rise 3
```

Siehe auch: "option tcp-check", "option httpchk"

<a id="entry-5-2-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Aktiviert oder deaktiviert ktls für diese Sockets. Wenn aktiviert, wird kTLS verwendet, sofern der
Kernel dies unterstützt und der Verschlüsselungsalgorithmus kompatibel ist. Dies ist nur unter
Linux ab 4.17 verfügbar. Beachten Sie, dass einige Netzwerktreiber und/oder TLS-Stacks die
Verwendung von kTLS auf TLS v1.2 beschränken können. Siehe auch "force-tlsv12".

<a id="entry-5-2-log-bufsize"></a>

**`log-bufsize <bufsize>`**

```haproxy
log-bufsize <bufsize>
```

Kann in folgenden Kontexten verwendet werden: log

"log-bufsize" legt die Größe des Ringpuffers für den impliziten Ring fest, der dem Log-Server in
einem Log-Backend zugeordnet wird. Ohne Angabe gilt der Standardwert BUFSIZE. Ein größerer Wert
erhöht den Speicherverbrauch, kann bei langsamen Servern aber den Verlust von Protokollmeldungen
verhindern helfen, da mehr ausstehende Meldungen im Puffer Platz finden. Dieses Schlüsselwort darf
nur in Log-Backend-Abschnitten (mit "mode log") verwendet werden.

<a id="entry-5-2-log-proto"></a>

**`log-proto <logproto>`**

```haproxy
log-proto <logproto>
```

Kann in folgenden Kontexten verwendet werden: log, ring

"log-proto" legt das Protokoll zur Weiterleitung von Ereignismeldungen an einen Server fest, der
in einem log- oder ring-Abschnitt konfiguriert ist. Mögliche Werte sind "legacy" und "octet-count";
sie entsprechen "Non-transparent-framing" bzw. "Octet counting" in rfc6587. Der Standardwert ist
"legacy".

<a id="entry-5-2-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "maxconn" gibt die maximale Anzahl gleichzeitiger Verbindungen zu diesem Server an.
Übersteigt die Anzahl gleichzeitig eingehender Verbindungen diesen Wert, werden sie in eine
Warteschlange gestellt, bis ein Platz frei wird. Dieser Parameter ist sehr wichtig, da er empfindliche
Server bei extremer Last vor dem Ausfall bewahren kann. Ist "minconn" angegeben, wird die Grenze
dynamisch. Der Standardwert "0" bedeutet unbegrenzt. Siehe auch "minconn", "maxqueue" und das
Backend-Schlüsselwort "fullconn".

Im HTTP-Modus begrenzt dieser Parameter die Anzahl gleichzeitiger Anfragen statt der Verbindungen.
Mehrere Anfragen können über eine einzige TCP-Verbindung zum Server multiplexiert werden. Bei einem
maxconn-Wert von 50 können beispielsweise zwischen 1 und 50 tatsächliche Serververbindungen
bestehen, aber höchstens 50 gleichzeitige Anfragen.

<a id="entry-5-2-maxqueue"></a>

**`maxqueue <maxqueue>`**

```haproxy
maxqueue <maxqueue>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "maxqueue" gibt die maximale Anzahl von Verbindungen an, die in der Warteschlange
für diesen Server warten. Ist diese Grenze erreicht, werden weitere Anfragen auf andere Server
umverteilt, anstatt unbegrenzt auf Bedienung zu warten. Das unterbricht die Persistenz, kann
Benutzern aber eine schnelle erneute Anmeldung ermöglichen, wenn der gewünschte Server ausfällt.
Einige Lastverteilungsalgorithmen wie leastconn berücksichtigen dies und nehmen bis zu dieser Grenze
Anfragen in die Serverwarteschlange auf, wenn der Wert explizit auf einen Wert größer als null
gesetzt ist. Gerade bei einstelligen maxconn-Werten lässt sich die Last damit häufig besser glätten.
Der Standardwert "0" bedeutet eine unbegrenzte Warteschlange. Siehe auch die Parameter "maxconn"
und "minconn" sowie "balance leastconn".

<a id="entry-5-2-max-reuse"></a>

**`max-reuse <count>`**

```haproxy
max-reuse <count>
```

Kann in folgenden Kontexten verwendet werden: http, ring

Bei Verwendung im http-Kontext:

Das Argument "max-reuse" weist die HTTP-Verbindungsverarbeitung an, eine Serververbindung höchstens
so oft für neue Anfragen wiederzuverwenden. Zulässig sind -1 (der Standardwert), wodurch die Grenze
deaktiviert wird, oder ein positiver Wert. Der Wert null deaktiviert Keep-Alive effektiv. Dies dient
ausschließlich dazu, bestimmte Serverfehler zu umgehen, die mit der Zeit Ressourcenlecks verursachen.
Die unteren Schichten halten sich nicht zwingend an dieses Argument, da technische Einschränkungen
dessen Durchsetzung unmöglich machen können. Zumindest HTTP/2-Verbindungen zu Servern beachten es.

Bei Verwendung im ring-Kontext:

Das Argument "max-reuse" weist die TCP-Verbindungsverarbeitung der Senke an, eine Serververbindung
höchstens so oft zum Senden von Meldungen wiederzuverwenden. Die Verbindung zum Server wird also
zwangsweise abgebaut, sobald mindestens "max-reuse + 1" Meldungen über dieselbe Verbindung
verarbeitet wurden. Anschließend wird sie automatisch neu aufgebaut. Bei vielen Meldungen im
Multithread-Betrieb kann dies helfen, die Last des Rings besser auf mehrere Threads zu verteilen.
Eine Verbindung bleibt nämlich während ihrer gesamten Lebensdauer an denselben CPU-Thread gebunden:
Anders als bei HTTP gibt es keine Syslog-Transaktionen. Daher könnte die Serververbindung unbegrenzt
bestehen bleiben, solange der Server sie nicht schließt und kein Netzwerkfehler auftritt. Durch
gelegentliches Abbauen der Verbindungen erhalten andere Threads die Möglichkeit, ihrerseits einige
Meldungen zu übernehmen. Dies kann auch einen geordneten Wechsel von Log-Servern unterstützen, wenn
zwischen haproxy und den Log-Servern eine zusätzliche Lastverteilungsschicht liegt. Bedenken Sie
jedoch, dass bei jeder Verbindungserneuerung ein ausgehender Port im Zustand TIME_WAIT verbleibt,
der auf modernen Betriebssystemen etwa eine Minute lang nicht wiederverwendet werden kann.
Deshalb muss auf ausreichend hohe Werte geachtet werden, damit die Quellports nicht schnell
erschöpft sind. Als Faustregel gilt: Schließen Sie Verbindungen niemals häufiger als einige Male pro Sekunde
und vorzugsweise deutlich seltener. Zulässig sind -1 (der Standardwert), wodurch
die Grenze deaktiviert wird, oder ein positiver Wert. Anders als im HTTP-Kontext wird "max-reuse"
bei Senkenservern nur nach Möglichkeit eingehalten: Meldungen des Rings werden in Stapeln
verarbeitet, und die Grenze wird zwischen den Stapeln geprüft.

<a id="entry-5-2-minconn"></a>

**`minconn <minconn>`**

```haproxy
minconn <minconn>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Wenn "minconn" gesetzt ist, wird maxconn zu einer dynamischen Grenze, die der Backend-Last folgt.
Der Server akzeptiert immer mindestens `<minconn>` Verbindungen und nie mehr als `<maxconn>`.
Hat das Backend weniger als `<fullconn>` gleichzeitige Verbindungen, verläuft die Grenze linear zwischen
beiden Werten. So lässt sich die Serverlast bei normaler Auslastung begrenzen und bei hoher
Last stärker erhöhen, ohne den Server bei außergewöhnlich hoher Last zu überlasten. Siehe auch
"maxconn", "maxqueue" und das Backend-Schlüsselwort "fullconn".

<a id="entry-5-2-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Unter Linux kann festgelegt werden, welchem Netzwerknamensraum ein Socket angehört. Mit dieser
Direktive kann ein Server explizit an einen anderen Namensraum als den Standardnamensraum gebunden
werden. Weitere Informationen zu Netzwerknamensräumen finden Sie in der Dokumentation Ihres
Betriebssystems.

<a id="entry-5-2-no-agent-check"></a>

**`no-agent-check`**

```haproxy
no-agent-check
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "agent-check" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "agent-check"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-backup"></a>

**`no-backup`**

```haproxy
no-backup
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "backup" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "backup"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-check"></a>

**`no-check`**

```haproxy
no-check
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "check" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "check"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-check-reuse-pool"></a>

**`no-check-reuse-pool`**

```haproxy
no-check-reuse-pool
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option hebt eine frühere Einstellung "check-reuse-pool" auf, die möglicherweise von
"default-server" geerbt wurde. Jede Prüfung wird über ihre eigene Verbindung durchgeführt.

<a id="entry-5-2-no-check-sni-auto"></a>

**`no-check-sni-auto`**

```haproxy
no-check-sni-auto
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als "server"-Einstellung verwendet werden, um die standardmäßig aktivierte
automatische SNI-Auswahl für SSL-Health-Checks zu deaktivieren.

Siehe "no-sni-auto", um die automatische SNI-Auswahl für weitergeleiteten Datenverkehr zu
deaktivieren.

<a id="entry-5-2-no-check-ssl"></a>

**`no-check-ssl`**

```haproxy
no-check-ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "check-ssl" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "check-ssl"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-renegotiate"></a>

**`no-renegotiate`**

```haproxy
no-renegotiate
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert für das betreffende SSL-Backend die Mechanismen zur Neuverhandlung, sowohl den alten
unsicheren als auch die neuere "secure renegotiation" (RFC 5746 TLS Renegotiation Indication
Extension). Diese Option ist auch in der globalen Anweisung "ssl-default-server-options" verfügbar.
In TLS 1.3 ist keine Neuverhandlung mehr möglich. Sind weder "renegotiate" noch "no-renegotiate"
angegeben, bleibt das Standardverhalten der SSL-Bibliothek erhalten. Beispielsweise aktiviert
OpenSSL standardmäßig die sichere Neuverhandlung, während AWS-LC sie deaktiviert. Siehe auch
"renegotiate".

<a id="entry-5-2-no-send-proxy"></a>

**`no-send-proxy`**

```haproxy
no-send-proxy
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "send-proxy" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "send-proxy"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-send-proxy-v2"></a>

**`no-send-proxy-v2`**

```haproxy
no-send-proxy-v2
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "send-proxy-v2" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "send-proxy-v2"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-send-proxy-v2-ssl"></a>

**`no-send-proxy-v2-ssl`**

```haproxy
no-send-proxy-v2-ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "send-proxy-v2-ssl" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "send-proxy-v2-ssl"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-send-proxy-v2-ssl-cn"></a>

**`no-send-proxy-v2-ssl-cn`**

```haproxy
no-send-proxy-v2-ssl-cn
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "send-proxy-v2-ssl-cn" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "send-proxy-v2-ssl-cn"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-sni-auto"></a>

**`no-sni-auto`**

```haproxy
no-sni-auto
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um die standardmäßig aktivierte
automatische SNI-Auswahl zu deaktivieren.

Siehe "no-check-sni-auto", um die automatische SNI-Auswahl für SSL-Health-Checks zu deaktivieren.

<a id="entry-5-2-no-ssl"></a>

**`no-ssl`**

```haproxy
no-ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "ssl" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "ssl"-Einstellung aus "default-server" zurückzusetzen.

Beachten Sie, dass bei Verwendung von `default-server ssl` und `no-ssl` für den Server dennoch eine
SSL-Verbindung initialisiert wird, damit sie später über die Runtime-API aktiviert werden kann:
Siehe die Befehle `set server` in der Verwaltungsdokumentation.

<a id="entry-5-2-no-ssl-reuse"></a>

**`no-ssl-reuse`**

```haproxy
no-ssl-reuse
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Wiederverwendung von SSL-Sitzungen, wenn die Kommunikation mit dem
Server über SSL erfolgt. Damit muss der Server für jede neue Verbindung einen vollständigen
Handshake durchführen. Dies ist vermutlich nur für Benchmarks, die Fehlerbehebung und besonders
misstrauische Benutzer nützlich.

<a id="entry-5-2-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Unterstützung für SSLv3, wenn die Kommunikation mit dem Server über
SSL erfolgt. Beachten Sie, dass SSLv2 im Code deaktiviert ist und durch keine Konfigurationsoption
aktiviert werden kann. Verwenden Sie stattdessen "ssl-min-ver" und "ssl-max-ver".

In default-server unterstützt: Nein

<a id="entry-5-2-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie
deaktiviert die zustandslose Sitzungswiederaufnahme (RFC 5077 TLS-Ticket-Erweiterung) und erzwingt
zustandsbehaftete Sitzungswiederaufnahme. Die zustandslose Sitzungswiederaufnahme erfordert auf
Servern mehr CPU-Leistung. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options"
verfügbar. Der TLS-Ticket-Mechanismus wird nur bis TLS 1.2 verwendet. Forward Secrecy ist mit
TLS-Tickets beeinträchtigt, sofern die Ticket-Schlüssel nicht regelmäßig gewechselt werden (durch
Neuladen oder mit "tls-ticket-keys"). Siehe auch "tls-tickets".

<a id="entry-5-2-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Unterstützung für TLSv1.0, wenn die Kommunikation mit dem Server
über SSL erfolgt. Beachten Sie, dass SSLv2 im Code deaktiviert ist und durch keine
Konfigurationsoption aktiviert werden kann. TLSv1 ist aufwendiger als SSLv3, daher ist es bei der
Kommunikation mit lokalen Servern oft sinnvoll, es zu deaktivieren. Diese Option ist auch in der
globalen Anweisung "ssl-default-server-options" verfügbar. Verwenden Sie stattdessen "ssl-min-ver"
und "ssl-max-ver".

In default-server unterstützt: Nein

<a id="entry-5-2-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Unterstützung für TLSv1.1, wenn die Kommunikation mit dem Server
über SSL erfolgt. Beachten Sie, dass SSLv2 im Code deaktiviert ist und durch keine
Konfigurationsoption aktiviert werden kann. TLSv1 ist aufwendiger als SSLv3, daher ist es bei der
Kommunikation mit lokalen Servern oft sinnvoll, es zu deaktivieren. Diese Option ist auch in der
globalen Anweisung "ssl-default-server-options" verfügbar. Verwenden Sie stattdessen "ssl-min-ver"
und "ssl-max-ver".

In default-server unterstützt: Nein

<a id="entry-5-2-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Unterstützung für TLSv1.2, wenn die Kommunikation mit dem Server
über SSL erfolgt. Beachten Sie, dass SSLv2 im Code deaktiviert ist und durch keine
Konfigurationsoption aktiviert werden kann. TLSv1 ist aufwendiger als SSLv3, daher ist es bei der
Kommunikation mit lokalen Servern oft sinnvoll, es zu deaktivieren. Diese Option ist auch in der
globalen Anweisung "ssl-default-server-options" verfügbar. Verwenden Sie stattdessen "ssl-min-ver"
und "ssl-max-ver".

In default-server unterstützt: Nein

<a id="entry-5-2-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option deaktiviert die Unterstützung für TLSv1.3, wenn die Kommunikation mit dem Server
über SSL erfolgt. Beachten Sie, dass SSLv2 im Code deaktiviert ist und durch keine
Konfigurationsoption aktiviert werden kann. TLSv1 ist aufwendiger als SSLv3, daher ist es bei der
Kommunikation mit lokalen Servern oft sinnvoll, es zu deaktivieren. Diese Option ist auch in der
globalen Anweisung "ssl-default-server-options" verfügbar. Verwenden Sie stattdessen "ssl-min-ver"
und "ssl-max-ver".

In default-server unterstützt: Nein

<a id="entry-5-2-no-verifyhost"></a>

**`no-verifyhost`**

```haproxy
no-verifyhost
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "verifyhost" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "verifyhost"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-no-tfo"></a>

**`no-tfo`**

```haproxy
no-tfo
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "tfo" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "tfo"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-non-stick"></a>

**`non-stick`**

```haproxy
non-stick
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Fügt diesem Server zugewiesene Verbindungen niemals einer stick-table hinzu. Dies kann zusammen
mit backup verwendet werden, um die Persistenz über stick-table für Backup-Server zu deaktivieren.

<a id="entry-5-2-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Dies aktiviert die NPN-TLS-Erweiterung und bietet die angegebene Protokollliste über NPN als unterstützt an. Die Protokollliste besteht aus einer durch Kommas getrennten Liste von Protokollnamen, beispielsweise: "http/1.1,http/1.0" (ohne Anführungszeichen). Dies erfordert, dass die SSL-Bibliothek mit aktivierter Unterstützung für TLS-Erweiterungen gebaut wurde (überprüfen Sie mit haproxy -vv). Beachten Sie, dass die NPN-Erweiterung durch die ALPN-Erweiterung ersetzt wurde (siehe das Schlüsselwort "alpn"), diese ist jedoch erst ab OpenSSL 1.0.2 verfügbar.

<a id="entry-5-2-observe"></a>

**`observe <mode>`**

```haproxy
observe <mode>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option aktiviert die Anpassung des Serverzustands basierend auf der Beobachtung der Kommunikation mit dem Server. Standardmäßig ist diese Funktion deaktiviert und deren Aktivierung erfordert zudem die Aktivierung von Health Checks. Es werden zwei Modi unterstützt: "layer4" und "layer7". Im layer4-Modus sind nur erfolgreiche oder fehlgeschlagene TCP-Verbindungen von Bedeutung. Im layer7-Modus, der nur für HTTP-Proxys erlaubt ist, werden Antworten vom Server überprüft, beispielsweise gültige oder ungültige HTTP-Codes, nicht parsbare Header, Zeitüberschreitungen usw. Gültige Statuscodes umfassen 100 bis 499, 501 und 505.

Siehe auch: "check", "on-error" und "error-limit".

<a id="entry-5-2-on-error"></a>

**`on-error <mode>`**

```haproxy
on-error <mode>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Wählt aus, was geschehen soll, wenn genügend aufeinanderfolgende Fehler erkannt werden. Derzeit sind vier Modi verfügbar:

- fastinter: erzwingt fastinter
- fail-check: simuliert eine fehlgeschlagene Prüfung und erzwingt fastinter (Standard)
- sudden-death: simuliert eine fehlgeschlagene Health-Check-Prüfung unmittelbar vor der Ausfallgrenze;
  eine weitere fehlgeschlagene Prüfung markiert den Server als ausgefallen; erzwingt fastinter
- mark-down: markiert den Server sofort als ausgefallen und erzwingt fastinter

Siehe auch: "check", "observe" und "error-limit".

<a id="entry-5-2-on-marked-down"></a>

**`on-marked-down <action>`**

```haproxy
on-marked-down <action>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Ändert, was geschieht, wenn ein Server als ausgefallen markiert wird. Derzeit ist eine Aktion verfügbar:

- shutdown-sessions: Beendet Peer-Streams. Wenn diese Einstellung aktiviert ist, werden alle Verbindungen zum Server sofort beendet, sobald der Server ausfällt. Dies kann verwendet werden, wenn der Health Check komplexere Fälle als ein einfacher Verbindungsstatus erkennt und lange Zeitüberschreitungen dazu führen würden, dass der Dienst zu lange unerreichbar bleibt. Beispielsweise kann ein Health Check erkennen, dass eine Datenbank blockiert ist und dass keine bestehenden Verbindungen mehr wiederverwendet werden können. Verbindungen, die auf diese Weise beendet werden, werden mit einem 'D'-Beendigungscode protokolliert (für "Down").

Aktionen sind standardmäßig deaktiviert.

<a id="entry-5-2-on-marked-up"></a>

**`on-marked-up <action>`**

```haproxy
on-marked-up <action>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Ändert, was geschieht, wenn ein Server als aktiv markiert wird. Derzeit ist eine Aktion verfügbar:

- shutdown-backup-sessions: Beendet Streams auf allen Backup-Servern. Dies erfolgt nur, wenn der Server nicht im Backup-Status ist und nicht deaktiviert ist (er muss ein effektives Gewicht von \> 0 haben). Dies kann gelegentlich verwendet werden, um einen aktiven Server nach der Wiederherstellung dazu zu zwingen, die gesamte Last wieder aufzunehmen, insbesondere bei langen Sitzungen (z. B. LDAP, SQL, ...). Dies kann mehr Probleme verursachen, als es lösen soll (z. B. unvollständige Transaktionen), verwenden Sie diese Funktion daher mit äußerster Vorsicht. Streams, die aufgrund der erneuten Verfügbarkeit eines Servers beendet werden, werden mit einem 'U'-Beendigungscode protokolliert (für "Up").

Aktionen sind standardmäßig deaktiviert.

<a id="entry-5-2-pool-conn-name"></a>

**`pool-conn-name <expr>`**

```haproxy
pool-conn-name <expr>
```

Kann in folgenden Kontexten verwendet werden: http

Beim Aufbau einer Backend-Verbindung wird dieser Ausdruck ausgewertet, um den Verbindungsnamen
zu erzeugen. Dieser Name ist eine der Schlüsseleigenschaften der Verbindung im Pool ungenutzter
Serververbindungen. Siehe das Schlüsselwort "http-reuse". Sucht eine Anfrage eine vorhandene
ungenutzte Verbindung, wird der Ausdruck ausgewertet, um eine identische Verbindung zu finden.

Im Kontext, in dem SSL SNI für die Backend-Verbindung verwendet wird, wird der Verbindungsname automatisch auf das Ergebnis des "sni"-Ausdrucks gesetzt. Dies entspricht dem häufigsten Einsatzfall. Für erweiterte Konfigurationen kann "pool-conn-name" verwendet werden, um dies zu überschreiben.

Siehe auch: "http-reuse", "sni"

<a id="entry-5-2-pool-low-conn"></a>

**`pool-low-conn <max>`**

```haproxy
pool-low-conn <max>
```

Kann in folgenden Kontexten verwendet werden: http

Legt einen unteren Schwellenwert für die Anzahl ungenutzter Verbindungen zu einem Server fest.
Unterhalb dieses Werts versucht ein Thread nicht, eine Verbindung von einem anderen Thread zu
übernehmen. Das kann die CPU-Nutzung bei vielen sehr schnellen Servern verbessern: Alle Threads
behalten jederzeit einige ungenutzte Verbindungen, statt diese bei einem Thread anzusammeln und
anschließend zwischen Threads zu verschieben. Typische Werte in Höhe der doppelten Thread-Anzahl
scheinen bereits bei Antwortzeiten unter einer Millisekunde sehr gute Leistung zu liefern.
Der Standardwert null erlaubt, jede ungenutzte Verbindung jederzeit zu verwenden; dies ist für den
normalen Einsatz empfohlen. Es gilt nur für Verbindungen, die nach denselben Grundsätzen wie bei
"http-reuse" gemeinsam genutzt werden können. Wird die gemeinsame Nutzung von Verbindungen durch
Threads mit "tune.idle-pool.shared" deaktiviert, kann diese Einstellung sehr wichtig sein, um
jedem Thread stets einige Verbindungen zu sichern. Andernfalls sinkt die Wiederverwendungsrate mit
steigender Thread-Anzahl.

<a id="entry-5-2-pool-max-conn"></a>

**`pool-max-conn <max>`**

```haproxy
pool-max-conn <max>
```

Kann in folgenden Kontexten verwendet werden: http

Legt die maximale Anzahl ungenutzter Verbindungen zu einem Server fest. -1 bedeutet unbegrenzt,
0 bedeutet keine ungenutzten Verbindungen. Der Standardwert ist -1. Sind ungenutzte Verbindungen
aktiviert, werden verwaiste Verbindungen, die keiner Clientsitzung mehr angehören, in einen eigenen
Pool verschoben. So bleiben sie für spätere Clients verwendbar. Dies gilt nur für Verbindungen,
die nach denselben Grundsätzen wie bei "http-reuse" gemeinsam genutzt werden können.

<a id="entry-5-2-pool-purge-delay"></a>

**`pool-purge-delay <delay>`**

```haproxy
pool-purge-delay <delay>
```

Kann in folgenden Kontexten verwendet werden: http

Legt die Verzögerung bis zum Beginn der Bereinigung ungenutzter Verbindungen fest. In jedem
Intervall von `<delay>` wird die Hälfte der ungenutzten Verbindungen geschlossen. 0 bedeutet, dass
keine ungenutzten Verbindungen gehalten werden. Der Standardwert ist 5s.

<a id="entry-5-2-port"></a>

**`port <port>`**

```haproxy
port <port>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Mit dem "port"-Parameter wird es möglich, einen anderen Port für Health Checks oder zur Prüfung des Agent-Checks zu verwenden. Bei einigen Servern kann es sinnvoll sein, einen Port speziell für eine Komponente zu reservieren, die komplexe Tests durchführen kann, die besser für Health Checks geeignet sind als die Anwendung selbst. Häufig wird beispielsweise ein einfaches Skript in inetd ausgeführt. Dieser Parameter wird ignoriert, wenn der "check"-Parameter nicht gesetzt ist. Siehe auch: "addr"-Parameter.

<a id="entry-5-2-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Erzwingt das Multiplexer-Protokoll für ausgehende Verbindungen zu diesem Server. Es muss mit dem
Modus des Backends (TCP oder HTTP) kompatibel und auf der Backend-Seite verwendbar sein. Die Liste
verfügbarer Protokolle wird von haproxy -vv ausgegeben. Angezeigt werden die Protokolleigenschaften:
der Modus (TCP/HTTP), die Seite (FE/BE), der Name des Multiplexers und seine Flags.

Einige Protokolle sind anfällig für Head-of-Line-Blocking auf der Server-Seite (flag=HOL_RISK). Schließlich unterstützen einige Protokolle keine Upgrades (flag=NO_UPG). Die HTX-Kompatibilität wird ebenfalls angegeben (flag=HTX).

Folgende Protokolle können als Argument für eine "proto"-Anweisung in einer Server-Zeile verwendet werden:

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

Idee hinter dieser Option ist, die Auswahl des besten Multiplexer-Protokolls für alle Verbindungen, die zu diesem Server hergestellt werden, zu umgehen.

Wenn ALPN oder NPN konfiguriert ist, sollten die angegebenen Protokolle mit dem Multiplexer-Protokoll
kompatibel sein, um Probleme zu vermeiden. Ist beispielsweise "proto h1" gesetzt, sollte ALPN nicht
auf "h2" gesetzt werden.

Siehe auch "ws", um für Websocket-Streams ein alternatives Protokoll zu verwenden.

QMux ist eine Teilmenge von QUIC, die über TCP läuft. Sie entspricht dem folgenden Protokollentwurf:
<https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. In haproxy gilt sie derzeit als
experimentell.

<a id="entry-5-2-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Diese QUIC-spezifische Einstellung wählt den Algorithmus zur Überlastkontrolle für alle
Verbindungen zu diesem Server. Die Algorithmen ähneln denen von TCP. Eine vollständige Beschreibung
aller Anpassungsmöglichkeiten finden Sie bei der gleichnamigen bind-Option.

Standardwert: cubic

Siehe auch: "tune.quic.be.tx.pacing" und "tune.quic.be.cc.max-win-size"

<a id="entry-5-2-redir"></a>

**`redir <prefix>`**

```haproxy
redir <prefix>
```

Kann in folgenden Kontexten verwendet werden: http

Der Parameter "redir" aktiviert die Umleitung für alle an diesen Server gerichteten GET- und
HEAD-Anfragen. HAProxy leitet die Anfrage dann nicht an den Server weiter, sondern sendet eine
Antwort "HTTP 302". Deren "Location"-Header besteht aus diesem Präfix, unmittelbar gefolgt von der
angefragten URI ab dem führenden '/' des Pfadbestandteils. Nach `<prefix>` sollte deshalb kein
abschließender Schrägstrich stehen. Alle ungültigen Anfragen werden abgewiesen; Anfragen, die weder
GET noch HEAD sind, werden normal vom Server bedient. Da die Antwort vollständig erzeugt wird,
sind darin weder Header-Änderungen noch das Einfügen von Cookies möglich. Cookies in Anfragen
werden jedoch weiterhin ausgewertet. Damit lässt sich diese Lösung auch verwenden, um Benutzer
bei einem lokalen Ausfall an einen entfernten Standort umzuleiten. Der wichtigste Einsatzzweck
besteht darin, die Bandbreite für statische Server zu erhöhen, indem Clients direkt Verbindungen
zu ihnen aufbauen. Hinweis: Verwenden Sie hier niemals ein relatives Ziel, da sonst eine Schleife
zwischen Client und HAProxy entsteht!

Beispiel: server srv1 192.168.1.1:80 redir <http://image1.mydomain.com> check

<a id="entry-5-2-renegotiate"></a>

**`renegotiate`**

```haproxy
renegotiate
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option aktiviert den Mechanismus zur sicheren Neuverhandlung (RFC 5746 TLS Renegotiation
Indication Extension) für ein bestimmtes SSL-Backend. Das bedeutet nicht, dass der SSL-Client
Anfragen zur Neuverhandlung sendet; es erlaubt Backends lediglich, auf Anforderung des Servers neu
zu verhandeln. Die zugrunde liegende SSL-Bibliothek muss Neuverhandlung weiterhin tatsächlich
unterstützen. Diese Option ist auch in der globalen Anweisung "ssl-default-server-options"
verfügbar. In TLS 1.3 ist keine Neuverhandlung mehr möglich. Sind weder "renegotiate" noch
"no-renegotiate" angegeben, bleibt das Standardverhalten der SSL-Bibliothek erhalten. Beispielsweise
aktiviert OpenSSL standardmäßig die sichere Neuverhandlung, während AWS-LC sie deaktiviert.

<a id="entry-5-2-rise"></a>

**`rise <count>`**

```haproxy
rise <count>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Der Parameter "rise" legt fest, dass ein Server nach `<count>` aufeinanderfolgenden erfolgreichen
Health Checks als betriebsbereit gilt. Ohne Angabe beträgt dieser Wert standardmäßig 2. Siehe auch
die Parameter "check", "inter" und "fall".

resolve-opts `<option>`,`<option>`,... Kann in folgenden Kontexten verwendet werden: tcp, http, log

Durch Kommas getrennte Liste von Optionen für die DNS-Auflösung dieses Servers.

Verfügbare Optionen:

- allow-dup-ip Standardmäßig verhindert HAProxy doppelte IP-Adressen in einem Backend, wenn die
  DNS-Auflösung zur Laufzeit aktiv ist. In manchen Fällen ist es jedoch sinnvoll, dass zwei Server
  (im selben Backend und über denselben FQDN aufgelöst) dieselbe IP-Adresse haben. Aktivieren Sie
  dafür einfach diese Option. Sie ist das Gegenteil von prevent-dup-ip.

- ignore-weight Ignoriert das in einem SRV-Eintrag gesetzte Gewicht. Dies ist nützlich, wenn
  Gewichte anders gesteuert werden sollen, beispielsweise über "agent-check" oder die Runtime-API.

- prevent-dup-ip Setzt das Standardverhalten von HAProxy für einen Server durch: Eine IP-Adresse,
  die bereits einem Server im selben Backend mit demselben fqdn zugeordnet ist, darf nicht erneut
  verwendet werden. Dies ist das Gegenteil von allow-dup-ip.

Beispiel:

```text
backend b_myapp
  default-server init-addr none resolvers dns
  server s1 myapp.example.com:80 check resolve-opts allow-dup-ip
  server s2 myapp.example.com:81 check resolve-opts allow-dup-ip
```

Wenn allow-dup-ip gesetzt ist:

- Gibt der Nameserver eine einzige IP-Adresse zurück, verwenden beide Server diese Adresse.
- Gibt der Nameserver 2 IP-Adressen zurück, wählt jeder Server eine andere Adresse.

Standardwert: nicht gesetzt

<a id="entry-5-2-resolve-prefer"></a>

**`resolve-prefer <family>`**

```haproxy
resolve-prefer <family>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Wenn DNS-Auflösung für einen Server aktiviert ist und mehrere IP-Adressen aus verschiedenen
Adressfamilien zurückgegeben werden, bevorzugt HAProxy eine Adresse aus der im Parameter
"resolve-prefer" angegebenen Familie. Siehe auch das globale Schlüsselwort "dns-accept-family", um
ausschließlich eine bestimmte Familie zu erzwingen. Verfügbare Familien: "ipv4" und "ipv6".

Standardwert: ipv6

Beispiel:

```text
server s1 app1.domain.com:80 resolvers mydns resolve-prefer ipv6
```

<a id="entry-5-2-resolve-net"></a>

**`resolve-net <network>[,<network[,...]]`**

```haproxy
resolve-net <network>[,<network[,...]]
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Diese Option bevorzugt die Auswahl einer IP-Adresse, die zu einem Netzwerk passt. In Clouds ist
dies nützlich, um eine lokale IP-Adresse zu bevorzugen. Ein Hochverfügbarkeitsdienst in einer Cloud
kann mit vielen IP-Adressen in verschiedenen Rechenzentren bekanntgegeben werden. Da die Latenz
zwischen Rechenzentren nicht vernachlässigbar ist, ermöglicht diese Änderung, ein lokales
Rechenzentrum zu bevorzugen. Passt keine Adresse zum konfigurierten Netzwerk, wird eine andere
Adresse ausgewählt.

Beispiel:

```text
server s1 app1.domain.com:80 resolvers mydns resolve-net 10.0.0.0/8
```

<a id="entry-5-2-resolvers"></a>

**`resolvers <id>`**

```haproxy
resolvers <id>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Verweist auf einen vorhandenen Abschnitt "resolvers", um den Hostnamen dieses Servers aufzulösen.
Bei Verwendung von Resolvern wird häufig empfohlen, die libc-basierte Auflösung zu deaktivieren,
auch wenn es Ausnahmen gibt (siehe [Abschnitt 5.3.1](/de/haproxy/bind-and-server-options/#section-5-3-1)).
In jedem Fall empfiehlt es sich, bei Resolvern "init-addr" explizit anzugeben, um diesen Punkt nicht
zu übersehen.

Beispiel:

```text
server s1 app1.domain.com:80 init-addr last,none check resolvers mydns
```

Siehe auch [Abschnitt 5.3](/de/haproxy/bind-and-server-options/#section-5-3) für Details zur Implementierung und zu beachtende Fallstricke.

<a id="entry-5-2-send-proxy"></a>

**`send-proxy`**

```haproxy
send-proxy
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "send-proxy" erzwingt das PROXY-Protokoll für jede Verbindung zu diesem Server.
Das PROXY-Protokoll informiert die Gegenstelle über die Adressen auf Schicht 3/4 der eingehenden
Verbindung. Dadurch kennt sie unabhängig vom Protokoll der oberen Schicht die Client-Adresse oder
die angesprochene öffentliche Adresse. Bei Verbindungen, die von einem Listener mit "accept-proxy"
oder "accept-netscaler-cip" angenommen wurden, wird die übermittelte Adresse verwendet. Es werden
nur die Adressfamilien TCPv4 und TCPv6 unterstützt. Andere Familien, etwa Unix-Sockets, melden die
Familie UNKNOWN. Server mit dieser Option können vollständig mit einer weiteren HAProxy-Instanz
verkettet werden, die mit "accept-proxy" lauscht. Die Einstellung darf nicht verwendet werden, wenn
der Server das Protokoll nicht versteht. Bei Health Checks an den Server wird das PROXY-Protokoll
mit dieser Option automatisch verwendet, sofern nicht explizit "port" oder "addr" angegeben ist.
In diesem Fall ist zusätzlich eine explizite Direktive "check-send-proxy" erforderlich. Siehe auch
"no-send-proxy" in diesem Abschnitt sowie die Optionen "accept-proxy" und "accept-netscaler-cip"
des Schlüsselworts "bind".

<a id="entry-5-2-send-proxy-v2"></a>

**`send-proxy-v2`**

```haproxy
send-proxy-v2
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "send-proxy-v2" erzwingt Version 2 des PROXY-Protokolls für jede Verbindung zu diesem
Server. Das PROXY-Protokoll informiert die Gegenstelle über die Adressen auf Schicht 3/4 der
eingehenden Verbindung. Dadurch kennt sie unabhängig vom Protokoll der oberen Schicht die
Client-Adresse oder die angesprochene öffentliche Adresse. Außerdem werden ALPN-Informationen
gesendet, wenn alpn ausgehandelt wurde. Die Einstellung darf nicht verwendet werden, wenn der Server
diese Protokollversion nicht versteht. Siehe auch "no-send-proxy-v2" in diesem Abschnitt und die
Option send-proxy" des Schlüsselworts "bind".

<a id="entry-5-2-set-proxy-v2-tlv-fmt"></a>

**`set-proxy-v2-tlv-fmt(<id>) <fmt>`**

```haproxy
set-proxy-v2-tlv-fmt(<id>) <fmt>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Mit "set-proxy-v2-tlv-fmt" können beliebige TLVs der PROXY-Protokollversion 2 gesendet werden.
Zum Typbereich (`<id>`) der definierten TLV-Typen siehe Abschnitt 2.2.8. der PROXY-Protokollspezifikation.
Der Wert kann dagegen frei gewählt werden, sofern er die maximale Länge von 65,535 Bytes nicht
überschreitet. Die Option kann auch TLVs weiterleiten: Mit dem Sample-Abruf "fc_pp_tlv" wird dazu
ein vom Frontend empfangenes TLV-Feld abgerufen. Sie kann als server- oder default-server-Option
verwendet werden. Damit PPv2-TLVs tatsächlich gesendet werden, muss sie zusammen mit send-proxy-v2
verwendet werden.

Beispiel: server srv1 192.168.1.1:80 send-proxy-v2 set-proxy-v2-tlv-fmt(0x20) %[fc_pp_tlv(0x20)]

In diesem Fall wird das TLV-Feld vom Typ 0x20 als Zeichenfolge abgerufen und als Wert eines neu
erzeugten TLV-Felds verwendet, das ebenfalls den Typ 0x20 hat.

<a id="entry-5-2-proxy-v2-options"></a>

**`proxy-v2-options <option>[,<option>]*`**

```haproxy
proxy-v2-options <option>[,<option>]*
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "proxy-v2-options" fügt Optionen hinzu, die bei Verwendung von "send-proxy-v2" mit
Version 2 des PROXY-Protokolls gesendet werden. Verfügbar sind:

- ssl : Siehe auch "send-proxy-v2-ssl".
- cert-cn : Siehe auch "send-proxy-v2-ssl-cn".
- ssl-cipher: Name des verwendeten Ciphers.
- cert-sig : Signaturalgorithmus des verwendeten Zertifikats.
- cert-key : Schlüsselalgorithmus des verwendeten Zertifikats.
- authority: Vom Client übermittelter Hostname (nur SNI aus einer TLS-Verbindung wird unterstützt).
- crc32c : Prüfsumme des PROXYv2-Headers.
- unique-id: Sendet eine mit "unique-id-format" des Frontends erzeugte eindeutige ID im
  PROXYv2-Header. Diese unique-id ist hauptsächlich für "mode tcp" vorgesehen. In "mode http" kann
  sie zu unerwarteten Ergebnissen führen, da die erzeugte eindeutige ID auch für die erste
  HTTP-Anfrage einer Keep-Alive-Verbindung verwendet wird.

<a id="entry-5-2-send-proxy-v2-ssl"></a>

**`send-proxy-v2-ssl`**

```haproxy
send-proxy-v2-ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "send-proxy-v2-ssl" erzwingt Version 2 des PROXY-Protokolls für jede Verbindung zu
diesem Server. Das PROXY-Protokoll informiert die Gegenstelle über die Adressen auf Schicht 3/4
der eingehenden Verbindung. Dadurch kennt sie unabhängig vom Protokoll der oberen Schicht die
Client-Adresse oder die angesprochene öffentliche Adresse. Zusätzlich wird die
SSL-Informationserweiterung des PROXY-Protokolls in den PROXY-Protokoll-Header aufgenommen. Die
Einstellung darf nicht verwendet werden, wenn der Server diese Protokollversion nicht versteht.
Siehe auch "no-send-proxy-v2-ssl" in diesem Abschnitt und die Option "send-proxy-v2" des
Schlüsselworts "bind".

<a id="entry-5-2-send-proxy-v2-ssl-cn"></a>

**`send-proxy-v2-ssl-cn`**

```haproxy
send-proxy-v2-ssl-cn
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "send-proxy-v2-ssl" erzwingt Version 2 des PROXY-Protokolls für jede Verbindung zu
diesem Server. Das PROXY-Protokoll informiert die Gegenstelle über die Adressen auf Schicht 3/4
der eingehenden Verbindung. Dadurch kennt sie unabhängig vom Protokoll der oberen Schicht die
Client-Adresse oder die angesprochene öffentliche Adresse. Zusätzlich werden die
SSL-Informationserweiterung des PROXY-Protokolls sowie der Common Name aus dem Subject des
Client-Zertifikats (falls vorhanden) in den PROXY-Protokoll-Header aufgenommen. Die Einstellung darf
nicht verwendet werden, wenn der Server diese Protokollversion nicht versteht. Siehe auch
"no-send-proxy-v2-ssl-cn" in diesem Abschnitt und die Option "send-proxy-v2" des Schlüsselworts
"bind".

<a id="entry-5-2-shard"></a>

**`shard <shard>`**

```haproxy
shard <shard>
```

Kann in folgenden Kontexten verwendet werden: peers

Dieser Parameter wird nur bei der Synchronisierung von stick-tables über das peers-Protokoll
verwendet. "shard" bezeichnet die Peers, die alle Stick-Table-Aktualisierungen für Schlüssel
empfangen, deren Verteilungshash diesem Shard entspricht. Zulässige Werte reichen von 0 bis zum
Wert des Parameters "shards" im Abschnitt "peers". Der Standardwert 0 bedeutet, dass der Peer
alle Schlüsselaktualisierungen empfängt. Werte größer als "shards" werden ignoriert. Ebenso wird
jeder für den lokalen Peer angegebene Wert ignoriert.

Beispiel:

```haproxy
peers mypeers
     shards 3
     peer A 127.0.0.1:40001 # local peer without shard value (0 internally)
     peer B 127.0.0.1:40002 shard 1
     peer C 127.0.0.1:40003 shard 2
     peer D 127.0.0.1:40004 shard 3
```

<a id="entry-5-2-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Sie legt
die Zeichenfolge mit der Liste der Signaturalgorithmen fest, die beim TLSv1.2- und TLSv1.3-Handshake
ausgehandelt werden. Das Format der Zeichenfolge ist in "man 3 SSL_CTX_set1_sigalgs" in den
OpenSSL-Handbuchseiten beschrieben. Von dieser Einstellung wird abgeraten, sofern keine
Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-5-2-slowstart"></a>

**`slowstart <start_time_in_ms>`**

```haproxy
slowstart <start_time_in_ms>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "slowstart" eines Servers nimmt einen Wert in Millisekunden entgegen. Dieser gibt
an, nach welcher Zeit ein gerade wieder verfügbar gewordener Server mit voller Leistung arbeitet.
Wie bei allen zeitbasierten Parametern kann explizit eine andere Einheit aus { us, ms, s, m, h, d }
angegeben werden. Die Leistung steigt während dieser Zeit linear von 0 auf 100%. Die Begrenzung
wirkt auf zwei Parameter:

- maxconn: Die vom Server akzeptierte Verbindungsanzahl steigt von 1 auf 100% der üblichen
  dynamischen Grenze, die durch (minconn,maxconn,fullconn) definiert ist.

- weight: Verwendet das Backend einen dynamisch gewichteten Algorithmus, steigt das Gewicht
  linear von 1 auf 100%. Dabei wird es bei jedem Health Check aktualisiert. Deshalb ist es wichtig,
  dass "inter" kleiner als "slowstart" ist, um die Anzahl der Schritte zu maximieren.

slowstart gilt niemals beim Start von HAProxy, da dies laufende Server beeinträchtigen würde.
Es gilt nur, wenn ein Server zuvor als ausgefallen erkannt wurde.

<a id="entry-5-2-sni"></a>

**`sni <expression>`**

```haproxy
sni <expression>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Der Parameter "sni" wertet den Sample-Abrufausdruck aus, wandelt ihn in eine Zeichenfolge um und
verwendet das Ergebnis als Hostnamen in der SNI-TLS-Erweiterung an den Server. Ein typischer
Anwendungsfall ist, in einem TCP/SSL-Brückenszenario die vom Client empfangene SNI weiterzugeben;
als Ausdruck dient dabei der Sample-Abruf "ssl_fc_sni". DIES DARF NICHT FÜR HTTPS VERWENDET WERDEN.
Dort sollte stattdessen req.hdr(host) verwendet werden, da die SNI bei HTTPS immer dem Host-Feld
entsprechen muss und Clients über dieselbe Verbindung verschiedene Hostnamen verwenden dürfen).
Ist "verify required" gesetzt (die empfohlene Einstellung), wird der resultierende Name außerdem
mit den Namen im Serverzertifikat abgeglichen. Weitere Informationen finden Sie bei "verify".
Soll die SNI für Health Checks gesetzt werden, finden Sie Einzelheiten bei "check-sni".

Standardmäßig wird die SNI dem Verbindungsnamen für "http-reuse" zugewiesen, sofern dieser nicht
durch das Server-Schlüsselwort "pool-conn-name" überschrieben wird.

<a id="entry-5-2-sni-auto"></a>

**`sni-auto`**

```haproxy
sni-auto
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Der Parameter "sni-auto" aktiviert die automatische SNI-Auswahl, sofern noch kein Wert gesetzt
wurde. Er setzt den Ausdruck "sni" auf "req.hdr(host),field(1,:)". Damit wird die SNI mit dem
Hostnamen der an den Server gesendeten Anfrage übermittelt, jedoch ohne Portnummer. Dies ist
standardmäßig aktiviert. Als "server"-Einstellung kann dieser Parameter jedoch eine über
"default-server" geerbte Standardeinstellung "no-sni-auto" zurücksetzen. Er kann auch als
"default-server"-Einstellung verwendet werden, um eine frühere "no-sni-auto"-Einstellung aus
"default-server" zurückzusetzen.

Bei HTTPS-Verbindungen richtet sich die gewählte SNI nach dem Wert des host-Headers der Anfrage,
sofern dieser vorhanden ist. Andernfalls bleibt sie ungesetzt. Bei anderen Protokollen wird die
Option ignoriert.

Wird die automatische SNI-Auswahl verwendet, wird der Wert dem Verbindungsnamen für "http-reuse"
zugewiesen, sofern dieser nicht durch das Server-Schlüsselwort "pool-conn-name" überschrieben wird.

Siehe "check-sni-auto", um die automatische SNI-Auswahl für SSL-Health-Checks zu aktivieren.

<a id="entry-5-2-source"></a>

**`source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<pl>[-<ph>]] [interface <name>] ...
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Der Parameter "source" setzt die Quelladresse für Verbindungen zum Server. Er verwendet genau
dieselben Parameter und dasselbe Prinzip wie das Backend-Schlüsselwort "source", gilt aber nur für
den Server, der darauf verweist. Einzelheiten finden Sie beim Schlüsselwort "source".

Zusätzlich kann mit "source" in einer server-Zeile ein Quellportbereich angegeben werden. Dazu
werden die untere und obere Grenze durch einen Bindestrich ('-') getrennt. Einige Betriebssysteme
verlangen möglicherweise eine gültige IP-Adresse, wenn ein Quellportbereich angegeben ist.
Mehrere Server dürfen dieselbe IP-Adresse und denselben Bereich verwenden. Damit lässt sich die
Grenze von insgesamt 64k gleichzeitigen Verbindungen umgehen; die Grenze liegt dann bei 64k
Verbindungen pro Server.

Seit Linux 4.2/libc 2.23 wird IP_BIND_ADDRESS_NO_PORT für Verbindungen gesetzt, bei denen eine
Quelladresse ohne Portangabe angegeben ist.

<a id="entry-5-2-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option aktiviert die SSL-Verschlüsselung ausgehender Verbindungen zum Server. Bei
SSL-Verbindungen zu Servern ist die Prüfung der Serverzertifikate mit "verify" entscheidend;
andernfalls ist die Kommunikation für einfache Man-in-the-Middle-Angriffe anfällig, wodurch SSL
nutzlos wird. Mit dieser Option werden auch Health Checks automatisch über SSL gesendet, sofern
nicht eine "port"- oder "addr"-Direktive ein anderes Prüfziel angibt. Siehe "no-ssl", um "ssl" zu
deaktivieren, und "check-ssl", um SSL-Health-Checks zu erzwingen.

<a id="entry-5-2-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die Verwendung von `<version>` oder einer niedrigeren Version, wenn die
Kommunikation mit dem Server über SSL erfolgt. Sie ist auch in der globalen Anweisung
"ssl-default-server-options" verfügbar. Siehe auch "ssl-min-ver".

<a id="entry-5-2-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option erzwingt die Verwendung von `<version>` oder einer höheren Version, wenn die
Kommunikation mit dem Server über SSL erfolgt. Sie ist auch in der globalen Anweisung
"ssl-default-server-options" verfügbar. Siehe auch "ssl-max-ver".

<a id="entry-5-2-ssl-reuse"></a>

**`ssl-reuse`**

```haproxy
ssl-reuse
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "no-ssl-reuse" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "no-ssl-reuse"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-stick"></a>

**`stick`**

```haproxy
stick
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "non-stick" zurückzusetzen. Sie kann auch als "default-server"-Einstellung
verwendet werden, um eine frühere "non-stick"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-strict-maxconn"></a>

**`strict-maxconn`**

```haproxy
strict-maxconn
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Die Bezeichnung maxconn für Server ist etwas irreführend: Sie legt tatsächlich die maximale Anzahl
an Anfragen fest, die an einen Server gesendet werden. Mit ungenutzten Verbindungen kann die
Gesamtzahl der Verbindungen zum Server jedoch höher sein. Wird eine strikte Verbindungsgrenze
benötigt, kann strict-maxconn ergänzt werden. Dann werden niemals mehr als maxconn Verbindungen zu
einem Server aufgebaut; bei Bedarf werden Verbindungen wiederverwendet oder beendet. Beachten Sie
jedoch, dass Anfragen dadurch fehlschlagen können, wenn keine neue Verbindung aufgebaut werden kann
und keine ungenutzte Verbindung verfügbar ist. Das kann bei als "private" bezeichneten Verbindungen geschehen, die
wegen einer erfolgten Authentifizierung ausschließlich an eine Sitzung gebunden sind.

<a id="entry-5-2-socks4"></a>

**`socks4 <addr>:<port>`**

```haproxy
socks4 <addr>:<port>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option aktiviert einen vorgeschalteten socks4-Tunnel für ausgehende Verbindungen zum Server.
Sie erzwingt standardmäßig nicht, dass Health Checks über socks4 laufen. Dafür muss das Schlüsselwort
"check-via-socks4" verwendet werden.

<a id="entry-5-2-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Aktiviert die TCP-MD5-Signatur (RFC 2385 Schutz von BGP-Sitzungen mithilfe der TCP-MD5-Signaturoption)
für alle ausgehenden Verbindungen zu diesem Server. Diese Option ist nur unter Linux verfügbar.
Wenn sie aktiviert ist, wird die Zeichenfolge `<password>` verwendet, um jedes TCP-Segment mit
einem 16-Byte-MD5-Digest zu signieren. Dies schützt die TCP-Verbindung vor Spoofing. Der wichtigste
Anwendungsfall ist der Schutz von BGP gegen das Einschleusen gefälschter TCP-Segmente in den
Verbindungsstrom. Die Option kann aber für alle sehr langlebigen TCP-Verbindungen nützlich sein.

<a id="entry-5-2-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Setzt den TCP User Timeout für alle ausgehenden Verbindungen zu diesem Server. Diese Option ist
unter Linux seit Version 2.6.37 verfügbar. Damit kann HAProxy eine Zeitüberschreitung für Sockets
konfigurieren, deren Daten innerhalb der angegebenen Zeit keine Bestätigung erhalten. Dies ist
besonders für langlebige Verbindungen mit langen Leerlaufzeiten nützlich, etwa Remote-Terminals
oder Datenbank-Verbindungspools. Dort müssen die Zeitüberschreitungen für Client und Server hoch
bleiben, um lange Leerlaufzeiten zu ermöglichen; zugleich ist es wichtig, das Verschwinden des
Servers zu erkennen, um alle Ressourcen seiner Verbindung (und der Clientsitzung) freizugeben.
Ein weiterer typischer Anwendungsfall ist, Verbindungen zu ausgefallenen Servern zwangsweise zu
beenden, wenn Health Checks zu langsam sind oder während eines unterbrechungsfreien Neuladens,
bei dem Health Checks deaktiviert sind. Das Argument ist eine Zeitspanne, standardmäßig in
Millisekunden. Dies funktioniert nur bei regulären TCP-Verbindungen und wird bei anderen
Protokollen ignoriert.

<a id="entry-5-2-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option aktiviert TCP Fast Open für Verbindungen zu Servern auf Systemen, die es unterstützen
(derzeit nur Linux-Kernel \>= 4.11). Weitere Informationen zu TCP Fast Open finden Sie bei der
bind-Option "tfo". Beachten Sie, dass bei tfo auch die Schlüsselwörter "conn-failure",
"empty-response" und "response-timeout" für "retry-on" verwendet werden sollten. Andernfalls kann
HAProxy die Verbindung bei einem Fehler nicht erneut versuchen. Siehe auch "no-tfo".

<a id="entry-5-2-track"></a>

**`track [<backend>/]<server>`**

```haproxy
track [<backend>/]<server>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Mit dieser Option wird der aktuelle Zustand eines Servers durch Verfolgen eines anderen Servers
bestimmt. Auch ein Server, der seinerseits einen anderen verfolgt, kann verfolgt werden, sofern am
Ende der Kette ein Server mit aktivierten Health Checks steht. Fehlt `<backend>`, wird das aktuelle
Backend verwendet. Wird disable-on-404 verwendet, muss es auf beiden Proxys aktiviert sein.

Beispiel:

```text
backend A
server a1 1.1.1.1:80 track B/b1
server a2 1.1.1.2:80 track B/b1

backend B
server b1 2.2.2.2:80 check
```

<a id="entry-5-2-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Option kann als "server"-Einstellung verwendet werden, um eine über "default-server" als
Standardwert geerbte Einstellung "no-tls-tickets" zurückzusetzen. Der TLS-Ticket-Mechanismus wird
nur bis TLS 1.2 verwendet. Forward Secrecy ist mit TLS-Tickets beeinträchtigt, sofern die
Ticket-Schlüssel nicht regelmäßig gewechselt werden (durch Neuladen oder mit "tls-ticket-keys").
Die Option kann auch als "default-server"-Einstellung verwendet werden, um eine frühere
"no-tls-tickets"-Einstellung aus "default-server" zurückzusetzen.

<a id="entry-5-2-verify"></a>

**`verify [none|required]`**

```haproxy
verify [none|required]
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde. Bei
'none' wird das Serverzertifikat nicht überprüft. Andernfalls wird das vom Server bereitgestellte
Zertifikat mit den CAs aus 'ca-file' und optionalen CRLs aus 'crl-file' überprüft, nachdem geprüft
wurde, ob die Namen in den Zertifikatsattributen subject und subjectAlternateNames mit dem über
"sni" übergebenen Namen übereinstimmen. Wurde dieser nicht angegeben, wird der mit "verifyhost"
übergebene statische Hostname verwendet. Wird kein Name gefunden, werden die Namen im Zertifikat
ignoriert. Deshalb ist es ohne SNI wichtig, "verifyhost" zu verwenden. Schlägt die Überprüfung fehl,
wird der Handshake abgebrochen. Bei SSL-Verbindungen zu Servern ist die Überprüfung der
Serverzertifikate von entscheidender Bedeutung; andernfalls ist die Kommunikation für einfache
Man-in-the-Middle-Angriffe anfällig und SSL dadurch völlig nutzlos. Sofern "ssl_server_verify" nicht
im globalen Abschnitt steht, ist "verify" standardmäßig auf "required" gesetzt.

<a id="entry-5-2-verifyhost"></a>

**`verifyhost <hostname>`**

```haproxy
verifyhost <hostname>
```

Kann in folgenden Kontexten verwendet werden: tcp, http, log, peers, ring

Diese Einstellung ist nur verfügbar, wenn Unterstützung für OpenSSL einkompiliert wurde, und
wirkt nur, wenn auch 'verify required' angegeben ist. Sie legt einen statischen Standardhostnamen
fest, gegen den das Serverzertifikat geprüft wird, wenn für die Verbindung zum Server keine SNI
verwendet wurde. Ohne SNI ist dies die einzige Möglichkeit, die Hostnamenprüfung zu aktivieren.
Der statische Hostname wird, sofern gesetzt, auch für Health Checks verwendet, wenn diese keinen
SNI-Wert bereitstellen. Passt keiner der Hostnamen im Zertifikat zum angegebenen Hostnamen, wird der
Handshake abgebrochen. Die Hostnamen im vom Server bereitgestellten Zertifikat dürfen Platzhalter
enthalten. Siehe auch "verify", "sni" und "no-verifyhost".

<a id="entry-5-2-weight"></a>

**`weight <weight>`**

```haproxy
weight <weight>
```

Kann in folgenden Kontexten verwendet werden: tcp, http

Der Parameter "weight" passt das Gewicht des Servers im Verhältnis zu anderen Servern an.
Alle Server erhalten Last proportional zu ihrem Gewicht im Verhältnis zur Summe aller Gewichte:
Je höher das Gewicht, desto höher die Last. Das Standardgewicht ist 1, der Maximalwert 256.
Bei 0 nimmt der Server nicht an der Lastverteilung teil, akzeptiert aber weiterhin durch Persistenz
zugeordnete Verbindungen. Wird die Last damit entsprechend der Serverkapazität verteilt, empfiehlt
es sich, mit Werten zu beginnen, die erhöht und verringert werden können, beispielsweise zwischen
10 und 100. So bleibt für spätere Anpassungen ausreichend Spielraum nach oben und unten.

<a id="entry-5-2-ws"></a>

**`ws { auto | h1 | h2 }`**

```haproxy
ws { auto | h1 | h2 }
```

Kann in folgenden Kontexten verwendet werden: http

Mit dieser Option wird das Protokoll zur Weiterleitung von Websocket-Streams konfiguriert. Dies
ist besonders bei einem HTTP/2-Backend nützlich, das H2-Websockets gemäß RFC8441 nicht unterstützt.

Der Standardmodus ist "auto". Er verwendet dasselbe Protokoll wie das Hauptprotokoll. Nur bei
ALPN gibt es einen Unterschied: Hier kann versucht werden, die ALPN ausschließlich für
Websocket-Streams auf "http/1.1" herabzusetzen, sofern die konfigurierte Server-ALPN dieses
Protokoll enthält.

Der Wert "h1" erzwingt HTTP/1.1 für Websocket-Streams; ist SSL-ALPN für den Server aktiviert,
erfolgt dies über ALPN. Entsprechend kann "h2" HTTP/2.0-Websockets erzwingen. Verwenden Sie diesen
Wert mit Vorsicht: Der Server muss RFC8441 unterstützen, andernfalls meldet haproxy beim
Weiterleiten von Websockets einen Fehler.

Beachten Sie, dass NPN nicht berücksichtigt wird, da es zugunsten der ALPN-Erweiterung als
veraltet gilt.

Siehe auch "alpn" und "proto".

## 5.3. Auflösung von Server-IP-Adressen über DNS {#section-5-3}

HAProxy erlaubt einen Hostnamen in der server-Zeile, um die IP-Adresse über Nameserver zu
ermitteln. Standardmäßig löst HAProxy den Namen beim Start während des Parsens der
Konfigurationsdatei auf und speichert das Ergebnis für die gesamte Prozesslebensdauer zwischen.
In manchen Fällen reicht dies nicht aus, etwa bei Amazon, wo sich die IP eines Servers nach einem
Neustart ändern kann oder die virtuelle IP eines ELB von der aktuellen Auslastung abhängt.

Dieses Kapitel beschreibt, wie HAProxy zur Namensauflösung von Servern während der Laufzeit
konfiguriert werden kann.

Unabhängig davon, ob die Servernamensauflösung zur Laufzeit aktiviert ist, führt HAProxy
standardmäßig beim Start während des Parsens der Konfiguration die erste Auflösung über libc
durch, sofern dies nicht mit "init-addr" deaktiviert wurde.

### 5.3.1. Überblick {#section-5-3-1}

Wie in der Einleitung beschrieben, erfolgt die Namensauflösung in HAProxy an zwei verschiedenen
Punkten der Prozesslebensdauer:

```text
1. Beim Start verarbeitet HAProxy die Definition der server-Zeile und
   erkennt einen Hostnamen. Zur Auflösung dieses Hostnamens verwendet
   es libc-Funktionen. Diese Auflösung basiert auf /etc/resolv.conf.

2. Zur Laufzeit führt HAProxy regelmäßig Namensauflösungen für Server
   durch, die eine DNS-Auflösung benötigen.
```

Weitere Ereignisse können zur Laufzeit eine Namensauflösung auslösen:

- Wenn der Health Check eines Servers mit einer Verbindungszeitüberschreitung endet, kann dies
  daran liegen, dass der Server eine neue IP-Adresse hat. Daher muss eine Namensauflösung ausgelöst
  werden, um die neue IP zu ermitteln.

Bei Verwendung von Resolvern kann der Servername entweder ein Hostname oder ein SRV-Label sein.
HAProxy betrachtet alles, was mit einem Unterstrich beginnt, als SRV-Label. Ist ein SRV-Label
angegeben, werden die zugehörigen SRV-Einträge vom DNS-Server abgerufen und die darin enthaltenen
Hostnamen verwendet. Das SRV-Label wird regelmäßig geprüft. Werden Server hinzugefügt oder
entfernt, übernimmt HAProxy diese Änderungen automatisch.

Dabei ist Folgendes zu beachten:

- Alle Nameserver werden gleichzeitig abgefragt. HAProxy verarbeitet die erste gültige Antwort.

- Eine Auflösung gilt als ungültig (NX, Zeitüberschreitung, abgelehnt), wenn alle Server einen
  Fehler zurückgeben.

- Der in HAProxy implementierte DNS-Client ist sehr einfach und versteht die Vielzahl von Optionen
  und erweiterten Konfigurationen nicht, die der Resolver eines Betriebssystems verarbeiten kann.
  Außer bei sehr einfachen Konfigurationen, in denen ein durch seinen FQDN bekannter Server stets
  genau eine IP-Adresse hat und diese gelegentlich erneuert (z. B. nach einem Neustart), wird daher
  dringend empfohlen, libc-basierte Auflösung beim Start nicht mit DNS-basierter Auflösung zur
  Laufzeit zu mischen. Solche Mischkonfigurationen verursachen bekanntermaßen Fehler bei der
  Adresserneuerung. Sofern Sie nicht genau wissen, was Sie tun, sollten Sie deshalb "libc" immer
  aus "init-addr" ausschließen, wenn Sie "resolvers" in einer server-Zeile verwenden.

### 5.3.2. Der Abschnitt resolvers {#section-5-3-2}

Dieser Abschnitt enthält Informationen zur Namensauflösung in HAProxy. Es können beliebig viele
resolvers-Abschnitte angelegt werden. Jeder Abschnitt kann mehrere Nameserver enthalten.

Beim Start versucht HAProxy, einen resolvers-Abschnitt namens "default" zu erzeugen, sofern in der
Konfiguration noch kein Abschnitt so benannt wurde. Er wird standardmäßig vom httpclient verwendet
und nutzt das Schlüsselwort parse-resolv-conf. Kann HAProxy diesen Abschnitt nicht automatisch
erzeugen, wird weder ein Fehler noch eine Warnung ausgegeben.

Sind in einem resolvers-Abschnitt mehrere Nameserver konfiguriert, verwendet HAProxy die erste
gültige Antwort. Bei ungültigen Antworten wird nur die letzte behandelt. So erhält ein langsamer
Server die Möglichkeit, nach einem schnellen fehlerhaften oder veralteten Server noch eine gültige
Antwort zu liefern.

Gibt jeder Server einen anderen Fehlertyp zurück, verwendet HAProxy nur den letzten Fehler.
Auf diesen wird die folgende Verarbeitung angewendet:

```text
1. HAProxy wiederholt dieselbe DNS-Anfrage mit einem neuen Anfragetyp.
   A-Anfragen werden auf AAAA umgestellt oder umgekehrt. SRV-Anfragen
   sind hiervon nicht betroffen. Auch Zeitüberschreitungen sind ausgenommen.

2. Nach dem Wechsel des Anfragetyps (oder wenn dieser nicht anwendbar
   ist) wiederholt HAProxy die ursprüngliche DNS-Anfrage mit dem
   bevorzugten Anfragetyp.

3. HAProxy wiederholt die vorherigen Schritte <resolve_retries> Mal.
   Wird danach keine gültige Antwort empfangen, beendet es die
   DNS-Auflösung und meldet den Fehler.
```

Bei 2 Nameservern in einem resolvers-Abschnitt sind beispielsweise folgende Abläufe möglich:

- Die erste Antwort ist gültig und wird sofort übernommen; die zweite wird ignoriert.

- Die erste Antwort ist ungültig, die zweite gültig; dann wird die zweite übernommen.

- Die erste Antwort ist NX domain, die zweite ist abgeschnitten; HAProxy wiederholt die Abfrage
  dann mit einem neuen Typ.

- Die erste Antwort ist NX domain, bei der zweiten tritt eine Zeitüberschreitung auf; HAProxy
  wiederholt die Abfrage dann mit einem neuen Typ.

- Bei beiden Nameservern tritt eine Zeitüberschreitung auf; HAProxy wiederholt die Abfrage dann
  mit demselben Abfragetyp.

Da ein DNS-Server möglicherweise nicht alle IP-Adressen in einer DNS-Antwort zurückgibt, speichert
HAProxy frühere Antworten zwischen. Eine Antwort gilt als veraltet, wenn die IP-Adresse
`<hold obsolete>` Sekunden lang nicht zurückgegeben wurde.

<a id="entry-5-3-2-resolvers"></a>

**`resolvers <resolvers id>`**

```haproxy
resolvers <resolvers id>
```

Erzeugt eine neue Nameserverliste mit der Kennung `<resolvers id>`. Wie oben beschrieben, existiert
der besondere Name "default" immer und wird automatisch erzeugt, wenn er nicht explizit deklariert
wurde. Interne Dienste wie httpclient verwenden diesen Eintrag. Die Deklaration eines Eintrags
"default" beeinflusst daher die Namensauflösung dieser Dienste.

Ein resolvers-Abschnitt akzeptiert die folgenden Parameter:

<a id="entry-5-3-2-accepted-payload-size"></a>

**`accepted_payload_size <nb>`**

```haproxy
accepted_payload_size <nb>
```

Definiert die maximale Nutzlastgröße, die HAProxy akzeptiert und allen in diesem resolvers-Abschnitt
konfigurierten Nameservern mitteilt. `<nb>` wird in Bytes angegeben. Ohne Angabe meldet HAProxy 512
(den von RFC 6891 definierten Mindestwert).

Hinweis: Der höchste zulässige Wert ist 65535. Für UDP wird 4096 empfohlen; von Werten über 8192
wird abgeraten, sofern Sie nicht sicher sind, dass System und Netzwerk damit umgehen können.
Werte über 65507 sind nicht sinnvoll, da dies die maximale UDP-Nutzlastgröße ist. Wenn Sie nur
TCP-Nameserver zur Verarbeitung sehr großer DNS-Antworten verwenden, sollten Sie den Höchstwert
65535 setzen.

<a id="entry-5-3-2-nameserver"></a>

**`nameserver <name> <address>[:port] [param*]`**

```haproxy
nameserver <name> <address>[:port] [param*]
```

Konfiguriert einen Nameserver. Dessen `<name>` sollte eindeutig sein. Standardmäßig wird `<address>`
als Datagramm-Adresse betrachtet. Ist also eine IPv4- oder IPv6-Adresse ohne besondere
Adresspräfixe (Absatz 11.) konfiguriert, wird UDP verwendet. Mit einem Adresspräfix für ein
Stream-Protokoll gilt der Nameserver als Stream-Server (beispielsweise TCP), und die für
DNS-Auflösung relevanten "server"-Parameter aus Abschnitt 5.2 werden berücksichtigt. Hinweis:
Derzeit werden im TCP-Modus 4 Abfragen im Pipelining-Verfahren über dieselben Verbindungen gesendet.
Alle 5 Sekunden wird eine Gruppe ungenutzter Verbindungen entfernt. Mit "maxconn" kann die Anzahl
dieser gleichzeitigen Verbindungen begrenzt werden. TLS sollte ebenfalls nutzbar sein, sofern der
Server es unterstützt.

<a id="entry-5-3-2-parse-resolv-conf"></a>

**`parse-resolv-conf`**

```haproxy
parse-resolv-conf
```

Fügt alle Nameserver aus /etc/resolv.conf zur Nameserverliste dieses resolvers-Abschnitts hinzu.
Die Reihenfolge entspricht der, die entstünde, wenn jeder Nameserver aus /etc/resolv.conf anstelle
dieser Direktive einzeln im resolvers-Abschnitt stünde.

<a id="entry-5-3-2-hold"></a>

**`hold <status> <period>`**

```haproxy
hold <status> <period>
```

Bestimmt beim Empfang einer DNS-Antwort mit `<status>`, ob der Serverzustand von UP zu DOWN
wechseln soll. Dazu wird geprüft, ob innerhalb der zurückliegenden Zeitspanne `<period>` ein
gültiger Status empfangen wurde, der den gerade empfangenen ungültigen Status aufhebt.

    `<status>`: letzter Status der Namensauflösung.
           nx        Nach einem NXDOMAIN-Status wird geprüft, ob im
                     zurückliegenden Zeitraum ein gültiger Status vorlag.

           refused   Nach einem REFUSED-Status wird geprüft, ob im
                     zurückliegenden Zeitraum ein gültiger Status vorlag.

           timeout   Nach Ablauf von "timeout retry" wird geprüft, ob im
                     zurückliegenden Zeitraum ein gültiger Status vorlag.

           other     Nach einem anderen ungültigen Status wird geprüft, ob im
                     zurückliegenden Zeitraum ein gültiger Status vorlag.

           valid     Gilt nur für die Aktionen "http-request do-resolve" und
                     "tcp-request content do-resolve". Definiert, wie lange
                     der Server eine gültige Antwort behält, bevor er eine
                     weitere Auflösung auslöst. Beeinflusst nicht die
                     dynamische Auflösung von Servern.

           obsolete  Definiert, wie lange nach Empfang eines aktualisierten
                     Antworteintrags gewartet wird, bevor veraltete DNS-Einträge
                     entfernt werden. Gilt für SRV-Einträge.

    `<period>`: Zurückliegende Zeitspanne, innerhalb derer eine gültige Antwort
               empfangen worden sein muss. Verwendet das HAProxy-Zeitformat
               und wird standardmäßig in Millisekunden angegeben.

Bei einem Server, dessen IP-Adresse dynamisch über DNS ermittelt wird, führt eine ungültige
DNS-Antwort wie NXDOMAIN zum Wechsel von UP zu DOWN. Die hold-Direktiven legen fest, wie weit in
der Vergangenheit nach einer gültigen Antwort gesucht wird. Wurde innerhalb von `<period>` eine
gültige Antwort empfangen, wird der gerade empfangene ungültige Status ignoriert.

Wurde im zurückliegenden Zeitraum keine gültige Antwort empfangen, wird der Server als DOWN
markiert. Ist beispielsweise "hold nx 30s" gesetzt und die zuletzt empfangene DNS-Antwort war
NXDOMAIN, wird der Server als DOWN markiert, sofern in den letzten 30 Sekunden keine gültige
Antwort empfangen wurde.

Ein Server im Zustand DOWN wird sofort als UP markiert, sobald ein gültiger Status vom DNS-Server
eintrifft.

Für "hold valid" und "hold obsolete" gilt ein gesondertes Verhalten.

Der Standardwert beträgt 10s für "valid", 0s für "obsolete" und 30s für die anderen Werte.

<a id="entry-5-3-2-resolve-retries"></a>

**`resolve_retries <nb>`**

```haproxy
resolve_retries <nb>
```

Definiert die Anzahl `<nb>` der Abfragen zur Auflösung eines Servernamens, bevor aufgegeben wird.
Standardwert: 3

Ein Wiederholungsversuch erfolgt bei einer Nameserver-Zeitüberschreitung oder wenn die gesamte
Folge des Wechsels zwischen DNS-Abfragetypen abgeschlossen ist und erneut beim standardmäßigen
Abfragetyp ANY begonnen werden muss.

<a id="entry-5-3-2-timeout"></a>

**`timeout <event> <time>`**

```haproxy
timeout <event> <time>
```

Definiert Zeitüberschreitungen für die Namensauflösung. `<event>` bezeichnet das Ereignis, für das
die Zeitspanne `<time>` gilt. Verfügbar sind: - resolve: Standardzeit bis zum Auslösen von
Namensauflösungen, wenn keine andere Zeit gilt. Standardwert: 1s - retry : Zeit zwischen zwei
DNS-Abfragen, wenn keine gültige Antwort empfangen wurde. Standardwert: 1s `<time>` : dem Ereignis
zugeordnete Zeit. Verwendet das HAProxy-Zeitformat. `<time>` wird in Millisekunden angegeben.

Beispiel:

```text
resolvers mydns
  nameserver dns1 10.0.0.1:53
  nameserver dns2 10.0.0.2:53
  nameserver dns3 tcp@10.0.0.3:53
  parse-resolv-conf
  resolve_retries       3
  timeout resolve       1s
  timeout retry         1s
  hold other           30s
  hold refused         30s
  hold nx              30s
  hold timeout         30s
  hold valid           10s
  hold obsolete        30s
```
