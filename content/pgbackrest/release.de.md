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

pgBackRest-Versionsnummern bestehen aus drei Teilen: Haupt-, Neben- und Patchversion. Eine Hauptversion *kann* die Kompatibilität mit der vorherigen Hauptversion aufheben. Die Versionen der Reihe v2 sind jedoch vollständig mit v1-Repositorys kompatibel und akzeptieren alle v1-Optionen. Nebenversionen können Fehlerbehebungen und neue Funktionen enthalten, ändern aber das Repository-Format nicht und vermeiden nach Möglichkeit Änderungen an Optionen und Benennungen. Patchversionen enthalten Fehlerbehebungen für die jeweils aktuelle Nebenversion.

Funktionsversionen sind für den dritten Montag im Januar, April, Juli und Oktober vorgesehen. Patchversionen erscheinen bei Bedarf am dritten Montag der übrigen Monate.

Die Dokumentation für v1 ist [hier](https://pgbackrest.org/1) verfügbar.

Die Versionshinweise können auch „Zusätzliche Hinweise“ enthalten. Änderungen in diesem Abschnitt betreffen jedoch ausschließlich die Dokumentation oder die Testsuite und haben keine direkten Auswirkungen auf die Codebasis von pgBackRest.

--------

## Dokumentierte stabile Version {#current-stable-release}

Diese Spiegelung dokumentiert v2.60.0. Neuere Versionen sind in der [Versionsgeschichte des Originalprojekts](https://pgbackrest.org/release.html) aufgeführt.

### v2.60.0 – Versionshinweise {#v2600-release-notes}

*Seitenprüfsummenfehler und Vorabladen aus Objektspeichern*

*Veröffentlicht am 18. Oktober 2026*

**WICHTIGER HINWEIS**: Der Befehl `restore` meldet nun einen Fehler und bricht ab, wenn eine wiederhergestellte Datei eine ungültige Seitenprüfsumme enthält. Der Cluster bleibt dadurch unvollständig und kann nicht starten; die Wiederherstellung muss daher erneut ausgeführt werden. Der Befehl `expire` verweigert nun das Entfernen abgelaufener Backups, wenn das älteste verbleibende Backup Prüfsummenfehler enthalten würde. Dies verhindert auch das Entfernen abgelaufener Archive in diesem Repository. Mit `checksum-page-error=n` werden Warnungen statt Fehlern ausgegeben.

**Funktionen:**

- Option `checksum-page-error` hinzugefügt, um bei ungültigen Seitenprüfsummen einen Fehler zu melden. (*Beigetragen von Andrew Pogrebnoi. Geprüft von Douglas J Hunley, David Steele, Greg Sabino Mullane, Stefan Fercot. Vorgeschlagen von Greg Sabino Mullane.*)

  Diese Option gilt für die Befehle `backup`, `restore` und `expire`. Der Befehl `backup` gibt standardmäßig wie bisher für jede Datei eine Warnung aus und meldet nun zusätzlich am Ende des Backups die Gesamtzahl der Prüfsummenwarnungen. Bei `restore` und `expire` ist ein Fehler die Standardeinstellung. Zuvor meldete `restore` ungültige Seitenprüfsummen überhaupt nicht.

  Issue [#2687](https://github.com/pgbackrest/pgbackrest/issues/2687); Pull Request [#2833](https://github.com/pgbackrest/pgbackrest/pull/2833); Commit [`d7f54b2`](https://github.com/pgbackrest/pgbackrest/commit/d7f54b2245c8a9467e9a811c65626fe77739376b)
- Unterstützung für GCS Workload Identity Federation. (*Beigetragen von Adol Rodriguez. Geprüft von Douglas J Hunley, David Steele.*)

  Setzen Sie `repo-gcs-key-type=web-id` und geben Sie mit `repo-gcs-key` eine Datei mit Anmeldedaten eines externen Kontos an, wie sie etwa von `gcloud iam workload-identity-pools create-cred-config` erzeugt wird. Das Web-Identity-Token wird ohne Dienstkontoschlüssel gegen ein Zugriffstoken ausgetauscht. Die Tokendatei wird bei jedem Austausch neu geladen, um rotierte Tokens zu übernehmen, beispielsweise projizierte Dienstkonto-Tokens von Kubernetes. Die Übernahme der Identität eines Dienstkontos wird nicht unterstützt.

  Issue [#2838](https://github.com/pgbackrest/pgbackrest/issues/2838); Pull Request [#2839](https://github.com/pgbackrest/pgbackrest/pull/2839); Commit [`1d217e6`](https://github.com/pgbackrest/pgbackrest/commit/1d217e626301118ae2c1e7be39a6a4affa86e501)
- Vorabladen mehrerer Dateien oder Bereiche aus Objektspeichern. (*Geprüft von Andrew Pogrebnoi, Douglas J Hunley.*)

  Anfragen werden vor dem aktuellen Lesevorgang eingereiht, sodass sie während des Lesens weiterlaufen. Kleine Lücken zwischen Dateien werden mitgelesen, statt eine neue Anfrage auszulösen. `Restore` nutzt dies zum Lesen gebündelter Dateien und blockinkrementeller Zuordnungen; `backup` liest damit blockinkrementelle Zuordnungen des vorherigen Backups. `repo-storage-prefetch` (Standard 3) legt die Anzahl eingereihter Anfragen fest, `repo-storage-read-over` (Standard 64KiB) die größte mitgelesene Lücke.

  [`e63dec3`](https://github.com/pgbackrest/pgbackrest/commit/e63dec323b9e79513638b9858e4ad13b6072d060) Mehrere Dateien oder Bereiche aus Objektspeichern vorabladen.; Pull Request [#2783](https://github.com/pgbackrest/pgbackrest/pull/2783)

  [`5ae4015`](https://github.com/pgbackrest/pgbackrest/commit/5ae4015d37081eba4259f4de379a9d160236de0e) Lesevorgänge früherer blockinkrementeller Zuordnungen während des Backups zusammenfassen.; Pull Request [#2816](https://github.com/pgbackrest/pgbackrest/pull/2816)

**Verbesserungen:**

- Keep-alive-Anfragen an entfernte Prozesse reduziert. (*Geprüft von Douglas J Hunley.*)

  Bei `archive-push` und `backup` wurde nach jedem abgeschlossenen Auftrag eine Keep-alive-Anfrage an jeden entfernten Prozess gesendet, selbst wenn dieser gerade eine Anfrage erhalten hatte. Eine Keep-alive-Anfrage wird nun nur gesendet, wenn seit 30 Sekunden keine Anfrage an den entfernten Prozess gesendet wurde.

  Commit [`f652261`](https://github.com/pgbackrest/pgbackrest/commit/f652261d32a4ffba98e7da26a41ef4ef1cd08da3)
- Azure-Teilanfragen ohne Antwort im Batch erneut ausführen. (*Geprüft von Douglas J Hunley.*)

  Schlägt eine Batch-Löschung bei Azure fehl, kann eine einzelne Antwort für den gesamten Batch zurückgegeben werden. Teilanfragen ohne Antwort galten als abgeschlossen, sodass nur eine Datei pro Batch entfernt wurde, während der Befehl Erfolg meldete. Teilanfragen ohne Antwort werden nun wiederholt.

  Issue [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Pull Request [#2849](https://github.com/pgbackrest/pgbackrest/pull/2849); Commit [`567a245`](https://github.com/pgbackrest/pgbackrest/commit/567a2451244e0e7a4c54e41880fac1a007b49930)
- Manifestprüfungen beim Rekonstruieren von `backup.info` reduziert. (*Geprüft von Douglas J Hunley. Vorgeschlagen von todeb.*)

  Die Befehle `backup`, `expire` und `annotate` prüfen nicht mehr auf ein `backup.manifest`, wenn die Repository-Auflistung zeigt, dass der Backup-Pfad nicht existiert, oder wenn ein differenzielles bzw. inkrementelles Backup zu einem vollständigen Backup-Satz gehört, der nicht in `backup.info` enthalten ist. Jede Prüfung ist eine Anfrage; bei Objektspeichern wird die Prüfung auf ein fehlendes Manifest daher als 404 protokolliert.

  Issue [#2769](https://github.com/pgbackrest/pgbackrest/issues/2769); Pull Request [#2825](https://github.com/pgbackrest/pgbackrest/pull/2825); Commit [`0d3c340`](https://github.com/pgbackrest/pgbackrest/commit/0d3c340087bfb97263c29a8fd681cf079071236b)
- Ursprüngliche Größe zur Entscheidung über das Bündeln einer Datei verwenden. (*Geprüft von Douglas J Hunley.*)

  Bisher wurde anhand der Größe einer blockinkrementellen Datei im vorherigen Backup entschieden, ob sie gebündelt wird. Dadurch konnte eine Datei, die inzwischen über `repo-bundle-limit` hinausgewachsen war, weiterhin in einem Bündel gespeichert werden. Nun wird die aktuelle Dateigröße verwendet.

  Pull Request [#2843](https://github.com/pgbackrest/pgbackrest/pull/2843); Commit [`340d58b`](https://github.com/pgbackrest/pgbackrest/commit/340d58bb49d6c88a002a0d23830fd37be155cc21)
- Kontext zu Fehlern beim Lesen von Blockzuordnungen während des Backups hinzugefügt. (*Geprüft von Stefan Fercot, Douglas J Hunley.*)

  Ein Fehler beim Lesen der Blockzuordnung eines früheren Backups nennt nun Datei, Repository-Pfad, Offset und Zuordnungsgröße. Liefert ein Lesevorgang weniger Bytes als erwartet, wird dies ausdrücklich gemeldet und nicht als Analysefehler ausgegeben.

  [`bc91688`](https://github.com/pgbackrest/pgbackrest/commit/bc91688c4cf18fa6a36ec65441784533d5e6bdd5) Kontext zu Fehlern beim Lesen von Blockzuordnungen während des Backups hinzufügen.; Issue [#2489](https://github.com/pgbackrest/pgbackrest/issues/2489); Issue [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Pull Request [#2830](https://github.com/pgbackrest/pgbackrest/pull/2830)

  [`f46bfaf`](https://github.com/pgbackrest/pgbackrest/commit/f46bfafdd53dd0031a320fa95b08568263901ff3) Optionsnamen in Fehlern zu blockinkrementellen Zuordnungen korrigieren.
- `current_timestamp` in der Backup-Startkennzeichnung in `text` umwandeln. (*Beigetragen von Tiago Corcelli de Oliveira. Geprüft von David Steele.*)

  Eine benutzerdefinierte implizite Umwandlung von `timestamptz` in `text` ließ das Backup mit „operator is not unique: unknown || timestamp with time zone“ fehlschlagen. Der Text der Kennzeichnung bleibt unverändert.

  Issue [#2873](https://github.com/pgbackrest/pgbackrest/issues/2873); Commit [`86936e1`](https://github.com/pgbackrest/pgbackrest/commit/86936e1fa60b10b7592eaac09283c4bb5991265d)
- Kompilieren unter illumos unterstützt. (*Beigetragen von Kalevi Kolttonen. Geprüft von Douglas J Hunley, David Steele.*)

  Ein OmniOS-Auftrag wurde zur CI hinzugefügt. Solaris könnte ebenfalls funktionieren, wurde aber nicht getestet.

  Pull Request [#2870](https://github.com/pgbackrest/pgbackrest/pull/2870); Commit [`ad72e58`](https://github.com/pgbackrest/pgbackrest/commit/ad72e5815f3cf9c0c6170dcbe04ef9c41762d3d9)
- OpenSSL 4 unterstützt. (*Geprüft von Douglas J Hunley.*)

  Das Kompilieren mit OpenSSL 4 schlug fehl, da `X509_get_subject_name()` nun einen Namen mit `const` zurückgibt.

  Commit [`a729ac8`](https://github.com/pgbackrest/pgbackrest/commit/a729ac881f48225622151841e80146f7a3a4bce6)
- Builds mit clang korrigiert. (*Geprüft von Douglas J Hunley.*)

  Unter Linux installiert gcc `libbacktrace.a` dort, wo auch clang danach sucht, `backtrace.h` jedoch an einem Ort, den nur gcc findet. Ein clang-Build fand dadurch die Bibliothek, scheiterte dann aber beim Kompilieren. Die Bibliothek wird nun nur verwendet, wenn auch ihr Header gefunden wird. Außerdem wurden Rückgabetypen korrigiert, die clang in Debug-Builds als einschränkende Typumwandlungen meldet.

  [`84b031a`](https://github.com/pgbackrest/pgbackrest/commit/84b031af68fe6a30b4150ec6c903cc8c1781fc05) Beim Prüfen auf libbacktrace auch den Header voraussetzen.

  [`195e66b`](https://github.com/pgbackrest/pgbackrest/commit/195e66bafd89da511fb0d48e6e053176104c47c7) Bei Funktionen mit einem auf StringId basierenden Enum als Rückgabetyp den deklarierten Typ zurückgeben.

  [`d9e5e14`](https://github.com/pgbackrest/pgbackrest/commit/d9e5e14e93f460d62930f58dd4dd5bbc2a9f3a85) Aus einer mit Rückgabetyp bool deklarierten Funktion bool zurückgeben.
- Codegenerierung von C nach Python migriert.

  Während des Builds erzeugt nun ein Python-Werkzeug Code aus den Deklarationen für Optionen, Fehler, Hilfe und PostgreSQL. Es ersetzt ein C-Werkzeug, das zuvor erst kompiliert werden musste. Ein Build aus einem git-Checkout benötigt PyYAML statt libyaml. Der Release-Tarball enthält den generierten Code und benötigt keines von beiden.

  Commit [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e)

**Verbesserungen der Dokumentation:**

- Website modernisiert. Besonderer Dank geht an Jan für das treffende und urkomische Logo. (*Beigetragen von David Steele, Jan Wieremjewicz. Geprüft von Steve Atkins, Kai Wagner, Douglas J Hunley, Nikolaos Stamatopoulos, Matt Hudson, Stefan Fercot.*)

  Die Website hat ein neues Design mit hellen und dunklen Themes sowie einem Layout für Mobiltelefone. Seiten mit einem Inhaltsverzeichnis zeigen es neben dem Text und markieren den gerade gelesenen Abschnitt. Befehle und Konfigurationsdateien lassen sich per Schaltfläche kopieren. Konfigurationsdateien markieren die Zeilen, die der jeweilige Abschnitt ändert, und Versionshinweise können für weitere Details aufgeklappt werden.

  [`5bc14b5`](https://github.com/pgbackrest/pgbackrest/commit/5bc14b581a054ab3dc9cd633954a689acc99a58f) Dokumentationstitel kürzen und Mehrdeutigkeiten beseitigen.

  [`b668d71`](https://github.com/pgbackrest/pgbackrest/commit/b668d71f22489cbd4d5e120e7e6e73be0ca9e167) Sponsoren auf der Startseite weiter unten platzieren und den Unterstützungsaufruf kürzen.

  [`60b85c5`](https://github.com/pgbackrest/pgbackrest/commit/60b85c58d98dd65d47747e6355f47c934cd6b430) Website modernisieren.

  [`ab8df23`](https://github.com/pgbackrest/pgbackrest/commit/ab8df23807cc4c11768ef40196bcade70ebec23a) Beim Teilen eines Links eine Karte statt des Logos anzeigen.

  [`76ae494`](https://github.com/pgbackrest/pgbackrest/commit/76ae49456c7dace20bbd6f17e8acdfd36bf03a46) Inhaltsverzeichnis der Versionsseite entfernen und den Abstand um das Datum verringern.

  [`3e86c71`](https://github.com/pgbackrest/pgbackrest/commit/3e86c71f5546c86941f35d5be3a7fdcd98af3cca) Optionen in der Befehlsreferenz verlinken statt wiederholen.

  [`dc3af7b`](https://github.com/pgbackrest/pgbackrest/commit/dc3af7b2aee5778dbe9200e31d5a2f95ecae5777) Befehlstitel in der Befehlsreferenz verdeutlichen.

  [`078d52c`](https://github.com/pgbackrest/pgbackrest/commit/078d52c5768bb67989624b5418fdd687fab9e485) Die von einem Abschnitt geänderten Zeilen einer Konfigurationsdatei markieren.

  [`bd33623`](https://github.com/pgbackrest/pgbackrest/commit/bd33623ba945ed251e2a6704cea14a81d51c2c9e) Befehlsausgaben wie Konfigurationsdateien markieren.

  [`578fc2d`](https://github.com/pgbackrest/pgbackrest/commit/578fc2de14a6a739401fd58b9a232cf587c52fb4) Neben Konfigurationsdateien auch Befehle kopieren.

  [`1fb93f9`](https://github.com/pgbackrest/pgbackrest/commit/1fb93f92725124d6afa8953b7c7243aee92fcaf5) Einen Fehler melden, wenn ein Konfigurationsabschnitt nichts für den Leser Sichtbares ändert.

  [`2f3b2f2`](https://github.com/pgbackrest/pgbackrest/commit/2f3b2f22a30a35340549d42b09d5aaa58d9dfe61) Das Website-Logo mit der Startseite verlinken.

  [`8f902c6`](https://github.com/pgbackrest/pgbackrest/commit/8f902c66609c0bf1de6720e60552adde515209cd) Dokumentationsbuild beschleunigen.

  [`b56b6ab`](https://github.com/pgbackrest/pgbackrest/commit/b56b6ab4d24ff6298b95b415b3115591e311de20) Neueste Meldungen automatisch auf der Startseite auflisten.

  [`5b8987d`](https://github.com/pgbackrest/pgbackrest/commit/5b8987da0bb24fc3979fb764ccbde82b7b0e9500) Beispiele für Optionstypen in der Referenz als Codeblöcke darstellen.

  [`b5d5274`](https://github.com/pgbackrest/pgbackrest/commit/b5d527471444f90df5529f15726b3d33065f9829) Das Menü horizontal scrollen lassen, statt es durch Zeilenumbrüche aus dem sichtbaren Bereich zu schieben.

  [`9ae2c32`](https://github.com/pgbackrest/pgbackrest/commit/9ae2c32a35f56f53f299e8c04f004ed3386b95e4) Die aktuelle Seite im Menü hervorheben, statt sie wegzulassen.

  [`b8da5b0`](https://github.com/pgbackrest/pgbackrest/commit/b8da5b061d0f9c5d1cc01e936dc65cbdd9f70be7) Style- und Skriptlinks versionieren, damit veraltete Cache-Inhalte neu abgerufen werden.

  [`ec57431`](https://github.com/pgbackrest/pgbackrest/commit/ec57431aa88860b9058d971b938afb5e35a142c7) Direkt zu einem Abschnitt springen statt dorthin zu gleiten.

  [`46babed`](https://github.com/pgbackrest/pgbackrest/commit/46babedaed8429026efa4592d93a8d9876acad0b) Den Rand, über den das Menü hinausgeht, ausblenden statt hart abschneiden.

  [`17de501`](https://github.com/pgbackrest/pgbackrest/commit/17de50192b7e40d7517a4079451e93da5c39b3f3) Den Balken einer section2-Überschrift unter statt neben dem Titel platzieren.

  [`940f431`](https://github.com/pgbackrest/pgbackrest/commit/940f4311375dda3caabdc0bdd01c36bedf43d46f) Den Seitentitel neben dem Logo zentrieren und bei Zeilenumbruch linksbündig ausrichten.

  [`050ca9e`](https://github.com/pgbackrest/pgbackrest/commit/050ca9e354421530ba4282d95dead90e31d6dc2a) Aufklappbare Details zu den Versionshinweisen hinzufügen.

  [`bd8f99b`](https://github.com/pgbackrest/pgbackrest/commit/bd8f99be00cd4b03a1b234bf7fbaa39f406c0c44) Details zu den Versionshinweisen von v2.33 bis v2.60 hinzufügen.

  [`28a1e3d`](https://github.com/pgbackrest/pgbackrest/commit/28a1e3d6278992e0a347aab19248abdcddefd491) Darstellung der Schlüsselwörter im hellen Modus anpassen.

  [`1911f5f`](https://github.com/pgbackrest/pgbackrest/commit/1911f5f1744ff4bfee528d95e37a0a8d9b77d6b3) Die Versionshistorie bei der Upstream-Integration in CI enden lassen.
- Veröffentlichungsplan dokumentiert.

  Funktionsversionen sind für den dritten Montag im Januar, April, Juli und Oktober vorgesehen. Patchversionen erscheinen bei Bedarf am dritten Montag der übrigen Monate. Die Einleitung der Versionshinweise beschreibt außerdem die Haupt-, Neben- und Patchbestandteile einer Versionsnummer.

  [`9bca69a`](https://github.com/pgbackrest/pgbackrest/commit/9bca69a591abcee0623ff910d0db3e27008cfc25) Veröffentlichungsplan dokumentieren.

  [`c179f3f`](https://github.com/pgbackrest/pgbackrest/commit/c179f3f7d6d6b1963d9d3b98b981786ef9546022) Versionsnummerierung in der Einleitung der Versionshinweise aktualisieren.
- Dokumentationswerkzeuge von C und Perl nach Python migriert.

  Die Dokumentation wird mit `doc/doc.py` statt mit einem von `doc/doc.pl` gestarteten C-Werkzeug erzeugt. Der Dokumentationsbuild benötigt damit kein Perl mehr.

  [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e) Build- und Dokumentationscode von C nach Python migrieren.

  [`fa3d197`](https://github.com/pgbackrest/pgbackrest/commit/fa3d1979b77d6252642c64d708a951914e0a0ac2) Verbleibenden Dokumentationscode von Perl nach Python migrieren.

**Verbesserungen der Testsuite:**

- Testumgebung von C und Perl nach Python migriert.

  Tests werden mit `test/test.py` statt `test/test.pl` ausgeführt. Testcontainer und CI-Runner benötigen kein Perl mehr, und die Testumgebung selbst ist durch Tests abgedeckt.

  [`163e5ba`](https://github.com/pgbackrest/pgbackrest/commit/163e5ba0f9ff72ec730f0b35ddac0e5d68ece531) Testumgebung von C nach Python migrieren.

  [`e25c662`](https://github.com/pgbackrest/pgbackrest/commit/e25c6621e8427e862e4ce0196d059ab651bb276d) Restliche Testumgebung von Perl nach Python migrieren.
- Fil-C-Auftrag zur CI hinzugefügt.

  Fil-C ist eine speichersichere C-Implementierung, die jeden Zeigerzugriff prüft. Sie fand zwei Lesezugriffe außerhalb der Grenzen, die gcc, clang und Valgrind übersehen hatten. Ein neuer Workflow kompiliert und testet außerdem direkt auf dem CI-Runner mit gcc und clang, jeweils mit und ohne optionale Bibliotheken.

  [`f32a5d5`](https://github.com/pgbackrest/pgbackrest/commit/f32a5d5543c4dc547006629bdb2dd52d3edb9205) Workflow zum Kompilieren und Testen auf dem Runner ohne Container hinzufügen.

  [`12396fb`](https://github.com/pgbackrest/pgbackrest/commit/12396fb353bc4aa10c3739b826189e421732adf5) Fil-C-Auftrag zum Kompilierungsworkflow hinzufügen.

  [`908a11a`](https://github.com/pgbackrest/pgbackrest/commit/908a11a841e85d4e66e4aa551380b52aabfe606f) Die Fil-C-Distribution unverändert verwenden, da sie jetzt alle benötigten Bibliotheken enthält.
- Fuzz-Tests für die Leser von `JSON`, `Ini` und `Pack` hinzugefügt.

  Die Leser werden in der CI mit libFuzzer, AddressSanitizer und UndefinedBehaviorSanitizer getestet. Das Fuzzing fand mehrere Fehler beim Lesen ungültiger Eingaben. Beispielsweise konnten tief verschachtelte JSON-Arrays in einer Informationsdatei oder einer Objektspeicherantwort einen Überlauf des Speicherkontextstapels verursachen.

  Commit [`4c65010`](https://github.com/pgbackrest/pgbackrest/commit/4c65010e7d28ea68571732fb275d91266a97ad80)
- Testbenutzernamen zugelassen, die adduser unter Debian ablehnt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Der Testcontainer wird mit demselben Benutzernamen wie der Hostbenutzer erstellt. Debians `adduser` lehnt Namen mit einem Punkt wie `first.last` ab. Daher schlug für diese Benutzer der Container-Build auf Debian-basierten Images fehl.

  Issue [#2858](https://github.com/pgbackrest/pgbackrest/issues/2858); Pull Request [#2859](https://github.com/pgbackrest/pgbackrest/pull/2859); Commit [`ce19dae`](https://github.com/pgbackrest/pgbackrest/commit/ce19dae6a2d6ab3665374ead04c270fd45d563fb)


--------

## Stabile Versionen {#stable-releases}

### v2.59.3 – Versionshinweise {#v2593-release-notes}

*Fehler bei schwachen Verschlüsselungsunterschlüsseln*

*Veröffentlicht am 4. Oktober 2026*

**WICHTIGER HINWEIS**: In früheren Versionen konnten bei einem Fehler beim Zugriff auf die Zufallsdaten des Systems schwache Verschlüsselungsunterschlüssel und Salts erzeugt werden. Weitere Informationen finden Sie unter [Schwache Unterschlüssel und Salts bei der Verschlüsselung](/de/pgbackrest/news/#weak-encryption).

**Fehlerbehebungen:**

- Möglichen Prüfsummenfehler beim Laden verschlüsselter Informationsdateien und Manifeste behoben. (*Behoben von j0uinim. Geprüft von David Steele.*)

  Eine große verschlüsselte Informations- oder Manifestdatei konnte beim Laden ihre letzten Zeilen verlieren, wodurch die Prüfsummenprüfung fehlschlug. Die verlorenen Zeilen mussten in den letzten Verschlüsselungsblock passen, weshalb dies in der Praxis unwahrscheinlich ist.

  Issue [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Pull Request [#2868](https://github.com/pgbackrest/pgbackrest/pull/2868); Commit [`2def063`](https://github.com/pgbackrest/pgbackrest/commit/2def063e06c6f0b7e137309c7ed0d7631a42f6cf)
- Mögliche Erzeugung schwacher Verschlüsselungsunterschlüssel oder Salts behoben. (*Behoben von j0uinim. Geprüft von David Steele, Stefan Fercot, Douglas J Hunley.*)

  Konnte OpenSSL keine Zufallsdaten vom Betriebssystem beziehen, wurde der Fehler ignoriert. Unterschlüssel und Salts wurden dann aus nicht zufälligen Speicherinhalten erzeugt. Nun wird ein Fehler gemeldet.

  Issue [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Pull Request [#2867](https://github.com/pgbackrest/pgbackrest/pull/2867); Commit [`47ed78f`](https://github.com/pgbackrest/pgbackrest/commit/47ed78f8d54a44466a872852939edc0273172bf1)

### v2.59.2 – Versionshinweise {#v2592-release-notes}

*Unterstützung für PostgreSQL 19beta4*

*Veröffentlicht am 27. September 2026*

**Fehlerbehebungen:**

- Fehler bei einer leeren Blockzuordnung behoben, wenn eine Datei während des Backups auf die Länge null gekürzt wird. (*Geprüft von Douglas J Hunley. Gemeldet von JPCOSTA78.*)

  Eine blockinkrementelle Datei, die größer als `repo-bundle-limit` war und während eines Backups von PostgreSQL auf null gekürzt wurde, wurde als Blockzuordnung ohne Blöcke gespeichert. Jedes spätere Backup, das auf diese Datei verwies, schlug bis zum nächsten vollständigen Backup mit „unexpected eof“ fehl.

  Issue [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Pull Request [#2842](https://github.com/pgbackrest/pgbackrest/pull/2842); Commit [`572d163`](https://github.com/pgbackrest/pgbackrest/commit/572d1631026d5f10915634592b547f3439b7a291)
- Wiederholungen von Lesevorgängen deaktiviert, wenn Filter an den Treiber übergeben werden. (*Geprüft von Douglas J Hunley. Gemeldet von megamaced.*)

  Das Wiederholen eines Lesevorgangs aus einem Objektspeicher-Repository über einen Repository-Host führte zu einem Absturz. Der Client wiederholt diese Lesevorgänge nicht mehr. Der Repository-Host wiederholt seine Lesevorgänge aus dem Objektspeicher weiterhin.

  Issue [#2845](https://github.com/pgbackrest/pgbackrest/issues/2845); Pull Request [#2846](https://github.com/pgbackrest/pgbackrest/pull/2846); Commit [`c6eca28`](https://github.com/pgbackrest/pgbackrest/commit/c6eca28ff8e551bd2e76f0c91b1a70ddee60b35e)
- Seitenweises Auflisten von S3-Versionen korrigiert. (*Geprüft von Douglas J Hunley, guruguruguru. Gemeldet von guruguruguru.*)

  Das Lesen eines Repositorys zu einem Zielzeitpunkt mit `repo-target-time` schlug mit „unable to find child 'NextContinuationToken'“ fehl, wenn unter einem Präfix mehr als tausend Versionen aufgelistet wurden.

  Issue [#2854](https://github.com/pgbackrest/pgbackrest/issues/2854); Pull Request [#2855](https://github.com/pgbackrest/pgbackrest/pull/2855); Commit [`6f0490d`](https://github.com/pgbackrest/pgbackrest/commit/6f0490dd29f0c756e6766fd9be023805540815fc)
- Azure-Versionsheader für die `SAS`-Authentifizierung gesetzt. (*Geprüft von Douglas J Hunley. Gemeldet von Florian Helmberger.*)

  Batch-Löschungen benötigen den Versionsheader. Bei `SAS`-Authentifizierung wurde daher jeder Batch abgelehnt. Die Ablehnung sah wie der Fehler einer einzelnen Datei aus; der Rest des Batches wurde nicht gelöscht, obwohl `expire` Erfolg meldete. Dadurch blieben abgelaufene Backups und WAL im Repository.

  Issue [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Pull Request [#2848](https://github.com/pgbackrest/pgbackrest/pull/2848); Commit [`ea3293b`](https://github.com/pgbackrest/pgbackrest/commit/ea3293be75c86b5e6c9ca4158b5ebe2a3224f76f)
- Hängenbleiben des asynchronen `archive-push` an einer Backup-Historiendatei mit der Größe null behoben. (*Behoben von Andrew Kroh. Geprüft von David Steele, Douglas J Hunley.*)

  Eine Backup-Historiendatei mit der Größe null, etwa in einem aus einem Speicher-Snapshot kopierten Cluster, ließ jeden asynchronen `archive-push`-Lauf fehlschlagen. Dadurch wurde kein WAL archiviert. `archive-push-batch-size` wird nun anhand der Größe des ersten bereitstehenden WAL-Segments in eine Segmentanzahl umgerechnet.

  Issue [#2856](https://github.com/pgbackrest/pgbackrest/issues/2856); Pull Request [#2857](https://github.com/pgbackrest/pgbackrest/pull/2857); Commit [`12b1b3c`](https://github.com/pgbackrest/pgbackrest/commit/12b1b3cf58caee7b04ed788eee221726f5caa155)
- Befehl `annotate` auf einem entfernten verschlüsselten Repository korrigiert. (*Behoben von Douglas J Hunley. Geprüft von David Steele.*)

  War das Repository verschlüsselt und die Verschlüsselung nur auf dem Repository-Host konfiguriert, konnte `annotate` die Datei `backup.info` nicht laden.

  Commit [`497ad5a`](https://github.com/pgbackrest/pgbackrest/commit/497ad5aee0c654611d2ad4185958727e1341dd8c)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta4/rc1.

  PostgreSQL 19beta4 nahm die Online-Änderungen an Seitenprüfsummen zurück, sodass die Seitenprüfsummenversion wieder auf 0 und 1 beschränkt ist. Außerdem wurden die Version von `pg_control` und die magische Zahl der WAL-Seiten geändert.

  Commit [`89eae83`](https://github.com/pgbackrest/pgbackrest/commit/89eae839d5ca79591aaea8157f437688c3b53df4)

### v2.59.1 – Versionshinweise {#v2591-release-notes}

*Unterstützung für PostgreSQL 19beta3*

*Veröffentlicht am 17. August 2026*

**Fehlerbehebungen:**

- Hängenbleiben behoben, wenn der Chunk-Puffer kleiner als der Eingabepuffer ist. (*Geprüft von Andrew Pogrebnoi, Douglas J Hunley. Gemeldet von crajac66.*)

  Ein mehrteiliger Upload nach S3, GCS oder Azure konnte endlos laufen, wenn der Chunk-Puffer kleiner als der Eingabepuffer war, beispielsweise nachdem die Chunk-Größe während des Uploads erhöht worden war. Der Chunk-Puffer ist nun immer groß genug, um den Eingabepuffer aufzunehmen.

  Issue [#2818](https://github.com/pgbackrest/pgbackrest/issues/2818); Pull Request [#2819](https://github.com/pgbackrest/pgbackrest/pull/2819); Commit [`a53e470`](https://github.com/pgbackrest/pgbackrest/commit/a53e470eca258c2db088af55be307403c8f43b7a)
- Neue Backup-Kennzeichnung nur mit ihrem eigenen vollständigen Backup-Satz verglichen. (*Geprüft von Douglas J Hunley. Gemeldet von Anton Glushakov.*)

  Einige Objektspeicher listen ein Präfix weiter auf, nachdem alle darunterliegenden Objekte gelöscht wurden, etwa MinIO mit Objektsperren oder SeaweedFS. Ein entferntes vollständiges Backup konnte dadurch weiterhin im Repository erscheinen. Alle folgenden differenziellen und inkrementellen Backups schlugen dann mit „new backup label ... is not later than latest backup label ...“ fehl. Eine neue Kennzeichnung wird nun nur mit den Backups ihres eigenen vollständigen Backup-Satzes verglichen.

  Issue [#2792](https://github.com/pgbackrest/pgbackrest/issues/2792); Pull Request [#2824](https://github.com/pgbackrest/pgbackrest/pull/2824); Commit [`d01f77e`](https://github.com/pgbackrest/pgbackrest/commit/d01f77e8237f5d008bb7782c18ced12cd6d1971a)
- Von GitHub erzeugte Quellcodearchive korrigiert, in denen für den Build erforderliche Dateien fehlten. (*Gemeldet von aardvarkzed.*)

  In den von GitHub für eine Veröffentlichung erzeugten Quellcodearchiven fehlten die Werkzeuge zur Codegenerierung und deren Eingabedateien. Deshalb ließen sie sich nicht kompilieren. Nun wird nur noch der Distributions-Tarball um diese Dateien gekürzt.

  Issue [#2821](https://github.com/pgbackrest/pgbackrest/issues/2821); Commit [`163670a`](https://github.com/pgbackrest/pgbackrest/commit/163670a4eeede6d2d170b5d1f55c5ba0b66ba564)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta3. (*Beigetragen von Lardière Sébastien. Geprüft von David Steele.*)

  PostgreSQL 19beta3 änderte die magische Zahl der WAL-Seiten.

  Commit [`5cbc256`](https://github.com/pgbackrest/pgbackrest/commit/5cbc256bf37a44fa478d73a12a2e5b2d84fa6337)

**Verbesserungen der Dokumentation:**

- Ausnahme für Punkte in S3-Bucket-Namen bei `repo-s3-uri-style=path` dokumentiert.

  Bei `repo-s3-uri-style=path` ist der Bucket Teil des Pfads statt des Hostnamens. Punkte im Bucket-Namen verursachen daher keine Abweichung vom Hostnamen im Zertifikat.

  Commit [`bbdc4b9`](https://github.com/pgbackrest/pgbackrest/commit/bbdc4b9217a0e66f6a01c05f4edc04282cffb3fc)
- Explizite Konfiguration von `hot_standby` aus dem Benutzerhandbuch entfernt.

  `hot_standby` ist seit PostgreSQL 10 standardmäßig aktiviert. Die Schnellstartanleitung weist nun darauf hin, dass ein Standby ohne diese Einstellung keine schreibgeschützten Verbindungen annimmt.

  Commit [`cda454d`](https://github.com/pgbackrest/pgbackrest/commit/cda454d4bac0c0412230a0b41513659a7d0d4205)

### v2.59.0 – Versionshinweise {#v2590-release-notes}

*Unterstützung für PostgreSQL 19beta2*

*Veröffentlicht am 20. Juli 2026*

**HINWEIS FÜR PAKETBETREUER**: Ein neuer Distributions-Tarball vereinfacht den Build, indem er vorgenerierte HTML-Dokumentation, eine Manpage und Code bereitstellt. Der Tarball ist jeder Veröffentlichung als Datei mit dem Namen `pgbackrest-{version}.tar.gz` beigefügt. Einzelheiten stehen in der `README.md` im Tarball. Bitte verwenden Sie den neuen Distributions-Tarball, um die zusätzlichen Build-Werkzeuge zu vermeiden, die in künftigen Versionen zur Codegenerierung erforderlich sein werden. Weitere Informationen stehen unter [Neuer Distributions-Tarball](/de/pgbackrest/news/#distribution-tarball).<br/> <br/> **HINWEIS FÜR PAKETBETREUER**: Es gibt eine neue optionale Abhängigkeit von `libsystemd`.<br/> <br/> **WICHTIGER HINWEIS**: Ab dieser Version darf standardmäßig nur der Befehl `restore` als root ausgeführt werden. Mit `allow-root` können andere Befehle als root ausgeführt werden (dies wird jedoch nicht empfohlen).

**Fehlerbehebungen:**

- Fehler behoben, durch den `expire` ein auf einem anderen Host laufendes Backup entfernte. (*Geprüft von Douglas J Hunley. Gemeldet von Dmitrii.*)

  Ein Backup wird erst nach seinem Abschluss zu `backup.info` hinzugefügt. Lief `expire` auf einem Host, während auf einem anderen ein Backup erstellt wurde, etwa `expire` auf einem Standby während des Backups des Primärservers, wurde das laufende Backup entfernt. Das Entfernen abgelaufener Backups löscht nun das neueste Backup nicht mehr, solange es läuft oder fortgesetzt werden kann.

  Issue [#2622](https://github.com/pgbackrest/pgbackrest/issues/2622); Pull Request [#2797](https://github.com/pgbackrest/pgbackrest/pull/2797); Commit [`aa0e215`](https://github.com/pgbackrest/pgbackrest/commit/aa0e215019f50f92a8f0c97f907affc1d3bf86c4)
- Fehler behoben, durch den `archive-push-queue-max` bei einem Fehler einer WAL-Datei nicht durchgesetzt wurde. (*Geprüft von Stefan Fercot. Gemeldet von vut12.*)

  Im asynchronen Modus wurde die Warteschlange anhand der noch zu übertragenden WAL-Dateien gemessen. Schlug eine WAL-Datei wiederholt fehl, wurden die nachfolgenden WAL-Dateien übertragen und nicht mehr mitgezählt, obwohl sie in `pg_wal` verblieben. Dadurch wurde die Warteschlangengrenze nie erreicht und `pg_wal` konnte den Datenträger füllen. Nun werden wie im synchronen Modus alle WAL-Dateien gezählt, auf deren Archivierung PostgreSQL wartet.

  Issue [#2629](https://github.com/pgbackrest/pgbackrest/issues/2629); Pull Request [#2799](https://github.com/pgbackrest/pgbackrest/pull/2799); Commit [`7fe3636`](https://github.com/pgbackrest/pgbackrest/commit/7fe363658639bbc2f70e53496fa6da4acb9e481e)
- Fehler beim asynchronen `archive-get` während einer Recovery über einen Timeline-Wechsel hinweg behoben. (*Geprüft von Douglas J Hunley. Gemeldet von Jimmy Yih.*)

  Zwei asynchrone Prozesse konnten um die Archivsperre konkurrieren. Der unterlegene Prozess beendete sich, bevor er das Segment abrief, für das er gestartet worden war. Das aufrufende `archive-get` wartete dann bis `archive-timeout` und meldete einen Fehler für ein vorhandenes Segment. Dies konnte die Recovery vorzeitig beenden, besonders bei einem Timeline-Wechsel. Das Segment wird nun direkt abgerufen, wenn der dafür vorgesehene asynchrone Prozess nicht läuft.

  Issue [#2423](https://github.com/pgbackrest/pgbackrest/issues/2423); Pull Request [#2806](https://github.com/pgbackrest/pgbackrest/pull/2806); Commit [`baed942`](https://github.com/pgbackrest/pgbackrest/commit/baed942af0d61fcf3c2cb1f7d1bf1d6fe5bb6df9)
- Möglichen Pufferüberlauf im Fehlermodul behoben. (*Behoben von Christophe Pettus. Geprüft von David Steele.*)

  Ein für seinen Puffer zu langer Stacktrace wurde nicht terminiert und konnte über das Pufferende hinaus gelesen werden. Eine für ihren Puffer zu lange Fehlermeldung konnte beim Anhängen eines Systemfehlers über das Pufferende hinaus schreiben. Beide Fälle erfordern eine ungewöhnlich lange Meldung.

  [`7fd8bc8`](https://github.com/pgbackrest/pgbackrest/commit/7fd8bc89a15cb039111aa85fd37f9dc68f7c4d6d) Möglichen Pufferüberlauf im Fehlermodul beheben.

  [`5ca98ab`](https://github.com/pgbackrest/pgbackrest/commit/5ca98abc91f823ef97ff6a1e77d65727d1259218) Beim Formatieren von Fehlermeldungen den gesamten Puffer nutzen.

  [`3a71dc8`](https://github.com/pgbackrest/pgbackrest/commit/3a71dc839a89b83f592c1d5813c068bcded1b6bc) Bei überlangen Meldungen Schreibzugriffe außerhalb des Fehlerpuffers verhindern.
- Zugriff auf bereits freigegebenen Speicher im parallelen Protokollclient behoben. (*Geprüft von Douglas J Hunley. Gemeldet von Georgy Shelkovy.*)

  Ein Client ohne weitere Arbeit wurde freigegeben, blieb aber in der Clientliste und wurde bei einem späteren Aufruf erneut freigegeben. Bei Debug- oder Trace-Protokollierung wurde dadurch auf freigegebenen Speicher zugegriffen, was einen Absturz auslösen konnte, etwa bei einem parallelen Backup mit `log-level-file=trace`.

  Issue [#2754](https://github.com/pgbackrest/pgbackrest/issues/2754); Pull Request [#2804](https://github.com/pgbackrest/pgbackrest/pull/2804); Commit [`31432ed`](https://github.com/pgbackrest/pgbackrest/commit/31432ed3977302b5e183f2b592d85afb521b4f55)
- Heap-Überlauf behoben, wenn eine pg-Option ohne pg1 gesetzt wird. (*Geprüft von Douglas J Hunley. Gemeldet von Naveen.*)

  Wurden `pg`-Optionen für andere Indizes ohne `pg1-path` gesetzt, etwa `pg2-path` und `pg3-path`, wurde die Indexzuordnung überschrieben. Unter musl, beispielsweise auf Alpine, wurde dadurch der Heap beschädigt und ein Segmentierungsfehler ausgelöst. Außerdem fiel der `pg-path` mit der höchsten Nummer weg.

  Issue [#1768](https://github.com/pgbackrest/pgbackrest/issues/1768); Pull Request [#2796](https://github.com/pgbackrest/pgbackrest/pull/2796); Commit [`2d767de`](https://github.com/pgbackrest/pgbackrest/commit/2d767de3c59cf5570639e75755dc73c626fb99e1)
- Absturz behoben, wenn unter musl 1.2.6 während des Beendens ein Signal eintrifft.

  musl 1.2.6, etwa auf Alpine 3.24, stürzt ab, wenn `exit()` während eines bereits laufenden Beendigungsvorgangs aufgerufen wird. Dies geschah, wenn während des Beendens ein Signal eintraf, beispielsweise wenn `server` einen Kindprozess beendete, der sich bereits beendete. Signale während des Beendens werden nun ignoriert.

  Commit [`e166a33`](https://github.com/pgbackrest/pgbackrest/commit/e166a33f48a00192c09b0f1cea3465243c03d1f1)

**Funktionen:**

- Unterstützung für PostgreSQL 19beta1/beta2. (*Geprüft von Stefan Fercot.*)

  Unterstützung für PostgreSQL 19beta1/beta2 hinzugefügt. PostgreSQL 19 kann Seitenprüfsummen im laufenden Betrieb aktivieren und deaktivieren. Während einer dieser Vorgänge werden Seitenprüfsummen nicht geprüft.

  [`bc6d399`](https://github.com/pgbackrest/pgbackrest/commit/bc6d399a6a160f5fa41dd3a98ae046dff66e56a8) Unterstützung für PostgreSQL 19beta1.; Pull Request [#2779](https://github.com/pgbackrest/pgbackrest/pull/2779)

  [`2777395`](https://github.com/pgbackrest/pgbackrest/commit/2777395dacc35aec51572d3e75c621725e2f9d9c) Unterstützung für PostgreSQL 19beta2.
- Option `archive-expire-before` zum Bereinigen des WAL-Archivs hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Die `expire`-Option `archive-expire-before` entfernt WAL vor einem angegebenen Segment aus dem Archiv, jedoch niemals WAL, das ein aufbewahrtes Backup benötigt. Mit `archive_cleanup_command` kann sie das Archiv ab dem Restartpoint eines Standbys bereinigen und so `pg_archivecleanup` ersetzen, das die Aufbewahrungsregeln nicht kennt.

  [`6cd692b`](https://github.com/pgbackrest/pgbackrest/commit/6cd692b1b321faf544ee3a9b1f503fd48007d7c7) WAL-Ablaufbehandlung in expireArchiveId() auslagern.

  [`4945139`](https://github.com/pgbackrest/pgbackrest/commit/4945139392c21f197f2e307abc3c89b5548cef8d) Option archive-expire-before zum Bereinigen des WAL-Archivs hinzufügen.; Pull Request [#2801](https://github.com/pgbackrest/pgbackrest/pull/2801)
- Stapellöschung für Azure-Speicher hinzugefügt. (*Geprüft von Douglas J Hunley, Crispy.*)

  Dateien werden über die Azure Blob Batch API gelöscht, bis zu 256 pro Anfrage statt mit einer Anfrage je Datei. Das beschleunigt `expire` und andere Befehle, die Dateien aus dem Repository entfernen.

  Pull Request [#2786](https://github.com/pgbackrest/pgbackrest/pull/2786); Commit [`ffa325b`](https://github.com/pgbackrest/pgbackrest/commit/ffa325b8a44c1e9e44dc038bbcc8aece6f312a90)
- Unterstützung für S3 Outposts hinzugefügt. (*Beigetragen von Shiva Kumar Ambigi. Geprüft von David Steele, Roberto Mello.*)

  Setzen Sie bei einem S3-Outposts-Endpunkt `repo-s3-service=s3-outposts`. Die Option bestimmt den Dienstnamen für die Signierung von Anfragen und hat den Standardwert `s3`.

  Pull Request [#2762](https://github.com/pgbackrest/pgbackrest/pull/2762); Commit [`6c51800`](https://github.com/pgbackrest/pgbackrest/commit/6c518001c24ad2405eaf750d358f69703322a221)
- S3-Prozessauthentifizierung hinzugefügt. (*Geprüft von Andrew Charlton. Vorgeschlagen von Andrew Charlton.*)

  Setzen Sie `repo-s3-key-type=process` und `repo-s3-process-cmd` auf einen Befehl, der temporäre Anmeldedaten im JSON-Format des AWS-Prozess-Anmeldedatenanbieters ausgibt. Die Anmeldedaten werden vor ihrem Ablauf erneuert.

  Pull Request [#2778](https://github.com/pgbackrest/pgbackrest/pull/2778); Commit [`b5a578a`](https://github.com/pgbackrest/pgbackrest/commit/b5a578a5c2c88d53fca0ee8cfbfb8ee662ce7e48)
- Distributions-Tarball mit generiertem Code und Dokumentation bereitgestellt.

  Der Tarball enthält den generierten Code sowie die fertige Manpage und HTML-Dokumentation. Er lässt sich daher ohne die Werkzeuge zur Code- und Dokumentationsgenerierung einschließlich `libyaml` kompilieren und installieren.

  Commit [`8fcfef5`](https://github.com/pgbackrest/pgbackrest/commit/8fcfef5d8732055f9bc8e50224d5b7a988512e61)

**Verbesserungen:**

- Erneuter Verbindungsaufbau zum SFTP-Speicher, nachdem der Server eine inaktive Verbindung getrennt hat. (*Geprüft von Stefan Fercot. Vorgeschlagen von mustafa0x, tisserat.*)

  SFTP-Server und Firewalls können länger inaktive Verbindungen schließen, etwa die Leseverbindung zum Repository während der Kopierphase eines Backups. Die nächste Nutzung schlug dann mit einem Socketfehler fehl. Eine unterbrochene Verbindung wird nun erneut geöffnet und der Vorgang einmal wiederholt.

  [`d72bea9`](https://github.com/pgbackrest/pgbackrest/commit/d72bea9fe7c3975fc6832a51b0b0c1c041c467d2) In SFTP-Lese-/Schreibobjekten die libssh2-Sitzung aus dem Speicherobjekt holen.

  [`a31febf`](https://github.com/pgbackrest/pgbackrest/commit/a31febfbd9ba639589fe57e4083ae9358b1306a4) SFTP-Speicher neu verbinden, nachdem der Server eine inaktive Verbindung geschlossen hat.; Issue [#2739](https://github.com/pgbackrest/pgbackrest/issues/2739); Issue [#2772](https://github.com/pgbackrest/pgbackrest/issues/2772); Pull Request [#2793](https://github.com/pgbackrest/pgbackrest/pull/2793)
- Zwischenspeicherung von Benutzern und Gruppen für eine schnellere Erstellung des Manifests hinzugefügt. (*Beigetragen von Gunnar Lindholm. Geprüft von David Steele.*)

  Werden Benutzer- und Gruppennamen über einen entfernten Namensdienst wie sssd oder LDAP aufgelöst, benötigt jede Abfrage einen Netzwerk-Roundtrip. Bei Clustern mit Millionen Dateien dominierte dies die Manifesterstellung. Benutzer- und Gruppennamen werden nun zwischengespeichert.

  Pull Request [#2773](https://github.com/pgbackrest/pgbackrest/pull/2773); Commit [`1e6d23f`](https://github.com/pgbackrest/pgbackrest/commit/1e6d23fea72ac9c599f8b62a2e0a3de02d0d08d0)
- Backup-Fortschritt je Repository zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Will Morland. Geprüft von David Steele, Stefan Fercot.*)

  Laufen Backups gleichzeitig für mehrere Repositorys, meldet `info` nun neben dem Gesamtfortschritt auch den Fortschritt je Repository. Die JSON-Ausgabe enthält für jede Backup-Sperre ein `repo`-Array.

  Issue [#2736](https://github.com/pgbackrest/pgbackrest/issues/2736); Pull Request [#2740](https://github.com/pgbackrest/pgbackrest/pull/2740); Commit [`77312b3`](https://github.com/pgbackrest/pgbackrest/commit/77312b33ba913132b33401d862c2e354f323c786)
- Prüfungen von `backup.info` zum Befehl `verify` hinzugefügt. (*Beigetragen von Denis Garsh. Geprüft von David Steele, Douglas J Hunley.*)

  Der Befehl `verify` warnt nun, wenn ein Backup im Repository nicht in `backup.info` steht oder ein in `backup.info` verzeichnetes Backup im Repository fehlt. Ein fehlendes Backup wird als Backup mit fehlendem Manifest gemeldet.

  Issue [#2723](https://github.com/pgbackrest/pgbackrest/issues/2723); Pull Request [#2752](https://github.com/pgbackrest/pgbackrest/pull/2752); Commit [`7f82fb6`](https://github.com/pgbackrest/pgbackrest/commit/7f82fb6635c1e3e9dd285d53076e9aee3fbf1ca2)
- Konfiguration des S3-STS-Endpunkts ermöglicht. (*Beigetragen von Simon Gratton. Geprüft von David Steele.*)

  Setzen Sie `repo-s3-sts-host`, um mit `repo-s3-key-type=web-id` einen regionalen STS-Endpunkt wie `sts.eu-central-2.amazonaws.com` zu verwenden. AWS-Regionen mit gesonderter Aktivierung akzeptieren keine Anmeldedaten vom globalen Endpunkt, der weiterhin der Standard ist.

  Issue [#2791](https://github.com/pgbackrest/pgbackrest/issues/2791); Pull Request [#2798](https://github.com/pgbackrest/pgbackrest/pull/2798); Commit [`11f5582`](https://github.com/pgbackrest/pgbackrest/commit/11f5582dfe696187cab1f15d08f649a5117730b3)
- `archive-push-batch-size` hinzugefügt, um die pro asynchronem Durchlauf übertragene WAL-Menge zu begrenzen. (*Geprüft von Stefan Fercot.*)

  Im asynchronen Modus wird `archive-push-queue-max` nur zu Beginn eines Laufs geprüft. Beim Abarbeiten eines großen Rückstands konnte die Warteschlange dadurch weit über die Grenze anwachsen. `archive-push-batch-size` (Standard 16GiB) begrenzt die pro Lauf übertragenen WAL-Daten, sodass die Warteschlange früher erneut geprüft wird.

  Pull Request [#2803](https://github.com/pgbackrest/pgbackrest/pull/2803); Commit [`34a035f`](https://github.com/pgbackrest/pgbackrest/commit/34a035f4d62f06822c1f60f72a605762cc1ad79c)
- Asynchrones `archive-push` beim ersten Fehler beendet. (*Geprüft von Stefan Fercot. Vorgeschlagen von Lardière Sébastien.*)

  War das Repository nicht verfügbar, versuchte der asynchrone Prozess weiter, jedes bereitstehende WAL-Segment zu übertragen. Ein Lauf konnte so lange dauern, dass sich `pg_wal` füllte, bevor `archive-push-queue-max` erneut geprüft wurde. Der Lauf endet nun nach dem ersten Fehler, sobald die laufenden Aufträge abgeschlossen sind.

  Issue [#1848](https://github.com/pgbackrest/pgbackrest/issues/1848); Pull Request [#2802](https://github.com/pgbackrest/pgbackrest/pull/2802); Commit [`a0c1435`](https://github.com/pgbackrest/pgbackrest/commit/a0c14359392e283d88f72e7f9f815d9e78ddfb10)
- Verarbeitung von HTTP-Antworten mit Chunked-Übertragung robuster gestaltet. (*Beigetragen von Shubham. Geprüft von David Steele.*)

  Chunk-Erweiterungen und Trailer werden nun akzeptiert. `transfer-encoding` wird ohne Beachtung der Groß-/Kleinschreibung verglichen, und Antworten mit sowohl `transfer-encoding` als auch `content-length` werden abgelehnt.

  Pull Request [#2785](https://github.com/pgbackrest/pgbackrest/pull/2785); Commit [`34bba82`](https://github.com/pgbackrest/pgbackrest/commit/34bba828c6ba97579d65c2199c02d94bf31257a5)
- Fehler bei Ausführung als root, sofern `allow-root` nicht aktiviert ist. (*Geprüft von Douglas J Hunley.*)

  Die Ausführung eines anderen Befehls als `restore` als root konnte Dateien im Repository erzeugen, etwa `backup.info`, auf die der PostgreSQL-Benutzer nicht zugreifen konnte. `allow-root` ist für alle Befehle außer `restore` standardmäßig deaktiviert. Die Prüfung gilt auch auf entfernten Hosts.

  Issue [#1693](https://github.com/pgbackrest/pgbackrest/issues/1693); Pull Request [#2812](https://github.com/pgbackrest/pgbackrest/pull/2812); Commit [`0daf53d`](https://github.com/pgbackrest/pgbackrest/commit/0daf53da03fb179b5771b6aaa559f9e0cc5842bb)
- Anzahl binärer Suchen beim Erstellen des Manifests reduziert. (*Beigetragen von Gunnar Lindholm. Geprüft von David Steele.*)

  Bei der Manifesterstellung eines differenziellen oder inkrementellen Backups wurde für jede Datei dreimal im vorherigen Manifest gesucht. Nun genügt eine Suche. Bei Clustern mit Millionen Dateien spart dies Millionen Suchvorgänge.

  Pull Request [#2774](https://github.com/pgbackrest/pgbackrest/pull/2774); Commit [`f1ef629`](https://github.com/pgbackrest/pgbackrest/commit/f1ef62956adabf305a7e959477ea1bb668fd8d65)
- Leistung bei der Positionierung innerhalb von Dateien während blockinkrementeller Delta-Wiederherstellungen verbessert. (*Geprüft von David Christensen, Douglas J Hunley.*)

  Bei einer blockinkrementellen Delta-Wiederherstellung wurden für jeden geschriebenen Block die Dateiposition gesetzt und der Schreibpuffer geleert; Blöcke sind oft nur 8KiB groß. Die Dateiposition wird nun nachverfolgt, und Positionierung sowie Pufferleerung erfolgen nur bei Bedarf.

  Pull Request [#2732](https://github.com/pgbackrest/pgbackrest/pull/2732); Commit [`b908d5e`](https://github.com/pgbackrest/pgbackrest/commit/b908d5e2c5b37ef968f19e2c40a1001e19e5b87f)
- Backup-Dateien der Reihe nach gebündelt, anstatt nach einer besser passenden Datei zu suchen. (*Geprüft von Stefan Fercot.*)

  Eine Datei, die ein Bündel über `repo-bundle-size` hinaus vergrößert hätte, wurde zugunsten einer späteren kleineren Datei in der Warteschlange übersprungen. Dateien werden nun der Reihe nach hinzugefügt. Ein Bündel wird geschlossen, sobald es `repo-bundle-size` erreicht, und kann diese Größe daher um bis zu `repo-bundle-limit` überschreiten.

  Pull Request [#2794](https://github.com/pgbackrest/pgbackrest/pull/2794); Commit [`253dbc3`](https://github.com/pgbackrest/pgbackrest/commit/253dbc3f03e5581c98bb97b252dc77b8defd3693)
- Zugrunde liegenden Fehler gemeldet, wenn eine Abfrage nicht abgeschlossen werden kann. (*Geprüft von Andrew Pogrebnoi. Vorgeschlagen von Marco Fontana.*)

  Ging die Verbindung nach Übermittlung des ersten Abfrageergebnisses verloren, etwa unter Last, erschien nur die allgemeine Meldung „NULL result required to complete request“. Nun wird der PostgreSQL-Fehler ausgegeben, ergänzt um Hinweise auf einen Verbindungsverlust sowie zu aggressive Einstellungen von `idle_session_timeout` und `idle_in_transaction_session_timeout`.

  Issue [#2789](https://github.com/pgbackrest/pgbackrest/issues/2789); Pull Request [#2790](https://github.com/pgbackrest/pgbackrest/pull/2790); Commit [`23e966c`](https://github.com/pgbackrest/pgbackrest/commit/23e966cd8f17a8cd446b04901d0ae66ebf4118ee)
- Tatsächlichen Fehler gemeldet, wenn eine Anfrage nach S3-Zugangsdaten fehlschlägt. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Mitchell Grice.*)

  Ein AWS-Fehler bei einer Anforderung von `web-id`- oder `pod-id`-Anmeldedaten wurde als Fehler beim Analysieren der Antwort gemeldet. Nun wird der von AWS zurückgegebene Fehler ausgegeben; beim Protokollieren der Anfrage werden Tokens unkenntlich gemacht.

  Issue [#1997](https://github.com/pgbackrest/pgbackrest/issues/1997); Pull Request [#2808](https://github.com/pgbackrest/pgbackrest/pull/2808); Commit [`b0c57c2`](https://github.com/pgbackrest/pgbackrest/commit/b0c57c280d727e743b72a6d86e2c3e413307e44b)
- Fehler des Spool-Pfads von `archive-push` im PostgreSQL-Protokoll gemeldet. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Don Seiler.*)

  Konnte der asynchrone Spool-Pfad nicht erstellt werden, etwa wegen fehlender Berechtigung, ließ sich der Fehler nicht in den Spool schreiben. `archive-push` scheiterte dann mit einer allgemeinen Zeitüberschreitung und einem Verweis auf das asynchrone Protokoll. Der Spool-Pfad wird nun vor dem Start des asynchronen Prozesses erstellt, sodass der Fehler im PostgreSQL-Protokoll erscheint.

  Issue [#1408](https://github.com/pgbackrest/pgbackrest/issues/1408); Pull Request [#2810](https://github.com/pgbackrest/pgbackrest/pull/2810); Commit [`7b0159c`](https://github.com/pgbackrest/pgbackrest/commit/7b0159c7dfd69763b63b1385fd564c18a4a5c1bc)
- Bei einer nicht unterstützten Version auf ein möglicherweise veraltetes pgBackRest hingewiesen.

  Erkennt pgBackRest eine PostgreSQL-Version nicht, etwa wenn ein älteres pgBackRest auf dem Wiederherstellungshost ein Backup eines neueren Clusters liest, weist der Fehler nun auf eine möglicherweise notwendige Aktualisierung von pgBackRest auf allen Hosts hin. Die Version wird in benutzerfreundlicher Form ausgegeben, etwa 13 statt 130000.

  Commit [`d4f697e`](https://github.com/pgbackrest/pgbackrest/commit/d4f697ebce705f9439798f970103fd38f829dfff)
- Integration von systemd-Benachrichtigungen hinzugefügt. (*Beigetragen von Andrew Jackson. Geprüft von David Steele.*)

  Bei einem Build mit `libsystemd` benachrichtigt der Befehl `server` systemd, sobald er Verbindungen annehmen kann und wenn er beendet wird, wie es auch PostgreSQL und PgBouncer tun.

  Issue [#2757](https://github.com/pgbackrest/pgbackrest/issues/2757); Pull Request [#2760](https://github.com/pgbackrest/pgbackrest/pull/2760); Commit [`742fff1`](https://github.com/pgbackrest/pgbackrest/commit/742fff174a3f5baaed932afa284334ca2aa1be82)
- Fehler `unused parameter` in meson-Compilerprüfungen unterdrückt. (*Beigetragen von Jörg Plate. Geprüft von David Steele.*)

  Die Compilerprüfungen von meson deklarierten ungenutzte Parameter von `main()`. Wurden Warnungen über ungenutzte Parameter als Fehler behandelt, schlugen diese Prüfungen fehl.

  Issue [#2724](https://github.com/pgbackrest/pgbackrest/issues/2724); Commit [`d4465bd`](https://github.com/pgbackrest/pgbackrest/commit/d4465bd6f78d6d58d18ebedbe8f63b55d0ae2508)
- C11 ist nun der mindestens erforderliche C-Standard. (*Geprüft von Mohammad Ali Nazir Kosar.*)

  Pull Request [#2738](https://github.com/pgbackrest/pgbackrest/pull/2738); Commit [`3a6c671`](https://github.com/pgbackrest/pgbackrest/commit/3a6c67183cd9c6a12c24f0d978ef5e501b7c3fcf)

**Verbesserungen der Dokumentation:**

- Option `stanza` für die Befehle `repo-*` als intern gekennzeichnet. (*Geprüft von Stefan Fercot.*)

  Die Option `stanza` wirkt bei `repo-*`-Befehlen nur zusammen mit undokumentierten Speicherpfadkonstanten. Die Dokumentation erweckte daher den Eindruck einer Wirkung, die sie nicht hatte. Die Option wird für diese Befehle nicht mehr dokumentiert und funktioniert unverändert.

  Issue [#2735](https://github.com/pgbackrest/pgbackrest/issues/2735); Commit [`3e9eabd`](https://github.com/pgbackrest/pgbackrest/commit/3e9eabd8a5551cdaeb6bc78a52f000eaf239defb)
- Dokumentiert, dass info die Verschlüsselungseinstellungen aus dem globalen Abschnitt liest. (*Geprüft von Stefan Fercot. Vorgeschlagen von Ron Johnson.*)

  Ohne `stanza` liest `info` die Verschlüsselungseinstellungen nur aus dem globalen Abschnitt. Für eine Stanza konfigurierte Verschlüsselungseinstellungen erfordern daher `stanza`.

  Issue [#1407](https://github.com/pgbackrest/pgbackrest/issues/1407); Pull Request [#2805](https://github.com/pgbackrest/pgbackrest/pull/2805); Commit [`2137bda`](https://github.com/pgbackrest/pgbackrest/commit/2137bda1a5a1ad890d0137feffe8491102041af3)
- Dokumentiert, dass `expire-auto` die Konfiguration des Befehls `backup` verwendet. (*Geprüft von Stefan Fercot. Vorgeschlagen von Lardière Sébastien.*)

  Das automatische Entfernen abgelaufener Backups nach einem Backup verwendet die Konfiguration von `backup`. Optionen, die nur für `expire` gesetzt sind, gelten dabei nicht. Deaktivieren Sie `expire-auto` und führen Sie `expire` separat aus, wenn eine eigene Konfiguration erforderlich ist.

  Issue [#1874](https://github.com/pgbackrest/pgbackrest/issues/1874); Pull Request [#2807](https://github.com/pgbackrest/pgbackrest/pull/2807); Commit [`cf847f9`](https://github.com/pgbackrest/pgbackrest/commit/cf847f94cd7ab6517ec1abb30075fb53dc75d5f8)
- Anpassung der logrotate-Direktive `su` für einen eigenen Benutzer dokumentiert. (*Geprüft von Douglas J Hunley. Vorgeschlagen von lkanbus.*)

  Pakete können eine logrotate-Konfiguration installieren, die Protokolle als Benutzer `postgres` rotiert. Gehören Repository und Protokolle einem eigenen Benutzer, muss die `su`-Direktive auf diesen Benutzer geändert werden. Andernfalls schlägt die Rotation mit einem Berechtigungsfehler fehl.

  Issue [#2737](https://github.com/pgbackrest/pgbackrest/issues/2737); Pull Request [#2809](https://github.com/pgbackrest/pgbackrest/pull/2809); Commit [`bde2c50`](https://github.com/pgbackrest/pgbackrest/commit/bde2c509c923fbe2844c10b0f95c55973378d2ae)
- Dokumentiert, dass Kommentare am Zeilenende in Konfigurationsdateien nicht unterstützt werden. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Alex Richman.*)

  Kommentare am Zeilenende wurden nie unterstützt, auch wenn sie bei manchen Optionen scheinbar funktionieren. Unterstützt werden nur Kommentare auf einer eigenen Zeile.

  Issue [#1633](https://github.com/pgbackrest/pgbackrest/issues/1633); Pull Request [#2811](https://github.com/pgbackrest/pgbackrest/pull/2811); Commit [`8571799`](https://github.com/pgbackrest/pgbackrest/commit/85717992cadbfdabc571fb23914b62b08c7f6f44)

**Verbesserungen der Testsuite:**

- Gruppenkonflikte von Alpine in CI-Containern behoben. (*Beigetragen von Artur Zakirov. Geprüft von David Steele.*)

  Beim Umbenennen der Testgruppe werden nun auch Gruppeneinträge mit Mitgliedern berücksichtigt. Die Alpine-Gruppe wird nur erstellt, wenn sie noch nicht existiert.

  Pull Request [#2784](https://github.com/pgbackrest/pgbackrest/pull/2784); Commit [`760dd8d`](https://github.com/pgbackrest/pgbackrest/commit/760dd8db69e7c6e5cbb9c5b7e2067b6813cf4497)

### v2.58.0 – Versionshinweise {#v2580-release-notes}

*Verbesserungen für Objektspeicher*

*Veröffentlicht am 19. Januar 2026*

**WICHTIGER HINWEIS**: Die Mindestwerte der Option `repo-storage-upload-chunk-size` wurden erhöht. Sie entsprechen nun den von den Anbietern zugelassenen Mindestwerten.

**Fehlerbehebungen:**

- Deadlock durch Protokollierung im Signalhandler behoben. (*Behoben von Maxim Michkov. Geprüft von David Steele.*)

  Ein Signal, das eintraf, während `gmtime_r()` eine Sperre hielt, etwa das von `stop` mit `--force` gesendete SIGTERM, konnte beim Protokollieren im Signalhandler einen Deadlock auslösen. Der Signalhandler protokolliert nun ausschließlich mit Funktionen, die für asynchrone Signale sicher sind.

  Issue [#2710](https://github.com/pgbackrest/pgbackrest/issues/2710); Pull Request [#2715](https://github.com/pgbackrest/pgbackrest/pull/2715); Commit [`e13c462`](https://github.com/pgbackrest/pgbackrest/commit/e13c462908c6ee25f8795b5d1373981549d4d5cf)

**Funktionen:**

- HTTP-Unterstützung für S3, GCS und Azure. (*Beigetragen von Will Morland. Geprüft von David Steele.*)

  Ein Objektspeicher-Endpunkt kann nun mit `http://` beginnen, um ohne TLS zu verbinden. Fehlt eine Protokollangabe, wird weiterhin HTTPS verwendet.

  Issue [#2340](https://github.com/pgbackrest/pgbackrest/issues/2340); Pull Request [#2703](https://github.com/pgbackrest/pgbackrest/pull/2703); Commit [`2398dd4`](https://github.com/pgbackrest/pgbackrest/commit/2398dd4d432d312b3641e9fbbcbe0487ad43112d)
- Entfernen des ältesten vollständigen Backups unabhängig von der aktuellen Aufbewahrung ermöglicht. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Ron Johnson.*)

  Die `expire`-Option `--oldest` entfernt das älteste vollständige Backup und seine abhängigen Backups unabhängig von den Aufbewahrungseinstellungen, etwa wenn der Speicherplatz im Repository knapp wird. Auch WAL vor dem ältesten verbleibenden vollständigen Backup wird entfernt.

  Issue [#2666](https://github.com/pgbackrest/pgbackrest/issues/2666); Pull Request [#2709](https://github.com/pgbackrest/pgbackrest/pull/2709); Commit [`bf2b276`](https://github.com/pgbackrest/pgbackrest/commit/bf2b276dc011464b13039630870934fd42ca473c)
- Unterstützung für verwaltete Identitäten von Azure. (*Beigetragen von Moiz Ibrar, Matthew Mols. Geprüft von David Steele.*)

  Setzen Sie `repo-azure-key-type=auto`, um Anmeldedaten automatisch über verwaltete Identitäten abzurufen, statt sie zu konfigurieren. Die Anmeldedaten werden vor ihrem Ablauf erneuert.

  Issue [#2023](https://github.com/pgbackrest/pgbackrest/issues/2023); Pull Request [#2712](https://github.com/pgbackrest/pgbackrest/pull/2712); Commit [`38f14d7`](https://github.com/pgbackrest/pgbackrest/commit/38f14d73b6a62d06e1ead7942e49a2bb2ae90dab)
- ***Experimentelle*** Unterstützung für S3 EKS Pod Identity. (*Beigetragen von Pierre BOUTELOUP. Geprüft von David Steele.*)

  Setzen Sie `repo-s3-key-type=pod-id`, um Anmeldedaten automatisch über die EKS-Pod-Identität abzurufen, statt sie zu konfigurieren. Die Anmeldedaten werden vor ihrem Ablauf erneuert.

  Issue [#2718](https://github.com/pgbackrest/pgbackrest/issues/2718); Pull Request [#2719](https://github.com/pgbackrest/pgbackrest/pull/2719); Commit [`79544f6`](https://github.com/pgbackrest/pgbackrest/commit/79544f64a3ce198f4685f923739def997fcafbce)
- Konfiguration von TLS-Cipher-Suites ermöglicht. (*Beigetragen von Gunnar "Nick" Bluth. Geprüft von David Steele.*)

  Setzen Sie `tls-cipher-12` für TLS 1.2 und `tls-cipher-13` für TLS 1.3, beispielsweise zur Erfüllung von Compliance-Vorgaben. Die Cipher-Suites gelten für sämtliche Verbindungen eines Prozesses.

  [`fbc607a`](https://github.com/pgbackrest/pgbackrest/commit/fbc607a48b1fb4ae65c9f2691c44453f02aef2b8) Konfiguration von TLS-Cipher-Suites erlauben.; Issue [#2697](https://github.com/pgbackrest/pgbackrest/issues/2697); Pull Request [#2700](https://github.com/pgbackrest/pgbackrest/pull/2700)

  [`91ad655`](https://github.com/pgbackrest/pgbackrest/commit/91ad65537f55aa3825b6c7b626a9e1b7cbb1ad4c) Den in fbc607a4 hinzugefügten instabilen Unit-Test common/io-tls korrigieren.
- Festlegen der Prozesspriorität ermöglicht. (*Geprüft von Douglas J Hunley.*)

  `priority` setzt die Scheduling-Priorität von pgBackRest-Prozessen wie `nice` auf einen Wert von -20 bis 19. Ein höherer Wert verringert die Wahrscheinlichkeit, dass pgBackRest PostgreSQL beeinträchtigt.

  Pull Request [#2693](https://github.com/pgbackrest/pgbackrest/pull/2693); Commit [`0fc7e96`](https://github.com/pgbackrest/pgbackrest/commit/0fc7e96f5addb01e7f6f3585e37d209cc17dd956)

**Verbesserungen:**

- Punkte in S3-Bucket-Namen bei Verwendung pfadbasierter URIs zugelassen. (*Beigetragen von Joakim Hindersson. Geprüft von David Steele.*)

  Punkte im Bucket-Namen verursachen nur bei hostbasierten URIs eine Abweichung vom Hostnamen im Zertifikat. Sie sind daher nun mit `repo-s3-uri-style=path` zulässig, das die meisten selbst betriebenen S3-Dienste verwenden.

  Pull Request [#2713](https://github.com/pgbackrest/pgbackrest/pull/2713); Commit [`3fdb4a1`](https://github.com/pgbackrest/pgbackrest/commit/3fdb4a1ea00b442aca5fc714818d293d57490386)
- TLS >= 1.2 verlangt, sofern die Überprüfung nicht deaktiviert ist. (*Geprüft von Douglas J Hunley, Gunnar "Nick" Bluth.*)

  TLS 1.0 und 1.1 sind seit 2021 veraltet. Für Verbindungen zwischen pgBackRest-Hosts ist die Prüfung stets aktiviert. Wird die Prüfung für einen Objektspeicher mit `repo-storage-verify-tls` deaktiviert, etwa für ein selbstsigniertes Zertifikat, sind alle Protokollversionen zulässig.

  Pull Request [#2720](https://github.com/pgbackrest/pgbackrest/pull/2720); Commit [`5b4b20a`](https://github.com/pgbackrest/pgbackrest/commit/5b4b20a8d7d17c2bffe106595310853e3f3a9604)
- Größe von S3/GCS/Azure-Chunks bei großen Uploads dynamisch angepasst. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Timothée Peignier.*)

  Die Anzahl der Teile eines Uploads ist begrenzt. Mit dem Standardwert von `repo-storage-upload-chunk-size` lag die maximale Dateigröße daher bei 50GiB für S3, 40GiB für GCS und 200GiB für Azure. Die Chunk-Größe wächst nun während des Uploads, sodass Dateien bis 5TiB nach S3 und GCS und bis 45TiB nach Azure übertragen werden können.

  Issue [#2679](https://github.com/pgbackrest/pgbackrest/issues/2679); Pull Request [#2701](https://github.com/pgbackrest/pgbackrest/pull/2701); Commit [`86554fa`](https://github.com/pgbackrest/pgbackrest/commit/86554faa707292855c2776a0c70b5e212b1e3945)
- S3/GCS/Azure-Chunk-Größe für kleine Dateien optimiert. (*Geprüft von Douglas J Hunley.*)

  Beim Öffnen einer Datei wurde der gesamte Chunk-Puffer reserviert, obwohl viele Dateien kleiner als ein Chunk sind. Der Puffer wächst nun mit den eintreffenden Daten. Das spart beim Hochladen kleiner Dateien Speicher.

  Pull Request [#2705](https://github.com/pgbackrest/pgbackrest/pull/2705); Commit [`28bfa20`](https://github.com/pgbackrest/pgbackrest/commit/28bfa20ba3b860f72ba7ab6c018e37ada99e2109)
- Unterstützung für PostgreSQL `9.5` entfernt. (*Geprüft von Douglas J Hunley.*)

  PostgreSQL 9.5 wird nicht mehr unterstützt. Dies entspricht der Richtlinie, fünf PostgreSQL-Versionen nach deren Supportende zu unterstützen.

  Pull Request [#2692](https://github.com/pgbackrest/pgbackrest/pull/2692); Commit [`5171e8b`](https://github.com/pgbackrest/pgbackrest/commit/5171e8bde31b9711c9c5b4ccc5170b61c5235548)
- Protokollierung des Standardwerts für Optionen mit einer nicht aufgelösten Abhängigkeit verbessert. (*Geprüft von Stefan Fercot.*)

  Eine in der Konfigurationsdatei gesetzte Option wurde zu Beginn eines Befehls protokolliert, obwohl ihre Abhängigkeit nicht erfüllt war und ihr Standardwert verwendet wurde. In diesem Fall wird die Option nun nicht mehr protokolliert.

  Issue [#2707](https://github.com/pgbackrest/pgbackrest/issues/2707); Pull Request [#2708](https://github.com/pgbackrest/pgbackrest/pull/2708); Commit [`38ac638`](https://github.com/pgbackrest/pgbackrest/commit/38ac6387cbbfc6f78a686de657e5a4de4ed59295)

**Verbesserungen der Dokumentation:**

- Explizite Konfiguration von `max_wal_senders`/`wal_level` aus dem Benutzerhandbuch entfernt. (*Vorgeschlagen von Jamie Nguyen.*)

  Seit PostgreSQL 10 haben `max_wal_senders` und `wal_level` standardmäßig die vom Benutzerhandbuch verlangten Werte.

  Issue [#2699](https://github.com/pgbackrest/pgbackrest/issues/2699); Commit [`bce97d3`](https://github.com/pgbackrest/pgbackrest/commit/bce97d3ea80675b8eab3dbf692e8bc8f077f30c7)
- Klargestellt, dass Bündelung bei Dateisystemen mit großen Blockgrößen nützlich ist. (*Vorgeschlagen von Ron Johnson.*)

  Das Bündeln spart Platz auf Dateisystemen mit großen Blöcken, auf denen jede kleine Datei einen ganzen Block belegt.

  Issue [#2706](https://github.com/pgbackrest/pgbackrest/issues/2706); Commit [`a7e5f28`](https://github.com/pgbackrest/pgbackrest/commit/a7e5f28511c27f2504a873db26803b26a84df8f1)

### v2.57.0 – Versionshinweise {#v2570-release-notes}

*Symbolische Links im Repository unterdrücken*

*Veröffentlicht am 18. Oktober 2025*

**Fehlerbehebungen:**

- Verschachtelung der Zeitüberschreitungen für HTTP/TLS/Sockets aufgehoben. (*Geprüft von David Christensen.*)

  Eine fehlgeschlagene Socketverbindung wurde auch von der TLS- und HTTP-Schicht wiederholt. Mit dem Standardwert von 60 Sekunden für `io-timeout` dauerte es daher neun Minuten, bis eine Verbindung endgültig abbrach. Jede Schicht wiederholt nun nur noch ihre eigenen Fehler.

  Issue [#2654](https://github.com/pgbackrest/pgbackrest/issues/2654); Pull Request [#2662](https://github.com/pgbackrest/pgbackrest/pull/2662); Commit [`9c7f064`](https://github.com/pgbackrest/pgbackrest/commit/9c7f0648648e651d82918e5dbfc3d511abee3298)
- Möglichen Segfault in der Fehlermeldung zu Seitenprüfsummen behoben. (*Behoben von Zsolt Parragi. Geprüft von David Steele.*)

  Die Fehlermeldung für ungültige Seitenprüfsummen verwendete eine Zeichenkette außerhalb ihres Gültigkeitsbereichs. Dadurch konnten unbrauchbare Daten protokolliert werden oder ein Absturz auftreten. Besonders wahrscheinlich war dies mit pg_tde, da jede verschlüsselte Datei die Seitenprüfsummenprüfung nicht besteht.

  Pull Request [#2675](https://github.com/pgbackrest/pgbackrest/pull/2675); Commit [`adc5e5b`](https://github.com/pgbackrest/pgbackrest/commit/adc5e5b23b9b544745724a7eaa0461b88b691e36)
- Möglichen Segmentierungsfehler in Meldungen zur Backup-Fortsetzung behoben.

  Die Meldung darüber, warum ein Backup nicht fortgesetzt werden kann, verwendete eine Zeichenkette außerhalb ihres Gültigkeitsbereichs. Dies konnte zu unbrauchbaren Protokolldaten oder einem Absturz führen.

  Commit [`c1c40a4`](https://github.com/pgbackrest/pgbackrest/commit/c1c40a4a851efe98be83aca2044c02fd1c7fb2ae)

**Funktionen:**

- Option `repo-symlink` hinzugefügt, um die Erstellung symbolischer Links im Repository zu unterdrücken. (*Geprüft von Douglas J Hunley. Vorgeschlagen von Ron Johnson.*)

  Einige ansonsten Posix-kompatible Dateisysteme unterstützen keine symbolischen Links. Mit `repo-symlink=n` wird verhindert, dass der symbolische Link `latest` und die Tablespace-Links im Repository angelegt werden.

  Issue [#2673](https://github.com/pgbackrest/pgbackrest/issues/2673); Pull Request [#2674](https://github.com/pgbackrest/pgbackrest/pull/2674); Commit [`bfd9790`](https://github.com/pgbackrest/pgbackrest/commit/bfd97907311a25ed239798691cff52cf73acdb83)

**Verbesserungen:**

- HTTP-Wiederholungsversuche für die Fehler 408 und 429 hinzugefügt. (*Geprüft von David Christensen.*)

  Anfragen mit HTTP-Fehlern 408 (Request Timeout) und 429 (Too Many Requests) werden nun wiederholt. Fehler 429 treten bei Cloudflare R2 häufig auf.

  Pull Request [#2661](https://github.com/pgbackrest/pgbackrest/pull/2661); Commit [`8733900`](https://github.com/pgbackrest/pgbackrest/commit/87339004e59c03d2a03a6ceb8426202346849c37)

### v2.56.0 – Versionshinweise {#v2560-release-notes}

*Verbesserte Fortschrittsinformationen*

*Veröffentlicht am 21. Juli 2025*

**Fehlerbehebungen:**

- Problem beim gezielten Entfernen von Backups behoben, wenn das Repository keine Backups enthält. (*Geprüft von Stefan Fercot. Gemeldet von Anup Gupta.*)

  Das gezielte Entfernen von Backups schlug mit „cannot get index 0 from list with 0 value(s)“ fehl, wenn ein Repository keine Backups enthielt.

  Issue [#2645](https://github.com/pgbackrest/pgbackrest/issues/2645); Pull Request [#2646](https://github.com/pgbackrest/pgbackrest/pull/2646); Commit [`638815b`](https://github.com/pgbackrest/pgbackrest/commit/638815b4cde1ba1322516e256742c51676af66f0)

**Funktionen:**

- Wiederherstellungsfortschritt zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Denis Garsh, Maxim Michkov. Geprüft von David Steele.*)

  Der Befehl `restore` erfasst nun seinen Fortschritt, den `info` zusammen mit dem Backup-Fortschritt anzeigt. Eine Wiederherstellung wird außerdem nicht mehr durch `stop` beendet.

  Issue [#2546](https://github.com/pgbackrest/pgbackrest/issues/2546); Pull Request [#2652](https://github.com/pgbackrest/pgbackrest/pull/2652); Commit [`8cdd9ce`](https://github.com/pgbackrest/pgbackrest/commit/8cdd9ce1c4ab6cca508932a41a3013374d7547ef)
- Detailstufe für die Ausgabe des Befehls `info` hinzugefügt, die nur den Fortschritt anzeigt. (*Beigetragen von Denis Garsh. Geprüft von David Steele, Stefan Fercot.*)

  Mit `--detail-level=progress` wird nur der Fortschritt ausgegeben. Dies ist schneller, da das Repository nicht gelesen wird. Der Standardwert ist `full`.

  Pull Request [#2550](https://github.com/pgbackrest/pgbackrest/pull/2550); Commit [`2706168`](https://github.com/pgbackrest/pgbackrest/commit/2706168f609af544b0453d384c7fb620626fc205)

**Verbesserungen:**

- Fehlgeschlagene Lesevorgänge auf Objektspeichern wiederholt. (*Geprüft von David Christensen.*)

  Ein bereits begonnener Lesevorgang aus einem Objektspeicher wurde bei einem Fehler vollständig abgebrochen. Dadurch musste möglicherweise ein aufwendiger Auftrag neu gestartet werden, etwa bei einer Wiederherstellung. Ein fehlgeschlagener Lesevorgang wird nun an der Unterbrechungsstelle fortgesetzt.

  Pull Request [#2642](https://github.com/pgbackrest/pgbackrest/pull/2642); Commit [`5e14692`](https://github.com/pgbackrest/pgbackrest/commit/5e14692588b9fd8a566c9a1795c866ba2e83eebd)
- Standardwerte in der Befehlszeilenhilfe korrigiert. (*Geprüft von David Christensen, Chris Bandy.*)

  Hat eine Option mehrere Standardwerte, etwa `repo-storage-upload-chunk-size` bei einem S3- und einem Azure-Repository, zeigt die Optionsliste `<multi>` an, und die Hilfe zur Option führt jeden Standardwert auf. Für Optionen, die in der aktuellen Konfiguration ungültig sind, werden keine Standardwerte angezeigt.

  Pull Request [#2625](https://github.com/pgbackrest/pgbackrest/pull/2625); Commit [`8737cad`](https://github.com/pgbackrest/pgbackrest/commit/8737cad566974c37529595715ecdc06571420752)

**Verbesserungen der Dokumentation:**

- Diskrete Optionswerte gegebenenfalls als Liste beschrieben. (*Beigetragen von Anton Kurochkin. Geprüft von David Steele.*)

  Die Werte von Optionen wie `output` für die Befehle `verify` und `version` werden nun wie bei anderen Optionen als Liste beschrieben.

  Pull Request [#2638](https://github.com/pgbackrest/pgbackrest/pull/2638); Commit [`2e76e9f`](https://github.com/pgbackrest/pgbackrest/commit/2e76e9fc699d22286f6bf05fddc271d8fa22523e)
- "less than" in der Hilfeausgabe für die Option `archive-mode` korrigiert. (*Beigetragen von Anton Kurochkin. Geprüft von David Steele.*)

  Pull Request [#2633](https://github.com/pgbackrest/pgbackrest/pull/2633); Commit [`cb67322`](https://github.com/pgbackrest/pgbackrest/commit/cb673225e90604a8865ce30c188d15661f945e5e)

### v2.55.1 – Versionshinweise {#v2551-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 5. Mai 2025*

**Fehlerbehebungen:**

- Änderung „content-md5 auf S3 nur bei Bedarf berechnen“ zurückgenommen. (*Geprüft von David Christensen. Gemeldet von Frank Brendel.*)

  Bei aktiviertem Object Lock verlangt S3 für Uploads entweder `content-md5` oder eine `x-amz-content-*`-Prüfsumme. Da Scality die alternativen Prüfsummen nicht akzeptierte, schlugen Uploads fehl. `content-md5` wird nun wieder für alle Anfragen mit Inhalt berechnet.

  Issue [#2613](https://github.com/pgbackrest/pgbackrest/issues/2613); Pull Request [#2615](https://github.com/pgbackrest/pgbackrest/pull/2615); Commit [`8bbb982`](https://github.com/pgbackrest/pgbackrest/commit/8bbb98243566bfa052f6aacfd1bd3a6acd770e40)
- Prüfung der unteren Grenzen für Optionsschlüssel korrigiert. (*Geprüft von David Christensen, Wolfgang Walther. Gemeldet von Wolfgang Walther.*)

  Eine indizierte Option mit dem Schlüssel 0, etwa `pg0-path`, verursachte einen Segmentierungsfehler. Nun wird ein Fehler gemeldet.

  Issue [#2610](https://github.com/pgbackrest/pgbackrest/issues/2610); Pull Request [#2611](https://github.com/pgbackrest/pgbackrest/pull/2611); Commit [`5e01098`](https://github.com/pgbackrest/pgbackrest/commit/5e01098617a3803067b153be2d41e023cd4d95e4)

### v2.55.0 – Versionshinweise {#v2550-release-notes}

*Verbesserte Überprüfung und Unterstützung für PostgreSQL 18*

*Veröffentlicht am 21. April 2025*

**Fehlerbehebungen:**

- Problem bei der blockinkrementellen Wiederherstellung aus einem nicht als Standard verwendeten Repository behoben. (*Geprüft von David Christensen. Getestet von Aleksander Łukasz. Gemeldet von Aleksander Łukasz.*)

  Verwendete das wiederherzustellende Backup blockinkrementelle Daten und lag es nicht im Repository mit der niedrigsten Nummer, las die Wiederherstellung einen Teil dieser Daten aus dem Repository mit der niedrigsten Nummer. Durch Setzen von `repo` ließ sich das Problem umgehen.

  Issue [#2577](https://github.com/pgbackrest/pgbackrest/issues/2577); Pull Request [#2579](https://github.com/pgbackrest/pgbackrest/pull/2579); Commit [`5d2c67c`](https://github.com/pgbackrest/pgbackrest/commit/5d2c67c3c6975ea3ed08c7425f6e410ae378913f)
- `recovery_target_timeline=current` für PostgreSQL < 12 nicht gesetzt. (*Geprüft von Stefan Fercot.*)

  Vor PostgreSQL 12 verhält sich ein ausdrücklich auf `current` gesetztes `recovery_target_timeline` wie `latest`, obwohl `current` der Standard ist. Für diese Versionen wird die Einstellung nun aus `recovery.conf` weggelassen, wenn sie auf `current` gesetzt ist.

  Pull Request [#2533](https://github.com/pgbackrest/pgbackrest/pull/2533); Commit [`6fbb28f`](https://github.com/pgbackrest/pgbackrest/commit/6fbb28fa2d615576be78376c7f539921f6b8bc6a)
- Protokollierung des Archivbereichs beim Entfernen abgelaufener Daten korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Aleš Zelený.*)

  Nur der letzte entfernte Archivpfad wurde als Beginn des Bereichs protokolliert. Dadurch sah es im Protokoll so aus, als wären wesentlich weniger Dateien entfernt worden als tatsächlich.

  Issue [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Pull Request [#2554](https://github.com/pgbackrest/pgbackrest/pull/2554); Commit [`47f050f`](https://github.com/pgbackrest/pgbackrest/commit/47f050f8fd816e57326d881f4253d8a13c0f8da6)
- Fehlermeldungen für Abfragen ohne Ergebnisse korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Susantha Bathige.*)

  Ein Fehler einer Abfrage, die keine Ergebnisse liefern sollte, wurde als unerwartetes Ergebnis statt als eigentlicher Fehler gemeldet.

  Pull Request [#2539](https://github.com/pgbackrest/pgbackrest/pull/2539); Commit [`d5cefb7`](https://github.com/pgbackrest/pgbackrest/commit/d5cefb7290c34c64a2b9aa89ff04a718df4ec18b)

**Funktionen:**

- Ziel-Timeline der Recovery überprüft. (*Geprüft von Stefan Fercot.*)

  Ein Backup, das der Ziel-Timeline nicht folgen kann, etwa eines nach der Promotion eines Standbys und dem Abzweigen der neuen Timeline, scheiterte erst beim Start der Recovery mit einem schwer verständlichen PostgreSQL-Fehler. Die Timeline wird nun vor Beginn der Wiederherstellung anhand der Historiendateien geprüft.

  Pull Request [#2534](https://github.com/pgbackrest/pgbackrest/pull/2534); Commit [`922e9f0`](https://github.com/pgbackrest/pgbackrest/commit/922e9f0775c39b64e009251a6bec8ef9b83c190f)
- Überprüfung eines angegebenen Backups ermöglicht. (*Beigetragen von Maxim Michkov. Geprüft von David Steele.*)

  Die `verify`-Option `--set` prüft nur das angegebene Backup und das für dessen Konsistenz erforderliche WAL.

  Issue [#2419](https://github.com/pgbackrest/pgbackrest/issues/2419); Pull Request [#2544](https://github.com/pgbackrest/pgbackrest/pull/2544); Commit [`e4def88`](https://github.com/pgbackrest/pgbackrest/commit/e4def8845eb5c3fe9fb8cc44d9f64766cfb348c2)
- Unterstützung für S3/GCS mit Kostenübernahme durch den Anforderer hinzugefügt. (*Beigetragen von Timothée Peignier. Geprüft von David Steele.*)

  Setzen Sie `repo-s3-requester-pays` oder `repo-gcs-user-project`, um die Kosten dem Anfragenden statt dem Bucket-Eigentümer zuzurechnen. So kann beispielsweise ein Hostingdienst seinen Kunden Zugriff auf ihre Backups gewähren.

  [`4db0263`](https://github.com/pgbackrest/pgbackrest/commit/4db0263fd63274a8168eb4de17b320d2f86251a2) Unterstützung für S3 Requester Pays hinzufügen.; Pull Request [#2560](https://github.com/pgbackrest/pgbackrest/pull/2560)

  [`814bf48`](https://github.com/pgbackrest/pgbackrest/commit/814bf487c3955e877d226faaa22324d3c79863b2) Unterstützung für GCS Requester Pays hinzufügen.; Pull Request [#2557](https://github.com/pgbackrest/pgbackrest/pull/2557)
- Unterstützung für PostgreSQL 18. (*Geprüft von Stefan Fercot.*)

  Diese Version erschien vor der ersten Beta von PostgreSQL 18, sodass dessen Unterstützung zunächst experimentell war. Bis PostgreSQL 18.0 änderte sich nichts, was pgBackRest betrifft.

  Pull Request [#2603](https://github.com/pgbackrest/pgbackrest/pull/2603); Commit [`565d2e0`](https://github.com/pgbackrest/pgbackrest/commit/565d2e0c47cd21df890a40b3a94a8c865bed76d9)
- Verbindungen zu PostgreSQL über abstrakte Domain-Sockets ermöglicht. (*Getestet von Chris Bandy. Vorgeschlagen von Chris Bandy.*)

  `pg-socket-path` muss kein absoluter Pfad mehr sein und kann daher einen abstrakten Domain-Socket bezeichnen. libpq meldet einen ungültigen Pfad.

  Issue [#2529](https://github.com/pgbackrest/pgbackrest/issues/2529); Pull Request [#2535](https://github.com/pgbackrest/pgbackrest/pull/2535); Commit [`68f22ae`](https://github.com/pgbackrest/pgbackrest/commit/68f22aea6665b9dcbe76dbfaa731f37187e1ce20)
- Numerische Ausgabe zum Befehl `version` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Mit `--output=num` wird die Version als Zahl wie 2055000 ausgegeben, was Vergleiche erleichtert.

  Issue [#2410](https://github.com/pgbackrest/pgbackrest/issues/2410); Pull Request [#2526](https://github.com/pgbackrest/pgbackrest/pull/2526); Commit [`750a051`](https://github.com/pgbackrest/pgbackrest/commit/750a051b7aeccc3dd7ae9c07af2c73cb25057de9)

**Verbesserungen:**

- Ausführung des Backup-Befehls auf entfernten Repositorys ermöglicht. (*Geprüft von Stefan Fercot.*)

  Der Befehl `backup` kann nun auf einem Host mit entferntem Repository ausgeführt werden. Das erlaubt eine flexiblere Wahl des Hosts, auf dem Backups laufen.

  [`4a94b6b`](https://github.com/pgbackrest/pgbackrest/commit/4a94b6bef9108ab775c0070571a1fb7dd8883eeb) Protokollhelfer refaktorieren.

  [`931435c`](https://github.com/pgbackrest/pgbackrest/commit/931435c0177ded2189903385d520d5c8819c4f5e) Betrieb des Befehls backup mit entfernten Repositorys ermöglichen.; Pull Request [#2512](https://github.com/pgbackrest/pgbackrest/pull/2512)
- lz4 für die Protokollkomprimierung verwendet. (*Geprüft von Stefan Fercot.*)

  lz4 komprimiert deutlich schneller als gz und erreicht bei den niedrigen Stufen der Protokollkompression ähnliche Kompressionsraten. `compress-level-network=0` deaktiviert die Protokollkompression nicht mehr.

  [`0577b03`](https://github.com/pgbackrest/pgbackrest/commit/0577b0301689bc19d49c4081cc652971de5da8cf) lz4 für die Protokollkompression verwenden.; Pull Request [#2488](https://github.com/pgbackrest/pgbackrest/pull/2488)

  [`5c8296d`](https://github.com/pgbackrest/pgbackrest/commit/5c8296df066564be35d3936610ebff1c332f38da) Hinweis auf das Deaktivieren der Netzwerkkompression aus der Dokumentation entfernen.
- `content-md5` auf S3 nur bei Bedarf berechnet. (*Geprüft von David Christensen.*)

  Der Header `content-md5` wird nur für Batch-Löschanfragen berechnet, die ihn voraussetzen. Dies spart CPU-Zeit beim Hochladen von Dateien. Diese Änderung wurde in v2.55.1 zurückgenommen.

  Pull Request [#2592](https://github.com/pgbackrest/pgbackrest/pull/2592); Commit [`20bfd14`](https://github.com/pgbackrest/pgbackrest/commit/20bfd14b73ad6d75b6fb1169565b18dcfa183c9b)
- Warnung ausgegeben, wenn ein Wert einer Option mit mehreren Schlüsseln überschrieben wird. (*Geprüft von David Christensen, Stefan Fercot.*)

  Optionen mit Schlüssel-Wert-Paaren wie `recovery-option` überschrieben einen Wert stillschweigend, wenn sein Schlüssel erneut angegeben wurde. Nun wird eine Warnung protokolliert.

  Issue [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Pull Request [#2594](https://github.com/pgbackrest/pgbackrest/pull/2594); Commit [`cab4d6f`](https://github.com/pgbackrest/pgbackrest/commit/cab4d6fd5c775d6e1a9cd9889d825eee667b5322)
- Detaillierte Protokollierung beim Entfernen abgelaufener Archivpfade hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Das Entfernen vieler Archivdateien konnte wie ein Hängenbleiben wirken. Eine Meldung auf der Protokollstufe detail zeigt nun den Fortschritt.

  [`4dcfa9e`](https://github.com/pgbackrest/pgbackrest/commit/4dcfa9ef59c5e75c6c0ee83390c64b9a3d4af1fc) Detailprotokollierung zum expire-Test hinzufügen.

  [`2155a12`](https://github.com/pgbackrest/pgbackrest/commit/2155a12a3d861645de5618518350f90962fbc26d) Detailprotokollierung für entfernte Archivpfade hinzufügen.; Issue [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Pull Request [#2559](https://github.com/pgbackrest/pgbackrest/pull/2559)
- Unterstützung für PostgreSQL `9.4` entfernt. (*Geprüft von Stefan Fercot.*)

  PostgreSQL 9.4 wird entsprechend der Richtlinie, fünf PostgreSQL-Versionen nach ihrem Supportende zu unterstützen, nicht mehr unterstützt. Backups von 9.4-Clustern können weiterhin über die Ablaufbehandlung entfernt werden.

  Pull Request [#2472](https://github.com/pgbackrest/pgbackrest/pull/2472); Commit [`48f511d`](https://github.com/pgbackrest/pgbackrest/commit/48f511dad339ef9357e00f7bd8e2bf4b7c800dd4)
- Build mit autoconf/make entfernt. (*Geprüft von David Christensen.*)

  v2.54.0 war die letzte Version mit Unterstützung für den autoconf/make-Build. Verwenden Sie zum Kompilieren meson.

  Pull Request [#2470](https://github.com/pgbackrest/pgbackrest/pull/2470); Commit [`89c9bab`](https://github.com/pgbackrest/pgbackrest/commit/89c9baba72fc99616083a7adc4be2c3e2bf9e4dd)

**Verbesserungen der Dokumentation:**

- Dokumentation zur Angabe mehrerer Stanzas mit `tls-server-auth` korrigiert. (*Geprüft von David Christensen, Stefan Fercot. Vorgeschlagen von Terry MacAndrew.*)

  Mehrere Stanzas werden für `tls-server-auth` als durch Kommas getrennte Liste angegeben. Die Dokumentation hatte dazu aufgefordert, die Option zu wiederholen.

  Issue [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Pull Request [#2595](https://github.com/pgbackrest/pgbackrest/pull/2595); Commit [`53a45d2`](https://github.com/pgbackrest/pgbackrest/commit/53a45d25c3e60e5067010b2676f5d6216638fbe3)
- Entfernen abgelaufener inkrementeller Backups erläutert. (*Geprüft von Stefan Fercot.*)

  Die Dokumentation erweckte den Eindruck, inkrementelle Backups würden anhand einer Anzahl entfernt. Nun erklärt sie deren Ablaufbehandlung und dass vollständige Backups bei der differenziellen Aufbewahrung als differenzielle Backups mitzählen.

  Pull Request [#2601](https://github.com/pgbackrest/pgbackrest/pull/2601); Commit [`8bdba74`](https://github.com/pgbackrest/pgbackrest/commit/8bdba747981e8805a9bf355050f70cdf19e9babc)
- Anforderung erläutert, dass die lokale und entfernte pgBackRest-Version übereinstimmen müssen. (*Beigetragen von Greg Clough. Geprüft von David Steele.*)

  Issue [#2540](https://github.com/pgbackrest/pgbackrest/issues/2540); Pull Request [#2541](https://github.com/pgbackrest/pgbackrest/pull/2541); Commit [`82299eb`](https://github.com/pgbackrest/pgbackrest/commit/82299eb4cd997524eeddef170ad99669ed6651cf)
- FAQ zum Export eines eigenständigen Clusters hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Die FAQ erklärt, wie aus einem mit `--archive-copy` erstellten und mit `--type=none` wiederhergestellten Backup ein eigenständiger Export eines Clusters erzeugt wird.

  Pull Request [#2605](https://github.com/pgbackrest/pgbackrest/pull/2605); Commit [`9386920`](https://github.com/pgbackrest/pgbackrest/commit/9386920b79971347c6c57589190bf09b591d8b4d)
- Einschränkung von `--tablespace-map-all` bei der Erstellung von Tablespaces erläutert. (*Geprüft von Stefan Fercot, Christophe Courtois. Vorgeschlagen von Christophe Courtois.*)

  Ein nach Beginn des Backups erstellter Tablespace steht nicht im Manifest und kann daher nicht durch `tablespace-map-all` umgeordnet werden.

  Pull Request [#2538](https://github.com/pgbackrest/pgbackrest/pull/2538); Commit [`e625ed8`](https://github.com/pgbackrest/pgbackrest/commit/e625ed8be2228cb99c3801f9d1776909a2201c5a)
- Verhalten von `--repo-retention-full-type` erläutert. (*Geprüft von Antoine Beaupré. Vorgeschlagen von Antoine Beaupré.*)

  Issue [#2562](https://github.com/pgbackrest/pgbackrest/issues/2562); Pull Request [#2583](https://github.com/pgbackrest/pgbackrest/pull/2583); Commit [`84eb9a7`](https://github.com/pgbackrest/pgbackrest/commit/84eb9a742dcf75f071e011946263dedaa985099e)
- Empfehlung für Objektspeicher von `--process-max` auf `--repo-bundle` geändert. (*Geprüft von Stefan Fercot.*)

  Bei Objektspeichern verringert `repo-bundle` die für die Dateierstellung benötigte Zeit wesentlich stärker als `process-max`, da weniger Dateien angelegt werden.

  Pull Request [#2542](https://github.com/pgbackrest/pgbackrest/pull/2542); Commit [`aa7210a`](https://github.com/pgbackrest/pgbackrest/commit/aa7210a1830825e0a3e6b6740937357341127a6f)
- `unix_socket_directory` durch `unix_socket_directories` ersetzt. (*Beigetragen von hyunkyu han. Geprüft von David Steele.*)

  `unix_socket_directory` ist seit PostgreSQL 9.2 nicht mehr gültig. Daher wird nur `unix_socket_directories` dokumentiert.

  Issue [#2589](https://github.com/pgbackrest/pgbackrest/issues/2589); Commit [`b28ae98`](https://github.com/pgbackrest/pgbackrest/commit/b28ae98cec7ae7e881e6476c1cba1ba7e1abc358)
- Empfohlen, `spool-path` nicht innerhalb von `pg_xlog`/`pg_wal` abzulegen. (*Geprüft von Martín Marqués, Don Seiler. Vorgeschlagen von Martín Marqués.*)

  Ein Spool-Pfad innerhalb von `pg_xlog` oder `pg_wal` kann bei PostgreSQL-Werkzeugen wie `pg_rewind` Probleme verursachen.

  Pull Request [#2600](https://github.com/pgbackrest/pgbackrest/pull/2600); Commit [`dd3a7d9`](https://github.com/pgbackrest/pgbackrest/commit/dd3a7d99a78d0d604967d90e8a8dbf8915432896)

### v2.54.2 – Versionshinweise {#v2542-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 20. Januar 2025*

**Fehlerbehebungen:**

- Problem nach dem Deaktivieren der Bündelung bei aktivierter blockinkrementeller Verarbeitung behoben. (*Geprüft von David Christensen.*)

  Wurde das Bündeln deaktiviert, nachdem Backups mit Bündelung und blockinkrementeller Verarbeitung erstellt worden waren, ließen sich die vorherigen Backups nicht mehr lesen. Die dafür erforderliche Einstellung wird nun beibehalten.

  Pull Request [#2511](https://github.com/pgbackrest/pgbackrest/pull/2511); Commit [`dbc6f28`](https://github.com/pgbackrest/pgbackrest/commit/dbc6f2875356ec16cf4883830a0d7b00204752ee)

**Verbesserungen der Dokumentation:**

- Verhalten bei mehreren Konfigurationsdateien erläutert. (*Geprüft von Paul Bierly. Vorgeschlagen von Paul Bierly.*)

  Jede Konfigurationsdatei muss für sich gültig sein. Deshalb muss jeder Abschnitt in jeder Datei angegeben werden, die darin eine Option setzt. Die Dokumentation weist außerdem darauf hin, dass Anführungszeichen nicht unterstützt werden, umgebende Leerzeichen bei Schlüsseln und Werten entfernt und mehrfach angegebene Abschnitte zusammengeführt werden.

  Commit [`5da2df4`](https://github.com/pgbackrest/pgbackrest/commit/5da2df4a933f04d5fb9a3b6c7c59529f3afa805b)

### v2.54.1 – Versionshinweise {#v2541-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 16. Dezember 2024*

**Fehlerbehebungen:**

- Problem behoben, bei dem die Befehle `version`/`help` versuchten, `pgbackrest.conf` zu laden. (*Geprüft von Stefan Fercot. Gemeldet von Bradford Boyle, Julian.*)

  In v2.54.0 luden die Befehle `version` und `help` die Datei `pgbackrest.conf` und schlugen fehl, wenn sie nicht gelesen oder ausgewertet werden konnte.

  Issue [#2476](https://github.com/pgbackrest/pgbackrest/issues/2476); Pull Request [#2477](https://github.com/pgbackrest/pgbackrest/pull/2477); Commit [`8d69118`](https://github.com/pgbackrest/pgbackrest/commit/8d6911898afd75c586ef70c6d8559b1e5959a155)

**Verbesserungen der Testsuite:**

- Asynchrone Archivierung in Integrationstests stabilisiert. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)

  Ein von einem Integrationstest zurückgelassenes asynchrones `archive-get` konnte einen Fehler in die Warteschlange des nächsten Tests schreiben und dessen Recovery fehlschlagen lassen.

  Issue [#2463](https://github.com/pgbackrest/pgbackrest/issues/2463); Pull Request [#2481](https://github.com/pgbackrest/pgbackrest/pull/2481); Commit [`b90ce9e`](https://github.com/pgbackrest/pgbackrest/commit/b90ce9eb8c7cd9e9b131477a377249a3d3fda181)

### v2.54.0 – Versionshinweise {#v2540-release-notes}

*Zielzeitpunkt für versionierten Speicher*

*Veröffentlicht am 21. Oktober 2024*

**HINWEIS FÜR PAKETBETREUER**: Dies ist die letzte Version mit neuen Funktionen, die den Build mit autoconf/make unterstützt. Bitte wechseln Sie zu meson, falls noch nicht geschehen. Patch-Versionen von 2.54.X werden, sofern es welche gibt, weiterhin autoconf/make unterstützen.

**Fehlerbehebungen:**

- Leistungsproblem bei PostgreSQL-Abfragen mit großen Datenmengen behoben. (*Behoben von Thibault Vincent, David Steele. Geprüft von David Christensen. Getestet von Antoine Millet. Gemeldet von Antoine Millet.*)

  Die Logik für Abfragezeitüberschreitungen verzögerte das Lesen der Ergebnisse. Dadurch konnte eine Abfrage mit großer Ergebnismenge bis zu `db-timeout` dauern. Ergebnisse werden nun gelesen, sobald sie verfügbar sind.

  [`6ac4e8d`](https://github.com/pgbackrest/pgbackrest/commit/6ac4e8dd78f16e93300f7747c4bc8fa8e1a0558b) Testersatz des fd-Moduls in den Test des io-Moduls verschieben.

  [`77ae753`](https://github.com/pgbackrest/pgbackrest/commit/77ae753ef59bd40b9867be21e8519093786c3b85) Einmalige Ausführung des fdReady()-Testersatzes mit einem festgelegten Rückgabewert erlauben.

  [`33fa396`](https://github.com/pgbackrest/pgbackrest/commit/33fa3965616b1432e5d1d59c489302fa4891a39e) Wait-Objekt refaktorieren, um die verbleibende Wartezeit über waitRemains() bereitzustellen.

  [`c8ccaaa`](https://github.com/pgbackrest/pgbackrest/commit/c8ccaaa755993e3fd5e87148bd0a991acb3050c3) Leistung von PostgreSQL-Abfragen für große Datenmengen verbessern.; Issue [#2458](https://github.com/pgbackrest/pgbackrest/issues/2458); Pull Request [#2459](https://github.com/pgbackrest/pgbackrest/pull/2459)

**Funktionen:**

- Lesen von Repositorys auf versioniertem Speicher zu einem Zielzeitpunkt ermöglicht. (*Geprüft von Stefan Fercot, David Christensen.*)

  Die Befehle `archive-get`, `info`, `repo-get`, `repo-ls`, `restore` und `verify` können ein Repository auf versioniertem Azure-, GCS- oder S3-Speicher in seinem Zustand zu `repo-target-time` lesen. Das ermöglicht eine Wiederherstellung auch dann, wenn das Repository versehentlich oder absichtlich gelöscht oder beschädigt wurde.

  Pull Request [#2404](https://github.com/pgbackrest/pgbackrest/pull/2404); Commit [`b19134d`](https://github.com/pgbackrest/pgbackrest/commit/b19134dccd5d0dab87b5d45b443f481df00370b1)
- Angefordertes Backup vom Standby auch ohne verfügbaren Standby ermöglicht. (*Geprüft von Stefan Fercot.*)

  Mit `backup-standby=prefer` wird von einem Standby gesichert, sofern einer verfügbar ist, andernfalls vom Primärserver. Dies hilft nicht, wenn der Standby zwar antwortet, sich nach Beginn des Backups aber nicht mit dem Primärserver synchronisieren kann.

  Pull Request [#2378](https://github.com/pgbackrest/pgbackrest/pull/2378); Commit [`a42629f`](https://github.com/pgbackrest/pgbackrest/commit/a42629f87ab70ffaee8d1241eb50c5ea7154a87d)

**Verbesserungen:**

- Liste der Backup-Referenzen für die Textausgabe des Befehls `info` zusammengefasst. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Die Liste der Backup-Referenzen kann sehr lang sein. Die Textausgabe von `info` fasst sie daher nun zusammen. Mit `--set` wird die vollständige Liste angezeigt.

  Pull Request [#2399](https://github.com/pgbackrest/pgbackrest/pull/2399); Commit [`b306f83`](https://github.com/pgbackrest/pgbackrest/commit/b306f83493cc859ad15c8f175fc6db2321b79340)
- web-id-Token bei jeder S3-Authentifizierung erneuert. (*Beigetragen von Brent Graveland. Geprüft von David Steele.*)

  Die durch `AWS_WEB_IDENTITY_TOKEN_FILE` bezeichnete Tokendatei wurde nur einmal beim Start gelesen. Bei einem langen Vorgang konnte das Token daher ablaufen. Nun wird es bei jeder Authentifizierung gelesen.

  Issue [#2428](https://github.com/pgbackrest/pgbackrest/issues/2428); Pull Request [#2429](https://github.com/pgbackrest/pgbackrest/pull/2429); Commit [`95a4b9e`](https://github.com/pgbackrest/pgbackrest/commit/95a4b9e10a3f7a26ebaae22fc6abd79cee14189a)
- Aktuelle Werte indizierter Optionen in der Hilfe korrekt angezeigt. (*Geprüft von David Christensen.*)

  Der angezeigte aktuelle Wert einer indizierten Option war immer der Wert des ersten Index, etwa `pg1-path`. Die Hilfe zur Option führt nun den Wert jedes Index auf. Bei mehreren Werten zeigt die Optionsliste `<multi>` an.

  Pull Request [#2453](https://github.com/pgbackrest/pgbackrest/pull/2453); Commit [`b3ca2e3`](https://github.com/pgbackrest/pgbackrest/commit/b3ca2e34823b28862d999f87c4d7346707952a5b)
- `backup.info` nur bei geändertem Inhalt gespeichert. (*Geprüft von Stefan Fercot.*)

  `expire` speicherte `backup.info` auch dann, wenn sich die Datei nicht geändert hatte. Weniger Speichervorgänge erleichtern zudem die Wahl eines Zielzeitpunkts auf versioniertem Speicher.

  Pull Request [#2403](https://github.com/pgbackrest/pgbackrest/pull/2403); Commit [`b454b9e`](https://github.com/pgbackrest/pgbackrest/commit/b454b9e403526b1f352df964d9206c27d2397df3)
- Einschränkung beim parallelen Lesen von Dateien während der Wiederherstellung entfernt. (*Geprüft von David Christensen.*)

  Das Protokoll konnte auf einem entfernten Host jeweils nur eine Datei lesen oder schreiben. Eine Wiederherstellung las daher die Dateien einzeln aus dem Repository. Protokollbefehle können nun multiplexiert werden, sodass mehrere Dateien gleichzeitig gelesen werden können, beispielsweise ein Bündel und die blockinkrementellen Daten einer darin enthaltenen Datei.

  [`df8cbc9`](https://github.com/pgbackrest/pgbackrest/commit/df8cbc91c348bc2f746767c87ac5626460fb6f39) Protokollbefehle multiplexieren.; Pull Request [#2108](https://github.com/pgbackrest/pgbackrest/pull/2108)

  [`46c1297`](https://github.com/pgbackrest/pgbackrest/commit/46c1297be344909e900be596a865064233da9f87) Beschränkung beim parallelen Lesen von Dateien während der Wiederherstellung entfernen.; Pull Request [#2436](https://github.com/pgbackrest/pgbackrest/pull/2436)
- SFTP-Fehlermeldungen verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  SFTP-Fehler wurden bisher nur als Nummern gemeldet. Nun enthalten sie auch eine Fehlerbeschreibung.

  Pull Request [#2439](https://github.com/pgbackrest/pgbackrest/pull/2439); Commit [`70bda2c`](https://github.com/pgbackrest/pgbackrest/commit/70bda2cfb21130eb589a87cb419fb5f22a71c78a)

**Neue Inhalte der Dokumentation:**

- Abschnitt zur Leistungsoptimierung zum Benutzerhandbuch hinzugefügt. (*Geprüft von Stefan Fercot.*)

  Optionen zur üblichen Leistungsverbesserung waren über die Dokumentation verstreut. Die Schnellstartanleitung enthält nun einen Abschnitt, der sie auflistet.

  Pull Request [#2446](https://github.com/pgbackrest/pgbackrest/pull/2446); Commit [`278319e`](https://github.com/pgbackrest/pgbackrest/commit/278319eba3444070123d3f0f277be9234604d937)

**Verbesserungen der Dokumentation:**

- Quelle für `data_directory` erläutert. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Matthias.*)

  `pg-path` sollte dem von PostgreSQL gemeldeten `data_directory` entsprechen. Dieser Wert kann von dem in `postgresql.conf` abweichen.

  Issue [#2464](https://github.com/pgbackrest/pgbackrest/issues/2464); Pull Request [#2467](https://github.com/pgbackrest/pgbackrest/pull/2467); Commit [`9ba2db0`](https://github.com/pgbackrest/pgbackrest/commit/9ba2db017348d304f96ce89592fc01f29197e136)
- Logik verbessert, die entscheidet, wann eine Zusammenfassung kleingeschrieben werden sollte. (*Vorgeschlagen von Daniel Westermann.*)

  Zusammenfassungen, die mit einem Eigennamen oder Akronym wie PostgreSQL beginnen, werden in der Dokumentation nicht mehr kleingeschrieben.

  Issue [#2462](https://github.com/pgbackrest/pgbackrest/issues/2462); Commit [`eb2f279`](https://github.com/pgbackrest/pgbackrest/commit/eb2f279a2998d1ed893c5d8984590ab4997a5f32)

### v2.53.1 – Versionshinweise {#v2531-release-notes}

*Unterstützung für PostgreSQL 17*

*Veröffentlicht am 19. August 2024*

**Fehlerbehebungen:**

- Berechtigungen bei der Ausführung von `restore` als root korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Will M.*)

  Wurde `restore` als root ausgeführt, gehörte `pg_control` anschließend root. Eine Wiederherstellung als root schlug außerdem fehl, wenn der Basispfad nicht existierte.

  Issue [#2407](https://github.com/pgbackrest/pgbackrest/issues/2407); Pull Request [#2416](https://github.com/pgbackrest/pgbackrest/pull/2416); Commit [`7bd8da4`](https://github.com/pgbackrest/pgbackrest/commit/7bd8da4eecb0ce1461854414b727606a5e884edf)
- Segfault bei verzögerten Verbindungsfehlern behoben. (*Geprüft von David Christensen. Gemeldet von Anton Glushakov.*)

  Ein Verbindungsfehler, der erst bei einem späteren Wartevorgang gemeldet wurde, konnte einen Segmentierungsfehler verursachen.

  Issue [#2420](https://github.com/pgbackrest/pgbackrest/issues/2420); Pull Request [#2422](https://github.com/pgbackrest/pgbackrest/pull/2422); Commit [`377ba06`](https://github.com/pgbackrest/pgbackrest/commit/377ba062ac81867dca6197265688deb0111ae81a)
- Prüfung auf doppelte lokale Repositorys für SFTP übersprungen. (*Behoben von Reid Thompson. Geprüft von David Steele. Gemeldet von Anton Kurochkin.*)

  Die Prüfung auf mehrfach konfigurierte lokale Repositorys wurde auch auf SFTP-Repositorys angewendet, die niemals lokal sind.

  Issue [#2418](https://github.com/pgbackrest/pgbackrest/issues/2418); Pull Request [#2421](https://github.com/pgbackrest/pgbackrest/pull/2421); Commit [`9840304`](https://github.com/pgbackrest/pgbackrest/commit/98403046ed6af4c54fa2f572ecf9c211f94b67db)

**Verbesserungen:**

- Unterstützung für PostgreSQL 17.

  PostgreSQL 17beta3 änderte die Control- und WAL-Formate, was für eine Beta ungewöhnlich ist.

  Commit [`189d15d`](https://github.com/pgbackrest/pgbackrest/commit/189d15d1a640e31aac5ffbbd0fb06eb9eed8b576)

### v2.53 – Versionshinweise {#v253-release-notes}

*Gleichzeitige Backups*

*Veröffentlicht am 22. Juli 2024*

**WICHTIGER HINWEIS**: Der Standardwert der Option `log-level-stderr` wurde von `warn` auf `off` geändert. Dies erleichtert das Erfassen von Fehlern, wenn nur `stdout` umgeleitet wird. Um das bisherige Verhalten beizubehalten, setzen Sie `log-level-stderr=warn`.<br/> <br/> **HINWEIS FÜR PAKETBETREUER**: Der meson-Build benötigt nun die lz4-Bibliothek.<br/> <br/> **HINWEIS FÜR PAKETBETREUER**: Der meson-Build benötigt nun Compiler-Unterstützung für `__builtin_clzl()` und `__builtin_bswap64()`.

**Fehlerbehebungen:**

- Fehler beim Umbenennen über SFTP behoben, wenn die Datei bereits existiert. (*Behoben von Reid Thompson. Geprüft von David Steele. Gemeldet von ahmed112212.*)

  Einige SFTP-Server melden eine bereits vorhandene Datei mit einem bisher unbehandelten Fehler. Dadurch schlug das Umbenennen einer Datei über eine bestehende Datei fehl.

  Issue [#2376](https://github.com/pgbackrest/pgbackrest/issues/2376); Pull Request [#2377](https://github.com/pgbackrest/pgbackrest/pull/2377); Commit [`d6f0bf8`](https://github.com/pgbackrest/pgbackrest/commit/d6f0bf88af8b39492aa8e20c09bdf30260e2eb2f)

**Funktionen:**

- Gleichzeitige Backups auf unterschiedlichen Repositorys ermöglicht. (*Geprüft von Reid Thompson, Stefan Fercot.*)

  Backups derselben Stanza können nun gleichzeitig auf verschiedenen Repositorys laufen, da Sperren jetzt je Stanza und Repository statt nur je Stanza gelten. Dies ist mit PostgreSQL <= 9.5 nicht möglich.

  [`270dce4`](https://github.com/pgbackrest/pgbackrest/commit/270dce41b6fff0d0ad0769b0ea5df0011140f0b9) Sperrmodul refaktorieren.; Pull Request [#2371](https://github.com/pgbackrest/pgbackrest/pull/2371)

  [`cfb8aa2`](https://github.com/pgbackrest/pgbackrest/commit/cfb8aa202ee972579697db2cc8d5d8ef111f0022) In 31c7824a fehlende entfernte Sperren für Stanza-Befehle ergänzen.

  [`edd6163`](https://github.com/pgbackrest/pgbackrest/commit/edd61636a98d193b7c0634b5a4444527132959e0) Gleichzeitige Backups auf verschiedenen Repositorys ermöglichen.; Pull Request [#2389](https://github.com/pgbackrest/pgbackrest/pull/2389)
- Unterstützung für IP-basierte SANs bei der Validierung von TLS-Zertifikaten. (*Beigetragen von David Christensen. Geprüft von David Steele.*)

  Zertifikate mit einer IP-Adresse als Subject Alternative Name, etwa `IP:1.2.3.4`, werden nun geprüft. IPv4- und IPv6-Adressen müssen exakt übereinstimmen.

  Issue [#1977](https://github.com/pgbackrest/pgbackrest/issues/1977); Pull Request [#2047](https://github.com/pgbackrest/pgbackrest/pull/2047); Commit [`dfb620b`](https://github.com/pgbackrest/pgbackrest/commit/dfb620b0b8cf884ca486b413f4cd162e258b2fc5)

**Verbesserungen:**

- Standardwert der Option `log-level-stderr` auf `off` gesetzt. (*Geprüft von Greg Sabino Mullane, Stefan Fercot.*)

  Warnungen und Fehler auf stderr gingen häufig verloren, wenn zum Sammeln der Protokolle nur stdout umgeleitet wurde. Ein ausdrücklich gesetztes `log-level-stderr` ist nicht betroffen.

  Pull Request [#2379](https://github.com/pgbackrest/pgbackrest/pull/2379); Commit [`7d54073`](https://github.com/pgbackrest/pgbackrest/commit/7d540730941994d3cb630c695e9f672e047d8e7f)
- Alternative WAL-Segmentgrößen für PostgreSQL ≤ 10 ermöglicht. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)

  PostgreSQL <= 10 kann mit einer anderen WAL-Segmentgröße kompiliert werden. Abspaltungen wie Greenplum legen sie mit `initdb` fest.

  Pull Request [#2303](https://github.com/pgbackrest/pgbackrest/pull/2303); Commit [`4ac3b82`](https://github.com/pgbackrest/pgbackrest/commit/4ac3b82c99ff3bd48d2cc74651a47ce072ac0022)
- Hinweis zur Prüfung des SFTP-Autorisierungsprotokolls hinzugefügt. (*Beigetragen von Vitalii Zurian. Geprüft von Reid Thompson, David Steele.*)

  Bei fehlgeschlagener SFTP-Authentifizierung weist der Fehler nun darauf hin, dass das Autorisierungsprotokoll des Servers weitere Details enthalten kann.

  Issue [#2381](https://github.com/pgbackrest/pgbackrest/issues/2381); Pull Request [#2385](https://github.com/pgbackrest/pgbackrest/pull/2385); Commit [`ccae609`](https://github.com/pgbackrest/pgbackrest/commit/ccae60940241b30e8bc3e405936b6ba68857930c)
- Standardwerte und zulässige Werte von Zeitoptionen mit passenden Einheiten anzeigen.

  Standardwerte und zulässige Werte von Zeitoptionen wurden in Sekunden angezeigt, was bei großen Werten schwer lesbar war. Sekundenbruchteile sind nicht mehr zulässig. Ein Wert wie `archive-timeout=0.5` muss daher als `archive-timeout=500ms` geschrieben werden.

  Commit [`3a2266f`](https://github.com/pgbackrest/pgbackrest/commit/3a2266f327c340ff1133a6a2398429c844b5755d)
- OpenSSL >= 1.1.1 voraussetzen.

  Commit [`cf8625d`](https://github.com/pgbackrest/pgbackrest/commit/cf8625d24bd953ad1ed448c32b937584009e5b6b)

**Verbesserungen der Dokumentation:**

- Verhalten von `archive-push` bei mehreren Repositorys erläutert. (*Geprüft von Stefan Fercot.*)

  Fällt ein Repository aus, kann `archive-push` nur bei aktiviertem `archive-async` mit der Übertragung an andere Repositorys fortfahren.

  Pull Request [#2398](https://github.com/pgbackrest/pgbackrest/pull/2398); Commit [`ec3e387`](https://github.com/pgbackrest/pgbackrest/commit/ec3e387bb73826c30b32bf0221acb2d56f23f1c5)

### v2.52.1 – Versionshinweise {#v2521-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 25. Juni 2024*

**Fehlerbehebungen:**

- Problem bei Dateien behoben, die auf dem Replikat größer sind als auf dem Primärserver. (*Geprüft von Stefan Fercot. Gemeldet von Nicolas Lassimonne.*)

  Hatte eine Datei bei einem blockinkrementellen Backup vom Standby auf Primärserver und Standby unterschiedliche Größen, speicherte das nächste differenzielle oder inkrementelle Backup die Größe vom Primärserver. Das darauf folgende Backup schlug mit „repo size must be > 0“ fehl.

  [`83aaa86`](https://github.com/pgbackrest/pgbackrest/commit/83aaa868ef396348bf96589457f13c1805b25cb6) Unit-Tests für blockinkrementelle Backups vom Standby hinzufügen.

  [`aabc122`](https://github.com/pgbackrest/pgbackrest/commit/aabc122021a582e9d0193f978cf710cff95c2bee) Problem mit Dateien beheben, die auf dem Replikat größer sind als auf dem Primärserver.; Issue [#2358](https://github.com/pgbackrest/pgbackrest/issues/2358); Pull Request [#2367](https://github.com/pgbackrest/pgbackrest/pull/2367)

### v2.52 – Versionshinweise {#v252-release-notes}

*Unterstützung für PostgreSQL 17beta1*

*Veröffentlicht am 27. Mai 2024*

**HINWEIS FÜR PAKETBETREUER**: Das Build-System von pgBackRest ist nun meson. Der Build mit autoconf/make erhält keine neuen Funktionen mehr und wird nach einigen Versionen entfernt.

**Funktionen:**

- Unterstützung für GCS-Stapellöschung hinzugefügt. (*Geprüft von Reid Thompson.*)

  Dateien werden mit Batch-Anfragen statt mit einer Anfrage je Datei entfernt. Dies beschleunigt `expire` und andere Befehle, die Dateien aus dem Repository löschen.

  Pull Request [#2326](https://github.com/pgbackrest/pgbackrest/pull/2326); Commit [`76bcb74`](https://github.com/pgbackrest/pgbackrest/commit/76bcb740b66f64804dbbf5a2a6be6407f9cec376)
- Unterstützung für S3-Verschlüsselung mit `SSE-C`. (*Geprüft von Tim Jones. Vorgeschlagen von Tim Jones.*)

  Mit `repo-s3-sse-customer-key` verschlüsselt S3 die Daten nach der Übertragung mit dem angegebenen Schlüssel. Dies ist weniger sicher als die Verschlüsselung vor der Übertragung mit `repo-cipher-type`.

  Issue [#2279](https://github.com/pgbackrest/pgbackrest/issues/2279); Pull Request [#2282](https://github.com/pgbackrest/pgbackrest/pull/2282); Commit [`57731b6`](https://github.com/pgbackrest/pgbackrest/commit/57731b6cd261c732041aacc094429ab02ca13418)
- Unterstützung für PostgreSQL 17beta1. (*Geprüft von Stefan Fercot.*)

  Katalogversion und magische WAL-Zahl für PostgreSQL 17 hinzugefügt.

  Pull Request [#2328](https://github.com/pgbackrest/pgbackrest/pull/2328); Commit [`fb22f04`](https://github.com/pgbackrest/pgbackrest/commit/fb22f04555fecfa143354372ec3543ab186c131d)

**Verbesserungen:**

- Explizites Deaktivieren optionaler Abhängigkeiten bei meson-Builds ermöglicht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)

  Eine optionale Funktion kann im meson-Build deaktiviert werden, auch wenn ihre Bibliothek installiert ist. Dies benötigen manche Plattformen wie FreeBSD. Standardmäßig wird eine Funktion aktiviert, wenn ihre Bibliothek gefunden wird.

  Pull Request [#2321](https://github.com/pgbackrest/pgbackrest/pull/2321); Commit [`7b95fd3`](https://github.com/pgbackrest/pgbackrest/commit/7b95fd3bd29346e7325aa161bfee45efd71e22eb)
- python beim meson-Build dynamisch gesucht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)

  Der meson-Build findet nun die Python-Installation, statt eine Binärdatei `python3` im Suchpfad vorauszusetzen, etwa wenn nur `python3.9` installiert ist. Die minimale meson-Version ist nun 0.47.

  [`55e9969`](https://github.com/pgbackrest/pgbackrest/commit/55e996912aa57d39ea21f5dc905b7acabe93b0f8) Minimale meson-Version auf 0.47 anheben.

  [`e00e33b`](https://github.com/pgbackrest/pgbackrest/commit/e00e33b52856a63e82552ccc12df235d1a7f6f17) Python im meson-Build dynamisch finden.; Pull Request [#2338](https://github.com/pgbackrest/pgbackrest/pull/2338)
- Build-Ziel `pgbackrest` in meson als installierbar gekennzeichnet. (*Beigetragen von Bradford Boyle. Geprüft von David Steele.*)

  Pull Request [#2312](https://github.com/pgbackrest/pgbackrest/pull/2312); Commit [`7877983`](https://github.com/pgbackrest/pgbackrest/commit/7877983acb3b1a27e900f7e7aea89cb7b29a817d)

**Verbesserungen der Dokumentation:**

- Dokumentation zu `start`/`stop` an die tatsächliche Funktionalität angepasst. (*Geprüft von Stefan Fercot.*)

  Issue [#2325](https://github.com/pgbackrest/pgbackrest/issues/2325); Issue [#2334](https://github.com/pgbackrest/pgbackrest/issues/2334); Pull Request [#2352](https://github.com/pgbackrest/pgbackrest/pull/2352); Commit [`b6ac11b`](https://github.com/pgbackrest/pgbackrest/commit/b6ac11beec920fe978994c0d018c380477199ca8)

### v2.51 – Versionshinweise {#v251-release-notes}

*Build-System Meson*

*Veröffentlicht am 25. März 2024*

**Fehlerbehebungen:**

- Dateien mit der Länge null bei blockinkrementellen Delta-Wiederherstellungen übersprungen. (*Geprüft von Sebastian Krause, René Højbjerg Larsen. Gemeldet von Sebastian Krause.*)

  Eine vorhandene leere Datei ließ eine blockinkrementelle Delta-Wiederherstellung im Blockprüfsummenfilter fehlschlagen. Diese Dateien werden nun übersprungen, da sie keine wiederverwendbaren Daten enthalten.

  Issue [#2271](https://github.com/pgbackrest/pgbackrest/issues/2271); Pull Request [#2272](https://github.com/pgbackrest/pgbackrest/pull/2272); Commit [`f7a7ab1`](https://github.com/pgbackrest/pgbackrest/commit/f7a7ab16c9652179945717ebf9b68af3aa8a0b0e)
- Leistungsregression beim Auflisten des Speichers behoben. (*Geprüft von Stephen Frost. Gemeldet von Maksym Boguk.*)

  Beim Auflisten eines Pfads wurden detaillierte Informationen zu jeder Datei angefordert. Das konnte insbesondere bei Objektspeichern langsam sein. Nun werden nur die für die Liste benötigten Informationen angefordert.

  Issue [#2275](https://github.com/pgbackrest/pgbackrest/issues/2275); Pull Request [#2276](https://github.com/pgbackrest/pgbackrest/pull/2276); Commit [`e00bfe2`](https://github.com/pgbackrest/pgbackrest/commit/e00bfe2d2c3f124b2883e3c2d169a2ce506a1e98)
- Fortschrittsprotokollierung korrigiert, wenn sich die Dateigröße während des Backups ändert. (*Geprüft von Stephen Frost. Gemeldet von samkingno.*)

  Issue [#2298](https://github.com/pgbackrest/pgbackrest/issues/2298); Pull Request [#2304](https://github.com/pgbackrest/pgbackrest/pull/2304); Commit [`76956e7`](https://github.com/pgbackrest/pgbackrest/commit/76956e71cfa3044867213bd65a6f22e96120c108)

**Verbesserungen:**

- Unterstützung für Dual-Stack-Verbindungen verbessert. (*Geprüft von Stephen Frost. Vorgeschlagen von Timothée Peignier.*)

  Wird ein Hostname in mehrere Adressen aufgelöst, etwa IPv4 und IPv6, wird die nächste Adresse versucht, sobald der vorherigen ausreichend Zeit zum Verbindungsaufbau eingeräumt wurde. Dies folgt dem „Happy Eyeballs“-Ansatz aus RFC 8305. Ein Verbindungsversuch, der weder scheitert noch eine Verbindung herstellt, verbraucht nicht mehr die gesamte verfügbare Zeit.

  Issue [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Pull Request [#2235](https://github.com/pgbackrest/pgbackrest/pull/2235); Commit [`7448fde`](https://github.com/pgbackrest/pgbackrest/commit/7448fde157c6d22f57b90c0cef11957b0aadf4b3)
- meson zum primären Build-System gemacht. (*Geprüft von Stephen Frost.*)

  meson ist nun das Buildsystem für Tests und Dokumentationsbuilds. Funktionen, die außerhalb ihres Moduls nicht verwendet werden, werden verborgen. Das verkleinert die Binärdatei.

  [`e3d9df3`](https://github.com/pgbackrest/pgbackrest/commit/e3d9df3ae9669ee5749b970d59f8afeb20fd3d9d) meson zum primären Buildsystem machen.; Pull Request [#2264](https://github.com/pgbackrest/pgbackrest/pull/2264)

  [`f287178`](https://github.com/pgbackrest/pgbackrest/commit/f287178b705cc90aa887d66c932e2a223029649b) Sichtbarkeit von Funktionen und Variablen auf hidden setzen.; Pull Request [#2265](https://github.com/pgbackrest/pgbackrest/pull/2265)
- Unveränderte Dateien bei inkrementellen Backups ohne Delta erkannt. (*Geprüft von Stephen Frost.*)

  Bei einem differenziellen oder inkrementellen Backup ohne Delta wird eine Datei, die in einen einzigen Puffer passt, sowie jede blockinkrementelle Datei mit der Datei im vorherigen Backup verglichen. Ist sie unverändert, wird sie referenziert statt gespeichert.

  Pull Request [#2257](https://github.com/pgbackrest/pgbackrest/pull/2257); Commit [`9d91d1b`](https://github.com/pgbackrest/pgbackrest/commit/9d91d1b2f817b543fc8d970af56d1442c325ed7c)
- Ungültige Recovery bei entferntem `backup_label` verhindert. (*Geprüft von Stephen Frost.*)

  Wird `backup_label` aus einem wiederhergestellten Cluster entfernt, verwendet PostgreSQL den Checkpoint aus `pg_control` für die Crash-Recovery. Dies beschädigt den Cluster fast immer. Die Wiederherstellung macht den Checkpoint in `pg_control` nun ungültig, sodass die Recovery stattdessen fehlschlägt. `pg_controldata` zeigt den Checkpoint als `0/DEAD` an.

  Pull Request [#2232](https://github.com/pgbackrest/pgbackrest/pull/2232); Commit [`e634fd8`](https://github.com/pgbackrest/pgbackrest/commit/e634fd85cedc1ae3aef7c4fa2556d7d73d05cb8a)
- Verarbeitung der WAL-Segmentwarteschlange von `archive-push` verbessert. (*Geprüft von Stephen Frost.*)

  Zum Messen der Warteschlange wurde die Größe jedes WAL-Segments darin gelesen. Nun wird die Größe des ersten Segments für alle verwendet.

  Pull Request [#2277](https://github.com/pgbackrest/pgbackrest/pull/2277); Commit [`cf17515`](https://github.com/pgbackrest/pgbackrest/commit/cf17515e409440eecfb04bf7186790d8baa8ab12)
- Fortsetzen von Backups auf vollständige Backups beschränkt. (*Geprüft von Stephen Frost, Stefan Fercot.*)

  Die Fortsetzung funktionierte bei differenziellen und inkrementellen Delta-Backups nicht richtig. Zudem ändert sich eine seit dem vorherigen Backup geänderte Datei wahrscheinlich vor einer Fortsetzung erneut. Deshalb werden nun nur vollständige Backups fortgesetzt.

  Pull Request [#2268](https://github.com/pgbackrest/pgbackrest/pull/2268); Commit [`dddcbcd`](https://github.com/pgbackrest/pgbackrest/commit/dddcbcd8e9a1cae578b0cc5bb2d1aa768330f3c5)
- Fortsetzungsfunktion für blockinkrementelle Backups aktualisiert. (*Geprüft von Stephen Frost.*)

  Beim Fortsetzen wurden blockinkrementelle Dateien entfernt. Es funktionierte zwar, kopierte aber alle diese Dateien erneut. Blockinkrementelle Dateien bleiben beim Fortsetzen nun erhalten.

  Pull Request [#2296](https://github.com/pgbackrest/pgbackrest/pull/2296); Commit [`ff47450`](https://github.com/pgbackrest/pgbackrest/commit/ff47450402fde5ebc64a08d31791551bee52200e)
- `--version` und `--help` für Version und Hilfe zugelassen. (*Geprüft von Greg Sabino Mullane. Vorgeschlagen von Greg Sabino Mullane.*)

  `--version` und `--help` funktionieren nun wie bei den meisten Programmen. Mit `help` erhalten Sie Hilfe zu einem bestimmten Befehl oder einer Option.

  Pull Request [#2263](https://github.com/pgbackrest/pgbackrest/pull/2263); Commit [`68db307`](https://github.com/pgbackrest/pgbackrest/commit/68db3075d7ac4a48377967ad54e45b95b9ee6c61)
- Detaillierten Backtrace zum Build mit autoconf/make hinzugefügt. (*Geprüft von Stephen Frost.*)

  Fehler-Stacktraces im autoconf/make-Build enthalten nun Details aus libbacktrace. Leistungstests zeigten dafür keinen merklichen Aufwand.

  Pull Request [#1970](https://github.com/pgbackrest/pgbackrest/pull/1970); Commit [`676700d`](https://github.com/pgbackrest/pgbackrest/commit/676700d8ca6f2e0e0ab8123aa9606c8ec7aa81ae)

**Verbesserungen der Dokumentation:**

- Verweise auf `recovery.conf` aktualisiert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Stephen Frost.*)

  Verweise auf `recovery.conf` schließen nun `postgresql.auto.conf` ein, das neuere PostgreSQL-Versionen verwenden.

  Pull Request [#2281](https://github.com/pgbackrest/pgbackrest/pull/2281); Commit [`6835178`](https://github.com/pgbackrest/pgbackrest/commit/68351785f6816a23526900db595557cf6e3a0056)

### v2.50 – Versionshinweise {#v250-release-notes}

*Leistungsverbesserungen und Fehlerbehebungen*

*Veröffentlicht am 22. Januar 2024*

**Fehlerbehebungen:**

- Unvollständigen Lesevorgang bei blockinkrementellen Wiederherstellungen korrigiert. (*Geprüft von Stephen Frost. Getestet von Brent Graveland. Gemeldet von Adol Rodriguez, Brent Graveland.*)

  Ein komprimierter Superblock kann mit Bytes enden, die für die Dekomprimierung nicht benötigt werden, aber das Datenende markieren. Abhängig von der Lage des Puffers relativ zu den Daten wurden diese Bytes nicht gelesen und die Wiederherstellung schlug fehl.

  Issue [#2215](https://github.com/pgbackrest/pgbackrest/issues/2215); Issue [#2238](https://github.com/pgbackrest/pgbackrest/issues/2238); Pull Request [#2256](https://github.com/pgbackrest/pgbackrest/pull/2256); Commit [`f4a4af2`](https://github.com/pgbackrest/pgbackrest/commit/f4a4af299bee93ab7dde599ccdb35becc1c2afad)
- Überlauf behoben, der den Backup-Fortschritt in der Ausgabe von `info` unterdrückte. (*Behoben von Robert Donovan. Geprüft von Joe Wildish.*)

  Die Größen in der Sperrdatei wurden als 32-Bit-Werte gelesen. Deshalb zeigte `info` bei Backups über 4GiB keinen Fortschritt an.

  Issue [#2251](https://github.com/pgbackrest/pgbackrest/issues/2251); Pull Request [#2252](https://github.com/pgbackrest/pgbackrest/pull/2252); Commit [`25f1489`](https://github.com/pgbackrest/pgbackrest/commit/25f14898babf4ad78baef3e8343933a863633975)

**Verbesserungen:**

- Unvollständige Dateien bei blockinkrementellen Delta-Wiederherstellungen beibehalten. (*Geprüft von Stephen Frost.*)

  Eine kleinere als erwartete Datei wurde bei einer blockinkrementellen Delta-Wiederherstellung nicht behalten, obwohl ihre Blöcke wiederverwendbar sind, etwa beim Wiederholen einer fehlgeschlagenen Wiederherstellung oder beim Wiederherstellen über eine kleinere Datei.

  Pull Request [#2254](https://github.com/pgbackrest/pgbackrest/pull/2254); Commit [`a42614e`](https://github.com/pgbackrest/pgbackrest/commit/a42614e8f3a9e6871c16331f01c2cd765ab181aa)
- Unterstützung für alternative, beim Kompilieren festgelegte Seitengrößen hinzugefügt. (*Beigetragen von Viktor Kurilko. Geprüft von David Steele.*)

  PostgreSQL kann mit einer anderen Seitengröße wie 4096 kompiliert werden. Abspaltungen wie Greenplum nutzen dies.

  Pull Request [#2197](https://github.com/pgbackrest/pgbackrest/pull/2197); Commit [`89d5278`](https://github.com/pgbackrest/pgbackrest/commit/89d5278b74ab0d880345575d7ac4c239cd1fce54)
- Beim Bündeln Dateien übersprungen, die während des Backups gekürzt wurden. (*Beigetragen von Georgy Shelkovy. Geprüft von David Steele.*)

  Eine Datei, die nach der Zuordnung zu Bündeln auf null gekürzt wurde, blieb in ihrem Bündel gespeichert. In einem Debug-Build schlug dabei eine Assertion fehl. Solche Dateien werden nun übersprungen.

  [`02eea55`](https://github.com/pgbackrest/pgbackrest/commit/02eea555c7169e99892fdbc8ce7cc1ee59f50509) Beim Bündeln während des Backups gekürzte Dateien überspringen.; Pull Request [#2227](https://github.com/pgbackrest/pgbackrest/pull/2227)

  [`c879509`](https://github.com/pgbackrest/pgbackrest/commit/c8795094d418802a0e24d4d19da66973c71b00e5) Rückgabe von const-Prüfsummenpuffern aus backupFile() erlauben.

  [`9049fec`](https://github.com/pgbackrest/pgbackrest/commit/9049fec2c02c4110e16ffdff7b56f83d8ff32b4a) Überspringen gekürzter Dateien beim Bündeln während des Backups refaktorieren.

  Entwicklung in [v2.49](#v249-release-notes):

  [`337da35`](https://github.com/pgbackrest/pgbackrest/commit/337da35ab278e058ec4cdffeb4319f1a1e2cb0df) Test zum Verhalten gebündelter Dateien hinzufügen, die während des Backups gekürzt werden.
- Fehlermeldungen des SFTP-Speichers verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Pull Request [#2249](https://github.com/pgbackrest/pgbackrest/pull/2249); Commit [`7c17eec`](https://github.com/pgbackrest/pgbackrest/commit/7c17eec3db455d3e8e660f4f8247b6975517648f)

### v2.49 – Versionshinweise {#v249-release-notes}

*Unterstützung für PostgreSQL 9.3 entfernt*

*Veröffentlicht am 27. November 2023*

**Fehlerbehebungen:**

- Regression bei Wiederholungsversuchen behoben. (*Geprüft von Stephen Frost. Gemeldet von Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)

  v2.48 entfernte die Wiederholung, die erfolgte, wenn ein Vorgang sein gesamtes Zeitlimit verbrauchte. Eine Zeitüberschreitung wurde dadurch zum Fehler, etwa beim Warten darauf, dass ein Socket zu einem Objektspeicher beschreibbar wird. Nun erfolgen auch nach Ablauf des Zeitlimits noch zwei Wiederholungen.

  [`3c116e1`](https://github.com/pgbackrest/pgbackrest/commit/3c116e1829a0df62aaf50ce241c63d829eb438e0) Ungenutzten Header entfernen.

  [`fa5b2d4`](https://github.com/pgbackrest/pgbackrest/commit/fa5b2d44ad9f7591517eecaaaaeb07e9500dd51c) Regression bei Wiederholungsversuchen beheben.; Issue [#2200](https://github.com/pgbackrest/pgbackrest/issues/2200); Issue [#2214](https://github.com/pgbackrest/pgbackrest/issues/2214); Pull Request [#2221](https://github.com/pgbackrest/pgbackrest/pull/2221)
- Rekursives Entfernen von Pfaden im SFTP-Speichertreiber korrigiert. (*Behoben von Reid Thompson. Geprüft von Stephen Frost. Gemeldet von Luc.*)

  Einige SFTP-Server melden beim Löschen eines Verzeichnisses wie einer Datei eine verweigerte Berechtigung statt eines allgemeinen Fehlers. Auf diesen Servern schlug dadurch das rekursive Entfernen eines Pfads fehl.

  Issue [#2219](https://github.com/pgbackrest/pgbackrest/issues/2219); Pull Request [#2226](https://github.com/pgbackrest/pgbackrest/pull/2226); Commit [`c4dc466`](https://github.com/pgbackrest/pgbackrest/commit/c4dc4665f88e9d67a3b66f44cd59d6dd4bb5107f)

**Verbesserungen:**

- Unterstützung für PostgreSQL `9.3` entfernt. (*Geprüft von Stephen Frost.*)

  PostgreSQL 9.3 wird entsprechend der Richtlinie, fünf PostgreSQL-Versionen nach ihrem Supportende zu unterstützen, nicht mehr unterstützt.

  Pull Request [#2220](https://github.com/pgbackrest/pgbackrest/pull/2220); Commit [`dcf0781`](https://github.com/pgbackrest/pgbackrest/commit/dcf078198761a2cfe9be6b4c7f4b4fb07ef53cbf)

**Neue Inhalte der Dokumentation:**

- Optionen für Projektbetreuer dokumentiert. (*Geprüft von Stefan Fercot.*)

  Maintainer-Optionen werden nun in einem eigenen Abschnitt einschließlich der Einschränkungen ihrer Verwendung dokumentiert. `pg-version-force` ist nicht mehr intern.

  Pull Request [#2202](https://github.com/pgbackrest/pgbackrest/pull/2202); Commit [`21c8c8a`](https://github.com/pgbackrest/pgbackrest/commit/21c8c8a66cb06eba714bfa41bed7239af3d14f08)
- Dokumentation zur Point-in-Time-Recovery für PostgreSQL >= 13 aktualisiert.

  Seit PostgreSQL 13 schlägt die Recovery fehl, wenn das Wiederherstellungsziel nicht erreicht wird. Der Abschnitt zur zeitpunktbezogenen Wiederherstellung funktioniert nun sowohl für PostgreSQL 13 und neuer als auch für ältere Versionen.

  Commit [`eb69e2e`](https://github.com/pgbackrest/pgbackrest/commit/eb69e2ee6339047f0145b751437ac2bec82bb5ab)

**Verbesserungen der Testsuite:**

- Ausführung des Unittests `config/load` ohne installiertes `libssh2` ermöglicht. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Wu Ning.*)

  Issue [#2193](https://github.com/pgbackrest/pgbackrest/issues/2193); Pull Request [#2194](https://github.com/pgbackrest/pgbackrest/pull/2194); Commit [`e2b734e`](https://github.com/pgbackrest/pgbackrest/commit/e2b734eff97e3fac32895b799cc32126013aae27)

### v2.48 – Versionshinweise {#v248-release-notes}

*Tags für den Repository-Speicher*

*Veröffentlicht am 25. September 2023*

**Fehlerbehebungen:**

- Problem bei der blockinkrementellen Wiederherstellung ohne Blockliste behoben. (*Geprüft von Stephen Frost. Getestet von Burak Yurdakul. Gemeldet von Burak Yurdakul.*)

  Eine Blockzuordnung ohne Blöcke wird geschrieben, wenn sich der Zeitstempel einer Datei ohne Änderung ihres Inhalts ändert. Sie wurde nicht entschlüsselt, wenn sie innerhalb desselben Bündel-Lesevorgangs auf eine ohne blockinkrementelle Verarbeitung gespeicherte Datei folgte. Bei genügend betroffenen Dateien wurden alle Wiederholungen aufgebraucht und die Wiederherstellung schlug fehl.

  Issue [#2182](https://github.com/pgbackrest/pgbackrest/issues/2182); Pull Request [#2184](https://github.com/pgbackrest/pgbackrest/pull/2184); Commit [`31de127`](https://github.com/pgbackrest/pgbackrest/commit/31de127cf42438b1fac04c161c47264aa1fb1060)

**Funktionen:**

- Option `--repo-storage-tag` zum Erstellen von Objekt-Tags hinzugefügt. (*Geprüft von Stephen Frost, Stefan Fercot, Timothée Peignier.*)

  Mit `repo-storage-tag` werden Objekte beim Schreiben in ein S3-, GCS- oder Azure-Repository mit Tags versehen. Die Tags werden je Repository gesetzt.

  Issue [#2150](https://github.com/pgbackrest/pgbackrest/issues/2150); Pull Request [#2159](https://github.com/pgbackrest/pgbackrest/pull/2159); Commit [`1b4e0cc`](https://github.com/pgbackrest/pgbackrest/commit/1b4e0cce5f3ff5ea3ee0b889e6d4ce4de1430b04)
- Prüfung bekannter Hosts zum SFTP-Speichertreiber hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von Stephen Frost, David Steele.*)

  SFTP-Hostschlüssel werden nun standardmäßig anhand der Known-Hosts-Dateien geprüft, also mit `repo-sftp-host-key-check-type=strict`. Mit `repo-sftp-host-key-check-type=accept-new` werden neue Hosts automatisch hinzugefügt; `repo-sftp-host-key-check-type=none` überspringt die Prüfung wie bisher.

  Pull Request [#2125](https://github.com/pgbackrest/pgbackrest/pull/2125); Commit [`ce9ba0f`](https://github.com/pgbackrest/pgbackrest/commit/ce9ba0fadee652d409488bee701ea6a51cafec75)
- Unterstützung für Dual-Stack-Verbindungen. (*Geprüft von Stephen Frost.*)

  Alle Adressen, in die ein Hostname aufgelöst wird, werden nun nacheinander versucht, beispielsweise eine IPv6-Adresse ohne Route zum Host und anschließend eine IPv4-Adresse. Dies geschieht bis zum Verbindungsaufbau oder zum Ablauf des Zeitlimits. Wiederholte Fehler werden in Fehlermeldungen außerdem zusammengefasst.

  [`5314dbf`](https://github.com/pgbackrest/pgbackrest/commit/5314dbffc761bc7507db02693f2421c1578efe10) Genauigkeit des Wait-Objekts bei Verschachtelung verbessern.

  [`c180513`](https://github.com/pgbackrest/pgbackrest/commit/c1805134b370f0c5c54c40a2df8978599328784f) Wiederholte Fehler in der ErrorRetry-Ausgabe zusammenfassen.

  [`edbd520`](https://github.com/pgbackrest/pgbackrest/commit/edbd520c81f5d437963aaf42d1c79b2c51d01665) Adresslistenabfrage refaktorieren, um alle zurückgegebenen Adressen einzubeziehen.; Pull Request [#2174](https://github.com/pgbackrest/pgbackrest/pull/2174)

  [`39bb8a0`](https://github.com/pgbackrest/pgbackrest/commit/39bb8a0d3a96eef63219dff262a9306a4f59dae9) Unterstützung für Dual-Stack-Verbindungen.; Issue [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Pull Request [#2175](https://github.com/pgbackrest/pgbackrest/pull/2175)
- Bereits verarbeitete und gesamte Backup-Größe zur JSON-Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Die JSON-Ausgabe von `info` enthält nun die bereits verarbeitete und die gesamte Größe eines laufenden Backups, damit andere Programme den Fortschritt überwachen können.

  Issue [#2007](https://github.com/pgbackrest/pgbackrest/issues/2007); Pull Request [#2141](https://github.com/pgbackrest/pgbackrest/pull/2141); Commit [`e3fcd8c`](https://github.com/pgbackrest/pgbackrest/commit/e3fcd8cd9e0be42a32fc4cbd2ae3db2c072eabcd)

**Verbesserungen:**

- check-Befehl für mehrere Stanzas. (*Geprüft von Stephen Frost.*)

  Ohne Angabe von `stanza` prüft `check` nun alle Stanzas in der Konfiguration.

  Pull Request [#2057](https://github.com/pgbackrest/pgbackrest/pull/2057); Commit [`1141dc2`](https://github.com/pgbackrest/pgbackrest/commit/1141dc20708cf0c68296f83e74c872a7db9c2bd9)
- Lesen von `pg_control` wiederholt, bis die Prüfsumme gültig ist. (*Geprüft von Stefan Fercot, Stephen Frost.*)

  Auf manchen Dateisystemen wie ext4 kann das Lesen von `pg_control` während eines gleichzeitigen Schreibvorgangs inkonsistente Teildaten liefern. Der Lesevorgang wird nun wiederholt, bis die Prüfsumme gültig ist.

  Pull Request [#2131](https://github.com/pgbackrest/pgbackrest/pull/2131); Commit [`f42d927`](https://github.com/pgbackrest/pgbackrest/commit/f42d927d2dcd58cf5a80d68eaf6888bcf2c67a4b)
- Prüfung der WAL-Segmente nach erfolgreichem Backup optimiert. (*Geprüft von Stephen Frost.*)

  Die Prüfung der WAL-Segmente nach einem Backup listete den Speicher einmal je Segment auf. Nun wird jedes WAL-Verzeichnis einmal aufgelistet und die Liste wiederverwendet.

  Pull Request [#2169](https://github.com/pgbackrest/pgbackrest/pull/2169); Commit [`9d3a605`](https://github.com/pgbackrest/pgbackrest/commit/9d3a605900644059ff0e030d71a818b3965eb031)
- Leistung mehrteiliger Übertragungen bei GCS verbessert. (*Geprüft von Reid Thompson.*)

  Teile eines mehrteiligen Uploads werden nun übertragen, sobald sie verfügbar sind.

  Pull Request [#2162](https://github.com/pgbackrest/pgbackrest/pull/2162); Commit [`6cb9c40`](https://github.com/pgbackrest/pgbackrest/commit/6cb9c40fb8ea18e6572bf3f6e44bbb1d8f922682)
- Ausführung des Befehls `archive-get` bei gestoppter Stanza ermöglicht. (*Geprüft von Tom Swartz, David Christensen, Reid Thompson.*)

  Da `archive-get` nicht in das Repository schreibt, kann der Befehl nun wie `restore` bei gestoppter Stanza ausgeführt werden.

  Commit [`fbd992a`](https://github.com/pgbackrest/pgbackrest/commit/fbd992adc7b18db5e70774d675c160c8c8e2f031)
- Führende Tilde in Pfaden für öffentliche/private SFTP-Schlüssel akzeptiert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Pfade für `repo-sftp-private-key-file` und `repo-sftp-public-key-file` dürfen nun wie dokumentiert mit `~` beginnen.

  Pull Request [#2136](https://github.com/pgbackrest/pgbackrest/pull/2136); Commit [`eb32d6d`](https://github.com/pgbackrest/pgbackrest/commit/eb32d6de5e1575a37efb166abbf7df400d93352e)
- GCS-Zugangsdaten vor der Erneuerung des Authentifizierungstokens neu geladen. (*Geprüft von Stephen Frost. Vorgeschlagen von Daniel Farina.*)

  Die Dienstschlüsseldatei wird nun vor dem Erneuern des Authentifizierungstokens erneut gelesen. Der Schlüssel kann dadurch während eines laufenden Befehls ersetzt werden.

  Pull Request [#2072](https://github.com/pgbackrest/pgbackrest/pull/2072); Commit [`995a8e9`](https://github.com/pgbackrest/pgbackrest/commit/995a8e96691d23eaf3914a425669f89deb3ce002)

**Fehlerbehebungen in der Dokumentation:**

- Beispiel für die Option `tls-server-address` in der Konfigurationsreferenz korrigiert. (*Behoben von Hartmut Goebel. Geprüft von David Steele.*)

  Das Beispiel `::*` war ungültig. Verwenden Sie `*` für IPv4 oder `::` für IPv6.

  Pull Request [#2165](https://github.com/pgbackrest/pgbackrest/pull/2165); Commit [`43524a4`](https://github.com/pgbackrest/pgbackrest/commit/43524a47a4c6a847f76514812f94b87cb7af4c05)
- Beispiel für die Option `filter` in der Befehlsreferenz korrigiert.

  Commit [`cb3ff6e`](https://github.com/pgbackrest/pgbackrest/commit/cb3ff6ed4336af9e4c0643d8224d5bc3d790a655)

**Verbesserungen der Testsuite:**

- Ausführung des Unittests `storage/sftp` ohne installiertes `libssh2` ermöglicht. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Wu Ning.*)

  Issue [#2163](https://github.com/pgbackrest/pgbackrest/issues/2163); Pull Request [#2177](https://github.com/pgbackrest/pgbackrest/pull/2177); Commit [`c3c0834`](https://github.com/pgbackrest/pgbackrest/commit/c3c0834e170196a1241a368779162fcca65f9ad5)

### v2.47 – Versionshinweise {#v247-release-notes}

*Leistungsverbesserungen und Fehlerbehebungen*

*Veröffentlicht am 24. Juli 2023*

**Fehlerbehebungen:**

- Blockinkrementelle Informationen im Manifest während eines Delta-Backups beibehalten. (*Geprüft von Stephen Frost. Gemeldet von Francisco Miguel Biete Banon.*)

  Änderte sich eine Datei so, dass sie als neue Datei nicht mehr blockinkrementell verarbeitet würde, etwa weil sie unter die Größenuntergrenze schrumpfte oder ihr Zeitstempel weit genug in die Vergangenheit rückte, gingen ihre blockinkrementellen Informationen im Manifest eines Delta-Backups verloren. Dies geschah auch dann, wenn weiterhin auf die Datei im vorherigen Backup verwiesen werden konnte.

  [`1d42aed`](https://github.com/pgbackrest/pgbackrest/commit/1d42aed152563fff6ec70c517d86eb39158b3f20) Prüfung referenzierter Dateien im Unit-Test command/backup verbessern.

  [`4c27d74`](https://github.com/pgbackrest/pgbackrest/commit/4c27d74bbd3a44d8ab1af140277d3cd8302060c2) Blockinkrementelle Informationen im Manifest während eines Delta-Backups erhalten.; Issue [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Pull Request [#2123](https://github.com/pgbackrest/pgbackrest/pull/2123)
- Blockinkrementelle Dateinamen im Befehl `verify` korrigiert. (*Geprüft von Reid Thompson. Gemeldet von Francisco Miguel Biete Banon.*)

  Für blockinkrementelle Dateien außerhalb eines Bündels verwendete `verify` die Komprimierungserweiterung statt `.pgbi` und konnte sie deshalb nicht finden.

  Issue [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Pull Request [#2120](https://github.com/pgbackrest/pgbackrest/pull/2120); Commit [`cdb7e26`](https://github.com/pgbackrest/pgbackrest/commit/cdb7e26350822b55c00771d6d575242b1202e741)
- Unbegründetes automatisches Delta-Backup beim Backup vom Standby behoben. (*Geprüft von Stephen Frost. Gemeldet von krmozejko, Don Seiler.*)

  Dateigrößen auf dem Standby können von denen auf dem Primärserver abweichen, etwa bei Free Space Maps. Das nächste inkrementelle Backup konnte dadurch eine Größenänderung auf dem Primärserver erkennen und auf einen deutlich langsameren Prüfsummen-Delta-Vergleich wechseln. Die ursprüngliche Größe wird nun im Manifest gespeichert und für den Vergleich verwendet.

  Issue [#2020](https://github.com/pgbackrest/pgbackrest/issues/2020); Pull Request [#2124](https://github.com/pgbackrest/pgbackrest/pull/2124); Commit [`5ed6f8d`](https://github.com/pgbackrest/pgbackrest/commit/5ed6f8df1487174985c42d6e13c367d70c2d8b8a)
- `recovery.signal` für PostgreSQL >= 12 bei Recovery mit `type=none` übersprungen. (*Geprüft von Stefan Fercot. Gemeldet von T.Anastacio.*)

  Bei `type=none` wird für PostgreSQL >= 12 keine Datei `recovery.signal` mehr geschrieben. Dies entspricht dem Verhalten älterer Versionen.

  Issue [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Pull Request [#2070](https://github.com/pgbackrest/pgbackrest/pull/2070); Commit [`9cceed6`](https://github.com/pgbackrest/pgbackrest/commit/9cceed6ac4a32c14a797eba89a4ad1dc06d89d80)
- Erzeugung eindeutiger Kennzeichnungen für differenzielle/inkrementelle Backups korrigiert. (*Behoben von Andrey Sokolov. Geprüft von David Steele.*)

  Gab es mindestens zwei vollständige Backups und war das neueste entfernt worden, schlug ein differenzielles oder inkrementelles Backup wie bei einer zurückgestellten Uhr fehl. Seine Kennzeichnung wurde mit der des entfernten vollständigen Backups verglichen.

  Issue [#1873](https://github.com/pgbackrest/pgbackrest/issues/1873); Pull Request [#2104](https://github.com/pgbackrest/pgbackrest/pull/2104); Commit [`0ac0934`](https://github.com/pgbackrest/pgbackrest/commit/0ac09344dc17fb54e250705ce49399b86329bb3d)
- Zeitbasiertes Entfernen abgelaufener Archivdaten korrigiert, wenn keine Backups abgelaufen sind. (*Geprüft von Stefan Fercot.*)

  War die zeitbasierte Aufbewahrungsfrist erfüllt, ohne dass Backups entfernt wurden, wurde auch kein Archiv entfernt. Stattdessen wurde „time-based archive retention not met“ protokolliert. Es war dann ein weiteres Backup nötig, um das ältere WAL zu entfernen.

  Issue [#2103](https://github.com/pgbackrest/pgbackrest/issues/2103); Pull Request [#2109](https://github.com/pgbackrest/pgbackrest/pull/2109); Commit [`762498f`](https://github.com/pgbackrest/pgbackrest/commit/762498f4cd5f1425db4c176fc707926d62cc7c04)

**Verbesserungen:**

- Leistung des SFTP-Speichertreibers verbessert. (*Beigetragen von Stephen Frost, Reid Thompson. Geprüft von David Steele.*)

  Der SFTP-Speichertreiber wartete eine feste Zeit, wenn libssh2 nicht fortfahren konnte. Nun wartet er, bis der Socket lesbar oder beschreibbar ist.

  [`e280ed9`](https://github.com/pgbackrest/pgbackrest/commit/e280ed9098a6f5da9bdabb541e9c69d4f24ffcf2) Behandlung von Ergebniscodes in storage/sftp vereinheitlichen.

  [`125676a`](https://github.com/pgbackrest/pgbackrest/commit/125676ae0e98d3730d2dc0d47e37ca1df145d044) Initialisierung und Handshake in storageSftpNew() bereinigen.

  [`28b6b2d`](https://github.com/pgbackrest/pgbackrest/commit/28b6b2d4659d78ce67c1bd3104d96e5705d955c9) Leistung des SFTP-Speichertreibers verbessern.; Pull Request [#2089](https://github.com/pgbackrest/pgbackrest/pull/2089)
- Zeitzonenversatz zur Datums-/Zeitausgabe des Befehls `info` hinzugefügt. (*Geprüft von Stefan Fercot, Philip Hurst. Vorgeschlagen von Philip Hurst.*)

  Zeitstempel in der Ausgabe von `info` enthalten nun den Zeitzonenoffset. Sie können dadurch direkt als Wiederherstellungsziel verwendet werden, etwa mit `--target`.

  [`9efd5cd`](https://github.com/pgbackrest/pgbackrest/commit/9efd5cd0bb40c5dc2fcac2e21c9b62e554b94db6) Zeitzonenoffset zur Datums- und Zeitausgabe von info hinzufügen.; Issue [#2093](https://github.com/pgbackrest/pgbackrest/issues/2093); Pull Request [#2095](https://github.com/pgbackrest/pgbackrest/pull/2095)

  [`aa229a1`](https://github.com/pgbackrest/pgbackrest/commit/aa229a1deef3afeebb66db1443b19e24559adf96) time_t-Umwandlungen anhand der Coverity-Meldungen anpassen.
- Fehlerbehandlung für nicht unterstützte Funktionen zentralisiert. (*Geprüft von Stefan Fercot.*)

  Fehler zu nicht einkompilierten Funktionen wie lz4 sind nun ausführlicher und einheitlicher. Die Angabe von SFTP-Speicher ohne einkompilierte SFTP-Unterstützung führt nicht mehr zu einer fehlgeschlagenen Assertion.

  [`de46276`](https://github.com/pgbackrest/pgbackrest/commit/de46276bf60b8a2181621b123d1a99e56808a089) Verarbeitung der Liste zulässiger Werte im Modul config/parse refaktorieren.

  [`36ff81d`](https://github.com/pgbackrest/pgbackrest/commit/36ff81dc6ff7e98e40c0c05a4a343a71b91b1678) Fehlerbehandlung für nicht unterstützte Funktionen zentralisieren.; Pull Request [#2075](https://github.com/pgbackrest/pgbackrest/pull/2075)

**Verbesserungen der Dokumentation:**

- Im Benutzerhandbuch klargestellt, dass die Installation aus Paketen bevorzugt wird. (*Geprüft von Stefan Fercot. Vorgeschlagen von dr-kd.*)

  Pull Request [#2090](https://github.com/pgbackrest/pgbackrest/pull/2090); Commit [`a36f480`](https://github.com/pgbackrest/pgbackrest/commit/a36f480c85c7add6fdf0e5517748d740e3a7b424)

### v2.46 – Versionshinweise {#v246-release-notes}

*Blockinkrementelles Backup und SFTP-Speicher*

*Veröffentlicht am 22. Mai 2023*

**Funktionen:**

- Blockinkrementelles Backup. (*Geprüft von John Morris, Stephen Frost, Stefan Fercot.*)

  Die blockinkrementelle Verarbeitung speichert nur die seit dem vorherigen Backup geänderten Teile einer Datei. Das spart bei differenziellen und inkrementellen Backups großer Dateien Platz und Zeit. Aktivieren Sie sie mit `repo-block`, das `repo-bundle` voraussetzt.

  [`dd4e526`](https://github.com/pgbackrest/pgbackrest/commit/dd4e52679ecdc43539bd038b5aa9bd4ff9055cbf) Aufteilung in Chunks und Blocknummern aus der inkrementellen Blockliste entfernen.; Pull Request [#2029](https://github.com/pgbackrest/pgbackrest/pull/2029)

  [`822f2a5`](https://github.com/pgbackrest/pgbackrest/commit/822f2a584260a012b833455a7a2bd1c8487e3010) Blockinkrementelle Funktion fertigstellen.; Pull Request [#2053](https://github.com/pgbackrest/pgbackrest/pull/2053)
- SFTP-Unterstützung für Repository-Speicher. (*Beigetragen von Reid Thompson. Geprüft von Stephen Frost, David Steele.*)

  Mit `repo-type=sftp` und `repo-sftp-host` wird das Repository auf einem SFTP-Server gespeichert.

  Pull Request [#1959](https://github.com/pgbackrest/pgbackrest/pull/1959); Commit [`87087fa`](https://github.com/pgbackrest/pgbackrest/commit/87087fac231d2110160b3219daee3f9fb91aec02)

  Entwicklung in [v2.42](#v242-release-notes):

  [`01b81f9`](https://github.com/pgbackrest/pgbackrest/commit/01b81f9d374701eb489dd1888bcba25fb5d6df84) Link-Erstellung in die Speicherschnittstelle verschieben.; Pull Request [#1879](https://github.com/pgbackrest/pgbackrest/pull/1879)
- Unterstützung für PostgreSQL 16. (*Geprüft von Stefan Fercot.*)

  Katalogversion und magische WAL-Zahl für PostgreSQL 16 hinzugefügt.

  Pull Request [#2051](https://github.com/pgbackrest/pgbackrest/pull/2051); Commit [`3fc3690`](https://github.com/pgbackrest/pgbackrest/commit/3fc3690dd77ef5fa032abb006558184164db53ec)

**Verbesserungen:**

- Überspringen der Seitenheader-Prüfungen ermöglicht. (*Geprüft von David Christensen. Vorgeschlagen von David Christensen.*)

  Die Prüfungen der Seitenheader während der Seitenprüfsummenprüfung können bei verschlüsselten Seiten falsche Fehler melden. Mit `page-header-check=n` werden sie übersprungen. Standardmäßig sind sie aktiviert.

  Pull Request [#2045](https://github.com/pgbackrest/pgbackrest/pull/2045); Commit [`f5e6bc2`](https://github.com/pgbackrest/pgbackrest/commit/f5e6bc26983396ec51c6579aade37db39807f3a5)
- `chown()` auf Recovery-Dateien während der Wiederherstellung vermieden. (*Geprüft von Stefan Fercot, Marcelo Henrique Neppel. Vorgeschlagen von Marcelo Henrique Neppel.*)

  Die Wiederherstellung übersprang `chown()` bei wiederhergestellten Dateien mit bereits richtigem Eigentümer, nicht aber bei den geschriebenen Recovery-Dateien. Nun überspringt auch der Posix-Treiber `chown()`, wenn der Eigentümer bereits stimmt.

  Issue [#2036](https://github.com/pgbackrest/pgbackrest/issues/2036); Pull Request [#2038](https://github.com/pgbackrest/pgbackrest/pull/2038); Commit [`3ff88ff`](https://github.com/pgbackrest/pgbackrest/commit/3ff88ffbb495fd669e9a361478e60192930ee0a1)
- Fehlerdetails zu Wiederholungsversuchen bei HTTP hinzugefügt.

  Ein Fehler nach HTTP-Wiederholungen nennt nun deren Anzahl und Dauer.

  [`801e396`](https://github.com/pgbackrest/pgbackrest/commit/801e396dace2a4d9f4125ef0e751c90dc0cc644a) Fehlermodule in das Verzeichnis common/error verschieben.

  [`df419b3`](https://github.com/pgbackrest/pgbackrest/commit/df419b34b55a15a902ff5cc1912aaebc7e023738) Fehlermeldungen bei Wiederholungsversuchen verbessern.

  [`f33e1cf`](https://github.com/pgbackrest/pgbackrest/commit/f33e1cfb1600643820a1ae76bdeb15c62ac1fcc7) Details zu wiederholten Fehlern bei HTTP-Wiederholungen hinzufügen.

**Verbesserungen der Dokumentation:**

- Warnung zur Verwendung von Recovery mit `type=none` hinzugefügt. (*Geprüft von Stefan Fercot.*)

  Bei Recovery mit `type=none` wird die Timeline am Ende nicht erhöht. Dadurch kann PostgreSQL doppelte WAL-Dateien archivieren, die abgelehnt werden und den Datenträger füllen. Auch Werkzeuge wie `pg_rewind` können fehlschlagen oder den Cluster beschädigen. Die Dokumentation warnt nun davor.

  Issue [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Pull Request [#2069](https://github.com/pgbackrest/pgbackrest/pull/2069); Commit [`a28b72c`](https://github.com/pgbackrest/pgbackrest/commit/a28b72c62431bcf9df02791219d9d6f5d0e60b54)
- Hinweis zur Ausführung von `stanza-create` auf bereits erstellten Repositorys hinzugefügt.

  Bereits vorhandene Stanzas werden übersprungen. `stanza-create` kann daher bedenkenlos erneut ausgeführt werden, etwa nach dem Konfigurieren eines neuen Repositorys.

  Commit [`0c1f823`](https://github.com/pgbackrest/pgbackrest/commit/0c1f823e7a3abf1cadb44de3832ec1ddb2da7ec8)

### v2.45 – Versionshinweise {#v245-release-notes}

*Blockinkrementelles Backup (BETA)*

*Veröffentlicht am 20. März 2023*

**Fehlerbehebungen:**

- Schreiben von `recovery.signal` bei der Wiederherstellung von Offline-Backups standardmäßig übersprungen. (*Geprüft von Stefan Fercot. Gemeldet von Marcel Borger.*)

  Bei PostgreSQL >= 12 verhindert `recovery.signal` den Start, wenn das Backup offline mit `wal_level=minimal` erstellt wurde. Bei Offline-Backups wird die Datei nun nicht mehr geschrieben, außer `type` ist ausdrücklich gesetzt. Dies kann etwa für eine zeitpunktbezogene Wiederherstellung aus einem Offline-Backup mit höherem `wal_level` erforderlich sein.

  [`0818601`](https://github.com/pgbackrest/pgbackrest/commit/0818601c055724bde3b97d4b02d3a38b0a53899a) Online-Flag im Manifest der Unit-Tests command/restore setzen.

  [`2fa7e53`](https://github.com/pgbackrest/pgbackrest/commit/2fa7e53c5d4b5a5fd79f62d39763746727a5b9be) recovery.signal beim Wiederherstellen von Offline-Backups standardmäßig nicht schreiben.; Issue [#2018](https://github.com/pgbackrest/pgbackrest/issues/2018); Pull Request [#2019](https://github.com/pgbackrest/pgbackrest/pull/2019)

**Funktionen:**

- Blockinkrementelles Backup (BETA). (*Geprüft von John Morris, Stephen Frost, Stefan Fercot.*)

  Die blockinkrementelle Verarbeitung speichert nur die seit dem vorherigen Backup geänderten Teile einer Datei statt der gesamten Datei. Aktivieren Sie sie mit `repo-block`, das `repo-bundle` voraussetzt. Die Funktion ist in der Beta-Phase und benötigt zusätzlich die Option `beta`. Verwenden Sie sie nicht in Produktion: Das Datenträgerformat wird sich vor der allgemein verfügbaren Version noch ändern.

  [`089fae0`](https://github.com/pgbackrest/pgbackrest/commit/089fae035bf0a9778fff0527ea3cbb113625a403) Blockinkrementelle Verarbeitung zur Ausgabe des Tests real/all hinzufügen.

  [`3feed38`](https://github.com/pgbackrest/pgbackrest/commit/3feed389a2199454db68e446851323498b45db20) Behandlung des Dateiendes in IoChunkedRead verbessern.

  [`d520816`](https://github.com/pgbackrest/pgbackrest/commit/d520816acf9ecb01ef805cecbc9de7e8d0a9f468) Parameterliste aus deltaMapNew() entfernen.

  [`779efe0`](https://github.com/pgbackrest/pgbackrest/commit/779efe0d7a54340141e01597279e9ab1d0bd0773) Blockinkrementelle Größen einheitlich als size_t deklarieren.

  [`dffc933`](https://github.com/pgbackrest/pgbackrest/commit/dffc933384e4327e2fd52868dd19668ed9d3ed91) DeltaMap in BlockHash umbenennen.

  [`a9867cb`](https://github.com/pgbackrest/pgbackrest/commit/a9867cb0b8e8d7abcac9b18b76e3e490c265f3cb) Optionen repo-block-age-map und repo-block-size-map hinzufügen.

  [`16ac5ee`](https://github.com/pgbackrest/pgbackrest/commit/16ac5ee8d3b926464cd27e8f064579f1e7935f4c) Blockinkrementelle Manifestschlüssel umbenennen.

  [`da91858`](https://github.com/pgbackrest/pgbackrest/commit/da9185870222057b97365f5db0acf797f959ec5e) Optionales Rohformat für Komprimierungstypen hinzufügen.

  [`7e5adc0`](https://github.com/pgbackrest/pgbackrest/commit/7e5adc03594a3b7a975001e80902a51df3ddd577) Rohkomprimierung und Rohverschlüsselung für Bündelung und blockinkrementelle Backups verwenden.

  [`8b5153a`](https://github.com/pgbackrest/pgbackrest/commit/8b5153ad210011812c8fe6db2f2ed829a5aa543a) Superblöcke für blockinkrementelle Backups.; Pull Request [#1996](https://github.com/pgbackrest/pgbackrest/pull/1996)

  [`210bed4`](https://github.com/pgbackrest/pgbackrest/commit/210bed4511ae5523b170eb193b877346d787140d) xxHash statt SHA-1 für blockinkrementelle Prüfsummen verwenden.

  [`6252c0e`](https://github.com/pgbackrest/pgbackrest/commit/6252c0e4485caee362edec13302a5f735a69bff4) Größe des Backup-Satzes bei blockinkrementellen Backups aus info ausschließen.

  [`1119a53`](https://github.com/pgbackrest/pgbackrest/commit/1119a5353911d6d326edac325f530bb796a806ae) BlockHash in BlockChecksum umbenennen.

  [`6b409d0`](https://github.com/pgbackrest/pgbackrest/commit/6b409d049eb935146f7996b75b97744b75c411a9) Standardwerte für Block- und Superblockgröße anhand der Tests anpassen.

  [`1281a6e`](https://github.com/pgbackrest/pgbackrest/commit/1281a6eaf8552232c8c9af4d7fc15c082a7794d9) Sicherstellen, dass bei gleicher Block- und Superblockgröße keine Fortsetzungen entstehen.

  [`5c1f78d`](https://github.com/pgbackrest/pgbackrest/commit/5c1f78d4dd62c37218285d13b09a9450eb3a588e) Tippfehler in blockIncrProcess() korrigieren.

  [`c30d3e4`](https://github.com/pgbackrest/pgbackrest/commit/c30d3e439b77d544477e289606d30d0c8ffe301f) Korrekturen und Verbesserungen blockinkrementeller Zuordnungen.; Pull Request [#2026](https://github.com/pgbackrest/pgbackrest/pull/2026)

  [`24f7252`](https://github.com/pgbackrest/pgbackrest/commit/24f725212d0c1dedc0f34fe4e939e481585ff697) Infrastruktur für Beta-Funktionen hinzufügen.

  [`04d224b`](https://github.com/pgbackrest/pgbackrest/commit/04d224b88e73194ff1c6497dbecaaff392008dfe) Beta-Funktion und Dokumentation für blockinkrementelle Backups hinzufügen.

  Entwicklung in [v2.44](#v244-release-notes):

  [`912eec6`](https://github.com/pgbackrest/pgbackrest/commit/912eec63bb971c10a545e582f628c982f4e00005) Blockinkrementelles Backup.; Issue [#959](https://github.com/pgbackrest/pgbackrest/issues/959); Issue [#1806](https://github.com/pgbackrest/pgbackrest/issues/1806); Issue [#1913](https://github.com/pgbackrest/pgbackrest/issues/1913); Pull Request [#1916](https://github.com/pgbackrest/pgbackrest/pull/1916)

  Entwicklung in [v2.42](#v242-release-notes):

  [`1ea6a41`](https://github.com/pgbackrest/pgbackrest/commit/1ea6a4142e47e2e0b56911ad1f028dfcddc5fd64) Aktualisierung von Manifestdateieinträgen verbessern.; Pull Request [#1888](https://github.com/pgbackrest/pgbackrest/pull/1888)

  [`c647bcb`](https://github.com/pgbackrest/pgbackrest/commit/c647bcb50954f623d29104cdb8a1457ed8e94579) Manifest-Flags zur Dateiverarbeitung während des Backups hinzufügen.; Pull Request [#1889](https://github.com/pgbackrest/pgbackrest/pull/1889)

  [`102ce5d`](https://github.com/pgbackrest/pgbackrest/commit/102ce5dee47e8d9a8d2eeaf2b2cc2bac105914ef) Persistente Referenzliste zum Manifest hinzufügen.; Pull Request [#1890](https://github.com/pgbackrest/pgbackrest/pull/1890)

  [`ac99201`](https://github.com/pgbackrest/pgbackrest/commit/ac99201c0ebde616279214e600e49fdf506f7469) bufferSize zu cvtUInt64FromVarInt128() hinzufügen, um Lesevorgänge weiter zu begrenzen.

  [`5602f17`](https://github.com/pgbackrest/pgbackrest/commit/5602f179a177a8513b96c762590829c012c28175) varint-128-Kodierung und -Dekodierung zu IoRead/IoWrite hinzufügen.; Pull Request [#1891](https://github.com/pgbackrest/pgbackrest/pull/1891)

  [`352cbf1`](https://github.com/pgbackrest/pgbackrest/commit/352cbf1d5738a720292b5067051a05efc2b9a8ac) Boolesche Werte von ManifestFile in Bitfelder umwandeln.

  [`e7e106f`](https://github.com/pgbackrest/pgbackrest/commit/e7e106f781be01027d4829b258902549eb36eb7b) Schreibgeschützten Speicher zur Prüfsummenberechnung in restoreFile() verwenden.

  [`909be41`](https://github.com/pgbackrest/pgbackrest/commit/909be412f8ad0d87f23ce2a2dbca94c3e0732f9f) Unit-Tests command/backup und command/restore tauschen.

  [`1730ef4`](https://github.com/pgbackrest/pgbackrest/commit/1730ef4ac3d88137bd218e6128b0107a8bf2c121) Flag noTruncate zu storageNewWriteP() hinzufügen.; Pull Request [#1898](https://github.com/pgbackrest/pgbackrest/pull/1898)

  [`fee38c2`](https://github.com/pgbackrest/pgbackrest/commit/fee38c2c7cc3ae318bf0d3b50fe23c22900c2311) Filter als Handler-Array an entfernten Speicher übergeben.

  [`5fceee8`](https://github.com/pgbackrest/pgbackrest/commit/5fceee88a9439460bf24082f275ec2e695cc6bf6) backupFileRepoPathP() hinzufügen.

  [`221db61`](https://github.com/pgbackrest/pgbackrest/commit/221db610d2a054ed00ad27377663941abfb9fb98) Namen in der Integrationstestmatrix real/all kürzen.

  [`c9db7bc`](https://github.com/pgbackrest/pgbackrest/commit/c9db7bc274211820030c4ab6ab8c70c1b1896254) cipherBlockNew() um optionale Parameter erweitern.

  [`58b3c91`](https://github.com/pgbackrest/pgbackrest/commit/58b3c91babc6af9e003e5ef09bf99becf8a6f827) Rohmodus zu CipherBlock hinzufügen, um Platz zu sparen.

**Verbesserungen:**

- Nur einen Gruppenindex mit ausschließlich Standardwerten beibehalten. (*Geprüft von Stefan Fercot.*)

  Eine nicht anwendbare Option, etwa `repo2-s3-key`, wenn `repo2-type` nicht `s3` ist, konnte ein Phantom-Repository mit ausschließlich Standardwerten erzeugen. Repository- und PostgreSQL-Indizes mit nur Standardwerten werden nun entfernt, sofern noch ein anderer Index verbleibt.

  Pull Request [#2011](https://github.com/pgbackrest/pgbackrest/pull/2011); Commit [`1648c13`](https://github.com/pgbackrest/pgbackrest/commit/1648c133d6bc1ffd0682ae6219934d00295aa580)

**Verbesserungen der Dokumentation:**

- Explizite Anweisungen für Upgrades zwischen `2.x`-Versionen hinzugefügt. (*Beigetragen von Christophe Courtois. Geprüft von David Steele.*)

  Ein neuer Abschnitt im Benutzerhandbuch erklärt, dass für Upgrades zwischen `2.x`-Versionen nur die neuen Binärdateien installiert werden müssen. Ein Downgrade ist ebenfalls möglich, sofern keine von der älteren Version nicht unterstützten Funktionen verwendet wurden.

  Issue [#1774](https://github.com/pgbackrest/pgbackrest/issues/1774); Pull Request [#1993](https://github.com/pgbackrest/pgbackrest/pull/1993); Commit [`15d5dcd`](https://github.com/pgbackrest/pgbackrest/commit/15d5dcdd3bb387aab28bbe7262011c38c7d6d22c)
- Mit der Einführung von TLS überholte Verweise auf SSH entfernt.

  Die Hilfe für `repo-host`, `pg-host` und deren Portoptionen nennt SSH nicht mehr als einziges Remote-Protokoll. Auch Angaben zur SSH-Komprimierung wurden entfernt.

  Commit [`c5907a2`](https://github.com/pgbackrest/pgbackrest/commit/c5907a2e7193ca8f79cf56dca23e0df118e686c3)

### v2.44 – Versionshinweise {#v244-release-notes}

*Unterstützung für PostgreSQL 9.0/9.1/9.2 entfernt*

*Veröffentlicht am 30. Januar 2023*

**Verbesserungen:**

- Unterstützung für PostgreSQL `9.0`/`9.1`/`9.2` entfernt. (*Geprüft von Stefan Fercot.*)

  pgBackRest unterstützt nun zehn PostgreSQL-Versionen: die fünf noch unterstützten und die letzten fünf Versionen nach ihrem Supportende. Mit PostgreSQL 15 sind damit `9.0`, `9.1` und `9.2` ausgeschlossen.

  Pull Request [#1941](https://github.com/pgbackrest/pgbackrest/pull/1941); Commit [`77c721e`](https://github.com/pgbackrest/pgbackrest/commit/77c721eb635c6d757d2d5ed6f2ffc083720c10a7)
- Wiederherstellung mit Fehler abgebrochen, wenn kein Backup zur aktuellen PostgreSQL-Version passt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Soulou.*)

  Nach einem `stanza-upgrade` ohne neues Backup verwendete die Wiederherstellung das letzte Backup der vorherigen PostgreSQL-Version. Daraus erstellte Replikate konnten fehlschlagen. Die Wiederherstellung meldet nun in diesem Fall einen Fehler, sofern nicht `set` oder `type=time`/`type=lsn` angegeben ist.

  Issue [#1942](https://github.com/pgbackrest/pgbackrest/issues/1942); Pull Request [#1967](https://github.com/pgbackrest/pgbackrest/pull/1967); Commit [`b9be4fa`](https://github.com/pgbackrest/pgbackrest/commit/b9be4fa54039e2c79fad0dc1552c7ffaf883004c)
- Bereichsprüfung für `compress-level` für jeden `compress-type` hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von gkleen, ViperRu.*)

  Der Bereich für `compress-level` war bei jedem `compress-type` auf `0-9` begrenzt. Das ist der Bereich für `gz`, aber nur eine Teilmenge der von `lz4` und `zst` erlaubten Werte. Jeder Typ hat nun seinen eigenen Bereich, etwa `-7` bis `22` für `zst`.

  Issue [#1216](https://github.com/pgbackrest/pgbackrest/issues/1216); Issue [#1931](https://github.com/pgbackrest/pgbackrest/issues/1931); Pull Request [#1962](https://github.com/pgbackrest/pgbackrest/pull/1962); Commit [`44da314`](https://github.com/pgbackrest/pgbackrest/commit/44da314adb2b63f96b1d571f822e91a0e412e984)

**Verbesserungen der Dokumentation:**

- Warnung zur Aktivierung des „hierarchischen Namensraums“ auf Azure-Speicher hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von Vojtech Galda, Pluggi, asjonos.*)

  Bei aktiviertem hierarchischem Namespace verlangt Azure, Verzeichnisse separat zu löschen, wodurch `expire` fehlschlägt. Das Benutzerhandbuch warnt nun davor, diese Funktion zu aktivieren.

  Issue [#1770](https://github.com/pgbackrest/pgbackrest/issues/1770); Pull Request [#1980](https://github.com/pgbackrest/pgbackrest/pull/1980); Commit [`3aea997`](https://github.com/pgbackrest/pgbackrest/commit/3aea997df5ace85251d0579ccbe13fa938f587ee)
- Ersetzung von Zeilenvorschüben im Überwachungsbeispiel hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von rudonx, gmustdie, Ivan Shelestov.*)

  Das Überwachungsbeispiel schlug fehl, wenn die Ausgabe von `info` einen Zeilenumbruch enthielt, etwa in manchen Fehlermeldungen. `COPY` wandelt `\n` in einen Zeilenumbruch um, den `jsonb` ablehnt. Das Beispiel ersetzt nun Zeilenumbrüche vor der Umwandlung in `jsonb`.

  Issue [#1910](https://github.com/pgbackrest/pgbackrest/issues/1910); Pull Request [#1963](https://github.com/pgbackrest/pgbackrest/pull/1963); Commit [`ae258f6`](https://github.com/pgbackrest/pgbackrest/commit/ae258f604e634f1d2a760ffdb92dd359fd1129bb)
- Verhalten von `target-action` bei verschiedenen PostgreSQL-Versionen erläutert. (*Beigetragen von Chris Bandy. Geprüft von David Steele, Anton Kurochkin, Stefan Fercot. Vorgeschlagen von Anton Kurochkin, Chris Bandy.*)

  Die Wirkung von `pause` hängt von `hot_standby` und der PostgreSQL-Version ab. Bei `hot_standby=off` verhält sich `pause` unter PostgreSQL >= 12 wie `shutdown`, bei älteren Versionen wie `promote`.

  Issue [#987](https://github.com/pgbackrest/pgbackrest/issues/987); Issue [#1314](https://github.com/pgbackrest/pgbackrest/issues/1314); Pull Request [#1960](https://github.com/pgbackrest/pgbackrest/pull/1960); Commit [`84a3ff8`](https://github.com/pgbackrest/pgbackrest/commit/84a3ff8b7ac1243c0b47c6585697f4fcf3c12065)
- Übersichtsseite aktualisiert und erläutert. (*Geprüft von Stefan Fercot.*)

  Der Abschnitt über fehlende Parallelverarbeitung in anderen Backup-Lösungen war nicht mehr zutreffend und wurde neu formuliert. Weitere Abschnitte wurden für aktuelle Begriffe und bessere Verständlichkeit überarbeitet.

  Pull Request [#1966](https://github.com/pgbackrest/pgbackrest/pull/1966); Commit [`36ee30d`](https://github.com/pgbackrest/pgbackrest/commit/36ee30d118ce6cc7720653a3d3a49a06c655c463)
- Dunkelmodus zur Website hinzugefügt. (*Vorgeschlagen von Stephen Frost.*)

  Die Website verwendet dunkle Farben, wenn der Browser ein dunkles Farbschema bevorzugt.

  Commit [`ed818b3`](https://github.com/pgbackrest/pgbackrest/commit/ed818b31867c640d72ef829dd36cd0a7feff12df)

### v2.43 – Versionshinweise {#v243-release-notes}

*Fehlerbehebung*

*Veröffentlicht am 28. November 2022*

**Fehlerbehebungen:**

- Fehlende Referenz bei differenziellen/inkrementellen Backups korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Marcel Borger, ulfedf, jaymefSO.*)

  In v2.42 schlug ein differenzielles oder inkrementelles Backup mit „unable to find '...' in string list“ fehl, wenn sein Vorgänger mit einer älteren Version erstellt worden war. Die für ein älteres Manifest aufgebaute Referenzliste enthält nun auch die Kennzeichnung des Backups selbst.

  [`28f6604`](https://github.com/pgbackrest/pgbackrest/commit/28f660482aa5abb97850a9d7c89c2e5e9f23a4c9) Test für manifestBackupLabelSet() im Unit-Test info/manifest verschieben.

  [`c4bf775`](https://github.com/pgbackrest/pgbackrest/commit/c4bf775099c85e3cd081f9c1ce35efd4c71d9161) Fehlende Referenz bei diff/incr-Backups korrigieren.; Issue [#1933](https://github.com/pgbackrest/pgbackrest/issues/1933); Pull Request [#1935](https://github.com/pgbackrest/pgbackrest/pull/1935)

**Verbesserungen:**

- Hinweis hinzugefügt, wenn eine Option ohne Index angegeben wird. (*Geprüft von Stefan Fercot.*)

  Eine Option, die einen Index benötigt, etwa `repo-storage-ca-file`, meldet nun einen Fehler mit einem Hinweis auf den indizierten Namen wie `repo1-storage-ca-file`. Bei veralteten Optionen nennt ein Hinweis außerdem den aktuellen Namen.

  Issue [#1925](https://github.com/pgbackrest/pgbackrest/issues/1925); Pull Request [#1929](https://github.com/pgbackrest/pgbackrest/pull/1929); Commit [`3f363cb`](https://github.com/pgbackrest/pgbackrest/commit/3f363cb3aed1a7c6836ee6c32eae600129a6f6b8)

### v2.42 – Versionshinweise {#v242-release-notes}

*Fehlerbehebungen*

*Veröffentlicht am 22. November 2022*

**Fehlerbehebungen:**

- Speicherleck bei `backup`/`restore` mit Dateibündelung behoben. (*Geprüft von John Morris. Getestet von Oscar. Gemeldet von Oscar.*)

  Bei gebündelten Dateien gab die Wiederherstellung manche E/A-Objekte erst frei, nachdem alle Dateien des Bündels wiederhergestellt waren. Bei vielen kleinen Dateien wuchs der Speicherbedarf bis zum Fehler „unable to allocate“. Beim Fortsetzen eines Backups gab es ein ähnliches, kleineres Speicherleck.

  Issue [#1877](https://github.com/pgbackrest/pgbackrest/issues/1877); Pull Request [#1878](https://github.com/pgbackrest/pgbackrest/pull/1878); Commit [`cd8db7d`](https://github.com/pgbackrest/pgbackrest/commit/cd8db7d9e53e041ad6fb31f2f015541c1d24abc2)
- Protokollfehler bei unvollständigem Lesen einer entfernten Datei behoben. (*Geprüft von Stephen Frost.*)

  Ein vorzeitig beendeter oder teilweise fehlgeschlagener Lesevorgang einer entfernten Datei hinterließ das Protokoll in einem ungültigen Zustand. Der nächste Befehl scheiterte mit „client state is 'data-get' but expected 'idle'“, und der ursprüngliche Fehler ging verloren. Nun wird beim Schließen der Datei der verbleibende Inhalt gelesen.

  [`ea162e8`](https://github.com/pgbackrest/pgbackrest/commit/ea162e821634919b7c839e866b99bf82010dbacc) storageReadRemoteOpen() im Modul storage/remote/read verschieben.

  [`7967c75`](https://github.com/pgbackrest/pgbackrest/commit/7967c750d83466d030081e9deb1d70a1ba240271) Protokollfehler beim unvollständigen Lesen einer entfernten Datei beheben.; Pull Request [#1900](https://github.com/pgbackrest/pgbackrest/pull/1900)

**Verbesserungen:**

- Beim Bündeln keine Referenzen für Dateien mit der Länge null gespeichert. (*Geprüft von Stefan Fercot.*)

  Gebündelte diff/incr-Backups speicherten für leere Dateien eine Referenz auf ein vorheriges Backup, obwohl leere Dateien in keinem Backup gespeichert werden. Die Referenz wurde bei der Wiederherstellung ignoriert, belegte aber Platz im Manifest.

  Pull Request [#1887](https://github.com/pgbackrest/pgbackrest/pull/1887); Commit [`f981fb4`](https://github.com/pgbackrest/pgbackrest/commit/f981fb45d9931e597afec764e13b1a53d8365d25)
- Allgemeinere Beschreibungen für `pg_start_backup()`/`pg_stop_backup()` verwendet. (*Geprüft von Greg Sabino Mullane, David Christensen. Vorgeschlagen von Greg Sabino Mullane.*)

  PostgreSQL 15 benannte diese Funktionen in `pg_backup_start()`/`pg_backup_stop()` um. Protokolle und Dokumentation verwenden nun Beschreibungen, die von der PostgreSQL-Version unabhängig sind.

  Pull Request [#1901](https://github.com/pgbackrest/pgbackrest/pull/1901); Commit [`ddd966c`](https://github.com/pgbackrest/pgbackrest/commit/ddd966cadc30440a81100144204d4084a0f2ac3a)

**Verbesserungen der Testsuite:**

- Option `--psql-bin` von `test.pl` an die Befehlszeilenhilfe angepasst. (*Beigetragen von Koshi Shibagaki. Geprüft von David Steele.*)

  Die Hilfe zeigte `--psql-bin`, die Option hieß jedoch `--pgsql-bin`. Nun trägt die Option den in der Hilfe angegebenen Namen.

  Pull Request [#1920](https://github.com/pgbackrest/pgbackrest/pull/1920); Commit [`3ad5884`](https://github.com/pgbackrest/pgbackrest/commit/3ad588443b452e04f3abcc107e825dc47e078103)

### v2.41 – Versionshinweise {#v241-release-notes}

*Backup-Anmerkungen*

*Veröffentlicht am 19. September 2022*

**Fehlerbehebungen:**

- Falsche zeitbasierte Ablaufberechnung für nicht als Standard verwendete Repositorys korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Adam Brusselback.*)

  Wurde `expire` ohne `repo` ausgeführt, wurde der zeitbasierte Wert von `repo-retention-full` für alle Repositorys aus dem Repository mit der niedrigsten Nummer gelesen. Nun verwendet jedes Repository seinen eigenen Wert.

  Issue [#1852](https://github.com/pgbackrest/pgbackrest/issues/1852); Pull Request [#1854](https://github.com/pgbackrest/pgbackrest/pull/1854); Commit [`eda7f81`](https://github.com/pgbackrest/pgbackrest/commit/eda7f81ee4fd6818ce458768144fc3fc1e1f0f21)
- Problem beim rekursiven Auflisten von Verzeichnissen mit einem Filter behoben. (*Geprüft von Stephen Frost. Gemeldet von Efremov Egor.*)

  `repo-ls` mit `recurse` und `filter` konnte durch doppelte Speicherfreigabe oder einen Segmentierungsfehler scheitern, wenn der letzte Verzeichniseintrag ein nicht leeres Unterverzeichnis war. Eine übergeordnete Liste wurde freigegeben, bevor die Einträge ihrer Unterverzeichnisse verarbeitet waren.

  Issue [#1870](https://github.com/pgbackrest/pgbackrest/issues/1870); Pull Request [#1871](https://github.com/pgbackrest/pgbackrest/pull/1871); Commit [`c39c9f2`](https://github.com/pgbackrest/pgbackrest/commit/c39c9f220ed328b4175d912e109697b726e9ea9b)

**Funktionen:**

- Anmerkungen als Schlüssel-Wert-Paare für Backups. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Adam Berlin.*)

  Mit der Option `annotation` von `backup` lassen sich einem Backup Schlüssel-Wert-Anmerkungen hinzufügen. Der neue Befehl `annotate` kann sie später ergänzen, ändern oder entfernen. `info` zeigt Anmerkungen in der Textausgabe bei gesetztem `set` an und nimmt sie immer in die JSON-Ausgabe auf.

  Issue [#1709](https://github.com/pgbackrest/pgbackrest/issues/1709); Pull Request [#1724](https://github.com/pgbackrest/pgbackrest/pull/1724); Commit [`381fd0a`](https://github.com/pgbackrest/pgbackrest/commit/381fd0a5a4de61624615b150ba98beeafac31f7e)

**Verbesserungen:**

- `--set` in der JSON-Ausgabe des Befehls `info` unterstützt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Anton Kurochkin.*)

  Mit `set` enthält die JSON-Ausgabe von `info` nun die bereits in der Textausgabe vorhandenen Details, etwa die Fehler- und Tablespace-Listen.

  Issue [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Pull Request [#1501](https://github.com/pgbackrest/pgbackrest/pull/1501); Commit [`db75ffd`](https://github.com/pgbackrest/pgbackrest/commit/db75ffd27037d690a11eb02902f929250fe2bf5b)
- Konfiguration der Upload-Chunk-Größe für Objektspeicher ermöglicht. (*Geprüft von Stefan Fercot. Vorgeschlagen von Anton Glushakov.*)

  Mit `repo-storage-upload-chunk-size` wird die Größe jedes Upload-Teils für S3, GCS oder Azure festgelegt. Größere Teile können die Leistung verbessern, benötigen aber mehr Speicher. Die Standardwerte bleiben unverändert.

  [`ff1188f`](https://github.com/pgbackrest/pgbackrest/commit/ff1188f92dfc9e8f6d4aeca8b71a9886f24f58b4) quote-Tag in der Befehlszeilenhilfe zulassen.

  [`b05d31f`](https://github.com/pgbackrest/pgbackrest/commit/b05d31f531b55b747175cf94c963f95574c54d2b) Konfiguration der Upload-Chunk-Größe für Objektspeicher erlauben.; Issue [#1843](https://github.com/pgbackrest/pgbackrest/issues/1843); Pull Request [#1847](https://github.com/pgbackrest/pgbackrest/pull/1847)
- Zeitstempel von archive.info nach erfolgreichem Backup aktualisiert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Alex Richman.*)

  `archive.info` und seine Kopie wurden nur von `stanza-create` und `stanza-upgrade` geschrieben. Eine Lebenszyklusrichtlinie des Objektspeichers zum Entfernen alter Dateien konnte sie daher löschen. Ihre Zeitstempel werden nun nach jedem erfolgreichen Backup aktualisiert.

  Issue [#1853](https://github.com/pgbackrest/pgbackrest/issues/1853); Pull Request [#1855](https://github.com/pgbackrest/pgbackrest/pull/1855); Commit [`3b5df1e`](https://github.com/pgbackrest/pgbackrest/commit/3b5df1e089234d425dd225f8c1976755dc947c8a)
- Prüfung der Standby-Timeline hinter den Checkpoint verschoben. (*Geprüft von Stefan Fercot. Getestet von Keith Fiske. Vorgeschlagen von Keith Fiske.*)

  Die Prüfung, ob der Standby auf der erwarteten Timeline liegt, verwendete `pg_control` aus der Zeit vor dem Backup-Start. Direkt nach einer Promotion war die neue Timeline möglicherweise noch nicht in `pg_control` eingetragen, und das Backup scheiterte mit „standby is on timeline ... but expected ...“. Die Prüfung erfolgt nun nach dem Checkpoint.

  Issue [#1816](https://github.com/pgbackrest/pgbackrest/issues/1816); Pull Request [#1819](https://github.com/pgbackrest/pgbackrest/pull/1819); Commit [`c267ba5`](https://github.com/pgbackrest/pgbackrest/commit/c267ba51b1778b5872f4ee928a9614545d743f3f)
- Warnmeldung beim Fortsetzen eines Backups verbessert. (*Vorgeschlagen von Cynthia Shang.*)

  Die Warnung klang, als müsse der Benutzer eingreifen. Nun stellt sie klar, dass ungültige Dateien entfernt werden und anschließend das Backup fortgesetzt wird.

  Commit [`cbbe93f`](https://github.com/pgbackrest/pgbackrest/commit/cbbe93f592d8097393c5ffe214f0a8c5fb0549c1)

**Verbesserungen der Dokumentation:**

- Absoluten Pfad für `kill` in `pgbackrest.service` hinzugefügt. (*Vorgeschlagen von Don Seiler.*)

  Das Beispiel `pgbackrest.service` verwendet nun `/bin/kill` in `ExecReload`. Ältere systemd-Versionen benötigen einen absoluten Pfad.

  Commit [`e9ff524`](https://github.com/pgbackrest/pgbackrest/commit/e9ff5248039eedb25da2fee550ec64fcebbc51c7)

### v2.40 – Versionshinweise {#v240-release-notes}

*Unterstützung für OpenSSL 3*

*Veröffentlicht am 18. Juli 2022*

**HINWEIS FÜR PAKETBETREUER**: Ein experimenteller meson-Build wurde hinzugefügt. Paketbetreuer sollten jedoch auf absehbare Zeit weiterhin den Build mit autoconf/make verwenden.

**Verbesserungen:**

- Unterstützung für OpenSSL 3. (*Geprüft von Stephen Frost.*)

  pgBackRest lässt sich nun mit OpenSSL 3 kompilieren. Warnungen zu veralteten Funktionen werden unterdrückt. Ein unerwartetes EOF wird anhand der von OpenSSL 3 gemeldeten Fehlercodes erkannt.

  Pull Request [#1767](https://github.com/pgbackrest/pgbackrest/pull/1767); Commit [`08242ee`](https://github.com/pgbackrest/pgbackrest/commit/08242ee6ac93b9eb9c05cc39e3db15bbafb9052c)
- Beim Auflisten des Inhalts eines Pfads einen Snapshot erstellt. (*Geprüft von John Morris, Stephen Frost.*)

  Ein unsortiert aufgelisteter Pfad wurde gelesen, während seine Einträge verarbeitet wurden. Wurden währenddessen Dateien gelöscht, übersprangen manche Dateisysteme noch vorhandene Dateien, sodass sich der Pfad nicht entfernen ließ. Auflistungen verwenden nun stets eine Momentaufnahme des Pfads.

  [`61ca9b5`](https://github.com/pgbackrest/pgbackrest/commit/61ca9b58a000aa8789ef3267682519bdb15e8a6b) hrnStorageInfoListCallback() in Tests durch TEST_STORAGE_LIST() ersetzen.

  [`1c0bf0b`](https://github.com/pgbackrest/pgbackrest/commit/1c0bf0b15da8c0d15cc639851ff1d1bd05b51d06) Null-Prüfungen für Benutzer und Gruppen im Remote-Protokoll umordnen und Tests ergänzen.

  [`72960bb`](https://github.com/pgbackrest/pgbackrest/commit/72960bbf179b4e8051bd4fc50be57d95159e9e13) strTrunc() in strTruncIdx() umbenennen und strTrunc() hinzufügen.

  [`75623d4`](https://github.com/pgbackrest/pgbackrest/commit/75623d4583bfdaccb3a19b935fd04d744b363923) Beim Auflisten eines Pfadinhalts eine Momentaufnahme erstellen.; Issue [#1754](https://github.com/pgbackrest/pgbackrest/issues/1754); Pull Request [#1805](https://github.com/pgbackrest/pgbackrest/pull/1805)
- `target-timeline=current` bei einer Wiederherstellung mit `type=immediate` erzwungen. (*Geprüft von Stephen Frost.*)

  Bei PostgreSQL >= 12 ist `latest` die Standard-Ziel-Timeline. Die Recovery konnte fehlschlagen, wenn die neueste Timeline im Repository vom Backup aus nicht erreichbar war. Eine Wiederherstellung mit `type=immediate` wechselt die Timeline nicht und setzt das Ziel daher nun auf `current`.

  Pull Request [#1814](https://github.com/pgbackrest/pgbackrest/pull/1814); Commit [`364af16`](https://github.com/pgbackrest/pgbackrest/commit/364af1635d40431276cc6fd87d6ddd689b611e09)
- Dateien bei Delta-`restore` gekürzt, wenn sie größer als erwartet sind. (*Geprüft von Stephen Frost.*)

  Die Delta-Wiederherstellung kopierte eine Datei aus dem Repository, sobald ihre Größe vom Manifest abwich. Eine größere Datei wird nun auf die Manifestgröße gekürzt und nur kopiert, wenn ihre Prüfsumme nicht stimmt. Dateien, an die lediglich Daten angehängt wurden, etwa Protokolle, werden nicht mehr kopiert.

  Pull Request [#1758](https://github.com/pgbackrest/pgbackrest/pull/1758); Commit [`7ec51e7`](https://github.com/pgbackrest/pgbackrest/commit/7ec51e7e6279ea576ad3b4b5c2ea1fc389d08ab5)
- Inkrementelles Speichern des Manifests bei `resume=n` deaktiviert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Während eines Backups wird das Manifest regelmäßig gespeichert, um eine Fortsetzung zu ermöglichen. Bei `resume=n` entfallen diese Speichervorgänge nun.

  Pull Request [#1760](https://github.com/pgbackrest/pgbackrest/pull/1760); Commit [`60d70fa`](https://github.com/pgbackrest/pgbackrest/commit/60d70fa66fc3f709914f40dd088bac1b467001f2)
- Backup-Fortschritt vor Beginn des Kopierens auf null Prozent gesetzt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Der Fortschritt eines Backups wurde erst nach dem Kopieren der ersten Datei gemeldet. Nun wird er zu Beginn des Kopierens auf null gesetzt.

  Pull Request [#1759](https://github.com/pgbackrest/pgbackrest/pull/1759); Commit [`38ad283`](https://github.com/pgbackrest/pgbackrest/commit/38ad2838d553febae1b7fe0244d942dfaa9cf548)
- S3-Flag `IsTruncated` verwendet, um die Fortsetzung der Auflistung zu bestimmen. (*Geprüft von John Morris. Getestet von Soulou. Vorgeschlagen von Christian Montagne.*)

  Neuere Scality-Versionen senden bei einer nicht abgeschnittenen Liste ein leeres `NextContinuationToken`. Dies verursachte eine Endlosschleife. Nun entscheidet `IsTruncated`, ob die Liste fortgesetzt wird. Ein fehlendes oder leeres Token bei einer abgeschnittenen Liste ist ein Fehler.

  Issue [#1748](https://github.com/pgbackrest/pgbackrest/issues/1748); Pull Request [#1783](https://github.com/pgbackrest/pgbackrest/pull/1783); Commit [`845d82f`](https://github.com/pgbackrest/pgbackrest/commit/845d82f6825d4101e6a465a435ef056ff6ec15a2)

**Fehlerbehebungen in der Dokumentation:**

- Interne Optionen in der Konfigurationsreferenz übersprungen. (*Gemeldet von Francisco Miguel Biete Banon.*)

  Optionen, die nur für einige Befehle intern sind, erschienen in der Konfigurationsreferenz. Die Befehlszeilenhilfe war nicht betroffen.

  Commit [`2643050`](https://github.com/pgbackrest/pgbackrest/commit/2643050be0dc4b7363c434f58373919bd6fdac68)

**Verbesserungen der Dokumentation:**

- Link zur PostgreSQL-Konfiguration im Abschnitt zum Repository-Host hinzugefügt. (*Geprüft von Stefan Fercot. Vorgeschlagen von Julien Cigar.*)

  Pull Request [#1809](https://github.com/pgbackrest/pgbackrest/pull/1809); Commit [`74a4ac8`](https://github.com/pgbackrest/pgbackrest/commit/74a4ac801db921f7b11b63b9f927228c6a6af861)

**Verbesserungen der Testsuite:**

- Experimentellen Meson-Build hinzugefügt. (*Geprüft von Eli Schwartz, Sam Bassaly.*)

  Meson hat eine einfachere Syntax und bessere Leistung als autoconf/make. Es wird für Codegenerierung und Test-Builds verwendet und lehnt alle Builds außer Debug-Builds ab. Paketbetreuer sollten weiterhin autoconf/make verwenden.

  [`2feaaea`](https://github.com/pgbackrest/pgbackrest/commit/2feaaeaac803d6c0193477b56dbeb622fd991156) In andere C-Dateien eingebundenen C-Dateien die Erweiterung .inc geben.

  [`b8fc20d`](https://github.com/pgbackrest/pgbackrest/commit/b8fc20d5b8e7ca003ff39f29ea6e3ba57653f55c) Experimentellen Meson-Build hinzufügen.; Pull Request [#1765](https://github.com/pgbackrest/pgbackrest/pull/1765)

  [`665da12`](https://github.com/pgbackrest/pgbackrest/commit/665da12ae7f519077512e60ce3a5ec6c6a9997fd) Include-Kommentar in meson.build allgemeiner formulieren.

  [`9fd85a1`](https://github.com/pgbackrest/pgbackrest/commit/9fd85a104ad56061b028afd9057ce8c1d636d3dd) meson für alle Builds außer Debug-Builds deaktivieren.

  [`59f148b`](https://github.com/pgbackrest/pgbackrest/commit/59f148bf6ea8c090d4d65ce5b135a71501e8ae22) -fmacro-prefix-map erzeugen, um den relativen Pfad aus __FILE__ zu entfernen.

  [`0eccbc8`](https://github.com/pgbackrest/pgbackrest/commit/0eccbc8bf47073ab8ec1f13fed9865d0bd7c3635) Meson-Builds mit Version 0.45 ermöglichen.
- Übergabe beliebiger Pfade an die Option `--test-path` ermöglicht. (*Beigetragen von Andrey Sokolov. Geprüft von David Steele.*)

  Pull Request [#1764](https://github.com/pgbackrest/pgbackrest/pull/1764); Commit [`29b2a54`](https://github.com/pgbackrest/pgbackrest/commit/29b2a54fcc74457af5c63ffb505c5fbb24bb2ade)
- Kompilierfehler behoben, wenn `DEBUG_EXEC_TIME` ohne `DEBUG` definiert ist. (*Beigetragen von Andrey Sokolov. Geprüft von David Steele.*)

  Ohne `DEBUG` expandierte das `ASSERT()`, das die Startzeit verwendete, zu nichts. Die ungenutzte Variable verursachte dadurch einen Kompilierungsfehler. Die Prüfung verwendet nun `CHECK()`.

  Pull Request [#1775](https://github.com/pgbackrest/pgbackrest/pull/1775); Commit [`1a00ab1`](https://github.com/pgbackrest/pgbackrest/commit/1a00ab10033e9ac6e6f797627567e8b91e143432)

### v2.39 – Versionshinweise {#v239-release-notes}

*Überprüfung und Dateibündelung*

*Veröffentlicht am 16. Mai 2022*

**Fehlerbehebungen:**

- Fehler behoben, bei dem eine aus `FINALLY()` ausgelöste Ausnahme eine Endlosschleife verursachte. (*Geprüft von Stephen Frost.*)

  Ein in einem `FINALLY()`-Block ausgelöster Fehler führte zurück in denselben Block. Dort wurde er wahrscheinlich erneut ausgelöst und verursachte eine Endlosschleife. `FINALLY()` läuft nun nur einmal.

  [`9a271e9`](https://github.com/pgbackrest/pgbackrest/commit/9a271e925c6239fbd3577f9827c34940e7e43ae4) Endlosschleife durch einen aus FINALLY() ausgelösten Fehler beheben.; Pull Request [#1732](https://github.com/pgbackrest/pgbackrest/pull/1732)

  [`ef4c4ab`](https://github.com/pgbackrest/pgbackrest/commit/ef4c4ab8525f81c9ed22c7e82ed12096e81703c5) Zustand von FINALLY() mit einer Variablen statt einer Funktion verfolgen.; Pull Request [#1744](https://github.com/pgbackrest/pgbackrest/pull/1744)
- Bei allen Sperrfehlern einen Fehler ausgegeben, außer wenn ein anderer Prozess die Sperre hält. (*Geprüft von Reid Thompson. Getestet von Geir Råness. Gemeldet von Geir Råness.*)

  `archive-get`/`archive-push` meldeten keinen Fehler, wenn die Sperre aus einem anderen Grund wie fehlenden Berechtigungen nicht erworben werden konnte. Der asynchrone Prozess wurde nicht gestartet, und der Benutzer erhielt nur eine allgemeine Fehlermeldung ohne asynchrones Protokoll. Solche Fehlschläge werden nun als Fehler gemeldet.

  Issue [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Pull Request [#1730](https://github.com/pgbackrest/pgbackrest/pull/1730); Commit [`9629908`](https://github.com/pgbackrest/pgbackrest/commit/962990869454b15db058f4037dbc0b1b611fc95e)

**Funktionen:**

- Bündelung von Backup-Dateien zur besseren Unterstützung kleiner Dateien. (*Geprüft von Reid Thompson, Stefan Fercot, Chris Bandy.*)

  Beim Bündeln werden kleine Dateien gemeinsam im Repository gespeichert, um beim Backup Zeit und Platz zu sparen. Das hilft besonders bei Objektspeichern, auf denen das Anlegen jeder Datei aufwendig ist. Aktivieren Sie es mit `repo-bundle` und passen Sie es mit `repo-bundle-size` und `repo-bundle-limit` an. Die Wiederherstellung liest benachbarte Dateien eines Bündels mit einem einzigen Lesevorgang.

  [`4d2fef1`](https://github.com/pgbackrest/pgbackrest/commit/4d2fef1c37d357965f0ffb9af0d7489f3be1371b) Redundanten restoreFile()-Test entfernen und Testabdeckung verbessern.

  [`5141370`](https://github.com/pgbackrest/pgbackrest/commit/514137040e60e8fff0e7f42f43b493113abae5ff) Parameter limit zu ioCopyP() hinzufügen.

  [`dca6da8`](https://github.com/pgbackrest/pgbackrest/commit/dca6da86bfe84a0cda004df1140d125db1630c90) Befehl restore für Dateibündelung optimieren.; Issue [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Pull Request [#1683](https://github.com/pgbackrest/pgbackrest/pull/1683)

  [`0054677`](https://github.com/pgbackrest/pgbackrest/commit/0054677147121967889ead7feab0959fb19e39a6) Bündelprotokollierung zum Befehl backup hinzufügen.

  [`3f66f42`](https://github.com/pgbackrest/pgbackrest/commit/3f66f42ef9605a83c356e4c6eb3ef47bcb12c30d) Optionen bundle-* in repo-bundle-* umbenennen.; Pull Request [#1694](https://github.com/pgbackrest/pgbackrest/pull/1694)

  [`fe9fd2f`](https://github.com/pgbackrest/pgbackrest/commit/fe9fd2ff2d778b86c0df159aabe7644f18f6479f) repo-hardlink bei aktiviertem repo-bundle deaktivieren.

  [`424008d`](https://github.com/pgbackrest/pgbackrest/commit/424008d293661dfb1a167cfec2697def48057447) Dateien zulassen, die nach Erstellung des Backup-Manifests leer werden.

  [`f405fc6`](https://github.com/pgbackrest/pgbackrest/commit/f405fc6ae281eebf4d61abb39963a9830fe2fa2f) Bündelung von Backup-Dateien dokumentieren.; Pull Request [#1740](https://github.com/pgbackrest/pgbackrest/pull/1740)

  Entwicklung in [v2.38](#v238-release-notes):

  [`a79034a`](https://github.com/pgbackrest/pgbackrest/commit/a79034ae2f6a8ec66b84c62ab6cd4042d2c1a249) Bereichslesen für alle Speichertreiber hinzufügen.; Pull Request [#1619](https://github.com/pgbackrest/pgbackrest/pull/1619)

  [`b791f1c`](https://github.com/pgbackrest/pgbackrest/commit/b791f1c82f53fa16866837d4544b58243c682f7f) Eigentümer bei der Wiederherstellung ohne Änderungen an Manifest-Interna setzen.

  [`f84909f`](https://github.com/pgbackrest/pgbackrest/commit/f84909f85f7dfb202ac812c67665cc590a5acad4) Behandlung des Posix-Leseoffsets nach einem Fehler korrigieren.

  [`4ca0590`](https://github.com/pgbackrest/pgbackrest/commit/4ca0590a51a665535fbba903b8f55e10557b606a) backupProcessQueue() zur Verwendung der Struktur BackupJobData refaktorieren.

  [`16559d9`](https://github.com/pgbackrest/pgbackrest/commit/16559d9e421c66596d21b047c8afe1b2c96ccd82) Wo passend die Konstante PG_FILE_POSTMTRPID verwenden.

  [`8c062e1`](https://github.com/pgbackrest/pgbackrest/commit/8c062e1af824c3dc80ff94b3df8d433f95e88d0f) primary-Flag aus dem Manifest entfernen.; Pull Request [#1630](https://github.com/pgbackrest/pgbackrest/pull/1630)

  [`b0db4b8`](https://github.com/pgbackrest/pgbackrest/commit/b0db4b8ff00db913cb69308017a56155d6070830) Berechtigungen des Basispfads in den Integrationstests mock/all vereinfachen.

  [`4a73a02`](https://github.com/pgbackrest/pgbackrest/commit/4a73a0286387f3f2185f3f193f9c20ed0d7d926d) Manifeststandardwerte vereinfachen.; Pull Request [#1631](https://github.com/pgbackrest/pgbackrest/pull/1631)

  [`575ae77`](https://github.com/pgbackrest/pgbackrest/commit/575ae77c0dee12b932469d479b2e45dbaf389737) Im Manifest varNewUInt64() nach Möglichkeit durch VARUINT64() ersetzen.

  [`61ce586`](https://github.com/pgbackrest/pgbackrest/commit/61ce58692f3092b72833b6e9ee87037f45b3b702) Manifestdateistrukturen platzsparend packen.; Pull Request [#1626](https://github.com/pgbackrest/pgbackrest/pull/1626)

  [`ca13f11`](https://github.com/pgbackrest/pgbackrest/commit/ca13f11b4a3858587c7055b0b2b4a8b396dd8451) jsonFromStrInternal() optimieren.

  [`e4df5b7`](https://github.com/pgbackrest/pgbackrest/commit/e4df5b7d3846134832b9315e22786f679d63a46b) Standardwerte für Manifestdateien vereinfachen.; Pull Request [#1632](https://github.com/pgbackrest/pgbackrest/pull/1632)

  [`7dd657b`](https://github.com/pgbackrest/pgbackrest/commit/7dd657b7dd163ded9fbf7caef37eea7e08bc5a37) Erzeugung von Dateinamen im Modul command/verify vereinfachen.

  [`34d6495`](https://github.com/pgbackrest/pgbackrest/commit/34d649579eb3bd1530aa99f0ed1879e7d3125424) Dateien während des Backups im Repository bündeln.; Issue [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Pull Request [#1655](https://github.com/pgbackrest/pgbackrest/pull/1655)

  [`efc09db`](https://github.com/pgbackrest/pgbackrest/commit/efc09db7b9ece6e7b7f92538d56d6ab7b9798f8f) Bündelbare Dateien begrenzen.; Issue [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Pull Request [#1662](https://github.com/pgbackrest/pgbackrest/pull/1662)

  [`e6e1122`](https://github.com/pgbackrest/pgbackrest/commit/e6e1122dbcf5e667d683295f7e7e45de4bbf56bd) Datei in manifestFileAdd() als Referenz übergeben.
- Verify-Befehl zum Validieren des Inhalts eines Repositorys. (*Beigetragen von Cynthia Shang, Reid Thompson. Geprüft von David Steele, Stefan Fercot.*)

  Der Befehl `verify` prüft, ob Backups und WAL im Repository gültig sind. Mit `output=text` werden die Ergebnisse ausgegeben; `verbose` zeigt neben Fehlern auch erfolgreich geprüfte Elemente an.

  Pull Request [#1607](https://github.com/pgbackrest/pgbackrest/pull/1607); Commit [`65d22e4`](https://github.com/pgbackrest/pgbackrest/commit/65d22e43257d46ff6523ffbdb3af59e30deeaea5)
- Unterstützung für PostgreSQL 15. (*Geprüft von Stefan Fercot.*)

  PostgreSQL 15 entfernt exklusive Backups, benennt die Funktionen zum Starten und Beenden von Backups um und entfernt `pg_database.datlastsysoid`, das pgBackRest nicht mehr verwendet.

  [`692fe49`](https://github.com/pgbackrest/pgbackrest/commit/692fe496bdb5fa6dcffeb9f85b6188ceb1df707a) Abhängigkeit von pg_database.datlastsysoid entfernen.; Pull Request [#1735](https://github.com/pgbackrest/pgbackrest/pull/1735)

  [`20782c8`](https://github.com/pgbackrest/pgbackrest/commit/20782c88bc8d0842d547bd5f4fecdb292e69d1f7) Unterstützung für PostgreSQL 15.; Pull Request [#1736](https://github.com/pgbackrest/pgbackrest/pull/1736)
- Backup-Fortschritt in Prozent in der Ausgabe von `info` angezeigt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  `info` zeigt den Fertigstellungsgrad eines laufenden Backups auf dessen Ausführungshost an. Die JSON-Ausgabe meldet ihn als Ganzzahl, nämlich den Prozentwert mal 100.

  [`d9088b2`](https://github.com/pgbackrest/pgbackrest/commit/d9088b2e2b16a89d29b967187a547976f96061fc) Backup-Fortschritt in Prozent in info ausgeben.; Issue [#1490](https://github.com/pgbackrest/pgbackrest/issues/1490); Pull Request [#1621](https://github.com/pgbackrest/pgbackrest/pull/1621)

  [`a6b1adb`](https://github.com/pgbackrest/pgbackrest/commit/a6b1adb5fd533b4b9aca29646c8acf647d872959) Überflüssigen Zeilenumbruch beim Schreiben einer Sperrdatei entfernen.

  Entwicklung in [v2.38](#v238-release-notes):

  [`22734eb`](https://github.com/pgbackrest/pgbackrest/commit/22734eb376b3183924cb7794f9111c1eeb5d92d6) ioBufferReadNewOpen() und ioBufferWriteNewOpen() hinzufügen.

  [`9b2f10d`](https://github.com/pgbackrest/pgbackrest/commit/9b2f10dbb49a8b869cef2c419d9957ed4c550016) Sperrcode refaktorieren.; Pull Request [#1643](https://github.com/pgbackrest/pgbackrest/pull/1643)
- Backup für den Befehl `restore` mit `--type=lsn` automatisch ausgewählt. (*Beigetragen von Reid Thompson. Geprüft von Stefan Fercot, David Steele.*)

  Mit `type=lsn` wählt die Wiederherstellung nun das neueste Backup, das am LSN `target` oder davor endete.

  [`08d9e26`](https://github.com/pgbackrest/pgbackrest/commit/08d9e269c6f03e7797584e90c53eb0743b787f60) Prüfung des Zieltyps im Wiederherstellungsmodul verständlicher gestalten.

  [`d8d4132`](https://github.com/pgbackrest/pgbackrest/commit/d8d4132118edd7f93a5b221478c85c2d213c39dd) Backup für restore --type=lsn automatisch auswählen.; Pull Request [#1706](https://github.com/pgbackrest/pgbackrest/pull/1706)

  [`ea4d73f`](https://github.com/pgbackrest/pgbackrest/commit/ea4d73f375558c237fce696f20c19d1efef00bc1) Reihenfolge des Felds backup-lsn-stop im Unit-Test command/restore korrigieren.
- Warnung zu vorhandenem WAL bei deaktiviertem `archive-mode-check` unterdrückt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Bei `archive-mode-check=n` und WAL-Übertragung von mehreren Hosts ist eine bereits archivierte WAL-Datei mit gleicher Prüfsumme zu erwarten und erzeugt keine Warnung mehr. Eine andere Prüfsumme bleibt ein Fehler.

  Pull Request [#1711](https://github.com/pgbackrest/pgbackrest/pull/1711); Commit [`aad7171`](https://github.com/pgbackrest/pgbackrest/commit/aad7171940afdb221a03825bee6eb2f1827289f1)
- Unterstützung für AWS IMDSv2 hinzugefügt. (*Beigetragen von Nuno Pires. Geprüft von David Steele.*)

  IMDSv2 schützt die Instanzmetadaten, die Anmeldedaten für `repo-s3-key-type=auto` bereitstellen. Scheitert die IMDSv2-Tokenanfrage, fällt pgBackRest auf IMDSv1 zurück.

  Issue [#1685](https://github.com/pgbackrest/pgbackrest/issues/1685); Pull Request [#1691](https://github.com/pgbackrest/pgbackrest/pull/1691); Commit [`21cef09`](https://github.com/pgbackrest/pgbackrest/commit/21cef09dfd03c313531dc66ba9556164ae2835ab)

**Verbesserungen:**

- Ändern der Option `repo-hardlink` nach einem vollständigen Backup ermöglicht. (*Geprüft von Reid Thompson.*)

  Eine Änderung von `repo-hardlink` erforderte ein neues vollständiges Backup. Die Option kann nun jederzeit geändert werden, etwa zum Deaktivieren für die Dateibündelung.

  Pull Request [#1699](https://github.com/pgbackrest/pgbackrest/pull/1699); Commit [`7afaac0`](https://github.com/pgbackrest/pgbackrest/commit/7afaac0a3d0e43e5598d1abf548559dbe6329363)
- Genauigkeit der Fortschrittsprotokollierung in Prozent für `backup` und `restore` erhöht. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Der Fortschritt wird nun in Hundertstelprozent protokolliert. Dadurch gibt es bei großen Backups und Wiederherstellungen häufiger Aktualisierungen.

  Pull Request [#1679](https://github.com/pgbackrest/pgbackrest/pull/1679); Commit [`330e199`](https://github.com/pgbackrest/pgbackrest/commit/330e19900ee3415d920680cf6e6856bf5e8e9a69)
- Pfadvalidierung für die Befehle `repo-*` verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Ein Pfad darf kein `//` enthalten, ein abschließendes `/` wird entfernt, und absolute Pfade müssen innerhalb des Repository-Pfads liegen.

  [`5ae84d5`](https://github.com/pgbackrest/pgbackrest/commit/5ae84d5e474e95dcc00c174aa5111815a5a70ba5) Pfadprüfung für repo-*-Befehle verbessern.; Pull Request [#1697](https://github.com/pgbackrest/pgbackrest/pull/1697)

  [`19dd015`](https://github.com/pgbackrest/pgbackrest/commit/19dd015d589ed3efd31a2a238249a150fb3748c1) Probleme der verbesserten Pfadprüfung für repo-*-Befehle beheben.; Pull Request [#1751](https://github.com/pgbackrest/pgbackrest/pull/1751)
- Befehl `stop` verbessert, sodass er die Option `stanza` berücksichtigt. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von ragaoua.*)

  `stop` mit `force` und `stanza` beendet nun nur Prozesse, die Sperren für diese Stanza halten. Zuvor wurden Prozesse aller Stanzas beendet.

  Issue [#1608](https://github.com/pgbackrest/pgbackrest/issues/1608); Pull Request [#1676](https://github.com/pgbackrest/pgbackrest/pull/1676); Commit [`f7ab002`](https://github.com/pgbackrest/pgbackrest/commit/f7ab002aa74dd2ca277123f7500018ae68a04c74)
- Fehlermeldung bei ungültigem `repo-azure-key` verbessert. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Seth Daniel.*)

  Bei `repo-azure-key-type=shared` wird `repo-azure-key` nun auf gültiges Base64 geprüft.

  Issue [#1686](https://github.com/pgbackrest/pgbackrest/issues/1686); Pull Request [#1688](https://github.com/pgbackrest/pgbackrest/pull/1688); Commit [`7c9208b`](https://github.com/pgbackrest/pgbackrest/commit/7c9208ba856a71833dc7d8f1cf8cb2b4bb4b7414)
- Hinweis zur Prüfung des Protokolls bei asynchronen Fehlern von `archive-get`/`archive-push` hinzugefügt. (*Geprüft von Reid Thompson.*)

  Kann der asynchrone Prozess seine Statusdateien nicht schreiben, läuft `archive-get`/`archive-push` mit einem allgemeinen Fehler in ein Zeitlimit. Der Fehler nennt nun den Pfad des asynchronen Protokolls, das die eigentliche Fehlermeldung enthält.

  Issue [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`03c71aa`](https://github.com/pgbackrest/pgbackrest/commit/03c71aa606bc0dc89303b3907e7fcbd83ace79d6)
- `ClockError` für unerwartete Uhrabweichungen und Zeitzonenänderungen hinzugefügt. (*Geprüft von Greg Sabino Mullane, Stefan Fercot. Vorgeschlagen von Greg Sabino Mullane.*)

  Pull Request [#1739](https://github.com/pgbackrest/pgbackrest/pull/1739); Commit [`5f8c9cd`](https://github.com/pgbackrest/pgbackrest/commit/5f8c9cd66a1b39a47acaddfbc3cf443ae8057519)
- Dateinamenerweiterungen des historischen Manifests vor der Anzeige in der Fehlermeldung entfernt. (*Geprüft von Stefan Fercot.*)

  War eine neue Backup-Kennzeichnung nicht neuer als die letzte in der Historie, zeigte der Fehler den Namen des historischen Manifests an, etwa `20220504-222042F_20220504-222141I.manifest.gz`. Nun wird nur die Kennzeichnung angezeigt.

  Pull Request [#1738](https://github.com/pgbackrest/pgbackrest/pull/1738); Commit [`b6bfd9f`](https://github.com/pgbackrest/pgbackrest/commit/b6bfd9f99d74b1f5e631cf6462b68342589d2b80)
- user:group zum Berechtigungsfehler bei Sperren hinzugefügt. (*Geprüft von Reid Thompson.*)

  Issue [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`0055fa4`](https://github.com/pgbackrest/pgbackrest/commit/0055fa40fee2636fed88699f52e9e67cd2803f71)
- Hinweis ergänzen, wenn der Primärcluster nicht gefunden wird.

  Der Fehler „unable to find primary cluster“ enthält nun den Hinweis, zu prüfen, ob alle verfügbaren Cluster in Recovery sind.

  Commit [`46b7b72`](https://github.com/pgbackrest/pgbackrest/commit/46b7b7287446d0bb5ed0963fd01c51fb2b08893f)

**Fehlerbehebungen in der Dokumentation:**

- Falschen Verweis auf `stanza-update` im Benutzerhandbuch korrigiert. (*Behoben von Abubakar Mohammed. Geprüft von David Steele.*)

  Commit [`3dd7960`](https://github.com/pgbackrest/pgbackrest/commit/3dd796045160c4d4dbf70ec2800ad483867629f1)
- Beispiel für die Option `repo-gcs-key-type` in der Konfigurationsreferenz korrigiert. (*Geprüft von Reid Thompson.*)

  Das Beispiel verwendete den ungültigen Wert `none`. Nun verwendet es `auto`.

  Commit [`166039c`](https://github.com/pgbackrest/pgbackrest/commit/166039c0da1875581a08d41ab8a44adf95fa6db1)
- Beispiel für `tls-server-auth` korrigiert und Erläuterungen hinzugefügt. (*Geprüft von Reid Thompson.*)

  Im Beispiel fehlte der Client-CN. Es lautet nun `client-cn=stanza1`. Die Hilfe stellt außerdem klar, dass für den Client-CN keine Platzhalter zulässig sind.

  Commit [`c222ce1`](https://github.com/pgbackrest/pgbackrest/commit/c222ce1a5f6f813188b7e87a3838d6dce656e0ff)

**Verbesserungen der Dokumentation:**

- Aussagen zu unterstützten Versionen in der Dokumentation vereinfacht. (*Geprüft von Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)

  Die Benutzerhandbücher nannten PostgreSQL-Versionsbereiche und erweckten damit den Eindruck, andere Versionen wie PostgreSQL 12 unter RHEL würden nicht unterstützt. Die Bereiche wurden entfernt. Die Einleitung erklärt nun, welche Versionen die Handbücher abdecken.

  Pull Request [#1742](https://github.com/pgbackrest/pgbackrest/pull/1742); Commit [`eefa0b1`](https://github.com/pgbackrest/pgbackrest/commit/eefa0b161a6a02b7843e18455443a4bce41cd4b9)
- Beschreibungen der Optionstypen hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Die Konfigurationsreferenz beschreibt nun jeden Optionstyp, etwa die Einheiten für Größenoptionen, statt die Beschreibung bei jeder Option zu wiederholen.

  Pull Request [#1747](https://github.com/pgbackrest/pgbackrest/pull/1747); Commit [`a913113`](https://github.com/pgbackrest/pgbackrest/commit/a913113fda5886ffd2ff136cdd52a3f469eca026)
- FAQ zu Backup-Typen und Wiederherstellungsgeschwindigkeit hinzugefügt. (*Beigetragen von David Christensen. Geprüft von Reid Thompson.*)

  Ein neuer FAQ-Eintrag erklärt, dass der Backup-Typ nur das Backup beeinflusst, nicht die Geschwindigkeit der Wiederherstellung.

  Pull Request [#1731](https://github.com/pgbackrest/pgbackrest/pull/1731); Commit [`50d409a`](https://github.com/pgbackrest/pgbackrest/commit/50d409a812be577f2c296f3d6096cf97fab049ff)
- Erforderlichen Basisbranch für Pull Requests dokumentiert. (*Beigetragen von David Christensen. Geprüft von Reid Thompson.*)

  Der Beitragsleitfaden legt nun fest, dass Pull Requests auf dem Branch `integration` basieren müssen.

  Pull Request [#1733](https://github.com/pgbackrest/pgbackrest/pull/1733); Commit [`cc5b061`](https://github.com/pgbackrest/pgbackrest/commit/cc5b0614894e1b5ef78f1ceba3bc8e4760a40a24)

### v2.38 – Versionshinweise {#v238-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 6. März 2022*

**WICHTIGER HINWEIS**: Die vom Befehl `info` gemeldete Repository-Größe basiert nun vollständig auf den Daten, die pgBackRest in den Speicher geschrieben hat. Zuvor konnte pgBackRest in bestimmten Fällen erkennen, ob der Speicher zusätzliche Komprimierung anwendete. Dies wird nicht mehr unterstützt.

**Fehlerbehebungen:**

- Bei Fehlern während der S3-Stapellöschung von Dateien Wiederholungsversuche durchgeführt. (*Geprüft von Reid Thompson. Gemeldet von Alex Richman.*)

  Eine fehlgeschlagene Batch-Löschung wurde wiederholt, Fehler einzelner Dateien im Batch jedoch nicht. Dadurch konnte pgBackRest bei der Ablaufbehandlung oder beim Entfernen eines nicht fortsetzbaren Backups abbrechen. Im Batch fehlgeschlagene Dateien werden nun einzeln mit den üblichen HTTP-Wiederholungen gelöscht.

  Issue [#1650](https://github.com/pgbackrest/pgbackrest/issues/1650); Pull Request [#1653](https://github.com/pgbackrest/pgbackrest/pull/1653); Commit [`551e5bc`](https://github.com/pgbackrest/pgbackrest/commit/551e5bc6f67c91cf1e11da0cefe24f9650353adc)
- Vergleich der Werte des HTTP-Headers `connection` ohne Beachtung der Groß-/Kleinschreibung ermöglicht. (*Geprüft von Reid Thompson. Gemeldet von Rémi Vidier.*)

  Die HTTP-Spezifikation erlaubt beliebige Groß-/Kleinschreibung in Werten des Headers `connection`, etwa `Close`.

  Issue [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Pull Request [#1675](https://github.com/pgbackrest/pgbackrest/pull/1675); Commit [`b33cabe`](https://github.com/pgbackrest/pgbackrest/commit/b33cabe08c33e29eb8aef65dd46b2c1f3cf2d186)

**Funktionen:**

- Unterstützung für serverseitige Verschlüsselung von AWS S3 mit KMS hinzugefügt. (*Beigetragen von Christoph Berg. Geprüft von David Steele. Getestet von Tharindu Amila.*)

  Mit `repo-s3-kms-key-id` werden Objekte mit einem von AWS KMS verwalteten Schlüssel verschlüsselt.

  Issue [#1430](https://github.com/pgbackrest/pgbackrest/issues/1430); Pull Request [#1567](https://github.com/pgbackrest/pgbackrest/pull/1567); Commit [`3097acd`](https://github.com/pgbackrest/pgbackrest/commit/3097acd73a21b630aa5352be57a82b031930f96b)
- Option `archive-missing-retry` hinzugefügt. (*Geprüft von Stefan Fercot.*)

  Standardmäßig versucht `archive-get` ein bereits als fehlend gemeldetes WAL-Segment erneut. So werden Fehlmeldungen im Spool-Pfad aus einer früheren Wiederherstellung ignoriert. Mit `archive-missing-retry=n` kann PostgreSQL das Archivende erkennen und auch während laufender WAL-Archivierung auf Streaming umschalten. Der Spool-Pfad muss dann zu Beginn der Recovery leer sein.

  Pull Request [#1642](https://github.com/pgbackrest/pgbackrest/pull/1642); Commit [`10038db`](https://github.com/pgbackrest/pgbackrest/commit/10038db9c9f2b4753c3821e0b246fa8626527184)
- Filter für den Backup-Typ zum Befehl `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Setzen Sie `type`, um nur Backups dieses Typs anzuzeigen, etwa `type=full`.

  Issue [#600](https://github.com/pgbackrest/pgbackrest/issues/600); Pull Request [#1651](https://github.com/pgbackrest/pgbackrest/pull/1651); Commit [`b26097f`](https://github.com/pgbackrest/pgbackrest/commit/b26097f8d8a7e2af6e9a21576994cbb47110c6f4)

**Verbesserungen:**

- Bei fehlgeschlagener Seitenprüfung während `backup` einen Wiederholungsversuch ausgeführt. (*Geprüft von Stephen Frost, David Christensen.*)

  Eine Seite mit ungültiger Prüfsumme wird nun erneut gelesen. Nur wenn sie unverändert ist, wird ein Fehler gemeldet. Eine veränderte Seite wird gerade von PostgreSQL geschrieben, und das WAL enthält ein vollständiges Seitenabbild. Nullseiten werden nun vollständig auf Nullwerte geprüft, nicht nur anhand von `pd_upper`.

  [`b489707`](https://github.com/pgbackrest/pgbackrest/commit/b4897077937ee4571ba719276a44d5db0a75510e) Tests aus command/backup-common in das Modul command/backup verschieben.

  [`9eec98c`](https://github.com/pgbackrest/pgbackrest/commit/9eec98c61302121134d2067326dbd2cd0f2f0b9c) Bei fehlgeschlagener Seitenprüfsummenprüfung während des Backups erneut lesen.; Issue [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Pull Request [#1667](https://github.com/pgbackrest/pgbackrest/pull/1667)

  [`53f1b25`](https://github.com/pgbackrest/pgbackrest/commit/53f1b2520434221c01caf92e052403a28c455c1b) Prüfung von Nullseiten verbessern.; Issue [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Pull Request [#1669](https://github.com/pgbackrest/pgbackrest/pull/1669)
- TLS-Server behandelt, die Verbindungen nicht geordnet schließen. (*Geprüft von David Christensen, Stephen Frost. Getestet von Rémi Vidier.*)

  Einige Server schließen den Socket statt der TLS-Verbindung. Hat eine Antwort weder Inhaltslänge noch Chunked-Encoding und lässt sich ihr Inhalt auswerten, gilt der geschlossene Socket nun als EOF. Diese Server funktionierten seit v2.35 nicht mehr.

  Issue [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Pull Request [#1677](https://github.com/pgbackrest/pgbackrest/pull/1677); Commit [`59a5373`](https://github.com/pgbackrest/pgbackrest/commit/59a5373cf85e4ad0057b592bfe855495384dfcbd)
- Backup-LSNs zur Ausgabe des Befehls `info` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Start- und End-LSN eines Backups werden mit `set` und in der JSON-Ausgabe angezeigt, um eine LSN-basierte zeitpunktbezogene Wiederherstellung zu ermöglichen.

  Pull Request [#1610](https://github.com/pgbackrest/pgbackrest/pull/1610); Commit [`d866dd5`](https://github.com/pgbackrest/pgbackrest/commit/d866dd5c297dc046581134a108032cf9694cae0e)
- Abschließende Schrägstriche in Pfaden für `repo-ls` automatisch entfernt. (*Beigetragen von David Christensen. Geprüft von David Steele.*)

  Ein abschließender Schrägstrich im Pfad führte bei manchen Repository-Speichertypen dazu, dass `repo-ls` keinen Inhalt anzeigte.

  Pull Request [#1673](https://github.com/pgbackrest/pgbackrest/pull/1673); Commit [`6320712`](https://github.com/pgbackrest/pgbackrest/commit/632071232344a1160ef932d6e0d65eb3149ed226)
- Bei fatalen Fehlern keine Wiederholungsversuche durchgeführt. (*Geprüft von Reid Thompson.*)

  Das Wiederholen fataler Fehler, besonders bei Speichermangel, kann zum Hängenbleiben führen. Assertion- und Speicherfehler werden nun ohne Wiederholung gemeldet.

  [`8573a2d`](https://github.com/pgbackrest/pgbackrest/commit/8573a2df14d0bfd5578333b68147cc12c93c6f96) Fehlertest für protocolClientFree() im Protokollmodul verbessern.

  [`8d0cce6`](https://github.com/pgbackrest/pgbackrest/commit/8d0cce66f83abc1ff02a985ec3f0d7e285c09d72) Im Wiederholungstest des Protokollmoduls einen normalen Fehler verwenden.

  [`8046f06`](https://github.com/pgbackrest/pgbackrest/commit/8046f0630715015d5adcced570c54e9a183c0e73) Fatale Fehler nicht wiederholen.; Pull Request [#1658](https://github.com/pgbackrest/pgbackrest/pull/1658)
- Unterstützung für PostgreSQL `8.3`/`8.4` entfernt. (*Geprüft von Reid Thompson, Stefan Fercot.*)

  Es gibt keine Hinweise darauf, dass diese Versionen noch verwendet werden, während ihre Unterstützung Entwicklungs- und Testzeit kostet. Verwenden Sie eine ältere pgBackRest-Version, um sie zu sichern oder von ihnen zu migrieren.

  Pull Request [#1611](https://github.com/pgbackrest/pgbackrest/pull/1611); Commit [`bb4b30d`](https://github.com/pgbackrest/pgbackrest/commit/bb4b30ddd3f80c246c565eb4769efc82b9509648)
- Logik zur Ermittlung zusätzlicher Dateisystemkomprimierung entfernt. (*Geprüft von Reid Thompson, Stefan Fercot.*)

  Nach dem Kopieren einer Datei prüfte pgBackRest deren Größe auf dem Datenträger, um Dateisystemkomprimierung etwa durch ZFS zu erkennen. Dies war ungetestet, bei vielen kleinen Dateien langsam und verhinderte die Bündelung. Die Repository-Größe in `info` entspricht nun den von pgBackRest geschriebenen Daten.

  Pull Request [#1652](https://github.com/pgbackrest/pgbackrest/pull/1652); Commit [`cb630ff`](https://github.com/pgbackrest/pgbackrest/commit/cb630ffe3b5c819b5e97ac11d5974000bd44d632)

**Fehlerbehebungen in der Dokumentation:**

- Optionen `repo` in der TLS-Dokumentation in den Abschnitt `global` verschoben. (*Gemeldet von Anton Kurochkin.*)

  Das Benutzerhandbuch setzte diese Optionen im Stanza-Abschnitt. Das funktioniert in manchen Fällen, entspricht aber nicht der empfohlenen Vorgehensweise.

  Commit [`53de3e3`](https://github.com/pgbackrest/pgbackrest/commit/53de3e3aeb71f8209f56167941df35bbfcb7cdc9)
- Ungenutzte Option `backup-standby` aus den Stanza-Befehlen entfernt. (*Gemeldet von Stefan Fercot.*)

  `stanza-create` und `stanza-upgrade` führten `backup-standby` in Befehlsreferenz und Hilfe auf, verwendeten die Option aber nicht.

  Commit [`5cbb4a3`](https://github.com/pgbackrest/pgbackrest/commit/5cbb4a3e6b13598b90cae46fad28c31604f9f094)
- Tippfehler in der Hilfe und den Versionshinweisen korrigiert. (*Behoben von Daniel Gustafsson. Geprüft von David Steele.*)

  [`cacfdd9`](https://github.com/pgbackrest/pgbackrest/commit/cacfdd94d74307285b1b590ec0977d7db3142d0d) Tippfehler in Hilfe und Versionshinweisen korrigieren.; Pull Request [#1671](https://github.com/pgbackrest/pgbackrest/pull/1671)

  [`5c332a0`](https://github.com/pgbackrest/pgbackrest/commit/5c332a0b100d5a5180b3d95bd90d4d7b521b42db) Zuordnung von Beiträgen in den Versionshinweisen zu cacfdd94 und f798458e korrigieren.

**Verbesserungen der Dokumentation:**

- Prüfung auf Betriebsbereitschaft zur systemd-Dienstkonfiguration hinzugefügt. (*Vorgeschlagen von Yogesh Sharma.*)

  Das Beispiel `pgbackrest.service` prüft nun kurz nach dem Start, ob der Server noch läuft. Zuvor wurde bei einem fehlgeschlagenen Start kein Fehler gemeldet, während systemd im Hintergrund erneut versuchte zu starten.

  Commit [`f1bdf3e`](https://github.com/pgbackrest/pgbackrest/commit/f1bdf3e04b07dc9a2eaa1fdbe5278cc18371e868)
- FAQ zur Erklärung des WAL-Archivsuffixes hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Das Suffix einer WAL-Datei im Repository ist ihre SHA1-Prüfsumme, mit der die Datei geprüft wird. Es darf nicht weggelassen werden.

  Issue [#1485](https://github.com/pgbackrest/pgbackrest/issues/1485); Issue [#1663](https://github.com/pgbackrest/pgbackrest/issues/1663); Pull Request [#1664](https://github.com/pgbackrest/pgbackrest/pull/1664); Commit [`98d525d`](https://github.com/pgbackrest/pgbackrest/commit/98d525dba43ba259ff7989746b8e5be3382c189d)
- Darauf hingewiesen, dass Replikationsslots nicht wiederhergestellt werden. (*Beigetragen von Reid Thompson. Geprüft von David Steele, Stefan Fercot. Vorgeschlagen von Christophe Courtois.*)

  Issue [#1585](https://github.com/pgbackrest/pgbackrest/issues/1585); Pull Request [#1601](https://github.com/pgbackrest/pgbackrest/pull/1601); Commit [`a82f017`](https://github.com/pgbackrest/pgbackrest/commit/a82f0179cdd5742e5c5b1e0bdfd23166753fdb38)

### v2.37 – Versionshinweise {#v237-release-notes}

*TLS-Server*

*Veröffentlicht am 3. Januar 2022*

**WICHTIGER HINWEIS**: Wenn der Befehl `restore` kein Backup findet, das zu einem angegebenen Zielzeitpunkt passt, wird nun ein Fehler ausgelöst. Zuvor wurde eine Warnung protokolliert.

**Fehlerbehebungen:**

- Delta-Link-Zuordnung von `restore` korrigiert, wenn der Pfad/die Datei bereits existiert. (*Geprüft von Reid Thompson. Gemeldet von Younes Alhroub.*)

  Ordnete `link-map` oder `link-all` einen vorhandenen Pfad oder eine Datei einem Link zu, ließ die Delta-Wiederherstellung den bestehenden Pfad oder die Datei unverändert. Nun wird er bzw. sie durch den Link ersetzt.

  Issue [#1588](https://github.com/pgbackrest/pgbackrest/issues/1588); Pull Request [#1589](https://github.com/pgbackrest/pgbackrest/pull/1589); Commit [`a73fe4e`](https://github.com/pgbackrest/pgbackrest/commit/a73fe4eb966f9685f6e4179c397a10c1e7f15f19)
- Socket-Leck bei wiederholten Verbindungsversuchen behoben. (*Geprüft von Reid Thompson. Gemeldet von James Coleman.*)

  In optimierten Builds wurde der Socket eines fehlgeschlagenen Verbindungsversuchs nicht geschlossen. Jeder erneute Versuch ließ daher einen Socket offen.

  Issue [#1593](https://github.com/pgbackrest/pgbackrest/issues/1593); Pull Request [#1594](https://github.com/pgbackrest/pgbackrest/pull/1594); Commit [`615bdff`](https://github.com/pgbackrest/pgbackrest/commit/615bdff4030a31bfedfe7df04676e3948ec9c2c0)

**Funktionen:**

- TLS-Server hinzugefügt. (*Geprüft von Stephen Frost, Reid Thompson. Getestet von Andrew L'Ecuyer.*)

  Der Befehl `server` startet einen TLS-Server, der statt SSH den Zugriff auf Repository- und PostgreSQL-Hosts ermöglicht. Setzen Sie auf dem Client `repo-host-type=tls` oder `pg-host-type=tls` und konfigurieren Sie Zertifikate sowie Clientautorisierung mit `tls-server-*`. `SIGHUP` lädt die Konfiguration neu, `SIGTERM` stoppt den Server.

  [`2d963ce`](https://github.com/pgbackrest/pgbackrest/commit/2d963ce9471808172f879916c3f3accc35f14d56) Befehl server-start in server umbenennen.

  [`7b3ea88`](https://github.com/pgbackrest/pgbackrest/commit/7b3ea883c7c010aafbeb14d150d073a113b703e4) Behandlung von SIGTERM und SIGHUP zum TLS-Server hinzufügen.; Pull Request [#1572](https://github.com/pgbackrest/pgbackrest/pull/1572)

  [`f06101d`](https://github.com/pgbackrest/pgbackrest/commit/f06101de77a980c7e4115762f2fc301280aa4127) TLS-Serverdokumentation hinzufügen.; Pull Request [#1597](https://github.com/pgbackrest/pgbackrest/pull/1597)

  Entwicklung in [v2.36](#v236-release-notes):

  [`ccc255d`](https://github.com/pgbackrest/pgbackrest/commit/ccc255d3e05d8ce2b6ac251d1498f71b04098a86) TLS-Server hinzufügen.; Pull Request [#1504](https://github.com/pgbackrest/pgbackrest/pull/1504)

  [`13d4559`](https://github.com/pgbackrest/pgbackrest/commit/13d4559708819787ad05be6f37ec0badb0eccae5) Rückgabewert von getsockopt() prüfen.

  Entwicklung in [v2.35](#v235-release-notes):

  [`947c7a8`](https://github.com/pgbackrest/pgbackrest/commit/947c7a84cb37d09ab925785ca7670c970e32b8a3) cmdLocal()/cmdRemote() zur Annahme eines ProtocolServer-Objekts refaktorieren.

  [`0999de0`](https://github.com/pgbackrest/pgbackrest/commit/0999de0279fabf35af80396a9a8d35546ec02d53) noop aus protocolClientNew() in die local/remote-Initialisierung verschieben.
- Option `--cmd` hinzugefügt. (*Beigetragen von Reid Thompson. Geprüft von Stefan Fercot, David Steele. Vorgeschlagen von Virgile CREVON.*)

  Setzen Sie `cmd` auf die pgBackRest-Programmdatei, die in von pgBackRest geschriebenen Befehlen verwendet werden soll, etwa in `restore_command` in `recovery.conf`.

  Issue [#1537](https://github.com/pgbackrest/pgbackrest/issues/1537); Pull Request [#1540](https://github.com/pgbackrest/pgbackrest/pull/1540); Commit [`2a57647`](https://github.com/pgbackrest/pgbackrest/commit/2a576477b316238473525e56bc8fc8ea5790455f)

**Verbesserungen:**

- Archiv unmittelbar nach Beginn des Backups geprüft. (*Geprüft von Reid Thompson, David Christensen.*)

  Ein Backup scheiterte bei nicht funktionierender WAL-Archivierung erst nach dem Kopieren aller Dateien. Nun wird das Archiv direkt nach dem Backup-Start geprüft. Auf einem inaktiven System wird ein Wiederherstellungspunkt erstellt, um einen WAL-Segmentwechsel auszulösen.

  Issue [#152](https://github.com/pgbackrest/pgbackrest/issues/152); Pull Request [#1570](https://github.com/pgbackrest/pgbackrest/pull/1570); Commit [`1f14f45`](https://github.com/pgbackrest/pgbackrest/commit/1f14f45dfb0d1677a695719381cbd5a8a3c6c986)
- Timeline- und Checkpoint-Prüfungen zum Backup hinzugefügt. (*Geprüft von Stefan Fercot, Reid Thompson.*)

  Das Backup prüft nun, ob `pg_control` den Checkpoint und die Timeline des Backup-Starts enthält und ob ein Standby dem Primärserver folgt. Er muss sich auf derselben Timeline befinden und sein Checkpoint darf nicht nach dem Backup-Checkpoint liegen.

  Pull Request [#1581](https://github.com/pgbackrest/pgbackrest/pull/1581); Commit [`49145d7`](https://github.com/pgbackrest/pgbackrest/commit/49145d72bac16498cdbf5eeb3cd6128ea0be0667)
- Während eines Backups geprüft, ob Cluster laufen und korrekt konfiguriert sind. (*Geprüft von Stefan Fercot.*)

  Ein Backup schlägt nun sofort fehl, wenn ein Cluster stoppt oder der Standby zum Primärserver wird. Zuvor wurde ein gestoppter Primärserver erst am Backup-Ende erkannt; eine Promotion des Standbys wurde gar nicht erkannt.

  Pull Request [#1584](https://github.com/pgbackrest/pgbackrest/pull/1584); Commit [`bd2ba80`](https://github.com/pgbackrest/pgbackrest/commit/bd2ba802db11c505ec69943fa81b2b379073fbf4)
- Fehler ausgegeben, wenn `restore` kein zum Zielzeitpunkt passendes Backup findet. (*Geprüft von Reid Thompson, Douglas J Hunley. Vorgeschlagen von Douglas J Hunley.*)

  Zuvor war dies eine leicht zu übersehende Warnung. Dadurch konnte viel Zeit für die Wiederherstellung eines Backups verloren gehen, das das Ziel nicht erreichen kann.

  Issue [#1582](https://github.com/pgbackrest/pgbackrest/issues/1582); Pull Request [#1586](https://github.com/pgbackrest/pgbackrest/pull/1586); Commit [`be4ac39`](https://github.com/pgbackrest/pgbackrest/commit/be4ac3923cb77873da298a30aca5d847b3c635af)
- Protokoll/Port in S3/Azure-Endpunkten ausgewertet. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  `repo-s3-endpoint`, `repo-azure-endpoint` und `repo-storage-host` dürfen nun Protokoll und Port enthalten, etwa `https://host:9000`.

  Issue [#1560](https://github.com/pgbackrest/pgbackrest/issues/1560); Pull Request [#1591](https://github.com/pgbackrest/pgbackrest/pull/1591); Commit [`6a12458`](https://github.com/pgbackrest/pgbackrest/commit/6a12458440168f13cb05d70f36ea54b1860e390c)
- Warnung ergänzen, wenn `checkpoint_timeout` größer als `db-timeout` ist. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Bei `start-fast=n` kann ein Backup während des Wartens auf den Checkpoint das Zeitlimit überschreiten, wenn `checkpoint_timeout` größer als `db-timeout` ist. Das Backup warnt nun in diesem Fall.

  Pull Request [#1564](https://github.com/pgbackrest/pgbackrest/pull/1564); Commit [`6723305`](https://github.com/pgbackrest/pgbackrest/commit/672330593789f07aaad90bbafcd2597cbc602686)
- HTTP-Methode zur HTTP-Fehlerausgabe hinzugefügt. (*Beigetragen von Christoph Berg. Geprüft von David Steele.*)

  Pull Request [#1566](https://github.com/pgbackrest/pgbackrest/pull/1566); Commit [`c38e2d3`](https://github.com/pgbackrest/pgbackrest/commit/c38e2d31709804eb4b9125a15ad84c8fc813f366)
- y/n-Argumente für boolesche Befehlszeilenoptionen zugelassen. (*Beigetragen von Reid Thompson. Geprüft von David Steele.*)

  Pull Request [#1571](https://github.com/pgbackrest/pgbackrest/pull/1571); Commit [`1a0560d`](https://github.com/pgbackrest/pgbackrest/commit/1a0560d363d28737befb8c222647783d4fc2ca29)
- Protokollierung der Backup-Größe exakt an die Ausgabe des Befehls `info` angeglichen. (*Beigetragen von Reid Thompson. Geprüft von David Steele. Vorgeschlagen von Mahomed Hussein.*)

  Die protokollierte Backup-Größe enthält nun nur die kopierten Dateien sowie `backup_label` und `tablespace_map`. Zuvor wurde etwa bei einem inkrementellen Backup nach einem Switchover die Größe aller geprüften Dateien protokolliert.

  [`6e63576`](https://github.com/pgbackrest/pgbackrest/commit/6e635764a66278d5a8c2b4d30b23063bc3923067) Protokollierte Backup-Größe an die von info gemeldete Größe angleichen.; Issue [#766](https://github.com/pgbackrest/pgbackrest/issues/766); Pull Request [#1562](https://github.com/pgbackrest/pgbackrest/pull/1562)

  [`afe77e7`](https://github.com/pgbackrest/pgbackrest/commit/afe77e76e0adf948138d797e227a6f4c7d47c2eb) Beitragsautor für 6e635764 aktualisieren.

  [`1e77fc3`](https://github.com/pgbackrest/pgbackrest/commit/1e77fc3d75490b7a1b6a0b31be9298c995ec672f) Dateigrößen von backup_label und tablespace_map in die Protokollausgabe aufnehmen.; Pull Request [#1568](https://github.com/pgbackrest/pgbackrest/pull/1568)

  [`a3d7a23`](https://github.com/pgbackrest/pgbackrest/commit/a3d7a23a9d90611a3d31947598fbea240b250710) Backup-Größe mit infoBackupDataByLabel() protokollieren.; Pull Request [#1573](https://github.com/pgbackrest/pgbackrest/pull/1573)

  [`dcb4f09`](https://github.com/pgbackrest/pgbackrest/commit/dcb4f09d8315e92c0877b589f3fa9b7f0fa65f93) In 1e77fc3d eingeführte Änderungen an backupFilePut() zurücknehmen.

**Verbesserungen der Dokumentation:**

- Standardwert und zulässige Werte von Größenoptionen mit passenden Einheiten angezeigt. (*Geprüft von Reid Thompson.*)

  [`cff961e`](https://github.com/pgbackrest/pgbackrest/commit/cff961ede7e41fa8035ffe7451a22eb5ea0e46c1) Aufbau von Wertelisten bei der Konfigurationsdarstellung zentralisieren.

  [`038abaa`](https://github.com/pgbackrest/pgbackrest/commit/038abaa71d816cc87b382bd81d3df62ddec9455a) Standardwerte und zulässige Werte von Größenoptionen mit passenden Einheiten anzeigen.; Pull Request [#1557](https://github.com/pgbackrest/pgbackrest/pull/1557)
- Tippfehler korrigiert und Dokumentation zur Option `tablespace-map-all` verbessert. (*Geprüft von Reid Thompson. Vorgeschlagen von Reid Thompson.*)

  Commit [`df89eff`](https://github.com/pgbackrest/pgbackrest/commit/df89eff429e9b8fbc68d9e9895badf9719fd31d2)
- Überholte Aussage zur künftigen Unterstützung mehrerer Repositorys entfernt. (*Vorgeschlagen von David Christensen.*)

  Die Dokumentation gab an, dass nur ein Repository erlaubt sei, obwohl seit v2.33 mehrere Repositorys unterstützt werden.

  Commit [`dea7524`](https://github.com/pgbackrest/pgbackrest/commit/dea752477ab8e812cdbd717eb2091baf3f5d0906)

### v2.36 – Versionshinweise {#v236-release-notes}

*Kleinere Fehlerbehebungen und Verbesserungen*

*Veröffentlicht am 1. November 2021*

**Fehlerbehebungen:**

- "global" als Stanza-Präfix zugelassen. (*Geprüft von Stefan Fercot. Gemeldet von Younes Alhroub.*)

  Ein Stanza-Name, der mit `global` beginnt, etwa `global_stanza`, wurde abgelehnt, weil der Konfigurationsparser ihn als globalen Abschnitt behandelte.

  Issue [#1524](https://github.com/pgbackrest/pgbackrest/issues/1524); Pull Request [#1525](https://github.com/pgbackrest/pgbackrest/pull/1525); Commit [`498902e`](https://github.com/pgbackrest/pgbackrest/commit/498902e885c9d7a44648ccc01b20454094d5b742)
- Segfault bei einer ungültigen GCS-Schlüsseldatei behoben. (*Geprüft von Stephen Frost. Gemeldet von Henrik Feldt.*)

  Eine GCS-Schlüsseldatei ohne Client-E-Mail-Adresse, privaten Schlüssel oder Token-URI verursachte einen Segmentierungsfehler. Nun wird ein Fehler gemeldet.

  Issue [#1536](https://github.com/pgbackrest/pgbackrest/issues/1536); Commit [`2cea005`](https://github.com/pgbackrest/pgbackrest/commit/2cea005f740d640290a9948595f5933833e30e7d)

**Verbesserungen:**

- Erstellung neuer Links durch die Option `link-map` ermöglicht. (*Geprüft von Don Seiler, Stefan Fercot, Chris Bandy. Vorgeschlagen von Don Seiler.*)

  `link-map` konnte bisher nur im Backup vorhandene Links neu zuordnen. Nun kann es für jeden Pfad oder jede Datei im Backup einen neuen Link erstellen.

  [`d89a677`](https://github.com/pgbackrest/pgbackrest/commit/d89a67776cfbb7b3047dbe297cc0c768e5c670e8) Tests für restoreManifestMap() im Unit-Test command/restore refaktorieren.

  [`cf1a575`](https://github.com/pgbackrest/pgbackrest/commit/cf1a57518fe3230886509f59fcec9c9a81e6513c) restoreManifestMap() so refaktorieren, dass link-map den Ablauf steuert.

  [`68c5f3e`](https://github.com/pgbackrest/pgbackrest/commit/68c5f3eaf18fc9bd10fde15a323890bcdcbf4534) Erstellen neuer Links durch link-map ermöglichen.; Issue [#1409](https://github.com/pgbackrest/pgbackrest/issues/1409); Pull Request [#1520](https://github.com/pgbackrest/pgbackrest/pull/1520)
- Höchsten zulässigen Index für die Optionen `pg`/`repo` auf 256 erhöht. (*Geprüft von Cynthia Shang.*)

  Der höchste Index lag bei `pg`-Optionen bei 8 und bei `repo`-Optionen bei 4. Beide erlauben nun 256, etwa `pg256-path`.

  [`02b06aa`](https://github.com/pgbackrest/pgbackrest/commit/02b06aa4957cf3fe64ceb7a44cc1893bff12fe99) Maximalen Index für pg/repo-Optionen auf 256 erhöhen.; Pull Request [#1481](https://github.com/pgbackrest/pgbackrest/pull/1481)

  [`71047a9`](https://github.com/pgbackrest/pgbackrest/commit/71047a9d6d1eea71b3fbd430983541a54049cc69) Mit strncpy() die nach optionName kopierten Zeichen begrenzen.
- Authentifizierung mit `WebIdentity` für AWS S3 hinzugefügt. (*Geprüft von James Callahan, Reid Thompson, Andrew L'Ecuyer. Getestet von Benjamin Blattberg.*)

  Mit `repo-s3-key-type=web-id` werden Anmeldedaten in einer EKS-Umgebung automatisch abgerufen.

  [`cfd8233`](https://github.com/pgbackrest/pgbackrest/commit/cfd823355af2ac99f30c5e1393a121c6dbf622b7) S3-Speichertreiber für zusätzliche Authentifizierungsmethoden refaktorieren.

  [`3879bc6`](https://github.com/pgbackrest/pgbackrest/commit/3879bc69b888daa04d2ca98a2d1219cf22519ddc) WebIdentity-Authentifizierung für AWS S3 hinzufügen.; Issue [#1203](https://github.com/pgbackrest/pgbackrest/issues/1203); Pull Request [#1527](https://github.com/pgbackrest/pgbackrest/pull/1527)

  [`1152f7a`](https://github.com/pgbackrest/pgbackrest/commit/1152f7a7d64e69eed1d9e74b48a308f6c742c28a) Nicht übereinstimmende Parameter im Aufruf von tlsClientNew() korrigieren.
- Option `repo-azure-uri-style` hinzufügen.

  Setzen Sie `repo-azure-uri-style` auf `host` (Standard) oder `path`, um den Azure-URI-Stil auszuwählen. Azurite verwendet hostbasierte URIs, wenn der Endpunkt wie ein mehrteiliger Hostname aussieht.

  Commit [`096829b`](https://github.com/pgbackrest/pgbackrest/commit/096829b3b257444162417662612e80d8cb2ac6ec)
- Fehler bei der Validierung von Backup-Dateien in `backup.info` gemeldet. (*Beigetragen von Stefan Fercot. Geprüft von David Steele.*)

  Während eines Backups erkannte Fehler wie ungültige Seitenprüfsummen wurden bisher nur durch `info` mit `set` angezeigt. Ein Flag in `backup.info` zeigt nun in Text- und JSON-Ausgabe an, dass ein Backup Fehler enthält. Für die Details ist weiterhin `set` erforderlich.

  Issue [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Pull Request [#1508](https://github.com/pgbackrest/pgbackrest/pull/1508); Commit [`34f7873`](https://github.com/pgbackrest/pgbackrest/commit/34f78734325743b4e34cb39224852e6debf49750)
- Startzeit der Recovery zum Wiederherstellungsprotokoll von Online-Backups hinzugefügt. (*Geprüft von Tom Swartz, Stefan Fercot. Vorgeschlagen von Tom Swartz.*)

  Die Wiederherstellung protokolliert nun den Zeitpunkt, ab dem die Recovery beginnt. Dies zeigt, wie viel WAL wiedergegeben werden muss.

  Issue [#1507](https://github.com/pgbackrest/pgbackrest/issues/1507); Pull Request [#1518](https://github.com/pgbackrest/pgbackrest/pull/1518); Commit [`9e79f0e`](https://github.com/pgbackrest/pgbackrest/commit/9e79f0e64b661e944ce2b3897c366feea1544ac2)
- Ursprünglichen Fehler und Wiederholungsversuche beim Fehlschlagen eines lokalen Jobs gemeldet. (*Geprüft von Stefan Fercot.*)

  Scheitert ein lokaler Auftrag nach seinen Wiederholungen, wird nun zuerst der ursprüngliche Fehler mit Stacktrace gemeldet, gefolgt von den Wiederholungsfehlern. Zuvor erschien nur der letzte Fehler, häufig ein Folgefehler wie ein nicht mehr synchrones Protokoll.

  [`136d309`](https://github.com/pgbackrest/pgbackrest/commit/136d309dd4bc1ada9f3d775f036b62292fda390b) Angabe eines Stacktraces für errorInternalThrow() ermöglichen.

  [`ae40ed6`](https://github.com/pgbackrest/pgbackrest/commit/ae40ed6ec9cf77e577518b128518a5763767f589) Parameter jobRetry zu HRN_CFG_LOAD() hinzufügen.

  [`6af827c`](https://github.com/pgbackrest/pgbackrest/commit/6af827cbb1e78cd4c5d649ed4cb24c49a7204b8f) Ursprünglichen Fehler und Wiederholungen beim Scheitern eines lokalen Auftrags melden.; Pull Request [#1521](https://github.com/pgbackrest/pgbackrest/pull/1521)
- Seitenprüfsummenfehler in der Textausgabe von info in Fehlerliste umbenannt. (*Geprüft von Stefan Fercot.*)

  In der Textausgabe von `info` lautet die Bezeichnung nun „error list“ statt „page checksum error“. Eine Datei kann einen Ausrichtungsfehler statt eines Seitenprüfsummenfehlers aufweisen.

  Pull Request [#1519](https://github.com/pgbackrest/pgbackrest/pull/1519); Commit [`9346895`](https://github.com/pgbackrest/pgbackrest/commit/9346895f5b61627b50d431f09447e08d8a50caa8)
- Hinweise zur Meldung über eine Zeitüberschreitung bei der WAL-Wiedergabe auf dem Standby hinzugefügt. (*Geprüft von Cynthia Shang, Stefan Fercot. Vorgeschlagen von Leigh Downs.*)

  Bei einer Zeitüberschreitung beim Warten auf die WAL-Wiedergabe des Standbys erscheinen nun Hinweise, die laufende Replikation zu prüfen und `backup-standby` für ein Backup vom Primärserver zu deaktivieren.

  Issue [#1434](https://github.com/pgbackrest/pgbackrest/issues/1434); Commit [`b7ef12a`](https://github.com/pgbackrest/pgbackrest/commit/b7ef12a76f219881d0b24c715592af96fe5c9b8f)

**Fehlerbehebungen in der Dokumentation:**

- Falschen Hostnamen im Benutzerhandbuch korrigieren. (*Behoben von Reid Thompson. Geprüft von David Steele.*)

  Die Replikationskonfiguration verwendete in `pg_hba.conf` die IP-Adresse von pg-primary statt der von pg-standby.

  Pull Request [#1544](https://github.com/pgbackrest/pgbackrest/pull/1544); Commit [`1cb8ae1`](https://github.com/pgbackrest/pgbackrest/commit/1cb8ae15de5b4276682bdd9825ca97012cd43855)

**Verbesserungen der Dokumentation:**

- Optionsdokumentation verbessern.

  Die Hilfe zu `buffer-size` beschreibt nun alle Vorgänge, die die Option verwenden. Die Beschreibungen von `cmd-ssh`, `repo-host-cmd` und `pg-host-cmd` wurden vereinheitlicht. `archive-header-check` wurde in den Archivabschnitt der Konfigurationsreferenz verschoben.

  [`3763624`](https://github.com/pgbackrest/pgbackrest/commit/376362475e3b3b13b70313d9002d4ff8b25b4b40) archive-header-check in den Archivabschnitt der Referenz verschieben.

  [`e1f6c06`](https://github.com/pgbackrest/pgbackrest/commit/e1f6c066b3da11fd21b1155c90370c3fa2da06b7) Dokumentation für buffer-size verbessern.

  [`fa564ee`](https://github.com/pgbackrest/pgbackrest/commit/fa564ee1969229b5cf60d2479d8ace85325f4db3) Dokumentation für cmd-ssh, repo-host-cmd und pg-host-cmd verbessern.

### v2.35 – Versionshinweise {#v235-release-notes}

*Binärprotokoll*

*Veröffentlicht am 23. August 2021*

**WICHTIGER HINWEIS**: Die Protokollierungsstufe für kopierte Dateien in den Befehlen `backup`/`restore` wurde auf `detail` geändert. Dies reduziert die Ausgabemenge auf der Stufe `info`. Falls diese Meldungen benötigt werden, setzen Sie die Protokollierungsstufe für die Befehle `backup`/`restore` auf `detail`

**Fehlerbehebungen:**

- Fehler beim Abschließen mehrteiliger S3-Uploads erkannt. (*Geprüft von Cynthia Shang. Getestet von Marco Montagna. Gemeldet von Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)

  Der Abschluss eines mehrteiligen Uploads kann fehlschlagen, obwohl S3 einen HTTP-Erfolg meldet. Eine Antwort ohne `ETag` gilt nun als Fehler, und der Auftrag wird wiederholt.

  [`8e1807c`](https://github.com/pgbackrest/pgbackrest/commit/8e1807cdbe08a6e059ff79220247cf4b3c058979) Fehler beim Abschluss mehrteiliger S3-Uploads erkennen.; Issue [#1116](https://github.com/pgbackrest/pgbackrest/issues/1116); Issue [#1290](https://github.com/pgbackrest/pgbackrest/issues/1290); Issue [#1433](https://github.com/pgbackrest/pgbackrest/issues/1433); Pull Request [#1438](https://github.com/pgbackrest/pgbackrest/pull/1438)

  [`25508a4`](https://github.com/pgbackrest/pgbackrest/commit/25508a48e0d3b0a3eabc6d1fe858b9c3dc12dc86) In 8e187cdb fehlende Beitragsautoren ergänzen.
- Erkennung zyklischer symbolischer Links korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Rohit Raveendran.*)

  Links wurden vor ihrer Prüfung verfolgt. Ein zyklischer Link führte deshalb bei der Manifesterstellung zu endloser Rekursion und einem Absturz.

  Issue [#1447](https://github.com/pgbackrest/pgbackrest/issues/1447); Pull Request [#1452](https://github.com/pgbackrest/pgbackrest/pull/1452); Commit [`43b8746`](https://github.com/pgbackrest/pgbackrest/commit/43b874628c86ec4fe297dbd5cab5bd3f62b8639b)
- Nur ausgewählte Optionen `repo` an die Gegenstelle übergeben. (*Geprüft von David Christensen, Cynthia Shang. Gemeldet von Greg Sabino Mullane, David Christensen.*)

  Optionen für andere Repositorys konnten auf dem entfernten Host Konflikte auslösen, da dieser genau ein Repository verwendet.

  Pull Request [#1480](https://github.com/pgbackrest/pgbackrest/pull/1480); Commit [`935de1e`](https://github.com/pgbackrest/pgbackrest/commit/935de1e7a06d60415c16cad137875b49346337c6)

**Verbesserungen:**

- Binärprotokoll. (*Geprüft von Cynthia Shang.*)

  Lokale und entfernte Prozesse kommunizieren nun im binären Pack-Format statt in JSON. Packs sind kompakter, schneller zu erzeugen und auszuwerten sowie streng typisiert. Jede Nachricht wird an einer einzigen Stelle geschrieben, wodurch ein Fehler das Protokoll seltener in einem ungültigen Zustand zurücklässt. Nachrichten haben keine Größenbegrenzung.

  [`6a1c033`](https://github.com/pgbackrest/pgbackrest/commit/6a1c0337ddee9900dda58b7d2fa74d82c0586ed2) Binärprotokoll.; Pull Request [#1424](https://github.com/pgbackrest/pgbackrest/pull/1424)

  [`2d5cbfc`](https://github.com/pgbackrest/pgbackrest/commit/2d5cbfc73142fa99df609aa23b64db5342e73c88) Durch das Binärprotokoll in 6a1c0337 eingeführte Speicherlecks beheben.

  [`f716cb6`](https://github.com/pgbackrest/pgbackrest/commit/f716cb6f4f9765baa03f71b5563786d79d9f04a2) Durch das Binärprotokoll in 6a1c0337 eingeführten Zugriff auf freigegebenen Speicher beheben.

  [`4fb6384`](https://github.com/pgbackrest/pgbackrest/commit/4fb6384f10f6cd26c422ab9b24feb5ae0ebeeee9) Weitere durch das Binärprotokoll in 6a1c0337 eingeführte Speicherlecks beheben.
- Datenverzeichnis bei `restore` automatisch erstellt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Chris Bandy.*)

  Eine aus Perl übernommene Prüfung verhinderte, dass die Wiederherstellung das Datenverzeichnis anlegte.

  Issue [#1445](https://github.com/pgbackrest/pgbackrest/issues/1445); Pull Request [#1454](https://github.com/pgbackrest/pgbackrest/pull/1454); Commit [`056a307`](https://github.com/pgbackrest/pgbackrest/commit/056a3070e0dba299389c7b5049878d40dd91ec9a)
- `restore` mit `--type=lsn` ermöglicht. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang. Vorgeschlagen von James Coleman.*)

  Setzen Sie für eine Wiederherstellung bis zu einem LSN unter PostgreSQL >= 10 `type=lsn` und den LSN in `target`.

  Issue [#1339](https://github.com/pgbackrest/pgbackrest/issues/1339); Pull Request [#1462](https://github.com/pgbackrest/pgbackrest/pull/1462); Commit [`563d117`](https://github.com/pgbackrest/pgbackrest/commit/563d117967ab9770f9f646c6186d0bc37121611f)
- Protokollierungsstufe für durch `backup`/`restore` kopierte Dateien auf detail geändert. (*Geprüft von Stefan Fercot. Vorgeschlagen von Jens Wilke.*)

  Dadurch wird die Protokollstufe `info` weniger ausführlich. Mit `detail` wird jede kopierte Datei angezeigt.

  Issue [#1277](https://github.com/pgbackrest/pgbackrest/issues/1277); Pull Request [#1455](https://github.com/pgbackrest/pgbackrest/pull/1455); Commit [`849ab34`](https://github.com/pgbackrest/pgbackrest/commit/849ab343aa10d66fbbd27cad407eff981c186d06)
- In einer Schleife gewartet, bis die Checkpoint-LSN die Wiedergabe-LSN erreicht. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Vorgeschlagen von Fatih Mencutekin.*)

  Auf einem Standby kann der Checkpoint-LSN dem Replay-LSN etwas hinterherhinken, bis `pg_control` aktualisiert ist. Das Backup prüft nun weiter, statt fehlzuschlagen.

  Issue [#1450](https://github.com/pgbackrest/pgbackrest/issues/1450); Pull Request [#1460](https://github.com/pgbackrest/pgbackrest/pull/1460); Commit [`8fac1ac`](https://github.com/pgbackrest/pgbackrest/commit/8fac1ac50d28557d162fbb251fbbdcc3c9fb950c)
- Gesamte Dateianzahl bei `backup` und gesamte Größe/Dateianzahl bei `restore` protokolliert. (*Geprüft von Cynthia Shang.*)

  Die Backup-Größe wird nun am Ende protokolliert und enthält auch nach dem Hauptkopiervorgang zum Manifest hinzugefügte Dateien wie `backup_label` und WAL. Die Wiederherstellung protokolliert nun ebenfalls Größe und Gesamtzahl der Dateien.

  Pull Request [#1489](https://github.com/pgbackrest/pgbackrest/pull/1489); Commit [`a0bdfa4`](https://github.com/pgbackrest/pgbackrest/commit/a0bdfa436c9e1c2723be905ebe5cef7809a26244)

**Fehlerbehebungen in der Dokumentation:**

- Falsche Hostnamen im Benutzerhandbuch korrigiert. (*Geprüft von Stefan Fercot. Gemeldet von Greg Sabino Mullane.*)

  Einige Beispiele zeigten `pg1` statt des Hostnamens. Der Installationsblock installierte Pakete unabhängig vom angegebenen Host auf dem Build-Host.

  Pull Request [#1479](https://github.com/pgbackrest/pgbackrest/pull/1479); Commit [`155ef85`](https://github.com/pgbackrest/pgbackrest/commit/155ef85013088a1150a4c15b04af36420d06e9c3)

**Verbesserungen der Dokumentation:**

- Dokumentation für Mitwirkende aktualisiert und Vorlage für Pull Requests hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Der Beitragsleitfaden enthält nun ein Inhaltsverzeichnis sowie Abschnitte zum Verstehen der Testausgabe und zum Einreichen eines Pull Requests. GitHub zeigt für neue Pull Requests nun eine Vorlage.

  [`e3d05e2`](https://github.com/pgbackrest/pgbackrest/commit/e3d05e2b4aa80149219b6d49a3136b34fa268127) Beitragsdokumentation aktualisieren und Pull-Request-Vorlage hinzufügen.; Pull Request [#1469](https://github.com/pgbackrest/pgbackrest/pull/1469)

  [`71b654f`](https://github.com/pgbackrest/pgbackrest/commit/71b654fc29497319862fe01c3917bbc353cc6dd9) Links korrigieren und Kindprozessbeispiel aktualisieren.; Pull Request [#1487](https://github.com/pgbackrest/pgbackrest/pull/1487)
- Backup-Dokumentation im Benutzerhandbuch neu angeordnet. (*Geprüft von Cynthia Shang.*)

  Die Abschnitte „Option für schnellen Start“ und „Archivzeitlimit“ wurden nach „Schnellstart – Backup ausführen“ verschoben. Der Abschnitt „Option für automatisches Stoppen“, der nur PostgreSQL <= 9.6 betrifft, wurde entfernt.

  Pull Request [#1488](https://github.com/pgbackrest/pgbackrest/pull/1488); Commit [`6ab18dc`](https://github.com/pgbackrest/pgbackrest/commit/6ab18dc0fa42885aea8eb9405ab0a943c2d49a71)
- Verhalten von `restore` mit `--type` in der Befehlsreferenz erläutert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Die Referenz stellt nun klar, dass `set` angegeben werden muss, wenn das Ziel vor dem letzten Backup liegt und `type` nicht `time` ist.

  Commit [`a6691c6`](https://github.com/pgbackrest/pgbackrest/commit/a6691c6f615f90195aeb6c1c6657a6afd79a10d3)
- Tippfehler in Dokumentation und Kommentaren korrigiert. (*Beigetragen von Eric Radman. Geprüft von David Steele.*)

  Pull Request [#1446](https://github.com/pgbackrest/pgbackrest/pull/1446); Commit [`23bdc3d`](https://github.com/pgbackrest/pgbackrest/commit/23bdc3deb62a622713064df3b0777110ebba8723)

**Verbesserungen der Testsuite:**

- Prüfung auf einen Testpfad innerhalb des Repository-Pfads hinzugefügt. (*Geprüft von Greg Sabino Mullane. Vorgeschlagen von Greg Sabino Mullane.*)

  Ein Testpfad innerhalb des Repository-Pfads verursachte seltsame Fehler, da das Repository in den Testpfad kopiert wird. `test.pl` meldet nun in diesem Fall einen Fehler.

  Issue [#1472](https://github.com/pgbackrest/pgbackrest/issues/1472); Pull Request [#1474](https://github.com/pgbackrest/pgbackrest/pull/1474); Commit [`e32f9e1`](https://github.com/pgbackrest/pgbackrest/commit/e32f9e146b11389e3d16feba9665360b73737d66)
- Statische Codeanalyse mit CodeQL hinzugefügt. (*Geprüft von Cynthia Shang.*)

  CodeQL läuft nun in der CI. Die gefundenen Probleme wurden behoben; etwa wurden `gmtime()`/`localtime()` durch `gmtime_r()`/`localtime_r()` ersetzt.

  Pull Request [#1457](https://github.com/pgbackrest/pgbackrest/pull/1457); Commit [`3c8819e`](https://github.com/pgbackrest/pgbackrest/commit/3c8819e10f9eff89195566e7e02f349373f5c4c7)
- Tests auf Standardmuster umgestellt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  [`3f9fbc3`](https://github.com/pgbackrest/pgbackrest/commit/3f9fbc3c24eab48e7ae2871484ea01273049e601) Tests für command/expire an die Standardmuster anpassen.; Pull Request [#1420](https://github.com/pgbackrest/pgbackrest/pull/1420)

  [`03021c6`](https://github.com/pgbackrest/pgbackrest/commit/03021c6a17f1374e84ef42614fa1dd2a6be4b64d) Tests für command/stanza an die Standardmuster anpassen.; Pull Request [#1426](https://github.com/pgbackrest/pgbackrest/pull/1426)

  [`8dd882b`](https://github.com/pgbackrest/pgbackrest/commit/8dd882badee76b038dc8b494a1112eb3e18ef678) Tests für info/infoArchive an die Standardmuster anpassen.; Pull Request [#1436](https://github.com/pgbackrest/pgbackrest/pull/1436)

  [`ff95edd`](https://github.com/pgbackrest/pgbackrest/commit/ff95eddc369597c76a9ea70ffbada493ed4d1951) Tests für command/verify an die Standardmuster anpassen.; Pull Request [#1435](https://github.com/pgbackrest/pgbackrest/pull/1435)

  [`17c9ed0`](https://github.com/pgbackrest/pgbackrest/commit/17c9ed0ef0380fb14fba9a5299b6618ca8c92c2e) Tests für command/info an die Standardmuster anpassen.; Pull Request [#1432](https://github.com/pgbackrest/pgbackrest/pull/1432)

  [`bffb43e`](https://github.com/pgbackrest/pgbackrest/commit/bffb43ea3fe00f445a2fc3c44a07f105cee65b4b) Tests für command/check an die Standardmuster anpassen.; Pull Request [#1431](https://github.com/pgbackrest/pgbackrest/pull/1431)

  [`fb2d111`](https://github.com/pgbackrest/pgbackrest/commit/fb2d111dcd75021313a64a348959482339bf7f2a) Tests für info/infoBackup an die Standardmuster anpassen.; Pull Request [#1437](https://github.com/pgbackrest/pgbackrest/pull/1437)

  [`065a8c8`](https://github.com/pgbackrest/pgbackrest/commit/065a8c8454d2acdd72c0c71a24d6b8bc09669e18) Defines in Unit-Tests durch Zeichenkettenkonstanten ersetzen.; Pull Request [#1440](https://github.com/pgbackrest/pgbackrest/pull/1440)

  [`c620811`](https://github.com/pgbackrest/pgbackrest/commit/c6208113bfce9d637ca3fd0b35ab28a819c1a83e) Parameter timeModified zum Makro HRN_STORAGE_PUT() hinzufügen.

  [`6a90d46`](https://github.com/pgbackrest/pgbackrest/commit/6a90d469094ee2697ae4c932349756a54136799d) Tests für info/manifest an die Standardmuster anpassen.; Pull Request [#1444](https://github.com/pgbackrest/pgbackrest/pull/1444)

  [`62e8d97`](https://github.com/pgbackrest/pgbackrest/commit/62e8d97af03e7628d5710b17aad1cc31f83d7e69) Tests für command/archive an die Standardmuster anpassen.; Pull Request [#1449](https://github.com/pgbackrest/pgbackrest/pull/1449)

  [`8bb0b28`](https://github.com/pgbackrest/pgbackrest/commit/8bb0b28455d59ef884eab7ab25a91f988adbab81) Tests für command/control und command/command an die Standardmuster anpassen.; Pull Request [#1456](https://github.com/pgbackrest/pgbackrest/pull/1456)

  [`f2ec4e0`](https://github.com/pgbackrest/pgbackrest/commit/f2ec4e00a4c4c388a8f1b094381fd566a3dc9aa7) Verschlüsselungsparameter zum Makro TEST_STORAGE_GET() hinzufügen.

  [`4ad0bbd`](https://github.com/pgbackrest/pgbackrest/commit/4ad0bbda53b34688146f14d130cf0e53c8dd650f) Tests für command/backup an die Standardmuster anpassen.; Pull Request [#1463](https://github.com/pgbackrest/pgbackrest/pull/1463)

  [`117ffe8`](https://github.com/pgbackrest/pgbackrest/commit/117ffe88965fd60ce3dcb328e9d28503870af05a) Tests für command/help an die Standardmuster anpassen.; Pull Request [#1464](https://github.com/pgbackrest/pgbackrest/pull/1464)

  [`ebe5848`](https://github.com/pgbackrest/pgbackrest/commit/ebe5848494d4e37a9c86f1fafb5b3453c1f425a6) Tests für command/local und command/remote an die Standardmuster anpassen.; Pull Request [#1466](https://github.com/pgbackrest/pgbackrest/pull/1466)

  [`a6cdf5b`](https://github.com/pgbackrest/pgbackrest/commit/a6cdf5b22f0eed53f33bbd84478af0542c81af7d) Tests für command/repo an die Standardmuster anpassen.; Pull Request [#1467](https://github.com/pgbackrest/pgbackrest/pull/1467)

  [`4992508`](https://github.com/pgbackrest/pgbackrest/commit/49925087644c76df005828eb27c24f503a09b20b) Tests für command/restore an die Standardmuster anpassen.; Pull Request [#1468](https://github.com/pgbackrest/pgbackrest/pull/1468)

  [`4c9ddf5`](https://github.com/pgbackrest/pgbackrest/commit/4c9ddf5ef25d0f441e20e918f57c1ec79218cfdb) Tests für storage an die Standardmuster anpassen.; Pull Request [#1470](https://github.com/pgbackrest/pgbackrest/pull/1470)

  [`eeaab6a`](https://github.com/pgbackrest/pgbackrest/commit/eeaab6a3d192fc788c0f74aadbf4b3de5da52531) config-Tests (außer parse) an die Standardmuster anpassen.; Pull Request [#1473](https://github.com/pgbackrest/pgbackrest/pull/1473)

  [`f653b59`](https://github.com/pgbackrest/pgbackrest/commit/f653b59664e757a0e3da63cc8462deafe2d9e0ef) Tests für db/db an die Standardmuster anpassen.; Pull Request [#1486](https://github.com/pgbackrest/pgbackrest/pull/1486)

  [`e17865a`](https://github.com/pgbackrest/pgbackrest/commit/e17865a03a5451b82a101557d400ff223d104383) Tests für protocol/protocol an die Standardmuster anpassen.; Pull Request [#1491](https://github.com/pgbackrest/pgbackrest/pull/1491)

  [`eca2fc6`](https://github.com/pgbackrest/pgbackrest/commit/eca2fc69589cd44f7c1a43206553984adde5cfb1) Tests für config/parse an die Standardmuster anpassen.; Pull Request [#1492](https://github.com/pgbackrest/pgbackrest/pull/1492)

### v2.34 – Versionshinweise {#v234-release-notes}

*Unterstützung für PostgreSQL 14*

*Veröffentlicht am 7. Juni 2021*

**Fehlerbehebungen:**

- Probleme mit übrig gebliebenen Spool-Dateien aus einem vorherigen `restore` behoben. (*Geprüft von Cynthia Shang, Stefan Fercot. Getestet von Floris van Nee. Gemeldet von Floris van Nee.*)

  Eine im Spool-Pfad verbliebene Meldung einer früheren Wiederherstellung konnte `archive-get` ein WAL-Segment als fehlend melden lassen. Wird die Meldung bei der ersten Prüfung gefunden, wird sie nun entfernt und der asynchrone Prozess erneut gestartet. Antwortet dieser nicht, wird ein Fehler gemeldet, statt das WAL-Segment als fehlend auszugeben.

  Issue [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Pull Request [#1371](https://github.com/pgbackrest/pgbackrest/pull/1371); Commit [`f45e76f`](https://github.com/pgbackrest/pgbackrest/commit/f45e76fa2e8ce0f62317a74fdd51083d52659cd5)
- Problem beim Prüfen von Links bei einer großen Anzahl von Tablespaces behoben. (*Geprüft von Cynthia Shang. Getestet von Avinash Vallarapu. Gemeldet von Avinash Vallarapu.*)

  Die Linkprüfung verbrauchte bei vielen Tablespaces viel Speicher und konnte abstürzen. Die neue Prüfung ist deutlich schneller, benötigt wesentlich weniger Speicher und erkennt außerdem doppelte Dateilinks.

  Issue [#1354](https://github.com/pgbackrest/pgbackrest/issues/1354); Pull Request [#1356](https://github.com/pgbackrest/pgbackrest/pull/1356); Commit [`eba013b`](https://github.com/pgbackrest/pgbackrest/commit/eba013b49b850e53d59795ac6358fcb3381048a3)
- Nicht mehr benötigte entfernte Verbindungen freigegeben, damit sie während `restore` keine Zeitüberschreitung verursachen. (*Geprüft von Cynthia Shang. Gemeldet von Francisco Miguel Biete Banon.*)

  Verbindungen zu entfernten Hosts blieben während der gesamten Wiederherstellung geöffnet und konnten ablaufen. Am Ende langer Wiederherstellungen erschien dadurch eine harmlose, aber störende Warnung. Nun werden sie nach dem Laden des Manifests geschlossen.

  Issue [#1368](https://github.com/pgbackrest/pgbackrest/issues/1368); Pull Request [#1374](https://github.com/pgbackrest/pgbackrest/pull/1374); Commit [`06fa185`](https://github.com/pgbackrest/pgbackrest/commit/06fa18582a405417c8ab4ba667cb01a13a5c3103)
- `help` korrigiert, wenn eine gültige Option für den angegebenen Befehl ungültig ist. (*Geprüft von Stefan Fercot. Gemeldet von Cynthia Shang.*)

  `help` verursachte einen Segmentierungsfehler, wenn Hilfe zu einer für den Befehl ungültigen Option angefordert wurde.

  Pull Request [#1375](https://github.com/pgbackrest/pgbackrest/pull/1375); Commit [`45f8355`](https://github.com/pgbackrest/pgbackrest/commit/45f83558ea862c6f496a27b886e1160e6303bbe8)

**Funktionen:**

- Unterstützung für PostgreSQL 14 hinzugefügt. (*Geprüft von Cynthia Shang.*)

  PostgreSQL 14 erfordert gegenüber PostgreSQL 13 keine Codeänderungen. Die Katalogversion kann sich nun während der Beta-/RC-Phase von PostgreSQL ändern, ohne eine neue pgBackRest-Version zu benötigen.

  Pull Request [#1413](https://github.com/pgbackrest/pgbackrest/pull/1413); Commit [`2452c4d`](https://github.com/pgbackrest/pgbackrest/commit/2452c4d5a4c230b8e3c33d3bddf69e56dfbec284)
- Automatische GCS-Authentifizierung für GCE-Instanzen hinzugefügt. (*Geprüft von Jan Wieck. Getestet von Daniel Farina.*)

  Mit `repo-gcs-key-type=auto` wird das Authentifizierungstoken aus den Instanzmetadaten einer GCE-Instanz bezogen.

  [`7b71604`](https://github.com/pgbackrest/pgbackrest/commit/7b71604defa02d5ed9b7aa3407961cb59a52cc45) Vorhandene Variable für den Port des GCS-Testservers verwenden.

  [`26fefa6`](https://github.com/pgbackrest/pgbackrest/commit/26fefa6aeeae90bbb572ea57b605fb8fe526f1a0) Auswertung der GCS-Tokenantwort in eine eigene Funktion auslagern.

  [`9af0331`](https://github.com/pgbackrest/pgbackrest/commit/9af033194abc4b1cd3f06c3a97fff71c966c3827) Automatische GCS-Authentifizierung für GCE-Instanzen hinzufügen.; Pull Request [#1395](https://github.com/pgbackrest/pgbackrest/pull/1395)
- Option `repo-retention-history` zum Entfernen abgelaufener Backup-Historien hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang, David Steele.*)

  Legen Sie fest, wie viele Tage Backup-Historie aufbewahrt werden. Standardmäßig bleibt die gesamte Historie erhalten. Die Historie noch im Repository vorhandener Backups wird niemals entfernt. Läuft das Manifest eines vollständigen Backups ab, gilt dies auch für die Manifeste seiner differenziellen und inkrementellen Backups.

  Pull Request [#1389](https://github.com/pgbackrest/pgbackrest/pull/1389); Commit [`5b332b2`](https://github.com/pgbackrest/pgbackrest/commit/5b332b22b508d896abb64fa6abe26c78c83a29bc)
- Option `db-exclude` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang.*)

  Die Wiederherstellung schließt die angegebenen Datenbanken aus, indem sie sie als mit Nullen gefüllte Sparse-Dateien schreibt. PostgreSQL kann weiterhin die Recovery durchführen; anschließend lassen sich die Datenbanken löschen. Bei `db-include` gilt `db-exclude` nur für die Systemdatenbanken `template0`, `template1` und `postgres`.

  Issue [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Pull Request [#1337](https://github.com/pgbackrest/pgbackrest/pull/1337); Commit [`292f836`](https://github.com/pgbackrest/pgbackrest/commit/292f836f1243e51d102bb4be202e7b21a7a386b1)

**Verbesserungen:**

- Protokollierung beim Entfernen abgelaufener Archivdaten von der Stufe detail auf info geändert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Pull Request [#1416](https://github.com/pgbackrest/pgbackrest/pull/1416); Commit [`aceb956`](https://github.com/pgbackrest/pgbackrest/commit/aceb956815a87f0c19ea171de25d2c3842a6d806)
- Archiv-Spool-Pfad der Stanza bei `restore` entfernt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)

  Dateien im Spool-Pfad konnten den neuen Cluster beeinträchtigen. Alte `archive-push`-Bestätigungen konnten beispielsweise dazu führen, dass WAL nicht archiviert wurde.

  Issue [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Pull Request [#1386](https://github.com/pgbackrest/pgbackrest/pull/1386); Commit [`320c6e1`](https://github.com/pgbackrest/pgbackrest/commit/320c6e1aad2cc9a8dabecb2bc91a9b34464de6ec)
- Beim Kopieren für `backup` Dateien nicht atomar geschrieben und Pfade nicht synchronisiert. (*Geprüft von Stephen Frost, Stefan Fercot, Cynthia Shang.*)

  Atomare Schreibvorgänge sind nicht nötig, da beim Fortsetzen eines fehlgeschlagenen Backups die Prüfsummen geprüft und am Backup-Ende alle Pfade synchronisiert werden.

  Pull Request [#1373](https://github.com/pgbackrest/pgbackrest/pull/1373); Commit [`aa72c19`](https://github.com/pgbackrest/pgbackrest/commit/aa72c19a831fb0dd15a50a003fbaad427f335353)

**Verbesserungen der Dokumentation:**

- Dokumentation für Mitwirkende aktualisiert. (*Beigetragen von Cynthia Shang. Geprüft von David Steele, Stefan Fercot.*)

  Der Beitragsleitfaden enthält mehr Beispiele zum Schreiben von Code, Hinzufügen von Konfigurationsoptionen und Testen.

  Pull Request [#1400](https://github.com/pgbackrest/pgbackrest/pull/1400); Commit [`68faf14`](https://github.com/pgbackrest/pgbackrest/commit/68faf1482a42ea14f5b00a91e19bd5aedec275b8)
- RHEL/CentOS-Benutzerhandbuch zu einem einzigen Dokument zusammengeführt. (*Geprüft von Cynthia Shang.*)

  Das zweite Handbuch diente hauptsächlich zur Dokumentation von `stop-auto` für PostgreSQL <= 9.5, dessen Support inzwischen beendet ist. Die Option bleibt in der Referenz dokumentiert.

  Pull Request [#1405](https://github.com/pgbackrest/pgbackrest/pull/1405); Commit [`ccac75e`](https://github.com/pgbackrest/pgbackrest/commit/ccac75e7de8754b39bb691ff8830a2839ea7a285)
- Klargestellt, dass `repo-s3-role` kein `ARN` ist. (*Beigetragen von Isaac Yuen. Geprüft von David Steele.*)

  Pull Request [#1365](https://github.com/pgbackrest/pgbackrest/pull/1365); Commit [`5bf1606`](https://github.com/pgbackrest/pgbackrest/commit/5bf160643b53699a28a8f0920c36d6ded767d249)

### v2.33 – Versionshinweise {#v233-release-notes}

*Unterstützung für mehrere Repositorys und GCS*

*Veröffentlicht am 5. April 2021*

**Fehlerbehebungen:**

- Optionswarnungen korrigiert, die asynchrones `archive-get`/`archive-push` störten. (*Geprüft von Cynthia Shang. Gemeldet von Lev Kokotov.*)

  Eine Optionswarnung im asynchronen Prozess wurde auf das geschlossene stdout geschrieben und ließ den Prozess abbrechen. Da für die asynchrone Rolle nun andere Optionen gültig sein können als für die Standardrolle, trat dies häufiger auf. Optionswarnungen werden nun nur für die Standardrolle protokolliert.

  Issue [#1299](https://github.com/pgbackrest/pgbackrest/issues/1299); Pull Request [#1301](https://github.com/pgbackrest/pgbackrest/pull/1301); Commit [`3837e61`](https://github.com/pgbackrest/pgbackrest/commit/3837e61a7504b1e211e4b3a70cbe97343c1cf2e6)
- Speicherleck beim Kopieren des Archivs während des Backups behoben. (*Geprüft von Cynthia Shang. Gemeldet von Christian ROUX, Efremov Egor.*)

  Das Kopieren von WAL in das Backup mit `archive-copy` verursachte ein Speicherleck, besonders wenn WAL neu komprimiert werden musste.

  Issue [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Commit [`778adbf`](https://github.com/pgbackrest/pgbackrest/commit/778adbf19f71ceb90071f01197bf189d59b14df0)
- Stack-Überlauf bei der Erzeugung der Verschlüsselungspassphrase behoben. (*Geprüft von Cynthia Shang. Gemeldet von bsiara.*)

  Der Puffer für die erzeugte Passphrase hatte keinen Platz für das abschließende Nullbyte. Dies wurde auf arm64 mit musl libc entdeckt.

  Issue [#1294](https://github.com/pgbackrest/pgbackrest/issues/1294); Pull Request [#1295](https://github.com/pgbackrest/pgbackrest/pull/1295); Commit [`d29855b`](https://github.com/pgbackrest/pgbackrest/commit/d29855bd0bf8b957fa8c06445d22e425c443a704)
- `repo-ls` mit `/` auf S3-Repositorys korrigiert. (*Geprüft von Cynthia Shang. Gemeldet von Lesovsky Alexey.*)

  S3 meldet `/` als Datei ohne die erwarteten Header, was einen Fehler verursachte. Bei Speicher ohne Pfadunterstützung wird `/` nun als nicht vorhanden gemeldet.

  Issue [#1317](https://github.com/pgbackrest/pgbackrest/issues/1317); Pull Request [#1336](https://github.com/pgbackrest/pgbackrest/pull/1336); Commit [`b1d945e`](https://github.com/pgbackrest/pgbackrest/commit/b1d945ebb774c25676155af439b0558e8582bbe5)

**Funktionen:**

- Unterstützung für mehrere Repositorys. (*Beigetragen von Cynthia Shang, David Steele. Geprüft von Stefan Fercot, Stephen Frost.*)

  Bis zu vier Repositorys können konfiguriert werden, etwa ein lokales für schnelle Wiederherstellungen und ein entferntes für Redundanz. `archive-push` überträgt WAL an alle Repositorys; Backups werden für jedes Repository geplant. Manche Befehle arbeiten mit allen Repositorys, andere benötigen `repo`. Ist nur `repo1` konfiguriert, ist `repo` nicht erforderlich.

  [`3408f1e`](https://github.com/pgbackrest/pgbackrest/commit/3408f1ee2ee3f774699a15de045e0afe3eaf9a26) Unterstützung mehrerer Repositorys in expire verbessern.; Pull Request [#1289](https://github.com/pgbackrest/pgbackrest/pull/1289)

  [`e28f6f1`](https://github.com/pgbackrest/pgbackrest/commit/e28f6f11e97a80e9c1adf1a6eaeeabbfc991914f) expire nach einem Fehler beim Verarbeiten eines Repositorys fortsetzen.; Pull Request [#1308](https://github.com/pgbackrest/pgbackrest/pull/1308)

  [`bec3e20`](https://github.com/pgbackrest/pgbackrest/commit/bec3e20b2cb061ef0413df24234ebe246ea53063) Unterstützung mehrerer Repositorys zu archive-get hinzufügen.; Pull Request [#1292](https://github.com/pgbackrest/pgbackrest/pull/1292)

  [`118d9e6`](https://github.com/pgbackrest/pgbackrest/commit/118d9e64fea71c2e049b52802e55f72f5793871b) Unterstützung mehrerer Repositorys in restore verbessern.; Pull Request [#1300](https://github.com/pgbackrest/pgbackrest/pull/1300)

  [`065b2ff`](https://github.com/pgbackrest/pgbackrest/commit/065b2ff2300a9f06a8c32621fac521451ca942bd) repoMin/Max im Befehl info refaktorieren.

  [`0ddc038`](https://github.com/pgbackrest/pgbackrest/commit/0ddc0380ff408f9ed6e8bcd4d328df500681ce77) Standard-Repository für restore aus den Integrationstests entfernen.

  [`13dc8e6`](https://github.com/pgbackrest/pgbackrest/commit/13dc8e68d74fa9e06180e67b7e59994767b4a34d) --repo für backup optional machen.; Pull Request [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`a1280c4`](https://github.com/pgbackrest/pgbackrest/commit/a1280c41e530500e5bbde73a900683f6db207686) Warnungen von archive-push an das Verhalten von archive-get angleichen.

  [`3b8f0ef`](https://github.com/pgbackrest/pgbackrest/commit/3b8f0ef7ae8a81ae969934fff4ad3da299454b24) Fehlertoleranz beim Schreiben zu archive-push hinzufügen.; Pull Request [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`95063f6`](https://github.com/pgbackrest/pgbackrest/commit/95063f6812279cd59380fd72e16e67b631582bd0) --repo für alle übrigen Befehle außer stanza-delete optional machen.

  [`1dbb3bf`](https://github.com/pgbackrest/pgbackrest/commit/1dbb3bf50b94dcc9d53dfe1e5ad57a17bd6d38e8) Unterstützung mehrerer Repositorys.; Pull Request [#1227](https://github.com/pgbackrest/pgbackrest/pull/1227)

  [`31c7824`](https://github.com/pgbackrest/pgbackrest/commit/31c7824a4d84cbf5a0ba0938f4caa546fa67af0a) Entfernte Ausführung von stanza-*-Befehlen ermöglichen.; Pull Request [#1326](https://github.com/pgbackrest/pgbackrest/pull/1326)

  [`2789d3b`](https://github.com/pgbackrest/pgbackrest/commit/2789d3b6206c4de9299a3bc459e04cdab793abc9) Fehlertoleranz von info verbessern.; Pull Request [#1342](https://github.com/pgbackrest/pgbackrest/pull/1342)

  [`01b8e22`](https://github.com/pgbackrest/pgbackrest/commit/01b8e2258f6efa5386665c33cb5c267c154376fb) Fehlertoleranz von archive-push verbessern.; Pull Request [#1343](https://github.com/pgbackrest/pgbackrest/pull/1343)
- GCS-Unterstützung für Repository-Speicher. (*Geprüft von Cynthia Shang. Getestet von Daniel Farina.*)

  Mit `repo-type=gcs` wird das Repository auf GCS oder einem GCS-kompatiblen Objektspeicher abgelegt.

  [`dcb79ab`](https://github.com/pgbackrest/pgbackrest/commit/dcb79ab8fb18c63c2d56ecacd9d680b999ea044b) Mit \u maskierte JSON-Zeichen dekodieren.

  [`1b4b353`](https://github.com/pgbackrest/pgbackrest/commit/1b4b3538cc218f66ed1e903c3caeade4b0ab1120) In HTTP- und Speichermodulen uri wo passend in path umbenennen.

  [`66a4ff4`](https://github.com/pgbackrest/pgbackrest/commit/66a4ff496afe63305cb1a437bcb52d1efc11edf7) Pfad vor der Übergabe an HttpRequest kodieren.

  [`d485609`](https://github.com/pgbackrest/pgbackrest/commit/d4856096587c72daee76f8ad8408db677a16d6dd) strNewEncode(), strCatEncode() und bufNewDecode() hinzufügen.

  [`abcbe0f`](https://github.com/pgbackrest/pgbackrest/commit/abcbe0f9c1804ecb1b93b811cfb0a362c17e1b85) Dateien des encode-Moduls in einer Datei zusammenführen.

  [`edab2a0`](https://github.com/pgbackrest/pgbackrest/commit/edab2a0b89eabc5fd5ba6e795d938670bd5d3105) Für Kodierungstypen switch statt if-else verwenden.

  [`f6c3262`](https://github.com/pgbackrest/pgbackrest/commit/f6c3262861252b24e7e0cffd6d67e0c5e3291f3e) Funktionen valid/validate des encode-Moduls nicht öffentlich bereitstellen.

  [`a1f4fd3`](https://github.com/pgbackrest/pgbackrest/commit/a1f4fd32a1790e569ccae3598cd9648bb25d13b6) ASSERT_MSG() hinzufügen.

  [`00b60e5`](https://github.com/pgbackrest/pgbackrest/commit/00b60e564eef13f8adba0ab867fcde2c352669d6) base64url-Kodierung hinzufügen.

  [`54c4eb0`](https://github.com/pgbackrest/pgbackrest/commit/54c4eb0c10758879b4bf2b96efd2a1523ecccc21) Entfernte Speicherobjekte beschreibbar machen.

  [`088662d`](https://github.com/pgbackrest/pgbackrest/commit/088662d986288843d1bfd118b724091c93df4569) GCS als Repository-Speicher unterstützen.; Issue [#631](https://github.com/pgbackrest/pgbackrest/issues/631); Issue [#743](https://github.com/pgbackrest/pgbackrest/issues/743); Pull Request [#1320](https://github.com/pgbackrest/pgbackrest/pull/1320)
- Option `archive-header-check` hinzugefügt. (*Geprüft von Stephen Frost, Cynthia Shang. Vorgeschlagen von Hans-Jürgen Schönig.*)

  Der WAL-Header wird anhand der PostgreSQL-Version und der Systemkennung geprüft, damit WAL an die richtige Stanza gesendet wird. Die Prüfung ist standardmäßig aktiviert und kann bei Bedarf deaktiviert werden, etwa für verschlüsseltes WAL.

  Pull Request [#1298](https://github.com/pgbackrest/pgbackrest/pull/1298); Commit [`b6106f3`](https://github.com/pgbackrest/pgbackrest/commit/b6106f3c1f586b410c50c9da8dcea583cc157423)

**Verbesserungen:**

- Neu erstellte Systemdatenbanken bei der selektiven Wiederherstellung eingeschlossen. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang.*)

  Eine neu erstellte Systemdatenbank (`template0`, `template1` oder `postgres`) hat eine OID, durch die sie wie eine Benutzerdatenbank erscheint. Diese Datenbanken werden nun unabhängig von ihrer OID immer wiederhergestellt.

  Issue [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Pull Request [#1307](https://github.com/pgbackrest/pgbackrest/pull/1307); Commit [`6942ff5`](https://github.com/pgbackrest/pgbackrest/commit/6942ff569dd950a5146faa0bebfee69e241c4179)
- `content-length` aus den signierten S3-Headern ausgeschlossen. (*Geprüft von Cynthia Shang. Vorgeschlagen von Brian P Bockelman.*)

  Manche Proxys ändern den Header `content-length`. War er signiert, schlug dadurch die Authentifizierung fehl.

  Issue [#1340](https://github.com/pgbackrest/pgbackrest/issues/1340); Pull Request [#1341](https://github.com/pgbackrest/pgbackrest/pull/1341); Commit [`7d7ac0e`](https://github.com/pgbackrest/pgbackrest/commit/7d7ac0e0eb63a02bbc1dd8bd8fc89c6008c740f8)
- Seltener verwendete Optionen für den Repository-Speicher zusammengefasst. (*Geprüft von Cynthia Shang.*)

  Die S3- und Azure-Optionen für CA, Host, Port und TLS-Prüfung wurden in `repo-storage-*` umbenannt. Beispielsweise heißt `repo1-s3-host` nun `repo1-storage-host`. Die alten Namen werden weiterhin akzeptiert.

  Pull Request [#1321](https://github.com/pgbackrest/pgbackrest/pull/1321); Commit [`d1aa765`](https://github.com/pgbackrest/pgbackrest/commit/d1aa765a9d5f290738c1de00c5ea99d5f6056ba5)
- Benutzerdefinierten Standardwert für `config-path` mit `./configure --with-configdir` ermöglicht. (*Beigetragen von Michael Schout. Geprüft von David Steele.*)

  Paketbetreuer können beim Build einen anderen Standardwert für `config-path` festlegen. Ohne diese Option bleibt der Standard `/etc/pgbackrest`.

  [`6a717e0`](https://github.com/pgbackrest/pgbackrest/commit/6a717e032f1309ddc9dc955042b5e2ac2bc7324d) Konfigurationspfad im configure-Skript setzen.

  [`9243962`](https://github.com/pgbackrest/pgbackrest/commit/9243962b9504787c6f4af42318af6dc27094136d) Eigenen Standardwert für config-path mit ./configure --with-configdir erlauben.; Issue [#1251](https://github.com/pgbackrest/pgbackrest/issues/1251); Issue [#1293](https://github.com/pgbackrest/pgbackrest/issues/1293); Pull Request [#1255](https://github.com/pgbackrest/pgbackrest/pull/1255)
- Kopieren des Archivs während `backup` protokolliert. (*Geprüft von Cynthia Shang, Stefan Fercot.*)

  Issue [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Pull Request [#1328](https://github.com/pgbackrest/pgbackrest/pull/1328); Commit [`c862e96`](https://github.com/pgbackrest/pgbackrest/commit/c862e9654aff198167efeb897957bf93c1afe453)

**Verbesserungen der Dokumentation:**

- Referenz um Links zu Beispielen im Benutzerhandbuch ergänzt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Die Befehlsreferenz verlinkt nun die Abschnitte des Benutzerhandbuchs mit Beispielen. Einige Beschreibungen wurden verdeutlicht, etwa `set` für `expire`.

  Pull Request [#1353](https://github.com/pgbackrest/pgbackrest/pull/1353); Commit [`d372dd6`](https://github.com/pgbackrest/pgbackrest/commit/d372dd652c9a01b72444998d87f0f44464676803)
- Dokumentation zur selektiven Wiederherstellung um Einschränkungen ergänzt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)

  Ohne `type=immediate` kann die Recovery fehlschlagen, da PostgreSQL nach Erreichen der Konsistenz mit Nullen gefüllte Seiten als Fehler meldet. Unter PostgreSQL >= 13 kann `ignore_invalid_pages` verwendet werden. Prüfen Sie dabei jedoch die Protokolle auf ungültige Seiten in den ausgewählten Datenbanken.

  Issue [#796](https://github.com/pgbackrest/pgbackrest/issues/796); Pull Request [#1329](https://github.com/pgbackrest/pgbackrest/pull/1329); Commit [`92d12cc`](https://github.com/pgbackrest/pgbackrest/commit/92d12ccb9bd0787e30441794e2a2a4d4a4e0fe9c)
- Erläuterung zu `compress-type` in der Dokumentation zu `archive-copy` hinzugefügt. (*Geprüft von Cynthia Shang, Stefan Fercot.*)

  Verwenden `archive-push` und `backup` unterschiedliche Werte für `compress-type`, muss WAL neu komprimiert werden, was aufwendig sein kann.

  Issue [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Pull Request [#1327](https://github.com/pgbackrest/pgbackrest/pull/1327); Commit [`9506ffa`](https://github.com/pgbackrest/pgbackrest/commit/9506ffae39dd86d2c5454511026f1249097d96a2)
- Standardwerte für `compress-level` je Wert von `compress-type` hinzugefügt. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Die Standardwerte sind 9 für `bz2`, 6 für `gz`, 1 für `lz4` und 3 für `zst`.

  Issue [#1242](https://github.com/pgbackrest/pgbackrest/issues/1242); Pull Request [#1346](https://github.com/pgbackrest/pgbackrest/pull/1346); Commit [`3e20608`](https://github.com/pgbackrest/pgbackrest/commit/3e206088e79c4a73a20b8f2fda1706c6b95fa188)
- Hinweis hinzugefügt, dass dieselben NFS-Einstellungen wie bei PostgreSQL erforderlich sind. (*Beigetragen von Cynthia Shang. Geprüft von David Steele.*)

  Issue [#871](https://github.com/pgbackrest/pgbackrest/issues/871); Pull Request [#1347](https://github.com/pgbackrest/pgbackrest/pull/1347); Commit [`7598762`](https://github.com/pgbackrest/pgbackrest/commit/75987621fab5f57d0e95b42eabd301731587c438)

### v2.32 – Versionshinweise {#v232-release-notes}

*Repository-Befehle*

*Veröffentlicht am 8. Februar 2021*

**Fehlerbehebungen:**

- Fortsetzen nach teilweiser Löschung des Backups durch einen vorherigen Fortsetzungsversuch korrigiert. (*Geprüft von Cynthia Shang. Gemeldet von Tom Swartz.*)

**Funktionen:**

- Befehl `repo-ls` hinzugefügt. (*Geprüft von Cynthia Shang. Getestet von Stefan Fercot.*)
- Befehl `repo-get` hinzugefügt. (*Beigetragen von Stefan Fercot, David Steele. Geprüft von Cynthia Shang.*)
- Option `archive-mode-check` hinzugefügt. (*Beigetragen von Stefan Fercot. Geprüft von David Steele. Getestet von Michael Banck.*)

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
- Option `repo-azure-endpoint` hinzugefügt. (*Geprüft von Cynthia Shang. Getestet von Brian Peterson. Vorgeschlagen von Brian Peterson.*)
- Option `pg-database` hinzugefügt. (*Geprüft von Cynthia Shang.*)

**Verbesserungen:**

- Ausgabe des Befehls `info` verbessert, wenn eine Stanza angegeben ist, aber fehlt. (*Beigetragen von Stefan Fercot. Geprüft von Cynthia Shang, David Steele. Vorgeschlagen von uspen.*)
- Leistung bei großen Dateilisten in den Befehlen `backup`/`restore` verbessert. (*Geprüft von Cynthia Shang. Getestet von Oscar.*)
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

- Temporäre S3-Zugangsdaten auf AWS-Instanzen automatisch abgerufen. (*Beigetragen von David Steele, Stephen Frost. Geprüft von Cynthia Shang, Aleš Zelený, Jeanette Bromage. Getestet von David Youatt.*)
- Option `archive-mode` hinzugefügt, um die Archivierung bei der Wiederherstellung zu deaktivieren. (*Geprüft von Stephen Frost. Vorgeschlagen von Stephen Frost.*)

**Verbesserungen:**

- Unterstützung für PostgreSQL 13 beta3. Änderungen an den Control-/Katalog-/WAL-Versionen in nachfolgenden Beta-Versionen können die Kompatibilität aufheben. pgBackRest wird jedoch mit jeder Veröffentlichung entsprechend aktualisiert.
- Asynchrones `list`/`remove` für S3/Azure-Speicher. (*Geprüft von Cynthia Shang, Stephen Frost.*)
- Speicherverbrauch bei der Erkennung nicht protokollierter Relationen während der Manifesterstellung verbessert. (*Geprüft von Cynthia Shang, Stephen Frost, Oscar. Getestet von Brad Nicholson. Vorgeschlagen von Oscar, Brad Nicholson.*)
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

- Azure-Unterstützung für Repository-Speicher. (*Geprüft von Cynthia Shang. Getestet von Don Seiler.*)
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

- Nicht blockierende TLS-Implementierung. (*Geprüft von Cynthia Shang, Stephen Frost. Getestet von Slava Moudry.*)
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
