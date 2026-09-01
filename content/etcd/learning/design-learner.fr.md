---
title: etcd design membre apprenant
weight: 2375
description: Atténuation des défis courants liés à la reconfiguration du membership
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/design-learner.md"
---

etcd Membre apprenant
============

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


Contexte
==========

La reconfiguration du membership a été l’un des plus grands défis opérationnels. Examinons les défis courants.

### 1. Nouveau membre de cluster surcharge le leader {#1-new-cluster-member-overloads-leader}
Un membre etcd nouvellement joint démarre sans données, ce qui entraîne un plus grand nombre de mises à jour provenant du leader jusqu’à ce qu’il rattrape la log du leader. Le réseau du leader est alors plus susceptible d’être surchargé, bloquant ou perdant les battements de cœur envoyés aux suiveurs. Dans ce cas, un suiveur peut atteindre son délai d’élection et déclencher une nouvelle élection de leader. Ainsi, un cluster comportant un nouveau membre est plus vulnérable à une élection de leader. À la fois l’élection de leader et la propagation ultérieure des mises à jour vers le nouveau membre sont sujettes à provoquer des périodes d’indisponibilité du cluster (voir *Figure 1*).

![serveur-membre-apprenant-figure-01](/etcd/learning/img/server-learner-figure-01.png)

### 2. Scénarios de partition réseau {#2-network-partitions-scenarios}
Que se passe-t-il en cas de partition réseau ? Cela dépend de la partition du leader. Si le leader conserve toujours un quorum actif, le cluster continue de fonctionner (voir *Figure 2*).

![server-learner-figure-02](/etcd/learning/img/server-learner-figure-02.png)

#### 2.1 Isolement du leader {#21-leader-isolation}
Que se passe-t-il si le leader devient isolé du reste du cluster ? Le leader surveille l’évolution de chaque suiveur. Lorsque le leader perd la connectivité avec le quorum, il redevient suiveur, ce qui affecte la disponibilité du cluster (voir *Figure 3*).

![server-learner-figure-03](/etcd/learning/img/server-learner-figure-03.png)

Lorsqu’un nouveau nœud est ajouté à un cluster de 3 nœuds, la taille du cluster devient 4 et la taille du quorum devient 3. Que se passe-t-il si un nouveau nœud rejoint le cluster, puis qu’une partition réseau se produit ? Cela dépend de la partition dans laquelle se trouve le nouveau membre après la partition.

#### 2.2 Fractionnement du cluster 3+1 {#22-cluster-split-31}
Si le nouveau nœud se trouve accidentellement dans la même partition que le leader, ce dernier conserve toujours un quorum actif de 3. Aucune élection de leader n’a lieu, et la disponibilité du cluster n’est pas affectée (voir *Figure 4*).

![server-learner-figure-04](/etcd/learning/img/server-learner-figure-04.png)

#### 2.3 Fractionnement du cluster 2+2 {#23-cluster-split-22}
Si le cluster est partitionné en deux parties de deux, aucune des partitions ne conserve le quorum de 3. Dans ce cas, une élection de leader a lieu (voir *Figure 5*).

![server-learner-figure-05](/etcd/learning/img/server-learner-figure-05.png)

#### 2.4 Quorum perdu {#24-quorum-lost}
Que se passe-t-il si une partition réseau se produit en premier, puis qu’un nouveau membre est ajouté ? Un cluster à 3 nœuds déjà partitionné dispose déjà d’un suiveur déconnecté. Lorsqu’un nouveau membre est ajouté, le quorum passe de 2 à 3. Ce cluster dispose désormais de seulement 2 nœuds actifs sur 4, perd donc son quorum et déclenche une nouvelle élection de leader (voir *Figure 6*).

![serveur-membre-apprenant-figure-06](/etcd/learning/img/server-learner-figure-06.png)

Étant donné que l’opération d’ajout d’un membre peut modifier la taille du quorum, il est toujours recommandé de supprimer d’abord le membre pour remplacer un nœud défaillant.

Ajouter un nouveau membre à un cluster à 1 nœud modifie la taille du quorum à 2, provoquant immédiatement une élection du leader lorsque le leader précédent constate que le quorum n’est pas actif. Cela est dû au fait que l’opération « member add » est une procédure en deux étapes, où l’utilisateur doit d’abord appliquer la commande « member add », puis démarrer le processus du nouveau nœud (voir *Figure 7*).

![server-learner-figure-07](/etcd/learning/img/server-learner-figure-07.png)

### 3. Mauvaises configurations du cluster {#3-cluster-misconfigurations}
Un cas encore plus critique survient lorsque le membre ajouté est mal configuré. La reconfiguration du membre est un processus en deux étapes : « etcdctl member add » et le démarrage d’un processus serveur etcd avec l’URL de pair donnée. Autrement dit, la commande « member add » est appliquée indépendamment de l’URL, même lorsque la valeur de l’URL est invalide. Si la première étape est exécutée avec des URLs invalides, la deuxième étape ne peut même pas démarrer le nouvel etcd. Une fois que le cluster a perdu son quorum, il n’existe aucune possibilité de revenir en arrière sur le changement de configuration (voir *Figure 8*).

![serveur-membre-apprenant-figure-08](/etcd/learning/img/server-learner-figure-08.png)

La même règle s'applique à un cluster à plusieurs nœuds. Par exemple, si deux membres du cluster sont hors ligne (l'un est défaillant, l'autre mal configuré) et deux membres sont opérationnels, il faut désormais au moins 3 votes pour modifier la composition du cluster (voir *Figure 9*).

![server-learner-figure-09](/etcd/learning/img/server-learner-figure-09.png)

Comme indiqué ci-dessus, une simple mauvaise configuration peut faire basculer l’ensemble du cluster dans un état inopératoire. Dans un tel cas, un opérateur doit recréer manuellement le cluster en utilisant le drapeau `etcd --force-new-cluster`. Étant donné qu’etcd est devenu un service critique pour Kubernetes, toute interruption, aussi brève soit-elle, peut avoir un impact significatif sur les utilisateurs. Que pouvons-nous faire de mieux pour simplifier ces opérations ? Entre autres, l’élection du leader est essentielle à la disponibilité du cluster : pouvons-nous rendre la reconfiguration de la composition du cluster moins disruptive en ne modifiant pas la taille du quorum ? Un nouveau membre peut-il rester inactif, ne demandant au leader que les mises à jour minimales, jusqu’à ce qu’il soit à jour ? La mauvaise configuration de la composition du cluster peut-elle toujours être annulée et gérée de manière plus sécurisée (une commande d’ajout de membre erronée ne devrait jamais faire échouer le cluster) ? Un utilisateur doit-il s’inquiéter de la topologie réseau lors de l’ajout d’un nouveau membre ? L’API d’ajout de membre peut-elle fonctionner indépendamment de l’emplacement des nœuds et des partitions réseau en cours ?

Membre apprenant Raft
============

Afin de réduire les lacunes de disponibilité décrites dans la section précédente, [Raft §4.2.1](https://github.com/ongardie/dissertation/blob/master/stanford.pdf) introduit un nouvel état de nœud appelé « membre apprenant », qui rejoint le cluster en tant que **membre non votant** jusqu’à ce qu’il ait rattrapé les journaux du leader.

Fonctionnalités de la version 3.4
----------------

Un opérateur doit effectuer le minimum de travail possible pour ajouter un nouveau membre apprenant. Utilisez la commande `member add --learner` pour ajouter un nouveau membre apprenant, qui rejoint le cluster en tant que membre non votant tout en recevant toutes les données du leader (voir *Figure 10*).

![server-learner-figure-10](/etcd/learning/img/server-learner-figure-10.png)

Lorsqu’un membre apprenant a rattrapé l’avancement du leader, il peut être promu en membre votant à l’aide de l’API `member promote`, qui contribue alors au quorum (voir *Figure 11*).

![serveur-membre-apprenant-figure-11](/etcd/learning/img/server-learner-figure-11.png)

Le serveur etcd valide la demande de promotion afin d'assurer sa sécurité opérationnelle. Un membre apprenant ne peut être promu en membre votant qu'après avoir rattrapé le journal du leader (voir *Figure 12*).

![server-learner-figure-12](/etcd/learning/img/server-learner-figure-12.png)

Le membre apprenant ne sert quasiment qu'à titre de nœud de secours jusqu'à sa promotion : la direction ne peut pas être transférée vers un membre apprenant. Le membre apprenant rejette les lectures et écritures clients (le chargeur de requêtes client ne doit pas acheminer les requêtes vers un membre apprenant). Cela signifie qu’un membre apprenant n’a pas besoin d’émettre de requêtes d’index de lecture au leader. Cette limitation simplifie l’implémentation initiale du membre apprenant dans la version v3.4 (voir *Figure 13*).

![server-learner-figure-13](/etcd/learning/img/server-learner-figure-13.png)

En outre, etcd limite le nombre total de membres apprenants qu’un cluster peut avoir, afin d’éviter de surcharger le leader avec la réplication des journaux. Un membre apprenant ne se promeut jamais lui-même. Bien qu’etcd fournisse des informations sur l’état du membre apprenant et des vérifications de sécurité, l’opérateur du cluster doit prendre la décision finale quant à la promotion d’un membre apprenant ou non.

Fonctionnalités proposées pour les versions futures

*État apprenant uniquement et par défaut* : Définir l'état par défaut d'un nouveau membre sur apprenant améliore considérablement la sécurité de la reconfiguration du groupe de membres, car un membre apprenant ne modifie pas la taille du quorum. Une mauvaise configuration reste toujours réversible sans perdre le quorum.

*Promotion automatique des membres votants* : Dès qu’un membre apprenant a rattrapé les journaux du leader, le cluster peut promouvoir automatiquement ce membre apprenant. etcd impose que l’utilisateur définisse certains seuils, et dès que ces conditions sont remplies, le membre apprenant se promeut lui-même en membre votant. Du point de vue de l’utilisateur, la commande « member add » fonctionnera de la même manière qu’aujourd’hui, mais avec une sécurité renforcée par la fonctionnalité de membre apprenant.

*Passer un membre apprenant en nœud de basculement de secours* : un membre apprenant rejoint en tant que nœud de secours et est automatiquement promu lorsque la disponibilité du cluster est compromise.

*Rendre le membre apprenant en lecture seule* : un membre apprenant peut servir de nœud en lecture seule qui ne sera jamais promu. En mode de cohérence faible, le membre apprenant reçoit uniquement des données du leader et ne traite jamais d'écritures. Servir les lectures localement, sans surcharge de consensus, réduit considérablement la charge imposée au leader, mais peut entraîner la lecture de données périmées. En mode de cohérence forte, le membre apprenant demande l'index de lecture au leader afin de servir les données les plus récentes, mais continue de rejeter les écritures.

Membre apprenant vs. Fabricant de miroir

etcd implémente une fonctionnalité de « mirror maker » à l’aide de l’API de surveillance pour relayer continuellement les créations et mises à jour de clés vers un cluster distinct. La mise en miroir présente généralement une surcharge de latence faible une fois la synchronisation initiale terminée. Les membres apprenants et la mise en miroir se recouvrent en ce sens qu’ils peuvent tous deux être utilisés pour répliquer des données existantes en lecture seule. Toutefois, la mise en miroir ne garantit pas la linéarité. En cas de déconnexion réseau, des valeurs de clés antérieures peuvent avoir été supprimées, et les clients sont censés vérifier les réponses de surveillance pour s’assurer de l’ordre correct. Par conséquent, aucune garantie d’ordre n’est assurée dans un miroir. Utilisez la mise en miroir pour une latence minimale (par exemple, entre centres de données) au prix de la cohérence. Utilisez les membres apprenants pour conserver toutes les données historiques et leur ordre.

Annexe : Implémentation du membre apprenant dans la version 3.4
============================================================

*Exposer le type de nœud "Learner" à l'API "MemberAdd".*

Le client etcd ajoute un indicateur à l’API « MemberAdd » pour un nœud membre apprenant. Le gestionnaire du serveur etcd applique l’entrée de changement d’appartenance avec le type `pb.ConfChangeAddLearnerNode`. Dès que la commande a été appliquée, un serveur rejoint le cluster avec l’indicateur `etcd --initial-cluster-state=existing`. Ce nœud membre apprenant ne peut ni voter ni être compté dans le quorum.

Le serveur etcd ne doit pas transférer le leadership à un membre apprenant, car celui-ci peut encore être en retard et ne compte pas dans le quorum. Le serveur etcd limite le nombre de membres apprenants qu’un cluster peut avoir à un seul : plus il y a de membres apprenants, plus le leader doit propager de données. Les clients peuvent interagir avec un nœud membre apprenant, mais celui-ci rejette toutes les requêtes sauf les lectures sérialisables et l’API d’état du membre. Ceci vise à simplifier l’implémentation initiale. À l’avenir, un membre apprenant pourra être étendu en serveur en lecture seule qui miroir continuellement les données du cluster. Le chargeur de requêtes client doit fournir une fonction d’aide pour exclure l’endpoint d’un membre apprenant. Sinon, une requête envoyée à un membre apprenant peut échouer. L’appel client de synchronisation du membre doit tenir compte du type de nœud membre apprenant. Il en va de même pour l’appel de mise à jour des points d’accès clients.

Les réponses de `MemberList` et `MemberStatus` doivent indiquer quel nœud est le membre apprenant.

*Ajouter l'API "MemberPromote".*

En interne dans Raft, un deuxième appel `MemberAdd` au nœud membre apprenant le promeut en membre votant. Le leader suit l’avancement de chaque suiveur et membre apprenant. Si le membre apprenant n’a pas terminé son message d’instantané, rejeter la demande de promotion. Accepter la demande de promotion uniquement si et seulement si : le nœud membre apprenant est dans un état sain, et le membre apprenant est synchronisé avec le leader ou l’écart est inférieur au seuil (par exemple, le nombre d’entrées à répliquer vers le membre apprenant est inférieur à 1/10 du nombre d’entrées de l’instantané, ce qui signifie qu’il est peu probable que, même après la promotion, le leader doive envoyer un nouvel instantané au membre apprenant). Toute cette logique est codée en dur dans le paquet `etcdserver` et n’est pas configurable.

Référence
=========

- Problème GitHub original : [etcd#9161](https://github.com/etcd-io/etcd/issues/9161)
- Cas d'utilisation : [etcd#3715](https://github.com/etcd-io/etcd/issues/3715)
- Cas d'utilisation : [etcd#8888](https://github.com/etcd-io/etcd/issues/8888)
- Cas d'utilisation : [etcd#10114](https://github.com/etcd-io/etcd/issues/10114)
