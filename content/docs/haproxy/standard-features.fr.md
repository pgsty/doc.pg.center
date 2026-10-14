---
title: "Fonctionnalités standard"
linkTitle: "Fonctionnalités standard"
weight: 50
description: "Extraction d'échantillons, cartes, listes ACL, commutation de contenu, tables de persistance, réécriture et protection des serveurs"
icon: fa-solid fa-sliders
module: [HAPROXY]
categories: [Concept]
aliases:
  - /haproxy/intro/standard-features/
  - /docs/haproxy/intro/standard-features/
  - /haproxy/standard-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 3.4–3.4.8"
---

Dans cette section, sont énumérées certaines fonctionnalités très couramment utilisées avec HAProxy mais qui ne sont pas nécessairement disponibles sur d'autres répartiteurs de charge.

## 3.4.1. Fonctionnalités standard : Échantillonnage et conversion d'informations {#section-3-4-1}

HAProxy prend en charge l'extraction d'échantillons à l'aide d'une large gamme de « fonctions d'extraction d'échantillon ». Le principe consiste à extraire des éléments d'information appelés échantillons, destinés à une utilisation immédiate. Cela est utilisé pour la persistance de session, la création de conditions, la génération d'informations dans les journaux ou l'enrichissement des en-têtes HTTP.

Les échantillons peuvent être récupérés à partir de diverses sources :

- constantes : entiers, chaînes, adresses IP, blocs binaires ;

- le processus : date, variables d'environnement, état du serveur/frontal/backend/processus, compteurs/débits d'octets/connexions, longueur de la file d'attente, générateur aléatoire, ...

- variables : variables par session, par requête, par réponse ;

- la connexion cliente : adresses et ports source et destination, ainsi que tous les compteurs de statistiques
    associés ;

- la session client SSL : protocole, version, algorithme, chiffre, taille de clé, identifiant de session, tous les champs du certificat client et serveur, numéro de série du certificat, SNI, ALPN, NPN, prise en charge par le client de certaines extensions ;

- contenu des tampons de requête et de réponse : charge utile arbitraire à l'offset/longueur, longueur des données, RDP
  cookie, décodage du type SSL hello, décodage du SNI TLS;

- HTTP (requête et réponse) : méthode, URI, chemin, arguments de chaîne de requête, code d’état, en-têtes, valeurs d’en-tête positionnelles, cookies, captures, authentification, éléments du corps ;

Un échantillon peut ensuite passer par un certain nombre d'opérateurs appelés « convertisseurs » afin d'effectuer une transformation. Un convertisseur consomme un échantillon et en produit un nouveau, éventuellement de type complètement différent. Par exemple, un convertisseur peut être utilisé pour ne retourner que la longueur entière de la chaîne d'entrée, ou pour convertir une chaîne en majuscules. Un nombre arbitraire de convertisseurs peut être appliqué en série à un échantillon avant son utilisation finale. Parmi tous les convertisseurs d'échantillons disponibles, les suivants sont les plus couramment utilisés :

- opérateurs arithmétiques et logiques : ils permettent d'effectuer des calculs avancés sur les données d'entrée, tels que le calcul de rapports, de pourcentages ou simplement la conversion d'une unité à une autre ;

- Les masques d'adresse IP sont utiles lorsque certaines adresses doivent être regroupées par réseaux plus grands ;

- représentation des données : décodage URL, base64, hexadécimal, chaînes JSON, hachage ;

- conversion de chaîne : extraire des sous-chaînes à des positions fixes, de longueur fixe, extraire des champs spécifiques autour de certains délimiteurs, extraire des mots précis, modifier la casse, appliquer une substitution basée sur une expression régulière ;

- conversion de date : convertir au format de date HTTP, convertir entre heure locale et UTC, et ajouter ou supprimer un décalage ;

- rechercher une entrée dans une table de persistance afin de trouver des statistiques ou le serveur affecté ;

- conversion clé-valeur basée sur une carte à partir d'un fichier (utilisée principalement pour la géolocalisation).

## 3.4.2. Fonctionnalités standard : Maps {#section-3-4-2}

Les cartes sont un type puissant de convertisseur consistant à charger un fichier à deux colonnes en mémoire au démarrage, puis à rechercher chaque échantillon d'entrée dans la première colonne et à renvoyer le motif correspondant de la deuxième colonne s'il est trouvé, ou une valeur par défaut sinon. Comme la sortie est également un échantillon, elle peut à son tour subir d'autres transformations, y compris d'autres recherches dans des cartes. Les cartes sont principalement utilisées pour traduire l'adresse IP du client en numéro de AS ou code pays, car elles prennent en charge la correspondance la plus longue pour les adresses réseau, mais elles peuvent être utilisées à diverses autres fins.

Une partie de leur force provient de leur capacité à être mises à jour à la volée, soit depuis la ligne de commande, soit à partir de certaines actions utilisant d’autres échantillons, ce qui leur permet de stocker et de récupérer des informations entre des accès successifs. Une autre force réside dans l’indexation basée sur un arbre binaire, qui les rend extrêmement rapides, même lorsqu’elles contiennent des centaines de milliers d’entrées, rendant la géolocalisation très peu coûteuse et facile à mettre en œuvre.

## 3.4.3. Fonctionnalités standard : ACL et conditions {#section-3-4-3}

La plupart des opérations dans HAProxy peuvent être rendues conditionnelles. Les conditions sont construites en combinant plusieurs ACL à l’aide d’opérateurs logiques (ET, OU, NON). Chaque ACL est une série de tests fondés sur les éléments suivants :

- une méthode d'extraction d'échantillon pour récupérer l'élément à tester ;

- une série facultative de convertisseurs permettant de transformer l'élément ;

- une liste de modèles à comparer ;

- une méthode de correspondance pour indiquer comment comparer les modèles avec l'échantillon

Par exemple, l’échantillon peut être extrait de l’en-tête HTTP « Host », puis converti en minuscules, avant d’être comparé à plusieurs modèles regex à l’aide de la méthode de correspondance regex.

Techniquement, les ACL sont basées sur le même noyau que les cartes ; elles partagent exactement la même structure interne, les mêmes méthodes de correspondance de motifs et les mêmes performances. La seule différence réelle réside dans le fait qu’au lieu de renvoyer un échantillon, elles ne renvoient que « trouvé » ou « non trouvé ». En matière d’utilisation, les motifs ACL peuvent être déclarés en ligne dans le fichier de configuration et n’ont pas besoin de fichier dédié. Les ACL peuvent être nommées afin de faciliter leur utilisation ou d’améliorer la lisibilité des configurations. Une ACL nommée peut être déclarée plusieurs fois, et elle évaluera toutes les définitions successivement jusqu’à ce qu’une correspondance soit trouvée.

Environ 13 méthodes différentes de correspondance de modèles sont proposées, dont le masque d'adresse IP, les plages d'entiers, les sous-chaînes et les expressions régulières. Elles fonctionnent comme des fonctions, et tout comme dans n'importe quel langage de programmation, seules les parties nécessaires sont évaluées. Ainsi, lorsqu'une condition impliquant un OU est déjà vraie, les suivantes ne sont pas évaluées, et de même, lorsqu'une condition impliquant un ET est déjà fausse, le reste de la condition n'est pas évalué.

Il n’existe aucune limite pratique au nombre d’ACL déclarées, et un certain nombre d’ACL couramment utilisées sont fournies. Toutefois, l’expérience a montré que les configurations utilisant de nombreuses ACL nommées sont souvent difficiles à dépanner, et qu’il peut parfois être plus simple d’utiliser des ACL anonymes en ligne, car cela réduit le nombre de références en dehors de la portée analysée.

## 3.4.4. Fonctionnalités standard : Commutation de contenu {#section-3-4-4}

HAProxy implémente un mécanisme connu sous le nom de commutation basée sur le contenu. Le principe consiste à ce qu'une connexion ou une requête arrive sur un frontal, puis que les informations transportées par cette requête ou cette connexion soient traitées ; à ce stade, il est possible d'écrire des conditions basées sur des ACLs utilisant ces informations pour déterminer quel backend traitera la requête. Ainsi, le trafic est acheminé vers un backend ou un autre en fonction du contenu de la requête. L'exemple le plus courant consiste à utiliser l'en-tête Host et/ou des éléments du chemin (sous-répertoires ou extensions de nom de fichier) pour décider si une requête HTTP cible un objet statique ou l'application, puis à acheminer le trafic des objets statiques vers un backend composé de serveurs rapides et légers, et tout le reste du trafic vers un serveur d'application plus complexe, constituant ainsi une solution d'hébergement virtuel à granularité fine. Cela est particulièrement pratique pour faire coexister plusieurs technologies dans le cadre d'une solution plus globale.

Un autre cas d'utilisation de la commutation de contenu consiste à utiliser des algorithmes de répartition de charge différents selon divers critères. Un cache peut utiliser un hachage d'URI tandis qu'une application peut utiliser round-robin.

Enfin, et ce n'est pas le moindre point, il permet à plusieurs clients d'utiliser une petite part d'une ressource commune en imposant des limites de connexion par backend (donc par client).

Les règles de commutation de contenu se montrent très performantes, bien que leur efficacité puisse dépendre du nombre et de la complexité des ACL en usage. Il est toutefois possible d’écrire des règles de commutation de contenu dynamiques où une valeur d’échantillon se transforme directement en nom de backend, sans faire appel aux ACL. De telles configurations ont été rapportées comme fonctionnant correctement avec au moins 300 000 backends en production.

## 3.4.5. Fonctionnalités standard : tables de persistance {#section-3-4-5}

Les tables de persistance sont couramment utilisées pour stocker des informations de persistance, c'est-à-dire pour conserver une référence au serveur vers lequel un visiteur donné a été dirigé. La clé est alors l'identifiant associé au visiteur (son adresse source, l'ID SSL de la connexion, un cookie HTTP ou RDP, le numéro de client extrait de l'URL ou de la charge utile, ...) et la valeur stockée est ensuite l'identifiant du serveur.

Les tables de persistance peuvent utiliser trois types d'échantillons différents pour leurs clés : des entiers, des chaînes de caractères et des adresses.
Une seule table de persistance peut être référencée dans un proxy, et elle est désignée partout par le nom du proxy.
Jusqu'à 8 clés peuvent être suivies en parallèle.
L'identifiant du serveur est fixé pendant le traitement d'une requête ou d'une réponse, une fois que la clé et le serveur sont connus.

Le contenu de la table de persistance peut être répliqué en mode actif-actif avec d'autres nœuds HAProxy appelés « peers », ainsi qu'avec le nouveau processus lors d'une opération de rechargement, afin que tous les nœuds de répartition de charge partagent les mêmes informations et prennent les mêmes décisions de routage lorsque les requêtes clients sont réparties sur plusieurs nœuds.

Étant donné que les tables de persistance sont indexées sur les éléments permettant d'identifier un client, elles sont souvent utilisées pour stocker des informations supplémentaires, telles que des statistiques par client. Ces statistiques supplémentaires consomment de l'espace supplémentaire et doivent être déclarées explicitement. Les types de statistiques pouvant être stockées incluent la bande passante entrante et sortante, le nombre de connexions simultanées, le débit et le nombre de connexions sur une période donnée, la quantité et la fréquence des erreurs, certaines balises et certains compteurs spécifiques, etc. Afin de permettre le stockage de ces informations sans être contraint de rester lié à un serveur donné, une fonctionnalité spéciale « suivi » est mise en œuvre, permettant de suivre jusqu'à 3 clés simultanées provenant de tables différentes en même temps, indépendamment des règles de persistance. Chaque statistique stockée peut être recherchée, exportée et effacée depuis la CLI et enrichit les capacités de dépannage en temps réel.

Bien que ce mécanisme puisse être utilisé pour surclasser un visiteur de retour ou ajuster la qualité du service fourni en fonction du comportement (bon ou mauvais), il est principalement employé pour lutter contre l’abus de service et, plus généralement, les attaques DDoS, car il permet de mettre en œuvre des modèles complexes pour détecter certains comportements malveillants à une vitesse de traitement élevée.

## 3.4.6. Fonctionnalités standard : chaînes formatées {#section-3-4-6}

HAProxy doit manipuler de nombreuses chaînes de caractères, par exemple dans les journaux, les redirections, l’ajout d’en-têtes, etc. Afin de garantir la plus grande flexibilité, la notion de chaînes formatées a été introduite, initialement pour les journaux, ce qui explique pourquoi elle est toujours appelée « log-format ». Ces chaînes contiennent des caractères d’échappement permettant d’insérer diverses données dynamiques, y compris des variables et des expressions d’extraction d’échantillon, ainsi que de modifier le codage pendant la conversion du résultat en chaîne (par exemple, en ajoutant des guillemets). Cela offre un moyen puissant de construire le contenu d’en-têtes, de générer des données de réponse ou même des modèles de réponse, ou encore de personnaliser les lignes de journal. En outre, pour simplifier la construction des chaînes les plus courantes, environ 50 balises spéciales sont fournies comme raccourcis pour des informations fréquemment utilisées dans les journaux.

## 3.4.7. Fonctionnalités standard : réécriture et redirection HTTP {#section-3-4-7}

Installer un répartiteur de charge devant une application qui n'a jamais été conçue pour cela peut s'avérer une tâche difficile sans les outils appropriés. L'une des opérations les plus fréquemment demandées dans ce cas consiste à ajuster les en-têtes des requêtes et des réponses afin que le répartiteur de charge semble être le serveur d'origine et corriger les informations codées en dur. Cela implique de modifier le chemin des requêtes (ce qui est fortement déconseillé), de modifier le champ d'en-tête Host, de modifier le champ d'en-tête de réponse Location pour les redirections, de modifier les attributs de chemin et de domaine pour les cookies, et ainsi de suite. Il arrive également qu’un certain nombre de serveurs soient excessivement verbeux et tendent à révéler trop d’informations dans les réponses, ce qui les rend plus vulnérables aux attaques ciblées. Bien que, théoriquement, ce ne soit pas le rôle d’un répartiteur de charge de nettoyer ces informations, en pratique, il se trouve au meilleur emplacement dans l’infrastructure pour garantir que tout soit correctement nettoyé.

De même, le répartiteur de charge peut parfois devoir intercepter certaines requêtes et répondre par une redirection vers une nouvelle URL cible. Bien que certaines personnes aient tendance à confondre les redirections et la réécriture, il s'agit de deux concepts totalement différents : la réécriture fait voir des choses différentes au client et au serveur (et entraîne un désaccord sur l'emplacement de la page visitée), tandis que les redirections demandent au client de visiter la nouvelle URL afin qu'il voie le même emplacement que le serveur.

Pour ce faire, HAProxy prend en charge diverses possibilités de réécriture et de redirection, parmi lesquelles :

- réécriture d'URL et d'en-têtes basée sur des expressions régulières dans les requêtes et les réponses. Les expressions régulières sont l'outil le plus couramment utilisé pour modifier les valeurs d'en-tête, car elles sont faciles à manipuler et bien comprises ;

- Les en-têtes peuvent également être ajoutés, supprimés ou remplacés selon des chaînes formatées, afin de transmettre des informations (par exemple, l'algorithme et le chiffre TLS côté client) ;

- Les redirections HTTP peuvent utiliser n'importe quel code 3xx vers une URI relative, absolue ou entièrement dynamique (chaîne formatée) ;

- Les redirections HTTP prennent également en charge certaines options supplémentaires, telles que la définition ou la suppression d'un cookie spécifique, la suppression de la chaîne de requête, l'ajout d'une barre oblique si elle est manquante, etc. ;

- une puissante directive « return » permet de personnaliser chaque partie d'une réponse, comme le statut, les en-têtes ou le corps, en utilisant des contenus dynamiques ou même des fichiers modèles.

- toutes les opérations prennent en charge des conditions basées sur les ACL ;

## 3.4.8. Fonctionnalités standard : protection des serveurs {#section-3-4-8}

HAProxy met tout en œuvre pour maximiser la disponibilité du service, et à cet effet, il déploie de grands efforts pour protéger les serveurs contre la surcharge et les attaques. Le premier et le plus important point est que seules les requêtes complètes et valides sont acheminées vers les serveurs. La raison première est que HAProxy doit identifier les éléments du protocole nécessaires pour rester synchronisé avec le flux d’octets, et la deuxième raison est qu’aussi longtemps que la requête n’est pas complète, il n’existe aucun moyen de savoir si certains éléments pourraient modifier sa sémantique. Le bénéfice direct de cette approche est que les serveurs ne sont pas exposés à des requêtes invalides ou incomplètes. Cela constitue une protection très efficace contre les attaques slowloris, qui n'ont presque aucun impact sur HAProxy.

Un autre point important est que HAProxy dispose de tampons pour stocker les requêtes et les réponses, et qu’en n’envoyant une requête au serveur que lorsqu’elle est complète, et en lisant entièrement la réponse très rapidement depuis le réseau local, la connexion côté serveur est utilisée pendant une durée très brève, ce qui préserve au maximum les ressources du serveur.

Une extension directe de cette fonctionnalité est que HAProxy peut limiter artificiellement le nombre de connexions simultanées ou de requêtes en attente vers un serveur, garantissant ainsi que le serveur ne sera jamais surchargé, même en cas de pointe de trafic où il fonctionnerait continuellement à 100 % de sa capacité. Toutes les requêtes excédentaires seront simplement mises en file d'attente pour être traitées lorsqu'une place se libère. En fin de compte, cette économie importante de ressources garantit souvent des temps de réponse du serveur bien meilleurs, ce qui se traduit par une performance réelle supérieure à celle obtenue en surchargeant le serveur. Les requêtes en attente peuvent être réacheminées vers d'autres serveurs, ou même annulées en file d'attente si le client se déconnecte, ce qui protège également les serveurs contre l'effet « rechargement », où chaque clic sur « recharger » d’un visiteur sur une page à chargement lent déclenche généralement une nouvelle requête et maintient le serveur dans un état surchargé.

Le mécanisme de démarrage progressif protège également les serveurs redémarrés contre des niveaux élevés de trafic pendant qu'ils finalisent encore leur démarrage ou qu'ils compilent certaines classes.

En ce qui concerne la protection au niveau du protocole, il est possible de relâcher l'analyseur HTTP afin d'accepter des requêtes ou réponses non conformes mais inoffensives, voire de les corriger. Cela permet d'accéder à des applications défectueuses pendant qu'une correction est en cours de développement. Parallèlement, les messages problématiques sont entièrement capturés avec un rapport détaillé qui aide les développeurs à identifier la cause dans l'application. Les violations de protocole les plus dangereuses sont correctement détectées, traitées et corrigées. Par exemple, les requêtes ou réponses malformées comportant deux en-têtes Content-Length sont soit corrigées si leurs valeurs sont identiques, soit rejetées si elles diffèrent, car cela devient un problème de sécurité. L'inspection de protocole n'est pas limitée à HTTP, elle est également disponible pour d'autres protocoles tels que TLS ou RDP.

Lorsqu'une violation de protocole ou une attaque est détectée, diverses options sont disponibles pour répondre à l'utilisateur, telles que le renvoi de la classique « HTTP 400 bad request », la fermeture de la connexion par un reset TCP, ou la simulation d'une erreur après un délai prolongé (« tarpit ») afin de troubler l'attaquant. Toutes ces mesures contribuent à protéger les serveurs en décourageant le client fautif de poursuivre une attaque devenue très coûteuse à maintenir.

HAProxy propose également des options plus avancées pour protéger contre les fuites de données accidentelles et les croisements de session. Non seulement il peut journaliser les réponses suspectes du serveur, mais il peut également journaliser et, optionnellement, bloquer une réponse pouvant compromettre la confidentialité d’un visiteur donné. Un exemple en est un cookie pouvant être mis en cache apparaissant dans une réponse pouvant être mise en cache, ce qui pourrait entraîner la livraison de ce cookie à un autre visiteur par un cache intermédiaire, provoquant ainsi un partage de session accidentel.
