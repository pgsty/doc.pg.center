---
title: "Considérations de sécurité"
weight: 160
icon: fa-solid fa-lock
description: "Considérations de sécurité pour DCS, l'API REST et la gestion des identifiants."
module: [PATRONI]
categories: [Concept]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Un cluster Patroni dispose de deux interfaces à protéger contre l'accès non autorisé : le stockage de configuration distribué (DCS) et l'API REST Patroni.

--------

## Protection du DCS {#protecting-dcs}

Patroni et [patronictl](/fr/patroni/patronictl#patronictl) stockent et récupèrent tous deux des données dans le DCS.

Même lorsque le DCS ne contient aucune information sensible, il permet de modifier certaines configurations de Patroni/PostgreSQL. Par conséquent, la première mesure à prendre est de protéger le DCS lui-même.

Les détails de protection dépendent du type de DCS utilisé. Les paramètres d'authentification et de chiffrement (jetons/authentification basique/certificats clients) pour les types de DCS pris en charge sont décrits dans les [paramètres de configuration](/fr/patroni/config/yaml#yaml).

La recommandation générale consiste à activer TLS pour toutes les communications DCS.

--------

## Protection de l'API REST {#protecting-the-rest-api}

Protéger l'API REST est une tâche plus complexe.

L'API REST de Patroni est utilisée par Patroni lui-même lors de la course au leader, par l'outil [patronictl](/fr/patroni/patronictl#patronictl) afin d'effectuer des basculements, des basculements planifiés, des réinitialisations, des redémarrages ou des rechargements, par HAProxy ou tout autre équilibreur de charge pour effectuer des vérifications de santé HTTP, et bien sûr également pour la surveillance.

Du point de vue de la sécurité, l'API REST contient des points d'accès sûrs (`GET` : requêtes qui ne font que récupérer des informations) et des points d'accès non sûrs (`PUT`, `POST`, `PATCH` et `DELETE` : requêtes qui modifient l'état des nœuds).

Les points d'accès non sûrs peuvent être protégés par une authentification HTTP basique en définissant les paramètres `restapi.authentication.username` et `restapi.authentication.password`. Il n'existe aucun moyen de protéger les points d'accès sûrs sans activer le TLS.

Lorsque le TLS pour l'API REST est activé et qu'une PKI est configurée, l'authentification mutuelle entre le serveur API et le client API est possible pour tous les points d'accès.

Les paramètres de la section `restapi` permettent l'authentification client TLS auprès du serveur. Selon la valeur du paramètre `verify_client`, le serveur API exige une vérification réussie du certificat client pour les appels d'API sûrs et non sûrs (`verify_client: required`), uniquement pour les appels d'API non sûrs (`verify_client: optional`), ou pour aucun appel d'API (`verify_client: none`).

Les paramètres de la section `ctl` permettent au client (l'outil [patronictl](/fr/patroni/patronictl#patronictl), qui utilise la même configuration que Patroni) d'authentifier le serveur TLS. Définissez `insecure: true` pour désactiver la vérification du certificat serveur par le client. Consultez les [paramètres de configuration](/fr/patroni/config/yaml#patronictl_settings) pour une description détaillée des paramètres TLS client.

Protéger la base de données PostgreSQL elle-même contre l'accès non autorisé est hors du champ de ce document et est traité dans <https://www.postgresql.org/docs/current/client-authentication.html>.
