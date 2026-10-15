---
title: "Versionshinweise"
linkTitle: "Versionen"
weight: 60
description: "Versionsgeschichte von pgBackRest mit ausführlichem Änderungsprotokoll für jede Version."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## Einleitung {#introduction}

pgBackRest-Versionsnummern bestehen aus zwei Teilen: Haupt- und Nebenversion. Eine Hauptversion *kann* die Kompatibilität mit der vorherigen Hauptversion aufheben. Die Versionen der Reihe v2 sind jedoch vollständig mit v1-Repositorys kompatibel und akzeptieren alle v1-Optionen. Nebenversionen können Fehlerbehebungen und neue Funktionen enthalten, ändern aber das Repository-Format nicht und vermeiden nach Möglichkeit Änderungen an Optionen und Benennungen. Die Dokumentation für v1 ist [hier](https://pgbackrest.org/1) verfügbar. Die Versionshinweise können auch „Zusätzliche Hinweise“ enthalten. Änderungen in diesem Abschnitt betreffen jedoch ausschließlich die Dokumentation oder die Testsuite und haben keine direkten Auswirkungen auf die Codebasis von pgBackRest.


--------

## Dokumentierte stabile Version {#current-stable-release}

Diese Spiegelung dokumentiert v2.59.3. Neuere Versionen sind in der [Versionsgeschichte des Originalprojekts](https://pgbackrest.org/release.html) aufgeführt.

### v2.59.3 – Versionshinweise {#v2593-release-notes}

*Fehler bei schwachen Verschlüsselungsunterschlüsseln*

*Veröffentlicht am 4. Oktober 2026*

**WICHTIGER HINWEIS**: In früheren Versionen konnten bei einem Fehler beim Zugriff auf die Zufallsdaten des Systems schwache Verschlüsselungsunterschlüssel und Salts erzeugt werden. Weitere Informationen finden Sie unter [Schwache Unterschlüssel und Salts bei der Verschlüsselung](/de/pgbackrest/news/#weak-encryption).

**Fehlerbehebungen:**

- Möglichen Prüfsummenfehler beim Laden verschlüsselter Informationsdateien und Manifeste behoben. (*Behoben von j0uinim. Geprüft von David Steele.*)
- Mögliche Erzeugung schwacher Verschlüsselungsunterschlüssel oder Salts behoben. (*Behoben von j0uinim. Geprüft von David Steele, Stefan Fercot, Douglas J Hunley.*)


--------

## Stabile Versionen {#stable-releases}


### v2.59.2 – Versionshinweise {#v2592-release-notes}

*Unterstützung für PostgreSQL 19beta4*

*Veröffentlicht am 27. September 2026*

**Fehlerbehebungen:**

- Fehler bei einer leeren Blockzuordnung behoben, wenn eine Datei während des Backups auf die Länge null gekürzt wird. (*Geprüft von Douglas J Hunley. Gemeldet von JPCOSTA78.*)
- Wiederholungen von Lesevorgängen deaktiviert, wenn Filter an den Treiber übergeben werden. (*Geprüft von Douglas J Hunley. Gemeldet von megamaced.*)
- Seitenweises Auflisten von S3-Versionen korrigiert. (*Geprüft von Douglas J Hunley, guruguruguru. Gemeldet von guruguruguru.*)
- Azure-Versionsheader für die SAS-Authentifizierung gesetzt. (*Geprüft von Douglas J Hunley. Gemeldet von Florian Helmberger.*)
- Hängenbleiben des asynchronen `archive-push` an einer Backup-Historiendatei mit der Größe null behoben. (*Behoben von Andrew Kroh. Geprüft von David Steele, Douglas J Hunley.*)
- Befehl `annotate` auf einem entfernten verschlüsselten Repository korrigiert. (*Behoben von Douglas J Hunley. Geprüft von David Steele.*)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta4.



### v2.59.1 – Versionshinweise {#v2591-release-notes}

*Unterstützung für PostgreSQL 19beta3*

*Veröffentlicht am 17. August 2026*

**Fehlerbehebungen:**

- Hängenbleiben behoben, wenn der Chunk-Puffer kleiner als der Eingabepuffer ist. (*Geprüft von Andrew Pogrebnoi, Douglas J Hunley. Gemeldet von crajac66.*)
- Neue Backup-Kennzeichnung nur mit ihrem eigenen vollständigen Backup-Satz verglichen. (*Geprüft von Douglas J Hunley. Gemeldet von Anton Glushakov.*)
- Von GitHub erzeugte Quellcodearchive korrigiert, in denen für den Build erforderliche Dateien fehlten. (*Gemeldet von aardvarkzed.*)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta3. (*Beigetragen von Lardière Sébastien. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Ausnahme für Punkte in S3-Bucket-Namen bei `repo-s3-uri-style=path` dokumentiert.
- Explizite Konfiguration von `hot_standby` aus dem Benutzerhandbuch entfernt.


### v2.59.0 – Versionshinweise {#v2590-release-notes}

*Unterstützung für PostgreSQL 19beta2*

*Veröffentlicht am 20. Juli 2026*

**HINWEIS FÜR PAKETBETREUER**: Ein neuer Distributions-Tarball vereinfacht den Build, indem er vorgenerierte HTML-Dokumentation, eine Manpage und Code bereitstellt. Der Tarball ist jeder Veröffentlichung als Datei mit dem Namen `pgbackrest-{version}.tar.gz` beigefügt. Einzelheiten stehen in der `README.md` im Tarball. Bitte verwenden Sie den neuen Distributions-Tarball, um die zusätzlichen Build-Werkzeuge zu vermeiden, die in künftigen Versionen zur Codegenerierung erforderlich sein werden. Weitere Informationen stehen unter [Neuer Distributions-Tarball](/de/pgbackrest/news/#distribution-tarball). **HINWEIS FÜR PAKETBETREUER**: Es gibt eine neue optionale Abhängigkeit von `libsystemd`. **WICHTIGER HINWEIS**: Ab dieser Version darf standardmäßig nur der Befehl `restore` als root ausgeführt werden. Mit `allow-root` können andere Befehle als root ausgeführt werden (dies wird jedoch nicht empfohlen).

**Fehlerbehebungen:**

- Fehler behoben, durch den `expire` ein auf einem anderen Host laufendes Backup entfernte. (*Geprüft von Douglas J Hunley. Gemeldet von Dmitrii.*)
- Fehler behoben, durch den `archive-push-queue-max` bei einem Fehler einer WAL-Datei nicht durchgesetzt wurde. (*Geprüft von Stefan Fercot. Gemeldet von vut12.*)
- Fehler beim asynchronen `archive-get` während einer Recovery über einen Timeline-Wechsel hinweg behoben. (*Geprüft von Douglas J Hunley. Gemeldet von Jimmy Yih.*)
- Möglichen Pufferüberlauf im Fehlermodul behoben. (*Behoben von Christophe Pettus. Geprüft von David Steele.*)
- Zugriff auf bereits freigegebenen Speicher im parallelen Protokollclient behoben. (*Geprüft von Douglas J Hunley. Gemeldet von Georgy Shelkovy.*)
- Heap-Überlauf behoben, wenn eine pg-Option ohne pg1 gesetzt wird. (*Geprüft von Douglas J Hunley. Gemeldet von Naveen.*)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta2. (*Geprüft von Stefan Fercot.*)
- Option `archive-expire-before` zum Bereinigen des WAL-Archivs hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Stapellöschung für Azure-Speicher hinzugefügt. (*Geprüft von Douglas J Hunley, Crispy.*)
- Unterstützung für S3 Outposts hinzugefügt. (*Beigetragen von Shiva Kumar Ambigi. Geprüft von David Steele, Roberto Mello.*)
- S3-Prozessauthentifizierung hinzugefügt. (*Geprüft von Andrew Charlton. Vorgeschlagen von Andrew Charlton.*)

**Verbesserungen:**

- Erneuter Verbindungsaufbau zum SFTP-Speicher, nachdem der Server eine inaktive Verbindung getrennt hat. (*Geprüft von Stefan Fercot. Vorgeschlagen von mustafa0x, tisserat.*)
- Zwischenspeicherung von Benutzern und Gruppen für eine schnellere Erstellung des Manifests hinzugefügt. (*Beigetragen von Gunnar Lindholm. Geprüft von David Steele.*)
- Backup-Fortschritt je Repository zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Will Morland. Geprüft von David Steele, Stefan Fercot.*)
- Prüfungen von `backup.info` zum Befehl `verify` hinzugefügt. (*Beigetragen von Denis Garsh. Geprüft von David Steele, Douglas J Hunley.*)
- Konfiguration des S3-STS-Endpunkts ermöglicht. (*Beigetragen von Simon Gratton. Geprüft von David Steele.*)
- `archive-push-batch-size` hinzugefügt, um die pro asynchronem Durchlauf übertragene WAL-Menge zu begrenzen. (*Geprüft von Stefan Fercot.*)
- Asynchrones `archive-push` beim ersten Fehler beendet. (*Geprüft von Stefan Fercot. Vorgeschlagen von Lardière Sébastien.*)
- Verarbeitung von HTTP-Antworten mit Chunked-Übertragung robuster gestaltet. (*Beigetragen von Shubham. Geprüft von David Steele.*)
- Fehler bei Ausführung als root, sofern `allow-root` nicht aktiviert ist. (*Geprüft von Douglas J Hunley.*)
- Anzahl binärer Suchen beim Erstellen des Manifests reduziert. (*Beigetragen von Gunnar Lindholm. Geprüft von David Steele.*)
- Leistung bei der Positionierung innerhalb von Dateien während blockinkrementeller Delta-Wiederherstellungen verbessert. (*Geprüft von David Christensen, Douglas J Hunley.*)
- Backup-Dateien der Reihe nach gebündelt, anstatt nach einer besser passenden Datei zu suchen. (*Geprüft von Stefan Fercot.*)
- Zugrunde liegenden Fehler gemeldet, wenn eine Abfrage nicht abgeschlossen werden kann. (*Geprüft von Andrew Pogrebnoi. Vorgeschlagen von Marco Fontana.*)
- Tatsächlichen Fehler gemeldet, wenn eine Anfrage nach S3-Zugangsdaten fehlschlägt. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Mitchell Grice.*)
- Fehler des Spool-Pfads von `archive-push` im PostgreSQL-Protokoll gemeldet. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Don Seiler.*)
- Bei einer nicht unterstützten Version auf ein möglicherweise veraltetes pgBackRest hingewiesen.
- Integration von systemd-Benachrichtigungen hinzugefügt. (*Beigetragen von Andrew Jackson. Geprüft von David Steele.*)
- Fehler `unused parameter` in meson-Compilerprüfungen unterdrückt. (*Beigetragen von Jörg Plate. Geprüft von David Steele.*)
- C11 ist nun der mindestens erforderliche C-Standard. (*Geprüft von Mohammad Ali Nazir Kosar.*)

**Verbesserungen der Dokumentation:**

- Option `stanza` für die Befehle `repo-*` als intern gekennzeichnet. (*Geprüft von Stefan Fercot.*)
- Dokumentiert, dass info die Verschlüsselungseinstellungen aus dem globalen Abschnitt liest. (*Geprüft von Stefan Fercot. Vorgeschlagen von Ron Johnson.*)
- Dokumentiert, dass `expire-auto` die Konfiguration des Befehls `backup` verwendet. (*Geprüft von Stefan Fercot. Vorgeschlagen von Lardière Sébastien.*)
- Anpassung der logrotate-Direktive `su` für einen eigenen Benutzer dokumentiert. (*Geprüft von Douglas J Hunley. Vorgeschlagen von lkanbus.*)
- Dokumentiert, dass Kommentare am Zeilenende in Konfigurationsdateien nicht unterstützt werden. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Alex Richman.*)

**Verbesserungen der Testsuite:**

- Gruppenkonflikte von Alpine in CI-Containern behoben. (*Beigetragen von Artur Zakirov. Geprüft von David Steele.*)


### v2.58.0 – Versionshinweise {#v2580-release-notes}

*Verbesserungen für Objektspeicher*

*Veröffentlicht am 19. Januar 2026*

**WICHTIGER HINWEIS**: Die Mindestwerte der Option `repo-storage-upload-chunk-size` wurden erhöht. Sie entsprechen nun den von den Anbietern zugelassenen Mindestwerten.

**Fehlerbehebungen:**

- Deadlock durch Protokollierung im Signalhandler behoben. (*Behoben von Maxim Michkov. Geprüft von David Steele.*)

**Funktionen:**

- HTTP-Unterstützung für S3, GCS und Azure. (*Beigetragen von Will Morland. Geprüft von David Steele.*)
- Entfernen des ältesten vollständigen Backups unabhängig von der aktuellen Aufbewahrung ermöglicht. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Ron Johnson.*)
- Unterstützung für verwaltete Identitäten von Azure. (*Beigetragen von Moiz Ibrar, Matthew Mols. Geprüft von David Steele.*)
- ***Experimentelle*** Unterstützung für S3 EKS Pod Identity. (*Beigetragen von Pierre BOUTELOUP. Geprüft von David Steele.*)
- Konfiguration von TLS-Cipher-Suites ermöglicht. (*Beigetragen von Gunnar "Nick" Bluth. Geprüft von David Steele.*)
- Festlegen der Prozesspriorität ermöglicht. (*Geprüft von Douglas J Hunley.*)

**Verbesserungen:**

- Punkte in S3-Bucket-Namen bei Verwendung pfadbasierter URIs zugelassen. (*Beigetragen von Joakim Hindersson. Geprüft von David Steele.*)
- TLS >= 1.2 verlangt, sofern die Überprüfung nicht deaktiviert ist. (*Geprüft von Douglas J Hunley, Gunnar "Nick" Bluth.*)
- Größe von S3/GCS/Azure-Chunks bei großen Uploads dynamisch angepasst. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Timothée Peignier.*)
- S3/GCS/Azure-Chunk-Größe für kleine Dateien optimiert. (*Geprüft von Douglas J Hunley.*)
- Unterstützung für PostgreSQL `9.5` entfernt. (*Geprüft von Douglas J Hunley.*)
- Protokollierung des Standardwerts für Optionen mit einer nicht aufgelösten Abhängigkeit verbessert. (*Geprüft von Stefan Fercot.*)

**Verbesserungen der Dokumentation:**

- Explizite Konfiguration von `max_wal_senders`/`wal_level` aus dem Benutzerhandbuch entfernt. (*Vorgeschlagen von Jamie Nguyen.*)
- Klargestellt, dass Bündelung bei Dateisystemen mit großen Blockgrößen nützlich ist. (*Vorgeschlagen von Ron Johnson.*)


### v2.57.0 – Versionshinweise {#v2570-release-notes}

*Symbolische Links im Repository unterdrücken*

*Veröffentlicht am 18. Oktober 2025*

**Fehlerbehebungen:**

- Verschachtelung der Zeitüberschreitungen für HTTP/TLS/Sockets aufgehoben. (*Geprüft von David Christensen.*)
- Möglichen Segfault in der Fehlermeldung zu Seitenprüfsummen behoben. (*Behoben von Zsolt Parragi. Geprüft von David Steele.*)

**Funktionen:**

- Option `repo-symlink` hinzugefügt, um die Erstellung symbolischer Links im Repository zu unterdrücken. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Ron Johnson.*)

**Verbesserungen:**

- HTTP-Wiederholungsversuche für die Fehler 408 und 429 hinzugefügt. (*Geprüft von David Christensen.*)


### v2.56.0 – Versionshinweise {#v2560-release-notes}

*Verbesserte Fortschrittsinformationen*

*Veröffentlicht am 21. Juli 2025*

**Fehlerbehebungen:**

- Problem beim gezielten Entfernen von Backups behoben, wenn das Repository keine Backups enthält. (*Geprüft von Stefan Fercot. Gemeldet von Anup Gupta.*)

**Funktionen:**

- Wiederherstellungsfortschritt zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Denis Garsh, Maxim Michkov. Geprüft von David Steele.*)
- Detailstufe für die Ausgabe des Befehls `info` hinzugefügt, die nur den Fortschritt anzeigt. (*Beigetragen von Denis Garsh. Geprüft von David Steele, Stefan Fercot.*)

**Verbesserungen:**

- Fehlgeschlagene Lesevorgänge auf Objektspeichern wiederholt. (*Geprüft von David Christensen.*)
- Standardwerte in der Befehlszeilenhilfe korrigiert. (*Geprüft von David Christensen, Chris Bandy.*)

**Verbesserungen der Dokumentation:**

- Diskrete Optionswerte gegebenenfalls als Liste beschrieben. (*Beigetragen von Anton Kurochkin. Geprüft von David Steele.*)
- "less than" in der Hilfeausgabe für die Option `archive-mode` korrigiert. (*Beigetragen von Anton Kurochkin. Geprüft von David Steele.*)


### v2.55.1 – Versionshinweise {#v2551-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 5. Mai 2025*

**Fehlerbehebungen:**

- Änderung „content-md5 auf S3 nur bei Bedarf berechnen“ zurückgenommen. (*Geprüft von David Christensen. Gemeldet von Frank Brendel.*)
- Prüfung der unteren Grenzen für Optionsschlüssel korrigiert. (*Geprüft von David Christensen, Wolfgang Walther. Gemeldet von Wolfgang Walther.*)


### v2.55.0 – Versionshinweise {#v2550-release-notes}

*Verbesserte Überprüfung und Unterstützung für PostgreSQL 18*

*Veröffentlicht am 21. April 2025*

**Fehlerbehebungen:**

- Problem bei der blockinkrementellen Wiederherstellung aus einem nicht als Standard verwendeten Repository behoben. (*Geprüft von David Christensen, Aleksander Łukasz. Gemeldet von Aleksander Łukasz.*)
- `recovery_target_timeline=current` für PostgreSQL < 12 nicht gesetzt. (*Geprüft von Stefan Fercot.*)
- Protokollierung des Archivbereichs beim Entfernen abgelaufener Daten korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Aleš Zelený.*)
- Fehlermeldungen für Abfragen ohne Ergebnisse korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Susantha Bathige.*)

**Funktionen:**

- Ziel-Timeline der Recovery überprüft. (*Geprüft von Stefan Fercot.*)
- Überprüfung eines angegebenen Backups ermöglicht. (*Beigetragen von Maxim Michkov. Geprüft von David Steele.*)
- Unterstützung für S3/GCS mit Kostenübernahme durch den Anforderer hinzugefügt. (*Beigetragen von Timothée Peignier. Geprüft von David Steele.*)
- Unterstützung für PostgreSQL 18. (*Geprüft von Stefan Fercot.*)
- Verbindungen zu PostgreSQL über abstrakte Domain-Sockets ermöglicht. (*Geprüft von Chris Bandy. Vorgeschlagen von Chris Bandy.*)
- Numerische Ausgabe zum Befehl `version` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

**Verbesserungen:**

- Ausführung des Backup-Befehls auf entfernten Repositorys ermöglicht. (*Geprüft von Stefan Fercot.*)
- lz4 für die Protokollkomprimierung verwendet. (*Geprüft von Stefan Fercot.*)
- `content-md5` auf S3 nur bei Bedarf berechnet. (*Geprüft von David Christensen.*)
- Warnung ausgegeben, wenn ein Wert einer Option mit mehreren Schlüsseln überschrieben wird. (*Geprüft von David Christensen, Stefan Fercot.*)
- Detaillierte Protokollierung beim Entfernen abgelaufener Archivpfade hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Unterstützung für PostgreSQL `9.4` entfernt. (*Geprüft von Stefan Fercot.*)
- Build mit autoconf/make entfernt. (*Geprüft von David Christensen.*)

**Verbesserungen der Dokumentation:**

- Dokumentation zur Angabe mehrerer Stanzas mit `tls-server-auth` korrigiert. (*Geprüft von David Christensen, Stefan Fercot. Vorgeschlagen von Terry MacAndrew.*)
- Entfernen abgelaufener inkrementeller Backups erläutert. (*Geprüft von Stefan Fercot.*)
- Anforderung erläutert, dass die lokale und entfernte pgBackRest-Version übereinstimmen müssen. (*Beigetragen von Greg Clough. Geprüft von David Steele.*)
- FAQ zum Export eines eigenständigen Clusters hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Einschränkung von `--tablespace-map-all` bei der Erstellung von Tablespaces erläutert. (*Geprüft von Stefan Fercot, Christophe Courtois. Vorgeschlagen von Christophe Courtois.*)
- Verhalten von `--repo-retention-full-type` erläutert. (*Geprüft von Antoine Beaupré. Vorgeschlagen von Antoine Beaupré.*)
- Empfehlung für Objektspeicher von `--process-max` auf `--repo-bundle` geändert. (*Geprüft von Stefan Fercot.*)
- `unix_socket_directory` durch `unix_socket_directories` ersetzt. (*Beigetragen von hyunkyu han. Geprüft von David Steele.*)
- Empfohlen, `spool-path` nicht innerhalb von `pg_xlog`/`pg_wal` abzulegen. (*Geprüft von Martín Marqués, Don Seiler. Vorgeschlagen von Martín Marqués.*)


### v2.54.2 – Versionshinweise {#v2542-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 20. Januar 2025*

**Fehlerbehebungen:**

- Problem nach dem Deaktivieren der Bündelung bei aktivierter blockinkrementeller Verarbeitung behoben. (*Geprüft von David Christensen.*)

**Verbesserungen der Dokumentation:**

- Verhalten bei mehreren Konfigurationsdateien erläutert. (*Geprüft von Paul Bierly. Vorgeschlagen von Paul Bierly.*)


### v2.54.1 – Versionshinweise {#v2541-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 16. Dezember 2024*

**Fehlerbehebungen:**

- Problem behoben, bei dem die Befehle `version`/`help` versuchten, `pgbackrest.conf` zu laden. (*Geprüft von Stefan Fercot. Gemeldet von Bradford Boyle, Julian.*)

**Verbesserungen der Testsuite:**

- Asynchrone Archivierung in Integrationstests stabilisiert. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)


### v2.54.0 – Versionshinweise {#v2540-release-notes}

*Zielzeitpunkt für versionierten Speicher*

*Veröffentlicht am 21. Oktober 2024*

**HINWEIS FÜR PAKETBETREUER**: Dies ist die letzte Version mit neuen Funktionen, die den Build mit autoconf/make unterstützt. Bitte wechseln Sie zu meson, falls noch nicht geschehen. Patch-Versionen von 2.54.X werden, sofern es welche gibt, weiterhin autoconf/make unterstützen.

**Fehlerbehebungen:**

- Leistungsproblem bei PostgreSQL-Abfragen mit großen Datenmengen behoben. (*Behoben von Thibault Vincent, David Steele. Geprüft von David Christensen, Antoine Millet. Gemeldet von Antoine Millet.*)

**Funktionen:**

- Lesen von Repositorys auf versioniertem Speicher zu einem Zielzeitpunkt ermöglicht. (*Geprüft von Stefan Fercot, David Christensen.*)
- Angefordertes Backup vom Standby auch ohne verfügbaren Standby ermöglicht. (*Geprüft von Stefan Fercot.*)

**Verbesserungen:**

- Liste der Backup-Referenzen für die Textausgabe des Befehls `info` zusammengefasst. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- web-id-Token bei jeder S3-Authentifizierung erneuert. (*Beigetragen von Brent Graveland. Geprüft von David Steele.*)
- Aktuelle Werte indizierter Optionen in der Hilfe korrekt angezeigt. (*Geprüft von David Christensen.*)
- `backup.info` nur bei geändertem Inhalt gespeichert. (*Geprüft von Stefan Fercot.*)
- Einschränkung beim parallelen Lesen von Dateien während der Wiederherstellung entfernt. (*Geprüft von David Christensen.*)
- SFTP-Fehlermeldungen verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

**Neue Inhalte der Dokumentation:**

- Abschnitt zur Leistungsoptimierung zum Benutzerhandbuch hinzugefügt. (*Geprüft von Stefan Fercot.*)

**Verbesserungen der Dokumentation:**

- Quelle für `data_directory` erläutert. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Matthias.*)
- Logik verbessert, die entscheidet, wann eine Zusammenfassung kleingeschrieben werden sollte. (*Vorgeschlagen von Daniel Westermann.*)


### v2.53.1 – Versionshinweise {#v2531-release-notes}

*Unterstützung für PostgreSQL 17*

*Veröffentlicht am 19. August 2024*

**Fehlerbehebungen:**

- Berechtigungen bei der Ausführung von `restore` als root korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Will M.*)
- Segfault bei verzögerten Verbindungsfehlern behoben. (*Geprüft von David Christensen. Gemeldet von Anton Glushakov.*)
- Prüfung auf doppelte lokale Repositorys für SFTP übersprungen. (*Behoben von Reid Thompson. Geprüft von David Steele. Gemeldet von Anton Kurochkin.*)

**Verbesserungen:**

- Unterstützung für PostgreSQL 17.


### v2.53 – Versionshinweise {#v253-release-notes}

*Gleichzeitige Backups*

*Veröffentlicht am 22. Juli 2024*

**WICHTIGER HINWEIS**: Der Standardwert der Option `log-level-stderr` wurde von `warn` auf `off` geändert. Dies erleichtert das Erfassen von Fehlern, wenn nur `stdout` umgeleitet wird. Um das bisherige Verhalten beizubehalten, setzen Sie `log-level-stderr=warn`. **HINWEIS FÜR PAKETBETREUER**: Der meson-Build benötigt nun die lz4-Bibliothek. **HINWEIS FÜR PAKETBETREUER**: Der meson-Build benötigt nun Compiler-Unterstützung für `__builtin_clzl()` und `__builtin_bswap64()`.

**Fehlerbehebungen:**

- Fehler beim Umbenennen über SFTP behoben, wenn die Datei bereits existiert. (*Behoben von Reid Thompson. Geprüft von David Steele. Gemeldet von ahmed112212.*)

**Funktionen:**

- Gleichzeitige Backups auf unterschiedlichen Repositorys ermöglicht. (*Geprüft von Reid Thompson, Stefan Fercot.*)
- Unterstützung für IP-basierte SANs bei der Validierung von TLS-Zertifikaten. (*Beigetragen von David Christensen. Geprüft von David Steele.*)

**Verbesserungen:**

- Standardwert der Option `log-level-stderr` auf `off` gesetzt. (*Geprüft von Greg Sabino Mullane, Stefan Fercot.*)
- Alternative WAL-Segmentgrößen für PostgreSQL ≤ 10 ermöglicht. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)
- Hinweis zur Prüfung des SFTP-Autorisierungsprotokolls hinzugefügt. (*Beigetragen von Vitalii Zurian. Geprüft von Reid Thompson, David Steele.*)

**Verbesserungen der Dokumentation:**

- Verhalten von `archive-push` bei mehreren Repositorys erläutert. (*Geprüft von Stefan Fercot.*)


### v2.52.1 – Versionshinweise {#v2521-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 25. Juni 2024*

**Fehlerbehebungen:**

- Problem bei Dateien behoben, die auf dem Replikat größer sind als auf dem Primärserver. (*Geprüft von Stefan Fercot. Gemeldet von Nicolas Lassimonne.*)


### v2.52 – Versionshinweise {#v252-release-notes}

*Unterstützung für PostgreSQL 17beta1*

*Veröffentlicht am 27. Mai 2024*

**HINWEIS FÜR PAKETBETREUER**: Das Build-System von pgBackRest ist nun meson. Der Build mit autoconf/make erhält keine neuen Funktionen mehr und wird nach einigen Versionen entfernt.

**Funktionen:**

- Unterstützung für GCS-Stapellöschung hinzugefügt. (*Geprüft von Reid Thompson.*)
- Unterstützung für S3-Verschlüsselung mit `SSE-C`. (*Geprüft von Tim Jones. Vorgeschlagen von Tim Jones.*)
- Unterstützung für PostgreSQL 17beta1. (*Geprüft von Stefan Fercot.*)

**Verbesserungen:**

- Explizites Deaktivieren optionaler Abhängigkeiten bei meson-Builds ermöglicht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)
- python beim meson-Build dynamisch gesucht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)
- Build-Ziel `pgbackrest` in meson als installierbar gekennzeichnet. (*Beigetragen von Bradford Boyle. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Dokumentation zu `start`/`stop` an die tatsächliche Funktionalität angepasst. (*Geprüft von Stefan Fercot.*)


### v2.51 – Versionshinweise {#v251-release-notes}

*Build-System Meson*

*Veröffentlicht am 25. März 2024*

**Fehlerbehebungen:**

- Dateien mit der Länge null bei blockinkrementellen Delta-Wiederherstellungen übersprungen. (*Geprüft von Sebastian Krause, René Højbjerg Larsen. Gemeldet von Sebastian Krause.*)
- Leistungsregression beim Auflisten des Speichers behoben. (*Geprüft von Stephen Frost. Gemeldet von Maksym Boguk.*)
- Fortschrittsprotokollierung korrigiert, wenn sich die Dateigröße während des Backups ändert. (*Geprüft von Stephen Frost. Gemeldet von samkingno.*)

**Verbesserungen:**

- Unterstützung für Dual-Stack-Verbindungen verbessert. (*Geprüft von Stephen Frost. Vorgeschlagen von Timothée Peignier.*)
- meson zum primären Build-System gemacht. (*Geprüft von Stephen Frost.*)
- Unveränderte Dateien bei inkrementellen Backups ohne Delta erkannt. (*Geprüft von Stephen Frost.*)
- Ungültige Recovery bei entferntem `backup_label` verhindert. (*Geprüft von Stephen Frost.*)
- Verarbeitung der WAL-Segmentwarteschlange von `archive-push` verbessert. (*Geprüft von Stephen Frost.*)
- Fortsetzen von Backups auf vollständige Backups beschränkt. (*Geprüft von Stephen Frost, Stefan Fercot.*)
- Fortsetzungsfunktion für blockinkrementelle Backups aktualisiert. (*Geprüft von Stephen Frost.*)
- `--version` und `--help` für Version und Hilfe zugelassen. (*Geprüft von Greg Sabino Mullane. Vorgeschlagen von Greg Sabino Mullane.*)
- Detaillierten Backtrace zum Build mit autoconf/make hinzugefügt. (*Geprüft von Stephen Frost.*)

**Verbesserungen der Dokumentation:**

- Verweise auf `recovery.conf` aktualisiert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Stephen Frost.*)


### v2.50 – Versionshinweise {#v250-release-notes}

*Leistungsverbesserungen und Fehlerbehebungen*

*Veröffentlicht am 22. Januar 2024*

**Fehlerbehebungen:**

- Unvollständigen Lesevorgang bei blockinkrementellen Wiederherstellungen korrigiert. (*Geprüft von Stephen Frost, Brent Graveland. Gemeldet von Adol Rodriguez, Brent Graveland.*)
- Überlauf behoben, der den Backup-Fortschritt in der Ausgabe von `info` unterdrückte. (*Behoben von Robert Donovan. Geprüft von Joe Wildish.*)

**Verbesserungen:**

- Unvollständige Dateien bei blockinkrementellen Delta-Wiederherstellungen beibehalten. (*Geprüft von Stephen Frost.*)
- Unterstützung für alternative, beim Kompilieren festgelegte Seitengrößen hinzugefügt. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)
- Beim Bündeln Dateien übersprungen, die während des Backups gekürzt wurden. (*Beigetragen von Georgy Shelkovy. Geprüft von David Steele.*)
- Fehlermeldungen des SFTP-Speichers verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)


### v2.49 – Versionshinweise {#v249-release-notes}

*Unterstützung für PostgreSQL 9.3 entfernt*

*Veröffentlicht am 27. November 2023*

**Fehlerbehebungen:**

- Regression bei Wiederholungsversuchen behoben. (*Geprüft von Stephen Frost. Gemeldet von Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)
- Rekursives Entfernen von Pfaden im SFTP-Speichertreiber korrigiert. (*Behoben von Reid Thompson. Geprüft von Stephen Frost. Gemeldet von Luc.*)

**Verbesserungen:**

- Unterstützung für PostgreSQL `9.3` entfernt. (*Geprüft von Stephen Frost.*)

**Neue Inhalte der Dokumentation:**

- Optionen für Projektbetreuer dokumentiert. (*Geprüft von Stefan Fercot.*)
- Dokumentation zur Point-in-Time-Recovery für PostgreSQL >= 13 aktualisiert.

**Verbesserungen der Testsuite:**

- Ausführung des Unittests `config/load` ohne installiertes `libssh2` ermöglicht. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Wu Ning.*)


### v2.48 – Versionshinweise {#v248-release-notes}

*Tags für den Repository-Speicher*

*Veröffentlicht am 25. September 2023*

**Fehlerbehebungen:**

- Problem bei der blockinkrementellen Wiederherstellung ohne Blockliste behoben. (*Geprüft von Stephen Frost, Burak Yurdakul. Gemeldet von Burak Yurdakul.*)

**Funktionen:**

- Option `--repo-storage-tag` zum Erstellen von Objekt-Tags hinzugefügt. (*Geprüft von Stephen Frost, Stefan Fercot, Timothée Peignier.*)
- Prüfung bekannter Hosts zum SFTP-Speichertreiber hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von Stephen Frost, David Steele.*)
- Unterstützung für Dual-Stack-Verbindungen. (*Geprüft von Stephen Frost.*)
- Bereits verarbeitete und gesamte Backup-Größe zur JSON-Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

**Verbesserungen:**

- check-Befehl für mehrere Stanzas. (*Geprüft von Stephen Frost.*)
- Lesen von `pg_control` wiederholt, bis die Prüfsumme gültig ist. (*Geprüft von Stefan Fercot, Stephen Frost.*)
- Prüfung der WAL-Segmente nach erfolgreichem Backup optimiert. (*Geprüft von Stephen Frost.*)
- Leistung mehrteiliger Übertragungen bei GCS verbessert. (*Geprüft von Reid Thompson.*)
- Ausführung des Befehls `archive-get` bei gestoppter Stanza ermöglicht. (*Geprüft von Tom Swartz, David Christensen, Reid Thompson.*)
- Führende Tilde in Pfaden für öffentliche/private SFTP-Schlüssel akzeptiert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- GCS-Zugangsdaten vor der Erneuerung des Authentifizierungstokens neu geladen. (*Geprüft von Stephen Frost. Vorgeschlagen von Daniel Farina.*)

**Fehlerbehebungen in der Dokumentation:**

- Beispiel für die Option `tls-server-address` in der Konfigurationsreferenz korrigiert. (*Behoben von Hartmut Goebel. Geprüft von David Steele.*)
- Beispiel für die Option `filter` in der Befehlsreferenz korrigiert.

**Verbesserungen der Testsuite:**

- Ausführung des Unittests `storage/sftp` ohne installiertes `libssh2` ermöglicht. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Wu Ning.*)


### v2.47 – Versionshinweise {#v247-release-notes}

*Leistungsverbesserungen und Fehlerbehebungen*

*Veröffentlicht am 24. Juli 2023*

**Fehlerbehebungen:**

- Blockinkrementelle Informationen im Manifest während eines Delta-Backups beibehalten. (*Geprüft von Stephen Frost. Gemeldet von Francisco Miguel Biete Banon.*)
- Blockinkrementelle Dateinamen im Befehl `verify` korrigiert. (*Geprüft von Reid Thompson. Gemeldet von Francisco Miguel Biete Banon.*)
- Unbegründetes automatisches Delta-Backup beim Backup vom Standby behoben. (*Geprüft von Stephen Frost. Gemeldet von krmozejko, Don Seiler.*)
- `recovery.signal` für PostgreSQL >= 12 bei Recovery mit `type=none` übersprungen. (*Geprüft von Stefan Fercot. Gemeldet von T.Anastacio.*)
- Erzeugung eindeutiger Kennzeichnungen für differenzielle/inkrementelle Backups korrigiert. (*Behoben von Andrey Sokolov. Geprüft von David Steele.*)
- Zeitbasiertes Entfernen abgelaufener Archivdaten korrigiert, wenn keine Backups abgelaufen sind. (*Geprüft von Stefan Fercot.*)

**Verbesserungen:**

- Leistung des SFTP-Speichertreibers verbessert. (*Beigetragen von Stephen Frost, Reid Thompson. Geprüft von David Steele.*)
- Zeitzonenversatz zur Datums-/Zeitausgabe des Befehls `info` hinzugefügt. (*Geprüft von Stefan Fercot, Philip Hurst. Vorgeschlagen von Philip Hurst.*)
- Fehlerbehandlung für nicht unterstützte Funktionen zentralisiert. (*Geprüft von Stefan Fercot.*)

**Verbesserungen der Dokumentation:**

- Im Benutzerhandbuch klargestellt, dass die Installation aus Paketen bevorzugt wird. (*Geprüft von Stefan Fercot. Vorgeschlagen von dr-kd.*)


### v2.46 – Versionshinweise {#v246-release-notes}

*Blockinkrementelles Backup und SFTP-Speicher*

*Veröffentlicht am 22. Mai 2023*

**Funktionen:**

- Blockinkrementelles Backup. (*Geprüft von John Morris, Stephen Frost, Stefan Fercot.*)
- SFTP-Unterstützung für Repository-Speicher. (*Beigetragen von Reid Thompson. Geprüft von Stephen Frost, David Steele.*)
- Unterstützung für PostgreSQL 16. (*Geprüft von Stefan Fercot.*)

**Verbesserungen:**

- Überspringen der Seitenheader-Prüfungen ermöglicht. (*Geprüft von David Christensen. Vorgeschlagen von David Christensen.*)
- `chown()` auf Recovery-Dateien während der Wiederherstellung vermieden. (*Geprüft von Stefan Fercot, Marcelo Henrique Neppel. Vorgeschlagen von Marcelo Henrique Neppel.*)
- Fehlerdetails zu Wiederholungsversuchen bei HTTP hinzugefügt.

**Verbesserungen der Dokumentation:**

- Warnung zur Verwendung von Recovery mit `type=none` hinzugefügt. (*Geprüft von Stefan Fercot.*)
- Hinweis zur Ausführung von `stanza-create` auf bereits erstellten Repositorys hinzugefügt.


### v2.45 – Versionshinweise {#v245-release-notes}

*Blockinkrementelles Backup (BETA)*

*Veröffentlicht am 20. März 2023*

**Fehlerbehebungen:**

- Schreiben von `recovery.signal` bei der Wiederherstellung von Offline-Backups standardmäßig übersprungen. (*Geprüft von Stefan Fercot. Gemeldet von Marcel Borger.*)

**Funktionen:**

- Blockinkrementelles Backup (BETA). (*Geprüft von John Morris, Stephen Frost, Stefan Fercot.*)

**Verbesserungen:**

- Nur einen Gruppenindex mit ausschließlich Standardwerten beibehalten. (*Geprüft von Stefan Fercot.*)

**Verbesserungen der Dokumentation:**

- Explizite Anweisungen für Upgrades zwischen `2.x`-Versionen hinzugefügt. (*Beigetragen von Christophe Courtois. Geprüft von David Steele.*)
- Mit der Einführung von TLS überholte Verweise auf SSH entfernt.


### v2.44 – Versionshinweise {#v244-release-notes}

*Unterstützung für PostgreSQL 9.0/9.1/9.2 entfernt*

*Veröffentlicht am 30. Januar 2023*

**Verbesserungen:**

- Unterstützung für PostgreSQL `9.0`/`9.1`/`9.2` entfernt. (*Geprüft von Stefan Fercot.*)
- Wiederherstellung mit Fehler abgebrochen, wenn kein Backup zur aktuellen PostgreSQL-Version passt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Soulou.*)
- Bereichsprüfung für `compress-level` für jeden `compress-type` hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von gkleen, ViperRu.*)

**Verbesserungen der Dokumentation:**

- Warnung zur Aktivierung des „hierarchischen Namensraums“ auf Azure-Speicher hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von Vojtech Galda, Pluggi, asjonos.*)
- Ersetzung von Zeilenvorschüben im Überwachungsbeispiel hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von rudonx, gmustdie, Ivan Shelestov.*)
- Verhalten von `target-action` bei verschiedenen PostgreSQL-Versionen erläutert. (*Beigetragen von Chris Bandy. Geprüft von David Steele, Anton Kurochkin, Stefan Fercot. Vorgeschlagen von Anton Kurochkin, Chris Bandy.*)
- Übersichtsseite aktualisiert und erläutert. (*Geprüft von Stefan Fercot.*)
- Dunkelmodus zur Website hinzugefügt. (*Vorgeschlagen von Stephen Frost.*)


### v2.43 – Versionshinweise {#v243-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 28. November 2022*

**Fehlerbehebungen:**

- Fehlende Referenz bei differenziellen/inkrementellen Backups korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Marcel Borger, ulfedf, jaymefSO.*)

**Verbesserungen:**

- Hinweis hinzugefügt, wenn eine Option ohne Index angegeben wird. (*Geprüft von Stefan Fercot.*)


### v2.42 – Versionshinweise {#v242-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 22. November 2022*

**Fehlerbehebungen:**

- Speicherleck bei `backup`/`restore` mit Dateibündelung behoben. (*Geprüft von John Morris, Oscar. Gemeldet von Oscar.*)
- Protokollfehler bei unvollständigem Lesen einer entfernten Datei behoben. (*Geprüft von Stephen Frost.*)

**Verbesserungen:**

- Beim Bündeln keine Referenzen für Dateien mit der Länge null gespeichert. (*Geprüft von Stefan Fercot.*)
- Allgemeinere Beschreibungen für `pg_start_backup()`/`pg_stop_backup()` verwendet. (*Geprüft von Greg Sabino Mullane, David Christensen. Vorgeschlagen von Greg Sabino Mullane.*)

**Verbesserungen der Testsuite:**

- Option `--psql-bin` von `test.pl` an die Befehlszeilenhilfe angepasst. (*Beigetragen von Koshi Shibagaki. Geprüft von David Steele.*)


### v2.41 – Versionshinweise {#v241-release-notes}

*Backup-Anmerkungen*

*Veröffentlicht am 19. September 2022*

**Fehlerbehebungen:**

- Falsche zeitbasierte Ablaufberechnung für nicht als Standard verwendete Repositorys korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Adam Brusselback.*)
- Problem beim rekursiven Auflisten von Verzeichnissen mit einem Filter behoben. (*Geprüft von Stephen Frost. Gemeldet von Efremov Egor.*)

**Funktionen:**

- Anmerkungen als Schlüssel-Wert-Paare für Backups. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Adam Berlin.*)

**Verbesserungen:**

- `--set` in der JSON-Ausgabe des Befehls `info` unterstützt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Anton Kurochkin.*)
- Konfiguration der Upload-Chunk-Größe für Objektspeicher ermöglicht. (*Geprüft von Stefan Fercot. Vorgeschlagen von Anton Glushakov.*)
- Zeitstempel von archive.info nach erfolgreichem Backup aktualisiert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Alex Richman.*)
- Prüfung der Standby-Timeline hinter den Checkpoint verschoben. (*Geprüft von Stefan Fercot, Keith Fiske. Vorgeschlagen von Keith Fiske.*)
- Warnmeldung beim Fortsetzen eines Backups verbessert. (*Vorgeschlagen von Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- Absoluten Pfad für `kill` in `pgbackrest.service` hinzugefügt. (*Vorgeschlagen von Don Seiler.*)


### v2.40 – Versionshinweise {#v240-release-notes}

*Unterstützung für OpenSSL 3*

*Veröffentlicht am 18. Juli 2022*

**HINWEIS FÜR PAKETBETREUER**: Ein experimenteller meson-Build wurde hinzugefügt. Paketbetreuer sollten jedoch auf absehbare Zeit weiterhin den Build mit autoconf/make verwenden.

**Verbesserungen:**

- Unterstützung für OpenSSL 3. (*Geprüft von Stephen Frost.*)
- Beim Auflisten des Inhalts eines Pfads einen Snapshot erstellt. (*Geprüft von John Morris, Stephen Frost.*)
- `target-timeline=current` bei einer Wiederherstellung mit `type=immediate` erzwungen. (*Geprüft von Stephen Frost.*)
- Dateien bei Delta-`restore` gekürzt, wenn sie größer als erwartet sind. (*Geprüft von Stephen Frost.*)
- Inkrementelles Speichern des Manifests bei `resume=n` deaktiviert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Backup-Fortschritt vor Beginn des Kopierens auf null Prozent gesetzt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- S3-Flag `IsTruncated` verwendet, um die Fortsetzung der Auflistung zu bestimmen. (*Geprüft von John Morris, Soulou. Vorgeschlagen von Christian Montagne.*)

**Fehlerbehebungen in der Dokumentation:**

- Interne Optionen in der Konfigurationsreferenz übersprungen. (*Gemeldet von Francisco Miguel Biete Banon.*)

**Verbesserungen der Dokumentation:**

- Link zur PostgreSQL-Konfiguration im Abschnitt zum Repository-Host hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von Julien Cigar.*)

**Verbesserungen der Testsuite:**

- Experimentellen Meson-Build hinzugefügt. (*Geprüft von Eli Schwartz, Sam Bassaly.*)
- Übergabe beliebiger Pfade an die Option `--test-path` ermöglicht. (*Beigetragen von Andrey Sokolov. Geprüft von David Steele.*)
- Kompilierfehler behoben, wenn `DEBUG_EXEC_TIME` ohne `DEBUG` definiert ist. (*Beigetragen von Andrey Sokolov. Geprüft von David Steele.*)


### v2.39 – Versionshinweise {#v239-release-notes}

*Überprüfung und Dateibündelung*

*Veröffentlicht am 16. Mai 2022*

**Fehlerbehebungen:**

- Fehler behoben, bei dem eine aus `FINALLY()` ausgelöste Ausnahme eine Endlosschleife verursachte. (*Geprüft von Stephen Frost.*)
- Bei allen Sperrfehlern einen Fehler ausgegeben, außer wenn ein anderer Prozess die Sperre hält. (*Geprüft von Reid Thompson, Geir Råness. Gemeldet von Geir Råness.*)

**Funktionen:**

- Bündelung von Backup-Dateien zur besseren Unterstützung kleiner Dateien. (*Geprüft von Reid Thompson, Stefan Fercot, Chris Bandy.*)
- Verify-Befehl zum Validieren des Inhalts eines Repositorys. (*Beigetragen von Cynthia Shang, Reid Thompson. Geprüft von David Steele, Stefan Fercot.*)
- Unterstützung für PostgreSQL 15. (*Geprüft von Stefan Fercot.*)
- Backup-Fortschritt in Prozent in der Ausgabe von `info` angezeigt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Backup für den Befehl `restore` mit `--type=lsn` automatisch ausgewählt. (*Beigetragen von Reid Thompson. Geprüft von Stefan Fercot, David Steele.*)
- Warnung zu vorhandenem WAL bei deaktiviertem `archive-mode-check` unterdrückt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Unterstützung für AWS IMDSv2 hinzugefügt. (*Beigetragen von Nuno Pires. Geprüft von David Steele.*)

**Verbesserungen:**

- Ändern der Option `repo-hardlink` nach einem vollständigen Backup ermöglicht. (*Geprüft von Reid Thompson.*)
- Genauigkeit der Fortschrittsprotokollierung in Prozent für `backup` und `restore` erhöht. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Pfadvalidierung für die Befehle `repo-*` verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Befehl `stop` verbessert, sodass er die Option `stanza` berücksichtigt. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von ragaoua.*)
- Fehlermeldung bei ungültigem `repo-azure-key` verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Seth Daniel.*)
- Hinweis zur Prüfung des Protokolls bei asynchronen Fehlern von `archive-get`/`archive-push` hinzugefügt. (*Geprüft von Reid Thompson.*)
- `ClockError` für unerwartete Uhrabweichungen und Zeitzonenänderungen hinzugefügt. (*Geprüft von Greg Sabino Mullane, Stefan Fercot. Vorgeschlagen von Greg Sabino Mullane.*)
- Dateinamenerweiterungen des historischen Manifests vor der Anzeige in der Fehlermeldung entfernt. (*Geprüft von Stefan Fercot.*)
- user:group zum Berechtigungsfehler bei Sperren hinzugefügt. (*Geprüft von Reid Thompson.*)

**Fehlerbehebungen in der Dokumentation:**

- Falschen Verweis auf `stanza-update` im Benutzerhandbuch korrigiert. (*Behoben von Abubakar Mohammed. Geprüft von David Steele.*)
- Beispiel für die Option `repo-gcs-key-type` in der Konfigurationsreferenz korrigiert. (*Geprüft von Reid Thompson.*)
- Beispiel für `tls-server-auth` korrigiert und Erläuterungen hinzugefügt. (*Geprüft von Reid Thompson.*)

**Verbesserungen der Dokumentation:**

- Aussagen zu unterstützten Versionen in der Dokumentation vereinfacht. (*Geprüft von Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)
- Beschreibungen der Optionstypen hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- FAQ zu Backup-Typen und Wiederherstellungsgeschwindigkeit hinzugefügt. (*Beigetragen von David Christensen. Geprüft von Reid Thompson.*)
- Erforderlichen Basisbranch für Pull Requests dokumentiert. (*Beigetragen von David Christensen. Geprüft von Reid Thompson.*)


### v2.38 – Versionshinweise {#v238-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 6. März 2022*

**WICHTIGER HINWEIS**: Die vom Befehl `info` gemeldete Repository-Größe basiert nun vollständig auf den Daten, die pgBackRest in den Speicher geschrieben hat. Zuvor konnte pgBackRest in bestimmten Fällen erkennen, ob der Speicher zusätzliche Komprimierung anwendete. Dies wird nicht mehr unterstützt.

**Fehlerbehebungen:**

- Bei Fehlern während der S3-Stapellöschung von Dateien Wiederholungsversuche durchgeführt. (*Geprüft von Reid Thompson. Gemeldet von Alex Richman.*)
- Vergleich der Werte des HTTP-Headers `connection` ohne Beachtung der Groß-/Kleinschreibung ermöglicht. (*Geprüft von Reid Thompson. Gemeldet von Rémi Vidier.*)

**Funktionen:**

- Unterstützung für serverseitige Verschlüsselung von AWS S3 mit KMS hinzugefügt. (*Beigetragen von Christoph Berg. Geprüft von David Steele, Tharindu Amila.*)
- Option `archive-missing-retry` hinzugefügt. (*Geprüft von Stefan Fercot.*)
- Filter für den Backup-Typ zum Befehl `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

**Verbesserungen:**

- Bei fehlgeschlagener Seitenprüfung während `backup` einen Wiederholungsversuch ausgeführt. (*Geprüft von Stephen Frost, David Christensen.*)
- TLS-Server behandelt, die Verbindungen nicht geordnet schließen. (*Geprüft von Rémi Vidier, David Christensen, Stephen Frost.*)
- Backup-LSNs zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Abschließende Schrägstriche in Pfaden für `repo-ls` automatisch entfernt. (*Beigetragen von David Christensen. Geprüft von David Steele.*)
- Bei fatalen Fehlern keine Wiederholungsversuche durchgeführt. (*Geprüft von Reid Thompson.*)
- Unterstützung für PostgreSQL `8.3`/`8.4` entfernt. (*Geprüft von Reid Thompson, Stefan Fercot.*)
- Logik zur Ermittlung zusätzlicher Dateisystemkomprimierung entfernt. (*Geprüft von Reid Thompson, Stefan Fercot.*)

**Fehlerbehebungen in der Dokumentation:**

- Optionen `repo` in der TLS-Dokumentation in den Abschnitt `global` verschoben. (*Gemeldet von Anton Kurochkin.*)
- Ungenutzte Option `backup-standby` aus den Stanza-Befehlen entfernt. (*Gemeldet von Stefan Fercot.*)
- Tippfehler in der Hilfe und den Versionshinweisen korrigiert. (*Behoben von Daniel Gustafsson. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Prüfung auf Betriebsbereitschaft zur systemd-Dienstkonfiguration hinzugefügt. (*Vorgeschlagen von Yogesh Sharma.*)
- FAQ zur Erklärung des WAL-Archivsuffixes hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Darauf hingewiesen, dass Replikationsslots nicht wiederhergestellt werden. (*Beigetragen von Reid Thompson. Geprüft von David Steele, Stefan Fercot. Vorgeschlagen von Christophe Courtois.*)


### v2.37 – Versionshinweise {#v237-release-notes}

*TLS-Server*

*Veröffentlicht am 3. Januar 2022*

**WICHTIGER HINWEIS**: Wenn der Befehl `restore` kein Backup findet, das zu einem angegebenen Zielzeitpunkt passt, wird nun ein Fehler ausgelöst. Zuvor wurde eine Warnung protokolliert.

**Fehlerbehebungen:**

- Delta-Link-Zuordnung von `restore` korrigiert, wenn der Pfad/die Datei bereits existiert. (*Geprüft von Reid Thompson. Gemeldet von Younes Alhroub.*)
- Socket-Leck bei wiederholten Verbindungsversuchen behoben. (*Geprüft von Reid Thompson. Gemeldet von James Coleman.*)

**Funktionen:**

- TLS-Server hinzugefügt. (*Geprüft von Stephen Frost, Reid Thompson, Andrew L'Ecuyer.*)
- Option `--cmd` hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von Stefan Fercot, David Steele. Vorgeschlagen von Virgile CREVON.*)

**Verbesserungen:**

- Archiv unmittelbar nach Beginn des Backups geprüft. (*Geprüft von Reid Thompson, David Christensen.*)
- Timeline- und Checkpoint-Prüfungen zum Backup hinzugefügt. (*Geprüft von Stefan Fercot, Reid Thompson.*)
- Während eines Backups geprüft, ob Cluster laufen und korrekt konfiguriert sind. (*Geprüft von Stefan Fercot.*)
- Fehler ausgegeben, wenn `restore` kein zum Zielzeitpunkt passendes Backup findet. (*Geprüft von Reid Thompson, Douglas J Hunley. Vorgeschlagen von Douglas J Hunley.*)
- Protokoll/Port in S3/Azure-Endpunkten ausgewertet. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Warnung hinzugefügt, wenn checkpoint_timeout größer als `db-timeout` ist. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- HTTP-Methode zur HTTP-Fehlerausgabe hinzugefügt. (*Beigetragen von Christoph Berg. Geprüft von David Steele.*)
- y/n-Argumente für boolesche Befehlszeilenoptionen zugelassen. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)
- Protokollierung der Backup-Größe exakt an die Ausgabe des Befehls `info` angeglichen. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Mahomed Hussein.*)

**Verbesserungen der Dokumentation:**

- Standardwert und zulässige Werte von Größenoptionen mit passenden Einheiten angezeigt. (*Geprüft von Reid Thompson.*)
- Tippfehler korrigiert und Dokumentation zur Option `tablespace-map-all` verbessert. (*Geprüft von Reid Thompson. Vorgeschlagen von Reid Thompson.*)
- Überholte Aussage zur künftigen Unterstützung mehrerer Repositorys entfernt. (*Vorgeschlagen von David Christensen.*)


### v2.36 – Versionshinweise {#v236-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 1. November 2021*

**Fehlerbehebungen:**

- "global" als Stanza-Präfix zugelassen. (*Geprüft von Stefan Fercot. Gemeldet von Younes Alhroub.*)
- Segfault bei einer ungültigen GCS-Schlüsseldatei behoben. (*Geprüft von Stephen Frost. Gemeldet von Henrik Feldt.*)

**Verbesserungen:**

- Erstellung neuer Links durch die Option `link-map` ermöglicht. (*Geprüft von Don Seiler, Stefan Fercot, Chris Bandy. Vorgeschlagen von Don Seiler.*)
- Höchsten zulässigen Index für die Optionen `pg`/`repo` auf 256 erhöht. (*Geprüft von Cynthia Shang.*)
- Authentifizierung mit `WebIdentity` für AWS S3 hinzugefügt. (*Geprüft von James Callahan, Reid Thompson, Benjamin Blattberg, Andrew L'Ecuyer.*)
- Fehler bei der Validierung von Backup-Dateien in `backup.info` gemeldet. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Startzeit der Recovery zum Wiederherstellungsprotokoll von Online-Backups hinzugefügt. (*Geprüft von Tom Swartz, Stefan Fercot. Vorgeschlagen von Tom Swartz.*)
- Ursprünglichen Fehler und Wiederholungsversuche beim Fehlschlagen eines lokalen Jobs gemeldet. (*Geprüft von Stefan Fercot.*)
- Seitenprüfsummenfehler in der Textausgabe von info in Fehlerliste umbenannt. (*Geprüft von Stefan Fercot.*)
- Hinweise zur Meldung über eine Zeitüberschreitung bei der WAL-Wiedergabe auf dem Standby hinzugefügt. (*Geprüft von Cynthia Shang, Stefan Fercot. Vorgeschlagen von Leigh Downs.*)


### v2.35 – Versionshinweise {#v235-release-notes}

*Binärprotokoll*

*Veröffentlicht am 23. August 2021*

**WICHTIGER HINWEIS**: Die Protokollierungsstufe für kopierte Dateien in den Befehlen `backup`/`restore` wurde auf `detail` geändert. Dies reduziert die Ausgabemenge auf der Stufe `info`. Falls diese Meldungen benötigt werden, setzen Sie die Protokollierungsstufe für die Befehle `backup`/`restore` auf `detail`

**Fehlerbehebungen:**

- Fehler beim Abschließen mehrteiliger S3-Uploads erkannt. (*Geprüft von Cynthia Shang, Marco Montagna. Gemeldet von Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)
- Erkennung zyklischer symbolischer Links korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Rohit Raveendran.*)
- Nur ausgewählte Optionen `repo` an die Gegenstelle übergeben. (*Geprüft von David Christensen, Cynthia Shang. Gemeldet von Greg Sabino Mullane, David Christensen.*)

**Verbesserungen:**

- Binärprotokoll. (*Geprüft von Cynthia Shang.*)
- Datenverzeichnis bei `restore` automatisch erstellt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Chris Bandy.*)
- `restore` mit `--type=lsn` ermöglicht. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang. Vorgeschlagen von James Coleman.*)
- Protokollierungsstufe für durch `backup`/`restore` kopierte Dateien auf detail geändert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Jens Wilke.*)
- In einer Schleife gewartet, bis die Checkpoint-LSN die Wiedergabe-LSN erreicht. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Fatih Mencutekin.*)
- Gesamte Dateianzahl bei `backup` und gesamte Größe/Dateianzahl bei `restore` protokolliert. (*Geprüft von Cynthia Shang.*)

**Fehlerbehebungen in der Dokumentation:**

- Falsche Hostnamen im Benutzerhandbuch korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Greg Sabino Mullane.*)

**Verbesserungen der Dokumentation:**

- Dokumentation für Mitwirkende aktualisiert und Vorlage für Pull Requests hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Backup-Dokumentation im Benutzerhandbuch neu angeordnet. (*Geprüft von Cynthia Shang.*)
- Verhalten von `restore` mit `--type` in der Befehlsreferenz erläutert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Tippfehler in Dokumentation und Kommentaren korrigiert. (*Beigetragen von Eric Radman. Geprüft von David Steele.*)

**Verbesserungen der Testsuite:**

- Prüfung auf einen Testpfad innerhalb des Repository-Pfads hinzugefügt. (*Geprüft von Greg Sabino Mullane. Vorgeschlagen von Greg Sabino Mullane.*)
- Statische Codeanalyse mit CodeQL hinzugefügt. (*Geprüft von Cynthia Shang.*)
- Tests auf Standardmuster umgestellt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.34 – Versionshinweise {#v234-release-notes}

*Unterstützung für PostgreSQL 14*

*Veröffentlicht am 7. Juni 2021*

**Fehlerbehebungen:**

- Probleme mit übrig gebliebenen Spool-Dateien aus einem vorherigen `restore` behoben. (*Geprüft von Cynthia Shang, Stefan Fercot, Floris van Nee. Gemeldet von Floris van Nee.*)
- Problem beim Prüfen von Links bei einer großen Anzahl von Tablespaces behoben. (*Geprüft von Cynthia Shang, Avinash Vallarapu. Gemeldet von Avinash Vallarapu.*)
- Nicht mehr benötigte entfernte Verbindungen freigegeben, damit sie während `restore` keine Zeitüberschreitung verursachen. (*Geprüft von Cynthia Shang. Gemeldet von Francisco Miguel Biete Banon.*)
- `help` korrigiert, wenn eine gültige Option für den angegebenen Befehl ungültig ist. (*Geprüft von Stefan Fercot. Gemeldet von Cynthia Shang.*)

**Funktionen:**

- Unterstützung für PostgreSQL 14 hinzugefügt. (*Geprüft von Cynthia Shang.*)
- Automatische GCS-Authentifizierung für GCE-Instanzen hinzugefügt. (*Geprüft von Jan Wieck, Daniel Farina.*)
- Option `repo-retention-history` zum Entfernen abgelaufener Backup-Historien hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang, David Steele.*)
- Option `db-exclude` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Protokollierung beim Entfernen abgelaufener Archivdaten von der Stufe detail auf info geändert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Archiv-Spool-Pfad der Stanza bei `restore` entfernt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)
- Beim Kopieren für `backup` Dateien nicht atomar geschrieben und Pfade nicht synchronisiert. (*Geprüft von Stephen Frost, Stefan Fercot, Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- Dokumentation für Mitwirkende aktualisiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele, Stefan Fercot.*)
- RHEL/CentOS-Benutzerhandbuch zu einem einzigen Dokument zusammengeführt. (*Geprüft von Cynthia Shang.*)
- Klargestellt, dass `repo-s3-role` kein `ARN` ist. (*Beigetragen von Isaac Yuen. Geprüft von David Steele.*)


### v2.33 – Versionshinweise {#v233-release-notes}

*Unterstützung für mehrere Repositorys und GCS*

*Veröffentlicht am 5. April 2021*

**Fehlerbehebungen:**

- Optionswarnungen korrigiert, die asynchrones `archive-get`/`archive-push` störten. (*Geprüft von Cynthia Shang. Gemeldet von Lev Kokotov.*)
- Speicherleck beim Kopieren des Archivs während des Backups behoben. (*Geprüft von Cynthia Shang. Gemeldet von Christian ROUX, Efremov Egor.*)
- Stack-Überlauf bei der Erzeugung der Verschlüsselungspassphrase behoben. (*Geprüft von Cynthia Shang. Gemeldet von bsiara.*)
- `repo-ls` mit `/` auf S3-Repositorys korrigiert. (*Geprüft von Cynthia Shang. Gemeldet von Lesovsky Alexey.*)

**Funktionen:**

- Unterstützung für mehrere Repositorys. (*Beigetragen von Cynthia Shang, David Steele. Geprüft von Stefan Fercot, Stephen Frost.*)
- GCS-Unterstützung für Repository-Speicher. (*Geprüft von Cynthia Shang, Daniel Farina.*)
- Option `archive-header-check` hinzugefügt. (*Geprüft von Stephen Frost, Cynthia Shang. Vorgeschlagen von Hans-Jürgen Schönig.*)

**Verbesserungen:**

- Neu erstellte Systemdatenbanken bei der selektiven Wiederherstellung eingeschlossen. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang.*)
- `content-length` aus den signierten S3-Headern ausgeschlossen. (*Geprüft von Cynthia Shang. Vorgeschlagen von Brian P Bockelman.*)
- Seltener verwendete Optionen für den Repository-Speicher zusammengefasst. (*Geprüft von Cynthia Shang.*)
- Benutzerdefinierten Standardwert für `config-path` mit `./configure --with-configdir` ermöglicht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)
- Kopieren des Archivs während `backup` protokolliert. (*Geprüft von Cynthia Shang, Stefan Fercot.*)

**Verbesserungen der Dokumentation:**

- Referenz um Links zu Beispielen im Benutzerhandbuch ergänzt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Dokumentation zur selektiven Wiederherstellung um Einschränkungen ergänzt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)
- Erläuterung zu `compress-type` in der Dokumentation zu `archive-copy` hinzugefügt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)
- Standardwerte für `compress-level` je Wert von `compress-type` hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Hinweis hinzugefügt, dass dieselben NFS-Einstellungen wie bei PostgreSQL erforderlich sind. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.32 – Versionshinweise {#v232-release-notes}

*Repository-Befehle*

*Veröffentlicht am 8. Februar 2021*

**Fehlerbehebungen:**

- Fortsetzen nach teilweiser Löschung des Backups durch einen vorherigen Fortsetzungsversuch korrigiert. (*Geprüft von Cynthia Shang. Gemeldet von Tom Swartz.*)

**Funktionen:**

- Befehl `repo-ls` hinzugefügt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)
- Befehl `repo-get` hinzugefügt. (*Beigetragen von Stefan Fercot, David Steele. Geprüft von Cynthia Shang.*)
- Option `archive-mode-check` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele, Michael Banck.*)

**Verbesserungen:**

- Leistung von `archive-get` verbessert. (*Geprüft von Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- Dokumentation des Befehls `expire` verbessert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.31 – Versionshinweise {#v231-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 7. Dezember 2020*

**Fehlerbehebungen:**

- `[`, `#` und `space` als erstes Zeichen in Datenbanknamen zugelassen. (*Geprüft von Stefan Fercot, Cynthia Shang. Gemeldet von Jefferson Alexandre.*)
- `standby.signal` nur unter PostgreSQL 12 erstellt, wenn der Typ von `restore` `standby` ist. (*Behoben von Stefan Fercot. Geprüft von David Steele. Gemeldet von Keith Fiske.*)

**Funktionen:**

- Abgelaufene Historiendateien entfernt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)
- Seitenprüfsummenfehler in der Ausgabe `text` des Befehls `info` gemeldet. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang.*)
- Option `repo-azure-endpoint` hinzugefügt. (*Geprüft von Cynthia Shang, Brian Peterson. Vorgeschlagen von Brian Peterson.*)
- Option `pg-database` hinzugefügt. (*Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Ausgabe des Befehls `info` verbessert, wenn eine Stanza angegeben ist, aber fehlt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang, David Steele. Vorgeschlagen von uspen.*)
- Leistung bei großen Dateilisten in den Befehlen `backup`/`restore` verbessert. (*Geprüft von Cynthia Shang, Oscar.*)
- Wiederholungsversuche für das Warten in PostgreSQL beim Start eines Backups hinzugefügt. (*Geprüft von Cynthia Shang. Vorgeschlagen von Vitaliy Kukharik.*)

**Verbesserungen der Dokumentation:**

- Dokumentation für RHEL/CentOS 6 durch RHEL/CentOS 8 ersetzt.


### v2.30 – Versionshinweise {#v230-release-notes}

*Unterstützung für PostgreSQL 13*

*Veröffentlicht am 5. Oktober 2020*

**Fehlerbehebungen:**

- Fehler mit Hinweisen ausgegeben, wenn der Backup-Benutzer `pg_settings` nicht lesen kann. (*Geprüft von Stefan Fercot, Cynthia Shang. Gemeldet von Mohamed Insaf K.*)

**Funktionen:**

- Unterstützung für PostgreSQL 13. (*Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Erkennung der PostgreSQL-Version verbessert. (*Geprüft von Cynthia Shang, Stephen Frost.*)
- Fehlermeldung zum Arbeitsverzeichnis verbessert. (*Geprüft von Stefan Fercot.*)
- Hinweis zum Starten der Stanza hinzugefügt, wenn das WAL-Segment nicht gefunden wird. (*Beigetragen von David Christensen. Geprüft von David Steele.*)
- Hinweis bei nicht übereinstimmenden Protokollversionen hinzugefügt. (*Geprüft von Cynthia Shang. Vorgeschlagen von loop-evgeny.*)

**Verbesserungen der Dokumentation:**

- Hinweis hinzugefügt, dass die pgBackRest-Versionen beim entfernten Betrieb übereinstimmen müssen. (*Geprüft von Cynthia Shang. Vorgeschlagen von loop-evgeny.*)
- Text zum info-Befehl in die Referenz verschoben und mit dem Benutzerhandbuch verknüpft. (*Geprüft von Cynthia Shang. Vorgeschlagen von Christophe Courtois.*)
- Pfad des yum-Repositorys im CentOS/RHEL-Benutzerhandbuch aktualisiert. (*Beigetragen von Heath Lord. Geprüft von David Steele.*)


### v2.29 – Versionshinweise {#v229-release-notes}

*Automatische S3-Zugangsdaten auf AWS*

*Veröffentlicht am 31. August 2020*

**Fehlerbehebungen:**

- Fehler beim Schließen von Prozessen `local`/`remote` unterdrückt. Da der Befehl bereits abgeschlossen ist, wäre ein Fehler kontraproduktiv. Eine **Warnung** weist weiterhin darauf hin, dass etwas Ungewöhnliches passiert ist. (*Geprüft von Cynthia Shang. Gemeldet von argdenis.*)
- Problem mit dem Zeichen `=` in Datei- oder Datenbanknamen behoben. (*Geprüft von Bastian Wegge, Cynthia Shang. Gemeldet von Brad Nicholson, Bastian Wegge.*)

**Funktionen:**

- Temporäre S3-Zugangsdaten auf AWS-Instanzen automatisch abgerufen. (*Beigetragen von David Steele, Stephen Frost. Geprüft von Cynthia Shang, David Youatt, Aleš Zelený, Jeanette Bromage.*)
- Option `archive-mode` hinzugefügt, um die Archivierung bei der Wiederherstellung zu deaktivieren. (*Geprüft von Stephen Frost. Vorgeschlagen von Stephen Frost.*)

**Verbesserungen:**

- Unterstützung für PostgreSQL 13 beta3. Änderungen an den Control-/Katalog-/WAL-Versionen in nachfolgenden Beta-Versionen können die Kompatibilität aufheben. pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.
- Asynchrones `list`/`remove` für S3/Azure-Speicher. (*Geprüft von Cynthia Shang, Stephen Frost.*)
- Speicherverbrauch bei der Erkennung nicht protokollierter Relationen während der Manifesterstellung verbessert. (*Geprüft von Cynthia Shang, Stephen Frost, Brad Nicholson, Oscar. Vorgeschlagen von Oscar, Brad Nicholson.*)
- Dateideskriptoren nach dem Abspalten des asynchronen Prozesses vorsorglich geschlossen. (*Geprüft von Stephen Frost, Cynthia Shang.*)
- Schließen der entfernten Backup-Verbindung bis nach der Archivprüfung verzögert. (*Beigetragen von Floris van Nee. Geprüft von David Steele.*)
- Detaillierte Fehlerausgabe verbessert. (*Geprüft von Cynthia Shang.*)
- TLS-Fehlermeldungen verbessert. (*Geprüft von Cynthia Shang, Stephen Frost.*)

**Fehlerbehebungen in der Dokumentation:**

- `none` zur Referenz der Option `compress-type` hinzugefügt und Beispiel korrigiert. (*Gemeldet von Ugo Bellavance, Don Seiler.*)
- Fehlenden Typ `azure` in der Referenz der Option `repo-type` hinzugefügt. (*Behoben von Don Seiler. Geprüft von David Steele.*)
- Tippfehler in der Referenz der Option `repo-cipher-type` korrigiert. (*Behoben von Don Seiler. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Klargestellt, dass `expire` regelmäßig ausgeführt werden muss, wenn `expire-auto` deaktiviert ist. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Douglas J Hunley.*)


### v2.28 – Versionshinweise {#v228-release-notes}

*Azure als Repository-Speicher*

*Veröffentlicht am 20. Juli 2020*

**Fehlerbehebungen:**

- Fehler behoben, durch den sich `restore` mit `--force` wie mit `--force --delta` verhielt. Dadurch ersetzte `restore` Dateien anhand von Zeitstempel und Größe, statt sie zu überschreiben. Einige Dateien, die hätten aktualisiert werden sollen, blieben deshalb unverändert. Normales `restore` und `restore` mit `--delta` waren von diesem Problem nicht betroffen. (*Geprüft von Cynthia Shang.*)

**Funktionen:**

- Azure-Unterstützung für Repository-Speicher. (*Geprüft von Cynthia Shang, Don Seiler.*)
- Option `expire-auto` hinzugefügt. Damit lässt sich das automatische Entfernen abgelaufener Daten nach einem erfolgreichen Backup deaktivieren. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang, David Steele.*)

**Verbesserungen:**

- Asynchroner mehrteiliger S3-Upload. (*Geprüft von Stephen Frost.*)
- Automatische Wiederholungsversuche für `backup`, `restore`, `archive-get` und `archive-push`. (*Geprüft von Cynthia Shang.*)
- Abfrageparallelität in PostgreSQL-Sitzungen zur Backup-Steuerung deaktiviert. (*Geprüft von Stefan Fercot.*)
- Unterstützung für PostgreSQL 13 beta2. Änderungen an den Control-/Katalog-/WAL-Versionen in nachfolgenden Beta-Versionen können die Kompatibilität aufheben. pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.
- Behandlung eines ungültigen HTTP-Antwortstatus verbessert. (*Geprüft von Cynthia Shang.*)
- Fehlermeldung bei fehlender Option `pg1-path` für den Befehl `archive-get` verbessert. (*Geprüft von Cynthia Shang.*)
- Hinweis hinzugefügt, wenn nach einem Timeline-Wechsel ein prüfsummenbasiertes Delta aktiviert wird. (*Geprüft von Matt Bunter, Cynthia Shang.*)
- PostgreSQL statt `postmaster` verwendet, wo es angebracht ist. (*Geprüft von Cynthia Shang.*)

**Fehlerbehebungen in der Dokumentation:**

- Falsches Beispiel für die Option `repo-retention-full-type` korrigiert. (*Gemeldet von Höseyin Sönmez.*)
- Interne Befehle aus der Befehlsreferenz in HTML und Manpages entfernt. (*Gemeldet von Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- PostgreSQL-Versionen zum Erstellen der Benutzerhandbücher aktualisiert. Außerdem Versionsbereiche hinzugefügt, um anzuzeigen, dass ein Benutzerhandbuch für einen Bereich von PostgreSQL-Versionen gilt, auch wenn es für eine bestimmte Version erstellt wurde. (*Geprüft von Stephen Frost.*)
- FAQ zum Entfernen eines bestimmten Backup-Satzes aktualisiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- FAQ zur Erläuterung des standardmäßigen PITR-Verhaltens aktualisiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.27 – Versionshinweise {#v227-release-notes}

*Verbessertes Entfernen abgelaufener Daten und Komprimierungstreiber*

*Veröffentlicht am 26. Mai 2020*

**Fehlerbehebungen:**

- Problem bei der Prüfung behoben, ob Datei-Links in Pfad-Links enthalten sind. (*Geprüft von Cynthia Shang. Gemeldet von Christophe Cavallié.*)
- `pg-path1` für synchrones `archive-push` optional gemacht. (*Geprüft von Cynthia Shang. Gemeldet von Jerome Peng.*)
- Der Befehl `expire` prüft nun, ob eine Stop-Datei vorhanden ist. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Fehlenden Begründungstext in HTTP-Antworten behandelt. (*Geprüft von Cynthia Shang. Gemeldet von Tenuun.*)
- Puffergröße für das Leeren des lz4-Komprimierungspuffers erhöht. (*Geprüft von Cynthia Shang. Gemeldet von Eric Radman.*)
- Optionen `pg-host*` und `repo-host*` für den Befehl `remote` ignoriert. (*Geprüft von Cynthia Shang. Gemeldet von Pavel Suderevsky.*)
- Möglicherweise fehlende Optionen `pg1-*` für den Befehl `remote` korrigiert. (*Geprüft von Cynthia Shang. Gemeldet von Andrew L'Ecuyer.*)

**Funktionen:**

- Zeitbasierte Aufbewahrung vollständiger Backups. Die Option `--repo-retention-full-type` ermöglicht die Aufbewahrung vollständiger Backups anhand eines in Tagen angegebenen Zeitraums. (*Beigetragen von Cynthia Shang, Pierre Ducroquet. Geprüft von David Steele.*)
- Gezieltes Entfernen von Backups. Benutzer können ein bestimmtes Backup unabhängig von den Aufbewahrungseinstellungen entfernen. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Unterstützung für Zstandard-Komprimierung. Die Einstellung `compress-type=zst` macht neue Backups und Archive mit früheren Versionen von pgBackRest inkompatibel; sie können damit nicht wiederhergestellt werden. (*Geprüft von Cynthia Shang.*)
- Unterstützung für bzip2-Komprimierung. Die Einstellung `compress-type=bz2` macht neue Backups und Archive mit früheren Versionen von pgBackRest inkompatibel; sie können damit nicht wiederhergestellt werden. (*Beigetragen von Stephen Frost. Geprüft von David Steele, Cynthia Shang.*)
- Status der laufenden Befehle `backup`/`expire` zum Befehl `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

**Verbesserungen:**

- WAL-Archive erst nach Erreichen des Schwellenwerts `repo-retention-archive` entfernt. Zuvor wurde WAL vor dem ersten vollständigen Backup nach diesem Backup entfernt. Nun bleibt es gemäß den Aufbewahrungseinstellungen erhalten. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Lokale MD5-Implementierung hinzugefügt, damit S3 bei aktiviertem FIPS funktioniert. (*Geprüft von Cynthia Shang, Stephen Frost. Vorgeschlagen von Brian Almeida, John Kelly.*)
- Unterstützung für PostgreSQL 13 beta1. Änderungen an den Control-/Katalog-/WAL-Versionen in nachfolgenden Beta-Versionen können die Kompatibilität aufheben. pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert. (*Geprüft von Cynthia Shang.*)
- Standardwert von `buffer-size` auf `1MiB` reduziert. (*Geprüft von Stephen Frost.*)
- Verständlichen Fehler ausgegeben, wenn `expire` nicht auf dem Repository-Host ausgeführt wird. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.26 – Versionshinweise {#v226-release-notes}

*Nicht blockierendes TLS*

*Veröffentlicht am 20. April 2020*

**Fehlerbehebungen:**

- Leeren Teilausdruck aus dem regulären Ausdruck für das Manifest entfernt. Dieser verursachte unter MacOS Probleme, während andere Plattformen offenbar korrekt funktionierten. (*Behoben von David Raftis. Geprüft von David Steele.*)

**Verbesserungen:**

- Nicht blockierende TLS-Implementierung. (*Geprüft von Slava Moudry, Cynthia Shang, Stephen Frost.*)
- Kopiergröße beim Backup nur für WAL-protokollierte Dateien begrenzt. Das bisherige Verhalten konnte dazu führen, dass `postgresql.conf` oder `postgresql.auto.conf` im Backup gekürzt wurden. (*Geprüft von Cynthia Shang.*)
- TCP-Keepalive-Optionen konfigurierbar gemacht. (*Vorgeschlagen von Marc Cousin.*)
- Option `io-timeout` hinzugefügt. (*Geprüft von Cynthia Shang.*)


### v2.25 – Versionshinweise {#v225-release-notes}

*Unterstützung für LZ4-Komprimierung*

*Veröffentlicht am 26. März 2020*

**Funktionen:**

- Unterstützung für lz4-Komprimierung hinzugefügt. Die Einstellung `compress-type=lz4` macht neue Backups und Archive mit früheren Versionen von pgBackRest inkompatibel; sie können damit nicht wiederhergestellt werden. (*Geprüft von Cynthia Shang.*)
- Option `--dry-run` zum Befehl `expire` hinzugefügt. Ein Probelauf zeigt, welche Backups/Archivdaten der Befehl `expire` entfernen würde, ohne tatsächlich etwas zu entfernen. (*Beigetragen von Cynthia Shang, Luca Ferrari. Geprüft von David Steele. Vorgeschlagen von Marc Cousin.*)

**Verbesserungen:**

- Leistung bei der entfernten Manifesterstellung verbessert. (*Vorgeschlagen von Jens Wilke.*)
- Erkennung von Keepalive-Optionen unter Linux korrigiert. (*Beigetragen von Marc Cousin. Geprüft von David Steele.*)
- Host-Erkennung in configure hinzugefügt, um Flags für Sprachstandards korrekt zu setzen. (*Beigetragen von Marc Cousin. Geprüft von David Steele.*)
- Optionen `compress`/`compress-level` aus Befehlen entfernt, die sie nicht nutzen. Diese Befehle (z. B. `restore`, `archive-get`) verwendeten die Komprimierungsoptionen nie, ließen sie aber in der Befehlszeile zu. Nun verursachen diese Optionen in der Befehlszeile einen Fehler. Entfernen Sie die ungenutzten Optionen, falls diese Fehler auftreten. (*Geprüft von Cynthia Shang.*)
- Kopiergröße von Backup-Dateien auf die zu Beginn des Backups gemeldete Größe begrenzt. Wächst eine Datei während des Backups, wird sie durch WAL-Wiedergabe während der Recovery rekonstruiert. Die zusätzlichen Daten müssen daher nicht kopiert werden. (*Geprüft von Cynthia Shang.*)


### v2.24 – Versionshinweise {#v224-release-notes}

*Automatische Auswahl eines Backup-Satzes für einen Zielzeitpunkt*

*Veröffentlicht am 25. Februar 2020*

**Fehlerbehebungen:**

- Zombieprozesse in asynchronen Archivbefehlen verhindert. (*Geprüft von Stephen Frost. Gemeldet von Adam Brusselback, ejberdecia.*)
- Fehler ausgegeben, wenn `archive-get`/`archive-push`/`restore` nicht auf einem PostgreSQL-Host ausgeführt werden. (*Geprüft von Stephen Frost. Gemeldet von Jesper St John.*)
- HTTP-Inhalt bis eof gelesen, wenn Größe/Kodierung nicht angegeben sind. (*Geprüft von Cynthia Shang. Gemeldet von Christian ROUX.*)
- Fortsetzen korrigiert, wenn das fortsetzbare Backup von Perl erstellt wurde. In diesem Fall sollte das fortsetzbare Backup ignoriert werden. Der C-Code konnte jedoch das von Perl geschriebene unvollständige Manifest nicht laden, da sich das Format geringfügig unterscheidet. Prüfungen hinzugefügt, um diesen Fall zu erkennen und ordnungsgemäß fortzufahren. (*Gemeldet von Kacey Holston.*)

**Funktionen:**

- Backup-Satz bei der Wiederherstellung automatisch ausgewählt, wenn ein Zielzeitpunkt angegeben ist. Die automatische Auswahl erfolgt nur, wenn `--set` nicht angegeben ist. Kann kein Backup-Satz für den angegebenen Zielzeitpunkt gefunden werden, wird der neueste Backup-Satz als Standard verwendet. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen:**

- Temporäre Datei `pg_internal.init` beim Backup übersprungen. (*Geprüft von Cynthia Shang. Vorgeschlagen von Michael Paquier.*)
- Weitere Prüfungen des Manifests bei `backup` hinzugefügt. (*Geprüft von Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- Verhindert, dass lock-bot Kommentare zu gesperrten Issues hinzufügt. (*Vorgeschlagen von Christoph Berg.*)


### v2.23 – Versionshinweise {#v223-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 27. Januar 2020*

**Fehlerbehebungen:**

- Beschädigung des Manifests durch fehlende Dateien behoben. Wenn PostgreSQL während des Backups eine Datei entfernte oder diese auf dem Standby fehlte, wurde möglicherweise die nächste Datei nicht kopiert und im Manifest aktualisiert. In diesem Fall führte die Wiederherstellung des Backups zu einem Fehler. (*Geprüft von Cynthia Shang. Gemeldet von Vitaliy Kukharik.*)

**Verbesserungen:**

- `pkg-config` statt `xml2-config` für libxml2-Build-Optionen verwendet. (*Beigetragen von David Steele, Adrian Vondendriesch.*)
- Bei `backup`/`restore` geprüft, ob Prüfsummen im Manifest gesetzt sind. (*Geprüft von Cynthia Shang.*)


### v2.22 – Versionshinweise {#v222-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 21. Januar 2020*

**Fehlerbehebungen:**

- Fehler bei der Timeline-Konvertierung behoben. Die Timeline wird benötigt, um nach einem Backup die WAL-Segmente im Archiv zu prüfen. Die Konvertierung erfolgte zur Basis `10` statt `16`, was bei Timelines ≥ `0xA` zu Fehlern führte. (*Gemeldet von Lukas Ertl, Eric Veldhuyzen.*)


### v2.21 – Versionshinweise {#v221-release-notes}

*Migration nach C abgeschlossen*

*Veröffentlicht am 15. Januar 2020*

**Fehlerbehebungen:**

- Fehler behoben, durch den asynchrone Befehle Optionen ignorierten. Die asynchronen Prozesse `archive-get`/`archive-push` luden keine Optionen aus befehlsspezifischen Konfigurationsabschnitten wie `[global:archive-get]`. (*Geprüft von Cynthia Shang. Gemeldet von Urs Kramer.*)
- Behandlung von `\` in Dateinamen korrigiert. `\` wurde bei der Berechnung der Manifest-Prüfsumme nicht korrekt maskiert, wodurch das Manifest nicht geladen werden konnte. Da `\` in Cluster-Dateinamen selten bis gar nicht vorkommen sollte, dürfte dies im praktischen Einsatz kein schwerwiegendes Problem sein.

**Funktionen:**

- pgBackRest besteht nun vollständig aus C-Code.
- Option `pg-user` hinzugefügt. Sie legt den Datenbankbenutzernamen für Verbindungen zu PostgreSQL fest. Ohne diese Angabe verbindet sich pgBackRest wie bisher mit dem lokalen Betriebssystembenutzer oder `PGUSER`. (*Beigetragen von Mike Palmiotto. Geprüft von David Steele.*)
- Pfadbasierte URIs im S3-Treiber zugelassen.

**Verbesserungen:**

- Der Befehl `backup` ist vollständig in C implementiert. (*Geprüft von Cynthia Shang.*)


### v2.20 – Versionshinweise {#v220-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 12. Dezember 2019*

**Fehlerbehebungen:**

- archive-push/archive-get bei symbolisch verknüpftem `PGDATA` korrigiert. Diese Befehle versuchten, `cwd()` als `PGDATA` zu verwenden. Bei symbolisch verknüpftem `PGDATA` wich dies jedoch vom in pgBackRest konfigurierten Pfad ab. Wenn `cwd()` nicht mit dem pgBackRest-Pfad übereinstimmt, wird mit `chdir()` in diesen Pfad gewechselt und sichergestellt, dass das nächste `cwd()` mit dem Ergebnis des ersten Aufrufs übereinstimmt. (*Gemeldet von Stephen Frost, Milosz Suchy.*)
- Referenzliste bei der Rekonstruktion von `backup.info` im Befehl `expire` korrigiert. Da der Befehl `backup` noch die Perl-Version der Rekonstruktion verwendet, tritt das Problem nur auf, wenn **1)** ein Backup in `backup.info` fehlt und **2)** der Befehl `expire` direkt ausgeführt wird, statt wie üblich nach `backup`. Aufgrund dieser unwahrscheinlichen Kombination dürfte dies im praktischen Einsatz kein Problem sein.
- Segfault bei unerwartetem EOF während der gzip-Dekomprimierung behoben. (*Gemeldet von Stephen Frost.*)


### v2.19 – Versionshinweise {#v219-release-notes}

*Migrationen nach C und Fehlerbehebungen*

*Veröffentlicht am 12. November 2019*

**Fehlerbehebungen:**

- Zeitüberschreitung auf der Gegenstelle bei Delta-Wiederherstellungen behoben. Bei einer Delta-Wiederherstellung eines weitgehend unveränderten Clusters konnte auf der Gegenstelle eine Zeitüberschreitung auftreten, wenn innerhalb von `protocol-timeout` keine Dateien aus dem Repository abgerufen wurden. Keepalives hinzugefügt, um dies zu verhindern. (*Gemeldet von James Sewell, Jens Wilke.*)
- Behandlung wiederholter HTTP-Header korrigiert. Wiederholte HTTP-Header sollten wie ein einzelner kommagetrennter Header behandelt werden, statt wie bisher einen Fehler auszulösen. (*Gemeldet von donicrosby.*)

**Verbesserungen:**

- JSON-Ausgabe des Befehls `info` nicht mehr zur besseren Lesbarkeit formatiert. Überwachungssysteme können JSON ohne Zeilenvorschübe leichter verarbeiten. Bei Bedarf können externe Werkzeuge wie `jq` die Ausgabe formatieren. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Der Befehl `check` ist vollständig in C implementiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Dokumentiert, wie man zu pgBackRest beitragen kann. (*Beigetragen von Cynthia Shang, David Steele.*)
- Höchste unterstützte Version für die Option `auto-stop` dokumentiert. (*Beigetragen von Brad Nicholson. Geprüft von David Steele.*)

**Verbesserungen der Testsuite:**

- Verwendung des Container-Testpfads bei `--vm=none` korrigiert. (*Vorgeschlagen von Stephen Frost.*)
- Nicht übereinstimmende Zeitzone im expect-Test korrigiert. (*Vorgeschlagen von Stephen Frost.*)
- Eingebetteten libc-Code standardmäßig nicht automatisch generiert. (*Vorgeschlagen von Stephen Frost.*)


### v2.18 – Versionshinweise {#v218-release-notes}

*Unterstützung für PostgreSQL 12*

*Veröffentlicht am 1. Oktober 2019*

**Funktionen:**

- Unterstützung für PostgreSQL 12.
- Option `set` zum Befehl `info` für eine detaillierte Textausgabe hinzugefügt. Die zusätzlichen Angaben umfassen Datenbanken für die selektive Wiederherstellung sowie eine Liste von Tablespaces und symbolischen Links mit ihren Standardzielen. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Stephen Frost, ejberdecia.*)
- Wiederherstellungstyp `standby` hinzugefügt. Dieser fügt für PostgreSQL < 12 automatisch standby_mode=on zu recovery.conf hinzu und erstellt für PostgreSQL ≥ 12 die Datei `standby.signal`. Dadurch entsteht eine gemeinsame Schnittstelle für verschiedene PostgreSQL-Versionen. (*Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Der Befehl `restore` ist vollständig in C implementiert. (*Geprüft von Cynthia Shang.*)

**Verbesserungen der Dokumentation:**

- Zusammenhang zwischen `db-timeout` und `protocol-timeout` dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von James Chanco Jr.*)
- Dokumentation zu Standby-Repositorys präzisiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- FAQ zur zeitbasierten Point-in-Time-Recovery hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v2.17 – Versionshinweise {#v217-release-notes}

*Migrationen nach C und Fehlerbehebungen*

*Veröffentlicht am 3. September 2019*

**Fehlerbehebungen:**

- Langsame Manifesterstellung bei sehr großen Mengen von Tabellen/Segmenten verbessert. (*Gemeldet von Jens Wilke.*)
- Ausschlüsse für spezielle Dateien korrigiert. (*Gemeldet von CluelessTechnologist, Janis Puris, Rachid Broum.*)

**Verbesserungen:**

- Die Befehle `stanza-create/update/delete` sind vollständig in C implementiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Die Befehle `start`/`stop` sind vollständig in C implementiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Protokollverzeichnisse/-dateien mit dem Modus `0750`/`0640` erstellt. (*Vorgeschlagen von Damiano Albani.*)

**Fehlerbehebungen in der Dokumentation:**

- Installation des Pakets `yum.p.o` korrigiert, wenn ein benutzerdefiniertes Paket angegeben ist. (*Gemeldet von Joe Ayers, John Harvey.*)

**Verbesserungen der Dokumentation:**

- pgBackRest als unprivilegierter Benutzer gebaut. (*Vorgeschlagen von Laurenz Albe.*)


### v2.16 – Versionshinweise {#v216-release-notes}

*Migrationen nach C und Fehlerbehebungen*

*Veröffentlicht am 5. August 2019*

**Fehlerbehebungen:**

- Bei S3-Fehlern `RequestTimeTooSkewed` Wiederholungsversuche durchgeführt, statt sofort abzubrechen. (*Gemeldet von sean0101n, Tim Garton, Jesper St John, Aleš Zelený.*)
- Falsche Behandlung von `transfer-encoding` in der Antwort auf eine `HEAD`-Anfrage korrigiert. (*Gemeldet von Pavel Suderevsky.*)
- Durch Optimierungen in gcc 9 aufgedeckte Verletzungen von Gültigkeitsbereichen korrigiert. (*Gemeldet von Christian Lange, Ned T. Crigler.*)

**Funktionen:**

- Option `repo-s3-port` zum Festlegen eines vom Standard abweichenden S3-Dienstports hinzugefügt.

**Verbesserungen:**

- Der Befehl `local` für `backup` ist vollständig in C implementiert. (*Beigetragen von David Steele, Cynthia Shang.*)
- Der Befehl `check` ist teilweise in C implementiert. (*Geprüft von Cynthia Shang.*)


### v2.15 – Versionshinweise {#v215-release-notes}

*C-Implementierung von Expire*

*Veröffentlicht am 25. Juni 2019*

**Fehlerbehebungen:**

- Zu aggressives Entfernen abgelaufener Daten bei der Archivaufbewahrung korrigiert. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Mohamad El-Rifai.*)

**Verbesserungen:**

- Der Befehl `expire` ist vollständig in C implementiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Der Befehl `local` für die Wiederherstellung ist vollständig in C implementiert.
- Fest codierten PostgreSQL-Benutzer entfernt, damit `$PGUSER` funktioniert. (*Vorgeschlagen von Julian Zhang, Janis Puris.*)
- Option `--prefix` von configure berücksichtigt. (*Vorgeschlagen von Daniel Westermann.*)
- Option `repo-s3-verify-ssl` in `repo-s3-verify-tls` umbenannt. Der neue Name wird bevorzugt, weil pgBackRest keine SSL-Protokollversion unterstützt; alle gelten als unsicher. Der alte Name wird weiterhin akzeptiert.

**Verbesserungen der Dokumentation:**

- FAQ zur Dokumentation hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- `wal_level=replica` in der Dokumentation für PostgreSQL ≥ 9.6 verwendet. (*Vorgeschlagen von Patrick McLaughlin.*)


### v2.14 – Versionshinweise {#v214-release-notes}

*Fehlerbehebung und Verbesserungen*

*Veröffentlicht am 20. Mai 2019*

**Fehlerbehebungen:**

- Segfault bei `process-max` > 8 für `archive-push`/`archive-get` behoben. (*Gemeldet von Jens Wilke.*)

**Verbesserungen:**

- Datenbankprüfungen übersprungen, wenn `stanza-delete` mit `force` ausgeführt wird. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von hatifnatt.*)
- Skript `configure` zur verbesserten Unterstützung mehrerer Plattformen hinzugefügt.

**Neue Inhalte der Dokumentation:**

- Benutzerhandbücher für CentOS/RHEL 6/7 hinzugefügt.


### v2.13 – Versionshinweise {#v213-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 18. April 2019*

**Fehlerbehebungen:**

- Probleme durch Lesevorgänge der Länge null für IO-Filter behoben, die diese nicht erwarteten. (*Gemeldet von brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru.*)
- Zuverlässigkeit der Fehlermeldungen aus Prozessen `local`/`remote` korrigiert.
- Posix/CIFS-Fehlermeldungen korrigiert, die beim Schreiben/Synchronisieren/Schließen den falschen Dateinamen meldeten.


### v2.12 – Versionshinweise {#v212-release-notes}

*C-Implementierung von Archive Push*

*Veröffentlicht am 11. April 2019*

**WICHTIGER HINWEIS**: Die neue TLS/SSL-Implementierung verbietet gemäß RFC-2818 Punkte in S3-Bucket-Namen. Diese Sicherheitskorrektur ist für eine standardkonforme Hostnamenprüfung erforderlich.

**Fehlerbehebungen:**

- Probleme behoben, wenn eine Pfadoption mit / endet. (*Gemeldet von Marc Cousin.*)
- Probleme behoben, wenn `log-level-file=off` für den Befehl `archive-get` gesetzt ist. (*Gemeldet von Brad Nicholson.*)
- C-Code korrigiert, sodass er wie Perl das Optionsformat `host:port` erkennt. (*Gemeldet von Kyle Nevins.*)
- Probleme mit Protokollierungsoptionen der Befehle `remote`/`local` behoben.

**Verbesserungen:**

- Der Befehl `archive-push` ist vollständig in C implementiert.
- Obergrenze für `process-max` auf `999` erhöht. (*Vorgeschlagen von Rakshitha-BR.*)
- Fehlermeldung verbessert, wenn ein S3-Bucket-Name Punkte enthält.

**Verbesserungen der Dokumentation:**

- Klargestellt, dass S3-kompatible Objektspeicher unterstützt werden. (*Vorgeschlagen von Magnus Hagander.*)


### v2.11 – Versionshinweise {#v211-release-notes}

*C-Implementierung von Archive Get*

*Veröffentlicht am 11. März 2019*

**Fehlerbehebungen:**

- Möglicherweise gekürzte WAL-Segmente bei einem Fehler während des Schreibens korrigiert. (*Gemeldet von blogh.*)
- Fehlende WAL-Minimum-/Maximum-Angaben im info-Befehl bei angegebener Stanza korrigiert. (*Behoben von Stefan Fercot. Geprüft von David Steele.*)
- Nicht standardkonformes JSON für von C an Perl übergebene Optionen korrigiert. (*Gemeldet von Leo Khomenko.*)

**Verbesserungen:**

- Der Befehl `archive-get` ist vollständig in C implementiert.
- Socket-Keepalive in älteren Perl-Versionen aktiviert. (*Beigetragen von Marc Cousin. Geprüft von David Steele.*)
- Fehler ausgegeben, wenn Parameter an einen Befehl übergeben werden, der keine Parameter akzeptiert. (*Vorgeschlagen von Jason O'Donnell.*)
- Hinweise hinzugefügt, wenn ein WAL-Segment im Archiv nicht gefunden werden kann. (*Vorgeschlagen von Hans-Jürgen Schönig.*)
- Fehlermeldung verbessert, wenn der Hostname in einem Zertifikat nicht gefunden werden kann. (*Vorgeschlagen von James Badger.*)
- Zusätzliche Optionen zu `backup.manifest` für die Fehlersuche hinzugefügt. (*Beigetragen von blogh. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Standardversion der Dokumentation auf PostgreSQL 10 aktualisiert.


### v2.10 – Versionshinweise {#v210-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 9. Februar 2019*

**Fehlerbehebungen:**

- Bisher nicht implementierte, für `archive-get` erforderliche Methode des S3-Treibers hinzugefügt. (*Gemeldet von mibiio.*)
- Prüfung auf falsch konfiguriertes `pg-path` korrigiert. (*Gemeldet von James Chanco Jr.*)


### v2.09 – Versionshinweise {#v209-release-notes}

*Kleinere Verbesserungen und Fehlerbehebungen*

*Veröffentlicht am 30. Januar 2019*

**Fehlerbehebungen:**

- Problem behoben, bei dem mehrere asynchrone Statusdateien einen zum Abbruch führenden Fehler verursachten. (*Gemeldet von Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley.*)

**Verbesserungen:**

- Der Befehl `info` ist vollständig in C implementiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Textmeldung des Befehls `info` vereinfacht, wenn keine Stanzas vorhanden sind. Den Repository-Pfad durch "the repository" ersetzt.
- Flag `_DARWIN_C_SOURCE` zum Makefile für MacOS-Builds hinzugefügt. (*Beigetragen von Douglas J Hunley. Geprüft von David Steele.*)
- Adressauflösung im C-TLS-Client auf moderne Verfahren umgestellt. (*Vorgeschlagen von Bruno Friedmann.*)
- Posix-konformen Header für `strcasecmp()` und `fd_set` eingebunden. (*Vorgeschlagen von ucando.*)

**Fehlerbehebungen in der Dokumentation:**

- Fest codierten Repository-Pfad korrigiert. (*Gemeldet von Heath Lord.*)

**Verbesserungen der Dokumentation:**

- Klargestellt, dass Verschlüsselung immer auf der Clientseite erfolgt. (*Vorgeschlagen von Bruce Burdick.*)
- Beispiele zum Einrichten eines Dokumentationshosts hinzugefügt.
- `if` in Manifestvariablen, Listen und Listeneinträgen zugelassen.


### v2.08 – Versionshinweise {#v208-release-notes}

*Kleinere Verbesserungen und Fehlerbehebungen*

*Veröffentlicht am 2. Januar 2019*

**Fehlerbehebungen:**

- Abruf der S3-Objektinformationen unmittelbar nach dem Hochladen entfernt. (*Gemeldet von Matt Kunkel.*)
- Typ von `archive-get-queue-max` auf `size` korrigiert. (*Gemeldet von Ronan Dunklau.*)
- Fehlermeldung hinzugefügt, wenn `uid`/`gid` des aktuellen Benutzers keinem Namen zugeordnet werden können. (*Gemeldet von Camilo Aguilar.*)
- Fehler ausgegeben, wenn `--target-action=shutdown` für PostgreSQL < 9.5 angegeben ist.

**Verbesserungen:**

- TCP-Keepalives für S3-Verbindungen gesetzt. (*Vorgeschlagen von Ronan Dunklau.*)
- Textausgabe des Befehls `info` so umgeordnet, dass das neueste Backup zuletzt ausgegeben wird. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Ryan Lambert.*)
- Dateieigentümer nur bei Bedarf geändert.
- Header `authentication` beim Ausgeben von S3-Fehlern geschwärzt. (*Vorgeschlagen von Brad Nicholson.*)

**Verbesserungen der Dokumentation:**

- Wirkung von `target-action` und Unterstützung durch PostgreSQL-Versionen erläutert. (*Vorgeschlagen von Keith Fiske.*)
- Klargestellt, dass Region/Endpunkt für den Bucket korrekt konfiguriert sein müssen. (*Vorgeschlagen von Pritam Barhate.*)
- Dokumentation zum Erstellen der Dokumentation hinzugefügt.


### v2.07 – Versionshinweise {#v207-release-notes}

*Automatisches prüfsummenbasiertes Backup-Delta*

*Veröffentlicht am 16. November 2018*

**Fehlerbehebungen:**

- Problem behoben, bei dem `archive-push-queue-max` bei Verbindungsfehlern nicht berücksichtigt wurde. (*Gemeldet von Lardière Sébastien.*)
- Verwendung einer festen WAL-Segmentgröße zur Feststellung einer Überschreitung von `archive-push-queue-max` korrigiert.
- Fehler nach fehlgeschlagenem Öffnen der Protokolldatei behoben, wenn die Verarbeitung fortgesetzt werden sollte. (*Gemeldet von vthriller.*)

**Funktionen:**

- Prüfsummenbasiertes Backup-Delta automatisch aktiviert, wenn Unregelmäßigkeiten wie ein Timeline-Wechsel erkannt werden. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen:**

- Bei allen S3-Fehlern `5xx` Wiederholungsversuche durchgeführt, statt nur bei internen Fehlern `500`. (*Vorgeschlagen von Craig A. James.*)


### v2.06 – Versionshinweise {#v206-release-notes}

*Prüfsummenbasiertes Delta-Backup und Unterstützung für PostgreSQL 11*

*Veröffentlicht am 15. Oktober 2018*

**Fehlerbehebungen:**

- Fehlende URI-Kodierung im S3-Treiber korrigiert. (*Gemeldet von Dan Farrell.*)
- Falsche Fehlermeldung für doppelte Optionen in Konfigurationsdateien korrigiert. (*Gemeldet von Jesper St John.*)
- Falsch als Fehler gemeldeten Rückgabewert in der Protokollierung auf Stufe `info` korrigiert. Ein Rückgabecode von 1 aus `archive-get` wurde auf Stufe `info` als Fehlermeldung protokolliert; ansonsten funktionierte der Vorgang korrekt.

**Funktionen:**

- Prüfsummenbasiertes Delta für inkrementelle Backups hinzugefügt. Solche Backups verwenden Prüfsummen statt Zeitstempeln, um festzustellen, ob sich Dateien geändert haben. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Unterstützung für PostgreSQL 11, einschließlich konfigurierbarer WAL-Segmentgröße.

**Verbesserungen:**

- Alle Dateien in einem verknüpften Tablespace-Verzeichnis außer dem Unterverzeichnis für die aktuelle PostgreSQL-Version ignoriert. Zuvor wurde ein Fehler ausgegeben, wenn andere Dateien vorhanden waren und nicht dem PostgreSQL-Benutzer gehörten.
- Befehl `info` verbessert, sodass er den Verschlüsselungstyp der Stanza anzeigt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Douglas J Hunley.*)
- Unterstützung für Sonderzeichen in Dateinamen verbessert.
- Angabe der Option `delta` in der pgBackRest-Konfigurationsdatei ermöglicht. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- `command` in `authorized_hosts` zur Verbesserung der SSH-Sicherheit verwendet. (*Vorgeschlagen von Stephen Frost, Magnus Hagander.*)
- Zulässige Werte für die Option `buffer-size` in der Konfigurationsreferenz aufgelistet. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Stéphane Schildknecht.*)


### v2.05 – Versionshinweise {#v205-release-notes}

*Optionen über Umgebungsvariablen und Ausschluss temporärer/nicht protokollierter Relationen*

*Veröffentlicht am 31. August 2018*

**Fehlerbehebungen:**

- Problem behoben, bei dem *relative* Links in `$PGDATA` mit falschem Pfad im Backup gespeichert werden konnten. Absolute Links waren nicht betroffen; relative Tablespace-Links wurden durch andere Prüfungen erkannt. (*Gemeldet von Cynthia Shang.*)
- Unvollständig implementierte Option `online` aus dem Befehl `check` entfernt. Der Offline-Betrieb widerspricht dem Zweck dieses Befehls: zu prüfen, ob Archivierung und Backups korrekt funktionieren. (*Gemeldet von Jason O'Donnell.*)
- Problem behoben, bei dem in C ausgelöste Fehler beim Aufruf aus Perl nicht protokolliert wurden. pgBackRest beendete sich ordnungsgemäß mit dem richtigen Fehlercode. Es fehlte jedoch eine Fehlermeldung zur Unterstützung der Fehlersuche. (*Gemeldet von Douglas J Hunley.*)
- Problem bei mehrfacher Angabe einer booleschen Option wie `delta` behoben. (*Gemeldet von Yogesh Sharma.*)

**Funktionen:**

- Festlegen beliebiger Optionen über Umgebungsvariablen ermöglicht. Dies umfasst Optionen, die zuvor nur in der Befehlszeile angegeben werden konnten, etwa `stanza`, sowie geheime Optionen, die nicht in der Befehlszeile angegeben werden durften, etwa `repo1-s3-key-secret`.
- Dateien temporärer und nicht protokollierter Relationen (Tabellen/Indizes) vom Backup ausgeschlossen. Die Implementierung verwendet dieselbe Logik wie die PostgreSQL-Patches [8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25) und [920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f), die diese Funktion hinzufügen. Temporäre Relationen werden ab PostgreSQL ≥ `9.0` ausgeschlossen. Nicht protokollierte Relationen werden ab PostgreSQL ≥ `9.1` ausgeschlossen, wo diese Funktion eingeführt wurde. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Ausschließen beliebiger Verzeichnisse und/oder Dateien von einem Backup ermöglicht. Ein falscher Einsatz dieser Funktion kann zu inkonsistenten Backups führen. Lesen Sie daher vor der Verwendung die Dokumentation zu `--exclude` sorgfältig. (*Geprüft von Cynthia Shang.*)
- Option `log-subprocess` hinzugefügt, um die Dateiprotokollierung für Unterprozesse `local` und `remote` zu ermöglichen.
- Unterstützung für PostgreSQL 11 Beta 3.

**Verbesserungen:**

- Dateien mit Größe null im Backup-Manifest dürfen unabhängig von der Zeitstempeldifferenz auf ein vorheriges Manifest verweisen. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Leistung von asynchronem `archive-get`/`archive-push` durch direkte Prüfung der Statusdateien verbessert. (*Beigetragen von Stephen Frost. Geprüft von David Steele.*)
- Fehlermeldung verbessert, wenn einem Befehl die Option `stanza` fehlt. (*Vorgeschlagen von Sarah Conway.*)

**Fehlerbehebungen in der Dokumentation:**

- Ungültige Protokollierungsstufe in der Referenz der Option `log-path` korrigiert. (*Gemeldet von Camilo Aguilar.*)

**Verbesserungen der Dokumentation:**

- Versuche eingestellt, Mitwirkende in `release.xml` nach Nach-/Vornamen zu ordnen. Die Namen wurden in den Versionshinweisen stets genau wie angegeben dargestellt. Wir versuchten jedoch, interne IDs anhand von Nach-/Vornamen zu vergeben, was schwer zu bestimmen sein kann und letztlich keinen Sinn ergibt. Angeregt durch Christophes Vortrag auf der PostgresOpen 2017: „Menschen haben keinen Primärschlüssel“. (*Vorgeschlagen von Christophe Pettus.*)

**Verbesserungen der Testsuite:**

- Fehler ausgegeben, wenn LibC außerhalb der Testumgebung gebaut wird. LibC wird für Produktionsbuilds nicht mehr benötigt.


### v2.04 – Versionshinweise {#v204-release-notes}

*Kritischer Fehler beim Fortsetzen von Backups behoben*

*Veröffentlicht am 5. Juli 2018*

**WICHTIGER HINWEIS**: Diese Version behebt einen kritischen Fehler beim Fortsetzen von Backups. Alle vor dieser Version fortgesetzten Backups sollten als inkonsistent betrachtet werden. Ein Backup wird nach einem vorherigen fehlgeschlagenen Backup fortgesetzt, sofern nicht `resume=n` angegeben wurde. Ein fortgesetztes Backup lässt sich an der Meldung "aborted backup of same type exists, will be cleaned to remove invalid files and resumed" im Backup-Protokoll erkennen. Wenn diese Meldung vorhanden ist, verwenden Sie weder dieses Backup noch ein anderes Backup desselben Satzes für eine Wiederherstellung. Prüfen Sie außerdem die Wiederherstellungsprotokolle darauf, ob ein fortgesetztes Backup wiederhergestellt wurde. Falls ja, können sich inkonsistente Daten im Cluster befinden.

**Fehlerbehebungen:**

- Kritischen Fehler beim Fortsetzen behoben, der zu inkonsistenten Backups führte. Eine Regression in `v0.82` entfernte den Zeitstempelvergleich bei der Entscheidung, welche Dateien des abgebrochenen Backups beim Fortsetzen beibehalten werden. Weitere Einzelheiten stehen im Hinweis oben. (*Gemeldet von David Youatt, Yogesh Sharma, Stephen Frost.*)
- Fehler bei der selektiven Wiederherstellung behoben, wenn nur eine Benutzerdatenbank im Cluster vorhanden ist. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Nj Baliyan.*)
- Nicht ISO-8601-konformes Zeitstempelformat in S3-Autorisierungsheadern korrigiert. AWS und einige Gateways tolerierten Stundenangaben mit führenden Leerzeichen statt Nullen, andere jedoch nicht. (*Behoben von Andrew Schwartz. Geprüft von David Steele.*)

**Funktionen:**

- Unterstützung für PostgreSQL 11 Beta 2.

**Verbesserungen:**

- HTTP-Client verbessert, sodass er `content-length` auf 0 setzt, wenn der Server den Wert nicht angibt. S3 und Gateways setzen immer `content-length` oder `transfer-encoding`. `HTTP 1.1` verlangt dies jedoch nicht, und Proxys wie HAProxy geben möglicherweise keinen der beiden Header an. (*Vorgeschlagen von Adam K. Sumner.*)
- `search_path = 'pg_catalog'` für PostgreSQL-Verbindungen gesetzt. (*Vorgeschlagen von Stephen Frost.*)

**Verbesserungen der Dokumentation:**

- Neuen Abschnitt zum Bauen von pgBackRest und zum Build auf einem separaten Host erstellt.
- Beispiel einer S3-Richtlinie zur Beschränkung von Bucket-Berechtigungen hinzugefügt. (*Vorgeschlagen von Douglas J Hunley, Jason O'Donnell.*)


### v2.03 – Versionshinweise {#v203-release-notes}

*Bereitstellung einer einzigen ausführbaren Datei*

*Veröffentlicht am 22. Mai 2018*

**Fehlerbehebungen:**

- Möglichen Pufferüberlauf bei der Verarbeitung von Fehlermeldungen behoben. (*Gemeldet von Lætitia.*)
- Setzen einer Archivschreibsperre für den synchronen Befehl `archive-get` korrigiert. (*Gemeldet von uspen.*)

**Verbesserungen:**

- Exportierte C-Funktionen und Perl-Module direkt in die ausführbare pgBackRest-Datei eingebettet.
- `time_t` statt `__time_t` zur besseren Portierbarkeit verwendet. (*Vorgeschlagen von Nick Floersch.*)
- Gesamtlaufzeit in Millisekunden am Ende des Befehls ausgegeben.


### v2.02 – Versionshinweise {#v202-release-notes}

*Paralleles asynchrones Archive Get und zusätzliche Konfigurationsdateien*

*Veröffentlicht am 6. Mai 2018*

**Fehlerbehebungen:**

- Rekursive Verzeichnissynchronisierung korrigiert, wenn nur das angegebene Verzeichnis synchronisiert werden sollte. (*Gemeldet von Craig A. James.*)
- Fehler "path not found" von `archive-copy` bei inkrementellen/differenziellen Backups behoben. (*Gemeldet von yummyliu, Vitaliy Kukharik.*)
- Fehler bei der Manifesterstellung behoben, wenn zwei oder mehr Dateien in `PGDATA` mit demselben Verzeichnis verknüpft sind. (*Gemeldet von Vitaliy Kukharik.*)
- Fehlschlagen der Delta-Wiederherstellung bei fehlender verknüpfter Datei behoben.
- Darstellung von Schlüssel-Wert- und Listenoptionen in der Hilfe korrigiert. (*Gemeldet von Clinton Adams.*)

**Funktionen:**

- Asynchrones, paralleles `archive-get` hinzugefügt. Diese Funktion hält eine Warteschlange von WAL-Segmenten vor, um die Latenz zu verringern, wenn PostgreSQL ein WAL-Segment mit restore_command anfordert.
- Unterstützung für zusätzliche pgBackRest-Konfigurationsdateien hinzugefügt. Das Verzeichnis wird über die Option `--config-include-path` angegeben. Option `--config-path` hinzugefügt, um den Standard-Basispfad der Optionen `--config` und `--config-include-path` zu überschreiben. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Option `repo-s3-token` hinzugefügt, um temporäre Zugangstokens konfigurieren zu können. pgBackRest kann derzeit keine neuen Zugangsdaten anfordern. Daher muss der gesamte Befehl, etwa `backup` oder `restore`, abgeschlossen sein, bevor die Zugangsdaten ablaufen. (*Beigetragen von Yogesh Sharma. Geprüft von David Steele.*)

**Verbesserungen:**

- Optionen `archive-push-queue-max`, `manifest-save-threshold` und `buffer-size` aktualisiert, sodass sie Werte in `KB`, `MB`, `GB`, `TB` oder `PB` mit einer Potenz von `1024` als Multiplikator akzeptieren. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Pfadsynchronisierung bei Backup/Wiederherstellung effizienter gestaltet. Das Durchsuchen des gesamten Verzeichnisses kann bei vielen kleinen Tabellen sehr aufwendig sein. Daher wird die Pfadliste im Backup-Manifest zur Synchronisierung verwendet, statt den Backup-/Wiederherstellungspfad zu durchsuchen.
- Befehlsparameter zusätzlich zu den Befehlsoptionen in der anfänglichen info-Protokollmeldung angezeigt.
- Option archive-queue-max in archive-push-queue-max umbenannt. Dies entspricht der neuen Option `archive-get-queue-max`. Der alte Optionsname wird weiterhin akzeptiert.

**Fehlerbehebungen in der Dokumentation:**

- Dokumentation um 32-Bit-Unterstützung und Einschränkungen ergänzt. Die 32-Bit-Unterstützung wurde in v1.26 hinzugefügt. (*Gemeldet von Viorel Tabara.*)

**Verbesserungen der Dokumentation:**

- Überwachungsbeispiele mit PostgreSQL und jq hinzugefügt. (*Vorgeschlagen von Stephen Frost, Brian Faherty.*)
- Beispiel für die Verwendung eines Befehlsabschnitts zur Archivierungskonfiguration hinzugefügt. (*Vorgeschlagen von Christophe Courtois.*)
- Beschreibung von `info --output=json` als experimentell aus der Dokumentation entfernt.
- Veraltete Beschreibung der Option `spool-path` aktualisiert.

**Neue Funktionen der Testsuite:**

- lcov für Berichte zur Abdeckung der C-Unittests verwendet. Wechsel von Devel::Cover, da es für aus gcov konvertierte Berichte keine Zweigabdeckung meldete. Eine unvollständige Zweigabdeckung eines Moduls erzeugt nun einen Fehler. Die Abdeckung der Unittests wird im Bericht nur angezeigt, wenn ihre Anweisungs- oder Zweigabdeckung unvollständig ist.


### v2.01 – Versionshinweise {#v201-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 19. März 2018*

**Fehlerbehebungen:**

- Fehler behoben, durch den die Optionen `--target-action` und `--recovery-option` bei Wiederherstellungen mit `--type=immediate` als ungültig gemeldet wurden. (*Gemeldet von Brad Nicholson.*)
- Sofort einen Fehler ausgegeben, wenn eine geheime Option wie `repo1-s3-key` in der Befehlszeile übergeben wird. Da pgBackRest geheime Optionen nicht an Unterprozesse weitergab, wurde zuvor ein unklarer Fehler ausgelöst. Der neue Fehler ist wesentlich deutlicher und enthält Hinweise zur Behebung. Die Befehlsdokumentation wurde angepasst, um geheime Optionen, die nicht in der Befehlszeile angegeben werden können, auszulassen. (*Gemeldet von Brad Nicholson.*)
- Problem bei der Übergabe von `--no-config` an eingebettetes Perl behoben. (*Gemeldet von Ibrahim Edib Kokdemir.*)
- Problem behoben, bei dem `log-level-stderr` > `warn` beim Beenden eines Prozesses `local`/`remote` einen Fehler verursachte, weil unerwartete Ausgabe auf stderr vorlag. Der Höchstwert für Prozesse `local`/`remote` ist nun `error`, da es für diese Prozesse keinen Grund gibt, Warnungen auszugeben. (*Gemeldet von Clinton Adams.*)
- Manifesttest im Befehl `check` bei vorhandenen Tablespaces korrigiert. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Thomas Flatley.*)

**Verbesserungen:**

- Fehler ausgegeben, wenn in der Konfigurationsdatei mehrere Argumente für eine Option gesetzt werden, die keine mehreren Argumente akzeptiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Überflüssige sudo-Befehle aus `src/Makefile` entfernt. (*Beigetragen von Adrian Vondendriesch. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Index in Beispielen für indizierte Optionen angezeigt, also `repo-*` und `pg-*`. (*Vorgeschlagen von Stephen Frost.*)
- Inhaltsverzeichnis auf der Befehlsseite vereinfacht, indem nur Befehle aufgeführt werden. (*Vorgeschlagen von Stephen Frost.*)
- Verweise auf den optionalen Charakter der C-Bibliothek entfernt.

**Neue Funktionen der Testsuite:**

- Paket-Builds für CentOS/RHEL hinzugefügt.
- clang für die statische Codeanalyse verwendet. Anfangs wurden nur einige Funktionen gefunden, die mit `__noreturn__` hätten gekennzeichnet werden sollen.


### v2.00 – Versionshinweise {#v200-release-notes}

*Leistungsverbesserungen bei der WAL-Archivierung*

*Veröffentlicht am 23. Februar 2018*

**Funktionen:**

- Der Befehl `archive-push` ist jetzt teilweise in C implementiert. Dadurch läuft der PostgreSQL-`archive_command` deutlich schneller, wenn er Statusmeldungen des asynchronen Archivierungsprozesses verarbeitet. (*Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Der Befehl `check` prüft jetzt, ob das Backup-Manifest erstellt werden kann. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Leistung des HTTPS-Clients verbessert. Die Pufferung berücksichtigt jetzt die `pending`-Bytes am Socket, sofern vorhanden, statt sich ausschließlich auf `select()` zu verlassen. In manchen Fällen wurden die letzten Bytes erst beim Schließen der Verbindung ausgegeben.
- Leistung beim Löschen in S3 verbessert. Die Konstante `S3_BATCH_MAX` war vermutlich während Tests durch den fest codierten Wert 2 ersetzt worden.
- Jede Option, die nicht ausschließlich auf der Befehlszeile verfügbar ist, kann nun auf der Befehlszeile auf ihren Standardwert zurückgesetzt werden. Damit lassen sich Optionen aus `pgbackrest.conf` zurücksetzen, sodass seltener neue Konfigurationsdateien für besondere Anforderungen nötig sind.
- Die C-Bibliothek ist jetzt erforderlich. Dadurch entfällt das bedingte Laden, und neue Bibliotheksfunktionen lassen sich leichter entwickeln.
- Die ausführbare Datei `pgbackrest` ist jetzt ein C-Programm statt eines Perl-Programms. Dadurch laufen bestimmte zeitkritische Befehle wie das asynchrone `archive-push` schneller.
- Für eine einheitlichere Benennung wurden `db-*`-Optionen in `pg-*` und `backup-*`-Optionen in `repo-*` umbenannt. `repo-*`-Optionen sind jetzt indiziert, obwohl derzeit nur ein Repository zulässig ist.

**Neue Inhalte der Dokumentation:**

- Alle Cluster in der Dokumentation werden mit Prüfsummen initialisiert.

**Verbesserungen der Dokumentation:**

- Veraltete Optionsnamen in der Dokumentation und Befehlszeilenhilfe aufgeführt.
- Klargestellt, dass S3-Buckets vom Benutzer erstellt werden müssen. (*Vorgeschlagen von David Youatt.*)


### v1.29 – Versionshinweise {#v129-release-notes}

*Behebung eines kritischen Fehlers beim Fortsetzen von Backups*

*Veröffentlicht am 5. Juli 2018*

**WICHTIGER HINWEIS**: Diese Version behebt einen kritischen Fehler beim Fortsetzen von Backups. Alle vor dieser Version fortgesetzten Backups sollten als inkonsistent betrachtet werden. Nach einem fehlgeschlagenen Backup wird dieses fortgesetzt, sofern nicht `resume=n` angegeben wurde. Ein fortgesetztes Backup lässt sich an der Meldung "aborted backup of same type exists, will be cleaned to remove invalid files and resumed" im Backup-Protokoll erkennen. Ist diese Meldung vorhanden, darf weder dieses Backup noch ein anderes Backup desselben Satzes zur Wiederherstellung verwendet werden. Außerdem ist in den Wiederherstellungsprotokollen zu prüfen, ob ein fortgesetztes Backup wiederhergestellt wurde. Ist dies der Fall, können inkonsistente Daten im Cluster vorliegen.

**Fehlerbehebungen:**

- Kritischen Fehler beim Fortsetzen behoben, der zu inkonsistenten Backups führte. Durch eine Regression in `v0.82` entfiel der Zeitstempelvergleich bei der Entscheidung, welche Dateien des abgebrochenen Backups beim Fortsetzen beibehalten werden. Einzelheiten stehen im Hinweis oben. (*Gemeldet von David Youatt, Yogesh Sharma, Stephen Frost.*)
- Nicht ISO-8601-konformes Zeitstempelformat in S3-Autorisierungsheadern korrigiert. AWS und einige Gateways akzeptierten Stundenangaben mit führenden Leerzeichen statt Nullen, andere dagegen nicht. (*Behoben von Andrew Schwartz. Geprüft von David Steele.*)
- Fehler behoben, bei dem Verzeichnisse rekursiv synchronisiert wurden, obwohl nur das angegebene Verzeichnis synchronisiert werden sollte. (*Gemeldet von Craig A. James.*)
- Fehler behoben, bei dem die Optionen `--target-action` und `--recovery-option` bei der Wiederherstellung mit `--type=immediate` als ungültig gemeldet wurden. (*Gemeldet von Brad Nicholson.*)
- Fehler behoben, bei dem `archive-copy` bei inkrementellen oder differenziellen Backups die Meldung "path not found" ausgab. (*Gemeldet von yummyliu, Vitaliy Kukharik.*)
- Fehler beim Erstellen des Manifests behoben, wenn zwei oder mehr Dateien in `PGDATA` mit demselben Verzeichnis verknüpft sind. (*Gemeldet von Vitaliy Kukharik.*)
- Fehler behoben, durch den die Delta-Wiederherstellung bei einer fehlenden verknüpften Datei scheiterte.
- Fehler bei der selektiven Wiederherstellung behoben, wenn der Cluster nur eine Benutzerdatenbank enthält. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Nj Baliyan.*)

**Verbesserungen:**

- Der HTTP-Client setzt `content-length` jetzt auf 0, wenn der Server keinen Wert angibt. S3 und entsprechende Gateways setzen stets `content-length` oder `transfer-encoding`; `HTTP 1.1` verlangt dies jedoch nicht, und Proxys wie HAProxy können beide weglassen. (*Vorgeschlagen von Adam K. Sumner.*)
- Leistung des HTTPS-Clients verbessert. Die Pufferung berücksichtigt jetzt die `pending`-Bytes am Socket, sofern vorhanden, statt sich ausschließlich auf `select()` zu verlassen. In manchen Fällen wurden die letzten Bytes erst beim Schließen der Verbindung ausgegeben.
- Leistung beim Löschen in S3 verbessert. Die Konstante `S3_BATCH_MAX` war vermutlich während Tests durch den fest codierten Wert 2 ersetzt worden.
- Pfadsynchronisierung bei Backups und Wiederherstellungen effizienter gestaltet. Das gesamte Verzeichnis einzulesen, kann bei vielen kleinen Tabellen sehr aufwendig sein. Statt den Backup- oder Wiederherstellungspfad einzulesen, wird nun die Pfadliste im Backup-Manifest für die Synchronisierung verwendet. Die nicht mehr benötigte rekursive Pfadsynchronisierung wurde entfernt.

**Fehlerbehebungen in der Dokumentation:**

- Dokumentation um die 32-Bit-Unterstützung und ihre Einschränkungen ergänzt. Die 32-Bit-Unterstützung wurde in v1.26 eingeführt. (*Gemeldet von Viorel Tabara.*)

**Verbesserungen der Dokumentation:**

- Klargestellt, dass S3-Buckets vom Benutzer erstellt werden müssen. (*Vorgeschlagen von David Youatt.*)
- Veraltete Beschreibung der Option `spool-path` aktualisiert.


### v1.28 – Versionshinweise {#v128-release-notes}

*Stanzas löschen*

*Veröffentlicht am 1. Februar 2018*

**Fehlerbehebungen:**

- Fehler behoben, durch den eine einzelne Datenbank in einem Tablespace nicht mit --db-include wiederhergestellt werden konnte. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Chiranjeevi Ravilla.*)
- Beim Abgleich von `archive.info` mit `backup.info` wird jetzt sichergestellt, dass die neueste `db-id` gewählt wird. Dies gewährleistet die richtige Zuordnung bei doppelten Werten für `system-id` und `db-version`, etwa nach dem Rückgängigmachen eines `pg_upgrade`. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Adam K. Sumner.*)
- Übermäßig ausführliche Fehlermeldung bei einem ungültigen Befehl korrigiert. (*Gemeldet von Jason O'Donnell.*)

**Funktionen:**

- Befehl `stanza-delete` zum Entfernen ungenutzter Stanzas hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Magnus Hagander.*)

**Verbesserungen:**

- Der Befehl `stanza-create` gibt keinen Fehler mehr aus, wenn die Stanza bereits existiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Dokumentation zu `stanza-create --force` um einen ausdrücklichen Hinweis auf die gebotene Vorsicht ergänzt. (*Vorgeschlagen von Jason O'Donnell.*)


### v1.27 – Versionshinweise {#v127-release-notes}

*Fehlerbehebungen und Dokumentation*

*Veröffentlicht am 19. Dezember 2017*

**Fehlerbehebungen:**

- Fehler behoben, der Meldungen über einen falschen Ausführungsort für `backup` und `restore` unterdrückte. Ist ein Backup-Host vorhanden, sollten Backups nur dort und Wiederherstellungen nur auf dem Datenbank-Host zulässig sein, sofern nicht eine alternative Konfiguration erstellt wird, die den entfernten Host ignoriert. (*Gemeldet von Lardière Sébastien.*)
- Fehler behoben, durch den WAL unter PostgreSQL 10 nicht entfernt wurde. Ursache war ein fehlerhafter regulärer Ausdruck, der für alle PostgreSQL-Hauptversionen folgendes Format erwartete: X.X. (*Gemeldet von Adam Brusselback.*)
- Fehler behoben, durch den `--no-config` nicht an Kindprozesse übergeben wurde. Diese lasen daher weiterhin die lokale Konfigurationsdatei, was unerwartetes Verhalten verursachen konnte.
- Befehl `info` korrigiert, sodass `"db (prior)"` nicht mehr ausgegeben wird, wenn für eine frühere Version des Clusters weder Backups noch Archive vorhanden sind. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Stephen Frost.*)

**Neue Inhalte der Dokumentation:**

- Zusammenhang zwischen den Optionen `archive-copy` und `archive-check` dokumentiert. (*Vorgeschlagen von Markus Nullmeier.*)
- Referenzdokumentation zu `archive-copy` verbessert.


### v1.26 – Versionshinweise {#v126-release-notes}

*Repository-Verschlüsselung*

*Veröffentlicht am 21. November 2017*

**Fehlerbehebungen:**

- Fehler behoben, der beim Wiederherstellen das Kopieren großer Manifeste scheitern lassen konnte. (*Gemeldet von Craig A. James.*)
- Falschen WAL-Offset auf 32-Bit-Architekturen korrigiert. (*Behoben von Javier Wilson. Geprüft von David Steele.*)
- Fehler beim Abrufen von WAL für alte Datenbankversionen behoben. Nach einem `stanza-upgrade` sollte es weiterhin möglich sein, Backups der vorherigen Version wiederherzustellen und mit `archive-get` eine Recovery durchzuführen. Allerdings prüfte archive-get nur die neueste Datenbankversion und -kennung und scheiterte deshalb. Zudem wurden Probleme bereinigt, wenn dieselbe Datenbankversion und -kennung mehrfach in der Historie vorkommt. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Clinton Adams.*)
- Fehler bei der Wiederherstellung von Gruppen behoben, die im Backup ungültig waren. Kann das Backup einer Gruppe keinen Namen zuordnen, speichert es die Gruppe im Manifest als `false`. Bei der Wiederherstellung verwendet es dann den Eigentümer von $PGDATA zum Setzen der Gruppe oder, falls dies nicht möglich ist, die Gruppe des aktuellen Benutzers. Diese Logik funktionierte nicht richtig: Die gewählte Gruppe überschrieb bei der Wiederherstellung den Benutzer. Dadurch blieb die Gruppe undefiniert, und der Benutzer wurde fälschlich auf die Gruppe gesetzt. (*Gemeldet von Jeff McCormick.*)
- Fehler bei der Parameterübergabe an entfernte Prozesse behoben. Bei mehreren angegebenen Datenbanken wurden stets Pfad, Port und Socket-Pfad von db1 übergeben, unabhängig davon, welche Datenbank tatsächlich angesprochen wurde. (*Gemeldet von uspen.*)

**Funktionen:**

- Unterstützung für Repository-Verschlüsselung. (*Beigetragen von Cynthia Shang, David Steele.*)

**Verbesserungen:**

- gzip-Filter bei `--compress-level-network=0` deaktiviert. Der Filter wurde mit Komprimierungsstufe 0 verwendet und verursachte dadurch Aufwand ohne Nutzen.
- Dekomprimierung im gzip-Filter beschleunigt.

**Neue Inhalte der Dokumentation:**

- Vorlage hinzugefügt, um bei Problemmeldungen von Anfang an bessere Informationen zu erhalten. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Verwendung der Option `archive-timeout` verdeutlicht und ihren Unterschied zur PostgreSQL-Einstellung archive_timeout beschrieben. (*Beigetragen von Cynthia Shang. Geprüft von David Steele. Vorgeschlagen von Keith Fiske.*)

**Neue Funktionen der Testsuite:**

- Automatisierte Tests für die 32-Bit-Architektur i386/i686.


### v1.25 – Versionshinweise {#v125-release-notes}

*Leistungsverbesserungen für S3*

*Veröffentlicht am 24. Oktober 2017*

**Fehlerbehebungen:**

- Fehler behoben, durch den benutzerdefinierte Werte für `compress-level` ignoriert wurden. (*Gemeldet von Jens Wilke.*)
- Fehlermeldung bei überlappenden Timelines entfernt. Überlappende Timelines sind in vielen Szenarien der Point-in-Time-Recovery (PITR) zulässig. (*Gemeldet von blogh.*)
- Fälle korrigiert, in denen `database-id` in der JSON-Ausgabe von info nicht als Ganzzahl dargestellt wurde. (*Behoben von Cynthia Shang. Geprüft von David Steele. Gemeldet von Jason O'Donnell.*)

**Funktionen:**

- Listenabfragen in S3 beschleunigt. Ein literaler Anfangsteil des Filterausdrucks wird als Suchpräfix verwendet. Dadurch bleibt die Anfrage oft klein genug, um eine Ratenbegrenzung zu vermeiden. (*Vorgeschlagen von Mihail Shvein.*)

**Neue Funktionen der Testsuite:**

- I/O-Leistungstests hinzugefügt.


### v1.24 – Versionshinweise {#v124-release-notes}

*Neue Backup-Ausschlüsse*

*Veröffentlicht am 28. September 2017*

**Fehlerbehebungen:**

- Fehler behoben, bei dem während der Initialisierung eines Backups vom Standby Warnungen statt Protokollmeldungen niedrigerer Priorität ausgegeben wurden. (*Gemeldet von uspen.*)
- Fehler behoben, durch den einige `db-*`-Optionen wie `db-port` nicht an entfernte Prozesse übergeben wurden. (*Gemeldet von uspen.*)

**Funktionen:**

- Inhalte von `pg_snapshots`, `pg_serial`, `pg_notify` und `pg_dynshmem` vom Backup ausgeschlossen, da sie beim Start neu erstellt werden.
- Dateien namens `pg_internal.init` vom Backup ausgeschlossen, da sie beim Start neu erstellt werden.

**Verbesserungen:**

- Protokolldatei erst öffnen, wenn der asynchrone Prozess vollständig vom Hauptprozess getrennt ist, damit dieser nicht ebenfalls in die Datei schreibt. (*Vorgeschlagen von Jens Wilke.*)

**Neue Inhalte der Dokumentation:**

- Konfiguration für SSH ohne Passwort hinzugefügt.

**Verbesserungen der Dokumentation:**

- In der Dokumentation „master“ gemäß der PostgreSQL-Konvention durch „primary“ ersetzt.


### v1.23 – Versionshinweise {#v123-release-notes}

*Mehrere Standbys und Unterstützung für PostgreSQL 10*

*Veröffentlicht am 3. September 2017*

**Fehlerbehebungen:**

- Fehler behoben, durch den die Komprimierung bei wachsenden Dateien abbrechen konnte. (*Gemeldet von Jesper St John, Aleksandr Rogozin.*)
- Fehler behoben, durch den der lokale Prozess keine Keep-alives an den entfernten Prozess sendete. (*Gemeldet von William Cox.*)

**Funktionen:**

- Für Backups vom Standby können bis zu sieben Standbys konfiguriert werden. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Unterstützung für PostgreSQL 10.
- Beim Lesen von XML-Daten zusätzlich zur Übertragung in Blöcken (Chunked Encoding) auch `content-length` zugelassen, um die Kompatibilität mit S3-Gateways von Drittanbietern zu verbessern. (*Vorgeschlagen von Victor Gdalevich.*)

**Verbesserungen:**

- HTTP-Zeitlimit für S3 erhöht.
- Wiederholungen von HTTP-Anfragen hinzugefügt, um vorübergehende S3-Netzwerkfehler besser abzufangen.

**Fehlerbehebungen in der Dokumentation:**

- Dokumentgenerierung korrigiert, sodass Abschnittszusammenfassungen auf der Konfigurationsseite erscheinen. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)


### v1.22 – Versionshinweise {#v122-release-notes}

*Fehler bei S3-Wiederholungen behoben*

*Veröffentlicht am 9. August 2017*

**Fehlerbehebungen:**

- Authentifizierungsfehler bei S3-Wiederholungen behoben.


### v1.21 – Versionshinweise {#v121-release-notes}

*Verbesserte info-Ausgabe und Option für den SSH-Port*

*Veröffentlicht am 8. August 2017*

**Fehlerbehebungen:**

- Das Verzeichnis `archive_status` wird jetzt bei der Wiederherstellung neu erstellt, um PostgreSQL 8.3 zu unterstützen. Anders als neuere Versionen erstellt diese Version es nicht automatisch neu. (*Gemeldet von Stephen Frost.*)
- Fehler behoben, durch den das leere Archivverzeichnis einer alten PostgreSQL-Version nach einem `stanza-upgrade` zurückbleiben konnte. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)

**Funktionen:**

- Befehl `info` in der Text- und JSON-Ausgabe so geändert, dass er die Archiv-ID sowie das kleinste und größte derzeit im Archiv vorhandene WAL-Segment für die aktuelle und gegebenenfalls frühere Version des Datenbankclusters anzeigt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Optionen `--backup-ssh-port` und `--db-ssh-port` zur Unterstützung abweichender SSH-Ports hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen:**

- Anfrage wiederholen, wenn S3 einen internen Fehler (500) zurückgibt.

**Fehlerbehebungen in der Dokumentation:**

- Beschreibung von `--online` entsprechend dem jeweiligen Befehlskontext korrigiert.

**Neue Inhalte der Dokumentation:**

- Erstellung von `/etc/pgbackrest.conf` in die Anleitung zur manuellen Installation aufgenommen.

**Verbesserungen der Dokumentation:**

- Repository-Optionen in der Befehls- und Befehlszeilenhilfe in einen eigenen Abschnitt verschoben. (*Vorgeschlagen von Stephen Frost.*)


### v1.20 – Versionshinweise {#v120-release-notes}

*Kritischen Fehler für 8.3/8.4 behoben*

*Veröffentlicht am 27. Juni 2017*

**WICHTIGER HINWEIS**: PostgreSQL-Installationen der Versionen 8.3 und 8.4, die Tablespaces verwenden, sollten sofort von jeder v1-Version aktualisiert werden und ein vollständiges Backup durchführen. Ein Fehler verhinderte ausschließlich in diesen Versionen die Sicherung von Tablespaces. PostgreSQL ≥ 9.0 ist nicht betroffen.

**Fehlerbehebungen:**

- Fehler behoben, der Backups von Tablespaces unter PostgreSQL ≤ 8.4 verhinderte.
- Beim Bau der C-Bibliothek ein fehlendes Flag ergänzt. Dessen Fehlen führte auf 32-Bit-Systemen zu einer unpassenden Binärdatei. (*Gemeldet von Adrian Vondendriesch.*)

**Funktionen:**

- Optionen `s3-repo-ca-path` und `s3-repo-ca-file` hinzugefügt, um Systeme zu unterstützen, auf denen `IO::Socket::SSL` CAs nicht automatisch findet, etwa RHEL7, oder um eigene CAs zu laden. (*Vorgeschlagen von Scott Frazer.*)

**Neue Funktionen der Testsuite:**

- Dokumentations-Builds in CI aufgenommen.


### v1.19 – Versionshinweise {#v119-release-notes}

*Unterstützung für S3*

*Veröffentlicht am 12. Juni 2017*

**Fehlerbehebungen:**

- Befehl `info` korrigiert, sodass die angezeigten kleinsten und größten WAL-Segmente im Archiv zur aktuellen Datenbankversion gehören. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Befehl `backup` korrigiert, sodass `backup-standby` zurückgesetzt und das Backup auf dem Primärserver fortgesetzt wird, wenn der Standby nicht konfiguriert und/oder nicht erreichbar ist. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Fehler behoben, durch den Konfigurationswarnungen eines entfernten Prozesses Fehler im Hauptprozess auslösten. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)

**Funktionen:**

- Unterstützung für Repositorys auf Amazon S3. (*Geprüft von Cynthia Shang.*)

**Fehlerbehebungen in der Dokumentation:**

- Ungültige Option `max-archive-mb` in der Konfigurationsreferenz durch `archive-queue-max` ersetzt.
- Fehlendes `sudo` im Installationsabschnitt ergänzt. (*Behoben von Lætitia. Geprüft von David Steele.*)


### v1.18 – Versionshinweise {#v118-release-notes}

*Stanza-Upgrades, Refactoring und verbesserte Sperren*

*Veröffentlicht am 12. April 2017*

**Fehlerbehebungen:**

- Fehler behoben, bei dem lesende Operationen mit lokalen Arbeitsprozessen, etwa `restore`, Schreibsperren erzeugten, die paralleles `archive-push` beeinträchtigen konnten. (*Gemeldet von Jens Wilke.*)

**Funktionen:**

- Befehl stanza-upgrade hinzugefügt, um nach einem Upgrade auf eine neue PostgreSQL-Hauptversion auch die Stanza aktualisieren zu können. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Validierung von `pgbackrest.conf` hinzugefügt, die bei ungültigen Optionen oder Optionen im falschen Abschnitt warnt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen:**

- Sperrkonzept vereinfacht. Jetzt hält nur der Hauptprozess Schreibsperren für `archive-push` und `backup`, statt wie bisher alle lokalen und entfernten Arbeitsprozesse.
- Zeitstempel der Dateien in den Backup-Verzeichnissen nicht mehr an die Zeitstempel im Clusterverzeichnis angleichen. Dies diente ursprünglich zum Fortsetzen von Backups, das inzwischen mit Prüfsummen umgesetzt ist.
- Fehlermeldung verbessert, wenn `restore` die Datei `postmaster.pid` erkennt. (*Vorgeschlagen von Yogesh Sharma.*)
- Rückgabecodes im Bereich 25 bis 125 neu nummeriert, damit PostgreSQL einige davon nicht als schwerwiegende Signalfehler interpretiert. (*Vorgeschlagen von Yogesh Sharma.*)


### v1.17 – Versionshinweise {#v117-release-notes}

*Fehler bei Seitenprüfsummen behoben*

*Veröffentlicht am 13. März 2017*

**Fehlerbehebungen:**

- Fehler behoben, durch den neu initialisierte, aber ungenutzte Seiten Warnungen zu Seitenprüfsummen auslösten. (*Gemeldet von Stephen Frost.*)


### v1.16 – Versionshinweise {#v116-release-notes}

*Verbesserte Seitenprüfsummen, CI und Pakettests*

*Veröffentlicht am 2. März 2017*

**Fehlerbehebungen:**

- Fehler behoben, bei dem Tabellen über 1GB nach dem ersten Segment Warnungen zu Seitenprüfsummen ausgaben. (*Gemeldet von Stephen Frost.*)
- Fehler behoben, bei dem Datenbanken mit einem vom Standard abweichenden Tablespace fälschlich warnten, dass `pg_filenode.map` und `pg_internal.init` nicht an Seitengrenzen ausgerichtet seien. (*Gemeldet von blogh.*)

**Neue Funktionen der Testsuite:**

- Kontinuierliche Integration mit `travis-ci`.
- Automatisierter Bau von Debian-Paketen für alle unterstützten Distributionen.


### v1.15 – Versionshinweise {#v115-release-notes}

*Refactoring und Fehlerbehebungen*

*Veröffentlicht am 13. Februar 2017*

**Fehlerbehebungen:**

- In v1.13 eingeführte Regression behoben, durch die Backups scheitern konnten, wenn während der Manifest-Erstellung Dateien entfernt wurden, etwa durch das Löschen von Tabellen. (*Gemeldet von Navid Golpayegani.*)


### v1.14 – Versionshinweise {#v114-release-notes}

*Refactoring und Fehlerbehebungen*

*Veröffentlicht am 13. Februar 2017*

**Fehlerbehebungen:**

- Fehler behoben, bei dem ein fehlgeschlagenes archive-push nicht erneut versucht wurde, sondern PostgreSQL dauerhaft Fehler erhielt, sofern die `.error`-Datei nicht manuell gelöscht wurde. (*Gemeldet von Jens Wilke.*)
- Wettlaufsituation bei paralleler Archivierung behoben, in der das Erstellen neuer Pfade einen Fehler auslöste, wenn mehrere Prozesse dies gleichzeitig versuchten. (*Gemeldet von Jens Wilke.*)

**Verbesserungen:**

- Ermittlung von `wal archive min/max` durch den Befehl `info` beschleunigt. (*Vorgeschlagen von Jens Wilke.*)

**Neue Inhalte der Dokumentation:**

- Dokumentation zur asynchronen Archivierung aktualisiert, um die neue Funktionsweise und die Unterschiede zur alten Methode genauer zu beschreiben. (*Vorgeschlagen von Jens Wilke.*)


### v1.13 – Versionshinweise {#v113-release-notes}

*Parallele Archivierung, Stanza-Erstellung sowie verbessertes info und check*

*Veröffentlicht am 5. Februar 2017*

**WICHTIGER HINWEIS**: Die neue Implementierung der asynchronen Archivierung kopiert WAL nicht mehr in eine separate Warteschlange. Nach dem Upgrade auf `1.13` noch in der alten Warteschlange vorhandenes WAL wird aufgegeben und **nicht** in das Repository übertragen. Um dies zu verhindern, zunächst die Archivierung mit `archive_command = false` anhalten. Danach die asynchrone Warteschlange mit `pgbackrest --stanza=[stanza-name] archive-push` leeren und warten, bis der Prozess abgeschlossen ist. Prüfen, dass die Warteschlange in `[spool-path]/archive/[stanza-name]/out` leer ist. Abschließend `1.13` installieren und den ursprünglichen `archive_command` wiederherstellen. **WICHTIGER HINWEIS**: Der Befehl `stanza-create` ist nicht mehr optional und muss ausgeführt werden, bevor Backups oder Archivierung für eine **neue** Stanza möglich sind. Für bereits vorhandene Stanzas muss `stanza-create` nicht ausgeführt werden.

**Fehlerbehebungen:**

- const-Zuweisung korrigiert, die beim Kompilieren der C-Bibliothek eine Warnung auslöste. (*Behoben von Adrian Vondendriesch. Geprüft von David Steele.*)
- Einige für `--repo-sync` fehlende Verzeichnissynchronisierungen ergänzt.
- Fehler behoben, durch den ein fehlender Benutzer oder eine fehlende Gruppe bei der Wiederherstellung in `File->owner()` den Fehler "uninitialized value" auslösen konnte. (*Gemeldet von Leonardo GG Avellar.*)
- Fehler behoben, bei dem Meldungen über Protokollabweichungen den erwarteten Wert nicht ausgaben.
- Irreführende Protokollmeldung von `archive-get` korrigiert, die den Exit-Code 1 als ungewöhnlichen Abbruch bezeichnete.

**Funktionen:**

- Verbesserte Implementierung der asynchronen Archivierung mit mehreren Prozessen.
- `stanza-create` so verbessert, dass es beschädigte Repositorys in den meisten Fällen reparieren kann und robust genug ist, um verpflichtend zu werden. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- `check` kann jetzt auf einem Standby ausgeführt werden. Dabei erfolgen nur grundlegende Prüfungen, da `pg_switch_xlog()` auf einem Replikat nicht ausgeführt werden kann. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- WAL-Bereiche für Archiv und Backups zum Befehl `info` hinzugefügt.
- Warnung hinzugefügt, beim Neuzuordnen von Tablespaces unter PostgreSQL < 9.2 auch `pg_tablespace.spclocation` zu aktualisieren. (*Beigetragen von blogh. Geprüft von David Steele.*)
- Sperren auf entfernten Hosts für `archive-get`, `restore`, `info` und `check` nicht mehr voraussetzen, da diese Befehle nur lesend zugreifen. (*Vorgeschlagen von Michael Vitale.*)

**Verbesserungen:**

- Kopfzeile der Protokolldatei erst beim Schreiben des ersten Protokolleintrags ausgeben. (*Vorgeschlagen von Jens Wilke.*)
- Durch Filterung anhand der LSN zum Backup-Beginn das Risiko verringert, dass unvollständig geschriebene Seiten fälschlich Fehler bei Seitenprüfsummen melden.
- Intel-spezifische Optimierung aus den Build-Flags der C-Bibliothek entfernt. (*Beigetragen von Adrian Vondendriesch. Geprüft von David Steele.*)
- Option `--lock` entfernt. Sie wurde eingeführt, bevor das Sperrverzeichnis außerhalb des Repositorys liegen konnte, und ist inzwischen überholt.
- Option `--log-timestamp` hinzugefügt, um Zeitstempel in Protokollen unterdrücken zu können. Sie dient hauptsächlich dazu, Filter in der automatisch erzeugten Dokumentation zu vermeiden.
- Korrekten Fehlercode zurückgeben, wenn ein relativer Pfad nicht in einen absoluten umgewandelt werden kann. (*Vorgeschlagen von Yogesh Sharma.*)

**Neue Inhalte der Dokumentation:**

- Option `process-max` im Benutzerhandbuch dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v1.12 – Versionshinweise {#v112-release-notes}

*Seitenprüfsummen, Konfiguration und Fehlerbehebungen*

*Veröffentlicht am 12. Dezember 2016*

**WICHTIGER HINWEIS**: In früheren Versionen konnten auf der Befehlszeile Optionen angegeben werden, die für den aktuellen Befehl ungültig waren, ohne einen Fehler auszulösen. Ungültige Optionen erzeugen jetzt einen Fehler. Daher ist es wichtig, die Befehlszeilenoptionen in Ihrer Umgebung sorgfältig zu prüfen, um Störungen zu vermeiden.

**Fehlerbehebungen:**

- Fehler behoben, durch den für den jeweiligen Befehl ungültige Optionen ohne Fehlermeldung auf der Befehlszeile angegeben werden konnten. Die Optionen wurden ignoriert und änderten das Verhalten nicht, führten aber zu Verwirrung. Ungültige Optionen erzeugen jetzt einen Fehler. (*Gemeldet von Nikhilchandra Kulkarni.*)
- Fehler behoben, durch den interne symbolische Verknüpfungen für Tablespaces im Repository nicht erstellt wurden. Dies fiel nur auf, wenn Cluster mithilfe von Dateisystem-Snapshots manuell am Speicherort gestartet werden sollten; normale Backups und Wiederherstellungen waren nicht betroffen.
- Fehler behoben, der die Fehlerausgabe auf der Konsole vor der Initialisierung der Protokollierung verhinderte, etwa beim Einlesen von Optionen. Fehlercodes wurden weiterhin korrekt zurückgegeben; ein fehlgeschlagener Prozess erschien dadurch also nicht als erfolgreich. (*Gemeldet von Adrian Vondendriesch.*)
- Fehler behoben, durch den eine auf dem Backup-Server angegebene `db-port`-Option nur dann korrekt an den entfernten Prozess übergeben wurde, wenn sie zur ersten konfigurierten Datenbank gehörte. (*Gemeldet von Michael Vitale.*)

**Funktionen:**

- Option `--checksum-page` hinzugefügt, mit der pgBackRest Seitenprüfsummen in Datendateien validieren kann, wenn Prüfsummen unter PostgreSQL >= 9.3 aktiviert sind. Diese Funktion erfordert eine C-Bibliothek, die anfangs möglicherweise noch nicht in Betriebssystempaketen enthalten ist. Die Option wird automatisch aktiviert, wenn die Bibliothek vorhanden ist und Prüfsummen im Cluster aktiviert sind. (*Vorgeschlagen von Stephen Frost.*)
- Option `--repo-link` hinzugefügt, um interne symbolische Verknüpfungen zu unterdrücken, wenn das Dateisystem des Repositorys sie nicht unterstützt. Dies beeinträchtigt keine pgBackRest-Funktion. Die Verknüpfung `latest` und die internen Tablespace-Verknüpfungen werden jedoch nicht erstellt, was das manuelle Starten von Clustern am Speicherort mittels Dateisystem-Snapshots beeinträchtigt.
- Option `--repo-sync` hinzugefügt, um Verzeichnissynchronisierungen im Repository für Dateisysteme zu deaktivieren, die sie nicht unterstützen, etwa NTFS.
- Einheitlichen Protokolleintrag hinzugefügt, der den erfolgreichen Abschluss eines Befehls meldet. Ein erfolgreiches Backup endet beispielsweise mit: `INFO: backup command end: completed successfully`. (*Vorgeschlagen von Jens Wilke.*)

**Verbesserungen:**

- Zur Vereinfachung wird `pg_control` jetzt zusammen mit den übrigen Dateien kopiert, statt separat am Ende des Vorgangs. Der Befehl `backup` benötigt dieses bisherige Verhalten nicht; `restore` kopiert in eine temporäre Datei, die am Ende der Wiederherstellung umbenannt wird.

**Fehlerbehebungen in der Dokumentation:**

- Fehler behoben, der Ausnahmen bei PDF-Builds unterdrückte.
- In v1.10 eingeführte Regression bei Abschnittslinks behoben.

**Neue Inhalte der Dokumentation:**

- Aufbewahrung in den Schnellstartabschnitt aufgenommen.


### v1.11 – Versionshinweise {#v111-release-notes}

*Fehler bei der Effizienz asynchroner Archivierung behoben*

*Veröffentlicht am 17. November 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den die asynchrone Archivierung pro Ausführung nur eine Datei statt mehrerer Dateien als Gruppe übertrug. Diese in v1.09 eingeführte Regression beeinträchtigte nur die Effizienz; alle WAL-Segmente wurden im asynchronen Modus korrekt archiviert. (*Gemeldet von Stephen Frost.*)


### v1.10 – Versionshinweise {#v110-release-notes}

*Stanza-Erstellung und kleinere Fehlerbehebungen*

*Veröffentlicht am 8. November 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den ein Backup scheitern konnte, wenn zwischen Backups keine Datenbankänderungen erfolgt waren und sich nur `pg_control` geändert hatte.
- Fehler behoben, durch den Tablespace-Pfade mit demselben Präfix einen Fehler wegen einer ungültigen Verknüpfung auslösten. (*Gemeldet von Nikhilchandra Kulkarni.*)

**Funktionen:**

- Befehl `stanza-create` hinzugefügt, um Stanzas im Repository ausdrücklich anzulegen. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen:**

- Überflüssige `use lib`-Anweisungen aus Perl-Modulen entfernt. (*Vorgeschlagen von Devrim Gündüz.*)


### v1.09 – Versionshinweise {#v109-release-notes}

*Unterstützung für 9.6, Konfigurierbarkeit und Fehlerbehebungen*

*Veröffentlicht am 10. Oktober 2016*

**Fehlerbehebungen:**

- Befehl `check` korrigiert, sodass bei fehlendem Backup-Verzeichnis keine Fehlermeldung protokolliert wird. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Fehlermeldung korrigiert, damit bei einem ungültigen Archivierungsbefehl dieser korrekt angezeigt wird. (*Gemeldet von Jason O'Donnell.*)
- Fehler behoben, durch den der asynchrone Archivierer nicht gestartet wurde, wenn `archive-push` nicht genügend Platz hatte, um ein neues WAL-Segment einzureihen. Dadurch wurde die Warteschlange ohne manuellen Eingriff, etwa einen direkten Aufruf von `archive-push`, nie geleert. PostgreSQL erhält weiterhin Fehler, wenn der Speicherplatz für neue WAL-Segmente fehlt; der asynchrone Prozess wird jedoch trotzdem gestartet, damit schließlich wieder Platz frei wird. (*Gemeldet von Jens Wilke.*)
- Zeitüberschreitung beim entfernten Prozess behoben, die auftrat, wenn ein lokaler Prozess beim Fortsetzen oder Wiederherstellen Prüfsummen berechnete, aber keine Dateien kopierte und der entfernte Prozess dadurch untätig blieb. (*Gemeldet von Jens Wilke.*)

**Funktionen:**

- Unter PostgreSQL 9.6 werden automatisch nicht exklusive Backups verwendet.
- Option `cmd-ssh` hinzugefügt, um den ssh-Client anzugeben. (*Vorgeschlagen von Jens Wilke.*)
- Option `log-level-stderr` hinzugefügt, die steuert, ob Konsolenmeldungen an `stderr` oder `stdout` gesendet werden. Der Standardwert ist `warn`. Dies ändert das Verhalten gegenüber früheren Versionen, auch wenn es intuitiver sein mag. Mit `log-level-stderr=off` bleibt das bisherige Verhalten erhalten. (*Vorgeschlagen von Sascha Biberhofer.*)
- `application_name` für Datenbankverbindungen auf `"pgBackRest [command]"` setzen. (*Vorgeschlagen von Jens Wilke.*)
- Prüfen, ob archive_mode aktiviert ist, wenn die Option `archive-check` aktiviert ist.

**Verbesserungen:**

- Fehlermeldung beim erfolglosen Anfordern der kooperativen pgBackRest-Sperre verdeutlicht, damit klar ist, dass es sich nicht um eine PostgreSQL-Backup-Sperre handelt. (*Vorgeschlagen von Jens Wilke.*)
- pgBackRest-Versionsnummer in die INFO-Protokollausgabe beim Befehlsstart aufgenommen.
- Prozess-ID in der INFO-Protokollausgabe beim Starten und Stoppen lokaler Prozesse protokolliert.

**Neue Inhalte der Dokumentation:**

- Option `archive-timeout` im Benutzerhandbuch dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v1.08 – Versionshinweise {#v108-release-notes}

*Fehlerbehebungen und verbesserte Protokollierung*

*Veröffentlicht am 14. September 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den lokale Prozesse nach Abschluss die Verbindung nicht trennten und später eine Zeitüberschreitung auslösen konnten. (*Gemeldet von Todd Vernick.*)
- Fehler behoben, durch den die Protokollschicht beim Warten auf WAL-Segmente im Archiv eine Zeitüberschreitung auslösen konnte. (*Gemeldet von Todd Vernick.*)

**Verbesserungen:**

- Dateiprotokollausgabe bis zum Erstellen der Datei zwischenspeichern, damit das Protokoll vollständiger ist.


### v1.07 – Versionshinweise {#v107-release-notes}

*Umstellung von Threads auf Prozesse und Fehlerbehebungen*

*Veröffentlicht am 7. September 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den Tablespaces bei einem Backup vom Standby vom Primärserver kopiert wurden.
- Befehl `check` korrigiert, sodass Backup-Informationen auch auf dem entfernten Host und nicht nur lokal geprüft werden. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Fehler behoben, durch den `retention-archive` bei `retention-archive-type=diff` nicht automatisch gesetzt wurde. Dadurch wurden Archive weniger konsequent als beabsichtigt entfernt. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)

**Funktionen:**

- Perl-Threads zur Verbesserung von Kompatibilität und Leistung durch Prozesse ersetzt.
- Inhalte von `$PGDATA/pg_replslot` ausschließen, damit Replikationsslots des Primärservers nicht in das Backup gelangen.
- `archive-start` und `archive-stop` werden jetzt auch bei `archive-check=n` in `backup.manifest` eingetragen. (*Vorgeschlagen von Jens Wilke.*)
- Zusätzliche Warnungen, wenn die Einstellungen zur Archivaufbewahrung möglicherweise nicht die beabsichtigte Wirkung haben oder eine unbegrenzte Aufbewahrung erlauben. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Experimentelle Unterstützung für nicht exklusive Backups unter PostgreSQL 9.6 rc1. Änderungen der Control-, Katalog- oder WAL-Versionen in späteren Release-Kandidaten können die Kompatibilität aufheben; pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.

**Fehlerbehebungen in der Dokumentation:**

- Kleinere Probleme bei der Reproduzierbarkeit der Dokumentation im Zusammenhang mit Binärpfaden behoben.

**Neue Inhalte der Dokumentation:**

- Archivaufbewahrung dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v1.06 – Versionshinweise {#v106-release-notes}

*Backups vom Standby und Fehlerbehebungen*

*Veröffentlicht am 25. August 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den eine Tablespace-Verknüpfung, die auf eine weitere Verknüpfung zeigte, keinen Fehler auslöste, sondern den Tablespace vollständig übersprang. (*Gemeldet von Michael Vitale.*)
- Fehler behoben, durch den Optionen, die nur einen Wert zulassen sollten, mehrfach ohne Fehlermeldung in `pgbackrest.conf` angegeben werden konnten. (*Gemeldet von Michael Vitale.*)
- Fehler behoben, durch den `protocol-timeout` nicht automatisch erhöht wurde, wenn `db-timeout` erhöht wurde. (*Gemeldet von Todd Vernick.*)

**Funktionen:**

- Backups von einem Standby-Cluster. Zum Starten und Stoppen des Backups sowie zum Kopieren nicht replizierter Dateien ist weiterhin eine Verbindung zum Primärcluster erforderlich. Der weitaus größte Teil der Dateien wird jedoch vom Standby kopiert, um den Primärserver zu entlasten.
- Flexiblere Datenbankkonfiguration. Primärserver und Standby können beide auf dem Backup-Server konfiguriert werden; pgBackRest erkennt automatisch, welcher der Primärserver ist. Bei einem separaten Backup-Server sind daher nach einem Failover vom Primärserver zum Standby keine Änderungen an der Backup-Konfiguration nötig.
- Verzeichnisse vom Backup ausschließen, die PostgreSQL beim Start leert, neu erstellt oder mit Nullen füllt. Dazu gehören `pgsql_tmp` und `pg_stat_tmp`. Zusätzlich zu den bereits ausgeschlossenen Dateien `backup_label.old`, `postmaster.opts`, `postmaster.pid`, `recovery.conf` und `recovery.done` wird nun auch `postgresql.auto.conf.tmp` ausgeschlossen.
- Experimentelle Unterstützung für nicht exklusive Backups unter PostgreSQL 9.6 beta4. Änderungen der Control-, Katalog- oder WAL-Versionen in späteren Betaversionen können die Kompatibilität aufheben; pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.

**Verbesserungen:**

- Fehlermeldung bei der Manifest-Erstellung für Verknüpfungen verbessert, die auf weitere Verknüpfungen zeigen.
- Fehlermeldung bei relativen Pfaden in `archive-push` oder `archive-get` um Hinweise ergänzt.
- Backup-Protokollmeldungen verbessert, sodass erkennbar ist, von welchem Host Dateien kopiert werden.


### v1.05 – Versionshinweise {#v105-release-notes}

*Fehler bei der Prüfung von Tablespace-Verknüpfungen behoben*

*Veröffentlicht am 9. August 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den Tablespace-Pfade mit $PGDATA als Teilzeichenfolge als Unterverzeichnisse von $PGDATA erkannt wurden, obwohl sie keine waren. Auch die Prüfung relativer Pfade wurde etwas verschärft. (*Gemeldet von Chris Fort.*)

**Neue Inhalte der Dokumentation:**

- Planung von Backups mit cron dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

**Verbesserungen der Dokumentation:**

- Liste ausstehender Aufgaben von der pgBackRest-Website in das Wiki des GitHub-Repositorys verschoben. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v1.04 – Versionshinweise {#v104-release-notes}

*Verschiedene Fehlerbehebungen*

*Veröffentlicht am 30. Juli 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den ein überflüssiger entfernter Prozess erstellt wurde. Dadurch konnten Backups oder Wiederherstellungen mit Threads eine Zeitüberschreitung und/oder einen Sperrkonflikt auslösen. (*Gemeldet von Michael Vitale.*)
- Fehler behoben, durch den db-path für `check` nicht vorgeschrieben war. Fehlte der Wert, wurde deshalb eine Assertion statt einer verständlichen Fehlermeldung ausgelöst. (*Gemeldet von Michael Vitale.*)
- Befehl `check` korrigiert, sodass er einen Fehler ausgibt, wenn Datenbankversion oder -kennung nicht mit dem Archiv übereinstimmen. (*Behoben von Cynthia Shang. Geprüft von David Steele.*)
- Fehler behoben, durch den ein entfernter Prozess selbst einen entfernten Prozess starten konnte, wenn `backup-host` in der `pgbackrest.conf` auf dem Datenbankserver fehlte. (*Gemeldet von Lardière Sébastien.*)
- Fehler behoben, durch den die Inhalte von `pg_xlog` gesichert wurden, wenn das Verzeichnis symbolisch verknüpft war. Dies verursachte bei der Wiederherstellung keine Probleme, verschwendete aber Speicherplatz.
- Ungültigen `log()`-Aufruf in den Sperrroutinen korrigiert.

**Funktionen:**

- Experimentelle Unterstützung für nicht exklusive Backups unter PostgreSQL 9.6 beta3. Änderungen der Control-, Katalog- oder WAL-Versionen in späteren Betaversionen können die Kompatibilität aufheben; pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.

**Verbesserungen:**

- Begrüßungstexte auf SSH-Protokollverbindungen unterdrücken.
- Fehlermeldungen entfernter Prozesse verbessert, sodass der Host erkennbar ist, auf dem der Fehler auftrat.
- Alle Typen entfernter Prozesse setzen jetzt Sperren. Die Ausnahmen stammten aus der Zeit, als Testumgebung und pgBackRest in derselben VM liefen, und gelten nicht mehr.

**Neue Inhalte der Dokumentation:**

- Erläuterung ergänzt, warum der Standardwert von `backrest-user` `backrest` ist. (*Vorgeschlagen von Michael Vitale.*)
- Informationen zur Paketverfügbarkeit auf unterstützten Plattformen aktualisiert. (*Vorgeschlagen von Michael Vitale.*)


### v1.03 – Versionshinweise {#v103-release-notes}

*Befehl check und Fehlerbehebungen*

*Veröffentlicht am 2. Juli 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den `keep-alives` bei einem `backup` mit mehreren Threads und vielen kleinen Dateien zu kurz kommen konnten. Beim Fortsetzen von `backup` mit einem oder mehreren Threads sowie bei der Prüfsummenberechnung von `restore` fehlten sie zudem vollständig. (*Gemeldet von Janice Parkinson, Chris Barber.*)
- Fehler behoben, durch den `expire` bei explizitem Aufruf über die Befehlszeile die Ausführung verweigerte, wenn `db-host` gesetzt war. Bei automatischer Ausführung von `expire` nach einem `backup` trat dies nicht auf. (*Gemeldet von Chris Barber.*)
- Fehler behoben, durch den archive_command auch bei deaktiviertem `archive-check` validiert wurde.

**Funktionen:**

- Befehl `check` hinzugefügt, um die korrekte pgBackRest-Konfiguration für Archivierung und Backups zu prüfen. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Option `protocol-timeout` hinzugefügt. Zuvor war `protocol-timeout` auf `db-timeout` + 30 Sekunden festgelegt.
- Wenn entfernte Prozesse am Ende des Backups nicht beendet werden können, wird keine Ausnahme mehr ausgelöst. Stattdessen erscheint eine Warnung, die einen höheren Wert für `protocol-timeout` empfiehlt.
- Experimentelle Unterstützung für nicht exklusive Backups unter PostgreSQL 9.6 beta2. Änderungen der Control-, Katalog- oder WAL-Versionen in späteren Betaversionen können die Kompatibilität aufheben; pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.

**Verbesserungen:**

- Umgang mit beim Backup erfassten Benutzern und Gruppen verbessert, die auf dem Wiederherstellungshost nicht existieren. Auch der Fall, dass ein Benutzer oder eine Gruppe keinem Namen zugeordnet ist, wird ausdrücklich behandelt.
- Optionen werden jetzt wesentlich strenger geprüft. Zuvor konnte ein Befehl eine Option verwenden, die ihm nicht ausdrücklich zugeordnet war. Dies betraf besonders `backup-host` und `db-host`, die den Ausführungsort bestimmen.

**Verbesserungen der Dokumentation:**

- Festes Datum für die Dokumentation zugelassen, um reproduzierbare Builds zu ermöglichen. (*Vorgeschlagen von Adrian Vondendriesch.*)
- Asynchrone Archivierung im Benutzerhandbuch dokumentiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Empfohlener Installationsort für pgBackRest-Module ist jetzt `/usr/share/perl5`, da `/usr/lib/perl5` in neueren Perl-Versionen aus dem Suchpfad entfernt wurde.
- Anleitung zum Entfernen früherer pgBackRest-Versionen hinzugefügt.


### v1.02 – Versionshinweise {#v102-release-notes}

*Fehlerbehebung für Perl 5.22*

*Veröffentlicht am 2. Juni 2016*

**Fehlerbehebungen:**

- Verwendung von sprintf() an neue Einschränkungen in Perl 5.22 angepasst. Parameter, die nicht im Formatstring referenziert werden, sind nicht mehr zulässig. (*Behoben von Adrian Vondendriesch. Geprüft von David Steele.*)

**Fehlerbehebungen in der Dokumentation:**

- Syntax korrigiert, die mit Perl 5.2X nicht kompatibel war. (*Behoben von Christoph Berg, Adrian Vondendriesch. Geprüft von David Steele.*)
- Absolute Pfade für das PDF-Logo korrigiert. (*Gemeldet von Adrian Vondendriesch.*)

**Neue Inhalte der Dokumentation:**

- Versionshinweise in Abschnitte gegliedert, um Fehlerbehebungen, Funktionen und Refactoring klar zu trennen. Ein Abschnitt „Zusätzliche Hinweise“ enthält Änderungen an Dokumentation und Testsuite, die den Kerncode nicht betreffen.
- Erzeugung einer Handbuchseite hinzugefügt. (*Beigetragen von Adrian Vondendriesch, David Steele.*)
- Das Änderungsprotokoll war der letzte Teil der Dokumentation, der nur als Markdown ausgegeben wurde. Ein Konverter ermöglicht jetzt die Ausgabe mit den Standard-Renderern. Das Änderungsprotokoll ist künftig auf der Website zu finden und wurde in „Versionen“ umbenannt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)


### v1.01 – Versionshinweise {#v101-release-notes}

*Erweitertes info, selektive Wiederherstellung und Unterstützung für 9.6*

*Veröffentlicht am 17. Mai 2016*

**Funktionen:**

- Textausgabe von `info` um Zeitstempel, Größen und die Referenzliste für alle Backups erweitert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)
- Selektive Wiederherstellung von Datenbanken aus einem Cluster-Backup ermöglicht. Wenn nur bestimmte Datenbanken wiederhergestellt werden, kann dies viel Speicherplatz und Zeit sparen. Nicht wiederhergestellte Datenbanken sind nicht zugänglich, müssen jedoch manuell gelöscht werden, damit sie aus dem gemeinsamen Katalog verschwinden. (*Geprüft von Cynthia Shang, Greg Smith, Stephen Frost. Vorgeschlagen von Stephen Frost.*)
- Experimentelle Unterstützung für nicht exklusive Backups unter PostgreSQL 9.6 beta1. Änderungen der Control-, Katalog- oder WAL-Versionen in späteren Betaversionen können die Kompatibilität aufheben; pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert. (*Geprüft von Cynthia Shang.*)


### v1.00 – Versionshinweise {#v100-release-notes}

*Neues Repository-Format und Konfigurationsschema, Unterstützung für Verknüpfungen*

*Veröffentlicht am 14. April 2016*

**WICHTIGER HINWEIS**: Diese Version mit grundlegender Umstellung ist nicht mit älteren pgBackRest-Versionen kompatibel. Manifestformat, Speicherstruktur, Konfigurationsschema sowie Namen ausführbarer Dateien und Pfade wurden geändert. Für die Backups dieser pgBackRest-Version muss ein neues Repository erstellt werden. Das alte Repository muss noch eine Zeit lang aufbewahrt werden, falls eine Wiederherstellung nötig ist. Wiederherstellungen aus dem alten Repository erfordern die vorherige pgBackRest-Version. Dank der geänderten Namen können `1.00` und eine frühere pgBackRest-Version jedoch gleichzeitig installiert sein. Weitere Einzelheiten zu den Änderungen stehen in den folgenden Hinweisen.

**Funktionen:**

- Neues Konfigurationsschema implementiert, das wesentlich einfacher zu verwenden sein sollte. Einzelheiten stehen im Benutzerhandbuch und in der Konfigurationsreferenz. Bei einer einfachen Konfiguration können jetzt alle Optionen im Abschnitt `stanza` stehen. Gemeinsame Optionen für mehrere Stanzas können im Abschnitt `[global]` stehen. Komplexere Konfigurationen können weiterhin Befehlsabschnitte nutzen; dies sollte jedoch selten nötig sein. (*Vorgeschlagen von Michael Renner.*)
- `repo-path` bezeichnet jetzt immer das Repository für Backups und Archiv, ob lokal oder entfernt. Daher wurde `repo-remote-path` entfernt. Die neue Option `spool-path` legt einen Speicherort fest, an dem WAL-Segmente bei asynchroner Archivierung zwischengespeichert werden. Ein lokales Repository ist nicht mehr erforderlich.
- Der Standardname der Konfigurationsdatei ist jetzt `pgbackrest.conf` statt `pg_backrest.conf`. Dies vereinheitlicht die Benennung mit anderen Änderungen und verhindert zugleich, dass beim Umstieg auf `1.00` versehentlich alte Konfigurationsdateien geladen werden. (*Vorgeschlagen von Michael Renner, Stephen Frost.*)
- Standardname des Repositorys von `/var/lib/backup` in `/var/lib/pgbackrest` geändert. (*Vorgeschlagen von Michael Renner, Stephen Frost.*)
- Sperrdateien liegen standardmäßig in `/tmp/pgbackrest`. Heute wäre `/run/pgbackrest` der bevorzugte Ort, würde jedoch Init-Skripte erfordern, die diese Version nicht enthält. Das Sperrverzeichnis lässt sich mit `lock-path` konfigurieren.
- Protokolldateien liegen standardmäßig in `/var/log/pgbackrest` und erhalten keinen Datumszusatz mehr, damit sie mit `logrotate` verwaltet werden können. Das Protokollverzeichnis lässt sich mit `log-path` konfigurieren. (*Vorgeschlagen von Stephen Frost.*)
- Name der ausführbaren Datei von `pg_backrest` in `pgbackrest` geändert. (*Vorgeschlagen von Michael Renner, Stephen Frost.*)
- Alle aus PGDATA verknüpften Dateien und Verzeichnisse sind jetzt im Backup enthalten. Standardmäßig werden Verknüpfungen als Dateien oder Verzeichnisse direkt in PGDATA wiederhergestellt. Mit `--link-all` lassen sich alle Verknüpfungen an ihren ursprünglichen Speicherorten wiederherstellen. Mit `--link-map` lässt sich eine Verknüpfung einem neuen Speicherort zuordnen.
- Option `--tablespace` entfernt und durch `--tablespace-map-all` ersetzt, deren Name die Funktion deutlicher beschreiben sollte.
- Protokollstufe `detail` hinzugefügt, die mehr Informationen als `info` ausgibt, ohne so ausführlich wie `debug` zu sein.


--------

## Versionen vor der ersten stabilen Veröffentlichung {#pre-stable-releases}


### v0.92 – Versionshinweise {#v092-release-notes}

*Fehler beim Repository-Pfad auf der Befehlszeile behoben*

*Veröffentlicht am 6. April 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den der Hauptprozess `--repo-remote-path` statt `--repo-path` an den entfernten Prozess übergab. Dadurch wurden Sperrdateien im Standard-Repository-Verzeichnis `/var/lib/backup` erstellt, was gewöhnlich zum Scheitern führte. Dies trat nur auf, wenn `--repo-remote-path` auf der Befehlszeile statt in `pg_backrest.conf` definiert war. (*Gemeldet von Jan Wieck.*)


### v0.91 – Versionshinweise {#v091-release-notes}

*Tablespace-Fehler behoben und kleinere Verbesserungen*

*Veröffentlicht am 22. März 2016*

**WICHTIGE FEHLERBEHEBUNG FÜR TABLESPACES**: In 0.90 wurde versehentlich eine Änderung des Repository-Formats eingeführt. Dadurch war ein auf dem Datenträger gespeichertes Backup mit Tablespaces kein gültiger PostgreSQL-Cluster mehr. Dies betraf nur Benutzer, die Backups zur Wiederherstellung von PostgreSQL-Clustern direkt kopierten, statt den Befehl restore zu verwenden. Die Korrektur ist jedoch mit älteren Backups, die Tablespaces enthalten, unabhängig von der Wiederherstellungsmethode nicht kompatibel: pgBackRest meldet Fehler und verweigert die Wiederherstellung. Für alle Cluster mit Tablespaces sollten unmittelbar nach der Installation von Version 0.91 neue vollständige Backups erstellt werden. Müssen ältere Backups wiederhergestellt werden, ist eine zum Backup passende pgBackRest-Version zu verwenden.

**Fehlerbehebungen:**

- In pgBackRest 0.90 eingeführte Repository-Inkompatibilität behoben. (*Gemeldet von Evan Benoit.*)

**Funktionen:**

- `global/pg_control` beim Backup zuletzt kopieren.
- `.info`- und `.manifest`-Dateien zunächst temporär schreiben, bevor sie an ihren endgültigen Speicherort verschoben und mit fsync synchronisiert werden.
- Option `--no-start-stop` in `--no-online` umbenannt.

**Neue Funktionen der Testsuite:**

- Statische Quellcodeanalyse mit Perl-Critic; derzeit wird die Stufe gentle bestanden.


### v0.90 – Versionshinweise {#v090-release-notes}

*Unterstützung für 9.5, verschiedene Verbesserungen und kleinere Fehlerbehebungen*

*Veröffentlicht am 7. Februar 2016*

**Fehlerbehebungen:**

- Fehler behoben, durch den `--no-archive-check` einen Konfigurationsfehler auslöste. (*Gemeldet von Jason O'Donnell.*)
- Fehler behoben, durch den eine temporäre WAL-Datei nach einem Systemabsturz im ungünstigen Moment das nächste `archive-push` scheitern lassen konnte.
- `retention-archive` kann jetzt sicher niedriger als die Backup-Aufbewahrung (`retention-full` oder `retention-diff`) eingestellt werden, ohne zusätzlich `archive-copy=n` anzugeben. WAL, das Backups außerhalb der Archivaufbewahrung in einen konsistenten Zustand versetzt, bleibt im Archiv erhalten. PITR ist für diese Backups außerhalb der Archivaufbewahrung allerdings nicht möglich.

**Funktionen:**

- Beim Sichern und Wiederherstellen von Tablespaces bearbeitet pgBackRest nur das Unterverzeichnis für die jeweils verwendete PostgreSQL-Version. Da mehrere Versionen in einem Tablespace liegen können, insbesondere während eines binären Upgrades, verhindert dies das Kopieren überflüssiger Dateien beim Backup und das mögliche Löschen anderer Versionen bei der Wiederherstellung. Dies gilt nur für PostgreSQL >= 9.0; frühere PostgreSQL-Versionen konnten kein gemeinsames Tablespace-Verzeichnis nutzen.
- Fehler ausgeben, wenn `archive-check=y` gesetzt ist, `archive_command` aber nicht `pg_backrest` ausführt. (*Beigetragen von Jason O'Donnell. Geprüft von David Steele.*)
- Fehlermeldung bei fehlendem `repo-path` oder `repo-remote-path` verbessert.
- Prüfungen für die Wiederherstellungsoptionen `--delta` und `--force` hinzugefügt, um sicherzustellen, dass das Ziel ein gültiges $PGDATA-Verzeichnis ist. pgBackRest prüft, ob `PG_VERSION` oder eine von einer abgebrochenen Wiederherstellung verbliebene `backup.manifest` vorhanden ist. Fehlen beide Dateien, werden `--delta` und `--force` deaktiviert. Die Wiederherstellung wird dennoch fortgesetzt, sofern weder im $PGDATA-Verzeichnis noch in einem Tablespace-Verzeichnis Dateien liegen; andernfalls wird sie abgebrochen.
- Bei der Wiederherstellung mit `--set=latest`, dem Standardwert, wird das tatsächlich wiederhergestellte Backup protokolliert.
- Unterstützung für partielle WAL-Segmente und die Einstellung `recovery_target_action` aus PostgreSQL 9.5. `archive_mode = 'always'` wird noch nicht unterstützt.
- Unterstützung für die in PostgreSQL 9.4 eingeführte Recovery-Einstellung `recovery_target = 'immediate'`.
- Folgende Tablespace-Prüfungen hinzugefügt: Pfade oder Dateien in pg_tblspc, relative Verknüpfungen in pg_tblspc und Tablespaces in $PGDATA. Alle drei Fälle erzeugen Fehler.


### v0.89 – Versionshinweise {#v089-release-notes}

*Zeitüberschreitungsfehler behoben und Wiederherstellung aus schreibgeschützten Repositorys*

*Veröffentlicht am 24. Dezember 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den länger laufende Backups oder Wiederherstellungen mit entferntem Zugriff und Threads eine Zeitüberschreitung auslösten. Keepalives verhindern jetzt, dass der entfernte Prozess des Hauptprozesses sein Zeitlimit überschreitet, während die entfernten Prozesse der Threads die Arbeit erledigen. Auch die Fehlermeldung bei Zeitüberschreitungen wurde verbessert, um die Fehlersuche zu erleichtern. (*Gemeldet von Stephen Frost.*)

**Funktionen:**

- Wiederherstellungen aus einem schreibgeschützten Repository mit `--no-lock` und `--log-level-file=off` ermöglicht. `--no-lock` ist nur bei Wiederherstellungen zulässig.


### v0.88 – Versionshinweise {#v088-release-notes}

*Dokumentation und kleinere Fehlerbehebungen*

*Veröffentlicht am 22. November 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den `start` und `stop` die Option `--config` erforderten. (*Gemeldet von Dmitry Didovicher.*)
- Fehler behoben, durch den Protokolldateien überschrieben statt ergänzt wurden. (*Gemeldet von Stephen Frost, Dmitry Didovicher.*)
- Fehler behoben, durch den `backup-user` nicht optional war.

**Funktionen:**

- In den Backup-Verzeichnissen des Repositorys werden keine symbolischen Verknüpfungen mehr erstellt. Diese konnten praktisch überallhin zeigen und potenziell gefährlich sein. Bei der Wiederherstellung werden symbolische Verknüpfungen weiterhin neu erstellt. (*Vorgeschlagen von Stephen Frost.*)
- Aussagekräftigere Meldungen beim Entfernen abgelaufener Backups hinzugefügt. Das Entfernen vollständiger und differenzieller Backups wird jeweils in einer Zeile zusammen mit allen entfernten abhängigen Backups protokolliert.
- Die Archivaufbewahrung wird automatisch auf die Aufbewahrung vollständiger Backups gesetzt, sofern sie nicht ausdrücklich konfiguriert ist.

**Neue Inhalte der Dokumentation:**

- Benutzerhandbuch um Delta-Wiederherstellungen, das Entfernen abgelaufener Backups, dedizierte Backup-Hosts, das Starten und Stoppen von pgBackRest sowie Replikation ergänzt.


### v0.87 – Versionshinweise {#v087-release-notes}

*Website und Benutzerhandbuch*

*Veröffentlicht am 28. Oktober 2015*

**Funktionen:**

- `backup_label.old` und `recovery.done` werden jetzt von Backups ausgeschlossen.

**Neue Inhalte der Dokumentation:**

- Neues Benutzerhandbuch hinzugefügt, das die Grundlagen von pgBackRest und einige fortgeschrittene Themen einschließlich PITR behandelt. Weitere Inhalte folgen, aber ein Anfang ist gemacht. (*Beigetragen von David Steele, Stephen Frost. Geprüft von Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher.*)


### v0.85 – Versionshinweise {#v085-release-notes}

*Befehle start/stop und kleinere Fehlerbehebungen*

*Veröffentlicht am 8. Oktober 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den nach einem vollständig erfolgreichen Backup oder einer Wiederherstellung dennoch ein Fehler zurückgegeben werden konnte.
- Fehler behoben, durch den das Fortsetzen scheiterte, wenn nach einem fehlgeschlagenen Backup temporäre Dateien im Backup-Hauptverzeichnis lagen. Dies trat besonders dann auf, wenn der Backup-Prozess während des Kopierens beendet wurde.

**Funktionen:**

- Befehle `stop` und `start` hinzugefügt, um pgBackRest-Prozesse auf einem System zu verhindern, auf dem PostgreSQL heruntergefahren ist oder das aus anderen Gründen ruhen soll.
- Experimentelle Unterstützung für PostgreSQL 9.5 beta1. Änderungen der Control-Version oder WAL-Kennung in künftigen Versionen können die Kompatibilität aufheben; die Unterstützung wird jedoch mit jeder pgBackRest-Version entsprechend aktualisiert. Alle Regressionstests bestehen mit Ausnahme der Tests für `--target-resume`, dessen Funktion sich in 9.5 geändert hat. Für `.partial`-WAL-Segmente gibt es noch keine Tests.


### v0.82 – Versionshinweise {#v082-release-notes}

*Refactoring, Befehlszeilenhilfe und kleinere Fehlerbehebungen*

*Veröffentlicht am 14. September 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den fortgesetzte komprimierte Backups vorhandene Dateien nicht beibehielten.
- Fehler behoben, durch den beim Fortsetzen sowie bei inkrementellen und differenziellen Backups nicht sichergestellt wurde, dass das vorherige Backup dieselben Einstellungen für Komprimierung und Hardlinks hatte.
- Fehler behoben, durch den ein kaltes Backup mit `--no-start-stop` auf einem laufenden PostgreSQL-Cluster ohne `--force` gestartet werden konnte.
- Fehler behoben, durch den ein Thread gestartet werden konnte, obwohl keiner angefordert war.
- Fehler behoben, durch den die pgBackRest-Versionsnummer in `backup.info` und `archive.info` nach einem Upgrade oder Downgrade nicht aktualisiert wurde.
- Fehler behoben, durch den `info` eine Ausnahme auslöste, wenn das Repository keine Stanzas enthielt. (*Gemeldet von Stephen Frost.*)
- Fehler behoben, durch den NOTICEs von PostgreSQLs `pg_stop_backup()` an `stderr` ausgegeben wurden. (*Gemeldet von Stephen Frost.*)

**Funktionen:**

- Experimentelle Unterstützung für PostgreSQL 9.5 alpha2. Änderungen der Control-Version oder WAL-Kennung in künftigen Versionen können die Kompatibilität aufheben; die Unterstützung wird jedoch mit jeder pgBackRest-Version entsprechend aktualisiert. Alle Regressionstests bestehen mit Ausnahme der Tests für `--target-resume`, dessen Funktion sich in 9.5 geändert hat. Für `.partial`-WAL-Segmente gibt es noch keine Tests.

**Verbesserungen:**

- Option und Abschnitt `recovery-setting` in `recovery-option` umbenannt, um die pgBackRest-Namenskonventionen einheitlicher anzuwenden.
- Dynamisches Laden von Modulen hinzugefügt, um Befehle und insbesondere die asynchrone Archivierung zu beschleunigen.

**Neue Inhalte der Dokumentation:**

- Die Befehlszeilenhilfe wird jetzt aus derselben XML-Quelle wie die übrige Dokumentation erzeugt und enthält deutlich mehr Einzelheiten.


### v0.80 – Versionshinweise {#v080-release-notes}

*DBI-Unterstützung, Stabilität und Komfortfunktionen*

*Veröffentlicht am 9. August 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den `info` für das älteste und neueste Backup jeweils die aktuelle Uhrzeit als formatierten Zeitstempel ausgab. Nur die Ausgabe als `text` war betroffen; `json` gab die korrekten Epoch-Werte aus. (*Gemeldet von Michael Renner.*)
- Protokollfehler behoben, der das Protokollieren von ssh-Fehlern, insbesondere beim Verbindungsaufbau, verhinderte.

**Funktionen:**

- Das Repository wird jetzt mit einheitlichen Verzeichnis- und Dateiberechtigungen erstellt und aktualisiert. Standardmäßig wird `umask` auf `0000` gesetzt; dies lässt sich mit `neutral-umask` deaktivieren. (*Vorgeschlagen von Cynthia Shang.*)
- Option `stop-auto` hinzugefügt, um fehlgeschlagene Backups beim Start eines neuen Backups automatisch zu stoppen.
- Option `db-timeout` hinzugefügt, um die Wartezeit von pgBackRest auf die Rückkehr von `pg_start_backup()` und `pg_stop_backup()` zu begrenzen.
- `pg_control` zu Beginn der Wiederherstellung entfernen und erst ganz am Ende zurückkopieren. Dies verhindert, dass PostgreSQL einen teilweise wiederhergestellten Cluster startet.
- Prüfungen ergänzt, um die Übereinstimmung von `db-path` und `db-port` sicherzustellen. Dazu werden das vom Cluster gemeldete `data_directory` mit `db-path` und die gemeldete Version mit dem aus `pg_control` gelesenen Wert verglichen. Für `db-socket-path` wird geprüft, ob der Pfad absolut ist.
- Experimentelle Unterstützung für PostgreSQL 9.5 alpha1. Änderungen der Control-Version oder WAL-Kennung in künftigen Versionen können die Kompatibilität aufheben; die Unterstützung wird jedoch mit jeder pgBackRest-Version entsprechend aktualisiert. Alle Regressionstests bestehen mit Ausnahme der Tests für `--target-resume`, dessen Funktion sich in 9.5 geändert hat. Für `.partial`-WAL-Segmente gibt es noch keine Tests.

**Verbesserungen:**

- Für PostgreSQL-Verbindungen werden jetzt Perls `DBI` und `DBD::Pg` statt `psql` verwendet. Die Einstellungen `cmd-psql` und `cmd-psql-option` wurden entfernt und durch `db-port` und `db-socket-path` ersetzt. `DBD::Pg` gemäß der Installationsanleitung für das jeweilige Betriebssystem installieren.

**Neue Funktionen der Testsuite:**

- vagrant-Testkonfigurationen für Ubuntu 14.04 und CentOS 7 hinzugefügt.


### v0.78 – Versionshinweise {#v078-release-notes}

*CPAN-Abhängigkeiten entfernt, Stabilität verbessert*

*Veröffentlicht am 13. Juli 2015*

**Verbesserungen:**

- Abhängigkeit von CPAN-Paketen für den Betrieb mit mehreren Threads entfernt. Die Pakete `threads` und `Thread::Queue` zu aktualisieren, kann weiterhin sinnvoll sein, ist aber nicht mehr erforderlich.
- Ansteigende Wartezeiten verwenden jetzt eine Fibonacci-Folge statt einer geometrischen Folge. Dadurch wachsen sie weniger stark und bleiben dennoch angemessen.

**Neue Funktionen der Testsuite:**

- vagrant-Testkonfigurationen für Ubuntu 12.04 und CentOS 6 hinzugefügt.


### v0.77 – Versionshinweise {#v077-release-notes}

*Unterstützung für CentOS/RHEL 6 und Protokollverbesserungen*

*Veröffentlicht am 30. Juni 2015*

**Funktionen:**

- Datei- und Verzeichnissynchronisierung zum Objekt `File` hinzugefügt, um Backups, Wiederherstellungen und Archivierung zusätzlich abzusichern. (*Vorgeschlagen von Andres Freund.*)
- Unterstützung für Perl 5.10.1 und OpenSSH 5.3 hinzugefügt, die unter CentOS/RHEL 6 Standard sind. (*Vorgeschlagen von Eric Radman.*)
- Fehlermeldung verbessert, wenn ein Backup ohne gesetzten `archive_command` und ohne `--no-archive-check` ausgeführt wird. (*Vorgeschlagen von Eric Radman.*)


### v0.75 – Versionshinweise {#v075-release-notes}

*Neues Repository-Format, Befehl info und experimentelle Unterstützung für 9.5*

*Veröffentlicht am 14. Juni 2015*

**WICHTIGER HINWEIS**: Diese Version mit grundlegender Umstellung ist nicht mit älteren pgBackRest-Versionen kompatibel. Manifestformat, Speicherstruktur und Namen der Binärdateien wurden geändert. Für die Backups dieser pgBackRest-Version muss ein neues Repository erstellt werden. Das alte Repository muss noch eine Zeit lang aufbewahrt werden, falls eine Wiederherstellung nötig ist. Die Datei `pg_backrest.conf` hat sich nicht geändert. Verweise auf `pg_backrest.pl` in cron oder anderswo müssen jedoch in `pg_backrest` ohne die Endung `.pl` geändert werden.

**Funktionen:**

- Befehl `info` hinzugefügt.
- Die Protokollierung verwendet jetzt ungepufferte Ausgabe. Dadurch sollten Protokolldateien, in die mehrere Threads schreiben, weniger ungeordnet sein. (*Vorgeschlagen von Michael Renner.*)
- Experimentelle Unterstützung für PostgreSQL 9.5. Änderungen der Control-Version oder WAL-Kennung können die Kompatibilität aufheben; die Unterstützung wird jedoch mit jeder Version aktualisiert.

**Verbesserungen:**

- Effizientere Dateireihenfolge für `backup`. Dateien werden in absteigender Größenreihenfolge kopiert, damit am Ende nicht ein einzelner Thread eine große Datei kopieren muss. Für `restore` war dies bereits implementiert.


### v0.70 – Versionshinweise {#v070-release-notes}

*Stabilere Archivierung, bessere Protokollierung und Hilfe*

*Veröffentlicht am 1. Juni 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den `archive-copy` bei einem inkrementellen oder differenziellen Backup mit `hardlink=n` scheiterte. In diesem Fall existiert `pg_xlog` noch nicht und muss erstellt werden. (*Gemeldet von Michael Renner.*)
- Fehler in der asynchronen Archivierung behoben, durch den `archive-push` beim Erreichen von `archive-max-mb` nicht korrekt 0 zurückgab. Die asynchrone Prüfung erfolgt jetzt nach der Übertragung, damit die Stoppdatei nicht zweimal entfernt werden muss. Außerdem wurden Unit-Tests für diesen Fall ergänzt und Fehlermeldungen verständlicher gestaltet. (*Gemeldet von Michael Renner.*)
- Sperrfehler behoben, der mehrere gleichartige Operationen für dieselbe Stanza zulassen konnte. Die Datenintegrität schien dadurch nicht beeinträchtigt, jedoch entstanden unnötige Fehler bei der Archivierung und möglicherweise Fehler bei Backups oder Wiederherstellungen. (*Gemeldet von Michael Renner.*)

**Funktionen:**

- Doppelte WAL-Segmente dürfen jetzt archiviert werden, wenn ihre Prüfsummen übereinstimmen. Dies ist für bestimmte Recovery-Szenarien erforderlich.
- Kommentare und das Deaktivieren von Zeilen in `pg_backrest.conf` mit dem Zeichen `#` ermöglicht. Nur ein `#` als erstes Zeichen einer Zeile wird berücksichtigt. (*Vorgeschlagen von Michael Renner.*)
- Protokollierung vor `pg_start_backup()` verbessert, damit erkennbar ist, wann das Backup auf einen Checkpoint wartet. (*Vorgeschlagen von Michael Renner.*)
- Verschiedene Korrekturen an Befehlsverhalten und Protokollierung. (*Geprüft von Michael Renner. Vorgeschlagen von Michael Renner.*)

**Verbesserungen:**

- Modul `JSON` durch `JSON::PP` ersetzt, das zum Perl-Kern gehört.

**Fehlerbehebungen in der Dokumentation:**

- Verschiedene Korrekturen in der Hilfe. (*Geprüft von Michael Renner. Gemeldet von Michael Renner.*)


### v0.65 – Versionshinweise {#v065-release-notes}

*Verbessertes Fortsetzen und bessere Protokollierung bei der Wiederherstellung, kompakte Wiederherstellungen*

*Veröffentlicht am 11. Mai 2015*

**Fehlerbehebungen:**

- Fehler behoben, durch den kein absoluter Pfad in `recovery.conf` geschrieben wurde, wenn die Wiederherstellung mit einem relativen Pfad lief.

**Funktionen:**

- Unterstützung für das Fortsetzen verbessert. Bereits vorhandene Dateien werden auf Änderungen geprüft; das Manifest wird häufiger gespeichert, damit Prüfsummen während des Backups erhalten bleiben. Zusätzliche Unit-Tests prüfen die einzelnen Fälle beim Fortsetzen.
- Das Fortsetzen ist jetzt optional. Es lässt sich mit der Einstellung `resume` oder auf der Befehlszeile mit `--no-resume` deaktivieren.
- Mehr info-Meldungen bei der Wiederherstellung. Zuvor hatten die meisten Wiederherstellungsmeldungen die Stufe debug, sodass wenig im Protokoll erschien.
- Einstellung `tablespace` hinzugefügt, um Tablespaces in `pg_tblspc` wiederherzustellen. Dadurch entstehen kompakte Wiederherstellungen, die für Entwicklung, Staging usw. praktisch sind. Derzeit lassen sich diese Wiederherstellungen nicht sichern, da pgBackRest unter `pg_tblspc` ausschließlich Verknüpfungen erwartet.


### v0.61 – Versionshinweise {#v061-release-notes}

*Fehler bei unkomprimiertem entferntem Ziel behoben*

*Veröffentlicht am 21. April 2015*

**Fehlerbehebungen:**

- Pufferfehler behoben, der beim Kopieren großer, gut komprimierbarer Dateien an ein unkomprimiertes entferntes Ziel auftreten konnte. Der Fehler wurde im Dekomprimierungscode erkannt und führte zu einem fehlgeschlagenen statt einem beschädigten Backup. Erfolgreiche Backups aus früheren Versionen sollten daher nicht betroffen sein.


### v0.60 – Versionshinweise {#v060-release-notes}

*Bessere Versionsunterstützung und WAL-Verbesserungen*

*Veröffentlicht am 19. April 2015*

**Fehlerbehebungen:**

- Das Übertragen doppelter WAL-Segmente erzeugt jetzt einen Fehler. Zuvor funktionierte dies nur bei deaktivierten Prüfsummen.

**Funktionen:**

- Datenbanksystemkennungen (IDs) stellen sicher, dass alle WAL-Segmente eines Archivs zusammengehören. Dies sollte Fehlkonfigurationen verhindern, bei denen WAL mehrerer Cluster in dasselbe Archiv gelangt.

**Neue Funktionen der Testsuite:**

- Regressionstests funktionieren zurück bis PostgreSQL 8.3.


### v0.50 – Versionshinweise {#v050-release-notes}

*Wiederherstellung und vieles mehr*

*Veröffentlicht am 25. März 2015*

**Fehlerbehebungen:**

- Fehlerhafte Prüfsummen korrigiert; sie funktionieren jetzt bei normalen und fortgesetzten Backups. Die Erkenntnis, dass Prüfsummen und Prüfsummendeltas funktional getrennt werden sollten, hat mehrere Dinge vereinfacht. Für Prüfsummendeltas wurde Issue #28 angelegt.
- Fehler behoben, durch den ein Backup auf Grundlage eines abgebrochenen Backups mit anderem Typ oder anderem vorherigen Backup fortgesetzt werden konnte.

**Funktionen:**

- Wiederherstellungsfunktion hinzugefügt.
- Alle Optionen können jetzt auf der Befehlszeile gesetzt werden, wodurch `pg_backrest.conf` optional wird.
- Komprimierung und Dekomprimierung erfolgen jetzt ohne Threads; Prüfsumme und Größe werden im Datenstrom berechnet. Dateiprüfsummen sind damit nicht mehr optional.
- Option `--no-start-stop` hinzugefügt, um Backups bei heruntergefahrenem Postgres zu ermöglichen. Ist `postmaster.pid` vorhanden, muss `--force` angegeben werden, damit das Backup startet. Läuft Postgres noch, wird dabei wahrscheinlich ein inkonsistentes Backup erstellt. Diese Option dient vor allem Unit-Tests, kann aber auch praktische Anwendungen haben.
- Prüfsumme für `backup.manifest` hinzugefügt, um beschädigte oder veränderte Manifeste zu erkennen.
- Die Verknüpfung `latest` zeigt immer auf das letzte Backup. Dies erhöht den Bedienkomfort und vereinfacht Wiederherstellungen.

**Neue Funktionen der Testsuite:**

- Umfassendere Unit-Tests in allen Bereichen.


### v0.30 – Versionshinweise {#v030-release-notes}

*Umstrukturierung des Kerns und Unit-Tests*

*Veröffentlicht am 5. Oktober 2014*

**Neue Inhalte der Dokumentation:**

- Dringend benötigte Dokumentation hinzugefügt.

**Neue Funktionen der Testsuite:**

- Recht umfassende Unit-Tests für alle grundlegenden Operationen. Hier bleibt sicher noch Arbeit, aber an Unit-Tests gibt es immer etwas zu tun.


### v0.19 – Versionshinweise {#v019-release-notes}

*Verbesserte Fehlermeldungen und Fehlerbehandlung*

*Veröffentlicht am 13. Mai 2014*

**Fehlerbehebungen:**

- Schwerwiegenden Fehler gefunden und behoben: `file_copy()` ignorierte standardmäßig Fehler. Zudem ließ ein Problem in `file_exists()` die Prüfung scheitern, obwohl die Datei existierte. Zusammen hätten diese Fehler ohne Fehlermeldung zu einem beschädigten Backup führen können, auch wenn dies sehr unwahrscheinlich ist.


### v0.18 – Versionshinweise {#v018-release-notes}

*Nicht schwerwiegenden Fehler bei fehlender Archivdatei zurückgeben*

*Veröffentlicht am 13. April 2014*

**Fehlerbehebungen:**

- `archive-get` gibt jetzt 1 zurück, wenn die Archivdatei fehlt, um dies von schwerwiegenden Fehlern wie gescheiterten ssh-Verbindungen oder Dateikopien zu unterscheiden. Damit erkennt PostgreSQL, dass der Archivdatenstrom regulär beendet wurde. Mögliche Lücken im Archivdatenstrom werden dabei jedoch nicht berücksichtigt. (*Gemeldet von Stephen Frost.*)


### v0.17 – Versionshinweise {#v017-release-notes}

*Warnung bei nicht löschbaren Archivverzeichnissen*

*Veröffentlicht am 3. April 2014*

**Fehlerbehebungen:**

- Konnte ein Archivverzeichnis, das leer sein sollte, nicht gelöscht werden, gab backrest einen Fehler aus. Eine geeignete Korrektur ist vorgesehen; vorerst wurde daraus eine Warnung, damit die Verarbeitung fortgesetzt werden kann. Dies beeinträchtigte Backups: Mitunter wurde die letzte Archivdatei nicht übertragen, wenn die erste Archivdatei in einem anderen Verzeichnis gelegen hatte und ungünstige Umstände hinzukamen.


### v0.16 – Versionshinweise {#v016-release-notes}

*RequestTTY=yes für SSH-Sitzungen*

*Veröffentlicht am 1. April 2014*

**Fehlerbehebungen:**

- `RequestTTY=yes` zu ssh-Sitzungen hinzugefügt, in der Hoffnung, gelegentliches Hängenbleiben zu verhindern.


### v0.15 – Versionshinweise {#v015-release-notes}

*archive-get hinzugefügt*

*Veröffentlicht am 29. März 2014*

**Funktionen:**

- Funktion `archive-get` zur Unterstützung von Wiederherstellungen hinzugefügt.
- Option `start-fast=y` hinzugefügt, um beim Backup-Start einen Checkpoint zu erzwingen.


### v0.11 – Versionshinweise {#v011-release-notes}

*Kleinere Korrekturen*

*Veröffentlicht am 26. März 2014*

**Fehlerbehebungen:**

- Option `master_stderr_discard` bei SSH-Datenbankverbindungen entfernt. Es gab gelegentliches Hängenbleiben, möglicherweise im Zusammenhang mit Problemen, die ursprünglich im Dateicode auftraten. (*Gemeldet von Stephen Frost.*)
- Sperrdateikonflikte bei `backup` und `expire` auf `ERROR` geändert. Durch Übernahme aus den Archivsperren standen sie auf `DEBUG`.


### v0.10 – Versionshinweise {#v010-release-notes}

*Backups und Archivierung funktionieren*

*Veröffentlicht am 5. März 2014*

**Funktionen:**

- Noch keine Wiederherstellungsfunktion, aber die Backup-Verzeichnisse sind konsistente PostgreSQL-Datenverzeichnisse. Die Dateien müssen entweder dekomprimiert werden, oder die Komprimierung muss beim Backup deaktiviert sein. Unkomprimierte Backups auf ZFS oder einem ähnlichen Dateisystem eignen sich gut, da sie lokal über einen Snapshot wiederhergestellt werden können, um logische Backups zu erstellen oder gezielt Daten wiederherzustellen.
- Die Archivierung verwendet einen einzelnen Thread. Auf unseren Datenbanken mit mehreren Terabyte und hohem Schreibvolumen war dies bisher kein Problem. Empfohlen wird ein großes WAL-Volume oder die asynchrone Option mit einem großen, nahe gelegenen Volume.
- Backups verwenden mehrere Threads. Die Bibliothek `Net::OpenSSH` scheint jedoch nicht zu 100% threadsicher zu sein und bleibt daher sehr selten in einem Thread hängen. Ein allgemeines Prozesszeitlimit behebt dies, indem der Prozess beendet wird. Ja, eine sehr unschöne Lösung.
- Bei jedem fortgesetzten Backup gehen Prüfsummen verloren. Wird mehrfach fortgesetzt, zeichnet nur das letzte Backup Prüfsummen auf. Prüfsummen früherer Backups werden korrekt erfasst, und ein vollständiges Backup setzt alles zurück.
- `backup.manifest` wird als `Storable` geschrieben, da `Config::IniFile` offenbar nicht gut mit großen Dateien umgeht. Eine Speicherung als menschenlesbarer Text ist ausdrücklich gewünscht.

**Neue Inhalte der Dokumentation:**

- Überhaupt keine Dokumentation außerhalb des Codes. Abgesehen von diesen Versionshinweisen.
