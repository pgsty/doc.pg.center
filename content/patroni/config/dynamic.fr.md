---
title: "Paramètres de configuration dynamique"
linkTitle: "Configuration dynamique"
weight: 10
icon: fa-solid fa-sliders
description: "Paramètres de configuration dynamique stockés dans le DCS et appliqués au cluster entier."
module: [PATRONI]
categories: [Référence]
upstream_link: "https://patroni.readthedocs.io/en/latest/dynamic_configuration.html"
---

<a id="dynamic"></a>
La configuration dynamique est stockée dans le magasin de configuration distribué (DCS) et appliquée sur tous les nœuds du cluster.

Pour modifier la configuration dynamique, vous pouvez utiliser soit l'outil [patronictl_edit_config](/fr/patroni/patronictl#patronictl_edit_config), soit l'[API REST](/fr/patroni/rest_api#rest_api) de Patroni.

- **loop_wait** : nombre de secondes pendant lesquelles la boucle s'endort. Valeur par défaut : 10, valeur minimale possible : 1
- **ttl** : durée de vie du verrou de leader (en secondes). Pensez-y comme la durée avant le déclenchement du processus de basculement automatique. Valeur par défaut : 30, valeur minimale possible : 20
- **retry_timeout** : délai d'attente pour les nouvelles tentatives des opérations DCS et PostgreSQL (en secondes). Les problèmes DCS ou réseau de durée inférieure à cette valeur ne provoqueront pas la rétrogradation du leader par Patroni. Valeur par défaut : 10, valeur minimale possible : 3

> [!WARNING]
> Lorsque vous modifiez les valeurs de **loop_wait**, **retry_timeout** ou **ttl**, vous devez respecter la règle suivante :
>
> ```python
> loop_wait + 2 * retry_timeout <= ttl
> ```

- **maximum_lag_on_failover** : le nombre maximum d'octets dont un suiveur peut être en retard pour pouvoir participer à l'élection du leader.
- **primary_race_backoff** : reporte l'élection du leader sur les répliques secondaires de `primary_race_backoff` secondes si la réplication WAL depuis le primaire progresse encore. Cela permet de réduire les basculements inutiles causés par un Patroni temporairement sans réponse. Valeur par défaut : 0 (désactivé).
- **maximum_lag_on_syncnode** : le nombre maximum d'octets dont un suiveur synchrone peut être en retard avant d'être considéré comme un candidat défaillant et remplacé par un suiveur asynchrone sain. Patroni utilise le LSN maximal des répliques s'il y a plus d'un suiveur, sinon il utilise le LSN WAL actuel du leader. Valeur par défaut : -1. Patroni ne prendra aucune mesure pour remplacer un suiveur synchrone défaillant lorsque cette valeur est réglée à 0 ou inférieure. Veuillez définir une valeur suffisamment élevée pour éviter que Patroni ne remplace fréquemment un suiveur synchrone pendant des pics de charge transactionnelle.
- **max_timelines_history** : nombre maximum d'éléments d'historique de timeline conservés dans le DCS. Valeur par défaut : 0. Lorsqu'elle est réglée sur 0, l'historique complet est conservé dans le DCS.
- **primary_start_timeout** : durée autorisée à un serveur primaire pour se rétablir après une panne avant que le basculement ne soit déclenché (en secondes). Valeur par défaut : 300 secondes. Si cette valeur est réglée sur 0, le basculement est effectué immédiatement après détection d'une panne, si possible. En cas de réplication asynchrone, un basculement peut entraîner la perte de transactions. Le temps de basculement maximal en cas de panne du primaire est : loop_wait + primary_start_timeout + loop_wait, sauf si primary_start_timeout est égal à zéro, auquel cas il est simplement égal à loop_wait. Ajustez cette valeur en fonction de votre compromis entre durabilité et disponibilité.
- **primary_stop_timeout** : nombre de secondes pendant lesquelles Patroni est autorisé à attendre lors de l'arrêt de Postgres, et qui n'est effectif que lorsque synchronous_mode est activé. Si la valeur est supérieure à 0 et que synchronous_mode est activé, Patroni envoie un signal SIGKILL au postmaster si l'opération d'arrêt dure plus longtemps que la valeur définie par primary_stop_timeout. Définissez cette valeur en fonction de votre compromis entre durabilité et disponibilité. Si ce paramètre n'est pas défini ou est défini à une valeur inférieure ou égale à 0, primary_stop_timeout n'est pas pris en compte.
- **synchronous_mode** : active le mode de réplication synchrone. Valeurs possibles : `off`, `on`, `quorum`. Dans ce mode, le leader gère `synchronous_standby_names`, et seul le dernier leader connu, ou l'une des répliques synchrones, est autorisée à participer à la course au leader. Le mode synchrone garantit que les transactions validées ne seront pas perdues lors d’un basculement, au prix de la perte de disponibilité pour les écritures lorsque Patroni ne peut pas garantir la durabilité des transactions. Voir la documentation sur les [modes de réplication](/fr/patroni/replication_modes#replication_modes) pour plus de détails.
- **synchronous_mode_strict** : empêche la désactivation de la réplication synchrone si aucune réplique synchrone n'est disponible, bloquant toutes les écritures clients sur le primaire. En mode synchrone fondé sur les priorités (`synchronous_mode: on`), Patroni 4.1.5 définit `synchronous_standby_names` à `*` lorsqu'aucune réplique synchrone admissible n'est disponible. Consultez la [documentation des modes de réplication](/fr/patroni/replication_modes#replication_modes) pour plus de détails.
- **synchronous_node_count** : si le mode [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé, ce paramètre est utilisé par Patroni pour gérer le nombre précis d'instances de standby synchrones et ajuste l'état dans le DCS ainsi que le paramètre `synchronous_standby_names` dans PostgreSQL au fur et à mesure que les membres rejoignent ou quittent le cluster. Si la valeur est définie à un nombre supérieur au nombre de nœuds éligibles, elle sera automatiquement ajustée. Valeur par défaut : `1`.
- **failsafe_mode** : active le mode [mode de sécurité du DCS](/fr/patroni/dcs_failsafe_mode#dcs_failsafe_mode). Valeur par défaut : `false`.
- **postgresql** :
  - **use_pg_rewind** : indique si pg_rewind doit être utilisé. Valeur par défaut : `false`. Notez que le cluster doit avoir été initialisé avec `data page checksums` (`--data-checksums` option pour `initdb`) et/ou `wal_log_hints` doit être défini à `on`, sinon `pg_rewind` ne fonctionnera pas.
  - **use_slots** : indique si les slots de réplication doivent être utilisés. Valeur par défaut : `true` sur PostgreSQL 9.4+.
  - **recovery_conf** : paramètres de configuration supplémentaires écrits dans recovery.conf lors de la configuration du suiveur. Il n’existe plus de recovery.conf dans PostgreSQL 12, mais vous pouvez continuer à utiliser cette section, car Patroni la gère de manière transparente.
  - **parameters** : paramètres de configuration (GUC) pour Postgres au format `{max_connections: 100, wal_level: "replica", max_wal_senders: 10, wal_log_hints: "on"}`. Beaucoup de ces paramètres sont requis pour que la réplication fonctionne.
  - **parameters_primary** : (facultatif) substitutions de paramètres spécifiques au rôle pour le primaire. Ces valeurs sont fusionnées avec et remplacent celles du paramètre **parameters**.
  - **parameters_replica** : (facultatif) substitutions de paramètres spécifiques au rôle pour la réplique. Ces valeurs sont fusionnées avec et remplacent celles du paramètre **parameters**.
  - **parameters_standby_leader** : (facultatif) substitutions de paramètres spécifiques au rôle pour le standby_leader. Ces valeurs sont fusionnées avec et remplacent celles du paramètre **parameters**.
  - **pg_hba** : liste de lignes que Patroni utilisera pour générer `pg_hba.conf`. Patroni ignore ce paramètre si le paramètre PostgreSQL `hba_file` est défini avec une valeur différente de celle par défaut.
    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5** : une ligne de ce type est obligatoire pour la réplication.
  - **pg_hba_primary** : (facultatif) entrées pg_hba spécifiques au rôle primaire. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.
  - **pg_hba_replica** : (facultatif) entrées pg_hba spécifiques au rôle réplique. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.
  - **pg_hba_standby_leader** : (facultatif) entrées pg_hba spécifiques au rôle standby_leader. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.
  - **pg_ident** : liste de lignes que Patroni utilisera pour générer `pg_ident.conf`. Patroni ignore ce paramètre si le paramètre `ident_file` PostgreSQL est défini avec une valeur autre que celle par défaut.
    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary** : (facultatif) entrées pg_ident spécifiques au rôle primaire. Elles remplacent entièrement **pg_ident** (pas de fusion). Si non définies, **pg_ident** est utilisée.
  - **pg_ident_replica** : (facultatif) entrées pg_ident spécifiques au rôle réplique. Elles remplacent entièrement **pg_ident** (pas de fusion). Si non définies, **pg_ident** est utilisée.
  - **pg_ident_standby_leader** : (facultatif) entrées pg_ident spécifiques au rôle standby_leader. Elles remplacent entièrement **pg_ident** (pas de fusion). Si non définies, **pg_ident** est utilisée.
- **standby_cluster** : si cette section est définie, cela signifie que l'on souhaite amorcer un cluster de secours.
  - **host** : adresse du nœud distant
  - **port** : port du nœud distant
  - **primary_slot_name** : nom de la slot à utiliser sur le nœud distant pour la réplication. Ce paramètre est facultatif ; sa valeur par défaut est dérivée du nom de l'instance (voir la fonction `slot_name_from_member_name`).
  - **create_replica_methods** : liste ordonnée des méthodes pouvant être utilisées pour amorcer un leader de secours à partir du primaire distant, peut différer de la liste définie dans [postgresql_settings](/fr/patroni/config/yaml#postgresql_settings)
  - **restore_command** : commande permettant de restaurer les enregistrements WAL depuis le primaire distant vers les nœuds d'un cluster de secours, peut différer de la liste définie dans [postgresql_settings](/fr/patroni/config/yaml#postgresql_settings)
  - **archive_cleanup_command** : commande de nettoyage pour le leader de secours
  - **recovery_min_apply_delay** : durée d'attente avant d'appliquer réellement les enregistrements WAL sur un leader de secours
- **member_slots_ttl** : durée de rétention des slots de réplication physique pour les répliques lorsqu'elles sont arrêtées. Valeur par défaut : `30min`. Définissez-la sur `0` si vous souhaitez conserver le comportement ancien (lorsque la clé du membre expire dans le DCS, le slot est supprimé immédiatement). Cette fonctionnalité n'est disponible qu'à partir de PostgreSQL 11.
- **slots** : définir des slots de réplication permanents. Ces slots seront préservés lors d’un basculement planifié ou d’un basculement. Les slots permanents qui n'existent pas seront créés par Patroni. À partir de PostgreSQL 11, les slots physiques permanents sont créés sur tous les nœuds et leur position est avancée toutes les **loop_wait** secondes. Pour les versions de PostgreSQL antérieures à 11, les slots de réplication physiques permanents ne sont maintenus que sur le primaire actuel. Les slots logiques sont copiés depuis le primaire vers une réplique lors d’un redémarrage, puis leur position est avancée toutes les **loop_wait** secondes (le cas échéant). La copie des fichiers de slots logiques s’effectue via la connexion `libpq` et à l’aide des identifiants de rewind ou des identifiants de superutilisateur (voir la section **postgresql.authentication**). Il existe toujours un risque que la position du slot logique sur la réplique soit légèrement en retard par rapport au précédent primaire, l’application doit donc être préparée à recevoir certains messages une seconde fois après un basculement. La méthode la plus simple consiste à suivre `confirmed_flush_lsn`. L’activation des slots de réplication permanents nécessite que **postgresql.use_slots** soit défini à `true`. Si des slots de réplication logiques permanents sont définis, Patroni activera automatiquement `hot_standby_feedback`. Étant donné que le basculement des slots de réplication logiques est dangereux sous PostgreSQL 9.6 et versions antérieures, et que PostgreSQL 10 manque certaines fonctions essentielles, cette fonctionnalité n’est disponible qu’avec PostgreSQL 11+.
  - **my_slot_name** : le nom de la slot de réplication permanente. Si le nom de la slot permanente correspond à celui du nœud actuel, celle-ci ne sera pas créée sur ce nœud. Si vous ajoutez une slot de réplication physique permanente dont le nom correspond à celui d'un membre Patroni, Patroni veillera à ce que la slot créée ne soit pas supprimée, même si le membre correspondant ne répond plus, situation qui entraînerait normalement la suppression de la slot par Patroni. Bien que cela puisse être utile dans certaines situations, par exemple lorsque vous souhaitez que les slots de réplication utilisés par les membres persistent pendant des défaillances temporaires ou lors de l'importation de membres existants dans un nouveau cluster Patroni (voir [Convertir une instance autonome en cluster Patroni](/fr/patroni/existing_data#existing_data) pour plus de détails), l'opérateur doit exercer une prudence particulière afin que ces conflits de noms ne soient pas persistés dans le DCS, lorsque la slot n'est plus nécessaire, en raison de leur impact sur le fonctionnement normal de Patroni.
    - **type** : type de slot. Peut être `physical` ou `logical`. Si le slot est logique, vous devez également définir `database` et `plugin`. Si le slot est physique, vous pouvez éventuellement définir `cluster_type`.
    - **database** : nom de la base de données où les slots logiques doivent être créés.
    - **plugin** : nom du plugin pour le slot logique.
    - **cluster_type** : type de cluster (`primary` ou `standby`) sur lequel le slot doit exclusivement être créé ; sinon, il ne sera pas créé ou un slot déjà existant sera supprimé.
- **ignore_slots** : liste de jeux de propriétés de slot de réplication que Patroni doit ignorer. Cette configuration/fonctionnalité/etc. est utile lorsque certains slots de réplication sont gérés en dehors de Patroni. Tout sous-ensemble de propriétés correspondantes entraînera l'ignorance du slot par Patroni.
  - **name** : nom du slot de réplication.
  - **type** : type de slot. Peut être `physical` ou `logical`. Si le slot est logique, vous pouvez éventuellement définir `database` et/ou `plugin`.
  - **database** : le nom de la base de données (lorsqu'il s'agit d'un slot `logical`).
  - **plugin** : le plugin de décodage logique (lorsqu'il s'agit d'un slot `logical`).

Note : **slots** est une carte associative tandis que **ignore_slots** est un tableau. Par exemple :

```yaml
slots:
  permanent_logical_slot_name:
    type: logical
    database: my_db
    plugin: test_decoding
  permanent_physical_slot_name:
    type: physical
  ...
ignore_slots:
  - name: ignored_logical_slot_name
    type: logical
    database: my_db
    plugin: test_decoding
  - name: ignored_physical_slot_name
    type: physical
  ...
```

Note : Lorsque PostgreSQL v11 ou une version ultérieure est utilisé, Patroni maintient des slots de réplication physique sur tous les nœuds pouvant devenir un leader, afin que les nœuds répliques conservent les segments WAL réservés s’ils sont potentiellement requis par d’autres nœuds. Si un nœud est absent et que sa clé membre dans le DCS expire, le slot de réplication correspondant est supprimé après `member_slots_ttl` (valeur par défaut : `30min`). Vous pouvez ajuster cette durée en fonction de vos besoins. Autrement, si la topologie du cluster est statique (nombre fixe de nœuds dont les noms ne changent jamais), vous pouvez configurer des slots de réplication physique permanents nommés selon les noms des nœuds afin d’éviter la suppression des slots et le recyclage des fichiers WAL pendant une indisponibilité temporaire de la réplique :

```yaml
slots:
  node_name1:
    type: physical
  node_name2:
    type: physical
  node_name3:
    type: physical
  ...
```

> [!WARNING]
> Les slots de réplication permanents ne sont synchronisés qu'à partir du `primary`/`standby_leader` vers les nœuds répliques. Cela signifie que les applications doivent les utiliser uniquement depuis le nœud leader. Leur utilisation sur les nœuds répliques entraîne une croissance indéfinie de `pg_wal` sur tous les autres nœuds du cluster. Une exception à cette règle concerne les slots physiques correspondant aux noms des membres Patroni (créés et gérés par Patroni). Ces slots sont synchronisés entre tous les nœuds, car ils sont utilisés pour la réplication entre eux.

> [!WARNING]
> Définir l'étiquette `nostream` sur un nœud de secours désactive la copie et la synchronisation des slots de réplication logique permanents sur ce nœud lui-même et sur toutes ses répliques en cascade, le cas échéant.
