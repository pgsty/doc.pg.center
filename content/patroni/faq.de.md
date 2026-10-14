---
title: "Häufige Fragen"
weight: 180
icon: fa-solid fa-circle-question
description: "Häufig gestellte Fragen zum Betrieb von Patroni und zur Fehlerbehebung."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/faq.html"
---

<a id="faq"></a>
Dieser Abschnitt beantwortet die am häufigsten gestellten Fragen zu Patroni. Die Unterabschnitte behandeln jeweils unterschiedliche Themenbereiche.

Wir hoffen, dass sich damit die meisten Fragen klären lassen. Bei weiteren Fragen oder unerwarteten Problemen erläutern die Abschnitte [Austausch](/de/patroni/contributing_guidelines#chatting) und [Fehler melden](/de/patroni/contributing_guidelines#reporting_bugs), wie Unterstützung angefragt oder Probleme gemeldet werden können.

--------

## Vergleich mit anderen HA-Lösungen {#comparison-with-other-ha-solutions}

Warum benötigt Patroni einen separaten Cluster aus DCS-Knoten, während andere Lösungen wie `repmgr` ohne ihn auskommen?  
HA-Lösungen lassen sich auf verschiedene Weise implementieren, jeweils mit Vor- und Nachteilen.

Software wie `repmgr` lässt die Knoten miteinander kommunizieren, um zu entscheiden, wann Maßnahmen ergriffen werden sollten.

Patroni stützt sich dagegen auf den im DCS gespeicherten Zustand. Der DCS dient Patroni als maßgebliche Informationsquelle für die Entscheidung, was zu tun ist.

Ein separater DCS-Cluster kann die Architektur aufwendiger machen. Dieser Ansatz verringert jedoch auch die Wahrscheinlichkeit von Split-Brain-Situationen im Postgres-Cluster.

Wie unterscheidet sich Patroni bei der Verwaltung von Postgres von anderen HA-Lösungen?  
Patroni verwaltet sowohl die Hochverfügbarkeit des Postgres-Clusters als auch Postgres selbst.

Wenn noch keine Postgres-Knoten existieren, übernimmt Patroni die Initialisierung des Primärservers und der Standby-Knoten sowie die Verwaltung ihrer Postgres-Konfiguration. Existieren die Postgres-Knoten bereits, übernimmt Patroni die Verwaltung des Clusters.

Darüber hinaus verfügt Patroni über Selbstheilungsfunktionen. Wenn ein Primärserver ausfällt, führt Patroni ein Failover zu einem Replikat durch und versucht außerdem, den bisherigen Primärserver als Replikat des neuen Primärservers wieder einzubinden. Ebenso versucht Patroni, ein ausgefallenes Replikat wieder einzubinden.

Deshalb bezeichnen wir Patroni als „Vorlage für HA-Lösungen“. Es geht über die Verwaltung physischer Replikation hinaus und verwaltet Postgres als Ganzes.

--------

## DCS {#dcs}

Kann derselbe `etcd`-Cluster Daten von zwei oder mehr Patroni-Clustern speichern?  
Ja, das ist möglich!

Informationen zu einem Patroni-Cluster werden im DCS unter einem Pfad gespeichert, dessen Präfix aus den Patroni-Einstellungen `namespace` und `scope` besteht.

Solange die Kombinationen aus namespace und scope der verschiedenen Patroni-Cluster nicht kollidieren, sollte derselbe DCS-Cluster Informationen zu mehreren Patroni-Clustern speichern können.

Was geschieht, wenn verschiedene Patroni-Cluster dieselbe Kombination aus `namespace` und `scope` sowie denselben DCS-Cluster verwenden?  
Hat der zweite Cluster eine andere Postgres-Systemkennung, erkennt Patroni unter diesem DCS-Pfad inkompatible Daten. Außerhalb des Pause-Modus beendet es sich, statt den zweiten Cluster zu verwalten, weil es davon ausgeht, dass der gespeicherte Zustand zu einem anderen Cluster gehört und Patroni falsch konfiguriert wurde.

Für unterschiedliche Patroni-Cluster, die denselben DCS-Cluster nutzen, müssen unterschiedliche Kombinationen aus `namespace` / `scope` verwendet werden.

Was geschieht beim Verlust des DCS-Clusters?  
Der DCS speichert im Wesentlichen den Status und die dynamische Konfiguration des Patroni-Clusters.

Als unmittelbare Folge wechseln alle Patroni-Cluster, die diesen DCS nutzen, in den schreibgeschützten Modus – sofern [der DCS-Failsafe-Modus](/de/patroni/dcs_failsafe_mode#dcs_failsafe_mode) nicht aktiviert ist.

Was ist beim Verlust des DCS-Clusters zu tun?  
Nach dem Verlust des DCS-Clusters sind drei Ergebnisse möglich:

1.  Der DCS-Cluster wird vollständig wiederhergestellt: Auf Patroni-Seite ist nichts zu tun. Sobald der DCS-Cluster wiederhergestellt ist, sollte auch Patroni wieder funktionsfähig werden;
2.  Der DCS-Cluster wird an derselben Stelle neu erstellt, und die Endpunkte bleiben unverändert. Auf Patroni-Seite sind keine Änderungen erforderlich;
3.  Ein neuer DCS-Cluster mit anderen Endpunkten wird erstellt. Die DCS-Endpunkte müssen in der Patroni-Konfiguration jedes Patroni-Knotens aktualisiert werden.

In den Szenarien `2.` und `3.` erstellt Patroni die Statusinformationen anhand des aktuellen Cluster-Zustands neu. Außerdem stellt es die dynamische Konfiguration im DCS aus der Backup-Datei `patroni.dynamic.json` wieder her, die im Postgres-Datenverzeichnis jedes Mitglieds des Patroni-Clusters gespeichert ist.

Was geschieht, wenn die Mehrheit im DCS-Cluster verloren geht?  
Der DCS reagiert nicht mehr, woraufhin Patroni den aktuellen lesenden und schreibenden Postgres-Knoten herabstuft.

Dabei ist zu beachten: Patroni stützt seine Aktionen im Cluster auf den Zustand des DCS.

Mit dem [DCS-Failsafe-Modus](/de/patroni/dcs_failsafe_mode#dcs_failsafe_mode) lassen sich die Auswirkungen dieser Situation abmildern.

--------

## patronictl {#patronictl}

Muss [patronictl](/de/patroni/patronictl#patronictl) auf dem Patroni-Host ausgeführt werden?  
Nein, das ist nicht erforderlich.

Bei Zugriff auf den Patroni-Host ist es praktisch, [patronictl](/de/patroni/patronictl#patronictl) dort auszuführen, da dieselbe Konfigurationsdatei des Agenten `patroni` auch für [patronictl](/de/patroni/patronictl#patronictl) verwendet werden kann.

[patronictl](/de/patroni/patronictl#patronictl) ist jedoch im Wesentlichen ein Client und kann auch auf entfernten Rechnern ausgeführt werden. Es benötigt lediglich eine ausreichende Konfiguration, um den DCS und die REST API der Patroni-Mitglieder zu erreichen.

Warum werden die Informationen zu einem Patroni-Mitglied nicht mehr in der Ausgabe von [`patronictl list`](/de/patroni/patronictl#patronictl_list) angezeigt?  
Die von [`patronictl list`](/de/patroni/patronictl#patronictl_list) angezeigten Informationen basieren auf dem Inhalt des DCS.

Wenn Informationen zu einem Mitglied aus dem DCS verschwunden sind, läuft der Patroni-Agent auf diesem Knoten sehr wahrscheinlich nicht mehr oder kann nicht mit dem DCS kommunizieren.

Da das Mitglied die Informationen nicht aktualisieren kann, laufen sie im DCS schließlich ab. Folglich erscheint das Mitglied nicht mehr in der Ausgabe von [`patronictl list`](/de/patroni/patronictl#patronictl_list).

Warum sind die Informationen zu einem Patroni-Mitglied in der Ausgabe von [`patronictl list`](/de/patroni/patronictl#patronictl_list) nicht aktuell?  
Die von [`patronictl list`](/de/patroni/patronictl#patronictl_list) angezeigten Informationen basieren auf dem Inhalt des DCS.

Standardmäßig aktualisiert Patroni diese Informationen etwa alle `loop_wait` Sekunden. Selbst wenn alles ordnungsgemäß funktioniert, können die im DCS gespeicherten Informationen also bis zu `loop_wait` Sekunden hinter dem tatsächlichen Zustand zurückliegen.

Dies gilt jedoch nicht ausnahmslos. Manche Patroni-Operationen aktualisieren die DCS-Informationen sofort.

--------

## Konfiguration {#configuration}

Was unterscheidet die dynamische von der lokalen Konfiguration?  
Die dynamische (oder globale) Konfiguration wird im DCS gespeichert und auf alle Mitglieder des Patroni-Clusters angewendet. Sie sollte der bevorzugte Ort für Konfigurationseinstellungen sein.

Knotenspezifische Einstellungen oder Werte, die die globale Konfiguration überschreiben sollen, sollten nur auf dem jeweiligen Patroni-Mitglied als lokale Konfiguration gesetzt werden. Diese lokale Konfiguration kann über die Konfigurationsdatei oder über Umgebungsvariablen festgelegt werden.

Weitere Informationen unter [Konfiguration](/de/patroni/config#config).

Welche Konfigurationsarten gibt es in Patroni, und welche haben Vorrang?  
Es gibt folgende Arten:

- Dynamische Konfiguration: gilt für alle Mitglieder;
- Lokale Konfiguration: gilt für das lokale Mitglied und überschreibt die dynamische Konfiguration;
- Umgebungskonfiguration: gilt für das lokale Mitglied und überschreibt sowohl die dynamische als auch die lokale Konfiguration.

**Hinweis:** Einige Postgres-GUCs können nur global, also über die dynamische Konfiguration, gesetzt werden. Außerdem erzwingt Patroni für manche GUCs einen fest programmierten Wert.

Weitere Informationen unter [Konfiguration](/de/patroni/config#config).

Gibt es eine Hilfe zum Erstellen der Patroni-Konfigurationsdatei?  
Ja.

Mit `patroni --generate-sample-config` kann eine Patroni-Beispielkonfiguration erstellt werden. `patroni --generate-config` erstellt eine Patroni-Konfiguration auf Basis einer bestehenden Postgres-Instanz.

Weitere Einzelheiten finden sich unter [Beispielkonfiguration erzeugen](/de/patroni/config#generate_sample_config) und [Konfiguration erzeugen](/de/patroni/config#generate_config).

Parameter unter `bootstrap.dcs` wurden geändert, aber Patroni wendet die Änderungen nicht auf die Cluster-Mitglieder an. Woran liegt das?  
Die unter `bootstrap.dcs` konfigurierten Werte werden nur bei der Initialisierung eines neuen Clusters verwendet. Während dieser Initialisierung werden sie in den DCS geschrieben.

Nach Abschluss der Initialisierung lässt sich die dynamische Konfiguration nur noch über den DCS ändern.

Weitere Einzelheiten folgen in der nächsten Frage.

Wie lässt sich die dynamische Konfiguration ändern?  
Dafür muss die Konfiguration im DCS geändert werden. Dies ist auf folgende Weise möglich:

- Über [`patronictl edit-config`](/de/patroni/patronictl#patronictl_edit_config); oder
- Mit einer `PATCH`-Anfrage an den [Konfigurationsendpunkt](/de/patroni/rest_api#config_endpoint).

Wie lässt sich die lokale Konfiguration ändern?  
Dafür muss die Konfigurationsdatei des jeweiligen Patroni-Mitglieds geändert und dem Patroni-Agenten das Signal `SIGHUP` gesendet werden. Dies ist auf folgende Weise möglich:

- Eine `POST`-Anfrage an den REST-API-[Endpunkt zum Neuladen](/de/patroni/rest_api#reload_endpoint) senden; oder

- [`patronictl reload`](/de/patroni/patronictl#patronictl_reload) ausführen; oder

- Dem Patroni-Prozess lokal das Signal `SIGHUP` senden:

  > - Wurde Patroni über systemd gestartet, kann der Befehl `systemctl reload PATRONI_UNIT.service` verwendet werden, wobei `PATRONI_UNIT` der Name des Patroni-Dienstes ist; oder
  > - Wurde Patroni auf andere Weise gestartet, muss der Prozess `patroni` ermittelt und `kill -s HUP PID` ausgeführt werden. Dabei ist `PID` die Prozess-ID des Prozesses `patroni`.

**Hinweis:** In manchen Fällen funktioniert das Neuladen mit [`patronictl reload`](/de/patroni/patronictl#patronictl_reload) möglicherweise nicht:

- Abgelaufene REST-API-Zertifikate: Dies lässt sich mit der Option `-k` von [patronictl](/de/patroni/patronictl#patronictl) umgehen;
- Falsche Zugangsdaten: beispielsweise wenn die Zugangsdaten für `restapi` oder `ctl` in der Konfigurationsdatei geändert werden und dieselbe Datei für Patroni und [patronictl](/de/patroni/patronictl#patronictl) verwendet wird.

Wie lässt sich die Umgebungskonfiguration ändern?  
Patroni liest die Umgebungskonfiguration nur beim Start ein.

Nach einer Änderung der Umgebungskonfiguration muss daher der jeweilige Patroni-Agent neu gestartet werden.

Darauf achten, kein Failover im Cluster auszulösen! Hierzu kann [`patronictl pause`](/de/patroni/patronictl#patronictl_pause) hilfreich sein.

Wie lassen sich wiederholte Heartbeat-Protokollzeilen im Normalbetrieb reduzieren?

Wenn wiederholte Zeilen wie `Lock owner: ...` und `no action. I am ...` die Protokolle überladen, `log.deduplicate_heartbeat_logs: true` konfigurieren.

Dies kann entweder in der Patroni-YAML-Datei ([Protokollierungseinstellungen](/de/patroni/config/yaml#log_settings)) oder mit `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS=true` festgelegt werden.

Dabei ist zu beachten: Das Unterdrücken wiederholter Heartbeat-Meldungen reduziert das Protokollvolumen. Es entfällt aber auch die Sicht auf den Heartbeat jedes einzelnen Schleifendurchlaufs, die bei der Diagnose eines Failovers hilfreich sein kann.

Was geschieht, wenn ein Postgres-GUC geändert wird, der ein Neuladen erfordert?  
Wenn die dynamische oder lokale Konfiguration wie in den vorherigen Fragen beschrieben geändert wird, übernimmt Patroni das Neuladen der Postgres-Konfiguration.

Was geschieht, wenn ein Postgres-GUC geändert wird, der einen Neustart erfordert?  
Patroni markiert die betroffenen Mitglieder mit dem Flag `pending restart`.

Wann und wie die Mitglieder neu gestartet werden, muss selbst festgelegt werden. Der Neustart ist auf folgende Weise möglich:

- Über [`patronictl restart`](/de/patroni/patronictl#patronictl_restart); oder
- Mit einer `POST`-Anfrage an den [Neustart-Endpunkt](/de/patroni/rest_api#restart_endpoint).

**Hinweis:** Einige Postgres-GUCs erfordern eine besondere Reihenfolge beim Neustart der Postgres-Knoten. Weitere Einzelheiten finden sich unter [GUCs für gemeinsam genutzten Speicher](/de/patroni/config#shared_memory_gucs).

Was unterscheidet `etcd` und `etcd3` in der Patroni-Konfiguration?  
`etcd` verwendet die API-Version 2 von `etcd`, während `etcd3` die API-Version 3 von `etcd` verwendet.

Zu beachten ist, dass Informationen, die mit API-Version 2 gespeichert wurden, nicht mit API-Version 3 verwaltet werden können und umgekehrt.

Die Verwendung von `etcd3` anstelle von `etcd` wird empfohlen, weil:

- API-Version 2 ab etcd v3.4 standardmäßig deaktiviert ist;
- API-Version 2 mit etcd v3.6 vollständig entfernt wurde.

`use_slots` ist in der Patroni-Konfiguration aktiviert. Wenn ein Cluster-Mitglied eine Zeit lang offline ist, wird sein Replikationsslot jedoch auf dem vorgelagerten Knoten gelöscht. Wie lässt sich das vermeiden?  
Es gibt zwei Möglichkeiten:

1.  `member_slots_ttl` kann angepasst werden (Standardwert `30min`, verfügbar seit Patroni `4.0.0` und ab PostgreSQL 11). Replikationsslots abwesender Mitglieder werden dann nicht entfernt, solange ihre Ausfallzeit unter dem konfigurierten Grenzwert liegt.
2.  Für die Mitglieder können permanente physische Replikationsslots konfiguriert werden.

Seit Patroni `3.2.0` können Slots für Mitglieder als permanente, von Patroni verwaltete Slots eingerichtet werden.

Ab PostgreSQL 11 erstellt Patroni die permanenten physischen Slots auf allen Knoten, entfernt sie nicht und rückt ihre LSN auf allen Knoten entsprechend der vom Mitglied bereits konsumierten LSN vor.

Wird das betreffende Mitglied später entfernt, liegt die Anpassung der Konfiguration permanenter Slots **in Ihrer Verantwortung**. Andernfalls behält Patroni die Slots dauerhaft bei.

**Hinweis:** Auch vor Patroni `3.2.0` konnten Slots für Mitglieder als permanente physische Slots konfiguriert werden. Sie wurden jedoch nur auf dem aktuellen Leader verwaltet. Bei einem Failover oder Switchover wurden diese Slots auf dem neuen Leader erstellt. Dies garantierte aber nicht, dass dort alle WAL-Segmente für den abwesenden Knoten vorhanden waren.

**Hinweis:** Selbst mit Patroni `3.2.0` kann eine kleine Race Condition auftreten. Direkt bei der Erstellung auf dem Replikat kann der Slot weiter fortgeschritten sein als derselbe Slot auf dem Leader. Wenn niemand den Slot konsumiert, können nach einem Failover deshalb weiterhin Dateien fehlen. Daher wird die Konfiguration kontinuierlicher Archivierung empfohlen, um benötigtes WAL wiederherstellen oder PITR durchführen zu können.

Was unterscheidet `loop_wait`, `retry_timeout` und `ttl`?  
Patroni führt regelmäßig einen sogenannten HA-Zyklus durch. Dabei prüft es den Zustand des Clusters anhand mehrerer Kontrollen und ergreift abhängig vom Ergebnis gegebenenfalls Maßnahmen, etwa ein Failover zu einem Standby.

`loop_wait` legt fest, wie lange Patroni in Sekunden vor dem nächsten HA-Prüfzyklus warten sollte.

`retry_timeout` legt die Wartezeit für Wiederholungsversuche beim DCS und bei Postgres fest. Reagiert der DCS beispielsweise länger als `retry_timeout` Sekunden nicht, kann Patroni den Primärserver vorsorglich herabstufen.

`ttl` legt die Lease-Dauer des `leader`-Locks im DCS fest. Kann der aktuelle Leader die Lease während seiner HA-Zyklen länger als `ttl` nicht erneuern, läuft sie ab. Dadurch wird eine `leader race` im Cluster ausgelöst.

**Hinweis:** Beim Ändern dieser Einstellungen ist zu beachten, dass Patroni die im Abschnitt [Dynamische Konfiguration](/de/patroni/config/dynamic#dynamic) beschriebenen Regeln und Mindestwerte erzwingt.

--------

## Verwaltung von Postgres {#postgres-management}

Können Postgres-GUCs direkt in der Postgres-Konfiguration geändert werden?  
Ja, dies sollte jedoch vermieden werden.

Patroni verwaltet die Postgres-Konfiguration und kann Änderungen an den Konfigurationsdateien später überschreiben.

Es gibt einige Möglichkeiten, die Konfiguration außerhalb der Verwaltung durch Patroni anzupassen:

- Postgres-GUCs über `$PGDATA/postgresql.base.conf` ändern; oder
- `postgresql.custom_conf` festlegen. Diese Datei wird dann anstelle von `postgresql.base.conf` verwendet und kann extern verwaltet werden; oder
- GUCs mit `ALTER SYSTEM` / `ALTER DATABASE` / `ALTER USER` ändern.

Weitere Informationen finden sich im Abschnitt [Wichtige Konfigurationsregeln](/de/patroni/config#important_configuration_rules).

In jedem Fall wird empfohlen, die gesamte Postgres-Konfiguration über Patroni zu verwalten. Das zentralisiert die Verwaltung und erleichtert bei Bedarf die Fehlersuche in Patroni.

Können Postgres-Knoten direkt neu gestartet werden?  
Nein, Postgres sollte **nicht** direkt verwaltet werden!

Jeder Versuch, den Postgres-Server ohne Patroni neu zu starten, kann ein Failover im Cluster auslösen.

Wenn der Postgres-Server verwaltet werden muss, sind dafür die von Patroni bereitgestellten Verfahren zu verwenden.

Kann Patroni die Verwaltung eines bestehenden Postgres-Clusters übernehmen?  
Ja, das ist möglich!

Eine ausführliche Anleitung findet sich unter [Bestehende Daten übernehmen](/de/patroni/existing_data#existing_data).

Wie verwaltet Patroni Postgres?  
Patroni startet und stoppt Postgres durch Aufruf der ausführbaren Postgres-Dateien wie `pg_ctl` und `postgres`.

Daher **MÜSSEN** alle anderen Instanzen deaktiviert werden, die Postgres-Cluster verwalten könnten, etwa systemd-Units wie `postgresql.service`. Nur Patroni sollte Postgres-Instanzen im Cluster starten, stoppen und hochstufen können. Andernfalls können Split-Brain-Situationen entstehen. Fällt beispielsweise der als Primärserver laufende Knoten aus und die Unit `postgresql.service` ist aktiviert, kann diese Postgres wieder starten und dadurch einen Split Brain verursachen.

--------

## Konzepte und Voraussetzungen {#concepts-and-requirements}

Welche Anwendungen gehören zu Patroni?  
Patroni wird im Wesentlichen mit zwei Anwendungen ausgeliefert:

- `patroni`: Der Patroni-Agent verwaltet einen Postgres-Knoten;
- [patronictl](/de/patroni/patronictl#patronictl): Ein Befehlszeilenwerkzeug zur Interaktion mit einem Patroni-Cluster (Switchover, Neustarts, Konfigurationsänderungen usw.). Weitere Informationen finden sich unter [patronictl](/de/patroni/patronictl#patronictl).

Was ist ein `standby cluster` in Patroni?  
Ein Cluster, in dem kein Postgres-Primärserver läuft, also kein Mitglied mit Lese- und Schreibzugriff.

Solche Cluster replizieren Daten aus einem anderen Cluster und sind in der Regel für die Replikation zwischen Rechenzentren nützlich.

Der Leader des Clusters ist ein Standby, der Änderungen von einem entfernten Postgres-Knoten repliziert. Die übrigen Standbys sind für kaskadierende Replikation von diesem Leader-Mitglied konfiguriert.

**Hinweis:** Der Standby-Cluster weiß nichts über den Quellcluster, von dem er repliziert. Er kann sogar `restore_command` anstelle von WAL-Streaming verwenden und einen vollständig unabhängigen DCS-Cluster nutzen.

Weitere Einzelheiten finden sich unter [Standby-Cluster](/de/patroni/standby_cluster#standby_cluster).

Was ist ein `leader` in Patroni?  
Ein `leader` in Patroni koordiniert gewissermaßen den Cluster.

In einem regulären Patroni-Cluster ist der `leader` der Knoten mit Lese- und Schreibzugriff.

In einem Patroni-Standby-Cluster repliziert der `leader` (auch als `standby leader` bezeichnet) von einem entfernten Postgres-Knoten und gibt diese Änderungen per kaskadierender Replikation an die anderen Mitglieder des Standby-Clusters weiter.

Benötigt Patroni eine Mindestanzahl an Postgres-Knoten im Cluster?  
Nein, Patroni kann mit beliebig vielen Postgres-Knoten betrieben werden.

Dabei ist zu beachten: Patroni ist vom DCS entkoppelt.

Was bedeutet [Pause](/de/patroni/pause#pause) in Patroni?  
Mit der von Patroni angebotenen Pause kann seine Verwaltung von Postgres vorübergehend zurückgenommen werden.

Dies ist vor allem bei Wartungsarbeiten am Cluster nützlich, wenn Patroni keine HA-Entscheidungen treffen soll, etwa ein Failover zu einem Standby beim Stoppen des Primärservers.

Weitere Informationen finden sich unter [Pause](/de/patroni/pause#pause).

--------

## Automatisches Failover {#automatic-failover}

Wie funktioniert automatisches Failover in Patroni?  
Das automatische Failover von Patroni basiert auf der sogenannten `leader race`.

Patroni speichert den Cluster-Status im DCS, darunter einen `leader`-Lock, der den Namen des Patroni-Mitglieds enthält, das aktuell der `leader` des Clusters ist.

Dieser `leader`-Lock hat eine Gültigkeitsdauer. Erneuert der Leader-Knoten die Lease des `leader`-Locks nicht rechtzeitig, läuft der Schlüssel im DCS schließlich ab.

Wenn der `leader`-Lock abläuft, wird die sogenannte `leader race` ausgelöst: Alle Knoten prüfen, ob sie die besten Kandidaten für die Übernahme der Rolle `leader` sind. Zu diesen Prüfungen gehören Aufrufe der REST API aller anderen Patroni-Mitglieder.

Alle Patroni-Mitglieder, die sich als besten Kandidaten für die Übernahme des `leader`-Locks ermitteln, versuchen, ihn zu übernehmen. Das erste Patroni-Mitglied, das den `leader`-Lock übernehmen kann, stuft sich zum Knoten mit Lese- und Schreibzugriff (oder zum `standby leader`) hoch. Die anderen werden so konfiguriert, dass sie ihm folgen.

Kann automatisches Failover im Patroni-Cluster vorübergehend deaktiviert werden?  
Ja, das ist möglich!

Dazu kann der Cluster vorübergehend pausiert werden. Dies ist typischerweise bei Wartungsarbeiten nützlich.

Um automatisches Failover wieder zu aktivieren, muss lediglich die Pause des Clusters aufgehoben werden.

Weitere Informationen finden sich unter [Pause](/de/patroni/pause#pause).

--------

## Initialisierung und Erstellung von Standbys {#bootstrapping-and-standbys-creation}

Wie erstellt Patroni einen Postgres-Primärserver und einen Postgres-Standby?  
Standardmäßig initialisiert Patroni einen neuen Cluster mit `initdb` und erstellt Standby-Knoten mit `pg_basebackup` aus einer Kopie des Mitglieds `leader`.

Dieses Verhalten lässt sich durch eigene Bootstrap-Methoden und Methoden zur Replikaterstellung anpassen.

Eigene Methoden sind beispielsweise nützlich, um Backups wiederherzustellen, die mit Werkzeugen wie pgBackRest oder Barman erstellt wurden.

Ausführliche Informationen finden sich unter [Benutzerdefinierter Bootstrap](/de/patroni/replica_bootstrap#custom_bootstrap) und [Benutzerdefinierte Replikaterstellung](/de/patroni/replica_bootstrap#custom_replica_creation).

--------

## Überwachung {#monitoring}

Wie lässt sich ein Patroni-Cluster überwachen?  
Patroni stellt über seine [REST API](/de/patroni/rest_api#rest_api) einige praktische Endpunkte bereit:

- `/metrics`: stellt Überwachungsmetriken in einem von Prometheus lesbaren Format bereit;
- `/patroni`: stellt den Status des lokalen Patroni/Postgres-Knotens im JSON-Format bereit. Die Informationen ähneln stark denen des Endpunkts `/metrics`.

Diese Endpunkte können für Überwachungsprüfungen verwendet werden.
