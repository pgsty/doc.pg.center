---
title: "Questions fréquemment posées"
linkTitle: "FAQ"
weight: 70
description: "Questions fréquentes sur la sauvegarde, la restauration, la configuration et le dépannage avec pgBackRest."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Référence]
aliases: [/pgbackrest/faq/]
upstream_link: "https://pgbackrest.org/faq.html"
---

--------

## Introduction {#introduction}

Les questions fréquemment posées ont pour but de fournir des précisions sur des questions spécifiques qui peuvent ou non être traitées dans le guide utilisateur, la configuration ou la référence des commandes. Si vous ne trouvez pas de réponse à votre problème particulier ici, n'oubliez pas que la liste des problèmes pgBackRest [Issues List in GitHub](https://github.com/pgbackrest/pgbackrest/issues) constitue également une ressource précieuse.


--------

## Que faire si j’obtiens l’erreur « impossible de trouver le segment WAL » ? {#what-if-i-get-the-could-not-find-wal-segment-error}

La cause de cette erreur peut résulter de nombreux problèmes différents, dont certains peuvent être :

- `archive_command` mal configuré
- fichiers de configuration pgBackRest incorrectement configurés
- problème de réseau ou d'autorisations
- problème de configuration d'un produit tiers, par exemple S3, Swift ou MinIO
- grande quantité de WAL en attente d'archivage

Il est recommandé de :

- vérifiez le `archive_command` dans PostgreSQL
- vérifiez les paramètres de configuration de pgBackRest sur chaque hôte (par exemple, les paramètres `pg*` sont définis sur l'hôte du dépôt et les paramètres `repo*` sur l'hôte pg)
- exécutez la commande `check` avec `--archive-timeout` défini à une valeur supérieure à celle du fichier de configuration pgBackRest (ou à la valeur par défaut) afin de vérifier si la file d'attente WAL nécessite plus de temps pour se vider. Si le système génère beaucoup de WAL, envisagez de configurer [asynchronous archiving](/fr/docs/pgbackrest/user-guide/#asynchronous-archiving)


--------

## Comment purger manuellement un jeu de sauvegarde ? {#how-do-i-manually-purge-a-backup-set}

Une sauvegarde complète peut être expirée à l’aide de l’option `--set`, comme expliqué dans [Référence des commandes : Expirer](/fr/docs/pgbackrest/command/expire/).


--------

## Comment puis-je configurer les options indépendamment pour chaque commande ? {#how-can-i-configure-options-independently-for-each-command}

pgBackRest peut définir des options indépendamment dans le fichier de configuration pour chaque commande. [Configurer une stanza de cluster](/fr/docs/pgbackrest/user-guide/#configure-cluster-stanza) décrit cette fonctionnalité ainsi que la hiérarchie de priorité des options.

Par exemple, l’option `process-max` peut être optimisée pour chaque commande :

```ini
[global]
# used where not overridden
process-max=2

[global:backup]
# more cores for backup
process-max=4

[global:restore]
# all the cores for restore
process-max=8

[global:archive-push]
# more cores for archive-push
process-max=3

[global:archive-get]
# fewer cores for archive-get
process-max=1
```


--------

## Puis-je utiliser des points (points) dans le nom de mon bucket S3 ? {#can-i-use-dots-periods-in-my-s3-bucket-name}

RFC-2818 n'autorise pas les caractères génériques à correspondre à un point (.), aussi les noms de bucket S3 ne doivent pas contenir de points. Si le nom de bucket S3 contient des points, une erreur telle que « unable to find hostname 'my.backup.bucket.s3.amazonaws.com' in certificate common name or subject alternative names » se produira.

L'exception est `repo-s3-uri-style=path`, qui ajoute le nom du bucket au URI au lieu de l'hôte. Comme le bucket n'est pas inclus dans le nom d'hôte, le certificat est vérifié uniquement par rapport à l'endpoint, et les points dans le nom du bucket ne posent pas de problème. Notez que les URI au format chemin ne sont pas pris en charge par toutes les solutions de stockage objet compatibles S3.


--------

## Où puis-je trouver des paquets pour les versions antérieures de pgBackRest ? {#where-can-i-find-packages-for-older-versions-of-pgbackrest}

Le dépôt [apt.PostgreSQL.org](https://apt.postgresql.org) maintient une [archive des anciennes versions](https://apt-archive.postgresql.org). Debian maintient également [des instantanés](https://snapshot.debian.org/binary/pgbackrest/) de toutes les versions de test.


--------

## Pourquoi une tentative de sauvegarde échoue-t-elle lorsque `backup-standby=y` et la base de données en mode standby sont hors ligne ? {#why-does-a-backup-attempt-fail-when-backup-standbyy-and-the-standby-database-is-down}

Configurer la sauvegarde à partir d’un serveur secondaire est généralement destiné à réduire la charge sur le principal. Passer à la sauvegarde sur le principal lorsque le serveur secondaire est hors service contredit souvent cet objectif. Il n’est pas recommandé de surcharger le principal dans une situation où le système présente déjà des défaillances. Les sauvegardes ne sont pas critiques à condition d’en disposer une récente — ce qui compte, c’est de maintenir le archivage des WAL. Il reste ample temps pour effectuer une sauvegarde lorsque le système est à nouveau stable.

Si vous avez réellement besoin d'une sauvegarde, la solution consiste à disposer de plus de serveurs secondaires ou à supprimer `backup-standby`. Cette restriction peut être levée en ligne de commande grâce à `--no-backup-standby`, ce qui évite de réconfigurer le système pour une sauvegarde ponctuelle.


--------

## Dois-je configurer mon dépôt sur un hôte de secours ? {#should-i-setup-my-repository-on-a-standby-host}

No. Lorsque les bases de données primaire et secondaire sont configurées, les fichiers de configuration de pgBackRest doivent être symétriques afin de gérer sans heurt les basculements. Si ce n’est pas le cas, les configurations devront être modifiées lors d’un basculement, ou des problèmes supplémentaires pourraient survenir.

Consultez la section [Hôte dédié au dépôt](/fr/docs/pgbackrest/user-guide/#dedicated-repository-host) du guide utilisateur pour plus d'informations.


--------

## La restauration à un instant donné basée sur le temps ne semble pas fonctionner, pourquoi ? {#time-based-point-in-time-recovery-does-not-appear-to-work-why}

L'erreur la plus fréquente lors de l'utilisation de la restauration à un instant donné basée sur le temps est d'oublier de sélectionner un jeu de sauvegarde antérieur à l'instant cible. pgBackRest tentera de déterminer une sauvegarde à partir de laquelle poursuivre le traitement à partir de l'instant spécifié par `--target=` si l'option `--set` n'est pas précisée. Si aucun jeu de sauvegarde n'est trouvé, la restauration par défaut utilisera la dernière sauvegarde. Toutefois, si la dernière sauvegarde est postérieure à l'instant cible, alors `--target=` n'est pas considéré comme valide par PostgreSQL et est donc ignoré, ce qui entraîne une récupération des journaux (WAL) jusqu'à l'instant le plus récent disponible.

Pour utiliser l'option `--set`, sélectionnez un jeu de sauvegarde en exécutant la commande `info` et en identifiant la sauvegarde dont l'horodatage de fin est antérieur à l'heure cible. Ensuite, lors de la restauration, précisez l'option `--set=BACKUP_LABEL` où `BACKUP_LABEL` correspond au jeu de sauvegarde sélectionné.

Consultez la section [Restauration à un instant donné](/fr/docs/pgbackrest/user-guide/#point-in-time-recovery) du guide utilisateur pour plus d'informations.


--------

## Qu'est-ce que signifie le suffixe de l'archive WAL ? {#what-does-the-wal-archive-suffix-mean}

Le suffixe est la somme de contrôle SHA1 utilisée pour vérifier l'intégrité du fichier. Il n'existe aucun moyen de l'omettre.


--------

## La restauration de types de sauvegarde spécifiques (pleine, différentielle, incrémentielle) prend-elle plus de temps ? {#does-it-take-longer-to-restore-specific-backup-types-full-differential-incremental}

Les différents types de sauvegarde nécessitent le même temps de restauration. La restauration récupère les fichiers en se basant sur le manifeste de sauvegarde, qui peut faire référence à des fichiers provenant d'une sauvegarde antérieure dans le cas de sauvegardes incrémentielles ou différentielles. Bien qu’il puisse y avoir des différences dans le temps passé à *créer* une sauvegarde donnée (selon le type de sauvegarde), la taille de la base de données détermine le temps de restauration (le débit disque, le débit réseau, etc. étant égaux).


--------

## Comment puis-je exporter une sauvegarde pour l'utiliser dans un environnement hors réseau ? {#how-can-i-export-a-backup-for-use-in-a-network-isolated-environment}

pgBackRest utilise le dépôt non seulement pour stocker les sauvegardes et les archives WAL, mais aussi pour conserver les métadonnées essentielles nécessaires à des fonctionnalités telles que la compression, le chiffrement et le regroupement de fichiers. En raison de cela, copier simplement une sauvegarde accompagnée d'un sous-ensemble de fichiers WAL ne fonctionnera généralement pas, sauf si des conditions très spécifiques et restrictives sont respectées.

Toutefois, une solution de contournement existe si votre objectif est de créer une exportation autonome d'une base de données que vous pouvez transférer (par exemple, via une clé USB). Vous pouvez effectuer une sauvegarde avec l'option [`--archive-copy`](/fr/docs/pgbackrest/command/backup/#copy-archive-option---archive-copy) activée afin de garantir que les segments WAL nécessaires sont stockés conjointement avec la sauvegarde. Ensuite, procédez à la restauration à l'aide de [`--type=none`](/fr/docs/pgbackrest/command/restore/#type-option---type) `--pg1-path=/your/target/path`. Cela produit un répertoire de données PostgreSQL restauré contenant déjà tous les fichiers WAL requis dans `pg_wal`, de manière similaire à ce que `pg_basebackup` créerait.

Vous pouvez ensuite copier ce répertoire vers un autre système, et PostgreSQL devrait être en mesure de s'en remettre sans avoir besoin d'accéder au dépôt pgBackRest.

Veuillez noter qu’il ne sera pas effectué de basculement de timeline lors de la récupération de cette sauvegarde, ce qui signifie que ce cluster ne doit pas envoyer de WAL vers le dépôt d’origine d’où il a été exporté. Si le nouveau cluster est dans un environnement réseau isolé, cela ne devrait pas poser de problème.
