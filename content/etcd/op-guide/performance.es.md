---
title: Rendimiento
weight: 4550
description: "Comprender el rendimiento: latencia y tasa de procesamiento"
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/performance.md"
---

## Comprender el rendimiento {#understanding-performance}

etcd proporciona un rendimiento alto estable y sostenido. Dos factores definen el rendimiento: la latencia y la tasa de procesamiento. La latencia es el tiempo que toma completar una operación. La tasa de procesamiento es el total de operaciones completadas dentro de cierto periodo de tiempo. Normalmente la latencia media aumenta a medida que aumenta la tasa de procesamiento global cuando etcd acepta solicitudes de clientes concurrentes. En entornos de cloud habituales, como una `n-4` estándar en Google Compute Engine (GCE) o un tipo de máquina comparable en AWS, un clúster de etcd de tres miembros completa una solicitud en menos de un milisegundo bajo carga ligera, y puede completar más de 30,000 solicitudes por segundo bajo carga pesada.

etcd usa el algoritmo de consenso Raft para replicar las solicitudes entre los miembros y alcanzar un acuerdo. El rendimiento del consenso, en especial la latencia de confirmación, está limitado por dos restricciones físicas: la latencia de E/S de red y la latencia de E/S de disco. El tiempo mínimo para terminar una solicitud de etcd es el tiempo de ida y vuelta de red (RTT) entre los miembros, más el tiempo que `fdatasync` necesita para confirmar los datos en el almacenamiento permanente. El RTT dentro de un centro de datos puede llegar a varios cientos de microsegundos. Un RTT típico dentro de Estados Unidos ronda los 50ms, y puede ser tan lento como 400ms entre continentes. La latencia típica de fdatasync para un disco mecánico es de unos 10ms. En los SSD, la latencia suele ser inferior a 1ms. Para aumentar la tasa de procesamiento, etcd agrupa múltiples solicitudes y las envía juntas a Raft. Esta política de agrupamiento permite a etcd alcanzar una tasa de procesamiento elevada incluso bajo carga pesada.

Hay otros subsistemas que afectan al rendimiento global de etcd. Cada solicitud serializada de etcd debe pasar por el motor de almacenamiento MVCC de etcd basado en boltdb, lo que suele tomar decenas de microsegundos. Periódicamente, etcd toma instantáneas incrementales de sus solicitudes aplicadas recientemente, combinándolas de nuevo con la instantánea previa en disco. Este proceso puede provocar un pico de latencia. Aunque normalmente esto no es un problema en los SSD, puede duplicar la latencia observada en discos HDD. Asimismo, las compactaciones en curso pueden afectar al rendimiento de etcd. Afortunadamente, el impacto suele ser insignificante ya que la compactación se escalona para no competir por recursos con las solicitudes normales. El sistema RPC, gRPC, otorga a etcd una API bien definida y extensible, pero también introduce una latencia adicional, especialmente para lecturas locales.

## Benchmarks {#benchmarks}

La evaluación del rendimiento de etcd puede hacerse con la herramienta CLI [benchmark](https://github.com/etcd-io/etcd/tree/main/tools/benchmark) incluida con etcd.

Para algunas cifras de rendimiento de referencia, consideramos un clúster de etcd de tres miembros con la siguiente configuración de hardware:

- Google Cloud Compute Engine
- 3 máquinas de 8 vCPUs + 16GB de memoria + 50GB SSD
- 1 máquina (cliente) de 16 vCPUs + 30GB de memoria + 50GB SSD
- Ubuntu 17.04
- etcd 3.2.0, go 1.8.3

Con esta configuración, etcd puede escribir aproximadamente:

| Número de claves | Tamaño de clave en bytes | Tamaño de valor en bytes | Número de conexiones | Número de clientes | Servidor etcd de destino | QPS medio de escritura | Latencia media por solicitud | RSS medio del servidor |
|---------------:|------------------:|--------------------:|----------------------:|------------------:|--------------------|------------------:|----------------------------:|-------------------:|
| 10,000 | 8 | 256 | 1 | 1 | solo el líder | 583 | 1.6ms | 48 MB |
| 100,000 | 8 | 256 | 100 | 1000 | solo el líder | 44,341 | 22ms |  124MB |
| 100,000 | 8 | 256 | 100 | 1000 | todos los miembros |  50,104 | 20ms |  126MB |

Comandos de ejemplo:

```sh
# write to leader
benchmark --endpoints=${HOST_1} --target-leader --conns=1 --clients=1 \
    put --key-size=8 --sequential-keys --total=10000 --val-size=256
benchmark --endpoints=${HOST_1} --target-leader  --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256

# write to all members
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256
```

Las solicitudes de lectura linealizables pasan por un cuórum de los miembros del clúster para lograr el consenso y obtener los datos más recientes. Las solicitudes de lectura serializables son más baratas que las linealizables porque las atiende cualquier miembro individual de etcd, en lugar de un cuórum de miembros, a cambio de posiblemente servir datos obsoletos. etcd puede leer:

| Número de solicitudes | Tamaño de clave en bytes | Tamaño de valor en bytes | Número de conexiones | Número de clientes | Consistencia | QPS medio de lectura | Latencia media por solicitud |
|-------------------:|------------------:|--------------------:|----------------------:|------------------:|-------------|-----------------:|----------------------------:|
| 10,000 | 8 | 256 | 1 | 1 | Linealizable | 1,353 | 0.7ms |
| 10,000 | 8 | 256 | 1 | 1 | Serializable | 2,909 | 0.3ms |
| 100,000 | 8 | 256 | 100 | 1000 | Linealizable | 141,578 | 5.5ms |
| 100,000 | 8 | 256 | 100 | 1000 | Serializable | 185,758 | 2.2ms |

Comandos de ejemplo:

```sh
# Single connection read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=l --total=10000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=s --total=10000

# Many concurrent read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=l --total=100000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=s --total=100000
```

Recomendamos ejecutar la prueba de benchmark al configurar por primera vez un clúster de etcd en un entorno nuevo, para asegurarte de que el clúster alcanza un rendimiento adecuado; la latencia y la tasa de procesamiento del clúster pueden ser sensibles a pequeñas diferencias del entorno.
