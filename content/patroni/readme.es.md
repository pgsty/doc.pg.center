---
title: "Introducción"
weight: 10
icon: fa-solid fa-circle-info
description: "Introducción a Patroni, inicio rápido y conceptos fundamentales de alta disponibilidad."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/README.html"
---

<a id="readme"></a>
Patroni es una plantilla para soluciones de PostgreSQL de alta disponibilidad (HA) usando Python. Patroni se originó como un fork de [Governor](https://github.com/compose/governor), el proyecto de Compose. Incluye numerosas funcionalidades nuevas.

Para información adicional de contexto, consulta:

- [PostgreSQL HA con Kubernetes y Patroni](https://www.youtube.com/watch?v=iruaCgeG7qs), charla de Josh Berkus en la KubeCon 2016 (vídeo)
- [Entrada del blog de Zalando Tech de febrero de 2016](https://engineering.zalando.com/posts/2016/02/zalandos-patroni-a-template-for-high-availability-postgresql.html)

--------

## Estado del desarrollo {#development-status}

Patroni está en desarrollo activo y acepta contribuciones. Consulta nuestra sección [Contribuir](/es/patroni/contributing_guidelines#contributing_guidelines) a continuación para más detalles.

Informamos sobre las nuevas versiones [aquí](/es/patroni/releases#releases).

--------

## Requisitos técnicos/Instalación {#technical-requirementsinstallation}

Ve [aquí](/es/patroni/installation#installation) para obtener orientación sobre cómo instalar y actualizar Patroni en diversas plataformas.

<a id="running_configuring"></a>

--------

## Planificación del número de nodos de PostgreSQL {#planning-the-number-of-postgresql-nodes}

Los nodos de Patroni/PostgreSQL están desacoplados de los nodos del DCS (excepto cuando el propio Patroni implementa RAFT) y, por lo tanto, no hay ningún requisito sobre el número mínimo de nodos. Ejecutar un clúster formado por un primario y un standby es perfectamente válido. Puedes añadir más nodos standby más adelante.

**Clústeres de 2 nodos** (primario + standby) son comunes y proporcionan conmutación por error automática con alta disponibilidad. Ten en cuenta que, durante la conmutación por error, temporalmente no tendrás redundancia hasta que el nodo fallido se reincorpore.

**Requisitos del DCS**: tu DCS (etcd, ZooKeeper, Consul) debe ejecutarse con **3 o 5 nodos** para un consenso y una tolerancia a fallos adecuados. Un único clúster de DCS puede almacenar información de cientos o miles de clústeres de Patroni usando diferentes combinaciones de namespace/scope.

--------

## Ejecución y configuración {#running-and-configuring}

La siguiente sección asume que el repositorio de Patroni ha sido clonado desde <https://github.com/patroni/patroni>. En concreto, necesitarás los archivos de configuración de ejemplo `postgres0.yml` y `postgres1.yml`. Si instalaste Patroni con pip, puedes obtener esos archivos del repositorio git y reemplazar `./patroni.py` que aparece más abajo por el comando `patroni`.

Los comandos que siguen usan la API v2 de etcd y requieren una versión de etcd que admita `--enable-v2`, como etcd 3.5. Para etcd 3.6 o más reciente, usa en cambio la configuración `etcd3` de Patroni, porque [etcd 3.6 eliminó el soporte de la API v2](https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/).

Para empezar, ejecuta lo siguiente desde distintas terminales: :

    > etcd --data-dir=data/etcd --enable-v2=true
    > ./patroni.py postgres0.yml
    > ./patroni.py postgres1.yml

Verás entonces cómo se inicia un clúster de alta disponibilidad. Prueba distintos ajustes en los archivos YAML para ver cómo cambia el comportamiento del clúster. Termina los procesos de algunos de los componentes para observar cómo se comporta el sistema.

Añade más archivos `postgres*.yml` para crear un clúster aún mayor.

Patroni proporciona una configuración de [HAProxy](https://www.haproxy.org/), que dará a tu aplicación un único endpoint para conectarse al líder del clúster. Para configurarla, ejecuta:

    > haproxy -f haproxy.cfg

    > psql --host 127.0.0.1 --port 5000 postgres

--------

## Configuración YAML {#yaml-configuration}

Ve [aquí](/es/patroni/config/yaml#yaml) para obtener información completa sobre los ajustes de etcd, consul y ZooKeeper. Y para ver un ejemplo, consulta [postgres0.yml](https://github.com/patroni/patroni/blob/master/postgres0.yml).

--------

## Configuración mediante variables de entorno {#environment-configuration}

Ve [aquí](/es/patroni/config/env#env) para obtener información completa sobre cómo configurar (sobrescribir) ajustes mediante variables de entorno.

--------

## Opciones de replicación {#replication-choices}

Patroni usa la replicación en flujo de Postgres, que es asíncrona por defecto. La configuración de replicación asíncrona de Patroni admite el ajuste `maximum_lag_on_failover`. Este ajuste evita que una réplica sea promovida durante una conmutación por error si va más atrás que el líder en más bytes que la cantidad configurada. Este valor debería aumentarse o reducirse según los requisitos del negocio. También es posible usar replicación síncrona para mejores garantías de durabilidad. Consulta la [documentación sobre modos de replicación](/es/patroni/replication_modes#replication_modes) para más detalles.

--------

## Las aplicaciones no deben usar superusuarios {#applications-should-not-use-superusers}

Al conectarte desde una aplicación, usa siempre un usuario que no sea superusuario. Patroni necesita acceso a la base de datos para funcionar correctamente. Al usar un superusuario desde una aplicación, potencialmente puedes agotar todo el pool de conexiones, incluidas las conexiones reservadas para superusuarios mediante el ajuste `superuser_reserved_connections`. Si Patroni no puede acceder al primario porque el pool de conexiones está lleno, el comportamiento no será el deseable.

--------

## Probar tu solución de HA {#testing-your-ha-solution}

Probar una solución de HA es un proceso que consume mucho tiempo y con muchas variables. Esto es especialmente cierto si se considera una aplicación multiplataforma. Necesitas un administrador de sistemas capacitado o un consultor para hacer este trabajo. No es algo que podamos cubrir en profundidad en la documentación.

Dicho esto, aquí tienes algunas piezas de tu infraestructura que deberías asegurarte de probar:

- Red (la red frente a tu sistema, así como las propias tarjetas de red (físicas o virtuales))
- E/S de disco
- límites de archivos (nofile en Linux)
- RAM. Incluso si tienes desactivado el oomkiller, la indisponibilidad de RAM puede causar problemas.
- CPU
- Contención en la virtualización (sobreasignación del hipervisor)
- Cualquier limitación de cgroup (probablemente relacionada con lo anterior)
- `kill -9` de cualquier proceso postgres (¡excepto el postmaster!). Es una simulación decente de un segfault.

Algo que no deberías hacer es ejecutar `kill -9` sobre un proceso postmaster. Esto se debe a que eliminar únicamente el proceso no reproduce las condiciones subyacentes de agotamiento de recursos u otros fallos de infraestructura. Si te preocupa que tu infraestructura sea insegura y que un atacante pueda ejecutar `kill -9`, ninguna cantidad de procesos de HA va a arreglar eso. El atacante simplemente volverá a eliminar el proceso, o causará caos de otra manera.
