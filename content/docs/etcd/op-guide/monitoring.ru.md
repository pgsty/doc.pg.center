---
title: Мониторинг etcd
weight: 4500
description: Мониторинг etcd для проверки состояния системы и отладки кластера
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/monitoring.md"
aliases: [/etcd/op-guide/monitoring/]
---

Каждый сервер etcd предоставляет локальные сведения мониторинга через конечные
точки HTTP на клиентском порту. Эти данные полезны для проверки состояния системы
и отладки кластера.

## Конечная точка отладки {#debug-endpoint}

Если задан `--log-level=debug`, сервер etcd экспортирует отладочные сведения по
пути `/debug` на клиентском порту. Используйте `--log-level=debug` осторожно:
он снижает производительность и включает подробное ведение журнала.

`/debug/pprof` — стандартная конечная точка профилирования среды выполнения Go.
Она позволяет профилировать использование CPU, кучи, мьютексов и goroutine.
В примере `go tool pprof` получает 10 функций, на которые etcd тратит больше всего времени:

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

Конечная точка `/debug/requests` показывает трассировки gRPC и статистику
производительности в веб-браузере. Например, так выглядит запрос `Range` для ключа `abc`:

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## Конечная точка метрик {#metrics-endpoint}

Каждый сервер etcd экспортирует метрики по пути `/metrics` на клиентском порту
и, необязательно, по адресам из `--listen-metrics-urls`.

Метрики можно получить с помощью `curl`:

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

## Проверка состояния {#health-check}

Начиная с v3.3.0, все адреса из `--listen-metrics-urls` отвечают не только через
`/metrics`, но и через `/health`. Это полезно, когда стандартная конечная точка
защищена взаимной клиентской аутентификацией TLS, но балансировщику нагрузки или
службе мониторинга всё ещё нужен доступ к проверке состояния.

Начиная с v3.4 добавлены две конечные точки: `/livez` и `/readyz`.

* `/livez` показывает, работает ли процесс или его необходимо перезапустить;
* `/readyz` показывает, готов ли процесс обслуживать трафик.

Архитектура конечных точек описана в [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz).

Каждая конечная точка включает несколько отдельных проверок. Параметр `verbose`
выводит подробности проверок и их состояние, например:

```bash
curl -k http://localhost:2379/readyz?verbose
```

Ответ будет выглядеть примерно так:

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

API HTTP также позволяет исключать отдельные проверки, например:

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

Самый простой способ получать и сохранять метрики etcd — запустить службу мониторинга [Prometheus][prometheus].

Сначала установите Prometheus:

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

Настройте сборщик Prometheus на конечные точки кластера etcd:

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

Запустите обработчик Prometheus:

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

Теперь Prometheus будет собирать метрики etcd каждые 10 секунд.


### Оповещения {#alerting}

Для кластеров etcd v3 доступен набор [стандартных оповещений](https://github.com/etcd-io/etcd/tree/main/contrib/mixin) Prometheus.

> [!NOTE]
> Метки `job` может потребоваться адаптировать к конкретной задаче. Правила рассчитаны на один кластер, поэтому рекомендуется выбирать уникальные для кластера метки.

### Grafana {#grafana}

[Grafana][grafana] имеет встроенную поддержку Prometheus; добавьте источник данных Prometheus:

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

Затем импортируйте стандартный [шаблон панели etcd][template] и настройте его.
Например, если источник данных Prometheus называется `my-etcd`, поля `datasource`
в JSON также должны иметь значение `my-etcd`.

Пример панели:

![](/docs/etcd/op-guide/etcd-sample-grafana.png)

## Распределённая трассировка {#distributed-tracing}

В v3.5 etcd добавлена распределённая трассировка с помощью [OpenTelemetry](https://github.com/open-telemetry).

> [!NOTE]
> В etcd 3.7 используйте приведённые ниже флаги трассировки без прежнего экспериментального префикса.

Чтобы включить распределённую трассировку, передайте серверу etcd
`--enable-distributed-tracing=true` и флаг
`--distributed-tracing-sampling-rate=<number>`, задающий число
выборок на миллион спанов. Частота выборки по умолчанию — `0`.

Настройте распределённую трассировку, запустив сервер etcd со следующими необязательными флагами:

- `--distributed-tracing-address` - (необязательно) - "localhost:4317" - адрес сборщика трассировок.

- `--distributed-tracing-service-name` - (необязательно) - "etcd" - имя службы распределённой трассировки, которое должно быть одинаковым для всех экземпляров etcd.

- `--distributed-tracing-instance-id` - (необязательно) - идентификатор экземпляра; хотя параметр необязателен, его настоятельно рекомендуется задать, и он должен быть уникальным для каждого экземпляра etcd.

Перед включением распределённой трассировки убедитесь, что конечная точка
OpenTelemetry доступна. Если её адрес отличается от стандартного, переопределите
его флагом `--distributed-tracing-address`. Варианты запуска
OpenTelemetry описаны в [документации сборщика](https://opentelemetry.io/docs/collector/getting-started/).

> [!NOTE]
> Как и любой сигнал наблюдаемости, эта возможность расходует ресурсы. По первым измерениям дополнительные затраты CPU могут составлять от 2% до 4%.

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /docs/etcd/op-guide/grafana.json
