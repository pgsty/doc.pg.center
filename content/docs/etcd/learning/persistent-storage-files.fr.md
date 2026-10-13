---
title: Fichiers de stockage persistant d'etcd
weight: 2650
description: Référence du format de stockage persistant et des fichiers
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/persistent-storage-files.md"
aliases: [/etcd/learning/persistent-storage-files/]
---

Ce document explique le format de stockage persistant d’etcd : nomenclature, contenu et outils permettant aux développeurs d’en inspecter le contenu. À l’avenir, ce document devrait être mis à jour pour refléter les évolutions du modèle de stockage. Il s’adresse aux développeurs d’etcd afin de les aider dans leurs besoins de récupération de données.


## Prérequis {#prerequisites}

Les articles suivants fournissent des informations de fond utiles pour ce document :

* [Vue d'ensemble du modèle de données etcd](/fr/docs/etcd/learning/data_model/)
* [Vue d'ensemble de Raft](https://raft.github.io/raft.pdf) (notamment la section « 5.3 Réplication des journaux »).


## Aperçu {#overview}

### Fichiers de longue durée de vie {#long-leaving-files}

<table>
  <tr>
    <th>Nom de fichier</th>
    <th>Objectif général</th>
  </tr>

  <tr>
    <td><pre>./member/snap/db</pre></td>
    <td><strong>bbolt <a href="https://en.wikipedia.org/wiki/B%2B_tree">b+tree</a></strong> qui stocke toutes les données appliquées, les informations d'autorisation d'appartenance et les métadonnées. Il connaît l'index du dernier journal WAL appliqué (<a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a>).
    </td>
  </tr>

  <tr>
    <td><pre>./member/snap/0000000000000002-0000000000049425.snap
./member/snap/0000000000000002-0000000000061ace.snap</pre>
    </td>
    <td>
      <p>
        Instantanés périodiques <strong>de l’ancien magasin v2</strong>, contenant :
        <ul>
          <li>informations de base sur le membre</li>
          <li>etcd-version</li>
        </ul>
      </p>
      <p>À compter d'etcd v3, le contenu est redondant par rapport au contenu des fichiers /snap/db.</p>
      <p>Périodiquement (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>), ces fichiers <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L597">sont supprimés</a>, et les derniers <code>--max-snapshots=5</code> sont conservés.</p>
   </td>
  </tr>

  <tr>
    <td><pre>/member/snap/000000000007a178.snap.db</pre></td>
    <td>
      <p>Un instantané <strong>bbolt complet téléchargé</strong> depuis le leader etcd si la réplique était trop en retard.</p>
      <p>Possède le même type de contenu que le fichier (<code>./member/snap/db</code>)</p>
      <p>
        Le fichier est utilisé dans deux scénarios :
        <ul>
          <li>En réponse à la demande du leader de se rétablir à partir de l'instantané.</li>
          <li><a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L444">Lors du démarrage du serveur</a>, lorsque le dernier instantané (.snap.db) est trouvé et détecté comme ayant un index plus récent que consistent_index dans le fichier actuel <code>snap.db</code>.</li>
        </ul>
        Note : Les instantanés périodiques générés sur chaque réplique ne sont émis qu'au format de fichier *.snap (et non *.snap.db). Ainsi, aucune garantie n'est donnée que le dernier instantané (dans le journal WAL) dispose d'un fichier *.snap.db. Toutefois, dans un tel cas, le backend (snap/db) doit être plus récent que l'instantané.
      </p>
      <p>
        Le fichier <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L1236"> n'est pas supprimé une fois la récupération terminée</a> (le contenu entier est donc copié dans le fichier ./member/snap/db). Périodiquement (<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L87">30s</a>), les fichiers <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/server.go#L774">sont</a> purgés.
Ici aussi, <code>--max-snapshots=5</code> sont conservés. Comme ces fichiers peuvent atteindre plusieurs Go, cela peut entraîner un risque d'épuisement de l'espace disque.
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/000000000000000f-00000000000b38c7.wal
./member/wal/000000000000000e-00000000000a7fe3.wal
./member/wal/000000000000000d-000000000009c70c.wal</pre>
    </td>
    <td>
      <p><strong>Journaux d'écriture de Raft</strong>, contenant les transactions récentes acceptées par Raft, ainsi que des instantanés périodiques ou des enregistrements CRC.</p>
      <p> Les fichiers récents <code>--max-wals=5</code> sont conservés. Chaque fichier mesure <code>~64*10^6</code> octets. Le fichier est coupé lorsqu'il dépasse cette taille codée en dur, de sorte que les fichiers peuvent légèrement dépasser cette taille (la préallocation <code>0.tmp</code> ne garantit donc pas une protection complète contre le dépassement du disque).</p>
      <p>Si les instantanés sont trop espacés, il peut y avoir plus de <code>--max-wals=5</code>, car les verrous au niveau du système de fichiers protègent les fichiers, empêchant qu'ils ne soient supprimés trop tôt.</p>
    </td>
  </tr>

  <tr>
    <td><pre>./member/wal/0.tmp (or .../1.tmp)</pre></td>
    <td>
      <strong>Espace préalloué</strong> pour le prochain fichier de journal d'écriture anticipée.
      Utilisé pour éviter que Raft ne reste bloqué en raison d'un manque de capacité des journaux WAL, sans possibilité de déclencher une alarme.
    </td>
  </tr>
</table>


### Fichiers temporaires {#temporary-files}

Pendant le traitement interne d’etcd, il est possible de rencontrer plusieurs fichiers à durée de vie courte :

<table>
  <tr>
    <th>Fichier</th>
    <th>Objectif général</th>
  </tr>
  <tr>
    <td><pre>./member/snap/0000000000000002-000000000007a178.snap.broken</pre></td>
    <td>
      <p>Les fichiers d'instantané sont renommés en « broken » lorsqu'ils ne peuvent pas être <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/api/snap/snapshotter.go#L144">chargés</a>.<p>
      <!-- TODO: etcdserver/api/snap/snapshotter.go:148 -->
      <p>La tentative de chargement du fichier le plus récent a lieu lorsqu’etcd est <a href="https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/etcdserver/server.go#L302">démarré</a>.</p>
      <!-- TODO: etcdserver/server.go:428 -->
      <p>Ou lors des commandes de sauvegarde/migration d'etcdctl.</p>
   </td>
  </tr>
  <tr>
    <td><pre>./member/snap/tmp071677638 (random suffix)</pre></td>
    <td>
      <p><a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L39">Fichier temporaire</a> (bbolt) créé sur les répliques en réponse à la demande msgSnap du leader, afin de répondre à la demande du leader de restaurer le stockage à partir de l'instantané fourni.</p>
      <p>
        Après une récupération réussie (complète) du contenu, le fichier est <a href="https://github.com/etcd-io/etcd/blob/ae9734ed278b7a1a7dfc82e800471ebbf9fce56f/etcdserver/api/snap/db.go#L55">renommé</a> en : <code>/member/snap/[SNAPSHOT-INDEX].snap.db</code>. En cas de mort du serveur ou de son interruption pendant le téléchargement des fichiers, ceux-ci restent sur le disque et ne sont jamais nettoyés automatiquement. Ils peuvent être de taille importante (en gigaoctets).
      </p>
      <p>Voir <a href="https://github.com/etcd-io/etcd/issues/12837">etcd/issues/12837</a>. <strong>Corrigé dans etcd 3.5.</strong></p>
    </td>
  </tr>
  <tr>
    <td><pre>/member/snap/db.tmp.071677638 (random suffix)</pre></td>
    <td>
      <p>Un fichier temporaire contenant une copie du contenu du backend (/member/snap/db), pendant le <a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/mvcc/backend/backend.go#L373">processus de défragmentation</a>. Une fois le processus réussi, le fichier est renommé en /member/snap/db, remplaçant ainsi le backend original.</p>
      <p>Au démarrage du serveur etcd, ces fichiers sont<a href="https://github.com/etcd-io/etcd/blob/a4570a60e771402360755beb7d662bdbca1f87f2/server/etcdserver/api/snap/snapshotter.go#L217">supprimés</a>.</p>
    </td>
  </tr>
</table>

## bbolt arbre B+ : **member/snap/db** {#bbolt-btree-membersnapdb}

Ce fichier contient le contenu principal d'etcd, appliqué à un point spécifique du journal Raft (voir [consistent_index](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92)).


### Organisation physique {#physical-organization}

Le stockage bolt est physiquement organisé sous la forme d’un arbre [b+tree](https://en.wikipedia.org/wiki/B%2B_tree). Les pages physiques de l’arbre b+ ne sont jamais modifiées in situ[^1]. À la place, leur contenu est copié vers une nouvelle page (récupérée à partir de la liste des pages libres), et la page ancienne est ajoutée à la liste des pages libres dès qu’aucune transaction ouverte ne peut plus y accéder. Grâce à ce processus, une transaction RO ouverte voit un état cohérent de l’historique du stockage. Une transaction RW est exclusive et bloque toutes les autres transactions RW.
Les grandes valeurs sont stockées sur plusieurs pages continues. Le processus de récupération de pages combiné à la nécessité d’attribuer des zones contiguës de pages de tailles différentes peut entraîner une fragmentation croissante du stockage bbolt.

Le fichier bbolt ne se réduit jamais automatiquement. Seul le processus de défragmentation permet de réécrire le fichier dans un nouveau fichier disposant d'une certaine réserve de pages libres à la fin et dont la taille a été tronquée.


### Organisation logique {#logical-organization}

Le stockage bbolt est divisé en compartiments. Dans chaque compartiment, des clés (paires byte[]->byte[] valeurs) sont stockées dans l'ordre lexicographique. La liste ci-dessous représente les compartiments utilisés par etcd (dans la version 3.5) ainsi que les clés en usage.

<table>
  <tr>
    <th>Bucket</th>
    <th>Clé</th>
    <th>Valeur d'exemple</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>alarm</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/etcdserverpb/rpc.proto#L976">rpcpb.Alarm</a> :
    {MemberID, Alarm: NONE|NOSPACE|CORRUPT}</code>
    </td>
    <td><code>nil</code></td>
    <td>Indique que des problèmes ont été diagnostiqués sur l'un des membres.</td>
  </tr>
  <tr>
    <td>auth</td>
    <td>"authRevision"</td>
    <td><code>""</code> (vide) ou <code>BigEndian.PutUint64</code></td>
    <td>
      <p>Tout changement de rôles ou d'utilisateurs incrémente ce champ à la validation de la transaction.</p>
      <p>
        La valeur n'est utilisée que pour le verrouillage optimiste <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/v3_server.go#L461"> durant </a> le processus d'autorisation.
      </p>
    </td>
  </tr>
  <tr>
    <td>authRoles</td>
    <td>[roleName] en tant que chaîne</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L38">authpb.Role</a></code> sérialisé</td>
    <td></td>
  </tr>
  <tr>
    <td>authUsers</td>
    <td>[userName] en tant que chaîne</td>
    <td><code><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/authpb/auth.proto#L17">authpb.User</a></code> sérialisé</td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="2" >cluster</td>
    <td>"clusterVersion"</td>
    <td><code>"3.5.0"</code> (chaîne)</td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/etcdserver/server.go#L2314">version mineure</a>, agréée par consensus, de la version de stockage commune.</td>
  </tr>
  <tr>
    <td>"downgrade"</td>
    <td>JSON: <pre>{
  "target-version": "3.4.0"
  "enabled": true/false
}</pre>
    </td>
    <td>
      <p>Persiste l'intention configurée par la requête la plus récente : <code>Downgrade RPC</code>.</p>
      <p>Depuis la version v3.5</p>
    </td>
  </tr>
  <tr>
    <td><strong>key</strong></td>
    <td>
      <p>[revisionId] encodée à l'aide de <a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub}</p>
      <p>Les suppressions de paires clé-valeur sont sérialisées avec un « t » à la fin (comme une « pierre tombale »)</p>
    </td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/api/mvccpb/kv.proto#L12"><code>mvccpb.KeyValue</code></a> sérialisé au format Protocol Buffers (<code>key, create_rev, mod_rev, version, value, lease id</code>)</td>
    <td></td>
  </tr>
  <tr>
    <td>lease</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/lease/leasepb/lease.proto#L13"><code>leasepb.Lease</code></a> sérialisé au format Protocol Buffers (ID, TTL, RemainingTTL)</td>
    <td>
      <p>Remarque : LeaseCheckpoint étend uniquement RemainingTTL. Le TTL provient uniquement de l'origine de Grant.</p>
      <p style="text-decoration:underline;">Note2 : les TTL sont conservés en secondes (à partir de la valeur « now » non définie). Un serveur pris dans une boucle de redémarrage ne libère pas les baux !!!</p>
    </td>
  </tr>
  <tr>
    <td>members</td>
    <td>[memberId] en hexadécimal sous forme de chaîne : <code>"8e9e05c52164694d"</code></td>
    <td>
      <em>Chaîne JSON sérialisée du type <a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/member.go#L43">membre</a> :</em>
      <pre>{
  "id":10276657743932975437,
  "peerURLs":[
  "<a href="http://localhost:2380">http://localhost:2380</a>"],
  "name":"default",
  "clientURLs": ["http://localhost:2379"]
}</pre>
    </td>
    <td>Informations d'appartenance au cluster convenues.</td>
  </tr>
  <tr>
    <td>members_removed</td>
    <td>[memberId] en hexadécimal sous forme de chaîne : <code>"8e9e05c52164694d"</code></td>
    <td><code>[]byte("removed")</code></td>
    <td>
      <p>Identifiants de tous les membres supprimés. Utilisé pour vérifier qu'un membre supprimé n'est jamais réajouté sous le même identifiant.</p>
      <p><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/api/membership/cluster.go#L251">Le champ est actuellement (3.4) lu à partir du magasin V2 et jamais à partir de V3</a>. Voir <a href="https://github.com/etcd-io/etcd/pull/12820">https://github.com/etcd-io/etcd/pull/12820</a></p>
    </td>
  </tr>
  <tr>
    <td rowspan="3"><strong>meta</strong></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/etcdserver/cindex/cindex.go#L92">"consistent_index"</a></td>
    <td>uint64 octets (BigEndian)</td>
    <td>Représente le décalage de la dernière entrée WAL appliquée au stockage Bolt DB.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L41">"scheduledCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} encodé. (16 octets)</td>
    <td>Utilisé pour réinitialiser le compactage si un incident s'est produit après une demande de compactage.</td>
  </tr>
  <tr>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore.go#L42">"finishedCompactRev"</a></td>
    <td><a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/revision.go#L56">bytesToRev</a>{main,sub} encodé. (16 octets)</td>
    <td>Révision à laquelle le magasin a été récemment compacté avec succès (<a href="https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54">https://github.com/etcd-io/etcd/blob/ae7862e8bc8007eb396099db4e0e04ac026c8df5/server/mvcc/kvstore_compaction.go#L54</a>)</td>
  </tr>
  <tr>
    <td></td>
    <td>"confState"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12962">Depuis etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"term"</td>
    <td></td>
    <td><a href="https://github.com/etcd-io/etcd/pull/12964">Depuis etcd 3.5</a></td>
  </tr>
  <tr>
    <td></td>
    <td>"storage-version"</td>
    <td></td>
    <td></td>
  </tr>
</table>


### Outils {#tools}


#### bbolt {#bbolt}

bbolt dispose d'un outil en ligne de commande permettant d'inspecter le contenu du fichier.

Exemples d'utilisation :

##### Lister tous les buckets dans le fichier bbolt donné : {#list-all-buckets-in-given-bbolt-file}

```
% go run go.etcd.io/bbolt/cmd/bbolt buckets ./default.etcd/member/snap/db
```


##### Lire une paire clé/valeur particulière : {#read-a-particular-keyvalue-pair}

```
% go run go.etcd.io/bbolt/cmd/bbolt get ./default.etcd/member/snap/db cluster clusterVersion
```


#### etcd-dump-db {#etcd-dump-db}

etcd-dump-db peut être utilisé pour lister le contenu du backend v3 d’etcd (bbolt).

```
% go run go.etcd.io/etcd/v3/tools/etcd-dump-db  list-bucket default.etcd
alarm
auth
...
```

Voir d'autres exemples dans : [https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-db)


## WAL : journal d'écriture anticipée {#wal-write-ahead-log}

Le journal d’écriture anticipée (Write ahead log) est un stockage persistant Raft utilisé pour stocker les propositions. Le leader stocke d’abord la proposition dans son journal, puis la réplique simultanément aux suiveurs à l’aide du protocole Raft. Chaque suiveur persiste la proposition dans son WAL avant de confirmer la réplication au leader.

Le journal WAL utilisé dans etcd diffère du modèle Raft canonique en deux sens :

*  Il persiste non seulement les entrées indexées, mais aussi les instantanés Raft (légers) et l’état dur. Ainsi, l’état Raft complet du membre peut être récupéré à partir du journal WAL seul.
*  Il fonctionne uniquement en ajout. Les entrées ne sont pas remplacées in situ, mais une entrée ajoutée ultérieurement dans le fichier (avec le même index) remplace la précédente.


### Noms de fichiers {#file-names}

Les fichiers de journal WAL sont nommés selon le motif suivant :

```
"%016x-%016x.wal", seq, index
```

Exemple : `./member/wal/0000000000000010-00000000000bf1e6.wal`

Ainsi, les noms de fichiers contiennent des chaînes codées en hexadécimal :


* Numéro séquentiel du fichier de journal WAL
* Index de la première entrée ou instantané dans le fichier.
    En particulier, le premier fichier « 0000000000000000-0000000000000000.wal » contient l’enregistrement initial d’instantané avec l’index=0.

### Contenu physique {#physical-content}

Le fichier de journal WAL contient une séquence de "[Frames](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L62)". Chaque trame contient :


1. [LittleEndian](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/encoder.go#L120)[^2] entier non signé 64 bits encodé qui contient la longueur de la structure [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) (3).
2. Remplissage : un certain nombre d'octets nuls, de manière à ce que la taille totale du cadre soit alignée (modulo 8)
3. Données marshallées [walpb.Record](https://github.com/etcd-io/etcd/blob/a1ff0d5373335665b3e5f4cb22a538ac63757cb6/server/wal/walpb/record.proto#L11) :
    1. [type](https://github.com/etcd-io/etcd/blob/aa97484166d2b3fb6afeb4390344e68b02afb566/server/storage/wal/wal.go#L39) - énumération entière codée déterminant l'interprétation du champ de données ci-dessous
    2. data - selon le type, généralement un message Protocol Buffers sérialisé
    3. crc - somme de contrôle CRC-32 de tous les champs « data » combinés (sans type) dans tous les enregistrements du journal sur cette réplique particulière depuis la création du journal WAL. Veuillez noter que la somme de contrôle prend en compte TOUS les enregistrements (même ceux qui n’ont pas été validés par Raft).

Les fichiers sont « coupés » (un nouveau fichier est créé) lorsque le fichier actuel dépasse <code>64*10^6</code> octets.


### Contenu logique {#logical-content}

Les fichiers de journal d'écriture anticipée dans la couche logique contiennent :

* `Raftpb.Entry: `propositions récentes répliquées par le leader Raft. Certaines de ces propositions sont considérées comme « validées », tandis que d'autres peuvent être logiquement remplacées.
* `Raftpb.HardState(term,commit,vote): `information périodique (très fréquente) sur l'index d'une entrée de journal qui est « validée » (répliquée sur la majorité des serveurs), garantissant ainsi qu'elle ne sera pas modifiée ou remplacée, et pouvant être appliquée aux backends (v2, v3). Elle contient également un « terme » (indicateur indiquant s'il y a eu des modifications liées à une élection) et un vote — le membre pour lequel la réplique actuelle a voté durant le terme en cours.
* `walpb.Snapshot(term, index): `instantanés périodiques de l’état Raft (aucun contenu de base de données, uniquement l’index du journal d’instantané et le terme Raft)
    * Le contenu du magasin V2 est stocké dans des fichiers *.store séparés.
    * Le contenu du magasin V3 est conservé dans le fichier bbolt, et devient un instantané implicite dès que les entrées y sont appliquées.
* enregistrement de somme de contrôle crc32 (au début de chaque fichier), utilisé pour reprendre le contrôle CRC pour le reste du fichier.
* `etcdserverpb.Metadata(node_id, cluster_id)` - identification du cluster et de la réplique représentés par le journal.

Chaque fichier de journal WAL est construit à partir de (dans l'ordre) :

1. CRC-32 (valeur CRC calculée sur tous les fichiers précédents, 0 pour le premier fichier).
2. Cadre de métadonnées (identifiants du cluster et de la réplique)
3. Uniquement pour le premier fichier WAL :

    * Trame d'instantané vide (Index : 0, Terme : 0).
        L'objectif de cette trame est de maintenir l'invariant selon lequel toutes les entrées sont « précédées » par un instantané.

   Pour le fichier WAL non initial (2e+ fichier) :

    * Trame HardState.

4. Mélange d'entrées, d'états durs et d'enregistrements d'instantané

Le journal WAL peut contenir plusieurs entrées pour l’index identique. Une telle situation peut survenir dans les cas décrits dans la figure 7 du document [Raft](http://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf). Le journal WAL d’etcd est uniquement ajouté, les entrées sont donc remplacées en ajoutant une nouvelle entrée portant le même index.

En particulier lors de la lecture du WAL, [la logique remplace les anciennes entrées par les nouvelles](https://github.com/etcd-io/etcd/blob/release-3.4/wal/wal.go#L448-L462). Ainsi, seule la dernière version des entrées dont entry.index &lt;= HardState.commit peut être considérée comme définitive. Les entrées dont l'index est supérieur à HardState.commit sont sujettes à modification.

Les « termes » dans le journal WAL sont censés être monotones.

Les « indexes » dans le journal WAL sont censés :

1. démarrer à partir d’un instantané
2. croître séquentiellement à partir de cet instantané tant qu’il reste dans le même « terme »
3. si le terme change, l’index peut diminuer, mais uniquement jusqu’à une nouvelle valeur supérieure à celle de HardState.commit
4. un nouvel instantané peut avoir lieu avec un index quelconque supérieur ou égal à HardState.commit, ce qui ouvre une nouvelle séquence pour les index


![fichiers de stockage persistant etcd](/docs/etcd/learning/img/persistent-storage-files-figure-01.png)


### Outils {#tools-1}


#### etcd-dump-logs {#etcd-dump-logs}

Les journaux WAL d'etcd peuvent être lus à l'aide de l'outil [etcd-dump-logs](https://github.com/etcd-io/etcd/tree/master/tools/etcd-dump-logs) :

```
% go install go.etcd.io/etcd/v3/tools/etcd-dump-logs@latest

% go run go.etcd.io/etcd/v3/tools/etcd-dump-logs --start-index=0 aname.etcd
```

Prenez note que :

* L'outil affiche uniquement les entrées, et non tous les enregistrements WAL (instantanés, HardStates) présents dans les fichiers de journal WAL.
* L'outil applique automatiquement des « substitutions » aux entrées. Si une entrée est remplacée (par une entrée plus récente au même index), l'outil n'affiche que la valeur finale.
* L'outil affiche également les entrées non validées (issues de la fin du LOG), sans information sur HardState.commitIndex, de sorte qu'il n'est pas possible de savoir si les entrées sont définitives ou non.


## Instantanés de (Store V2) : **member/snap/{term}-{index}.snap** {#snapshots-of-store-v2-membersnapterm-indexsnap}


### Noms de fichiers : {#file-names-1}

**member/snap/{term}-{index}.snap**

Les noms de fichiers sont générés [ici](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L78) `("%016x-%016x.snap") ` et utilisent deux composants encodés en hexadécimal :


* term -> Terme Raft (période entre les élections) au moment de l'émission de l'instantané
* index -> Index de la dernière proposition appliquée au moment de l'émission de l'instantané

### Création {#creation}

Les fichiers *.snap sont créés par la méthode [Snapshotter.SaveSnap](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snapshotter.go#L68).

Il existe 2 déclencheurs contrôlant la création de ces fichiers :


* Un nouveau fichier est créé toutes les --snapshot-count= propositions appliquées environ (10 000 par défaut dans v3.7.0). Cette valeur est approximative : les propositions peuvent arriver par lots, la création d'un instantané n'est envisagée qu'à la fin du lot et le processus est finalement planifié de manière asynchrone.
  Le nom de l'option (--snapshot-count) est assez trompeur : elle contrôle la [différence de valeur d’index](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/server.go#L1266) entre le dernier index d’instantané et le dernier index de proposition appliquée.
* Raft demande à la réplique de restaurer à partir de l'instantané. Pendant qu'une réplique reçoit l'instantané via le message msgSnap, il le sauvegarde également (de manière légère) dans le journal WAL. Cela garantit que dans la queue du journal WAL se trouve toujours un instantané valide suivi d'entrées. Cela supprime ainsi tout risque de discontinuité dans les journaux WAL.

Actuellement, les fichiers sont approximativement [^3] associés 1 à 1 aux entrées Snapshot des journaux WAL. Avec le décommissionnement du store v2, nous prévoyons que les fichiers ne seront plus écrits du tout (optionnel : 3.5.x, obligatoire : 3.6.x).


### Contenu {#content}

Le fichier contient un proto [snapdb.snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/server/etcdserver/api/snap/snappb/snap.proto#L11) `(uint32 crc, bytes data)` marshallé,

dont le champ 'data' contient [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31) :

(bytes data, SnapshotMetadata{index, term, [conf](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L99)} metadata),

Enfin, les données imbriquées contiennent un contenu [store v2](#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files) sérialisé au format JSON.


En particulier, il y a :

* Terme
* Index
* Données d'appartenance :
    *  <code>/0/members/8e9e05c52164694d/attributes -> <strong>{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}</strong></code>
    *  <code>/0/members/8e9e05c52164694d/RaftAttributes -> <strong>"{\"peerURLs\":[\"http://localhost:2380\"]}"</strong></code>
* Version du stockage : /0/version-> 3.5.0


### Outils {#tools-2}


#### protoc {#protoc}

La commande suivante vous permet de visualiser le contenu du fichier lorsqu'elle est exécutée depuis le répertoire racine d'etcd :


```
cat default.etcd/member/snap/0000000000000002-0000000000049425.snap |
  protoc --decode=snappb.snapshot \
    server/etcdserver/api/snap/snappb/snap.proto \
    -I $(go list -f '{{.Dir}}' github.com/gogo/protobuf/proto)/.. \
    -I . \
    -I $(go list -m -f '{{.Dir}}' github.com/gogo/protobuf)/protobuf
```


De même, vous pouvez extraire le champ 'data' et le décoder en tant que [Raftpb.Snapshot](https://github.com/etcd-io/etcd/blob/ad5b30297a43daeb5ce7311fa606ce4c1f16618f/raft/raftpb/raft.proto#L31).


### Exemple de contenu du magasin sérialisé JSON version 2 dans les fichiers *.snap d'etcd 3.4 : {#exemplar-json-serialized-store-v2-content-in-etcd-34-snap-files}

```json
{
  "Root":{
    "Path":"/",
    "CreatedIndex":0,
    "ModifiedIndex":0,
    "ExpireTime":"0001-01-01T00:00:00Z",
    "Value":"",
    "Children":{
      "0":{
        "Path":"/0",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{
          "members":{
            "Path":"/0/members",
            "CreatedIndex":1,
            "ModifiedIndex":1,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"",
            "Children":{
              "8e9e05c52164694d":{
                "Path":"/0/members/8e9e05c52164694d",
                "CreatedIndex":1,
                "ModifiedIndex":1,
                "ExpireTime":"0001-01-01T00:00:00Z",
                "Value":"",
                "Children":{
                  "attributes":{
                    "Path":"/0/members/8e9e05c52164694d/attributes",
                    "CreatedIndex":2,
                    "ModifiedIndex":2,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
                    "Children":null
                  },
                  "RaftAttributes":{
                    "Path":"/0/members/8e9e05c52164694d/RaftAttributes",
                    "CreatedIndex":1,
                    "ModifiedIndex":1,
                    "ExpireTime":"0001-01-01T00:00:00Z",
                    "Value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
                    "Children":null
                  }
                }
              }
            }
          },
          "version":{
            "Path":"/0/version",
            "CreatedIndex":3,
            "ModifiedIndex":3,
            "ExpireTime":"0001-01-01T00:00:00Z",
            "Value":"3.5.0",
            "Children":null
          }
        }
      },
      "1":{
        "Path":"/1",
        "CreatedIndex":0,
        "ModifiedIndex":0,
        "ExpireTime":"0001-01-01T00:00:00Z",
        "Value":"",
        "Children":{


        }
      }
    }
  },
  "WatcherHub":{
    "EventHistory":{
      "Queue":{
        "Events":[
          {
            "action":"create",
            "node":{
              "key":"/0/members/8e9e05c52164694d/RaftAttributes",
              "value":"{\"peerURLs\":[\"http://localhost:2380\"]}",
              "modifiedIndex":1,
              "createdIndex":1
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/members/8e9e05c52164694d/attributes",
              "value":"{\"name\":\"default\",\"clientURLs\":[\"http://localhost:2379\"]}",
              "modifiedIndex":2,
              "createdIndex":2
            }
          },
          {
            "action":"set",
            "node":{
              "key":"/0/version",
              "value":"3.5.0",
              "modifiedIndex":3,
              "createdIndex":3
            }
          }
        ]
      }
    }
  }
}
```

## Modifications {#changes}

Cette section est réservée à la description des modifications apportées aux formats de fichier introduits entre différentes versions d'etcd.

[^1]:
     Les pages de métadonnées situées au début du fichier bbolt sont modifiées in situ.

[^2]:
     Incohérent, car la majorité des uint sont écrits en big endian

[^3]:
     L'instantané initial (index : 0) au début du journal WAL n'est pas associé à un fichier *.snap. Les anciens fichiers *.snap (ou journaux WAL) peuvent être supprimés.
