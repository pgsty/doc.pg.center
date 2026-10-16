---
title: Glosario
weight: 2900
description: Términos usados en la documentación, la línea de comandos y el código fuente de etcd
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/glossary.md"
---

Este documento define los distintos términos usados en la documentación, la línea de comandos y el código fuente de etcd.

## Alarma {#alarm}

El servidor de etcd genera una alarma cada vez que el clúster necesita la intervención de un operador para mantenerse fiable.

## Autenticación {#authentication}

La autenticación gestiona los permisos de acceso de los usuarios a los recursos de etcd.

## Cliente {#client}

Un cliente se conecta al clúster de etcd para emitir solicitudes de servicio, como recuperar pares clave-valor, escribir datos u observar actualizaciones.

## Clúster {#cluster}

Un clúster consta de varios miembros.

El nodo de cada miembro sigue el protocolo de consenso de raft para replicar los registros. El clúster recibe propuestas de los miembros, las confirma y las aplica al almacén local.

## Compactación {#compaction}

La compactación descarta todo el historial de eventos de etcd y las versiones sustituidas de las claves anteriores a una revisión dada. Se usa para recuperar espacio de almacenamiento en la base de datos del backend de etcd.

## Elección {#election}

El clúster de etcd celebra elecciones entre sus miembros para elegir un líder como parte del protocolo de consenso de raft.

## Endpoint {#endpoint}

Una URL que apunta a un servicio o recurso de etcd.

## Clave {#key}

Un identificador definido por el usuario para almacenar y recuperar valores definidos por el usuario en etcd.

## Rango de claves {#key-range}

Un conjunto de claves que contiene una clave individual, un intervalo léxico para todas las x tales que a <= x < b, o todas las claves mayores que una clave dada.

## Espacio de claves {#keyspace}

El conjunto de todas las claves de un clúster de etcd.

## Concesión {#lease}

Un contrato renovable de corta duración que elimina las claves asociadas a él al expirar.

## Miembro {#member}

Un servidor etcd lógico que participa en el servicio de un clúster de etcd.

## Revisión de modificación {#modification-revision}

La primera revisión que contiene la última escritura de una clave dada.

## Par {#peer}

Un par es otro miembro del mismo clúster.

## Propuesta {#proposal}

Una propuesta es una solicitud (por ejemplo, una solicitud de escritura, una solicitud de cambio de configuración) que debe pasar por el protocolo de raft.

## Cuórum {#quorum}

El número de miembros activos necesario para el consenso que modifica el estado del clúster. etcd requiere una mayoría de miembros para alcanzar el cuórum.

## Revisión {#revision}

Un contador de 64 bits para todo el clúster que empieza en 1 y se incrementa cada vez que se modifica el espacio de claves.

## Rol {#role}

Una unidad de permisos sobre un conjunto de rangos de claves que puede concederse a un conjunto de usuarios para el control de acceso.

## Instantánea {#snapshot}

Una copia de seguridad puntual del estado del clúster de etcd.

## Almacén {#store}

El almacenamiento físico que respalda el espacio de claves del clúster.

## Término {#term}

Un término es un entero que aumenta de forma monótona y que está asociado a cada elección de líder en el algoritmo de Raft.
Para un término solo puede haber un líder elegido, y el término se incrementa con cada cambio de líder.

## Transacción {#transaction}

Un conjunto de operaciones ejecutadas atómicamente. Todas las claves modificadas en una transacción comparten la misma revisión de modificación.

## Versión de la clave {#key-version}

El número de escrituras de una clave desde su creación, comenzando en 1. La versión de una clave inexistente o eliminada es 0.

## Observador {#watcher}

Un cliente abre un observador para vigilar las actualizaciones de un rango de claves dado.
