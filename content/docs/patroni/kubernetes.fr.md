---
title: "Utilisation de Patroni avec Kubernetes"
linkTitle: "Utiliser avec Kubernetes"
weight: 120
icon: fas fa-dharmachakra
description: "Utilisation de Patroni avec les objets, étiquettes et la découverte de service Kubernetes."
module: [PATRONI]
categories: [Tâche]
aliases: [/patroni/kubernetes/]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
Patroni peut utiliser des objets Kubernetes afin de stocker l’état du cluster et gérer la clé du leader. Cela lui permet de fonctionner avec PostgreSQL dans un environnement Kubernetes sans nécessiter de magasin de cohérence, c’est-à-dire qu’il n’est pas nécessaire de déployer un Étcd supplémentaire. Patroni peut utiliser deux types d’objets Kubernetes pour stocker la clé du leader et les clés de configuration, configurés via les variables d’environnement `kubernetes.use_endpoints` ou `PATRONI_KUBERNETES_USE_ENDPOINTS`.

--------

## Utiliser les points de terminaison {#use-endpoints}

Bien que ce soit le mode recommandé, il est désactivé par défaut pour des raisons de compatibilité. Lorsqu’il est activé, Patroni stocke la configuration du cluster et la clé du leader dans les champs `metadata: annotations` du `Endpoints` correspondant qu’il crée. Le changement de leader est plus sûr qu’avec `ConfigMaps`, car les annotations contenant les informations sur le leader ainsi que les adresses réelles pointant vers le pod leader en cours d’exécution sont mises à jour simultanément en une seule opération.

--------

## Utiliser les ConfigMaps {#use-configmaps}

En ce mode, Patroni crée des ConfigMaps au lieu des Endpoints et stocke les clés dans les métadonnées de ces ConfigMaps. Le changement de leader nécessite au moins deux mises à jour : une pour le ConfigMap du leader, et une autre pour l'Endpoint correspondant.

Pour rediriger le trafic vers le leader PostgreSQL, vous devez configurer le service Kubernetes PostgreSQL afin d'utiliser un sélecteur d'étiquettes avec `role_label` (configuré dans la configuration Patroni).

Notez qu’il existe, dans certains cas — par exemple lors de l’exécution sur OpenShift — aucune alternative à l’utilisation des ConfigMaps.

--------

## Configuration {#configuration}

Les paramètres Patroni Kubernetes [settings](/fr/docs/patroni/config/yaml#kubernetes_settings) et les variables d'environnement [environment variables](/fr/docs/patroni/config/env#kubernetes_environment) sont décrits dans les chapitres généraux de la documentation.

<a id="kubernetes_role_values"></a>

### Personnaliser l'étiquette de rôle {#customize-role-label}

Par défaut, Patroni affecte des étiquettes correspondantes au pod dans lequel il s'exécute, en fonction du rôle du nœud, telles que `role=primary`. La clé et la valeur de l'étiquette peuvent être personnalisées à l'aide de `kubernetes.role_label`, `kubernetes.leader_label_value`, `kubernetes.follower_label_value` et `kubernetes.standby_leader_label_value`.

Remarque : si vous migrez des étiquettes de rôle par défaut vers des étiquettes personnalisées, vous pouvez réduire la durée d'indisponibilité en suivant les étapes de migration :

1.  Ajoutez une étiquette temporaire en utilisant la valeur d'origine du rôle pour le pod avec `kubernetes.tmp_role_label` (comme `tmp_role`). Une fois les pods redémarrés, les étiquettes suivantes seront définies par Patroni :

> ```yaml
> étiquettes :
>   nom-cluster : foo
>   rôle : primaire
>   rôle_temporaire : primaire
> ```

2.  Une fois tous les pods mis à jour, modifiez le sélecteur de service pour qu'il sélectionne l'étiquette temporaire.

> ```yaml
> sélecteur :
>   nom-cluster : foo
>   rôle-temporaire : primaire
> ```

3.  Ajoutez votre étiquette de rôle personnalisée (par exemple, définissez `kubernetes.leader_label_value=primary`). Une fois les pods redémarrés, ils recevront les nouvelles étiquettes suivantes définies par Patroni :

> ```yaml
> étiquettes :
>   nom-cluster : foo
>   rôle : primaire
>   rôle_temporaire : primaire
> ```

4.  Une fois que tous les pods ont été mis à jour, modifiez le sélecteur de service pour utiliser la nouvelle valeur de rôle.

> ```yaml
> sélecteur :
>   nom-cluster : foo
>   rôle : primaire
> ```

5.  Enfin, supprimez l'étiquette temporaire de votre configuration et mettez à jour tous les pods.

> ```yaml
> étiquettes:
>   nom-cluster : foo
>   rôle : primaire
> ```

--------

## Exemples {#examples}

- Le dossier [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) du dépôt Patroni contient des exemples d'image Docker et du manifeste Kubernetes permettant de tester la configuration Patroni sous Kubernetes. Notez qu'en l'état actuel, il ne sera pas possible d'utiliser des PersistentVolumes en raison de problèmes de permissions.
- Vous trouverez l'image Docker complète, capable d'utiliser des PersistentVolumes, dans le projet [Spilo](https://github.com/zalando/spilo).
- Il existe également un [Helm chart](https://github.com/kubernetes/charts/tree/master/incubator/patroni) permettant de déployer l'image Spilo configurée avec Patroni en exécution sous Kubernetes.
- Pour exécuter vos clusters de bases de données à grande échelle avec Patroni et Spilo, consultez le projet [postgres-operator](https://github.com/zalando/postgres-operator). Il implémente le modèle d'opérateur pour gérer les clusters Spilo.
