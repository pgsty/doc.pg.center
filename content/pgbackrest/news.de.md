---
title: "Nachrichten"
linkTitle: "Nachrichten"
weight: 10
description: "Offizielle Nachrichten zum pgBackRest-Projekt, Versionsankündigungen und Neuigkeiten zur Projektpflege."
icon: fa-solid fa-newspaper
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/news.html"
---

--------

## pgBackRest 2.60.0 veröffentlicht {#release-2-60-0}

**18. Oktober 2026**

Die pgBackRest-Community freut sich, die Veröffentlichung von [pgBackRest](https://pgbackrest.org) 2.60.0 bekanntzugeben. Dies ist die neueste Version der zuverlässigen, einfach zu bedienenden Lösung für Backup und Wiederherstellung, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

pgBackRest bietet umfangreiche Funktionen für die Verwaltung Ihrer Backup- und Recovery-Infrastruktur, darunter: parallele Backups und Wiederherstellungen, vollständige/differenzielle/inkrementelle Backups, blockinkrementelle Backups, mehrere Repositorys, Delta-Wiederherstellung, parallele asynchrone Archivierung, Schutz vor Malware und Ransomware, Prüfsummen für jede Datei, während des Backups geprüfte Seitenprüfsummen (sofern aktiviert), mehrere Komprimierungsverfahren, Verschlüsselung, Fortsetzung unvollständiger oder fehlgeschlagener Backups, Backups vom Standby, Unterstützung für Tablespaces und Links, Unterstützung für S3/Azure/GCS/SFTP, Entfernen abgelaufener Backups, lokalen und entfernten Betrieb über SSH oder TLS, flexible Konfiguration und vieles mehr.

pgBackRest kann aus dem [PostgreSQL Yum Repository](https://yum.postgresql.org) oder dem [PostgreSQL APT Repository](https://apt.postgresql.org) installiert werden; Pakete sind auch für viele andere Distributionen verfügbar. Der Quellcode steht unter [Versionen](/de/pgbackrest/release/) zum Download bereit.

### Wichtige neue Funktionen und Verbesserungen {#release-2-60-0-feature}

- Option checksum-page-error für Fehler bei ungültigen Seitenprüfsummen ergänzt (Andrew Pogrebnoi)
- Unterstützung für GCS Workload Identity Federation (Adol Rodriguez)
- Leseanfragen für mehrere Dateien oder Bereiche aus Objektspeichern vorab senden (David Steele)
- Keep-alive-Anfragen an entfernte Prozesse reduziert (David Steele)
- In der Antwort fehlende Teilanfragen eines Azure-Batches erneut ausführen (David Steele)
- Weniger Manifestprüfungen beim Rekonstruieren von backup.info (David Steele)
- Kompilieren unter illumos unterstützt (Kalevi Kolttonen)
- OpenSSL 4 unterstützt (David Steele)
- Website modernisiert (David Steele, Jan Wieremjewicz)

Weitere Funktionen und Verbesserungen sind in den [Versionshinweisen zu 2.60.0](/de/pgbackrest/release/#v2600-release-notes) beschrieben.

### Wichtige Hinweise {#release-2-60-0-note}

- Der Befehl restore meldet jetzt einen Fehler und hält an, wenn eine wiederhergestellte Datei eine ungültige Seitenprüfsumme enthält. Dadurch bleibt der Cluster unvollständig und kann nicht starten; die Wiederherstellung muss erneut ausgeführt werden. Der Befehl expire verweigert jetzt das Entfernen abgelaufener Backups, wenn das älteste beibehaltene Backup Prüfsummenfehler enthalten würde. Damit wird auch die Bereinigung des Archivs in diesem Repository verhindert. Mit checksum-page-error=n werden stattdessen Warnungen ausgegeben.
- Zum Kompilieren aus einem Git-Checkout wird PyYAML statt libyaml benötigt. Das Tar-Archiv der Distribution enthält den generierten Code und benötigt keines von beiden.
- PostgreSQL 19rc1 wird ab v2.59.2 unterstützt, einschließlich dieser Version.

### Links {#release-2-60-0-link}

- [Website](/de/pgbackrest/)
- [Benutzerhandbücher](/de/pgbackrest/user-guide/)
- [Versionshinweise](/de/pgbackrest/release/)

### Sponsoren {#release-2-60-0-sponsorship}

Diese Version wurde durch die großzügige Förderung von [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/) ermöglicht.


--------

## Schwache Unterschlüssel und Salts bei der Verschlüsselung {#weak-encryption}

**4. Oktober 2026**

pgBackRest-Versionen vor 2.59.3 prüften bei der Erzeugung von Zufallsdaten für die Verschlüsselung nicht auf Fehler. Wenn OpenSSL keine Zufallsdaten vom Betriebssystem beziehen konnte, wurden Verschlüsselungsunterschlüssel und Salts aus bereits im Speicher vorhandenen Daten erzeugt, ohne einen Fehler zu melden. Nicht verschlüsselte Repositorys sind nicht betroffen.

Dieser Fehler dürfte selten auftreten. Mögliche Ursachen sind eine Sandbox oder eine seccomp-Richtlinie, die den Systemaufruf `getrandom()` blockiert, sowie eine ungültige OpenSSL-Konfiguration.

Besonders kritisch sind die Unterschlüssel in `archive.info` und `backup.info`. Sie werden einmalig von `stanza-create` erzeugt und während der gesamten Lebensdauer der Stanza verwendet. Ein Upgrade ersetzt daher einen schwachen Unterschlüssel nicht. Schwache Backup-Unterschlüssel und Salts werden entfernt, wenn Backups und WAL ablaufen.

### Auswirkungen {#weak-encryption-impact}

Der WAL-Unterschlüssel wird in `archive.info` gespeichert, der Manifest-Unterschlüssel in `backup.info`. Ein schwacher Unterschlüssel lässt sich leichter erraten als ein zufälliger. Mit einem erratenen Unterschlüssel können die damit verschlüsselten Dateien ohne `repo-cipher-pass` entschlüsselt werden. Wie viel leichter dies ist, hängt vom Speicherinhalt ab, der je nach Plattform und Build variiert. Ein schwacher Unterschlüssel in `archive.info` gefährdet sämtliche WAL im Repository. Ein schwacher Unterschlüssel in `backup.info` gefährdet jedes Backup, da die Manifeste mit ihm verschlüsselt werden und jedes Manifest den Unterschlüssel für die Dateien seines Backups enthält. Dies betrifft auch WAL und Backups, die nach dem Upgrade hinzugefügt werden.

Der Unterschlüssel für die Dateien eines Backups wird für jedes vollständige Backup erzeugt und auch von den darauf basierenden differenziellen und inkrementellen Backups verwendet. Ein schwacher Backup-Unterschlüssel gefährdet die Dateien in all diesen Backups.

Ein schwaches Salt legt keinen Unterschlüssel offen. Dateien, die mit demselben Unterschlüssel und Salt verschlüsselt werden, verwenden denselben Schlüssel und IV. Identische Daten in diesen Dateien ergeben daher identische verschlüsselte Daten. Das Salt wird unverschlüsselt am Anfang jeder Datei gespeichert. Ein schwaches Salt kann bis zu 8 Byte zuvor im Speicher vorhandener Daten enthalten.

### Unterschlüssel prüfen {#weak-encryption-check-subkey}

Führen Sie die folgenden Befehle auf einem Host mit Zugriff auf das Repository aus und setzen Sie `STANZA` auf den Namen der Stanza. Ergänzen Sie die `pgbackrest`-Befehle um `--repo`, um ein anderes als das erste Repository zu prüfen.

```bash
STANZA=demo

for file in archive/$STANZA/archive.info backup/$STANZA/backup.info; do
    for key in $(pgbackrest --stanza=$STANZA repo-get $file | grep '^cipher-pass=' | grep -oE '[A-Za-z0-9+/]{64}'); do
        echo "$(printf '%s' $key | base64 -d | od -An -v -tx1 | tr -s ' ' '\n' | grep -c '^00$') $file"
    done
done
```

Die erste Spalte gibt die Anzahl der Nullbytes im Unterschlüssel an. Ein zufälliger Unterschlüssel enthält in weniger als einem von 25 000 000 Fällen 6 oder mehr Nullbytes. Die in Tests gefundenen schwachen Unterschlüssel enthielten hingegen 13 oder mehr. Ein Unterschlüssel mit 6 oder mehr Nullbytes sollte als schwach gelten.

### OpenSSL 1.0 {#weak-encryption-openssl-1-0}

pgBackRest-Versionen vor 2.53 konnten mit OpenSSL 1.0 gebaut werden. Wenn es keine Zufallsdaten vom Betriebssystem beziehen kann, erzeugt es Zufallsdaten aus einem Zustand, der nicht mit Zufallsdaten initialisiert wurde. Auf diese Weise erzeugte schwache Unterschlüssel lassen sich mit der obigen Prüfung nicht erkennen.

### Abhilfemaßnahmen {#weak-encryption-remediation}

- Führen Sie ein Upgrade auf pgBackRest 2.59.3 oder neuer durch. Diese Versionen melden einen Fehler, wenn keine Zufallsdaten erzeugt werden können.
- Ist der Unterschlüssel in `archive.info` oder `backup.info` schwach, erstellen Sie die Stanza in einem neuen Repository und behalten Sie das alte Repository nur so lange, wie dessen Backups benötigt werden.
- Erwägen Sie nach dem Upgrade ein neues vollständiges Backup, da differenzielle und inkrementelle Backups den Unterschlüssel ihres vollständigen Backups verwenden.
- Schwache Backup-Unterschlüssel und Salts werden entfernt, wenn die Backups und WAL aus der Zeit vor dem Upgrade ablaufen. Bei Backups mit langer Aufbewahrungsdauer bleiben sie bis zu deren Ablauf erhalten.


--------

## pgBackRest 2.59.3 veröffentlicht {#release-2-59-3}

**4. Oktober 2026**

Die pgBackRest-Community freut sich, die Veröffentlichung von [pgBackRest](https://pgbackrest.org) 2.59.3 bekanntzugeben. Dies ist die neueste Version der zuverlässigen, einfach zu bedienenden Lösung für Backup und Wiederherstellung, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

pgBackRest bietet umfangreiche Funktionen für die Verwaltung Ihrer Backup- und Recovery-Infrastruktur, darunter: parallele Backups und Wiederherstellungen, vollständige/differenzielle/inkrementelle Backups, blockinkrementelle Backups, mehrere Repositorys, Delta-Wiederherstellung, parallele asynchrone Archivierung, Schutz vor Malware und Ransomware, Prüfsummen für jede Datei, während des Backups geprüfte Seitenprüfsummen (sofern aktiviert), mehrere Komprimierungsverfahren, Verschlüsselung, Fortsetzung unvollständiger oder fehlgeschlagener Backups, Backups vom Standby, Unterstützung für Tablespaces und Links, Unterstützung für S3/Azure/GCS/SFTP, Entfernen abgelaufener Backups, lokalen und entfernten Betrieb über SSH oder TLS, flexible Konfiguration und vieles mehr.

pgBackRest kann aus dem [PostgreSQL Yum Repository](https://yum.postgresql.org) oder dem [PostgreSQL APT Repository](https://apt.postgresql.org) installiert werden; Pakete sind auch für viele andere Distributionen verfügbar. Der Quellcode steht unter [Versionen](/de/pgbackrest/release/) zum Download bereit.

### Fehlerbehebungen {#release-2-59-3-feature}

- Mögliche Erzeugung schwacher Verschlüsselungsunterschlüssel oder Salts behoben (j0uinim)
- Möglichen Prüfsummenfehler beim Laden verschlüsselter Informationsdateien und Manifeste behoben (j0uinim)

Weitere Fehlerbehebungen und Verbesserungen sind in den [Versionshinweisen zu 2.59.3](/de/pgbackrest/release/#v2593-release-notes) beschrieben.

### Wichtige Hinweise {#release-2-59-3-note}

- In früheren Versionen konnten bei einem Fehler beim Zugriff auf die Zufallsdaten des Systems schwache Verschlüsselungsunterschlüssel und Salts erzeugt werden. Weitere Informationen finden Sie unter [Schwache Unterschlüssel und Salts bei der Verschlüsselung](/de/pgbackrest/news/#weak-encryption).

### Links {#release-2-59-3-link}

- [Website](/de/pgbackrest/)
- [Benutzerhandbücher](/de/pgbackrest/user-guide/)
- [Versionshinweise](/de/pgbackrest/release/)

### Sponsoren {#release-2-59-3-sponsorship}

Diese Version wurde durch die großzügige Förderung von [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/) ermöglicht.



--------

## pgBackRest 2.59.2 veröffentlicht {#release-2-59-2}

**27. September 2026**

Die pgBackRest-Community freut sich, die Veröffentlichung von [pgBackRest](https://pgbackrest.org) 2.59.2 bekanntzugeben. Dies ist die neueste Version der zuverlässigen, einfach zu bedienenden Lösung für Backup und Wiederherstellung, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

pgBackRest bietet umfangreiche Funktionen für die Verwaltung Ihrer Backup- und Recovery-Infrastruktur, darunter: parallele Backups und Wiederherstellungen, vollständige/differenzielle/inkrementelle Backups, blockinkrementelle Backups, mehrere Repositorys, Delta-Wiederherstellung, parallele asynchrone Archivierung, Schutz vor Malware und Ransomware, Prüfsummen für jede Datei, während des Backups geprüfte Seitenprüfsummen (sofern aktiviert), mehrere Komprimierungsverfahren, Verschlüsselung, Fortsetzung unvollständiger oder fehlgeschlagener Backups, Backups vom Standby, Unterstützung für Tablespaces und Links, Unterstützung für S3/Azure/GCS/SFTP, Entfernen abgelaufener Backups, lokalen und entfernten Betrieb über SSH oder TLS, flexible Konfiguration und vieles mehr.

pgBackRest kann aus dem [PostgreSQL Yum Repository](https://yum.postgresql.org) oder dem [PostgreSQL APT Repository](https://apt.postgresql.org) installiert werden; Pakete sind auch für viele andere Distributionen verfügbar. Der Quellcode steht unter [Versionen](/de/pgbackrest/release/) zum Download bereit.

### Neue Funktionen und Fehlerbehebungen {#release-2-59-2-feature}

- Unterstützung für PostgreSQL 19beta4 (David Steele)
- Fehler bei einer leeren Blockzuordnung behoben, wenn eine Datei während des Backups auf die Länge null gekürzt wird (David Steele)
- Wiederholungen von Lesevorgängen deaktiviert, wenn Filter an den Treiber übergeben werden (David Steele)
- Seitenweises Auflisten von S3-Versionen korrigiert (David Steele)
- Azure-Versionsheader für die SAS-Authentifizierung gesetzt (David Steele)
- Hängenbleiben des asynchronen `archive-push` an einer Backup-Historiendatei mit der Größe null behoben (Andrew Kroh)
- Befehl `annotate` auf einem entfernten verschlüsselten Repository korrigiert (Douglas J Hunley)

Weitere Fehlerbehebungen und Verbesserungen sind in den [Versionshinweisen zu 2.59.2](/de/pgbackrest/release/#v2592-release-notes) beschrieben.

### Wichtige Hinweise {#release-2-59-2-note}

- PostgreSQL 19beta4 hat die Formate von `pg_control` und WAL geändert. Cluster und WAL aus einer früheren Beta-Version von 19 werden daher nicht mehr unterstützt. Cluster mit einer früheren Beta-Version sollten mit 19beta4 neu erstellt werden.

### Links {#release-2-59-2-link}

- [Website](/de/pgbackrest/)
- [Benutzerhandbücher](/de/pgbackrest/user-guide/)
- [Versionshinweise](/de/pgbackrest/release/)

### Sponsoren {#release-2-59-2-sponsorship}

Diese Version wurde durch die großzügige Förderung von [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/) ermöglicht.


--------

## pgBackRest 2.59.1 veröffentlicht {#release-2-59-1}

**17. August 2026**

Die pgBackRest-Community freut sich, die Veröffentlichung von [pgBackRest](https://pgbackrest.org) 2.59.1 bekanntzugeben. Dies ist die neueste Version der zuverlässigen, einfach zu bedienenden Lösung für Backup und Wiederherstellung, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

pgBackRest bietet umfangreiche Funktionen für die Verwaltung Ihrer Backup- und Recovery-Infrastruktur, darunter: parallele Backups und Wiederherstellungen, vollständige/differenzielle/inkrementelle Backups, blockinkrementelle Backups, mehrere Repositorys, Delta-Wiederherstellung, parallele asynchrone Archivierung, Schutz vor Malware und Ransomware, Prüfsummen für jede Datei, während des Backups geprüfte Seitenprüfsummen (sofern aktiviert), mehrere Komprimierungsverfahren, Verschlüsselung, Fortsetzung unvollständiger oder fehlgeschlagener Backups, Backups vom Standby, Unterstützung für Tablespaces und Links, Unterstützung für S3/Azure/GCS/SFTP, Entfernen abgelaufener Backups, lokalen und entfernten Betrieb über SSH oder TLS, flexible Konfiguration und vieles mehr.

pgBackRest kann aus dem [PostgreSQL Yum Repository](https://yum.postgresql.org) oder dem [PostgreSQL APT Repository](https://apt.postgresql.org) installiert werden; Pakete sind auch für viele andere Distributionen verfügbar. Der Quellcode steht unter [Versionen](/de/pgbackrest/release/) zum Download bereit.

### Neue Funktionen und Fehlerbehebungen {#release-2-59-1-feature}

- Unterstützung für PostgreSQL 19beta3 (Lardière Sébastien)
- Hängenbleiben behoben, wenn der Chunk-Puffer kleiner als der Eingabepuffer ist (David Steele)
- Neue Backup-Kennzeichnung nur mit ihrem eigenen vollständigen Backup-Satz verglichen (David Steele)
- Von GitHub erzeugte Quellcodearchive korrigiert, in denen für den Build erforderliche Dateien fehlten (David Steele)

Weitere Fehlerbehebungen und Verbesserungen sind in den [Versionshinweisen zu 2.59.1](/de/pgbackrest/release/#v2591-release-notes) beschrieben.

### Wichtige Hinweise {#release-2-59-1-note}

- PostgreSQL 19beta3 hat das WAL-Format geändert. WAL, das mit einer früheren Beta-Version von PostgreSQL 19 archiviert wurde, ist daher nicht mehr lesbar. Cluster mit einer früheren Beta-Version sollten mit 19beta3 neu erstellt werden.

### Links {#release-2-59-1-link}

- [Website](/de/pgbackrest/)
- [Benutzerhandbücher](/de/pgbackrest/user-guide/)
- [Versionshinweise](/de/pgbackrest/release/)

### Sponsoren {#release-2-59-1-sponsorship}

Diese Version wurde durch die großzügige Förderung von [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/) ermöglicht.


--------

## Neuer Distributions-Tarball {#distribution-tarball}

**20. Juli 2026**

Ab pgBackRest 2.59.0 enthält jede Veröffentlichung einen Distributions-Tarball, der das Bauen aus dem Quellcode vereinfacht. Anders als ein Checkout des Git-Repositorys enthält der Tarball bereits den generierten Quellcode und die fertig gerenderte Dokumentation. pgBackRest lässt sich damit ohne die Werkzeuge zur Codegenerierung oder Dokumentation bauen und installieren, die ein Repository-Checkout benötigt.

Der Tarball enthält den pgBackRest-Quellcode mit dem vorgenerierten Code, die Manpage der Befehlsreferenz, die HTML-Dokumentation und einen Smoke-Test zur Überprüfung des Builds. Er wird mit meson und ninja gebaut und benötigt nur die üblichen pgBackRest-Bibliotheken.

Der Tarball ist jeder Veröffentlichung als Datei mit dem Namen `pgbackrest-{version}.tar.gz` beigefügt, zusammen mit einer passenden `.sha256sum`-Prüfsumme. Er kann von der Seite [Versionen](https://github.com/pgbackrest/pgbackrest/releases) auf GitHub heruntergeladen werden. Anweisungen zum Bauen und Testen stehen in der `README.md` im Tarball.

Paketbetreuer werden gebeten, den Distributions-Tarball für den Build zu verwenden, um die zusätzlichen Build-Werkzeuge zu vermeiden, die in künftigen Versionen zur Erzeugung von Code und Dokumentation erforderlich sein werden.


--------

## pgBackRest 2.59.0 veröffentlicht {#release-2-59-0}

**20. Juli 2026**

Die pgBackRest-Community freut sich, die Veröffentlichung von [pgBackRest](https://pgbackrest.org) 2.59.0 bekanntzugeben. Dies ist die neueste Version der zuverlässigen, einfach zu bedienenden Lösung für Backup und Wiederherstellung, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

pgBackRest bietet umfangreiche Funktionen für die Verwaltung Ihrer Backup- und Recovery-Infrastruktur, darunter: parallele Backups und Wiederherstellungen, vollständige/differenzielle/inkrementelle Backups, blockinkrementelle Backups, mehrere Repositorys, Delta-Wiederherstellung, parallele asynchrone Archivierung, Schutz vor Malware und Ransomware, Prüfsummen für jede Datei, während des Backups geprüfte Seitenprüfsummen (sofern aktiviert), mehrere Komprimierungsverfahren, Verschlüsselung, Fortsetzung unvollständiger oder fehlgeschlagener Backups, Backups vom Standby, Unterstützung für Tablespaces und Links, Unterstützung für S3/Azure/GCS/SFTP, Entfernen abgelaufener Backups, lokalen und entfernten Betrieb über SSH oder TLS, flexible Konfiguration und vieles mehr.

pgBackRest kann aus dem [PostgreSQL Yum Repository](https://yum.postgresql.org) oder dem [PostgreSQL APT Repository](https://apt.postgresql.org) installiert werden; Pakete sind auch für viele andere Distributionen verfügbar. Der Quellcode steht unter [Versionen](/de/pgbackrest/release/) zum Download bereit.

### Wesentliche neue Funktionen und Verbesserungen {#feature}

- Unterstützung für PostgreSQL 19 (David Steele)
- Option `archive-expire-before` zum Bereinigen des WAL-Archivs hinzugefügt (Stefan Fercot)
- Unterstützung für S3 Outposts hinzugefügt (Shiva Kumar Ambigi)
- S3-Prozessauthentifizierung hinzugefügt (David Steele)
- Zwischenspeicherung von Benutzern und Gruppen für eine schnellere Erstellung des Manifests hinzugefügt (Gunnar Lindholm)
- Erneuter Verbindungsaufbau zum SFTP-Speicher, nachdem der Server eine inaktive Verbindung getrennt hat (David Steele)
- Backup-Fortschritt je Repository zur Ausgabe des Befehls `info` hinzugefügt (Will Morland)
- Stapellöschung für Azure-Speicher hinzugefügt (David Steele)
- Prüfungen von `backup.info` zum Befehl `verify` hinzugefügt (Denis Garsh)
- Konfiguration des S3-STS-Endpunkts ermöglicht (Simon Gratton)
- Integration von systemd-Benachrichtigungen hinzugefügt (Andrew Jackson)
- Fehler bei Ausführung als root, sofern `allow-root` nicht aktiviert ist (David Steele)
- Asynchrones `archive-push` beim ersten Fehler beendet (David Steele)

Weitere Funktionen und Verbesserungen sind in den [Versionshinweisen zu 2.59.0](/de/pgbackrest/release/#v2590-release-notes) beschrieben.

### Wichtige Hinweise {#note}

- Standardmäßig darf nur der Befehl `restore` als root ausgeführt werden. Mit `allow-root` können andere Befehle als root ausgeführt werden (dies wird jedoch nicht empfohlen).
- Ein neuer Distributions-Tarball mit vorgenerierter Dokumentation, Manpage und Code ist jeder Veröffentlichung beigefügt, um die Paketerstellung zu vereinfachen. Weitere Informationen stehen unter [Neuer Distributions-Tarball](#distribution-tarball).
- Es gibt eine neue optionale Abhängigkeit von `libsystemd`.

### Links {#link}

- [Website](/de/pgbackrest/)
- [Benutzerhandbücher](/de/pgbackrest/user-guide/)
- [Versionshinweise](/de/pgbackrest/release/)

### Sponsoren {#sponsorship}

Diese Version wurde durch die großzügige Förderung von [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/) ermöglicht.


--------

## pgBackRest wird fortgeführt! {#will-continue}

**18. Mai 2026**

Ich freue mich, bekanntgeben zu können, dass pgBackRest fortgeführt wird! In den vergangenen Wochen hat sich eine Gruppe von Sponsoren zusammengefunden, um die weitere Entwicklung zu finanzieren. Dank ihrer Unterstützung hängt das Projekt nicht mehr von einem einzigen Sponsor ab. Das gibt pgBackRest die nötige langfristige Stabilität.

Ich möchte jedem unserer Sponsoren danken:

[Amazon Web Services](https://aws.amazon.com) stellt Privatpersonen, Unternehmen und Behörden Cloud-Computing-Ressourcen nach Bedarf zur Verfügung. Nutzen Sie Rechenleistung, Speicher, Datenbanken, maschinelles Lernen und über 200 Dienste und zahlen Sie nur für das, was Sie tatsächlich nutzen. Darauf ausgelegt, mit Ihnen zu wachsen und in die Gemeinschaften zu investieren, denen wir gemeinsam angehören.

[Supabase](https://supabase.com) ist eine vollständige Backend-Plattform auf Basis von PostgreSQL. Sie ermöglicht es Entwicklern, Anwendungen schnell zu erstellen und zu skalieren, ohne Infrastruktur verwalten zu müssen. Sie umfasst eine Postgres-Datenbank, Benutzerauthentifizierung, Echtzeitabonnements, Dateispeicher, Edge-Funktionen und serverlose Funktionen, unterstützt von einer aktiven Open-Source-Community.

[pgEdge](https://pgedge.com) ist eine unternehmenstaugliche Open-Source-Postgres-Plattform für AI, Hochverfügbarkeit und weitere Einsatzgebiete. Sie bietet native Werkzeuge für agentenbasierte AI und eine DBA-Arbeitsumgebung, Überwachung und Reaktion auf Vorfälle, flexible Bereitstellung und Wartung ohne Ausfallzeiten. Sie skaliert von einem einzelnen Knoten bis zu einem Active-Active-Multi-Master-System in der Cloud, vor Ort oder in vom Netz getrennten Umgebungen.

[Tiger Data](https://tigerdata.com), die Entwickler von TimescaleDB, entwickelt die auf PostgreSQL basierende Open-Source-Zeitreihendatenbank und betreibt Tiger Cloud, eine verwaltete Plattform für Zeitreihen, Analysen und AI-Arbeitslasten. Sowohl selbstverwaltete als auch Cloud-Angebote ermöglichen es Organisationen, Zeitreihendaten in großem Umfang zu erfassen, zu speichern und zu analysieren, von Edge- bis zu zentralen Cloud-Bereitstellungen.

[Percona](https://percona.com) ist ein Unternehmen für Open-Source-Datenbanksoftware, Support und Dienstleistungen, das Organisationen dabei hilft, die volle Kontrolle über ihre Dateninfrastruktur zu behalten. Mit frei verfügbarer Open-Source-Software, fachkundigem 24/7-Support und praktischer Datenbankexpertise unterstützt es Unternehmen beim sicheren und effizienten Betrieb von MySQL, PostgreSQL, MongoDB, Valkey und Redis.

[Eon.io](https://eon.io) ist eine intelligente Cloud-Infrastruktur für Backup, Recovery und Datenverwaltung. Sie hilft Teams, Backups effizienter zu speichern und darauf zuzugreifen, und macht Daten für Analyse- und AI-Abläufe zugänglich. Sie bietet schnelle, granulare Recovery und deutlich geringere Speicherkosten für Postgres und datenintensive Arbeitslasten in allen Clouds, einschließlich Recovery nach versehentlichem Datenverlust und Regressionen durch AI-Agenten.

Diese Organisationen setzen auf pgBackRest, um für ihre Produkte und Kunden eine zuverlässige Disaster Recovery zu gewährleisten. Ihre Investition spiegelt die entscheidende Rolle von pgBackRest im PostgreSQL-Ökosystem wider. Ihre gemeinsame Unterstützung sichert den langfristigen Fortbestand des Projekts.

Ich freue mich darauf, die Arbeit wieder aufzunehmen. Es sind Funktionen und Optimierungen in Vorbereitung, die ich in kommenden Versionen gerne vorstellen möchte. Vielen Dank an unsere Sponsoren, die dies ermöglichen, und an die Community für ihre Geduld und Unterstützung während dieses Übergangs.


--------

## Neuigkeiten zur Projektpflege {#maintenance-update}

**4. Mai 2026**

Nachdem ich angekündigt hatte, pgBackRest nicht mehr zu pflegen, wurde mein Posteingang mit Nachrichten überflutet. Es hat eine Weile gedauert, sie zu sichten. Viele enthielten gute Wünsche und Dank für meine Arbeit über die Jahre.

Doch bald zeichnete sich ein Muster ab. Es ist klar, dass viele pgBackRest-Nutzer, insbesondere diejenigen, die ihrerseits pgBackRest-Nutzer betreuen, eine Fortführung des Projekts mit mir als Hauptbetreuer bevorzugen würden. Das würde ich mir selbst sehr wünschen, aber nach monatelanger Suche nach Finanzierung hatte ich gerade beschlossen, dass es nicht gelingen würde.

Nun hat sich die Lage geändert, und es scheint nahezu sicher, dass ich genügend Finanzierung für die Fortführung des Projekts sichern kann. Diesmal wird pgBackRest von einer Gruppe von Sponsoren finanziert, damit eine einzelne Firmenübernahme meine Fähigkeit zur weiteren Arbeit am Projekt nicht mehr beeinträchtigt. Wir sollten auch einen weiteren Betreuer hinzunehmen können, um die Arbeit zu verteilen und für Kontinuität in der Zukunft zu sorgen.

Ich weiß, dass dies ein Schock war und große Unsicherheit herrscht. Bitte haben Sie Geduld: Die aktuelle Version von pgBackRest funktioniert, und es gibt keine offenen kritischen Fehler oder Sicherheitsprobleme. Es ist daher nicht nötig, das Projekt sofort zu forken.

Ich rechne damit, bis Ende der Woche eine verbindlichere Ankündigung machen zu können. Bitte warten Sie bis dahin ab und seien Sie versichert, dass wir aktiv daran arbeiten, pgBackRest wiederzubeleben.


--------

## pgBackRest wird nicht mehr gepflegt {#no-longer-maintained}

**27. April 2026**

TL;DR: pgBackRest wird nicht mehr gepflegt. Wenn Sie einen Fork von pgBackRest erstellen, wählen Sie bitte einen neuen Namen für Ihr Projekt.

Nach reiflicher Überlegung habe ich beschlossen, die Arbeit an pgBackRest einzustellen. Diese Entscheidung ist mir nicht leichtgefallen. pgBackRest war in den vergangenen dreizehn Jahren mein Herzensprojekt. Ich hatte das Glück, während eines großen Teils dieser Zeit von Unternehmen gefördert zu werden. Es gab aber auch viele späte Abende und Wochenenden, an denen ich mit Unterstützung zahlreicher Mitwirkender daran gearbeitet habe, pgBackRest zu dem Projekt zu machen, das es heute ist. Jeder Open-Source-Entwickler weiß genau, was ich meine und wie viel vom eigenen Leben einem besonderen Projekt gewidmet wird.

Seit dem Verkauf von Crunchy Data habe ich pgBackRest weiter gepflegt und nach einer Stelle gesucht, die mir die Fortsetzung dieser Arbeit ermöglichen würde. Bisher war ich damit jedoch nicht erfolgreich. Auch meine Bemühungen um Sponsoren blieben weit hinter dem zurück, was ich brauche, um das Projekt weiterführen zu können.

Wie jeder andere muss auch ich meinen Lebensunterhalt verdienen, und das Angebot an Stellen mit Bezug zu pgBackRest ist sehr begrenzt. Ich kann nun mehr Möglichkeiten in Betracht ziehen. Diese werden mir jedoch keine Zeit für die Arbeit an pgBackRest lassen, die viel Zeit für Pflege, Fehlerbehebungen, PR-Prüfungen, das Beantworten von Issues usw. erfordert. Darin ist noch nicht einmal die Zeit für neue Funktionen enthalten, die ich besonders gerne entwickle. Statt die Arbeit schlecht und/oder sporadisch zu erledigen, halte ich einen klaren Schlussstrich für sinnvoller.

Ich gehe davon aus, dass pgBackRest irgendwann geforkt wird. Das wird aber ein neues Projekt mit neuen Betreuern sein, die sich das Vertrauen genauso erarbeiten müssen wie wir.

Nochmals vielen Dank an alle, die über die Jahre zu pgBackRest beigetragen haben. Es war mir eine Freude, mit Ihnen zusammenzuarbeiten!
