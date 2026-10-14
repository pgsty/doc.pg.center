---
title: "Installation"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "Instructions d’installation et de mise à jour de Patroni sur les plates-formes prises en charge."
module: [PATRONI]
categories: [Tutoriel]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## Prérequis pour Mac OS {#pre-requirements-for-mac-os}

Pour installer les prérequis sur un Mac, exécutez la commande suivante :

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

À compter de [psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/), la version binaire de psycopg2 ne sera plus installée par défaut. Son installation à partir du code source nécessite un compilateur C ainsi que les paquets de développement postgres+python. Étant donné que l’écosystème Python ne permet pas de spécifier la dépendance comme `psycopg2 OR psycopg2-binary`, vous devrez déterminer vous-même la méthode d’installation.

Plusieurs options sont disponibles :

1.  Utilisez le gestionnaire de paquets de votre distribution

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2.  Spécifiez l’un des éléments `psycopg3`, `psycopg2` ou `psycopg2-binary` dans la [liste des dépendances](/fr/patroni/installation#extras) lors de l'installation de Patroni avec pip.

<a id="extras"></a>

--------

## Installation avec pip {#general-installation-for-pip}

Patroni peut être installé avec pip :

```bash
pip install patroni[dependencies]
```

où `dependencies` peut être vide ou composé d’un ou plusieurs des éléments suivants :

etcd ou etcd3  
module `python-etcd` afin d'utiliser etcd comme magasin de configuration distribué (DCS)

consul  
module `py-consul` afin d'utiliser Consul comme DCS

zookeeper  
module `kazoo` afin d'utiliser Zookeeper comme DCS

exhibitor  
module `kazoo` afin d'utiliser Exhibitor comme DCS (mêmes dépendances que pour Zookeeper)

kubernetes  
[kubernetes](/fr/patroni/kubernetes#kubernetes) module afin d'utiliser Kubernetes comme DCS dans Patroni

raft  
module `pysyncobj` afin d'utiliser l'implémentation Python de Raft comme DCS

aws  
`boto3` afin d'utiliser les rappels AWS

jsonlogger  
module `python-json-logger` afin d'activer la [journalisation](/fr/patroni/config/yaml#log_settings) au format JSON

systemd  
`systemd-python` afin d'utiliser l'intégration sd_notify

all  
tous les précédents (à l’exception de la famille psycopg)

psycopg3  
module `psycopg[binary]>=3.0.0`

psycopg2  
module `psycopg2>=2.5.4`

psycopg2-binary  
module `psycopg2-binary`

Par exemple, la commande permettant d’installer Patroni avec psycopg3, les dépendances pour etcd en tant que DCS, et les rappels AWS est :

```bash
pip install patroni[psycopg3,etcd3,aws]
```

Notez que les outils externes appelés lors de la création d'une réplique ou dans des scripts d'amorçage personnalisés (par exemple WAL-E) devraient être installés indépendamment de Patroni.

<a id="package_installation"></a>

--------

## Installation du paquet sous Linux {#package-installation-on-linux}

Les paquets Patroni peuvent être disponibles pour votre système d'exploitation, produits par la communauté Postgres pour :

- RHEL, RockyLinux, AlmaLinux ;
- Debian et Ubuntu ;
- SUSE Enterprise Linux.

Vous pouvez également trouver des paquets pour les dépendances directes de Patroni, telles que des modules Python qui pourraient ne pas être disponibles dans les dépôts officiels du système d'exploitation.

Pour plus d'informations, consultez la documentation du dépôt [PGDG](https://www.postgresql.org/download/linux/).

Si vous utilisez un système d'exploitation dérivé de RedHat Enterprise Linux, vous devrez peut-être également recourir à des paquets provenant d'EPEL ; consultez la documentation du [dépôt EPEL](https://docs.fedoraproject.org/en-US/epel/).

Une fois que vous avez installé le dépôt PGDG pour votre système d'exploitation, vous pouvez installer Patroni.

> [!NOTE]
> Les paquets Patroni ne sont pas maintenus par les développeurs Patroni, mais par la communauté Postgres. Si vous avez besoin d'assistance, essayez d'abord de vous connecter sur [Postgres slack](http://pgtreats.info/slack-invite).

### Installation sur les dérivés de Debian {#installing-on-debian-derivatives}

Avec le dépôt PGDG installé, consultez [ci-dessus](/fr/patroni/installation#package_installation), puis installez Patroni via apt en exécutant :

```bash
apt-get install patroni
```

### Installation sur les dérivés RedHat {#installing-on-redhat-derivatives}

Avec le dépôt PGDG installé, voir [ci-dessus](/fr/patroni/installation#package_installation), installez Patroni avec un DCS etcd via dnf sur RHEL 9 (et dérivés) en exécutant :

```bash
dnf install patroni patroni-etcd
```

Vous pouvez installer etcd à partir de PGDG si votre distribution dérivée de RedHat ne fournit pas de paquets. Sur les nœuds qui hébergeront le DCS, exécutez :

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

Vous pouvez remplacer la version de RHEL par `8` dans le dépôt afin de créer `pgdg-rhel8-extras` si nécessaire. Le nom du dépôt reste `pgdg-rhelN-extras` sur RockyLinux, AlmaLinux, Oracle Linux, etc...

### Installation sur SUSE Enterprise Linux {#installing-on-suse-enterprise-linux}

Vous devrez peut-être activer les référentiels SUSE PackageHub pour certaines dépendances. Voir la documentation de [SUSE PackageHub](https://packagehub.suse.com/how-to-use/).

Pour SLES 15, avec le dépôt PGDG installé (voir [ci-dessus](/fr/patroni/installation#package_installation)), vous pouvez installer Patroni avec :

```bash
zypper install patroni patroni-etcd
```

Avec le dépôt PackageHub SUSE activé, vous pouvez également installer etcd :

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## Mise à jour {#upgrading}

La mise à jour de Patroni est un processus très simple : mettez à jour l'installation logicielle, puis redémarrez le démon Patroni sur chaque nœud du cluster.

Toutefois, redémarrer le démon Patroni entraîne un redémarrage de la base de données PostgreSQL. Dans certaines situations, cela peut provoquer un basculement du nœud primaire de votre cluster ; il est donc recommandé de mettre le cluster en mode maintenance jusqu'à la fin du redémarrage du démon Patroni.

Pour placer le cluster en mode maintenance, exécutez la commande suivante sur l'un des nœuds Patroni :

```bash
patronictl pause --wait
```

Ensuite, sur chaque nœud du cluster, effectuez la mise à jour du paquet nécessaire pour votre système d'exploitation :

```bash
apt-get update && apt-get install patroni
```

Redémarrez le démon Patroni sur chaque nœud :

```bash
systemctl restart patroni
```

Enfin, reprenez la surveillance de Postgres avec Patroni afin de sortir le cluster du mode maintenance :

```bash
patronictl resume --wait
```

Le cluster sera désormais entièrement opérationnel avec la nouvelle version de Patroni.
