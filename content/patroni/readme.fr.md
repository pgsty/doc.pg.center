---
title: "Introduction"
weight: 10
icon: fa-solid fa-circle-info
description: "Introduction à Patroni, démarrage rapide et concepts fondamentaux de haute disponibilité."
module: [PATRONI]
categories: [Concept]
aliases: [/docs/patroni/readme/]
upstream_link: "https://patroni.readthedocs.io/en/latest/README.html"
---

<a id="readme"></a>
Patroni est un modèle de solutions PostgreSQL à haute disponibilité (HA) basé sur Python. Patroni a été initialement développé à partir d'une branche de [Governor](https://github.com/compose/governor), le projet de Compose. Il intègre de nombreuses fonctionnalités nouvelles.

Pour plus d'informations de contexte, voir :

- [Haute disponibilité PostgreSQL avec Kubernetes et Patroni](https://www.youtube.com/watch?v=iruaCgeG7qs), conférence de Josh Berkus à KubeCon 2016 (vidéo)
- [Article du blog technique Zalando, février 2016](https://engineering.zalando.com/posts/2016/02/zalandos-patroni-a-template-for-high-availability-postgresql.html)

--------

## Statut de développement {#development-status}

Patroni est en développement actif et accepte les contributions. Consultez notre section [Contributing](/fr/patroni/contributing_guidelines#contributing_guidelines) ci-dessous pour plus de détails.

Nous signalons les informations sur les nouvelles versions [ici](/fr/patroni/releases#releases).

--------

## Exigences techniques/Installation {#technical-requirementsinstallation}

Aller à [here](/fr/patroni/installation#installation) pour obtenir des instructions sur l'installation et la mise à jour de Patroni sur diverses plates-formes.

<a id="running_configuring"></a>

--------

## Planification du nombre de nœuds PostgreSQL {#planning-the-number-of-postgresql-nodes}

Les nœuds Patroni/PostgreSQL sont déconnectés des nœuds DCS (sauf lorsque Patroni implémente lui-même RAFT) et il n'existe donc aucune exigence concernant le nombre minimal de nœuds. Exécuter un cluster composé d'un nœud primaire et d'un nœud en veille est tout à fait acceptable. Vous pouvez ajouter davantage de nœuds en veille ultérieurement.

**Clusters à 2 nœuds** (primaire + secondaire) sont courants et offrent un basculement automatique avec une haute disponibilité. Notez qu’en cas de basculement, vous aurez temporairement une absence de redondance jusqu’à ce que le nœud défaillant se reconnecte.

**Exigences du DCS** : Votre DCS (etcd, ZooKeeper, Consul) doit fonctionner avec **3 ou 5 nœuds** pour assurer un consensus correct et une tolérance aux pannes. Un seul cluster DCS peut stocker des informations pour des centaines ou des milliers de clusters Patroni en utilisant différentes combinaisons d'espace de noms (namespace) ou de portée (scope).

--------

## Exécution et configuration {#running-and-configuring}

La section suivante suppose que le dépôt Patroni a été cloné à partir de <https://github.com/patroni/patroni>. Vous aurez besoin des fichiers de configuration exemple `postgres0.yml` et `postgres1.yml`. Si vous avez installé Patroni avec pip, vous pouvez obtenir ces fichiers à partir du dépôt git et remplacer `./patroni.py` ci-dessous par la commande `patroni`.

Pour commencer, effectuez les opérations suivantes depuis des terminaux distincts :

    > etcd --data-dir=data/etcd --enable-v2=true
    > ./patroni.py postgres0.yml
    > ./patroni.py postgres1.yml

Vous verrez alors un cluster à haute disponibilité démarrer. Testez différents paramètres dans les fichiers YAML pour observer les changements de comportement du cluster. Mettez hors service certains composants pour observer le comportement du système.

Ajoutez davantage de fichiers `postgres*.yml` pour créer un cluster encore plus grand.

Patroni fournit une configuration [HAProxy](https://www.haproxy.org/), qui permet à votre application de se connecter au leader du cluster via un seul point d'accès. Pour la configurer, exécutez :

    > haproxy -f haproxy.cfg

    > psql --host 127.0.0.1 --port 5000 postgres

--------

## Configuration YAML {#yaml-configuration}

Aller à [here](/fr/patroni/config/yaml#yaml) pour obtenir des informations complètes sur les paramètres d'etcd, consul et ZooKeeper. Pour un exemple, voir [postgres0.yml](https://github.com/patroni/patroni/blob/master/postgres0.yml).

--------

## Configuration de l'environnement {#environment-configuration}

Accédez à [ici](/fr/patroni/config/env#env) pour obtenir des informations complètes sur la configuration (remplacement) des paramètres via des variables d'environnement.

--------

## Options de réplication {#replication-choices}

Patroni utilise la réplication en streaming de Postgres, qui est asynchrone par défaut. La configuration de réplication asynchrone de Patroni permet de définir les paramètres `maximum_lag_on_failover`. Ce paramètre garantit qu’un basculement ne se produira pas si un suiveur est retardé de plus d’un certain nombre d’octets par rapport au leader. Ce paramètre doit être ajusté en fonction des besoins métiers. Il est également possible d’utiliser la réplication synchrone pour des garanties de durabilité renforcées. Voir la documentation sur les modes de réplication [ pour plus de détails](/fr/patroni/replication_modes#replication_modes).

--------

## Les applications ne doivent pas utiliser de superutilisateurs {#applications-should-not-use-superusers}

Lors de la connexion depuis une application, utilisez toujours un utilisateur non superutilisateur. Patroni nécessite un accès à la base de données pour fonctionner correctement. En utilisant un superutilisateur depuis une application, vous risquez d'utiliser l'intégralité du pool de connexions, y compris les connexions réservées aux superutilisateurs, avec le paramètre `superuser_reserved_connections`. Si Patroni ne parvient pas à accéder au primaire car le pool de connexions est plein, le comportement sera indésirable.

--------

## Test de votre solution haute disponibilité {#testing-your-ha-solution}

Tester une solution haute disponibilité est une opération longue, soumise à de nombreux facteurs. Cela est particulièrement vrai lorsqu’il s’agit d’une application multiplateforme. Un administrateur système expérimenté ou un consultant est nécessaire pour mener à bien cette tâche. Ce point ne peut pas être traité en profondeur dans la documentation.

En revanche, voici quelques composants de votre infrastructure que vous devez impérativement tester :

- Réseau (le réseau devant votre système ainsi que les cartes réseau \[physiques ou virtuelles\] elles-mêmes)
- E/S disque
- Limites de fichiers (nofile sous Linux)
- Mémoire RAM. Même si l'oomkiller est désactivé, l'indisponibilité de la mémoire RAM peut entraîner des problèmes.
- Processeur
- Contestation de virtualisation (surallocation du système hôte)
- Toute limitation cgroup (probablement liée à ce qui précède)
- `kill -9` de tout processus postgres (à l'exception du postmaster !). Ceci constitue une simulation raisonnable d'un plantage.

Une chose que vous ne devez pas faire est d'exécuter `kill -9` sur un processus postmaster. Cela s'explique par le fait que cela ne reproduit aucun scénario réel. Si vous craignez que votre infrastructure soit compromise et qu'un attaquant puisse exécuter `kill -9`, aucune configuration de haute disponibilité ne pourra résoudre ce problème. L'attaquant supprimera simplement le processus à nouveau, ou provoquera d'autres perturbations.
