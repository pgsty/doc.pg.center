---
title: "Parallelverarbeitung"
linkTitle: "Parallelverarbeitung"
weight: 50
description: "Zwischen der abschnittsweisen Parallelverarbeitung einer einzelnen Protokolldatei und der parallelen Verarbeitung vieler Protokolle wählen"
search_keywords: [--Jobs, --jobs, --tempdir, Jobs, jobs, tempdir]
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [Aufgabe]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger bietet zwei einander ergänzende Modi für die Parallelverarbeitung. Wählen Sie den Modus anhand der Struktur Ihrer Eingabedaten und nicht allein nach der Anzahl der CPUs.

| Option | Parallelitätseinheit | Geeignet für | Wichtigste Einschränkung |
|---|---|---|---|
| `-j N` / `--jobs N` | Abschnitte einer Protokolldatei | eine große Protokolldatei mit wahlfreiem Zugriff | An Abschnittsgrenzen kann eine geringe Anzahl von Abfragen doppelt gezählt oder ausgelassen werden |
| `-J N` / `--Jobs N` | vollständige Protokolldateien | viele unabhängige Protokolle | nützlich nur, wenn genügend Dateien vorhanden sind, um die Worker auszulasten |

## Eine große Datei mit `-j` aufteilen {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

Der Algorithmus des Originalprojekts teilt jede Datei in `N` Bytebereiche auf, startet für jeden Bereich einen eigenen Parser, schreibt temporäre Binärstatistiken und führt diese anschließend zum endgültigen Bericht zusammen.

```text
für jede Protokolldatei
    die Datei in N Abschnitte aufteilen
    Anfangs- und Endposition jedes Abschnitts bestimmen
    an diesen Positionen N Parserprozesse starten
    pro Parser eine temporäre Binärdatei mit Statistiken schreiben
auf die Worker warten
die Binärdateien zusammenführen und den Bericht erstellen
```

Da Protokolleinträge und mehrzeilige Anweisungen nicht genau an Byte-Offsets ausgerichtet sind, können an den Abschnittsgrenzen bis zu etwa `N` Abfragen pro Datei abgeschnitten, ausgelassen oder — häufiger — doppelt gezählt werden. Verwenden Sie diesen Modus für aggregierte Analysen sehr großer Dateien, nicht für Abläufe, die eine forensisch exakte Zählung jedes Protokolleintrags erfordern.

## Mehrere Dateien mit `-J` verarbeiten {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

Jeder Worker verarbeitet eine vollständige Datei, sodass dieser Modus Ungenauigkeiten an Abschnittsgrenzen vermeidet. Besonders nützlich ist er bei Hunderten kleiner Dateien und ausreichender CPU- sowie I/O-Kapazität. Die Dokumentation des Originalprojekts sieht `-J` auch für unabhängige komprimierte Dateien vor; das Aufteilen einer einzelnen Datei mit `-j` erfordert dagegen unkomprimierte Eingabedaten mit wahlfreiem Zugriff.

## Benchmark des Originalprojekts {#benchmark}

Das Handbuch des Originalprojekts nennt diese Messwerte für einen Host mit 8 CPUs. Betrachten Sie sie als Vergleich der beiden Algorithmen und nicht als Prognose für aktuelle Hardware.

Eine Datei mit 9.5 GB:

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 1h41m18 | 50m25 | 25m39 | 15m58 |
| `-J` | 1h41m18 | 54m28 | 41m16 | 34m45 |

Zweihundert Dateien à 10 MB, insgesamt 2 GB:

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 20m15 | 9m56 | 5m20 | 4m20 |
| `-J` | 20m15 | 9m49 | 5m00 | 2m40 |

In der Praxis empfiehlt sich `-j` für wenige große Dateien und `-J` für viele kleine Dateien. Sie können beide Modi kombinieren, sofern Eingabe und Plattform dies unterstützen. Messen Sie jedoch die Leistung dieser Kombination: Die Protokollanalyse kann eher durch den Durchsatz des Speichersystems als durch die CPU-Leistung begrenzt werden.

## Einschränkungen und temporäre Dateien {#limits-and-temporary-files}

- `-j` ist für komprimierte oder CSV-Eingabedaten nicht verfügbar und setzt das Forken von Prozessen voraus; daher steht dieser Modus unter Windows nicht zur Verfügung.
- Verwenden Sie für entfernte Protokolle, die nicht im CSV-Format vorliegen, die Verarbeitung ganzer Dateien mit `-J`; die Aufteilung einer einzelnen Datei mit `-j` erfordert lokale Eingaben mit wahlfreiem Lesezugriff. CSV-Protokolle können über SSH gelesen werden. Im hier dokumentierten Entwicklungssnapshot nach Version 13.2 filtert der Überwachungsmodus (`-w`) CSV-Datensätze auf dem entfernten Host mit `awk`, wobei mehrzeilige Felder erhalten bleiben. Siehe die [Optionen für entfernte Eingaben](/de/pgbadger/command-line/).
- Die parallele Analyse erstellt im ausgewählten temporären Verzeichnis Dateien mit Namen wie `tmp_pgbadgerXXXX.bin` (standardmäßig im temporären Systemverzeichnis).
- Löschen Sie diese Dateien nicht, während pgBadger läuft. Verwenden Sie `--tempdir`, um sie auf einem Speichermedium mit ausreichender Kapazität abzulegen.
- Beginnen Sie mit einer moderaten Anzahl von Workern und überwachen Sie CPU-Auslastung, Lesedurchsatz, Verbrauch an temporärem Speicherplatz und Laufzeit.
