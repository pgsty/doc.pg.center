---
title: "8. Protokollierung"
linkTitle: "8. Protokollierung"
weight: 190
description: "Protokollstufen, Formate, Profile, Zeitmessungen, erfasste Werte, Zustände und Beispiele"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/configuration/logging/
  - /docs/haproxy/configuration/logging/
  - /haproxy/configuration-logging/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 8"
---

Eine der Stärken von HAProxy sind seine präzisen Protokolle. Sie bieten vermutlich die detailliertesten Informationen, die bei einem solchen Produkt verfügbar sind. Das ist bei der Fehlerbehebung in komplexen Umgebungen sehr wichtig. Zu den standardmäßig protokollierten Angaben gehören Client-Ports, Zeitmessungen der TCP/HTTP-Zustände, der genaue Stream-Zustand und die genaue Ursache bei der Beendigung, Angaben zu Entscheidungen über die Weiterleitung an einen Server und natürlich die Möglichkeit, beliebige Header zu erfassen.

Damit Administratoren schneller reagieren können, macht HAProxy interne wie externe Probleme deutlich sichtbar. Protokolle können gleichzeitig mit unterschiedlichen Stufenfiltern an verschiedene Ziele gesendet werden:

- globale Protokolle auf Prozessebene (Systemfehler, Start/Stopp usw.)
- Systemfehler und interne Fehler je Instanz (Ressourcenmangel, Programmfehler usw.)
- externe Probleme je Instanz (Server verfügbar/ausgefallen, maximale Verbindungszahl)
- Aktivitäten je Instanz (Clientverbindungen), entweder beim Aufbau oder bei der Beendigung.
- Steuerung der Protokollstufe je Anfrage, etwa http-request set-log-level silent if sensitive_request

Durch die Verteilung unterschiedlicher Protokollstufen auf verschiedene Protokollserver können mehrere Betriebsteams zusammenarbeiten und ihre Probleme möglichst schnell beheben. Beispielsweise kann das Systemteam systemweite Fehler überwachen, während das Anwendungsteam den Verfügbarkeitszustand seiner Server in Echtzeit beobachtet und das Sicherheitsteam Aktivitätsprotokolle mit einer Stunde Verzögerung auswertet.

## 8.1. Protokollstufen {#section-8-1}

TCP- und HTTP-Verbindungen können mit Datum, Uhrzeit, Quell-IP-Adresse, Zieladresse, Verbindungsdauer, Antwortzeiten, HTTP-Anfrage, HTTP-Statuscode, Anzahl übertragener Bytes, Umständen der Stream-Beendigung und sogar ausgetauschten Cookie-Werten protokolliert werden. Damit lassen sich beispielsweise Probleme eines bestimmten Nutzers verfolgen. Alle Meldungen können an bis zu zwei syslog-Server gesendet werden. Weitere Informationen zu Protokoll-Facilities stehen beim Schlüsselwort "log" in [Abschnitt 4.2](/de/docs/haproxy/proxies/#section-4-2).

## 8.2. Protokollformate {#section-8-2}

HAProxy unterstützt 5 Protokollformate. Mehrere Felder kommen in allen Formaten vor und werden in den folgenden Abschnitten erläutert. Einige können je nach Konfiguration leicht abweichen, da bestimmte Optionen eigene Kennzeichen verwenden. Folgende Formate werden unterstützt:

- Das Standardformat ist sehr einfach und wird äußerst selten verwendet. Es liefert nur grundlegende
  Angaben zur eingehenden Verbindung zum Zeitpunkt ihrer Annahme: Quell-IP:Port, Ziel-IP:Port
  und Frontend-Name. Dieser Modus wird irgendwann entfallen und daher nur kurz beschrieben.

- Das TCP-Format ist umfangreicher. Es wird durch "option tcplog" im Frontend aktiviert.
  HAProxy wartet dann gewöhnlich bis zum Verbindungsende, bevor es protokolliert. Das Format
  enthält wesentlich mehr Informationen, etwa Zeitmessungen, Verbindungszahlen und Warteschlangengröße.
  Für reine TCP-Proxys wird dieses Format empfohlen.

- Das HTTP-Format ist für HTTP-Proxys am umfangreichsten. Es wird durch "option httplog" im
  Frontend aktiviert. Es enthält dieselben Angaben wie das TCP-Format, ergänzt um HTTP-spezifische
  Felder wie Anfrage, Statuscode sowie erfasste Header und Cookies. Für HTTP-Proxys wird dieses
  Format empfohlen.

- Das CLF-HTTP-Format entspricht dem HTTP-Format, ordnet die Felder aber wie im CLF-Format an.
  In diesem Modus stehen alle Zeitmessungen, erfassten Werte, Flags usw. jeweils in einem eigenen
  Feld hinter den gemeinsamen Feldern, in derselben Reihenfolge wie im Standard-HTTP-Format.

- Mit dem benutzerdefinierten Protokollformat lassen sich eigene Protokollzeilen gestalten.

Die folgenden Abschnitte beschreiben diese Formate im Einzelnen. Die Formatbeschreibung erfolgt feldweise. Sofern nicht anders angegeben, ist ein Feld ein Textabschnitt, der durch eine beliebige Anzahl von Leerzeichen abgegrenzt wird. Da syslog-Server am Zeilenanfang Felder einfügen können, wird stets angenommen, dass das erste Feld den Prozessnamen und die Prozesskennung enthält.

Hinweis: Da Protokollzeilen recht lang sein können, sind die Beispiele in den folgenden Abschnitten möglicherweise auf mehrere Zeilen aufgeteilt. Beispielzeilen beginnen mit 3 schließenden spitzen Klammern ('\>\>\>'). Bei einer mehrzeiligen Darstellung endet jede nicht abschließende Zeile mit einem Backslash ('&#92;'), und die nächste Zeile ist um zwei Zeichen eingerückt.

### 8.2.1. Standard-Protokollformat {#section-8-2-1}

Dieses Format wird verwendet, wenn keine besondere Option gesetzt ist. Die Meldung wird sofort bei Annahme der Verbindung ausgegeben. Derzeit ist dies das einzige Format, das die Ziel-IP-Adresse und die Zielports der Anfrage protokolliert.

Beispiel:

```shell
    listen www
        mode http
        log global
        server srv1 127.0.0.1:8000

>>> Feb  6 12:12:09 localhost \
      haproxy[14385]: Connect from 10.0.1.2:33312 to 10.0.3.31:8012 \
      (www/HTTP)
```

Feld Format Auszug aus dem obigen Beispiel

```text
    1   process_name '[' pid ']:'                            haproxy[14385]:
    2   'Connect from'                                          Connect from
    3   source_ip ':' source_port                             10.0.1.2:33312
    4   'to'                                                              to
    5   destination_ip ':' destination_port                   10.0.3.31:8012
    6   '(' frontend_name '/' mode ')'                            (www/HTTP)
```


Ausführliche Feldbeschreibung:

- "source_ip" ist die IP-Adresse des Clients, der die Verbindung aufgebaut hat.
- "source_port" ist der TCP-Port des Clients, der die Verbindung aufgebaut hat.
- "destination_ip" ist die IP-Adresse, mit der sich der Client verbunden hat.
- "destination_port" ist der TCP-Port, mit dem sich der Client verbunden hat.
- "frontend_name" ist der Name des Frontends (oder Listeners), das die Verbindung angenommen
  und verarbeitet hat.
- "mode" ist der Betriebsmodus des Frontends (TCP oder HTTP).

Bei einem UNIX-Socket sind Quell- und Zieladresse als "unix:" gekennzeichnet. Die Ports geben die interne ID des Sockets an, der die Verbindung angenommen hat; dieselbe ID erscheint auch in den Statistiken.

Für neue Installationen wird von diesem veralteten Format abgeraten, da es irgendwann entfallen wird.

### 8.2.2. TCP-Protokollformat {#section-8-2-2}

Das TCP-Format wird durch "option tcplog" im Frontend verwendet und für reine TCP-Proxys empfohlen. Es liefert viele wertvolle Informationen zur Fehlerbehebung. Da es Zeitmessungen und Bytezähler enthält, wird die Meldung normalerweise am Sitzungsende ausgegeben. Mit "option logasap" kann sie früher ausgegeben werden, was in den meisten Umgebungen mit langen Sitzungen wie entfernten Terminals sinnvoll ist. Sitzungen, die den "monitor"-Regeln entsprechen, werden niemals protokolliert. Mit "option dontlognull" im Frontend können außerdem Meldungen für Sitzungen unterdrückt werden, in denen Client und Server keine Daten ausgetauscht haben. Bei "option dontlog-normal" im Frontend werden erfolgreiche Verbindungen nicht protokolliert.

Intern ist das TCP-Protokollformat als benutzerdefiniertes Format mit genau der folgenden Zeichenkette deklariert. Sie kann bei Bedarf auch als Grundlage für Erweiterungen dienen. Alternativ lässt sich die Variable HAPROXY_TCP_LOG_FMT verwenden. Die Verwendung beschreibt [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6) „Benutzerdefiniertes Protokollformat“:

```shell
# strict equivalent of "option tcplog"
log-format "%ci:%cp [%t] %ft %b/%s %Tw/%Tc/%Tt %B %ts \
            %ac/%fc/%bc/%sc/%rc %sq/%bq"
# or using the HAPROXY_TCP_LOG_FMT variable
log-format "${HAPROXY_TCP_LOG_FMT}"
```

Das CLF-Protokollformat ist intern als benutzerdefiniertes Format mit genau dieser Zeichenkette deklariert:

```shell
# strict equivalent of "option tcplog clf"
log-format "%{Q}o %{-Q}ci - - [%T] \"TCP \" 000 %B \"\" \"\" %cp \
            %ms %ft %b %s %Th %Tw %Tc %Tt %U %ts-- %ac %fc %bc \
            %sc %rc %sq %bq \"\" \"\" "
```

Einige Felder können je nach Konfigurationsoption leicht abweichen. Sie sind unten mit einem Sternchen ('\*') hinter dem Feldnamen gekennzeichnet.

Beispiel:

```shell
    frontend fnt
        mode tcp
        option tcplog
        log global
        default_backend bck

    backend bck
        server srv1 127.0.0.1:8000

>>> Feb  6 12:12:56 localhost \
      haproxy[14387]: 10.0.1.2:33313 [06/Feb/2009:12:12:51.443] fnt \
      bck/srv1 0/0/5007 212 -- 0/0/0/0/3 0/0
```

Feld Format Auszug aus dem obigen Beispiel

```text
    1   process_name '[' pid ']:'                            haproxy[14387]:
    2   client_ip ':' client_port                             10.0.1.2:33313
    3   '[' accept_date ']'                       [06/Feb/2009:12:12:51.443]
    4   frontend_name                                                    fnt
    5   backend_name '/' server_name                                bck/srv1
    6   Tw '/' Tc '/' Tt*                                           0/0/5007
    7   bytes_read*                                                      212
    8   termination_state                                                 --
    9   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*    0/0/0/0/3
   10   srv_queue '/' backend_queue                                      0/0
```


Ausführliche Feldbeschreibung:

- "client_ip" ist die IP-Adresse des Clients, der die TCP-Verbindung zu HAProxy aufgebaut hat.
  Wurde die Verbindung stattdessen über einen UNIX-Socket angenommen, ersetzt das Wort "unix"
  die IP-Adresse. Bei einem Socket mit "accept-proxy" und korrekt verwendetem PROXY-Protokoll
  oder mit "accept-netscaler-cip" und korrekt verwendetem NetScaler Client IP Insertion-Protokoll
  geben die Protokolle die Informationen der weitergeleiteten Verbindung wieder.

- "client_port" ist der TCP-Port des Clients, der die Verbindung aufgebaut hat. Wurde sie über
  einen UNIX-Socket angenommen, steht hier stattdessen die ID des annehmenden Sockets, die auch
  in der Statistikschnittstelle erscheint.

- "accept_date" ist der genaue Zeitpunkt, zu dem HAProxy die Verbindung empfangen hat.
  Er kann geringfügig vom im Netzwerk beobachteten Zeitpunkt abweichen, wenn die Verbindung
  im System-Backlog warten musste. Gewöhnlich entspricht er dem Zeitpunkt in den Protokollen
  vorgeschalteter Firewalls. Im HTTP-Modus wird accept_date auf den frühesten Zeitpunkt
  zurückgesetzt, zu dem die Verbindung eine neue Anfrage empfangen kann: bei HTTP/1 auf das
  Ende der vorherigen Antwort, bei HTTP/2 unmittelbar nach der vorherigen Anfrage.

- "frontend_name" ist der Name des Frontends (oder Listeners), das die Verbindung angenommen
  und verarbeitet hat.

- "backend_name" ist der Name des Backends (oder Listeners), das zur Verwaltung der Verbindung
  zum Server gewählt wurde. Wenn keine Umschaltregel angewendet wurde, entspricht es dem
  Frontend, was bei TCP-Anwendungen häufig der Fall ist.

- "server_name" ist der Name des letzten Servers, an den die Verbindung gesendet wurde.
  Nach Verbindungsfehlern und einer Umverteilung kann er vom zuerst gewählten Server abweichen.
  Dieser Server gehört zum Backend, das die Anfrage verarbeitet hat. Wurde die Verbindung
  vor Erreichen eines Servers abgebrochen, steht statt des Servernamens "`<NOSRV>`".

- "Tw" ist die gesamte Wartezeit in den verschiedenen Warteschlangen in Millisekunden.
  Der Wert kann "-1" sein, wenn die Verbindung vor Erreichen der Warteschlange abgebrochen wurde.
  Weitere Einzelheiten stehen unten unter „Zeitmessungen“.

- "Tc" ist die gesamte Wartezeit bis zum Verbindungsaufbau zum endgültigen Server in
  Millisekunden, einschließlich Wiederholungsversuchen. Der Wert kann "-1" sein, wenn die
  Verbindung abgebrochen wurde, bevor eine Verbindung zum Server hergestellt werden konnte.
  Weitere Einzelheiten stehen unten unter „Zeitmessungen“.

- "Tt" ist die gesamte Zeit zwischen Annahme und letztem Schließen in Millisekunden.
  Sie umfasst alle Verarbeitungsschritte. Eine Ausnahme besteht bei "option logasap":
  Dann endet die Zeitmessung mit der Protokollausgabe. Ein vorangestelltes '+' zeigt in
  diesem Fall an, dass der endgültige Wert größer sein wird. Weitere Einzelheiten stehen
  unten unter „Zeitmessungen“.

- "bytes_read" ist die Gesamtzahl der zum Zeitpunkt der Protokollausgabe vom Server an
  den Client übertragenen Bytes. Bei "option logasap" erhält der Wert ein vorangestelltes '+',
  das auf einen möglicherweise größeren Endwert hinweist. Es handelt sich um einen 64-Bit-Zähler;
  Werkzeuge zur Protokollauswertung müssen ihn daher ohne Überlauf verarbeiten können.

- "termination_state" beschreibt den Zustand der Sitzung bei ihrer Beendigung. Das Feld
  zeigt den Sitzungszustand, die Seite, die die Sitzung beendet hat, und den Grund dafür
  (Zeitüberschreitung, Fehler usw.). Normalerweise sollten die Flags "--" lauten. Dies bedeutet,
  dass eine der Seiten die Sitzung beendet hat und keine Daten mehr in den Puffern lagen.
  Weitere Einzelheiten stehen unten unter „Stream-Zustand bei der Trennung“.

- "actconn" ist die Gesamtzahl gleichzeitiger Verbindungen im Prozess zum Zeitpunkt der
  Protokollierung der Sitzung. Sie hilft zu erkennen, wann systemseitige Grenzen je Prozess
  erreicht wurden. Liegt actconn etwa nahe bei 512, während mehrere Verbindungsfehler auftreten,
  begrenzt das System den Prozess wahrscheinlich auf 1024 Dateideskriptoren, die alle belegt sind.
  Zur Systemanpassung siehe [Abschnitt 3](/de/docs/haproxy/global/) „Globaler Abschnitt“.

- "feconn" ist die Gesamtzahl gleichzeitiger Verbindungen im Frontend zum Zeitpunkt der
  Protokollierung der Sitzung. Damit lassen sich der Ressourcenbedarf bei hoher Last abschätzen
  und das Erreichen von "maxconn" des Frontends erkennen. Große sprunghafte Anstiege deuten
  meistens auf einen Engpass bei den Backend-Servern hin, manchmal aber auch auf einen
  Denial-of-Service-Angriff.

- "beconn" ist die Gesamtzahl gleichzeitiger Verbindungen, die das Backend zum Zeitpunkt
  der Protokollierung der Sitzung verwaltet. Dazu gehören alle gleichzeitig auf Servern aktiven
  sowie die in Warteschlangen wartenden Verbindungen. Damit lässt sich abschätzen, wie viele
  zusätzliche Server eine Anwendung bei hoher Last benötigt. Große sprunghafte Anstiege deuten
  meistens auf einen Engpass bei den Backend-Servern hin, manchmal aber auch auf einen
  Denial-of-Service-Angriff.

- "srv_conn" ist die Gesamtzahl der zum Zeitpunkt der Protokollierung der Sitzung noch
  auf dem Server aktiven Verbindungen. Sie kann den konfigurierten Parameter "maxconn" des
  Servers niemals überschreiten. Liegt sie sehr häufig nahe bei oder genau auf "maxconn",
  greift die Verkehrsregelung häufig ein. Dann ist entweder maxconn des Servers zu niedrig,
  oder es gibt zu wenige Server, um die Last mit optimaler Antwortzeit zu verarbeiten.
  Ist "srv_conn" nur bei einem Server hoch, hat dieser meist ein Problem, durch das die
  Verarbeitung von Verbindungen länger dauert als bei den anderen Servern.

- "retries" ist die Zahl der Wiederholungsversuche beim Verbindungsaufbau zum Server in
  dieser Sitzung. Sie muss normalerweise null sein, außer wenn ein Server genau zum Zeitpunkt
  des Verbindungsversuchs gestoppt wird. Häufige Wiederholungsversuche deuten meist auf ein
  Netzwerkproblem zwischen HAProxy und dem Server oder einen falsch konfigurierten System-Backlog
  des Servers hin, der keine neuen Verbindungen aufnehmen kann. Ein optional vorangestelltes '+'
  zeigt an, dass die Sitzung nach Erreichen der maximalen Anzahl von Wiederholungsversuchen
  beim ursprünglichen Server umverteilt wurde. Der protokollierte Servername bezeichnet dann
  den Server, an den die Verbindung umverteilt wurde, und nicht den ersten. Beide können
  beispielsweise bei Hashing dennoch identisch sein. Als Faustregel gilt daher: Steht vor
  der Anzahl der Wiederholungsversuche ein '+', sollte sie nicht dem protokollierten Server
  zugerechnet werden.

- "srv_queue" ist die Gesamtzahl der Anfragen, die vor dieser Anfrage in der
  Serverwarteschlange verarbeitet wurden. War die Anfrage nicht in der Serverwarteschlange,
  ist der Wert null. Die ungefähre Antwortzeit des Servers lässt sich abschätzen, indem die
  Wartezeit durch die Anzahl der Anfragen in der Warteschlange geteilt wird. Durchläuft eine
  Sitzung nach einer Umverteilung zwei Serverwarteschlangen, werden ihre Positionen addiert.
  Eine Anfrage sollte nur nach einer Umverteilung sowohl die Server- als auch die
  Backend-Warteschlange durchlaufen.

- "backend_queue" ist die Gesamtzahl der Anfragen, die vor dieser Anfrage in der globalen
  Warteschlange des Backends verarbeitet wurden. War die Anfrage nicht in der globalen
  Warteschlange, ist der Wert null. Damit lässt sich die durchschnittliche Warteschlangenlänge
  abschätzen. Geteilt durch den Parameter "maxconn" eines Servers ergibt sie leicht die Anzahl
  fehlender Server. Nach einer Umverteilung kann eine Sitzung die Backend-Warteschlange zweimal
  durchlaufen; dann werden beide Positionen addiert. Eine Anfrage sollte nur nach einer
  Umverteilung sowohl die Server- als auch die Backend-Warteschlange durchlaufen.

### 8.2.3. HTTP-Protokollformat {#section-8-2-3}

Das HTTP-Format ist das vollständigste und für HTTP-Proxys am besten geeignete Format. Es wird durch "option httplog" im Frontend aktiviert. Es liefert dieselben Informationen wie das TCP-Format und zusätzlich HTTP-spezifische Angaben. Wie beim TCP-Format wird die Meldung gewöhnlich am Stream-Ende ausgegeben, außer wenn "option logasap" angegeben ist. Dies ist meist nur für Download-Websites sinnvoll. Ein Stream, der den "monitor"-Regeln entspricht, wird niemals protokolliert. Mit "option dontlognull" im Frontend können außerdem Streams von der Protokollierung ausgenommen werden, bei denen der Client keine Daten gesendet hat. Bei "option dontlog-normal" im Frontend werden erfolgreiche Verbindungen nicht protokolliert.

Intern ist das HTTP-Protokollformat als benutzerdefiniertes Format mit genau der folgenden Zeichenkette deklariert. Sie kann bei Bedarf auch als Grundlage für Erweiterungen dienen. Alternativ lässt sich die Variable HAPROXY_HTTP_LOG_FMT verwenden. Die Verwendung beschreibt [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6) „Benutzerdefiniertes Protokollformat“:

```shell
# strict equivalent of "option httplog"
log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC \
            %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r"
# or using the HAPROXY_HTTP_LOG_FMT variable
log-format "${HAPROXY_HTTP_LOG_FMT}"
```

Das CLF-Protokollformat ist intern als benutzerdefiniertes Format mit genau dieser Zeichenkette deklariert:

```shell
# strict equivalent of "option httplog clf"
log-format "%{+Q}o %{-Q}ci - - [%trg] %r %ST %B \"\" \"\" %cp \
            %ms %ft %b %s %TR %Tw %Tc %Tr %Ta %tsc %ac %fc \
            %bc %sc %rc %sq %bq %CC %CS %hrl %hsl"
```

Die meisten Felder entsprechen denen des TCP-Protokolls, einige unterscheiden sich. Manche Felder können je nach Konfigurationsoption leicht abweichen. Sie sind unten mit einem Sternchen ('\*') hinter dem Feldnamen gekennzeichnet.

Beispiel:

```shell
    frontend http-in
        mode http
        option httplog
        log global
        default_backend bck

    backend static
        server srv1 127.0.0.1:8000

>>> Feb  6 12:14:14 localhost \
      haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
      static/srv1 10/0/30/69/109 200 2750 - - ---- 1/1/1/1/0 0/0 {1wt.eu} \
      {} "GET /index.html HTTP/1.1"
```

Feld Format Auszug aus dem obigen Beispiel

```text
    1   process_name '[' pid ']:'                            haproxy[14389]:
    2   client_ip ':' client_port                             10.0.1.2:33317
    3   '[' request_date ']'                      [06/Feb/2009:12:14:14.655]
    4   frontend_name                                                http-in
    5   backend_name '/' server_name                             static/srv1
    6   TR '/' Tw '/' Tc '/' Tr '/' Ta*                       10/0/30/69/109
    7   status_code                                                      200
    8   bytes_read*                                                     2750
    9   captured_request_cookie                                            -
   10   captured_response_cookie                                           -
   11   termination_state                                               ----
   12   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*    1/1/1/1/0
   13   srv_queue '/' backend_queue                                      0/0
   14   '{' captured_request_headers* '}'                   {haproxy.1wt.eu}
   15   '{' captured_response_headers* '}'                                {}
   16   '"' http_request '"'                      "GET /index.html HTTP/1.1"
```


Ausführliche Feldbeschreibung:

- "client_ip" ist die IP-Adresse des Clients, der die TCP-Verbindung zu HAProxy aufgebaut hat.
  Wurde die Verbindung stattdessen über einen UNIX-Socket angenommen, ersetzt das Wort "unix"
  die IP-Adresse. Bei einem Socket mit "accept-proxy" und korrekt verwendetem PROXY-Protokoll
  oder mit "accept-netscaler-cip" und korrekt verwendetem NetScaler Client IP Insertion-Protokoll
  geben die Protokolle die Informationen der weitergeleiteten Verbindung wieder.

- "client_port" ist der TCP-Port des Clients, der die Verbindung aufgebaut hat. Wurde sie über
  einen UNIX-Socket angenommen, steht hier stattdessen die ID des annehmenden Sockets, die auch
  in der Statistikschnittstelle erscheint.

- "request_date" ist der genaue Zeitpunkt, zu dem HAProxy das erste Byte der HTTP-Anfrage
  empfangen hat (Protokollfeld %tr).

- "frontend_name" ist der Name des Frontends (oder Listeners), das die Verbindung angenommen
  und verarbeitet hat.

- "backend_name" ist der Name des Backends (oder Listeners), das zur Verwaltung der Verbindung
  zum Server gewählt wurde. Wenn keine Umschaltregel angewendet wurde, entspricht es dem Frontend.

- "server_name" ist der Name des letzten Servers, an den die Verbindung gesendet wurde.
  Nach Verbindungsfehlern und einer Umverteilung kann er vom zuerst gewählten Server abweichen.
  Dieser Server gehört zum Backend, das die Anfrage verarbeitet hat. Wurde die Anfrage vor
  Erreichen eines Servers abgebrochen, steht statt des Servernamens "`<NOSRV>`". Hat das
  Statistiksubsystem die Anfrage abgefangen, steht dort stattdessen "`<STATS>`".

- "TR" ist die gesamte Wartezeit in Millisekunden vom Empfang des ersten Bytes bis zur
  vollständigen HTTP-Anfrage des Clients, ohne Nachrichtenkörper. Der Wert kann "-1" sein,
  wenn die Verbindung vor Empfang der vollständigen Anfrage abgebrochen oder eine ungültige
  Anfrage empfangen wurde. Er sollte immer sehr klein sein, da eine Anfrage gewöhnlich in
  ein einziges Paket passt. Hohe Werte deuten meist auf Netzwerkprobleme zwischen Client und
  HAProxy oder auf von Hand eingegebene Anfragen hin. Weitere Einzelheiten stehen in
  [Abschnitt 8.4](/de/docs/haproxy/configuration-logging/#section-8-4) „Zeitmessungen“.

- "Tw" ist die gesamte Wartezeit in den verschiedenen Warteschlangen in Millisekunden.
  Der Wert kann "-1" sein, wenn die Verbindung vor Erreichen der Warteschlange abgebrochen wurde.
  Weitere Einzelheiten stehen in [Abschnitt 8.4](/de/docs/haproxy/configuration-logging/#section-8-4) „Zeitmessungen“.

- "Tc" ist die gesamte Wartezeit bis zum Verbindungsaufbau zum endgültigen Server in
  Millisekunden, einschließlich Wiederholungsversuchen. Der Wert kann "-1" sein, wenn die
  Anfrage abgebrochen wurde, bevor eine Verbindung hergestellt werden konnte. Weitere
  Einzelheiten stehen in [Abschnitt 8.4](/de/docs/haproxy/configuration-logging/#section-8-4) „Zeitmessungen“.

- "Tr" ist die gesamte Wartezeit in Millisekunden, bis der Server eine vollständige
  HTTP-Antwort ohne Daten gesendet hat. Der Wert kann "-1" sein, wenn die Anfrage vor Empfang
  einer vollständigen Antwort abgebrochen wurde. Er entspricht gewöhnlich der Bearbeitungszeit
  des Servers für die Anfrage, kann aber durch die vom Client an den Server gesendete Datenmenge
  beeinflusst werden. Hohe Werte bei "GET"-Anfragen deuten meist auf einen überlasteten Server hin.
  Weitere Einzelheiten stehen in [Abschnitt 8.4](/de/docs/haproxy/configuration-logging/#section-8-4) „Zeitmessungen“.

- "Ta" ist die Zeit, in der die Anfrage in HAProxy aktiv war: die gesamte Zeit in
  Millisekunden zwischen dem Empfang des ersten Anfragebytes und dem Senden des letzten
  Antwortbytes. Sie umfasst alle Verarbeitungsschritte außer Handshake (siehe Th) und
  Leerlaufzeit (siehe Ti). Eine Ausnahme besteht bei "option logasap": Dann endet die
  Zeitmessung mit der Protokollausgabe. Ein vorangestelltes '+' zeigt in diesem Fall an,
  dass der endgültige Wert größer sein wird. Weitere Einzelheiten stehen in
  [Abschnitt 8.4](/de/docs/haproxy/configuration-logging/#section-8-4) „Zeitmessungen“.

- "status_code" ist der an den Client zurückgegebene HTTP-Statuscode. Er wird gewöhnlich
  vom Server gesetzt, kann aber auch von HAProxy stammen, wenn der Server nicht erreichbar
  ist oder HAProxy seine Antwort blockiert.

- "bytes_read" ist die Gesamtzahl der zum Zeitpunkt der Protokollausgabe an den Client
  übertragenen Bytes, einschließlich HTTP-Headern. Bei "option logasap" erhält der Wert ein
  vorangestelltes '+', das auf einen möglicherweise größeren Endwert hinweist. Es handelt sich
  um einen 64-Bit-Zähler; Werkzeuge zur Protokollauswertung müssen ihn daher ohne Überlauf
  verarbeiten können.

- "captured_request_cookie" ist ein optionaler Eintrag im Format "name=value", der anzeigt,
  dass der Client dieses Cookie in der Anfrage mitgesendet hat. Cookie-Name und maximale Länge
  werden mit "capture cookie" in der Frontend-Konfiguration festgelegt. Ist die Option nicht
  gesetzt, enthält das Feld einen einzelnen Bindestrich ('-'). Es kann nur ein Cookie erfasst
  werden. Damit wird gewöhnlich der Austausch von Sitzungs-IDs zwischen Client und Server
  verfolgt, um durch Anwendungsfehler verursachte Sitzungsverwechslungen zwischen Clients
  zu erkennen. Weitere Einzelheiten stehen unten unter „HTTP-Header und Cookies erfassen“.

- "captured_response_cookie" ist ein optionaler Eintrag im Format "name=value", der anzeigt,
  dass der Server mit seiner Antwort ein Cookie zurückgegeben hat. Cookie-Name und maximale
  Länge werden mit "capture cookie" in der Frontend-Konfiguration festgelegt. Ist die Option
  nicht gesetzt, enthält das Feld einen einzelnen Bindestrich ('-'). Es kann nur ein Cookie
  erfasst werden. Damit wird gewöhnlich der Austausch von Sitzungs-IDs zwischen Client und
  Server verfolgt, um durch Anwendungsfehler verursachte Sitzungsverwechslungen zwischen Clients
  zu erkennen. Weitere Einzelheiten stehen unten unter „HTTP-Header und Cookies erfassen“.

- "termination_state" beschreibt den Zustand des Streams bei seiner Beendigung. Wie bei
  TCP-Protokollen zeigt das Feld den Stream-Zustand, die Seite, die den Stream beendet hat,
  und den Grund dafür (Zeitüberschreitung, Fehler usw.). Die letzten beiden Zeichen enthalten
  außerdem Angaben zu Persistenzaktionen an Cookies. Normalerweise sollten die Flags mit "--"
  beginnen. Dies bedeutet, dass eine der Seiten den Stream beendet hat und keine Daten mehr
  in den Puffern lagen. Weitere Einzelheiten stehen unten unter „Stream-Zustand bei der Trennung“.

- "actconn" ist die Gesamtzahl gleichzeitiger Verbindungen im Prozess zum Zeitpunkt der
  Protokollierung des Streams. Sie hilft zu erkennen, wann systemseitige Grenzen je Prozess
  erreicht wurden. Liegt actconn etwa nahe bei 512 oder 1024, während mehrere Verbindungsfehler auftreten,
  begrenzt das System den Prozess wahrscheinlich auf 1024 Dateideskriptoren, die alle belegt sind.
  Zur Systemanpassung siehe [Abschnitt 3](/de/docs/haproxy/global/) „Globaler Abschnitt“.

- "feconn" ist die Gesamtzahl gleichzeitiger Verbindungen im Frontend zum Zeitpunkt der
  Protokollierung des Streams. Damit lassen sich der Ressourcenbedarf bei hoher Last abschätzen
  und das Erreichen von "maxconn" des Frontends erkennen. Große sprunghafte Anstiege deuten
  meistens auf einen Engpass bei den Backend-Servern hin, manchmal aber auch auf einen
  Denial-of-Service-Angriff.

- "beconn" ist die Gesamtzahl gleichzeitiger Verbindungen, die das Backend zum Zeitpunkt
  der Protokollierung des Streams verwaltet. Dazu gehören alle gleichzeitig auf Servern aktiven
  sowie die in Warteschlangen wartenden Verbindungen. Damit lässt sich abschätzen, wie viele
  zusätzliche Server eine Anwendung bei hoher Last benötigt. Große sprunghafte Anstiege deuten
  meistens auf einen Engpass bei den Backend-Servern hin, manchmal aber auch auf einen
  Denial-of-Service-Angriff.

- "srv_conn" ist die Gesamtzahl der zum Zeitpunkt der Protokollierung des Streams noch
  auf dem Server aktiven Verbindungen. Sie kann den konfigurierten Parameter "maxconn" des
  Servers niemals überschreiten. Liegt sie sehr häufig nahe bei oder genau auf "maxconn",
  greift die Verkehrsregelung häufig ein. Dann ist entweder maxconn des Servers zu niedrig,
  oder es gibt zu wenige Server, um die Last mit optimaler Antwortzeit zu verarbeiten.
  Ist "srv_conn" nur bei einem Server hoch, hat dieser meist ein Problem, durch das die
  Verarbeitung von Anfragen länger dauert als bei den anderen Servern.

- "retries" ist die Zahl der Wiederholungsversuche beim Verbindungsaufbau zum Server in
  diesem Stream. Sie muss normalerweise null sein, außer wenn ein Server genau zum Zeitpunkt
  des Verbindungsversuchs gestoppt wird. Häufige Wiederholungsversuche deuten meist auf ein
  Netzwerkproblem zwischen HAProxy und dem Server oder einen falsch konfigurierten System-Backlog
  des Servers hin, der keine neuen Verbindungen aufnehmen kann. Ein optional vorangestelltes '+'
  zeigt an, dass der Stream nach Erreichen der maximalen Anzahl von Wiederholungsversuchen
  beim ursprünglichen Server umverteilt wurde. Der protokollierte Servername bezeichnet dann
  den Server, an den die Verbindung umverteilt wurde, und nicht den ersten. Beide können
  beispielsweise bei Hashing dennoch identisch sein. Als Faustregel gilt daher: Steht vor
  der Anzahl der Wiederholungsversuche ein '+', sollte sie nicht dem protokollierten Server
  zugerechnet werden.

- "srv_queue" ist die Gesamtzahl der Anfragen, die vor dieser Anfrage in der
  Serverwarteschlange verarbeitet wurden. War die Anfrage nicht in der Serverwarteschlange,
  ist der Wert null. Die ungefähre Antwortzeit des Servers lässt sich abschätzen, indem die
  Wartezeit durch die Anzahl der Anfragen in der Warteschlange geteilt wird. Durchläuft eine
  Sitzung nach einer Umverteilung zwei Serverwarteschlangen, werden ihre Positionen addiert.
  Eine Anfrage sollte nur nach einer Umverteilung sowohl die Server- als auch die
  Backend-Warteschlange durchlaufen.

- "backend_queue" ist die Gesamtzahl der Anfragen, die vor dieser Anfrage in der globalen
  Warteschlange des Backends verarbeitet wurden. War die Anfrage nicht in der globalen
  Warteschlange, ist der Wert null. Damit lässt sich die durchschnittliche Warteschlangenlänge
  abschätzen. Geteilt durch den Parameter "maxconn" eines Servers ergibt sie leicht die Anzahl
  fehlender Server. Nach einer Umverteilung kann ein Stream die Backend-Warteschlange zweimal
  durchlaufen; dann werden beide Positionen addiert. Eine Anfrage sollte nur nach einer
  Umverteilung sowohl die Server- als auch die Backend-Warteschlange durchlaufen.

- "captured_request_headers" ist die Liste der Anfrage-Header, die durch "capture request header"
  im Frontend erfasst wurden. Mehrere Header können erfasst werden; sie sind durch einen
  senkrechten Strich ('\|') getrennt. Ist keine Erfassung aktiviert, entfallen die geschweiften
  Klammern, wodurch sich die übrigen Felder verschieben. Dieses Feld kann Leerzeichen enthalten.
  Seine Verwendung erfordert daher einen ausgefeilteren Protokollparser als ohne das Feld.
  Weitere Einzelheiten stehen unten unter „HTTP-Header und Cookies erfassen“.

- "captured_response_headers" ist die Liste der Antwort-Header, die durch "capture response header"
  im Frontend erfasst wurden. Mehrere Header können erfasst werden; sie sind durch einen
  senkrechten Strich ('\|') getrennt. Ist keine Erfassung aktiviert, entfallen die geschweiften
  Klammern, wodurch sich die übrigen Felder verschieben. Dieses Feld kann Leerzeichen enthalten.
  Seine Verwendung erfordert daher einen ausgefeilteren Protokollparser als ohne das Feld.
  Weitere Einzelheiten stehen unten unter „HTTP-Header und Cookies erfassen“.

- "http_request" ist die vollständige HTTP-Anfragezeile mit Methode, Anfrage und
  HTTP-Versionszeichenkette. Nicht druckbare Zeichen werden kodiert (siehe unten „Nicht druckbare
  Zeichen“). Dies ist immer das letzte Feld. Es ist stets von Anführungszeichen umschlossen und
  das einzige Feld, das selbst Anführungszeichen enthalten kann. Neue Felder werden vor diesem
  Feld in das Protokollformat eingefügt. Ist die Anfrage sehr groß und passt nicht in den
  standardmäßigen syslog-Puffer (1024 Zeichen), kann das Feld abgeschnitten werden. Deshalb
  muss es immer das letzte Feld bleiben.

### 8.2.4. HTTPS-Protokollformat {#section-8-2-4}

Das HTTPS-Format eignet sich am besten für HTTP-Verbindungen über SSL. Es erweitert das HTTP-Format (siehe [Abschnitt 8.2.3](/de/docs/haproxy/configuration-logging/#section-8-2-3)) um SSL-bezogene Informationen und wird durch "option httpslog" im Frontend aktiviert. Wie bei TCP und HTTP wird die Meldung gewöhnlich am Stream-Ende ausgegeben, außer wenn "option logasap" angegeben ist. Ein Stream, der den "monitor"-Regeln entspricht, wird niemals protokolliert. Mit "option dontlognull" im Frontend können außerdem Streams von der Protokollierung ausgenommen werden, bei denen der Client keine Daten gesendet hat. Bei "option dontlog-normal" im Frontend werden erfolgreiche Verbindungen nicht protokolliert.

Intern ist das HTTPS-Protokollformat als benutzerdefiniertes Format mit genau der folgenden Zeichenkette deklariert. Sie kann bei Bedarf auch als Grundlage für Erweiterungen dienen. Alternativ lässt sich die Variable HAPROXY_HTTPS_LOG_FMT verwenden. Die Verwendung beschreibt [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6) „Benutzerdefiniertes Protokollformat“:

```shell
# strict equivalent of "option httpslog"
log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC \
           %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r \
           %[fc_err]/%[ssl_fc_err,hex]/%[ssl_c_err]/\
           %[ssl_c_ca_err]/%[ssl_fc_is_resumed] %[ssl_fc_sni]/%sslv/%sslc"
# or using the HAPROXY_HTTPS_LOG_FMT variable
log-format "${HAPROXY_HTTPS_LOG_FMT}"
```

Dieses Format entspricht im Wesentlichen dem HTTP-Format (siehe [Abschnitt 8.2.3](/de/docs/haproxy/configuration-logging/#section-8-2-3)), an das neue Felder angehängt werden. Diese neuen Felder (Zeilen 17 und 18) werden hier erläutert. Für die HTTP-Felder siehe den HTTP-Abschnitt.

Beispiel:

```shell
    frontend https-in
        mode http
        option httpslog
        log global
        bind *:443 ssl crt mycerts/srv.pem ...
        default_backend bck

    backend static
        server srv1 127.0.0.1:8000 ssl crt mycerts/clt.pem ...

>>> Feb  6 12:14:14 localhost \
      haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] https-in \
      static/srv1 10/0/30/69/109 200 2750 - - ---- 1/1/1/1/0 0/0 {1wt.eu} \
      {} "GET /index.html HTTP/1.1" 0/0/0/0/0 \
      1wt.eu/TLSv1.3/TLS_AES_256_GCM_SHA384
```

Feld Format Auszug aus dem obigen Beispiel

```text
    1   process_name '[' pid ']:'                              haproxy[14389]:
    2   client_ip ':' client_port                               10.0.1.2:33317
    3   '[' request_date ']'                        [06/Feb/2009:12:14:14.655]
    4   frontend_name                                                 https-in
    5   backend_name '/' server_name                               static/srv1
    6   TR '/' Tw '/' Tc '/' Tr '/' Ta*                         10/0/30/69/109
    7   status_code                                                        200
    8   bytes_read*                                                       2750
    9   captured_request_cookie                                              -
   10   captured_response_cookie                                             -
   11   termination_state                                                 ----
   12   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*      1/1/1/1/0
   13   srv_queue '/' backend_queue                                        0/0
   14   '{' captured_request_headers* '}'                     {haproxy.1wt.eu}
   15   '{' captured_response_headers* '}'                                  {}
   16   '"' http_request '"'                        "GET /index.html HTTP/1.1"
   17   fc_err '/' ssl_fc_err '/' ssl_c_err
        '/' ssl_c_ca_err '/' ssl_fc_is_resumed                       0/0/0/0/0
   18   ssl_fc_sni '/' ssl_version
        '/' ssl_ciphers                  1wt.eu/TLSv1.3/TLS_AES_256_GCM_SHA384
```


Ausführliche Feldbeschreibung:

- "fc_err" ist der Verbindungsstatus auf der Frontend-Seite und entspricht dem Sample-Abruf
  "fc_err". Weitere Informationen liefern die Beschreibungen der Sample-Abruffunktionen
  "fc_err" und "fc_err_str".

- "ssl_fc_err" ist der letzte Fehler des ersten SSL-Fehlerstapels, der aus Sicht des
  Frontends auf der Verbindung aufgetreten ist. Damit lassen sich beispielsweise Fehler beim
  SSL-Handshake erkennen. Wenn alles erfolgreich war, ist der Wert 0. Weitere Informationen
  stehen in der Beschreibung des Sample-Abrufs "ssl_fc_err".

- "ssl_c_err" ist der Status der Prüfung des Clientzertifikats. Der Handshake kann auch
  bei einem Prüfungsfehlercode ungleich null erfolgreich sein, wenn der Fehler ignoriert wird.
  Siehe den Sample-Abruf "ssl_c_err" und die Option "crt-ignore-err".

- "ssl_c_ca_err" ist der Status der Prüfung der Clientzertifikatskette. Der Handshake kann
  auch bei einem Prüfungsfehlercode ungleich null erfolgreich sein, wenn der Fehler ignoriert
  wird. Siehe den Sample-Abruf "ssl_c_ca_err" und die Option "ca-ignore-err".

- "ssl_fc_is_resumed" ist wahr, wenn die eingehende TLS-Sitzung über den zustandsbehafteten
  Cache oder ein zustandsloses Ticket wiederaufgenommen wurde. Eine TLS-Sitzung kann von
  mehreren Anfragen gemeinsam genutzt werden.

- "ssl_fc_sni" ist die vom Client zur Zertifikatsauswahl übermittelte SNI (Server Name
  Indication). Sie entspricht gewöhnlich dem Hostnamen der ersten Anfrage einer Verbindung.
  Fehlt das Feld, hat der Client möglicherweise keine SNI gesendet. haproxy verwendet dann
  das Standardzertifikat oder weist bei strict-sni die Verbindung ab.

- "ssl_version" ist die SSL-Version des Frontends.

- "ssl_ciphers" ist der für die Verbindung verwendete SSL-Cipher.

### 8.2.5. Fehlerprotokollformat {#section-8-2-5}

Schlägt eine eingehende Verbindung wegen eines SSL-Handshakes oder eines ungültigen PROXY-Protokoll-Headers fehl, protokolliert HAProxy das Ereignis in einem kürzeren, festen Zeilenformat. Dies gilt nicht, wenn mit "error-log-format" ein eigenes Fehlerprotokollformat definiert wurde. Standardmäßig werden Meldungen mit der Stufe LOG_INFO ausgegeben. Ist im Backend "log-separate-errors" gesetzt, wird stattdessen LOG_ERR verwendet. Verbindungen ohne Datenaustausch, etwa Prüfanfragen, werden bei gesetzter Option "dontlognull" nicht protokolliert.

Das Standardformat sieht so aus:

```text
  >>> Dec  3 18:27:14 localhost \
        haproxy[6103]: 127.0.0.1:56059 [03/Dec/2012:17:35:10.380] frt/f1: \
        Connection error during SSL handshake

Feld    Format                                  Auszug aus dem obigen Beispiel
```

```text
    1   process_name '[' pid ']:'                             haproxy[6103]:
    2   client_ip ':' client_port                            127.0.0.1:56059
    3   '[' accept_date ']'                       [03/Dec/2012:17:35:10.380]
    4   frontend_name "/" bind_name ":"                              frt/f1:
    5   message                        Connection error during SSL handshake
```

Diese Felder liefern nur die grundlegenden Informationen zur Untersuchung fehlgeschlagener Verbindungen.

Mit der Direktive "error-log-format" wird das oben beschriebene ältere Format nicht mehr verwendet; alle Fehlerprotokollzeilen folgen dann dem definierten Format.

Es folgt ein Beispiel für ein recht vollständiges error-log-format. Es gibt Quelladresse und -port, den Zeitpunkt von accept() für die Verbindung, den Frontend-Namen, die Anzahl aktiver Verbindungen im Prozess und im betreffenden Frontend, die interne Fehlerkennung von haproxy für die Frontend-Verbindung, die hexadezimale OpenSSL-Fehlernummer (die zur vollständigen Dekodierung an "openssl errstr" übergeben werden kann), den Status der Extraktion des Clientzertifikats (0 bedeutet kein Fehler), den Status der Prüfung des Clientzertifikats anhand der CA (0 bedeutet kein Fehler), einen booleschen Wert für eine neue oder wiederaufgenommene Verbindung, die optionale Server Name Indication (SNI) des Clients sowie gegebenenfalls den SSL-Versionsnamen und die auf der Verbindung verwendeten SSL-Cipher aus. Fehler bei Backend-Verbindungen werden hier niemals gemeldet: Damit eine Backend-Verbindung fehlschlagen kann, muss sie bereits einen erfolgreich angelegten Stream durchlaufen haben. Sie erscheint deshalb im regulären Verkehrsprotokoll (siehe option httplog oder option httpslog).

```haproxy
# detailed frontend connection error log
error-log-format "%ci:%cp [%tr] %ft %ac/%fc %[fc_err]/\
      %[ssl_fc_err,hex]/%[ssl_c_err]/%[ssl_c_ca_err]/%[ssl_fc_is_resumed] \
      %[ssl_fc_sni]/%sslv/%sslc"
```

### 8.2.6. Benutzerdefiniertes Protokollformat {#section-8-2-6}

Ursprünglich dienten benutzerdefinierte Protokollformate ausschließlich der Protokollierung. Weil sich damit aber bequem mehrere komplexe Ausdrücke zu einer Zeichenkette zusammensetzen lassen, wurden sie von vielen Direktiven übernommen, die zuvor nur eine Zeichenkette als Argument akzeptierten. Diese können nun auch eine solche Formatdefinition annehmen. Derartige Argumente heißen in diesem Dokument meist "`<fmt>`" und werden genau wie das hier beschriebene Argument der Direktive "log-format" definiert.

Reichen die Standardformate für die Protokollierung nicht aus, lassen sich neue Formate sehr genau festlegen. Ein Protokollformat von Grund auf zu erstellen ist nicht immer einfach. Deshalb wird dringend empfohlen, zunächst die vorhandenen Formate ("option tcplog", "option httplog", "option httpslog") anzusehen, das am besten passende auszuwählen, seine entsprechende "log-format"-Zeichenkette zu kopieren und anzupassen.

Eine benutzerdefinierte Protokollformatdefinition ist aus Sicht der Konfiguration ein einziges Argument. Sie darf deshalb keine Leerzeichen oder Tabulatoren enthalten, außer wenn diese mit einem Backslash ('&#92;') maskiert werden oder die gesamte Definition in Anführungszeichen steht. Letzteres wird empfohlen. Formatzeichenketten ohne Anführungszeichen werden nicht mehr empfohlen: Die Erfahrung zeigt, dass sie sehr fehleranfällig sind, weil bereits ein fehlender Backslash das Format unbemerkt abschneiden kann. Solche Konfigurationen sind weiterhin häufig anzutreffen, weil Protokollformate nach Version 1.5-dev9 breit übernommen wurden, 3 Jahre bevor Anführungszeichen verwendbar waren. Es wird jedoch empfohlen, sie jetzt in Zeichenketten mit Anführungszeichen umzuwandeln und die Backslashes zu entfernen.

Eine Protokollformatdefinition besteht aus beliebig vielen Formatelementen, getrennt durch Text und Leerzeichen. Ein Formatelement beginnt mit '%'. Um ein wörtliches '%' auszugeben, muss ihm ein weiteres '%' vorangestellt werden, sodass '%%' entsteht.

Formatelemente können Aliase oder Sample-Ausdrücke sein:

Steht ein Element in eckigen Klammern ('[' .. ']'), wird es als Regel mit einem Sample-Ausdruck verwendet (siehe [Abschnitt 7.3](/de/docs/haproxy/acls-and-samples/#section-7-3)). Damit lassen sich seltenere Angaben ergänzen, etwa der DN des SSL-Clientzertifikats oder der Schlüssel, mit dem ein Eintrag in einer Stick Table gespeichert würde. Dies wird auch häufig bei Aktionen außerhalb der Protokollierung verwendet, etwa zur Header-Bearbeitung oder für Variablen.

Hat das Element dagegen einen alphanumerischen Namen, ist es ein Alias. Die verfügbaren Aliase stehen in der folgenden Tabelle.

Elemente können Argumente in geschweiften Klammern ('{}') annehmen. Mehrere Argumente werden darin durch Kommas getrennt. Flags lassen sich mit einem vorangestellten '+' oder '-' hinzufügen oder entfernen. Die verfügbaren Flags werden weiter unten aufgeführt.

Der besondere Alias "%o" überträgt seine Flags auf alle anderen Formatelemente derselben Formatzeichenkette. Dies ist besonders bei Zeichenketten mit Anführungszeichen ("Q") und maskierten Zeichen ("E") praktisch.

Der besondere Alias "%OG" liefert den Ursprung einer Protokollmeldung, also wann und wo sie erzeugt wurde, in lesbarer Form. Das ist besonders bei "option logasap" nützlich: Einige Protokollvariablen oder Sample-Abrufe können unvollständige Werte liefern oder sich unterschiedlich verhalten, je nachdem, wann und wo der Formatausdruck ausgewertet wurde. Mögliche Werte sind:

- "sess_error": Die Meldung wurde bei der Behandlung eines Sitzungsfehlers erzeugt.
- "sess_killed": Die Meldung wurde beim Abbruch einer Sitzung erzeugt (beendete embryonale Sitzung).
- "txn_accept": Die Meldung wurde unmittelbar nach Annahme der Frontend-Verbindung erzeugt.
- "txn_request": Die Meldung wurde nach Empfang der Clientanfrage erzeugt.
- "txn_connect": Die Meldung wurde nach Aufbau der Backend-Verbindung erzeugt.
- "txn_response": Die Meldung wurde bei der Verarbeitung der Serverantwort erzeugt.
- "txn_close": Die Meldung wurde im letzten Transaktionsschritt vor dem Schließen erzeugt.
- "unspec": Unbekannt oder nicht angegeben. "%OG" ist nur bei der Protokollierung relevant.

Elemente können optional mit ('()') benannt werden. Der Name muss unmittelbar nach '%' vor den Argumenten stehen. Bei gesetztem Kodierungsflag wie "json" oder "cbor" wird er automatisch als Schlüsselname verwendet. Ohne Kodierungsflag, also standardmäßig, wird der Name ignoriert. Der Ausgabetyp eines Elements lässt sich durch ':type' hinter dem Namen erzwingen: %(itemname:itemtype)aliasname oder %(itemname:itemtype)[expr], wobei itemtype 'str', 'sint' oder 'bool' sein kann. Die Typangabe ist nur bei Verwendung einer Kodierungsmethode relevant. Auch ein leerer Name ist möglich, um den Ausgabetyp eines anonymen Elements zu erzwingen: %(:itemtype), etwa wenn die Kodierung nicht global gesetzt ist. Weitere Informationen stehen unten bei den Flag-Definitionen.

Da benutzerdefinierte Protokollformate ursprünglich nur für die Protokollierung gedacht waren, werden nicht druckbare und unsichere Zeichen (außerhalb der ASCII-Codes 32 bis 126 sowie einige weitere) je nach Einsatzort gesondert behandelt. [Abschnitt 8.6](/de/docs/haproxy/configuration-logging/#section-8-6) beschreibt das genaue Vorgehen für Protokolle. Es verhindert die Ausgabe unsicherer Codes, die die Lesbarkeit im Terminal beeinträchtigen. Bei Header-Feldern, Health Checks oder Antwortnutzdaten sind die Regeln weniger streng: Nur in HTTP-Header-Feldern verbotene Zeichen werden durch ihre hexadezimale Kodierung mit vorangestelltem '%' ersetzt. Normalerweise ist dies unproblematisch. Es kann aber die Ausgabe verändern, wenn ein Zeichen unverändert erwartet wird, etwa beim Erstellen einer Fehlerseite oder vollständiger Antwortnutzdaten, in denen Zeilenumbrüche als "%0A" erscheinen könnten.

Hinweis: Bei den Konfigurationsdirektiven "log-format", "log-format-sd" und "unique-id-format" gelten Leerzeichen als Trennzeichen und werden zusammengefasst.

Hinweis: Beim syslog-Nachrichtenformat RFC5424 sollten die Zeichen '"', '&#92;' und ']' innerhalb von PARAM-VALUE durch ein vorangestelltes '&#92;' maskiert werden (Einzelheiten unter <https://tools.ietf.org/html/rfc5424#section-6.3.3>). In solchen Fällen sollte das Flag "E" in Betracht gezogen werden.

Folgende Element-Flags werden unterstützt und lassen sich über die Argumente des Elements aktivieren oder deaktivieren:

- Q: Eine Zeichenkette in Anführungszeichen setzen.
- X: Hexadezimale Darstellung (IPs, Ports, %Ts, %rt, %pid).
- E: Die Zeichen '"', '&#92;' und ']' in einer Zeichenkette durch ein vorangestelltes
  '&#92;' maskieren (vorgesehen für Protokollformate mit strukturierten Daten nach RFC5424).
- bin: Versuchen, Binärdaten zu erhalten. Dies kann bei Sample-Ausdrücken mit binärer Ausgabe
  nützlich sein, um die Originaldaten zu bewahren. Dabei können jedoch nicht druckbare Zeichen
  einschließlich NULL-Bytes entstehen, die die meisten syslog-Endpunkte nicht erwarten.
  Das Flag ist daher hauptsächlich für set-var-fmt, Ringpuffer und binärfähige Protokollendpunkte
  vorgesehen. Es kann nur global mit %o gesetzt werden; als Option eines einzelnen Elements
  wird es ignoriert.
- json: Den Wert automatisch im JSON-Format kodieren. Bei globaler Aktivierung werden nur benannte Formatelemente berücksichtigt. Unvollständige Zahlenwerte, etwa '%B' bei logasap, die ohne Kodierung normalerweise ein vorangestelltes '+' erhalten, werden unverändert kodiert. Die Option '+E' wird außerdem ignoriert. Wie in [Abschnitt 8.6](/de/docs/haproxy/configuration-logging/#section-8-6) beschrieben, werden Zeichen außerhalb des Bereichs 32..126 Byte für Byte mit JSON-Escape-Sequenzen maskiert, sodass die Ausgabe unabhängig von der Eingabe aus druckbarem ASCII besteht. Dies gilt auch für gültige UTF-8-Sequenzen: Nach dem Dekodieren erscheint Nicht-ASCII-Text als seine einzelnen Bytes. Beispielsweise wird U+00E9, kodiert als 0xC3 0xA9, als "&#92;u00C3&#92;u00A9" protokolliert. Mit "utf8" unten lässt sich solcher Text erhalten.
- utf8: Zusammen mit "json" werden gültige UTF-8-Sequenzen aus mehreren Bytes unmaskiert ausgegeben. C1-Steuerzeichen (U+0080 bis U+009F) werden weiterhin maskiert und durch ihren Codepunkt dargestellt. Ungültige Sequenzen werden Byte für Byte maskiert, damit die Ausgabe immer gültiges UTF-8 bleibt. Da gültiges UTF-8 unverändert ausgegeben wird, kann ein Client mit bestimmten Sonderzeichen die Darstellung einer Protokollzeile im Terminal oder in einem Protokollbetrachter verändern, etwa mit Richtungswechseln, Zeichen ohne Breite oder Zeilen- und Absatztrennern. Deshalb sollte dieses Flag nur für Inhalte aus vertrauenswürdigen Quellen verwendet werden oder wenn die Protokolle nicht in einem Terminal angezeigt werden sollen. Ohne "json" hat es keine Wirkung.
- cbor: Den Wert automatisch im CBOR-Format kodieren. Bei globaler Aktivierung werden nur
  benannte Formatelemente berücksichtigt. Standardmäßig werden cbor-kodierte Daten in HEX-Form
  dargestellt, damit sie auf stdout druckbar bleiben und mit gewöhnlichen syslog-Endpunkten
  verwendet werden können. Wie bei json werden unvollständige Zahlenwerte unverändert kodiert
  und '+E' ignoriert. Zusammen mit '+bin' werden direkt rohe binäre CBOR-Nutzdaten erzeugt.
  Dabei entstehen nicht druckbare Zeichen; dies ist daher hauptsächlich für set-var-fmt,
  Ringpuffer und binärfähige Protokollendpunkte vorgesehen.

Beispiel:

```text
log-format %T\ %t\ Some\ Text
log-format %{+Q}o\ %t\ %s\ %{-Q}r

log-format-sd %{+Q,+E}o\ [exampleSDID@1234\ header=%[capture.req.hdr(0)]]

log-format "%{+json}o %(request)r %(custom_expr)[str(custom)]"
log-format "%{+json,+utf8}o %(request)r %(custom_expr)[str(custom)]"
log-format "%{+cbor}o %(request)r %(custom_expr)[str(custom)]"
```

Die derzeit definierten Aliase stehen in der folgenden Tabelle:

```text
  +---+------+------------------------------------------------------+--------------+
  | R |Alias | Feldname (Beschreibung unter 8.2.2 und 8.2.3)        | Typ          |
  |   |      | Alternative mit Sample-Abruf                         |              |
  +===+======+======================================================+==============+
  |   | %o   | Besonderer Alias: Flags auf alle folgenden Elemente  |              |
  +---+------+------------------------------------------------------+--------------+
  |                                 Datumsformate                                  |
  +---+------+------------------------------------------------------+--------------+
  |   | %T   | Annahmezeit UTC + Zeitzone                           |              |
  |   |      | %[accept_date,utime("%d/%b/%Y:%H:%M:%S %z")]         | Datum        |
  +---+------+------------------------------------------------------+--------------+
  |   | %Tl  | Annahmezeit lokal + Zeitzone                         |              |
  |   |      | %[accept_date,ltime("%d/%b/%Y:%H:%M:%S %z")]         | Datum        |
  +---+------+------------------------------------------------------+--------------+
  |   | %Ts  | Annahmezeit als UNIX-Zeitstempel                     | numerisch    |
  |   |      | %[accept_date]                                       |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %t   | Annahmezeit lokal (Millisekundenauflösung)           |              |
  |   |      | %[accept_date(ms),ms_ltime("%d/%b/%Y:%H:%M:%S.%3N")] | Datum        |
  +---+------+------------------------------------------------------+--------------+
  |   | %ms  | Millisekunden der Annahmezeit                        |              |
  |   |      | %[accept_date(ms),ms_utime("%3N")]                   | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %tr  | Anfragezeit lokal (Millisekundenauflösung)           |              |
  |   |      | %[request_date(ms),ms_ltime("%d/%b/%Y:%H:%M:%S.%3N")] | Datum        |
  +---+------+------------------------------------------------------+--------------+
  | H | %trg | Anfragezeit UTC + Zeitzone                           |              |
  |   |      | %[request_date,utime("%d/%b/%Y:%H:%M:%S %z")]        | Datum        |
  +---+------+------------------------------------------------------+--------------+
  | H | %trl | Anfragezeit lokal + Zeitzone                         |              |
  |   |      | %[request_date,ltime("%d/%b/%Y:%H:%M:%S %z")]        | Datum        |
  +---+------+------------------------------------------------------+--------------+
  |                                 Zeitmessungen                                  |
  +---+------+------------------------------------------------------+--------------+
  | H | %Ta  | Aktive Zeit der Anfrage (von TR bis zum Ende)        |              |
  |   |      | %[txn.timer.total]                                   | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Tc  | Tc                                                   |              |
  |   |      | %[bc.timer.connect]                                  | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Td  | Td = Tt - (Tq + Tw + Tc + Tr)                        |              |
  |   |      | %[res.timer.data]                                    | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Th  | Handshake-Dauer (SSL, PROXY-Protokoll)               |              |
  |   |      | %[fc.timer.handshake]                                | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %Ti  | Leerlaufzeit vor der HTTP-Anfrage                    |              |
  |   |      | %[req.timer.idle]                                    | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %Tq  | Th + Ti + TR                                         |              |
  |   |      | %[req.timer.tq]                                      | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %TR  | Dauer des vollen Anfrageempfangs ab dem 1. Byte      |              |
  |   |      | %[req.timer.hdr]                                     | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %Tr  | Tr (Antwortzeit)                                     |              |
  |   |      | %[res.timer.hdr]                                     | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Tt  | Tt                                                   |              |
  |   |      | %[fc.timer.total]                                    | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Tu  | Tu                                                   |              |
  |   |      | %[txn.timer.user]                                    | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %Tw  | Tw                                                   |              |
  |   |      | %[req.timer.queue]                                   | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |                                    Sonstige                                    |
  +---+------+------------------------------------------------------+--------------+
  |   | %B   | bytes_read (vom Server zum Client)                   | numerisch    |
  |   |      | %[res.bytes_in]                                      |              |
  +---+------+------------------------------------------------------+--------------+
  | H | %CC  | captured_request_cookie                              | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  | H | %CS  | captured_response_cookie                             | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %H   | hostname                                             | Zeichenkette |
  |   |      | %[hostname]                                          |              |
  +---+------+------------------------------------------------------+--------------+
  | H | %HM  | HTTP-Methode (z. B. POST)                            | Zeichenkette |
  |   |      | %[method]
  +---+------+------------------------------------------------------+--------------+
  | H | %HP  | HTTP-Anfrage-URI ohne Query-String                   | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  | H | %HPO | Nur HTTP-Pfad (ohne Host und Query-String)           | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  | H | %HQ  | Query-String der HTTP-Anfrage-URI (z. B. ?bar=baz)   | Zeichenkette |
  |   |      | ?%[query]                                            |              |
  +---+------+------------------------------------------------------+--------------+
  | H | %HU  | HTTP-Anfrage-URI (z. B. /foo?bar=baz)                | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  | H | %HV  | HTTP-Version (z. B. HTTP/1.0)                        | Zeichenkette |
  |   |      | HTTP/%[req.ver]                                      |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %ID  | unique-id                                            | Zeichenkette |
  |   |      | %[unique-id]                                         |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %ST  | status_code                                          | numerisch    |
  |   |      | %[txn.status]                                        |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %U   | bytes_uploaded (vom Client zum Server)               | numerisch    |
  |   |      | %[req.bytes_in]                                      |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %ac  | actconn                                              |              |
  |   |      | %[act_conn]                                          | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %b   | backend_name                                         |              |
  |   |      | %[be_name]                                           | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %bc  | beconn (gleichzeitige Backend-Verbindungen)          | numerisch    |
  |   |      | %[be_conn]                                           |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %bi  | backend_source_ip (verbindende Adresse)              |              |
  |   |      | %[bc_src]                                            | IP           |
  +---+------+------------------------------------------------------+--------------+
  |   | %bp  | backend_source_port (verbindende Adresse)            |              |
  |   |      | %[bc_src_port]                                       | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %bq  | backend_queue                                        | numerisch    |
  |   |      | %[bc_be_queue]                                       |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %ci  | client_ip (angenommene Adresse)                      |              |
  |   |      | %[src]                                               | IP           |
  +---+------+------------------------------------------------------+--------------+
  |   | %cp  | client_port (angenommene Adresse)                    |              |
  |   |      | %[src_port]                                          | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %f   | frontend_name                                        | Zeichenkette |
  |   |      | %[fe_name]                                           |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %fc  | feconn (gleichzeitige Frontend-Verbindungen)         | numerisch    |
  |   |      | %[fe_conn]                                           |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %fi  | frontend_ip (annehmende Adresse)                     |              |
  |   |      | %[dst]                                               | IP           |
  +---+------+------------------------------------------------------+--------------+
  |   | %fp  | frontend_port (annehmende Adresse)                   |              |
  |   |      | %[dst_port]                                          | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %ft  | frontend_name_transport (Suffix '~' für SSL)         | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %lc  | frontend_log_counter                                 | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %hr  | captured_request_headers im Standardstil             | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %hrl | captured_request_headers im CLF-Stil                 | Zeichenkette |
  |   |      |                                                      | Liste        |
  +---+------+------------------------------------------------------+--------------+
  |   | %hs  | captured_response_headers im Standardstil            | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %hsl | captured_response_headers im CLF-Stil                | Zeichenkette |
  |   |      |                                                      | Liste        |
  +---+------+------------------------------------------------------+--------------+
  | L | %OG  | Lesbarer Ursprung der Protokollmeldung               | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %pid | PID                                                  |              |
  |   |      | %[pid]                                               | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  | H | %r   | http_request                                         | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %rc  | retries                                              | numerisch    |
  |   |      | %[txn.redispatched,iif(+,)]%[txn.conn_retries]       |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %rt  | request_counter (HTTP-Anfrage oder TCP-Sitzung)      | numerisch    |
  |   |      | %[txn.id32]                                          |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %s   | server_name                                          | Zeichenkette |
  |   |      | %[srv_name]                                          |              |
  +---+------+------------------------------------------------------+--------------+
  |   | %sc  | srv_conn (gleichzeitige Serververbindungen)          | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %si  | server_IP (Zieladresse)                              |              |
  |   |      | %[bc_dst]                                            | IP           |
  +---+------+------------------------------------------------------+--------------+
  |   | %sp  | server_port (Zieladresse)                            |              |
  |   |      | %[bc_dst_port]                                       | numerisch    |
  +---+------+------------------------------------------------------+--------------+
  |   | %sq  | srv_queue                                            | numerisch    |
  |   |      | %[bc_srv_queue]                                      |              |
  +---+------+------------------------------------------------------+--------------+
  | S | %sslc| ssl_ciphers (z. B. AES-SHA)                          |              |
  |   |      | %[ssl_fc_cipher]                                     | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  | S | %sslv| ssl_version (z. B. TLSv1)                            |              |
  |   |      | %[ssl_fc_protocol]                                   | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
  |   | %ts  | termination_state                                    | Zeichenkette |
  |   |      | %[txn.sess_term_state]                               |              |
  +---+------+------------------------------------------------------+--------------+
  | H | %tsc | termination_state mit Cookie-Status                  | Zeichenkette |
  +---+------+------------------------------------------------------+--------------+
```

    R = Einschränkungen: H = nur mode http; S = nur SSL; L = nur Protokollierung

## 8.3. Erweiterte Protokollierungsoptionen {#section-8-3}

Einige erweiterte Protokollierungsoptionen werden häufig gesucht, sind aber beim bloßen Durchsehen der Optionen schwer zu finden. Dieser Abschnitt bietet einen Einstieg in einige Optionen für eine bessere Protokollierung. Einzelheiten zur Verwendung stehen in der Schlüsselwortreferenz.

### 8.3.1. Protokollierung externer Tests deaktivieren {#section-8-3-1}

Überwachungswerkzeuge führen häufig Health Checks an HAProxy aus. Dies kann ein Load-Balancer auf Schicht 3 wie LVS oder ein kommerzieller Load-Balancer sein, aber auch ein umfassenderes Überwachungssystem wie Nagios. Bei sehr häufigen Tests stellt sich oft die Frage, wie sich deren Protokollierung deaktivieren lässt. Dafür gibt es drei Möglichkeiten:

- Kommen die Verbindungen aus beliebigen Quellen und sind sie reine TCP-Prüfanfragen,
  soll oft einfach die Protokollierung von Verbindungen ohne Datenaustausch deaktiviert werden.
  Dazu dient "option dontlognull" im Frontend. Dies unterdrückt auch die Protokollierung von
  Portscans, was erwünscht sein kann oder auch nicht.

- Die Aktion "http-request set-log-level silent" kann mit unterschiedlichen Bedingungen
  verwendet werden, etwa Quellnetzen, Pfaden oder User-Agents.

- Wird eine bekannte URI für die Tests verwendet, diese mit "monitor-uri" für die Überwachung
  reservieren. Jeder Host, der diese Anfrage sendet, erhält dann nur das Ergebnis eines
  Health Checks; die Anfrage wird nicht protokolliert.

### 8.3.2. Vor dem Ende des Streams protokollieren {#section-8-3-2}

Bei einer Protokollierung erst am Verbindungsende bleibt der Ablauf während sehr langer Streams, etwa entfernter Terminalsitzungen oder großer Downloads, unsichtbar. "option logasap" im Frontend umgeht dieses Problem: HAProxy protokolliert dann möglichst früh, unmittelbar vor Beginn der Datenübertragung. Bei TCP wird weiterhin der Verbindungsstatus zum Server erfasst; bei HTTP erfolgt die Ausgabe direkt nach Verarbeitung der Server-Header. Die angegebene Bytezahl ist dann die Anzahl der an den Client gesendeten Header-Bytes. Zur Unterscheidung von gewöhnlichen Protokollen erhalten Gesamtzeit und Bytezahl ein vorangestelltes '+', das auf sicher größere tatsächliche Werte hinweist.

### 8.3.3. Protokollstufe bei Fehlern erhöhen {#section-8-3-3}

Manchmal ist es praktischer, Protokolle des normalen Datenverkehrs von Fehlerprotokollen zu trennen, etwa um Fehler in Protokolldateien leichter zu überwachen. Mit "log-separate-errors" steigt die syslog-Stufe für Verbindungen mit Fehlern, Zeitüberschreitungen, Wiederholungsversuchen, Umverteilungen oder HTTP-Statuscodes 5xx von "info" auf "err". Dadurch kann ein syslog-Daemon die Meldungen in einer eigenen Datei ablegen. Die Fehler sollten unbedingt auch in der Datei für den normalen Datenverkehr verbleiben, damit die Reihenfolge der Meldungen erhalten bleibt. Vorsicht ist auch geboten, wenn der syslog-Daemon bereits alle Meldungen oberhalb von "notice" in einer "admin"-Datei speichert, da "err" höher als "notice" liegt.

### 8.3.4. Protokollierung erfolgreicher Verbindungen deaktivieren {#section-8-3-4}

Es mag zunächst ungewöhnlich klingen, doch manche großen Websites müssen mehrere Tausend Meldungen pro Sekunde verarbeiten. Es fällt ihnen schwer, diese lange vollständig aufzubewahren oder Fehler darin zu erkennen. Ist im Frontend "dontlog-normal" gesetzt, werden normale Verbindungen nicht protokolliert. Als normal gilt dabei eine Verbindung ohne Fehler, Zeitüberschreitung, Wiederholungsversuch oder Umverteilung. Bei HTTP wird zusätzlich der Statuscode geprüft; Antworten mit Status 5xx gelten ebenfalls nicht als normal und werden protokolliert. Von dieser Einstellung wird jedoch ausdrücklich abgeraten, weil dadurch die meisten nützlichen Informationen aus den Protokollen verschwinden. Nur verwenden, wenn keine Alternative besteht.

### 8.3.5. Protokollprofile {#section-8-3-5}

Direktiven wie "log-format", "log-format-sd", "error-log-format" oder "log-tag" konfigurieren die Protokollformatierung global oder auf Proxy-Ebene. Es kann jedoch sinnvoll sein, diese Einstellungen möglichst nahe am Protokollziel festzulegen, also je "log"-Direktive.

Dazu dient der Abschnitt "log-profile", der an beliebiger Stelle der Konfiguration definiert werden kann. Seine Schlüsselwörter beschreiben, wie die für eine bestimmte `log`-Direktive ausgegebenen Meldungen aufgebaut werden sollen.

Eine "log"-Direktive kann ein bestimmtes log-profile anhand seines Namens auswählen. Mehrere "log"-Direktiven können dasselbe Profil verwenden.

log-profile `<name>` Erstellt ein neues Protokollprofil mit der Kennung `<name>`.

log-tag `<string>` Überschreibt das syslog-Tag, das mit "log-tag" global oder je Proxy gesetzt wurde.

on `<step>` [drop] [format `<fmt>`] [sd `<sd_fmt>`] Überschreibt die Formatzeichenkette, mit der die Protokollzeile normalerweise beim Schritt `<step>` erzeugt wird. `<fmt>` überschreibt je nach `<step>` die Zeichenkette "log-format" oder "error-log-format", während `<sd_fmt>` die Zeichenkette "log-format-sd" überschreibt. Beides kann kombiniert werden.

Mit dem besonderen Schlüsselwort "drop" wird für den angegebenen `<step>` keine Meldung ausgegeben. Es hat Vorrang vor zuvor definierten Angaben für "format" und "sd".

Mögliche Werte für `<step>` sind:

- "accept": log-format überschreiben, wenn die Meldung unmittelbar nach Annahme der Frontend-Verbindung entsteht.
- "request": log-format überschreiben, wenn die Meldung nach Empfang der Clientanfrage entsteht.
- "connect": log-format überschreiben, wenn die Meldung nach Aufbau der Backend-Verbindung entsteht.
- "response": log-format überschreiben, wenn die Meldung während der Verarbeitung der Serverantwort entsteht.
- "close": log-format überschreiben, wenn die Meldung im letzten Transaktionsschritt (txn) entsteht.
- "error": error-log-format überschreiben, wenn die Meldung aufgrund eines Transaktionsfehlers entsteht.
- "any": log-format und error-log-format für alle Protokollierungsschritte überschreiben, sofern
  keine genauere Festlegung für einen einzelnen Schritt vorliegt.

Weitere relevante Werte für `<step>` stehen bei der Aktion "do-log".

Diese Einstellung ist nur für "log"-Direktiven in Kontexten relevant, in denen "log-format" sinnvoll ist, etwa bei http- und tcp-Proxys. Andernfalls wird sie ignoriert.

Beispiel:

```text
log-profile myprof

  log-tag "custom-tag"

  on error format "%ci: error"
  on connect drop
  on any sd "custom-sd"

listen myproxy
  mode http
  option httplog
  log-tag "normal"

  log stdout format rfc5424 local0
  # success:
  # <134>1 2024-06-12T10:09:11.823400+02:00 - normal 224482 - - 127.0.0.1:53594 [12/Jun/2024:10:09:11.814] myproxy myproxy/<NOSRV> 0/-1/-1/-1/0 200 49 - - LR-- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
  #
  # error:
  # <134>1 2024-06-12T10:09:44.810929+02:00 - normal 224482 - - 127.0.0.1:59258 [12/Jun/2024:10:09:44.426] myproxy myproxy/<NOSRV> -1/-1/-1/-1/384 400 0 - - CR-- 1/1/0/0/0 0/0 "<BADREQ>"

  log 127.0.0.1:514 format rfc5424 profile myprof local0
  # success:
  # <134>1 2024-06-12T10:09:11.823428+02:00 - custom-tag 224482 - custom-sd 127.0.0.1:53594 [12/Jun/2024:10:09:11.814] myproxy myproxy/<NOSRV> 0/-1/-1/-1/0 200 49 - - LR-- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
  #
  # error:
  # <134>1 2024-06-12T10:09:51.566524+02:00 - custom-tag 224482 - - 127.0.0.1: error
```

## 8.4. Zeitmessungen {#section-8-4}

Zeitmessungen helfen sehr bei der Untersuchung von Netzwerkproblemen. Alle Werte werden in Millisekunden (ms) angegeben und sollten zusammen mit den Flags zur Stream-Beendigung ausgewertet werden. Im TCP-Modus mit "option tcplog" im Frontend werden 3 Messpunkte als "Tw/Tc/Tt" ausgegeben, im HTTP-Modus 5 als "TR/Tw/Tc/Tr/Ta". Hinzu kommen drei weitere Messwerte: "Th", "Ti" und "Tq".

Zeitmessungen im HTTP-Modus:

```text
                 erste Anfrage               2. Anfrage
      |<-------------------------------->|<-------------- ...
      t         tr                       t    tr ...
   ---|----|----|----|----|----|----|----|----|--
     : Th   Ti   TR   Tw   Tc   Tr   Td: Ti   ...
     :<---- Tq ---->:                  :
     :<-------------- Tt -------------->:
     :<--        -----Tu--------------->:
               :<--------- Ta --------->:
```

Zeitmessungen im TCP-Modus:

```text
           TCP-Sitzung
      |<----------------->|
      t                   t
   ---|----|----|----|----|---
      | Th   Tw   Tc   Td |
      |<------ Tt ------->|
```

- Th: Gesamtdauer für die Annahme der TCP-Verbindung und die Handshakes der Protokolle
  niedrigerer Schichten, derzeit proxy-protocol und SSL. Dies kann während der gesamten
  Verbindungsdauer nur einmal geschehen. Ein hoher Wert kann bedeuten, dass der Client nur
  vorab eine Verbindung aufgebaut, aber noch nichts gesendet hat, dass Netzwerkprobleme wie
  MTU-Probleme den rechtzeitigen Abschluss des Handshakes verhindern oder dass die Berechnung
  des SSL-Handshakes sehr aufwendig war. Diese Zeit wird nur vor der ersten Anfrage angegeben.
  Sie kann daher über alle Anfragen gemittelt werden, um den anteiligen Aufwand zu ermitteln.
  Bei der zweiten und allen folgenden Anfragen wird hier stets null ausgegeben.

  Dieser Messwert heißt als log-format-Alias %Th und als Sample-Abruf fc.timer.handshake.

- Ti: Leerlaufzeit vor der HTTP-Anfrage, nur im HTTP-Modus. Gemessen wird zwischen dem
  Ende der Handshakes und dem ersten Byte der HTTP-Anfrage. Bei einer zweiten Anfrage im
  Keep-Alive-Modus beginnt die Messung nach dem Ende der Übertragung der vorherigen Antwort.
  Bei einem Multiplex-Protokoll wie HTTP/2 beginnt sie unmittelbar nach der vorherigen Anfrage.
  Manche Browser bauen Verbindungen vorab auf, um die Latenz einer späteren Anfrage zu
  verringern, und halten sie bis zur Verwendung offen. Diese Verzögerung erscheint als
  Leerlaufzeit. Ein Wert von -1 bedeutet, dass auf der Verbindung nichts empfangen wurde.

  Dieser Messwert heißt als log-format-Alias %Ti und als Sample-Abruf req.timer.idle.

- TR: Gesamtdauer für den Empfang der Clientanfrage, nur im HTTP-Modus. Dies ist die
  Zeit vom Empfang der ersten Bytes bis zur Leerzeile, die das Ende der HTTP-Header markiert.
  "-1" bedeutet, dass das Header-Ende nie empfangen wurde. Dies geschieht bei vorzeitigem
  Schließen durch den Client oder einer Zeitüberschreitung. Die Dauer ist gewöhnlich sehr kurz,
  da die meisten Anfragen in ein einziges Paket passen. Ein hoher Wert kann auf eine bei
  einem Test von Hand eingegebene Anfrage hinweisen.

  Dieser Messwert heißt als log-format-Alias %TR und als Sample-Abruf req.timer.hdr.

- Tq: Gesamtdauer für den Empfang der Clientanfrage ab Verbindungsannahme oder ab dem
  Senden des letzten Bytes der vorherigen Antwort, nur im HTTP-Modus. Sie entspricht genau
  Th + Ti + TR, außer wenn einer dieser Werte -1 ist; dann ist auch Tq gleich -1. Vor HTTP
  Keep-Alive und dem vorzeitigen Verbindungsaufbau durch Browser war dieser Wert sehr nützlich.
  Heute wird empfohlen, stattdessen TR zu verwenden, da die Leerlaufzeit die Berichte stark
  mit Schwankungen belastet.

  Dieser Messwert heißt als log-format-Alias %Tq und als Sample-Abruf req.timer.tq.

- Tw: Gesamte Wartezeit in den Warteschlangen auf einen freien Verbindungsplatz. Sie
  berücksichtigt die Backend- und Serverwarteschlangen und hängt von deren Größe sowie davon
  ab, wie lange der Server für vorherige Anfragen benötigt. "-1" bedeutet, dass die Anfrage
  vor Erreichen der Warteschlange beendet wurde, was meist bei ungültigen oder abgewiesenen
  Anfragen geschieht.

  Dieser Messwert heißt als log-format-Alias %Tw und als Sample-Abruf req.timer.queue.

- Tc: Gesamtdauer für den Aufbau der TCP-Verbindung zum Server. Dies ist die Zeit zwischen
  dem Senden der Verbindungsanfrage durch den Proxy und ihrer Bestätigung durch den Server,
  also zwischen TCP-SYN-Paket und zugehörigem SYN/ACK-Antwortpaket. "-1" bedeutet, dass keine
  Verbindung zustande kam.

  Dieser Messwert heißt als log-format-Alias %Tc und als Sample-Abruf bc.timer.connect.

- Tr: Antwortzeit des Servers, nur im HTTP-Modus. Dies ist die Zeit zwischen dem Aufbau
  der TCP-Verbindung zum Server und dem Senden seiner vollständigen Antwort-Header. Sie gibt
  ausschließlich die Bearbeitungszeit der Anfrage ohne den Netzwerkaufwand für die
  Datenübertragung an. Muss der Client Daten an den Server senden, etwa bei einer POST-Anfrage,
  läuft die Messung jedoch bereits, was die scheinbare Antwortzeit verfälschen kann. Bei
  POST-Anfragen von Clients hinter einem nicht vertrauenswürdigen Netzwerk sollte diesem Feld
  daher gewöhnlich nur eingeschränkt vertraut werden. "-1" bedeutet, dass der letzte
  Antwort-Header, die Leerzeile, nie empfangen wurde. Meist ist dann die Serverzeitgrenze vor
  Verarbeitung der Anfrage abgelaufen oder der Server hat eine ungültige Antwort geliefert.

  Dieser Messwert heißt als log-format-Alias %Tr und als Sample-Abruf res.timer.hdr.

- Td: Gesamtdauer der Übertragung der Antwortnutzdaten bis zum letzten an den Client
  gesendeten Byte. Bei HTTP beginnt sie nach dem letzten Antwort-Header, also nach Tr.

  Es ist nicht garantiert, dass die gesendeten Daten beim Client ankommen; sie können
  im Kernel oder im Netzwerk festhängen.

  Dieser Messwert heißt als log-format-Alias %Td und als Sample-Abruf res.timer.data.

- Ta: Gesamte aktive Zeit der HTTP-Anfrage vom Empfang des ersten Bytes ihres Headers
  durch den Proxy bis zum Senden des letzten Bytes des Antwortkörpers. Eine Ausnahme besteht
  bei der Option "logasap": Dann entspricht sie nur (TR+Tw+Tc+Tr) und erhält ein vorangestelltes '+'.
  Daraus lässt sich die Datenübertragungszeit "Td" durch Abziehen der übrigen gültigen
  Messwerte berechnen:

```text
Td = Ta - (TR + Tw + Tc + Tr)
```

    Messwerte mit dem Wert "-1" müssen aus dieser Gleichung ausgeschlossen werden.
    "Ta" kann niemals negativ sein.

    Dieser Messwert heißt als log-format-Alias %Ta und als Sample-Abruf txn.timer.total.

- Tt: Gesamtdauer des Streams von der Annahme durch den Proxy bis zum Schließen beider
  Seiten. Eine Ausnahme besteht bei der Option "logasap": Dann entspricht sie nur
  (Th+Ti+TR+Tw+Tc+Tr) und erhält ein vorangestelltes '+'. Daraus lässt sich die
  Datenübertragungszeit "Td" durch Abziehen der übrigen gültigen Messwerte berechnen:

```text
Td = Tt - (Th + Ti + TR + Tw + Tc + Tr)
```

    Messwerte mit dem Wert "-1" müssen aus dieser Gleichung ausgeschlossen werden.
    Im TCP-Modus müssen außerdem "Ti", "Tq" und "Tr" ausgeschlossen werden.
    "Tt" kann niemals negativ sein; bei HTTP entspricht Tt einfach (Th+Ti+Ta).

    Dieser Messwert heißt als log-format-Alias %Tt und als Sample-Abruf fc.timer.total.

- Tu: Geschätzte Gesamtdauer aus Sicht des Clients von der Annahme durch den Proxy bis
  zum Schließen beider Seiten, ohne Leerlaufzeit. Damit lässt sich die vom Nutzer wahrgenommene
  Gesamtdauer grob messen, ohne den Einfluss der Keep-Alive-Leerlaufzeit zwischen Anfragen.
  Es ist nur eine Schätzung, da sie gleiche Netzwerklatenzen in beiden Richtungen voraussetzt.
  Eine Ausnahme besteht bei der Option "logasap": Dann entspricht sie nur
  (Th+TR+Tw+Tc+Tr) und erhält ein vorangestelltes '+'.

  Dieser Messwert heißt als log-format-Alias %Tu und als Sample-Abruf txn.timer.user.

Diese Zeitmessungen liefern wertvolle Hinweise auf Fehlerursachen. Da TCP Wiederholungsintervalle von 3, 6, 12... Sekunden vorgibt, hängen Werte nahe Vielfachen von 3s fast immer mit Paketverlusten durch Netzwerkprobleme zusammen, etwa Kabel, Aushandlung oder Überlastung. Liegt "Ta" oder "Tt" nahe einer konfigurierten Zeitgrenze, wurde ein Stream häufig wegen einer Zeitüberschreitung abgebrochen.

Die häufigsten Fälle:

- Liegt "Th" oder "Ti" nahe bei 3000, ging wahrscheinlich ein Paket zwischen Client und
  Proxy verloren. In lokalen Netzen ist dies sehr selten, kann aber bei weit entfernten Clients
  mit großen Anfragen auftreten. Höhere Werte können auch ohne Netzwerkproblem entstehen.
  Während eines Angriffs oder unmittelbar nach dem Ende eines Ressourcenengpasses nimmt
  HAProxy manchmal Tausende Verbindungen innerhalb weniger Millisekunden an. Die dafür benötigte
  Zeit verzögert zwangsläufig die Verarbeitung anderer Verbindungen etwas. Werden einige
  Tausend Verbindungen gleichzeitig angenommen, können daher Anfragezeiten von einigen zehn
  Millisekunden entstehen. In einem Keep-Alive-Modus können längere Leerlaufzeiten erscheinen,
  da "Ti" die Wartezeit auf weitere Anfragen misst.

- Liegt "Tc" nahe bei 3000, ging beim Verbindungsaufbau wahrscheinlich ein Paket zwischen
  Server und Proxy verloren. Dieser Wert sollte stets sehr niedrig sein, etwa 1 ms in lokalen
  Netzen und weniger als einige zehn ms in entfernten Netzen.

- Liegt "Tr" fast immer unter 3000, mit wenigen Ausnahmen, die ungefähr dem Durchschnitt
  zuzüglich 3000 entsprechen, gehen wahrscheinlich Pakete zwischen Proxy und Server verloren.

- Ist "Ta" selbst bei kleinen Bytezahlen groß, schließen häufig weder Client noch Server
  die Verbindung, während HAProxy im Tunnelmodus arbeitet und beide einen Keep-Alive-Modus
  vereinbart haben. Zur Behebung muss eine HTTP-Option verwendet werden, die Keep-Alive oder
  das Schließen im Frontend oder Backend beeinflusst. Bei Verbindungsregelung mit "maxconn"
  auf den Servern sind möglichst kleine Werte für 'Ta' oder 'Tt' wichtig: Erst wenn eine
  Verbindung freigegeben wird, erhält der Server eine neue.

Weitere auffällige Fälle im HTTP-Protokoll ('xx' steht für einen beliebigen, zu ignorierenden Wert):

```text
TR/Tw/Tc/Tr/+Ta  Im Frontend ist "option logasap" gesetzt; die Meldung wurde
                 vor der Datenphase ausgegeben. Alle Zeitmessungen sind gültig,
                 außer "Ta", das kürzer als die tatsächliche Dauer ist.

-1/xx/xx/xx/Ta   Der Client konnte nicht rechtzeitig eine vollständige Anfrage
                 senden oder brach zu früh ab. Zuerst die Flags zur
                 Stream-Beendigung, dann "timeout http-request" und
                 "timeout client" prüfen.

TR/-1/xx/xx/Ta   Die Anfrage konnte nicht verarbeitet werden, etwa weil Server
                 ausgefallen waren oder die Anfrage ungültig oder durch ACL-
                 Regeln verboten war. Die Flags zur Stream-Beendigung prüfen.

TR/Tw/-1/xx/Ta   Die Verbindung zum Server konnte nicht aufgebaut werden.
                 Entweder wies er sie aktiv zurück, oder die Zeitgrenze lief
                 nach Ta-(TR+Tw) ms ab. Zuerst die Flags zur Stream-Beendigung,
                 dann "timeout connect" prüfen. Die Aktion tarpit kann ähnliche
                 Muster erzeugen; "Tw" entspricht dann der Dauer, für die die
                 Clientverbindung offen gehalten wurde.

TR/Tw/Tc/-1/Ta   Der Server nahm die Verbindung an, lieferte aber nicht
                 rechtzeitig eine vollständige Antwort oder schloss die
                 Verbindung unerwartet nach Ta-(TR+Tw+Tc) ms. Zuerst die Flags
                 zur Stream-Beendigung, dann "timeout server" prüfen.
```

## 8.5. Stream-Zustand bei der Trennung {#section-8-5}

TCP- und HTTP-Protokolle enthalten unmittelbar vor der Anzahl aktiver Verbindungen im Feld "termination_state" ein Kennzeichen zur Stream-Beendigung. Im TCP-Modus ist es 2 Zeichen lang, im HTTP-Modus 4. Jedes Zeichen hat eine eigene Bedeutung:

- Das erste Zeichen bezeichnet das erste Ereignis, das zur Beendigung des Streams führte:

```text
C: Der Client hat die TCP-Sitzung unerwartet abgebrochen.

S: Der Server hat die TCP-Sitzung unerwartet abgebrochen oder sie
    ausdrücklich zurückgewiesen.

P: Der Proxy hat den Stream oder die Sitzung vorzeitig abgebrochen:
    wegen einer Verbindungsgrenze, eines passenden DENY-Filters oder
    einer Sicherheitsprüfung, die einen gefährlichen Fehler in der
    Serverantwort erkannt und blockiert hat, der Informationen hätte
    preisgeben können, etwa ein zwischenspeicherbares Cookie.

L: HAProxy hat den Stream lokal verarbeitet.

R: Eine Ressource des Proxys ist erschöpft, etwa Speicher, Sockets oder
    Quellports. Dies tritt gewöhnlich beim Verbindungsaufbau auf; die
    Systemprotokolle sollten den genauen Fehler enthalten. Dies muss
    als sehr schwerwiegende Auffälligkeit betrachtet werden, die so
    schnell wie möglich mit allen Mitteln behoben werden sollte.

I: Der Proxy hat bei einer Selbstprüfung einen internen Fehler erkannt.
    Dies sollte NIEMALS geschehen. Bitte melden Sie Protokolle mit diesem
    Kennzeichen, da es sich fast sicher um einen Programmfehler handelt.
    Ein vorsorglicher Neustart des Prozesses nach einem solchen Ereignis
    ist ebenfalls ratsam, falls Speicherbeschädigung die Ursache war.

D: HAProxy hat den Stream beendet, weil der Server als ausgefallen
    erkannt wurde und so konfiguriert war, dass bei einem Ausfall
    alle Verbindungen beendet werden.

U: HAProxy hat den Stream auf diesem Backup-Server beendet, weil ein
    aktiver Server als verfügbar erkannt wurde und so konfiguriert war,
    dass dann alle Backup-Verbindungen beendet werden.

K: Ein Administrator hat den Stream über HAProxy aktiv beendet.

c: Die clientseitige Zeitgrenze lief ab, während darauf gewartet wurde,
    dass der Client Daten sendet oder empfängt.

s: Die serverseitige Zeitgrenze lief ab, während darauf gewartet wurde,
    dass der Server Daten sendet oder empfängt.

-: Normaler Stream-Abschluss: Client und Server haben geschlossen;
    in den Puffern lagen keine Daten mehr.
```

- Das zweite Zeichen bezeichnet den Zustand des TCP- oder HTTP-Streams beim Schließen:

```text
R: Der Proxy wartete auf eine vollständige, gültige ANFRAGE des Clients,
    nur im HTTP-Modus. An keinen Server wurde etwas gesendet.

Q: Der Proxy wartete in der WARTESCHLANGE auf einen Verbindungsplatz.
    Dies kann nur bei Servern mit gesetztem 'maxconn' auftreten. Es kann
    auch in der globalen Warteschlange nach einer Umverteilung auftreten,
    wenn zuvor ein Verbindungsversuch zu einem ausfallenden Server
    fehlgeschlagen ist. Ist keine Umverteilung gemeldet, wurde kein
    Verbindungsversuch zu irgendeinem Server unternommen.

C: Der Proxy wartete auf den Aufbau der VERBINDUNG zum Server.
    Der Server hat höchstens einen Verbindungsversuch bemerkt.

H: Der Proxy wartete auf vollständige, gültige Antwort-HEADER des
    Servers, nur bei HTTP.

D: Der Stream befand sich in der DATENPHASE.

L: Der Proxy übertrug noch LETZTE Daten an den Client, während der
    Server bereits fertig war. Dies ist sehr selten und kann nur
    auftreten, wenn der Client beim Empfang der letzten Pakete ausfällt.

T: Die Anfrage wurde mit tarpit verzögert. Die Clientverbindung blieb
    für die gesamte Dauer von "timeout tarpit" oder bis zum Schließen
    durch den Client offen. Beide Fälle erscheinen im Messwert "Tw".

-: Normaler Stream-Abschluss nach Ende der Datenübertragung.
```

- Das dritte Zeichen gibt an, ob der Client das Persistenz-Cookie mitgesendet hat,
  nur im HTTP-Modus:

```text
N: Der Client hat KEIN Cookie mitgesendet. Dies trifft gewöhnlich auf
    neue Besucher zu. Die Anzahl dieses Kennzeichens in den Protokollen
    zeigt daher meist zuverlässig die Entwicklung der Besucherzahlen.

I: Der Client hat ein UNGÜLTIGES Cookie mitgesendet, das keinem bekannten
    Server entspricht. Mögliche Ursachen sind eine kürzliche
    Konfigurationsänderung, vermischte Cookies von HTTP/HTTPS-Websites,
    bedingtes Ignorieren der Persistenz oder ein Angriff.

D: Das Client-Cookie bezeichnet einen AUSGEFALLENEN Server. Entweder
    war "option persist" gesetzt und der Client wurde an diesen Server
    geleitet, oder sie war nicht gesetzt und der Client wurde an einen
    anderen Server umverteilt.

V: Der Client hat ein GÜLTIGES Cookie mitgesendet und wurde an den
    zugehörigen Server geleitet.

E: Der Client hat ein gültiges Cookie mitgesendet, dessen letzter
    Zeitpunkt jedoch älter ist, als "maxidle" erlaubt. Das Cookie gilt
    deshalb als ABGELAUFEN und wird ignoriert. Die Anfrage wird so
    umverteilt, als wäre kein Cookie vorhanden.

O: Der Client hat ein gültiges Cookie mitgesendet, dessen erster
    Zeitpunkt jedoch älter ist, als "maxlife" erlaubt. Das Cookie gilt
    deshalb als zu ALT und wird ignoriert. Die Anfrage wird so
    umverteilt, als wäre kein Cookie vorhanden.

U: Ein Cookie war vorhanden, wurde aber nicht zur Serverauswahl
    verwendet, weil ein anderes Verfahren zum Einsatz kam,
    gewöhnlich eine "use-server"-Regel.

-: Nicht anwendbar; in der Konfiguration ist kein Cookie gesetzt.
```

- Das letzte Zeichen beschreibt die Aktionen am vom Server zurückgegebenen Persistenz-Cookie,
  nur im HTTP-Modus:

```text
N: Der Server hat KEIN Cookie geliefert; es wurde auch keines eingefügt.

I: Der Server hat kein Cookie geliefert; der Proxy hat eines EINGEFÜGT.
    Im Modus "cookie insert" wird ein vom Server geliefertes Cookie
    dennoch überschrieben und hier als "I" gemeldet.

U: Der Proxy hat den letzten Zeitpunkt im vom Client mitgesendeten
    Cookie AKTUALISIERT. Dies ist nur im Insert-Modus mit "maxidle"
    möglich und geschieht bei jeder Aktivität zu einem anderen als dem
    im Cookie angegebenen Zeitpunkt. Bei jeder anderen Änderung, etwa
    einer Umverteilung, wird das Cookie stattdessen als eingefügt markiert.

P: Der Server hat ein Cookie GELIEFERT; es wurde unverändert übertragen.

R: Der Proxy hat das vom Server gelieferte Cookie UMGESCHRIEBEN,
    was in den Modi "cookie rewrite" oder "cookie prefix" geschieht.

D: Der Proxy hat das vom Server gelieferte Cookie GELÖSCHT.

-: Nicht anwendbar; in der Konfiguration ist kein Cookie gesetzt.
```

Die Kombination der ersten beiden Flags zeigt ausführlich, was beim Ende des Streams oder der Sitzung geschah und warum er beziehungsweise sie beendet wurde. Sie hilft etwa, überlastete Server, Netzwerkprobleme, lokale Ressourcenengpässe und Angriffe zu erkennen.

Die häufigsten Kombinationen von Beendigungsflags stehen unten in alphabetischer Reihenfolge. Zur leichteren Orientierung folgt die Variante mit Kleinbuchstaben jeweils direkt auf die mit Großbuchstaben.

Flags Grund

     --   Normale Beendigung.

     CC   Der Client brach ab, bevor die Verbindung zum Server aufgebaut war.
          Dies kann geschehen, wenn HAProxy einen kürzlich ausgefallenen oder
          ungeprüften Server zu erreichen versucht und der Client abbricht,
          während HAProxy auf dessen Antwort oder auf "timeout connect" wartet.

     CD   Der Client brach während der Datenübertragung unerwartet ab. Mögliche
          Ursachen sind ein Browserabsturz, ein zwischengeschaltetes Gerät,
          das die Verbindung zwischen Client und HAProxy aktiv trennt,
          Routingprobleme auf diesem Weg oder ein Keep-Alive-Stream zwischen
          Server und Client, den zuerst der Client beendet.

     cD   Der Client hat während der gesamten Dauer von "timeout client"
          weder Daten gesendet noch bestätigt. Häufig sind Netzwerkfehler
          auf der Clientseite oder ein unsauberes Verlassen des Netzwerks
          durch den Client die Ursache.

     CH   Der Client brach ab, während er auf den Beginn der Serverantwort
          wartete. Möglicherweise antwortete der Server zu langsam, oder
          der Client klickte zu früh auf 'Stop'.

     cH   "timeout client" lief beim Warten auf Clientdaten während einer
          POST-Anfrage ab. Eine Ursache können zu große TCP-MSS-Werte für
          PPPoE-Netze sein, die keine Pakete voller Größe übertragen können.
          Dies kann auch auftreten, wenn die Clientzeitgrenze kleiner als
          die Serverzeitgrenze ist und der Server zu lange zum Antworten braucht.

     CQ   Der Client brach ab, während sein Stream auf einen Server mit
          genügend freien Verbindungsplätzen wartete. Möglicherweise waren
          alle Server ausgelastet oder der zugewiesene Server antwortete zu langsam.

     CR   Der Client brach ab, bevor er eine vollständige HTTP-Anfrage gesendet
          hatte. Wahrscheinlich wurde die Anfrage von Hand mit einem telnet-Client
          eingegeben und zu früh abgebrochen. Der HTTP-Statuscode ist hier
          vermutlich 400. Gelegentlich kann auch ein IDS die Verbindung zwischen
          HAProxy und Client beenden. Mit "option http-ignore-probes" lassen
          sich Verbindungen ohne Datenaustausch ignorieren.

     cR   "timeout http-request" lief ab, bevor der Client eine vollständige
          HTTP-Anfrage gesendet hatte. Mögliche Ursachen sind zu große TCP-MSS-
          Werte auf der Clientseite für PPPoE-Netze, die keine Pakete voller
          Größe übertragen können, zu langsam von Hand eingegebene Anfragen
          oder eine vergessene Leerzeile am Anfrageende. Der HTTP-Statuscode
          ist hier vermutlich 408. Hinweis: Einige Browser haben seit Kurzem
          eine "pre-connect"-Funktion. Sie verbinden sich vorsorglich mit kürzlich
          besuchten Websites, falls der Nutzer sie erneut aufrufen möchte.
          Dadurch entstehen viele Verbindungen, die bei zuerst ablaufender
          Zeitgrenze mit 408 Request Timeout oder bei vorherigem Schließen
          durch den Browser mit 400 Bad Request enden. Sie füllen die Protokolle
          und erhöhen Fehlerzähler. Manche Versionen einiger Browser sollen
          sogar den Fehlercode anzeigen. Mit "option http-ignore-probes" im
          Frontend lassen sich diese unerwünschten Auswirkungen umgehen:
          Verbindungen ohne Datenübertragung werden vollständig ignoriert.
          Dadurch werden allerdings auch Fehler von Nutzern mit
          Verbindungsproblemen verborgen.

     CT   Der Client brach ab, während sein Stream mit tarpit verzögert wurde.
          Es ist wichtig zu prüfen, ob dies bei gültigen Anfragen geschieht,
          um fehlerhafte tarpit-Regeln auszuschließen. Bei vielen solchen
          Fällen kann es sinnvoll sein, "timeout tarpit" näher an den
          durchschnittlichen Messwert "Tw" zu senken, damit nicht wenige
          Angreifer unnötig Ressourcen binden.

     LC   HAProxy fing die Anfrage ab und verarbeitete sie lokal. Sie wurde
          nicht an den Server gesendet. Dies tritt nur bei einer Weiterleitung
          durch einen Parameter "redir" in der Serverzeile auf.

     LR   HAProxy fing die Anfrage ab und verarbeitete sie lokal. Sie wurde
          nicht an den Server gesendet. Gewöhnlich wurde eine Weiterleitung
          zurückgegeben, eine HTTP-return-Anweisung verarbeitet oder die
          Anfrage von einem Applet bearbeitet, etwa stats, cache,
          Prometheus-Exporter oder Lua-Applet.

     LH   HAProxy fing die Antwort ab und verarbeitete sie lokal. Gewöhnlich
          wurde eine Weiterleitung zurückgegeben oder eine HTTP-return-Anweisung
          verarbeitet.

     SC   Der Server oder ein Gerät zwischen ihm und HAProxy wies die
          TCP-Verbindung ausdrücklich zurück; der Proxy empfing ein TCP-RST
          oder eine ICMP-Nachricht. Unter bestimmten Umständen meldet auch
          der Netzwerk-Stack, dass der Server nicht erreichbar ist, etwa
          wegen einer fehlenden Route oder ARP-Antwort im lokalen Netz.
          Im HTTP-Modus ist der Statuscode dann vermutlich 502 oder 503.

     sC   "timeout connect" lief ab, bevor die Verbindung zum Server
          vollständig aufgebaut war. Im HTTP-Modus ist der Statuscode
          dann vermutlich 503 oder 504.

     SD   Die Serververbindung endete während der Datenübertragung mit einem
          Fehler. Gewöhnlich hat HAProxy beim Datenaustausch ein RST vom
          Server oder eine ICMP-Nachricht eines zwischengeschalteten Geräts
          empfangen. Ursache kann ein Serverabsturz oder ein Netzwerkproblem
          an einem zwischengeschalteten Gerät sein.

     sD   Der Server hat während der Datenphase für die gesamte Dauer von
          "timeout server" weder Daten gesendet noch bestätigt. Häufige
          Ursachen sind zu kurze Zeitgrenzen auf vorgeschalteten L4-Geräten
          wie Firewalls oder Load-Balancern sowie Keep-Alive-Sitzungen zwischen
          Client und Server, deren Zeitgrenze zuerst in HAProxy abläuft.

     SH   Der Server brach vor dem Senden seiner vollständigen HTTP-Antwort-
          Header ab oder stürzte bei der Anfrageverarbeitung ab. Ein Abbruch
          zu diesem Zeitpunkt ist sehr selten. Daher sollten seine Protokolle
          darauf geprüft werden, ob und warum er abgestürzt ist. Die
          protokollierte Anfrage kann auf eine kleine Gruppe fehlerhafter
          Anfragen hinweisen, die Programmfehler in der Anwendung auslösen.
          Gelegentlich kann auch ein IDS die Verbindung zwischen HAProxy
          und dem Server beenden.

     sH   "timeout server" lief ab, bevor der Server seine Antwort-Header
          zurückgeben konnte. Dies ist die häufigste Auffälligkeit und deutet
          auf zu lange Transaktionen hin, vermutlich wegen überlasteter Server
          oder Datenbanken. Kurzfristig hilft ein höherer Wert für "timeout server".
          Die langen Antwortzeiten beeinträchtigen aber die Nutzererfahrung.
          Die einzige dauerhafte Lösung besteht darin, die Anwendung zu korrigieren.

     sQ   Der Stream wartete zu lange in der Warteschlange und lief ab.
          Tritt dies zu oft auf, die Einstellungen "timeout queue" und
          "timeout connect" prüfen. Viele solche Fälle in kurzen Zeiträumen
          können auf allgemeine Serverprobleme durch I/O- oder Datenbankengpässe
          oder auf Überlastung durch externe Angriffe hindeuten.

     PC   Der Proxy verweigerte den Verbindungsaufbau zum Server, weil beim
          Versuch die Socket-Grenze des Prozesses erreicht wurde. Der globale
          Parameter "maxconn" kann erhöht werden, um dies zu verhindern.
          Dieser Zustand ist sehr selten und kann auftreten, wenn der globale
          Parameter "ulimit-n" von Hand erzwungen wird.

     PD   Nach dem Senden der Server-Header blockierte der Proxy eine fehlerhaft
          formatierte Nachricht mit Chunked-Kodierung in einer Anfrage oder
          Antwort. Meist handelt es sich um eine ungültige Nachricht vom Server
          an den Client. HAProxy unterstützt Chunk-Größen bis 2GB - 1
          (2147483647 Bytes). Größere Werte gelten als Fehler.

     PH   Der Proxy blockierte die Serverantwort, weil sie ungültig,
          unvollständig, gefährlich hinsichtlich der Cache-Steuerung war oder
          einem Sicherheitsfilter entsprach. Dabei erhält der Client einen
          HTTP-Fehler 502. Eine mögliche Ursache ist ein HTTP-Headername mit
          unzulässigen Zeichen. Selten kann der Proxy auch vor der Serverantwort
          eine syntaktisch ungültige Clientanfrage mit Chunked-Kodierung
          blockieren. Dann erhält der Client einen HTTP-Fehler 400, der auch
          protokolliert wird. Schließlich kann ein Fehler beim Umschreiben
          eines Antwort-Headers die Ursache sein. Dann wird ein HTTP-Fehler
          500 gesendet; siehe "tune.maxrewrite" und "http-response strict-mode".

     PR   Der Proxy blockierte die HTTP-Anfrage des Clients: Bei ungültiger
          HTTP-Syntax antwortete er mit einem HTTP-Fehler 400, bei einem
          passenden deny-Filter mit einem HTTP-Fehler 403. Auch ein Fehler
          beim Umschreiben eines Anfrage-Headers ist möglich. Dann wird
          ein HTTP-Fehler 500 gesendet; siehe "tune.maxrewrite" und
          "http-request strict-mode".

     PT   Der Proxy blockierte die Clientanfrage und verzögerte die Verbindung
          mit tarpit, bevor er einen Serverfehler 500 zurückgab. An den Server
          wurde nichts gesendet. Die Verbindung blieb so lange offen,
          wie der Messwert "Tw" angibt.

     RC   Eine lokale Ressource war erschöpft, etwa Speicher, Sockets oder
          Quellports, sodass die Serververbindung nicht aufgebaut werden konnte.
          Die Fehlerprotokolle nennen genau die fehlende Ressource. Dies ist
          sehr selten und lässt sich nur durch geeignete Systemanpassungen beheben.

Die Kombination der letzten beiden Flags zeigt ausführlich, wie Client, Server und HAProxy die Persistenz behandelt haben. Das ist bei Verbindungsabbrüchen sehr wichtig, wenn Nutzer über wiederholte Authentifizierung klagen. Häufig treten folgende Flags auf:

```text
--   Das Persistenz-Cookie ist nicht aktiviert.

NN   Der Client hat kein Cookie mitgesendet; in die Antwort wurde keines
     eingefügt. Dies kann beispielsweise im Insert-Modus mit "postonly"
     bei einer GET-Anfrage auftreten.

II   Das Client-Cookie bezeichnet einen ungültigen Server; in die
     Antwort wurde ein gültiges Cookie eingefügt. Dies geschieht meist,
     wenn ein "server"-Eintrag aus der Konfiguration entfernt wird:
     Ein Client kann dessen Cookie-Wert noch senden, obwohl kein
     anderer Server ihn kennt.

NI   Der Client hat kein Cookie mitgesendet; in die Antwort wurde eines
     eingefügt. Dies geschieht im Modus "insert" gewöhnlich bei der
     ersten Anfrage jedes Nutzers und erleichtert damit das Zählen
     tatsächlicher Nutzer.

VN   Der Client hat ein Cookie mitgesendet; in die Antwort wurde keines
     eingefügt. Dies gilt für die meisten Antworten, wenn der Client
     bereits ein Cookie hat.

VU   Der Client hat ein Cookie mit einem nicht ganz aktuellen Zeitpunkt
     des letzten Besuchs mitgesendet; die Antwort enthält deshalb ein
     aktualisiertes Cookie. Dies kann auch geschehen, wenn gar kein
     Zeitpunkt vorhanden war oder wenn ein Zeitpunkt vorhanden war,
     aber "maxidle" nicht gesetzt war, um das Cookie auf unbegrenzte
     Gültigkeit umzustellen.

EI   Der Zeitpunkt des letzten Besuchs im Client-Cookie war für
     "maxidle" zu alt. Das Cookie wurde ignoriert und in die Antwort
     ein neues eingefügt.

OI   Der Zeitpunkt des ersten Besuchs im Client-Cookie war für
     "maxlife" zu alt. Das Cookie wurde ignoriert und in die Antwort
     ein neues eingefügt.

DI   Der vom Cookie bezeichnete Server war ausgefallen. Ein neuer Server
     wurde ausgewählt und ein neues Cookie in der Antwort ausgegeben.

VI   Der vom Cookie bezeichnete Server war nicht als ausgefallen
     markiert, aber nicht erreichbar. Die Anfrage wurde an einen
     anderen Server umverteilt, der dann in der Antwort angegeben wurde.
```

## 8.6. Nicht druckbare Zeichen {#section-8-6}

Damit Protokollauswertungswerkzeuge und Terminals beim Lesen der Protokolle keine Probleme bekommen, werden nicht druckbare Zeichen nicht unverändert ausgegeben. Stattdessen erscheint ihr zweistelliger hexadezimaler ASCII-Code mit vorangestelltem '#'. Nur Zeichen zwischen 32 und 126 einschließlich können unmaskiert protokolliert werden. Das Maskierungszeichen '#' selbst wird zur Vermeidung von Mehrdeutigkeiten ebenfalls kodiert, als "#23". Dasselbe gilt für '"', das zu "#22" wird, sowie beim Protokollieren von Headern für '{', '\|' und '}'.

Dies gilt nicht für die cbor-Kodierung, die bereits sichere Hexadezimalziffern oder korrekt abgegrenzte Binärblöcke verwendet. Diese werden nicht an ein Terminal gesendet, sondern von einem CBOR-Parser verarbeitet.

Die json-Kodierung verwendet stattdessen JSON-Escape-Sequenzen. Mit der Option +utf8 werden außerdem gültige UTF-8-Sequenzen aus mehreren Bytes unverändert ausgegeben (siehe das Flag "utf8" in [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6)).

Das Leerzeichen (' ') wird in Headern nicht kodiert. Dies kann Werkzeuge beeinträchtigen, die Felder anhand der Anzahl von Leerzeichen bestimmen. Ein typischer Header mit Leerzeichen ist "User-Agent".

Einige syslog-Daemons wie syslog-ng maskieren das Anführungszeichen ('"') mit einem Backslash ('&#92;'). Dies kann gefahrlos rückgängig gemacht werden, da Anführungszeichen sonst nirgendwo in den Protokollen vorkommen dürfen.

## 8.7. HTTP-Cookies erfassen {#section-8-7}

Das Erfassen von Cookies erleichtert es, eine vollständige Nutzersitzung zu verfolgen. Dazu dient "capture cookie" im Frontend; Einzelheiten stehen in [Abschnitt 4.2](/de/docs/haproxy/proxies/#section-4-2). Es kann nur ein Cookie erfasst werden. Dasselbe Cookie wird gleichzeitig in der Anfrage (Header "Cookie:") und in der Antwort (Header "Set-Cookie:") geprüft. Die jeweiligen Werte erscheinen im HTTP-Protokoll in "captured_request_cookie" und "captured_response_cookie" (siehe [Abschnitt 8.2.3](/de/docs/haproxy/configuration-logging/#section-8-2-3) zum HTTP-Protokollformat). Fehlt eines der Cookies, steht statt seines Werts ein Bindestrich ('-'). Dadurch lässt sich etwa der Wechsel eines Nutzers in eine neue Sitzung leicht erkennen, da ihm der Server ein neues Cookie zuweist. Auch ein unerwartet falsch gesetztes Cookie, das Sitzungen zwischen Clients verwechselt, lässt sich so erkennen.

Beispiele:

```shell
# capture the first cookie whose name starts with "ASPSESSION"
capture cookie ASPSESSION len 32

# capture the first cookie whose name is exactly "vgnvisitor"
capture cookie vgnvisitor= len 32
```

Für weitergehende Erfassungen können "http-request"- und "http-response"-Regeln Cookies Variablen des Geltungsbereichs "txn" zuweisen. Die Werte lassen sich mit den Sample-Abruffunktionen "req.cook" und "res.cook" aus Anfrage oder Antwort auslesen (siehe [Abschnitt 7.3.6](/de/docs/haproxy/acls-and-samples/#section-7-3-6)) und mit "set-var" oder "set-var-fmt" einer Variablen zuweisen (siehe [Abschnitt 4.3](/de/docs/haproxy/proxies/#section-4-3)). Ein benutzerdefiniertes log-format kann diese Variablen dann an beliebiger Stelle ausgeben (siehe [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6)).

## 8.8. HTTP-Header erfassen (älteres Verfahren) {#section-8-8}

Das Erfassen von Headern hilft, eindeutige Anfragekennungen eines vorgeschalteten Proxys, virtuelle Hostnamen, User-Agents, content-length bei POST-Anfragen, Referrer und Ähnliches zu verfolgen. In Antworten lassen sich etwa Angaben zur Antwortlänge, zu den Vorgaben des Servers für den Cache oder zum Zielort eines Objekts bei einer Weiterleitung ermitteln.

Es gibt zwei Verfahren zur Header-Erfassung. Beim modernen Verfahren werden Variablen aus den gewünschten Headern oder aus zusammengesetzten Samples von "req.hdr_names", "req.hdrs", "res.hdr_names" und "res.hdrs" gesetzt; alle Möglichkeiten stehen in [Abschnitt 7.3.6](/de/docs/haproxy/acls-and-samples/#section-7-3-6). Mit den Aktionen "set-var" und "set-var-fmt" der Regelsätze "http-request" und "http-response" lassen sie sich Variablen des Geltungsbereichs "txn" zuweisen (siehe [Abschnitt 4.3](/de/docs/haproxy/proxies/#section-4-3)). Diese können dann in benutzerdefinierten Protokollformaten referenziert werden (siehe [Abschnitt 8.2.6](/de/docs/haproxy/configuration-logging/#section-8-2-6)). Dies ist das empfohlene Verfahren zur Erfassung von HTTP-Headern.

Daneben gibt es das ältere Verfahren aus der Zeit vor http-request-Regeln und Variablen. Es erfordert keine Anpassung des Protokollformats und wird seit Langem sowohl zur Protokollierung als auch als Behelf verwendet, um Anfrageinformationen über die gesamte HTTP-Transaktion hinweg weiterzugeben. Es verwendet die älteren "capture"-Regelsätze und wird in diesem Abschnitt beschrieben.

Beim älteren Verfahren werden Header mit "capture request header" und "capture response header" im Frontend erfasst. Einzelheiten stehen in den Definitionen in [Abschnitt 4.2](/de/docs/haproxy/proxies/#section-4-2).

Anfrage- und Antwort-Header können gleichzeitig erfasst werden. Fehlende Header werden als leere Zeichenketten protokolliert. Kommt ein Header mehrfach vor, wird nur das letzte Vorkommen erfasst. Anfrage-Header werden in der Reihenfolge ihrer Deklaration innerhalb geschweifter Klammern '{' und '}' zusammengefasst und durch '\|' ohne Leerzeichen getrennt. Antwort-Header haben dieselbe Darstellung und folgen nach einem Leerzeichen auf den Block der Anfrage-Header. Beide Blöcke stehen im Protokoll unmittelbar vor der HTTP-Anfrage.

Als Sonderfall kann die Erfassung eines HTTP-Headers in einem TCP-Frontend definiert werden. Damit lassen sich Header protokollieren, die in einem HTTP-Backend ausgewertet werden, wenn die Anfrage anschließend an dieses Backend übergeben wird.

Beispiel:

```shell
# This instance chains to the outgoing proxy
listen proxy-out
    mode http
    option httplog
    option logasap
    log global
    server cache1 192.168.1.1:3128

    # log the name of the virtual server
    capture request  header Host len 20

    # log the amount of data uploaded during a POST
    capture request  header Content-Length len 10

    # log the beginning of the referrer
    capture request  header Referer len 20

    # server name (useful for outgoing proxies only)
    capture response header Server len 20

    # logging the content-length is useful with "option logasap"
    capture response header Content-Length len 10

    # log the expected cache behavior on the response
    capture response header Cache-Control len 8

    # the Via header will report the next proxy's name
    capture response header Via len 20

    # log the URL location during a redirection
    capture response header Location len 20
```

```text
    >>> Aug  9 20:26:09 localhost \
          haproxy[2022]: 127.0.0.1:34014 [09/Aug/2004:20:26:09] proxy-out \
          proxy-out/cache1 0/0/0/162/+162 200 +350 - - ---- 0/0/0/0/0 0/0 \
          {fr.adserver.yahoo.co||http://fr.f416.mail.} {|864|private||} \
          "GET http://fr.adserver.yahoo.com/"
```

```text
    >>> Aug  9 20:30:46 localhost \
          haproxy[2022]: 127.0.0.1:34020 [09/Aug/2004:20:30:46] proxy-out \
          proxy-out/cache1 0/0/0/182/+182 200 +279 - - ---- 0/0/0/0/0 0/0 \
          {w.ods.org||} {Formilux/0.1.8|3495|||} \
          "GET http://trafic.1wt.eu/ HTTP/1.1"
```

```text
    >>> Aug  9 20:30:46 localhost \
          haproxy[2022]: 127.0.0.1:34028 [09/Aug/2004:20:30:46] proxy-out \
          proxy-out/cache1 0/0/2/126/+128 301 +223 - - ---- 0/0/0/0/0 0/0 \
          {www.sytadin.equipement.gouv.fr||http://trafic.1wt.eu/} \
          {Apache|230|||http://www.sytadin.} \
          "GET http://www.sytadin.equipement.gouv.fr/ HTTP/1.1"
```

## 8.9. Protokollbeispiele {#section-8-9}

Die folgenden Protokollbeispiele mit Erläuterungen stammen aus der Praxis; einige wurden von Hand erstellt. Zur besseren Lesbarkeit wurde der syslog-Teil entfernt. Sie sollen ausschließlich erklären, wie die Meldungen zu lesen sind.

    >>> haproxy[674]: 127.0.0.1:33318 [15/Oct/2003:08:31:57.130] px-http &#92;
          px-http/srv1 6559/0/7/147/6723 200 243 - - ---- 5/3/3/1/0 0/0 &#92;
          "HEAD / HTTP/1.0"

    => Eine lange Anfrage (6.5s) wurde von Hand über 'telnet' eingegeben.
       Der Server antwortete in 147 ms; die Sitzung endete normal ('----').

    >>> haproxy[674]: 127.0.0.1:33319 [15/Oct/2003:08:31:57.149] px-http &#92;
          px-http/srv1 6559/1230/7/147/6870 200 243 - - ---- 324/239/239/99/0 &#92;
          0/9 "HEAD / HTTP/1.0"

    => Wie zuvor, aber die Anfrage stand hinter 9 anderen Anfragen in
       der globalen Warteschlange und wartete dort 1230 ms.

```text
    >>> haproxy[674]: 127.0.0.1:33320 [15/Oct/2003:08:32:17.654] px-http \
          px-http/srv1 9/0/7/14/+30 200 +243 - - ---- 3/3/3/1/0 0/0 \
          "GET /image.iso HTTP/1.0"
```

    => Anfrage für eine lange Datenübertragung. Da "logasap" gesetzt war,
       wurde die Meldung unmittelbar vor der Datenübertragung ausgegeben.
       Der Server antwortete in 14 ms, 243 Header-Bytes wurden an den Client
       gesendet, und von der Annahme bis zum ersten Datenbyte vergingen 30 ms.

    >>> haproxy[674]: 127.0.0.1:33320 [15/Oct/2003:08:32:17.925] px-http &#92;
          px-http/srv1 9/0/7/14/30 502 243 - - PH-- 3/2/2/0/0 0/0 &#92;
          "GET /cgi-bin/bug.cgi? HTTP/1.0"

    => Der Proxy blockierte eine Serverantwort: entweder aufgrund einer
       "http-response deny"-Regel, wegen eines fehlerhaften, nicht HTTP-konformen
       Formats oder weil sensible Informationen hätten zwischengespeichert
       werden können. Die Antwort wird dann durch "502 bad gateway" ersetzt.
       Die Flags ("PH--") zeigen, dass HAProxy die 502 zurückgab, nicht der Server.

    >>> haproxy[18113]: 127.0.0.1:34548 [15/Oct/2003:15:18:55.798] px-http &#92;
          px-http/`<NOSRV>` -1/-1/-1/-1/8490 -1 0 - - CR-- 2/2/2/0/0 0/0 ""

    => Der Client vervollständigte seine Anfrage nie und brach nach 8.5s
       selbst ab ("C---"), während der Proxy auf die Anfrage-Header wartete
       ("-R--"). An keinen Server wurde etwas gesendet.

    >>> haproxy[18113]: 127.0.0.1:34549 [15/Oct/2003:15:19:06.103] px-http &#92;
         px-http/`<NOSRV>` -1/-1/-1/-1/50001 408 0 - - cR-- 2/2/2/0/0 0/0 ""

    => Der Client vervollständigte seine Anfrage nie. Nach 50s wurde sie
       durch die Zeitüberschreitung abgebrochen ("c---"), während der Proxy
       auf die Anfrage-Header wartete ("-R--"). An keinen Server wurde etwas
       gesendet; der Proxy konnte dem Client jedoch den Statuscode 408 senden.

    >>> haproxy[18989]: 127.0.0.1:34550 [15/Oct/2003:15:24:28.312] px-tcp &#92;
          px-tcp/srv1 0/0/5007 0 cD 0/0/0/0/0 0/0

    => Diese Meldung wurde mit "option tcplog" erzeugt. Die Clientzeitgrenze
       lief nach 5 Sekunden ab ("c----").

    >>> haproxy[18989]: 10.0.0.1:34552 [15/Oct/2003:15:26:31.462] px-http &#92;
          px-http/srv1 3183/-1/-1/-1/11215 503 0 - - SC-- 205/202/202/115/3 &#92;
          0/0 "HEAD / HTTP/1.0"

    => Die Anfrage benötigte 3s bis zur Vollständigkeit, vermutlich wegen
       eines Netzwerkproblems. Die Serververbindung schlug nach 4 Versuchen
       von je 2 Sekunden fehl ('SC--'); konfiguriert war 'retries 3'. Es gab
       keine Umverteilung, sonst wäre "/+3" zu sehen. Der Client erhielt
       Statuscode 503. Auf diesem Server bestanden 115 Verbindungen, auf
       diesem Proxy 202 und im gesamten Prozess 205. Möglicherweise wies
       der Server die Verbindung wegen zu vieler bestehender Verbindungen ab.
