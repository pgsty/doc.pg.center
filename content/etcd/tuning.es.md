---
title: Ajuste
weight: 1450
description: Cuándo actualizar los ajustes del intervalo de latido y del tiempo de espera de elección
icon: fa-solid fa-sliders
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tuning.md"
---

Los ajustes predeterminados de etcd deberían funcionar bien en instalaciones sobre una red local donde la latencia de red media es baja. Sin embargo, al usar etcd a través de varios centros de datos o sobre redes con una latencia alta, puede que los ajustes del intervalo de latido y del tiempo de espera de elección necesiten un ajuste fino.

La red no es la única fuente de latencia. Cada petición y respuesta puede verse afectada por discos lentos tanto en el líder como en la réplica. Cada uno de estos tiempos de espera representa el tiempo total desde la petición hasta la respuesta correcta de la otra máquina.

## Parámetros de tiempo {#time-parameters}

El protocolo de consenso distribuido subyacente se basa en dos parámetros de tiempo distintos para garantizar que los nodos puedan transferir el liderazgo si uno se bloquea o se desconecta. El primer parámetro se llama el *intervalo de latido*. Es la frecuencia con la que el líder notifica a las réplicas que sigue siendo el líder.
Como buena práctica, este parámetro debería fijarse en torno al tiempo de ida y vuelta entre los miembros. Por defecto, etcd utiliza un intervalo de latido de `100ms`.

El segundo parámetro es el *tiempo de espera de elección*. Este tiempo de espera es cuánto puede estar un nodo réplica sin recibir un latido antes de intentar convertirse él mismo en líder. Por defecto, etcd utiliza un tiempo de espera de elección de `1000ms`.

Ajustar estos valores supone un compromiso. Se recomienda que el valor del intervalo de latido ronde el máximo del tiempo medio de ida y vuelta (RTT) entre los miembros, normalmente alrededor de 0.5-1.5x el tiempo de ida y vuelta. Si el intervalo de latido es demasiado bajo, etcd enviará mensajes innecesarios que aumentan el uso de recursos de CPU y de red. Por otro lado, un intervalo de latido demasiado alto conduce a un tiempo de espera de elección alto. Un tiempo de espera de elección más alto tarda más en detectar un fallo del líder. La forma más sencilla de medir el tiempo de ida y vuelta (RTT) es usar la [utilidad PING][ping].

El tiempo de espera de elección debería fijarse en función del intervalo de latido y del tiempo medio de ida y vuelta entre los miembros. Los tiempos de espera de elección deben ser al menos 10 veces el tiempo de ida y vuelta para poder absorber la varianza de la red. Por ejemplo, si el tiempo de ida y vuelta entre los miembros es de 10ms, el tiempo de espera de elección debería ser de al menos 100ms.

El límite superior del tiempo de espera de elección es 50000ms (50s), que solo debería usarse al desplegar un clúster etcd distribuido a escala global. Un tiempo de ida y vuelta razonable para los Estados Unidos continentales es de 130ms, y el tiempo entre Estados Unidos y Japón ronda los 350-400ms. Si la red tiene un rendimiento desigual o retrasos/pérdidas de paquetes habituales, es posible que hagan falta un par de reintentos para enviar correctamente un paquete. Así, 5s es un límite superior seguro para el tiempo de ida y vuelta global. Dado que el tiempo de espera de elección debería ser un orden de magnitud mayor que el tiempo de difusión, en el caso de ~5s para un clúster distribuido globalmente, 50 segundos se convierte en un máximo razonable.

El intervalo de latido y el valor del tiempo de espera de elección deberían ser los mismos para todos los miembros de un clúster. Establecer valores diferentes para los miembros de etcd puede alterar la estabilidad del clúster.

Los valores predeterminados pueden sobrescribirse en la línea de comandos:

```sh
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

Los valores se especifican en milisegundos.

## Instantáneas {#snapshots}

etcd añade todos los cambios de claves a un archivo de registro. Este registro crece indefinidamente y constituye un historial lineal completo de cada cambio realizado en las claves. Un historial completo funciona bien en clústeres con poco uso, pero los clústeres con un uso intensivo acarrearían un registro de gran tamaño.

Para evitar tener un registro enorme, etcd realiza instantáneas periódicas. Estas instantáneas ofrecen a etcd una forma de compactar el registro guardando el estado actual del sistema y eliminando los registros antiguos.

### Ajuste de las instantáneas {#snapshot-tuning}

Las instantáneas de Raft se crean después de un número configurado de entradas aplicadas; etcd 3.7 ya no utiliza el backend V2. Por defecto, se harán instantáneas cada 10,000 cambios. Si el uso de memoria y de disco de etcd es demasiado alto, prueba a bajar el umbral de instantánea estableciendo lo siguiente en la línea de comandos:

```sh
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## Disco {#disk}

Un clúster etcd es muy sensible a las latencias de disco. Dado que etcd debe persistir las propuestas en su registro, la actividad de disco de otros procesos puede provocar latencias de `fsync` largas. La consecuencia es que etcd puede perder latidos, lo que causa tiempos de espera en las peticiones y una pérdida temporal del líder. Un servidor etcd a veces puede ejecutarse de forma estable junto a estos procesos cuando se le da una prioridad de disco alta.

En Linux, la prioridad de disco de etcd puede configurarse con `ionice`:

```sh
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

## Red {#network}

Si el líder de etcd atiende un gran número de peticiones de clientes concurrentes, es posible que retrase el procesamiento de las peticiones de par de las réplicas debido a la congestión de la red. Esto se manifiesta como mensajes de error del búfer de envío en los nodos réplica:

```
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
```

Estos errores pueden resolverse dando prioridad al tráfico de pares de etcd frente a su tráfico de clientes. En Linux, el tráfico de pares puede priorizarse utilizando el mecanismo de control de tráfico:

```
tc qdisc add dev eth0 root handle 1: prio bands 3
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1
```

[ping]: https://en.wikipedia.org/wiki/Ping_(networking_utility)


Para cancelar `tc`, ejecuta:

```
tc qdisc del dev eth0 root
```

## CPU {#cpu}

Como etcd es muy sensible a la latencia, el rendimiento puede optimizarse aún más en sistemas Linux configurando el gobernador de CPU en el modo performance o conservative.

En Linux, el gobernador de CPU puede configurarse en el modo performance:
```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
