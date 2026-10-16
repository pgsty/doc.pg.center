---
title: "Modo a prueba de fallos del DCS"
weight: 110
icon: fa-solid fa-shield-halved
description: "Comportamiento, requisitos y advertencias operativas del modo a prueba de fallos del DCS."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html"
---

<a id="dcs_failsafe_mode"></a>

--------

## El problema {#the-problem}

Patroni depende en gran medida del Distributed Configuration Store (DCS) para resolver la tarea de las elecciones de líder y detectar particiones de red. Es decir, el nodo solo puede ejecutar Postgres como primario si puede actualizar el bloqueo de líder en el DCS. En caso de que la actualización del bloqueo de líder falle, Postgres se degrada inmediatamente y se inicia en modo de solo lectura. Dependiendo del DCS utilizado, las probabilidades de encontrarse con el «problema» varían. Por ejemplo, con Etcd que se utiliza únicamente para Patroni, las probabilidades son casi nulas, mientras que con la API de K8s (respaldada por Etcd) podría observarse con más frecuencia.

--------

## Razones de la implementación actual {#reasons-for-the-current-implementation}

El fallo en la actualización del bloqueo de líder puede deberse a dos razones principales:

1.  Partición de red
2.  Caída del DCS

En general, es imposible distinguir entre estas dos situaciones desde un único nodo y, por lo tanto, Patroni asume el peor caso: la partición de red. En el caso de una red particionada, otros nodos del clúster de Patroni podrían tomar con éxito el bloqueo de líder y promover Postgres a primario. Para evitar un split-brain, el primario antiguo se degrada antes de que expire el bloqueo de líder.

--------

## Modo a prueba de fallos del DCS {#dcs-failsafe-mode}

Introducimos una nueva opción especial, el `failsafe_mode`. Solo puede habilitarse mediante la [configuración dinámica](/es/patroni/config/dynamic#dynamic) global almacenada en la clave `/config` del DCS. Si el modo a prueba de fallos está habilitado y la actualización del bloqueo de líder en el DCS falla por motivos diferentes a una discrepancia de versión/valor/índice, Postgres puede seguir ejecutándose como primario si puede acceder a todos los miembros conocidos del clúster mediante la REST API de Patroni.

--------

## Detalles de implementación de bajo nivel {#low-level-implementation-details}

- Introducimos una nueva clave permanente en el DCS, llamada `/failsafe`.
- La clave `/failsafe` contiene todos los miembros conocidos del clúster de Patroni dado en un momento dado.
- El líder actual mantiene la clave `/failsafe`.
- Un miembro solo puede participar en la carrera por el liderazgo y convertirse en el nuevo líder si está presente en la clave `/failsafe`.
- Si el clúster consta de un único nodo, la clave `/failsafe` contendrá un único miembro.
- En caso de «caída» del DCS, el primario existente se conecta a todos los miembros listados en la clave `/failsafe` mediante la REST API `POST /failsafe` y puede seguir ejecutándose como primario si todas las réplicas lo reconocen.
- Si uno de los miembros no responde, el primario se degrada.
- Las réplicas utilizan las solicitudes entrantes de la REST API `POST /failsafe` como indicador de que el primario sigue vivo. Esta información se almacena en caché durante `ttl` segundos.

--------

## Preguntas frecuentes {#faq}

- ¿Por qué DEBE el primario actual ver TODOS los demás miembros? ¿No podemos confiar en el cuórum aquí?

  ¡Es una excelente pregunta! El problema es que la visión del cuórum puede ser diferente desde la perspectiva del DCS y de Patroni. Mientras que los nodos del DCS deben estar distribuidos uniformemente entre las zonas de disponibilidad, no existe tal regla para Patroni y, lo que es más importante, no existe un mecanismo para introducir y aplicar tal regla. Si la mayoría de los nodos de Patroni acaba en la parte perdedora de la red particionada (incluido el primario) mientras los nodos de la minoría están en la parte ganadora, el primario debe degradarse. Solo comprobando TODOS los demás miembros es posible detectar tal situación.

- ¿Qué ocurre si un nodo/pod se termina mientras el DCS está caído?

  Si el DCS no es accesible, la comprobación «¿son accesibles TODOS los demás miembros del clúster?» se ejecuta en cada ciclo del bucle de latido (cada `loop_wait` segundos). Si el pod/nodo se termina, la comprobación fallará y Postgres se degradará a solo lectura y no se recuperará hasta que el DCS se restaure.

- ¿Qué ocurre si se pierden todos los miembros del clúster de Patroni mientras el DCS está caído?

  Patroni podría configurarse para crear la nueva réplica a partir de la copia de seguridad incluso cuando el clúster no tiene líder. Pero, si el nuevo miembro no está presente en la clave `/failsafe`, no podrá tomar el bloqueo de líder ni promoverse.

- ¿Qué ocurrirá si el primario perdió el acceso al DCS mientras que las réplicas no?

  El primario ejecutará el código failsafe y contactará con todas las réplicas conocidas. Estas réplicas utilizarán esta información como indicador de que el primario está vivo y no iniciarán la carrera por el liderazgo incluso si el bloqueo de líder en el DCS ha expirado.

- ¿Cómo habilitar el modo a prueba de fallos?

  Antes de habilitar el `failsafe_mode`, asegúrate de que la versión de Patroni en todos los miembros esté actualizada. Después de eso, puedes usar la [REST API](/es/patroni/rest_api#rest_api) `PATCH /config` o [patronictl edit-config -s failsafe_mode=true](/es/patroni/patronictl#patronictl_edit_config_parameters)
