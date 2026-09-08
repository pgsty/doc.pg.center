---
title: "Journal des modifications"
weight: 70
description: "Historique des versions et notes de publication de PgBouncer"
icon: fa-solid fa-scroll
module: [PGBOUNCER]
categories: [Référence]
aliases: [/pgbouncer/changelog/]
upstream_link: "https://www.pgbouncer.org/changelog.html"
---

--------

## PgBouncer 1.25.x {#pgbouncer-125x}

**2026-05-08  -  PgBouncer 1.25.2  -  "Touch humain avec une touche fraîche dans la course au titre pleine d'incertitudes**

- Sécurité
  * Correctif CVE-2026-6664 : Une dépassement d'entier dans le code de traitement des paquets réseau de PgBouncer antérieur à la version 1.25.2 contourne une vérification de borne et peut entraîner un crash. Un attaquant distant non authentifié peut provoquer un crash de PgBouncer en envoyant un paquet d'authentification SCRAM malformé.
  * Correctif CVE-2026-6665 : Le code SCRAM de PgBouncer antérieur à la version 1.25.2 ne vérifiait pas correctement la valeur de retour de `strlcat()` lors de la construction du contenu du message client-final SCRAM. Un serveur malveillant pouvant envoyer un message serveur-final SCRAM avec un nonce long peut déclencher un dépassement de pile.
  * Correctif CVE-2026-6666 : Une référence vers un pointeur nul possible dans PgBouncer antérieur à la version 1.25.2 pouvait entraîner un crash si un serveur envoyait une réponse d'erreur sans champ SQLSTATE.
  * Correctif CVE-2026-6667 : PgBouncer antérieur à la version 1.25.2 n'effectuait pas de vérification d'autorisation appropriée pour la commande `KILL_CLIENT`. Tous les utilisateurs ayant accès à la console d'administration, qui nécessite elle-même une authentification, pouvaient exécuter cette commande. Cette opération doit uniquement être autorisée pour les utilisateurs listés dans le paramètre `admin_users`.

- Correctifs
  * Précision de la documentation du paramètre `default_pool_size`.
  * Correction de la documentation pour `client_tls13_ciphers` et `server_tls13_ciphers`.

**2025-12-03  -  PgBouncer 1.25.1  -  « Correction de plusieurs bogues avant Noël »**

- Sécurité
  * Correction de CVE-2025-12819 : avant cette version, il était possible à un attaquant non authentifié d'exécuter du SQL arbitraire pendant l'authentification en fournissant un paramètre search_path malveillant dans le message StartupMessage. Les systèmes présentant TOUS les paramètres suivants sont vulnérables :

    1. `track_extra_parameters` inclut search_path (configuration non par défaut, probablement configurée uniquement dans les environnements utilisant Citus ou PostgreSQL 18)
    2. `auth_user` est défini sur une chaîne non vide (configuration non par défaut)
    3. `auth_query` est configuré sans noms d'objets qualifiés (configuration par défaut, l'opérateur < n'est pas qualifié par schéma)

- Correctifs
    - Corrige les erreurs d'authentification SCRAM ad-hoc après une reconnexion au serveur ([#1432], introduit dans 1.25.0)
    - Ajoute les typedef manquants pour les architectures exotiques sans prise en charge SIMD ([#1414], introduit dans 1.25.0)
    - Supprime l'avertissement bruyant dans les journaux lorsqu'un client ferme la connexion avant d'envoyer des données ([#1420], introduit dans 1.25.0)
    - Empêche une éventuelle déréférencement de pointeur nul ([#1423], introduit dans 1.25.0)
    - Corrige une éventuelle fuite mémoire ([#1422], introduit dans 1.25.0)
    - Corrige l'analyse SCRAM des messages du serveur ([#1431], introduit dans 1.25.0)

[#1414]: https://github.com/pgbouncer/pgbouncer/pull/1414
[#1420]: https://github.com/pgbouncer/pgbouncer/pull/1420
[#1422]: https://github.com/pgbouncer/pgbouncer/pull/1422
[#1423]: https://github.com/pgbouncer/pgbouncer/pull/1423
[#1431]: https://github.com/pgbouncer/pgbouncer/pull/1431
[#1432]: https://github.com/pgbouncer/pgbouncer/pull/1432

**2025-11-09  -  PgBouncer 1.25.0  -  « Le version avec le support LDAP »**

- Fonctionnalités
    * Ajouter l'authentification LDAP ! Vous pouvez la configurer à l'aide d'un fichier HBA ou à l'aide de `auth_ldap_options`. ([#731])
    * Ajouter la prise en charge des connexions TLS côté client. Cela permet aux clients d'utiliser la mise en place plus rapide de la connexion TLS introduite dans PostgreSQL 17. PgBouncer ne peut pas (pour l'instant) se connecter aux serveurs PostgreSQL en utilisant cette mise en place plus rapide. ([#1359])
    * Ajouter l'état inactif à `SHOW CLIENTS`. ([#1191])
    * Ajouter le paramètre `transaction_timeout`, tant au niveau global qu'au niveau de l'utilisateur. ([#1242])
    * Envoyer un message NOTICE au client s'il est mis en file d'attente sans recevoir de connexion pendant plus de 5 secondes. Cette durée peut être modifiée ou désactivée à l'aide de `query_wait_notify`. ([#1264])
    * Ajouter le paramètre `scram_iterations` pour permettre aux opérateurs d'opter pour une vitesse d'authentification au détriment de la sécurité. ([#1339])
    * Ajouter `client_tls13_ciphers` et `server_tls13_ciphers` pour choisir les suites de chiffrement TLSv1.3 à activer. ([#1352])
- Modifications
    * Améliorer considérablement les performances de l'authentification SCRAM ad hoc. ([#1338])
    * Permettre à `KILL` de ne pas spécifier de base de données, ce qui signifie désormais `KILL` toutes les bases de données. ([#1317])
    * La requête de vérification de santé passe par défaut à l'envoi d'une requête vide au lieu de `SELECT 1`. ([#1233])
    * Consigner l'intégralité de la file d'attente PAM comme avertissement. Cela facilite la recherche de la cause des requêtes lentes provoquées par celle-ci. ([#1297])
    * La commande `RELOAD` indique désormais tout erreur survenue lors du rechargement. ([#1231])
    * Activer l'accès au socket UNIX de PgBouncer pendant l'arrêt pour les connexions administratives. Cela facilite pour l'opérateur de déterminer pourquoi un processus PgBouncer ne s'arrête pas et/ou d'exécuter manuellement `KILL_CLIENT` pour les connexions bloquées. ([#1305])
    * Modifier `mkauth.py` pour ne plus ajouter de troisième champ obsolète. ([#1365])
    * Améliorer les messages de `FATAL` dans les fonctions `disconnect_client` et `disconnect_server`. ([#1382])
    * Arrêter l'utilisation de la fonction OpenSSL obsolète `EVP_PKEY_get0_EC_KEY`. Cela pourrait provoquer des problèmes avec certaines implémentations FIPS. ([#1384])
- Correctifs
    * Corriger la panne liée aux mots de passe longs (1024 caractères ou plus). ([#1215])
    * Corriger les connexions multi-hôtes lors de l'utilisation de `server_tls_sslmode=verify-full`. ([#1303])
    * Corriger une erreur rare `FATAL` lors du transfert de demandes d'annulation. ([#1383])
    * Corriger le tri des paramètres dans `SHOW CONFIG`. ([#1403])
    * Renforcer l'analyse du paquet de démarrage. ([#1407])

[#731]: https://github.com/pgbouncer/pgbouncer/pull/731
[#1191]: https://github.com/pgbouncer/pgbouncer/pull/1191
[#1215]: https://github.com/pgbouncer/pgbouncer/pull/1215
[#1231]: https://github.com/pgbouncer/pgbouncer/pull/1231
[#1233]: https://github.com/pgbouncer/pgbouncer/pull/1233
[#1242]: https://github.com/pgbouncer/pgbouncer/pull/1242
[#1264]: https://github.com/pgbouncer/pgbouncer/pull/1264
[#1297]: https://github.com/pgbouncer/pgbouncer/pull/1297
[#1303]: https://github.com/pgbouncer/pgbouncer/pull/1303
[#1305]: https://github.com/pgbouncer/pgbouncer/pull/1305
[#1317]: https://github.com/pgbouncer/pgbouncer/pull/1317
[#1338]: https://github.com/pgbouncer/pgbouncer/pull/1338
[#1339]: https://github.com/pgbouncer/pgbouncer/pull/1339
[#1352]: https://github.com/pgbouncer/pgbouncer/pull/1352
[#1359]: https://github.com/pgbouncer/pgbouncer/pull/1359
[#1365]: https://github.com/pgbouncer/pgbouncer/pull/1365
[#1382]: https://github.com/pgbouncer/pgbouncer/pull/1382
[#1383]: https://github.com/pgbouncer/pgbouncer/pull/1383
[#1384]: https://github.com/pgbouncer/pgbouncer/pull/1384
[#1403]: https://github.com/pgbouncer/pgbouncer/pull/1403
[#1407]: https://github.com/pgbouncer/pgbouncer/pull/1407

--------

## PgBouncer 1.24.x {#pgbouncer-124x}

**2025-04-16  -  PgBouncer 1.24.1  -  « CVE-2025-2291 VALIDE JUSQU’À hier »**

- Sécurité
  * Correction de CVE-2025-2291 : auparavant, PgBouncer ne tenait pas compte de la clause VALID UNTIL d'un mot de passe lors de la requête des hachages de mot de passe via son auth_query. Ainsi, si PgBouncer était utilisé comme proxy transparent devant Postgres, il pouvait autoriser des mots de passe ayant déjà expiré. Pour résoudre ce problème, la requête d'authentification par défaut ainsi que les exemples de fonctions d'authentification personnalisées dans la documentation ont été mis à jour pour prendre en compte VALID UNTIL. Si vous utilisez une auth_query personnalisée, vous devez la mettre à jour en conséquence. Si vous utilisez la requête d'authentification par défaut, vous pouvez soit mettre à jour vers PgBouncer 1.24.1, soit modifier votre configuration pour utiliser la nouvelle requête d'authentification par défaut sur une version antérieure de PgBouncer.

- Correctifs
  * Corrige la prise en charge de PAM en revenant à la prise en charge de l'authentification `pam` dans le fichier HBA. ([#1291]) (bug introduit dans la version 1.24.0)
  * Corrige le bug sur la diminution du compteur de connexions utilisateur. Ce correctif était inclus dans l'étiquette 1.24.0 sur GitHub, mais le paquet de version ne le contenait pas. ([#1238]) (bug introduit dans la version 1.24.0)
  * Ajoute `test_load_balance_hosts.py` au paquet tarball. ([#1282])
  * Corrige les problèmes de tests afin de permettre leur exécution par les paquettisateurs Debian. ([#1266], [#1250])

- Documentation
  * Mettre à jour l'`auth_query` exemple pour définir un `search_path` sûr. ([#1245])

[#1238]: https://github.com/pgbouncer/pgbouncer/pull/1238
[#1291]: https://github.com/pgbouncer/pgbouncer/pull/1291
[#1282]: https://github.com/pgbouncer/pgbouncer/pull/1282
[#1266]: https://github.com/pgbouncer/pgbouncer/pull/1266
[#1250]: https://github.com/pgbouncer/pgbouncer/pull/1250
[#1245]: https://github.com/pgbouncer/pgbouncer/pull/1245

**2025-01-10  -  PgBouncer 1.24.0  -  « Nouvelle année, nouveau bouncer »**

- Fonctionnalités
  * Ajouter la prise en charge de `Type=notify-reload` pour systemd. Cela nécessite systemd
    version 253 ou ultérieure. ([#1148])
  * Ajouter la commande `KILL_CLIENT` à la console d'administration. Cela permet de terminer
    une connexion client par force. ([#1147])
  * Ajouter le paramètre `max_user_client_connections`, tant au niveau global qu'au niveau utilisateur. ([#1137])
  * Ajouter le paramètre `max_db_client_connections`, tant au niveau global qu'au niveau base de données. ([#1138])
  * Ajouter le compteur `current_client_connections` à la sortie de `SHOW USERS` et `SHOW DATABASES`. ([#1137], [#1138])
  * Ajouter le paramètre `load_balance_hosts`, pour prendre en charge **non** le load balancing entre hôtes. ([#736])
  * Exposer les compteurs d'utilisation des requêtes préparées dans `SHOW STATS`. ([#1192])
  * Ajouter le paramètre `client_idle_timeout`. ([#1189])
  * Ajouter au niveau utilisateur les paramètres `query_timeout` et `reserve_pool_size`. ([#1180], [#1228])
  * Activer la prise en charge de l'authentification `pam` dans le fichier HBA. ([#326])

- Changements
  * Ne pas réutiliser les connexions lors d’un RELOAD si la configuration TLS est inchangée. Auparavant, si vous aviez des connexions TLS, toutes étaient réinitialisées lors d’un RELOAD, ce qui pouvait entraîner une dégradation temporaire mais importante des performances. À présent, cela n’arrive que lorsque les paramètres TLS sont réellement modifiés. ([#1157])
  * Activer la prise en charge des requêtes préparées par défaut, `max_prepared_statements` est désormais défini à 200 par défaut. Ce changement de valeur par défaut ne devrait affecter que les clients qui utilisent réellement des requêtes préparées. Si vous utilisez des requêtes préparées, il est recommandé de consulter les limitations de cette fonctionnalité dans [notre documentation][prepared-docs]. ([#1144])
  * Les sockets, clients et serveurs peuvent désormais être identifiés par un ID unique dans la sortie d’administration. Auparavant, ils pouvaient être identifiés par leur pointeur, mais ces derniers étaient souvent réutilisés par de nouveaux clients après déconnexion. ([#1172])
  * Message d’erreur plus clair en cas de fichier pid vide. ([#1195])
  * Renvoyer l’erreur d’origine au client en cas d’échec de `server_login_retry`. ([#1152])
  * Consigner l’erreur d’origine du serveur en cas d’erreur provenant de `auth_query`. ([#1187])
  * Définir `default_pool_size` à 0 signifie une taille illimitée. ([#1227])
  * Changer le nom du paramètre `reserve_pool` pour les bases de données en `reserve_pool_size`. Le nom précédent reste une alias du nouveau nom. ([#1232])

- Correctifs
  * Amélioration de la gestion de divers cas d'erreur peu probables, tels que les erreurs de mémoire (OOM). Ces erreurs pouvaient auparavant provoquer des plantages ou des fuites mémoire. ([#1108], [#1101], [#1099], [#1169], [#1202])
  * Correction de la valeur par défaut de `server_tls_sslmode` dans le fichier de configuration d'exemple. ([#1133])
  * Suppression de la mention dans la documentation d'un alias non valide pour `server_tls_protocols`. ([#1155])
  * Correction d'un bogue survenant lors de l'utilisation combinée de `auth_query` et des connexions de réplication. Ce bogue pouvait entraîner des échecs de connexion dans de tels environnements. ([#1166])
  * Ignorer les requêtes d'annulation du client pendant que PgBouncer configure les paramètres du serveur. ([#298])

[prepared-docs]: /fr/docs/pgbouncer/config/#max_prepared_statements

[#1148]: https://github.com/pgbouncer/pgbouncer/pull/1148
[#1147]: https://github.com/pgbouncer/pgbouncer/pull/1147
[#1137]: https://github.com/pgbouncer/pgbouncer/pull/1137
[#1138]: https://github.com/pgbouncer/pgbouncer/pull/1138
[#736]: https://github.com/pgbouncer/pgbouncer/pull/736
[#1192]: https://github.com/pgbouncer/pgbouncer/pull/1192
[#1189]: https://github.com/pgbouncer/pgbouncer/pull/1189
[#1180]: https://github.com/pgbouncer/pgbouncer/pull/1180
[#1228]: https://github.com/pgbouncer/pgbouncer/pull/1228
[#326]: https://github.com/pgbouncer/pgbouncer/pull/326
[#1157]: https://github.com/pgbouncer/pgbouncer/pull/1157
[#1144]: https://github.com/pgbouncer/pgbouncer/pull/1144
[#1172]: https://github.com/pgbouncer/pgbouncer/pull/1172
[#1195]: https://github.com/pgbouncer/pgbouncer/pull/1195
[#1152]: https://github.com/pgbouncer/pgbouncer/pull/1152
[#1187]: https://github.com/pgbouncer/pgbouncer/pull/1187
[#1227]: https://github.com/pgbouncer/pgbouncer/pull/1227
[#1232]: https://github.com/pgbouncer/pgbouncer/pull/1232
[#1108]: https://github.com/pgbouncer/pgbouncer/pull/1108
[#1101]: https://github.com/pgbouncer/pgbouncer/pull/1101
[#1099]: https://github.com/pgbouncer/pgbouncer/pull/1099
[#1169]: https://github.com/pgbouncer/pgbouncer/pull/1169
[#1202]: https://github.com/pgbouncer/pgbouncer/pull/1202
[#1133]: https://github.com/pgbouncer/pgbouncer/pull/1133
[#1155]: https://github.com/pgbouncer/pgbouncer/pull/1155
[#1166]: https://github.com/pgbouncer/pgbouncer/pull/1166
[#298]: https://github.com/pgbouncer/pgbouncer/pull/298

--------

## PgBouncer 1.23.x {#pgbouncer-123x}

**2024-08-02  -  PgBouncer 1.23.1  -  « Tout est remis en ordre »**

- Correctifs
  * Corriger un éventuel plantage par segmentation après le rechargement de la configuration de PgBouncer. ([#1105]) (bug introduit dans la version 1.23.0)
  * Corriger tous les plantages connus liés à put_in_order. ([#1120])
    (de nouveaux plantages ont été introduits dans la version 1.23.0)
  * Ajouter les fichiers manquants au fichier tar de la version qui sont nécessaires pour les tests.
    ([#1124]) (les fichiers manquants ont été introduits dans la version 1.23.0)

[#1120]: https://github.com/pgbouncer/pgbouncer/pull/1120
[#1105]: https://github.com/pgbouncer/pgbouncer/pull/1105
[#1124]: https://github.com/pgbouncer/pgbouncer/pull/1124

**2024-07-03  -  PgBouncer 1.23.0  -  « Vers de nouveaux débuts »**

- Fonctionnalités
  * Ajout du support des redémarrages progressifs. Le signal SIGTERM ne provoque plus l'arrêt immédiat du processus PgBouncer. Il effectue désormais une « fermeture très sécurisée » : il attend que tous les clients se déconnectent avant de s'arrêter. Ce nouveau comportement de SIGTERM permet les redémarrages progressifs de plusieurs processus PgBouncer derrière un équilibreur de charge, ou écoutant sur le même port à l'aide de `so_reuseport`.
Il s'agit d'une **modification mineure rétroactive**. Si vous comptiez sur le comportement ancien de SIGTERM dans votre Dockerfile ou votre fichier de service Systemd, vous devez désormais utiliser SIGQUIT. ([#902])
  * Ajout du support des mappages de noms d'utilisateur pour les méthodes d'authentification `cert` et `peer`. Cette fonctionnalité permet de disposer de la flexibilité selon laquelle l'utilisateur initiant la connexion n'a pas besoin d'être l'utilisateur de la base de données. Le support des mappages de noms d'utilisateur par PgBouncer fonctionne de manière très similaire à celui de PostgreSQL, avec les exceptions indiquées dans la documentation. ([#996])
  * Ajout du support des connexions de réplication via PgBouncer. ([#876])

- Modifications
  * Améliorer la sortie de `SHOW USERS` pour lister les connexions. ([#1040])
  * Permettre la configuration `pool_size` par utilisateur. ([#1049])
  * Permettre la configuration `server_lifetime` par base de données. ([#1057])
  * Ajouter le support de la liste des utilisateurs créés dynamiquement dans la sortie de `SHOW USERS`. ([#1052])
  * Ajouter le support du type d'adresse `all` dans la configuration HBA. ([#1078])
  * Ajouter le support du redémarrage automatique lors de l'utilisation de systemd. ([#1080])
  * Augmenter le niveau minimum requis de c-ares à 1.9.0 ([#1076])

- Correctifs
  * Corrige les problèmes liés à la gestion des paquets de démarrage volumineux et partiels. ([#1058])
  * Ajoute le support du format `--config=value` dans le paramètre de démarrage options. ([#1064])
  * Corrige le calcul de la métrique `avg_wait_time`. ([#727])
  * Ajoute le support de la négociation de la version du protocole postgres avec le client. ([#1007])
  * Ajoute une requête en attente pour `auth_query`. ([#1034])
  * Améliorations multiples de la documentation et de l'infrastructure CI.

[#996]: https://github.com/pgbouncer/pgbouncer/pull/996
[#1040]: https://github.com/pgbouncer/pgbouncer/pull/1040
[#1049]: https://github.com/pgbouncer/pgbouncer/pull/1049
[#1057]: https://github.com/pgbouncer/pgbouncer/pull/1057
[#1052]: https://github.com/pgbouncer/pgbouncer/pull/1052
[#1058]: https://github.com/pgbouncer/pgbouncer/pull/1058
[#1007]: https://github.com/pgbouncer/pgbouncer/pull/1007
[#876]: https://github.com/pgbouncer/pgbouncer/pull/876
[#902]: https://github.com/pgbouncer/pgbouncer/pull/902
[#1064]: https://github.com/pgbouncer/pgbouncer/pull/1064
[#1078]: https://github.com/pgbouncer/pgbouncer/pull/1078
[#1080]: https://github.com/pgbouncer/pgbouncer/pull/1080
[#727]: https://github.com/pgbouncer/pgbouncer/pull/727
[#1076]: https://github.com/pgbouncer/pgbouncer/pull/1076
[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034

--------

## PgBouncer 1.22.x {#pgbouncer-122x}

**2024-03-04  -  PgBouncer 1.22.1  -  « Il fait l’été à Bangalore »**

- Correctifs
  * Corrige les problèmes provoqués par certains clients utilisant des requêtes `COPY FROM STDIN`. Ces requêtes pouvaient entraîner des fuites mémoire, des régressions de performance et un comportement incorrect des requêtes préparées. ([#1025])
    (bug introduit dans la version 1.21.0)
  * Ajoute les tests manquants au fichier source de la version ([#1026])
    (les tests manquants ont été introduits dans les versions 1.19.0 et 1.21.0)

[#1025]: https://github.com/pgbouncer/pgbouncer/pull/1025
[#1026]: https://github.com/pgbouncer/pgbouncer/pull/1026

**2024-01-31  -  PgBouncer 1.22.0  -  « DEALLOCATE ALL »**

- Fonctionnalités
  * Ajoute le support de `DEALLOCATE ALL` et `DISCARD ALL` lorsque
    `max_prepared_statements` est défini à une valeur non nulle (le mode normal `DEALLOCATE` reste toujours non pris en charge) ([#972])
  * Permet de configurer `auth_query` par base de données ([#979])

- Modifications
  * Amélioration des paramètres dans le fichier unit systemd recommandé ([#983])
  * Mise en œuvre de la logique d’échec rapide pour tous les scénarios où aucune connexion fonctionnelle à la base de données n’existe plus et aucune ne peut être établie ([#998])
  * Améliorations multiples de la documentation

- Correctifs
  * Corrige un problème dans PG14+ où PgBouncer envoyait `SET DateStyle='ISO'` pour chaque transaction ([#879])
  * Corrige le traitement du champ vide `application_name` ([#999])
  * Corrige la compilation sous Windows avec OpenSSL 3.2.0 ([#1009])

[#972]: https://github.com/pgbouncer/pgbouncer/pull/972
[#979]: https://github.com/pgbouncer/pgbouncer/pull/979
[#983]: https://github.com/pgbouncer/pgbouncer/pull/983
[#998]: https://github.com/pgbouncer/pgbouncer/pull/998
[#879]: https://github.com/pgbouncer/pgbouncer/pull/879
[#999]: https://github.com/pgbouncer/pgbouncer/pull/999
[#1009]: https://github.com/pgbouncer/pgbouncer/pull/1009

--------

## PgBouncer 1.21.x {#pgbouncer-121x}

**2023-10-16  -  PgBouncer 1.21.0  -  "Celui avec les requêtes préparées**

- Fonctionnalités
  * Ajout du support des requêtes préparées nommées au niveau du protocole ! Il s'agit probablement de l'une des fonctionnalités les plus demandées pour PgBouncer. L'utilisation conjointe des requêtes préparées avec PgBouncer peut réduire considérablement la charge CPU de votre système (aussi bien côté PgBouncer que côté PostgreSQL). Dans des tests synthétiques, cette fonctionnalité a permis d'augmenter le débit des requêtes de 15 % à 250 %, selon la charge. Pour bénéficier de cette nouvelle fonctionnalité, vous devez modifier le paramètre `max_prepared_statements` afin de lui attribuer une valeur non nulle (la valeur exacte dépend de votre charge, mais 100 est probablement raisonnable). Consultez [la documentation sur `max_prepared_statements`](/fr/docs/pgbouncer/config/#max_prepared_statements) pour plus de détails sur le fonctionnement de cette fonctionnalité, ses limitations et la manière de régler la valeur. Une fois cela fait, assurez-vous que votre bibliothèque cliente utilise effectivement les requêtes préparées. La manière de procéder varie selon le client, vous devez donc consulter la documentation du client que vous utilisez. Cette fonctionnalité a été testée de manière très poussée avant sa mise en production, mais des problèmes de performance ou des bogues pourraient toutefois exister en raison de sa complexité. Si vous en découvrez, veuillez les signaler. ([#845])

- Modifications
  * Amélioration de la sécurité des paramètres OpenSSL, les valeurs par défaut étaient très obsolètes.
    À partir de cette version, les valeurs par défaut sont désormais identiques à celles du système OpenSSL sur lequel s'exécute PgBouncer. ([#948] & [libusual/#41])
  * PgBouncer utilise désormais OpenSSL pour calculer les hachages MD5 lorsque cela est possible. Cela est nécessaire pour utiliser PgBouncer de manière conforme au FIPS. ([#949])
  * Conserver `min_pool_size` pour les pools avec un utilisateur forcé, même si aucun client n'est connecté à PgBouncer ([#947])
  * La manière dont un `peer_id` est encodé dans le jeton d'annulation par PgBouncer a changé, ce qui signifie que la réplication entre différentes versions de PgBouncer ne fonctionnera pas si toutes ne se trouvent pas du même côté de la limite de version v1.21.0. ([#945])

- Correctifs
  * Correction d'un plantage avec le message d'erreur : « FATAL dans la fonction client_proto() : état client incorrect : 6/7 » ([#928]) (bug introduit dans la version 1.18.0)
  * Correction d'un plantage avec le message d'erreur : « FATAL dans la fonction server_proto() : serveur dans un état incorrect : 11 » ([#927]) (bug introduit dans la version 1.18.0)
  * Réduction du niveau de journalisation pour les annulations ([#903])
  * Correction du préfixe de journalisation slog pour les pairs ([#922])
  * Correction d'erreurs de frappe dans la documentation ([#932])
  * Correction des erreurs signalées par l'analyseur statique ([#943])
  * Ne pas tuer tous les clients en attente en cas d'erreurs FATAL temporaires durant la connexion ([#946])
  * Utiliser la base de données automatique lorsque la base de données dans `auth_dbname` n'est pas explicitement configurée ([#921])

- Nettoyage
  * Suppression du support pour udns ([#938])

[#845]: https://github.com/pgbouncer/pgbouncer/pull/845
[#948]: https://github.com/pgbouncer/pgbouncer/pull/948
[#949]: https://github.com/pgbouncer/pgbouncer/pull/949
[#947]: https://github.com/pgbouncer/pgbouncer/pull/947
[#945]: https://github.com/pgbouncer/pgbouncer/pull/945
[#903]: https://github.com/pgbouncer/pgbouncer/pull/903
[#922]: https://github.com/pgbouncer/pgbouncer/pull/922
[#932]: https://github.com/pgbouncer/pgbouncer/pull/932
[#928]: https://github.com/pgbouncer/pgbouncer/pull/928
[#927]: https://github.com/pgbouncer/pgbouncer/pull/927
[#943]: https://github.com/pgbouncer/pgbouncer/pull/943
[#946]: https://github.com/pgbouncer/pgbouncer/pull/946
[#921]: https://github.com/pgbouncer/pgbouncer/pull/921
[#938]: https://github.com/pgbouncer/pgbouncer/pull/938
[libusual/#41]: https://github.com/libusual/libusual/pull/41

--------

## PgBouncer 1.20.x {#pgbouncer-120x}

**2023-08-09  -  PgBouncer 1.20.1  -  « Options facultatives »**

- Correctifs
  * Corrige une régression où placer `options` à l'intérieur de `ignore_startup_parameters`
    ne faisait plus ignorer les paramètres inconnus présents dans le paramètre de démarrage `options`
    depuis la version 1.20.0. ([#908])
  * Corrige une coquille ambiguë dans la documentation ([#917])

[#908]: https://github.com/pgbouncer/pgbouncer/pull/908
[#917]: https://github.com/pgbouncer/pgbouncer/pull/917

**2023-07-20  -  PgBouncer 1.20.0  -  "Un nom drôle se trouve ici**

- Dépréciations
  * L'option de redémarrage en ligne est désormais considérée comme obsolète. Cette fonctionnalité a reçu très peu d'attention ces dernières années. Elle présente plusieurs problèmes connus, et les nouvelles fonctionnalités ajoutées ne la prennent souvent pas en charge. La méthode recommandée pour effectuer un redémarrage en ligne aujourd'hui consiste à utiliser les fonctionnalités `so_reuseport` et `peers`. Ainsi, vous pouvez faire fonctionner plusieurs processus PgBouncer sur le même port. En redémarrant ces processus un par un, vous pouvez vous assurer qu'un processus PgBouncer reste toujours en écoute sur le port souhaité. ([#894])

- Fonctionnalités
  * Introduit le `track_extra_parameters` qui permet de suivre davantage de paramètres en mode pooling de transactions. Auparavant, PgBouncer ne suivait que `application_name`, `DateStyle`, `TimeZone` et `standard_conforming_strings`. À présent, PgBouncer suit `IntervalStyle` par défaut. En modifiant `track_extra_parameters`, vous pouvez suivre encore plus de paramètres, mais uniquement [ceux que PostgreSQL renvoie au client][guc_report]. Si vous utilisez Citus 12.0+, Citus veillera à ce que PostgreSQL renvoie également `search_path` au client. Ainsi, si vous utilisez Citus, vous pouvez ajouter `search_path` à la configuration `track_extra_parameters`. ([#867])
  * Transmettre le SQLSTATE pendant l'étape d'authentification. Cela permet de détecter l'absence de base de données, ce qui est utilisé par Npgsql (un fournisseur de données .NET pour PostgreSQL). ([#814])
  * Changer la valeur par défaut de `server_tls_sslmode` en `prefer`. ([#866])
  * Ajouter la prise en charge du paramètre de démarrage `options`. Cela permet d'utiliser [la variable d'environnement `PGOPTIONS` que connaissent `psql` et `libpq`][pgoptions]. En utilisant cette variable, vous pouvez définir n'importe quel paramètre PostgreSQL au démarrage. Cela ne fonctionne que pour les paramètres PostgreSQL que PgBouncer suit via `track_extra_parameters`. ([#878])

- Correctifs
  * Ne plus planter lorsque la base `pgbouncer` est utilisée comme auth_dbname. Cela reste non pris en charge, mais une erreur claire est désormais affichée au lieu d'un plantage. ([#817])
  * Corriger le nom de `peer_cache` dans `SHOW MEM`. Il était incorrectement affiché comme `db_cache` auparavant. ([#864])
  * Corriger la confusion entre source et destination dans les journaux. PgBouncer enregistrait une adresse IP source alors qu'il s'agissait en réalité de l'adresse IP de destination. ([#880])
  * N'enregistrer les connexions administrateur via les sockets Unix que lorsque `log_connections` est défini à `1`. ([#883])

[guc_report]: https://www.postgresql.org/docs/15/protocol-flow.html#PROTOCOL-ASYNC
[pgoptions]: https://www.postgresql.org/docs/current/config-setting.html#id-1.6.7.4.5
[#867]: https://github.com/pgbouncer/pgbouncer/pull/867
[#814]: https://github.com/pgbouncer/pgbouncer/pull/814
[#866]: https://github.com/pgbouncer/pgbouncer/pull/866
[#878]: https://github.com/pgbouncer/pgbouncer/pull/878
[#817]: https://github.com/pgbouncer/pgbouncer/pull/817
[#864]: https://github.com/pgbouncer/pgbouncer/pull/864
[#880]: https://github.com/pgbouncer/pgbouncer/pull/880
[#883]: https://github.com/pgbouncer/pgbouncer/pull/883
[#894]: https://github.com/pgbouncer/pgbouncer/pull/894

--------

## PgBouncer 1.19.x {#pgbouncer-119x}

**2023-05-31  -  PgBouncer 1.19.1  -  « Sunny Spring »**

Il s'agit d'une mise à jour mineure qui corrige quelques bogues récemment introduits :

- Correctifs
  * Correctif : FATAL dans la fonction disconnect_client() : état client incorrect : 0 ([#846])
    (bug introduit dans la version 1.18.0)
  * Correctif : FATAL dans la fonction server_proto() : serveur en état incorrect : 14 ([#849])
    (bug introduit dans la version 1.18.0)
  * Ajout des fichiers nécessaires à l'exécution des tests basés sur Python au fichier source de la version de publication ([#852])
    (nouveaux tests introduits dans la version 1.19.0)

[#846]: https://github.com/pgbouncer/pgbouncer/pull/846
[#849]: https://github.com/pgbouncer/pgbouncer/pull/849
[#852]: https://github.com/pgbouncer/pgbouncer/pull/852

**2023-05-04  -  PgBouncer 1.19.0  -  "Le genre classique, généré à la main**

- Fonctionnalités
  * Ajouter l'option `auth_dbname`, qui précise contre quelle base de données exécuter le `auth_query`. ([#764])
  * Ajouter la commande `SHOW STATE`, qui indique si PgBouncer est actif, en pause ou suspendu. ([#528])
  * Ajouter le support du peering entre processus PgBouncer. Cela permet de configurer PgBouncer de manière à ce que les requêtes d'annulation fonctionnent encore lorsque plusieurs processus PgBouncer différents sont derrière un même équilibreur de charge. ([#666])
  * Ajouter un paramètre dédié `cancel_wait_timeout`, qui détermine après combien de temps abandonner l'envoi d'une requête d'annulation. Valeur par défaut : 10 secondes. ([#833])
  * Nouveau cadre de test ([#792])

- Correctifs
  * Correction d'une fuite mémoire possible lors d'une erreur d'établissement de connexion TLS. ([#796])
  * Amélioration des messages d'erreur pour les options de ligne de commande non prises en charge sous Windows. ([#620])
  * Correction de l'appel à `disconnect_server` sur un serveur en état `BEING_CANCELED`. ([#815]) (introduit dans la version 1.18.0)
  * Ne plus quitter avec un statut non nul lors de la réception d'un `SIGTERM`. ([#834])
  * Échec immédiat au démarrage lorsque la création d'une socket a échoué dans `unix_socket_dir`. ([#830])
  * Échec immédiat au démarrage lorsque aucune des adresses dans `listen_addr` ne peut être écoutée. ([#838])
  * Afficher davantage de messages d'avertissement avec plus d'informations lorsque `sbuf_connect` échoue. Cela est particulièrement utile en cas d'échec de création de sockets Unix. ([#837])

- Nettoyages
  * Mises à jour diverses de CI pour une meilleure performance
  * Suppression d'AppVeyor

[#528]: https://github.com/pgbouncer/pgbouncer/issues/528
[#620]: https://github.com/pgbouncer/pgbouncer/pull/620
[#666]: https://github.com/pgbouncer/pgbouncer/pull/666
[#764]: https://github.com/pgbouncer/pgbouncer/pull/764
[#792]: https://github.com/pgbouncer/pgbouncer/pull/792
[#796]: https://github.com/pgbouncer/pgbouncer/pull/796
[#815]: https://github.com/pgbouncer/pgbouncer/pull/815
[#830]: https://github.com/pgbouncer/pgbouncer/pull/830
[#833]: https://github.com/pgbouncer/pgbouncer/pull/833
[#834]: https://github.com/pgbouncer/pgbouncer/pull/834
[#837]: https://github.com/pgbouncer/pgbouncer/pull/837
[#838]: https://github.com/pgbouncer/pgbouncer/pull/838

--------

## PgBouncer 1.18.x {#pgbouncer-118x}

**2022-12-12  -  PgBouncer 1.18.0  -  « Aucun mystère de vrai »**

- Fonctionnalités
  * Ajouter `application_name` à `SHOW CLIENTS`/`SERVERS`/`SOCKETS`
    sortie ([#449](https://github.com/pgbouncer/pgbouncer/pull/449))
  * Ajouter des informations sur les requêtes d'annulation à la sortie de `SHOW
    CLIENTS `/` SERVEURS `/` POOLS`
    ([#782](https://github.com/pgbouncer/pgbouncer/pull/782))

- Correctifs
  * Faire échouer l'opération `sbuf_send_pending` si le socket de destination est fermé
    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))
  * Corriger plusieurs plantages possibles
    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),
    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))
  * Corriger un dépassement dans la liste d'hôtes séparés par des virgules, qui
    redirigeait la connexion vers un socket Unix
    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))
  * Ne pas évincer de connexions pour atteindre `min_pool_size`
    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))
  * Corriger `SHOW HELP` avec PostgreSQL 15
    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))
  * Corriger une condition de concurrence dans la gestion de l'annulation des requêtes.
    L'annulation d'une requête d'un client pouvait annuler celle d'un autre client
    lorsque PgBouncer recevait la demande d'annulation après que la requête visée
    s'était déjà terminée.
    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))

- Nettoyages
  * Mises à jour diverses de CI

--------

## PgBouncer 1.17.x {#pgbouncer-117x}

**2022-03-23  -  PgBouncer 1.17.0  -  « Une ligne a été tracée »**

- Fonctionnalités
  * Une définition de base de données peut spécifier une liste hôte séparée par des virgules.
    Les hôtes seront connectés selon un schéma de rotation.
  * Lorsqu'une connexion est tentée vers une base de données inexistante, l'erreur ("base de données introuvable") est désormais signalée après l'authentification. Cela empêche les clients non authentifiés de sonder l'existence de bases de données. (Cela correspond à la modification apportée dans la version 1.15.0, qui consistait à signaler les utilisateurs manquants après l'authentification.)
  * Ne pas envoyer d'erreurs de déconnexion du serveur au client avant la connexion.
    Cela pourrait révéler des informations non publiques, telles que des détails de configuration, à un client qui n'est pas encore connecté.
  * Augmenter à nouveau la longueur maximale du mot de passe. Apparemment, la dernière augmentation n'a pas été suffisante assez longtemps.
  * Supprimer le rechargement automatique de `auth_file`. Le `auth_file` n'est désormais relu que lors d'un rechargement du fichier de configuration, et non plus automatiquement dès qu'il est modifié.
  * La version pour Windows inclut désormais un fichier de ressource d'information sur la version.
  * Les versions pour Windows créées sur CI sont désormais liées de manière statique, ce qui permet de les utiliser directement sans dépendances supplémentaires.

- Correctifs
  * Le support d'OpenSSL 3 a été corrigé. Les versions précédentes plantaient.
  * Ne pas appliquer le mécanisme de défaillance rapide au moment de la connexion. Ceci fait partie du changement mentionné ci-dessus qui consiste à ne pas signaler les erreurs du serveur avant l'authentification. Cela corrige également une situation particulière liée à l'authentification en pass-through SCRAM, où il est nécessaire de permettre l'échange d'authentification côté client afin de pouvoir réauthentifier côté serveur. Le mécanisme de défaillance rapide s'applique toujours juste après l'authentification, de sorte que le comportement observé reste identique dans la plupart des cas.
  * Modifier `auth_type` dans l'exemple `pgbouncer.ini` par `md5` afin de correspondre à la valeur par défaut intégrée. Certains utilisent ce fichier comme fichier de configuration par défaut, vérifiez donc si cette modification de configuration reste pertinente pour votre cas d'utilisation.
  * Corriger le plantage à la sortie dans les builds avec assertions activées.
  * Améliorer la documentation et le comportement de `tcp_defer_accept`. La documentation était incorrecte et trompeuse concernant la valeur par défaut. Dans certains cas, une valeur erronée était affichée par la commande "show config". En outre, si l'option est définie mais non prise en charge, afficher une erreur au lieu de l'ignorer, de manière similaire à la gestion des options de socket spécifiques à la plateforme.
  * Corriger la compilation avec c-ares sous Windows. c-ares >=1.18.0 est désormais requis sous Windows.

- Nettoyages
  * La plupart des avertissements de dépréciation provenant d'Autoconf >=2.70 ont été supprimés. Les versions anciennes d'Autoconf sont toujours prises en charge.
  * L'utilisation de Cirrus CI a été étendue à davantage de plateformes.
  * Le support de Travis CI a été supprimé.
  * Mise à jour des emplacements de recherche du fichier racine CA par défaut, afin de couvrir davantage de plateformes, telles que Fedora/RHEL/CentOS.
  * Les scripts Python utilisent désormais `python3` par défaut. La compatibilité avec Python 2 n'est plus maintenue.
  * Les scripts de la suite de tests utilisent désormais `command -v` à la place de `which`, qui est déprécié.
  * Plusieurs messages d'erreur ont été reformulés afin de préciser plus clairement la commande ou le paramètre de configuration auxquels ils se rapportent.
  * Les scripts de la suite de tests n'exigent plus GNU sed.
  * `make check` fonctionne désormais sous Windows (mais pas encore la suite de tests SSL).
  * Documentation indiquant que la console d'administration ne prend en charge que le protocole de requête simple, et amélioration des messages d'erreur concernant cette limitation.

--------

## PgBouncer 1.16.x {#pgbouncer-116x}

**2021-11-11  -  PgBouncer 1.16.1  -  « Test de profondeur contre efficacité discrète »**

Il s'agit d'une mise à jour mineure incluant une correction de sécurité.

* Faire que PgBouncer agisse en tant que serveur rejette les données superflues après une négociation de chiffrement SSL ou GSS.

Un attaquant en position d’interception pouvant injecter des données dans la connexion TCP pourrait insérer des données en clair au début d’une session base de données supposée protégée par chiffrement. Cela pourrait être exploité pour envoyer des commandes SQL falsifiées au serveur, bien que cela ne fonctionne que si PgBouncer ne demande aucune donnée d’authentification. (Toutefois, une configuration de PgBouncer reposant sur l’authentification par certificat SSL pourrait ne pas exiger de telles données.) (CVE-2021-3935)

**2021-08-09  -  PgBouncer 1.16.0  -  « Repoussé un jaguar »**

- Fonctionnalités
  * Prise en charge du rechargement à chaud des paramètres TLS. Lorsque le fichier
    de configuration est rechargé, les paramètres TLS modifiés prennent automatiquement effet.
  * Ajout de la prise en charge des sockets de domaine Unix abstraits. Préfixez le
    chemin d'un socket de domaine Unix par `@` pour utiliser l'espace de noms abstrait.
    Cette fonction correspond à celle introduite dans PostgreSQL 14.
  * Les longueurs maximales des mots de passe et des noms d'utilisateur ont été
    portées respectivement à 996 et 128. Plusieurs services cloud l'exigent.
  * La taille minimale du pool peut désormais être définie par base de données, comme
    la taille normale du pool et celle du pool de réserve.
  * Le nombre d'annulations de requêtes en attente est affiché dans `SHOW
    POOLS`.

- Correctifs
  * L'analyse de configuration a été renforcée en matière de gestion des erreurs dans de nombreuses situations. Là où, auparavant, une erreur pouvait être journalisée tout en permettant la poursuite du traitement, les erreurs de configuration entraînent désormais des échecs au démarrage. C'est ce qui devait toujours se produire, mais certains fragments de code ne l'ont pas correctement implémenté. Certains utilisateurs pourront constater que leurs configurations étaient erronées depuis longtemps et ne fonctionneront plus désormais.
  * La gestion des annulations de requête a été corrigée. Dans certaines circonstances, les demandes d'annulation semblaient bloquées pendant une longue durée. Ce comportement ne devrait plus se produire. En fait, les demandes d'annulation peuvent désormais dépasser le nombre de connexions du pool d'un facteur deux, ce qui signifie qu'elles ne devraient plus être bloquées. ([#542](https://github.com/pgbouncer/pgbouncer/pull/542), [#543](https://github.com/pgbouncer/pgbouncer/pull/543))
  * Le mélange d'authentification md5 et scram via HBA a été corrigé.
  * La compilation avec c-ares sous Windows a été corrigée.
  * Les messages redoutés « FIXME : fin de requête, mais query_start == 0 » ont été résolus. Nous savons désormais pourquoi ils se produisent, et vous ne devriez plus les voir. ([#565](https://github.com/pgbouncer/pgbouncer/pull/565))
  * Correction du rechargement de `default_pool_size`, `min_pool_size` et `res_pool_size`. Le rechargement de ces paramètres ne fonctionnait auparavant pas.

- Nettoyages
  * Cirrus CI est désormais
    [utilisé](https://cirrus-ci.com/github/pgbouncer/pgbouncer) à la place
    de Travis CI.
  * Comme à l'accoutumée, de nombreux tests ont été ajoutés.
  * Le message d'erreur « serveur non propre » a été clarifié. Il indique désormais « déconnexion du client pendant que le serveur n'était pas prêt » ou « déconnexion du client avant que tout n'ait été envoyé au serveur ». Le premier cas peut survenir si la connexion client est fermée alors qu'une transaction est en cours, ce qui pouvait prêter à confusion pour certains utilisateurs.
  * Il n'est plus possible d'utiliser « pgbouncer » comme nom de base de données. Ce nom est réservé à la console d'administration, et son utilisation comme nom de base de données normale ne fonctionnait jamais correctement. Cette utilisation est désormais explicitement interdite.
  * Les erreurs envoyées aux clients avant la fermeture de la connexion sont désormais étiquetées comme FATAL au lieu de simplement ERROR. Certaines clients étaient autrement confus. ([#564](https://github.com/pgbouncer/pgbouncer/pull/564))
  * Correction des avertissements du compilateur avec GCC 11.
    ([#623](https://github.com/pgbouncer/pgbouncer/issues/623))

--------

## PgBouncer 1.15.x {#pgbouncer-115x}

**2020-11-19  -  PgBouncer 1.15.0  -  « Ich hab noch einen Koffer in Berlin »**

- Fonctionnalités
  * Amélioration du rapport des échecs d'authentification. Les messages d'échec d'authentification envoyés au client indiquent désormais uniquement qu'une authentification a échoué, sans fournir de détails supplémentaires. Ces détails sont disponibles dans le journal de PgBouncer. De plus, si l'utilisateur demandé n'existe pas, l'authentification est toujours traitée jusqu'à son terme et aboutit au même message d'échec générique. Cela empêche les clients d'effectuer des sondages sur l'instance PgBouncer afin d'obtenir des informations sur les noms d'utilisateurs ou d'autres éléments liés à l'authentification. Ce comportement est similaire à celui de PostgreSQL.
  * Ne rien logger si le client se déconnecte immédiatement. Cela évite le spam dans les journaux lorsque des systèmes de surveillance ouvrent simplement une connexion TCP/IP sans envoyer de données avant de se déconnecter.
  * Utilisation du journal systemd pour la journalisation lorsqu'il est utilisé. Lorsque nous détectons que stderr est redirigé vers le journal systemd, nous utilisons les fonctions natives de systemd pour la sortie de journalisation. Cela évite d'imprimer des horodatages et des PID en double, rendant ainsi le journal un peu plus propre. De plus, cela ajoute des métadonnées telles que le niveau de gravité aux journaux, de sorte que si le journal est transmis à syslog, les messages disposent de métadonnées utiles.
  * Un sous-ensemble de la suite de tests peut désormais être exécuté sous Windows.
  * `SHOW CONFIG` affiche désormais les valeurs par défaut des paramètres.

- Correctifs
  * Correction de l'option `so_reuseport` sous FreeBSD. Le code original de PgBouncer 1.12.0 ne fonctionnait pas réellement sous FreeBSD.
    ([#504](https://github.com/pgbouncer/pgbouncer/pull/504))
  * Correction de la compilation sur les systèmes avec des versions anciennes de systemd. Ce problème était apparu à partir de la version 1.14.0.
    ([#505](https://github.com/pgbouncer/pgbouncer/issues/505))
  * La cible du fichier makefile pour la construction des paquets binaires Windows au format zip a été corrigée.
  * Les options de ligne de commande longues fonctionnent désormais également sous Windows.
  * Correction du comportement du paramètre global `auth_user`. Le comportement précédent était ambigu et instable, car il dépendait de l'ordre des entrées dans le fichier de configuration. Ce n'est plus le cas.
    ([#391](https://github.com/pgbouncer/pgbouncer/issues/391),
    [#393](https://github.com/pgbouncer/pgbouncer/issues/393))

- Nettoyages
  * Améliorer la stabilité et la portabilité des tests.
  * Moderniser le code lié à Autoconf.
  * Désactiver les avertissements de dépréciation du compilateur provenant d'OpenSSL 3.0.0.

--------

## PgBouncer 1.14.x {#pgbouncer-114x}

**2020-06-11  -  PgBouncer 1.14.0  -  "La ritrovata magia**

- Fonctionnalités
  * Ajouter le passage en transparence de l'authentification SCRAM. Cela permet d'utiliser des secrets SCRAM chiffrés dans PgBouncer (soit dans `userlist.txt`, soit provenant de `auth_query`) pour se connecter aux serveurs.
  * Ajouter le support de l'activation par socket systemd. Cela est particulièrement utile pour permettre à systemd de gérer la création des sockets domaine Unix sur les systèmes où l'accès à `/var/run/postgresql` est restreint.
  * Ajouter le support des sockets domaine Unix sous Windows.

- Nettoyages
  * Ajouter un fichier de configuration plus petit, alternatif
    `pgbouncer-minimal.ini` pour les tests ou le déploiement.

--------

## PgBouncer 1.13.x {#pgbouncer-113x}

**2020-04-27  -  PgBouncer 1.13.0  -  "Mon jeu préféré**

- Fonctionnalités
  * Ajouter le paramètre de configuration `tcp_user_timeout` pour définir l'option de socket correspondante.
  * `client_tls_protocols` et `server_tls_protocols` ont maintenant pour valeur par défaut `secure`, ce qui signifie que seuls TLS 1.2 et TLS 1.3 sont activés. Les versions plus anciennes sont toujours prises en charge, mais ne sont pas activées par défaut.
  * Ajout du support des notifications de service systemd. Actuellement, cela permet d'utiliser les unités de service `Type=notify`. Une intégration plus poussée est prévue pour les versions futures.

- Correctifs
  * Correction des messages de journal sur plusieurs lignes
    ([libusual #24](https://github.com/libusual/libusual/pull/24))
  * Gestion des noms d’utilisateur nuls renvoyés par `auth_query` de manière appropriée
    ([#340](https://github.com/pgbouncer/pgbouncer/pull/340))

- Nettoyages
  * Les fichiers de paquetage Debian sous `debian` ont été supprimés. Il est recommandé d'utiliser les paquets provenant de https://apt.postgresql.org/.
  * Nombreuses corrections et améliorations apportées au jeu de tests
  * Les tests n'essaient plus d'utiliser sudo par défaut. Cette fonctionnalité peut désormais être activée explicitement en définissant la variable d'environnement `USE_SUDO`
  * L'API libevent a été mise à jour pour utiliser les interfaces de style version 2 et ne plus utiliser les interfaces obsolètes de la version 1.

--------

## PgBouncer 1.12.x {#pgbouncer-112x}

**2019-10-17  -  PgBouncer 1.12.0  -  « Il s'agit d'apprendre et de s'améliorer »**

Cette version inclut diverses améliorations mineures et corrections.

- Fonctionnalités
  * Ajouter un paramètre pour activer l'option `SO_REUSEPORT` socket. Sur certains systèmes d'exploitation, cela permet d'exécuter plusieurs instances de PgBouncer sur le même hôte, écoutant sur le même port, avec une distribution automatique des connexions par le noyau.
  * Ajouter un paramètre pour utiliser un fichier `resolv.conf` distinct du système d'exploitation. Cela permet de définir des serveurs DNS personnalisés et éventuellement d'autres options DNS.
  * Envoyer la sortie de `SHOW VERSION` sous forme de ligne de résultat normale au lieu d'un message NOTICE. Cela facilite la consommation et est cohérent avec les autres commandes `SHOW`.

- Correctifs
  * Envoyer les colonnes de statistiques en tant que `numeric` au lieu de `bigint`. Cela évite que certaines bibliothèques clientes échouent sur des valeurs dépassant la plage de `bigint`. ([#360](https://github.com/pgbouncer/pgbouncer/pull/360),
    [#401](https://github.com/pgbouncer/pgbouncer/pull/401))
  * Corriger le problème des utilisateurs PAM qui perdaient leur mot de passe. ([#285](https://github.com/pgbouncer/pgbouncer/issues/285))
  * Accepter les clients ayant activé le binding de canal SCRAM. Précédemment, un client prenant en charge le binding de canal (c’est-à-dire PostgreSQL 11+) pouvait échouer à se connecter à PgBouncer dans certaines situations. (PgBouncer ne prend pas en charge le binding de canal. Ce changement ne corrige que la prise en charge des clients qui le proposent.)
  * Corriger la compilation avec les versions plus récentes de musl-libc (utilisée par Alpine Linux).

- Nettoyages
  * Ajouter la cible `make check`. Cela permet d'exécuter tous les tests depuis une seule commande.
  * Supprimer les références à la wiki PostgreSQL. Toutes les informations sont désormais soit dans la documentation de PgBouncer, soit sur le site web.
  * Supprimer le support de la version 1.x de Libevent. La version 2.x de Libevent est désormais requise. Libevent est maintenant détecté à l'aide de pkg-config.
  * Corriger les avertissements du compilateur sous macOS et Windows. La compilation sur ces plates-formes ne devrait plus générer d'avertissements.
  * Corriger certains avertissements provenant de scan-build LLVM.

--------

## PgBouncer 1.11.x {#pgbouncer-111x}

**2019-08-27  -  PgBouncer 1.11.0  -  « Instinct for Greatness »**

- Fonctionnalités
  * Ajout du support de l'authentification SCRAM pour les clients et les serveurs. Un nouveau type d'authentification `scram-sha-256` est ajouté.
  * Gérer `auth_type=password` lorsque le mot de passe stocké est au format md5, comme le ferait un serveur PostgreSQL. ([#129](https://github.com/pgbouncer/pgbouncer/pull/129))
  * Ajout de l'option `log_stats` pour désactiver l'affichage des statistiques dans le journal. ([#287](https://github.com/pgbouncer/pgbouncer/pull/287))
  * Ajout de la fuseau horaire aux horodatages du journal.
  * Placer le PID entre crochets dans le préfixe du journal.
- Correctifs
  * Correction du test de configuration OpenSSL lors de l'exécution contre une version plus récente d'OpenSSL avec `-Werror`.
  * Correction du calcul du temps d'attente avec `auth_user`. Cela pouvait entraîner un crash ou afficher des valeurs incorrectes pour le temps d'attente. ([#393](https://github.com/pgbouncer/pgbouncer/pull/393))
  * Gestion du paquet GSSENCRequest, ajouté dans PostgreSQL 12. Il ne fait rien pour l'instant, mais évite des messages d'erreur trompeurs concernant un « en-tête de paquet incorrect ».
- Nettoyages
  * Nombreuses améliorations du jeu de tests et plusieurs nouveaux tests ajoutés
  * Correction de plusieurs avertissements du compilateur sous Windows.
  * Extension de la documentation de la section `[users]` et ajout à l'exemple de fichier de configuration. ([#330](https://github.com/pgbouncer/pgbouncer/pull/330))

--------

## PgBouncer 1.10.x {#pgbouncer-110x}

**2019-07-01  -  PgBouncer 1.10.0  -  "Peur du monde**

- Fonctionnalités
  * Ajouter la prise en charge de l'activation et de la désactivation du TLS 1.3. (Le TLS 1.3 était déjà pris en charge, selon la bibliothèque OpenSSL, mais les paramètres de configuration permettant de sélectionner les versions du protocole TLS sont désormais également compatibles avec cette version.)
- Correctifs
  * Corriger la prise en charge du TLS 1.3. Ce problème était présent avec OpenSSL 1.1.1 et 1.1.1a (mais pas avant ni après).
  * Corriger une panne rare dans `SHOW FDS`
    ([#311](https://github.com/pgbouncer/pgbouncer/issues/311)).
  * Corriger un problème pouvant entraîner une interruption prolongée si de nombreuses demandes d'annulation arrivent
    ([#329](https://github.com/pgbouncer/pgbouncer/issues/329)).
  * Éviter le message « réponse inattendue provenant de la requête de connexion » après un rechargement de postgres
    ([#220](https://github.com/pgbouncer/pgbouncer/issues/220)).
  * Corriger le calcul de `idle_transaction_timeout`
    ([#125](https://github.com/pgbouncer/pgbouncer/issues/125)).  Ce bug pouvait entraîner des délais d'attente prématurés dans des situations spécifiques.
- Nettoyages
  * Préciser divers messages de journalisation et d'erreur.
  * Corriger les problèmes détectés par Coverity (aucun n'avait d'impact significatif en pratique).
  * Améliorer et documenter tous les scripts de test.
  * Ajouter des commandes SHOW supplémentaires à la documentation.
  * Convertir la documentation du format rst au format Markdown.
  * Tous les scripts Python présents dans l'arborescence source sont désormais compatibles avec Python 3.

--------

## PgBouncer 1.9.x {#pgbouncer-19x}

**2018-08-13  -  PgBouncer 1.9.0  -  "Chaos Survival**

- Fonctionnalités
  * Commande RECONNECT
  * Commande WAIT_CLOSE
  * Fermeture rapide – Déconnecte immédiatement un serveur en mode pool de sessions si celui-ci est en "close_needed" (reconnexion).
  * Ajout de la colonne close_needed dans SHOW SERVERS
- Correctifs
  * Éviter le double free dans parse_filename
  * Éviter le déréférencement d'un pointeur NULL dans parse_line
- Nettoyages
  * Portage de mkauth.py vers Python 3
  * Amélioration de la documentation des signaux
  * Amélioration de la documentation de démarrage rapide
  * Documentation de la commande SET
  * Correction de la liste des logiciels requis
  * Correction des avertissements -Wimplicit-fallthrough
  * Ajout de la documentation manquante pour divers champs SHOW
  * Documentation du comportement de reconnexion lors d'un rechargement et d'un changement DNS
  * Documentation du fait que KILL nécessite RESUME par la suite
  * Précision de la documentation de server_lifetime
  * Corrections de fautes de frappe et de majuscules dans les messages et la documentation
  * Correction de l'appel psql dans les tests
  * Autres améliorations diverses de la configuration des tests

--------

## PgBouncer 1.8.x {#pgbouncer-18x}

**2017-12-20  -  PgBouncer 1.8.1  -  "Approche par pression constante**

- Correctifs
  * Inclure le fichier `include/pam.h` dans le paquet source tarball. Cela empêchait la construction du paquet tarball 1.8.

**2017-12-19  -  PgBouncer 1.8  -  « Confiant aux commandes »**

- Fonctionnalités
  * Prise en charge de l'authentification PAM. (Activer avec `--with-pam`.)
  * Ajouter les champs `paused` et `disabled` à la sortie `SHOW DATABASES`.
  * Ajouter le champ `maxwait_us` à la sortie `SHOW POOLS`.
  * Ajouter les champs `wait` et `wait_us` à la sortie des commandes `SHOW`.
  * Ajouter de nouvelles commandes `SHOW STATS_TOTALS` et `SHOW STATS_AVERAGES`.
  * Suivre les requêtes et les transactions séparément dans `SHOW STATS`. Les champs `total_requests`, `avg_req` et `avg_query` ont été remplacés par de nouveaux champs.
  * Ajouter `wait_time` à `SHOW STATS`.
- Correctifs
  * Mise à jour de libusual pour prendre en charge OpenSSL 1.1.
  * Ne pas tenter d'utiliser TLS sur les sockets Unix.
  * Lors de l'analyse de `pg_hba.conf`, poursuivre l'analyse après les lignes erronées au lieu de rejeter entièrement le fichier.
    ([#118](https://github.com/pgbouncer/pgbouncer/issues/118))
  * Plusieurs corrections supplémentaires liées à l'analyse de HBA.
  * Corriger la condition de course lors de l'annulation d'une requête.
    ([#141](https://github.com/pgbouncer/pgbouncer/issues/141))
- Nettoyages
  * `auth_user` peut désormais être défini globalement, et non seulement par base de données.
    ([#142](https://github.com/pgbouncer/pgbouncer/issues/142))
  * Définir l'encodage du client et du serveur de la console sur `UTF8`.

--------

## PgBouncer 1.7.x {#pgbouncer-17x}

**2016-02-26  -  PgBouncer 1.7.2  -  « Enfin en vol »**

- Correctifs
  * Corrige un plantage lors de la suppression d'un fichier PID obsolète. Problème introduit dans la version 1.7.1.
  * Désactivez le nettoyage — cela perturbe la prise de contrôle et n'est pas utile pour les charges de production. Problème introduit dans la version 1.7.1.
  * Après une prise de contrôle, attendez que le fichier PID disparaisse avant de démarrer. Une fermeture lente due au nettoyage mémoire a mis en évidence une course existante. ([#113](https://github.com/pgbouncer/pgbouncer/issues/113))
- Nettoyages
  * Rendre la construction reproductible en supprimant la gestion de DBGVER. ([#112](https://github.com/pgbouncer/pgbouncer/issues/112))
  * Antimake : trier la liste de fichiers provenant de $(wildcard), les versions récentes de gmake ne trient plus automatiquement. ([#111](https://github.com/pgbouncer/pgbouncer/issues/111))
  * Affiche la version de libssl dans les journaux.
  * deb : activer le durcissement complet.

**2016-02-18  -  PgBouncer 1.7.1  -  « Transférer à cinq amis ou sinon »**

AVERTISSEMENT : À compter de la version 1.7, `server_reset_query` n'est plus exécuté lorsque la base de données est en mode pool de transactions. Ce point n'avait pas été suffisamment mis en évidence dans l'annonce de la version 1.7. Si vos applications dépendent de ce comportement, utilisez `server_reset_query_always` pour restaurer le comportement précédent.

Sinon, le principal travail de cette version a consisté à identifier une fuite mémoire liée au TLS, qui s'est finalement révélée n'exister pas. En réalité, la bibliothèque libssl incluse dans Debian/wheezy présente une surcharge de 600 ko par connexion (sans fuite), au lieu des 20 à 30 ko attendus. À surveiller attentivement lors de l'utilisation du TLS.

- Correctifs
  * TLS : Renommer le mode sslmode "disabled" en "disable", conformément à la terminologie utilisée par PostgreSQL.
  * TLS : `client_tls_sslmode=verify-ca/-full` rejette désormais les connexions sans certificat client.
    ([#104](https://github.com/pgbouncer/pgbouncer/issues/104))
  * TLS : `client_tls_sslmode=allow/require` valider le certificat client s'il est envoyé.
    Précédemment, la validation du certificat était laissée non configurée, ce qui faisait échouer les connexions avec certificat client.
    ([#105](https://github.com/pgbouncer/pgbouncer/issues/105))
  * Corriger une fuite mémoire lors de la libération de la base de données.
  * Corriger une fuite mémoire potentielle dans tls_handshake().
  * Corriger la gestion de la fin de fichier dans tls_handshake().
  * Corriger la taille trop petite de memset dans asn1_time_parse compat.
  * Corriger la compilation sans TLS (`--without-openssl`).
    ([#101](https://github.com/pgbouncer/pgbouncer/issues/101))
  * Corriger divers problèmes liés à la compilation sous Windows.
    ([#100](https://github.com/pgbouncer/pgbouncer/issues/100))
- Nettoyages
  * TLS : Utiliser SSL_MODE_RELEASE_BUFFERS afin de réduire l'utilisation mémoire des connexions inactives.
  * Libérer la mémoire allouée à la sortie.
    Facilite l'exécution des vérificateurs de fuites mémoire.
  * Améliorer la documentation de `server_reset_query`.
    ([#110](https://github.com/pgbouncer/pgbouncer/issues/110))
  * Ajouter des options TLS à la configuration exemple.

**2015-12-18  -  PgBouncer 1.7  -  "Les couleurs varient après la résurrection**

- Fonctionnalités
  * Prise en charge des connexions TLS. OpenSSL/LibreSSL est utilisé comme implémentation backend.
  * Prise en charge de l'authentification via certificat client TLS.
  * Prise en charge de l'authentification « peer » sur les sockets Unix.
  * Prise en charge du fichier de contrôle d'accès basé sur l'hôte, comme [pg_hba.conf](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html) dans Postgres. Cela permet de configurer le TLS pour les connexions réseau et l'authentification « peer » pour les connexions locales.
- Nettoyages
  * Définit `query_wait_timeout` à 120 s par défaut. La valeur par défaut actuelle (0) entraîne un enfilement infini, ce qui n'est pas utile. Cela signifie que si un client a une requête en attente et n'a pas été affecté à une connexion serveur, la connexion client sera fermée.
  * Désactive `server_reset_query_always` par défaut. La réinitialisation de requête n'est désormais utilisée que dans les pools en mode session.
  * Augmente pkt_buf à 4096 octets. Améliore les performances avec TLS. Le comportement est probablement spécifique à la charge, mais il est sans danger de le faire depuis la version 1.2, où les tampons de paquet sont séparés des connexions et utilisés de manière paresseuse depuis le pool.
  * Prise en charge du comptage des paquets ReadyForQuery attendus en cas de pipeline. Évite de libérer le serveur trop tôt. Corrige [#52](https://github.com/pgbouncer/pgbouncer/issues/52).
  * Amélioration de la logique sbuf_loopcnt : la socket est garantie de être retraitée même en l'absence d'événement provenant de la socket. Nécessaire pour TLS, qui dispose de son propre mécanisme de tamponnage.
  * Adaptation des tests système pour fonctionner avec les versions modernes de BSD et MacOS. (Eric Radman)
  * Suppression de l'authentification **crypt**. Elle est obsolète et n'est plus prise en charge par PostgreSQL depuis la version 8.4.
  * Correction de l'option de configuration "--with-cares" sans argument : elle était défectueuse.

--------

## PgBouncer 1.6.x {#pgbouncer-16x}

**2015-09-03  -  PgBouncer 1.6.1  -  « Studio Audience Approves »**

- Fonctionnalités
  * Nouveau paramètre : `server_reset_query_always`. Lorsqu’il est défini,
désactive l’utilisation de `server_reset_query` dans les pools non sessionnels.
PgBouncer introduit un mode de poolage par pool, mais le poolage par session
et le poolage par transaction ne doivent pas utiliser la même requête de réinitialisation.
En réalité, le poolage par transaction ne doit pas utiliser de requête de réinitialisation.

    It is set in 1.6.x, but will be disabled in 1.7.

- Correctifs
  * [SECURITÉ] Suppression de l'affectation non valide de `auth_user`. (#69)
    Lorsque `auth_user` est défini et que le client demande un nom d'utilisateur inexistant,
    le client se connecte en tant que `auth_user`. Ce comportement est incorrect.

    [CVE-2015-6817](https://access.redhat.com/security/cve/cve-2015-6817)

  * Ignorer NoticeResponse dans handle_auth_response. Sinon, les niveaux de journalisation verbeux du serveur entraînent des échecs de connexion.

  * console : Remplir `auth_user` lorsque auth_type=any. Sinon, la journalisation peut planter (#67).

  * Plusieurs correctifs de portabilité (OpenBSD, Solaris, OSX).

**2015-08-01  -  PgBouncer 1.6  -  « Zombies de l'avenir »**

- Fonctionnalités

  * Charger le hachage du mot de passe utilisateur depuis la base de données postgres.
    Nouveaux paramètres :

    auth_user
        user to use for connecting same db and fetching user info.
        Can be set per-database too.

    auth_query
        SQL query to run under auth_user.
        Default: "SELECT usename, passwd FROM pg_shadow WHERE usename=$1"

    (Cody Cutrer)

  * Le mode de poolage peut être configuré à la fois par base de données et par utilisateur.
    (Cody Cutrer)

  * Limites de connexions par base de données et par utilisateur : max_db_connections et max_user_connections.
(Cody Cutrer / Pavel Stehule)

  * Ajouter les commandes DISABLE/ENABLE pour empêcher les nouvelles connexions.
    (William Grant)

  * Nouveau backend DNS : c-ares. Seul backend DNS à prendre en charge toutes les fonctionnalités intéressantes :  /etc/hosts avec actualisation, recherche SOA, réponses longues (via TCP/EDNS+UDP) et IPv6. Il est désormais le backend privilégié, et devrait probablement être le **seul** backend à l'avenir, puisqu'il est inutile de maintenir une multitude de bibliothèques insuffisantes.

    SNAFU: c-ares versions <= 1.10 have bug which breaks CNAME-s support
    when IPv6 has been enabled.  (Fixed upstream.)  As a workaround,
    c-ares <= 1.10 is used IPv4-only.  So PgBouncer will drop other backends
    only when c-ares >1.10 (still unreleased) has been out some time...

  * Affiche remote_pid dans SHOW CLIENTS/SERVERS. Disponible pour les clients connectés via des sockets Unix, ainsi que pour les serveurs TCP et sockets Unix. Dans le cas d'un serveur TCP, le PID est extrait de la clé d'annulation.

  * Ajouter un paramètre de configuration séparé (dns_nxdomain_ttl) pour contrôler le cache négatif DNS.
(Cody Cutrer)

  * Ajoutez l'adresse IP et le port de l'hôte client à application_name.
Cela est activé par un paramètre de configuration application_name_add_host
qui est désactivé par défaut.
(Andrew Dunstan)

  * Les fichiers de configuration contiennent la directive '%include FILENAME' pour permettre de diviser la configuration en plusieurs fichiers.
(Andrew Dunstan)

- Nettoyages

  * log : entourer l'adresse ipv6 de crochets []
  * log : lors de la connexion au serveur, afficher l'adresse IP locale et le port
  * win32 : utiliser le style gnu pour les arguments longs : --foo
  * Autoriser les chiffres dans le nom d'hôte, essayer toujours d'analyser avec inet_pton
  * Corriger deallocate_all() dans la FAQ
  * Corriger le mot-clé incorrect dans l'exemple de fichier de configuration
    (Magnus Hagander)
  * Autoriser les commentaires (avec ';') dans les fichiers d'authentification.
    (Guillaume Aubert)
  * Corriger les fautes d'orthographe dans les messages de journalisation et les commentaires.
    (Dmitriy Olshevskiy)

- Correctifs

  * corriger le lancement de nouvelles connexions pendant la maintenance
    (Cody Cutrer)
  * ne pas charger deux fois le fichier d'authentification au démarrage
    (Cody Cutrer)
  * invalidation correcte pour les bases autodéfinies
  * IPv6 : définir IPV6_V6ONLY sur la socket d'écoute.
  * win32 : ne pas définir SO_REUSEADDR sur la socket d'écoute.
  * corriger la copie d'adresse IPv6
  * corriger l'annulation des clients en attente.
    (Mathieu Fenniak)
  * petit correctif, vérifier obligatoirement le résultat de calloc
    (Heikki Linnakangas)
  * ajouter une nouvelle ligne à la fin du fichier PID
    (Peter Eisentraut)
  * ne pas autoriser de nouvelles connexions serveur lorsque PAUSE <db> a été émis.
    (Petr Jelinek)
  * corriger « paquet incorrect » lors de la connexion lorsque l'en-tête est retardé.
    (Michal Trojnara, Marko Kreen)
  * corriger les erreurs détectées par Coverty.
    (Euler Taveira)
  * désactiver server_idle_timeout lorsque le nombre de serveurs tombe en dessous de min_pool (#60)
    (Marko Kreen)

--------

## PgBouncer 1.5.x {#pgbouncer-15x}

**2015-04-09  -  PgBouncer 1.5.5  -  « Play Dead To Win »**

- Correctifs
  * Corrige une panne distante — un ordre de paquets non valide provoque une recherche pointeur NULL.
Non exploitable, uniquement une attaque de type DDoS.

**2012-11-28  -  PgBouncer 1.5.4  -  « Pas de fuites, apprentissage réussi »**

- Correctifs
  * DNS : correction d'une fuite mémoire dans le backend getaddrinfo_a().
  * DNS : correction d'une fuite mémoire dans le backend udns.
  * DNS : correction du calcul des statistiques.
  * DNS : amélioration de la gestion des messages d'erreur pour getaddrinfo_a().
  * Correction de la compilation sous Win32.
  * Correction de la vérification des dépendances du compilateur dans configure.
  * Quelques corrections dans la documentation.

**2012-09-12  -  PgBouncer 1.5.3  -  "Quantum Toaster**

- Correction critique

  * Les noms de base de données trop longs peuvent entraîner un plantage, ce qui est potentiellement déclenchable à distance si les bases de données automatiques sont activées.

Les vérifications initiales supposaient que tous les noms proviennent de fichiers de configuration,
ce qui justifiait l'utilisation de fatal(), mais lorsque les bases de données automatiques sont activées
    - par '*' dans la section [databases] - le nom de la base peut provenir du réseau,
ce qui rend la fermeture à distance possible.

    [CVE-2012-4575](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-4575)

- Fonctionnalités mineures

  * max_packet_size - paramètre de configuration permettant de régler la taille maximale des paquets autorisés. La valeur par défaut est conservée à (2G-1), mais elle peut désormais être réduite.
  * En cas d’en-tête de paquet non analysable, l’afficher en hexadécimal dans le journal et le message d’erreur.

- Correctifs

  * AntiMake : il utilisait $(relpath) et $(abspath) pour manipuler les chemins,
    mais cela entraînait une erreur de compilation lorsque le chemin de l'arborescence source contenait
    des liens symboliques. Le code a maintenant été modifié pour ne plus fonctionner qu'avec des chaînes de caractères simples.
  * console : il est désormais possible d'utiliser SET pour définir des valeurs de chaîne vide.
  * config.txt : indique que tous les délais d'attente peuvent être définis sous forme de nombres à virgule flottante.
    Il s'agit d'une fonctionnalité peu visible introduite à la version 1.4.

**2012-05-29  -  PgBouncer 1.5.2  -  « Ne mâche pas, avale simplement »**

- Correctifs
  * En raison d'une erreur, reserve_pool_timeout était exprimé en microsecondes,
    au lieu de secondes, ce qui activait immédiatement la réserve lorsque le pool était plein.
    Cette valeur est désormais exprimée en secondes, comme prévu.
    (Signalé par Keyur Govande)

**2012-04-17  -  PgBouncer 1.5.1  -  « Abandonner, Réessayer, Ignorer ? »**

- Fonctionnalités
  * Paramètres permettant de configurer les permissions sur le socket Unix :
    unix_socket_mode=0777, unix_socket_group=''
- Correctifs
  * Permettre une chaîne vide pour les variables côté serveur — cela est nécessaire pour assurer le bon fonctionnement de "application_name", qui est le seul paramètre ne disposant pas de valeur par défaut côté serveur.
  * En cas de modification de la chaîne de connexion, exiger une actualisation des paramètres du serveur.
    Précédemment, PgBouncer continuait avec les anciens paramètres,
    ce qui provoquait des dysfonctionnements lors d'une mise à jour de Postgres.
  * En cas de modification de la chaîne de connexion autodb, fermer les anciennes connexions.
  * cf_setint : utiliser strtol() au lieu de atoi() pour analyser les paramètres de configuration entiers.
    Cela permet de traiter les valeurs hexadécimales, octales et améliore la détection des erreurs.
  * Utiliser sigqueue() pour détecter l'existence de union sigval — corrige la compilation sur HPUX.
  * Supprimer la commande 'git' du fichier Makefile, qui provoque des erreurs aléatoires
    lors d'une compilation à partir d'un paquet tarball standard.
  * Documenter le paramètre stats_period.
    Ce paramètre permet de régler la période d'affichage des statistiques.
  * Exiger Asciidoc >= 8.4, les documents ne sont plus compatibles
    avec les versions antérieures.
  * Cesser d'essayer de réessayer en cas d'EINTR provenant de close().

**2012-01-05  -  PgBouncer 1.5  -  « Clients satisfaits depuis 2007 »**

Si vous utilisez plus de 8 adresses IP derrière un même nom DNS, vous devez désormais utiliser le protocole EDNS0 pour les requêtes. Seuls les backends getaddrinfo_a()/getaddrinfo() et UDNS le supportent ; libevent 1.x/2.x ne le fait pas. Pour l’activer pour libc, ajoutez « options edns0 » à /etc/resolv.conf.

GNU Make 3.81+ est requis pour la compilation.

- Fonctionnalités
  * Détection des modifications des réponses DNS et invalidation des connexions vers les adresses IP désormais absentes de la dernière réponse.
    (Petr Jelinek)
  * Invalidation basée sur le numéro de série de la zone DNS. Lorsque l'option dns_zone_check_period est définie, toutes les zones DNS sont interrogées pour obtenir leur SOA, et si le numéro de série a changé, toutes les adresses hôtes sont redemandées. Cette fonction est nécessaire pour assurer une invalidation déterministe des connexions, car l'invalidation au moment de la recherche est inutile si aucune recherche n'est effectuée.
    Fonctionne uniquement avec le backend UDNS nouveau.
  * Nouvelles commandes SHOW DNS_HOSTS et SHOW DNS_ZONES pour examiner le cache DNS.
  * Nouveau paramètre : min_pool_size — évite de supprimer toutes les connexions lorsqu'il n'y a pas de charge.
    (Filip Rembialkowski)
  * idle_in_transaction_timeout — tue la transaction si l'attente est trop longue.
    Non défini par défaut.
  * Nouveau backend libudns pour les requêtes DNS. Plus fonctionnel que evdns.
    Utiliser --with-udns pour l'activer. Ne fonctionne pas encore avec IPv6.
  * Commande KILL, pour tuer immédiatement toutes les connexions d'une base de données.
    (Michael Tharp)
  * Migration vers le système de construction Antimake pour obtenir des fichiers Makefiles plus lisibles.
    Une version GNU Make 3.81 ou supérieure est désormais requise pour la compilation.
- Correctifs
  * Le DNS fonctionne désormais avec les noms d'hôtes IPv6.
  * Ne pas modifier l'état de la connexion lorsqu'un NOTIFY arrive du serveur.
  * Divers correctifs de documentation.
    (Dan McGee)
  * Console : prise en charge de la citation ident avec "". À l'origine, aucune commande ne prenait de noms de base de données, donc aucune citation n'était nécessaire.
  * Console : autorisation des chiffres au début des expressions régulières de mot. Essayer d'utiliser un parseur strict rendrait les choses trop complexes ici.
  * Ne pas expirer les bases de données automatiques en pause.
    (Michael Tharp)
  * Créer les bases de données automatiques au besoin lors de l'opération PAUSE.
    (Michael Tharp)
  * Correction du message de journal incorrect émis par la commande RESUME.
    (Peter Eisentraut)
  * Lorsqu'un paramètre user= est présent sans password= dans la chaîne de connexion, le mot de passe est pris dans la liste des utilisateurs.
  * Analyse correcte du caractère '*' dans le code de prise de contrôle.
  * autogen.sh : compatibilité avec les versions anciennes d'autoconf/automake.
  * Correction de la panne lors de l'exécution en tant que service sous win32 due à une mauvaise implémentation de basename() dans les bibliothèques mingw/msvc. Une version compatible de basename() est désormais toujours utilisée.

--------

## PgBouncer 1.4.x {#pgbouncer-14x}

**2011-06-16  -  PgBouncer 1.4.2  -  Algorithme « Strike-First »**

Systèmes d'exploitation concernés : \*BSD, Solaris, Win32.

- Correctifs de portabilité
  * Passer les CFLAGS au lienur. Nécessaire lors de l'utilisation de la fonction getaddrinfo_a() basée sur pthread en fallback.
  * lib/find_modules.sh : Remplacer split() par index()+substr(). Cela devrait permettre le fonctionnement avec les versions plus anciennes d'AWK.
  * <usual/endian.h> : Ignorer les définitions système de htoX/Xtoh. Il se peut qu'un sous-ensemble de macros soit défini.
  * <usual/signal.h> : Séparer sigval compatible de sigevent compatible
  * <usual/socket.h> : Inclure <sys/uio.h> pour obtenir iovec
  * <usual/time.h> : Détection améliorée des fonctions sur win32
  * <usual/base_win32.h> : Supprimer la déclaration redondante de sigval/sigevent

**2011-04-01  -  PgBouncer 1.4.1  -  « C’était tout un spectacle »**

- Fonctionnalités

  * Prise en charge de l'écoute/connecter sur les adresses IPv6.
    (Hannu Krosing)
  * Adresses d'écoute multiples dans 'listen_addr'. Pour chaque appel à getaddrinfo(),
    les noms peuvent également être utilisés.
  * console : Envoyer la version de PgBouncer en tant que 'server_version' au client.

- Correctifs importants

  * Désactiver getaddrinfo_a() sur glibc < 2.9 car il provoque un plantage sur les versions anciennes.

    Notable affected OS'es: RHEL/CentOS 5.x (glibc 2.5), Ubuntu 8.04 (glibc 2.7).
    Also Debian/lenny (glibc 2.7) which has non-crashing getaddrinfo_a()
    but we have no good way to detect it.

    Please use libevent 2.x on such OS'es, fallback getaddrinfo_a() is not
    meant for production systems.  And read new 'DNS lookup support' section
    in README to see how DNS backend is picked.

    (Hubert Depesz Lubaczewski, Dominique Hermsdorff, David Sommerseth)

  * Par défaut, --enable-evdns si la bibliothèque libevent 2.x est utilisée.

  * Activer tcp_keepalive par défaut, car c'est ce que fait également Postgres.
    (Hubert Depesz Lubaczewski)

  * Définit par défaut server_reset_query sur DISCARD ALL pour assurer la compatibilité avec Postgres.

  * win32 : Corriger les plantages liés à une adresse de socket Unix NULL.
    (Hiroshi Saito)

  * Correction de l'opération de nettoyage autodb : le code de nettoyage ancien mélangait bases de données et pools :
    dès qu'un pool vide était détecté, la base de données était marquée comme « inactif »,
    ce qui pouvait entraîner la fermeture d'une base de données avec des utilisateurs actifs.

    Reported-By: Hubert Depesz Lubaczewski

- Correctifs

  * Rendre la fonction getaddrinfo_a compatible et non bloquante en utilisant un seul thread parallèle pour les recherches.
  * Activer la compilation avec pthread si getaddrinfo_a est utilisé.
  * Le release_server n’a pas défini ->last_lifetime_disconnect lors de la déconnexion par durée de vie.
    (Emmanuel Courreges)
  * win32 : corriger le fichier d’authentification avec des fins de ligne DOS – load_file() ne tenait pas compte de la réduction de taille du fichier lors du chargement.
    (Rich Schaaf)
  * <usual/endian.h> : ajouter une détection autoconf pour les fonctions d’encodage/décodage afin d’éviter les conflits sur BSD.
    (James Pye)
  * Ne pas planter si le fichier de configuration n’existe pas.
    (Lou Picciano)
  * Ne pas planter en cas d’échec de recherche DNS lors de la journalisation au niveau bruit (-v -v).
    (Hubert Depesz Lubaczewski, Dominique Hermsdorff)
  * Utiliser des accents graves au lieu de $(cmd) dans find_modules.sh pour améliorer la portabilité.
    (Lou Picciano)
  * Utiliser 'awk' au lieu de 'sed' dans find_modules.sh pour améliorer la portabilité.
    (Giorgio Valoti)
  * Journaliser les informations sur le backend DNS asynchrone actif au démarrage.
  * Corriger --disable-evdns pour qu’il signifie « non » au lieu de « oui ».
  * Préciser dans la documentation que -R nécessite unix_socket_dir.
  * Discuter de server_reset_query dans faq.txt.
  * Restaurer le memset perdu dans l’allocateur de tranches.
  * Diverses corrections mineures de portabilité dans libusual.

**2011-01-11  -  PgBouncer 1.4  -  "Gore Code**

- Fonctionnalités

  * Recherche DNS asynchrone – au lieu de résoudre les noms d'hôtes au moment du rechargement, ceux-ci sont désormais résolus au moment de la connexion, avec mise en cache configurable.
(Voir le paramètre dns_max_ttl.)

    By default it uses getaddrinfo_a() (glibc) as backend, if it does not
    exist, then getaddrinfo_a() is emulated via blocking(!) getaddrinfo().

    When --enable-evdns argument to configure, libevent's evdns is used
    as backend.  It is not used by default, because libevent 1.3/1.4
    contain buggy implementation.  Only evdns in libevent 2.0 seems OK.

  * Nouvelle variable de configuration : syslog_ident, pour personnaliser le nom syslog.

  * Prise en charge correcte du paramètre de démarrage `application_name`.

  * Options longues en ligne de commande (Guillaume Lelarge)

  * Correctifs de compatibilité Solaris (Hubert Depesz Lubaczewski)

  * Nouvelle variable de configuration : disable_pqexec. Les environnements très paranoïaques peuvent désactiver le protocole de requête simple avec cette option. Nécessite que les applications utilisent uniquement le protocole de requête étendu.

  * Compatibilité Postgres : si le nom de la base est vide dans le paquet de démarrage, utilisez le nom d'utilisateur comme base.

- Correctifs

  * Les paramètres serveur DateStyle et TimeZone doivent utiliser la casse exacte.
  * Console : envoyer les paramètres serveur datetime, timezone et stdstr au client.

- Nettoyages internes

  * Utilisez la bibliothèque libusual pour les fonctions utilitaires de bas niveau.
  * Supprimez la limite de longueur fixe des paramètres du serveur.

--------

## PgBouncer 1.3.x {#pgbouncer-13x}

**2010-09-09  -  PgBouncer 1.3.4  -  « Bouncer est toujours droit »**

- Correctifs
  * Appliquer une logique de défaillance rapide au moment de la connexion. Ainsi, si le serveur échoue, les clients reçoivent une erreur lors de la connexion.
  * Ne pas étiqueter automatiquement les bases de données générées pour leur vérification au moment du rechargement, sinon elles sont supprimées, car elles n'existent pas dans la configuration.
  * Ignorer par défaut le paramètre application_name. Cela évite que tous les utilisateurs de Postgres 9.0 n'aient à l'ajouter eux-mêmes dans ignore_startup_parameters=.
  * Corriger la citation pg_auth. '\' n'est pas utilisé à cet endroit.
  * Meilleure signalisation d'erreurs depuis la console, afficher la requête entrante à l'utilisateur.
  * Prise en charge des systèmes d'exploitation (OpenBSD) où tv_sec n'est pas de type time_t.
  * Éviter les avertissements trop bruyants sous gcc 4.5.

**2010-05-10  -  PgBouncer 1.3.3  -  "NSFW**

- Améliorations
  * Rendre le paramètre listen(2) configurable : listen_backlog. Cela est utile sur les systèmes où la valeur maximale autorisée est configurable.
  * Améliorer les messages de déconnexion pour indiquer quel utilisateur ou nom de base a provoqué l'échec de connexion.
- Correctifs
  * Déplacer la logique de redémarrage rapide. L'ancienne implémentation était ennuyeuse dans le cas de bases de données ou d'utilisateurs définitivement corrompus, en tentant de réessayer même lorsque aucun client ne souhaitait se connecter.
  * Faire en sorte que les fonctions de journalisation conservent l'ancien errno, sinon PgBouncer peut se comporter de manière inattendue aux niveaux de journalisation élevés ou en cas de problèmes d'écriture du journal.
  * Augmenter la taille de divers tampons liés au démarrage afin de gérer le démarrage plus bruyant d'EDB.
  * Détecter les requêtes de démarrage au protocole V2 et fournir une raison claire pour la déconnexion.

**2010-03-15  -  PgBouncer 1.3.2  -  « Boomerang Bullet »**

- Correctifs

  * Nouvelle variable de configuration 'query_wait_timeout'. Si le client ne reçoit pas de connexion au serveur dans ce délai en secondes, il sera tué.

  * Si aucune connexion serveur n'est disponible dans le pool et que la dernière tentative de connexion a échoué, alors ne pas mettre les connexions clients en attente, mais envoyer une erreur immédiatement.

    This together with previous fix avoids unnecessary stalls if
    a database has gone down.

  * Suivre l'état libevent dans sbuf.c pour éviter un appel double à event_del(). Bien qu'il soit généralement sûr, cela ne semble pas fonctionner à 100 %. Nous devrions désormais toujours savoir si l'appel a été effectué ou non.

  * Désactiver la maintenance pendant SUSPEND. Sinon, avec des délais d'expiration courts, le bouncer ancien pourrait fermer quelques connexions après les avoir transférées.

  * Appliquer client_login_timeout aux clients en attente du paquet d'accueil (première connexion au serveur). Sinon, ils peuvent rester en attente indéfiniment, sauf si query_timeout est défini.

  * win32 : Ajouter l’option -U/-P à -regservice pour permettre à l’utilisateur de choisir le compte sous lequel exécuter le service. Le choix automatique précédent entre le compte Local Service et le compte Local System n’était pas suffisamment fiable.

  * console : Supprimer le caractère \0 à la fin des colonnes texte. Il était difficile à détecter, car les clients C le géraient correctement.

  * Améliorations de la documentation.  (Greg Sabino Mullane)

  * Préciser quelques messages de journal liés à la connexion.

  * Changer le niveau de journalisation des erreurs envoyées par le pooler (généralement lors de la déconnexion) de INFO à WARNING, car elles indiquent des problèmes.

  * Message du journal de changement pour query_timeout : « timeout de requête ».

**2009-07-06  -  PgBouncer 1.3.1  -  « Conforme désormais aux exigences de surveillance de l’NSA »**

- Correctifs
  * Corrige un problème lié à sbuf_loopcnt qui pouvait entraîner des connexions bloquées.
    Si la longueur de la requête ou du résultat est proche d'un multiple de (pktlen*sbuf_loopcnt)
    [10 k par défaut], elle pouvait rester en attente de données supplémentaires qui ne s'afficheraient jamais.
  * Rend la reconfiguration de base de données immédiate. Actuellement, les anciennes connexions
    pouvaient être réutilisées après SIGHUP.
  * Corrige SHOW DATABASES qui était cassé suite à l'ajout d'une colonne.
  * L'accès à la console était désactivé lorsque "auth_type=any" car pgbouncer supprimait le nom d'utilisateur.
    Correction : si "auth_type=any", autoriser tout utilisateur à accéder à la console en tant qu'administrateur.
  * Corrige la mauvaise définition du macro CUSTOM_ALIGN. Heureusement, il est inutilisé si le système d'exploitation définit déjà ALIGN, aussi le bug semble n'avoir jamais eu lieu dans la pratique.
  * win32 : appeler WSAStartup() toujours, pas seulement en mode démon
    car l'analyse de configuration doit résoudre les hôtes.
  * win32 : entourer le nom de fichier de configuration de guillemets dans la ligne de commande du service
    pour autoriser les espaces dans les chemins. Le chemin de l'exécutable
    ne semble pas nécessiter cela grâce à une certaine magie win32.
  * Ajoute STATS au texte de SHOW HELP.
  * doc/usage.txt : les unités de temps dans les résultats de la console sont en microsecondes, pas en millisecondes.

**2009-02-18  -  PgBouncer 1.3 -  "Nouveau coup final Ki-Smash**

- Fonctionnalités

  * IANA a attribué le port 6432 comme port officiel pour PgBouncer.
Par conséquent, le numéro de port par défaut a été modifié en 6432. Les utilisateurs individuels existants n'ont pas besoin de procéder à une modification, mais si vous distribuez des paquets de PgBouncer, veuillez modifier le port par défaut du paquet pour qu’il corresponde au port officiel.

  * Création dynamique de bases de données (David Galoyan)

    Now you can define database with name "*".  If defined, it's connect
    string will be used for all undefined databases.  Useful mostly
    for test / dev environments.

  * Prise en charge Windows (Hiroshi Saito)

    PgBouncer runs on Windows 2000+ now.  Command line usage stays same,
    except it cannot run as daemon and cannot do online reboot.
    To run as service, define parameter service_name in config. Then:

        > pgbouncer.exe config.ini -regservice
        > net start SERVICE_NAME

    To stop and unregister:

        > net stop SERVICE_NAME
        > pgbouncer.exe config.ini -unregservice

    To use Windows Event Log, event DLL needs to be registered first:

        > regsrv32 pgbevent.dll

    Afterwards you can set "syslog = 1" in config.

- Fonctionnalités mineures

  * Les noms de bases de données dans le fichier de configuration peuvent désormais être entre guillemets à l'aide de la syntaxe standard SQL d'identification, afin de permettre l'utilisation de caractères non standards dans les noms de bases.

  * Nouveaux paramètres ajustables : 'reserve_pool_size' et 'reserve_pool_timeout'.
    En cas de clients dans le pool ayant attendu plus de
    'reserve_pool_timeout' secondes, 'reserve_pool_size' indique
    le nombre de connexions pouvant être ajoutées au pool. Il peut également
    être défini par pool à l'aide de la variable de connexion 'reserve_pool'.

  * Nouvelle option réglable 'sbuf_loopcnt' pour limiter le temps passé sur une socket.

    In some situations - eg SMP server, local Postgres and fast network -
    pgbouncer can run recv()->send() loop many times without blocking
    on either side.  But that means other connections will stall for
    a long time.  To make processing more fair, limit the times
    of doing recv()->send() one socket.  If count reaches limit,
    just proceed processing other sockets.  The processing for
    that socket will resume on next event loop.

    Thanks to Alexander Schocke for report and testing.

  * L'authentification crypt() est désormais facultative, puisqu'elle a été supprimée de Postgres.
Si le système d'exploitation ne la fournit pas, PgBouncer fonctionne correctement sans elle.

  * Ajoutez des millisecondes aux horodatages de journalisation.

  * Remplacer l’implémentation MD5 ancienne par une version plus compacte.

  * Mettre à jour la licence ISC avec la clarification de la FSF.

- Correctifs

  * En cas d'échec de event_del(), procédez simplement au nettoyage.
    Auparavant, PgBouncer tentait de le réessayer si l'échec était dû à ENOMEM.
    Mais cela a provoqué des inondations de logs avec des répétitions infinies, si bien que
    libevent ne semble pas le supporter.

    Why event_del() report failure first time is still mystery.

  * --enable-debug ne contrôle désormais plus que le retrait des informations de débogage du binaire.
Il n'interagit plus avec -fomit-frame-pointer car cela est dangereux.

  * Corrige l'ordre d'inclusion, car sinon les fichiers d'inclusion système pourraient être chargés avant les fichiers internes. Ce problème affectait le fichier d'en-tête md5.h récent.

  * Inclure le fichier COPYRIGHT dans le .tgz...

--------

## PgBouncer 1.2.x {#pgbouncer-12x}

**2008-08-08  -  PgBouncer 1.2.3  -  « Bytes soigneusement sélectionnés »**

- Correctifs
  * Désactive le code SO_ACCEPTFILTER pour les BSDs qui ne fonctionnaient pas.
  * Inclut l'exemple etc/userlist.txt dans le fichier tgz.
  * Utilise '$(MAKE)' au lieu de 'make' pour la récursion (Jorgen Austvik).
  * Définit _GNU_SOURCE car glibc est inutilisable autrement.
  * Permet à libevent 1.1 de passer le test de liaison afin que nous puissions plus tard indiquer « 1.3b+ requis ».
  * Détecte les fichiers PID obsolètes et les supprime.

Merci à Devrim GUNDUZ et à Bjoern Metzdorf pour leurs rapports de problèmes et leurs tests.

**2008-08-06  -  PgBouncer 1.2.2  -  « Barf-bag inclus »**

- Correctifs
  * Supprimez 'drop_on_error', cela était une mauvaise idée. Il a été ajouté comme solution de contournement
    pour un comportement défectueux du cache de plan dans Postgres, mais peut entraîner des dommages
    dans le cas courant où certaines requêtes renvoient toujours une erreur.

**2008-08-04  -  PgBouncer 1.2.1  -  « Waterproof »**

- Fonctionnalités
  * Nouveau paramètre 'drop_on_error' – si le serveur génère une erreur, la connexion ne sera pas réutilisée mais supprimée après que le client l'ait terminée. Cela est nécessaire pour actualiser le cache des plans. L'actualisation automatique ne fonctionne pas même dans la version 8.3. Valeur par défaut : 1.
- Correctifs
  * COMMANDE SHOW SOCKETS/CLIENTS/SERVERS : ne plus planter si la socket n'a pas de tampon.
  * Correction de la boucle infinie lors de SUSPEND si suspend_timeout est déclenché.
- Nettoyages mineurs
  * Utilisation de <sys/uio.h> pour 'struct iovec'.
  * Annuler l'arrêt (provenant de SIGINT) lors de RESUME/SIGUSR2, sinon il sera déclenché lors du prochain PAUSE.
  * Message de journalisation correct si une opération de console est annulée.

**2008-07-29  -  PgBouncer 1.2  -  « Flûte magique ordinaire »**

PgBouncer 1.2 nécessite désormais la bibliothèque libevent version 1.3b ou ultérieure.
Les versions anciennes de libevent plantent avec le nouveau code de redémarrage.

- Fonctionnalités

  * Option de ligne de commande (-u) et paramètre de configuration (user=) pour prendre en charge le changement d'utilisateur au démarrage. pgbouncer refuse désormais de s'exécuter en tant qu'utilisateur root.

    (Jacob Coby)

  * Texte d'utilisation plus descriptif (-h).  (Jacob Coby)

  * Nouvelle option de base de données : connect_query permettant d'exécuter une requête sur les nouvelles connexions avant qu'elles ne soient utilisées.

    (Teodor Sigaev)

  * Nouvelle variable de configuration 'ignore_startup_parameters' permettant d'autoriser ou d'ignorer des paramètres supplémentaires dans le paquet de démarrage. Par défaut, seuls les paramètres « database » et « user » sont autorisés ; tous les autres provoquent une erreur. Cette fonctionnalité est nécessaire pour tolérer les comportements excessivement ambitieux de JDBC, qui tente de définir inconditionnellement « extra_float_digits=2 » dans le paquet de démarrage.

  * Journalisation vers syslog : nouveaux paramètres syslog=0/1 et
    syslog_facility=daemon/user/local0.

  * Redémarrage en ligne moins effrayant (-R)

    - Déplacer le chargement des descripteurs avant le fork, afin qu'il s'affiche dans la console et puisse être interrompu par ^C

    - Conserver SHUTDOWN après fork, afin que ^C soit sécurisé

    - Une tentative de connexion à la socket Unix est effectuée afin de vérifier si un processus écoute déjà.
À présent, -R peut être utilisé même si aucun processus précédent n'était en cours d'exécution. Si un processus précédent existe, mais que -R n'est pas utilisé, le démarrage échoue.

  * Nouvelles commandes de la console :

    - SHOW TOTALS affiche un résumé des statistiques (tel qu'il apparaît dans les journaux) ainsi que l'utilisation mémoire.

    - SHOW ACTIVE_SOCKETS - comme show sockets ; mais filtre uniquement les connexions actives.

- Fonctionnalités moins visibles

  * suspend_timeout - fermer les connexions bloquées et les connexions longues en cours de connexion. Cela ajoute une sécurité supplémentaire lors d'un redémarrage.

  * Lorsqu'une base de données distante génère une erreur lors de la connexion, avertir les clients.

  * Supprimer une base de données de la configuration et recharger le fichier fonctionne : toutes les connexions sont interrompues et la base de données est supprimée.

  * Faux des paramètres dans les commandes SHOW/SET de la console pour qu’elles ressemblent davantage à celles de Postgres.
    C’était nécessaire pour permettre à psycopg de se connecter à la console.
    (client_encoding/isolation_transaction_par défaut/datestyle/timezone)

  * Définir server_lifetime=0 pour déconnecter immédiatement la connexion au serveur après sa première utilisation. Une valeur « 0 » précédemment signifiait que PgBouncer ignorait l'âge du serveur. Comme ce comportement n'était pas documenté, il ne devrait pas y avoir d'utilisateurs qui en dépendent.

  * Améliorations internes :

    - Les tampons de paquets sont alloués de manière paresseuse et réutilisés. Cela devrait entraîner une réduction importante de l'utilisation mémoire. Cela permet également de raisonnablement utiliser un grand pktbuf avec un grand nombre de connexions.

    - Nombreuses améliorations de gestion des erreurs ; PgBouncer devrait désormais survivre aux situations de manque de mémoire (OOM) de manière correcte.

    - Utiliser l'allocateur de tranches pour la gestion de la mémoire.

    - Nombreux nettoyages de code.

- Correctifs

  * Un seul appel à accept() était effectué par boucle d'événements, ce qui pouvait entraîner une file d'attente de connexions en cas d'importantes tentatives de connexion. Le socket d'écoute est désormais toujours entièrement vidé, ce qui devrait résoudre ce problème.
  * Gérer EINTR provenant de connect().
  * Assurer la compatibilité de configure.ac avec autoconf 2.59.
  * Correctifs de compatibilité pour Solaris (Magne Maehre)

--------

## PgBouncer 1.1.x {#pgbouncer-11x}

**2007-12-10  -  PgBouncer 1.1.2  -  "The Hammer**

- Fonctionnalités
  * Les déconnexions dues à server_lifetime sont désormais espacées de
    (server_lifetime / pool_size) secondes. Cela empêche PgBouncer de provoquer des tempêtes de reconnexion.
- Correctifs
  * Problèmes liés à la mise à jour en ligne de la version 1.0 vers la 1.1 :
    - La version 1.0 ne suit pas les paramètres serveur, qui restent donc à NULL,
      mais la version 1.1 ne s'attendait pas à cette situation et plantait.
    - Si les paramètres serveur sont inconnus, mais que ceux du client sont définis,
      émettre une commande SET pour ces derniers, plutôt que de générer une erreur.
  * Suppression des instructions de débogage temporaires qui avaient été accidentellement laissées
    dans le code au niveau INFO, afin d'éviter qu'elles ne polluent les journaux.
  * Réparation du fichier debian/changelog
- Nettoyage
  * Réorganisation des champs de la structure SBuf pour obtenir un meilleur alignement du tampon.

**2007-10-26  -  PgBouncer 1.1.1  -  "Breakdancing Bee**

- Correctifs
  * Le paramètre serveur cache pouvait rester non initialisé, ce qui entraînait un SET inutile. Cela provoquait un problème sur la version 8.1, qui ne permet pas de modifier standard_conforming_strings.
    (Merci à Dimitri Fontaine pour le rapport et les tests.)
  * Quelques corrections dans la documentation.
  * Inclure doc/fixman.py dans le fichier .tgz.

**2007-10-09  -  PgBouncer 1.1  -  "Mad-Hat Toolbox**

- Fonctionnalités

  * Suivez les paramètres de serveur suivants :

        client_encoding  datestyle, timezone, standard_conforming_strings

  * Améliorations de la chaîne de connexion à la base de données  :

    - Accepter le nom d'hôte dans host=
    - Accepter un emplacement personnalisé de socket Unix dans host=
    - Accepter les valeurs entre guillemets : password=' asd''foo'

  * Nouvelle variable de configuration : server_reset_query, envoyée immédiatement après la libération.
  * Nouvelle variable de configuration : server_round_robin, pour basculer entre LIFO et RR.
  * Le paquet d'annulation envoyé pour une connexion inactif ne la supprime plus.
  * L'annulation avec ^C depuis psql fonctionne pour SUSPEND / PAUSE.
  * Afficher les limites de descripteurs de fichiers au démarrage.
  * Lors de la suspension, tenter d'atteindre une frontière de paquet dès que possible.
  * Ajouter 'timezone' aux paramètres de base de données.
  * Utiliser un descripteur de fichier de journal longévité. Réouvert en cas de SIGHUP / RELOAD ;
  * Informations sur le point de terminaison local des connexions dans SHOW SERVERS/CLIENTS/SOCKETS.

- Nettoyage du code

  * Plus de messages de journalisation détaillés incluent des informations sur les sockets.
  * Suppression du nombre magique et nettoyage des messages d'erreur. (David Fetter)
  * Structure d'enveloppe pour les informations sur le paquet courant. Élimine une grande partie de la complexité.

- Correctifs

  * Détecter mieux les en-têtes de paquets invalides.
  * La vérification des modifications du fichier d'authentification était défectueuse, ce qui poussait PgBouncer à le recharger trop souvent.

--------

## PgBouncer 1.0.x {#pgbouncer-10x}

**2007-06-18  -  PgBouncer 1.0.8  -  « Jutsu de pelle zombie »**

- Correctifs
  * Correction d'un plantage lors du traitement du paquet d'annulation. (^C depuis psql)
- Fonctionnalités
  * PAUSE <db> ; RESUME <db> ; fonctionne désormais.
  * Nettoyage de l'analyse des commandes de la console d'administration.
  * Désactivation de la vérification coûteuse de type in-list.

**2007-04-19  -  PgBouncer 1.0.7  -  « With Vitamin A-Z »**

- Correctifs
  * Plusieurs paquets d'erreur/avis avec send() bloquant entre des assertions déclenchées. Corriger en supprimant entièrement la logique de vidage. Comme pgbouncer ne fait aucun tamponnage actif, cette logique n'est pas nécessaire. Il s'agissait d'un vestige de l'époque où le tamponnage était transféré au noyau via MSG_MORE.
  * Éviter également d'appeler la logique recv() lorsque l'envoi est débloqué.
  * Code de recherche dans la liste pour admin_users et stats_users traitait incorrectement les recherches partielles. Correction apportée.
  * Uniformiser la recherche de l'UID du pair sur les sockets UNIX avec getpeereid().

**2007-04-12  -  PgBouncer 1.0.6  -  « Daily Dose »**

- Correctifs
  * Le correctif « Désactiver la maintenance pendant la prise de contrôle » pouvait désactiver la maintenance de manière globale. Corriger cela.
  * Correctif de compilation pour FreeBSD, <sys/ucred.h> nécessite <sys/param.h>.
Merci à Robert Gogolok pour le signalement.

**2007-04-11  -  PgBouncer 1.0.5  -  « Enough for today »**

- Correctifs
  * Correction des bugs liés au redémarrage en ligne :
    - Définir -> prêt pour les serveurs inactifs.
    - Suppression du code obsolète dans use_client_socket()
    - Désactivation de la maintenance pendant la prise de contrôle.

**2007-04-11  -  PgBouncer 1.0.4  -  « Dernier bogue « last » »**

- Correctifs
  * Avertissement provenant d'un serveur inactif marqué comme sale.
    release_server() ne s'y attendait pas. Corrigez-le
    en les supprimant.

**2007-04-11  -  PgBouncer 1.0.3  -  « Fearless Fork »**

- Correctifs
  * Un traitement d'erreur manquait dans le chemin de connexion, ce qui pouvait déclencher des assertions lors de la fermeture d'une connexion.
  * Nettoyage des assertions dans sbuf.c afin de détecter les problèmes plus tôt.
  * Générer un fichier core lorsque Assert() est déclenché.

- Nouvelles fonctionnalités
  * Nouvelles variables de configuration : log_connections, log_disconnections,
    log_pooler_errors pour activer/désactiver le bruit d'audit.
  * Variable de configuration : client_login_timeout pour tuer les connexions inactives
    pendant la phase d'authentification qui pourraient bloquer SUSPEND et donc le redémarrage en ligne.

**2007-03-28  -  PgBouncer 1.0.2  -  « Supersonic Spoon »**

- Correctifs
  * libevent peut signaler un événement supprimé à l'intérieur de la même boucle.
    Éviter la réutilisation du socket pour une même boucle.
  * release_server() appelé depuis disconnect_client() ne vérifiait pas
    si le paquet avait effectivement été envoyé.

**2007-03-15  -  PgBouncer 1.0.1  -  « Technologie alien »**

- Correctifs
  * Utilisation mixte du temps mis en cache et du temps non mis en cache, ainsi que l'utilisation non signée du type typedef *usec_t*
    provoquait des erreurs de timeout de requête erronées.
  * Correction d'un cas rare où une socket réveillée depuis un état d'attente d'envoi pouvait rester bloquée.
  * File d'attente des connexions serveur plus équitable. Avant, une nouvelle requête pouvait obtenir une connexion serveur avant une requête plus ancienne.
  * Retarder la libération du serveur jusqu'à ce que tout soit garanti comme envoyé.

- Fonctionnalités
  * Commande SHOW SOCKETS pour obtenir des informations détaillées sur l'état.
  * Inclure le pointeur PgSocket dans les journaux, afin de faciliter le suivi d'une connexion.
  * Dans la console, autoriser SELECT à la place de SHOW.
  * Diverses nettoyages de code.

**2007-03-13  -  PgBouncer 1.0  -  "Tuunitud bemm**

- Première version publique.
