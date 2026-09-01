---
title: Guidelines de tri des problèmes
weight: 8100
description: "Guidelines pour le tri des problèmes etcd"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/triage/issues.md"
---

## Objectif {#purpose}

Accélérer la gestion des problèmes.

Les problèmes liés à `etcd` sont répertoriés sur https://github.com/etcd-io/etcd/issues
et sont identifiés par des étiquettes. Par exemple, un problème identifié
comme un bogue sera éventuellement étiqueté `area/bug `. Les nouveaux problèmes
apparaissent initialement sans étiquette, mais les responsables `etcd` et les contributeurs actifs
ajoutent des étiquettes en fonction de leurs constatations. La liste détaillée des étiquettes est disponible sur
https://github.com/kubernetes/kubernetes/labels

Voici quelques recherches prédéfinies sur les problèmes, pour plus de commodité :
* [Bugs](https://github.com/etcd-io/etcd/labels/area%2Fbug)
* [Aide demandée](https://github.com/etcd-io/etcd/labels/Help%20Wanted)
* [Problèmes les plus anciens sans tri](https://github.com/etcd-io/etcd/issues?utf8=%E2%9C%93&q=is%3Aopen+sort%3Aupdated-asc+)
* [Réunion de tri des problèmes](https://etcd.io/community/#community-meetings)

## Portée {#scope}

Ces directives servent de document principal pour trier les problèmes reçus dans `etcd`. Tous sont invités à aider à la gestion des problèmes et des demandes de tirage, mais le travail et les responsabilités décrits dans ce document sont destinés aux mainteneurs et contributeurs actifs de `etcd`.

## Vérifier qu'un problème est un bogue {#validate-if-an-issue-is-a-bug}

Vérifiez si le problème est bien un bogue. Si ce n’est pas le cas, ajoutez un commentaire avec vos constatations et fermez l’issue mineure. Pour une issue non mineure, attendez de recevoir une réponse du rapporteur d’incident et vérifiez s’il y a une objection. Si le rapporteur d’incident ne répond pas dans les 30 jours, fermez l’issue. Si le problème ne peut pas être reproduit ou s’il nécessite des informations supplémentaires, laissez un commentaire pour le rapporteur d’incident.

## Problèmes inactifs {#inactive-issues}

Les problèmes qui manquent d'informations fournies par le rapporteur doivent être fermés si ce dernier ne fournit pas d'informations dans les 60 jours.

## Problèmes en double {#duplicate-issues}

Si un problème est en double, ajoutez un commentaire indiquant cette situation, accompagné d'une référence vers le problème original, puis clôturez-le.

## Problèmes qui n'appartiennent pas à etcd {#issues-that-dont-belong-to-etcd}

Parfois, des problèmes sont signalés qui appartiennent en réalité à d'autres projets utilisant `etcd`. Par exemple, des problèmes liés à `grpc` ou `golang`. Ces problèmes doivent être traités en demandant au signalement de créer une issue dans le projet approprié. Fermer l’issue, sauf si un mainteneur et le signaleur estiment nécessaire de la laisser ouverte pour des raisons de suivi.

## Vérifier que les étiquettes importantes sont présentes {#verify-important-labels-are-in-place}

Assurez-vous que l’issue dispose des étiquettes correspondant aux domaines auxquels elle appartient, que les assignataires appropriés sont ajoutés et que l’échéance est définie. Si l’une de ces étiquettes est manquante, ajoutez-la. Si les étiquettes ne peuvent pas être attribuées en raison de privilèges limités ou si l’étiquette correcte ne peut pas être déterminée, cela ne pose pas de problème ; contactez les responsables si nécessaire.

## Poke le propriétaire de l'issue si nécessaire {#poke-issue-owner-if-needed}

Si une issue dont le propriétaire est un développeur n’a pas de demande de fusion (PR) créée en 30 jours, contactez le propriétaire de l’issue et demandez une PR ou la libération de la propriété si nécessaire.
