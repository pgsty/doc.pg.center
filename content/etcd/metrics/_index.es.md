---
title: Métricas
weight: 1350
description: Métricas para la supervisión y la depuración en tiempo real
icon: fa-solid fa-chart-line
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/metrics/_index.md"
---

etcd usa [Prometheus][prometheus] para el reporte de métricas. Las métricas pueden usarse para la supervisión y la depuración en tiempo real. etcd no persiste sus métricas; si un miembro se reinicia, las métricas se restablecerán.

La forma más simple de ver las métricas disponibles es hacer cURL al endpoint de métricas `/metrics`. El formato se describe [en la documentación de Prometheus](http://prometheus.io/docs/instrumenting/exposition_formats/).

Sigue el [documento de introducción a Prometheus][prometheus-getting-started] para levantar un servidor de Prometheus que recoja las métricas de etcd.

La nomenclatura de las métricas sigue las [buenas prácticas sugeridas de Prometheus][prometheus-naming]. Un nombre de métrica tiene como espacio de nombres el prefijo `etcd` o `etcd_debugging` y un prefijo de subsistema (por ejemplo `wal` y `etcdserver`).

## Métricas del espacio de nombres etcd {#etcd-namespace-metrics}

Las métricas bajo el prefijo `etcd` sirven para la supervisión y las alertas. Son métricas de alto nivel estables. Si hay cualquier cambio en estas métricas, se incluirá en las notas de la versión.

Las métricas relacionadas con etcd2 están documentadas en la [guía de métricas v2][v2-http-metrics].

### Servidor {#server}

Estas métricas describen el estado del servidor de etcd. Para detectar cortes o problemas que requieran diagnóstico, las métricas del servidor de todo clúster de etcd en producción deberían supervisarse de cerca.

Todas estas métricas llevan el prefijo `etcd_server_`

| Nombre                      | Descripción                                              | Tipo    |
|---------------------------|----------------------------------------------------------|---------|
| has_leader                | Existe o no un líder. 1 indica que existe; 0, que no.      | Gauge   |
| leader_changes_seen_total | El número de cambios de líder observados.                | Counter |
| proposals_committed_total | El número total de propuestas de consenso confirmadas.   | Gauge   |
| proposals_applied_total   | El número total de propuestas de consenso aplicadas.     | Gauge   |
| proposals_pending         | El número actual de propuestas pendientes.               | Gauge   |
| proposals_failed_total    | El número total de propuestas fallidas observadas.       | Counter |

`has_leader` indica si el miembro tiene un líder. Si un miembro no tiene líder, está
totalmente no disponible. Si ninguno de los miembros del clúster tiene líder, todo el clúster
está totalmente no disponible.

`leader_changes_seen_total` cuenta el número de cambios de líder que el miembro ha observado desde su inicio. Los cambios de liderazgo rápidos afectan significativamente al rendimiento de etcd. También señalan que el líder es inestable, quizá por problemas de conectividad de red o por una carga excesiva sobre el clúster de etcd.

`proposals_committed_total` registra el número total de propuestas de consenso confirmadas. Este indicador (gauge) debería aumentar con el tiempo si el clúster está sano. Varios miembros sanos de un clúster de etcd pueden tener a la vez distintos totales de propuestas confirmadas. Esta discrepancia puede deberse a la recuperación desde los pares tras el arranque, a quedar retrasado respecto del líder, o a ser el líder y por ello tener el mayor número de confirmaciones. Es importante supervisar esta métrica en todos los miembros del clúster; un retraso consistentemente grande entre un solo miembro y su líder indica que ese miembro es lento o no está sano.

`proposals_applied_total` registra el número total de propuestas de consenso aplicadas. El servidor de etcd aplica cada propuesta confirmada de forma asíncrona. La diferencia entre `proposals_committed_total` y `proposals_applied_total` normalmente debería ser pequeña (dentro de unos pocos miles incluso bajo carga alta). Si la diferencia entre ellas sigue aumentando, indica que el servidor de etcd está sobrecargado. Esto puede ocurrir al aplicar consultas costosas como consultas de rango pesadas u operaciones txn grandes.

`proposals_pending` indica cuántas propuestas están en cola para confirmarse. El aumento de propuestas pendientes sugiere que hay una carga alta de clientes o que el miembro no puede confirmar propuestas.

`proposals_failed_total` normalmente está relacionado con dos problemas: fallos temporales relacionados con una elección de líder o un tiempo de inactividad más largo causado por la pérdida de cuórum en el clúster.

### Disco {#disk}

Estas métricas describen el estado de las operaciones de disco.

Todas estas métricas llevan el prefijo `etcd_disk_`.

| Nombre                               | Descripción                                           | Tipo      |
|------------------------------------|-------------------------------------------------------|-----------|
| wal_fsync_duration_seconds         | Las distribuciones de latencia de fsync llamadas por wal.      | Histogram |
| backend_commit_duration_seconds    | Las distribuciones de latencia de commit llamadas por el backend.| Histogram |

Se llama a un `wal_fsync` cuando etcd persiste sus entradas de registro en el disco antes de aplicarlas.

Se llama a un `backend_commit` cuando etcd confirma en el disco una instantánea incremental de sus cambios más recientes.

Latencias altas en las operaciones de disco (`wal_fsync_duration_seconds` o `backend_commit_duration_seconds`) a menudo indican problemas de disco. Pueden causar una latencia de solicitudes alta o hacer el clúster inestable.

### Red {#network}

Estas métricas describen el estado de la red.

Todas estas métricas llevan el prefijo `etcd_network_`

| Nombre                            | Descripción                                                        | Tipo          |
|---------------------------------|--------------------------------------------------------------------|---------------|
| peer_sent_bytes_total           | El número total de bytes enviados al par con ID `To`.           | Counter(To)   |
| peer_received_bytes_total       | El número total de bytes recibidos del par con ID `From`.   | Counter(From) |
| peer_sent_failures_total        | El número total de fallos de envío al par con ID `To`.      | Counter(To)   |
| peer_received_failures_total    | El número total de fallos de recepción del par con ID `From`. | Counter(From) |
| peer_round_trip_time_seconds    | Histograma del tiempo de ida y vuelta entre pares.                           | Histogram(To) |
| client_grpc_sent_bytes_total    | El número total de bytes enviados a clientes gRPC.                    | Counter       |
| client_grpc_received_bytes_total| El número total de bytes recibidos de clientes gRPC.                | Counter       |

`peer_sent_bytes_total` cuenta el número total de bytes enviados a un par específico. Normalmente el miembro líder envía más datos que los demás miembros, ya que es responsable de transmitir los datos replicados.

`peer_received_bytes_total` cuenta el número total de bytes recibidos de un par específico. Normalmente los miembros réplica reciben datos solo del miembro líder.

### Solicitudes gRPC {#grpc-requests}

Estas métricas se exponen mediante [go-grpc-prometheus][go-grpc-prometheus].

## Métricas del espacio de nombres etcd_debugging {#etcd_debugging-namespace-metrics}

Las métricas bajo el prefijo `etcd_debugging` sirven para la depuración. Dependen mucho de la implementación y son volátiles. Pueden cambiar o eliminarse sin previo aviso en nuevas versiones de etcd. Algunas de estas métricas podrían pasarse al prefijo `etcd` cuando se vuelvan más estables.

### Instantánea {#snapshot}

| Nombre                                       | Descripción                                                | Tipo      |
|--------------------------------------------|------------------------------------------------------------|-----------|
| snapshot_save_total_duration_seconds       | Las distribuciones de latencia total de las llamadas a save realizadas por snapshot | Histogram |

Una duración de instantánea anormalmente alta (`snapshot_save_total_duration_seconds`) indica problemas de disco y podría hacer que el clúster se vuelva inestable.

## Métricas proporcionadas por Prometheus {#prometheus-supplied-metrics}

La biblioteca cliente de Prometheus proporciona varias métricas bajo los espacios de nombres `go` y `process`. Hay algunas especialmente interesantes.

| Nombre                              | Descripción                                | Tipo         |
|-----------------------------------|--------------------------------------------|--------------|
| process_open_fds                  | Número de descriptores de archivo abiertos.           | Gauge        |
| process_max_fds                   | Número máximo de descriptores de archivo abiertos.   | Gauge        |

> [!NOTE]
> Las métricas de proceso, como `process_open_fds` y `process_max_fds`, no están soportadas por ahora en sistemas Darwin (macOS).

Un uso intensivo de los descriptores de archivo (`process_open_fds`) (es decir, cerca del límite de descriptores de archivo del proceso, `process_max_fds`) indica un posible problema de agotamiento de descriptores de archivo. Si los descriptores de archivo se agotan, etcd puede generar un panic porque no puede crear archivos WAL nuevos.

## Lista generada de métricas {#generated-list-of-metrics}

[go-grpc-prometheus]: https://github.com/grpc-ecosystem/go-grpc-prometheus
[prometheus]: https://prometheus.io/
[prometheus-getting-started]: https://prometheus.io/docs/introduction/getting_started/
[prometheus-naming]: https://prometheus.io/docs/practices/naming/
[v2-http-metrics]: https://etcd.io/docs/v2.3/metrics/#http-requests
