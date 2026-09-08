---
title: Plateformes prises en charge
weight: 4800
description: "etcd prise en charge des architectures et systèmes d'exploitation courants"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/supported-platform.md"
aliases: [/etcd/op-guide/supported-platform/]
---

## Support tiers {#support-tiers}

etcd s'exécute sur différentes plates-formes, mais les garanties qu'il fournit dépendent du niveau de prise en charge de la plate-forme :

- **Niveau 1** : entièrement pris en charge par les mainteneurs [etcd][] ; etcd est garanti pour passer tous les tests, y compris les tests fonctionnels et de robustesse.
- **Niveau 2** : etcd est garanti pour passer les tests d'intégration et les tests bout en bout, mais pas nécessairement les tests fonctionnels ou de robustesse.
- **Niveau 3** : etcd est garanti pour être compilé, peut être légèrement testé (ou non), et doit donc être considéré comme _instable_.

## Prise en charge actuelle {#current-support}

Le tableau suivant répertorie les plateformes actuellement prises en charge ainsi que leur niveau de prise en charge correspondant pour etcd :

| Architecture | Système d'exploitation | Niveau de support | Responsables |
|:------------:|:----------------------:|:-----------------:|:------------:|
| AMD64        | Linux                  |      1            | [mainteneurs etcd][] |
| ARM64        | Linux                  |      1            | [mainteneurs etcd][] |
| AMD64        | Darwin                 |      3            |              |
| ARM64        | Darwin                 |      3            |              |
| AMD64        | Windows                |      3            |              |
| ppc64le             | Linux                  |      3            |              |
| s390x               | Linux                  |      3            |              |

Les plateformes non listées ne sont pas prises en charge.

## Prise en charge d'une nouvelle plateforme {#supporting-a-new-platform}

Souhaitez-vous contribuer à etcd en tant que « mainteneur officiel » d'une nouvelle plateforme ? En plus d'engager votre soutien à la plateforme, vous devez configurer une intégration continue (CI) d'etcd répondant aux exigences suivantes, selon le niveau de support :

| intégration continue etcd           | Niveau 1  | Niveau 2  | Niveau 3  |
|---------------------------------------|:-------:|:-------:|:-------:|
| La construction réussit               | &check; | &check; | &check; |
| Les tests unitaires réussissent       | &check; | &check; |         |
| Les tests d'intégration et bout-en-bout réussissent | &check; | &check; |         |
| Les tests de robustesse réussissent   | &check; |         |         |

Pour un exemple de configuration du CI de niveau 2 pour ARM64, consultez [PR etcd #12928][].

## Plateformes non prises en charge {#unsupported-platforms}

Pour éviter d'exécuter accidentellement un serveur etcd sur une plateforme non prise en charge, etcd affiche un message d'avertissement et s'arrête immédiatement, sauf si la variable d'environnement `ETCD_UNSUPPORTED_ARCH` est définie sur l'architecture cible.

> [!WARNING]
> Systèmes 32 bits__
>  etcd présente des **problèmes connus** sur les systèmes 32 bits en raison d'un bogue dans le runtime Go.
> >   Pour plus d'informations, consultez l'[issue Go #599][go-issue] et la note sur le bogue du paquet
>
>   [go-atomic]: https://golang.org/pkg/sync/atomic/#pkg-note-BUG
>   [go-issue]: https://github.com/golang/go/issues/599

[etcd maintainers]: https://github.com/etcd-io/etcd/blob/main/OWNERS
[etcd PR #12928]: https://github.com/etcd-io/etcd/pull/12928
