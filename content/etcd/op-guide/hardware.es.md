---
title: Recomendaciones de hardware
weight: 4400
description: Directrices de hardware para administrar clústeres de etcd
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/hardware.md"
---

etcd suele funcionar bien con recursos limitados para fines de desarrollo o pruebas; es habitual desarrollar con etcd en un portátil o en una máquina cloud económica. Sin embargo, al ejecutar clústeres de etcd en producción, algunas directrices de hardware resultan útiles para una administración adecuada. Estas sugerencias no son reglas estrictas; sirven como un buen punto de partida para un despliegue de producción robusto. Como siempre, los despliegues deben probarse con cargas simuladas antes de ejecutarse en producción.

## CPUs {#cpus}

Pocos despliegues de etcd requieren una gran capacidad de CPU. Los clústeres típicos necesitan de dos a cuatro núcleos para funcionar con fluidez.
Los despliegues de etcd muy cargados, que atienden a miles de clientes o decenas de miles de solicitudes por segundo, tienden a estar limitados por la CPU, ya que etcd puede servir las solicitudes desde memoria. Estos despliegues de gran carga suelen necesitar de ocho a dieciséis núcleos dedicados.


## Memoria {#memory}

etcd tiene una huella de memoria relativamente pequeña, pero su rendimiento depende de disponer de memoria suficiente. Un servidor de etcd almacena agresivamente en caché los datos clave-valor y dedica la mayor parte del resto de su memoria al seguimiento de los watchers. Normalmente, 8GB son suficientes. Para despliegues de gran carga con miles de watchers y millones de claves, asigna entre 16GB y 64GB de memoria según corresponda.


## Discos {#disks}

Unos discos rápidos son el factor más crítico para el rendimiento y la estabilidad de un despliegue de etcd.

Un disco lento aumentará la latencia de las solicitudes de etcd y podría dañar la estabilidad del clúster. Dado que el protocolo de consenso de etcd depende del almacenamiento persistente de metadatos en un registro, una mayoría de los miembros del clúster de etcd debe escribir cada solicitud en el disco. Además, etcd también volcará de forma incremental puntos de control de su estado al disco para poder truncar ese registro. Si estas escrituras tardan demasiado, los latidos pueden agotar su tiempo de espera y desencadenar una elección, lo que mina la estabilidad del clúster. En general, para determinar si un disco es lo bastante rápido para etcd, se puede usar una herramienta de evaluación como [fio][fio]. Lee [aquí][fio-blog-post] un ejemplo.

etcd es muy sensible a la latencia de escritura en disco. Normalmente se requieren 50 IOPS secuenciales (por ejemplo, un disco de 7200 RPM). Para clústeres con mucha carga, se recomiendan 500 IOPS secuenciales (por ejemplo, un SSD local típico o un dispositivo de bloques virtualizado de alto rendimiento). Ten en cuenta que la mayoría de los proveedores de cloud publican IOPS concurrentes en lugar de IOPS secuenciales; las IOPS concurrentes publicadas pueden alcanzar 10x las IOPS secuenciales. Para medir las IOPS secuenciales reales, sugerimos usar una herramienta de evaluación de discos como [diskbench][diskbench] o [fio][fio].

etcd requiere solo un ancho de banda de disco modesto, pero un mayor ancho de banda de disco permite tiempos de recuperación más rápidos cuando un miembro fallido debe ponerse al día con el clúster. Normalmente, 10MB/s recuperarán 100MB de datos en 15 segundos. Para clústeres grandes, se sugiere 100MB/s o más para recuperar 1GB de datos en 15 segundos.

Cuando sea posible, respalda el almacenamiento de etcd con un SSD. Un SSD suele proporcionar latencias de escritura más bajas y con menos variación que un disco mecánico, lo que mejora la estabilidad y la fiabilidad de etcd. Si usas discos mecánicos, consigue los discos más rápidos posibles (15,000 RPM). Usar RAID 0 también es una forma eficaz de aumentar la velocidad del disco, tanto para discos mecánicos como para SSD. Con al menos tres miembros en el clúster, las variantes de RAID con espejo y/o paridad son innecesarias; la replicación consistente de etcd ya proporciona alta disponibilidad.


## Red {#network}

Los despliegues de etcd de varios miembros se benefician de una red rápida y fiable. Para que etcd sea a la vez consistente y tolerante a particiones, una red poco fiable con cortes por partición conducirá a una disponibilidad deficiente. Una latencia baja garantiza que los miembros de etcd puedan comunicarse rápido. Un ancho de banda alto puede reducir el tiempo para recuperar un miembro de etcd fallido. 1GbE es suficiente para los despliegues comunes de etcd. Para clústeres grandes de etcd, una red de 10GbE reducirá el tiempo medio de recuperación.

Despliega los miembros de etcd dentro de un único centro de datos cuando sea posible, para evitar sobrecostes de latencia y reducir la posibilidad de eventos de partición. Si se necesita un dominio de fallo en otro centro de datos, elige uno más cercano al existente. Lee también la documentación de [ajuste de rendimiento][tuning] para más información sobre despliegues entre centros de datos.


## Ejemplos de configuraciones de hardware {#example-hardware-configurations}

Aquí hay algunos ejemplos de configuraciones de hardware en entornos de AWS y GCE. Como se mencionó antes, y conviene insistir en ello de todos modos, los administradores deben probar un despliegue de etcd con una carga de trabajo simulada antes de ponerlo en producción.

Ten en cuenta que estas configuraciones asumen que estas máquinas están totalmente dedicadas a etcd. Ejecutar otras aplicaciones junto con etcd en estas máquinas puede causar contenciones de recursos y provocar inestabilidad en el clúster.

### Clúster pequeño {#small-cluster}

Un clúster pequeño atiende a menos de 100 clientes, menos de 200 solicitudes por segundo y almacena no más de 100MB de datos.

Ejemplo de carga de trabajo de aplicación: un clúster de Kubernetes de 50 nodos

| Proveedor | Tipo | vCPUs | Memoria (GB) | IOPS concurrentes máx. | Ancho de banda de disco (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.large | 2 | 8 | 3600 | 56.25 |
| GCE | n1-standard-2 + 50GB PD SSD | 2 | 7.5 | 1500 | 25 |


### Clúster mediano {#medium-cluster}

Un clúster mediano atiende a menos de 500 clientes, menos de 1,000 solicitudes por segundo y almacena no más de 500MB de datos.

Ejemplo de carga de trabajo de aplicación: un clúster de Kubernetes de 250 nodos

| Proveedor | Tipo | vCPUs | Memoria (GB) | IOPS concurrentes máx. | Ancho de banda de disco (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.xlarge | 4 | 16 | 6000 | 93.75 |
| GCE | n1-standard-4 + 150GB PD SSD | 4 | 15 | 4500 | 75 |


### Clúster grande {#large-cluster}

Un clúster grande atiende a menos de 1,500 clientes, menos de 10,000 solicitudes por segundo y almacena no más de 1GB de datos.

Ejemplo de carga de trabajo de aplicación: un clúster de Kubernetes de 1,000 nodos

| Proveedor | Tipo | vCPUs | Memoria (GB) | IOPS concurrentes máx. | Ancho de banda de disco (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.2xlarge | 8 | 32 | 8000 | 125 |
| GCE | n1-standard-8 + 250GB PD SSD | 8 | 30 | 7500 | 125 |


### Clúster xLarge {#xlarge-cluster}

Un clúster xLarge atiende a más de 1,500 clientes, más de 10,000 solicitudes por segundo y almacena más de 1GB de datos.

Ejemplo de carga de trabajo de aplicación: un clúster de Kubernetes de 3,000 nodos

| Proveedor | Tipo | vCPUs | Memoria (GB) | IOPS concurrentes máx. | Ancho de banda de disco (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.4xlarge | 16 | 64 | 16,000 | 250 |
| GCE | n1-standard-16 + 500GB PD SSD | 16 | 60 | 15,000 | 250 |


[diskbench]: https://github.com/ongardie/diskbenchmark
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[tuning]: /es/etcd/tuning/
