---
title: "Prise en charge Citus"
weight: 130
icon: fas fa-lemon
description: "Détails d'intégration Patroni pour les groupes coordinateur et worker Citus."
module: [PATRONI]
categories: [Concept]
aliases: [/patroni/citus/]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
Patroni permet de déployer très facilement des clusters [Multi-Node Citus](https://docs.citusdata.com/en/stable/installation/multi_node.html).

--------

## TL;DR {#tldr}

Il n’existe que quelques règles simples à suivre :

1.  [Extension Citus](https://github.com/citusdata/citus) pour PostgreSQL doit être disponible sur tous les nœuds. La version minimale prise en charge est 10.0, mais pour bénéficier pleinement des basculements planifiés transparents et des redémarrages des workers, nous recommandons d'utiliser au moins la version Citus 11.2.
2.  Le nom du cluster (`scope`) doit être identique sur tous les nœuds Citus !
3.  Les identifiants de superutilisateur doivent être identiques sur le nœud coordinateur et sur tous les nœuds workers, et `pg_hba.conf` doit autoriser l'accès en tant que superutilisateur entre tous les nœuds.
4.  [API REST](/fr/docs/patroni/config/yaml#restapi_settings) doit être accessible depuis les nœuds workers vers le coordinateur. Par exemple, les identifiants doivent être identiques, et si configurés, les certificats clients émis par les nœuds workers doivent être acceptés par le coordinateur.
5.  Ajoutez la section suivante au `patroni.yaml` :

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

Ensuite, il vous suffit de démarrer Patroni, qui s'occupera du reste :

0.   Patroni définira `bootstrap.dcs.synchronous_mode` sur [quorum](/fr/docs/patroni/replication_modes#quorum_mode) s'il n'est pas explicitement défini sur une autre valeur.
1.  [citus](/fr/docs/patroni/citus#citus) sera automatiquement ajouté à `shared_preload_libraries`.
2.  Si `max_prepared_transactions` n'est pas explicitement défini dans la configuration globale [dynamic](/fr/docs/patroni/config/dynamic#dynamic), Patroni le définira automatiquement sur `2*max_connections`.
3.  La valeur du GUC `citus.local_hostname` sera ajustée de `localhost` à la valeur utilisée par Patroni pour se connecter à l'instance locale PostgreSQL. Cette valeur peut parfois différer de `localhost` car PostgreSQL pourrait ne pas écouter sur ce port.
4.  Le `citus.database` sera automatiquement créé, suivi de `CREATE EXTENSION citus`.
5.  Les [identifiants](/fr/docs/patroni/config/yaml#postgresql_settings) actuels du superutilisateur seront ajoutés à la table `pg_dist_authinfo` pour permettre la communication entre les nœuds. N'oubliez pas de les mettre à jour si vous modifiez ensuite le nom d'utilisateur, le mot de passe, le certificat SSL ou la clé SSL du superutilisateur !
6.  Le nœud primaire du coordinateur découvrira automatiquement les nœuds primaires workers et les ajoutera à la table `pg_dist_node` au moyen de la fonction `citus_add_node()`.
7.  Patroni maintiendra également `pg_dist_node` lors des basculements automatiques ou planifiés des clusters coordinateur ou workers.

--------

## patronictl {#patronictl}

Les clusters coordinateur et workers sont des clusters PostgreSQL physiquement distincts, regroupés logiquement à l’aide de l’extension de base de données [Citus](https://github.com/citusdata/citus) pour PostgreSQL. Par conséquent, dans la plupart des cas, il n’est pas possible de les gérer comme une entité unique.

Cela entraîne deux différences majeures dans le comportement de [patronictl](/fr/docs/patroni/patronictl#patronictl) lorsque `patroni.yaml` contient la section [citus](/fr/docs/patroni/citus#citus) par rapport à l'usage habituel :

1.   Le `list` et le `topology` affichent par défaut tous les membres de la formation Citus (coordonnateurs et workers). La nouvelle colonne `Group` indique à quel groupe Citus ils appartiennent.
2.   Pour toutes les commandes [patronictl](/fr/docs/patroni/patronictl#patronictl), une nouvelle option est introduite, nommée `--group`. Pour certaines commandes, la valeur par défaut du groupe peut être extraite du `patroni.yaml`. Par exemple, [patronictl_pause](/fr/docs/patroni/patronictl#patronictl_pause) activera le mode maintenance par défaut pour le `group` défini dans la section [citus](/fr/docs/patroni/citus#citus), mais par exemple pour [patronictl_basculement_planifié](/fr/docs/patroni/patronictl#patronictl_switchover) ou [patronictl_remove](/fr/docs/patroni/patronictl#patronictl_remove) le groupe doit être spécifié explicitement.

Exemple de sortie de [patronictl list](/fr/docs/patroni/patronictl#patronictl_list) pour le cluster Citus :

postgres@coord1:~$ patronictl list demo
    + Cluster Citus : demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Groupe | Membre  | Hôte        | Rôle           | État    | TL | Réception LSN | Décalage | Relecture LSN | Décalage |
    +--------+---------+-------------+----------------+---------+----+---------------+----------+---------------+----------+
    |      0 | coord1  | 172.27.0.10 | Réplique       | en cours  |  1 |   0/41C0368   |    0     |   0/41C0368   |    0     |
    |      0 | coord2  | 172.27.0.6  | Standby Quorum | en cours  |  1 |   0/41C0368   |    0     |   0/41C0368   |    0     |
    |      0 | coord3  | 172.27.0.4  | Leader         | en cours  |  1 |               |          |               |          |
    |      1 | work1-1 | 172.27.0.8  | Standby Quorum | en cours  |  1 |   0/31D3198   |    0     |   0/31D3198   |    0     |
    |      1 | work1-2 | 172.27.0.2  | Leader         | en cours  |  1 |               |          |               |          |
    |      2 | work2-1 | 172.27.0.5  | Standby Quorum | en cours  |  1 |   0/31CDFC0   |    0     |   0/31CDFC0   |    0     |
    |      2 | work2-2 | 172.27.0.7  | Leader         | en cours  |  1 |               |          |               |          |
    +--------+---------+-------------+----------------+---------+----+---------------+----------+---------------+----------+

Si nous ajoutons l'option `--group`, la sortie sera modifiée comme suit :

postgres@coord1:~$ patronictl list demo --group 0
    + Cluster Citus : demo (groupe : 0, 7179854923829112860) -+-------------+-----+------------+-----+
    | Membre | Hôte        | Rôle           | État    | TL | LSN de réception | Retard | LSN de lecture | Retard |
    +--------+-------------+----------------+---------+----+------------------+--------+----------------+--------+
    | coord1 | 172.27.0.10 | Réplique       | en cours |  1 |   0/41C0368      |   0    |  0/41C0368     |   0    |
    | coord2 | 172.27.0.6  | Standby quorum | en cours |  1 |   0/41C0368      |   0    |  0/41C0368     |   0    |
    | coord3 | 172.27.0.4  | Leader         | en cours |  1 |                  |        |                |        |
    +--------+-------------+----------------+---------+----+------------------+--------+----------------+--------+

postgres@coord1:~$ patronictl list demo --group 1
    + Cluster Citus : demo (groupe : 1, 7179854923881963547) -+-------------+-----+------------+-----+
    | Membre  | Hôte       | Rôle           | État    | TL | Réception LSN | Décalage | Relecture LSN | Décalage |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work1-1 | 172.27.0.8 | Standby Quorum | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    | work1-2 | 172.27.0.2 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+

--------

## Basculement planifié worker Citus {#citus-worker-switchover}

Lorsqu’un basculement planifié est orchestré pour un nœud worker Citus, Citus permet de rendre ce basculement quasi transparent pour une application. Étant donné qu’une application se connecte au coordinateur, qui à son tour se connecte aux nœuds workers, il est possible avec Citus de [mettre en pause](/fr/docs/patroni/pause#pause) le trafic SQL sur le coordinateur pour les shards hébergés sur un nœud worker. Le basculement s’effectue alors tout en maintenant le trafic sur le coordinateur, puis reprend dès qu’un nouveau nœud worker primaire est prêt à accepter les requêtes en lecture-écriture.

Exemple de [patronictl_switchover](/fr/docs/patroni/patronictl#patronictl_switchover) sur le cluster worker :

postgres@coord1:~$ patronictl switchover demo
    + Cluster Citus : demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Groupe | Membre  | Hôte        | Rôle           | État    | TL | LSN de réception | Retard | LSN de relecture | Retard |
    +--------+---------+-------------+----------------+---------+----+------------------+-------+------------------+-------+
    |      0 | coord1  | 172.27.0.10 | Réplique       | en cours  |  1 |   0/41C0368      |   0   |  0/41C0368      |   0   |
    |      0 | coord2  | 172.27.0.6  | Standby quorum | en cours  |  1 |   0/41C0368      |   0   |  0/41C0368      |   0   |
    |      0 | coord3  | 172.27.0.4  | Primaire       | en cours  |  1 |                  |       |                |       |
    |      1 | work1-1 | 172.27.0.8  | Primaire       | en cours  |  1 |                  |       |                |       |
    |      1 | work1-2 | 172.27.0.2  | Standby quorum | en cours  |  1 |   0/31D3198      |   0   |  0/31D3198      |   0   |
    |      2 | work2-1 | 172.27.0.5  | Standby quorum | en cours  |  1 |   0/31CDFC0      |   0   |  0/31CDFC0      |   0   |
    |      2 | work2-2 | 172.27.0.7  | Primaire       | en cours  |  1 |                  |       |                |       |
    +--------+---------+-------------+----------------+---------+----+------------------+-------+------------------+-------+
    Groupe Citus : 2
    Primaire [work2-2] :
    Candidat ['work2-1'] [] :
    À quelle heure le basculement planifié doit-il avoir lieu (par exemple 2024-08-26T08:02)  [maintenant] :
    Topologie actuelle du cluster
    + Cluster Citus : demo (groupe : 2, 7179854924063375386) -+-------------+-----+------------+-----+
    | Membre  | Hôte       | Rôle           | État    | TL | Réception LSN | Délai | Relecture LSN | Délai |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work2-1 | 172.27.0.5 | Standby Quorum | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    | work2-2 | 172.27.0.7 | Primaire       | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    Êtes-vous sûr de vouloir effectuer un basculement planifié du cluster demo, en rétrogradant le primaire actuel work2-2 ? [o/N] : o
    2024-08-26 07:02:40.33003 Basculé avec succès vers "work2-1"
    + Cluster Citus : demo (groupe : 2, 7179854924063375386) --------+---------+------------+---------+
    | Membre  | Hôte       | Rôle    | État    | TL | Réception LSN |     Délai | Relecture LSN |     Délai |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+
    | work2-1 | 172.27.0.5 | Leader  | running |  1 |             |         |            |         |
    | work2-2 | 172.27.0.7 | Réplique | arrêté  |    |     inconnu   | inconnu |    inconnu   | inconnu |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+

postgres@coord1:~$ patronictl list demo
    + Cluster Citus : demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Groupe | Membre  | Hôte        | Rôle           | État    | TL | Réception LSN | Décalage | Relecture LSN | Décalage |
    +--------+---------+-------------+----------------+---------+----+---------------+----------+---------------+----------+
    |      0 | coord1  | 172.27.0.10 | Réplique       | en cours  |  1 |   0/41C0368   |    0     |   0/41C0368   |    0     |
    |      0 | coord2  | 172.27.0.6  | Standby Quorum | en cours  |  1 |   0/41C0368   |    0     |   0/41C0368   |    0     |
    |      0 | coord3  | 172.27.0.4  | Leader         | en cours  |  1 |               |          |               |          |
    |      1 | work1-1 | 172.27.0.8  | Leader         | en cours  |  1 |               |          |               |          |
    |      1 | work1-2 | 172.27.0.2  | Standby Quorum | en cours  |  1 |   0/31D3198   |    0     |   0/31D3198   |    0     |
    |      2 | work2-1 | 172.27.0.5  | Leader         | en cours  |  2 |               |          |               |          |
    |      2 | work2-2 | 172.27.0.7  | Standby Quorum | en cours  |  2 |   0/31CDFC0   |    0     |   0/31CDFC0   |    0     |
    +--------+---------+-------------+----------------+---------+----+---------------+----------+---------------+----------+

Et voici à quoi cela ressemble du côté du coordinateur :

    # The worker primary notifies the coordinator that it is going to execute "pg_ctl stop".
    2024-08-26 07:02:38,636 DEBUG: query(BEGIN, ())
    2024-08-26 07:02:38,636 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.7-demoted', 5432, 10000))
    # From this moment all application traffic on the coordinator to the worker group 2 is paused.

    # The old worker primary is assigned as a secondary.
    2024-08-26 07:02:40,084 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (7, '172.19.0.7', 5432, 10000))

    # The future worker primary notifies the coordinator that it acquired the leader lock in DCS and about to run "pg_ctl promote".
    2024-08-26 07:02:40,085 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.5', 5432, 10000))

    # The new worker primary just finished promote and notifies coordinator that it is ready to accept read-write traffic.
    2024-08-26 07:02:41,485 DEBUG: query(COMMIT, ())
    # From this moment the application traffic on the coordinator to the worker group 2 is unblocked.

--------

## Nœuds secondaires {#secondary-nodes}

À compter de Patroni v4.0.0, les nœuds secondaires Citus sans balise `noloadbalance` [tag](/fr/docs/patroni/config/yaml#tags_settings) sont également inscrits dans `pg_dist_node`. Toutefois, pour utiliser les nœuds secondaires aux requêtes en lecture seule, les applications doivent modifier la variable GUC [citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum).

--------

## Découverte du DCS {#peek-into-dcs}

Le cluster Citus (coordinateur et workers) est stocké dans le DCS sous la forme d'une flotte de clusters Patroni logiquement regroupés :

    /service/batman/              # scope=batman
    /service/batman/0/            # citus.group=0, coordinator
    /service/batman/0/initialize
    /service/batman/0/leader
    /service/batman/0/members/
    /service/batman/0/members/m1
    /service/batman/0/members/m2
    /service/batman/1/            # citus.group=1, worker
    /service/batman/1/initialize
    /service/batman/1/leader
    /service/batman/1/members/
    /service/batman/1/members/m3
    /service/batman/1/members/m4
    ...

Une telle approche a été retenue car, pour la plupart des SDC, il devient possible de récupérer l’intégralité du cluster Citus en une seule requête de lecture récursive. Seuls les nœuds coordinateurs Citus lisent l’arborescence entière, car ils doivent découvrir les nœuds workers. Les nœuds workers lisent uniquement le sous-arbre correspondant à leur propre groupe, et dans certains cas, celui du groupe coordinateur.

--------

## Citus sur Kubernetes {#citus-on-kubernetes}

Étant donné que Kubernetes ne prend pas en charge les structures hiérarchiques, nous avons dû inclure le groupe citus à tous les objets K8s créés par Patroni :

    batman-0-leader  # la carte de configuration du leader pour le coordinateur
    batman-0-config  # la carte de configuration contenant les clés initialize, config et history
    ...
    batman-1-leader  # la carte de configuration du leader pour le groupe de workers 1
    batman-1-config
    ...

Autrement dit, le modèle de nommage est : `${scope}-${citus.group}-${type}`.

Tous les objets Kubernetes sont découverts par Patroni à l’aide du sélecteur d’étiquettes [label selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors), les Pods exécutant Patroni&Citus ainsi que les Endpoints/ConfigMaps doivent donc posséder des étiquettes similaires, et Patroni doit être configuré pour les utiliser à l’aide des paramètres Kubernetes [settings](/fr/docs/patroni/config/yaml#kubernetes_settings) ou des variables d’environnement <kubernetes_environment>.

Quelques exemples de configuration Patroni utilisant les variables d'environnement des Pods :

1.   pour le cluster coordinateur

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "0"
    citus-type: coordinator
    cluster-name: citusdemo
  name: citusdemo-0-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "0"
```

2.   pour le cluster worker du groupe 2

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "2"
    citus-type: worker
    cluster-name: citusdemo
  name: citusdemo-2-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "2"
```

Comme vous l'avez peut-être remarqué, les deux exemples définissent le libellé `citus-group`. Celui-ci permet à Patroni d'identifier l'appartenance d'un objet à un groupe Citus donné. La variable d'environnement `PATRONI_CITUS_GROUP` porte la même valeur que ce libellé. Lorsque Patroni crée de nouveaux objets Kubernetes, ConfigMaps ou Endpoints, il leur ajoute automatiquement le libellé `citus-group: ${env.PATRONI_CITUS_GROUP}` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: citusdemo-0-leader  # Is generated as ${env.PATRONI_SCOPE}-${env.PATRONI_CITUS_GROUP}-leader
  labels:
    application: patroni    # Is set from the ${env.PATRONI_KUBERNETES_LABELS}
    cluster-name: citusdemo # Is automatically set from the ${env.PATRONI_SCOPE}
    citus-group: '0'        # Is automatically set from the ${env.PATRONI_CITUS_GROUP}
```

Vous trouverez un exemple complet de déploiement Patroni sur Kubernetes avec prise en charge de Citus dans le dossier [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) du dépôt Patroni.

Il existe deux fichiers importants pour vous :

1.  Dockerfile.citus
2.  citus_k8s.yaml

--------

## Mises à jour Citus et mises à jour majeures PostgreSQL {#citus-upgrades-and-postgresql-major-upgrades}

Tout d’abord, veuillez consulter la procédure de mise à jour de la version Citus dans la [documentation](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html). Une modification mineure est à noter dans le processus. Lors de l’exécution de la mise à jour, vous devez utiliser [patronictl_restart](/fr/docs/patroni/patronictl#patronictl_restart) au lieu de `systemctl restart` pour redémarrer PostgreSQL.

La mise à niveau majeure de PostgreSQL avec Citus est un peu plus complexe. Vous devrez combiner les techniques décrites dans la documentation Citus concernant les mises à niveau majeures et la documentation Patroni concernant `PostgreSQL major upgrade<major_upgrade>`. Veillez à garder à l'esprit qu'un cluster Citus est composé de nombreux clusters Patroni (coordinateurs et workers), qui doivent tous être mis à niveau de manière indépendante.
