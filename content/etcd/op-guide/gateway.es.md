---
title: Puerta de enlace de etcd
weight: 4300
description: La puerta de enlace de etcd, cuándo usarla y cómo configurarla
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/gateway.md"
---

## Qué es la puerta de enlace de etcd {#what-is-etcd-gateway}

La puerta de enlace de etcd es un proxy TCP simple que reenvía los datos de red al clúster de etcd. La puerta de enlace no tiene estado y es transparente; no inspecciona las solicitudes de los clientes ni interfiere con las respuestas del clúster. No termina conexiones TLS, no realiza negociaciones TLS en nombre de sus clientes ni verifica si la conexión es segura.

La puerta de enlace admite varios puntos de acceso del servidor de etcd y funciona con una política simple de turno rotativo. Solo enruta hacia puntos de acceso disponibles y oculta los fallos a sus clientes. Otras políticas de reintento, como el turno rotativo ponderado, podrían admitirse en el futuro.

## Cuándo usar la puerta de enlace de etcd {#when-to-use-etcd-gateway}

Toda aplicación que acceda a etcd debe conocer primero la dirección de un punto de acceso de cliente del clúster de etcd. Si varias aplicaciones en el mismo servidor acceden al mismo clúster de etcd, cada aplicación necesita igualmente conocer los puntos de acceso de cliente publicados del clúster de etcd. Si el clúster de etcd se reconfigura para tener puntos de acceso diferentes, cada aplicación puede necesitar también actualizar su lista de puntos de acceso. Esta reconfiguración a gran escala es tanto tediosa como propensa a errores.

La puerta de enlace de etcd resuelve este problema actuando como un punto de acceso local estable. Una configuración típica de la puerta de enlace de etcd tiene cada máquina ejecutando una puerta de enlace que escucha en una dirección local y cada aplicación de etcd conectándose a su puerta de enlace local. El resultado es que solo la puerta de enlace necesita actualizar sus puntos de acceso, en lugar de actualizar cada aplicación una por una.

En resumen, para propagar automáticamente los cambios de los puntos de acceso del clúster, la puerta de enlace de etcd se ejecuta en cada máquina que atiende a varias aplicaciones que acceden al mismo clúster de etcd.

## Cuándo no usar la puerta de enlace de etcd {#when-not-to-use-etcd-gateway}

- Mejorar el rendimiento

La puerta de enlace no está diseñada para mejorar el rendimiento del clúster de etcd. No proporciona caché, agrupación de watches ni procesamiento por lotes. El equipo de etcd está desarrollando un proxy con caché diseñado para mejorar la escalabilidad del clúster.

- Ejecutarse en un sistema de gestión de clústeres

Los sistemas avanzados de gestión de clústeres como Kubernetes admiten de forma nativa el descubrimiento de servicios. Las aplicaciones pueden acceder a un clúster de etcd mediante un nombre DNS o una dirección IP virtual gestionada por el sistema. Por ejemplo, kube-proxy es equivalente a la puerta de enlace de etcd.

## Iniciar la puerta de enlace de etcd {#start-etcd-gateway}

Considera un clúster de etcd con los siguientes puntos de acceso estáticos:

|Nombre|Dirección|Nombre de host|Puerto|
|------|---------|------------------|----|
|infra0|10.0.1.10|infra0.example.com|2379|
|infra1|10.0.1.11|infra1.example.com|2379|
|infra2|10.0.1.12|infra2.example.com|2379|

Inicia la puerta de enlace de etcd para usar estos puntos de acceso estáticos con el comando:

```bash
$ etcd gateway start --endpoints=infra0.example.com:2379,infra1.example.com:2379,infra2.example.com:2379
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

Alternativamente, si usas DNS para el descubrimiento de servicios, considera las entradas DNS SRV:

```bash
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```bash
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

Inicia la puerta de enlace de etcd para obtener los puntos de acceso de las entradas DNS SRV con el comando:

```bash
$ etcd gateway start --discovery-srv=example.com
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

## Opciones de configuración {#configuration-flags}

### Clúster de etcd {#etcd-cluster}

#### --endpoints {#endpoints}

 * Lista separada por comas de destinos de servidor etcd para reenviar las conexiones de clientes.
 * Valor por defecto: `127.0.0.1:2379`
 * El puerto debe incluirse.
 * Ejemplo no válido: `https://127.0.0.1:2379` (la puerta de enlace no termina TLS). Ten en cuenta que la puerta de enlace no verifica el esquema HTTP ni inspecciona las solicitudes, solo reenvía las solicitudes a los puntos de acceso indicados.

#### --discovery-srv {#discovery-srv}

 * Dominio DNS usado para arrancar los puntos de acceso del clúster mediante registros SRV.
 * Por defecto: (sin establecer)

### Red {#network}

#### --listen-addr {#listen-addr}

 * Interfaz y puerto de escucha para aceptar solicitudes de clientes.
 * Valor por defecto: `127.0.0.1:23790`

#### --retry-delay {#retry-delay}

 * Duración del retraso antes de reintentar la conexión con puntos de acceso fallidos.
 * Valor por defecto: 1m0s
 * Ejemplo no válido: "123" (se espera una unidad de tiempo en el formato)

### Seguridad {#security}

#### --insecure-discovery {#insecure-discovery}

 * Aceptar registros SRV que no sean seguros o que sean susceptibles a ataques de intermediario (man-in-the-middle).
 * Valor por defecto: `false`

#### --trusted-ca-file {#trusted-ca-file}

 * Ruta al archivo de CA TLS del cliente del clúster de etcd, usado para verificar los puntos de acceso devueltos por el descubrimiento SRV. Ten en cuenta que se usa ÚNICAMENTE para autenticar los puntos de acceso descubiertos, no para crear conexiones de transferencia de datos. La puerta de enlace nunca termina conexiones TLS ni crea conexiones TLS en nombre de sus clientes.
 * Por defecto: (sin establecer)
