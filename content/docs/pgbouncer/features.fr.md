---
title: "Fonctionnalités"
weight: 10
description: "Fonctionnalités de PgBouncer — modes de pooling et compatibilité SQL"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Concept]
aliases: [/pgbouncer/features/]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- Plusieurs niveaux de sévérité lors de la rotation des connexions :

  **Pooling de sessions**
  : Méthode la moins intrusive. Lorsqu’un client se connecte, une connexion serveur lui est attribuée pour toute la durée de sa connexion. Lorsque le client se déconnecte, la connexion serveur est remise dans le pool. Ce mode prend en charge toutes les fonctionnalités de PostgreSQL.

  **Pooling de transactions**
  : Une connexion serveur est attribuée à un client uniquement pendant une transaction. Lorsque PgBouncer détecte la fin de la transaction, elle est remise dans le pool. Ce mode est incompatible avec certaines fonctionnalités de PostgreSQL liées à la session. Il ne peut être utilisé que si l'application évite ces fonctionnalités, répertoriées dans le tableau ci-dessous.

  **Pooling d'instructions**
  : Méthode la plus agressive. Il s'agit d'un pooling de transactions avec une particularité : les transactions à plusieurs instructions sont interdites. Ce mode vise à imposer le fonctionnement en « autocommit » côté client et s'adresse principalement à PL/Proxy.

- Faibles besoins en mémoire (2 kB par connexion par défaut), car PgBouncer n'a pas besoin de lire chaque paquet en entier d'un seul coup.

- Il n’est pas lié à un seul serveur backend. Les bases de données de destination peuvent résider sur des hôtes différents.

- Prise en charge de la reconfiguration à chaud pour la plupart des paramètres.

- Prise en charge des [redémarrages et mises à niveau progressifs](/fr/docs/pgbouncer/usage/#shutdown-wait_for_clients) à l'aide de plusieurs processus avec [`so_reuseport`](/fr/docs/pgbouncer/config/#so_reuseport). L'ancien redémarrage en ligne (`-R`) a été supprimé dans la version 1.26.0.

--------

## Carte des fonctionnalités SQL pour les modes de pooling {#sql-feature-map-for-pooling-modes}

Le tableau suivant répertorie plusieurs fonctionnalités de PostgreSQL et leur compatibilité avec les modes de pooling de PgBouncer. Le pooling de *transactions* modifie *par conception* le comportement du serveur attendu par le client. Il ne peut donc être utilisé que si l'application évite les fonctionnalités incompatibles.

| Fonctionnalité                        | Pooling de sessions  | Pooling de transactions  |
|---------------------------------------|:--------------------:|:------------------------:|
| Paramètres de démarrage [^0]         | Oui                  | Oui                      |
| SET/RESET                             | Oui                  | Pour les paramètres suivis [^0] |
| LISTEN                                | Oui                  | Jamais                   |
| NOTIFY                                | Oui                  | Oui                      |
| WITHOUT HOLD CURSOR                  | Oui                  | Oui                      |
| WITH HOLD CURSOR                     | Oui                  | Jamais                   |
| Plans préparés au niveau du protocole | Oui                  | Oui [^1]              |
| PREPARE / DEALLOCATE                  | Oui                  | Jamais                   |
| Tables temporaires ON COMMIT DROP   | Oui                  | Oui                      |
| Tables temporaires PRESERVE/DELETE ROWS | Oui                  | Jamais                   |
| Réinitialisation des plans mis en cache | Oui                  | Oui                      |
| Instruction LOAD                      | Oui                  | Jamais                   |
| Verrous advisory au niveau de la session | Oui                  | Jamais                   |

[^0]: Depuis la version 1.26.0, PgBouncer suit tous les paramètres signalés par le serveur que les clients peuvent modifier : `application_name`, `client_encoding`, `DateStyle`, `default_transaction_read_only` (PostgreSQL 14+), `IntervalStyle`, `scram_iterations` (PostgreSQL 16+), `search_path` (PostgreSQL 18+), `session_authorization`, `standard_conforming_strings` et `TimeZone`. Pour les paramètres que le serveur ne signale pas, seules les valeurs de démarrage sont suivies ; les modifications ultérieures par `SET` ne le sont pas. Consultez [`track_extra_parameters`](/fr/docs/pgbouncer/config/#track_extra_parameters) et [`ignore_startup_parameters`](/fr/docs/pgbouncer/config/#ignore_startup_parameters) pour plus de détails et pour les paramètres fournis par des extensions.

[^1]: La prise en charge des requêtes préparées au niveau du protocole est activée lorsque [`max_prepared_statements`](/fr/docs/pgbouncer/config/#max_prepared_statements) est non nul. La valeur par défaut est 200 ; la définir à 0 désactive cette prise en charge. `PREPARE` / `DEALLOCATE` au niveau SQL reste incompatible avec le pooling de transactions, à l'exception de `DEALLOCATE ALL` et `DISCARD ALL` lorsque le suivi est activé.
