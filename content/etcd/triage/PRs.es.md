---
title: Gestión de pull requests
weight: 8200
description: "Directrices para gestionar las pull requests de etcd"
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/PRs.md"
---

## Propósito {#purpose}

Acelerar la gestión de las pull requests.

Las pull requests de `etcd` se listan en https://github.com/etcd-io/etcd/pulls
Una pull request (PR) puede tener varias etiquetas, un hito, un revisor, etc. La lista detallada de etiquetas puede consultarse en
https://github.com/kubernetes/kubernetes/labels

A continuación se muestran algunos ejemplos de búsquedas de PR para mayor comodidad:
* [PR abiertas para el hito etcd-v3.4](https://github.com/etcd-io/etcd/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+milestone%3Aetcd-v3.4)
* [PR en investigación](https://github.com/etcd-io/etcd/labels/Investigating)

## Alcance {#scope}

Estas directrices sirven como documento principal para gestionar las pull requests en `etcd`. Cualquiera está invitado a ayudar a gestionar las PR, pero el trabajo y las responsabilidades tratados en este documento se han pensado para los mantenedores de `etcd` y los colaboradores activos.

## Gestionar las PR inactivas {#handle-inactive-prs}
Avisa al propietario de la PR si los comentarios de revisión no se atienden en 15 días. Si el propietario de la PR no responde en 90 días, actualiza la PR con un nuevo commit si es posible. Si no, la PR inactiva debería cerrarse después de 180 días.

## Avisar al revisor si es necesario {#poke-reviewer-if-needed}

Los revisores suelen responder con puntualidad, pero teniendo en cuenta que todo el mundo está ocupado, dales algo de tiempo tras solicitar la revisión si no se recibe una respuesta rápida. Si no hay respuesta en 10 días, no dudes en contactar con ellos añadiendo un comentario en la PR o enviando un correo electrónico o un mensaje por Slack.

## Verificar que las etiquetas importantes están presentes {#verify-important-labels-are-in-place}

Asegúrate de que se hayan añadido a la PR los revisores adecuados. Asimismo, comprueba que se haya identificado un hito. Si falta alguna de estas etiquetas u otra etiqueta importante, añádela. Si no se puede decidir una etiqueta correcta, deja un comentario para que los mantenedores lo hagan según sea necesario.
