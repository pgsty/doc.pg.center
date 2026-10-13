---
title: Modules Go
weight: 1650
description: Organisation des modules Go du projet etcd
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/modules.md"
aliases: [/etcd/dev-internal/modules/]
---

Le projet etcd (à partir de la version 3.5) est organisé en plusieurs modules [golang](https://golang.org/ref/mod) hébergés dans un [dépôt unique](https://golang.org/ref/mod#vcs-dir).

![modules graph](/docs/etcd/dev-internal/img/modules.svg)

Les modules suivants sont disponibles :

  - **go.etcd.io/etcd/api/v3** - contient les définitions d'API
      (protos et bibliothèques générées à partir de protos) qui définissent le protocole de communication
      entre les clients et le serveur etcd.

  - **go.etcd.io/etcd/pkg/v3** - ensemble de packages d'utilitaires utilisés par etcd
      sans être spécifiques à etcd lui-même. Un package doit être placé ici uniquement s'il pourrait éventuellement être déplacé vers son propre dépôt à l'avenir.
      Évitez d'ajouter ici du code qui a de nombreuses dépendances, car celles-ci deviendraient automatiquement des dépendances de la bibliothèque cliente
      (que nous souhaitons garder légère).

  - **go.etcd.io/etcd/client/v3** - bibliothèque cliente utilisée pour contacter etcd sur le réseau (grpc). Recommandée pour toute utilisation nouvelle d'etcd.

  - **go.etcd.io/etcd/client/v2** - bibliothèque cliente héritée utilisée pour contacter etcd via le protocole HTTP. Dépréciée. Tout usage nouveau devrait dépendre de la bibliothèque /v3.

  - **go.etcd.io/etcd/raft/v3** - implémentation du protocole de consensus distribué.
      Ne devrait pas contenir de code spécifique à etcd.

  - **go.etcd.io/etcd/server/v3** - implémentation etcd.
      Le code de ce package est interne à etcd et ne devrait pas être utilisé par des projets externes. La structure du package et l'API peuvent évoluer au sein des versions mineures.

  - **go.etcd.io/etcd/etcdctl/v3** - un outil en ligne de commande permettant d'accéder à etcd et de le gérer.

  - **go.etcd.io/etcd/tests/v3** - un module qui contient tous les tests d'intégration d'etcd.
    Remarque : Tous les tests unitaires (rapides et n'exigeant pas de dépendances entre modules)
    devraient être conservés dans les modules locaux au code testé.

  - **go.etcd.io/bbolt** - implémentation d'un arbre B persistant.
      Hébergé dans un dépôt séparé : https://github.com/etcd-io/bbolt.


### Opérations {#operations}

1. Tous les modules etcd devraient être publiés en versions identiques, par exemple :
   `go.etcd.io/etcd/client/v3@v3.5.10` doit dépendre de `go.etcd.io/etcd/api/v3@v3.5.10`.

   La mise à jour cohérente des versions peut être effectuée à l’aide de :
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. Les modules publiés devraient être étiquetés conformément aux règles https://golang.org/ref/mod#vcs-version,
   c’est-à-dire que chaque module devrait recevoir sa propre étiquette.
   La mise en étiquette peut être effectuée à l’aide de :
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. Tous les modules etcd devraient dépendre des mêmes versions des dépendances sous-jacentes.
    Cela peut être vérifié à l'aide de :
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. Les fichiers go.mod ne doivent pas contenir de dépendances non utilisées et doivent respecter le format `go mod tidy`.
    Cette vérification est effectuée par :
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. Pour déclencher des actions sur tous les modules (par exemple, formater automatiquement tous les fichiers), veuillez
   utiliser/étendre le script suivant :
   ```shell script
   % ./scripts/fix.sh
   ```

### Avenir {#future}

À terme, nous souhaitons faire évoluer les modules etcd vers le modèle suivant :

![modules graph](/docs/etcd/dev-internal/img/modules-future.svg)

Cela suppose :
  - Séparation d'etcdmigrate/etcdadm à partir du binaire etcdctl.
    Grâce à cela, etcdctl deviendrait clairement un wrapper en ligne de commande autour de l'API client réseau,
    tandis que etcdmigrate/etcdadm prendrait en charge les opérations physiques directes sur les fichiers de stockage etcd.
  - Séparation d'etcd-proxy à partir du binaire ./etcd, car il contient du code plus expérimental
    et donc des risques et des dépendances supplémentaires.
  - Dépréciation du support du protocole v2.
