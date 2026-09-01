---
title: "Contrôle d'accès basé sur les rôles"
weight: 4100
description: Guide d’authentification basique et de contrôle d’accès basé sur les rôles
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/authentication/rbac.md"
---

## Aperçu {#overview}

L’authentification a été ajoutée à etcd 2.1. L’API v3 d’etcd a légèrement modifié l’API et l’interface utilisateur de la fonctionnalité d’authentification afin de mieux s’adapter au nouveau modèle de données. Ce guide vise à aider les utilisateurs à configurer une authentification basique et un contrôle d’accès basé sur les rôles dans etcd v3.

## Utilisateurs et rôles spéciaux {#special-users-and-roles}

Il existe un utilisateur spécial, `root`, et un rôle spécial, `root`.

### Utilisateur `root` {#user-root}

L'utilisateur `root`, qui dispose d'un accès complet à etcd, doit être créé avant d'activer l'authentification. L'idée derrière l'utilisateur `root` est d'assurer des opérations administratives : gestion des rôles et des utilisateurs ordinaires. L'utilisateur `root` doit posséder le rôle `root` et est autorisé à modifier tout élément à l'intérieur d'etcd.

### Rôle `root` {#role-root}

Le rôle `root` peut être attribué à tout utilisateur, en plus de l'utilisateur racine. Un utilisateur disposant du rôle `root` dispose à la fois d'un accès en lecture-écriture global et des autorisations pour mettre à jour la configuration d'authentification du cluster. En outre, le rôle `root` accorde les privilèges nécessaires à la maintenance générale du cluster, notamment la modification de la composition du cluster, la défragmentation du magasin et la prise d'instantanés.

## Travail avec les utilisateurs {#working-with-users}

Le sous-commande `user` pour `etcdctl` gère toutes les opérations relatives aux comptes utilisateurs.

Une liste des utilisateurs peut être obtenue avec :

```
$ etcdctl user list
```

Créer un utilisateur est aussi simple que

```
$ etcdctl user add myusername
```

La création d’un nouvel utilisateur demande de saisir un nouveau mot de passe. Le mot de passe peut être fourni depuis l’entrée standard lorsque l’option `--interactive=false` est utilisée. `--new-user-password` peut également être utilisé pour fournir le mot de passe.

La création d’un utilisateur qui ne peut pas être authentifié avec un mot de passe est également possible, comme indiqué ci-dessous :

```
$ etcdctl user add myusername --no-password
```

Un tel utilisateur ne peut être authentifié que par [TLS Common Name](#using-tls-common-name).

> [!NOTE]
> etcd ne prend pas en charge l'authentification avec un mot de passe vide via `--user username:`. Par exemple, un utilisateur créé avec un mot de passe vide, tel que `etcdctl user add anonymous:''`, ne peut pas s'authentifier par des requêtes username/password et les requêtes telles que `etcdctl --user anonymous: get foo` échouent avec `user name is empty`.

Les rôles peuvent être attribués ou retirés à un utilisateur avec :

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

Les paramètres de l'utilisateur peuvent être inspectés à l'aide de :

```
$ etcdctl user get myusername
```

Et le mot de passe d’un utilisateur peut être modifié avec

```
$ etcdctl user passwd myusername
```

Changer le mot de passe provoquera une nouvelle demande de mot de passe. Le mot de passe peut être fourni depuis l'entrée standard lorsque l'option `--interactive=false` est utilisée.

Supprimez un compte avec :
```
$ etcdctl user delete myusername
```


## Travail avec les rôles {#working-with-roles}

Le sous-commande `role` pour `etcdctl` gère toutes les opérations relatives aux contrôles d'accès pour des rôles spécifiques, tels qu'ils ont été attribués à des utilisateurs individuels.

Lister les rôles avec :

```
$ etcdctl role list
```

Créez un nouveau rôle avec :

```
$ etcdctl role add myrolename
```

Un rôle n’a pas de mot de passe ; il définit simplement un nouvel ensemble de droits d’accès.

Les rôles ont accès à une clé unique ou à une plage de clés.

La plage peut être spécifiée sous la forme d'un intervalle [clé_de_depart, clé_de_fin) où la clé_de_depart doit être strictement inférieure à la clé_de_fin selon un ordre alphabétique.

L'accès peut être accordé en lecture, écriture ou les deux, comme dans les exemples suivants :

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

Pour voir ce qui est accordé, nous pouvons consulter le rôle à tout moment :

```
$ etcdctl role get myrolename
```

La révocation des autorisations s'effectue de la même manière logique :

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

Comme pour supprimer un rôle entièrement :

```
$ etcdctl role delete myrolename
```

## Activer l'authentification {#enabling-authentication}

Les étapes minimales pour activer l’authentification sont les suivantes. L’administrateur peut configurer les utilisateurs et les rôles avant ou après l’activation de l’authentification, selon son choix.

Assurez-vous que l'utilisateur racine est créé :

```
$ etcdctl user add root
Password of root:
```

Activer l'authentification :

```
$ etcdctl auth enable
```

Après cela, etcd fonctionne avec l'authentification activée. Pour la désactiver pour une raison quelconque, utilisez la commande inverse :

```
$ etcdctl --user root:rootpw auth disable
```

## Portée de sécurité de l'authentification {#security-scope-of-authentication}

Lorsque l'authentification est activée avec `etcdctl auth enable`, elle protège les opérations de l'API gRPC V3 (get, put, delete, surveillance, etc.).

Les points de terminaison HTTP `/metrics` et `/health` fonctionnent sur un gestionnaire distinct et **ne sont pas** protégés par l'authentification RBAC V3. Ce design permet à Prometheus et aux équilibreurs de charge de récupérer les métriques sans nécessiter d'authentification gRPC, tout en maintenant la protection des données clé-valeur.

Pour sécuriser ces points de visualisation :

- Activez le mTLS avec `--cert-file`, `--key-file` et `--client-cert-auth`
- Ou liez les métriques à une interface privée en utilisant `--listen-metrics-urls`
- Ou utilisez des règles de réseau policies/firewall pour restreindre l'accès

## Utilisation de `etcdctl` pour l'authentification {#using-etcdctl-to-authenticate}

`etcdctl` prend en charge un indicateur similaire à `curl` pour l'authentification.

```
$ etcdctl --user user:password get foo
```

Le mot de passe peut être fourni à partir d'une invite :

```
$ etcdctl --user user get foo
```

Le mot de passe peut également être fourni via une option de ligne de commande `--password` :

```
$ etcdctl --user user --password password get foo
```


Sinon, toutes les commandes `etcdctl` restent identiques. Les utilisateurs et rôles peuvent toujours être créés et modifiés, mais nécessitent une authentification par un utilisateur disposant du rôle root.

## Utilisation du nom commun TLS {#using-tls-common-name}
À compter de la version v3.2, si un serveur etcd est lancé avec l'option `--client-cert-auth=true`, le champ Common Name (CN) du certificat TLS du client sera utilisé comme utilisateur etcd. Dans ce cas, le nom commun sert à authentifier l'utilisateur, et le client n'a pas besoin de mot de passe. Notez que si les deux conditions suivantes sont remplies : 1. `--client-cert-auth=true` est fourni et le CN est fourni par le client, et 2. le nom d'utilisateur et le mot de passe sont fournis par le client, l'authentification basée sur le nom d'utilisateur et le mot de passe est prioritaire. Notez que cette fonctionnalité ne peut pas être utilisée avec gRPC-proxy ni avec gRPC-gateway. Cela est dû au fait que gRPC-proxy termine la connexion TLS provenant de son client, si bien que tous les clients partagent un certificat du proxy. gRPC-gateway utilise une connexion TLS interne pour transformer une requête HTTP en requête gRPC, ce qui entraîne la même limitation. Par conséquent, les clients ne peuvent pas transmettre correctement leur CN au serveur. gRPC-proxy provoquera une erreur et s'arrêtera si le certificat fourni a un CN non vide. gRPC-proxy renvoie une erreur indiquant que le client possède un CN non vide dans son certificat.

## Remarques sur la force du mot de passe {#notes-on-password-strength}
Les API `etcdctl` et etcd n'imposent aucune longueur de mot de passe particulière lors de la création d'un utilisateur ou de la mise à jour de son mot de passe. Il incombe à l'administrateur d'appliquer ces exigences. Pour réduire les risques liés aux mots de passe faibles, utilisez [l'authentification fondée sur le nom commun TLS](#using-tls-common-name) ainsi que des utilisateurs créés avec l'option `--no-password`.
