---
title: "Notes de version"
linkTitle: "Versions"
weight: 60
description: "Historique des versions de pgBackRest avec un journal des modifications détaillé pour chaque version."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [Référence]
aliases: [/pgbackrest/release/]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## Introduction {#introduction}

Les numéros de version de pgBackRest se composent de deux parties : majeure et mineure. Une version majeure *peut* rompre la compatibilité avec la version majeure précédente, mais les versions v2 sont entièrement compatibles avec les dépôts v1 et acceptent toutes les options v1. Les versions mineures peuvent inclure des correctifs et des fonctionnalités, mais ne modifient pas le format du dépôt et s'efforcent d'éviter tout changement aux options et aux noms. La documentation de la version v1 est disponible [ici](https://pgbackrest.org/1). Les notes relatives à une version peuvent également contenir des « Notes supplémentaires », mais les modifications dans cette section n'ont d'impact direct que sur la documentation ou le jeu de tests et n'affectent pas le codebase de pgBackRest.


--------

## Version stable actuelle {#current-stable-release}

Ce miroir couvre la v2.59.3. Consultez l'[historique des versions amont](https://pgbackrest.org/release.html) pour les versions plus récentes.

### Notes de version v2.59.3 {#v2593-release-notes}

*Bogue des sous-clés de chiffrement faibles*

*Publié le 4 octobre 2026*

**REMARQUE IMPORTANTE**: Dans les versions précédentes, une erreur d’accès aux données aléatoires du système pouvait entraîner la génération de sous-clés de chiffrement et de sels faibles. Consultez [Sous-clés de chiffrement et sels faibles](/fr/docs/pgbackrest/news/#weak-encryption) pour plus d’informations.

**Correctifs de bogues:**

- Correction d’une possible erreur de somme de contrôle lors du chargement des fichiers d’information et des manifestes chiffrés. (*Corrigé par j0uinim. Relu par David Steele.*)
- Correction de la génération possible de sous-clés de chiffrement ou de sels faibles. (*Corrigé par j0uinim. Relu par David Steele, Stefan Fercot, Douglas J Hunley.*)


--------


## Versions stables {#stable-releases}


### Notes de version v2.59.2 {#v2592-release-notes}

*Prise en charge de PostgreSQL 19beta4*

*Sortie le 27 septembre 2026*

**Correctifs de bogues :**

- Corriger la carte de blocs vide lorsqu'un fichier est tronqué à zéro pendant la sauvegarde. (*Révisé par Douglas J Hunley. Signalement par JPCOSTA78.*)
- Désactiver la nouvelle tentative de lecture lorsque des filtres sont passés au pilote. (*Révisé par Douglas J Hunley. Signalement par megamaced.*)
- Corriger la pagination de la liste des versions S3. (*Révisé par Douglas J Hunley, guruguruguru. Signalement par guruguruguru.*)
- Définir l'en-tête de version Azure pour l'authentification SAS. (*Révisé par Douglas J Hunley. Signalement par Florian Helmberger.*)
- Corriger le blocage de `archive-push` asynchrone sur un fichier d'historique de sauvegarde de taille nulle. (*Corrigé par Andrew Kroh. Révisé par David Steele, Douglas J Hunley.*)
- Corriger la commande `annotate` sur un dépôt distant chiffré. (*Corrigé par Douglas J Hunley. Révisé par David Steele.*)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta4.



### Notes de version v2.59.1 {#v2591-release-notes}

*Prise en charge de PostgreSQL 19beta3*

*Sortie le 17 août 2026*

**Correctifs de bogues :**

- Corriger le blocage lorsque la taille du tampon de morceau est inférieure à celle du tampon d'entrée. (*Révisé par Andrew Pogrebnoi, Douglas J Hunley. Signalement par crajac66.*)
- Comparer une étiquette de sauvegarde nouvelle uniquement avec son propre jeu de sauvegardes complètes. (*Révisé par Douglas J Hunley. Signalement par Anton Glushakov.*)
- Corriger les archives sources générées par GitHub qui manquent des fichiers nécessaires à la compilation. (*Signalement par aardvarkzed.*)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta3. (*Contribution de Lardière Sébastien. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Documenter l'exception pour les points dans les noms de bucket S3 lorsque `repo-s3-uri-style=path`.
- Suppression de la configuration explicite `hot_standby` du guide utilisateur.


### Notes de version v2.59.0 {#v2590-release-notes}

*Prise en charge de PostgreSQL 19beta2*

*Sortie le 20 juillet 2026*

**NOTE AUX PAQUETEURS** : Un nouveau paquet source est disponible, qui simplifie le processus de compilation en fournissant une documentation HTML prégénérée, une page de manuel et du code. Ce paquet est joint à chaque version comme un élément et porte le nom `pgbackrest-{version}.tar.gz`. Consultez `README.md` dans le paquet pour plus de détails. Veuillez utiliser ce nouveau paquet source afin d’éviter les outils supplémentaires nécessaires à la génération du code dans les versions futures. Consultez [Nouveau paquet source](/fr/docs/pgbackrest/news/#distribution-tarball) pour plus d’informations. **NOTE AUX PAQUETEURS** : Une dépendance optionnelle supplémentaire est désormais requise : `libsystemd`. **NOTE IMPORTANTE** : À compter de cette version, seule la commande `restore` peut être exécutée en tant que root par défaut. Utilisez `allow-root` pour exécuter d'autres commandes en tant que root (ce qui n’est toutefois pas recommandé).

**Correctifs de bogues :**

- Corriger la suppression par `expire` d'une sauvegarde en cours sur un autre hôte. (*Révisé par Douglas J Hunley. Signalement par Dmitrii.*)
- Corriger la non-application de `archive-push-queue-max` lorsqu'un fichier WAL provoque une erreur. (*Révisé par Stefan Fercot. Signalement par vut12.*)
- Corriger l'échec asynchrone de `archive-get` pendant une récupération traversant un changement de timeline. (*Révisé par Douglas J Hunley. Signalement par Jimmy Yih.*)
- Corriger un possible dépassement de tampon dans le module d'erreur. (*Corrigé par Christophe Pettus. Révisé par David Steele.*)
- Corriger une utilisation après libération du client du protocole parallèle. (*Révisé par Douglas J Hunley. Signalement par Georgy Shelkovy.*)
- Corriger un dépassement de tas lorsqu'une option pg est définie sans pg1. (*Révisé par Douglas J Hunley. Signalement par Naveen.*)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta2. (*Révisé par Stefan Fercot.*)
- Ajout de l'option `archive-expire-before` pour nettoyer l'archive WAL. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Ajout de la suppression par lots pour le stockage Azure. (*Révisé par Douglas J Hunley, Crispy.*)
- Ajout de la prise en charge des S3 Outposts. (*Contribution de Shiva Kumar Ambigi. Révisé par David Steele, Roberto Mello.*)
- Ajout de l'authentification par processus S3. (*Révisé par Andrew Charlton. Suggéré par Andrew Charlton.*)

**Améliorations :**

- Reconnecter le stockage SFTP après que le serveur a fermé une connexion inactive. (*Révisé par Stefan Fercot. Suggéré par mustafa0x, tisserat.*)
- Ajouter le cache utilisateur/groupe pour une construction plus rapide du manifeste. (*Contribution de Gunnar Lindholm. Révisé par David Steele.*)
- Ajouter la progression de sauvegarde par dépôt dans la sortie de la commande `info`. (*Contribution de Will Morland. Révisé par David Steele, Stefan Fercot.*)
- Ajouter des vérifications `backup.info` à la commande `verify`. (*Contribution de Denis Garsh. Révisé par David Steele, Douglas J Hunley.*)
- Permettre la configuration du point de terminaison S3 STS. (*Contribution de Simon Gratton. Révisé par David Steele.*)
- Ajouter `archive-push-batch-size` pour limiter la quantité de WAL envoyée par exécution asynchrone. (*Révisé par Stefan Fercot.*)
- Quitter l'opération asynchrone `archive-push` à la première erreur. (*Révisé par Stefan Fercot. Suggéré par Lardière Sébastien.*)
- Renforcer l'analyse des réponses HTTP chunkées. (*Contribution de Shubham. Révisé par David Steele.*)
- Erreur lors de l'exécution en tant que root sauf si `allow-root` est activé. (*Révisé par Douglas J Hunley.*)
- Moins de recherches binaires lors de la construction du manifeste. (*Contribution de Gunnar Lindholm. Révisé par David Steele.*)
- Améliorer les performances de recherche lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par David Christensen, Douglas J Hunley.*)
- Regrouper les fichiers de sauvegarde dans l'ordre plutôt que de rechercher un meilleur ajustement. (*Révisé par Stefan Fercot.*)
- Signaler l'erreur sous-jacente lorsqu'une requête échoue à se terminer. (*Révisé par Andrew Pogrebnoi. Suggéré par Marco Fontana.*)
- Signaler l'erreur réelle lorsqu'une requête de crédentials S3 échoue. (*Révisé par Douglas J Hunley. Suggéré par Mitchell Grice.*)
- Signaler les erreurs de chemin de stockage temporaire `archive-push` dans le journal PostgreSQL. (*Révisé par Douglas J Hunley. Suggéré par Don Seiler.*)
- Indication que pgBackRest pourrait être obsolète lorsqu'une version n'est plus prise en charge.
- Ajouter l'intégration avec systemd notify. (*Contribution de Andrew Jackson. Révisé par David Steele.*)
- Supprimer les erreurs `unused parameter` des sondes du compilateur meson. (*Contribution de Jörg Plate. Révisé par David Steele.*)
- C11 est désormais la norme C minimale. (*Révisé par Mohammad Ali Nazir Kosar.*)

**Améliorations de la documentation :**

- Rendre l'option `stanza` interne pour les commandes `repo-*`. (*Révisé par Stefan Fercot.*)
- Documenter le fait que les paramètres de chiffrement sont lus à partir de la section globale. (*Révisé par Stefan Fercot. Suggéré par Ron Johnson.*)
- Documenter que `expire-auto` utilise la configuration de la commande `backup`. (*Révisé par Stefan Fercot. Suggéré par Lardière Sébastien.*)
- Documenter l'ajustement de la directive `su` de logrotate pour un utilisateur dédié. (*Révisé par Douglas J Hunley. Suggéré par lkanbus.*)
- Documenter que les commentaires se terminant à la fin de ligne ne sont pas pris en charge dans les fichiers de configuration. (*Révisé par Douglas J Hunley. Suggéré par Alex Richman.*)

**Améliorations de la suite de tests :**

- Corriger les conflits de groupes dans les conteneurs CI Alpine. (*Contribution de Artur Zakirov. Révisé par David Steele.*)

### Notes de version v2.58.0 {#v2580-release-notes}

*Améliorations du stockage objet*

*Sortie le 19 janvier 2026*

**AVERTISSEMENT IMPORTANT** : Les valeurs minimales de l'option `repo-storage-upload-chunk-size` ont augmenté. Elles correspondent désormais au minimum autorisé par les fournisseurs.

**Correctifs de bogues :**

- Corriger un blocage dû à la journalisation dans un gestionnaire de signal. (*Corrigé par Maxim Michkov. Révisé par David Steele.*)

**Fonctionnalités :**

- Prise en charge HTTP pour S3, GCS et Azure. (*Contribution de Will Morland. Révisé par David Steele.*)
- Permettre l'expiration de la sauvegarde complète la plus ancienne, indépendamment de la rétention actuelle. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Ron Johnson.*)
- Prise en charge des identités gérées Azure. (*Contribution de Moiz Ibrar, Matthew Mols. Révisé par David Steele.*)
- Prise en charge ***expérimentale*** de l'identité de pod S3 EKS. (*Contribution de Pierre BOUTELOUP. Révisé par David Steele.*)
- Permettre la configuration des suites de chiffrement TLS. (*Contribution de Gunnar "Nick" Bluth. Révisé par David Steele.*)
- Permettre la définition de la priorité du processus. (*Révisé par Douglas J Hunley.*)

**Améliorations :**

- Autoriser les points dans les noms de bucket S3 lors de l'utilisation d'URI en style chemin. (*Contribution de Joakim Hindersson. Révisé par David Steele.*)
- Exiger TLS >= 1.2 sauf si la vérification est désactivée. (*Révisé par Douglas J Hunley, Gunnar "Nick" Bluth.*)
- Ajuster dynamiquement la taille des morceaux S3/GCS/Azure pour les téléversements volumineux. (*Révisé par Douglas J Hunley. Suggéré par Timothée Peignier.*)
- Optimiser la taille des morceaux S3/GCS/Azure pour les petits fichiers. (*Révisé par Douglas J Hunley.*)
- Supprimer le support de PostgreSQL `9.5`. (*Révisé par Douglas J Hunley.*)
- Améliorer la journalisation de la valeur par défaut pour les options ayant une dépendance non résolue. (*Révisé par Stefan Fercot.*)

**Améliorations de la documentation :**

- Supprimer la configuration explicite `max_wal_senders`/`wal_level` du guide utilisateur. (*Suggéré par Jamie Nguyen.*)
- Préciser que le regroupement est utile pour les systèmes de fichiers à grandes tailles de bloc. (*Suggéré par Ron Johnson.*)


### Notes de version v2.57.0 {#v2570-release-notes}

*Supprimer les liens symboliques du dépôt*

*Sortie le 18 octobre 2025*

**Correctifs de bogues :**

- Décongestionner les délais d'attente HTTP/TLS/socket. (*Révisé par David Christensen.*)
- Corriger un éventuel plantage dans le message d'erreur de somme de contrôle de page. (*Corrigé par Zsolt Parragi. Révisé par David Steele.*)

**Fonctionnalités :**

- Ajouter l'option `repo-symlink` pour supprimer la création des liens symboliques du dépôt. (*Révisé par Douglas J Hunley. Suggéré par Ron Johnson.*)

**Améliorations :**

- Ajouter des tentatives HTTP pour les erreurs 408 et 429. (*Révisé par David Christensen.*)


### Notes de version v2.56.0 {#v2560-release-notes}

*Améliorations des informations de progression*

*Sortie le 21 juillet 2025*

**Correctifs de bogues :**

- Corriger le problème d'expiration à la demande lorsque aucune sauvegarde n'est présente dans un dépôt. (*Révisé par Stefan Fercot. Signalement par Anup Gupta.*)

**Fonctionnalités :**

- Ajouter la progression de la restauration à la sortie de la commande `info`. (*Contribution de Denis Garsh, Maxim Michkov. Révisé par David Steele.*)
- Ajouter le niveau de détail « progression uniquement » à la sortie de la commande `info`. (*Contribution de Denis Garsh. Révisé par David Steele, Stefan Fercot.*)

**Améliorations :**

- Réessayer les lectures échouées sur les magasins d'objets. (*Révisé par David Christensen.*)
- Corriger les valeurs par défaut dans l'aide en ligne de commande. (*Révisé par David Christensen, Chris Bandy.*)

**Améliorations de la documentation :**

- Décrivez les valeurs d'option discrètes sous forme de liste lorsque cela est approprié. (*Contribution de Anton Kurochkin. Révisé par David Steele.*)
- Corrigez « inférieur à » dans la sortie d'aide pour l'option `archive-mode`. (*Contribution de Anton Kurochkin. Révisé par David Steele.*)


### Notes de version v2.55.1 {#v2551-release-notes}

*Correctifs de bogues*

*Sortie le 5 mai 2025*

**Correctifs de bogues :**

- Annuler « calculer le content-md5 sur S3 uniquement lorsqu'il est nécessaire ». (*Révisé par David Christensen. Signalement par Frank Brendel.*)
- Corriger la vérification des bornes inférieures pour les clés d'option. (*Révisé par David Christensen, Wolfgang Walther. Signalement par Wolfgang Walther.*)


### Notes de version v2.55.0 {#v2550-release-notes}

*Améliorations de vérification et prise en charge de PostgreSQL 18*

*Sortie le 21 avril 2025*

**Correctifs de bogues :**

- Corriger le problème de restauration incrémentielle par bloc sur un dépôt non par défaut. (*Révisé par David Christensen, Aleksander Łukasz. Signalement par Aleksander Łukasz.*)
- Ne pas définir `recovery_target_timeline=current` pour PostgreSQL < 12. (*Révisé par Stefan Fercot.*)
- Corriger la journalisation de la plage d'archives expirées. (*Révisé par Stefan Fercot. Signalement par Aleš Zelený.*)
- Corriger le rapport d'erreur pour les requêtes sans résultat. (*Révisé par Stefan Fercot. Signalement par Susantha Bathige.*)

**Fonctionnalités :**

- Vérifier le timeline cible de la récupération. (*Révisé par Stefan Fercot.*)
- Permettre la vérification d'une sauvegarde spécifiée. (*Contribution de Maxim Michkov. Révisé par David Steele.*)
- Ajouter la prise en charge de « requester pays » (paiement par le demandeur) pour S3/GCS. (*Contribution de Timothée Peignier. Révisé par David Steele.*)
- Prise en charge de PostgreSQL 18. (*Révisé par Stefan Fercot.*)
- Permettre les connexions à PostgreSQL via des sockets de domaine abstraits. (*Révisé par Chris Bandy. Suggéré par Chris Bandy.*)
- Ajouter une sortie numérique à la commande `version`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

**Améliorations :**

- Autoriser la commande de sauvegarde à fonctionner sur des dépôts distants. (*Révisé par Stefan Fercot.*)
- Utiliser lz4 pour la compression du protocole. (*Révisé par Stefan Fercot.*)
- Calculer `content-md5` sur S3 uniquement lorsqu'il est nécessaire. (*Révisé par David Christensen.*)
- Afficher un avertissement lorsque la valeur d'une option à plusieurs clés est remplacée. (*Révisé par David Christensen, Stefan Fercot.*)
- Ajouter un journal détaillé pour le chemin d'archive expiré. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Supprimer le support de PostgreSQL `9.4`. (*Révisé par Stefan Fercot.*)
- Supprimer la construction autoconf/make. (*Révisé par David Christensen.*)

**Améliorations de la documentation :**

- Corriger la documentation concernant la spécification de plusieurs stanzas avec `tls-server-auth`. (*Révisé par David Christensen, Stefan Fercot. Suggéré par Terry MacAndrew.*)
- Préciser la durée de validité des sauvegardes incrémentielles. (*Révisé par Stefan Fercot.*)
- Préciser la condition de correspondance des versions locales/distantes de pgBackRest. (*Contribution de Greg Clough. Révisé par David Steele.*)
- Ajouter une question fréquente sur l'exportation d'un cluster auto-contenu. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Mise en garde concernant `--tablespace-map-all` au sujet de la création de tablespaces. (*Révisé par Stefan Fercot, Christophe Courtois. Suggéré par Christophe Courtois.*)
- Préciser le comportement de `--repo-retention-full-type`. (*Révisé par Antoine Beaupré. Suggéré par Antoine Beaupré.*)
- Modifier la recommandation concernant les magasins d'objets de `--process-max` à `--repo-bundle`. (*Révisé par Stefan Fercot.*)
- Mettre à jour `unix_socket_directory` vers `unix_socket_directories`. (*Contribution de hyunkyu han. Révisé par David Steele.*)
- Ne pas placer `spool-path` dans `pg_xlog`/`pg_wal`. (*Révisé par Martín Marqués, Don Seiler. Suggéré par Martín Marqués.*)


### Notes de version v2.54.2 {#v2542-release-notes}

*Correction de bogue*

*Sortie le 20 janvier 2025*

**Correctifs de bogues :**

- Corriger le problème survenu après avoir désactivé le regroupement avec l'incrémentation par bloc activée. (*Révisé par David Christensen.*)

**Améliorations de la documentation :**

- Préciser le comportement des fichiers de configuration multiples. (*Révisé par Paul Bierly. Suggéré par Paul Bierly.*)


### Notes de version v2.54.1 {#v2541-release-notes}

*Correction de bogue*

*Sortie le 16 décembre 2024*

**Correctifs de bogues :**

- Corriger le problème lié aux commandes `version`/`help` qui tentaient de charger `pgbackrest.conf`. (*Révisé par Stefan Fercot. Signalement par Bradford Boyle, Julian.*)

**Améliorations de la suite de tests :**

- Stabiliser l'archivage asynchrone dans les tests d'intégration. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)


### Notes de version v2.54.0 {#v2540-release-notes}

*Instant cible pour le stockage versionné*

*Sortie le 21 octobre 2024*

**NOTE AUX PAQUETEURS** : Cette version est la dernière à prendre en charge la construction autoconf/make. Veuillez migrer vers meson si ce n’est pas déjà fait. Les correctifs de version 2.54.X (le cas échéant) continueront à prendre en charge autoconf/make.

**Correctifs de bogues :**

- Corriger les performances des requêtes PostgreSQL sur de grands jeux de données. (*Corrigé par Thibault Vincent, David Steele. Révisé par David Christensen, Antoine Millet. Signalement par Antoine Millet.*)

**Fonctionnalités :**

- Autorise la lecture des dépôts sur un stockage versionné à un instant cible. (*Révisé par Stefan Fercot, David Christensen.*)

- Autorise l'exécution de la sauvegarde demandée depuis un serveur secondaire, même en l'absence de serveur secondaire. (*Révisé par Stefan Fercot.*)

**Améliorations :**

- Résumer la liste de référence des sauvegardes dans la sortie texte de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Actualiser le jeton web-id pour chaque authentification S3. (*Contribution de Brent Graveland. Révisé par David Steele.*)
- Afficher correctement les valeurs actuelles des options indexées dans l’aide. (*Révisé par David Christensen.*)
- Enregistrer `backup.info` uniquement lorsque son contenu a changé. (*Révisé par Stefan Fercot.*)
- Supprimer la limitation relative à la lecture de fichiers en parallèle lors d’une restauration. (*Révisé par David Christensen.*)
- Améliorer les messages d’erreur SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)

**Fonctionnalités de la documentation :**

- Ajouter une section d'optimisation des performances au guide utilisateur. (*Révisé par Stefan Fercot.*)

**Améliorations de la documentation :**

- Préciser la source de `data_directory`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Matthias.*)
- Meilleure logique pour déterminer quand un résumé doit être en minuscules. (*Suggéré par Daniel Westermann.*)


### Notes de version v2.53.1 {#v2531-release-notes}

*Prise en charge de PostgreSQL 17*

*Sortie le 19 août 2024*

**Correctifs de bogues :**

- Corrigez les permissions lorsque `restore` est exécuté en tant qu'utilisateur root. (*Révisé par Stefan Fercot. Signalement par Will M.*)
- Corrigez le plantage (segfault) sur les erreurs de connexion différées. (*Révisé par David Christensen. Signalement par Anton Glushakov.*)
- Ignorez la vérification des doublons du dépôt local pour SFTP. (*Corrigé par Reid Thompson. Révisé par David Steele. Signalement par Anton Kurochkin.*)

**Améliorations :**

- Prise en charge de PostgreSQL 17.


### Notes de version v2.53 {#v253-release-notes}

*Sauvegardes concurrentes*

*Sortie le 22 juillet 2024*

**NOTE IMPORTANTE** : La valeur par défaut de l'option `log-level-stderr` a été modifiée de `warn` à `off`. Cela facilite la détection des erreurs lorsqu'on redirige uniquement `stdout`. Pour conserver le comportement antérieur, définissez `log-level-stderr=warn`. **NOTE AUX PAQUETEURS** : La bibliothèque lz4 est désormais requise par la construction meson. **NOTE AUX PAQUETEURS** : La prise en charge du compilateur pour `__builtin_clzl()` et `__builtin_bswap64()` est désormais requise par la construction meson.

**Correctifs de bogues :**

- Correction d'une erreur de renommage SFTP lorsque le fichier existe déjà. (*Corrigé par Reid Thompson. Révisé par David Steele. Signalement par ahmed112212.*)

**Fonctionnalités :**

- Autoriser les sauvegardes à s'exécuter en parallèle sur des dépôts différents. (*Révisé par Reid Thompson, Stefan Fercot.*)

- Prise en charge des SAN basés sur l'IP pour la validation des certificats TLS. (*Contribution de David Christensen. Révisé par David Steele.*)

**Améliorations :**

- Définir l'option `log-level-stderr` sur `off` par défaut. (*Révisé par Greg Sabino Mullane et Stefan Fercot.*)
- Autoriser d'autres tailles de segment WAL pour PostgreSQL ≤ 10. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)
- Ajouter une indication invitant à consulter le journal d'autorisation SFTP. (*Contribution de Vitalii Zurian. Révisé par Reid Thompson et David Steele.*)

**Améliorations de la documentation :**

- Préciser le comportement multi-repo de `archive-push`. (*Révisé par Stefan Fercot.*)


### Notes de version v2.52.1 {#v2521-release-notes}

*Correction de bogue*

*Sortie le 25 juin 2024*

**Correctifs de bogues :**

- Corriger le problème des fichiers plus volumineux sur la réplique que sur le primaire. (*Révisé par Stefan Fercot. Signalement par Nicolas Lassimonne.*)


### Notes de version v2.52 {#v252-release-notes}

*Prise en charge de PostgreSQL 17beta1*

*Sortie le 27 mai 2024*

**NOTE AUX PAQUETEURS** : Le système de construction de pgBackRest est désormais meson. Le système de construction autoconf/make ne recevra plus de nouvelles fonctionnalités et sera supprimé après quelques versions.

**Fonctionnalités :**

- Ajout de la prise en charge de la suppression par lot GCS. (*Révisé par Reid Thompson.*)
- Prise en charge du chiffrement S3 `SSE-C`. (*Révisé par Tim Jones. Suggéré par Tim Jones.*)
- Prise en charge de PostgreSQL 17beta1. (*Révisé par Stefan Fercot.*)

**Améliorations :**

- Permettre la désactivation explicite des dépendances optionnelles lors des compilations meson. (*Contribution de Michael Schout. Révisé par David Steele.*)
- Rechercher dynamiquement python lors de la compilation meson. (*Contribution de Michael Schout. Révisé par David Steele.*)
- Marquer la cible de compilation `pgbackrest` comme installable dans meson. (*Contribution de Bradford Boyle. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Mettre à jour la documentation de `start`/`stop` pour qu'elle reflète la fonctionnalité réelle. (*Révisé par Stefan Fercot.*)


### Notes de version v2.51 {#v251-release-notes}

*Système de construction Meson*

*Sortie le 25 mars 2024*

**Correctifs de bogues :**

- Ignorer les fichiers de taille nulle lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par Sebastian Krause, René Højbjerg Larsen. Signalement par Sebastian Krause.*)
- Corriger la régression de performance dans la liste de stockage. (*Révisé par Stephen Frost. Signalement par Maksym Boguk.*)
- Corriger la journalisation de progression lorsque la taille du fichier change pendant la sauvegarde. (*Révisé par Stephen Frost. Signalement par samkingno.*)

**Améliorations :**

- Amélioration du support des connexions en double pile. (*Révisé par Stephen Frost. Suggéré par Timothée Peignier.*)
- Utilisation de meson comme système de construction principal. (*Révisé par Stephen Frost.*)
- Détection des fichiers inchangés lors d'une sauvegarde incrémentielle non delta. (*Révisé par Stephen Frost.*)
- Empêcher une récupération invalide lorsque `backup_label` est supprimé. (*Révisé par Stephen Frost.*)
- Amélioration de la gestion de la file d'attente des segments WAL `archive-push`. (*Révisé par Stephen Frost.*)
- Limite la fonctionnalité de reprise aux sauvegardes complètes. (*Révisé par Stephen Frost, Stefan Fercot.*)
- Mise à jour de la fonctionnalité de reprise pour les sauvegardes incrémentielles par bloc. (*Révisé par Stephen Frost.*)
- Permettre `--version` et `--help` pour la version et l'aide. (*Révisé par Greg Sabino Mullane. Suggéré par Greg Sabino Mullane.*)
- Ajout d'un backtrace détaillé dans la construction autoconf/make. (*Révisé par Stephen Frost.*)

**Améliorations de la documentation :**

- Mettre à jour les références à `recovery.conf`. (*Révisé par Stefan Fercot. Suggéré par Stephen Frost.*)


### Notes de version v2.50 {#v250-release-notes}

*Améliorations des performances et corrections de bogues*

*Sortie le 22 janvier 2024*

**Correctifs de bogues :**

- Corriger la lecture courte lors d'une restauration incrémentielle par bloc. (*Révisé par Stephen Frost, Brent Graveland. Signalement par Adol Rodriguez, Brent Graveland.*)
- Corriger la suppression de la progression de la sauvegarde dans la sortie `info`. (*Corrigé par Robert Donovan. Révisé par Joe Wildish.*)

**Améliorations :**

- Conserver les fichiers partiels lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par Stephen Frost.*)
- Ajouter la prise en charge des tailles de page alternatives au moment de la compilation. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)
- Ignorer les fichiers tronqués pendant la sauvegarde lors du regroupement. (*Contribution de Georgy Shelkovy. Révisé par David Steele.*)
- Améliorer les messages d'erreur du stockage SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)


### Notes de version v2.49 {#v249-release-notes}

*Supprimer le support de PostgreSQL 9.3*

*Sortie le 27 novembre 2023*

**Correctifs de bogues :**

- Corriger un problème de réessais. (*Révisé par Stephen Frost. Signalement par Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)
- Corriger la suppression récursive de chemins dans le pilote de stockage SFTP. (*Corrigé par Reid Thompson. Révisé par Stephen Frost. Signalement par Luc.*)

**Améliorations :**

- Supprimer le support de PostgreSQL `9.3`. (*Révisé par Stephen Frost.*)

**Fonctionnalités de la documentation :**

- Documenter les options du mainteneur. (*Révisé par Stefan Fercot.*)
- Mise à jour de la documentation de la restauration à un instant donné pour PostgreSQL >= 13.

**Améliorations de la suite de tests :**

- Autoriser l'exécution des tests unitaires `config/load` sans que `libssh2` soit installé. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Wu Ning.*)


### Notes de version v2.48 {#v248-release-notes}

*Balises de stockage du dépôt*

*Sortie le 25 septembre 2023*

**Correctifs de bogues :**

- Corriger le problème de restauration d'une sauvegarde incrémentielle par bloc sans liste de blocs. (*Révisé par Stephen Frost, Burak Yurdakul. Signalement par Burak Yurdakul.*)

**Fonctionnalités :**

- Ajouter l'option `--repo-storage-tag` pour créer des balises d'objets. (*Révisé par Stephen Frost, Stefan Fercot, Timothée Peignier.*)
- Ajouter la vérification des hôtes connus pour le pilote de stockage SFTP. (*Contribution de Reid Thompson. Révisé par Stephen Frost, David Steele.*)
- Prise en charge des connexions en double pile. (*Révisé par Stephen Frost.*)
- Ajouter la taille de la sauvegarde terminée/total à la sortie JSON de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

**Améliorations :**

- Commande de vérification multi-stanza. (*Révisé par Stephen Frost.*)
- Réessayer la lecture de `pg_control` jusqu'à ce que la somme de contrôle soit valide. (*Révisé par Stefan Fercot, Stephen Frost.*)
- Optimiser la vérification du segment WAL après une sauvegarde réussie. (*Révisé par Stephen Frost.*)
- Améliorer les performances multi-partie du GCS. (*Révisé par Reid Thompson.*)
- Permettre à la commande `archive-get` de s'exécuter lorsque la stanza est arrêtée. (*Révisé par Tom Swartz, David Christensen, Reid Thompson.*)
- Accepter un tilde initial dans les chemins pour les clés publiques/privées SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Recharger les identifiants GCS avant de renouveler le jeton d'authentification. (*Révisé par Stephen Frost. Suggéré par Daniel Farina.*)

**Correctifs de bogues dans la documentation :**

- Corriger l'exemple de référence de configuration pour l'option `tls-server-address`. (*Corrigé par Hartmut Goebel. Révisé par David Steele.*)
- Corriger l'exemple de référence de commande pour l'option `filter`.

**Améliorations de la suite de tests :**

- Autoriser l'exécution des tests unitaires `storage/sftp` sans que `libssh2` soit installé. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Wu Ning.*)


### Notes de version v2.47 {#v247-release-notes}

*Améliorations des performances et corrections de bogues*

*Sortie le 24 juillet 2023*

**Correctifs de bogues :**

- Conserver les informations incrémentielles par bloc dans le manifeste lors d'une sauvegarde incrémentielle. (*Révisé par Stephen Frost. Signalement par Francisco Miguel Biete Banon.*)
- Corriger les noms de fichiers incrémentiels dans la commande `verify`. (*Révisé par Reid Thompson. Signalement par Francisco Miguel Biete Banon.*)
- Corriger la sauvegarde delta automatique erronée lors d'une sauvegarde depuis un serveur de secours. (*Révisé par Stephen Frost. Signalement par krmozejko, Don Seiler.*)
- Ignorer `recovery.signal` pour PostgreSQL >= 12 lorsque la récupération `type=none`. (*Révisé par Stefan Fercot. Signalement par T.Anastacio.*)
- Corriger la génération de libellés uniques pour les sauvegardes diff/incr. (*Corrigé par Andrey Sokolov. Révisé par David Steele.*)
- Corriger l'expiration des archives basée sur le temps lorsque aucune sauvegarde n'est expirée. (*Révisé par Stefan Fercot.*)

**Améliorations :**

- Améliorer les performances du pilote de stockage SFTP. (*Contribution de Stephen Frost, Reid Thompson. Révisé par David Steele.*)
- Ajouter un décalage horaire à la sortie de date/heure de la commande `info`. (*Révisé par Stefan Fercot, Philip Hurst. Suggéré par Philip Hurst.*)
- Centraliser le traitement des erreurs liées aux fonctionnalités non prises en charge. (*Révisé par Stefan Fercot.*)

**Améliorations de la documentation :**

- Préciser la préférence à installer à partir des paquets dans le guide utilisateur. (*Révisé par Stefan Fercot. Suggéré par dr-kd.*)


### Notes de version v2.46 {#v246-release-notes}

*Sauvegarde incrémentielle par bloc et stockage SFTP*

*Sortie le 22 mai 2023*

**Fonctionnalités :**

- Sauvegarde incrémentielle par bloc. (*Révisé par John Morris, Stephen Frost, Stefan Fercot.*)
- Prise en charge SFTP pour le stockage du dépôt. (*Contribution de Reid Thompson. Révisé par Stephen Frost, David Steele.*)
- Prise en charge de PostgreSQL 16. (*Révisé par Stefan Fercot.*)

**Améliorations :**

- Permettre de passer outre les vérifications d'en-tête de page. (*Révisé par David Christensen. Suggéré par David Christensen.*)
- Éviter `chown()` sur les fichiers de récupération lors d'une restauration. (*Révisé par Stefan Fercot, Marcelo Henrique Neppel. Suggéré par Marcelo Henrique Neppel.*)
- Ajouter des détails d'erreur pour les tentatives de réessai HTTP.

**Améliorations de la documentation :**

- Ajouter un avertissement concernant l'utilisation de la récupération `type=none`. (*Révisé par Stefan Fercot.*)
- Ajouter une note sur l'exécution de `stanza-create` sur des dépôts déjà créés.


### Notes de version v2.45 {#v245-release-notes}

*Sauvegarde incrémentielle par bloc (BÉTA)*

*Sortie le 20 mars 2023*

**Correctifs de bogues :**

- Ne pas écrire `recovery.signal` par défaut lors de la restauration de sauvegardes hors ligne. (*Révisé par Stefan Fercot. Signalement par Marcel Borger.*)

**Fonctionnalités :**

- Sauvegarde incrémentielle par bloc (BÉTA). (*Révisé par John Morris, Stephen Frost, Stefan Fercot.*)

**Améliorations :**

- Conservez un seul index de groupe avec les valeurs par défaut. (*Révisé par Stefan Fercot.*)

**Améliorations de la documentation :**

- Ajouter des instructions explicites pour la mise à jour entre les versions `2.x`. (*Contribution de Christophe Courtois. Révisé par David Steele.*)
- Supprimer les références à SSH rendues obsolètes avec l'introduction de TLS.


### Notes de version v2.44 {#v244-release-notes}

*Supprimer le support de PostgreSQL 9.0/9.1/9.2*

*Sortie le 30 janvier 2023*

**Améliorations :**

- Supprimer la prise en charge de PostgreSQL `9.0`/`9.1`/`9.2`. (*Révisé par Stefan Fercot.*)
- Erreur de restauration lorsque aucune sauvegarde ne correspond à la version actuelle de PostgreSQL. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Soulou.*)
- Ajouter le contrôle de plage pour chaque `compress-type` via `compress-level`. (*Révisé par Stefan Fercot. Suggéré par gkleen, ViperRu.*)

**Améliorations de la documentation :**

- Ajouter un avertissement concernant l'activation de « namespace hiérarchique » sur le stockage Azure. (*Révisé par Stefan Fercot. Suggéré par Vojtech Galda, Pluggi, asjonos.*)
- Ajouter un remplacement pour les sauts de ligne dans l'exemple de surveillance. (*Révisé par Stefan Fercot. Suggéré par rudonx, gmustdie, Ivan Shelestov.*)
- Préciser le comportement de `target-action` sur différentes versions de PostgreSQL. (*Contribution de Chris Bandy. Révisé par David Steele, Anton Kurochkin, Stefan Fercot. Suggéré par Anton Kurochkin, Chris Bandy.*)
- Mises à jour et clarifications apportées à la page d'accueil. (*Révisé par Stefan Fercot.*)
- Ajouter le mode sombre au site web. (*Suggéré par Stephen Frost.*)


### Notes de version v2.43 {#v243-release-notes}

*Correction de bogue*

*Sortie le 28 novembre 2022*

**Correctifs de bogues :**

- Corriger la référence manquante dans une sauvegarde différentielle/incrémentielle. (*Révisé par Stefan Fercot. Signalement par Marcel Borger, ulfedf, jaymefSO.*)

**Améliorations :**

- Ajouter un indicateur lorsque l'option est spécifiée sans index. (*Révisé par Stefan Fercot.*)


### Notes de version v2.42 {#v242-release-notes}

*Correctifs de bogues*

*Sortie le 22 novembre 2022*

**Correctifs de bogues :**

- Corriger une fuite mémoire dans le bundle de fichiers `backup`/`restore`. (*Révisé par John Morris, Oscar. Signalement par Oscar.*)
- Corriger une erreur de protocole lors d'une lecture partielle d'un fichier distant. (*Révisé par Stephen Frost.*)

**Améliorations :**

- Ne pas stocker de références pour les fichiers de longueur nulle lors du regroupement. (*Révisé par Stefan Fercot.*)
- Utiliser des descriptions plus générales pour `pg_start_backup()`/`pg_stop_backup()`. (*Révisé par Greg Sabino Mullane, David Christensen. Suggéré par Greg Sabino Mullane.*)

**Améliorations de la suite de tests :**

- Mettre à jour l'option `test.pl` `--psql-bin` pour qu'elle corresponde à l'aide en ligne de commande. (*Contribution de Koshi Shibagaki. Révisé par David Steele.*)


### Notes de version v2.41 {#v241-release-notes}

*Annotations de sauvegarde*

*Sortie le 19 septembre 2022*

**Correctifs de bogues :**

- Correction de l'expiration incorrecte du délai pour les dépôts non par défaut. (*Révisé par Stefan Fercot. Signalement par Adam Brusselback.*)
- Correction du problème survenant lors de l'affichage récursif des répertoires avec un filtre. (*Révisé par Stephen Frost. Signalement par Efremov Egor.*)

**Fonctionnalités :**

- Annotations clé/valeur pour la sauvegarde. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Adam Berlin.*)

**Améliorations :**

- Prise en charge `--set` dans la sortie JSON pour la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Anton Kurochkin.*)
- Permettre la configuration de la taille des morceaux à téléverser pour les magasins d'objets. (*Révisé par Stefan Fercot. Suggéré par Anton Glushakov.*)
- Mettre à jour les horodatages du fichier archive.info après une sauvegarde réussie. (*Révisé par Stefan Fercot. Suggéré par Alex Richman.*)
- Déplacer la vérification du timeline de la base de secours après le point de contrôle. (*Révisé par Stefan Fercot, Keith Fiske. Suggéré par Keith Fiske.*)
- Améliorer le message d'avertissement lors de la reprise d'une sauvegarde. (*Suggéré par Cynthia Shang.*)

**Améliorations de la documentation :**

- Ajouter le chemin absolu pour `kill` dans `pgbackrest.service`. (*Suggéré par Don Seiler.*)


### Notes de version v2.40 {#v240-release-notes}

*Prise en charge d’OpenSSL 3*

*Sortie le 18 juillet 2022*

**NOTE AUX PAQUETEURS** : Une version expérimentale de la construction avec meson a été ajoutée, mais les paqueteurs doivent continuer à utiliser la construction autoconf/make pour le moment.

**Améliorations :**

- Prise en charge d'OpenSSL 3. (*Révisé par Stephen Frost.*)
- Créer un instantané lors de l'affichage du contenu d'un chemin. (*Révisé par John Morris, Stephen Frost.*)
- Forcer `target-timeline=current` lors de la restauration `type=immediate`. (*Révisé par Stephen Frost.*)
- Tronquer les fichiers pendant une restauration delta (`restore`) lorsqu'ils sont plus grands que prévu. (*Révisé par Stephen Frost.*)
- Désactiver l'enregistrement du manifeste incrémentiel lorsque `resume=n`. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Définir le pourcentage de progression de la sauvegarde sur zéro avant le début de la copie. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Utiliser le drapeau S3 `IsTruncated` pour déterminer la continuation de la liste. (*Révisé par John Morris, Soulou. Suggéré par Christian Montagne.*)

**Correctifs de bogues dans la documentation :**

- Ignorer les options internes dans la référence de configuration. (*Signalement par Francisco Miguel Biete Banon.*)

**Améliorations de la documentation :**

- Ajouter un lien vers la configuration PostgreSQL dans la section hôte du dépôt. (*Révisé par Stefan Fercot. Suggéré par Julien Cigar.*)

**Améliorations de la suite de tests :**

- Ajouter la construction expérimentale avec Meson. (*Révisé par Eli Schwartz, Sam Bassaly.*)
- Permettre à tout chemin d'être passé à l'option `--test-path`. (*Contribution de Andrey Sokolov. Révisé par David Steele.*)
- Corriger l'erreur de compilation lorsque `DEBUG_EXEC_TIME` est défini sans `DEBUG`. (*Contribution de Andrey Sokolov. Révisé par David Steele.*)


### Notes de version v2.39 {#v239-release-notes}

*Vérification et regroupement de fichiers*

*Sortie le 16 mai 2022*

**Correctifs de bogues :**

- Corriger l'erreur levée par `FINALLY()` provoquant une boucle infinie. (*Révisé par Stephen Frost.*)
- Erreur sur toutes les échecs de verrouillage, sauf lorsque le verrou est détenu par un autre processus. (*Révisé par Reid Thompson, Geir Råness. Signalement par Geir Råness.*)

**Fonctionnalités :**

- Regroupement des fichiers de sauvegarde pour une meilleure prise en charge des petits fichiers. (*Révisé par Reid Thompson, Stefan Fercot, Chris Bandy.*)
- Commande verify pour valider le contenu d’un dépôt. (*Contribution de Cynthia Shang, Reid Thompson. Révisé par David Steele, Stefan Fercot.*)
- Prise en charge de PostgreSQL 15. (*Révisé par Stefan Fercot.*)
- Affichage du pourcentage d’avancement de la sauvegarde dans la sortie `info`. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Sélection automatique de la sauvegarde pour la commande `restore` `--type=lsn`. (*Contribution de Reid Thompson. Révisé par Stefan Fercot, David Steele.*)
- Suppression de l’avertissement relatif au WAL existant lorsque `archive-mode-check` est désactivé. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Ajout de la prise en charge d’AWS IMDSv2. (*Contribution de Nuno Pires. Révisé par David Steele.*)

**Améliorations :**

- Permettre la modification de l'option `repo-hardlink` après une sauvegarde complète. (*Révisé par Reid Thompson.*)
- Améliorer la précision de la journalisation du pourcentage d'avancement pour `backup` et `restore`. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Améliorer la validation des chemins pour les commandes `repo-*`. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Améliorer la commande `stop` afin qu'elle respecte l'option `stanza`. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par ragaoua.*)
- Améliorer le message d'erreur pour un `repo-azure-key` non valide. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Seth Daniel.*)
- Ajouter une indication pour vérifier le journal sur `archive-get`/`archive-push` en cas d'erreur asynchrone. (*Révisé par Reid Thompson.*)
- Ajouter `ClockError` en cas de décalage horaire ou de changement de fuseau horaire inattendu. (*Révisé par Greg Sabino Mullane, Stefan Fercot. Suggéré par Greg Sabino Mullane.*)
- Supprimer les extensions du manifeste de l'historique avant de l'afficher dans le message d'erreur. (*Révisé par Stefan Fercot.*)
- Ajouter l'utilisateur:groupe à l'erreur de permission de verrouillage. (*Révisé par Reid Thompson.*)

**Correctifs de bogues dans la documentation :**

- Correction d'une référence incorrecte à `stanza-update` dans le guide utilisateur. (*Corrigé par Abubakar Mohammed. Révisé par David Steele.*)
- Correction de l'exemple pour l'option `repo-gcs-key-type` dans la référence de configuration. (*Révisé par Reid Thompson.*)
- Correction de l'exemple pour `tls-server-auth` et ajout de précisions. (*Révisé par Reid Thompson.*)

**Améliorations de la documentation :**

- Simplifier les messages concernant les versions prises en charge dans la documentation. (*Révisé par Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)
- Ajouter des descriptions des types d'option. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Ajouter une FAQ sur les types de sauvegarde et la vitesse de restauration. (*Contribution de David Christensen. Révisé par Reid Thompson.*)
- Documenter la branche de base requise pour les demandes de fusion. (*Contribution de David Christensen. Révisé par Reid Thompson.*)


### Notes de version v2.38 {#v238-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 6 mars 2022*

**NOTE IMPORTANTE** : La taille du dépôt rapportée par la commande `info` est désormais entièrement basée sur ce que pgBackRest a écrit dans le stockage. Dans certains cas, pgBackRest pouvait auparavant détecter si une compression supplémentaire était appliquée par le stockage, mais cette fonctionnalité n’est plus prise en charge.

**Correctifs de bogues :**

- Réessayer les erreurs survenues lors de la suppression par lot de fichiers S3. (*Révisé par Reid Thompson. Signalement par Alex Richman.*)
- Permettre la correspondance insensible à la casse des valeurs d’en-tête HTTP `connection`. (*Révisé par Reid Thompson. Signalement par Rémi Vidier.*)

**Fonctionnalités :**

- Ajouter la prise en charge du chiffrement côté serveur AWS S3 utilisant KMS. (*Contribution de Christoph Berg. Révisé par David Steele, Tharindu Amila.*)
- Ajouter l'option `archive-missing-retry`. (*Révisé par Stefan Fercot.*)
- Ajouter un filtre de type de sauvegarde à la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

**Améliorations :**

- Réessayer en cas d'échec de validation de page pendant `backup`. (*Révisé par Stephen Frost, David Christensen.*)
- Gérer les serveurs TLS qui ne ferment pas les connexions de manière gracieuse. (*Révisé par Rémi Vidier, David Christensen, Stephen Frost.*)
- Ajouter les LSN de sauvegarde à la sortie de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Supprimer automatiquement les barres obliques en fin de chemins `repo-ls`. (*Contribution de David Christensen. Révisé par David Steele.*)
- Ne pas réessayer les erreurs fatales. (*Révisé par Reid Thompson.*)
- Supprimer le support de PostgreSQL `8.3`/`8.4`. (*Révisé par Reid Thompson, Stefan Fercot.*)
- Supprimer la logique qui tentait de déterminer une compression supplémentaire du système de fichiers. (*Révisé par Reid Thompson, Stefan Fercot.*)

**Correctifs de bogues dans la documentation :**

- Déplacer les options `repo` dans la documentation TLS vers la section `global`. (*Signalement par Anton Kurochkin.*)
- Supprimer l'option `backup-standby` inutilisée des commandes de stanza. (*Signalement par Stefan Fercot.*)
- Corriger les fautes de frappe dans l'aide et les notes de version. (*Corrigé par Daniel Gustafsson. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Ajouter une vérification de disponibilité à la configuration du service systemd. (*Suggéré par Yogesh Sharma.*)
- Ajouter une FAQ expliquant le suffixe de l'archive WAL. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Notez que les slots de réplication ne sont pas restaurés. (*Contribution de Reid Thompson. Révisé par David Steele, Stefan Fercot. Suggéré par Christophe Courtois.*)


### Notes de version v2.37 {#v237-release-notes}

*Serveur TLS*

*Sortie le 3 janvier 2022*

**NOTE IMPORTANTE** : Si la commande `restore` n'est pas en mesure de trouver une sauvegarde correspondant à une cible de temps spécifiée, une erreur sera levée, contrairement à auparavant où un avertissement était simplement journalisé.

**Correctifs de bogues :**

- Corriger le mappage des liens delta de `restore` lorsque le chemin ou le fichier existe déjà. (*Révisé par Reid Thompson. Signalement par Younes Alhroub.*)
- Corriger la fuite de socket lors des nouvelles tentatives de connexion. (*Révisé par Reid Thompson. Signalement par James Coleman.*)

**Fonctionnalités :**

- Ajouter un serveur TLS. (*Révisé par Stephen Frost, Reid Thompson, Andrew L'Ecuyer.*)
- Ajouter l'option `--cmd`. (*Contribution de Reid Thompson. Révisé par Stefan Fercot, David Steele. Suggéré par Virgile CREVON.*)

**Améliorations :**

- Vérifier l'archive immédiatement après le démarrage de la sauvegarde. (*Révisé par Reid Thompson, David Christensen.*)
- Ajouter des vérifications de timeline et de point de contrôle à la sauvegarde. (*Révisé par Stefan Fercot, Reid Thompson.*)
- Vérifier que les clusters sont actifs et correctement configurés pendant une sauvegarde. (*Révisé par Stefan Fercot.*)
- Erreur lorsque `restore` est incapable de trouver une sauvegarde correspondant à la cible de temps. (*Révisé par Reid Thompson, Douglas J Hunley. Suggéré par Douglas J Hunley.*)
- Analyser le protocole/port dans les points d'accès S3/Azure. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Ajouter un avertissement lorsque checkpoint_timeout dépasse `db-timeout`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Ajouter un verbe à la sortie d'erreur HTTP. (*Contribution de Christoph Berg. Révisé par David Steele.*)
- Permettre les arguments y/n pour les options de ligne de commande booléennes. (*Contribution de Reid Thompson. Révisé par David Steele.*)
- Faire correspondre exactement la taille de la sauvegarde au format de sortie de la commande `info`. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Mahomed Hussein.*)

**Améliorations de la documentation :**

- Afficher les valeurs par défaut et autorisées de l'option de taille, accompagnées des unités appropriées. (*Révisé par Reid Thompson.*)
- Corriger les fautes de frappe et améliorer la documentation de l'option `tablespace-map-all`. (*Révisé par Reid Thompson. Suggéré par Reid Thompson.*)
- Supprimer l'énoncé obsolète concernant la prise en charge future de plusieurs dépôts. (*Suggéré par David Christensen.*)


### Notes de version v2.36 {#v236-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 1er novembre 2021*

**Correctifs de bogues :**

- Autoriser « global » comme préfixe de stanza. (*Révisé par Stefan Fercot. Signalement par Younes Alhroub.*)
- Corriger le plantage (segfault) lors d'un fichier de clé GCS invalide. (*Révisé par Stephen Frost. Signalement par Henrik Feldt.*)

**Améliorations :**

- Autoriser l'option `link-map` pour créer de nouveaux liens. (*Révisé par Don Seiler, Stefan Fercot, Chris Bandy. Suggéré par Don Seiler.*)
- Augmenter le nombre maximal d'index autorisé pour les options `pg`/`repo` à 256. (*Révisé par Cynthia Shang.*)
- Ajouter l'authentification `WebIdentity` pour AWS S3. (*Révisé par James Callahan, Reid Thompson, Benjamin Blattberg, Andrew L'Ecuyer.*)
- Signaler les erreurs de validation des fichiers de sauvegarde dans `backup.info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Ajouter l'heure de démarrage de la récupération au journal de restauration en ligne d'une sauvegarde. (*Révisé par Tom Swartz, Stefan Fercot. Suggéré par Tom Swartz.*)
- Signaler l'erreur d'origine et les tentatives de réessai en cas d'échec d'une tâche locale. (*Révisé par Stefan Fercot.*)
- Renommer l'erreur de somme de contrôle de page en liste d'erreurs dans la sortie texte d'information. (*Révisé par Stefan Fercot.*)
- Ajouter des indications à l'avertissement de délai d'attente de relecture en mode secondaire. (*Révisé par Cynthia Shang, Stefan Fercot. Suggéré par Leigh Downs.*)


### Notes de version v2.35 {#v235-release-notes}

*Protocole binaire*

*Sortie le 23 août 2021*

**NOTE IMPORTANTE** : Le niveau de journalisation des fichiers copiés dans les commandes `backup`/`restore` a été modifié en `detail`. Cela rend le niveau de journalisation `info` moins bruyant, mais si ces messages sont nécessaires, définissez le niveau de journalisation des commandes `backup`/`restore` sur `detail`.

**Correctifs de bogues :**

- Détecter les erreurs lors de la finalisation du téléversement multipartite S3. (*Révisé par Cynthia Shang, Marco Montagna. Signalement par Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)
- Corriger la détection des liens symboliques circulaires. (*Révisé par Stefan Fercot. Signalement par Rohit Raveendran.*)
- Transmettre uniquement les options `repo` sélectionnées au serveur distant. (*Révisé par David Christensen, Cynthia Shang. Signalement par Greg Sabino Mullane, David Christensen.*)

**Améliorations :**

- Protocole binaire. (*Révisé par Cynthia Shang.*)
- Créer automatiquement le répertoire de données sur `restore`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Chris Bandy.*)
- Autoriser `restore` `--type=lsn`. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang. Suggéré par James Coleman.*)
- Modifier le niveau de journalisation des fichiers copiés `backup`/`restore` en détail. (*Révisé par Stefan Fercot. Suggéré par Jens Wilke.*)
- Boucler en attendant que le LSN de point de contrôle atteigne le LSN de relecture. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Fatih Mencutekin.*)
- Journaliser le total des fichiers `backup` et le total de la taille par fichier `restore`. (*Révisé par Cynthia Shang.*)

**Correctifs de bogues dans la documentation :**

- Correction de noms d'hôtes incorrects dans le guide utilisateur. (*Révisé par Stefan Fercot. Signalement par Greg Sabino Mullane.*)

**Améliorations de la documentation :**

- Mettre à jour la documentation relative à la contribution et ajouter un modèle de demande de fusion. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Réorganiser la documentation relative aux sauvegardes dans le guide utilisateur. (*Révisé par Cynthia Shang.*)
- Préciser le comportement de `restore` `--type` dans la référence de commande. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Corriger les fautes de frappe dans la documentation et les commentaires. (*Contribution de Eric Radman. Révisé par David Steele.*)

**Améliorations de la suite de tests :**

- Ajouter une vérification du chemin de test à l'intérieur du chemin de répertoire. (*Révisé par Greg Sabino Mullane. Suggéré par Greg Sabino Mullane.*)
- Ajouter une analyse statique du code avec CodeQL. (*Révisé par Cynthia Shang.*)
- Mettre à jour les tests pour utiliser des modèles standards. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.34 {#v234-release-notes}

*Prise en charge de PostgreSQL 14*

*Sortie le 7 juin 2021*

**Correctifs de bogues :**

- Corriger les problèmes liés aux fichiers de file d'attente résiduels d'une précédente `restore`. (*Révisé par Cynthia Shang, Stefan Fercot, Floris van Nee. Signalement par Floris van Nee.*)
- Corriger le problème survenant lors de la vérification des liens pour un grand nombre d'espaces de tables. (*Révisé par Cynthia Shang, Avinash Vallarapu. Signalement par Avinash Vallarapu.*)
- Libérer les distants inutiles afin qu'ils n'expirent pas durant `restore`. (*Révisé par Cynthia Shang. Signalement par Francisco Miguel Biete Banon.*)
- Corriger `help` lorsqu'une option valide est invalide pour la commande spécifiée. (*Révisé par Stefan Fercot. Signalement par Cynthia Shang.*)

**Fonctionnalités :**

- Ajouter la prise en charge de PostgreSQL 14. (*Révisé par Cynthia Shang.*)
- Ajouter l'authentification automatique GCS pour les instances GCE. (*Révisé par Jan Wieck, Daniel Farina.*)
- Ajouter l'option `repo-retention-history` pour expirer l'historique des sauvegardes. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang, David Steele.*)
- Ajouter l'option `db-exclude`. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang.*)

**Améliorations :**

- Modifier le niveau de journalisation de l'expiration de l'archive de détail à information. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Supprimer le chemin de stockage temporaire de l'archive de la stanza sur `restore`. (*Révisé par Cynthia Shang, Stefan Fercot.*)
- Ne pas écrire les fichiers de manière atomique ni synchroniser les chemins pendant la copie `backup`. (*Révisé par Stephen Frost, Stefan Fercot, Cynthia Shang.*)

**Améliorations de la documentation :**

- Mettre à jour la documentation relative aux contributions. (*Contribution de Cynthia Shang. Révisé par David Steele, Stefan Fercot.*)
- Consolider le guide utilisateur RHEL/CentOS en un seul document. (*Révisé par Cynthia Shang.*)
- Préciser que `repo-s3-role` n'est pas un `ARN`. (*Contribution de Isaac Yuen. Révisé par David Steele.*)


### Notes de version v2.33 {#v233-release-notes}

*Prise en charge des dépôts multiples et de GCS*

*Sortie le 5 avril 2021*

**Correctifs de bogues :**

- Corriger les avertissements d'option bloquant la synchronisation asynchrone `archive-get`/`archive-push`. (*Révisé par Cynthia Shang. Signalement par Lev Kokotov.*)
- Corriger la fuite mémoire lors de la sauvegarde pendant la copie de l'archive. (*Révisé par Cynthia Shang. Signalement par Christian ROUX, Efremov Egor.*)
- Corriger le dépassement de pile lors de la génération de la phrase de passe du chiffrement. (*Révisé par Cynthia Shang. Signalement par bsiara.*)
- Corriger `repo-ls` `/` sur les dépôts S3. (*Révisé par Cynthia Shang. Signalement par Lesovsky Alexey.*)

**Fonctionnalités :**

- Prise en charge de plusieurs dépôts. (*Contribution de Cynthia Shang, David Steele. Révisé par Stefan Fercot, Stephen Frost.*)
- Prise en charge de GCS pour le stockage du dépôt. (*Révisé par Cynthia Shang, Daniel Farina.*)
- Ajout de l'option `archive-header-check`. (*Révisé par Stephen Frost, Cynthia Shang. Suggéré par Hans-Jürgen Schönig.*)

**Améliorations :**

- Inclure les bases de données système recréées lors d'une restauration sélective. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang.*)
- Exclure `content-length` des en-têtes signés S3. (*Révisé par Cynthia Shang. Suggéré par Brian P Bockelman.*)
- Consolider les options de stockage du dépôt moins couramment utilisées. (*Révisé par Cynthia Shang.*)
- Permettre un `config-path` par défaut personnalisé avec `./configure --with-configdir`. (*Contribution de Michael Schout. Révisé par David Steele.*)
- Journaliser la copie de l'archive pendant `backup`. (*Révisé par Cynthia Shang, Stefan Fercot.*)

**Améliorations de la documentation :**

- Mettre à jour la référence pour inclure des liens vers des exemples du guide utilisateur. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Mettre à jour la documentation de la restauration sélective avec des avertissements. (*Révisé par Cynthia Shang, Stefan Fercot.*)
- Ajouter une clarification sur `compress-type` dans la documentation de `archive-copy`. (*Révisé par Cynthia Shang, Stefan Fercot.*)
- Ajouter les valeurs par défaut de `compress-level` en fonction de la valeur de `compress-type`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajouter une note indiquant que les paramètres NFS requis doivent être identiques à ceux de PostgreSQL. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.32 {#v232-release-notes}

*Commandes du dépôt*

*Sortie le 8 février 2021*

**Correctifs de bogues :**

- Corriger la reprise après suppression partielle d'une sauvegarde par une reprise antérieure. (*Révisé par Cynthia Shang. Signalement par Tom Swartz.*)

**Fonctionnalités :**

- Ajouter la commande `repo-ls`. (*Révisé par Cynthia Shang, Stefan Fercot.*)
- Ajouter la commande `repo-get`. (*Contribution de Stefan Fercot, David Steele. Révisé par Cynthia Shang.*)
- Ajouter l'option `archive-mode-check`. (*Contribution de Stefan Fercot. Révisé par David Steele, Michael Banck.*)

**Améliorations :**

- Améliorer les performances de `archive-get`. (*Révisé par Cynthia Shang.*)

**Améliorations de la documentation :**

- Améliorer la documentation de la commande `expire`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.31 {#v231-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 7 décembre 2020*

**Correctifs de bogues :**

- Autoriser `[`, `#` et `space` comme premier caractère dans les noms de base de données. (*Révisé par Stefan Fercot, Cynthia Shang. Signalement par Jefferson Alexandre.*)
- Créer `standby.signal` uniquement sur PostgreSQL 12 lorsque le type `restore` est `standby`. (*Corrigé par Stefan Fercot. Révisé par David Steele. Signalement par Keith Fiske.*)

**Fonctionnalités :**

- Expire les fichiers d'historique. (*Contribution de Stefan Fercot. Révisé par David Steele.*)
- Signale les erreurs de somme de contrôle de page dans la sortie de la commande `info` `text`. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang.*)
- Ajoute l'option `repo-azure-endpoint`. (*Révisé par Cynthia Shang, Brian Peterson. Suggéré par Brian Peterson.*)
- Ajoute l'option `pg-database`. (*Révisé par Cynthia Shang.*)

**Améliorations :**

- Améliorer la sortie de la commande `info` lorsqu'une stanza est spécifiée mais manquante. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang, David Steele. Suggéré par uspen.*)
- Améliorer les performances des listes de fichiers volumineuses dans les commandes `backup`/`restore`. (*Révisé par Cynthia Shang, Oscar.*)
- Ajouter des tentatives de nouvelle tentative lors de la mise en sommeil de PostgreSQL au démarrage d'une sauvegarde. (*Révisé par Cynthia Shang. Suggéré par Vitaliy Kukharik.*)

**Améliorations de la documentation :**

- Remplacer la documentation RHEL/CentOS 6 par celle de RHEL/CentOS 8.


### Notes de version v2.30 {#v230-release-notes}

*Prise en charge de PostgreSQL 13*

*Sortie le 5 octobre 2020*

**Correctifs de bogues :**

- Erreur avec indications lorsque l'utilisateur de sauvegarde ne peut pas lire `pg_settings`. (*Révisé par Stefan Fercot, Cynthia Shang. Signalement par Mohamed Insaf K.*)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 13. (*Révisé par Cynthia Shang.*)

**Améliorations :**

- Améliorer l'identification de la version de PostgreSQL. (*Révisé par Cynthia Shang, Stephen Frost.*)
- Améliorer le message d'erreur relatif au répertoire de travail. (*Révisé par Stefan Fercot.*)
- Ajouter une indication sur le démarrage de la stanza lorsque le segment WAL n'est pas trouvé. (*Contribution de David Christensen. Révisé par David Steele.*)
- Ajouter une indication concernant un désaccord de version de protocole. (*Révisé par Cynthia Shang. Suggéré par loop-evgeny.*)

**Améliorations de la documentation :**

- Ajouter une note indiquant que les versions de pgBackRest doivent être identiques lorsqu'elles sont exécutées à distance. (*Révisé par Cynthia Shang. Suggéré par loop-evgeny.*)
- Déplacer le texte de la commande info vers la référence et établir un lien vers le guide utilisateur. (*Révisé par Cynthia Shang. Suggéré par Christophe Courtois.*)
- Mettre à jour le chemin du dépôt yum pour le guide utilisateur CentOS/RHEL. (*Contribution de Heath Lord. Révisé par David Steele.*)


### Notes de version v2.29 {#v229-release-notes}

*Crédentiels S3 automatiques sur AWS*

*Sortie le 31 août 2020*

**Correctifs de bogues :**

- Supprime les erreurs lors de la fermeture des processus `local`/`remote`. Étant donné que la commande est terminée, il est contre-productif de lever une erreur, mais **avertit** tout de même pour indiquer qu’un événement inhabituel s’est produit. (*Révisé par Cynthia Shang. Signalement par argdenis.*)
- Corrige le problème lié au caractère `=` dans les noms de fichier ou de base de données. (*Révisé par Bastian Wegge, Cynthia Shang. Signalement par Brad Nicholson, Bastian Wegge.*)

**Fonctionnalités :**

- Récupérer automatiquement les identifiants temporaires S3 sur les instances AWS. (*Contribution de David Steele, Stephen Frost. Révisé par Cynthia Shang, David Youatt, Aleš Zelený, Jeanette Bromage.*)
- Ajouter l'option `archive-mode` pour désactiver l'archivage lors d'une restauration. (*Révisé par Stephen Frost. Suggéré par Stephen Frost.*)

**Améliorations :**

- Prise en charge de PostgreSQL 13 beta3. Les modifications apportées aux versions de contrôle/catalogue/WAL dans les versions beta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.
- Prise en charge de l’asynchrone `list`/`remove` pour le stockage S3/Azure. (*Révisé par Cynthia Shang, Stephen Frost.*)
- Amélioration de l'utilisation mémoire lors de la détection des relations non enregistrées lors de la construction du manifeste. (*Révisé par Cynthia Shang, Stephen Frost, Brad Nicholson, Oscar. Suggéré par Oscar, Brad Nicholson.*)
- Fermeture proactive des descripteurs de fichiers après le fork du processus asynchrone. (*Révisé par Stephen Frost, Cynthia Shang.*)
- Report de la fermeture de la connexion distante de la sauvegarde jusqu’après le contrôle de l’archive. (*Contribution de Floris van Nee. Révisé par David Steele.*)
- Amélioration de la sortie détaillée des erreurs. (*Révisé par Cynthia Shang.*)
- Amélioration du rapport des erreurs TLS. (*Révisé par Cynthia Shang, Stephen Frost.*)

**Correctifs de bogues dans la documentation :**

- Ajouter `none` à la référence de l'option `compress-type` et corriger l'exemple. (*Signalement par Ugo Bellavance, Don Seiler.*)
- Ajouter le type manquant `azure` dans la référence de l'option `repo-type`. (*Corrigé par Don Seiler. Révisé par David Steele.*)
- Corriger l'orthographe dans la référence de l'option `repo-cipher-type`. (*Corrigé par Don Seiler. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Précisez que `expire` doit être exécuté régulièrement lorsque `expire-auto` est désactivé. (*Révisé par Douglas J Hunley. Suggéré par Douglas J Hunley.*)


### Notes de version v2.28 {#v228-release-notes}

*Stockage de dépôt Azure*

*Sortie le 20 juillet 2020*

**Correctifs de bogues :**

- Correction `restore` `--force` agissant comme `--force --delta`. Cela a fait que `restore` remplaçait les fichiers en fonction de leur horodatage et de leur taille plutôt que de les écraser, ce qui a laissé certains fichiers qui auraient dû être mis à jour inchangés. Les `restore` et `restore` `--delta` normaux n'ont pas été affectés par ce problème. (*Révisé par Cynthia Shang.*)

**Fonctionnalités :**

- Prise en charge d'Azure pour le stockage du dépôt. (*Révisé par Cynthia Shang, Don Seiler.*)

- Ajouter l'option `expire-auto`. Cela permet de désactiver l'expiration automatique après une sauvegarde réussie. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang, David Steele.*)

**Améliorations :**

- Téléversement asynchrone multipart S3. (*Révisé par Stephen Frost.*)
- Réessai automatique pour `backup`, `restore`, `archive-get` et `archive-push`. (*Révisé par Cynthia Shang.*)
- Désactiver la parallélisation des requêtes dans les sessions PostgreSQL utilisées pour le contrôle de la sauvegarde. (*Révisé par Stefan Fercot.*)
- Prise en charge de PostgreSQL 13 beta2. Les modifications apportées aux versions du contrôle/catalogue/WAL dans les versions bêta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.
- Amélioration de la gestion des codes de réponse HTTP non valides. (*Révisé par Cynthia Shang.*)
- Amélioration du message d'erreur lorsque l'option `pg1-path` est manquante pour la commande `archive-get`. (*Révisé par Cynthia Shang.*)
- Ajout d'un indicateur lorsque la somme de contrôle delta est activée après un basculement de timeline. (*Révisé par Matt Bunter, Cynthia Shang.*)
- Utiliser PostgreSQL au lieu de `postmaster` lorsque cela est approprié. (*Révisé par Cynthia Shang.*)

**Correctifs de bogues dans la documentation :**

- Correction de l'exemple incorrect pour l'option `repo-retention-full-type`. (*Signalement par Höseyin Sönmez.*)
- Suppression des commandes internes des références HTML et man. (*Signalement par Cynthia Shang.*)

**Améliorations de la documentation :**

- Mettre à jour les versions de PostgreSQL utilisées pour la construction des guides utilisateur. Ajouter également des plages de versions pour indiquer qu’un guide utilisateur est pertinent pour une plage de versions de PostgreSQL, même s’il a été construit pour une version spécifique. (*Révisé par Stephen Frost.*)
- Mettre à jour la FAQ concernant l’expiration d’un jeu de sauvegarde spécifique. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Mettre à jour la FAQ pour clarifier le comportement par défaut de la récupération à un point précis dans le temps (PITR). (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.27 {#v227-release-notes}

*Améliorations de l’expiration et pilotes de compression*

*Sortie le 26 mai 2020*

**Correctifs de bogues :**

- Corriger le problème de vérification du fait que des liens de fichier soient contenus dans des liens de chemin. (*Révisé par Cynthia Shang. Signalement par Christophe Cavallié.*)
- Permettre que `pg-path1` soit facultatif pour la synchronisation `archive-push`. (*Révisé par Cynthia Shang. Signalement par Jerome Peng.*)
- La commande `expire` vérifie désormais la présence d'un fichier d'arrêt. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Gérer le cas où la phrase de raison est absente dans la réponse HTTP. (*Révisé par Cynthia Shang. Signalement par Tenuun.*)
- Augmenter la taille du tampon pour le vidage de la compression lz4. (*Révisé par Cynthia Shang. Signalement par Eric Radman.*)
- Ignorer les options `pg-host*` et `repo-host*` pour la commande `remote`. (*Révisé par Cynthia Shang. Signalement par Pavel Suderevsky.*)
- Corriger la possibilité de manque d'options `pg1-*` pour la commande `remote`. (*Révisé par Cynthia Shang. Signalement par Andrew L'Ecuyer.*)

**Fonctionnalités :**

- Rétention basée sur la durée pour les sauvegardes complètes. L'option `--repo-retention-full-type` permet de conserver les sauvegardes complètes selon une période définie, exprimée en jours. (*Contribution de Cynthia Shang, Pierre Ducroquet. Révisé par David Steele.*)
- Expiration de sauvegarde à la demande. Permet à l'utilisateur de supprimer une sauvegarde spécifique, indépendamment des paramètres de rétention. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Prise en charge de la compression Zstandard. Notez que la configuration de `compress-type=zst` rendra les nouvelles sauvegardes et archives incompatibles (non restaurables) avec les versions antérieures de pgBackRest. (*Révisé par Cynthia Shang.*)
- Prise en charge de la compression bzip2. Notez que la configuration de `compress-type=bz2` rendra les nouvelles sauvegardes et archives incompatibles (non restaurables) avec les versions antérieures de pgBackRest. (*Contribution de Stephen Frost. Révisé par David Steele, Cynthia Shang.*)
- Ajout de l'état d'exécution `backup`/`expire` à la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

**Améliorations :**

- Expire les archives WAL uniquement lorsque le seuil `repo-retention-archive` est atteint. Les archives WAL antérieures à la première sauvegarde complète étaient auparavant expirées après la première sauvegarde complète. Elles sont désormais conservées selon les paramètres de rétention. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajouter une implémentation locale MD5 afin que S3 fonctionne lorsque FIPS est activé. (*Révisé par Cynthia Shang, Stephen Frost. Suggéré par Brian Almeida, John Kelly.*)
- Prise en charge de PostgreSQL 13 beta1. Les modifications apportées aux versions de contrôle/catalogue/WAL dans les versions bêta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution. (*Révisé par Cynthia Shang.*)
- Réduire la valeur par défaut de `buffer-size` à `1MiB`. (*Révisé par Stephen Frost.*)
- Générer une erreur lisible par l'utilisateur si `expire` n'est pas exécuté sur l'hôte du dépôt. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.26 {#v226-release-notes}

*TLS non bloquant*

*Sortie le 20 avril 2020*

**Correctifs de bogues :**

- Supprimez l'expression imbriquée vide de l'expression régulière du manifeste. MacOS n'était pas satisfait de cette modification, bien que les autres plates-formes semblent fonctionner correctement. (*Corrigé par David Raftis. Révisé par David Steele.*)

**Améliorations :**

- Implémentation TLS non bloquante. (*Révisé par Slava Moudry, Cynthia Shang, Stephen Frost.*)
- Limite uniquement la taille de copie des fichiers journalisés WAL. Le comportement précédent pouvait entraîner une troncature de `postgresql.conf` ou de `postgresql.auto.conf` dans la sauvegarde. (*Révisé par Cynthia Shang.*)
- Les options de keep-alive TCP sont configurables. (*Suggéré par Marc Cousin.*)
- Ajoute l'option `io-timeout`. (*Révisé par Cynthia Shang.*)


### Notes de version v2.25 {#v225-release-notes}

*LZ4 Prise en charge de la compression*

*Sortie le 26 mars 2020*

**Fonctionnalités :**

- Ajouter la prise en charge de la compression lz4. Notez que la configuration de `compress-type=lz4` rendra les nouvelles sauvegardes et archives incompatibles (non restaurables) avec les versions antérieures de pgBackRest. (*Révisé par Cynthia Shang.*)
- Ajouter l'option `--dry-run` à la commande `expire`. Utilisez l'option dry-run pour visualiser les sauvegardes/archives qui seraient supprimées par la commande `expire` sans effectuer de suppression réelle. (*Contribution de Cynthia Shang, Luca Ferrari. Révisé par David Steele. Suggéré par Marc Cousin.*)

**Améliorations :**

- Améliorer les performances de la construction du manifeste distant. (*Suggéré par Jens Wilke.*)
- Corriger la détection des options keepalive sous Linux. (*Contribution de Marc Cousin. Révisé par David Steele.*)
- Ajouter la détection de l'hôte dans configure pour définir correctement les drapeaux standards. (*Contribution de Marc Cousin. Révisé par David Steele.*)
- Supprimer les options `compress`/`compress-level` des commandes où elles ne sont pas utilisées. Ces commandes (par exemple `restore`, `archive-get`) n'ont jamais utilisé les options de compression mais autorisaient leur passage en ligne de commande. Elles généreront désormais une erreur si ces options sont passées en ligne de commande. Si de telles erreurs se produisent, supprimez les options inutilisées. (*Révisé par Cynthia Shang.*)
- Limite la taille de copie des fichiers de sauvegarde à la taille indiquée au démarrage de la sauvegarde. Si un fichier augmente de taille pendant la sauvegarde, il sera reconstruit par lecture des WAL lors de la restauration, il n'est donc pas nécessaire de copier les données supplémentaires. (*Révisé par Cynthia Shang.*)


### Notes de version v2.24 {#v224-release-notes}

*Sélection automatique de l'ensemble de sauvegarde pour la cible de temps*

*Sortie le 25 février 2020*

**Correctifs de bogues :**

- Empêcher la création de processus orphelins dans les commandes d'archive asynchrones. (*Révisé par Stephen Frost. Signalement par Adam Brusselback, ejberdecia.*)
- Erreur lorsque `archive-get`/`archive-push`/`restore` ne sont pas exécutés sur un hôte PostgreSQL. (*Révisé par Stephen Frost. Signalement par Jesper St John.*)
- Lire le contenu HTTP jusqu'à la fin lorsque la taille ou le codage n'est pas spécifié. (*Révisé par Cynthia Shang. Signalement par Christian ROUX.*)
- Corriger la reprise lorsque la sauvegarde reprise a été créée par Perl. Dans ce cas, la sauvegarde reprise doit être ignorée, mais le code C n'était pas en mesure de charger le manifeste partiel écrit par Perl car le format diffère légèrement. Ajouter des validations pour détecter ce cas et continuer de manière correcte. (*Signalement par Kacey Holston.*)

**Fonctionnalités :**

- Sélection automatique de l'ensemble de sauvegarde lors d'une restauration lorsqu'une cible de temps est spécifiée. La sélection automatique n'est effectuée que lorsque `--set` n'est pas précisé. Si aucun ensemble de sauvegarde correspondant à l'instant cible n'est trouvé, l'ensemble de sauvegarde le plus récent (par défaut) sera utilisé. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations :**

- Ignorer le fichier temporaire `pg_internal.init` pendant la sauvegarde. (*Révisé par Cynthia Shang. Suggéré par Michael Paquier.*)
- Ajouter davantage de validations du manifeste lors de `backup`. (*Révisé par Cynthia Shang.*)

**Améliorations de la documentation :**

- Empêcher le bot de verrouillage d'ajouter des commentaires aux problèmes verrouillés. (*Suggéré par Christoph Berg.*)


### Notes de version v2.23 {#v223-release-notes}

*Correction de bogue*

*Sortie le 27 janvier 2020*

**Correctifs de bogues :**

- Corrige les fichiers manquants qui corrompent le manifeste. Si un fichier a été supprimé par PostgreSQL pendant la sauvegarde (ou s'il manquait sur le serveur de repli), le fichier suivant pourrait ne pas être copié ni mis à jour dans le manifeste. Si cela s'est produit, la sauvegarde générerait une erreur lors de sa restauration. (*Révisé par Cynthia Shang. Signalement par Vitaliy Kukharik.*)

**Améliorations :**

- Utilisez `pkg-config` à la place de `xml2-config` pour les options de compilation de libxml2. (*Contribution de David Steele, Adrian Vondendriesch.*)
- Les sommes de contrôle de validation sont définies dans le manifeste sur `backup`/`restore`. (*Révisé par Cynthia Shang.*)


### Notes de version v2.22 {#v222-release-notes}

*Correction de bogue*

*Sortie le 21 janvier 2020*

**Correctifs de bogues :**

- Corriger une erreur de conversion de timeline. La timeline est nécessaire pour vérifier les segments WAL dans l'archive après une sauvegarde. La conversion a été effectuée en base `10` au lieu de `16`, ce qui a entraîné des erreurs lorsque la timeline était ≥ `0xA`. (*Signalement par Lukas Ertl, Eric Veldhuyzen.*)


### Notes de version v2.21 {#v221-release-notes}

*C Migration terminée*

*Sortie le 15 janvier 2020*

**Correctifs de bogues :**

- Corriger l'ignorance des options par les commandes asynchrones. Les processus asynchrones `archive-get`/`archive-push` ne chargeaient pas les options configurées dans les sections de configuration de commande, par exemple `[global:archive-get]`. (*Révisé par Cynthia Shang. Signalement par Urs Kramer.*)
- Corriger la gestion de `\` dans les noms de fichiers. `\` n'était pas correctement échappé lors du calcul de la somme de contrôle du manifeste, ce qui empêchait le chargement du manifeste. Étant donné que les occurrences de `\` dans les noms de fichiers de cluster devraient être rares voire inexistantes, cela ne semble pas constituer un problème sérieux en production.

**Fonctionnalités :**

- pgBackRest est désormais entièrement écrit en C.
- Ajouter l'option `pg-user`. Spécifie le nom d'utilisateur de la base de données lors de la connexion à PostgreSQL. Si non spécifié, pgBackRest se connecte avec l'utilisateur système local ou `PGUSER`, ce qui était le comportement précédent. (*Contribution de Mike Palmiotto. Révisé par David Steele.*)
- Permettre les URI au format chemin dans le pilote S3.

**Améliorations :**

- La commande `backup` est entièrement implémentée en C. (*Révisé par Cynthia Shang.*)


### Notes de version v2.20 {#v220-release-notes}

*Correctifs de bogues*

*Sortie le 12 décembre 2019*

**Correctifs de bogues :**

- Corriger archive-push/archive-get lorsque `PGDATA` est un lien symbolique. Ces commandes tentaient d'utiliser `cwd()` comme `PGDATA` mais cela aurait été en désaccord avec le chemin configuré dans pgBackRest si `PGDATA` était un lien symbolique. Si `cwd()` ne correspond pas au chemin pgBackRest, effectuez un appel à `chdir()` vers le chemin et assurez-vous que le prochain `cwd()` correspond au résultat de l'appel initial. (*Signalement par Stephen Frost, Milosz Suchy.*)

- Corriger la liste de références lors de la reconstruction de `backup.info` dans la commande `expire`. Étant donné que la commande `backup` utilise encore la version Perl de la reconstruction, ce problème ne se manifestera que si **1)** une sauvegarde est manquante dans `backup.info` et **2)** la commande `expire` est exécutée directement au lieu d’être exécutée après `backup` comme d’habitude. Cette combinaison peu probable d’événements signifie que ce problème est probablement sans incidence en production.

- Corriger le plantage (segfault) en cas de fin inattendue (EOF) lors de la décompression gzip. (*Signalement par Stephen Frost.*)


### Notes de version v2.19 {#v219-release-notes}

*C Migrations et corrections de bogues*

*Sortie le 12 novembre 2019*

**Correctifs de bogues :**

- Corriger le délai d'attente distant lors d'une restauration delta. Lorsqu'une restauration delta est effectuée sur un cluster largement inchangé, le serveur distant peut expirer si aucun fichier n'est récupéré depuis le dépôt dans un délai de `protocol-timeout`. Ajouter des messages de maintien de connexion pour éviter l'expiration du serveur distant. (*Signalement par James Sewell, Jens Wilke.*)
- Corriger la gestion des en-têtes HTTP répétés. Lorsque des en-têtes HTTP sont répétés, ils doivent être traités comme équivalents à un seul en-tête séparé par des virgules, plutôt que de générer une erreur, ce qui était le comportement précédent. (*Signalement par donicrosby.*)

**Améliorations :**

- La sortie JSON de la commande `info` n'est plus formatée de manière lisible. Les systèmes de surveillance peuvent ainsi plus facilement traiter le JSON sans sauts de ligne. Des outils externes tels que `jq` peuvent être utilisés pour formater la sortie si nécessaire. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- La commande `check` est entièrement implémentée en C. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Documentez comment contribuer à pgBackRest. (*Contribution de Cynthia Shang, David Steele.*)
- Documentez la version maximale prise en charge par l'option `auto-stop`. (*Contribution de Brad Nicholson. Révisé par David Steele.*)

**Améliorations de la suite de tests :**

- Corriger le chemin du conteneur utilisé lors de `--vm=none`. (*Suggéré par Stephen Frost.*)
- Corriger le décalage d’heure dans le test expect. (*Suggéré par Stephen Frost.*)
- Ne plus générer automatiquement le code libc intégré par défaut. (*Suggéré par Stephen Frost.*)


### Notes de version v2.18 {#v218-release-notes}

*Prise en charge de PostgreSQL 12*

*Sortie le 1er octobre 2019*

**Fonctionnalités :**

- Prise en charge de PostgreSQL 12.
- Ajouter l'option `set` de la commande `info` pour produire une sortie texte détaillée. Les informations supplémentaires comprennent les bases de données utilisables pour une restauration sélective, ainsi qu'une liste des tablespaces et des liens symboliques avec leurs destinations par défaut. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Stephen Frost et ejberdecia.*)
- Ajouter le type de restauration `standby`. Il ajoute automatiquement standby_mode=on à recovery.conf pour PostgreSQL < 12 et crée `standby.signal` pour PostgreSQL ≥ 12, fournissant ainsi une interface commune aux versions de PostgreSQL. (*Révisé par Cynthia Shang.*)

**Améliorations :**

- La commande `restore` est entièrement implémentée en C. (*Révisé par Cynthia Shang.*)

**Améliorations de la documentation :**

- Documentez la relation entre `db-timeout` et `protocol-timeout`. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par James Chanco Jr.*)
- Ajoutez des précisions documentaires concernant les dépôts de bascule. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajoutez une FAQ sur la restauration à un instant donné basée sur le temps. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v2.17 {#v217-release-notes}

*C Migrations et corrections de bogues*

*Sortie le 3 septembre 2019*

**Correctifs de bogues :**

- Améliorer la construction du manifeste lent pour un très grand nombre de tables/segments. (*Signalement par Jens Wilke.*)
- Corriger les exclusions pour les fichiers spéciaux. (*Signalement par CluelessTechnologist, Janis Puris, Rachid Broum.*)

**Améliorations :**

- Les commandes `stanza-create/update/delete` sont entièrement implémentées en C. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Les commandes `start`/`stop` sont entièrement implémentées en C. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Créez les répertoires/fichiers de journalisation avec le mode `0750`/`0640`. (*Suggéré par Damiano Albani.*)

**Correctifs de bogues dans la documentation :**

- Correction du paquet `yum.p.o` lors de l'installation d'un paquet personnalisé. (*Signalement par Joe Ayers, John Harvey.*)

**Améliorations de la documentation :**

- Compiler pgBackRest en tant qu'utilisateur non privilégié. (*Suggéré par Laurenz Albe.*)


### Notes de version v2.16 {#v216-release-notes}

*C Migrations et corrections de bogues*

*Sortie le 5 août 2019*

**Correctifs de bogues :**

- Réessayer les erreurs S3 `RequestTimeTooSkewed` au lieu de terminer immédiatement. (*Signalement par sean0101n, Tim Garton, Jesper St John et Aleš Zelený.*)
- Corriger le traitement incorrect de la réponse `transfer-encoding` à une requête `HEAD`. (*Signalement par Pavel Suderevsky.*)
- Corriger les violations de portée révélées par les optimisations de gcc 9. (*Signalement par Christian Lange et Ned T. Crigler.*)

**Fonctionnalités :**

- Ajouter l'option `repo-s3-port` pour définir un port de service S3 non standard.

**Améliorations :**

- La commande `local` pour `backup` est entièrement implémentée en C. (*Contribution de David Steele, Cynthia Shang.*)
- La commande `check` est implémentée en partie en C. (*Révisé par Cynthia Shang.*)


### Notes de version v2.15 {#v215-release-notes}

*Implémentation C de Expire*

*Sortie le 25 juin 2019*

**Correctifs de bogues :**

- Corriger la rétention des archives qui expirait de manière trop agressive. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Mohamad El-Rifai.*)

**Améliorations :**

- La commande `expire` est entièrement implémentée en C. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- La commande `local` pour la restauration est entièrement implémentée en C.
- Supprimer l'utilisateur PostgreSQL codé en dur afin que `$PGUSER` fonctionne. (*Suggéré par Julian Zhang, Janis Puris.*)
- Respecter l'option de configuration `--prefix`. (*Suggéré par Daniel Westermann.*)
- Renommer l'option `repo-s3-verify-ssl` en `repo-s3-verify-tls`. Le nouveau nom est préféré car pgBackRest ne prend en charge aucune version de protocole SSL (toutes sont considérées comme non sécurisées). Le nom ancien continuera d'être accepté.

**Améliorations de la documentation :**

- Ajouter une FAQ à la documentation. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Utiliser `wal_level=replica` dans la documentation pour PostgreSQL ≥ 9.6. (*Suggéré par Patrick McLaughlin.*)


### Notes de version v2.14 {#v214-release-notes}

*Correction de bogues et améliorations*

*Sortie le 20 mai 2019*

**Correctifs de bogues :**

- Correction d'un plantage (segfault) lorsque `process-max` > 8 pour `archive-push`/`archive-get`. (*Signalement par Jens Wilke.*)

**Améliorations :**

- Ignorer les vérifications de base de données lorsque `stanza-delete` est utilisé avec `force`. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par hatifnatt.*)
- Ajouter le script `configure` pour une meilleure prise en charge multiplateforme.

**Fonctionnalités de la documentation :**

- Ajouter les guides utilisateur pour CentOS/RHEL 6/7.


### Notes de version v2.13 {#v213-release-notes}

*Correctifs de bogues*

*Sortie le 18 avril 2019*

**Correctifs de bogues :**

- Corriger les lectures de longueur nulle causant des problèmes avec les filtres d'E/S qui ne les attendaient pas. (*Signalement par brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru.*)
- Corriger la fiabilité du rapport d'erreurs provenant des processus `local`/`remote`.
- Corriger les messages d'erreur Posix/CIFS qui indiquaient le mauvais nom de fichier lors d'écriture/synchronisation/fermeture.


### Notes de version v2.12 {#v212-release-notes}

*Implémentation C de l'archivage par poussée*

*Sortie le 11 avril 2019*

**AVERTISSEMENT IMPORTANT** : La nouvelle implémentation TLS/SSL interdit les points dans les noms de buckets S3 conformément à la RFC-2818. Cette correction de sécurité est obligatoire pour une vérification conforme du nom d'hôte.

**Correctifs de bogues :**

- Corriger les problèmes survenant lorsque l'option de chemin se termine par / . (*Signalement par Marc Cousin.*)
- Corriger les problèmes lorsque `log-level-file=off` est défini pour la commande `archive-get`. (*Signalement par Brad Nicholson.*)
- Corriger le code C pour reconnaître le format d'option `host:port` comme le fait Perl. (*Signalement par Kyle Nevins.*)
- Corriger les problèmes liés aux options de journalisation de la commande `remote`/`local`.

**Améliorations :**

- La commande `archive-push` est entièrement implémentée en C.
- Augmenter la limite `process-max` à `999`. (*Suggéré par Rakshitha-BR.*)
- Améliorer le message d'erreur lorsque le nom d'un bucket S3 contient des points.

**Améliorations de la documentation :**

- Préciser que les magasins d'objets compatibles S3 sont pris en charge. (*Suggéré par Magnus Hagander.*)


### Notes de version v2.11 {#v211-release-notes}

*Implémentation C de l'archive get*

*Sortie le 11 mars 2019*

**Correctifs de bogues :**

- Correction de segments WAL tronqués éventuels en cas d'erreur survenue pendant l'écriture. (*Signalement par blogh.*)
- Correction de la commande info qui manquait les valeurs min/max WAL lorsque la stanza était spécifiée. (*Corrigé par Stefan Fercot. Révisé par David Steele.*)
- Correction de la sortie JSON non conforme pour les options transmises du C au Perl. (*Signalement par Leo Khomenko.*)

**Améliorations :**

- La commande `archive-get` est entièrement implémentée en C.
- Activer la fonctionnalité de maintien de connexion (keep-alive) sur les versions anciennes de Perl. (*Contribution de Marc Cousin. Révisé par David Steele.*)
- Erreur lorsqu'on passe des paramètres à une commande qui n'en accepte pas. (*Suggéré par Jason O'Donnell.*)
- Ajouter des indications lorsque l'on ne parvient pas à trouver un segment WAL dans l'archive. (*Suggéré par Hans-Jürgen Schönig.*)
- Améliorer le message d'erreur lorsque le nom d'hôte ne peut être trouvé dans un certificat. (*Suggéré par James Badger.*)
- Ajouter des options supplémentaires à `backup.manifest` à des fins de débogage. (*Contribution de blogh. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Mettre à jour la version par défaut de la documentation pour PostgreSQL 10.


### Notes de version v2.10 {#v210-release-notes}

*Correctifs de bogues*

*Sortie le 9 février 2019*

**Correctifs de bogues :**

- Ajoute une méthode de pilote S3 non implémentée requise pour `archive-get`. (*Signalement par mibiio.*)
- Corrige la vérification de la configuration incorrecte de `pg-path`. (*Signalement par James Chanco Jr.*)


### Notes de version v2.09 {#v209-release-notes}

*Améliorations mineures et corrections de bogues*

*Sortie le 30 janvier 2019*

**Correctifs de bogues :**

- Corriger le problème lié à la présence de plusieurs fichiers d'état asynchrones entraînant une erreur fatale. (*Signalement par Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley.*)

**Améliorations :**

- La commande `info` est entièrement implémentée en C. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Simplifier le message texte de la commande `info` lorsqu'aucun stanza n'est présent. Remplacer le chemin du dépôt par « le dépôt ».
- Ajouter le drapeau `_DARWIN_C_SOURCE` au fichier Makefile pour les compilations sur MacOS. (*Contribution de Douglas J Hunley. Révisé par David Steele.*)
- Mettre à jour la recherche d'adresse dans le client TLS C pour utiliser des méthodes modernes. (*Suggéré par Bruno Friedmann.*)
- Inclure l'en-tête conforme à Posix pour `strcasecmp()` et `fd_set`. (*Suggéré par ucando.*)

**Correctifs de bogues dans la documentation :**

- Corriger le chemin du dépôt codé en dur. (*Signalement par Heath Lord.*)

**Améliorations de la documentation :**

- Préciser que le chiffrement est toujours effectué côté client. (*Suggéré par Bruce Burdick.*)
- Ajouter des exemples pour la construction d'un hôte de documentation.
- Permettre `if` dans les variables de manifeste, les listes et les éléments de liste.


### Notes de version v2.08 {#v208-release-notes}

*Améliorations mineures et corrections de bogues*

*Sortie le 2 janvier 2019*

**Correctifs de bogues :**

- Supprimer la requête d'information sur l'objet S3 immédiatement après son envoi. (*Signalement par Matt Kunkel.*)
- Corriger `archive-get-queue-max` pour qu'il soit de type `size`. (*Signalement par Ronan Dunklau.*)
- Ajouter un message d'erreur lorsque l'utilisateur actuel `uid`/`gid` ne correspond à aucun nom. (*Signalement par Camilo Aguilar.*)
- Erreur lorsque `--target-action=shutdown` est spécifié pour PostgreSQL < 9.5.

**Améliorations :**

- Activer les keepalives TCP sur les connexions S3. (*Suggéré par Ronan Dunklau.*)
- Réorganiser la sortie texte de la commande `info` afin que la sauvegarde la plus récente soit affichée en dernier. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Ryan Lambert.*)
- Modifier les propriétaires de fichiers uniquement lorsque nécessaire.
- Masquer l’en-tête `authentication` lors de la levée d’erreurs S3. (*Suggéré par Brad Nicholson.*)

**Améliorations de la documentation :**

- Préciser quand `target-action` prend effet et la prise en charge des versions de PostgreSQL. (*Suggéré par Keith Fiske.*)
- Préciser que la région/le point de terminaison doit être correctement configuré pour le bucket. (*Suggéré par Pritam Barhate.*)
- Ajouter la documentation relative à la construction de la documentation.


### Notes de version v2.07 {#v207-release-notes}

*Vérification automatique de la somme de contrôle des différences de sauvegarde*

*Sortie le 16 novembre 2018*

**Correctifs de bogues :**

- Corriger le problème où `archive-push-queue-max` n'était pas pris en compte en cas d'erreur de connexion. (*Signalement par Lardière Sébastien.*)
- Corriger la taille statique du segment WAL utilisée pour déterminer si la limite de `archive-push-queue-max` a été dépassée.
- Corriger l'erreur survenue après un échec d'ouverture du fichier journal lorsque le traitement doit continuer. (*Signalement par vthriller.*)

**Fonctionnalités :**

- Activer automatiquement la somme de contrôle de sauvegarde delta lorsqu'une anomalie (par exemple, un changement de timeline) est détectée. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations :**

- Réessayer toutes les erreurs S3 `5xx`, et non plus seulement les erreurs internes `500`. (*Suggéré par Craig A. James.*)


### Notes de version v2.06 {#v206-release-notes}

*Sauvegarde delta par sommes de contrôle et prise en charge de PostgreSQL 11*

*Sortie le 15 octobre 2018*

**Correctifs de bogues :**

- Corriger le codage URI manquant dans le pilote S3. (*Signalement par Dan Farrell.*)
- Corriger le message d'erreur incorrect pour les options en double dans les fichiers de configuration. (*Signalement par Jesper St John.*)
- Corriger l'erreur signalée de manière incorrecte dans la journalisation de `info`. Un code de retour 1 provenant de `archive-get` était enregistré comme un message d'erreur au niveau `info` mais fonctionnait correctement dans les autres cas.

**Fonctionnalités :**

- Ajouter un delta de somme de contrôle pour les sauvegardes incrémentielles. Les sauvegardes incrémentielles utilisant un delta de somme de contrôle déterminent si les fichiers ont changé à l'aide de sommes de contrôle plutôt que de timestamps. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Prise en charge de PostgreSQL 11, y compris la taille configurable des segments WAL.

**Améliorations :**

- Ignorez tous les fichiers dans un répertoire de tablespace lié, sauf le sous-répertoire correspondant à la version actuelle de PostgreSQL. Une erreur était précédemment générée si d'autres fichiers étaient présents et non possédés par l'utilisateur PostgreSQL.
- Améliorer la commande `info` afin d'afficher le type de chiffrement de la stanza. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Douglas J Hunley.*)
- Améliorer le support des caractères spéciaux dans les noms de fichiers.
- Permettre de spécifier l'option `delta` dans le fichier de configuration de pgBackRest. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Utilisez `command` dans `authorized_hosts` afin d'améliorer la sécurité SSH. (*Suggéré par Stephen Frost, Magnus Hagander.*)
- Liste des valeurs autorisées pour l'option `buffer-size` dans la référence de configuration. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Stéphane Schildknecht.*)


### Notes de version v2.05 {#v205-release-notes}

*Options de variables d'environnement et exclusion des relations temporaires/non enregistrées*

*Sortie le 31 août 2018*

**Correctifs de bogues :**

- Corriger le problème où les liens *relatifs* dans `$PGDATA` pouvaient être stockés dans la sauvegarde avec un chemin incorrect. Ce problème n'affectait pas les liens absolus, et les liens relatifs vers des espaces de table étaient détectés par d'autres vérifications. (*Signalement par Cynthia Shang.*)
- Supprimer l'option incomplètement implémentée `online` de la commande `check`. L'opération hors ligne va à l'encontre de l'objectif de cette commande, qui est de vérifier si l'archivage et les sauvegardes fonctionnent correctement. (*Signalement par Jason O'Donnell.*)
- Corriger le problème où les erreurs levées en C n'étaient pas journalisées lorsqu'elles étaient appelées depuis Perl. pgBackRest se terminait correctement avec le bon code d'erreur, mais ne fournissait pas de message d'erreur pour faciliter le débogage. (*Signalement par Douglas J Hunley.*)
- Corriger le problème survenant lorsque l'option booléenne (par exemple `delta`) était spécifiée plus d'une fois. (*Signalement par Yogesh Sharma.*)

**Fonctionnalités :**

- Permet de définir n'importe quelle option via une variable d'environnement. Cela inclut les options qui pouvaient auparavant être spécifiées uniquement en ligne de commande, par exemple `stanza`, ainsi que les options sensibles qui ne pouvaient pas être spécifiées en ligne de commande, par exemple `repo1-s3-key-secret`.
- Exclut les fichiers de relations (table/index) temporaires et non enregistrées de la sauvegarde. Implémenté à l'aide de la même logique que les correctifs ajoutant cette fonctionnalité à PostgreSQL, [8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25) et [920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f). L'exclusion des relations temporaires est activée dans PostgreSQL ≥ `9.0`. L'exclusion des relations non enregistrées est activée dans PostgreSQL ≥ `9.1`, où cette fonctionnalité a été introduite. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Autorise l'exclusion arbitraire de répertoires et/ou de fichiers d'une sauvegarde. Une utilisation incorrecte de cette fonctionnalité peut entraîner des sauvegardes incohérentes ; lisez attentivement la documentation de `--exclude` avant de l'utiliser. (*Révisé par Cynthia Shang.*)
- Ajoute l'option `log-subprocess` pour permettre la journalisation des fichiers pour les sous-processus `local` et `remote`.
- Prise en charge de PostgreSQL 11 Beta 3.

**Améliorations :**

- Autoriser les fichiers de taille nulle dans le manifeste de sauvegarde pour référencer un manifeste antérieur, indépendamment de l'écart de timestamp. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Améliorer les performances asynchrones de `archive-get`/`archive-push` en vérifiant directement les fichiers d'état. (*Contribution de Stephen Frost. Révisé par David Steele.*)
- Améliorer le message d'erreur lorsqu'une commande manque l'option `stanza`. (*Suggéré par Sarah Conway.*)

**Correctifs de bogues dans la documentation :**

- Corriger le niveau de journalisation incorrect dans la référence de l'option `log-path`. (*Signalement par Camilo Aguilar.*)

**Améliorations de la documentation :**

- Cessez de tenter d'organiser les contributeurs dans `release.xml` par nom puis prénom. Les noms des contributeurs ont toujours été présentés dans les notes de version exactement tels qu'indiqués, mais nous avons tenté d'attribuer des identifiants internes basés sur le nom puis prénom, ce qui peut être difficile à déterminer et ne présente finalement pas de sens. Inspiré par la conférence de Christophe à PostgresOpen 2017, « Les êtres humains n'ont pas de clé primaire ». (*Suggéré par Christophe Pettus.*)

**Améliorations de la suite de tests :**

- Erreur si la compilation de LibC est effectuée en dehors de l'environnement de test. LibC n'est plus requis pour les compilations de production.


### Notes de version v2.04 {#v204-release-notes}

*Correction critique de bogue pour la reprise de sauvegarde*

*Sortie le 5 juillet 2018*

**NOTE IMPORTANTE** : Cette version corrige un bogue critique dans la fonctionnalité de reprise de sauvegarde. Toutes les sauvegardes reprises antérieures à cette version doivent être considérées comme incohérentes. Une sauvegarde sera reprise après l'échec d'une sauvegarde précédente, sauf si `resume=n` a été spécifié. Une sauvegarde reprise peut être identifiée en consultant le journal de sauvegarde pour le message « aborted backup of same type exists, will be cleaned to remove invalid files and resumed ». Si ce message est présent, n'utilisez pas cette sauvegarde ni aucune autre sauvegarde du même ensemble pour une restauration, et vérifiez les journaux de restauration pour savoir si une sauvegarde reprise a été restaurée. Dans ce cas, des données incohérentes peuvent être présentes dans le cluster.

**Correctifs de bogues :**

- Corriger un bogue critique dans la reprise qui entraînait des sauvegardes incohérentes. Une régression dans `v0.82` avait supprimé la comparaison des horodatages lors de la décision des fichiers à conserver de la sauvegarde interrompue lors de la reprise. Voir la note ci-dessus pour plus de détails. (*Signalement par David Youatt, Yogesh Sharma, Stephen Frost.*)
- Corriger l'erreur dans la restauration sélective lorsque seule une base utilisateur existe dans le cluster. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Nj Baliyan.*)
- Corriger le format d'horodatage ISO-8601 non conforme dans les en-têtes d'autorisation S3. AWS et certaines passerelles toléraient un espace au lieu d'heures zéro-paddées, tandis que d'autres ne le faisaient pas. (*Corrigé par Andrew Schwartz. Révisé par David Steele.*)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 11 Beta 2.

**Améliorations :**

- Améliorer le client HTTP pour définir `content-length` à 0 lorsque non spécifié par le serveur. S3 (et les passerelles) définissent toujours `content-length` ou `transfer-encoding`, mais `HTTP 1.1` n'exige pas cette valeur, et les proxies (par exemple HAProxy) peuvent ne pas inclure l'un ni l'autre. (*Suggéré par Adam K. Sumner.*)
- Définir `search_path = 'pg_catalog'` sur les connexions PostgreSQL. (*Suggéré par Stephen Frost.*)

**Améliorations de la documentation :**

- Créez une nouvelle section pour décrire la compilation de pgBackRest et effectuez la compilation sur un hôte distinct.
- Ajoutez un exemple de stratégie S3 pour restreindre les privilèges sur le bucket. (*Suggéré par Douglas J Hunley, Jason O'Donnell.*)


### Notes de version v2.03 {#v203-release-notes}

*Exécutable unique pour le déploiement*

*Sortie le 22 mai 2018*

**Correctifs de bogues :**

- Corriger un dépassement de tampon potentiel dans la gestion des messages d'erreur. (*Signalement par Lætitia.*)
- Corriger l'acquisition du verrou d'écriture sur l'archive pour la commande synchronisée `archive-get`. (*Signalement par uspen.*)

**Améliorations :**

- Intégrer directement les fonctions C exportées et les modules Perl dans l'exécutable pgBackRest.
- Utilisez `time_t` à la place de `__time_t` pour une meilleure portabilité. (*Suggéré par Nick Floersch.*)
- Afficher le temps d'exécution total en millisecondes à la fin de la commande.


### Notes de version v2.02 {#v202-release-notes}

*Archivage asynchrone parallèle et configuration incluse*

*Sortie le 6 mai 2018*

**Correctifs de bogues :**

- Corriger la synchronisation récursive des répertoires, qui s'exécutait de manière récursive alors que seul le répertoire spécifié devait être synchronisé. (*Signalement par Craig A. James.*)
- Corriger l'erreur « chemin introuvable » levée par `archive-copy` lors des sauvegardes incrémentielles ou différentielles. (*Signalement par yummyliu, Vitaliy Kukharik.*)
- Corriger l'échec de construction du manifeste lorsque deux ou plusieurs fichiers dans `PGDATA` sont liés au même répertoire. (*Signalement par Vitaliy Kukharik.*)
- Corriger l'échec de la restauration delta lorsqu'un fichier lié est manquant.
- Corriger l'affichage des options clé/valeur et des listes dans l'aide. (*Signalement par Clinton Adams.*)

**Fonctionnalités :**

- Ajouter un `archive-get` asynchrone et parallèle. Cette fonctionnalité maintient une file d’attente de segments WAL afin de réduire la latence lorsque PostgreSQL demande un segment WAL via la commande restore_command.
- Ajouter la prise en charge de fichiers de configuration pgBackRest supplémentaires. Le répertoire est spécifié par l’option `--config-include-path`. Ajouter l’option `--config-path` pour remplacer le chemin de base par défaut des options `--config` et `--config-include-path`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajouter l’option `repo-s3-token` pour permettre la configuration de jetons d’identité temporaires. pgBackRest ne dispose actuellement d’aucun moyen de demander de nouvelles identités, de sorte que toute commande (par exemple `backup`, `restore`) doit s’achever avant l’expiration des identités. (*Contribution de Yogesh Sharma. Révisé par David Steele.*)

**Améliorations :**

- Mettez à jour les options `archive-push-queue-max`, `manifest-save-threshold` et `buffer-size` pour accepter des valeurs en `KB`, `MB`, `GB`, `TB` ou `PB` où le multiplicateur est une puissance de `1024`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Améliorez l'efficacité de la synchronisation du chemin de sauvegarde/restauration. Le balayage de tout le répertoire peut être très coûteux si de nombreuses petites tables sont présentes. Le manifeste de sauvegarde contient la liste des chemins ; utilisez-le pour effectuer les synchronisations au lieu de balayer le chemin de sauvegarde/restauration.
- Affichez les paramètres de commande ainsi que les options de commande dans le message initial du journal d'information.
- Renommez l'option archive-queue-max en archive-push-queue-max. Cette modification est cohérente avec la nouvelle option `archive-get-queue-max`. Le nom d'option ancien sera toujours accepté.

**Correctifs de bogues dans la documentation :**

- Mettre à jour la documentation pour inclure la prise en charge des systèmes 32 bits et les précautions associées. La prise en charge des systèmes 32 bits a été ajoutée à la version 1.26. (*Signalement par Viorel Tabara.*)

**Améliorations de la documentation :**

- Ajouter des exemples de surveillance utilisant PostgreSQL et jq. (*Suggéré par Stephen Frost, Brian Faherty.*)
- Ajouter un exemple d'utilisation de la section commande dans la configuration de l'archivage. (*Suggéré par Christophe Courtois.*)
- Supprimer la documentation décrivant `info --output=json` comme expérimentale.
- Mettre à jour la description obsolète de l'option `spool-path`.

**Fonctionnalités du jeu de tests :**

- Utilisez lcov pour le rapport de couverture des tests unitaires en C. Passez de Devel::Cover car celui-ci ne rapportait pas la couverture des branches pour les rapports convertis à partir de gcov. Une couverture de branche incomplète pour un module génère désormais une erreur. La couverture des tests unitaires n'est pas affichée dans le rapport à moins qu'elle ne soit incomplète, soit en couverture d'instructions, soit en couverture de branches.


### Notes de version v2.01 {#v201-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 19 mars 2018*

**Correctifs de bogues :**

- Correction des options `--target-action` et `--recovery-option` signalées comme non valides lors de la restauration avec `--type=immediate`. (*Signalement par Brad Nicholson.*)
- Erreur immédiate lorsqu'une option sécurisée (par exemple `repo1-s3-key`) est passée en ligne de commande. Comme pgBackRest ne transmettait pas les options sécurisées aux sous-processus, une erreur obscure était générée. L'erreur nouvelle est bien plus claire et fournit des indications sur la manière de résoudre le problème. Mise à jour de la documentation de la commande pour omettre les options sécurisées qui ne peuvent pas être spécifiées en ligne de commande. (*Signalement par Brad Nicholson.*)
- Correction du problème de passage de `--no-config` à Perl intégré. (*Signalement par Ibrahim Edib Kokdemir.*)
- Correction du problème où la spécification de `log-level-stderr` > `warn` entraînait une erreur du processus `local`/`remote` à la sortie, en raison de la présence de données sur stderr alors qu'aucune n'était attendue. La valeur maximale pour un processus `local`/`remote` est désormais `error`, car il n'existe aucune raison pour que ces processus émettent des avertissements. (*Signalement par Clinton Adams.*)
- Correction du test de manifest dans la commande `check` lorsque des espaces de table sont présents. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Thomas Flatley.*)

**Améliorations :**

- Erreur lorsque plusieurs arguments sont définis dans le fichier de configuration pour une option qui ne prend pas plusieurs arguments. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Supprimer les commandes sudo superflues dans `src/Makefile`. (*Contribution de Adrian Vondendriesch. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Afficher l'index dans les exemples pour les options indexées, par exemple `repo-*`, `pg-*`. (*Suggéré par Stephen Frost.*)
- Simplifier la table des matières sur la page de commande en ne listant que les commandes. (*Suggéré par Stephen Frost.*)
- Supprimer les références à la bibliothèque C étant facultative.

**Fonctionnalités du jeu de tests :**

- Ajouter les versions du paquet CentOS/RHEL.
- Utiliser clang pour l'analyse statique du code. Rien trouvé initialement, hormis certaines fonctions qui auraient dû être marquées `__noreturn__`.


### Notes de version v2.00 {#v200-release-notes}

*Améliorations des performances pour l’envoi d’archive*

*Sortie le 23 février 2018*

**Fonctionnalités :**

- La commande `archive-push` est désormais partiellement écrite en C, ce qui permet à PostgreSQL `archive_command` de s'exécuter de manière significativement plus rapide lors du traitement des messages d'état provenant du processus d'archive asynchrone. (*Révisé par Cynthia Shang.*)

**Améliorations :**

- Améliorer la commande `check` afin de vérifier que le manifeste de sauvegarde peut être construit. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Améliorer les performances du client HTTPS. Le tamponnage prend désormais en compte les `pending` octets sur la socket (lorsqu'ils sont présents) plutôt que de se fier uniquement à `select()`. Dans certains cas, les derniers octets n'étaient pas envoyés avant la fermeture de la connexion.
- Améliorer les performances de suppression sur S3. La constante `S3_BATCH_MAX` avait été remplacée par une valeur codée en dur de 2, probablement durant des tests.
- Permettre la réinitialisation à la valeur par défaut de toute option non liée à la ligne de commande depuis la ligne de commande. Cela permet de réinitialiser les options dans `pgbackrest.conf` à leur valeur par défaut, réduisant ainsi la nécessité d'écrire de nouveaux fichiers de configuration pour des besoins spécifiques.
- La bibliothèque C est désormais requise. Cela élimine le chargement conditionnel et simplifie le développement de nouvelles fonctionnalités de la bibliothèque.
- L'exécutable `pgbackrest` est désormais un binaire C au lieu d'un script Perl. Cela permet à certaines commandes critiques en termes de temps (comme `archive-push` en mode asynchrone) de s'exécuter plus rapidement.
- Renommer les options `db-*` en `pg-*` et les options `backup-*` en `repo-*` afin d'améliorer la cohérence. Les options `repo-*` sont désormais indexées, bien qu'actuellement une seule soit autorisée.

**Fonctionnalités de la documentation :**

- Tous les clusters dans la documentation sont initialisés avec des sommes de contrôle.

**Améliorations de la documentation :**

- Liste les noms d'option obsolètes dans la documentation et dans l'aide en ligne de commande.
- Précisez que les buckets S3 doivent être créés par l'utilisateur. (*Suggéré par David Youatt.*)


### Notes de version v1.29 {#v129-release-notes}

*Correction critique de bogue pour la reprise de sauvegarde*

*Sortie le 5 juillet 2018*

**NOTE IMPORTANTE** : Cette version corrige un bogue critique dans la fonctionnalité de reprise de sauvegarde. Toutes les sauvegardes reprises antérieures à cette version doivent être considérées comme incohérentes. Une sauvegarde sera reprise après l'échec d'une sauvegarde précédente, sauf si `resume=n` a été spécifié. Une sauvegarde reprise peut être identifiée en consultant le journal de sauvegarde pour le message « aborted backup of same type exists, will be cleaned to remove invalid files and resumed ». Si ce message est présent, n'utilisez pas cette sauvegarde ni aucune autre sauvegarde du même ensemble pour une restauration, et vérifiez les journaux de restauration pour savoir si une sauvegarde reprise a été restaurée. Dans ce cas, des données incohérentes peuvent être présentes dans le cluster.

**Correctifs de bogues :**

- Corriger un bogue critique dans la reprise qui entraînait des sauvegardes incohérentes. Une régression dans `v0.82` avait supprimé la comparaison des horodatages lors de la décision des fichiers à conserver de la sauvegarde interrompue lors de la reprise. Voir la note ci-dessus pour plus de détails. (*Signalement par David Youatt, Yogesh Sharma, Stephen Frost.*)
- Corriger le format d'horodatage ISO-8601 non conforme dans les en-têtes d'autorisation S3. AWS et certaines passerelles acceptaient un espace au lieu d'un zéro pour les heures, tandis que d'autres ne le faisaient pas. (*Corrigé par Andrew Schwartz. Révisé par David Steele.*)
- Corriger les synchronisations de répertoires qui s'exécutaient de manière récursive alors que seul le répertoire spécifié devait être synchronisé. (*Signalement par Craig A. James.*)
- Corriger la signalisation d'options `--target-action` et `--recovery-option` comme étant non valides lors de la restauration avec `--type=immediate`. (*Signalement par Brad Nicholson.*)
- Corriger `archive-copy` qui provoquait une erreur « chemin introuvable » pour les sauvegardes incrémentielles ou différentielles. (*Signalement par yummyliu, Vitaliy Kukharik.*)
- Corriger l'échec de la construction du manifeste lorsque deux ou plusieurs fichiers dans `PGDATA` sont liés au même répertoire. (*Signalement par Vitaliy Kukharik.*)
- Corriger l'échec de la restauration delta lorsqu'un fichier lié était manquant.
- Corriger l'erreur lors d'une restauration sélective lorsque seule une base utilisateur existe dans le cluster. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Nj Baliyan.*)

**Améliorations :**

- Améliorer le client HTTP pour définir `content-length` à 0 lorsque non spécifié par le serveur. S3 (et les passerelles) définissent toujours `content-length` ou `transfer-encoding`, mais `HTTP 1.1` ne l'exige pas, et les proxies (par exemple HAProxy) peuvent ne pas inclure l'un ni l'autre. (*Suggéré par Adam K. Sumner.*)
- Améliorer les performances du client HTTPS. Le tampon prend désormais en compte les `pending` octets sur la socket (lorsqu'ils sont présents) plutôt que de se fier uniquement à `select()`. Dans certains cas, les derniers octets n'étaient pas envoyés avant la fermeture de la connexion.
- Améliorer les performances de suppression S3. La constante `S3_BATCH_MAX` avait été remplacée par une valeur codée en dur de 2, probablement pendant les tests.
- Optimiser la synchronisation des chemins de sauvegarde/restauration. Scanner tout le répertoire peut être très coûteux si de nombreuses petites tables sont présentes. Le manifeste de sauvegarde contient la liste des chemins, donc il est désormais utilisé pour effectuer les synchronisations au lieu de scanner le chemin de sauvegarde/restauration. Supprimer la fonctionnalité de synchronisation récursive des chemins, qui n'est plus utilisée.

**Correctifs de bogues dans la documentation :**

- Mettre à jour la documentation pour inclure la prise en charge des systèmes 32 bits et les précautions associées. La prise en charge des systèmes 32 bits a été ajoutée à la version 1.26. (*Signalement par Viorel Tabara.*)

**Améliorations de la documentation :**

- Préciser que les buckets S3 doivent être créés par l'utilisateur. (*Suggéré par David Youatt.*)
- Mettre à jour la description obsolète de l'option `spool-path`.


### Notes de version v1.28 {#v128-release-notes}

*Suppression d'une stanza*

*Sortie le 1er février 2018*

**Correctifs de bogues :**

- Corrigé l'impossibilité de restaurer une base de données unique contenue dans un tablespace à l'aide de --db-include. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Chiranjeevi Ravilla.*)
- Assurez-vous que la dernière version de `db-id` est sélectionnée lors de la correspondance entre `archive.info` et `backup.info`. Cela garantit une correspondance correcte en cas de doublons de `system-id` et `db-version` (par exemple, après un retour en arrière d'une `pg_upgrade`). (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Adam K. Sumner.*)
- Corrigé le message d'erreur excessivement verbeux lors de la signalisation d'une commande non valide. (*Signalement par Jason O'Donnell.*)

**Fonctionnalités :**

- Ajouter la commande `stanza-delete` pour nettoyer les stanzas inutilisés. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Magnus Hagander.*)

**Améliorations :**

- Améliorer la commande `stanza-create` afin qu'elle ne génère pas d'erreur lorsque la stanza existe déjà. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Mettre à jour la documentation `stanza-create --force` pour insister sur la prudence à observer lors de son utilisation. (*Suggéré par Jason O'Donnell.*)


### Notes de version v1.27 {#v127-release-notes}

*Correctifs de bogues et documentation*

*Sortie le 19 décembre 2017*

**Correctifs de bogues :**

- Corrigé un problème qui masquait les erreurs de localité pour `backup` et `restore`. Lorsqu’un hôte de sauvegarde est présent, les sauvegardes doivent être autorisées uniquement sur l’hôte de sauvegarde et les restaurations uniquement sur l’hôte de base de données, sauf si une configuration alternative est définie pour ignorer l’hôte distant. (*Signalement par Lardière Sébastien.*)

- Corrigé un problème où les WAL n’étaient pas expirées sous PostgreSQL 10. Ce problème était dû à une expression régulière incorrecte qui supposait que toutes les versions majeures de PostgreSQL étaient au format X.X. (*Signalement par Adam Brusselback.*)

- Corrigé un problème où l’option `--no-config` n’était pas transmise aux processus enfants. Cela signifiait que les processus enfants lisaient encore le fichier de configuration local et pouvaient provoquer des comportements inattendus.

- Corrigé la commande `info` afin d’éliminer la sortie `"db (prior)"` lorsque aucune sauvegarde ou archive n’existe pour une version antérieure du cluster. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Stephen Frost.*)

**Fonctionnalités de la documentation :**

- Documentez la relation entre les options `archive-copy` et `archive-check`. (*Suggéré par Markus Nullmeier.*)
- Améliorez la documentation de référence de `archive-copy`.


### Notes de version v1.26 {#v126-release-notes}

*Chiffrement du dépôt*

*Sortie le 21 novembre 2017*

**Correctifs de bogues :**

- Corrigé un problème pouvant entraîner l'échec du copiage de manifestes volumineux lors d'une restauration. (*Signalement par Craig A. James.*)
- Corrigé le décalage WAL incorrect sur les architectures 32 bits. (*Corrigé par Javier Wilson. Révisé par David Steele.*)
- Corrigé un problème de récupération du WAL pour les anciennes versions de la base de données. Après une `stanza-upgrade`, il devrait toujours être possible de restaurer des sauvegardes de la version précédente et de procéder à une récupération avec `archive-get`. Toutefois, archive-get ne vérifiait que la dernière version/id de base de données et échouait. Correction également de certains problèmes lorsque la même version/id de base de données apparaît plusieurs fois dans l'historique. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Clinton Adams.*)
- Corrigé un problème concernant la définition correcte des groupes de sauvegarde lors d'une restauration. Si la sauvegarde ne parvient pas à mapper un groupe à un nom, elle stocke le groupe dans le manifeste sous la forme `false` puis utilise soit le propriétaire de $PGDATA pour définir le groupe lors de la restauration, soit, à défaut, le groupe de l'utilisateur courant. Cette logique ne fonctionnait pas correctement car le groupe sélectionné écrasait l'utilisateur lors de la restauration, laissant le groupe indéfini et l'utilisateur incorrectement défini comme le groupe. (*Signalement par Jeff McCormick.*)

- Corrigé un problème de passage de paramètres aux hôtes distants. Lorsqu'un nombre supérieur à une base de données était spécifié, le chemin, le port et le chemin du socket étaient passés pour db1 indépendamment de la base de données réellement ciblée. (*Signalement par uspen.*)

**Fonctionnalités :**

- Prise en charge du chiffrement du dépôt. (*Contribution de Cynthia Shang, David Steele.*)

**Améliorations :**

- Désactivez le filtre gzip lorsque `--compress-level-network=0`. Ce filtre était utilisé avec un niveau de compression défini à 0, ce qui ajoutait une surcharge sans aucun bénéfice.
- Amélioration des performances de décompression pour le filtre gzip.

**Fonctionnalités de la documentation :**

- Ajouter un modèle pour améliorer les informations initiales collectées lors de la soumission de rapports. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Préciser l'utilisation de l'option `archive-timeout` et décrire la différence avec le paramètre archive_timeout de PostgreSQL. (*Contribution de Cynthia Shang. Révisé par David Steele. Suggéré par Keith Fiske.*)

**Fonctionnalités du jeu de tests :**

- Tests automatisés pour l'architecture 32 bits i386/i686.


### Notes de version v1.25 {#v125-release-notes}

*Améliorations des performances S3*

*Sortie le 24 octobre 2017*

**Correctifs de bogues :**

- Corriger les paramètres personnalisés pour l'option `compress-level` ignorés. (*Signalement par Jens Wilke.*)
- Supprimer l'erreur détectée lors de la détection de lignes temporelles chevauchantes. Les lignes temporelles chevauchantes sont valides dans de nombreux scénarios de récupération à un instant donné (PITR). (*Signalement par blogh.*)
- Corriger les cas où `database-id` n'était pas rendu comme un entier dans la sortie JSON d'information. (*Corrigé par Cynthia Shang. Révisé par David Steele. Signalement par Jason O'Donnell.*)

**Fonctionnalités :**

- Améliorer les performances des requêtes de liste sur S3. Toute portion littérale au début d'une expression de filtre est utilisée pour générer un préfixe de recherche, ce qui permet souvent de maintenir la requête suffisamment petite pour éviter les limitations de débit. (*Suggéré par Mihail Shvein.*)

**Fonctionnalités du jeu de tests :**

- Ajouter des tests de performance I/O.


### Notes de version v1.24 {#v124-release-notes}

*Nouvelles exclusions de sauvegarde*

*Sortie le 28 septembre 2017*

**Correctifs de bogues :**

- Corrigé un problème où des avertissements étaient émis à la place de messages de journal de priorité inférieure lors de la sauvegarde depuis un serveur secondaire en cours d'initialisation. (*Signalement par uspen.*)

- Corrigé un problème où certaines options `db-*` (par exemple `db-port`) n'étaient pas transmises aux hôtes distants. (*Signalement par uspen.*)

**Fonctionnalités :**

- Exclure le contenu de `pg_snapshots`, `pg_serial`, `pg_notify` et `pg_dynshmem` de la sauvegarde, car ils sont régénérés au démarrage.
- Exclure les fichiers `pg_internal.init` de la sauvegarde, car ils sont régénérés au démarrage.

**Améliorations :**

- Ouvrir le fichier de journal après que le processus asynchrone est complètement séparé du processus principal afin d'éviter que le processus principal n'écrive également dans le fichier. (*Suggéré par Jens Wilke.*)

**Fonctionnalités de la documentation :**

- Configurer l'accès SSH sans mot de passe.

**Améliorations de la documentation :**

- Renommer master en primary dans la documentation pour l'aligner sur la convention PostgreSQL.


### Notes de version v1.23 {#v123-release-notes}

*Réplicas multiples et prise en charge de PostgreSQL 10*

*Sortie le 3 septembre 2017*

**Correctifs de bogues :**

- Corrigé un problème pouvant entraîner l'abandon de la compression sur les fichiers en croissance. (*Signalement par Jesper St John, Aleksandr Rogozin.*)
- Corrigé un problème empêchant l'envoi des messages d'activité (keep-alives) depuis le processus local vers le serveur distant. (*Signalement par William Cox.*)

**Fonctionnalités :**

- Jusqu'à sept serveurs secondaires peuvent être configurés pour effectuer une sauvegarde à partir d'un secondaire. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Prise en charge de PostgreSQL 10.
- Permettre `content-length` (en plus du codage par tronçons) lors de la lecture des données XML afin d'améliorer la compatibilité avec les passerelles S3 tierces. (*Suggéré par Victor Gdalevich.*)

**Améliorations :**

- Augmenter le délai d'attente HTTP pour S3.
- Ajouter des réessais HTTP pour renforcer la résilience face aux erreurs réseau transitoires de S3.

**Correctifs de bogues dans la documentation :**

- Corrigé la génération de documentation pour inclure des résumés de section sur la page Configuration. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.22 {#v122-release-notes}

*Correctif du réessai S3*

*Sortie le 9 août 2017*

**Correctifs de bogues :**

- Correctif d'un problème d'authentification dans la répétition des tentatives S3.


### Notes de version v1.21 {#v121-release-notes}

*Amélioration de la sortie d'informations et option de port SSH*

*Sortie le 8 août 2017*

**Correctifs de bogues :**

- Le répertoire `archive_status` est désormais régénéré lors d'une restauration afin de prendre en charge PostgreSQL 8.3, qui ne le recrée pas automatiquement comme le font les versions plus récentes. (*Signalement par Stephen Frost.*)
- Corrigé un problème pouvant laisser derrière lui un répertoire d'archive vide pour une ancienne version de PostgreSQL après une `stanza-upgrade`. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)

**Fonctionnalités :**

- Modifié la commande `info` (sortie texte et JSON) pour afficher l'identifiant d'archive ainsi que les valeurs minimale et maximale de WAL actuellement présentes dans l'archive pour la version actuelle du cluster de base de données et, le cas échéant, pour la version précédente. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

- Ajout des options `--backup-ssh-port` et `--db-ssh-port` pour prendre en charge les ports SSH non par défaut. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations :**

- Réessayer lorsque S3 retourne une erreur interne (500).

**Correctifs de bogues dans la documentation :**

- Précisez la description de `--online` en fonction du contexte de la commande.

**Fonctionnalités de la documentation :**

- Ajouter la création de `/etc/pgbackrest.conf` aux instructions d'installation manuelle.

**Améliorations de la documentation :**

- Déplacer les options du dépôt dans une section séparée dans l’aide en ligne de commande. (*Suggéré par Stephen Frost.*)


### Notes de version v1.20 {#v120-release-notes}

*Correctif de bogue critique 8.3/8.4*

*Sortie le 27 juin 2017*

**AVERTISSEMENT IMPORTANT** : les installations de PostgreSQL 8.3 et 8.4 utilisant des espaces de tables devraient être mises à niveau immédiatement, quelle que soit la version v1 installée, puis faire l’objet d’une sauvegarde complète. Un bogue empêchait les espaces de tables d’être sauvegardés sur ces versions uniquement. PostgreSQL ≥ 9.0 n’est pas affecté.

**Correctifs de bogues :**

- Corrigé un problème empêchant la sauvegarde des espaces de table sur PostgreSQL ≤ 8.4.
- Corrigé le flag manquant dans la compilation de la bibliothèque C, qui entraînait une incompatibilité binaire sur les systèmes 32 bits. (*Signalement par Adrian Vondendriesch.*)

**Fonctionnalités :**

- Ajoutez les options `s3-repo-ca-path` et `s3-repo-ca-file` pour prendre en charge les systèmes où les autorités de certification ne sont pas automatiquement trouvées par `IO::Socket::SSL`, par exemple RHEL7, ou pour charger des autorités de certification personnalisées. (*Suggéré par Scott Frazer.*)

**Fonctionnalités du jeu de tests :**

- Ajouter la génération de la documentation dans le CI.


### Notes de version v1.19 {#v119-release-notes}

*Prise en charge S3*

*Sortie le 12 juin 2017*

**Correctifs de bogues :**

- Corrigé la commande `info` afin que les valeurs minimale et maximale de l'archive WAL affichées correspondent à la version actuelle de la base de données. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Corrigé la commande `backup` afin que l'option `backup-standby` soit réinitialisée (et que la sauvegarde se poursuive sur le principal) si le serveur secondaire n'est pas configuré et/ou inaccessible. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Corrigé les avertissements de configuration provoqués par un processus distant entraînant des erreurs dans le processus principal. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)

**Fonctionnalités :**

- Prise en charge du dépôt Amazon S3. (*Révisé par Cynthia Shang.*)

**Correctifs de bogues dans la documentation :**

- Option `max-archive-mb` invalide modifiée dans la référence de configuration vers `archive-queue-max`.
- Correction de l'absence de `sudo` dans la section d'installation. (*Corrigé par Lætitia. Révisé par David Steele.*)


### Notes de version v1.18 {#v118-release-notes}

*Améliorations de la mise à jour, du réaménagement et du verrouillage de la stanza*

*Sortie le 12 avril 2017*

**Correctifs de bogues :**

-  Corrigé un problème où les opérations en lecture seule utilisant des processus workers locaux (par exemple `restore`) créaient des verrous d'écriture pouvant interférer avec le parallélisme de `archive-push`. (*Signalement par Jens Wilke.*)

**Fonctionnalités :**

- Ajouté la commande stanza-upgrade pour fournir un mécanisme de mise à jour d'une stanza après une mise à jour vers une nouvelle version majeure de PostgreSQL. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

- Ajouté la validation de `pgbackrest.conf` afin d'afficher des avertissements si les options ne sont pas valides ou ne se trouvent pas dans la section correcte. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations :**

- Simplifier le schéma de verrouillage. À présent, seul le processus principal détient les verrous d'écriture (pour les commandes `archive-push` et `backup`) et non plus tous les processus workers locaux et distants comme auparavant.
- Ne plus définir les horodatages des fichiers dans les répertoires de sauvegarde pour qu'ils correspondent aux horodatages du répertoire du cluster. Cela était initialement fait pour permettre la reprise de sauvegarde, mais ce processus est désormais implémenté à l'aide de sommes de contrôle.
- Amélioration du message d'erreur lorsque la commande `restore` détecte la présence de `postmaster.pid`. (*Suggéré par Yogesh Sharma.*)
- Réaffecter les codes de retour compris entre 25 et 125 afin d'éviter que PostgreSQL les interprète comme des exceptions signal fatales. (*Suggéré par Yogesh Sharma.*)


### Notes de version v1.17 {#v117-release-notes}

*Page Correction d'un bogue de somme de contrôle*

*Sortie le 13 mars 2017*

**Correctifs de bogues :**

- Corrigé un problème où des pages nouvellement initialisées (mais non utilisées) provoquaient des avertissements de somme de contrôle. (*Signalement par Stephen Frost.*)


### Notes de version v1.16 {#v116-release-notes}

*Améliorations de la somme de contrôle, intégration continue et test des paquets*

*Sortie le 2 mars 2017*

**Correctifs de bogues :**

- Corrigé un problème où les tables de plus de 1 Go affichaient des avertissements de somme de contrôle de page après le premier segment. (*Signalement par Stephen Frost.*)
- Corrigé un problème où les bases de données créées avec un tablespace non par défaut déclenchaient des avertissements erronés concernant le positionnement aligné des pages pour `pg_filenode.map` et `pg_internal.init`. (*Signalement par blogh.*)

**Fonctionnalités du jeu de tests :**

- Intégration continue avec `travis-ci`.
- Génération automatique des paquets Debian pour toutes les distributions prises en charge.


### Notes de version v1.15 {#v115-release-notes}

*Refactorisation et corrections de bogues*

*Sortie le 13 février 2017*

**Correctifs de bogues :**

- Corrigé une régression introduite dans la version 1.13 qui pouvait entraîner l'échec des sauvegardes si des fichiers étaient supprimés (par exemple, des tables supprimées) pendant la construction du manifeste. (*Signalement par Navid Golpayegani.*)


### Notes de version v1.14 {#v114-release-notes}

*Refactorisation et corrections de bogues*

*Sortie le 13 février 2017*

**Correctifs de bogues :**

- Corrigé un problème où une erreur lors de l'envoi d'une archive n'était pas réessayée et renvoyait des erreurs à PostgreSQL indéfiniment (sauf si le fichier `.error` était supprimé manuellement). (*Signalement par Jens Wilke.*)
- Corrigé une condition de course dans l'archivage parallèle où la création de nouveaux chemins provoquait une erreur lorsque plusieurs processus tentaient de la réaliser simultanément. (*Signalement par Jens Wilke.*)

**Améliorations :**

- Amélioration des performances de `wal archive min/max` fournie par la commande `info`. (*Suggéré par Jens Wilke.*)

**Fonctionnalités de la documentation :**

- Mise à jour de la documentation sur l'archivage asynchrone pour décrire plus précisément le fonctionnement de la nouvelle méthode et les différences avec l'ancienne méthode. (*Suggéré par Jens Wilke.*)


### Notes de version v1.13 {#v113-release-notes}

*Archivage parallèle, création de stanza, informations et vérification améliorées*

*Sortie le 5 février 2017*

**AVERTISSEMENT IMPORTANT** : La nouvelle implémentation de l'archivage asynchrone ne copie plus les WAL vers une file séparée. Si des WAL restent dans la file ancienne après la mise à jour vers `1.13`, elles seront abandonnées et **ne** seront pas envoyées au dépôt. Pour éviter ce résultat, arrêtez l'archivage en définissant `archive_command = false`. Ensuite, videz la file asynchrone en exécutant `pgbackrest --stanza=[stanza-name] archive-push` et attendez que le processus se termine. Vérifiez que la file dans `[spool-path]/archive/[stanza-name]/out` est vide. Enfin, installez `1.13` et restaurez la valeur initiale de `archive_command`. **AVERTISSEMENT IMPORTANT** : La commande `stanza-create` n'est plus facultative et doit être exécutée avant toute sauvegarde ou archivage sur une **nouvelle** stanza. Les stanzas existantes n'ont pas besoin d'exécuter `stanza-create`.

**Correctifs de bogues :**

- Correction d'une affectation constante fixe provoquant un avertissement du compilateur dans la bibliothèque C. (*Corrigé par Adrian Vondendriesch. Révisé par David Steele.*)
- Correction de quelques synchronisations de répertoires manquantes pour l'option `--repo-sync`.
- Correction d'un problème où l'absence d'un utilisateur/groupe lors d'une restauration pouvait provoquer une erreur « valeur non initialisée » dans `File->owner()`. (*Signalement par Leonardo GG Avellar.*)
- Correction d'un problème où les erreurs de non-correspondance de protocole ne produisaient pas la valeur attendue.
- Correction d'un message de journal `archive-get` erroné indiquant qu'un code de sortie de 1 correspondait à une terminaison anormale.

**Fonctionnalités :**

- Implémentation améliorée, multi-processus, de l'archivage asynchrone.
- Amélioration de la commande `stanza-create` afin qu'elle puisse réparer la plupart des dépôts endommagés et être suffisamment robuste pour être rendue obligatoire. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Amélioration de la commande `check` pour qu'elle puisse s'exécuter sur une instance de secours, bien que seules des vérifications basiques soient effectuées car `pg_switch_xlog()` ne peut pas être exécutée sur un réplica. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajout des plages d'archives et de sauvegardes à la commande `info`.
- Ajout d'un avertissement pour mettre à jour `pg_tablespace.spclocation` lors du remappage des espaces de tables dans PostgreSQL < 9.2. (*Contribution de blogh. Révisé par David Steele.*)
- Suppression des exigences de verrouillage distant pour les commandes `archive-get`, `restore`, `info` et `check`, puisqu'il s'agit d'opérations en lecture seule. (*Suggéré par Michael Vitale.*)

**Améliorations :**

- Le bannière du fichier de journal n'est pas affichée avant la première entrée de journal écrite. (*Suggéré par Jens Wilke.*)
- Réduit la probabilité de faux positifs dans les sommes de contrôle de page causés par des pages déchirées en filtrant sur le LSN de début de sauvegarde.
- Supprime l'optimisation spécifique à Intel des drapeaux de compilation de la bibliothèque C. (*Contribution de Adrian Vondendriesch. Révisé par David Steele.*)
- Supprime l'option `--lock`. Cette option a été introduite avant que le répertoire de verrouillage ne puisse être situé en dehors du dépôt et est désormais obsolète.
- Ajoute l'option `--log-timestamp` pour permettre de supprimer les horodatages dans la journalisation. Cela est principalement utilisé pour éviter les filtres dans la documentation automatisée.
- Renvoie un code d'erreur approprié lorsqu'il n'est pas possible de convertir un chemin relatif en chemin absolu. (*Suggéré par Yogesh Sharma.*)

**Fonctionnalités de la documentation :**

- Ajout de la documentation dans le Guide utilisateur pour l'option `process-max`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.12 {#v112-release-notes}

*Pages Somme de contrôle, Configuration et corrections de bogues*

*Sortie le 12 décembre 2016*

**NOTE IMPORTANTE** : Dans les versions antérieures, il était possible de spécifier des options en ligne de commande qui étaient non valides pour la commande courante sans recevoir d'erreur. Une erreur sera désormais générée pour les options non valides, il est donc essentiel de vérifier soigneusement les options en ligne de commande dans votre environnement afin d'éviter toute interruption.

**Correctifs de bogues :**

- Corrigé un problème où des options non valides pour la commande spécifiée pouvaient être fournies en ligne de commande sans générer d'erreur. Ces options étaient ignorées et ne provoquaient aucun changement de comportement, mais pouvaient prêter à confusion. Les options non valides génèrent désormais une erreur. (*Signalement par Nikhilchandra Kulkarni.*)

- Corrigé un problème où les liens symboliques internes n'étaient pas créés pour les espaces de table dans le dépôt. Ce problème n'était apparent que lorsqu'on tentait de démarrer manuellement des clusters in situ à l'aide de captures instantanées du système de fichiers, et n'affectait pas les opérations normales de sauvegarde ou de restauration.

- Corrigé un problème qui empêchait l'affichage des erreurs sur la console avant l'initialisation du système de journalisation, c'est-à-dire pendant l'analyse des options. Les codes d'erreur étaient toujours renvoyés correctement, de sorte que cela n'aurait pas fait apparaître un processus comme ayant réussi alors qu'il avait échoué. (*Signalement par Adrian Vondendriesch.*)
- Corrigé un problème où l'option `db-port` spécifiée sur le serveur de sauvegarde n'était pas correctement transmise au serveur distant, sauf si elle provenait de la première base de données configurée. (*Signalement par Michael Vitale.*)

**Fonctionnalités :**

- Ajout de l'option `--checksum-page` permettant à pgBackRest de valider les sommes de contrôle des pages dans les fichiers de données lorsque les sommes de contrôle sont activées sur PostgreSQL >= 9.3. Notez que cette fonctionnalité nécessite une bibliothèque C qui peut ne pas être disponible initialement dans les paquets du système d'exploitation. L'option sera automatiquement activée lorsque la bibliothèque est présente et que les sommes de contrôle sont activées sur le cluster. (*Suggéré par Stephen Frost.*)

- Ajout de l'option `--repo-link` permettant de supprimer les liens symboliques internes lorsque le dépôt est situé sur un système de fichiers qui ne les supporte pas. Cette option n'affecte pas la fonctionnalité de pgBackRest, mais le lien de commodité `latest` ne sera pas créé, ni les liens symboliques internes des espaces de table, ce qui affectera la capacité à initialiser manuellement des clusters à partir de captures instantanées du système de fichiers.

- Ajout de l'option `--repo-sync` permettant de désactiver les synchronisations de répertoires dans le dépôt pour les systèmes de fichiers qui ne les supportent pas, par exemple NTFS.
- Ajouté une entrée de journal prédéfinie pour indiquer qu'une commande s'est terminée avec succès. Par exemple, une sauvegarde se termine avec succès avec : `INFO: backup command end: completed successfully`. (*Suggéré par Jens Wilke.*)

**Améliorations :**

- Pour simplifier, le fichier `pg_control` est désormais copié avec les autres fichiers, et non pas seul à la fin du processus. La commande `backup` n'exige pas ce comportement, et `restore` copie dans un fichier temporaire qui est renommé à la fin de la restauration.

**Correctifs de bogues dans la documentation :**

- Corrigé un problème qui masquait les exceptions lors de la génération des PDF.
- Corrigé une régression liée aux liens de section introduite dans la version 1.10.

**Fonctionnalités de la documentation :**

- Ajout de la rétention à la section QuickStart.


### Notes de version v1.11 {#v111-release-notes}

*Correction de bogue améliorant l'efficacité de l'archivage asynchrone*

*Sortie le 17 novembre 2016*

**Correctifs de bogues :**

- Corrigé un problème où l'archivage asynchrone transférait un fichier par exécution au lieu de transférer les fichiers par lots. Cette régression a été introduite dans la version 1.09 et n'a affecté que l'efficacité, tous les segments WAL ont été correctement archivés en mode asynchrone. (*Signalement par Stephen Frost.*)


### Notes de version v1.10 {#v110-release-notes}

*Création de stanza et corrections de petits bogues*

*Sortie le 8 novembre 2016*

**Correctifs de bogues :**

- Corriger un problème pouvant faire échouer une sauvegarde lorsqu'aucune modification n'avait été apportée à la base de données depuis la sauvegarde précédente et que seul `pg_control` avait changé.
- Corriger un problème où des chemins de tablespace partageant le même préfixe provoquaient une erreur de lien invalide. (*Signalement par Nikhilchandra Kulkarni.*)

**Fonctionnalités :**

- Ajouté la commande `stanza-create` pour formaliser la création de stanzas dans le dépôt. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations :**

- Supprimé les directives `use lib` superflues des modules Perl. (*Suggéré par Devrim Gündüz.*)


### Notes de version v1.09 {#v109-release-notes}

*9.6 Prise en charge, configurabilité et corrections de bogues*

*Sortie le 10 octobre 2016*

**Correctifs de bogues :**

- Corrigé la commande `check` afin d'éviter qu'un message d'erreur ne soit journalisé si le répertoire de sauvegarde n'existe pas. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Corrigé le message d'erreur pour qu'il affiche correctement la commande d'archive lorsqu'une commande d'archive invalide est détectée. (*Signalement par Jason O'Donnell.*)
- Corrigé un problème où l'archivage asynchrone n'était pas lancé si `archive-push` ne disposait pas de suffisamment d'espace pour mettre en file une nouvelle tranche WAL. Cela signifiait que la file n'était jamais vidée sans intervention manuelle (par exemple, en appelant `archive-push` directement). PostgreSQL affiche désormais des erreurs lorsque l'espace est insuffisant pour stocker de nouvelles tranches WAL, mais le processus asynchrone est toujours lancé afin que l'espace soit finalement libéré. (*Signalement par Jens Wilke.*)
- Corrigé un délai d'attente distant survenu lorsqu'un processus local générant des sommes de contrôle (lors d'une reprise ou d'une restauration) ne copiait pas de fichiers, permettant ainsi à la connexion distante de rester inactive. (*Signalement par Jens Wilke.*)

**Fonctionnalités :**

- Les sauvegardes non exclusives sont utilisées automatiquement sur PostgreSQL 9.6.
- Ajout de l'option `cmd-ssh` permettant de spécifier le client SSH. (*Suggéré par Jens Wilke.*)
- Ajout de l'option `log-level-stderr` pour contrôler si les messages de journalisation console sont envoyés à `stderr` ou à `stdout`. Par défaut, cette option est définie sur `warn`, ce qui constitue un changement de comportement par rapport aux versions précédentes, même si cela peut paraître plus intuitif. Définir `log-level-stderr=off` permet de préserver le comportement ancien. (*Suggéré par Sascha Biberhofer.*)
- Définir `application_name` sur `"pgBackRest [command]"` pour les connexions à la base de données. (*Suggéré par Jens Wilke.*)
- Vérifier que archive_mode est activé lorsque l'option `archive-check` est activée.

**Améliorations :**

- Message d'erreur clarifié lorsque l'acquisition du verrou d'advisory pgBackRest échoue, afin de préciser qu'il ne s'agit pas d'un verrou de sauvegarde PostgreSQL. (*Suggéré par Jens Wilke.*)
- Numéro de version de pgBackRest inclus dans la sortie INFO du journal de démarrage de la commande.
- Identifiant de processus (PID) inscrit dans les journaux INFO de démarrage/arrêt du processus local.

**Fonctionnalités de la documentation :**

- Ajout de la documentation de l'option `archive-timeout` dans le guide utilisateur. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.08 {#v108-release-notes}

*Correctifs de bogues et améliorations des journaux*

*Sortie le 14 septembre 2016*

**Correctifs de bogues :**

- Corrigé un problème où les processus locaux ne se déconnectaient pas une fois terminés et pouvaient ensuite expirer. (*Signalement par Todd Vernick.*)
- Corrigé un problème où la couche de protocole pouvait expirer en attendant l'arrivée des segments WAL dans l'archive. (*Signalement par Todd Vernick.*)

**Améliorations :**

- Mémorise la sortie du journal de fichier jusqu'à la création du fichier, afin de produire un journal plus complet.


### Notes de version v1.07 {#v107-release-notes}

*Thread de traitement : conversions et corrections de bogues*

*Sortie le 7 septembre 2016*

**Correctifs de bogues :**

- Corrigé un problème où les espaces de tables étaient copiés depuis le principal lors d'une sauvegarde en mode secondaire.
- Corrigé la commande `check` afin que les informations de sauvegarde soient vérifiées à distance et non seulement localement. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Corrigé un problème où `retention-archive` n'était pas automatiquement défini lorsque `retention-archive-type=diff`, entraînant une expiration de l'archive moins agressive que prévue. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)

**Fonctionnalités :**

- Converti les threads Perl en processus afin d'améliorer la compatibilité et les performances.
- Exclut le contenu du répertoire `$PGDATA/pg_replslot` afin que les slots de réplication sur le serveur principal ne fassent pas partie de la sauvegarde.
- Les paramètres `archive-start` et `archive-stop` sont désormais renseignés dans `backup.manifest` même lorsque `archive-check=n`. (*Suggéré par Jens Wilke.*)
- Avertissements supplémentaires lorsque les paramètres de rétention de l'archive pourraient ne pas avoir l'effet escompté ou permettre une rétention indéfinie. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Prise en charge expérimentale des sauvegardes non exclusives dans PostgreSQL 9.6 rc1. Les modifications apportées aux versions du contrôle/catalogue/WAL dans les versions candidates ultérieures pourraient rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.

**Correctifs de bogues dans la documentation :**

- Corrigé des problèmes mineurs de reproductibilité de la documentation liés aux chemins binaires.

**Fonctionnalités de la documentation :**

- Documentation relative à la rétention des archives. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.06 {#v106-release-notes}

*Sauvegarde depuis une instance de secours et corrections de bogues*

*Sortie le 25 août 2016*

**Correctifs de bogues :**

- Corrigé un problème où un lien de tablespace référençant un autre lien ne produisait pas d'erreur, mais sautait entièrement le tablespace. (*Signalement par Michael Vitale.*)

- Corrigé un problème où des options qui ne devaient pas autoriser de valeurs multiples pouvaient être spécifiées plusieurs fois dans `pgbackrest.conf` sans lever d'erreur. (*Signalement par Michael Vitale.*)

- Corrigé un problème où l'option `protocol-timeout` n'était pas automatiquement augmentée lorsque l'option `db-timeout` était augmentée. (*Signalement par Todd Vernick.*)

**Fonctionnalités :**

- Sauvegarder depuis un cluster standby. Une connexion au cluster primaire reste nécessaire pour démarrer ou arrêter la sauvegarde et copier les fichiers non répliqués, mais l'immense majorité des fichiers est copiée depuis le standby afin de réduire la charge du primaire.
- Assouplir la configuration des bases de données. Le primaire comme le standby peuvent être configurés sur le serveur de sauvegarde ; pgBackRest détermine automatiquement lequel est primaire. Avec un serveur de sauvegarde distinct, aucun changement de configuration n'est donc requis après un basculement du primaire vers le standby.
- Exclure pendant la sauvegarde les répertoires que PostgreSQL nettoie, recrée ou remet à zéro au démarrage. Cela comprend `pgsql_tmp` et `pg_stat_tmp`. Le fichier `postgresql.auto.conf.tmp` est désormais exclu, en plus de `backup_label.old`, `postmaster.opts`, `postmaster.pid`, `recovery.conf` et `recovery.done`.
- Prise en charge expérimentale des sauvegardes non exclusives dans PostgreSQL 9.6 beta4. Les modifications apportées aux versions du contrôle/catégorie/WAL dans les versions beta ultérieures peuvent entraîner une incompatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.

**Améliorations :**

- Améliorer le message d'erreur pour les liens référençant des liens dans la construction du manifeste.
- Ajouter des indications au message d'erreur lors de la détection de chemins relatifs dans `archive-push` ou `archive-get`.
- Améliorer les messages du journal de sauvegarde pour indiquer l'hôte d'où les fichiers sont copiés.


### Notes de version v1.05 {#v105-release-notes}

*Correction d'un bogue lié à la vérification des liens de tablespace*

*Sortie le 9 août 2016*

**Correctifs de bogues :**

- Corrigé un problème où les chemins de tablespace contenant $PGDATA comme sous-chaîne étaient identifiés comme des sous-répertoires de $PGDATA, même lorsqu'ils ne l'étaient pas. Renforcement légère du contrôle des chemins relatifs. (*Signalement par Chris Fort.*)

**Fonctionnalités de la documentation :**

- Ajout de la documentation sur la planification des sauvegardes avec cron. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

**Améliorations de la documentation :**

- Déplacé la liste d'attente depuis le site web de pgBackRest vers la documentation wiki du dépôt GitHub. (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.04 {#v104-release-notes}

*Divers correctifs de bogues*

*Sortie le 30 juillet 2016*

**Correctifs de bogues :**

- Corrigé un problème où une connexion distante superflue était créée, pouvant entraîner un délai d'attente ou un conflit de verrou pendant une sauvegarde/restauration multithreadées. (*Signalement par Michael Vitale.*)
- Corrigé un problème où le chemin de la base de données n'était pas requis pour la commande `check`, ce qui provoquait une assertion en cas de manque plutôt qu'un message d'erreur explicite. (*Signalement par Michael Vitale.*)
- Corrigé la commande `check` afin qu'elle lève une erreur lorsque la version ou l'identifiant de la base de données ne correspond pas à celle de l'archive. (*Corrigé par Cynthia Shang. Révisé par David Steele.*)
- Corrigé un problème où une connexion distante pouvait tenter de démarrer sa propre connexion distante lorsque l'option `backup-host` n'était pas présente dans `pgbackrest.conf` sur le serveur de base de données. (*Signalement par Lardière Sébastien.*)
- Corrigé un problème où le contenu du répertoire `pg_xlog` était sauvegardé lorsqu'il était un lien symbolique. Cela n'avait pas d'impact sur la restauration mais représentait un gaspillage d'espace.
- Corrigé un appel invalide à `log()` dans les routines de verrouillage.

**Fonctionnalités :**

- Prise en charge expérimentale des sauvegardes non exclusives dans PostgreSQL 9.6 beta3. Les modifications apportées aux versions du contrôle/catégorie/WAL dans les versions bêta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.

**Améliorations :**

- Supprime les bannières sur les connexions du protocole SSH.
- Messages d'erreur distants améliorés pour identifier l'hôte où l'erreur a été levée.
- Tous les types distants prennent désormais des verrous. Les exceptions datent de l'époque où le cadre de test et pgBackRest s'exécutaient dans la même machine virtuelle et ne s'appliquent plus.

**Fonctionnalités de la documentation :**

- Ajout d'une clarification sur la raison pour laquelle la valeur par défaut de l'option `backrest-user` est `backrest`. (*Suggéré par Michael Vitale.*)
- Mise à jour des informations concernant la disponibilité des paquets sur les plates-formes prises en charge. (*Suggéré par Michael Vitale.*)


### Notes de version v1.03 {#v103-release-notes}

*Commande de vérification et corrections de bogues*

*Sortie le 2 juillet 2016*

**Correctifs de bogues :**

- Corrigé un problème où `keep-alives` pouvait être bloqué par de nombreux petits fichiers lors d'une `backup` multithreadée. Elles étaient également complètement absentes lors de la reprise de `backup` en mode simple ou multithreadé et du contrôle `restore` des sommes de contrôle. (*Signalement par Janice Parkinson, Chris Barber.*)

- Corrigé un problème où la commande `expire` refusait de s'exécuter lorsqu'elle était appelée explicitement en ligne de commande si l'option `db-host` était définie. Ce problème ne se produisait pas lorsque `expire` était exécuté automatiquement après un `backup` (*Signalement par Chris Barber.*)

- Corrigé un problème où la validation était exécutée sur archive_command même lorsque l'option `archive-check` était désactivée.

**Fonctionnalités :**

- Ajout de la commande `check` pour valider que pgBackRest est correctement configuré pour l'archivage et les sauvegardes. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Ajout de l'option `protocol-timeout`. Précédemment, `protocol-timeout` était défini comme `db-timeout` + 30 secondes.
- Une erreur de fermeture des hôtes distants à la fin de la sauvegarde ne provoque plus d'exception. Un avertissement est désormais généré, recommandant d'augmenter `protocol-timeout`.
- Prise en charge expérimentale des sauvegardes non exclusives dans PostgreSQL 9.6 beta2. Les modifications apportées aux versions du contrôle/catalogue/WAL dans les versions bêta suivantes peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.

**Améliorations :**

- Amélioration de la gestion des utilisateurs/groupes capturés lors de la sauvegarde et qui n'existent pas sur l'hôte de restauration. Gestion explicite du cas où l'utilisateur/groupe n'est pas mappé à un nom.

- La gestion des options est désormais bien plus stricte. Il était auparavant possible qu'une commande utilise une option non explicitement attribuée à celle-ci. Cela était particulièrement vrai pour les options `backup-host` et `db-host`, utilisées pour déterminer la localité.

**Améliorations de la documentation :**

- Autorise l'utilisation d'une date statique pour la documentation afin de générer des builds reproductibles. (*Suggéré par Adrian Vondendriesch.*)
- Ajout de la documentation sur l'archivage asynchrone dans le guide utilisateur. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Le lieu d'installation recommandé pour les modules pgBackRest est désormais `/usr/share/perl5` car `/usr/lib/perl5` a été retiré de la chaîne de recherche dans les versions plus récentes de Perl.
- Ajout des instructions pour supprimer les versions antérieures de pgBackRest.


### Notes de version v1.02 {#v102-release-notes}

*Correction de bogue pour Perl 5.22*

*Sortie le 2 juin 2016*

**Correctifs de bogues :**

- Correction de l'utilisation de sprintf() en raison de nouvelles contraintes dans Perl 5.22. Les paramètres non référencés dans la chaîne de format ne sont plus autorisés. (*Corrigé par Adrian Vondendriesch. Révisé par David Steele.*)

**Correctifs de bogues dans la documentation :**

- Corrigé une syntaxe incorrecte incompatible avec Perl 5.2X. (*Corrigé par Christoph Berg, Adrian Vondendriesch. Révisé par David Steele.*)
- Corrigé les chemins absolus utilisés pour le logo PDF. (*Signalement par Adrian Vondendriesch.*)

**Fonctionnalités de la documentation :**

- Les notes de version sont désormais divisées en sections afin de distinguer clairement les bogues, les fonctionnalités et les révisions. Une section « Notes supplémentaires » a été ajoutée pour les modifications apportées à la documentation et à la suite de tests qui n'affectent pas le code central.
- Génération de la page de manuel ajoutée. (*Contribution de Adrian Vondendriesch, David Steele.*)
- Le journal des modifications était la dernière pièce de documentation à être rendue uniquement en Markdown. Un convertisseur a été écrit afin que le document puisse être généré par les rendus standards. Le journal des modifications sera désormais disponible sur le site web et a été renommé « Versions ». (*Contribution de Cynthia Shang. Révisé par David Steele.*)


### Notes de version v1.01 {#v101-release-notes}

*Informations améliorées, restauration sélective et prise en charge de la version 9.6*

*Sortie le 17 mai 2016*

**Fonctionnalités :**

- Sortie texte améliorée de la commande `info` incluant des horodatages, des tailles et la liste de référence de toutes les sauvegardes. (*Contribution de Cynthia Shang. Révisé par David Steele.*)
- Permet la restauration sélective de bases de données à partir d'une sauvegarde de cluster. Cette fonctionnalité peut entraîner des économies importantes d'espace et de temps lorsque seules certaines bases de données sont restaurées. Les bases de données non restaurées ne seront pas accessibles, mais doivent être supprimées manuellement avant de pouvoir être supprimées du catalogue partagé. (*Révisé par Cynthia Shang, Greg Smith, Stephen Frost. Suggéré par Stephen Frost.*)
- Prise en charge expérimentale des sauvegardes non exclusives dans PostgreSQL 9.6 beta1. Les modifications apportées aux versions du contrôle/catalogue/WAL dans les versions bêta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution. (*Révisé par Cynthia Shang.*)


### Notes de version v1.00 {#v100-release-notes}

*Nouveau format de dépôt et schéma de configuration, prise en charge des liens*

*Sortie le 14 avril 2016*

**AVERTISSEMENT IMPORTANT** : Cette version de jour de rupture rompt la compatibilité avec les versions antérieures de pgBackRest. Le format du manifeste, la structure sur disque, le schéma de configuration et les noms d'exécutables/chemins ont tous été modifiés. Vous devez créer un nouveau dépôt pour stocker les sauvegardes de cette version de pgBackRest et conserver votre ancien dépôt pendant un certain temps au cas où vous devriez effectuer une restauration. Les restaurations à partir de l'ancien dépôt nécessiteront la version antérieure de pgBackRest, mais en raison des changements de nom, il est possible d'avoir `1.00` et une version antérieure de pgBackRest installées en même temps. Consultez les notes ci-dessous pour plus de détails sur les modifications apportées.

**Fonctionnalités :**

- Implémenté un nouveau schéma de configuration qui devrait être bien plus simple à utiliser. Consultez le Guide utilisateur et la Référence de configuration pour plus de détails, mais pour une configuration simple, toutes les options peuvent désormais être placées dans la section `stanza`. Les options communes à plusieurs stanzas peuvent être placées dans la section `[global]`. Les configurations plus complexes peuvent toujours utiliser des sections de commande, bien que ce cas d'usage soit désormais rare. (*Suggéré par Michael Renner.*)

- L'option `repo-path` fait désormais toujours référence au dépôt où sont stockées les sauvegardes et les archives, qu'elles soient locales ou distantes, de sorte que l'option `repo-remote-path` a été supprimée. La nouvelle option `spool-path` peut être utilisée pour définir un emplacement de mise en file d'attente des segments WAL lors de l'archivage asynchrone. Un dépôt local n'est plus obligatoire.
- Le nom de fichier de configuration par défaut est désormais `pgbackrest.conf` au lieu de `pg_backrest.conf`. Cette modification a été effectuée pour assurer une cohérence avec d'autres changements de nommage, mais aussi pour éviter que des fichiers de configuration anciens ne soient chargés accidentellement lors de la migration vers `1.00`. (*Suggéré par Michael Renner, Stephen Frost.*)
- Le nom de dépôt par défaut a été modifié de `/var/lib/backup` à `/var/lib/pgbackrest`. (*Suggéré par Michael Renner, Stephen Frost.*)
- Les fichiers de verrouillage sont désormais stockés par défaut dans `/tmp/pgbackrest`. À l’heure actuelle, `/run/pgbackrest` est l'emplacement recommandé, mais cela nécessiterait des scripts d’initialisation qui ne font pas partie de cette version. L’option `lock-path` peut être utilisée pour configurer le répertoire de verrouillage.
- Les fichiers de journalisation sont désormais stockés par défaut dans `/var/log/pgbackrest` et ne comportent plus la date en suffixe, afin de pouvoir être gérés avec `logrotate`. L’option `log-path` peut être utilisée pour configurer le répertoire de journalisation. (*Suggéré par Stephen Frost.*)
- Nom du fichier exécutable passé de `pg_backrest` à `pgbackrest`. (*Suggéré par Michael Renner, Stephen Frost.*)
- Tous les fichiers et répertoires liés à PGDATA sont désormais inclus dans la sauvegarde. Par défaut, les liens seront restaurés directement dans PGDATA en tant que fichiers ou répertoires. L'option `--link-all` peut être utilisée pour restaurer tous les liens à leurs emplacements d'origine. L'option `--link-map` peut être utilisée pour rediriger un lien vers un nouvel emplacement.
- Option `--tablespace` supprimée et remplacée par l'option `--tablespace-map-all`, qui indique plus clairement sa fonction.
- Niveau de journalisation `detail` ajouté, qui fournit plus d'informations que `info` sans être aussi verbeux que `debug`.


--------

## Versions pré-stables {#pre-stable-releases}


### Notes de version v0.92 {#v092-release-notes}

*Correction du chemin du dépôt en ligne de commande*

*Sortie le 6 avril 2016*

**Correctifs de bogues :**

- Corrigé un problème où le processus principal transmettait `--repo-remote-path` au lieu de `--repo-path` au dépôt distant, entraînant la création des fichiers de verrouillage dans le répertoire par défaut du dépôt (`/var/lib/backup`), ce qui entraînait généralement un échec. Ce problème ne se produisait que lorsque `--repo-remote-path` était défini en ligne de commande plutôt que dans `pg_backrest.conf`. (*Signalement par Jan Wieck.*)


### Notes de version v0.91 {#v091-release-notes}

*Correction de bogue liée aux espaces de table et améliorations mineures*

*Sortie le 22 mars 2016*

**CORRECTION D'URGENCE POUR LES ESPACES DE TABLE** : Une modification du format du dépôt a été accidentellement introduite dans la version 0.90, ce qui signifiait que la sauvegarde sur disque n’était plus un cluster PostgreSQL valide lorsque la sauvegarde contenait des espaces de table. Cela n’affectait que les utilisateurs qui ont copié directement les sauvegardes pour restaurer des clusters PostgreSQL au lieu d’utiliser la commande de restauration. Toutefois, la correction rompt la compatibilité avec les anciennes sauvegardes contenant des espaces de table, quelle que soit la méthode de restauration (pgBackRest lèvera des erreurs et refusera la restauration). De nouvelles sauvegardes complètes doivent être effectuées immédiatement après l’installation de la version 0.91 pour tous les clusters contenant des espaces de table. Si des sauvegardes anciennes doivent être restaurées, utilisez une version de pgBackRest correspondant à la version de la sauvegarde.

**Correctifs de bogues :**

- Correctif apporté à une incompatibilité du dépôt introduite avec pgBackRest 0.90. (*Signalement par Evan Benoit.*)

**Fonctionnalités :**

- Copiez `global/pg_control` dernier pendant les sauvegardes.
- Écrivez les fichiers `.info` et `.manifest` dans un répertoire temporaire avant de les déplacer vers leurs emplacements finaux et de les synchroniser sur le disque.
- Renommez l'option `--no-start-stop` en `--no-online`.

**Fonctionnalités du jeu de tests :**

- Analyse statique de code à l'aide de Perl-Critic, actuellement réussie en mode doux.


### Notes de version v0.90 {#v090-release-notes}

*9.5 Prise en charge, diverses améliorations et corrections de bogues mineures*

*Sortie le 7 février 2016*

**Correctifs de bogues :**

- Corrigé un problème où la spécification de `--no-archive-check` provoquait une erreur de configuration. (*Signalement par Jason O'Donnell.*)

- Corrigé un problème où un fichier WAL temporaire laissé après un crash système bien synchronisé pouvait faire échouer le prochain `archive-push`.

- L'option `retention-archive` peut désormais être définie en toute sécurité à une valeur inférieure à la rétention des sauvegardes (`retention-full` ou `retention-diff`) sans avoir à spécifier `archive-copy=n`. Le WAL nécessaire pour rendre les sauvegardes situées en dehors de la rétention d'archive cohérentes sera conservé dans l'archive. Toutefois, dans ce cas, la récupération à un point précis (PITR) ne sera pas possible pour les sauvegardes situées en dehors de la rétention d'archive.

**Fonctionnalités :**

- Lors de la sauvegarde et de la restauration des espaces de tables, pgBackRest ne traite que le sous-répertoire créé pour la version de PostgreSQL utilisée. Étant donné qu'une même tablespace peut contenir plusieurs versions (notamment lors d'une mise à jour binaire), cela empêche de copier trop de fichiers lors d'une sauvegarde et d'effacer accidentellement d'autres versions lors d'une restauration. Cette règle s'applique uniquement aux versions de PostgreSQL >= 9.0 — les versions antérieures ne pouvaient pas partager un répertoire d'espace de tables.

- Génère une erreur lorsque `archive-check=y` est présent mais que `archive_command` n'exécute pas `pg_backrest`. (*Contribution de Jason O'Donnell. Révisé par David Steele.*)

- Amélioration du message d'erreur lorsque `repo-path` ou `repo-remote-path` n'existe pas.
- Ajout de vérifications pour les options de restauration `--delta` et `--force` afin de s'assurer que le destinataire est un répertoire $PGDATA valide. pgBackRest vérifiera la présence de `PG_VERSION` ou de `backup.manifest` (restes d'une restauration interrompue). Si aucun de ces fichiers n'est trouvé, `--delta` et `--force` seront désactivés, mais la restauration se poursuivra à moins qu'il n'y ait des fichiers dans le répertoire $PGDATA (ou dans les répertoires de tablespace), auquel cas l'opération sera interrompue.

- Lorsqu'on restaure `--set=latest` (valeur par défaut), la sauvegarde réellement restaurée sera affichée dans le journal.

- Prise en charge des segments partiels WAL de PostgreSQL 9.5 et du paramètre `recovery_target_action`. Le paramètre `archive_mode = 'always'` n'est pas encore pris en charge.

- Prise en charge du paramètre de récupération `recovery_target = 'immediate'` introduit dans PostgreSQL 9.4.

- Les vérifications suivantes relatives aux tablespaces ont été ajoutées : chemins ou fichiers dans pg_tblspc, liens relatifs dans pg_tblspc, tablespaces dans $PGDATA. Les trois cas généreront des erreurs.


### Notes de version v0.89 {#v089-release-notes}

*Correction d'un bogue de délai d'attente et prise en charge des dépôts en lecture seule lors de la restauration*

*Sortie le 24 décembre 2015*

**Correctifs de bogues :**

- Corrigé un problème où les sauvegardes/restaurations plus longues entraînaient une expiration du délai lorsqu'elles étaient distantes et multithreadées. Des messages d'activité sont désormais utilisés pour s'assurer que la connexion distante du processus principal n'expire pas pendant que les threads distants effectuent tout le travail. Le message d'erreur lié aux délais d'expiration a également été amélioré afin de faciliter le débogage. (*Signalement par Stephen Frost.*)

**Fonctionnalités :**

-  Autorise les restaurations sur un dépôt en lecture seule en utilisant `--no-lock` et `--log-level-file=off`. L'option `--no-lock` ne peut être utilisée qu'avec les restaurations.


### Notes de version v0.88 {#v088-release-notes}

*Documentation et corrections de bogues mineures*

*Sortie le 22 novembre 2015*

**Correctifs de bogues :**

- Corrigé un problème où les commandes `start`/`stop` exigeaient l'option `--config`. (*Signalement par Dmitry Didovicher.*)
- Corrigé un problème où les fichiers de journalisation étaient écrasés au lieu d’être ajoutés. (*Signalement par Stephen Frost, Dmitry Didovicher.*)
- Corrigé un problème où `backup-user` n’était pas facultatif.

**Fonctionnalités :**

- Les liens symboliques ne sont plus créés dans les répertoires de sauvegarde du dépôt. Ces liens symboliques pouvaient pointer vers n'importe quelle localisation et présenter potentiellement un risque. Les liens symboliques sont toujours régénérés lors d'une restauration. (*Suggéré par Stephen Frost.*)

- Amélioration du message lors de l'expiration d'une sauvegarde. L'expiration des sauvegardes complètes et différentielles est journalisée sur une seule ligne, accompagnée d'une liste de toutes les sauvegardes dépendantes expirées.

- La rétention des archives est automatiquement définie sur la rétention des sauvegardes complètes si elle n'est pas configurée explicitement.

**Fonctionnalités de la documentation :**

- Ajout de la documentation dans le guide utilisateur pour les restaurations delta, l'expiration, les hôtes de sauvegarde dédiés, le démarrage et l'arrêt de pgBackRest, ainsi que la réplication.


### Notes de version v0.87 {#v087-release-notes}

*Site web et guide utilisateur*

*Sortie le 28 octobre 2015*

**Fonctionnalités :**

- Les fichiers `backup_label.old` et `recovery.done` sont désormais exclus des sauvegardes.

**Fonctionnalités de la documentation :**

- Ajout d'un nouveau guide utilisateur couvrant les bases de pgBackRest ainsi que certains sujets avancés, notamment la récupération à un instant donné (PITR). Beaucoup d'autres contenus à venir, mais c'est un bon départ. (*Contribution de David Steele, Stephen Frost. Révisé par Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher.*)


### Notes de version v0.85 {#v085-release-notes}

*Commandes de démarrage/arrêt et corrections de petits bogues*

*Sortie le 8 octobre 2015*

**Correctifs de bogues :**

- Corrigé un problème où une erreur pouvait être renvoyée après une sauvegarde ou une restauration ayant complètement réussi.
- Corrigé un problème où une reprise échouait si des fichiers temporaires étaient présents dans le répertoire racine de la sauvegarde lorsqu'une sauvegarde échouait. Ce scénario était probable si le processus de sauvegarde était interrompu pendant la phase de copie.

**Fonctionnalités :**

-  Ajout des commandes `stop` et `start` afin d'empêcher les processus pgBackRest de s'exécuter sur un système où PostgreSQL est arrêté ou où le système doit être mis en veille pour une autre raison.
-  Prise en charge expérimentale de PostgreSQL 9.5 beta1. Cette fonctionnalité peut être rompue si la version de contrôle ou la magie des WAL change dans des versions ultérieures, mais elle sera mise à jour à chaque version de pgBackRest pour suivre l'évolution. Tous les tests de régression passent, sauf les tests `--target-resume` (cette fonctionnalité a été modifiée dans la version 9.5) et aucune vérification n'a encore été effectuée pour les segments WAL `.partial`.


### Notes de version v0.82 {#v082-release-notes}

*Refactorisation, aide en ligne de commande et corrections de bogues mineures*

*Sortie le 14 septembre 2015*

**Correctifs de bogues :**

- Corrigé un problème où les sauvegardes compressées reprises ne conservaient pas les fichiers existants.
- Corrigé un problème où la reprise et les sauvegardes incrémentielles/différentielles ne garantissaient pas que la sauvegarde précédente avait les mêmes paramètres de compression et de liens durs.
- Corrigé un problème où une sauvegarde froide utilisant `--no-start-stop` pouvait être lancée sur un cluster PostgreSQL en cours d'exécution sans que `--force` soit spécifié.
- Corrigé un problème où un thread pouvait être lancé même lorsque aucun thread n'avait été demandé.
- Corrigé un problème où le numéro de version de pgBackRest n'était pas mis à jour dans `backup.info` et `archive.info` après une mise à jour ou une rétrogradation.
- Corrigé un problème où la commande `info` lançait une exception lorsque le dépôt ne contenait aucun stanza. (*Signalement par Stephen Frost.*)
- Corrigé un problème où les avertissements PostgreSQL `pg_stop_backup()` étaient envoyés vers `stderr`. (*Signalement par Stephen Frost.*)

**Fonctionnalités :**

- Prise en charge expérimentale de PostgreSQL 9.5 alpha2. Cette fonctionnalité peut cesser de fonctionner si la version de contrôle ou la magie WAL change dans les versions futures, mais elle sera mise à jour à chaque version de pgBackRest pour suivre l'évolution. Tous les tests de régression passent, sauf les tests `--target-resume` (cette fonctionnalité a évolué en 9.5) et aucune vérification n'a encore été effectuée sur les segments WAL `.partial`.

**Améliorations :**

- Option et section renommées `recovery-setting` en `recovery-option` afin d’être plus cohérentes avec les conventions de nommage de pgBackRest.
- Chargement dynamique des modules ajouté afin d’accélérer les commandes, notamment l’archivage asynchrone.

**Fonctionnalités de la documentation :**

- Aide en ligne de commande extraite désormais à partir de la même source XML utilisée pour les autres documents et inclut bien plus de détails.


### Notes de version v0.80 {#v080-release-notes}

*Fonctionnalités de prise en charge, de stabilité et de commodité pour DBI*

*Sortie le 9 août 2015*

**Correctifs de bogues :**

- Corrigé un problème qui faisait que l'horodatage formaté des sauvegardes la plus ancienne et la plus récente était rapporté comme étant l'instant actuel par la commande `info`. Seule la sortie `text` était affectée — la sortie `json` rapportait les valeurs d'époque correctes. (*Signalement par Michael Renner.*)
- Corrigé un problème de protocole empêchant la journalisation des erreurs SSH (notamment lors de la connexion).

**Fonctionnalités :**

- Le dépôt est désormais créé et mis à jour avec des modes de répertoires et de fichiers cohérents. Par défaut, `umask` est défini sur `0000`, mais cette option peut être désactivée à l'aide du paramètre `neutral-umask`. (*Suggéré par Cynthia Shang.*)
- Ajout de l'option `stop-auto` permettant d'arrêter automatiquement les sauvegardes échouées lorsqu'une nouvelle sauvegarde démarre.
- Ajout de l'option `db-timeout` pour limiter le temps d'attente que pgBackRest attendra que `pg_start_backup()` et `pg_stop_backup()` retournent.
- Suppression du fichier `pg_control` au début de la restauration et copie du fichier à la fin. Cela empêche toute possibilité de démarrer une restauration partielle par PostgreSQL.
- Ajout de vérifications pour s'assurer que le paramètre `db-path` est cohérent avec `db-port` en comparant le `data_directory` rapporté par le cluster au paramètre `db-path` et la version rapportée par le cluster à la valeur lue depuis `pg_control`. Le paramètre `db-socket-path` est vérifié afin de s'assurer qu'il s'agit d'un chemin absolu.
- Prise en charge expérimentale de PostgreSQL 9.5 alpha1. Cette fonctionnalité peut cesser de fonctionner si la version de contrôle ou la magie WAL change dans les versions futures, mais elle sera mise à jour à chaque version de pgBackRest pour suivre l'évolution. Tous les tests de régression passent, sauf les tests `--target-resume` (cette fonctionnalité a évolué en 9.5) et aucune vérification n'a encore été effectuée sur les segments WAL `.partial`.

**Améliorations :**

- Utilisation désormais de Perl `DBI` et `DBD::Pg` pour les connexions à PostgreSQL au lieu de `psql`. Les paramètres `cmd-psql` et `cmd-psql-option` ont été supprimés et remplacés par `db-port` et `db-socket-path`. Suivez les instructions du Guide d'installation pour installer `DBD::Pg` sur votre système d'exploitation.

**Fonctionnalités du jeu de tests :**

- Ajout des configurations de test Vagrant pour Ubuntu 14.04 et CentOS 7.


### Notes de version v0.78 {#v078-release-notes}

*Supprimer les dépendances CPAN, améliorations de stabilité*

*Sortie le 13 juillet 2015*

**Améliorations :**

- Suppression de la dépendance aux paquets CPAN pour l'exécution multithreadée. Bien qu'il puisse être pertinent de mettre à jour les paquets `threads` et `Thread::Queue`, cela n'est plus nécessaire.
- Modification du délai d'attente pour utiliser une suite de Fibonacci au lieu d'une suite géométrique. Cela fait croître le délai d'attente de manière moins agressive tout en conservant des valeurs raisonnables.

**Fonctionnalités du jeu de tests :**

- Ajout des configurations de test Vagrant pour Ubuntu 12.04 et CentOS 6.


### Notes de version v0.77 {#v077-release-notes}

*Prise en charge de CentOS/RHEL 6 et améliorations de protocole*

*Sortie le 30 juin 2015*

**Fonctionnalités :**

- Ajout de synchronisations de fichiers et de répertoires à l'objet `File` pour une sécurité accrue lors de la sauvegarde/restauration et de l'archivage. (*Suggéré par Andres Freund.*)
- Ajout du support pour Perl 5.10.1 et OpenSSH 5.3, qui sont par défaut sur CentOS/RHEL 6. (*Suggéré par Eric Radman.*)
- Amélioration du message d'erreur lorsqu'une sauvegarde est exécutée sans que `archive_command` soit défini et sans que `--no-archive-check` soit précisé. (*Suggéré par Eric Radman.*)


### Notes de version v0.75 {#v075-release-notes}

*Nouveau format de dépôt, commande info et prise en charge expérimentale de la version 9.5*

*Sortie le 14 juin 2015*

**AVERTISSEMENT IMPORTANT** : Cette version de jour de flag rompt la compatibilité avec les versions antérieures de pgBackRest. Le format du manifeste, la structure sur disque et les noms binaires ont tous changé. Vous devez créer un nouveau dépôt pour stocker les sauvegardes de cette version de pgBackRest et conserver votre ancien dépôt pendant un certain temps au cas où vous devriez effectuer une restauration. Le fichier `pg_backrest.conf` n’a pas changé, mais vous devrez modifier toute référence à `pg_backrest.pl` dans cron (ou ailleurs) en `pg_backrest` (sans l’extension `.pl`).

**Fonctionnalités :**

- Ajouté la commande `info`.
- La journalisation utilise désormais une sortie non tamponnée. Cela devrait rendre les fichiers journaux écrits par plusieurs threads moins chaotiques. (*Suggéré par Michael Renner.*)
- Prise en charge expérimentale de PostgreSQL 9.5. Cette fonctionnalité peut cesser de fonctionner si la version de contrôle ou la magie WAL change, mais sera mise à jour à chaque version.

**Améliorations :**

- Ordre de fichiers plus efficace pour `backup`. Les fichiers sont copiés dans l'ordre décroissant de taille, afin qu'un seul thread ne se retrouve pas à copier un grand fichier à la fin. Cette optimisation était déjà mise en œuvre pour `restore`.


### Notes de version v0.70 {#v070-release-notes}

*Améliorations de la stabilité pour l'archivage, journalisation améliorée et aide*

*Sortie le 1er juin 2015*

**Correctifs de bogues :**

- Corrigé un problème où `archive-copy` échouait lors d'une sauvegarde incrémentielle ou différentielle lorsque `hardlink=n`. Dans ce cas, le chemin `pg_xlog` n'existe pas encore et doit être créé. (*Signalement par Michael Renner.*)

- Corrigé un problème dans l'archivage asynchrone où `archive-push` ne renvoyait pas correctement 0 lorsque `archive-max-mb` était atteint, et déplacé la vérification asynchrone après le transfert afin d'éviter de supprimer le fichier d'arrêt deux fois. Des tests unitaires ont également été ajoutés pour ce cas, et les messages d'erreur ont été améliorés pour mieux indiquer à l'utilisateur ce qui s'est produit. (*Signalement par Michael Renner.*)

- Corrigé un problème de verrouillage pouvant permettre plusieurs opérations du même type contre une même stanza. Ce problème semblait sans incidence sur l'intégrité des données, mais pouvait provoquer des erreurs inutiles lors de l'archivage et entraîner des erreurs lors de la sauvegarde ou de la restauration. (*Signalement par Michael Renner.*)

**Fonctionnalités :**

- Autoriser la sauvegarde de segments WAL en double lorsque la somme de contrôle correspond. Cela est nécessaire pour certains scénarios de récupération.
- Autoriser les commentaires/désactivations dans `pg_backrest.conf` à l’aide du caractère `#`. Seuls les caractères `#` situés en première position de la ligne sont pris en compte. (*Suggéré par Michael Renner.*)
- Amélioration de la journalisation avant `pg_start_backup()` afin de préciser clairement quand la sauvegarde attend un point de contrôle. (*Suggéré par Michael Renner.*)
- Diverses corrections de comportement des commandes et de la journalisation. (*Révisé par Michael Renner. Suggéré par Michael Renner.*)

**Améliorations :**

- Remplacé le module `JSON` par `JSON::PP`, qui est fourni avec Perl de base.

**Correctifs de bogues dans la documentation :**

- Divers correctifs apportés à l'aide. (*Révisé par Michael Renner. Signalement par Michael Renner.*)


### Notes de version v0.65 {#v065-release-notes}

*Amélioration de la journalisation de la reprise et de la restauration, restaurations compactes*

*Sortie le 11 mai 2015*

**Correctifs de bogues :**

- Corrigé un problème où un chemin absolu n'était pas écrit dans `recovery.conf` lorsque la restauration était exécutée avec un chemin relatif.

**Fonctionnalités :**

- Meilleur support de la reprise. Les fichiers repris sont vérifiés afin de s'assurer qu'ils n'ont pas été modifiés et le manifeste est enregistré plus fréquemment afin de préserver les sommes de contrôle au fur et à mesure que la sauvegarde progresse. Plus de tests unitaires pour vérifier chaque cas de reprise.

- La reprise est désormais facultative. Utilisez le paramètre `resume` ou `--no-resume` en ligne de commande pour la désactiver.

- Messages d'information supplémentaires pendant la restauration. Auparavant, la plupart des messages de restauration étaient au niveau débogage, si bien qu'il n'y avait pas beaucoup de sortie dans le journal.

- Ajout du paramètre `tablespace` permettant de restaurer les espaces de table dans le chemin `pg_tblspc`. Cela permet des restaurations compactes, pratiques pour le développement, les environnements de préproduction, etc. Actuellement, ces restaurations ne peuvent pas être sauvegardées, car pgBackRest s'attend à ce que seules des liaisons soient présentes dans le chemin `pg_tblspc`.


### Notes de version v0.61 {#v061-release-notes}

*Correction d'un bogue lié à une destination distante non compressée*

*Sortie le 21 avril 2015*

**Correctifs de bogues :**

- Corrigé une erreur de tamponnage pouvant survenir sur de grands fichiers fortement compressibles lors de la copie vers une destination distante non compressée. L'erreur a été détectée dans le code de décompression et entraînait un échec de la sauvegarde plutôt qu'une corruption, elle ne devrait donc pas affecter les sauvegardes réussies effectuées avec les versions précédentes.


### Notes de version v0.60 {#v060-release-notes}

*Prise en charge améliorée des versions et améliorations du WAL*

*Sortie le 19 avril 2015*

**Correctifs de bogues :**

- L’envoi de WAL en double génère désormais une erreur. Cela fonctionnait auparavant uniquement si les sommes de contrôle étaient désactivées.

**Fonctionnalités :**

- Les identifiants du système de base de données sont utilisés pour s'assurer que toutes les traces WAL archivées correspondent entre elles. Cela devrait aider à prévenir les mauvaises configurations qui enverraient des traces WAL provenant de plusieurs clusters vers le même archivage.

**Fonctionnalités du jeu de tests :**

- Tests de régression fonctionnels à partir de PostgreSQL 8.3.


### Notes de version v0.50 {#v050-release-notes}

*Restauration et bien plus*

*Sortie le 25 mars 2015*

**Correctifs de bogues :**

- Corrigé les sommes de contrôle endommagées, qui fonctionnent désormais avec les sauvegardes normales et reprises. Enfin compris que les sommes de contrôle et les deltas de sommes de contrôle devraient être fonctionnellement séparés, ce qui a simplifié plusieurs aspects. L'incident #28 a été créé pour les deltas de sommes de contrôle.
- Corrigé un problème où une sauvegarde pouvait être reprise à partir d'une sauvegarde interrompue qui n'avait pas le même type ni la même sauvegarde précédente.

**Fonctionnalités :**

- Ajout de la fonctionnalité de restauration.
- Toutes les options peuvent désormais être définies en ligne de commande, rendant `pg_backrest.conf` facultatif.
- La compression/décompression est désormais effectuée sans threads et la somme de contrôle/taille est calculée en flux. Cela signifie que les sommes de contrôle de fichier ne sont plus facultatives.
- Ajout de l'option `--no-start-stop` pour autoriser les sauvegardes lorsque Postgres est arrêté. Si `postmaster.pid` est présent, `--force` est requis pour exécuter la sauvegarde (bien qu'une sauvegarde incohérente soit probablement créée si Postgres est en cours d'exécution). Cette option a été ajoutée principalement à des fins de tests unitaires, mais elle pourrait avoir des applications dans des environnements réels.
- Somme de contrôle pour `backup.manifest` afin de détecter un manifeste corrompu ou modifié.
- Le lien `latest` pointe toujours vers la dernière sauvegarde. Cette fonctionnalité a été ajoutée pour plus de commodité et pour simplifier les restaurations.

**Fonctionnalités du jeu de tests :**

- Tests unitaires plus complets dans toutes les zones.


### Notes de version v0.30 {#v030-release-notes}

*Restructuration centrale et tests unitaires*

*Sortie le 5 octobre 2014*

**Fonctionnalités de la documentation :**

- Ajout de documentation très utile

**Fonctionnalités du jeu de tests :**

- Des tests unitaires assez complets pour toutes les opérations de base. Des travaux supplémentaires restent à accomplir ici, bien sûr, mais il reste toujours plus de travail à faire sur les tests unitaires.


### Notes de version v0.19 {#v019-release-notes}

*Amélioration du rapport/dépistage des erreurs*

*Sortie le 13 mai 2014*

**Correctifs de bogues :**

- Détection et correction d'un bogue grave où `file_copy()` était par défaut configuré pour ignorer les erreurs. Un autre problème dans `file_exists()` provoquait l'échec du test lorsque le fichier existait effectivement. Ensemble, ils auraient pu entraîner une sauvegarde corrompue sans aucune erreur, bien que cela soit très improbable.


### Notes de version v0.18 {#v018-release-notes}

*Retourner une erreur douce lorsque l’archive est manquante*

*Sortie le 13 avril 2014*

**Correctifs de bogues :**

- La commande `archive-get` retourne désormais 1 lorsque le fichier d'archive est manquant, afin de le distinguer des erreurs graves (échec de connexion SSH, erreur de copie de fichier, etc.). Cela permet à PostgreSQL de savoir que le flux d'archive s'est terminé normalement. Toutefois, cela ne tient pas compte des éventuelles lacunes dans le flux d'archive. (*Signalement par Stephen Frost.*)


### Notes de version v0.17 {#v017-release-notes}

*Avertir lorsque les répertoires d'archive ne peuvent pas être supprimés*

*Sortie le 3 avril 2014*

**Correctifs de bogues :**

- Si un répertoire d'archive qui devrait être vide n'a pas pu être supprimé, backrest lançait une erreur. Une correction définitive est en cours, mais pour l'instant, cela a été changé en avertissement afin que le traitement puisse continuer. Cela affectait les sauvegardes, car parfois le fichier d'archive final n'était pas envoyé si le premier fichier d'archive se trouvait dans un répertoire différent (plus un peu de malchance).


### Notes de version v0.16 {#v016-release-notes}

*RequestTTY=yes pour les sessions SSH*

*Sortie le 1er avril 2014*

**Correctifs de bogues :**

- Ajouté `RequestTTY=yes` aux sessions SSH. Espérons que cela empêchera les blocages aléatoires.


### Notes de version v0.15 {#v015-release-notes}

*Ajouté archive-get*

*Sortie le 29 mars 2014*

**Fonctionnalités :**

- Ajout de la fonctionnalité `archive-get` pour faciliter les restaurations.
- Ajout de l'option permettant de forcer un point de contrôle au démarrage de la sauvegarde, `start-fast=y`.


### Notes de version v0.11 {#v011-release-notes}

*Correctifs mineurs*

*Sortie le 26 mars 2014*

**Correctifs de bogues :**

- Supprimé l'option `master_stderr_discard` sur les connexions SSH à la base de données. Des blocages occasionnels ont été observés, qui pourraient être liés à des problèmes initialement rencontrés dans le code des fichiers. (*Signalement par Stephen Frost.*)

- Modifié les conflits de fichiers verrou sur les commandes `backup` et `expire` pour qu’ils soient définis sur `ERROR`. Ils étaient initialement définis sur `DEBUG` en raison d'un copier-coller à partir des verrous d'archive.


### Notes de version v0.10 {#v010-release-notes}

*La sauvegarde et l'archivage sont fonctionnels*

*Sortie le 5 mars 2014*

**Fonctionnalités :**

- La restauration n'est pas encore implémentée, mais les répertoires de sauvegarde sont des répertoires de données PostgreSQL cohérents. Vous devrez décompresser les fichiers ou désactiver la compression de la sauvegarde. Les sauvegardes non compressées sur ZFS, ou un système de fichiers similaire, sont une bonne option car elles peuvent être restaurées localement par instantané pour créer des sauvegardes logiques ou récupérer ponctuellement des données.
- L'archivage est monothread. Cela n'a posé aucun problème sur nos bases de plusieurs téraoctets soumises à un fort volume d'écritures. Un grand volume de WAL est recommandé, ou l'option asynchrone avec un grand volume à proximité.
- Les sauvegardes sont multithreadées, mais la bibliothèque `Net::OpenSSH` ne semble pas sûre à 100% avec les threads et peut très occasionnellement en bloquer un. Un délai global tue le processus et résout le problème. Oui, c'est assez laid.
- Les sommes de contrôle sont perdues lors de toute sauvegarde reprise. Seule la sauvegarde finale enregistre la somme de contrôle après plusieurs reprises. Les sommes de contrôle des sauvegardes précédentes sont correctement enregistrées, et une sauvegarde complète réinitialise tout.

- Le `backup.manifest` est écrit en tant que `Storable` car `Config::IniFile` ne semble pas gérer correctement les grands fichiers. Il serait particulièrement souhaitable de les sauvegarder sous forme de texte lisible par l’humain.

**Fonctionnalités de la documentation :**

- Aucune documentation (hors du code). Enfin, sauf ces notes de version.
