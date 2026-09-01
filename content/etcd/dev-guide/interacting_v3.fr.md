---
title: Interaction avec etcd
weight: 3250
description: "etcdctl : un outil en ligne de commande pour interagir avec le serveur etcd"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

Les utilisateurs interagissent généralement avec etcd en définissant ou en récupérant la valeur d'une clé. Cette section décrit comment effectuer ces opérations à l'aide d'etcdctl, un outil en ligne de commande pour interagir avec le serveur etcd. Les concepts décrits ici s'appliquent également aux API gRPC ou aux API des bibliothèques clientes.

La version de l'API utilisée par etcdctl pour communiquer avec etcd peut être définie à `2` ou `3` via la variable d'environnement `ETCDCTL_API`. Par défaut, etcdctl sur la branche master (3.4) utilise l'API v3, tandis que les versions antérieures (3.3 et antérieures) utilisent par défaut l'API v2.

Notez qu'une clé créée à l'aide de l'API v2 ne pourra pas être interrogée via l'API v3. Une requête v3 ```etcdctl get``` d'une clé v2 se terminera avec le code 0 et sans données de clé ; il s'agit du comportement attendu.


```bash
export ETCDCTL_API=3
```

## Rechercher les versions {#find-versions}

La version d'etcdctl et la version de l'API serveur peuvent être utiles pour identifier les commandes appropriées à utiliser pour effectuer diverses opérations sur etcd.

Voici la commande permettant de trouver les versions :

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## Écrire une clé {#write-a-key}

Les applications stockent des clés dans le cluster etcd en écrivant sur des clés. Chaque clé stockée est répliquée sur tous les membres du cluster etcd via le protocole Raft afin d'assurer la cohérence et la fiabilité.

Voici la commande permettant de définir la valeur de la clé `foo` à `bar` :

```bash
$ etcdctl put foo bar
OK
```

Un clé peut également être définie pour une durée déterminée en lui associant un bail.

Voici la commande permettant de définir la valeur de la clé `foo1` à `bar1` pendant 10 s.

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> L'identifiant de bail `1234abcd` dans la commande ci-dessus fait référence à l'identifiant retourné lors de la création du bail de 10 s. Cet identifiant peut ensuite être associé à une clé.

## Lire les clés {#read-keys}

Les applications peuvent lire les valeurs des clés d’un cluster etcd. Les requêtes peuvent lire une seule clé ou une plage de clés.

Supposons que le cluster etcd ait stocké les clés suivantes :

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

Voici la commande pour lire la valeur de la clé `foo` :

```bash
$ etcdctl get foo
foo
bar
```

Voici la commande pour lire la valeur de la clé `foo` au format hexadécimal :

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Voici la commande pour lire uniquement la valeur de la clé `foo` :

```bash
$ etcdctl get foo --print-value-only
bar
```

Voici la commande pour parcourir les clés allant de `foo` à `foo3` :

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` est exclu car la plage se situe dans l'intervalle demi-ouvert `[foo, foo3)`, en excluant `foo3`.

Voici la commande permettant de parcourir toutes les clés ayant pour préfixe `foo` :

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

Voici la commande pour parcourir toutes les clés ayant pour préfixe `foo`, en limitant le nombre de résultats à 2 :

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

Voici la commande permettant de parcourir toutes les clés préfixées par `foo` en utilisant l'API RPC [`RangeStream`](/fr/etcd/learning/api/#rangestream). Le résultat est identique à un appel unaire `Range` :

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream` ne prend pas en charge `--order`, `--sort-by` ni les filtres de révision.

## Lire les versions antérieures des clés {#read-past-version-of-keys}

Les applications peuvent souhaiter lire des versions obsolètes d'une clé. Par exemple, une application peut souhaiter revenir à une configuration ancienne en accédant à une version antérieure d'une clé. En outre, une application peut souhaiter obtenir une vue cohérente sur plusieurs clés au fil de plusieurs requêtes en accédant à l'historique des clés.

Étant donné qu'une modification apportée au magasin clé-valeur d'un cluster etcd incrémente la révision globale du cluster etcd, une application peut lire des clés obsolètes en fournissant une révision etcd antérieure.

Supposons qu’un cluster etcd dispose déjà des clés suivantes :

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

Voici un exemple pour accéder aux versions antérieures des clés :

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## Lire les clés dont la valeur en octets est supérieure ou égale à celle de la clé spécifiée {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

Les applications peuvent souhaiter lire des clés dont la valeur en octets est supérieure ou égale à celle de la clé spécifiée.

Supposons qu’un cluster etcd dispose déjà des clés suivantes :

```bash
a = 123
b = 456
z = 789
```

Voici la commande permettant de lire les clés dont la valeur d'octet est supérieure ou égale à celle de la clé `b` :

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## Supprimer des clés {#delete-keys}

Les applications peuvent supprimer une clé ou une plage de clés d'un cluster etcd.

Supposons qu’un cluster etcd dispose déjà des clés suivantes :

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

Voici la commande pour supprimer la clé `foo` :

```bash
$ etcdctl del foo
1 # one key is deleted
```

Voici la commande permettant de supprimer les clés comprises entre `foo` et `foo9` :

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

Voici la commande permettant de supprimer la clé `zoo` avec la paire clé-valeur supprimée renvoyée :

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

Voici la commande permettant de supprimer les clés dont le préfixe est `zoo` :

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

Voici la commande permettant de supprimer les clés dont la valeur d'octet est supérieure ou égale à celle de la clé `b` :

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## Surveillance des modifications de clé {#watch-key-changes}

Les applications peuvent surveiller une clé ou une plage de clés afin de détecter toute mise à jour.

Voici la commande pour surveiller la clé `foo` :

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

Voici la commande pour surveiller la clé `foo` au format hexadécimal :

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Voici la commande pour effectuer une surveillance sur une plage de clés de `foo` à `foo9` :

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

Voici la commande pour surveiller les clés ayant le préfixe `foo` :

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

Voici la commande pour effectuer une surveillance sur plusieurs clés `foo` et `zoo` :

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## Surveillance des modifications historiques des clés {#watch-historical-changes-of-keys}

Les applications peuvent souhaiter surveiller les modifications historiques de clés dans etcd. Par exemple, une application peut souhaiter recevoir toutes les modifications d'une clé ; si l'application reste connectée à etcd, alors `watch` est suffisant. Toutefois, si l'application ou etcd échoue, une modification peut survenir pendant l'indisponibilité, et l'application ne recevra pas la mise à jour en temps réel. Pour garantir que la mise à jour soit livrée, l'application doit pouvoir surveiller les modifications historiques des clés. Pour cela, une application peut spécifier une révision historique lors d'une surveillance, tout comme lors de la lecture d'une version antérieure de clés.

Supposons que nous ayons terminé la séquence d'opérations suivante :

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

Voici un exemple de surveillance des modifications historiques :

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

Voici un exemple de surveillance uniquement à partir du dernier changement historique :

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## Progression de la surveillance {#watch-progress}

Les applications peuvent souhaiter vérifier l’avancement d’une surveillance afin de déterminer à quel point le flux de surveillance est à jour. Par exemple, si une surveillance est utilisée pour mettre à jour un cache, il peut être utile de savoir si le cache est périmé par rapport à la révision obtenue à partir d’une lecture en quorum.

Les requêtes de progression peuvent être émises à l’aide de la commande « progress » dans une session de surveillance interactive afin de demander au serveur etcd d’envoyer une mise à jour de notification de progression dans le flux de surveillance :

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> Le numéro de révision dans la réponse de notification de progression est la révision du nœud local du serveur etcd auquel le flux de surveillance est connecté. Si ce nœud est isolé et n'appartient pas au quorum, cette révision de notification de progression peut être inférieure à la révision retournée par une lecture effectuée en quorum contre un nœud serveur etcd non isolé.

## Révisions compactées {#compacted-revisions}

Comme nous l'avons mentionné, etcd conserve des révisions afin que les applications puissent lire des versions antérieures des clés. Toutefois, afin d'éviter de accumuler une quantité illimitée d'historique, il est important de compacter les révisions passées. Une fois la compaction effectuée, etcd supprime les révisions historiques, libérant ainsi des ressources pour une utilisation future. Toutes les données obsolètes dont la révision est antérieure à la révision compactée deviendront indisponibles.

Voici la commande pour compacter les révisions :

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> La révision actuelle du serveur etcd peut être obtenue en utilisant la commande get sur une clé quelconque (existante ou non) au format JSON. L'exemple ci-dessous montre la requête pour mykey, qui n'existe pas sur le serveur etcd :

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## Accorder des bails {#grant-leases}

Les applications peuvent accorder des bails pour des clés depuis un cluster etcd. Lorsqu'une clé est associée à un bail, sa durée de vie est liée à celle du bail, qui à son tour est régulée par une durée de vie (TTL). Chaque bail a une valeur minimale de durée de vie (TTL) spécifiée par l'application au moment de l'accord. La valeur réelle de TTL du bail est au moins égale à la durée minimale et est choisie par le cluster etcd. Dès qu'une durée de vie (TTL) d'un bail a expiré, le bail expire et toutes les clés associées sont supprimées.

Voici la commande pour accorder un bail :

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## Révoquer les bails {#revoke-leases}

Les applications révoquent les bails par identifiant de bail. La révocation d’un bail supprime toutes les clés associées.

Supposons que nous ayons terminé la séquence d'opérations suivante :

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

Voici la commande pour révoquer le même bail :

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## Maintenir les bails actifs {#keep-leases-alive}

Les applications peuvent maintenir un bail actif en actualisant périodiquement son TTL afin qu'il ne expire pas.

Supposons que nous ayons terminé la séquence d'opérations suivante :

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

Voici la commande permettant de maintenir le bail actif :

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## Obtenir les informations sur le bail {#get-lease-information}

Les applications peuvent souhaiter connaître les informations relatives aux bails, afin de les renouveler ou de vérifier s'ils existent encore ou ont expiré. Les applications peuvent également souhaiter connaître les clés auxquelles un bail particulier est associé.

Supposons que nous ayons terminé la séquence d'opérations suivante :

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

Voici la commande permettant d'obtenir des informations sur le bail :

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

Voici la commande permettant d'obtenir des informations sur le bail ainsi que les clés associées au bail :

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
