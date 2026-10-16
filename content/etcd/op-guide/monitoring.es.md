---
title: Monitoreo de etcd
weight: 4500
description: Monitorear etcd para la salud del sistema y la depuración del clúster
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/monitoring.md"
---

Cada servidor de etcd proporciona información de monitoreo local en su puerto de cliente a través de puntos de acceso http. Los datos de monitoreo son útiles tanto para la comprobación de la salud del sistema como para la depuración del clúster.

## Punto de acceso de depuración {#debug-endpoint}

Si se establece `--log-level=debug`, el servidor de etcd exporta información de depuración en su puerto de cliente bajo la ruta `/debug`. Ten cuidado al establecer `--log-level=debug`, ya que habrá un rendimiento degradado y un registro muy detallado.

El punto de acceso `/debug/pprof` es el punto de acceso estándar de perfilado del runtime de Go. Puede usarse para perfilar la utilización de CPU, heap, mutex y goroutines. Por ejemplo, aquí `go tool pprof` obtiene las 10 funciones principales donde etcd pasa su tiempo:

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

El punto de acceso `/debug/requests` ofrece trazas gRPC y estadísticas de rendimiento a través de un navegador web. Por ejemplo, aquí hay una solicitud `Range` para la clave `abc`:

```
When	Elapsed (s)
2017/08/18 17:34:51.999317 	0.000244 	/etcdserverpb.KV/Range
17:34:51.999382 	 .    65 	... RPC: from 127.0.0.1:47204 deadline:4.999377747s
17:34:51.999395 	 .    13 	... recv: key:"abc"
17:34:51.999499 	 .   104 	... OK
17:34:51.999535 	 .    36 	... sent: header:<cluster_id:14841639068965178418 member_id:10276657743932975437 revision:15 raft_term:17 > kvs:<key:"abc" create_revision:6 mod_revision:14 version:9 value:"asda" > count:1
```

## Punto de acceso de métricas {#metrics-endpoint}

Cada servidor de etcd exporta métricas bajo la ruta `/metrics` en su puerto de cliente y, opcionalmente, en las ubicaciones indicadas por `--listen-metrics-urls`.

Las métricas pueden obtenerse con `curl`:

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

## Comprobación de salud {#health-check}

Desde v3.3.0, además de responder al punto de acceso `/metrics`, cualquier ubicación especificada por `--listen-metrics-urls` responderá también al punto de acceso `/health`. Esto puede ser útil si el punto de acceso estándar está configurado con autenticación TLS mutua (de cliente), pero un balanceador de carga o un servicio de monitoreo aún necesita acceso a la comprobación de salud.

Desde v3.4 se añaden dos nuevos puntos de acceso: `/livez` y `/readyz`.

* el punto de acceso `/livez` refleja si el proceso está vivo o si necesita un reinicio.
* el punto de acceso `/readyz` refleja si el proceso está listo para atender tráfico.

Los detalles de diseño de los puntos de acceso están documentados en el [KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-etcd/4331-livez-readyz).

Cada punto de acceso incluye varias comprobaciones de salud individuales, y puedes usar el parámetro `verbose` para mostrar los detalles de las comprobaciones y su estado, por ejemplo

```bash
curl -k http://localhost:2379/readyz?verbose
```

y verías una respuesta similar a

```text
[+]data_corruption ok
[+]serializable_read ok
[+]linearizable_read ok
ok
```

La API http también admite excluir comprobaciones específicas, por ejemplo

```bash
curl -k http://localhost:2379/readyz?exclude=data_corruption
```

## Prometheus {#prometheus}

Ejecutar un servicio de monitoreo [Prometheus][prometheus] es la forma más sencilla de ingerir y registrar las métricas de etcd.

Primero, instala Prometheus:

```sh
PROMETHEUS_VERSION="2.0.0"
wget https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz -O /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz
tar -xvzf /tmp/prometheus-$PROMETHEUS_VERSION.linux-amd64.tar.gz --directory /tmp/ --strip-components=1
/tmp/prometheus -version
```

Configura el scraper de Prometheus para apuntar a los puntos de acceso del clúster de etcd:

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

Configura el manejador de Prometheus:

```sh
nohup /tmp/prometheus \
    -config.file /tmp/test-etcd.yaml \
    -web.listen-address ":9090" \
    -storage.local.path "test-etcd.data" >> /tmp/test-etcd.log  2>&1 &
```

Ahora Prometheus extraerá las métricas de etcd cada 10 segundos.


### Alertas {#alerting}

Existe un conjunto de [alertas por defecto](https://github.com/etcd-io/etcd/tree/main/contrib/mixin) para clústeres etcd v3 para Prometheus.

> [!NOTE]
> Ten en cuenta que las etiquetas `job` pueden necesitar ajustes para adaptarse a una necesidad particular. Las reglas se escribieron para aplicarse a un único clúster, por lo que se recomienda elegir etiquetas únicas por clúster.

### Grafana {#grafana}

[Grafana][grafana] tiene soporte integrado para Prometheus; solo añade una fuente de datos de Prometheus:

```
Name:   test-etcd
Type:   Prometheus
Url:    http://localhost:9090
Access: proxy
```

Luego importa la [plantilla de panel de etcd por defecto][template] y personalízala. Por ejemplo, si el nombre de la fuente de datos de Prometheus es `my-etcd`, los valores del campo `datasource` en JSON también deben ser `my-etcd`.

Panel de ejemplo:

![](/etcd/op-guide/etcd-sample-grafana.png)

## Trazado distribuido {#distributed-tracing}

En v3.5 etcd añadió soporte para trazado distribuido usando [OpenTelemetry](https://github.com/open-telemetry).

> [!NOTE]
> En etcd 3.7, usa las opciones de trazado siguientes sin el antiguo prefijo experimental.

Para habilitar el trazado distribuido, pasa `--enable-distributed-tracing=true` al servidor de etcd, junto con la opción `--distributed-tracing-sampling-rate=<number>` para elegir cuántas muestras recopilar por millón de spans; la tasa de muestreo por defecto es `0`.

Configura el trazado distribuido iniciando el servidor de etcd con los siguientes indicadores opcionales:

- `--distributed-tracing-address` - (Opcional) - "localhost:4317" - Dirección del recolector de trazado.

- `--distributed-tracing-service-name` - (Opcional) - "etcd" - Nombre del servicio de trazado distribuido, debe ser el mismo en todas las instancias de etcd.

- `--distributed-tracing-instance-id` - (Opcional) - ID de instancia; aunque es opcional, se recomienda encarecidamente establecerlo, y debe ser único por instancia de etcd.

Antes de habilitar el trazado distribuido, asegúrate de tener el punto de acceso de OpenTelemetry; si esa dirección difiere de la predeterminada, sobrescríbela con la opción `--distributed-tracing-address`. Debido a que OpenTelemetry tiene distintas formas de ejecutarse, consulta la [documentación del collector](https://opentelemetry.io/docs/collector/getting-started/) para saber más.

> [!NOTE]
> Existe una sobrecarga de recursos, como con cualquier señal de observabilidad; según nuestras mediciones iniciales, esa sobrecarga podría suponer un consumo adicional de CPU de 2% - 4%.

[grafana]: http://grafana.org/
[prometheus]: https://prometheus.io/
[template]: /etcd/op-guide/grafana.json
