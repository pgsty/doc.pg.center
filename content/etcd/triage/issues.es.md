---
title: Directrices para la clasificación de incidencias
weight: 8100
description: "Directrices para clasificar las incidencias de etcd"
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/issues.md"
---

## Propósito {#purpose}

Acelerar la gestión de las incidencias.

Las incidencias de `etcd` se listan en https://github.com/etcd-io/etcd/issues
y se identifican con etiquetas. Por ejemplo, una incidencia identificada
como error acabará recibiendo la etiqueta `area/bug `. Las incidencias nuevas
empiezan sin ninguna etiqueta, pero normalmente los mantenedores de `etcd` y los colaboradores activos
añaden etiquetas según sus hallazgos. La lista detallada de etiquetas puede consultarse en
https://github.com/kubernetes/kubernetes/labels

A continuación se muestran algunas búsquedas predefinidas sobre incidencias para mayor comodidad:
* [Errores](https://github.com/etcd-io/etcd/labels/area%2Fbug)
* [Ayuda solicitada](https://github.com/etcd-io/etcd/labels/Help%20Wanted)
* [Incidencias sin clasificar más antiguas](https://github.com/etcd-io/etcd/issues?utf8=%E2%9C%93&q=is%3Aopen+sort%3Aupdated-asc+)
* [Reunión de clasificación de incidencias](https://etcd.io/community/#community-meetings)

## Alcance {#scope}

Estas directrices sirven como documento principal para clasificar las incidencias entrantes en
`etcd`. Cualquiera está invitado a ayudar a gestionar las incidencias y las PR, pero el trabajo y las responsabilidades tratados en este documento se han pensado para los mantenedores de `etcd` y los colaboradores activos.

## Validar si una incidencia es un error {#validate-if-an-issue-is-a-bug}

Valida si la incidencia es realmente un error. Si no lo es, añade un comentario con los hallazgos y cierra la incidencia trivial. Para una incidencia no trivial, espera la respuesta de quien la reportó y comprueba si hay alguna objeción. Si quien reportó la incidencia no responde en 30 días, cierra la incidencia. Si el problema no se puede reproducir o requiere más información, deja un comentario para quien la reportó.

## Incidencias inactivas {#inactive-issues}

Las incidencias a las que falta información suficiente de quien las reportó deberían cerrarse si no se proporciona información en 60 días.

## Incidencias duplicadas {#duplicate-issues}

Si una incidencia es un duplicado, añade un comentario indicándolo junto con una referencia a la incidencia original y ciérrala.

## Incidencias que no pertenecen a etcd {#issues-that-dont-belong-to-etcd}

A veces se reportan incidencias que en realidad pertenecen a otros proyectos que `etcd` utiliza. Por ejemplo, incidencias de `grpc` o `golang`. Estas incidencias deben tratarse pidiendo a quien las reportó que las abra en el otro proyecto que corresponda. Cierra la incidencia salvo que un mantenedor y quien la reportó consideren necesario mantenerla abierta con fines de seguimiento.

## Verificar que las etiquetas importantes están presentes {#verify-important-labels-are-in-place}

Asegúrate de que la incidencia tenga etiquetas en las áreas a las que pertenece, de que se hayan añadido los asignados adecuados y de que se haya identificado un hito. Si falta alguna de estas etiquetas, añádela. Si no se pueden asignar etiquetas por privilegios limitados o no se puede decidir la etiqueta correcta, no pasa nada; contacta con los mantenedores si es necesario.

## Avisar al propietario de la incidencia si es necesario {#poke-issue-owner-if-needed}

Si una incidencia propiedad de un desarrollador no tiene ninguna PR creada en 30 días, contacta con el propietario de la incidencia y pídele una PR o que libere la propiedad si es necesario.
