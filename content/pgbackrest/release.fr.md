---
title: "Notes de version"
linkTitle: "Versions"
weight: 60
description: "Historique des versions de pgBackRest avec un journal des modifications détaillé pour chaque version."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [Référence]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## Introduction {#introduction}

Les numéros de version de pgBackRest se composent de trois parties : majeure, mineure et corrective. Une version majeure *peut* rompre la compatibilité avec la version majeure précédente, mais les versions v2 sont entièrement compatibles avec les dépôts v1 et acceptent toutes les options v1. Les versions mineures peuvent inclure des correctifs et des fonctionnalités, mais ne modifient pas le format du dépôt et s'efforcent d'éviter tout changement aux options et aux noms. Les versions correctives corrigent des bogues de la version mineure la plus récente.

Les versions fonctionnelles sont prévues le troisième lundi de janvier, avril, juillet et octobre. Les versions correctives sont prévues, si nécessaire, le troisième lundi des autres mois.

La documentation de la version v1 est disponible [ici](https://pgbackrest.org/1).

Les notes relatives à une version peuvent également contenir des « Notes supplémentaires », mais les modifications de cette section concernent uniquement la documentation ou la suite de tests et n'ont aucun effet direct sur le code de pgBackRest.

--------

## Version stable actuelle {#current-stable-release}

Ce miroir couvre la v2.60.0. Consultez l'[historique des versions amont](https://pgbackrest.org/release.html) pour les versions plus récentes.

### Notes de version v2.60.0 {#v2600-release-notes}

*Erreurs de somme de contrôle des pages et prélecture du stockage objet*

*Sortie le 18 octobre 2026*

**REMARQUE IMPORTANTE** : La commande `restore` signale désormais une erreur et s'arrête si un fichier restauré contient une somme de contrôle de page invalide. Le cluster reste alors incomplet et ne peut pas démarrer ; il faut donc relancer la restauration. La commande `expire` refuse désormais d'effectuer l'expiration si la plus ancienne sauvegarde conservée devait contenir des erreurs de somme de contrôle, ce qui empêche aussi l'expiration des archives dans ce dépôt. Définissez `checksum-page-error=n` pour émettre un avertissement plutôt qu'une erreur.

**Fonctionnalités :**

- Ajout de l'option `checksum-page-error` pour signaler une erreur en cas de somme de contrôle de page invalide. (*Contribution de Andrew Pogrebnoi. Révisé par Douglas J Hunley, David Steele, Greg Sabino Mullane, Stefan Fercot. Suggéré par Greg Sabino Mullane.*)

  Cette option s'applique aux commandes `backup`, `restore` et `expire`. Par défaut, la commande `backup` émet un avertissement pour chaque fichier, comme auparavant, et indique désormais aussi le nombre total d'avertissements de somme de contrôle à la fin de la sauvegarde. Les commandes `restore` et `expire` signalent une erreur par défaut. Auparavant, la commande `restore` ne signalait aucune somme de contrôle de page invalide.

  Ticket [#2687](https://github.com/pgbackrest/pgbackrest/issues/2687); Demande d’intégration [#2833](https://github.com/pgbackrest/pgbackrest/pull/2833); Commit [`d7f54b2`](https://github.com/pgbackrest/pgbackrest/commit/d7f54b2245c8a9467e9a811c65626fe77739376b)
- Prise en charge de Workload Identity Federation pour GCS. (*Contribution de Adol Rodriguez. Révisé par Douglas J Hunley, David Steele.*)

  Définissez `repo-gcs-key-type=web-id` et faites pointer `repo-gcs-key` vers un fichier d'identifiants de compte externe, par exemple généré par `gcloud iam workload-identity-pools create-cred-config`. Le jeton d'identité Web est échangé contre un jeton d'accès sans clé de compte de service. Le fichier de jeton est rechargé à chaque échange pour prendre en compte les rotations, notamment celles des jetons de compte de service projetés par Kubernetes. L'emprunt d'identité d'un compte de service n'est pas pris en charge.

  Ticket [#2838](https://github.com/pgbackrest/pgbackrest/issues/2838); Demande d’intégration [#2839](https://github.com/pgbackrest/pgbackrest/pull/2839); Commit [`1d217e6`](https://github.com/pgbackrest/pgbackrest/commit/1d217e626301118ae2c1e7be39a6a4affa86e501)
- Prélecture de plusieurs fichiers ou plages depuis les stockages objet. (*Révisé par Andrew Pogrebnoi, Douglas J Hunley.*)

  Les requêtes sont mises en file avant la lecture courante afin qu'elles progressent pendant la lecture. Les petits intervalles entre fichiers sont lus au passage, au lieu de déclencher une nouvelle requête. `Restore` utilise ce mécanisme pour lire les fichiers regroupés et les cartes incrémentales par blocs ; `backup` l'utilise pour lire les cartes incrémentales par blocs de la sauvegarde précédente. `repo-storage-prefetch` (3 par défaut) définit le nombre de requêtes mises en file et `repo-storage-read-over` (64KiB par défaut) la taille maximale d'un intervalle lu au passage.

  [`e63dec3`](https://github.com/pgbackrest/pgbackrest/commit/e63dec323b9e79513638b9858e4ad13b6072d060) Prélecture de plusieurs fichiers ou plages depuis les stockages objet. ; Demande d’intégration [#2783](https://github.com/pgbackrest/pgbackrest/pull/2783)

  [`5ae4015`](https://github.com/pgbackrest/pgbackrest/commit/5ae4015d37081eba4259f4de379a9d160236de0e) Regroupement des lectures des cartes incrémentales par blocs précédentes pendant la sauvegarde. ; Demande d’intégration [#2816](https://github.com/pgbackrest/pgbackrest/pull/2816)

**Améliorations :**

- Réduction des requêtes de maintien de connexion vers les processus distants. (*Révisé par Douglas J Hunley.*)

  Une requête de maintien de connexion était envoyée à chaque processus distant à chaque fin de tâche dans `archive-push` et `backup`, même si une requête venait de lui être envoyée. Elle n'est désormais envoyée que si aucune requête n'a été adressée au processus distant depuis 30 secondes.

  Commit [`f652261`](https://github.com/pgbackrest/pgbackrest/commit/f652261d32a4ffba98e7da26a41ef4ef1cd08da3)
- Nouvelle tentative pour les sous-requêtes Azure absentes de la réponse à un lot. (*Révisé par Douglas J Hunley.*)

  Lorsqu'une suppression par lot échoue dans Azure, le service peut renvoyer une seule réponse pour tout le lot. Les sous-requêtes sans réponse étaient considérées comme terminées : un seul fichier par lot était alors supprimé, tandis que la commande annonçait un succès. Les sous-requêtes sans réponse sont désormais réessayées.

  Ticket [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Demande d’intégration [#2849](https://github.com/pgbackrest/pgbackrest/pull/2849); Commit [`567a245`](https://github.com/pgbackrest/pgbackrest/commit/567a2451244e0e7a4c54e41880fac1a007b49930)
- Réduction des vérifications de manifestes lors de la reconstruction de `backup.info`. (*Révisé par Douglas J Hunley. Suggéré par todeb.*)

  Les commandes `backup`, `expire` et `annotate` ne recherchent plus de `backup.manifest` lorsque le listing du dépôt indique que le chemin de sauvegarde n'existe pas, ou lorsqu'une sauvegarde différentielle ou incrémentale appartient à un jeu de sauvegardes complètes absent de `backup.info`. Chaque vérification constitue une requête ; sur un stockage objet, la recherche d'un manifeste absent est donc journalisée comme une erreur 404.

  Ticket [#2769](https://github.com/pgbackrest/pgbackrest/issues/2769); Demande d’intégration [#2825](https://github.com/pgbackrest/pgbackrest/pull/2825); Commit [`0d3c340`](https://github.com/pgbackrest/pgbackrest/commit/0d3c340087bfb97263c29a8fd681cf079071236b)
- Utilisation de la taille d'origine pour déterminer si un fichier doit être regroupé. (*Révisé par Douglas J Hunley.*)

  La taille d'un fichier incrémental par blocs dans la sauvegarde précédente servait à décider de son regroupement. Ainsi, un fichier ayant dépassé `repo-bundle-limit` pouvait encore être stocké dans un regroupement. La taille actuelle du fichier est désormais utilisée.

  Demande d’intégration [#2843](https://github.com/pgbackrest/pgbackrest/pull/2843); Commit [`340d58b`](https://github.com/pgbackrest/pgbackrest/commit/340d58bb49d6c88a002a0d23830fd37be155cc21)
- Ajout de contexte aux erreurs de lecture des cartes de blocs pendant la sauvegarde. (*Révisé par Stefan Fercot, Douglas J Hunley.*)

  Une erreur de lecture de la carte de blocs d'une sauvegarde précédente indique désormais le fichier, le chemin dans le dépôt, le décalage et la taille de la carte. Une lecture renvoyant moins d'octets que prévu est signalée comme telle, et non comme une erreur d'analyse.

  [`bc91688`](https://github.com/pgbackrest/pgbackrest/commit/bc91688c4cf18fa6a36ec65441784533d5e6bdd5) Ajout de contexte aux erreurs de lecture des cartes de blocs pendant la sauvegarde. ; Ticket [#2489](https://github.com/pgbackrest/pgbackrest/issues/2489); Ticket [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Demande d’intégration [#2830](https://github.com/pgbackrest/pgbackrest/pull/2830)

  [`f46bfaf`](https://github.com/pgbackrest/pgbackrest/commit/f46bfafdd53dd0031a320fa95b08568263901ff3) Correction du nom d'option dans les erreurs de carte incrémentale par blocs.
- Conversion de `current_timestamp` en `text` dans l'étiquette de début de sauvegarde. (*Contribution de Tiago Corcelli de Oliveira. Révisé par David Steele.*)

  Une conversion implicite définie par l'utilisateur de `timestamptz` vers `text` faisait échouer la sauvegarde avec « operator is not unique: unknown || timestamp with time zone ». Le texte de l'étiquette reste inchangé.

  Ticket [#2873](https://github.com/pgbackrest/pgbackrest/issues/2873); Commit [`86936e1`](https://github.com/pgbackrest/pgbackrest/commit/86936e1fa60b10b7592eaac09283c4bb5991265d)
- Prise en charge de la compilation sur illumos. (*Contribution de Kalevi Kolttonen. Révisé par Douglas J Hunley, David Steele.*)

  Une tâche OmniOS a été ajoutée à la CI. Solaris pourrait également fonctionner, mais n'a pas été testé.

  Demande d’intégration [#2870](https://github.com/pgbackrest/pgbackrest/pull/2870); Commit [`ad72e58`](https://github.com/pgbackrest/pgbackrest/commit/ad72e5815f3cf9c0c6170dcbe04ef9c41762d3d9)
- Prise en charge d'OpenSSL 4. (*Révisé par Douglas J Hunley.*)

  La compilation avec OpenSSL 4 échouait, car `X509_get_subject_name()` renvoie désormais un nom `const`.

  Commit [`a729ac8`](https://github.com/pgbackrest/pgbackrest/commit/a729ac881f48225622151841e80146f7a3a4bce6)
- Correction des compilations avec clang. (*Révisé par Douglas J Hunley.*)

  Sous Linux, gcc installe `libbacktrace.a` à un emplacement où clang la recherche également, mais installe `backtrace.h` à un emplacement que seul gcc trouve. Une compilation avec clang trouvait la bibliothèque, puis échouait. La bibliothèque n'est désormais utilisée que si son en-tête est trouvé. Les types de retour que clang signale comme des conversions avec réduction de plage dans les compilations de débogage sont également corrigés.

  [`84b031a`](https://github.com/pgbackrest/pgbackrest/commit/84b031af68fe6a30b4150ec6c903cc8c1781fc05) Exiger l'en-tête lors de la vérification de libbacktrace.

  [`195e66b`](https://github.com/pgbackrest/pgbackrest/commit/195e66bafd89da511fb0d48e6e053176104c47c7) Renvoyer le type déclaré pour les fonctions renvoyant une énumération fondée sur StringId.

  [`d9e5e14`](https://github.com/pgbackrest/pgbackrest/commit/d9e5e14e93f460d62930f58dd4dd5bbc2a9f3a85) Renvoyer bool dans une fonction déclarée comme renvoyant bool.
- Migration de la génération de code de C vers Python.

  Lors de la compilation, le code est généré à partir des déclarations d'options, d'erreurs, d'aide et de PostgreSQL par un outil Python, qui remplace un outil C qu'il fallait d'abord compiler. La compilation depuis une copie de travail git nécessite PyYAML au lieu de libyaml. L'archive de publication contient le code généré et ne nécessite ni l'un ni l'autre.

  Commit [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e)

**Améliorations de la documentation :**

- Modernisation du site web. Remerciements particuliers à Jan pour son logo bien trouvé et hilarant. (*Contribution de David Steele, Jan Wieremjewicz. Révisé par Steve Atkins, Kai Wagner, Douglas J Hunley, Nikolaos Stamatopoulos, Matt Hudson, Stefan Fercot.*)

  Le site adopte un nouveau design avec des thèmes clair et sombre et une mise en page adaptée aux téléphones. Les pages avec une table des matières l'affichent à côté du texte et y indiquent la section en cours de lecture. Les commandes et fichiers de configuration peuvent être copiés à l'aide d'un bouton ; les fichiers de configuration mettent en évidence les lignes modifiées par chaque section, et les notes de version peuvent être dépliées pour afficher davantage de détails.

  [`5bc14b5`](https://github.com/pgbackrest/pgbackrest/commit/5bc14b581a054ab3dc9cd633954a689acc99a58f) Raccourcir et clarifier les titres de la documentation.

  [`b668d71`](https://github.com/pgbackrest/pgbackrest/commit/b668d71f22489cbd4d5e120e7e6e73be0ca9e167) Déplacer les sponsors plus bas sur la page d'accueil et raccourcir l'appel au soutien.

  [`60b85c5`](https://github.com/pgbackrest/pgbackrest/commit/60b85c58d98dd65d47747e6355f47c934cd6b430) Moderniser le site web.

  [`ab8df23`](https://github.com/pgbackrest/pgbackrest/commit/ab8df23807cc4c11768ef40196bcade70ebec23a) Afficher une carte plutôt que le logo lorsqu'un lien est partagé.

  [`76ae494`](https://github.com/pgbackrest/pgbackrest/commit/76ae49456c7dace20bbd6f17e8acdfd36bf03a46) Supprimer la table des matières de la page des versions et réduire l'espacement autour de la date.

  [`3e86c71`](https://github.com/pgbackrest/pgbackrest/commit/3e86c71f5546c86941f35d5be3a7fdcd98af3cca) Référencer les options par des liens plutôt que les répéter dans la référence des commandes.

  [`dc3af7b`](https://github.com/pgbackrest/pgbackrest/commit/dc3af7b2aee5778dbe9200e31d5a2f95ecae5777) Clarifier les titres des commandes dans la référence des commandes.

  [`078d52c`](https://github.com/pgbackrest/pgbackrest/commit/078d52c5768bb67989624b5418fdd687fab9e485) Marquer les lignes modifiées par une section dans un fichier de configuration.

  [`bd33623`](https://github.com/pgbackrest/pgbackrest/commit/bd33623ba945ed251e2a6704cea14a81d51c2c9e) Marquer la sortie d'une commande comme un fichier de configuration.

  [`578fc2d`](https://github.com/pgbackrest/pgbackrest/commit/578fc2de14a6a739401fd58b9a232cf587c52fb4) Permettre de copier une commande aussi bien qu'un fichier de configuration.

  [`1fb93f9`](https://github.com/pgbackrest/pgbackrest/commit/1fb93f92725124d6afa8953b7c7243aee92fcaf5) Signaler une erreur lorsqu'une section de configuration ne change rien de visible pour le lecteur.

  [`2f3b2f2`](https://github.com/pgbackrest/pgbackrest/commit/2f3b2f22a30a35340549d42b09d5aaa58d9dfe61) Faire du logo du site un lien vers l'accueil.

  [`8f902c6`](https://github.com/pgbackrest/pgbackrest/commit/8f902c66609c0bf1de6720e60552adde515209cd) Accélérer la génération de la documentation.

  [`b56b6ab`](https://github.com/pgbackrest/pgbackrest/commit/b56b6ab4d24ff6298b95b415b3115591e311de20) Lister automatiquement les actualités les plus récentes sur la page d'accueil.

  [`5b8987d`](https://github.com/pgbackrest/pgbackrest/commit/5b8987da0bb24fc3979fb764ccbde82b7b0e9500) Présenter les exemples de types d'options comme des blocs de code dans la référence.

  [`b5d5274`](https://github.com/pgbackrest/pgbackrest/commit/b5d527471444f90df5529f15726b3d33065f9829) Faire défiler le menu horizontalement au lieu de le laisser déborder par retour à la ligne.

  [`9ae2c32`](https://github.com/pgbackrest/pgbackrest/commit/9ae2c32a35f56f53f299e8c04f004ed3386b95e4) Mettre la page courante en évidence dans le menu plutôt que l'en retirer.

  [`b8da5b0`](https://github.com/pgbackrest/pgbackrest/commit/b8da5b061d0f9c5d1cc01e936dc65cbdd9f70be7) Versionner les liens des styles et scripts pour renouveler les caches périmés.

  [`ec57431`](https://github.com/pgbackrest/pgbackrest/commit/ec57431aa88860b9058d971b938afb5e35a142c7) Aller directement à une section plutôt que faire défiler progressivement la page.

  [`46babed`](https://github.com/pgbackrest/pgbackrest/commit/46babedaed8429026efa4592d93a8d9876acad0b) Estomper le bord au-delà duquel le menu continue au lieu de le couper net.

  [`17de501`](https://github.com/pgbackrest/pgbackrest/commit/17de50192b7e40d7517a4079451e93da5c39b3f3) Placer la barre d'un en-tête section2 sous le titre plutôt qu'à côté.

  [`940f431`](https://github.com/pgbackrest/pgbackrest/commit/940f4311375dda3caabdc0bdd01c36bedf43d46f) Centrer le titre de la page à côté du logo et l'aligner à gauche lorsqu'il passe sur plusieurs lignes.

  [`050ca9e`](https://github.com/pgbackrest/pgbackrest/commit/050ca9e354421530ba4282d95dead90e31d6dc2a) Ajouter des détails dépliables aux notes de version.

  [`bd8f99b`](https://github.com/pgbackrest/pgbackrest/commit/bd8f99be00cd4b03a1b234bf7fbaa39f406c0c44) Ajouter les détails des notes de version de v2.33 à v2.60.

  [`28a1e3d`](https://github.com/pgbackrest/pgbackrest/commit/28a1e3d6278992e0a347aab19248abdcddefd491) Ajuster le style des mots-clés en mode clair.

  [`1911f5f`](https://github.com/pgbackrest/pgbackrest/commit/1911f5f1744ff4bfee528d95e37a0a8d9b77d6b3) Arrêter l'historique des notes de version à l'intégration amont dans la CI.
- Documentation du calendrier des publications.

  Les versions fonctionnelles sont prévues le troisième lundi de janvier, avril, juillet et octobre. Les versions correctives sont prévues, si nécessaire, le troisième lundi des autres mois. L'introduction des notes de version décrit également les composantes majeure, mineure et corrective des numéros de version.

  [`9bca69a`](https://github.com/pgbackrest/pgbackrest/commit/9bca69a591abcee0623ff910d0db3e27008cfc25) Documenter le calendrier des publications.

  [`c179f3f`](https://github.com/pgbackrest/pgbackrest/commit/c179f3f7d6d6b1963d9d3b98b981786ef9546022) Mettre à jour la numérotation des versions dans l'introduction des notes de version.
- Migration des outils de documentation de C et Perl vers Python.

  La documentation est générée par `doc/doc.py` au lieu d'un outil C lancé par `doc/doc.pl`, et sa génération ne nécessite plus Perl.

  [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e) Migrer le code de compilation et de documentation de C vers Python.

  [`fa3d197`](https://github.com/pgbackrest/pgbackrest/commit/fa3d1979b77d6252642c64d708a951914e0a0ac2) Migrer le reste du code de documentation de Perl vers Python.

**Améliorations de la suite de tests :**

- Migration du banc de tests de C et Perl vers Python.

  Les tests sont exécutés avec `test/test.py` au lieu de `test/test.pl`. Les conteneurs de test et les exécuteurs CI ne nécessitent plus Perl, et le banc de tests est lui-même couvert par des tests.

  [`163e5ba`](https://github.com/pgbackrest/pgbackrest/commit/163e5ba0f9ff72ec730f0b35ddac0e5d68ece531) Migrer le banc de tests de C vers Python.

  [`e25c662`](https://github.com/pgbackrest/pgbackrest/commit/e25c6621e8427e862e4ce0196d059ab651bb276d) Migrer le reste du banc de tests de Perl vers Python.
- Ajout d'une tâche Fil-C à la CI.

  Fil-C est une implémentation de C sûre du point de vue mémoire, qui vérifie chaque accès par pointeur. Elle a trouvé deux lectures hors limites qui avaient échappé à gcc, clang et Valgrind. Un nouveau workflow compile et teste également sur l'exécuteur CI avec gcc et clang, avec et sans les bibliothèques optionnelles.

  [`f32a5d5`](https://github.com/pgbackrest/pgbackrest/commit/f32a5d5543c4dc547006629bdb2dd52d3edb9205) Ajouter un workflow pour compiler et tester sur l'exécuteur sans conteneur.

  [`12396fb`](https://github.com/pgbackrest/pgbackrest/commit/12396fb353bc4aa10c3739b826189e421732adf5) Ajouter une tâche Fil-C au workflow de compilation.

  [`908a11a`](https://github.com/pgbackrest/pgbackrest/commit/908a11a841e85d4e66e4aa551380b52aabfe606f) Utiliser la distribution Fil-C telle quelle, puisqu'elle inclut désormais toutes les bibliothèques nécessaires.
- Ajout de tests de fuzzing pour les lecteurs `JSON`, `Ini` et `Pack`.

  Les lecteurs sont soumis au fuzzing avec libFuzzer, AddressSanitizer et UndefinedBehaviorSanitizer dans la CI. Ces tests ont révélé plusieurs bogues dans la lecture des entrées invalides : par exemple, des tableaux JSON profondément imbriqués dans un fichier d'information ou une réponse de stockage objet pouvaient déborder la pile des contextes mémoire.

  Commit [`4c65010`](https://github.com/pgbackrest/pgbackrest/commit/4c65010e7d28ea68571732fb275d91266a97ad80)
- Acceptation de noms d'utilisateurs de test refusés par adduser sur Debian. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Le conteneur de test est construit avec le même nom d'utilisateur que celui de l'hôte. La commande `adduser` de Debian refuse les noms contenant un point, comme `first.last` ; la construction du conteneur échouait donc sur les images Debian pour ces utilisateurs.

  Ticket [#2858](https://github.com/pgbackrest/pgbackrest/issues/2858); Demande d’intégration [#2859](https://github.com/pgbackrest/pgbackrest/pull/2859); Commit [`ce19dae`](https://github.com/pgbackrest/pgbackrest/commit/ce19dae6a2d6ab3665374ead04c270fd45d563fb)


--------

## Versions stables {#stable-releases}

### Notes de version v2.59.3 {#v2593-release-notes}

*Bogue des sous-clés de chiffrement faibles*

*Sortie le 4 octobre 2026*

**REMARQUE IMPORTANTE**: Dans les versions précédentes, une erreur d’accès aux données aléatoires du système pouvait entraîner la génération de sous-clés de chiffrement et de sels faibles. Consultez [Sous-clés de chiffrement et sels faibles](/fr/pgbackrest/news/#weak-encryption) pour plus d’informations.

**Correctifs de bogues:**

- Correction d’une possible erreur de somme de contrôle lors du chargement des fichiers d’information et des manifestes chiffrés. (*Corrigé par j0uinim. Relu par David Steele.*)

  Un gros fichier d'information ou manifeste chiffré pouvait perdre ses dernières lignes au chargement, ce qui faisait échouer la vérification de la somme de contrôle. Les lignes perdues devaient tenir dans le dernier bloc de chiffrement ; ce cas est donc peu probable en pratique.

  Ticket [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Demande d’intégration [#2868](https://github.com/pgbackrest/pgbackrest/pull/2868); Commit [`2def063`](https://github.com/pgbackrest/pgbackrest/commit/2def063e06c6f0b7e137309c7ed0d7631a42f6cf)
- Correction de la génération possible de sous-clés de chiffrement ou de sels faibles. (*Corrigé par j0uinim. Relu par David Steele, Stefan Fercot, Douglas J Hunley.*)

  Lorsqu'OpenSSL ne parvenait pas à obtenir des données aléatoires du système d'exploitation, l'échec était ignoré et les sous-clés et sels étaient générés à partir d'une zone mémoire non aléatoire. Une erreur est désormais signalée.

  Ticket [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Demande d’intégration [#2867](https://github.com/pgbackrest/pgbackrest/pull/2867); Commit [`47ed78f`](https://github.com/pgbackrest/pgbackrest/commit/47ed78f8d54a44466a872852939edc0273172bf1)

### Notes de version v2.59.2 {#v2592-release-notes}

*Prise en charge de PostgreSQL 19beta4*

*Sortie le 27 septembre 2026*

**Correctifs de bogues :**

- Corriger la carte de blocs vide lorsqu'un fichier est tronqué à zéro pendant la sauvegarde. (*Révisé par Douglas J Hunley. Signalement par JPCOSTA78.*)

  Un fichier incrémental par blocs dépassant `repo-bundle-limit` et tronqué à zéro par PostgreSQL pendant une sauvegarde était stocké comme une carte de blocs sans blocs. Toutes les sauvegardes suivantes référençant ce fichier échouaient avec « unexpected eof » jusqu'à la prochaine sauvegarde complète.

  Ticket [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Demande d’intégration [#2842](https://github.com/pgbackrest/pgbackrest/pull/2842); Commit [`572d163`](https://github.com/pgbackrest/pgbackrest/commit/572d1631026d5f10915634592b547f3439b7a291)
- Désactiver la nouvelle tentative de lecture lorsque des filtres sont passés au pilote. (*Révisé par Douglas J Hunley. Signalement par megamaced.*)

  La nouvelle tentative de lecture d'un dépôt sur stockage objet via un hôte de dépôt provoquait un plantage. Le client ne réessaie plus ces lectures. L'hôte du dépôt continue de réessayer ses lectures depuis le stockage objet.

  Ticket [#2845](https://github.com/pgbackrest/pgbackrest/issues/2845); Demande d’intégration [#2846](https://github.com/pgbackrest/pgbackrest/pull/2846); Commit [`c6eca28`](https://github.com/pgbackrest/pgbackrest/commit/c6eca28ff8e551bd2e76f0c91b1a70ddee60b35e)
- Corriger la pagination de la liste des versions S3. (*Révisé par Douglas J Hunley, guruguruguru. Signalement par guruguruguru.*)

  La lecture d'un dépôt à un instant cible avec `repo-target-time` échouait avec « unable to find child 'NextContinuationToken' » lorsque plus de mille versions étaient répertoriées sous un préfixe.

  Ticket [#2854](https://github.com/pgbackrest/pgbackrest/issues/2854); Demande d’intégration [#2855](https://github.com/pgbackrest/pgbackrest/pull/2855); Commit [`6f0490d`](https://github.com/pgbackrest/pgbackrest/commit/6f0490dd29f0c756e6766fd9be023805540815fc)
- Définir l'en-tête de version Azure pour l'authentification `SAS`. (*Révisé par Douglas J Hunley. Signalement par Florian Helmberger.*)

  Les suppressions par lot nécessitent l'en-tête de version ; avec l'authentification `SAS`, chaque lot était donc rejeté. Ce rejet semblait ne concerner qu'un seul fichier, et le reste de chaque lot n'était pas supprimé alors que `expire` annonçait un succès. Des sauvegardes et WAL expirés restaient ainsi dans le dépôt.

  Ticket [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Demande d’intégration [#2848](https://github.com/pgbackrest/pgbackrest/pull/2848); Commit [`ea3293b`](https://github.com/pgbackrest/pgbackrest/commit/ea3293be75c86b5e6c9ca4158b5ebe2a3224f76f)
- Corriger le blocage de `archive-push` asynchrone sur un fichier d'historique de sauvegarde de taille nulle. (*Corrigé par Andrew Kroh. Révisé par David Steele, Douglas J Hunley.*)

  Un fichier d'historique de sauvegarde de taille nulle, par exemple dans un cluster copié depuis un instantané de stockage, faisait échouer chaque exécution asynchrone de `archive-push`, si bien qu'aucun WAL n'était archivé. `archive-push-batch-size` est désormais converti en nombre de segments à partir de la taille du premier segment WAL prêt.

  Ticket [#2856](https://github.com/pgbackrest/pgbackrest/issues/2856); Demande d’intégration [#2857](https://github.com/pgbackrest/pgbackrest/pull/2857); Commit [`12b1b3c`](https://github.com/pgbackrest/pgbackrest/commit/12b1b3cf58caee7b04ed788eee221726f5caa155)
- Corriger la commande `annotate` sur un dépôt distant chiffré. (*Corrigé par Douglas J Hunley. Révisé par David Steele.*)

  Lorsque le dépôt était chiffré et que le chiffrement était configuré uniquement sur l'hôte du dépôt, `annotate` ne parvenait pas à charger `backup.info`.

  Commit [`497ad5a`](https://github.com/pgbackrest/pgbackrest/commit/497ad5aee0c654611d2ad4185958727e1341dd8c)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta4/rc1.

  PostgreSQL 19beta4 a annulé les changements des sommes de contrôle de pages en ligne ; leur version est donc de nouveau limitée à 0 et 1. Cette version a également changé la version de `pg_control` et le nombre magique des pages WAL.

  Commit [`89eae83`](https://github.com/pgbackrest/pgbackrest/commit/89eae839d5ca79591aaea8157f437688c3b53df4)

### Notes de version v2.59.1 {#v2591-release-notes}

*Prise en charge de PostgreSQL 19beta3*

*Sortie le 17 août 2026*

**Correctifs de bogues :**

- Corriger le blocage lorsque la taille du tampon de morceau est inférieure à celle du tampon d'entrée. (*Révisé par Andrew Pogrebnoi, Douglas J Hunley. Signalement par crajac66.*)

  Un envoi multipartie vers S3, GCS ou Azure pouvait boucler indéfiniment lorsque le tampon de morceau était plus petit que le tampon d'entrée, par exemple après une augmentation de la taille des morceaux pendant l'envoi. Le tampon de morceau est désormais toujours assez grand pour contenir le tampon d'entrée.

  Ticket [#2818](https://github.com/pgbackrest/pgbackrest/issues/2818); Demande d’intégration [#2819](https://github.com/pgbackrest/pgbackrest/pull/2819); Commit [`a53e470`](https://github.com/pgbackrest/pgbackrest/commit/a53e470eca258c2db088af55be307403c8f43b7a)
- Comparer une étiquette de sauvegarde nouvelle uniquement avec son propre jeu de sauvegardes complètes. (*Révisé par Douglas J Hunley. Signalement par Anton Glushakov.*)

  Certains stockages objet continuent de lister un préfixe après la suppression de tout son contenu, par exemple MinIO avec le verrouillage d'objets ou SeaweedFS. Une sauvegarde complète supprimée pouvait donc encore apparaître dans le dépôt. Toutes les sauvegardes différentielles et incrémentales suivantes échouaient alors avec « new backup label ... is not later than latest backup label ... ». Une nouvelle étiquette n'est désormais comparée qu'aux sauvegardes de son propre jeu de sauvegardes complètes.

  Ticket [#2792](https://github.com/pgbackrest/pgbackrest/issues/2792); Demande d’intégration [#2824](https://github.com/pgbackrest/pgbackrest/pull/2824); Commit [`d01f77e`](https://github.com/pgbackrest/pgbackrest/commit/d01f77e8237f5d008bb7782c18ced12cd6d1971a)
- Corriger les archives sources générées par GitHub qui manquent des fichiers nécessaires à la compilation. (*Signalement par aardvarkzed.*)

  Les archives sources générées par GitHub pour une version ne contenaient pas les outils de génération de code ni les fichiers qu'ils lisent ; elles ne pouvaient donc pas être compilées. Seule l'archive de distribution est désormais allégée.

  Ticket [#2821](https://github.com/pgbackrest/pgbackrest/issues/2821); Commit [`163670a`](https://github.com/pgbackrest/pgbackrest/commit/163670a4eeede6d2d170b5d1f55c5ba0b66ba564)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta3. (*Contribution de Lardière Sébastien. Révisé par David Steele.*)

  PostgreSQL 19beta3 a changé le nombre magique des pages WAL.

  Commit [`5cbc256`](https://github.com/pgbackrest/pgbackrest/commit/5cbc256bf37a44fa478d73a12a2e5b2d84fa6337)

**Améliorations de la documentation :**

- Documenter l'exception pour les points dans les noms de bucket S3 lorsque `repo-s3-uri-style=path`.

  Avec `repo-s3-uri-style=path`, le bucket fait partie du chemin plutôt que du nom d'hôte ; les points dans son nom ne provoquent donc pas de divergence avec le nom d'hôte du certificat.

  Commit [`bbdc4b9`](https://github.com/pgbackrest/pgbackrest/commit/bbdc4b9217a0e66f6a01c05f4edc04282cffb3fc)
- Suppression de la configuration explicite `hot_standby` du guide utilisateur.

  `hot_standby` est activé par défaut depuis PostgreSQL 10. Le guide de démarrage rapide précise désormais qu'un serveur de secours n'accepte pas de connexions en lecture seule sans ce paramètre.

  Commit [`cda454d`](https://github.com/pgbackrest/pgbackrest/commit/cda454d4bac0c0412230a0b41513659a7d0d4205)

### Notes de version v2.59.0 {#v2590-release-notes}

*Prise en charge de PostgreSQL 19beta2*

*Sortie le 20 juillet 2026*

**NOTE AUX PAQUETEURS** : Un nouveau paquet source est disponible, qui simplifie le processus de compilation en fournissant une documentation HTML prégénérée, une page de manuel et du code. Ce paquet est joint à chaque version comme un élément et porte le nom `pgbackrest-{version}.tar.gz`. Consultez `README.md` dans le paquet pour plus de détails. Veuillez utiliser ce nouveau paquet source afin d’éviter les outils supplémentaires nécessaires à la génération du code dans les versions futures. Consultez [Nouveau paquet source](/fr/pgbackrest/news/#distribution-tarball) pour plus d’informations.<br/> <br/> **NOTE AUX PAQUETEURS** : Une nouvelle dépendance optionnelle à `libsystemd` a été ajoutée.<br/> <br/> **NOTE IMPORTANTE** : À compter de cette version, seule la commande `restore` peut être exécutée en tant que root par défaut. Utilisez `allow-root` pour exécuter d'autres commandes en tant que root (ce qui n’est toutefois pas recommandé).

**Correctifs de bogues :**

- Corriger la suppression par `expire` d'une sauvegarde en cours sur un autre hôte. (*Révisé par Douglas J Hunley. Signalement par Dmitrii.*)

  Une sauvegarde n'est ajoutée à `backup.info` qu'une fois terminée. Lorsque `expire` s'exécutait sur un hôte pendant qu'une sauvegarde tournait sur un autre, par exemple `expire` sur un serveur de secours pendant la sauvegarde du primaire, la sauvegarde en cours était supprimée. L'expiration ne supprime plus la dernière sauvegarde lorsqu'elle est en cours ou peut être reprise.

  Ticket [#2622](https://github.com/pgbackrest/pgbackrest/issues/2622); Demande d’intégration [#2797](https://github.com/pgbackrest/pgbackrest/pull/2797); Commit [`aa0e215`](https://github.com/pgbackrest/pgbackrest/commit/aa0e215019f50f92a8f0c97f907affc1d3bf86c4)
- Corriger la non-application de `archive-push-queue-max` lorsqu'un fichier WAL provoque une erreur. (*Révisé par Stefan Fercot. Signalement par vut12.*)

  En mode asynchrone, la taille de la file était calculée à partir des WAL restant à envoyer. Lorsqu'un fichier WAL échouait à répétition, les suivants étaient envoyés et n'étaient plus comptés, bien qu'ils restent dans `pg_wal`. La limite de la file n'était donc jamais atteinte et `pg_wal` pouvait remplir le disque. La file est désormais mesurée à partir de tous les WAL dont PostgreSQL attend l'archivage, comme en mode synchrone.

  Ticket [#2629](https://github.com/pgbackrest/pgbackrest/issues/2629); Demande d’intégration [#2799](https://github.com/pgbackrest/pgbackrest/pull/2799); Commit [`7fe3636`](https://github.com/pgbackrest/pgbackrest/commit/7fe363658639bbc2f70e53496fa6da4acb9e481e)
- Corriger l'échec asynchrone de `archive-get` pendant une récupération traversant un changement de timeline. (*Révisé par Douglas J Hunley. Signalement par Jimmy Yih.*)

  Deux processus asynchrones pouvaient se disputer le verrou d'archive. Celui qui perdait se terminait avant d'avoir récupéré le segment pour lequel il avait été lancé. Le `archive-get` qui l'avait démarré attendait alors `archive-timeout` et renvoyait une erreur pour un segment pourtant présent, ce qui pouvait arrêter la récupération prématurément, notamment lors d'un changement de timeline. Le segment est désormais récupéré directement lorsque le processus asynchrone chargé de le récupérer ne tourne pas.

  Ticket [#2423](https://github.com/pgbackrest/pgbackrest/issues/2423); Demande d’intégration [#2806](https://github.com/pgbackrest/pgbackrest/pull/2806); Commit [`baed942`](https://github.com/pgbackrest/pgbackrest/commit/baed942af0d61fcf3c2cb1f7d1bf1d6fe5bb6df9)
- Corriger un possible dépassement de tampon dans le module d'erreur. (*Corrigé par Christophe Pettus. Révisé par David Steele.*)

  Une trace de pile trop longue pour son tampon n'était pas terminée et pouvait être lue au-delà de celui-ci. Une erreur trop longue pour son tampon pouvait aussi provoquer une écriture au-delà de sa fin lors de l'ajout d'une erreur système. Ces deux cas nécessitent un message inhabituellement long.

  [`7fd8bc8`](https://github.com/pgbackrest/pgbackrest/commit/7fd8bc89a15cb039111aa85fd37f9dc68f7c4d6d) Corriger un possible dépassement de tampon dans le module d'erreur.

  [`5ca98ab`](https://github.com/pgbackrest/pgbackrest/commit/5ca98abc91f823ef97ff6a1e77d65727d1259218) Utiliser tout le tampon lors du formatage des messages d'erreur.

  [`3a71dc8`](https://github.com/pgbackrest/pgbackrest/commit/3a71dc839a89b83f592c1d5813c068bcded1b6bc) Empêcher une écriture hors limites dans le tampon d'erreur pour un message trop long.
- Corriger une utilisation après libération du client du protocole parallèle. (*Révisé par Douglas J Hunley. Signalement par Georgy Shelkovy.*)

  Un client n'ayant plus de travail était libéré, mais restait dans la liste des clients et était de nouveau libéré lors d'un appel ultérieur. Avec la journalisation de débogage ou de trace, cela entraînait une lecture de mémoire libérée et pouvait provoquer un plantage, par exemple lors d'une sauvegarde parallèle avec `log-level-file=trace`.

  Ticket [#2754](https://github.com/pgbackrest/pgbackrest/issues/2754); Demande d’intégration [#2804](https://github.com/pgbackrest/pgbackrest/pull/2804); Commit [`31432ed`](https://github.com/pgbackrest/pgbackrest/commit/31432ed3977302b5e183f2b592d85afb521b4f55)
- Corriger un dépassement de tas lorsqu'une option pg est définie sans pg1. (*Révisé par Douglas J Hunley. Signalement par Naveen.*)

  Lorsque des options `pg` étaient définies pour d'autres index sans `pg1-path`, par exemple `pg2-path` et `pg3-path`, la table des index était écrasée. Cela corrompait le tas avec musl, notamment sur Alpine, et provoquait une erreur de segmentation. Le `pg-path` portant le plus grand numéro était également omis.

  Ticket [#1768](https://github.com/pgbackrest/pgbackrest/issues/1768); Demande d’intégration [#2796](https://github.com/pgbackrest/pgbackrest/pull/2796); Commit [`2d767de`](https://github.com/pgbackrest/pgbackrest/commit/2d767de3c59cf5570639e75755dc73c626fb99e1)
- Correction d'un plantage lorsqu'un signal arrive pendant la terminaison avec musl 1.2.6.

  musl 1.2.6, par exemple sur Alpine 3.24, plante lorsque `exit()` est appelé alors qu'une terminaison est déjà en cours. Cela se produisait lorsqu'un signal arrivait pendant la terminaison, par exemple quand la commande `server` terminait un processus enfant qui était déjà en train de se terminer. Un signal reçu pendant la terminaison est désormais ignoré.

  Commit [`e166a33`](https://github.com/pgbackrest/pgbackrest/commit/e166a33f48a00192c09b0f1cea3465243c03d1f1)

**Fonctionnalités :**

- Prise en charge de PostgreSQL 19beta1/beta2. (*Révisé par Stefan Fercot.*)

  Ajout de la prise en charge de PostgreSQL 19beta1/beta2. PostgreSQL 19 peut activer et désactiver les sommes de contrôle des pages en ligne. Celles-ci ne sont pas validées pendant l'une ou l'autre de ces opérations.

  [`bc6d399`](https://github.com/pgbackrest/pgbackrest/commit/bc6d399a6a160f5fa41dd3a98ae046dff66e56a8) Prise en charge de PostgreSQL 19beta1. ; Demande d’intégration [#2779](https://github.com/pgbackrest/pgbackrest/pull/2779)

  [`2777395`](https://github.com/pgbackrest/pgbackrest/commit/2777395dacc35aec51572d3e75c621725e2f9d9c) Prise en charge de PostgreSQL 19beta2.
- Ajout de l'option `archive-expire-before` pour nettoyer l'archive WAL. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  L'option `archive-expire-before` de `expire` supprime de l'archive les WAL précédant un segment donné, mais jamais ceux nécessaires à une sauvegarde conservée. Elle peut nettoyer l'archive à partir du point de redémarrage d'un serveur de secours avec `archive_cleanup_command`, à la place de `pg_archivecleanup`, qui ne tient pas compte de la rétention.

  [`6cd692b`](https://github.com/pgbackrest/pgbackrest/commit/6cd692b1b321faf544ee3a9b1f503fd48007d7c7) Extraire l'expiration des WAL dans expireArchiveId().

  [`4945139`](https://github.com/pgbackrest/pgbackrest/commit/4945139392c21f197f2e307abc3c89b5548cef8d) Ajouter l'option archive-expire-before pour nettoyer l'archive WAL. ; Demande d’intégration [#2801](https://github.com/pgbackrest/pgbackrest/pull/2801)
- Ajout de la suppression par lots pour le stockage Azure. (*Révisé par Douglas J Hunley, Crispy.*)

  Les fichiers sont supprimés avec l'API Azure Blob Batch, jusqu'à 256 par requête, au lieu d'une requête par fichier. Cela accélère `expire` et les autres commandes qui suppriment des fichiers du dépôt.

  Demande d’intégration [#2786](https://github.com/pgbackrest/pgbackrest/pull/2786); Commit [`ffa325b`](https://github.com/pgbackrest/pgbackrest/commit/ffa325b8a44c1e9e44dc038bbcc8aece6f312a90)
- Ajout de la prise en charge des S3 Outposts. (*Contribution de Shiva Kumar Ambigi. Révisé par David Steele, Roberto Mello.*)

  Définissez `repo-s3-service=s3-outposts` pour utiliser un point de terminaison S3 Outposts. Cette option fixe le nom du service utilisé pour signer les requêtes et vaut `s3` par défaut.

  Demande d’intégration [#2762](https://github.com/pgbackrest/pgbackrest/pull/2762); Commit [`6c51800`](https://github.com/pgbackrest/pgbackrest/commit/6c518001c24ad2405eaf750d358f69703322a221)
- Ajout de l'authentification par processus S3. (*Révisé par Andrew Charlton. Suggéré par Andrew Charlton.*)

  Définissez `repo-s3-key-type=process` et faites pointer `repo-s3-process-cmd` vers une commande qui produit des identifiants temporaires au format JSON du fournisseur d'identifiants par processus AWS. Les identifiants sont renouvelés avant leur expiration.

  Demande d’intégration [#2778](https://github.com/pgbackrest/pgbackrest/pull/2778); Commit [`b5a578a`](https://github.com/pgbackrest/pgbackrest/commit/b5a578a5c2c88d53fca0ee8cfbfb8ee662ce7e48)
- Fourniture d'une archive de distribution avec le code et la documentation générés.

  L'archive contient le code généré ainsi que la page de manuel et la documentation HTML déjà produites. Elle se compile et s'installe donc sans les outils de génération de code et de documentation, notamment `libyaml`.

  Commit [`8fcfef5`](https://github.com/pgbackrest/pgbackrest/commit/8fcfef5d8732055f9bc8e50224d5b7a988512e61)

**Améliorations :**

- Reconnecter le stockage SFTP après que le serveur a fermé une connexion inactive. (*Révisé par Stefan Fercot. Suggéré par mustafa0x, tisserat.*)

  Les serveurs SFTP et les pare-feu peuvent fermer une connexion restée inactive, par exemple la connexion de lecture du dépôt pendant la phase de copie d'une sauvegarde. L'utilisation suivante échouait alors avec une erreur de socket. Une connexion interrompue est désormais rouverte et l'opération est réessayée une fois.

  [`d72bea9`](https://github.com/pgbackrest/pgbackrest/commit/d72bea9fe7c3975fc6832a51b0b0c1c041c467d2) Récupérer la session libssh2 depuis le stockage dans les objets de lecture/écriture SFTP.

  [`a31febf`](https://github.com/pgbackrest/pgbackrest/commit/a31febfbd9ba639589fe57e4083ae9358b1306a4) Reconnecter le stockage SFTP après la fermeture d'une connexion inactive par le serveur. ; Ticket [#2739](https://github.com/pgbackrest/pgbackrest/issues/2739); Ticket [#2772](https://github.com/pgbackrest/pgbackrest/issues/2772); Demande d’intégration [#2793](https://github.com/pgbackrest/pgbackrest/pull/2793)
- Ajouter le cache utilisateur/groupe pour une construction plus rapide du manifeste. (*Contribution de Gunnar Lindholm. Révisé par David Steele.*)

  Lorsque les noms d'utilisateurs et de groupes sont résolus par un service distant, comme sssd ou LDAP, chaque recherche nécessite un aller-retour réseau. Ces recherches représentaient l'essentiel du temps de construction du manifeste pour les clusters contenant des millions de fichiers. Les noms d'utilisateurs et de groupes sont désormais mis en cache.

  Demande d’intégration [#2773](https://github.com/pgbackrest/pgbackrest/pull/2773); Commit [`1e6d23f`](https://github.com/pgbackrest/pgbackrest/commit/1e6d23fea72ac9c599f8b62a2e0a3de02d0d08d0)
- Ajouter la progression de sauvegarde par dépôt dans la sortie de la commande `info`. (*Contribution de Will Morland. Révisé par David Steele, Stefan Fercot.*)

  Lorsque des sauvegardes s'exécutent simultanément sur plusieurs dépôts, la commande `info` indique désormais la progression de chaque dépôt en plus de la progression globale. La sortie JSON contient un tableau `repo` pour chaque verrou de sauvegarde.

  Ticket [#2736](https://github.com/pgbackrest/pgbackrest/issues/2736); Demande d’intégration [#2740](https://github.com/pgbackrest/pgbackrest/pull/2740); Commit [`77312b3`](https://github.com/pgbackrest/pgbackrest/commit/77312b33ba913132b33401d862c2e354f323c786)
- Ajouter des vérifications `backup.info` à la commande `verify`. (*Contribution de Denis Garsh. Révisé par David Steele, Douglas J Hunley.*)

  La commande `verify` émet désormais un avertissement lorsqu'une sauvegarde du dépôt est absente de `backup.info` et lorsqu'une sauvegarde de `backup.info` est absente du dépôt. Une sauvegarde absente est signalée comme ayant un manifeste manquant.

  Ticket [#2723](https://github.com/pgbackrest/pgbackrest/issues/2723); Demande d’intégration [#2752](https://github.com/pgbackrest/pgbackrest/pull/2752); Commit [`7f82fb6`](https://github.com/pgbackrest/pgbackrest/commit/7f82fb6635c1e3e9dd285d53076e9aee3fbf1ca2)
- Permettre la configuration du point de terminaison S3 STS. (*Contribution de Simon Gratton. Révisé par David Steele.*)

  Définissez `repo-s3-sts-host` pour utiliser un point de terminaison STS régional avec `repo-s3-key-type=web-id`, par exemple `sts.eu-central-2.amazonaws.com`. Les régions AWS à activation explicite n'acceptent pas les identifiants du point de terminaison global, qui reste la valeur par défaut.

  Ticket [#2791](https://github.com/pgbackrest/pgbackrest/issues/2791); Demande d’intégration [#2798](https://github.com/pgbackrest/pgbackrest/pull/2798); Commit [`11f5582`](https://github.com/pgbackrest/pgbackrest/commit/11f5582dfe696187cab1f15d08f649a5117730b3)
- Ajouter `archive-push-batch-size` pour limiter la quantité de WAL envoyée par exécution asynchrone. (*Révisé par Stefan Fercot.*)

  En mode asynchrone, `archive-push-queue-max` n'est vérifié qu'au début d'une exécution. Une exécution traitant un gros retard pouvait donc laisser la file dépasser largement la limite. `archive-push-batch-size` (16GiB par défaut) limite les WAL envoyés par exécution, afin que la file soit revérifiée plus tôt.

  Demande d’intégration [#2803](https://github.com/pgbackrest/pgbackrest/pull/2803); Commit [`34a035f`](https://github.com/pgbackrest/pgbackrest/commit/34a035f4d62f06822c1f60f72a605762cc1ad79c)
- Quitter l'opération asynchrone `archive-push` à la première erreur. (*Révisé par Stefan Fercot. Suggéré par Lardière Sébastien.*)

  Lorsque le dépôt était indisponible, le processus asynchrone continuait d'essayer chaque segment WAL prêt. Une exécution pouvait donc durer assez longtemps pour que `pg_wal` se remplisse avant la prochaine vérification de `archive-push-queue-max`. L'exécution s'arrête désormais à la première erreur, une fois les tâches en cours terminées.

  Ticket [#1848](https://github.com/pgbackrest/pgbackrest/issues/1848); Demande d’intégration [#2802](https://github.com/pgbackrest/pgbackrest/pull/2802); Commit [`a0c1435`](https://github.com/pgbackrest/pgbackrest/commit/a0c14359392e283d88f72e7f9f815d9e78ddfb10)
- Renforcer l'analyse des réponses HTTP chunkées. (*Contribution de Shubham. Révisé par David Steele.*)

  Les extensions de morceaux et les en-têtes de fin sont désormais acceptés, `transfer-encoding` est comparé sans tenir compte de la casse, et une réponse contenant à la fois `transfer-encoding` et `content-length` est rejetée.

  Demande d’intégration [#2785](https://github.com/pgbackrest/pgbackrest/pull/2785); Commit [`34bba82`](https://github.com/pgbackrest/pgbackrest/commit/34bba828c6ba97579d65c2199c02d94bf31257a5)
- Erreur lors de l'exécution en tant que root sauf si `allow-root` est activé. (*Révisé par Douglas J Hunley.*)

  L'exécution d'une commande autre que `restore` en tant que root pouvait créer dans le dépôt des fichiers, comme `backup.info`, auxquels l'utilisateur PostgreSQL n'avait pas accès. `allow-root` est désactivé par défaut pour toutes les commandes sauf `restore`, et la vérification s'applique aussi aux hôtes distants.

  Ticket [#1693](https://github.com/pgbackrest/pgbackrest/issues/1693); Demande d’intégration [#2812](https://github.com/pgbackrest/pgbackrest/pull/2812); Commit [`0daf53d`](https://github.com/pgbackrest/pgbackrest/commit/0daf53da03fb179b5771b6aaa559f9e0cc5842bb)
- Moins de recherches binaires lors de la construction du manifeste. (*Contribution de Gunnar Lindholm. Révisé par David Steele.*)

  La construction du manifeste d'une sauvegarde différentielle ou incrémentale recherchait chaque fichier trois fois dans le manifeste précédent. Elle ne le recherche désormais qu'une fois, ce qui évite des millions de recherches dans les clusters contenant des millions de fichiers.

  Demande d’intégration [#2774](https://github.com/pgbackrest/pgbackrest/pull/2774); Commit [`f1ef629`](https://github.com/pgbackrest/pgbackrest/commit/f1ef62956adabf305a7e959477ea1bb668fd8d65)
- Améliorer les performances de recherche lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par David Christensen, Douglas J Hunley.*)

  Lors d'une restauration delta incrémentale par blocs, chaque bloc écrit provoquait un repositionnement et un vidage du tampon d'écriture ; les blocs font souvent 8KiB. La position dans le fichier est désormais suivie, et le repositionnement et le vidage ne sont effectués que si nécessaire.

  Demande d’intégration [#2732](https://github.com/pgbackrest/pgbackrest/pull/2732); Commit [`b908d5e`](https://github.com/pgbackrest/pgbackrest/commit/b908d5e2c5b37ef968f19e2c40a1001e19e5b87f)
- Regrouper les fichiers de sauvegarde dans l'ordre plutôt que de rechercher un meilleur ajustement. (*Révisé par Stefan Fercot.*)

  Un fichier qui aurait fait dépasser `repo-bundle-size` à un regroupement était écarté au profit d'un fichier plus petit situé plus loin dans la file. Les fichiers sont désormais ajoutés dans l'ordre et le regroupement est fermé lorsqu'il atteint `repo-bundle-size`. Un regroupement peut donc dépasser cette taille de jusqu'à `repo-bundle-limit`.

  Demande d’intégration [#2794](https://github.com/pgbackrest/pgbackrest/pull/2794); Commit [`253dbc3`](https://github.com/pgbackrest/pgbackrest/commit/253dbc3f03e5581c98bb97b252dc77b8defd3693)
- Signaler l'erreur sous-jacente lorsqu'une requête échoue à se terminer. (*Révisé par Andrew Pogrebnoi. Suggéré par Marco Fontana.*)

  Lorsque la connexion était perdue après la remise du premier résultat d'une requête, par exemple sous forte charge, le message générique « NULL result required to complete request » était émis. L'erreur de PostgreSQL est désormais rapportée, avec des indications sur une possible perte de connexion et des valeurs trop agressives de `idle_session_timeout` et `idle_in_transaction_session_timeout`.

  Ticket [#2789](https://github.com/pgbackrest/pgbackrest/issues/2789); Demande d’intégration [#2790](https://github.com/pgbackrest/pgbackrest/pull/2790); Commit [`23e966c`](https://github.com/pgbackrest/pgbackrest/commit/23e966cd8f17a8cd446b04901d0ae66ebf4118ee)
- Signaler l'erreur réelle lorsqu'une requête de crédentials S3 échoue. (*Révisé par Douglas J Hunley. Suggéré par Mitchell Grice.*)

  Une erreur AWS lors d'une demande d'identifiants `web-id` ou `pod-id` était signalée comme un échec d'analyse de la réponse. L'erreur renvoyée par AWS est désormais rapportée, et les jetons sont masqués lorsque la requête est journalisée.

  Ticket [#1997](https://github.com/pgbackrest/pgbackrest/issues/1997); Demande d’intégration [#2808](https://github.com/pgbackrest/pgbackrest/pull/2808); Commit [`b0c57c2`](https://github.com/pgbackrest/pgbackrest/commit/b0c57c280d727e743b72a6d86e2c3e413307e44b)
- Signaler les erreurs de chemin de stockage temporaire `archive-push` dans le journal PostgreSQL. (*Révisé par Douglas J Hunley. Suggéré par Don Seiler.*)

  Lorsque le chemin de spool asynchrone ne pouvait pas être créé, par exemple faute de permission, l'erreur ne pouvait pas être écrite dans le spool et `archive-push` échouait avec un délai d'attente générique renvoyant au journal asynchrone. Le chemin de spool est désormais créé avant le démarrage du processus asynchrone, afin que l'erreur apparaisse dans le journal PostgreSQL.

  Ticket [#1408](https://github.com/pgbackrest/pgbackrest/issues/1408); Demande d’intégration [#2810](https://github.com/pgbackrest/pgbackrest/pull/2810); Commit [`7b0159c`](https://github.com/pgbackrest/pgbackrest/commit/7b0159c7dfd69763b63b1385fd564c18a4a5c1bc)
- Indication que pgBackRest pourrait être obsolète lorsqu'une version n'est plus prise en charge.

  Lorsque pgBackRest ne reconnaît pas une version de PostgreSQL, par exemple si une ancienne version de pgBackRest sur l'hôte de restauration lit la sauvegarde d'un cluster plus récent, l'erreur indique désormais qu'une mise à jour de pgBackRest sur tous les hôtes peut être nécessaire. La version est affichée sous une forme destinée à l'utilisateur, par exemple 13 plutôt que 130000.

  Commit [`d4f697e`](https://github.com/pgbackrest/pgbackrest/commit/d4f697ebce705f9439798f970103fd38f829dfff)
- Ajouter l'intégration avec systemd notify. (*Contribution de Andrew Jackson. Révisé par David Steele.*)

  Lorsqu'il est compilé avec `libsystemd`, le programme `server` signale à systemd qu'il est prêt à accepter des connexions et qu'il s'arrête, comme le font PostgreSQL et PgBouncer.

  Ticket [#2757](https://github.com/pgbackrest/pgbackrest/issues/2757); Demande d’intégration [#2760](https://github.com/pgbackrest/pgbackrest/pull/2760); Commit [`742fff1`](https://github.com/pgbackrest/pgbackrest/commit/742fff174a3f5baaed932afa284334ca2aa1be82)
- Supprimer les erreurs `unused parameter` des sondes du compilateur meson. (*Contribution de Jörg Plate. Révisé par David Steele.*)

  Les tests du compilateur par meson déclaraient des paramètres de `main()` inutilisés, ce qui faisait échouer les tests lorsque les avertissements de paramètres inutilisés étaient traités comme des erreurs.

  Ticket [#2724](https://github.com/pgbackrest/pgbackrest/issues/2724); Commit [`d4465bd`](https://github.com/pgbackrest/pgbackrest/commit/d4465bd6f78d6d58d18ebedbe8f63b55d0ae2508)
- C11 est désormais la norme C minimale. (*Révisé par Mohammad Ali Nazir Kosar.*)

  Demande d’intégration [#2738](https://github.com/pgbackrest/pgbackrest/pull/2738); Commit [`3a6c671`](https://github.com/pgbackrest/pgbackrest/commit/3a6c67183cd9c6a12c24f0d978ef5e501b7c3fcf)

**Améliorations de la documentation :**

- Rendre l'option `stanza` interne pour les commandes `repo-*`. (*Révisé par Stefan Fercot.*)

  L'option `stanza` n'a d'effet sur les commandes `repo-*` qu'avec des constantes de chemin de stockage non documentées ; la documentation laissait donc croire à un effet qu'elle n'avait pas. Cette option n'est plus documentée pour ces commandes et fonctionne comme auparavant.

  Ticket [#2735](https://github.com/pgbackrest/pgbackrest/issues/2735); Commit [`3e9eabd`](https://github.com/pgbackrest/pgbackrest/commit/3e9eabd8a5551cdaeb6bc78a52f000eaf239defb)
- Documenter le fait que les paramètres de chiffrement sont lus à partir de la section globale. (*Révisé par Stefan Fercot. Suggéré par Ron Johnson.*)

  Sans `stanza`, la commande `info` ne lit les paramètres de chiffrement que dans la section globale. Les paramètres de chiffrement configurés pour une stanza nécessitent donc `stanza`.

  Ticket [#1407](https://github.com/pgbackrest/pgbackrest/issues/1407); Demande d’intégration [#2805](https://github.com/pgbackrest/pgbackrest/pull/2805); Commit [`2137bda`](https://github.com/pgbackrest/pgbackrest/commit/2137bda1a5a1ad890d0137feffe8491102041af3)
- Documenter que `expire-auto` utilise la configuration de la commande `backup`. (*Révisé par Stefan Fercot. Suggéré par Lardière Sébastien.*)

  L'expiration automatique après une sauvegarde utilise la configuration de la commande `backup` ; les options définies uniquement pour `expire` ne sont donc pas appliquées. Désactivez `expire-auto` et lancez `expire` séparément lorsque cette commande nécessite sa propre configuration.

  Ticket [#1874](https://github.com/pgbackrest/pgbackrest/issues/1874); Demande d’intégration [#2807](https://github.com/pgbackrest/pgbackrest/pull/2807); Commit [`cf847f9`](https://github.com/pgbackrest/pgbackrest/commit/cf847f94cd7ab6517ec1abb30075fb53dc75d5f8)
- Documenter l'ajustement de la directive `su` de logrotate pour un utilisateur dédié. (*Révisé par Douglas J Hunley. Suggéré par lkanbus.*)

  Les paquets peuvent installer une configuration logrotate qui fait tourner les journaux sous l'utilisateur `postgres`. Si un utilisateur dédié possède le dépôt et les journaux, la directive `su` doit être modifiée pour cet utilisateur, faute de quoi la rotation échoue avec une erreur de permission.

  Ticket [#2737](https://github.com/pgbackrest/pgbackrest/issues/2737); Demande d’intégration [#2809](https://github.com/pgbackrest/pgbackrest/pull/2809); Commit [`bde2c50`](https://github.com/pgbackrest/pgbackrest/commit/bde2c509c923fbe2844c10b0f95c55973378d2ae)
- Documenter que les commentaires se terminant à la fin de ligne ne sont pas pris en charge dans les fichiers de configuration. (*Révisé par Douglas J Hunley. Suggéré par Alex Richman.*)

  Les commentaires de fin de ligne n'ont jamais été pris en charge, même s'ils semblent fonctionner pour certaines options. Seuls les commentaires sur une ligne distincte sont pris en charge.

  Ticket [#1633](https://github.com/pgbackrest/pgbackrest/issues/1633); Demande d’intégration [#2811](https://github.com/pgbackrest/pgbackrest/pull/2811); Commit [`8571799`](https://github.com/pgbackrest/pgbackrest/commit/85717992cadbfdabc571fb23914b62b08c7f6f44)

**Améliorations de la suite de tests :**

- Corriger les conflits de groupes dans les conteneurs CI Alpine. (*Contribution de Artur Zakirov. Révisé par David Steele.*)

  Les entrées de groupe contenant des membres sont désormais prises en compte lors du renommage du groupe de test, et le groupe Alpine n'est créé que s'il n'existe pas déjà.

  Demande d’intégration [#2784](https://github.com/pgbackrest/pgbackrest/pull/2784); Commit [`760dd8d`](https://github.com/pgbackrest/pgbackrest/commit/760dd8db69e7c6e5cbb9c5b7e2067b6813cf4497)

### Notes de version v2.58.0 {#v2580-release-notes}

*Améliorations du stockage objet*

*Sortie le 19 janvier 2026*

**AVERTISSEMENT IMPORTANT** : Les valeurs minimales de l'option `repo-storage-upload-chunk-size` ont augmenté. Elles correspondent désormais au minimum autorisé par les fournisseurs.

**Correctifs de bogues :**

- Corriger un blocage dû à la journalisation dans un gestionnaire de signal. (*Corrigé par Maxim Michkov. Révisé par David Steele.*)

  Un signal reçu alors que `gmtime_r()` détenait un verrou, par exemple le SIGTERM envoyé par `stop` avec `--force`, pouvait provoquer un interblocage lorsque le gestionnaire de signal écrivait dans le journal. Celui-ci n'utilise désormais que des fonctions sûres vis-à-vis des signaux asynchrones pour journaliser.

  Ticket [#2710](https://github.com/pgbackrest/pgbackrest/issues/2710); Demande d’intégration [#2715](https://github.com/pgbackrest/pgbackrest/pull/2715); Commit [`e13c462`](https://github.com/pgbackrest/pgbackrest/commit/e13c462908c6ee25f8795b5d1373981549d4d5cf)

**Fonctionnalités :**

- Prise en charge HTTP pour S3, GCS et Azure. (*Contribution de Will Morland. Révisé par David Steele.*)

  Un point de terminaison de stockage objet peut désormais commencer par `http://` pour établir une connexion sans TLS. HTTPS reste utilisé si aucun protocole n'est précisé.

  Ticket [#2340](https://github.com/pgbackrest/pgbackrest/issues/2340); Demande d’intégration [#2703](https://github.com/pgbackrest/pgbackrest/pull/2703); Commit [`2398dd4`](https://github.com/pgbackrest/pgbackrest/commit/2398dd4d432d312b3641e9fbbcbe0487ad43112d)
- Permettre l'expiration de la sauvegarde complète la plus ancienne, indépendamment de la rétention actuelle. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Ron Johnson.*)

  L'option `--oldest` de `expire` fait expirer la plus ancienne sauvegarde complète et celles qui en dépendent, indépendamment des paramètres de rétention, par exemple lorsque le dépôt manque d'espace. Les WAL précédant la plus ancienne sauvegarde complète restante expirent également.

  Ticket [#2666](https://github.com/pgbackrest/pgbackrest/issues/2666); Demande d’intégration [#2709](https://github.com/pgbackrest/pgbackrest/pull/2709); Commit [`bf2b276`](https://github.com/pgbackrest/pgbackrest/commit/bf2b276dc011464b13039630870934fd42ca473c)
- Prise en charge des identités gérées Azure. (*Contribution de Moiz Ibrar, Matthew Mols. Révisé par David Steele.*)

  Définissez `repo-azure-key-type=auto` pour récupérer automatiquement les identifiants à l'aide d'identités managées plutôt que les configurer. Ils sont renouvelés avant leur expiration.

  Ticket [#2023](https://github.com/pgbackrest/pgbackrest/issues/2023); Demande d’intégration [#2712](https://github.com/pgbackrest/pgbackrest/pull/2712); Commit [`38f14d7`](https://github.com/pgbackrest/pgbackrest/commit/38f14d73b6a62d06e1ead7942e49a2bb2ae90dab)
- Prise en charge ***expérimentale*** de l'identité de pod S3 EKS. (*Contribution de Pierre BOUTELOUP. Révisé par David Steele.*)

  Définissez `repo-s3-key-type=pod-id` pour récupérer automatiquement les identifiants à l'aide de l'identité de pod EKS plutôt que les configurer. Ils sont renouvelés avant leur expiration.

  Ticket [#2718](https://github.com/pgbackrest/pgbackrest/issues/2718); Demande d’intégration [#2719](https://github.com/pgbackrest/pgbackrest/pull/2719); Commit [`79544f6`](https://github.com/pgbackrest/pgbackrest/commit/79544f64a3ce198f4685f923739def997fcafbce)
- Permettre la configuration des suites de chiffrement TLS. (*Contribution de Gunnar "Nick" Bluth. Révisé par David Steele.*)

  Définissez `tls-cipher-12` pour TLS 1.2 et `tls-cipher-13` pour TLS 1.3, par exemple pour répondre à des exigences de conformité. Les suites cryptographiques s'appliquent à toutes les connexions établies par un processus.

  [`fbc607a`](https://github.com/pgbackrest/pgbackrest/commit/fbc607a48b1fb4ae65c9f2691c44453f02aef2b8) Permettre la configuration des suites cryptographiques TLS. ; Ticket [#2697](https://github.com/pgbackrest/pgbackrest/issues/2697); Demande d’intégration [#2700](https://github.com/pgbackrest/pgbackrest/pull/2700)

  [`91ad655`](https://github.com/pgbackrest/pgbackrest/commit/91ad65537f55aa3825b6c7b626a9e1b7cbb1ad4c) Corriger le test unitaire common/io-tls instable ajouté dans fbc607a4.
- Permettre la définition de la priorité du processus. (*Révisé par Douglas J Hunley.*)

  `priority` définit la priorité d'ordonnancement des processus pgBackRest de -20 à 19, comme `nice`. Une valeur plus élevée réduit le risque que pgBackRest perturbe PostgreSQL.

  Demande d’intégration [#2693](https://github.com/pgbackrest/pgbackrest/pull/2693); Commit [`0fc7e96`](https://github.com/pgbackrest/pgbackrest/commit/0fc7e96f5addb01e7f6f3585e37d209cc17dd956)

**Améliorations :**

- Autoriser les points dans les noms de bucket S3 lors de l'utilisation d'URI en style chemin. (*Contribution de Joakim Hindersson. Révisé par David Steele.*)

  Les points dans un nom de bucket ne provoquent une divergence avec le nom d'hôte du certificat qu'avec les URI de type hôte. Ils sont donc désormais autorisés avec `repo-s3-uri-style=path`, utilisé par la plupart des services S3 auto-hébergés.

  Demande d’intégration [#2713](https://github.com/pgbackrest/pgbackrest/pull/2713); Commit [`3fdb4a1`](https://github.com/pgbackrest/pgbackrest/commit/3fdb4a1ea00b442aca5fc714818d293d57490386)
- Exiger TLS >= 1.2 sauf si la vérification est désactivée. (*Révisé par Douglas J Hunley, Gunnar "Nick" Bluth.*)

  TLS 1.0 et 1.1 sont obsolètes depuis 2021. La vérification est toujours activée pour les connexions entre hôtes pgBackRest. Lorsque la vérification est désactivée pour un stockage objet avec `repo-storage-verify-tls`, par exemple pour un certificat autosigné, toutes les versions du protocole sont autorisées.

  Demande d’intégration [#2720](https://github.com/pgbackrest/pgbackrest/pull/2720); Commit [`5b4b20a`](https://github.com/pgbackrest/pgbackrest/commit/5b4b20a8d7d17c2bffe106595310853e3f3a9604)
- Ajuster dynamiquement la taille des morceaux S3/GCS/Azure pour les téléversements volumineux. (*Révisé par Douglas J Hunley. Suggéré par Timothée Peignier.*)

  Le nombre de morceaux d'un envoi étant limité, la valeur par défaut de `repo-storage-upload-chunk-size` limitait la taille maximale des fichiers à 50GiB sur S3, 40GiB sur GCS et 200GiB sur Azure. La taille des morceaux augmente désormais pendant l'envoi, ce qui permet d'envoyer des fichiers jusqu'à 5TiB vers S3 et GCS et jusqu'à 45TiB vers Azure.

  Ticket [#2679](https://github.com/pgbackrest/pgbackrest/issues/2679); Demande d’intégration [#2701](https://github.com/pgbackrest/pgbackrest/pull/2701); Commit [`86554fa`](https://github.com/pgbackrest/pgbackrest/commit/86554faa707292855c2776a0c70b5e212b1e3945)
- Optimiser la taille des morceaux S3/GCS/Azure pour les petits fichiers. (*Révisé par Douglas J Hunley.*)

  Tout le tampon de morceau était alloué à l'ouverture d'un fichier, même si de nombreux fichiers sont plus petits qu'un morceau. Le tampon grandit désormais à mesure que les données arrivent, ce qui économise de la mémoire lors de l'envoi de petits fichiers.

  Demande d’intégration [#2705](https://github.com/pgbackrest/pgbackrest/pull/2705); Commit [`28bfa20`](https://github.com/pgbackrest/pgbackrest/commit/28bfa20ba3b860f72ba7ab6c018e37ada99e2109)
- Supprimer le support de PostgreSQL `9.5`. (*Révisé par Douglas J Hunley.*)

  PostgreSQL 9.5 n'est plus pris en charge, conformément à la politique consistant à prendre en charge cinq versions de PostgreSQL arrivées en fin de vie.

  Demande d’intégration [#2692](https://github.com/pgbackrest/pgbackrest/pull/2692); Commit [`5171e8b`](https://github.com/pgbackrest/pgbackrest/commit/5171e8bde31b9711c9c5b4ccc5170b61c5235548)
- Améliorer la journalisation de la valeur par défaut pour les options ayant une dépendance non résolue. (*Révisé par Stefan Fercot.*)

  Une option définie dans le fichier de configuration était journalisée au début d'une commande lorsque sa dépendance n'était pas satisfaite, alors que sa valeur par défaut était utilisée. L'option n'est plus journalisée dans ce cas.

  Ticket [#2707](https://github.com/pgbackrest/pgbackrest/issues/2707); Demande d’intégration [#2708](https://github.com/pgbackrest/pgbackrest/pull/2708); Commit [`38ac638`](https://github.com/pgbackrest/pgbackrest/commit/38ac6387cbbfc6f78a686de657e5a4de4ed59295)

**Améliorations de la documentation :**

- Supprimer la configuration explicite `max_wal_senders`/`wal_level` du guide utilisateur. (*Suggéré par Jamie Nguyen.*)

  Depuis PostgreSQL 10, les valeurs par défaut de `max_wal_senders` et `wal_level` sont celles requises par le guide utilisateur.

  Ticket [#2699](https://github.com/pgbackrest/pgbackrest/issues/2699); Commit [`bce97d3`](https://github.com/pgbackrest/pgbackrest/commit/bce97d3ea80675b8eab3dbf692e8bc8f077f30c7)
- Préciser que le regroupement est utile pour les systèmes de fichiers à grandes tailles de bloc. (*Suggéré par Ron Johnson.*)

  Le regroupement économise de l'espace sur les systèmes de fichiers à grands blocs, où chaque petit fichier occupe un bloc entier.

  Ticket [#2706](https://github.com/pgbackrest/pgbackrest/issues/2706); Commit [`a7e5f28`](https://github.com/pgbackrest/pgbackrest/commit/a7e5f28511c27f2504a873db26803b26a84df8f1)

### Notes de version v2.57.0 {#v2570-release-notes}

*Supprimer les liens symboliques du dépôt*

*Sortie le 18 octobre 2025*

**Correctifs de bogues :**

- Décongestionner les délais d'attente HTTP/TLS/socket. (*Révisé par David Christensen.*)

  Une connexion de socket en échec était également réessayée par les couches TLS et HTTP. Avec le `io-timeout` par défaut de 60 secondes, une connexion mettait donc neuf minutes à expirer. Chaque couche ne réessaie désormais que ses propres échecs.

  Ticket [#2654](https://github.com/pgbackrest/pgbackrest/issues/2654); Demande d’intégration [#2662](https://github.com/pgbackrest/pgbackrest/pull/2662); Commit [`9c7f064`](https://github.com/pgbackrest/pgbackrest/commit/9c7f0648648e651d82918e5dbfc3d511abee3298)
- Corriger un éventuel plantage dans le message d'erreur de somme de contrôle de page. (*Corrigé par Zsolt Parragi. Révisé par David Steele.*)

  Le message d'erreur des sommes de contrôle de pages invalides utilisait une chaîne hors de sa portée, ce qui pouvait journaliser des données incohérentes ou provoquer un plantage. Cela se produisait surtout avec pg_tde, puisque tous les fichiers chiffrés échouent à la vérification des sommes de contrôle des pages.

  Demande d’intégration [#2675](https://github.com/pgbackrest/pgbackrest/pull/2675); Commit [`adc5e5b`](https://github.com/pgbackrest/pgbackrest/commit/adc5e5b23b9b544745724a7eaa0461b88b691e36)
- Correction d'une possible erreur de segmentation dans les messages de reprise de sauvegarde.

  Le message indiquant pourquoi une sauvegarde ne peut pas être reprise utilisait une chaîne hors de sa portée, ce qui pouvait journaliser des données incohérentes ou provoquer un plantage.

  Commit [`c1c40a4`](https://github.com/pgbackrest/pgbackrest/commit/c1c40a4a851efe98be83aca2044c02fd1c7fb2ae)

**Fonctionnalités :**

- Ajouter l'option `repo-symlink` pour supprimer la création des liens symboliques du dépôt. (*Révisé par Douglas J Hunley. Suggéré par Ron Johnson.*)

  Certains systèmes de fichiers par ailleurs compatibles Posix ne prennent pas en charge les liens symboliques. Définissez `repo-symlink=n` pour empêcher la création des liens symboliques `latest` et des tablespaces dans le dépôt.

  Ticket [#2673](https://github.com/pgbackrest/pgbackrest/issues/2673); Demande d’intégration [#2674](https://github.com/pgbackrest/pgbackrest/pull/2674); Commit [`bfd9790`](https://github.com/pgbackrest/pgbackrest/commit/bfd97907311a25ed239798691cff52cf73acdb83)

**Améliorations :**

- Ajouter des tentatives HTTP pour les erreurs 408 et 429. (*Révisé par David Christensen.*)

  Les erreurs HTTP 408 (Request Timeout) et 429 (Too Many Requests) sont désormais réessayées. Les erreurs 429 sont courantes sur Cloudflare R2.

  Demande d’intégration [#2661](https://github.com/pgbackrest/pgbackrest/pull/2661); Commit [`8733900`](https://github.com/pgbackrest/pgbackrest/commit/87339004e59c03d2a03a6ceb8426202346849c37)

### Notes de version v2.56.0 {#v2560-release-notes}

*Améliorations des informations de progression*

*Sortie le 21 juillet 2025*

**Correctifs de bogues :**

- Corriger le problème d'expiration à la demande lorsque aucune sauvegarde n'est présente dans un dépôt. (*Révisé par Stefan Fercot. Signalement par Anup Gupta.*)

  L'expiration ponctuelle échouait avec « cannot get index 0 from list with 0 value(s) » lorsqu'un dépôt ne contenait aucune sauvegarde.

  Ticket [#2645](https://github.com/pgbackrest/pgbackrest/issues/2645); Demande d’intégration [#2646](https://github.com/pgbackrest/pgbackrest/pull/2646); Commit [`638815b`](https://github.com/pgbackrest/pgbackrest/commit/638815b4cde1ba1322516e256742c51676af66f0)

**Fonctionnalités :**

- Ajouter la progression de la restauration à la sortie de la commande `info`. (*Contribution de Denis Garsh, Maxim Michkov. Révisé par David Steele.*)

  La commande `restore` enregistre désormais sa progression, que `info` affiche aux côtés de celle des sauvegardes. Une restauration n'est plus non plus interrompue par la commande `stop`.

  Ticket [#2546](https://github.com/pgbackrest/pgbackrest/issues/2546); Demande d’intégration [#2652](https://github.com/pgbackrest/pgbackrest/pull/2652); Commit [`8cdd9ce`](https://github.com/pgbackrest/pgbackrest/commit/8cdd9ce1c4ab6cca508932a41a3013374d7547ef)
- Ajouter le niveau de détail « progression uniquement » à la sortie de la commande `info`. (*Contribution de Denis Garsh. Révisé par David Steele, Stefan Fercot.*)

  Définissez `--detail-level=progress` pour n'afficher que la progression. Cela est plus rapide, car le dépôt n'est pas lu. La valeur par défaut est `full`.

  Demande d’intégration [#2550](https://github.com/pgbackrest/pgbackrest/pull/2550); Commit [`2706168`](https://github.com/pgbackrest/pgbackrest/commit/2706168f609af544b0453d384c7fb620626fc205)

**Améliorations :**

- Réessayer les lectures échouées sur les magasins d'objets. (*Révisé par David Christensen.*)

  Une lecture depuis un stockage objet qui échouait après avoir commencé était fatale, ce qui pouvait imposer de recommencer une tâche coûteuse, par exemple lors d'une restauration. Une lecture en échec est désormais reprise à l'endroit où elle s'est arrêtée.

  Demande d’intégration [#2642](https://github.com/pgbackrest/pgbackrest/pull/2642); Commit [`5e14692`](https://github.com/pgbackrest/pgbackrest/commit/5e14692588b9fd8a566c9a1795c866ba2e83eebd)
- Corriger les valeurs par défaut dans l'aide en ligne de commande. (*Révisé par David Christensen, Chris Bandy.*)

  Lorsqu'une option a plusieurs valeurs par défaut, comme `repo-storage-upload-chunk-size` avec un dépôt S3 et un dépôt Azure, la liste des options affiche `<multi>` et l'aide de l'option énumère chaque valeur par défaut. Les valeurs par défaut des options non valides dans la configuration courante ne sont pas affichées.

  Demande d’intégration [#2625](https://github.com/pgbackrest/pgbackrest/pull/2625); Commit [`8737cad`](https://github.com/pgbackrest/pgbackrest/commit/8737cad566974c37529595715ecdc06571420752)

**Améliorations de la documentation :**

- Décrivez les valeurs d'option discrètes sous forme de liste lorsque cela est approprié. (*Contribution de Anton Kurochkin. Révisé par David Steele.*)

  Les valeurs d'options comme `output` pour les commandes `verify` et `version` sont désormais présentées sous forme de liste, comme pour les autres options.

  Demande d’intégration [#2638](https://github.com/pgbackrest/pgbackrest/pull/2638); Commit [`2e76e9f`](https://github.com/pgbackrest/pgbackrest/commit/2e76e9fc699d22286f6bf05fddc271d8fa22523e)
- Corrigez « inférieur à » dans la sortie d'aide pour l'option `archive-mode`. (*Contribution de Anton Kurochkin. Révisé par David Steele.*)

  Demande d’intégration [#2633](https://github.com/pgbackrest/pgbackrest/pull/2633); Commit [`cb67322`](https://github.com/pgbackrest/pgbackrest/commit/cb673225e90604a8865ce30c188d15661f945e5e)

### Notes de version v2.55.1 {#v2551-release-notes}

*Correctifs de bogues*

*Sortie le 5 mai 2025*

**Correctifs de bogues :**

- Annuler « calculer le content-md5 sur S3 uniquement lorsqu'il est nécessaire ». (*Révisé par David Christensen. Signalement par Frank Brendel.*)

  Lorsque le verrouillage d'objets est activé, S3 exige soit `content-md5`, soit une somme de contrôle `x-amz-content-*` pour les envois. Scality n'acceptant pas les autres sommes de contrôle, les envois échouaient. `content-md5` est de nouveau calculé pour toutes les requêtes avec contenu.

  Ticket [#2613](https://github.com/pgbackrest/pgbackrest/issues/2613); Demande d’intégration [#2615](https://github.com/pgbackrest/pgbackrest/pull/2615); Commit [`8bbb982`](https://github.com/pgbackrest/pgbackrest/commit/8bbb98243566bfa052f6aacfd1bd3a6acd770e40)
- Corriger la vérification des bornes inférieures pour les clés d'option. (*Révisé par David Christensen, Wolfgang Walther. Signalement par Wolfgang Walther.*)

  Une option indexée avec une clé de 0, par exemple `pg0-path`, provoquait une erreur de segmentation. Elle produit désormais une erreur.

  Ticket [#2610](https://github.com/pgbackrest/pgbackrest/issues/2610); Demande d’intégration [#2611](https://github.com/pgbackrest/pgbackrest/pull/2611); Commit [`5e01098`](https://github.com/pgbackrest/pgbackrest/commit/5e01098617a3803067b153be2d41e023cd4d95e4)

### Notes de version v2.55.0 {#v2550-release-notes}

*Améliorations de vérification et prise en charge de PostgreSQL 18*

*Sortie le 21 avril 2025*

**Correctifs de bogues :**

- Corriger le problème de restauration incrémentielle par bloc sur un dépôt non par défaut. (*Révisé par David Christensen. Testé par Aleksander Łukasz. Signalement par Aleksander Łukasz.*)

  Lorsque la sauvegarde à restaurer était incrémentale par blocs et ne se trouvait pas dans le dépôt portant le plus petit numéro, la restauration lisait une partie des données incrémentales par blocs depuis ce dernier. Définir `repo` permettait de contourner le problème.

  Ticket [#2577](https://github.com/pgbackrest/pgbackrest/issues/2577); Demande d’intégration [#2579](https://github.com/pgbackrest/pgbackrest/pull/2579); Commit [`5d2c67c`](https://github.com/pgbackrest/pgbackrest/commit/5d2c67c3c6975ea3ed08c7425f6e410ae378913f)
- Ne pas définir `recovery_target_timeline=current` pour PostgreSQL < 12. (*Révisé par Stefan Fercot.*)

  Avant PostgreSQL 12, définir explicitement `recovery_target_timeline` sur `current` produit le comportement de `latest`, bien que `current` soit la valeur par défaut. Pour ces versions, le paramètre est désormais omis de `recovery.conf` lorsqu'il vaut `current`.

  Demande d’intégration [#2533](https://github.com/pgbackrest/pgbackrest/pull/2533); Commit [`6fbb28f`](https://github.com/pgbackrest/pgbackrest/commit/6fbb28fa2d615576be78376c7f539921f6b8bc6a)
- Corriger la journalisation de la plage d'archives expirées. (*Révisé par Stefan Fercot. Signalement par Aleš Zelený.*)

  Seul le dernier chemin d'archive supprimé était journalisé comme début de la plage. Le journal laissait donc penser que bien moins de fichiers avaient expiré qu'en réalité.

  Ticket [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Demande d’intégration [#2554](https://github.com/pgbackrest/pgbackrest/pull/2554); Commit [`47f050f`](https://github.com/pgbackrest/pgbackrest/commit/47f050f8fd816e57326d881f4253d8a13c0f8da6)
- Corriger le rapport d'erreur pour les requêtes sans résultat. (*Révisé par Stefan Fercot. Signalement par Susantha Bathige.*)

  Une erreur provenant d'une requête censée ne renvoyer aucun résultat était signalée comme un résultat inattendu, au lieu de rapporter l'erreur.

  Demande d’intégration [#2539](https://github.com/pgbackrest/pgbackrest/pull/2539); Commit [`d5cefb7`](https://github.com/pgbackrest/pgbackrest/commit/d5cefb7290c34c64a2b9aa89ff04a718df4ec18b)

**Fonctionnalités :**

- Vérifier le timeline cible de la récupération. (*Révisé par Stefan Fercot.*)

  Une sauvegarde incapable de suivre la timeline cible, par exemple réalisée après la promotion d'un serveur de secours et la bifurcation de la nouvelle timeline, n'échouait qu'au début de la récupération, avec une erreur PostgreSQL difficile à interpréter. La timeline est désormais vérifiée à l'aide des fichiers d'historique avant le début de la restauration.

  Demande d’intégration [#2534](https://github.com/pgbackrest/pgbackrest/pull/2534); Commit [`922e9f0`](https://github.com/pgbackrest/pgbackrest/commit/922e9f0775c39b64e009251a6bec8ef9b83c190f)
- Permettre la vérification d'une sauvegarde spécifiée. (*Contribution de Maxim Michkov. Révisé par David Steele.*)

  L'option `--set` de `verify` ne vérifie que la sauvegarde indiquée et les WAL nécessaires pour la rendre cohérente.

  Ticket [#2419](https://github.com/pgbackrest/pgbackrest/issues/2419); Demande d’intégration [#2544](https://github.com/pgbackrest/pgbackrest/pull/2544); Commit [`e4def88`](https://github.com/pgbackrest/pgbackrest/commit/e4def8845eb5c3fe9fb8cc44d9f64766cfb348c2)
- Ajouter la prise en charge de « requester pays » (paiement par le demandeur) pour S3/GCS. (*Contribution de Timothée Peignier. Révisé par David Steele.*)

  Définissez `repo-s3-requester-pays` ou `repo-gcs-user-project` pour facturer le demandeur plutôt que le propriétaire du bucket, par exemple afin qu'un service hébergé puisse donner à ses clients accès à leurs sauvegardes.

  [`4db0263`](https://github.com/pgbackrest/pgbackrest/commit/4db0263fd63274a8168eb4de17b320d2f86251a2) Ajouter la prise en charge de Requester Pays pour S3. ; Demande d’intégration [#2560](https://github.com/pgbackrest/pgbackrest/pull/2560)

  [`814bf48`](https://github.com/pgbackrest/pgbackrest/commit/814bf487c3955e877d226faaa22324d3c79863b2) Ajouter la prise en charge de Requester Pays pour GCS. ; Demande d’intégration [#2557](https://github.com/pgbackrest/pgbackrest/pull/2557)
- Prise en charge de PostgreSQL 18. (*Révisé par Stefan Fercot.*)

  Cette version a été publiée avant l'existence d'une bêta de PostgreSQL 18 ; sa prise en charge était donc initialement expérimentale. Aucun changement affectant pgBackRest n'est intervenu avant PostgreSQL 18.0.

  Demande d’intégration [#2603](https://github.com/pgbackrest/pgbackrest/pull/2603); Commit [`565d2e0`](https://github.com/pgbackrest/pgbackrest/commit/565d2e0c47cd21df890a40b3a94a8c865bed76d9)
- Permettre les connexions à PostgreSQL via des sockets de domaine abstraits. (*Testé par Chris Bandy. Suggéré par Chris Bandy.*)

  `pg-socket-path` n'a plus besoin d'être un chemin absolu et peut donc désigner un socket de domaine abstrait. libpq rapporte un chemin non valide.

  Ticket [#2529](https://github.com/pgbackrest/pgbackrest/issues/2529); Demande d’intégration [#2535](https://github.com/pgbackrest/pgbackrest/pull/2535); Commit [`68f22ae`](https://github.com/pgbackrest/pgbackrest/commit/68f22aea6665b9dcbe76dbfaa731f37187e1ce20)
- Ajouter une sortie numérique à la commande `version`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Définissez `--output=num` pour afficher la version sous forme numérique, par exemple 2055000, plus facile à comparer.

  Ticket [#2410](https://github.com/pgbackrest/pgbackrest/issues/2410); Demande d’intégration [#2526](https://github.com/pgbackrest/pgbackrest/pull/2526); Commit [`750a051`](https://github.com/pgbackrest/pgbackrest/commit/750a051b7aeccc3dd7ae9c07af2c73cb25057de9)

**Améliorations :**

- Autoriser la commande de sauvegarde à fonctionner sur des dépôts distants. (*Révisé par Stefan Fercot.*)

  La commande `backup` peut désormais s'exécuter sur un hôte dont le dépôt est distant, ce qui offre davantage de souplesse dans le choix de l'hôte de sauvegarde.

  [`4a94b6b`](https://github.com/pgbackrest/pgbackrest/commit/4a94b6bef9108ab775c0070571a1fb7dd8883eeb) Refactoriser l'assistant de protocole.

  [`931435c`](https://github.com/pgbackrest/pgbackrest/commit/931435c0177ded2189903385d520d5c8819c4f5e) Permettre à la commande backup de fonctionner sur des dépôts distants. ; Demande d’intégration [#2512](https://github.com/pgbackrest/pgbackrest/pull/2512)
- Utiliser lz4 pour la compression du protocole. (*Révisé par Stefan Fercot.*)

  lz4 compresse bien plus vite que gz et offre des taux similaires aux niveaux faibles utilisés pour la compression du protocole. Définir `compress-level-network=0` ne désactive plus la compression du protocole.

  [`0577b03`](https://github.com/pgbackrest/pgbackrest/commit/0577b0301689bc19d49c4081cc652971de5da8cf) Utiliser lz4 pour la compression du protocole. ; Demande d’intégration [#2488](https://github.com/pgbackrest/pgbackrest/pull/2488)

  [`5c8296d`](https://github.com/pgbackrest/pgbackrest/commit/5c8296df066564be35d3936610ebff1c332f38da) Supprimer de la documentation la référence à la désactivation de la compression réseau.
- Calculer `content-md5` sur S3 uniquement lorsqu'il est nécessaire. (*Révisé par David Christensen.*)

  L'en-tête `content-md5` n'est calculé que pour les requêtes de suppression par lot, qui l'exigent, afin d'économiser du processeur lors des envois de fichiers. Ce changement a été annulé dans la v2.55.1.

  Demande d’intégration [#2592](https://github.com/pgbackrest/pgbackrest/pull/2592); Commit [`20bfd14`](https://github.com/pgbackrest/pgbackrest/commit/20bfd14b73ad6d75b6fb1169565b18dcfa183c9b)
- Afficher un avertissement lorsque la valeur d'une option à plusieurs clés est remplacée. (*Révisé par David Christensen, Stefan Fercot.*)

  Les options à paires clé/valeur, comme `recovery-option`, écrasaient silencieusement une valeur lorsque sa clé était spécifiée à nouveau. Un avertissement est désormais journalisé.

  Ticket [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Demande d’intégration [#2594](https://github.com/pgbackrest/pgbackrest/pull/2594); Commit [`cab4d6f`](https://github.com/pgbackrest/pgbackrest/commit/cab4d6fd5c775d6e1a9cd9889d825eee667b5322)
- Ajouter un journal détaillé pour le chemin d'archive expiré. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  La suppression d'un grand nombre de fichiers d'archive pouvait donner l'impression d'un blocage. Un message au niveau de détail affiche désormais la progression.

  [`4dcfa9e`](https://github.com/pgbackrest/pgbackrest/commit/4dcfa9ef59c5e75c6c0ee83390c64b9a3d4af1fc) Ajouter la journalisation détaillée au test d'expiration.

  [`2155a12`](https://github.com/pgbackrest/pgbackrest/commit/2155a12a3d861645de5618518350f90962fbc26d) Ajouter une journalisation détaillée du chemin d'archive expiré. ; Ticket [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Demande d’intégration [#2559](https://github.com/pgbackrest/pgbackrest/pull/2559)
- Supprimer le support de PostgreSQL `9.4`. (*Révisé par Stefan Fercot.*)

  PostgreSQL 9.4 n'est plus pris en charge, conformément à la politique de prise en charge de cinq versions de PostgreSQL arrivées en fin de vie. Les sauvegardes de clusters 9.4 peuvent toujours être supprimées par expiration.

  Demande d’intégration [#2472](https://github.com/pgbackrest/pgbackrest/pull/2472); Commit [`48f511d`](https://github.com/pgbackrest/pgbackrest/commit/48f511dad339ef9357e00f7bd8e2bf4b7c800dd4)
- Supprimer la construction autoconf/make. (*Révisé par David Christensen.*)

  La v2.54.0 était la dernière version prenant en charge la compilation avec autoconf/make. Utilisez meson pour compiler.

  Demande d’intégration [#2470](https://github.com/pgbackrest/pgbackrest/pull/2470); Commit [`89c9bab`](https://github.com/pgbackrest/pgbackrest/commit/89c9baba72fc99616083a7adc4be2c3e2bf9e4dd)

**Améliorations de la documentation :**

- Corriger la documentation concernant la spécification de plusieurs stanzas avec `tls-server-auth`. (*Révisé par David Christensen, Stefan Fercot. Suggéré par Terry MacAndrew.*)

  Pour `tls-server-auth`, plusieurs stanzas se spécifient dans une liste séparée par des virgules. La documentation indiquait de répéter l'option.

  Ticket [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Demande d’intégration [#2595](https://github.com/pgbackrest/pgbackrest/pull/2595); Commit [`53a45d2`](https://github.com/pgbackrest/pgbackrest/commit/53a45d25c3e60e5067010b2676f5d6216638fbe3)
- Préciser la durée de validité des sauvegardes incrémentielles. (*Révisé par Stefan Fercot.*)

  La documentation laissait entendre que les sauvegardes incrémentales expiraient selon un nombre à conserver. Elle explique désormais leur expiration et précise que les sauvegardes complètes comptent comme des sauvegardes différentielles pour la rétention différentielle.

  Demande d’intégration [#2601](https://github.com/pgbackrest/pgbackrest/pull/2601); Commit [`8bdba74`](https://github.com/pgbackrest/pgbackrest/commit/8bdba747981e8805a9bf355050f70cdf19e9babc)
- Préciser la condition de correspondance des versions locales/distantes de pgBackRest. (*Contribution de Greg Clough. Révisé par David Steele.*)

  Ticket [#2540](https://github.com/pgbackrest/pgbackrest/issues/2540); Demande d’intégration [#2541](https://github.com/pgbackrest/pgbackrest/pull/2541); Commit [`82299eb`](https://github.com/pgbackrest/pgbackrest/commit/82299eb4cd997524eeddef170ad99669ed6651cf)
- Ajouter une question fréquente sur l'exportation d'un cluster auto-contenu. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  La FAQ explique comment créer un export autonome d'un cluster à partir d'une sauvegarde effectuée avec `--archive-copy` et restaurée avec `--type=none`.

  Demande d’intégration [#2605](https://github.com/pgbackrest/pgbackrest/pull/2605); Commit [`9386920`](https://github.com/pgbackrest/pgbackrest/commit/9386920b79971347c6c57589190bf09b591d8b4d)
- Mise en garde concernant `--tablespace-map-all` au sujet de la création de tablespaces. (*Révisé par Stefan Fercot, Christophe Courtois. Suggéré par Christophe Courtois.*)

  Un tablespace créé après le début de la sauvegarde n'est pas dans le manifeste ; `tablespace-map-all` ne peut donc pas le remapper.

  Demande d’intégration [#2538](https://github.com/pgbackrest/pgbackrest/pull/2538); Commit [`e625ed8`](https://github.com/pgbackrest/pgbackrest/commit/e625ed8be2228cb99c3801f9d1776909a2201c5a)
- Préciser le comportement de `--repo-retention-full-type`. (*Révisé par Antoine Beaupré. Suggéré par Antoine Beaupré.*)

  Ticket [#2562](https://github.com/pgbackrest/pgbackrest/issues/2562); Demande d’intégration [#2583](https://github.com/pgbackrest/pgbackrest/pull/2583); Commit [`84eb9a7`](https://github.com/pgbackrest/pgbackrest/commit/84eb9a742dcf75f071e011946263dedaa985099e)
- Modifier la recommandation concernant les magasins d'objets de `--process-max` à `--repo-bundle`. (*Révisé par Stefan Fercot.*)

  Sur les stockages objet, `repo-bundle` réduit bien davantage le temps de création des fichiers que `process-max`, car moins de fichiers sont créés.

  Demande d’intégration [#2542](https://github.com/pgbackrest/pgbackrest/pull/2542); Commit [`aa7210a`](https://github.com/pgbackrest/pgbackrest/commit/aa7210a1830825e0a3e6b6740937357341127a6f)
- Mettre à jour `unix_socket_directory` vers `unix_socket_directories`. (*Contribution de hyunkyu han. Révisé par David Steele.*)

  `unix_socket_directory` n'est plus valide depuis PostgreSQL 9.2 ; seul `unix_socket_directories` est donc documenté.

  Ticket [#2589](https://github.com/pgbackrest/pgbackrest/issues/2589); Commit [`b28ae98`](https://github.com/pgbackrest/pgbackrest/commit/b28ae98cec7ae7e881e6476c1cba1ba7e1abc358)
- Ne pas placer `spool-path` dans `pg_xlog`/`pg_wal`. (*Révisé par Martín Marqués, Don Seiler. Suggéré par Martín Marqués.*)

  Un chemin de spool situé dans `pg_xlog` ou `pg_wal` peut perturber des outils PostgreSQL comme `pg_rewind`.

  Demande d’intégration [#2600](https://github.com/pgbackrest/pgbackrest/pull/2600); Commit [`dd3a7d9`](https://github.com/pgbackrest/pgbackrest/commit/dd3a7d99a78d0d604967d90e8a8dbf8915432896)

### Notes de version v2.54.2 {#v2542-release-notes}

*Correction de bogue*

*Sortie le 20 janvier 2025*

**Correctifs de bogues :**

- Corriger le problème survenu après avoir désactivé le regroupement avec l'incrémentation par bloc activée. (*Révisé par David Christensen.*)

  Lorsque le regroupement était désactivé après des sauvegardes effectuées avec regroupement et incrémental par blocs, les sauvegardes précédentes devenaient illisibles. Le paramètre nécessaire à leur lecture est désormais conservé.

  Demande d’intégration [#2511](https://github.com/pgbackrest/pgbackrest/pull/2511); Commit [`dbc6f28`](https://github.com/pgbackrest/pgbackrest/commit/dbc6f2875356ec16cf4883830a0d7b00204752ee)

**Améliorations de la documentation :**

- Préciser le comportement des fichiers de configuration multiples. (*Révisé par Paul Bierly. Suggéré par Paul Bierly.*)

  Chaque fichier de configuration doit être valide indépendamment des autres. Une section doit donc être spécifiée dans chaque fichier qui y définit une option. La documentation précise aussi que les guillemets ne sont pas pris en charge, que les espaces en bordure des clés et valeurs sont supprimés et que les sections répétées sont fusionnées.

  Commit [`5da2df4`](https://github.com/pgbackrest/pgbackrest/commit/5da2df4a933f04d5fb9a3b6c7c59529f3afa805b)

### Notes de version v2.54.1 {#v2541-release-notes}

*Correction de bogue*

*Sortie le 16 décembre 2024*

**Correctifs de bogues :**

- Corriger le problème lié aux commandes `version`/`help` qui tentaient de charger `pgbackrest.conf`. (*Révisé par Stefan Fercot. Signalement par Bradford Boyle, Julian.*)

  Dans la v2.54.0, les commandes `version` et `help` chargeaient `pgbackrest.conf` et échouaient si ce fichier ne pouvait pas être lu ou analysé.

  Ticket [#2476](https://github.com/pgbackrest/pgbackrest/issues/2476); Demande d’intégration [#2477](https://github.com/pgbackrest/pgbackrest/pull/2477); Commit [`8d69118`](https://github.com/pgbackrest/pgbackrest/commit/8d6911898afd75c586ef70c6d8559b1e5959a155)

**Améliorations de la suite de tests :**

- Stabiliser l'archivage asynchrone dans les tests d'intégration. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)

  Un `archive-get` asynchrone laissé en cours d'exécution par un test d'intégration pouvait écrire une erreur dans la file du test suivant et faire échouer sa récupération.

  Ticket [#2463](https://github.com/pgbackrest/pgbackrest/issues/2463); Demande d’intégration [#2481](https://github.com/pgbackrest/pgbackrest/pull/2481); Commit [`b90ce9e`](https://github.com/pgbackrest/pgbackrest/commit/b90ce9eb8c7cd9e9b131477a377249a3d3fda181)

### Notes de version v2.54.0 {#v2540-release-notes}

*Instant cible pour le stockage versionné*

*Sortie le 21 octobre 2024*

**NOTE AUX PAQUETEURS** : Cette version est la dernière à prendre en charge la construction autoconf/make. Veuillez migrer vers meson si ce n’est pas déjà fait. Les correctifs de version 2.54.X (le cas échéant) continueront à prendre en charge autoconf/make.

**Correctifs de bogues :**

- Corriger les performances des requêtes PostgreSQL sur de grands jeux de données. (*Corrigé par Thibault Vincent, David Steele. Révisé par David Christensen. Testé par Antoine Millet. Signalement par Antoine Millet.*)

  La logique de délai d'attente des requêtes retardait la lecture des résultats. Une requête renvoyant un grand résultat pouvait donc prendre jusqu'à `db-timeout`. Les résultats sont désormais lus dès qu'ils sont disponibles.

  [`6ac4e8d`](https://github.com/pgbackrest/pgbackrest/commit/6ac4e8dd78f16e93300f7747c4bc8fa8e1a0558b) Déplacer le substitut du module fd vers le test du module io.

  [`77ae753`](https://github.com/pgbackrest/pgbackrest/commit/77ae753ef59bd40b9867be21e8519093786c3b85) Permettre au substitut de fdReady() de s'exécuter une seule fois avec une valeur de retour donnée.

  [`33fa396`](https://github.com/pgbackrest/pgbackrest/commit/33fa3965616b1432e5d1d59c489302fa4891a39e) Refactoriser l'objet Wait pour exposer le temps d'attente restant via waitRemains().

  [`c8ccaaa`](https://github.com/pgbackrest/pgbackrest/commit/c8ccaaa755993e3fd5e87148bd0a991acb3050c3) Corriger les performances des requêtes PostgreSQL pour les grands jeux de données. ; Ticket [#2458](https://github.com/pgbackrest/pgbackrest/issues/2458); Demande d’intégration [#2459](https://github.com/pgbackrest/pgbackrest/pull/2459)

**Fonctionnalités :**

- Autorise la lecture des dépôts sur un stockage versionné à un instant cible. (*Révisé par Stefan Fercot, David Christensen.*)

  Les commandes `archive-get`, `info`, `repo-get`, `repo-ls`, `restore` et `verify` peuvent lire un dépôt sur stockage Azure, GCS ou S3 versionné tel qu'il était à `repo-target-time`. Cela permet une récupération même si le dépôt a été supprimé ou corrompu, accidentellement ou par malveillance.

  Demande d’intégration [#2404](https://github.com/pgbackrest/pgbackrest/pull/2404); Commit [`b19134d`](https://github.com/pgbackrest/pgbackrest/commit/b19134dccd5d0dab87b5d45b443f481df00370b1)
- Autorise l'exécution de la sauvegarde demandée depuis un serveur secondaire, même en l'absence de serveur secondaire. (*Révisé par Stefan Fercot.*)

  Définissez `backup-standby=prefer` pour sauvegarder depuis un serveur de secours s'il est disponible, sinon depuis le primaire. Cela n'aide pas si le serveur de secours répond mais ne parvient pas à se synchroniser avec le primaire après le début de la sauvegarde.

  Demande d’intégration [#2378](https://github.com/pgbackrest/pgbackrest/pull/2378); Commit [`a42629f`](https://github.com/pgbackrest/pgbackrest/commit/a42629f87ab70ffaee8d1241eb50c5ea7154a87d)

**Améliorations :**

- Résumer la liste de référence des sauvegardes dans la sortie texte de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  La liste des références de sauvegarde pouvant être très longue, la sortie texte de `info` en donne désormais un résumé. La liste complète est affichée avec `--set`.

  Demande d’intégration [#2399](https://github.com/pgbackrest/pgbackrest/pull/2399); Commit [`b306f83`](https://github.com/pgbackrest/pgbackrest/commit/b306f83493cc859ad15c8f175fc6db2321b79340)
- Actualiser le jeton web-id pour chaque authentification S3. (*Contribution de Brent Graveland. Révisé par David Steele.*)

  Le fichier de jeton désigné par `AWS_WEB_IDENTITY_TOKEN_FILE` était lu une seule fois au démarrage. Le jeton pouvait donc expirer pendant une opération longue. Il est désormais lu à chaque authentification.

  Ticket [#2428](https://github.com/pgbackrest/pgbackrest/issues/2428); Demande d’intégration [#2429](https://github.com/pgbackrest/pgbackrest/pull/2429); Commit [`95a4b9e`](https://github.com/pgbackrest/pgbackrest/commit/95a4b9e10a3f7a26ebaae22fc6abd79cee14189a)
- Afficher correctement les valeurs actuelles des options indexées dans l’aide. (*Révisé par David Christensen.*)

  La valeur courante affichée pour une option indexée était toujours celle du premier index, par exemple `pg1-path`. L'aide de l'option affiche désormais la valeur de chaque index, et la liste des options indique `<multi>` lorsqu'il y en a plusieurs.

  Demande d’intégration [#2453](https://github.com/pgbackrest/pgbackrest/pull/2453); Commit [`b3ca2e3`](https://github.com/pgbackrest/pgbackrest/commit/b3ca2e34823b28862d999f87c4d7346707952a5b)
- Enregistrer `backup.info` uniquement lorsque son contenu a changé. (*Révisé par Stefan Fercot.*)

  `expire` enregistrait `backup.info` même s'il n'avait pas changé. Réduire le nombre d'enregistrements facilite aussi le choix d'un instant cible sur un stockage versionné.

  Demande d’intégration [#2403](https://github.com/pgbackrest/pgbackrest/pull/2403); Commit [`b454b9e`](https://github.com/pgbackrest/pgbackrest/commit/b454b9e403526b1f352df964d9206c27d2397df3)
- Supprimer la limitation relative à la lecture de fichiers en parallèle lors d’une restauration. (*Révisé par David Christensen.*)

  Le protocole ne pouvait lire ou écrire qu'un fichier à la fois sur un hôte distant ; une restauration lisait donc les fichiers du dépôt un par un. Les commandes du protocole peuvent désormais être multiplexées, ce qui permet à une restauration de lire plusieurs fichiers à la fois, par exemple un regroupement et les données incrémentales par blocs d'un fichier qu'il contient.

  [`df8cbc9`](https://github.com/pgbackrest/pgbackrest/commit/df8cbc91c348bc2f746767c87ac5626460fb6f39) Multiplexage des commandes du protocole. ; Demande d’intégration [#2108](https://github.com/pgbackrest/pgbackrest/pull/2108)

  [`46c1297`](https://github.com/pgbackrest/pgbackrest/commit/46c1297be344909e900be596a865064233da9f87) Supprimer la limitation de lecture parallèle des fichiers pendant une restauration. ; Demande d’intégration [#2436](https://github.com/pgbackrest/pgbackrest/pull/2436)
- Améliorer les messages d’erreur SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Les erreurs SFTP n'étaient indiquées que par des numéros. Elles comportent désormais une description.

  Demande d’intégration [#2439](https://github.com/pgbackrest/pgbackrest/pull/2439); Commit [`70bda2c`](https://github.com/pgbackrest/pgbackrest/commit/70bda2cfb21130eb589a87cb419fb5f22a71c78a)

**Fonctionnalités de la documentation :**

- Ajouter une section d'optimisation des performances au guide utilisateur. (*Révisé par Stefan Fercot.*)

  Les options qui améliorent couramment les performances étaient dispersées dans la documentation. Le guide de démarrage rapide dispose désormais d'une section qui les répertorie.

  Demande d’intégration [#2446](https://github.com/pgbackrest/pgbackrest/pull/2446); Commit [`278319e`](https://github.com/pgbackrest/pgbackrest/commit/278319eba3444070123d3f0f277be9234604d937)

**Améliorations de la documentation :**

- Préciser la source de `data_directory`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Matthias.*)

  `pg-path` doit correspondre au `data_directory` indiqué par PostgreSQL, qui peut différer de la valeur de `postgresql.conf`.

  Ticket [#2464](https://github.com/pgbackrest/pgbackrest/issues/2464); Demande d’intégration [#2467](https://github.com/pgbackrest/pgbackrest/pull/2467); Commit [`9ba2db0`](https://github.com/pgbackrest/pgbackrest/commit/9ba2db017348d304f96ce89592fc01f29197e136)
- Meilleure logique pour déterminer quand un résumé doit être en minuscules. (*Suggéré par Daniel Westermann.*)

  Les résumés commençant par un nom propre ou un acronyme, comme PostgreSQL, ne sont plus convertis en minuscules dans la documentation.

  Ticket [#2462](https://github.com/pgbackrest/pgbackrest/issues/2462); Commit [`eb2f279`](https://github.com/pgbackrest/pgbackrest/commit/eb2f279a2998d1ed893c5d8984590ab4997a5f32)

### Notes de version v2.53.1 {#v2531-release-notes}

*Prise en charge de PostgreSQL 17*

*Sortie le 19 août 2024*

**Correctifs de bogues :**

- Corrigez les permissions lorsque `restore` est exécuté en tant qu'utilisateur root. (*Révisé par Stefan Fercot. Signalement par Will M.*)

  Lorsque `restore` était exécuté en tant que root, `pg_control` appartenait à root. Une restauration en tant que root échouait également si le chemin de base n'existait pas.

  Ticket [#2407](https://github.com/pgbackrest/pgbackrest/issues/2407); Demande d’intégration [#2416](https://github.com/pgbackrest/pgbackrest/pull/2416); Commit [`7bd8da4`](https://github.com/pgbackrest/pgbackrest/commit/7bd8da4eecb0ce1461854414b727606a5e884edf)
- Corrigez le plantage (segfault) sur les erreurs de connexion différées. (*Révisé par David Christensen. Signalement par Anton Glushakov.*)

  Une erreur de connexion suffisamment retardée pour être signalée lors d'une attente ultérieure pouvait provoquer une erreur de segmentation.

  Ticket [#2420](https://github.com/pgbackrest/pgbackrest/issues/2420); Demande d’intégration [#2422](https://github.com/pgbackrest/pgbackrest/pull/2422); Commit [`377ba06`](https://github.com/pgbackrest/pgbackrest/commit/377ba062ac81867dca6197265688deb0111ae81a)
- Ignorez la vérification des doublons du dépôt local pour SFTP. (*Corrigé par Reid Thompson. Révisé par David Steele. Signalement par Anton Kurochkin.*)

  La vérification des dépôts locaux configurés plusieurs fois s'appliquait également aux dépôts SFTP, qui ne sont jamais locaux.

  Ticket [#2418](https://github.com/pgbackrest/pgbackrest/issues/2418); Demande d’intégration [#2421](https://github.com/pgbackrest/pgbackrest/pull/2421); Commit [`9840304`](https://github.com/pgbackrest/pgbackrest/commit/98403046ed6af4c54fa2f572ecf9c211f94b67db)

**Améliorations :**

- Prise en charge de PostgreSQL 17.

  PostgreSQL 17beta3 a changé les formats du fichier de contrôle et des WAL, ce qui est inhabituel pour une bêta.

  Commit [`189d15d`](https://github.com/pgbackrest/pgbackrest/commit/189d15d1a640e31aac5ffbbd0fb06eb9eed8b576)

### Notes de version v2.53 {#v253-release-notes}

*Sauvegardes concurrentes*

*Sortie le 22 juillet 2024*

**NOTE IMPORTANTE** : La valeur par défaut de l'option `log-level-stderr` a été modifiée de `warn` à `off`. Cela facilite la détection des erreurs lorsqu'on redirige uniquement `stdout`. Pour conserver le comportement antérieur, définissez `log-level-stderr=warn`.<br/> <br/> **NOTE AUX PAQUETEURS** : La bibliothèque lz4 est désormais requise par la construction meson.<br/> <br/> **NOTE AUX PAQUETEURS** : La prise en charge du compilateur pour `__builtin_clzl()` et `__builtin_bswap64()` est désormais requise par la construction meson.

**Correctifs de bogues :**

- Correction d'une erreur de renommage SFTP lorsque le fichier existe déjà. (*Corrigé par Reid Thompson. Révisé par David Steele. Signalement par ahmed112212.*)

  Certains serveurs SFTP signalent l'existence d'un fichier par une erreur qui n'était pas traitée. Le renommage d'un fichier en remplacement d'un fichier existant échouait donc.

  Ticket [#2376](https://github.com/pgbackrest/pgbackrest/issues/2376); Demande d’intégration [#2377](https://github.com/pgbackrest/pgbackrest/pull/2377); Commit [`d6f0bf8`](https://github.com/pgbackrest/pgbackrest/commit/d6f0bf88af8b39492aa8e20c09bdf30260e2eb2f)

**Fonctionnalités :**

- Autoriser les sauvegardes à s'exécuter en parallèle sur des dépôts différents. (*Révisé par Reid Thompson, Stefan Fercot.*)

  Les sauvegardes d'une même stanza peuvent désormais s'exécuter simultanément sur des dépôts différents, car les verrous portent maintenant sur la stanza et le dépôt, et non sur la seule stanza. Cela n'est pas possible avec PostgreSQL <= 9.5.

  [`270dce4`](https://github.com/pgbackrest/pgbackrest/commit/270dce41b6fff0d0ad0769b0ea5df0011140f0b9) Refactoriser le module de verrouillage. ; Demande d’intégration [#2371](https://github.com/pgbackrest/pgbackrest/pull/2371)

  [`cfb8aa2`](https://github.com/pgbackrest/pgbackrest/commit/cfb8aa202ee972579697db2cc8d5d8ef111f0022) Ajouter les verrous distants des commandes stanza oubliés dans 31c7824a.

  [`edd6163`](https://github.com/pgbackrest/pgbackrest/commit/edd61636a98d193b7c0634b5a4444527132959e0) Permettre l'exécution simultanée de sauvegardes sur des dépôts différents. ; Demande d’intégration [#2389](https://github.com/pgbackrest/pgbackrest/pull/2389)
- Prise en charge des SAN basés sur l'IP pour la validation des certificats TLS. (*Contribution de David Christensen. Révisé par David Steele.*)

  Les certificats dont le nom alternatif du sujet est une adresse IP, comme `IP:1.2.3.4`, sont désormais validés. Les adresses IPv4 et IPv6 doivent correspondre exactement.

  Ticket [#1977](https://github.com/pgbackrest/pgbackrest/issues/1977); Demande d’intégration [#2047](https://github.com/pgbackrest/pgbackrest/pull/2047); Commit [`dfb620b`](https://github.com/pgbackrest/pgbackrest/commit/dfb620b0b8cf884ca486b413f4cd162e258b2fc5)

**Améliorations :**

- Définir l'option `log-level-stderr` sur `off` par défaut. (*Révisé par Greg Sabino Mullane et Stefan Fercot.*)

  Les avertissements et erreurs écrits sur stderr étaient souvent perdus lorsque seul stdout était redirigé pour collecter les journaux. Une valeur de `log-level-stderr` définie explicitement n'est pas affectée.

  Demande d’intégration [#2379](https://github.com/pgbackrest/pgbackrest/pull/2379); Commit [`7d54073`](https://github.com/pgbackrest/pgbackrest/commit/7d540730941994d3cb630c695e9f672e047d8e7f)
- Autoriser d'autres tailles de segment WAL pour PostgreSQL ≤ 10. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)

  PostgreSQL <= 10 peut être compilé avec une taille différente de segment WAL, et des dérivés comme Greenplum la définissent avec `initdb`.

  Demande d’intégration [#2303](https://github.com/pgbackrest/pgbackrest/pull/2303); Commit [`4ac3b82`](https://github.com/pgbackrest/pgbackrest/commit/4ac3b82c99ff3bd48d2cc74651a47ce072ac0022)
- Ajouter une indication invitant à consulter le journal d'autorisation SFTP. (*Contribution de Vitalii Zurian. Révisé par Reid Thompson et David Steele.*)

  En cas d'échec de l'authentification SFTP, l'erreur indique désormais que le journal d'autorisation du serveur peut fournir davantage de détails.

  Ticket [#2381](https://github.com/pgbackrest/pgbackrest/issues/2381); Demande d’intégration [#2385](https://github.com/pgbackrest/pgbackrest/pull/2385); Commit [`ccae609`](https://github.com/pgbackrest/pgbackrest/commit/ccae60940241b30e8bc3e405936b6ba68857930c)
- Affichage des valeurs par défaut et des valeurs autorisées des options de durée avec des unités appropriées.

  Les valeurs par défaut et autorisées des options de durée étaient affichées en secondes, ce qui rendait les grandes valeurs difficiles à lire. Les fractions de seconde ne sont plus autorisées : une valeur comme `archive-timeout=0.5` doit donc s'écrire `archive-timeout=500ms`.

  Commit [`3a2266f`](https://github.com/pgbackrest/pgbackrest/commit/3a2266f327c340ff1133a6a2398429c844b5755d)
- Exiger OpenSSL >= 1.1.1.

  Commit [`cf8625d`](https://github.com/pgbackrest/pgbackrest/commit/cf8625d24bd953ad1ed448c32b937584009e5b6b)

**Améliorations de la documentation :**

- Préciser le comportement multi-repo de `archive-push`. (*Révisé par Stefan Fercot.*)

  Lorsqu'un dépôt est en échec, `archive-push` ne peut pas poursuivre l'envoi vers les autres dépôts à moins que `archive-async` soit activé.

  Demande d’intégration [#2398](https://github.com/pgbackrest/pgbackrest/pull/2398); Commit [`ec3e387`](https://github.com/pgbackrest/pgbackrest/commit/ec3e387bb73826c30b32bf0221acb2d56f23f1c5)

### Notes de version v2.52.1 {#v2521-release-notes}

*Correction de bogue*

*Sortie le 25 juin 2024*

**Correctifs de bogues :**

- Corriger le problème des fichiers plus volumineux sur la réplique que sur le primaire. (*Révisé par Stefan Fercot. Signalement par Nicolas Lassimonne.*)

  Avec l'incrémental par blocs, lorsqu'un fichier avait une taille différente sur le primaire et le serveur de secours pendant une sauvegarde depuis ce dernier, la sauvegarde différentielle ou incrémentale suivante enregistrait la taille du primaire. La sauvegarde d'après échouait avec « repo size must be > 0 ».

  [`83aaa86`](https://github.com/pgbackrest/pgbackrest/commit/83aaa868ef396348bf96589457f13c1805b25cb6) Ajouter des tests unitaires de sauvegarde depuis un serveur de secours avec l'incrémental par blocs.

  [`aabc122`](https://github.com/pgbackrest/pgbackrest/commit/aabc122021a582e9d0193f978cf710cff95c2bee) Corriger le problème des fichiers plus grands sur le réplica que sur le primaire. ; Ticket [#2358](https://github.com/pgbackrest/pgbackrest/issues/2358); Demande d’intégration [#2367](https://github.com/pgbackrest/pgbackrest/pull/2367)

### Notes de version v2.52 {#v252-release-notes}

*Prise en charge de PostgreSQL 17beta1*

*Sortie le 27 mai 2024*

**NOTE AUX PAQUETEURS** : Le système de construction de pgBackRest est désormais meson. Le système de construction autoconf/make ne recevra plus de nouvelles fonctionnalités et sera supprimé après quelques versions.

**Fonctionnalités :**

- Ajout de la prise en charge de la suppression par lot GCS. (*Révisé par Reid Thompson.*)

  Les fichiers sont supprimés par requêtes groupées plutôt qu'avec une requête par fichier, ce qui accélère `expire` et les autres commandes supprimant des fichiers du dépôt.

  Demande d’intégration [#2326](https://github.com/pgbackrest/pgbackrest/pull/2326); Commit [`76bcb74`](https://github.com/pgbackrest/pgbackrest/commit/76bcb740b66f64804dbbf5a2a6be6407f9cec376)
- Prise en charge du chiffrement S3 `SSE-C`. (*Révisé par Tim Jones. Suggéré par Tim Jones.*)

  Définissez `repo-s3-sse-customer-key` pour que S3 chiffre les données avec la clé fournie après leur transmission. Cette méthode est moins sûre que le chiffrement avant transmission avec `repo-cipher-type`.

  Ticket [#2279](https://github.com/pgbackrest/pgbackrest/issues/2279); Demande d’intégration [#2282](https://github.com/pgbackrest/pgbackrest/pull/2282); Commit [`57731b6`](https://github.com/pgbackrest/pgbackrest/commit/57731b6cd261c732041aacc094429ab02ca13418)
- Prise en charge de PostgreSQL 17beta1. (*Révisé par Stefan Fercot.*)

  Ajout de la version du catalogue et du nombre magique WAL de PostgreSQL 17.

  Demande d’intégration [#2328](https://github.com/pgbackrest/pgbackrest/pull/2328); Commit [`fb22f04`](https://github.com/pgbackrest/pgbackrest/commit/fb22f04555fecfa143354372ec3543ab186c131d)

**Améliorations :**

- Permettre la désactivation explicite des dépendances optionnelles lors des compilations meson. (*Contribution de Michael Schout. Révisé par David Steele.*)

  Une fonctionnalité optionnelle peut être désactivée dans la compilation meson même si sa bibliothèque est installée, comme l'exigent certaines plateformes, notamment FreeBSD. Par défaut, une fonctionnalité est activée lorsque sa bibliothèque est trouvée.

  Demande d’intégration [#2321](https://github.com/pgbackrest/pgbackrest/pull/2321); Commit [`7b95fd3`](https://github.com/pgbackrest/pgbackrest/commit/7b95fd3bd29346e7325aa161bfee45efd71e22eb)
- Rechercher dynamiquement python lors de la compilation meson. (*Contribution de Michael Schout. Révisé par David Steele.*)

  La compilation meson trouve désormais l'installation de python au lieu d'exiger un exécutable `python3` dans le chemin, par exemple lorsque seul `python3.9` est installé. La version minimale de meson est désormais 0.47.

  [`55e9969`](https://github.com/pgbackrest/pgbackrest/commit/55e996912aa57d39ea21f5dc905b7acabe93b0f8) Porter la version minimale de meson à 0.47.

  [`e00e33b`](https://github.com/pgbackrest/pgbackrest/commit/e00e33b52856a63e82552ccc12df235d1a7f6f17) Trouver python dynamiquement lors de la compilation meson. ; Demande d’intégration [#2338](https://github.com/pgbackrest/pgbackrest/pull/2338)
- Marquer la cible de compilation `pgbackrest` comme installable dans meson. (*Contribution de Bradford Boyle. Révisé par David Steele.*)

  Demande d’intégration [#2312](https://github.com/pgbackrest/pgbackrest/pull/2312); Commit [`7877983`](https://github.com/pgbackrest/pgbackrest/commit/7877983acb3b1a27e900f7e7aea89cb7b29a817d)

**Améliorations de la documentation :**

- Mettre à jour la documentation de `start`/`stop` pour qu'elle reflète la fonctionnalité réelle. (*Révisé par Stefan Fercot.*)

  Ticket [#2325](https://github.com/pgbackrest/pgbackrest/issues/2325); Ticket [#2334](https://github.com/pgbackrest/pgbackrest/issues/2334); Demande d’intégration [#2352](https://github.com/pgbackrest/pgbackrest/pull/2352); Commit [`b6ac11b`](https://github.com/pgbackrest/pgbackrest/commit/b6ac11beec920fe978994c0d018c380477199ca8)

### Notes de version v2.51 {#v251-release-notes}

*Système de construction Meson*

*Sortie le 25 mars 2024*

**Correctifs de bogues :**

- Ignorer les fichiers de taille nulle lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par Sebastian Krause, René Højbjerg Larsen. Signalement par Sebastian Krause.*)

  Un fichier existant de longueur nulle faisait échouer une restauration delta incrémentale par blocs dans le filtre de somme de contrôle des blocs. Ces fichiers sont désormais ignorés, car ils ne contiennent rien à réutiliser.

  Ticket [#2271](https://github.com/pgbackrest/pgbackrest/issues/2271); Demande d’intégration [#2272](https://github.com/pgbackrest/pgbackrest/pull/2272); Commit [`f7a7ab1`](https://github.com/pgbackrest/pgbackrest/commit/f7a7ab16c9652179945717ebf9b68af3aa8a0b0e)
- Corriger la régression de performance dans la liste de stockage. (*Révisé par Stephen Frost. Signalement par Maksym Boguk.*)

  Lister un chemin demandait des informations détaillées pour chaque fichier, ce qui pouvait être lent, notamment sur les stockages objet. Seules les informations nécessaires à la liste sont désormais demandées.

  Ticket [#2275](https://github.com/pgbackrest/pgbackrest/issues/2275); Demande d’intégration [#2276](https://github.com/pgbackrest/pgbackrest/pull/2276); Commit [`e00bfe2`](https://github.com/pgbackrest/pgbackrest/commit/e00bfe2d2c3f124b2883e3c2d169a2ce506a1e98)
- Corriger la journalisation de progression lorsque la taille du fichier change pendant la sauvegarde. (*Révisé par Stephen Frost. Signalement par samkingno.*)

  Ticket [#2298](https://github.com/pgbackrest/pgbackrest/issues/2298); Demande d’intégration [#2304](https://github.com/pgbackrest/pgbackrest/pull/2304); Commit [`76956e7`](https://github.com/pgbackrest/pgbackrest/commit/76956e71cfa3044867213bd65a6f22e96120c108)

**Améliorations :**

- Amélioration du support des connexions en double pile. (*Révisé par Stephen Frost. Suggéré par Timothée Peignier.*)

  Lorsqu'un nom d'hôte se résout en plusieurs adresses, par exemple IPv4 et IPv6, l'adresse suivante est essayée dès que la précédente a disposé d'un délai raisonnable pour se connecter, selon l'approche « happy eyeballs » de la RFC 8305. Une tentative qui n'échoue ni n'aboutit ne consomme plus tout le temps disponible.

  Ticket [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Demande d’intégration [#2235](https://github.com/pgbackrest/pgbackrest/pull/2235); Commit [`7448fde`](https://github.com/pgbackrest/pgbackrest/commit/7448fde157c6d22f57b90c0cef11957b0aadf4b3)
- Utilisation de meson comme système de construction principal. (*Révisé par Stephen Frost.*)

  meson est désormais le système de compilation utilisé pour les tests et la génération de la documentation. Les fonctions non utilisées hors de leur module sont désormais masquées, ce qui réduit la taille du binaire.

  [`e3d9df3`](https://github.com/pgbackrest/pgbackrest/commit/e3d9df3ae9669ee5749b970d59f8afeb20fd3d9d) Faire de meson le système de compilation principal. ; Demande d’intégration [#2264](https://github.com/pgbackrest/pgbackrest/pull/2264)

  [`f287178`](https://github.com/pgbackrest/pgbackrest/commit/f287178b705cc90aa887d66c932e2a223029649b) Masquer la visibilité des fonctions et variables. ; Demande d’intégration [#2265](https://github.com/pgbackrest/pgbackrest/pull/2265)
- Détection des fichiers inchangés lors d'une sauvegarde incrémentielle non delta. (*Révisé par Stephen Frost.*)

  Lors d'une sauvegarde différentielle ou incrémentale sans delta, un fichier tenant dans un seul tampon, ou tout fichier incrémental par blocs, est comparé au fichier de la sauvegarde précédente. S'il n'a pas changé, il est référencé plutôt que stocké.

  Demande d’intégration [#2257](https://github.com/pgbackrest/pgbackrest/pull/2257); Commit [`9d91d1b`](https://github.com/pgbackrest/pgbackrest/commit/9d91d1b2f817b543fc8d970af56d1442c325ed7c)
- Empêcher une récupération invalide lorsque `backup_label` est supprimé. (*Révisé par Stephen Frost.*)

  Si `backup_label` est supprimé d'un cluster restauré, PostgreSQL utilise le point de contrôle de `pg_control` pour la récupération après incident, ce qui corrompt presque toujours le cluster. La restauration invalide désormais ce point de contrôle dans `pg_control`, afin que la récupération échoue à la place. `pg_controldata` affiche alors le point de contrôle comme `0/DEAD`.

  Demande d’intégration [#2232](https://github.com/pgbackrest/pgbackrest/pull/2232); Commit [`e634fd8`](https://github.com/pgbackrest/pgbackrest/commit/e634fd85cedc1ae3aef7c4fa2556d7d73d05cb8a)
- Amélioration de la gestion de la file d'attente des segments WAL `archive-push`. (*Révisé par Stephen Frost.*)

  La taille de chaque segment WAL de la file était lue pour mesurer la file. La taille du premier segment est désormais utilisée pour tous.

  Demande d’intégration [#2277](https://github.com/pgbackrest/pgbackrest/pull/2277); Commit [`cf17515`](https://github.com/pgbackrest/pgbackrest/commit/cf17515e409440eecfb04bf7186790d8baa8ab12)
- Limite la fonctionnalité de reprise aux sauvegardes complètes. (*Révisé par Stephen Frost, Stefan Fercot.*)

  La reprise ne fonctionnait pas correctement pour les sauvegardes différentielles et incrémentales en mode delta. De plus, un fichier modifié depuis la sauvegarde précédente risque de changer à nouveau avant une reprise. Seules les sauvegardes complètes peuvent désormais être reprises.

  Demande d’intégration [#2268](https://github.com/pgbackrest/pgbackrest/pull/2268); Commit [`dddcbcd`](https://github.com/pgbackrest/pgbackrest/commit/dddcbcd8e9a1cae578b0cc5bb2d1aa768330f3c5)
- Mise à jour de la fonctionnalité de reprise pour les sauvegardes incrémentielles par bloc. (*Révisé par Stephen Frost.*)

  La reprise supprimait les fichiers incrémentaux par blocs : elle fonctionnait, mais les recopiait tous. Ces fichiers sont désormais conservés lors d'une reprise.

  Demande d’intégration [#2296](https://github.com/pgbackrest/pgbackrest/pull/2296); Commit [`ff47450`](https://github.com/pgbackrest/pgbackrest/commit/ff47450402fde5ebc64a08d31791551bee52200e)
- Permettre `--version` et `--help` pour la version et l'aide. (*Révisé par Greg Sabino Mullane. Suggéré par Greg Sabino Mullane.*)

  `--version` et `--help` fonctionnent désormais comme dans la plupart des programmes. Utilisez `help` pour obtenir l'aide d'une commande ou d'une option particulière.

  Demande d’intégration [#2263](https://github.com/pgbackrest/pgbackrest/pull/2263); Commit [`68db307`](https://github.com/pgbackrest/pgbackrest/commit/68db3075d7ac4a48377967ad54e45b95b9ee6c61)
- Ajout d'un backtrace détaillé dans la construction autoconf/make. (*Révisé par Stephen Frost.*)

  Les traces de pile d'erreur de la compilation autoconf/make comprennent désormais les détails de libbacktrace, dont les tests de performances n'ont montré aucun coût notable.

  Demande d’intégration [#1970](https://github.com/pgbackrest/pgbackrest/pull/1970); Commit [`676700d`](https://github.com/pgbackrest/pgbackrest/commit/676700d8ca6f2e0e0ab8123aa9606c8ec7aa81ae)

**Améliorations de la documentation :**

- Mettre à jour les références à `recovery.conf`. (*Révisé par Stefan Fercot. Suggéré par Stephen Frost.*)

  Les références à `recovery.conf` incluent désormais `postgresql.auto.conf`, utilisé par les versions récentes de PostgreSQL.

  Demande d’intégration [#2281](https://github.com/pgbackrest/pgbackrest/pull/2281); Commit [`6835178`](https://github.com/pgbackrest/pgbackrest/commit/68351785f6816a23526900db595557cf6e3a0056)

### Notes de version v2.50 {#v250-release-notes}

*Améliorations des performances et corrections de bogues*

*Sortie le 22 janvier 2024*

**Correctifs de bogues :**

- Corriger la lecture courte lors d'une restauration incrémentielle par bloc. (*Révisé par Stephen Frost. Testé par Brent Graveland. Signalement par Adol Rodriguez, Brent Graveland.*)

  Un superbloc compressé peut se terminer par des octets inutiles à sa décompression mais marquant la fin des données. Selon l'alignement du tampon sur les données, ces octets n'étaient pas lus et la restauration échouait.

  Ticket [#2215](https://github.com/pgbackrest/pgbackrest/issues/2215); Ticket [#2238](https://github.com/pgbackrest/pgbackrest/issues/2238); Demande d’intégration [#2256](https://github.com/pgbackrest/pgbackrest/pull/2256); Commit [`f4a4af2`](https://github.com/pgbackrest/pgbackrest/commit/f4a4af299bee93ab7dde599ccdb35becc1c2afad)
- Corriger la suppression de la progression de la sauvegarde dans la sortie `info`. (*Corrigé par Robert Donovan. Révisé par Joe Wildish.*)

  Les tailles du fichier de verrou étaient lues comme des valeurs sur 32 bits. La commande `info` ne rapportait donc pas la progression d'une sauvegarde supérieure à 4GiB.

  Ticket [#2251](https://github.com/pgbackrest/pgbackrest/issues/2251); Demande d’intégration [#2252](https://github.com/pgbackrest/pgbackrest/pull/2252); Commit [`25f1489`](https://github.com/pgbackrest/pgbackrest/commit/25f14898babf4ad78baef3e8343933a863633975)

**Améliorations :**

- Conserver les fichiers partiels lors d'une restauration delta des sauvegardes incrémentielles par bloc. (*Révisé par Stephen Frost.*)

  Un fichier plus petit que prévu n'était pas conservé pour une restauration delta incrémentale par blocs, bien que ses blocs puissent être réutilisés, par exemple lors de la reprise d'une restauration échouée ou d'une restauration sur un fichier plus petit.

  Demande d’intégration [#2254](https://github.com/pgbackrest/pgbackrest/pull/2254); Commit [`a42614e`](https://github.com/pgbackrest/pgbackrest/commit/a42614e8f3a9e6871c16331f01c2cd765ab181aa)
- Ajouter la prise en charge des tailles de page alternatives au moment de la compilation. (*Contribution de Viktor Kurilko. Révisé par David Steele.*)

  PostgreSQL peut être compilé avec une taille de page différente, comme 4096 ; des dérivés tels que Greenplum le font.

  Demande d’intégration [#2197](https://github.com/pgbackrest/pgbackrest/pull/2197); Commit [`89d5278`](https://github.com/pgbackrest/pgbackrest/commit/89d5278b74ab0d880345575d7ac4c239cd1fce54)
- Ignorer les fichiers tronqués pendant la sauvegarde lors du regroupement. (*Contribution de Georgy Shelkovy. Révisé par David Steele.*)

  Un fichier tronqué à zéro après l'affectation des fichiers aux regroupements restait stocké dans son regroupement, et une compilation de débogage échouait sur une assertion. Ces fichiers sont désormais ignorés.

  [`02eea55`](https://github.com/pgbackrest/pgbackrest/commit/02eea555c7169e99892fdbc8ce7cc1ee59f50509) Ignorer les fichiers tronqués pendant la sauvegarde lors du regroupement. ; Demande d’intégration [#2227](https://github.com/pgbackrest/pgbackrest/pull/2227)

  [`c879509`](https://github.com/pgbackrest/pgbackrest/commit/c8795094d418802a0e24d4d19da66973c71b00e5) Permettre à backupFile() de renvoyer des tampons de somme de contrôle const.

  [`9049fec`](https://github.com/pgbackrest/pgbackrest/commit/9049fec2c02c4110e16ffdff7b56f83d8ff32b4a) Refactoriser l'omission des fichiers tronqués pendant la sauvegarde lors du regroupement.

  Développement dans [v2.49](#v249-release-notes) :

  [`337da35`](https://github.com/pgbackrest/pgbackrest/commit/337da35ab278e058ec4cdffeb4319f1a1e2cb0df) Ajouter un test montrant le comportement des fichiers regroupés tronqués pendant la sauvegarde.
- Améliorer les messages d'erreur du stockage SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Demande d’intégration [#2249](https://github.com/pgbackrest/pgbackrest/pull/2249); Commit [`7c17eec`](https://github.com/pgbackrest/pgbackrest/commit/7c17eec3db455d3e8e660f4f8247b6975517648f)

### Notes de version v2.49 {#v249-release-notes}

*Supprimer le support de PostgreSQL 9.3*

*Sortie le 27 novembre 2023*

**Correctifs de bogues :**

- Corriger un problème de réessais. (*Révisé par Stephen Frost. Signalement par Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)

  La v2.48 avait supprimé la nouvelle tentative effectuée lorsqu'une opération épuisait tout son délai. Un dépassement de délai devenait donc une erreur, par exemple en attendant qu'un socket soit prêt à écrire sur un stockage objet. Deux nouvelles tentatives sont désormais effectuées même si le délai a expiré.

  [`3c116e1`](https://github.com/pgbackrest/pgbackrest/commit/3c116e1829a0df62aaf50ce241c63d829eb438e0) Supprimer un en-tête inutilisé.

  [`fa5b2d4`](https://github.com/pgbackrest/pgbackrest/commit/fa5b2d44ad9f7591517eecaaaaeb07e9500dd51c) Corriger la régression des nouvelles tentatives. ; Ticket [#2200](https://github.com/pgbackrest/pgbackrest/issues/2200); Ticket [#2214](https://github.com/pgbackrest/pgbackrest/issues/2214); Demande d’intégration [#2221](https://github.com/pgbackrest/pgbackrest/pull/2221)
- Corriger la suppression récursive de chemins dans le pilote de stockage SFTP. (*Corrigé par Reid Thompson. Révisé par Stephen Frost. Signalement par Luc.*)

  Certains serveurs SFTP signalent un refus de permission plutôt qu'un échec lorsqu'un répertoire est supprimé comme un fichier. La suppression récursive d'un chemin échouait donc sur ces serveurs.

  Ticket [#2219](https://github.com/pgbackrest/pgbackrest/issues/2219); Demande d’intégration [#2226](https://github.com/pgbackrest/pgbackrest/pull/2226); Commit [`c4dc466`](https://github.com/pgbackrest/pgbackrest/commit/c4dc4665f88e9d67a3b66f44cd59d6dd4bb5107f)

**Améliorations :**

- Supprimer le support de PostgreSQL `9.3`. (*Révisé par Stephen Frost.*)

  PostgreSQL 9.3 n'est plus pris en charge, conformément à la politique de prise en charge de cinq versions de PostgreSQL arrivées en fin de vie.

  Demande d’intégration [#2220](https://github.com/pgbackrest/pgbackrest/pull/2220); Commit [`dcf0781`](https://github.com/pgbackrest/pgbackrest/commit/dcf078198761a2cfe9be6b4c7f4b4fb07ef53cbf)

**Fonctionnalités de la documentation :**

- Documenter les options du mainteneur. (*Révisé par Stefan Fercot.*)

  Les options destinées aux mainteneurs sont désormais documentées dans une section distincte avec les précautions d'utilisation, et `pg-version-force` n'est plus interne.

  Demande d’intégration [#2202](https://github.com/pgbackrest/pgbackrest/pull/2202); Commit [`21c8c8a`](https://github.com/pgbackrest/pgbackrest/commit/21c8c8a66cb06eba714bfa41bed7239af3d14f08)
- Mise à jour de la documentation de la restauration à un instant donné pour PostgreSQL >= 13.

  Depuis PostgreSQL 13, la récupération échoue si la cible de récupération n'est pas atteinte. La section sur la récupération à un instant donné fonctionne désormais aussi bien pour PostgreSQL 13 et suivants que pour les versions précédentes.

  Commit [`eb69e2e`](https://github.com/pgbackrest/pgbackrest/commit/eb69e2ee6339047f0145b751437ac2bec82bb5ab)

**Améliorations de la suite de tests :**

- Autoriser l'exécution des tests unitaires `config/load` sans que `libssh2` soit installé. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Wu Ning.*)

  Ticket [#2193](https://github.com/pgbackrest/pgbackrest/issues/2193); Demande d’intégration [#2194](https://github.com/pgbackrest/pgbackrest/pull/2194); Commit [`e2b734e`](https://github.com/pgbackrest/pgbackrest/commit/e2b734eff97e3fac32895b799cc32126013aae27)

### Notes de version v2.48 {#v248-release-notes}

*Balises de stockage du dépôt*

*Sortie le 25 septembre 2023*

**Correctifs de bogues :**

- Corriger le problème de restauration d'une sauvegarde incrémentielle par bloc sans liste de blocs. (*Révisé par Stephen Frost. Testé par Burak Yurdakul. Signalement par Burak Yurdakul.*)

  Une carte de blocs sans blocs, écrite lorsque l'horodatage d'un fichier change sans changement de son contenu, n'était pas déchiffrée lorsqu'elle suivait un fichier stocké sans incrémental par blocs dans la même lecture de regroupement. Si suffisamment de fichiers étaient affectés, les nouvelles tentatives étaient épuisées et la restauration échouait.

  Ticket [#2182](https://github.com/pgbackrest/pgbackrest/issues/2182); Demande d’intégration [#2184](https://github.com/pgbackrest/pgbackrest/pull/2184); Commit [`31de127`](https://github.com/pgbackrest/pgbackrest/commit/31de127cf42438b1fac04c161c47264aa1fb1060)

**Fonctionnalités :**

- Ajouter l'option `--repo-storage-tag` pour créer des balises d'objets. (*Révisé par Stephen Frost, Stefan Fercot, Timothée Peignier.*)

  Définissez `repo-storage-tag` pour ajouter des étiquettes aux objets écrits dans un dépôt S3, GCS ou Azure. Les étiquettes sont définies par dépôt.

  Ticket [#2150](https://github.com/pgbackrest/pgbackrest/issues/2150); Demande d’intégration [#2159](https://github.com/pgbackrest/pgbackrest/pull/2159); Commit [`1b4e0cc`](https://github.com/pgbackrest/pgbackrest/commit/1b4e0cce5f3ff5ea3ee0b889e6d4ce4de1430b04)
- Ajouter la vérification des hôtes connus pour le pilote de stockage SFTP. (*Contribution de Reid Thompson. Révisé par Stephen Frost, David Steele.*)

  Les clés d'hôte SFTP sont désormais vérifiées par défaut dans les fichiers d'hôtes connus, soit `repo-sftp-host-key-check-type=strict`. Définissez `repo-sftp-host-key-check-type=accept-new` pour ajouter automatiquement les nouveaux hôtes, ou `repo-sftp-host-key-check-type=none` pour omettre la vérification comme auparavant.

  Demande d’intégration [#2125](https://github.com/pgbackrest/pgbackrest/pull/2125); Commit [`ce9ba0f`](https://github.com/pgbackrest/pgbackrest/commit/ce9ba0fadee652d409488bee701ea6a51cafec75)
- Prise en charge des connexions en double pile. (*Révisé par Stephen Frost.*)

  Chaque adresse obtenue pour un nom d'hôte est désormais essayée à son tour, par exemple une adresse IPv6 sans route vers l'hôte puis une adresse IPv4, jusqu'à ce qu'une connexion aboutisse ou que le délai expire. Les erreurs répétées lors des nouvelles tentatives sont également résumées dans les messages d'erreur.

  [`5314dbf`](https://github.com/pgbackrest/pgbackrest/commit/5314dbffc761bc7507db02693f2421c1578efe10) Rendre l'objet Wait plus précis lorsqu'il est imbriqué.

  [`c180513`](https://github.com/pgbackrest/pgbackrest/commit/c1805134b370f0c5c54c40a2df8978599328784f) Agréger les erreurs répétées dans la sortie ErrorRetry.

  [`edbd520`](https://github.com/pgbackrest/pgbackrest/commit/edbd520c81f5d437963aaf42d1c79b2c51d01665) Refactoriser la recherche d'adresses pour inclure toutes les adresses renvoyées. ; Demande d’intégration [#2174](https://github.com/pgbackrest/pgbackrest/pull/2174)

  [`39bb8a0`](https://github.com/pgbackrest/pgbackrest/commit/39bb8a0d3a96eef63219dff262a9306a4f59dae9) Prise en charge des connexions double pile. ; Ticket [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Demande d’intégration [#2175](https://github.com/pgbackrest/pgbackrest/pull/2175)
- Ajouter la taille de la sauvegarde terminée/total à la sortie JSON de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  La sortie JSON de `info` comprend désormais les tailles traitée et totale d'une sauvegarde en cours, afin que d'autres programmes puissent suivre sa progression.

  Ticket [#2007](https://github.com/pgbackrest/pgbackrest/issues/2007); Demande d’intégration [#2141](https://github.com/pgbackrest/pgbackrest/pull/2141); Commit [`e3fcd8c`](https://github.com/pgbackrest/pgbackrest/commit/e3fcd8cd9e0be42a32fc4cbd2ae3db2c072eabcd)

**Améliorations :**

- Commande de vérification multi-stanza. (*Révisé par Stephen Frost.*)

  Lorsque `stanza` n'est pas spécifié, `check` vérifie désormais toutes les stanzas de la configuration.

  Demande d’intégration [#2057](https://github.com/pgbackrest/pgbackrest/pull/2057); Commit [`1141dc2`](https://github.com/pgbackrest/pgbackrest/commit/1141dc20708cf0c68296f83e74c872a7db9c2bd9)
- Réessayer la lecture de `pg_control` jusqu'à ce que la somme de contrôle soit valide. (*Révisé par Stefan Fercot, Stephen Frost.*)

  Sur certains systèmes de fichiers, comme ext4, une lecture de `pg_control` pendant une écriture simultanée peut renvoyer des données partiellement écrites. La lecture est désormais réessayée jusqu'à ce que la somme de contrôle soit valide.

  Demande d’intégration [#2131](https://github.com/pgbackrest/pgbackrest/pull/2131); Commit [`f42d927`](https://github.com/pgbackrest/pgbackrest/commit/f42d927d2dcd58cf5a80d68eaf6888bcf2c67a4b)
- Optimiser la vérification du segment WAL après une sauvegarde réussie. (*Révisé par Stephen Frost.*)

  La vérification des segments WAL après une sauvegarde listait le stockage une fois par segment. Chaque répertoire WAL n'est désormais listé qu'une fois, puis la liste est réutilisée.

  Demande d’intégration [#2169](https://github.com/pgbackrest/pgbackrest/pull/2169); Commit [`9d3a605`](https://github.com/pgbackrest/pgbackrest/commit/9d3a605900644059ff0e030d71a818b3965eb031)
- Améliorer les performances multi-partie du GCS. (*Révisé par Reid Thompson.*)

  Les morceaux d'un envoi multipartie sont désormais envoyés dès qu'ils sont disponibles.

  Demande d’intégration [#2162](https://github.com/pgbackrest/pgbackrest/pull/2162); Commit [`6cb9c40`](https://github.com/pgbackrest/pgbackrest/commit/6cb9c40fb8ea18e6572bf3f6e44bbb1d8f922682)
- Permettre à la commande `archive-get` de s'exécuter lorsque la stanza est arrêtée. (*Révisé par Tom Swartz, David Christensen, Reid Thompson.*)

  La commande `archive-get` n'écrit pas dans le dépôt ; elle peut donc désormais s'exécuter lorsque la stanza est arrêtée, comme `restore`.

  Commit [`fbd992a`](https://github.com/pgbackrest/pgbackrest/commit/fbd992adc7b18db5e70774d675c160c8c8e2f031)
- Accepter un tilde initial dans les chemins pour les clés publiques/privées SFTP. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Les chemins de `repo-sftp-private-key-file` et `repo-sftp-public-key-file` peuvent désormais commencer par `~`, comme indiqué dans la documentation.

  Demande d’intégration [#2136](https://github.com/pgbackrest/pgbackrest/pull/2136); Commit [`eb32d6d`](https://github.com/pgbackrest/pgbackrest/commit/eb32d6de5e1575a37efb166abbf7df400d93352e)
- Recharger les identifiants GCS avant de renouveler le jeton d'authentification. (*Révisé par Stephen Frost. Suggéré par Daniel Farina.*)

  Le fichier de clé de service est désormais relu avant le renouvellement du jeton d'authentification, ce qui permet de remplacer la clé pendant l'exécution d'une commande.

  Demande d’intégration [#2072](https://github.com/pgbackrest/pgbackrest/pull/2072); Commit [`995a8e9`](https://github.com/pgbackrest/pgbackrest/commit/995a8e96691d23eaf3914a425669f89deb3ce002)

**Correctifs de bogues dans la documentation :**

- Corriger l'exemple de référence de configuration pour l'option `tls-server-address`. (*Corrigé par Hartmut Goebel. Révisé par David Steele.*)

  L'exemple `::*` n'était pas valide. Utilisez `*` pour IPv4 ou `::` pour IPv6.

  Demande d’intégration [#2165](https://github.com/pgbackrest/pgbackrest/pull/2165); Commit [`43524a4`](https://github.com/pgbackrest/pgbackrest/commit/43524a47a4c6a847f76514812f94b87cb7af4c05)
- Corriger l'exemple de référence de commande pour l'option `filter`.

  Commit [`cb3ff6e`](https://github.com/pgbackrest/pgbackrest/commit/cb3ff6ed4336af9e4c0643d8224d5bc3d790a655)

**Améliorations de la suite de tests :**

- Autoriser l'exécution des tests unitaires `storage/sftp` sans que `libssh2` soit installé. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Wu Ning.*)

  Ticket [#2163](https://github.com/pgbackrest/pgbackrest/issues/2163); Demande d’intégration [#2177](https://github.com/pgbackrest/pgbackrest/pull/2177); Commit [`c3c0834`](https://github.com/pgbackrest/pgbackrest/commit/c3c0834e170196a1241a368779162fcca65f9ad5)

### Notes de version v2.47 {#v247-release-notes}

*Améliorations des performances et corrections de bogues*

*Sortie le 24 juillet 2023*

**Correctifs de bogues :**

- Conserver les informations incrémentielles par bloc dans le manifeste lors d'une sauvegarde incrémentielle. (*Révisé par Stephen Frost. Signalement par Francisco Miguel Biete Banon.*)

  Lorsqu'un fichier changeait de sorte qu'il n'aurait plus utilisé l'incrémental par blocs s'il avait été nouveau, par exemple en passant sous la limite de taille ou en prenant un horodatage suffisamment ancien, ses informations d'incrémental par blocs disparaissaient du manifeste d'une sauvegarde delta, même si le fichier pouvait encore référencer la sauvegarde précédente.

  [`1d42aed`](https://github.com/pgbackrest/pgbackrest/commit/1d42aed152563fff6ec70c517d86eb39158b3f20) Améliorer la validation des fichiers référencés dans le test unitaire command/backup.

  [`4c27d74`](https://github.com/pgbackrest/pgbackrest/commit/4c27d74bbd3a44d8ab1af140277d3cd8302060c2) Préserver les informations d'incrémental par blocs du manifeste pendant une sauvegarde delta. ; Ticket [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Demande d’intégration [#2123](https://github.com/pgbackrest/pgbackrest/pull/2123)
- Corriger les noms de fichiers incrémentiels dans la commande `verify`. (*Révisé par Reid Thompson. Signalement par Francisco Miguel Biete Banon.*)

  La commande `verify` utilisait l'extension de compression au lieu de `.pgbi` pour les fichiers incrémentaux par blocs stockés hors d'un regroupement, et ne pouvait donc pas les trouver.

  Ticket [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Demande d’intégration [#2120](https://github.com/pgbackrest/pgbackrest/pull/2120); Commit [`cdb7e26`](https://github.com/pgbackrest/pgbackrest/commit/cdb7e26350822b55c00771d6d575242b1202e741)
- Corriger la sauvegarde delta automatique erronée lors d'une sauvegarde depuis un serveur de secours. (*Révisé par Stephen Frost. Signalement par krmozejko, Don Seiler.*)

  Les tailles des fichiers sur le serveur de secours peuvent différer de celles du primaire, par exemple pour les cartes d'espace libre. La sauvegarde incrémentale suivante pouvait donc détecter un changement de taille sur le primaire et passer à un delta par somme de contrôle, beaucoup plus long. La taille d'origine est désormais conservée dans le manifeste et utilisée pour la comparaison.

  Ticket [#2020](https://github.com/pgbackrest/pgbackrest/issues/2020); Demande d’intégration [#2124](https://github.com/pgbackrest/pgbackrest/pull/2124); Commit [`5ed6f8d`](https://github.com/pgbackrest/pgbackrest/commit/5ed6f8df1487174985c42d6e13c367d70c2d8b8a)
- Ignorer `recovery.signal` pour PostgreSQL >= 12 lorsque la récupération `type=none`. (*Révisé par Stefan Fercot. Signalement par T.Anastacio.*)

  Avec `type=none`, `recovery.signal` n'est plus écrit pour PostgreSQL >= 12, conformément au comportement des versions antérieures.

  Ticket [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Demande d’intégration [#2070](https://github.com/pgbackrest/pgbackrest/pull/2070); Commit [`9cceed6`](https://github.com/pgbackrest/pgbackrest/commit/9cceed6ac4a32c14a797eba89a4ad1dc06d89d80)
- Corriger la génération de libellés uniques pour les sauvegardes diff/incr. (*Corrigé par Andrey Sokolov. Révisé par David Steele.*)

  Avec au moins deux sauvegardes complètes dont la plus récente avait expiré, une sauvegarde différentielle ou incrémentale échouait comme si l'horloge avait reculé, car son étiquette était comparée à celle de la sauvegarde complète expirée.

  Ticket [#1873](https://github.com/pgbackrest/pgbackrest/issues/1873); Demande d’intégration [#2104](https://github.com/pgbackrest/pgbackrest/pull/2104); Commit [`0ac0934`](https://github.com/pgbackrest/pgbackrest/commit/0ac09344dc17fb54e250705ce49399b86329bb3d)
- Corriger l'expiration des archives basée sur le temps lorsque aucune sauvegarde n'est expirée. (*Révisé par Stefan Fercot.*)

  Lorsque la rétention temporelle était satisfaite sans qu'aucune sauvegarde n'expire, les archives n'expiraient pas et le message « time-based archive retention not met » était journalisé. Il fallait alors une sauvegarde supplémentaire pour faire expirer les WAL antérieurs.

  Ticket [#2103](https://github.com/pgbackrest/pgbackrest/issues/2103); Demande d’intégration [#2109](https://github.com/pgbackrest/pgbackrest/pull/2109); Commit [`762498f`](https://github.com/pgbackrest/pgbackrest/commit/762498f4cd5f1425db4c176fc707926d62cc7c04)

**Améliorations :**

- Améliorer les performances du pilote de stockage SFTP. (*Contribution de Stephen Frost, Reid Thompson. Révisé par David Steele.*)

  Le pilote de stockage SFTP attendait une durée fixe lorsque libssh2 ne pouvait pas poursuivre. Il attend désormais que le socket soit prêt en lecture ou en écriture.

  [`e280ed9`](https://github.com/pgbackrest/pgbackrest/commit/e280ed9098a6f5da9bdabb541e9c69d4f24ffcf2) Harmoniser le traitement des codes de résultat dans storage/sftp.

  [`125676a`](https://github.com/pgbackrest/pgbackrest/commit/125676ae0e98d3730d2dc0d47e37ca1df145d044) Nettoyer l'initialisation et la négociation dans storageSftpNew().

  [`28b6b2d`](https://github.com/pgbackrest/pgbackrest/commit/28b6b2d4659d78ce67c1bd3104d96e5705d955c9) Améliorer les performances du pilote de stockage SFTP. ; Demande d’intégration [#2089](https://github.com/pgbackrest/pgbackrest/pull/2089)
- Ajouter un décalage horaire à la sortie de date/heure de la commande `info`. (*Révisé par Stefan Fercot, Philip Hurst. Suggéré par Philip Hurst.*)

  Les horodatages de la sortie de `info` incluent désormais le décalage de fuseau horaire, afin de pouvoir servir directement de cible de récupération, par exemple avec `--target`.

  [`9efd5cd`](https://github.com/pgbackrest/pgbackrest/commit/9efd5cd0bb40c5dc2fcac2e21c9b62e554b94db6) Ajouter le décalage de fuseau horaire aux dates et heures de la sortie de info. ; Ticket [#2093](https://github.com/pgbackrest/pgbackrest/issues/2093); Demande d’intégration [#2095](https://github.com/pgbackrest/pgbackrest/pull/2095)

  [`aa229a1`](https://github.com/pgbackrest/pgbackrest/commit/aa229a1deef3afeebb66db1443b19e24559adf96) Modifier les conversions time_t selon les avertissements de Coverity.
- Centraliser le traitement des erreurs liées aux fonctionnalités non prises en charge. (*Révisé par Stefan Fercot.*)

  Les erreurs relatives aux fonctionnalités non compilées, comme lz4, sont désormais plus détaillées et cohérentes. Spécifier un stockage SFTP lorsqu'il n'a pas été compilé ne fait plus échouer une assertion.

  [`de46276`](https://github.com/pgbackrest/pgbackrest/commit/de46276bf60b8a2181621b123d1a99e56808a089) Refactoriser le traitement des listes de valeurs autorisées dans config/parse.

  [`36ff81d`](https://github.com/pgbackrest/pgbackrest/commit/36ff81dc6ff7e98e40c0c05a4a343a71b91b1678) Centraliser le traitement des erreurs des fonctionnalités non prises en charge. ; Demande d’intégration [#2075](https://github.com/pgbackrest/pgbackrest/pull/2075)

**Améliorations de la documentation :**

- Préciser la préférence à installer à partir des paquets dans le guide utilisateur. (*Révisé par Stefan Fercot. Suggéré par dr-kd.*)

  Demande d’intégration [#2090](https://github.com/pgbackrest/pgbackrest/pull/2090); Commit [`a36f480`](https://github.com/pgbackrest/pgbackrest/commit/a36f480c85c7add6fdf0e5517748d740e3a7b424)

### Notes de version v2.46 {#v246-release-notes}

*Sauvegarde incrémentielle par bloc et stockage SFTP*

*Sortie le 22 mai 2023*

**Fonctionnalités :**

- Sauvegarde incrémentielle par bloc. (*Révisé par John Morris, Stephen Frost, Stefan Fercot.*)

  L'incrémental par blocs ne stocke que les parties d'un fichier modifiées depuis la sauvegarde précédente, ce qui économise de l'espace et du temps dans les sauvegardes différentielles et incrémentales de gros fichiers. Activez-le avec `repo-block`, qui nécessite `repo-bundle`.

  [`dd4e526`](https://github.com/pgbackrest/pgbackrest/commit/dd4e52679ecdc43539bd038b5aa9bd4ff9055cbf) Supprimer le découpage et les numéros de blocs de la liste incrémentale des blocs. ; Demande d’intégration [#2029](https://github.com/pgbackrest/pgbackrest/pull/2029)

  [`822f2a5`](https://github.com/pgbackrest/pgbackrest/commit/822f2a584260a012b833455a7a2bd1c8487e3010) Finaliser la fonctionnalité d'incrémental par blocs. ; Demande d’intégration [#2053](https://github.com/pgbackrest/pgbackrest/pull/2053)
- Prise en charge SFTP pour le stockage du dépôt. (*Contribution de Reid Thompson. Révisé par Stephen Frost, David Steele.*)

  Définissez `repo-type=sftp` et `repo-sftp-host` pour stocker le dépôt sur un serveur SFTP.

  Demande d’intégration [#1959](https://github.com/pgbackrest/pgbackrest/pull/1959); Commit [`87087fa`](https://github.com/pgbackrest/pgbackrest/commit/87087fac231d2110160b3219daee3f9fb91aec02)

  Développement dans [v2.42](#v242-release-notes) :

  [`01b81f9`](https://github.com/pgbackrest/pgbackrest/commit/01b81f9d374701eb489dd1888bcba25fb5d6df84) Déplacer la création de liens vers l'interface de stockage. ; Demande d’intégration [#1879](https://github.com/pgbackrest/pgbackrest/pull/1879)
- Prise en charge de PostgreSQL 16. (*Révisé par Stefan Fercot.*)

  Ajout de la version du catalogue et du nombre magique WAL de PostgreSQL 16.

  Demande d’intégration [#2051](https://github.com/pgbackrest/pgbackrest/pull/2051); Commit [`3fc3690`](https://github.com/pgbackrest/pgbackrest/commit/3fc3690dd77ef5fa032abb006558184164db53ec)

**Améliorations :**

- Permettre de passer outre les vérifications d'en-tête de page. (*Révisé par David Christensen. Suggéré par David Christensen.*)

  Les vérifications d'en-tête effectuées lors de la validation des sommes de contrôle des pages peuvent signaler de fausses erreurs pour les pages chiffrées. Définissez `page-header-check=n` pour les omettre. Elles sont activées par défaut.

  Demande d’intégration [#2045](https://github.com/pgbackrest/pgbackrest/pull/2045); Commit [`f5e6bc2`](https://github.com/pgbackrest/pgbackrest/commit/f5e6bc26983396ec51c6579aade37db39807f3a5)
- Éviter `chown()` sur les fichiers de récupération lors d'une restauration. (*Révisé par Stefan Fercot, Marcelo Henrique Neppel. Suggéré par Marcelo Henrique Neppel.*)

  La restauration omettait `chown()` pour les fichiers restaurés ayant déjà le bon propriétaire, mais pas pour les fichiers de récupération qu'elle écrivait. Le pilote Posix omet désormais aussi `chown()` lorsque le propriétaire est déjà correct.

  Ticket [#2036](https://github.com/pgbackrest/pgbackrest/issues/2036); Demande d’intégration [#2038](https://github.com/pgbackrest/pgbackrest/pull/2038); Commit [`3ff88ff`](https://github.com/pgbackrest/pgbackrest/commit/3ff88ffbb495fd669e9a361478e60192930ee0a1)
- Ajouter des détails d'erreur pour les tentatives de réessai HTTP.

  Une erreur après des nouvelles tentatives HTTP indique désormais leur nombre et leur durée.

  [`801e396`](https://github.com/pgbackrest/pgbackrest/commit/801e396dace2a4d9f4125ef0e751c90dc0cc644a) Déplacer les modules d'erreur dans le répertoire common/error.

  [`df419b3`](https://github.com/pgbackrest/pgbackrest/commit/df419b34b55a15a902ff5cc1912aaebc7e023738) Améliorer les messages d'erreur des nouvelles tentatives.

  [`f33e1cf`](https://github.com/pgbackrest/pgbackrest/commit/f33e1cfb1600643820a1ae76bdeb15c62ac1fcc7) Ajouter des détails sur les erreurs répétées lors des nouvelles tentatives HTTP.

**Améliorations de la documentation :**

- Ajouter un avertissement concernant l'utilisation de la récupération `type=none`. (*Révisé par Stefan Fercot.*)

  Le mode de récupération `type=none` n'incrémente pas la timeline à la fin de la récupération. PostgreSQL peut alors archiver des WAL en double, qui sont rejetés et remplissent le disque ; des outils comme `pg_rewind` peuvent aussi échouer ou corrompre le cluster. La documentation met désormais en garde contre ce mode.

  Ticket [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Demande d’intégration [#2069](https://github.com/pgbackrest/pgbackrest/pull/2069); Commit [`a28b72c`](https://github.com/pgbackrest/pgbackrest/commit/a28b72c62431bcf9df02791219d9d6f5d0e60b54)
- Ajouter une note sur l'exécution de `stanza-create` sur des dépôts déjà créés.

  Les stanzas déjà présentes sont ignorées. Il est donc sûr de relancer `stanza-create`, par exemple après la configuration d'un nouveau dépôt.

  Commit [`0c1f823`](https://github.com/pgbackrest/pgbackrest/commit/0c1f823e7a3abf1cadb44de3832ec1ddb2da7ec8)

### Notes de version v2.45 {#v245-release-notes}

*Sauvegarde incrémentielle par bloc (BÉTA)*

*Sortie le 20 mars 2023*

**Correctifs de bogues :**

- Ne pas écrire `recovery.signal` par défaut lors de la restauration de sauvegardes hors ligne. (*Révisé par Stefan Fercot. Signalement par Marcel Borger.*)

  Avec PostgreSQL >= 12, `recovery.signal` empêche PostgreSQL de démarrer lorsque la sauvegarde a été réalisée hors ligne avec `wal_level=minimal`. La restauration n'écrit désormais plus ce fichier pour les sauvegardes hors ligne, sauf si `type` est défini explicitement, par exemple pour une récupération à un instant donné depuis une sauvegarde hors ligne effectuée avec un `wal_level` plus élevé.

  [`0818601`](https://github.com/pgbackrest/pgbackrest/commit/0818601c055724bde3b97d4b02d3a38b0a53899a) Définir l'indicateur online du manifeste dans les tests unitaires command/restore.

  [`2fa7e53`](https://github.com/pgbackrest/pgbackrest/commit/2fa7e53c5d4b5a5fd79f62d39763746727a5b9be) Ne pas écrire recovery.signal par défaut lors de la restauration de sauvegardes hors ligne. ; Ticket [#2018](https://github.com/pgbackrest/pgbackrest/issues/2018); Demande d’intégration [#2019](https://github.com/pgbackrest/pgbackrest/pull/2019)

**Fonctionnalités :**

- Sauvegarde incrémentielle par bloc (BÉTA). (*Révisé par John Morris, Stephen Frost, Stefan Fercot.*)

  L'incrémental par blocs stocke uniquement les parties d'un fichier modifiées depuis la sauvegarde précédente, au lieu du fichier entier. Activez-le avec `repo-block`, qui nécessite `repo-bundle`. Cette fonctionnalité est en bêta et nécessite aussi l'option `beta`. Ne l'utilisez pas en production : le format sur disque changera avant la version stable.

  [`089fae0`](https://github.com/pgbackrest/pgbackrest/commit/089fae035bf0a9778fff0527ea3cbb113625a403) Ajouter l'incrémental par blocs à la sortie du test real/all.

  [`3feed38`](https://github.com/pgbackrest/pgbackrest/commit/3feed389a2199454db68e446851323498b45db20) Améliorer la gestion de fin de fichier dans IoChunkedRead.

  [`d520816`](https://github.com/pgbackrest/pgbackrest/commit/d520816acf9ecb01ef805cecbc9de7e8d0a9f468) Supprimer la liste des paramètres de deltaMapNew().

  [`779efe0`](https://github.com/pgbackrest/pgbackrest/commit/779efe0d7a54340141e01597279e9ab1d0bd0773) Déclarer systématiquement la taille de l'incrémental par blocs en size_t.

  [`dffc933`](https://github.com/pgbackrest/pgbackrest/commit/dffc933384e4327e2fd52868dd19668ed9d3ed91) Renommer DeltaMap en BlockHash.

  [`a9867cb`](https://github.com/pgbackrest/pgbackrest/commit/a9867cb0b8e8d7abcac9b18b76e3e490c265f3cb) Ajouter les options repo-block-age-map et repo-block-size-map.

  [`16ac5ee`](https://github.com/pgbackrest/pgbackrest/commit/16ac5ee8d3b926464cd27e8f064579f1e7935f4c) Renommer les clés du manifeste de l'incrémental par blocs.

  [`da91858`](https://github.com/pgbackrest/pgbackrest/commit/da9185870222057b97365f5db0acf797f959ec5e) Ajouter un format brut optionnel pour les types de compression.

  [`7e5adc0`](https://github.com/pgbackrest/pgbackrest/commit/7e5adc03594a3b7a975001e80902a51df3ddd577) Utiliser la compression et le chiffrement bruts pour le regroupement et la sauvegarde incrémentale par blocs.

  [`8b5153a`](https://github.com/pgbackrest/pgbackrest/commit/8b5153ad210011812c8fe6db2f2ed829a5aa543a) Superblocs de sauvegarde incrémentale par blocs. ; Demande d’intégration [#1996](https://github.com/pgbackrest/pgbackrest/pull/1996)

  [`210bed4`](https://github.com/pgbackrest/pgbackrest/commit/210bed4511ae5523b170eb193b877346d787140d) Utiliser xxHash plutôt que SHA-1 pour les sommes de contrôle de l'incrémental par blocs.

  [`6252c0e`](https://github.com/pgbackrest/pgbackrest/commit/6252c0e4485caee362edec13302a5f735a69bff4) Exclure la taille du jeu de sauvegardes de info pour les sauvegardes incrémentales par blocs.

  [`1119a53`](https://github.com/pgbackrest/pgbackrest/commit/1119a5353911d6d326edac325f530bb796a806ae) Renommer BlockHash en BlockChecksum.

  [`6b409d0`](https://github.com/pgbackrest/pgbackrest/commit/6b409d049eb935146f7996b75b97744b75c411a9) Ajuster les valeurs par défaut des tailles de bloc et de superbloc selon les tests.

  [`1281a6e`](https://github.com/pgbackrest/pgbackrest/commit/1281a6eaf8552232c8c9af4d7fc15c082a7794d9) Garantir l'absence de continuations lorsque la taille de bloc est égale à celle du superbloc.

  [`5c1f78d`](https://github.com/pgbackrest/pgbackrest/commit/5c1f78d4dd62c37218285d13b09a9450eb3a588e) Corriger une faute dans blockIncrProcess().

  [`c30d3e4`](https://github.com/pgbackrest/pgbackrest/commit/c30d3e439b77d544477e289606d30d0c8ffe301f) Corrections et améliorations des cartes incrémentales par blocs. ; Demande d’intégration [#2026](https://github.com/pgbackrest/pgbackrest/pull/2026)

  [`24f7252`](https://github.com/pgbackrest/pgbackrest/commit/24f725212d0c1dedc0f34fe4e939e481585ff697) Ajouter l'infrastructure des fonctionnalités bêta.

  [`04d224b`](https://github.com/pgbackrest/pgbackrest/commit/04d224b88e73194ff1c6497dbecaaff392008dfe) Ajouter la fonctionnalité bêta et la documentation de la sauvegarde incrémentale par blocs.

  Développement dans [v2.44](#v244-release-notes) :

  [`912eec6`](https://github.com/pgbackrest/pgbackrest/commit/912eec63bb971c10a545e582f628c982f4e00005) Sauvegarde incrémentale par blocs. ; Ticket [#959](https://github.com/pgbackrest/pgbackrest/issues/959); Ticket [#1806](https://github.com/pgbackrest/pgbackrest/issues/1806); Ticket [#1913](https://github.com/pgbackrest/pgbackrest/issues/1913); Demande d’intégration [#1916](https://github.com/pgbackrest/pgbackrest/pull/1916)

  Développement dans [v2.42](#v242-release-notes) :

  [`1ea6a41`](https://github.com/pgbackrest/pgbackrest/commit/1ea6a4142e47e2e0b56911ad1f028dfcddc5fd64) Améliorer les mises à jour des fichiers du manifeste. ; Demande d’intégration [#1888](https://github.com/pgbackrest/pgbackrest/pull/1888)

  [`c647bcb`](https://github.com/pgbackrest/pgbackrest/commit/c647bcb50954f623d29104cdb8a1457ed8e94579) Ajouter des indicateurs au manifeste pour le traitement des fichiers pendant la sauvegarde. ; Demande d’intégration [#1889](https://github.com/pgbackrest/pgbackrest/pull/1889)

  [`102ce5d`](https://github.com/pgbackrest/pgbackrest/commit/102ce5dee47e8d9a8d2eeaf2b2cc2bac105914ef) Ajouter une liste persistante des références au manifeste. ; Demande d’intégration [#1890](https://github.com/pgbackrest/pgbackrest/pull/1890)

  [`ac99201`](https://github.com/pgbackrest/pgbackrest/commit/ac99201c0ebde616279214e600e49fdf506f7469) Ajouter bufferSize à cvtUInt64FromVarInt128() pour limiter davantage les lectures.

  [`5602f17`](https://github.com/pgbackrest/pgbackrest/commit/5602f179a177a8513b96c762590829c012c28175) Ajouter l'encodage et le décodage varint-128 à IoRead/IoWrite. ; Demande d’intégration [#1891](https://github.com/pgbackrest/pgbackrest/pull/1891)

  [`352cbf1`](https://github.com/pgbackrest/pgbackrest/commit/352cbf1d5738a720292b5067051a05efc2b9a8ac) Convertir les booléens de ManifestFile en champs de bits.

  [`e7e106f`](https://github.com/pgbackrest/pgbackrest/commit/e7e106f781be01027d4829b258902549eb36eb7b) Utiliser un stockage en lecture seule pour calculer la somme de contrôle dans restoreFile().

  [`909be41`](https://github.com/pgbackrest/pgbackrest/commit/909be412f8ad0d87f23ce2a2dbca94c3e0732f9f) Permuter les tests unitaires command/backup et command/restore.

  [`1730ef4`](https://github.com/pgbackrest/pgbackrest/commit/1730ef4ac3d88137bd218e6128b0107a8bf2c121) Ajouter l'indicateur noTruncate à storageNewWriteP(). ; Demande d’intégration [#1898](https://github.com/pgbackrest/pgbackrest/pull/1898)

  [`fee38c2`](https://github.com/pgbackrest/pgbackrest/commit/fee38c2c7cc3ae318bf0d3b50fe23c22900c2311) Transmettre les filtres au stockage distant sous forme de tableau de gestionnaires.

  [`5fceee8`](https://github.com/pgbackrest/pgbackrest/commit/5fceee88a9439460bf24082f275ec2e695cc6bf6) Ajouter backupFileRepoPathP().

  [`221db61`](https://github.com/pgbackrest/pgbackrest/commit/221db610d2a054ed00ad27377663941abfb9fb98) Raccourcir les noms dans la matrice des tests d'intégration real/all.

  [`c9db7bc`](https://github.com/pgbackrest/pgbackrest/commit/c9db7bc274211820030c4ab6ab8c70c1b1896254) Modifier cipherBlockNew() pour autoriser des paramètres optionnels.

  [`58b3c91`](https://github.com/pgbackrest/pgbackrest/commit/58b3c91babc6af9e003e5ef09bf99becf8a6f827) Ajouter un mode brut à CipherBlock pour économiser de l'espace.

**Améliorations :**

- Conservez un seul index de groupe avec les valeurs par défaut. (*Révisé par Stefan Fercot.*)

  Une option non applicable, par exemple `repo2-s3-key` lorsque `repo2-type` n'est pas `s3`, pouvait ajouter un dépôt fantôme ne contenant que des valeurs par défaut. Les index de dépôt et PostgreSQL n'ayant que des valeurs par défaut sont désormais supprimés, sauf s'il ne reste aucun autre index.

  Demande d’intégration [#2011](https://github.com/pgbackrest/pgbackrest/pull/2011); Commit [`1648c13`](https://github.com/pgbackrest/pgbackrest/commit/1648c133d6bc1ffd0682ae6219934d00295aa580)

**Améliorations de la documentation :**

- Ajouter des instructions explicites pour la mise à jour entre les versions `2.x`. (*Contribution de Christophe Courtois. Révisé par David Steele.*)

  Une nouvelle section du guide utilisateur explique que les mises à niveau entre versions `2.x` nécessitent uniquement l'installation des nouveaux binaires. Un retour à une version antérieure est également possible si aucune fonctionnalité non prise en charge par cette version n'a été utilisée.

  Ticket [#1774](https://github.com/pgbackrest/pgbackrest/issues/1774); Demande d’intégration [#1993](https://github.com/pgbackrest/pgbackrest/pull/1993); Commit [`15d5dcd`](https://github.com/pgbackrest/pgbackrest/commit/15d5dcdd3bb387aab28bbe7262011c38c7d6d22c)
- Supprimer les références à SSH rendues obsolètes avec l'introduction de TLS.

  L'aide de `repo-host`, `pg-host` et de leurs options de port ne présente plus SSH comme le seul protocole distant. Les détails sur la compression SSH ont également été supprimés.

  Commit [`c5907a2`](https://github.com/pgbackrest/pgbackrest/commit/c5907a2e7193ca8f79cf56dca23e0df118e686c3)

### Notes de version v2.44 {#v244-release-notes}

*Supprimer le support de PostgreSQL 9.0/9.1/9.2*

*Sortie le 30 janvier 2023*

**Améliorations :**

- Supprimer la prise en charge de PostgreSQL `9.0`/`9.1`/`9.2`. (*Révisé par Stefan Fercot.*)

  pgBackRest prend désormais en charge dix versions de PostgreSQL : les cinq versions encore prises en charge et les cinq dernières versions arrivées en fin de vie. À partir de PostgreSQL 15, cela exclut `9.0`, `9.1` et `9.2`.

  Demande d’intégration [#1941](https://github.com/pgbackrest/pgbackrest/pull/1941); Commit [`77c721e`](https://github.com/pgbackrest/pgbackrest/commit/77c721eb635c6d757d2d5ed6f2ffc083720c10a7)
- Erreur de restauration lorsque aucune sauvegarde ne correspond à la version actuelle de PostgreSQL. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Soulou.*)

  Après un `stanza-upgrade` sans nouvelle sauvegarde, la restauration utilisait la dernière sauvegarde, issue de la version précédente de PostgreSQL. Les réplicas construits ainsi pouvaient échouer. La restauration signale désormais une erreur dans ce cas, sauf si `set`, `type=time` ou `type=lsn` est spécifié.

  Ticket [#1942](https://github.com/pgbackrest/pgbackrest/issues/1942); Demande d’intégration [#1967](https://github.com/pgbackrest/pgbackrest/pull/1967); Commit [`b9be4fa`](https://github.com/pgbackrest/pgbackrest/commit/b9be4fa54039e2c79fad0dc1552c7ffaf883004c)
- Ajouter le contrôle de plage pour chaque `compress-type` via `compress-level`. (*Révisé par Stefan Fercot. Suggéré par gkleen, ViperRu.*)

  La plage de `compress-level` était `0-9` pour tous les `compress-type`. Cette plage convient à `gz`, mais ne représente qu'une partie des valeurs autorisées par `lz4` et `zst`. Chaque type possède désormais sa propre plage, par exemple de `-7` à `22` pour `zst`.

  Ticket [#1216](https://github.com/pgbackrest/pgbackrest/issues/1216); Ticket [#1931](https://github.com/pgbackrest/pgbackrest/issues/1931); Demande d’intégration [#1962](https://github.com/pgbackrest/pgbackrest/pull/1962); Commit [`44da314`](https://github.com/pgbackrest/pgbackrest/commit/44da314adb2b63f96b1d571f822e91a0e412e984)

**Améliorations de la documentation :**

- Ajouter un avertissement concernant l'activation de « namespace hiérarchique » sur le stockage Azure. (*Révisé par Stefan Fercot. Suggéré par Vojtech Galda, Pluggi, asjonos.*)

  Lorsque l'espace de noms hiérarchique est activé, Azure exige la suppression séparée des répertoires et `expire` échoue. Le guide utilisateur indique désormais de ne pas l'activer.

  Ticket [#1770](https://github.com/pgbackrest/pgbackrest/issues/1770); Demande d’intégration [#1980](https://github.com/pgbackrest/pgbackrest/pull/1980); Commit [`3aea997`](https://github.com/pgbackrest/pgbackrest/commit/3aea997df5ace85251d0579ccbe13fa938f587ee)
- Ajouter un remplacement pour les sauts de ligne dans l'exemple de surveillance. (*Révisé par Stefan Fercot. Suggéré par rudonx, gmustdie, Ivan Shelestov.*)

  L'exemple de supervision échouait lorsque la sortie de `info` contenait un saut de ligne, par exemple dans certains messages d'erreur, car `COPY` convertit `\n` en un saut de ligne rejeté par `jsonb`. L'exemple remplace désormais les sauts de ligne avant la conversion en `jsonb`.

  Ticket [#1910](https://github.com/pgbackrest/pgbackrest/issues/1910); Demande d’intégration [#1963](https://github.com/pgbackrest/pgbackrest/pull/1963); Commit [`ae258f6`](https://github.com/pgbackrest/pgbackrest/commit/ae258f604e634f1d2a760ffdb92dd359fd1129bb)
- Préciser le comportement de `target-action` sur différentes versions de PostgreSQL. (*Contribution de Chris Bandy. Révisé par David Steele, Anton Kurochkin, Stefan Fercot. Suggéré par Anton Kurochkin, Chris Bandy.*)

  L'effet de `pause` dépend de `hot_standby` et de la version de PostgreSQL. Avec `hot_standby=off`, `pause` agit comme `shutdown` sur PostgreSQL >= 12 et comme `promote` sur les versions précédentes.

  Ticket [#987](https://github.com/pgbackrest/pgbackrest/issues/987); Ticket [#1314](https://github.com/pgbackrest/pgbackrest/issues/1314); Demande d’intégration [#1960](https://github.com/pgbackrest/pgbackrest/pull/1960); Commit [`84a3ff8`](https://github.com/pgbackrest/pgbackrest/commit/84a3ff8b7ac1243c0b47c6585697f4fcf3c12065)
- Mises à jour et clarifications apportées à la page d'accueil. (*Révisé par Stefan Fercot.*)

  La section affirmant que les autres solutions de sauvegarde ne prennent pas en charge le traitement parallèle n'était plus exacte et a été reformulée. D'autres sections ont été mises à jour pour employer la terminologie actuelle et gagner en clarté.

  Demande d’intégration [#1966](https://github.com/pgbackrest/pgbackrest/pull/1966); Commit [`36ee30d`](https://github.com/pgbackrest/pgbackrest/commit/36ee30d118ce6cc7720653a3d3a49a06c655c463)
- Ajouter le mode sombre au site web. (*Suggéré par Stephen Frost.*)

  Le site utilise des couleurs sombres lorsque le navigateur préfère un thème sombre.

  Commit [`ed818b3`](https://github.com/pgbackrest/pgbackrest/commit/ed818b31867c640d72ef829dd36cd0a7feff12df)

### Notes de version v2.43 {#v243-release-notes}

*Correction de bogue*

*Sortie le 28 novembre 2022*

**Correctifs de bogues :**

- Corriger la référence manquante dans une sauvegarde différentielle/incrémentielle. (*Révisé par Stefan Fercot. Signalement par Marcel Borger, ulfedf, jaymefSO.*)

  Dans la v2.42, une sauvegarde différentielle ou incrémentale échouait avec « unable to find '...' in string list » si sa sauvegarde précédente provenait d'une version antérieure. La liste des références construite à partir d'un ancien manifeste inclut désormais l'étiquette de la sauvegarde elle-même.

  [`28f6604`](https://github.com/pgbackrest/pgbackrest/commit/28f660482aa5abb97850a9d7c89c2e5e9f23a4c9) Déplacer le test de manifestBackupLabelSet() dans le test unitaire info/manifest.

  [`c4bf775`](https://github.com/pgbackrest/pgbackrest/commit/c4bf775099c85e3cd081f9c1ce35efd4c71d9161) Corriger la référence manquante dans une sauvegarde diff/incr. ; Ticket [#1933](https://github.com/pgbackrest/pgbackrest/issues/1933); Demande d’intégration [#1935](https://github.com/pgbackrest/pgbackrest/pull/1935)

**Améliorations :**

- Ajouter un indicateur lorsque l'option est spécifiée sans index. (*Révisé par Stefan Fercot.*)

  Une option nécessitant un index, comme `repo-storage-ca-file`, produit désormais une erreur accompagnée d'un indice montrant le nom indexé, par exemple `repo1-storage-ca-file`. Une option obsolète reçoit aussi un indice indiquant son nom actuel.

  Ticket [#1925](https://github.com/pgbackrest/pgbackrest/issues/1925); Demande d’intégration [#1929](https://github.com/pgbackrest/pgbackrest/pull/1929); Commit [`3f363cb`](https://github.com/pgbackrest/pgbackrest/commit/3f363cb3aed1a7c6836ee6c32eae600129a6f6b8)

### Notes de version v2.42 {#v242-release-notes}

*Correctifs de bogues*

*Sortie le 22 novembre 2022*

**Correctifs de bogues :**

- Corriger une fuite mémoire dans le bundle de fichiers `backup`/`restore`. (*Révisé par John Morris. Testé par Oscar. Signalement par Oscar.*)

  La restauration ne libérait certains objets d'E/S des fichiers regroupés qu'après la restauration de tous les fichiers du regroupement. Avec de nombreux petits fichiers, la mémoire augmentait jusqu'à l'échec avec « unable to allocate ». La sauvegarde présentait une fuite similaire, plus faible, lors d'une reprise.

  Ticket [#1877](https://github.com/pgbackrest/pgbackrest/issues/1877); Demande d’intégration [#1878](https://github.com/pgbackrest/pgbackrest/pull/1878); Commit [`cd8db7d`](https://github.com/pgbackrest/pgbackrest/commit/cd8db7d9e53e041ad6fb31f2f015541c1d24abc2)
- Corriger une erreur de protocole lors d'une lecture partielle d'un fichier distant. (*Révisé par Stephen Frost.*)

  Une lecture distante interrompue prématurément ou en échec laissait le protocole dans un état incorrect. La commande suivante échouait avec « client state is 'data-get' but expected 'idle' », et l'erreur initiale était perdue. Le reste du fichier est désormais lu lors de sa fermeture.

  [`ea162e8`](https://github.com/pgbackrest/pgbackrest/commit/ea162e821634919b7c839e866b99bf82010dbacc) Déplacer storageReadRemoteOpen() dans le module storage/remote/read.

  [`7967c75`](https://github.com/pgbackrest/pgbackrest/commit/7967c750d83466d030081e9deb1d70a1ba240271) Corriger l'erreur de protocole lors d'une lecture courte d'un fichier distant. ; Demande d’intégration [#1900](https://github.com/pgbackrest/pgbackrest/pull/1900)

**Améliorations :**

- Ne pas stocker de références pour les fichiers de longueur nulle lors du regroupement. (*Révisé par Stefan Fercot.*)

  Les sauvegardes diff/incr regroupées stockaient une référence à une sauvegarde précédente pour les fichiers de longueur nulle, qui ne sont stockés dans aucune sauvegarde. La référence était ignorée à la restauration mais occupait de l'espace dans le manifeste.

  Demande d’intégration [#1887](https://github.com/pgbackrest/pgbackrest/pull/1887); Commit [`f981fb4`](https://github.com/pgbackrest/pgbackrest/commit/f981fb45d9931e597afec764e13b1a53d8365d25)
- Utiliser des descriptions plus générales pour `pg_start_backup()`/`pg_stop_backup()`. (*Révisé par Greg Sabino Mullane, David Christensen. Suggéré par Greg Sabino Mullane.*)

  PostgreSQL 15 a renommé ces fonctions en `pg_backup_start()`/`pg_backup_stop()`. Les journaux et la documentation utilisent désormais des descriptions indépendantes de la version de PostgreSQL.

  Demande d’intégration [#1901](https://github.com/pgbackrest/pgbackrest/pull/1901); Commit [`ddd966c`](https://github.com/pgbackrest/pgbackrest/commit/ddd966cadc30440a81100144204d4084a0f2ac3a)

**Améliorations de la suite de tests :**

- Mettre à jour l'option `test.pl` `--psql-bin` pour qu'elle corresponde à l'aide en ligne de commande. (*Contribution de Koshi Shibagaki. Révisé par David Steele.*)

  L'aide indiquait `--psql-bin`, mais l'option s'appelait `--pgsql-bin`. L'option porte désormais le nom indiqué dans l'aide.

  Demande d’intégration [#1920](https://github.com/pgbackrest/pgbackrest/pull/1920); Commit [`3ad5884`](https://github.com/pgbackrest/pgbackrest/commit/3ad588443b452e04f3abcc107e825dc47e078103)

### Notes de version v2.41 {#v241-release-notes}

*Annotations de sauvegarde*

*Sortie le 19 septembre 2022*

**Correctifs de bogues :**

- Correction de l'expiration incorrecte du délai pour les dépôts non par défaut. (*Révisé par Stefan Fercot. Signalement par Adam Brusselback.*)

  Lorsque `expire` était lancé sans `repo`, la valeur temporelle de `repo-retention-full` de chaque dépôt était lue dans le dépôt au plus petit numéro. Chaque dépôt utilise désormais sa propre valeur.

  Ticket [#1852](https://github.com/pgbackrest/pgbackrest/issues/1852); Demande d’intégration [#1854](https://github.com/pgbackrest/pgbackrest/pull/1854); Commit [`eda7f81`](https://github.com/pgbackrest/pgbackrest/commit/eda7f81ee4fd6818ce458768144fc3fc1e1f0f21)
- Correction du problème survenant lors de l'affichage récursif des répertoires avec un filtre. (*Révisé par Stephen Frost. Signalement par Efremov Egor.*)

  `repo-ls` avec `recurse` et `filter` pouvait échouer avec une double libération ou une erreur de segmentation lorsque la dernière entrée d'un répertoire était un sous-répertoire non vide. Une liste parente était libérée avant le traitement des entrées de ses sous-répertoires.

  Ticket [#1870](https://github.com/pgbackrest/pgbackrest/issues/1870); Demande d’intégration [#1871](https://github.com/pgbackrest/pgbackrest/pull/1871); Commit [`c39c9f2`](https://github.com/pgbackrest/pgbackrest/commit/c39c9f220ed328b4175d912e109697b726e9ea9b)

**Fonctionnalités :**

- Annotations clé/valeur pour la sauvegarde. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Adam Berlin.*)

  Ajoutez des annotations clé/valeur à une sauvegarde avec l'option `annotation` de `backup`, puis ajoutez-les, modifiez-les ou supprimez-les ultérieurement avec la nouvelle commande `annotate`. La commande `info` affiche les annotations dans la sortie texte lorsque `set` est spécifié et les inclut toujours dans la sortie JSON.

  Ticket [#1709](https://github.com/pgbackrest/pgbackrest/issues/1709); Demande d’intégration [#1724](https://github.com/pgbackrest/pgbackrest/pull/1724); Commit [`381fd0a`](https://github.com/pgbackrest/pgbackrest/commit/381fd0a5a4de61624615b150ba98beeafac31f7e)

**Améliorations :**

- Prise en charge `--set` dans la sortie JSON pour la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Anton Kurochkin.*)

  Avec `set`, la sortie JSON de `info` comprend désormais les détails déjà présents dans la sortie texte, notamment les listes d'erreurs et de tablespaces.

  Ticket [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Demande d’intégration [#1501](https://github.com/pgbackrest/pgbackrest/pull/1501); Commit [`db75ffd`](https://github.com/pgbackrest/pgbackrest/commit/db75ffd27037d690a11eb02902f929250fe2bf5b)
- Permettre la configuration de la taille des morceaux à téléverser pour les magasins d'objets. (*Révisé par Stefan Fercot. Suggéré par Anton Glushakov.*)

  Définissez `repo-storage-upload-chunk-size` pour changer la taille de chaque morceau envoyé vers S3, GCS ou Azure. Des morceaux plus grands peuvent améliorer les performances, mais consomment davantage de mémoire. Les valeurs par défaut restent inchangées.

  [`ff1188f`](https://github.com/pgbackrest/pgbackrest/commit/ff1188f92dfc9e8f6d4aeca8b71a9886f24f58b4) Autoriser la balise quote dans l'aide en ligne de commande.

  [`b05d31f`](https://github.com/pgbackrest/pgbackrest/commit/b05d31f531b55b747175cf94c963f95574c54d2b) Permettre de configurer la taille des morceaux d'envoi vers les stockages objet. ; Ticket [#1843](https://github.com/pgbackrest/pgbackrest/issues/1843); Demande d’intégration [#1847](https://github.com/pgbackrest/pgbackrest/pull/1847)
- Mettre à jour les horodatages du fichier archive.info après une sauvegarde réussie. (*Révisé par Stefan Fercot. Suggéré par Alex Richman.*)

  `archive.info` et sa copie n'étaient écrits que par `stanza-create` et `stanza-upgrade`. Une politique de cycle de vie du stockage objet supprimant les anciens fichiers pouvait donc les effacer. Leurs horodatages sont désormais mis à jour après chaque sauvegarde réussie.

  Ticket [#1853](https://github.com/pgbackrest/pgbackrest/issues/1853); Demande d’intégration [#1855](https://github.com/pgbackrest/pgbackrest/pull/1855); Commit [`3b5df1e`](https://github.com/pgbackrest/pgbackrest/commit/3b5df1e089234d425dd225f8c1976755dc947c8a)
- Déplacer la vérification du timeline de la base de secours après le point de contrôle. (*Révisé par Stefan Fercot. Testé par Keith Fiske. Suggéré par Keith Fiske.*)

  La vérification de la timeline du serveur de secours utilisait le `pg_control` antérieur au début de la sauvegarde. Juste après une promotion, la nouvelle timeline pouvait ne pas encore avoir été écrite dans `pg_control`, et la sauvegarde échouait avec « standby is on timeline ... but expected ... ». La vérification s'effectue désormais après le point de contrôle.

  Ticket [#1816](https://github.com/pgbackrest/pgbackrest/issues/1816); Demande d’intégration [#1819](https://github.com/pgbackrest/pgbackrest/pull/1819); Commit [`c267ba5`](https://github.com/pgbackrest/pgbackrest/commit/c267ba51b1778b5872f4ee928a9614545d743f3f)
- Améliorer le message d'avertissement lors de la reprise d'une sauvegarde. (*Suggéré par Cynthia Shang.*)

  L'avertissement laissait penser que l'utilisateur devait intervenir. Il précise désormais que les fichiers invalides seront supprimés, puis que la sauvegarde reprendra.

  Commit [`cbbe93f`](https://github.com/pgbackrest/pgbackrest/commit/cbbe93f592d8097393c5ffe214f0a8c5fb0549c1)

**Améliorations de la documentation :**

- Ajouter le chemin absolu pour `kill` dans `pgbackrest.service`. (*Suggéré par Don Seiler.*)

  L'exemple `pgbackrest.service` utilise désormais `/bin/kill` dans `ExecReload`. Les anciennes versions de systemd exigent un chemin absolu.

  Commit [`e9ff524`](https://github.com/pgbackrest/pgbackrest/commit/e9ff5248039eedb25da2fee550ec64fcebbc51c7)

### Notes de version v2.40 {#v240-release-notes}

*Prise en charge d’OpenSSL 3*

*Sortie le 18 juillet 2022*

**NOTE AUX PAQUETEURS** : Une version expérimentale de la construction avec meson a été ajoutée, mais les paqueteurs doivent continuer à utiliser la construction autoconf/make pour le moment.

**Améliorations :**

- Prise en charge d'OpenSSL 3. (*Révisé par Stephen Frost.*)

  pgBackRest peut désormais être compilé avec OpenSSL 3. Les avertissements de dépréciation sont masqués, et une fin de fichier inattendue est détectée à l'aide des codes d'erreur d'OpenSSL 3.

  Demande d’intégration [#1767](https://github.com/pgbackrest/pgbackrest/pull/1767); Commit [`08242ee`](https://github.com/pgbackrest/pgbackrest/commit/08242ee6ac93b9eb9c05cc39e3db15bbafb9052c)
- Créer un instantané lors de l'affichage du contenu d'un chemin. (*Révisé par John Morris, Stephen Frost.*)

  Un chemin listé sans tri était lu pendant le traitement de ses entrées. Lorsque des fichiers étaient supprimés durant l'énumération, certains systèmes de fichiers omettaient des fichiers encore présents, et le chemin ne pouvait pas être supprimé. Les énumérations utilisent désormais toujours un instantané du chemin.

  [`61ca9b5`](https://github.com/pgbackrest/pgbackrest/commit/61ca9b58a000aa8789ef3267682519bdb15e8a6b) Remplacer hrnStorageInfoListCallback() par TEST_STORAGE_LIST() dans les tests.

  [`1c0bf0b`](https://github.com/pgbackrest/pgbackrest/commit/1c0bf0b15da8c0d15cc639851ff1d1bd05b51d06) Réordonner les vérifications des utilisateurs et groupes nuls dans le protocole distant et ajouter des tests.

  [`72960bb`](https://github.com/pgbackrest/pgbackrest/commit/72960bbf179b4e8051bd4fc50be57d95159e9e13) Renommer strTrunc() en strTruncIdx() et ajouter strTrunc().

  [`75623d4`](https://github.com/pgbackrest/pgbackrest/commit/75623d4583bfdaccb3a19b935fd04d744b363923) Créer un instantané lors de l'énumération du contenu d'un chemin. ; Ticket [#1754](https://github.com/pgbackrest/pgbackrest/issues/1754); Demande d’intégration [#1805](https://github.com/pgbackrest/pgbackrest/pull/1805)
- Forcer `target-timeline=current` lors de la restauration `type=immediate`. (*Révisé par Stephen Frost.*)

  Avec PostgreSQL >= 12, la timeline cible par défaut est `latest`, et la récupération pouvait échouer si la dernière timeline du dépôt était inaccessible depuis la sauvegarde. Une restauration avec `type=immediate` ne changeant pas de timeline, elle fixe désormais la timeline cible à `current`.

  Demande d’intégration [#1814](https://github.com/pgbackrest/pgbackrest/pull/1814); Commit [`364af16`](https://github.com/pgbackrest/pgbackrest/commit/364af1635d40431276cc6fd87d6ddd689b611e09)
- Tronquer les fichiers pendant une restauration delta (`restore`) lorsqu'ils sont plus grands que prévu. (*Révisé par Stephen Frost.*)

  La restauration delta copiait un fichier du dépôt dès que sa taille différait de celle du manifeste. Un fichier plus grand est désormais tronqué à la taille du manifeste et n'est copié que si sa somme de contrôle diffère. Les fichiers auxquels des données ont seulement été ajoutées, comme les journaux, ne sont plus copiés.

  Demande d’intégration [#1758](https://github.com/pgbackrest/pgbackrest/pull/1758); Commit [`7ec51e7`](https://github.com/pgbackrest/pgbackrest/commit/7ec51e7e6279ea576ad3b4b5c2ea1fc389d08ab5)
- Désactiver l'enregistrement du manifeste incrémentiel lorsque `resume=n`. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Pendant une sauvegarde, le manifeste est enregistré périodiquement pour permettre une reprise. Ces enregistrements sont désormais omis lorsque `resume=n`.

  Demande d’intégration [#1760](https://github.com/pgbackrest/pgbackrest/pull/1760); Commit [`60d70fa`](https://github.com/pgbackrest/pgbackrest/commit/60d70fa66fc3f709914f40dd088bac1b467001f2)
- Définir le pourcentage de progression de la sauvegarde sur zéro avant le début de la copie. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  La progression d'une sauvegarde n'était rapportée qu'après la copie du premier fichier. Elle est désormais fixée à zéro dès le début de la copie.

  Demande d’intégration [#1759](https://github.com/pgbackrest/pgbackrest/pull/1759); Commit [`38ad283`](https://github.com/pgbackrest/pgbackrest/commit/38ad2838d553febae1b7fe0244d942dfaa9cf548)
- Utiliser le drapeau S3 `IsTruncated` pour déterminer la continuation de la liste. (*Révisé par John Morris. Testé par Soulou. Suggéré par Christian Montagne.*)

  Les versions récentes de Scality envoient un `NextContinuationToken` vide lorsque la liste n'est pas tronquée, ce qui provoquait une boucle infinie. L'indicateur `IsTruncated` détermine désormais s'il faut poursuivre la liste ; un jeton absent ou vide pour une liste tronquée constitue une erreur.

  Ticket [#1748](https://github.com/pgbackrest/pgbackrest/issues/1748); Demande d’intégration [#1783](https://github.com/pgbackrest/pgbackrest/pull/1783); Commit [`845d82f`](https://github.com/pgbackrest/pgbackrest/commit/845d82f6825d4101e6a465a435ef056ff6ec15a2)

**Correctifs de bogues dans la documentation :**

- Ignorer les options internes dans la référence de configuration. (*Signalement par Francisco Miguel Biete Banon.*)

  Les options internes pour certaines commandes seulement apparaissaient dans la référence de configuration. L'aide en ligne de commande n'était pas affectée.

  Commit [`2643050`](https://github.com/pgbackrest/pgbackrest/commit/2643050be0dc4b7363c434f58373919bd6fdac68)

**Améliorations de la documentation :**

- Ajouter un lien vers la configuration PostgreSQL dans la section hôte du dépôt. (*Révisé par Stefan Fercot. Suggéré par Julien Cigar.*)

  Demande d’intégration [#1809](https://github.com/pgbackrest/pgbackrest/pull/1809); Commit [`74a4ac8`](https://github.com/pgbackrest/pgbackrest/commit/74a4ac801db921f7b11b63b9f927228c6a6af861)

**Améliorations de la suite de tests :**

- Ajouter la construction expérimentale avec Meson. (*Révisé par Eli Schwartz, Sam Bassaly.*)

  Meson a une syntaxe plus simple et de meilleures performances qu'autoconf/make. Il est utilisé pour la génération de code et les compilations de test, et refuse toute compilation autre que de débogage. Les empaqueteurs doivent continuer d'utiliser autoconf/make.

  [`2feaaea`](https://github.com/pgbackrest/pgbackrest/commit/2feaaeaac803d6c0193477b56dbeb622fd991156) Ajouter l'extension .inc aux fichiers C inclus dans d'autres fichiers C.

  [`b8fc20d`](https://github.com/pgbackrest/pgbackrest/commit/b8fc20d5b8e7ca003ff39f29ea6e3ba57653f55c) Ajouter une compilation Meson expérimentale. ; Demande d’intégration [#1765](https://github.com/pgbackrest/pgbackrest/pull/1765)

  [`665da12`](https://github.com/pgbackrest/pgbackrest/commit/665da12ae7f519077512e60ce3a5ec6c6a9997fd) Généraliser le commentaire d'inclusion dans meson.build.

  [`9fd85a1`](https://github.com/pgbackrest/pgbackrest/commit/9fd85a104ad56061b028afd9057ce8c1d636d3dd) Désactiver meson sauf pour les compilations de débogage.

  [`59f148b`](https://github.com/pgbackrest/pgbackrest/commit/59f148bf6ea8c090d4d65ce5b135a71501e8ae22) Générer -fmacro-prefix-map pour retirer le chemin relatif de __FILE__.

  [`0eccbc8`](https://github.com/pgbackrest/pgbackrest/commit/0eccbc8bf47073ab8ec1f13fed9865d0bd7c3635) Faire fonctionner les compilations Meson avec la version 0.45.
- Permettre à tout chemin d'être passé à l'option `--test-path`. (*Contribution de Andrey Sokolov. Révisé par David Steele.*)

  Demande d’intégration [#1764](https://github.com/pgbackrest/pgbackrest/pull/1764); Commit [`29b2a54`](https://github.com/pgbackrest/pgbackrest/commit/29b2a54fcc74457af5c63ffb505c5fbb24bb2ade)
- Corriger l'erreur de compilation lorsque `DEBUG_EXEC_TIME` est défini sans `DEBUG`. (*Contribution de Andrey Sokolov. Révisé par David Steele.*)

  Sans `DEBUG`, le `ASSERT()` utilisant l'heure de début était remplacé par une expression vide, et la variable inutilisée provoquait une erreur de compilation. La vérification utilise désormais `CHECK()`.

  Demande d’intégration [#1775](https://github.com/pgbackrest/pgbackrest/pull/1775); Commit [`1a00ab1`](https://github.com/pgbackrest/pgbackrest/commit/1a00ab10033e9ac6e6f797627567e8b91e143432)

### Notes de version v2.39 {#v239-release-notes}

*Vérification et regroupement de fichiers*

*Sortie le 16 mai 2022*

**Correctifs de bogues :**

- Corriger l'erreur levée par `FINALLY()` provoquant une boucle infinie. (*Révisé par Stephen Frost.*)

  Une erreur levée dans un bloc `FINALLY()` revenait dans le même bloc, où elle risquait d'être levée de nouveau, provoquant une boucle infinie. `FINALLY()` ne s'exécute désormais qu'une fois.

  [`9a271e9`](https://github.com/pgbackrest/pgbackrest/commit/9a271e925c6239fbd3577f9827c34940e7e43ae4) Corriger la boucle infinie causée par une erreur levée dans FINALLY(). ; Demande d’intégration [#1732](https://github.com/pgbackrest/pgbackrest/pull/1732)

  [`ef4c4ab`](https://github.com/pgbackrest/pgbackrest/commit/ef4c4ab8525f81c9ed22c7e82ed12096e81703c5) Utiliser une variable plutôt qu'une fonction pour suivre l'état de FINALLY(). ; Demande d’intégration [#1744](https://github.com/pgbackrest/pgbackrest/pull/1744)
- Erreur sur toutes les échecs de verrouillage, sauf lorsque le verrou est détenu par un autre processus. (*Révisé par Reid Thompson. Testé par Geir Råness. Signalement par Geir Råness.*)

  `archive-get`/`archive-push` ne signalaient pas d'erreur lorsque le verrou ne pouvait pas être pris pour une autre raison, par exemple des permissions, et le processus asynchrone n'était pas lancé. L'utilisateur obtenait un message d'échec générique, sans journal asynchrone. Ces échecs produisent désormais des erreurs.

  Ticket [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Demande d’intégration [#1730](https://github.com/pgbackrest/pgbackrest/pull/1730); Commit [`9629908`](https://github.com/pgbackrest/pgbackrest/commit/962990869454b15db058f4037dbc0b1b611fc95e)

**Fonctionnalités :**

- Regroupement des fichiers de sauvegarde pour une meilleure prise en charge des petits fichiers. (*Révisé par Reid Thompson, Stefan Fercot, Chris Bandy.*)

  Le regroupement stocke les petits fichiers ensemble dans le dépôt afin d'économiser du temps et de l'espace pendant la sauvegarde, surtout sur les stockages objet où la création de chaque fichier coûte cher. Activez-le avec `repo-bundle` et ajustez-le avec `repo-bundle-size` et `repo-bundle-limit`. La restauration lit les fichiers adjacents d'un regroupement en une seule lecture.

  [`4d2fef1`](https://github.com/pgbackrest/pgbackrest/commit/4d2fef1c37d357965f0ffb9af0d7489f3be1371b) Supprimer un test redondant de restoreFile() et améliorer la couverture.

  [`5141370`](https://github.com/pgbackrest/pgbackrest/commit/514137040e60e8fff0e7f42f43b493113abae5ff) Ajouter le paramètre limit à ioCopyP().

  [`dca6da8`](https://github.com/pgbackrest/pgbackrest/commit/dca6da86bfe84a0cda004df1140d125db1630c90) Optimiser la commande restore pour le regroupement de fichiers. ; Ticket [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Demande d’intégration [#1683](https://github.com/pgbackrest/pgbackrest/pull/1683)

  [`0054677`](https://github.com/pgbackrest/pgbackrest/commit/0054677147121967889ead7feab0959fb19e39a6) Ajouter la journalisation des regroupements à la commande backup.

  [`3f66f42`](https://github.com/pgbackrest/pgbackrest/commit/3f66f42ef9605a83c356e4c6eb3ef47bcb12c30d) Renommer les options bundle-* en repo-bundle-*. ; Demande d’intégration [#1694](https://github.com/pgbackrest/pgbackrest/pull/1694)

  [`fe9fd2f`](https://github.com/pgbackrest/pgbackrest/commit/fe9fd2ff2d778b86c0df159aabe7644f18f6479f) Désactiver repo-hardlink lorsque repo-bundle est activé.

  [`424008d`](https://github.com/pgbackrest/pgbackrest/commit/424008d293661dfb1a167cfec2697def48057447) Autoriser les fichiers devenant vides après la construction du manifeste de sauvegarde.

  [`f405fc6`](https://github.com/pgbackrest/pgbackrest/commit/f405fc6ae281eebf4d61abb39963a9830fe2fa2f) Documenter le regroupement des fichiers de sauvegarde. ; Demande d’intégration [#1740](https://github.com/pgbackrest/pgbackrest/pull/1740)

  Développement dans [v2.38](#v238-release-notes) :

  [`a79034a`](https://github.com/pgbackrest/pgbackrest/commit/a79034ae2f6a8ec66b84c62ab6cd4042d2c1a249) Ajouter la lecture par plage à tous les pilotes de stockage. ; Demande d’intégration [#1619](https://github.com/pgbackrest/pgbackrest/pull/1619)

  [`b791f1c`](https://github.com/pgbackrest/pgbackrest/commit/b791f1c82f53fa16866837d4544b58243c682f7f) Gérer les propriétaires lors de la restauration sans modifier la structure interne du manifeste.

  [`f84909f`](https://github.com/pgbackrest/pgbackrest/commit/f84909f85f7dfb202ac812c67665cc590a5acad4) Corriger la gestion du décalage de lecture Posix après une erreur.

  [`4ca0590`](https://github.com/pgbackrest/pgbackrest/commit/4ca0590a51a665535fbba903b8f55e10557b606a) Refactoriser backupProcessQueue() pour utiliser la structure BackupJobData.

  [`16559d9`](https://github.com/pgbackrest/pgbackrest/commit/16559d9e421c66596d21b047c8afe1b2c96ccd82) Utiliser la constante PG_FILE_POSTMTRPID lorsque cela convient.

  [`8c062e1`](https://github.com/pgbackrest/pgbackrest/commit/8c062e1af824c3dc80ff94b3df8d433f95e88d0f) Supprimer l'indicateur primary du manifeste. ; Demande d’intégration [#1630](https://github.com/pgbackrest/pgbackrest/pull/1630)

  [`b0db4b8`](https://github.com/pgbackrest/pgbackrest/commit/b0db4b8ff00db913cb69308017a56155d6070830) Simplifier les permissions du chemin de base dans les tests d’intégration mock/all.

  [`4a73a02`](https://github.com/pgbackrest/pgbackrest/commit/4a73a0286387f3f2185f3f193f9c20ed0d7d926d) Simplifier les valeurs par défaut du manifeste. ; Demande d’intégration [#1631](https://github.com/pgbackrest/pgbackrest/pull/1631)

  [`575ae77`](https://github.com/pgbackrest/pgbackrest/commit/575ae77c0dee12b932469d479b2e45dbaf389737) Convertir varNewUInt64() en VARUINT64() là où c'est possible dans le manifeste.

  [`61ce586`](https://github.com/pgbackrest/pgbackrest/commit/61ce58692f3092b72833b6e9ee87037f45b3b702) Compacter les structures de fichier du manifeste pour économiser de la mémoire. ; Demande d’intégration [#1626](https://github.com/pgbackrest/pgbackrest/pull/1626)

  [`ca13f11`](https://github.com/pgbackrest/pgbackrest/commit/ca13f11b4a3858587c7055b0b2b4a8b396dd8451) Optimiser jsonFromStrInternal().

  [`e4df5b7`](https://github.com/pgbackrest/pgbackrest/commit/e4df5b7d3846134832b9315e22786f679d63a46b) Simplifier les valeurs par défaut des fichiers du manifeste. ; Demande d’intégration [#1632](https://github.com/pgbackrest/pgbackrest/pull/1632)

  [`7dd657b`](https://github.com/pgbackrest/pgbackrest/commit/7dd657b7dd163ded9fbf7caef37eea7e08bc5a37) Simplifier la construction des noms de fichiers dans command/verify.

  [`34d6495`](https://github.com/pgbackrest/pgbackrest/commit/34d649579eb3bd1530aa99f0ed1879e7d3125424) Regrouper les fichiers du dépôt pendant la sauvegarde. ; Ticket [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Demande d’intégration [#1655](https://github.com/pgbackrest/pgbackrest/pull/1655)

  [`efc09db`](https://github.com/pgbackrest/pgbackrest/commit/efc09db7b9ece6e7b7f92538d56d6ab7b9798f8f) Limiter les fichiers pouvant être regroupés. ; Ticket [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Demande d’intégration [#1662](https://github.com/pgbackrest/pgbackrest/pull/1662)

  [`e6e1122`](https://github.com/pgbackrest/pgbackrest/commit/e6e1122dbcf5e667d683295f7e7e45de4bbf56bd) Passer le fichier par référence dans manifestFileAdd().
- Commande verify pour valider le contenu d’un dépôt. (*Contribution de Cynthia Shang, Reid Thompson. Révisé par David Steele, Stefan Fercot.*)

  La commande `verify` vérifie la validité des sauvegardes et des WAL du dépôt. Définissez `output=text` pour afficher les résultats et `verbose` pour inclure les éléments vérifiés avec succès en plus des erreurs.

  Demande d’intégration [#1607](https://github.com/pgbackrest/pgbackrest/pull/1607); Commit [`65d22e4`](https://github.com/pgbackrest/pgbackrest/commit/65d22e43257d46ff6523ffbdb3af59e30deeaea5)
- Prise en charge de PostgreSQL 15. (*Révisé par Stefan Fercot.*)

  PostgreSQL 15 supprime la sauvegarde exclusive, renomme les fonctions de début et de fin de sauvegarde et supprime `pg_database.datlastsysoid`, que pgBackRest n'utilise plus.

  [`692fe49`](https://github.com/pgbackrest/pgbackrest/commit/692fe496bdb5fa6dcffeb9f85b6188ceb1df707a) Supprimer la dépendance à pg_database.datlastsysoid. ; Demande d’intégration [#1735](https://github.com/pgbackrest/pgbackrest/pull/1735)

  [`20782c8`](https://github.com/pgbackrest/pgbackrest/commit/20782c88bc8d0842d547bd5f4fecdb292e69d1f7) Prise en charge de PostgreSQL 15. ; Demande d’intégration [#1736](https://github.com/pgbackrest/pgbackrest/pull/1736)
- Affichage du pourcentage d’avancement de la sauvegarde dans la sortie `info`. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  `info` affiche le pourcentage d'avancement d'une sauvegarde sur l'hôte où elle s'exécute. La sortie JSON le fournit sous forme d'entier, égal au pourcentage multiplié par 100.

  [`d9088b2`](https://github.com/pgbackrest/pgbackrest/commit/d9088b2e2b16a89d29b967187a547976f96061fc) Afficher le pourcentage d'avancement des sauvegardes dans info. ; Ticket [#1490](https://github.com/pgbackrest/pgbackrest/issues/1490); Demande d’intégration [#1621](https://github.com/pgbackrest/pgbackrest/pull/1621)

  [`a6b1adb`](https://github.com/pgbackrest/pgbackrest/commit/a6b1adb5fd533b4b9aca29646c8acf647d872959) Supprimer un saut de ligne superflu lors de l'écriture d'un fichier de verrou.

  Développement dans [v2.38](#v238-release-notes) :

  [`22734eb`](https://github.com/pgbackrest/pgbackrest/commit/22734eb376b3183924cb7794f9111c1eeb5d92d6) Ajouter ioBufferReadNewOpen() et ioBufferWriteNewOpen().

  [`9b2f10d`](https://github.com/pgbackrest/pgbackrest/commit/9b2f10dbb49a8b869cef2c419d9957ed4c550016) Refactoriser le code de verrouillage. ; Demande d’intégration [#1643](https://github.com/pgbackrest/pgbackrest/pull/1643)
- Sélection automatique de la sauvegarde pour la commande `restore` `--type=lsn`. (*Contribution de Reid Thompson. Révisé par Stefan Fercot, David Steele.*)

  Avec `type=lsn`, la restauration choisit désormais la sauvegarde la plus récente terminée au LSN `target` ou avant celui-ci.

  [`08d9e26`](https://github.com/pgbackrest/pgbackrest/commit/08d9e269c6f03e7797584e90c53eb0743b787f60) Clarifier la vérification du type de cible dans le module de restauration.

  [`d8d4132`](https://github.com/pgbackrest/pgbackrest/commit/d8d4132118edd7f93a5b221478c85c2d213c39dd) Sélectionner automatiquement la sauvegarde pour restore --type=lsn. ; Demande d’intégration [#1706](https://github.com/pgbackrest/pgbackrest/pull/1706)

  [`ea4d73f`](https://github.com/pgbackrest/pgbackrest/commit/ea4d73f375558c237fce696f20c19d1efef00bc1) Corriger l'ordre du champ backup-lsn-stop dans le test unitaire command/restore.
- Suppression de l’avertissement relatif au WAL existant lorsque `archive-mode-check` est désactivé. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Avec `archive-mode-check=n` et des WAL envoyés depuis plusieurs hôtes, la présence dans l'archive d'un fichier WAL de même somme de contrôle est normale et ne produit plus d'avertissement. Une somme de contrôle différente reste une erreur.

  Demande d’intégration [#1711](https://github.com/pgbackrest/pgbackrest/pull/1711); Commit [`aad7171`](https://github.com/pgbackrest/pgbackrest/commit/aad7171940afdb221a03825bee6eb2f1827289f1)
- Ajout de la prise en charge d’AWS IMDSv2. (*Contribution de Nuno Pires. Révisé par David Steele.*)

  IMDSv2 protège les métadonnées d'instance fournissant les identifiants pour `repo-s3-key-type=auto`. pgBackRest se replie sur IMDSv1 si la demande de jeton IMDSv2 échoue.

  Ticket [#1685](https://github.com/pgbackrest/pgbackrest/issues/1685); Demande d’intégration [#1691](https://github.com/pgbackrest/pgbackrest/pull/1691); Commit [`21cef09`](https://github.com/pgbackrest/pgbackrest/commit/21cef09dfd03c313531dc66ba9556164ae2835ab)

**Améliorations :**

- Permettre la modification de l'option `repo-hardlink` après une sauvegarde complète. (*Révisé par Reid Thompson.*)

  Modifier `repo-hardlink` nécessitait une nouvelle sauvegarde complète. Il peut désormais être modifié à tout moment, notamment pour le désactiver en vue du regroupement de fichiers.

  Demande d’intégration [#1699](https://github.com/pgbackrest/pgbackrest/pull/1699); Commit [`7afaac0`](https://github.com/pgbackrest/pgbackrest/commit/7afaac0a3d0e43e5598d1abf548559dbe6329363)
- Améliorer la précision de la journalisation du pourcentage d'avancement pour `backup` et `restore`. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Le pourcentage d'avancement est désormais journalisé avec deux décimales, ce qui fournit des mises à jour plus fréquentes pour les sauvegardes et restaurations volumineuses.

  Demande d’intégration [#1679](https://github.com/pgbackrest/pgbackrest/pull/1679); Commit [`330e199`](https://github.com/pgbackrest/pgbackrest/commit/330e19900ee3415d920680cf6e6856bf5e8e9a69)
- Améliorer la validation des chemins pour les commandes `repo-*`. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Un chemin ne peut pas contenir `//`, un `/` final est supprimé et un chemin absolu doit se trouver sous le chemin du dépôt.

  [`5ae84d5`](https://github.com/pgbackrest/pgbackrest/commit/5ae84d5e474e95dcc00c174aa5111815a5a70ba5) Améliorer la validation des chemins pour les commandes repo-*. ; Demande d’intégration [#1697](https://github.com/pgbackrest/pgbackrest/pull/1697)

  [`19dd015`](https://github.com/pgbackrest/pgbackrest/commit/19dd015d589ed3efd31a2a238249a150fb3748c1) Corriger les problèmes de la validation améliorée des chemins pour repo-*. ; Demande d’intégration [#1751](https://github.com/pgbackrest/pgbackrest/pull/1751)
- Améliorer la commande `stop` afin qu'elle respecte l'option `stanza`. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par ragaoua.*)

  `stop` avec `force` et `stanza` ne termine désormais que les processus détenant des verrous pour cette stanza. Auparavant, il terminait les processus de toutes les stanzas.

  Ticket [#1608](https://github.com/pgbackrest/pgbackrest/issues/1608); Demande d’intégration [#1676](https://github.com/pgbackrest/pgbackrest/pull/1676); Commit [`f7ab002`](https://github.com/pgbackrest/pgbackrest/commit/f7ab002aa74dd2ca277123f7500018ae68a04c74)
- Améliorer le message d'erreur pour un `repo-azure-key` non valide. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Seth Daniel.*)

  Avec `repo-azure-key-type=shared`, la validité base64 de `repo-azure-key` est désormais vérifiée.

  Ticket [#1686](https://github.com/pgbackrest/pgbackrest/issues/1686); Demande d’intégration [#1688](https://github.com/pgbackrest/pgbackrest/pull/1688); Commit [`7c9208b`](https://github.com/pgbackrest/pgbackrest/commit/7c9208ba856a71833dc7d8f1cf8cb2b4bb4b7414)
- Ajouter une indication pour vérifier le journal sur `archive-get`/`archive-push` en cas d'erreur asynchrone. (*Révisé par Reid Thompson.*)

  Si le processus asynchrone ne peut pas écrire ses fichiers d'état, `archive-get`/`archive-push` expire avec une erreur générique. L'erreur indique désormais le chemin du journal asynchrone, qui contient l'erreur réelle.

  Ticket [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`03c71aa`](https://github.com/pgbackrest/pgbackrest/commit/03c71aa606bc0dc89303b3907e7fcbd83ace79d6)
- Ajouter `ClockError` en cas de décalage horaire ou de changement de fuseau horaire inattendu. (*Révisé par Greg Sabino Mullane, Stefan Fercot. Suggéré par Greg Sabino Mullane.*)

  Demande d’intégration [#1739](https://github.com/pgbackrest/pgbackrest/pull/1739); Commit [`5f8c9cd`](https://github.com/pgbackrest/pgbackrest/commit/5f8c9cd66a1b39a47acaddfbc3cf443ae8057519)
- Supprimer les extensions du manifeste de l'historique avant de l'afficher dans le message d'erreur. (*Révisé par Stefan Fercot.*)

  Lorsqu'une nouvelle étiquette de sauvegarde n'était pas postérieure à la dernière étiquette de l'historique, l'erreur montrait le nom du manifeste historique, par exemple `20220504-222042F_20220504-222141I.manifest.gz`. Elle n'affiche désormais que l'étiquette.

  Demande d’intégration [#1738](https://github.com/pgbackrest/pgbackrest/pull/1738); Commit [`b6bfd9f`](https://github.com/pgbackrest/pgbackrest/commit/b6bfd9f99d74b1f5e631cf6462b68342589d2b80)
- Ajouter l'utilisateur:groupe à l'erreur de permission de verrouillage. (*Révisé par Reid Thompson.*)

  Ticket [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`0055fa4`](https://github.com/pgbackrest/pgbackrest/commit/0055fa40fee2636fed88699f52e9e67cd2803f71)
- Ajouter un indice lorsque le cluster primaire est introuvable.

  L'erreur « unable to find primary cluster » inclut désormais un indice demandant si tous les clusters disponibles sont en récupération.

  Commit [`46b7b72`](https://github.com/pgbackrest/pgbackrest/commit/46b7b7287446d0bb5ed0963fd01c51fb2b08893f)

**Correctifs de bogues dans la documentation :**

- Correction d'une référence incorrecte à `stanza-update` dans le guide utilisateur. (*Corrigé par Abubakar Mohammed. Révisé par David Steele.*)

  Commit [`3dd7960`](https://github.com/pgbackrest/pgbackrest/commit/3dd796045160c4d4dbf70ec2800ad483867629f1)
- Correction de l'exemple pour l'option `repo-gcs-key-type` dans la référence de configuration. (*Révisé par Reid Thompson.*)

  L'exemple utilisait `none`, une valeur invalide. Il utilise désormais `auto`.

  Commit [`166039c`](https://github.com/pgbackrest/pgbackrest/commit/166039c0da1875581a08d41ab8a44adf95fa6db1)
- Correction de l'exemple pour `tls-server-auth` et ajout de précisions. (*Révisé par Reid Thompson.*)

  Le CN du client manquait dans l'exemple, qui est désormais `client-cn=stanza1`. L'aide précise également que les jokers ne sont pas autorisés pour le CN du client.

  Commit [`c222ce1`](https://github.com/pgbackrest/pgbackrest/commit/c222ce1a5f6f813188b7e87a3838d6dce656e0ff)

**Améliorations de la documentation :**

- Simplifier les messages concernant les versions prises en charge dans la documentation. (*Révisé par Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)

  Les guides utilisateur indiquaient des plages de versions PostgreSQL, laissant croire que les autres versions, comme PostgreSQL 12 sur RHEL, n'étaient pas prises en charge. Ces plages ont été retirées, et l'introduction explique désormais les versions couvertes par les guides.

  Demande d’intégration [#1742](https://github.com/pgbackrest/pgbackrest/pull/1742); Commit [`eefa0b1`](https://github.com/pgbackrest/pgbackrest/commit/eefa0b161a6a02b7843e18455443a4bce41cd4b9)
- Ajouter des descriptions des types d'option. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  La référence de configuration décrit désormais chaque type d'option, notamment les unités de taille, au lieu de répéter cette description pour chaque option.

  Demande d’intégration [#1747](https://github.com/pgbackrest/pgbackrest/pull/1747); Commit [`a913113`](https://github.com/pgbackrest/pgbackrest/commit/a913113fda5886ffd2ff136cdd52a3f469eca026)
- Ajouter une FAQ sur les types de sauvegarde et la vitesse de restauration. (*Contribution de David Christensen. Révisé par Reid Thompson.*)

  Une nouvelle entrée de FAQ explique que le type de sauvegarde n'affecte que la sauvegarde, et non la vitesse de restauration.

  Demande d’intégration [#1731](https://github.com/pgbackrest/pgbackrest/pull/1731); Commit [`50d409a`](https://github.com/pgbackrest/pgbackrest/commit/50d409a812be577f2c296f3d6096cf97fab049ff)
- Documenter la branche de base requise pour les demandes de fusion. (*Contribution de David Christensen. Révisé par Reid Thompson.*)

  Le guide de contribution précise désormais que les demandes d'intégration doivent partir de la branche `integration`.

  Demande d’intégration [#1733](https://github.com/pgbackrest/pgbackrest/pull/1733); Commit [`cc5b061`](https://github.com/pgbackrest/pgbackrest/commit/cc5b0614894e1b5ef78f1ceba3bc8e4760a40a24)

### Notes de version v2.38 {#v238-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 6 mars 2022*

**NOTE IMPORTANTE** : La taille du dépôt rapportée par la commande `info` est désormais entièrement basée sur ce que pgBackRest a écrit dans le stockage. Dans certains cas, pgBackRest pouvait auparavant détecter si une compression supplémentaire était appliquée par le stockage, mais cette fonctionnalité n’est plus prise en charge.

**Correctifs de bogues :**

- Réessayer les erreurs survenues lors de la suppression par lot de fichiers S3. (*Révisé par Reid Thompson. Signalement par Alex Richman.*)

  Une suppression par lot échouée était réessayée, mais pas les erreurs de fichiers individuels du lot. pgBackRest pouvait donc s'arrêter pendant l'expiration ou la suppression d'une sauvegarde non reprenable. Les fichiers en échec dans un lot sont désormais supprimés individuellement avec les nouvelles tentatives HTTP habituelles.

  Ticket [#1650](https://github.com/pgbackrest/pgbackrest/issues/1650); Demande d’intégration [#1653](https://github.com/pgbackrest/pgbackrest/pull/1653); Commit [`551e5bc`](https://github.com/pgbackrest/pgbackrest/commit/551e5bc6f67c91cf1e11da0cefe24f9650353adc)
- Permettre la correspondance insensible à la casse des valeurs d’en-tête HTTP `connection`. (*Révisé par Reid Thompson. Signalement par Rémi Vidier.*)

  La spécification HTTP autorise les valeurs de l'en-tête `connection` dans n'importe quelle casse, par exemple `Close`.

  Ticket [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Demande d’intégration [#1675](https://github.com/pgbackrest/pgbackrest/pull/1675); Commit [`b33cabe`](https://github.com/pgbackrest/pgbackrest/commit/b33cabe08c33e29eb8aef65dd46b2c1f3cf2d186)

**Fonctionnalités :**

- Ajouter la prise en charge du chiffrement côté serveur AWS S3 utilisant KMS. (*Contribution de Christoph Berg. Révisé par David Steele. Testé par Tharindu Amila.*)

  Définissez `repo-s3-kms-key-id` pour chiffrer les objets avec une clé gérée par AWS KMS.

  Ticket [#1430](https://github.com/pgbackrest/pgbackrest/issues/1430); Demande d’intégration [#1567](https://github.com/pgbackrest/pgbackrest/pull/1567); Commit [`3097acd`](https://github.com/pgbackrest/pgbackrest/commit/3097acd73a21b630aa5352be57a82b031930f96b)
- Ajouter l'option `archive-missing-retry`. (*Révisé par Stefan Fercot.*)

  Par défaut, `archive-get` réessaie un segment WAL déjà signalé absent, ce qui ignore les notifications d'absence laissées dans le spool par une restauration précédente. Avec `archive-missing-retry=n`, PostgreSQL peut détecter la fin de l'archive et passer à la réplication en continu même pendant l'archivage des WAL. Le spool doit alors être vide au début de la récupération.

  Demande d’intégration [#1642](https://github.com/pgbackrest/pgbackrest/pull/1642); Commit [`10038db`](https://github.com/pgbackrest/pgbackrest/commit/10038db9c9f2b4753c3821e0b246fa8626527184)
- Ajouter un filtre de type de sauvegarde à la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Définissez `type` pour n'afficher que les sauvegardes de ce type, par exemple `type=full`.

  Ticket [#600](https://github.com/pgbackrest/pgbackrest/issues/600); Demande d’intégration [#1651](https://github.com/pgbackrest/pgbackrest/pull/1651); Commit [`b26097f`](https://github.com/pgbackrest/pgbackrest/commit/b26097f8d8a7e2af6e9a21576994cbb47110c6f4)

**Améliorations :**

- Réessayer en cas d'échec de validation de page pendant `backup`. (*Révisé par Stephen Frost, David Christensen.*)

  Une page dont la somme de contrôle est invalide est désormais relue. Elle n'est signalée comme une erreur que si elle n'a pas changé. Une page modifiée est en cours d'écriture par PostgreSQL, et le WAL contient une image complète de la page. Les pages nulles sont désormais vérifiées entièrement, plutôt que sur le seul champ `pd_upper`.

  [`b489707`](https://github.com/pgbackrest/pgbackrest/commit/b4897077937ee4571ba719276a44d5db0a75510e) Déplacer les tests command/backup-common dans le module command/backup.

  [`9eec98c`](https://github.com/pgbackrest/pgbackrest/commit/9eec98c61302121134d2067326dbd2cd0f2f0b9c) Réessayer en cas d'échec de validation d'une somme de contrôle de page pendant la sauvegarde. ; Ticket [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Demande d’intégration [#1667](https://github.com/pgbackrest/pgbackrest/pull/1667)

  [`53f1b25`](https://github.com/pgbackrest/pgbackrest/commit/53f1b2520434221c01caf92e052403a28c455c1b) Améliorer la validation des pages nulles. ; Ticket [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Demande d’intégration [#1669](https://github.com/pgbackrest/pgbackrest/pull/1669)
- Gérer les serveurs TLS qui ne ferment pas les connexions de manière gracieuse. (*Révisé par David Christensen, Stephen Frost. Testé par Rémi Vidier.*)

  Certains serveurs ferment le socket plutôt que la connexion TLS. Si une réponse n'a ni longueur de contenu ni encodage par morceaux et que son contenu peut être analysé, le socket fermé est désormais traité comme une fin de fichier. Ces serveurs avaient cessé de fonctionner dans la v2.35.

  Ticket [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Demande d’intégration [#1677](https://github.com/pgbackrest/pgbackrest/pull/1677); Commit [`59a5373`](https://github.com/pgbackrest/pgbackrest/commit/59a5373cf85e4ad0057b592bfe855495384dfcbd)
- Ajouter les LSN de sauvegarde à la sortie de la commande `info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Les LSN de début et de fin d'une sauvegarde sont affichés avec `set` et dans la sortie JSON, pour permettre la récupération à un instant donné fondée sur un LSN.

  Demande d’intégration [#1610](https://github.com/pgbackrest/pgbackrest/pull/1610); Commit [`d866dd5`](https://github.com/pgbackrest/pgbackrest/commit/d866dd5c297dc046581134a108032cf9694cae0e)
- Supprimer automatiquement les barres obliques en fin de chemins `repo-ls`. (*Contribution de David Christensen. Révisé par David Steele.*)

  Une barre oblique finale dans le chemin empêchait `repo-ls` d'afficher le contenu sur certains types de stockage de dépôt.

  Demande d’intégration [#1673](https://github.com/pgbackrest/pgbackrest/pull/1673); Commit [`6320712`](https://github.com/pgbackrest/pgbackrest/commit/632071232344a1160ef932d6e0d65eb3149ed226)
- Ne pas réessayer les erreurs fatales. (*Révisé par Reid Thompson.*)

  Réessayer les erreurs fatales, notamment les manques de mémoire, peut provoquer des blocages. Les erreurs d'assertion et de mémoire sont désormais signalées sans nouvelle tentative.

  [`8573a2d`](https://github.com/pgbackrest/pgbackrest/commit/8573a2df14d0bfd5578333b68147cc12c93c6f96) Améliorer le test d'erreur de protocolClientFree() dans le module de protocole.

  [`8d0cce6`](https://github.com/pgbackrest/pgbackrest/commit/8d0cce66f83abc1ff02a985ec3f0d7e285c09d72) Utiliser une erreur normale dans le test de nouvelle tentative du module de protocole.

  [`8046f06`](https://github.com/pgbackrest/pgbackrest/commit/8046f0630715015d5adcced570c54e9a183c0e73) Ne pas réessayer les erreurs fatales. ; Demande d’intégration [#1658](https://github.com/pgbackrest/pgbackrest/pull/1658)
- Supprimer le support de PostgreSQL `8.3`/`8.4`. (*Révisé par Reid Thompson, Stefan Fercot.*)

  Rien n'indique que ces versions soient encore utilisées, et leur prise en charge coûte du temps de développement et de test. Utilisez une ancienne version de pgBackRest pour les sauvegarder ou migrer depuis celles-ci.

  Demande d’intégration [#1611](https://github.com/pgbackrest/pgbackrest/pull/1611); Commit [`bb4b30d`](https://github.com/pgbackrest/pgbackrest/commit/bb4b30ddd3f80c246c565eb4769efc82b9509648)
- Supprimer la logique qui tentait de déterminer une compression supplémentaire du système de fichiers. (*Révisé par Reid Thompson, Stefan Fercot.*)

  Après la copie d'un fichier, pgBackRest vérifiait sa taille sur disque pour détecter la compression du système de fichiers, par exemple ZFS. Ce mécanisme n'était pas testé, ralentissait le traitement de nombreux petits fichiers et bloquait leur regroupement. La taille du dépôt indiquée par `info` correspond désormais à ce que pgBackRest a écrit.

  Demande d’intégration [#1652](https://github.com/pgbackrest/pgbackrest/pull/1652); Commit [`cb630ff`](https://github.com/pgbackrest/pgbackrest/commit/cb630ffe3b5c819b5e97ac11d5974000bd44d632)

**Correctifs de bogues dans la documentation :**

- Déplacer les options `repo` dans la documentation TLS vers la section `global`. (*Signalement par Anton Kurochkin.*)

  Le guide utilisateur définissait ces options dans la section stanza, ce qui fonctionne dans certains cas mais n'est pas la pratique recommandée.

  Commit [`53de3e3`](https://github.com/pgbackrest/pgbackrest/commit/53de3e3aeb71f8209f56167941df35bbfcb7cdc9)
- Supprimer l'option `backup-standby` inutilisée des commandes de stanza. (*Signalement par Stefan Fercot.*)

  `stanza-create` et `stanza-upgrade` mentionnaient `backup-standby` dans leur référence et leur aide, sans utiliser cette option.

  Commit [`5cbb4a3`](https://github.com/pgbackrest/pgbackrest/commit/5cbb4a3e6b13598b90cae46fad28c31604f9f094)
- Corriger les fautes de frappe dans l'aide et les notes de version. (*Corrigé par Daniel Gustafsson. Révisé par David Steele.*)

  [`cacfdd9`](https://github.com/pgbackrest/pgbackrest/commit/cacfdd94d74307285b1b590ec0977d7db3142d0d) Corriger des fautes dans l'aide et les notes de version. ; Demande d’intégration [#1671](https://github.com/pgbackrest/pgbackrest/pull/1671)

  [`5c332a0`](https://github.com/pgbackrest/pgbackrest/commit/5c332a0b100d5a5180b3d95bd90d4d7b521b42db) Corriger les attributions des notes de version dans cacfdd94 et f798458e.

**Améliorations de la documentation :**

- Ajouter une vérification de disponibilité à la configuration du service systemd. (*Suggéré par Yogesh Sharma.*)

  L'exemple `pgbackrest.service` vérifie désormais que le serveur tourne encore peu après son démarrage. Auparavant, un échec de démarrage ne signalait aucune erreur pendant que systemd réessayait en arrière-plan.

  Commit [`f1bdf3e`](https://github.com/pgbackrest/pgbackrest/commit/f1bdf3e04b07dc9a2eaa1fdbe5278cc18371e868)
- Ajouter une FAQ expliquant le suffixe de l'archive WAL. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Le suffixe d'un fichier WAL dans le dépôt est sa somme de contrôle SHA1, utilisée pour vérifier le fichier. Il ne peut pas être omis.

  Ticket [#1485](https://github.com/pgbackrest/pgbackrest/issues/1485); Ticket [#1663](https://github.com/pgbackrest/pgbackrest/issues/1663); Demande d’intégration [#1664](https://github.com/pgbackrest/pgbackrest/pull/1664); Commit [`98d525d`](https://github.com/pgbackrest/pgbackrest/commit/98d525dba43ba259ff7989746b8e5be3382c189d)
- Notez que les slots de réplication ne sont pas restaurés. (*Contribution de Reid Thompson. Révisé par David Steele, Stefan Fercot. Suggéré par Christophe Courtois.*)

  Ticket [#1585](https://github.com/pgbackrest/pgbackrest/issues/1585); Demande d’intégration [#1601](https://github.com/pgbackrest/pgbackrest/pull/1601); Commit [`a82f017`](https://github.com/pgbackrest/pgbackrest/commit/a82f0179cdd5742e5c5b1e0bdfd23166753fdb38)

### Notes de version v2.37 {#v237-release-notes}

*Serveur TLS*

*Sortie le 3 janvier 2022*

**NOTE IMPORTANTE** : Si la commande `restore` n'est pas en mesure de trouver une sauvegarde correspondant à une cible de temps spécifiée, une erreur sera levée, contrairement à auparavant où un avertissement était simplement journalisé.

**Correctifs de bogues :**

- Corriger le mappage des liens delta de `restore` lorsque le chemin ou le fichier existe déjà. (*Révisé par Reid Thompson. Signalement par Younes Alhroub.*)

  Lorsque `link-map` ou `link-all` transformait un chemin ou fichier existant en lien, une restauration delta conservait le chemin ou fichier existant. Il est désormais remplacé par le lien.

  Ticket [#1588](https://github.com/pgbackrest/pgbackrest/issues/1588); Demande d’intégration [#1589](https://github.com/pgbackrest/pgbackrest/pull/1589); Commit [`a73fe4e`](https://github.com/pgbackrest/pgbackrest/commit/a73fe4eb966f9685f6e4179c397a10c1e7f15f19)
- Corriger la fuite de socket lors des nouvelles tentatives de connexion. (*Révisé par Reid Thompson. Signalement par James Coleman.*)

  Dans les compilations optimisées, le socket d'une tentative de connexion échouée n'était pas fermé, et chaque nouvelle tentative laissait un socket ouvert.

  Ticket [#1593](https://github.com/pgbackrest/pgbackrest/issues/1593); Demande d’intégration [#1594](https://github.com/pgbackrest/pgbackrest/pull/1594); Commit [`615bdff`](https://github.com/pgbackrest/pgbackrest/commit/615bdff4030a31bfedfe7df04676e3948ec9c2c0)

**Fonctionnalités :**

- Ajouter un serveur TLS. (*Révisé par Stephen Frost, Reid Thompson. Testé par Andrew L'Ecuyer.*)

  La commande `server` lance un serveur TLS pouvant remplacer SSH pour accéder aux hôtes de dépôt et PostgreSQL. Définissez `repo-host-type=tls` ou `pg-host-type=tls` sur le client et configurez les certificats et l'autorisation des clients avec les options `tls-server-*`. `SIGHUP` recharge la configuration et `SIGTERM` arrête le serveur.

  [`2d963ce`](https://github.com/pgbackrest/pgbackrest/commit/2d963ce9471808172f879916c3f3accc35f14d56) Renommer la commande server-start en server.

  [`7b3ea88`](https://github.com/pgbackrest/pgbackrest/commit/7b3ea883c7c010aafbeb14d150d073a113b703e4) Ajouter la gestion de SIGTERM et SIGHUP au serveur TLS. ; Demande d’intégration [#1572](https://github.com/pgbackrest/pgbackrest/pull/1572)

  [`f06101d`](https://github.com/pgbackrest/pgbackrest/commit/f06101de77a980c7e4115762f2fc301280aa4127) Ajouter la documentation du serveur TLS. ; Demande d’intégration [#1597](https://github.com/pgbackrest/pgbackrest/pull/1597)

  Développement dans [v2.36](#v236-release-notes) :

  [`ccc255d`](https://github.com/pgbackrest/pgbackrest/commit/ccc255d3e05d8ce2b6ac251d1498f71b04098a86) Ajouter un serveur TLS. ; Demande d’intégration [#1504](https://github.com/pgbackrest/pgbackrest/pull/1504)

  [`13d4559`](https://github.com/pgbackrest/pgbackrest/commit/13d4559708819787ad05be6f37ec0badb0eccae5) Vérifier la valeur de retour de getsockopt().

  Développement dans [v2.35](#v235-release-notes) :

  [`947c7a8`](https://github.com/pgbackrest/pgbackrest/commit/947c7a84cb37d09ab925785ca7670c970e32b8a3) Refactoriser cmdLocal()/cmdRemote() pour accepter un objet ProtocolServer.

  [`0999de0`](https://github.com/pgbackrest/pgbackrest/commit/0999de0279fabf35af80396a9a8d35546ec02d53) Déplacer noop de protocolClientNew() vers l'initialisation local/remote.
- Ajouter l'option `--cmd`. (*Contribution de Reid Thompson. Révisé par Stefan Fercot, David Steele. Suggéré par Virgile CREVON.*)

  Définissez `cmd` comme l'exécutable pgBackRest à utiliser dans les commandes écrites par pgBackRest, par exemple `restore_command` dans `recovery.conf`.

  Ticket [#1537](https://github.com/pgbackrest/pgbackrest/issues/1537); Demande d’intégration [#1540](https://github.com/pgbackrest/pgbackrest/pull/1540); Commit [`2a57647`](https://github.com/pgbackrest/pgbackrest/commit/2a576477b316238473525e56bc8fc8ea5790455f)

**Améliorations :**

- Vérifier l'archive immédiatement après le démarrage de la sauvegarde. (*Révisé par Reid Thompson, David Christensen.*)

  Une sauvegarde ne signalait un échec d'archivage WAL qu'après avoir copié tous les fichiers. L'archive est désormais vérifiée juste après le début de la sauvegarde. Sur un système inactif, un point de restauration est créé pour provoquer un changement de segment WAL.

  Ticket [#152](https://github.com/pgbackrest/pgbackrest/issues/152); Demande d’intégration [#1570](https://github.com/pgbackrest/pgbackrest/pull/1570); Commit [`1f14f45`](https://github.com/pgbackrest/pgbackrest/commit/1f14f45dfb0d1677a695719381cbd5a8a3c6c986)
- Ajouter des vérifications de timeline et de point de contrôle à la sauvegarde. (*Révisé par Stefan Fercot, Reid Thompson.*)

  La sauvegarde vérifie désormais que `pg_control` contient le point de contrôle et la timeline du début de sauvegarde, et qu'un serveur de secours suit le primaire, c'est-à-dire qu'il est sur la même timeline et que son point de contrôle n'est pas postérieur à celui de la sauvegarde.

  Demande d’intégration [#1581](https://github.com/pgbackrest/pgbackrest/pull/1581); Commit [`49145d7`](https://github.com/pgbackrest/pgbackrest/commit/49145d72bac16498cdbf5eeb3cd6128ea0be0667)
- Vérifier que les clusters sont actifs et correctement configurés pendant une sauvegarde. (*Révisé par Stefan Fercot.*)

  Une sauvegarde échoue désormais dès qu'un cluster s'arrête ou qu'un serveur de secours est promu. Auparavant, l'arrêt du primaire n'était détecté qu'en fin de sauvegarde, et la promotion du serveur de secours n'était pas détectée.

  Demande d’intégration [#1584](https://github.com/pgbackrest/pgbackrest/pull/1584); Commit [`bd2ba80`](https://github.com/pgbackrest/pgbackrest/commit/bd2ba802db11c505ec69943fa81b2b379073fbf4)
- Erreur lorsque `restore` est incapable de trouver une sauvegarde correspondant à la cible de temps. (*Révisé par Reid Thompson, Douglas J Hunley. Suggéré par Douglas J Hunley.*)

  Il s'agissait d'un avertissement facile à manquer, et beaucoup de temps pouvait être perdu à restaurer une sauvegarde incapable d'atteindre la cible.

  Ticket [#1582](https://github.com/pgbackrest/pgbackrest/issues/1582); Demande d’intégration [#1586](https://github.com/pgbackrest/pgbackrest/pull/1586); Commit [`be4ac39`](https://github.com/pgbackrest/pgbackrest/commit/be4ac3923cb77873da298a30aca5d847b3c635af)
- Analyser le protocole/port dans les points d'accès S3/Azure. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  `repo-s3-endpoint`, `repo-azure-endpoint` et `repo-storage-host` peuvent désormais inclure un protocole et un port, par exemple `https://host:9000`.

  Ticket [#1560](https://github.com/pgbackrest/pgbackrest/issues/1560); Demande d’intégration [#1591](https://github.com/pgbackrest/pgbackrest/pull/1591); Commit [`6a12458`](https://github.com/pgbackrest/pgbackrest/commit/6a12458440168f13cb05d70f36ea54b1860e390c)
- Ajouter un avertissement lorsque `checkpoint_timeout` dépasse `db-timeout`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Avec `start-fast=n`, une sauvegarde peut dépasser le délai en attendant le point de contrôle si `checkpoint_timeout` est supérieur à `db-timeout`. La sauvegarde émet désormais un avertissement dans ce cas.

  Demande d’intégration [#1564](https://github.com/pgbackrest/pgbackrest/pull/1564); Commit [`6723305`](https://github.com/pgbackrest/pgbackrest/commit/672330593789f07aaad90bbafcd2597cbc602686)
- Ajouter un verbe à la sortie d'erreur HTTP. (*Contribution de Christoph Berg. Révisé par David Steele.*)

  Demande d’intégration [#1566](https://github.com/pgbackrest/pgbackrest/pull/1566); Commit [`c38e2d3`](https://github.com/pgbackrest/pgbackrest/commit/c38e2d31709804eb4b9125a15ad84c8fc813f366)
- Permettre les arguments y/n pour les options de ligne de commande booléennes. (*Contribution de Reid Thompson. Révisé par David Steele.*)

  Demande d’intégration [#1571](https://github.com/pgbackrest/pgbackrest/pull/1571); Commit [`1a0560d`](https://github.com/pgbackrest/pgbackrest/commit/1a0560d363d28737befb8c222647783d4fc2ca29)
- Faire correspondre exactement la taille de la sauvegarde au format de sortie de la commande `info`. (*Contribution de Reid Thompson. Révisé par David Steele. Suggéré par Mahomed Hussein.*)

  La taille de sauvegarde journalisée n'inclut désormais que les fichiers copiés, plus `backup_label` et `tablespace_map`. Auparavant, une sauvegarde incrémentale après une bascule pouvait, par exemple, journaliser la taille de tous les fichiers vérifiés.

  [`6e63576`](https://github.com/pgbackrest/pgbackrest/commit/6e635764a66278d5a8c2b4d30b23063bc3923067) Faire correspondre la taille journalisée de la sauvegarde à celle rapportée par info. ; Ticket [#766](https://github.com/pgbackrest/pgbackrest/issues/766); Demande d’intégration [#1562](https://github.com/pgbackrest/pgbackrest/pull/1562)

  [`afe77e7`](https://github.com/pgbackrest/pgbackrest/commit/afe77e76e0adf948138d797e227a6f4c7d47c2eb) Mettre à jour le contributeur de 6e635764.

  [`1e77fc3`](https://github.com/pgbackrest/pgbackrest/commit/1e77fc3d75490b7a1b6a0b31be9298c995ec672f) Inclure les tailles de backup_label et tablespace_map dans le journal. ; Demande d’intégration [#1568](https://github.com/pgbackrest/pgbackrest/pull/1568)

  [`a3d7a23`](https://github.com/pgbackrest/pgbackrest/commit/a3d7a23a9d90611a3d31947598fbea240b250710) Utiliser infoBackupDataByLabel() pour journaliser la taille de la sauvegarde. ; Demande d’intégration [#1573](https://github.com/pgbackrest/pgbackrest/pull/1573)

  [`dcb4f09`](https://github.com/pgbackrest/pgbackrest/commit/dcb4f09d8315e92c0877b589f3fa9b7f0fa65f93) Annuler les modifications de backupFilePut() introduites dans 1e77fc3d.

**Améliorations de la documentation :**

- Afficher les valeurs par défaut et autorisées de l'option de taille, accompagnées des unités appropriées. (*Révisé par Reid Thompson.*)

  [`cff961e`](https://github.com/pgbackrest/pgbackrest/commit/cff961ede7e41fa8035ffe7451a22eb5ea0e46c1) Centraliser la construction des listes de valeurs lors du rendu de la configuration.

  [`038abaa`](https://github.com/pgbackrest/pgbackrest/commit/038abaa71d816cc87b382bd81d3df62ddec9455a) Afficher les valeurs par défaut et autorisées des options de taille avec des unités appropriées. ; Demande d’intégration [#1557](https://github.com/pgbackrest/pgbackrest/pull/1557)
- Corriger les fautes de frappe et améliorer la documentation de l'option `tablespace-map-all`. (*Révisé par Reid Thompson. Suggéré par Reid Thompson.*)

  Commit [`df89eff`](https://github.com/pgbackrest/pgbackrest/commit/df89eff429e9b8fbc68d9e9895badf9719fd31d2)
- Supprimer l'énoncé obsolète concernant la prise en charge future de plusieurs dépôts. (*Suggéré par David Christensen.*)

  La documentation indiquait qu'un seul dépôt était autorisé, alors que plusieurs dépôts sont pris en charge depuis la v2.33.

  Commit [`dea7524`](https://github.com/pgbackrest/pgbackrest/commit/dea752477ab8e812cdbd717eb2091baf3f5d0906)

### Notes de version v2.36 {#v236-release-notes}

*Corrections de bogues mineurs et améliorations*

*Sortie le 1er novembre 2021*

**Correctifs de bogues :**

- Autoriser « global » comme préfixe de stanza. (*Révisé par Stefan Fercot. Signalement par Younes Alhroub.*)

  Un nom de stanza commençant par `global`, par exemple `global_stanza`, était rejeté parce que l'analyseur de configuration le traitait comme une section globale.

  Ticket [#1524](https://github.com/pgbackrest/pgbackrest/issues/1524); Demande d’intégration [#1525](https://github.com/pgbackrest/pgbackrest/pull/1525); Commit [`498902e`](https://github.com/pgbackrest/pgbackrest/commit/498902e885c9d7a44648ccc01b20454094d5b742)
- Corriger le plantage (segfault) lors d'un fichier de clé GCS invalide. (*Révisé par Stephen Frost. Signalement par Henrik Feldt.*)

  Un fichier de clé GCS sans adresse électronique du client, clé privée ou URI de jeton provoquait une erreur de segmentation. Il produit désormais une erreur.

  Ticket [#1536](https://github.com/pgbackrest/pgbackrest/issues/1536); Commit [`2cea005`](https://github.com/pgbackrest/pgbackrest/commit/2cea005f740d640290a9948595f5933833e30e7d)

**Améliorations :**

- Autoriser l'option `link-map` pour créer de nouveaux liens. (*Révisé par Don Seiler, Stefan Fercot, Chris Bandy. Suggéré par Don Seiler.*)

  `link-map` ne pouvait remapper que les liens présents dans la sauvegarde. Il peut désormais créer un lien pour n'importe quel chemin ou fichier de la sauvegarde.

  [`d89a677`](https://github.com/pgbackrest/pgbackrest/commit/d89a67776cfbb7b3047dbe297cc0c768e5c670e8) Refactoriser les tests de restoreManifestMap() dans command/restore.

  [`cf1a575`](https://github.com/pgbackrest/pgbackrest/commit/cf1a57518fe3230886509f59fcec9c9a81e6513c) Refactoriser restoreManifestMap() pour le piloter par link-map.

  [`68c5f3e`](https://github.com/pgbackrest/pgbackrest/commit/68c5f3eaf18fc9bd10fde15a323890bcdcbf4534) Permettre à link-map de créer de nouveaux liens. ; Ticket [#1409](https://github.com/pgbackrest/pgbackrest/issues/1409); Demande d’intégration [#1520](https://github.com/pgbackrest/pgbackrest/pull/1520)
- Augmenter le nombre maximal d'index autorisé pour les options `pg`/`repo` à 256. (*Révisé par Cynthia Shang.*)

  L'index maximal était 8 pour les options `pg` et 4 pour les options `repo`. Il est désormais 256 pour les deux, par exemple `pg256-path`.

  [`02b06aa`](https://github.com/pgbackrest/pgbackrest/commit/02b06aa4957cf3fe64ceb7a44cc1893bff12fe99) Porter l'index maximal des options pg/repo à 256. ; Demande d’intégration [#1481](https://github.com/pgbackrest/pgbackrest/pull/1481)

  [`71047a9`](https://github.com/pgbackrest/pgbackrest/commit/71047a9d6d1eea71b3fbd430983541a54049cc69) Utiliser strncpy() pour limiter les caractères copiés dans optionName.
- Ajouter l'authentification `WebIdentity` pour AWS S3. (*Révisé par James Callahan, Reid Thompson, Andrew L'Ecuyer. Testé par Benjamin Blattberg.*)

  Définissez `repo-s3-key-type=web-id` pour obtenir automatiquement des identifiants dans un environnement EKS.

  [`cfd8233`](https://github.com/pgbackrest/pgbackrest/commit/cfd823355af2ac99f30c5e1393a121c6dbf622b7) Refactoriser le pilote S3 pour ajouter des méthodes d'authentification.

  [`3879bc6`](https://github.com/pgbackrest/pgbackrest/commit/3879bc69b888daa04d2ca98a2d1219cf22519ddc) Ajouter l'authentification WebIdentity pour AWS S3. ; Ticket [#1203](https://github.com/pgbackrest/pgbackrest/issues/1203); Demande d’intégration [#1527](https://github.com/pgbackrest/pgbackrest/pull/1527)

  [`1152f7a`](https://github.com/pgbackrest/pgbackrest/commit/1152f7a7d64e69eed1d9e74b48a308f6c742c28a) Corriger les paramètres incohérents d'un appel à tlsClientNew().
- Ajouter l'option `repo-azure-uri-style`.

  Définissez `repo-azure-uri-style` sur `host` (par défaut) ou `path` pour choisir le style d'URI Azure. Azurite utilise les URI de type hôte lorsque le point de terminaison ressemble à un nom d'hôte en plusieurs parties.

  Commit [`096829b`](https://github.com/pgbackrest/pgbackrest/commit/096829b3b257444162417662612e80d8cb2ac6ec)
- Signaler les erreurs de validation des fichiers de sauvegarde dans `backup.info`. (*Contribution de Stefan Fercot. Révisé par David Steele.*)

  Les erreurs détectées pendant une sauvegarde, comme les sommes de contrôle de pages invalides, n'étaient affichées que par `info` avec `set`. Un indicateur dans `backup.info` signale désormais dans les sorties texte et JSON qu'une sauvegarde comporte des erreurs. Le détail nécessite toujours `set`.

  Ticket [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Demande d’intégration [#1508](https://github.com/pgbackrest/pgbackrest/pull/1508); Commit [`34f7873`](https://github.com/pgbackrest/pgbackrest/commit/34f78734325743b4e34cb39224852e6debf49750)
- Ajouter l'heure de démarrage de la récupération au journal de restauration en ligne d'une sauvegarde. (*Révisé par Tom Swartz, Stefan Fercot. Suggéré par Tom Swartz.*)

  La restauration journalise désormais l'instant de départ de la récupération, ce qui permet d'estimer la quantité de WAL à rejouer.

  Ticket [#1507](https://github.com/pgbackrest/pgbackrest/issues/1507); Demande d’intégration [#1518](https://github.com/pgbackrest/pgbackrest/pull/1518); Commit [`9e79f0e`](https://github.com/pgbackrest/pgbackrest/commit/9e79f0e64b661e944ce2b3897c366feea1544ac2)
- Signaler l'erreur d'origine et les tentatives de réessai en cas d'échec d'une tâche locale. (*Révisé par Stefan Fercot.*)

  Lorsqu'une tâche locale échoue après ses nouvelles tentatives, l'erreur rapporte désormais l'erreur initiale avec sa trace de pile, puis les erreurs des nouvelles tentatives. Auparavant, seule la dernière erreur était rapportée, souvent une conséquence en cascade comme une désynchronisation du protocole.

  [`136d309`](https://github.com/pgbackrest/pgbackrest/commit/136d309dd4bc1ada9f3d775f036b62292fda390b) Permettre de fournir une trace de pile à errorInternalThrow().

  [`ae40ed6`](https://github.com/pgbackrest/pgbackrest/commit/ae40ed6ec9cf77e577518b128518a5763767f589) Ajouter le paramètre jobRetry à HRN_CFG_LOAD().

  [`6af827c`](https://github.com/pgbackrest/pgbackrest/commit/6af827cbb1e78cd4c5d649ed4cb24c49a7204b8f) Rapporter l'erreur initiale et les nouvelles tentatives lors de l'échec d'une tâche locale. ; Demande d’intégration [#1521](https://github.com/pgbackrest/pgbackrest/pull/1521)
- Renommer l'erreur de somme de contrôle de page en liste d'erreurs dans la sortie texte d'information. (*Révisé par Stefan Fercot.*)

  Dans la sortie texte de `info`, le libellé est désormais « error list » au lieu de « page checksum error ». Un fichier peut avoir une erreur d'alignement plutôt qu'une erreur de somme de contrôle de page.

  Demande d’intégration [#1519](https://github.com/pgbackrest/pgbackrest/pull/1519); Commit [`9346895`](https://github.com/pgbackrest/pgbackrest/commit/9346895f5b61627b50d431f09447e08d8a50caa8)
- Ajouter des indications à l'avertissement de délai d'attente de relecture en mode secondaire. (*Révisé par Cynthia Shang, Stefan Fercot. Suggéré par Leigh Downs.*)

  Le dépassement du délai d'attente du rejeu par le serveur de secours indique désormais de vérifier que la réplication fonctionne et de désactiver `backup-standby` pour sauvegarder depuis le primaire.

  Ticket [#1434](https://github.com/pgbackrest/pgbackrest/issues/1434); Commit [`b7ef12a`](https://github.com/pgbackrest/pgbackrest/commit/b7ef12a76f219881d0b24c715592af96fe5c9b8f)

**Corrections de bogues dans la documentation :**

- Corriger le nom d'hôte incorrect dans le guide utilisateur. (*Corrigé par Reid Thompson. Révisé par David Steele.*)

  La configuration de réplication utilisait l'adresse IP de pg-primary dans `pg_hba.conf`, au lieu de celle de pg-standby.

  Demande d’intégration [#1544](https://github.com/pgbackrest/pgbackrest/pull/1544); Commit [`1cb8ae1`](https://github.com/pgbackrest/pgbackrest/commit/1cb8ae15de5b4276682bdd9825ca97012cd43855)

**Améliorations de la documentation :**

- Améliorer la documentation des options.

  L'aide de `buffer-size` décrit désormais toutes les opérations qui l'utilisent, les descriptions de `cmd-ssh`, `repo-host-cmd` et `pg-host-cmd` sont cohérentes, et `archive-header-check` a été déplacé dans la section d'archivage de la référence de configuration.

  [`3763624`](https://github.com/pgbackrest/pgbackrest/commit/376362475e3b3b13b70313d9002d4ff8b25b4b40) Déplacer archive-header-check dans la section d'archivage de la référence.

  [`e1f6c06`](https://github.com/pgbackrest/pgbackrest/commit/e1f6c066b3da11fd21b1155c90370c3fa2da06b7) Améliorer la documentation de buffer-size.

  [`fa564ee`](https://github.com/pgbackrest/pgbackrest/commit/fa564ee1969229b5cf60d2479d8ace85325f4db3) Améliorer la documentation de cmd-ssh, repo-host-cmd et pg-host-cmd.

### Notes de version v2.35 {#v235-release-notes}

*Protocole binaire*

*Sortie le 23 août 2021*

**NOTE IMPORTANTE** : Le niveau de journalisation des fichiers copiés dans les commandes `backup`/`restore` a été modifié en `detail`. Cela rend le niveau de journalisation `info` moins bruyant, mais si ces messages sont nécessaires, définissez le niveau de journalisation des commandes `backup`/`restore` sur `detail`.

**Correctifs de bogues :**

- Détecter les erreurs lors de la finalisation du téléversement multipartite S3. (*Révisé par Cynthia Shang. Testé par Marco Montagna. Signalement par Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)

  La finalisation d'un envoi multipartie peut échouer même si S3 renvoie un succès HTTP. Une réponse sans `ETag` est désormais traitée comme un échec, et la tâche est réessayée.

  [`8e1807c`](https://github.com/pgbackrest/pgbackrest/commit/8e1807cdbe08a6e059ff79220247cf4b3c058979) Détecter les erreurs de finalisation d'un envoi multipartie S3. ; Ticket [#1116](https://github.com/pgbackrest/pgbackrest/issues/1116); Ticket [#1290](https://github.com/pgbackrest/pgbackrest/issues/1290); Ticket [#1433](https://github.com/pgbackrest/pgbackrest/issues/1433); Demande d’intégration [#1438](https://github.com/pgbackrest/pgbackrest/pull/1438)

  [`25508a4`](https://github.com/pgbackrest/pgbackrest/commit/25508a48e0d3b0a3eabc6d1fe858b9c3dc12dc86) Ajouter les contributeurs oubliés dans 8e187cdb.
- Corriger la détection des liens symboliques circulaires. (*Révisé par Stefan Fercot. Signalement par Rohit Raveendran.*)

  Les liens étaient suivis avant d'être vérifiés. Un lien circulaire entraînait donc une récursion infinie lors de la construction du manifeste, puis un plantage.

  Ticket [#1447](https://github.com/pgbackrest/pgbackrest/issues/1447); Demande d’intégration [#1452](https://github.com/pgbackrest/pgbackrest/pull/1452); Commit [`43b8746`](https://github.com/pgbackrest/pgbackrest/commit/43b874628c86ec4fe297dbd5cab5bd3f62b8639b)
- Transmettre uniquement les options `repo` sélectionnées au serveur distant. (*Révisé par David Christensen, Cynthia Shang. Signalement par Greg Sabino Mullane, David Christensen.*)

  Les options d'autres dépôts pouvaient provoquer des conflits sur l'hôte distant, qui utilise exactement un dépôt.

  Demande d’intégration [#1480](https://github.com/pgbackrest/pgbackrest/pull/1480); Commit [`935de1e`](https://github.com/pgbackrest/pgbackrest/commit/935de1e7a06d60415c16cad137875b49346337c6)

**Améliorations :**

- Protocole binaire. (*Révisé par Cynthia Shang.*)

  Les processus locaux et distants communiquent désormais au format binaire pack plutôt qu'en JSON. Les packs sont plus compacts, plus rapides à produire et à analyser, et strictement typés. Chaque message est écrit en un seul endroit, ce qui réduit le risque qu'une erreur laisse le protocole dans un état incorrect. La taille des messages n'est pas limitée.

  [`6a1c033`](https://github.com/pgbackrest/pgbackrest/commit/6a1c0337ddee9900dda58b7d2fa74d82c0586ed2) Protocole binaire. ; Demande d’intégration [#1424](https://github.com/pgbackrest/pgbackrest/pull/1424)

  [`2d5cbfc`](https://github.com/pgbackrest/pgbackrest/commit/2d5cbfc73142fa99df609aa23b64db5342e73c88) Corriger les fuites mémoire introduites par le protocole binaire dans 6a1c0337.

  [`f716cb6`](https://github.com/pgbackrest/pgbackrest/commit/f716cb6f4f9765baa03f71b5563786d79d9f04a2) Corriger l'accès après libération introduit par le protocole binaire dans 6a1c0337.

  [`4fb6384`](https://github.com/pgbackrest/pgbackrest/commit/4fb6384f10f6cd26c422ab9b24feb5ae0ebeeee9) Corriger d'autres fuites mémoire introduites par le protocole binaire dans 6a1c0337.
- Créer automatiquement le répertoire de données sur `restore`. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Chris Bandy.*)

  Une vérification migrée depuis Perl empêchait la restauration de créer le répertoire de données.

  Ticket [#1445](https://github.com/pgbackrest/pgbackrest/issues/1445); Demande d’intégration [#1454](https://github.com/pgbackrest/pgbackrest/pull/1454); Commit [`056a307`](https://github.com/pgbackrest/pgbackrest/commit/056a3070e0dba299389c7b5049878d40dd91ec9a)
- Autoriser `restore` `--type=lsn`. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang. Suggéré par James Coleman.*)

  Définissez `type=lsn` et un LSN dans `target` pour récupérer jusqu'à ce LSN avec PostgreSQL >= 10.

  Ticket [#1339](https://github.com/pgbackrest/pgbackrest/issues/1339); Demande d’intégration [#1462](https://github.com/pgbackrest/pgbackrest/pull/1462); Commit [`563d117`](https://github.com/pgbackrest/pgbackrest/commit/563d117967ab9770f9f646c6186d0bc37121611f)
- Modifier le niveau de journalisation des fichiers copiés `backup`/`restore` en détail. (*Révisé par Stefan Fercot. Suggéré par Jens Wilke.*)

  Cela rend le niveau de journalisation `info` moins verbeux. Choisissez `detail` pour voir chaque fichier copié.

  Ticket [#1277](https://github.com/pgbackrest/pgbackrest/issues/1277); Demande d’intégration [#1455](https://github.com/pgbackrest/pgbackrest/pull/1455); Commit [`849ab34`](https://github.com/pgbackrest/pgbackrest/commit/849ab343aa10d66fbbd27cad407eff981c186d06)
- Boucler en attendant que le LSN de point de contrôle atteigne le LSN de relecture. (*Contribution de Stefan Fercot. Révisé par David Steele. Suggéré par Fatih Mencutekin.*)

  Sur un serveur de secours, le LSN du point de contrôle peut être légèrement en retard sur le LSN rejoué jusqu'à la mise à jour de `pg_control`. La sauvegarde continue désormais de vérifier au lieu d'échouer.

  Ticket [#1450](https://github.com/pgbackrest/pgbackrest/issues/1450); Demande d’intégration [#1460](https://github.com/pgbackrest/pgbackrest/pull/1460); Commit [`8fac1ac`](https://github.com/pgbackrest/pgbackrest/commit/8fac1ac50d28557d162fbb251fbbdcc3c9fb950c)
- Journaliser le total des fichiers `backup` et le total de la taille par fichier `restore`. (*Révisé par Cynthia Shang.*)

  La taille de sauvegarde est désormais journalisée en fin de sauvegarde et comprend les fichiers ajoutés au manifeste après la copie principale, comme `backup_label` et les WAL. La restauration journalise désormais sa taille et le nombre total de fichiers.

  Demande d’intégration [#1489](https://github.com/pgbackrest/pgbackrest/pull/1489); Commit [`a0bdfa4`](https://github.com/pgbackrest/pgbackrest/commit/a0bdfa436c9e1c2723be905ebe5cef7809a26244)

**Correctifs de bogues dans la documentation :**

- Correction de noms d'hôtes incorrects dans le guide utilisateur. (*Révisé par Stefan Fercot. Signalement par Greg Sabino Mullane.*)

  Certains exemples affichaient `pg1` au lieu du nom d'hôte, et le bloc d'installation installait les paquets sur l'hôte de compilation, quel que soit l'hôte spécifié.

  Demande d’intégration [#1479](https://github.com/pgbackrest/pgbackrest/pull/1479); Commit [`155ef85`](https://github.com/pgbackrest/pgbackrest/commit/155ef85013088a1150a4c15b04af36420d06e9c3)

**Améliorations de la documentation :**

- Mettre à jour la documentation relative à la contribution et ajouter un modèle de demande de fusion. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  Le guide de contribution contient désormais une table des matières et des sections expliquant la sortie des tests et l'envoi d'une demande d'intégration. GitHub affiche désormais un modèle pour les nouvelles demandes d'intégration.

  [`e3d05e2`](https://github.com/pgbackrest/pgbackrest/commit/e3d05e2b4aa80149219b6d49a3136b34fa268127) Mettre à jour le guide de contribution et ajouter un modèle de demande d'intégration. ; Demande d’intégration [#1469](https://github.com/pgbackrest/pgbackrest/pull/1469)

  [`71b654f`](https://github.com/pgbackrest/pgbackrest/commit/71b654fc29497319862fe01c3917bbc353cc6dd9) Corriger les liens et mettre à jour l'exemple de processus enfant. ; Demande d’intégration [#1487](https://github.com/pgbackrest/pgbackrest/pull/1487)
- Réorganiser la documentation relative aux sauvegardes dans le guide utilisateur. (*Révisé par Cynthia Shang.*)

  Les sections « Option de démarrage rapide » et « Délai d'archivage » ont été déplacées vers « Démarrage rapide - Effectuer une sauvegarde ». La section « Option d'arrêt automatique », qui ne concerne que PostgreSQL <= 9.6, a été supprimée.

  Demande d’intégration [#1488](https://github.com/pgbackrest/pgbackrest/pull/1488); Commit [`6ab18dc`](https://github.com/pgbackrest/pgbackrest/commit/6ab18dc0fa42885aea8eb9405ab0a943c2d49a71)
- Préciser le comportement de `restore` `--type` dans la référence de commande. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  La référence précise désormais que `set` doit être spécifié lorsque la cible précède la dernière sauvegarde et que `type` n'est pas `time`.

  Commit [`a6691c6`](https://github.com/pgbackrest/pgbackrest/commit/a6691c6f615f90195aeb6c1c6657a6afd79a10d3)
- Corriger les fautes de frappe dans la documentation et les commentaires. (*Contribution de Eric Radman. Révisé par David Steele.*)

  Demande d’intégration [#1446](https://github.com/pgbackrest/pgbackrest/pull/1446); Commit [`23bdc3d`](https://github.com/pgbackrest/pgbackrest/commit/23bdc3deb62a622713064df3b0777110ebba8723)

**Améliorations de la suite de tests :**

- Ajouter une vérification du chemin de test à l'intérieur du chemin de répertoire. (*Révisé par Greg Sabino Mullane. Suggéré par Greg Sabino Mullane.*)

  Un chemin de test situé dans le chemin du dépôt provoquait des échecs étranges, car le dépôt est copié dans le chemin de test. `test.pl` signale désormais une erreur dans ce cas.

  Ticket [#1472](https://github.com/pgbackrest/pgbackrest/issues/1472); Demande d’intégration [#1474](https://github.com/pgbackrest/pgbackrest/pull/1474); Commit [`e32f9e1`](https://github.com/pgbackrest/pgbackrest/commit/e32f9e146b11389e3d16feba9665360b73737d66)
- Ajouter une analyse statique du code avec CodeQL. (*Révisé par Cynthia Shang.*)

  CodeQL s'exécute désormais dans la CI. Les problèmes détectés ont été corrigés ; par exemple, `gmtime()`/`localtime()` ont été remplacés par `gmtime_r()`/`localtime_r()`.

  Demande d’intégration [#1457](https://github.com/pgbackrest/pgbackrest/pull/1457); Commit [`3c8819e`](https://github.com/pgbackrest/pgbackrest/commit/3c8819e10f9eff89195566e7e02f349373f5c4c7)
- Mettre à jour les tests pour utiliser des modèles standards. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  [`3f9fbc3`](https://github.com/pgbackrest/pgbackrest/commit/3f9fbc3c24eab48e7ae2871484ea01273049e601) Adapter les tests command/expire aux modèles standard. ; Demande d’intégration [#1420](https://github.com/pgbackrest/pgbackrest/pull/1420)

  [`03021c6`](https://github.com/pgbackrest/pgbackrest/commit/03021c6a17f1374e84ef42614fa1dd2a6be4b64d) Adapter les tests command/stanza aux modèles standard. ; Demande d’intégration [#1426](https://github.com/pgbackrest/pgbackrest/pull/1426)

  [`8dd882b`](https://github.com/pgbackrest/pgbackrest/commit/8dd882badee76b038dc8b494a1112eb3e18ef678) Adapter les tests info/infoArchive aux modèles standard. ; Demande d’intégration [#1436](https://github.com/pgbackrest/pgbackrest/pull/1436)

  [`ff95edd`](https://github.com/pgbackrest/pgbackrest/commit/ff95eddc369597c76a9ea70ffbada493ed4d1951) Adapter les tests command/verify aux modèles standard. ; Demande d’intégration [#1435](https://github.com/pgbackrest/pgbackrest/pull/1435)

  [`17c9ed0`](https://github.com/pgbackrest/pgbackrest/commit/17c9ed0ef0380fb14fba9a5299b6618ca8c92c2e) Adapter les tests command/info aux modèles standard. ; Demande d’intégration [#1432](https://github.com/pgbackrest/pgbackrest/pull/1432)

  [`bffb43e`](https://github.com/pgbackrest/pgbackrest/commit/bffb43ea3fe00f445a2fc3c44a07f105cee65b4b) Adapter les tests command/check aux modèles standard. ; Demande d’intégration [#1431](https://github.com/pgbackrest/pgbackrest/pull/1431)

  [`fb2d111`](https://github.com/pgbackrest/pgbackrest/commit/fb2d111dcd75021313a64a348959482339bf7f2a) Adapter les tests info/infoBackup aux modèles standard. ; Demande d’intégration [#1437](https://github.com/pgbackrest/pgbackrest/pull/1437)

  [`065a8c8`](https://github.com/pgbackrest/pgbackrest/commit/065a8c8454d2acdd72c0c71a24d6b8bc09669e18) Remplacer les définitions par des constantes de chaîne dans les tests unitaires. ; Demande d’intégration [#1440](https://github.com/pgbackrest/pgbackrest/pull/1440)

  [`c620811`](https://github.com/pgbackrest/pgbackrest/commit/c6208113bfce9d637ca3fd0b35ab28a819c1a83e) Ajouter le paramètre timeModified à la macro HRN_STORAGE_PUT().

  [`6a90d46`](https://github.com/pgbackrest/pgbackrest/commit/6a90d469094ee2697ae4c932349756a54136799d) Adapter les tests info/manifest aux modèles standard. ; Demande d’intégration [#1444](https://github.com/pgbackrest/pgbackrest/pull/1444)

  [`62e8d97`](https://github.com/pgbackrest/pgbackrest/commit/62e8d97af03e7628d5710b17aad1cc31f83d7e69) Adapter les tests command/archive aux modèles standard. ; Demande d’intégration [#1449](https://github.com/pgbackrest/pgbackrest/pull/1449)

  [`8bb0b28`](https://github.com/pgbackrest/pgbackrest/commit/8bb0b28455d59ef884eab7ab25a91f988adbab81) Adapter les tests command/control et command/command aux modèles standard. ; Demande d’intégration [#1456](https://github.com/pgbackrest/pgbackrest/pull/1456)

  [`f2ec4e0`](https://github.com/pgbackrest/pgbackrest/commit/f2ec4e00a4c4c388a8f1b094381fd566a3dc9aa7) Ajouter les paramètres de chiffrement à la macro TEST_STORAGE_GET().

  [`4ad0bbd`](https://github.com/pgbackrest/pgbackrest/commit/4ad0bbda53b34688146f14d130cf0e53c8dd650f) Adapter les tests command/backup aux modèles standard. ; Demande d’intégration [#1463](https://github.com/pgbackrest/pgbackrest/pull/1463)

  [`117ffe8`](https://github.com/pgbackrest/pgbackrest/commit/117ffe88965fd60ce3dcb328e9d28503870af05a) Adapter les tests command/help aux modèles standard. ; Demande d’intégration [#1464](https://github.com/pgbackrest/pgbackrest/pull/1464)

  [`ebe5848`](https://github.com/pgbackrest/pgbackrest/commit/ebe5848494d4e37a9c86f1fafb5b3453c1f425a6) Adapter les tests command/local et command/remote aux modèles standard. ; Demande d’intégration [#1466](https://github.com/pgbackrest/pgbackrest/pull/1466)

  [`a6cdf5b`](https://github.com/pgbackrest/pgbackrest/commit/a6cdf5b22f0eed53f33bbd84478af0542c81af7d) Adapter les tests command/repo aux modèles standard. ; Demande d’intégration [#1467](https://github.com/pgbackrest/pgbackrest/pull/1467)

  [`4992508`](https://github.com/pgbackrest/pgbackrest/commit/49925087644c76df005828eb27c24f503a09b20b) Adapter les tests command/restore aux modèles standard. ; Demande d’intégration [#1468](https://github.com/pgbackrest/pgbackrest/pull/1468)

  [`4c9ddf5`](https://github.com/pgbackrest/pgbackrest/commit/4c9ddf5ef25d0f441e20e918f57c1ec79218cfdb) Adapter les tests storage aux modèles standard. ; Demande d’intégration [#1470](https://github.com/pgbackrest/pgbackrest/pull/1470)

  [`eeaab6a`](https://github.com/pgbackrest/pgbackrest/commit/eeaab6a3d192fc788c0f74aadbf4b3de5da52531) Adapter les tests config (sauf parse) aux modèles standard. ; Demande d’intégration [#1473](https://github.com/pgbackrest/pgbackrest/pull/1473)

  [`f653b59`](https://github.com/pgbackrest/pgbackrest/commit/f653b59664e757a0e3da63cc8462deafe2d9e0ef) Adapter les tests db/db aux modèles standard. ; Demande d’intégration [#1486](https://github.com/pgbackrest/pgbackrest/pull/1486)

  [`e17865a`](https://github.com/pgbackrest/pgbackrest/commit/e17865a03a5451b82a101557d400ff223d104383) Adapter les tests protocol/protocol aux modèles standard. ; Demande d’intégration [#1491](https://github.com/pgbackrest/pgbackrest/pull/1491)

  [`eca2fc6`](https://github.com/pgbackrest/pgbackrest/commit/eca2fc69589cd44f7c1a43206553984adde5cfb1) Adapter les tests config/parse aux modèles standard. ; Demande d’intégration [#1492](https://github.com/pgbackrest/pgbackrest/pull/1492)

### Notes de version v2.34 {#v234-release-notes}

*Prise en charge de PostgreSQL 14*

*Sortie le 7 juin 2021*

**Correctifs de bogues :**

- Corriger les problèmes liés aux fichiers de file d'attente résiduels d'une précédente `restore`. (*Révisé par Cynthia Shang, Stefan Fercot. Testé par Floris van Nee. Signalement par Floris van Nee.*)

  Une notification laissée dans le spool par une restauration précédente pouvait faire signaler un segment WAL absent par `archive-get`. Lorsqu'elle est trouvée au premier contrôle, elle est désormais supprimée et le processus asynchrone est relancé. Si ce processus ne répond pas, une erreur est signalée au lieu de déclarer le segment WAL absent.

  Ticket [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Demande d’intégration [#1371](https://github.com/pgbackrest/pgbackrest/pull/1371); Commit [`f45e76f`](https://github.com/pgbackrest/pgbackrest/commit/f45e76fa2e8ce0f62317a74fdd51083d52659cd5)
- Corriger le problème survenant lors de la vérification des liens pour un grand nombre d'espaces de tables. (*Révisé par Cynthia Shang. Testé par Avinash Vallarapu. Signalement par Avinash Vallarapu.*)

  La vérification des liens consommait beaucoup de mémoire avec de nombreux tablespaces et pouvait planter. La nouvelle vérification est nettement plus rapide, utilise beaucoup moins de mémoire et détecte aussi les liens de fichiers en double.

  Ticket [#1354](https://github.com/pgbackrest/pgbackrest/issues/1354); Demande d’intégration [#1356](https://github.com/pgbackrest/pgbackrest/pull/1356); Commit [`eba013b`](https://github.com/pgbackrest/pgbackrest/commit/eba013b49b850e53d59795ac6358fcb3381048a3)
- Libérer les distants inutiles afin qu'ils n'expirent pas durant `restore`. (*Révisé par Cynthia Shang. Signalement par Francisco Miguel Biete Banon.*)

  Les connexions distantes restaient ouvertes pendant toute la restauration et pouvaient expirer, provoquant un avertissement sans conséquence mais perturbant à la fin d'une longue restauration. Elles sont désormais fermées après le chargement du manifeste.

  Ticket [#1368](https://github.com/pgbackrest/pgbackrest/issues/1368); Demande d’intégration [#1374](https://github.com/pgbackrest/pgbackrest/pull/1374); Commit [`06fa185`](https://github.com/pgbackrest/pgbackrest/commit/06fa18582a405417c8ab4ba667cb01a13a5c3103)
- Corriger `help` lorsqu'une option valide est invalide pour la commande spécifiée. (*Révisé par Stefan Fercot. Signalement par Cynthia Shang.*)

  `help` provoquait une erreur de segmentation lorsqu'on lui demandait l'aide d'une option non valide pour la commande.

  Demande d’intégration [#1375](https://github.com/pgbackrest/pgbackrest/pull/1375); Commit [`45f8355`](https://github.com/pgbackrest/pgbackrest/commit/45f83558ea862c6f496a27b886e1160e6303bbe8)

**Fonctionnalités :**

- Ajouter la prise en charge de PostgreSQL 14. (*Révisé par Cynthia Shang.*)

  PostgreSQL 14 ne nécessite aucun changement de code par rapport à PostgreSQL 13. La version du catalogue peut désormais changer durant les phases bêta et rc de PostgreSQL sans nécessiter une nouvelle version de pgBackRest.

  Demande d’intégration [#1413](https://github.com/pgbackrest/pgbackrest/pull/1413); Commit [`2452c4d`](https://github.com/pgbackrest/pgbackrest/commit/2452c4d5a4c230b8e3c33d3bddf69e56dfbec284)
- Ajouter l'authentification automatique GCS pour les instances GCE. (*Révisé par Jan Wieck. Testé par Daniel Farina.*)

  Définissez `repo-gcs-key-type=auto` pour obtenir le jeton d'authentification depuis les métadonnées d'une instance GCE.

  [`7b71604`](https://github.com/pgbackrest/pgbackrest/commit/7b71604defa02d5ed9b7aa3407961cb59a52cc45) Utiliser la variable existante pour le port du serveur de test GCS.

  [`26fefa6`](https://github.com/pgbackrest/pgbackrest/commit/26fefa6aeeae90bbb572ea57b605fb8fe526f1a0) Extraire l'analyse des réponses de jeton GCS dans une fonction séparée.

  [`9af0331`](https://github.com/pgbackrest/pgbackrest/commit/9af033194abc4b1cd3f06c3a97fff71c966c3827) Ajouter l'authentification GCS automatique pour les instances GCE. ; Demande d’intégration [#1395](https://github.com/pgbackrest/pgbackrest/pull/1395)
- Ajouter l'option `repo-retention-history` pour expirer l'historique des sauvegardes. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang, David Steele.*)

  Définissez le nombre de jours d'historique de sauvegarde à conserver. Par défaut, tout l'historique est conservé ; l'historique des sauvegardes encore présentes dans le dépôt n'expire jamais. Lorsqu'un manifeste de sauvegarde complète expire, ceux de ses sauvegardes différentielles et incrémentales expirent aussi.

  Demande d’intégration [#1389](https://github.com/pgbackrest/pgbackrest/pull/1389); Commit [`5b332b2`](https://github.com/pgbackrest/pgbackrest/commit/5b332b22b508d896abb64fa6abe26c78c83a29bc)
- Ajouter l'option `db-exclude`. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang.*)

  La restauration exclut les bases de données indiquées en les écrivant sous forme de fichiers creux remplis de zéros. PostgreSQL peut toujours effectuer la récupération, puis ces bases peuvent être supprimées. Avec `db-include`, `db-exclude` ne s'applique qu'aux bases système `template0`, `template1` et `postgres`.

  Ticket [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Demande d’intégration [#1337](https://github.com/pgbackrest/pgbackrest/pull/1337); Commit [`292f836`](https://github.com/pgbackrest/pgbackrest/commit/292f836f1243e51d102bb4be202e7b21a7a386b1)

**Améliorations :**

- Modifier le niveau de journalisation de l'expiration de l'archive de détail à information. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  Demande d’intégration [#1416](https://github.com/pgbackrest/pgbackrest/pull/1416); Commit [`aceb956`](https://github.com/pgbackrest/pgbackrest/commit/aceb956815a87f0c19ea171de25d2c3842a6d806)
- Supprimer le chemin de stockage temporaire de l'archive de la stanza sur `restore`. (*Révisé par Cynthia Shang, Stefan Fercot.*)

  Les fichiers du spool pouvaient perturber le nouveau cluster. Par exemple, d'anciens accusés de réception `archive-push` pouvaient lui faire omettre l'archivage de WAL.

  Ticket [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Demande d’intégration [#1386](https://github.com/pgbackrest/pgbackrest/pull/1386); Commit [`320c6e1`](https://github.com/pgbackrest/pgbackrest/commit/320c6e1aad2cc9a8dabecb2bc91a9b34464de6ec)
- Ne pas écrire les fichiers de manière atomique ni synchroniser les chemins pendant la copie `backup`. (*Révisé par Stephen Frost, Stefan Fercot, Cynthia Shang.*)

  Les écritures atomiques sont inutiles, car les sommes de contrôle sont validées lors de la reprise d'une sauvegarde échouée, et tous les chemins sont synchronisés en fin de sauvegarde.

  Demande d’intégration [#1373](https://github.com/pgbackrest/pgbackrest/pull/1373); Commit [`aa72c19`](https://github.com/pgbackrest/pgbackrest/commit/aa72c19a831fb0dd15a50a003fbaad427f335353)

**Améliorations de la documentation :**

- Mettre à jour la documentation relative aux contributions. (*Contribution de Cynthia Shang. Révisé par David Steele, Stefan Fercot.*)

  Le guide de contribution contient davantage d'exemples pour écrire du code, ajouter des options de configuration et tester.

  Demande d’intégration [#1400](https://github.com/pgbackrest/pgbackrest/pull/1400); Commit [`68faf14`](https://github.com/pgbackrest/pgbackrest/commit/68faf1482a42ea14f5b00a91e19bd5aedec275b8)
- Consolider le guide utilisateur RHEL/CentOS en un seul document. (*Révisé par Cynthia Shang.*)

  Le second guide servait surtout à documenter `stop-auto` pour PostgreSQL <= 9.5, désormais en fin de vie. L'option reste documentée dans la référence.

  Demande d’intégration [#1405](https://github.com/pgbackrest/pgbackrest/pull/1405); Commit [`ccac75e`](https://github.com/pgbackrest/pgbackrest/commit/ccac75e7de8754b39bb691ff8830a2839ea7a285)
- Préciser que `repo-s3-role` n'est pas un `ARN`. (*Contribution de Isaac Yuen. Révisé par David Steele.*)

  Demande d’intégration [#1365](https://github.com/pgbackrest/pgbackrest/pull/1365); Commit [`5bf1606`](https://github.com/pgbackrest/pgbackrest/commit/5bf160643b53699a28a8f0920c36d6ded767d249)

### Notes de version v2.33 {#v233-release-notes}

*Prise en charge des dépôts multiples et de GCS*

*Sortie le 5 avril 2021*

**Correctifs de bogues :**

- Corriger les avertissements d'option bloquant la synchronisation asynchrone `archive-get`/`archive-push`. (*Révisé par Cynthia Shang. Signalement par Lev Kokotov.*)

  Un avertissement d'option du processus asynchrone était écrit sur une sortie stdout fermée, ce qui faisait abandonner le processus. Ce cas est devenu plus fréquent depuis que le rôle asynchrone peut avoir des options valides différentes du rôle par défaut. Les avertissements d'options ne sont désormais journalisés que pour le rôle par défaut.

  Ticket [#1299](https://github.com/pgbackrest/pgbackrest/issues/1299); Demande d’intégration [#1301](https://github.com/pgbackrest/pgbackrest/pull/1301); Commit [`3837e61`](https://github.com/pgbackrest/pgbackrest/commit/3837e61a7504b1e211e4b3a70cbe97343c1cf2e6)
- Corriger la fuite mémoire lors de la sauvegarde pendant la copie de l'archive. (*Révisé par Cynthia Shang. Signalement par Christian ROUX, Efremov Egor.*)

  La copie des WAL dans la sauvegarde avec `archive-copy` provoquait une fuite de mémoire, surtout lorsque les WAL devaient être recompressés.

  Ticket [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Commit [`778adbf`](https://github.com/pgbackrest/pgbackrest/commit/778adbf19f71ceb90071f01197bf189d59b14df0)
- Corriger le dépassement de pile lors de la génération de la phrase de passe du chiffrement. (*Révisé par Cynthia Shang. Signalement par bsiara.*)

  Le tampon de la phrase secrète générée n'avait pas de place pour le zéro terminal. Ce défaut a été détecté sur arm64 avec musl libc.

  Ticket [#1294](https://github.com/pgbackrest/pgbackrest/issues/1294); Demande d’intégration [#1295](https://github.com/pgbackrest/pgbackrest/pull/1295); Commit [`d29855b`](https://github.com/pgbackrest/pgbackrest/commit/d29855bd0bf8b957fa8c06445d22e425c443a704)
- Corriger `repo-ls` `/` sur les dépôts S3. (*Révisé par Cynthia Shang. Signalement par Lesovsky Alexey.*)

  S3 signale `/` comme un fichier sans les en-têtes attendus, ce qui provoquait une erreur. `/` est désormais signalé comme inexistant sur les stockages qui ne prennent pas en charge les chemins.

  Ticket [#1317](https://github.com/pgbackrest/pgbackrest/issues/1317); Demande d’intégration [#1336](https://github.com/pgbackrest/pgbackrest/pull/1336); Commit [`b1d945e`](https://github.com/pgbackrest/pgbackrest/commit/b1d945ebb774c25676155af439b0558e8582bbe5)

**Fonctionnalités :**

- Prise en charge de plusieurs dépôts. (*Contribution de Cynthia Shang, David Steele. Révisé par Stefan Fercot, Stephen Frost.*)

  Jusqu'à quatre dépôts peuvent être configurés, par exemple un dépôt local pour les restaurations rapides et un dépôt distant pour la redondance. `archive-push` envoie les WAL à tous les dépôts, et les sauvegardes sont planifiées pour chaque dépôt. Certaines commandes agissent sur tous les dépôts, tandis que d'autres exigent `repo`. `repo` n'est pas nécessaire lorsque seul `repo1` est configuré.

  [`3408f1e`](https://github.com/pgbackrest/pgbackrest/commit/3408f1ee2ee3f774699a15de045e0afe3eaf9a26) Améliorer la prise en charge de plusieurs dépôts par expire. ; Demande d’intégration [#1289](https://github.com/pgbackrest/pgbackrest/pull/1289)

  [`e28f6f1`](https://github.com/pgbackrest/pgbackrest/commit/e28f6f11e97a80e9c1adf1a6eaeeabbfc991914f) Poursuivre expire après une erreur de traitement d'un dépôt. ; Demande d’intégration [#1308](https://github.com/pgbackrest/pgbackrest/pull/1308)

  [`bec3e20`](https://github.com/pgbackrest/pgbackrest/commit/bec3e20b2cb061ef0413df24234ebe246ea53063) Ajouter la prise en charge de plusieurs dépôts à archive-get. ; Demande d’intégration [#1292](https://github.com/pgbackrest/pgbackrest/pull/1292)

  [`118d9e6`](https://github.com/pgbackrest/pgbackrest/commit/118d9e64fea71c2e049b52802e55f72f5793871b) Améliorer la prise en charge de plusieurs dépôts par restore. ; Demande d’intégration [#1300](https://github.com/pgbackrest/pgbackrest/pull/1300)

  [`065b2ff`](https://github.com/pgbackrest/pgbackrest/commit/065b2ff2300a9f06a8c32621fac521451ca942bd) Refactoriser repoMin/Max de la commande info.

  [`0ddc038`](https://github.com/pgbackrest/pgbackrest/commit/0ddc0380ff408f9ed6e8bcd4d328df500681ce77) Supprimer le dépôt par défaut de restore dans les tests d'intégration.

  [`13dc8e6`](https://github.com/pgbackrest/pgbackrest/commit/13dc8e68d74fa9e06180e67b7e59994767b4a34d) Rendre --repo facultatif pour backup. ; Demande d’intégration [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`a1280c4`](https://github.com/pgbackrest/pgbackrest/commit/a1280c41e530500e5bbde73a900683f6db207686) Faire fonctionner les avertissements de archive-push comme ceux de archive-get.

  [`3b8f0ef`](https://github.com/pgbackrest/pgbackrest/commit/3b8f0ef7ae8a81ae969934fff4ad3da299454b24) Ajouter la tolérance aux erreurs d'écriture à archive-push. ; Demande d’intégration [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`95063f6`](https://github.com/pgbackrest/pgbackrest/commit/95063f6812279cd59380fd72e16e67b631582bd0) Rendre --repo facultatif pour les commandes restantes sauf stanza-delete.

  [`1dbb3bf`](https://github.com/pgbackrest/pgbackrest/commit/1dbb3bf50b94dcc9d53dfe1e5ad57a17bd6d38e8) Prise en charge de plusieurs dépôts. ; Demande d’intégration [#1227](https://github.com/pgbackrest/pgbackrest/pull/1227)

  [`31c7824`](https://github.com/pgbackrest/pgbackrest/commit/31c7824a4d84cbf5a0ba0938f4caa546fa67af0a) Permettre l'exécution distante des commandes stanza-*. ; Demande d’intégration [#1326](https://github.com/pgbackrest/pgbackrest/pull/1326)

  [`2789d3b`](https://github.com/pgbackrest/pgbackrest/commit/2789d3b6206c4de9299a3bc459e04cdab793abc9) Améliorer la tolérance aux erreurs de info. ; Demande d’intégration [#1342](https://github.com/pgbackrest/pgbackrest/pull/1342)

  [`01b8e22`](https://github.com/pgbackrest/pgbackrest/commit/01b8e2258f6efa5386665c33cb5c267c154376fb) Améliorer la tolérance aux erreurs de archive-push. ; Demande d’intégration [#1343](https://github.com/pgbackrest/pgbackrest/pull/1343)
- Prise en charge de GCS pour le stockage du dépôt. (*Révisé par Cynthia Shang. Testé par Daniel Farina.*)

  Définissez `repo-type=gcs` pour stocker le dépôt sur GCS ou un stockage objet compatible GCS.

  [`dcb79ab`](https://github.com/pgbackrest/pgbackrest/commit/dcb79ab8fb18c63c2d56ecacd9d680b999ea044b) Décoder les caractères JSON échappés par \u.

  [`1b4b353`](https://github.com/pgbackrest/pgbackrest/commit/1b4b3538cc218f66ed1e903c3caeade4b0ab1120) Renommer uri en path lorsque cela convient dans les modules HTTP et de stockage.

  [`66a4ff4`](https://github.com/pgbackrest/pgbackrest/commit/66a4ff496afe63305cb1a437bcb52d1efc11edf7) Encoder le chemin avant de le transmettre à HttpRequest.

  [`d485609`](https://github.com/pgbackrest/pgbackrest/commit/d4856096587c72daee76f8ad8408db677a16d6dd) Ajouter strNewEncode(), strCatEncode() et bufNewDecode().

  [`abcbe0f`](https://github.com/pgbackrest/pgbackrest/commit/abcbe0f9c1804ecb1b93b811cfb0a362c17e1b85) Regrouper les fichiers du module encode en un seul.

  [`edab2a0`](https://github.com/pgbackrest/pgbackrest/commit/edab2a0b89eabc5fd5ba6e795d938670bd5d3105) Utiliser switch plutôt que if-else pour les types d'encodage.

  [`f6c3262`](https://github.com/pgbackrest/pgbackrest/commit/f6c3262861252b24e7e0cffd6d67e0c5e3291f3e) Ne pas exposer les fonctions valid/validate du module encode.

  [`a1f4fd3`](https://github.com/pgbackrest/pgbackrest/commit/a1f4fd32a1790e569ccae3598cd9648bb25d13b6) Ajouter ASSERT_MSG().

  [`00b60e5`](https://github.com/pgbackrest/pgbackrest/commit/00b60e564eef13f8adba0ab867fcde2c352669d6) Ajouter l'encodage base64url.

  [`54c4eb0`](https://github.com/pgbackrest/pgbackrest/commit/54c4eb0c10758879b4bf2b96efd2a1523ecccc21) Rendre les objets de stockage distant accessibles en écriture.

  [`088662d`](https://github.com/pgbackrest/pgbackrest/commit/088662d986288843d1bfd118b724091c93df4569) Prise en charge de GCS pour le stockage du dépôt. ; Ticket [#631](https://github.com/pgbackrest/pgbackrest/issues/631); Ticket [#743](https://github.com/pgbackrest/pgbackrest/issues/743); Demande d’intégration [#1320](https://github.com/pgbackrest/pgbackrest/pull/1320)
- Ajout de l'option `archive-header-check`. (*Révisé par Stephen Frost, Cynthia Shang. Suggéré par Hans-Jürgen Schönig.*)

  L'en-tête WAL est vérifié par rapport à la version de PostgreSQL et à l'identifiant système afin de garantir l'envoi des WAL à la bonne stanza. Cette vérification est activée par défaut et peut être désactivée si nécessaire, par exemple pour des WAL chiffrés.

  Demande d’intégration [#1298](https://github.com/pgbackrest/pgbackrest/pull/1298); Commit [`b6106f3`](https://github.com/pgbackrest/pgbackrest/commit/b6106f3c1f586b410c50c9da8dcea583cc157423)

**Améliorations :**

- Inclure les bases de données système recréées lors d'une restauration sélective. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang.*)

  Une base système (`template0`, `template1` ou `postgres`) recréée possède un OID qui la fait apparaître comme une base utilisateur. Ces bases sont désormais toujours restaurées, quel que soit leur OID.

  Ticket [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Demande d’intégration [#1307](https://github.com/pgbackrest/pgbackrest/pull/1307); Commit [`6942ff5`](https://github.com/pgbackrest/pgbackrest/commit/6942ff569dd950a5146faa0bebfee69e241c4179)
- Exclure `content-length` des en-têtes signés S3. (*Révisé par Cynthia Shang. Suggéré par Brian P Bockelman.*)

  Certains proxys modifient l'en-tête `content-length`, ce qui faisait échouer l'authentification lorsqu'il était signé.

  Ticket [#1340](https://github.com/pgbackrest/pgbackrest/issues/1340); Demande d’intégration [#1341](https://github.com/pgbackrest/pgbackrest/pull/1341); Commit [`7d7ac0e`](https://github.com/pgbackrest/pgbackrest/commit/7d7ac0e0eb63a02bbc1dd8bd8fc89c6008c740f8)
- Consolider les options de stockage du dépôt moins couramment utilisées. (*Révisé par Cynthia Shang.*)

  Les options S3 et Azure de CA, d'hôte, de port et de vérification TLS sont renommées en `repo-storage-*` ; par exemple, `repo1-s3-host` devient `repo1-storage-host`. Les anciens noms restent acceptés.

  Demande d’intégration [#1321](https://github.com/pgbackrest/pgbackrest/pull/1321); Commit [`d1aa765`](https://github.com/pgbackrest/pgbackrest/commit/d1aa765a9d5f290738c1de00c5ea99d5f6056ba5)
- Permettre un `config-path` par défaut personnalisé avec `./configure --with-configdir`. (*Contribution de Michael Schout. Révisé par David Steele.*)

  Les empaqueteurs peuvent choisir une autre valeur par défaut de `config-path` lors de la compilation. Sans cette option, la valeur par défaut reste `/etc/pgbackrest`.

  [`6a717e0`](https://github.com/pgbackrest/pgbackrest/commit/6a717e032f1309ddc9dc955042b5e2ac2bc7324d) Définir le chemin de configuration dans le script configure.

  [`9243962`](https://github.com/pgbackrest/pgbackrest/commit/9243962b9504787c6f4af42318af6dc27094136d) Permettre un config-path par défaut personnalisé avec ./configure --with-configdir. ; Ticket [#1251](https://github.com/pgbackrest/pgbackrest/issues/1251); Ticket [#1293](https://github.com/pgbackrest/pgbackrest/issues/1293); Demande d’intégration [#1255](https://github.com/pgbackrest/pgbackrest/pull/1255)
- Journaliser la copie de l'archive pendant `backup`. (*Révisé par Cynthia Shang, Stefan Fercot.*)

  Ticket [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Demande d’intégration [#1328](https://github.com/pgbackrest/pgbackrest/pull/1328); Commit [`c862e96`](https://github.com/pgbackrest/pgbackrest/commit/c862e9654aff198167efeb897957bf93c1afe453)

**Améliorations de la documentation :**

- Mettre à jour la référence pour inclure des liens vers des exemples du guide utilisateur. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  La référence des commandes renvoie désormais aux sections du guide utilisateur contenant des exemples, et certaines descriptions ont été clarifiées, notamment `set` pour `expire`.

  Demande d’intégration [#1353](https://github.com/pgbackrest/pgbackrest/pull/1353); Commit [`d372dd6`](https://github.com/pgbackrest/pgbackrest/commit/d372dd652c9a01b72444998d87f0f44464676803)
- Mettre à jour la documentation de la restauration sélective avec des avertissements. (*Révisé par Cynthia Shang, Stefan Fercot.*)

  La récupération peut échouer si `type=immediate` n'est pas spécifié, car PostgreSQL signale les pages remplies de zéros comme des erreurs une fois la cohérence atteinte. Sur PostgreSQL >= 13, `ignore_invalid_pages` peut être utilisé, mais il faut vérifier les journaux pour rechercher des pages invalides dans les bases sélectionnées.

  Ticket [#796](https://github.com/pgbackrest/pgbackrest/issues/796); Demande d’intégration [#1329](https://github.com/pgbackrest/pgbackrest/pull/1329); Commit [`92d12cc`](https://github.com/pgbackrest/pgbackrest/commit/92d12ccb9bd0787e30441794e2a2a4d4a4e0fe9c)
- Ajouter une clarification sur `compress-type` dans la documentation de `archive-copy`. (*Révisé par Cynthia Shang, Stefan Fercot.*)

  Les WAL doivent être recompressés lorsque `archive-push` et `backup` utilisent des `compress-type` différents, ce qui peut être coûteux.

  Ticket [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Demande d’intégration [#1327](https://github.com/pgbackrest/pgbackrest/pull/1327); Commit [`9506ffa`](https://github.com/pgbackrest/pgbackrest/commit/9506ffae39dd86d2c5454511026f1249097d96a2)
- Ajouter les valeurs par défaut de `compress-level` en fonction de la valeur de `compress-type`. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  Les valeurs par défaut sont 9 pour `bz2`, 6 pour `gz`, 1 pour `lz4` et 3 pour `zst`.

  Ticket [#1242](https://github.com/pgbackrest/pgbackrest/issues/1242); Demande d’intégration [#1346](https://github.com/pgbackrest/pgbackrest/pull/1346); Commit [`3e20608`](https://github.com/pgbackrest/pgbackrest/commit/3e206088e79c4a73a20b8f2fda1706c6b95fa188)
- Ajouter une note indiquant que les paramètres NFS requis doivent être identiques à ceux de PostgreSQL. (*Contribution de Cynthia Shang. Révisé par David Steele.*)

  Ticket [#871](https://github.com/pgbackrest/pgbackrest/issues/871); Demande d’intégration [#1347](https://github.com/pgbackrest/pgbackrest/pull/1347); Commit [`7598762`](https://github.com/pgbackrest/pgbackrest/commit/75987621fab5f57d0e95b42eabd301731587c438)

### Notes de version v2.32 {#v232-release-notes}

*Commandes du dépôt*

*Sortie le 8 février 2021*

**Correctifs de bogues :**

- Corriger la reprise après suppression partielle d'une sauvegarde par une reprise antérieure. (*Révisé par Cynthia Shang. Signalement par Tom Swartz.*)

**Fonctionnalités :**

- Ajouter la commande `repo-ls`. (*Révisé par Cynthia Shang. Testé par Stefan Fercot.*)
- Ajouter la commande `repo-get`. (*Contribution de Stefan Fercot, David Steele. Révisé par Cynthia Shang.*)
- Ajouter l'option `archive-mode-check`. (*Contribution de Stefan Fercot. Révisé par David Steele. Testé par Michael Banck.*)

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
- Ajoute l'option `repo-azure-endpoint`. (*Révisé par Cynthia Shang. Testé par Brian Peterson. Suggéré par Brian Peterson.*)
- Ajoute l'option `pg-database`. (*Révisé par Cynthia Shang.*)

**Améliorations :**

- Améliorer la sortie de la commande `info` lorsqu'une stanza est spécifiée mais manquante. (*Contribution de Stefan Fercot. Révisé par Cynthia Shang, David Steele. Suggéré par uspen.*)
- Améliorer les performances des listes de fichiers volumineuses dans les commandes `backup`/`restore`. (*Révisé par Cynthia Shang. Testé par Oscar.*)
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

- Récupérer automatiquement les identifiants temporaires S3 sur les instances AWS. (*Contribution de David Steele, Stephen Frost. Révisé par Cynthia Shang, Aleš Zelený, Jeanette Bromage. Testé par David Youatt.*)
- Ajouter l'option `archive-mode` pour désactiver l'archivage lors d'une restauration. (*Révisé par Stephen Frost. Suggéré par Stephen Frost.*)

**Améliorations :**

- Prise en charge de PostgreSQL 13 beta3. Les modifications apportées aux versions de contrôle/catalogue/WAL dans les versions beta ultérieures peuvent rompre la compatibilité, mais pgBackRest sera mis à jour à chaque version pour suivre l'évolution.
- Prise en charge de l’asynchrone `list`/`remove` pour le stockage S3/Azure. (*Révisé par Cynthia Shang, Stephen Frost.*)
- Amélioration de l'utilisation mémoire lors de la détection des relations non enregistrées lors de la construction du manifeste. (*Révisé par Cynthia Shang, Stephen Frost, Oscar. Testé par Brad Nicholson. Suggéré par Oscar, Brad Nicholson.*)
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

- Prise en charge d'Azure pour le stockage du dépôt. (*Révisé par Cynthia Shang. Testé par Don Seiler.*)
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

- Implémentation TLS non bloquante. (*Révisé par Cynthia Shang, Stephen Frost. Testé par Slava Moudry.*)
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
