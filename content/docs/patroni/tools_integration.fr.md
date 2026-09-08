---
title: "Intégration avec d'autres outils"
linkTitle: "Intégration des outils"
weight: 150
icon: fas fa-puzzle-piece
description: "Intégration de Patroni avec des outils externes de sauvegarde et d'orchestration."
module: [PATRONI]
categories: [Concept]
aliases: [/patroni/tools_integration/]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni est capable d'intégrer d'autres outils de votre infrastructure. Dans cette section, vous trouverez une liste d'exemples, qui, bien qu'elle ne soit pas exhaustive, peut vous inspirer sur les façons dont Patroni peut s'intégrer à d'autres outils.

--------

## Barman {#barman}

Patroni fournit une application nommée `patroni_barman` qui intègre la logique de communication avec `pg-backup-api`, vous permettant ainsi d'effectuer des opérations Barman à distance.

Cette application possède actuellement plusieurs sous-commandes : `recover` et `config-switch`.

### patroni_barman recover {#patroni_barman-recover}

Le sous-commande `recover` peut être utilisé comme méthode personnalisée d'amorçage ou de création de réplique. Vous trouverez plus d'informations à ce sujet dans [replica_imaging_and_bootstrap](/fr/docs/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### configuration du basculement de Patroni Barman {#patroni_barman-config-switch}

Le sous-commande `config-switch` est conçu pour être utilisé comme un rappel `on_role_change` dans Patroni. Par exemple, supposez que vous diffusez les WAL depuis votre serveur primaire actuel vers votre hôte Barman. En cas de basculement dans le cluster, vous souhaiterez peut-être commencer à diffuser les WAL depuis le nouveau serveur primaire. Vous pouvez réaliser cela en utilisant `patroni_barman config-switch` comme rappel `on_role_change`.

> [!NOTE]
> Ce sous-commande dépend de la commande `barman config-switch`, qui est chargée de remplacer la configuration d'un serveur Barman en appliquant un modèle prédéfini au-dessus de celle existante. Cette commande est disponible depuis Barman 3.10. Veuillez consulter la documentation Barman pour plus de détails.

Ceci est un exemple de la manière dont vous pouvez configurer Patroni pour appliquer un modèle de configuration si ce nœud Patroni est promu en primaire :

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> `patroni_barman config-switch` nécessite que Barman et `pg-backup-api` soient configurés sur l'hôte Barman, afin de pouvoir exécuter un `barman config-switch` distant via l'API de sauvegarde. Il requiert également que des modèles Barman préconfigurés soient appliqués. L'exemple ci-dessus utilise un sous-ensemble des paramètres disponibles. Vous pouvez obtenir davantage d'informations en exécutant `patroni_barman config-switch --help` et en consultant la documentation de Barman.
