---
title: Conventions de journalisation
weight: 1600
description: Catégories de niveau de journalisation
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/logging.md"
aliases: [/etcd/dev-internal/logging/]
---

etcd utilise la bibliothèque [zap][zap] pour la journalisation de la sortie de l'application, catégorisée en *niveaux*. Le niveau d'un message de journalisation est déterminé selon les conventions suivantes :

* Les journaux DebugLevel sont généralement volumineux et sont habituellement désactivés en production.
  * Exemples :
    * Envoyer un message normal à un pair distant
    * Écrire une entrée de journal sur le disque

* InfoLevel est la priorité de journalisation par défaut.
  * Exemples :
    * Configuration au démarrage
    * Commencer à effectuer un instantané
    * Ajouter un nouveau nœud au cluster
    * Ajouter un nouvel utilisateur au sous-système d'authentification

* Les journaux WarnLevel sont plus importants que ceux de niveau Info, mais ne nécessitent pas de revue humaine individuelle.
  * Exemples :
    * Échec de l’envoi d’un message Raft à un pair distant
    * Échec de réception d’un message de battement de cœur dans le délai d’élection configuré

* Les journaux ErrorLevel sont de haute priorité. Si une application fonctionne correctement, elle ne devrait générer aucun journal de niveau erreur.
  * Exemples :
    * Échec de l'allocation d'espace disque pour le WAL

* PanicLevel enregistre un message, puis déclenche une panique.
  * Exemples :
    * Échec du codage des messages Raft

* FatalLevel enregistre un message, puis appelle os.Exit(1).
  * Exemples :
    * Échec de la sauvegarde de l'instantané Raft

[zap]: https://github.com/uber-go/zap
