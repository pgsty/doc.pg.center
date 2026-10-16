---
title: ملفات التخزين الدائم لـ etcd
weight: 2650
description: مرجع لصيغة التخزين الدائم والملفات
categories: [مفهوم]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/persistent-storage-files.md"
---

يشرح هذا المستند صيغة التخزين الدائم لـ etcd: التسمية، والمحتوى، والأدوات التي تتيح للمطورين فحصها. ومستقبلًا، ينبغي توسيع هذا المستند ليعكس التغييرات على نموذج التخزين. هذا المستند موجه إلى مطوري etcd لمساعدتهم في احتياجاتهم من استعادة البيانات.


## المتطلبات المسبقة {#prerequisites}

توفر المقالات التالية معلومات أساسية مفيدة لهذا المستند:

* [نظرة عامة على نموذج بيانات etcd](/ar/etcd/learning/data_model/)
* [نظرة عامة على Raft](https://raft.github.io/raft.pdf) (خاصة قسم "5.3 Log replication").


## نظرة عامة {#overview}

### الملفات طويلة البقاء {#long-leaving-files}

<table>
  <tr>
    <th>اسم الملف</th>
    <th>الغرض العام</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>bbolt <a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a></strong> يخزن جميع البيانات المطبقة، ومعلومات تخويل العضوية والبيانات الوصفية. وهو يعرف فهرس آخر مدخلة سجل WAL مطبقة (<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>).
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        لقطات دورية <strong>لمخزن v2 القديم</strong>، تحتوي على:
        <ul>
          <li>معلومات العضوية الأساسية</li>
          <li>etcd-version</li>
        </ul>
      </p>
      <p>ابتداءً من etcd v3، المحتوى يكرر محتوى ملفات /snap/db.</p>
      <p>دوريًا (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">تُحذف</a> هذه الملفات، ويُحافَظ على آخر <code>--max-snapshots=5</code>.</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>لقطة <strong>bbolt كاملة محمّلة</strong> من قائد etcd إذا كانت النسخة المتماثلة متأخرة أكثر من اللازم.</p>
      <p>لها نوع المحتوى نفسه كملف (<code>./member/snap/db</code>).</p>
      <p>
        يُستخدم الملف في سيناريوهين:
        <ul>
          <li>استجابةً لطلب القائد بالتعافي من اللقطة.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">أثناء بدء تشغيل الخادم</a>، عندما يُعثر على آخر لقطة (ملف .snap.db) ويُكتشف أن لها فهرسًا أحدث من consistent_index في ملف <code>snap.db</code> الحالي.</li>
        </ul>
        ملاحظة: اللقطات الدورية المولدة على كل نسخة متماثلة تُبث في شكل ملف *.snap فقط (وليس ملف snap.db). لذا لا ضمان بأن اللقطة الأحدث (في سجل WAL) لها ملف *.snap.db. لكن في مثل هذه الحالة يُتوقع أن تكون الواجهة الخلفية (snap/db) أحدث من اللقطة.
      </p>
      <p>
        لا <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236">يُحذف الملف عند انتهاء التعافي</a> (لذا يُفرَّغ المحتوى كله إلى ملف ./member/snap/db). ودوريًا (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>) <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">تُحذف</a> الملفات.
هنا أيضًا يُحافَظ على <code>--max-snapshots=5</code>. ولأن هذه الملفات قد تكون بحجم O(GBs)، فقد يخلق ذلك خطر نفاد مساحة القرص.
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>سجلات الكتابة المسبقة (Write Ahead Logs) الخاصة بـ Raft</strong>، التي تحتوي المعاملات الحديثة المقبولة من Raft، ولقطات دورية أو سجلات CRC.</p>
      <p>يُحافَظ على ملفات <code>--max-wals=5</code> الحديثة. كل من هذه الملفات بحجم <code>~64*10^6</code> بايت. يُقطع الملف عند تجاوزه هذا الحجم المشفر ثابتًا، فقد تتجاوز الملفات هذا الحجم قليلًا (لذا فالتخصيص المسبق <code>0.tmp</code> لا يقدم حماية كاملة من امتلاء القرص).</p>
      <p>إذا كانت اللقطات متباعدة أكثر من اللازم، فقد يوجد أكثر من <code>--max-wals=5</code>، لأن أقفال مستوى نظام الملفات تحمي الملفات وتمنع حذفها مبكرًا أكثر من اللازم.</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>مساحة مخصصة مسبقًا</strong> لملف سجل الكتابة المسبقة التالي.
      تُستخدم لتجنب علوق Raft بسبب نقص سعة سجلات WAL دون إمكانية رفع إنذار.
    </td>
  </tr>
</table>


### الملفات المؤقتة {#temporary-files}

أثناء المعالجة الداخلية لـ etcd، من الممكن مصادفة عدة ملفات قصيرة العمر:

<table>
  <tr>
    <th>الملف</th>
    <th>الغرض العام</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>تُعاد تسمية ملفات اللقطات إلى ‘broken’ عندما تعجز عن <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">التحميل</a>.<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>تحدث محاولة تحميل أحدث ملف عندما <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">يبدأ</a> etcd.</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>أو أثناء أمري backup/migrate في etcdctl.</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">ملف مؤقت</a> (bbolt) ينشأ على النسخ المتماثلة استجابةً لطلب القائد msgSnap، أي استجابةً لمطالبة القائد باستعادة التخزين من اللقطة المعطاة.</p>
      <p>
        بعد الاسترجاع الناجح (الكامل) للمحتوى <a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">تُعاد تسمية</a> الملف إلى: <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>. وفي حالة موت الخادم أو قتله في منتصف تنزيل الملفات، تبقى الملفات على القرص ولا تُنظف تلقائيًا أبدًا. وقد تكون ضخمة الحجم (GBs).
      </p>
      <p>انظر <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>. <strong>أُصلحت في etcd 3.5.</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>ملف مؤقت يحتوي نسخة من محتوى الواجهة الخلفية (/member/snap/db)، أثناء <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">عملية إزالة التجزئة</a>. بعد نجاح العملية تُعاد تسمية الملف إلى /member/snap/db مستبدلًا الواجهة الخلفية الأصلية.</p>
      <p>عند بدء تشغيل خادم etcd، <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">تُقلَّم</a> هذه الملفات.</p>
    </td>
  </tr>
</table>

## شجرة bbolt b+: **member/snap/db** {#bbolt-btree-membersnapdb}

يحتوي هذا الملف المحتوى الرئيسي لـ etcd، المطبَّق حتى نقطة محددة من سجل Raft (انظر [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)).


### التنظيم الفيزيائي {#physical-organization}

تخزين better bolt منظم فيزيائيًا كـ[b+tree](https://en.wikipedia.org/wiki/B%2B_tree). لا تُعدَّل الصفحات الفيزيائية لشجرة b-tree في مكانها أبدًا[^1]. وبدلًا من ذلك، يُنسخ المحتوى إلى صفحة جديدة (مستردة من قائمة الصفحات الحرة) وتُضاف الصفحة القديمة إلى قائمة الصفحات الحرة فور ألا تكون هناك معاملة مفتوحة قد تلجأ إليها. وبفضل هذه العملية، ترى معاملة RO مفتوحة حالة تاريخية متسقة للتخزين. ومعاملة RW حصرية وتحجب سائر معاملات RW الأخرى.  \
تُخزن القيم الكبيرة على صفحات متتالية متعددة. وعملية استرداد الصفحات مقترنة بحاجة إلى تخصيص مناطق متجاورة من صفحات بأحجام مختلفة قد تقود إلى تزايد تجزئة تخزين bbolt.

لا يتقلص ملف bbolt من تلقاء نفسه أبدًا. فقط في عملية إزالة التجزئة، يمكن إعادة كتابة الملف إلى ملف جديد فيه بعض احتياطي الصفحات الحرة في نهايته وحجم مبتور.


### التنظيم المنطقي {#logical-organization}

ينقسم تخزين bbolt إلى حاويات (buckets). في كل حاوية تُخزن مفاتيح (أزواج byte[]->value byte[])، بالترتيب المعجمي. القائمة أدناه تمثل الحاويات التي يستخدمها etcd (اعتبارًا من الإصدار 3.5) والمفاتيح المستخدمة.

<table>
  <tr>
    <th>الحاوية</th>
    <th>المفتاح</th>
    <th>قيمة نموذجية</th>
    <th>الوصف</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a>:
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>يشير إلى أنه شُخِّصت مشكلات في أحد الأعضاء.</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code> (فارغ) أو <code>BigEndian.PutUint64</code></td>
    <td>
      <p>أي تغيير في الأدوار أو المستخدمين يزيد هذا الحقل عند تثبيت المعاملة.</p>
      <p>
        تُستخدم القيمة فقط من أجل <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461">القفل التفاؤلي خلال</a> عملية التخويل.
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] كسلسلة نصية</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code> مسلسل</td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] كسلسلة نصية</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code> مسلسل</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code> (سلسلة نصية)</td>
    <td>الإصدار <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">الفرعي</a> لنسخة التخزين المشتركة المتفق عليها بالإجماع.</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>يديم القصد المُعد من أحدث طلب: <code>Downgrade RPC</code>.</p>
      <p>منذ v3.5</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId] مرمزة باستخدام <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}</p>
      <p>تُسلسل عمليات حذف المفتاح-القيمة بوضع 't' في النهاية (بوصفها "Tombstone")</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> بروتو مسلسل (<code>key, create_rev, mod_rev, version, value, lease id</code>)</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> بروتو مسلسل (ID, TTL, RemainingTTL)</td>
    <td>
      <p>ملاحظة: LeaseCheckpoint يمدد RemainingTTL فقط. مجرد TTL هو من Grant الأصلي.</p>
      <p style="text-decoration:underline;">ملاحظة2: نديم TTLs بالثواني (من «الآن» غير المحدد). الخادم الدائر في حلقة انهيار لا يحرر عقود الإيجار!!!</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId] بالنظام الست عشري كسلسلة نصية: <code>"8e9e05c52164694d"</code></td>
    <td>
      <em>سلسلة JSON مسلسلة لبنية <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">العضو</a> (Member):</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>معلومات عضوية العنقود المتفق عليها.</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId] بالنظام الست عشري كسلسلة نصية: <code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>معرفات جميع الأعضاء المحذوفين. تُستخدم للتحقق من أن عضوًا محذوفًا لن يضاف أبدًا مجددًا بالمعرف نفسه.</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">يُقرأ الحقل حاليًا (3.4) من المخزن V2 ولا يؤخذ أبدًا من V3</a>. انظر <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>بايتات uint64 (BigEndian)</td>
    <td>يمثل إزاحة آخر مدخلة WAL مطبَّقة على تخزين bolt DB.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} مرمزة. (16 بايت)</td>
    <td>تُستخدم لإعادة تهيئة الضغط إذا حدث انهيار بعد طلب ضغط.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} مرمزة. (16 بايت)</td>
    <td>المراجعة التي ضُغط عندها المخزن بنجاح مؤخرًا (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">منذ etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">منذ etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### الأدوات {#tools}


#### bbolt {#bbolt}

لدى bbolt أداة سطر أوامر تتيح فحص محتوى الملف.

أمثلة على الاستخدام:

##### سرد جميع الحاويات في ملف bbolt المعطى: {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### قراءة زوج مفتاح/قيمة معين: {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

يمكن استخدام etcd-dump-db لسرد محتوى الواجهة الخلفية v3 لـ etcd (bbolt).

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

انظر مزيدًا من الأمثلة في: [https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL: سجل الكتابة المسبقة {#wal-write-ahead-log}

سجل الكتابة المسبقة تخزين دائم لـ Raft يُستخدم لتخزين الاقتراحات. يخزن القائد أولًا الاقتراح في سجله ثم ينسخه (بالتزامن) إلى التوابع باستخدام بروتوكول Raft. ويديم كل تابع الاقتراح في WAL الخاص به قبل تأكيد النسخ إلى القائد.

يختلف سجل WAL المستخدم في etcd عن نموذج Raft المرجعي في أمرين:

* إنه يديم ليس المدخلات المفهرسة فقط، بل أيضًا لقطات Raft (خفيفة) والحالة الصلبة (hard-state). لذا يمكن استرداد حالة Raft الكاملة للعضو من سجل WAL وحده.
* إنه للإلحاق فقط. لا تُستبدل المدخلات في مكانها، بل إن مدخلة تُلحق لاحقًا في الملف (بالفهرس نفسه) تحل محل السابقة.


### أسماء الملفات {#file-names}

تسمى ملفات سجل WAL وفق النمط التالي:

```
"%016x-%016x.wal", seq, index
```

مثال: `./member/wal/0000000000000010-00000000000bf1e6.wal`

فأسماء الملفات تحوي بترميز ست عشري:


* الرقم التسلسلي لملف سجل WAL
* فهرس أول مدخلة أو لقطة في الملف.
  على وجه الخصوص، الملف الأول “0000000000000000-0000000000000000.wal” يحمل سجل اللقطة الأولية بـ index=0.

### المحتوى الفيزيائي {#physical-content}

يحتوي ملف سجل WAL سلسلة من "[إطارات](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)". يحتوي كل إطار على:


1. [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] uint64 مرمز يحتوي طول [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) المسلسل (3).
2. الحشو: عدد من بايتات 0، بحيث يكون حجم الإطار كله محاذى (mod 8)
3. بيانات [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) المسلسلة:
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - تعداد مرمز كعدد صحيح يقود تفسير حقل البيانات أدناه
    2. data - بحسب النوع، عادة بروتو مسلسل
    3. crc - مجموع تحقق CRC-32 لجميع حقول “data” مجمعة (دون type) في جميع سجلات السجل على هذه النسخة المتماثلة تحديدًا منذ إنشاء سجل WAL. يرجى ملاحظة أن CRC يأخذ في الاعتبار جميع السجلات (حتى تلك التي لم يثبّتها Raft).

تُقطع الملفات (يبدأ ملف جديد) عندما يتجاوز الملف الحالي <code>64*10^6</code> بايت.


### المحتوى المنطقي {#logical-content}

تحتوي ملفات سجل الكتابة المسبقة في الطبقة المنطقية على:

* `Raftpb.Entry: ` اقتراحات حديثة نسخها قائد Raft. تُعتبر بعض هذه الاقتراحات ‘مثبَّتة’ والبعض الآخر عرضة للاستبدال المنطقي.
* `Raftpb.HardState(term,commit,vote): ` معلومات دورية (متواترة جدًا) عن فهرس مدخلة سجل ‘مثبَّتة’ (منسوخة إلى أغلبية الخوادم)، أي مضمونة عدم تغييرها/استبدالها وقابلة للتطبيق على الواجهات الخلفية (v2، v3). تحتوي أيضًا حقل «term» (مؤشرًا على حدوث أي تغييرات متعلقة بالانتخاب) وصوتًا - العضو الذي صوتت له النسخة المتماثلة الحالية في الدورة الحالية.
* `walpb.Snapshot(term, index): ` لقطات دورية لحالة Raft (لا محتوى قاعدة بيانات، فقط فهرس سجل اللقطة ودورة Raft)
    * محتوى المخزن V2 يُخزن في ملفات *.store منفصلة.
    * محتوى المخزن V3 يُصان في ملف bbolt، ويصير لقطة ضمنية فور تطبيق المدخلات هناك.
* سجل مجموع تحقق crc32 (في بداية كل ملف)، يستأنف فحص CRC لبقية الملف.
* `etcdserverpb.Metadata(node_id, cluster_id)` - يحدد العنقود والنسخة المتماثلة التي يمثلها السجل.

يُبنى كل ملف سجل WAL من (بالترتيب):

1. إطار CRC-32 (crc تراكمي من جميع الملفات السابقة، 0 للملف الأول).
2. إطار البيانات الوصفية (معرفا العنقود والنسخة المتماثلة)
3. لملف WAL الأولي فقط:

    * إطار لقطة فارغ (Index:0, Term: 0).
      الغرض من هذا الإطار صيانة ثابتة مفادها أن جميع المدخلات ‘تسبقها’ لقطة.

   لملف WAL غير الأولي (2+):

    * إطار HardState.

4. مزيج من مدخلات وسجلات الحالة الصلبة واللقطات

قد يحتوي سجل WAL مدخلات متعددة للفهرس نفسه. يمكن أن يحدث مثل ذلك في الحالات الموصوفة في الشكل 7 من [ورقة Raft](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf). سجل WAL في etcd للإلحاق فقط، فتُستبدل المدخلات بإلحاق مدخلة جديدة بالفهرس نفسه.

على الخصوص أثناء قراءة WAL، [يستبدل المنطق المدخلات القديمة بالأحدث](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462). وهكذا لا يمكن اعتبار إلا النسخة الأخيرة من المدخلات ذات entry.index &lt;= HardState.commit نهائية. أما المدخلات ذات الفهرس > HardState.commit فعرضة للتغيير.

«الدورات» في سجل WAL متوقع أن تكون رتيبة.

«الفهارس» في سجل WAL متوقع أن:

1. تبدأ من لقطة ما
2. تنمو تتابعيًا بعد تلك اللقطة ما دامت في ‘الدورة’ نفسها
3. إذا تغيرت الدورة، فقد ينقص الفهرس، لكن إلى قيمة جديدة أعلى من HardState.commit الأحدث.
4. قد تحدث لقطة جديدة بأي فهرس >= HardState.commit، تفتح تتابعًا جديدًا للفهارس.


![ملفات التخزين الدائم لـ etcd](/etcd/learning/img/persistent-storage-files-figure-01.png)


### الأدوات {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

يمكن قراءة سجلات WAL لـ etcd باستخدام أداة [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs):

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

انتبه إلى أن:

* تعرض الأداة المدخلات فقط، وليس كل سجلات WAL (اللقطات، HardStates) الموجودة في ملفات سجل WAL.
* تطبق الأداة تلقائيًا ‘استبدالات’ على المدخلات. فإذا استُبدلت مدخلة (بمدخلة أحدث بالفهرس نفسه)، فلن تطبع الأداة إلا القيمة النهائية.
* تطبع الأداة أيضًا المدخلات غير المثبَّتة (من ذيل السجل LOG)، دون معلومات عن HardState.commitIndex، فلا يُعرف ما إذا كانت المدخلات نهائية أم لا.


## لقطات (المخزن V2): **member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### أسماء الملفات: {#file-names-1}

**member/snap/{term}-{index}.snap**

تولَّد أسماء الملفات [هنا](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) `("%016x-%016x.snap") ` وتستخدم مركبَين مرمزين بالنظام الست عشري:


* term -> دورة Raft (الفترة بين الانتخابات) عند إصدار اللقطة
* index -> فهرس آخر اقتراح مطبَّق عند إصدار اللقطة

### الإنشاء {#creation}

تُنشأ ملفات *.snap بواسطة الدالة [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68).

هناك محفزان يتحكمان في إنشاء هذه الملفات:


* ينشأ ملف جديد كل (تقريبًا) --snapshot-count= اقتراح مطبَّق (10,000 افتراضيًا في v3.7.0). والقيمة تقريبية لأننا قد نتلقى الاقتراحات على دفعات ولا ننظر في التقاط اللقطة إلا في نهاية الدفعة، وأخيرًا لأن عملية التقاط اللقطة تجدول على نحو غير متزامن.
  اسم العلم (--snapshot-count) مضلل إلى حد بعيد لأنه يقود [الفروق في قيمة الفهرس بين ](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266)فهرس آخر لقطة وفهرس آخر اقتراح مطبَّق.
* يطلب Raft من النسخة المتماثلة التعافي من اللقطة. فبينما تتلقى النسخة المتماثلة اللقطة عبر رسالة سلكية (msgSnap)، تُديمها أيضًا (بخفة) في سجل WAL. يضمن ذلك وجود لقطة صالحة تتبعها مدخلات في ذيل سجلات WAL دومًا. فهو يكبت أي نقص محتمل في الاستمرارية في سجلات WAL.

حاليًا ترتبط الملفات تقريبًا[^3] ارتباطًا 1-1 مع مدخلات Snapshot في سجلات WAL. ومع سحب المخزن v2 من الخدمة، نتوقع توقف كتابة هذه الملفات كليًا (اختياري: 3.5.x، وإلزامي: 3.6.x).


### المحتوى {#content}

يحتوي الملف بروتو [snapdb.snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) المسلسل `(uint32 crc, bytes data)`،

الذي يحمل في حقل 'data' [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31):

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata)،

وأخيرًا تحمل البيانات المتداخلة محتوى [مخزن v2](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files) مسلسلًا بصيغة JSON.


على الخصوص هناك:

* الدورة (Term)
* الفهرس (Index)
* بيانات العضوية:
    * <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    * <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* نسخة التخزين: /0/version-> 3.5.0


### الأدوات {#tools-2}


#### protoc {#protoc}

يتيح لك الأمر التالي رؤية محتوى الملف عند تنفيذه من الدليل الجذري لـ etcd:


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


وبالمثل يمكنك استخراج حقل 'data' وفك ترميزه كـ[Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31).


### مثال لمحتوى مخزن v2 مسلسل بصيغة JSON في ملفات *.snap لـ etcd 3.4: {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

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

## التغييرات {#changes}

هذا القسم محجوز لوصف التغييرات على صيغ الملفات المدخلة بين إصدارات etcd المختلفة.

[^1]:
     تُعدَّل صفحات البيانات الوصفية في بداية ملف bbolt في مكانها.

[^2]:
     غير متسق، فأغلب uint تُكتب بالـ bigendian

[^3]:
     اللقطة الأولية (index:0) في بداية سجل WAL لا ترتبط بملف *.snap. كما قد تُحذف ملفات *.snap القديمة (أو سجلات WAL).
