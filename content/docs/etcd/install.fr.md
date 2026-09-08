---
title: Installer
weight: 1150
description: "Instructions d'installation d'etcd à partir de binaires pré-construits ou à partir du code source."
icon: fa-solid fa-download
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/install.md"
aliases: [/etcd/install/]
---

## Exigences {#requirements}

Avant d’installer etcd, consultez les pages suivantes :

- [Plateformes prises en charge][]
- [Recommandations matérielles][]

## Installer les binaires préconstruits {#install-pre-built-binaries}

La méthode la plus simple pour installer etcd consiste à utiliser des binaires pré-construits :

 1. Téléchargez le fichier archive compressé pour votre plateforme depuis [Releases][],
     en choisissant une version [v3.7.0][tagged-release] ou ultérieure.
 2. Décompressez le fichier archive. Cela crée un répertoire contenant les binaires.
 3. Ajoutez les binaires exécutables à votre chemin d'accès. Par exemple, renommez et/ou déplacez
     les binaires vers un répertoire de votre chemin d'accès (comme `/usr/local/bin`), ou ajoutez le
     répertoire créé à l'étape précédente à votre chemin d'accès.
 4. À partir d'un shell, vérifiez que `etcd` est dans votre chemin d'accès :

    ```sh
    $ etcd --version
    etcd Version: 3.7.0
    ...
    ```

## Générer à partir du code source {#build-from-source}

Si vous avez [Go version 1.21+][go], vous pouvez compiler etcd à partir de son code source en suivant ces étapes :

 1. [Téléchargez le dépôt etcd sous forme de fichier zip][download] et décompressez-le, ou clonez le dépôt à l'aide de la commande suivante.

    ```sh
    $ git clone -b v3.7.0 https://github.com/etcd-io/etcd.git
    ```
    Pour construire à partir de `main@HEAD`, omettre le drapeau `-b v3.7.0`.

 2. Changer de répertoire :

    ```sh
    $ cd etcd
    ```
 3. Exécutez le script de compilation :

    ```sh
    $ ./scripts/build.sh
    ```

    Les binaires se trouvent dans le répertoire `bin`.

 4. Ajoutez le chemin complet du répertoire `bin` à votre variable d'environnement PATH, par exemple :

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. Vérifiez que `etcd` est dans votre chemin :

    ```sh
    $ etcd --version
    ```

## Installation via les paquets du système {#installation-via-os-packages}
*Avertissement : les installations d'etcd via les gestionnaires de paquets du système d'exploitation peuvent fournir des versions obsolètes, car elles ne sont ni automatiquement maintenues ni officiellement prises en charge par le projet etcd. Utilisez donc les paquets du système avec précaution.*

Il existe plusieurs façons d'installer etcd sur différents systèmes d'exploitation, et voici quelques exemples de la manière dont cela peut être réalisé.

### macOS (Homebrew) {#macos-homebrew}

1. Mettre à jour Homebrew :
```sh
$ brew update
```

2. Installer etcd :
```sh
$ brew install etcd
```

3. Vérifier l'installation
```sh
$ etcd --version
```

## Linux {#linux}

Bien qu’il soit possible d’installer etcd via les dépôts officiels et les gestionnaires de paquets de nombreuses distributions Linux majeures, les versions publiées peuvent être fortement obsolètes. L’installation de cette manière est donc fortement déconseillée.

La méthode recommandée pour installer etcd sous Linux consiste soit à utiliser des binaires pré-construits [pré-construits](#install-pre-built-binaries), soit à utiliser Homebrew.

### Homebrew sous Linux {#homebrew-on-linux}

[Homebrew peut fonctionner sous Linux] et peut fournir des versions récentes des logiciels.

- Prérequis
  - Mettre à jour Homebrew :

    ```sh
    $ brew update
    ```

- Procédure
  - Installation à l'aide de `brew` :

    ```sh
    $ brew install etcd
    ```

- Résultat
  - Vérifiez l'installation en obtenant la version :

    ```sh
    $ etcd --version
    etcd Version: 3.7.0
    ...
    ```

## Docker {#docker}

etcd utilise [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) comme registre conteneur principal, et [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) comme secondaire.

Pour exécuter etcd à l’aide de Docker :

```sh
ETCD_VER=v3.7.0

rm -rf /tmp/etcd-data.tmp && mkdir -p /tmp/etcd-data.tmp && \
  docker rmi gcr.io/etcd-development/etcd:${ETCD_VER} || true && \
  docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
  --name etcd-gcr-${ETCD_VER} \
  gcr.io/etcd-development/etcd:${ETCD_VER} \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster s1=http://0.0.0.0:2380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --log-level info \
  --logger zap \
  --log-outputs stderr

docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcd --version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdutl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl endpoint health
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl put foo bar
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl get foo
```

## Installation dans le cadre de l'installation de Kubernetes {#installation-as-part-of-kubernetes-installation}

- [Exécuter etcd en tant que StatefulSet Kubernetes][]

## Vérification d'installation {#installation-check}

Pour une vérification de cohérence un peu plus poussée de votre installation, consultez
[Quickstart][].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.0.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /fr/docs/etcd/op-guide/hardware/
[Quickstart]: /fr/docs/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /fr/docs/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.0
[Supported platforms]: /fr/docs/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
