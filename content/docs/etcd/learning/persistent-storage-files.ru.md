---
title: Файлы постоянного хранилища etcd
weight: 2650
description: Справочник по формату и файлам постоянного хранилища
categories: [Концепция]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/persistent-storage-files.md"
aliases: [/etcd/learning/persistent-storage-files/]
---

В этом документе описан формат постоянного хранилища etcd: именование, содержимое и инструменты, позволяющие разработчикам исследовать файлы. В дальнейшем документ следует дополнять по мере изменений модели хранения. Он предназначен для разработчиков etcd и помогает при восстановлении данных.


## Предварительные сведения {#prerequisites}

Для понимания документа полезны следующие вводные материалы:

* [обзор модели данных etcd](/ru/docs/etcd/learning/data_model/)
* [обзор Raft](https://raft.github.io/raft.pdf) (особенно раздел "5.3 Log replication").


## Обзор {#overview}

### Долгоживущие файлы {#long-leaving-files}

<table>
  <tr>
    <th>Имя файла</th>
    <th>Высокоуровневое назначение</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong><a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a> bbolt</strong>, хранящее все применённые данные, сведения об авторизации состава кластера и метаданные. Оно знает последний применённый индекс журнала WAL (<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>).
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        Периодические <strong>снимки устаревшего хранилища v2</strong>, содержащие:
        <ul>
          <li>основные сведения о составе кластера</li>
          <li>версию etcd</li>
        </ul>
      </p>
      <p>Начиная с etcd v3 их содержимое дублирует содержимое файлов /snap/db.</p>
      <p>Периодически (каждые <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) эти файлы <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">удаляются</a>, при этом сохраняются последние <code>--max-snapshots=5</code>.</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>Полный <strong>загруженный снимок bbolt</strong> с лидера etcd, если реплика отставала слишком сильно.</p>
      <p>Содержит данные того же типа, что и файл (<code>./member/snap/db</code>).</p>
      <p>
        Файл используется в 2 сценариях:
        <ul>
          <li>В ответ на запрос лидера восстановиться из снимка.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">Во время запуска сервера</a>, если найден последний снимок (файл .snap.db) и его индекс новее consistent_index в текущем файле <code>snap.db</code>.</li>
        </ul>
        Примечание: периодические снимки, создаваемые на каждой реплике, записываются только как файлы *.snap, а не snap.db. Поэтому наличие файла *.snap.db для самого нового снимка в журнале WAL не гарантируется. Однако в этом случае бэкенд (snap/db) должен быть новее снимка.
      </p>
      <p>
        Файл <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">не удаляется после завершения восстановления</a>, когда всё его содержимое перенесено в ./member/snap/db. Периодически (каждые <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) файлы <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">удаляются</a>.
Здесь также сохраняются последние <code>--max-snapshots=5</code>. Поскольку размер таких файлов может иметь порядок O(GBs), возникает риск исчерпания дискового пространства.
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Журналы предзаписи Raft</strong>, содержащие недавние транзакции, принятые Raft, периодические снимки или записи CRC.</p>
      <p>Сохраняются последние <code>--max-wals=5</code> файлов. Размер каждого составляет <code>~64*10^6</code> байтов. Файл обрезается после превышения этого жёстко заданного размера, поэтому файлы могут быть немного больше (и предварительно выделенный <code>0.tmp</code> не обеспечивает полной защиты от переполнения диска).</p>
      <p>Если снимки создаются слишком редко, файлов может быть больше <code>--max-wals=5</code>, поскольку блокировки на уровне файловой системы защищают их от слишком раннего удаления.</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>Предварительно выделенное пространство</strong> для следующего файла журнала предзаписи.
      Позволяет не допустить остановки Raft из-за нехватки места для журналов WAL без возможности активировать аварийный сигнал.
    </td>
  </tr>
</table>


### Временные файлы {#temporary-files}

Во время внутренней обработки etcd могут встречаться несколько краткоживущих файлов:

<table>
  <tr>
    <th>Файл</th>
    <th>Высокоуровневое назначение</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>Файлы снимков переименовываются в ‘broken’, если их невозможно <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">загрузить</a>.<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>Попытка загрузить самый новый файл выполняется при <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">запуске</a> etcd.</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>Либо при выполнении команд backup/migrate в etcdctl.</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">Временный</a> файл bbolt, создаваемый на репликах в ответ на запрос лидера msgSnap, то есть на требование лидера восстановить хранилище из заданного снимка.</p>
      <p>
        После успешного полного получения содержимого файл <a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">переименовывается</a> в <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>. Если сервер отказывает или принудительно завершается во время загрузки файлов, они остаются на диске и никогда не очищаются автоматически. Их размер может быть значительным (GBs).
      </p>
      <p>См. <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>. <strong>Исправлено в etcd 3.5.</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>Временный файл, содержащий копию содержимого бэкенда (/member/snap/db) во время <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">дефрагментации</a>. После её успешного завершения файл переименовывается в /member/snap/db и заменяет исходный бэкенд.</p>
      <p>При запуске сервера etcd эти файлы <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">удаляются</a>.</p>
    </td>
  </tr>
</table>

## b+tree bbolt: **member/snap/db** {#bbolt-btree-membersnapdb}

Этот файл содержит основное содержимое etcd, применённое до определённой точки журнала Raft (см. [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)).


### Физическая организация {#physical-organization}

Физически хранилище better bolt организовано как [b+tree](https://en.wikipedia.org/wiki/B%2B_tree). Физические страницы b-tree никогда не изменяются на месте[^1]. Вместо этого содержимое копируется на новую страницу, полученную из списка свободных, а старая страница добавляется в список свободных, как только не остаётся открытых транзакций, способных к ней обратиться. Благодаря этому открытая транзакция RO видит согласованное историческое состояние хранилища. Транзакция RW является исключительной и блокирует все остальные транзакции RW.  \
Большие значения хранятся на нескольких непрерывных страницах. Освобождение страниц в сочетании с необходимостью выделять непрерывные области страниц разного размера может усиливать фрагментацию хранилища bbolt.

Файл bbolt сам по себе никогда не уменьшается. Только при дефрагментации его можно переписать в новый файл с некоторым запасом свободных страниц в конце и усечённым размером.


### Логическая организация {#logical-organization}

Хранилище bbolt разделено на сегменты. В каждом сегменте ключи (пары byte[]->value byte[]) хранятся в лексикографическом порядке. Ниже перечислены сегменты, используемые etcd по состоянию на версию 3.5, и задействованные ключи.

<table>
  <tr>
    <th>Сегмент</th>
    <th>Ключ</th>
    <th>Пример значения</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>Указывает, что у одного из участников диагностированы проблемы.</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code> (empty) or <code>BigEndian.PutUint64</code></td>
    <td>
      <p>Любое изменение ролей или пользователей увеличивает это поле при фиксации транзакции.</p>
      <p>
        Значение используется только для <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">оптимистической блокировки во время</a> авторизации.
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] в виде строки</td>
    <td>сериализованный <code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code></td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] в виде строки</td>
    <td>сериализованный <code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code> (string)</td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">Дополнительная</a> версия общей версии хранилища, согласованной консенсусом.</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>Сохраняет намерение, заданное последним запросом <code>Downgrade RPC</code>.</p>
      <p>Начиная с v3.5</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId], закодированный с помощью <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}</p>
      <p>Удаления пар «ключ — значение» сериализуются с 't' в конце (как "Tombstone")</p>
    </td>
    <td>сериализованный proto <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> (<code>key, create_rev, mod_rev, version, value, lease id</code>)</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td>сериализованный proto <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> (ID, TTL, RemainingTTL)</td>
    <td>
      <p>Примечание: LeaseCheckpoint продлевает только RemainingTTL. TTL берётся из исходного Grant.</p>
      <p style="text-decoration:underline;">Примечание 2: TTL сохраняются в секундах (от неопределённого 'now'). Сервер в цикле аварийных перезапусков не освобождает аренды!!!</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId] в шестнадцатеричном виде как строка: <code>"8e9e05c52164694d"</code></td>
    <td>
      <em>Структура <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">Member</a>, сериализованная в JSON как строка:</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>Согласованные сведения о составе кластера.</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId] в шестнадцатеричном виде как строка: <code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>Идентификаторы всех удалённых участников. Используются для проверки, что удалённый участник никогда не добавляется снова с тем же идентификатором.</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">Сейчас (3.4) поле читается из хранилища V2 и никогда из V3</a>. См. <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>байты uint64 (BigEndian)</td>
    <td>Представляет смещение последней записи WAL, применённой к хранилищу БД bolt.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td>закодированный <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}. (16 байтов)</td>
    <td>Используется для повторной инициализации компактизации, если после её запроса произошёл сбой.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td>закодированный <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}. (16 байтов)</td>
    <td>Ревизия, на которой недавно успешно компактизировано хранилище (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">Начиная с etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">Начиная с etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### Инструменты {#tools}


#### bbolt {#bbolt}

bbolt предоставляет инструмент командной строки для исследования содержимого файла.

Примеры использования:

##### Перечисление всех сегментов заданного файла bbolt: {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### Чтение определённой пары «ключ — значение»: {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-db позволяет перечислить содержимое бэкенда etcd v3 (bbolt).

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

Дополнительные примеры: [https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL: журнал предзаписи {#wal-write-ahead-log}

Журнал предзаписи — постоянное хранилище Raft для предложений. Сначала лидер сохраняет предложение в своём журнале, а затем параллельно реплицирует его последователям по протоколу Raft. Каждый последователь сохраняет предложение в своём WAL, прежде чем подтвердить репликацию лидеру.

Используемый в etcd журнал WAL отличается от канонической модели Raft по 2 признакам:

* Он сохраняет не только индексированные записи, но также облегчённые снимки Raft и hard-state. Поэтому полное состояние Raft участника можно восстановить только из журнала WAL.
* Он доступен только для добавления. Записи не перезаписываются на месте: добавленная позднее в файл запись с тем же индексом замещает предыдущую.


### Имена файлов {#file-names}

Файлы журнала WAL именуются по следующему шаблону:

```
"%016x-%016x.wal", seq, index
```

Пример: `./member/wal/0000000000000010-00000000000bf1e6.wal`

Таким образом, имя файла содержит в шестнадцатеричной кодировке:


* Порядковый номер файла журнала WAL
* Индекс первой записи или снимка в файле.
  В частности, первый файл “0000000000000000-0000000000000000.wal” содержит запись исходного снимка с index=0.

### Физическое содержимое {#physical-content}

Файл журнала WAL содержит последовательность «[кадров](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)». Каждый кадр содержит:


1. Закодированное в [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] значение uint64, содержащее длину сериализованной [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) (3).
2. Заполнение: некоторое количество байтов 0, обеспечивающее выравнивание размера всего кадра (mod 8)
3. Сериализованные данные [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11):
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) — перечисление в кодировке int, определяющее интерпретацию поля data ниже
    2. data — в зависимости от типа, обычно сериализованный proto
    3. crc — контрольная сумма RC-32 совокупности всех полей “data” без type во всех записях журнала этой реплики с момента создания WAL. Обратите внимание: CRC учитывает ВСЕ записи, даже если Raft их не зафиксировал.

Файлы «обрезаются» (начинается новый файл), когда текущий превышает <code>64*10^6</code> байтов.


### Логическое содержимое {#logical-content}

На логическом уровне файлы журнала предзаписи содержат:

* `Raftpb.Entry: `недавние предложения, реплицированные лидером Raft. Некоторые из них считаются зафиксированными, а остальные могут быть логически замещены.
* `Raftpb.HardState(term,commit,vote): `периодические и очень частые сведения об индексе зафиксированной записи журнала, то есть реплицированной на большинство серверов, гарантированно не подлежащей изменению или замещению и применимой к бэкендам (v2, v3). Также содержит “term”, указывающий на изменения, связанные с выборами, и vote — участника, за которого текущая реплика проголосовала в текущем сроке полномочий.
* `walpb.Snapshot(term, index): `периодические снимки состояния Raft без содержимого БД, только индекс журнала снимка и срок полномочий Raft
    * Содержимое хранилища V2 хранится в отдельных файлах *.store.
    * Содержимое хранилища V3 находится в файле bbolt и становится неявным снимком сразу после применения записей.
* запись контрольной суммы crc32 в начале каждого файла, позволяющая продолжить проверку CRC для остальной части файла.
* `etcdserverpb.Metadata(node_id, cluster_id)` — идентификаторы кластера и реплики, представленных журналом.

Каждый файл журнала WAL состоит из следующих элементов по порядку:

1. Кадр CRC-32 (накопленная crc всех предыдущих файлов, 0 для первого файла).
2. Кадр метаданных (идентификаторы кластера и реплики)
3. Только для исходного файла WAL:

    * Пустой кадр Snapshot (Index:0, Term: 0).
      Он поддерживает инвариант, согласно которому всем записям «предшествует» снимок.

   Для не исходного файла WAL (2nd+):

    * Кадр HardState.

4. Смесь записей entry, hard-state и snapshot

Журнал WAL может содержать несколько записей с одним индексом. Такая ситуация возможна в случаях, описанных на рисунке 7 [статьи о Raft](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf). Журнал WAL etcd доступен только для добавления, поэтому запись замещается добавлением новой записи с тем же индексом.

В частности, при чтении WAL [логика замещает старые записи новыми](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462). Поэтому окончательной можно считать только последнюю версию записей с entry.index &lt;= HardState.commit. Записи с index > HardState.commit могут изменяться.

Значения "terms" в журнале WAL должны быть монотонными.

Значения "indexes" в журнале WAL должны:

1. начинаться с некоторого снимка
2. последовательно расти после снимка, пока остаются в том же ‘term’
3. при изменении term индекс может уменьшиться, но только до нового значения, превышающего последний HardState.commit.
4. новый снимок может появиться с любым index >= HardState.commit, открывая новую последовательность индексов.


![etcd persistent storage files](/docs/etcd/learning/img/persistent-storage-files-figure-01.png)


### Инструменты {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

Журналы WAL etcd можно читать инструментом [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs):

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

Учитывайте следующее:

* Инструмент показывает только Entries, а не все записи WAL (Snapshots, HardStates) из файлов журнала.
* Инструмент автоматически применяет «замещения» записей. Если запись замещена более новой с тем же индексом, выводится только окончательное значение.
* Инструмент также выводит незафиксированные записи из хвоста LOG без сведений о HardState.commitIndex, поэтому неизвестно, являются ли они окончательными.


## Снимки (хранилища V2): **member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### Имена файлов: {#file-names-1}

**member/snap/{term}-{index}.snap**

Имена файлов создаются [здесь](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) по шаблону `("%016x-%016x.snap") `и содержат 2 компонента в шестнадцатеричной кодировке:


* term -> срок полномочий Raft (период между выборами) на момент создания снимка
* index -> индекс последнего применённого предложения на момент создания снимка

### Создание {#creation}

Файлы *.snap создаются методом [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68).

Создание этих файлов управляется 2 триггерами:


* Новый файл создаётся примерно каждые --snapshotCount=(по умолчанию 100'000) применённых предложений. Значение приблизительно, поскольку предложения могут поступать пакетами, создание снимка рассматривается только в конце пакета, а сам процесс планируется асинхронно.
  Имя флага (--snapshotCount) не вполне точно: он определяет [разницу значений индекса между ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)индексом последнего снимка и индексом последнего применённого предложения.
* Raft требует, чтобы реплика восстановилась из снимка. Получая снимок по сети в сообщении msgSnap, реплика также создаёт его облегчённую контрольную точку в журнале WAL. Это гарантирует, что в хвосте журналов WAL всегда находится действительный снимок с последующими записями, и предотвращает возможный разрыв непрерывности журналов.

Сейчас файлы приблизительно[^3] соответствуют записям Snapshot журналов WAL в отношении 1-1. После вывода хранилища v2 из эксплуатации запись этих файлов должна полностью прекратиться (необязательно в 3.5.x, обязательно в 3.6.x).


### Содержимое {#content}

Файл содержит сериализованный [proto snapdb.snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)`,

в поле 'data' которого находится [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31):

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata),

Наконец, вложенные данные содержат сериализованное в JSON [содержимое хранилища v2](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files).


В частности, присутствуют:

* Term
* Index
* Данные о составе кластера:
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* Версия хранилища: /0/version-> 3.5.0


### Инструменты {#tools-2}


#### protoc {#protoc}

Следующая команда позволяет просмотреть содержимое файла при выполнении из корневого каталога etcd:


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


Аналогично можно извлечь поле 'data' и декодировать его как '[Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31)`'`


### Пример сериализованного в JSON содержимого хранилища v2 в файлах *.snap etcd 3.4: {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

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

## Изменения {#changes}

Этот раздел предназначен для описания изменений форматов файлов между различными версиями etcd.

[^1]:
     Страницы метаданных в начале файла bbolt изменяются на месте.

[^2]:
     Это непоследовательно, поскольку большинство uint записываются в bigendian

[^3]:
     Исходный снимок (index:0) в начале журнала WAL не связан с файлом *.snap. Кроме того, старые файлы *.snap или журналы WAL могут удаляться.
