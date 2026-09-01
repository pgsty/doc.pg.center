---
title: "Modes de réplication"
weight: 70
icon: fa-solid fa-share-nodes
description: "Modes de réplication asynchrone et synchrone gérés par Patroni."
module: [PATRONI]
categories: [Concept]
aliases: [/docs/patroni/replication_modes/]
upstream_link: "https://patroni.readthedocs.io/en/latest/replication_modes.html"
---

<a id="replication_modes"></a>
Patroni utilise la réplication en streaming de PostgreSQL. Pour en savoir plus sur la réplication en streaming, consultez la documentation [Postgres](http://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION). Par défaut, Patroni configure PostgreSQL pour une réplication asynchrone. Le choix de votre schéma de réplication dépend de vos considérations métier. Étudiez à la fois la réplication asynchrone et synchrone, ainsi que d'autres solutions de haute disponibilité, afin de déterminer la solution la mieux adaptée à votre situation.

--------

## Durabilité en mode asynchrone {#asynchronous-mode-durability}

En mode asynchrone, le cluster peut perdre certaines transactions validées afin d'assurer la disponibilité. En cas de défaillance du serveur primaire ou de sa mise hors ligne pour toute autre raison, Patroni promeut automatiquement un serveur secondaire suffisamment sain en serveur primaire. Toutes les transactions non répliquées vers ce serveur secondaire restent sur une « timeline dérivée » sur le serveur primaire, et sont effectivement irrécupérables[^1].

Le nombre de transactions pouvant être perdues est contrôlé par le paramètre `maximum_lag_on_failover`. Étant donné que la position du journal de transactions du serveur primaire n'est pas échantillonnée en temps réel, en pratique, la quantité de données perdue en cas de basculement est bornée au pire cas par `maximum_lag_on_failover` octets de journal de transactions, plus la quantité écrite durant les dernières `ttl` secondes (`loop_wait`/2 secondes en cas moyen). Toutefois, le retard typique de réplication en régime stable est bien inférieur à une seconde.

Par défaut, lors de l'élection du leader, Patroni ne tient pas compte de la timeline actuelle des répliques, ce qui peut entraîner un comportement indésirable dans certains cas. Vous pouvez empêcher qu'un nœud dont la timeline diffère de celle d'un ancien primaire ne devienne le nouveau leader en modifiant la valeur du paramètre `check_timeline` en `true`.

--------

## Réplication synchrone PostgreSQL {#postgresql-synchronous-replication}

Vous pouvez utiliser la réplication synchrone de Postgres [synchronous replication](http://www.postgresql.org/docs/current/static/warm-standby.html#SYNCHRONOUS-REPLICATION) avec Patroni. La réplication synchrone garantit la cohérence au sein d’un cluster en confirmant que les écritures sont écrites sur une instance secondaire avant de renvoyer une réponse de succès au client connecté. Le coût de la réplication synchrone : une latence accrue et un débit réduit en écriture. Ce débit dépend entièrement de la performance du réseau.

Dans les environnements de datacenter hébergés (comme AWS, Rackspace ou tout réseau que vous ne contrôlez pas), la réplication synchrone augmente sensiblement la variabilité des performances d'écriture. Si les followers deviennent inaccessibles depuis le leader, ce dernier devient effectivement en lecture seule.

Pour activer un test de réplication synchrone simple, ajoutez les lignes suivantes à la section `parameters` de vos fichiers de configuration YAML :

```yaml
synchronous_commit: "on"
synchronous_standby_names: "*"
```

Lors de l'utilisation de la réplication synchrone PostgreSQL, utilisez au moins trois nœuds de données Postgres afin de garantir la disponibilité des écritures en cas de défaillance d'un hôte.

L'utilisation de la réplication synchrone PostgreSQL ne garantit pas l'absence totale de transactions perdues en toutes circonstances. Si le primaire et le secondaire servant actuellement de réplica synchrone tombent en panne simultanément, un troisième nœud ne contenant peut-être pas toutes les transactions sera promu.

<a id="synchronous_mode"></a>

--------

## mode synchrone {#synchronous-mode}

Pour les cas d'utilisation où la perte de transactions validées n'est pas acceptable, vous pouvez activer le mode synchrone de Patroni via [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode). Lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé, Patroni ne promeut pas un serveur de secours à moins d'être certain que ce dernier contient toutes les transactions qui ont pu retourner un statut de validation réussie au client[^2]. Cela signifie que le système peut être indisponible en écriture même si certains serveurs sont disponibles. Les administrateurs système peuvent toutefois utiliser des commandes de basculement manuel pour promouvoir un serveur de secours, même si cela entraîne une perte de transactions.

Activer le mode synchrone [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) ne garantit pas la durabilité des commits sur plusieurs nœuds dans toutes les circonstances. Lorsqu’aucun réplica approprié n’est disponible, le serveur primaire accepte toutefois les écritures, sans garantir leur réplication. Si le serveur primaire tombe en panne en ce mode, aucun réplica ne sera promu. Lorsque l’hôte qui était auparavant le primaire revient, il sera automatiquement promu, sauf si un basculement manuel a été effectué par l’administrateur système. Ce comportement rend le mode synchrone utilisable avec des clusters à deux nœuds.

Lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé et qu’un réplica tombe en panne, les validations bloquent jusqu’à l’itération suivante de Patroni, qui bascule le principal en mode autonome (retard maximal pour les écritures `ttl` secondes, cas moyen `loop_wait`/2 secondes). Une fermeture manuelle ou une redémarrage d’un réplica ne provoque pas d’interruption du service de validation. Le réplica signale au principal de se libérer de ses fonctions de réplica synchrone avant le démarrage de l’arrêt de PostgreSQL.

Lorsqu’il est absolument nécessaire de garantir que chaque écriture est stockée de manière durable sur au moins deux nœuds, activez `synchronous_mode_strict` en plus du mode [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode). Ce paramètre empêche Patroni de désactiver la réplication synchrone sur le nœud primaire lorsque aucun candidat de réplique synchrone n’est disponible, à moins que la transaction PostgreSQL ne désactive explicitement `synchronous_commit`, bloquant ainsi toutes les demandes d’écriture clients jusqu’à ce qu’au moins une réplique synchrone soit disponible.

Lorsque `synchronous_mode_strict` est activé et qu’aucune connexion de réplication active ne satisfait le facteur de réplication minimal, Patroni détermine la valeur de `synchronous_standby_names` comme suit :

1.  **Les derniers nœuds synchrones connus sont disponibles dans la clé `/sync` du DCS** : Patroni définit ou conserve `synchronous_standby_names` avec les nœuds qui y sont enregistrés. Par exemple, si `/sync` contient `leader=node1, sync_standby=node2,node3` et que les deux réplicas cessent leur réplication, Patroni continuera d'utiliser :

    ```ini
    synchronous_standby_names = 'node2,node3'
    ```

    Ces nœuds sont les derniers connus pour avoir reçu le dernier commit. Les commits seront bloqués jusqu'à ce qu'au moins l'un d'entre eux se reconnecte.

2.  **Basculement manuel vers un nœud asynchrone** : lorsqu'un nœud qui n'était pas dans la clé `/sync` est promu, par exemple via `patronictl failover --force`, il définit `synchronous_standby_names` sur l'ancien nœud primaire, car l'ancien nœud primaire est le seul nœud garanti pour avoir les données validées les plus récentes.

3.  **La clé `/sync` est vide** : par exemple, le mode strict vient d’être activé ou le cluster vient d’être initialisé sans réplique encore présente. Patroni définit :

    ```ini
    synchronous_standby_names = '__patroni_strict_sync_replica_placeholder__'
    ```

    Il s'agit d'une valeur sentinelle intégrée qui ne correspond à aucun nom de nœud réel, ce qui fait bloquer toutes les écritures jusqu'à ce qu'une réplique admissible commence à diffuser depuis le primaire. Ce placeholder remplace l'ancienne option générique `*`, qui pouvait inadvertamment permettre à un nœud non qualifié de satisfaire le critère de synchronisation.

> [!AVERTISSEMENT]
> La valeur `__patroni_strict_sync_replica_placeholder__` est réservée par Patroni et **ne doit pas** être utilisée comme `name` d'un nœud Patroni dans `patroni.yaml`. Patroni refusera de démarrer si ce nom est configuré.

Lorsque le mode strict est activé, Patroni émet un avertissement dans les journaux : `"No active replication connections and synchronous_mode_strict is requested. Commits will be delayed."`. Cet avertissement est émis une seule fois par événement d'activation, et non à chaque itération de la boucle HA.

Vous pouvez garantir qu’un serveur de repli ne devienne jamais un serveur de repli synchrone en définissant l’option `nosync` sur true. Il est recommandé de le définir ainsi pour les serveurs de repli situés derrière des connexions réseau lentes, qui entraîneraient une dégradation des performances s’ils devenaient des serveurs de repli synchrone. Définir l’option `nostream` sur true aura également le même effet.

Le mode synchrone peut être activé ou désactivé à l’aide de la commande `patronictl edit-config` ou via l’interface REST de Patroni. Voir [configuration dynamique](/fr/patroni/config/dynamic#dynamic) pour les instructions.

Note : En raison de la manière dont la réplication synchrone est implémentée dans PostgreSQL, il est encore possible de perdre des transactions même en utilisant `synchronous_mode_strict`. Si le backend PostgreSQL est annulé pendant l'attente de l'acquittement de la réplication (en raison d'une annulation de paquet due à un délai d'attente client ou à une panne du backend), les modifications de transaction deviennent visibles pour les autres backends. Ces modifications ne sont pas encore répliquées et peuvent être perdues en cas de promotion du standby.

--------

## Facteur de réplication synchrone {#synchronous-replication-factor}

Le paramètre `synchronous_node_count` est utilisé par Patroni pour gérer le nombre de bases de données en mode synchrone. Il est défini par défaut à `1`. Il n'a aucun effet lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est défini à `off`. Lorsqu'il est activé, Patroni gère précisément le nombre de bases de données en mode synchrone en fonction du paramètre `synchronous_node_count` et ajuste l'état dans le DCS et `synchronous_standby_names` dans PostgreSQL au moment où les membres rejoignent ou quittent le cluster. Si ce paramètre est défini à une valeur supérieure au nombre de nœuds éligibles, Patroni le réduit automatiquement.

--------

## Lag maximal sur nœud synchrone {#maximum-lag-on-synchronous-node}

Par défaut, Patroni reste sur les nœuds déclarés comme `synchronous`, selon la vue `pg_stat_replication`, même lorsque d'autres nœuds sont en avance. Cela permet de minimiser le nombre de changements de `synchronous_standby_names`. Pour modifier ce comportement, on peut utiliser le paramètre `maximum_lag_on_syncnode`. Il détermine jusqu'à quel retard une réplique peut être considérée comme « synchrone ».

Patroni utilise le LSN maximal de la réplique si plusieurs relais sont présents, sinon il utilise le LSN actuel du WAL du leader. La valeur par défaut est `-1`, et Patroni ne prendra aucune mesure pour échanger une réplique synchrone défaillante lorsque cette valeur est définie à `0` ou inférieure. Veuillez définir cette valeur suffisamment élevée afin que Patroni n'échange pas fréquemment les répliques synchrones pendant des pics de volume de transactions.

--------

## Implémentation du mode synchrone {#synchronous-mode-implementation}

Lorsque le mode synchrone est activé, Patroni maintient l'état de synchronisation dans le DCS (`/sync` key), qui contient la base primaire la plus récente et les bases de données en veille synchrone actuelles. Cet état est mis à jour selon des contraintes d'ordre strict afin d'assurer les invariants suivants :

-  Un nœud doit être marqué comme leader le plus récent chaque fois qu'il peut accepter des transactions d'écriture. Un plantage de Patroni ou une fermeture incorrecte de PostgreSQL peut entraîner une violation de cet invariant.
-  Un nœud doit être configuré comme réplica synchrone dans PostgreSQL aussi longtemps qu'il est publié comme réplica synchrone dans la clé `/sync` du DCS.
-  Un nœud qui n'est ni leader ni réplica synchrone actuel n'est pas autorisé à se promouvoir automatiquement.

Patroni n’attribuera qu’un ou plusieurs nœuds de secours synchrone en fonction du paramètre `synchronous_node_count` à `synchronous_standby_names`.

À chaque itération de la boucle HA, Patroni réévalue le choix des nœuds de secours synchrones. Si la liste actuelle de nœuds de secours synchrones est connectée et n’a pas demandé à être retirée de son statut synchrone, elle reste sélectionnée. Sinon, les membres du cluster disponibles pour la synchronisation les plus avancés dans la réplication sont sélectionnés.

### Exemple : {#example}

#### Clé `/config` dans DCS {#config-key-in-dcs}

```yaml
synchronous_mode: on
synchronous_node_count: 2
...
```

#### Clé `/sync` dans le DCS {#sync-key-in-dcs}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2"
}
```

#### postgresql.conf {#postgresqlconf}

```ini
synchronous_standby_names = 'FIRST 2 (node1,node2)'
```

Dans les exemples ci-dessus, seuls les nœuds `node1` et `node2` sont connus comme synchrones et autorisés à être promus automatiquement en cas de défaillance du primaire (`node0`).

<a id="quorum_mode"></a>

--------

## Mode de validation Quorum {#quorum-commit-mode}

À partir de PostgreSQL v10, Patroni prend en charge la réplication synchrone basée sur le quorum.

En ce mode, Patroni maintient l’état de synchronisation dans le DCS, qui contient le dernier primary connu, le nombre de nœuds requis pour atteindre la majorité, et les nœuds actuellement éligibles à voter pour la majorité. En état stable, les nœuds votant pour la majorité sont le leader et tous les réplicas synchrones. Cet état est mis à jour selon des contraintes d’ordre strict, concernant la promotion des nœuds et `synchronous_standby_names`, afin de garantir qu’à tout moment, tout sous-ensemble de votants pouvant atteindre la majorité inclut au moins un nœud ayant effectué le dernier commit réussi.

À chaque itération de la boucle HA, Patroni réévalue les choix de réplicas synchrones et le quorum, en fonction de la disponibilité des nœuds et de la configuration demandée du cluster. Dans les versions de PostgreSQL supérieures à 9.6, tous les nœuds éligibles sont ajoutés en tant que réplicas synchrones dès que leur réplication rattrape le leader.

La validation en quorum permet de réduire les latences dans le cas le plus défavorable, même en fonctionnement normal, car une latence plus élevée de réplication vers un serveur de secours peut être compensée par les autres serveurs de secours.

Le mode synchrone basé sur le quorum peut être activé en définissant [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) sur `quorum` à l’aide de la commande `patronictl edit-config` ou via l’interface REST de Patroni. Voir [configuration dynamique](/fr/patroni/config/dynamic#dynamic) pour les instructions.

D'autres paramètres, tels que `synchronous_node_count`, `maximum_lag_on_syncnode` et `synchronous_mode_strict`, fonctionnent de la même manière qu'avec `synchronous_mode=on`.

En mode validation par quorum avec `synchronous_mode_strict`, lorsque aucune réplique active n'est disponible, Patroni définit `synchronous_standby_names` à `ANY N (<last known voters>)`, en conservant les derniers électeurs du quorum connus à partir de `/sync`, ou à `ANY 1 (__patroni_strict_sync_replica_placeholder__)` lorsque aucun électeur n'est stocké dans la clé `/sync`.

### Exemple : {#example-1}

#### Clé `/config` dans DCS {#config-key-in-dcs-1}

```yaml
synchronous_mode: quorum
synchronous_node_count: 2
...
```

#### Clé `/sync` dans le DCS {#sync-key-in-dcs-1}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2,node3",
    "quorum": 1
}
```

#### postgresql.conf {#postgresqlconf-1}

```ini
synchronous_standby_names = 'ANY 2 (node1,node2,node3)'
```

Si le nœud primaire (`node0`) échoue, dans l'exemple ci-dessus, deux des nœuds `node1`, `node2`, `node3` auront reçu la dernière transaction, mais nous ne savons pas lesquels. Pour déterminer si le nœud `node1` a reçu la dernière transaction, il faut comparer son LSN avec celui d'au moins un nœud (`quorum=1` dans la clé `/sync`) parmi `node2` et `node3`. Si `node1` n'est pas en retard par rapport à au moins l'un d'entre eux, on peut garantir qu'il n'y aura pas de perte de données visible pour l'utilisateur si `node1` est promu.

[^1]: Les données sont toujours présentes, mais leur récupération nécessite une intervention manuelle de la part d'un spécialiste de la récupération de données. Lorsque Patroni est autorisé à effectuer un rewind avec `use_pg_rewind`, la timeline forkée est automatiquement supprimée afin de rejoindre le primaire défaillant dans le cluster. Toutefois, pour que `use_pg_rewind` fonctionne correctement, soit le cluster doit être initialisé avec `data page checksums` (`--data-checksums` option pour `initdb`), soit `wal_log_hints` doit être défini sur `on`.

[^2]: Les clients peuvent modifier le comportement au niveau de chaque transaction à l'aide du paramètre `synchronous_commit` de PostgreSQL. Les transactions dont la valeur de `synchronous_commit` est `off` ou `local` peuvent être perdues en cas de basculement, mais ne seront pas bloquées par les retards de réplication.
