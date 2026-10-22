---
title: "2. HAProxy konfigurieren"
linkTitle: "2. Konfigurationsgrundlagen"
weight: 130
description: "Dateisyntax, Anführungszeichen, Variablen, Bedingungen, Zeit- und Größenformate, Adressen und Beispiele"
icon: fa-solid fa-file-code
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/configuration-basics/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 2"
---

## 2.1. Format der Konfigurationsdatei {#section-2-1}

Die Konfiguration von HAProxy bezieht Parameter aus 3 wesentlichen Quellen:

- den Befehlszeilenargumenten, die immer Vorrang haben
- den Konfigurationsdateien, deren Format hier beschrieben wird
- der Umgebung des laufenden Prozesses, sofern bestimmte Umgebungsvariablen ausdrücklich referenziert werden

Die Konfigurationsdatei verwendet ein recht einfaches hierarchisches Format mit wenigen Grundregeln:

```text
1. Eine Konfigurationsdatei ist eine geordnete Folge von Anweisungen.

2. Eine Anweisung ist eine einzelne nicht leere Zeile bis zum ersten
   ungeschützten "#" (Raute).

3. Eine Zeile besteht aus Tokens oder „Wörtern“, die durch ungeschützte
   Leerzeichen oder Tabulatoren getrennt sind.

4. Das erste Wort oder die erste Wortfolge einer Zeile ist eines der in
   diesem Dokument aufgeführten Schlüsselwörter oder Schlüsselwortfolgen.

5. Alle übrigen Wörter sind Argumente des ersten. Manche sind bekannte,
   hier aufgeführte Schlüsselwörter, andere Werte, Verweise auf andere
   Konfigurationsteile oder Ausdrücke.

6. Bestimmte Schlüsselwörter begrenzen einen Abschnitt, in dem nur ein
   Teil der Schlüsselwörter unterstützt wird.

7. Ein Abschnitt endet am Dateiende oder mit einem besonderen Schlüsselwort,
   das einen neuen Abschnitt beginnt.
```

Mehr ist zum Schreiben eines einfachen, aber zuverlässigen Konfigurationsgenerators nicht nötig. Um jede beliebige Konfiguration zuverlässig auszuwerten oder bestimmte Grenzfälle zu behandeln, reicht dies jedoch nicht aus.

Aus den obigen Regeln ergeben sich zunächst einige Folgerungen. Nach Regel 6 und 7 gelten die Schlüsselwörter zum Definieren eines neuen Abschnitts überall und können in keinem bestimmten Abschnitt eine andere Bedeutung haben. Diese Schlüsselwörter bestehen stets aus einem einzelnen Wort, nicht aus einer Wortfolge. Der nachfolgende Abschnitt wird gewöhnlich mit demselben Namen bezeichnet. So meint „globaler Abschnitt“ den Konfigurationsabschnitt nach dem Schlüsselwort "global". Diese Bezeichnung wird in Fehlermeldungen häufig verwendet, um die zu bearbeitenden Stellen leichter auffindbar zu machen.

Mehrere Abschnittstypen erzeugen ein internes Objekt oder einen Konfigurationsbereich, der von anderen unterscheidbar sein muss. Dafür nehmen sie ein zusätzliches Wort entgegen, das den Namen dieses Abschnitts festlegt. Bei einigen ist der Abschnittsname zwingend erforderlich. So erzeugt "frontend foo" einen neuen Abschnitt des Typs "frontend" mit dem Namen "foo". Ein Name gilt gewöhnlich nur für seinen Abschnittstyp; zwei Abschnitte unterschiedlichen Typs können denselben Namen tragen. Davon wird jedoch abgeraten, da es die Konfigurationsverwaltung erschwert.

Aus Regel 7 folgt unmittelbar, dass beim Einlesen mehrerer Dateien jede davon mit einem neuen Abschnitt beginnen muss und jedes Dateiende einen Abschnitt beendet. Eine Datei kann weder Unterabschnitte enthalten noch einen bestehenden Abschnitt beenden und einen neuen beginnen.

Regel 1 besagt, dass die Reihenfolge wichtig ist. Manche Schlüsselwörter definieren Direktiven, die mehrfach wiederholt werden können, um eine geordnete Folge von Regeln zu bilden. Beispielsweise können mit "tcp-request" Regeln für "accept" und "reject" anhand verschiedener Kriterien abwechselnd angewendet werden. Ein Werkzeug zur Bearbeitung von Konfigurationsdateien muss deshalb beim Ändern einer Datei stets die Reihenfolge innerhalb eines Abschnitts erhalten. Die Reihenfolge der Abschnitte ist gewöhnlich unerheblich. Eine Ausnahme bildet der globale Abschnitt: Er muss vor den anderen stehen, kann aber bei Bedarf wiederholt werden. Außerdem können bestimmten erzeugten Objekten wie Proxys automatisch Kennungen zugewiesen werden, die sich beim Umordnen der Abschnitte ändern. Sie erscheinen beispielsweise in der Statistik. In der folgenden Konfiguration erhält "foo" daher eine kleinere ID als "bar". Werden die beiden Abschnitte vertauscht, kehrt sich dies um:

```text
listen foo
    bind :80

listen bar
    bind :81
```

Ein weiterer wichtiger Punkt: Nach den Regeln 2 und 3 gehören Leerzeilen, Leerzeichen, Tabulatoren und Kommentare nach einem ungeschützten "#" nicht zur Konfiguration, da sie nur als Begrenzungen dienen. Die folgenden Konfigurationen sind daher exakt gleichwertig:

```text
    global#this is the global section
daemon#daemonize
    frontend         foo
mode             http   # or tcp
```

und:

```shell
global
    daemon

# this is the public web frontend
frontend foo
    mode http
```

Üblicherweise wird nur das Schlüsselwort, das einen neuen Abschnitt beginnt, linksbündig angeordnet. Alle anderen Schlüsselwörter werden durch einen Tabulator oder einige vorangestellte Leerzeichen eingerückt. So ist sofort erkennbar, dass sie zu demselben Abschnitt gehören, wie im zweiten Beispiel oben. Kommentare vor einem neuen Abschnitt helfen beim Erkennen des gesuchten Abschnitts. Eine Leerzeile am Abschnittsende erleichtert es ebenfalls, beim Bearbeiten dessen Ende zu finden.

Tabulatoren eignen sich gut zum Einrücken, lassen sich aber schlecht kopieren und einfügen. Werden stattdessen Leerzeichen verwendet, werden nur wenige (2 bis 4) empfohlen. So bleibt die Bearbeitung vor Ort auch mit einfachen Editoren ohne automatische Einrückung handhabbar.

Früher wurden Argumente häufig an festen Tabulatorpositionen ausgerichtet, da die meisten Schlüsselwörter höchstens zwei Argumente annahmen. Für moderne Versionen mit komplexen Ausdrücken eignet sich dies nicht mehr und wird nicht empfohlen.

## 2.2. Anführungszeichen und Maskierung {#section-2-2}

In modernen Konfigurationen benötigen manche Argumente Zeichen, die zuvor ausschließlich als Trennzeichen dienten. HAProxy unterstützt deshalb die Maskierung eines Zeichens mit einem vorangestellten Backslash ('&#92;'), schwaches Quoting mit doppelten Anführungszeichen ("") um einen Textabschnitt und starkes Quoting mit einfachen Anführungszeichen ('') um einen Textabschnitt.

Dies ähnelt dem Vorgehen in verschiedenen Programmiersprachen und besonders dem üblichen Verhalten der Bourne-Shell. Beim Zerlegen der Zeilen in Wörter berücksichtigt der Konfigurationsparser auch Anführungszeichen und Backslashes. So entscheidet er, ob ein Zeichen als Trennzeichen oder als wörtliches Zeichen innerhalb des aktuellen Wortes gilt. Anschließend werden das Maskierungszeichen und die Anführungszeichen entfernt; das verbleibende Wort wird unverändert etwa als Schlüsselwort oder Argument verwendet.

Wird innerhalb eines Wortes ein Backslash benötigt, muss er entweder mit sich selbst maskiert werden, also durch einen doppelten Backslash, oder in einfache Anführungszeichen gesetzt werden.

Außerhalb von Anführungszeichen wird ein Sonderzeichen durch einen vorangestellten Backslash ('&#92;') maskiert:

```text
\    kennzeichnet ein Leerzeichen statt eines Trennzeichens
\#   kennzeichnet eine Raute statt des Beginns eines Kommentars
\\   fügt einen Backslash ein
\'   fügt ein einfaches Anführungszeichen statt eines starken Quoting-Zeichens ein
\"   fügt ein doppeltes Anführungszeichen statt eines schwachen Quoting-Zeichens ein
```

Zusätzlich lassen sich einige nicht druckbare Zeichen mit der üblichen C-Schreibweise einfügen:

```text
\n   fügt einen Zeilenvorschub ein (LF, Zeichen \x0a oder dezimal ASCII 10)
\r   fügt einen Wagenrücklauf ein (CR, Zeichen \x0d oder dezimal ASCII 13)
\t   fügt einen Tabulator ein (Zeichen \x09 oder dezimal ASCII 9)
\xNN fügt das Zeichen mit dem hexadezimalen ASCII-Code NN ein (z. B. \x0a für LF).
```

Für schwaches Quoting wird das zu schützende Zeichen oder die Zeichenfolge in doppelte Anführungszeichen ("") gesetzt. Dadurch werden folgende Interpretationen verhindert:

```text
     Leerzeichen oder Tabulator als Worttrenner
'    einfaches Anführungszeichen als Begrenzer für starkes Quoting
```

```haproxy
#    Raute als Kommentarbeginn
```

Schwaches Quoting ermöglicht die Auswertung von Umgebungsvariablen, denen ein Dollarzeichen ('\$') vorangestellt wird. Außerhalb von Anführungszeichen werden diese nicht ausgewertet. Wird innerhalb doppelter Anführungszeichen ein Dollarzeichen als solches benötigt, muss es mit einem Backslash maskiert werden.

Für starkes Quoting wird das zu schützende Zeichen oder die Zeichenfolge in einfache Anführungszeichen ('') gesetzt. Darin wird nichts interpretiert; dies ist eine wirksame Methode, reguläre Ausdrücke zu schützen.

Die folgende Tabelle zeigt daraus abgeleitet, wie Sonderzeichen in verschiedenen Kontexten eingegeben werden können. Nicht druckbare Zeichen sind durch ihren Namen in spitzen Klammern ersetzt. Manche Zeichen lassen sich nur maskiert darstellen und besitzen innerhalb einfacher Anführungszeichen keine mögliche Darstellung; deshalb fehlen sie dort:

```text
  Zeichen    |  Unquotiert   |  Schwach quotiert           |  Stark quotiert
  -----------+---------------+-----------------------------+-----------------
    <TAB>    |  \<TAB>, \x09 |  "<TAB>", "\<TAB>", "\x09"  |  '<TAB>'
  -----------+---------------+-----------------------------+-----------------
    <LF>     |  \n, \x0a     |  "\n", "\x0a"               |
  -----------+---------------+-----------------------------+-----------------
    <CR>     |  \r, \x0d     |  "\r", "\x0d"               |
  -----------+---------------+-----------------------------+-----------------
    <SPC>    |  \<SPC>, \x20 |  "<SPC>", "\<SPC>", "\x20"  |  '<SPC>'
  -----------+---------------+-----------------------------+-----------------
    "        |  \", \x22     |  "\"", "\x22"               |  '"'
  -----------+---------------+-----------------------------+-----------------
    #        |  \#, \x23     |  "#", "\#", "\x23"          |  '#'
  -----------+---------------+-----------------------------+-----------------
    $        |  $, \$, \x24  |  "\$", "\x24"               |  '$'
  -----------+---------------+-----------------------------+-----------------
    '        |  \', \x27     |  "'", "\'", "\x27"          |
  -----------+---------------+-----------------------------+-----------------
    \        |  \\, \x5c     |  "\\", "\x5c"               |  '\'
  -----------+---------------+-----------------------------+-----------------
```

Beispiel:

```shell
# those are all strictly equivalent:
log-format %{+Q}o\ %t\ %s\ %{-Q}r
log-format "%{+Q}o %t %s %{-Q}r"
log-format '%{+Q}o %t %s %{-Q}r'
log-format "%{+Q}o %t"' %s %{-Q}r'
log-format "%{+Q}o %t"' %s'\ %{-Q}r
```

In einem besonderen Fall kann eine zweite Ebene von Anführungszeichen oder Maskierung nötig sein. Manche Schlüsselwörter nehmen Argumente in runden Klammern entgegen, teilweise durch Kommas getrennt. Meist sind dies Ganzzahlen oder vordefinierte Wörter. Bei beliebigen Zeichenketten kann jedoch eine weitere Maskierungsebene erforderlich sein, um Zeichen des Arguments von dessen Begrenzungszeichen zu unterscheiden. Ein häufiges Beispiel ist der Konverter "regsub". Er nimmt einen regulären Ausdruck als Argument entgegen. Wird darin eine schließende runde Klammer benötigt, muss sie eigene Anführungszeichen erhalten.

Für Anführungszeichen verhält sich der Parser für Schlüsselwortargumente genauso wie der Parser auf oberster Ebene. Lediglich die Escape-Sequenzen &#92;#, &#92;\$ und &#92;xNN werden nicht verarbeitet. Weniger offensichtlich ist, dass die innen verwendeten Begrenzungszeichen zunächst maskiert oder in Anführungszeichen gesetzt werden müssen, damit sie nicht bereits auf der obersten Ebene aufgelöst werden.

Das folgende Beispiel verwendet den Konverter "regsub" mit 3 Argumenten: einem regulären Ausdruck, einer Ersetzungszeichenkette und einer Menge von Flags:

```shell
# replace all occurrences of "foo" with "blah" in the path:
http-request set-path %[path,regsub(foo,blah,g)]
```

Hier waren keine besonderen Anführungszeichen nötig. Soll nun aber sowohl "foo" als auch "bar" durch "blah" ersetzt werden, wird der reguläre Ausdruck "(foo\|bar)" benötigt. Folgendes ist nicht möglich:

```text
http-request set-path %[path,regsub((foo|bar),blah,g)]
```

Denn die Zeichenkette soll so aufgeteilt werden:

```text
    http-request set-path %[path,regsub((foo|bar),blah,g)]
                                       |---------|----|-|
                                 arg1 _/         /    /
                                 arg2 __________/    /
                                 arg3 ______________/
```

Tatsächlich wird jedoch eine Zeichenkette zwischen öffnender und schließender Klammer übergeben, gefolgt von ungültigem Resttext:

```text
    http-request set-path %[path,regsub((foo|bar),blah,g)]
                                       |--------|--------|
                        arg1=(foo|bar _/        /
                    ungültiger Rest   _________/
```

Es scheint naheliegend, die schließende Klammer in Anführungszeichen zu setzen. Allein genügt dies aber nicht: Wie oben beschrieben, verarbeitet der Parser auf oberster Ebene die Anführungszeichen und löst sie vor der Verarbeitung dieses Wortes auf:

```text
http-request set-path %[path,regsub("(foo|bar)",blah,g)]
------------ -------- ----------------------------------
   Wort1       Wort2    Wort3=%[path,regsub((foo|bar),blah,g)]
```

Für den Argumentparser auf der zweiten Ebene hat sich somit nichts geändert: Er sieht weiterhin einen abgeschnittenen regulären Ausdruck als einziges Argument und ungültigen Resttext am Ende. Werden die Anführungszeichen maskiert, gelangen sie unverändert auf die zweite Ebene:

```text
    http-request set-path %[path,regsub(\"(foo|bar)\",blah,g)]
    ------------ -------- ------------------------------------
       Wort1       Wort2    Wort3=%[path,regsub("(foo|bar)",blah,g)]
                                                |---------||----|-|
                                arg1=(foo|bar) _/          /    /
                                    arg2=blah  ___________/    /
                                        arg3=g _______________/
```

Alternativ kann die gesamte Zeichenkette außen in einfache und innen in doppelte Anführungszeichen gesetzt werden, damit die doppelten Anführungszeichen nicht wieder entfernt werden:

```text
    http-request set-path '%[path,regsub("(foo|bar)",blah,g)]'
    ------------ --------  ----------------------------------
       Wort1       Wort2    Wort3=%[path,regsub("(foo|bar)",blah,g)]
                                                |---------||----|-|
                                arg1=(foo|bar) _/          /    /
                                          arg2 ___________/    /
                                          arg3 _______________/
```

Dabei ist zu beachten, dass Begrenzungszeichen innerhalb der übergeordneten Zeichenkette gewöhnliche Zeichen bleiben und keine Trennfunktion mehr haben. Insbesondere gehören Leerzeichen und Tabulatoren neben Kommas zur Zeichenkette. Das folgende Beispiel ist an mehreren Stellen falsch:

```text
    http-request set-path '%[path, regsub("(foo|bar)", blah, g)]'
    ------------ --------  --------------------------------------
       Wort1       Wort2    Wort3=%[path, regsub("(foo|bar)", blah, g)]
                                        |--------|---------||-----|--|
                       Konverter=" regsub" _/        /         /   /
                                    arg1=(foo|bar) _/         /   /
                                     arg2=" blah" ___________/   /
                                        arg3=" g" ______________/
```

Allein die Leerzeichen um die Kommas führen dazu, dass diese Teil des Feldes selbst werden. Der Konverter " regsub" mit führendem Leerzeichen wird daher nicht gefunden und löst einen Fehler aus. Weniger offensichtlich ist, dass die Ersetzungszeichenkette " blah" ein Leerzeichen in die Ausgabe einfügt. Eine gute Faustregel lautet deshalb, niemals unnötige Leerzeichen in Ausdrücke einzufügen.

In regulären Ausdrücken kann das Dollarzeichen ('\$') auftreten oder ein Backslash ('&#92;') in der Ersetzungszeichenkette verwendet werden. Diese Zeichen werden innerhalb doppelter Anführungszeichen ebenfalls verarbeitet. Daher sind einfache Anführungszeichen oder eine doppelte Maskierung vorzuziehen. Beispiel:

```text
    http-request set-path '%[path,regsub("^/(here)(/|$)","my/\1",g)]'
    ------------ --------  -----------------------------------------
       Wort1       Wort2    Wort3=%[path,regsub("^/(here)(/|$)","my/\1",g)]
                                                |-------------| |-----||-|
                              arg1=(here)(/|$) _/               /      /
                                    arg2=my/\1 ________________/      /
                                          arg3 ______________________/
```

Innerhalb einfacher Anführungszeichen sind Backslashes keine Maskierungszeichen. Das gesamte obige Wort ist bereits durch einfache Anführungszeichen vor ihrer Interpretation geschützt. Wäre dagegen der gesamte Ausdruck in doppelte Anführungszeichen gesetzt, würden das Dollarzeichen und die Backslashes bereits auf oberster Ebene aufgelöst und dadurch der Argumentinhalt auf der zweiten Ebene beschädigt.

Da einfache Anführungszeichen innerhalb von starkem Quoting nicht maskiert werden können, müssen sie bei Bedarf im Argument zweimal maskiert oder in Anführungszeichen gesetzt werden. Dafür gibt es mehrere Möglichkeiten:

```text
http-request set-var(txn.foo) str("\\'foo\\'")
http-request set-var(txn.foo) str(\"\'foo\'\")
http-request set-var(txn.foo) str(\\\'foo\\\')
```

Im Zweifelsfall zunächst ganz auf Anführungszeichen verzichten und nur Argumente mit Kommas oder schließenden runden Klammern in einfache oder doppelte Anführungszeichen setzen. Enthält die Zeichenkette ein Dollarzeichen oder einen Backslash, müssen diese Anführungszeichen gegebenenfalls mit einem Backslash maskiert werden. Dies ähnelt der doppelten Maskierung eines an "eval" übergebenen Befehls in einer Bourne-Shell. Für API-Autoren ist es vermutlich am besten, ausnahmslos jedes Argument unabhängig von seinem Inhalt mit maskierten Anführungszeichen zu umgeben. Für Anwender sind Konfigurationen wahrscheinlich besser lesbar, wenn der gesamte Ausdruck in einfachen und jedes Argument in doppelten Anführungszeichen steht.

## 2.3. Umgebungsvariablen {#section-2-3}

Die HAProxy-Konfiguration unterstützt Umgebungsvariablen. Sie werden ausschließlich innerhalb doppelter Anführungszeichen interpretiert und beim Einlesen der Konfiguration expandiert. Variablennamen müssen mit einem Dollarzeichen ("\$") beginnen und können wie in der Bourne-Shell zusätzlich in geschweifte Klammern ("{}") eingeschlossen werden. Sie dürfen alphanumerische Zeichen und Unterstriche ("\_") enthalten, sollten aber nicht mit einer Ziffer beginnen. Enthält eine Variable mehrere durch Leerzeichen getrennte Werte, lässt sie sich in einzelne Argumente expandieren: Dazu die Variable in geschweifte Klammern setzen und vor der schließenden Klammer das Suffix '[\*]' ergänzen. Ein Standardwert für nicht gesetzte Variablen kann nach einem Bindestrich '-' hinter dem Variablennamen angegeben werden. Er ersetzt nur nicht vorhandene Variablen, keine leeren.

Beispiel:

```text
bind "fd@${FD_APP1}"

log "${LOCAL_SYSLOG-127.0.0.1}:514" local0 notice  # send to local server

user "$HAPROXY_USER"
```

Einige Variablen werden von HAProxy definiert und können in der Konfigurationsdatei verwendet werden. Sie sind in der folgenden Tabelle aufgeführt und in vier Kategorien eingeteilt:

- verwendbar: Die Variable ist in der Konfiguration zugänglich. Sie kann direkt aufgelöst
  oder in bedingten Blöcken und Prädikaten zum Aktivieren oder Deaktivieren von
  Konfigurationsfragmenten verwendet werden, wie in [Abschnitt 2.4](/de/haproxy/configuration-basics/#section-2-4)
  „Bedingte Blöcke“ beschrieben.

- veränderbar: Die Variable kann in der Konfiguration mit "setenv"/"unsetenv" neu definiert
  oder entfernt werden.

- aufgelistet: Die Variable erscheint in der Ausgabe des CLI-Befehls "show env", der in
  [Abschnitt 9.3](/de/haproxy/statistics-and-monitoring/#section-9-3) „Unix-Socket-Befehle“ des Verwaltungshandbuchs beschrieben ist.

Daneben gibt es die Unterkategorien „Master“ und „Worker“, die in der folgenden Tabelle mit 'M' bzw. 'W' gekennzeichnet sind. Sie zeigen die Unterschiede zwischen den beiden Prozessen beim Start von HAProxy im Master-Worker-Modus.

- Master: Die Variable ist im Master-Prozess gesetzt und zugänglich. Sie erscheint daher
  in der Ausgabe von "show env" der Master-CLI und kann in bedingten Blöcken oder Direktiven
  spezielle Einstellungen für den Master aktivieren. Siehe die Beispiele in [Abschnitt 2.4](/de/haproxy/configuration-basics/#section-2-4)
  „Bedingte Blöcke“.

- Worker: Die Variable ist im Worker-Prozess gesetzt und zugänglich. Sie erscheint in
  "show env" der Worker-CLI oder in "@1 show env" der Master-CLI und kann ebenfalls
  Bedingungen für Parameter des Worker-Prozesses bilden. Siehe die Beispiele in [Abschnitt 2.4](/de/haproxy/configuration-basics/#section-2-4)
  „Bedingte Blöcke“.

Im eigenständigen Betrieb ohne die Option "-W" und ohne das Schlüsselwort "master-worker" verhält sich der Prozess wie ein Worker. Ausgenommen sind die Variablen "HAPROXY_MASTER_CLI" und "HAPROXY_MWORKER", die dann nicht definiert sind.

Einige Variablen sind als weder verwendbar noch veränderbar gekennzeichnet:

- HAPROXY_CFGFILES
- HAPROXY_MWORKER
- HAPROXY_CLI
- HAPROXY_MASTER_CLI
- HAPROXY_LOCALPEER

Ihre Werte sind beim Einlesen der Konfiguration undefiniert und werden erst später während der Initialisierung gesetzt. Daher wird empfohlen, diese Variablen weder in bedingten Blöcken noch in den Schlüsselwörtern "setenv"/"resetenv"/"unsetenv" des globalen Abschnitts zu referenzieren.

Die folgende Tabelle fasst den Status der Variablen für die verschiedenen Betriebsarten zusammen:

```text
  +---------------------------+---------+------------+-----------+
  |          Variable         | nutzbar |  änderbar  | angezeigt |
  |                           +---------+------------+-----------+
  |                           |  M | W  |   M  |  W  |  M  |  W  |
  +---------------------------+----+----+------+-----+-----+-----+
  | HAPROXY_STARTUP_VERSION   |  X | X  |      |     |  X  |  X  |
  | HAPROXY_BRANCH            |  X | X  |      |     |  X  |  X  |
  | HAPROXY_CFGFILES          |    |    |      |     |  X  |  X  |
  | HAPROXY_MWORKER           |    |    |      |     |  X  |  X  |
  | HAPROXY_CLI               |    |    |      |     |     |  X  |
  | HAPROXY_MASTER_CLI        |    |    |      |     |  X  |     |
  | HAPROXY_LOCALPEER         |    | X  |      |     |     |  X  |
  | HAPROXY_HTTP_LOG_FMT      |    | X  |      |  X  |     |     |
  | HAPROXY_HTTP_CLF_LOG_FMT  |    | X  |      |  X  |     |     |
  | HAPROXY_HTTPS_LOG_FMT     |    | X  |      |  X  |     |     |
  | HAPROXY_TCP_LOG_FMT       |    | X  |      |  X  |     |     |
  | HAPROXY_TCP_CLF_LOG_FMT   |    | X  |      |  X  |     |     |
  | HAPROXY_KEYLOG_FC_LOG_FMT |    | X  |      |  X  |     |     |
  | HAPROXY_KEYLOG_BC_LOG_FMT |    | X  |      |  X  |     |     |
  +---------------------------+----+----+------+-----+-----+-----+
```

Im Einzelnen handelt es sich um folgende Variablen:

- HAPROXY_LOCALPEER: beim Prozessstart definiert; enthält den Namen des lokalen Peers.
  Siehe "-L" im Verwaltungshandbuch.

- HAPROXY_CFGFILES: durch Semikolons getrennte Liste der von HAProxy geladenen
  Konfigurationsdateien. Kann bei der Angabe eines Verzeichnisses nützlich sein.

- HAPROXY_HTTP_LOG_FMT: enthält das HTTP-Standardprotokollformat aus [Abschnitt
  8.2.3](/de/haproxy/configuration-logging/#section-8-2-3) „HTTP-Protokollformat“. Damit lässt sich das Standardformat
  überschreiben, ohne die gesamte ursprüngliche Definition kopieren zu müssen.

- HAPROXY_HTTP_CLF_LOG_FMT: enthält das HTTP-CLF-Standardprotokollformat aus
  [Abschnitt 8.2.3](/de/haproxy/configuration-logging/#section-8-2-3) „HTTP-Protokollformat“. Damit lässt sich das Standardformat
  überschreiben, ohne die gesamte ursprüngliche Definition kopieren zu müssen.

Beispiel:

```shell
# Add the rule that gave the final verdict to the log
log-format "${HAPROXY_TCP_LOG_FMT} lr=%[last_rule_file]:%[last_rule_line]"
```

- HAPROXY_HTTPS_LOG_FMT: wie HAPROXY_HTTP_LOG_FMT, jedoch für das HTTPS-Protokollformat
  aus [Abschnitt 8.2.4](/de/haproxy/configuration-logging/#section-8-2-4) „HTTPS-Protokollformat“.

- HAPROXY_TCP_LOG_FMT: wie HAPROXY_HTTP_LOG_FMT, jedoch für das TCP-Protokollformat aus
  [Abschnitt 8.2.2](/de/haproxy/configuration-logging/#section-8-2-2) „TCP-Protokollformat“.

- HAPROXY_TCP_CLF_LOG_FMT: wie HAPROXY_HTTP_CLF_LOG_FMT, jedoch für das TCP-CLF-Protokollformat
  aus [Abschnitt 8.2.2](/de/haproxy/configuration-logging/#section-8-2-2) „TCP-Protokollformat“.

- HAPROXY_KEYLOG_FC_LOG_FMT: enthält das Keylog-Format für die clientseitige TLS-Verbindung
  des Frontends. Schlüsseleinträge werden durch Zeilenumbrüche getrennt; das Format ist daher
  möglicherweise nicht mit dem verwendeten syslog-Server kompatibel. "tune.ssl.keylog on" ist erforderlich.

- HAPROXY_KEYLOG_BC_LOG_FMT: wie HAPROXY_KEYLOG_FC_LOG_FMT, jedoch für die serverseitige
  TLS-Verbindung des Backends. Schlüsseleinträge werden durch Zeilenumbrüche getrennt; das Format
  ist daher möglicherweise nicht mit dem verwendeten syslog-Server kompatibel. "tune.ssl.keylog on" ist erforderlich.

- HAPROXY_MWORKER: Diese Variable wird im Master-Worker-Modus auf 1 gesetzt.

- HAPROXY_CLI: konfigurierte Listener-Adressen des Statistik-Sockets jedes Prozesses,
  durch Semikolons getrennt.

- HAPROXY_MASTER_CLI: im Master-Worker-Modus die durch Semikolons getrennten
  Listener-Adressen der Master-CLI.

- HAPROXY_STARTUP_VERSION: enthält die beim Start verwendete Version. Im Master-Worker-Modus
  ist dies die Version, mit der der Master gestartet wurde, auch nach Aktualisierung der
  ausführbaren Datei und anschließendem Neuladen.

- HAPROXY_BRANCH: enthält die Version des HAProxy-Zweigs, etwa "2.8", jedoch nicht die
  vollständige Versionsnummer. Dies kann bei einer Migration nützlich sein, wenn Ressourcen
  wie Maps oder Zertifikate in einem Pfad mit der Nummer des Versionszweigs liegen.

Zusätzlich werden einige Pseudovariablen intern aufgelöst und lassen sich wie gewöhnliche Variablen verwenden. Pseudovariablen beginnen immer mit einem Punkt ('.'); nur in ihnen ist ein Punkt zulässig. Derzeit gibt es folgende Pseudovariablen:

- .FILE: Name der gerade eingelesenen Konfigurationsdatei.

- .LINE: Zeilennummer in der gerade eingelesenen Konfigurationsdatei, beginnend bei eins.

- .SECTION: Name des gerade eingelesenen Abschnitts oder dessen Typ, wenn der Abschnitt
  keinen Namen hat, etwa "global". Vor dem ersten Abschnitt ist dies eine leere Zeichenkette.

Diese Variablen werden an der Stelle aufgelöst, an der sie eingelesen werden. Wird beispielsweise ".LINE" in einer "log-format"-Direktive eines defaults-Abschnitts verwendet, steht die Zeilennummer bereits vor dem Parsen und Kompilieren der "log-format"-Direktive fest. Nachfolgende Proxys verwenden daher dieselbe Zeilennummer.

So lassen sich in Variablen, Protokollen, Fehlerstatus, Health Checks und Header-Werten Informationen zum Auffinden einer Regel ausgeben. Zeilennummern können sogar zur Benennung von Konfigurationsobjekten wie Servern dienen.

## 2.4. Bedingte Blöcke {#section-2-4}

Manchmal ist es praktisch, beliebige Teile der Konfiguration abhängig von Bedingungen ein- oder auszuschalten. So lassen sich beispielsweise SSL oder Cipher sowie Listener einer Vorproduktionsumgebung ohne Änderung der Konfiguration aktivieren oder deaktivieren. Auch die Konfigurationssyntax kann während einer Migration zwei verschiedene HAProxy-Versionen unterstützen. HAProxy bietet dafür verschachtelbare Direktiven nach Art eines Präprozessors, die Textblöcke einbeziehen oder ignorieren. Diese Direktiven müssen in einer eigenen Zeile stehen und wirken auf die folgenden Zeilen. Zwei davon unterstützen einen Ausdruck; die anderen wechseln lediglich zu einem alternativen Block oder schließen die aktuelle Ebene ab. Bedingte Blöcke werden mit folgenden 4 Direktiven gebildet:

- .if `<condition>`
- .elif `<condition>`
- .else
- .endif

".if" eröffnet eine neue verschachtelte Ebene, ".elif" und ".else" bleiben auf derselben Ebene, und ".endif" schließt eine Ebene. Jedes ".if" muss mit einem zugehörigen ".endif" abgeschlossen werden. ".elif" darf nur auf ".if" oder ".elif" folgen; beliebig viele ".elif" können aufeinanderfolgen. Je ".if" ist nur ein ".else" zulässig. Es muss immer nach dem ".if" oder dem letzten ".elif" eines Blocks stehen.

Kommentare können bei Bedarf nach einem '#' in derselben Zeile stehen und werden ignoriert. Die Direktiven werden wie andere Konfigurationsdirektiven in Tokens zerlegt; daher können Bedingungen Umgebungsvariablen verwenden.

Bedingungen lassen sich auch beim Start mit dem Parameter -cc auswerten. Siehe „3. HAProxy starten“ im Verwaltungshandbuch.

Eine Bedingung ist entweder eine leere Zeichenkette, die falsch ergibt, oder ein Ausdruck aus einer beliebigen Kombination folgender Elemente:

- die Ganzzahl null ('0'), die immer "false" ergibt
- eine Ganzzahl ungleich null, etwa '1', die immer "true" ergibt
- ein Prädikat, optional gefolgt von Argumenten in runden Klammern
- eine Bedingung in einem Paar runder Klammern '(' und ')'
- ein Ausrufezeichen ('!') vor einem der obigen nicht leeren Elemente, das dessen Wert negiert
- mit logischem AND ('&&') verknüpfte Ausdrücke, die von links nach rechts ausgewertet werden,
  bis einer falsch ergibt
- mit logischem OR ('\|\|') verknüpfte Ausdrücke, die von rechts nach links ausgewertet werden,
  bis einer wahr ergibt

Dabei werden derselbe Zeilen-Tokenizer und Argumentparser wie in der übrigen Konfigurationssprache verwendet. Wörter werden an Folgen eines oder mehrerer ungeschützter Leerzeichen oder Tabulatoren getrennt und vor der Auswertung mit jeweils einem Leerzeichen wieder zusammengesetzt. So muss nicht die gesamte Zeile in Anführungszeichen gesetzt werden. Allerdings gehören dadurch Leerzeichen um Kommas oder Klammern tatsächlich zum Wert, was nicht immer erwartet wird. Beispielsweise prüft der folgende Ausdruck:

```text
.if defined( HAPROXY_MWORKER )
```

ob die Variable " HAPROXY_MWORKER " mit den Leerzeichen existiert. Dieser Ausdruck:

```text
.if streq("$ENABLE_SSL",     1)
```

vergleicht dagegen die Umgebungsvariable "ENABLE_SSL" mit dem Wert " 1", der ein einzelnes führendes Leerzeichen enthält. Denn die Zeile wird zunächst wie folgt in Wörter zerlegt:

```text
   .if streq("$ENABLE_SSL",     1)
  |---|--------------------|   |--|
    1           2               3
```

Anschließend wird das schwache Quoting verarbeitet und die Umgebungsvariable "\$ENABLE_SSL" aufgelöst, beispielsweise mit ENABLE_SSL=0. Schließlich werden die Wörter mit jeweils einem Leerzeichen dazwischen zu einer einzigen Zeichenkette zusammengesetzt:

```text
   .if streq(0, 1)
  |---|-------|--|
    1     2     3
```

Erst danach wird diese als einzelner Ausdruck ausgewertet. Das zwischen Komma und "1" eingefügte Leerzeichen gehört weiterhin zum Argumentwert, sodass das Argument " 1" lautet:

```text
   .if streq(0, 1)
  |---|-----|-|--|
    \    \    \  \_ Argument2: " 1"
     \    \    \___ Argument1: "0"
      \    \_______ Funktion: "streq"
       \___________ Direktive: ".if"
```

Selbst wenn ENABLE_SSL den Wert "1" hätte, würde dieser also nicht mit " 1" übereinstimmen, da sich die Zeichenketten um ein Leerzeichen unterscheiden.

Hinweis: Wie in Abschnitt „2.2. Anführungszeichen und Maskierung“ erläutert, ist es eine gute Faustregel, niemals unnötige Leerzeichen in Ausdrücke einzufügen.

Wie in anderen Sprachen hat AND Vorrang vor OR. Daher wird "A && B \|\| C && D" als "(A && B) \|\| (C && D)" ausgewertet.

Derzeit werden folgende Prädikate unterstützt:

- awslc_api_atleast(`<ver>`): ergibt wahr, wenn die aktuelle awslc-API-Nummer mindestens
  so neu wie `<ver>` ist, andernfalls falsch. Beispiel: awslc_api_atleast(35)

- awslc_api_before(`<ver>`): ergibt wahr, wenn die aktuelle awslc-API-Nummer strikt älter
  als `<ver>` ist, andernfalls falsch. Beispiel: awslc_api_before(26)

- defined(`<name>`) : ergibt wahr, wenn die Umgebungsvariable `<name>` existiert,
  unabhängig von ihrem Inhalt

- feature(`<name>`) : ergibt wahr, wenn die Funktion `<name>` in der Funktionsliste von
  "haproxy -vv" als vorhanden aufgeführt ist, also `<name>` nach einem '+' erscheint

- openssl_version_atleast(`<ver>`): ergibt wahr, wenn die aktuelle openssl-Version
  mindestens so neu wie `<ver>` ist, andernfalls falsch. Bibliotheken wie LibreSSL, AWS-LC
  und WolfSSL geben ebenfalls eine Pseudo-OpenSSL-Version an. Beispiel:

```text
ssllib_name_startswith(OpenSSL) && openssl_version_atleast(1.1.1)
```

- openssl_version_before(`<ver>`): ergibt wahr, wenn die aktuelle openssl-Version strikt
  älter als `<ver>` ist, andernfalls falsch. Bibliotheken wie LibreSSL, AWS-LC und WolfSSL
  geben ebenfalls eine Pseudo-OpenSSL-Version an. Beispiel: openssl_version_before(3.5.0)

- ssllib_name_startswith(`<name>`) : ergibt wahr, wenn der Name der mit HAProxy eingebundenen
  SSL-Bibliothek mit `<name>` beginnt. Beispiel: ssllib_name_startswith(wolfSSL)

- streq(`<str1>`,`<str2>`) : ergibt nur dann wahr, wenn beide Zeichenketten gleich sind

- strneq(`<str1>`,`<str2>`): ergibt nur dann wahr, wenn sich beide Zeichenketten unterscheiden

- strstr(`<str1>`,`<str2>`): ergibt nur dann wahr, wenn die zweite Zeichenkette in der ersten vorkommt.

- version_atleast(`<ver>`): ergibt wahr, wenn die aktuelle haproxy-Version mindestens so
  neu wie `<ver>` ist, andernfalls falsch. Die Versionssyntax entspricht der Ausgabe von
  "haproxy -v"; fehlende Bestandteile werden als null angenommen.

- version_before(`<ver>`): ergibt wahr, wenn die aktuelle haproxy-Version strikt älter
  als `<ver>` ist, andernfalls falsch. Die Versionssyntax entspricht der Ausgabe von
  "haproxy -v"; fehlende Bestandteile werden als null angenommen.

- enabled(`<opt>`) : ergibt wahr, wenn die Option `<opt>` zur Laufzeit aktiviert ist.
  Nur ein Teil der Optionen wird unterstützt:

```text
POLL, EPOLL, KQUEUE, EVPORTS, SPLICE,
GETADDRINFO, REUSEPORT, FAST-FORWARD,
SERVER-SSL-VERIFY-NONE
```

Beispiel:

```haproxy
# 1. HAPROXY_MWORKER variable is set automatically by HAProxy in master and
# in worker process environments (see HAProxy variables matrix from
# 2.3. Environment variables). Its presence enables an additional listener.

global
  master-worker

.if defined(HAPROXY_MWORKER)
    listen mwcli_px
       bind :1111
       ...
.endif
```


```haproxy
# 2. HAPROXY_BRANCH is set automatically by HAProxy in master and in worker
# process environments (see HAProxy variables matrix from 2.3. Environment
# variables). We check HAPROXY_BRANCH value and conditionally enable
# mworker-max-reloads parameter.

global
  master-worker

.if streq("$HAPROXY_BRANCH",3.1)
     mworker-max-reloads 5
.endif
```


```haproxy
# 3. Some arbitrary environment variables are set by user in the global
# section. If HAProxy is started in master-worker mode, they are presented in
# master and in worker process environments. We check values of these
# variables and conditionally enable ports 80 and 443. Environment variables
# checks can be mixed with features and version checks.

global
  setenv WITH_SSL yes
  unsetenv SSL_ONLY

.if strneq("$SSL_ONLY",yes)
       bind :80
.endif

.if streq("$WITH_SSL",yes)
  .if feature(OPENSSL)
       bind :443 ssl crt ...
  .endif
.endif

.if feature(OPENSSL) && (streq("$WITH_SSL",yes) || streq("$SSL_ONLY",yes))
       bind :443 ssl crt ...
.endif

.if version_atleast(2.4-dev19)
    profiling.memory on
.endif

.if !feature(OPENSSL)
    .alert "SSL support is mandatory"
.endif
```


Vier weitere Direktiven dienen der Ausgabe von Statusmeldungen:

- .diag "message" : gibt diese Meldung nur im Diagnosemodus (-dD) aus
- .notice "message" : gibt diese Meldung auf der Stufe NOTICE aus
- .warning "message": gibt diese Meldung auf der Stufe WARNING aus
- .alert "message" : gibt diese Meldung auf der Stufe ALERT aus

Meldungen auf der Stufe WARNING können den Prozessstart verhindern, wenn "zero-warning" aktiviert ist. Meldungen auf der Stufe ALERT führen immer zu einem schwerwiegenden Fehler. Damit lassen sich ungeeignete Bedingungen erkennen und Hinweise für den Anwender ausgeben.

Beispiel:

```text
.if "${A}"
  .if "${B}"
     .notice "A=1, B=1"
  .elif "${C}"
     .notice "A=1, B=0, C=1"
  .elif "${D}"
     .warning "A=1, B=0, C=0, D=1"
  .else
     .alert "A=1, B=0, C=0, D=0"
  .endif
.else
     .notice "A=0"
.endif

.diag "WTA/2021-05-07: replace 'redirect' with 'return' after switch to 2.4"
      http-request redirect location /goaway if ABUSE
```

## 2.5. Zeitformat {#section-2-5}

Manche Parameter enthalten Zeitwerte, etwa Zeitüberschreitungen. Sofern nicht ausdrücklich anders angegeben, werden sie gewöhnlich in Millisekunden ausgedrückt. Durch Anhängen einer Einheit an den Zahlenwert können aber auch andere Einheiten verwendet werden. Dies ist zu beachten, da es nicht bei jedem Schlüsselwort wiederholt wird. Unterstützt werden:

- us: Mikrosekunden. 1 Mikrosekunde = 1/1000000 Sekunde
- ms: Millisekunden. 1 Millisekunde = 1/1000 Sekunde. Dies ist der Standard.
- s : Sekunden. 1s = 1000ms
- m : Minuten. 1m = 60s = 60000ms
- h : Stunden. 1h = 60m = 3600s = 3600000ms
- d : Tage. 1d = 24h = 1440m = 86400s = 86400000ms

## 2.6. Größenformat {#section-2-6}

Manche Parameter enthalten Größenwerte, etwa Bandbreitengrenzen. Sofern nicht ausdrücklich anders angegeben, werden sie gewöhnlich in Bytes ausgedrückt. Durch Anhängen einer Einheit an den Zahlenwert können aber auch andere Einheiten verwendet werden. Dies ist zu beachten, da es nicht bei jedem Schlüsselwort wiederholt wird. Die folgenden Einheiten werden unabhängig von der Groß-/Kleinschreibung unterstützt:

- k: Kilobytes. 1 Kilobyte = 1024 Bytes
- m: Megabytes. 1 Megabyte = 1048576 Bytes
- g: Gigabytes. 1 Gigabyte = 1073741824 Bytes

Zeit- und Größenformate erfordern Ganzzahlen; Nachkommastellen sind nicht zulässig.

## 2.7. Namensformat für Maps und ACLs {#section-2-7}

Für Maps und ACLs können Musterlisten verwendet werden. Eine Musterliste wird durch ihren Namen identifiziert und kann an verschiedenen Stellen der Konfiguration zum Einsatz kommen. Je nach Namensformat gibt es drei Kategorien:

- Musterlisten aus regulären Dateien: Dies ist der Standardfall. Der absolute oder relative
  Dateiname dient als Name. Die Datei muss existieren, andernfalls tritt ein Fehler auf;
  sie darf jedoch leer sein. Das Präfix "file@" kann angegeben werden, gehört aber nicht zum
  Namen der Liste. Ein Dateiname verweist mit und ohne dieses Präfix auf dieselbe Musterliste.

- Musterlisten aus optionalen Dateien: Vor dem Dateinamen muss das Präfix "opt@" stehen.
  Die Datei muss nicht existieren. Ist sie vorhanden, wird ihr Inhalt geladen; fehlt sie,
  wird kein Fehler gemeldet. Das Präfix gehört nicht zum Namen der Liste. Bei gleichem
  Dateinamen verweisen optionale und reguläre Dateien daher auf dieselbe Musterliste.

- Musterlisten aus virtuellen Dateien: Der Name ist lediglich eine Kennung und verweist auf
  keine Datei. Das Präfix "virt@" muss verwendet werden und gehört zum Namen. Diese Listen
  lassen sich daher nicht mit den anderen Arten vermischen.

Virtuelle Dateien eignen sich für vollständig dynamisch verwaltete Muster, die beim Start und Neuladen noch nicht vorhanden sind. Optionale Dateien können unter denselben Bedingungen verwendet werden. Muster lassen sich jedoch in die Datei schreiben, etwa mit einem externen Skript auf Basis des CLI-Befehls "show map". Dadurch können sie beim Neuladen erhalten bleiben.

Hinweis: Auch wenn solche Namen unwahrscheinlich sind, können damit keine regulären Dateien geladen werden, deren Name mit "file@", "opt@" oder "virt@" beginnt. Dazu muss ausdrücklich "./" vor den Dateinamen gesetzt werden, beispielsweise "file@./virt@map".

## 2.8. Variablen {#section-2-8}

In der HAProxy-Konfiguration lassen sich Variablen in Sample-Abruffunktionen, Konvertern, log-format-Zeichenketten und TCP/HTTP-Aktionen verwenden. Prozessweite Variablen sind während der gesamten Prozesslebensdauer global zugänglich; andere haben eine kürzere Lebensdauer. Wie in Shell-Skripten ist eine Variable ein symbolischer Name für einen Speicherbereich. Ihre Größe ist unbegrenzt, und der Speicher wird dynamisch reserviert. Deshalb müssen Variablen besonders bei intensiver Nutzung mit Vorsicht eingesetzt werden. Über die globalen Parameter "tune.vars" lässt sich jedoch der maximale Speicherverbrauch der Variablen begrenzen.

Variablen müssen im Format "`<scope>`.`<name>`" bezeichnet werden. `<scope>` ist ein einzelnes Wort für die Lebensdauer der Variablen. Der Teil `<name>` darf innerhalb eines Geltungsbereichs nur 'a-z', 'A-Z', '0-9' und '\_' enthalten. Er ist dort eindeutig. Derselbe Name kann jedoch in verschiedenen Geltungsbereichen vorkommen und bezeichnet dann unterschiedliche Variablen. Unterstützt werden folgende Geltungsbereiche:

- proc : Variablen, die während der gesamten Prozesslebensdauer bekannt und global
  zugänglich sind. "proc"-Variablen lassen sich über die CLI mit "get var" und "set var"
  bearbeiten. In Abschnitten des Typs "global" können sie außerdem mit "set-var" und
  "set-var-fmt" gesetzt werden.

- sess : Variablen, die während der gesamten Sitzungslebensdauer bekannt sind. "sess"-Variablen
  gehören ausschließlich zu einer Sitzung, sind außerhalb davon unsichtbar und werden nicht
  mit anderen Sitzungen geteilt.

- txn : Variablen, die während der gesamten Transaktionslebensdauer bekannt sind. "txn"-Variablen
  gehören ausschließlich zu einem Stream, sind außerhalb davon unsichtbar und werden nicht
  mit anderen Streams geteilt.

- req : Variablen, die während der Anfrageverarbeitung eines bestimmten Streams bekannt sind.
  "req"-Variablen sind vom Erzeugen des Streams bis zum ersten Verbindungsversuch zum Server
  sichtbar. Sie gehören ausschließlich zu einem Stream, sind außerhalb davon unsichtbar und
  werden nicht mit anderen Streams geteilt. Zwischen "req"- und "res"-Variablen gibt es
  keinerlei Überschneidung.

- res : Variablen, die während der Antwortverarbeitung eines bestimmten Streams bekannt sind.
  "res"-Variablen sind vom ersten Verbindungsversuch zum Server bis zur Zerstörung des Streams
  sichtbar. Sie gehören ausschließlich zu einem Stream, sind außerhalb davon unsichtbar und
  werden nicht mit anderen Streams geteilt. Zwischen "req"- und "res"-Variablen gibt es
  keinerlei Überschneidung.

- check: Variablen, die während eines Health Checks bekannt sind. "check"-Variablen gehören
  ausschließlich zu einem Health Check, sind außerhalb davon unsichtbar und werden nicht mit
  anderen Health Checks geteilt. Sie können mit speziellen "tcp-check"- oder "http-check"-Direktiven
  gesetzt werden.

Je nach Kontext können zusätzliche Geltungsbereiche verwendet werden, die auf den Elternstream des aktuellen Streams verweisen:

- psess: wie "sess", verwendet jedoch die Sitzung des Elternstreams, sofern vorhanden.

- ptxn : wie "txn", verwendet jedoch die Transaktion des Elternstreams, sofern vorhanden.

- preq : wie "req", verwendet jedoch den Elternstream, sofern vorhanden. "preq"-Variablen
  sind nur während der Anfrageverarbeitung des Elternstreams zugänglich.

- pres : wie "res", verwendet jedoch den Elternstream, sofern vorhanden. "pres"-Variablen
  sind nur während der Antwortverarbeitung des Elternstreams zugänglich.

Auf den Elternstream verweisende Geltungsbereiche sind nutzbar, sobald dieser definiert ist. Meist gibt es keinen Elternstream; andernfalls wird dies ausdrücklich angegeben. Derzeit können nur Werte von Variablen aus einem Geltungsbereich des Elternstreams gelesen werden. Solche Variablen lassen sich weder setzen noch entfernen. Ein Kindstream übernimmt gewöhnlich zu einem bestimmten Zeitpunkt eine Verarbeitung für den Elternstream und hält diesen an, bis der Vorgang abgeschlossen ist. Der Elternstream kann daher beispielsweise mitten in der Anfrage- oder Antwortverarbeitung pausieren. Bestimmte Geltungsbereiche sind dann vom Kindstream aus nicht verfügbar. Untersucht etwa ein Kindstream eine Anfrage, findet er keine Variablen im Geltungsbereich "pres": Der Elternstream verarbeitet gerade keine Antwort und hat deshalb keine Variablen im Bereich "res".

Der Inhalt einer Variablen ist das Ergebnis eines Sample-Abrufausdrucks und übernimmt dessen Ausgabetyp. Dieser muss zur Verwendung der Variablen passen. Enthält eine Variable beispielsweise eine Zeichenkette und wird im Konverter "add()" verwendet, muss sie für einen erfolgreichen Aufruf in eine gültige Ganzzahl umwandelbar sein. Das ist besonders beim Vergleich von Variablen mit statischen Werten wichtig: Es muss die passende Abgleichmethode verwendet werden.

## 2.9. Adressformate {#section-2-9}

Mehrere Direktiven wie "bind", "server", "nameserver" und "log" benötigen eine Adresse.

Dies kann ein Hostname, eine IPv4- oder IPv6-Adresse oder '*' sein. '*' entspricht der speziellen Adresse "0.0.0.0" und kann bei "bind" oder "dgram-bind" verwendet werden, um auf allen IPv4-Adressen des Systems zu lauschen. Die IPv6-Entsprechung ist '::'.

Je nach Direktive folgt auf die IP-Adresse ein Port oder Portbereich. Bei 'bind' ist dies zwingend erforderlich, bei 'server' optional.

Die Adresse kann auch mit einem Schrägstrich '/' beginnen. Dann gehört sie zur Familie "unix", und '/' mit den folgenden Zeichen muss den Pfad angeben.

Ob standardmäßig der Socket-Typ beziehungsweise die Transportmethode "datagram" oder "stream" verwendet wird, hängt von der Direktive mit der Adresse ab. 'bind' und 'server' verwenden standardmäßig "stream", während 'log', 'nameserver' und 'dgram-bind' "datagram" verwenden.

Optional kann ein Präfix die Adressfamilie und/oder den Socket-Typ sowie die Transportmethode erzwingen.

### 2.9.1. Präfixe für Adressfamilien {#section-2-9-1}

'abns@`<name>`': Der folgende `<name>` bezeichnet einen abstrakten Namensraum (nur unter Linux).

'abnsz@`<name>`': Der folgende `<name>` bezeichnet einen nullterminierten abstrakten Namensraum (nur unter Linux).

'fd@`<n>`': Die folgende Adresse ist ein vom Elternprozess geerbter Dateideskriptor `<n>`. Er muss gebunden sein, kann aber bereits lauschen oder noch nicht.

'ip@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt je nach Syntax als IPv4- oder IPv6-Adresse. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'ipv4@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv4-Adresse. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'ipv6@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv6-Adresse. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'sockpair@`<n>`': Die folgende Adresse ist der Dateideskriptor eines verbundenen Unix-Sockets oder eines Socket-Paars. Beim Verbindungsaufbau erzeugt der Initiator ein Paar verbundener Sockets und übergibt einen davon über den FD an die Gegenstelle. Der Listener wartet auf den FD über den Unix-Socket und verwendet ihn wie den FD eines accept(). Mit Vorsicht verwenden.

               Fehler: Dieses Protokoll ist unter macOS bekanntermaßen
               unzuverlässig, da die sendmsg(2)-Implementierung von macOS
               fehlerhaft ist. Die Verbindung wird möglicherweise nicht korrekt angenommen.

'unix@`<path>`': Die folgende Zeichenkette gilt als UNIX-Socket `<path>`. Das Präfix eignet sich zur Angabe eines UNIX-Socket-Pfads, der nicht mit '/' beginnt.

### 2.9.2. Präfixe für Socket-Typen {#section-2-9-2}

Den obigen Präfixen für Adressfamilien kann ein weiteres Präfix vorangestellt werden, um Socket-Typ und Transportmethode zu erzwingen. Der Standard hängt von der Direktive mit der Adresse ab, kann aber in manchen Fällen überschrieben werden. So verwendet "log" standardmäßig syslog über UDP, lässt sich aber auf syslog über TCP zwingen.

Diese Präfixe wurden für interne Zwecke entworfen. Anwender sollten stattdessen die Aliase aus dem folgenden Abschnitt „2.9.3. Protokollpräfixe“ verwenden. Gelegentlich sind sie dennoch praktisch, etwa bei geerbten Sockets, die über ihre Dateideskriptornummer bekannt sind. In diesem Fall ist die Adressfamilie "fd", und der Socket-Typ muss angegeben werden.

Wer eines dieser Präfixe benötigt, weil sich das gewünschte Verhalten nicht mit Protokollpräfixen konfigurieren lässt, sollte dies den Betreuern melden.

'stream+`<family>`@`<address>`' erzwingt "stream" als Socket-Typ und Transportmethode.

'dgram+`<family>`@`<address>`' erzwingt "datagram" als Socket-Typ und Transportmethode.

'quic+`<family>`@`<address>`' erzwingt den Socket-Typ "datagram" und die Transportmethode "stream".

### 2.9.3. Protokollpräfixe {#section-2-9-3}

'quic4@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv4-Adresse; der Socket-Typ wird jedoch auf "datagram" und die Transportmethode auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein UDP-Port oder -Portbereich angegeben werden. Dies entspricht "quic+ipv4@".

'quic6@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv6-Adresse; der Socket-Typ wird jedoch auf "datagram" und die Transportmethode auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein UDP-Port oder -Portbereich angegeben werden. Dies entspricht "quic+ipv6@".

'tcp@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt je nach Syntax als IPv4- oder IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'stream+ip@'.

'tcp4@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv4-Adresse; Socket-Typ und Transportmethode werden jedoch auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'stream+ipv4@'.

'tcp6@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'stream+ipv6@'.

'mptcp@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt je nach Syntax als IPv4- oder IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch mit dem MPTCP-Protokoll auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'mptcp4@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv4-Adresse; Socket-Typ und Transportmethode werden jedoch mit dem MPTCP-Protokoll auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'mptcp6@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch mit dem MPTCP-Protokoll auf "stream" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden.

'udp@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt je nach Syntax als IPv4- oder IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch auf "datagram" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'dgram+ip@'.

'udp4@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv4-Adresse; Socket-Typ und Transportmethode werden jedoch auf "datagram" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'dgram+ipv4@'.

'udp6@`<address>`[:port1[-port2]]': Die folgende `<address>` gilt immer als IPv6-Adresse; Socket-Typ und Transportmethode werden jedoch auf "datagram" festgelegt. Je nach verwendender Direktive kann oder muss ein Port oder Portbereich angegeben werden. Dies ist ein Alias für 'dgram+ipv6@'.

'uxdg@`<path>`': Die folgende Zeichenkette gilt als Unix-Socket `<path>`; die Transportmethode wird jedoch auf "datagram" festgelegt. Dies ist ein Alias für 'dgram+unix@'.

'uxst@`<path>`': Die folgende Zeichenkette gilt als Unix-Socket `<path>`; die Transportmethode wird jedoch auf "stream" festgelegt. Dies ist ein Alias für 'stream+unix@'.

In künftigen Versionen könnten weitere Präfixe für Protokolle wie QUIC verwendet werden, das einen Stream-Transport auf Sockets des Typs "datagram" bereitstellt.

## 2.10. Beispiele {#section-2-10}

```haproxy
# Simple configuration for an HTTP proxy listening on port 80 on all
    # interfaces and forwarding requests to a single backend "servers" with a
    # single server "server1" listening on 127.0.0.1:8000
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    frontend http-in
        bind *:80
        default_backend servers

    backend servers
        server server1 127.0.0.1:8000 maxconn 32


    # The same configuration defined with a single listen block. Shorter but
    # less expressive, especially in HTTP mode.
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    listen http-in
        bind *:80
        server server1 127.0.0.1:8000 maxconn 32
```

Ist haproxy über \$PATH erreichbar, lassen sich diese Konfigurationen in einer Shell wie folgt prüfen:

```shell
$ sudo haproxy -f configuration.conf -c
```
