---
title: "4. Proxys"
linkTitle: "4. Proxys"
weight: 150
description: "Standardwerte, Frontends, Backends, Listener sowie Referenzen der Proxy-Schlüsselwörter und Aktionen"
icon: fa-solid fa-right-left
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/proxies/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 4"
---

Die Proxy-Konfiguration kann in einer Reihe von Abschnitten definiert werden:

- defaults [`<name>`] [ from `<defaults_name>` ]
- frontend `<name>` [ from `<defaults_name>` ]
- backend `<name>` [ from `<defaults_name>` ]
- listen `<name>` [ from `<defaults_name>` ]

Ein "frontend"-Abschnitt beschreibt eine Gruppe lauschender Sockets, die Clientverbindungen annehmen.

Ein "backend"-Abschnitt beschreibt eine Gruppe von Servern, mit denen der Proxy eine Verbindung herstellt, um eingehende Verbindungen weiterzuleiten.

Ein "listen"-Abschnitt definiert einen vollständigen Proxy, bei dem Frontend- und Backend-Teil in einem einzigen Abschnitt kombiniert sind. Dies ist im Allgemeinen für rein TCP-basierten Datenverkehr nützlich.

Ein "defaults"-Abschnitt setzt alle Einstellungen auf die dokumentierten Standardwerte zurück und legt neue Werte für die nachfolgenden Abschnitte fest. Alle "frontend", "backend" und "listen"-Abschnitte beziehen ihre Anfangseinstellungen immer aus einem defaults-Abschnitt, standardmäßig den zuletzt vor dem neu erstellten Abschnitt definierten. Es ist möglich, explizit einen bestimmten "defaults"-Abschnitt anzugeben, von dem die Anfangseinstellungen geladen werden sollen, indem dessen Name in der Abschnittszeile nach dem optionalen Schlüsselwort "from" angegeben wird. Während "defaults"-Abschnitte keinen Namen erfordern, wird die Angabe eines Namens für bessere Lesbarkeit empfohlen. Dies ist auch die einzige Möglichkeit, einen bestimmten Abschnitt anstelle des Standardvorgängers anzugeben. Da "defaults"-Abschnittsnamen optional sind, wird standardmäßig eine sehr großzügige Prüfung auf deren Namen angewendet, und diese dürfen sogar überlappen. Wenn jedoch ein "defaults"-Abschnitt von einem anderen Abschnitt referenziert wird, muss dessen Name der Syntax entsprechen, die für alle Proxy-Namen gilt, und dieser Name muss innerhalb der defaults-Abschnitte eindeutig sein. Bitte beachten Sie, dass unabhängig davon, was derzeit erlaubt ist, generell von der Verwendung doppelter Abschnittsnamen abgeraten wird und die gleiche Syntax wie für Proxy-Namen eingehalten werden sollte. Diese Regel könnte in einer zukünftigen Version verbindlich werden. Zudem wird eine Warnung ausgegeben, wenn ein defaults-Abschnitt explizit von einem Proxy verwendet wird, während er gleichzeitig implizit von einem anderen Proxy verwendet wird, weil er der zuletzt definierte ist. Es wird dringend empfohlen, beide Verwendungsarten nicht zu mischen, sondern entweder stets explizite Referenzen zu verwenden oder einen letzten gemeinsamen defaults-Abschnitt bereitzustellen, der ausschließlich für implizite Verwendungen reserviert ist.

Beachten Sie, dass ein defaults-Abschnitt auch seine Anfangseinstellungen von einem anderen defaults-Abschnitt beziehen kann, und dadurch Einstellungen über mehrere Ebenen von defaults-Abschnitten vererbt werden können. Dies kann praktisch sein, um bestimmte Konfigurationsprofile zu erstellen, die Gruppen von Standardwerten enthalten (z. B. TCP oder HTTP sowie kurze oder lange Zeitüberschreitungen), kann aber schnell unübersichtlich werden.

Standardmäßig werden benannte defaults-Abschnitte nach der Konfigurationsanalyse beibehalten. Dies ermöglicht deren Wiederverwendung bei der dynamischen Erstellung von Backends. Dieses Verhalten kann global über das Schlüsselwort "tune.defaults.purge" geändert werden.

Alle Proxy-Namen müssen aus Groß- und Kleinbuchstaben, Ziffern, '-' (Bindestrich), '\_' (Unterstrich), '.' (Punkt) und ':' (Doppelpunkt) gebildet werden. Bei ACL-Namen wird zwischen Groß- und Kleinschreibung unterschieden. Daher bezeichnen "www" und "WWW" zwei verschiedene Proxys.

Historisch gesehen konnten sich alle Proxy-Namen unter bestimmten Bedingungen überlappen (z. B. wenn sie nicht über dieselben Frontend- oder Backend-Funktionen verfügten), doch dies verursachte zu viele Probleme in den Protokollen sowie Verwirrung bei CLI-Operationen, Stick-Table-Namen und Statistikabfragen. Zwei Proxys müssen nun unabhängig von ihren jeweiligen Funktionen unterschiedliche Namen haben.

Derzeit werden zwei wesentliche Proxy-Modi unterstützt: "tcp", auch bekannt als Schicht 4, und "http", auch bekannt als Schicht 7. Im Modus für Schicht 4 leitet HAProxy bidirektionalen Datenverkehr einfach zwischen zwei Seiten weiter. Im Modus für Schicht 7 analysiert HAProxy das Protokoll und kann anhand beliebiger Kriterien damit interagieren, indem es beliebige Inhalte in Anfragen oder Antworten zulässt, blockiert, umschaltet, hinzufügt, ändert oder entfernt.

Im HTTP-Modus hängt die Verarbeitung von Anfragen und Antworten, die über eine Verbindung fließen, von der Kombination der HTTP-Optionen im Frontend und im Backend ab. HAProxy unterstützt 3 Verbindungsmodi:

- KAL: Keep-Alive ("option http-keep-alive"), der Standardmodus: Alle Anfragen und Antworten werden verarbeitet, und die Verbindungen bleiben zwischen Antworten und neuen Anfragen offen, aber inaktiv.

- SCL: Serververbindung schließen ("option http-server-close"): Die Verbindung zum Server wird geschlossen, nachdem das Ende der Antwort empfangen wurde; die Verbindung zum Client bleibt offen.

- CLO: Verbindung schließen ("option httpclose"): Die Verbindung wird nach Ende der Antwort geschlossen, und in beiden Richtungen wird "Connection: close" angehängt.

Der effektive Modus, der auf eine Verbindung angewendet wird, die durch ein Frontend und ein Backend läuft, kann je nach Proxy-Modus anhand der folgenden Matrix bestimmt werden, aber kurz gesagt sind die Modi symmetrisch, Keep-Alive ist die schwächste Option und das Schließen der Verbindung die stärkste.

                   Backend-Modus

```text
                | KAL | SCL | CLO
            ----+-----+-----+----
            KAL | KAL | SCL | CLO
            ----+-----+-----+----
   Modus    SCL | SCL | SCL | CLO
            ----+-----+-----+----
            CLO | CLO | CLO | CLO
```

Es ist möglich, ein TCP-Frontend an ein HTTP-Backend anzuschließen. Dies ist sinnlos, wenn nur HTTP-Verkehr behandelt wird. Es kann jedoch genutzt werden, um mehrere Protokolle innerhalb desselben Frontends zu verarbeiten. In diesem Fall wird die Clientverbindung zunächst als rohe TCP-Verbindung behandelt, bevor sie auf HTTP umgestellt wird. Vor dem Protokollwechsel werden die Inhaltsverarbeitungen auf Rohdaten durchgeführt. Nach dem Protokollwechsel werden die Daten analysiert und intern als HTX gespeichert, wodurch die Verwendung der Rohdarstellung nicht mehr möglich ist. Es gibt keine Möglichkeit, zurückzukehren.

Es gibt zwei Arten von Protokollwechseln: In-Place-Protokollwechsel und destruktive Protokollwechsel. Erstere beinhalten einen TCP-zu-HTTP/1-Protokollwechsel. In HTTP/1 werden die Anfrageverarbeitungen serialisiert, wodurch der anwendungsbezogene Datenstrom erhalten bleiben kann. Letztere beinhalten einen TCP-zu-HTTP/2-Protokollwechsel. Da es sich um ein multiplextes Protokoll handelt, kann der anwendungsbezogene Datenstrom keinem HTTP/2-Datenstrom zugeordnet werden und wird zerstört. Neue anwendungsbezogene Datenströme werden dann erstellt, wenn HAProxy neue HTTP/2-Datenströme auf der unteren Ebene im H2-Multiplexer empfängt. Es ist wichtig, diesen Unterschied zu verstehen, da dies die Art und Weise, wie Daten verarbeitet werden, grundlegend verändert. Bei einem HTTP/1-Protokollwechsel gehen die bereits auf Rohdaten durchgeführten Inhaltsverarbeitungen weder verloren noch werden sie erneut ausgeführt, während bei einem HTTP/2-Protokollwechsel die anwendungsbezogenen Datenströme getrennt sind und alle Frontend-Regeln systematisch auf jeden einzelnen angewendet werden. Wie bereits erwähnt, wird der erste Datenstrom, der TCP-Datenstrom, zerstört, jedoch erst nachdem die Frontend-Regeln ausgewertet wurden.

Bei der HTTP-Verarbeitung aus einem TCP-Proxy heraus ist außerdem zu beachten: HAProxy kann HTTP/1 während der tcp-request content-Regeln analysieren, aber nicht HTTP/2. Es ist lediglich möglich, die HTTP/2-Verbindungspräambel zu analysieren. Dies stellt eine erhebliche Einschränkung bezüglich der HTTP-Inhaltsanalyse im TCP-Modus dar. Konkret ist es nur möglich festzustellen, ob empfangene Daten HTTP sind. Zum Beispiel ist es nicht möglich, aufgrund des Host-Headers ein Backend auszuwählen, was in HTTP/1 trivial ist. Glücklicherweise gibt es eine Lösung, um diesen Nachteil zu mildern.

Es gibt zwei Möglichkeiten, einen HTTP-Protokollwechsel durchzuführen. Die erste, historische Methode, besteht darin, ein HTTP-Backend auszuwählen. Der Protokollwechsel erfolgt, wenn das Backend festgelegt wird. Für In-Place-Protokollwechsel wird nur die Backend-Konfiguration bei der HTTP-Datenverarbeitung berücksichtigt. Bei destruktiven Protokollwechseln wird der anwendungsbezogene Datenstrom zerstört, wodurch die Verarbeitung gestoppt wird. Mit dieser Methode sind die Möglichkeiten, ein Backend mit einer HTTP/2-Verbindung auszuwählen, wirklich begrenzt, wie oben erwähnt, und etwas sinnlos, da der Datenstrom zerstört wird. Die zweite Methode besteht darin, während der Auswertung der tcp-request content-Regeln den Protokollwechsel durchzuführen, mithilfe der Aktion "switch-mode http". In diesem Fall erfolgt der Protokollwechsel im Frontend-Kontext, und es ist möglich, HTTP-Direktiven in diesem Frontend zu definieren. Für In-Place-Protokollwechsel bietet dies sofort die volle Leistungsfähigkeit der HTTP-Analyse. Das Verhalten ähnelt damit stark dem eines HTTP-Frontends. Bei destruktiven Protokollwechseln ändert sich nichts, außer dass es sinnlos ist, ein Backend auf Basis begrenzter Informationen auszuwählen. Dies ist natürlich die empfohlene Methode. Daher ist es ausreichend, im Rahmen der tcp-request content-Regeln den Anfrageprotokolltyp zu prüfen, um einen HTTP-Protokollwechsel durchzuführen. Alle verbleibenden HTTP-Manipulationen können dann in die http-request-Regelmenge des Frontends verlegt werden. Behalten Sie jedoch im Hinterkopf, dass die tcp-request content-Regeln weiterhin auf jedem Datenstrom ausgewertet werden, was sich nicht ändern lässt.

## 4.1. Matrix der Proxy-Schlüsselwörter {#section-4-1}

Die folgende Liste von Schlüsselwörtern wird unterstützt. Die meisten davon können nur in einem begrenzten Satz von Abschnittstypen verwendet werden. Einige sind als „veraltet“ markiert, da sie aus einer alten Syntax stammen, die verwirrend oder funktional eingeschränkt sein kann, und es gibt neue empfohlene Schlüsselwörter, die sie ersetzen sollen. Schlüsselwörter, die mit "(\*)" markiert sind, können optional mit dem Präfix "no" invertiert werden, z. B. "no option contstats". Dies ist sinnvoll, wenn die Option standardmäßig aktiviert ist und für einen bestimmten Fall deaktiviert werden muss. Solche Optionen können auch mit "default" präfixiert werden, um die Standardwerte unabhängig von vorherigen "defaults"-Abschnitten wiederherzustellen. Schlüsselwörter, die in defaults-Abschnitten unterstützt werden und mit "(!)" markiert sind, sind nur in benannten defaults-Abschnitten, nicht in anonymen, unterstützt.

Hinweis: Einige gefährliche und nicht empfohlene Direktiven sind bewusst nicht in der folgenden Matrix aufgeführt. Das ist beabsichtigt. Diese Direktiven sind dokumentiert. Doch durch ihre Nicht-Aufnahme in dieser Liste wird noch ein weiterer Weg geschaffen, um von ihrer Verwendung abzuraten.

```text
 Schlüsselwort                        defaults   frontend   listen    backend
------------------------------------+----------+----------+---------+---------
acl                                       X (!)      X         X         X
backlog                                   X          X         X         -
balance                                   X          -         X         X
be-unpublished                            -          -         X         X
bind                                      -          X         X         -
capture cookie                            -          X         X         -
capture request header                    -          X         X         -
capture response header                   -          X         X         -
clitcpka-cnt                              X          X         X         -
clitcpka-idle                             X          X         X         -
clitcpka-intvl                            X          X         X         -
compression                               X          X         X         X
cookie                                    X          -         X         X
crt                                       -          X         X         -
declare capture                           -          X         X         -
default-server                            X          -         X         X
default_backend                           X          X         X         -
description                               -          X         X         X
disabled                                  X          X         X         X
dispatch                    (deprecated)  -          -         X         X
email-alert from                          X          X         X         X
email-alert level                         X          X         X         X
email-alert mailers                       X          X         X         X
email-alert myhostname                    X          X         X         X
email-alert to                            X          X         X         X
enabled                                   X          X         X         X
errorfile                                 X          X         X         X
errorfiles                                X          X         X         X
errorloc                                  X          X         X         X
errorloc302                               X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
errorloc303                               X          X         X         X
error-log-format                          X          X         X         -
external-check command                    X          -         X         X
external-check path                       X          -         X         X
force-persist                             -          -         X         X
force-be-switch                           -          X         X         -
filter                                    -          X         X         X
fullconn                                  X          -         X         X
guid                                      -          X         X         X
hash-balance-factor                       X          -         X         X
hash-preserve-affinity                    X          -         X         X
hash-type                                 X          -         X         X
http-after-response                       X (!)      X         X         X
http-check comment                        X          -         X         X
http-check connect                        X          -         X         X
http-check disable-on-404                 X          -         X         X
http-check expect                         X          -         X         X
http-check send                           X          -         X         X
http-check send-state                     X          -         X         X
http-check set-var                        X          -         X         X
http-check unset-var                      X          -         X         X
http-error                                X          X         X         X
http-request                              X (!)      X         X         X
http-response                             X (!)      X         X         X
http-reuse                                X          -         X         X
http-send-name-header                     X          -         X         X
id                                        -          X         X         X
ignore-persist                            -          -         X         X
load-server-state-from-file               X          -         X         X
log                                  (*)  X          X         X         X
log-format                                X          X         X         -
log-format-sd                             X          X         X         -
log-tag                                   X          X         X         X
log-steps                                 X          X         X         -
max-keep-alive-queue                      X          -         X         X
max-session-srv-conns                     X          X         X         -
maxconn                                   X          X         X         -
mode                                      X          X         X         X
monitor fail                              -          X         X         -
monitor-uri                               X          X         X         -
option abortonclose                  (*)  X          X         X         X
option allbackups                    (*)  X          -         X         X
option checkcache                    (*)  X          -         X         X
option clitcpka                      (*)  X          X         X         -
option contstats                     (*)  X          X         X         -
option disable-h2-upgrade            (*)  X          X         X         -
option dontlog-normal                (*)  X          X         X         -
option dontlognull                   (*)  X          X         X         -
-- keyword -------------------------- defaults - frontend - listen -- backend -
option external-check                     X          -         X         X
option forwardfor                         X          X         X         X
option forwarded                     (*)  X          -         X         X
option h1-case-adjust-bogus-client   (*)  X          X         X         -
option h1-case-adjust-bogus-server   (*)  X          -         X         X
option http-buffer-request           (*)  X          X         X         X
option http-drop-request-trailers    (*)  X          -         -         X
option http-drop-response-trailers   (*)  X          -         X         -
option http-ignore-probes            (*)  X          X         X         -
option http-keep-alive               (*)  X          X         X         X
option http-no-delay                 (*)  X          X         X         X
option http-pretend-keepalive        (*)  X          -         X         X
option http-restrict-req-hdr-names        X          X         X         X
option http-server-close             (*)  X          X         X         X
option http-use-proxy-header         (*)  X          X         X         -
option httpchk                            X          -         X         X
option httpclose                     (*)  X          X         X         X
option httplog                            X          X         X         -
option httpslog                           X          X         X         -
option idle-close-on-response        (*)  X          X         X         -
option independent-streams           (*)  X          X         X         X
option ldap-check                         X          -         X         X
option log-health-checks             (*)  X          -         X         X
option log-separate-errors           (*)  X          X         X         -
option logasap                       (*)  X          X         X         -
option mysql-check                        X          -         X         X
option nolinger                      (*)  X          X         X         X
option originalto                         X          X         X         X
option persist                       (*)  X          -         X         X
option pgsql-check                        X          -         X         X
option prefer-last-server            (*)  X          -         X         X
option redispatch                    (*)  X          -         X         X
option redis-check                        X          -         X         X
option smtpchk                            X          -         X         X
option socket-stats                  (*)  X          X         X         -
option splice-auto                   (*)  X          X         X         X
option splice-request                (*)  X          X         X         X
option splice-response               (*)  X          X         X         X
option spop-check                         X          -         X         X
option srvtcpka                      (*)  X          -         X         X
option ssl-hello-chk                      X          -         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
option tcp-check                          X          -         X         X
option tcp-smart-accept              (*)  X          X         X         -
option tcp-smart-connect             (*)  X          -         X         X
option tcpka                              X          X         X         X
option tcplog                             X          X         X         -
option transparent      (deprecated) (*)  X          -         X         X
option use-small-buffers             (*)  X          -         X         X
persist rdp-cookie                        X          -         X         X
quic-initial                              X (!)      X         X         -
rate-limit sessions                       X          X         X         -
redirect                                  -          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
retries                                   X          -         X         X
retry-on                                  X          -         X         X
server                                    -          -         X         X
server-state-file-name                    X          -         X         X
server-template                           -          -         X         X
source                                    X          -         X         X
srvtcpka-cnt                              X          -         X         X
srvtcpka-idle                             X          -         X         X
srvtcpka-intvl                            X          -         X         X
stats admin                               -          X         X         X
stats auth                                X          X         X         X
stats enable                              X          X         X         X
stats hide-version                        X          X         X         X
stats http-request                        -          X         X         X
stats realm                               X          X         X         X
stats refresh                             X          X         X         X
stats scope                               X          X         X         X
stats show-desc                           X          X         X         X
stats show-legends                        X          X         X         X
stats show-node                           X          X         X         X
stats show-version                        X          X         X         X
stats uri                                 X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
stick match                               -          -         X         X
stick on                                  -          -         X         X
stick store-request                       -          -         X         X
stick store-response                      -          -         X         X
stick-table                               -          X         X         X
tcp-check comment                         X          -         X         X
tcp-check connect                         X          -         X         X
tcp-check expect                          X          -         X         X
tcp-check send                            X          -         X         X
tcp-check send-lf                         X          -         X         X
tcp-check send-binary                     X          -         X         X
tcp-check send-binary-lf                  X          -         X         X
tcp-check set-var                         X          -         X         X
tcp-check unset-var                       X          -         X         X
tcp-request connection                    X (!)      X         X         -
tcp-request content                       X (!)      X         X         X
tcp-request inspect-delay                 X (!)      X         X         X
tcp-request session                       X (!)      X         X         -
tcp-response content                      X (!)      -         X         X
tcp-response inspect-delay                X (!)      -         X         X
timeout check                             X          -         X         X
timeout client                            X          X         X         -
timeout client-fin                        X          X         X         -
timeout client-hs                         X          X         X         -
timeout connect                           X          -         X         X
timeout http-keep-alive                   X          X         X         X
timeout http-request                      X          X         X         X
timeout queue                             X          -         X         X
timeout server                            X          -         X         X
timeout server-fin                        X          -         X         X
timeout tarpit                            X          X         X         X
timeout tunnel                            X          -         X         X
transparent                 (deprecated)  X          -         X         X
unique-id-format                          X          X         X         X
unique-id-header                          X          X         X         -
use_backend                               -          X         X         -
use-fcgi-app                              -          -         X         X
use-server                                -          -         X         X
------------------------------------+----------+----------+---------+---------
 Schlüsselwort                        defaults   frontend   listen    backend
```

## 4.2. Alphabetisch sortierte Schlüsselwortreferenz {#section-4-2}

Dieser Abschnitt enthält eine Beschreibung jedes Schlüsselworts und seiner Verwendung.

<a id="entry-4-2-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

Eine Zugriffskontrollliste anlegen oder ergänzen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Diese Anweisung ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. ACLs, die in einem defaults-Abschnitt definiert sind, sind aus anderen Abschnitten, die ihn verwenden, nicht sichtbar.

Beispiel:

```text
acl invalid_src  src          0.0.0.0/7 224.0.0.0/3
acl invalid_src  src_port     0:1023
acl local_dst    hdr(host) -i localhost
```

Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

Dem System Hinweise auf die ungefähre gewünschte Größe der Listen-Warteschlange geben

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<conns>   ist die Zahl ausstehender Verbindungen. Je nach Betriebssystem
          kann dies bereits bestätigte Verbindungen, noch nicht bestätigte
          Verbindungen oder beide zusammen bezeichnen.
```

Diese Option ist nur für Stream-Listener, einschließlich QUIC-Listener, von Bedeutung. Bei QUIC-Instanzen verhält sie sich jedoch anders.

Für alle Listener außer QUIC besteht eine Möglichkeit zum Schutz vor SYN-Flood-Angriffen darin, die Größe des SYN-Backlogs des Systems zu erhöhen. Je nach System ist dies manchmal über einen Systemparameter einstellbar, manchmal nicht einstellbar und manchmal richtet sich das System nach Hinweisen, die die Anwendung beim Aufruf von listen() bereitstellt. Standardmäßig übergibt HAProxy den Wert von maxconn des Frontends an den listen()-Aufruf. Auf Systemen, die diesen Wert nutzen können, kann es gelegentlich sinnvoll sein, einen anderen Wert anzugeben, weshalb dieser backlog-Parameter existiert.

Unter Linux 2.4 wird der Parameter vom System ignoriert. Unter Linux 2.6 wird er als Hinweis verwendet, und das System akzeptiert Werte bis zur nächstgrößeren Zweierpotenz, jedoch nie oberhalb bestimmter Grenzen (üblicherweise 32768).

Für QUIC-Listener legt backlog eine gemeinsame Grenze für die maximale Anzahl aktiver Handshakes und Verbindungen fest, die darauf warten, angenommen zu werden. Die Handshake-Phase hängt hauptsächlich von der Netzwerklatenz zum entfernten Peer ab, während die zweite Phase ausschließlich von der Last von haproxy abhängt. Wenn eine dieser Grenzen erreicht ist, beginnt haproxy, empfangene INITIAL-Pakete zu verwerfen, wodurch keine neuen Verbindungen mehr angelegt werden können, bis der Überschuss an Verbindungen abnimmt. Dieser Zustand kann dazu führen, dass Browser stillschweigend auf eine ältere HTTP-Version wechseln und auf TCP umschalten.

Siehe auch: "maxconn" und die Optimierungshilfe des Zielbetriebssystems.

<a id="entry-4-2-balance"></a>

**`balance <algorithm> [ <arguments> ]`**

```haproxy
balance <algorithm> [ <arguments> ]
balance url_param <param> [check_post]
```

Den in einem Backend zu verwendenden Lastverteilungsalgorithmus festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<algorithm> ist der Algorithmus zur Auswahl eines Servers für die
            Lastverteilung. Dies gilt nur, wenn keine Informationen zur
            Sitzungsbindung vorliegen oder eine Verbindung einem anderen
            Server neu zugewiesen wird. <algorithm> kann einer der folgenden
            Algorithmen sein:

  roundrobin  Jeder Server wird entsprechend seinem Gewicht abwechselnd
              verwendet. Dies ist der gleichmäßigste und fairste Algorithmus,
              solange die Verarbeitungszeiten der Server gleichmäßig verteilt
              bleiben. Dieser Algorithmus ist dynamisch: Servergewichte können
              im laufenden Betrieb angepasst werden, beispielsweise für einen
              langsamen Anlauf. Konstruktionsbedingt ist er auf 4095 aktive
              Server pro Backend begrenzt. In manchen großen Servergruppen
              kann es nach einem sehr kurzen Ausfall gelegentlich einige
              Hundert Anfragen dauern, bis ein wieder verfügbarer Server in
              die Gruppe aufgenommen wird und Datenverkehr empfängt. Das ist
              normal, wenn auch sehr selten. Dieser Hinweis soll vermeiden,
              dass Sie sich Sorgen machen, falls Sie dies beobachten.
              Hinweis: Bei Backends im LOG-Modus werden Gewichte ignoriert.

  static-rr   Jeder Server wird entsprechend seinem Gewicht abwechselnd
              verwendet. Dieser Algorithmus ähnelt roundrobin, ist jedoch
              statisch: Eine Änderung des Servergewichts im laufenden Betrieb
              hat keine Wirkung. Dafür gibt es keine konstruktionsbedingte
              Begrenzung der Serverzahl. Ein wieder verfügbarer Server wird
              unmittelbar wieder in die Gruppe aufgenommen, sobald die gesamte
              Zuordnung neu berechnet wurde. Außerdem benötigt dieser
              Algorithmus etwas weniger CPU-Leistung (etwa -1%). Er kann nicht
              im LOG-Modus verwendet werden.

  leastconn   Der Server mit den wenigsten Verbindungen erhält die Verbindung.
              Innerhalb von Gruppen gleich ausgelasteter Server wird
              Round-Robin verwendet, damit alle Server zum Einsatz kommen.
              Dieser Algorithmus wird für sehr lange Sitzungen empfohlen,
              etwa bei LDAP, SQL oder TSE. Für Protokolle mit kurzen Sitzungen
              wie HTTP eignet er sich dagegen weniger gut. Der Algorithmus
              ist dynamisch: Servergewichte können im laufenden Betrieb
              angepasst werden, beispielsweise für einen langsamen Anlauf.
              Neben bestehenden Verbindungen berücksichtigt er auch wartende
              Verbindungen, um Warteschlangen zu minimieren. Dieser Algorithmus
              kann nicht im LOG-Modus verwendet werden.

  first       Der erste Server mit freien Verbindungsplätzen erhält die
              Verbindung. Die Server werden vom kleinsten zum größten
              numerischen Bezeichner ausgewählt (siehe Serverparameter "id").
              Standardmäßig entspricht dieser der Position des Servers in der
              Gruppe. Sobald ein Server seinen maxconn-Wert erreicht, wird der
              nächste verwendet. Der Algorithmus ist ohne maxconn-Einstellung
              nicht sinnvoll. Er soll stets möglichst wenige Server verwenden,
              damit zusätzliche Server in Zeiten geringer Last ausgeschaltet
              werden können. Der Algorithmus ignoriert das Servergewicht und
              ist für lange Sitzungen wie RDP oder IMAP nützlicher als für
              HTTP, kann aber auch dort hilfreich sein. Für einen effizienten
              Einsatz wird empfohlen, dass eine Cloud-Steuerung die
              Serverauslastung regelmäßig prüft und ungenutzte Server abschaltet.
              Ebenso sollte sie die Backend-Warteschlange regelmäßig prüfen
              und bei wachsender Warteschlange weitere Server einschalten.
              Alternativ kann "http-check send-state" die Server über die
              Last informieren. Dieser Algorithmus kann nicht im LOG-Modus
              verwendet werden.

  hash        Erwartet als Argument einen regulären Sample-Ausdruck. Der
              Ausdruck wird für jede Anfrage ausgewertet und anhand des
              konfigurierten hash-type gehasht. Der Hash wird durch das
              Gesamtgewicht der laufenden Server geteilt, um den Server zu
              bestimmen, der die Anfrage erhält. Dies kann "source", "uri",
              "hdr()", "url_param()" oder "rdp-cookie" ersetzen, um etwa einen
              Konverter zu verwenden, die Auswertung zu verfeinern oder Daten
              aus lokalen Variablen zu extrahieren. Sind die Daten nicht
              verfügbar, wird Round-Robin verwendet. Dieser Algorithmus ist
              standardmäßig statisch: Eine Änderung des Servergewichts im
              laufenden Betrieb hat keine Wirkung. Mit "hash-type" lässt
              sich dies ändern. Der Algorithmus kann nicht für Backends im
              LOG-Modus verwendet werden; dafür ist "log-hash" vorgesehen.

  source      Die Quell-IP-Adresse wird gehasht und durch das Gesamtgewicht
              der laufenden Server geteilt, um den Server zu bestimmen, der
              die Anfrage erhält. Dadurch erreicht dieselbe Client-IP-Adresse
              immer denselben Server, solange kein Server ausfällt oder
              verfügbar wird. Ändert sich das Hash-Ergebnis, weil sich die
              Zahl laufender Server ändert, werden viele Clients einem anderen
              Server zugewiesen. Dieser Algorithmus wird meist im TCP-Modus
              verwendet, in dem kein Cookie eingefügt werden kann. Er kann
              auch im Internet verwendet werden, um Clients, die
              Sitzungscookies ablehnen, nach Möglichkeit an denselben Server
              zu binden. Der Algorithmus ist standardmäßig statisch: Eine
              Änderung des Servergewichts im laufenden Betrieb hat keine
              Wirkung. Mit "hash-type" lässt sich dies ändern. Siehe auch
              die Option "hash" oben. Dieser Algorithmus kann nicht für
              Backends im LOG-Modus verwendet werden.

  uri         Dieser Algorithmus hasht entweder den linken Teil der URI vor
              dem Fragezeichen oder die gesamte URI, wenn der Parameter
              "whole" vorhanden ist. Der Hash-Wert wird durch das
              Gesamtgewicht der laufenden Server geteilt. Das Ergebnis
              bestimmt, welcher Server die Anfrage erhält. Dadurch wird
              dieselbe URI immer demselben Server zugewiesen, solange kein
              Server verfügbar wird oder ausfällt. Dies wird bei Proxy-Caches
              und Virenschutz-Proxys verwendet, um die Cache-Trefferrate zu
              maximieren. Dieser Algorithmus kann nur in einem HTTP-Backend
              verwendet werden. Er ist standardmäßig statisch: Eine Änderung
              des Servergewichts im laufenden Betrieb hat keine Wirkung.
              Mit "hash-type" lässt sich dies ändern.

              Dieser Algorithmus unterstützt die optionalen Parameter "len"
              und "depth", jeweils gefolgt von einer positiven ganzen Zahl.
              Diese Optionen können helfen, wenn die Lastverteilung allein
              anhand des URI-Anfangs erfolgen soll. Der Parameter "len" gibt
              an, wie viele Zeichen am Anfang der URI der Algorithmus für
              die Hash-Berechnung berücksichtigen sollte. "len" auf 1 zu
              setzen, ist selten sinnvoll, da die meisten URIs mit "/"
              beginnen.

              Der Parameter "depth" gibt die maximale Verzeichnistiefe für
              die Hash-Berechnung an. Jeder Schrägstrich in der Anfrage zählt
              als eine Ebene. Sind beide Parameter angegeben, endet die
              Auswertung, sobald einer der Grenzwerte erreicht ist.

              Der Parameter "path-only" gibt an, dass der Hash-Schlüssel
              beim ersten '/' des Pfades beginnt. Damit lässt sich der
              Authority-Teil absoluter URIs ignorieren und sicherstellen,
              dass HTTP/1- und HTTP/2-URIs denselben Hash liefern. Siehe auch
              die Option "hash" oben.

  url_param   Der als Argument angegebene URL-Parameter wird in der
              Abfragezeichenfolge jeder HTTP-GET-Anfrage gesucht.

              Mit dem Modifikator "check_post" wird der Parameter im Inhalt
              einer HTTP-POST-Anfrage gesucht, falls er nicht in der
              Abfragezeichenfolge nach dem Fragezeichen ('?') in der URL
              gefunden wird. Die Analyse des Nachrichtenkörpers beginnt erst,
              wenn entweder die angekündigte Datenmenge empfangen wurde oder
              der Anfragepuffer voll ist. Im unwahrscheinlichen Fall einer
              Chunked-Kodierung wird nur der erste Chunk durchsucht. Durch
              eine Chunk-Grenze getrennte Parameterwerte werden gegebenenfalls
              zufällig verteilt. Dieses Schlüsselwort unterstützte früher
              einen optionalen Parameter <max_wait>, der heute ignoriert wird.

              Folgt auf den gefundenen Parameter ein Gleichheitszeichen ('=')
              mit einem Wert, wird der Wert gehasht und durch das
              Gesamtgewicht der laufenden Server geteilt. Das Ergebnis
              bestimmt, welcher Server die Anfrage erhält.

              Damit lassen sich Benutzerkennungen in Anfragen verfolgen und
              sicherstellen, dass dieselbe Benutzer-ID immer an denselben
              Server gesendet wird, solange kein Server verfügbar wird oder
              ausfällt. Wird kein Wert oder kein Parameter gefunden, wird
              Round-Robin verwendet. Dieser Algorithmus kann nur in einem
              HTTP-Backend verwendet werden. Er ist standardmäßig statisch:
              Eine Änderung des Servergewichts im laufenden Betrieb hat keine
              Wirkung. Mit "hash-type" lässt sich dies ändern. Siehe auch
              die Option "hash" oben.

  hdr(<name>) Der HTTP-Header <name> wird in jeder HTTP-Anfrage gesucht. Wie
              bei der entsprechenden ACL-Funktion 'hdr()' wird beim
              Headernamen in Klammern nicht zwischen Groß- und Kleinschreibung
              unterschieden. Fehlt der Header oder enthält er keinen Wert,
              wird stattdessen der Algorithmus roundrobin verwendet.

              Mit dem optionalen Parameter 'use_domain_only' lässt sich der
              Hash-Algorithmus bei bestimmten Headern wie 'Host' auf den
              Hauptteil der Domain beschränken. Im Host-Wert "haproxy.1wt.eu"
              wird beispielsweise nur "1wt" berücksichtigt.

              Der Algorithmus ist standardmäßig statisch: Eine Änderung des
              Servergewichts im laufenden Betrieb hat keine Wirkung.
              Mit "hash-type" lässt sich dies ändern. Siehe auch die
              Option "hash" oben.

  random
  random(<draws>)
              Als Schlüssel für die konsistente Hash-Funktion wird eine
              Zufallszahl verwendet. Dadurch werden die Servergewichte
              berücksichtigt; dynamische Gewichtsänderungen und neu
              hinzugefügte Server wirken sofort. Zufällige Lastverteilung
              kann bei großen Servergruppen oder häufigem Hinzufügen und
              Entfernen von Servern nützlich sein. Sie kann die Überlastung
              einzelner Server vermeiden, die roundrobin oder leastconn in
              dieser Situation verursachen könnten. Mit hash-balance-factor
              lässt sich die Fairness der Lastverteilung weiter verbessern,
              besonders bei stark schwankenden Antwortzeiten der Server.
              Ist das Argument <draws> vorhanden, muss es eine ganze Zahl
              von mindestens eins sein. Sie gibt die Zahl der Ziehungen an,
              bevor der am wenigsten ausgelastete dieser Server gewählt wird.
              Es wurde nachgewiesen, dass bereits die Auswahl des weniger
              ausgelasteten von zwei Servern die Fairness des Algorithmus
              deutlich verbessert: Der am stärksten ausgelastete Server
              einer Gruppe wird nie ausgewählt, und Verzerrungen durch eine
              ungleichmäßige Verteilung der konsistenten Liste entfallen.
              Höhere Werte N schließen die N-1 am stärksten ausgelasteten
              Server aus, kosten jedoch Leistung. Bei sehr hohen Werten
              nähert sich das Ergebnis dem von leastconn, wird aber viel
              langsamer berechnet. Bei großen Servergruppen mit sehr
              niedriger Last oder perfekter Verteilung führt der Lastvergleich
              zudem häufig zu Gleichständen. Haben alle verglichenen Server
              dieselbe Last, werden deshalb ihre Anfrageraten während der
              letzten Sekunde verglichen. Damit wird die Servernutzung im
              zeitlichen Verlauf ähnlich wie bei roundrobin besser verteilt,
              und Ungleichmäßigkeiten des konsistenten Hashings werden
              ausgeglichen. Der Standardwert ist 2 und liefert im Allgemeinen
              eine sehr gute Verteilung und Leistung. Bei großen Gruppen mit
              geringer Last, also weniger als einigen Anfragen pro Sekunde
              und Server, kann eine Erhöhung auf 3 oder sogar 4 helfen.
              Der Algorithmus ist auch als Power of Two Random Choices
              bekannt und wird hier beschrieben:
              http://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf

              Bei Backends im LOG-Modus wird die Anzahl der Ziehungen
              ignoriert und nur eine Zufallszahl gezogen, da dort kein
              Konzept der Serverlast besteht. Zufällige Protokollverteilung
              kann bei großen Gruppen oder häufigem Hinzufügen und Entfernen
              von Servern aus dem Pool verfügbarer Server nützlich sein.
              Sie kann die Überlastung einzelner Server vermeiden, die
              roundrobin in dieser Situation verursachen könnte.

  rdp-cookie
  rdp-cookie(<name>)
              Das RDP-Cookie <name>, bei fehlender Angabe "mstshash", wird
              für jede eingehende TCP-Anfrage gesucht und gehasht. Wie bei
              der entsprechenden ACL-Funktion 'req.rdp_cookie()' wird bei
              seinem Namen nicht zwischen Groß- und Kleinschreibung
              unterschieden. Dieser Mechanismus ist als eingeschränkte Form
              der Sitzungsbindung nützlich, da derselbe Benutzer oder dieselbe
              Sitzungs-ID stets an denselben Server gesendet werden kann.
              Wird das Cookie nicht gefunden, wird stattdessen der normale
              Algorithmus roundrobin verwendet.

              Damit dies funktioniert, muss das Frontend sicherstellen, dass
              bereits ein RDP-Cookie im Anfragepuffer vorhanden ist. Dazu muss
              eine Regel 'tcp-request content accept' mit einer ACL
              'req.rdp_cookie_cnt' kombiniert werden.

              Der Algorithmus ist standardmäßig statisch: Eine Änderung des
              Servergewichts im laufenden Betrieb hat keine Wirkung.
              Mit "hash-type" lässt sich dies ändern. Siehe auch die
              Option "hash" oben.

  log-hash    Erwartet als Argument eine durch Kommas getrennte Liste von
              Konvertern. Diese werden nacheinander auf die eingehende
              Protokollnachricht angewendet. Das Ergebnis wird in eine
              Zeichenfolge umgewandelt und anschließend anhand des
              konfigurierten hash-type gehasht. Der resultierende Hash wählt
              den Zielserver unter den im Protokoll-Backend deklarierten
              Servern aus. Ziel des Algorithmus ist, mithilfe von
              Zeichenfolgenkonvertern einen Schlüssel aus der fertigen
              Protokollnachricht zu extrahieren und anhand seines Hashes
              denselben Server beizubehalten. Zurzeit werden nur
              "map-based"-Hashes unterstützt. Dieser Algorithmus kann nur
              für Backends im LOG-Modus verwendet werden; für andere ist
              stattdessen "hash" vorgesehen.

  sticky      Versucht, möglichst lange denselben Server zu verwenden. Der
              erste Server in der Liste verfügbarer Server erhält sämtliche
              Protokollnachrichten. Wechselt er in den Zustand DOWN, übernimmt
              der nächste Server in der Liste. Wird ein zuvor als DOWN
              markierter Server wieder UP, wird er am Listenende angefügt.
              Der gebundene Server ändert sich daher erst, wenn er DOWN wird.

<arguments> ist eine optionale Liste von Argumenten, die einige Algorithmen
            benötigen können. Zurzeit unterstützen nur "url_param", "uri"
            und "log-hash" ein optionales Argument.
```

Der Lastverteilungsalgorithmus eines Backends wird auf "random" festgelegt, wenn weder ein anderer Algorithmus noch ein Modus oder eine Option festgelegt wurde. Der Algorithmus darf für jedes Backend nur einmal festgelegt werden.

Bei Authentifizierungsschemata, die dieselbe Verbindung erfordern, wie NTLM, dürfen URI-basierte Algorithmen nicht verwendet werden, da dies dazu führen würde, dass nachfolgende Anfragen an verschiedene Backend-Server weitergeleitet werden, wodurch die ungültigen Annahmen verletzt würden, auf denen NTLM beruht.

TCP/HTTP-Beispiele:

```text
balance roundrobin
balance url_param userid
balance url_param session_id check_post 64
balance hdr(User-Agent)
balance hdr(host)
balance hdr(Host) use_domain_only
balance hash req.cookie(clientid)
balance hash var(req.client_id)
balance hash req.hdr_ip(x-forwarded-for,-1),ipmask(24)
```

LOG-Backend-Beispiele:

```text
global
  log backend@mylog-rrb local0 # send all logs to mylog-rrb backend
  log backend@mylog-hash local0 # send all logs to mylog-hash backend

backend mylog-rrb
  mode log
  balance roundrobin

  server s1 udp@127.0.0.1:514 # will receive 50% of log messages
  server s2 udp@127.0.0.1:514

backend mylog-hash
  mode log

  # extract "METHOD URL PROTO" at the end of the log message,
  # and let haproxy hash it so that log messages generated from
  # similar requests get sent to the same syslog server:
  balance log-hash 'field(-2,\")'

  # server list here
  server s1 127.0.0.1:514
  #...
```

Hinweis: Die folgenden Einschränkungen und Besonderheiten beim Einsatz der "check_post"-Erweiterung mit "url_param" müssen berücksichtigt werden:

    - Alle POST-Anfragen kommen für die Prüfung infrage, da nicht feststellbar ist, ob die Parameter im Textkörper oder in der Entität enthalten sind, die binäre Daten enthalten kann. Daher kann eine andere Methode erforderlich sein, um die Prüfung von POST-Anfragen einzuschränken, die keine URL-Parameter im Textkörper enthalten. (siehe acl http_end)

    - Die Verwendung eines `<max_wait>`-Werts, der größer als die Größe des Anfrage-Puffers ist, ergibt keinen Sinn und ist nutzlos. Die Puffergröße wird beim Kompilieren festgelegt und beträgt standardmäßig 16 kB.

    - Content-Encoding wird nicht unterstützt, die Parametersuche wird wahrscheinlich fehlschlagen; die Lastverteilung fällt auf Round Robin zurück.

    - Expect: 100-continue wird nicht unterstützt, die Lastverteilung fällt auf Round Robin zurück.

    - Transfer-Encoding (RFC7230 3.3.1) wird nur im ersten Chunk unterstützt. Wenn der gesamte Parameterwert nicht im ersten Chunk enthalten ist, ist die Auswahl des Servers undefiniert (genauer gesagt wird sie dadurch bestimmt, wie wenig tatsächlich im ersten Chunk enthalten war).

    - Diese Funktion unterstützt nicht die Erzeugung einer Antwort mit dem Status 100, 411 oder 501.

    - In einigen Fällen kann die Aktivierung von "check_post" einen Versuch auslösen, den gesamten Inhalt eines Nachrichtenkörpers zu durchsuchen. Die Suche endet normalerweise, wenn lineare Leerraumzeichen oder Steuerzeichen gefunden werden, was auf das Ende einer möglichen Liste von URL-Parametern hinweist. Dies ist wahrscheinlich kein Problem bei SGML-artigen Nachrichtenkörpern.

Siehe auch: "dispatch", "cookie", "transparent", "hash-type".

<a id="entry-4-2-be-unpublished"></a>

**`be-unpublished`**

```haproxy
be-unpublished
```

Das Backend im unveröffentlichten Zustand starten.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Dadurch werden alle use_backend- und default_backend-Regeln aus einem anderen Proxy, die auf den aktuellen Proxy verweisen, ignoriert, und die nächsten Regeln zur inhaltsabhängigen Umschaltung werden ausgewertet. Dies kann jedoch über eine "force-be-switch"-Regel umgangen werden.

Dieser Zustand ähnelt dem deaktivierten Zustand, unterscheidet sich jedoch in einigen Punkten. Erstens wird ein unveröffentlichtes Backend weiterhin vollständig initialisiert, einschließlich der Health Checks der Server, die weiterhin aktiv bleiben. Schließlich kann ein Backend mit dem Befehl "publish backend" über die CLI veröffentlicht werden. Siehe das Management-Handbuch.

Siehe auch: "force-be-switch"

<a id="entry-4-2-bind"></a>

**`bind [<address>]:<port_range> [, ...] [param*]`**

```haproxy
bind [<address>]:<port_range> [, ...] [param*]
bind /<path> [, ...] [param*]
```

Eine oder mehrere Adressen und/oder Ports festlegen, an denen ein Frontend lauscht.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<address>     ist optional und kann ein Hostname, eine IPv4-Adresse, eine
              IPv6-Adresse oder '*' sein. Sie bezeichnet die Adresse, an der
              das Frontend lauscht. Ohne Angabe werden alle IPv4-Adressen des
              Systems verwendet. Gleiches gilt für '*' oder die besondere
              Systemadresse "0.0.0.0". Die IPv6-Entsprechung lautet '::'. Für
              UDP sind beim Binden an mehrere Adressen bestimmte Funktionen
              des Betriebssystems (OS) erforderlich, damit Antworten die richtige
              Netzwerkschnittstelle und Quelladresse verwenden. QUIC-Listener
              daher nur auf ausreichend modernen Systemen an mehrere
              Adressen binden.

              Optional kann der Adresse ein Adressfamilienpräfix vorangestellt
              werden, um die Familie unabhängig vom Adressformat zu erzwingen.
              Damit lässt sich beispielsweise der Pfad zu einem Unix-Socket
              ohne Schrägstrich ('/') angeben. Zurzeit werden diese Präfixe
              unterstützt:
                - 'ipv4@'  -> Adresse ist immer IPv4
                - 'ipv6@'  -> Adresse ist immer IPv6
                - 'udp@'   -> Adresse wird als IPv4 oder IPv6 aufgelöst und
                  das Protokoll UDP verwendet. Diese Listener werden derzeit
                  nur in log-forward-Abschnitten unterstützt.
                - 'udp4@'  -> Adresse ist immer IPv4 und das Protokoll UDP
                  wird verwendet. Diese Listener werden derzeit nur in
                  log-forward-Abschnitten unterstützt.
                - 'udp6@'  -> Adresse ist immer IPv6 und das Protokoll UDP
                  wird verwendet. Diese Listener werden derzeit nur in
                  log-forward-Abschnitten unterstützt.
                - 'unix@'  -> Adresse ist ein Pfad zu einem lokalen Unix-Socket
                - 'abns@'  -> Adresse liegt im abstrakten Namensraum (nur Linux).
                - 'abnsz@'  -> Adresse liegt im abstrakten Namensraum (nur Linux),
                   wird jedoch ausdrücklich mit einem Nullzeichen beendet.
                   sun_path wird also nicht mit \0 aufgefüllt. Dies ist für
                   die Verbindung mit Programmen nützlich, die die von haproxy
                   standardmäßig verwendete abns-Namenslogik nicht umsetzen.
                - 'fd@<n>' -> vom übergeordneten Prozess geerbten Dateideskriptor
                  <n> verwenden. Der fd muss gebunden sein und kann bereits
                  lauschen, muss dies aber nicht.
                - 'sockpair@<n>'-> wie fd@, jedoch muss der fd eines verbundenen
                  Unix-Sockets oder eines Socketpaars verwendet werden. bind
                  wartet auf einen über den Unix-Socket empfangenen FD und
                  verwendet ihn wie den FD eines accept(). Sollte mit Vorsicht
                  verwendet werden.
                - 'quic4@' -> Adresse wird als IPv4 aufgelöst und das Protokoll
                  UDP verwendet. Für optimale Leistung bei hohem Datenverkehr
                  sollte "tune.quic.fe.sock-per-conn
                  default-on" beibehalten werden. Andernfalls werden
                  QUIC-Verbindungen über den Listener-Socket multiplexiert.
                  Alternativ können QUIC-Listener-Instanzen auf mehrere
                  Threads verteilt werden, beispielsweise mit "shards", um
                  zumindest die Konkurrenz zwischen Threads zu verringern.
                - 'quic6@' -> Adresse wird als IPv6 aufgelöst und das Protokoll
                  UDP verwendet. Der Leistungshinweis zu QUIC über IPv4 gilt
                  auch hier.
                - 'rhttp@' [ EXPERIMENTAL ] -> für umgekehrtes HTTP verwendet.
                  Die Adresse muss einen Server im Format
                  '<backend>/<server>' angeben. Über diesen Server werden
                  Verbindungen zu einer entfernten Adresse aufgebaut. Der
                  Listener versucht, "nbconn" Verbindungen aufrechtzuerhalten.
                  Diese Funktion ist experimentell und erfordert eine Zeile
                  mit "expose-experimental-directives" vor dieser bind-Zeile.

              Im Adressparameter können Umgebungsvariablen verwendet werden;
              siehe Abschnitt 2.3 zu Umgebungsvariablen.

<port_range>  ist entweder ein einzelner TCP-Port oder ein Portbereich, an dem
              der Proxy Verbindungen für die oben angegebene IP-Adresse
              annimmt. Für TCP-Listener ist der Port zwingend erforderlich.
              Bei einer IPv6-Adresse ist der Port immer die Zahl nach dem
              letzten Doppelpunkt (':'). Ein Bereich kann folgendermaßen
              angegeben werden:
               - als numerischer Port (z. B. '80')
               - als durch Bindestrich getrennter Portbereich mit ausdrücklich
                 angegebenen unteren und oberen Grenzen (z. B. '2000-2100'),
                 die beide zum Bereich gehören.

              Bei Portbereichen ist besondere Vorsicht erforderlich: Jedes
              Paar <address:port> belegt einen Socket, also einen
              Dateideskriptor. Ein einfacher Bereich kann daher viele
              Deskriptoren verbrauchen und alle verfügbaren Sockets aufbrauchen.
              Zudem darf jedes Paar <address:port> unter allen Instanzen auf
              demselben System nur einmal verwendet werden. Das Binden an
              Ports unter 1024 erfordert zum Programmstart im Allgemeinen
              besondere Berechtigungen, die vom Parameter 'uid' unabhängig sind.

<path>        ist ein UNIX-Socket-Pfad, der mit einem Schrägstrich ('/') beginnt.
              Dies ist eine Alternative zum TCP-Listener-Port. HAProxy nimmt
              dann UNIX-Verbindungen an dem Socket an diesem Pfad entgegen.
              Der Pfad muss mit einem Schrägstrich beginnen und ist
              standardmäßig absolut. Er kann relativ zu dem Präfix sein,
              das mit "unix-bind" im global-Abschnitt festgelegt ist. Die
              Gesamtlänge von Präfix und Socket-Pfad darf die Systemgrenzen
              für UNIX-Sockets nicht überschreiten; diese liegen häufig bei
              107 Zeichen.

<param*>      ist eine Liste von Parametern, die für alle auf derselben Zeile
              deklarierten Sockets gelten. Diese zahlreichen Parameter hängen
              vom Betriebssystem (OS) und den Build-Optionen ab und werden in einem
              eigenen Abschnitt beschrieben. Weitere Einzelheiten stehen in
              Abschnitt 5.
```

Es ist möglich, eine durch Kommas getrennte Liste von address:port-Kombinationen anzugeben. Das Frontend lauscht dann an allen diesen Adressen. Es gibt keine feste Grenze für die Anzahl der Adressen und Ports, an denen ein Frontend lauschen kann, ebenso wenig wie für die Anzahl der "bind"-Anweisungen in einem Frontend.

Beispiel:

```text
listen http_proxy
    bind :80,:443
    bind 10.0.0.1:10080,10.0.0.1:10443
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy

listen http_https_proxy
    bind :80
    bind :443 ssl crt /etc/haproxy/site.pem

listen http_https_proxy_explicit
    bind ipv6@:80
    bind ipv4@public_ssl:443 ssl crt /etc/haproxy/site.pem
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy

listen external_bind_app1
    bind "fd@${FD_APP1}"

listen h3_quic_proxy
    bind quic4@10.0.0.1:8888 ssl crt /etc/mycrt
```

Hinweis: Bei Sockets im abstrakten Namensraum von Linux verwenden HAProxy-Sockets der Familie "abns" die gesamte Länge von sun_path als Adresslänge. Andere Programme wie socat verwenden standardmäßig nur die Länge der Zeichenkette. Übergeben Sie der Definition eines abstrakten Sockets in socat die Option ",unix-tightsocklen=0", um Kompatibilität mit HAProxy zu erreichen, oder verwenden Sie stattdessen die HAProxy-Socket-Familie "abnsz".

Siehe auch: "source", "option forwardfor", "unix-bind" und die PROXY-Protokoll-Dokumentation sowie [Abschnitt 5](/de/haproxy/bind-and-server-options/) zu Bind-Optionen.

<a id="entry-4-2-capture-cookie"></a>

**`capture cookie <name> len <length>`**

```haproxy
capture cookie <name> len <length>
```

Ein Cookie in der Anfrage und in der Antwort erfassen und protokollieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<name>    ist der Anfang des Namens des zu erfassenden Cookies. Für einen
          exakten Namensvergleich genügt ein angehängtes Gleichheitszeichen
          ('='). Der vollständige Name erscheint im Protokoll. Dies ist bei
          Anwendungsservern nützlich, die sowohl Cookie-Name als auch -Wert
          anpassen (z. B. ASPSESSIONXXX).

<length>  ist die maximale Zahl protokollierter Zeichen, einschließlich
          Cookie-Name, Gleichheitszeichen und Wert im üblichen Format
          "name=value". Überschreitet die Zeichenfolge <length>, wird sie
          rechts abgeschnitten.
```

Es wird nur das erste Cookie erfasst. Sowohl die "cookie"-Anfrage-Header als auch die "set-cookie"-Antwort-Header werden überwacht. Dies ist besonders nützlich, um Anwendungsfehler zu erkennen, die zu Sitzungsüberschneidungen oder -diebstahl zwischen Benutzern führen, da die Cookies eines Benutzers normalerweise nur auf der Anmeldeseite geändert werden können.

Wenn das Cookie vom Client nicht übermittelt wurde, wird die zugehörige Protokollspalte mit "-" angezeigt. Wenn eine Anfrage keine Zuweisung eines Cookies durch den Server verursacht, wird in der Antwortspalte "-" angezeigt.

Die Erfassung erfolgt nur im Frontend, da sichergestellt werden muss, dass das Protokollformat für ein bestimmtes Frontend nicht je nach Backend wechselt. Dies könnte sich in Zukunft ändern. Es kann nur eine "capture cookie"-Anweisung pro Frontend geben. Die maximale Erfassungslänge wird durch die globale Einstellung "tune.http.cookielen" festgelegt und beträgt standardmäßig 63 Zeichen. Es ist nicht möglich, eine Erfassung in einem "defaults"-Abschnitt anzugeben.

Beispiel:

```text
capture cookie ASPSESSION len 32
```

Siehe auch: "capture request header", "capture response header" sowie [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-capture-request-header"></a>

**`capture request header <name> len <length>`**

```haproxy
capture request header <name> len <length>
```

Das letzte Vorkommen des angegebenen Anfrageheaders erfassen und protokollieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<name>    ist der Name des zu erfassenden Headers. Bei Headernamen wird
          nicht zwischen Groß- und Kleinschreibung unterschieden. Üblicherweise
          werden sie jedoch wie in den Anfragen geschrieben, mit einem
          Großbuchstaben am Anfang jedes Wortes. Der Headername erscheint
          nicht im Protokoll, sondern nur sein Wert; die Position im Protokoll
          bleibt jedoch erhalten.

<length>  ist die maximale Zahl der Zeichen, die aus dem Wert extrahiert und
          protokolliert werden. Überschreitet die Zeichenfolge <length>, wird
          sie rechts abgeschnitten.
```

Der vollständige Wert des letzten Vorkommens des Headers wird erfasst. Der Wert wird in geschweiften Klammern ('{}') in das Protokoll aufgenommen. Werden mehrere Header erfasst, werden sie durch einen senkrechten Strich ('\|') getrennt und in derselben Reihenfolge angezeigt, in der sie in der Konfiguration deklariert wurden. Nicht vorhandene Header werden als leere Zeichenkette protokolliert. Häufig erfasste Anfrageheader sind das Feld "Host" in Umgebungen mit virtuellem Hosting, "Content-length" bei Unterstützung von Uploads, "User-agent" zur schnellen Unterscheidung echter Benutzer von Robotern und "X-Forwarded-For" in Umgebungen mit vorgeschalteten Proxys, um den Ursprung der Anfrage festzustellen.

Beim Erfassen von Headern wie "User-agent" können auch Leerzeichen protokolliert werden, was die Protokollanalyse erschwert. Wählen Sie daher die protokollierten Werte sorgfältig aus, wenn Ihr Protokollparser die geschweiften Klammern nicht zuverlässig auswerten kann.

Weder die Anzahl noch die Länge der erfassten Anfrageheader ist begrenzt. Es ist jedoch sinnvoll, beide gering zu halten, um den Speicherbedarf pro Stream zu begrenzen. Damit das Protokollformat für ein bestimmtes Frontend einheitlich bleibt, kann die Headererfassung nur in einem Frontend deklariert werden. In einem "defaults"-Abschnitt kann keine Erfassung angegeben werden.

Beispiel:

```text
capture request header Host len 15
capture request header X-Forwarded-For len 15
capture request header Referer len 15
```

Siehe auch: "capture cookie", "capture response header" sowie [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-capture-response-header"></a>

**`capture response header <name> len <length>`**

```haproxy
capture response header <name> len <length>
```

Das letzte Vorkommen des angegebenen Antwortheaders erfassen und protokollieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<name>    ist der Name des zu erfassenden Headers. Bei Headernamen wird
          nicht zwischen Groß- und Kleinschreibung unterschieden. Üblicherweise
          werden sie jedoch wie in der Antwort geschrieben, mit einem
          Großbuchstaben am Anfang jedes Wortes. Der Headername erscheint
          nicht im Protokoll, sondern nur sein Wert; die Position im Protokoll
          bleibt jedoch erhalten.

<length>  ist die maximale Zahl der Zeichen, die aus dem Wert extrahiert und
          protokolliert werden. Überschreitet die Zeichenfolge <length>, wird
          sie rechts abgeschnitten.
```

Der vollständige Wert des letzten Vorkommens des Headers wird erfasst. Das Ergebnis wird nach den erfassten Anfrageheadern in geschweiften Klammern ('{}') in das Protokoll aufgenommen. Werden mehrere Header erfasst, werden sie durch einen senkrechten Strich ('\|') getrennt und in derselben Reihenfolge angezeigt, in der sie in der Konfiguration deklariert wurden. Nicht vorhandene Header werden als leere Zeichenkette protokolliert. Häufig erfasste Antwortheader sind "Content-length", der die erwartete Anzahl zurückgegebener Bytes angibt, und "Location", um Weiterleitungen nachzuverfolgen.

Weder die Anzahl noch die Länge der erfassten Antwortheader ist begrenzt. Es ist jedoch sinnvoll, beide gering zu halten, um den Speicherbedarf pro Stream zu begrenzen. Damit das Protokollformat für ein bestimmtes Frontend einheitlich bleibt, kann die Headererfassung nur in einem Frontend deklariert werden. In einem "defaults"-Abschnitt kann keine Erfassung angegeben werden.

Beispiel:

```text
capture response header Content-length len 9
capture response header Location len 15
```

Siehe auch: "capture cookie", "capture request header" sowie [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-clitcpka-cnt"></a>

**`clitcpka-cnt <count>`**

```haproxy
clitcpka-cnt <count>
```

Die maximale Anzahl von Keepalive-Prüfungen festlegen, die TCP auf der Clientseite senden soll, bevor es die Verbindung trennt.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<count>   ist die maximale Zahl der Keepalive-Prüfungen.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPCNT. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_probes) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option clitcpka", "clitcpka-idle", "clitcpka-intvl".

<a id="entry-4-2-clitcpka-idle"></a>

**`clitcpka-idle <timeout>`**

```haproxy
clitcpka-idle <timeout>
```

Die Zeit festlegen, die eine Verbindung inaktiv bleiben muss, bevor TCP Keepalive-Prüfungen sendet, sofern das Senden von TCP-Keepalive-Paketen auf der Clientseite aktiviert ist.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<timeout> ist die Zeit, die eine Verbindung inaktiv bleiben muss, bevor
          TCP Keepalive-Prüfungen sendet. Standardmäßig wird sie in Sekunden
          angegeben. Jede andere Einheit ist möglich, wenn sie wie am Anfang
          dieses Dokuments erläutert an die Zahl angehängt wird.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPIDLE. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_time) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option clitcpka", "clitcpka-cnt", "clitcpka-intvl".

<a id="entry-4-2-clitcpka-intvl"></a>

**`clitcpka-intvl <timeout>`**

```haproxy
clitcpka-intvl <timeout>
```

Den zeitlichen Abstand zwischen einzelnen Keepalive-Prüfungen auf der Clientseite festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<timeout> ist die Zeit zwischen einzelnen Keepalive-Prüfungen.
          Standardmäßig wird sie in Sekunden angegeben. Jede andere Einheit
          ist möglich, wenn sie wie am Anfang dieses Dokuments erläutert
          an die Zahl angehängt wird.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPINTVL. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_intvl) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option clitcpka", "clitcpka-cnt", "clitcpka-idle".

<a id="entry-4-2-compression-algo"></a>

**`compression algo <algorithm> ...`**

```haproxy
compression algo <algorithm> ...
compression algo-req <algorithm>
compression algo-res <algorithm>
compression type <mime type> ...
```

HTTP-Komprimierung aktivieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
algo     gefolgt von der Liste unterstützter Kompressionsalgorithmen für
         Antworten (veraltetes Schlüsselwort).
algo-req gefolgt vom Kompressionsalgorithmus für Anfragen (es wird nur einer
  angegeben).
algo-res gefolgt von der Liste unterstützter Kompressionsalgorithmen für
         Antworten.
type     gefolgt von der Liste der MIME-Typen, die in Antworten komprimiert
         werden (veraltetes Schlüsselwort).
type-req gefolgt von der Liste der MIME-Typen, die in Anfragen komprimiert
         werden.
type-res gefolgt von der Liste der MIME-Typen, die in Antworten komprimiert
         werden.
```

Derzeit werden folgende Algorithmen unterstützt:

```text
identity     dient hauptsächlich der Fehlersuche und war bei der Entwicklung
             der Kompressionsfunktion nützlich. Identity verändert die Daten
             nicht.

gzip         verwendet gzip-Kompression. Diese Einstellung ist nur verfügbar,
             wenn Unterstützung für zlib oder libslz einkompiliert wurde.

deflate      wie "gzip", jedoch mit dem deflate-Algorithmus und dem zlib-Format.
             Die Unterstützung dieses Algorithmus ist bei vielen Browsern
             unklar; neuere Browser unterstützen ihn überhaupt nicht. Von
             seiner Verwendung außerhalb von Experimenten wird dringend
             abgeraten. Diese Einstellung ist nur verfügbar, wenn Unterstützung
             für zlib oder libslz einkompiliert wurde.

raw-deflate  wie "deflate" ohne die zlib-Hülle; als Alternative verwendet,
             wenn der Browser "deflate" anfordert. Alle verbreiteten Browser
             verstehen dieses Format. Trotz des Verstoßes gegen die Standards
             funktioniert es bekanntermaßen besser als "deflate", zumindest
             in MSIE und einigen Safari-Versionen. Nicht zusammen mit
             "deflate" verwenden, sondern entweder das eine oder das andere,
             da beide auf dasselbe Accept-Encoding-Token reagieren. Diese
             Einstellung ist nur verfügbar, wenn Unterstützung für zlib oder
             libslz einkompiliert wurde.
```

Die Komprimierung wird abhängig vom Anfrageheader Accept-Encoding aktiviert. Bei identity wird dieser Header nicht berücksichtigt. Unterstützen die Backend-Server HTTP-Komprimierung, bleiben diese Direktiven wirkungslos: HAProxy erkennt die komprimierte Antwort und komprimiert sie nicht erneut. Unterstützen die Backend-Server keine HTTP-Komprimierung und enthält die Anfrage einen Accept-Encoding-Header, komprimiert HAProxy die zugehörige Antwort.

Die Komprimierung wird deaktiviert, wenn: \* die Anfrage im Header "Accept-Encoding" keinen unterstützten Komprimierungsalgorithmus angibt \* die Antwort nicht HTTP/1.1 oder höher verwendet \* der HTTP-Statuscode keiner der Werte 200, 201, 202 oder 203 ist \* die Antwort weder einen Header "Content-Length" noch einen Header "Transfer-Encoding" mit dem letzten Wert "chunked" enthält \* die Antwort einen Header "Content-Type" enthält, dessen erster Wert mit "multipart" beginnt \* die Antwort im Header "Cache-control" den Wert "no-transform" enthält \* User-Agent auf "Mozilla/4" passt, sofern es sich nicht um MSIE 6 mit XP SP2 oder MSIE 7 und neuer handelt \* die Antwort einen Header "Content-Encoding" enthält, der anzeigt, dass die Antwort bereits komprimiert ist (siehe compression offload) \* die Antwort einen ungültigen Header "ETag" oder mehrere ETag-Header enthält \* die Nutzdatengröße unter der Mindestgröße liegt (siehe compression minsize-res)

Hinweis: Die Komprimierung gibt keinen Warning-Header aus.

Beispiele:

```text
compression algo gzip
compression type text/html text/plain
```

Siehe auch: "compression offload", "compression direction", "compression minsize-req" und "compression
minsize-res"

<a id="entry-4-2-compression-minsize-req"></a>

**`compression minsize-req <size>`**

```haproxy
compression minsize-req <size>
compression minsize-res <size>
```

Die Mindestgröße der Nutzdaten in Bytes festlegen, ab der die Komprimierung angewendet wird.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Nutzdaten unterhalb dieser Größe werden nicht komprimiert. Dadurch entfällt unnötiger CPU-Aufwand für Daten, die von der Komprimierung nicht wesentlich profitieren würden. "minsize-req" gilt für Anfragen und "minsize-res" für Antworten. Der Standardwert ist 0.

<a id="entry-4-2-compression-offload"></a>

**`compression offload`**

```haproxy
compression offload
```

HAProxy ausschließlich als Komprimierungsinstanz einsetzen.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Die Einstellung "offload" bewirkt, dass HAProxy den Accept-Encoding-Header entfernt, um zu verhindern, dass Backend-Server Antworten komprimieren. Es wird dringend empfohlen, dies nicht zu tun, da sonst die gesamte Komprimierungsarbeit an der einzigen Stelle durchgeführt wird, an der HAProxy installiert ist. In bestimmten Bereitstellungsszenarien kann HAProxy jedoch vor einem fehlerhaften Gateway installiert sein, dessen fehlerhafte HTTP-Komprimierung nicht abgeschaltet werden kann. In diesem Fall kann HAProxy verwendet werden, um zu verhindern, dass das Gateway ungültige Nutzdaten ausgibt. In diesem Fall funktioniert das einfache Entfernen des Headers in der Konfiguration nicht, da es vor der Analyse des Headers angewendet wird und dadurch HAProxy am Komprimieren hindert. In solchen Szenarien sollte stattdessen die Einstellung "offload" verwendet werden.

Wird diese Einstellung in einem defaults-Abschnitt verwendet, wird eine Warnung ausgegeben und die Option ignoriert.

Siehe auch: "compression type", "compression algo", "compression direction"

<a id="entry-4-2-compression-direction"></a>

**`compression direction <direction> (deprecated)`**

```haproxy
compression direction <direction> (deprecated)
```

Ermöglicht es HAProxy, sowohl Anfragen als auch Antworten zu komprimieren. Gültige Werte sind "request", um nur Anfragen zu komprimieren, "response", um nur Antworten zu komprimieren, oder "both", wenn beide komprimiert werden sollen. Der Standardwert ist "response".

Diese Anweisung ist nur relevant, wenn die veraltete "filter compression" aktiviert wurde. Bei expliziter Verwendung der Filter comp-req und comp-res ist die Komprimierungsrichtung redundant.

Kann in folgenden Kontexten verwendet werden: http

Siehe auch: "compression type", "compression algo", "compression offload"

<a id="entry-4-2-cookie"></a>

**`cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]`**

```haproxy
cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]
              [ postonly ] [ preserve ] [ httponly ] [ secure ]
              [ domain <domain> ]* [ maxidle <idle> ] [ maxlife <life> ]
              [ dynamic ] [ attr <value> ]*
```

Cookiebasierte Sitzungsbindung in einem Backend aktivieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<name>    ist der Name des Cookies, das für die Sitzungsbindung überwacht,
          geändert oder eingefügt wird. Dieses Cookie wird dem Client in
          einem "Set-Cookie"-Header der Antwort gesendet und vom Client in
          allen Anfragen in einem "Cookie"-Header zurückgegeben. Der Name
          sollte besonders sorgfältig gewählt werden, damit er mit keinem
          möglichen Anwendungscookie kollidiert. Werden dieselben Backends
          möglicherweise von denselben Clients verwendet, etwa über HTTP/HTTPS,
          sollten außerdem für alle Backends unterschiedliche Cookie-Namen
          verwendet werden, wenn keine backendübergreifende Sitzungsbindung
          gewünscht ist.

rewrite   Dieses Schlüsselwort gibt an, dass der Server das Cookie bereitstellt
          und HAProxy dessen Wert ändern muss, um die Serverkennung darin
          einzutragen. Dieser Modus ist praktisch, wenn die Anwendung komplexe
          Kombinationen von "Set-cookie"- und "Cache-control"-Headern verwaltet.
          Sie kann dann entscheiden, ob ein Cookie zur Sitzungsbindung
          ausgegeben werden soll. Da alle Antworten überwacht werden sollten,
          funktioniert dieser Modus nicht im HTTP-Tunnelmodus. Sofern das
          Anwendungsverhalten nicht sehr komplex und/oder fehlerhaft ist,
          wird davon abgeraten, neue Installationen mit diesem Modus zu
          beginnen. Das Schlüsselwort ist mit "insert" und "prefix"
          unvereinbar.

insert    Dieses Schlüsselwort gibt an, dass HAProxy das Cookie zur
          Sitzungsbindung in Serverantworten einfügen muss, wenn der Client

          noch kein Cookie besitzt, das ihm den Zugriff auf diesen Server
          ermöglicht hätte. Ohne die Option "preserve" wird ein vom Server
          ausgegebenes Cookie desselben Namens vor der Verarbeitung entfernt.
          Daher lässt sich dieser Modus zur Umstellung bestehender
          Konfigurationen im Modus "rewrite" verwenden. Das Cookie ist nur
          ein Sitzungscookie und wird nicht auf dem Datenträger des Clients
          gespeichert. Standardmäßig sieht der Server die vom Client gesendeten
          Cookies, sofern nicht die Option "indirect" hinzugefügt wird.
          Wegen möglicher Cache-Effekte ist es im Allgemeinen sinnvoll, die
          Schlüsselwörter "nocache" oder "postonly" hinzuzufügen (siehe unten).
          Das Schlüsselwort "insert" ist mit "rewrite" und "prefix"
          unvereinbar.

prefix    Dieses Schlüsselwort gibt an, dass ein vorhandenes Cookie ergänzt
          wird, statt ein eigenes Cookie zur Sitzungsbindung zu verwenden.
          Dies kann in bestimmten Umgebungen erforderlich sein, wenn der
          Client nur ein einziges Cookie unterstützt und die Anwendung dieses
          bereits benötigt. Setzt der Server in diesem Fall ein Cookie namens
          <name>, werden ihm die Serverkennung und ein Trennzeichen vorangestellt.
          Dieses Präfix wird aus allen Clientanfragen entfernt, sodass der
          Server sein ursprüngliches Cookie vorfindet. Da alle Anfragen und
          Antworten verändert werden können, funktioniert dieser Modus nicht
          im Tunnelmodus. Das Schlüsselwort "prefix" ist mit "rewrite" und
          "insert" unvereinbar. Hinweis: Von der Kombination aus "indirect"
          und "prefix" wird dringend abgeraten, da Cookie-Aktualisierungen
          des Servers andernfalls nicht an Clients gesendet würden.

indirect  Mit dieser Option wird einem Client kein Cookie gesendet, wenn er
          bereits ein gültiges Cookie für den Server besitzt, der die Anfrage
          verarbeitet hat. Setzt der Server selbst ein solches Cookie, wird
          es entfernt, sofern nicht zusätzlich "preserve" gesetzt ist. Im
          Modus "insert" werden außerdem Cookies aus den an den Server
          übertragenen Anfragen entfernt. Für die Anwendung ist der Mechanismus
          zur Sitzungsbindung damit vollständig transparent. Hinweis: Von der
          Kombination aus "indirect" und "prefix" wird dringend abgeraten,
          da Cookie-Aktualisierungen des Servers andernfalls nicht an Clients
          gesendet würden.

nocache   Diese Option wird zusammen mit dem Modus insert empfohlen, wenn
          zwischen Client und HAProxy ein Cache liegt. Sie sorgt dafür, dass
          eine sonst cachebare Antwort als nicht cachebar markiert wird, wenn
          ein Cookie eingefügt werden muss. Dies ist wichtig: Werden etwa
          alle Cookies zur Sitzungsbindung auf einer cachebaren Startseite
          gesetzt, laden anschließend alle Kunden die Seite aus einem
          vorgeschalteten Cache. Alle hätten dann dasselbe Cookie zur
          Sitzungsbindung, sodass ein Server deutlich mehr Datenverkehr
          erhielte als die anderen. Siehe auch "insert" und "postonly".

postonly  Diese Option beschränkt das Einfügen von Cookies auf Antworten auf
          POST-Anfragen. Sie ist eine Alternative zu "nocache": Da
          POST-Antworten nicht cachebar sind, wird das Cookie zur
          Sitzungsbindung niemals im Cache gespeichert. Die meisten Websites
          benötigen vor der ersten POST-Anfrage, meist einer Anmeldung, keine
          Sitzungsbindung. Daher optimiert diese Methode das Caching sehr
          effizient, ohne ein Cookie zur Sitzungsbindung im Cache zu riskieren.
          Siehe auch "insert" und "nocache".

preserve  Diese Option kann nur mit "insert" und/oder "indirect" verwendet
          werden. Sie erlaubt dem Server, das Cookie zur Sitzungsbindung
          selbst auszugeben. Wird in diesem Fall ein Cookie in der Antwort
          gefunden, lässt HAProxy es unverändert. Damit lässt sich die
          Sitzungsbindung beispielsweise nach einer Abmeldeanfrage beenden.
          Der Server muss dazu lediglich ein Cookie mit einem ungültigen Wert,
          etwa einem leeren Wert, oder mit einem Datum in der Vergangenheit
          ausgeben. Zusammen mit der Prüfoption "disable-on-404" ermöglicht
          dieser Mechanismus ein vollständig geordnetes Herunterfahren, da
          Benutzer den Server nach der Abmeldung endgültig verlassen.

httponly  Diese Option weist HAProxy an, beim Einfügen eines Cookies das
          Cookie-Attribut "HttpOnly" hinzuzufügen. Dadurch gibt ein User-Agent
          das Cookie nicht an Komponenten außerhalb von HTTP weiter. Weitere
          Informationen zu diesem Attribut enthält RFC6265.

secure    Diese Option weist HAProxy an, beim Einfügen eines Cookies das
          Cookie-Attribut "Secure" hinzuzufügen. Dadurch sendet ein User-Agent
          dieses Cookie nie über ungesicherte Kanäle. Ein Cookie mit diesem
          Attribut wird somit ausschließlich über SSL/TLS-Verbindungen
          übermittelt. Weitere Informationen zu diesem Attribut enthält RFC6265.

domain    Mit dieser Option wird die Domain angegeben, für die ein Cookie
          eingefügt wird. Sie erfordert genau einen Parameter: einen gültigen
          Domainnamen. Beginnt die Domain mit einem Punkt, darf der Browser
          das Cookie für jeden Host verwenden, dessen Name so endet. Durch
          mehrfache Angabe der Option lassen sich auch mehrere Domainnamen
          angeben. Einige Browser erlauben nur wenige Domains; dabei ist
          also Vorsicht geboten. Zur Orientierung: 10 Domains funktionieren
          bei MSIE 6 und Firefox 2 wie erwartet.

maxidle   Mit dieser Option werden eingefügte Cookies nach einer gewissen
          Inaktivitätszeit ignoriert. Sie funktioniert nur für Cookies im
          Modus insert. Beim Senden eines Cookies an den Client wird auch
          sein Ausgabedatum mitgesendet. Wird das Cookie später erneut
          vorgelegt und liegt das Datum länger zurück als die im Parameter
          angegebene Zeit in Sekunden, wird es ignoriert. Andernfalls wird
          es bei Bedarf beim Senden der Antwort an den Client aktualisiert.
          Dies verhindert insbesondere, dass Benutzer, die ihren Browser nie
          schließen, zu lange an denselben Server gebunden bleiben, etwa
          nach einer Änderung der Gruppengröße. Ist diese Option gesetzt
          und enthält ein Cookie kein Datum, wird es immer akzeptiert, aber
          in der Antwort aktualisiert. So behalten Administratoren Zugriff
          auf ihre Websites. Cookies mit einem Datum mehr als 24 Stunden
          in der Zukunft werden ignoriert. Dadurch können Administratoren
          Zeitzonenprobleme beheben, ohne Benutzer von der Website auszuschließen.

maxlife   Mit dieser Option werden eingefügte Cookies nach einer gewissen
          Lebensdauer ignoriert, unabhängig davon, ob sie verwendet werden.
          Sie funktioniert nur für Cookies im Modus insert. Beim ersten
          Senden eines Cookies an den Client wird auch sein Ausgabedatum
          mitgesendet. Wird das Cookie später erneut vorgelegt und liegt
          das Datum länger zurück als die im Parameter angegebene Zeit in
          Sekunden, wird es ignoriert. Enthält das Cookie in der Anfrage
          kein Datum, wird es akzeptiert und mit einem Datum versehen.
          Cookies mit einem Datum mehr als 24 Stunden in der Zukunft werden
          ignoriert. Dadurch können Administratoren Zeitzonenprobleme beheben,
          ohne Benutzer von der Website auszuschließen. Anders als bei maxidle
          wird dieser Wert nicht aktualisiert; nur das Datum des ersten
          Besuchs zählt. maxidle und maxlife können gleichzeitig verwendet
          werden. Dies verhindert insbesondere, dass Benutzer, die ihren
          Browser nie schließen, zu lange an denselben Server gebunden bleiben,
          etwa nach einer Änderung der Gruppengröße. Diese Methode greift
          stärker als maxidle, da sie nach einer absoluten Zeitspanne eine
          Neuzuweisung erzwingt.

dynamic   Aktiviert dynamische Cookies. Für jeden Server wird anhand seiner
          IP-Adresse und seines Ports sowie eines geheimen Schlüssels
          dynamisch ein Sitzungscookie erzeugt. Der Schlüssel wird mit der
          Backend-Direktive "dynamic-cookie-key" angegeben.
          Bei jeder Änderung der IP-Adresse wird das Cookie neu erzeugt;
          die Erzeugung erfolgt nur für IPv4/IPv6.

attr      Diese Option weist HAProxy an, beim Einfügen eines Cookies ein
          zusätzliches Attribut hinzuzufügen. Der Attributwert kann beliebige
          Zeichen außer Steuerzeichen oder ";" enthalten. Diese Option kann
          mehrfach angegeben werden.
```

In einem HTTP-Backend kann nur ein einziges Cookie zur Sitzungsbindung vorhanden sein, das in einem defaults-Abschnitt deklariert werden kann. Der Wert des Cookies entspricht dem Wert, der nach dem Schlüsselwort "cookie" in einer "server"-Anweisung angegeben ist. Wenn für einen bestimmten Server kein Cookie deklariert ist, wird kein Cookie gesetzt.

Beispiele:

```text
cookie JSESSIONID prefix
cookie SRV insert indirect nocache
cookie SRV insert postonly indirect
cookie SRV insert indirect nocache maxidle 30m maxlife 8h
```

Siehe auch: "balance source", "capture cookie", "server" und "ignore-persist"

<a id="entry-4-2-declare-capture"></a>

**`declare capture [ request | response ] len <length>`**

```haproxy
declare capture [ request | response ] len <length>
```

Einen Erfassungsplatz deklarieren.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<length> ist die zulässige Länge der Erfassung.
```

Diese Deklaration ist nur im Frontend- oder listen-Abschnitt verfügbar, der reservierte Platz kann jedoch in Backends verwendet werden. Das Schlüsselwort "request" reserviert einen Erfassungsplatz für die Anfrage, "response" reserviert einen Erfassungsplatz für die Antwort.

Siehe auch: "capture-req", "capture-res" (Sample-Konverter), "capture.req.hdr", "capture.res.hdr" (Sample-Abrufe), "http-request capture" und "http-response capture"

<a id="entry-4-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Die Standardoptionen für einen Server in einem Backend ändern.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<param*>  ist eine Liste von Parametern für diesen Server. Das Schlüsselwort
          "default-server" akzeptiert zahlreiche Optionen, denen ein eigener
          Abschnitt gewidmet ist. Weitere Einzelheiten stehen in Abschnitt 5.
```

Beispiel:

```text
default-server inter 1000 weight 13
```

Siehe auch: "server" und [Abschnitt 5](/de/haproxy/bind-and-server-options/) über Server-Optionen

<a id="entry-4-2-default-backend"></a>

**`default_backend <backend>`**

```haproxy
default_backend <backend>
```

Das Backend festlegen, das verwendet werden soll, wenn keine "use_backend"-Regel zutrifft.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<backend> ist der Name des zu verwendenden Backends.
```

Bei der inhaltsabhängigen Umschaltung zwischen Frontend und Backends unter Verwendung des Schlüsselworts "use_backend" ist es oft nützlich, anzugeben, welches Backend verwendet wird, wenn keine Regel zutrifft. In der Regel ist dies das dynamische Backend, das alle unbestimmten Anfragen empfängt.

Wenn ein Backend deaktiviert oder unveröffentlicht ist, werden default_backend-Regeln, die darauf verweisen, ignoriert, und die Verarbeitung des Streams verbleibt beim ursprünglichen Proxy.

Beispiel:

```text
use_backend     dynamic  if  url_dyn
use_backend     static   if  url_css url_img extension_img
default_backend dynamic
```

Siehe auch: "use_backend"

<a id="entry-4-2-description"></a>

**`description <string>`**

```haproxy
description <string>
```

Einen listen-, frontend- oder backend-Abschnitt beschreiben.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Argumente: Zeichenkette

Ermöglicht das Hinzufügen eines Satzes zur Beschreibung des zugehörigen Objekts auf der HAProxy-HTML-Statistikseite. Die Beschreibung wird rechts neben dem Objektnamen angezeigt. Es ist nicht notwendig, Leerzeichen im `<string>`-Argument durch einen Backslash zu maskieren.

<a id="entry-4-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Einen Proxy, ein Frontend oder ein Backend deaktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Das Schlüsselwort "disabled" dient zur Deaktivierung einer Instanz, hauptsächlich, um einen Listener-Port freizugeben oder einen Dienst vorübergehend zu deaktivieren. Die Instanz wird weiterhin erstellt und ihre Konfiguration überprüft, aber sie wird im Zustand "stopped" erstellt und erscheint in den Statistiken entsprechend. Sie empfängt keinen Datenverkehr und sendet weder Health Checks noch Protokollmeldungen. Es ist möglich, mehrere Instanzen gleichzeitig zu deaktivieren, indem das Schlüsselwort "disabled" in einem "defaults"-Abschnitt verwendet wird.

Standardmäßig kann ein deaktiviertes Backend nicht für die inhaltsabhängige Umschaltung ausgewählt werden. Mit "force-be-switch" kann ein Teil des Datenverkehrs diese Einschränkung jedoch umgehen.

Siehe auch: "enabled", "force-be-switch"

<a id="entry-4-2-dispatch"></a>

**`dispatch <address>:<port>   (deprecated)`**

```haproxy
dispatch <address>:<port>   (deprecated)
```

Eine Standardserveradresse festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<address> ist die IPv4-Adresse des Standardservers. Alternativ wird ein
          auflösbarer Hostname unterstützt; dieser wird jedoch beim Start
          aufgelöst.

<ports>   ist eine zwingend erforderliche Portangabe. Alle Verbindungen werden
          an diesen Port gesendet. Port-Offsets, wie sie bei normalen Servern
          möglich sind, sind hier nicht zulässig.
```

Das Schlüsselwort "dispatch" bezeichnet einen Standardserver, der verwendet wird, wenn kein anderer Server die Verbindung übernehmen kann. Früher wurde es verwendet, um nicht persistente Verbindungen an einen zusätzlichen Load-Balancer weiterzuleiten. Aufgrund seiner einfachen Syntax wurde es auch für einfache TCP-Relais verwendet. Für eine klarere Konfiguration wird empfohlen, darauf zu verzichten und stattdessen die Direktive "server" zu verwenden.

Dieses Schlüsselwort wurde in 3.3 als veraltet markiert und wird wegen einiger interner Einschränkungen in 3.5 entfernt (keine Unterstützung für SSL oder inaktive Verbindungen usw.). Die Verwendung führt zu einer Warnung, die durch Aktivierung der Anweisung "expose-deprecated-directives" im global-Abschnitt unterdrückt werden kann.

Die korrekte Vorgehensweise ohne diese Anweisung ist, einfach einen Server mit derselben Adresse und demselben Port zu deklarieren. Wenn die Anweisung "dispatch" mit anderen Servern kombiniert wurde, sollten diese Server mit einem Gewicht von null konfiguriert werden, damit sie vom Lastverteilungsalgorithmus niemals ausgewählt werden.

Beispiel:

```text
backend deprecated_setup
    dispatch 192.168.100.100:80 # external load balancer's address
    server s1 192.168.100.1:80 cookie S1 check
    server s2 192.168.100.2:80 cookie S2 check

backend modern_setup
    server external_lb 192.168.100.100:80
    server s1 192.168.100.1:80 cookie S1 check weight 0
    server s2 192.168.100.2:80 cookie S2 check weight 0
```

Siehe auch: "server"

<a id="entry-4-2-dynamic-cookie-key"></a>

**`dynamic-cookie-key <string>`**

```haproxy
dynamic-cookie-key <string>
```

Den geheimen Schlüssel für dynamische Cookies eines Backends festlegen.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: Der zu verwendende geheime Schlüssel.

Wenn dynamische Cookies aktiviert sind (siehe die Anweisung "dynamic" für Cookies), wird für jeden Server ein dynamisches Cookie erstellt (sofern nicht explizit auf der "server"-Zeile angegeben), das aus einem Hash der IP-Adresse des Servers, des TCP-Ports und des geheimen Schlüssels gebildet wird. Auf diese Weise kann sichergestellt werden, dass die Sitzungsbindung über mehrere Load-Balancer hinweg erhalten bleibt, selbst wenn Server dynamisch hinzugefügt oder entfernt werden.

<a id="entry-4-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Einen Proxy, ein Frontend oder ein Backend aktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Das Schlüsselwort "enabled" dient zur expliziten Aktivierung einer Instanz, wenn die Standardeinstellung auf "disabled" gesetzt wurde. Dies wird äußerst selten verwendet.

Siehe auch: "disabled"

<a id="entry-4-2-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

Anstelle von HAProxy erzeugter Fehler den Inhalt einer Datei zurückgeben.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<code>    ist der HTTP-Statuscode. HAProxy kann derzeit die Codes
          200, 400, 401, 403, 404, 405, 407, 408, 410, 413, 414, 425,
          429, 431, 500, 501, 502, 503 und 504 erzeugen.

<file>    bezeichnet eine Datei mit der vollständigen HTTP-Antwort. Es wird
          empfohlen, dem Dateinamen wie üblich ".http" anzuhängen, damit
          die Antwort nicht mit HTML-Fehlerseiten verwechselt wird, und
          absolute Pfade zu verwenden, da die Dateien vor einem möglichen
          chroot eingelesen werden.
```

Dieses Schlüsselwort dient zum Ersetzen von Fehlern, die HAProxy selbst erkennt und zurückgibt; vom Server zurückgegebene Fehler werden damit nicht umgeschrieben. Daher werden nur wenige Fehlercodes unterstützt.

Der Code 200 wird als Antwort auf Anfragen ausgegeben, die auf eine "monitor-uri"-Regel passen.

Die Dateien werden beim Start von HAProxy eingelesen und müssen der HTTP-Spezifikation entsprechen. Sie sollten die konfigurierte Puffergröße (BUFSIZE), üblicherweise 16 kB, nicht überschreiten, da andernfalls ein interner Fehler zurückgegeben wird. Außerdem ist es sinnvoll, keine Verweise auf lokale Inhalte (etwa Bilder) einzufügen: Wenn alle Server ausgefallen sind, könnte sonst anstelle eines Bildes ein Fehler zurückgegeben werden, wodurch eine Schleife zwischen Client und HAProxy entsteht. Schließlich darf die Antwort (tune.bufsize - tune.maxrewrite) nicht überschreiten, damit für "http-after-response"-Regeln noch genügend Platz bleibt (siehe "tune.maxrewrite").

Die Dateien werden zusammen mit der Konfiguration gelesen und im Speicher gehalten. Daher werden die Fehler auch dann weiterhin zurückgegeben, wenn der Prozess in einer chroot-Umgebung läuft; Änderungen an den Dateien werden während der Laufzeit des Prozesses nicht berücksichtigt. Eine einfache Methode zur Entwicklung dieser Dateien besteht darin, sie dem Statuscode 403 zuzuordnen und eine gesperrte URL abzufragen.

Siehe auch: "http-error", "errorloc", "errorloc302", "errorloc303"

Beispiel:

```text
errorfile 400 /etc/haproxy/errorfiles/400badreq.http
errorfile 408 /dev/null  # work around Chrome pre-connect bug
errorfile 403 /etc/haproxy/errorfiles/403forbid.http
errorfile 503 /etc/haproxy/errorfiles/503sorry.http

```

<a id="entry-4-2-errorfiles"></a>

**`errorfiles <name> [<code> ...]`**

```haproxy
errorfiles <name> [<code> ...]
```

Die im http-errors-Abschnitt `<name>` definierten Fehlerdateien vollständig oder teilweise importieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<name>  ist der Name eines vorhandenen http-errors-Abschnitts.

<code>  ist ein HTTP-Statuscode. Mehrere Statuscodes können angegeben werden.
        HAProxy kann derzeit die Codes 200, 400, 401, 403, 404, 405, 407,
        408, 410, 413, 414, 425, 429, 431, 500, 501, 502, 503 und 504
        erzeugen.
```

Die im http-errors-Abschnitt mit dem Namen `<name>` definierten Fehler werden in den aktuellen Proxy importiert. Wird kein Statuscode angegeben, werden alle Fehlerdateien dieses http-errors-Abschnitts importiert. Andernfalls werden nur die Fehlerdateien für die aufgeführten Statuscodes importiert. Diese Fehlerdateien überschreiben die bereits für den Proxy definierten benutzerdefinierten Fehler. Sie können ihrerseits durch nachfolgende Definitionen überschrieben werden. Funktional entspricht dies genau der manuellen Deklaration aller Fehlerdateien mit "errorfile"-Direktiven.

Siehe auch: "http-error", "errorfile", "errorloc", "errorloc302", "errorloc303" und [Abschnitt 12.4](/de/haproxy/other-sections/#section-12-4) zu http-errors.

Beispiel:

```text
errorfiles generic
errorfiles site-1 403 404

```

<a id="entry-4-2-errorloc"></a>

**`errorloc <code> <url>`**

```haproxy
errorloc <code> <url>
errorloc302 <code> <url>
```

Anstelle von HAProxy erzeugter Fehler eine HTTP-Weiterleitung zu einer URL zurückgeben

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<code>    ist der HTTP-Statuscode. HAProxy kann derzeit die Codes
          200, 400, 401, 403, 404, 405, 407, 408, 410, 413, 414, 425,
          429, 431, 500, 501, 502, 503 und 504 erzeugen.

<url>     ist der genaue Inhalt des Headers "Location". Er kann eine relative
          URI zu einer Fehlerseite auf derselben Website oder eine absolute
          URI zu einer Fehlerseite auf einer anderen Website enthalten.
          Relative URIs sollten besonders sorgfältig gewählt werden, um
          Weiterleitungsschleifen zu vermeiden, wenn die URI selbst denselben
          Fehler auslösen kann (z. B. 500).
```

Dieses Schlüsselwort dient zum Ersetzen von Fehlern, die HAProxy selbst erkennt und zurückgibt; vom Server zurückgegebene Fehler werden damit nicht umgeschrieben. Daher werden nur wenige Fehlercodes unterstützt.

Der Code 200 wird als Antwort auf Anfragen ausgegeben, die auf eine "monitor-uri"-Regel passen.

Beide Schlüsselwörter geben den HTTP-Statuscode 302 zurück, der den Client anweist, die angegebene URL mit derselben HTTP-Methode abzurufen. Bei anderen Methoden als GET, etwa POST, kann dies erhebliche Probleme verursachen, da die an den Client gesendete URL möglicherweise nur GET zulässt. Um dieses Problem zu umgehen, verwenden Sie "errorloc303": Es sendet den HTTP-Statuscode 303 und weist den Client damit an, die URL mit einer GET-Anfrage abzurufen.

Siehe auch: "http-error", "errorfile", "errorloc303"

<a id="entry-4-2-errorloc303"></a>

**`errorloc303 <code> <url>`**

```haproxy
errorloc303 <code> <url>
```

Anstelle von HAProxy erzeugter Fehler eine HTTP-Weiterleitung zu einer URL zurückgeben

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<code>    ist der HTTP-Statuscode. HAProxy kann derzeit die Codes
          200, 400, 401, 403, 404, 405, 407, 408, 410, 413, 414, 425,
          429, 431, 500, 501, 502, 503 und 504 erzeugen.

<url>     ist der genaue Inhalt des Headers "Location". Er kann eine relative
          URI zu einer Fehlerseite auf derselben Website oder eine absolute
          URI zu einer Fehlerseite auf einer anderen Website enthalten.
          Relative URIs sollten besonders sorgfältig gewählt werden, um
          Weiterleitungsschleifen zu vermeiden, wenn die URI selbst denselben
          Fehler auslösen kann (z. B. 500).
```

Dieses Schlüsselwort dient zum Ersetzen von Fehlern, die HAProxy selbst erkennt und zurückgibt; vom Server zurückgegebene Fehler werden damit nicht umgeschrieben. Daher werden nur wenige Fehlercodes unterstützt.

Der Code 200 wird als Antwort auf Anfragen ausgegeben, die auf eine "monitor-uri"-Regel passen.

Beide Schlüsselwörter geben den HTTP-Statuscode 303 zurück, der den Client anweist, die angegebene URL mit derselben HTTP-Methode GET abzurufen. Dies löst die üblichen Probleme mit "errorloc" und dem Code 302. Möglicherweise unterstützen einige sehr alte, vor HTTP/1.1 entwickelte Browser dies nicht; bislang wurden jedoch keine solchen Probleme gemeldet.

Siehe auch: "http-error", "errorfile", "errorloc", "errorloc302"

<a id="entry-4-2-email-alert-from"></a>

**`email-alert from <emailaddr>`**

```haproxy
email-alert from <emailaddr>
```

Die Absenderadresse festlegen, die sowohl im Umschlag als auch im Header der E-Mail-Benachrichtigungen verwendet wird. Von dieser Adresse werden die E-Mail-Benachrichtigungen versendet.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<emailaddr> ist die Absenderadresse für E-Mail-Warnungen.
```

Außerdem müssen "email-alert mailers" und "email-alert to" festgelegt sein. Dann wird der Versand von E-Mail-Benachrichtigungen für den Proxy aktiviert.

Siehe auch: "email-alert level", "email-alert mailers", "email-alert myhostname", "email-alert to", [Abschnitt 12.3](/de/haproxy/other-sections/#section-12-3) zu Mailern.

<a id="entry-4-2-email-alert-level"></a>

**`email-alert level <level>`**

```haproxy
email-alert level <level>
```

Die maximale Protokollstufe von Meldungen festlegen, für die E-Mail-Benachrichtigungen gesendet werden. Dies dient als Filter für den Versand der E-Mail-Benachrichtigungen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<level> Eine der 8 syslog-Stufen:
          emerg alert crit err warning notice info  debug
        Die obigen syslog-Stufen sind von der niedrigsten zur höchsten geordnet.
```

Die Standardstufe ist alert

Außerdem müssen "email-alert from", "email-alert mailers" und "email-alert to" festgelegt sein. Dann wird der Versand von E-Mail-Benachrichtigungen für den Proxy aktiviert.

Benachrichtigungen werden gesendet, wenn:

- ein nicht pausierter Server als ausgefallen markiert wird und `<level>` alert oder niedriger ist
- ein pausierter Server als ausgefallen markiert wird und `<level>` notice oder niedriger ist
- ein Server als verfügbar markiert wird oder in den Zustand drain wechselt und `<level>` notice oder niedriger ist
- "option log-health-checks" aktiviert ist, `<level>` info oder niedriger ist und der Status eines Health Checks aktualisiert wird

Siehe auch: "email-alert from", "email-alert mailers", "email-alert myhostname", "email-alert to", [Abschnitt 12.3](/de/haproxy/other-sections/#section-12-3) zu Mailern.

<a id="entry-4-2-email-alert-mailers"></a>

**`email-alert mailers <mailersect>`**

```haproxy
email-alert mailers <mailersect>
```

Die Mailer festlegen, die für den Versand von E-Mail-Benachrichtigungen verwendet werden

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<mailersect> ist der Name des mailers-Abschnitts für E-Mail-Warnungen.
```

Außerdem müssen "email-alert from" und "email-alert to" festgelegt sein. Dann wird der Versand von E-Mail-Benachrichtigungen für den Proxy aktiviert.

Siehe auch: "email-alert from", "email-alert level", "email-alert myhostname", "email-alert to", [Abschnitt 12.3](/de/haproxy/other-sections/#section-12-3) zu Mailern.

<a id="entry-4-2-email-alert-myhostname"></a>

**`email-alert myhostname <hostname>`**

```haproxy
email-alert myhostname <hostname>
```

Den Hostnamen festlegen, der bei der Kommunikation mit Mailern verwendet wird.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<hostname> ist der Hostname für die Kommunikation mit Mailservern.
```

Standardmäßig wird der Hostname des Systems verwendet.

Außerdem müssen "email-alert from", "email-alert mailers" und "email-alert to" festgelegt sein. Dann wird der Versand von E-Mail-Benachrichtigungen für den Proxy aktiviert.

Siehe auch: "email-alert from", "email-alert level", "email-alert mailers", "email-alert to", [Abschnitt
12.3](/de/haproxy/other-sections/#section-12-3) zu Mailern.

<a id="entry-4-2-email-alert-to"></a>

**`email-alert to <emailaddr>`**

```haproxy
email-alert to <emailaddr>
```

Sowohl die Empfängeradresse im Umschlag als auch die Zieladresse im Header von E-Mail-Benachrichtigungen festlegen. An diese Adresse werden die E-Mail-Benachrichtigungen gesendet.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<emailaddr> ist die Empfängeradresse für E-Mail-Warnungen.
```

Außerdem müssen "email-alert mailers" und "email-alert to" festgelegt sein. Dann wird der Versand von E-Mail-Benachrichtigungen für den Proxy aktiviert.

Siehe auch: "email-alert from", "email-alert level", "email-alert mailers", "email-alert myhostname", [Abschnitt 12.3](/de/haproxy/other-sections/#section-12-3) zu Mailern.

<a id="entry-4-2-error-log-format"></a>

**`error-log-format <fmt>`**

```haproxy
error-log-format <fmt>
```

Die Formatzeichenkette für Protokolleinträge bei Verbindungsfehlern auf der Frontendseite festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Diese Direktive legt die Formatzeichenkette für Protokolleinträge fest, die Informationen zu Fehlern, Zeitüberschreitungen, Wiederholungsversuchen, erneuten Zuweisungen oder HTTP-Statuscodes 5xx enthalten. Dieses Format gilt somit für jede Protokollzeile, auf die sich die Option "log-separate-errors" auswirken würde, einschließlich der in [Abschnitt 8.2.5](/de/haproxy/configuration-logging/#section-8-2-5) beschriebenen Verbindungsfehler.

Wird die Direktive in einem defaults-Abschnitt verwendet, verwenden alle nachfolgenden Frontends dasselbe Protokollformat. [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschreibt benutzerdefinierte Formatzeichenketten für Protokolle ausführlich.

Die Direktive "error-log-format" überschreibt vorherige "error-log-format"-Direktiven.

<a id="entry-4-2-force-persist"></a>

**`force-persist { if | unless } <condition>`**

```haproxy
force-persist { if | unless } <condition>
```

Eine Bedingung deklarieren, um die Sitzungsbindung an ausgefallene Server zu erzwingen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Standardmäßig werden Anfragen nicht an ausgefallene Server verteilt. Mit "option
persist" lässt sich dies erzwingen, allerdings ohne Bedingung; bei gesetzter "option redispatch" erfolgt zudem eine erneute Zuweisung an einen funktionsfähigen Server. Damit bleiben nur wenige Möglichkeiten, bestimmte Anfragen gezielt an einen Server zu senden, der für Wartungsarbeiten künstlich als ausgefallen markiert wurde.

Mit der Anweisung "force-persist" können verschiedene ACL-basierte Bedingungen deklariert werden. Sind sie erfüllt, ignoriert eine Anfrage den Ausfallstatus eines Servers und versucht dennoch, eine Verbindung zu ihm herzustellen. So lässt sich ein Server starten, der auf Health Checks weiterhin einen Fehler zurückgibt, und der Dienst mit einem speziell konfigurierten Browser testen. Praktische Möglichkeiten sind beispielsweise eine bestimmte Quell-IP-Adresse oder ein bestimmtes Cookie. Das Cookie hat außerdem den Vorteil, dass es im Browser über eine Testseite einfach hinzugefügt oder entfernt werden kann. Sobald der Dienst überprüft ist, kann er allgemein zugänglich gemacht werden, indem er auf Health Checks eine gültige Antwort zurückgibt.

Die erzwungene Sitzungsbindung wird aktiviert, wenn eine "if"-Bedingung erfüllt ist oder eine "unless"-Bedingung nicht erfüllt ist. Die abschließende erneute Zuweisung ist dabei immer deaktiviert.

Siehe auch: "option redispatch", "ignore-persist", "persist" und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-external-check-command"></a>

**`external-check command <command>`**

```haproxy
external-check command <command>
```

Das bei einem external-check auszuführende Programm

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<command> ist der auszuführende externe Befehl.
```

Dem Befehl werden folgende Argumente übergeben:

`<proxy_address>` `<proxy_port>` `<server_address>` `<server_port>`

Die Werte `<proxy_address>` und `<proxy_port>` werden vom ersten Listener abgeleitet, der IPv4, IPv6 oder ein UNIX-Socket verwendet. Bei einem UNIX-Socket-Listener ist proxy_address der Pfad des Sockets und `<proxy_port>` die Zeichenkette "NOT_USED". In einem backend-Abschnitt lässt sich kein Listener bestimmen; daher haben sowohl `<proxy_address>` als auch `<proxy_port>` den Zeichenkettenwert "NOT_USED".

Einige Werte werden auch über Umgebungsvariablen bereitgestellt.

Umgebungsvariablen:

```text
HAPROXY_PROXY_ADDR      Die erste bind-Adresse, falls vorhanden; andernfalls
                        leer, etwa in einem "backend"-Abschnitt.

HAPROXY_PROXY_ID        Die Backend-ID.

HAPROXY_PROXY_NAME      Der Backend-Name.

HAPROXY_PROXY_PORT      Der erste bind-Port, falls vorhanden; andernfalls
                        leer, etwa in einem "backend"-Abschnitt oder bei
                        einem UNIX-Socket.

HAPROXY_SERVER_ADDR     Die Serveradresse.

HAPROXY_SERVER_CURCONN  Die aktuelle Zahl der Verbindungen auf dem Server.

HAPROXY_SERVER_ID       Die Server-ID.

HAPROXY_SERVER_MAXCONN  Die maximale Verbindungszahl des Servers.

HAPROXY_SERVER_NAME     Der Servername.

HAPROXY_SERVER_PORT     Der Serverport, falls vorhanden; bei einem UNIX-Socket
                        leer.

HAPROXY_SERVER_SSL      "0", wenn SSL nicht verwendet wird, andernfalls "1".

HAPROXY_SERVER_PROTO    Das vom Server verwendete Protokoll: "cli" (haproxy-CLI),
                        "syslog" (syslog-TCP-Server), "peers" (peers-TCP-Server),
                        "h1" (HTTP/1.x-Server), "h2" (HTTP/2-Server) oder
                        "tcp" (jeder andere TCP-Server).

PATH                    Die beim Ausführen des Befehls verwendete
                        Umgebungsvariable PATH kann mit "external-check path"
                        gesetzt werden.
```

Wird der Befehl ausgeführt und mit dem Status null beendet, gilt die Prüfung als erfolgreich; andernfalls gilt sie als fehlgeschlagen.

Beispiel:

```text
external-check command /bin/true
```

Siehe auch: "external-check", "option external-check", "external-check path"

<a id="entry-4-2-external-check-path"></a>

**`external-check path <path>`**

```haproxy
external-check path <path>
```

Der Wert der Umgebungsvariablen PATH bei der Ausführung eines external-check

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<path> ist der Pfad, der beim Ausführen des externen Befehls verwendet wird.
```

Der Standardpfad ist "".

Beispiel:

```text
external-check path "/usr/bin:/bin"
```

Siehe auch: "external-check", "option external-check", "external-check command"

<a id="entry-4-2-force-be-switch"></a>

**`force-be-switch { if | unless } <condition>`**

```haproxy
force-be-switch { if | unless } <condition>
```

Der inhaltsabhängigen Umschaltung erlauben, ein Backend auch dann auszuwählen, wenn es deaktiviert oder unveröffentlicht ist. Administratoren können mit dieser Regel den Datenverkehr zu Diensten testen, bevor sie diese nach außen zugänglich machen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Siehe auch: "be-unpublished", "disabled"

<a id="entry-4-2-filter"></a>

**`filter <name> [param*]`**

```haproxy
filter <name> [param*]
```

Den Filter `<name>` zur Filterliste des Proxys hinzufügen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Argumente:

```text
<name>     ist der Name des Filters. Offiziell unterstützte Filter sind in
           Abschnitt 9 aufgeführt.

<param*>   ist eine Liste von Parametern, die der Filter <name> akzeptiert.
           Für das Einlesen dieser Parameter ist der Filter verantwortlich.
           Alle Einzelheiten zu unterstützten Parametern stehen in der
           Dokumentation des jeweiligen Filters (Abschnitt 9).
```

Die filter-Zeile kann für denselben Proxy mehrfach verwendet werden. Bei Bedarf kann derselbe Filter mehrmals referenziert werden.

Beispiel:

```text
listen
  bind *:80

  filter trace name BEFORE-HTTP-COMP
  filter compression
  filter trace name AFTER-HTTP-COMP

  compression algo gzip
  compression offload

  server srv1 192.168.0.1:80
```

Siehe auch: [Abschnitt 9](/de/haproxy/filters/).

<a id="entry-4-2-fullconn"></a>

**`fullconn <conns>`**

```haproxy
fullconn <conns>
```

Festlegen, bei welcher Backend-Last die Server ihren maxconn-Wert erreichen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<conns>   ist die Zahl von Verbindungen am Backend, bei der die Server
          ihre maximale Verbindungszahl verwenden.
```

Ist für einen Server der Parameter "maxconn" angegeben, überschreitet seine Anzahl gleichzeitiger Verbindungen diesen Wert niemals. Ist zusätzlich "minconn" angegeben, bezeichnet dies eine dynamische Grenze, die der Backend-Last folgt. Der Server akzeptiert dann stets mindestens `<minconn>` Verbindungen, aber nie mehr als `<maxconn>`. Hat das Backend weniger als `<conns>` gleichzeitige Verbindungen, steigt die Grenze linear zwischen den beiden Werten an. Dadurch lässt sich die Serverlast bei normalem Betrieb begrenzen und bei hoher Last weiter erhöhen, ohne die Server bei außergewöhnlich hoher Last zu überlasten.

Da sich dieser Wert nur schwer richtig bestimmen lässt, setzt HAProxy ihn automatisch auf 10% der Summe der maxconn-Werte aller Frontends, die zu diesem Backend verzweigen können (anhand der Regeln "use_backend" und "default_backend"). Daher kann die Angabe gefahrlos entfallen. "use_backend"-Regeln mit dynamischen Namen werden jedoch nicht berücksichtigt, da sich nicht feststellen lässt, ob sie auf dieses Backend verweisen könnten.

Beispiel:

```shell
# The servers will accept between 100 and 1000 concurrent connections each
# and the maximum of 1000 will be reached when the backend reaches 10000
# connections.
backend dynamic
   fullconn   10000
   server     srv1   dyn1:80 minconn 100 maxconn 1000
   server     srv2   dyn2:80 minconn 100 maxconn 1000
```

Siehe auch: "maxconn", "server"

<a id="entry-4-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

Eine globale, eindeutige ID für diesen Proxy festlegen, bei der Groß- und Kleinschreibung unterschieden werden.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

`<string>` muss in der gesamten haproxy-Konfiguration über alle Objekttypen hinweg eindeutig sein. Das Format ist nicht vorgegeben, damit Benutzer ihre eigene Namenskonvention wählen können. Die einzige Einschränkung ist die Länge, die 127 Zeichen nicht überschreiten darf. Zulässig sind alle alphanumerischen Zeichen sowie '.', ':', '-' und '\_'. Siehe auch "shm-stats-file".

<a id="entry-4-2-hash-balance-factor"></a>

**`hash-balance-factor <factor>`**

```haproxy
hash-balance-factor <factor>
```

Den Lastverteilungsfaktor für konsistentes Hashing mit begrenzter Last festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| nein \| ja

Argumente:

```text
<factor> steuert die maximale Zahl gleichzeitiger Anfragen an einen Server,
         ausgedrückt als Prozentsatz der durchschnittlichen Zahl gleichzeitiger
         Anfragen über alle aktiven Server.
```

Die Angabe eines "hash-balance-factor" für einen Server mit "hash-type consistent" aktiviert einen Algorithmus, der verhindert, dass ein einzelner Server zu viele Anfragen gleichzeitig erhält, selbst wenn manche Hash-Buckets wesentlich mehr Anfragen erhalten als andere. Der Wert 0 für `<factor>` (der Standardwert) deaktiviert die Funktion. Andernfalls ist `<factor>` ein Prozentsatz größer als 100. Ist `<factor>` beispielsweise 150, darf kein Server eine Last von mehr als dem 1.5-Fachen des Durchschnitts haben. Werden Servergewichte verwendet, werden diese berücksichtigt.

Scheidet der zunächst ausgewählte Server aus, wählt der Algorithmus anhand des Anfragehashes einen anderen Server, bis ein Server mit freier Kapazität gefunden wird. Ein höherer `<factor>` erlaubt eine ungleichmäßigere Verteilung zwischen den Servern; ein niedrigerer `<factor>` bedeutet dagegen, dass im Durchschnitt mehr Server geprüft werden, was sich auf die Leistung auswirkt. Sinnvolle Werte liegen zwischen 125 und 200.

Diese Einstellung wird auch von "balance random" verwendet, das intern auf dem Verfahren des konsistenten Hashings beruht.

Siehe auch: "balance" und "hash-type".

<a id="entry-4-2-hash-preserve-affinity"></a>

**`hash-preserve-affinity { always | maxconn | maxqueue }`**

```haproxy
hash-preserve-affinity { always | maxconn | maxqueue }
```

Ein Verfahren für die Zuordnung von Streams zu Servern bei hashbasierter Lastverteilung festlegen, wenn Server ausgelastet sind oder eine volle Warteschlange haben.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Folgende Werte können angegeben werden:

    - "always"  : Dies ist die Standardstrategie. Ein Stream wird anhand des
                   Hashings einem Server zugeordnet, unabhängig davon, ob der
                   Server derzeit ausgelastet ist.

    - "maxconn" : Bei dieser Auswahl werden Server übersprungen, für die
                   "maxconn" festgelegt ist und die derzeit ausgelastet sind.
                   Entlang des Hash-Rings wird ein anderer Server ausgewählt.
                   Dies wirkt sich nicht auf Server ohne "maxconn" aus. Sind
                   alle Server ausgelastet, wird die Anfrage in die Warteschlange
                   des letzten Servers im Hash-Ring vor dem ursprünglich
                   ausgewählten Server eingereiht.

    - "maxqueue": Bei dieser Auswahl werden Server übersprungen, für die
                   "maxconn" festgelegt ist, "maxqueue" einen Wert ungleich null
                   hat (begrenzte Warteschlangengröße) und deren Warteschlange
                   derzeit voll ist. Entlang des Hash-Rings wird ein anderer
                   Server ausgewählt. Dies wirkt sich nicht auf Server aus,
                   bei denen nicht sowohl "maxconn" als auch "maxqueue"
                   festgelegt sind.

Siehe auch: "maxconn", "maxqueue", "hash-balance-factor"

<a id="entry-4-2-hash-type"></a>

**`hash-type <method> <function> <modifier>`**

```haproxy
hash-type <method> <function> <modifier>
```

Ein Verfahren zur Zuordnung von Hashes zu Servern festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<method> ist die Methode zur Serverauswahl anhand des von <function>
         berechneten Hashes:

  map-based   Die Hash-Tabelle ist ein statisches Array aller verfügbaren
              Server. Die Hashes sind sehr gleichmäßig und berücksichtigen
              Gewichte, sind jedoch statisch: Gewichtsänderungen eines
              verfügbaren Servers werden ignoriert. Ein langsamer Anlauf
              ist daher nicht möglich. Da ein Server anhand seiner Position
              im Array ausgewählt wird, ändern sich die meisten Zuordnungen
              bei einer Änderung der Serverzahl. Wird ein Server verfügbar,
              fällt er aus oder wird er einer Gruppe hinzugefügt, werden
              deshalb die meisten Verbindungen auf andere Server umverteilt.
              Dies kann beispielsweise bei Caches ungünstig sein.

  consistent  Die Hash-Tabelle ist ein Baum, der jeden Server mehrfach enthält.
              Der Hash-Schlüssel wird im Baum gesucht und der nächstgelegene
              Server ausgewählt. Dieser Hash ist dynamisch und unterstützt
              Gewichtsänderungen verfügbarer Server; damit ist er mit dem
              langsamen Anlauf vereinbar. Sein Vorteil: Wird ein Server
              verfügbar oder fällt er aus, werden nur seine Zuordnungen
              verschoben. Wird der Gruppe ein Server hinzugefügt, wird nur
              ein kleiner Teil der Zuordnungen umverteilt. Daher eignet sich
              diese Methode besonders für Caches. Prinzipbedingt ist die
              Verteilung jedoch nie ganz gleichmäßig. Gelegentlich kann es nötig sein,
              Gewicht oder ID eines Servers anzupassen, um die Last
              gleichmäßiger zu verteilen. Für dieselbe Verteilung auf mehreren
              Load-Balancern ist es wichtig, dass alle Server exakt dieselben IDs haben.
              Hinweis: Ohne ausdrückliche Hash-Funktion verwendet konsistentes
              Hashing sdbm und avalanche.

<function> ist die zu verwendende Hash-Funktion:

   sdbm   Diese Funktion wurde ursprünglich für die Datenbankbibliothek sdbm
          entwickelt, eine gemeinfreie Neuimplementierung von ndbm. Sie mischt
          Bits gut und erreicht dadurch eine bessere Schlüsselverteilung
          und weniger Aufteilungen. Sie eignet sich außerdem als allgemeine
          Hash-Funktion mit guter Verteilung, sofern das Gesamtgewicht der
          Server kein Vielfaches von 64 ist. Andernfalls kann der Modifikator
          avalanche helfen.

   djb2   Diese Funktion wurde vor vielen Jahren erstmals von Dan Bernstein
          in comp.lang.c vorgeschlagen. Studien zeigen, dass sie bei bestimmten
          Lastprofilen eine bessere Verteilung als sdbm liefert. Mit
          textbasierten Eingaben funktioniert sie meist gut, kann jedoch bei
          rein numerischen Eingaben oder einem Gesamtgewicht als Vielfaches
          von 33 extrem schlecht abschneiden, sofern nicht zusätzlich der
          Modifikator avalanche verwendet wird.

   wt6    Diese Funktion wurde früher beim Testen anderer Funktionen für
          HAProxy entwickelt. Sie verteilt nicht so gleichmäßig wie die
          anderen, reagiert aber deutlich weniger empfindlich auf die
          Eingabedaten oder die Serverzahl. Sie kann als Alternative zu
          sdbm+avalanche oder djb2+avalanche für konsistentes Hashing oder
          für numerische Daten sinnvoll sein, etwa eine Quell-IP-Adresse
          oder eine Besucherkennung in einem URL-Parameter.

   crc32  Dies ist die verbreitetste CRC32-Implementierung, wie sie etwa in
          Ethernet, gzip und PNG verwendet wird. Sie ist langsamer als die
          anderen, kann aber besonders bei Zeichenfolgen eine bessere
          Verteilung oder weniger vorhersehbare Ergebnisse liefern.

   none   Der Schlüssel wird nicht gehasht, sondern direkt als Hash verwendet.
          Dies ist nützlich, um den Schlüssel selbst mit einem Konverter zu
          hashen und haproxy das Ergebnis direkt verwenden zu lassen. Dazu
          wird der Schlüssel gegebenenfalls in eine Zeichenfolge umgewandelt
          und als ganze Zahl eingelesen, deren Wert als Schlüssel dient.
          Einige Typen von Eingabeschlüsseln, etwa IP-Adressen, sind hierfür
          möglicherweise nicht sinnvoll.

<modifier> gibt eine optionale Methode an, die nach dem Hashen angewendet wird:

   avalanche   Diese Direktive gibt an, dass das Ergebnis der obigen
               Hash-Funktion nicht unverändert verwendet werden sollte,
               sondern zuerst ein vollständiger Avalanche-Hash mit 4 Byte
               darauf angewendet werden muss. Dabei werden die Ergebnisbits
               des vorherigen Hashes gemischt, um unerwünschte Effekte bei
               wenigen möglichen Eingabewerten oder einer Serverzahl als
               Vielfaches einer Hash-Komponente zu vermeiden (64 bei SDBM,
               33 bei DJB2). Mit avalanche ist das Ergebnis meist weniger
               vorhersehbar, aber auch weniger gleichmäßig als bei der
               ursprünglichen Funktion. Bei manchen Lastprofilen können
               Tests nötig sein. Dieser Hash gehört zu den vielen von
               Bob Jenkins vorgeschlagenen Hash-Funktionen.
```

Der Standard-Hash-Typ ist "map-based" und wird für die meisten Anwendungen empfohlen. Die Standardfunktion ist "sdbm"; die Funktion sollte anhand des Wertebereichs der zu hashenden Werte ausgewählt werden.

Siehe auch: "balance", "hash-balance-factor", "hash-preserve-affinity", "server"

<a id="entry-4-2-http-after-response"></a>

**`http-after-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-after-response <action> <options...> [ { if | unless } <condition> ]
```

Zugriffskontrolle für alle Antworten auf Schicht 7 (von Servern, Applets/Diensten und intern erzeugte Antworten).

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Die Anweisung http-after-response definiert Regeln für die Verarbeitung auf Schicht 7. Die Regeln werden in der Reihenfolge ihrer Deklaration ausgewertet, wenn sie in einem Abschnitt frontend, listen oder backend vorkommen. Da sie auf Antworten angewendet werden, werden zuerst die Regeln des Backends und anschließend die des Frontends angewendet. Auf jede Regel kann optional eine ACL-basierte Bedingung folgen; dann wird die Regel nur ausgewertet, wenn diese Bedingung wahr ist.

Anders als http-response-Regeln gelten diese Regeln für alle Antworten: sowohl für Serverantworten als auch für sämtliche von HAProxy erzeugten Antworten. Sie werden am Ende der Antwortanalyse und vor der Datenweiterleitung ausgewertet.

Die Bedingung wird unmittelbar vor der Ausführung der Aktion ausgewertet, und die Aktion wird genau einmal ausgeführt. Daher ist es unproblematisch, wenn eine Aktion ein Element ändert, das in der Bedingung geprüft wird. Das bedeutet auch, dass mehrere Aktionen dieselbe Bedingung verwenden können: Die erste Aktion, die das Ergebnis der Bedingung ändert, reicht dann aus, um die übrigen Aktionen implizit zu deaktivieren. Dies wird beispielsweise verwendet, wenn einer leeren Variablen ein Wert aus verschiedenen Quellen zugewiesen werden soll. Die Anzahl der "http-after-response"-Anweisungen pro Instanz ist nicht begrenzt.

Das erste Schlüsselwort nach "http-after-response" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "HTTP Aft").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Hinweis: Fehler, die bereits früh beim Parsen der Anfrage auftreten, werden auf einer niedrigeren Ebene vom Multiplexer behandelt, noch vor jeder HTTP-Analyse. Für diese Fehler wird daher kein http-after-response-Regelsatz ausgewertet.

Beispiel:

```text
http-after-response set-header Strict-Transport-Security "max-age=31536000"
http-after-response set-header Cache-Control "no-store,no-cache,private"
http-after-response set-header Pragma "no-cache"

```

<a id="entry-4-2-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
```

Einen Kommentar für die nachfolgende http-check-Regel definieren, der bei ihrem Fehlschlagen im Protokoll ausgegeben wird.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<string>  ist die Kommentarmeldung, die dem Protokoll hinzugefügt wird,
          wenn die nachfolgende http-check-Regel fehlschlägt.
```

Dies funktioniert nur für die Regeln connect, send und expect. Es dient einer verständlichen Fehlermeldung.

Siehe auch: "option httpchk", "http-check connect", "http-check send" und "http-check expect".

<a id="entry-4-2-http-check-connect"></a>

**`http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]`**

```haproxy
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
```

Eine neue Verbindung für einen HTTP-Health-Check öffnen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

default      Die Standardoptionen der server-Zeile für Health Checks verwenden.
             Die Serveroptionen werden nur verwendet, wenn sie nicht neu
             definiert wurden.

port <expr>  Ohne Angabe wird der Prüfport oder der Serverport verwendet.
             Gibt HAProxy das Ziel für den Verbindungsaufbau an.
             <port> muss eine gültige ganze TCP-Portnummer von 1 bis 65535
             oder ein Sample-Abruf-Ausdruck sein.

addr <ip>    legt die IP-Adresse für den Health Check fest.

send-proxy   sendet eine Zeichenfolge des PROXY-Protokolls.

via-socks4   aktiviert ausgehende Health Checks über einen vorgeschalteten
             socks4-Proxy.

ssl          öffnet eine verschlüsselte Verbindung.

sni <sni>    gibt die SNI für Health Checks über SSL an.

alpn <alpn>  legt fest, welche Protokolle über ALPN angekündigt werden.
             Die Protokollliste enthält durch Kommas getrennte Protokollnamen,
             etwa "h2,http/1.1". Ohne Angabe wird das ALPN des Servers verwendet.

proto <name> erzwingt das für diese Verbindung zu verwendende
             Multiplexer-Protokoll. Es muss ein HTTP-Mux-Protokoll sein und
             auf der Backend-Seite verwendet werden können. Die verfügbaren
             Protokolle werden von haproxy -vv ausgegeben.

linger       schließt die Verbindung sauber, statt nur ein RST zu senden.
```

Wie bei tcp-check-Health-Checks kann die Verbindung konfiguriert werden, die für einen HTTP-Health-Check verwendet wird. Diese Direktive sollte auch zur Beschreibung eines Szenarios mit mehreren Anfrage-Antwort-Wechseln verwendet werden, möglicherweise über unterschiedliche Ports oder mit unterschiedlichen Servern.

Wenn weder in der Serverzeile ein TCP-Port noch eine port-Direktive für den Server konfiguriert ist, muss im ersten Schritt der http-check-Sequenz der Port mit "http-check connect" angegeben werden.

In einem http-check-Regelsatz ist ein 'connect' erforderlich; außerdem muss der Regelsatz mit einer 'connect'-Regel beginnen. Damit soll sichergestellt werden, dass Administratoren wissen, was sie tun.

Auch wenn der Regelsatz mit connect beginnen muss, dürfen diesem noch Regeln vom Typ set-var, unset-var oder comment vorausgehen.

Beispiele:

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option httpchk

http-check connect
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399
http-check connect port 443 ssl sni haproxy.1wt.eu
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399

server www 10.0.0.1 check port 80
```

Siehe auch: "option httpchk", "http-check send", "http-check expect"

<a id="entry-4-2-http-check-disable-on-404"></a>

**`http-check disable-on-404`**

```haproxy
http-check disable-on-404
```

Bei einer HTTP/404-Antwort auf Health Checks einen Wartungsmodus aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Wenn diese Option aktiviert ist, wird ein Server, der eine HTTP-Antwort 404 zurückgibt, aus der weiteren Lastverteilung ausgeschlossen, empfängt jedoch weiterhin Verbindungen mit Sitzungsbindung. Damit können Web-Administratoren ihre Server bequem geordnet herunterfahren. Es ist wichtig zu beachten, dass ein Server, der als ausgefallen erkannt wird, während er sich in diesem Modus befindet, keine alert-Meldung auslöst, sondern lediglich eine notice-Meldung. Wenn der Server erneut 2xx oder 3xx antwortet, wird er sofort wieder in die Farm eingefügt. Der Status auf der Statistikseite meldet "NOLB" für einen Server in diesem Modus. Es ist wichtig zu beachten, dass diese Option nur in Verbindung mit der "httpchk"-Option funktioniert. Wenn diese Option zusammen mit "http-check expect" verwendet wird, hat sie Vorrang, sodass 404-Antworten weiterhin als Soft-Stop betrachtet werden. Beachten Sie außerdem, dass ein gestoppter Server auch dann weiterhin gestoppt bleibt, wenn er mit 404 antwortet. Diese Option wird nur für laufende Server ausgewertet.

Siehe auch: "option httpchk" und "http-check expect".

<a id="entry-4-2-http-check-expect"></a>

**`http-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
```

HTTP-Health-Checks so konfigurieren, dass sie Antwortinhalte oder bestimmte Statuscodes berücksichtigen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

min-recv  ist optional und kann die minimale Datenmenge festlegen, die für
          die Auswertung der aktuellen expect-Regel erforderlich ist. Liegt
          die Zahl empfangener Bytes darunter, wartet die Prüfung auf weitere
          Daten. Damit lassen sich mehrdeutige Vergleichsregeln auflösen oder
          aufwendige Regex-Vergleiche auf bekanntermaßen noch unvollständigen
          Inhalten vermeiden. Bei einer exakten Zeichenfolge wird das Minimum
          aus Zeichenfolgenlänge und diesem Parameter verwendet. Der Wert -1
          bewirkt, dass der Parameter ignoriert wird. Trifft die expect-Regel
          nicht zu, wartet die Prüfung auf weitere Daten. Beim Wert 0 ist
          das Auswertungsergebnis immer endgültig.

ok-status <st>     ist optional und kann den Prüfstatus setzen, wenn die
                   expect-Regel erfolgreich ausgewertet wird und die letzte
                   Regel im tcp-check-Regelsatz ist. Unterstützt werden
                   "L7OK", "L7OKC", "L6OK" und "L4OK":
                     - L7OK : Prüfung auf Schicht 7 bestanden.
                     - L7OKC: Prüfung auf Schicht 7 bedingt bestanden;
                               Server in den Zustand NOLB setzen.
                     - L6OK : Prüfung auf Schicht 6 bestanden.
                     - L4OK : Prüfung auf Schicht 4 bestanden.
                   Standardmäßig wird "L7OK" verwendet.

error-status <st>  ist optional und kann den Prüfstatus setzen, wenn bei
                   der Auswertung der expect-Regel ein Fehler auftritt.
                   Unterstützt werden "L7OKC", "L7RSP", "L7STS", "L6RSP"
                   und "L4CON":
                     - L7OKC: Prüfung auf Schicht 7 bedingt bestanden;
                               Server in den Zustand NOLB setzen.
                     - L7RSP: ungültige Antwort auf Schicht 7; Protokollfehler.
                     - L7STS: Antwortfehler auf Schicht 7, etwa HTTP 5xx.
                     - L6RSP: ungültige Antwort auf Schicht 6; Protokollfehler.
                     - L4CON: Verbindungsproblem auf Schicht 1-4.
                   Standardmäßig wird "L7RSP" verwendet.

tout-status <st>   ist optional und kann den Prüfstatus setzen, wenn bei
                   der Auswertung der expect-Regel eine Zeitüberschreitung
                   auftritt. Unterstützt werden "L7TOUT", "L6TOUT" und
                   "L4TOUT":
                     - L7TOUT: Zeitüberschreitung auf Schicht 7 (HTTP/SMTP).
                     - L6TOUT: Zeitüberschreitung auf Schicht 6 (SSL).
                     - L4TOUT: Zeitüberschreitung auf Schicht 1-4.
                   Standardmäßig wird "L7TOUT" verwendet.

on-success <fmt>   ist optional und kann die protokollierte Informationsmeldung
                   anpassen, wenn die expect-Regel erfolgreich ausgewertet
                   wird und die letzte Regel im tcp-check-Regelsatz ist.
                   <fmt> ist eine Zeichenfolge im benutzerdefinierten
                   Protokollformat (siehe Abschnitt 8.2.6).

on-error <fmt>     ist optional und kann die protokollierte Informationsmeldung
                   anpassen, wenn bei der Auswertung der expect-Regel ein
                   Fehler auftritt. <fmt> ist eine Zeichenfolge im
                   benutzerdefinierten Protokollformat (siehe Abschnitt 8.2.6).

status-code <expr> ist optional und kann den bei Erfolg oder Fehler im
                   Protokoll ausgegebenen Prüfstatuscode setzen. <expr> ist
                   ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
                   gefolgt von Konvertern.

<match>   ist ein Schlüsselwort, das die Suche nach einem bestimmten Muster
          in der Antwort festlegt. Möglich sind "status", "rstatus", "hdr",
          "fhdr", "string" und "rstring". Dem Schlüsselwort kann ein
          Ausrufezeichen ("!") vorangestellt werden, um den Vergleich zu
          negieren. Zwischen Ausrufezeichen und Schlüsselwort sind Leerzeichen
          zulässig. Weitere Einzelheiten zu den unterstützten Schlüsselwörtern
          stehen unten.

<pattern> ist das gesuchte Muster. Es kann eine Zeichenfolge, ein regulärer
          Ausdruck oder ein komplexeres Muster mit mehreren Argumenten sein.
          Enthält ein Zeichenfolgenmuster Leerzeichen, müssen diese mit dem
          üblichen umgekehrten Schrägstrich ('\') maskiert werden.
```

Standardmäßig betrachtet "option httpchk" die Antwortstatuscodes 2xx und 3xx als gültig und alle anderen als ungültig. Wenn "http-check expect" verwendet wird, definiert es, was als gültig oder ungültig gilt. In einem Backend ist nur eine einzige "http-check"-Anweisung zulässig. Wenn ein Server nicht antwortet oder eine Zeitüberschreitung auftritt, schlägt die Prüfung selbstverständlich fehl. Die verfügbaren Musterabgleiche sind:

```text
status <codes>:  prüft die Statuscodes, die beim Einlesen der Zeichenfolge
                  <codes> ermittelt werden. Sie muss eine durch Kommas getrennte
                  Liste von Statuscodes oder Codebereichen sein. Eine
                  Health-Check-Antwort gilt als gültig, wenn ihr Statuscode
                  einem Code entspricht oder in einem Bereich der Liste liegt.
                  Steht vor dem Schlüsselwort "status" ein "!", gilt die
                  Antwort bei übereinstimmendem Statuscode als ungültig.

rstatus <regex>: prüft den HTTP-Statuscode mit einem regulären Ausdruck.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Statuscode
                  dem Ausdruck entspricht. Steht vor dem Schlüsselwort
                  "rstatus" ein "!", gilt die Antwort bei übereinstimmendem
                  Statuscode als ungültig. Dies dient meist dazu, mehrere
                  Codes zu prüfen.

hdr  { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  prüft das angegebene Headermuster an den HTTP-Antwortheadern.
                  Das Namensmuster ist zwingend erforderlich, das Wertmuster
                  hingegen optional. Ohne Wertmuster wird nur geprüft, ob
                  der Header vorhanden ist. <meth> ist die Vergleichsmethode
                  für Headername oder Headerwert. Unterstützt werden "str"
                  (exakter Vergleich), "beg" (Präfixvergleich), "end"
                  (Suffixvergleich), "sub" (Teilzeichenfolgenvergleich) und
                  "reg" (Regex-Vergleich). Ohne Angabe erfolgt ein exakter
                  Vergleich. Mit dem Parameter "name-lf" wird <name> als
                  Zeichenfolge im benutzerdefinierten Protokollformat
                  ausgewertet (siehe Abschnitt 8.2.6). Mit "value-lf" wird
                  <value> als Zeichenfolge im Protokollformat ausgewertet.
                  Diese Parameter können nicht mit der Regex-Vergleichsmethode
                  verwendet werden. Der Headerwert wird als durch Kommas
                  getrennte Liste behandelt. Beim Vergleich der Headernamen
                  wird nicht zwischen Groß- und Kleinschreibung unterschieden.

fhdr { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  prüft das angegebene Muster für einen vollständigen Header
                  an den HTTP-Antwortheadern. Es verhält sich genau wie "hdr",
                  prüft aber den vollständigen Headerwert; Kommas gelten
                  nicht als Trennzeichen.

string <string>: prüft, ob die exakte Zeichenfolge im HTTP-Antwortkörper vorkommt.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Körper
                  diese exakte Zeichenfolge enthält. Steht vor dem Schlüsselwort
                  "string" ein "!", gilt die Antwort als ungültig, wenn
                  ihr Körper diese Zeichenfolge enthält. Damit lässt sich
                  beispielsweise ein zwingend erforderliches Wort am Ende
                  einer dynamischen Seite suchen oder ein Fehler erkennen,
                  wenn eine bestimmte Fehlermeldung auf der Prüfseite erscheint,
                  etwa ein Stacktrace.

rstring <regex>: prüft den HTTP-Antwortkörper mit einem regulären Ausdruck.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Körper
                  diesem Ausdruck entspricht. Steht vor dem Schlüsselwort
                  "rstring" ein "!", gilt die Antwort als ungültig, wenn
                  ihr Körper dem Ausdruck entspricht. Damit lässt sich
                  beispielsweise ein zwingend erforderliches Wort am Ende
                  einer dynamischen Seite suchen oder ein Fehler erkennen,
                  wenn eine bestimmte Fehlermeldung auf der Prüfseite erscheint,
                  etwa ein Stacktrace.

string-lf <fmt>: prüft, ob eine Zeichenfolge im benutzerdefinierten Protokollformat
                  (siehe Abschnitt 8.2.6) im HTTP-Antwortkörper vorkommt.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Körper
                  die Zeichenfolge enthält, die aus der Auswertung von <fmt>
                  nach den Regeln für Protokollformate entsteht. Mit einem
                  vorangestellten "!" gilt die Antwort als ungültig, wenn
                  ihr Körper die Zeichenfolge enthält.
```

Es ist wichtig zu beachten, dass die Antworten auf eine bestimmte Größe begrenzt werden, die durch die globale Option "tune.bufsize" festgelegt ist, die standardmäßig 16384 Bytes beträgt. Daher enthalten zu große Antworten bei Verwendung von "string" oder "rstring" möglicherweise nicht das erforderliche Muster. Falls eine große Antwort unbedingt erforderlich ist, kann die Standardmaximalgröße durch Setzen der globalen Variablen geändert werden. Es ist jedoch ratsam, sich daran zu erinnern, dass die Analyse sehr großer Antworten CPU-Zyklen verschwenden kann, insbesondere wenn reguläre Ausdrücke verwendet werden, und dass es immer besser ist, die Prüfungen auf kleinere Ressourcen zu konzentrieren.

In einer http-check-Regelsatz kann die letzte expect-Regel implizit sein. Wenn nach der letzten "http-check send"-Anweisung keine expect-Regel angegeben ist, wird eine implizite expect-Regel definiert, die auf Statuscodes 2xx oder 3xx prüft. Das bedeutet, diese Regel ist auch dann definiert, wenn überhaupt keine "http-check"-Regel vorhanden ist, wenn nur "option httpchk" gesetzt ist.

Wenn "http-check expect" mit "http-check disable-on-404" kombiniert wird, hat schließlich die letztere Direktive Vorrang, wenn der Server mit 404 antwortet.

Beispiele:

```shell
# only accept status 200 as valid
http-check expect status 200,201,300-310

# be sure a sessid coookie is set
http-check expect hdr name "set-cookie" value -m beg "sessid="

# consider SQL errors as errors
http-check expect ! string SQL\ Error

# consider status 5xx only as errors
http-check expect ! rstatus ^5

# check that we have a correct hexadecimal tag before /html
http-check expect rstring <!--tag:[0-9a-f]*--></html>
```

Siehe auch: "option httpchk", "http-check connect", "http-check disable-on-404" und "http-check send".

<a id="entry-4-2-http-check-send"></a>

**`http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]`**

```haproxy
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
```

Der bei HTTP-Health-Checks gesendeten Anfrage eine optionale Liste von Headern und/oder einen Nachrichtenkörper hinzufügen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

meth <method>  ist die optionale HTTP-Methode für die Anfragen. Ohne Angabe
               wird "OPTIONS" verwendet, da diese Methode meist wenig
               Verarbeitung auf dem Server erfordert und leicht aus
               Protokollen herauszufiltern ist. Jede Methode kann verwendet
               werden; vom Erfinden nicht standardisierter Methoden wird
               jedoch abgeraten.

uri <uri>      ist optional und setzt die in HTTP-Anfragen verwendete URI
               auf die Zeichenfolge <uri>. Der Standardwert ist "/", der
               auf fast jedem Server standardmäßig erreichbar ist. Er kann
               durch jede andere URI ersetzt werden. Abfragezeichenfolgen
               sind zulässig.

uri-lf <fmt>   ist optional und setzt die in HTTP-Anfragen verwendete URI
               anhand des benutzerdefinierten Protokollformats <fmt>
               (siehe Abschnitt 8.2.6). Der Standardwert ist "/", der auf
               fast jedem Server standardmäßig erreichbar ist. Er kann
               durch jede andere URI ersetzt werden. Abfragezeichenfolgen
               sind zulässig.

ver <version>  ist die optionale Zeichenfolge der HTTP-Version. Der Standard
               ist "HTTP/1.0". Manche Server verhalten sich mit HTTP 1.0
               jedoch fehlerhaft; dann kann eine Umstellung auf HTTP/1.1
               helfen. Das Feld Host ist bei HTTP/1.1 zwingend erforderlich;
               es mit dem Argument "hdr" hinzufügen.

hdr <name> <fmt>  fügt das HTTP-Headerfeld mit dem Namen <name> hinzu.
                  Sein Wert wird durch <fmt> nach den in Abschnitt 8.2.6
                  beschriebenen Regeln für benutzerdefinierte Protokollformate
                  bestimmt.

body <string>  fügt der bei HTTP Health Checks gesendeten Anfrage den durch
               <string> festgelegten Körper hinzu. Ist er definiert, wird
               der Header "Content-Length" der Anfrage automatisch hinzugefügt.

body-lf <fmt>  fügt der bei HTTP Health Checks gesendeten Anfrage den durch
               das benutzerdefinierte Protokollformat <fmt> festgelegten Körper
               hinzu (siehe Abschnitt 8.2.6). Ist er definiert, wird der
               Header "Content-Length" der Anfrage automatisch hinzugefügt.
```

Neben der Anfragezeile, die durch die Anweisung "option httpchk" definiert wird, ist dies die gültige Methode, um einige Header und optional einen Nachrichtenkörper zur Anfrage hinzuzufügen, die während HTTP-Health-Checks gesendet wird. Wenn ein Nachrichtenkörper definiert ist, wird automatisch der zugehörige "Content-Length"-Header hinzugefügt. Daher sollte dieser Header oder der "Transfer-encoding"-Header nicht in der Anfrage enthalten sein, die durch "http-check send" bereitgestellt wird. Falls vorhanden, wird er ignoriert. Der alte Trick, Header nach der Versionszeichenkette in der "option httpchk"-Zeile hinzuzufügen, ist nun veraltet.

Außerdem unterstützt "http-check send" kein HTTP-Keep-Alive. Beachten Sie, dass automatisch ein "Connection: close"-Header angehängt wird, es sei denn, ein Connection-Header wurde bereits über einen hdr-Eintrag konfiguriert.

Beachten Sie außerdem, dass der Host-Header und der Authority-Teil der Anfrage, wenn beide definiert sind, automatisch synchronisiert werden. Das bedeutet, wenn beim Senden der HTTP-Anfrage ein Host-Header eingefügt wird, wird der Authority-Teil der Anfrage entsprechend aktualisiert. Seien Sie daher nicht überrascht, wenn der Host-Header-Wert den konfigurierten Authority-Teil der Anfrage überschreibt.

Beachten Sie außerdem, dass derzeit kein Host-Header automatisch in HTTP/1.1 oder höheren Anfragen hinzugefügt wird. Sie sollten ihn explizit hinzufügen.

Siehe auch: "option httpchk", "http-check send-state" und "http-check expect".

<a id="entry-4-2-http-check-send-state"></a>

**`http-check send-state`**

```haproxy
http-check send-state
```

Die Ausgabe eines Zustandsheaders bei HTTP-Health-Checks aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Wenn diese Option aktiviert ist, sendet HAProxy systematisch einen speziellen Header "X-Haproxy-Server-State" mit einer Liste von Parametern, die jedem Server mitteilen, wie er von HAProxy wahrgenommen wird. Dies kann beispielsweise dann nützlich sein, wenn ein Server ohne Zugriff auf HAProxy verändert wird und der Betreiber wissen möchte, ob HAProxy ihn weiterhin als aktiv erkennt oder ob der Server der letzte in einer Farm ist.

Der Header besteht aus durch Semikolons getrennten Feldern, wobei das erste ein Wort ("UP", "DOWN", "NOLB") ist, möglicherweise gefolgt von der Anzahl gültiger Prüfungen im Verhältnis zur insgesamt für den Zustandswechsel erforderlichen Anzahl, wie in der Statistikoberfläche. Die folgenden Felder haben die Form "`<variable>`=`<value>`" und geben in beliebiger Reihenfolge einige Werte an, die in der Statistikoberfläche verfügbar sind: – eine Variable "address", die die Adresse des Backend-Servers enthält. Dies entspricht dem `<address>`-Feld in der Serverdeklaration. Bei Unix-Domain-Sockets wird "unix" angezeigt.

    -  eine Variable "port", die den Port des Backend-Servers enthält. Dies entspricht dem `<port>`-Feld in der Serverdeklaration. Bei Unix-Domain-Sockets wird "unix" angezeigt.

    -  eine Variable "name", die den Namen des Backends gefolgt von einem Schrägstrich ("/") und dem Namen des Servers enthält. Dies kann verwendet werden, wenn ein Server in mehreren Backends überprüft wird.

    -  eine Variable "node", die den Namen des HAProxy-Knotens enthält, wie in der globalen "node"-Variablen festgelegt, andernfalls den Hostnamen des Systems, falls nicht angegeben.

    -  eine Variable "weight", die das Gewicht des Servers, einen Schrägstrich ("/") und das Gesamtgewicht der Farm (wobei nur verwendbare Server gezählt werden) enthält. Dies hilft zu erkennen, ob andere Server zur Lastverteilung zur Verfügung stehen, wenn dieser ausfällt.

    -  eine Variable "scur", die die aktuelle Anzahl an gleichzeitigen Verbindungen auf dem Server, gefolgt von einem Schrägstrich ("/") und der Gesamtanzahl an Verbindungen auf allen Servern des gleichen Backends enthält.

    -  eine Variable "qcur", die die aktuelle Anzahl an Anfragen in der Warteschlange des Servers enthält.

Beispiel für einen vom Anwendungsserver empfangenen Header:

```shell
>>>  X-Haproxy-Server-State: UP 2/3; name=bck/srv2; node=lb1; weight=1/2; \
       scur=13/22; qcur=0
```

Siehe auch: "option httpchk", "http-check disable-on-404" und "http-check send".

<a id="entry-4-2-http-check-set-var"></a>

**`http-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Diese Operation legt den Inhalt einer Variablen fest. Die Variable wird inline deklariert.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<var-name>   Der Name der Variablen. Nur die Geltungsbereiche "proc", "sess"
             und "check" sind möglich. Einzelheiten zu Variablen stehen in
             Abschnitt 2.8.

 <cond>      Eine Menge von Bedingungen, die alle erfüllt sein müssen, damit
             die Variable tatsächlich gesetzt wird (etwa "ifnotempty", "ifgt"
             usw.). Die vollständige Liste möglicher Bedingungen steht in
             der Beschreibung des Konverters set-var.

 <expr>      Ein Sample-Abruf-Ausdruck, gegebenenfalls gefolgt von Konvertern.

 <fmt>       Der Wert als benutzerdefiniertes Protokollformat (siehe
             benutzerdefinierte Protokollformate in Abschnitt 8.2.6).
```

Beispiele:

```text
http-check set-var(check.port) int(1234)
http-check set-var-fmt(check.port) "name=%H"

```

<a id="entry-4-2-http-check-unset-var"></a>

**`http-check unset-var(<var-name>)`**

```haproxy
http-check unset-var(<var-name>)
```

Eine Referenz auf eine Variable innerhalb ihres Gültigkeitsbereichs freigeben.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<var-name>   Der Name der Variablen. Nur die Geltungsbereiche "proc", "sess"
             und "check" sind möglich. Einzelheiten zu Variablen stehen in
             Abschnitt 2.8.
```

Beispiele:

```text
http-check unset-var(check.port)

```

<a id="entry-4-2-http-error-status"></a>

**`http-error status <code> [content-type <type>]`**

```haproxy
http-error status <code> [content-type <type>]
           [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

               file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
           [ hdr `<name>` `<fmt>` ]*

Eine benutzerdefinierte Fehlermeldung festlegen, die anstelle der von HAProxy erzeugten Fehler verwendet wird.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
status <code>        ist der HTTP-Statuscode und muss angegeben werden.
                     HAProxy kann derzeit die Codes 200, 400, 401, 403,
                     404, 405, 407, 408, 410, 413, 414, 425, 429, 431,
                     500, 501, 502, 503 und 504 erzeugen.

content-type <type>  ist der Inhaltstyp der Antwort, etwa "text/plain".
                     Ist eine errorfile konfiguriert oder sind die Nutzdaten
                     leer, wird dieser Parameter ignoriert und sollte
                     weggelassen werden. Andernfalls muss er definiert sein.

default-errorfiles   Setzt die zuvor für den aktuellen Proxy definierte
                     Fehlermeldung für den Status <code> zurück. Bei einem
                     Backend wird die Fehlermeldung des Frontends verwendet,
                     sofern definiert. Bei einem Frontend wird die
                     Standardfehlermeldung verwendet.

errorfile <file>     bezeichnet eine Datei mit der vollständigen HTTP-Antwort.
                     Es wird empfohlen, dem Dateinamen wie üblich ".http"
                     anzuhängen, damit die Antwort nicht mit HTML-Fehlerseiten
                     verwechselt wird, und absolute Pfade zu verwenden, da
                     Dateien vor einem möglichen chroot eingelesen werden.

errorfiles <name>    bezeichnet den http-errors-Abschnitt, aus dem die
                     Fehlermeldung mit dem Statuscode <code> importiert wird.
                     Wird keine solche Meldung gefunden, werden die
                     Fehlermeldungen des Proxys berücksichtigt.

file <file>          gibt die Datei für die Antwortnutzdaten an. Ist die Datei
                     nicht leer, muss ihr Inhaltstyp als Argument von
                     "content-type" gesetzt werden; andernfalls wird jedes
                     "content-type"-Argument ignoriert. <file> wird als
                     unverarbeitete Zeichenfolge behandelt.

string <str>         gibt die unverarbeitete Zeichenfolge für die Antwortnutzdaten
                     an. Der Inhaltstyp muss immer als Argument von
                     "content-type" gesetzt werden.

lf-file <file>       gibt die Datei für die Antwortnutzdaten an. Ist die Datei
                     nicht leer, muss ihr Inhaltstyp als Argument von
                     "content-type" gesetzt werden; andernfalls wird jedes
                     "content-type"-Argument ignoriert. <file> wird als
                     benutzerdefiniertes Protokollformat ausgewertet
                     (siehe Abschnitt 8.2.6).

lf-string <str>      gibt die Zeichenfolge im Protokollformat für die
                     Antwortnutzdaten an. Der Inhaltstyp muss immer als
                     Argument von "content-type" gesetzt werden.

hdr <name> <fmt>     fügt der Antwort das HTTP-Headerfeld mit dem Namen
                     <name> hinzu. Sein Wert wird durch <fmt> nach den
                     Regeln für benutzerdefinierte Protokollformate bestimmt
                     (siehe Abschnitt 8.2.6). Bei Verwendung einer errorfile
                     wird dieser Parameter ignoriert.
```

Diese Direktive kann anstelle von "errorfile" verwendet werden, um eine benutzerdefinierte Fehlermeldung festzulegen. Wie die Direktive "errorfile" gilt sie für Fehler, die HAProxy erkennt und zurückgibt. Ist eine Fehlerdatei definiert, wird sie beim Start von HAProxy eingelesen und muss den HTTP-Standards entsprechen. Die erzeugte Antwort darf die konfigurierte Puffergröße (BUFFSIZE) nicht überschreiten, da andernfalls ein interner Fehler zurückgegeben wird. Wenn Sie diese Fehler mit http-after-response-Regeln umschreiben möchten, sollte schließlich der reservierte Pufferbereich verfügbar sein (siehe "tune.maxrewrite").

Die Dateien werden zusammen mit der Konfiguration gelesen und im Speicher gehalten. Daher werden die Fehler auch dann weiterhin zurückgegeben, wenn der Prozess in einer chroot-Umgebung läuft; Änderungen an den Dateien werden während der Laufzeit des Prozesses nicht berücksichtigt.

Hinweis: Fehler vom Typ 400/408/500, die früh beim Parsen der Anfrage auftreten, werden auf einer niedrigeren Ebene vom Multiplexer behandelt. Auf dieser Ebene wird keine benutzerdefinierte Formatierung unterstützt. Daher werden nur statische Fehlermeldungen unterstützt, die mit der Direktive "errorfile" definiert sind. Diese Einschränkung besteht jedoch nur beim Parsen der Anfrageheader oder zwischen zwei Transaktionen.

Siehe auch: "errorfile", "errorfiles", "errorloc", "errorloc302", "errorloc303" und [Abschnitt 12.4](/de/haproxy/other-sections/#section-12-4) zu http-errors.

<a id="entry-4-2-http-request"></a>

**`http-request <action> [options...] [ { if | unless } <condition> ]`**

```haproxy
http-request <action> [options...] [ { if | unless } <condition> ]
```

Zugriffskontrolle für Anfragen auf Schicht 7

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Die Anweisung http-request definiert Regeln für die Verarbeitung auf Schicht 7. Die Regeln werden in der Reihenfolge ihrer Deklaration ausgewertet, wenn sie in einem Abschnitt frontend, listen oder backend vorkommen. Auf jede Regel kann optional eine ACL-basierte Bedingung folgen; dann wird die Regel nur ausgewertet, wenn diese Bedingung wahr ist.

Die Bedingung wird unmittelbar vor der Ausführung der Aktion ausgewertet, und die Aktion wird genau einmal ausgeführt. Daher ist es unproblematisch, wenn eine Aktion ein Element ändert, das in der Bedingung geprüft wird. Das bedeutet auch, dass mehrere Aktionen dieselbe Bedingung verwenden können: Die erste Aktion, die das Ergebnis der Bedingung ändert, reicht dann aus, um die übrigen Aktionen implizit zu deaktivieren. Dies wird beispielsweise verwendet, wenn einer leeren Variablen ein Wert aus verschiedenen Quellen zugewiesen werden soll. Die Anzahl der "http-request"-Anweisungen pro Instanz ist nicht begrenzt.

Das erste Schlüsselwort nach "http-request" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "HTTP Req").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Beispiel:

```text
acl nagios src 192.168.129.3
acl local_net src 192.168.0.0/16
acl auth_ok http_auth(L1)

http-request allow if nagios
http-request allow if local_net auth_ok
http-request auth realm Gimme if local_net auth_ok
http-request deny
```

Beispiel:

```text
acl key req.hdr(X-Add-Acl-Key) -m found
acl add path /addacl
acl del path /delacl

acl myhost hdr(Host) -f myhost.lst

http-request add-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key add
http-request del-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key del
```

Beispiel:

```text
acl value  req.hdr(X-Value) -m found
acl setmap path /setmap
acl delmap path /delmap

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-request set-map(map.lst) %[src] %[req.hdr(X-Value)] if setmap value
http-request del-map(map.lst) %[src]                     if delmap
```

Siehe auch: "stats http-request", [Abschnitt 12.2](/de/haproxy/other-sections/#section-12-2) zu Benutzerlisten und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-http-response"></a>

**`http-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-response <action> <options...> [ { if | unless } <condition> ]
```

Zugriffskontrolle für Antworten auf Schicht 7

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Die Anweisung http-response definiert Regeln für die Verarbeitung auf Schicht 7. Die Regeln werden in der Reihenfolge ihrer Deklaration ausgewertet, wenn sie in einem Abschnitt frontend, listen oder backend vorkommen. Da sie auf Antworten angewendet werden, werden zuerst die Regeln des Backends und anschließend die des Frontends angewendet. Auf jede Regel kann optional eine ACL-basierte Bedingung folgen; dann wird die Regel nur ausgewertet, wenn diese Bedingung wahr ist.

Die Bedingung wird unmittelbar vor der Ausführung der Aktion ausgewertet, und die Aktion wird genau einmal ausgeführt. Daher ist es unproblematisch, wenn eine Aktion ein Element ändert, das in der Bedingung geprüft wird. Das bedeutet auch, dass mehrere Aktionen dieselbe Bedingung verwenden können: Die erste Aktion, die das Ergebnis der Bedingung ändert, reicht dann aus, um die übrigen Aktionen implizit zu deaktivieren. Dies wird beispielsweise verwendet, wenn einer leeren Variablen ein Wert aus verschiedenen Quellen zugewiesen werden soll. Die Anzahl der "http-response"-Anweisungen pro Instanz ist nicht begrenzt.

Das erste Schlüsselwort nach "http-response" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "HTTP Res").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Beispiel:

```text
acl key_acl res.hdr(X-Acl-Key) -m found

acl myhost hdr(Host) -f myhost.lst

http-response add-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
http-response del-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
```

Beispiel:

```text
acl value  res.hdr(X-Value) -m found

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-response set-map(map.lst) %[src] %[res.hdr(X-Value)] if value
http-response del-map(map.lst) %[src]                     if ! value
```

Siehe auch: "http-request", [Abschnitt 12.2](/de/haproxy/other-sections/#section-12-2) zu Benutzerlisten und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-http-reuse"></a>

**`http-reuse { never | safe | aggressive | always }`**

```haproxy
http-reuse { never | safe | aggressive | always }
```

Festlegen, wie inaktive HTTP-Verbindungen von mehreren Anfragen gemeinsam genutzt werden dürfen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Um den Aufwand für den Aufbau einer neuen Verbindung zu den Backend-Servern bei jeder HTTP-Anfrage zu vermeiden, versucht HAProxy, solche inaktiven Verbindungen nach ihrer Verwendung offenzuhalten. Diese Verbindungen gehören jeweils zu einem bestimmten Server und werden in einer als Pool bezeichneten Liste gespeichert. Innerhalb dieser Liste werden sie anhand gemeinsamer Schlüsseleigenschaften gruppiert. Bei nachfolgenden HTTP-Anfragen wird im zugehörigen Pool nach einer kompatiblen Verbindung mit identischen Eigenschaften gesucht. Diese Verbindung wird dann wiederverwendet, statt eine neue aufzubauen.

Mit dem Server-Schlüsselwort "pool-max-conn" lässt sich die Anzahl inaktiver Verbindungen begrenzen, die zu einem Server offengehalten werden. Nicht verwendete Verbindungen werden regelmäßig gemäß dem Intervall "pool-purge-delay" entfernt.

Anhand folgender Verbindungseigenschaften wird entschieden, ob eine inaktive Verbindung für eine bestimmte Anfrage wiederverwendet werden kann:

- Quell- und Zieladressen
- Proxy-Protokoll
- die Socket-Optionen TOS und mark
- der Verbindungsname, der durch das Ergebnis der Auswertung des Ausdrucks "pool-conn-name" bestimmt wird, sofern dieser vorhanden ist, andernfalls durch den Ausdruck "sni". Dessen Standardwert ist "req.hdr(host),field(1,:)"; er verwendet also das Feld "Host" aus dem Header der eingehenden Anfrage ohne Doppelpunkt und Portnummer.

In manchen Fällen finden aufgrund zusätzlicher Einschränkungen keine Verbindungssuche oder Wiederverwendung statt. Dies wird durch die Wiederverwendungsstrategie bestimmt, die als Argument des Schlüsselworts angegeben wird:

    - "never" : Inaktive Verbindungen werden niemals von mehreren Sitzungen
                 gemeinsam genutzt. Dieser Modus kann erzwungen werden, um eine
                 aus einem defaults-Abschnitt geerbte andere Strategie aufzuheben
                 oder um Fehler zu untersuchen. Wenn beispielsweise eine alte,
                 fehlerhafte Anwendung annimmt, dass mehrere Anfragen über
                 dieselbe Verbindung vom selben Client stammen, und sich die
                 Anwendung nicht korrigieren lässt, kann es sinnvoll sein, die
                 gemeinsame Nutzung von Verbindungen in einem einzelnen Backend
                 zu deaktivieren. Ein Beispiel wäre eine alte HAProxy-Version,
                 die im Tunnelmodus Cookies einfügt und nach der ersten Anfrage
                 keine weiteren Anfragen prüft.

    - "safe"  : Dies ist die Standardstrategie und die empfohlene Strategie.
                 Die erste Anfrage einer Sitzung wird immer über eine eigene
                 Verbindung gesendet. Nur nachfolgende Anfragen dürfen über
                 andere bestehende Verbindungen verteilt werden. Damit ist
                 sichergestellt, dass der Browser die Anfrage unbemerkt erneut
                 versuchen kann, falls der Server die Verbindung während des
                 Sendens der Anfrage schließt. Da dies genau dem gewöhnlichen
                 Keepalive-Verhalten entspricht, sollte es keine Nebenwirkungen
                 geben. Verbindungen mit Protokollen, die von Head-of-Line-
                 Blockierung betroffen sind (Backends mit h2 oder fcgi), werden
                 außerdem gesondert behandelt. Sobald mindestens ein Stream
                 verarbeitet wird, ist die verwendete Verbindung für Streams
                 derselben Sitzung reserviert. Werden keine Streams mehr
                 verarbeitet, wird die Verbindung freigegeben und kann
                 wiederverwendet werden.

    - "aggressive": Dieser Modus kann in Webservice-Umgebungen nützlich sein,
                 in denen nicht unbedingt alle Server bekannt sind und es von
                 Vorteil wäre, die meisten ersten Anfragen über bestehende
                 Verbindungen zu senden. Erste Anfragen werden dabei nur über
                 bestehende Verbindungen gesendet, die bereits mindestens einmal
                 wiederverwendet wurden. Damit ist nachgewiesen, dass der Server
                 die Wiederverwendung von Verbindungen korrekt unterstützt.
                 Dieser Modus sollte nur verwendet werden, wenn sichergestellt
                 ist, dass der Client gelegentlich eine fehlgeschlagene Anfrage
                 wiederholen kann, und der Vorteil der aggressiven
                 Wiederverwendung die Nachteile seltener Verbindungsfehler
                 deutlich überwiegt.

    - "always": Dieser Modus wird nur empfohlen, wenn bekannt ist, dass der
                 Pfad zum Server bestehende Verbindungen niemals kurz nach
                 ihrer Freigabe unterbricht. Er erlaubt, die erste Anfrage einer
                 Sitzung über eine bestehende Verbindung zu senden. Gegenüber
                 der Strategie "safe" kann dies die Leistung erheblich steigern,
                 wenn das Backend eine Cache-Farm ist: Solche Komponenten zeigen
                 üblicherweise ein gleichmäßiges Verhalten und profitieren von
                 der gemeinsamen Verbindungsnutzung. Es wird empfohlen, die
                 Zeitüberschreitung "http-keep-alive" in diesem Modus niedrig zu
                 halten, damit keine toten Verbindungen weiter verwendbar
                 bleiben. Meist ergeben sich dieselben Leistungsgewinne wie mit
                 "aggressive", jedoch mit höheren Risiken. Dieser Modus sollte
                 nur verwendet werden, wenn er die Situation gegenüber
                 "aggressive" verbessert.

Verbindungen mit bestimmten fehlerhaften, auf der Verbindung beruhenden Authentifizierungsschemata wie NTLM werden nach Möglichkeit als privat markiert und niemals gemeinsam genutzt. Dies gilt jedoch nicht bei einem Protokoll mit Multiplexing-Unterstützung und einer Wiederverwendungsstufe oberhalb der Standardstrategie "safe": In diesem Fall verhindert nichts, dass die Verbindung bereits gemeinsam genutzt wird.

Ob eine inaktive Verbindung nach der Verarbeitung offengehalten oder geschlossen wird, hängt außerdem von "tune.pool-low-fd-ratio" (Standard: 20%) und "tune.pool-high-fd-ratio" (Standard: 25%) ab. Diese Werte geben den Anteil der insgesamt verfügbaren Dateideskriptoren an, der von inaktiven Verbindungen belegt wird. Oberhalb des ersten Grenzwerts hält haproxy Verbindungen nach einer Antwort nicht mehr offen; oberhalb des zweiten beendet es inaktive Verbindungen aktiv. Konfigurationen mit einem sehr hohen Anteil inaktiver Verbindungen können eine geringere Wiederverwendungsrate aufweisen, weil zu wenige Verbindungen offenbleiben. Ursache kann ein zu niedriger globaler "maxconn"-Wert sein oder viel HTTP/2- beziehungsweise HTTP/3-Verkehr im Frontend (wenige Verbindungen) bei gleichzeitigen HTTP/1-Verbindungen im Backend. In diesem Fall kann es sinnvoll sein, diese Schwellenwerte anzupassen oder einfach den globalen "maxconn"-Wert zu erhöhen.

In seltenen Fällen wird der Hostname zur Unterscheidung ausgehender TLS-Verbindungen verwendet, etwa bei einem Forward Proxy, bei dem sich die meisten Anfragen an unterschiedliche Hosts richten. Dann ist die Wiederverwendungsrate sehr niedrig, und selten verwendete Verbindungen werden automatisch entfernt, bevor sie erneut verwendet werden können. Der Mechanismus misst nämlich fortlaufend die durchschnittliche Anzahl von Verbindungen, die benötigt wird, um den Dienst ohne Erschöpfung der Ressourcen bereitzustellen. In solchen Situationen kann ein Wert für "pool-low-conn" nahe der erwarteten durchschnittlichen Anzahl inaktiver Verbindungen helfen, mehr Verbindungen zu erhalten: Threads werden dadurch dazu angehalten, eigene Verbindungen aufzubauen, statt Verbindungen anderer Threads zu übernehmen und so den Pool verfügbarer Verbindungen zu verkleinern.

Wenn ein lokal gehosteter Server mehrere Websites betreibt und ein einziges Zertifikat mit mehreren Hostnamen oder Platzhaltern verwendet, kann es wirksamer sein, einfach "no-sni-auto" in der "server"-Zeile zu verwenden. Dadurch wird vermieden, eine Verbindung für einen einzelnen Host-Namen zu reservieren, und die Wiederverwendungsrate steigt erheblich. Manche Server führen jedoch übermäßig strenge Prüfungen zwischen Host und SNI durch und weisen deshalb nachfolgende Anfragen ab. Diese Option muss daher vorab überprüft werden. Das Standardverhalten ("sni-auto") funktioniert auch mit solchen Servern sicher.

Wenn Thread-Gruppen ausdrücklich aktiviert sind, können inaktive Verbindungen nur zwischen Threads derselben Gruppe verwendet werden. Daher kann eine ungleichmäßige Lastverteilung zwischen den Gruppen dazu führen, dass mehr inaktive Verbindungen benötigt werden und die Wiederverwendungsrate sinkt. In diesem Fall kann dieselbe Lösung angewendet werden: den globalen "maxconn"-Wert oder die Pool-Anteile erhöhen.

Siehe auch: "option http-keep-alive", "pool-conn-name", "pool-max-conn", "pool-purge-delay", "server
maxconn", "sni", "thread-groups", "tune.pool-high-fd-ratio", "tune.pool-low-fd-ratio"

<a id="entry-4-2-http-send-name-header"></a>

**`http-send-name-header [<header>]`**

```haproxy
http-send-name-header [<header>]
```

Den Servernamen in eine Anfrage einfügen. Dabei die durch `<header>` angegebene Headerzeichenkette verwenden

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<header>  Die Header-Zeichenfolge, mit der der Servername gesendet wird.
```

Die Anweisung "http-send-name-header" setzt das Headerfeld mit dem Namen `<header>` unmittelbar vor dem Senden der Anfrage auf den Namen des Zielservers. Alle vorhandenen Vorkommen dieses Headers werden entfernt. Bei Wiederholungsversuchen und erneuten Zuweisungen wird das Headerfeld aktualisiert, sodass es stets den Server angibt, zu dem gerade eine Verbindung versucht wird. Da dieser Header erst sehr spät beim Verbindungsaufbau geändert wird, kann dies unerwartete Auswirkungen auf bereits geänderte Header haben. Wird die Anweisung beispielsweise mit transportbezogenen Headern wie connection, content-length oder transfer-encoding verwendet, werden wahrscheinlich ungültige Anfragen an den Server gesendet. Daher sind folgende Headernamen verboten: host, content-length, transfer-encoding und connection.

Siehe auch: "server"

<a id="entry-4-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

Einem Proxy eine dauerhafte ID zuweisen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Argumente: keine

Eine dauerhafte ID für den Proxy festlegen. Diese ID muss eindeutig und positiv sein. Wird sie nicht festgelegt, wird automatisch eine unbenutzte ID zugewiesen. Aus historischen Gründen wird der Wert 1 nur bei ausdrücklicher Angabe verwendet. Der niedrigste automatisch zugewiesene Wert ist daher 2. Diese ID wird derzeit nur in den Statistiken zurückgegeben.

<a id="entry-4-2-ignore-persist"></a>

**`ignore-persist { if | unless } <condition>`**

```haproxy
ignore-persist { if | unless } <condition>
```

Eine Bedingung zum Ignorieren der Sitzungsbindung deklarieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Wenn die cookiebasierte Sitzungsbindung aktiviert ist, gilt diese standardmäßig uneingeschränkt für jede Anfrage, die das Cookie enthält, vorausgesetzt, der Zielserver ist verfügbar und läuft.

Mit der Anweisung "ignore-persist" können verschiedene ACL-basierte Bedingungen deklariert werden. Sind sie erfüllt, ignoriert eine Anfrage die Sitzungsbindung. Dies ist gelegentlich für die Lastverteilung von Anfragen nach statischen Dateien nützlich, die häufig keine Sitzungsbindung benötigen. Auch für einen bestimmten User-Agent, etwa manche Webcrawler, lässt sich die Sitzungsbindung damit vollständig deaktivieren.

Die Sitzungsbindung wird ignoriert, wenn eine "if"-Bedingung erfüllt ist oder eine "unless"-Bedingung nicht erfüllt ist.

Beispiel:

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
ignore-persist  if url_static
```

Siehe auch: "force-persist", "cookie" und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-load-server-state-from-file"></a>

**`load-server-state-from-file { global | local | none }`**

```haproxy
load-server-state-from-file { global | local | none }
```

Ein unterbrechungsfreies Neuladen von HAProxy ermöglichen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Diese Direktive verweist HAProxy auf eine Datei, in der die Serverzustände des zuvor laufenden Prozesses gespeichert wurden. So kann der neue Prozess beim Start vor der Verarbeitung von Datenverkehr die alten Zustände auf die Server anwenden, als hätte kein Neuladen stattgefunden. Die Direktive "load-server-state-from-file" legt fest, welche Datei HAProxy verwenden soll. Derzeit gibt es nur 2 Argumente: entweder das Laden von Zuständen verhindern oder Zustände aus einer Datei laden, die alle Backends und Server enthält. Die Zustandsdatei kann erzeugt werden, indem der Befehl "show servers state" über das Statistik-Socket ausgeführt und seine Ausgabe umgeleitet wird.

Das Dateiformat ist versioniert und sehr spezifisch. Erläuterungen enthält die Dokumentation des Befehls "show servers state" (Kapitel 9.3 des Verwaltungshandbuchs).

Argumente:

```text
global     Den Inhalt der Datei laden, auf die die globale Direktive
           "server-state-file" verweist.

local      Den Inhalt der Datei laden, auf die "server-state-file-name"
           verweist, sofern diese Direktive gesetzt ist. Andernfalls wird
           der Backend-Name als Dateiname verwendet.

none       Keine Zustandsinformationen für dieses Backend laden.
```

Hinweise: - Die IP-Adresse eines Servers bleibt beim Neuladen standardmäßig erhalten. Die Reihenfolge lässt sich jedoch mit der Servereinstellung "init-addr" ändern. Das bedeutet, dass eine zur Laufzeit über die CLI geänderte IP-Adresse erhalten bleibt und Änderungen am lokalen Resolver, etwa /etc/hosts, möglicherweise wirkungslos bleiben, wenn die Zustandsdatei verwendet wird.

    - Das Servergewicht wird aus dem zuvor laufenden Prozess übernommen,
      sofern es nicht zwischen der vorherigen und der neuen Konfigurationsdatei
      geändert wurde.

Beispiel: Minimale Konfiguration

      global
       stats socket /tmp/socket
       server-state-file /tmp/server_state

      defaults
       load-server-state-from-file global

      backend bk
       server s1 127.0.0.1:22 check weight 11
       server s2 127.0.0.1:22 check weight 12

Anschließend kann Folgendes ausgeführt werden:

```text
socat /tmp/socket - <<< "show servers state" > /tmp/server_state
```

Der Inhalt der Datei /tmp/server_state sähe dann etwa so aus:

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

Beispiel: Minimale Konfiguration

    global
     stats socket /tmp/socket
     server-state-base /etc/haproxy/states

    defaults
     load-server-state-from-file local

    backend bk
     server s1 127.0.0.1:22 check weight 11
     server s2 127.0.0.1:22 check weight 12

Anschließend kann Folgendes ausgeführt werden:

```text
socat /tmp/socket - <<< "show servers state bk" > /etc/haproxy/states/bk
```

Der Inhalt der Datei /etc/haproxy/states/bk sähe etwa so aus:

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

Siehe auch: "server-state-file", "server-state-file-name" und "show servers state"

<a id="entry-4-2-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [<level> [<minlevel>]]
no log
```

Die Protokollierung von Ereignissen und Datenverkehr pro Instanz aktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Präfix:

```text
no         sollte verwendet werden, wenn die Liste der Protokollziele
           geleert werden muss, etwa wenn die Standardliste nicht übernommen
           werden soll. Dieses Präfix erlaubt keine Argumente.
```

Argumente:

```text
global     sollte verwendet werden, wenn die Protokollierungsparameter der
           Instanz denen des global-Abschnitts entsprechen. Dies ist der
           häufigste Anwendungsfall. "global" ersetzt sämtliche log-Argumente
           durch die der Protokolleinträge im Abschnitt "global". Pro Instanz
           kann nur eine Anweisung "log global" verwendet werden; diese Form
           akzeptiert keine weiteren Parameter.

<target>   gibt das Ziel der Protokollnachrichten an. Das Format entspricht
           dem der Protokollziele im Abschnitt "global". Möglich sind:

           - Eine IPv4-Adresse, optional gefolgt von einem Doppelpunkt (':')
             und einem UDP-Port. Ohne Portangabe wird standardmäßig 514
             verwendet, der übliche syslog-Port.

           - Eine IPv6-Adresse, gefolgt von einem Doppelpunkt (':') und
             optional einem UDP-Port. Ohne Portangabe wird standardmäßig
             514 verwendet, der übliche syslog-Port.

           - Ein Dateisystempfad zu einem UNIX-Domain-Socket. Dabei sind
             chroot (der Pfad muss innerhalb des chroot erreichbar sein)
             und uid/gid (der Pfad muss entsprechend beschreibbar sein)
             zu berücksichtigen.

           - Eine Dateideskriptornummer in der Form "fd@<number>", die auf
             eine Pipe, ein Terminal oder einen Socket verweisen kann.
             Dabei werden ungepufferte Protokolle verwendet und pro
             Protokolleintrag ein writev()-Aufruf ausgeführt. Dies ist etwas
             aufwendig, für die meisten Lastprofile jedoch vertretbar.
             So gesendete Nachrichten werden nicht gekürzt, können aber
             verworfen werden; dann wird der Zähler DroppedLogs erhöht.
             writev() ist selbst bei Pipes für Nachrichten bis zur Größe
             PIPE_BUF atomar. POSIX empfiehlt hierfür mindestens 512;
             auf den meisten modernen Betriebssystemen sind es 4096 Byte.
             Größere Nachrichten können mit Nachrichten anderer Prozesse
             vermischt werden. Ausnahmsweise kann der Dateideskriptor zur
             Fehlersuche auch auf eine Datei verweisen. Dies verlangsamt
             HAProxy jedoch erheblich, da nicht blockierende Aufrufe ignoriert
             werden. Zudem lässt sich die Datei ohne Neustart des Prozesses
             weder leeren noch rotieren. Das konfigurierte syslog-Format
             bleibt erhalten, sodass die Ausgabe für einen TCP-syslog-Server
             geeignet ist. Siehe auch die Formate "short" und "raw" unten.

           - "stdout" / "stderr" als Aliase für "fd@1" bzw. "fd@2";
             siehe oben.

           - Ein Ringpuffer in der Form "ring@<name>". Dieser liegt im
             Arbeitsspeicher und ist über den CLI-Befehl "show events"
             erreichbar. Der Befehl listet auch vorhandene Ringpuffer und
             deren Größen auf. Diese Puffer gehen beim Neuladen oder Neustart
             verloren. Ergänzend eingesetzt können sie jedoch die
             Fehlerbehebung erleichtern, da Protokolle sofort verfügbar sind.
             Siehe Abschnitt 12.5 zu Ringpuffern.

           - Ein Protokoll-Backend in der Form "backend@<name>". Es sendet
             Protokollnachrichten an das entsprechende Backend, das anhand
             seiner Lastverteilungseinstellungen den richtigen Zielserver
             auswählt. Ein Protokoll-Backend ist ein backend-Abschnitt mit
             gesetztem "mode log" (weitere Informationen unter "mode").

           - Ein ausdrückliches Stream-Adresspräfix wie "tcp@", "tcp6@",
             "tcp4@" oder "uxst@" legt einen impliziten Ringpuffer mit
             einem Stream-Weiterleitungsserver für die angegebene Adresse an.

           Im Adressparameter können Umgebungsvariablen verwendet werden;
           siehe Abschnitt 2.3 zu Umgebungsvariablen.

<length>   ist eine optionale maximale Zeilenlänge. Längere Protokollzeilen
           werden vor dem Senden gekürzt, da syslog-Server unterschiedlich
           mit Zeilenlängen umgehen. Alle unterstützen den Standardwert 1024,
           manche verwerfen längere Zeilen jedoch einfach, während andere
           sie protokollieren. Unterstützt ein Server lange Zeilen, kann
           dieser Wert hier erhöht werden, um ihre Kürzung zu vermeiden.
           Verwirft ein Server lange Zeilen, ist es umgekehrt besser, sie
           vor dem Senden zu kürzen. Zulässig sind Werte von 80 bis
           einschließlich 65535. Der Standardwert 1024 eignet sich im
           Allgemeinen für alle üblichen Anwendungen. In besonderen Fällen
           mit langen erfassten Werten oder JSON-formatierten Protokollen
           können größere Werte nötig sein. Werden Anfrage-URIs gekürzt,
           muss möglicherweise auch "tune.http.logurilen" erhöht werden.

<ranges>   Eine durch Kommas getrennte Liste von Bereichen, die die in eine
           Stichprobe aufzunehmenden Protokolleinträge bestimmen. Dies dient
           zur Lastverteilung der an den Protokollserver gesendeten Einträge.
           Die Bereichsgrenzen dürfen nicht null sein; die Nummerierung
           beginnt bei 1. Die Größe bzw. Periode der Stichprobe in
           Protokolleinträgen muss mit <sample_size> festgelegt werden.

<sample_size>
           Die Stichprobengröße in Protokolleinträgen für die Verteilung
           der Protokollierungslast. Sie verteilt die Last der an den
           syslog-Server gesendeten Einträge. Die Größe muss mindestens
           dem Maximum der oberen Bereichsgrenzen entsprechen.
           Siehe auch den Parameter <ranges>.

<format> ist das Format zur Erzeugung von syslog-Nachrichten. Möglich sind:

  local     Entspricht dem syslog-Nachrichtenformat rfc3164, jedoch ohne
            Hostnamenfeld. Dies ist der Standard.
            Hinweis: Die Option "log-send-hostname" ändert den Standard
            in rfc3164.

  rfc3164   Das syslog-Nachrichtenformat RFC3164.
            (https://tools.ietf.org/html/rfc3164)

  rfc5424   Das syslog-Nachrichtenformat RFC5424.
            (https://tools.ietf.org/html/rfc5424)

  priority  Eine Nachricht, die nur Stufe und syslog-Facility in spitzen
            Klammern wie '<63>' enthält, gefolgt vom Text. PID, Datum,
            Uhrzeit, Prozessname und Systemname entfallen. Dieses Format
            ist für einen lokalen Protokollserver vorgesehen.

  short     Eine Nachricht, die nur eine Stufe in spitzen Klammern wie '<3>'
            enthält, gefolgt vom Text. PID, Datum, Uhrzeit, Prozessname und
            Systemname entfallen. Dieses Format ist für einen lokalen
            Protokollserver vorgesehen und mit dem systemd-Protokolldienst
            kompatibel.

  timed     Eine Nachricht, die nur eine Stufe in spitzen Klammern wie '<3>'
            enthält, gefolgt vom ISO-Datum und dem Text. PID, Prozessname
            und Systemname entfallen. Dieses Format ist für einen lokalen
            Protokollserver vorgesehen.

  iso       Eine Nachricht, die nur das ISO-Datum enthält, gefolgt vom Text.
            PID, Prozessname und Systemname entfallen. Dieses Format ist
            für einen lokalen Protokollserver vorgesehen.

  raw       Eine Nachricht, die nur den Text enthält. Stufe, PID, Datum,
            Uhrzeit, Prozessname und Systemname entfallen. Dieses Format
            ist für Container oder die Entwicklung vorgesehen, wo der
            Schweregrad nur vom verwendeten Dateideskriptor abhängt
            (stdout/stderr).

<prof>     Name des optionalen "log-profile"-Abschnitts, der bei der
           Protokollerstellung zum Überschreiben einiger Protokolloptionen
           berücksichtigt wird. Weitere Informationen unter
           "8.3.5. Protokollprofile".

<facility> muss eine der 24 standardmäßigen syslog-Facilities sein:

               kern   user   mail   daemon auth   syslog lpr    news
               uucp   cron   auth2  ftp    ntp    audit  alert  cron2
               local0 local1 local2 local3 local4 local5 local6 local7

           Bei den Formaten "short" und "raw" wird die Facility ignoriert,
           bleibt aber als Positionsfeld erforderlich. In diesem Fall wird
           "daemon" empfohlen, um die ausschließlich lokale Verwendung
           deutlich zu machen.

<level>    ist optional und filtert ausgehende Nachrichten. Standardmäßig
           werden alle Nachrichten gesendet. Bei Angabe einer Stufe werden
           nur Nachrichten mit mindestens diesem Schweregrad gesendet.
           Optional kann eine Mindeststufe angegeben werden. Ist sie gesetzt,
           werden Nachrichten mit einem höheren Schweregrad auf diese Stufe
           begrenzt. Damit lässt sich vermeiden, dass "emerg"-Nachrichten
           bei manchen syslog-Standardkonfigurationen auf allen Terminals
           erscheinen. Es gibt acht bekannte Stufen:

             emerg  alert  crit   err    warning notice info  debug
```

Das Frontend entscheidet, welche Informationen einer Verbindung protokolliert werden. Bei inhaltsabhängiger Umschaltung werden die Protokolleinträge des Backends ignoriert. Verbindungen werden auf der Stufe "info" protokolliert.

Die Protokolldeklarationen im Backend legen jedoch fest, wie und wo Änderungen des Serverstatus protokolliert werden. Die Stufe "notice" zeigt an, dass ein Server verfügbar wird; "warning" wird für Beendigungssignale und die endgültige Beendigung eines Dienstes verwendet; "alert" wird verwendet, wenn ein Server ausfällt.

Hinweis: Gemäß RFC3164 werden Meldungen vor der Ausgabe auf 1024 Bytes gekürzt.

Beispiel:

```text
log global
log stdout format short daemon          # send log to systemd
log stdout format raw daemon            # send everything to stdout
log stderr format raw daemon notice     # send important events to stderr
log 127.0.0.1:514 local0 notice         # only send important events
log tcp@127.0.0.1:514 local0 notice notice  # same but limit output
                                            # level and send in tcp
log "${LOCAL_SYSLOG}:514" local0 notice   # send to local server
```

<a id="entry-4-2-log-format"></a>

**`log-format <fmt>`**

```haproxy
log-format <fmt>
```

Die benutzerdefinierte Formatzeichenkette für die Protokollierung des Datenverkehrs festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Diese Direktive legt die Formatzeichenkette für alle Protokolleinträge fest, die durch Datenverkehr über das Frontend mit dieser Zeile entstehen. Wird die Direktive in einem defaults-Abschnitt verwendet, verwenden alle nachfolgenden Frontends dasselbe Protokollformat. [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschreibt benutzerdefinierte Formatzeichenketten für Protokolle ausführlich.

Es kann auch ein besonderes log-format definiert werden, das nur bei Verbindungsfehlern verwendet wird; siehe die Option "error-log-format".

Die Direktive "log-format" überschreibt vorherige Direktiven vom Typ "option tcplog", "log-format", "option httplog" und "option httpslog".

<a id="entry-4-2-log-format-sd"></a>

**`log-format-sd <fmt>`**

```haproxy
log-format-sd <fmt>
```

Die benutzerdefinierte Formatzeichenkette zur Erzeugung strukturierter Daten gemäß RFC5424 festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Diese Direktive legt die Formatzeichenkette für den Teil mit strukturierten Daten gemäß RFC5424 fest. Sie gilt für alle Protokolleinträge, die durch Datenverkehr über das Frontend mit dieser Zeile entstehen. Wird die Direktive in einem defaults-Abschnitt verwendet, verwenden alle nachfolgenden Frontends dasselbe Protokollformat. [Abschnitt
8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschreibt die Formatzeichenkette für Protokolle ausführlich.

Weitere Informationen zum Teil mit strukturierten Daten nach RFC5424 finden Sie unter <https://tools.ietf.org/html/rfc5424#section-6.3>.

Hinweis: Diese Formatzeichenkette wird nur für Logger verwendet, deren Protokollformat auf "rfc5424" gesetzt ist.

Beispiel:

```text
log-format-sd [exampleSDID@1234\ bytes=\"%B\"\ status=\"%ST\"]
```

<a id="entry-4-2-log-steps"></a>

**`log-steps <steps>`**

```haproxy
log-steps <steps>
```

Festlegen, bei welchen Schritten der Transaktionsverarbeitung Protokolleinträge erzeugt werden sollen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Bei der Verarbeitung von TCP-/HTTP-Transaktionen kann haproxy an verschiedenen Stellen Protokolleinträge erzeugen, etwa bei accept, connect, request, response und close.

Standardmäßig gibt HAProxy pro Transaktion einen einzigen Protokolleintrag aus, sobald alle im Protokollformatausdruck verwendeten Elemente verfügbar sind. In der Praxis wird der Eintrag daher gewöhnlich am Ende der Transaktion ausgegeben, also nach dem Ende der Antwort bei HTTP oder am Ende der Verbindung bei TCP, sofern "option logasap" nicht verwendet wird.

Mit der Direktive "log-steps" lassen sich die genauen Ausgabezeitpunkte festlegen und sogar mehrere Protokolleinträge für dieselbe Transaktion erzeugen. Der Sonderwert 'all' aktiviert sämtliche verfügbaren Protokollauslöser, sodass eine Transaktion von accept bis close verfolgt werden kann. Einzelne Protokollauslöser können auch über ihre durch Kommas getrennten Namen angegeben werden, um gezielt festzulegen, wann Protokolleinträge erzeugt werden.

Übliche Protokollauslöser sind: accept, connect, request, response und close.

Beispiel:

```text
frontend myfront
    option httplog
    log-steps accept,close         #only log accept and close for the txn
```

Als Protokollierungsschritte angegebene Protokollauslöser, etwa accept oder close, können unverändert in log-profiles nach der Direktive 'on' verwendet werden. Die Kombination von "log-steps" mit log-profiles ermöglicht eine genaue Steuerung der Protokolleinträge, die haproxy während der Transaktionsverarbeitung automatisch erzeugt.

Diese Einstellung ist nur für Frontends relevant; in Backends wird sie ignoriert.

Siehe auch: "log-profile"

<a id="entry-4-2-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

Das Protokollkennzeichen für alle ausgehenden Protokollmeldungen festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Das tag-Feld im Syslog-Header wird auf diese Zeichenkette gesetzt. Standardmäßig wird das im global-Abschnitt festgelegte log-tag verwendet, andernfalls der Programmname beim Aufruf über die Befehlszeile, üblicherweise "HAProxy". Dies kann hilfreich sein, um mehrere Prozesse auf demselben Host oder Kundeninstanzen innerhalb desselben Prozesses zu unterscheiden. Im Backend verwenden Protokollmeldungen über verfügbare oder ausgefallene Server dieses Kennzeichen. Es kann praktisch sein, in einem defaults-Abschnitt ein log-tag für einen gehosteten Kunden festzulegen, darauf alle Frontends und Backends dieses Kunden folgen zu lassen und dann für den nächsten Kunden einen neuen defaults-Abschnitt zu beginnen. Siehe auch die globale Direktive "log-tag".

<a id="entry-4-2-max-keep-alive-queue"></a>

**`max-keep-alive-queue <value>`**

```haproxy
max-keep-alive-queue <value>
```

Die maximale Serverwarteschlangengröße für die Beibehaltung von Keepalive-Verbindungen festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

HTTP-Keepalive versucht nach Möglichkeit, dieselbe Serververbindung wiederzuverwenden. Gelegentlich kann dies jedoch nachteilig sein, etwa wenn ein Server viele Verbindungen hat, während andere untätig sind. Dies gilt besonders für Server mit statischen Inhalten.

Diese Einstellung legt einen Schwellenwert für die Anzahl wartender Verbindungen fest, ab dem HAProxy nicht mehr versucht, denselben Server wiederzuverwenden, sondern bevorzugt einen anderen sucht. Der Standardwert -1 bedeutet, dass es keine Grenze gibt. Der Wert null bedeutet, dass Keepalive-Anfragen niemals in eine Warteschlange eingereiht werden. Für sehr nahe Server, die mit geringer Latenz erreichbar sind und auf das Unterbrechen von Keepalive unempfindlich reagieren, wird ein niedriger Wert empfohlen; ein lokaler Server für statische Inhalte kann beispielsweise 10 oder weniger verwenden. Bei entfernten Servern mit hoher Latenz können höhere Werte nötig sein, um die Latenz und/oder den Aufwand für die Auswahl eines anderen Servers auszugleichen.

Dies hat keine Auswirkungen auf Antworten, die infolge einer 401-Antwort an denselben Server gebunden bleiben. Sie gehen weiterhin an denselben Server, selbst wenn sie dafür in eine Warteschlange eingereiht werden müssen.

Siehe auch: "option http-server-close", "option prefer-last-server", den Serverparameter "maxconn" und cookiebasierte Sitzungsbindung.

<a id="entry-4-2-max-session-srv-conns"></a>

**`max-session-srv-conns <nb>`**

```haproxy
max-session-srv-conns <nb>
```

Die maximale Anzahl ausgehender Verbindungen festlegen, die für eine bestimmte Clientsitzung inaktiv offengehalten werden können. Der Standardwert ist 5; er entspricht genau dem beim Kompilieren definierten MAX_SRV_LIST.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

<a id="entry-4-2-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

Die maximale Anzahl gleichzeitiger Verbindungen eines Frontends festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<conns>   ist die maximale Zahl gleichzeitiger Verbindungen, die das
          Frontend zur Verarbeitung annimmt. Weitere Verbindungen stellt
          das System in die Listen-Warteschlange des Sockets. Sie werden
          bedient, sobald eine Verbindung geschlossen wird.
```

Wenn das System dies unterstützt, kann es bei großen Websites sinnvoll sein, diese Grenze sehr hoch zu setzen, damit HAProxy die Verbindungswarteschlangen verwaltet und Verbindungsversuche der Clients nicht unbeantwortet bleiben. Dieser Wert sollte den globalen maxconn-Wert nicht überschreiten. Außerdem enthält eine Verbindung zwei Puffer von jeweils tune.bufsize (standardmäßig 16kB) sowie weitere Daten. Dadurch werden pro aufgebauter Verbindung etwa 33 kB RAM benötigt. Ein mittelgroßes System mit 1GB RAM kann bei entsprechender Abstimmung also ungefähr 20000-25000 gleichzeitige Verbindungen bewältigen.

Wird `<conns>` sehr hoch gesetzt, sind die Server möglicherweise nicht für diese Last ausgelegt. Daher ist es im Allgemeinen sinnvoll, ihnen angemessene Verbindungsgrenzen zuzuweisen.

Ist dieser Wert null, was dem Standard entspricht, wird der globale "maxconn"-Wert verwendet.

Siehe auch: "server", "maxconn" im global-Abschnitt, "fullconn"

<a id="entry-4-2-mode"></a>

**`mode { tcp|http|log|spop }`**

```haproxy
mode { tcp|http|log|spop }
```

Den Betriebsmodus oder das Protokoll der Instanz festlegen. Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \|
listen \| backend ja \| ja \| ja \| ja Argumente:

```text
tcp       Die Instanz arbeitet im reinen TCP-Modus. Zwischen Clients und
          Servern wird eine Vollduplex-Verbindung aufgebaut; eine Untersuchung
          auf Schicht 7 erfolgt nicht. Dies ist der Standardmodus. Er sollte
          für SSL, SSH, SMTP usw. verwendet werden.

http      Die Instanz arbeitet im HTTP-Modus. Die Clientanfrage wird eingehend
          analysiert, bevor eine Verbindung zu einem Server aufgebaut wird.
          Nicht RFC-konforme Anfragen werden abgelehnt. Filterung,
          Verarbeitung und Umschaltung auf Schicht 7 sind möglich. In diesem
          Modus liegt ein Großteil des Nutzens von HAProxy.

haterm    Das Frontend arbeitet im HTTP-Benchmark-Modus haterm. Backends
          unterstützen dies nicht. Einzelheiten stehen in doc/haterm.txt.

log       In einem backend-Abschnitt macht diese Einstellung das Backend zu
          einem Protokoll-Backend. Es kann mit der Syntax "backend@<name>"
          als Protokollziel jeder "log"-Direktive verwendet werden.
          Protokollnachrichten werden entsprechend den mit "balance"
          konfigurierbaren Lastverteilungseinstellungen auf die Server des
          Backends verteilt. Protokoll-Backends unterstützen UDP-Server durch
          das Präfix "udp@" vor der Serveradresse. Allgemeine Backend- und
          Serverfunktionen werden unterstützt, TCP- oder HTTP-spezifische
          Funktionen dagegen nicht.

spop      In einem backend-Abschnitt macht diese Einstellung das Backend zu
          einem spop-Backend. Dieser Modus ist zwingend erforderlich, wenn
          das Backend SPOA-Server enthält. Ist jedoch tcp als Modus gesetzt,
          wird er beim Erkennen solcher Server automatisch in spop geändert.

```

Bei inhaltsabhängiger Umschaltung müssen Frontend und Backend im selben Modus arbeiten, üblicherweise HTTP. Andernfalls wird die Konfiguration abgelehnt.

Beispiel:

```text
defaults http_instances
    mode http

```

<a id="entry-4-2-monitor-fail"></a>

**`monitor fail { if | unless } <condition>`**

```haproxy
monitor fail { if | unless } <condition>
```

Eine Bedingung hinzufügen, um auf eine HTTP-Überwachungsanfrage einen Fehler zurückzugeben.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
if <cond>     Die Überwachungsanfrage schlägt fehl, wenn die Bedingung erfüllt
              ist, und ist andernfalls erfolgreich. Die Bedingung sollte einen
              kombinierten Test beschreiben, der einen Fehler auslösen muss,
              wenn alle Bedingungen erfüllt sind, etwa eine geringe Serverzahl
              sowohl im Backend als auch in dessen Ersatz-Backend.

unless <cond> Die Überwachungsanfrage ist nur erfolgreich, wenn die Bedingung
              erfüllt ist, und schlägt andernfalls fehl. Eine solche Bedingung
              kann prüfen, ob in einer Liste von Backends eine Mindestzahl
              aktiver Server vorhanden ist.
```

Diese Anweisung fügt eine Bedingung hinzu, die erzwingen kann, dass die Antwort auf eine Überwachungsanfrage einen Fehler meldet. Fragt eine externe Komponente die für die Überwachung vorgesehene URI ab, wird standardmäßig eine Antwort mit dem Status 200 zurückgegeben. Ist eine der obigen Bedingungen erfüllt, antwortet HAProxy mit 503 statt
200. Damit lässt sich der Ausfall eines Standorts an eine externe Komponente melden, die ihre Routing-Ankündigungen zwischen mehreren Standorten auf die von HAProxy gemeldete Verfügbarkeit stützen kann. In diesem Fall würde eine ACL mit dem Kriterium "nbsrv" verwendet. "monitor fail" funktioniert nur im HTTP-Modus. Beide Statusmeldungen können bei Bedarf mit "errorfile" oder "errorloc" angepasst werden.

Beispiel:

```text
frontend www
   mode http
   acl site_dead nbsrv(dynamic) lt 2
   acl site_dead nbsrv(static)  lt 2
   monitor-uri   /site_alive
   monitor fail  if site_dead
```

Siehe auch: "monitor-uri", "errorfile", "errorloc"

<a id="entry-4-2-monitor-uri"></a>

**`monitor-uri <uri>`**

```haproxy
monitor-uri <uri>
```

Eine URI für Überwachungsanfragen externer Komponenten abfangen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<uri>     ist die genaue URI, die abgefangen werden soll, um den
          Gesundheitszustand von HAProxy zurückzugeben, statt die Anfrage
          weiterzuleiten.
```

Wenn ein Frontend eine HTTP-Anfrage mit Bezug auf `<uri>` empfängt, leitet HAProxy sie weder weiter noch protokolliert es sie. Stattdessen gibt es abhängig von den mit "monitor fail" definierten Fehlerbedingungen entweder "HTTP/1.0 200 OK" oder "HTTP/1.0 503 Service unavailable" zurück. Dies reicht normalerweise für jede vorgeschaltete HTTP-Prüfung aus, um den Dienst als UP und betriebsbereit zu erkennen, ohne die Anfrage an einen Backend-Server weiterzuleiten. Die HTTP-Methode, die Version und alle Header werden ignoriert; die Anfrage muss jedoch zumindest auf HTTP-Ebene gültig sein. Dieses Schlüsselwort darf nur in einem Frontend im HTTP-Modus verwendet werden.

Überwachungsanfragen werden sehr früh verarbeitet, unmittelbar nach dem Parsen der Anfrage und noch vor jeder "http-request"-Regel. Davor werden nur die tcp-request-Regelsätze angewendet. Diese Anfragen können auch nicht protokolliert werden; dies ist beabsichtigt. Es kann nur eine URI zur Überwachung konfiguriert werden. Bei mehreren "monitor-uri"-Anweisungen legt die letzte die zu verwendende URI fest. Diese Anfragen dienen ausschließlich dazu, einer übergeordneten Komponente den Zustand von HAProxy zu melden. Mit "monitor fail" und ACLs lassen sich jedoch beliebig viele Bedingungen hinzufügen und das Ergebnis dadurch an jede denkbare Prüfung anpassen, meistens an die Anzahl verfügbarer Server in einem Backend.

Hinweis: Beginnt `<uri>` mit einem Schrägstrich ('/'), erfolgt der Abgleich mit dem Pfad der Anfrage anstelle ihrer URI. Dies ist eine Umgehungslösung, damit HTTP/2-Anfragen auf die monitor-uri passen. Bei HTTP/2 werden Clients nämlich dazu angehalten, ausschließlich absolute URIs zu senden.

Beispiel:

```shell
# Use /haproxy_test to report HAProxy's status
frontend www
    mode http
    monitor-uri /haproxy_test
```

Siehe auch: "monitor fail"

<a id="entry-4-2-option-abortonclose"></a>

**`option abortonclose`**

```haproxy
option abortonclose
no option abortonclose
```

Den vorzeitigen Abbruch noch nicht begonnener Verarbeitung beim Schließen durch den Client aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

TCP-Verbindungen können in jeder Richtung unabhängig geschlossen werden. Eine nur in einer Richtung geschlossene Verbindung wird häufig als „halbgeschlossen“ bezeichnet. Als das HTTP-Umfeld noch überwiegend den Schließmodus verwendete, bei dem vor dem Schließen nur eine Anfrage und eine Antwort pro Verbindung übertragen wurden, war folgendes Verhalten skriptgesteuerter Clients verbreitet: Anfrage senden, die Senderichtung schließen, auf die Antwort warten, das Schließsignal empfangen und den Vorgang beenden. Mit Keepalive und fortschrittlicheren Protokollen ist dieses Vorgehen jedoch praktisch verschwunden. Wenn ein Client die Verbindung vor Empfang seiner Antwort schließt, liegt das im Wesentlichen daran, dass der Benutzer eine Übertragung abbrechen möchte oder eine Zeitüberschreitung eingetreten ist und die Verbindung geschlossen wird.

Diese beiden Situationen, halbgeschlossene Verbindung und Abbruch, lassen sich auf der Serverseite, hier am HAProxy-Listener, nicht unterscheiden. Das ist problematisch: Wird die Verbindung offengehalten und die Anfrage trotz eines Abbruchs durch den Client weiterverarbeitet, kann dies viele Ressourcen verbrauchen. Dies gilt besonders, wenn der Benutzer die Schaltfläche „Neu laden“ betätigt hat, da dann neue Anfragen eingereiht werden, ohne die vorherigen abzubrechen. Umgekehrt würde ein grundsätzlicher Abbruch bei solchen halbgeschlossenen Verbindungen zahlreiche TCP-Anwendungen beeinträchtigen, ebenso manche HTTP-Anwendungen in internen Netzen, die mit älteren Agenten kommunizieren.

Mit der Option "abortonclose" lässt sich das gewünschte Verhalten wählen: - In einem Frontend verhindert sie die Verarbeitung ausstehender TLS-Handshakes auf einer halbgeschlossenen Verbindung. Dazu kann es kommen, wenn ein Benutzer während einer HTTPS-Anfrage unter hoher Last „Neu laden“ betätigt, beispielsweise bei einem VRRP-Failover vom aktiven HAProxy-Knoten auf den Ersatzknoten: Alle Clients verbinden sich gleichzeitig neu und müssen jeweils einen aufwendigen, vollständigen TLS-Handshake durchführen. Dauert dies länger als einige Sekunden, geben wahrscheinlich manche Benutzer auf. CPU-Zyklen für deren Handshakes aufzuwenden, wäre sinnlos. Wegen des CPU-Aufwands von TLS-Handshakes wird empfohlen, diese Option auf aus dem Internet erreichbaren Frontends aktiviert zu lassen. Für eingehende TLS-Verbindungen ist dies der Standard.

    - In einem Backend bewirkt sie bei halbgeschlossenen Verbindungen den
      Versuch, eine noch nicht an einen Server gesendete Anfrage abzubrechen,
      also während sie in der Warteschlange liegt oder eine Verbindung
      hergestellt wird. Wird die Anfrage bereits von einem Server bearbeitet,
      wird auch die Verbindung zum Server halbgeschlossen, um ihm denselben
      Zustand zu signalisieren. Der Server entscheidet dann über das weitere
      Vorgehen. Für Backends im HTTP-Modus ist dies der Standard.

Es wird empfohlen, diese Option für aus dem Internet erreichbare TLS-Endpunkte und HTTP-Dienste zu aktivieren und für reine TCP-Dienste sowie nicht öffentlich erreichbare ältere Umgebungen zu deaktivieren. In HTTP-Backends ist sie standardmäßig aktiviert. Sie kann ausdrücklich deaktiviert werden, indem ihr das Schlüsselwort "no" vorangestellt wird, entweder im Backend-Abschnitt selbst oder im "defaults"-Abschnitt, von dem er erbt. Auch für TLS-Listener ist sie standardmäßig aktiviert und kann ausdrücklich deaktiviert werden, indem "no option
abortonclose" im Frontend oder im geerbten "defaults"-Abschnitt angegeben wird.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "timeout queue" sowie die Serverparameter "maxconn" und "maxqueue"

<a id="entry-4-2-option-accept-invalid-http-request"></a>

**`option accept-invalid-http-request     (deprecated)`**

```haproxy
option accept-invalid-http-request     (deprecated)
no option accept-invalid-http-request  (deprecated)
```

Weniger strenges Parsen von HTTP-Anfragen aktivieren oder deaktivieren

Das Schlüsselwort "accept-invalid-http-request" ist veraltet. Verwenden Sie stattdessen "option
accept-unsafe-violations-in-http-request".

<a id="entry-4-2-option-accept-invalid-http-response"></a>

**`option accept-invalid-http-response     (deprecated)`**

```haproxy
option accept-invalid-http-response     (deprecated)
no option accept-invalid-http-response  (deprecated)
```

Weniger strenges Parsen von HTTP-Antworten aktivieren oder deaktivieren

Das Schlüsselwort "accept-invalid-http-response" ist veraltet. Verwenden Sie stattdessen "option
accept-unsafe-violations-in-http-response".

<a id="entry-4-2-option-accept-unsafe-violations-in-http-request"></a>

**`option accept-unsafe-violations-in-http-request`**

```haproxy
option accept-unsafe-violations-in-http-request
no option accept-unsafe-violations-in-http-request
```

Weniger strenges Parsen von HTTP-Anfragen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Standardmäßig hält sich HAProxy beim Parsen von Nachrichten an die verschiedenen HTTP-RFCs. Das Parsen ist daher recht streng, und bei fehlerhaften Nachrichten wird ein Fehler an den Client zurückgegeben. Dieses Verhalten ist beabsichtigt, da solche Nachrichten vor allem für Angriffe verwendet werden, die Schwächen von Servern ausnutzen und Sicherheitsfilter umgehen. Manchmal hält sich ein fehlerhafter Browser aus irgendeinem Grund, etwa wegen seiner Konfiguration oder Implementierung, nicht an diese RCFs, und das Problem wird nicht sofort behoben. In diesem Fall kann diese Option den HAProxy-Parser weniger streng machen, damit er bestimmte ungültige Anfragen akzeptiert. Aus historischen Gründen betreffen die meisten Regeln das Parsen von H1. Neuere HTTP-Versionen sind tendenziell sauberer, und Anwendungen halten sich strenger an diese Protokolle.

Ist diese Option gesetzt, gelten folgende Regeln:

    * Nur bei H1 führen ungültige Zeichen, einschließlich des NULL-Zeichens,
      im Headernamen nicht zur Ablehnung; der Header wird jedoch verworfen.

    * Nur bei H1 wird das NULL-Zeichen im Headerwert akzeptiert;

    * Nur bei H1 werden Zeichen oberhalb von 127 in der URI akzeptiert. RFC3986
      legt die in einer URI erlaubten Zeichen genau fest. Die Zeichen 0-31,
      32 (Leerzeichen), 34 ('"'), 60 ('<'), 62 ('>'), 92 ('&#92;'), 94 ('^'),
      96 ('`'), 123 ('{'), 124 ('|'), 125 ('}'), 127 (Löschzeichen) und alle
      darüberliegenden Zeichen sind normalerweise nicht erlaubt. Bei H1 werden
      alle Zeichen im Bereich (0..32) sowie 127 immer blockiert. Alle Zeichen
      oberhalb von 127 (ausschließlich) werden ebenfalls blockiert, außer wenn
      diese Option aktiviert ist. Andere Zeichen (33..126) werden überhaupt
      nicht geprüft.

    * Bei H1 und H2 werden URLs mit Fragmentverweisen ('#' nach dem Pfad)
      akzeptiert;

    * Nur bei H1 wird der Authority-Teil von CONNECT-Anfragen nicht geprüft;

    * Nur bei H1 erfolgt keine Prüfung zwischen dem Authority-Teil und dem Wert
      des Host-Headers.

    * Nur bei H1 werden die Prüfungen der HTTP-Version gelockert. Dadurch werden
      GET-Anfragen nach HTTP/0.9 ohne Versionsangabe, andere Protokollnamen wie RTSP
      sowie mehrere Ziffern sowohl für die Haupt- als auch die Unterversion
      zugelassen.

    * Nur bei H1 werden WebSocket-Anfragen (RFC6455) akzeptiert, die kein
      gültiges Headerfeld "Sec-Websocket-Key" enthalten.

Diese Option sollte niemals standardmäßig aktiviert werden, da sie Anwendungsfehler verdeckt und Sicherheitslücken öffnet. Sie sollte erst eingesetzt werden, nachdem ein Problem bestätigt wurde.

Ist diese Option aktiviert, werden ungültige, aber akzeptierte H1-Anfragen erfasst, um eine spätere Analyse mit der Anfrage "show errors" über das UNIX-Statistik-Socket zu ermöglichen. Dies hilft auch zu bestätigen, dass das Problem behoben wurde.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option accept-unsafe-violations-in-http-response" und "show errors" über das Statistik-Socket.

<a id="entry-4-2-option-accept-unsafe-violations-in-http-response"></a>

**`option accept-unsafe-violations-in-http-response`**

```haproxy
option accept-unsafe-violations-in-http-response
no option accept-unsafe-violations-in-http-response
```

Weniger strenges Parsen von HTTP-Antworten aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Ähnlich wie "option accept-unsafe-violations-in-http-request" kann diese Option die Regeln für das Parsen von HTTP-Antworten lockern. Sie sollte nur für vertrauenswürdige ältere Server aktiviert werden, um bestimmte ungültige Antworten zu akzeptieren. Aus historischen Gründen betreffen die meisten Regeln das Parsen von H1. Neuere HTTP-Versionen sind tendenziell sauberer, und Anwendungen halten sich strenger an diese Protokolle.

Ist diese Option gesetzt, gelten folgende Regeln:

    * Nur bei H1 werden Statuscodes mit mehr als 3 Ziffern nicht abgelehnt,
      sofern ihr Wert in 16 Bit passt.

    * Nur bei H1 führen ungültige Zeichen, einschließlich des NULL-Zeichens,
      im Headernamen nicht zur Ablehnung; der Header wird jedoch verworfen.

    * Nur bei H1 wird das NULL-Zeichen im Headerwert akzeptiert;

    * Nur bei H1 werden leere Werte oder mehrere Vorkommen des Wertes "chunked"
      im Header Transfer-Encoding akzeptiert;

    * Nur bei H1 erfolgt keine Prüfung zwischen dem Authority-Teil und dem Wert
      des Host-Headers.

    * Nur bei H1 werden die Prüfungen der HTTP-Version gelockert. Dadurch werden
      andere Protokollnamen wie RTSP sowie mehrere Ziffern sowohl für die Haupt-
      als auch die Unterversion zugelassen.

    * Nur bei H1 werden WebSocket-Antworten (RFC6455) akzeptiert, die kein
      gültiges Headerfeld "Sec-Websocket-Accept" enthalten.

Diese Option sollte niemals standardmäßig aktiviert werden, da sie Anwendungsfehler verdeckt und Sicherheitslücken öffnet. Sie sollte erst eingesetzt werden, nachdem ein Problem bestätigt wurde.

Ist diese Option aktiviert, werden fehlerhafte Headernamen in Antworten weiterhin akzeptiert. Die vollständige Antwort wird jedoch erfasst, um eine spätere Analyse mit der Anfrage "show errors" über das UNIX-Statistik-Socket zu ermöglichen. Dies hilft auch zu bestätigen, dass das Problem behoben wurde.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option accept-unsafe-violations-in-http-request" und "show errors" über das Statistik-Socket.

<a id="entry-4-2-option-allbackups"></a>

**`option allbackups`**

```haproxy
option allbackups
no option allbackups
```

Entweder alle Ersatzserver gleichzeitig oder nur den ersten verwenden

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Standardmäßig erhält der erste betriebsbereite Ersatzserver den gesamten Datenverkehr, wenn alle regulären Server ausgefallen sind. Manchmal ist es jedoch sinnvoll, mehrere Ersatzserver gleichzeitig zu verwenden, weil einer allein nicht ausreicht. Ist "option allbackups" aktiviert, erfolgt die Lastverteilung zwischen allen Ersatzservern, sobald alle regulären Server nicht verfügbar sind. Dabei wird derselbe Lastverteilungsalgorithmus verwendet, und die Servergewichte werden berücksichtigt. Zwischen den Ersatzservern besteht dann keine Prioritätsreihenfolge mehr.

Diese Option wird vorwiegend bei statischen Serverfarmen eingesetzt, die eine Entschuldigungsseite zurückgeben sollen, wenn eine Anwendung vollständig offline ist.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

<a id="entry-4-2-option-checkcache"></a>

**`option checkcache`**

```haproxy
option checkcache
no option checkcache
```

Alle Serverantworten analysieren und Antworten mit zwischenspeicherbaren Cookies blockieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Manche übergeordneten Frameworks setzen überall Anwendungscookies und geben Entwicklern nicht immer genügend Kontrolle darüber, wie Antworten zwischengespeichert werden sollen. Wird ein Sitzungscookie zusammen mit einem zwischenspeicherbaren Objekt zurückgegeben, besteht ein hohes Risiko, dass Sitzungen zwischen Benutzern verwechselt oder gestohlen werden, wenn diese dieselben Caches verwenden. In manchen Situationen ist es besser, die Antwort zu blockieren, als sensible Sitzungsinformationen unkontrolliert weiterzugeben.

Die Option "checkcache" aktiviert eine eingehende Prüfung aller Serverantworten auf strikte Einhaltung der HTTP-Spezifikation zur Zwischenspeicherbarkeit. Sie prüft die Header "Cache-control", "Pragma" und "Set-cookie" in der Serverantwort sorgfältig darauf, ob ein Cookie auf einem clientseitigen Proxy zwischengespeichert werden könnte. Bei aktivierter Option dürfen nur folgende Antworten an den Client ausgeliefert werden: - alle ohne "Set-Cookie"-Header; - alle mit einem anderen Rückgabecode als 200, 203, 204, 206, 300, 301, 404, 405, 410, 414, 501, sofern der Server kein Headerfeld "Cache-control: public" gesetzt hat; - alle, die aus einer Anfrage mit einer anderen Methode als GET, HEAD, OPTIONS, TRACE hervorgehen, sofern der Server kein Headerfeld 'Cache-Control: public' gesetzt hat; - Antworten mit einem Header 'Pragma: no-cache' - Antworten mit einem Header 'Cache-control: private' - Antworten mit einem Header 'Cache-control: no-store' - Antworten mit einem Header 'Cache-control: max-age=0' - Antworten mit einem Header 'Cache-control: s-maxage=0' - Antworten mit einem Header 'Cache-control: no-cache' - Antworten mit einem Header 'Cache-control: no-cache="set-cookie"' - Antworten mit einem Header 'Cache-control:
no-cache="set-cookie,' (wobei weitere Felder nach set-cookie zulässig sind) - Antworten, die weder Frischeinformationen ("Cache-control" mit "max-age" oder "s-maxage" oder einen "Expires"-Header) noch einen Validator (einen "ETag"- oder "Last-Modified"-Header) enthalten, da ein spezifikationskonformer Cache eine solche Antwort nicht speichert.

Erfüllt eine Antwort diese Anforderungen nicht, wird sie wie durch eine Regel "http-response deny" blockiert, mit "HTTP 502 bad gateway". Der Sitzungsstatus zeigt "PH--" an. Dies bedeutet, dass der Proxy die Antwort während der Headerverarbeitung blockiert hat. Zusätzlich wird eine alert-Meldung protokolliert, damit Administratoren erfahren, dass etwas korrigiert werden muss.

Da dies die Anwendung erheblich beeinflusst, sollte sie vor dem Produktiveinsatz mit aktivierter Option gründlich getestet werden. Es ist auch sinnvoll, die Option bei Tests immer zu aktivieren, selbst wenn sie im Produktivbetrieb nicht verwendet wird, da sie potenziell gefährliches Anwendungsverhalten meldet.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

<a id="entry-4-2-option-clitcpka"></a>

**`option clitcpka`**

```haproxy
option clitcpka
no option clitcpka
```

Das Senden von TCP-Keepalive-Paketen auf der Clientseite aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Befindet sich zwischen einem Client und einem Server eine Firewall oder eine andere Komponente, die Sitzungszustände verfolgt, und verwendet das Protokoll sehr lange Sitzungen mit langen inaktiven Phasen, etwa bei Remotedesktops, besteht ein Risiko: Eine zwischengeschaltete Komponente könnte eine zu lange inaktive Sitzung ablaufen lassen.

Werden TCP-Keepalives auf Socket-Ebene aktiviert, sendet das System regelmäßig Pakete an das andere Ende der Verbindung und hält diese damit aktiv. Der Abstand zwischen Keepalive-Prüfungen wird ausschließlich vom System gesteuert und hängt sowohl vom Betriebssystem als auch von dessen Abstimmungsparametern ab.

Keepalive-Pakete werden auf Anwendungsebene weder gesendet noch empfangen. Nur die Netzwerkstapel sehen sie. Selbst wenn also eine Seite des Proxys bereits Keepalives verwendet, um ihre Verbindung aktiv zu halten, werden diese Pakete nicht zur anderen Seite des Proxys weitergeleitet.

Dies hat nichts mit HTTP-Keepalive zu tun.

Die Option "clitcpka" aktiviert das Senden von TCP-Keepalive-Prüfungen auf der Clientseite einer Verbindung. Dies sollte helfen, wenn zwischen HAProxy und einem Client Sitzungen ablaufen.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option srvtcpka", "option tcpka"

<a id="entry-4-2-option-contstats"></a>

**`option contstats`**

```haproxy
option contstats
```

Die kontinuierliche Aktualisierung der Datenverkehrsstatistiken aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Standardmäßig werden die Zähler für die Statistikberechnung erst erhöht, wenn ein Stream endet. Bei kleinen Objekten funktioniert dies recht gut. Bei großen Objekten, etwa großen Bildern oder Archiven, oder bei A/V-Streaming sieht ein aus den HAProxy-Zählern erzeugtes Diagramm jedoch wie ein Igel aus. Bei aktivierter Option werden die Zähler während des Streams häufig erhöht, typischerweise alle 5 Sekunden, was meist für gleichmäßige Diagramme ausreicht. Die erneute Zählung greift unmittelbar in einen häufig ausgeführten Verarbeitungspfad ein. Sie ist daher nicht standardmäßig aktiviert, da sie bei sehr vielen Sitzungen zahlreiche Aufweckvorgänge verursachen und die Leistung geringfügig senken kann.

<a id="entry-4-2-option-disable-h2-upgrade"></a>

**`option disable-h2-upgrade`**

```haproxy
option disable-h2-upgrade
no option disable-h2-upgrade
```

Den impliziten Wechsel einer HTTP/1.x-Clientverbindung auf HTTP/2 aktivieren oder deaktivieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Standardmäßig kann HAProxy eine HTTP/1.x-Clientverbindung implizit in eine HTTP/2-Verbindung umwandeln, wenn die erste über eine bestimmte HTTP-Verbindung empfangene Anfrage der HTTP/2-Verbindungspräambel entspricht, also der Zeichenkette "PRI \*
HTTP/2.0&#92;r&#92;n&#92;r&#92;nSM&#92;r&#92;n&#92;r&#92;n".
So können HTTP/1.x- und HTTP/2-Clients über Verbindungen ohne SSL unterstützt werden. Diese Option muss verwendet werden, um den impliziten Protokollwechsel zu deaktivieren. Dieser implizite Wechsel wird nur bei HTTP-Proxys unterstützt, und die Option ist entsprechend nur dort verfügbar. HTTP/2 kann bei unverschlüsselten Verbindungen auch durch "proto h2" in der bind-Zeile erzwungen werden. Schließlich gilt diese Option für alle bind-Zeilen. Um implizite Wechsel auf HTTP/2 für eine bestimmte bind-Zeile zu deaktivieren, kann "proto
h1" verwendet werden.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

<a id="entry-4-2-option-dontlog-normal"></a>

**`option dontlog-normal`**

```haproxy
option dontlog-normal
no option dontlog-normal
```

Die Protokollierung normaler, erfolgreicher Verbindungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Große Websites verarbeiten mehrere Tausend Verbindungen pro Sekunde, wodurch die Protokollierung erheblichen Aufwand verursachen kann. Manche müssen Protokolle sogar abschalten und können dann Probleme im Produktivbetrieb nicht untersuchen. Diese Option sorgt dafür, dass normale Verbindungen ohne Fehler, Zeitüberschreitung, Wiederholungsversuch oder erneute Zuweisung nicht protokolliert werden. Dadurch bleibt Speicherplatz für Auffälligkeiten. Im HTTP-Modus wird der Antwortstatuscode geprüft; Rückgabecodes 5xx werden weiterhin protokolliert.

Von dieser Option wird dringend abgeraten: Der Schlüssel zur Lösung komplexer Probleme findet sich meist in den normalen Protokolleinträgen, die hier entfallen. Wenn Sie Protokolle trennen müssen, verwenden Sie stattdessen die Option "log-separate-errors".

Siehe auch: "log", "dontlognull", "log-separate-errors" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-dontlognull"></a>

**`option dontlognull`**

```haproxy
option dontlognull
no option dontlognull
```

Die Protokollierung von Verbindungen ohne Datenübertragung aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

In manchen Umgebungen verbinden sich Komponenten regelmäßig mit verschiedenen Systemen, um deren Erreichbarkeit zu prüfen. Dies können andere Load-Balancer oder Überwachungssysteme sein. Standardmäßig erzeugt selbst eine einfache Portprüfung oder ein Portscan einen Protokolleintrag. Wenn solche Verbindungen die Protokolle zu stark belasten, kann die Option "dontlognull" aktiviert werden. Dann werden Verbindungen, über die keine Daten übertragen wurden, nicht protokolliert, was typischerweise auf diese Prüfungen zutrifft. Fehler werden jedoch weiterhin an den Client zurückgegeben und in den Statistiken gezählt. Ist dies nicht gewünscht, kann stattdessen die Option http-ignore-probes verwendet werden.

Im Allgemeinen wird empfohlen, diese Option in nicht kontrollierten Umgebungen wie dem Internet nicht zu verwenden, da andernfalls Scans und andere bösartige Aktivitäten nicht protokolliert würden.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "log", "http-ignore-probes", "monitor-uri" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-external-check"></a>

**`option external-check`**

```haproxy
option external-check
```

Externe Prozesse für Health Checks von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Der Zustand eines Servers kann mit einem externen Befehl geprüft werden. Dazu wird das mit "external-check command" festgelegte Programm ausgeführt.

Die globale Einstellung "external-check" muss aktiviert sein.

Siehe auch: "external-check", "external-check command", "external-check path"

<a id="entry-4-2-option-forwarded"></a>

**`option forwarded [ proto ]`**

```haproxy
option forwarded [ proto ]
                 [ host | host-expr <host_expr> ]
                 [ by | by-expr <by_expr> ] [ by_port | by_port-expr <by_port_expr>]
                 [ for | for-expr <for_expr> ] [ for_port | for_port-expr <for_port_expr>]
no option forwarded
```

Das Einfügen des forwarded-Headers gemäß rfc 7239 in an Server gesendete Anfragen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<host_expr>     Optionales Argument für einen eigenen Sample-Ausdruck, dessen
                Ergebnis als Wert des Parameters 'host' verwendet wird.

<by_expr>       Optionales Argument für einen eigenen Sample-Ausdruck, dessen
                Ergebnis als nodename-Wert des Parameters 'by' verwendet wird.

<for_expr>      Optionales Argument für einen eigenen Sample-Ausdruck, dessen
                Ergebnis als nodename-Wert des Parameters 'for' verwendet wird.

<by_port_expr>  Optionales Argument für einen eigenen Sample-Ausdruck, dessen
                Ergebnis als nodeport-Wert des Parameters 'by' verwendet wird.

<for_port_expr> Optionales Argument für einen eigenen Sample-Ausdruck, dessen
                Ergebnis als nodeport-Wert des Parameters 'for' verwendet wird.

```

Da HAProxy als Reverse-Proxy arbeitet, geht den Servern ein Teil des Anfragekontexts verloren, etwa der Ursprung der Anfrage mit IP-Adresse des Clients und verwendetem Protokoll.

Diese Einschränkung wird häufig mit dem bekannten x-forward-for und verwandten x-forward-\*-Headern umgangen, um Teile dieses Kontexts an die dahinterliegenden Server und Anwendungen weiterzugeben. Obwohl dies üblicherweise funktioniert und weit verbreitet ist, wird es nicht offiziell von der IETF unterstützt und kann Interoperabilitäts- und Sicherheitsprobleme verursachen.

Als Lösung hat die IETF eine neue HTTP-Erweiterung beschrieben: den forwarded-Header (RFC7239). Weitere Informationen: <https://www.rfc-editor.org/rfc/rfc7239.html>

Dieser einzelne Header kann zahlreiche Details übermitteln und löst vor allem das Problem verketteter Proxys. Der RFC erlaubt mehreren hintereinandergeschalteten Proxys, ihre eigenen Werte an einen bereits vorhandenen Header anzuhängen.

Diese Option kann in einem defaults-, listen- oder backend-Abschnitt angegeben werden; in frontend-Abschnitten wird sie ignoriert.

Wird option forwarded ohne Argumente gesetzt, gilt das implizite Standardverhalten. Dabei wird der Parameter proto aktiviert und die ursprüngliche IP-Adresse des Clients eingefügt.

Die entsprechende explizite, manuelle Konfiguration wäre:

```text
option forwarded proto for
```

Das Schlüsselwort 'by' aktiviert den Parameter 'by' ("nodename") im forwarded-Header. Damit lassen sich Informationen zum Proxy der Anfrage einfügen. Der Wert von 'by' wird auf die IP-Adresse des Proxys, also die Zieladresse, gesetzt. Ist sie nicht verfügbar, etwa bei einem UNIX-Listener, wird 'by' auf "unknown" gesetzt.

Das Schlüsselwort 'by-expr' aktiviert den Parameter 'by' ("nodename") im forwarded-Header. Damit lassen sich Informationen zum Proxy der Anfrage einfügen. Der Wert von 'by' wird auf das Ergebnis des Sample-Ausdrucks `<by_expr>` gesetzt, sofern dieses gültig ist, andernfalls auf "unknown".

Das Schlüsselwort 'for' aktiviert den Parameter 'for' ("nodename") im forwarded-Header. Damit lassen sich Informationen zum Client der Anfrage einfügen. Der Wert von 'for' wird auf die IP-Adresse des Clients, also die Quelladresse, gesetzt. Ist sie nicht verfügbar, etwa bei einem UNIX-Listener, wird 'for' auf "unknown" gesetzt.

Das Schlüsselwort 'for-expr' aktiviert den Parameter 'for' ("nodename") im forwarded-Header. Damit lassen sich Informationen zum Client der Anfrage einfügen. Der Wert von 'for' wird auf das Ergebnis des Sample-Ausdrucks `<for_expr>` gesetzt, sofern dieses gültig ist, andernfalls auf "unknown".

Das Schlüsselwort 'by_port' ergänzt den Parameter 'by' um die Information "nodeport". 'by_port' erfordert, dass 'by' oder 'by-expr' gesetzt ist; andernfalls wird es ignoriert. "nodeport" wird auf den Port des Proxys, also den Zielport, gesetzt, sofern er verfügbar ist; andernfalls wird es ignoriert.

Das Schlüsselwort 'by_port-expr' ergänzt den Parameter 'by' um die Information "nodeport". 'by_port-expr' erfordert, dass 'by' oder 'by-expr' gesetzt ist; andernfalls wird es ignoriert. "nodeport" wird auf das Ergebnis des Sample-Ausdrucks `<by_port_expr>` gesetzt, sofern dieses gültig ist; andernfalls wird es ignoriert.

Das Schlüsselwort 'for_port' ergänzt den Parameter 'for' um die Information "nodeport". 'for_port' erfordert, dass 'for' oder 'for-expr' gesetzt ist; andernfalls wird es ignoriert. "nodeport" wird auf den Port des Clients, also den Quellport, gesetzt, sofern er verfügbar ist; andernfalls wird es ignoriert.

Das Schlüsselwort 'for_port-expr' ergänzt den Parameter 'for' um die Information "nodeport". 'for_port-expr' erfordert, dass 'for' oder 'for-expr' gesetzt ist; andernfalls wird es ignoriert. "nodeport" wird auf das Ergebnis des Sample-Ausdrucks `<for_port_expr>` gesetzt, sofern dieses gültig ist; andernfalls wird es ignoriert.

Beispiele:

```shell
# Those servers want the ip address and protocol of the client request
# Resulting header would look like this:
#   forwarded: proto=http;for=127.0.0.1
backend www_default
    mode http
    option forwarded
    #equivalent to: option forwarded proto for

# Those servers want the requested host and hashed client ip address
# as well as client source port (you should use seed for xxh32 if ensuring
# ip privacy is a concern)
# Resulting header would look like this:
#   forwarded: host="haproxy.org";for="_000000007F2F367E:60138"
backend www_host
    mode http
    option forwarded host for-expr src,xxh32,hex for_port

# Those servers want custom data in host, for and by parameters
# Resulting header would look like this:
#   forwarded: host="host.com";by=_haproxy;for="[::1]:10"
backend www_custom
    mode http
    option forwarded host-expr str(host.com) by-expr str(_haproxy) for for_port-expr int(10)

# Those servers want random 'for' obfuscated identifiers for request
# tracing purposes while protecting sensitive IP information
# Resulting header would look like this:
#   forwarded: for=_000000002B1F4D63
backend www_for_hide
    mode http
    option forwarded for-expr rand,hex
```

Siehe auch: "option forwardfor", "option originalto"

<a id="entry-4-2-option-forwardfor"></a>

**`option forwardfor [ except <network> ] [ header <name> ] [ if-none ]`**

```haproxy
option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
```

Das Einfügen des Headers X-Forwarded-For in an Server gesendete Anfragen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<network> ist ein optionales Argument, das diese Option für Quellen
          deaktiviert, die <network> entsprechen.
<name>    ist ein optionales Argument, um einen anderen Namen für den Header
          "X-Forwarded-For" anzugeben.
```

Da HAProxy als Reverse-Proxy arbeitet, sehen die Server seine IP-Adresse als Clientadresse. Das ist manchmal störend, wenn in den Serverprotokollen die IP-Adresse des Clients erwartet wird. Als Lösung kann HAProxy allen an den Server gesendeten Anfragen den bekannten HTTP-Header "X-Forwarded-For" hinzufügen. Dessen Wert gibt die IP-Adresse des Clients an. Da dieser Header immer am Ende der vorhandenen Headerliste angehängt wird, muss der Server so konfiguriert sein, dass er ausschließlich das letzte Vorkommen dieses Headers verwendet. Wie die Verwendung dieses Standardheaders aktiviert wird, steht im Serverhandbuch. Es darf nur das letzte Vorkommen verwendet werden, da der Client durchaus bereits einen solchen Header mitgesendet haben kann.

Mit dem Schlüsselwort "header" kann anstelle von "X-Forwarded-For" ein anderer Headername angegeben werden. Dies kann nützlich sein, wenn bereits ein "X-Forwarded-For"-Header einer anderen Anwendung wie stunnel vorhanden ist und erhalten bleiben soll. Dasselbe gilt, wenn der Backend-Server "X-Forwarded-For" nicht verwendet und einen anderen Header verlangt; Zeus Web Servers benötigen beispielsweise "X-Cluster-Client-IP".

Manchmal wird dieselbe HAProxy-Instanz sowohl für direkten Clientzugriff als auch für Zugriff über einen Reverse-Proxy verwendet, etwa wenn ein SSL-Reverse-Proxy den HTTPS-Verkehr entschlüsselt. Für eine bekannte Quelladresse oder ein bekanntes Netz lässt sich das Hinzufügen des Headers mit dem Schlüsselwort "except" und der nachfolgenden Netzadresse deaktivieren. Bei Quell-IP-Adressen, die zu diesem Netz passen, wird der Header dann nicht hinzugefügt. Dies wird am häufigsten mit privaten Netzen oder 127.0.0.1 verwendet. Sowohl IPv4 als auch IPv6 werden unterstützt.

Alternativ legt das Schlüsselwort "if-none" fest, dass der Header nur hinzugefügt wird, wenn er noch nicht vorhanden ist. Dies sollte nur in einer vollständig vertrauenswürdigen Umgebung verwendet werden, da ein Sicherheitsproblem entstehen kann, wenn die bei HAProxy eintreffenden Header vom Endbenutzer kontrolliert werden.

Diese Option kann im Frontend oder im Backend angegeben werden. Verwendet sie mindestens eines von beiden, wird der Header hinzugefügt. Wenn beide das Unterargument header definieren, hat dessen Einstellung im Backend Vorrang vor der im Frontend. Beim Argument "if-none" setzt sich dagegen die zwingende Hinzufügung durch, sobald mindestens eines von Frontend und Backend dieses Argument nicht angibt.

Beispiel:

```shell
# Public HTTP address also used by stunnel on the same machine
frontend www
    mode http
    option forwardfor except 127.0.0.1  # stunnel already adds the header

# Those servers want the IP Address in X-Client
backend www
    mode http
    option forwardfor header X-Client
```

Siehe auch: "option httpclose", "option http-server-close", "option http-keep-alive"

<a id="entry-4-2-option-h1-case-adjust-bogus-client"></a>

**`option h1-case-adjust-bogus-client`**

```haproxy
option h1-case-adjust-bogus-client
no option h1-case-adjust-bogus-client
```

Die Anpassung der Groß- und Kleinschreibung von HTTP/1-Headern für fehlerhafte Clients aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Für Headernamen gibt es keine vorgeschriebene Groß- und Kleinschreibung, da gemäß RFC7230 nicht zwischen ihnen unterschieden wird. Anwendungen müssen Headernamen daher ohne Unterscheidung der Groß- und Kleinschreibung verarbeiten. Einige fehlerhafte Anwendungen verletzen jedoch die Standards und verlassen sich fälschlicherweise auf die von Browsern am häufigsten verwendete Schreibweise. Mit HTTP/2 wird dies kritisch, weil sämtliche Headernamen in Kleinbuchstaben übertragen werden müssen und HAProxy dieselbe Konvention verwendet. Unabhängig von der HTTP-Version werden alle Headernamen in Kleinbuchstaben an Clients und Server gesendet.

Wenn HAProxy eine HTTP/1-Antwort empfängt, werden deren Headernamen in Kleinbuchstaben umgewandelt, so verarbeitet und an die Clients gesendet. Wenn bekannt ist, dass ein Client die HTTP-Standards verletzt und eine von HAProxy kommende Antwort nicht verarbeiten kann, lassen sich die kleingeschriebenen Headernamen beim Formatieren und Senden der Antwort in ein anderes Format umwandeln. Dazu wird diese Option aktiviert und mit den globalen Direktiven "h1-case-adjust" oder "h1-case-adjust-file" die Liste der umzuformatierenden Header angegeben. Dies darf nur eine vorübergehende Umgehungslösung sein, bis der Client korrigiert wurde: Clients, die solche Umgehungen benötigen, können für Content-Smuggling-Angriffe anfällig sein und müssen unbedingt korrigiert werden.

Diese Option hat keine Auswirkungen auf standardkonforme Clients.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option h1-case-adjust-bogus-server", "h1-case-adjust", "h1-case-adjust-file".

<a id="entry-4-2-option-h1-case-adjust-bogus-server"></a>

**`option h1-case-adjust-bogus-server`**

```haproxy
option h1-case-adjust-bogus-server
no option h1-case-adjust-bogus-server
```

Die Anpassung der Groß- und Kleinschreibung von HTTP/1-Headern für fehlerhafte Server aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Für Headernamen gibt es keine vorgeschriebene Groß- und Kleinschreibung, da gemäß RFC7230 nicht zwischen ihnen unterschieden wird. Anwendungen müssen Headernamen daher ohne Unterscheidung der Groß- und Kleinschreibung verarbeiten. Einige fehlerhafte Anwendungen verletzen jedoch die Standards und verlassen sich fälschlicherweise auf die von Browsern am häufigsten verwendete Schreibweise. Mit HTTP/2 wird dies kritisch, weil sämtliche Headernamen in Kleinbuchstaben übertragen werden müssen und HAProxy dieselbe Konvention verwendet. Unabhängig von der HTTP-Version werden alle Headernamen in Kleinbuchstaben an Clients und Server gesendet.

Wenn HAProxy eine HTTP/1-Anfrage empfängt, werden deren Headernamen in Kleinbuchstaben umgewandelt, so verarbeitet und an die Server gesendet. Wenn bekannt ist, dass ein Server die HTTP-Standards verletzt und eine von HAProxy kommende Anfrage nicht verarbeiten kann, lassen sich die kleingeschriebenen Headernamen beim Formatieren und Senden der Anfrage in ein anderes Format umwandeln. Dazu wird diese Option aktiviert und mit den globalen Direktiven "h1-case-adjust" oder "h1-case-adjust-file" die Liste der umzuformatierenden Header angegeben. Dies darf nur eine vorübergehende Umgehungslösung sein, bis der Server korrigiert wurde: Server, die solche Umgehungen benötigen, können für Content-Smuggling-Angriffe anfällig sein und müssen unbedingt korrigiert werden.

Diese Option hat keine Auswirkungen auf standardkonforme Server.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option h1-case-adjust-bogus-client", "h1-case-adjust", "h1-case-adjust-file".

<a id="entry-4-2-option-http-buffer-request"></a>

**`option http-buffer-request`**

```haproxy
option http-buffer-request
no option http-buffer-request
```

Das Warten auf den vollständigen HTTP-Anfragekörper vor der weiteren Verarbeitung aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Manchmal ist es sinnvoll, vor einer Entscheidung auf den Körper einer HTTP-Anfrage zu warten. Dies geschieht beispielsweise bei "balance url_param". Ein erster Anwendungsfall ist das Puffern von Anfragen langsamer Clients, bevor eine Verbindung zum Server aufgebaut wird. Ein weiterer ist eine Routing-Entscheidung anhand des Inhalts des Anfragekörpers. Im Frontend oder Backend erzwingt diese Option, dass die HTTP-Verarbeitung wartet, bis entweder der gesamte Anfragekörper empfangen wurde oder der Anfragepuffer voll ist. Dies kann bei Anwendungen unerwünschte Nebenwirkungen haben, die HTTP zweckwidrig verwenden und ungepufferte Übertragungen zwischen Frontend und Backend erwarten. Daher sollte diese Option keinesfalls standardmäßig verwendet werden.

Siehe auch: "option http-no-delay", "timeout http-request", "http-request wait-for-body"

<a id="entry-4-2-option-http-drop-request-trailers"></a>

**`option http-drop-request-trailers`**

```haproxy
option http-drop-request-trailers
no option http-drop-request-trailers
```

HTTP-Trailer beim Senden einer Anfrage an den Server verwerfen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| nein \| ja

Argumente: keine

Ist diese Option aktiviert, werden sämtliche HTTP-Trailer einer Anfrage verworfen, bevor sie an den Server gesendet wird.

RFC9110#section-6.5.1 legt fest, dass Trailerfelder mit Headerfeldern zusammengeführt werden können. Dies sollte bewusst geschehen, kann jedoch für manche Anwendungen problematisch sein. Das gilt insbesondere dann, wenn bösartige Clients sensible Headerfelder im Trailerteil verstecken und zwischengeschaltete Komponenten sie ohne besondere Prüfung mit den Headern zusammenführen. In diesem Fall kann diese Option im Backend aktiviert werden, um alle Trailerfelder aus Anfragen zu entfernen, bevor sie an den Server gesendet werden.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option http-drop-response-trailers"

<a id="entry-4-2-option-http-drop-response-trailers"></a>

**`option http-drop-response-trailers`**

```haproxy
option http-drop-response-trailers
no option http-drop-response-trailers
```

HTTP-Trailer beim Senden einer Antwort an den Client verwerfen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Diese Option ähnelt "option http-drop-request-trailers", muss jedoch verwendet werden, um Trailerfelder aus Antworten zu verwerfen, bevor diese an Clients gesendet werden.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option http-drop-request-trailers"

<a id="entry-4-2-option-http-ignore-probes"></a>

**`option http-ignore-probes`**

```haproxy
option http-ignore-probes
no option http-ignore-probes
```

Die Protokollierung von Verbindungen ohne Datenübertragung und Anfragezeitüberschreitungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Einige Browser haben begonnen, eine "pre-connect"-Funktion zu implementieren: Sie verbinden sich vorsorglich mit kürzlich besuchten Websites, falls der Benutzer sie erneut aufrufen möchte. Dadurch entstehen viele Verbindungen zu Websites, die mit 408 Request Timeout enden, wenn zuerst die Zeitüberschreitung eintritt, oder mit 400 Bad Request, wenn der Browser sie vorher schließt. Diese Verbindungen füllen die Protokolle und erhöhen die Fehlerzähler. "option dontlognull" gab es bereits, reicht hier jedoch nicht aus. Diese Option bewirkt stattdessen Folgendes: - Sie verhindert, dass eine 400/408-Meldung an den Client gesendet wird, wenn vor dem Schließen der Verbindung nichts empfangen wurde; - sie verhindert in dieser Situation jeden Protokolleintrag; - sie verhindert die Erhöhung jedes Fehlerzählers.

Die leere Verbindung wird damit stillschweigend ignoriert. Diese Option sollte möglichst nur verwendet werden, wenn ihre Notwendigkeit feststeht, da sie tatsächliche Probleme verdeckt. Die häufigste Ursache dafür, dass keine Anfrage empfangen wird und ein Status 408 erscheint, ist eine abweichende MTU zwischen dem Client und einer zwischengeschalteten Komponente wie einem VPN, das zu große Pakete blockiert. Solche Probleme treten gewöhnlich bei POST-Anfragen sowie bei GET-Anfragen mit großen Cookies auf. Die Protokolle sind häufig die einzige Möglichkeit, sie zu erkennen.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "log", "dontlognull", "errorfile" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-http-keep-alive"></a>

**`option http-keep-alive`**

```haproxy
option http-keep-alive
no option http-keep-alive
```

HTTP-Keepalive vom Client bis zum Server für HTTP/1.x-Verbindungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Standardmäßig arbeitet HAProxy bei dauerhaften HTTP/1.x-Verbindungen im Keepalive-Modus: Es verarbeitet jede Anfrage und Antwort einer Verbindung und lässt die Verbindung anschließend auf beiden Seiten inaktiv offen. Dieser Modus lässt sich durch verschiedene Optionen wie "option http-server-close" oder "option
httpclose" ändern. Mit dieser Option kann wieder zum Keepalive-Modus zurückgekehrt werden, etwa wenn in einem defaults-Abschnitt ein anderer Modus verwendet wurde.

"option http-keep-alive" aktiviert den HTTP-Keepalive-Modus sowohl auf der Client- als auch auf der Serverseite. Dies bietet die geringste Latenz auf der Clientseite mit ihrem langsameren Netz und die schnellste Sitzungswiederverwendung auf der Serverseite, erfordert jedoch das Offenhalten inaktiver Verbindungen zu den Servern. Bei kleinen Objekten lässt sich mit dieser Option im Allgemeinen ungefähr die doppelte Anfragerate gegenüber der Option "http-server-close" erreichen. Sie kann vor allem in zwei Situationen nützlich sein:

    - wenn der Server nicht HTTP-konform ist und die Verbindung statt der
      Anfragen authentifiziert, etwa bei NTLM-Authentifizierung

    - wenn der Aufbau der Verbindung zum Server im Verhältnis zum Abruf des
      zugehörigen Objekts vom Server erheblichen Aufwand verursacht.

Letzteres kann bei einem schnellen Server für statische Inhalte oder einem Cache auftreten.

Derzeit zeigen die Protokolle nicht an, ob Anfragen aus derselben Sitzung stammen. Der im Protokoll angegebene Annahmezeitpunkt entspricht dem Ende der vorherigen Anfrage, und die Anfragezeit entspricht der Wartezeit auf eine neue Anfrage. Die Keepalive-Anfragezeit wird weiterhin durch "timeout http-keep-alive" begrenzt oder, falls nicht gesetzt, durch "timeout http-request".

Diese Option deaktiviert und ersetzt alle vorherigen Optionen "option httpclose" oder "option http-server-close".

Siehe auch: "option httpclose",, "option http-server-close", "option prefer-last-server" und "option
http-pretend-keepalive".

<a id="entry-4-2-option-http-no-delay"></a>

**`option http-no-delay`**

```haproxy
option http-no-delay
no option http-no-delay
```

Das System anweisen, bei HTTP geringe interaktive Verzögerungen gegenüber hohem Durchsatz zu bevorzugen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Bei HTTP fließen die Nutzdaten jeweils nur in eine Richtung; Interaktivität ist nicht vorgesehen. Von jedem Agenten wird erwartet, Daten bei vertretbar geringer Verzögerung in gewissem Umfang zu puffern. Es gibt einige äußerst seltene Anwendungen zwischen Servern, die das HTTP-Protokoll missbrauchen und erwarten, dass die Nutzdatenphase hochgradig interaktiv ist, wobei innerhalb einer einzigen Anfrage viele Datenblöcke abwechselnd in beide Richtungen übertragen werden. Dies wird von der HTTP-Spezifikation überhaupt nicht unterstützt und wird bei den meisten Proxies oder Servern nicht funktionieren. Wenn solche Anwendungen dies über HAProxy versuchen, funktioniert es zwar, doch treten hohe Verzögerungen auf, da die Netzwerkoptimierungen einen hohen Durchsatz bevorzugen, indem sie das System anweisen, auf ausreichend Daten zu warten, um nur vollständige Pakete zu senden. Typische Verzögerungen betragen etwa 200 ms pro Hin- und Rückweg. Beachten Sie, dass dies nur bei abnormalen Anwendungen auftritt. Normale Anwendungen wie CONNECT-Anfragen oder WebSockets sind nicht betroffen.

Wenn "option http-no-delay" im Frontend oder Backend einer Verbindung gesetzt ist, werden alle solchen Optimierungen deaktiviert, um den Datenaustausch möglichst schnell zu machen. Natürlich gibt dies keine Garantie für die Funktionalität, da die Funktion an jeder anderen Stelle scheitern kann. Aber wenn es über HAProxy funktioniert, wird es so schnell wie möglich funktionieren. Diese Option sollte niemals standardmäßig aktiviert werden und sollte niemals verwendet werden, außer wenn eine solche fehlerhafte Anwendung entdeckt wurde. Der Einfluss dieser Option ist eine Erhöhung des Bandbreitenverbrauchs und des CPU-Verbrauchs, was die Leistung in Umgebungen mit hoher Latenz erheblich beeinträchtigen kann.

Siehe auch: "option http-buffer-request"

<a id="entry-4-2-option-http-pretend-keepalive"></a>

**`option http-pretend-keepalive`**

```haproxy
option http-pretend-keepalive
no option http-pretend-keepalive
```

Festlegen, ob HAProxy gegenüber dem Server Keepalive für eine HTTP/1.x-Verbindung ankündigt

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Wenn "option http-server-close" oder "option httpclose" aktiviert ist, fügt HAProxy einen "Connection: close"-Header zur HTTP/1.x-Anfrage hinzu, die an den Server weitergeleitet wird. Leider verzichten einige Server beim Erkennen dieses Headers automatisch auf die Chunked-Kodierung für Antworten unbekannter Länge, obwohl dies völlig unabhängig davon ist. Die Folge ist, dass ein Client oder ein Cache eine unvollständige Antwort erhalten kann, ohne dies zu bemerken, und die Antwort für vollständig halten könnte.

Durch die Einstellung von "option http-pretend-keepalive" lässt HAProxy den Server glauben, dass die Verbindung weiterhin aktiv bleibt. Der Server fällt dann nicht auf das unerwünschte Verhalten zurück. Sobald HAProxy die gesamte Antwort erhalten hat, schließt es die Verbindung zum Server genau so, wie es bei "option httpclose" der Fall wäre. Auf diese Weise erhält der Client eine normale Antwort, und die Verbindung wird korrekt auf der Serverseite geschlossen.

Es wird empfohlen, diese Option nicht standardmäßig zu aktivieren, da die meisten Server die Verbindung effizienter selbst nach dem letzten Paket schließen und ihre Puffer etwas früher freigeben werden. Außerdem könnte das zusätzliche Paket im Netzwerk die erreichbare Spitzenleistung insgesamt leicht reduzieren. Bei aktivierter Option hat HAProxy allerdings etwas weniger Arbeit zu erledigen. Wenn HAProxy somit der Engpass in der gesamten Architektur ist, könnte die Aktivierung dieser Option einige CPU-Zyklen sparen.

Diese Option kann in Backend- und listen-Abschnitten gesetzt werden. Die Verwendung in einem Frontend-Abschnitt wird ignoriert, und es wird während des Starts eine Warnung ausgegeben. Es handelt sich um eine Backend-bezogene Option, daher besteht kein echter Grund, sie in einem Frontend zu setzen.

Wenn diese Option in einem "defaults"-Abschnitt aktiviert wurde, kann sie in einer bestimmten Instanz durch Voranstellen des "no"-Schlüsselworts deaktiviert werden.

Siehe auch: "option httpclose", "option http-server-close" und "option http-keep-alive"

<a id="entry-4-2-option-http-restrict-req-hdr-names"></a>

**`option http-restrict-req-hdr-names { preserve | delete | reject }`**

```haproxy
option http-restrict-req-hdr-names { preserve | delete | reject }
```

Das Verhalten von HAProxy für Namen von HTTP-Anfrageheadern mit Zeichen außerhalb des Zeichensatzes "[a-zA-Z0-9-]" festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
preserve  Deaktiviert die Filterung. Dies ist der Standardmodus für
          HTTP-Proxys ohne konfigurierte FastCGI-Anwendung.

delete    Entfernt Anfrageheader, deren Name ein Zeichen außerhalb des
          Zeichensatzes "[a-zA-Z0-9-]" enthält. Dies ist der Standardmodus
          für HTTP-Backends mit konfigurierter FastCGI-Anwendung.

reject    Lehnt die Anfrage mit einer 403-Forbidden-Antwort ab, wenn sie einen
          Headernamen mit einem Zeichen außerhalb des Zeichensatzes
          "[a-zA-Z0-9-]" enthält.
```

Diese Option kann verwendet werden, um die Namen von Anfrageheadern auf alphanumerische Zeichen und Bindestriche ([A-Za-z0-9-]) zu beschränken. Dies kann erforderlich sein, um mit nicht-HTTP-konformen Servern zu interagieren, die bestimmte Zeichen in Headernamen nicht korrekt behandeln. Es kann auch erforderlich sein für FastCGI-Anwendungen, da alle nicht alphanumerischen Zeichen in Headernamen durch einen Unterstrich ('\_') ersetzt werden. Dadurch ist es leicht möglich, Headernamen zu verwechseln und einige Regeln zu umgehen. Zum Beispiel werden die Header "X-Forwarded-For" und "X_Forwarded-For" beide in FastCGI zu "HTTP_X_FORWARDED_FOR" konvertiert.

Diese Option wird für jeden Proxy nach der Auswertung der http-request-Regeln ausgewertet.

<a id="entry-4-2-option-http-server-close"></a>

**`option http-server-close`**

```haproxy
option http-server-close
no option http-server-close
```

Das Schließen von HTTP/1.x-Verbindungen auf der Serverseite aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Standardmäßig arbeitet HAProxy im Keep-Alive-Modus bezüglich persistenter HTTP/1.x-Verbindungen: Es verarbeitet jede Anfrage und Antwort einer Verbindung und lässt die Verbindung anschließend auf beiden Seiten inaktiv offen. Dieser Modus kann durch mehrere Optionen geändert werden, wie beispielsweise "option http-server-close" oder "option httpclose". Die Einstellung von "option http-server-close" aktiviert das Schließen von HTTP-Verbindungen auf der Serverseite, während die Fähigkeit zur Unterstützung von HTTP Keep-Alive und Pipelining auf Clientseite erhalten bleibt. Dies bietet die niedrigste Latenz auf Clientseite (bei langsamen Netzwerken) und die schnellste Sitzungs-Wiederverwendung auf Serverseite, um Serverressourcen zu sparen, vergleichbar mit "option httpclose". Dadurch können auch Server ohne Keepalive-Unterstützung gegenüber Clients im Keepalive-Modus bereitgestellt werden, sofern sie die Anforderungen von RFC7230 erfüllen. Bitte beachten Sie, dass einige Server diese Anforderungen nicht immer erfüllen, wenn sie "Connection: close" in der Anfrage sehen. Die Folge ist, dass Keep-Alive niemals verwendet wird. Eine Lösung besteht darin, "option http-pretend-keepalive" zu aktivieren.

Derzeit geben die Protokolle nicht an, ob Anfragen aus derselben Sitzung stammen oder nicht. Das in den Protokollen angegebene Annahmezeitpunkt entspricht dem Ende der vorherigen Anfrage, und die Anfragezeit entspricht der Zeit, die zum Warten auf eine neue Anfrage benötigt wird. Die Keepalive-Anfragezeit wird weiterhin durch "timeout http-keep-alive" begrenzt oder, falls nicht gesetzt, durch "timeout http-request".

Diese Option kann sowohl in einem Frontend als auch in einem Backend gesetzt werden. Sie ist aktiviert, wenn sie mindestens im Frontend oder im Backend der Verbindung aktiviert ist. Sie deaktiviert und ersetzt jede vorherige "option httpclose" oder "option http-keep-alive". [Abschnitt 4](/de/haproxy/proxies/) ("Proxys") beschreibt, wie sich diese Option mit anderen kombiniert, wenn Frontend- und Backend-Einstellungen voneinander abweichen.

Wenn diese Option in einem "defaults"-Abschnitt aktiviert wurde, kann sie in einer bestimmten Instanz durch Voranstellen des "no"-Schlüsselworts deaktiviert werden.

Siehe auch: "option httpclose", "option http-pretend-keepalive" und "option http-keep-alive".

<a id="entry-4-2-option-http-use-proxy-header"></a>

**`option http-use-proxy-header`**

```haproxy
option http-use-proxy-header
no option http-use-proxy-header
```

Den nicht standardisierten Header Proxy-Connection anstelle von Connection verwenden

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

RFC7230 schreibt ausdrücklich vor, dass HTTP/1.1-Agenten über den Connection-Header angeben müssen, ob sie dauerhafte oder nicht dauerhafte Verbindungen wünschen. Browser und Proxys ignorieren diesen Header jedoch bei Verbindungen über einen Proxy und verwenden stattdessen den undokumentierten, nicht standardisierten Header Proxy-Connection. Problematisch wird dies, wenn ein Load-Balancer zwischen Browsern und solchen Proxys eingesetzt wird: HAProxy versteht dann etwas anderes als das, was Client und Proxy miteinander vereinbaren.

Wird diese Option in einem Frontend gesetzt, kann HAProxy bei Erkennung von Proxy-Anfragen automatisch auf diesen nicht standardisierten Header wechseln. Als Proxy-Anfrage gilt hier eine Anfrage, deren URI weder mit '/' noch mit '\*' beginnt. Dies ist mit dem HTTP-Tunnelmodus inkompatibel. Die Option kann nur in einem Frontend angegeben werden und wirkt sich während der gesamten Verarbeitung auf die Anfrage aus.

Bei gesetzter Option verwendet außerdem eine Anfrage, die eine Authentifizierung erfordert, automatisch die Header zur Proxy-Authentifizierung, sofern sie selbst eine Proxy-Anfrage ist. Damit lässt sich die Authentifizierung vor einem bestehenden Proxy prüfen oder erzwingen.

Diese Option sollte normalerweise niemals verwendet werden, außer vor einem Proxy.

Siehe auch: "option httpclose" und "option http-server-close".

<a id="entry-4-2-option-httpchk"></a>

**`option httpchk`**

```haproxy
option httpchk
option httpchk <uri>
option httpchk <method> <uri>
option httpchk <method> <uri> <version>
option httpchk <method> <uri> <version> <host>
```

Das HTTP-Protokoll für Health Checks der Server aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<method>  ist die optionale HTTP-Methode für die Anfragen. Ohne Angabe wird
          "OPTIONS" verwendet, da diese Methode meist wenig Verarbeitung auf
          dem Server erfordert und leicht aus Protokollen herauszufiltern ist.
          Jede Methode kann verwendet werden; vom Erfinden nicht standardisierter
          Methoden wird jedoch abgeraten.

<uri>     ist die in HTTP-Anfragen verwendete URI. Standardmäßig ist dies " / ",
          die auf fast jedem Server standardmäßig erreichbar ist. Sie kann
          durch jede andere URI ersetzt werden. Abfragezeichenfolgen sind
          zulässig.

<version> ist die optionale Zeichenfolge der HTTP-Version. Der Standard ist
          "HTTP/1.0". Manche Server verhalten sich mit HTTP 1.0 jedoch
          fehlerhaft; dann kann eine Umstellung auf HTTP/1.1 helfen. Das
          Feld Host ist bei HTTP/1.1 zwingend erforderlich.

<host>    ist der optionale Wert des HTTP-Headers Host. Standardmäßig ist er
          nicht gesetzt. Er ist eine Zeichenfolge im Protokollformat.
```

Standardmäßig bestehen Serverzustandsprüfungen nur aus dem Versuch, eine TCP-Verbindung aufzubauen. Wird "option
httpchk" angegeben, wird nach dem Aufbau der TCP-Verbindung eine vollständige HTTP-Anfrage gesendet. Antworten mit 2xx und 3xx gelten als gültig; alle anderen Antworten sowie das vollständige Ausbleiben einer Antwort zeigen einen Serverausfall an.

In Kombination mit "http-check"-Direktiven lassen sich die bei HTTP-Health-Checks gesendete Anfrage oder die Abgleichregeln für die Antwort anpassen. Außerdem kann wie mit der Direktive "tcp-check" für TCP-Health-Checks eine send/expect-Sequenz konfiguriert werden.

Zum Öffnen der Verbindungen für HTTP-Health-Checks wird standardmäßig die Serverkonfiguration verwendet. Serverparameter können jedoch mit "http-check connect"-Regeln überschrieben werden.

Die Option "httpchk" erfordert nicht zwingend ein HTTP-Backend; sie funktioniert auch mit reinen TCP-Backends. Dies ist besonders nützlich, um einfache Skripte zu prüfen, die über den inetd-Daemon an eigene Ports gebunden sind. Intern wird jedoch stets ein HTX-Multiplexer verwendet. Das bedeutet, dass die Anfrageformatierung und das Parsen der Antwort streng erfolgen.

Beispiele:

```shell
# Relay HTTPS traffic to Apache instance and check service availability
# using HTTP request "OPTIONS * HTTP/1.1" on port 80.
backend https_relay
    mode tcp
    option httpchk OPTIONS * HTTP/1.1
    http-check send hdr Host www
    server apache1 192.168.1.1:443 check port 80
```

Siehe auch: "option ssl-hello-chk", "option smtpchk", "option mysql-check", "option pgsql-check", "http-check" sowie die Serveroptionen "check", "port" und "inter".

<a id="entry-4-2-option-httpclose"></a>

**`option httpclose`**

```haproxy
option httpclose
no option httpclose
```

Das Schließen von HTTP/1.x-Verbindungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Standardmäßig arbeitet HAProxy bei dauerhaften HTTP/1.x-Verbindungen im Keepalive-Modus: Es verarbeitet jede Anfrage und Antwort einer Verbindung und lässt die Verbindung anschließend auf beiden Seiten inaktiv offen. Dieser Modus lässt sich durch verschiedene Optionen wie "option http-server-close" oder "option
httpclose" ändern.

Ist "option httpclose" gesetzt, schließt HAProxy je nach Ort der Einstellung die Client- oder die Serververbindung. Für Clientverbindungen zählt das Frontend, für Serververbindungen das Backend. Wird die Option in einem Listener gesetzt, gilt sie für beide Seiten. In jeder Richtung wird geprüft, ob bereits ein Header "Connection: close" gesetzt ist; fehlt er, wird er hinzugefügt.

Diese Option kann auch mit "option http-pretend-keepalive" kombiniert werden. Dann wird der Anfrageheader "Connection: close" nicht gesendet, die Verbindung aber weiterhin geschlossen, sobald die vollständige Antwort empfangen wurde.

Sie deaktiviert und ersetzt alle vorherigen Optionen "option http-server-close" oder "option http-keep-alive".

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option http-server-close".

<a id="entry-4-2-option-httplog"></a>

**`option httplog [ clf ]`**

```haproxy
option httplog [ clf ]
```

Die Protokollierung von HTTP-Anfrage, Streamstatus und Zeitmessungen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
clf       Mit dem Argument "clf" wird das CLF-Format statt des
          standardmäßigen HTTP-Formats von HAProxy ausgegeben. Dies ist
          nützlich, wenn die HAProxy-Protokolle mit einem bestimmten
          Protokollanalyseprogramm verarbeitet werden müssen, das nur
          CLF unterstützt und nicht erweiterbar ist.
```

Standardmäßig ist das Protokollausgabeformat sehr knapp: Es enthält lediglich Quell- und Zieladressen sowie den Instanznamen. Mit "option httplog" erhält jede Protokollzeile ein wesentlich ausführlicheres Format. Es enthält unter anderem die HTTP-Anfrage, Verbindungszeitmessungen, den Streamstatus, Verbindungszahlen, erfasste Header und Cookies, die Namen von Frontend, Backend und Server sowie natürlich Quelladresse und Ports.

Die alleinige Angabe von "option httplog" hebt automatisch den Modus 'clf' auf, wenn dieser standardmäßig gesetzt war.

"option httplog" überschreibt jede vorherige "log-format"-Direktive.

Siehe auch: [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-httpslog"></a>

**`option httpslog`**

```haproxy
option httpslog
```

Die Protokollierung von HTTPS-Anfrage, Streamstatus und Zeitmessungen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Standardmäßig ist das Protokollausgabeformat sehr knapp: Es enthält lediglich Quell- und Zieladressen sowie den Instanznamen. Mit "option httpslog" erhält jede Protokollzeile ein wesentlich ausführlicheres Format. Es enthält unter anderem die HTTP-Anfrage, Verbindungszeitmessungen, den Streamstatus, Verbindungszahlen, erfasste Header und Cookies, die Namen von Frontend, Backend und Server, den Status der SSL-Zertifikatsprüfung und des SSL-Handshakes sowie natürlich Quelladresse und Ports.

"option httpslog" überschreibt jede vorherige "log-format"-Direktive.

Siehe auch: [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-idle-close-on-response"></a>

**`option idle-close-on-response`**

```haproxy
option idle-close-on-response
no option idle-close-on-response
```

Das Schließen inaktiver Frontendverbindungen während eines sanften Stopps vermeiden

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Standardmäßig werden inaktive Verbindungen bei einem sanften Stopp geschlossen. In manchen Umgebungen hat ein Client bereits inaktive Verbindungen zum Proxy aufgebaut, um später Anfragen zu senden. Wenn Schreibfehler nicht korrekt durch Wiederholungsversuche behandelt werden, kann dies beim Neuladen von haproxy zu Fehlern führen. Obwohl eine korrekte Implementierung bei Verbindungs- oder Schreibfehlern erneut versuchen sollte, wurde diese Option eingeführt, um die Kompatibilität mit haproxy vor Version 2.4 zu erhalten. Vor v2.4 wartete haproxy tatsächlich auf eine letzte Anfrage und Antwort, um vor dem Schließen den Header "connection: close" hinzuzufügen. So wurde dem Client mitgeteilt, dass die Verbindung nicht wiederverwendbar sein würde.

Dieses Verhalten wurde beispielsweise bei AWS mit einem vor haproxy geschalteten ALB beobachtet. Im Ergebnis sendete ALB beim Neuladen von haproxy den Status 502.

Benutzer werden darauf hingewiesen, dass diese Option die Anzahl alter Prozesse erhöhen kann, wenn Verbindungen zu lange inaktiv bleiben. Bei häufigem Neuladen kann es erforderlich sein, die Clientzeitüberschreitungen und/oder den Parameter "hard-stop-after" entsprechend anzupassen.

Siehe auch: "timeout client", "timeout client-fin", "timeout http-request", "hard-stop-after"

<a id="entry-4-2-option-independent-streams"></a>

**`option independent-streams`**

```haproxy
option independent-streams
no option independent-streams
```

Die unabhängige Behandlung von Zeitüberschreitungen für beide Richtungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Standardmäßig werden beim Senden von Daten über ein Socket sowohl dessen Schreib- als auch dessen Lesezeitüberschreitung neu gestartet. Der Grund ist, dass auf dem Socket Aktivität stattfindet und es keine andere Möglichkeit gibt festzustellen, ob Daten empfangen werden sollten.

Dieses Standardverhalten ist für fast alle Anwendungen erwünscht. In einem bestimmten Fall ist es jedoch sinnvoll, es zu deaktivieren und die Lesezeitüberschreitung nur bei eingehenden Daten neu zu starten: bei Streams mit langen Zeitüberschreitungen und wenig Datenaustausch, etwa Telnet-Sitzungen. Verschwindet der Server plötzlich, sammeln sich die ausgehenden Daten in den Socket-Puffern des Systems. Beide Zeitüberschreitungen werden weiterhin korrekt neu gestartet, und es lässt sich nicht erkennen, dass der Server die Daten nicht empfängt. Daher tritt keine Zeitüberschreitung ein. Wenn das zugrunde liegende Protokoll gesendete Daten jedoch stets zurückspiegelt, würde dies allein ausreichen, um das Problem anhand der Lesezeitüberschreitung zu erkennen. Bei Protokollen mit mehr Datenaustausch tritt dieses Problem nicht auf, da sich die Daten nicht lange in den Socket-Puffern ansammeln.

Wird diese Option im Frontend gesetzt, wird die Lesezeitüberschreitung beim Senden von Daten an den Client nicht mehr neu gestartet. Dafür gibt es vermutlich wenig Anwendungsmöglichkeiten. Im Backend verhindert die Option entsprechend das Neustarten der Lesezeitüberschreitung beim Senden von Daten an den Server. Dadurch schlagen gewöhnlich große HTTP-POST-Übertragungen über langsame Leitungen fehl; verwenden Sie die Option daher mit Vorsicht.

Siehe auch: "timeout client", "timeout server" und "timeout tunnel"

<a id="entry-4-2-option-ldap-check"></a>

**`option ldap-check`**

```haproxy
option ldap-check
```

LDAPv3-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Es kann geprüft werden, ob der Server LDAPv3 korrekt verarbeitet, statt lediglich zu testen, ob er die TCP-Verbindung annimmt. Bei gesetzter Option wird eine anonyme Simple-Bind-Nachricht für LDAPv3 an den Server gesendet und die Antwort auf eine LDAPv3-Bind-Antwortnachricht untersucht.

Der Server gilt nur dann als funktionsfähig, wenn die LDAP-Antwort für resultCode den Wert success enthält (<http://tools.ietf.org/html/rfc4511#section-4.1.9>).

Die Protokollierung von Bind-Anfragen hängt vom Server ab. Hinweise zur Konfiguration finden Sie in dessen Dokumentation.

Beispiel:

```text
option ldap-check
```

Siehe auch: "option httpchk"

<a id="entry-4-2-option-log-health-checks"></a>

**`option log-health-checks`**

```haproxy
option log-health-checks
no option log-health-checks
```

Die Protokollierung von Statusänderungen bei Health Checks aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Standardmäßig werden fehlgeschlagene Health Checks protokolliert, wenn der Server UP ist, und erfolgreiche Prüfungen, wenn er DOWN ist. Dadurch ist die Menge zusätzlicher Informationen begrenzt.

Bei aktivierter Option wird jede Änderung des Prüfungsstatus oder des Serverzustands protokolliert. So lässt sich erkennen, dass ein Server vor seinem Absturz gelegentlich Prüfungen nicht bestand, oder genau nachvollziehen, wann er keinen gültigen HTTP-Status mehr zurückgab, wann anschließend der Port Verbindungen abwies und wann der Server schließlich überhaupt nicht mehr antwortete.

Statusänderungen, die nicht durch Health Checks verursacht werden, etwa das Aktivieren oder Deaktivieren über die CLI, werden von dieser Option absichtlich nicht protokolliert.

Siehe auch: "option httpchk", "option ldap-check", "option mysql-check", "option pgsql-check", "option
redis-check", "option smtpchk", "option tcp-check", "log" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-log-separate-errors"></a>

**`option log-separate-errors`**

```haproxy
option log-separate-errors
no option log-separate-errors
```

Die Protokollstufe für nicht vollständig erfolgreiche Verbindungen ändern

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Fehler in Protokollen zu finden, ist manchmal schwierig. Mit dieser Option erhöht HAProxy die Stufe von Einträgen mit möglicherweise aufschlussreichen Informationen wie Fehlern, Zeitüberschreitungen, Wiederholungsversuchen, erneuten Zuweisungen oder HTTP-Statuscodes 5xx von "info" auf "err". Die meisten Syslog-Daemons können solche Einträge dadurch getrennt in einer anderen Datei protokollieren. Entfernen Sie sie jedoch nicht aus der ursprünglichen Datei, da sonst die Reihenfolge verloren geht, die sehr wichtige Informationen liefert.

Große Websites mit mehreren Tausend Verbindungen pro Sekunde können damit normalen Datenverkehr in einem Ringpuffer protokollieren und nur die kleineren Fehlerprotokolle archivieren.

Siehe auch: "log", "dontlognull", "dontlog-normal" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-logasap"></a>

**`option logasap`**

```haproxy
option logasap
no option logasap
```

Frühzeitige Protokollierung aktivieren oder deaktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Standardmäßig werden Protokolleinträge ausgegeben, sobald alle in der log-format-Zeichenkette verwendeten Protokollformat-Aliasse und Sample-Abrufe einen Wert liefern oder wenn der Stream beendet wird. So können die eingebauten Protokollformate die Übertragungszeit oder die Anzahl der Bytes in den Protokollmeldungen berücksichtigen.

Bei langlebigen Verbindungen, etwa großen Dateiübertragungen oder RDP, kann es dauern, bis eine Anfrage oder Verbindung im Protokoll erscheint. Mit "option logasap" wird die Protokollmeldung im Modus tcp unmittelbar nach dem Aufbau der Serververbindung erzeugt, im Modus http unmittelbar nach dem Senden der vollständigen Header durch den Server. Es fehlen dann die endgültige Gesamtzahl der Bytes und die vollständige Gesamtzeit: Die Bytezahl gibt nur die bis zur Erzeugung der Meldung übertragenen Daten an, und die Zeit berücksichtigt weder die restliche Verbindungsdauer noch die verbleibende Übertragungszeit. Bei HTTP ist es sinnvoll, den Antwortheader Content-Length zu erfassen, damit das Protokoll zumindest die erwartete Anzahl zu übertragender Bytes angibt.

Beispiele:

```text
listen http_proxy 0.0.0.0:80
    mode http
    option httplog
    option logasap
    log 192.168.2.200 local3
```

```text
    >>> Feb  6 12:14:14 localhost \
          haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
          static/srv1 9/10/7/14/+30 200 +243 - - ---- 3/1/1/1/0 1/0 \
          "GET /image.iso HTTP/1.0"
```

Siehe auch: "option httplog", "capture response header" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-mysql-check"></a>

**`option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]`**

```haproxy
option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]
```

MySQL-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<username> Der Benutzername für die Verbindung zum MySQL-Server.
post-41    Mit Clients ab v4.1 kompatible Prüfungen senden (Standard).
pre-41     Mit Clients vor v4.1 kompatible Prüfungen senden.
post-80    Mit Clients ab v8.0 kompatible Prüfungen senden, bei denen
           CLIENT_PLUGIN_AUTH gesetzt ist und mysql_native_password als
           Authentifizierungs-Plugin verwendet wird. Diese Option für
           MySQL-Server ab 8.0+ verwenden, wenn der Benutzer für Health Checks
           mit mysql_native_password-Authentifizierung angelegt wurde. Beispiel:
             CREATE USER 'haproxy'@'%' IDENTIFIED WITH mysql_native_password BY '';
```

Wird ein Benutzername angegeben, besteht die Prüfung aus dem Senden von zwei MySQL-Paketen: einem Paket vom Typ Client Authentication und einem QUIT-Paket, um die MySQL-Sitzung korrekt zu schließen. Anschließend werden das MySQL-Paket Handshake Initialization und/oder das Error-Paket geparst. Dies ist ein einfacher, aber nützlicher Test, der auf dem Server weder Fehler noch abgebrochene Verbindungsaufbauten erzeugt. Er erfordert jedoch einen nicht gesperrten, berechtigten Benutzer ohne Passwort. So lässt sich ein einfacher eingeschränkter MySQL-Benutzer mit optionalen Ressourcenlimits anlegen:

```text
CREATE USER '<username>'@'<ip_of_haproxy|network_of_haproxy/netmask>'
/*!50701 WITH MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 0 */
/*M!100201 MAX_STATEMENT_TIME 0.0001 */;
```

Wird kein Benutzername angegeben, was veraltet ist und nicht empfohlen wird, besteht die Prüfung lediglich aus dem Parsen des MySQL-Pakets Handshake Initialization oder des Error-Pakets. In diesem Modus wird nichts gesendet. Es wurde berichtet, dass dies zu einer Sperrung führen kann, wenn die Prüfung zu häufig erfolgt und/oder nicht genügend Datenverkehr vorhanden ist. In diesem Fall muss der MySQL-Wert "max_connect_errors" geprüft werden: Wird nach einer unterbrochenen Verbindung innerhalb von weniger als MySQL "max_connect_errors" Versuchen erfolgreich eine Verbindung aufgebaut, wird der Fehlerzähler für den Host auf null zurückgesetzt. Wird der Host mit HAProxy gesperrt, lässt sich die Sperre ausschließlich mit der Anweisung "FLUSH HOSTS" aufheben.

Dies prüft weder das Vorhandensein noch die Konsistenz der Datenbank. Dazu kann beispielsweise eine externe Prüfung mit xinetd verwendet werden.

Die Prüfung erfordert MySQL \>=3.22. Für ältere Versionen verwenden Sie bitte eine TCP-Prüfung.

Ein MySQL-Server benötigt häufig die IP-Adresse des Clients für verschiedene Zwecke, etwa den Abgleich von IP-basierten Berechtigungen und die Verbindungsprotokollierung. Wenn möglich, ist es daher oft sinnvoll, beim Verbindungsaufbau zum Server mit dem Argument "usesrc" des Schlüsselworts "source" die IP-Adresse des Clients als eigene auszugeben. Dazu muss die Funktion für transparente Proxys einkompiliert sein, und der MySQL-Server muss den Verkehr zum Client über den Rechner mit HAProxy routen.

Siehe auch: "option httpchk"

<a id="entry-4-2-option-nolinger"></a>

**`option nolinger`**

```haproxy
option nolinger
no option nolinger
```

Das sofortige Freigeben von Sitzungsressourcen nach dem Schließen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Wenn Clients oder Server Verbindungen unsauber abbrechen, etwa durch eine physische Trennung, greift die Sitzungszeitüberschreitung, und die Sitzung wird geschlossen. Im System bleibt sie jedoch noch einige Zeit im Zustand FIN_WAIT1, belegt Ressourcen und kann den Aufbau neuer Verbindungen einschränken.

In diesem Fall kann "option nolinger" aktiviert werden. Sie zwingt das System, beim Schließen alle noch ausstehenden Daten eines Sockets sofort zu entfernen. Dadurch wird ein TCP RST gesendet, ausstehende Daten werden abgeschnitten, und die Sitzung wird sofort aus den Systemtabellen entfernt. Für den Client zeigt sich dies gewöhnlich in abgeschnittenen Antworten, wenn das Schließen zusammen mit dem letzten Datenblock erfolgt, etwa bei einer Weiterleitung oder Fehlerantwort. Auf der Serverseite kann die Option helfen, beim Weiterleiten eines Clientabbruchs in Tunneln die Quellports sofort freizugeben. In beiden Fällen werden TCP-Resets gesendet. Da die Sitzung sofort zerstört wird, gibt es keine erneute Übertragung. In einem Netz mit Paketverlusten kann dies Probleme verstärken, besonders wenn sich auf der verlustbehafteten Seite eine Firewall befindet: Diese könnte den Reset empfangen und verarbeiten, ihre Sitzung entfernen und anschließend jeden weiteren Datenverkehr dieser Sitzung blockieren, einschließlich erneuter Übertragungen von der anderen Seite. Empfängt die andere Seite den Reset nicht, wird sie daher nie wieder einen RST erhalten, und die Firewall protokolliert möglicherweise viele blockierte Pakete.

Aus all diesen Gründen wird dringend empfohlen, diese Option NICHT zu verwenden, außer wenn sie als letzter Ausweg unbedingt erforderlich ist. In den meisten Situationen erzielen die Zeitüberschreitungen "client-fin" oder "server-fin" ähnliche Ergebnisse bei zuverlässigerem Verhalten. Unter Linux kann auch die bind- oder Servereinstellung "tcp-ut" verwendet werden.

Diese Option kann je nach benötigter Seite in Frontends und Backends verwendet werden: im Frontend für Clients, im Backend für Server. Obwohl sie technisch in "defaults"-Abschnitten unterstützt wird, darf sie dort wirklich nicht verwendet werden. Sie könnte versehentlich in Abschnitte vererbt werden, in denen sie nicht verwendet werden darf, und dort Probleme verursachen.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "timeout client-fin", "timeout server-fin" sowie das bind- oder Server-Schlüsselwort "tcp-ut".

<a id="entry-4-2-option-originalto"></a>

**`option originalto [ except <network> ] [ header <name> ]`**

```haproxy
option originalto [ except <network> ] [ header <name> ]
```

Das Einfügen des Headers X-Original-To in an Server gesendete Anfragen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<network> ist ein optionales Argument, das diese Option für Quellen
          deaktiviert, die <network> entsprechen.
<name>    ist ein optionales Argument, um einen anderen Namen für den Header
          "X-Original-To" anzugeben.
```

Da HAProxy im transparenten Modus arbeiten kann, lässt sich jede Clientanfrage zum Proxy umleiten. HAProxy selbst kann jede Anfrage an eine komplexe SQUID-Umgebung weiterleiten, wobei der Zielhost aus SO_ORIGINAL_DST verloren geht. Dies ist störend, wenn Zugriffsregeln auf Ziel-IP-Adressen beruhen sollen. Als Lösung kann HAProxy allen an den Server gesendeten Anfragen einen neuen HTTP-Header "X-Original-To" hinzufügen. Dessen Wert gibt die ursprüngliche Ziel-IP-Adresse an. Es muss so konfiguriert werden, dass ausschließlich das letzte Vorkommen dieses Headers verwendet wird. Nur dieses darf verwendet werden, da der Client durchaus bereits einen solchen Header mitgesendet haben kann.

Mit dem Schlüsselwort "header" kann anstelle von "X-Original-To" ein anderer Headername angegeben werden. Dies kann nützlich sein, wenn bereits ein "X-Original-To"-Header einer anderen Anwendung vorhanden ist und erhalten bleiben soll. Dasselbe gilt, wenn der Backend-Server "X-Original-To" nicht verwendet und einen anderen Header verlangt.

Manchmal wird dieselbe HAProxy-Instanz sowohl für direkten Clientzugriff als auch für Zugriff über einen Reverse-Proxy verwendet, etwa wenn ein SSL-Reverse-Proxy den HTTPS-Verkehr entschlüsselt. Für eine bekannte Zieladresse oder ein bekanntes Netz lässt sich das Hinzufügen des Headers mit dem Schlüsselwort "except" und der nachfolgenden Netzadresse deaktivieren. Bei Ziel-IP-Adressen, die zu diesem Netz passen, wird der Header dann nicht hinzugefügt. Dies wird am häufigsten mit privaten Netzen oder 127.0.0.1 verwendet. Sowohl IPv4 als auch IPv6 werden unterstützt.

Diese Option kann im Frontend oder im Backend angegeben werden. Verwendet sie mindestens eines von beiden, wird der Header hinzugefügt. Wenn beide das Unterargument header definieren, hat dessen Einstellung im Backend Vorrang vor der im Frontend.

Beispiele:

```shell
# Original Destination address
frontend www
    mode http
    option originalto except 127.0.0.1

# Those servers want the IP Address in X-Client-Dst
backend www
    mode http
    option originalto header X-Client-Dst
```

Siehe auch: "option httpclose", "option http-server-close".

<a id="entry-4-2-option-persist"></a>

**`option persist`**

```haproxy
option persist
no option persist
```

Die erzwungene Sitzungsbindung an ausgefallene Server aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Erreicht eine HTTP-Anfrage ein Backend mit einem Cookie, das auf einen ausgefallenen Server verweist, wird sie standardmäßig einem anderen Server zugewiesen. Falls unbedingt erforderlich, kann mit "option persist" erzwungen werden, dass die Anfrage zunächst an den ausgefallenen Server gesendet wird. Ein häufiger Anwendungsfall sind extrem ausgelastete Server, deren Zustand ständig zwischen verfügbar und ausgefallen wechselt. Benutzer werden dann weiterhin an den Server geleitet, auf dem sie ihre Sitzung eröffnet haben, in der Hoffnung, dass ihre Anfrage korrekt bearbeitet wird. Es wird empfohlen, diese Option zusammen mit "option redispatch" zu verwenden: Kann überhaupt keine Verbindung zum Server hergestellt werden, weil er endgültig ausgefallen ist, wird der Client schließlich an einen anderen funktionsfähigen Server weitergeleitet.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option redispatch", "retries", "force-persist"

<a id="entry-4-2-option-pgsql-check-user"></a>

**`option pgsql-check user <username>`**

```haproxy
option pgsql-check user <username>
```

PostgreSQL-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<username> Der Benutzername für die Verbindung zum PostgreSQL-Server.
```

Die Prüfung sendet eine PostgreSQL-StartupMessage und wartet entweder auf eine Authentifizierungsanfrage oder eine ErrorResponse-Nachricht. Dies ist ein einfacher, aber nützlicher Test, der auf dem Server weder Fehler noch abgebrochene Verbindungsaufbauten erzeugt. Diese Prüfung entspricht "mysql-check".

Siehe auch: "option httpchk"

<a id="entry-4-2-option-prefer-last-server"></a>

**`option prefer-last-server`**

```haproxy
option prefer-last-server
no option prefer-last-server
```

Mehrere über die Lastverteilung zugewiesene Anfragen auf demselben Server belassen können

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Ist der verwendete Lastverteilungsalgorithmus nicht deterministisch und wurde eine vorherige Anfrage an einen Server gesendet, zu dem HAProxy noch eine Verbindung hält, ist es manchmal erwünscht, nachfolgende Anfragen derselben Sitzung möglichst an denselben Server zu senden. Dies unterscheidet sich von Sitzungsbindung: Es wird lediglich eine Präferenz angegeben, die HAProxy ohne jede Garantie umzusetzen versucht. Der eigentliche Anwendungsfall sind Keepalive-Verbindungen zu Servern. Bei dieser Option versucht HAProxy, dieselbe Verbindung zum Server wiederzuverwenden, statt die Anfrage einem anderen Server zuzuweisen und dadurch die bestehende Verbindung zu schließen. Für Server mit statischen Dateien kann dies sinnvoll sein. In Kombination mit Hashing-Algorithmen ist es wenig sinnvoll. Bei nicht deterministischer Lastverteilung versucht HAProxy bereits automatisch, bei einem Server zu bleiben, der 401 sendet, oder bei einem Proxy, der 407 sendet (Authentifizierung erforderlich). Dies ist für das fehlerhafte NTLM-Authentifizierungsverfahren zwingend erforderlich und erleichtert die Fehlersuche bei manchen mangelhaften Anwendungen erheblich. Auch in solchen Umgebungen kann option prefer-last-server sinnvoll sein, damit der Datenverkehr nicht nach jeder anderen Antwort neu verteilt wird.

Hier ist es hilfreich zu erläutern, welche Lastverteilungsalgorithmen als deterministisch gelten. Deterministische Algorithmen wählen für bestimmte Clientdaten immer denselben Server, sofern sich die Menge verfügbarer Server nicht geändert hat. Im Allgemeinen wählen sie den Zielserver durch Hashing oder Nachschlagen anhand der eingehenden Anfragen. Dies gilt jedoch nicht immer: Auch "static-rr" kann beispielsweise als deterministisch angesehen werden, weil die Serverauswahl auf dem statischen Servergewicht beruht und damit vorhersehbar ist. Der Algorithmus "sticky" bietet deterministisches Routing für wiederkehrende Clients.

Nicht deterministische Algorithmen wählen dagegen anhand des dynamischen Serverzustands oder einer einfachen Rotation aus. Daher ist nicht garantiert, dass zwei aufeinanderfolgende Anfragen denselben Server erreichen. option prefer-last-server ist speziell für solche Algorithmen vorgesehen; roundrobin und leastconn sind Beispiele dafür.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option http-keep-alive"

<a id="entry-4-2-option-redispatch"></a>

**`option redispatch`**

```haproxy
option redispatch
option redispatch <interval>
no option redispatch
```

Die erneute Verteilung von Sitzungen bei Verbindungsfehlern aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<interval> Der optionale ganzzahlige Wert, der bestimmt, wie oft bei
           erneuten Verbindungsversuchen eine Neuzuweisung erfolgt. Ein
           positiver Wert P fordert eine Neuzuweisung bei jedem P-ten Versuch
           an. Ein negativer Wert N fordert sie beim N-ten Versuch an, vom
           letzten Wiederholungsversuch aus rückwärts gezählt. So behält der Standardwert -1
           das bisherige Verhalten bei, beim letzten Versuch neu zuzuweisen.
           Ein positiver Wert von 1 bedeutet eine Neuzuweisung bei jedem
           Wiederholungsversuch, ein positiver Wert von 3 bei jedem dritten.
           Mit 0 können Neuzuweisungen deaktiviert werden.

```

Ist im HTTP-Modus ein durch ein Cookie bestimmter Server ausgefallen, können Clients dauerhaft an ihn gebunden bleiben, etwa bei "option persist" oder "force-persist". Da sie das Cookie nicht löschen können, ist ihnen dann der Zugriff auf den Dienst nicht mehr möglich.

Mit "option redispatch" darf der Proxy die cookie- oder auf konsistentem Hashing beruhende Sitzungsbindung aufheben und die Clients einem funktionierenden Server zuweisen.

Aktive Server werden aus einer Teilmenge der Liste verfügbarer Server ausgewählt. Aktive Server, die weder ausgefallen noch in Wartung sind, also entweder nicht auf ihren Zustand geprüft werden oder als "up" geprüft wurden, werden in folgender Reihenfolge ausgewählt:

```text
1. Ein beliebiger aktiver Server, der kein Backup-Server ist, falls
   vorhanden, oder

2. Falls "allbackups" nicht gesetzt ist, der erste Backup-Server in der
   Liste, oder

3. Falls "allbackups" gesetzt ist, ein beliebiger Backup-Server.
```

Bei einem Wiederholungsversuch versucht HAProxy, einen anderen als den zuletzt verwendeten Server auszuwählen. Der neue Server wird aus der aktuellen Serverliste gewählt.

Wird die Liste zwischen Wiederholungsversuchen aktualisiert, können Verbindungen gelegentlich auch zu einem Ersatzserver umgeleitet werden. Dies kann beispielsweise geschehen, wenn zahlreiche Wiederholungsversuche länger dauern als nötig, um den Ausfall eines Servers zu erkennen, ihn aus der Liste zu entfernen und auf die Ersatzserverliste zurückzufallen.

Die Option erlaubt außerdem, bei mehreren Verbindungsfehlern Verbindungen zu einem anderen Server erneut zu versuchen. Dafür muss "retries" auf einen Wert ungleich null gesetzt sein.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option persist", "force-persist", "retries"

<a id="entry-4-2-option-redis-check"></a>

**`option redis-check`**

```haproxy
option redis-check
```

Redis-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Es kann geprüft werden, ob der Server das REDIS-Protokoll korrekt verarbeitet, statt lediglich zu testen, ob er die TCP-Verbindung annimmt. Bei gesetzter Option wird der Redis-Befehl PING an den Server gesendet und die Antwort auf die Nachricht "+PONG" untersucht.

Beispiel:

```text
option redis-check
```

Siehe auch: "option httpchk", "option tcp-check", "tcp-check expect"

<a id="entry-4-2-option-smtpchk"></a>

**`option smtpchk`**

```haproxy
option smtpchk
option smtpchk <hello> <domain>
```

SMTP-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<hello>   ist ein optionales Argument für den zu verwendenden Befehl "hello".
          Möglich sind "HELO" für SMTP oder "EHLO" für ESMTP. Alle anderen
          Werte werden in den Standardbefehl "HELO" umgewandelt.

<domain>  ist der Domainname, der dem Server übermittelt wird. Er kann nur
          angegeben werden und ist dann zwingend erforderlich, wenn der
          hello-Befehl angegeben wurde. Standardmäßig wird "localhost" verwendet.
```

Bei gesetzter "option smtpchk" bestehen die Health Checks aus TCP-Verbindungen, auf die ein SMTP-Befehl folgt. Standardmäßig lautet dieser "HELO localhost". Der Rückgabecode des Servers wird ausgewertet; nur Codes, die mit "2" beginnen, gelten als gültig. Alle anderen Antworten, einschließlich einer ausbleibenden Antwort, gelten als Fehler und zeigen einen ausgefallenen Server an.

Dieser Test ist für SMTP-Server oder -Relays vorgesehen. Je nach Anfrage protokollieren manche Server möglicherweise nicht jeden Verbindungsversuch. Daher kann es sinnvoll sein, durch Versuche ein besseres Verhalten zu erreichen. Die Verwendung von Telnet auf Port 25 ist häufig einfacher als das Anpassen der Konfiguration.

Ein SMTP-Server benötigt häufig die IP-Adresse des Clients für verschiedene Zwecke, etwa Spamfilter, Schutz vor gefälschten Absendern und Protokollierung. Wenn möglich, ist es daher oft sinnvoll, beim Verbindungsaufbau zum Server mit dem Argument "usesrc" des Schlüsselworts "source" die IP-Adresse des Clients als eigene auszugeben. Dazu muss die Funktion für transparente Proxys einkompiliert sein.

Beispiel:

```text
option smtpchk HELO mydomain.org
```

Siehe auch: "option httpchk", "source"

```haproxy
option socket-stats
no option socket-stats
```

Das Erfassen und Bereitstellen getrennter Statistiken für jedes Socket aktivieren oder deaktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

<a id="entry-4-2-option-splice-auto"></a>

**`option splice-auto`**

```haproxy
option splice-auto
no option splice-auto
```

Die automatische Kernel-Beschleunigung für Sockets in beiden Richtungen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Ist diese Option im Frontend oder im Backend aktiviert, prüft HAProxy automatisch, ob TCP-Splicing im Kernel zur Weiterleitung von Daten zwischen Client und Server in einer der beiden Richtungen sinnvoll ist. HAProxy schätzt anhand von Heuristiken, ob Kernel-Splicing die Leistung verbessern könnte. Beide Richtungen werden unabhängig behandelt. Die Heuristiken sind bewusst zurückhaltend, um übermäßigen Einsatz von Splicing zu vermeiden. Diese Option erfordert, dass Splicing beim Kompilieren aktiviert wurde. Mit der globalen Option "nosplice" kann es global deaktiviert werden. Da splice Pipes verwendet, müssen dafür genügend freie Pipes vorhanden sein.

Wichtiger Hinweis: TCP-Splicing im Kernel ist eine Linux-spezifische Funktion, die erstmals in Kernel 2.6.25 erschien. Sie beschleunigt die Übertragung zwischen Sockets im Kernel, ohne Daten in den Benutzeradressraum zu kopieren. Dies kann die Leistung spürbar steigern und CPU-Zyklen sparen. Da viele frühe Implementierungen fehlerhaft sind, Daten beschädigen und/oder ineffizient arbeiten, ist die Funktion nicht standardmäßig aktiviert und sollte mit äußerster Vorsicht verwendet werden. Die Korrektheit einer Implementierung lässt sich zwar nicht erkennen, doch 2.6.29 ist die erste Version mit einer ordnungsgemäß funktionierenden Implementierung. Im Zweifelsfall kann Splicing mit dem globalen Schlüsselwort "nosplice" global deaktiviert werden.

Beispiel:

```text
option splice-auto
```

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option splice-request", "option splice-response" sowie die globalen Optionen "nosplice" und "maxpipes"

<a id="entry-4-2-option-splice-request"></a>

**`option splice-request`**

```haproxy
option splice-request
no option splice-request
```

Die automatische Kernel-Beschleunigung für Sockets bei Anfragen aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Ist diese Option im Frontend oder im Backend aktiviert, verwendet HAProxy nach Möglichkeit TCP-Splicing im Kernel, um Daten vom Client zum Server weiterzuleiten. Wenn keine freien Pipes mehr vorhanden sind, kann weiterhin das recv/send-Verfahren verwendet werden. Diese Option erfordert, dass Splicing beim Kompilieren aktiviert wurde. Mit der globalen Option "nosplice" kann es global deaktiviert werden. Da splice Pipes verwendet, müssen dafür genügend freie Pipes vorhanden sein.

Wichtiger Hinweis: Einschränkungen bei der Verwendung finden Sie unter "option splice-auto".

Beispiel:

```text
option splice-request
```

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option splice-auto", "option splice-response" sowie die globalen Optionen "nosplice" und "maxpipes"

<a id="entry-4-2-option-splice-response"></a>

**`option splice-response`**

```haproxy
option splice-response
no option splice-response
```

Die automatische Kernel-Beschleunigung für Sockets bei Antworten aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Ist diese Option im Frontend oder im Backend aktiviert, verwendet HAProxy nach Möglichkeit TCP-Splicing im Kernel, um Daten vom Server zum Client weiterzuleiten. Wenn keine freien Pipes mehr vorhanden sind, kann weiterhin das recv/send-Verfahren verwendet werden. Diese Option erfordert, dass Splicing beim Kompilieren aktiviert wurde. Mit der globalen Option "nosplice" kann es global deaktiviert werden. Da splice Pipes verwendet, müssen dafür genügend freie Pipes vorhanden sein.

Wichtiger Hinweis: Einschränkungen bei der Verwendung finden Sie unter "option splice-auto".

Beispiel:

```text
option splice-response
```

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option splice-auto", "option splice-request" sowie die globalen Optionen "nosplice" und "maxpipes"

<a id="entry-4-2-option-spop-check"></a>

**`option spop-check`**

```haproxy
option spop-check
```

SPOP-Health-Checks zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Es kann geprüft werden, ob der Server das SPOP-Protokoll korrekt verarbeitet, statt lediglich zu testen, ob er die TCP-Verbindung annimmt. Bei gesetzter Option findet ein HELLO-Handshake zwischen HAProxy und dem Server statt. Die Antwort wird darauf geprüft, dass kein Fehler gemeldet wird.

Beispiel:

```text
option spop-check
```

Siehe auch: "option httpchk"

<a id="entry-4-2-option-srvtcpka"></a>

**`option srvtcpka`**

```haproxy
option srvtcpka
no option srvtcpka
```

Das Senden von TCP-Keepalive-Paketen auf der Serverseite aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Befindet sich zwischen einem Client und einem Server eine Firewall oder eine andere Komponente, die Sitzungszustände verfolgt, und verwendet das Protokoll sehr lange Sitzungen mit langen inaktiven Phasen, etwa bei Remotedesktops, besteht ein Risiko: Eine zwischengeschaltete Komponente könnte eine zu lange inaktive Sitzung ablaufen lassen.

Werden TCP-Keepalives auf Socket-Ebene aktiviert, sendet das System regelmäßig Pakete an das andere Ende der Verbindung und hält diese damit aktiv. Der Abstand zwischen Keepalive-Prüfungen wird ausschließlich vom System gesteuert und hängt sowohl vom Betriebssystem als auch von dessen Abstimmungsparametern ab.

Keepalive-Pakete werden auf Anwendungsebene weder gesendet noch empfangen. Nur die Netzwerkstapel sehen sie. Selbst wenn also eine Seite des Proxys bereits Keepalives verwendet, um ihre Verbindung aktiv zu halten, werden diese Pakete nicht zur anderen Seite des Proxys weitergeleitet.

Dies hat nichts mit HTTP-Keepalive zu tun.

Die Option "srvtcpka" aktiviert das Senden von TCP-Keepalive-Prüfungen auf der Serverseite einer Verbindung. Dies sollte helfen, wenn zwischen HAProxy und einem Server Sitzungen ablaufen.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option clitcpka", "option tcpka"

<a id="entry-4-2-option-ssl-hello-chk"></a>

**`option ssl-hello-chk`**

```haproxy
option ssl-hello-chk
```

Health Checks mit SSLv3-Client-Hello zum Testen von Servern verwenden

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Wenn SSL-basierte Protokolle im TCP-Modus durch HAProxy weitergeleitet werden, kann geprüft werden, ob der Server SSL korrekt verarbeitet, statt lediglich zu testen, ob er die TCP-Verbindung annimmt. Bei gesetzter "option ssl-hello-chk" werden nach dem Verbindungsaufbau zum Server reine SSLv3-Client-Hello-Nachrichten gesendet. Die Antwort wird auf eine SSL-Server-Hello-Nachricht untersucht. Der Server gilt nur dann als funktionsfähig, wenn die Antwort diese Server-Hello-Nachricht enthält.

Alle bislang getesteten Server antworten korrekt auf SSLv3-Client-Hello-Nachrichten. Die meisten protokollieren Anfragen, die nur Hello-Nachrichten enthalten, nicht einmal, was von Vorteil ist.

Diese Prüfung funktioniert auch ohne einkompilierte SSL-Unterstützung in HAProxy, da sie die SSL-Nachricht selbst erzeugt. Ist SSL-Unterstützung verfügbar, sollten bevorzugt native SSL-Health-Checks verwendet werden.

Siehe auch: "option httpchk", "check-ssl"

<a id="entry-4-2-option-tcp-check"></a>

**`option tcp-check`**

```haproxy
option tcp-check
```

Health Checks mit tcp-check-send/expect-Sequenzen durchführen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Diese Prüfmethode ist für die Kombination mit "tcp-check"-Befehlslisten vorgesehen, um Health Checks mit send/expect-Sequenzen zu ermöglichen.

TCP-Prüfungen unterstützen derzeit 4 Betriebsarten: - keine "tcp-check"-Direktive: Der Health Check besteht nur aus einem Verbindungsversuch. Dies bleibt der Standardmodus.

    - Nur "tcp-check send" oder "tcp-check send-binary" ist angegeben: Beim
      Öffnen der Verbindung wird eine Zeichenkette gesendet. Bei manchen
      Protokollen lässt sich so beispielsweise eine "QUIT"-Nachricht senden,
      damit der Server nicht bei jedem Health Check einen Verbindungsfehler
      protokolliert. Das Prüfergebnis hängt weiterhin ausschließlich davon ab,
      ob sich die Verbindung öffnen lässt.

    - Nur "tcp-check expect" ist angegeben: Damit wird eine Begrüßungsmeldung
      geprüft. Die Verbindung wird geöffnet, und HAProxy wartet auf Inhalte
      vom Server, die bestimmte Regeln erfüllen müssen. Das Prüfergebnis
      richtet sich nach der Übereinstimmung zwischen Inhalt und Regeln.
      Dies eignet sich für POP, IMAP, SMTP, FTP, SSH und TELNET.

    - Sowohl "tcp-check send" als auch "tcp-check expect" sind angegeben:
      Damit wird ein Protokoll mit einem Begrüßungsaustausch geprüft. HAProxy
      sendet eine Nachricht, der Server antwortet, und die Antwort wird
      analysiert. Das Prüfergebnis richtet sich nach der Übereinstimmung
      zwischen Antwortinhalt und Regeln. Dies eignet sich häufig für Protokolle
      mit Bindung oder einem Anfrage-Antwort-Modell. Beispiele sind LDAP,
      MySQL, Redis und SSL, obwohl für sie bereits eigene Prüfungen mit einem
      tieferen Verständnis des jeweiligen Protokolls vorhanden sind.
      In diesem Modus können zahlreiche Anfragen gesendet und zahlreiche
      Antworten analysiert werden.

Ein fünfter Modus erlaubt das Einfügen von Kommentaren in verschiedene Schritte des Skripts.

Jeder erstellten tcp-check-Regel kann eine Direktive "comment" mit einer nachfolgenden Zeichenkette hinzugefügt werden. Diese Zeichenkette erscheint im Protokoll und im Debug-Modus auf stderr. Damit lassen sich verständliche Fehlermeldungen erstellen. "comment" ist selbstverständlich optional.

Während eines Health Checks steht ein Variablengültigkeitsbereich bereit, in dem mit "tcp-check set-var" Daten-Samples gespeichert werden können. Diese Variablen lassen sich mit "tcp-check
unset-var" freigeben.

Beispiele:

```shell
# perform a POP check (analyze only server's banner)
option tcp-check
tcp-check expect string +OK\ POP3\ ready comment POP\ protocol

# perform an IMAP check (analyze only server's banner)
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready comment IMAP\ protocol

# look for the redis master server after ensuring it speaks well
# redis protocol, then it exits properly.
# (send a command then analyze the response 3 times)
option tcp-check
tcp-check comment PING\ phase
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check comment role\ check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check comment QUIT\ phase
tcp-check send QUIT\r\n
tcp-check expect string +OK

Eine HTTP-Anfrage erstellen und anschließend die Antwort analysieren
(vor der Analyse mehrere Header senden)
option tcp-check
tcp-check comment forge\ and\ send\ HTTP\ request
tcp-check send HEAD\ /\ HTTP/1.1\r\n
tcp-check send Host:\ www.mydomain.com\r\n
tcp-check send User-Agent:\ HAProxy\ tcpcheck\r\n
tcp-check send \r\n
tcp-check expect rstring HTTP/1\..\ (2..|3..) comment check\ HTTP\ response

```

Siehe auch: "tcp-check connect", "tcp-check expect" und "tcp-check send".

<a id="entry-4-2-option-tcp-smart-accept"></a>

**`option tcp-smart-accept`**

```haproxy
option tcp-smart-accept
no option tcp-smart-accept
```

Das Einsparen eines ACK-Pakets bei der Verbindungsannahme aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente: keine

Geht eine HTTP-Verbindungsanfrage ein, bestätigt das System sie im Namen von HAProxy. Anschließend sendet der Client sofort seine Anfrage, die das System ebenfalls bestätigt, während es HAProxy über die neue Verbindung informiert. HAProxy liest daraufhin die Anfrage und antwortet. Das System sendet damit ein unnötiges TCP ACK, denn die Anfrage könnte ebenso gut beim Senden der Antwort durch HAProxy bestätigt werden.

Deshalb bittet HAProxy im HTTP-Modus das System automatisch, dieses unnötige ACK nicht zu senden, sofern die Plattform dies unterstützt, derzeit zumindest Linux. Dies darf keine Probleme verursachen, da das System das ACK ohnehin nach 40 ms sendet, falls die Antwort länger als erwartet ausbleibt.

Bei komplexer Netzwerkfehlersuche kann es sinnvoll sein, diese Optimierung zu deaktivieren: Verzögerte ACKs können es erschweren festzustellen, an welcher Stelle Pakete verzögert werden. Mit "no option
tcp-smart-accept" lässt sich dann zum normalen Verhalten zurückkehren.

Auch für Proxys ohne HTTP kann die Optimierung mit "option tcp-smart-accept" erzwungen werden. Dies kann beispielsweise bei Diensten wie SMTP sinnvoll sein, bei denen der Server zuerst spricht.

Es wird empfohlen, diese Option nicht in einem defaults-Abschnitt zu erzwingen. Im Zweifelsfall kann sie durch Voranstellen des Schlüsselworts "default" auf automatische Werte zurückgesetzt oder mit "no" deaktiviert werden.

Siehe auch: "option tcp-smart-connect"

<a id="entry-4-2-option-tcp-smart-connect"></a>

**`option tcp-smart-connect`**

```haproxy
option tcp-smart-connect
no option tcp-smart-connect
```

Das Einsparen eines ACK-Pakets beim Verbindungsaufbau aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Auf bestimmten Systemen, zumindest Linux, kann HAProxy den Kernel anweisen, bei einer Verbindungsanfrage nicht sofort ein leeres ACK zu senden, sondern direkt die gepufferte Anfrage. Das spart ein Netzwerkpaket und steigert die Leistung. Auch für manche Server kann dies nützlich sein, weil sie die Anfrage unmittelbar mit der eingehenden Verbindung erhalten.

Diese Funktion wird durch "option tcp-smart-connect" in einem Backend aktiviert. Sie ist nicht standardmäßig aktiviert, da sie die Netzwerkfehlersuche erschwert.

Ihre Aktivierung ist nur bei Protokollen sinnvoll, bei denen der Client zuerst spricht, etwa HTTP. In anderen Fällen wird ein normales ACK gesendet, wenn keine Daten anstelle des ACK gesendet werden können.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: "option tcp-smart-accept"

<a id="entry-4-2-option-tcpka"></a>

**`option tcpka`**

```haproxy
option tcpka
```

Das Senden von TCP-Keepalive-Paketen auf beiden Seiten aktivieren oder deaktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Befindet sich zwischen einem Client und einem Server eine Firewall oder eine andere Komponente, die Sitzungszustände verfolgt, und verwendet das Protokoll sehr lange Sitzungen mit langen inaktiven Phasen, etwa bei Remotedesktops, besteht ein Risiko: Eine zwischengeschaltete Komponente könnte eine zu lange inaktive Sitzung ablaufen lassen.

Werden TCP-Keepalives auf Socket-Ebene aktiviert, sendet das System regelmäßig Pakete an das andere Ende der Verbindung und hält diese damit aktiv. Der Abstand zwischen Keepalive-Prüfungen wird ausschließlich vom System gesteuert und hängt sowohl vom Betriebssystem als auch von dessen Abstimmungsparametern ab.

Keepalive-Pakete werden auf Anwendungsebene weder gesendet noch empfangen. Nur die Netzwerkstapel sehen sie. Selbst wenn also eine Seite des Proxys bereits Keepalives verwendet, um ihre Verbindung aktiv zu halten, werden diese Pakete nicht zur anderen Seite des Proxys weitergeleitet.

Dies hat nichts mit HTTP-Keepalive zu tun.

Die Option "tcpka" aktiviert das Senden von TCP-Keepalive-Prüfungen sowohl auf der Client- als auch auf der Serverseite einer Verbindung. Dies ist nur in "defaults"- oder "listen"-Abschnitten sinnvoll. Wird die Option in einem Frontend verwendet, erhält nur die Clientseite Keepalives; in einem Backend erhält nur die Serverseite Keepalives. Daher wird bei einer zwischen Frontends und Backends aufgeteilten Konfiguration dringend empfohlen, ausdrücklich "option clitcpka" und "option srvtcpka" zu verwenden.

Siehe auch: "option clitcpka", "option srvtcpka"

<a id="entry-4-2-option-tcplog"></a>

**`option tcplog [clf]`**

```haproxy
option tcplog [clf]
```

Die erweiterte Protokollierung von TCP-Verbindungen mit Streamstatus und Zeitmessungen aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
clf       Mit dem Argument "clf" wird das CLF-Format statt des
          standardmäßigen TCP-Formats von HAProxy ausgegeben. Dies ist
          nützlich, wenn die HAProxy-Protokolle mit einem bestimmten
          Protokollanalyseprogramm verarbeitet werden müssen, das nur
          CLF unterstützt und nicht erweiterbar ist. Da es ein HTTP-Format
          erwartet, sind einige Werte vorgegeben: Als HTTP-Anfrage erscheint
          TCP und als Antwortcode 000.
```

Standardmäßig ist das Protokollausgabeformat sehr knapp: Es enthält lediglich Quell- und Zieladressen sowie den Instanznamen. Mit "option tcplog" erhält jede Protokollzeile ein wesentlich ausführlicheres Format. Es enthält unter anderem Verbindungszeitmessungen, den Streamstatus, Verbindungszahlen, die Namen von Frontend, Backend und Server sowie natürlich Quelladresse und Ports. Bei reinen TCP-Proxys hilft diese Option festzustellen, ob der Client oder der Server die Verbindung trennt oder eine Zeitüberschreitung aufweist. Bei normalen HTTP-Proxys ist "option httplog" vorzuziehen, da es noch vollständiger ist.

"option tcplog" überschreibt jede vorherige "log-format"-Direktive.

Siehe auch: "option httplog" und [Abschnitt 8](/de/haproxy/configuration-logging/) zur Protokollierung.

<a id="entry-4-2-option-transparent"></a>

**`option transparent        (deprecated)`**

```haproxy
option transparent        (deprecated)
no option transparent     (deprecated)
```

Transparente Proxyverarbeitung auf der Clientseite aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Diese Option wurde eingeführt, um Load-Balancern auf Schicht 3 eine Sitzungsbindung auf Schicht 7 bereitzustellen. Dazu wird die Fähigkeit des Betriebssystems genutzt, eine eingehende Verbindung zu einer entfernten Adresse an einen lokalen Prozess, hier HAProxy, umzuleiten und diesem die ursprünglich angeforderte Adresse mitzuteilen. Bei dieser Option werden Sitzungen ohne Cookies an die ursprüngliche Ziel-IP-Adresse der eingehenden Anfrage weitergeleitet, die mit der eines anderen Geräts übereinstimmen sollte. Anfragen mit Cookies werden weiterhin an den passenden Server weitergeleitet.

Entgegen einer verbreiteten Annahme bewirkt diese Option NICHT, dass HAProxy beim Verbindungsaufbau dem Server die IP-Adresse des Clients präsentiert.

Seit 3.3 ist diese Option veraltet, da sie unter mehreren internen technischen Einschränkungen litt. Ihre Verwendung erzeugt eine Warnung, die bei tatsächlichem Bedarf mit dem globalen Schlüsselwort "expose-deprecated-directives" vermieden werden kann.

Der richtige Ansatz besteht darin, einen Server mit der Adresse 0.0.0.0 zu deklarieren, der die Verbindung zur erwarteten Zieladresse herstellt. Ein Server behandelt auch inaktive Verbindungen zu den Zielservern korrekt.

Beispiel:

```shell
# option transparent  ## before 3.3
server transparent 0.0.0.0
```

Siehe auch: das Argument "usesrc" des Schlüsselworts "source" und die Option "transparent" des Schlüsselworts "bind".

option use-small-buffers [ queue \| l7-retries \| check ]\*

Die Unterstützung kleiner Puffer für die angegebenen Kategorien aktivieren.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Mit dieser Option kann die Unterstützung kleiner Puffer an verschiedenen Stellen aktiviert werden, um Speicher zu sparen. Ohne Parameter werden kleine Puffer standardmäßig überall verwendet, wo dies möglich ist. Andernfalls lässt sich ihre Verwendung auf folgende Bereiche begrenzen:

- queue: Ist dies gesetzt, werden ausreichend kleine Anfragen in kleinen Puffern gespeichert, wenn die Verbindung in der Warteschlange steht.
- l7-retries: Ist dies gesetzt, werden Anfragen bei aktivierten L7-Wiederholungen in kleinen Puffern gesichert.
- check: Ist dies gesetzt, werden kleine Puffer für Anfragen für Health Checks verwendet.

Bei aktivierter Option werden kleine Puffer nur verwendet, wenn dies möglich ist. Sind die Daten zu groß, wird automatisch ein regulärer Puffer verwendet. Die Größe kleiner Puffer lässt sich über die globale Einstellung "tune.bufsize.small" konfigurieren.

Wurde diese Option in einem "defaults"-Abschnitt aktiviert, kann sie in einer bestimmten Instanz durch Voranstellen des Schlüsselworts "no" deaktiviert werden.

Siehe auch: tune.bufsize.small

<a id="entry-4-2-persist-rdp-cookie"></a>

**`persist rdp-cookie`**

```haproxy
persist rdp-cookie
persist rdp-cookie(<name>)
```

Sitzungsbindung anhand von RDP-Cookies aktivieren

Kann in folgenden Kontexten verwendet werden: tcp

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<name>    ist der optionale Name des zu prüfenden RDP-Cookies. Ohne Angabe
          wird der Standardname "msts" verwendet. Derzeit gibt es keinen
          triftigen Grund, diesen Namen zu ändern.
```

Diese Anweisung aktiviert die Sitzungsbindung anhand eines RDP-Cookies. Das RDP-Cookie enthält alle Informationen, die zur Suche des Servers in der Liste bekannter Server nötig sind. Ist diese Option im Backend gesetzt, wird die Anfrage analysiert. Wird ein RDP-Cookie gefunden, wird es dekodiert. Verweist es auf einen bekannten Server, wird die Verbindung an ihn weitergeleitet, sofern er noch UP ist oder "option persist" gesetzt ist.

Dies ist nur in einem TCP-Backend sinnvoll. Damit es funktioniert, muss das Frontend jedoch lange genug gewartet haben, um sicherzustellen, dass ein RDP-Cookie im Anfragepuffer vorliegt. Dies entspricht der Anforderung der Lastverteilungsmethode "rdp-cookie". Daher wird dringend empfohlen, alle Anweisungen in einem einzigen "listen"-Abschnitt unterzubringen.

Der Terminalserver gibt dieses RDP-Cookie nur aus, wenn er für "token redirection mode" konfiguriert ist. Das bedeutet, dass die Option "IP address redirection" deaktiviert ist.

Beispiel:

```text
listen tse-farm
    bind :3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # if server is unknown, let's balance on the same cookie.
    # alternatively, "balance leastconn" may be useful too.
    balance rdp-cookie
    server srv1 1.1.1.1:3389
    server srv2 1.1.1.2:3389
```

Siehe auch: "balance rdp-cookie", "tcp-request" und die ACL "req.rdp_cookie".

<a id="entry-4-2-quic-initial"></a>

**`quic-initial <action> [ { if | unless } <condition> ]`**

```haproxy
quic-initial <action> [ { if | unless } <condition> ]
```

Eine Aktion auf einem eingehenden QUIC-Initial-Paket ausführen. Anders als bei "tcp-request connection" geschieht dies bereits vor dem Erzeugen jeglicher Verbindungselemente sowie vor Beginn und Abschluss des SSL-Handshakes. Beim Ablehnen von Verbindungsversuchen ist dies effizienter.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| nein

Argumente:

```text
<action>    legt die auszuführende Aktion fest, wenn die Bedingung zutrifft.
            Siehe unten.

<condition> ist eine gewöhnliche ACL-basierte Bedingung ausschließlich auf
            Schicht 4 (siehe Abschnitt 7). QUIC-Initial-Regeln werden jedoch
            selbst für manche Sample-Abrufmethoden der Schicht 4 zu früh
            ausgeführt. Obwohl die Konfiguration keine Warnung ausgibt, kann
            dies zu nicht spezifiziertem Laufzeitverhalten führen, jedoch
            nicht zu Abstürzen. Als unterstützt gelten zurzeit nur interne
            Samples sowie "src*" und "dst*" auf Schicht 4.

```

Diese Aktion wird früh beim Parsen von QUIC-Paketen ausgeführt. Daher wird nur eine kleine Auswahl von Aktionen unterstützt: - accept - dgram-drop - reject - send-retry

<a id="entry-4-2-rate-limit-sessions"></a>

**`rate-limit sessions <rate>`**

```haproxy
rate-limit sessions <rate>
```

Die Anzahl neuer Sitzungen begrenzen, die ein Frontend pro Sekunde annimmt

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<rate>    Der Parameter <rate> ist eine ganze Zahl und gibt die maximale
          Zahl neuer Sitzungen pro Sekunde an, die das Frontend annimmt.
```

Erreicht das Frontend die angegebene Anzahl neuer Sitzungen pro Sekunde, nimmt es keine neuen Verbindungen mehr an, bis die Rate wieder unter die Grenze fällt. Währenddessen bleiben die wartenden Sitzungen im Backlog des Sockets, also in Systempuffern. HAProxy weiß dann nicht einmal, dass Sitzungen warten. Bei einer sehr niedrigen Grenze für einen stark ausgelasteten Dienst kann es sinnvoll sein, den Socket-Backlog mit dem Schlüsselwort "backlog" zu vergrößern.

Diese Funktion blockiert besonders wirksam verbindungsbasierte Angriffe oder missbräuchliche Nutzung von Diensten auf empfindlichen Servern. Da die Sitzungsrate jede Millisekunde gemessen wird, ist sie äußerst genau. Außerdem greift die Grenze sofort; zum Erkennen des Schwellenwerts ist keinerlei Verzögerung nötig.

Beispiel: Die SMTP-Verbindungsrate auf höchstens 10 pro Sekunde begrenzen.

```haproxy
listen smtp
    mode tcp
    bind :25
    rate-limit sessions 10
    server smtp1 127.0.0.1:1025
```


Hinweis: Bei Erreichen der maximalen Rate ändert sich der Frontendstatus nicht. Wenn die Option "socket-stats" aktiviert ist, erscheinen seine Sockets in den Statistiken jedoch als "WAITING".

Siehe auch: das Schlüsselwort "backlog" und das ACL-Kriterium "fe_sess_rate".

<a id="entry-4-2-redirect-location"></a>

**`redirect location <loc> [code <code>] <option> [{if | unless} <condition>]`**

```haproxy
redirect location <loc> [code <code>] <option> [{if | unless} <condition>]
redirect prefix   <pfx> [code <code>] <option> [{if | unless} <condition>]
redirect scheme   <sch> [code <code>] <option> [{if | unless} <condition>]
```

Eine HTTP-Weiterleitung zurückgeben, wenn eine Bedingung erfüllt beziehungsweise nicht erfüllt ist

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Ist die Bedingung bei if erfüllt beziehungsweise bei unless nicht erfüllt, führt die HTTP-Anfrage zu einer Weiterleitungsantwort. Ohne Bedingung gilt die Weiterleitung uneingeschränkt.

Argumente:

```text
<loc>     Bei "redirect location" wird der genaue Wert von <loc> in den
          HTTP-Header "Location" eingesetzt. In einer "http-request"-Regel
          folgt <loc> den Regeln für benutzerdefinierte Protokollformate und
          kann dynamische Werte enthalten (siehe benutzerdefinierte
          Protokollformate in Abschnitt 8.2.6).

<pfx>     Bei "redirect prefix" wird der Header "Location" aus <pfx> und
          dem vollständigen URI-Pfad zusammengesetzt, einschließlich der
          Abfragezeichenfolge, sofern nicht "drop-query" angegeben ist
          (siehe unten). Entspricht <pfx> genau "/", wird ausnahmsweise
          nichts vor die ursprüngliche URI gesetzt. Damit kann an dieselbe
          URL umgeleitet werden, etwa um ein Cookie einzufügen. In einer
          "http-request"-Regel folgt <pfx> den Regeln für benutzerdefinierte
          Protokollformate und kann dynamische Werte enthalten (siehe
          benutzerdefinierte Protokollformate in Abschnitt 8.2.6).

<sch>     Bei "redirect scheme" wird der Header "Location" aus <sch>,
          "://", dem ersten Vorkommen des Headers "Host" und dem URI-Pfad
          zusammengesetzt. Die Abfragezeichenfolge wird einbezogen, sofern
          nicht "drop-query" angegeben ist (siehe unten). Fehlt ein Pfad
          oder lautet er "*", wird stattdessen "/" verwendet. Fehlt ein
          "Host"-Header, wird eine leere Hostkomponente zurückgegeben. Die
          meisten neueren Browser interpretieren dies als Weiterleitung an
          denselben Host. Diese Direktive dient hauptsächlich zur Weiterleitung
          von HTTP auf HTTPS. In einer "http-request"-Regel folgt <sch>
          den Regeln für benutzerdefinierte Protokollformate und kann
          dynamische Werte enthalten (siehe benutzerdefinierte Protokollformate
          in Abschnitt 8.2.6).

<code>    Der optionale Code gibt die gewünschte Art der HTTP-Weiterleitung
          an. Unterstützt werden nur 301, 302, 303, 307 und 308; ohne
          Angabe ist 302 der Standard. 301 bedeutet "Moved permanently";
          ein Browser kann Location zwischenspeichern. 302
          bedeutet "Moved temporarily"; der Browser sollte die Weiterleitung
          nicht zwischenspeichern. 303 entspricht 302, allerdings ruft der
          Browser das Ziel mit GET ab. 307 entspricht ebenfalls 302, stellt
          jedoch klar, dass dieselbe Methode erneut verwendet werden muss.
          Ebenso ersetzt 308 den Code 301, wenn dieselbe Methode verwendet
          werden muss.

<option>  Mehrere Optionen erlauben die Anpassung des gewünschten Verhaltens
          einer Weiterleitung:

  - "drop-query"
    Bei einer präfixbasierten Weiterleitung wird das Ziel mit diesem
    Schlüsselwort ohne eine mögliche Abfragezeichenfolge gesetzt. Dies ist
    etwa nützlich, um Benutzer auf eine ungesicherte Seite zu leiten. Bei
    Weiterleitungen vom Typ location hat es keine Wirkung.

  - "append-slash"
    Dieses Schlüsselwort kann mit "drop-query" kombiniert werden, um Benutzer
    von einer URL ohne abschließenden '/' an dieselbe URL mit '/' umzuleiten.
    Damit lässt sich sicherstellen, dass Suchmaschinen nur eine URL sehen.
    Dafür ist der Antwortcode 301 vorzuziehen.

  - "ignore-empty"
    Dieses Schlüsselwort wirkt nur, wenn das Weiterleitungsziel durch einen
    Protokollformatausdruck erzeugt wird, also bei Verwendung in http-request
    oder http-response. Ist das Ergebnis des Ausdrucks leer, sollte die
    Regel ohne Meldung übersprungen werden. Dies dient hauptsächlich dazu,
    viele bekannte Pfade über eine einfache Zuordnungstabelle umzuleiten.

  - "set-cookie NAME[=value]"
    Der Antwort wird ein Header "Set-Cookie" mit NAME und optional "=value"
    hinzugefügt. Dies zeigt gelegentlich an, dass ein Benutzer bereits
    gesehen wurde, etwa zum Schutz vor bestimmten DoS-Arten. Weitere
    Cookie-Optionen werden nicht hinzugefügt; es handelt sich also um ein
    Sitzungscookie. Für einen Browser unterscheidet sich ein bloßer
    Cookie-Name ohne Gleichheitszeichen von einem Cookie mit Gleichheitszeichen.

  - "set-cookie-fmt <fmt>"
    Entspricht der obigen Option, befüllt den Header "Set-Cookie" jedoch
    mit dem Ergebnis der Auswertung der Protokollformatzeichenfolge <fmt>.
    Auf die Einhaltung des Formats "NAME[=value]" achten, da beim Einlesen
    der Konfiguration keine besondere Prüfung erfolgt.

  - "clear-cookie NAME[=]"
    Ein Header "Set-Cookie" mit NAME und optional "=" wird hinzugefügt,
    jedoch mit dem Attribut "Max-Age" auf null. Dies weist den Browser
    an, das Cookie zu löschen, etwa auf Abmeldeseiten. Das Löschen von
    "NAME" entfernt jedoch kein mit "NAME=value" gesetztes Cookie.
    Dafür muss "NAME=" gelöscht werden, da der Browser diese Formen
    unterscheidet.

  - "keep-query"
    Bei einer Weiterleitung vom Typ location wird mit diesem Schlüsselwort
    eine vorhandene Abfragezeichenfolge der ursprünglichen URI an das Ziel
    angehängt. Fehlt die Abfragezeichenfolge, wird nichts hinzugefügt. Enthält
    das Ziel bereits eine Abfragezeichenfolge, wird die ursprüngliche mit
    dem Trennzeichen '&' angehängt.

```

Beispiel: Nur die Anmelde-URL auf HTTPS umstellen.

```haproxy
acl clear      dst_port  80
acl secure     dst_port  8080
acl login_page url_beg   /login
acl logout     url_beg   /logout
acl uid_given  url_reg   /login?userid=[^&]+
acl cookie_set hdr_sub(cookie) SEEN=1

redirect prefix   https://mysite.com set-cookie SEEN=1 if !cookie_set
redirect prefix   https://mysite.com           if login_page !secure
redirect prefix   http://mysite.com drop-query if login_page !uid_given
redirect location http://mysite.com/           if !login_page secure
redirect location / clear-cookie USERID=       if logout
```



Beispiel: Anfragen nach Artikeln ohne '/' weiterleiten.

```haproxy
acl missing_slash path_reg ^/article/[^/]*$
redirect code 301 prefix / drop-query append-slash if missing_slash
```


Beispiel: Sämtlichen HTTP-Verkehr auf HTTPS weiterleiten, wenn SSL durch HAProxy verarbeitet wird.

```haproxy
redirect scheme https if !{ ssl_fc }
```


Beispiel: Allen Hosts ohne 'www.' dieses Präfix voranstellen.

```haproxy
http-request redirect code 301 location      \
  http://www.%[hdr(host)]%[capture.req.uri]  \
  unless { hdr_beg(host) -i www }
```


Beispiel: Nur alte URLs dauerhaft auf neue weiterleiten.

```haproxy
http-request redirect code 301 location               \
  %[path,map_str(old-blog-articles.map)] ignore-empty
```


Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-retries"></a>

**`retries <value>`**

```haproxy
retries <value>
```

Die Anzahl der Wiederholungsversuche auf einem Server nach einem Fehler festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<value>   ist die Zahl der Wiederholungen, die nach einem Fehler für eine
          Anfrage oder einen Verbindungsversuch zu einem Server erfolgen sollten.
```

Standardmäßig gelten Wiederholungen nur für neue Verbindungsversuche. Mit der Direktive "retry-on" können jedoch andere Bedingungen eine Wiederholung auslösen, etwa eine leere Antwort oder ein unerwünschter Statuscode. Jede davon zählt als ein Versuch. Sobald die Gesamtzahl der Versuche den hier angegebenen Wert erreicht, wird ein Fehler zurückgegeben.

Um sofortige neue Verbindungsversuche zu einem gerade neu startenden Server zu vermeiden, wird vor einer Wiederholung auf demselben Server eine Wartezeit von min("timeout connect", eine Sekunde) eingehalten.

Bei gesetzter "option redispatch" können manche Wiederholungen auf einem anderen Server erfolgen, selbst wenn ein Cookie auf einen anderen Server verweist. Standardmäßig gilt dies nur für den letzten Wiederholungsversuch, sofern "option redispatch" kein Argument übergeben wurde.

Siehe auch: "option redispatch"

<a id="entry-4-2-retry-on"></a>

**`retry-on [space-delimited list of keywords]`**

```haproxy
retry-on [space-delimited list of keywords]
```

Festlegen, wann automatisch versucht werden soll, eine fehlgeschlagene Anfrage zu wiederholen. Diese Einstellung ist nur gültig, wenn "mode" auf http gesetzt ist; andernfalls wird sie stillschweigend ignoriert.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
 <keywords>  ist eine durch Leerzeichen getrennte Liste von Schlüsselwörtern
             oder HTTP-Statuscodes. Jeder Eintrag bezeichnet eine Fehlerart,
             bei der ein erneuter Anfrageversuch gewünscht ist. Vor einer
             Änderung dieser Einstellung die Hinweise am Ende lesen.
             Unterstützt werden folgende Schlüsselwörter:

   none              Niemals erneut versuchen.

   conn-failure      Erneut versuchen, wenn die Verbindung oder der
                     SSL-Handshake fehlschlug und die Anfrage nicht gesendet
                     werden konnte. Dies ist der Standard.

   empty-response    Erneut versuchen, wenn die Serververbindung geschlossen
                     wurde, nachdem ein Teil der Anfrage gesendet worden war,
                     aber noch nichts vom Server empfangen wurde. Mögliche
                     Ursachen sind eine Anfragezeitüberschreitung auf dem
                     Server, schlechte Netzwerkbedingungen oder ein Absturz
                     bzw. Neustart des Servers während der Verarbeitung.

   junk-response     Erneut versuchen, wenn der Server etwas zurückgibt, das
                     nicht wie eine vollständige HTTP-Antwort aussieht.
                     Dazu zählen unvollständige Antwortheader sowie Inhalte
                     außerhalb von HTTP. Wiederholungen sind bei solchen
                     Ereignissen meist keine gute Idee: Ursache können eine
                     Fehlkonfiguration, etwa ein falscher Serverport, oder
                     eine schädliche Anfrage sein, etwa ein Angriff durch
                     Pufferüberlauf.

   response-timeout  Die Serverzeitüberschreitung trat beim Warten auf die
                     Antwort zur Anfrage ein. Mögliche Ursachen sind schlechte
                     Netzwerkbedingungen, die Wiederverwendung einer unterwegs
                     abgelaufenen inaktiven Verbindung oder eine besonders
                     aufwendige Anfrage. Bei Servern mit aufwendiger
                     Datenbankverarbeitung, etwa vollständigen Tabellenscans,
                     sind Wiederholungen meist keine gute Idee, da sie
                     Denial-of-Service-Angriffe verstärken können.

   0rtt-rejected     Anfragen erneut versuchen, die als Early Data gesendet
                     und vom Server abgelehnt wurden. Die Wiederholung
                     solcher Anfragen gilt im Allgemeinen als sicher.

   <status>          Einer der HTTP-Statuscodes "401" (Unauthorized), "403"
                     (Forbidden), "404" (Not Found), "408" (Request Timeout),
"421" (Misdirected Request), "425" (Too Early),
"429" (Too Many Requests), "500" (Server Error),
"501" (Not Implemented), "502" (Bad Gateway),
"503" (Service Unavailable), "504" (Gateway Timeout).

   all-retryable-errors
                     Anfrage bei jedem als wiederholbar eingestuften Fehler
                     erneut versuchen. Dies aktiviert derzeit "conn-failure",
                     "empty-response", "junk-response", "response-timeout",
                     "0rtt-rejected", "500", "502", "503" und "504".
```

Diese Direktive ersetzt alle vorherigen Einstellungen durch die neuen; sie wirkt nicht kumulativ.

Jeder andere Wert als "none" und "conn-failure" erfordert das Reservieren eines Puffers und das Kopieren der gesamten Anfrage in diesen Puffer. Dies wirkt sich auf Speicherverbrauch und Leistung aus. Anfragen, die nicht in einen einzelnen Puffer passen, werden niemals wiederholt; siehe die globale Einstellung tune.bufsize.

Sie müssen sicherstellen, dass die Anwendung einen Schutz gegen wiederholte Ausführung besitzt, etwa eindeutige Transaktions-IDs in Anfragen, oder dass die Wiederholung derselben Anfrage folgenlos bleibt. Andernfalls ist jeder retry-on-Wert außer "conn-failure" und "none" sehr gefährlich. Server für statische Dateien und Caches gelten im Allgemeinen bei jeder Art von Wiederholung als sicher. Die Verwendung eines Statuscodes kann nützlich sein, um einen auffällig arbeitenden Server rasch zu verlassen, etwa bei Speichermangel oder Dateisystemproblemen. In diesem Fall kann es jedoch sinnvoll sein, die Verbindung sofort einem anderen Server zuzuweisen; siehe dazu "option redispatch". Schließlich ist zu bedenken, dass die meisten Fehler durch die Anfragen selbst verursacht werden. Das Wiederholen einer Anfrage, die einen Server zu fehlerhaftem Verhalten bringt, verschlechtert daher häufig die Lage dieses Servers oder bei erneuter Zuweisung sogar die des gesamten Dienstes.

Wenn Sie nicht genau wissen, wie die Anwendung mit wiederholten Anfragen umgeht, sollten Sie diese Direktive nicht verwenden.

Der Standardwert ist "conn-failure".

Beispiel:

```text
retry-on 503 504
```

Siehe auch: "retries", "option redispatch", "tune.bufsize"

<a id="entry-4-2-server"></a>

**`server <name> <address>[:[port]] [param*]`**

```haproxy
server <name> <address>[:[port]] [param*]
```

Einen Server in einem Backend deklarieren

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<name>    ist der diesem Server zugewiesene interne Name. Er erscheint in
          Protokollen und Warnungen. Ist "http-send-name-header" gesetzt,
          wird er dem an den Server gesendeten Anfrageheader hinzugefügt.
          Dieser Name muss innerhalb des backend-Abschnitts eindeutig sein.

<address> ist die IPv4- oder IPv6-Adresse des Servers. Alternativ wird ein
          auflösbarer Hostname unterstützt, der jedoch beim Start aufgelöst
          wird. Die Adressen "0.0.0.0" und "*" haben eine besondere Bedeutung:
          Die Verbindung wird an dieselbe IP-Adresse wie die Clientverbindung
          weitergeleitet. Dies ist bei transparenten Proxy-Architekturen
          nützlich, in denen die Clientverbindung abgefangen wird und HAProxy
          an die ursprüngliche Zieladresse weiterleiten muss. Es entspricht
          ungefähr dem Schlüsselwort "transparent", erlaubt mit einem Server
          jedoch die Begrenzung der Parallelität und die Ausgabe von
          Statistiken. Optional kann der Adresse ein Adressfamilienpräfix
          vorangestellt werden, das die Familie unabhängig vom Adressformat
          erzwingt. So lässt sich etwa ein Unix-Socket-Pfad ohne Schrägstrich
          ('/') angeben. Zurzeit werden folgende Präfixe unterstützt:
                - 'ipv4@'  -> Adresse ist immer IPv4.
                - 'ipv6@'  -> Adresse ist immer IPv6.
                - 'unix@'  -> Adresse ist ein Pfad zu einem lokalen Unix-Socket.
                - 'abns@'  -> Adresse liegt im abstrakten Namensraum (nur Linux).
                - 'abnsz@'  -> Adresse liegt im abstrakten Namensraum (nur Linux),
                   wird jedoch ausdrücklich mit einem Nullzeichen beendet.
                   sun_path wird also nicht mit \0 aufgefüllt. Dies ist
                   für Verbindungen mit Programmen nützlich, die die von
                   haproxy standardmäßig verwendete abns-Namenslogik nicht
                   umsetzen.
                - 'sockpair@' -> Adresse ist der FD eines verbundenen
                  Unix-Sockets oder eines Socketpaars. Beim Verbindungsaufbau
                  erzeugt das Backend ein Paar verbundener Sockets und
                  übergibt einen davon über den FD. Die bind-Seite verwendet
                  den empfangenen Socket als Client-FD. Sollte mit Vorsicht
                  verwendet werden.
                - 'quic4@' [ EXPERIMENTAL] -> Adresse wird als IPv4 aufgelöst
                  und das Protokoll UDP verwendet. QUIC auf der Backend-Seite
                  gilt hauptsächlich deshalb als experimentell, weil Server
                  damit nicht zur Laufzeit entfernt werden können. Die
                  Verwendung erfordert das globale Schlüsselwort
                  "expose-experimental-directives".
                - 'quic6@' [ EXPERIMENTAL] -> Adresse wird als IPv6 aufgelöst
                  und das Protokoll UDP verwendet. Dies gilt ebenfalls als
                  experimentell.
                - 'rhttp@' [ EXPERIMENTAL ] -> eigene Adressfamilie für einen
                  passiven Server im Kontext von umgekehrtem HTTP. Diese
                  experimentelle Funktion erfordert
                  "expose-experimental-directives" in einer Zeile vor
                  diesem Server.
          Im Adressparameter können Umgebungsvariablen verwendet werden;
          siehe Abschnitt 2.3 zu Umgebungsvariablen. Mit "init-addr" lässt
          sich ändern, wie IP-Adressen beim Start aufgelöst werden sollen.

<port>    ist eine optionale Portangabe. Ist sie gesetzt, werden alle
          Verbindungen an diesen Port gesendet. Andernfalls wird der Port
          verwendet, zu dem sich der Client verbunden hat. Dem Port kann
          auch ein "+" oder "-" vorangestellt werden. Dann wird dieser
          Wert zum Clientport addiert, um den Serverport zu bestimmen.

<param*>  ist eine Liste von Parametern für diesen Server. Das Schlüsselwort
          "server" akzeptiert zahlreiche Optionen, denen ein eigener
          Abschnitt gewidmet ist. Weitere Einzelheiten stehen in Abschnitt 5.
```

Beispiele:

```text
server first  10.1.1.1:1080 cookie first  check inter 1000
server second 10.1.1.2:1080 cookie second check inter 1000
server transp ipv4@
server backup "${SRV_BACKUP}:1080" backup
server www1_dc1 "${LAN_DC1}.101:80"
server www1_dc2 "${LAN_DC2}.101:80"
```

Hinweis: Bei Sockets im abstrakten Namensraum von Linux verwenden HAProxy-Sockets der Familie "abns" die gesamte Länge von sun_path als Adresslänge. Andere Programme wie socat verwenden standardmäßig nur die Länge der Zeichenkette. Übergeben Sie der Definition eines abstrakten Sockets in socat die Option ",unix-tightsocklen=0", um Kompatibilität mit HAProxy zu erreichen, oder verwenden Sie stattdessen die HAProxy-Socket-Familie "abnsz".

Siehe auch: "default-server", "http-send-name-header" und [Abschnitt 5](/de/haproxy/bind-and-server-options/) zu Serveroptionen

<a id="entry-4-2-server-state-file-name"></a>

**`server-state-file-name [ { use-backend-name | <file> } ]`**

```haproxy
server-state-file-name [ { use-backend-name | <file> } ]
```

Die Serverzustandsdatei festlegen, die gelesen und geladen wird und deren Zustände auf die Server dieses Backends angewendet werden.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Dies gilt nur, wenn die Direktive "load-server-state-from-file" auf "local" gesetzt ist. Wenn `<file>` nicht angegeben ist, wenn "use-backend-name" verwendet wird oder wenn diese Direktive nicht gesetzt ist, wird der Backendname verwendet. Beginnt `<file>` mit einem Schrägstrich '/', gilt es als absoluter Pfad. Andernfalls wird `<file>` an den Wert der globalen Direktive "server-state-base" angehängt.

Beispiel: Mit der folgenden minimalen Konfiguration würde HAProxy die Serverzustandsdatei '/etc/haproxy/states/bk' suchen:

    global
      server-state-file-base /etc/haproxy/states

    backend bk
      load-server-state-from-file

Siehe auch: "server-state-base", "load-server-state-from-file" und "show servers state"

<a id="entry-4-2-server-template"></a>

**`server-template <prefix> <num | range> <fqdn>[:<port>] [params*]`**

```haproxy
server-template <prefix> <num | range> <fqdn>[:<port>] [params*]
```

Eine Vorlage zur Initialisierung von Servern mit gemeinsamen Parametern festlegen. Die Namen dieser Server werden aus den Parametern `<prefix>` und \<num \| range\> gebildet.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<prefix>  Ein Präfix für die zu erzeugenden Servernamen.

<num | range>
          Ist <num> angegeben, initialisiert diese Vorlage <num> Server mit
          den Namenssuffixen 1 bis <num>. Alternativ kann ein Zahlenbereich
          <num_low>-<num_high> angegeben werden, um <num_low> bis <num_high>
          als Servernamenssuffixe zu verwenden.

<fqdn>    Ein FQDN für alle Server, die diese Vorlage initialisiert.

<port>    Dieselbe Bedeutung wie das Argument <port> von "server"
          (siehe Schlüsselwort "server").

<params*>
          Weitere Serverparameter aus allen vom Schlüsselwort "server"
          unterstützten Parametern.
```

Beispiele:

```shell
# Initializes 3 servers with srv1, srv2 and srv3 as names,
# google.com as FQDN, and health-check enabled.
server-template srv 1-3 google.com:80 check

# or
server-template srv 3 google.com:80 check

# would be equivalent to:
server srv1 google.com:80 check
server srv2 google.com:80 check
server srv3 google.com:80 check


```

<a id="entry-4-2-source"></a>

**`source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<port>] [interface <name>]
```

Die Quelladresse für ausgehende Verbindungen festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<addr>    ist die IPv4-Adresse, an die HAProxy vor einer Verbindung zu einem
          Server bindet. Diese Adresse dient auch als Quelle für Health Checks.

          Der Standardwert 0.0.0.0 bedeutet, dass das System die geeignetste
          Adresse zum Erreichen des Ziels auswählt. Optional kann ein
          Adressfamilienpräfix vorangestellt werden, das die Familie unabhängig
          vom Adressformat erzwingt. So lässt sich etwa ein Unix-Socket-Pfad
          ohne Schrägstrich ('/') angeben. Zurzeit werden folgende Präfixe
          unterstützt:
            - 'ipv4@' -> Adresse ist immer IPv4.
            - 'ipv6@' -> Adresse ist immer IPv6.
            - 'unix@' -> Adresse ist ein Pfad zu einem lokalen Unix-Socket.
            - 'abns@' -> Adresse liegt im abstrakten Namensraum (nur Linux).
            - 'abnsz@'  -> Adresse liegt im mit Nullzeichen abgeschlossenen
                           abstrakten Namensraum (nur Linux).

          Im Adressparameter können Umgebungsvariablen verwendet werden;
          siehe Abschnitt 2.3 zu Umgebungsvariablen.

<port>    ist ein optionaler Port. Normalerweise ist er nicht nötig, kann
          aber in besonderen Fällen nützlich sein. Der Standardwert null
          bedeutet, dass das System einen freien Port auswählt. Portbereiche
          werden im Backend nicht unterstützt. Um Portbereiche zu erzwingen,
          müssen sie in jeder "server"-Zeile angegeben werden.

<addr2>   ist die dem Server präsentierte IP-Adresse, wenn Verbindungen im
          vollständig transparenten Proxy-Modus weitergeleitet werden. Dies
          wird derzeit nur von einigen angepassten Linux-Kerneln unterstützt.
          Ist diese Adresse angegeben, werden Verbindungen von Clients zum
          Server mit dieser Adresse präsentiert. Health Checks verwenden
          weiterhin <addr>.

<port2>   ist der optionale Port, der dem Server bei Weiterleitung von
          Verbindungen im vollständig transparenten Proxy-Modus präsentiert
          wird (siehe <addr2> oben). Der Standardwert null bedeutet, dass
          das System einen freien Port auswählt.

<hdr>     ist der Name eines HTTP-Headers, aus dem die IP-Adresse zum Binden
          abgerufen wird. Er bezeichnet eine durch Kommas getrennte Headerliste,
          die mehrere IP-Adressen enthalten kann. Standardmäßig wird das
          letzte Vorkommen verwendet. Dies ist für X-Forwarded-For vorgesehen,
          um automatisch an die Client-IP-Adresse zu binden, wie sie der
          vorherige Proxy, meist Stunnel, gesehen hat. Für ein anderes als
          das letzte Vorkommen siehe den Parameter <occ> unten. Wird der
          Header oder das Vorkommen nicht gefunden, erfolgt keine Bindung;
          dann wird die Standard-IP-Adresse des Proxys verwendet. Wie bei
          jedem HTTP-Header wird beim Headernamen nicht zwischen Groß- und
          Kleinschreibung unterschieden.

<occ>     ist die Nummer des zu verwendenden Wertes in einem Header mit
          mehreren Werten. Zusammen mit "hdr_ip(<hdr>)" legt sie fest,
          welches Vorkommen als Quell-IP-Adresse verwendet wird. Positive
          Werte zählen vom ersten Vorkommen aus, wobei 1 das erste ist.
          Negative Werte zählen vom letzten aus, wobei -1 das letzte ist.
          Dies hilft, wenn ein X-Forwarded-For-Header am Eingang einer
          Infrastruktur gesetzt wird und mehrere Proxy-Ebenen weiter
          verwendet werden muss. Ohne Angabe wird -1 angenommen. Der Wert
          null deaktiviert diese Funktion.

<name>    ist der optionale Name einer Schnittstelle, an die ausgehender
          Datenverkehr gebunden wird. Auf Systemen mit dieser Unterstützung,
          derzeit nur Linux, lässt sich so der gesamte Datenverkehr zum
          Server an diese Schnittstelle binden, selbst wenn die Routingtabellen
          eine andere vorsehen. Dies sollte mit äußerster Vorsicht verwendet
          werden. Diese Option erfordert Root-Rechte.
```

Das Schlüsselwort "source" ist in komplexen Umgebungen nützlich, in denen nur eine bestimmte Adresse Verbindungen zu den Servern herstellen darf. Dies kann beispielsweise nötig sein, wenn eine private Adresse über ein öffentliches Gateway verwendet werden muss und bekannt ist, dass das System die passende Quelladresse nicht selbst bestimmen kann.

Mit dem optionalen Schlüsselwort "usesrc" lässt sich eine Erweiterung verwenden, die auf bestimmten gepatchten Linux-Kerneln verfügbar ist. Sie ermöglicht Verbindungen zu den Servern mit einer IP-Adresse, die nicht zum System selbst gehört. Dies wird als vollständig transparenter Proxymodus bezeichnet. Damit dies funktioniert, müssen die Zielserver ihren Rückverkehr zu dieser Adresse über den Rechner mit HAProxy routen. Auf diesem Rechner muss in der Regel IP-Weiterleitung aktiviert sein.

In diesem vollständig transparenten Proxymodus kann erzwungen werden, dass den Servern eine bestimmte IP-Adresse präsentiert wird. Dies wird tatsächlich selten verwendet. Häufiger soll HAProxy die IP-Adresse des Clients präsentieren. Dafür gibt es zwei Verfahren:

    - Die IP-Adresse und den Port des Clients präsentieren. Dies ist der
      transparenteste Modus, kann jedoch bei aktivierter IP-Verbindungsverfolgung
      auf dem Rechner Probleme verursachen: Dieselbe Verbindung kann zweimal
      mit unterschiedlichen Zuständen erscheinen. Der große Vorteil ist jedoch,
      dass das System nicht auf 64k ausgehende Adress-Port-Kombinationen begrenzt
      ist, da sämtliche Clientbereiche verwendet werden können.

    - Nur die IP-Adresse des Clients präsentieren und einen freien Port wählen.
      Diese Lösung ist weiterhin recht elegant, aber etwas weniger transparent:
      Die Protokolle nachgeschalteter Firewalls stimmen nicht mit denen der
      vorgeschalteten überein. Außerdem ist die Anzahl gleichzeitiger
      Verbindungen auf die üblichen 64k Ports begrenzt. Da sich die Ports auf
      beiden Seiten unterscheiden, wird die lokale IP-Verbindungsverfolgung
      des Rechners jedoch nicht durch die Wiederverwendung derselben Sitzung
      gestört.

Diese Option legt die Standardquelle für alle Server des Backends fest. Sie kann auch in einem "defaults"-Abschnitt angegeben werden. Eine genauere Festlegung der Quelladresse auf Serverebene ist mit der Serveroption "source" möglich. Weitere Informationen enthält [Abschnitt 5](/de/haproxy/bind-and-server-options/).

"usesrc" benötigt root-Rechte oder auf unterstützten Systemen die Capability "cap_net_raw". Siehe auch die globale Direktive "setcap".

Beispiele:

```text
backend private
    # Connect to the servers using our 192.168.1.200 source address
    source 192.168.1.200

backend transparent_ssl1
    # Connect to the SSL farm from the client's source address
    source 192.168.1.200 usesrc clientip

backend transparent_ssl2
    # Connect to the SSL farm from the client's source address and port
    # not recommended if IP conntrack is present on the local machine.
    source 192.168.1.200 usesrc client

backend transparent_ssl3
    # Connect to the SSL farm from the client's source address. It
    # is more conntrack-friendly.
    source 192.168.1.200 usesrc clientip

backend transparent_smtp
    # Connect to the SMTP farm from the client's source address/port
    # with Tproxy version 4.
    source 0.0.0.0 usesrc clientip

backend transparent_http
    # Connect to the servers using the client's IP as seen by previous
    # proxy.
    source 0.0.0.0 usesrc hdr_ip(x-forwarded-for,-1)
```

Siehe auch: die Serveroption "source" in [Abschnitt 5](/de/haproxy/bind-and-server-options/), die Tproxy-Patches für den Linux-Kernel auf [www.balabit.com](http://www.balabit.com) und das Schlüsselwort "bind".

<a id="entry-4-2-srvtcpka-cnt"></a>

**`srvtcpka-cnt <count>`**

```haproxy
srvtcpka-cnt <count>
```

Die maximale Anzahl von Keepalive-Prüfungen festlegen, die TCP auf der Serverseite senden soll, bevor es die Verbindung trennt.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<count>   ist die maximale Zahl der Keepalive-Prüfungen.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPCNT. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_probes) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option srvtcpka", "srvtcpka-idle", "srvtcpka-intvl".

<a id="entry-4-2-srvtcpka-idle"></a>

**`srvtcpka-idle <timeout>`**

```haproxy
srvtcpka-idle <timeout>
```

Die Zeit festlegen, die eine Verbindung inaktiv bleiben muss, bevor TCP Keepalive-Prüfungen sendet, sofern das Senden von TCP-Keepalive-Paketen auf der Serverseite aktiviert ist.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist die Zeit, die eine Verbindung inaktiv bleiben muss, bevor
          TCP Keepalive-Prüfungen sendet. Standardmäßig wird sie in Sekunden
          angegeben. Jede andere Einheit ist möglich, wenn sie wie am Anfang
          dieses Dokuments erläutert an die Zahl angehängt wird.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPIDLE. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_time) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option srvtcpka", "srvtcpka-cnt", "srvtcpka-intvl".

<a id="entry-4-2-srvtcpka-intvl"></a>

**`srvtcpka-intvl <timeout>`**

```haproxy
srvtcpka-intvl <timeout>
```

Den zeitlichen Abstand zwischen einzelnen Keepalive-Prüfungen auf der Serverseite festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist die Zeit zwischen einzelnen Keepalive-Prüfungen.
          Standardmäßig wird sie in Sekunden angegeben. Jede andere Einheit
          ist möglich, wenn sie wie am Anfang dieses Dokuments erläutert
          an die Zahl angehängt wird.
```

Dieses Schlüsselwort entspricht der Socket-Option TCP_KEEPINTVL. Wird es nicht angegeben, wird der systemweite TCP-Parameter (tcp_keepalive_intvl) verwendet. Die Verfügbarkeit dieser Einstellung hängt vom Betriebssystem ab. Unter Linux funktioniert sie bekanntermaßen.

Siehe auch: "option srvtcpka", "srvtcpka-cnt", "srvtcpka-idle".

<a id="entry-4-2-stats-admin"></a>

**`stats admin { if | unless } <cond>`**

```haproxy
stats admin { if | unless } <cond>
```

Die Administration über die Statistikseite aktivieren, wenn eine Bedingung erfüllt beziehungsweise nicht erfüllt ist

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Diese Anweisung aktiviert die Administrationsstufe der Statistikseite, wenn eine Bedingung bei if erfüllt beziehungsweise bei unless nicht erfüllt ist.

Die Administrationsstufe erlaubt das Aktivieren und Deaktivieren von Servern über die Weboberfläche. Aus Sicherheitsgründen ist die Statistikseite standardmäßig schreibgeschützt. Sind im Abschnitt "stats scope"-Direktiven gesetzt, akzeptieren nur die dadurch bezeichneten Proxys Zustandsänderungen; der Zugriff auf die anderen wird verweigert.

Derzeit ist die POST-Anfrage auf die Puffergröße abzüglich des reservierten Pufferbereichs begrenzt. Ist die Serverliste zu lang, wird die Anfrage daher nicht verarbeitet. Es wird empfohlen, jeweils nur wenige Server zu ändern.

Diese administrativen POST-Anfragen sind für CSRF-Angriffe anfällig. Als teilweise Gegenmaßnahme wird geprüft, ob Origin beziehungsweise bei fehlendem Origin der Referer mit dem Host-Header übereinstimmt. Dies reicht jedoch nicht aus, um solche Angriffe vollständig zu verhindern. Ein vollständiger Schutz ist nicht möglich. Es wird empfohlen, diese Funktion nicht über eine öffentliche Schnittstelle zugänglich zu machen und den zugriffsberechtigten Personenkreis einzuschränken.

Beispiel:

```shell
# statistics admin level only for localhost
backend stats_localhost
    stats enable
    stats admin if LOCALHOST
```

Beispiel:

```shell
# statistics admin level always enabled because of the authentication
backend stats_auth
    stats enable
    stats auth  admin:AdMiN123
    stats admin if TRUE
```

Beispiel:

```shell
# statistics admin level depends on the authenticated user
userlist stats-auth
    group admin    users admin
    user  admin    insecure-password 'AdMiN123'
    group readonly users haproxy
    user  haproxy  insecure-password 'haproxy'

backend stats_auth
    stats enable
    acl AUTH       http_auth(stats-auth)
    acl AUTH_ADMIN http_auth_group(stats-auth) admin
    stats http-request auth unless AUTH
    stats admin if AUTH_ADMIN
```

Siehe auch: "stats enable", "stats auth", "stats http-request", "stats scope", [Abschnitt 12.2](/de/haproxy/other-sections/#section-12-2) zu Benutzerlisten und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-ssl-f-use"></a>

**`ssl-f-use [<sslbindconf> ...]*`**

```haproxy
ssl-f-use [<sslbindconf> ...]*
```

Dem aktuellen Frontend ein Zertifikat zuweisen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

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
- ktls
- no-alpn
- no-ca-names
- npn
- sigalgs
- ssl-min-ver
- ssl-max-ver
- verify

sslbindconf unterstützt außerdem die folgenden Schlüsselwörter von crt-store
load (siehe Abschnitt 12.7.1. Ladeoptionen):

- crt
- key
- ocsp
- issuer
- sctl
- ocsp-update
```

Ein Zertifikat `<crtname>` einer crt-list zuweisen, die automatisch aus dem Frontendnamen mit vorangestelltem @ erstellt wird, etwa '@frontend1'.

Diese implizite crt-list wird jeder "ssl"-bind-Zeile im aktuellen Frontend zugewiesen.

Die crt-list-Befehle über das Statistik-Socket wirken auf diese Liste. Zertifikate und SSL-Optionen können darin also ersetzt, entfernt oder hinzugefügt werden.

Beispiel:

```text
frontend https
    bind :443 ssl
    bind quic4@:443 ssl
    ssl-f-use crt foobar.pem.rsa sigalgs "RSA-PSS+SHA256"
    ssl-f-use crt test.foobar.pem
    ssl-f-use crt test2.foobar.crt key test2.foobar.key ocsp test2.foobar.ocsp ocsp-update on
```

Siehe auch: "crt-list" und "crt".

<a id="entry-4-2-stats-auth"></a>

**`stats auth <user>:<passwd>`**

```haproxy
stats auth <user>:<passwd>
```

Statistiken mit Authentifizierung aktivieren und einem Konto Zugriff gewähren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<user>    ist ein Benutzername, dem Zugriff gewährt wird.

<passwd>  ist das Klartextpasswort dieses Benutzers.
```

Diese Anweisung aktiviert Statistiken mit den Standardeinstellungen und beschränkt den Zugriff auf deklarierte Benutzer. Sie kann beliebig oft wiederholt werden, um beliebig vielen Benutzern Zugriff zu gewähren. Versucht ein Benutzer ohne gültiges Konto auf die Statistiken zuzugreifen, wird die Antwort "401 Forbidden" zurückgegeben, damit der Browser nach einem gültigen Benutzernamen und Passwort fragt. Der an den Browser zurückgegebene Realm kann mit "stats realm" konfiguriert werden.

Da HTTP-Basisauthentifizierung verwendet wird, werden die Passwörter im Klartext über das Netz übertragen. Daher wurde entschieden, auch in der Konfigurationsdatei Klartextpasswörter zu verwenden. Dies soll Benutzer daran erinnern, dass diese Passwörter nicht sensibel sein und nicht für andere Konten wiederverwendet werden sollten.

Mit "stats
scope" lässt sich außerdem die Auswahl der im Bericht angezeigten Proxys einschränken.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats enable", "stats realm", "stats scope", "stats uri"

<a id="entry-4-2-stats-enable"></a>

**`stats enable`**

```haproxy
stats enable
```

Die Statistikdarstellung mit Standardeinstellungen aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Diese Anweisung aktiviert die Statistikdarstellung mit den beim Kompilieren festgelegten Standardeinstellungen. Sofern nicht anders angegeben, gelten folgende Einstellungen: - stats uri : /haproxy?stats - stats realm: "HAProxy
Statistics" - stats auth : keine Authentifizierung - stats scope: keine Einschränkung

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats realm", "stats uri"

<a id="entry-4-2-stats-hide-version"></a>

**`stats hide-version`**

```haproxy
stats hide-version
```

Statistiken aktivieren und die Anzeige der HAProxy-Version ausblenden

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Die Statistikseite kann neben den Statistiken nützliche Statusinformationen anzeigen, darunter die HAProxy-Version. Die genaue Version jedem zugänglich zu machen, gilt jedoch im Allgemeinen als gefährlich, da dies gezielte Angriffe auf bekannte Schwachstellen erleichtern kann. Die Anweisung "stats hide-version" entfernt die Versionsangabe aus dem Statistikbericht. Dies wird für öffentliche Websites und für Websites mit schwachen Zugangsdaten empfohlen und ist das Standardverhalten.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats enable", "stats realm", "stats uri", "stats show-version"

<a id="entry-4-2-stats-http-request"></a>

**`stats http-request { allow | deny | auth [realm <realm>] }`**

```haproxy
stats http-request { allow | deny | auth [realm <realm>] }
             [ { if | unless } <condition> ]
```

Zugriffskontrolle für Statistiken

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Wie "http-request" erlaubt diese Gruppe von Optionen eine genaue Steuerung des Zugriffs auf die Statistiken. Auf jede Option können if/unless und eine ACL folgen. Die erste Option mit erfüllter Bedingung oder ohne Bedingung entscheidet abschließend. Bei "deny" wird ein Fehler 403 zurückgegeben, bei "allow" erfolgt die normale Verarbeitung, und bei "auth" wird der Fehlercode 401/407 zurückgegeben, sodass der Client zur Eingabe von Benutzername und Passwort aufgefordert werden sollte.

Die Anzahl der http-request-Anweisungen pro Instanz ist nicht fest begrenzt.

Siehe auch: "http-request", [Abschnitt 12.2](/de/haproxy/other-sections/#section-12-2) zu Benutzerlisten und [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

<a id="entry-4-2-stats-realm"></a>

**`stats realm <realm>`**

```haproxy
stats realm <realm>
```

Statistiken aktivieren und den Authentifizierungs-Realm festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<realm>   ist der Name des Bereichs für HTTP-Basisauthentifizierung, der
          dem Browser mitgeteilt wird. Der Browser zeigt ihn im Dialog an,
          der zur Eingabe eines gültigen Benutzernamens und Passworts auffordert.
```

Der Realm wird als einzelnes Wort eingelesen. Enthaltene Leerzeichen sollten daher mit einem Backslash ('&#92;') maskiert werden.

Diese Anweisung ist nur zusammen mit "stats auth" nützlich, da sie ausschließlich die Authentifizierung betrifft.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats enable", "stats uri"

<a id="entry-4-2-stats-refresh"></a>

**`stats refresh <delay>`**

```haproxy
stats refresh <delay>
```

Statistiken mit automatischer Aktualisierung aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<delay>   ist die empfohlene Aktualisierungszeit in Sekunden, die dem Browser
          beim Abrufen der Berichtsseite zurückgegeben wird. Der Browser kann
          zwar eine beliebige Zeit wählen, hält sich aber meist an die Angabe
          und aktualisiert die Seite in diesem Sekundenabstand. Das Intervall
          kann auch in jeder anderen Zeiteinheit angegeben werden, indem die
          Einheit wie am Anfang dieses Dokuments erläutert an den Wert
          angehängt wird.
```

Diese Anweisung ist für Überwachungsanzeigen nützlich, die dauerhaft eine Seite mit der Aktivität des Load-Balancers anzeigen. Ist sie gesetzt, enthält der HTML-Bericht einen Link "refresh"/"stop refresh", über den der Benutzer die automatische Aktualisierung der Seite ein- oder ausschalten kann.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats enable", "stats realm", "stats uri"

<a id="entry-4-2-stats-scope"></a>

**`stats scope { <name> | "." }`**

```haproxy
stats scope { <name> | "." }
```

Statistiken aktivieren und den Zugriffsbereich begrenzen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<name>    ist der Name eines anzuzeigenden listen-, frontend- oder
          backend-Abschnitts. Der besondere Name "." (ein einzelner Punkt)
          bezeichnet den Abschnitt, in dem die Anweisung steht.
```

Ist diese Anweisung angegeben, erscheinen nur die mit ihr aufgeführten Abschnitte im Bericht. Alle anderen werden ausgeblendet, und Versuche, ihren Zustand im Administrationsmodus zu ändern, werden abgewiesen. Die Anweisung kann beliebig oft angegeben werden, wenn mehrere Abschnitte angezeigt werden sollen. Die Namen werden lediglich durch einfache Zeichenkettenvergleiche geprüft. Ob ein angegebener Abschnitt tatsächlich existiert, wird niemals geprüft.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats enable", "stats realm", "stats uri" und "stats admin"

<a id="entry-4-2-stats-show-desc"></a>

**`stats show-desc [ <desc> ]`**

```haproxy
stats show-desc [ <desc> ]
```

Die Anzeige einer Beschreibung auf der Statistikseite aktivieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

    `<desc>`    ist eine optionale anzuzeigende Beschreibung. Fehlt sie, wird
              automatisch die Beschreibung aus dem global-Abschnitt verwendet.

Diese Anweisung ist für Benutzer nützlich, die ihren Kunden gemeinsam genutzte Dienste anbieten, bei denen Knotenname oder Beschreibung für jeden Kunden unterschiedlich sein sollten.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen. Standardmäßig wird keine Beschreibung angezeigt.

Beispiel:

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-desc Master node for Europe, Asia, Africa
    stats uri       /admin?stats
    stats refresh   5s
```

Siehe auch: "show-node", "stats enable", "stats uri" und "description" im global-Abschnitt.

<a id="entry-4-2-stats-show-legends"></a>

**`stats show-legends`**

```haproxy
stats show-legends
```

Die Anzeige zusätzlicher Informationen auf der Statistikseite aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Die Anzeige zusätzlicher Informationen auf der Statistikseite aktivieren: - cap: Fähigkeiten (Proxy) - mode: einer der Werte tcp, http oder health (Proxy) - id: SNMP ID (Proxy, Socket, Server) - IP (Socket, Server) - cookie (Backend, Server)

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen. Standardmäßig werden diese Informationen nicht angezeigt.

Siehe auch: "stats enable", "stats uri".

<a id="entry-4-2-stats-show-modules"></a>

**`stats show-modules`**

```haproxy
stats show-modules
```

Die Anzeige zusätzlicher Statistikmodule auf der Statistikseite aktivieren

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Am Ende der Zeile werden neue Spalten hinzugefügt, deren Tooltips die zusätzlichen Statistikwerte enthalten.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen. Standardverhalten ist, diese Informationen nicht anzuzeigen.

Siehe auch: "stats enable", "stats uri".

<a id="entry-4-2-stats-show-node"></a>

**`stats show-node [ <name> ]`**

```haproxy
stats show-node [ <name> ]
```

Die Anzeige eines Hostnamens auf der Statistikseite aktivieren.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<name>    ist ein optionaler anzuzeigender Name. Ohne Angabe wird automatisch
          der Knotenname aus dem global-Abschnitt verwendet.
```

Diese Anweisung ist für Benutzer nützlich, die ihren Kunden gemeinsam genutzte Dienste anbieten, bei denen der Knoten oder die Beschreibung auf einer Statistikseite für jeden Kunden unterschiedlich sein kann. Standardverhalten ist, den Hostnamen nicht anzuzeigen.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-node Europe-1
    stats uri       /admin?stats
    stats refresh   5s
```

Siehe auch: "show-desc", "stats enable", "stats uri" und "node" im globalen Abschnitt.

<a id="entry-4-2-stats-show-version"></a>

**`stats show-version`**

```haproxy
stats show-version
```

Statistiken aktivieren und die HAProxy-Version anzeigen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente: keine

Die Statistikseite kann zusätzliche nützliche Statusinformationen zusammen mit den Statistiken anzeigen. Dazu gehört die HAProxy-Version. Es wird jedoch allgemein als gefährlich angesehen, die genaue Version an Dritte zu melden, da dies Angreifern helfen kann, gezielte Angriffe auf bekannte Schwachstellen durchzuführen. Daher ist dies standardmäßig deaktiviert. Die Angabe "stats show-version" ermöglicht die Anzeige dieser Informationen. Dies wird für öffentliche Websites oder Websites mit schwachen Anmeldeinformationen nicht empfohlen.

Siehe auch: "stats auth", "stats enable", "stats realm", "stats uri", "stats hide-version"

<a id="entry-4-2-stats-uri"></a>

**`stats uri <prefix>`**

```haproxy
stats uri <prefix>
```

Statistiken aktivieren und das URI-Präfix für den Zugriff darauf festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<prefix>  ist das Präfix jeder URI, die an stats umgeleitet wird.
          Es kann ein Fragezeichen ('?') enthalten, um einen Teil einer
          Abfragezeichenfolge anzugeben.
```

Die Statistik-URI wird im weitergeleiteten Datenverkehr abgefangen, sodass die Statistikseite als Seite innerhalb der normalen Anwendung erscheint. Es wird dringend empfohlen sicherzustellen, dass die gewählte URI niemals in der Anwendung vorkommt. Andernfalls wäre die Anwendungsressource unter dieser URI nicht mehr erreichbar.

Die standardmäßig in HAProxy eingebaute URI ist "/haproxy?stats", diese kann jedoch beim Kompilieren geändert werden. Daher ist es besser, sie hier stets explizit anzugeben. Es ist allgemein eine gute Idee, ein Fragezeichen in der URI zu verwenden, damit zwischengeschaltete Proxys das Ergebnis nicht zwischenspeichern. Außerdem wird jede Zeichenkette, die mit dem Präfix beginnt, als Statistikanfrage akzeptiert, sodass das Fragezeichen dabei hilft sicherzustellen, dass keine gültige URI mit denselben Wörtern beginnt.

Es ist manchmal sehr praktisch, "/" als URI-Präfix zu verwenden und diese Anweisung in einer eigenen "listen"-Instanz zu platzieren. Dadurch wird es einfach, eine Adresse oder einen Port ausschließlich für Statistiken zu reservieren.

Obwohl diese Anweisung allein ausreicht, um die Statistikdarstellung zu aktivieren, wird empfohlen, alle weiteren Einstellungen ausdrücklich festzulegen, statt sich auf wenig offensichtliche Standardparameter zu verlassen.

Beispiel:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Siehe auch: "stats auth", "stats enable", "stats realm"

<a id="entry-4-2-stick-match"></a>

**`stick match <pattern> [table <table>] [{if | unless} <cond>]`**

```haproxy
stick match <pattern> [table <table>] [{if | unless} <cond>]
```

Eine Bedingung zum Abgleich eines Anfragemusters definieren, um einen Benutzer an einen Server zu binden

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<pattern>  ist eine Sample-Ausdrucksregel wie in Abschnitt 7.3 beschrieben.
           Sie legt fest, welche Elemente der eingehenden Anfrage oder
           Verbindung analysiert werden, um einen passenden Eintrag in einer
           Stick Table zu finden. Diese Regel ist zwingend erforderlich.

<table>    ist ein optionaler Name einer Stick Table. Ohne Angabe wird die
           Tabelle desselben Backends verwendet. Eine Stick Table wird mit
           der Anweisung "stick-table" deklariert.

<cond>     ist eine optionale Vergleichsbedingung. Damit kann ein bestimmtes
           Kriterium nur dann verglichen werden, wenn andere Bedingungen
           erfüllt oder nicht erfüllt sind. Beispielsweise kann die
           Quell-IP-Adresse verwendet werden, außer wenn eine Anfrage über
           einen bekannten Proxy kommt; dann würde ein Header verglichen,
           der diese IP-Adresse enthält.
```

Manche Protokolle oder Anwendungen erfordern komplexe Regeln zur Sitzungsbindung und können sich nicht immer allein auf Cookies oder Hashing verlassen. Die Anweisung "stick match" beschreibt eine Regel, um das Kriterium für die Sitzungsbindung aus einer eingehenden Anfrage oder Verbindung zu extrahieren. Eine vollständige Liste der möglichen Muster und Umwandlungsregeln enthält [Abschnitt 7](/de/haproxy/acls-and-samples/).

Die Tabelle muss mit der Anweisung "stick-table" deklariert werden. Ihr Typ muss mit dem Muster kompatibel sein. Standardmäßig wird die Tabelle im selben Backend verwendet. Eine Tabelle kann mit anderen Backends gemeinsam genutzt werden, indem sie über das Schlüsselwort "table" referenziert wird. Bei Verweis auf eine andere Tabelle werden die Server-IDs innerhalb der Backends verwendet. Standardmäßig beginnen die Server-IDs in jedem Backend bei 1, sodass die Reihenfolge der Server ausreicht. Im Zweifelsfall wird jedoch dringend empfohlen, die Server-IDs über deren Einstellung "id" ausdrücklich festzulegen.

Mit "if" oder "unless" und einer nachfolgenden Bedingung lässt sich einschränken, wann eine Anweisung "stick match" angewendet wird. ACL-basierte Bedingungen werden in [Abschnitt 7](/de/haproxy/acls-and-samples/) beschrieben.

Die Anzahl der "stick match"-Anweisungen ist nicht begrenzt. Die erste anwendbare Regel mit einem Treffer leitet die Anfrage an denselben Server, der die Anfrage bearbeitet hat, durch die der Eintrag angelegt wurde. So lassen sich mehrere Abgleiche als Rückfallmöglichkeiten verwenden.

Die stick-Regeln werden nach den Cookies zur Sitzungsbindung geprüft. Hat bereits ein Cookie den Server ausgewählt, beeinflussen sie die Sitzungsbindung daher nicht. Damit lassen sich sehr einfach Cookies einfügen und IP-Adressen abgleichen, um die Sitzungsbindung zwischen HTTP und HTTPS aufrechtzuerhalten.

Beispiel:

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

Siehe auch: "stick-table", "stick on", [Abschnitt 11](/de/haproxy/stick-tables-and-peers/) über Stick Tables und [Abschnitt 7](/de/haproxy/acls-and-samples/) über ACLs und Sample-Abruf.

<a id="entry-4-2-stick-on"></a>

**`stick on <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick on <pattern> [table <table>] [{if | unless} <condition>]
```

Ein Anfragemuster definieren, um einen Benutzer einem Server zuzuordnen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Hinweis: Diese Form ist genau äquivalent zu "stick match" gefolgt von "stick store-request", alle mit denselben Argumenten. Einzelheiten finden Sie bei beiden Schlüsselwörtern. Sie dient lediglich dazu, leichter wartbare Konfigurationen zu schreiben.

Beispiele:

```shell
# The following form ...
stick on src table pop if !localhost

# ...is strictly equivalent to this one:
stick match src table pop if !localhost
stick store-request src table pop if !localhost


# Use cookie persistence for HTTP, and stick on source address for HTTPS as
# well as HTTP without cookie. Share the same table between both accesses.
backend http
    mode http
    balance roundrobin
    stick on src table https
    cookie SRV insert indirect nocache
    server s1 192.168.1.1:80 cookie s1
    server s2 192.168.1.1:80 cookie s2

backend https
    mode tcp
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

Siehe auch: "stick match", "stick store-request" und [Abschnitt 11](/de/haproxy/stick-tables-and-peers/) über Stick Tables.

<a id="entry-4-2-stick-store-request"></a>

**`stick store-request <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-request <pattern> [table <table>] [{if | unless} <condition>]
```

Ein Anfragemuster definieren, mit dem ein Eintrag in einer Tabelle zur Sitzungsbindung angelegt wird

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<pattern>  ist eine Sample-Ausdrucksregel wie in Abschnitt 7.3 beschrieben.
           Sie legt fest, welche Elemente der eingehenden Anfrage oder
           Verbindung analysiert, extrahiert und in der Tabelle gespeichert
           werden, sobald ein Server ausgewählt ist.

<table>    ist ein optionaler Name einer Stick Table. Ohne Angabe wird die
           Tabelle desselben Backends verwendet. Eine Stick Table wird mit
           der Anweisung "stick-table" deklariert.

<cond>     ist eine optionale Speicherbedingung. Damit können bestimmte
           Kriterien nur gespeichert werden, wenn gewisse Bedingungen erfüllt
           oder nicht erfüllt sind. Beispielsweise kann die Quell-IP-Adresse
           gespeichert werden, außer wenn die Anfrage über einen bekannten
           Proxy kommt; dann würde die konvertierte Form eines Headers
           gespeichert, der diese IP-Adresse enthält.
```

Manche Protokolle oder Anwendungen erfordern komplexe Regeln zur Sitzungsbindung und können sich nicht immer allein auf Cookies oder Hashing verlassen. Die Anweisung "stick store-request" beschreibt eine Regel, die festlegt, was wann aus der Anfrage extrahiert werden soll. Das Ergebnis wird in einer Tabelle zur Sitzungsbindung gespeichert, damit spätere Anfragen es mit "stick match" abgleichen können. Der extrahierte Teil muss natürlich sinnvoll sein und bei einer späteren Anfrage wiedergefunden werden können. Häufig ist es beispielsweise sinnvoll, die IP-Adresse eines Clients zu speichern. Auch eine ID aus einem URL-Parameter ist sinnvoll. Einen Quellport zu speichern, ist dagegen fast nie sinnvoll, weil er nur zufällig wiedergefunden würde. Eine vollständige Liste der möglichen Muster und Umwandlungsregeln enthält [Abschnitt 7](/de/haproxy/acls-and-samples/).

Die Tabelle muss mit der Anweisung "stick-table" deklariert werden. Ihr Typ muss mit dem Muster kompatibel sein. Standardmäßig wird die Tabelle im selben Backend verwendet. Eine Tabelle kann mit anderen Backends gemeinsam genutzt werden, indem sie über das Schlüsselwort "table" referenziert wird. Bei Verweis auf eine andere Tabelle werden die Server-IDs innerhalb der Backends verwendet. Standardmäßig beginnen die Server-IDs in jedem Backend bei 1, sodass die Reihenfolge der Server ausreicht. Im Zweifelsfall wird jedoch dringend empfohlen, die Server-IDs über deren Einstellung "id" ausdrücklich festzulegen.

Mit "if" oder "unless" und einer nachfolgenden Bedingung lässt sich einschränken, wann eine Anweisung "stick store-request" angewendet wird. Die Bedingung wird beim Parsen der Anfrage ausgewertet, sodass beliebige Kriterien verwendet werden können. ACL-basierte Bedingungen werden in [Abschnitt 7](/de/haproxy/acls-and-samples/) beschrieben.

Die Anzahl der "stick store-request"-Anweisungen ist nicht begrenzt. Pro Anfrage oder Antwort sind jedoch höchstens 8 gleichzeitige Speichervorgänge möglich. Unabhängig von der Anzahl der Regeln können dadurch bis zu 8 Kriterien gespeichert werden, die aus der Anfrage oder der Antwort extrahiert wurden. Nur die ersten 8 passenden Kriterien werden behalten. So können mehrere Tabellen gleichzeitig befüllt werden, um die Chance zu erhöhen, einen Benutzer bei einem anderen Protokoll oder Zugriffsverfahren wiederzuerkennen. Mehrere store-request-Regeln dürfen dieselbe Tabelle verwenden. Werden die Regeln in absteigender Präferenzreihenfolge angeordnet, lässt sich so das geeignetste Kriterium auswählen. Für eine bestimmte Tabelle wird nur das erste extrahierte Kriterium gespeichert. Alle nachfolgenden store-request-Regeln für dieselbe Tabelle werden übersprungen, ohne ihre ACLs auszuwerten.

Die "store-request"-Regeln werden ausgewertet, sobald die Verbindung zum Server aufgebaut ist. Dadurch enthält die Tabelle den tatsächlichen Server, der die Anfrage verarbeitet hat.

Beispiel:

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

Siehe auch: "stick-table", "stick on", [Abschnitt 11](/de/haproxy/stick-tables-and-peers/) zu Stick Tables und [Abschnitt 7](/de/haproxy/acls-and-samples/) zu ACLs und Sample-Abrufen.

<a id="entry-4-2-stick-store-response"></a>

**`stick store-response <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-response <pattern> [table <table>] [{if | unless} <condition>]
```

Ein Antwortmuster definieren, mit dem ein Eintrag in einer Tabelle zur Sitzungsbindung angelegt wird

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<pattern>  ist eine Sample-Ausdrucksregel wie in Abschnitt 7.3 beschrieben.
           Sie legt fest, welche Elemente der Antwort oder Verbindung
           analysiert, extrahiert und in der Tabelle gespeichert werden,
           sobald ein Server ausgewählt ist.

<table>    ist ein optionaler Name einer Stick Table. Ohne Angabe wird die
           Tabelle desselben Backends verwendet. Eine Stick Table wird mit
           der Anweisung "stick-table" deklariert.

<cond>     ist eine optionale Speicherbedingung. Damit können bestimmte
           Kriterien nur gespeichert werden, wenn gewisse Bedingungen erfüllt
           oder nicht erfüllt sind. Beispielsweise kann die SSL-Sitzungs-ID
           nur dann gespeichert werden, wenn die Antwort ein SSL-Server-Hello ist.
```

Manche Protokolle oder Anwendungen erfordern komplexe Regeln zur Sitzungsbindung und können sich nicht immer allein auf Cookies oder Hashing verlassen. Die Anweisung "stick store-response" beschreibt eine Regel, die festlegt, was wann aus der Antwort extrahiert werden soll. Das Ergebnis wird in einer Tabelle zur Sitzungsbindung gespeichert, damit spätere Anfragen es mit "stick match" abgleichen können. Der extrahierte Teil muss natürlich sinnvoll sein und bei einer späteren Anfrage wiedergefunden werden können. Eine ID aus einem Antwortheader zu speichern, ist beispielsweise sinnvoll. Eine vollständige Liste der möglichen Muster und Umwandlungsregeln enthält [Abschnitt 7](/de/haproxy/acls-and-samples/).

Die Tabelle muss mit der Anweisung "stick-table" deklariert werden. Ihr Typ muss mit dem Muster kompatibel sein. Standardmäßig wird die Tabelle im selben Backend verwendet. Eine Tabelle kann mit anderen Backends gemeinsam genutzt werden, indem sie über das Schlüsselwort "table" referenziert wird. Bei Verweis auf eine andere Tabelle werden die Server-IDs innerhalb der Backends verwendet. Standardmäßig beginnen die Server-IDs in jedem Backend bei 1, sodass die Reihenfolge der Server ausreicht. Im Zweifelsfall wird jedoch dringend empfohlen, die Server-IDs über deren Einstellung "id" ausdrücklich festzulegen.

Mit "if" oder "unless" und einer nachfolgenden Bedingung lässt sich einschränken, wann eine Anweisung "stick store-response" angewendet wird. Die Bedingung wird beim Parsen der Antwort ausgewertet, sodass beliebige Kriterien verwendet werden können. ACL-basierte Bedingungen werden in [Abschnitt 7](/de/haproxy/acls-and-samples/) beschrieben.

Die Anzahl der "stick store-response"-Anweisungen ist nicht begrenzt. Pro Anfrage oder Antwort sind jedoch höchstens 8 gleichzeitige Speichervorgänge möglich. Unabhängig von der Anzahl der Regeln können dadurch bis zu 8 Kriterien gespeichert werden, die aus der Anfrage oder der Antwort extrahiert wurden. Nur die ersten 8 passenden Kriterien werden behalten. So können mehrere Tabellen gleichzeitig befüllt werden, um die Chance zu erhöhen, einen Benutzer bei einem anderen Protokoll oder Zugriffsverfahren wiederzuerkennen. Mehrere store-response-Regeln dürfen dieselbe Tabelle verwenden. Werden die Regeln in absteigender Präferenzreihenfolge angeordnet, lässt sich so das geeignetste Kriterium auswählen. Für eine bestimmte Tabelle wird nur das erste extrahierte Kriterium gespeichert. Alle nachfolgenden store-response-Regeln für dieselbe Tabelle werden übersprungen, ohne ihre ACLs auszuwerten. Eine store-response-Regel darf jedoch dieselbe Tabelle verwenden, auf die bereits eine store-request-Regel verweist. Jede Tabelle kann somit gleichzeitig genau ein Element aus der Anfrage und ein Element aus der Antwort lernen.

Die Tabelle enthält den tatsächlichen Server, der die Anfrage verarbeitet hat.

Beispiel:

```shell
# Learn SSL session ID from both request and response and create affinity.
backend https
    mode tcp
    balance roundrobin
    # maximum SSL session ID length is 32 bytes.
    stick-table type binary len 32 size 30k expire 30m

    acl clienthello req.ssl_hello_type 1
    acl serverhello res.ssl_hello_type 2

    # use tcp content accepts to detects ssl client and server hello.
    tcp-request inspect-delay 5s
    tcp-request content accept if clienthello

    # no timeout on response inspect delay by default.
    tcp-response content accept if serverhello

    # SSL session ID (SSLID) may be present on a client or server hello.
    # Its length is coded on 1 byte at offset 43 and its value starts
    # at offset 44.

    # Match and learn on request if client hello.
    stick on req.payload_lv(43,1) if clienthello

    # Learn on response if server hello.
    stick store-response resp.payload_lv(43,1) if serverhello

    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

Siehe auch: "stick-table", "stick on", [Abschnitt 11](/de/haproxy/stick-tables-and-peers/) zu Stick Tables und [Abschnitt 7](/de/haproxy/acls-and-samples/) zu ACLs und Musterextraktion.

<a id="entry-4-2-stick-table-type"></a>

**`stick-table type <type> size <size> [expire <expire>] [args...]`**

```haproxy
stick-table type <type> size <size> [expire <expire>] [args...]
```

Die Tabelle zur Sitzungsbindung für den aktuellen Abschnitt konfigurieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| ja

Damit wird eine stick-table deklariert und konfiguriert. Vollständige Einzelheiten und die Liste unterstützter Argumente finden Sie in [Abschnitt 11.1](/de/haproxy/stick-tables-and-peers/#section-11-1). Nur Typ und Größe sind zwingend erforderlich.

<a id="entry-4-2-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
```

Einen Kommentar für die nachfolgende tcp-check-Regel definieren, der bei ihrem Fehlschlagen im Protokoll ausgegeben wird.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<string>  ist die Kommentarmeldung, die dem Protokoll hinzugefügt wird,
          wenn die nachfolgende tcp-check-Regel fehlschlägt.
```

Dies funktioniert nur für die Regeln connect, send und expect. Es dient einer verständlichen Fehlermeldung.

Siehe auch: "option tcp-check", "tcp-check connect", "tcp-check send" und "tcp-check expect".

<a id="entry-4-2-tcp-check-connect"></a>

**`tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]`**

```haproxy
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
```

Eine neue Verbindung öffnen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

default      Die Standardoptionen der server-Zeile für Health Checks verwenden.
             Die Serveroptionen werden nur verwendet, wenn sie nicht neu
             definiert wurden.

port <expr>  Ohne Angabe wird der Prüfport oder der Serverport verwendet.
             Gibt HAProxy das Ziel für den Verbindungsaufbau an.
             <port> muss eine gültige ganze TCP-Portnummer von 1 bis 65535
             oder ein Sample-Abruf-Ausdruck sein.

addr <ip>    legt die IP-Adresse für den Health Check fest.

send-proxy   sendet eine Zeichenfolge des PROXY-Protokolls.

via-socks4   aktiviert ausgehende Health Checks über einen vorgeschalteten
             socks4-Proxy.

ssl          öffnet eine verschlüsselte Verbindung.

sni <sni>    gibt die SNI für Health Checks über SSL an.

alpn <alpn>  legt fest, welche Protokolle über ALPN angekündigt werden.
             Die Protokollliste enthält durch Kommas getrennte Protokollnamen,
             etwa "http/1.1,http/1.0" (ohne Anführungszeichen).
             Ohne Angabe wird das ALPN des Servers verwendet.

proto <name> erzwingt das für diese Verbindung zu verwendende
             Multiplexer-Protokoll. Es muss ein TCP-Mux-Protokoll sein und
             auf der Backend-Seite verwendet werden können. Die verfügbaren
             Protokolle werden von haproxy -vv ausgegeben.

linger       schließt die Verbindung sauber, statt nur ein RST zu senden.
```

Verwendet eine Anwendung mehr als einen TCP-Port oder verteilt HAProxy in einem Backend die Last mehrerer Dienste, ist es sinnvoll, jeden Dienst einzeln zu prüfen, bevor ein Server als betriebsbereit gilt.

Wenn weder in der Serverzeile ein TCP-Port noch eine port-Direktive für den Server konfiguriert ist, muss 'tcp-check connect port `<port>`' der erste Schritt der Sequenz sein.

In einem tcp-check-Regelsatz ist ein 'connect' erforderlich; außerdem muss der Regelsatz mit einer 'connect'-Regel beginnen. Damit soll sichergestellt werden, dass Administratoren wissen, was sie tun.

Auch wenn der Regelsatz mit connect beginnen muss, dürfen diesem noch Regeln vom Typ set-var, unset-var oder comment vorausgehen.

Beispiele:

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option tcp-check
tcp-check connect
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
tcp-check connect port 443 ssl
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
server www 10.0.0.1 check port 80

# check both POP and IMAP from a single server:
option tcp-check
tcp-check connect port 110 linger
tcp-check expect string +OK\ POP3\ ready
tcp-check connect port 143
tcp-check expect string *\ OK\ IMAP4\ ready
server mail 10.0.0.1 check
```

Siehe auch: "option tcp-check", "tcp-check send", "tcp-check expect"

<a id="entry-4-2-tcp-check-expect"></a>

**`tcp-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
```

Die bei einem allgemeinen Health Check zu erfassenden und zu analysierenden Daten festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

min-recv  ist optional und kann die minimale Datenmenge festlegen, die für
          die Auswertung der aktuellen expect-Regel erforderlich ist. Liegt
          die Zahl empfangener Bytes darunter, wartet die Prüfung auf weitere
          Daten. Damit lassen sich mehrdeutige Vergleichsregeln auflösen oder
          aufwendige Regex-Vergleiche auf bekanntermaßen noch unvollständigen
          Inhalten vermeiden. Bei einer exakten Zeichenfolge (string oder binary) wird das Minimum
          aus Zeichenfolgenlänge und diesem Parameter verwendet. Der Wert -1
          bewirkt, dass der Parameter ignoriert wird. Trifft die expect-Regel
          nicht zu, wartet die Prüfung auf weitere Daten. Beim Wert 0 ist
          das Auswertungsergebnis immer endgültig.

ok-status <st>     ist optional und kann den Prüfstatus setzen, wenn die
                   expect-Regel erfolgreich ausgewertet wird und die letzte
                   Regel im tcp-check-Regelsatz ist. Unterstützt werden
                   "L7OK", "L7OKC", "L6OK" und "L4OK":
                     - L7OK : Prüfung auf Schicht 7 bestanden.
                     - L7OKC: Prüfung auf Schicht 7 bedingt bestanden;
                               Server in den Zustand NOLB setzen.
                     - L6OK : Prüfung auf Schicht 6 bestanden.
                     - L4OK : Prüfung auf Schicht 4 bestanden.
                   Standardmäßig wird "L7OK" verwendet.

error-status <st>  ist optional und kann den Prüfstatus setzen, wenn bei
                   der Auswertung der expect-Regel ein Fehler auftritt.
                   Unterstützt werden "L7OKC", "L7RSP", "L7STS", "L6RSP"
                   und "L4CON":
                     - L7OKC: Prüfung auf Schicht 7 bedingt bestanden;
                               Server in den Zustand NOLB setzen.
                     - L7RSP: ungültige Antwort auf Schicht 7; Protokollfehler.
                     - L7STS: Antwortfehler auf Schicht 7, etwa HTTP 5xx.
                     - L6RSP: ungültige Antwort auf Schicht 6; Protokollfehler.
                     - L4CON: Verbindungsproblem auf Schicht 1-4.
                   Standardmäßig wird "L7RSP" verwendet.

tout-status <st>   ist optional und kann den Prüfstatus setzen, wenn bei
                   der Auswertung der expect-Regel eine Zeitüberschreitung
                   auftritt. Unterstützt werden "L7TOUT", "L6TOUT" und
                   "L4TOUT":
                     - L7TOUT: Zeitüberschreitung auf Schicht 7 (HTTP/SMTP).
                     - L6TOUT: Zeitüberschreitung auf Schicht 6 (SSL).
                     - L4TOUT: Zeitüberschreitung auf Schicht 1-4.
                   Standardmäßig wird "L7TOUT" verwendet.

on-success <fmt>   ist optional und kann die protokollierte Informationsmeldung
                   anpassen, wenn die expect-Regel erfolgreich ausgewertet
                   wird und die letzte Regel im tcp-check-Regelsatz ist.
                   <fmt> ist ein benutzerdefiniertes
                   Protokollformat (siehe Abschnitt 8.2.6).

on-error <fmt>     ist optional und kann die protokollierte Informationsmeldung
                   anpassen, wenn bei der Auswertung der expect-Regel ein
                   Fehler auftritt. <fmt> ist ein
                   benutzerdefiniertes Protokollformat (siehe Abschnitt 8.2.6).

status-code <expr> ist optional und kann den bei Erfolg oder Fehler im
                   Protokoll ausgegebenen Prüfstatuscode setzen. <expr> ist
                   ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
                   gefolgt von Konvertern.

<match>   ist ein Schlüsselwort, das die Suche nach einem bestimmten Muster
          in der Antwort festlegt. Möglich sind "string", "rstring", "binary"
          und "rbinary".
          Dem Schlüsselwort kann ein Ausrufezeichen ("!") vorangestellt werden,
          um den Vergleich zu negieren. Zwischen Ausrufezeichen und
          Schlüsselwort sind Leerzeichen zulässig. Weitere Einzelheiten zu
          den unterstützten Schlüsselwörtern stehen unten.

<pattern> ist das gesuchte Muster. Es kann eine Zeichenfolge oder ein regulärer
          Ausdruck sein. Enthält das Muster Leerzeichen, müssen sie mit dem
          üblichen umgekehrten Schrägstrich ('\') maskiert werden.
          Bei einem binären Vergleich muss das Muster als Folge einer geraden
          Anzahl hexadezimaler Ziffern angegeben werden. Je zwei Ziffern
          stellen ein Byte dar. Die hexadezimalen Ziffern können groß- oder
          kleingeschrieben werden.
```

Die verfügbaren Abgleicharten sind bewusst ihren Entsprechungen bei http-check ähnlich:

```text
string <string>: prüft, ob die exakte Zeichenfolge im Antwortpuffer vorkommt.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Puffer
                  diese exakte Zeichenfolge enthält. Steht vor dem Schlüsselwort
                  "string" ein "!", gilt die Antwort als ungültig, wenn
                  ihr Körper diese Zeichenfolge enthält. Damit lässt sich
                  ein erforderliches Muster in einer Protokollantwort suchen
                  oder ein Fehler erkennen, wenn eine bestimmte Fehlermeldung
                  in einer Protokoll-Begrüßungsmeldung erscheint.

rstring <regex>: prüft den Antwortpuffer mit einem regulären Ausdruck.
                  Eine Health-Check-Antwort gilt als gültig, wenn ihr Puffer
                  diesem Ausdruck entspricht. Steht vor dem Schlüsselwort
                  "rstring" ein "!", gilt die Antwort als ungültig, wenn
                  ihr Körper dem Ausdruck entspricht.

string-lf <fmt>: prüft, ob eine Zeichenfolge im benutzerdefinierten Protokollformat
                  im Antwortpuffer vorkommt. Eine Health-Check-Antwort gilt
                  als gültig, wenn ihr Puffer die Zeichenfolge enthält,
                  die aus der Auswertung von <fmt> nach den in Abschnitt
                  8.2.6 beschriebenen Regeln für benutzerdefinierte
                  Protokollformate entsteht. Mit einem vorangestellten "!"
                  gilt die Antwort als ungültig, wenn ihr Puffer die
                  Zeichenfolge enthält.

binary <hexstring>: prüft, ob die exakte Zeichenfolge in ihrer hexadezimalen
                     Form im Antwortpuffer vorkommt. Eine Health-Check-Antwort
                     gilt als gültig, wenn ihr Puffer diese exakte
                     hexadezimale Zeichenfolge enthält. Dies dient zum
                     Vergleich von Daten in binären Protokollen.

rbinary <regex>: prüft den Antwortpuffer wie "rstring" mit einem regulären
                  Ausdruck. Der Antwortpuffer wird jedoch einschließlich
                  NUL-Bytes in seine hexadezimale Form umgewandelt. Damit
                  können alle Regex-Implementierungen beliebige binäre Inhalte
                  vergleichen. Die hexadezimale Darstellung benötigt doppelt
                  so viel Platz wie die ursprüngliche Antwort. Das gesuchte
                  Muster sollte daher mit höchstens der halben Größe des
                  Antwortpuffers auskommen.

binary-lf <hexfmt>: prüft, ob ein benutzerdefiniertes Protokollformat in
                     seiner hexadezimalen Form im Antwortpuffer vorkommt.
                     Eine Health-Check-Antwort gilt als gültig, wenn ihr
                     Puffer die hexadezimale Zeichenfolge enthält, die
                     aus der Auswertung von <fmt> nach den Regeln für
                     benutzerdefinierte Protokollformate entsteht (siehe
                     Abschnitt 8.2.6). Mit einem vorangestellten "!" gilt
                     die Antwort als ungültig, wenn ihr Puffer die
                     hexadezimale Zeichenfolge enthält. Vor dem Vergleich
                     mit dem Antwortpuffer wird die hexadezimale Zeichenfolge
                     in eine binäre Zeichenfolge umgewandelt.
```

Die Antworten werden auf eine bestimmte Größe begrenzt, die durch die globale Option "tune.bufsize" festgelegt ist und standardmäßig 16384 Bytes beträgt. Daher enthalten zu große Antworten bei Verwendung von "string", "rstring" oder binary möglicherweise nicht das erforderliche Muster. Ist eine große Antwort zwingend erforderlich, kann die standardmäßige Maximalgröße über die globale Variable geändert werden. Das Parsen sehr großer Antworten kann jedoch CPU-Zyklen verschwenden, insbesondere bei regulären Ausdrücken. Es ist daher stets besser, kleinere Ressourcen zu prüfen. Außerdem findet die Prüfung in ihrer derzeitigen Form nach einem Nullzeichen in der Antwort weder Zeichenketten noch Treffer für reguläre Ausdrücke. Ebenso kann kein Abgleich auf das Nullzeichen angefordert werden.

Beispiele:

```shell
# perform a POP check
option tcp-check
tcp-check expect string +OK\ POP3\ ready

# perform an IMAP check
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready

# look for the redis master server
option tcp-check
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check send QUIT\r\n
tcp-check expect string +OK

```

Siehe auch: "option tcp-check", "tcp-check connect", "tcp-check send", "tcp-check send-binary", "http-check expect", tune.bufsize

<a id="entry-4-2-tcp-check-send"></a>

**`tcp-check send <data> [comment <msg>]`**

```haproxy
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
```

Eine Zeichenkette oder ein benutzerdefiniertes Protokollformat festlegen, das bei einem allgemeinen Health Check als Anfrage gesendet wird

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

<data>         ist die Zeichenfolge, die während einer allgemeinen
               Health-Check-Sitzung gesendet wird.

<fmt>          ist das benutzerdefinierte Protokollformat, das nach seiner
               Auswertung während einer allgemeinen Health-Check-Sitzung
               gesendet wird (siehe Abschnitt 8.2.6).
```

Beispiele:

```shell
# look for the redis master server
option tcp-check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
```

Siehe auch: "option tcp-check", "tcp-check connect", "tcp-check expect", "tcp-check send-binary", tune.bufsize

<a id="entry-4-2-tcp-check-send-binary"></a>

**`tcp-check send-binary <hexstring> [comment <msg>]`**

```haproxy
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
```

Eine Zeichenkette aus Hexadezimalziffern oder ein benutzerdefiniertes Protokollformat mit Hexadezimalziffern festlegen, das bei einem rohen TCP-Health-Check als binäre Anfrage gesendet wird

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
comment <msg>  legt die zu meldende Nachricht fest, wenn die Regelauswertung
               fehlschlägt.

<hexstring>    ist die hexadezimale Zeichenfolge, die nach der Umwandlung in
               Binärdaten während einer allgemeinen Health-Check-Sitzung
               gesendet wird.

<hexfmt>       ist das hexadezimale benutzerdefinierte Protokollformat, das nach
               Auswertung und Umwandlung in Binärdaten während einer
               allgemeinen Health-Check-Sitzung gesendet wird
               (siehe Abschnitt 8.2.6).
```

Beispiele:

```shell
# redis check in binary
option tcp-check
tcp-check send-binary 50494e470d0a # PING\r\n
tcp-check expect binary 2b504F4e47 # +PONG

```

Siehe auch: "option tcp-check", "tcp-check connect", "tcp-check expect", "tcp-check send", tune.bufsize

<a id="entry-4-2-tcp-check-set-var"></a>

**`tcp-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Diese Operation legt den Inhalt einer Variablen fest. Die Variable wird inline deklariert.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<var-name>   Der Name der Variablen. Nur die Geltungsbereiche "proc", "sess"
             und "check" sind möglich. Einzelheiten zu Variablen stehen in
             Abschnitt 2.8.

 <cond>      Eine Menge von Bedingungen, die alle erfüllt sein müssen, damit
             die Variable tatsächlich gesetzt wird (etwa "ifnotempty", "ifgt"
             usw.). Die vollständige Liste möglicher Bedingungen steht in
             der Beschreibung des Konverters set-var.

 <expr>      Ein Sample-Abruf-Ausdruck, gegebenenfalls gefolgt von Konvertern.

 <fmt>       Der Wert nach den Regeln für benutzerdefinierte Protokollformate
             (siehe benutzerdefinierte Protokollformate in Abschnitt 8.2.6).
```

Beispiele:

```text
tcp-check set-var(check.port) int(1234)
tcp-check set-var-fmt(check.name) "%H"

```

<a id="entry-4-2-tcp-check-unset-var"></a>

**`tcp-check unset-var(<var-name>)`**

```haproxy
tcp-check unset-var(<var-name>)
```

Eine Referenz auf eine Variable innerhalb ihres Gültigkeitsbereichs freigeben.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<var-name>   Der Name der Variablen. Nur die Geltungsbereiche "proc", "sess"
             und "check" sind möglich. Einzelheiten zu Variablen stehen in
             Abschnitt 2.8.
```

Beispiele:

```text
tcp-check unset-var(check.port)

```

<a id="entry-4-2-tcp-request-connection"></a>

**`tcp-request connection <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
tcp-request connection <action> <options...> [ { if | unless } <condition> ]
```

Abhängig von einer Bedingung auf Schicht 4 eine Aktion auf einer eingehenden Verbindung ausführen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| nein

Argumente:

```text
<action>    legt die auszuführende Aktion fest, wenn die Bedingung zutrifft.
            Siehe unten.

<condition> ist eine gewöhnliche ACL-basierte Bedingung ausschließlich auf
            Schicht 4 (siehe Abschnitt 7).
```

Unmittelbar nach der Annahme einer neuen eingehenden Verbindung können Bedingungen ausgewertet werden, um zu entscheiden, ob die Verbindung akzeptiert oder verworfen werden muss oder ihre Zähler verfolgt werden sollen. Diese Bedingungen können keine Dateninhalte verwenden, da aus der Verbindung noch nichts gelesen wurde und noch keine Puffer reserviert sind. So lassen sich Verbindungen aus verschiedenen Quellen mit sehr geringem Aufwand gezielt und schnell akzeptieren oder verwerfen. Müssen für die Entscheidung Inhalte untersucht werden, sind stattdessen "tcp-request content"-Anweisungen zu verwenden.

Die Regeln "tcp-request connection" werden genau in der Reihenfolge ihrer Deklaration ausgewertet. Passt keine Regel oder gibt es keine Regel, wird die eingehende Verbindung standardmäßig akzeptiert. Die Anzahl der Regeln ist nicht gesondert begrenzt. Auf jede Regel kann optional eine ACL-basierte Bedingung folgen; dann wird die Regel nur ausgewertet, wenn diese Bedingung wahr ist.

Die Bedingung wird unmittelbar vor der Ausführung der Aktion ausgewertet, und die Aktion wird genau einmal ausgeführt. Daher ist es unproblematisch, wenn eine Aktion ein Element ändert, das in der Bedingung geprüft wird. Das bedeutet auch, dass mehrere Aktionen dieselbe Bedingung verwenden können: Die erste Aktion, die das Ergebnis der Bedingung ändert, reicht dann aus, um die übrigen Aktionen implizit zu deaktivieren. Dies wird beispielsweise verwendet, wenn einer leeren Variablen ein Wert aus verschiedenen Quellen zugewiesen werden soll.

Das erste Schlüsselwort nach "tcp-request connection" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "TCP RqCon").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Die Bedingung "if/unless" ist optional. Ohne Bedingung wird die Aktion uneingeschränkt ausgeführt. Dies kann für "track-sc\*"-Aktionen nützlich sein oder um die Standardaktion auf Ablehnen zu ändern.

Beispiel: Alle Verbindungen von Hosts auf einer Positivliste akzeptieren, zu schnell eintreffende Verbindungen ohne Zählung ablehnen und akzeptierte Verbindungen verfolgen. Dadurch wird die Verbindungsrate missbräuchlicher Quellen begrenzt.

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection reject if { src_conn_rate gt 10 }
        tcp-request connection track-sc0 src

Beispiel: Alle Verbindungen von Hosts auf der Positivliste annehmen, alle anderen Verbindungen zählen und zu schnell eintreffende ablehnen. Dadurch bleiben missbräuchliche Quellen blockiert, solange sie ihre Rate nicht verringern.

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection track-sc0 src
        tcp-request connection reject if { sc0_conn_rate gt 10 }

Beispiel: Das PROXY-Protokoll für Datenverkehr von allen bekannten Proxys aktivieren.

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }

Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

Siehe auch: "tcp-request session", "tcp-request content", "stick-table"

<a id="entry-4-2-tcp-request-content"></a>

**`tcp-request content <action> [{if | unless} <condition>]`**

```haproxy
tcp-request content <action> [{if | unless} <condition>]
```

Abhängig von einer Bedingung auf den Schichten 4-7 eine Aktion auf einer neuen Sitzung ausführen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Argumente:

```text
<action>    legt die auszuführende Aktion fest, wenn die Bedingung zutrifft.
            Siehe unten.

<condition> ist eine gewöhnliche ACL-basierte Bedingung auf den Schichten 4-7
            (siehe Abschnitt 7).
```

Der Inhalt einer Anfrage kann in einer frühen Phase der Anfrageverarbeitung untersucht werden, der TCP-Inhaltsprüfung. Dabei werden ACL-basierte Regeln bei jeder Aktualisierung des Anfrageinhalts ausgewertet, bis eine Regel "accept", "reject" oder "switch-mode" passt oder die Wartezeit für die TCP-Anfrageprüfung ohne passende Regel abläuft.

Der erste Unterschied zu "tcp-request connection"-Regeln besteht darin, dass "tcp-request
content"-Regeln Inhalte für ihre Entscheidung verwenden können. Meist geht es dabei um die Erkennung oder Gültigkeit eines Protokolls. Der zweite Unterschied ist, dass inhaltsbasierte Regeln sowohl in Frontends als auch in Backends verwendet werden können. Bei HTTP-Keepalive mit dem Client werden alle tcp-request content-Regeln erneut ausgewertet. HAProxy merkt sich daher, welche Zuordnungen zu Stick-Zählern durch "tcp-request connection" und welche durch "tcp-request content" entstanden sind. Nach der Verarbeitung einer HTTP-Anfrage werden alle inhaltsbezogenen Zuordnungen verworfen, damit die bei der nächsten Anfrage erneut ausgewerteten Regeln sie neu bestimmen können. Dies ist besonders wichtig, wenn eine Regel L7-Informationen verfolgt oder von einer L7-basierten ACL abhängt, da sich die Zuordnung zwischen Anfragen ändern kann.

Inhaltsbasierte Regeln werden genau in der Reihenfolge ihrer Deklaration ausgewertet. Passt keine Regel oder gibt es keine Regel, wird der Inhalt standardmäßig akzeptiert. Die Anzahl der Regeln ist nicht gesondert begrenzt.

Es ist nicht vorgeschrieben, wird aber empfohlen, track-sc0 in "tcp-request
connection"-Regeln, track-sc1 in "tcp-request content"-Regeln des Frontends und track-sc2 in "tcp-request content"-Regeln des Backends zu verwenden. Dies macht die Konfiguration lesbarer und erleichtert die Fehlersuche. Es ist jedoch nur eine Empfehlung; alle Zähler dürfen überall verwendet werden.

Das erste Schlüsselwort nach "tcp-request content" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "TCP RqCnt").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Die Bedingung "if/unless" ist optional. Ohne Bedingung wird die Aktion uneingeschränkt ausgeführt. Dies kann für "track-sc\*"-Aktionen nützlich sein oder um die Standardaktion auf Ablehnen zu ändern.

Es wird außerdem empfohlen, Informationen, die *nicht* vom Inhalt auf Schicht 7 abhängen, mit einer "tcp-request session"-Regel zu verfolgen, besonders bei HTTP-Frontends. Teile der HTTP-Verarbeitung finden auf Sitzungsebene statt und können zu einer frühen Ablehnung der Anfragen führen. Dadurch kann die Verfolgung auf Inhaltsebene beeinträchtigt werden. Beim Start wird eine Warnung ausgegeben, um solche unzuverlässigen Anwendungen möglichst zu verhindern.

In einem TCP-Proxy lassen sich mit "tcp-request content"-Regeln problemlos Inhalte auf Schicht 7 abgleichen. HTTP-spezifische ACL-Abgleiche können den Pufferinhalt vorläufig parsen, bevor sie die benötigten Daten extrahieren. Lässt sich der gepufferte Inhalt nicht als gültige HTTP-Nachricht parsen, passt die ACL nicht. Dabei wird genau derselbe Parser wie bei der übrigen HTTP-Verarbeitung verwendet, sodass keine Gefahr abweichender Interpretation besteht. In einem HTTP-Frontend oder HTTP-Backend ist garantiert, dass die HTTP-Inhalte bereits bei der ersten Auswertung der Regel verfügbar sind: Das HTTP-Parsen erfolgt früh in der Verbindungsverarbeitung auf Sitzungsebene. Für solche Proxys sind "http-request"-Regeln jedoch wesentlich naheliegender und werden empfohlen.

Auch das Verfolgen von layer7-Informationen ist möglich, sofern sie bei der Verarbeitung der Regel vorliegen. Sind die zu verfolgenden Daten noch nicht verfügbar, kann die Regelverarbeitung bis zum Ablauf der Prüfwartezeit warten.

Beispiel:

```text
tcp-request content use-service lua.deny if { src -f /etc/haproxy/blacklist.lst }
```

Beispiel:

```text
tcp-request content set-var(sess.my_var) src
tcp-request content set-var-fmt(sess.from) %[src]:%[src_port]
tcp-request content unset-var(sess.my_var2)
```

Beispiel:

```shell
# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (Only works for HTTP/1 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 30s
tcp-request content accept if is_host_com
tcp-request content reject

# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (works for HTTP/1 and HTTP/2 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 5s
tcp-request content switch-mode http if HTTP
tcp-request content reject   # non-HTTP traffic is implicit here
...
http-request reject unless is_host_com
```

Beispiel:

```shell
# reject SMTP connection if client speaks first
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content reject if content_present

# Forward HTTPS connection only if client speaks
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content accept if content_present
tcp-request content reject
```

Beispiel:

```shell
# Track the last IP(stick-table type string) from X-Forwarded-For
tcp-request inspect-delay 10s
tcp-request content track-sc0 hdr(x-forwarded-for,-1)
# Or track the last IP(stick-table type ip|ipv6) from X-Forwarded-For
tcp-request content track-sc0 req.hdr_ip(x-forwarded-for,-1)
```

Beispiel:

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content track-sc0 base table req-rate
```

Beispiel: Zähler je Frontend und Backend verfolgen und missbräuchliche Clients im Frontend blockieren, wenn das Backend Missbrauch erkennt und gpc0 markiert.

        frontend http
            # Use General Purpose Counter 0 in SC0 as a global abuse counter
            # protecting all our sites
            stick-table type ip size 1m expire 5m store gpc0
            tcp-request connection track-sc0 src
            tcp-request connection reject if { sc0_get_gpc0 gt 0 }
            ...
            use_backend http_dynamic if { path_end .php }

        backend http_dynamic
            # if a source makes too fast requests to this dynamic site (tracked
            # by SC1), block it globally in the frontend.
            stick-table type ip size 1m expire 5m store http_req_rate(10s)
            acl click_too_fast sc1_http_req_rate gt 10
            acl mark_as_abuser sc0_inc_gpc0(http) gt 0
            tcp-request content track-sc1 src
            tcp-request content reject if click_too_fast mark_as_abuser

Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

Siehe auch: "tcp-request connection", "tcp-request session", "tcp-request inspect-delay" und "http-request".

<a id="entry-4-2-tcp-request-inspect-delay"></a>

**`tcp-request inspect-delay <timeout>`**

```haproxy
tcp-request inspect-delay <timeout>
```

Die maximal zulässige Wartezeit auf Daten während der Inhaltsprüfung festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Wer HAProxy hauptsächlich als TCP-Relay verwendet, ist oft besorgt darüber, beliebige Protokolle ohne Analyse an einen Server weiterzugeben. Um Anfrageinhalte analysieren zu können, müssen die Daten zunächst zurückgehalten und anschließend untersucht werden. Diese Anweisung ermöglicht lediglich, Daten höchstens für die angegebene Zeit zurückzuhalten.

Die TCP-Inhaltsprüfung erfolgt sehr früh beim Eintreffen einer Verbindung im Frontend und erneut sehr früh bei ihrer Weiterleitung an ein Backend. Eine Verbindung kann daher zuerst im Frontend und dann ein zweites Mal im Backend verzögert werden, wenn beide tcp-request-Regeln besitzen.

Bei der Inhaltsprüfung wertet HAProxy mit jedem neu eintreffenden Datenblock sämtliche Regeln aus und berücksichtigt dabei, dass die Daten noch unvollständig sind. Passt vor Ablauf der genannten Wartezeit keine Regel, erfolgt beim Ablauf eine letzte Prüfung, bei der die Inhalte als endgültig betrachtet werden. Ohne eingestellte Wartezeit wartet HAProxy überhaupt nicht und entscheidet sofort anhand der verfügbaren Informationen. Dies dürfte wenig nützlich sein und kann sogar von Wettlaufsituationen abhängen; solche Konfigurationen werden daher nicht empfohlen.

Die Prüfwartezeit wird verkürzt, wenn ein Verbindungsfehler oder eine Verbindungsschließung auftritt oder der Anfragepuffer voll ist.

Sobald eine Regel passt, wird die Anfrage freigegeben und wie üblich weiterverarbeitet. Läuft die Zeit ab, ohne dass eine Regel passt, wird die Anfrage standardmäßig unverändert durchgelassen.

Für die meisten Protokolle reichen wenige Sekunden, da die meisten Clients ihre vollständige Anfrage unmittelbar nach dem Verbindungsaufbau senden. Fügen Sie 3 oder mehr Sekunden für TCP-Wiederholungsübertragungen hinzu; mehr ist nicht nötig. Bei manchen Protokollen können große Werte sinnvoll sein, etwa um sicherzustellen, dass der Client niemals vor dem Server spricht, wie bei SMTP, oder um auf Daten des Clients zu warten, bevor Daten an den Server weitergegeben werden, wie bei SSL. Die Clientzeitüberschreitung muss mindestens die Prüfwartezeit abdecken, sonst läuft sie früher ab. Schließt der Client die Verbindung oder ist der Puffer voll, endet die Wartezeit sofort, da sich der Inhalt nicht mehr ändern kann.

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Proxys erben diesen Wert aus ihrem defaults-Abschnitt.

Siehe auch: "tcp-request content accept", "tcp-request content reject", "timeout client".

<a id="entry-4-2-tcp-request-session"></a>

**`tcp-request session <action> [{if | unless} <condition>]`**

```haproxy
tcp-request session <action> [{if | unless} <condition>]
```

Abhängig von einer Bedingung auf Schicht 5 eine Aktion auf einer validierten Sitzung ausführen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| ja \| ja \| nein

Argumente:

```text
<action>    legt die auszuführende Aktion fest, wenn die Bedingung zutrifft.
            Siehe unten.

<condition> ist eine gewöhnliche ACL-basierte Bedingung ausschließlich auf
            Schicht 5 (siehe Abschnitt 7).
```

Sobald eine Sitzung validiert ist, also alle Handshakes abgeschlossen sind, können Bedingungen ausgewertet werden, um zu entscheiden, ob die Sitzung akzeptiert oder verworfen werden muss oder ihre Zähler verfolgt werden sollen. Diese Bedingungen können keine Dateninhalte verwenden, da noch keine Puffer reserviert sind und die Verarbeitung in dieser Phase nicht warten kann. Hauptanwendungsfälle sind das Kopieren früh verfügbarer Informationen in Variablen, die in der Sitzung zugänglich sind, oder das Verfolgen nach dem Handshake erfasster Informationen. Dazu gehören SSL-Elemente wie SNI, Verschlüsselungsverfahren und der CN des Clientzertifikats sowie Informationen aus dem PROXY-Protokollheader, etwa um eine damit übermittelte Quelladresse zu verfolgen. Die extrahierten Informationen können also in eine Variable kopiert oder mit "track-sc"-Regeln verfolgt werden. Natürlich kann wie bei anderen Regelsätzen auch über Akzeptieren oder Ablehnen entschieden werden. Die meisten dieser Vorgänge wären ebenso in "tcp-request content"-Regeln möglich. Bei HTTP werden solche Regeln jedoch bei jeder neuen Anfrage ausgewertet, was nicht immer erwünscht ist. Beispielsweise könnte eine Regel bei jeder Auswertung einen Zähler erhöhen. Ebenso könnte aus der Quell-IP-Adresse per Geolokalisierung ein Land ermittelt und einer sitzungsweit gültigen Variablen zugewiesen werden, während anschließend die Quelladresse für alle Anfragen aus einem HTTP-Header umgeschrieben wird. Müssen für eine Entscheidung Inhalte untersucht werden, sind stattdessen "tcp-request content"-Anweisungen zu verwenden.

Die Regeln "tcp-request session" werden genau in der Reihenfolge ihrer Deklaration ausgewertet. Passt keine Regel oder gibt es keine Regel, wird die eingehende Sitzung standardmäßig akzeptiert. Die Anzahl der Regeln ist nicht gesondert begrenzt.

Das erste Schlüsselwort nach "tcp-request session" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "TCP RqSes").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Die Bedingung "if/unless" ist optional. Ohne Bedingung wird die Aktion uneingeschränkt ausgeführt. Dies kann für "track-sc\*"-Aktionen nützlich sein oder um die Standardaktion auf Ablehnen zu ändern.

Beispiel: Standardmäßig die ursprüngliche Quelladresse verfolgen oder bei Verbindungen von lokalen Proxys die im PROXY-Protokollheader angegebene Adresse. Die erste Regel auf Verbindungsebene aktiviert für diese Verbindungen den Empfang des PROXY-Protokolls. Die zweite Regel verfolgt die Adresse, die nach optionaler Dekodierung beibehalten werden soll.

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }
        tcp-request session track-sc0 src

Beispiel: Alle Sitzungen von Hosts auf der Positivliste annehmen, zu schnell eintreffende Sitzungen ablehnen, ohne sie zu zählen, und angenommene Sitzungen verfolgen. Dadurch wird die Sitzungsrate missbräuchlicher Quellen begrenzt.

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session reject if { src_sess_rate gt 10 }
        tcp-request session track-sc0 src

Beispiel: Alle Sitzungen von Hosts auf der Positivliste annehmen, alle anderen Sitzungen zählen und zu schnell eintreffende ablehnen. Dadurch bleiben missbräuchliche Quellen blockiert, solange sie ihre Rate nicht verringern.

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session track-sc0 src
        tcp-request session reject if { sc0_sess_rate gt 10 }

Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

Siehe auch: "tcp-request connection", "tcp-request content", "stick-table"

<a id="entry-4-2-tcp-response-content"></a>

**`tcp-response content <action> [{if | unless} <condition>]`**

```haproxy
tcp-response content <action> [{if | unless} <condition>]
```

Abhängig von einer Bedingung auf den Schichten 4-7 eine Aktion auf einer Sitzungsantwort ausführen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| nein \| ja \| ja

Argumente:

```text
<action>    legt die auszuführende Aktion fest, wenn die Bedingung zutrifft.
            Siehe unten.

<condition> ist eine gewöhnliche ACL-basierte Bedingung auf den Schichten 4-7
            (siehe Abschnitt 7).
```

Antwortinhalte können in einer frühen Phase der Antwortverarbeitung untersucht werden, der TCP-Inhaltsprüfung. Dabei werden ACL-basierte Regeln bei jeder Aktualisierung des Antwortinhalts ausgewertet, bis entweder eine abschließende Regel passt oder eine festgelegte Wartezeit für die TCP-Antwortprüfung ohne passende Regel abläuft.

Meist geht es bei diesen Entscheidungen um die Erkennung oder Gültigkeit eines Protokolls.

Inhaltsbasierte Regeln werden genau in der Reihenfolge ihrer Deklaration ausgewertet. Passt keine Regel oder gibt es keine Regel, wird der Inhalt standardmäßig akzeptiert. Die Anzahl der Regeln ist nicht gesondert begrenzt.

Das erste Schlüsselwort nach "tcp-response content" in der Syntax ist die Aktion der Regel, auf die optional unterschiedlich viele Argumente für die Aktion folgen. Die unterstützten Aktionen und ihre jeweilige Syntax sind in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) „Aktionen“ aufgeführt (suchen Sie nach Aktionen mit einem Häkchen in der Spalte "TCP RsCnt").

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Im defaults-Abschnitt definierte Regeln werden vor denen im zugehörigen Proxy-Abschnitt ausgewertet. Um Mehrdeutigkeiten zu vermeiden, darf derselbe defaults-Abschnitt in diesem Fall nicht zugleich von Proxys mit Frontend-Funktion und von Proxys mit Backend-Funktion verwendet werden. Ein listen-Abschnitt kann daher keinen defaults-Abschnitt verwenden, der solche Regeln definiert.

Die Bedingung "if/unless" ist optional. Ohne Bedingung wird die Aktion uneingeschränkt ausgeführt. Dies kann nützlich sein, um die Standardaktion auf Ablehnen zu ändern.

Es werden mehrere Arten von Aktionen unterstützt:

Mit "tcp-response content"-Regeln lassen sich problemlos Inhalte auf Schicht 7 abgleichen. Dabei muss jedoch sichergestellt sein, dass eine vollständige Antwort gepuffert wurde, da andernfalls keine Inhalte passen. Die beste Lösung dafür besteht darin, während der Prüfphase das HTTP-Protokoll zu erkennen.

Siehe [Abschnitt 7](/de/haproxy/acls-and-samples/) zur ACL-Verwendung.

Siehe auch: "tcp-request content", "tcp-response inspect-delay"

<a id="entry-4-2-tcp-response-inspect-delay"></a>

**`tcp-response inspect-delay <timeout>`**

```haproxy
tcp-response inspect-delay <timeout>
```

Die maximal zulässige Wartezeit auf eine Antwort während der Inhaltsprüfung festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja(!) \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Diese Direktive ist nur in benannten defaults-Abschnitten verfügbar, nicht in anonymen. Proxys erben diesen Wert aus ihrem defaults-Abschnitt.

Siehe auch: "tcp-response content", "tcp-request inspect-delay".

<a id="entry-4-2-timeout-check"></a>

**`timeout check <timeout>`**

```haproxy
timeout check <timeout>
```

Eine zusätzliche Prüfungszeitüberschreitung festlegen, die erst nach dem Aufbau einer Verbindung gilt.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Ist sie gesetzt, verwendet HAProxy min("timeout connect", "inter") als Verbindungszeitüberschreitung der Prüfung und "timeout
check" als zusätzliche Lesezeitüberschreitung. "min" verhindert, dass *sehr* lange Werte für "timeout connect", etwa wegen Warteschlangen oder Tarpits, die Prüfungen verlangsamen. Für derart lange Verbindungszeitüberschreitungen gibt es allerdings keinen gültigen Grund, da sich dies stets mit "timeout queue" und "timeout tarpit" vermeiden lässt.

Ist "timeout check" nicht gesetzt, verwendet HAProxy "inter" als Zeitüberschreitung für die gesamte Prüfung, also Verbindungsaufbau und Lesen, genau wie alle Versionen \<1.3.15.

Prüfanfragen sind meist viel einfacher und schneller zu bearbeiten als normale Anfragen. Da langsame Server gegebenenfalls ausgeschlossen werden sollen, sollte diese Zeitüberschreitung kleiner als "timeout server" sein.

Dieser Parameter gilt speziell für Backends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Dies ist eine der einfachsten Möglichkeiten, ihn nicht zu vergessen.

Siehe auch: "timeout connect", "timeout queue", "timeout server", "timeout tarpit".

<a id="entry-4-2-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

Die maximale Inaktivitätszeit auf der Clientseite festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Die Inaktivitätszeitüberschreitung gilt, wenn vom Client eine Bestätigung oder das Senden von Daten erwartet wird. Im HTTP-Modus ist sie besonders während der ersten Phase wichtig, in der der Client die Anfrage sendet, sowie während der Antwort, wenn er die vom Server gesendeten Daten liest. Für die erste Phase ist jedoch "timeout http-request" vorzuziehen, um HAProxy besser vor Angriffen wie Slowloris zu schützen. Der Wert wird standardmäßig in Millisekunden angegeben. Durch Anhängen einer Einheit kann entsprechend der Beschreibung am Anfang dieses Dokuments auch eine andere Einheit verwendet werden. Im TCP-Modus und in geringerem Maß auch im HTTP-Modus wird dringend empfohlen, Client- und Serverzeitüberschreitung gleich zu halten, um schwer zu untersuchende Situationen zu vermeiden. Sinnvoll sind Werte knapp oberhalb von Vielfachen von 3 Sekunden, etwa 4 oder 5 Sekunden, um einen oder mehrere TCP-Paketverluste abzudecken. Werden langlebige und kurzlebige Streams wie WebSocket und HTTP gemischt, sollten "timeout tunnel", das bei Tunneln "timeout
client" und "timeout server" überschreibt, sowie "timeout client-fin" für halbgeschlossene Verbindungen erwogen werden.

Dieser Parameter gilt speziell für Frontends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Dies ist eine der einfachsten Möglichkeiten, ihn nicht zu vergessen. Ein nicht angegebener Wert führt zu einer unbegrenzten Wartezeit, was nicht empfohlen wird. Diese Verwendung wird akzeptiert und funktioniert, erzeugt beim Start jedoch eine Warnung: Sind auch die Zeitüberschreitungen des Systems nicht konfiguriert, können sich abgelaufene Sitzungen im System ansammeln.

Siehe auch: "timeout server", "timeout tunnel", "timeout http-request".

<a id="entry-4-2-timeout-client-fin"></a>

**`timeout client-fin <timeout>`**

```haproxy
timeout client-fin <timeout>
```

Die Inaktivitätszeitüberschreitung auf der Clientseite für halbgeschlossene Verbindungen festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Die Inaktivitätszeitüberschreitung gilt, wenn vom Client eine Bestätigung oder das Senden von Daten erwartet wird, während eine Richtung bereits geschlossen ist. Anders als "timeout client" gilt sie nur für in einer Richtung geschlossene Verbindungen. Dies ist besonders nützlich, damit Verbindungen nicht zu lange im Zustand FIN_WAIT bleiben, wenn Clients nicht sauber trennen. Dieses Problem tritt besonders häufig bei langen Verbindungen wie RDP oder WebSocket auf. Diese Zeitüberschreitung kann "timeout tunnel" überschreiben, wenn eine Verbindung in einer Richtung geschlossen wird. Sie wird auf inaktive HTTP/2-Verbindungen angewendet, sobald ein GOAWAY-Frame gesendet wurde, was häufig die Erwartung eines raschen Verbindungsendes ausdrückt.

Dieser Parameter gilt speziell für Frontends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Standardmäßig ist er nicht gesetzt; halbgeschlossene Verbindungen verwenden daher die anderen Zeitüberschreitungen (timeout.client oder timeout.tunnel).

Siehe auch: "timeout client", "timeout server-fin" und "timeout tunnel".

<a id="entry-4-2-timeout-client-hs"></a>

**`timeout client-hs <timeout>`**

```haproxy
timeout client-hs <timeout>
```

Die maximale Wartezeit auf den Abschluss eines Client-TLS-Handshakes festlegen. Dies kann sowohl für TCP- als auch für QUIC-Verbindungen verwendet werden.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Ist diese Handshake-Zeitüberschreitung nicht gesetzt, wird stattdessen die Clientzeitüberschreitung verwendet.

<a id="entry-4-2-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

Die maximale Wartezeit auf einen erfolgreichen Verbindungsaufbau zu einem Server festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Befindet sich der Server im selben LAN wie HAProxy, sollte die Verbindung sofort zustande kommen, also innerhalb weniger Millisekunden. Dennoch ist es sinnvoll, einen oder mehrere TCP-Paketverluste abzudecken, indem Zeitüberschreitungen knapp oberhalb von Vielfachen von 3 Sekunden gewählt werden, etwa 4 oder 5 Sekunden. Standardmäßig setzt die Verbindungszeitüberschreitung auch die Zeitüberschreitungen für Warteschlangen und Tarpits auf denselben Wert, sofern diese nicht angegeben wurden.

Dieser Parameter gilt speziell für Backends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Dies ist eine der einfachsten Möglichkeiten, ihn nicht zu vergessen. Ein nicht angegebener Wert führt zu einer unbegrenzten Wartezeit, was nicht empfohlen wird. Diese Verwendung wird akzeptiert und funktioniert, erzeugt beim Start jedoch eine Warnung: Sind auch die Zeitüberschreitungen des Systems nicht konfiguriert, können sich fehlgeschlagene Sitzungen im System ansammeln.

Siehe auch: "timeout check", "timeout queue", "timeout server", "timeout tarpit".

<a id="entry-4-2-timeout-http-keep-alive"></a>

**`timeout http-keep-alive <timeout>`**

```haproxy
timeout http-keep-alive <timeout>
```

Die maximal zulässige Wartezeit auf den Beginn einer neuen HTTP-Anfrage festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Standardmäßig bestimmt "timeout
http-request" bei Keepalive die Wartezeit auf eine neue Anfrage. Dies ist nicht immer praktisch: Manche möchten sehr kurze Keepalive-Zeitüberschreitungen, um Verbindungen schneller freizugeben. Andere bevorzugen längere Wartezeiten, möchten aber weiterhin kurze Zeitüberschreitungen, sobald die Übertragung einer Anfrage begonnen hat.

Die Zeitüberschreitung "http-keep-alive" deckt diese Anforderungen ab. Sie legt fest, wie lange nach dem Senden einer Antwort auf den Beginn einer neuen HTTP-Anfrage gewartet wird. Sobald das erste Byte der Anfrage eingetroffen ist, gilt "http-request" für die Wartezeit auf die vollständige Anfrage. Leerzeilen vor einer neuen Anfrage starten die Zeitüberschreitung nicht neu und zählen nicht als neue Anfrage.

Es gibt noch einen Unterschied: Läuft eine Verbindung während timeout http-keep-alive ab, wird kein Fehler zurückgegeben; sie wird einfach geschlossen. Läuft sie während "http-request" beim Warten auf die vollständige Anfrage ab, erhält der Client vor dem Schließen einen HTTP-Fehler 408, sofern im Frontend nicht "option http-ignore-probes" gesetzt ist.

Im Allgemeinen eignet sich "timeout http-keep-alive" besonders für Websites mit vielen kurzen Verbindungen, um zu verhindern, dass Clients ansonsten inaktive Verbindungen zu lange offenhalten. Bei HTTP/1.1 lässt sich dies mit Werten von einigen zehn bis einigen hundert Millisekunden erreichen. Die Verbindung wird dann nach dem Abruf einer Seite geschlossen, ohne sie für weitere mögliche Clientaktivität offenhalten zu müssen. Neue Browseraktivität erfordert in diesem Fall einen neuen Handshake auf TCP- und/oder SSL-Ebene. Ein häufiger Anwendungsfall sind HTTP-Websites, die lediglich auf die HTTPS-Seite weiterleiten. Solche Verbindungen sollten nicht lange inaktiv offengehalten werden, da sie nicht wiederverwendet werden, allenfalls zum Abruf eines Favicons.

Ein weiterer Anwendungsfall ist das genaue Gegenteil: Manche Websites möchten Clients erlauben, inaktive Verbindungen lange wiederzuverwenden, etwa 30 Sekunden bis eine Minute, aber nicht so lange auf die erste Anfrage warten. Damit soll ein sehr kostengünstiger Angriffsweg vermieden werden. In diesem Fall wird http-keep-alive hoch gesetzt, während http-request niedrig bleibt, bei wenigen Sekunden.

Bei einem sehr kleinen Wert werden zusätzliche Anfragen ohne Pipelining wahrscheinlich über eine andere Verbindung verarbeitet. Nur echtes Pipelining, bei dem Anfragen direkt hintereinander ohne Warten auf eine Antwort gesendet werden, vermeidet dies; bei HTTP/1.1 ist es sehr selten. Die meisten HTTP/1.1-Implementierungen senden eine Anfrage, warten auf die Antwort und senden dann die nächste. Ein kleiner Wert für HTTP/1.1 kann bei Websites mit Hunderttausenden Clients Speicher und Sockets sparen, erhöht jedoch den Rechenaufwand für Handshakes.

Bei HTTP/2 sollte mit kleinen Werten besonders vorsichtig umgegangen werden. HTTP/2 bündelt Anfragen auf einer Verbindung, um den erneuten Aufbau der TCP- und/oder SSL-Schicht zu vermeiden. Das Protokoll verwendet außerdem Steuerframes, die mit frühzeitig geschlossenen TCP-Verbindungen schlecht zurechtkommen. In sehr seltenen Fällen können dadurch Antworten abgeschnitten werden, wenn Daten nach dem Verlassen von HAProxy unterwegs verloren gehen. HAProxy kann dann nicht einmal einen Fehler protokollieren. Ein empfohlener niedriger Ausgangswert für HTTP/2-Verbindungen liegt bei etwa 4 Sekunden. Dies verhindert bei den meisten modernen Keepalive-Implementierungen, dass ungenutzte Verbindungen unnötig offenbleiben, und erlaubt zugleich nachfolgenden Anfragen die Wiederverwendung. Der Wert ist jedoch nur ein Ausgangspunkt und sollte nach Bedarf angepasst werden.

Ist dieser Parameter nicht gesetzt, gilt "http-request". Sind beide nicht gesetzt, gilt auf der darunterliegenden Ebene weiterhin "timeout
client". Damit der Parameter wirkt, sollte er im Frontend gesetzt werden. Befindet sich das Frontend im TCP-Modus, wird stattdessen die Zeitüberschreitung des HTTP-Backends verwendet.

Siehe auch: "timeout http-request", "timeout client".

<a id="entry-4-2-timeout-http-request"></a>

**`timeout http-request <timeout>`**

```haproxy
timeout http-request <timeout>
```

Die maximal zulässige Wartezeit auf eine vollständige HTTP-Anfrage festlegen

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Für den Schutz vor DoS-Angriffen kann es erforderlich sein, die maximal zulässige Zeit zum Empfang einer vollständigen HTTP-Anfrage zu verkürzen, ohne die Clientzeitüberschreitung zu verändern. Dies schützt vor aufgebauten Verbindungen, über die nichts gesendet wird. Die Clientzeitüberschreitung schützt dagegen nicht ausreichend, weil sie nur Inaktivität erfasst: Sendet ein Angreifer gelegentlich ein Zeichen, wird sie nicht ausgelöst. Mit der HTTP-Anfragezeitüberschreitung wird die Anfrage unabhängig von der Sendegeschwindigkeit des Clients abgebrochen, wenn sie nicht rechtzeitig vollständig vorliegt. Beim Ablauf erhält der Client eine HTTP-Antwort 408 als Hinweis auf das Problem, und die Verbindung wird geschlossen. Im Protokoll erscheint der Beendigungscode "cR". Manche neueren Browser haben Probleme mit diesem standardkonformen, gut dokumentierten Verhalten. Daher kann es nötig sein, den Code 408 mit "option http-ignore-probes" oder "errorfile 408 /dev/null" zu verbergen. Weitere Einzelheiten stehen bei der Erläuterung des Beendigungscodes "cR" in [Abschnitt 8.5](/de/haproxy/configuration-logging/#section-8-5).

Standardmäßig gilt diese Zeitüberschreitung nur für den Headerteil der Anfrage, nicht für Daten. Sobald die Leerzeile empfangen wurde, gilt sie nicht mehr. Zusammen mit "option
http-buffer-request" gilt sie auch für den Anfragekörper. Bei Keepalive-Verbindungen wird sie erneut zum Warten auf eine zweite Anfrage verwendet, wenn "timeout http-keep-alive" nicht gesetzt ist.

Meist reichen wenige Sekunden, da die meisten Clients die vollständige Anfrage unmittelbar nach dem Verbindungsaufbau senden. Fügen Sie 3 oder mehr Sekunden für TCP-Wiederholungsübertragungen hinzu; mehr ist nicht nötig. Sehr niedrige Werte, etwa 50 ms, funktionieren in lokalen Netzen gewöhnlich, solange keine Pakete verloren gehen. Sie verhindern allerdings, dass Benutzer rohe HTTP-Anfragen mit Telnet eingeben.

Ist dieser Parameter nicht gesetzt, gilt weiterhin die Clientzeitüberschreitung zwischen den einzelnen eintreffenden Datenblöcken der Anfrage. Damit der Parameter wirkt, sollte er im Frontend gesetzt werden. Befindet sich das Frontend im TCP-Modus, wird stattdessen die Zeitüberschreitung des HTTP-Backends verwendet.

Siehe auch: "errorfile", "http-ignore-probes", "timeout http-keep-alive", "timeout client" und "option http-buffer-request".

<a id="entry-4-2-timeout-queue"></a>

**`timeout queue <timeout>`**

```haproxy
timeout queue <timeout>
```

Die maximale Wartezeit in der Warteschlange auf einen freien Verbindungsplatz festlegen

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Wird der maxconn-Wert eines Servers erreicht, bleiben Verbindungen in einer Warteschlange. Diese kann serverspezifisch sein oder für das gesamte Backend gelten. Damit die Wartezeit nicht unbegrenzt ist, gilt für die wartenden Anfragen eine Zeitüberschreitung. Wird sie erreicht, wird angenommen, dass die Anfrage praktisch nicht mehr bedient werden kann. Sie wird deshalb verworfen, und der Client erhält einen Fehler 503.

Die Anweisung "timeout queue" legt fest, wie lange eine Anfrage höchstens in einer Warteschlange verbleiben darf. Fehlt die Angabe, gilt aus Gründen der Abwärtskompatibilität mit älteren Versionen ohne "timeout queue" derselbe Wert wie für die Verbindungszeitüberschreitung des Backends ("timeout connect").

Siehe auch: "timeout connect".

<a id="entry-4-2-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

Die maximale Inaktivitätszeit auf der Serverseite festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Die Inaktivitätszeitüberschreitung gilt, wenn vom Server eine Bestätigung oder das Senden von Daten erwartet wird. Im HTTP-Modus ist sie besonders in der ersten Phase der Serverantwort wichtig, in der die Header gesendet werden müssen: Sie bildet unmittelbar die Verarbeitungszeit der Anfrage auf dem Server ab. Zur Wahl eines geeigneten Werts ist es oft sinnvoll, mit einer als nicht mehr akzeptabel angesehenen Antwortzeit zu beginnen, anschließend anhand der Protokolle die Verteilung der Antwortzeiten zu beobachten und den Wert entsprechend anzupassen.

Der Wert wird standardmäßig in Millisekunden angegeben. Durch Anhängen einer Einheit kann entsprechend der Beschreibung am Anfang dieses Dokuments auch eine andere Einheit verwendet werden. Im TCP-Modus und in geringerem Maß auch im HTTP-Modus wird dringend empfohlen, Client- und Serverzeitüberschreitung gleich zu halten, um schwer zu untersuchende Situationen zu vermeiden. Unabhängig von den erwarteten Serverantwortzeiten ist es sinnvoll, mindestens einen oder mehrere TCP-Paketverluste abzudecken. Dafür eignen sich Werte knapp oberhalb von Vielfachen von 3 Sekunden, etwa mindestens 4 oder 5 Sekunden. Werden langlebige und kurzlebige Streams wie WebSocket und HTTP gemischt, sollte "timeout tunnel" erwogen werden, das bei Tunneln "timeout client" und "timeout server" überschreibt.

Dieser Parameter gilt speziell für Backends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Dies ist eine der einfachsten Möglichkeiten, ihn nicht zu vergessen. Ein nicht angegebener Wert führt zu einer unbegrenzten Wartezeit, was nicht empfohlen wird. Diese Verwendung wird akzeptiert und funktioniert, erzeugt beim Start jedoch eine Warnung: Sind auch die Zeitüberschreitungen des Systems nicht konfiguriert, können sich abgelaufene Sitzungen im System ansammeln.

Siehe auch: "timeout client" und "timeout tunnel".

<a id="entry-4-2-timeout-server-fin"></a>

**`timeout server-fin <timeout>`**

```haproxy
timeout server-fin <timeout>
```

Die Inaktivitätszeitüberschreitung auf der Serverseite für halbgeschlossene Verbindungen festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http, log

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Die Inaktivitätszeitüberschreitung gilt, wenn vom Server eine Bestätigung oder das Senden von Daten erwartet wird, während eine Richtung bereits geschlossen ist. Anders als "timeout server" gilt sie nur für in einer Richtung geschlossene Verbindungen. Dies ist besonders nützlich, damit Verbindungen nicht zu lange im Zustand FIN_WAIT bleiben, wenn ein entfernter Server nicht sauber trennt. Dieses Problem tritt besonders häufig bei langen Verbindungen wie RDP oder WebSocket auf. Diese Zeitüberschreitung kann "timeout tunnel" überschreiben, wenn eine Verbindung in einer Richtung geschlossen wird. Die Einstellung wurde der Vollständigkeit halber bereitgestellt, sollte in den meisten Situationen aber nicht benötigt werden.

Dieser Parameter gilt speziell für Backends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Standardmäßig ist er nicht gesetzt; halbgeschlossene Verbindungen verwenden daher die anderen Zeitüberschreitungen (timeout.server oder timeout.tunnel).

Siehe auch: "timeout client-fin", "timeout server" und "timeout tunnel".

<a id="entry-4-2-timeout-tarpit"></a>

**`timeout tarpit <timeout>`**

```haproxy
timeout tarpit <timeout>
```

Die Dauer festlegen, für die im Tarpit gehaltene Verbindungen bestehen bleiben

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<timeout> ist die Tarpit-Dauer, standardmäßig in Millisekunden. Jede andere
          Einheit ist möglich, wenn sie wie am Anfang dieses Dokuments
          erläutert an die Zahl angehängt wird.
```

Wird eine Verbindung mit "http-request tarpit" in einen Tarpit versetzt, bleibt sie für eine bestimmte Zeit ohne Aktivität offen und wird anschließend geschlossen. "timeout tarpit" legt fest, wie lange sie offengehalten wird.

Der Wert wird standardmäßig in Millisekunden angegeben. Durch Anhängen einer Einheit kann entsprechend der Beschreibung am Anfang dieses Dokuments auch eine andere Einheit verwendet werden. Fehlt die Angabe, gilt aus Gründen der Abwärtskompatibilität mit älteren Versionen ohne "timeout tarpit" derselbe Wert wie für die Verbindungszeitüberschreitung des Backends ("timeout connect").

Siehe auch: "timeout connect".

<a id="entry-4-2-timeout-tunnel"></a>

**`timeout tunnel <timeout>`**

```haproxy
timeout tunnel <timeout>
```

Die maximale Inaktivitätszeit auf Client- und Serverseite für Tunnel festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente:

```text
<timeout> ist der Zeitüberschreitungswert, standardmäßig in Millisekunden.
          Jede andere Einheit ist möglich, wenn sie wie am Anfang dieses
          Dokuments erläutert an die Zahl angehängt wird.
```

Die Tunnelzeitüberschreitung gilt, wenn zwischen Client und Server eine bidirektionale Verbindung besteht und diese in beiden Richtungen inaktiv bleibt. Sobald die Verbindung zum Tunnel wird, ersetzt sie sowohl die Client- als auch die Serverzeitüberschreitung. Bei TCP gilt sie, sobald an keiner der beiden Verbindungen mehr eine Analysefunktion aktiv ist, etwa nachdem die TCP-Inhaltsregeln den Inhalt akzeptiert haben. Bei HTTP gilt sie nach einem Protokollwechsel, etwa zu WebSocket oder beim Weiterleiten einer CONNECT-Anfrage an einen Proxy, oder nach der ersten Antwort, wenn keine Keepalive- oder Schließoption angegeben ist.

Da diese Zeitüberschreitung gewöhnlich für langlebige Verbindungen verwendet wird, ist es meist sinnvoll, auch "timeout client-fin" zu setzen. Damit lässt sich behandeln, dass ein Client plötzlich aus dem Netz verschwindet und eine Schließung nicht bestätigt oder selbst eine Schließung sendet und ausstehende Daten nicht mehr bestätigt. Dies kann in verlustbehafteten Netzen mit Firewalls auftreten und ist an vielen Sitzungen im Zustand FIN_WAIT erkennbar.

Der Wert wird standardmäßig in Millisekunden angegeben. Durch Anhängen einer Einheit kann entsprechend der Beschreibung am Anfang dieses Dokuments auch eine andere Einheit verwendet werden. Unabhängig von der erwarteten normalen Inaktivitätsdauer ist es sinnvoll, mindestens einen oder mehrere TCP-Paketverluste abzudecken. Dafür eignen sich Werte knapp oberhalb von Vielfachen von 3 Sekunden, etwa mindestens 4 oder 5 Sekunden.

Dieser Parameter gilt speziell für Backends, kann jedoch in "defaults"-Abschnitten einmal für alle festgelegt werden. Dies ist eine der einfachsten Möglichkeiten, ihn nicht zu vergessen.

Beispiel:

```text
defaults http
    option http-server-close
    timeout connect 5s
    timeout client 30s
    timeout client-fin 30s
    timeout server 30s
    timeout tunnel  1h    # timeout to use with WebSocket and CONNECT
```

Siehe auch: "timeout client", "timeout client-fin", "timeout server".

<a id="entry-4-2-transparent"></a>

**`transparent (deprecated)`**

```haproxy
transparent (deprecated)
```

Transparente Proxyverarbeitung auf der Clientseite aktivieren

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| nein \| ja \| ja

Argumente: keine

Dieses Schlüsselwort wurde eingeführt, um Load-Balancern auf Schicht 3 eine Sitzungsbindung auf Schicht 7 bereitzustellen. Dazu wird die Fähigkeit des Betriebssystems genutzt, eine eingehende Verbindung zu einer entfernten Adresse an einen lokalen Prozess, hier HAProxy, umzuleiten und diesem die ursprünglich angeforderte Adresse mitzuteilen. Bei dieser Option werden Sitzungen ohne Cookies an die ursprüngliche Ziel-IP-Adresse der eingehenden Anfrage weitergeleitet, die mit der eines anderen Geräts übereinstimmen sollte. Anfragen mit Cookies werden weiterhin an den passenden Server weitergeleitet.

Das Schlüsselwort "transparent" ist veraltet. Verwenden Sie stattdessen "option transparent".

Entgegen einer verbreiteten Annahme bewirkt diese Option NICHT, dass HAProxy beim Verbindungsaufbau dem Server die IP-Adresse des Clients präsentiert.

Siehe auch: "option transparent"

<a id="entry-4-2-unique-id-format"></a>

**`unique-id-format <fmt>`**

```haproxy
unique-id-format <fmt>
```

Für jede Anfrage eine eindeutige ID erzeugen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| ja

Argumente:

```text
<fmt>   ist eine Zeichenfolge im benutzerdefinierten Protokollformat
        (siehe Abschnitt 8.2.6).
```

Dieses Schlüsselwort erzeugt mit dem benutzerdefinierten Protokollformat für jede Anfrage eine ID. Eine eindeutige ID hilft, eine Anfrage durch viele Komponenten einer komplexen Infrastruktur zu verfolgen. Die neu erzeugte ID kann auch mit dem Alias %ID in der benutzerdefinierten Formatzeichenkette protokolliert werden.

Das Format sollte aus Elementen bestehen, deren Kombination garantiert eindeutig ist. Sind beispielsweise mehrere HAProxy-Instanzen beteiligt, kann es wichtig sein, den Knotennamen einzubeziehen. Häufig müssen auch Quell- und Zieladressen sowie Ports der eingehenden Verbindung protokolliert werden. Da über dieselbe Verbindung mehrere Anfragen erfolgen können, kann ein Anfragezähler bei ihrer Unterscheidung helfen. Ebenso kann ein Zeitstempel vor dem Überlauf des Zählers schützen. Das Protokollieren der Prozess-ID vermeidet Kollisionen nach einem Neustart des Dienstes.

Für viele Felder wird die hexadezimale Darstellung empfohlen, da sie kompakter ist und Platz im Protokoll spart.

Bei normalen Verbindungen wird die eindeutige ID mit dem im Frontend konfigurierten Format erzeugt. Bei Health Checks wird das Backendformat verwendet, wenn der Abruf "unique-id" innerhalb eines tcp-check- oder http-check-Regelsatzes verwendet wird.

Beispiel:

```text
unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid

erzeugt:

       7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A
```

Siehe auch: "unique-id-header"

<a id="entry-4-2-unique-id-header"></a>

**`unique-id-header <name>`**

```haproxy
unique-id-header <name>
```

Der HTTP-Anfrage einen Header mit einer eindeutigen ID hinzufügen.

Kann in folgenden Kontexten verwendet werden: http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend ja \| ja \| ja \| nein

Argumente:

```text
<name>   ist der Name des Headers.
```

Mit unique-id-format einen unique-id-Header in die an den Server gesendete HTTP-Anfrage einfügen. Ohne vorhandenes unique-id-format funktioniert dies nicht.

Beispiel:

```text
    unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid
    unique-id-header X-Unique-ID

    erzeugt:

       X-Unique-ID: 7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A

Siehe auch: "unique-id-format"
```

<a id="entry-4-2-use-backend"></a>

**`use_backend <backend> [{if | unless} <condition>]`**

```haproxy
use_backend <backend> [{if | unless} <condition>]
```

Zu einem bestimmten Backend wechseln, wenn eine ACL-basierte Bedingung erfüllt beziehungsweise nicht erfüllt ist.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| ja \| ja \| nein

Argumente:

```text
<backend>   ist der Name eines gültigen backend- oder "listen"-Abschnitts
            oder ein benutzerdefiniertes Protokollformat, das einen Backend-Namen
            ergibt (siehe benutzerdefinierte Protokollformate in Abschnitt 8.2.6).

<condition> ist eine Bedingung aus ACLs wie in Abschnitt 7 beschrieben.
            Ohne Angabe wird die Regel bedingungslos angewendet.
```

Bei der inhaltsabhängigen Umschaltung treffen Verbindungen in einem Frontend ein und werden anschließend anhand verschiedener Bedingungen auf Backends verteilt. Das Schlüsselwort "use_backend" beschreibt die Zuordnung zwischen Bedingungen und Backends. Es wird üblicherweise bei HTTP-Verarbeitung eingesetzt, kann aber auch bei reinem TCP verwendet werden: entweder ohne Inhalte mit zustandslosen ACLs, etwa zur Prüfung der Quelladresse, oder zusammen mit einer "tcp-request"-Regel, um auf Nutzdaten zu warten.

Es können beliebig viele "use_backend"-Regeln angegeben werden. Sie werden in der Reihenfolge ihrer Deklaration ausgewertet; die erste passende Regel bestimmt das Backend. Dies gilt selbst dann, wenn das Backend als ausgefallen gilt. Verweist eine passende Regel jedoch auf ein deaktiviertes oder unveröffentlichtes Backend, wird sie ignoriert und die Regelauswertung fortgesetzt.

Bei der ersten Form wird das Backend verwendet, wenn die Bedingung erfüllt ist, bei der zweiten, wenn sie nicht erfüllt ist. Trifft keine Bedingung zu, wird das mit "default_backend" festgelegte Backend verwendet, sofern es nicht deaktiviert oder unveröffentlicht ist. Ist kein Standardbackend verfügbar, werden bei einem "listen"-Abschnitt die Server desselben Abschnitts verwendet. Bei einem Frontend wird dagegen kein Server verwendet und eine Antwort 503 service unavailable zurückgegeben.

Ein Wechsel von einem TCP-Frontend zu einem HTTP-Backend ist möglich. Hat das Frontend bereits geprüft, dass das Protokoll HTTP ist, beginnt die Backendverarbeitung sofort. Andernfalls wartet das Backend auf eine vollständige HTTP-Anfrage. Dies ist nützlich, wenn ein Frontend mehrere Protokolle auf einem einzigen Port dekodieren muss und eines davon HTTP ist.

Ist `<backend>` ein einfacher Name, wird er beim Einlesen der Konfiguration aufgelöst. Existiert das angegebene Backend nicht, wird ein Fehler gemeldet. Ist `<backend>` stattdessen ein benutzerdefiniertes Protokollformat, kann zu diesem Zeitpunkt keine Prüfung erfolgen. Der Backendname wird dann dynamisch zur Laufzeit aufgelöst. Entspricht der ermittelte Name keinem gültigen Backend, werden keine weiteren Regeln ausgewertet; stattdessen wird die Direktive default_backend angewendet. Bei dynamischen Backendnamen wird dringend empfohlen, ein Präfix zu verwenden, das kein anderes Backend verwendet. So wird sichergestellt, dass über die Anfrage kein unzulässiges Backend erzwungen werden kann.

"use_backend"-Regeln mit ausdrücklich angegebenem Namen dienen dazu, die Zuordnung zwischen Frontends und Backends zu ermitteln und damit die Backend-Einstellung "fullconn" zu berechnen. Bei dynamischen Namen ist dies nicht möglich.

Siehe auch: "default_backend", "tcp-request", "fullconn", "log-format" und [Abschnitt 7](/de/haproxy/acls-and-samples/) zu ACLs.

<a id="entry-4-2-use-fcgi-app"></a>

**`use-fcgi-app <name>`**

```haproxy
use-fcgi-app <name>
```

Die für das Backend zu verwendende FastCGI-Anwendung festlegen.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<name>    ist der Name der zu verwendenden FastCGI-Anwendung.
```

Einzelheiten zur Einrichtung von FastCGI-Anwendungen enthält [Abschnitt 10.1](/de/haproxy/fastcgi/#section-10-1).

<a id="entry-4-2-use-server"></a>

**`use-server <server> if <condition>`**

```haproxy
use-server <server> if <condition>
use-server <server> unless <condition>
```

Einen bestimmten Server nur verwenden, wenn eine ACL-basierte Bedingung erfüllt beziehungsweise nicht erfüllt ist.

Kann in folgenden Kontexten verwendet werden: tcp, http

Kann in folgenden Abschnitten verwendet werden: defaults \| frontend \| listen \| backend nein \| nein \| ja \| ja

Argumente:

```text
<server>    ist der Name eines gültigen Servers im selben Backend-Abschnitt
            oder eine Zeichenfolge im benutzerdefinierten Protokollformat,
            die einen Servernamen ergibt (siehe Abschnitt 8.2.6).

<condition> ist eine Bedingung aus ACLs wie in Abschnitt 7 beschrieben.
```

Standardmäßig werden Verbindungen, die ein Backend erreichen, gemäß dem konfigurierten Algorithmus auf die verfügbaren Server verteilt. Eine Ausnahme besteht, wenn ein Mechanismus zur Sitzungsbindung, etwa ein Cookie, verwendet und in der Anfrage gefunden wird.

Manchmal soll eine bestimmte Anfrage an einen bestimmten Server geleitet werden, ohne dafür ein eigenes Backend zu deklarieren. Dies ermöglichen "use-server"-Regeln. Sie werden nach den "redirect"-Regeln und vor den Cookies ausgewertet und haben Vorrang vor den Cookies. Es können beliebig viele "use-server"-Regeln angegeben werden. Sie werden in der Reihenfolge ihrer Deklaration ausgewertet; die erste passende Regel bestimmt den Server.

Wenn eine Regel einen ausgefallenen Server bezeichnet, "option persist" nicht verwendet wird und keine force-persist-Regel gegriffen hat, wird diese Regel ignoriert. Die Auswertung wird mit den folgenden Regeln fortgesetzt, bis eine passt.

Bei der ersten Form wird der Server verwendet, wenn die Bedingung erfüllt ist, bei der zweiten, wenn sie nicht erfüllt ist. Trifft keine Bedingung zu, wird die Verarbeitung fortgesetzt und der Server anhand anderer Mechanismen zur Sitzungsbindung zugewiesen.

Auch bei einer passenden Regel werden Cookies weiterhin verarbeitet, bestimmen dann aber nicht den Server. So können Präfixe aus Cookies mit vorangestelltem Präfix entfernt werden.

Die Anweisung "use-server" funktioniert sowohl im HTTP- als auch im TCP-Modus und eignet sich daher für die inhaltsbasierte Prüfung. Bei Protokollen mit implizitem TLS könnte beispielsweise ein Server aus einer Farm anhand des TLS-SNI-Felds ausgewählt werden; siehe auch "req.ssl_sni". Ist das Gewicht dieser Server auf null gesetzt, werden sie nicht für anderen Datenverkehr verwendet.

Beispiel:

```shell
# intercept incoming TLS requests based on the SNI field
use-server www if { req.ssl_sni -i www.example.com }
server     www 192.168.0.1:443 weight 0
use-server mail if { req.ssl_sni -i mail.example.com }
server     mail 192.168.0.1:465 weight 0
use-server imap if { req.ssl_sni -i imap.example.com }
server     imap 192.168.0.1:993 weight 0
# all the rest is forwarded to this server
server  default 192.168.0.2:443 check
```

Wenn `<server>` ein einfacher Name ist, wird er mit den vorhandenen Servern in der Konfiguration abgeglichen. Existiert der angegebene Server nicht, wird ein Fehler gemeldet. Handelt es sich um ein benutzerdefiniertes Protokollformat, erfolgt beim Parsen der Konfiguration keine Prüfung. Wenn zur Laufzeit kein gültiger Servername ermittelt werden kann, die use-server-Regel aber von einer ACL abhängig war, die wahr zurückgab, wird keine weitere use-server-Regel angewendet und auf die Lastverteilung zurückgegriffen.

Siehe auch: "use_backend", [Abschnitt 5](/de/haproxy/bind-and-server-options/) zu Servern und [Abschnitt 7](/de/haproxy/acls-and-samples/) zu ACLs.

## 4.3. Matrix der Aktionsschlüsselwörter {#section-4-3}

In verschiedenen Phasen der Anfrage- oder Antwortverarbeitung werden mehrere Regelsätze ausgewertet. Für jede darin enthaltene Regel kann eine Aktion ausgeführt werden, wenn die optionale Bedingung erfüllt ist.

Standardmäßig stehen zahlreiche Aktionen zur Verfügung. Sie können Inhalte ändern, die Verarbeitung zulassen oder blockieren, interne Zustände ändern usw. Außerdem können neue Aktionen in Lua definiert werden; deren Namen beginnen dann immer mit "lua.".

Während einige Aktionen früher nur in bestimmten Regelsätzen verfügbar waren, lassen sich heute viele Aktionen in vielen Regelsätzen verwenden. Die Aufstellung in diesem Abschnitt zeigt für jede unterstützte Aktion durch Markierung der entsprechenden abgekürzten Einträge, in welchen der folgenden Regelsätze sie verwendet werden kann:

- QUIC Ini: Die Aktion ist für "quic-initial"-Regeln gültig.
- TCP RqCon: Die Aktion ist für "tcp-request connection"-Regeln gültig.
- TCP RqSes: Die Aktion ist für "tcp-request session"-Regeln gültig.
- TCP RqCnt: Die Aktion ist für "tcp-request content"-Regeln gültig.
- TCP RsCnt: Die Aktion ist für "tcp-response content"-Regeln gültig.
- HTTP Req: Die Aktion ist für "http-request"-Regeln gültig.
- HTTP Res: Die Aktion ist für "http-response"-Regeln gültig.
- HTTP Aft: Die Aktion ist für "http-after-response"-Regeln gültig.

Dieselben Abkürzungen werden in der nachfolgenden Referenz in [Abschnitt 4.4](/de/haproxy/proxies/#section-4-4) verwendet.

```text
 Schlüsselwort          QUIC: Ini   TCP: RqCon RqSes RqCnt RsCnt   HTTP: Req Res Aft
----------------------+-----------+-----------+-----+-----+------+----------+---+----
accept                         X           X     X     X     X            -   -   -
add-acl                        -           -     -     -     -            X   X   -
add-header                     -           -     -     -     -            X   X   X
add-headers-bin                -           -     -     -     -            X   X   X
allow                          -           -     -     -     -            X   X   X
attach-srv                     -           -     X     -     -            -   -   -
auth                           -           -     -     -     -            X   -   -
cache-store                    -           -     -     -     -            -   X   -
cache-use                      -           -     -     -     -            X   -   -
capture                        -           -     -     X     -            X   X   X
close                          -           -     -     -     X            -   -   -
del-acl                        -           -     -     -     -            X   X   -
del-header                     -           -     -     -     -            X   X   X
del-headers-bin                -           -     -     -     -            X   X   X
del-map                        -           -     -     -     -            X   X   X
deny                           -           -     -     -     -            X   X   -
dgram-drop                     X           -     -     -     -            -   -   -
disable-l7-retry               -           -     -     -     -            X   -   -
do-log                         X           X     X     X     X            X   X   X
do-resolve                     -           -     -     X     -            X   -   -
early-hint                     -           -     -     -     -            X   -   -
expect-netscaler-cip           -           X     -     -     -            -   -   -
expect-proxy layer4            -           X     -     -     -            -   -   -
normalize-uri                  -           -     -     -     -            X   -   -
pause                          -           -     -     -     -            X   X   -
redirect                       -           -     -     -     -            X   X   -
reject                         X           X     X     X     X            X   -   -
replace-header                 -           -     -     -     -            X   X   X
replace-path                   -           -     -     -     -            X   -   -
replace-pathq                  -           -     -     -     -            X   -   -
replace-uri                    -           -     -     -     -            X   -   -
replace-value                  -           -     -     -     -            X   X   X
return                         -           -     -     -     -            X   X   -
sc-add-gpc                     -           X     X     X     X            X   X   X
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-sc-inc-gpc                     -           X     X     X     X            X   X   X
sc-inc-gpc0                    -           X     X     X     X            X   X   X
sc-inc-gpc1                    -           X     X     X     X            X   X   X
sc-set-gpt                     -           X     X     X     X            X   X   X
sc-set-gpt0                    -           X     X     X     X            X   X   X
send-retry                     X           -     -     -     -            -   -   -
send-spoe-group                -           -     -     X     X            X   X   -
set-bandwidth-limit            -           -     -     X     X            X   X   -
set-bc-mark                    -           -     -     X     -            X   -   -
set-bc-tos                     -           -     -     X     -            X   -   -
set-dst                        -           X     X     X     -            X   -   -
set-dst-port                   -           X     X     X     -            X   -   -
set-fc-mark                    -           X     X     X     X            X   X   -
set-fc-tos                     -           X     X     X     X            X   X   -
set-header                     -           -     -     -     -            X   X   X
set-headers-bin                -           -     -     -     -            X   X   X
set-log-level                  -           -     -     X     X            X   X   X
set-map                        -           -     -     -     -            X   X   X
set-mark (deprecated)          -           X     X     X     X            X   X   -
set-method                     -           -     -     -     -            X   -   -
set-nice                       -           -     -     X     X            X   X   -
set-path                       -           -     -     -     -            X   -   -
set-pathq                      -           -     -     -     -            X   -   -
set-priority-class             -           -     -     X     -            X   -   -
set-priority-offset            -           -     -     X     -            X   -   -
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-set-query                      -           -     -     -     -            X   -   -
set-retries                    -           -     -     X     -            X   -   -
set-src                        -           X     X     X     -            X   -   -
set-src-port                   -           X     X     X     -            X   -   -
set-status                     -           -     -     -     -            -   X   X
set-timeout                    -           -     -     -     -            X   X   -
set-tos (deprecated)           -           X     X     X     X            X   X   -
set-uri                        -           -     -     -     -            X   -   -
set-var                        -           X     X     X     X            X   X   X
set-var-fmt                    -           X     X     X     X            X   X   X
silent-drop                    -           X     X     X     X            X   X   -
strict-mode                    -           -     -     -     -            X   X   X
switch-mode                    -           -     -     X     -            -   -   -
tarpit                         -           -     -     -     -            X   -   -
track-sc0                      -           X     X     X     -            X   X   -
track-sc1                      -           X     X     X     -            X   X   -
track-sc2                      -           X     X     X     -            X   X   -
unset-var                      -           X     X     X     X            X   X   X
use-service                    -           -     -     X     -            X   -   -
wait-for-body                  -           -     -     -     -            X   X   -
wait-for-handshake             -           -     -     -     -            X   -   -
--keyword---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-
```

## 4.4. Alphabetisch sortierte Aktionsreferenz {#section-4-4}

Dieser Abschnitt beschreibt jede Aktion und ihre Verwendung ausführlich. Für die Kennzeichnung der Regelsätze wird dieselbe Terminologie wie oben in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3) verwendet.

<a id="entry-4-4-accept"></a>

**`accept`**

```haproxy
accept
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| - \| - \| -

Dies beendet die Regelauswertung und lässt die Anfrage oder Antwort die Prüfung passieren. Diese Aktion ist abschließend, d. h. für den aktuellen Abschnitt werden keine weiteren Regeln desselben Regelsatzes ausgewertet. Sie unterscheidet sich von der Aktion "allow" nur dadurch, dass aus Gründen historischer Kompatibilität "accept" für TCP- und QUIC-Regeln und "allow" für HTTP-Regeln verwendet wird. Siehe auch die Aktion "allow" weiter unten.

<a id="entry-4-4-add-acl"></a>

**`add-acl(<file-name>) <key fmt>`**

```haproxy
add-acl(<file-name>) <key fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Damit wird einer ACL ein neuer Eintrag hinzugefügt. Die ACL muss aus einer Datei geladen werden, auch wenn diese nur eine leere Platzhalterdatei ist. Der Dateiname der zu aktualisierenden ACL wird in Klammern angegeben. Die Aktion nimmt ein Argument entgegen: `<key fmt>`, das den in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschriebenen Regeln für benutzerdefinierte Protokollformate folgt, um den Inhalt des neuen Eintrags zu ermitteln. Vor dem Einfügen wird die ACL durchsucht, um doppelte oder mehrfach vorhandene Werte zu vermeiden. Dies entspricht dem Befehl "add acl" am Statistik-Socket, kann jedoch durch eine HTTP-Anfrage ausgelöst werden.

<a id="entry-4-4-add-header"></a>

**`add-header <name> <fmt>`**

```haproxy
add-header <name> <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies hängt ein HTTP-Header-Feld an, dessen Name in `<name>` und dessen Wert durch `<fmt>` festgelegt wird. Letzteres folgt den Regeln für benutzerdefinierte Protokollformate (siehe „Benutzerdefiniertes Protokollformat“ in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6)). Dies ist besonders nützlich, um verbindungsspezifische Informationen an den Server weiterzugeben, etwa das SSL-Zertifikat des Clients, oder um mehrere Header zu einem zusammenzufassen. Diese Regel ist nicht abschließend, sodass weitere ähnliche Regeln hinzugefügt werden können. Beachten Sie, dass der Header sofort hinzugefügt wird. Eine Regel kann daher den aus einer vorherigen Regel entstandenen Header wiederverwenden.

<a id="entry-4-4-add-headers-bin"></a>

**`add-headers-bin <expr> [ prefix <str> ]`**

```haproxy
add-headers-bin <expr> [ prefix <str> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies ist eine Variante der Aktion "add-header", bei der die Header-Namen und -Werte als binäre Zeichenfolge mit varint-Kodierung übergeben werden. Informationen zum varint-Format finden Sie beim Sample-Abruf "req.hdrs_bin". Dies ist nützlich, wenn mehrere Header gleichzeitig gesetzt werden sollen, ohne ihre Namen im Voraus kennen zu müssen. Beachten Sie, dass diese Header nicht vom HTTP-Parser validiert wurden. Dadurch können ungültige Nachrichten ausgegeben werden; im schlimmsten Fall kann dies Request-Smuggling-Angriffe ermöglichen. Auch die Anzahl der eingefügten Header ist relevant, da sie durch tune.http.maxhdr begrenzt wird. Wird das optionale Präfix angegeben, werden aus der kodierten Zeichenfolge nur die Header gesetzt, die mit `<str>` beginnen.

Beispiel:

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request add-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-allow"></a>

**`allow`**

```haproxy
allow
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies beendet die Regelauswertung und lässt die Anfrage die Prüfung passieren. Diese Aktion ist abschließend, d. h. für den aktuellen Abschnitt werden keine weiteren Regeln desselben Regelsatzes ausgewertet. Sie unterscheidet sich von der Aktion "accept" nur dadurch, dass aus Gründen historischer Kompatibilität "accept" für TCP-Regeln und "allow" für HTTP-Regeln verwendet wird. Siehe auch die Aktion "accept" weiter oben.

<a id="entry-4-4-attach-srv"></a>

**`attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]`**

```haproxy
attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| X \| - \| -
\| - \| - \| -

Damit wird die Verbindung nach dem ordnungsgemäßen Aufbau von HTTP/2 abgefangen. Die Verbindung wird auf die Backend-Seite umgekehrt und in den Pool ungenutzter Verbindungen des Servers `<srv>` aufgenommen. Dies kann nur mit Servern verwendet werden, deren Adresse mit 'rhttp@' angegeben ist.

Die Verbindung wird unter einem Namen in den Pool ungenutzter Serververbindungen aufgenommen, der sich aus der Auswertung von `<expr>` ergibt. Mit diesem Namen werden Anfragen abgeglichen, für die der Parameter "pool-conn-name" oder "sni" gilt. Weitere Einzelheiten finden Sie unter "http-reuse".

Reverse HTTP wird derzeit noch aktiv entwickelt. Der Konfigurationsmechanismus kann sich künftig ändern. Deshalb ist er intern als experimentell gekennzeichnet, was bedeutet, dass "expose-experimental-directives" in einer Zeile vor dieser Direktive stehen muss.

Beachten Sie, dass ein sehr ähnliches, aber unabhängiges Protokoll entwickelt wird. Siehe
<https://www.ietf.org/archive/id/draft-bt-httpbis-reverse-http-00.html>.

<a id="entry-4-4-auth"></a>

**`auth [realm <realm>]`**

```haproxy
auth [realm <realm>]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies beendet die Regelauswertung und antwortet sofort mit dem HTTP-Fehlercode 401 oder 407, um den Benutzer zur Angabe eines gültigen Benutzernamens und Passworts aufzufordern. Es werden keine weiteren "http-request"-Regeln ausgewertet. Der optionale Parameter "realm" wird unterstützt. Er legt den mit der Antwort zurückgegebenen Authentifizierungsbereich fest, üblicherweise den Namen der Anwendung.

Es wird die Fehlermeldung des jeweiligen Proxys verwendet. Sie kann mit einer Direktive "errorfile" oder "http-error" angepasst werden. Bei Antworten mit dem Status 401 werden alle Vorkommen des Headers WWW-Authenticate entfernt und durch einen neuen Header mit einer Aufforderung zur Basisauthentifizierung für den Bereich "`<realm>`" ersetzt. Bei Antworten mit dem Status 407 geschieht dasselbe mit dem Header Proxy-Authenticate. Wenn die Fehlermeldung nicht verändert werden darf, ziehen Sie stattdessen eine Regel "http-request return" in Betracht.

Beispiel:

```text
acl auth_ok http_auth_group(L1) G1
http-request auth unless auth_ok

```

<a id="entry-4-4-cache-store"></a>

**`cache-store <name>`**

```haproxy
cache-store <name>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| -

Speichert eine http-response im Cache. Die Antwort-Header werden in diesem Schritt gespeichert. Sie können also andere http-response-Aktionen verwenden, um Header vor oder nach dem Speichern der Antwort zu ändern. Diese Aktion richtet den Filter zum Speichern im Cache ein.

Siehe [Abschnitt 6.2](/de/haproxy/cache/#section-6-2) zur Einrichtung des Caches.

<a id="entry-4-4-cache-use"></a>

**`cache-use <name>`**

```haproxy
cache-use <name>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Versucht, ein zwischengespeichertes Objekt aus dem Cache `<name>` auszuliefern. Diese Direktive ist auch für das Speichern im Cache zwingend erforderlich, da sie den Cache-Hash berechnet. Wenn Sie eine Bedingung sowohl für das Speichern als auch für das Ausliefern verwenden möchten, empfiehlt es sich, sie nach dieser Direktive anzugeben.

Siehe [Abschnitt 6.2](/de/haproxy/cache/#section-6-2) zur Einrichtung des Caches.

<a id="entry-4-4-capture"></a>

**`capture <sample> [ len <length> | id <id> ]`**

```haproxy
capture <sample> [ len <length> | id <id> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| X \| X

Dies erfasst den Sample-Ausdruck `<sample>` aus dem Anfrage- oder Antwortpuffer und wandelt ihn in eine Zeichenfolge mit höchstens `<len>` Zeichen um. Die resultierende Zeichenfolge wird im nächsten "capture"-Slot für Anfragen bzw. Antworten gespeichert und kann somit neben erfassten HTTP-Headern erscheinen. Sie erscheint anschließend automatisch in den Protokollen und kann mit Sample-Abrufmethoden ausgelesen werden, um sie in Header oder andere Elemente einzufügen. Die Länge sollte begrenzt werden, da diese Größe für jede Erfassung während der gesamten Lebensdauer des Streams reserviert wird. Beachten Sie, dass die Länge nur mit "http-request"-Regeln verwendet werden kann.  Ein solcher Slot existiert nur in dem Abschnitt, der ihn deklariert. Wird diese Regel daher in einem "listen"-Abschnitt platziert, der zugleich als Backend eines anderen Frontends dient, wird sie für Streams von diesem Frontend ignoriert. Weitere Informationen finden Sie in [Abschnitt 7.3](/de/haproxy/acls-and-samples/#section-7-3) (Abrufen von Samples), unter "capture request header" und unter "capture response header".

Wird statt "len" das Schlüsselwort "id" verwendet, versucht die Aktion, die erfasste Zeichenfolge in einem zuvor deklarierten Erfassungsslot zu speichern. Dies ist nützlich, um Erfassungen in Backends durchzuführen. Die Slot-ID kann mit einer vorherigen Direktive "http-request capture" oder mit dem Schlüsselwort "declare capture" deklariert werden.

Wenn Sie diese Aktion in einem Backend verwenden, vergewissern Sie sich, dass die zugehörigen Frontends über die erforderlichen Erfassungsslots verfügen. Andernfalls wird diese Regel zur Laufzeit ignoriert. Da HAProxy Backend-Namen dynamisch zur Laufzeit auflösen kann, lässt sich dies beim Parsen der Konfiguration nicht erkennen.

<a id="entry-4-4-close"></a>

**`close`**

```haproxy
close
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| X
\| - \| - \| -

Damit wird die Verbindung zum Server sofort geschlossen. Es werden keine weiteren "tcp-response content"-Regeln ausgewertet. Diese Aktion dient hauptsächlich dazu, nach einem Austausch das Ende einer Verbindung zwischen Client und Server zu erzwingen, wenn das Anwendungsprotokoll zunächst den Ablauf langer Wartefristen vorsieht. Ziel ist es, ungenutzte Verbindungen zu beseitigen, die bei bestimmten Protokollen erhebliche Serverressourcen belegen.

<a id="entry-4-4-del-acl"></a>

**`del-acl(<file-name>) <key fmt>`**

```haproxy
del-acl(<file-name>) <key fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Damit wird ein Eintrag aus einer ACL gelöscht. Die ACL muss aus einer Datei geladen werden, auch wenn diese nur eine leere Platzhalterdatei ist. Der Dateiname der zu aktualisierenden ACL wird in Klammern angegeben. Die Aktion nimmt ein Argument entgegen: `<key fmt>`, das den Regeln für benutzerdefinierte Protokollformate in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) folgt, um den Inhalt des zu löschenden Eintrags zu ermitteln. Dies entspricht dem Befehl "del acl" am Statistik-Socket, kann jedoch durch eine HTTP-Anfrage oder -Antwort ausgelöst werden.

<a id="entry-4-4-del-header"></a>

**`del-header <name> [ -m <meth> ]`**

```haproxy
del-header <name> [ -m <meth> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies entfernt alle HTTP-Header-Felder mit dem in `<name>` angegebenen Namen. `<meth>` bezeichnet die auf den Header-Namen angewendete Abgleichmethode. Unterstützt werden "str" (exakte Übereinstimmung), "beg" (Präfixübereinstimmung), "end" (Suffixübereinstimmung), "sub" (Übereinstimmung mit einer Teilzeichenfolge) und "reg" (Übereinstimmung mit einem regulären Ausdruck). Wird keine Methode angegeben, wird auf exakte Übereinstimmung geprüft.

<a id="entry-4-4-del-headers-bin"></a>

**`del-headers-bin <expr> [ -m <meth> ]`**

```haproxy
del-headers-bin <expr> [ -m <meth> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies entfernt alle HTTP-Header-Felder, deren Namen in `<expr>` angegeben werden. `<expr>` muss eine binäre Zeichenfolge mit varint-Kodierung zurückgeben, die alle zu löschenden Header-Namen enthält. Eine Beschreibung der Kodierung und Beispiele finden Sie unter "add-headers-bin" und "set-headers-bin". `<meth>` bezeichnet die auf alle Header-Namen angewendete Abgleichmethode. Unterstützt werden "str" (exakte Übereinstimmung), "beg" (Präfixübereinstimmung), "end" (Suffixübereinstimmung) und "sub" (Übereinstimmung mit einer Teilzeichenfolge). "reg" (Übereinstimmung mit einem regulären Ausdruck) wird wegen der nicht vorhersehbaren Leistung zur Laufzeit nicht unterstützt. Wird keine Methode angegeben, wird auf exakte Übereinstimmung geprüft.

<a id="entry-4-4-del-map"></a>

**`del-map(<map-name>) <key fmt>`**

```haproxy
del-map(<map-name>) <key fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Damit wird ein Eintrag aus einer MAP gelöscht. `<map-name>` muss dem in 2.7. beschriebenen Namensformat für Maps und ACLs entsprechen. Der Name der zu aktualisierenden MAP wird in Klammern angegeben. Die Aktion nimmt ein Argument entgegen: `<key fmt>`, das den Regeln für benutzerdefinierte Protokollformate in [Abschnitt
8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) folgt, um den Inhalt des zu löschenden Eintrags zu ermitteln. Sie nimmt ein Argument entgegen: „Dateiname“. Dies entspricht dem Befehl "del map" am Statistik-Socket, kann jedoch durch eine HTTP-Anfrage oder -Antwort ausgelöst werden.

<a id="entry-4-4-deny"></a>

**`deny [ { status | deny_status } <code> ] [ content-type <type> ]`**

```haproxy
deny [ { status | deny_status } <code> ] [ content-type <type> ]
     [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

       file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
     [ hdr `<name>` `<fmt>` ]*

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Dies beendet die Regelauswertung und weist die Anfrage oder Antwort sofort zurück. Standardmäßig wird für Anfragen ein HTTP-Fehler 403 und für Antworten ein Fehler 502 zurückgegeben. Die zurückgegebene Antwort kann jedoch mit derselben Syntax wie bei der Aktion "return" angepasst werden. Einzelheiten finden Sie daher unter "return" weiter unten. Aus Kompatibilitätsgründen wird das Argument "default-errorfiles" impliziert, wenn kein Argument oder nur "deny_status" angegeben wird. Somit ist "deny [deny_status `<status>`]" ein Alias für "deny
[status `<status>`] default-errorfiles". Diese Aktion ist abschließend, d. h. für den aktuellen Abschnitt werden keine weiteren Regeln desselben Regelsatzes ausgewertet. Zur erweiterten Syntax siehe auch die Aktion "return".

<a id="entry-4-4-dgram-drop"></a>

**`dgram-drop`**

```haproxy
dgram-drop
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

Dies ignoriert ohne Rückmeldung den Empfang eines QUIC-Initial-Pakets, der andernfalls zur Instanziierung einer neuen QUIC-Verbindung und zur Ausführung ihres SSL-Handshakes geführt hätte.

<a id="entry-4-4-disable-l7-retry"></a>

**`disable-l7-retry`**

```haproxy
disable-l7-retry
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies deaktiviert jeden Versuch, die Anfrage zu wiederholen, wenn sie aus einem anderen Grund als einem Verbindungsfehler fehlschlägt. So lässt sich beispielsweise sicherstellen, dass POST-Anfragen bei einem Fehler nicht wiederholt werden.

<a id="entry-4-4-do-log"></a>

**`do-log [profile <log_profile>]`**

```haproxy
do-log [profile <log_profile>]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion löst manuell die Ausgabe eines Protokolleintrags auf dem Proxy aus. Dabei werden die Protokollierungsoptionen des Proxys berücksichtigt, einschließlich Formatierungsoptionen wie "log-format". Die während der Transaktionsverarbeitung automatisch vom Proxy erzeugten Protokolleinträge werden dadurch jedoch nicht beeinflusst.

Mit "log-profile" lässt sich für jeden verfügbaren Kontext, in dem die Aktion verwendet werden kann, genau beschreiben, wie der Protokolleintrag ausgegeben werden soll. Dazu dient das Schlüsselwort 'on', gefolgt von einem der Werte 'quic-init', 'tcp-req-conn', 'tcp-req-sess', 'tcp-req-cont', 'tcp-res-cont', 'http-req', 'http-res', 'http-after-res'.

Diese Kontexte werden auch bei Verwendung des Protokollformat-Alias "%OG" korrekt ausgegeben.

Mit dem optionalen Argument "profile" kann der Name eines log-profile-Abschnitts angegeben werden, der speziell für diese do-log-Aktion verwendet werden soll. Er ersetzt das standardmäßig geltende Profil, das dem aktuellen Logger zugeordnet ist.

Beispiel:

```text
log-profile my-dft-prof
  on tcp-req-conn format "Connect: %ci"

log-profile my-local-prof
  on tcp-req-conn format "Local Connect: %ci"

frontend myfront
  log stdout format rfc5424 profile my-dft-prof local0
  log-format "log generated using proxy logformat, from '%OG'"
  acl local src 127.0.0.1
  # on connection use either log-profile from the logger (my-dft-prof) or
  # explicit my-local-prof if source ip is localhost
  tcp-request connection do-log if !local
  tcp-request connection do-log profile my-local-prof if local
  # on content use proxy logformat, since no override was specified
  # in my-dft-prof
  tcp-request content do-log
```

<a id="entry-4-4-do-resolve"></a>

**`do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>`**

```haproxy
do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Diese Aktion führt für das Ergebnis von `<expr>` eine DNS-Auflösung durch und speichert das Ergebnis in der Variablen `<var>`. Sie verwendet den durch `<resolvers>` bezeichneten DNS-resolvers-Abschnitt. Mit den optionalen Argumenten 'ipv4' oder 'ipv6' kann eine bevorzugte Adressfamilie für die Auflösung gewählt werden. Siehe auch das globale Schlüsselwort "dns-accept-family", mit dem die ausschließliche Verwendung einer bestimmten Familie erzwungen werden kann.

Während der DNS-Auflösung pausiert die clientseitige Verbindung und wartet auf deren Abschluss. Wird eine IP-Adresse gefunden, wird sie in `<var>` gespeichert. Tritt ein Fehler beliebiger Art auf, wird `<var>` nicht gesetzt. Mit dieser Aktion lässt sich zur Laufzeit anhand von Informationen aus der Anfrage eine Server-IP-Adresse ermitteln, beispielsweise anhand eines Host-Headers. Wird diese Aktion zum Ermitteln der Server-IP-Adresse verwendet, die mit der Aktion "set-dst" gesetzt wird, muss die Server-IP-Adresse im Backend auf 0.0.0.0 gesetzt sein. Die Aktion do-resolve nimmt einen Parameter entgegen, der nur den Host enthält; jeder Port muss aus der Zeichenfolge entfernt werden.

Beispiel:

```text
resolvers mydns
  nameserver local 127.0.0.53:53
  nameserver google 8.8.8.8:53
  timeout retry   1s
  hold valid 10s
  hold nx 3s
  hold other 3s
  hold obsolete 0s
  accepted_payload_size 8192

frontend fe
  bind 10.42.0.1:80
  http-request do-resolve(txn.myip,mydns,ipv4) hdr(Host),host_only
  http-request capture var(txn.myip) len 40

  # return 503 when the variable is not set,
  # which mean DNS resolution error
  use_backend b_503 unless { var(txn.myip) -m found }

  default_backend be

backend b_503
  # dummy backend used to return 503.
  # one can use the errorfile directive to send a nice
  # 503 error page to end users

backend be
  # rule to prevent HAProxy from reconnecting to services
  # on the local network (forged DNS name used to scan the network)
  http-request deny if { var(txn.myip) -m ip 127.0.0.0/8 10.0.0.0/8 }
  http-request set-dst var(txn.myip)
  server clear 0.0.0.0:0
```

HINWEIS: Vergessen Sie nicht, die Schutzregeln einzurichten, damit HAProxy weder zum Scannen des Netzwerks verwendet wird noch, schlimmer noch, sich selbst in einer Schleife aufruft …

<a id="entry-4-4-early-hint"></a>

**`early-hint <name> <fmt>`**

```haproxy
early-hint <name> <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Damit wird vor jeder anderen Antwort eine HTTP-Antwort 103 Early Hints erstellt. Der Antwort wird ein HTTP-Header-Feld angehängt, dessen Name in `<name>` und dessen Wert durch `<fmt>` festgelegt wird. Letzteres folgt den Regeln für benutzerdefinierte Protokollformate (siehe „Benutzerdefiniertes Protokollformat“ in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6)). Dies ist besonders nützlich, um dem Client Link-Header zu übermitteln, mit denen für die Darstellung der HTML-Dokumente benötigte Ressourcen vorab geladen werden können.

Weitere Informationen finden Sie in RFC 8297.

<a id="entry-4-4-expect-netscaler-cip-layer4"></a>

**`expect-netscaler-cip layer4`**

```haproxy
expect-netscaler-cip layer4
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

Dies konfiguriert die dem Client zugewandte Verbindung so, dass sie einen Header des NetScaler Client IP insertion protocol empfängt, bevor auch nur ein Byte vom Socket gelesen wird. Dies entspricht dem Schlüsselwort "accept-netscaler-cip" in der "bind"-Zeile. Mit der TCP-Regel kann das PROXY-Protokoll jedoch anhand einer ACL nur für bestimmte IP-Adressbereiche akzeptiert werden. Dies ist praktisch, wenn Datenverkehr von öffentlichen Hosts mehrere Ebenen von Load-Balancern durchläuft.

<a id="entry-4-4-expect-proxy-layer4"></a>

**`expect-proxy layer4`**

```haproxy
expect-proxy layer4
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

Dies konfiguriert die dem Client zugewandte Verbindung so, dass sie einen Header des PROXY-Protokolls empfängt, bevor auch nur ein Byte vom Socket gelesen wird. Dies entspricht dem Schlüsselwort "accept-proxy" in der "bind"-Zeile. Mit der TCP-Regel kann das PROXY-Protokoll jedoch anhand einer ACL nur für bestimmte IP-Adressbereiche akzeptiert werden. Dies ist praktisch, wenn Datenverkehr von öffentlichen Hosts mehrere Ebenen von Load-Balancern durchläuft.

<a id="entry-4-4-normalize-uri"></a>

**`normalize-uri <normalizer>`**

```haproxy
normalize-uri <normalizer>
normalize-uri fragment-encode
normalize-uri fragment-strip
normalize-uri path-merge-slashes
normalize-uri path-strip-dot
normalize-uri path-strip-dotdot [ full ]
normalize-uri percent-decode-unreserved [ strict ]
normalize-uri percent-to-uppercase [ strict ]
normalize-uri query-sort-by-name
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Normalisiert die URI der Anfrage.

Die URI-Normalisierung ist in HAProxy 2.4 derzeit als experimentelle technische Vorschau verfügbar. Daher muss zuerst die globale Direktive 'expose-experimental-directives' angegeben werden, damit sie aufgerufen werden kann. Sie sollten darauf vorbereitet sein, dass sich das Verhalten der Normalisierer zur Behebung möglicher Probleme ändern und dadurch möglicherweise die korrekte Anfrageverarbeitung in Ihrer Infrastruktur beeinträchtigen kann.

Jeder Normalisierer behandelt genau eine Art der Normalisierung. So lässt sich der für das unterstützte Backend geeignete Normalisierungsumfang gezielt auswählen.

Beispielsweise kann der Normalisierer "path-strip-dotdot" für einen statischen Dateiserver nützlich sein, der die angeforderte URI direkt auf den Pfad im lokalen Dateisystem abbildet. Er kann jedoch das Routing einer API beeinträchtigen, die eine bestimmte Anzahl von Pfadsegmenten erwartet.

Beachten Sie, dass einige Normalisierer bei fehlerhaften URIs zu unsicheren Umwandlungen führen können. Auch eine ungeeignete Kombination von Normalisierern, die für sich genommen sicher sind, kann zu unsicheren Umwandlungen führen.

Beispielsweise kann der Normalisierer "percent-decode-unreserved" unerwartete Ergebnisse liefern, wenn eine fehlerhafte URI einzelne Prozentzeichen enthält. Eine solche fehlerhafte URI ist "/%%36%36": Sie würde zu "/%66" dekodiert, was wiederum "/f" entspricht. Mit der Option "strict" werden Anfragen für eine solche fehlerhafte URI sicher zurückgewiesen.

Folgende Normalisierer sind verfügbar:

- fragment-encode: Kodiert "#" als "%23".

  Der Normalisierer "fragment-strip" sollte bevorzugt werden, sofern nicht bekannt ist, dass fehlerhafte Clients '#' innerhalb der Pfadkomponente nicht korrekt kodieren.

  Beispiel:

  - /#foo -\> /%23foo

- fragment-strip: Entfernt die "fragment"-Komponente der URI.

  Gemäß RFC 3986#3.5 sollte die "fragment"-Komponente einer URI nicht gesendet, sondern nach dem Abrufen einer Ressource vom Benutzeragenten verarbeitet werden.

  Dieser Normalisierer sollte zuerst angewendet werden, damit das Fragment nicht als Teil der Pfadkomponente der Anfrage interpretiert wird.

  Beispiel:

  - /#foo -\> /

- path-strip-dot: Entfernt "/./"-Segmente innerhalb der "path"-Komponente (RFC 3986#6.2.2.3).

  Segmente mit prozentkodierten Punkten ("%2E") werden nicht erkannt. Falls dies unerwünscht ist, verwenden Sie zuerst den Normalisierer "percent-decode-unreserved".

  Beispiel:

  - /. -\> /
  - /./bar/ -\> /bar/
  - /a/./a -\> /a/a
  - /.well-known/ -\> /.well-known/ (unverändert)

- path-strip-dotdot: Normalisiert "/../"-Segmente innerhalb der "path"-Komponente (RFC 3986#6.2.2.3).

  Dabei werden Segmente, die auf das übergeordnete Verzeichnis zugreifen wollen, mit ihrem jeweils vorhergehenden Segment zusammengeführt.

  Leere Segmente werden nicht gesondert behandelt. Falls dies unerwünscht ist, verwenden Sie zuerst den Normalisierer "merge-slashes".

  Segmente mit prozentkodierten Punkten ("%2E") werden nicht erkannt. Falls dies unerwünscht ist, verwenden Sie zuerst den Normalisierer "percent-decode-unreserved".

  Beispiel:

  - /foo/../ -\> /
  - /foo/../bar/ -\> /bar/
  - /foo/bar/../ -\> /foo/
  - /../bar/ -\> /../bar/
  - /bar/../../ -\> /../
  - /foo//../ -\> /foo/
  - /foo/%2E%2E/ -\> /foo/%2E%2E/

  Wenn die Option "full" angegeben ist, wird auch ein führendes "../" entfernt:

  Beispiel:

  - /../bar/ -\> /bar/
  - /bar/../../ -\> /

- path-merge-slashes: Führt benachbarte Schrägstriche innerhalb der "path"-Komponente zu einem einzigen Schrägstrich zusammen.

  Beispiel:

  - // -\> /
  - /foo//bar -\> /foo/bar

- percent-decode-unreserved: Dekodiert nicht reservierte, prozentkodierte Zeichen zu ihrer Darstellung als gewöhnliche Zeichen (RFC 3986#6.2.2.2).

  Zu den nicht reservierten Zeichen gehören alle Buchstaben, alle Ziffern, "-", ".", "\_" und "~".

  Beispiel:

  - /%61dmin -\> /admin
  - /foo%3Fbar=baz -\> /foo%3Fbar=baz (unverändert)
  - /%%36%36 -\> /%66 (unsicher)
  - /%ZZ -\> /%ZZ

  Wenn die Option "strict" angegeben ist, führen ungültige Sequenzen zur Rückgabe von HTTP 400 Bad Request.

  Beispiel:

  - /%%36%36 -\> HTTP 400
  - /%ZZ -\> HTTP 400

- percent-to-uppercase: Wandelt Buchstaben innerhalb prozentkodierter Sequenzen in Großbuchstaben um (RFC 3986#6.2.2.1).

  Beispiel:

  - /%6f -\> /%6F
  - /%zz -\> /%zz

  Wenn die Option "strict" angegeben ist, führen ungültige Sequenzen zur Rückgabe von HTTP 400 Bad Request.

  Beispiel:

  - /%zz -\> HTTP 400

- query-sort-by-name: Sortiert die Parameter der Abfragezeichenfolge nach Parameternamen. Dabei wird angenommen, dass die Parameter durch '&' getrennt sind. Kürzere Namen werden vor längeren einsortiert; Parameter mit identischem Namen behalten ihre relative Reihenfolge bei.

  Beispiel:

  - /?c=3&a=1&b=2 -\> /?a=1&b=2&c=3
  - /?aaa=3&a=1&aa=2 -\> /?a=1&aa=2&aaa=3
  - /?a=3&b=4&a=1&b=5&a=2 -\> /?a=3&a=1&a=2&b=4&b=5

<a id="entry-4-4-pause"></a>

**`pause { <timeout> | <expr> }`**

```haproxy
pause { <timeout> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Dies setzt die Nachrichtenanalyse für die angegebene Anzahl von Millisekunden aus. Die Wartezeit kann in Millisekunden oder in einer anderen Einheit angegeben werden, wenn der Zahl wie zu Beginn dieses Dokuments beschrieben die Einheit angehängt wird. Auch ein Ausdruck kann angegeben werden; er muss eine Zahl zurückgeben, die als Wartezeit in Millisekunden interpretiert wird. Schlägt die Auswertung des Ausdrucks fehl oder liefert sie einen ungültigen Wert, wird die Aktion ignoriert und die Auswertung fortgesetzt.

Diese Aktion kann zur Fehlersuche verwendet werden. Sie kann aber auch dazu dienen, bestimmte Clients anhand bestimmter Kriterien zu verlangsamen. Beispielsweise können Clients bei zu hoher Anfragerate verlangsamt werden, indem sie mit einer "track-sc"-Regel verfolgt werden.

<a id="entry-4-4-redirect"></a>

**`redirect <rule>`**

```haproxy
redirect <rule>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Dies führt anhand einer Weiterleitungsregel eine HTTP-Weiterleitung durch. Die Aktion entspricht genau der Anweisung "redirect", fügt jedoch eine Weiterleitungsregel ein, die inmitten anderer "http-request"- oder "http-response"-Regeln verarbeitet wird. Außerdem verwenden diese Regeln das benutzerdefinierte Protokollformat. Bei Antworten sind nur Weiterleitungen vom Typ "location" zulässig. Wird während einer Antwort eine Weiterleitung ausgeführt, wird zudem die Übertragung vom Server an HAProxy unterbrochen, sodass keine Nutzdaten an den Client weitergeleitet werden können. Bei HTTP/1 kann dies dazu führen, dass einige Verbindungen geschlossen werden. Diese Aktion ist abschließend, d. h. für den aktuellen Abschnitt werden keine weiteren Regeln desselben Regelsatzes ausgewertet. Die Regelsyntax finden Sie beim Schlüsselwort "redirect".

<a id="entry-4-4-reject"></a>

**`reject`**

```haproxy
reject
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| - \| -

Dies beendet die Regelauswertung und schließt die Verbindung sofort, ohne eine Antwort zu senden. Bei HTTP-Regeln verhält sich die Aktion ähnlich wie "tcp-request content reject"-Regeln. Sie kann nützlich sein, um das sofortige Schließen von HTTP/2-Verbindungen zu erzwingen.

Bei "tcp-request connection"-Regeln werden zurückgewiesene Verbindungen nicht einmal zu einer Sitzung. Deshalb werden sie in den Statistiken separat als "denied connections" gezählt. Sie werden weder bei der Ratenbegrenzung für Sitzungen berücksichtigt noch protokolliert. Der Grund dafür ist, dass diese Regeln nur zum Filtern extrem hoher Verbindungsraten verwendet werden sollten, wie sie bei einem massiven DDoS-Angriff auftreten. Unter solch extremen Bedingungen würde bereits das Protokollieren jedes Ereignisses das System zusammenbrechen lassen und die Filterkapazität erheblich verringern. Wenn die Protokollierung unbedingt gewünscht ist, sollten stattdessen "tcp-request content"-Regeln verwendet werden, da auch "tcp-request session"-Regeln nichts protokollieren.

Bei Verwendung in "tcp-response content"-Regeln wird die Serververbindung geschlossen und die Antwort abgebrochen. Dies wird im Allgemeinen eingesetzt, um die Offenlegung vertraulicher Informationen zu verhindern, typischerweise nach einer Inhaltsprüfung zusammen mit der Aktion "wait-for-body".

Diese Aktion kann auch in "quic-initial"-Regeln verwendet werden. Die neu geöffnete QUIC-Verbindung wird sofort geschlossen, ohne den SSL-Handshake zu verarbeiten. Der Client wird mit dem Fehlercode CONNECTION_REFUSED benachrichtigt.

<a id="entry-4-4-replace-header"></a>

**`replace-header <name> <match-regex> <replace-fmt>`**

```haproxy
replace-header <name> <match-regex> <replace-fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies gleicht den Wert aller Vorkommen des Header-Felds `<name>` mit `<match-regex>` ab. Der Abgleich unterscheidet Groß- und Kleinschreibung. Übereinstimmende Werte werden vollständig durch `<replace-fmt>` ersetzt. In `<replace-fmt>` sind Formatzeichen zulässig; sie funktionieren wie die `<fmt>`-Argumente in "http-request
add-header". Übliche Rückverweise mit einem Backslash ('&#92;'), gefolgt von einer Zahl, werden unterstützt.

Diese Aktion arbeitet auf vollständigen Header-Zeilen, unabhängig von der Anzahl der darin enthaltenen Werte. Sie eignet sich daher gut für Header, deren Wert von Natur aus Kommas enthält, etwa If-Modified-Since oder Set-Cookie. Header mit einer kommagetrennten Werteliste, etwa Accept oder Cache-Control, sollten stattdessen mit der Aktion "replace-value" verarbeitet werden. Siehe auch die Aktion "replace-value".

Beispiel:

```shell
http-request replace-header Cookie foo=([^;]*);(.*) foo=\1;ip=%bi;\2

# applied to:
Cookie: foo=foobar; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# outputs:
Cookie: foo=foobar;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# assuming the backend IP is 192.168.1.20

http-request replace-header User-Agent curl foo

# applied to:
User-Agent: curl/7.47.0

# outputs:
User-Agent: foo
```

Beispiel:

```shell
http-response replace-header Set-Cookie (C=[^;]*);(.*) \1;ip=%bi;\2

# applied to:
Set-Cookie: C=1; expires=Tue, 14-Jun-2016 01:40:45 GMT

# outputs:
Set-Cookie: C=1;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT

# assuming the backend IP is 192.168.1.20.

```

<a id="entry-4-4-replace-path"></a>

**`replace-path <match-regex> <replace-fmt>`**

```haproxy
replace-path <match-regex> <replace-fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies funktioniert wie "replace-header", arbeitet jedoch auf der Pfadkomponente der Anfrage statt auf einem Header. Die Pfadkomponente beginnt am ersten '/' nach einer optionalen Kombination aus Schema und Authority und endet vor dem Fragezeichen. Die Ersetzung ändert daher weder das Schema noch die Authority oder die Abfragezeichenfolge.

Beachten Sie, dass die Auswertung regulärer Ausdrücke aufwendiger sein kann als die bestimmter ACLs. Bei seltenen Ersetzungen kann daher eine Bedingung sinnvoll sein, um die Auswertung vollständig zu vermeiden, wenn die Bedingung nicht zutrifft.

Beispiel:

```shell
# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-path (.*) /foo\1

# strip /foo: turn /foo/bar?q=1 into /bar?q=1
http-request replace-path /foo/(.*) /\1
# or more efficient if only some requests match:
http-request replace-path /foo/(.*) /\1 if { url_beg /foo/ }

```

<a id="entry-4-4-replace-pathq"></a>

**`replace-pathq <match-regex> <replace-fmt>`**

```haproxy
replace-pathq <match-regex> <replace-fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies bewirkt dasselbe wie "http-request replace-path", wobei der Pfad jedoch eine gegebenenfalls vorhandene Abfragezeichenfolge einschließt. Somit werden sowohl der Pfad als auch die Abfragezeichenfolge ersetzt.

Beispiel:

```shell
# suffix /foo: turn /bar?q=1 into /bar/foo?q=1:
http-request replace-pathq ([^?]*)(\?(.*))? \1/foo\2

```

<a id="entry-4-4-replace-uri"></a>

**`replace-uri <match-regex> <replace-fmt>`**

```haproxy
replace-uri <match-regex> <replace-fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies funktioniert wie "replace-header", arbeitet jedoch auf dem URI-Teil der Anfrage statt auf einem Header. Der URI-Teil kann optional ein Schema, eine Authority oder eine Abfragezeichenfolge enthalten. Diese gelten als Teil des Werts, mit dem der Abgleich erfolgt.

Beachten Sie, dass die Auswertung regulärer Ausdrücke aufwendiger sein kann als die bestimmter ACLs. Bei seltenen Ersetzungen kann daher eine Bedingung sinnvoll sein, um die Auswertung vollständig zu vermeiden, wenn die Bedingung nicht zutrifft.

WICHTIGER HINWEIS: Historisch verwendet bei HTTP/1.x die überwiegende Mehrheit der von Browsern gesendeten Anfragen die "origin form". Diese unterscheidet sich von der "absolute form" dadurch, dass ihr URI-Teil weder ein Schema noch eine Authority enthält. Meist verwenden nur an Proxys gesendete Anfragen, von Hand erstellte Anfragen und einige von bestimmten Anwendungen erzeugte Anfragen die absolute Form. Deshalb funktioniert "replace-uri" bei HTTP/1.x mit Regeln, die mit "/" beginnen, normalerweise problemlos. Bei HTTP/2 wird Clients jedoch nahegelegt, ausschließlich absolute URIs zu senden, die denen ähneln, mit denen HTTP/1-Clients Proxys ansprechen. Solche partiellen replace-uri-Regeln können dann unter HTTP/2 fehlschlagen, obwohl sie unter HTTP/1 funktionieren. Entweder müssen die Regeln so angepasst werden, dass sie optional auch ein Schema und eine Authority erfassen, oder es sollte replace-path verwendet werden.

Beispiel:

```shell
# rewrite all "http" absolute requests to "https":
http-request replace-uri ^http://(.*) https://\1

# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-uri ([^/:]*://[^/]*)?(.*) \1/foo\2

```

<a id="entry-4-4-replace-value"></a>

**`replace-value <name> <match-regex> <replace-fmt>`**

```haproxy
replace-value <name> <match-regex> <replace-fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies funktioniert wie "replace-header", gleicht den regulären Ausdruck jedoch mit jedem kommagetrennten Wert des Header-Felds `<name>` ab, statt mit dem gesamten Header. Dies eignet sich für alle Header, die mehrere Werte enthalten dürfen. Beispiele sind der Anfrage-Header Accept oder Cache-Control in Anfragen und Antworten.

Beispiel:

```shell
http-request replace-value X-Forwarded-For ^192\.168\.(.*)$ 172.16.\1

# applied to:
X-Forwarded-For: 192.168.10.1, 192.168.13.24, 10.0.0.37

# outputs:
X-Forwarded-For: 172.16.10.1, 172.16.13.24, 10.0.0.37
```

Beispiel:

```shell
http-after-response replace-value Cache-control ^public$ private

# applied to:
Cache-Control: max-age=3600, public

# outputs:
Cache-Control: max-age=3600, private

```

<a id="entry-4-4-return"></a>

**`return [ status <code> ] [ content-type <type> ]`**

```haproxy
return [ status <code> ] [ content-type <type> ]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

         file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Dies beendet die Regelauswertung und gibt sofort eine Antwort zurück. Der standardmäßige Statuscode der Antwort ist 200. Er kann optional als Argument von "status" angegeben werden. Der Inhaltstyp der Antwort kann ebenfalls als Argument von "content-type" angegeben werden. Schließlich kann auch die Antwort selbst definiert werden: als vollständige HTTP-Antwort durch Angabe der zu verwendenden Fehlerdatei oder als Antwortnutzdaten durch Angabe der zu verwendenden Datei oder Zeichenfolge. Die Antwort wird nach folgenden Regeln erstellt:

- Wenn weder eine Fehlerdatei noch zu verwendende Nutzdaten definiert sind, wird eine leere Platzhalterantwort zurückgegeben. Nur das Argument "status" wird berücksichtigt. Es kann ein beliebiger Code im Bereich [200, 599] sein. Ein gegebenenfalls vorhandenes Argument "content-type" wird ignoriert.

- Wenn das Argument "default-errorfiles" gesetzt ist, werden die Fehlerdateien des Proxys berücksichtigt. Wird das Argument "status" definiert, muss es einer der von HAProxy unterstützten Statuscodes sein (200, 400, 403, 404, 405, 408, 410, 413, 414, 425, 429, 431, 500, 501, 502, 503 und 504). Ein gegebenenfalls vorhandenes Argument "content-type" wird ignoriert.

- Wenn mit dem Argument "errorfile" eine bestimmte Fehlerdatei definiert ist, wird die entsprechende Datei zurückgegeben, die eine vollständige HTTP-Antwort enthält. Nur das Argument "status" wird berücksichtigt. Es muss einer der von HAProxy unterstützten Statuscodes sein (200, 400, 403, 404, 405, 408, 410, 413, 414, 425, 429, 431, 500, 501, 502, 503 und 504). Ein gegebenenfalls vorhandenes Argument "content-type" wird ignoriert.

- Wenn mit dem Argument "errorfiles" ein http-errors-Abschnitt definiert ist, wird die entsprechende Datei aus dem angegebenen http-errors-Abschnitt zurückgegeben, die eine vollständige HTTP-Antwort enthält. Nur das Argument "status" wird berücksichtigt. Es muss einer der von HAProxy unterstützten Statuscodes sein (200, 400, 403, 404, 405, 408, 410, 413, 414, 425, 429, 431, 500, 501, 502, 503 und 504). Ein gegebenenfalls vorhandenes Argument "content-type" wird ignoriert.

- Wenn das Argument "file" oder "lf-file" angegeben wird, wird der Dateiinhalt als Antwortnutzdaten verwendet. Ist die Datei nicht leer, muss ihr Inhaltstyp als Argument von "content-type" gesetzt werden. Andernfalls wird jedes Argument "content-type" ignoriert. Bei "lf-file" wird der Dateiinhalt als benutzerdefiniertes Protokollformat ausgewertet (siehe [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6)). Bei "file" wird er als unverarbeiteter Inhalt behandelt.

- Wenn das Argument "string" oder "lf-string" angegeben wird, wird die definierte Zeichenfolge als Antwortnutzdaten verwendet. Der Inhaltstyp muss stets als Argument von "content-type" gesetzt werden. Bei "lf-string" wird die Zeichenfolge als benutzerdefiniertes Protokollformat ausgewertet (siehe [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6)). Bei "string" wird sie als unverarbeitete Zeichenfolge behandelt.

Wenn die Antwort nicht auf einer Fehlerdatei beruht, können mit "hdr"-Argumenten HTTP-Header-Felder an die Antwort angehängt werden. Andernfalls werden alle "hdr"-Argumente ignoriert. Für jeden Header wird der Name in `<name>` und der Wert durch `<fmt>` festgelegt. Letzteres folgt den in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschriebenen Regeln für benutzerdefinierte Protokollformate.

Beachten Sie, dass die erzeugte Antwort kleiner als ein Puffer sein muss. Um Warnungen zu vermeiden, sollte beim Laden einer Fehlerdatei oder einer unverarbeiteten Datei außerdem der für das Umschreiben von Headern reservierte Pufferbereich frei bleiben.

Diese Aktion ist abschließend, d. h. für den aktuellen Abschnitt werden keine weiteren Regeln desselben Regelsatzes ausgewertet.

Beispiel:

```text
http-request return errorfile /etc/haproxy/errorfiles/200.http \
    if { path /ping }

http-request return content-type image/x-icon file /var/www/favicon.ico  \
    if { path /favicon.ico }

http-request return status 403 content-type text/plain    \
    lf-string "Access denied. IP %[src] is blacklisted."  \
    if { src -f /etc/haproxy/blacklist.lst }

```

<a id="entry-4-4-sc-add-gpc"></a>

**`sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion erhöht den allgemeinen Zähler am Index `<idx>` des Arrays, das dem mit `<sc-id>` bezeichneten Sitzungsbindungszähler zugeordnet ist. Der Erhöhungswert stammt entweder aus der Ganzzahl `<int>` oder aus dem als Ganzzahl ausgewerteten Ausdruck `<expr>`. Ganzzahlen und Ausdrücke sind auf vorzeichenlose 32-Bit-Werte begrenzt. Tritt ein Fehler auf, schlägt die Aktion ohne Meldung fehl und die Auswertung der Aktionen wird fortgesetzt. `<idx>` ist eine Ganzzahl zwischen 0 und 99, `<sc-id>` eine Ganzzahl zwischen 0 und 2. Auch wenn an diesem Index kein GPC gespeichert ist, schlägt die Aktion ohne Meldung fehl. Der Tabelleneintrag wird selbst dann aufgefrischt, wenn der Wert null ist. 'gpc_rate' wird automatisch angepasst, um die durchschnittliche Wachstumsrate des gpc-Werts widerzuspiegeln.

Diese Aktion gilt nur für die Array-Datentypen 'gpc' und 'gpc_rate', nicht für die älteren Datentypen 'gpc0', 'gpc1', 'gpc0_rate' oder 'gpc1_rate'. Für die älteren Datentypen gibt es keine entsprechende Funktion. Wenn der Wert jedoch immer 1 ist, siehe 'sc-inc-gpc()', 'sc-inc-gpc0()' und 'sc-inc-gpc1()'. Auch ein Verringern des Werts ist nicht möglich. Stattdessen können jedoch mit 'sc-set-gpt()' genaue Werte in einem allgemeinen Tag gespeichert werden.

Diese Aktion dient hauptsächlich dazu, Bewertungen oder Gesamtmengen zu zählen, etwa die vom Server oder von einer WAF gemeldete geschätzte Gefährlichkeit pro Quell-IP oder die insgesamt hochgeladenen Bytes.

<a id="entry-4-4-sc-inc-gpc"></a>

**`sc-inc-gpc(<idx>,<sc-id>)`**

```haproxy
sc-inc-gpc(<idx>,<sc-id>)
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion erhöht den allgemeinen Zähler am Index `<idx>` des Arrays, das dem mit `<sc-id>` bezeichneten Sitzungsbindungszähler zugeordnet ist. Tritt ein Fehler auf, schlägt die Aktion ohne Meldung fehl und die Auswertung der Aktionen wird fortgesetzt. `<idx>` ist eine Ganzzahl zwischen 0 und 99, `<sc-id>` eine Ganzzahl zwischen 0 und 2. Auch wenn an diesem Index kein GPC gespeichert ist, schlägt die Aktion ohne Meldung fehl. Diese Aktion gilt nur für die Array-Datentypen 'gpc' und 'gpc_rate', nicht für die älteren Datentypen 'gpc0', 'gpc1', 'gpc0_rate' oder 'gpc1_rate'.

<a id="entry-4-4-sc-inc-gpc0"></a>

**`sc-inc-gpc0(<sc-id>)`**

```haproxy
sc-inc-gpc0(<sc-id>)
sc-inc-gpc1(<sc-id>)
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion erhöht den Zähler GPC0 oder GPC1 entsprechend dem mit `<sc-id>` bezeichneten Sitzungsbindungszähler. Tritt ein Fehler auf, schlägt die Aktion ohne Meldung fehl und die Auswertung der Aktionen wird fortgesetzt.

<a id="entry-4-4-sc-set-gpt"></a>

**`sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion setzt das vorzeichenlose 32-Bit-GPT am Index `<idx>` des Arrays, das dem mit `<sc-id>` bezeichneten Sitzungsbindungszähler zugeordnet ist, auf den Wert von `<int>`/`<expr>`. Das erwartete Ergebnis ist ein boolescher Wert.

Tritt ein Fehler auf, schlägt die Aktion ohne Meldung fehl und die Auswertung der Aktionen wird fortgesetzt. `<idx>` ist eine Ganzzahl zwischen 0 und 99, `<sc-id>` eine Ganzzahl zwischen 0 und 2. Auch wenn an diesem Index kein GPT gespeichert ist, schlägt die Aktion ohne Meldung fehl.

Diese Aktion gilt nur für den Array-Datentyp 'gpt', nicht für den älteren Datentyp 'gpt0'.

<a id="entry-4-4-sc-set-gpt0"></a>

**`sc-set-gpt0(<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt0(<sc-id>) { <int> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Diese Aktion setzt das vorzeichenlose 32-Bit-Tag GPT0 entsprechend dem mit `<sc-id>` bezeichneten Sitzungsbindungszähler und dem Wert von `<int>`/`<expr>`. Das erwartete Ergebnis ist ein boolescher Wert. Tritt ein Fehler auf, schlägt die Aktion ohne Meldung fehl und die Auswertung der Aktionen wird fortgesetzt. Diese Aktion ist ein Alias für "sc-set-gpt(0,`<sc-id>`)". Siehe auch die Aktion "sc-set-gpt".

<a id="entry-4-4-send-retry"></a>

**`send-retry`**

```haproxy
send-retry
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

Diese Aktion erzwingt das Senden eines Retry-Pakets als Antwort auf ein Initial-Paket eines Clients ohne Token. Dies ist nützlich, um sicherzustellen, dass die Clientadresse validiert wird, bevor Verbindungselemente instanziiert werden und der Handshake beginnt.

<a id="entry-4-4-send-spoe-group"></a>

**`send-spoe-group <engine-name> <group-name>`**

```haproxy
send-spoe-group <engine-name> <group-name>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Mit dieser Aktion wird das Senden einer Gruppe von SPOE-Nachrichten ausgelöst. Dazu müssen sowohl die zum Senden verwendete SPOE-Engine als auch die zu sendende SPOE-Gruppe definiert sein. Die SPOE-Engine muss selbstverständlich auf einen vorhandenen SPOE-Filter verweisen. Ist in der SPOE-Filterzeile kein Engine-Name angegeben, muss der Name des SPOE-Agenten verwendet werden.

Argumente:

```text
<engine-name>  Der Name der SPOE-Engine.

<group-name>   Der Name der SPOE-Gruppe, wie in der Engine-Konfiguration
               angegeben.

```

<a id="entry-4-4-set-bandwidth-limit"></a>

**`set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]`**

```haproxy
set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Mit dieser Aktion wird der Filter `<name>` zur Bandbreitenbegrenzung aktiviert, je nach Filtertyp für Uploads oder Downloads. Eine individuelle Grenze und ein individueller Zeitraum können genau dann definiert werden, wenn `<name>` auf einen Filter zur Bandbreitenbegrenzung pro Stream verweist. Bei der Ausführung einer set-bandwidth-limit-Regel werden zunächst alle Einstellungen des Filters auf ihre Standardwerte zurückgesetzt, bevor er aktiviert wird. Werden mehrere "set-bandwidth-limit"-Aktionen für denselben Filter ausgeführt, wird deshalb nur die letzte berücksichtigt. Für denselben Stream können mehrere Filter zur Bandbreitenbegrenzung aktiviert werden.

Beachten Sie, dass diese Aktion nicht in einem defaults-Abschnitt verwendet werden kann, weil Filter zur Bandbreitenbegrenzung nicht in defaults-Abschnitten definiert werden können. Außerdem wird nur die Übertragung der HTTP-Nutzdaten begrenzt. Die HTTP-Header werden nicht berücksichtigt.

Argumente:

```text
<expr>  ist ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
        gefolgt von Konvertern. Das Ergebnis wird in eine ganze Zahl
        umgewandelt. Für den Parameter "limit" wird es als Größe in Byte,
        für den Parameter "period" als Dauer in Millisekunden interpretiert.

<size>  ist eine Zahl im HAProxy-Größenformat, angegeben in Byte.

<time>  ist eine Zahl im HAProxy-Zeitformat, angegeben in Millisekunden.
```

Beispiel:

```text
http-request set-bandwidth-limit global-limit
http-request set-bandwidth-limit my-limit limit 1m period 10s
```

Siehe [Abschnitt 9.7](/de/haproxy/filters/#section-9-7) zur Einrichtung von Filtern zur Bandbreitenbegrenzung.

<a id="entry-4-4-set-bc-mark"></a>

**`set-bc-mark { <mark> | <expr> }`**

```haproxy
set-bc-mark { <mark> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Damit wird auf unterstützten Plattformen der Netfilter/IPFW MARK für die Backend-Verbindung, also für alle an den Server gesendeten Pakete, auf den in `<mark>` oder `<expr>` übergebenen Wert gesetzt. Dies ist ein vorzeichenloser 32-Bit-Wert, der von netfilter/ipfw und der Routingtabelle oder bei der Paketüberwachung mit DTrace abgeglichen werden kann. `<mark>` kann dezimal oder hexadezimal mit dem Präfix "0x" angegeben werden. Alternativ kann `<expr>` verwendet werden: ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf und nachfolgenden Konvertern, der einen Ganzzahltyp ergeben muss. Diese Aktion kann nützlich sein, um bestimmte Pakete auf eine andere Route zu zwingen, etwa einen günstigeren Netzwerkpfad für große Downloads. Dies funktioniert ab Linux-Kernel 2.6.32 und erfordert Administratorrechte; es funktioniert außerdem unter FreeBSD und OpenBSD. Die Markierung bleibt während der gesamten Backend-/Serververbindung gesetzt, vom Verbindungsaufbau bis zum Schließen.

<a id="entry-4-4-set-bc-tos"></a>

**`set-bc-tos { <tos> | <expr> }`**

```haproxy
set-bc-tos { <tos> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Damit wird auf unterstützten Plattformen der Wert des TOS- oder DSCP-Felds für die Backend-Verbindung, also für alle an den Server gesendeten Pakete, auf den in `<tos>` oder `<expr>` übergebenen Wert gesetzt. Dieser Wert umfasst sämtliche 8 Bits des IP-TOS-Felds. Beachten Sie, dass bei DSCP oder TOS nur die oberen 6 Bits verwendet werden und die beiden unteren Bits immer 0 sind. Alternativ kann `<expr>` verwendet werden: ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf und nachfolgenden Konvertern, der einen Ganzzahltyp ergeben muss. Mit dieser Aktion lässt sich das Routingverhalten interner Router anhand von Informationen aus der Anfrage anpassen. Der tos-Wert bleibt während der gesamten Backend-/Serververbindung gesetzt, vom Verbindungsaufbau bis zum Schließen.

Weitere Informationen finden Sie in RFC 2474, 2597, 3260 und 4594.

<a id="entry-4-4-set-dst"></a>

**`set-dst <expr>`**

```haproxy
set-dst <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Damit wird die Ziel-IP-Adresse auf den Wert des angegebenen Ausdrucks gesetzt. Dies ist nützlich, wenn ein HAProxy vorgeschalteter Proxy die Ziel-IP umschreibt, die korrekte IP jedoch in einem HTTP-Header bereitstellt, oder wenn Sie die IP aus Datenschutzgründen verbergen möchten. Wenn Sie eine Verbindung mit der neuen Adresse bzw. dem neuen Port herstellen möchten, verwenden Sie im Backend '0.0.0.0:0' als Serveradresse.

Argumente:

```text
<expr>  ist ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
        gefolgt von Konvertern.
```

Beispiel:

```text
http-request set-dst hdr(x-dst)
http-request set-dst dst,ipmask(24)
```

Wenn möglich, behält set-dst den ursprünglichen Zielport bei, sofern die Adressfamilie dies zulässt. Andernfalls wird der Zielport auf 0 gesetzt.

<a id="entry-4-4-set-dst-port"></a>

**`set-dst-port <expr>`**

```haproxy
set-dst-port <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Damit wird der Zielport auf den Wert des angegebenen Ausdrucks gesetzt. Wenn Sie eine Verbindung mit der neuen Adresse bzw. dem neuen Port herstellen möchten, verwenden Sie im Backend '0.0.0.0:0' als Serveradresse.

Argumente:

```text
<expr>  ist ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
        gefolgt von Konvertern.
```

Beispiel:

```text
http-request set-dst-port hdr(x-port)
http-request set-dst-port int(4000)
```

Wenn möglich, behält set-dst-port die ursprüngliche Zieladresse bei, sofern die Adressfamilie einen Port unterstützt. Andernfalls setzt es die Zieladresse vor dem Umschreiben des Ports auf die IPv4-Adresse "0.0.0.0".

<a id="entry-4-4-set-fc-mark"></a>

**`set-fc-mark { <mark> | <expr> }`**

```haproxy
set-fc-mark { <mark> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Damit wird auf unterstützten Plattformen der Netfilter/IPFW MARK für alle an den Client gesendeten Pakete auf den in `<mark>` oder `<expr>` übergebenen Wert gesetzt. Dies ist ein vorzeichenloser 32-Bit-Wert, der von netfilter/ipfw und der Routingtabelle oder bei der Paketüberwachung mit DTrace abgeglichen werden kann. `<mark>` kann dezimal oder hexadezimal mit dem Präfix "0x" angegeben werden. Alternativ kann `<expr>` verwendet werden: ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf und nachfolgenden Konvertern, der einen Ganzzahltyp ergeben muss. Diese Aktion kann nützlich sein, um bestimmte Pakete auf eine andere Route zu zwingen, etwa einen günstigeren Netzwerkpfad für große Downloads. Dies funktioniert ab Linux-Kernel 2.6.32 und erfordert Administratorrechte; es funktioniert außerdem unter FreeBSD und OpenBSD.

<a id="entry-4-4-set-fc-tos"></a>

**`set-fc-tos { <tos | <expr> }`**

```haproxy
set-fc-tos { <tos | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Damit wird auf unterstützten Plattformen der Wert des TOS- oder DSCP-Felds für an den Client gesendete Pakete auf den in `<tos>` oder `<expr>` übergebenen Wert gesetzt. Dieser Wert umfasst sämtliche 8 Bits des IP-TOS-Felds. Beachten Sie, dass bei DSCP oder TOS nur die oberen 6 Bits verwendet werden und die beiden unteren Bits immer 0 sind. Alternativ kann `<expr>` verwendet werden: ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf und nachfolgenden Konvertern, der einen Ganzzahltyp ergeben muss. Mit dieser Aktion lässt sich das Routingverhalten von Grenzroutern anhand von Informationen aus der Anfrage anpassen.

Weitere Informationen finden Sie in RFC 2474, 2597, 3260 und 4594.

<a id="entry-4-4-set-header"></a>

**`set-header <name> <fmt>`**

```haproxy
set-header <name> <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies bewirkt dasselbe wie die Aktion "add-header", entfernt jedoch zuerst den Header, falls er bereits vorhanden ist. Dies ist nützlich, wenn Sicherheitsinformationen an den Server übergeben werden und der Header nicht von externen Benutzern manipuliert werden darf, oder um bestimmte Antwort-Header wie "Server" zu erzwingen und damit externe Informationen zu verbergen. Beachten Sie, dass der neue Wert vor dem Entfernen berechnet wird. So kann ein Wert an einen vorhandenen Header angehängt werden.

Beispiel:

```text
http-request set-header X-Haproxy-Current-Date %T
http-request set-header X-SSL                  %[ssl_fc]
http-request set-header X-SSL-Session_ID       %[ssl_fc_session_id,hex]
http-request set-header X-SSL-Client-Verify    %[ssl_c_verify]
http-request set-header X-SSL-Client-DN        %{+Q}[ssl_c_s_dn]
http-request set-header X-SSL-Client-CN        %{+Q}[ssl_c_s_dn(cn)]
http-request set-header X-SSL-Issuer           %{+Q}[ssl_c_i_dn]
http-request set-header X-SSL-Client-NotBefore %{+Q}[ssl_c_notbefore]
http-request set-header X-SSL-Client-NotAfter  %{+Q}[ssl_c_notafter]
```

<a id="entry-4-4-set-headers-bin"></a>

**`set-headers-bin <expr> [ prefix <str> ]`**

```haproxy
set-headers-bin <expr> [ prefix <str> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies ist eine Variante der Aktion "set-header", bei der die Header-Namen und -Werte als binäre Zeichenfolge mit varint-Kodierung übergeben werden. Informationen zum varint-Format finden Sie beim Sample-Abruf "req.hdrs_bin". Dies ist nützlich, wenn mehrere Header gleichzeitig gesetzt werden sollen, ohne ihre Namen im Voraus kennen zu müssen. Beachten Sie, dass diese Header nicht vom HTTP-Parser validiert wurden. Dadurch können ungültige Nachrichten ausgegeben werden; im schlimmsten Fall kann dies Request-Smuggling-Angriffe ermöglichen. Auch die Anzahl der eingefügten Header ist relevant, da sie durch tune.http.maxhdr begrenzt wird. Wird das optionale Präfix angegeben, werden aus der kodierten Zeichenfolge nur die Header gesetzt, die mit `<str>` beginnen.

Beispiel:

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request set-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-set-log-level"></a>

**`set-log-level <level>`**

```haproxy
set-log-level <level>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| X

Damit wird die Protokollierungsstufe der aktuellen Anfrage geändert, wenn eine bestimmte Bedingung erfüllt ist. Gültige Stufen sind die 8 syslog-Stufen (siehe Schlüsselwort "log") sowie die besondere Stufe "silent", die die Protokollierung für diese Anfrage deaktiviert. Diese Regel ist nicht abschließend; die letzte passende Regel hat daher Vorrang. Sie kann nützlich sein, um Health Checks von anderen Geräten auszublenden.

<a id="entry-4-4-set-map"></a>

**`set-map(<map-name>) <key fmt> <value fmt>`**

```haproxy
set-map(<map-name>) <key fmt> <value fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Damit wird einer Map ein neuer Eintrag hinzugefügt. `<map-name>` muss dem in 2.7. beschriebenen Namensformat für Maps und ACLs entsprechen. Der Name der zu aktualisierenden MAP wird in Klammern angegeben. Die Aktion nimmt 2 Argumente entgegen: `<key fmt>` folgt den in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6) beschriebenen Regeln für benutzerdefinierte Protokollformate und dient zum Ermitteln des Map-Schlüssels. `<value fmt>` folgt ebenfalls den Regeln für benutzerdefinierte Protokollformate und dient zum Ermitteln des Inhalts für den neuen Eintrag. Vor dem Einfügen wird die Map durchsucht, um doppelte oder mehrfach vorhandene Werte zu vermeiden. Dies entspricht dem Befehl "set map" am Statistik-Socket, kann jedoch durch eine HTTP-Anfrage ausgelöst werden.

<a id="entry-4-4-set-mark"></a>

**`set-mark <mark> (deprecated)`**

```haproxy
set-mark <mark> (deprecated)
```

Dies ist ein Alias für "set-fc-mark", das stattdessen verwendet werden sollte.

<a id="entry-4-4-set-method"></a>

**`set-method <fmt>`**

```haproxy
set-method <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies überschreibt die Anfragemethode mit dem Ergebnis der Auswertung der Formatzeichenfolge `<fmt>`. Dafür sollte es nur sehr wenige triftige Gründe geben, da dies eher etwas beschädigt als etwas behebt.

<a id="entry-4-4-set-nice"></a>

**`set-nice <nice>`**

```haproxy
set-nice <nice>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Dies setzt den "nice"-Faktor der gerade verarbeiteten Anfrage oder Antwort. Er wirkt sich nur im Verhältnis zu anderen gleichzeitig verarbeiteten Anfragen aus. Der Standardwert ist 0, sofern er nicht durch die Einstellung "nice" in der "bind"-Zeile geändert wird. Der zulässige Bereich ist -1024..1024. Je höher der Wert, desto mehr Vorrang lässt die Anfrage anderen. Niedrigere Werte machen die Anfrage wichtiger als andere. Dies kann nützlich sein, um bestimmte Anfragen zu beschleunigen oder die Priorität unwichtiger Anfragen zu senken. Eine Verwendung dieser Einstellung ohne vorherige Erprobung kann erhebliche Verlangsamungen verursachen.

<a id="entry-4-4-set-path"></a>

**`set-path <fmt>`**

```haproxy
set-path <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

    Dies überschreibt den Anfragepfad mit dem Ergebnis der Auswertung der
    Formatzeichenfolge `<fmt>`. Eine vorhandene Abfragezeichenfolge bleibt
    unverändert. Stehen vor dem Pfad ein Schema und eine Authority, bleiben
    auch diese unverändert. Hat die Anfrage keinen Pfad ("*"), wird dieser
    durch das Format ersetzt. Damit kann beispielsweise einem Pfad eine
    Verzeichniskomponente vorangestellt werden. Siehe auch
    "http-request set-query" und "http-request set-uri".

Beispiel:

```shell
# prepend the host name before the path
http-request set-path /%[hdr(host)]%[path]

```

<a id="entry-4-4-set-pathq"></a>

**`set-pathq <fmt>`**

```haproxy
set-pathq <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies bewirkt dasselbe wie "http-request set-path", schreibt jedoch auch die Abfragezeichenfolge um. Damit kann die Abfragezeichenfolge einschließlich des Fragezeichens entfernt werden; mit "http-request set-query" ist dies nicht möglich.

<a id="entry-4-4-set-priority-class"></a>

**`set-priority-class <expr>`**

```haproxy
set-priority-class <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Damit wird die Prioritätsklasse der aktuellen Anfrage in der Warteschlange gesetzt. Der Wert muss ein Sample-Ausdruck sein, der sich in eine Ganzzahl im Bereich -2047..2047 umwandeln lässt. Ergebnisse außerhalb dieses Bereichs werden auf dessen Grenzen beschränkt. Die Prioritätsklasse bestimmt die Reihenfolge, in der wartende Anfragen verarbeitet werden. Niedrigere Werte haben eine höhere Priorität.

<a id="entry-4-4-set-priority-offset"></a>

**`set-priority-offset <expr>`**

```haproxy
set-priority-offset <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Damit wird der Zeitstempelversatz für die Warteschlangenpriorität der aktuellen Anfrage gesetzt. Der Wert muss ein Sample-Ausdruck sein, der sich in eine Ganzzahl im Bereich -524287..524287 umwandeln lässt. Ergebnisse außerhalb dieses Bereichs werden auf dessen Grenzen beschränkt. Wird eine Anfrage in die Warteschlange aufgenommen, erfolgt ihre Einordnung zuerst nach der Prioritätsklasse und dann nach dem aktuellen Zeitstempel, korrigiert um den angegebenen Versatz in Millisekunden. Niedrigere Werte haben eine höhere Priorität. Beachten Sie, dass der resultierende Zeitstempel nur mit ausreichender Genauigkeit für 524,287ms (8m44s287ms) erfasst wird. Bleibt die Anfrage so lange in der Warteschlange, dass der korrigierte Zeitstempel diesen Wert überschreitet, wird sie fälschlich als Anfrage mit höchster Priorität erkannt. Daher ist es wichtig, "timeout queue" so zu wählen, dass der Wert zusammen mit dem Versatz diese Grenze nicht überschreitet.

<a id="entry-4-4-set-query"></a>

**`set-query <fmt>`**

```haproxy
set-query <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies überschreibt die Abfragezeichenfolge der Anfrage nach dem ersten Fragezeichen ("?") mit dem Ergebnis der Auswertung der Formatzeichenfolge `<fmt>`. Der Teil vor dem Fragezeichen bleibt unverändert. Enthält die Anfrage kein Fragezeichen und ist der neue Wert nicht leer, wird am Ende der URI ein Fragezeichen angefügt, gefolgt vom neuen Wert. War bereits ein Fragezeichen vorhanden, wird es niemals entfernt, auch nicht bei einem leeren Wert. Damit können Parameter zur Abfragezeichenfolge hinzugefügt oder daraus entfernt werden.

Siehe auch "http-request set-query" und "http-request set-uri".

Beispiel:

```shell
# replace "%3D" with "=" in the query string
http-request set-query %[query,regsub(%3D,=,g)]

```

<a id="entry-4-4-set-retries"></a>

**`set-retries <int> | <epxr>`**

```haproxy
set-retries <int> | <epxr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Diese Aktion überschreibt den angegebenen Wert "retries" nur für den aktuellen Stream. Er kann eine Ganzzahl im Bereich [0, 100] oder ein Ausdruck sein, der eine Ganzzahl im Bereich [0, 100] zurückgeben muss.

Beachten Sie, dass diese Aktion nur auf der Backend-Seite relevant ist und die Regel daher nur für Proxys mit Backend-Funktion verfügbar ist. In "defaults"-Abschnitten ist sie ebenfalls nicht zulässig. Wird die Aktion für einen Listener verwendet, wird sie im Frontend-Kontext ausgewertet. Der retries-Wert bleibt daher nur erhalten, wenn der Stream nicht zu einem anderen Backend geleitet wird, etwa durch eine use-backend-Regel. Andernfalls wird der standardmäßige retries-Wert des ausgewählten Backends voreingestellt.

Beispiel:

```text
tcp-request content set-retries 3
http-request set-retries var(txn.retries)
```

<a id="entry-4-4-set-src"></a>

**`set-src <expr>`**

```haproxy
set-src <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Damit wird die Quell-IP-Adresse auf den Wert des angegebenen Ausdrucks gesetzt. Dies ist nützlich, wenn ein HAProxy vorgeschalteter Proxy die Quell-IP umschreibt, die korrekte IP jedoch in einem HTTP-Header bereitstellt, oder wenn Sie die Quell-IP aus Datenschutzgründen verbergen möchten. Alle nachfolgenden Aufrufe des Abrufs "src" geben diesen Wert zurück (siehe Beispiel).

Argumente:

```text
<expr>  ist ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
        gefolgt von Konvertern.
```

Siehe auch "option forwardfor".

Beispiel:

```shell
http-request set-src hdr(x-forwarded-for)
http-request set-src src,ipmask(24)

# After the masking this will track connections
# based on the IP address with the last byte zeroed out.
http-request track-sc0 src
```

Wenn möglich, behält set-src den ursprünglichen Quellport bei, sofern die Adressfamilie dies zulässt. Andernfalls wird der Quellport auf 0 gesetzt.

<a id="entry-4-4-set-src-port"></a>

**`set-src-port <expr>`**

```haproxy
set-src-port <expr>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Damit wird der Quellport auf den Wert des angegebenen Ausdrucks gesetzt.

Argumente:

```text
<expr>  ist ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
        gefolgt von Konvertern.
```

Beispiel:

```text
http-request set-src-port hdr(x-port)
http-request set-src-port int(4000)
```

Wenn möglich, behält set-src-port die ursprüngliche Quelladresse bei, sofern die Adressfamilie einen Port unterstützt. Andernfalls setzt es die Quelladresse vor dem Umschreiben des Ports auf die IPv4-Adresse "0.0.0.0".

<a id="entry-4-4-set-status"></a>

**`set-status <status> [reason <str>]`**

```haproxy
set-status <status> [reason <str>]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| X

Dies ersetzt den Statuscode der Antwort durch `<status>`, der eine Ganzzahl zwischen 100 und 999 sein muss. Optional kann mit `<str>` ein individueller Begründungstext angegeben werden. Andernfalls wird ersatzweise die Standardbegründung für den angegebenen Code verwendet. Beachten Sie, dass die Begründungszeichenfolge nur in HTTP/1.x existiert und von anderen Protokollversionen ignoriert wird.

Beispiel:

```shell
# return "431 Request Header Fields Too Large"
http-response set-status 431
# return "503 Slow Down", custom reason
http-response set-status 503 reason "Slow Down".

```

<a id="entry-4-4-set-timeout"></a>

**`set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }`**

```haproxy
set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Diese Aktion überschreibt die angegebene Wartezeit "client", "connect", "queue", "server", "tarpit" oder "tunnel" nur für den aktuellen Stream. Das Ändern einer Wartezeit beeinflusst keine anderen Wartezeiten, auch wenn sie beim Parsen der Konfiguration voneinander geerbt werden (siehe letztes Beispiel). Die Wartezeit kann in Millisekunden oder in einer anderen Einheit angegeben werden, wenn der Zahl wie zu Beginn dieses Dokuments beschrieben die Einheit angehängt wird. Auch ein Ausdruck kann angegeben werden; er muss eine Zahl zurückgeben, die als Wartezeit in Millisekunden interpretiert wird.

Beachten Sie, dass die Wartezeiten connect, queue, server und tunnel nur auf der Backend-Seite relevant sind und diese Regel daher nur für Proxys mit Backend-Funktion verfügbar ist. Entsprechend ist die client-Wartezeit nur auf der Frontend-Seite relevant. Die tarpit-Wartezeit ist auf beiden Seiten verfügbar. Der Wartezeitwert muss ungleich null sein, um die erwarteten Ergebnisse zu erzielen. Wird die Aktion für einen Listener verwendet, wird sie im Frontend-Kontext ausgewertet. Individuelle Werte für backendseitige Wartezeiten bleiben daher nur erhalten, wenn der Stream nicht zu einem anderen Backend geleitet wird, etwa durch eine use-backend-Regel. Andernfalls werden die Standardwerte des ausgewählten Backends voreingestellt.

Beispiel:

```text
http-request set-timeout tunnel 5s
http-request set-timeout server req.hdr(host),map_int(host.lst)
```

Beispiel:

```text
http-response set-timeout tunnel 5s
http-response set-timeout server res.hdr(X-Refresh-Seconds),mul(1000)
```

Beispiel:

```text
defaults
  # This will set both tarpit and queue timeout to 5s as they are not
  # defined
  timeout connect 5s
  timeout client 30s
  timeout server 30s

listen foo
  # This will only change the connect timeout to 10s without affecting
  # queue or tarpit timeouts
  http-request set-timeout connect 10s
```

<a id="entry-4-4-set-tos"></a>

**`set-tos <tos> (deprecated)`**

```haproxy
set-tos <tos> (deprecated)
```

Dies ist ein Alias für "set-fc-tos", das stattdessen verwendet werden sollte.

<a id="entry-4-4-set-uri"></a>

**`set-uri <fmt>`**

```haproxy
set-uri <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies überschreibt die Anfrage-URI mit dem Ergebnis der Auswertung der Formatzeichenfolge `<fmt>`. Schema, Authority, Pfad und Abfragezeichenfolge werden gleichzeitig ersetzt. Damit können Hostangaben vor Proxys umgeschrieben oder komplexe Änderungen an der URI vorgenommen werden, etwa das Verschieben von Teilen zwischen Pfad und Abfragezeichenfolge. Wird eine absolute URI gesetzt, wird sie unverändert an HTTP/1.1-Server gesendet. Ist dieses Verhalten nicht erwünscht, sollten Host, Pfad und/oder Abfragezeichenfolge separat gesetzt werden. Siehe auch "http-request set-path" und "http-request set-query".

<a id="entry-4-4-set-var"></a>

**`set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
set-var(<var-name>[,<cond>...]) <expr>
set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Damit wird der Inhalt einer Variablen gesetzt. Die Variable wird direkt an dieser Stelle deklariert.

Argumente:

```text
<var-name>   Der Name der Variablen. Variablen des übergeordneten Streams
             können nicht gesetzt werden. Einzelheiten zu Variablen stehen
             in Abschnitt 2.8.

 <cond>      Eine Menge von Bedingungen, die alle erfüllt sein müssen, damit
             die Variable tatsächlich gesetzt wird (etwa "ifnotempty", "ifgt"
             usw.). Die vollständige Liste möglicher Bedingungen steht in
             der Beschreibung des Konverters set-var.

 <expr>      Ein gewöhnlicher HAProxy-Ausdruck aus einem Sample-Abruf,
             gefolgt von Konvertern.

 <fmt>       Der Wert nach den Regeln für benutzerdefinierte Protokollformate
             (siehe benutzerdefinierte Protokollformate in Abschnitt 8.2.6).
```

Für HTTP-Regeln können alle Geltungsbereiche verwendet werden. In Regelsätzen ohne Zugriff auf Inhalte, etwa "tcp-request connection" und "tcp-request
session", sind jedoch nur die Geltungsbereiche "proc" und "sess" verwendbar.

Beispiel:

```text
http-request set-var(req.my_var) req.fhdr(user-agent),lower
http-request set-var-fmt(txn.from) %[src]:%[src_port]

```

<a id="entry-4-4-silent-drop"></a>

**`silent-drop [ rst-ttl <ttl> ]`**

```haproxy
silent-drop [ rst-ttl <ttl> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Dies beendet die Regelauswertung und lässt die dem Client zugewandte Verbindung plötzlich auf systemabhängige Weise verschwinden, wobei eine Benachrichtigung des Clients möglichst verhindert wird. Beim Aufruf ohne das Argument rst-ttl wird mit TCP_REPAIR versucht, das Zurücksenden von FIN- oder RST-Paketen an den Client zu verhindern. Schlägt dies fehl, hauptsächlich wegen fehlender Berechtigungen, wird ersatzweise ein RST-Paket mit einer TTL von 1 gesendet.

Der Client sieht dadurch weiterhin eine bestehende Verbindung, während auf HAProxy keine mehr vorhanden ist, was Ressourcen spart. Zustandsbehaftete Geräte zwischen HAProxy und dem Client, etwa Firewalls, Proxys oder Load-Balancer, behalten die bestehende Verbindung jedoch ebenfalls in ihren Sitzungstabellen.

Das optionale rst-ttl ändert dieses Verhalten: TCP_REPAIR wird nicht verwendet, und es wird ein RST-Paket mit einer konfigurierbaren TTL gesendet. Bei einem sinnvollen Wert durchläuft das RST-Paket die lokale Infrastruktur und löscht die Verbindung in Firewalls und anderen Systemen, verschwindet jedoch, bevor es den Client erreicht. Zukünftige Pakete des Clients werden dann bereits von vorgeschalteten Geräten verworfen. Diese lokalen RSTs schützen lokale Ressourcen, aber nicht die des Clients. Dies darf nur verwendet werden, wenn die Folgen vollständig verstanden wurden.

<a id="entry-4-4-strict-mode"></a>

**`strict-mode { on | off }`**

```haproxy
strict-mode { on | off }
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Dies aktiviert oder deaktiviert den strikten Umschreibmodus für nachfolgende Regeln. Zuvor deklarierte Regeln sind davon nicht betroffen. Der Modus gilt nur für Regeln, die Anfragen umschreiben. Ist der strikte Modus aktiviert, löst jeder Fehler beim Umschreiben einen internen Fehler aus. Andernfalls werden solche Fehler ohne Meldung ignoriert. Der strikte Umschreibmodus dient dazu, manche Umschreibungen optional zu machen, während andere durchgeführt werden müssen, damit die Anfrageverarbeitung fortgesetzt werden kann.

Standardmäßig ist der strikte Umschreibmodus aktiviert. Sein Wert wird außerdem zurückgesetzt, wenn die Auswertung eines Regelsatzes endet. Wenn Sie den Modus beispielsweise im Frontend ändern, wird der Standardmodus wiederhergestellt, sobald HAProxy mit der Auswertung der Backend-Regeln beginnt.

<a id="entry-4-4-switch-mode-http"></a>

**`switch-mode http [ proto <name> ]`**

```haproxy
switch-mode http [ proto <name> ]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| - \| - \| -

Mit dieser Aktion wird ein Verbindungs-Upgrade durchgeführt. Derzeit werden nur HTTP-Upgrades unterstützt. Das Protokoll kann optional angegeben werden. Diese Aktion ist nur für Proxys mit Frontend-Funktion verfügbar. Das Verbindungs-Upgrade wird sofort durchgeführt; nachfolgende "tcp-request content"-Regeln werden nicht ausgewertet. Diese Upgrade-Methode sollte der impliziten Methode vorgezogen werden, die sich auf den Backend-Modus stützt. Bei ihrer Verwendung können HTTP-Direktiven ohne Warnung in einem Frontend gesetzt werden. Diese Direktiven werden bedingt ausgewertet, wenn das HTTP-Upgrade durchgeführt wird. Es muss jedoch weiterhin ein HTTP-Backend ausgewählt werden. Das Weiterleiten einer HTTP-Verbindung, mit oder ohne Upgrade, an einen TCP-Server wird weiterhin nicht unterstützt.

Weitere Einzelheiten zu HTTP-Upgrades finden Sie in [Abschnitt 4](/de/haproxy/proxies/) über Proxys.

<a id="entry-4-4-tarpit"></a>

**`tarpit [ { status | deny_status } <code>] [content-type <type>]`**

```haproxy
tarpit [ { status | deny_status } <code>] [content-type <type>]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

           file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies beendet die Regelauswertung und blockiert die Anfrage sofort, ohne zu antworten. Die Dauer wird durch "timeout tarpit" festgelegt oder, wenn dieser Wert nicht gesetzt ist, durch "timeout connect". Ist der Client nach Ablauf dieser Zeit noch verbunden, wird eine Antwort zurückgegeben, damit er keinen Verdacht schöpft, dass er absichtlich aufgehalten wurde. In den Protokollen erscheinen die Flags "PT". Die tarpit-Regel soll Bots während eines Angriffs verlangsamen, wenn deren Anzahl gleichzeitiger Anfragen begrenzt ist. Gegen sehr einfache Bots kann sie äußerst wirksam sein und die Last auf Firewalls gegenüber einer "deny"-Regel deutlich verringern. Gegen „korrekt“ entwickelte Bots kann sie die Lage jedoch verschlimmern, indem sie HAProxy und die vorgeschaltete Firewall zwingt, eine enorme Anzahl gleichzeitiger Verbindungen zu verwalten. Standardmäßig wird ein HTTP-Fehler 500 zurückgegeben. Die Antwort kann jedoch mit derselben Syntax wie bei "http-request return"-Regeln angepasst werden. Einzelheiten finden Sie daher unter "http-request return".

Aus Kompatibilitätsgründen wird das Argument "default-errorfiles" impliziert, wenn kein Argument oder nur "deny_status" angegeben wird. Somit ist "http-request tarpit [deny_status `<status>`]" ein Alias für "http-request tarpit [status `<status>`] default-errorfiles". Es werden keine weiteren "http-request"-Regeln ausgewertet. Siehe auch "http-request return" und "http-request silent-drop".

<a id="entry-4-4-track-sc0"></a>

**`track-sc0 <key> [table <table>]`**

```haproxy
track-sc0 <key> [table <table>]
track-sc1 <key> [table <table>]
track-sc2 <key> [table <table>]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| X \| -

Dies aktiviert die Verfolgung von Sitzungsbindungszählern anhand der aktuellen Anfrage. Diese Regeln beenden weder die Auswertung noch ändern sie die Standardaktion. Die Anzahl der Zähler, die von derselben Verbindung gleichzeitig verfolgt werden können, wird durch die globale Einstellung "tune.stick-counters" festgelegt. Ihr Standardwert ist MAX_SESS_STKCTR, sofern dieser beim Erstellen gesetzt wurde; er wird in haproxy -vv ausgegeben. Dessen Standardwert ist 3, sodass die track-sc-Nummer zwischen 0 und (tune.stick-counters-1) liegt. Die erste ausgeführte Regel "track-sc0" aktiviert die Verfolgung der Zähler der angegebenen Tabelle als ersten Satz. Die erste ausgeführte Regel "track-sc1" aktiviert die Verfolgung der Zähler der angegebenen Tabelle als zweiten Satz. Die erste ausgeführte Regel "track-sc2" aktiviert die Verfolgung der Zähler der angegebenen Tabelle als dritten Satz. Es wird empfohlen, den ersten Zählersatz für Zähler pro Frontend und den zweiten für Zähler pro Backend zu verwenden. Dies ist jedoch lediglich eine Richtlinie; alle Sätze können überall verwendet werden.

Argumente:

```text
<key>   ist zwingend erforderlich und eine Sample-Ausdrucksregel wie in
        Abschnitt 7.3 beschrieben. Sie legt fest, welche Elemente der
        eingehenden Verbindung, Anfrage oder Antwort analysiert, extrahiert
        und kombiniert werden, um den Tabelleneintrag auszuwählen, dessen
        Zähler aktualisiert werden.

<table> ist eine optionale Tabelle, die statt der im aktuellen Proxy
        deklarierten Standard-Stick-Table verwendet wird. Alle Zähler für
        Treffer und Aktualisierungen des Schlüssels werden dann bis zum
        Ende der Sitzung in dieser Tabelle geführt.
```

Sobald eine "track-sc\*"-Regel ausgeführt wird, wird der Schlüssel in der Tabelle gesucht. Wird er nicht gefunden, wird ein Eintrag dafür angelegt. Anschließend wird während der gesamten Lebensdauer der Sitzung ein Zeiger auf diesen Eintrag behalten. Seine Zähler werden so oft wie möglich aktualisiert, nämlich jedes Mal, wenn die Sitzungszähler aktualisiert werden, sowie grundsätzlich beim Ende der Sitzung. Zähler werden nur für Ereignisse aktualisiert, die nach Beginn der Verfolgung eintreten. Eine Ausnahme bilden Verbindungs- und Anfragezähler: Sie werden grundsätzlich aktualisiert, damit sie nützliche Informationen widerspiegeln.

Wenn der Eintrag Zähler für gleichzeitige Verbindungen verfolgt, wird eine Verbindung so lange gezählt, wie der Eintrag verfolgt wird. Während dieser Zeit läuft der Eintrag nicht ab. Das Verfolgen von Zählern bietet gegenüber dem bloßen Prüfen von Schlüsseln auch einen Leistungsvorteil, da für alle ACL-Prüfungen, die davon Gebrauch machen, nur ein Tabellenzugriff erfolgt.

<a id="entry-4-4-unset-var"></a>

**`unset-var(<var-name>)`**

```haproxy
unset-var(<var-name>)
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Damit wird eine Variable zurückgesetzt. Einzelheiten zu `<var-name>` finden Sie bei der Aktion "set-var".

Beispiel:

```text
http-request unset-var(req.my_var)

```

<a id="entry-4-4-use-service"></a>

**`use-service <service-name>`**

```haproxy
use-service <service-name>
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Diese Aktion führt je nach Regelsatz, in dem sie verwendet wird, den konfigurierten TCP- oder HTTP-Dienst aus, um auf die Anfrage zu antworten. Die Regel ist abschließend, d. h. im selben Regelsatz werden keine weiteren Regeln ausgewertet.

Ein Dienst kann eine beliebige gültige Antwort senden oder die Verbindung sofort schließen, ohne eine Antwort zu senden. Bei HTTP-Diensten muss eine gültige Antwort eine gültige HTTP-Antwort sein. Neben nativen Diensten, etwa dem Prometheus-Exporter für HTTP-Dienste, können auch eigene TCP- und HTTP-Dienste in Lua geschrieben werden.

Argumente:

```text
<service-name>  ist zwingend erforderlich und bezeichnet den aufzurufenden Dienst.
```

Beispiel:

```text
http-request use-service prometheus-exporter if { path /metrics }

```

<a id="entry-4-4-wait-for-body-time"></a>

**`wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]`**

```haproxy
wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Dies verzögert die Verarbeitung der Anfrage oder Antwort, bis eine der folgenden Bedingungen eintritt:

- Der vollständige Anfragekörper wurde empfangen; die Verarbeitung wird normal fortgesetzt.
- `<bytes>` Bytes wurden empfangen, wenn das Argument "at-least" angegeben und `<bytes>` ungleich null ist; die Verarbeitung wird normal fortgesetzt.
- Der Anfragepuffer ist voll; die Verarbeitung wird normal fortgesetzt. Die Größe dieses Puffers wird durch die Option "tune.bufsize" bestimmt.
- Die Anfrage wartet seit mehr als `<time>` Millisekunden. In diesem Fall antwortet HAProxy dem Client mit dem Fehler 408 "Request Timeout" und beendet die Verarbeitung der Anfrage. Beachten Sie, dass diese Zeitüberschreitung nicht eintritt, wenn zuvor eine der anderen Bedingungen erfüllt wurde, selbst wenn der vollständige Körper noch nicht empfangen wurde.

Die Option "use-large-buffer" kann gesetzt werden, um einen großen Puffer zuzuweisen, wenn der gewöhnliche Puffer zum Speichern des Nachrichtenkörpers zu klein ist. Dazu muss die globale Option "tune.bufsize.large" definiert sein.

Diese Aktion kann als Ersatz für "option http-buffer-request" verwendet werden.

Argumente:

```text
<time>    ist zwingend erforderlich und die maximale Wartezeit auf den
          Nachrichtenkörper. Sie folgt dem HAProxy-Zeitformat und wird in
          Millisekunden angegeben.

<bytes>   ist optional und die Mindestgröße der Nutzdaten, deren Empfang das
          Warten beendet. Sie folgt dem HAProxy-Größenformat und wird in
          Byte angegeben. Der Standardwert 0 bedeutet keine Begrenzung.
```

Beispiel:

```text
http-request wait-for-body time 1s at-least 1k if METH_POST
```

Siehe auch: "option http-buffer-request" und "tune.bufsize.large"

<a id="entry-4-4-wait-for-handshake"></a>

**`wait-for-handshake`**

```haproxy
wait-for-handshake
```

Verwendbar in: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Dies verzögert die Verarbeitung der Anfrage, bis der SSL-Handshake stattgefunden hat. Dies ist hauptsächlich nützlich, um die Verarbeitung früher Daten so lange aufzuschieben, bis ihre Gültigkeit sichergestellt ist.
