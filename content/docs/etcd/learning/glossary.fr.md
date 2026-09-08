---
title: Glossaire
weight: 2900
description: "Termes utilisés dans la documentation, la ligne de commande et le code source d'etcd"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/glossary.md"
aliases: [/etcd/learning/glossary/]
---

Ce document définit les différents termes utilisés dans la documentation, la ligne de commande et le code source d’etcd.

## Alarme {#alarm}

Le serveur etcd déclenche une alarme chaque fois que le cluster nécessite une intervention opérationnelle pour rester fiable.

## Authentification {#authentication}

L’authentification gère les autorisations d’accès des utilisateurs aux ressources etcd.

## Client {#client}

Un client se connecte au cluster etcd pour émettre des requêtes de service, telles que la récupération de paires clé-valeur, l'écriture de données ou la surveillance des mises à jour.

## cluster {#cluster}

Un cluster se compose de plusieurs membres.

Le nœud de chaque membre suit le protocole de consensus Raft pour répliquer les journaux. Le cluster reçoit des propositions des membres, les valide et les applique au magasin local.

## compactage {#compaction}

Le compactage supprime l'historique des événements et les clés obsolètes antérieures à une révision donnée. Il permet de libérer de l'espace de stockage dans la base de données backend d'etcd.

## Élection {#election}

Le cluster etcd organise des élections parmi ses membres afin de choisir un leader, conformément au protocole de consensus Raft.

## Point de terminaison {#endpoint}

Une URL pointant vers un service ou une ressource etcd.

## Clé {#key}

Identifiant défini par l'utilisateur pour le stockage et la récupération de valeurs définies par l'utilisateur dans etcd.

## Plage de clés {#key-range}

Un ensemble de clés contenant soit une clé individuelle, soit un intervalle lexicographique pour toutes les clés x telles que a < x <= b, soit toutes les clés supérieures à une clé donnée.

## espace de clés {#keyspace}

L'ensemble de toutes les clés dans un cluster etcd.

## bail {#lease}

Contrat renouvelable à courte durée qui supprime les clés associées à celui-ci à l'expiration.

## membre {#member}

Un serveur etcd logique participant au service d'un cluster etcd.

## Révision de modification {#modification-revision}

La première révision à contenir la dernière écriture sur une clé donnée.

## Pair {#peer}

Le pair est un autre membre du même cluster.

## Proposition {#proposal}

Une proposition est une demande (par exemple, une demande d'écriture, une demande de modification de configuration) qui doit passer par le protocole Raft.

## quorum {#quorum}

Nombre de membres actifs nécessaires pour atteindre un consensus afin de modifier l'état du cluster. etcd exige une majorité de membres pour atteindre le quorum.

## révision {#revision}

Compteur global sur 64 bits, initialisé à 1 et incrémenté à chaque modification de l’espace de clés.

## Rôle {#role}

Unité de permissions sur un ensemble de plages de clés, pouvant être attribuée à un ensemble d'utilisateurs pour le contrôle d'accès.

## instantané {#snapshot}

Une sauvegarde instantanée de l’état du cluster etcd.

## Stockage {#store}

Le stockage physique sous-jacent à l'espace de clés du cluster.

## Terme {#term}

Un terme est un entier strictement croissant associé à chaque élection de leader dans l'algorithme Raft.
Pour un terme donné, il ne peut y avoir qu'un seul leader élu, et le terme est incrémenté lors d'un changement de leader.

## Transaction {#transaction}

Opération en série exécutée de manière atomique. Toutes les clés modifiées au sein d'une transaction partagent la même révision de modification.

## Version de la clé {#key-version}

Le nombre d'écritures effectuées sur une clé depuis sa création, à compter de 1. La version d'une clé inexistante ou supprimée est 0.

## observateur {#watcher}

Un client ouvre un observateur pour surveiller les mises à jour sur une plage de clés donnée.
