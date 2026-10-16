---
title: "واجهة REST API لـ Patroni"
weight: 40
icon: fa-solid fa-book
description: "مرجع لنقاط نهاية REST API في Patroni وسلوكياتها التشغيلية."
module: [PATRONI]
categories: [مرجع]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
يقدم Patroni واجهة REST API غنية، يستخدمها Patroni نفسه أثناء سباق القيادة، وتستخدمها أداة [patronictl](/ar/patroni/patronictl#patronictl) لتنفيذ عمليات تجاوز الأعطال/التبديل/إعادة التهيئة/إعادة التشغيل/إعادة التحميل، كما يستخدمها HAProxy أو أي موازن حمل آخر لإجراء فحوص الصحة عبر HTTP، وبالطبع يمكن أيضًا استخدامها للمراقبة. تجد أدناه قائمة نقاط نهاية REST API في Patroni.

--------

## نقاط نهاية فحص الصحة {#health-check-endpoints}

لكل طلبات `GET` الخاصة بفحص الصحة، يعيد Patroni مستند JSON يحمل حالة العقدة، مع رمز حالة HTTP. وإذا لم تكن تريد مستند JSON أو لم تكن بحاجة إليه، يمكنك التفكير في استخدام الأسلوب `HEAD` أو `OPTIONS` بدلًا من `GET`.

- تعيد الطلبات التالية إلى REST API الخاص بـ Patroni رمز حالة HTTP **200** فقط عندما تعمل عقدة Patroni كأساسية مع امتلاكها قفل القائد:

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader`: يعيد رمز حالة HTTP **200** فقط عندما تعمل عقدة Patroni كقائد في [عنقود استعداد](/ar/patroni/standby_cluster#standby_cluster).

- `GET /leader`: يعيد رمز حالة HTTP **200** عندما تمتلك عقدة Patroni قفل القائد. وعلى خلاف `GET /primary` و`GET /standby-leader`، لا يعتمد هذا الفحص على ما إذا كان PostgreSQL يعمل بالدور `primary` أو `standby_leader`.

- `GET /replica`: نقطة نهاية فحص صحة النسخة المتماثلة. يعيد رمز حالة HTTP **200** فقط عندما تكون عقدة Patroni في الحالة `running`، والدور `replica`، ولا يكون الوسم `noloadbalance` مضبوطًا.

- `GET /replica?replication_state=<required state>`: نقطة نهاية فحص النسخة المتماثلة. إضافةً إلى فحوص `replica`، يتحقق أيضًا مما إذا كانت حالة النسخ المتماثل مطابقة للحالة المطلوبة. وهو مفيد بشكل أساسي مع `replication_state=streaming`، لاستبعاد النسخ المتماثلة التي لا تزال تلحق أثناء الاستعادة من الأرشيف.

- `GET /replica?lag=<max-lag>`: نقطة نهاية فحص النسخة المتماثلة. إضافةً إلى فحوص `replica`، يتحقق أيضًا من زمن استجابة النسخ المتماثل ولا يعيد رمز الحالة **200** إلا عندما يكون أقل من القيمة المحددة. يُستخدم المفتاح cluster.last_leader_operation من DCS لموضع wal الخاص بالقائد وحساب زمن الاستجابة على النسخة المتماثلة لأسباب تتعلق بالأداء. يمكن تحديد max-lag بالبايت (عدد صحيح) أو بقيم مقروءة للإنسان، مثل 16kB و64MB و1GB.

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2`: نقطة نهاية فحص النسخة المتماثلة. يتحقق أيضًا من الوسمين المحددين من قبل المستخدم `key1` و`key2` ومن قيمتيهما المقابلتين في قسم **tags** من إدارة إعداد yaml. وإذا لم يكن الوسم معرّفًا لنسخة ما، أو إذا كانت القيمة في إعداد yaml لا تطابق قيمة الاستعلام، فسيعيد رمز حالة HTTP 503.

  في الطلبات التالية، وبما أننا نتحقق من حالة القائد أو قائد الاستعداد، لا يطبّق Patroni أيًّا من الوسوم المحددة من قبل المستخدم وسيتم تجاهلها.

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only`: مثل نقطة النهاية أعلاه، لكنها تشمل الأساسي أيضًا.

- `GET /synchronous` أو `GET /sync`: يعيد رمز حالة HTTP **200** فقط عندما تعمل عقدة Patroni كعقدة استعداد متزامنة.

- `GET /read-only-sync`: مثل نقطة النهاية أعلاه، لكنها تشمل الأساسي أيضًا.

- `GET /quorum`: يعيد رمز حالة HTTP **200** فقط عندما تكون عقدة Patroni هذه مدرجة كعقدة نصاب في `synchronous_standby_names` على الأساسي.

- `GET /read-only-quorum`: مثل نقطة النهاية أعلاه، لكنها تشمل الأساسي أيضًا.

- `GET /asynchronous` أو `GET /async`: يعيد رمز حالة HTTP **200** فقط عندما تعمل عقدة Patroni كعقدة استعداد غير متزامنة.

- `GET /asynchronous?lag=<max-lag>` أو `GET /async?lag=<max-lag>`: نقطة نهاية فحص عقدة الاستعداد غير المتزامنة. إضافةً إلى فحوص `asynchronous` أو `async`، يتحقق أيضًا من زمن استجابة النسخ المتماثل ولا يعيد رمز الحالة **200** إلا عندما يكون أقل من القيمة المحددة. ويُستخدم المفتاح cluster.last_leader_operation من DCS لموضع wal الخاص بالقائد وحساب زمن الاستجابة على النسخة المتماثلة لأسباب تتعلق بالأداء. ويمكن تحديد max-lag بالبايت (عدد صحيح) أو بقيم مقروءة للإنسان، مثل 16kB و64MB و1GB.

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health`: يعيد رمز حالة HTTP **200** فقط عندما يكون PostgreSQL قيد التشغيل والعمل.

- `GET /liveness`: يعيد رمز حالة HTTP **200** إذا كانت حلقة نبض قلب Patroni تعمل بشكل سليم، و**503** إذا كان آخر تشغيل لها قبل أكثر من `ttl` ثانية على الأساسي أو `2*ttl` على النسخة المتماثلة. ويمكن استخدامها لـ `livenessProbe`.

- `GET /readiness?lag=<max-lag>&mode=apply|write`: يعيد رمز حالة HTTP **200** عندما تعمل عقدة Patroni كقائد، أو عندما يكون PostgreSQL قيد التشغيل وينسخ متماثلًا وغير متأخر كثيرًا عن القائد. يحدد المعامل lag مقدار التأخر المسموح به لعقدة الاستعداد، وقيمته الافتراضية هي `maximum_lag_on_failover`. ويمكن تحديد التأخر بالبايت أو بقيم مقروءة للإنسان، مثل 16kB أو 64MB أو 1GB. أما Mode فيحدد ما إذا كان يلزم إعادة تشغيل WAL (apply) أو الاكتفاء باستلامه (write). والقيمة الافتراضية هي apply.

  عند استخدامها كـ `readinessProbe` في Kubernetes، ستضمن أن الحجيرات (pods) التي بدأت للتو لا تصبح جاهزة إلا بعد أن تلحق بالقائد. وهذا، مقترنًا بـ PodDisruptionBudget، يحمي من إنهاء القائد مبكرًا أكثر من اللازم أثناء إعادة التشغيل المتدحرجة للعقد. كما سيضمن أن النسخ المتماثلة غير القادرة على مجاراة النسخ المتماثل لا تخدم حركة القراءة فقط. ويمكن استخدام نقطة النهاية هذه لـ `readinessProbe` عندما يتعذر استخدام نقاط نهاية Kubernetes لانتخابات القائد (OpenShift).

نقطة النهاية `liveness` خفيفة جدًا ولا تنفذ أي SQL. وينبغي إعداد المجسات (probes) بحيث تبدأ في الفشل تقريبًا عند الوقت الذي تنتهي فيه صلاحية مفتاح القائد. وبالقيمة الافتراضية لـ `ttl` وهي `30s`، ستبدو المجسات كمثال كالتالي:

```yaml
readinessProbe:
  httpGet:
    scheme: HTTP
    path: /readiness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
livenessProbe:
  httpGet:
    scheme: HTTP
    path: /liveness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

--------

## نقطة نهاية المراقبة {#monitoring-endpoint}

تُستخدم نقطة النهاية `GET /patroni` من قبل Patroni أثناء سباق القيادة. كما يمكن استخدامها من قبل نظام المراقبة لديك. ويحتوي مستند JSON الذي تنتجه هذه النقطة على البنية نفسها التي يحتويها JSON الذي تنتجه نقاط نهاية فحص الصحة.

**مثال:** عنقود سليم

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "primary",
  "server_version": 160004,
  "xlog": {
    "location": 67395656
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "dcs_last_seen": 1692356718,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**مثال:** عنقود غير مقفل

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "received_location": 67419744,
    "replayed_location": 67419744,
    "replayed_timestamp": null,
    "paused": false
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**مثال:** عنقود غير مقفل مع تفعيل [وضع الحماية من فشل DCS](/ar/patroni/dcs_failsafe_mode#dcs_failsafe_mode)

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "failsafe_mode_is_active": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**مثال:** عنقود مع تفعيل [وضع الإيقاف المؤقت](/ar/patroni/pause#pause)

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "pause": true,
  "dcs_last_seen": 1724874295,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

استرجع مقاييس Patroni بصيغة Prometheus عبر نقطة النهاية `GET /metrics`.

``` bash
$ curl http://localhost:8008/metrics

# HELP patroni_version Patroni semver without periods. \
# TYPE patroni_version gauge
patroni_version{scope="batman",name="patroni1"} 040000
# HELP patroni_postgres_running Value is 1 if Postgres is running, 0 otherwise.
# TYPE patroni_postgres_running gauge
patroni_postgres_running{scope="batman",name="patroni1"} 1
# HELP patroni_postmaster_start_time Epoch seconds since Postgres started.
# TYPE patroni_postmaster_start_time gauge
patroni_postmaster_start_time{scope="batman",name="patroni1"} 1724873966.352526
# HELP patroni_primary Value is 1 if this node is the leader, 0 otherwise.
# TYPE patroni_primary gauge
patroni_primary{scope="batman",name="patroni1"} 1
# HELP patroni_xlog_location Current location of the Postgres transaction log, 0 if this node is not the leader.
# TYPE patroni_xlog_location counter
patroni_xlog_location{scope="batman",name="patroni1"} 22320573386952
# HELP patroni_standby_leader Value is 1 if this node is the standby_leader, 0 otherwise.
# TYPE patroni_standby_leader gauge
patroni_standby_leader{scope="batman",name="patroni1"} 0
# HELP patroni_replica Value is 1 if this node is a replica, 0 otherwise.
# TYPE patroni_replica gauge
patroni_replica{scope="batman",name="patroni1"} 0
# HELP patroni_sync_standby Value is 1 if this node is a sync standby replica, 0 otherwise.
# TYPE patroni_sync_standby gauge
patroni_sync_standby{scope="batman",name="patroni1"} 0
# HELP patroni_quorum_standby Value is 1 if this node is a quorum standby replica, 0 otherwise.
# TYPE patroni_quorum_standby gauge
patroni_quorum_standby{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_received_location Current location of the received Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_received_location counter
patroni_xlog_received_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_location Current location of the replayed Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_replayed_location counter
patroni_xlog_replayed_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_timestamp Current timestamp of the replayed Postgres transaction log, 0 if null.
# TYPE patroni_xlog_replayed_timestamp gauge
patroni_xlog_replayed_timestamp{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_paused Value is 1 if the Postgres xlog is paused, 0 otherwise.
# TYPE patroni_xlog_paused gauge
patroni_xlog_paused{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_streaming Value is 1 if Postgres is streaming, 0 otherwise.
# TYPE patroni_postgres_streaming gauge
patroni_postgres_streaming{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_in_archive_recovery Value is 1 if Postgres is replicating from archive, 0 otherwise.
# TYPE patroni_postgres_in_archive_recovery gauge
patroni_postgres_in_archive_recovery{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_server_version Version of Postgres (if running), 0 otherwise.
# TYPE patroni_postgres_server_version gauge
patroni_postgres_server_version{scope="batman",name="patroni1"} 160004
# HELP patroni_cluster_unlocked Value is 1 if the cluster is unlocked, 0 if locked.
# TYPE patroni_cluster_unlocked gauge
patroni_cluster_unlocked{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_is_active Value is 1 if failsafe mode is active, 0 otherwise.
# TYPE patroni_failsafe_mode_is_active gauge
patroni_failsafe_mode_is_active{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_enabled Value is 1 if failsafe_mode is enabled, 0 otherwise.
# TYPE patroni_failsafe_mode_enabled gauge
patroni_failsafe_mode_enabled{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_member Value is 1 if this node is a member of failsafe, 0 otherwise.
# TYPE patroni_failsafe_member gauge
patroni_failsafe_member{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_timeline Postgres timeline of this node (if running), 0 otherwise.
# TYPE patroni_postgres_timeline gauge
patroni_postgres_timeline{scope="batman",name="patroni1"} 24
# HELP patroni_dcs_last_seen Epoch timestamp when DCS was last contacted successfully by Patroni.
# TYPE patroni_dcs_last_seen gauge
patroni_dcs_last_seen{scope="batman",name="patroni1"} 1724874235
# HELP patroni_pending_restart Value is 1 if the node needs a restart, 0 otherwise.
# TYPE patroni_pending_restart gauge
patroni_pending_restart{scope="batman",name="patroni1"} 1
# HELP patroni_is_paused Value is 1 if auto failover is disabled, 0 otherwise.
# TYPE patroni_is_paused gauge
patroni_is_paused{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_state Numeric representation of Postgres state.
# Values: 0=initdb, 1=initdb_failed, 2=custom_bootstrap, 3=custom_bootstrap_failed, 4=creating_replica, 5=running, 6=starting, 7=bootstrap_starting, 8=start_failed, 9=restarting, 10=restart_failed, 11=stopping, 12=stopped, 13=stop_failed, 14=crashed
# TYPE patroni_postgres_state gauge
patroni_postgres_state{scope="batman",name="patroni1"} 5
# HELP patroni_failover_priority Failover priority of this node.
# TYPE patroni_failover_priority gauge
patroni_failover_priority{scope="batman",name="patroni1"} 1
```

### قيم حالة PostgreSQL {#postgresql-state-values}

يوفر المقياس `patroni_postgres_state` تمثيلًا رقميًا للحالة الحالية لنسخة PostgreSQL. وهذا مفيد لأنظمة المراقبة والتنبيه التي تحتاج إلى تتبع تغييرات الحالة عبر الزمن. وتُولَّد القيم الرقمية باستخدام الدالة الساكنة `PostgresqlState.get_metrics_description()`.

| القيمة | اسم الحالة              | الوصف                                |
|-------|-------------------------|--------------------------------------|
| 0     | initdb                  | تهيئة عنقود جديد                     |
| 1     | initdb_failed           | فشل تهيئة العنقود الجديد             |
| 2     | custom_bootstrap        | تشغيل نص تهيئة أولية مخصص            |
| 3     | custom_bootstrap_failed | فشل نص التهيئة الأولية المخصص        |
| 4     | creating_replica        | إنشاء نسخة متماثلة من الأساسي        |
| 5     | running                 | PostgreSQL يعمل بشكل طبيعي           |
| 6     | starting                | PostgreSQL في طور البدء              |
| 7     | bootstrap_starting      | البدء بعد تهيئة أولية مخصصة          |
| 8     | start_failed            | فشل بدء تشغيل PostgreSQL             |
| 9     | restarting              | PostgreSQL يعيد التشغيل              |
| 10    | restart_failed          | فشل إعادة تشغيل PostgreSQL           |
| 11    | stopping                | PostgreSQL في طور التوقف             |
| 12    | stopped                 | PostgreSQL متوقف                     |
| 13    | stop_failed             | فشل إيقاف PostgreSQL                 |
| 14    | crashed                 | انهيار PostgreSQL                    |

قيم حالة PostgreSQL

> [!NOTE]
> هذه القيم الرقمية ثابتة ولن تتغير أبدًا للحفاظ على التوافق المتراجع مع أنظمة المراقبة القائمة. وإذا أُضيفت حالات جديدة في المستقبل، فسيُخصص لها قيم رقمية جديدة دون تغيير القيم الموجودة.

--------

## نقاط نهاية حالة العنقود {#cluster-status-endpoints}

- تولّد نقطة النهاية `GET /cluster` مستند JSON يصف طوبولوجيا العنقود وحالته الحالية:

``` bash
$ curl -s http://localhost:8008/cluster | jq .
{
  "members": [
    {
      "name": "patroni1",
      "role": "leader",
      "state": "running",
      "api_url": "http://10.89.0.4:8008/patroni",
      "host": "10.89.0.4",
      "port": 5432,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      }
    },
    {
      "name": "patroni2",
      "role": "replica",
      "state": "streaming",
      "api_url": "http://10.89.0.6:8008/patroni",
      "host": "10.89.0.6",
      "port": 5433,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      },
      "receive_lag": 0,
      "receive_lsn": "0/4000060",
      "replay_lag": 0,
      "replay_lsn": "0/4000060",
      "lag": 0,
      "lsn": "0/4000060"
    }
  ],
  "scope": "demo",
  "scheduled_switchover": {
    "at": "2023-09-24T10:36:00+02:00",
    "from": "patroni1",
    "to": "patroni3"
  }
}
```

- توفر نقطة النهاية `GET /history` عرضًا لتاريخ عمليات التبديل/تجاوز الأعطال في العنقود. وتشبه صيغته إلى حد كبير محتوى ملفات المحفوظات في دليل `pg_wal`. والفرق الوحيد هو حقل الطابع الزمني الذي يظهر متى أُنشئ الخط الزمني الجديد.

``` bash
$ curl -s http://localhost:8008/history | jq .
[
  [
    1,
    25623960,
    "no recovery target specified",
    "2019-09-23T16:57:57+02:00"
  ],
  [
    2,
    25624344,
    "no recovery target specified",
    "2019-09-24T09:22:33+02:00"
  ],
  [
    3,
    25624752,
    "no recovery target specified",
    "2019-09-24T09:26:15+02:00"
  ],
  [
    4,
    50331856,
    "no recovery target specified",
    "2019-09-24T09:35:52+02:00"
  ]
]
```

<a id="config_endpoint"></a>

--------

## نقطة نهاية الإعداد {#config-endpoint}

`GET /config`: الحصول على النسخة الحالية من الإعداد الديناميكي:

``` bash
$ curl -s http://localhost:8008/config | jq .
{
  "ttl": 30,
  "loop_wait": 10,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "100"
    }
  }
}
```

`PATCH /config`: تغيير الإعداد القائم.

``` bash
$ curl -s -XPATCH -d \
    '{"loop_wait":5,"ttl":20,"postgresql":{"parameters":{"max_connections":"101"}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "101"
    }
  }
}
```

يقوم استدعاء REST API أعلاه بترقيع الإعداد القائم ويعيد الإعداد الجديد.

لنتحقق من أن العقدة عالجت هذا الإعداد. أولًا، ينبغي أن تبدأ بطباعة أسطر السجل كل 5 ثوانٍ (loop_wait=5). ويتطلب تغيير "max_connections" إعادة تشغيل، لذا ينبغي كشف العلامة "pending_restart":

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "xlog": {
    "location": 2197818976
  },
  "timeline": 1,
  "dcs_last_seen": 1724874545,
  "database_system_identifier": "7408277255830290455",
  "pending_restart": true,
  "pending_restart_reason": {
    "max_connections": {
      "old_value": "100",
      "new_value": "101"
    }
  },
  "patroni": {
    "version": "4.0.0",
    "scope": "batman",
    "name": "patroni1"
  },
  "state": "running",
  "role": "primary",
  "server_version": 160004
}
```

إزالة المعاملات:

إذا أردت إزالة (إعادة ضبط) إعداد ما، فما عليك إلا ترقيعه بقيمة `null`:

``` bash
$ curl -s -XPATCH -d \
    '{"postgresql":{"parameters":{"max_connections":null}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5
    }
  }
}
```

يزيل الاستدعاء أعلاه `postgresql.parameters.max_connections` من الإعداد الديناميكي.

`PUT /config`: من الممكن أيضًا إجراء إعادة كتابة كاملة وغير مشروطة للإعداد الديناميكي القائم:

``` bash
$ curl -s -XPUT -d \
    '{"maximum_lag_on_failover":1048576,"retry_timeout":10,"postgresql":{"use_slots":true,"use_pg_rewind":true,"parameters":{"hot_standby":"on","wal_level":"hot_standby","unix_socket_directories":".","max_wal_senders":5}},"loop_wait":3,"ttl":20}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5
    },
    "use_pg_rewind": true
  },
  "loop_wait": 3
}
```

--------

## نقاط نهاية التبديل وتجاوز الأعطال {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### التبديل (switchover) {#switchover}

تعمل نقطة النهاية `/switchover` فقط عندما يكون العنقود سليمًا (أي عندما يوجد قائد). كما تتيح جدولة عملية تبديل في وقت محدد.

عند استدعاء نقطة النهاية `/switchover` يمكن تحديد عقدة مرشحة لكنه غير مطلوب، بخلاف نقطة النهاية `/failover`. وإذا لم تُحدد عقدة مرشحة، فستشارك جميع العقد المؤهلة في العنقود في سباق القيادة بعد تنحّي القائد.

في جسم JSON لطلب `POST` يجب تحديد الحقل `leader`. أما الحقلان `candidate` و`scheduled_at` فهما اختياريان ويمكن استخدامهما لجدولة تبديل في وقت محدد.

بحسب الموقف، قد تعيد الطلبات رموز حالات HTTP وأجسامًا مختلفة. ويُعاد رمز الحالة **200** عند اكتمال التبديل أو تجاوز الأعطال بنجاح. وإذا تمت جدولة التبديل بنجاح، سيعيد Patroni رمز حالة HTTP **202**. وفي حال حدوث خطأ ما، سيُعاد رمز حالة الخطأ (أحد **400** أو **412** أو **503**) مع بعض التفاصيل في جسم الاستجابة.

يمكن استخدام `DELETE /switchover` لحذف التبديل المجدول حاليًا.

**مثال:** تنفيذ تبديل إلى أي عقدة استعداد سليمة

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**مثال:** تنفيذ تبديل إلى عقدة محددة

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**مثال:** جدولة تبديل من القائد إلى أي عقدة استعداد سليمة أخرى في العنقود في وقت محدد.

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### تجاوز الأعطال (failover) {#failover}

يمكن استخدام نقطة النهاية `/failover` لإجراء تجاوز أعطال يدوي عندما لا توجد عقد سليمة (مثلًا إلى عقدة استعداد غير متزامنة إذا كانت جميع عقد الاستعداد المتزامنة غير سليمة بما يكفي للترقية). ومع ذلك، لا يوجد شرط ألا يكون للعنقود قائد — فيمكن تشغيل تجاوز الأعطال أيضًا على عنقود سليم.

في جسم JSON لطلب `POST` يجب تحديد الحقل `candidate`. وإذا حُدد الحقل `leader`، فسيُستثار تبديل بدلًا من ذلك.

**مثال:**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!WARNING]
> [كن حذرًا للغاية](/ar/patroni/rest_api#failover_healthcheck) عند استخدام نقطة النهاية هذه، إذ قد تتسبب في فقدان بيانات في بعض الحالات. وفي معظم الحالات، تلبي [نقطة نهاية التبديل](/ar/patroni/rest_api#switchover_api) احتياجات المسؤول.

تُستخدم نقطتا النهاية `POST /switchover` و`POST /failover` من قبل [patronictl_switchover](/ar/patroni/patronictl#patronictl_switchover) و[patronictl_failover](/ar/patroni/patronictl#patronictl_failover) على التوالي.

تُستخدم `DELETE /switchover` من قبل [patronictl flush cluster-name switchover](/ar/patroni/patronictl#patronictl_flush_parameters).

|                              | تجاوز الأعطال | التبديل                                   |
|------------------------------|----------|------------------------------------|
| يتطلب تحديد القائد    | لا       | نعم                                |
| يتطلب تحديد عقدة مرشحة | نعم      | لا                                 |
| يمكن تشغيله أثناء الإيقاف المؤقت | نعم | نعم (إلى عقدة مرشحة محددة فقط)     |
| يمكن جدولته             | لا       | نعم (إذا لم يكن الإيقاف المؤقت مفعلًا) |

مقارنة بين تجاوز الأعطال والتبديل

<a id="failover_healthcheck"></a>

### عقدة الاستعداد السليمة {#healthy-standby}

هناك عدد من الفحوص التي ينبغي أن يجتازها عضو في العنقود ليتمكن من المشاركة في سباق القيادة أثناء تبديل، أو ليصبح قائدًا كعقدة مرشحة لتجاوز الأعطال/التبديل:

- أن يكون قابلًا للوصول عبر واجهة Patroni API؛
- ألا يكون الوسم `nofailover` مضبوطًا لديه على `true`؛
- أن يكون المراقب (watchdog) يعمل بكامل وظائفه (إذا كان الإعداد يتطلب ذلك)؛
- في حالة تبديل في عنقود سليم أو تجاوز أعطال تلقائي، ألا يتجاوز الحد الأقصى لتأخر النسخ المتماثل (`maximum_lag_on_failover` [معامل الإعداد](/ar/patroni/config/dynamic#dynamic))؛
- في حالة تبديل في عنقود سليم أو تجاوز أعطال تلقائي، ألا يكون رقم خطه الزمني أصغر من الخط الزمني للعنقود إذا كان [معامل الإعداد](/ar/patroni/config/dynamic#dynamic) `check_timeline` مضبوطًا على `true`؛
- في [النمط المتزامن](/ar/patroni/replication_modes#synchronous_mode):
  - في حالة التبديل (مع عقدة مرشحة ومن دونها على حد سواء): أن يكون مدرجًا ضمن أعضاء المفتاح `/sync`؛
  - أما في تجاوز الأعطال، في العناقيد السليمة وغير السليمة على حد سواء، فيُهمل هذا الفحص.

> [!WARNING]
> في حالة تجاوز أعطال يدوي في عنقود بلا قائد، سيُسمح للعقدة المرشحة بالترقية حتى لو:
>
> - لم تكن ضمن أعضاء المفتاح `/sync` عندما يكون النمط المتزامن مفعلًا؛
> - تجاوز تأخرها الحد الأقصى المسموح به لتأخر النسخ المتماثل؛
> - كان رقم خطها الزمني أصغر من آخر خط زمني معروف للعنقود.

<a id="restart_endpoint"></a>

--------

## نقطة نهاية إعادة التشغيل {#restart-endpoint}

- `POST /restart`: يمكنك إعادة تشغيل Postgres على عقدة محددة بتنفيذ استدعاء `POST /restart`. وفي جسم JSON لطلب `POST` يمكن تحديد بعض شروط إعادة التشغيل اختياريًا:
  - **restart_pending**: قيمة منطقية، إذا ضُبطت على `true` فسيعيد Patroni تشغيل PostgreSQL فقط عندما تكون إعادة التشغيل معلقة لتطبيق بعض التغييرات على إعداد PostgreSQL.
  - **role**: تنفيذ إعادة التشغيل فقط إذا تطابق الدور الحالي للعقدة مع الدور الوارد في طلب POST.
  - **postgres_version**: تنفيذ إعادة التشغيل فقط إذا كان إصدار postgres الحالي أقدم من الإصدار المحدد في طلب POST.
  - **timeout**: المدة التي ينبغي انتظارها قبل أن يبدأ PostgreSQL بقبول الاتصالات. يتجاوز هذا `primary_start_timeout`.
  - **schedule**: طابع زمني مع المنطقة الزمنية، لجدولة إعادة التشغيل في وقت لاحق.
- `DELETE /restart`: حذف إعادة التشغيل المجدولة

تُستخدم نقطتا النهاية `POST /restart` و`DELETE /restart` من قبل [patronictl_restart](/ar/patroni/patronictl#patronictl_restart) و[patronictl flush cluster-name restart](/ar/patroni/patronictl#patronictl_flush_parameters) على التوالي.

<a id="reload_endpoint"></a>

--------

## نقطة نهاية إعادة التحميل {#reload-endpoint}

يأمر استدعاء `POST /reload` Patroni بإعادة قراءة ملف الإعداد وتطبيقه. وهذا يعادل إرسال الإشارة `SIGHUP` إلى عملية Patroni. وفي حال غيّرت بعض معاملات Postgres التي تتطلب إعادة تشغيل (مثل **shared_buffers**)، فلا يزال عليك تنفيذ إعادة تشغيل Postgres صراحةً إما باستدعاء نقطة النهاية `POST /restart` أو بمساعدة [patronictl_restart](/ar/patroni/patronictl#patronictl_restart).

تُستخدم نقطة نهاية إعادة التحميل من قبل [patronictl_reload](/ar/patroni/patronictl#patronictl_reload).

--------

## نقطة نهاية إعادة التهيئة {#reinitialize-endpoint}

`POST /reinitialize`: إعادة تهيئة دليل بيانات PostgreSQL على العقدة المحددة. يُسمح بتنفيذها على النسخ المتماثلة فقط. وبمجرد استدعائها، ستزيل دليل البيانات وتبدأ `pg_basebackup` أو بعض [طرق إنشاء النسخة المتماثلة](/ar/patroni/replica_bootstrap#custom_replica_creation) البديلة.

قد يفشل الاستدعاء إذا كان Patroni في حلقة محاولة استعادة (إعادة تشغيل) Postgres فاشل. ولتجاوز هذه المشكلة يمكن تحديد `{"force":true}` في جسم الطلب.

يمكنك تحديد {"from-leader":true} في جسم الطلب للحصول على النسخة الاحتياطية الأساسية مباشرةً من عقدة القائد. وهذا مفيد عند تنفيذ إعادة التهيئة أثناء فشل جميع عقد النسخ المتماثلة.

تُستخدم نقطة نهاية إعادة التهيئة من قبل [patronictl_reinit](/ar/patroni/patronictl#patronictl_reinit).
