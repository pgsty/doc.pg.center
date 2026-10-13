---
title: Passerelle etcd
weight: 4300
description: "Quand utiliser la passerelle etcd et comment la configurer"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/gateway.md"
aliases: [/etcd/op-guide/gateway/]
---

## Qu'est-ce que la passerelle etcd {#what-is-etcd-gateway}

La passerelle etcd est un proxy TCP simple qui achemine les données réseau vers le cluster etcd. La passerelle est sans état et transparente ; elle n'inspecte pas les requêtes clients et n'interfère pas avec les réponses du cluster. Elle ne termine pas les connexions TLS, ne réalise pas d'échanges TLS à la place de ses clients, ni ne vérifie si la connexion est sécurisée.

La passerelle prend en charge plusieurs points d'accès serveur etcd et fonctionne selon une politique de rotation simple. Elle ne route que vers les points d'accès disponibles et masque les échecs à ses clients. D'autres politiques de réessai, telles que la rotation pondérée, pourraient être prises en charge à l'avenir.

## Quand utiliser la passerelle etcd {#when-to-use-etcd-gateway}

Chaque application qui accède à etcd doit d'abord connaître l'adresse d'un point de terminaison client du cluster etcd. Si plusieurs applications sur le même serveur accèdent au même cluster etcd, chaque application doit tout de même connaître les points de terminaison clients annoncés du cluster etcd. Si le cluster etcd est reconfiguré pour utiliser des points de terminaison différents, chaque application peut également devoir mettre à jour sa liste de points de terminaison. Cette reconfiguration à grande échelle est à la fois fastidieuse et sujette aux erreurs.

La passerelle etcd résout ce problème en agissant comme un point d’accès local stable. Une configuration typique de passerelle etcd fait en sorte que chaque machine exécute une passerelle écoutant sur une adresse locale, et que chaque application etcd se connecte à sa passerelle locale. Le résultat est que seule la passerelle doit mettre à jour ses points de terminaison, et non chaque application individuellement.

En résumé, pour propager automatiquement les modifications des points d'accès du cluster, la passerelle etcd s'exécute sur chaque machine hébergeant plusieurs applications qui accèdent au même cluster etcd.

## Quand ne pas utiliser la passerelle etcd {#when-not-to-use-etcd-gateway}

- Amélioration des performances

La passerelle n’est pas conçue pour améliorer les performances du cluster etcd. Elle ne propose ni mise en cache, ni regroupement des opérations de surveillance, ni traitement par lots. L’équipe etcd développe actuellement un proxy de mise en cache conçu pour améliorer l’évolutivité du cluster.

- Exécution sur un système de gestion de cluster

Les systèmes de gestion de cluster avancés comme Kubernetes prennent en charge nativement la découverte de services. Les applications peuvent accéder à un cluster etcd à l’aide d’un nom DNS ou d’une adresse IP virtuelle gérée par le système. Par exemple, kube-proxy est équivalent à une passerelle etcd.

## Démarrer la passerelle etcd {#start-etcd-gateway}

Considérez un cluster etcd avec les points de terminaison statiques suivants :

|Nom|Adresse|Nom d'hôte|Port|
|------|---------|------------------|----|
|infra0|10.0.1.10|infra0.example.com|2379|
|infra1|10.0.1.11|infra1.example.com|2379|
|infra2|10.0.1.12|infra2.example.com|2379|

Démarrez la passerelle etcd pour utiliser ces points de terminaison statiques avec la commande :

```bash
$ etcd gateway start --endpoints=infra0.example.com:2379,infra1.example.com:2379,infra2.example.com:2379
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

Alternativement, si vous utilisez le DNS pour la découverte de service, envisagez les entrées SRV DNS :

```bash
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```bash
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

Démarrez la passerelle etcd pour récupérer les points d'accès à partir des entrées DNS SRV avec la commande :

```bash
$ etcd gateway start --discovery-srv=example.com
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

## Drapeaux de configuration {#configuration-flags}

### etcd cluster {#etcd-cluster}

#### --endpoints {#endpoints}

 *  Liste séparée par des virgules des cibles serveur etcd vers lesquelles les connexions clients sont acheminées.
 *  Valeur par défaut : `127.0.0.1:2379`
 *  Le port doit être inclus.
 *  Exemple incorrect : `https://127.0.0.1:2379` (la passerelle ne termine pas le TLS). Notez que la passerelle ne vérifie pas le schéma HTTP ni n'inspecte les requêtes, elle ne fait que les acheminer vers les points de terminaison indiqués.

#### --discovery-srv {#discovery-srv}

 * Domaine DNS utilisé pour amorcer les points d'accès du cluster via des enregistrements SRV.
 * Par défaut : (non défini)

### Réseau {#network}

#### --listen-addr {#listen-addr}

 * Interface et port d'écoute pour accepter les requêtes clients.
 * Valeur par défaut : `127.0.0.1:23790`

#### --retry-delay {#retry-delay}

 * Durée du délai avant de réessayer la connexion aux points de terminaison défaillants.
 * Valeur par défaut : 1m0s
 * Exemple non valide : "123" (unité de temps attendue au format)

### Sécurité {#security}

#### --insecure-discovery {#insecure-discovery}

 * Accepter les enregistrements SRV qui sont non sécurisés ou susceptibles d’attaques d’homme-du-milieu.
 * Valeur par défaut : `false`

#### --trusted-ca-file {#trusted-ca-file}

 * Chemin vers le fichier CA TLS du client pour le cluster etcd, utilisé pour vérifier les points de terminaison retournés par la découverte SRV. Notez qu'il n'est utilisé QUE pour l'authentification des points de terminaison découverts, et non pour établir des connexions de transfert de données. La passerelle ne termine jamais de connexions TLS ni ne crée de connexions TLS en lieu et place de ses clients.
 * Par défaut : (non défini)
