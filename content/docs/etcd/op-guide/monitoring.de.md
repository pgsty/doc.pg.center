---
title: "etcd überwachen"
weight: 4500
description: "Systemzustand überwachen und Clusterfehler in etcd untersuchen"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/monitoring.md"
aliases: [/etcd/op-guide/monitoring/]
---

Jeder etcd-Server stellt über HTTP-Endpunkte auf seinem Clientport lokale Überwachungsinformationen bereit. Diese Daten helfen sowohl bei der Prüfung des Systemzustands als auch bei der Fehlersuche im Cluster.

## Debug-Endpunkt {#debug-endpoint}

Ist `--log-level=debug` gesetzt, stellt der etcd-Server auf seinem Clientport unter dem Pfad `/debug` Informationen zur Fehlersuche bereit. `--log-level=debug` mit Bedacht setzen, da dies die Leistung beeinträchtigt und eine ausführliche Protokollierung verursacht.

Der Endpunkt `/debug/pprof` ist der standardmäßige Profiling-Endpunkt der Go-Laufzeitumgebung. Damit lassen sich CPU-, Heap-, Mutex- und Goroutine-Nutzung untersuchen. Im folgenden Beispiel ermittelt `go tool pprof` die 10 Funktionen, in denen etcd die meiste Zeit verbringt:

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

Der Endpunkt `/debug/requests` stellt gRPC-Traces und Leistungsstatistiken für einen Webbrowser bereit. Hier ist beispielsweise eine `Range`-Anfrage für den Schlüssel `abc` zu sehen:

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## Metrikendpunkt {#metrics-endpoint}

Jeder etcd-Server stellt Metriken unter dem Pfad `/metrics` auf seinem Clientport sowie optional an den mit `--listen-metrics-urls` angegebenen Adressen bereit.

Die Metriken lassen sich mit `curl` abrufen:

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

## Health Check {#health-check}

Seit v3.3.0 antworten alle mit `--listen-metrics-urls` angegebenen Adressen neben `/metrics` auch auf den Endpunkt `/health`. Dies ist hilfreich, wenn der Standardendpunkt mit gegenseitiger TLS-Authentifizierung (Clientauthentifizierung) konfiguriert ist, ein Load-Balancer oder Überwachungsdienst aber weiterhin Zugriff auf den Health Check benötigt.

Seit v3.4 gibt es die beiden neuen Endpunkte `/livez` und `/readyz`.

* Der Endpunkt `/livez` zeigt an, ob der Prozess lebt oder neu gestartet werden muss.
* Der Endpunkt `/readyz` zeigt an, ob der Prozess bereit ist, Anfragen zu bedienen.

Die Entwurfsdetails der Endpunkte sind im [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz) dokumentiert.

Jeder Endpunkt umfasst mehrere einzelne Health Checks. Mit dem Parameter `verbose` lassen sich Einzelheiten und Status der Prüfungen ausgeben, beispielsweise:

```bash
curl -k http://localhost:2379/readyz?verbose
```

Die Antwort sieht dann etwa so aus:

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

Die HTTP-API unterstützt auch den Ausschluss einzelner Prüfungen, beispielsweise:

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

Ein Überwachungsdienst mit [Prometheus][prometheus] ist der einfachste Weg, die Metriken von etcd zu erfassen und aufzuzeichnen.

Zunächst Prometheus installieren:

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

Die Endpunkte des etcd-Clusters als Abrufziele von Prometheus festlegen:

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

Den Prometheus-Handler einrichten:

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

Prometheus ruft nun alle 10 Sekunden die Metriken von etcd ab.


### Alarmierung {#alerting}

Für etcd-v3-Cluster gibt es einen Satz von [Standardalarmen](https://github.com/etcd-io/etcd/tree/main/contrib/mixin) für Prometheus.

> [!NOTE]
> Die `job`-Labels müssen möglicherweise an die jeweiligen Anforderungen angepasst werden. Die Regeln wurden für einen einzelnen Cluster geschrieben; daher werden Labels empfohlen, die für einen Cluster eindeutig sind.

### Grafana {#grafana}

[Grafana][grafana] unterstützt Prometheus von Haus aus; dazu einfach eine Prometheus-Datenquelle hinzufügen:

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

Anschließend die standardmäßige [etcd-Dashboardvorlage][template] importieren und anpassen. Heißt die Prometheus-Datenquelle beispielsweise `my-etcd`, müssen auch die Werte der `datasource`-Felder im JSON `my-etcd` lauten.

Beispieldashboard:

![](/docs/etcd/op-guide/etcd-sample-grafana.png)

## Verteiltes Tracing {#distributed-tracing}

In v3.5 wurde etcd um Unterstützung für verteiltes Tracing mit [OpenTelemetry](https://github.com/open-telemetry) erweitert.

> [!NOTE]
> In etcd 3.7 die folgenden Tracing-Optionen ohne das frühere Präfix experimental verwenden.

Um verteiltes Tracing zu aktivieren, dem etcd-Server `--enable-distributed-tracing=true` übergeben. Mit der Option `--distributed-tracing-sampling-rate=<number>` wird zusätzlich festgelegt, wie viele Stichproben pro Million Spans erfasst werden; die Standardrate ist `0`.

Das verteilte Tracing lässt sich konfigurieren, indem der etcd-Server mit folgenden optionalen Optionen gestartet wird:

- `--distributed-tracing-address` - (Optional) - "localhost:4317" - Adresse des Tracing-Collectors.

- `--distributed-tracing-service-name` - (Optional) - "etcd" - Dienstname für verteiltes Tracing; muss für alle etcd-Instanzen gleich sein.

- `--distributed-tracing-instance-id` - (Optional) - Instanz-ID; ihre Angabe ist optional, wird aber dringend empfohlen. Sie muss für jede etcd-Instanz eindeutig sein.

Vor der Aktivierung des verteilten Tracings sicherstellen, dass ein OpenTelemetry-Endpunkt verfügbar ist. Weicht seine Adresse vom Standard ab, sie mit `--distributed-tracing-address` überschreiben. Da OpenTelemetry auf verschiedene Arten betrieben werden kann, enthält die [Collector-Dokumentation](https://opentelemetry.io/docs/collector/getting-started/) weitere Informationen.

> [!NOTE]
> Wie jedes Signal zur Beobachtung des Systems verursacht auch diese Funktion zusätzlichen Ressourcenbedarf. Nach unseren ersten Messungen kann die zusätzliche CPU-Last zwischen 2% - 4% liegen.

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /docs/etcd/op-guide/grafana.json
