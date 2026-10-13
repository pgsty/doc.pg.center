---
title: Dateien der persistenten Speicherung in etcd
weight: 2650
description: Referenz der persistenten Speicherformate und Dateien
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/persistent-storage-files.md"
aliases: [/etcd/learning/persistent-storage-files/]
---

Dieses Dokument erläutert das Format der persistenten Speicherung in etcd: Benennung, Inhalt und Werkzeuge, mit denen Entwickler die Dateien untersuchen können. Künftig sollte es um Änderungen am Speichermodell erweitert werden. Es richtet sich an etcd-Entwickler und soll sie bei der Datenwiederherstellung unterstützen.


## Voraussetzungen {#prerequisites}

Die folgenden Artikel liefern hilfreiche Hintergrundinformationen zu diesem Dokument:

* [Überblick über das Datenmodell von etcd](/de/docs/etcd/learning/data_model/)
* [Überblick über Raft](https://raft.github.io/raft.pdf), insbesondere Abschnitt „5.3 Logreplikation“.


## Überblick {#overview}

### Langlebige Dateien {#long-leaving-files}

<table>
  <tr>
    <th>Dateiname</th>
    <th>Zweck</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>bbolt <a href="https://en.wikipedia.org/wiki/B%2B_tree">B+-Baum</a></strong>, der alle angewendeten Daten, Informationen zur Mitgliedschaft und Autorisierung sowie Metadaten speichert. Er kennt den zuletzt angewendeten WAL-Index (<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>).
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        Regelmäßige <strong>Snapshots des alten v2-Speichers</strong>, mit:
        <ul>
          <li>grundlegenden Mitgliedschaftsinformationen</li>
          <li>etcd-Version</li>
        </ul>
      </p>
      <p>Seit etcd v3 ist dieser Inhalt gegenüber den /snap/db-Dateien redundant.</p>
      <p>Regelmäßig (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) werden diese Dateien <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">bereinigt</a>, wobei die letzten <code>--max-snapshots=5</code> erhalten bleiben.</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>Ein vollständiger <strong>heruntergeladener bbolt-Snapshot</strong> vom etcd-Leader, falls das Replikat zu weit zurücklag.</p>
      <p>Enthält dieselbe Art von Daten wie die Datei (<code>./member/snap/db</code>).</p>
      <p>
        Die Datei wird in 2 Fällen verwendet:
        <ul>
          <li>Als Antwort auf die Aufforderung des Leaders zur Wiederherstellung aus dem Snapshot.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">Beim Serverstart</a>, wenn der letzte Snapshot, eine .snap.db-Datei, gefunden wird und einen neueren Index als consistent_index in der aktuellen Datei <code>snap.db</code> hat.</li>
        </ul>
        Hinweis: Regelmäßige Snapshots auf den einzelnen Replikaten werden nur als *.snap-Datei erzeugt, nicht als snap.db-Datei. Daher ist nicht garantiert, dass der neueste Snapshot im WAL eine *.snap.db-Datei besitzt. In diesem Fall wird jedoch erwartet, dass das Backend snap/db neuer ist als der Snapshot.
      </p>
      <p>
        Die Datei <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">wird nach Abschluss der Wiederherstellung nicht gelöscht</a> (der gesamte Inhalt wurde dann in ./member/snap/db übernommen). Regelmäßig (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) werden die Dateien <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">bereinigt</a>.
Auch hier bleiben <code>--max-snapshots=5</code> erhalten. Da diese Dateien O(GBs) groß sein können, besteht die Gefahr, dass der Datenträgerspeicher ausgeht.
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Write-Ahead-Logs von Raft</strong>, mit aktuellen von Raft akzeptierten Transaktionen, regelmäßigen Snapshots oder CRC-Einträgen.</p>
      <p>Die neuesten <code>--max-wals=5</code> Dateien bleiben erhalten. Jede dieser Dateien ist <code>~64*10^6</code> Bytes groß. Bei Überschreiten dieser fest codierten Größe wird eine neue Datei begonnen. Die Dateien können deshalb etwas größer werden; die vorab zugewiesene Datei <code>0.tmp</code> schützt daher nicht vollständig vor einer Überschreitung des verfügbaren Datenträgerspeichers.</p>
      <p>Bei zu seltenen Snapshots können mehr als <code>--max-wals=5</code> Dateien vorhanden sein, da Sperren auf Dateisystemebene sie vor vorzeitiger Löschung schützen.</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>Vorab zugewiesener Speicherplatz</strong> für die nächste Write-Ahead-Log-Datei.
      Verhindert, dass Raft wegen fehlender WAL-Kapazität blockiert, ohne einen Alarm auslösen zu können.
    </td>
  </tr>
</table>


### Temporäre Dateien {#temporary-files}

Während der internen Verarbeitung von etcd können mehrere kurzlebige Dateien auftreten:

<table>
  <tr>
    <th>Datei</th>
    <th>Zweck</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>Snapshot-Dateien werden in „broken“ umbenannt, wenn sie nicht <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">geladen werden können</a>.<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>Der Versuch, die neueste Datei zu laden, erfolgt, wenn etcd <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">gestartet wird</a>.</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>Oder während der backup/migrate-Befehle von etcdctl.</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">Temporäre</a> bbolt-Datei, die auf Replikaten als Antwort auf die msgSnap-Anfrage des Leaders erstellt wird, also auf dessen Aufforderung, den Speicher aus dem angegebenen Snapshot wiederherzustellen.</p>
      <p>
        Nach erfolgreichem vollständigem Abruf des Inhalts wird die Datei <a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">umbenannt</a> in: <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>. Stürzt der Server während des Herunterladens ab oder wird er beendet, bleiben die Dateien auf dem Datenträger und werden niemals automatisch bereinigt. Sie können erheblichen Umfang haben (GBs).
      </p>
      <p>Siehe <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>. <strong>In etcd 3.5 behoben.</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>Eine temporäre Datei, die während der <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">Defragmentierung</a> eine Kopie des Backend-Inhalts (/member/snap/db) enthält. Nach erfolgreichem Abschluss wird sie in /member/snap/db umbenannt und ersetzt das ursprüngliche Backend.</p>
      <p>Beim Start des etcd-Servers werden diese Dateien<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217"> bereinigt</a>.</p>
    </td>
  </tr>
</table>

## bbolt-B+-Baum: **member/snap/db** {#bbolt-btree-membersnapdb}

Diese Datei enthält die Hauptdaten von etcd, angewendet bis zu einer bestimmten Position im Raft-Log (siehe [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)).


### Physischer Aufbau {#physical-organization}

Der Speicher von „better bolt“ ist physisch als [B+-Baum](https://en.wikipedia.org/wiki/B%2B_tree) organisiert. Die physischen Seiten des B-Baums werden niemals an Ort und Stelle geändert[^1]. Stattdessen wird ihr Inhalt auf eine neue Seite kopiert, die aus der Liste freier Seiten stammt. Die alte Seite wird dieser Liste hinzugefügt, sobald keine offene Transaktion mehr auf sie zugreifen könnte. Dadurch sieht eine offene RO-Transaktion einen konsistenten historischen Speicherzustand. Die RW-Transaktion ist exklusiv und blockiert alle anderen RW-Transaktionen.  \
Große Werte werden auf mehreren zusammenhängenden Seiten gespeichert. Die Wiederverwendung von Seiten zusammen mit der nötigen Zuweisung zusammenhängender Seitenbereiche unterschiedlicher Größe kann zu einer zunehmenden Fragmentierung des bbolt-Speichers führen.

Die bbolt-Datei schrumpft niemals von selbst. Nur bei der Defragmentierung kann sie in eine neue Datei mit einem Puffer freier Seiten am Ende und verkleinerter Dateigröße umgeschrieben werden.


### Logischer Aufbau {#logical-organization}

Der bbolt-Speicher ist in Buckets unterteilt. In jedem Bucket werden Schlüssel (Paare vom Typ byte[]->value byte[]) in lexikografischer Reihenfolge gespeichert. Die folgende Liste zeigt die von etcd verwendeten Buckets mit Stand Version 3.5 und ihre Schlüssel.

<table>
  <tr>
    <th>Bucket</th>
    <th>Schlüssel</th>
    <th>Beispielwert</th>
    <th>Beschreibung</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>Zeigt an, dass bei einem Mitglied Probleme erkannt wurden.</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code> (leer) oder <code>BigEndian.PutUint64</code></td>
    <td>
      <p>Jede Änderung an Rollen oder Benutzern erhöht dieses Feld beim Bestätigen der Transaktion.</p>
      <p>
        Der Wert dient ausschließlich zur <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">optimistischen Sperrung während</a> des Autorisierungsvorgangs.
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] als Zeichenfolge</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code> serialisiert</td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] als Zeichenfolge</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code> serialisiert</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code> (string)</td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">Minor</a>-Version der durch Konsens vereinbarten gemeinsamen Speicherversion.</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>Speichert die Absicht dauerhaft, die durch die neueste Anfrage <code>Downgrade RPC</code> konfiguriert wurde.</p>
      <p>Seit v3.5</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId], kodiert mit <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}</p>
      <p>Löschungen von Schlüssel-Wert-Paaren werden mit einem abschließenden 't' als „Tombstone“ serialisiert</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> als serialisiertes Proto (<code>key, create_rev, mod_rev, version, value, lease id</code>)</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> als serialisiertes Proto (ID, TTL, RemainingTTL)</td>
    <td>
      <p>Hinweis: LeaseCheckpoint verlängert nur RemainingTTL. TTL stammt weiterhin vom ursprünglichen Grant.</p>
      <p style="text-decoration:underline;">Hinweis2: TTLs werden in Sekunden ab einem nicht definierten „jetzt“ gespeichert. Ein ständig abstürzender und neu startender Server gibt keine Leases frei!!!</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId] hexadezimal als Zeichenfolge: <code>"8e9e05c52164694d"</code></td>
    <td>
      <em>Als JSON-Zeichenfolge serialisierte <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">Member</a>-Struktur:</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>Durch Konsens vereinbarte Informationen zur Clustermitgliedschaft.</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId] hexadezimal als Zeichenfolge: <code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>IDs aller entfernten Mitglieder. Damit wird geprüft, dass ein entferntes Mitglied niemals unter derselben ID erneut hinzugefügt wird.</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">Das Feld wird derzeit (3.4) aus dem V2-Speicher und niemals aus V3 gelesen</a>. Siehe <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>uint64-Bytes (BigEndian)</td>
    <td>Repräsentiert den Offset des letzten auf den bolt-DB-Speicher angewendeten WAL-Eintrags.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} kodiert. (16 Bytes)</td>
    <td>Dient zur erneuten Initialisierung der Kompaktierung, wenn nach einer Kompaktierungsanfrage ein Absturz aufgetreten ist.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} kodiert. (16 Bytes)</td>
    <td>Revision, bis zu der der Speicher zuletzt erfolgreich kompaktiert wurde (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">Seit etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">Seit etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### Werkzeuge {#tools}


#### bbolt {#bbolt}

bbolt bietet ein Befehlszeilenwerkzeug zum Untersuchen des Dateiinhalts.

Anwendungsbeispiele:

##### Alle Buckets einer bbolt-Datei auflisten: {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### Ein bestimmtes Schlüssel-Wert-Paar lesen: {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-db kann den Inhalt des etcd-v3-Backends (bbolt) auflisten.

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

Weitere Beispiele: [https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL: Write-Ahead-Log {#wal-write-ahead-log}

Das Write-Ahead-Log ist ein persistenter Raft-Speicher für Vorschläge. Zuerst speichert der Leader den Vorschlag in seinem Log und repliziert ihn anschließend gleichzeitig über das Raft-Protokoll an die Follower. Jeder Follower speichert den Vorschlag dauerhaft in seinem WAL, bevor er dem Leader die Replikation bestätigt.

Das in etcd verwendete WAL unterscheidet sich in 2 Punkten vom kanonischen Raft-Modell:

* Es speichert nicht nur indizierte Einträge dauerhaft, sondern auch kleine Raft-Snapshots und HardState. So lässt sich der gesamte Raft-Zustand eines Mitglieds allein aus dem WAL wiederherstellen.
* Es wird nur angehängt. Einträge werden nicht an Ort und Stelle überschrieben; ein später in der Datei angehängter Eintrag mit demselben Index ersetzt den vorherigen logisch.


### Dateinamen {#file-names}

Die WAL-Dateien werden nach folgendem Muster benannt:

```
"%016x-%016x.wal", seq, index
```

Beispiel: `./member/wal/0000000000000010-00000000000bf1e6.wal`

Die Dateinamen enthalten also hexadezimal kodiert:


* Die fortlaufende Nummer der WAL-Datei
* Den Index des ersten Eintrags oder Snapshots in der Datei.
  Insbesondere enthält die erste Datei „0000000000000000-0000000000000000.wal“ den anfänglichen Snapshot-Eintrag mit index=0.

### Physischer Inhalt {#physical-content}

Die WAL-Datei enthält eine Folge von „[Frames](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)“. Jeder Frame enthält:


1. Eine in [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] kodierte uint64-Zahl mit der Länge des serialisierten [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) (3).
2. Auffüllung: Eine Anzahl von 0-Bytes, sodass die Größe des gesamten Frames ausgerichtet ist (mod 8)
3. Serialisierte [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11)-Daten:
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - Als int kodierte Aufzählung, die die Interpretation des folgenden data-Felds bestimmt
    2. data - Je nach type gewöhnlich ein serialisiertes Proto
    3. crc - CRC-32-Prüfsumme aller zusammengefassten „data“-Felder ohne type in allen Logeinträgen dieses Replikats seit Erstellung des WAL. CRC berücksichtigt ALLE Einträge, auch wenn sie nicht durch Raft bestätigt wurden.

Eine neue Datei beginnt, sobald die aktuelle Datei <code>64*10^6</code> Bytes überschreitet.


### Logischer Inhalt {#logical-content}

Auf logischer Ebene enthalten Write-Ahead-Log-Dateien:

* `Raftpb.Entry: `Aktuelle vom Raft-Leader replizierte Vorschläge. Einige gelten als bestätigt, andere können noch logisch überschrieben werden.
* `Raftpb.HardState(term,commit,vote): `Regelmäßige, sehr häufige Informationen über den Index eines bestätigten Logeintrags, der also auf die Mehrheit der Server repliziert wurde. Er wird garantiert nicht mehr geändert oder überschrieben und kann auf die Backends v2 und v3 angewendet werden. Enthalten sind außerdem ein „term“ als Hinweis auf wahlbezogene Änderungen sowie eine Stimme: das Mitglied, für das das aktuelle Replikat im aktuellen Term gestimmt hat.
* `walpb.Snapshot(term, index): `Regelmäßige Snapshots des Raft-Zustands ohne DB-Inhalt, nur mit Snapshot-Logindex und Raft-Term
    * Der Inhalt des V2-Speichers liegt in separaten *.store-Dateien.
    * Der Inhalt des V3-Speichers wird in der bbolt-Datei verwaltet und bildet einen impliziten Snapshot, sobald die Einträge dort angewendet sind.
* Ein crc32-Prüfsummeneintrag am Anfang jeder Datei, um die CRC-Prüfung für den Rest der Datei fortzusetzen.
* `etcdserverpb.Metadata(node_id, cluster_id)` - Identifiziert den Cluster und das Replikat, für die das Log steht.

Jede WAL-Datei besteht in dieser Reihenfolge aus:

1. CRC-32-Frame mit der fortlaufenden crc aller vorherigen Dateien, 0 für die erste Datei.
2. Metadaten-Frame mit Cluster- und Replikat-IDs
3. Nur für die erste WAL-Datei:

    * Leerer Snapshot-Frame (Index:0, Term: 0).
      Er stellt die Invariante sicher, dass allen Einträgen ein Snapshot vorausgeht.

   Für spätere WAL-Dateien (ab der 2.):

    * HardState-Frame.

4. Mischung aus Entry-, HardState- und Snapshot-Einträgen

Das WAL kann mehrere Einträge mit demselben Index enthalten. Dies kann in den in Abbildung 7. der [Raft-Veröffentlichung](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf) beschriebenen Fällen auftreten. Da an das etcd-WAL nur angehängt wird, werden Einträge durch Anhängen eines neuen Eintrags mit demselben Index überschrieben.

Insbesondere [ersetzt die Leselogik alte Einträge durch neuere Einträge](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462). Daher kann nur die jeweils letzte Version von Einträgen mit entry.index &lt;= HardState.commit als endgültig gelten. Einträge mit index > HardState.commit können sich noch ändern.

Es wird erwartet, dass die Terms im WAL monoton sind.

Für die Indizes im WAL wird Folgendes erwartet:

1. Sie beginnen bei einem Snapshot.
2. Nach diesem Snapshot steigen sie fortlaufend, solange sie im selben Term bleiben.
3. Bei einem Term-Wechsel kann der Index sinken, jedoch nur auf einen neuen Wert oberhalb des neuesten HardState.commit.
4. Ein neuer Snapshot kann mit jedem Index >= HardState.commit auftreten und beginnt eine neue Indexfolge.


![Dateien der persistenten Speicherung in etcd](/docs/etcd/learning/img/persistent-storage-files-figure-01.png)


### Werkzeuge {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

WAL-Dateien von etcd können mit dem Werkzeug [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs) gelesen werden:

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

Zu beachten:

* Das Werkzeug zeigt nur Entries und nicht alle WAL-Einträge wie Snapshots und HardStates in den WAL-Dateien.
* Es berücksichtigt automatisch das Überschreiben von Einträgen. Wurde ein Eintrag durch einen neueren mit demselben Index überschrieben, wird nur der endgültige Wert ausgegeben.
* Es gibt auch unbestätigte Einträge vom Ende des LOG aus, ohne Informationen zu HardState.commitIndex. Daher ist nicht erkennbar, ob diese Einträge endgültig sind.


## Snapshots des V2-Speichers: **member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### Dateinamen: {#file-names-1}

**member/snap/{term}-{index}.snap**

Die Dateinamen werden [hier](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) mit `("%016x-%016x.snap") `erzeugt und verwenden 2 hexadezimal kodierte Bestandteile:


* term -> Raft-Term, also der Zeitraum zwischen Wahlen, zum Zeitpunkt der Snapshot-Erstellung
* index -> Index des zuletzt angewendeten Vorschlags zum Zeitpunkt der Snapshot-Erstellung

### Erstellung {#creation}

Die *.snap-Dateien werden von der Methode [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68) erstellt.

Es gibt 2 Auslöser für die Erstellung dieser Dateien:


* Ungefähr alle --snapshot-count=(standardmäßig 10,000 in v3.7.0) angewendeten Vorschläge wird eine neue Datei erstellt. Dies ist nur ein Näherungswert, da Vorschläge gebündelt eintreffen können, ein Snapshot erst am Ende eines solchen Pakets geprüft und der Snapshot-Vorgang schließlich asynchron eingeplant wird.
  Der Optionsname --snapshot-count ist recht irreführend, da er die [Differenz der Indexwerte zwischen ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)dem letzten Snapshot und dem zuletzt angewendeten Vorschlag steuert.
* Raft fordert das Replikat auf, sich aus einem Snapshot wiederherzustellen. Während das Replikat den Snapshot über eine msgSnap-Nachricht empfängt, hält es ihn auch als kleinen Checkpoint im WAL fest. Damit ist garantiert, dass am Ende des WAL stets ein gültiger Snapshot gefolgt von Einträgen steht. Mögliche Lücken im WAL werden so vermieden.

Derzeit entsprechen die Dateien ungefähr[^3] im Verhältnis 1-1 den Snapshot-Einträgen im WAL. Mit der Stilllegung des v2-Speichers wird erwartet, dass diese Dateien überhaupt nicht mehr geschrieben werden, optional ab 3.5.x und verpflichtend ab 3.6.x.


### Inhalt {#content}

Die Datei enthält das serialisierte [snapdb.snapshot-Proto](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)`,

das im Feld 'data' einen [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31) enthält:

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata),

Die verschachtelten Daten enthalten schließlich den JSON-serialisierten [Inhalt des v2-Speichers](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files).


Insbesondere enthalten sind:

* Term
* Index
* Mitgliedschaftsdaten:
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* Speicherversion: /0/version-> 3.5.0


### Werkzeuge {#tools-2}


#### protoc {#protoc}

Der folgende Befehl zeigt den Dateiinhalt an, wenn er im Stammverzeichnis von etcd ausgeführt wird:


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


Ebenso lässt sich das Feld 'data' extrahieren und als [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31) dekodieren.


### Beispiel für JSON-serialisierten v2-Speicherinhalt in *.snap-Dateien von etcd 3.4: {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

```json
{
  "Root":{
    "Path":"/",
    "CreatedIndex":0,
    "ModifiedIndex":0,
    "ExpireTime":"0001-01-01T00:00:00Z",
    "Value":"",
    "Children":{
      "0":{
        "Path":"/0",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{
          "members":{
            "Path":"/0/members",
            "CreatedIndex":1,
            "ModifiedIndex":1,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"",
            "Children":{
              "8e9e05c52164694d":{
                "Path":"/0/members/8e9e05c52164694d",
                "CreatedIndex":1,
                "ModifiedIndex":1,
                "ExpireTime":"0001-01-01T00:00:00Z",
                "Value":"",
                "Children":{
                  "attributes":{
                    "Path":"/0/members/8e9e05c52164694d/attributes",
                    "CreatedIndex":2,
                    "ModifiedIndex":2,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
                    "Children":null
                  },
                  "RaftAttributes":{
                    "Path":"/0/members/8e9e05c52164694d/RaftAttributes",
                    "CreatedIndex":1,
                    "ModifiedIndex":1,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
                    "Children":null
                  }
                }
              }
            }
          },
          "version":{
            "Path":"/0/version",
            "CreatedIndex":3,
            "ModifiedIndex":3,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"3.5.0",
            "Children":null
          }
        }
      },
      "1":{
        "Path":"/1",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{


        }
      }
    }
  },
  "WatcherHub":{
    "EventHistory":{
      "Queue":{
        "Events":[
          {
            "action":"create",
            "node":{
              "key":"/0/members/8e9e05c52164694d/RaftAttributes",
              "value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
              "modifiedIndex":1,
              "createdIndex":1
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/members/8e9e05c52164694d/attributes",
              "value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
              "modifiedIndex":2,
              "createdIndex":2
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/version",
              "value":"3.5.0",
              "modifiedIndex":3,
              "createdIndex":3
            }
          }
        ]
      }
    }
  }
}
```

## Änderungen {#changes}

Dieser Abschnitt ist für die Beschreibung von Dateiformatänderungen zwischen etcd-Versionen vorgesehen.

[^1]:
     Die Metadatenseiten am Anfang der bbolt-Datei werden an Ort und Stelle geändert.

[^2]:
     Inkonsistent, da die meisten uint-Werte in Big Endian geschrieben werden

[^3]:
     Der anfängliche Snapshot mit index:0 am Anfang des WAL ist keiner *.snap-Datei zugeordnet. Zudem können alte *.snap-Dateien oder WAL-Dateien bereinigt werden.
