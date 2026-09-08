---
title: "Actualités"
linkTitle: "Actualités"
weight: 10
description: "Actualités officielles du projet pgBackRest, annonces de versions et mises à jour de maintenance."
icon: fa-solid fa-newspaper
module: [PGBACKREST]
categories: [Référence]
aliases: [/pgbackrest/news/]
upstream_link: "https://pgbackrest.org/news.html"
---

--------

## pgBackRest 2.59.1 publié {#release-2-59-1}

**17 août 2026**

La communauté pgBackRest est heureuse d'annoncer la sortie de [pgBackRest](https://pgbackrest.org) 2.59.1, la dernière version de la solution fiable, facile à utiliser, de sauvegarde et de restauration, pouvant s'adapter sans heurt aux plus grandes bases de données et charges de travail.

pgBackRest prend en charge un ensemble complet de fonctionnalités pour gérer votre infrastructure de sauvegarde et de récupération, notamment : sauvegarde/restauration en parallèle, sauvegardes complètes/différentielles/sauvegardes incrémentielles, sauvegarde incrémentielle par bloc, plusieurs dépôts, restauration par delta, archivage asynchrone en parallèle, protection contre les logiciels malveillants/rançongiciels, sommes de contrôle par fichier, sommes de contrôle par page (lorsqu’activées) validées pendant la sauvegarde, plusieurs types de compression, chiffrement, reprise partielle/échouée de sauvegarde, sauvegarde depuis un serveur secondaire, prise en charge des espaces de table et des liens, prise en charge de S3/Azure/GCS/SFTP, expiration des sauvegardes, opérations locales/distantes via SSH ou TLS, configuration flexible, et bien plus encore.

pgBackRest peut être installé à partir du [dépôt Yum PostgreSQL](https://yum.postgresql.org) ou du [dépôt APT PostgreSQL](https://apt.postgresql.org) ; des paquets sont également disponibles pour de nombreuses autres distributions. Le code source peut être téléchargé depuis [releases](/fr/docs/pgbackrest/release/).

### Nouvelles fonctionnalités et correctifs de bogues {#release-2-59-1-feature}

- Prise en charge de PostgreSQL 19beta3 (Lardière Sébastien)
- Correction d'un blocage lorsque la taille du tampon de morceau est inférieure à celle du tampon d'entrée (David Steele)
- Comparer une étiquette de sauvegarde nouvelle uniquement avec son propre jeu de sauvegardes complètes (David Steele)
- Correction des archives sources générées par GitHub qui manquaient des fichiers nécessaires à la compilation (David Steele)

Consultez les [Notes de version 2.59.1](/fr/docs/pgbackrest/release/#v2591-release-notes) pour obtenir des corrections et améliorations supplémentaires.

### Remarques importantes {#release-2-59-1-note}

- PostgreSQL 19beta3 a modifié le format WAL, de sorte que les WAL archivés depuis une version antérieure de PostgreSQL 19 beta ne sont plus lisibles. Les clusters exécutant une version antérieure du beta doivent être recréés avec 19beta3.

### Liens {#release-2-59-1-link}

- [Site web](/fr/docs/pgbackrest/)
- [Guides utilisateur](/fr/docs/pgbackrest/user-guide/)
- [Notes de version](/fr/docs/pgbackrest/release/)

### Parrainage {#release-2-59-1-sponsorship}

Ce correctif a été rendu possible grâce au généreux parrainage de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com), et [Data Egret](https://dataegret.com/).


--------

## Nouveau paquet tar de distribution {#distribution-tarball}

**20 juillet 2026**

À compter de la version 2.59.0 de pgBackRest, chaque version inclut un fichier tarball de distribution qui simplifie la compilation à partir des sources. Contrairement à un extrait du dépôt git, le fichier tarball contient les sources générées et la documentation rendue préalablement construites, de sorte que pgBackRest peut être compilé et installé sans nécessiter les outils de génération de code ni de documentation requis par un extrait du dépôt.

Le paquet tar contient le code source de pgBackRest avec le code prégénéré, la page de manuel de référence des commandes, la documentation HTML et un test de fumée pour vérifier la compilation. Il se compile avec meson et ninja en utilisant uniquement les bibliothèques habituelles de pgBackRest.

Le fichier archive est joint à chaque version en tant que fichier joint nommé `pgbackrest-{version}.tar.gz`, accompagné de la somme de contrôle correspondante `.sha256sum`. Téléchargez-le depuis la page [releases](https://github.com/pgbackrest/pgbackrest/releases) sur GitHub, puis consultez le fichier `README.md` contenu dans l'archive pour obtenir les instructions de compilation et de test.

Les paquetisateurs sont encouragés à effectuer les compilations à partir du tarball de distribution afin d’éviter les outils de construction supplémentaires que nécessitera à l’avenir la génération du code et de la documentation.


--------

## pgBackRest 2.59.0 publié {#release-2-59-0}

**20 juillet 2026**

La communauté pgBackRest est heureuse d'annoncer la sortie de [pgBackRest](https://pgbackrest.org) 2.59.0, la dernière version de la solution fiable, facile à utiliser, pour la sauvegarde et la restauration, qui s'adapte sans heurt aux plus grandes bases de données et charges de travail.

pgBackRest prend en charge un ensemble complet de fonctionnalités pour gérer votre infrastructure de sauvegarde et de récupération, notamment : sauvegarde/restauration en parallèle, sauvegardes complètes/différentielles/sauvegardes incrémentielles, sauvegarde incrémentielle par bloc, plusieurs dépôts, restauration par delta, archivage asynchrone en parallèle, protection contre les logiciels malveillants/rançongiciels, sommes de contrôle par fichier, sommes de contrôle par page (lorsqu’activées) validées pendant la sauvegarde, plusieurs types de compression, chiffrement, reprise partielle/échouée de sauvegarde, sauvegarde depuis un serveur secondaire, prise en charge des espaces de table et des liens, prise en charge de S3/Azure/GCS/SFTP, expiration des sauvegardes, opérations locales/distantes via SSH ou TLS, configuration flexible, et bien plus encore.

pgBackRest peut être installé à partir du [dépôt Yum PostgreSQL](https://yum.postgresql.org) ou du [dépôt APT PostgreSQL](https://apt.postgresql.org) ; des paquets sont également disponibles pour de nombreuses autres distributions. Le code source peut être téléchargé depuis [releases](/fr/docs/pgbackrest/release/).

### Nouvelles fonctionnalités et améliorations importantes {#feature}

- Prise en charge de PostgreSQL 19 (David Steele)
- Ajouter l'option `archive-expire-before` pour nettoyer l'archive WAL (Stefan Fercot)
- Ajouter la prise en charge des S3 Outposts (Shiva Kumar Ambigi)
- Ajouter l'authentification par processus S3 (David Steele)
- Ajouter le cache utilisateur/groupe pour une construction plus rapide du manifeste (Gunnar Lindholm)
- Reconnecter le stockage SFTP après que le serveur a fermé une connexion inactif (David Steele)
- Ajouter la progression par répertoire de sauvegarde dans la sortie de la commande `info` (Will Morland)
- Ajouter la suppression par lots pour le stockage Azure (David Steele)
- Ajouter des vérifications `backup.info` à la commande `verify` (Denis Garsh)
- Permettre la configuration du point de terminaison STS S3 (Simon Gratton)
- Ajouter l'intégration avec systemd notify (Andrew Jackson)
- Erreur lors de l'exécution en tant que root sauf si `allow-root` est activé (David Steele)
- Quitter l'opération asynchrone `archive-push` à la première erreur (David Steele)

Consultez les [Notes de version 2.59.0](/fr/docs/pgbackrest/release/#v2590-release-notes) pour obtenir des informations complémentaires sur les nouvelles fonctionnalités et améliorations.

### Remarques importantes {#note}

-  Seul la commande `restore` peut être exécutée en tant qu'utilisateur root par défaut. Utilisez `allow-root` pour exécuter d'autres commandes en tant qu'utilisateur root (ce qui n'est toutefois pas recommandé).
-  Une nouvelle archive de distribution comprenant la documentation prégénérée, la page de manuel et le code est jointe à chaque version pour simplifier le packaging. Consultez [Nouvelle archive de distribution](#distribution-tarball) pour plus d'informations.
-  Une nouvelle dépendance facultative sur `libsystemd` a été ajoutée.

### Liens {#link}

- [Site web](/fr/docs/pgbackrest/)
- [Guides utilisateur](/fr/docs/pgbackrest/user-guide/)
- [Notes de version](/fr/docs/pgbackrest/release/)

### Parrainage {#sponsorship}

Ce correctif a été rendu possible grâce au généreux parrainage de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com), et [Data Egret](https://dataegret.com/).


--------

## pgBackRest va continuer ! {#will-continue}

**18 mai 2026**

Je suis heureux d’annoncer que pgBackRest va poursuivre son développement ! Au cours des dernières semaines, une coalition de commanditaires s’est réunie afin de financer le développement continu. Leur soutien signifie que le projet n’est plus dépendant d’un seul commanditaire, offrant ainsi à pgBackRest la stabilité nécessaire à long terme.

Je tiens à remercier chacun de nos commanditaires :

[Amazon Web Services](https://aws.amazon.com) fournit des ressources informatiques cloud à la demande aux particuliers, aux entreprises et aux gouvernements. Accédez à une puissance de calcul, au stockage, aux bases de données, à l'apprentissage automatique et à plus de 200 services, en payant uniquement ce que vous utilisez. Conçu pour évoluer avec vous, en investissant dans les communautés que nous partageons.

[Supabase](https://supabase.com), une plateforme backend complète construite sur PostgreSQL, permet aux développeurs de créer et d'évoluer rapidement leurs applications sans gérer l'infrastructure. Elle inclut une base de données PostgreSQL, une authentification utilisateur, des abonnements en temps réel, un stockage de fichiers, des fonctions au bord et des fonctions sans serveur, tous soutenus par une communauté open-source active.

[pgEdge](https://pgedge.com) est une plateforme PostgreSQL open source de classe entreprise pour l'IA, la haute disponibilité et bien plus encore. Elle propose des outils natifs d'IA agentique, un atelier DBA, la supervision et la réponse aux incidents, un déploiement flexible et une maintenance sans interruption. Elle s'étend d'un nœud unique à une architecture multimaître active-active dans le cloud, sur site ou dans des environnements isolés.

[Tiger Data](https://tigerdata.com), créateurs de TimescaleDB, développe la base de données open source pour les séries temporelles construite sur PostgreSQL et exploite Tiger Cloud, une plateforme gérée dédiée aux charges de travail liées aux séries temporelles, à l'analyse et à l'intelligence artificielle. Les options auto-hébergées et cloud permettent aux organisations de capturer, stocker et analyser des séries temporelles à grande échelle, des déploiements aux bords jusqu'aux clouds centralisés.

[Percona](https://percona.com) est une entreprise de logiciels, d'assistance et de services open source qui aide les organisations à conserver le contrôle total de leur infrastructure de données. Elle leur permet d'exploiter MySQL, PostgreSQL, MongoDB, Valkey et Redis de manière sûre et efficace grâce à des logiciels open source librement accessibles, une assistance experte 24/7 et une expertise pratique des bases de données.

[Eon.io](https://eon.io) est une infrastructure cloud intelligente pour la sauvegarde, la récupération et la gestion des données, qui aide les équipes à stocker et à accéder aux sauvegardes de manière plus efficace, rendant les données accessibles pour les workflows d'analyse et d'intelligence artificielle. Elle propose une récupération rapide et granulaire, ainsi qu'un coût de stockage nettement réduit pour PostgreSQL et les charges de travail intensives en données, sur toutes les clouds, y compris la récupération suite à une perte accidentelle de données ou à une régression d'agent d'intelligence artificielle.

Ces organisations comptent sur pgBackRest pour assurer une récupération après sinistre fiable pour leurs produits et clients. Leur investissement reflète le rôle essentiel joué par pgBackRest dans l’écosystème PostgreSQL, et leur soutien collectif garantit la durabilité à long terme du projet.

J'ai hâte de reprendre le travail. Des fonctionnalités et des optimisations sont en cours de développement et je suis impatient de vous les présenter dans les prochaines versions. Merci à nos commanditaires pour avoir rendu cela possible, et merci à la communauté pour votre patience et votre soutien durant cette transition.


--------

## Mise à jour de maintenance {#maintenance-update}

**4 mai 2026**

Après avoir annoncé que je ne maintiens plus pgBackRest, ma boîte de réception s’est remplie. Il a fallu un certain temps pour trier les messages — beaucoup d’entre eux étaient des vœux de bonne chance et des remerciements pour mon travail au fil des années.

Mais un schéma s’est rapidement dessiné. Il est clair que de nombreux utilisateurs de pgBackRest, en particulier ceux qui doivent assister d’autres utilisateurs de pgBackRest, préféreraient que le projet continue avec moi en tant que principal mainteneur. Je le souhaiterais plus que tout, mais après plusieurs mois de financement participatif, j’avais tout juste décidé que cela n’arriverait pas.

La situation a maintenant évolué, et il semble presque certain que je pourrai obtenir suffisamment de financement pour poursuivre le projet. Cette fois, pgBackRest sera financé par une coalition de commanditaires, de sorte qu'une seule acquisition ne pourra plus affecter ma capacité à continuer le travail sur le projet. Nous devrions également pouvoir intégrer un autre mainteneur afin de répartir la charge de travail et assurer une continuité à l’avenir.

Je sais que cela a été une surprise et qu’il y a beaucoup d’incertitudes. Veuillez patienter — la version actuelle de pgBackRest fonctionne, et il n’existe aucun bogue critique ni problème de sécurité en cours, donc il n’est pas nécessaire de créer immédiatement une branche du projet.

J'espère pouvoir annoncer une décision définitive d'ici la fin de la semaine. En attendant, veuillez patienter et sachez que nous travaillons activement à la reprise de pgBackRest.


--------

## pgBackRest n'est plus maintenu {#no-longer-maintained}

**27 avril 2026**

TL;DR : pgBackRest n'est plus maintenu. Si vous créez une branche de pgBackRest, veuillez choisir un nouveau nom pour votre projet.

Après mûre réflexion, j'ai décidé d'arrêter de travailler sur pgBackRest. Je n'ai pas pris cette décision à la légère. pgBackRest a été mon projet personnel passionnant pendant treize ans, et j'ai eu la chance de bénéficier d'un parrainage corporatif pendant une grande partie de cette période, mais il y a aussi eu de nombreuses nuits et fins de semaine passées à faire évoluer pgBackRest jusqu'à ce qu'il devienne ce qu'il est aujourd'hui, avec l'aide de nombreux contributeurs. Chaque développeur logiciel libre sait exactement ce que je veux dire et à quel point une partie de sa vie peut être consacrée à un projet particulier.

Depuis la vente de Crunchy Data, j'assure moi-même le maintien de pgBackRest et je cherche un poste qui me permettrait de poursuivre ce travail, mais jusqu'à présent, je n'ai pas eu de succès. De même, mes tentatives pour obtenir un parrainage se sont avérées bien insuffisantes pour rendre le projet viable.

Comme tout le monde, je dois gagner ma vie, et le nombre de postes liés à pgBackRest est très limité. Je peux désormais envisager une plus large variété d'opportunités, mais celles-ci ne me laisseront pas le temps de travailler sur pgBackRest, qui demande une quantité significative d’heures pour la maintenance, la correction des bogues, l’examen des demandes de tirage, la réponse aux problèmes, etc. Cela ne prend même pas en compte le temps nécessaire à l’écriture de nouvelles fonctionnalités, ce que je préfère par-dessus tout. Plutôt que de mener ce travail de manière médiocre et/ou épisodique, il me semble préférable de faire une pause définitive.

Je suppose qu’à un moment donné, pgBackRest sera forké, mais ce sera un nouveau projet avec de nouveaux responsables, et ceux-ci devront gagner la confiance de la même manière que nous l’avons fait.

Encore merci à l'ensemble des contributeurs de pgBackRest au fil des années. Il a été un réel plaisir de travailler avec vous !
