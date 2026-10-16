---
title: "Modo de pausa/reanudación para el clúster"
linkTitle: "Pausar/Reanudar clúster"
weight: 100
icon: fa-solid fa-stopwatch
description: "Comportamiento del modo de pausa y reanudación para la gestión de clústeres de Patroni."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/pause.html"
---

<a id="pause"></a>

--------

## El objetivo {#the-goal}

Bajo ciertas circunstancias, Patroni necesita dejar temporalmente de gestionar el clúster, conservando al mismo tiempo el estado del clúster en el DCS. Los posibles casos de uso son actividades poco habituales en el clúster, como actualizaciones de versión mayor o recuperación ante corrupción. Durante esas actividades, los nodos a menudo se inician y se detienen por razones desconocidas para Patroni, e incluso algunos nodos pueden ser promovidos temporalmente, violando el supuesto de que se ejecuta un único primario. Por ello, Patroni necesita poder «desvincularse» del clúster en ejecución, implementando un equivalente del modo de mantenimiento de Pacemaker.

--------

## La implementación {#the-implementation}

Cuando Patroni se ejecuta en modo de pausa, no cambia el estado de PostgreSQL, excepto en los siguientes casos:

- Para cada nodo, la clave de miembro en el DCS se actualiza con la información actual sobre el clúster. Esto hace que Patroni ejecute consultas de solo lectura en un nodo miembro si el miembro se está ejecutando.
- Para el primario de Postgres con el bloqueo de líder, Patroni actualiza el bloqueo. Si el nodo con el bloqueo de líder deja de ser el primario (es decir, se degrada manualmente), Patroni liberará el bloqueo en lugar de volver a promover el nodo.
- Se permiten el reinicio manual no programado, la conmutación por error/switchover manual no programados y la reinicialización. No se permite ninguna acción programada. El switchover manual solo se permite si se especifica el nodo al que conmutar.
- Si Patroni detecta primarios «paralelos», emite una advertencia, pero no degrada al primario que no tiene el bloqueo de líder.
- Si no hay bloqueo de líder en el clúster, el primario en ejecución adquiere el bloqueo. Si hay más de un nodo primario, gana el primer primario que adquiera el bloqueo. Si no hay primario, Patroni no intenta promover ninguna réplica. Hay una excepción a esta regla: si no hay bloqueo de líder porque el primario anterior se ha degradado a sí mismo debido a una promoción manual, entonces solo el nodo candidato mencionado en la solicitud de promoción puede tomar el bloqueo de líder. Cuando se concede el nuevo bloqueo de líder (es decir, tras promover una réplica manualmente), Patroni se asegura de que las réplicas que estaban replicando desde el líder anterior cambien al nuevo.
- Cuando Postgres está detenido, Patroni no intenta iniciarlo. Cuando Patroni se detiene, no intenta detener la instancia de Postgres que está gestionando.
- Patroni no intentará eliminar los slots de replicación que no representen ni a otro miembro del clúster ni a un slot listado en la configuración de slots permanentes.

--------

## Guía de usuario {#user-guide}

[patronictl](/es/patroni/patronictl#patronictl) admite los comandos [pause](/es/patroni/patronictl#patronictl_pause) y [resume](/es/patroni/patronictl#patronictl_resume).

También se puede emitir una solicitud `PATCH /config` a la REST API de Patroni con `{"pause": true/false/null}` para actualizar la clave `{namespace}/{cluster}/config` en el DCS.
