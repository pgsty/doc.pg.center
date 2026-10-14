---
title: "Référence des commandes"
linkTitle: "Commandes"
weight: 40
description: "Référence de commande pgBackRest avec toutes les options pour les opérations de sauvegarde, de restauration, d'archive et de gestion."
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [Référence]
upstream_link: "https://pgbackrest.org/command.html"
---

## Introduction {#introduction}

Les commandes sont utilisées pour exécuter les différentes fonctions de pgBackRest. Ici, les options de commande sont listées de manière exhaustive, c'est-à-dire que chaque option applicable à une commande est indiquée avec cette commande, même si elle s'applique à une ou plusieurs autres commandes. Cela inclut toutes les options qui peuvent également être configurées dans `pgbackrest.conf`.

Les options non booléennes configurées dans `pgbackrest.conf` peuvent être réinitialisées à leur valeur par défaut en ligne de commande en utilisant le préfixe `reset-`. Cette fonctionnalité peut être utilisée pour effectuer une restauration directement sur un hôte de dépôt. En règle générale, pgBackRest génère une erreur car il détecte que l'hôte de base de données est distant et qu'une restauration ne peut pas être effectuée à distance. En ajoutant `--reset-pg1-host` en ligne de commande, pgBackRest ignore l'hôte de base de données distant et effectue la restauration localement. Il peut être nécessaire de passer un nouvel `--pg1-path` pour forcer la restauration à se produire dans un chemin spécifique, c'est-à-dire non pas le chemin utilisé sur l'hôte de base de données.

Le préfixe `no-` peut être utilisé pour définir une option booléenne à false en ligne de commande.

Toute option peut être définie dans une variable d’environnement en utilisant le préfixe `PGBACKREST_` et le nom de l’option en majuscules, en remplaçant `-` par `_`, par exemple `pg1-path` devient `PGBACKREST_PG1_PATH` et `stanza` devient `PGBACKREST_STANZA`. Les options booléennes sont représentées comme elles le seraient dans un fichier de configuration, par exemple `PGBACKREST_COMPRESS="n"`, et les variantes `reset-*` ne sont pas autorisées. Les options pouvant être spécifiées plusieurs fois en ligne de commande ou dans un fichier de configuration peuvent être représentées en séparant les valeurs par des deux-points, par exemple `PGBACKREST_DB_INCLUDE="db1:db2"`.

Les options en ligne de commande remplacent les options d'environnement, qui remplacent à leur tour les options du fichier de configuration.

Voir [Introduction à la configuration](/fr/pgbackrest/configuration/#introduction) pour obtenir des informations sur les types d'option

## Commandes {#commands}

| Commande                                                          | Résumé                                                                                 |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [**`annotate`**](/fr/pgbackrest/command/annotate/)             | Ajouter, modifier ou supprimer des annotations de sauvegarde après la création de la sauvegarde.                  |
| [**`archive-get`**](/fr/pgbackrest/command/archive-get/)       | Récupérer des segments WAL archivés pour une restauration, une restauration à un instant donné ou une récupération d’un réplica.                     |
| [**`archive-push`**](/fr/pgbackrest/command/archive-push/)     | Accepter les segments WAL provenant de PostgreSQL et les envoyer vers les dépôts configurés.           |
| [**`backup`**](/fr/pgbackrest/command/backup/)                 | Créer des sauvegardes vers le dépôt cible (par défaut, le dépôt de priorité la plus élevée).      |
| [**`check`**](/fr/pgbackrest/command/check/)                   | Valider la configuration des sauvegardes/archives d’un stanza et l’état de santé de l’archivage du WAL.                  |
| [**`expire`**](/fr/pgbackrest/command/expire/)                 | Expire les sauvegardes et les WAL archivés selon les politiques de rétention configurées.                 |
| [**`help`**](/fr/pgbackrest/command/help/)                     | Afficher l’aide des commandes et options au niveau général, de la commande ou de l’option.                      |
| [**`info`**](/fr/pgbackrest/command/info/)                     | Afficher l’état/métadonnées d’un stanza et des sauvegardes au format texte ou JSON.                       |
| [**`repo-get`**](/fr/pgbackrest/command/repo-get/)             | Lire les fichiers du dépôt (comme `cat`) pour l’administration, l’investigation et les tests.      |
| [**`repo-ls`**](/fr/pgbackrest/command/repo-ls/)               | Lister les fichiers/chemins du dépôt (comme `ls`) pour l’administration, l’investigation et les tests. |
| [**`restore`**](/fr/pgbackrest/command/restore/)               | Restaurer à partir d’une sauvegarde (la plus récente par défaut) avec une restauration à un instant donné facultative.           |
| [**`server`**](/fr/pgbackrest/command/server/)                 | Exécuter le serveur TLS pgBackRest pour accéder à distance sans SSH.                       |
| [**`server-ping`**](/fr/pgbackrest/command/server-ping/)       | Vérifier qu’un serveur TLS pgBackRest accepte les connexions.                     |
| [**`stanza-create`**](/fr/pgbackrest/command/stanza-create/)   | Créer les métadonnées d’un stanza dans tous les dépôts configurés.                                  |
| [**`stanza-delete`**](/fr/pgbackrest/command/stanza-delete/)   | Supprimer définitivement toutes les sauvegardes et archives d’un stanza.                               |
| [**`stanza-upgrade`**](/fr/pgbackrest/command/stanza-upgrade/) | Mettre à jour les métadonnées d’un stanza après une mise à niveau majeure de PostgreSQL.                       |
| [**`start`**](/fr/pgbackrest/command/start/)                   | Réactiver les processus pgBackRest après une précédente `stop`.                           |
| [**`stop`**](/fr/pgbackrest/command/stop/)                     | Empêcher l’exécution de nouveaux processus pgBackRest et, éventuellement, forcer l’arrêt des processus en cours.                |
| [**`verify`**](/fr/pgbackrest/command/verify/)                 | Vérifier que les données de sauvegarde et d’archive du dépôt sont valides.                         |
| [**`version`**](/fr/pgbackrest/command/version/)               | Afficher la version installée de pgBackRest.                                               |
{.full-width}
