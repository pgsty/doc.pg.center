---
title: Fonctionnalités d’etcd
weight: 3750
description: Utilisation des fonctionnalités d’etcd
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/features.md"
---

Ce document présente un aperçu des fonctionnalités d’etcd afin d’aider les utilisateurs à mieux comprendre ces fonctionnalités et le processus de dépréciation associé. Si vous souhaitez en savoir plus sur la manière dont les fonctionnalités sont développées dans etcd, veuillez consulter ces [guides de développement](https://github.com/etcd-io/etcd/blob/main/Documentation/contributor-guide/features.md).

Les fonctionnalités d'etcd sont classées en trois stades : expérimentales, stables et non sécurisées. Vous pouvez obtenir la liste des fonctionnalités en exécutant `etcd --help`.

## Expérimental {#experimental}

Afin d'obtenir un retour rapide, toute nouvelle fonctionnalité est généralement ajoutée en tant que fonctionnalité expérimentale. Une fonctionnalité expérimentale peut être identifiée en examinant le nom du drapeau, qui doit comporter le préfixe `--experimental`. Veuillez prendre en compte les points suivants lors de l'utilisation d'une fonctionnalité expérimentale :
- Elle peut contenir des bogues en raison d'un manque de tests utilisateurs. Son activation peut ne pas fonctionner comme prévu.
- Elle est désactivée par défaut.
- Le support de cette fonctionnalité peut être supprimé à tout moment sans préavis.
    - Elle peut être supprimée dans la prochaine version mineure ou majeure sans respecter la [politique de dépréciation des fonctionnalités](#feature-deprecation), sauf si elle devient stable.
    - L'équipe du projet apprécierait que les utilisateurs signalent tout problème lié aux fonctionnalités expérimentales. Toutefois, ces problèmes peuvent recevoir une priorité plus faible que ceux liés aux fonctionnalités stables.
- Un drapeau de fonctionnalité expérimentale est [déprécié](#feature-deprecation) lorsqu'il atteint le stade stable. Les utilisateurs devraient commencer à utiliser un drapeau de fonctionnalité stable dès que possible.

## Stable {#stable}

Ce stade est le plus courant pour les fonctionnalités dans etcd. Une fonctionnalité stable est caractérisée comme suit :
- Prise en charge dans le cadre des versions prises en charge d'etcd.
- Peut être activée par défaut.
- La suppression du support doit respecter la politique de [dépréciation de fonctionnalité](#feature-deprecation).

## Non sécurisé {#unsafe}

Les fonctionnalités non sécurisées sont rares et listées dans la section `Unsafe feature:` de la documentation d'utilisation d'etcd. Par défaut, elles sont désactivées. Elles devraient être utilisées avec précaution, en suivant la documentation. Une fonctionnalité non sécurisée peut être supprimée dans la prochaine version mineure ou majeure sans respecter la politique de dépréciation des fonctionnalités.

## Dépréciation de fonctionnalité {#feature-deprecation}

### Expérimental {#experimental-1}
Une fonctionnalité expérimentale est dépréciée lorsqu'elle atteint le stade stable.
- La documentation de la fonctionnalité expérimentale affichera un message de dépréciation accompagné d'une recommandation visant à utiliser un drapeau de fonctionnalité stable associé. Par exemple, `DEPRECATED. Use <feature-name> instead.`
- Une fonctionnalité dépréciée sera supprimée dans la version suivante.

### Stable {#stable-1}
Lorsque le projet évolue, une fonctionnalité stable peut parfois devoir être dépréciée et supprimée. Lorsque cela se produit,
- la documentation de la fonctionnalité affichera un message d'avertissement avant la version planifiée de dépréciation. Par exemple, `To be deprecated in <release>.`. Si une nouvelle fonctionnalité est déjà prévue pour remplacer la fonctionnalité `To be deprecated`, la documentation indiquera également ce fait. Par exemple, `Use <feature-name> instead.`.
- La fonctionnalité sera dépréciée lors de la version planifiée. À ce moment-là, la documentation de la fonctionnalité affichera un message de dépréciation accompagné d'une recommandation d’utilisation d’une fonctionnalité stable associée. Par exemple, `DEPRECATED. Use <feature-name> instead.`.
- Une fonctionnalité dépréciée sera supprimée lors de la version suivante.
