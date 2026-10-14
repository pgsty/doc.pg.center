---
title: Démarrage rapide
weight: 900
description: "Mettez etcd en marche en moins de 5 minutes !"
icon: fa-solid fa-rocket
categories: [Tutoriel]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
---

Suivez ces instructions pour installer, exécuter et tester localement un cluster à membre unique d'etcd :

 1. Installez etcd à partir de binaires précompilés ou du code source. Pour plus de détails, consultez [Installation][Install].

    > [!WARNING]
    > **Important** : Veillez à effectuer la dernière
    > étape des instructions d'installation afin de vérifier que `etcd` est dans votre chemin.

 2. Démarrer `etcd` :

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **Remarque** : La sortie produite par `etcd` correspond à des
    > [journaux](/fr/etcd/op-guide/configuration/#logging) &mdash; des journaux de niveau info peuvent
    > être ignorés.

 3. Depuis **un autre terminal**, utilisez `etcdctl` pour définir une clé :

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. Depuis le même terminal, récupérez la clé :

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## Que faire ensuite ? {#whats-next}

Découvrez d'autres méthodes de configuration et d'utilisation d'etcd dans les pages suivantes :

- Si vous êtes développeur :
  - Explorez l'[API][] gRPC.
  - Recherchez [des liaisons de langage et des outils][integrations].

- Si vous êtes opérateur ou administrateur :
  - Mettez en place un [cluster multi-machine][clustering].
  - Apprenez à [configurer][configure] etcd.
  - Utilisez TLS pour [sécuriser un cluster etcd][security].
  - [Optimisez etcd][tuning].

[api]: /fr/etcd/learning/api
[clustering]: /fr/etcd/op-guide/clustering
[configure]: /fr/etcd/op-guide/configuration
[integrations]: /fr/etcd/integrations
[security]: /fr/etcd/op-guide/security
[tuning]: /fr/etcd/tuning
[Install]: /fr/etcd/install/
