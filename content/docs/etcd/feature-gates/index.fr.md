---
title: Portes fonctionnelles
weight: 1175
icon: fa-solid fa-toggle-on
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/feature-gates/index.md"
aliases: [/etcd/feature-gates/]
---

<!-- overview -->
Cette page présente un aperçu des diverses options de fonctionnalité qu’un administrateur peut spécifier sur etcd.

Voir [étapes du fonctionnement](#feature-stages) pour une explication des étapes d'une fonctionnalité.

<!-- body -->
## Aperçu {#overview}

Les portes fonctionnelles sont un ensemble de paires clé=valeur qui décrivent les fonctionnalités d'etcd.
Vous pouvez activer ou désactiver ces fonctionnalités à l'aide du drapeau de ligne de commande `--feature-gates` sur etcd.

etcd vous permet d'activer ou de désactiver un ensemble de fonctionnalités expérimentales.
Utilisez le drapeau `-h` pour afficher la liste complète des fonctionnalités expérimentales.
Pour définir les fonctionnalités expérimentales, utilisez le drapeau `--feature-gates` avec une liste de paires fonctionnalité=valeur en ligne de commande :

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

Ou spécifiez `feature-gates` dans le fichier de configuration YAML :

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### Modification de la structure `embed.EtcdServer` {#change-in-embedetcdserver-struct}

En 3.6, le champ `ServerFeatureGate` est ajouté à `embed.Config`, et doit remplacer les champs expérimentaux ci-dessous :

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### Portes d’activation pour les fonctionnalités Alpha ou Beta {#feature-gates-for-alpha-or-beta-features}

Les tableaux suivants résumé les portes de fonctionnalité que vous pouvez activer sur etcd.

| Fonctionnalité                     | Valeur par défaut | Étape   | Détails                                                                                                                             |
|------------------------------------|-------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------|
| CompactHashCheck                   | false             | Alpha   | Active la vérification de corruption des données avant de servir tout trafic client/peer.                                                                 |
| InitialCorruptCheck                | false             | Alpha   | Active la vérification périodique par le leader des hachages de compactage des suiveurs.                                                                 |
| LeaseCheckpoint                    | false             | Alpha   | Active l'envoi de points de contrôle réguliers par le leader aux autres membres afin d'éviter la réinitialisation du TTL restant lors d'un changement de leader. |
| LeaseCheckpointPersist             | false             | Alpha   | Active la persistance du TTL restant afin d'éviter une auto-renouvellement indéfini des bails longs.                                                                 |
| SetMemberLocalAddr                 | false             | Alpha   | Active l'utilisation de la première adresse locale non boucle spécifiée dans initial-advertise-peer-urls comme adresse locale lors de la communication avec un pair. |
| StopGRPCServiceOnDefrag            | false             | Alpha   | Active l'arrêt du service gRPC etcd lors de la défragmentation afin de ne plus servir les requêtes clients.                                                                 |
| TxnModeWriteWithSharedBuffer       | true              | Beta    | Active l'utilisation d'un tampon partagé lors des opérations de vérification en lecture seule dans les transactions d'écriture.                                                                 |

## Utilisation d'une fonctionnalité {#using-a-feature}

### Stades des fonctionnalités {#feature-stages}

Une fonctionnalité peut être à l’étape *Alpha*, *Beta*, *GA* ou *Deprecated*.
Une fonctionnalité *Alpha* signifie :

*  Désactivé par défaut.
*  Peut présenter des bugs. L'activation de cette fonctionnalité peut exposer des bugs.
*  Le support de cette fonctionnalité peut être supprimé à tout moment sans préavis.
*  L'API peut évoluer de manière incompatible dans une version logicielle ultérieure sans préavis.
*  Recommandé pour une utilisation uniquement dans des clusters de test à durée limitée, en raison de risques accrus de bugs et du manque de support à long terme.

Une fonctionnalité *Beta* signifie :

* Activé par défaut.
* La fonctionnalité est bien testée. Son activation est considérée comme sûre.
* Le support de la fonctionnalité globale ne sera pas supprimé, bien que les détails puissent évoluer.
* Recommandé uniquement pour des utilisations non critiques pour l'activité car il existe un risque de découverte de bogues difficiles à détecter grâce à une adoption plus large.

> [!NOTE]
> N'hésitez pas à essayer les fonctionnalités *Beta* et à nous faire part de vos retours !
> Une fois sorties de la phase bêta, il se peut qu'il ne soit plus pratique pour nous d'apporter davantage de modifications.

Une fonctionnalité *General Availability* (GA) est également appelée fonctionnalité *stable*. Cela signifie :

* La fonctionnalité est toujours activée ; vous ne pouvez pas la désactiver.
* La porte de fonction correspondante n'est plus nécessaire.
* Les versions stables des fonctionnalités apparaîtront dans les logiciels publiés pendant de nombreuses versions ultérieures.

Une fonctionnalité *Deprecated* signifie :

* La porte de fonctionnalité n'est plus utilisée.
* La fonctionnalité a atteint le stade GA ou a été supprimée.
