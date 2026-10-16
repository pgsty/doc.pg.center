---
title: مراقبة etcd
weight: 4500
description: "مراقبة etcd لصحة النظام وتنقيح أخطاء العنقود"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/monitoring.md"
---

يوفر كل خادم etcd معلومات مراقبة محلية على منفذ العميل الخاص به عبر نقاط نهاية http. وتكون بيانات المراقبة هذه مفيدة لفحص صحة النظام ولتنقيح أخطاء العنقود في آن واحد.

## نقطة نهاية التنقيح {#debug-endpoint}

إذا ضُبط `--log-level=debug`، يصدّر خادم etcd معلومات التنقيح على منفذ العميل الخاص به تحت المسار `/debug`. واحترس عند ضبط `--log-level=debug`، إذ سيحدث تدهور في الأداء وإفراط في التسجيل.

نقطة النهاية `/debug/pprof` هي نقطة نهاية التنميط القياسية لبيئة تشغيل go. ويمكن استخدامها لتنميط استعمال المعالج والكومة (heap) وmutex وgoroutine. مثلًا، يحصل الأمر `go tool pprof` هنا على أهم 10 دوال يقضي فيها etcd وقته:

```sh
$ go tool pprof http://localhost:2379/debug/pprof/profile
Fetching profile from http://localhost:2379/debug/pprof/profile
Please wait... (30s)
Saved profile in /home/etcd/pprof/pprof.etcd.localhost:2379.samples.cpu.001.pb.gz
Entering interactive mode (type "help" for commands)
(pprof) top10
310ms of 480ms total (64.58%)
Showing top 10 nodes out of 157 (cum >= 10ms)
    flat  flat%   sum%        cum   cum%
   130ms 27.08% 27.08%      130ms 27.08%  runtime.futex
    70ms 14.58% 41.67%       70ms 14.58%  syscall.Syscall
    20ms  4.17% 45.83%       20ms  4.17%  github.com/coreos/etcd/vendor/golang.org/x/net/http2/hpack.huffmanDecode
    20ms  4.17% 50.00%       30ms  6.25%  runtime.pcvalue
    20ms  4.17% 54.17%       50ms 10.42%  runtime.schedule
    10ms  2.08% 56.25%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).AuthInfoFromCtx
    10ms  2.08% 58.33%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/etcdserver.(*EtcdServer).Lead
    10ms  2.08% 60.42%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/coreos/etcd/pkg/wait.(*timeList).Trigger
    10ms  2.08% 62.50%       10ms  2.08%  github.com/coreos/etcd/vendor/github.com/prometheus/client_golang/prometheus.(*MetricVec).hashLabelValues
    10ms  2.08% 64.58%       10ms  2.08%  github.com/coreos/etcd/vendor/golang.org/x/net/http2.(*Framer).WriteHeaders
```

تعطي نقطة النهاية `/debug/requests` آثار تتبع gRPC وإحصاءات الأداء عبر متصفح ويب. مثلًا، هذا طلب `Range` للمفتاح `abc`:

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## نقطة نهاية المقاييس {#metrics-endpoint}

يصدّر كل خادم etcd المقاييس تحت المسار `/metrics` على منفذ العميل الخاص به، واختياريًا في المواقع التي تحددها `--listen-metrics-urls`.

يمكن جلب المقاييس باستخدام `curl`:

```sh
$ curl -L http://localhost:2379/metrics | grep -v debugging # ignore unstable debugging metrics

# HELP etcd_disk_backend_commit_duration_seconds The latency distributions of commit called by backend.
# TYPE etcd_disk_backend_commit_duration_seconds histogram
etcd_disk_backend_commit_duration_seconds_bucket{le="0.002"} 72756
etcd_disk_backend_commit_duration_seconds_bucket{le="0.004"} 401587
etcd_disk_backend_commit_duration_seconds_bucket{le="0.008"} 405979
etcd_disk_backend_commit_duration_seconds_bucket{le="0.016"} 406464
...
```

## فحص الصحة {#health-check}

اعتبارًا من v3.3.0، وبالإضافة إلى الاستجابة لنقطة النهاية `/metrics`، ستستجيب أي مواقع تحددها `--listen-metrics-urls` أيضًا لنقطة النهاية `/health`. وقد يكون هذا مفيدًا إذا أُعدت نقطة النهاية القياسية بمصادقة TLS متبادلة (من جهة العميل)، بينما يظل موازن الحمل أو خدمة المراقبة بحاجة إلى الوصول إلى فحص الصحة.

اعتبارًا من v3.4، أُضيفت نقطتا نهاية جديدتان هما `/livez` و`/readyz`.

* تعكس نقطة النهاية `/livez` ما إذا كانت العملية حية أو تحتاج إلى إعادة تشغيل.
* تعكس نقطة النهاية `/readyz` ما إذا كانت العملية جاهزة لخدمة حركة البيانات.

تفاصيل تصميم نقطتَي النهاية موثقة في [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz).

تتضمن كل نقطة نهاية عدة فحوصات صحة فردية، ويمكنك استخدام المعلمة `verbose` لطباعة تفاصيل الفحوصات وحالتها، مثلًا 

```bash
curl -k http://localhost:2379/readyz?verbose
```

وسترى استجابة مشابهة لما يلي 

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

تدعم واجهة http API أيضًا استبعاد فحوصات محددة، مثلًا

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

يُعد تشغيل خدمة مراقبة [Prometheus][prometheus] أسهل طريقة لالتقاط مقاييس etcd وتسجيلها.

أولًا، ثبّت Prometheus:

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

اضبط أداة الكشط في Prometheus لاستهداف نقاط نهاية عنقود etcd:

```sh
cat > /tmp/test-etcd.yaml <<EOF
global:
  scrape_interval: 10s
scrape_configs:
  - job_name: test-etcd
    static_configs:
    - targets: ['10.240.0.32:2379','10.240.0.33:2379','10.240.0.34:2379']
EOF
cat /tmp/test-etcd.yaml
```

جهّز معالج Prometheus:

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

الآن سيكشط Prometheus مقاييس etcd كل 10 ثوانٍ.


### التنبيه {#alerting}

توجد مجموعة من [التنبيهات الافتراضية](https://github.com/etcd-io/etcd/tree/main/contrib/mixin) لعناقيد etcd v3 خاصة بـ Prometheus.

> [!NOTE]
> لاحظ أن تسميات `job` قد تحتاج إلى تعديل لتناسب حاجة معينة. وقد كُتبت القواعد لتطبَّق على عنقود واحد، لذا يوصى باختيار تسميات فريدة لكل عنقود.

### Grafana {#grafana}

يأتي [Grafana][grafana] بدعم مدمج لـ Prometheus؛ فقط أضف مصدر بيانات Prometheus:

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

ثم استورد [قالب لوحة معلومات etcd الافتراضي][template] وخصّصه. مثلًا، إذا كان اسم مصدر بيانات Prometheus هو `my-etcd`، فيجب أن تكون قيم حقل `datasource` في JSON هي `my-etcd` أيضًا.

لوحة معلومات نموذجية:

![](/etcd/op-guide/etcd-sample-grafana.png)

## التتبع الموزع {#distributed-tracing}

في v3.5 أضاف etcd دعم التتبع الموزع باستخدام [OpenTelemetry](https://github.com/open-telemetry).

> [!NOTE]
> في etcd 3.7، استخدم أعلام التتبع أدناه دون البادئة التجريبية السابقة.

لتمكين التتبع الموزع، مرِّر `--enable-distributed-tracing=true` إلى خادم etcd، مع العلم `--distributed-tracing-sampling-rate=<number>` لاختيار عدد العينات التي ستُجمع لكل مليون span، ومعدل أخذ العينات الافتراضي هو `0`.

اضبط التتبع الموزع ببدء خادم etcd بالأعلام الاختيارية التالية:

- `--distributed-tracing-address` - (اختياري) - "localhost:4317" - عنوان مجمّع التتبع (tracing collector).

- `--distributed-tracing-service-name` - (اختياري) - "etcd" - اسم خدمة التتبع الموزع، ويجب أن يكون متطابقًا عبر جميع نسخ etcd.

- `--distributed-tracing-instance-id` - (اختياري) - معرّف النسخة (Instance ID)، وهو اختياري لكن يوصى بشدة بضبطه، ويجب أن يكون فريدًا لكل نسخة etcd.

قبل تمكين التتبع الموزع، تأكد من توفر نقطة نهاية OpenTelemetry، وإذا كان هذا العنوان مختلفًا عن العنوان الافتراضي فتجاوزه بالعلم `--distributed-tracing-address`. ونظرًا إلى تعدد طرق تشغيل OpenTelemetry، راجع [وثائق المجمّع (collector)](https://opentelemetry.io/docs/collector/getting-started/) لمعرفة المزيد.

> [!NOTE]
> هناك حمل إضافي على الموارد، كما هو الحال مع أي إشارة قابلية رصد، ووفق قياساتنا الأولية قد يتراوح هذا الحمل ضمن 2% - 4% من حمل المعالج.

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /etcd/op-guide/grafana.json
