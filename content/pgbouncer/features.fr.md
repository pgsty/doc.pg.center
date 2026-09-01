---
title: "Fonctionnalités"
weight: 10
description: "Fonctionnalités de PgBouncer — modes de pool et compatibilité SQL"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Concept]
aliases: [/docs/pgbouncer/features/]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- Plusieurs niveaux de sévérité lors de la rotation des connexions :

  **Pooling de sessions**
: Méthode la moins intrusive. Lorsqu’un client se connecte, une connexion serveur lui est attribuée pour toute la durée de sa connexion. Lorsque le client se déconnecte, la connexion serveur est remise dans le pool. Ce mode prend en charge toutes les fonctionnalités de PostgreSQL.

  **Pooling de transactions**
: Une connexion serveur est attribuée à un client uniquement pendant une transaction. Lorsque PgBouncer détecte la fin de la transaction, le serveur est remis dans le pool. Ce mode désactive quelques fonctionnalités basées sur la session de PostgreSQL. Vous ne pouvez l'utiliser que si l'application coopère en ne utilisant pas les fonctionnalités qui causent des incompatibilités. Consultez le tableau ci-dessous pour les fonctionnalités incompatibles.

  **Pooling d'instructions**
: Méthode la plus agressive. Il s'agit d'un pooling de transactions avec une particularité : les transactions à plusieurs instructions sont interdites. Cette configuration vise à imposer le mode « autocommit » sur le client, principalement destinée à PL/Proxy.

- Faibles besoins en mémoire (2 kB par connexion par défaut). Cela est dû au fait que PgBouncer n’a pas besoin de voir entièrement les paquets à la fois.

- Il n’est pas lié à un seul serveur backend. Les bases de données de destination peuvent résider sur des hôtes différents.

- Prise en charge de la reconfiguration en temps réel pour la plupart des paramètres.

- Prise en charge du redémarrage/mise à jour en direct sans interrompre les connexions clients.

--------

## Carte des fonctionnalités SQL pour les modes de mise en pool {#sql-feature-map-for-pooling-modes}

Le tableau suivant liste diverses fonctionnalités de PostgreSQL et indique leur compatibilité avec les modes de poolage de PgBouncer. Notez que le poolage *transactionnel* rompt délibérément les attentes du client concernant le serveur et ne peut être utilisé que si l'application coopère en ne faisant pas usage des fonctionnalités non prises en charge.

| Fonctionnalité                        | Pooling de sessions  | Pooling de transactions  |
|---------------------------------------|:--------------------:|:------------------------:|
| Paramètres de démarrage [^0]         | Oui                  | Oui                      |
| SET/RESET                             | Oui                  | Jamais                   |
| LISTEN                                | Oui                  | Jamais                   |
| NOTIFY                                | Oui                  | Oui                      |
| Curseur WITHOUT HOLD                  | Oui                  | Oui                      |
| Curseur WITH HOLD                     | Oui                  | Jamais                   |
| Plans préparés au niveau du protocole | Oui                  | Oui [^1]              |
| PREPARE / DEALLOCATE                  | Oui                  | Jamais                   |
| Suppression des tables temporaires ON COMMIT | Oui                  | Oui                      |
| Conservation/Suppression des lignes dans les tables temporaires | Oui                  | Jamais                   |
| Réinitialisation des plans mis en cache | Oui                  | Oui                      |
| Instruction LOAD                      | Oui                  | Jamais                   |
| Verrous d'advisory au niveau de la session | Oui                  | Jamais                   |

[^0]: Les paramètres de démarrage sont `client_encoding`, `DateStyle`, `IntervalStyle`, `Timezone`, `standard_conforming_strings` et `application_name`. PgBouncer détecte leurs modifications et peut ainsi garantir leur cohérence pour le client. Pour prendre en charge d'autres paramètres, consultez [`track_extra_parameters`](/fr/pgbouncer/config/#track_extra_parameters) et [`ignore_startup_parameters`](/fr/pgbouncer/config/#ignore_startup_parameters).

[^1]: Vous devez définir [`max_prepared_statements`](/fr/pgbouncer/config/#max_prepared_statements) sur une valeur non nulle pour activer cette prise en charge.
