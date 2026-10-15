---
title: "7. ACLs und Sample-Abruf"
linkTitle: "7. ACLs & Sample-Abruf"
weight: 180
description: "ACL-Vergleiche, Bedingungen, Konverter, Sample-Abrufe und vordefinierte ACLs"
icon: fa-solid fa-filter
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/acls-and-samples/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 7"
---

HAProxy ist in der Lage, Daten aus Anfrage- oder Antwortströmen, aus Client- oder Serverinformationen, aus Tabellen, Umgebungsdaten usw. zu extrahieren. Der Vorgang, solche Daten zu extrahieren, wird als Sample-Abruf bezeichnet. Nach dem Abruf können diese Samples für verschiedene Zwecke verwendet werden, beispielsweise als Schlüssel einer Stick Table. Am häufigsten werden sie jedoch mit vordefinierten konstanten Daten, sogenannten Mustern, verglichen.

## 7.1. ACL-Grundlagen {#section-7-1}
Mit Zugriffskontrolllisten (ACL) wird eine benannte Methode deklariert, die beliebige Informationen mit einer Liste vordefinierter Muster vergleicht. Sie sollten als praktisch gleichwertig mit Funktionen in den meisten Programmiersprachen betrachtet werden: Durch die Deklaration stehen sie bereit und können später bei Bedarf aufgerufen werden. Ihre Auswertung ergibt lediglich eine Übereinstimmung oder Nichtübereinstimmung, was vergleichbar mit booleschen Werten in vielen Programmiersprachen ist. Im Gegensatz zu Funktionen in Programmiersprachen können ACLs beliebig oft überladen werden, um zusätzliche Übereinstimmungsmethoden für denselben Namen zu definieren. In diesem Fall werden sie alle in der Deklarationsreihenfolge ausgewertet, bis eine Übereinstimmung vorliegt.

ACLs bieten eine flexible Lösung, um anhand von Inhalten zwischen Zielen umzuschalten und allgemein Entscheidungen auf Grundlage von Daten aus der Anfrage, der Antwort oder dem Umgebungsstatus zu treffen. Das Prinzip ist einfach:

- ein Daten-Sample aus einem Datenstrom, einer Tabelle oder der Umgebung extrahieren
- optional das Format des extrahierten Samples umwandeln
- eine oder mehrere Methoden zum Musterabgleich auf dieses Sample anwenden
- Aktionen nur ausführen, wenn ein Muster auf das Sample zutrifft

Die Aktionen bestehen in der Regel darin, eine Anfrage zu blockieren, ein Backend auszuwählen oder einen Header hinzuzufügen.

Um einen Test zu definieren, wird das Schlüsselwort "acl" verwendet. Die Syntax lautet:

```text
acl <aclname> <criterion> [flags] [operator] [<value>] ...
```

Dies erstellt eine neue ACL `<aclname>` oder ergänzt eine bestehende mit neuen Tests. Diese Tests gelten für den im `<criterion>` angegebenen Teil der Anfrage/Antwort und können mit optionalen Flags [flags] angepasst werden. Einige Kriterien unterstützen auch einen Operator, der vor der Wertemenge angegeben werden kann. Optional können einige Konverter auf das Sample angewendet werden, und sie werden als durch Kommas getrennte Liste von Schlüsselwörtern unmittelbar nach dem ersten Schlüsselwort angegeben. Die Werte sind vom Typ, der vom Kriterium unterstützt wird, und werden durch Leerzeichen getrennt.

ACL-Namen müssen aus Groß- und Kleinbuchstaben, Ziffern, '-' (Bindestrich), '\_' (Unterstrich), '.' (Punkt) und ':' (Doppelpunkt) bestehen. Bei ACL-Namen wird zwischen Groß- und Kleinschreibung unterschieden, was bedeutet, dass "my_acl" und "My_Acl" zwei verschiedene ACLs sind.

Es gibt keine festgelegte Obergrenze für die Anzahl der ACLs. Unbenutzte ACLs beeinflussen die Leistung nicht, sie belegen lediglich wenig Speicher.

Das Kriterium ist im Allgemeinen der Name einer Sample-Abruf-Methode oder einer ihrer ACL-spezifischen Varianten. Die Standardtestmethode wird implizit durch den Ausgabetyp dieser Sample-Abruf-Methode bestimmt. Die ACL-Varianten können alternative Übereinstimmungsmethoden für dieselbe Sample-Abruf-Methode beschreiben. Nur die Sample-Abruf-Methoden unterstützen eine Umwandlung.

Sample-Abruf-Methoden geben Daten zurück, die von folgenden Typen sein können:

-  boolesch
-  Ganzzahl (vorzeichenbehaftet oder vorzeichenlos)
-  IPv4- oder IPv6-Adresse
-  Zeichenkette
-  Datenblock

Konverter können Daten eines dieser Typen in jeden dieser Typen umwandeln. Beispielsweise wandeln einige Konverter eine Zeichenkette in Kleinbuchstaben um; andere konvertieren eine Zeichenkette in eine IPv4-Adresse oder wenden eine Netzmaske auf eine IP-Adresse an. Das resultierende Sample hat den Typ des zuletzt in der Liste angewendeten Konverters. Ohne Konverter entspricht er dem Typ der Sample-Abruf-Methode.

Jedes Sample oder jeder Konverter gibt Daten eines bestimmten Typs zurück, der mit seinem Schlüsselwort in dieser Dokumentation angegeben wird. Wird eine ACL mit einer Standard-Sample-Abruf-Methode deklariert, wird für bestimmte Typen automatisch eine Standardabgleichsmethode verwendet, wie in der folgenden Tabelle zusammengefasst:

```text
   +------------------+-------------------+
   | Sample/Konverter | Standard-         |
   | Ausgabetyp       | Abgleich          |
   +------------------+-------------------+
   | boolean          | bool              |
   +------------------+-------------------+
   | integer          | int               |
   +------------------+-------------------+
   | ip               | ip                |
   +------------------+-------------------+
   | string           | str               |
   +------------------+-------------------+
   | binary           | kein; "-m" nutzen |
   +------------------+-------------------+
```

Beachten Sie, dass zum Abgleich von Binär-Samples eine Übereinstimmungsmethode explizit angegeben werden muss, siehe unten.

Die ACL-Engine kann diese Typen gegen Muster folgender Typen abgleichen:

-  boolesch
-  Ganzzahl oder Ganzzahlbereich
-  IP-Adresse / Netzwerk
-  Zeichenkette (genau, Teilzeichenkette, Suffix, Präfix, Unterordner, Domain)
-  regulärer Ausdruck
-  Hex-Block

Die folgenden ACL-Flags werden derzeit unterstützt:

```text
-i: Groß-/Kleinschreibung beim Abgleich aller nachfolgenden Muster ignorieren.
-f: Muster aus einer Liste laden.
-m: eine bestimmte Methode zum Musterabgleich verwenden
-n: DNS-Auflösungen verbieten
-M: die mit -f angegebene Datei wie eine Map laden.
-u: die eindeutige ID der ACL erzwingen
--: das Ende der Flags erzwingen. Nützlich, wenn eine Zeichenkette wie eines der Flags aussieht.
```

Auf das Flag "-f" folgt ein Name, der dem in 2.7 beschriebenen Namensformat für Maps und ACLs entsprechen muss. Es ist sogar möglich, mehrere "-f"-Argumente anzugeben, wenn die Muster aus mehreren Listen geladen werden sollen. Wenn eine vorhandene Datei referenziert wird, werden alle Zeilen als einzelne Werte gelesen. Leere Zeilen sowie Zeilen, die mit einem Rautezeichen ('#') beginnen, werden ignoriert. Alle führenden Leerzeichen und Tabulatoren werden entfernt. Muss unbedingt ein gültiges Muster eingefügt werden, das mit einem Rautezeichen beginnt, einfach ein Leerzeichen voranstellen, damit es nicht als Kommentar interpretiert wird. Je nach Datentyp und Abgleichsmethode kann HAProxy die Zeilen in einen binären Baum laden, was sehr schnelle Abfragen ermöglicht. Dies gilt für IPv4 und exakte Zeichenkettenabgleiche. In diesem Fall werden Duplikate automatisch entfernt.

Das Flag "-M" ermöglicht einer ACL die Verwendung einer Map. Wenn dieses Flag gesetzt ist, wird die Liste als zweispaltige Einträge analysiert. Die erste Spalte enthält die Muster, die von der ACL verwendet werden, und die zweite Spalte enthält die Samples. Das Sample kann später von einer Map verwendet werden. Dies kann in seltenen Fällen nützlich sein, wenn eine ACL lediglich dazu dient, die Existenz eines Musters in einer Map zu überprüfen, bevor eine Zuordnung angewendet wird.

Das Flag "-u" erzwingt die eindeutige ID der ACL. Diese eindeutige ID wird mit der Socket-Schnittstelle verwendet, um ACLs zu identifizieren und deren Werte dynamisch zu ändern. Beachten Sie, dass eine Datei immer anhand ihres Namens identifiziert wird, selbst wenn eine ID festgelegt ist.

Außerdem gilt: Das Flag "-i" wirkt sich auf nachfolgende Einträge aus und nicht auf Einträge, die aus vorhergehenden Dateien geladen wurden. Zum Beispiel:

```text
acl valid-ua hdr(user-agent) -f exact-ua.lst -i -f generic-ua.lst test
```

In diesem Beispiel wird jeder Eintrag aus "exact-ua.lst" exakt gegen den "user-agent"-Header der Anfrage abgeglichen. Danach wird jeder Eintrag aus "generic-ua" ohne Berücksichtigung der Groß-/Kleinschreibung abgeglichen. Anschließend wird auch das Wort "test" ohne Berücksichtigung der Groß-/Kleinschreibung abgeglichen.

Das Flag "-m" dient zur Auswahl einer bestimmten Musterabgleichsmethode für die Eingabedaten. Alle ACL-spezifischen Kriterien implizieren eine Musterabgleichsmethode und benötigen dieses Flag im Allgemeinen nicht. Es ist jedoch nützlich bei generischen Sample-Abrufmethoden, um anzugeben, wie diese gegen Muster abgeglichen werden sollen. Dies ist erforderlich für Sample-Abrufe, die einen Datentyp zurückgeben, für den keine offensichtliche Abgleichsmethode existiert (z. B. Zeichenkette oder Binärdaten). Wenn "-m" angegeben und gefolgt von einem Namen einer Musterabgleichsmethode ist, wird diese statt der Standardmethode für das Kriterium verwendet. Dadurch ist es möglich, Inhalte auf Arten abzugleichen, die ursprünglich nicht geplant waren, oder mit Sample-Abrufmethoden, die eine Zeichenkette zurückgeben. Die Abgleichsmethode beeinflusst auch die Art und Weise, wie die Muster analysiert werden. Daher darf sie nicht mit Sample-Abrufen verwendet werden, die ein Suffix für den Musterabgleich haben (\_beg, \_end, \_sub...). Außerdem ist die Angabe mehrerer "-m" Musterabgleichsmethoden nicht zulässig.

Das Flag "-n" verbietet DNS-Auflösungen. Es wird zusammen mit dem Laden von IP-Dateien verwendet. Standardmäßig nimmt der Parser an, dass eine nicht parsbare IP-Adresse möglicherweise ein Domänenname ist und versucht dann eine DNS-Auflösung. Das Flag "-n" deaktiviert diese Auflösung. Es ist nützlich, um fehlerhafte IP-Listen zu erkennen. Beachten Sie, dass bei nicht erreichbarem DNS-Server die HAProxy-Konfigurationsanalyse viele Minuten dauern kann, während auf das Eintreten der Zeitüberschreitung gewartet wird. Während dieser Zeit werden keine Fehlermeldungen angezeigt. Das Flag "-n" deaktiviert dieses Verhalten. Beachten Sie außerdem, dass diese Funktion während der Laufzeit für dynamische ACL-Änderungen deaktiviert ist.

Es gibt jedoch Einschränkungen. Nicht alle Methoden können mit allen Sample-Abrufmethoden verwendet werden. Außerdem muss "-m" vor "-f" stehen, wenn beide gemeinsam verwendet werden. Die Musterabgleichsmethode muss eine der folgenden sein:

- "found": Prüft lediglich, ob das angeforderte Sample im Datenstrom vorhanden ist, vergleicht es jedoch nicht mit einem Muster. Es wird empfohlen, kein Muster anzugeben, um Verwirrung zu vermeiden. Diese Abgleichsmethode ist besonders nützlich, um das Vorhandensein bestimmter Inhalte wie Header, Cookies usw. zu erkennen, auch wenn sie leer sind, ohne sie mit etwas zu vergleichen oder zu zählen.

- "bool": Prüft den Wert als booleschen Wert. Kann nur auf Sample-Abrufe angewendet werden, die einen booleschen oder ganzzahligen Wert zurückgeben, und benötigt kein Muster. Der Wert null oder false liefert keinen Treffer; alle anderen Werte liefern einen Treffer.

- "int": Vergleicht den Wert als Ganzzahl. Kann mit Ganzzahl- und booleschen Samples verwendet werden. Boolesch false entspricht der Ganzzahl 0, boolesch true der Ganzzahl 1.

- "ip": Vergleicht den Wert als IPv4- oder IPv6-Adresse. Ist nur mit IP-Adress-Samples kompatibel, daher implizit und nie erforderlich.

- "bin": Vergleicht den Inhalt mit einer Hexadezimalzeichenkette, die eine Binärsequenz darstellt. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "len": Vergleicht die Länge des Samples als Ganzzahl. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "str": Genauer Abgleich: Vergleicht den Inhalt mit einer Zeichenkette. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "sub": Teilstring-Abgleich: Prüft, ob der Inhalt mindestens eines der bereitgestellten Zeichenkettenmuster enthält. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "reg": Regex-Abgleich: Vergleicht den Inhalt mit einer Liste von regulären Ausdrücken. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "beg": Präfix-Abgleich: Prüft, ob der Inhalt mit einem der bereitgestellten Zeichenkettenmuster beginnt. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "end": Suffix-Abgleich: Prüft, ob der Inhalt mit einem der bereitgestellten Zeichenkettenmuster endet. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "dir": Unterverzeichnis-Abgleich: Prüft, ob ein durch Schrägstriche getrennter Teil des Inhalts exakt mit einem der bereitgestellten Zeichenkettenmuster übereinstimmt. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

- "dom": Domänen-Abgleich: Prüft, ob ein durch Punkte getrennter Teil des Inhalts exakt mit einem der bereitgestellten Zeichenkettenmuster übereinstimmt. Kann mit Binär- oder Zeichenketten-Samples verwendet werden.

Beispielsweise kann die Anwesenheit des Cookies "JSESSIONID" in einer HTTP-Anfrage schnell erkannt werden durch:

```text
acl jsess_present req.cook(JSESSIONID) -m found
```

Um einen regulären Ausdruck auf die ersten 500 Bytes der Daten im Puffer anzuwenden, würde man folgende ACL verwenden:

```text
acl script_tag req.payload(0,500) -m reg -i <script>
```

Auf Systemen, auf denen die Regex-Bibliothek bei Verwendung von "-i" viel langsamer ist, kann das Sample vor dem Abgleich in Kleinbuchstaben konvertiert werden, wie folgt:

```text
acl script_tag req.payload(0,500),lower -m reg <script>
```

Alle ACL-spezifischen Kriterien implizieren eine Standardabgleichsmethode. Meistens bestehen diese Kriterien aus der Verkettung des Namens der ursprünglichen Sample-Abrufmethode und der Abgleichsmethode. Zum Beispiel wendet "hdr_beg" die "beg"-Abgleichsmethode auf Samples an, die mit der "hdr"-Abrufmethode abgerufen wurden. Diese Abgleichsmethode ist nur verwendbar, wenn das Schlüsselwort allein verwendet wird, ohne Konverter. Wird nach einem solchen ACL-Schlüsselwort ein Konverter angewendet, wird die Standardabgleichsmethode dieses ACL-Schlüsselworts einfach ignoriert, da für den Abgleich der Ausgabetyp des letzten Konverters maßgeblich ist. Da alle ACL-spezifischen Kriterien auf einer Sample-Abrufmethode basieren, ist es immer möglich, stattdessen die ursprüngliche Sample-Abrufmethode und die explizite Abgleichsmethode unter Verwendung von "-m" zu verwenden.

Wenn mit "-m" eine alternative Abgleichsmethode für ein ACL-spezifisches Kriterium angegeben wird, wird diese Methode einfach auf die zugrunde liegende Sample-Abrufmethode angewendet. Zum Beispiel sind alle folgenden ACLs exakt äquivalent:

```text
acl short_form  hdr_beg(host)        www.
acl alternate1  hdr_beg(host) -m beg www.
acl alternate2  hdr_dom(host) -m beg www.
acl alternate3  hdr(host)     -m beg www.

```

Die folgende Tabelle fasst die Kompatibilitätsmatrix zwischen Sample- oder Konvertertypen und den Mustertypen, mit denen sie abgeglichen werden können, zusammen. Sie gibt für jede kompatible Kombination den Namen der zu verwendenden Abgleichsmethode an, umgeben von spitzen Klammern "\>" und "\<", wenn die Methode die Standardmethode ist und standardmäßig ohne "-m" funktioniert.

```text
                            +-------------------------------------------------+
                            |             Typ des Eingabe-Samples             |
    +-----------------------+---------+---------+---------+---------+---------+
    |       Mustertyp       | boolean | integer |    ip   |  string |  binary |
    +-----------------------+---------+---------+---------+---------+---------+
    | keiner (nur Existenz) |  found  |  found  |  found  |  found  |  found  |
    +-----------------------+---------+---------+---------+---------+---------+
    |  keiner (bool. Wert)  |>  bool <|   bool  |         |   bool  |         |
    +-----------------------+---------+---------+---------+---------+---------+
    |    Ganzzahl (Wert)    |   int   |>  int  <|   int   |   int   |         |
    +-----------------------+---------+---------+---------+---------+---------+
    |    Ganzzahl (Länge)   |   len   |   len   |   len   |   len   |   len   |
    +-----------------------+---------+---------+---------+---------+---------+
    |       IP-Adresse      |         |         |>   ip  <|    ip   |    ip   |
    +-----------------------+---------+---------+---------+---------+---------+
    |  exakte Zeichenkette  |   str   |   str   |   str   |>  str  <|   str   |
    +-----------------------+---------+---------+---------+---------+---------+
    |         Präfix        |   beg   |   beg   |   beg   |   beg   |   beg   |
    +-----------------------+---------+---------+---------+---------+---------+
    |         Suffix        |   end   |   end   |   end   |   end   |   end   |
    +-----------------------+---------+---------+---------+---------+---------+
    |    Teilzeichenkette   |   sub   |   sub   |   sub   |   sub   |   sub   |
    +-----------------------+---------+---------+---------+---------+---------+
    |    Unterverzeichnis   |   dir   |   dir   |   dir   |   dir   |   dir   |
    +-----------------------+---------+---------+---------+---------+---------+
    |         Domain        |   dom   |   dom   |   dom   |   dom   |   dom   |
    +-----------------------+---------+---------+---------+---------+---------+
    |   regulärer Ausdruck  |   reg   |   reg   |   reg   |   reg   |   reg   |
    +-----------------------+---------+---------+---------+---------+---------+
    |       Hex-Block       |         |         |         |   bin   |   bin   |
    +-----------------------+---------+---------+---------+---------+---------+
```

### 7.1.1. Abgleich boolescher Werte {#section-7-1-1}

Für den Abgleich eines booleschen Werts ist kein Vergleichswert erforderlich; alle angegebenen Werte werden ignoriert. Der boolesche Abgleich wird standardmäßig für alle Abrufmethoden vom Typ "boolean" verwendet. Dabei wird der abgerufene Wert unverändert zurückgegeben: Der boolesche Wert "true" liefert immer einen Treffer, "false" niemals.

Der boolesche Abgleich kann auch mit "-m bool" für Abrufmethoden erzwungen werden, die einen ganzzahligen Wert zurückgeben. Dabei wird der Ganzzahlwert 0 in den booleschen Wert "false" umgewandelt, alle anderen Werte in "true".

### 7.1.2. Abgleich von Ganzzahlen {#section-7-1-2}

Der Ganzzahlabgleich wird standardmäßig für Abrufmethoden verwendet, die Ganzzahlen zurückgeben. Er kann mit "-m int" auch für boolesche Abrufe erzwungen werden. Dabei wird "false" in die Ganzzahl 0 und "true" in die Ganzzahl 1 umgewandelt.

Der Ganzzahlabgleich unterstützt außerdem Ganzzahlbereiche und Operatoren. Er ist nur auf positive Werte anwendbar. Ein Bereich wird durch eine Unter- und eine Obergrenze ausgedrückt, die durch einen Doppelpunkt getrennt sind; beide Grenzen können jeweils weggelassen werden.

Beispielsweise ist "1024:65535" ein gültiger Bereich für nicht privilegierte Ports; auch "1024:" funktioniert. "0:1023" ist eine gültige Darstellung privilegierter Ports; auch ":1023" funktioniert.

Als Sonderfall unterstützen einige ACL-Funktionen Dezimalzahlen, die tatsächlich aus zwei durch einen Punkt getrennten Ganzzahlen bestehen. Dies wird beispielsweise für bestimmte Versionsprüfungen verwendet. Alle Eigenschaften des Ganzzahlabgleichs gelten auch für diese Dezimalzahlen, einschließlich Bereichen und Operatoren.

Zur einfacheren Verwendung werden auch Vergleichsoperatoren unterstützt. Operatoren mit Bereichen zu verwenden, ist kaum sinnvoll; davon wird dringend abgeraten. Ebenso ist es kaum sinnvoll, Größenvergleiche mit einer Menge von Werten durchzuführen.

Für den Ganzzahlabgleich stehen folgende Operatoren zur Verfügung:

```text
eq: wahr, wenn der geprüfte Wert mindestens einem Wert entspricht
ge: wahr, wenn der geprüfte Wert größer oder gleich mindestens einem Wert ist
gt: wahr, wenn der geprüfte Wert größer als mindestens ein Wert ist
le: wahr, wenn der geprüfte Wert kleiner oder gleich mindestens einem Wert ist
lt: wahr, wenn der geprüfte Wert kleiner als mindestens ein Wert ist
```

Die folgende ACL trifft beispielsweise auf jeden negativen Content-Length-Header zu:

```text
acl negative-length req.hdr_val(content-length) lt 0
```

Die folgende ACL trifft auf SSL-Versionen zwischen 3.0 und 3.1 einschließlich der Grenzen zu:

```text
acl sslv3 req.ssl_ver 3:3.1
```

### 7.1.3. Abgleich von Zeichenketten {#section-7-1-3}

Der Zeichenkettenabgleich ist auf Abrufmethoden für Zeichenketten oder Binärdaten anwendbar und steht in 6 verschiedenen Formen zur Verfügung:

- exakter Abgleich (-m str): Die extrahierte Zeichenkette muss exakt mit den Mustern übereinstimmen;

- Teilzeichenkettenabgleich (-m sub): Die Muster werden in der extrahierten Zeichenkette gesucht. Die ACL trifft zu, wenn eines davon darin gefunden wird;

- Präfixabgleich (-m beg): Die Muster werden mit dem Anfang der extrahierten Zeichenkette verglichen. Die ACL trifft zu, wenn eines davon übereinstimmt.

- Suffixabgleich (-m end): Die Muster werden mit dem Ende der extrahierten Zeichenkette verglichen. Die ACL trifft zu, wenn eines davon übereinstimmt.

- Unterverzeichnisabgleich (-m dir): Die Muster werden an beliebiger Stelle in der extrahierten Zeichenkette gesucht, begrenzt durch Schrägstriche ("/"), den Anfang oder das Ende der Zeichenkette. Die ACL trifft zu, wenn eines davon übereinstimmt. Die Zeichenkette "/images/png/logo/32x32.png" würde somit auf "/images", "/images/png", "images/png", "/png/logo", "logo/32x32.png" oder "32x32.png" passen, aber weder auf "png" noch auf "32x32".

- Domainabgleich (-m dom): Die Muster werden an beliebiger Stelle in der extrahierten Zeichenkette gesucht, begrenzt durch Punkte ("."), Doppelpunkte (":"), Schrägstriche ("/"), Fragezeichen ("?"), den Anfang oder das Ende der Zeichenkette. Dies ist für URLs vorgesehen. Führende und nachgestellte Trennzeichen im Muster werden ignoriert. Die ACL trifft zu, wenn eines der Muster übereinstimmt. In der Beispielzeichenkette "<http://www1.dc-eu.example.com:80/blah>" würden somit die Muster "http", "www1", ".www1", "dc-eu", "example", "com", "80", "dc-eu.example", "blah", ":www1:" und "dc-eu.example:80" passen, aber weder "eu" noch "dc". Domain-Suffixe zum Filtern oder für das Routing auf diese Weise abzugleichen, ist im Allgemeinen keine gute Idee: Das Routing ließe sich beispielsweise leicht täuschen, indem das passende Präfix einer anderen Domain vorangestellt wird.

Beim Zeichenkettenabgleich werden Zeichenketten so verwendet, wie sie übergeben werden. Eine Ausnahme bildet der Backslash ("&#92;"), mit dem bestimmte Zeichen wie Leerzeichen maskiert werden können.
Wenn das Flag "-i" vor der ersten Zeichenkette übergeben wird, erfolgt der Abgleich ohne Berücksichtigung der Groß-/Kleinschreibung. Um die Zeichenkette "-i" abzugleichen, diese entweder an zweiter Stelle angeben oder das Flag "--" vor der ersten Zeichenkette übergeben. Dasselbe gilt selbstverständlich für den Abgleich der Zeichenkette "--".

Für Binärabrufe, die Nullbytes (0x00) enthalten können, keinen Zeichenkettenabgleich verwenden, da der Vergleich beim ersten Nullbyte endet. Stattdessen den Binärabruf zunächst mit dem Konverter hex in eine Hexadezimalzeichenkette umwandeln.

Beispiel:

```shell
# matches if the string <tag> is present in the binary sample
acl tag_found req.payload(0,0),hex -m sub 3C7461673E
```

### 7.1.4. Abgleich mit regulären Ausdrücken (Regex) {#section-7-1-4}

Wie beim Zeichenkettenabgleich werden auch beim Abgleich mit regulären Ausdrücken die Zeichenketten so verwendet, wie sie übergeben werden. Eine Ausnahme bildet der Backslash ("&#92;"), mit dem bestimmte Zeichen wie Leerzeichen maskiert werden können. Wenn das Flag "-i" vor dem ersten regulären Ausdruck übergeben wird, erfolgt der Abgleich ohne Berücksichtigung der Groß-/Kleinschreibung. Um die Zeichenkette "-i" abzugleichen, diese entweder an zweiter Stelle angeben oder das Flag "--" vor der ersten Zeichenkette übergeben. Dasselbe Prinzip gilt selbstverständlich für den Abgleich der Zeichenkette "--".

### 7.1.5. Abgleich beliebiger Datenblöcke {#section-7-1-5}

Extrahierte Samples können mit einem Binärblock abgeglichen werden, der sich nicht zuverlässig als Zeichenkette darstellen lässt. Dazu müssen die Muster bei binärer Abgleichsmethode als Folge einer geraden Anzahl hexadezimaler Ziffern übergeben werden. Je zwei Ziffern stellen ein Byte dar. Hexadezimale Ziffern können in Groß- oder Kleinschreibung angegeben werden.

Beispiel:

```shell
# match "Hello\n" in the input stream (\x48 \x65 \x6c \x6c \x6f \x0a)
acl hello req.payload(0,6) -m bin 48656c6c6f0a
```

### 7.1.6. Abgleich von IPv4- und IPv6-Adressen {#section-7-1-6}

IPv4-Adressen können entweder als reine Adressen oder mit angehängter Netzmaske angegeben werden. Im zweiten Fall trifft der Abgleich zu, wenn die IPv4-Adresse innerhalb des Netzwerks liegt. Reine Adressen können auch durch einen auflösbaren Hostnamen ersetzt werden. Davon wird jedoch generell abgeraten, da Konfigurationen dadurch schwerer zu lesen und zu debuggen sind. Werden Hostnamen verwendet, sollte zumindest sichergestellt werden, dass sie in /etc/hosts stehen, damit die Konfiguration nicht von einem zufälligen DNS-Ergebnis zum Zeitpunkt des Einlesens abhängt.

Die durch Punkte getrennte IPv4-Notation wird sowohl in der üblichen Form als auch in einer verkürzten Form unterstützt, bei der nur aus 0 bestehende Oktette weggelassen werden:

```text
    +----------------+-------------+-------------+
    | Beispiel 1     | Beispiel 2  | Beispiel 3  |
    +----------------+-------------+-------------+
    | 192.168.0.1    | 10.0.0.12   | 127.0.0.1   |
    | 192.168.1      | 10.12       | 127.1       |
    | 192.168.0.1/22 | 10.0.0.12/8 | 127.0.0.1/8 |
    | 192.168.1/22   | 10.12/8     | 127.1/8     |
    +----------------+-------------+-------------+
```

Dies unterscheidet sich von der CIDR-Adressnotation nach RFC 4632, in der 192.168.42/24 gleichbedeutend mit 192.168.42.0/24 wäre.

IPv6-Adressen können in ihrer üblichen Form mit oder ohne angehängte Netzmaske eingegeben werden. Für IPv6-Netzmasken sind nur Bitanzahlen zulässig. Um Probleme mit zufällig aufgelösten IP-Adressen auszuschließen, sind Hostnamen in IPv6-Mustern niemals erlaubt.

HAProxy kann in den folgenden Fällen auch IPv4-Adressen mit IPv6-Adressen abgleichen:

- Die geprüfte Adresse ist IPv4, die Musteradresse ebenfalls IPv4: Der Abgleich erfolgt in IPv4 unter Verwendung der angegebenen Maske, sofern vorhanden.
- Die geprüfte Adresse ist IPv6, die Musteradresse ebenfalls IPv6: Der Abgleich erfolgt in IPv6 unter Verwendung der angegebenen Maske, sofern vorhanden.
- Die geprüfte Adresse ist IPv6, die Musteradresse IPv4: Der Abgleich erfolgt in IPv4 mit der Maske des Musters, wenn die IPv6-Adresse auf 2002:IPV4::, ::IPV4 oder ::ffff:IPV4 passt. Andernfalls schlägt er fehl.
- Die geprüfte Adresse ist IPv4, die Musteradresse IPv6: Zuerst wird die IPv4-Adresse durch Voranstellen von ::ffff: in IPv6 umgewandelt. Anschließend erfolgt der Abgleich in IPv6 mit der angegebenen IPv6-Maske.

## 7.2. Bedingungen aus ACLs bilden {#section-7-2}

Einige Aktionen werden nur ausgeführt, wenn eine Bedingung erfüllt ist. Eine Bedingung besteht aus einer Kombination von ACLs mit Operatoren. Es werden 3 Operatoren unterstützt:

- AND (implizit)
- OR (explizit mit dem Schlüsselwort "or" oder dem Operator "\|\|")
- Negation mit dem Ausrufezeichen ("!")

Eine Bedingung wird in disjunktiver Form gebildet:

```text
[!]acl1 [!]acl2 ... [!]acln  { or [!]acl1 [!]acl2 ... [!]acln } ...
```

Solche Bedingungen werden im Allgemeinen nach einer "if"- oder "unless"-Anweisung verwendet. Sie geben an, wann die Bedingung die Aktion auslöst.

Beispielsweise lassen sich HTTP-Anfragen an die URL "\*" mit anderen Methoden als "OPTIONS" blockieren, ebenso POST-Anfragen ohne content-length, GET- oder HEAD-Anfragen mit einem content-length größer als 0 und schließlich alle Anfragen, die weder GET/HEAD/POST/OPTIONS sind!

```haproxy
acl missing_cl req.hdr_cnt(Content-length) eq 0
http-request deny if HTTP_URL_STAR !METH_OPTIONS || METH_POST missing_cl
http-request deny if METH_GET HTTP_CONTENT
http-request deny unless METH_GET or METH_POST or METH_OPTIONS
```

Um ein anderes Backend für Anfragen nach statischen Inhalten auf der Website "www" sowie für jede Anfrage an die Hosts "img", "video", "download" und "ftp" auszuwählen:

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
acl host_www    hdr_beg(host) -i www
acl host_static hdr_beg(host) -i img. video. download. ftp.
```

```haproxy
# now use backend "static" for all static-only hosts, and for static URLs
# of host "www". Use backend "www" for the rest.
use_backend static if host_static or host_www url_static
use_backend www    if host_www
```

Regeln können auch mit „anonymen ACLs“ gebildet werden. Dies sind unbenannte ACL-Ausdrücke, die bei Bedarf erstellt werden, ohne zuvor deklariert werden zu müssen. Sie müssen in geschweifte Klammern eingeschlossen werden, wobei vor und hinter jeder Klammer ein Leerzeichen stehen muss, damit die Klammern als eigenständige Wörter erkannt werden. Beispiel:

```text
Die folgende Regel:

    acl missing_cl req.hdr_cnt(Content-length) eq 0
    http-request deny if METH_POST missing_cl

kann auch so geschrieben werden:

    http-request deny if METH_POST { req.hdr_cnt(Content-length) eq 0 }
```

Von dieser Schreibweise wird generell abgeraten, da sich damit viel leichter Fehler in die Konfiguration einschleichen. Bei sehr einfachen Regeln, die beispielsweise nur eine Quell-IP-Adresse abgleichen, kann ihre Verwendung jedoch sinnvoller sein als das Deklarieren von ACLs mit beliebigen Namen. Ein weiteres Beispiel für eine sinnvolle Verwendung:

```text
Mit benannten ACLs:

     acl site_dead nbsrv(dynamic) lt 2
     acl site_dead nbsrv(static)  lt 2
     monitor fail  if site_dead

Mit anonymen ACLs:

     monitor fail if { nbsrv(dynamic) lt 2 } || { nbsrv(static) lt 2 }
```

Ausführliche Hilfe zu den Schlüsselwörtern "http-request deny" und "use_backend" finden Sie in [Abschnitt 4.2](/de/haproxy/proxies/#section-4-2).

## 7.3. Sample-Abrufe {#section-7-3}

Ursprünglich dienten Sample-Abrufmethoden nur dazu, Daten abzurufen und mit ACLs gegen Muster abzugleichen. Mit der Einführung von Stick Tables entstand eine neue Klasse von Sample-Abrufmethoden, deren Syntax meist derjenigen ihrer ACL-Entsprechung gleicht. Diese Sample-Abrufmethoden werden auch „Abrufe“ genannt. Inzwischen sind ACLs und Abrufe zusammengewachsen: Alle ACL-Abrufmethoden stehen auch als allgemeine Abrufmethoden zur Verfügung, und ACLs können ihrerseits jede Sample-Abrufmethode verwenden.

Dieser Abschnitt beschreibt alle verfügbaren Sample-Abrufmethoden und deren Ausgabetyp. Einige Sample-Abrufmethoden besitzen veraltete Aliase, um die Kompatibilität mit bestehenden Konfigurationen zu erhalten. Diese sind ausdrücklich als veraltet gekennzeichnet und sollten in neuen Installationen nicht verwendet werden.

Samples sind typisiert. Der Typ eines Samples bestimmt, mit welchen Mustern es abgeglichen werden kann, welche Konverter darauf angewendet werden können und wie es umgewandelt wird, wenn ein anderer Typ erwartet wird. Folgende Typen werden verwendet:

- boolean: ein wahrer oder falscher Wert, wie ihn Abrufmethoden zurückgeben, die nur eine Bedingung melden. Solche Samples werden ohne die Option "-m" abgeglichen. Eine Ganzzahl gilt als wahr, wenn sie nicht null ist; eine Zeichenfolge wird zunächst als Ganzzahl eingelesen.

- integer: eine vorzeichenbehaftete 64-Bit-Ganzzahl, also ein Wert zwischen -2^63 und 2^63-1 (-9223372036854775808 und 9223372036854775807). Bei der Umwandlung einer Zeichenfolge in eine Ganzzahl endet die Konvertierung am ersten Zeichen, das keine Ziffer und kein führendes Vorzeichen ('+' oder '-') ist. Verwendet wird der Wert der eingelesenen Ziffern; ohne Ziffern ist er null, leere Zeichenfolgen können jedoch nicht umgewandelt werden. Werte außerhalb des darstellbaren Bereichs werden auf die kleinste oder größte darstellbare Ganzzahl begrenzt.

- IPv4-Adresse und IPv6-Adresse: Dies sind zwei unterschiedliche Typen, obwohl die meisten Stellen, die einen davon akzeptieren, auch den anderen akzeptieren und einfach als Stellen für eine Adresse dokumentiert sind. Eine IPv4-Adresse kann in eine Ganzzahl umgewandelt werden, die dem 32-Bit-Wert der Adresse entspricht, oder in eine IPv6-Adresse in IPv4-mapped-Form ("::ffff:a.b.c.d"). Die umgekehrten Konvertierungen sind eingeschränkter: Für eine IPv6-Adresse gibt es keine Ganzzahldarstellung, und sie kann nur dann in eine IPv4-Adresse umgewandelt werden, wenn es sich um eine IPv4-mapped-, IPv4-compatible- oder 6to4-Adresse handelt.

- string: eine Folge von Bytes, die am ersten NUL-Zeichen (0x00) endet; dieses gehört nicht zur Zeichenfolge. Wenn ein eingebettetes NUL-Zeichen benötigt wird, ist der Typ binary zu verwenden. Es wird keine Kodierung angenommen: HAProxy versucht nicht, diese Bytes als Zeichen zu interpretieren. Ob sie überhaupt Text darstellen, in welchem Zeichensatz und wie sie angezeigt werden, hängt allein von der Verwendung der Zeichenfolge ab. Die explizite oder implizite Umwandlung eines binary-Samples in eine Zeichenfolge verwirft daher stillschweigend alles ab dem ersten NUL-Zeichen.

- binary: ein Block von Bytes bekannter Länge; jedes Byte kann jeden Wert von 0 bis 255 einschließlich NUL annehmen. Diesen Typ liefern Abrufmethoden für Rohdaten, etwa einen Anfrage-Body oder den Inhalt eines Binärprotokolls. Ein solches Sample kann weder in boolean noch in eine Ganzzahl oder eine Adresse umgewandelt werden. Es muss entweder mit "-m bin" als Binärblock abgeglichen werden (siehe [Abschnitt 7.1.5](/de/haproxy/acls-and-samples/#section-7-1-5)) oder zunächst in eine druckbare Form umgewandelt werden, etwa mit dem Konverter "hex". Die umgekehrte Konvertierung ist uneingeschränkt möglich, da eine Zeichenfolge immer ein gültiger Binärblock ist.

- method: eine HTTP-Methode. HAProxy bekannte Methoden werden durch einen Bezeichner dargestellt; die anderen behalten ihre ursprüngliche Zeichenfolge.

Die folgende Konvertertabelle verwendet außerdem "any" für Konverter, die jeden Eingabetyp akzeptieren.

Sofern vorhanden, werden auch die ACL-Varianten mit ihren jeweiligen Abgleichsmethoden angegeben. Sie besitzen alle eine klar definierte Standardmethode zum Musterabgleich. Daher ist es nie erforderlich, mit der Option "-m" anzugeben, wie das Sample mit ACLs abgeglichen werden soll; zulässig ist es jedoch.

Wie die obige Kompatibilitätsmatrix zwischen Sample-Typ und Abgleichsmethode zeigt, ist bei Verwendung einer allgemeinen Sample-Abrufmethode in einer ACL die Option "-m" zwingend erforderlich, sofern das Sample nicht vom Typ boolean, integer, IPv4 oder IPv6 ist. Existiert dasselbe Schlüsselwort sowohl als ACL-Schlüsselwort als auch als Standardabrufmethode, wählt die ACL-Engine standardmäßig automatisch die reine ACL-Variante.

Einige dieser Schlüsselwörter unterstützen ein oder mehrere Pflichtargumente sowie ein oder mehrere optionale Argumente. Diese Argumente sind streng typisiert und werden beim Einlesen der Konfiguration geprüft, damit kein Betrieb mit einem fehlerhaften Argument möglich ist, etwa einem nicht aufgelösten Backend-Namen. Argumente von Abruffunktionen werden in runden Klammern übergeben und durch Kommas getrennt. Optionale Argumente sind im Folgenden durch eckige Klammern ('[ ]') gekennzeichnet. Sind alle Argumente optional, können die runden Klammern entfallen.

Die Syntax einer Standard-Sample-Abrufmethode hat somit eine der folgenden Formen:

- name
- name(arg1)
- name(arg1,arg2)

### 7.3.1. Konverter {#section-7-3-1}

Sample-Abrufmethoden können mit Transformationen kombiniert werden, die auf das abgerufene Sample angewendet werden und auch „Konverter“ heißen. Diese Kombinationen bilden sogenannte „Sample-Ausdrücke“; das Ergebnis ist ein „Sample“. Anfangs wurde dies nur von den Direktiven "stick on" und "stick store-request" unterstützt. Inzwischen wurde die Unterstützung auf alle Stellen ausgeweitet, an denen Samples verwendet werden können (ACLs, log-format, unique-id-format, add-header, ...).

Diese Transformationen werden als Folge bestimmter Schlüsselwörter nach der Sample-Abrufmethode aufgeführt. Sie können auch unmittelbar nach dem Argument des Abrufschlüsselworts angehängt werden, jeweils durch ein Komma getrennt. Die Schlüsselwörter können ihrerseits Argumente unterstützen, etwa eine Netzmaske, die in runden Klammern übergeben werden müssen.

Eine bestimmte Gruppe von Konvertern bilden bitweise und arithmetische Operatoren, mit denen sich Grundoperationen auf Ganzzahlen ausführen lassen. Unterstützt werden einige bitweise Operationen (and, or, xor, cpl) und einige arithmetische Operationen (add, sub, mul, div, mod, neg). Einige Vergleichsoperatoren (odd, even, not, bool) ermöglichen es, einen Treffer zu melden, ohne dafür eine ACL schreiben zu müssen.

Die folgenden Schlüsselwörter werden unterstützt:

```text
   Schlüsselwort                                   Eingabetyp   Ausgabetyp
------------------------------------------------+-------------+----------------
51d.single(prop[,prop*])                           string       string
add(value)                                         integer      integer
add_item(delim[,var[,suff]])                       string       string
aes_cbc_dec(bits,nonce,key[,<aad>])                binary       binary
aes_cbc_enc(bits,nonce,key[,<aad>])                binary       binary
aes_gcm_dec(bits,nonce,key,aead_tag[,aad])         binary       binary
aes_gcm_enc(bits,nonce,key,aead_tag[,aad])         binary       binary
and(value)                                         integer      integer
b64dec                                             string       binary
base2                                              binary       string
base64                                             binary       string
be2dec(separator,chunk_size[,truncate])            binary       string
le2dec(separator,chunk_size[,truncate])            binary       string
be2hex([separator[,chunk_size[,truncate]]])        binary       string
bool                                               integer      boolean
bytes(offset[,length])                             binary       binary
capture-req(id)                                    string       string
capture-res(id)                                    string       string
concat([start[,var[,end]]])                        string       string
cpl                                                integer      integer
crc32([avalanche])                                 binary       integer
crc32c([avalanche])                                binary       integer
cut_crlf                                           string       string
da-csv-conv(prop[,prop*])                          string       string
date                                               string       integer
debug([prefix][,destination])                       any          same
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
digest(algorithm)                                  binary       binary
div(value)                                         integer      integer
djb2([avalanche])                                  binary       integer
eth.data                                           binary       binary
eth.dst                                            binary       binary
eth.hdr                                            binary       binary
eth.proto                                          binary       integer
eth.src                                            binary       binary
eth.vlan                                           binary       integer
even                                               integer      boolean
fe_exists                                          string       boolean
field(index,delimiters[,count])                    string       string
fix_is_valid                                       binary       boolean
fix_tag_value(tag)                                 binary       binary
has_ctl([mask])                                    binary       boolean
hex                                                binary       string
hex2i                                              binary       integer
hmac(algorithm,key)                                binary       binary
host_only                                          string       string
htonl                                              integer      integer
http_date([offset[,unit]])                         integer      string
iif(true,false)                                    boolean      string
in_table([table])                                  any          boolean
ip.data                                            binary       binary
ip.df                                              binary       integer
ip.dst                                             binary       address
ip.fp                                              binary       binary
ip.hdr                                             binary       binary
ip.proto                                           binary       integer
ip.src                                             binary       address
ip.tos                                             binary       integer
ip.ttl                                             binary       integer
ip.ver                                             binary       integer
ipmask(mask4[,mask6])                              address      address
json([input-code])                                 string       string
json_query(json_path[,output_type])                string       _outtype_
jwt_decrypt_jwk(<jwk>)                             string       binary
jwt_decrypt_cert(<cert>)                           string       binary
jwt_decrypt_secret(<secret>)                       string       binary
jwt_header_query([json_path[,output_type]])        string       string
jwt_payload_query([json_path[,output_type]])       string       string
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
jwt_verify(alg,key)                                string       integer
jwt_verify_cert(alg,cert)                          string       integer
language(value[,default])                          string       string
length                                             string       integer
lower                                              string       string
ltime(format[,offset])                             integer      string
ltrim(chars)                                       string       string
map(map_name[,default_value])                      string       string
map_match(map_name[,default_value])                _match_      string
map_match_output(map_name[,default_value])         _match_      _output_
mod(value)                                         integer      integer
mqtt_field_value(pkt_type,fieldname_or_prop_ID)    binary       binary
mqtt_is_valid                                      binary       boolean
ms_ltime(format[,offset])                          integer      string
ms_utime(format[,offset])                          integer      string
mul(value)                                         integer      integer
nbsrv                                              string       integer
neg                                                integer      integer
not                                                integer      boolean
odd                                                integer      boolean
or(value)                                          integer      integer
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
param(name[,delim])                                string       string
port_only                                          string       integer
protobuf(field_number[,field_type])                binary       binary
regsub(regex,subst[,flags])                        string       string
reverse                                            string       string
reverse_dom                                        string       string
rfc7239_field(field)                               string       string
rfc7239_is_valid                                   string       boolean
rfc7239_n2nn                                       string       address / str
rfc7239_n2np                                       string       integer / str
rfc7239_nn                                         address/str  string
rfc7239_np                                         integer/str  string
rtrim(chars)                                       string       string
sdbm([avalanche])                                  binary       integer
secure_memcmp(var)                                 string       boolean
set-var(var[,cond...])                              any          same
sha1                                               binary       binary
sha2([bits])                                       binary       binary
srv_is_up                                          string       boolean
srv_queue                                          string       integer
strcmp(var)                                        string       boolean
sub(value)                                         integer      integer
table_bytes_in_rate([table])                       any          integer
table_bytes_out_rate([table])                      any          integer
table_clr_gpc(idx[,table])                         any          integer
table_clr_gpc0([table])                            any          integer
table_clr_gpc1([table])                            any          integer
table_conn_cnt([table])                            any          integer
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
table_conn_cur([table])                            any          integer
table_conn_rate([table])                           any          integer
table_expire([table[,default_value]])              any          integer
table_glitch_cnt([table])                          any          integer
table_glitch_rate([table])                         any          integer
table_gpc(idx[,table])                             any          integer
table_gpc0([table])                                any          integer
table_gpc0_rate([table])                           any          integer
table_gpc1([table])                                any          integer
table_gpc1_rate([table])                           any          integer
table_gpc_rate(idx[,table])                        any          integer
table_gpt(idx[,table])                             any          integer
table_gpt0([table])                                any          integer
table_http_err_cnt([table])                        any          integer
table_http_err_rate([table])                       any          integer
table_http_fail_cnt([table])                       any          integer
table_http_fail_rate([table])                      any          integer
table_http_req_cnt([table])                        any          integer
table_http_req_rate([table])                       any          integer
table_idle([table[,default_value]])                any          integer
table_inc_gpc(idx[,table])                         any          integer
table_inc_gpc0([table])                            any          integer
table_inc_gpc1([table])                            any          integer
table_kbytes_in([table])                           any          integer
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
table_kbytes_out([table])                          any          integer
table_server_id([table])                           any          integer
table_sess_cnt([table])                            any          integer
table_sess_rate([table])                           any          integer
table_trackers([table])                            any          integer
tcp.dst                                            binary       integer
tcp.flags                                          binary       integer
tcp.options.mss                                    binary       integer
tcp.options.sack                                   binary       integer
tcp.options.tsopt                                  binary       integer
tcp.options.tsval                                  binary       integer
tcp.options.wscale                                 binary       integer
tcp.options.wsopt                                  binary       integer
tcp.options_list                                   binary       binary
tcp.seq                                            binary       integer
tcp.src                                            binary       integer
tcp.win                                            binary       integer
ub64dec                                            string       string
ub64enc                                            string       string
ungrpc(field_number[,field_type])                  binary       binary / int
unset-var(var)                                      any          same
upper                                              string       string
url_dec([in_form])                                 string       string
url_enc([enc_type])                                string       string
us_ltime(format[,offset])                          integer      string
us_utime(format[,offset])                          integer      string
utime(format[,offset])                             integer      string
when(condition)                                     any          same
word(index,delimiters[,count])                     string       string
wt6([avalanche])                                   binary       integer
x509_v_err_str                                     integer      string
xor(value)                                         integer      integer
-- Schlüsselwort -------------------------------+- Eingabetyp + Ausgabetyp -
xxh3([seed])                                       binary       integer
xxh32([seed])                                      binary       integer
xxh64([seed])                                      binary       integer
```

Es folgt die ausführliche Liste der Konverterschlüsselwörter:

<a id="entry-7-3-1-51d-single"></a>

**`51d.single(<prop>[,<prop>*])`**

```haproxy
51d.single(<prop>[,<prop>*])
```

Gibt die Werte der angeforderten Eigenschaften als Zeichenkette zurück. Die Werte werden durch das mit "51degrees-property-separator" angegebene Trennzeichen getrennt. Das Gerät wird anhand des an den Konverter übergebenen User-Agent-Headers erkannt. Der Funktion können bis zu fünf Eigenschaftsnamen übergeben werden. Wird ein Eigenschaftsname nicht gefunden, wird der Wert "NoData" zurückgegeben.

Beispiel:

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request,
# containing values for the three properties requested by using the
# User-Agent passed to the converter.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[req.fhdr(User-Agent),51d.single(DeviceType,IsMobile,IsTablet)]
```

<a id="entry-7-3-1-add"></a>

**`add(<value>)`**

```haproxy
add(<value>)
```

Addiert `<value>` zum Eingabewert vom Typ vorzeichenbehaftete Ganzzahl und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. `<value>` kann ein Zahlenwert oder ein Variablenname sein. Einzelheiten zu Variablen finden Sie in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-add-item"></a>

**`add_item(<delim>[,<var>[,<suff>]])`**

```haproxy
add_item(<delim>[,<var>[,<suff>]])
```

Hängt mindestens 2 und höchstens 3 Felder an das aktuelle Sample an, das dabei in eine Zeichenkette umgewandelt wird. Das erste Feld, `<delim>`, ist eine konstante Zeichenkette. Sie wird unmittelbar an das vorhandene Sample angehängt, wenn dieses nicht leer ist und entweder `<var>` oder `<suff>` nicht leer ist. Das zweite Feld, `<var>`, ist ein Variablenname. Die Variable wird nachgeschlagen, ihr Inhalt in eine Zeichenkette umgewandelt und unmittelbar an den Teil `<delim>` angehängt. Wird die Variable nicht gefunden, wird nichts angehängt. Sie ist optional; ihr kann außerdem eine konstante Zeichenkette `<suff>` folgen. Wird `<var>` jedoch weggelassen, ist `<suff>` zwingend erforderlich. Dieser Konverter ähnelt dem Konverter concat und kann neue Variablen aus einer Folge anderer Variablen bilden. Der wesentliche Unterschied besteht darin, dass er prüft, ob das Hinzufügen eines Trennzeichens sinnvoll ist. Dies wäre beispielsweise bei einem leeren aktuellen Sample nicht der Fall. Mit dem Konverter concat wären dafür 2 getrennte Regeln nötig, wobei die erste vor dem Hinzufügen eines Trennzeichens prüfen müsste, ob die aktuelle Sample-Zeichenkette leer ist. Werden Kommas oder schließende Klammern als Trennzeichen benötigt, müssen sie durch Anführungszeichen oder Backslashes geschützt werden. Diese müssen ihrerseits geschützt werden, damit der Parser der ersten Ebene sie nicht entfernt; siehe [Abschnitt 2.2](/de/haproxy/configuration-basics/#section-2-2) zu Anführungszeichen und Maskierung. Beispiele folgen unten.

Beispiel:

```text
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1,"(site1)") if src,in_table(site1)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score2,"(site2)") if src,in_table(site2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score3,"(site3)") if src,in_table(site3)'
http-request set-header x-tagged %[var(req.tagged)]

http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1),add_item(",",req.score2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",,(site1))' if src,in_table(site1)
```

<a id="entry-7-3-1-aes-cbc-dec"></a>

**`aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])
```

Entschlüsselt die Eingabe aus Rohbytes je nach Parameter `<bits>` mit dem Algorithmus AES128-CBC, AES192-CBC oder AES256-CBC. Alle anderen Parameter müssen base64-kodiert sein; das Ergebnis wird als Rohbytes zurückgegeben. Der Parameter `<aad>` ist optional. Schlägt die Prüfung von `<aad>` fehl, gibt der Konverter keine Daten zurück. `<nonce>`, `<key>` und `<aad>` können Zeichenketten oder Variablen sein. Dieser Konverter benötigt mindestens OpenSSL 1.0.1.

Beispiel:

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_cbc_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-cbc-enc"></a>

**`aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])
```

Verschlüsselt die Eingabe aus Rohbytes je nach Parameter `<bits>` mit dem Algorithmus AES128-CBC, AES192-CBC oder AES256-CBC. Die Parameter `<nonce>`, `<key>` und `<aad>` müssen base64-kodiert sein. Der Parameter `<aad>` ist optional. Das Ergebnis wird als Rohbytes zurückgegeben. `<nonce>`, `<key>` und `<aad>` können Zeichenketten oder Variablen sein. Dieser Konverter benötigt mindestens OpenSSL 1.0.1.

Beispiel:

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_cbc_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-gcm-dec"></a>

**`aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

Entschlüsselt die Eingabe aus Rohbytes je nach Parameter `<bits>` mit dem Algorithmus AES128-GCM, AES192-GCM oder AES256-GCM. Alle anderen Parameter müssen base64-kodiert sein; das Ergebnis wird als Rohbytes zurückgegeben. Schlägt die Prüfung von `<aead_tag>` oder `<aad>` fehl, gibt der Konverter keine Daten zurück. Der Parameter `<aad>` ist optional. `<nonce>`, `<key>`, `<aead_tag>` und `<aad>` können Zeichenketten oder Variablen sein. Dieser Konverter benötigt mindestens OpenSSL 1.0.1.

Beispiel:

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_gcm_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-aes-gcm-enc"></a>

**`aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

Verschlüsselt die Eingabe aus Rohbytes je nach Parameter `<bits>` mit dem Algorithmus AES128-GCM, AES192-GCM oder AES256-GCM. Die Parameter `<nonce>`, `<key>` und `<aad>` müssen base64-kodiert sein. Der Parameter `<aead_tag>` muss eine Variable sein. Das AEAD-Tag wird base64-kodiert in dieser Variablen gespeichert. Der Parameter `<aad>` ist optional. Das Ergebnis wird als Rohbytes zurückgegeben. `<nonce>`, `<key>` und `<aad>` können Zeichenketten oder Variablen sein. Dieser Konverter benötigt mindestens OpenSSL 1.0.1.

Beispiel:

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_gcm_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-and"></a>

**`and(<value>)`**

```haproxy
and(<value>)
```

Führt eine bitweise "AND"-Verknüpfung zwischen `<value>` und dem Eingabewert vom Typ vorzeichenbehaftete Ganzzahl aus und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. `<value>` kann ein Zahlenwert oder ein Variablenname sein. Einzelheiten zu Variablen finden Sie in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-b64dec"></a>

**`b64dec`**

```haproxy
b64dec
```

Wandelt eine base64-kodierte Eingabezeichenkette in ihre Binärdarstellung um (Dekodierung). Dies ist die Umkehrung von base64(). Zur Variante base64url ("URL and Filename Safe Alphabet" (RFC 4648)) siehe "ub64dec".

<a id="entry-7-3-1-base2"></a>

**`base2`**

```haproxy
base2
```

Wandelt ein binäres Eingabe-Sample in eine binäre Zeichenkette mit acht Binärziffern je Eingabebyte um. Damit lässt sich der Abgleich mit dem längsten passenden Präfix auch für Typen durchführen, deren native Darstellung keinen Präfixabgleich erlaubt, beispielsweise für IP-Präfixe.

<a id="entry-7-3-1-base64"></a>

**`base64`**

```haproxy
base64
```

Wandelt ein binäres Eingabe-Sample in eine base64-Zeichenkette um. Damit lassen sich binäre Inhalte in einer zuverlässig übertragbaren Form protokollieren oder übertragen; beispielsweise kann eine SSL-ID in einen Header kopiert werden. Zur Variante base64url ("URL and Filename Safe Alphabet" (RFC 4648)) siehe "ub64enc".

<a id="entry-7-3-1-be2dec"></a>

**`be2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
be2dec(<separator>,<chunk_size>[,<truncate>])
```

Wandelt ein binäres Eingabe-Sample im Big-Endian-Format in eine Zeichenkette um, die je `<chunk_size>` Eingabebytes eine vorzeichenlose Ganzzahl enthält. Sofern angegeben, wird `<separator>` nach jeweils `<chunk_size>` Bytes der binären Eingabe eingefügt. Das `<truncate>`-Flag gibt an, ob die binäre Eingabe an `<chunk_size>`-Grenzen abgeschnitten wird. Der maximale Wert für `<chunk_size>` ist durch die Größe von long long int (8 Bytes) begrenzt.

Beispiel:

```text
bin(01020304050607),be2dec(:,2)   # 258:772:1286:7
bin(01020304050607),be2dec(-,2,1) # 258-772-1286
bin(01020304050607),be2dec(,2,1)  # 2587721286
bin(7f000001),be2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-le2dec"></a>

**`le2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
le2dec(<separator>,<chunk_size>[,<truncate>])
```

Wandelt ein binäres Eingabe-Sample im Little-Endian-Format in eine Zeichenkette um, die je `<chunk_size>` Eingabebytes eine vorzeichenlose Ganzzahl enthält. Sofern angegeben, wird `<separator>` nach jeweils `<chunk_size>` Bytes der binären Eingabe eingefügt. Das `<truncate>`-Flag gibt an, ob die binäre Eingabe an `<chunk_size>`-Grenzen abgeschnitten wird. Der maximale Wert für `<chunk_size>` ist durch die Größe von long long int (8 Bytes) begrenzt.

Beispiel:

```text
bin(01020304050607),le2dec(:,2)   # 513:1284:2055:7
bin(01020304050607),le2dec(-,2,1) # 513-1284-2055
bin(01020304050607),le2dec(,2,1)  # 51312842055
bin(7f000001),le2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-be2hex"></a>

**`be2hex([<separator>[,<chunk_size>[,<truncate>]]])`**

```haproxy
be2hex([<separator>[,<chunk_size>[,<truncate>]]])
```

Wandelt ein binäres Eingabe-Sample im Big-Endian-Format in eine Hexadezimalzeichenkette mit zwei Hexadezimalziffern je Eingabebyte um. Damit lassen sich Hex-Dumps binärer Eingabedaten in einer zuverlässig übertragbaren Form protokollieren oder übertragen; beispielsweise kann eine SSL-ID in einen Header kopiert werden. Sofern angegeben, wird `<separator>` nach jeweils `<chunk_size>` Bytes der binären Eingabe eingefügt. Das `<truncate>`-Flag gibt an, ob die binäre Eingabe an `<chunk_size>`-Grenzen abgeschnitten wird.

Beispiel:

```text
bin(01020304050607),be2hex         # 01020304050607
bin(01020304050607),be2hex(:,2)    # 0102:0304:0506:07
bin(01020304050607),be2hex(--,2,1) # 0102--0304--0506
bin(0102030405060708),be2hex(,3,1) # 010203040506
```

<a id="entry-7-3-1-bool"></a>

**`bool`**

```haproxy
bool
```

Gibt den booleschen Wert TRUE zurück, wenn der vorzeichenbehaftete ganzzahlige Eingabewert ungleich null ist, andernfalls FALSE. Zusammen mit and() kann damit bei Bitprüfungen an Eingabewerten true/false zurückgegeben werden, etwa um zu prüfen, ob ein Flag gesetzt ist.

<a id="entry-7-3-1-bytes"></a>

**`bytes(<offset>[,<length>])`**

```haproxy
bytes(<offset>[,<length>])
```

Extrahiert einige Bytes aus einem binären Eingabe-Sample. Das Ergebnis ist ein binäres Sample, das an einem Offset in Bytes innerhalb des ursprünglichen Samples beginnt und optional auf die angegebene Länge gekürzt wird. `<offset>` und `<length>` können Zahlenwerte oder Variablennamen sein. Der Konverter gibt ein leeres Sample zurück, wenn entweder `<offset>` oder `<length>` ungültig ist. `<offset>` ist ungültig, wenn der Wert negativ oder \>= der Länge des Eingabe-Samples ist. `<length>` ist ungültig, wenn der Wert negativ ist.

Beispiel:

```text
http-request set-var(txn.input) req.hdr(input) # let's say input is "012345"

http-response set-header bytes_0 "%[var(txn.input),bytes(0)]"  # outputs "012345"
http-response set-header bytes_1_3 "%[var(txn.input),bytes(1,3)]"  # outputs "123"

http-response set-var(txn.var_start) int(1)
http-response set-var(txn.var_length) int(3)
http-response set-header bytes_var1_var3    "%[var(txn.input),bytes(txn.var_start,txn.var_length)]"  # outputs "123"
```

<a id="entry-7-3-1-capture-req"></a>

**`capture-req(<id>)`**

```haproxy
capture-req(<id>)
```

Erfasst den Zeichenketteneintrag im Anfrage-Slot `<id>` und gibt den Eintrag unverändert zurück. Falls der Slot nicht existiert, schlägt die Erfassung ohne Meldung fehl.

Siehe auch: "declare capture", "http-request capture", "http-response capture", "capture.req.hdr" und "capture.res.hdr" (Sample-Abrufe).

<a id="entry-7-3-1-capture-res"></a>

**`capture-res(<id>)`**

```haproxy
capture-res(<id>)
```

Erfasst den Zeichenketteneintrag im Antwort-Slot `<id>` und gibt den Eintrag unverändert zurück. Falls der Slot nicht existiert, schlägt die Erfassung ohne Meldung fehl.

Siehe auch: "declare capture", "http-request capture", "http-response capture", "capture.req.hdr" und "capture.res.hdr" (Sample-Abrufe).

<a id="entry-7-3-1-concat"></a>

**`concat([<start>[,<var>[,<end>]]])`**

```haproxy
concat([<start>[,<var>[,<end>]]])
```

Hängt bis zu 3 Felder an das aktuelle Sample an, das dabei in eine Zeichenkette umgewandelt wird. Das erste Feld, `<start>`, ist eine konstante Zeichenkette, die unmittelbar an das vorhandene Sample angehängt wird. Sie kann weggelassen werden, wenn sie nicht verwendet wird. Das zweite Feld, `<var>`, ist ein Variablenname. Die Variable wird nachgeschlagen, ihr Inhalt in eine Zeichenkette umgewandelt und unmittelbar an den Teil `<first>` angehängt. Wird die Variable nicht gefunden, wird nichts angehängt. Auch dieses Feld kann weggelassen werden. Das dritte Feld, `<end>`, ist eine konstante Zeichenkette, die nach der Variablen angehängt wird und ebenfalls weggelassen werden kann. Zusammen ermöglichen diese Elemente, Variablen mit Trennzeichen an einen vorhandenen Satz von Variablen anzuhängen. Damit lassen sich neue Variablen aus einer Folge anderer Variablen bilden, beispielsweise durch Doppelpunkte getrennte Werte. Werden Kommas oder schließende Klammern als Trennzeichen benötigt, müssen sie durch Anführungszeichen oder Backslashes geschützt werden. Diese müssen ihrerseits geschützt werden, damit der Parser der ersten Ebene sie nicht entfernt. Dies wird oft verwendet, um zusammengesetzte Variablen aus anderen Variablen zu bilden; manchmal ist jedoch eine Formatzeichenkette mit mehreren Feldern praktischer. Beispiele folgen unten.

Beispiel:

```text
tcp-request session set-var(sess.src) src
tcp-request session set-var(sess.dn)  ssl_c_s_dn
tcp-request session set-var(txn.sig) str(),concat(<ip=,sess.ip,>),concat(<dn=,sess.dn,>)
tcp-request session set-var(txn.ipport) "str(),concat('addr=(',sess.ip),concat(',',sess.port,')')"
tcp-request session set-var-fmt(txn.ipport) "addr=(%[sess.ip],%[sess.port])"  ## does the same
http-request set-header x-hap-sig %[var(txn.sig)]
```

<a id="entry-7-3-1-cpl"></a>

**`cpl`**

```haproxy
cpl
```

Bildet das Einerkomplement des vorzeichenbehafteten ganzzahligen Eingabewerts, kehrt also alle Bits um, und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück.

<a id="entry-7-3-1-crc32"></a>

**`crc32([<avalanche>])`**

```haproxy
crc32([<avalanche>])
```

Bildet mit der Hashfunktion CRC32 aus einem binären Eingabe-Sample einen vorzeichenlosen 32-Bit-Wert. Ist das optionale Argument `<avalanche>` gleich 1, kann auf die Ausgabe zusätzlich eine Hashfunktion mit vollständigem Avalanche-Effekt angewendet werden. Dieser Konverter verwendet dieselben Funktionen wie die verschiedenen hashbasierten Algorithmen zur Lastverteilung und liefert daher exakt dieselben Ergebnisse. Er dient der Kompatibilität mit anderer Software, die CRC32-Werte für Eingabeschlüssel berechnen möchte, und folgt deshalb der gängigsten Implementierung, wie sie in Ethernet, Gzip, PNG usw. verwendet wird. Er ist langsamer als die anderen Algorithmen, kann aber eine bessere oder zumindest weniger vorhersehbare Verteilung liefern. Er darf nicht für Sicherheitszwecke eingesetzt werden, da sich ein 32-Bit-Hash trivial knacken lässt. Siehe auch "djb2", "sdbm", "wt6", "crc32c" sowie die Direktive "hash-type".

<a id="entry-7-3-1-crc32c"></a>

**`crc32c([<avalanche>])`**

```haproxy
crc32c([<avalanche>])
```

Bildet mit der Hashfunktion CRC32C aus einem binären Eingabe-Sample einen vorzeichenlosen 32-Bit-Wert. Ist das optionale Argument `<avalanche>` gleich 1, kann auf die Ausgabe zusätzlich eine Hashfunktion mit vollständigem Avalanche-Effekt angewendet werden. Dieser Konverter verwendet dieselben Funktionen, die in RFC4960, Anhang B [8], beschrieben werden. Er dient der Kompatibilität mit anderer Software, die CRC32C-Werte für Eingabeschlüssel berechnen möchte. Er ist langsamer als die anderen Algorithmen und darf nicht für Sicherheitszwecke eingesetzt werden, da sich ein 32-Bit-Hash trivial knacken lässt. Siehe auch "djb2", "sdbm", "wt6", "crc32" sowie die Direktive "hash-type".

<a id="entry-7-3-1-cut-crlf"></a>

**`cut_crlf`**

```haproxy
cut_crlf
```

Schneidet die Zeichenkettendarstellung des Eingabe-Samples beim ersten gefundenen Wagenrücklauf ('&#92;r') oder Zeilenumbruch ('&#92;n') ab. Dabei wird nur die Länge der Zeichenkette aktualisiert.

<a id="entry-7-3-1-da-csv-conv"></a>

**`da-csv-conv(<prop>[,<prop>*])`**

```haproxy
da-csv-conv(<prop>[,<prop>*])
```

Weist den DeviceAtlas-Konverter an, die übergebene User-Agent-Zeichenkette zu identifizieren und eine Zeichenkette aus den als Argumente aufgeführten Eigenschaften auszugeben. Die Eigenschaften werden miteinander verkettet und durch das mit dem globalen Schlüsselwort "deviceatlas-property-separator" festgelegte Trennzeichen getrennt, standardmäßig durch den senkrechten Strich ('\|'). Die Konfigurationssprache von HAProxy begrenzt die Anzahl auf 12 verschiedene Eigenschaften.

Beispiel:

```text
frontend www
  bind *:8881
  default_backend servers
  http-request set-header X-DeviceAtlas-Data %[req.fhdr(User-Agent),da-csv(primaryHardwareType,osName,osVersion,browserName,browserVersion,browserRenderingEngine)]
```

<a id="entry-7-3-1-date"></a>

**`date`**

```haproxy
date
```

Dieser Konverter wandelt ein Datum aus einem HTTP-Header um. Es kann im Format IMF, ASCTIME oder RFC850 vorliegen. Ausgegeben wird ein Unix-Zeitstempel.

Beispiel:

```text
http-request return lf-string "%[str('Sun, 06 Nov 1994 08:49:37 GMT'),date]\n" content-type text/plain
```

<a id="entry-7-3-1-debug"></a>

**`debug([<prefix][,<destination>])`**

```haproxy
debug([<prefix][,<destination>])
```

Dieser Konverter dient als Werkzeug zur Fehlersuche. Er erfasst das Eingabe-Sample und sendet es an das Ereignisziel `<destination>`. Dieses kann einen Ringpuffer wie "buf0" sowie "stdout" oder "stderr" bezeichnen. Die verfügbaren Ziele lassen sich zur Laufzeit mit "show events" auf der CLI prüfen. Ohne Angabe erfolgt die Ausgabe an "buf0", dessen Inhalt mit dem CLI-Befehl "show events" eingesehen werden kann. Ein optionales Präfix `<prefix>` hilft, Ausgaben mehrerer Ausdrücke zu unterscheiden. Es erscheint vor dem Doppelpunkt in der Ausgabemeldung. Das Eingabe-Sample wird unverändert an die Ausgabe weitergegeben. Deshalb kann der Konverter debug gefahrlos an beliebiger Stelle einer Kette eingefügt werden, auch bei nicht druckbaren Sample-Typen.

Beispiel:

```text
tcp-request connection track-sc0 src,debug(track-sc)
```

<a id="entry-7-3-1-digest"></a>

**`digest(<algorithm>)`**

```haproxy
digest(<algorithm>)
```

Wandelt ein binäres Eingabe-Sample in einen Message Digest um. Das Ergebnis ist ein binäres Sample. `<algorithm>` muss der Name eines OpenSSL-Message-Digests sein, beispielsweise sha256.

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

<a id="entry-7-3-1-div"></a>

**`div(<value>)`**

```haproxy
div(<value>)
```

Dividiert den vorzeichenbehafteten ganzzahligen Eingabewert durch `<value>` und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. Ist `<value>` null, wird die größte vorzeichenlose Ganzzahl zurückgegeben, üblicherweise 2^63-1. `<value>` kann ein Zahlenwert oder ein Variablenname sein. Einzelheiten zu Variablen finden Sie in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-djb2"></a>

**`djb2([<avalanche>])`**

```haproxy
djb2([<avalanche>])
```

Bildet mit der Hashfunktion DJB2 aus einem binären Eingabe-Sample einen vorzeichenlosen 32-Bit-Wert. Ist das optionale Argument `<avalanche>` gleich 1, kann auf die Ausgabe zusätzlich eine Hashfunktion mit vollständigem Avalanche-Effekt angewendet werden. Dieser Konverter verwendet dieselben Funktionen wie die verschiedenen hashbasierten Algorithmen zur Lastverteilung und liefert daher exakt dieselben Ergebnisse. Er ist hauptsächlich zur Fehlersuche vorgesehen, kann aber als Eintrag einer Stick Table zum Erfassen grober Statistiken verwendet werden. Er darf nicht für Sicherheitszwecke eingesetzt werden, da sich ein 32-Bit-Hash leicht knacken lässt. Siehe auch "crc32", "sdbm", "wt6", "crc32c" sowie die Direktive "hash-type".

<a id="entry-7-3-1-eth-data"></a>

**`eth.data`**

```haproxy
eth.data
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Überspringt den gesamten Ethernet-Header einschließlich möglicher VLANs und gibt einen binären Datenblock zurück, der beim Protokoll der Schicht 3 beginnt, üblicherweise IPv4 oder IPv6. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-eth-dst"></a>

**`eth.dst`**

```haproxy
eth.dst
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Gibt die 6 Bytes des Ethernet-Headers, die der Zieladresse des Frames entsprechen, als Binärblock zurück. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-eth-hdr"></a>

**`eth.hdr`**

```haproxy
eth.hdr
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Schneidet alles hinter dem Ethernet-Header ab, behält jedoch mögliche VLANs bei und gibt diesen Header als binären Datenblock zurück. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-eth-proto"></a>

**`eth.proto`**

```haproxy
eth.proto
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Gibt die Protokollnummer, auch EtherType genannt, aus dem Ethernet-Header hinter optionalen VLANs als Ganzzahl zurück. Normalerweise sollte sie entweder 0x800 für IPv4 oder 0x86DD für IPv6 sein. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-eth-src"></a>

**`eth.src`**

```haproxy
eth.src
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Gibt die 6 Bytes des Ethernet-Headers, die der Quelladresse des Frames entsprechen, als Binärblock zurück. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-eth-vlan"></a>

**`eth.vlan`**

```haproxy
eth.vlan
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "2" gesetzten bind-Option "tcp-ss" zurückgibt. Gibt die letzte im Ethernet-Header gefundene VLAN-ID als Ganzzahl zurück. Siehe auch "fc_saved_syn" und "tcp-ss".

<a id="entry-7-3-1-even"></a>

**`even`**

```haproxy
even
```

Gibt den booleschen Wert TRUE zurück, wenn der vorzeichenbehaftete ganzzahlige Eingabewert gerade ist, andernfalls FALSE. Dies ist funktional gleichbedeutend mit "not,and(1),bool".

<a id="entry-7-3-1-field"></a>

**`field(<index>,<delimiters>[,<count>])`**

```haproxy
field(<index>,<delimiters>[,<count>])
```

Extrahiert unter Berücksichtigung der angegebenen Trennzeichen die Teilzeichenkette am angegebenen Index aus einer Eingabezeichenkette. Bei einem positiven Index wird vom Anfang gezählt, bei einem negativen vom Ende. Die Indizes beginnen bei 1 beziehungsweise -1; die Trennzeichen werden als Zeichenkette mit einer Liste von Zeichen angegeben. Optional kann mit `<count>` die Anzahl der zu extrahierenden Felder festgelegt werden (Standard: 1). Der Wert 0 bedeutet, dass alle verbleibenden Felder extrahiert werden.

Beispiel:

```text
str(f1_f2_f3__f5),field(4,_)    # <empty>
str(f1_f2_f3__f5),field(5,_)    # f5
str(f1_f2_f3__f5),field(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),field(2,_,2)  # f2_f3
str(f1_f2_f3__f5),field(-2,_,3) # f2_f3_
str(f1_f2_f3__f5),field(-3,_,0) # f1_f2_f3
```

<a id="entry-7-3-1-fe-exists"></a>

**`fe_exists`**

```haproxy
fe_exists
```

Nimmt einen Frontend-Namen als Eingabewert entgegen und gibt den booleschen Wert TRUE zurück, wenn in der aktuellen Konfiguration ein Frontend mit diesem Namen existiert, andernfalls FALSE. Dies kann dort verwendet werden, wo es sinnvoll ist, anhand eines dynamischen Namens auf das Vorhandensein eines Frontends zu prüfen, etwa bei Map-Abfragen oder beim Beantworten einer externen Prüfung.

Beispiel:

```text
http-request deny unless { var(txn.fe_name),fe_exists }
```

<a id="entry-7-3-1-fix-is-valid"></a>

**`fix_is_valid`**

```haproxy
fix_is_valid
```

Analysiert eine binäre Nutzlast und führt Plausibilitätsprüfungen für FIX (Financial Information eXchange) durch:

- prüft, dass alle Tag-IDs und Werte nicht leer und die Tag-IDs numerisch sind
- prüft, dass das Tag BeginString an erster Stelle steht und eine gültige FIX-Version enthält
- prüft, dass das Tag BodyLength an zweiter Stelle steht und die richtige Länge des Nachrichtenkörpers enthält
- prüft, dass das Tag MsgType an dritter Stelle steht.
- prüft, dass das letzte Tag der Nachricht CheckSum ist und eine gültige Prüfsumme enthält

Aufgrund des derzeitigen Designs von HAProxy kann nur die erste vom Client und vom Server gesendete Nachricht analysiert werden.

Dieser Konverter gibt einen booleschen Wert zurück: true, wenn die Nutzlast eine gültige FIX-Nachricht enthält, andernfalls false.

Siehe auch den Konverter fix_tag_value.

Beispiel:

```text
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
```

<a id="entry-7-3-1-fix-tag-value"></a>

**`fix_tag_value(<tag>)`**

```haproxy
fix_tag_value(<tag>)
```

Analysiert eine FIX-Nachricht (Financial Information eXchange) und extrahiert den Wert des Tags `<tag>`. `<tag>` kann eine Zeichenkette oder eine Ganzzahl sein, die das gewünschte Tag angibt. Jeder Ganzzahlwert ist zulässig; jedoch werden nur die folgenden Zeichenketten in ihre ganzzahlige Entsprechung umgewandelt: BeginString, BodyLength, MsgType, SenderCompID, TargetCompID, CheckSum. Weitere Tagnamen lassen sich leicht ergänzen.

Aufgrund des derzeitigen Designs von HAProxy kann nur die erste vom Client und vom Server gesendete Nachricht analysiert werden. Dieser Konverter führt keine Validierung der Nachricht durch. Es wird dringend empfohlen, die Nachricht zuvor mit dem Konverter fix_is_valid zu validieren.

Siehe auch den Konverter fix_is_valid.

Beispiel:

```shell
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
# MsgType tag ID is 35, so both lines below will return the same content
tcp-request content set-var(txn.foo) req.payload(0,0),fix_tag_value(35)
tcp-request content set-var(txn.bar) req.payload(0,0),fix_tag_value(MsgType)
```

<a id="entry-7-3-1-has-ctl"></a>

**`has_ctl([mask])`**

```haproxy
has_ctl([mask])
```

Prüft das binäre Eingabe-Sample auf die durch das Maskenargument festgelegten Steuerzeichen. Die Maske ist eine 33-Bit-Zahl, entweder dezimal oder hexadezimal mit dem Präfix "0x". Für jedes zu erkennende Zeichen im Bereich 0x00 bis 0x1F ist das entsprechende Bit gesetzt; Bit 32 dient zum Erkennen des Zeichens DEL (0x7F). Ohne Maskenangabe verwendet der Konverter den Wert 0x1FFFFFDFF. Damit werden alle Steuerzeichen außer TAB (0x09) erkannt, das häufig in HTTP-Headern verwendet wird. Die spezielle Maske "any" entspricht 0x1FFFFFFFF und erkennt alle Steuerzeichen einschließlich TAB. Die spezielle Maske "http" entspricht 0x2401 und erkennt nur die in HTTP-Headerwerten verbotenen Steuerzeichen: CR (0x0D), LF (0x0A) und NUL (0x00).

Beispiele:

```shell
# reject presence of DEL, CR, LF, NUL characters in the referer header
http-request deny if { req.fhdr(referer),has_ctl(0x100002401) }
# reject presence of any control char but tab in any HTTP header value
http-request deny if { req.hdr(),has_ctl }
```

<a id="entry-7-3-1-hex"></a>

**`hex`**

```haproxy
hex
```

Wandelt ein binäres Eingabe-Sample in eine Hexadezimalzeichenkette mit zwei Hexadezimalziffern je Eingabebyte um. Damit lassen sich Hex-Dumps binärer Eingabedaten in einer zuverlässig übertragbaren Form protokollieren oder übertragen; beispielsweise kann eine SSL-ID in einen Header kopiert werden.

<a id="entry-7-3-1-hex2i"></a>

**`hex2i`**

```haproxy
hex2i
```

Wandelt eine Hexadezimalzeichenkette mit zwei Hexadezimalziffern je Eingabebyte in eine Ganzzahl um. Enthält der Eingabewert ein Zeichen, das keine Hexadezimalziffer ist, schlägt der Konverter fehl und gibt nichts zurück. So lässt sich eine ungültige Eingabe von einem gültigen Nullwert unterscheiden.

<a id="entry-7-3-1-hmac"></a>

**`hmac(<algorithm>,<key>)`**

```haproxy
hmac(<algorithm>,<key>)
```

Wandelt ein binäres Eingabe-Sample mit dem angegebenen Schlüssel in einen Nachrichtenauthentifizierungscode um. Das Ergebnis ist ein binäres Sample. `<algorithm>` muss einer der registrierten OpenSSL-Message-Digest-Namen sein, beispielsweise sha256. Der Parameter `<key>` muss base64-kodiert sein und kann eine Zeichenkette oder eine Variable sein.

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

<a id="entry-7-3-1-host-only"></a>

**`host_only`**

```haproxy
host_only
```

Wandelt eine Zeichenkette mit dem Wert eines Host-Headers um und entfernt daraus den Port. Die Eingabe muss dem Format des Host-Headerwerts entsprechen (rfc9110#section-7.2). Unterstützt werden Eingaben dieser Art: hostname, hostname:80, 127.0.0.1, 127.0.0.1:80, [::1], [::1]:80.

Dieser Konverter wandelt die Zeichenkette außerdem in Kleinbuchstaben um.

Siehe auch den Konverter "port_only", der den Port zurückgibt.

<a id="entry-7-3-1-htonl"></a>

**`htonl`**

```haproxy
htonl
```

Wandelt den ganzzahligen Eingabewert in seine binäre 32-Bit-Darstellung in Netzwerk-Byte-Reihenfolge um. Da Sample-Abrufe vorzeichenbehaftete 64-Bit-Ganzzahlen verwenden, wird der Eingabewert bei diesem Konverter zunächst in eine vorzeichenlose 32-Bit-Ganzzahl umgewandelt.

<a id="entry-7-3-1-http-date"></a>

**`http_date([<offset[,<unit>]])`**

```haproxy
http_date([<offset[,<unit>]])
```

Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette mit einem für HTTP-Headerfelder geeigneten Datumsformat um. Ist ein Offset angegeben, wird dieser vor der Umwandlung zum Datum addiert. Dies ist besonders nützlich für die Ausgabe von Date-Headerfeldern, von Expires-Werten in Antworten mit einem positiven Offset oder von Last-Modified-Werten mit einem negativen Offset. Bei Angabe einer Einheit wird der Zeitstempel als "s" für Sekunden (Standard), "ms" für Millisekunden oder "us" für Mikrosekunden seit der Epoche interpretiert. Für den Offset wird dieselbe Einheit wie für den Eingabezeitstempel angenommen.

<a id="entry-7-3-1-iif"></a>

**`iif(<true>,<false>)`**

```haproxy
iif(<true>,<false>)
```

Gibt die Zeichenkette `<true>` zurück, wenn der Eingabewert true ist. Andernfalls wird die Zeichenkette `<false>` zurückgegeben.

Beispiel:

```text
http-request set-header x-forwarded-proto %[ssl_fc,iif(https,http)]
```

<a id="entry-7-3-1-in-table"></a>

**`in_table([<table>])`**

```haproxy
in_table([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird der boolesche Wert false zurückgegeben, andernfalls true. Damit lässt sich prüfen, ob ein bestimmter Schlüssel in einer Tabelle vorhanden ist, die Elemente verfolgt, beispielsweise ob eine Quell-IP-Adresse oder ein Authorization-Header bereits beobachtet wurde.

<a id="entry-7-3-1-ip-data"></a>

**`ip.data`**

```haproxy
ip.data
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Überspringt den IP-Header sowie etwaige Optionen oder Erweiterungen und gibt einen binären Datenblock zurück, der beim Transportprotokoll beginnt, üblicherweise TCP oder UDP. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-df"></a>

**`ip.df`**

```haproxy
ip.df
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt die Ganzzahl 1 zurück, wenn das DF-Flag (nicht fragmentieren) im IP-Header gesetzt ist, andernfalls 0. IPv6 besitzt kein DF-Flag und fragmentiert standardmäßig nicht; daher wird immer 1 zurückgegeben. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-dst"></a>

**`ip.dst`**

```haproxy
ip.dst
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt die IPv4- oder IPv6-Zieladresse aus dem IPv4/v6-Header zurück. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-fp"></a>

**`ip.fp([<mode>])`**

```haproxy
ip.fp([<mode>])
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Untersucht verschiedene Teile des IP- und des TCP-Headers, um aus unveränderlichen Teilen eine Art Fingerabdruck zu erstellen. Dieser kann zur Unterscheidung mehrerer scheinbar identischer Hosts dienen. In der Praxis lässt sich damit ein sich fehlerhaft verhaltender Host unter mehreren Hosts mit gemeinsamer IP-Adresse genauer identifizieren, sodass legitime Nutzer nicht blockiert werden, wenn nur ein einzelner Host auffällig ist und blockiert werden muss. Der Konverter erzeugt aus der Eingabe einen binären Block mit mindestens 8 Bytes. Die Bytes des Fingerabdrucks sind wie folgt angeordnet: - Byte 0: IP-TOS-Feld (siehe ip.tos) - Byte 1: - Bit 7: IPv6 (1) / IPv4 (0) - Bit 6: ip.df - Bit 5..4: 0:ip.ttl\<=32; 1:ip.ttl\<=64; 2:ip.ttl\<=128; 3:ip.ttl\<=255 - Bit 3: IP-Optionen vorhanden (1) / nicht vorhanden (0) - Bit 2: TCP-Daten vorhanden (1) / nicht vorhanden (0) - Bit 1: CWR in TCP.flags gesetzt (1) / gelöscht (0) - Bit 0: ECE in TCP.flags gesetzt (1) / gelöscht (0) - Byte 2: - Bits 7..4: TCP-Headerlänge in Wörtern zu 4 Bytes - Bits 3..0: TCP-Fensterskalierung + 1 (1..15) / 0 (keine WS angekündigt) - Byte 3..4: tcp.win - Byte 5..6: tcp.options.mss oder null, falls nicht vorhanden - Byte 7: 1 Bit je vorhandener TCP-Option; die Optionen 2 bis 8 werden auf die Bits 0..6 abgebildet, und Bit 7 zeigt das Vorhandensein einer beliebigen Option von 9 bis 255 an.

Mit dem Argument `<mode>` lassen sich weitere Informationen an den Fingerabdruck anhängen. Standardmäßig, wenn `<mode>` nicht gesetzt oder null ist, besteht der Fingerabdruck ausschließlich aus den oben beschriebenen 8 Bytes. Ein anderer Wert für `<mode>` entspricht der Summe der folgenden Werte; die jeweiligen Bestandteile werden in der nachstehenden Reihenfolge an den Fingerabdruck angehängt: - 1: Der empfangene TTL-Wert wird angehängt (1 Byte). - 2: Die von "tcp.options_list" zurückgegebene Liste der TCP-Optionstypen mit 0 bis 40 zusätzlichen Bytes wird angehängt. - 4: Die Quell-IP-Adresse wird angehängt; dies fügt bei IPv4 4 Bytes und bei IPv6 16 Bytes hinzu.

Beispiel: Einen 13..25 Bytes langen Fingerabdruck aus dem Basis-FP, der TTL und der Quelladresse erstellen (1+4=5):

    frontend test
        mode http
        bind :4445 tcp-ss 1
        tcp-request connection set-var(sess.syn) fc_saved_syn
        http-request return status 200 content-type text/plain lf-string &#92;
              "src=%[var(sess.syn),ip.src] fp=%[var(sess.syn),ip.fp(5),hex]&#92;n"

Siehe auch "fc_saved_syn", "tcp-ss", "eth.data", "ip.df", "ip.ttl", "tcp.win", "tcp.options.mss" und "tcp.options_list".

<a id="entry-7-3-1-ip-hdr"></a>

**`ip.hdr`**

```haproxy
ip.hdr
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt einen binären Datenblock zurück, der mit dem IP-Header beginnt und nach der letzten Option oder Erweiterung, vor dem Header des Transportprotokolls, endet. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-proto"></a>

**`ip.proto`**

```haproxy
ip.proto
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt die Nummer des Transportprotokolls zurück, üblicherweise 6 für TCP oder 17 für UDP. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-src"></a>

**`ip.src`**

```haproxy
ip.src
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt die IPv4- oder IPv6-Quelladresse aus dem IPv4/v6-Header zurück. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-tos"></a>

**`ip.tos`**

```haproxy
ip.tos
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt eine Ganzzahl zurück, die dem Wert des Felds Type of Service (TOS) im IPv4-Header oder Traffic Class (TC) im IPv6-Header entspricht. Im heutigen Internet enthalten die oberen 6 Bits dieses Felds meist einen DSCP-Wert (Differentiated Services Codepoint); die beiden unteren Bits werden entweder nicht oder für IP ECN verwendet. DSCP-Werte sind in RFC2474 und RFC8436 beschrieben, IP-ECN-Felder in RFC3168. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-ttl"></a>

**`ip.ttl`**

```haproxy
ip.ttl
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt eine Ganzzahl zurück, die dem Feld TTL (Time To Live) oder HL (Hop Limit) im IPv4/IPv6-Header entspricht. Dieser Wert wird üblicherweise auf einen festen Anfangswert gesetzt und von jedem Router, den das Paket passiert, verringert. Ist der Anfangswert bekannt, lässt sich daraus abschätzen, aus welcher Entfernung ein Client eine Verbindung herstellt. Die meisten modernen Betriebssysteme beginnen mit einem Wert von 64. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ip-ver"></a>

**`ip.ver`**

```haproxy
ip.ver
```

Wird mit einem Eingabe-Sample verwendet, das einen binären Ethernet-Frame darstellt, wie ihn "fc_saved_syn" in Verbindung mit der auf "1" gesetzten bind-Option "tcp-ss" zurückgibt, oder mit der Ausgabe von "eth.data". Gibt die IP-Version aus dem IP-Header zurück, normalerweise entweder 4 oder 6. Dabei wird nicht geprüft, ob die Protokollnummer im darüberliegenden Ethernet-Frame übereinstimmt. Da der Konverter für gültige Pakete vorgesehen ist, wird davon ausgegangen, dass das Betriebssystem dies bereits überprüft hat. Siehe auch "fc_saved_syn", "tcp-ss" und "eth.data".

<a id="entry-7-3-1-ipmask"></a>

**`ipmask(<mask4>[,<mask6>])`**

```haproxy
ipmask(<mask4>[,<mask6>])
```

Wendet eine Maske auf eine IP-Adresse an und verwendet das Ergebnis für Suchen und zum Speichern. Damit können alle Hosts innerhalb einer bestimmten Maske dieselben Tabelleneinträge und damit denselben Server verwenden. mask4 kann in Punktnotation (z. B. 255.255.255.0) oder in CIDR-Notation (z. B. 24) angegeben werden. mask6 kann in Vierergruppen (z. B. ffff:ffff::) oder in CIDR-Notation (z. B. 64) angegeben werden. Wird keine mask6 angegeben, schlägt die Umwandlung von IPv6-Adressen aus Gründen der Rückwärtskompatibilität fehl.

<a id="entry-7-3-1-json"></a>

**`json([<input-code>])`**

```haproxy
json([<input-code>])
```

Maskiert die Eingabezeichenkette und erzeugt eine ASCII-Ausgabezeichenkette, die als JSON-Zeichenkette verwendet werden kann. Der Konverter versucht, die Eingabezeichenkette gemäß dem Parameter `<input-code>` zu dekodieren. Dieser kann "ascii", "utf8", "utf8s", "utf8p" oder "utf8ps" sein. Der Dekoder "ascii" schlägt niemals fehl. Der Dekoder "utf8" erkennt 3 Fehlerarten:

- fehlerhafte UTF-8-Sequenz (einzelnes Fortsetzungsbyte, falsche Anzahl von Fortsetzungsbytes, ...)
- ungültiger Bereich (der dekodierte Wert liegt in einem für UTF-8 verbotenen Bereich),
- überlange Kodierung (der Wert ist mit mehr Bytes als nötig kodiert).

Die UTF-8-JSON-Kodierung kann den Fehler "too long value" erzeugen, wenn das UTF-8-Zeichen größer als 0xffff ist, da die Spezifikation für Escape-Sequenzen in JSON-Zeichenketten nur 4 Hexadezimalziffern zur Kodierung des Werts zulässt. Den UTF-8-Dekoder gibt es in 4 Varianten, die durch die Kombination zweier Suffixbuchstaben bezeichnet werden: "p" für "permissive" (tolerant) und "s" für "silently ignore" (stillschweigend ignorieren). Die Dekoder verhalten sich wie folgt:

- "ascii" : schlägt niemals fehl;
- "utf8" : schlägt bei jedem erkannten Fehler fehl;
- "utf8s" : schlägt niemals fehl, entfernt aber die fehlerhaften Zeichen;
- "utf8p" : akzeptiert und korrigiert überlange Kodierungen, schlägt aber bei jedem anderen Fehler fehl;
- "utf8ps": schlägt niemals fehl, akzeptiert und korrigiert überlange Kodierungen, entfernt aber Zeichen, die anderen Fehlern entsprechen.

Dieser Konverter eignet sich besonders zum Erstellen korrekt maskierter JSON-Daten für die Protokollierung auf Servern, die Verkehrsprotokolle im JSON-Format verarbeiten.

Beispiel:

```text
capture request header Host len 15
capture request header user-agent len 150
log-format '{"ip":"%[src]","user-agent":"%[capture.req.hdr(1),json(utf8s)]"}'
```

Eingehende Anfrage vom Client 127.0.0.1:

```text
GET / HTTP/1.0
User-Agent: Very "Ugly" UA 1/2
```

Ausgegebenes Protokoll:

```text
{"ip":"127.0.0.1","user-agent":"Very \"Ugly\" UA 1\/2"}
```

<a id="entry-7-3-1-json-query"></a>

**`json_query(<json_path>[,<output_type>])`**

```haproxy
json_query(<json_path>[,<output_type>])
```

Der Konverter json_query unterstützt die JSON-Typen string, boolean, number und array. Gleitkommazahlen werden als Zeichenkette zurückgegeben. Mit der Angabe 'int' für output_type wird der Wert in eine Ganzzahl umgewandelt. Arrays werden als Zeichenkette zurückgegeben, die mit einer eckigen Klammer beginnt und endet. Der Inhalt ist eine CSV-Liste. Je nach Datentyp können die Array-Werte in Anführungszeichen stehen. Sind die Array-Werte komplexe Typen, enthält die Zeichenkette die vollständige JSON-Darstellung jedes Werts, durch Kommas getrennt. Beispielergebnis einer roles-Abfrage für ein JWT:

```text
["manage-account","manage-account-links","view-profile"]
```

Ist eine Umwandlung nicht möglich, schlägt der Konverter json_query fehl.

`<json_path>` muss eine gültige JSON-Path-Zeichenkette gemäß
<https://datatracker.ietf.org/doc/draft-ietf-jsonpath-base/> sein.

Hinweis: Abhängig vom Kontext und der zugrunde liegenden Implementierung ist das Verhalten beim Extrahieren mehrfach vorhandener JSON-Schlüssel undefiniert. Es kann das erste, letzte oder ein anderes Vorkommen desselben Schlüssels aus dem Eingabeinhalt zurückgegeben werden; kodiert übergebene Schlüsselnamen werden möglicherweise nicht immer erkannt. Dieser Konverter eignet sich daher nicht zur Bereinigung von Inhalten.

Beispiel:

```shell
# get a integer value from the request body
# "{"integer":4}" => 5
http-request set-var(txn.pay_int) req.body,json_query('$.integer','int'),add(1)

# get a key with '.' in the name
# {"my.key":"myvalue"} => myvalue
http-request set-var(txn.pay_mykey) req.body,json_query('$.my\\.key')

# {"boolean-false":false} => 0
http-request set-var(txn.pay_boolean_false) req.body,json_query('$.boolean-false')

# get the value of the key 'iss' from a JWT Bearer token
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec,json_query('$.iss')
```

<a id="entry-7-3-1-jwt-decrypt-cert"></a>

**`jwt_decrypt_cert(<cert>)`**

```haproxy
jwt_decrypt_cert(<cert>)
```

Prüft die Signatur eines als Eingabe übergebenen JSON Web Token im Format JSON Web Encryption (siehe RFC 7516) und gibt dessen mit dem bereitgestellten Zertifikat entschlüsselten Inhalt zurück. Der Parameter `<cert>` muss der Pfad zu einem bereits geladenen Zertifikat sein, das sich über den CLI-Befehl "dump ssl cert" ausgeben lässt. Die Option "jwt" des Zertifikats muss ausdrücklich auf "on" gesetzt sein (siehe die crt-list-Option "jwt"). Der Pfad kann direkt oder über eine Variable übergeben werden. Derzeit werden nur Token im Format Compact Serialization unterstützt: fünf durch Punkte getrennte, mit base64-url kodierte Zeichenketten.

Dieser Konverter kann für Token verwendet werden, deren Algorithmus (Feld "alg" des JOSE-Headers) einer der folgenden ist: RSA-OAEP, RSA-OAEP-256, ECDH-ES, ECDH-ES+A128KW, ECDH-ES+A192KW oder ECDH-ES+A256KW. Der Algorithmus RSA1_5 ist implementiert, aber entsprechend der Empfehlung in [Abschnitt 3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) von RFC 8725 standardmäßig deaktiviert. Bei Bedarf lässt er sich mit der globalen Option 'jwt.decrypt_alg_list' wieder aktivieren.

Die unterstützten Algorithmen und Verschlüsselungsalgorithmen (Felder "alg" bzw. "enc" des JOSE-Headers) lassen sich mit den globalen Optionen 'jwt.decrypt_alg_list' und 'jwt.decrypt_enc_list' ändern.

Das JWE-Token muss base64url-kodiert übergeben werden; die Ausgabe erfolgt "raw", also als Rohdaten. Tritt beim Analysieren des Tokens, beim Prüfen der Signatur oder beim Entschlüsseln des Inhalts ein Fehler auf, wird eine leere Zeichenkette zurückgegeben.

Beispiel:

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_cert("/foo/bar.pem")]
```

<a id="entry-7-3-1-jwt-decrypt-jwk"></a>

**`jwt_decrypt_jwk(<jwk>)`**

```haproxy
jwt_decrypt_jwk(<jwk>)
```

Prüft die Signatur eines als Eingabe übergebenen JSON Web Token im Format JSON Web Encryption (siehe RFC 7516) und gibt dessen mit dem bereitgestellten JSON Web Key (RFC7517) entschlüsselten Inhalt zurück. Der Parameter `<jwk>` muss ein gültiger JWK des Typs 'oct', 'EC' oder 'RSA' sein (Feld 'kty' des JSON-Schlüssels) und kann als Zeichenkette oder über eine Variable übergeben werden.

Derzeit werden nur Token im Format Compact Serialization unterstützt: fünf durch Punkte getrennte, mit base64-url kodierte Zeichenketten.

Dieser Konverter kann Token entschlüsseln, deren symmetrischer Algorithmus (Feld "alg" des JOSE-Headers) einer der folgenden ist: A128KW, A192KW, A256KW, A128GCMKW, A192GCMKW, A256GCMKW, dir. In diesem Fall muss der bereitgestellte JWK vom Typ 'oct' sein.

Dieser Konverter unterstützt außerdem Token, deren Algorithmus (Feld "alg" des JOSE-Headers) zur RSA-Familie gehört (RSA-OAEP oder RSA-OAEP-256), wenn ein JWK vom Typ 'RSA' übergeben wird, oder zur ECDH-Familie (ECDH-ES, ECDH-ES+A128KW, ECDH-ES+A192KW oder ECDH-ES+A256KW), wenn ein JWK vom Typ 'EC' übergeben wird. Der Algorithmus RSA1_5 ist implementiert, aber entsprechend der Empfehlung in [Abschnitt 3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) von RFC 8725 standardmäßig deaktiviert. Bei Bedarf lässt er sich mit der globalen Option 'jwt.decrypt_alg_list' wieder aktivieren.

Die Algorithmen A128KW und A192KW stehen unter AWS-LC nicht zur Verfügung. Daher funktionieren die Algorithmen A128KW, A192KW, ECDH-ES+A128KW und ECDH-ES+A192KW dort nicht.

Die unterstützten Algorithmen und Verschlüsselungsalgorithmen (Felder "alg" bzw. "enc" des JOSE-Headers) lassen sich mit den globalen Optionen 'jwt.decrypt_alg_list' und 'jwt.decrypt_enc_list' ändern.

Das JWE-Token muss base64url-kodiert übergeben werden; die Ausgabe erfolgt "raw", also als Rohdaten. Tritt beim Analysieren des Tokens, beim Prüfen der Signatur oder beim Entschlüsseln des Inhalts ein Fehler auf, wird eine leere Zeichenkette zurückgegeben.

Aufgrund der Behandlung einfacher Anführungszeichen, Kommas und doppelter Anführungszeichen in der Konfiguration muss der Inhalt des JWK korrekt maskiert werden, damit dieser Konverter richtig funktioniert (weitere Informationen stehen in [Abschnitt 2.2](/de/haproxy/configuration-basics/#section-2-2)).

Beispiel:

```shell
 # Get a JWT from the authorization header, put its decrypted content in an
 # HTTP header
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(\'{\"kty\":\"oct\",\"k\":\"wAsgsg\"}\')

# or via a variable
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-var(txn.jwk) str(\'{\"kty\":\"oct\",\"k\":\"Q-NFLlghQ\"}\')
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(txn.jwk)
```

<a id="entry-7-3-1-jwt-decrypt-secret"></a>

**`jwt_decrypt_secret(<secret>)`**

```haproxy
jwt_decrypt_secret(<secret>)
```

Prüft die Signatur eines als Eingabe übergebenen JSON Web Token im Format JSON Web Encryption (siehe RFC 7516) und gibt dessen mit dem bereitgestellten base64-kodierten Geheimnis entschlüsselten Inhalt zurück. Das Geheimnis kann als Zeichenkette oder über eine Variable übergeben werden. Derzeit werden nur Token im Format Compact Serialization unterstützt: fünf durch Punkte getrennte, mit base64-url kodierte Zeichenketten.

Dieser Konverter kann für Token verwendet werden, deren Algorithmus (Feld "alg" des JOSE-Headers) einer der folgenden ist: A128KW, A192KW, A256KW, A128GCMKW, A192GCMKW, A256GCMKW, dir. Die Algorithmen A128KW und A192KW stehen unter AWS-LC nicht zur Verfügung; die Entschlüsselung funktioniert dort nicht.

Das JWE-Token muss base64url-kodiert übergeben werden; die Ausgabe erfolgt "raw", also als Rohdaten. Tritt beim Analysieren des Tokens, beim Prüfen der Signatur oder beim Entschlüsseln des Inhalts ein Fehler auf, wird eine leere Zeichenkette zurückgegeben.

Beispiel:

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_secret("GawgguFyGrWKav7AX4VKUg")]
```

<a id="entry-7-3-1-jwt-header-query"></a>

**`jwt_header_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_header_query([<json_path>[,<output_type>]])
```

Bei Eingabe eines JSON Web Token (JWT) wird entweder der dekodierte Header-Teil des Tokens (der erste base64-url-kodierte Teil des JWT) zurückgegeben, wenn kein Parameter angegeben ist, oder eine json_query auf dem dekodierten Header-Teil ausgeführt. Einzelheiten zu den zulässigen Parametern json_path und output_type stehen beim Konverter "json_query". Dieser Konverter unterstützt sowohl JWS- als auch JWE-Token, sofern sie im Format Compact Serialization vorliegen.

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

<a id="entry-7-3-1-jwt-payload-query"></a>

**`jwt_payload_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_payload_query([<json_path>[,<output_type>]])
```

Bei Eingabe eines JSON Web Token (JWT) im Format JSON Web Signed (JWS) wird entweder der dekodierte Nutzlast-Teil des Tokens (der zweite base64-url-kodierte Teil des JWT) zurückgegeben, wenn kein Parameter angegeben ist, oder eine json_query auf dem dekodierten Nutzlast-Teil ausgeführt. Einzelheiten zu den zulässigen Parametern json_path und output_type stehen beim Konverter "json_query".

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

jwt_verify(`<alg>`,`<key>`)

Prüft die Signatur des als Eingabe übergebenen JSON Web Token (JWT) mit dem Algorithmus `<alg>` und dem Parameter `<key>`. Derzeit können nur JWS-Token im Format Compact Serialization verarbeitet werden: drei durch Punkte getrennte, mit base64-url kodierte Zeichenketten. Dieser Konverter prüft ausschließlich die Signatur des Tokens und führt keine vollständige JWT-Validierung gemäß [Abschnitt 7.2](https://www.rfc-editor.org/rfc/rfc7519#section-7.2) von RFC7519 durch. Beispielsweise wird nicht sichergestellt, dass Header und Nutzlast nach dem Dekodieren vollständig gültiges JSON enthalten; auch ihre jeweiligen Inhalte werden nicht geprüft.

- `<alg>` kann eine Zeichenkette oder der Name einer Variablen sein (siehe auch "set-var"), die den Namen des zur Überprüfung verwendeten Algorithmus enthält.

  Unterstützt werden die in [Abschnitt 3.1](https://www.rfc-editor.org/rfc/rfc7518#section-3.1) von RFC7518 genannten Algorithmen:

```text
   +-----------------+-------------------------------------------------+
   | Parameter "alg" | Digitaler Signatur- oder MAC-Algorithmus        |
   | Wert            |                                                 |
   +-----------------+-------------------------------------------------+
   | HS256           | HMAC mit SHA-256                                |
   | HS384           | HMAC mit SHA-384                                |
   | HS512           | HMAC mit SHA-512                                |
   | RS256           | RSASSA-PKCS1-v1_5 mit SHA-256                   |
   | RS384           | RSASSA-PKCS1-v1_5 mit SHA-384                   |
   | RS512           | RSASSA-PKCS1-v1_5 mit SHA-512                   |
   | ES256           | ECDSA mit P-256 und SHA-256                     |
   | ES384           | ECDSA mit P-384 und SHA-384                     |
   | ES512           | ECDSA mit P-521 und SHA-512                     |
   | PS256           | RSASSA-PSS mit SHA-256 und MGF1 mit SHA-256     |
   | PS384           | RSASSA-PSS mit SHA-384 und MGF1 mit SHA-384     |
   | PS512           | RSASSA-PSS mit SHA-512 und MGF1 mit SHA-512     |
   | none            | Keine digitale Signatur und kein MAC angewendet (siehe Hinweis unten) |
   +-----------------+-------------------------------------------------+
```

Der Algorithmus "none" ist standardmäßig nicht erlaubt, um den Empfehlungen in RFC8725 [Abschnitt 3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) zu folgen. Setzen Sie die globale Option 'jwt.allow_none_alg', um ihn ausdrücklich zu erlauben.


- `<key>` kann eine Zeichenkette oder der Name einer Variablen sein (siehe auch "set-var"), die ein Geheimnis oder den Pfad zu einem öffentlichen Schlüssel enthält.

  Geheimnisse sind nur bei HMAC-Algorithmen anwendbar.

  Öffentliche Schlüssel müssen entweder im Format PKCS#1 vorliegen (bei RSA-Schlüsseln, beginnend mit BEGIN RSA PUBLIC KEY) oder im SPKI-Format (Subject Public Key Info, beginnend mit BEGIN PUBLIC KEY). Öffentliche Schlüssel müssen beim Einlesen der Konfiguration verfügbar sein und lassen sich zur Laufzeit weder aktualisieren noch laden. Zur JWT-Token-Validierung anhand vollständiger PEM-Zertifikate siehe den Konverter "jwt_verify_cert".

  Alle öffentlichen Schlüssel, die zur Überprüfung von JWTs verwendet werden könnten, müssen bei der Initialisierung bekannt sein. Sie werden in einen eigenen Cache aufgenommen, damit zur Laufzeit keine Festplattenzugriffe nötig sind.

Gibt bei erfolgreicher Überprüfung 1, bei fehlgeschlagener Überprüfung 0 und bei jedem anderen Fehler einen strikt negativen Wert zurück. Wegen dieser von null verschiedenen Fehler-Rückgabewerte sollte das Ergebnis dieses Konverters niemals in einen booleschen Wert umgewandelt werden. Eine vollständige Liste der möglichen Rückgabewerte folgt unten.

Die möglichen Rückgabewerte sind:

```text
  +----+------------------------------------------------+
  | ID | Meldung                                        |
  +----+------------------------------------------------+
  | 1  | "Verification success"                         |
  | 0  | "Verification failure"                         |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)" |
  | -2 | "Unmanaged algorithm"                          |
  | -3 | "Invalid token"                                |
  | -4 | "Out of memory"                                |
  | -5 | "Unknown pubkey/certificate"                   |
  | -6 | "Internal error"                               |
  +----+------------------------------------------------+
```

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

Beispiel:

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public key to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify(txn.jwt_alg,"/path/to/pubkey.pem") 1 }
```

jwt_verify_cert(`<alg>`,`<cert>`)

Prüft die Signatur des als Eingabe übergebenen JSON Web Token (JWT) mit dem Algorithmus `<alg>` und dem Parameter `<cert>`. Derzeit können nur JWS-Token im Format Compact Serialization verarbeitet werden: drei durch Punkte getrennte, mit base64-url kodierte Zeichenketten. Dieser Konverter prüft ausschließlich die Signatur des Tokens und führt keine vollständige JWT-Validierung gemäß [Abschnitt 7.2](https://www.rfc-editor.org/rfc/rfc7519#section-7.2) von RFC7519 durch. Beispielsweise wird nicht sichergestellt, dass Header und Nutzlast nach dem Dekodieren vollständig gültiges JSON enthalten; auch ihre jeweiligen Inhalte werden nicht geprüft.

- `<alg>` kann eine Zeichenkette oder der Name einer Variablen sein (siehe auch "set-var"), die den Namen des zur Überprüfung verwendeten Algorithmus enthält. Anders als der Konverter "jwt_verify" erwartet dieser Konverter als zweiten Parameter ausschließlich ein Zertifikat. Er sollte daher nicht für Token mit HMAC-Algorithmen verwendet werden.

  Unterstützt werden die in [Abschnitt 3.1](https://www.rfc-editor.org/rfc/rfc7518#section-3.1) von RFC7518 genannten Algorithmen (außer den HMAC-Algorithmen):

```text
   +-----------------+-------------------------------------------------+
   | Parameter "alg" | Digitaler Signatur- oder MAC-Algorithmus        |
   | Wert            |                                                 |
   +-----------------+-------------------------------------------------+
   | RS256           | RSASSA-PKCS1-v1_5 mit SHA-256                   |
   | RS384           | RSASSA-PKCS1-v1_5 mit SHA-384                   |
   | RS512           | RSASSA-PKCS1-v1_5 mit SHA-512                   |
   | ES256           | ECDSA mit P-256 und SHA-256                     |
   | ES384           | ECDSA mit P-384 und SHA-384                     |
   | ES512           | ECDSA mit P-521 und SHA-512                     |
   | PS256           | RSASSA-PSS mit SHA-256 und MGF1 mit SHA-256     |
   | PS384           | RSASSA-PSS mit SHA-384 und MGF1 mit SHA-384     |
   | PS512           | RSASSA-PSS mit SHA-512 und MGF1 mit SHA-512     |
   | none            | Keine digitale Signatur und kein MAC angewendet |
   +-----------------+-------------------------------------------------+
```

- `<key>` kann eine Zeichenkette oder der Name einer Variablen sein (siehe auch "set-var"), die einen Zertifikatspfad enthält.

  Zertifikate müssen Standard-PEM-Zertifikate sein (beginnend mit BEGIN CERTIFICATE). Ihr Pfad kann dem Konverter direkt übergeben oder über eine Variable referenziert werden. Bei Verwendung einer Variablen können die entsprechenden Zertifikate entweder in einem crt-store deklariert oder dynamisch über den Stats-Socket geladen werden. Wird ein Pfad direkt angegeben und ist das entsprechende Zertifikat noch nicht im internen Zertifikatsspeicher geladen, wird es beim Einlesen der Konfiguration geladen. Es muss daher bereits vorhanden sein, andernfalls wird ein Fehler ausgelöst.

  Verwendet werden können nur Zertifikate, die ausdrücklich für die JWT-Validierung freigegeben sind. Siehe die crt-store-Option "jwt".

  Zertifikate lassen sich dynamisch aktualisieren und neue Zertifikate über den Stats-Socket hinzufügen. Siehe auch "set ssl cert" und "new ssl cert" im Verwaltungshandbuch.

Gibt bei erfolgreicher Überprüfung 1, bei fehlgeschlagener Überprüfung 0 und bei jedem anderen Fehler einen strikt negativen Wert zurück. Wegen dieser von null verschiedenen Fehler-Rückgabewerte sollte das Ergebnis dieses Konverters niemals in einen booleschen Wert umgewandelt werden. Eine vollständige Liste der möglichen Rückgabewerte folgt unten.

Die möglichen Rückgabewerte sind:

```text
  +----+------------------------------------------------+
  | ID | Meldung                                        |
  +----+------------------------------------------------+
  | 1  | "Verification success"                         |
  | 0  | "Verification failure"                         |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)" |
  | -2 | "Unmanaged algorithm"                          |
  | -3 | "Invalid token"                                |
  | -4 | "Out of memory"                                |
  | -5 | "Unknown pubkey/certificate"                   |
  | -6 | "Internal error"                               |
  | -7 | "Unavailable certificate" (siehe "jwt")        |
  +----+------------------------------------------------+
```

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

Beispiel:

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public certificate to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify_cert(txn.jwt_alg,"/path/to/cert.pem") 1 }
```

<a id="entry-7-3-1-language"></a>

**`language(<value>[,<default>])`**

```haproxy
language(<value>[,<default>])
```

Gibt aus einer mit "req.fhdr" aus dem Header "accept-language" extrahierten Liste den Wert mit dem höchsten q-Faktor zurück. Werte ohne q-Faktor haben den q-Faktor 1. Werte mit dem q-Faktor 0 werden verworfen. Es werden nur Werte berücksichtigt, die in der durch Semikolons getrennten Liste `<values>` enthalten sind. Die Syntax des Arguments `<value>` lautet "lang[;lang[;lang[;...]]]". Passt kein Wert zur angegebenen Liste und ist ein Standardwert angegeben, wird dieser zurückgegeben. Sprachnamen können nach einem Bindestrich ('-') eine Variante enthalten. Ist diese Variante in der Liste vorhanden, wird sie abgeglichen; andernfalls wird nur die Basissprache geprüft. Beim Abgleich wird Groß-/Kleinschreibung beachtet, und die ausgegebene Zeichenkette ist stets einer der in den Argumenten angegebenen Werte. Die Reihenfolge der Argumente spielt keine Rolle. Es zählt nur die Reihenfolge der Werte in der Anfrage, da bei mehreren Werten mit demselben q-Faktor der erste verwendet wird.

Beispiel:

```shell
# this configuration switches to the backend matching a
# given language based on the request:

acl es req.fhdr(accept-language),language(es;fr;en) -m str es
acl fr req.fhdr(accept-language),language(es;fr;en) -m str fr
acl en req.fhdr(accept-language),language(es;fr;en) -m str en
use_backend spanish if es
use_backend french  if fr
use_backend english if en
default_backend choose_your_language
```

<a id="entry-7-3-1-length"></a>

**`length`**

```haproxy
length
```

Ermittelt die Länge der Zeichenkette. Kann nur hinter einer Sample-Abruffunktion für Zeichenketten oder hinter einem Transformationsschlüsselwort stehen, das den Typ string zurückgibt. Das Ergebnis hat den Typ integer.

<a id="entry-7-3-1-lower"></a>

**`lower`**

```haproxy
lower
```

Wandelt ein Zeichenketten-Sample in Kleinbuchstaben um. Kann nur hinter einer Sample-Abruffunktion für Zeichenketten oder hinter einem Transformationsschlüsselwort stehen, das den Typ string zurückgibt. Das Ergebnis hat den Typ string.

<a id="entry-7-3-1-ltime"></a>

**`ltime(<format>[,<offset>])`**

```haproxy
ltime(<format>[,<offset>])
```

Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in Ortszeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Sekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime(). Siehe auch den Konverter utime.

Beispiel:

```shell
# Emit two colons, one with the local time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,ltime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-ltrim"></a>

**`ltrim(<chars>)`**

```haproxy
ltrim(<chars>)
```

Überspringt am Anfang der Zeichenkettendarstellung des Eingabe-Samples alle Zeichen aus `<chars>`.

<a id="entry-7-3-1-map"></a>

**`map(<map_name>[,<default_value>])`**

```haproxy
map(<map_name>[,<default_value>])
map_<match_type>(<map_name>[,<default_value>])
map_<match_type>_<output_type>(<map_name>[,<default_value>])
```

Sucht den Eingabewert in `<map_name>` mit der Abgleichmethode `<match_type>` und gibt den zugeordneten Wert zurück, umgewandelt in den Typ `<output_type>`. Wird der Eingabewert in `<map_name>` nicht gefunden, gibt der Konverter `<default_value>` zurück. Ist `<default_value>` nicht gesetzt, schlägt der Konverter fehl und verhält sich so, als ließe sich kein Eingabewert abrufen. Ist `<match_type>` nicht gesetzt, wird "str" verwendet. Ebenso wird bei nicht gesetztem `<output_type>` der Wert "str" verwendet. Das Schlüsselwort "map" ist der Einfachheit halber ein Alias für "map_str" und bildet eine Zeichenkette auf eine andere ab. `<map_name>` muss dem in 2.7. beschriebenen Namensformat für Maps und ACLs entsprechen.

Überschneidungen zwischen Schlüsseln sollten unbedingt vermieden werden: IP-Adressen und Zeichenketten werden in Bäumen gespeichert, sodass die erste der spezifischsten Übereinstimmungen verwendet wird. Andere Schlüssel werden in Listen gespeichert; hier wird das erste passende Vorkommen verwendet.

Die folgende Tabelle enthält alle verfügbaren Map-Funktionen, geordnet nach Eingabetyp, Abgleichmethode und Ausgabetyp.

```text
  Eingabetyp | Abgleich     | Ausgabetyp  str | Ausgabetyp  int | Ausgabetyp  ip | Ausgabetyp  key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | str          | map_str         | map_str_int     | map_str_ip     | map_str_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | beg          | map_beg         | map_beg_int     | map_beg_ip     | map_beg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | sub          | map_sub         | map_sub_int     | map_sub_ip     | map_sub_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | dir          | map_dir         | map_dir_int     | map_dir_ip     | map_dir_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | dom          | map_dom         | map_dom_int     | map_dom_ip     | map_dom_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | end          | map_end         | map_end_int     | map_end_ip     | map_end_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | reg          | map_reg         | map_reg_int     | map_reg_ip     | map_reg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | reg          | map_regm        | map_reg_int     | map_reg_ip     | map_reg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    int      | int          | map_int         | map_int_int     | map_int_ip     | map_int_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    ip       | ip           | map_ip          | map_ip_int      | map_ip_ip      | map_ip_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
```

Die spezielle Map "map_regm" erwartet eine Erfassungsgruppe im regulären Ausdruck und ändert die Ausgabe, indem Rückverweise (wie "&#92;1") durch den entsprechenden übereinstimmenden Text ersetzt werden.

Der Ausgabetyp "key" bedeutet, dass der Schlüssel des passenden Eintrags (wie in der Map-Datei vorhanden) als Zeichenkette zurückgegeben wird, anstelle des Werts. Das optionale Argument `<default_value>` wird beim Ausgabetyp "key" nicht unterstützt.

Die durch `<map_name>` referenzierten Dateien enthalten je Zeile einen Schlüssel und einen Wert. Zeilen, die mit '#' beginnen, werden ebenso wie Leerzeilen ignoriert. Führende Tabulatoren und Leerzeichen werden entfernt. Der Schlüssel ist dann das erste "Wort", also eine Folge von Zeichen ohne Leerzeichen oder Tabulatoren. Der Wert ist der auf die anschließende Folge von Leerzeichen oder Tabulatoren folgende Text bis zum Zeilenende, ohne abschließende Leerzeichen oder Tabulatoren.

Beispiel:

```text
     # this is a comment and is ignored
        2.22.246.0/23    United Kingdom      \n
     <-><-----------><--><------------><---->
      |       |       |         |        `- nachgestellte Leerzeichen ignoriert
      |       |       |         `---------- Wert
      |       |       `-------------------- Leerzeichen dazwischen ignoriert
      |       `---------------------------- Schlüssel
      `------------------------------------ führende Leerzeichen ignoriert
```

<a id="entry-7-3-1-mod"></a>

**`mod(<value>)`**

```haproxy
mod(<value>)
```

Dividiert den vorzeichenbehafteten ganzzahligen Eingabewert durch `<value>` und gibt den Rest als vorzeichenbehaftete Ganzzahl zurück. Ist `<value>` null, wird null zurückgegeben. `<value>` kann ein numerischer Wert oder ein Variablenname sein. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-mqtt-field-value"></a>

**`mqtt_field_value(<packettype>,<fieldname_or_property_ID>)`**

```haproxy
mqtt_field_value(<packettype>,<fieldname_or_property_ID>)
```

Gibt den Wert von `<fieldname>` zurück, der in der MQTT-Eingabenutzlast vom Typ `<packettype>` gefunden wird. `<packettype>` kann eine Zeichenkette (Abgleich ohne Beachtung der Groß-/Kleinschreibung) oder ein numerischer Wert sein, der dem Pakettyp entspricht, aus dem Daten extrahiert werden sollen. Die unterstützten Zeichenketten und Ganzzahlen stehen hier:
<https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718021>
<https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022>

`<fieldname>` hängt von `<packettype>` ab und kann einer der unten aufgeführten Werte sein. Beim Abgleich von `<fieldname>` wird die Groß-/Kleinschreibung nicht beachtet. `<property id>` kommt nur in MQTT-v5.0-Datenströmen vor. Siehe diese Tabelle: <https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901029>

- CONNECT (oder 1): flags, protocol_name, protocol_version, client_identifier, will_topic,
  will_payload, username, password, keepalive ODER eine beliebige Eigenschafts-ID als numerischer Wert (nur für MQTT-v5.0-Pakete):

```text
17: Session Expiry Interval
33: Receive Maximum
39: Maximum Packet Size
34: Topic Alias Maximum
25: Request Response Information
23: Request Problem Information
21: Authentication Method
22: Authentication Data
18: Will Delay Interval
 1: Payload Format Indicator
 2: Message Expiry Interval
 3: Content Type
 8: Response Topic
 9: Correlation Data
```

Noch nicht unterstützt:

```text
38: User Property
```

- CONNACK (oder 2): flags, protocol_version, reason_code ODER eine beliebige Eigenschafts-ID als numerischer Wert (nur für MQTT-v5.0-Pakete):

```text
17: Session Expiry Interval
33: Receive Maximum
36: Maximum QoS
37: Retain Available
39: Maximum Packet Size
18: Assigned Client Identifier
34: Topic Alias Maximum
31: Reason String
40; Wildcard Subscription Available
41: Subscription Identifiers Available
42: Shared Subscription Available
19: Server Keep Alive
26: Response Information
28: Server Reference
21: Authentication Method
22: Authentication Data
```

Noch nicht unterstützt:

```text
38: User Property
```

Aufgrund des derzeitigen Designs von HAProxy kann nur die erste vom Client und vom Server gesendete Nachricht analysiert werden. Daher kann dieser Konverter nur Daten aus den Pakettypen CONNECT und CONNACK extrahieren. CONNECT ist die erste vom Client gesendete Nachricht und CONNACK die erste vom Server gesendete Antwort.

Beispiel:

```shell
acl data_in_buffer req.len ge 4
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(connect,protocol_name) \
        if data_in_buffer
# do the same as above
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(1,protocol_name) \
        if data_in_buffer
```

<a id="entry-7-3-1-mqtt-is-valid"></a>

**`mqtt_is_valid`**

```haproxy
mqtt_is_valid
```

Prüft, ob die binäre Eingabe ein gültiges MQTT-Paket ist. Gibt einen booleschen Wert zurück.

Aufgrund des derzeitigen Designs von HAProxy kann nur die erste vom Client und vom Server gesendete Nachricht analysiert werden. Daher kann dieser Konverter nur Daten aus den Pakettypen CONNECT und CONNACK extrahieren. CONNECT ist die erste vom Client gesendete Nachricht und CONNACK die erste vom Server gesendete Antwort.

Es werden nur MQTT 3.1, 3.1.1 und 5.0 unterstützt.

Beispiel:

```text
acl data_in_buffer req.len ge 4
tcp-request content reject unless { req.payload(0,0),mqtt_is_valid }
```

<a id="entry-7-3-1-ms-ltime"></a>

**`ms_ltime(<format>[,<offset>])`**

```haproxy
ms_ltime(<format>[,<offset>])
```

Funktioniert wie "ltime", erwartet die Eingabe aber in Millisekunden. Unterstützt außerdem das von date(1) inspirierte Konvertierungskennzeichen %N. Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in Ortszeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Millisekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime().

Mit dem Konvertierungskennzeichen %N lässt sich der Nanosekundenanteil des Datums ausgeben. Da die Eingabe in Millisekunden erfolgt, ist die Genauigkeit begrenzt (000000000..999000000). %N kann zwischen % und N eine Breitenangabe enthalten. Dies ist nützlich zur Darstellung von Millisekunden (%3N) oder Mikrosekunden (%6N). Die voreingestellte und maximale Breite ist 9 (%N = %9N).

Siehe auch den Konverter utime für UTC sowie die Konverter "ltime" und "us_ltime".

Beispiel:

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/11:53:02.196 +0200 127.0.0.1:41530
log-format %[accept_date(ms),ms_ltime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-ms-utime"></a>

**`ms_utime(<format>[,<offset>])`**

```haproxy
ms_utime(<format>[,<offset>])
```

Funktioniert wie "utime", erwartet die Eingabe aber in Millisekunden. Unterstützt außerdem das von date(1) inspirierte Konvertierungskennzeichen %N. Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in UTC-Zeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Millisekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime().

Mit dem Konvertierungskennzeichen %N lässt sich der Nanosekundenanteil des Datums ausgeben. Da die Eingabe in Millisekunden erfolgt, ist die Genauigkeit begrenzt (000000000..999000000). %N kann zwischen % und N eine Breitenangabe enthalten. Dies ist nützlich zur Darstellung von Millisekunden (%3N) oder Mikrosekunden (%6N). Die voreingestellte und maximale Breite ist 9 (%N = %9N).

Siehe auch den Konverter ltime für Ortszeit sowie die Konverter "utime" und "us_utime".

Beispiel:

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196 +0000 127.0.0.1:41530
log-format %[accept_date(ms),ms_utime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-mul"></a>

**`mul(<value>)`**

```haproxy
mul(<value>)
```

Multipliziert den vorzeichenbehafteten ganzzahligen Eingabewert mit `<value>` und gibt das Produkt als vorzeichenbehaftete Ganzzahl zurück. Bei einem Überlauf wird der für das Vorzeichen größtmögliche Wert zurückgegeben, sodass die Operation nicht umläuft. `<value>` kann ein numerischer Wert oder ein Variablenname sein. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-nbsrv"></a>

**`nbsrv`**

```haproxy
nbsrv
```

Nimmt einen Eingabewert vom Typ string, interpretiert ihn als Backend-Namen und gibt die Anzahl der nutzbaren Server in diesem Backend zurück. Dies eignet sich für Stellen, an denen ein Backend anhand eines dynamischen Namens gesucht werden soll, beispielsweise anhand des Ergebnisses einer Map-Suche.

<a id="entry-7-3-1-neg"></a>

**`neg`**

```haproxy
neg
```

Nimmt den vorzeichenbehafteten ganzzahligen Eingabewert, berechnet den entgegengesetzten Wert und gibt den Rest als vorzeichenbehaftete Ganzzahl zurück. 0 bleibt unverändert. Dieser Operator ist für Subtraktionen mit umgekehrter Operandenreihenfolge vorgesehen: Um die Eingabe von einer Konstanten abzuziehen, genügt "neg,add(value)".

<a id="entry-7-3-1-not"></a>

**`not`**

```haproxy
not
```

Gibt den booleschen Wert FALSE zurück, wenn der vorzeichenbehaftete ganzzahlige Eingabewert ungleich null ist, andernfalls TRUE. In Verbindung mit and() kann dies dazu dienen, bei Bitprüfungen von Eingabewerten true/false zurückzugeben, beispielsweise um das Fehlen eines Flags zu prüfen.

<a id="entry-7-3-1-odd"></a>

**`odd`**

```haproxy
odd
```

Gibt den booleschen Wert TRUE zurück, wenn der vorzeichenbehaftete ganzzahlige Eingabewert ungerade ist, andernfalls FALSE. Dies ist funktional gleichbedeutend mit "and(1),bool".

<a id="entry-7-3-1-or"></a>

**`or(<value>)`**

```haproxy
or(<value>)
```

Führt ein bitweises "OR" zwischen `<value>` und dem vorzeichenbehafteten ganzzahligen Eingabewert aus und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. `<value>` kann ein numerischer Wert oder ein Variablenname sein. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-param"></a>

**`param(<name>[,<delim>])`**

```haproxy
param(<name>[,<delim>])
```

Extrahiert das erste Vorkommen des Parameters `<name>` aus der Eingabezeichenkette. Die Parameter werden durch `<delim>` getrennt, standardmäßig "&"; Name und Wert eines Parameters werden durch "=" getrennt. Gibt es vor dem Ende des Parameterabschnitts kein "=" und keinen Wert, entspricht dies dem Wert einer leeren Zeichenkette.

Dies kann zum Extrahieren von Parametern aus einer Abfragezeichenkette oder gegebenenfalls aus einem x-www-form-urlencoded-Nachrichtenkörper nützlich sein. Insbesondere kann `query,param(<name>)` als Alternative zu `urlp(<name>)` verwendet werden, die nur "&" als Trennzeichen nutzt, während "urlp" auch "?" und ";" verwendet.

Dieser Konverter behandelt URL-kodierte Zeichen nicht gesondert. Zum Dekodieren des Werts können Sie den Konverter url_dec auf die Ausgabe anwenden. Kann der Parametername in der Eingabe kodierte Zeichen enthalten, sollten Sie die Eingabe vermutlich vor dem Aufruf von "param" normalisieren. Dies ist mit "http-request normalize-uri" möglich, insbesondere mit den Optionen percent-decode-unreserved und percent-to-uppercase.

Beispiel:

```text
str(a=b&c=d&a=r),param(a)   # b
str(a&b=c),param(a)         # ""
str(a=&b&c=a),param(b)      # ""
str(a=1;b=2;c=4),param(b,;) # 2
query,param(redirect_uri),urldec()
```

<a id="entry-7-3-1-port-only"></a>

**`port_only`**

```haproxy
port_only
```

Wandelt eine Zeichenkette mit dem Wert eines Host-Headers in eine Ganzzahl um, indem der enthaltene Port zurückgegeben wird. Die Eingabe muss dem Format des Host-Headerwerts entsprechen (rfc9110#section-7.2). Unterstützt werden Eingaben dieser Art: hostname, hostname:80, 127.0.0.1, 127.0.0.1:80, [::1], [::1]:80.

Enthält die Eingabe keinen Port, wird 0 zurückgegeben.

Siehe auch den Konverter "host_only", der den Host zurückgibt.

<a id="entry-7-3-1-protobuf"></a>

**`protobuf(<field_number>[,<field_type>])`**

```haproxy
protobuf(<field_number>[,<field_type>])
```

Extrahiert aus einem binären Eingabe-Sample, das eine Protocol-Buffers-Nachricht darstellt, das Nachrichtenfeld mit der Feldnummer `<field_number>` (Punktnotation). Ist `<field_type>` nicht angegeben, erfolgt die Extraktion als Rohdaten; andernfalls als ganzzahliges Sample (siehe auch "ungrpc" weiter unten). Zulässig sind folgende Typen: "int32", "int64", "uint32", "uint64", "sint32", "sint64", "bool", "enum" für den Wire-Typ "varint" 0; "fixed64", "sfixed64", "double" für den 64bit-Wire-Typ 1; "fixed32", "sfixed32", "float" für den Wire-Typ 5. "string" gilt als längenbegrenzter Typ und benötigt daher zur Extraktion kein Argument `<field_type>`. Weitere Informationen zu den Feldtypen von Protocol-Buffers-Nachrichten stehen hier: <https://developers.google.com/protocol-buffers/docs/encoding>

<a id="entry-7-3-1-regsub"></a>

**`regsub(<regex>,<subst>[,<flags>])`**

```haproxy
regsub(<regex>,<subst>[,<flags>])
```

Wendet eine Ersetzung anhand eines regulären Ausdrucks auf die Eingabezeichenkette an. Führt dieselbe Operation aus wie das bekannte Programm "sed" mit "s/`<regex>`/`<subst>`/". Standardmäßig wird in der Eingabezeichenkette das erste Vorkommen des längsten auf den regulären Ausdruck `<regex>` passenden Teils durch die Ersetzungszeichenkette `<subst>` ersetzt. Mit dem Flag "g" im dritten Argument `<flags>` lassen sich stattdessen alle Vorkommen ersetzen. Mit dem Flag "i" in `<flags>` lässt sich außerdem die Beachtung der Groß-/Kleinschreibung beim regulären Ausdruck ausschalten. Da `<flags>` eine Zeichenkette ist, werden alle gewünschten Flags aneinandergehängt. Sind sowohl "i" als auch "g" gewünscht, haben "gi" und "ig" somit dieselbe Wirkung. Der wichtigste Anwendungsfall dieses Konverters ist das Ersetzen bestimmter Zeichen oder Zeichenfolgen durch andere.

Es wird dringend empfohlen, den regulären Ausdruck in geschützte Anführungszeichen einzuschließen. Dies verbessert die Lesbarkeit und verhindert, dass eine schließende Klammer im regulären Ausdruck mit der Funktionsklammer verwechselt wird. Wie in der Bourne-Shell wird die erste Ebene von Anführungszeichen beim Abgrenzen von Wortgruppen in der Zeile verarbeitet; eine zweite Ebene kann für Argumente verwendet werden. Für die äußere Ebene werden einfache Anführungszeichen empfohlen, da darin weder Rückstriche noch Dollarzeichen aufgelöst werden.

Beispiele:

```shell
# de-duplicate "/" in header "x-path".
# input:  x-path: /////a///b/c/xzxyz/
# output: x-path: /a/b/c/xzxyz/
http-request set-header x-path "%[hdr(x-path),regsub('/+','/','g')]"

# copy query string to x-query and drop all leading '?', ';' and '&'
http-request set-header x-query "%[query,regsub([?;&]*,'')]"

# capture groups and backreferences
# both lines do the same.
http-request redirect location %[url,'regsub("(foo|bar)([0-9]+)?","\2\1",i)']
http-request redirect location %[url,regsub(\"(foo|bar)([0-9]+)?\",\"\2\1\",i)]
```

<a id="entry-7-3-1-reverse"></a>

**`reverse`**

```haproxy
reverse
```

Kehrt die Eingabezeichenkette Byte für Byte um.

Dieser Konverter arbeitet unabhängig von der Kodierung und kehrt Bytes statt Zeichen um. Er eignet sich daher nicht zum Umkehren von menschlichem Text in UTF-8-Kodierung.

Damit lassen sich Suffixsuchen in der ursprünglichen Zeichenkette in Präfixsuchen in der umgekehrten Zeichenkette umwandeln. Dadurch können bei großen Maps indizierte Präfix-Abgleichfunktionen wie "map_beg" verwendet werden.

Beispiele:

```shell
"example.com" -> "moc.elpmaxe"
"ab cd" -> "dc ba"

# Given a map file where each key contains a reversed hostname:
#   moc.elpmaxe.ppa app1
#   moc.elpmaxe.bd  dbcluster
# Pick a backend based on the domain suffix of the Host header:
use_backend %[req.hdr(host),lower,reverse,map_beg(/etc/haproxy/hosts.map,default)]
```

<a id="entry-7-3-1-reverse-dom"></a>

**`reverse_dom`**

```haproxy
reverse_dom
```

Wandelt eine Zeichenkette mit einem FQDN-artigen Hostnamen in eine Form mit umgekehrter Reihenfolge der Labels um. Ein einzelner abschließender Punkt in der Eingabe wird ignoriert. Leere Labels lassen den Konverter fehlschlagen.

Dieser Konverter wandelt seine Eingabe weder in Kleinbuchstaben um noch entfernt er einen Port. Bei Bedarf soll er mit vorhandenen Konvertern wie "lower" oder "host_only" kombiniert werden.

Die Behandlung des abschließenden Punkts bleibt bewusst dem Aufrufer überlassen. So können Aufrufer entscheiden, ob sie auch die Stammdomain oder nur Subdomains abgleichen möchten.

Die Form mit umgekehrter Labelreihenfolge ist für große Domain-Maps nützlich, weil sie Domain-Suffixsuchen in Präfixsuchen umwandelt. Damit lassen sich indizierte Präfix-Abgleichfunktionen wie "map_beg" verwenden.

Beispiele:

```shell
"example.com" -> "com.example"
"mail.example.com" -> "com.example.mail"
"example.com." -> "com.example"

# match only subdomains of example.net, not the apex
acl example_net_sub req.hdr(Host),host_only,reverse_dom -m beg net.example.

# match only the apex
acl example_net_apex req.hdr(Host),host_only,reverse_dom -i net.example

# exact-or-subdomain prefix lookup using an explicit dotted form
http-request set-var(txn.rev_host) req.hdr(Host),host_only,reverse_dom,concat(.)
use_backend %[var(txn.rev_host),map_beg(/etc/haproxy/domains.map)]
```

<a id="entry-7-3-1-rfc7239-field"></a>

**`rfc7239_field(<field>)`**

```haproxy
rfc7239_field(<field>)
```

Extrahiert ein einzelnes Feld bzw. einen einzelnen Parameter aus einem als Eingabe übergebenen, RFC-7239-konformen Headerwert.

Unterstützte Felder sind: - proto: entweder 'http' oder 'https' - host: HTTP-konformer Host - for: RFC7239-Knoten - by: RFC7239-Knoten

Weitere Informationen stehen hier:

```text
https://www.rfc-editor.org/rfc/rfc7239.html#section-6
```

Beispiel:

```shell
# extract host field from forwarded header and store it in req.fhost var
http-request set-var(req.fhost) req.hdr(forwarded),rfc7239_field(host)
#input: "proto=https;host=\"haproxy.org:80\""
#  output: "haproxy.org:80"

# extract for field from forwarded header and store it in req.ffor var
http-request set-var(req.ffor) req.hdr(forwarded),rfc7239_field(for)
#input: "proto=https;host=\"haproxy.org:80\";for=\"127.0.0.1:9999\""
#  output: "127.0.0.1:9999"
```

<a id="entry-7-3-1-rfc7239-is-valid"></a>

**`rfc7239_is_valid`**

```haproxy
rfc7239_is_valid
```

Gibt true zurück, wenn der eingegebene Header einen RFC-7239-konformen Headerwert enthält, andernfalls false.

Beispiel:

```shell
acl valid req.hdr(forwarded),rfc7239_is_valid
#input: "for=127.0.0.1;proto=http"
#  output: TRUE
#input: "proto=custom"
#  output: FALSE
```

<a id="entry-7-3-1-rfc7239-n2nn"></a>

**`rfc7239_n2nn`**

```haproxy
rfc7239_n2nn
```

Wandelt einen RFC7239-Knoten (aus den 7239-Headerfeldern 'for' oder 'by') in seine entsprechende endgültige Knotennamensform um: - ipv4-Adresse - ipv6-Adresse - 'unknown' - Bezeichner '\_obfs'

Beispiel:

```shell
# extract 'for' field from forwarded header, extract nodename from
# resulting node identifier and store the result in req.fnn
http-request set-var(req.fnn) req.hdr(forwarded),rfc7239_field(for),rfc7239_n2nn
#input: "127.0.0.1:9999"
#  output: 127.0.0.1 (ipv4)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: ab:cd:ff:ff:ff:ff:ff:ff (ipv6)
#input: "_name:_port"
#  output: "_name" (string)
```

<a id="entry-7-3-1-rfc7239-n2np"></a>

**`rfc7239_n2np`**

```haproxy
rfc7239_n2np
```

Wandelt einen RFC7239-Knoten (aus den 7239-Headerfeldern 'for' oder 'by') in seine entsprechende endgültige Knotenportform um: - vorzeichenlose Ganzzahl - Bezeichner '\_obfs'

Beispiel:

```shell
# extract 'by' field from forwarded header, extract node port from
# resulting node identifier and store the result in req.fnp
http-request set-var(req.fnp) req.hdr(forwarded),rfc7239_field(by),rfc7239_n2np
#input: "127.0.0.1:9999"
#  output: 9999 (integer)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: 9998 (integer)
#input: "_name:_port"
#  output: "_port" (string)
```

<a id="entry-7-3-1-rfc7239-nn"></a>

**`rfc7239_nn`**

```haproxy
rfc7239_nn
```

Wandelt die übergebene Adresse oder Zeichenkette in einen RFC7239-konformen Knotennamen um. Dies kann verwendet werden, um die 7239-Headerfelder 'for' oder 'by' manuell zu erstellen.

Ist die übergebene Eingabe eine Zeichenkette, wird ihr automatisch das Zeichen '\_' vorangestellt, um einen verschleierten Bezeichner darzustellen. Die Zeichenkette muss dem Zeichensatz von RFC7239 entsprechen. Ist die Zeichenkette leer, wird sie in den Bezeichner "unknown" umgewandelt.

Beispiel:

```shell
#input: ipv6(ab:cd:ff:ff:ff:ff:ff:ff)
#  output: "[ab:cd:ff:ff:ff:ff:ff:ff]"
#input: str(test)
#  output: "_test"
#input: str()
#  output: "unknown"
```

Siehe auch: "rfc7239_np"

<a id="entry-7-3-1-rfc7239-np"></a>

**`rfc7239_np`**

```haproxy
rfc7239_np
```

Wandelt die übergebene vorzeichenlose Ganzzahl oder Zeichenkette in einen RFC7239-konformen Knotenport um. Dies kann verwendet werden, um die 7239-Headerfelder 'for' oder 'by' manuell zu erstellen.

Ist die übergebene Eingabe eine Zeichenkette, wird ihr automatisch das Zeichen '\_' vorangestellt, um einen verschleierten Bezeichner darzustellen. Die Zeichenkette muss dem Zeichensatz von RFC7239 entsprechen und darf nicht leer sein.

Beispiel:

```shell
#input: int(12)
#  output: "12"
#input: str(test)
#  output: "_test"

# build 'for' forwarded header field
http-request set-var-fmt(txn.test) "for=\"%[ipv6(::1),rfc7239_nn]:%[int(8080),rfc7239_np]\";"
#  output: "for=\"[::1]:8080\";"

# build RFC-compliant 7239 header:
http-request set-var-fmt(txn.forwarded) "for=\"%[ipv6(::1),rfc7239_nn]:%[str(8888),rfc7239_np]\";host=\"haproxy.org\";proto=http"
# check RFC-compliancy:
http-request set-var(txn.test) "var(txn.forwarded),debug(test,stderr),rfc7239_is_valid,debug(test,stderr)"
#  stderr output:
#    [debug] test: type=str <for="[::1]:_8888";host="haproxy.org";proto=http>
#    [debug] test: type=bool <1>
```

Siehe auch: "rfc7239_nn"

<a id="entry-7-3-1-rtrim"></a>

**`rtrim(<chars>)`**

```haproxy
rtrim(<chars>)
```

Überspringt am Ende der Zeichenkettendarstellung des Eingabe-Samples alle Zeichen aus `<chars>`.

<a id="entry-7-3-1-sdbm"></a>

**`sdbm([<avalanche>])`**

```haproxy
sdbm([<avalanche>])
```

Bildet mit der SDBM-Hashfunktion aus einem binären Eingabe-Sample einen vorzeichenlosen 32-Bit-Wert. Ist das optionale Argument `<avalanche>` gleich 1, kann zusätzlich eine vollständige Avalanche-Hashfunktion auf die Ausgabe angewendet werden. Dieser Konverter verwendet dieselben Funktionen wie die verschiedenen Hash-basierten Algorithmen zur Lastverteilung und liefert daher exakt dieselben Ergebnisse. Er ist hauptsächlich zur Fehlersuche gedacht, kann aber als Eintrag in einer Stick Table zum Erfassen grober Statistiken verwendet werden. Er darf nicht für Sicherheitszwecke verwendet werden, da ein 32-Bit-Hash leicht zu brechen ist. Siehe auch "crc32", "djb2", "wt6", "crc32c" und die Direktive "hash-type".

<a id="entry-7-3-1-secure-memcmp"></a>

**`secure_memcmp(<var>)`**

```haproxy
secure_memcmp(<var>)
```

Vergleicht den Inhalt von `<var>` mit dem Eingabewert. Beide Werte werden als binäre Zeichenketten behandelt. Gibt einen booleschen Wert zurück, der angibt, ob beide binären Zeichenketten übereinstimmen.

Haben beide binären Zeichenketten dieselbe Länge, wird der Vergleich in konstanter Zeit ausgeführt.

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

Beispiel:

```shell
http-request set-var(txn.token) hdr(token)
# Check whether the token sent by the client matches the secret token
# value, without leaking the contents using a timing attack.
acl token_given str(my_secret_token),secure_memcmp(txn.token)
```

<a id="entry-7-3-1-set-var"></a>

**`set-var(<var>[,<cond>...])`**

```haproxy
set-var(<var>[,<cond>...])
```

Setzt eine Variable auf den Eingabeinhalt und gibt diesen Inhalt unverändert aus, wenn alle angegebenen Bedingungen wahr sind (eine Liste der möglichen Bedingungen folgt unten). Die Variable behält den Wert und den zugehörigen Eingabetyp. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

Sie können dem Konverter höchstens vier der folgenden Bedingungen übergeben:

- "ifexists"/"ifnotexists":

```text
Prüft, ob die Variable bereits vor dem aktuellen set-var-Aufruf existierte.
Eine Variable wird normalerweise durch einen erfolgreichen set-var-Aufruf angelegt.
Variablen im Gültigkeitsbereich "proc" werden beim Einlesen der Konfiguration
angelegt; für sie ist die Bedingung "ifexists" daher immer wahr.
```

- "ifempty"/"ifnotempty":

```text
Prüft, ob die Eingabe leer ist.
Skalare Typen sind nie leer; die Bedingung ifempty ist für sie daher unabhängig
vom Inhalt der Eingabe immer falsch (Ganzzahlen, boolesche Werte, IPs ...).
```

- "ifset"/"ifnotset":

```text
Prüft, ob die Variable zuvor gesetzt wurde oder ob unset-var
für die Variable aufgerufen wurde.
Eine noch nicht existierende Variable gilt als nicht gesetzt. Eine "proc"-Variable
kann existieren, ohne gesetzt zu sein, da solche Variablen beim Einlesen
der Konfiguration angelegt werden.
```

- "ifgt"/"iflt":

```text
Prüft, ob der Inhalt der Variablen „größer als“ oder „kleiner als“
die Eingabe ist. Diese Prüfung kann nur durchgeführt werden, wenn sowohl
die Eingabe als auch die Variable vom Typ integer sind. Andernfalls gilt
die Prüfung standardmäßig als wahr.
```

<a id="entry-7-3-1-sha1"></a>

**`sha1`**

```haproxy
sha1
```

Wandelt ein binäres Eingabe-Sample in einen SHA-1-Digest um. Das Ergebnis ist ein binäres Sample mit einer Länge von 20 Bytes.

<a id="entry-7-3-1-sha2"></a>

**`sha2([<bits>])`**

```haproxy
sha2([<bits>])
```

Wandelt ein binäres Eingabe-Sample in einen Digest der SHA-2-Familie um. Das Ergebnis ist ein binäres Sample mit einer Länge von `<bits>`/8 Bytes.

Gültige Werte für `<bits>` sind 224, 256, 384 und 512; sie entsprechen jeweils SHA-`<bits>`. Der Standardwert ist 256.

Dieser Konverter ist nur verfügbar, wenn HAProxy mit USE_OPENSSL kompiliert wurde.

<a id="entry-7-3-1-srv-is-up"></a>

**`srv_is_up`**

```haproxy
srv_is_up
```

Nimmt einen Eingabewert vom Typ string, entweder einen Servernamen oder im Format `<backend>`/`<server>`, und gibt true zurück, wenn der bezeichnete Server derzeit UP ist. Dies eignet sich für Stellen, an denen der Serverstatus anhand eines dynamischen Namens abgefragt werden soll, beispielsweise anhand eines Cookie-Werts (z. B. req.cook(SRVID),srv_is_up), um anschließend zu entscheiden, ob eine Anfrage an ein anderes Ziel geleitet werden soll. Beachten Sie vor der Verwendung, dass dieser Konverter bei unkontrollierten Eingabedaten einem externen Beobachter ermöglichen könnte, den Zustand jedes Servers in der gesamten Konfiguration abzufragen. Dies ist in manchen Umgebungen möglicherweise nicht akzeptabel.

<a id="entry-7-3-1-srv-queue"></a>

**`srv_queue`**

```haproxy
srv_queue
```

Nimmt einen Eingabewert vom Typ string, entweder einen Servernamen oder im Format `<backend>`/`<server>`, und gibt die Anzahl der Streams in der Warteschlange dieses Servers zurück. Dies eignet sich für Stellen, an denen wartende Streams anhand eines dynamischen Namens abgefragt werden sollen, beispielsweise anhand eines Cookie-Werts (z. B. req.cook(SRVID),srv_queue), um anschließend zu entscheiden, ob die Persistenz aufgehoben oder eine Anfrage an ein anderes Ziel geleitet werden soll. Beachten Sie vor der Verwendung, dass dieser Konverter bei unkontrollierten Eingabedaten einem externen Beobachter ermöglichen könnte, den Zustand jedes Servers in der gesamten Konfiguration abzufragen. Dies ist in manchen Umgebungen möglicherweise nicht akzeptabel.

<a id="entry-7-3-1-strcmp"></a>

**`strcmp(<var>)`**

```haproxy
strcmp(<var>)
```

Vergleicht den Inhalt von `<var>` mit dem Eingabewert vom Typ string. Gibt das Ergebnis als vorzeichenbehaftete Ganzzahl entsprechend strcmp(3) zurück: 0, wenn beide Zeichenketten identisch sind. Einen Wert kleiner als 0, wenn die linke Zeichenkette lexikografisch kleiner als die rechte oder die linke Zeichenkette kürzer ist. Andernfalls einen Wert größer als 0 (rechte Zeichenkette größer als linke Zeichenkette oder rechte Zeichenkette kürzer).

Siehe auch den Konverter secure_memcmp, wenn Sie zwei binäre Zeichenketten in konstanter Zeit vergleichen müssen.

Beispiel:

```shell
http-request set-var(txn.host) hdr(host)
# Check whether the client is attempting domain fronting.
acl ssl_sni_http_host_match ssl_fc_sni,strcmp(txn.host) eq 0

```

<a id="entry-7-3-1-sub"></a>

**`sub(<value>)`**

```haproxy
sub(<value>)
```

Subtrahiert `<value>` vom vorzeichenbehafteten ganzzahligen Eingabewert und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. Hinweis: Um die Eingabe von einer Konstanten abzuziehen, genügt "neg,add(value)". `<value>` kann ein numerischer Wert oder ein Variablenname sein. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-table-bytes-in-rate"></a>

**`table_bytes_in_rate([<table>])`**

```haproxy
table_bytes_in_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die dem Eingabe-Sample in der angegebenen Tabelle zugeordnete durchschnittliche Byterate vom Client zum Server zurück, gemessen als Anzahl von Bytes über den in der Tabelle konfigurierten Zeitraum. Siehe auch das Sample-Abruf-Schlüsselwort sc_bytes_in_rate.

<a id="entry-7-3-1-table-bytes-out-rate"></a>

**`table_bytes_out_rate([<table>])`**

```haproxy
table_bytes_out_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Byterate vom Server zum Client zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Diese wird als Anzahl von Bytes über den in der Tabelle konfigurierten Zeitraum gemessen. Siehe auch das Sample-Abruf-Schlüsselwort sc_bytes_out_rate.

<a id="entry-7-3-1-table-clr-gpc"></a>

**`table_clr_gpc(<idx>[,<table>])`**

```haproxy
table_clr_gpc(<idx>[,<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Setzt den Allzweckzähler am Index `<idx>` des Arrays gpc zurück und gibt seinen vorherigen Wert zurück. `<idx>` ist eine Ganzzahl zwischen 0 und 99. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 0 zurückgegeben. Dieser Konverter gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'. Siehe auch das Sample-Abruf-Schlüsselwort sc_clr_gpc.

<a id="entry-7-3-1-table-clr-gpc0"></a>

**`table_clr_gpc0([<table>])`**

```haproxy
table_clr_gpc0([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Setzt den ersten Allzweckzähler '0' zurück und gibt seinen vorherigen Wert zurück. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 0 zurückgegeben. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf:

Beispiel:

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse src_http_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 5
acl save  src,table_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

Siehe auch das Sample-Abruf-Schlüsselwort sc_clr_gpc0.

<a id="entry-7-3-1-table-clr-gpc1"></a>

**`table_clr_gpc1([<table>])`**

```haproxy
table_clr_gpc1([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Setzt den ersten Allzweckzähler '1' zurück und gibt seinen vorherigen Wert zurück. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 0 zurückgegeben. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf. Siehe auch das Sample-Abruf-Schlüsselwort sc_clr_gpc1.

<a id="entry-7-3-1-table-conn-cnt"></a>

**`table_conn_cnt([<table>])`**

```haproxy
table_conn_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl eingehender Verbindungen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_conn_cnt.

<a id="entry-7-3-1-table-conn-cur"></a>

**`table_conn_cur([<table>])`**

```haproxy
table_conn_cur([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die aktuelle Anzahl gleichzeitig verfolgter Verbindungen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_conn_cur.

<a id="entry-7-3-1-table-conn-rate"></a>

**`table_conn_rate([<table>])`**

```haproxy
table_conn_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Rate eingehender Verbindungen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_conn_rate.

<a id="entry-7-3-1-table-expire"></a>

**`table_expire([<table>[,<default_value>]])`**

```haproxy
table_expire([<table>[,<default_value>]])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, schlägt der Konverter fehl, außer wenn `<default_value>` gesetzt ist: Dann ist der Konverter erfolgreich und gibt `<default_value>` zurück. Wird der Schlüssel gefunden, gibt der Konverter die verbleibende Zeit bis zum Ablauf des Schlüssels zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort table_idle.

<a id="entry-7-3-1-table-glitch-cnt"></a>

**`table_glitch_cnt([<table>])`**

```haproxy
table_glitch_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl von Störungen der Frontend-Verbindung zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_glitch_cnt und fc_glitches für den auf der aktuellen Frontend-Verbindung gemessenen Wert.

<a id="entry-7-3-1-table-glitch-rate"></a>

**`table_glitch_rate([<table>])`**

```haproxy
table_glitch_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Störungsrate der Frontend-Verbindung zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_glitch_rate.

<a id="entry-7-3-1-table-gpc"></a>

**`table_gpc(<idx>[,<table>])`**

```haproxy
table_gpc(<idx>[,<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter den aktuellen Wert des Allzweckzählers am Index `<idx>` des Arrays zurück, das dem Eingabe-Sample in der angegebenen `<table>` zugeordnet ist. `<idx>` ist eine Ganzzahl zwischen 0 und 99. Ist an diesem Index kein GPC gespeichert, wird ebenfalls die Ganzzahl 0 zurückgegeben. Dies gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpc.

<a id="entry-7-3-1-table-gpc0"></a>

**`table_gpc0([<table>])`**

```haproxy
table_gpc0([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter den aktuellen Wert des ersten Allzweckzählers zurück, der dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpc0.

<a id="entry-7-3-1-table-gpc0-rate"></a>

**`table_gpc0_rate([<table>])`**

```haproxy
table_gpc0_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die Häufigkeit zurück, mit der der dem Eingabe-Sample zugeordnete Zähler gpc0 über den in der angegebenen Tabelle konfigurierten Zeitraum erhöht wurde. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpc0_rate.

<a id="entry-7-3-1-table-gpc1"></a>

**`table_gpc1([<table>])`**

```haproxy
table_gpc1([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter den aktuellen Wert des zweiten Allzweckzählers zurück, der dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpc1.

<a id="entry-7-3-1-table-gpc1-rate"></a>

**`table_gpc1_rate([<table>])`**

```haproxy
table_gpc1_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die Häufigkeit zurück, mit der der dem Eingabe-Sample zugeordnete Zähler gpc1 über den in der angegebenen Tabelle konfigurierten Zeitraum erhöht wurde. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpc1_rate.

<a id="entry-7-3-1-table-gpc-rate"></a>

**`table_gpc_rate(<idx>[,<table>])`**

```haproxy
table_gpc_rate(<idx>[,<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die Häufigkeit zurück, mit der der Allzweckzähler am Index `<idx>` des Arrays über den konfigurierten Zeitraum erhöht wurde. Das Array ist dem Eingabe-Sample in der angegebenen Stick Table `<table>` zugeordnet. `<idx>` ist eine Ganzzahl zwischen 0 und 99. Ist an diesem Index kein gpc_rate gespeichert, wird ebenfalls die Ganzzahl 0 zurückgegeben. Dies gilt nur für den Array-data_type 'gpc_rate', nicht für die älteren data_types 'gpc0_rate' oder 'gpc1_rate'. Siehe auch das Sample-Abruf-Schlüsselwort sc_gpc_rate.

<a id="entry-7-3-1-table-gpt"></a>

**`table_gpt(<idx>[,<table>])`**

```haproxy
table_gpt(<idx>[,<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter den aktuellen Wert des Allzweck-Tags am Index `<idx>` des Arrays zurück, das dem Eingabe-Sample in der angegebenen `<table>` zugeordnet ist. `<idx>` ist eine Ganzzahl zwischen 0 und 99. Ist an diesem Index kein GPT gespeichert, wird ebenfalls die Ganzzahl 0 zurückgegeben. Dies gilt nur für den Array-data_type 'gpt', nicht für den älteren data-type 'gpt0'. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpt.

<a id="entry-7-3-1-table-gpt0"></a>

**`table_gpt0([<table>])`**

```haproxy
table_gpt0([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter den aktuellen Wert des ersten Allzweck-Tags zurück, das dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_get_gpt0.

<a id="entry-7-3-1-table-http-err-cnt"></a>

**`table_http_err_cnt([<table>])`**

```haproxy
table_http_err_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl von HTTP-Fehlern zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_err_cnt.

<a id="entry-7-3-1-table-http-err-rate"></a>

**`table_http_err_rate([<table>])`**

```haproxy
table_http_err_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Rate von HTTP-Fehlern zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Diese wird als Anzahl von Fehlern über den in der Tabelle konfigurierten Zeitraum gemessen. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_err_rate.

<a id="entry-7-3-1-table-http-fail-cnt"></a>

**`table_http_fail_cnt([<table>])`**

```haproxy
table_http_fail_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl von HTTP-Fehlschlägen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_fail_cnt.

<a id="entry-7-3-1-table-http-fail-rate"></a>

**`table_http_fail_rate([<table>])`**

```haproxy
table_http_fail_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Rate von HTTP-Fehlschlägen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Diese wird als Anzahl von Fehlschlägen über den in der Tabelle konfigurierten Zeitraum gemessen. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_fail_rate.

<a id="entry-7-3-1-table-http-req-cnt"></a>

**`table_http_req_cnt([<table>])`**

```haproxy
table_http_req_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl von HTTP-Anfragen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_req_cnt.

<a id="entry-7-3-1-table-http-req-rate"></a>

**`table_http_req_rate([<table>])`**

```haproxy
table_http_req_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Rate von HTTP-Anfragen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Diese wird als Anzahl von Anfragen über den in der Tabelle konfigurierten Zeitraum gemessen. Siehe auch das Sample-Abruf-Schlüsselwort sc_http_req_rate.

<a id="entry-7-3-1-table-idle"></a>

**`table_idle([<table>[,<default_value>]])`**

```haproxy
table_idle([<table>[,<default_value>]])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, schlägt der Konverter fehl, außer wenn `<default_value>` gesetzt ist: Dann ist der Konverter erfolgreich und gibt `<default_value>` zurück. Wird der Schlüssel gefunden, gibt der Konverter die Zeit zurück, die der dem Eingabe-Sample in der angegebenen Tabelle zugeordnete Schlüsseleintrag seit seiner letzten Aktualisierung inaktiv geblieben ist. Siehe auch das Sample-Abruf-Schlüsselwort table_expire.

<a id="entry-7-3-1-table-inc-gpc"></a>

**`table_inc_gpc(<idx>[,<table>])`**

```haproxy
table_inc_gpc(<idx>[,<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Erhöht den Allzweckzähler am Index `<idx>` des Arrays und gibt seinen neuen Wert zurück. `<idx>` ist eine Ganzzahl zwischen 0 und 99. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 1 zurückgegeben. Dieser Konverter gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'. Siehe auch sc_inc_gpc.

<a id="entry-7-3-1-table-inc-gpc0"></a>

**`table_inc_gpc0([<table>])`**

```haproxy
table_inc_gpc0([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Erhöht den Allzweckzähler '0' und gibt seinen neuen Wert zurück. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 1 zurückgegeben. Siehe auch sc0/sc2/sc2_inc_gpc0. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf:

Beispiel:

```text
acl abuse src,table_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-1-table-inc-gpc1"></a>

**`table_inc_gpc1([<table>])`**

```haproxy
table_inc_gpc1([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Erhöht den Allzweckzähler '1' und gibt seinen neuen Wert zurück. Wird der Eintrag nicht gefunden, wird ein Eintrag erstellt und 1 zurückgegeben. Siehe auch sc0/sc2/sc2_inc_gpc1. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf.

<a id="entry-7-3-1-table-kbytes-in"></a>

**`table_kbytes_in([<table>])`**

```haproxy
table_kbytes_in([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Datenmenge vom Client zum Server zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist, gemessen in Kilobytes. Die Prüfung erfolgt derzeit mit 32-Bit-Ganzzahlen, wodurch die Werte auf 4 Terabytes begrenzt sind. Siehe auch das Sample-Abruf-Schlüsselwort sc_kbytes_in.

<a id="entry-7-3-1-table-kbytes-out"></a>

**`table_kbytes_out([<table>])`**

```haproxy
table_kbytes_out([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Datenmenge vom Server zum Client zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist, gemessen in Kilobytes. Die Prüfung erfolgt derzeit mit 32-Bit-Ganzzahlen, wodurch die Werte auf 4 Terabytes begrenzt sind. Siehe auch das Sample-Abruf-Schlüsselwort sc_kbytes_out.

<a id="entry-7-3-1-table-server-id"></a>

**`table_server_id([<table>])`**

```haproxy
table_server_id([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die Server-ID zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Eine Server-ID wird einem Sample durch eine "stick"-Regel zugeordnet, wenn eine Verbindung zu einem Server erfolgreich hergestellt wird. Eine Server-ID von null bedeutet, dass diesem Schlüssel kein Server zugeordnet ist.

<a id="entry-7-3-1-table-sess-cnt"></a>

**`table_sess_cnt([<table>])`**

```haproxy
table_sess_cnt([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die kumulierte Anzahl eingehender Sitzungen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Eine Sitzung bezeichnet hier eine eingehende Verbindung, die von den Regelsätzen "tcp-request connection" akzeptiert wurde. Siehe auch das Sample-Abruf-Schlüsselwort sc_sess_cnt.

<a id="entry-7-3-1-table-sess-rate"></a>

**`table_sess_rate([<table>])`**

```haproxy
table_sess_rate([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die durchschnittliche Rate eingehender Sitzungen zurück, die dem Eingabe-Sample in der angegebenen Tabelle zugeordnet ist. Eine Sitzung bezeichnet hier eine eingehende Verbindung, die von den Regelsätzen "tcp-request connection" akzeptiert wurde. Siehe auch das Sample-Abruf-Schlüsselwort sc_sess_rate.

<a id="entry-7-3-1-table-trackers"></a>

**`table_trackers([<table>])`**

```haproxy
table_trackers([<table>])
```

Verwendet das Eingabe-Sample für eine Suche in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Wird der Schlüssel in der Tabelle nicht gefunden, wird die Ganzzahl null zurückgegeben. Andernfalls gibt der Konverter die aktuelle Anzahl gleichzeitiger Verbindungen zurück, die in der angegebenen Tabelle denselben Schlüssel wie das Eingabe-Sample verfolgen. Anders als table_conn_cur beruht dies nicht auf gespeicherten Informationen, sondern auf dem Referenzzähler der Tabelle (dem Wert "use", den "show table" auf der CLI zurückgibt). Dies kann für das Tracking auf layer7 manchmal besser geeignet sein. So lässt sich einem Server beispielsweise mitteilen, wie viele gleichzeitige Verbindungen von einer bestimmten Adresse bestehen. Siehe auch das Sample-Abruf-Schlüsselwort sc_trackers.

<a id="entry-7-3-1-tcp-dst"></a>

**`tcp.dst`**

```haproxy
tcp.dst
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Gibt eine Ganzzahl zurück, die den Zielport im TCP-Header darstellt. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-flags"></a>

**`tcp.flags`**

```haproxy
tcp.flags
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Gibt eine Ganzzahl zurück, die die TCP-Flags dieses TCP-Headers darstellt. Alle 8 Flags von FIN bis CWR werden abgerufen. Jedes Flag kann mit dem Konverter "and()" geprüft werden. Die Werte der einzelnen Flags sind in RFC9293 beschrieben. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-options-mss"></a>

**`tcp.options.mss`**

```haproxy
tcp.options.mss
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "MSS". Wird sie gefunden, wird eine Ganzzahl mit dem darin angekündigten Wert zurückgegeben, andernfalls null. MSS steht für Maximum Segment Size und gibt die maximale Segmentgröße in Bytes an, die die Gegenstelle empfangen kann. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-options-sack"></a>

**`tcp.options.sack`**

```haproxy
tcp.options.sack
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "Sack-Permitted". Wird sie gefunden, wird 1 zurückgegeben, andernfalls null. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-options-tsopt"></a>

**`tcp.options.tsopt`**

```haproxy
tcp.options.tsopt
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "Timestamp". Wird sie gefunden, wird 1 zurückgegeben, andernfalls null. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-options-tsval"></a>

**`tcp.options.tsval`**

```haproxy
tcp.options.tsval
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "Timestamp". Wird sie gefunden, wird der von der Gegenstelle gesendete Zeitstempelwert zurückgegeben; andernfalls wird nichts zurückgegeben. Zeitstempel sind vorzeichenlose 32-Bit-Werte ohne festgelegte Einheit, die allein die Gegenstelle bestimmt. Zeitstempel verschiedener Verbindungen sollten voneinander unabhängig sein. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-options-wscale"></a>

**`tcp.options.wscale`**

```haproxy
tcp.options.wscale
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "Window Scale". Wird sie gefunden, wird der von der Gegenstelle gesendete Fensterskalierungswert zurückgegeben, andernfalls null. Werte über 14 sind nicht zu erwarten, obwohl keine technische Einschränkung ihr Senden verhindert. Um festzustellen, ob die Fensterskalierungsoption verwendet wurde, verwenden Sie "tcp.options.wsopt". Siehe auch "tcp-ss", "fc_saved_syn", "ip.data" und "tcp.options.wsopt".

<a id="entry-7-3-1-tcp-options-wsopt"></a>

**`tcp.options.wsopt`**

```haproxy
tcp.options.wsopt
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Sucht nach einer TCP-Option vom Typ "Window Scale". Wird sie gefunden, wird 1 zurückgegeben, andernfalls 0. Siehe auch "fc_saved_syn", "tcp-ss", "ip.data" und "tcp.options.wscale".

<a id="entry-7-3-1-tcp-options-list"></a>

**`tcp.options_list`**

```haproxy
tcp.options_list
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Erzeugt eine binäre Folge aller TCP-Optionstypen in derselben Reihenfolge, in der sie im TCP-Header erscheinen. Dies kann 0 bis 60 Bytes ergeben (im ungünstigsten Fall). Die Option End-of-options wird nicht ausgegeben. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-seq"></a>

**`tcp.seq`**

```haproxy
tcp.seq
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Gibt eine Ganzzahl zurück, die die von der Gegenstelle im TCP-Header verwendete Sequenznummer darstellt. Sequenznummern sind vorzeichenlose 32-Bit-Werte. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-src"></a>

**`tcp.src`**

```haproxy
tcp.src
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Gibt eine Ganzzahl zurück, die den Quellport im TCP-Header darstellt. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-tcp-win"></a>

**`tcp.win`**

```haproxy
tcp.win
```

Wird mit einem Eingabe-Sample verwendet, das einen binären TCP-Header darstellt, wie ihn "ip.data" zurückgibt. Gibt eine Ganzzahl zurück, die die von der Gegenstelle im TCP-Header angekündigte Fenstergröße darstellt. Der Wert wird unverändert als vorzeichenloser 16-Bit-Wert zurückgegeben, ohne den Fensterskalierungsfaktor anzuwenden. Siehe auch "fc_saved_syn", "tcp-ss" und "ip.data".

<a id="entry-7-3-1-ub64dec"></a>

**`ub64dec`**

```haproxy
ub64dec
```

Dieser Konverter ist die base64url-Variante des Konverters b64dec. Die base64url-Kodierung ist die für URLs und Dateinamen geeignete Variante ("URL and Filename Safe Alphabet") der base64-Kodierung. Diese Kodierung wird auch im JWT-Standard (JSON Web Token) verwendet.

Beispiel:

```shell
# Decoding a JWT payload:
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec
```

<a id="entry-7-3-1-ub64enc"></a>

**`ub64enc`**

```haproxy
ub64enc
```

Dieser Konverter ist die base64url-Variante des Konverters base64.

<a id="entry-7-3-1-ungrpc"></a>

**`ungrpc(<field_number>[,<field_type>])`**

```haproxy
ungrpc(<field_number>[,<field_type>])
```

Extrahiert aus einem binären Eingabe-Sample, das eine gRPC-Nachricht darstellt, das Protocol-Buffers-Nachrichtenfeld mit der Feldnummer `<field_number>` (Punktnotation). Ist `<field_type>` nicht angegeben, erfolgt die Extraktion als Rohdaten; andernfalls als ganzzahliges Sample. Zulässig sind folgende Typen: "int32", "int64", "uint32", "uint64", "sint32", "sint64", "bool", "enum" für den Wire-Typ "varint" 0; "fixed64", "sfixed64", "double" für den 64bit-Wire-Typ 1; "fixed32", "sfixed32", "float" für den Wire-Typ 5. "string" gilt als längenbegrenzter Typ und benötigt daher zur Extraktion kein Argument `<field_type>`. Weitere Informationen zu den Feldtypen von Protocol-Buffers-Nachrichten stehen hier:
<https://developers.google.com/protocol-buffers/docs/encoding>

Beispiel:

```text
// with such a protocol buffer .proto file content adapted from
// https://github.com/grpc/grpc/blob/master/examples/protos/route_guide.proto

message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}

message PPoint {
  Point point = 59;
}

message Rectangle {
  // One corner of the rectangle.
  PPoint lo = 48;
  // The other corner of the rectangle.
  PPoint hi = 49;
}
```

Angenommen, der Anfragekörper besteht aus dem Wert eines Objekts "Rectangle" (zwei Protocol-Buffers-Nachrichten vom Typ PPoint). Die vier Protocol-Buffers-Felder könnten dann mit diesen "ungrpc"-Direktiven extrahiert werden:

```text
req.body,ungrpc(48.59.1,int32) # "latitude" of "lo" first PPoint
req.body,ungrpc(48.59.2,int32) # "longitude" of "lo" first PPoint
req.body,ungrpc(49.59.1,int32) # "latitude" of "hi" second PPoint
req.body,ungrpc(49.59.2,int32) # "longitude" of "hi" second PPoint
```

Das dazwischenliegende Feld 48.59 könnte auch wie folgt als binäres Sample extrahiert werden:

```text
req.body,ungrpc(48.59)
```

Da eine gRPC-Nachricht stets aus einem gRPC-Header und darauf folgenden Protocol-Buffers-Nachrichten besteht, könnte im vorherigen Beispiel "latitude" des ersten PPoint "lo" mit diesen gleichwertigen Direktiven extrahiert werden:

```text
req.body,ungrpc(48.59),protobuf(1,int32)
req.body,ungrpc(48),protobuf(59.1,int32)
req.body,ungrpc(48),protobuf(59),protobuf(1,int32)
```

Der erste Konverter muss "ungrpc" sein, die übrigen müssen "protobuf" sein. Nur der letzte darf optional ein zweites Argument enthalten, um das vorherige binäre Sample zu interpretieren.

<a id="entry-7-3-1-unset-var"></a>

**`unset-var(<var>)`**

```haproxy
unset-var(<var>)
```

Setzt eine Variable zurück, wenn der Eingabeinhalt definiert ist. Der Name der Variablen beginnt mit einer Angabe ihres Gültigkeitsbereichs. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-upper"></a>

**`upper`**

```haproxy
upper
```

Wandelt ein Zeichenketten-Sample in Großbuchstaben um. Kann nur hinter einer Sample-Abruffunktion für Zeichenketten oder hinter einem Transformationsschlüsselwort stehen, das den Typ string zurückgibt. Das Ergebnis hat den Typ string.

<a id="entry-7-3-1-url-dec"></a>

**`url_dec([<in_form>])`**

```haproxy
url_dec([<in_form>])
```

Nimmt eine URL-kodierte Zeichenkette als Eingabe und gibt deren dekodierte Fassung aus. Eingabe und Ausgabe haben den Typ string. Ist das Argument `<in_form>` auf eine Ganzzahl ungleich null gesetzt, wird die Eingabezeichenkette als Teil eines Formulars oder einer Abfragezeichenkette betrachtet, und das Zeichen '+' wird in ein Leerzeichen (' ') umgewandelt. Andernfalls geschieht dies nur nach einem Fragezeichen ('?'), das eine Abfragezeichenkette anzeigt.

<a id="entry-7-3-1-url-enc"></a>

**`url_enc([<enc_type>])`**

```haproxy
url_enc([<enc_type>])
```

Nimmt eine Zeichenkette als Eingabe und gibt deren kodierte Fassung aus. Eingabe und Ausgabe haben den Typ string. Standardmäßig ist die Kodierung für den Typ `query` vorgesehen. Derzeit wird kein anderer Typ unterstützt; das optionale Argument ist für künftige Änderungen vorgesehen.

<a id="entry-7-3-1-us-ltime"></a>

**`us_ltime(<format>[,<offset>])`**

```haproxy
us_ltime(<format>[,<offset>])
```

Funktioniert wie "ltime", erwartet die Eingabe aber in Mikrosekunden. Unterstützt außerdem das von date(1) inspirierte Konvertierungskennzeichen %N. Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in Ortszeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Mikrosekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime().

Mit dem Konvertierungskennzeichen %N lässt sich der Nanosekundenanteil des Datums ausgeben. Da die Eingabe in Mikrosekunden erfolgt, ist die Genauigkeit begrenzt (000000000..999999000). %N kann zwischen % und N eine Breitenangabe enthalten. Dies ist nützlich zur Darstellung von Millisekunden (%3N) oder Mikrosekunden (%6N). Die voreingestellte und maximale Breite ist 9 (%N = %9N).

Siehe auch den Konverter "utime" für UTC sowie die Konverter "ltime" und "ms_ltime".

Beispiel:

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_ltime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-us-utime"></a>

**`us_utime(<format>[,<offset>])`**

```haproxy
us_utime(<format>[,<offset>])
```

Funktioniert wie "utime", erwartet die Eingabe aber in Mikrosekunden. Unterstützt außerdem das von date(1) inspirierte Konvertierungskennzeichen %N. Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in UTC-Zeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Mikrosekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime().

Mit dem Konvertierungskennzeichen %N lässt sich der Nanosekundenanteil des Datums ausgeben. Da die Eingabe in Mikrosekunden erfolgt, ist die Genauigkeit begrenzt (000000000..999999000). %N kann zwischen % und N eine Breitenangabe enthalten. Dies ist nützlich zur Darstellung von Millisekunden (%3N) oder Mikrosekunden (%6N). Die voreingestellte und maximale Breite ist 9 (%N = %9N).

Siehe auch den Konverter "ltime" für Ortszeit sowie die Konverter "utime" und "ms_utime".

Beispiel:

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_utime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-utime"></a>

**`utime(<format>[,<offset>])`**

```haproxy
utime(<format>[,<offset>])
```

Wandelt eine Ganzzahl, die ein Datum seit der Epoche darstellen soll, in eine Zeichenkette um, die dieses Datum in UTC-Zeit wiedergibt. Das Format wird durch die Zeichenkette `<format>` mit strftime(3) festgelegt. Damit lassen sich beliebige Datumsformate in Protokollen verwenden. Ein optionaler `<offset>` in Sekunden kann auf das Eingabedatum angewendet werden (positiv oder negativ). Die von Ihrem Betriebssystem unterstützten Formate stehen in der Handbuchseite zu strftime(). Siehe auch den Konverter "ltime" sowie "ms_utime" und "us_utime".

Beispiel:

```shell
# Emit two colons, one with the UTC time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,utime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-when"></a>

**`when(<condition>[,<args>...])`**

```haproxy
when(<condition>[,<args>...])
```

Wertet die Bedingung aus und gibt bei einem wahren Ergebnis das Eingabe-Sample unverändert aus; andernfalls wird nichts zurückgegeben. Dies ist speziell für selten benötigte Daten gedacht, die nur unter bestimmten Bedingungen ausgegeben werden sollen, beispielsweise Debug-Informationen beim Auftreten eines Fehlers.

Die Bedingung besteht aus einem Schlüsselwort aus der folgenden Liste. Optional kann ihr ein Ausrufezeichen ('!') zur Negation vorangestellt werden, und es können für diese Bedingung spezifische Argumente folgen:

    - "error" gibt true zurück, wenn während der Verarbeitung der Anfrage oder des Streams ein Fehler aufgetreten ist. Es gelten dieselben Regeln wie für "dontlog-normal" (beispielsweise zählt ein erfolgreiches Redispatch als Fehler).

    - "forwarded" gibt true zurück, wenn die Anfrage an einen Backend-Server weitergeleitet wurde.

    - "normal" gibt true zurück, wenn kein Fehler aufgetreten ist (gleichbedeutend mit "!error").

    - "processed" gibt true zurück, wenn die Anfrage entweder an einen Backend-Server weitergeleitet oder von einem Applet verarbeitet wurde.

    - "stopping" gibt true zurück, wenn der Prozess zum Zeitpunkt der Regelauswertung gerade beendet wird.

    - "toapplet" gibt true zurück, wenn die Anfrage von einem Applet verarbeitet wurde.

    - "acl" gibt true zurück, wenn die im nächsten Argument angegebene ACL zu true ausgewertet wird. Die ACL wird direkt vom Konverter ausgewertet; ihre Bezugsgrößen müssen daher in diesem Kontext gültig sein. Ein Anwendungsfall ist die Prüfung, ob die gesamte Übertragungszeit zu lang ist, bevor entschieden wird, ob Details ungewöhnlich langer Übertragungen protokolliert werden sollen.

Der Inhalt wird in jedem Fall ausgewertet; dieses Vorgehen verhindert daher nicht die Erzeugung dieser Informationen. Es soll lediglich deren Ausgabe vermeiden.

Ein Beispiel wäre, Debug-Informationen zum Backend-Stream nur dann zu protokollieren, wenn während der Verarbeitung ein Fehler aufgetreten ist, oder beim Beenden zusätzliche Informationen zu protokollieren.

Beispiel:

```shell
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on error:
log-format "$HAPROXY_HTTP_LOG_FMT dbg={%[bs.debug_str,when(!normal)]}"

Hier enthält das Feld "dbg" im Protokoll nur einen Bindestrich ('-'),
um bei nicht erfüllter Regel fehlenden Inhalt anzuzeigen. Ist die Regel erfüllt,
wird ein vollständiger Debug-Block ausgegeben.
```

Beispiel

```haproxy
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on slow transfers
acl slow_xfer res.timer.data ge 10000   # more than 10s is slow
log-format "$HAPROXY_HTTP_LOG_FMT                                         \
            fsdbg={%[fs.debug_str,when(acl,slow_xfer)]}                   \
            bsdbg={%[bs.debug_str,when(acl,slow_xfer)]}"
```


Beispiel

```haproxy
# only emit the backend src/port when a real connection was issued:
log-format "$HAPROXY_HTTP_LOG_FMT \
           src=[%[bc_src,when(forwarded)]:%[bc_src_port,when(forwarded)]]"
```


Da die Auswertung des Ausdrucks beendet wird, wenn die Bedingung nicht wahr ist, lässt sich damit auch verhindern, dass ein nachfolgender Konverter aufgerufen wird. Beispielsweise könnte der Konverter debug() nur bei einem Fehler aufgerufen werden, um ein Element nur dann zu protokollieren, wenn dies unbedingt nötig ist.

Beispiel:

```shell
# emit the whole response headers list to stderr only on error and only
# when the output is a connection. We abuse a dummy variable here.
http-after-response set-var(res.test) \
              res.hdrs,when(error),when(forwarded),debug(hdrs,stderr)
```

Siehe auch: Konverter debug

<a id="entry-7-3-1-word"></a>

**`word(<index>,<delimiters>[,<count>])`**

```haproxy
word(<index>,<delimiters>[,<count>])
```

Extrahiert unter Berücksichtigung der angegebenen Trennzeichen das n-te Wort aus einer Eingabezeichenkette, vom Anfang (positiver Index) oder vom Ende (negativer Index) gezählt. Indizes beginnen bei 1 oder -1; die Trennzeichen werden als Zeichenliste in einer Zeichenkette angegeben. Leere Wörter werden übersprungen. Trennzeichen am Anfang oder Ende der Eingabezeichenkette werden daher ignoriert, und aufeinanderfolgende Trennzeichen innerhalb der Eingabe gelten als ein einziges Trennzeichen. Optional können Sie mit `<count>` die Anzahl zu extrahierender Wörter angeben (Standard: 1). Der Wert 0 bedeutet, dass alle verbleibenden Wörter extrahiert werden.

Beispiel:

```text
str(f1_f2_f3__f5),word(4,_)    # f5
str(f1_f2_f3__f5),word(5,_)    # <not found>
str(f1_f2_f3__f5),word(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),word(3,_,2)  # f3__f5
str(f1_f2_f3__f5),word(-2,_,3) # f1_f2_f3
str(f1_f2_f3__f5),word(-3,_,0) # f1_f2
str(/f1/f2/f3/f4),word(1,/)    # f1
str(/f1////f2/f3/f4),word(1,/) # f2
```

<a id="entry-7-3-1-wt6"></a>

**`wt6([<avalanche>])`**

```haproxy
wt6([<avalanche>])
```

Bildet mit der WT6-Hashfunktion aus einem binären Eingabe-Sample einen vorzeichenlosen 32-Bit-Wert. Ist das optionale Argument `<avalanche>` gleich 1, kann zusätzlich eine vollständige Avalanche-Hashfunktion auf die Ausgabe angewendet werden. Dieser Konverter verwendet dieselben Funktionen wie die verschiedenen Hash-basierten Algorithmen zur Lastverteilung und liefert daher exakt dieselben Ergebnisse. Er ist hauptsächlich zur Fehlersuche gedacht, kann aber als Eintrag in einer Stick Table zum Erfassen grober Statistiken verwendet werden. Er darf nicht für Sicherheitszwecke verwendet werden, da ein 32-Bit-Hash leicht zu brechen ist. Siehe auch "crc32", "djb2", "sdbm", "crc32c" und die Direktive "hash-type".

<a id="entry-7-3-1-x509-v-err-str"></a>

**`x509_v_err_str`**

```haproxy
x509_v_err_str
```

Wandelt einen numerischen Wert in den entsprechenden Namen einer X509_V_ERR-Konstante um. Dies ist in ACLs nützlich, damit eine Konfiguration mit mehreren OpenSSL-Versionen funktioniert, da sich einige Codes beim Wechsel der Version ändern können.

Wird der entsprechende Konstantenname nicht gefunden, wird der numerische Wert als Zeichenkette ausgegeben.

Die Liste der von OpenSSL bereitgestellten Konstanten steht unter
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES>. Achten Sie darauf, die Seite für die richtige OpenSSL-Version zu lesen.

Beispiel:

```text
bind :443 ssl crt common.pem ca-file ca-auth.crt verify optional crt-ignore-err X509_V_ERR_CERT_REVOKED,X509_V_ERR_CERT_HAS_EXPIRED

acl cert_expired ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_HAS_EXPIRED
acl cert_revoked ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_REVOKED
acl cert_ok      ssl_c_verify,x509_v_err_str -m str X509_V_OK

http-response add-header X-SSL Ok if cert_ok
http-response add-header X-SSL Expired if cert_expired
http-response add-header X-SSL Revoked if cert_revoked

http-response add-header X-SSL-verify %[ssl_c_verify,x509_v_err_str]
```

<a id="entry-7-3-1-xor"></a>

**`xor(<value>)`**

```haproxy
xor(<value>)
```

Führt ein bitweises "XOR" (exklusives OR) zwischen `<value>` und dem vorzeichenbehafteten ganzzahligen Eingabewert aus und gibt das Ergebnis als vorzeichenbehaftete Ganzzahl zurück. `<value>` kann ein numerischer Wert oder ein Variablenname sein. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-1-xxh3"></a>

**`xxh3([<seed>])`**

```haproxy
xxh3([<seed>])
```

Bildet aus einem binären Eingabe-Sample mit der XXH3-64-Bit-Variante der XXhash-Hashfunktion einen vorzeichenbehafteten 64-Bit-Wert. Dieser Hash unterstützt einen Startwert, der standardmäßig null ist; über das Argument `<seed>` kann ein anderer Wert übergeben werden. Dieser Hash gilt als sehr gut und sehr schnell. Daher kann er URLs und/oder URL-Parameter für die Verwendung als Schlüssel in Stick Tables hashen, um Statistiken mit niedriger Kollisionsrate zu erfassen. Dabei ist jedoch Vorsicht geboten, da der Algorithmus nicht als kryptografisch sicher gilt.

<a id="entry-7-3-1-xxh32"></a>

**`xxh32([<seed>])`**

```haproxy
xxh32([<seed>])
```

Bildet aus einem binären Eingabe-Sample mit der 32-Bit-Variante der XXHash-Hashfunktion einen vorzeichenlosen 32-Bit-Wert. Dieser Hash unterstützt einen Startwert, der standardmäßig null ist; über das Argument `<seed>` kann ein anderer Wert übergeben werden. Dieser Hash gilt als sehr gut und sehr schnell. Daher kann er URLs und/oder URL-Parameter für die Verwendung als Schlüssel in Stick Tables hashen, um Statistiken mit niedriger Kollisionsrate zu erfassen. Dabei ist jedoch Vorsicht geboten, da der Algorithmus nicht als kryptografisch sicher gilt.

<a id="entry-7-3-1-xxh64"></a>

**`xxh64([<seed>])`**

```haproxy
xxh64([<seed>])
```

Bildet aus einem binären Eingabe-Sample mit der 64-Bit-Variante der XXHash-Hashfunktion einen vorzeichenbehafteten 64-Bit-Wert. Dieser Hash unterstützt einen Startwert, der standardmäßig null ist; über das Argument `<seed>` kann ein anderer Wert übergeben werden. Dieser Hash gilt als sehr gut und sehr schnell. Daher kann er URLs und/oder URL-Parameter für die Verwendung als Schlüssel in Stick Tables hashen, um Statistiken mit niedriger Kollisionsrate zu erfassen. Dabei ist jedoch Vorsicht geboten, da der Algorithmus nicht als kryptografisch sicher gilt.

### 7.3.2. Sample-Abruf aus internen Zuständen {#section-7-3-2}

Eine erste Gruppe von Sample-Abrufmethoden bezieht sich auf interne Informationen, die keinerlei Bezug zu Client-Informationen haben. Diese Methoden werden gelegentlich mit Direktiven "monitor fail" verwendet, um externen Überwachungsinstanzen einen internen Zustand zu melden. Die in diesem Abschnitt beschriebenen Sample-Abrufmethoden können überall verwendet werden.

Übersicht über die Sample-Abrufmethoden in diesem Abschnitt und ihre jeweiligen Typen:

```text
  Schlüsselwort                                    Ausgabetyp
-------------------------------------------------+-------------
acl([!]<name>[,...])                               boolean
act_conn                                           integer
always_false                                       boolean
always_true                                        boolean
avg_queue([<backend>])                             integer
be_conn([<backend>])                               integer
be_conn_free([<backend>])                          integer
be_sess_rate([<backend>])                          integer
bin(<hex>)                                         bin
bool(<bool>)                                       bool
connslots([<backend>])                             integer
cpu_calls                                          integer
cpu_ns_avg                                         integer
cpu_ns_tot                                         integer
date([<offset>[,<unit>]])                          integer
date_us                                            integer
env(<name>)                                        string
fe_conn([<frontend>])                              integer
fe_req_rate([<frontend>])                          integer
fe_sess_rate([<frontend>])                         integer
hostname                                           string
int(<integer>)                                     signed
ipv4(<ipv4>)                                       ipv4
ipv6(<ipv6>)                                       ipv6
last_entity                                        string
last_rule_file                                     string
last_rule_line                                     integer
lat_ns_avg                                         integer
lat_ns_tot                                         integer
meth(<method>)                                     method
nbsrv([<backend>])                                 integer
pid                                                integer
prio_class                                         integer
prio_offset                                        integer
proc                                               integer
queue([<backend>])                                 integer
quic_enabled                                       boolean
rand([<range>])                                    integer
srv_conn([<backend>/]<server>)                     integer
srv_conn_free([<backend>/]<server>)                integer
srv_is_up([<backend>/]<server>)                    boolean
srv_iweight([<backend>/]<server>)                  integer
srv_queue([<backend>/]<server>)                    integer
srv_sess_rate([<backend>/]<server>)                integer
srv_uweight([<backend>/]<server>)                  integer
srv_weight([<backend>/]<server>)                   integer
stopping                                           boolean
str(<string>)                                      string
table_avl([<table>])                               integer
table_cnt([<table>])                               integer
term_events                                        string
thread                                             integer
txn.id32                                           integer
txn.sess_term_state                                string
uptime                                             integer
uuid([<version>])                                  string
var(<var-name>[,<default>])                        undefined
wait_end                                           boolean
waiting_entity                                     string
-------------------------------------------------+-------------
```

Ausführliche Liste:

<a id="entry-7-3-2-acl-boolean"></a>

**`acl([!]<name>[,...]): boolean`**

```haproxy
acl([!]<name>[,...]): boolean
```

Gibt true zurück, wenn die Auswertung aller benannten ACLs true ergibt, andernfalls false. Es können bis zu 12 ACLs angegeben werden, jeweils durch Kommas getrennt. Jeder benannten ACL kann ein "!" vorangestellt werden, um das Ergebnis zu negieren. Führt eine Auswertung zu einem Fehler, gibt auch das Sample einen Fehler zurück. HAProxy führt keine Validierungsprüfungen der referenzierten ACLs durch. Beispielsweise wird nicht geprüft, ob eine ACL, die ein HTTP-Anfrage-Sample verwendet, im Antwortkontext eingesetzt wird. Dieses Verhalten kann sich künftig ändern.

act_conn: integer Gibt die Gesamtzahl der aktiven gleichzeitigen Verbindungen des Prozesses zurück.

always_false: boolean Gibt stets den booleschen Wert "false" zurück. Kann beim Anpassen von Konfigurationen in ACLs vorübergehend als Ersatz für eine andere ACL verwendet werden.

always_true: boolean Gibt stets den booleschen Wert "true" zurück. Kann beim Anpassen von Konfigurationen in ACLs vorübergehend als Ersatz für eine andere ACL verwendet werden.

<a id="entry-7-3-2-avg-queue-integer"></a>

**`avg_queue([<backend>]): integer`**

```haproxy
avg_queue([<backend>]): integer
```

Gibt die Gesamtzahl der wartenden Verbindungen des angegebenen Backends geteilt durch die Anzahl aktiver Server zurück. Wird kein Backend angegeben, wird das aktuelle verwendet. Dies ist "queue" sehr ähnlich, berücksichtigt aber die Größe der Servergruppe, um die voraussichtliche Wartezeit bis zur Verarbeitung einer neuen Verbindung genauer zu messen. Die Hauptanwendung besteht darin, mit einer ACL neuen Nutzern eine Entschuldigungsseite zurückzugeben, wenn feststeht, dass sie nur eingeschränkten Dienst erhalten würden. Der Wert kann auch in einem Header an die Backend-Server weitergegeben werden, damit diese entscheiden können, in einem eingeschränkten Modus zu arbeiten oder einige Funktionen zu deaktivieren, um die Verarbeitung etwas zu beschleunigen. Ist kein aktiver Server mehr vorhanden, wird die doppelte Anzahl wartender Verbindungen als Messwert verwendet. Dies ist eine angemessene Schätzung, da ohnehin erwartet wird, dass bald ein Server zurückkehrt; neuer Verkehr soll dennoch bevorzugt an ein anderes Backend geleitet werden, wenn dieses in besserem Zustand ist. Siehe auch die Sample-Abrufe "queue", "be_conn" und "be_sess_rate".

<a id="entry-7-3-2-be-conn-integer"></a>

**`be_conn([<backend>]): integer`**

```haproxy
be_conn([<backend>]): integer
```

Bezieht sich auf die Anzahl der derzeit hergestellten Verbindungen des Backends, gegebenenfalls einschließlich der gerade ausgewerteten Verbindung. Wird kein Backend-Name angegeben, wird das aktuelle Backend verwendet. Es kann aber auch ein anderes Backend geprüft werden. Damit lässt sich eine bestimmte Servergruppe verwenden, wenn die normalerweise vorgesehene voll ist. Siehe auch die Kriterien "fe_conn", "queue", "be_conn_free" und "be_sess_rate".

<a id="entry-7-3-2-be-conn-free-integer"></a>

**`be_conn_free([<backend>]): integer`**

```haproxy
be_conn_free([<backend>]): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl verfügbarer Verbindungen über die verfügbaren Server im Backend entspricht. Warteschlangenplätze sind nicht enthalten. Backup-Server werden ebenfalls nicht berücksichtigt, sofern nicht alle anderen Server ausgefallen sind. Wird kein Backend-Name angegeben, wird das aktuelle Backend verwendet. Es kann aber auch ein anderes Backend geprüft werden. Damit lässt sich eine bestimmte Servergruppe verwenden, wenn die normalerweise vorgesehene voll ist. Siehe auch die Kriterien "be_conn", "connslots" und "srv_conn_free".

Weitere Einschränkungen und Hinweise: Ist maxconn oder maxqueue eines Servers gleich 0 (also unbegrenzt), ist dieser Abruf nicht sinnvoll; in diesem Fall wird -1 zurückgegeben.

<a id="entry-7-3-2-be-sess-rate-integer"></a>

**`be_sess_rate([<backend>]): integer`**

```haproxy
be_sess_rate([<backend>]): integer
```

Gibt eine Ganzzahl zurück, die der Rate neu angelegter Sitzungen im Backend entspricht, gemessen als Anzahl neuer Sitzungen pro Sekunde. Dies wird mit ACLs verwendet, um auf ein alternatives Backend umzuschalten, wenn ein ressourcenintensives oder empfindliches Backend eine zu hohe Sitzungsrate erreicht, oder um den Missbrauch eines Diensts zu begrenzen (beispielsweise das massenhafte Auslesen eines Online-Wörterbuchs zu verhindern). Es kann auch nützlich sein, diesen Wert mit einer log-format-Direktive in Protokolle aufzunehmen.

Beispiel:

```shell
# Redirect to an error page if the dictionary is requested too often
backend dynamic
    mode http
    acl being_scanned be_sess_rate gt 100
    redirect location /denied.html if being_scanned
```

<a id="entry-7-3-2-bin-bin"></a>

**`bin(<hex>): bin`**

```haproxy
bin(<hex>): bin
```

Gibt eine binäre Zeichenfolge zurück. Die Eingabe ist die hexadezimale Darstellung der Zeichenkette.

<a id="entry-7-3-2-bool-bool"></a>

**`bool(<bool>): bool`**

```haproxy
bool(<bool>): bool
```

Gibt einen booleschen Wert zurück. `<bool>` kann 'true', 'false', '1' oder '0' sein. 'false' und '0' sind gleichbedeutend. 'true' und '1' sind gleichbedeutend.

<a id="entry-7-3-2-connslots-integer"></a>

**`connslots([<backend>]): integer`**

```haproxy
connslots([<backend>]): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl noch verfügbarer Verbindungsplätze im Backend entspricht. Dazu werden die maximale Verbindungszahl aller Server und die maximale Warteschlangengröße aufsummiert. Dies wird vermutlich nur mit ACLs verwendet.

Die Grundidee besteht darin, die Anzahl noch verfügbarer Verbindungsplätze (Verbindungen und Warteschlange) zu messen, sodass darüber hinausgehender Verkehr an ein anderes Backend umgeleitet werden kann (vorgesehene Verwendung; siehe das Schlüsselwort "use_backend").

'connslots' = Anzahl verfügbarer Server-Verbindungsplätze + Anzahl verfügbarer Server-Warteschlangenplätze.

Zwar kann "fe_conn" verwendet werden, doch ist "connslots" besonders nützlich, wenn der Verkehr an eine einzige IP-Adresse geht und auf mehrere Backends aufgeteilt wird (etwa mit ACLs zur namensbasierten Lastverteilung) und Sie die verschiedenen Backends und ihre verfügbaren "connslots" unterscheiden möchten. Während "nbsrv" nur Server erfasst, die tatsächlich *ausgefallen* sind, arbeitet dieser Abruf feiner und betrachtet auch die Anzahl verfügbarer Verbindungsplätze. Siehe auch "queue" und "avg_queue".

Weitere Einschränkungen und Hinweise: Der Code berücksichtigt derzeit keine dynamischen Verbindungen. Ist außerdem maxconn oder maxqueue eines Servers gleich 0, ist dieser Abruf nicht sinnvoll; in diesem Fall wird -1 zurückgegeben.

cpu_calls: integer Gibt die Anzahl der Aufrufe der Aufgabe zurück, die den Stream oder die aktuelle Anfrage verarbeitet, seit diese Aufgabe angelegt wurde. Bei HTTP-Keep-Alive wird dieser Zähler für jede neue Anfrage auf derselben Verbindung zurückgesetzt. Der Wert sollte normalerweise niedrig und stabil sein (bei einer typischen einfachen Anfrage etwa 2 Aufrufe), kann aber bei zusätzlicher Verarbeitung wie Komprimierung, Caching oder Analyse hoch werden. Er dient ausschließlich der Leistungsüberwachung.

cpu_ns_avg: integer Gibt die durchschnittliche Anzahl von Nanosekunden zurück, die in jedem Aufruf der Aufgabe verbracht werden, welche den Stream oder die aktuelle Anfrage verarbeitet. Bei HTTP-Keep-Alive wird dieser Wert für jede neue Anfrage auf derselben Verbindung zurückgesetzt. Er zeigt die gesamten Verarbeitungskosten der Anfrage oder Verbindung pro Aufruf. Es gibt keinen grundsätzlich guten oder schlechten Wert; die in einem Aufruf verbrachte Zeit verursacht jedoch automatisch Verzögerungen anderer Verarbeitungsvorgänge (siehe lat_ns_avg weiter unten) und kann die beobachtete Antwortzeit anderer Verbindungen beeinflussen. Bestimmte Operationen wie Komprimierung, komplexer Regex-Abgleich oder aufwendige Lua-Operationen können diesen Wert direkt beeinflussen. Seine Aufnahme in Protokolle erleichtert es, problematische Verarbeitungsschritte zu finden, die zur Wiederherstellung einer angemessenen Leistung korrigiert werden müssen. Hinweis: Dieser Wert entspricht genau cpu_ns_tot geteilt durch cpu_calls.

cpu_ns_tot: integer Gibt die Gesamtzahl der Nanosekunden zurück, die in den Aufrufen der Aufgabe verbracht werden, welche den Stream oder die aktuelle Anfrage verarbeitet. Bei HTTP-Keep-Alive wird dieser Wert für jede neue Anfrage auf derselben Verbindung zurückgesetzt. Er zeigt die gesamten Verarbeitungskosten der Anfrage oder Verbindung pro Aufruf. Es gibt keinen grundsätzlich guten oder schlechten Wert; die in einem Aufruf verbrachte Zeit verursacht jedoch automatisch Verzögerungen anderer Verarbeitungsvorgänge (siehe lat_ns_avg weiter unten), erzeugt CPU-Last auf dem Rechner und kann die beobachtete Antwortzeit anderer Verbindungen beeinflussen. Bestimmte Operationen wie Komprimierung, komplexer Regex-Abgleich oder aufwendige Lua-Operationen können diesen Wert direkt beeinflussen. Seine Aufnahme in Protokolle erleichtert es, problematische Verarbeitungsschritte zu finden, die zur Wiederherstellung einer angemessenen Leistung korrigiert werden müssen. Der Wert kann durch eine hohe Anzahl cpu_calls künstlich hoch sein, beispielsweise bei der Verarbeitung vieler HTTP-Chunks. Daher wird häufig bevorzugt, stattdessen cpu_ns_avg zu protokollieren.

cpu_usage_grp: integer Gibt die während des letzten Abfragezyklus gemessene CPU-Auslastung zwischen 0 und 100 zurück, gemittelt über alle Threads der aktuellen Thread-Gruppe. Dies kann zur Fehlersuche und zur Protokollierung verwendet werden. Die Messung schwankt sehr stark, bleibt bei dauerhafter Last aber genau, da jeder Thread sie über einige Dutzend bis Hunderte von Anfragen ermittelt.

cpu_usage_proc: integer Gibt die während des letzten Abfragezyklus gemessene CPU-Auslastung zwischen 0 und 100 zurück, gemittelt über alle laufenden Threads. Dies kann zur Fehlersuche und zur Protokollierung verwendet werden. Die Messung schwankt sehr stark, bleibt bei dauerhafter Last aber genau, da jeder Thread sie über einige Dutzend bis Hunderte von Anfragen ermittelt. Der Wert entspricht 100 minus dem auf der Statistikseite und in "show info" gemeldeten Leerlaufanteil.

cpu_usage_thr: integer Gibt die während des letzten Abfragezyklus gemessene CPU-Auslastung zwischen 0 und 100 für den aufrufenden Thread zurück. Dies kann zur Fehlersuche und zur Protokollierung verwendet werden. Die Messung schwankt sehr stark, bleibt bei dauerhafter Last aber genau, da sie über einige Dutzend bis Hunderte von Anfragen ermittelt wird. Derselbe Wert wird verwendet, um bei zu vielen Störungen das Beenden von Verbindungen zu aktivieren oder die Komprimierung zu deaktivieren. Siehe auch "tune.glitches.kill.cpu-usage" und "maxcompcpuusage".

<a id="entry-7-3-2-date-integer"></a>

**`date([<offset>[,<unit>]]): integer`**

```haproxy
date([<offset>[,<unit>]]): integer
```

Gibt das aktuelle Datum als Epochenzeit zurück (Anzahl der Sekunden seit dem 01/01/1970).

Ist ein Offset angegeben, wird er vor der Rückgabe zum aktuellen Datum addiert. Dies ist besonders nützlich zur Berechnung relativer Daten, da sowohl positive als auch negative Offsets erlaubt sind. Nützlich ist die Kombination mit dem Konverter http_date.

`<unit>` ist optional und kann auf "s" für Sekunden (Standardverhalten), "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Einheit angegeben, ist der Rückgabewert eine Ganzzahl, die Sekunden, Millisekunden oder Mikrosekunden seit der Epoche zuzüglich Offset angibt. Dies ist nützlich, wenn eine Zeitauflösung unter einer Sekunde benötigt wird.

Beispiel:

```shell
# set an expires header to now+1 hour in every response
http-response set-header Expires %[date(3600),http_date]

# set an expires header to now+1 hour in every response, with
# millisecond granularity
http-response set-header Expires %[date(3600000,ms),http_date(0,ms)]
```

date_us: integer Gibt den Mikrosekundenanteil des Datums zurück; den Sekundenanteil liefert das Sample date. Dieses Sample ist mit dem Sample date konsistent, da es aus derselben timeval-Struktur stammt.

<a id="entry-7-3-2-env-string"></a>

**`env(<name>): string`**

```haproxy
env(<name>): string
```

Gibt eine Zeichenkette mit dem Wert der Umgebungsvariablen `<name>` zurück. Zur Erinnerung: Umgebungsvariablen gelten pro Prozess und werden beim Prozessstart erfasst. Damit lassen sich Informationen an den nächsten Server weitergeben oder mit ACLs bestimmte Aktionen auslösen, wenn der Prozess auf eine bestimmte Weise gestartet wurde.

Beispiele:

```shell
# Pass the Via header to next hop with the local hostname in it
http-request add-header Via 1.1\ %[env(HOSTNAME)]

# reject cookie-less requests when the STOP environment variable is set
http-request deny if !{ req.cook(SESSIONID) -m found } { env(STOP) -m found }
```

<a id="entry-7-3-2-fe-conn-integer"></a>

**`fe_conn([<frontend>]): integer`**

```haproxy
fe_conn([<frontend>]): integer
```

Gibt die Anzahl der derzeit hergestellten Verbindungen des Frontends zurück, gegebenenfalls einschließlich der gerade ausgewerteten Verbindung. Wird kein Frontend-Name angegeben, wird das aktuelle Frontend verwendet. Es kann aber auch ein anderes Frontend geprüft werden. Damit lässt sich vor einer vollständigen Sperre eine Entschuldigungsseite zurückgeben oder ein bestimmtes Backend zum Ableiten neuer Anfragen verwenden, wenn die Servergruppe als voll gilt. Dies wird überwiegend mit ACLs verwendet, kann aber auch Statistiken in HTTP-Headern an Server weitergeben. Siehe auch die Abrufe "dst_conn", "be_conn" und "fe_sess_rate".

<a id="entry-7-3-2-fe-req-rate-integer"></a>

**`fe_req_rate([<frontend>]): integer`**

```haproxy
fe_req_rate([<frontend>]): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl der pro Sekunde an ein Frontend gesendeten HTTP-Anfragen entspricht. Dieser Wert kann von "fe_sess_rate" abweichen, wenn Keep-Alive auf der Client-Seite aktiviert ist.

<a id="entry-7-3-2-fe-sess-rate-integer"></a>

**`fe_sess_rate([<frontend>]): integer`**

```haproxy
fe_sess_rate([<frontend>]): integer
```

Gibt eine Ganzzahl zurück, die der Rate neu angelegter Sitzungen im Frontend entspricht, gemessen als Anzahl neuer Sitzungen pro Sekunde. Dies wird mit ACLs verwendet, um die eingehende Sitzungsrate auf einen akzeptablen Bereich zu begrenzen und Missbrauch eines Diensts möglichst früh zu verhindern. Beispielsweise können Clients in Verbindung mit anderen ACLs auf Schicht 4 dazu gezwungen werden, etwas zu warten, bis die Rate wieder unter den Grenzwert sinkt. Es kann auch nützlich sein, diesen Wert mit einer log-format-Direktive in Protokolle aufzunehmen. Siehe auch die Direktive "rate-limit sessions" zur Verwendung in Frontends.

Beispiel:

```shell
# This frontend limits incoming mails to 10/s with a max of 100
# concurrent connections. We accept any connection below 10/s, and
# force excess clients to wait for 100 ms. Since clients are limited to
# 100 max, there cannot be more than 10 incoming mails per second.
frontend mail
    bind :25
    mode tcp
    maxconn 100
    acl too_fast fe_sess_rate ge 10
    tcp-request inspect-delay 100ms
    tcp-request content accept if ! too_fast
    tcp-request content accept if WAIT_END
```

hostname: string Gibt den Hostnamen des Systems zurück.

<a id="entry-7-3-2-int-signed-integer"></a>

**`int(<integer>): signed integer`**

```haproxy
int(<integer>): signed integer
```

Gibt eine vorzeichenbehaftete Ganzzahl zurück.

<a id="entry-7-3-2-ipv4-ipv4"></a>

**`ipv4(<ipv4>): ipv4`**

```haproxy
ipv4(<ipv4>): ipv4
```

Gibt eine IPv4-Adresse zurück.

<a id="entry-7-3-2-ipv6-ipv6"></a>

**`ipv6(<ipv6>): ipv6`**

```haproxy
ipv6(<ipv6>): ipv6
```

Gibt eine IPv6-Adresse zurück.

last_entity: string Gibt die Identität der letzten Entität zurück, die während der Stream-Analyse ausgewertet wurde. Dies kann die letzte zutreffende abschließende Regel oder der Filter sein, der die Verarbeitung unterbrochen hat.

Eine abschließende Regel beendet die Auswertung des Regelsatzes, beispielsweise "accept", "deny" oder "redirect". Dies funktioniert für TCP-Anfrage- und Antwortregeln in den Regelsätzen "content" sowie für HTTP-Regeln in "http-request", "http-response" und "http-after-response". Die älteren Regelsätze "redirect" werden nicht unterstützt, da diese Informationen dort nicht gespeichert werden. Auch "tcp-request connection" und "tcp-request session" werden nicht unterstützt, weil die Informationen auf Stream-Ebene gespeichert werden und während dieser Regeln noch keine Streams existieren. In diesem Fall entspricht der Rückgabewert "last_rule_file:last_rule_line". Siehe auch "last_rule_file" und "last_rule_line".

Bei einem Filter wird der von den Entwicklern festgelegte Bezeichner zurückgegeben. Ist dieser Bezeichner nicht definiert, wird ein Hexadezimalwert zurückgegeben, der einem eindeutigen internen Bezeichner entspricht.

Der Hauptzweck dieser Funktion besteht darin, die letzte Entität, die eine Verarbeitung unterbrochen hat, zur Unterstützung der Fehlersuche in Protokollen zu melden. Die zu Entitäten zurückgegebenen Informationen können sich im Laufe der Zeit ändern und dürfen ausschließlich zur Fehlersuche verwendet werden.

Beispiel:

```shell
# Log the last entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[last_entity,when(error)]
```

last_rule_file: string Gibt den Namen der Konfigurationsdatei zurück, die die letzte während der Stream-Analyse zutreffende abschließende Regel enthält. Eine abschließende Regel beendet die Auswertung des Regelsatzes, beispielsweise "accept", "deny" oder "redirect". Dies funktioniert für TCP-Anfrage- und Antwortregeln in den Regelsätzen "content" sowie für HTTP-Regeln in "http-request", "http-response" und "http-after-response". Die älteren Regelsätze "redirect" werden nicht unterstützt, da diese Informationen dort nicht gespeichert werden. Auch "tcp-request connection" und "tcp-request session" werden nicht unterstützt, weil die Informationen auf Stream-Ebene gespeichert werden und während dieser Regeln noch keine Streams existieren. Der Hauptzweck dieser Funktion besteht darin, die Position der Regel, die die endgültige Entscheidung getroffen hat, in Protokollen zu melden. Dies hilft beispielsweise zu klären, warum eine Anfrage abgelehnt wurde. Siehe auch "last_rule_line".

last_rule_line: integer Gibt die Zeilennummer in der Konfigurationsdatei zurück, an der die letzte während der Stream-Analyse zutreffende abschließende Regel steht. Eine abschließende Regel beendet die Auswertung des Regelsatzes, beispielsweise "accept", "deny" oder "redirect". Dies funktioniert für TCP-Anfrage- und Antwortregeln in den Regelsätzen "content" sowie für HTTP-Regeln in "http-request", "http-response" und "http-after-response". Die älteren Regelsätze "redirect" werden nicht unterstützt, da diese Informationen dort nicht gespeichert werden. Auch "tcp-request connection" und "tcp-request session" werden nicht unterstützt, weil die Informationen auf Stream-Ebene gespeichert werden und während dieser Regeln noch keine Streams existieren. Der Hauptzweck dieser Funktion besteht darin, die Position der Regel, die die endgültige Entscheidung getroffen hat, in Protokollen zu melden. Dies hilft beispielsweise zu klären, warum eine Anfrage abgelehnt wurde. Siehe auch "last_rule_file".

lat_ns_avg: integer Gibt die durchschnittliche Anzahl der Nanosekunden zwischen dem Aufwecken der den Stream bearbeitenden Aufgabe und ihrem tatsächlichen Aufruf zurück. Bei HTTP-Keep-Alive wird dieser Wert für jede neue Anfrage auf derselben Verbindung zurückgesetzt. Er zeigt die gesamte Verzögerung, die alle anderen parallel verarbeiteten Anfragen der aktuellen Anfrage auferlegen, und ist ein direkter Indikator für die durch ressourcenintensive Nachbarn wahrgenommene Leistung. Um den Wert niedrig zu halten, können Sie die Tiefe der Ausführungswarteschlange des Schedulers mit "tune.runqueue-depth" verringern, mit "tune.maxpollevents" die Anzahl gleichzeitig verarbeiteter Ereignisse reduzieren, den nice-Wert des Streams mit der Option "nice" in den "bind"-Zeilen oder im Frontend senken oder mit "tune.sched.low-latency" eine Planung mit geringer Latenz aktivieren. Sie können auch in den Protokollen nach anderen aufwendigen Anfragen mit hohen Werten von "cpu_ns_avg" suchen, deren Verarbeitung angepasst oder korrigiert werden muss. Mögliche Ursachen sind die Komprimierung großer Puffer, aufwendige reguläre Ausdrücke oder lange Listen regulärer Ausdrücke. Hinweis: Dieser Wert entspricht genau lat_ns_tot geteilt durch cpu_calls.

lat_ns_tot: integer Gibt die Gesamtzahl der Nanosekunden zwischen dem Aufwecken der den Stream bearbeitenden Aufgabe und ihrem tatsächlichen Aufruf zurück. Bei HTTP-Keep-Alive wird dieser Wert für jede neue Anfrage auf derselben Verbindung zurückgesetzt. Er zeigt die gesamte Verzögerung, die alle anderen parallel verarbeiteten Anfragen der aktuellen Anfrage auferlegen, und ist ein direkter Indikator für die durch ressourcenintensive Nachbarn wahrgenommene Leistung. Um den Wert niedrig zu halten, können Sie die Tiefe der Ausführungswarteschlange des Schedulers mit "tune.runqueue-depth" verringern, mit "tune.maxpollevents" die Anzahl gleichzeitig verarbeiteter Ereignisse reduzieren, den nice-Wert des Streams mit der Option "nice" in den "bind"-Zeilen oder im Frontend senken oder mit "tune.sched.low-latency" eine Planung mit geringer Latenz aktivieren. Sie können auch in den Protokollen nach anderen aufwendigen Anfragen mit hohen Werten von "cpu_ns_avg" suchen, deren Verarbeitung angepasst oder korrigiert werden muss. Mögliche Ursachen sind die Komprimierung großer Puffer, aufwendige reguläre Ausdrücke oder lange Listen regulärer Ausdrücke. Hinweis: Auch wenn intuitiv der Eindruck entstehen kann, dass die gesamte Latenz zur Übertragungszeit hinzukommt, ist dies fast nie der Fall. Während eine Aufgabe auf die CPU wartet, füllen sich die Netzwerkpuffer weiter, sodass beim nächsten Aufruf mehr auf einmal verarbeitet wird. Der Wert kann durch eine hohe Anzahl cpu_calls künstlich hoch sein, beispielsweise bei der Verarbeitung vieler HTTP-Chunks. Daher wird häufig bevorzugt, stattdessen lat_ns_avg zu protokollieren, da dies ein aussagekräftigerer Leistungsindikator ist.

<a id="entry-7-3-2-meth-method"></a>

**`meth(<method>): method`**

```haproxy
meth(<method>): method
```

Gibt eine Methode zurück.

<a id="entry-7-3-2-nbsrv-integer"></a>

**`nbsrv([<backend>]): integer`**

```haproxy
nbsrv([<backend>]): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl nutzbarer Server des aktuellen oder des benannten Backends entspricht. Dies wird überwiegend mit ACLs verwendet, kann aber auch in Protokollen nützlich sein. Üblicherweise wird damit auf ein alternatives Backend umgeschaltet, wenn die Anzahl der Server zu niedrig ist, um eine bestimmte Last zu bewältigen. In Verbindung mit "monitor fail" eignet es sich zum Melden eines Ausfalls.

pid: integer Gibt die PID des aktuellen Prozesses zurück. In den meisten Fällen ist dies die PID des Worker-Prozesses.

prio_class: integer Gibt die Prioritätsklasse des aktuellen Streams im Modus http oder der aktuellen Verbindung im Modus tcp zurück. Der Wert entspricht dem letzten Aufruf von "http-request set-priority-class" oder "tcp-request content set-priority-class".

prio_offset: integer Gibt den Prioritäts-Offset des aktuellen Streams im Modus http oder der aktuellen Verbindung im Modus tcp zurück. Der Wert entspricht dem letzten Aufruf von "http-request set-priority-offset" oder "tcp-request content set-priority-offset".

proc: integer Gibt immer den Wert 1 zurück; früher wurde die Nummer des aufrufenden Prozesses zurückgegeben.

<a id="entry-7-3-2-queue-integer"></a>

**`queue([<backend>]): integer`**

```haproxy
queue([<backend>]): integer
```

Gibt die Gesamtzahl wartender Verbindungen des angegebenen Backends zurück, einschließlich aller Verbindungen in Server-Warteschlangen. Wird kein Backend-Name angegeben, wird das aktuelle Backend verwendet; es kann aber auch ein anderes geprüft werden. Dies ist mit ACLs oder zur Weitergabe von Statistiken an Backend-Server nützlich. Damit lassen sich Aktionen auslösen, wenn die Warteschlangen einen bekannten Schwellenwert überschreiten, was in der Regel auf einen starken Verkehrszuwachs oder eine massive Verlangsamung der Server hindeutet. Eine mögliche Aktion wäre, neue Nutzer abzulehnen, bestehende aber weiterhin zu akzeptieren. Siehe auch die Abrufe "avg_queue", "be_conn" und "be_sess_rate".

quic_enabled: boolean Gibt true zurück, wenn die Unterstützung für das Transportprotokoll QUIC einkompiliert wurde und QUIC-Listener nicht durch die globale Option "tune.quic.listen" deaktiviert sind. Siehe auch die globale Option "tune.quic.listen".

<a id="entry-7-3-2-rand-integer"></a>

**`rand([<range>]): integer`**

```haproxy
rand([<range>]): integer
```

Gibt eine zufällige Ganzzahl aus einem Bereich mit `<range>` möglichen Werten zurück, beginnend bei null. Wird der Bereich nicht angegeben, ist der Standardwert 2^32, wodurch Zahlen zwischen 0 und 4294967295 entstehen. Dies kann beispielsweise zum Bereitstellen von Werten für Routing-Entscheidungen oder einfach zur Fehlersuche nützlich sein. Diese Zufallswerte dürfen nicht für Sicherheitszwecke verwendet werden.

<a id="entry-7-3-2-srv-conn-integer"></a>

**`srv_conn([<backend>/]<server>): integer`**

```haproxy
srv_conn([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl derzeit hergestellter Verbindungen des angegebenen Servers entspricht, gegebenenfalls einschließlich der gerade ausgewerteten Verbindung. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Damit lässt sich eine bestimmte Servergruppe verwenden, wenn ein Server voll ist, oder dem Server unsere Sicht auf die Anzahl aktiver Verbindungen mit ihm mitteilen. Siehe auch die Abrufmethoden "fe_conn", "be_conn", "queue" und "srv_conn_free".

<a id="entry-7-3-2-srv-conn-free-integer"></a>

**`srv_conn_free([<backend>/]<server>): integer`**

```haproxy
srv_conn_free([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl verfügbarer Verbindungen des angegebenen Servers entspricht, gegebenenfalls einschließlich der gerade ausgewerteten Verbindung. Warteschlangenplätze sind nicht enthalten. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Damit lässt sich eine bestimmte Servergruppe verwenden, wenn ein Server voll ist, oder dem Server unsere Sicht auf die Anzahl aktiver Verbindungen mit ihm mitteilen. Siehe auch die Abrufmethoden "be_conn_free" und "srv_conn".

Weitere Einschränkungen und Hinweise: Ist maxconn des Servers gleich 0, ist dieser Abruf nicht sinnvoll; in diesem Fall wird -1 zurückgegeben.

<a id="entry-7-3-2-srv-is-up-boolean"></a>

**`srv_is_up([<backend>/]<server>): boolean`**

```haproxy
srv_is_up([<backend>/]<server>): boolean
```

Gibt true zurück, wenn der angegebene Server UP ist, und false, wenn er DOWN oder im Wartungsmodus ist. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Dies wird hauptsächlich verwendet, um anhand eines externen, über einen Health Check gemeldeten Zustands zu handeln, etwa der Verfügbarkeit eines geografischen Standorts. Eine weitere, eher behelfsmäßige Verwendung besteht darin, Dummy-Server als boolesche Variablen einzusetzen, die über die CLI aktiviert oder deaktiviert werden können. So lassen sich Regeln, die von diesen ACLs abhängen, in Echtzeit anpassen.

<a id="entry-7-3-2-srv-iweight-integer"></a>

**`srv_iweight([<backend>/]<server>): integer`**

```haproxy
srv_iweight([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die dem anfänglichen Gewicht des Servers entspricht. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Siehe auch "srv_weight" und "srv_uweight".

<a id="entry-7-3-2-srv-queue-integer"></a>

**`srv_queue([<backend>/]<server>): integer`**

```haproxy
srv_queue([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl derzeit in der Warteschlange des angegebenen Servers wartender Verbindungen entspricht. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Mit der Direktive "use-server" kann dies gelegentlich dazu dienen, die Verwendung eines bekanntermaßen schnelleren Servers zu erzwingen, wenn dieser nur wenig ausgelastet ist. Siehe auch die Sample-Abrufmethoden "srv_conn", "avg_queue" und "queue".

<a id="entry-7-3-2-srv-sess-rate-integer"></a>

**`srv_sess_rate([<backend>/]<server>): integer`**

```haproxy
srv_sess_rate([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die der Rate neu angelegter Sitzungen des angegebenen Servers entspricht, gemessen als Anzahl neuer Sitzungen pro Sekunde. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Dies wird überwiegend mit ACLs verwendet, kann aber auch für Protokolle sinnvoll sein. Damit wird auf ein alternatives Backend umgeschaltet, wenn ein ressourcenintensives oder empfindliches Backend eine zu hohe Sitzungsrate erreicht, oder der Missbrauch eines Diensts begrenzt, beispielsweise um eine Überlastung der Server durch verzögerte Anfragen zu verhindern.

Beispiel:

```shell
# Redirect to a separate back
acl srv1_full srv_sess_rate(be1/srv1) gt 50
acl srv2_full srv_sess_rate(be1/srv2) gt 50
use_backend be2 if srv1_full or srv2_full
```

<a id="entry-7-3-2-srv-uweight-integer"></a>

**`srv_uweight([<backend>/]<server>): integer`**

```haproxy
srv_uweight([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die dem für den Benutzer sichtbaren Gewicht des Servers entspricht. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Siehe auch "srv_weight" und "srv_iweight".

<a id="entry-7-3-2-srv-weight-integer"></a>

**`srv_weight([<backend>/]<server>): integer`**

```haproxy
srv_weight([<backend>/]<server>): integer
```

Gibt eine Ganzzahl zurück, die dem aktuellen bzw. effektiven Gewicht des Servers entspricht. Wird `<backend>` weggelassen, wird der Server im aktuellen Backend gesucht. Siehe auch "srv_iweight" und "srv_uweight".

stopping: boolean Gibt TRUE zurück, wenn der Prozess, der die Funktion aufruft, gerade beendet wird. Dies kann für die Protokollierung nützlich sein, aber auch zum Lockern bestimmter Prüfungen oder zum Schließen bestimmter Verbindungen beim geordneten Herunterfahren.

<a id="entry-7-3-2-str-string"></a>

**`str(<string>): string`**

```haproxy
str(<string>): string
```

Gibt eine Zeichenkette zurück.

<a id="entry-7-3-2-table-avl-integer"></a>

**`table_avl([<table>]): integer`**

```haproxy
table_avl([<table>]): integer
```

Gibt die Gesamtzahl verfügbarer Einträge in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table zurück. Siehe auch "table_cnt".

<a id="entry-7-3-2-table-cnt-integer"></a>

**`table_cnt([<table>]): integer`**

```haproxy
table_cnt([<table>]): integer
```

Gibt die Gesamtzahl der derzeit verwendeten Einträge in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table zurück. Weitere Methoden zum Zählen von Einträgen stehen unter "table_conn_cnt" und table_avl.

term_events: string Gibt alle bekannten Beendigungsereignisse für alle einem Stream zugeordneten Entitäten auf Client- und Server-Seite zurück. Ein Tupel aus sieben Elementen mit folgenden Informationen wird zurückgegeben:

    - die Beendigungsereignisse der Frontend-Verbindung
    - die Beendigungsereignisse der Frontend-Mux-Verbindung
    - die Beendigungsereignisse des Frontend-Stream-Endpunktdeskriptors
      (des Mux-Streams oder des Applets)
    - die Beendigungsereignisse des Streams
    - die Beendigungsereignisse des Backend-Stream-Endpunktdeskriptors
      (des Mux-Streams oder des Applets)
    - die Beendigungsereignisse der Backend-Mux-Verbindung
    - die Beendigungsereignisse der Backend-Verbindung

Auf jeder Ebene werden die ersten vier Ereignisse gemeldet. Wurde für eine bestimmte Ebene noch kein Ereignis gemeldet, wird eine leere Zeichenkette zurückgegeben. Werden Beendigungsereignisse nicht unterstützt, wird "-" zurückgegeben.

Dies darf ausschließlich zur Fehlersuche verwendet werden. Das genaue Format ist nicht dokumentiert, da es sich je nach Anforderungen der Entwickler ändern kann.

tgroup: integer Gibt eine Ganzzahl zurück, die der Position der Thread-Gruppe entspricht, welche die Funktion aufruft, zwischen 0 und (global.thread-groups - 1). Dies ist für die Protokollierung und Fehlersuche nützlich.

thread: integer Gibt eine Ganzzahl zurück, die der Position des Threads entspricht, der die Funktion aufruft, zwischen 0 und (global.nbthread-1). Dies ist für die Protokollierung und Fehlersuche nützlich.

txn.id32: integer Gibt die interne Transaktions-ID zurück. Sie ist eine 32bits-Ganzzahl. Ihr Wert ist daher nicht uneingeschränkt eindeutig; Transaktions-IDs können umlaufen. Wie oft dies geschieht, hängt von der Anfragerate ab. In der Praxis sollte dies kein Problem sein. Für eine tatsächlich eindeutige ID siehe die Direktive "unique-id-format".

txn.sess_term_state: string Gibt den im Protokoll gemeldeten Beendigungszustand des TCP- oder HTTP-Streams zurück. Dies ist eine Zeichenkette aus 2 Zeichen: der abschließende Stream-Zustand, gefolgt vom Ereignis, das seine Beendigung verursacht hat. Die Liste möglicher Ereignisse steht in [Abschnitt 8.5](/de/haproxy/configuration-logging/#section-8-5) zum Stream-Zustand beim Verbindungsabbau. Zurückgegeben wird der aktuelle Wert zum Zeitpunkt der Auswertung des Sample-Abrufs. Dieser kann sich noch ändern. Außer bei Verwendung mit ACLs in "http-after-response"-Regelsätzen oder in Protokollmeldungen ist der Wert stets "--".

Beispiel:

```shell
# Return a 429-Too-Many-Requests if stream timed out in queue
http-after-response set-status 429 if { txn.sess_term_state  "sQ" }
```

uptime: integer Gibt die Laufzeit des aktuellen HAProxy-Workers in Sekunden zurück.

<a id="entry-7-3-2-uuid-string"></a>

**`uuid([<version>]): string`**

```haproxy
uuid([<version>]): string
```

Gibt eine UUID gemäß RFC 9562 zurück. Ist keine Version angegeben, wird eine UUID der Version 4 (vollständig zufällig) zurückgegeben.

Unterstützt werden die Versionen 4 und 7.

<a id="entry-7-3-2-var-undefined"></a>

**`var(<var-name>[,<default>]): undefined`**

```haproxy
var(<var-name>[,<default>]): undefined
```

Gibt eine Variable mit dem gespeicherten Typ zurück. Ist die Variable nicht gesetzt, schlägt der Sample-Abruf fehl, sofern kein Standardwert angegeben ist. Ist ein Standardwert angegeben, wird dieser als Zeichenkette zurückgegeben. Leere Zeichenketten sind zulässig. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/haproxy/configuration-basics/#section-2-8).

<a id="entry-7-3-2-dump-all-vars-string"></a>

**`dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string`**

```haproxy
dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string
```

Gibt eine Liste aller Variablen im angegebenen Gültigkeitsbereich zurück, optional nach Namenspräfix gefiltert und mit anpassbarem Trennzeichen.

Ausgabeformat: var1=value1`<delim>`var2=value2`<delim>`...

Wertkodierung nach Typ:

- Zeichenketten: in Anführungszeichen und maskiert (", &#92;, &#92;r,
  &#92;n, &#92;b, &#92;0). Beispiel:
  txn.name="John &#92;"Doe&#92;""
- Binärdaten: hexadezimal kodiert mit dem Präfix 'x', ohne Anführungszeichen. Beispiel: txn.data=x48656c6c6f
- Ganzzahlen: dezimal, ohne Anführungszeichen. Beispiel: txn.count=42
- Boolesche Werte: "true" oder "false", ohne Anführungszeichen. Beispiel: txn.active=true
- Adressen: IP-Adresszeichenkette, ohne Anführungszeichen. Beispiel: txn.client=192.168.1.1
- HTTP-Methoden: Zeichenkette in Anführungszeichen. Beispiel: req.method="GET"

Argumente:

- `<scope>` (optional): sess, txn, req, res oder proc. Wird es weggelassen, werden alle diese Gültigkeitsbereiche in der hier angegebenen Reihenfolge durchlaufen.

- `<prefix>` (optional): Filtert Variablen, deren Namen mit dem angegebenen Präfix beginnen, nachdem das Präfix des Gültigkeitsbereichs entfernt wurde. Hinweis zur Leistung: Bei der Präfixfilterung werden weiterhin alle Variablen des Gültigkeitsbereichs durchlaufen. Dies sollte nicht in Konfigurationen mit Tausenden von Variablen verwendet werden.

- `<delimiter>` (optional): Zeichenkette zur Trennung der Variablen. Standardmäßig ", " (Komma und Leerzeichen). Jede beliebige Zeichenkette ist möglich. Zur Erinnerung: Kommas oder Leerzeichen müssen zum Übergeben in einem Funktionsargument in einfache oder doppelte Anführungszeichen eingeschlossen werden. Steht der Ausdruck selbst bereits in Anführungszeichen, verwenden Sie die jeweils andere Art.

Rückgabewert:

- Bei Erfolg: Zeichenkette mit allen passenden Variablen
- Bei einem Fehler: leer (der Sample-Abruf schlägt fehl), wenn der Ausgabepuffer zu klein ist. Die Funktion schneidet die Ausgabe nicht ab, sondern schlägt vollständig fehl, um Teildaten zu vermeiden.

Dies ist besonders für die Fehlersuche, Protokollierung oder den Export von Variablenzuständen nützlich.

Beispiele:

```shell
# Dump all transaction variables
http-request return string %[dump_all_vars(txn)]

# Dump only variables starting with "user"
http-request set-header X-User-Vars "%[dump_all_vars(txn,user)]"

# Dump all process variables
http-request return string %[dump_all_vars(proc)]

# Custom delimiter (semicolon)
http-request set-header X-Vars "%[dump_all_vars(txn,,; )]"

# Force the default delimiter (comma space)
http-request set-header X-Vars "%[dump_all_vars(txn,,', ')]"

# Prefix filter with custom delimiter
http-request set-header X-Session "%[dump_all_vars(sess,user,|)]"

```

wait_end: boolean Dieser Abruf gibt entweder true zurück, wenn die Prüfzeit abgelaufen ist, oder liefert kein Sample. Er wird nur in ACLs in Verbindung mit der Inhaltsanalyse verwendet, um eine verfrühte falsche Entscheidung zu vermeiden. Er kann auch Aktionen verzögern, beispielsweise die verzögerte Ablehnung bestimmter Adressen. Da er entweder die Regelauswertung anhält oder sofort true zurückgibt, wird empfohlen, diese ACL als letzte in einer Regel zu verwenden. Die vordefinierte ACL "WAIT_END" ist stets ohne vorherige Deklaration verfügbar. Diese Prüfung wurde für die Inhaltsprüfung von TCP-Anfragen entwickelt.

Beispiele:

```shell
# delay every incoming request by 2 seconds
tcp-request inspect-delay 2s
tcp-request content accept if WAIT_END

# don't immediately tell bad guys they are rejected
tcp-request inspect-delay 10s
acl goodguys src 10.0.0.0/24
acl badguys  src 10.0.1.0/24
tcp-request content accept if goodguys
tcp-request content reject if badguys WAIT_END
tcp-request content reject
```

waiting_entity: string Gibt die Identität der Entität zurück, die auf die Fortsetzung ihrer Verarbeitung wartete, als ein Fehler oder eine Zeitüberschreitung auftrat. Dies kann beispielsweise eine Regel oder ein Filter sein. Diese Liste ist jedoch nicht vollständig, und das Format aller möglichen Entitäten ist nicht zwingend dokumentiert.

Ist die Entität eine Regel, wird ihre Position zurückgegeben: die Konfigurationsdatei, die die Regel enthält, gefolgt von der Zeile, in der sie in dieser Datei definiert ist, getrennt durch einen Doppelpunkt.

Bei einem Filter wird der von den Entwicklern festgelegte Bezeichner zurückgegeben. Ist dieser Bezeichner nicht definiert, wird ein Hexadezimalwert zurückgegeben, der einem eindeutigen internen Bezeichner entspricht.

Der Hauptzweck dieser Funktion besteht darin, die Entität in Protokollen zu melden, die die Stream-Analyse blockierte, als ein Fehler oder eine Zeitüberschreitung die Verarbeitung unterbrach. Dies unterstützt die Fehlersuche. Die zu Entitäten zurückgegebenen Informationen können sich im Laufe der Zeit ändern und dürfen ausschließlich zur Fehlersuche verwendet werden.

Beispiel:

```shell
# Log the waiting entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[waiting_entity,when(error)]
```

### 7.3.3. Sample-Abruf auf Schicht 4 {#section-7-3-3}

Schicht 4 beschreibt üblicherweise nur die Transportschicht, die in HAProxy der Verbindung am nächsten liegt und auf der noch keine Inhalte verfügbar sind. Die hier beschriebenen Abrufmethoden können bereits in den Regelsätzen "tcp-request connection" verwendet werden, sofern sie keine erst später verfügbaren Informationen benötigen. Dazu gehören im Allgemeinen TCP/IP-Adressen und Ports sowie Elemente aus Stick Tables, die sich auf die eingehende Verbindung beziehen. Beim Abruf eines Werts aus einem Sticky-Zähler kann die Zählernummer mit den vordefinierten Präfixen "sc0\_", "sc1\_" oder "sc2\_" ausdrücklich auf 0, 1 oder 2 gesetzt werden. Diese drei vordefinierten Präfixe können nur verwendet werden, wenn der globale Wert "tune.stick-counters" nicht größer als 3 ist. Andernfalls kann die Zählernummer als erstes ganzzahliges Argument bei Verwendung des Präfixes "sc\_" angegeben werden, von "sc_0" bis "sc_N", wobei N gleich (tune.stick-counters-1) ist. Mit der Form "sc\*" kann optional eine Tabelle angegeben werden. In diesem Fall wird der derzeit verfolgte Schlüssel in dieser alternativen Tabelle gesucht, anstelle der aktuell verfolgten Tabelle.

Übersicht über die Sample-Abrufmethoden in diesem Abschnitt und ihre jeweiligen Typen:

```text
  Schlüsselwort                                    Ausgabetyp
-------------------------------------------------+-------------
accept_date([<unit>])                              integer
bc.timer.connect                                   integer
bc_be_queue                                        integer
bc_dst                                             ip
bc_dst_port                                        integer
bc_err                                             integer
bc_err_name                                        string
bc_err_str                                         string
bc_glitches                                        integer
bc_http_major                                      integer
bc_nb_streams                                      integer
bc_reused                                          boolean
bc_rtt(<unit>)                                     integer
bc_rttvar(<unit>)                                  integer
bc_settings_streams_limit                          integer
bc_src                                             ip
bc_src_port                                        integer
bc_srv_queue                                       integer
be_id                                              integer
be_name                                            string
be_connect_timeout                                 integer
be_queue_timeout                                   integer
be_server_timeout                                  integer
be_tarpit_timeout                                  integer
be_tunnel_timeout                                  integer
bytes_in                                           integer
bytes_out                                          integer
cur_connect_timeout                                integer
cur_client_timeout                                 integer
cur_queue_timeout                                  integer
cur_server_timeout                                 integer
cur_tarpit_timeout                                 integer
cur_tunnel_timeout                                 integer
dst                                                ip
dst_conn                                           integer
dst_is_local                                       boolean
dst_port                                           integer
fc.timer.handshake                                 integer
fc.timer.total                                     integer
fc_dst                                             ip
fc_dst_is_local                                    boolean
fc_dst_port                                        integer
fc_err                                             integer
fc_err_name                                        string
fc_err_str                                         string
fc_fackets                                         integer
fc_glitches                                        integer
fc_http_major                                      integer
fc_lost                                            integer
fc_nb_streams                                      integer
fc_pp_authority                                    string
fc_pp_tlv(<id>)                                    string
fc_pp_unique_id                                    string
fc_rcvd_proxy                                      boolean
fc_reordering                                      integer
fc_retrans                                         integer
fc_rtt(<unit>)                                     integer
fc_rttvar(<unit>)                                  integer
fc_sacked                                          integer
fc_saved_syn                                       binary
fc_settings_streams_limit                          integer
fc_src                                             ip
fc_src_is_local                                    boolean
fc_src_port                                        integer
fc_unacked                                         integer
fe_tarpit_timeout                                  integer
fe_client_timeout                                  integer
fe_defbe                                           string
fe_id                                              integer
fe_name                                            string
req.bytes_in                                       integer
req.bytes_out                                      integer
res.bytes_in                                       integer
res.bytes_out                                      integer
res.timer.data                                     integer
sc0_bytes_in_rate([<table>])                       integer
sc0_bytes_out_rate([<table>])                      integer
sc0_clr_gpc0([<table>])                            integer
sc0_clr_gpc1([<table>])                            integer
sc0_conn_cnt([<table>])                            integer
sc0_conn_cur([<table>])                            integer
sc0_conn_rate([<table>])                           integer
sc0_get_gpc0([<table>])                            integer
sc0_get_gpc1([<table>])                            integer
sc0_get_gpt0([<table>])                            integer
sc0_glitch_cnt([<table>])                          integer
sc0_glitch_rate([<table>])                         integer
sc0_gpc0_rate([<table>])                           integer
sc0_gpc1_rate([<table>])                           integer
sc0_http_err_cnt([<table>])                        integer
sc0_http_err_rate([<table>])                       integer
sc0_http_fail_cnt([<table>])                       integer
sc0_http_fail_rate([<table>])                      integer
sc0_http_req_cnt([<table>])                        integer
sc0_http_req_rate([<table>])                       integer
sc0_inc_gpc0([<table>])                            integer
sc0_inc_gpc1([<table>])                            integer
sc0_kbytes_in([<table>])                           integer
sc0_kbytes_out([<table>])                          integer
sc0_key                                            any
sc0_sess_cnt([<table>])                            integer
sc0_sess_rate([<table>])                           integer
sc0_tracked([<table>])                             boolean
sc0_trackers([<table>])                            integer
sc1_bytes_in_rate([<table>])                       integer
sc1_bytes_out_rate([<table>])                      integer
sc1_clr_gpc0([<table>])                            integer
sc1_clr_gpc1([<table>])                            integer
sc1_conn_cnt([<table>])                            integer
sc1_conn_cur([<table>])                            integer
sc1_conn_rate([<table>])                           integer
sc1_get_gpc0([<table>])                            integer
sc1_get_gpc1([<table>])                            integer
sc1_get_gpt0([<table>])                            integer
sc1_glitch_cnt([<table>])                          integer
sc1_glitch_rate([<table>])                         integer
sc1_gpc0_rate([<table>])                           integer
sc1_gpc1_rate([<table>])                           integer
sc1_http_err_cnt([<table>])                        integer
sc1_http_err_rate([<table>])                       integer
sc1_http_fail_cnt([<table>])                       integer
sc1_http_fail_rate([<table>])                      integer
sc1_http_req_cnt([<table>])                        integer
sc1_http_req_rate([<table>])                       integer
sc1_inc_gpc0([<table>])                            integer
sc1_inc_gpc1([<table>])                            integer
sc1_kbytes_in([<table>])                           integer
sc1_kbytes_out([<table>])                          integer
sc1_key                                            any
sc1_sess_cnt([<table>])                            integer
sc1_sess_rate([<table>])                           integer
sc1_tracked([<table>])                             boolean
sc1_trackers([<table>])                            integer
sc2_bytes_in_rate([<table>])                       integer
sc2_bytes_out_rate([<table>])                      integer
sc2_clr_gpc0([<table>])                            integer
sc2_clr_gpc1([<table>])                            integer
sc2_conn_cnt([<table>])                            integer
sc2_conn_cur([<table>])                            integer
sc2_conn_rate([<table>])                           integer
sc2_get_gpc0([<table>])                            integer
sc2_get_gpc1([<table>])                            integer
sc2_get_gpt0([<table>])                            integer
sc2_glitch_cnt([<table>])                          integer
sc2_glitch_rate([<table>])                         integer
sc2_gpc0_rate([<table>])                           integer
sc2_gpc1_rate([<table>])                           integer
sc2_http_err_cnt([<table>])                        integer
sc2_http_err_rate([<table>])                       integer
sc2_http_fail_cnt([<table>])                       integer
sc2_http_fail_rate([<table>])                      integer
sc2_http_req_cnt([<table>])                        integer
sc2_http_req_rate([<table>])                       integer
sc2_inc_gpc0([<table>])                            integer
sc2_inc_gpc1([<table>])                            integer
sc2_kbytes_in([<table>])                           integer
sc2_kbytes_out([<table>])                          integer
sc2_key                                            any
sc2_sess_cnt([<table>])                            integer
sc2_sess_rate([<table>])                           integer
sc2_tracked([<table>])                             boolean
sc2_trackers([<table>])                            integer
sc_bytes_in_rate(<ctr>[,<table>])                  integer
sc_bytes_out_rate(<ctr>[,<table>])                 integer
sc_clr_gpc(<idx>,<ctr>[,<table>])                  integer
sc_clr_gpc0(<ctr>[,<table>])                       integer
sc_clr_gpc1(<ctr>[,<table>])                       integer
sc_conn_cnt(<ctr>[,<table>])                       integer
sc_conn_cur(<ctr>[,<table>])                       integer
sc_conn_rate(<ctr>[,<table>])                      integer
sc_get_gpc(<idx>,<ctr>[,<table>])                  integer
sc_get_gpc0(<ctr>[,<table>])                       integer
sc_get_gpc1(<ctr>[,<table>])                       integer
sc_get_gpt(<idx>,<ctr>[,<table>])                  integer
sc_get_gpt0(<ctr>[,<table>])                       integer
sc_glitch_cnt(<ctr>[,<table>])                     integer
sc_glitch_rate(<ctr>[,<table>])                    integer
sc_gpc0_rate(<ctr>[,<table>])                      integer
sc_gpc1_rate(<ctr>[,<table>])                      integer
sc_gpc_rate(<idx>,<ctr>[,<table>])                 integer
sc_http_err_cnt(<ctr>[,<table>])                   integer
sc_http_err_rate(<ctr>[,<table>])                  integer
sc_http_fail_cnt(<ctr>[,<table>])                  integer
sc_http_fail_rate(<ctr>[,<table>])                 integer
sc_http_req_cnt(<ctr>[,<table>])                   integer
sc_http_req_rate(<ctr>[,<table>])                  integer
sc_inc_gpc(<idx>,<ctr>[,<table>])                  integer
sc_inc_gpc0(<ctr>[,<table>])                       integer
sc_inc_gpc1(<ctr>[,<table>])                       integer
sc_kbytes_in(<ctr>[,<table>])                      integer
sc_kbytes_out(<ctr>[,<table>])                     integer
sc_key(<ctr>)                                      any
sc_sess_cnt(<ctr>[,<table>])                       integer
sc_sess_rate(<ctr>[,<table>])                      integer
sc_tracked(<ctr>[,<table>])                        boolean
sc_trackers(<ctr>[,<table>])                       integer
so_id                                              integer
so_name                                            string
src                                                ip
src_bytes_in_rate([<table>])                       integer
src_bytes_out_rate([<table>])                      integer
src_clr_gpc(<idx>[,<table>])                       integer
src_clr_gpc0([<table>])                            integer
src_clr_gpc1([<table>])                            integer
src_conn_cnt([<table>])                            integer
src_conn_cur([<table>])                            integer
src_conn_rate([<table>])                           integer
src_get_gpc(<idx>[,<table>])                       integer
src_get_gpc0([<table>])                            integer
src_get_gpc1([<table>])                            integer
src_get_gpt(<idx>[,<table>])                       integer
src_get_gpt0([<table>])                            integer
src_glitch_cnt([<table>])                          integer
src_glitch_rate([<table>])                         integer
src_gpc0_rate([<table>])                           integer
src_gpc1_rate([<table>])                           integer
src_gpc_rate(<idx>[,<table>])                      integer
src_http_err_cnt([<table>])                        integer
src_http_err_rate([<table>])                       integer
src_http_fail_cnt([<table>])                       integer
src_http_fail_rate([<table>])                      integer
src_http_req_cnt([<table>])                        integer
src_http_req_rate([<table>])                       integer
src_inc_gpc(<idx>[,<table>])                       integer
src_inc_gpc0([<table>])                            integer
src_inc_gpc1([<table>])                            integer
src_is_local                                       boolean
src_kbytes_in([<table>])                           integer
src_kbytes_out([<table>])                          integer
src_port                                           integer
src_sess_cnt([<table>])                            integer
src_sess_rate([<table>])                           integer
src_updt_conn_cnt([<table>])                       integer
srv_id                                             integer
srv_name                                           string
txn.conn_retries                                   integer
txn.redispatched                                   boolean
-------------------------------------------------+-------------
```

Ausführliche Liste:

<a id="entry-7-3-3-accept-date-integer"></a>

**`accept_date([<unit>]): integer`**

```haproxy
accept_date([<unit>]): integer
```

Dies ist der genaue Zeitpunkt, zu dem HAProxy die Verbindung empfangen hat. Er kann geringfügig von dem im Netzwerk beobachteten Zeitpunkt abweichen, wenn die Verbindung in der Backlog-Warteschlange des Systems warten musste. Üblicherweise ist dies derselbe Zeitpunkt, der in den Protokollen vorgelagerter Firewalls erscheinen kann. Im HTTP-Modus wird das Feld accept_date auf den ersten Zeitpunkt zurückgesetzt, zu dem die Verbindung für eine neue Anfrage bereit ist: bei HTTP/1 am Ende der vorherigen Antwort, bei HTTP/2 unmittelbar nach der vorherigen Anfrage.

Gibt einen Wert als Anzahl von Sekunden seit der Epoche zurück.

`<unit>` ist optional und kann auf "s" für Sekunden (Standardverhalten), "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Einheit angegeben, ist der Rückgabewert eine Ganzzahl, die Sekunden, Millisekunden oder Mikrosekunden seit der Epoche angibt. Dies ist nützlich, wenn eine Zeitauflösung unter einer Sekunde benötigt wird.

bc.timer.connect: integer Gesamtzeit zum Aufbau der TCP-Verbindung zum Server. Entspricht %Tc in log-format und wird in Millisekunden (ms) angegeben. Weitere Informationen stehen in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

bc_be_queue: integer Anzahl der aus der Warteschlange entnommenen Streams während des Wartens auf einen Verbindungsplatz im Ziel-Backend. Entspricht %bq in log-format.

bc_dst: ip Die Ziel-IP-Adresse der Verbindung auf der Server-Seite, also die Serveradresse, zu der HAProxy die Verbindung aufgebaut hat. Sie hat den Typ IP und funktioniert sowohl mit IPv4- als auch mit IPv6-Tabellen. In IPv6-Tabellen wird eine IPv4-Adresse gemäß RFC 4291 auf ihre IPv6-Entsprechung abgebildet.

bc_dst_port: integer Gibt eine Ganzzahl zurück, die dem TCP-Zielport der Verbindung auf der Server-Seite entspricht, also dem Port, zu dem HAProxy die Verbindung aufgebaut hat.

bc_err: integer Gibt die ID des Fehlers zurück, der möglicherweise auf der aktuellen Backend-Verbindung aufgetreten ist. Eine vollständige Liste der Fehlercodes mit den zugehörigen Fehlermeldungen steht beim Abruf "fc_err_str".

bc_err_name: string Gibt den internen Fehlernamen zurück, der das auf der Backend-Verbindung aufgetretene Problem beschreibt, das zum Fehlschlagen der Verbindung führte. Diese Zeichenkette besteht aus einem einzigen Wort und ist leer, wenn kein Fehler vorliegt. Sie entspricht der Spalte "name" in der beim Schlüsselwort "fc_err_str" gezeigten Tabelle.

bc_err_str: string Gibt eine Fehlermeldung zurück, die das auf der aktuellen Backend-Verbindung aufgetretene Problem beschreibt, das zum Fehlschlagen der Verbindung führte. Eine vollständige Liste der Fehlercodes mit den zugehörigen Fehlermeldungen steht beim Abruf "fc_err_str".

bc_glitches: integer Gibt die Anzahl der auf der Backend-Verbindung gezählten Protokollstörungen zurück. Dazu gehören üblicherweise Protokollverletzungen sowie kleine Anomalien, die auf einen fehlerhaften oder sich falsch verhaltenden Server hindeuten und Probleme in der Infrastruktur verursachen können, etwa vorzeitige Verbindungsabbrüche oder häufige TLS-Neuverhandlungen. Auch Antworten, die zu groß für einen einzelnen Puffer sind, können solche Störungen verursachen und HTTP-502-Fehler erklären. Idealerweise sollte dieser Wert null bleiben; im Allgemeinen ist jedoch ein sehr niedriger Wert im Verhältnis zur Gesamtzahl der Anfragen unproblematisch. Diese Werte sollten normalerweise nicht als alarmierend gelten, insbesondere kleine Werte. Ein plötzlicher Anstieg kann allerdings auf eine Anomalie hinweisen. Nicht alle Protokoll-Multiplexer erfassen diese Kennzahl. Weitere Einzelheiten zu den Ereignissen lassen sich nur durch aktivierte Traces erhalten, die den gesamten Austausch erfassen.

bc_http_major: integer Gibt die HTTP-Hauptversionskodierung der Backend-Verbindung zurück: 1 für HTTP/0.9 bis HTTP/1.1 oder 2 für HTTP/2. Dies beruht auf der Kodierung auf der Leitung und nicht auf der im Anfrage-Header angegebenen Version.

bc_nb_streams: integer Gibt die Anzahl der auf der Backend-Verbindung geöffneten Streams zurück.

bc_reused: boolean Gibt true zurück, wenn die Übertragung über eine wiederverwendete Backend-Verbindung erfolgte.

<a id="entry-7-3-3-bc-rtt-integer"></a>

**`bc_rtt(<unit>): integer`**

```haproxy
bc_rtt(<unit>): integer
```

Gibt die vom Kernel gemessene Round Trip Time (RTT) der Backend-Verbindung zurück. `<unit>` ist optional; die Standardeinheit ist Millisekunden. `<unit>` kann auf "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Serververbindung nicht hergestellt, handelt es sich nicht um TCP oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

<a id="entry-7-3-3-bc-rttvar-integer"></a>

**`bc_rttvar(<unit>): integer`**

```haproxy
bc_rttvar(<unit>): integer
```

Gibt die vom Kernel gemessene Varianz der Round Trip Time (RTT) der Backend-Verbindung zurück. `<unit>` ist optional; die Standardeinheit ist Millisekunden. `<unit>` kann auf "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Serververbindung nicht hergestellt, handelt es sich nicht um TCP oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

bc_settings_streams_limit: integer Gibt die maximal zulässige Anzahl von Streams auf der Backend-Verbindung zurück. Bei TCP- und HTTP/1.1-Verbindungen ist dies stets 1. Bei anderen Protokollen hängt der Wert von den mit dem Server ausgehandelten Einstellungen ab.

bc_src: ip Die Quell-IP-Adresse der Verbindung auf der Server-Seite, also die Adresse, von der aus HAProxy die Verbindung aufgebaut hat. Sie hat den Typ IP und funktioniert sowohl mit IPv4- als auch mit IPv6-Tabellen. In IPv6-Tabellen werden IPv4-Adressen gemäß RFC 4291 auf ihre IPv6-Entsprechung abgebildet.

bc_src_port: integer Gibt eine Ganzzahl zurück, die dem TCP-Quellport der Verbindung auf der Server-Seite entspricht, also dem Port, von dem aus HAProxy die Verbindung aufgebaut hat.

bc_srv_queue: integer Anzahl der aus der Warteschlange entnommenen Streams während des Wartens auf einen Verbindungsplatz auf dem Zielserver. Entspricht %sq in log-format.

be_id: integer Gibt eine Ganzzahl mit der ID des aktuellen Backends zurück. Kann in Frontends bei Antworten verwendet werden, um zu prüfen, welches Backend die Anfrage verarbeitet hat. Wird der Abruf in einem Frontend verwendet und wurde kein Backend benutzt, wird die ID des aktuellen Frontends zurückgegeben. Kann auch in einem tcp-check- oder http-check-Regelsatz verwendet werden.

be_connect_timeout: integer Gibt den konfigurierten Wert der Zeitüberschreitung für den Verbindungsaufbau des aktuellen Backends in Millisekunden zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden. Siehe auch "cur_connect_timeout".

be_name: string Gibt eine Zeichenkette mit dem Namen des aktuellen Backends zurück. Kann in Frontends bei Antworten verwendet werden, um zu prüfen, welches Backend die Anfrage verarbeitet hat. Wird der Abruf in einem Frontend verwendet und wurde kein Backend benutzt, wird der Name des aktuellen Frontends zurückgegeben. Kann auch in einem tcp-check- oder http-check-Regelsatz verwendet werden.

be_queue_timeout: integer Gibt den konfigurierten Wert der Zeitüberschreitung für die Warteschlange des aktuellen Backends in Millisekunden zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden. Siehe auch "cur_queue_timeout".

be_server_timeout: integer Gibt den konfigurierten Wert der Zeitüberschreitung für den Server des aktuellen Backends in Millisekunden zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden. Siehe auch "cur_server_timeout".

be_tarpit_timeout: integer Gibt den konfigurierten Wert der Zeitüberschreitung für die Warteschlange des aktuellen Backends in Millisekunden zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden. Siehe auch "cur_tarpit_timeout".

be_tunnel_timeout: integer Gibt den konfigurierten Wert der Zeitüberschreitung für den Tunnel des aktuellen Backends in Millisekunden zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden. Siehe auch "cur_tunnel_timeout".

bytes_in: integer Siehe "req.bytes_in".

bytes_out: integer Siehe "res.bytes_in".

cur_connect_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für den Verbindungsaufbau in Millisekunden zurück. Standardmäßig entspricht dies be_connect_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "be_connect_timeout".

cur_client_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für den Client in Millisekunden zurück. Standardmäßig entspricht dies fe_client_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "fe_client_timeout".

cur_queue_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für die Warteschlange in Millisekunden zurück. Standardmäßig entspricht dies be_queue_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "be_queue_timeout".

cur_server_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für den Server in Millisekunden zurück. Standardmäßig entspricht dies be_server_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "be_server_timeout".

cur_tarpit_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für die Tarpit in Millisekunden zurück. Standardmäßig entspricht dies fe_tarpit_timeout/be_tarpit_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "fe_tarpit_timeout" und "be_tarpit_timeout".

cur_tunnel_timeout: integer Gibt die aktuell für den Stream geltende Zeitüberschreitung für den Tunnel in Millisekunden zurück. Standardmäßig entspricht dies be_tunnel_timeout, sofern keine Regel "set-timeout" angewendet wurde. Siehe auch "be_tunnel_timeout".

dst: ip Die Ziel-IP-Adresse der Verbindung auf der Client-Seite, also die Adresse, zu der der Client die Verbindung aufgebaut hat. Beliebige tcp/http-Regeln können diese Adresse ändern. Dies kann im transparenten Modus nützlich sein. Sie hat den Typ IP und funktioniert sowohl mit IPv4- als auch mit IPv6-Tabellen. In IPv6-Tabellen wird eine IPv4-Adresse gemäß RFC 4291 auf ihre IPv6-Entsprechung abgebildet. Hat die eingehende Verbindung eine Adressübersetzung oder Umleitung mit Verbindungsverfolgung durchlaufen, wird die ursprüngliche Zieladresse vor der Umleitung gemeldet. Auf Linux-Systemen können Quelle und Ziel in seltenen Fällen vertauscht erscheinen, wenn der sysctl-Wert nf_conntrack_tcp_loose gesetzt ist: Eine verspätete Antwort kann eine abgelaufene Verbindung erneut öffnen und dabei vertauschen, was als Quelle und Ziel angesehen wird.

dst_conn: integer Gibt eine Ganzzahl zurück, die der Anzahl derzeit auf demselben Socket hergestellter Verbindungen entspricht, einschließlich der gerade ausgewerteten Verbindung. Dies wird normalerweise mit ACLs verwendet, kann aber auch Informationen in einem HTTP-Header oder in Protokollen an Server weitergeben. Damit lässt sich vor einer vollständigen Sperre eine Entschuldigungsseite zurückgeben oder ein bestimmtes Backend zum Ableiten neuer Anfragen verwenden, wenn der Socket als ausgelastet gilt. So lassen sich verschiedenen lauschenden Ports oder Adressen unterschiedliche Grenzwerte zuweisen. Siehe auch die Abrufe "fe_conn" und "be_conn".

dst_is_local: boolean Gibt true zurück, wenn die Zieladresse der eingehenden Verbindung lokal auf dem System liegt, oder false, wenn die Adresse auf dem System nicht vorhanden ist, die Verbindung also im transparenten Modus abgefangen wurde. Damit lassen sich standardmäßig bestimmte Regeln auf weitergeleiteten Verkehr und andere Regeln auf Verkehr zur tatsächlichen Adresse des Rechners anwenden. Beispielsweise könnte die Statistikseite nur an dieser Adresse bereitgestellt oder SSH-Zugriff lokal umgeleitet werden. Die Prüfung benötigt einige Systemaufrufe und sollte daher möglichst nur einmal pro Verbindung erfolgen.

dst_port: integer Gibt eine Ganzzahl zurück, die dem TCP-Zielport der Verbindung auf der Client-Seite entspricht, also dem Port, zu dem der Client die Verbindung aufgebaut hat. Beliebige tcp/http-Regeln können diese Adresse ändern. Dies kann im transparenten Modus verwendet werden, beim Zuweisen dynamischer Ports an bestimmte Clients für eine gesamte Anwendungssitzung, um alle Benutzer an denselben Server zu binden, oder um einem Server die Zielportinformationen in einem HTTP-Header mitzuteilen.

fc.timer.handshake: integer Gesamtzeit zum Akzeptieren einer TCP-Verbindung und zum Ausführen der Handshakes für Protokolle niedriger Ebenen. Derzeit sind dies proxy-protocol und SSL. Entspricht %Th in log-format und wird in Millisekunden (ms) angegeben. Weitere Informationen stehen in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

fc.timer.total: integer Gesamtdauer des Streams, vom Zeitpunkt der Annahme durch den Proxy bis zum Schließen beider Enden. Entspricht %Tt in log-format und wird in Millisekunden (ms) angegeben. Weitere Informationen stehen in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

fc_dst: ip Die ursprüngliche Ziel-IP-Adresse der Verbindung auf der Client-Seite. Nur Regeln "tcp-request connection" können diese Adresse ändern. Einzelheiten stehen unter "dst".

fc_dst_is_local: boolean Gibt true zurück, wenn die ursprüngliche Zieladresse der eingehenden Verbindung lokal auf dem System liegt, oder false, wenn die Adresse auf dem System nicht vorhanden ist. Einzelheiten stehen unter "dst_is_local".

fc_dst_port: integer Gibt eine Ganzzahl zurück, die dem ursprünglichen TCP-Zielport der Verbindung auf der Client-Seite entspricht. Nur Regeln "tcp-request connection" können diese Adresse ändern. Einzelheiten stehen unter "dst-port".

fc_err: integer Gibt die ID des Fehlers zurück, der möglicherweise auf der aktuellen Verbindung aufgetreten ist. Jeder strikt positive Wert dieses Abrufs zeigt an, dass die Verbindung nicht erfolgreich war und ein Fehlerprotokolleintrag ausgegeben würde, wie in [Abschnitt 8.2.5](/de/haproxy/configuration-logging/#section-8-2-5) beschrieben. Eine vollständige Liste der Fehlercodes mit den zugehörigen Fehlermeldungen steht beim Abruf "fc_err_str".

fc_err_name: string Gibt den internen Fehlernamen zurück, der das auf der Frontend-Verbindung aufgetretene Problem beschreibt, das zum Fehlschlagen der Verbindung führte. Diese Zeichenkette besteht aus einem einzigen Wort und ist leer, wenn kein Fehler vorliegt. Sie entspricht der Spalte "name" in der beim Schlüsselwort "fc_err_str" gezeigten Tabelle.

fc_err_str: string Gibt eine Fehlermeldung zurück, die das auf der aktuellen Verbindung aufgetretene Problem beschreibt, das zum Fehlschlagen der Verbindung führte. Diese Zeichenkette entspricht dem Teil "message" des Fehlerprotokollformats (siehe [Abschnitt 8.2.5](/de/haproxy/configuration-logging/#section-8-2-5)). Eine vollständige Liste der Fehlercodes mit den zugehörigen Fehlermeldungen folgt unten:

```text
  +----+------------------+-------------------------------------------------------------------------+
  | ID | Name             | Meldung                                                                 |
  +----+------------------+-------------------------------------------------------------------------+
  | 0  | -                | "Success"                                                               |
  | 1  | CONF_FDLIM       | "Reached configured maxconn value"                                      |
  | 2  | PROC_FDLIM       | "Too many sockets on the process"                                       |
  | 3  | SYS_FDLIM        | "Too many sockets on the system"                                        |
  | 4  | SYS_MEMLIM       | "Out of system buffers"                                                 |
  | 5  | NOPROTO          | "Protocol or address family not supported"                              |
  | 6  | SOCK_ERR         | "General socket error"                                                  |
  | 7  | PORT_RANGE       | "Source port range exhausted"                                           |
  | 8  | CANT_BIND        | "Can't bind to source address"                                          |
  | 9  | FREE_PORTS       | "Out of local source ports on the system"                               |
  | 10 | ADDR_INUSE       | "Local source address already in use"                                   |
  | 11 | PRX_EMPTY        | "Connection closed while waiting for PROXY protocol header"             |
  | 12 | PRX_ABORT        | "Connection error while waiting for PROXY protocol header"              |
  | 13 | PRX_TIMEOUT      | "Timeout while waiting for PROXY protocol header"                       |
  | 14 | PRX_TRUNCATED    | "Truncated PROXY protocol header received"                              |
  | 15 | PRX_NOT_HDR      | "Received something which does not look like a PROXY protocol header"   |
  | 16 | PRX_BAD_HDR      | "Received an invalid PROXY protocol header"                             |
  | 17 | PRX_BAD_PROTO    | "Received an unhandled protocol in the PROXY protocol header"           |
  | 18 | CIP_EMPTY        | "Connection closed while waiting for NetScaler Client IP header"        |
  | 19 | CIP_ABORT        | "Connection error while waiting for NetScaler Client IP header"         |
  | 20 | CIP_TIMEOUT      | "Timeout while waiting for a NetScaler Client IP header"                |
  | 21 | CIP_TRUNCATED    | "Truncated NetScaler Client IP header received"                         |
  | 22 | CIP_BAD_MAGIC    | "Received an invalid NetScaler Client IP magic number"                  |
  | 23 | CIP_BAD_PROTO    | "Received an unhandled protocol in the NetScaler Client IP header"      |
  | 24 | SSL_EMPTY        | "Connection closed during SSL handshake"                                |
  | 25 | SSL_ABORT        | "Connection error during SSL handshake"                                 |
  | 26 | SSL_TIMEOUT      | "Timeout during SSL handshake"                                          |
  | 27 | SSL_TOO_MANY     | "Too many SSL connections"                                              |
  | 28 | SSL_NO_MEM       | "Out of memory when initializing an SSL connection"                     |
  | 29 | SSL_RENEG        | "Rejected a client-initiated SSL renegotiation attempt"                 |
  | 30 | SSL_CA_FAIL      | "SSL client CA chain cannot be verified"                                |
  | 31 | SSL_CRT_FAIL     | "SSL client certificate not trusted"                                    |
  | 32 | SSL_MISMATCH     | "Server presented an SSL certificate different from the configured one" |
  | 33 | SSL_MISMATCH_SNI | "Server presented an SSL certificate different from the expected one"   |
  | 34 | SSL_HANDSHAKE    | "SSL handshake failure"                                                 |
  | 35 | SSL_HANDSHAKE_HB | "SSL handshake failure after heartbeat"                                 |
  | 36 | SSL_KILLED_HB    | "Stopped a TLSv1 heartbeat attack (CVE-2014-0160)"                      |
  | 37 | SSL_NO_TARGET    | "Attempt to use SSL on an unknown target (internal error)"              |
  | 38 | SSL_EARLY_FAILED | "Server refused early data"                                             |
  | 39 | SOCKS4_SEND      | "SOCKS4 Proxy write error during handshake"                             |
  | 40 | SOCKS4_RECV      | "SOCKS4 Proxy read error during handshake"                              |
  | 41 | SOCKS4_DENY      | "SOCKS4 Proxy deny the request"                                         |
  | 42 | SOCKS4_ABORT     | "SOCKS4 Proxy handshake aborted by server"                              |
  | 43 | SSL_FATAL        | "SSL fatal error"                                                       |
  | 44 | REVERSE          | "Reverse connect failure"                                               |
  | 45 | POLLERR          | "Poller reported POLLERR"                                               |
  | 46 | EREFUSED         | "ECONNREFUSED returned by OS"                                           |
  | 47 | ERESET           | "ECONNRESET returned by OS"                                             |
  | 48 | EUNREACH         | "ENETUNREACH returned by OS"                                            |
  | 49 | ENOMEM           | "ENOMEM returned by OS"                                                 |
  | 50 | EBADF            | "EBADF returned by OS"                                                  |
  | 51 | EFAULT           | "EFAULT returned by OS"                                                 |
  | 52 | EINVAL           | "EINVAL returned by OS"                                                 |
  | 53 | ENCONN           | "ENCONN returned by OS"                                                 |
  | 54 | ENSOCK           | "ENSOCK returned by OS"                                                 |
  | 55 | ENOBUFS          | "ENOBUFS returned by OS"                                                |
  | 56 | EPIPE            | "EPIPE returned by OS"                                                  |
  +----+------------------+-------------------------------------------------------------------------+
```

fc_fackets: integer Gibt den vom Kernel für die Client-Verbindung gemessenen fack-Zähler zurück. Ist die Serververbindung nicht hergestellt, handelt es sich nicht um TCP oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fc_glitches: integer Gibt die Anzahl der auf der Frontend-Verbindung gezählten Protokollstörungen zurück. Dazu gehören üblicherweise Protokollverletzungen sowie kleine Anomalien, die auf einen fehlerhaften oder sich falsch verhaltenden Client hindeuten und Probleme in der Infrastruktur verursachen können. Beispiele sind übermäßig viele Fehler in den Protokollen oder zahlreiche vorzeitige Verbindungsabbrüche, die häufige TLS-Neuverhandlungen auslösen. Auch Anfragen, die zu groß für einen einzelnen Puffer sind, können solche Störungen verursachen und HTTP-400-Fehler erklären. Idealerweise sollte dieser Wert null bleiben; manche Browser können jedoch gelegentlich eine Störung auslösen, wenn sie die Grenzen des Protokolls ausreizen. Diese Werte sollten normalerweise nicht als alarmierend gelten, insbesondere kleine Werte. Ein plötzlicher Anstieg kann allerdings auf eine Anomalie hinweisen. Große Werte, etwa Hunderte bis Tausende pro Verbindung oder so viele wie Anfragen, können auf einen eigens entwickelten Client hindeuten, der den Protokoll-Stack identifizieren oder angreifen will. Nicht alle Protokoll-Multiplexer erfassen diese Kennzahl. Weitere Einzelheiten zu den Ereignissen lassen sich nur durch aktivierte Traces erhalten, die den gesamten Austausch erfassen.

fc_http_major: integer Meldet die HTTP-Hauptversionskodierung der Frontend-Verbindung: 1 für HTTP/0.9 bis HTTP/1.1 oder 2 für HTTP/2. Dies beruht auf der Kodierung auf der Leitung und nicht auf der im Anfrage-Header angegebenen Version.

fc_lost: integer Handelt es sich bei der Verbindung weder um TCP noch um QUIC, schlägt der Sample-Abruf fehl. Bei QUIC wird die Anzahl verlorener QUIC-Pakete der Client-Verbindung zurückgegeben. Bei TCP wird der vom Kernel für die Client-Verbindung gemessene lost-Zähler zurückgegeben. Ist die Serververbindung nicht hergestellt oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fc_nb_streams: integer Gibt die Anzahl der auf der Frontend-Verbindung geöffneten Streams zurück.

fc_pp_authority: string Gibt das erste vom Client im PROXY-Protokoll-Header gesendete Authority-TLV zurück, sofern vorhanden.

<a id="entry-7-3-3-fc-pp-tlv-string"></a>

**`fc_pp_tlv(<id>): string`**

```haproxy
fc_pp_tlv(<id>): string
```

Gibt den TLV-Wert für die angegebene TLV-ID zurück. Die ID muss entweder ein numerischer Wert zwischen 0 und 255 oder einer der folgenden unterstützten symbolischen Namen sein, die den Suffixen der TLV-Konstanten in der PPv2-Spezifikation entsprechen: "ALPN": PP2_TYPE_ALPN, "AUTHORITY": PP2_TYPE_AUTHORITY, "CRC32": PP2_TYPE_CRC32C, "NETNS": PP2_TYPE_NETNS, "NOOP: PP2_TYPE_NOOP", "SSL": PP2_TYPE_SSL, "SSL_CIPHER": PP2_SUBTYPE_SSL_CIPHER, "SSL_CN": PP2_SUBTYPE_SSL_CN, "SSL_KEY_ALG": PP2_SUBTYPE_SSL_KEY_ALG, "SSL_SIG_ALG": PP2_SUBTYPE_SSL_SIG_ALG, "SSL_VERSION": PP2_SUBTYPE_SSL_VERSION, "UNIQUE_ID": PP2_TYPE_UNIQUE_ID.

Der empfangene Wert darf höchstens 1024 Bytes groß sein. Dies dient der Verhinderung möglicher DoS-Angriffe. Werte mit höchstens 256 Bytes können aus einem Speicherpool zugewiesen werden. Begrenzen Sie daher für optimale Leistung die Länge gesendeter Werte möglichst auf 256 Bytes.

Anders als fc_pp_authority und fc_pp_unique_id kann fc_pp_tlv alle Vorkommen eines angeforderten TLV durchlaufen, falls TLV-IDs mehrfach vorhanden sind. Die Reihenfolge entspricht den Positionen im PROXY-Protokoll-Header. Auf Duplikate sollte man sich jedoch möglichst nicht verlassen, da TLVs üblicherweise als eindeutig vorausgesetzt werden. Doppelte TLV-IDs deuten im Allgemeinen auf einen Fehler auf der Senderseite des PROXY-Protokoll-Headers hin.

fc_pp_unique_id: string Gibt das erste vom Client im PROXY-Protokoll-Header gesendete Unique-ID-TLV zurück, sofern vorhanden.

fc_rcvd_proxy: boolean Gibt true zurück, wenn der Client die Verbindung mit einem PROXY-Protokoll-Header begonnen hat.

fc_reordering: integer Handelt es sich bei der Verbindung weder um TCP noch um QUIC, schlägt der Sample-Abruf fehl. Bei QUIC wird die Anzahl umgeordneter QUIC-Pakete der Client-Verbindung zurückgegeben. Bei TCP wird der vom Kernel für die Client-Verbindung gemessene reordering-Zähler zurückgegeben. Ist die Serververbindung nicht hergestellt oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fc_retrans: integer Gibt den vom Kernel für die Client-Verbindung gemessenen retransmits-Zähler zurück. Ist die Serververbindung nicht hergestellt, handelt es sich nicht um TCP oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

<a id="entry-7-3-3-fc-rtt-integer"></a>

**`fc_rtt(<unit>): integer`**

```haproxy
fc_rtt(<unit>): integer
```

Handelt es sich bei der Verbindung weder um TCP noch um QUIC, schlägt der Sample-Abruf fehl. Bei QUIC wird die geglättete Round Trip Time der Client-Verbindung zurückgegeben. Bei TCP wird die vom Kernel für die Client-Verbindung gemessene Round Trip Time (RTT) zurückgegeben. `<unit>` ist optional; die Standardeinheit ist Millisekunden. `<unit>` kann auf "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Serververbindung nicht hergestellt oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

<a id="entry-7-3-3-fc-rttvar-integer"></a>

**`fc_rttvar(<unit>): integer`**

```haproxy
fc_rttvar(<unit>): integer
```

Handelt es sich bei der Verbindung weder um TCP noch um QUIC, schlägt der Sample-Abruf fehl. Bei QUIC wird die Varianz der geglätteten Round Trip Time der Client-Verbindung zurückgegeben. Bei TCP wird die vom Kernel für die Client-Verbindung gemessene Varianz der Round Trip Time (RTT) zurückgegeben. `<unit>` ist optional; die Standardeinheit ist Millisekunden. `<unit>` kann auf "ms" für Millisekunden oder "us" für Mikrosekunden gesetzt werden. Ist die Serververbindung nicht hergestellt oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fc_sacked: integer Gibt den vom Kernel für die Client-Verbindung gemessenen sacked-Zähler zurück. Ist die Serververbindung nicht hergestellt, handelt es sich nicht um TCP oder unterstützt das Betriebssystem TCP_INFO nicht, beispielsweise bei Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fc_saved_syn: binary Gibt eine Kopie des gespeicherten SYN-Pakets zurück, das das System beim Aufbau der eingehenden Verbindung aufbewahrt hat. Dies erfordert die Option "tcp-ss" in der "bind"-Zeile sowie mindestens Linux-Kernel 4.3. Ist "tcp-ss" auf 1 gesetzt, sind nur die IP- und TCP-Header enthalten. Bei "tcp-ss" gleich 2 steht zusätzlich der Ethernet-Header vor dem IP-Header. Damit lassen sich beispielsweise die Quell-MAC-Adresse oder VLANs prüfen oder protokollieren. Es ist nicht garantiert, dass ein SYN gespeichert wird. Werden etwa SYN-Cookies verwendet, wird das SYN-Paket nicht aufbewahrt; die Verbindung wird stattdessen anhand des passenden ACK-Pakets hergestellt. Außerdem garantiert das System nicht, die Kopie über den ersten Lesezugriff hinaus aufzubewahren. Es wird daher dringend empfohlen, sie in einer Regel "tcp-request connection" in eine Variable im Gültigkeitsbereich "sess" zu kopieren und für weitere Verarbeitung ausschließlich diese Variable zu verwenden. Auf der Loopback-Schnittstelle erzeugt das System einen künstlichen Ethernet-Header mit 14 Bytes, in dem Quell- und Zieladresse null sind und nur das Protokoll gesetzt ist. Zur Fehlersuche ist es praktisch, solche Samples mit dem Konverter "hex" in die hexadezimale Darstellung umzuwandeln. Beispiel (Felder unten manuell getrennt und kommentiert):

```shell
frontend test
    mode http
    bind :::4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain \
                 lf-string "%[var(sess.syn),hex]\n"

$ curl '0:4445'
000000000000 000000000000 0800 \  # MAC_DST MAC_SRC PROTO=IPv4
4500003C0A65400040063255       \  # IPv4 header, proto=6 (TCP)
7F000001 7F000001              \  # IP_SRC=127.0.0.1 IP_DST=127.0.0.1
E1F2 115D 01AF4E3E 00000000    \  # TCP_SPORT=57842 TCP_DPORT=4445, SEQ
A0 02 FFD7 FE300000            \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65495
0204FFD70402080A01C2A71A0000000001030307 # MSS=65495, TS, SACK, WSCALE 7

$ curl '[::1]:4445'
000000000000 000000000000 86DD   \ # MAC_DST MAC_SRC PROTO=IPv6
6008018F00280640                 \ # IPv6 header, proto=6 (TCP)
00000000000000000000000000000001 \ # SRC=::1
00000000000000000000000000000001 \ # DST=::1
9758 115D B5511F5D 00000000      \ # TCP_SPORT=38744 TCP_DPORT=4445, SEQ
A0 02 FFC4 00300000              \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65476
0204FFC40402080A9C231D680000000001030307 # MSS=65476, TS, SACK, WSCALE 7
```

Der Konverter "bytes()" hilft beim Extrahieren bestimmter Felder aus dem Paket. Mit be2dec() lassen sich auch Abschnitte lesen und als Ganzzahlen ausgeben. Für eine genauere Extraktion siehe die Konverter "eth.XXX".

Beispiel mit IPv4-Eingabe:

```shell
frontend test
    mode http
    bind :4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain lf-string \
                 "mac_dst=%[var(sess.syn),eth.dst,hex] \
                  mac_src=%[var(sess.syn),eth.src,hex] \
                  proto=%[var(sess.syn),eth.proto,bytes(6),be2hex(,2)] \
                  ipv4h=%[var(sess.syn),eth.data,bytes(0,12),hex] \
                  ipv4_src=%[var(sess.syn),eth.data,ip.src] \
                  ipv4_dst=%[var(sess.syn),eth.data,ip.dst] \
                  tcp_spt=%[var(sess.syn),eth.data,ip.data,tcp.src] \
                  tcp_dpt=%[var(sess.syn),eth.data,ip.data,tcp.dst] \
                  tcp_win=%[var(sess.syn),eth.data,ip.data,tcp.win] \
                  tcp_opt=%[var(sess.syn),eth.data,ip.data,bytes(20),hex]\n"

$ curl '0:4445'
mac_dst=000000000000 mac_src=000000000000 proto=0800 \
ipv4h=4500003CC9B7400040067302 ipv4_src=127.0.0.1 ipv4_dst=127.0.0.1 \
tcp_spt=43970 tcp_dpt=4445 tcp_win=65495 \
tcp_opt=0204FFD70402080A01DC0D410000000001030307
```

Siehe auch die "set-var"-Aktion, die "be2dec", "bytes", "hex", "eth.XXX", "ip.XXX" und "tcp.XXX"-Konverter.

fc_settings_streams_limit: integer Gibt die maximale Anzahl von Streams zurück, die auf der Frontend-Verbindung zulässig sind. Bei TCP- und HTTP/1.1-Verbindungen ist dieser Wert stets 1. Bei anderen Protokollen hängt er von den mit dem Client vereinbarten Einstellungen ab.

fc_src: ip Dies ist die ursprüngliche Quell-IP-Adresse der Verbindung auf der Client-Seite. Nur Regeln vom Typ "tcp-request connection" können diese Adresse ändern. Weitere Details siehe "src".

fc_src_is_local: boolean Gibt true zurück, wenn die Quelladresse der eingehenden Verbindung lokal zum System ist, oder false, wenn die Adresse nicht auf dem System existiert. Weitere Details siehe "src_is_local".

fc_src_port: integer Gibt einen Ganzzahlwert zurück, der dem TCP-Quellport der Verbindung auf der Client-Seite entspricht. Nur Regeln vom Typ "tcp-request connection" können diese Adresse ändern. Weitere Details siehe "src-port".

fc_unacked: integer Gibt den vom Kernel für die Client-Verbindung gemessenen unacked-Zähler zurück. Wenn die Server-Verbindung nicht hergestellt ist, wenn die Verbindung kein TCP ist oder wenn das Betriebssystem TCP_INFO nicht unterstützt, beispielsweise Linux-Kernels vor 2.4, schlägt der Sample-Abruf fehl.

fe_client_timeout: integer Gibt den Konfigurationswert in Millisekunden für die Zeitüberschreitung für den Client des aktuellen Frontends zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden.

fe_defbe: string Gibt eine Zeichenkette zurück, die den Namen des Standard-Backends des Frontends enthält. Sie kann in Frontends verwendet werden, um zu überprüfen, welches Backend Anfragen standardmäßig behandelt.

fe_id: integer Gibt einen Ganzzahlwert zurück, der die ID des aktuellen Frontends enthält. Er kann in Backends verwendet werden, um zu überprüfen, von welchem Frontend aus aufgerufen wurde, oder um alle Benutzer, die über dasselbe Frontend kommen, an denselben Server zu binden.

fe_name: string Gibt eine Zeichenkette zurück, die den Namen des aktuellen Frontends enthält. Sie kann in Backends verwendet werden, um zu überprüfen, von welchem Frontend aus aufgerufen wurde, oder um alle Benutzer, die über dasselbe Frontend kommen, an denselben Server zu binden.

fe_tarpit_timeout: integer Gibt den Konfigurationswert in Millisekunden für die Zeitüberschreitung für die Tarpit des aktuellen Frontends zurück. Diese Zeitüberschreitung kann durch eine Regel "set-timeout" überschrieben werden.

req.bytes_in: integer Gibt die Anzahl der vom Client empfangenen Bytes zurück. Der Wert entspricht dem, was von HAProxy empfangen wurde, einschließlich einiger Header und eines gewissen internen Kodierungsaufwands. Anfragekompression beeinflusst den hier gemeldeten Wert nicht.

req.bytes_out: integer Gibt die Anzahl der an den Server gesendeten Bytes zurück. Der Wert entspricht dem, was von HAProxy gesendet wurde, einschließlich einiger Header und eines gewissen internen Kodierungsaufwands. Anfragekompression beeinflusst den hier gemeldeten Wert.

res.bytes_in: integer Gibt die Anzahl der vom Server empfangenen Bytes zurück. Der Wert entspricht dem, was von HAProxy empfangen wurde, einschließlich einiger Header und eines gewissen internen Kodierungsaufwands. Antwortkompression beeinflusst den hier gemeldeten Wert nicht.

res.bytes_out: integer Gibt die Anzahl der an den Client gesendeten Bytes zurück. Der Wert entspricht dem, was von HAProxy gesendet wurde, einschließlich einiger Header und eines gewissen internen Kodierungsaufwands. Antwortkompression beeinflusst den hier gemeldeten Wert.

res.timer.data: integer Gibt die gesamte Übertragungszeit der Antwortnutzlast bis zum Senden des letzten Bytes an den Client zurück. Bei HTTP beginnt dies nach dem letzten Antwort-Header (nach Tr). Dies entspricht %Td im Log-Format und wird in Millisekunden (ms) angegeben. Weitere Informationen siehe [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“

<a id="entry-7-3-3-sc-bytes-in-rate-integer"></a>

**`sc_bytes_in_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_in_rate(<ctr>[,<table>]): integer
sc0_bytes_in_rate([<table>]): integer
sc1_bytes_in_rate([<table>]): integer
sc2_bytes_in_rate([<table>]): integer
```

Gibt die durchschnittliche Byterate vom Client zum Server aus den aktuell verfolgten Zählern zurück, gemessen in Bytes über den in der Tabelle konfigurierten Zeitraum. Siehe auch "table_bytes_in_rate".

<a id="entry-7-3-3-sc-bytes-out-rate-integer"></a>

**`sc_bytes_out_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_out_rate(<ctr>[,<table>]): integer
sc0_bytes_out_rate([<table>]): integer
sc1_bytes_out_rate([<table>]): integer
sc2_bytes_out_rate([<table>]): integer
```

Gibt die durchschnittliche Byterate vom Server zum Client aus den aktuell verfolgten Zählern zurück, gemessen in Bytes über den in der Tabelle konfigurierten Zeitraum. Siehe auch "table_bytes_out_rate".

<a id="entry-7-3-3-sc-clr-gpc-integer"></a>

**`sc_clr_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc(<idx>,<ctr>[,<table>]): integer
```

Setzt den Allzweckzähler am Index `<idx>` des Arrays zurück, das dem angegebenen verfolgten Zähler mit der ID `<ctr>` in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table `<table>` zugeordnet ist, und gibt seinen vorherigen Wert zurück. `<idx>` ist eine Ganzzahl zwischen 0 und 99 und `<ctr>` eine Ganzzahl zwischen 0 und 2. Vor dem ersten Aufruf ist der gespeicherte Wert null; der erste Aufruf gibt daher stets null zurück. Dieser Abruf gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'.

<a id="entry-7-3-3-sc-clr-gpc0-integer"></a>

**`sc_clr_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc0(<ctr>[,<table>]): integer
sc0_clr_gpc0([<table>]): integer
sc1_clr_gpc0([<table>]): integer
sc2_clr_gpc0([<table>]): integer
```

Setzt den ersten Allzweckzähler zurück, der den aktuell verfolgten Zählern zugeordnet ist, und gibt seinen vorherigen Wert zurück. Vor der ersten Ausführung ist der gespeicherte Wert null, sodass die erste Ausführung stets null zurückgibt. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf:

Beispiel:

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 5
acl save  sc0_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-clr-gpc1-integer"></a>

**`sc_clr_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc1(<ctr>[,<table>]): integer
sc0_clr_gpc1([<table>]): integer
sc1_clr_gpc1([<table>]): integer
sc2_clr_gpc1([<table>]): integer
```

Setzt den zweiten Allzweckzähler zurück, der den aktuell verfolgten Zählern zugeordnet ist, und gibt seinen vorherigen Wert zurück. Vor der ersten Ausführung ist der gespeicherte Wert null, sodass die erste Ausführung stets null zurückgibt. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf.

<a id="entry-7-3-3-sc-conn-cnt-integer"></a>

**`sc_conn_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cnt(<ctr>[,<table>]): integer
sc0_conn_cnt([<table>]): integer
sc1_conn_cnt([<table>]): integer
sc2_conn_cnt([<table>]): integer
```

Gibt die kumulierte Anzahl eingehender Verbindungen aus den derzeit verfolgten Zählern zurück. Siehe auch
"table_conn_cnt".

<a id="entry-7-3-3-sc-conn-cur-integer"></a>

**`sc_conn_cur(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cur(<ctr>[,<table>]): integer
sc0_conn_cur([<table>]): integer
sc1_conn_cur([<table>]): integer
sc2_conn_cur([<table>]): integer
```

Gibt die aktuelle Anzahl gleichzeitiger Verbindungen zurück, die die gleichen verfolgten Zähler verfolgen. Diese Zahl wird automatisch erhöht, wenn die Verfolgung beginnt, und verringert, wenn die Verfolgung beendet wird. Siehe auch
"table_conn_cur".

<a id="entry-7-3-3-sc-conn-rate-integer"></a>

**`sc_conn_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_rate(<ctr>[,<table>]): integer
sc0_conn_rate([<table>]): integer
sc1_conn_rate([<table>]): integer
sc2_conn_rate([<table>]): integer
```

Gibt die durchschnittliche Verbindungsrate aus den derzeit verfolgten Zählern zurück, gemessen in Anzahl von Verbindungen über den in der Tabelle konfigurierten Zeitraum. Siehe auch "table_conn_rate".

<a id="entry-7-3-3-sc-get-gpc-integer"></a>

**`sc_get_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc(<idx>,<ctr>[,<table>]): integer
```

Gibt den Wert des Allzweckzählers am Index `<idx>` im GPC-Array zurück, das dem derzeit verfolgten Zähler mit der ID `<ctr>` in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table `<table>` zugeordnet ist. `<idx>` ist eine Ganzzahl zwischen 0 und 99 und `<ctr>` eine Ganzzahl zwischen 0 und 2. Ist an diesem Index kein gpc gespeichert, wird null zurückgegeben. Dieser Abruf gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'. Siehe auch "table_gpc" und "sc_inc_gpc".

<a id="entry-7-3-3-sc-get-gpc0-integer"></a>

**`sc_get_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc0(<ctr>[,<table>]): integer
sc0_get_gpc0([<table>]): integer
sc1_get_gpc0([<table>]): integer
sc2_get_gpc0([<table>]): integer
```

Gibt den Wert des ersten Allzweckzählers zurück, der den derzeit verfolgten Zählern zugeordnet ist. Siehe auch "table_gpc0" und sc/sc0/sc1/sc2_inc_gpc0.

<a id="entry-7-3-3-sc-get-gpc1-integer"></a>

**`sc_get_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc1(<ctr>[,<table>]): integer
sc0_get_gpc1([<table>]): integer
sc1_get_gpc1([<table>]): integer
sc2_get_gpc1([<table>]): integer
```

Gibt den Wert des zweiten Allzweckzählers zurück, der den derzeit verfolgten Zählern zugeordnet ist. Siehe auch "table_gpc1" und sc/sc0/sc1/sc2_inc_gpc1.

<a id="entry-7-3-3-sc-get-gpt-integer"></a>

**`sc_get_gpt(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt(<idx>,<ctr>[,<table>]): integer
```

Gibt den Wert des ersten Allzweck-Tags am Index `<idx>` des Arrays zurück, das dem verfolgten Zähler mit der ID `<ctr>` in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table `<table>` zugeordnet ist. `<idx>` ist eine Ganzzahl zwischen 0 und 99 und `<ctr>` eine Ganzzahl zwischen 0 und
2. Ist an diesem Index kein GPT gespeichert, wird null zurückgegeben. Dieser Abruf gilt nur für den Array-data_type 'gpt', nicht für den älteren data-type 'gpt0'. Siehe auch "table_gpt".

<a id="entry-7-3-3-sc-get-gpt0-integer"></a>

**`sc_get_gpt0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt0(<ctr>[,<table>]): integer
sc0_get_gpt0([<table>]): integer
sc1_get_gpt0([<table>]): integer
sc2_get_gpt0([<table>]): integer
```

Gibt den Wert des ersten Allzweck-Tags zurück, der den derzeit verfolgten Zählern zugeordnet ist. Siehe auch "table_gpt0".

<a id="entry-7-3-3-sc-glitch-cnt-integer"></a>

**`sc_glitch_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_cnt(<ctr>[,<table>]): integer
sc0_glitch_cnt([<table>]): integer
sc1_glitch_cnt([<table>]): integer
sc2_glitch_cnt([<table>]): integer
```

Gibt die kumulierte Anzahl an Störungen der Frontend-Verbindung zurück, die bei Verbindungen beobachtet wurden, die den derzeit verfolgten Zählern zugeordnet sind. Diese Störungen führen in der Regel dazu, dass Anfragen oder Verbindungen abgebrochen werden, sodass der zurückgegebene Wert oft auf vergangene Verbindungen verweist. Es gibt keinen guten oder schlechten Wert, doch ein fehleranfälliger Client kann gelegentlich einige Störungen pro Verbindung verursachen, während ein sehr fehlerhafter oder böswilliger Client schnell Tausende Ereignisse pro Verbindung verursachen kann. Siehe auch fc_glitches für die Anzahl, die die aktuelle Verbindung betrifft, src_glitch_cnt zum Nachschlagen pro Quelle und sc_glitch_rate für die Ereignisratenmessung.

<a id="entry-7-3-3-sc-glitch-rate-integer"></a>

**`sc_glitch_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_rate(<ctr>[,<table>]): integer
sc0_glitch_rate([<table>]): integer
sc1_glitch_rate([<table>]): integer
sc2_glitch_rate([<table>]): integer
```

Gibt die durchschnittliche Rate zurück, mit der Störungen der Frontend-Verbindung für die derzeit verfolgten Zähler beobachtet wurden, gemessen in Anzahl von Ereignissen über den in der Tabelle konfigurierten Zeitraum. Diese Störungen führen in der Regel dazu, dass Anfragen oder Verbindungen abgebrochen werden, sodass der zurückgegebene Wert oft mit vergangenen Verbindungen verknüpft ist. Es gibt keinen guten oder schlechten Wert, doch ein fehleranfälliger Client kann gelegentlich einige Störungen pro Verbindung verursachen, weshalb eine niedrige Rate im Allgemeinen erwartet wird. Ein sehr fehlerhafter oder böswilliger Client kann jedoch schnell Tausende Ereignisse pro Verbindung verursachen und eine hohe Rate aufrechterhalten. Siehe auch "table_glitch_rate" und "sc_glitch_cnt".

<a id="entry-7-3-3-sc-gpc-rate-integer"></a>

**`sc_gpc_rate(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_gpc_rate(<idx>,<ctr>[,<table>]): integer
```

Gibt die durchschnittliche Inkrementrate des Allzweckzählers am Index `<idx>` des Arrays zurück, das dem verfolgten Zähler mit der ID `<ctr>` in der Tabelle des aktuellen Proxys oder in der angegebenen Stick Table `<table>` zugeordnet ist. Gibt die Häufigkeit an, mit der der Zähler gpc über den konfigurierten Zeitraum erhöht wurde. `<idx>` ist eine Ganzzahl zwischen 0 und 99 und `<ctr>` eine Ganzzahl zwischen 0 und 2. Das Zählerarray 'gpc_rate' muss in der Stick Table gespeichert sein, damit ein Wert zurückgegeben wird, da 'gpc' nur die Ereignisanzahl enthält. Dieser Abruf gilt nur für den Array-data_type 'gpc_rate', nicht für die älteren data_types 'gpc0_rate' oder 'gpc1_rate'. Siehe auch "table_gpc_rate", "sc_get_gpc" und "sc_inc_gpc".

<a id="entry-7-3-3-sc-gpc0-rate-integer"></a>

**`sc_gpc0_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc0_rate(<ctr>[,<table>]): integer
sc0_gpc0_rate([<table>]): integer
sc1_gpc0_rate([<table>]): integer
sc2_gpc0_rate([<table>]): integer
```

Gibt die durchschnittliche Inkrementrate des ersten Allzweckzählers zurück, der den derzeit verfolgten Zählern zugeordnet ist. Es wird die Häufigkeit zurückgegeben, mit der der Zähler gpc0 im konfigurierten Zeitraum inkrementiert wurde. Siehe auch src_gpc0_rate, sc/sc0/sc1/sc2_get_gpc0, und sc/sc0/sc1/sc2_inc_gpc0.
Beachten Sie, dass der Zähler "gpc0_rate" in der Stick Table gespeichert sein muss, damit ein Wert zurückgegeben wird, da "gpc0" nur die Ereignisanzahl speichert.

<a id="entry-7-3-3-sc-gpc1-rate-integer"></a>

**`sc_gpc1_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc1_rate(<ctr>[,<table>]): integer
sc0_gpc1_rate([<table>]): integer
sc1_gpc1_rate([<table>]): integer
sc2_gpc1_rate([<table>]): integer
```

Gibt die durchschnittliche Inkrementrate des zweiten Allzweckzählers zurück, der den derzeit verfolgten Zählern zugeordnet ist. Es wird die Häufigkeit zurückgegeben, mit der der Zähler gpc1 im konfigurierten Zeitraum inkrementiert wurde. Siehe auch src_gpc1_rate, sc/sc0/sc1/sc2_get_gpc1, und sc/sc0/sc1/sc2_inc_gpc1.
Beachten Sie, dass der Zähler "gpc1_rate" in der Stick Table gespeichert sein muss, damit ein Wert zurückgegeben wird, da "gpc1" nur die Ereignisanzahl speichert.

<a id="entry-7-3-3-sc-http-err-cnt-integer"></a>

**`sc_http_err_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_cnt(<ctr>[,<table>]): integer
sc0_http_err_cnt([<table>]): integer
sc1_http_err_cnt([<table>]): integer
sc2_http_err_cnt([<table>]): integer
```

Gibt die kumulierte Anzahl von HTTP-Fehlern aus den derzeit verfolgten Zählern zurück. Dazu gehören sowohl Anfragefehler als auch 4xx-Fehlerantworten. Siehe auch "table_http_err_cnt".

<a id="entry-7-3-3-sc-http-err-rate-integer"></a>

**`sc_http_err_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_rate(<ctr>[,<table>]): integer
sc0_http_err_rate([<table>]): integer
sc1_http_err_rate([<table>]): integer
sc2_http_err_rate([<table>]): integer
```

Gibt die durchschnittliche Rate von HTTP-Fehlern aus den aktuell verfolgten Zählern zurück, gemessen als Anzahl von Fehlern über den in der Tabelle konfigurierten Zeitraum. Dazu zählen sowohl Anfragefehler als auch 4xx-Fehlerantworten. Siehe auch src_http_err_rate.

<a id="entry-7-3-3-sc-http-fail-cnt-integer"></a>

**`sc_http_fail_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_cnt(<ctr>[,<table>]): integer
sc0_http_fail_cnt([<table>]): integer
sc1_http_fail_cnt([<table>]): integer
sc2_http_fail_cnt([<table>]): integer
```

Gibt die kumulierte Anzahl fehlgeschlagener HTTP-Antworten aus den aktuell verfolgten Zählern zurück. Dazu zählen sowohl Antwortfehler als auch 5xx-Statuscodes, die nicht 501 oder 505 sind. Siehe auch "table_http_fail_cnt".

<a id="entry-7-3-3-sc-http-fail-rate-integer"></a>

**`sc_http_fail_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_rate(<ctr>[,<table>]): integer
sc0_http_fail_rate([<table>]): integer
sc1_http_fail_rate([<table>]): integer
sc2_http_fail_rate([<table>]): integer
```

Gibt die durchschnittliche Rate fehlgeschlagener HTTP-Antworten aus den aktuell verfolgten Zählern zurück, gemessen als Anzahl von Fehlern über den in der Tabelle konfigurierten Zeitraum. Dazu zählen sowohl Antwortfehler als auch 5xx-Statuscodes, die nicht 501 oder 505 sind. Siehe auch "table_http_fail_rate".

<a id="entry-7-3-3-sc-http-req-cnt-integer"></a>

**`sc_http_req_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_cnt(<ctr>[,<table>]): integer
sc0_http_req_cnt([<table>]): integer
sc1_http_req_cnt([<table>]): integer
sc2_http_req_cnt([<table>]): integer
```

Gibt die kumulierte Anzahl von HTTP-Anfragen aus den aktuell verfolgten Zählern zurück. Dazu zählen alle gestarteten Anfragen, unabhängig davon, ob sie gültig waren. Siehe auch src_http_req_cnt.

<a id="entry-7-3-3-sc-http-req-rate-integer"></a>

**`sc_http_req_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_rate(<ctr>[,<table>]): integer
sc0_http_req_rate([<table>]): integer
sc1_http_req_rate([<table>]): integer
sc2_http_req_rate([<table>]): integer
```

Gibt die durchschnittliche Rate von HTTP-Anfragen aus den aktuell verfolgten Zählern zurück, gemessen als Anzahl von Anfragen über den in der Tabelle konfigurierten Zeitraum. Dazu zählen alle gestarteten Anfragen, unabhängig davon, ob sie gültig waren. Siehe auch src_http_req_rate.

<a id="entry-7-3-3-sc-inc-gpc-integer"></a>

**`sc_inc_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc(<idx>,<ctr>[,<table>]): integer
```

Erhöht den Allzweckzähler am Index `<idx>` des Arrays, das dem angegebenen verfolgten Zähler mit der ID `<ctr>` aus der Stick Table des aktuellen Proxys oder aus der angegebenen Stick Table `<table>` zugeordnet ist, und gibt seinen neuen Wert zurück. `<idx>` ist eine Ganzzahl zwischen 0 und 99 und `<ctr>` eine Ganzzahl zwischen 0 und 2. Vor dem ersten Aufruf ist der gespeicherte Wert null; der erste Aufruf erhöht ihn daher auf 1 und gibt 1 zurück. Dieser Abruf gilt nur für den Array-data_type 'gpc', nicht für die älteren data_types 'gpc0' oder 'gpc1'.

<a id="entry-7-3-3-sc-inc-gpc0-integer"></a>

**`sc_inc_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc0(<ctr>[,<table>]): integer
sc0_inc_gpc0([<table>]): integer
sc1_inc_gpc0([<table>]): integer
sc2_inc_gpc0([<table>]): integer
```

Erhöht den ersten Allzweckzähler, der den aktuell verfolgten Zählern zugeordnet ist, und gibt seinen neuen Wert zurück. Vor dem ersten Aufruf ist der gespeicherte Wert null; der erste Aufruf erhöht ihn daher auf 1 und gibt 1 zurück. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf:

Beispiel:

```text
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-inc-gpc1-integer"></a>

**`sc_inc_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc1(<ctr>[,<table>]): integer
sc0_inc_gpc1([<table>]): integer
sc1_inc_gpc1([<table>]): integer
sc2_inc_gpc1([<table>]): integer
```

Erhöht den zweiten Allzweckzähler, der den aktuell verfolgten Zählern zugeordnet ist, und gibt seinen neuen Wert zurück. Vor dem ersten Aufruf ist der gespeicherte Wert null; der erste Aufruf erhöht ihn daher auf 1 und gibt 1 zurück. Dies wird typischerweise als zweite ACL in einem Ausdruck verwendet, um eine Verbindung zu markieren, wenn eine erste ACL zutraf.

<a id="entry-7-3-3-sc-kbytes-in-integer"></a>

**`sc_kbytes_in(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_in(<ctr>[,<table>]): integer
sc0_kbytes_in([<table>]): integer
sc1_kbytes_in([<table>]): integer
sc2_kbytes_in([<table>]): integer
```

Gibt die Gesamtmenge an Client-zu-Server-Daten aus den aktuell verfolgten Zählern zurück, gemessen in Kilobyte. Der Test wird derzeit auf 32-Bit-Ganzzahlen durchgeführt, was Werte auf 4 Terabyte begrenzt. Siehe auch "table_kbytes_in".

<a id="entry-7-3-3-sc-kbytes-out-integer"></a>

**`sc_kbytes_out(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_out(<ctr>[,<table>]): integer
sc0_kbytes_out([<table>]): integer
sc1_kbytes_out([<table>]): integer
sc2_kbytes_out([<table>]): integer
```

Gibt die Gesamtmenge an Server-zu-Client-Daten aus den aktuell verfolgten Zählern zurück, gemessen in Kilobyte. Der Test wird derzeit auf 32-Bit-Ganzzahlen durchgeführt, was Werte auf 4 Terabyte begrenzt. Siehe auch "table_kbytes_out".

sc_key(`<ctr>`): any sc0_key: any sc1_key: any sc2_key: any Gibt den Schlüssel zurück, der zum Musterabgleich des aktuell verfolgten Zählers verwendet wird.

<a id="entry-7-3-3-sc-sess-cnt-integer"></a>

**`sc_sess_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_cnt(<ctr>[,<table>]): integer
sc0_sess_cnt([<table>]): integer
sc1_sess_cnt([<table>]): integer
sc2_sess_cnt([<table>]): integer
```

Gibt aus den aktuell verfolgten Zählern die kumulierte Anzahl eingehender Verbindungen zurück, die in Sitzungen umgewandelt wurden, also von einer Regel "tcp-request connection" akzeptiert wurden. Ein Backend kann mehr Sitzungen als Verbindungen zählen, da jede Verbindung bei Verwendung von HTTP-Keep-Alive auf der Verbindung zum Client zu mehreren Backend-Sitzungen führen kann. Siehe auch "table_sess_cnt".

<a id="entry-7-3-3-sc-sess-rate-integer"></a>

**`sc_sess_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_rate(<ctr>[,<table>]): integer
sc0_sess_rate([<table>]): integer
sc1_sess_rate([<table>]): integer
sc2_sess_rate([<table>]): integer
```

Gibt die durchschnittliche Sitzungsrate aus den aktuell verfolgten Zählern zurück, gemessen als Anzahl von Sitzungen über den in der Tabelle konfigurierten Zeitraum. Eine Sitzung ist eine Verbindung, die die frühen "tcp-request connection"-Regeln erfolgreich überstanden hat. Ein Backend kann mehr Sitzungen als Verbindungen zählen, da jede Verbindung bei Verwendung von HTTP-Keep-Alive auf der Verbindung zum Client mehrere Backend-Sitzungen erzeugen kann. Siehe auch "table_sess_rate".

<a id="entry-7-3-3-sc-tracked-boolean"></a>

**`sc_tracked(<ctr>[,<table>]): boolean`**

```haproxy
sc_tracked(<ctr>[,<table>]): boolean
sc0_tracked([<table>]): boolean
sc1_tracked([<table>]): boolean
sc2_tracked([<table>]): boolean
```

Gibt true zurück, wenn der angegebene Sitzungszähler derzeit von der aktuellen Sitzung verfolgt wird. Dies kann nützlich sein, um zu entscheiden, ob bestimmte Werte in einem Header, der an den Server übergeben wird, gesetzt werden sollen.

<a id="entry-7-3-3-sc-trackers-integer"></a>

**`sc_trackers(<ctr>[,<table>]): integer`**

```haproxy
sc_trackers(<ctr>[,<table>]): integer
sc0_trackers([<table>]): integer
sc1_trackers([<table>]): integer
sc2_trackers([<table>]): integer
```

Gibt die aktuelle Anzahl gleichzeitiger Verbindungen zurück, die dieselben Zähler verfolgen. Diese Anzahl wird beim Beginn des Trackings automatisch erhöht und beim Ende verringert. Anders als sc0_conn_cur beruht dies nicht auf gespeicherten Informationen, sondern auf dem Referenzzähler der Tabelle (dem Wert "use", den "show table" auf der CLI zurückgibt). Dies kann für das Tracking auf layer7 manchmal besser geeignet sein. So lässt sich einem Server beispielsweise mitteilen, wie viele gleichzeitige Verbindungen von einer bestimmten Adresse bestehen.

so_id: integer Gibt eine Ganzzahl mit der ID des aktuellen lauschenden Sockets zurück. Dies ist in Frontends mit vielen "bind"-Zeilen nützlich oder um alle Benutzer, die über denselben Socket kommen, an denselben Server zu binden.

so_name: string Gibt eine Zeichenkette mit dem Namen des aktuellen lauschenden Sockets zurück, wie er mit name in einer "bind"-Zeile definiert ist. Dies kann denselben Zwecken wie so_id dienen, verwendet aber Zeichenketten statt Ganzzahlen.

src: ip Die Quell-IP-Adresse des Clients der Sitzung. Beliebige tcp/http-Regeln können diese Adresse ändern. Sie hat den Typ IP und funktioniert sowohl mit IPv4- als auch mit IPv6-Tabellen. In IPv6-Tabellen werden IPv4-Adressen gemäß RFC 4291 auf ihre IPv6-Entsprechung abgebildet. Verwendet wird die Quelladresse auf TCP-Ebene und nicht die Adresse eines Clients hinter einem Proxy. Wird jedoch die bind-Direktive "accept-proxy" oder "accept-netscaler-cip" verwendet, kann dies die Adresse eines Clients hinter einer anderen mit dem PROXY-Protokoll kompatiblen Komponente sein. Dies gilt für alle Regelsätze außer "tcp-request connection", der die tatsächliche Adresse sieht. Hat die eingehende Verbindung eine Adressübersetzung oder Umleitung mit Verbindungsverfolgung durchlaufen, wird die ursprüngliche Zieladresse vor der Umleitung gemeldet. Auf Linux-Systemen können Quelle und Ziel in seltenen Fällen vertauscht erscheinen, wenn der sysctl-Wert nf_conntrack_tcp_loose gesetzt ist: Eine verspätete Antwort kann eine abgelaufene Verbindung erneut öffnen und dabei vertauschen, was als Quelle und Ziel angesehen wird.

Beispiel:

```shell
# add an HTTP header in requests with the originating address' country
http-request set-header X-Country %[src,map_ip(geoip.lst)]
```

<a id="entry-7-3-3-src-bytes-in-rate-integer"></a>

**`src_bytes_in_rate([<table>]): integer`**

```haproxy
src_bytes_in_rate([<table>]): integer
```

Entspricht dem Konverter "table_bytes_in_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_bytes_in_rate([`<table>`])

<a id="entry-7-3-3-src-bytes-out-rate-integer"></a>

**`src_bytes_out_rate([<table>]): integer`**

```haproxy
src_bytes_out_rate([<table>]): integer
```

Entspricht dem Konverter "table_bytes_out_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_bytes_out_rate([`<table>`])

<a id="entry-7-3-3-src-clr-gpc-integer"></a>

**`src_clr_gpc(<idx>[,<table>]): integer`**

```haproxy
src_clr_gpc(<idx>[,<table>]): integer
```

Entspricht dem Konverter "table_clr_gpc", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_clr_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-clr-gpc0-integer"></a>

**`src_clr_gpc0([<table>]): integer`**

```haproxy
src_clr_gpc0([<table>]): integer
```

Entspricht dem Konverter "table_clr_gpc0", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_clr_gpc0([`<table>`])

<a id="entry-7-3-3-src-clr-gpc1-integer"></a>

**`src_clr_gpc1([<table>]): integer`**

```haproxy
src_clr_gpc1([<table>]): integer
```

Entspricht dem Konverter "table_clr_gpc1", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_clr_gpc1([`<table>`])

<a id="entry-7-3-3-src-conn-cnt-integer"></a>

**`src_conn_cnt([<table>]): integer`**

```haproxy
src_conn_cnt([<table>]): integer
```

Entspricht dem Konverter "table_conn_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_conn_cnt([`<table>`])

<a id="entry-7-3-3-src-conn-cur-integer"></a>

**`src_conn_cur([<table>]): integer`**

```haproxy
src_conn_cur([<table>]): integer
```

Entspricht dem Konverter "table_conn_cur", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_conn_cur([`<table>`])

<a id="entry-7-3-3-src-conn-rate-integer"></a>

**`src_conn_rate([<table>]): integer`**

```haproxy
src_conn_rate([<table>]): integer
```

Entspricht dem Konverter "table_conn_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_conn_rate([`<table>`])

<a id="entry-7-3-3-src-get-gpc-integer"></a>

**`src_get_gpc(<idx>[,<table>]): integer`**

```haproxy
src_get_gpc(<idx>[,<table>]): integer
```

Entspricht dem Konverter "table_gpc", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpc0-integer"></a>

**`src_get_gpc0([<table>]): integer`**

```haproxy
src_get_gpc0([<table>]): integer
```

Entspricht dem Konverter "table_gpc0", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc0([`<table>`])

<a id="entry-7-3-3-src-get-gpc1-integer"></a>

**`src_get_gpc1([<table>]): integer`**

```haproxy
src_get_gpc1([<table>]): integer
```

Entspricht dem Konverter "table_gpc1", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc1([`<table>`])

<a id="entry-7-3-3-src-get-gpt-integer"></a>

**`src_get_gpt(<idx>[,<table>]): integer`**

```haproxy
src_get_gpt(<idx>[,<table>]): integer
```

Entspricht dem Konverter "table_gpt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpt(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpt0-integer"></a>

**`src_get_gpt0([<table>]): integer`**

```haproxy
src_get_gpt0([<table>]): integer
```

Entspricht dem Konverter "table_gpt0", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpt0([`<table>`])

<a id="entry-7-3-3-src-glitch-cnt-integer"></a>

**`src_glitch_cnt([<table>]): integer`**

```haproxy
src_glitch_cnt([<table>]): integer
```

Entspricht dem Konverter "table_glitch_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_glitch_cnt([`<table>`])

<a id="entry-7-3-3-src-glitch-rate-integer"></a>

**`src_glitch_rate([<table>]): integer`**

```haproxy
src_glitch_rate([<table>]): integer
```

Entspricht dem Konverter "table_glitch_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_glitch_rate([`<table>`])

<a id="entry-7-3-3-src-gpc-rate-integer"></a>

**`src_gpc_rate(<idx>[,<table>]): integer`**

```haproxy
src_gpc_rate(<idx>[,<table>]): integer
```

Entspricht dem Konverter "table_gpc_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc_rate(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-gpc0-rate-integer"></a>

**`src_gpc0_rate([<table>]): integer`**

```haproxy
src_gpc0_rate([<table>]): integer
```

Entspricht dem Konverter "table_gpc0_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc0_rate([`<table>`])

<a id="entry-7-3-3-src-gpc1-rate-integer"></a>

**`src_gpc1_rate([<table>]): integer`**

```haproxy
src_gpc1_rate([<table>]): integer
```

Entspricht dem Konverter "table_gpc1_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_gpc1_rate([`<table>`])

<a id="entry-7-3-3-src-http-err-cnt-integer"></a>

**`src_http_err_cnt([<table>]): integer`**

```haproxy
src_http_err_cnt([<table>]): integer
```

Entspricht dem Konverter "table_http_err_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_err_cnt([`<table>`])

<a id="entry-7-3-3-src-http-err-rate-integer"></a>

**`src_http_err_rate([<table>]): integer`**

```haproxy
src_http_err_rate([<table>]): integer
```

Entspricht dem Konverter "table_http_err_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_err_rate([`<table>`])

<a id="entry-7-3-3-src-http-fail-cnt-integer"></a>

**`src_http_fail_cnt([<table>]): integer`**

```haproxy
src_http_fail_cnt([<table>]): integer
```

Entspricht dem Konverter "table_http_fail_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_fail_cnt([`<table>`])

<a id="entry-7-3-3-src-http-fail-rate-integer"></a>

**`src_http_fail_rate([<table>]): integer`**

```haproxy
src_http_fail_rate([<table>]): integer
```

Entspricht dem Konverter "table_http_fail_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_fail_rate([`<table>`])

<a id="entry-7-3-3-src-http-req-cnt-integer"></a>

**`src_http_req_cnt([<table>]): integer`**

```haproxy
src_http_req_cnt([<table>]): integer
```

Entspricht dem Konverter "table_http_req_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_req_cnt([`<table>`])

<a id="entry-7-3-3-src-http-req-rate-integer"></a>

**`src_http_req_rate([<table>]): integer`**

```haproxy
src_http_req_rate([<table>]): integer
```

Entspricht dem Konverter "table_http_req_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_http_req_rate([`<table>`])

<a id="entry-7-3-3-src-inc-gpc-integer"></a>

**`src_inc_gpc(<idx>[,<table>]): integer`**

```haproxy
src_inc_gpc(<idx>[,<table>]): integer
```

Entspricht dem Konverter "src_inc_gpc", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_inc_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-inc-gpc0-integer"></a>

**`src_inc_gpc0([<table>]): integer`**

```haproxy
src_inc_gpc0([<table>]): integer
```

Entspricht dem Konverter "src_inc_gpc0", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_inc_gpc0([`<table>`])

<a id="entry-7-3-3-src-inc-gpc1-integer"></a>

**`src_inc_gpc1([<table>]): integer`**

```haproxy
src_inc_gpc1([<table>]): integer
```

Entspricht dem Konverter "src_inc_gpc1", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_inc_gpc1([`<table>`])

src_is_local: boolean Gibt true zurück, wenn die Quelladresse der eingehenden Verbindung lokal auf dem System liegt, oder false, wenn die Adresse auf dem System nicht vorhanden ist, die Verbindung also von einem entfernten Rechner kommt. UNIX-Adressen gelten als lokal. Damit lassen sich bestimmte Zugriffsbeschränkungen anhand der Herkunft des Clients anwenden, beispielsweise die Forderung nach Authentifizierung oder https für entfernte Rechner. Die Prüfung benötigt einige Systemaufrufe und sollte daher möglichst nur einmal pro Verbindung erfolgen.

<a id="entry-7-3-3-src-kbytes-in-integer"></a>

**`src_kbytes_in([<table>]): integer`**

```haproxy
src_kbytes_in([<table>]): integer
```

Entspricht dem Konverter "table_kbytes_in", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_kbytes_in([`<table>`])

<a id="entry-7-3-3-src-kbytes-out-integer"></a>

**`src_kbytes_out([<table>]): integer`**

```haproxy
src_kbytes_out([<table>]): integer
```

Entspricht dem Konverter "table_kbytes_out", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_kbytes_out([`<table>`])

src_port: integer Gibt eine Ganzzahl zurück, die dem TCP-Quellport der Verbindung auf der Client-Seite entspricht, also dem Port, von dem aus der Client die Verbindung aufgebaut hat. Beliebige tcp/http-Regeln können diese Adresse ändern. Diese Funktion ist nur begrenzt nützlich, da moderne Protokolle Quellports heute kaum berücksichtigen.

<a id="entry-7-3-3-src-sess-cnt-integer"></a>

**`src_sess_cnt([<table>]): integer`**

```haproxy
src_sess_cnt([<table>]): integer
```

Entspricht dem Konverter "table_sess_cnt", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_sess_cnt([`<table>`])

<a id="entry-7-3-3-src-sess-rate-integer"></a>

**`src_sess_rate([<table>]): integer`**

```haproxy
src_sess_rate([<table>]): integer
```

Entspricht dem Konverter "table_sess_rate", wobei der Schlüssel auf die Quelladresse der eingehenden Verbindung gesetzt ist.

Entspricht: src,table_sess_rate([`<table>`])

<a id="entry-7-3-3-src-updt-conn-cnt-integer"></a>

**`src_updt_conn_cnt([<table>]): integer`**

```haproxy
src_updt_conn_cnt([<table>]): integer
```

Erstellt oder aktualisiert den der Quelladresse der eingehenden Verbindung zugeordneten Eintrag in der Stick Table des aktuellen Proxys oder in der angegebenen Stick Table. Diese Tabelle muss zum Speichern des Datentyps "conn_cnt" konfiguriert sein, andernfalls wird der Abgleich ignoriert. Der aktuelle Zähler wird um eins erhöht und der Ablaufzeitgeber aufgefrischt. Der aktualisierte Zählerwert wird zurückgegeben; dieser Abgleich kann daher nicht null zurückgeben. Dies wurde verwendet, um Dienstmissbrauch anhand der Quelladresse abzuweisen. Hinweis: Es wird empfohlen, stattdessen die umfassenderen Aktionen "track-sc\*" in "tcp-request"-Regeln zu verwenden.

Beispiel:

```shell
# This frontend limits incoming SSH connections to 3 per 10 second for
# each source address, and rejects excess connections until a 10 second
# silence is observed. At most 20 addresses are tracked.
listen ssh
    bind :22
    mode tcp
    maxconn 100
    stick-table type ip size 20 expire 10s store conn_cnt
    tcp-request content reject if { src_updt_conn_cnt gt 3 }
    server local 127.0.0.1:22
```

srv_id: integer Gibt bei der Verarbeitung der Antwort eine Ganzzahl mit der ID des Servers zurück. Obwohl dies fast ausschließlich mit ACLs verwendet wird, ist es auch für die Protokollierung oder Fehlersuche einsetzbar. Kann auch in einem tcp-check- oder http-check-Regelsatz verwendet werden.

srv_name: string Gibt bei der Verarbeitung der Antwort eine Zeichenkette mit dem Namen des Servers zurück. Obwohl dies fast ausschließlich mit ACLs verwendet wird, ist es auch für die Protokollierung oder Fehlersuche einsetzbar. Kann auch in einem tcp-check- oder http-check-Regelsatz verwendet werden.

txn.conn_retries: integer Gibt die Anzahl der Verbindungswiederholungen zurück, die dieser Stream beim Verbindungsaufbau zum Server durchlaufen hat. Der Wert kann sich ändern, solange die Verbindung nicht vollständig hergestellt ist. Bei HTTP-Verbindungen kann der Wert durch L7-Wiederholungen beeinflusst werden.

txn.redispatched: boolean Gibt true zurück, wenn die Verbindung bei einer Wiederholung gemäß der Konfiguration von "option redispatch" einem Redispatch unterzogen wurde. Der Wert kann sich ändern, solange die Verbindung nicht vollständig hergestellt ist. Bei HTTP-Verbindungen kann der Wert durch L7-Wiederholungen beeinflusst werden.

### 7.3.4. Sample-Abruf auf Schicht 5 {#section-7-3-4}

Schicht 5 beschreibt üblicherweise nur die Sitzungsschicht, die in HAProxy der Sitzung am nächsten liegt, nachdem alle Verbindungs-Handshakes abgeschlossen sind, aber noch keine Inhalte verfügbar sind. Die hier beschriebenen Abrufmethoden können bereits in den Regelsätzen "tcp-request content" verwendet werden, sofern sie keine erst später verfügbaren Informationen benötigen. Dazu gehören im Allgemeinen die Ergebnisse von SSL-Aushandlungen.

Übersicht über die Sample-Abrufmethoden in diesem Abschnitt und ihre jeweiligen Typen:

```text
  Schlüsselwort                                    Ausgabetyp
-------------------------------------------------+-------------
51d.all(<prop>[,<prop>*])                          string
bs.aborted                                         boolean
bs.debug_str([<bitmap>])                           string
bs.id                                              integer
bs.rst_code                                        integer
fs.aborted                                         boolean
fs.debug_str([<bitmap>])                           string
fs.id                                              integer
fs.rst_code                                        integer
ssl_bc                                             boolean
ssl_bc_alg_keysize                                 integer
ssl_bc_alpn                                        string
ssl_bc_cipher                                      string
ssl_bc_client_early_traffic_secret                 string
ssl_bc_client_handshake_traffic_secret             string
ssl_bc_client_random                               binary
ssl_bc_client_traffic_secret_0                     string
ssl_bc_curve                                       string
ssl_bc_early_exporter_secret                       string
ssl_bc_err                                         integer
ssl_bc_err_str                                     string
ssl_bc_exporter_secret                             string
ssl_bc_is_resumed                                  boolean
ssl_bc_npn                                         string
ssl_bc_protocol                                    string
ssl_bc_server_handshake_traffic_secret             string
ssl_bc_server_random                               binary
ssl_bc_server_traffic_secret_0                     string
ssl_bc_session_id                                  binary
ssl_bc_session_key                                 binary
ssl_bc_sni                                         string
ssl_bc_unique_id                                   binary
ssl_bc_use_keysize                                 integer
ssl_c_ca_err                                       integer
ssl_c_ca_err_depth                                 integer
ssl_c_chain_der                                    binary
ssl_c_der                                          binary
ssl_c_err                                          integer
ssl_c_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_key_alg                                      string
ssl_c_notafter                                     string
ssl_c_notbefore                                    string
ssl_c_r_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_san                                          string
ssl_c_serial                                       binary
ssl_c_sha1                                         binary
ssl_c_sig_alg                                      string
ssl_c_used                                         boolean
ssl_c_verify                                       integer
ssl_c_version                                      integer
ssl_f_der                                          binary
ssl_f_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_key_alg                                      string
ssl_f_notafter                                     string
ssl_f_notbefore                                    string
ssl_f_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_serial                                       binary
ssl_f_sha1                                         binary
ssl_f_sig_alg                                      string
ssl_f_version                                      integer
ssl_fc                                             boolean
ssl_fc_alg_keysize                                 integer
ssl_fc_alpn                                        string
ssl_fc_cipher                                      string
ssl_fc_cipherlist_bin([<filter_option>])           binary
ssl_fc_cipherlist_hex([<filter_option>])           string
ssl_fc_cipherlist_str([<filter_option>])           string
ssl_fc_cipherlist_xxh                              integer
ssl_fc_client_early_traffic_secret                 string
ssl_fc_client_handshake_traffic_secret             string
ssl_fc_client_random                               binary
ssl_fc_client_traffic_secret_0                     string
ssl_fc_crtname                                     string
ssl_fc_curve                                       string
ssl_fc_early_exporter_secret                       string
ssl_fc_ecformats_bin                               binary
ssl_fc_eclist_bin([<filter_option>])               binary
ssl_fc_err                                         integer
ssl_fc_err_str                                     string
ssl_fc_exporter_secret                             string
ssl_fc_extlist_bin([<filter_option>])              binary
ssl_fc_has_crt                                     boolean
ssl_fc_has_early                                   boolean
ssl_fc_has_sni                                     boolean
ssl_fc_is_resumed                                  boolean
ssl_fc_npn                                         string
ssl_fc_protocol                                    string
ssl_fc_protocol_hello_id                           integer
ssl_fc_server_handshake_traffic_secret             string
ssl_fc_server_random                               binary
ssl_fc_server_traffic_secret_0                     string
ssl_fc_session_id                                  binary
ssl_fc_session_key                                 binary
ssl_fc_sigalgs_bin([<filter_option>])              binary
ssl_fc_sni                                         string
ssl_fc_supported_versions_bin([<filter_option>])   binary
ssl_fc_unique_id                                   binary
ssl_fc_use_keysize                                 integer
ssl_s_chain_der                                    binary
ssl_s_der                                          binary
ssl_s_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_key_alg                                      string
ssl_s_notafter                                     string
ssl_s_notbefore                                    string
ssl_s_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_serial                                       binary
ssl_s_sha1                                         binary
ssl_s_sig_alg                                      string
ssl_s_version                                      integer
txn.timer.user                                     integer
-------------------------------------------------+-------------
```

Ausführliche Liste:

<a id="entry-7-3-4-51d-all-string"></a>

**`51d.all(<prop>[,<prop>*]): string`**

```haproxy
51d.all(<prop>[,<prop>*]): string
```

Gibt die Werte der angeforderten Eigenschaften als Zeichenkette zurück. Die Werte werden durch das mit "51degrees-property-separator" angegebene Trennzeichen getrennt. Das Gerät wird anhand aller wichtigen HTTP-Header der Anfrage identifiziert. Der Funktion können bis zu fünf Eigenschaftsnamen übergeben werden. Kann ein Eigenschaftsname nicht gefunden werden, wird der Wert "NoData" zurückgegeben.

Beispiel:

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request
# containing the three properties requested using all relevant headers from
# the request.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[51d.all(DeviceType,IsMobile,IsTablet)]
```

bs.aborted: boolean Gibt true zurück, wenn für den aktuellen Stream ein Abbruch vom Server empfangen wurde. Andernfalls wird false zurückgegeben.

<a id="entry-7-3-4-bs-debug-str-string"></a>

**`bs.debug_str([<bitmap>]): string`**

```haproxy
bs.debug_str([<bitmap>]): string
```

Diese Funktion ist für Entwickler bei bestimmten komplexen Fehlersuchen gedacht. Sie extrahiert interne Zustände aus den unteren Ebenen des Backend-Streams und der Verbindung und ordnet sie als Zeichenkette an, üblicherweise als Folge durch Leerzeichen getrennter "name=value"-Einträge. Das optionale Argument `<bitmap>` legt fest, aus welchen Ebenen Informationen extrahiert werden, und ist ein arithmetisches OR oder die Summe der folgenden Werte: - Socket-Ebene: 16 - Verbindungsebene: 8 - Transportebene (z. B. SSL): 4 - Mux-Verbindung: 2 - Mux-Stream: 1

Diese Werte können sich zwischen Versionen ändern. Der Standardwert null hat eine besondere Bedeutung und aktiviert alle Ebenen. Verlassen Sie sich für eine langfristige Produktionsüberwachung nicht auf die Ausgabe dieser Funktion. Sie kann sich bei Bedarf an weiteren Details auch innerhalb eines stabilen Zweigs weiterentwickeln. Ein typischer Anwendungsfall besteht darin, diese Informationen zusammen mit fs.debug_str() ganz am Ende eines log-format anzuhängen. Beispiel:

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

bs.id: integer Gibt die Stream-ID des Multiplexers auf der Server-Seite zurück. Der Multiplexer ist dafür verantwortlich, die passenden Informationen zurückzugeben.

bs.rst_code: integer Gibt den vom Server für den aktuellen Stream empfangenen Reset-Code zurück. Zurückgegeben wird der Code des vom Server empfangenen H2-Frames RST_STREAM oder QUIC-Frames STOP_SENDING. Der Sample-Abruf schlägt fehl, wenn kein Abbruch empfangen wurde oder der Server-Stream kein H2/QUIC-Stream ist.

fs.aborted: boolean Gibt true zurück, wenn für den aktuellen Stream ein Abbruch vom Client empfangen wurde. Andernfalls wird false zurückgegeben.

<a id="entry-7-3-4-fs-debug-str-string"></a>

**`fs.debug_str([<bitmap>]): string`**

```haproxy
fs.debug_str([<bitmap>]): string
```

Diese Funktion ist für Entwickler bei bestimmten komplexen Fehlersuchen gedacht. Sie extrahiert interne Zustände aus den unteren Ebenen des Frontend-Streams und der Verbindung und ordnet sie als Zeichenkette an, üblicherweise als Folge durch Leerzeichen getrennter "name=value"-Einträge. Das optionale Argument `<bitmap>` legt fest, aus welchen Ebenen Informationen extrahiert werden, und ist ein arithmetisches OR oder die Summe der folgenden Werte: - Socket-Ebene: 16 - Verbindungsebene: 8 - Transportebene (z. B. SSL): 4 - Mux-Verbindung: 2 - Mux-Stream: 1

Diese Werte können sich zwischen Versionen ändern. Der Standardwert null hat eine besondere Bedeutung und aktiviert alle Ebenen. Verlassen Sie sich für eine langfristige Produktionsüberwachung nicht auf die Ausgabe dieser Funktion. Sie kann sich bei Bedarf an weiteren Details auch innerhalb eines stabilen Zweigs weiterentwickeln. Ein typischer Anwendungsfall besteht darin, diese Informationen zusammen mit bs.debug_str() ganz am Ende eines log-format anzuhängen. Beispiel:

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

fs.id: integer Gibt die Stream-ID des Multiplexers auf der Client-Seite zurück. Der Multiplexer ist dafür verantwortlich, die passenden Informationen zurückzugeben. Bei reinem TCP wird beispielsweise stets 0 zurückgegeben, da kein Stream vorhanden ist.

fs.rst_code: integer Gibt den vom Client für den aktuellen Stream empfangenen Reset-Code zurück. Zurückgegeben wird der Code des vom Client empfangenen H2-Frames RST_STREAM oder QUIC-Frames STOP_SENDING. Der Sample-Abruf schlägt fehl, wenn kein Abbruch empfangen wurde oder der Client-Stream kein H2/QUIC-Stream ist.

ssl_bc: boolean Gibt true zurück, wenn die Backend-Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde und lokal entschlüsselt wird. Das bedeutet, dass die ausgehende Verbindung zu einem Server mit der Option "ssl" hergestellt wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_alg_keysize: integer Gibt die unterstützte Schlüssellänge des symmetrischen Verschlüsselungsverfahrens in Bits zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_alpn: string Extrahiert das Feld Application Layer Protocol Negotiation aus einer ausgehenden Verbindung über eine TLS-Transportschicht. Das Ergebnis ist eine Zeichenkette mit dem mit dem Server ausgehandelten Protokollnamen. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Die TLS-Erweiterung ALPN wird nur angekündigt, wenn das Schlüsselwort "alpn" in der "server"-Zeile eine Protokollliste festlegt. Der Server ist außerdem nicht gezwungen, ein Protokoll aus dieser Liste zu wählen; ein beliebiges anderes kann angefordert werden. Die TLS-Erweiterung ALPN soll die TLS-Erweiterung NPN ersetzen. Siehe auch "ssl_bc_npn". Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_cipher: string Gibt den Namen des verwendeten Verschlüsselungsverfahrens zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_client_early_traffic_secret: string Gibt CLIENT_EARLY_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_client_handshake_traffic_secret: string Gibt CLIENT_HANDSHAKE_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_client_random: binary Gibt den Client-Zufallswert der Backend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_client_traffic_secret_0: string Gibt CLIENT_TRAFFIC_SECRET_0 als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_curve: string Gibt den Namen der beim Schlüsselaustausch verwendeten Kurve zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 3.0.0 oder AWS-LC \>= 1.57.0.

ssl_bc_early_exporter_secret: string Gibt EARLY_EXPORTER_SECRET als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_err: integer Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten ausgehenden Verbindung die ID des letzten Fehlers im ersten auf der Backend-Seite aufgetretenen Fehlerstapel zurück. Dies kann Handshake-Fehler sowie andere während der Lebensdauer der Verbindung auftretende Lese- oder Schreibfehler umfassen. Eine Textbeschreibung dieses Fehlercodes erhalten Sie mit dem Sample-Abruf "ssl_bc_err_str" oder dem Befehl "openssl errstr", der einen Fehlercode in hexadezimaler Darstellung als Parameter erwartet. Die vollständige Liste der Fehlercodes finden Sie in der Dokumentation Ihrer SSL-Bibliothek.

ssl_bc_err_str: string Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten ausgehenden Verbindung eine Zeichenkettendarstellung des letzten Fehlers im ersten Fehlerstapel zurück, der aus Sicht des Backends auf der Verbindung aufgetreten ist. Siehe auch "ssl_fc_err".

ssl_bc_exporter_secret: string Gibt EXPORTER_SECRET als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_is_resumed: boolean Gibt true zurück, wenn die Backend-Verbindung über eine SSL/TLS-Transportschicht hergestellt und die neu angelegte SSL-Sitzung mithilfe einer zwischengespeicherten Sitzung oder eines TLS-Tickets wiederaufgenommen wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_npn: string Extrahiert das Feld Next Protocol Negotiation aus einer ausgehenden Verbindung über eine TLS-Transportschicht. Das Ergebnis ist eine Zeichenkette mit dem mit dem Server ausgehandelten Protokollnamen. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Die TLS-Erweiterung NPN wird nur angekündigt, wenn das Schlüsselwort "npn" in der "server"-Zeile eine Protokollliste festlegt. Der Server ist außerdem nicht gezwungen, ein Protokoll aus dieser Liste zu wählen; jedes andere kann ebenfalls verwendet werden. Die TLS-Erweiterung NPN wurde durch ALPN ersetzt. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_protocol: string Gibt den Namen des verwendeten Protokolls zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_server_handshake_traffic_secret: string Gibt SERVER_HANDSHAKE_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_server_random: binary Gibt den Server-Zufallswert der Backend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_server_traffic_secret_0: string Gibt SERVER_TRAFFIC_SECRET_0 als hexadezimale Zeichenkette für die Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_bc_session_id: binary Gibt die SSL-ID der Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Die Protokollierung ist nützlich, um festzustellen, ob eine Sitzung wiederverwendet wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_session_key: binary Gibt den SSL-Sitzungs-Master-Schlüssel der Backend-Verbindung zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_sni: string Ruft das Feld der TLS-Erweiterung Server Name Indication (SNI) ab, das auf der Verbindung zum Server verwendet wurde. Das Ergebnis ist, sofern vorhanden, typischerweise eine Zeichenkette, die dem HTTPS-Hostnamen entspricht (253 Zeichen oder weniger). Der Hauptanwendungsfall ist die Protokollierung und Fehlersuche, etwa um festzustellen, welches SNI beim Verbindungsaufbau verwendet wurde, und es mit dem vom Server gesehenen Wert abzugleichen.

ssl_bc_unique_id: binary Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten ausgehenden Verbindung die eindeutige TLS-ID gemäß RFC5929 [Abschnitt 3](https://www.rfc-editor.org/rfc/rfc5929#section-3) zurück. Die eindeutige ID kann mit dem Konverter "ssl_bc_unique_id,base64" base64-kodiert werden. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_bc_use_keysize: integer Gibt die verwendete Schlüssellänge des symmetrischen Verschlüsselungsverfahrens in Bits zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Kann in einem tcp-check- oder http-check-Regelsatz verwendet werden.

ssl_c_ca_err: integer Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die ID des ersten bei der Prüfung des Client-Zertifikats in einer Tiefe \> 0 erkannten Fehlers zurück, oder 0, wenn bei dieser Prüfung kein Fehler auftrat. Die vollständige Liste der Fehlercodes finden Sie in der Dokumentation Ihrer SSL-Bibliothek.

ssl_c_ca_err_depth: integer Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die Tiefe in der CA-Kette zurück, in der der erste Fehler bei der Prüfung des Client-Zertifikats erkannt wurde. Trat kein Fehler auf, wird 0 zurückgegeben.

ssl_c_chain_der: binary Gibt die vom Client vorgelegte Zertifikatskette im DER-Format zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden. Das Ergebnis lässt sich mit jeder Bibliothek analysieren, die ASN.1-DER-Daten akzeptiert. Wiederaufgenommene Sitzungen werden derzeit nicht unterstützt.

ssl_c_der: binary Gibt das vom Client vorgelegte Zertifikat im DER-Format zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden.

ssl_c_err: integer Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die ID des ersten bei der Prüfung in Tiefe 0 erkannten Fehlers zurück, oder 0, wenn bei dieser Prüfung kein Fehler auftrat. Die vollständige Liste der Fehlercodes finden Sie in der Dokumentation Ihrer SSL-Bibliothek.

<a id="entry-7-3-4-ssl-c-i-dn-string"></a>

**`ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung den vollständigen Distinguished Name des Ausstellers des vom Client vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_c_i_dn(OU,2)" die zweite Organisationseinheit und "ssl_c_i_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_c_i_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_c_key_alg: string Gibt den Namen des Algorithmus zurück, mit dem der Schlüssel des vom Client vorgelegten Zertifikats erzeugt wurde, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_c_notafter: string Gibt das vom Client vorgelegte Enddatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_c_notbefore: string Gibt das vom Client vorgelegte Anfangsdatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

<a id="entry-7-3-4-ssl-c-r-dn-string"></a>

**`ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten und mit der konfigurierten ca-file erfolgreich validierten eingehenden Verbindung den vollständigen Distinguished Name der Root-CA des vom Client vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_c_r_dn(OU,2)" die zweite Organisationseinheit und "ssl_c_r_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_c_r_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

<a id="entry-7-3-4-ssl-c-s-dn-string"></a>

**`ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung den vollständigen Distinguished Name des Subjekts des vom Client vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_c_s_dn(OU,2)" die zweite Organisationseinheit und "ssl_c_s_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_c_s_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_c_san: string Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung mit Client-Zertifikat eine Zeichenkette mit den durch Kommas getrennten Subject-Alt-Name-Feldern des vorgelegten Zertifikats zurück.

Damit lässt sich das Client-Zertifikat untersuchen.

Beispiel:

```text
acl is_valid_client_cert ssl_c_used && ! ssl_c_verify
http-request set-header X-SSL-Client-SAN %[ssl_c_san] if is_valid_client_cert
```

ergibt:

```text
X-SSL-Client-SAN: IP Address:127.0.0.1, IP Address:127.0.0.2, IP Address:127.0.0.3, URI:http://docs.haproxy.org/2.7/, DNS:ca.tests.haproxy.com

```

ssl_c_serial: binary Gibt die Seriennummer des vom Client vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden.

ssl_c_sha1: binary Gibt den SHA-1-Fingerabdruck des vom Client vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Damit lässt sich ein Client an einen Server binden oder diese Information an einen Server weitergeben. Die Ausgabe ist binär; zur Weitergabe dieser Signatur an den Server muss sie daher hexadezimal oder mit base64 kodiert werden, wie im folgenden Beispiel:

Beispiel:

```text
http-request set-header X-SSL-Client-SHA1 %[ssl_c_sha1,hex]
```

ssl_c_sig_alg: string Gibt den Namen des Algorithmus zurück, mit dem das vom Client vorgelegte Zertifikat signiert wurde, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_c_used: boolean Gibt true zurück, wenn die aktuelle SSL-Sitzung ein Client-Zertifikat verwendet, auch wenn die aktuelle Verbindung eine SSL-Sitzungswiederaufnahme nutzt. Siehe auch "ssl_fc_has_crt".

ssl_c_verify: integer Gibt die Fehler-ID des Prüfergebnisses zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde, andernfalls null, wenn kein Fehler auftritt. Die vollständige Liste der Fehlercodes finden Sie in der Dokumentation Ihrer SSL-Bibliothek.

ssl_c_version: integer Gibt die Version des vom Client vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_f_der: binary Gibt das vom Frontend vorgelegte Zertifikat im DER-Format zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden.

<a id="entry-7-3-4-ssl-f-i-dn-string"></a>

**`ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung den vollständigen Distinguished Name des Ausstellers des vom Frontend vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_f_i_dn(OU,2)" die zweite Organisationseinheit und "ssl_f_i_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_f_i_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_f_key_alg: string Gibt den Namen des Algorithmus zurück, mit dem der Schlüssel des vom Frontend vorgelegten Zertifikats erzeugt wurde, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_f_notafter: string Gibt das vom Frontend vorgelegte Enddatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_f_notbefore: string Gibt das vom Frontend vorgelegte Anfangsdatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

<a id="entry-7-3-4-ssl-f-s-dn-string"></a>

**`ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung den vollständigen Distinguished Name des Subjekts des vom Frontend vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_f_s_dn(OU,2)" die zweite Organisationseinheit und "ssl_f_s_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_f_s_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_f_serial: binary Gibt die Seriennummer des vom Frontend vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden.

ssl_f_sha1: binary Gibt den SHA-1-Fingerabdruck des vom Frontend vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Damit lässt sich feststellen, welches Zertifikat mittels SNI ausgewählt wurde.

ssl_f_sig_alg: string Gibt den Namen des Algorithmus zurück, mit dem das vom Frontend vorgelegte Zertifikat signiert wurde, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_f_version: integer Gibt die Version des vom Frontend vorgelegten Zertifikats zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_fc: boolean Gibt true zurück, wenn die Frontend-Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde und lokal entschlüsselt wird. Das bedeutet, dass sie einem Socket entspricht, der mit einer "bind"-Zeile mit der Option "ssl" deklariert wurde.

Beispiel:

```shell
# This passes "X-Proto: https" to servers when client connects over SSL
listen http-https
    bind :80
    bind :443 ssl crt /etc/haproxy.pem
    http-request add-header X-Proto https if { ssl_fc }
```

ssl_fc_alg_keysize: integer Gibt die unterstützte Schlüssellänge des symmetrischen Verschlüsselungsverfahrens in Bits zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_fc_alpn: string Extrahiert das Feld Application Layer Protocol Negotiation aus einer eingehenden Verbindung über eine TLS-Transportschicht, die HAProxy lokal entschlüsselt. Das Ergebnis ist eine Zeichenkette mit dem vom Client angekündigten Protokollnamen. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Die TLS-Erweiterung ALPN wird nur angekündigt, wenn das Schlüsselwort "alpn" in der "bind"-Zeile eine Protokollliste festlegt. Der Client ist außerdem nicht gezwungen, ein Protokoll aus dieser Liste zu wählen; ein beliebiges anderes kann angefordert werden. Die TLS-Erweiterung ALPN soll die TLS-Erweiterung NPN ersetzen. Siehe auch "ssl_fc_npn".

ssl_fc_cipher: string Gibt den Namen des verwendeten Verschlüsselungsverfahrens zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

<a id="entry-7-3-4-ssl-fc-cipherlist-bin-binary"></a>

**`ssl_fc_cipherlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_cipherlist_bin([<filter_option>]): binary
```

Gibt die binäre Form der Verschlüsselungsverfahrensliste aus dem ClientHello zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte:

```text
0: die vollständige Liste der Verschlüsselungsverfahren zurückgeben (Standard)
1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen
```

Beispiel:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-cipherlist-hex-string"></a>

**`ssl_fc_cipherlist_hex([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_hex([<filter_option>]): string
```

Gibt die binäre Form der Verschlüsselungsverfahrensliste aus dem ClientHello hexadezimal kodiert zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte:

```text
0: die vollständige Liste der Verschlüsselungsverfahren zurückgeben (Standard)
1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen
```

<a id="entry-7-3-4-ssl-fc-cipherlist-str-string"></a>

**`ssl_fc_cipherlist_str([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_str([<filter_option>]): string
```

Gibt die dekodierte Textform der Verschlüsselungsverfahrensliste aus dem ClientHello zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte:

```text
0: die vollständige Liste der Verschlüsselungsverfahren zurückgeben (Standard)
1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen
```

Dieser Sample-Abruf ist nur mit OpenSSL \>= 1.0.2 verfügbar. Ist die Funktion nicht aktiviert, gibt dieser Sample-Abruf wie "ssl_fc_cipherlist_xxh" den Hash zurück.

ssl_fc_cipherlist_xxh: integer Gibt einen xxh64-Hash der Verschlüsselungsverfahrensliste zurück. Dieser Hash kann nur zurückgegeben werden, wenn "tune.ssl.capture-buffer-size" größer als 0 ist. Der Hash berücksichtigt dennoch sämtliche Daten der Verschlüsselungsverfahrensliste.

ssl_fc_client_early_traffic_secret: string Gibt CLIENT_EARLY_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_client_handshake_traffic_secret: string Gibt CLIENT_HANDSHAKE_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_client_random: binary Gibt den Client-Zufallswert der Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL.

ssl_fc_client_traffic_secret_0: string Gibt CLIENT_TRAFFIC_SECRET_0 als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_crtname: string Gibt den Namen des Zertifikats zurück, das für die eingehende SSL/TLS-Verbindung ausgewählt wurde. Dies ist der Name, wie er in "show ssl cert" erscheint: je nach Deklaration des Zertifikats in der Konfiguration ein Dateiname mit relativem oder absolutem Pfad oder ein Alias.

Beispiel:

```text
crt-store example
    load crt "example.com.pem"

frontend www
    bind *:443 ssl crt "@example/example.com.pem"
    acl match_certificate ssl_fc_crtname -m beg -i "@example/"
    http-request set-header X-Cert-Name %[ssl_fc_crtname] if match_certificate
```

ssl_fc_curve: string Gibt den Namen der beim Schlüsselaustausch verwendeten Kurve zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 3.0.0.

ssl_fc_early_rcvd: boolean Gibt true zurück, wenn auf dieser Verbindung frühzeitige Daten empfangen wurden, unabhängig davon, ob der Handshake inzwischen abgeschlossen ist. Für die Verkehrsverarbeitung hat dies keinen praktischen Anwendungsfall, ist aber praktisch die einzige Möglichkeit, zu erkennen, dass ein Client 0-RTT zum Senden frühzeitiger Daten verwendet hat. Das kann bei der Fehlersuche nützlich sein, da die einzigen Alternativen Netzwerkmitschnitte oder das Protokollieren der Flags der Frontend-Verbindung und deren Abgleich mit dem Code sind. Auch zum Erfassen von Statistiken über Client-Fähigkeiten kann dies nützlich sein. Siehe auch "ssl_fc_has_early".

ssl_fc_early_exporter_secret: string Gibt EARLY_EXPORTER_SECRET als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_ecformats_bin: binary Gibt die binäre Form der im ClientHello angegebenen unterstützten Punktformate elliptischer Kurven zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird.

Beispiel:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-eclist-bin-binary"></a>

**`ssl_fc_eclist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_eclist_bin([<filter_option>]): binary
```

Gibt die binäre Form der im ClientHello angegebenen unterstützten elliptischen Kurven zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte:

```text
0: die vollständige Liste der unterstützten elliptischen Kurven zurückgeben (Standard)
1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen
```

Beispiel:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_err: integer Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die ID des letzten Fehlers im ersten auf der Frontend-Seite aufgetretenen Fehlerstapel zurück, oder 0, wenn kein Fehler auftrat. Damit lassen sich Handshake-Fehler außerhalb der Zertifikatsprüfung, etwa nicht passende Verschlüsselungsverfahren, sowie andere während der Lebensdauer der Verbindung auftretende Lese- oder Schreibfehler erkennen. Fehler bei der Prüfung des Client-Zertifikats werden nicht über diesen Abruf gemeldet, sondern über die vorhandenen Abrufe "ssl_c_err", "ssl_c_ca_err" und "ssl_c_ca_err_depth". Eine Textbeschreibung dieses Fehlercodes erhalten Sie mit dem Sample-Abruf "ssl_fc_err_str" oder dem Befehl "openssl errstr", der einen Fehlercode in hexadezimaler Darstellung als Parameter erwartet. Die vollständige Liste der Fehlercodes finden Sie in der Dokumentation Ihrer SSL-Bibliothek.

ssl_fc_err_str: string Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung eine Zeichenkettendarstellung des letzten Fehlers im ersten auf der Frontend-Seite aufgetretenen Fehlerstapel zurück. Fehler bei der Prüfung des Client-Zertifikats werden nicht über diesen Abruf gemeldet. Siehe auch "ssl_fc_err".

ssl_fc_exporter_secret: string Gibt EXPORTER_SECRET als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

<a id="entry-7-3-4-ssl-fc-extlist-bin-binary"></a>

**`ssl_fc_extlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_extlist_bin([<filter_option>]): binary
```

Gibt die binäre Form der Erweiterungsliste aus dem ClientHello zurück. Die maximale Länge des Rückgabewerts wird durch die Größe des gemeinsamen Erfassungspuffers begrenzt, die mit "tune.ssl.capture-buffer-size" gesteuert wird. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte:

```text
0: die vollständige Liste der Erweiterungen zurückgeben (Standard)
1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen
```

Beispiel:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_has_crt: boolean Gibt true zurück, wenn in einer eingehenden Verbindung über eine SSL/TLS-Transportschicht ein Client-Zertifikat vorhanden ist. Dies ist nützlich, wenn die Anweisung 'verify' auf 'optional' gesetzt ist. Hinweis: Bei der Wiederaufnahme einer SSL-Sitzung mit Session ID oder TLS-Ticket ist das Client-Zertifikat in der aktuellen Verbindung nicht vorhanden, kann aber aus dem Cache oder Ticket abgerufen werden. Verwenden Sie daher bevorzugt "ssl_c_used", wenn Sie prüfen möchten, ob die aktuelle SSL-Sitzung ein Client-Zertifikat verwendet.

ssl_fc_has_early: boolean Gibt true zurück, wenn frühzeitige Daten gesendet wurden und der Handshake noch nicht abgeschlossen ist. Da dies Auswirkungen auf die Sicherheit hat, ist es nützlich, solche Daten ablehnen oder bis zum Abschluss des Handshakes warten zu können, etwa mit der Aktion "wait-for-handshake". Siehe auch "ssl_fc_early_rcvd".

ssl_fc_has_sni: boolean Prüft, ob in einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die TLS-Erweiterung Server Name Indication (SNI) vorhanden ist. Gibt true zurück, wenn die eingehende Verbindung ein TLS-SNI-Feld enthält. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen).

ssl_fc_is_resumed: boolean Gibt true zurück, wenn die SSL/TLS-Sitzung einer eingehenden Verbindung über eine SSL/TLS-Transportschicht mithilfe des SSL-Sitzungscaches oder von TLS-Tickets wiederaufgenommen wurde.

ssl_fc_npn: string Extrahiert das Feld Next Protocol Negotiation aus einer eingehenden Verbindung über eine TLS-Transportschicht, die HAProxy lokal entschlüsselt. Das Ergebnis ist eine Zeichenkette mit dem vom Client angekündigten Protokollnamen. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen). Die TLS-Erweiterung NPN wird nur angekündigt, wenn das Schlüsselwort "npn" in der "bind"-Zeile eine Protokollliste festlegt. Der Client ist außerdem nicht gezwungen, ein Protokoll aus dieser Liste zu wählen; ein beliebiges anderes kann angefordert werden. Die TLS-Erweiterung NPN wurde durch ALPN ersetzt.

ssl_fc_protocol: string Gibt den Namen des verwendeten Protokolls zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_fc_protocol_hello_id: integer Die Version des TLS-Protokolls, mit der der Client laut ClientHello-Nachricht während der Sitzung kommunizieren möchte. Dieser Wert kann nur zurückgegeben werden, wenn "tune.ssl.capture-buffer-size" größer als 0 ist.

Beispiel:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_server_handshake_traffic_secret: string Gibt SERVER_HANDSHAKE_TRAFFIC_SECRET als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_server_random: binary Gibt den Server-Zufallswert der Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL.

ssl_fc_server_traffic_secret_0: string Gibt SERVER_TRAFFIC_SECRET_0 als hexadezimale Zeichenkette für die Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine TLS-1.3-Transportschicht hergestellt wurde. Erfordert OpenSSL \>= 1.1.1. Dies ist einer der Schlüssel, die der OpenSSL-Keylog-Callback zur Erzeugung der SSLKEYLOGFILE ausgibt. Die SSL-Schlüsselprotokollierung muss mit "tune.ssl.keylog on" im Abschnitt global aktiviert werden. Siehe auch "tune.ssl.keylog".

ssl_fc_session_id: binary Gibt die SSL-ID der Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Damit lässt sich ein bestimmter Client an einen Server binden. Beachten Sie, dass einige Browser ihre Sitzungs-ID alle paar Minuten erneuern.

ssl_fc_session_key: binary Gibt den SSL-Sitzungs-Master-Schlüssel der Frontend-Verbindung zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Dies ist zum Entschlüsseln von Verkehr nützlich, der mit Verfahren mit kurzlebigen Schlüsseln gesendet wurde. Erfordert OpenSSL \>= 1.1.0 oder BoringSSL.

<a id="entry-7-3-4-ssl-fc-sigalgs-bin-binary"></a>

**`ssl_fc_sigalgs_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_sigalgs_bin([<filter_option>]): binary
```

Gibt den Inhalt der TLS-Erweiterung signatures_algorithms (13) zurück, die im ClientHello übermittelt wurde. Liefert eine binäre Liste von jeweils 2 Bytes langen Algorithmuskennungen gemäß dem TLS-RFC:
<https://datatracker.ietf.org/doc/html/rfc8446#section-4.2.3>.

Dieser Wert kann nur zurückgegeben werden, wenn "tune.ssl.capture-buffer-size" größer als 0 ist. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte: 0: vollständige Liste der Verschlüsselungsverfahren zurückgeben (Standard); 1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen.

ssl_fc_sni: string Extrahiert das Feld der TLS-Erweiterung Server Name Indication (SNI) aus einer eingehenden Verbindung über eine SSL/TLS-Transportschicht, die HAProxy lokal entschlüsselt. Das Ergebnis ist, sofern vorhanden, typischerweise eine Zeichenkette, die dem HTTPS-Hostnamen entspricht (253 Zeichen oder weniger). Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen).

Dieser Abruf unterscheidet sich vom obigen "req.ssl_sni" dadurch, dass er sich auf die von HAProxy entschlüsselte Verbindung bezieht und nicht auf unverändert weitergeleitete SSL-Inhalte. Siehe auch "ssl_fc_sni_end" und "ssl_fc_sni_reg" weiter unten. Die SSL-Bibliothek muss mit aktivierter Unterstützung für TLS-Erweiterungen gebaut worden sein (mit haproxy -vv prüfen).

ACHTUNG! Außer unter sehr speziellen Bedingungen ist es normalerweise nicht korrekt, dieses Feld als Ersatz für das HTTP-Headerfeld "Host" zu verwenden. Beispielsweise muss beim Weiterleiten einer HTTPS-Verbindung an einen Server das SNI-Feld mithilfe von "req.hdr(host)" aus dem HTTP-Host-Headerfeld gesetzt werden und nicht aus dem SNI-Wert der Frontend-Verbindung. SNI dient ausschließlich dazu, das von der Server-Seite vorgelegte Zertifikat auszuwählen. Clients dürfen anschließend Anfragen mit unterschiedlichen Host-Werten senden, solange diese mit den Namen im Zertifikat übereinstimmen. Daher sollte "ssl_fc_sni" normalerweise nicht als Argument des Server-Schlüsselworts "sni" verwendet werden, sofern das Backend nicht im TCP-Modus arbeitet.

Abgeleitete ACLs:

```text
ssl_fc_sni_end: Suffixabgleich
ssl_fc_sni_reg: Abgleich mit regulären Ausdrücken
```

<a id="entry-7-3-4-ssl-fc-supported-versions-bin-binary"></a>

**`ssl_fc_supported_versions_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_supported_versions_bin([<filter_option>]): binary
```

Gibt den Inhalt der TLS-Erweiterung supported_versions (43) zurück, die im ClientHello übermittelt wurde. Liefert eine binäre Liste von jeweils 2 Bytes langen Versionskennungen: TLSv1.3 (0x0304), TLSv1.2 (0x0303).

Dieser Wert kann nur zurückgegeben werden, wenn "tune.ssl.capture-buffer-size" größer als 0 ist. Mit `<filter_option>` lassen sich die zurückgegebenen Daten filtern. Zulässige Werte: 0: vollständige Liste der Verschlüsselungsverfahren zurückgeben (Standard); 1: GREASE-Werte (RFC8701) aus der Ausgabe ausschließen.

ssl_fc_unique_id: binary Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten eingehenden Verbindung die eindeutige TLS-ID gemäß RFC5929 [Abschnitt 3](https://www.rfc-editor.org/rfc/rfc5929#section-3) zurück. Die eindeutige ID kann mit dem Konverter "ssl_fc_unique_id,base64" base64-kodiert werden.

ssl_fc_use_keysize: integer Gibt die verwendete Schlüssellänge des symmetrischen Verschlüsselungsverfahrens in Bits zurück, wenn die eingehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_s_chain_der: binary Gibt die vom Server vorgelegte Zertifikatskette im DER-Format zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden. Das Ergebnis lässt sich mit jeder Bibliothek analysieren, die ASN.1-DER-Daten akzeptiert. Wiederaufgenommene Sitzungen werden derzeit nicht unterstützt.

ssl_s_der: binary Gibt das vom Server vorgelegte Zertifikat im DER-Format zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können die abzugleichenden Werte in hexadezimaler Form angegeben werden.

<a id="entry-7-3-4-ssl-s-i-dn-string"></a>

**`ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten ausgehenden Verbindung den vollständigen Distinguished Name des Ausstellers des vom Server vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_s_i_dn(OU,2)" die zweite Organisationseinheit und "ssl_s_i_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_s_i_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_s_key_alg: string Gibt den Namen des Algorithmus zurück, mit dem der Schlüssel des vom Server vorgelegten Zertifikats erzeugt wurde, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_s_notafter: string Gibt das vom Server vorgelegte Enddatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

ssl_s_notbefore: string Gibt das vom Server vorgelegte Anfangsdatum als formatierte Zeichenkette YYMMDDhhmmss[Z] zurück, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

<a id="entry-7-3-4-ssl-s-s-dn-string"></a>

**`ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Gibt bei einer über eine SSL/TLS-Transportschicht hergestellten ausgehenden Verbindung den vollständigen Distinguished Name des Subjekts des vom Server vorgelegten Zertifikats zurück, wenn kein `<entry>` angegeben ist. Andernfalls wird der Wert des ersten angegebenen Eintrags vom Anfang des DN aus zurückgegeben. Wird als optionales zweites Argument eine positive oder negative Vorkommensnummer angegeben, wird der Wert des n-ten angegebenen Eintrags vom Anfang bzw. Ende des DN aus zurückgegeben. Beispielsweise liefert "ssl_s_s_dn(OU,2)" die zweite Organisationseinheit und "ssl_s_s_dn(CN)" den Common Name. Mit dem Parameter `<format>` erhalten Sie den DN in einer für verschiedene Protokolle geeigneten Form. Derzeit wird rfc2253 für LDAP v3 unterstützt. Soll nur das Format geändert werden, können Sie für die ersten beiden Parameter eine leere Zeichenkette und null angeben. Beispiel: ssl_s_s_dn(,0,rfc2253). Enthält der ASN.1-Wert des angeforderten Eintrags (oder, wenn kein `<entry>` angegeben ist, der Wert eines beliebigen Eintrags im DN) ein eingebettetes NUL-Byte mit darauf folgenden weiteren Daten, gilt er als fehlerhaft und es werden keine Daten zurückgegeben.

ssl_s_serial: binary Gibt die Seriennummer des vom Server präsentierten Zertifikats zurück, wenn die ausgehende
Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Bei Verwendung in einer ACL können
die Vergleichswerte in hexadezimaler Form angegeben werden.

ssl_s_sha1: binary Gibt den SHA-1-Fingerabdruck des vom Server präsentierten Zertifikats zurück, wenn die
ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde. Damit lässt sich
feststellen, welches Zertifikat anhand von SNI ausgewählt wurde.

ssl_s_sig_alg: string Gibt den Namen des Algorithmus zurück, mit dem das vom Server präsentierte
Zertifikat signiert wurde, wenn die ausgehende Verbindung über eine SSL/TLS-Transportschicht
hergestellt wurde.

ssl_s_version: integer Gibt die Version des vom Server präsentierten Zertifikats zurück, wenn die
ausgehende Verbindung über eine SSL/TLS-Transportschicht hergestellt wurde.

txn.timer.user: integer Geschätzte Gesamtdauer aus Sicht des Clients vom Annehmen der Verbindung durch
den Proxy bis zum Schließen beider Enden, ohne Leerlaufzeit. Dies entspricht %Tu im log-format und
wird in Millisekunden (ms) angegeben. Weitere Einzelheiten finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4)
„Zeitereignisse“.

### 7.3.5. Sample-Abruf aus Pufferinhalten (Schicht 6) {#section-7-3-5}

Der Sample-Abruf aus Pufferinhalten unterscheidet sich etwas von den zuvor beschriebenen
Abrufmethoden, da die abgerufenen Daten nur vorübergehend vorhanden sind. Sie können nur verwendet
werden, solange sie verfügbar sind, und gehen beim Weiterleiten verloren. Deshalb können etwa
Samples, die während einer Anfrage aus Pufferinhalten abgerufen wurden, nicht in einer Antwort
verwendet werden. Selbst während des Abrufs können sich die Daten ändern. Manchmal müssen
Verzögerungen eingerichtet oder mehrere Methoden zum Sample-Abruf kombiniert werden, damit die
erwarteten Daten vollständig und verwendbar sind, beispielsweise durch die Inhaltsprüfung von
TCP-Anfragen. Weitere Einzelheiten hierzu finden Sie beim Schlüsselwort "tcp-request content".

Warnung: Die folgenden Methoden zum Sample-Abruf werden bei Verwendung in HTTP-Proxys ignoriert.
Sie verarbeiten ausschließlich die Rohinhalte der Puffer. HTTP-Proxys verwenden dagegen
strukturierte Inhalte, deren Rohdarstellung daher bedeutungslos ist. Wenn eine ACL eine der
folgenden Abrufmethoden verwendet, wird eine Warnung ausgegeben. Es lassen sich jedoch nicht alle
ungültigen Verwendungen erkennen, etwa in einem benutzerdefinierten Protokollformat oder einem
Sample-Ausdruck. Seien Sie deshalb vorsichtig.

Übersicht der Methoden zum Sample-Abruf in diesem Abschnitt und ihrer jeweiligen Typen:

```text
  Schlüsselwort                                       Ausgabetyp
----------------------------------------------------+-------------
distcc_body(<token>[,<occ>])                          binary
distcc_param(<token>[,<occ>])                         integer
payload(<offset>,<length>)                            binary
payload_lv(<offset1>,<length>[,<offset2>])            binary
rdp_cookie([<name>])                                  string
rdp_cookie_cnt([name])                                integer
rep_ssl_hello_type                                    integer
req.len                                               integer
req.payload(<offset>,<length>)                        binary
req.payload_lv(<offset1>,<length>[,<offset2>])        binary
req.proto_http                                        boolean
req.rdp_cookie([<name>])                              string
req.rdp_cookie_cnt([name])                            integer
req.ssl_alpn                                          string
req.ssl_cipherlist                                    binary
req.ssl_ec_ext                                        boolean
req.ssl_hello_type                                    integer
req.ssl_keyshare_groups                               binary
req.ssl_sigalgs                                       binary
req.ssl_sni                                           string
req.ssl_st_ext                                        integer
req.ssl_supported_groups                              binary
req.ssl_ver                                           integer
req_len                                               integer
req_proto_http                                        boolean
req_ssl_hello_type                                    integer
req_ssl_sni                                           string
req_ssl_ver                                           integer
res.len                                               integer
res.payload(<offset>,<length>)                        binary
res.payload_lv(<offset1>,<length>[,<offset2>])        binary
res.ssl_hello_type                                    integer
----------------------------------------------------+-------------
```

Ausführliche Liste:

<a id="entry-7-3-5-distcc-body-binary"></a>

**`distcc_body(<token>[,<occ>]): binary`**

```haproxy
distcc_body(<token>[,<occ>]): binary
```

Analysiert eine distcc-Nachricht und gibt den zum Vorkommen \#`<occ>` des Tokens `<token>` gehörenden
Inhalt zurück. Die Zählung der Vorkommen beginnt bei 1. Ohne Angabe kann ein beliebiges Vorkommen
passen, auch wenn derzeit in der Praxis nur das erste geprüft wird. Damit lassen sich Dateinamen
oder Argumente aus Dateien extrahieren, die mit distcc über HAProxy erstellt werden. Die vollständige
Liste der unterstützten Tokens finden Sie in der Protokolldokumentation von distcc.

<a id="entry-7-3-5-distcc-param-integer"></a>

**`distcc_param(<token>[,<occ>]): integer`**

```haproxy
distcc_param(<token>[,<occ>]): integer
```

Analysiert eine distcc-Nachricht und gibt den zum Vorkommen \#`<occ>` des Tokens `<token>` gehörenden
Parameter zurück. Die Zählung der Vorkommen beginnt bei 1. Ohne Angabe kann ein beliebiges Vorkommen
passen, auch wenn derzeit in der Praxis nur das erste geprüft wird. Damit lassen sich bestimmte
Informationen wie die Protokollversion, die Dateigröße oder das Argument aus Dateien extrahieren,
die mit distcc über HAProxy erstellt werden. Eine weitere Anwendung besteht darin, vor dem
Verbindungsaufbau zum Server auf den Beginn des vorverarbeiteten Dateiinhalts zu warten, um
ungenutzte Verbindungen zu vermeiden. Die vollständige Liste der unterstützten Tokens finden Sie
in der Protokolldokumentation von distcc.

Beispiel:

```shell
# wait up to 20s for the pre-processed file to be uploaded
tcp-request inspect-delay 20s
tcp-request content accept if { distcc_param(DOTI) -m found }
# send large files to the big farm
use_backend big_farm if { distcc_param(DOTI) gt 1000000 }
```

<a id="entry-7-3-5-payload-binary"></a>

**`payload(<offset>,<length>): binary (deprecated)`**

```haproxy
payload(<offset>,<length>): binary (deprecated)
```

Dies ist ein Alias für "req.payload" im Kontext einer Anfrage, etwa bei "stick on" oder "stick
match", und für "res.payload" im Kontext einer Antwort, etwa bei "stick store
response".

<a id="entry-7-3-5-payload-lv-binary"></a>

**`payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)`**

```haproxy
payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)
```

Dies ist ein Alias für "req.payload_lv" im Kontext einer Anfrage, etwa bei "stick on" oder "stick
match", und für "res.payload_lv" im Kontext einer Antwort, etwa bei "stick store
response".

req.len: integer req_len: integer (veraltet) Gibt eine Ganzzahl zurück, die der Anzahl der Bytes im
Anfragepuffer entspricht. Dies wird vor allem in ACL verwendet. Beachten Sie, dass dieser Test
nicht false zurückgibt, solange sich der Puffer noch verändert. Eine Prüfung auf Gleichheit mit
null trifft daher am Sitzungsbeginn fast immer sofort zu, während ein Test auf mehr Daten auf
deren Eingang wartet und erst dann false zurückgibt, wenn HAProxy sicher ist, dass keine weiteren
Daten eintreffen werden. Dieser Test wurde für die Inhaltsprüfung von TCP-Anfragen entwickelt.

<a id="entry-7-3-5-req-payload-binary"></a>

**`req.payload(<offset>,<length>): binary`**

```haproxy
req.payload(<offset>,<length>): binary
```

Extrahiert einen Binärblock mit `<length>` Bytes, der bei Byte `<offset>` im Anfragepuffer beginnt.
Ist das Argument `<length>` null, wird als Sonderfall der gesamte Puffer ab `<offset>` bis zum Ende
extrahiert. Damit lässt sich in ACLs prüfen, ob bestimmte Inhalte an einer beliebigen Stelle im
Puffer vorhanden sind.

ACL-Varianten:

```text
req.payload(<offset>,<length>): hexadezimaler Binärabgleich
```

<a id="entry-7-3-5-req-payload-lv-binary"></a>

**`req.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
req.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

Extrahiert einen Binärblock, dessen Größe im Anfragepuffer bei `<offset1>` über `<length>` Bytes
angegeben ist. Der Block beginnt bei `<offset2>`, sofern angegeben, andernfalls direkt nach dem
Längenfeld. Der Parameter `<offset2>` unterstützt auch relative Versätze, wenn ein '+' oder '-'
vorangestellt wird.

ACL-Varianten:

```text
req.payload_lv(<offset1>,<length>[,<offset2>]): hexadezimaler Binärabgleich
```

Beispiel: Siehe das Beispiel beim Schlüsselwort "stick store-response".

req.proto_http: boolean req_proto_http: boolean (veraltet) Gibt true zurück, wenn die Daten im
Anfragepuffer wie HTTP aussehen und sich korrekt als HTTP analysieren lassen. Dafür wird derselbe
Parser wie für gewöhnliche HTTP-Anfragen verwendet, sodass keine Überraschungen zu erwarten sind.
Der Test trifft erst zu, wenn die Anfrage vollständig ist, fehlgeschlagen ist oder eine
Zeitüberschreitung vorliegt. Er kann das Protokoll in TCP-Protokolleinträgen angeben; hauptsächlich
wird er jedoch verwendet, um die Analyse von TCP-Anfragen anzuhalten, bis eine vollständige
HTTP-Anfrage im Puffer liegt, etwa um einen Header nachzuverfolgen.

Beispiel:

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content reject if !HTTP
tcp-request content track-sc0 base table req-rate
```

<a id="entry-7-3-5-req-rdp-cookie-string"></a>

**`req.rdp_cookie([<name>]): string`**

```haproxy
req.rdp_cookie([<name>]): string
rdp_cookie([<name>]): string (deprecated)
```

Wenn der Anfragepuffer wie das RDP-Protokoll aussieht, wird das RDP-Cookie `<name>` extrahiert;
ohne Namensangabe ein beliebiges Cookie. Wie in der RDP-Protokollspezifikation dargestellt, prüft
der Parser nur das erste Cookie. Beim Cookie-Namen wird nicht zwischen Groß- und Kleinschreibung
unterschieden. In der Regel wird der Cookie-Name "MSTS" verwendet, da dieses Cookie bei passender
Client-Konfiguration den Benutzernamen des Clients enthalten kann, der sich mit dem Server
verbindet. Auch das Cookie "MSTSHASH" wird häufig für die Sitzungsbindung an Server verwendet.

Der Unterschied zu "balance rdp-cookie" besteht darin, dass ein beliebiger Algorithmus zur
Lastverteilung verwendet werden kann und die Verteilung der Clients auf Backend-Server deshalb
nicht an einen Hash des RDP-Cookies gebunden ist. Es wird erwartet, dass ein Algorithmus wie
"balance roundrobin" oder "balance leastconn" die Clients gleichmäßiger auf Backend-Server
verteilt als der von "balance
rdp-cookie" verwendete Hash.

ACL-Varianten:

```text
req.rdp_cookie([<name>]): exakter Zeichenkettenabgleich
```

Beispiel:

```text
listen tse-farm
    bind 0.0.0.0:3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # Persist based on the mstshash cookie
    # This is only useful makes sense if
    # balance rdp-cookie is not used
    stick-table type string size 204800
    stick on req.rdp_cookie(mstshash)
    server srv1 1.1.1.1:3389
    server srv1 1.1.1.2:3389
```

Siehe auch: "balance rdp-cookie", "persist rdp-cookie", "tcp-request" und die ACL "req.rdp_cookie".

<a id="entry-7-3-5-req-rdp-cookie-cnt-integer"></a>

**`req.rdp_cookie_cnt([name]): integer`**

```haproxy
req.rdp_cookie_cnt([name]): integer
rdp_cookie_cnt([name]): integer (deprecated)
```

Versucht, den Anfragepuffer als RDP-Protokoll zu analysieren, und gibt dann eine Ganzzahl zurück,
die der Anzahl der gefundenen RDP-Cookies entspricht. Wird optional ein Cookie-Name angegeben,
werden nur Cookies mit diesem Namen berücksichtigt. Dies wird vor allem in ACL verwendet.

ACL-Varianten:

```text
req.rdp_cookie_cnt([<name>]): Ganzzahlabgleich
```

req.ssl_alpn: string Gibt eine Zeichenfolge mit den Werten der TLS-Erweiterung Application-Layer
Protocol Negotiation (ALPN, RFC7301) zurück, die der Client in der SSL-ClientHello-Nachricht gesendet
hat. Dies gilt nur für die Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine
SSL-Datenschicht entschlüsselt wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option
"ssl". In ACL kann damit anhand der ALPN-Präferenzen eines TLS-Clients eine Routingentscheidung
getroffen werden, wie im folgenden Beispiel. Siehe auch "ssl_fc_alpn". Diese Abrufmethode analysiert
nur die erste ClientHello-Nachricht im Anfragepuffer. Einzelheiten zu den Folgen dieser
Einschränkung (HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) finden Sie in der
Dokumentation zum Schlüsselwort "req.ssl_sni".

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_acme if { req.ssl_alpn acme-tls/1 }
default_backend bk_default
```

<a id="entry-7-3-5-req-ssl-cipherlist-binary"></a>

**`req.ssl_cipherlist binary`**

```haproxy
req.ssl_cipherlist binary
```

Gibt die binäre Darstellung der vom Client unterstützten symmetrischen Verschlüsselungsoptionen
zurück, wie sie im Inhalt einer TLS-ClientHello-Nachricht angegeben sind. Dies gilt nur für die
Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt
wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Das entsprechende
Gegenstück für eine SSL-Bindung ist "ssl_fc_cipherlist_bin"; es kann verwendet werden, wenn die
Option "ssl" angegeben ist. Diese Abrufmethode analysiert nur die erste ClientHello-Nachricht im
Anfragepuffer. Einzelheiten zu den Folgen dieser Einschränkung (HelloRetryRequest, Neuaushandlung,
Encrypted Client Hello) finden Sie in der Dokumentation zum Schlüsselwort "req.ssl_sni".

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_cipherlist,be2hex(:,2),lower -m sub 1302:009f }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ec_ext: boolean Gibt einen booleschen Wert zurück, der angibt, ob der Client die in RFC4492,
[Abschnitt 5.1](https://www.rfc-editor.org/rfc/rfc4492#section-5.1) definierte Erweiterung Supported Elliptic Curves
in der SSL-ClientHello-Nachricht gesendet hat. Damit kann auf derselben IP-Adresse ECC-kompatiblen
Clients ein EC-Zertifikat präsentiert und für alle anderen RSA verwendet werden. Dies gilt nur
für die Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht
entschlüsselt wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Diese
Abrufmethode analysiert nur die erste ClientHello-Nachricht im Anfragepuffer. Einzelheiten zu den
Folgen dieser Einschränkung (HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) finden Sie
in der Dokumentation zum Schlüsselwort "req.ssl_sni".

req.ssl_hello_type: integer req_ssl_hello_type: integer (veraltet) Gibt eine Ganzzahl mit dem Typ der
SSL-Hello-Nachricht im Anfragepuffer zurück, wenn dessen Daten als vollständige SSL-Client-Hello-
Nachricht (v3 oder höher) analysiert werden können. Dies gilt nur für die Rohinhalte im Anfragepuffer
und nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt wurden. Daher funktioniert es
nicht bei "bind"-Zeilen mit der Option "ssl". Dies wird vor allem in ACL verwendet, um eine
SSL-Hello-Nachricht zu erkennen, die eine zur Sitzungsbindung verwendbare SSL-Sitzungs-ID enthalten
soll. Diese Abrufmethode analysiert nur die erste ClientHello-Nachricht im Anfragepuffer.
Einzelheiten zu den Folgen dieser Einschränkung (HelloRetryRequest, Neuaushandlung, Encrypted
Client Hello) finden Sie in der Dokumentation zum Schlüsselwort "req.ssl_sni".

<a id="entry-7-3-5-req-ssl-keyshare-groups-binary"></a>

**`req.ssl_keyshare_groups binary`**

```haproxy
req.ssl_keyshare_groups binary
```

Gibt die binäre Darstellung der Liste kryptografischer Parameter für den Schlüsselaustausch zurück,
die der Client laut TLS-ClientHello unterstützt. In TLS v1.3 ist keyshare Bestandteil der
ClientHello-Nachricht und deren letzte Erweiterung. Dies gilt nur für die Rohinhalte im
Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt wurden. Daher
funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Diese Abrufmethode analysiert nur die
erste ClientHello-Nachricht im Anfragepuffer. Einzelheiten zu den Folgen dieser Einschränkung
(HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) finden Sie in der Dokumentation zum
Schlüsselwort "req.ssl_sni".

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_keyshare_groups,be2hex(:,2),lower -m sub 001d  }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

<a id="entry-7-3-5-req-ssl-sigalgs-binary"></a>

**`req.ssl_sigalgs binary`**

```haproxy
req.ssl_sigalgs binary
```

Gibt die binäre Darstellung der Liste der Signaturalgorithmen zurück, die der Client laut
TLS-ClientHello unterstützt. Diese Information ist als Client-Hello-Erweiterung verfügbar. Dies
gilt nur für die Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht
entschlüsselt wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Das
entsprechende Gegenstück für eine SSL-Bindung ist "ssl_fc_sigalgs_bin"; es kann verwendet werden,
wenn die Option "ssl" angegeben ist. Diese Abrufmethode analysiert nur die erste ClientHello-
Nachricht im Anfragepuffer. Einzelheiten zu den Folgen dieser Einschränkung (HelloRetryRequest,
Neuaushandlung, Encrypted Client Hello) finden Sie in der Dokumentation zum Schlüsselwort
"req.ssl_sni".

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe4 if { req.ssl_sigalgs,be2hex(:,2),lower -m sub 0403:0805 }
server fe4  ${htst_fe4_addr}:${htst_fe4_port}
```

req.ssl_sni: string req_ssl_sni: string (veraltet) Gibt eine Zeichenfolge mit dem Wert der
TLS-Erweiterung Server Name zurück, die ein Client in einem durch den Anfragepuffer laufenden
TLS-Datenstrom gesendet hat, sofern die Pufferdaten als vollständige SSL-Client-Hello-Nachricht
(v3 oder höher) analysiert werden können. Dies gilt nur für die Rohinhalte im Anfragepuffer und
nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt wurden. Daher funktioniert es nicht
bei "bind"-Zeilen mit der Option "ssl". Es funktioniert nur bei Protokollen mit implizitem TLS wie
HTTPS (443), IMAPS (993) oder SMTPS (465), jedoch nicht bei Protokollen mit explizitem TLS wie
SMTP (25/587) oder IMAP (143). SNI enthält normalerweise den Namen des Hosts, mit dem der Client
sich verbinden möchte (bei neueren Browsern). Dieser Test wurde für die Inhaltsprüfung von
TCP-Anfragen entwickelt. Wenn eine inhaltsabhängige Weiterleitung erforderlich ist, sollte zuerst
auf eine vollständige Client-Hello-Nachricht (Typ 1) gewartet werden, wie im folgenden Beispiel.
Siehe auch "ssl_fc_sni". Beachten Sie, dass der zurückgegebene Wert aus den nachfolgend erläuterten
Gründen (HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) nicht zuverlässig genug ist,
um allein darauf gestützt den Zugriff auf bestimmte Hosts zu erlauben oder zu verweigern.

Diese Abrufmethode analysiert nur die erste ClientHello-Nachricht im Anfragepuffer. Sendet der
Client mehrere ClientHello-Nachrichten im selben TCP-Datenstrom, etwa weil der Server im Rahmen
von TLS 1.3 einen HelloRetryRequest (HRR) angefordert hat oder weil der Client eine TLS-Neuaushandlung
beginnt, wird nur der SNI-Wert aus der allerersten ClientHello-Nachricht zurückgegeben. Bei der
Neuaushandlung wird später im selben TCP-Datenstrom eine neue ClientHello-Nachricht gesendet, die
möglicherweise einen anderen SNI-Wert enthält. Der Inhalt aller nachfolgenden ClientHello-
Nachrichten wird ignoriert.

Bei Verwendung von Encrypted Client Hello (ECH) ist die auf der Leitung sichtbare ClientHello-
Nachricht nur das äußere ClientHello ("Outer"), das das eigentliche, verschlüsselte innere
ClientHello ("Inner") enthält. Der hier extrahierte SNI-Wert stammt in diesem Fall aus dem äußeren
ClientHello und dient als Tarnung; er bezeichnet nicht den Host, den der Client tatsächlich
erreichen möchte. Diese Abrufmethode kann das innere ClientHello derzeit weder entschlüsseln noch
analysieren. Bei Verwendung von ECH dürfen Entscheidungen zur Weiterleitung oder Zugriffskontrolle
daher nicht auf diese Methode gestützt werden.

ACL-Varianten:

```text
req.ssl_sni: exakter Zeichenkettenabgleich
```

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_allow if { req.ssl_sni -f allowed_sites }
default_backend bk_sorry_page
```

req.ssl_st_ext: integer Gibt 0 zurück, wenn der Client keine TLS-Erweiterung SessionTicket (RFC5077)
gesendet hat, 1, wenn der Client die TLS-Erweiterung SessionTicket gesendet hat, und 2, wenn er
zusätzlich ein TLS-SessionTicket mit einer Länge ungleich null gesendet hat. Dies gilt nur für die
Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt
wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Damit lässt sich etwa
erkennen, ob der Client ein SessionTicket gesendet hat, und die Sitzungsbindung entsprechend
festlegen: Ohne SessionTicket kann die Bindung anhand der SessionID erfolgen; bei Verwendung von
SessionTickets kann darauf verzichtet werden, da kein serverseitiger Zustand vorliegt. Diese
Abrufmethode analysiert nur die erste ClientHello-Nachricht im Anfragepuffer. Einzelheiten zu den
Folgen dieser Einschränkung (HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) finden Sie
in der Dokumentation zum Schlüsselwort "req.ssl_sni".

<a id="entry-7-3-5-req-ssl-supported-groups-binary"></a>

**`req.ssl_supported_groups binary`**

```haproxy
req.ssl_supported_groups binary
```

Gibt die binäre Darstellung der Liste der vom Client laut TLS-ClientHello unterstützten Gruppen
für den Schlüsselaustausch zurück. Dies kann sowohl Schlüsselaustausch mit elliptischen Kurven als
auch ohne EC umfassen. Dies gilt nur für die Rohinhalte im Anfragepuffer und nicht für Inhalte, die
über eine SSL-Datenschicht entschlüsselt wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit
der Option "ssl". Das entsprechende Gegenstück für eine SSL-Bindung ist "ssl_fc_eclist_bin"; es
kann verwendet werden, wenn die Option "ssl" angegeben ist. Diese Abrufmethode analysiert nur die
erste ClientHello-Nachricht im Anfragepuffer. Einzelheiten zu den Folgen dieser Einschränkung
(HelloRetryRequest, Neuaushandlung, Encrypted Client Hello) finden Sie in der Dokumentation zum
Schlüsselwort "req.ssl_sni".

Beispiele:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_supported_groups, be2hex(:,2),lower -m sub 0017 }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ver: integer req_ssl_ver: integer (veraltet) Gibt eine Ganzzahl mit der Version des
SSL/TLS-Protokolls eines Datenstroms im Anfragepuffer zurück. Sowohl SSLv2-Hello-Nachrichten als
auch SSLv3-Nachrichten werden unterstützt. TLSv1 wird als SSL-Version 3.1 angegeben. Der Wert
besteht aus der mit 65536 multiplizierten Hauptversion zuzüglich der Nebenversion. Dies gilt nur
für die Rohinhalte im Anfragepuffer und nicht für Inhalte, die über eine SSL-Datenschicht
entschlüsselt wurden. Daher funktioniert es nicht bei "bind"-Zeilen mit der Option "ssl". Die
ACL-Variante des Tests vergleicht mit einer Dezimalschreibweise der Form MAJOR.MINOR (etwa 3.1).
Diese Abrufmethode wird vor allem in ACL verwendet. Sie analysiert nur die erste ClientHello-
Nachricht im Anfragepuffer. Einzelheiten zu den Folgen dieser Einschränkung (HelloRetryRequest,
Neuaushandlung, Encrypted Client Hello) finden Sie in der Dokumentation zum Schlüsselwort
"req.ssl_sni".

ACL-Varianten:

```text
req.ssl_ver: Dezimalabgleich
```

res.len: integer Gibt eine Ganzzahl zurück, die der Anzahl der Bytes im Antwortpuffer entspricht.
Dies wird vor allem in ACL verwendet. Beachten Sie, dass dieser Test nicht false zurückgibt,
solange sich der Puffer noch verändert. Eine Prüfung auf Gleichheit mit null trifft daher am
Anfang des Datenstroms fast immer sofort zu, während ein Test auf mehr Daten auf deren Eingang
wartet und erst dann false zurückgibt, wenn HAProxy sicher ist, dass keine weiteren Daten eintreffen
werden. Dieser Test wurde für die Inhaltsprüfung von TCP-Antworten entwickelt. Er kann aber auch
in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-5-res-payload-binary"></a>

**`res.payload(<offset>,<length>): binary`**

```haproxy
res.payload(<offset>,<length>): binary
```

Extrahiert einen Binärblock mit `<length>` Bytes, der bei Byte `<offset>` im Antwortpuffer beginnt.
Ist das Argument `<length>` null, wird als Sonderfall der gesamte Puffer ab `<offset>` bis zum Ende
extrahiert. Damit lässt sich in ACLs prüfen, ob bestimmte Inhalte an einer beliebigen Stelle im
Puffer vorhanden sind. Dies kann auch in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-5-res-payload-lv-binary"></a>

**`res.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
res.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

Extrahiert einen Binärblock, dessen Größe im Antwortpuffer bei `<offset1>` über `<length>` Bytes
angegeben ist. Der Block beginnt bei `<offset2>`, sofern angegeben, andernfalls direkt nach dem
Längenfeld. Der Parameter `<offset2>` unterstützt auch relative Versätze, wenn ein '+' oder '-'
vorangestellt wird. Dies kann auch in expect-Regeln auf Basis von tcp-check verwendet werden.

Beispiel: Siehe das Beispiel beim Schlüsselwort "stick store-response".

res.ssl_hello_type: integer rep_ssl_hello_type: integer (veraltet) Gibt eine Ganzzahl mit dem Typ der
SSL-Hello-Nachricht im Antwortpuffer zurück, wenn dessen Daten als vollständige SSL-Hello-Nachricht
(v3 oder höher) analysiert werden können. Dies gilt nur für die Rohinhalte im Antwortpuffer und
nicht für Inhalte, die über eine SSL-Datenschicht entschlüsselt wurden. Daher funktioniert es
nicht bei "server"-Zeilen mit der Option "ssl". Dies wird vor allem in ACL verwendet, um eine
SSL-Hello-Nachricht zu erkennen, die eine zur Sitzungsbindung verwendbare SSL-Sitzungs-ID enthalten
soll.

### 7.3.6. HTTP-Sample-Abruf (Schicht 7) {#section-7-3-6}

Samples können aus HTTP-Inhalten, Anfragen und Antworten abgerufen werden. Diese Anwendungsschicht
wird auch als Schicht 7 bezeichnet. Die Daten in diesem Abschnitt können erst abgerufen werden,
wenn eine vollständige HTTP-Anfrage oder -Antwort aus dem jeweiligen Anfrage- oder Antwortpuffer
analysiert wurde. Dies ist bei allen HTTP-spezifischen Regeln und in Abschnitten mit "mode http"
immer der Fall. Bei der TCP-Inhaltsprüfung muss möglicherweise eine Prüfverzögerung vorgesehen
werden, damit die Anfrage oder Antwort zunächst eintreffen kann. Diese Abrufmethoden benötigen
unter Umständen etwas mehr CPU-Ressourcen als die Methoden für Schicht 4, jedoch nicht viel mehr,
da Anfrage und Antwort indiziert sind.

Hinweis: Die HTTP-Verarbeitung in tcp-request content-Regeln funktioniert in einem HTTP-Proxy wie
erwartet. In einem TCP-Proxy funktioniert sie ohne HTTP-Upgrade hingegen nur für HTTP/1-Inhalte.
Bei HTTP/2-Inhalten ist nur die Präambel sichtbar. Deshalb können hier nur die Methoden
"req.proto_http", "req.ver" und gegebenenfalls "method" zum Sample-Abruf verwendet werden. Alle
anderen L7-Abrufmethoden schlagen fehl. Nach einem HTTP-Upgrade funktionieren sie ebenso wie in
einem HTTP-Proxy.

Übersicht der Methoden zum Sample-Abruf in diesem Abschnitt und ihrer jeweiligen Typen:

```text
  Schlüsselwort                                    Ausgabetyp
-------------------------------------------------+-------------
base                                               string
base32                                             integer
base32+src                                         binary
baseq                                              string
capture.req.hdr(<idx>)                             string
capture.req.method                                 string
capture.req.uri                                    string
capture.req.ver                                    string
capture.res.hdr(<idx>)                             string
capture.res.ver                                    string
cook([<name>])                                     string
cook_cnt([<name>])                                 integer
cook_val([<name>])                                 integer
cookie([<name>])                                   string
hdr([<name>[,<occ>]])                              string
hdr_cnt([<header>])                                integer
hdr_ip([<name>[,<occ>]])                           ip
hdr_val([<name>[,<occ>]])                          integer
http_auth(<userlist>)                              boolean
http_auth_bearer([<header>])                       string
http_auth_group(<userlist>)                        string
http_auth_pass                                     string
http_auth_type                                     string
http_auth_user                                     string
http_first_req                                     boolean
method                                             integer
path                                               string
pathq                                              string
query([<options>])                                 string
req.body                                           binary
req.body_len                                       integer
req.body_param([<name>[,i]])                       string
req.body_size                                      integer
req.cook([<name>])                                 string
req.cook_cnt([<name>])                             integer
req.cook_names([<delim>])                          string
req.cook_val([<name>])                             integer
req.fhdr(<name>[,<occ>])                           string
req.fhdr_cnt([<name>])                             integer
req.hdr([<name>[,<occ>]])                          string
req.hdr_cnt([<name>])                              integer
req.hdr_ip([<name>[,<occ>]])                       ip
req.hdr_names([<delim>])                           string
req.hdr_val([<name>[,<occ>]])                      integer
req.hdrs                                           string
req.hdrs_bin                                       binary
req.timer.hdr                                      integer
req.timer.idle                                     integer
req.timer.queue                                    integer
req.timer.tq                                       integer
req.ver                                            string
req_ver                                            string
request_date([<unit>])                             integer
res.body                                           binary
res.body_len                                       integer
res.body_size                                      integer
res.cache_hit                                      boolean
res.cache_name                                     string
res.comp                                           boolean
res.comp_algo                                      string
res.cook([<name>])                                 string
res.cook_cnt([<name>])                             integer
res.cook_names([<delim>])                          string
res.cook_val([<name>])                             integer
res.fhdr([<name>[,<occ>]])                         string
res.fhdr_cnt([<name>])                             integer
res.hdr([<name>[,<occ>]])                          string
res.hdr_cnt([<name>])                              integer
res.hdr_ip([<name>[,<occ>]])                       ip
res.hdr_names([<delim>])                           string
res.hdr_val([<name>[,<occ>]])                      integer
res.hdrs                                           string
res.hdrs_bin                                       binary
res.timer.hdr                                      integer
res.ver                                            string
resp_ver                                           string
scook([<name>])                                    string
scook_cnt([<name>])                                integer
scook_val([<name>])                                integer
server_status                                      integer
set-cookie([<name>])                               string
shdr([<name>[,<occ>]])                             string
shdr_cnt([<name>])                                 integer
shdr_ip([<name>[,<occ>]])                          ip
shdr_val([<name>[,<occ>]])                         integer
status                                             integer
txn.status                                         integer
txn.timer.total                                    integer
unique-id                                          string
url                                                string
url32                                              integer
url32+src                                          binary
url_ip                                             ip
url_param([<name>[,<delim>[,i]]])                  string
url_port                                           integer
urlp([<name>[,<delim>[,i]]])                       string
urlp_val([<name>[,<delim>[,i]]])                   integer
-------------------------------------------------+-------------
```

Ausführliche Liste:

base: string Gibt die Verkettung des ersten Host-Headers mit dem Pfadteil der Anfrage zurück. Der
Pfad beginnt beim ersten Schrägstrich und endet vor dem Fragezeichen. Dies kann in Umgebungen mit
virtuellen Hosts nützlich sein, um URL-Missbrauch zu erkennen und die Effizienz gemeinsam genutzter
Caches zu verbessern. Zusammen mit einer Stick Table begrenzter Größe lassen sich damit auch
Statistiken über die nach Host/Pfad am häufigsten angeforderten Objekte erfassen. In ACLs ermöglicht
dies einfache Regeln zur inhaltsabhängigen Weiterleitung, die Host und Pfad gleichzeitig
berücksichtigen, etwa "[www.example.com/favicon.ico](http://www.example.com/favicon.ico)". Siehe auch "path" und "uri".

ACL-Varianten:

```text
base    : exakter Zeichenkettenabgleich
base_beg: Präfixabgleich
base_dir: Unterverzeichnisabgleich
base_dom: Domainabgleich
base_end: Suffixabgleich
base_len: Längenabgleich
base_reg: Abgleich mit regulären Ausdrücken
base_sub: Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

base32: integer Gibt einen 32-Bit-Hash des Werts zurück, den die oben beschriebene Abrufmethode
"base" liefert. Damit kann auf stark besuchten Websites die Aktivität je URL verfolgt werden, ohne
sämtliche URLs speichern zu müssen. Stattdessen wird ein kürzerer Hash gespeichert, was viel
Speicher spart. Der Ausgabetyp ist eine vorzeichenlose Ganzzahl. Verwendet wird die Hashfunktion
SDBM mit vollständigem Lawineneffekt auf die Ausgabe. Technisch entspricht base32 exakt
"base,sdbm(1)".

base32+src: binary Gibt die Verkettung des oben beschriebenen Abrufs base32 mit dem unten
beschriebenen Abruf src zurück. Das Ergebnis ist vom Typ binary und je nach Adressfamilie der
Quelladresse 8 oder 20 Bytes groß. Damit lassen sich Zähler je IP und je URL führen.

baseq: string Gibt die Verkettung des ersten Host-Headers mit dem Pfadteil der Anfrage einschließlich
der Abfragezeichenfolge zurück. Der Pfad beginnt beim ersten Schrägstrich. Mit dieser Methode
anstelle von "base" lässt sich die Zielressource für Statistiken oder Caching korrekt identifizieren.
Siehe auch "path", "pathq" und "base".

<a id="entry-7-3-6-capture-req-hdr-string"></a>

**`capture.req.hdr(<idx>): string`**

```haproxy
capture.req.hdr(<idx>): string
```

Extrahiert den Inhalt des mit "capture request header" erfassten Headers. idx bezeichnet die
Position des Schlüsselworts capture in der Konfiguration. Der erste Eintrag hat den Index 0.
Siehe auch: "capture request header".

capture.req.method: string Extrahiert die Methode (METHOD) einer HTTP-Anfrage. Sie kann sowohl in der
Anfrage als auch in der Antwort verwendet werden. Anders als bei "method" ist dies möglich, weil
der Wert in gesondert zugewiesenem Speicher vorliegt.

capture.req.uri: string Extrahiert die URI der Anfrage, die beim ersten Schrägstrich beginnt und vor
dem ersten Leerzeichen in der Anfrage endet, ohne den Hostteil. Anders als "path" und "url" kann
dieser Wert sowohl in der Anfrage als auch in der Antwort verwendet werden, weil er in gesondert
zugewiesenem Speicher vorliegt.

capture.req.ver: string Extrahiert die HTTP-Version der Anfrage und gibt sie im Format
"HTTP/`<major>`.`<minor>`" zurück. Da die Information dauerhaft gespeichert ist, kann sie sowohl in
Anfragen und Antworten als auch in Protokolleinträgen verwendet werden. Ist die Version der Anfrage
ungültig, schlägt dieser Sample-Abruf fehl.

<a id="entry-7-3-6-capture-res-hdr-string"></a>

**`capture.res.hdr(<idx>): string`**

```haproxy
capture.res.hdr(<idx>): string
```

Extrahiert den Inhalt des mit "capture response header" erfassten Headers. idx bezeichnet die
Position des Schlüsselworts capture in der Konfiguration. Der erste Eintrag hat den Index 0.
Siehe auch: "capture response header".

capture.res.ver: string Extrahiert die HTTP-Version der Antwort und gibt sie im Format
"HTTP/`<major>`.`<minor>`" zurück. Da die Information dauerhaft gespeichert ist, kann sie in
Protokolleinträgen verwendet werden. Ist die Version der Antwort ungültig, schlägt dieser
Sample-Abruf fehl.

<a id="entry-7-3-6-cookie-string"></a>

**`cookie([<name>]): string (deprecated)`**

```haproxy
cookie([<name>]): string (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Cookie"-Headerzeile der
Anfrage oder einem "Set-Cookie"-Header der Antwort und gibt dessen Wert als Zeichenfolge zurück.
Eine typische Anwendung besteht darin, mehrere Clients mit demselben Profil denselben Server
verwenden zu lassen. Dies ähnelt der früheren Funktion von "appsession" mit der Anweisung
"request-learn", unterstützt aber die Synchronisierung zwischen mehreren Peers und die Erhaltung
des Zustands über Neustarts hinweg. Ohne Namensangabe wird der Wert des ersten Cookies
zurückgegeben. Diese Abrufmethode sollte nicht mehr verwendet und durch req.cook() oder res.cook()
ersetzt werden, da sie die Richtung abhängig vom Verwendungskontext mehrdeutig bestimmt.

<a id="entry-7-3-6-hdr-string"></a>

**`hdr([<name>[,<occ>]]): string`**

```haproxy
hdr([<name>[,<occ>]]): string
```

Dies entspricht bei Verwendung in Anfragen req.hdr() und bei Verwendung in Antworten res.hdr().
Einzelheiten finden Sie bei den jeweiligen Abrufmethoden. Verwenden Sie bei Zweifeln an der
Abrufrichtung die expliziten Varianten. Beachten Sie, dass sich die ACL-Schlüsselwörter hdr\_\*
im Gegensatz zur Sample-Abrufmethode hdr() eindeutig auf die Anfrageheader beziehen.

<a id="entry-7-3-6-http-auth-boolean"></a>

**`http_auth(<userlist>): boolean`**

```haproxy
http_auth(<userlist>): boolean
```

Gibt einen booleschen Wert zurück, der angibt, ob die vom Client empfangenen Authentifizierungsdaten
mit einem in der angegebenen userlist gespeicherten Benutzernamen samt Passwort übereinstimmen.
Außerhalb von ACLs ist diese Abruffunktion kaum nützlich. Derzeit wird nur die HTTP-Basic-
Authentifizierung unterstützt.

<a id="entry-7-3-6-http-auth-bearer-string"></a>

**`http_auth_bearer([<header>]): string`**

```haproxy
http_auth_bearer([<header>]): string
```

Gibt bei Verwendung des Bearer-Schemas das vom Client gelieferte Token aus den
Autorisierungsdaten zurück, beispielsweise beim Senden von JSON Web Tokens. Die vom Client
gesendeten Daten werden nicht geprüft. Wird ein bestimmter `<header>` angegeben, wird dieser
anstelle des Headers Authorization analysiert.

<a id="entry-7-3-6-http-auth-group-string"></a>

**`http_auth_group(<userlist>): string`**

```haproxy
http_auth_group(<userlist>): string
```

Gibt eine Zeichenfolge mit dem Benutzernamen aus den vom Client empfangenen Authentifizierungsdaten
zurück, wenn sowohl der Benutzername als auch das Passwort gemäß der angegebenen userlist gültig
sind. Dies ist hauptsächlich für ACLs vorgesehen, die anschließend prüfen, ob der Benutzer zu
mindestens einer Gruppe aus einer Liste gehört. Außerhalb von ACLs ist diese Abruffunktion kaum
nützlich. Derzeit wird nur die HTTP-Basic-Authentifizierung unterstützt.

ACL-Varianten:

```text
http_auth_group(<userlist>): group ...
Gibt wahr zurück, wenn der aus der Anfrage ermittelte Benutzer, dessen Passwort
gemäß der angegebenen userlist gültig ist, mindestens einer der
Gruppen angehört.
```

http_auth_pass: string Gibt das Passwort des Benutzers aus den vom Client empfangenen
Authentifizierungsdaten zurück, wie es im Header Authorization angegeben ist. Dieser Sample-Abruf
führt keine Prüfungen durch. Nur Basic-Authentifizierung wird unterstützt.

http_auth_type: string Gibt die Authentifizierungsmethode aus den vom Client empfangenen
Authentifizierungsdaten zurück, wie sie im Header Authorization angegeben ist. Dieser Sample-Abruf
führt keine Prüfungen durch. Nur Basic-Authentifizierung wird unterstützt.

http_auth_user: string Gibt den Benutzernamen aus den vom Client empfangenen Authentifizierungsdaten
zurück, wie er im Header Authorization angegeben ist. Dieser Sample-Abruf führt keine Prüfungen
durch. Nur Basic-Authentifizierung wird unterstützt.

http_first_req: boolean Gibt true zurück, wenn die gerade verarbeitete Anfrage die erste auf der
Verbindung ist. Damit lassen sich Header hinzufügen oder entfernen, die bei manchen späteren
Anfragen fehlen können, oder Anfragen in den Protokolleinträgen leichter gruppieren.

method: integer + string Gibt eine Ganzzahl zurück, die der Methode in der HTTP-Anfrage entspricht.
Beispielsweise entspricht "GET" dem Wert 1; die Zuordnung lässt sich im Quellcode nachsehen. Der
Wert 9 bedeutet „andere Methode“ und kann in eine aus dem Datenstrom extrahierte Zeichenfolge
umgewandelt werden. Dies sollte nicht direkt als Sample verwendet werden, sondern ausschließlich
in ACLs, die Methoden in Mustern transparent in diese Werte aus Ganzzahl und Zeichenfolge
umwandeln. Einige vordefinierte ACL prüfen bereits die gängigsten Methoden.

ACL-Varianten:

```text
method: Methodenabgleich ohne Berücksichtigung der Groß-/Kleinschreibung
```

Beispiel:

```shell
# only accept GET and HEAD requests
acl valid_method method GET HEAD
http-request deny if ! valid_method
```

path: string Extrahiert den URL-Pfad der Anfrage, der beim ersten Schrägstrich beginnt und vor dem
Fragezeichen endet, ohne den Hostteil. Typische Anwendungen sind Caches mit Vorabrufunterstützung
sowie Portale, die mehrere Informationen aus Datenbanken zusammenführen und in Caches vorhalten
müssen. Bei Caches für ausgehenden Verkehr wäre "url" die bessere Wahl. In ACLs wird dies meist
zum Vergleich exakter Dateinamen wie "/login.php" oder, über die abgeleiteten Varianten, von
Verzeichnisteilen verwendet. Siehe auch die Abrufmethoden "url" und "base". Beachten Sie, dass der
HTTP-Standard jeglichen Fragmentverweis in der URI ('#' nach dem Pfad) strikt verbietet und dieser
daher abgewiesen wird. Hat das Frontend, das die Anfrage empfängt, jedoch
"option accept-unsafe-violations-in-http-request" gesetzt, wird dieser Fragmentteil akzeptiert
und erscheint auch im Pfad.

ACL-Varianten:

```text
path    : exakter Zeichenkettenabgleich
path_beg: Präfixabgleich
path_dir: Unterverzeichnisabgleich
path_dom: Domainabgleich
path_end: Suffixabgleich
path_len: Längenabgleich
path_reg: Abgleich mit regulären Ausdrücken
path_sub: Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

pathq: string Extrahiert den URL-Pfad der Anfrage einschließlich der Abfragezeichenfolge, beginnend
beim ersten Schrägstrich. Diese Abrufmethode eignet sich dazu, stets eine relative URI ohne Schema
und gegebenenfalls vorhandenen Autoritätsteil zu erhalten. Während dies die übliche Darstellung
eines HTTP/1.1-Anfrageziels ist, wird bei HTTP/2 häufig eine absolute URI verwendet. Diese
Abrufmethode liefert in beiden Fällen dasselbe Ergebnis. Beachten Sie, dass der HTTP-Standard
jeglichen Fragmentverweis in der URI ('#' nach dem Pfad) strikt verbietet und dieser daher
abgewiesen wird. Hat das Frontend, das die Anfrage empfängt, jedoch
"option accept-unsafe-violations-in-http-request" gesetzt, wird dieser Fragmentteil akzeptiert
und erscheint auch im Pfad.

<a id="entry-7-3-6-query-string"></a>

**`query([<options>]): string`**

```haproxy
query([<options>]): string
```

Extrahiert die Abfragezeichenfolge der Anfrage, die nach dem ersten Fragezeichen beginnt. Ohne
Fragezeichen liefert dieser Abruf nichts zurück. Ist ein Fragezeichen vorhanden, auf das nichts
folgt, wird eine leere Zeichenfolge zurückgegeben. Mit der Vergleichsmethode "found" lässt sich
daher einfach feststellen, ob eine Abfragezeichenfolge vorhanden ist. Diese Abrufmethode ergänzt
"path", das vor dem Fragezeichen endet, und "query_string", das das Fragezeichen einschließt.

Mit einem optionalen Parameter lässt sich der Rückgabewert anpassen. Folgende Optionen werden
unterstützt:

    - with_qm: Das Fragezeichen am Anfang der Abfragezeichenfolge einschließen,
                sofern diese nicht leer ist.

req.body: binary Gibt den verfügbaren Inhalt der HTTP-Anfrage als Datenblock zurück. Es wird
empfohlen, "option http-buffer-request" zu verwenden, damit so weit wie möglich auf den
Anfrageinhalt gewartet wird.

req.body_len: integer Gibt die Länge des verfügbaren Inhalts der HTTP-Anfrage in Bytes zurück.
Sie kann geringer als die angekündigte Länge sein, wenn der Inhalt größer als der Puffer ist.
Es wird empfohlen, "option http-buffer-request" zu verwenden, damit so weit wie möglich auf den
Anfrageinhalt gewartet wird.

<a id="entry-7-3-6-req-body-param-string"></a>

**`req.body_param([<name>[,i]]): string`**

```haproxy
req.body_param([<name>[,i]]): string
```

Diese Abrufmethode setzt voraus, dass der Inhalt der POST-Anfrage URL-kodiert ist. Der Benutzer
kann prüfen, ob "content-type" den Wert "application/x-www-form-urlencoded" enthält. Extrahiert
wird das erste Vorkommen des Parameters `<name>` im Inhalt, das vor '&' endet. Beim Parameternamen
wird zwischen Groß- und Kleinschreibung unterschieden, sofern nicht "i" als zweites Argument
angegeben ist. Ohne Namensangabe passt jeder Parameter, und der erste wird zurückgegeben. Das
Ergebnis ist eine Zeichenfolge mit dem Wert des Parameters `<name>` in seiner Darstellung im
Anfrageinhalt; eine URL-Dekodierung erfolgt nicht. Beachten Sie, dass die ACL-Variante dieser
Abrufmethode mehrere Parameter durchläuft und ohne Namensangabe nacheinander alle Parameterwerte
liefert.

req.body_size: integer Gibt die angekündigte Länge des Inhalts der HTTP-Anfrage in Bytes zurück.
Dies entspricht dem angekündigten Content-Length-Header oder, bei Chunked-Kodierung, der Größe
der verfügbaren Daten.

<a id="entry-7-3-6-req-cook-string"></a>

**`req.cook([<name>]): string`**

```haproxy
req.cook([<name>]): string
cook([<name>]): string (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Cookie"-Headerzeile der
Anfrage und gibt dessen Wert als Zeichenfolge zurück. Ohne Namensangabe wird der Wert des ersten
Cookies zurückgegeben. In ACLs werden alle passenden Cookies ausgewertet. Leerzeichen um Namen
und Wert werden gemäß der Spezifikation des Cookie-Headers (RFC6265) ignoriert. Beim Cookie-Namen
wird zwischen Groß- und Kleinschreibung unterschieden. Leere Cookies sind gültig, sodass ein
vorhandenes leeres Cookie durchaus einen leeren Wert zurückgeben kann. Mit dem Vergleich "found"
lässt sich das Vorhandensein erkennen. Verwenden Sie für vom Server gesendete Antwort-Cookies
die Variante res.cook().

ACL-Varianten:

```text
req.cook([<name>])    : exakter Zeichenkettenabgleich
req.cook_beg([<name>]): Präfixabgleich
req.cook_dir([<name>]): Unterverzeichnisabgleich
req.cook_dom([<name>]): Domainabgleich
req.cook_end([<name>]): Suffixabgleich
req.cook_len([<name>]): Längenabgleich
req.cook_reg([<name>]): Abgleich mit regulären Ausdrücken
req.cook_sub([<name>]): Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

<a id="entry-7-3-6-req-cook-cnt-integer"></a>

**`req.cook_cnt([<name>]): integer`**

```haproxy
req.cook_cnt([<name>]): integer
cook_cnt([<name>]): integer (deprecated)
```

Gibt eine Ganzzahl zurück, die der Anzahl der Vorkommen des Cookies `<name>` in der Anfrage
entspricht, oder aller Cookies, wenn `<name>` nicht angegeben ist.

<a id="entry-7-3-6-req-cook-names-string"></a>

**`req.cook_names([<delim>]): string`**

```haproxy
req.cook_names([<delim>]): string
```

Bildet eine Zeichenfolge durch Verkettung aller Cookie-Namen, wie sie beim Auswerten der Regel
in der Anfrage im Cookie-Header erscheinen. Das Standardtrennzeichen ist das Komma (','); es kann
jedoch über das optionale Argument `<delim>` überschrieben werden. Dabei wird nur das erste
Zeichen von `<delim>` berücksichtigt.

<a id="entry-7-3-6-req-cook-val-integer"></a>

**`req.cook_val([<name>]): integer`**

```haproxy
req.cook_val([<name>]): integer
cook_val([<name>]): integer (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Cookie"-Headerzeile der
Anfrage, wandelt dessen Wert in eine Ganzzahl um und gibt sie zurück. Ohne Namensangabe wird der
Wert des ersten Cookies zurückgegeben. In ACLs werden alle passenden Namen durchlaufen, bis ein
Wert übereinstimmt.

<a id="entry-7-3-6-req-fhdr-string"></a>

**`req.fhdr(<name>[,<occ>]): string`**

```haproxy
req.fhdr(<name>[,<occ>]): string
```

Gibt den vollständigen Wert des letzten Vorkommens des Headers `<name>` in einer HTTP-Anfrage
zurück. Anders als bei req.hdr() werden im Wert vorhandene Kommata mit zurückgegeben und nicht
als Trennzeichen verwendet. Bei Headern wie User-Agent kann dies nützlich sein.

Bei Verwendung in einer ACL werden alle Vorkommen durchlaufen, bis eine Übereinstimmung gefunden
wird.

Optional kann ein bestimmtes Vorkommen durch eine Positionsnummer angegeben werden. Positive
Werte zählen vom ersten Vorkommen an, wobei 1 das erste bezeichnet. Negative Werte geben die
Position relativ zum letzten Vorkommen an, wobei -1 das letzte bezeichnet.

<a id="entry-7-3-6-req-fhdr-cnt-integer"></a>

**`req.fhdr_cnt([<name>]): integer`**

```haproxy
req.fhdr_cnt([<name>]): integer
```

Gibt eine Ganzzahl zurück, die der Anzahl der Vorkommen des Anfrageheader-Feldnamens `<name>`
entspricht, oder der Gesamtzahl der Headerfelder, wenn `<name>` nicht angegeben ist. Wie req.fhdr()
unterscheidet sich dies von res.hdr_cnt() dadurch, dass Header nicht an Kommata aufgeteilt werden.

<a id="entry-7-3-6-req-hdr-string"></a>

**`req.hdr([<name>[,<occ>]]): string`**

```haproxy
req.hdr([<name>[,<occ>]]): string
```

Gibt den letzten durch Kommata getrennten Wert des Headers `<name>` in einer HTTP-Anfrage zurück.
Diese Abrufmethode behandelt jedes Komma als Trennzeichen zwischen einzelnen Werten. Dies ist
nützlich zur Verarbeitung von Headern, die als Wertelisten definiert sind, etwa Accept oder
X-Forwarded-For. Wenn stattdessen vollständige Headerzeilen benötigt werden, verwenden Sie
req.fhdr(). Prüfen Sie sorgfältig in RFC 7231, wie bestimmte Header zu analysieren sind. Bei
einigen, beispielsweise Connection, wird außerdem nicht zwischen Groß- und Kleinschreibung
unterschieden.

Bei Verwendung in einer ACL werden alle Vorkommen durchlaufen, bis eine Übereinstimmung gefunden
wird.

Optional kann ein bestimmtes Vorkommen durch eine Positionsnummer angegeben werden. Positive
Werte zählen vom ersten Vorkommen an, wobei 1 das erste bezeichnet. Negative Werte geben die
Position relativ zum letzten Vorkommen an, wobei -1 das letzte bezeichnet.

Eine typische Anwendung ist der in eine IP-Adresse umgewandelte X-Forwarded-For-Header in
Verbindung mit einer Stick Table für IP-Adressen.

ACL-Varianten:

```text
hdr([<name>[,<occ>]])    : exakter Zeichenkettenabgleich
hdr_beg([<name>[,<occ>]]): Präfixabgleich
hdr_dir([<name>[,<occ>]]): Unterverzeichnisabgleich
hdr_dom([<name>[,<occ>]]): Domainabgleich
hdr_end([<name>[,<occ>]]): Suffixabgleich
hdr_len([<name>[,<occ>]]): Längenabgleich
hdr_reg([<name>[,<occ>]]): Abgleich mit regulären Ausdrücken
hdr_sub([<name>[,<occ>]]): Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

<a id="entry-7-3-6-req-hdr-cnt-integer"></a>

**`req.hdr_cnt([<name>]): integer`**

```haproxy
req.hdr_cnt([<name>]): integer
hdr_cnt([<header>]): integer (deprecated)
```

Gibt eine Ganzzahl zurück, die der Anzahl der Vorkommen des Anfrageheader-Feldnamens `<name>`
entspricht, oder der Gesamtzahl der Headerfeldwerte, wenn `<name>` nicht angegeben ist. Wie req.hdr()
zählt dies jeden durch Kommata getrennten Teil des Headerwerts. Sollen vollständige Headerzeilen
gezählt werden, ist stattdessen req.fhdr_cnt() zu verwenden.

In ACLs kann damit das Vorhandensein, Fehlen oder der Missbrauch eines bestimmten Headers erkannt
werden. Außerdem lassen sich Request-Smuggling-Angriffe abwehren, indem Anfragen mit mehreren
Vorkommen bestimmter Header abgewiesen werden.

Weitere Informationen zum Headervergleich finden Sie unter req.hdr().

<a id="entry-7-3-6-req-hdr-ip-ip"></a>

**`req.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
req.hdr_ip([<name>[,<occ>]]): ip
hdr_ip([<name>[,<occ>]]): ip (deprecated)
```

Extrahiert das letzte Vorkommen des Headers `<name>` in einer HTTP-Anfrage, wandelt es in eine
IPv4- oder IPv6-Adresse um und gibt diese zurück. In ACLs werden alle Vorkommen geprüft; wenn
`<name>` fehlt, wird jeder Wert jedes Headers geprüft. Der Parser hält sich strikt an das in
RFC7239 beschriebene Format, mit der Erweiterung, dass auf IPv4-Adressen optional ein Doppelpunkt
(':') und eine gültige dezimale Portnummer von 0 bis 65535 folgen dürfen. Die Portnummer wird
stillschweigend verworfen. Alle anderen Formen passen nicht und führen dazu, dass die Adresse
ignoriert wird.

Der Parameter `<occ>` wird wie bei req.hdr() verarbeitet.

Typische Anwendungen sind die Header X-Forwarded-For und X-Client-IP.

<a id="entry-7-3-6-req-hdr-names-string"></a>

**`req.hdr_names([<delim>]): string`**

```haproxy
req.hdr_names([<delim>]): string
```

Bildet eine Zeichenfolge durch Verkettung aller Headernamen, wie sie beim Auswerten der Regel in
der Anfrage erscheinen. Das Standardtrennzeichen ist das Komma (','); es kann jedoch über das
optionale Argument `<delim>` überschrieben werden. Dabei wird nur das erste Zeichen von `<delim>`
berücksichtigt.

<a id="entry-7-3-6-req-hdr-val-integer"></a>

**`req.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
req.hdr_val([<name>[,<occ>]]): integer
hdr_val([<name>[,<occ>]]): integer (deprecated)
```

Extrahiert das letzte Vorkommen des Headers `<name>` in einer HTTP-Anfrage und wandelt es in eine
Ganzzahl um. In ACLs werden alle Vorkommen geprüft; wenn `<name>` fehlt, wird jeder Wert jedes
Headers geprüft.

Der Parameter `<occ>` wird wie bei req.hdr() verarbeitet.

Eine typische Anwendung ist der Header X-Forwarded-For.

req.hdrs: string Gibt die aktuellen Anfrageheader als Zeichenfolge zurück, einschließlich der
abschließenden Leerzeile, die die Header vom Anfrageinhalt trennt. Anhand dieser Leerzeile lässt
sich ein abgeschnittener Headerblock erkennen. Dieser Sample-Abruf ist für bestimmte
SPOE-Headeranalysatoren und für erweiterte Protokollierung nützlich.

req.hdrs_bin: binary Gibt die aktuellen Anfrageheader in voranalysierter Binärform zurück. Damit
lässt sich ein Teil der Verarbeitung über SPOE auslagern. Jede Zeichenfolge wird durch eine
Längenangabe gefolgt von der darin angegebenen Anzahl Bytes beschrieben. Die Länge wird mit der
in der SPOE-Dokumentation beschriebenen variablen Ganzzahlkodierung dargestellt. Das Ende der Liste
wird durch ein Paar aus leerem Headernamen und leerem Wert markiert, beide mit der Länge 0.

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: Zur Kodierung siehe die SPOE-Dokumentation. str: ``` <int:length>``<bytes> ```

req.timer.hdr: integer Gesamtdauer bis zum Empfang der Client-Anfrage, nur im HTTP-Modus. Dies ist
die Zeit vom Empfang der ersten Bytes bis zum Empfang der Leerzeile, die das Ende der HTTP-Header
markiert, durch den Proxy. Sie wird in Millisekunden (ms) angegeben und entspricht %TR in
log-format. Einzelheiten finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

req.timer.idle: integer Leerlaufzeit vor der HTTP-Anfrage, nur im HTTP-Modus. Dieser Zeitgeber zählt
vom Ende der Handshakes bis zum ersten Byte der HTTP-Anfrage. Der Wert wird in Millisekunden
angegeben und entspricht %Ti in log-format. Einzelheiten finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4)
„Zeitereignisse“.

req.timer.queue: integer Gesamtdauer in den Warteschlangen beim Warten auf einen Verbindungsplatz.
Sie wird in Millisekunden angegeben und entspricht %Tw in log-format. Einzelheiten finden Sie in
[Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

req.timer.tq: integer Gesamtdauer bis zum Empfang der Client-Anfrage ab dem Annahmezeitpunkt oder
seit dem Senden des letzten Bytes der vorherigen Antwort. Sie wird in Millisekunden angegeben und
entspricht %Tq in log-format. Einzelheiten finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4)
„Zeitereignisse“.

req.ver: string req_ver: string (veraltet) Gibt die Versionszeichenfolge aus der HTTP-Anfrage im
Format "`<major>`.`<minor>`" zurück. Dies kann für ACL nützlich sein. Einige vordefinierte ACL prüfen
bereits gängige Versionen. Da die Information dauerhaft gespeichert ist, kann sie sowohl in
Anfragen und Antworten als auch in Protokolleinträgen verwendet werden. Ist die Version der Anfrage
ungültig, schlägt dieser Sample-Abruf fehl.

Gängige Werte sind "1.0", "1.1", "2.0" oder "3.0".

ACL-Varianten:

```text
req.ver: exakter Zeichenkettenabgleich
```

<a id="entry-7-3-6-request-date-integer"></a>

**`request_date([<unit>]): integer`**

```haproxy
request_date([<unit>]): integer
```

Dies ist der genaue Zeitpunkt, zu dem HAProxy das erste Byte der HTTP-Anfrage empfangen hat
(log-format-Alias %tr). Er wird aus accept_date + Handshake-Dauer (%Th) + Leerlaufzeit (%Ti)
berechnet.

Gibt die Anzahl der Sekunden seit der Unix-Epoche zurück.

`<unit>` ist optional und kann auf "s" für Sekunden (Standardverhalten), "ms" für Millisekunden
oder "us" für Mikrosekunden gesetzt werden. Bei angegebener Einheit ist der Rückgabewert eine
Ganzzahl, die die Sekunden, Millisekunden oder Mikrosekunden seit der Unix-Epoche angibt. Dies ist
nützlich, wenn eine Zeitauflösung von weniger als einer Sekunde benötigt wird.

res.body: binary Gibt den verfügbaren Inhalt der HTTP-Antwort als Datenblock zurück. Anders als
auf der Anfrageseite gibt es keine Direktive, um auf den Antwortinhalt zu warten. Dieser
Sample-Abruf ist im Kontext von Health Checks besonders nützlich und verwendbar.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

res.body_len: integer Gibt die Länge des verfügbaren Inhalts der HTTP-Antwort in Bytes zurück.
Anders als auf der Anfrageseite gibt es keine Direktive, um auf den Antwortinhalt zu warten.
Dieser Sample-Abruf ist im Kontext von Health Checks besonders nützlich und verwendbar.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

res.body_size: integer Gibt die angekündigte Länge des Inhalts der HTTP-Antwort in Bytes zurück.
Dies entspricht dem angekündigten Content-Length-Header oder, bei Chunked-Kodierung, der Größe
der verfügbaren Daten. Anders als auf der Anfrageseite gibt es keine Direktive, um auf den
Antwortinhalt zu warten. Dieser Sample-Abruf ist im Kontext von Health Checks besonders
nützlich und verwendbar.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

res.cache_hit: boolean Gibt den booleschen Wert "true" zurück, wenn die Antwort aus einem
HTTP-Cache-Eintrag erstellt wurde, andernfalls den booleschen Wert "false".

res.cache_name: string Gibt eine Zeichenfolge mit dem Namen des HTTP-Caches zurück, aus dem die
HTTP-Antwort erstellt wurde, wenn res.cache_hit true ist; andernfalls eine leere Zeichenfolge.

res.comp: boolean Gibt den booleschen Wert "true" zurück, wenn HAProxy die Antwort komprimiert
hat, andernfalls den booleschen Wert "false". Damit können zusätzliche Informationen in die
Protokolleinträge aufgenommen werden.

res.comp_algo: string Gibt eine Zeichenfolge mit dem Namen des verwendeten Algorithmus zurück, wenn
HAProxy die Antwort komprimiert hat, beispielsweise "deflate". Damit können zusätzliche
Informationen in die Protokolleinträge aufgenommen werden.

<a id="entry-7-3-6-res-cook-string"></a>

**`res.cook([<name>]): string`**

```haproxy
res.cook([<name>]): string
scook([<name>]): string (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Set-Cookie"-Headerzeile der
Antwort und gibt dessen Wert als Zeichenfolge zurück. Ohne Namensangabe wird der Wert des ersten
Cookies zurückgegeben.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

ACL-Varianten:

```text
res.scook([<name>]: exakter Zeichenkettenabgleich
```

<a id="entry-7-3-6-res-cook-cnt-integer"></a>

**`res.cook_cnt([<name>]): integer`**

```haproxy
res.cook_cnt([<name>]): integer
scook_cnt([<name>]): integer (deprecated)
```

Gibt eine Ganzzahl zurück, die der Anzahl der Vorkommen des Cookies `<name>` in der Antwort
entspricht, oder aller Cookies, wenn `<name>` nicht angegeben ist. Dies ist vor allem zusammen
mit ACLs nützlich, um verdächtige Antworten zu erkennen.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-cook-names-string"></a>

**`res.cook_names([<delim>]): string`**

```haproxy
res.cook_names([<delim>]): string
```

Bildet eine Zeichenfolge durch Verkettung aller Cookie-Namen, wie sie beim Auswerten der Regel
in der Antwort in den Set-Cookie-Headern erscheinen. Das Standardtrennzeichen ist das Komma (',');
es kann jedoch über das optionale Argument `<delim>` überschrieben werden. Dabei wird nur das
erste Zeichen von `<delim>` berücksichtigt.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-cook-val-integer"></a>

**`res.cook_val([<name>]): integer`**

```haproxy
res.cook_val([<name>]): integer
scook_val([<name>]): integer (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Set-Cookie"-Headerzeile der
Antwort, wandelt dessen Wert in eine Ganzzahl um und gibt sie zurück. Ohne Namensangabe wird der
Wert des ersten Cookies zurückgegeben.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-fhdr-string"></a>

**`res.fhdr([<name>[,<occ>]]): string`**

```haproxy
res.fhdr([<name>[,<occ>]]): string
```

Diese Abrufmethode funktioniert wie req.fhdr(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Wie req.fhdr() gibt die Abrufmethode res.fhdr() vollständige Werte zurück. Wenn der Header als
Liste definiert ist, sollten Sie res.hdr() verwenden.

Diese Abrufmethode ist mitunter für Header wie Date oder Expires nützlich.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-fhdr-cnt-integer"></a>

**`res.fhdr_cnt([<name>]): integer`**

```haproxy
res.fhdr_cnt([<name>]): integer
```

Diese Abrufmethode funktioniert wie req.fhdr_cnt(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Wie req.fhdr_cnt() arbeitet die Abrufmethode res.fhdr_cnt() mit vollständigen Werten. Wenn der
Header als Liste definiert ist, sollten Sie res.hdr_cnt() verwenden.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-hdr-string"></a>

**`res.hdr([<name>[,<occ>]]): string`**

```haproxy
res.hdr([<name>[,<occ>]]): string
shdr([<name>[,<occ>]]): string (deprecated)
```

Diese Abrufmethode funktioniert wie req.hdr(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Wie req.hdr() betrachtet die Abrufmethode res.hdr() das Komma als Trennzeichen. Ist dies nicht
gewünscht, sollte res.fhdr() verwendet werden.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

ACL-Varianten:

```text
res.hdr([<name>[,<occ>]])    : exakter Zeichenkettenabgleich
res.hdr_beg([<name>[,<occ>]]): Präfixabgleich
res.hdr_dir([<name>[,<occ>]]): Unterverzeichnisabgleich
res.hdr_dom([<name>[,<occ>]]): Domainabgleich
res.hdr_end([<name>[,<occ>]]): Suffixabgleich
res.hdr_len([<name>[,<occ>]]): Längenabgleich
res.hdr_reg([<name>[,<occ>]]): Abgleich mit regulären Ausdrücken
res.hdr_sub([<name>[,<occ>]]): Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

<a id="entry-7-3-6-res-hdr-cnt-integer"></a>

**`res.hdr_cnt([<name>]): integer`**

```haproxy
res.hdr_cnt([<name>]): integer
shdr_cnt([<name>]): integer (deprecated)
```

Diese Abrufmethode funktioniert wie req.hdr_cnt(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Wie req.hdr_cnt() betrachtet die Abrufmethode res.hdr_cnt() das Komma als Trennzeichen. Ist dies
nicht gewünscht, sollte res.fhdr_cnt() verwendet werden.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-hdr-ip-ip"></a>

**`res.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
res.hdr_ip([<name>[,<occ>]]): ip
shdr_ip([<name>[,<occ>]]): ip (deprecated)
```

Diese Abrufmethode funktioniert wie req.hdr_ip(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Dies kann nützlich sein, um Daten in eine Stick Table zu übernehmen.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-hdr-names-string"></a>

**`res.hdr_names([<delim>]): string`**

```haproxy
res.hdr_names([<delim>]): string
```

Bildet eine Zeichenfolge durch Verkettung aller Headernamen, wie sie beim Auswerten der Regel in
der Antwort erscheinen. Das Standardtrennzeichen ist das Komma (','); es kann jedoch über das
optionale Argument `<delim>` überschrieben werden. Dabei wird nur das erste Zeichen von `<delim>`
berücksichtigt.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

<a id="entry-7-3-6-res-hdr-val-integer"></a>

**`res.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
res.hdr_val([<name>[,<occ>]]): integer
shdr_val([<name>[,<occ>]]): integer (deprecated)
```

Diese Abrufmethode funktioniert wie req.hdr_val(), arbeitet jedoch mit den Headern einer
HTTP-Antwort.

Dies kann nützlich sein, um Daten in eine Stick Table zu übernehmen.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

res.hdrs: string Gibt die aktuellen Antwortheader als Zeichenfolge zurück, einschließlich der
abschließenden Leerzeile, die die Header vom Anfrageinhalt trennt. Anhand dieser Leerzeile lässt
sich ein abgeschnittener Headerblock erkennen. Dieser Sample-Abruf ist für bestimmte
SPOE-Headeranalysatoren und für erweiterte Protokollierung nützlich.

Dies kann auch in expect-Regeln auf Basis von tcp-check verwendet werden.

res.hdrs_bin: binary Gibt die aktuellen Antwortheader in voranalysierter Binärform zurück. Damit
lässt sich ein Teil der Verarbeitung über SPOE auslagern. Dies kann in expect-Regeln auf Basis
von tcp-check verwendet werden. Jede Zeichenfolge wird durch eine Längenangabe gefolgt von der
darin angegebenen Anzahl Bytes beschrieben. Die Länge wird mit der in der SPOE-Dokumentation
beschriebenen variablen Ganzzahlkodierung dargestellt. Das Ende der Liste wird durch ein Paar aus
leerem Headernamen und leerem Wert markiert, beide mit der Länge 0.

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: Zur Kodierung siehe die SPOE-Dokumentation. str: ``` <int:length>``<bytes> ```

res.timer.hdr: integer Zeit vom Aufbau der TCP-Verbindung zum Server bis zum Senden seiner
vollständigen Antwortheader. Sie wird in Millisekunden angegeben und entspricht %Tr in log-format.
Einzelheiten finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

res.ver: string resp_ver: string (veraltet) Gibt die Versionszeichenfolge aus der HTTP-Antwort im
Format "`<major>`.`<minor>`" zurück. Dies kann für Protokolleinträge nützlich sein, ist aber
hauptsächlich für ACL vorgesehen. Ist die Version der Antwort ungültig, schlägt dieser
Sample-Abruf fehl.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

ACL-Varianten:

```text
resp.ver: exakter Zeichenkettenabgleich
```

server_status: integer Gibt eine Ganzzahl mit dem vom Server empfangenen HTTP-Statuscode zurück.
Wenn keine Antwort vom Server empfangen wurde, schlägt der Sample-Abruf fehl.

<a id="entry-7-3-6-set-cookie-string"></a>

**`set-cookie([<name>]): string (deprecated)`**

```haproxy
set-cookie([<name>]): string (deprecated)
```

Extrahiert das letzte Vorkommen des Cookie-Namens `<name>` aus einer "Set-Cookie"-Headerzeile der
Antwort und verwendet den zugehörigen Wert für den Vergleich. Dies ist mit der früheren Funktion
von "appsession" mit Standardoptionen vergleichbar, unterstützt aber die Synchronisierung zwischen
mehreren Peers und die Erhaltung des Zustands über Neustarts hinweg.

Diese Abruffunktion ist veraltet und wurde durch die Abrufmethode "res.cook" ersetzt. Dieses
Schlüsselwort wird in Kürze entfernt.

status: integer Gibt eine Ganzzahl mit dem HTTP-Statuscode der HTTP-Antwort zurück, beispielsweise 302. Dies wird hauptsächlich in ACLs und mit Ganzzahlbereichen verwendet, etwa um jeglichen
Location-Header zu entfernen, wenn die Antwort kein 3xx-Status ist. Dies ist der vom Client
empfangene Statuscode, sofern er nicht geändert wird, beispielsweise durch eine Aktion 'set-status'.

Dies kann in expect-Regeln auf Basis von tcp-check verwendet werden.

txn.status: integer Gibt eine Ganzzahl mit dem HTTP-Statuscode der Transaktion zurück, wie er im
Protokoll angegeben wird.

txn.timer.total: integer Gesamte aktive Zeit für die HTTP-Anfrage vom Empfang des ersten Bytes des
Anfrageheaders durch den Proxy bis zum Senden des letzten Bytes des Antwortinhalts. Dies
entspricht %Ta in log-format und wird in Millisekunden (ms) angegeben. Weitere Informationen
finden Sie in [Abschnitt 8.4](/de/haproxy/configuration-logging/#section-8-4) „Zeitereignisse“.

unique-id: string Gibt die der Anfrage zugeordnete unique-id zurück. Die Direktive "unique-id-format"
muss gesetzt sein; andernfalls schlägt der Sample-Abruf unique-id fehl. Die unique-id wird zwar
üblicherweise mit HTTP-Anfragen verwendet, diese Abrufmethode kann jedoch auch mit anderen
Protokollen verwendet werden. Bei anderen Protokollen als HTTP darf die Direktive unique-id-format
selbstverständlich keine HTTP-Bestandteile enthalten. Siehe: unique-id-format und unique-id-header.

url: string Extrahiert die URL der Anfrage in der darin vorliegenden Form. Typische Anwendungen sind
Caches mit Vorabrufunterstützung sowie Portale, die mehrere Informationen aus Datenbanken
zusammenführen und in Caches vorhalten müssen. In ACLs ist "path" gegenüber "url" vorzuziehen,
da Clients eine vollständige URL senden können, wie dies bei Proxys üblich ist. Der einzig
wirkliche Anwendungsfall ist der Vergleich mit "\*", das in "path" nicht passt und für das
bereits eine vordefinierte ACL existiert. Siehe auch "path" und "base". Beachten Sie, dass der
HTTP-Standard jeglichen Fragmentverweis in der URI ('#' nach dem Pfad) strikt verbietet und dieser
daher abgewiesen wird. Hat das Frontend, das die Anfrage empfängt, jedoch
"option accept-unsafe-violations-in-http-request" gesetzt, wird dieser Fragmentteil akzeptiert
und erscheint auch in der URL.

ACL-Varianten:

```text
url    : exakter Zeichenkettenabgleich
url_beg: Präfixabgleich
url_dir: Unterverzeichnisabgleich
url_dom: Domainabgleich
url_end: Suffixabgleich
url_len: Längenabgleich
url_reg: Abgleich mit regulären Ausdrücken
url_sub: Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

url32: integer Gibt einen 32-Bit-Hash des Werts zurück, der durch Verkettung des ersten Host-Headers
mit der gesamten URL einschließlich der Parameter entsteht, also nicht nur mit dem Pfadteil der
Anfrage wie beim oben beschriebenen Abruf "base32". Dies ist nützlich, um die Aktivität je URL zu
verfolgen. Gespeichert wird ein kürzerer Hash, was viel Speicher spart. Der Ausgabetyp ist eine
vorzeichenlose Ganzzahl.

url32+src: binary Gibt die Verkettung der Abrufmethoden "url32" und "src" zurück. Das Ergebnis ist
vom Typ binary und je nach Adressfamilie der Quelladresse 8 oder 20 Bytes groß. Damit lassen sich
Zähler je IP und je URL führen.

url_ip: ip Extrahiert die IP-Adresse aus der URL der Anfrage, wenn der Hostteil als IP-Adresse angegeben ist. Ist der Hostteil ein Name, schlägt der Abruf fehl, da keine Namensauflösung erfolgt. Die Verwendung ist sehr eingeschränkt. Beispielsweise kann ein Überwachungssystem dieses Feld anstelle der Quell-IP verwenden, um zu testen, welchen Pfad eine bestimmte Quelladresse nehmen würde, oder um einen Eintrag in einer Tabelle für eine bestimmte Quelladresse zu erzwingen. Es kann zusammen mit 'http-request set-dst' verwendet werden, um das frühere 'option http_proxy' nachzubilden.

url_port: integer Extrahiert den Portteil aus der URL der Anfrage. Wenn in der Anfrage kein Port angegeben ist, wird Port 80 angenommen. Wie bei "url_ip" funktioniert dies nur, wenn der Authority-Teil der URL als Adresse angegeben ist. Bei einem Hostnamen schlägt der Abruf fehl, da hier keine Namensauflösung erfolgt.

<a id="entry-7-3-6-urlp-string"></a>

**`urlp([<name>[,<delim>[,i]]]): string`**

```haproxy
urlp([<name>[,<delim>[,i]]]): string
url_param([<name>[,<delim>[,i]]]): string
```

Extrahiert das erste Vorkommen des Parameters `<name>` aus der Abfragezeichenfolge, die nach '?'
oder `<delim>` beginnt und vor '&', ';' oder `<delim>` endet. Beim Parameternamen wird zwischen
Groß- und Kleinschreibung unterschieden, sofern nicht "i" als drittes Argument angegeben ist.
Ohne Namensangabe passt jeder Parameter, und der erste wird zurückgegeben. Das Ergebnis ist eine
Zeichenfolge mit dem Wert des Parameters `<name>` in seiner Darstellung in der Anfrage; eine
URL-Dekodierung erfolgt nicht. Dies kann zur Sitzungsbindung anhand einer Client-ID, zum
Extrahieren eines als URL-Parameter übergebenen Anwendungscookies oder für Prüfungen in ACLs
verwendet werden. Beachten Sie, dass die ACL-Variante dieser Abrufmethode mehrere Parameter
durchläuft und ohne Namensangabe nacheinander alle Parameterwerte liefert.

ACL-Varianten:

```text
urlp(<name>[,<delim>])    : exakter Zeichenkettenabgleich
urlp_beg(<name>[,<delim>]): Präfixabgleich
urlp_dir(<name>[,<delim>]): Unterverzeichnisabgleich
urlp_dom(<name>[,<delim>]): Domainabgleich
urlp_end(<name>[,<delim>]): Suffixabgleich
urlp_len(<name>[,<delim>]): Längenabgleich
urlp_reg(<name>[,<delim>]): Abgleich mit regulären Ausdrücken
urlp_sub(<name>[,<delim>]): Teilzeichenkettenabgleich
```

Hinweis: Auf ACL-Varianten darf kein Konverter folgen; sie dürfen auch nicht in ACLs mit einer
Mustervergleichsmethode "-m" verwendet werden.

Beispiel:

```shell
# match http://example.com/foo?PHPSESSIONID=some_id
stick on urlp(PHPSESSIONID)
# match http://example.com/foo;JSESSIONID=some_id
stick on urlp(JSESSIONID,;)
```

<a id="entry-7-3-6-urlp-val-integer"></a>

**`urlp_val([<name>[,<delim>[,i]]]): integer`**

```haproxy
urlp_val([<name>[,<delim>[,i]]]): integer
```

Siehe "urlp" oben. Diese Variante extrahiert den URL-Parameter `<name>` aus der Anfrage und wandelt
ihn in eine Ganzzahl um. Dies kann beispielsweise zur Sitzungsbindung anhand einer Benutzer-ID
oder in ACLs zum Vergleich einer Seitennummer oder eines Preises verwendet werden.

### 7.3.7. Sample-Abruf für Entwickler {#section-7-3-7}

Diese Methoden zum Sample-Abruf sind Entwicklern vorbehalten und dürfen niemals in einer
Produktionsumgebung verwendet werden, außer auf Anforderung eines Entwicklers zur Fehlersuche.
Außerdem wird keine besondere Rücksicht auf Abwärtskompatibilität genommen. Es gibt keine
Garantie, dass die folgenden Abrufmethoden nicht geändert, umbenannt oder einfach entfernt werden.
Seien Sie daher besonders vorsichtig, falls Sie eine davon verwenden müssen. Um Mehrdeutigkeiten
zu vermeiden, liegen diese Methoden im eigenen Namensbereich "internal", beispielsweise
"internal.strm.is_htx".

Übersicht der Methoden zum Sample-Abruf in diesem Abschnitt und ihrer jeweiligen Typen:

```text
  Schlüsselwort                                    Ausgabetyp
-------------------------------------------------+-------------
internal.htx.data                                  integer
internal.htx.free                                  integer
internal.htx.free_data                             integer
internal.htx.has_eom                               boolean
internal.htx.nbblks                                integer
internal.htx.size                                  integer
internal.htx.used                                  integer
internal.htx_blk.size(<idx>)                       integer
internal.htx_blk.type(<idx>)                       string
internal.htx_blk.data(<idx>)                       binary
internal.htx_blk.hdrname(<idx>)                    string
internal.htx_blk.hdrval(<idx>)                     string
internal.htx_blk.start_line(<idx>)                 string
internal.strm.is_htx                               boolean
-------------------------------------------------+-------------
```

Ausführliche Liste:

internal.htx.data: integer Gibt die Größe in Bytes zurück, die die Daten in der einem Kanal
zugeordneten HTX-Nachricht belegen. Der Kanal wird anhand der Sample-Richtung ausgewählt.

internal.htx.free: integer Gibt den freien Platz (size - used) in Bytes in der einem Kanal
zugeordneten HTX-Nachricht zurück. Der Kanal wird anhand der Sample-Richtung ausgewählt.

internal.htx.free_data: integer Gibt den freien Platz für Daten in Bytes in der einem Kanal
zugeordneten HTX-Nachricht zurück. Der Kanal wird anhand der Sample-Richtung ausgewählt.

internal.htx.has_eom: boolean Gibt true zurück, wenn die einem Kanal zugeordnete HTX-Nachricht das
Flag für das Nachrichtenende (EOM) enthält, andernfalls false. Der Kanal wird anhand der
Sample-Richtung ausgewählt.

internal.htx.nbblks: integer Gibt die Anzahl der Blöcke in der einem Kanal zugeordneten HTX-Nachricht
zurück. Der Kanal wird anhand der Sample-Richtung ausgewählt.

internal.htx.size: integer Gibt die Gesamtgröße in Bytes der einem Kanal zugeordneten HTX-Nachricht
zurück. Der Kanal wird anhand der Sample-Richtung ausgewählt.

internal.htx.used: integer Gibt die insgesamt belegte Größe in Bytes (Daten + Metadaten) in der einem
Kanal zugeordneten HTX-Nachricht zurück. Der Kanal wird anhand der Sample-Richtung ausgewählt.

<a id="entry-7-3-7-internal-htx-blk-size-integer"></a>

**`internal.htx_blk.size(<idx>): integer`**

```haproxy
internal.htx_blk.size(<idx>): integer
```

Gibt die Größe des Blocks an Position `<idx>` in der einem Kanal zugeordneten HTX-Nachricht zurück,
oder 0, wenn er nicht existiert. Der Kanal wird anhand der Sample-Richtung ausgewählt. `<idx>` kann
eine beliebige positive Ganzzahl oder einer der folgenden Sonderwerte sein: \* head : Der älteste
eingefügte Block \* tail : Der zuletzt eingefügte Block \* first: Der erste Block, bei dem die Analyse
(neu) beginnen soll.

<a id="entry-7-3-7-internal-htx-blk-type-string"></a>

**`internal.htx_blk.type(<idx>): string`**

```haproxy
internal.htx_blk.type(<idx>): string
```

Gibt den Typ des Blocks an Position `<idx>` in der einem Kanal zugeordneten HTX-Nachricht zurück,
oder "HTX_BLK_UNUSED", wenn er nicht existiert. Der Kanal wird anhand der Sample-Richtung
ausgewählt. `<idx>` kann eine beliebige positive Ganzzahl oder einer der folgenden Sonderwerte sein:
\* head : Der älteste eingefügte Block \* tail : Der zuletzt eingefügte Block \* first: Der erste Block,
bei dem die Analyse (neu) beginnen soll.

<a id="entry-7-3-7-internal-htx-blk-data-binary"></a>

**`internal.htx_blk.data(<idx>): binary`**

```haproxy
internal.htx_blk.data(<idx>): binary
```

Gibt den Wert des DATA-Blocks an Position `<idx>` in der einem Kanal zugeordneten HTX-Nachricht
zurück, oder eine leere Zeichenfolge, wenn er nicht existiert oder kein DATA-Block ist. Der Kanal
wird anhand der Sample-Richtung ausgewählt. `<idx>` kann eine beliebige positive Ganzzahl oder
einer der folgenden Sonderwerte sein:

    * head : Der älteste eingefügte Block
    * tail : Der zuletzt eingefügte Block
    * first: Der erste Block, bei dem die Analyse (neu) beginnen soll

<a id="entry-7-3-7-internal-htx-blk-hdrname-string"></a>

**`internal.htx_blk.hdrname(<idx>): string`**

```haproxy
internal.htx_blk.hdrname(<idx>): string
```

Gibt den Headernamen des HEADER-Blocks an Position `<idx>` in der einem Kanal zugeordneten
HTX-Nachricht zurück, oder eine leere Zeichenfolge, wenn er nicht existiert oder kein HEADER-Block
ist. Der Kanal wird anhand der Sample-Richtung ausgewählt. `<idx>` kann eine beliebige positive
Ganzzahl oder einer der folgenden Sonderwerte sein:

    * head : Der älteste eingefügte Block
    * tail : Der zuletzt eingefügte Block
    * first: Der erste Block, bei dem die Analyse (neu) beginnen soll

<a id="entry-7-3-7-internal-htx-blk-hdrval-string"></a>

**`internal.htx_blk.hdrval(<idx>): string`**

```haproxy
internal.htx_blk.hdrval(<idx>): string
```

Gibt den Headerwert des HEADER-Blocks an Position `<idx>` in der einem Kanal zugeordneten
HTX-Nachricht zurück, oder eine leere Zeichenfolge, wenn er nicht existiert oder kein HEADER-Block
ist. Der Kanal wird anhand der Sample-Richtung ausgewählt. `<idx>` kann eine beliebige positive
Ganzzahl oder einer der folgenden Sonderwerte sein:

    * head : Der älteste eingefügte Block
    * tail : Der zuletzt eingefügte Block
    * first: Der erste Block, bei dem die Analyse (neu) beginnen soll

<a id="entry-7-3-7-internal-htx-blk-start-line-string"></a>

**`internal.htx_blk.start_line(<idx>): string`**

```haproxy
internal.htx_blk.start_line(<idx>): string
```

Gibt den Wert des REQ_SL- oder RES_SL-Blocks an Position `<idx>` in der einem Kanal zugeordneten
HTX-Nachricht zurück, oder eine leere Zeichenfolge, wenn er nicht existiert oder kein SL-Block
ist. Der Kanal wird anhand der Sample-Richtung ausgewählt. `<idx>` kann eine beliebige positive
Ganzzahl oder einer der folgenden Sonderwerte sein:

    * head : Der älteste eingefügte Block
    * tail : Der zuletzt eingefügte Block
    * first: Der erste Block, bei dem die Analyse (neu) beginnen soll

internal.strm.is_htx: boolean Gibt true zurück, wenn der aktuelle Datenstrom ein HTX-Datenstrom ist.
Das bedeutet, dass die Daten in den Kanalpuffern in der internen HTX-Darstellung gespeichert sind.
Andernfalls wird false zurückgegeben.

## 7.4. Vordefinierte ACLs {#section-7-4}

Einige vordefinierte ACLs sind fest einprogrammiert, damit sie nicht in jedem Frontend deklariert
werden müssen, das sie benötigt. Zur Vermeidung von Verwechslungen sind ihre Namen durchgehend
großgeschrieben. Die entsprechenden Ausdrücke sind nachfolgend aufgeführt.

```text
ACL-Name         Entspricht                         Verwendung
---------------+----------------------------------+------------------------------------------------------
FALSE            always_false                       niemals zutreffen
HTTP             req.proto_http                     zutreffen, wenn das Anfrageprotokoll gültiges HTTP ist
HTTP_1.0         req.ver 1.0                        zutreffen, wenn die HTTP-Version der Anfrage gleich 1.0 ist
HTTP_1.1         req.ver 1.1                        zutreffen, wenn die HTTP-Version der Anfrage gleich 1.1 ist
HTTP_2.0         req.ver 2.0                        zutreffen, wenn die HTTP-Version der Anfrage gleich 2.0 ist
HTTP_3.0         req.ver 3.0                        zutreffen, wenn die HTTP-Version der Anfrage gleich 3.0 ist
HTTP_CONTENT     req.hdr_val(content-length) gt 0   auf einen vorhandenen content-length-Wert in der HTTP-Anfrage prüfen
HTTP_URL_ABS     url_reg ^[^/:]*://                 auf absolute URL mit Schema prüfen
HTTP_URL_SLASH   url_beg /                          auf URL prüfen, die mit "/" beginnt
HTTP_URL_STAR    url     *                          auf URL prüfen, die "*" entspricht
LOCALHOST        src 127.0.0.1/8::1                auf Verbindung vom lokalen Host prüfen
METH_CONNECT     method  CONNECT                    auf HTTP-Methode CONNECT prüfen
METH_DELETE      method  DELETE                     auf HTTP-Methode DELETE prüfen
METH_GET         method  GET HEAD                   auf HTTP-Methode GET oder HEAD prüfen
METH_HEAD        method  HEAD                       auf HTTP-Methode HEAD prüfen
METH_OPTIONS     method  OPTIONS                    auf HTTP-Methode OPTIONS prüfen
METH_POST        method  POST                       auf HTTP-Methode POST prüfen
METH_PUT         method  PUT                        auf HTTP-Methode PUT prüfen
METH_TRACE       method  TRACE                      auf HTTP-Methode TRACE prüfen
RDP_COOKIE       req.rdp_cookie_cnt gt 0            auf Vorhandensein eines RDP-Cookies im Anfragepuffer prüfen
REQ_CONTENT      req.len gt 0                       auf Daten im Anfragepuffer prüfen
TRUE             always_true                        immer zutreffen
WAIT_END         wait_end                           auf das Ende der Inhaltsanalyse warten
---------------+----------------------------------+------------------------------------------------------
```
