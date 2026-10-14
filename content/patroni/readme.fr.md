---
title: "Introduction"
weight: 10
icon: fa-solid fa-circle-info
description: "Introduction à Patroni, démarrage rapide et concepts fondamentaux de haute disponibilité."
module: [PATRONI]
categories: [Concept]
upstream_link: "https://patroni.readthedocs.io/en/latest/README.html"
---

<a id="readme"></a>
Patroni est un modèle de solutions PostgreSQL à haute disponibilité (HA) basé sur Python. Patroni est à l'origine un fork de [Governor](https://github.com/compose/governor), le projet de Compose. Il intègre de nombreuses fonctionnalités nouvelles.

Pour plus d'informations de contexte, voir :

- [Haute disponibilité PostgreSQL avec Kubernetes et Patroni](https://www.youtube.com/watch?v=iruaCgeG7qs), conférence de Josh Berkus à KubeCon 2016 (vidéo)
- [Article du blog technique Zalando, février 2016](https://engineering.zalando.com/posts/2016/02/zalandos-patroni-a-template-for-high-availability-postgresql.html)

--------

## Statut de développement {#development-status}

Patroni est en développement actif et accepte les contributions. Consultez notre section [contribution](/fr/patroni/contributing_guidelines#contributing_guidelines) ci-dessous pour plus de détails.

Nous signalons les informations sur les nouvelles versions [ici](/fr/patroni/releases#releases).

--------

## Exigences techniques/Installation {#technical-requirementsinstallation}

Consultez [cette page](/fr/patroni/installation#installation) pour obtenir des conseils sur l'installation et la mise à jour de Patroni sur diverses plates-formes.

<a id="running_configuring"></a>

--------

## Planification du nombre de nœuds PostgreSQL {#planning-the-number-of-postgresql-nodes}

Les nœuds Patroni/PostgreSQL sont découplés des nœuds DCS (sauf lorsque Patroni implémente lui-même Raft) et il n'existe donc aucune exigence concernant le nombre minimal de nœuds. Exécuter un cluster composé d'un nœud primaire et d'une réplique est tout à fait acceptable. Vous pouvez ajouter davantage de répliques ultérieurement.

**Clusters à 2 nœuds** (primaire + secondaire) sont courants et offrent un basculement automatique avec une haute disponibilité. Notez qu’en cas de basculement, vous aurez temporairement une absence de redondance jusqu’à ce que le nœud défaillant réintègre le cluster.

**Exigences du DCS** : Votre DCS (etcd, ZooKeeper, Consul) doit fonctionner avec **3 ou 5 nœuds** pour assurer un consensus correct et une tolérance aux pannes. Un seul cluster DCS peut stocker des informations pour des centaines ou des milliers de clusters Patroni en utilisant différentes combinaisons d'espace de noms (namespace) et de portée (scope).

--------

## Exécution et configuration {#running-and-configuring}

La section suivante suppose que le dépôt Patroni a été cloné à partir de <https://github.com/patroni/patroni>. Vous aurez besoin des fichiers de configuration exemple `postgres0.yml` et `postgres1.yml`. Si vous avez installé Patroni avec pip, vous pouvez obtenir ces fichiers à partir du dépôt git et remplacer `./patroni.py` ci-dessous par la commande `patroni`.

Les commandes ci-dessous utilisent l’API v2 d’etcd et nécessitent une version prenant en charge `--enable-v2`, telle qu’etcd 3.5. Avec etcd 3.6 ou une version ultérieure, utilisez plutôt la configuration `etcd3` de Patroni, car [etcd 3.6 a supprimé la prise en charge de l’API v2](https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/).

Pour commencer, effectuez les opérations suivantes depuis des terminaux distincts :

    > etcd --data-dir=data/etcd --enable-v2=true
    > ./patroni.py postgres0.yml
    > ./patroni.py postgres1.yml

Vous verrez alors un cluster à haute disponibilité démarrer. Testez différents paramètres dans les fichiers YAML pour observer les changements de comportement du cluster. Arrêtez certains composants pour observer le comportement du système.

Ajoutez davantage de fichiers `postgres*.yml` pour créer un cluster encore plus grand.

Patroni fournit une configuration [HAProxy](https://www.haproxy.org/), qui permet à votre application de se connecter au leader du cluster via un seul point d'accès. Pour la configurer, exécutez :

    > haproxy -f haproxy.cfg

    > psql --host 127.0.0.1 --port 5000 postgres

--------

## Configuration YAML {#yaml-configuration}

Consultez [cette page](/fr/patroni/config/yaml#yaml) pour obtenir des informations complètes sur les paramètres d'etcd, Consul et ZooKeeper. Pour un exemple, voir [postgres0.yml](https://github.com/patroni/patroni/blob/master/postgres0.yml).

--------

## Configuration de l'environnement {#environment-configuration}

Consultez [cette page](/fr/patroni/config/env#env) pour obtenir des informations complètes sur la configuration (surcharge) des paramètres via des variables d'environnement.

--------

## Options de réplication {#replication-choices}

Patroni utilise la réplication en streaming de Postgres, qui est asynchrone par défaut. La configuration de réplication asynchrone de Patroni permet de définir les paramètres `maximum_lag_on_failover`. Ce paramètre empêche la promotion d’un suiveur lors d’un basculement si son retard sur le leader dépasse le nombre d’octets configuré. Ce paramètre devrait être augmenté ou diminué en fonction des besoins métiers. Il est également possible d’utiliser la réplication synchrone pour des garanties de durabilité renforcées. Consultez la [documentation sur les modes de réplication](/fr/patroni/replication_modes#replication_modes) pour plus de détails.

--------

## Les applications ne doivent pas utiliser de superutilisateurs {#applications-should-not-use-superusers}

Lors de la connexion depuis une application, utilisez toujours un utilisateur non superutilisateur. Patroni nécessite un accès à la base de données pour fonctionner correctement. En utilisant un superutilisateur depuis une application, vous risquez d'utiliser l'intégralité du pool de connexions, y compris les connexions réservées aux superutilisateurs, avec le paramètre `superuser_reserved_connections`. Si Patroni ne parvient pas à accéder au primaire car le pool de connexions est plein, le comportement sera indésirable.

--------

## Test de votre solution haute disponibilité {#testing-your-ha-solution}

Tester une solution haute disponibilité est une opération longue, soumise à de nombreux facteurs. Cela est particulièrement vrai lorsqu’il s’agit d’une application multiplateforme. Un administrateur système expérimenté ou un consultant est nécessaire pour mener à bien cette tâche. Ce point ne peut pas être traité en profondeur dans la documentation.

Cela dit, voici quelques éléments de votre infrastructure que vous devriez absolument tester :

- Réseau (le réseau devant votre système ainsi que les cartes réseau \[physiques ou virtuelles\] elles-mêmes)
- E/S disque
- Limites de fichiers (nofile sous Linux)
- Mémoire RAM. Même si l'oomkiller est désactivé, l'indisponibilité de la mémoire RAM peut entraîner des problèmes.
- Processeur
- Contention des ressources de virtualisation (surallocation de l'hyperviseur)
- Toute limitation cgroup (probablement liée à ce qui précède)
- `kill -9` de tout processus postgres (à l'exception du postmaster !). Ceci constitue une simulation raisonnable d'une erreur de segmentation.

Une chose que vous ne devez pas faire est d'exécuter `kill -9` sur un processus postmaster. En effet, tuer le processus seul ne reproduit pas les conditions sous-jacentes d’un épuisement des ressources ou d’autres défaillances de l’infrastructure. Si vous craignez que votre infrastructure soit compromise et qu'un attaquant puisse exécuter `kill -9`, aucune configuration de haute disponibilité ne pourra résoudre ce problème. L'attaquant se contentera de tuer à nouveau le processus, ou de provoquer le chaos d'une autre manière.
