---
title: Gestion des demandes de tirage
weight: 8200
description: "Guidelines pour la gestion des demandes d'intégration etcd"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/triage/PRs.md"
aliases: [/etcd/triage/prs/]
---

## Objectif {#purpose}

Accélérer la gestion des PR.

Les demandes de fusion `etcd` sont listées sur https://github.com/etcd-io/etcd/pulls
Une demande de fusion peut avoir divers étiquettes, un délai d'achèvement, un validateur, etc. La liste détaillée des étiquettes est disponible sur
https://github.com/kubernetes/kubernetes/labels

Voici quelques exemples de recherches sur PR pour plus de commodité :
* [Ouvrir les PRs pour le milestone etcd-v3.4](https://github.com/etcd-io/etcd/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+milestone%3Aetcd-v3.4)
* [PRs en cours d'investigation](https://github.com/etcd-io/etcd/labels/Investigating)

## Portée {#scope}

Ces directives servent de document principal pour la gestion des demandes de tirage (PR) dans `etcd`. Tous sont invités à aider à la gestion des PR, mais le travail et les responsabilités décrits dans ce document s'adressent principalement aux mainteneurs et contributeurs actifs de `etcd`.

## Gérer les demandes de tirage inactives {#handle-inactive-prs}
Poke le propriétaire de la PR si les commentaires de relecture ne sont pas traités en 15 jours. Si le propriétaire de la PR ne répond pas en 90 jours, mettez à jour la PR avec un nouveau commit si possible. Sinon, une PR inactif doit être fermée après 180 jours.

## Interroger le réviseur si nécessaire {#poke-reviewer-if-needed}

Les relecteurs sont réactifs de manière ponctuelle, mais étant donné que chacun est occupé, accordez-leur un délai après la demande de relecture si la réponse rapide n’est pas fournie. Si aucune réponse n’est donnée dans les 10 jours, n’hésitez pas à les contacter en ajoutant un commentaire dans la demande de fusion, en envoyant un courriel ou un message sur Slack.

## Vérifier que les étiquettes importantes sont présentes {#verify-important-labels-are-in-place}

Assurez-vous que les revueurs appropriés sont ajoutés à la demande de fusion (PR). Vérifiez également qu'une étiquette de livrable (milestone) est définie. Si l'une de ces étiquettes ou toute autre étiquette importante est manquante, ajoutez-la. Si aucune étiquette correcte ne peut être déterminée, laissez un commentaire pour inviter les responsables à intervenir selon le besoin.
