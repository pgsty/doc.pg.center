---
title: "Documentation de pgBackRest 2.59.3"
linkTitle: pgBackRest
weight: 20
icon: fa-solid fa-couch
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
description: "Sauvegarde et restauration fiable de PostgreSQL — documentation et référence pgBackRest."
module: [PGBACKREST]
categories: [Concept]
upstream_source: pgbackrest
upstream_ref: v2.59.3
upstream_link: "https://pgbackrest.org/"
cascade:
  upstream_source: pgbackrest
  upstream_ref: v2.59.3
  type: docs
  module: [PGBACKREST]
---

--------

## Introduction {#introduction}

pgBackRest est une solution fiable de sauvegarde et de restauration pour PostgreSQL, qui s'adapte sans heurt aux plus grandes bases de données et charges de travail.

Ce miroir de documentation couvre pgBackRest [v2.59.3](https://github.com/pgbackrest/pgbackrest/releases/tag/release/2.59.3). Les notes de version se trouvent sur la page [Notes de version](/fr/pgbackrest/release/).

La version 2.59.3 corrige la génération possible de sous-clés de chiffrement et de sels faibles. La mise à niveau ne remplace pas les sous-clés faibles existantes d’une stanza ; consultez [Sous-clés de chiffrement et sels faibles](/fr/pgbackrest/news/#weak-encryption) pour les vérifications et les mesures correctives.

Merci de nous donner une étoile sur [GitHub](https://github.com/pgbackrest/pgbackrest) si vous appréciez pgBackRest !


--------

## Actualités {#news}

**4 octobre 2026** - [Sous-clés de chiffrement et sels faibles](/fr/pgbackrest/news/#weak-encryption)

**4 octobre 2026** - [pgBackRest 2.59.3 publié](/fr/pgbackrest/news/#release-2-59-3)

**27 septembre 2026** - [pgBackRest 2.59.2 publié](/fr/pgbackrest/news/#release-2-59-2)


--------

## Parrains {#sponsors}

pgBackRest n'existerait pas sans parrainage. La rédaction de nouvelles fonctionnalités, la correction des bogues, la revue des contributions, la réponse aux questions de la communauté et la maintenance prennent une quantité considérable de temps. Veuillez envisager un [parrainage](https://github.com/sponsors/dwsteele) si vous utilisez pgBackRest dans votre entreprise.

Nos parrains : [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com), et [Data Egret](https://dataegret.com/).

Nous remercions nos parrains pour leur investissement dans l'infrastructure open source, au bénéfice de l'ensemble de la communauté PostgreSQL.

Anciens parrains : [Crunchy Data](https://crunchydata.com), [Resonate](https://resonate.com).


--------

## Fonctionnalités {#features}


### Sauvegarde et restauration parallèles {#parallel-backup--restore}

La compression est généralement le goulot d'étranglement lors des opérations de sauvegarde, aussi pgBackRest résout-il ce problème grâce au traitement parallèle et à des algorithmes de compression plus efficaces, tels que `lz4` et `zstd`.


### Opération locale ou distante {#local-or-remote-operation}

Un protocole personnalisé permet à pgBackRest de réaliser des sauvegardes, des restaurations et des archives localement ou à distance via TLS/SSH, avec une configuration minimale. Une interface permet également d'interroger PostgreSQL via la couche de protocole, de sorte qu'un accès distant à PostgreSQL n'est jamais nécessaire, ce qui améliore la sécurité.


### Dépôts multiples {#multiple-repositories}

La possibilité de plusieurs dépôts permet, par exemple, d’avoir un dépôt local avec une rétention réduite pour des restaurations rapides et un dépôt distant avec une rétention plus longue pour assurer la redondance et l’accès à travers l’entreprise.


### Sauvegardes complètes, différentielles et incrémentielles (au niveau fichier ou bloc) {#full-differential--incremental-backups-at-file-or-block-level}

Les sauvegardes complètes, différentielles et incrémentielles sont prises en charge. pgBackRest n'est pas sujet aux problèmes de résolution temporelle de `rsync`, ce qui rend les sauvegardes différentielles et incrémentielles sûres sans nécessiter de calculer la somme de contrôle de chaque fichier. Les sauvegardes au niveau du bloc économisent de l'espace en ne copiant que les parties des fichiers qui ont changé.


### Rotation des sauvegardes et expiration des archives {#backup-rotation--archive-expiration}

Les politiques de rétention peuvent être définies pour les sauvegardes complètes et les sauvegardes différentielles afin d'assurer une couverture pour toute période. L'archive WAL peut être conservée pour toutes les sauvegardes ou uniquement pour les plus récentes. Dans ce dernier cas, les WAL nécessaires à la cohérence des sauvegardes plus anciennes seront conservées dans l'archive.


### Intégrité de la sauvegarde {#backup-integrity}

Les sommes de contrôle sont calculées pour chaque fichier de la sauvegarde et vérifiées lors d'une restauration ou d'une vérification. Une fois la copie des fichiers terminée, la sauvegarde attend que chaque segment WAL nécessaire à la cohérence de la sauvegarde soit arrivé dans le dépôt.

Les sauvegardes dans le dépôt peuvent être stockées au même format qu’un cluster PostgreSQL standard (y compris les espaces de tables). Si la compression est désactivée et que les liens durs sont activés, il est possible de prendre un instantané d’une sauvegarde dans le dépôt et de faire démarrer directement un cluster PostgreSQL sur cet instantané. Cette approche présente un avantage pour les bases de données de taille téraoctet, dont la restauration classique est longue.

Toutes les opérations utilisent fsync au niveau des fichiers et des répertoires pour garantir la durabilité.


### Sommes de contrôle des pages {#page-checksums}

Si les sommes de contrôle des pages sont activées, pgBackRest vérifiera les sommes de contrôle de chaque fichier copié lors d'une sauvegarde. Toutes les sommes de contrôle des pages sont vérifiées lors d'une sauvegarde complète, et les sommes de contrôle des fichiers modifiés sont vérifiées lors des sauvegardes différentielles et incrémentielles.

Les échecs de validation n'interrompent pas le processus de sauvegarde, mais des avertissements précisant exactement quelles pages ont échoué sont affichés sur la console et dans le fichier de journal.

Cette fonctionnalité permet de détecter précocement les corruptions au niveau de la page, avant que les sauvegardes contenant des copies valides des données n'aient expiré.


### Reprise de sauvegarde {#backup-resume}

Une sauvegarde interrompue peut être reprise à l’endroit où elle a été interrompue. Les fichiers déjà copiés sont comparés aux sommes de contrôle du manifeste afin d’assurer l’intégrité. Comme cette opération peut s’effectuer entièrement sur l’hôte du dépôt, elle réduit la charge sur l’hôte PostgreSQL et économise du temps, puisque le calcul des sommes de contrôle est plus rapide que la compression et la retransmission des données.


### Compression en streaming et sommes de contrôle {#streaming-compression--checksums}

Les calculs de compression et de somme de contrôle sont effectués en flux pendant que les fichiers sont copiés vers le dépôt, que le dépôt soit local ou distant.

Si le dépôt est hébergé sur un hôte de dépôt, la compression est effectuée sur l'hôte PostgreSQL et les fichiers sont transmis au format compressé, puis stockés directement sur l'hôte de dépôt. Lorsque la compression est désactivée, un niveau de compression inférieur est utilisé afin d'utiliser efficacement la bande passante disponible tout en minimisant la charge CPU.


### Restauration delta {#delta-restore}

Le manifeste contient des sommes de contrôle pour chaque fichier de la sauvegarde, ce qui permet, lors d'une restauration, d'utiliser ces sommes de contrôle pour accélérer considérablement le traitement. Lors d'une restauration delta, les fichiers absents de la sauvegarde sont d'abord supprimés, puis des sommes de contrôle sont générées pour les fichiers restants. Les fichiers correspondant à ceux de la sauvegarde sont laissés en place, et les autres fichiers sont restaurés selon le processus habituel. Le traitement parallèle peut entraîner une réduction importante du temps de restauration.


### Envoi et récupération parallèles et asynchrones des WAL {#parallel-asynchronous-wal-push--get}

Des commandes dédiées permettent d'envoyer le WAL vers l'archive et de le récupérer depuis l'archive. Ces commandes prennent en charge le parallélisme afin d'accélérer le traitement et s'exécutent de manière asynchrone pour offrir à PostgreSQL le temps de réponse le plus court possible.

La transmission des segments WAL détecte automatiquement les segments WAL qui sont envoyés plusieurs fois et supprime les doublons lorsque les segments sont identiques ; sinon, une erreur est signalée. La transmission asynchrone des segments WAL permet de déléguer le transfert à un autre processus qui compresse les segments WAL en parallèle, afin d’optimiser le débit. Cette fonction peut être essentielle pour les bases de données générant un volume d’écriture extrêmement élevé.

La récupération asynchrone des WAL maintient une file locale de segments WAL décompressés et prêts à être rejoués. Cela réduit le temps nécessaire pour fournir les WAL à PostgreSQL, ce qui maximise la vitesse de relecture. Les connexions et le stockage à latence élevée (comme S3) en bénéficient le plus.

Les commandes push et get garantissent chacune la correspondance entre la base de données et le dépôt en comparant les versions de PostgreSQL et les identifiants système. Cela élimine pratiquement tout risque de configurer incorrectement l'emplacement de l'archive WAL.


### Prise en charge des tablespaces et des liens {#tablespace--link-support}

Les espaces de table sont entièrement pris en charge, et lors d'une restauration, il est possible de les rediriger vers n'importe quel emplacement. Il est également possible de rediriger tous les espaces de table vers un seul emplacement en une seule commande, ce qui est utile pour les restaurations en environnement de développement.

Les liens de fichiers et de répertoires sont pris en charge pour tout fichier ou répertoire du cluster PostgreSQL. Lors d'une restauration, il est possible de restaurer tous les liens à leurs emplacements d'origine, de rediriger certains ou tous les liens, ou de restaurer certains ou tous les liens en tant que fichiers ou répertoires normaux dans le répertoire du cluster.


### Prise en charge des magasins d’objets compatibles S3, Azure et GCS {#s3-azure-and-gcs-compatible-object-store-support}

Les dépôts pgBackRest peuvent être situés dans des magasins d'objets compatibles S3, Azure ou GCS afin de permettre une capacité et une rétention pratiquement illimitées.


### Chiffrement {#encryption}

pgBackRest peut chiffrer le dépôt afin de protéger les sauvegardes, quel que soit l'emplacement de stockage.


### Protection contre les rançongiciels et les logiciels malveillants {#ransomware--malware-protection}

Lorsque le dépôt est stocké dans un stockage d'objets versionné, pgBackRest peut lire le dépôt tel qu'il était à un instant donné. Si des sauvegardes sont supprimées ou corrompues par erreur, par un logiciel malveillant ou un rançongiciel, un instant cible peut être utilisé pour récupérer des données antérieures à la survenance des dégâts.

Le versionnement est pris en charge par les magasins d'objets compatibles S3, Azure et GCS. Le verrouillage d'objets pour S3 ou la suppression réversible pour GCS ou Azure peut offrir une protection supplémentaire contre toute modification non autorisée.


### Compatibilité avec dix versions de PostgreSQL {#compatibility-with-ten-versions-of-postgresql}

pgBackRest prend en charge dix versions de PostgreSQL, soit les cinq versions prises en charge et les cinq dernières versions obsolètes (EOL). Cela permet un délai suffisant pour passer à une version prise en charge.


--------

## Premiers pas {#getting-started}

pgBackRest vise à être facile à configurer et à utiliser :

- [Guides utilisateur](/fr/pgbackrest/user-guide/) pour divers systèmes d'exploitation et versions de PostgreSQL.
- Pages de commande pour les opérations en ligne de commande : [sauvegarde](/fr/pgbackrest/command/backup/), [restauration](/fr/pgbackrest/command/restore/), [vérification](/fr/pgbackrest/command/check/) et [informations](/fr/pgbackrest/command/info/).
- [Référence de configuration](/fr/pgbackrest/configuration/) pour la création de configurations pgBackRest.


--------

## Contributions {#contributions}

Les contributions à pgBackRest sont toujours les bienvenues ! Veuillez consulter nos [Guides pour contribuer](https://github.com/pgbackrest/pgbackrest/blob/main/CONTRIBUTING.md) pour obtenir les détails sur la manière de contribuer avec des fonctionnalités, des améliorations ou des rapports d'incidents.


--------

## Prise en charge {#support}

pgBackRest est entièrement gratuit et open source sous la licence [MIT](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE). Vous pouvez l'utiliser à des fins personnelles ou commerciales sans aucune restriction. Les rapports de bogues sont pris très au sérieux et seront traités aussi rapidement que possible. Veuillez signaler les bogues [ici](https://github.com/pgbackrest/pgbackrest/issues).

La mise en place d'une politique de récupération après sinistre solide, assortie de stratégies de réplication et de sauvegarde appropriées, peut s'avérer une tâche très complexe et intimidante. Vous pourriez avoir besoin d'aide pendant la phase d'architecture et d'un soutien continu afin de garantir que votre entreprise continue de fonctionner sans accroc.

Nos [parrains](#sponsors) proposent des produits et services incluant le support de pgBackRest et peuvent vous aider à répondre à vos besoins de récupération après sinistre.
