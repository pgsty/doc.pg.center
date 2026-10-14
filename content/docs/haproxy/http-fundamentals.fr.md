---
title: "1. Petit rappel sur HTTP"
linkTitle: "1. Fondamentaux HTTP"
weight: 120
description: "Transactions HTTP, requêtes, réponses, en-têtes et terminologie du protocole"
icon: fa-solid fa-globe
module: [HAPROXY]
categories: [Concept]
aliases:
  - /haproxy/configuration/http-fundamentals/
  - /haproxy/configuration/
  - /docs/haproxy/configuration/http-fundamentals/
  - /docs/haproxy/configuration/
  - /haproxy/http-fundamentals/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 1"
---

Ce document traite du langage de configuration tel qu’il est implémenté dans la version indiquée ci-dessus. Il ne fournit aucune indication, exemple ou conseil. Pour ce type de documentation, veuillez vous référer au Manuel de référence ou au Manuel d’architecture. Les chapitres numérotés sont ordonnés dans la barre latérale plate de HAProxy pour une navigation directe.

Lorsque HAProxy fonctionne en mode HTTP, la requête et la réponse sont entièrement analysées et indexées, ce qui permet de définir des critères de correspondance sur presque tout élément présent dans leur contenu.

Toutefois, il est essentiel de comprendre comment les requêtes et réponses HTTP sont structurées, ainsi que la manière dont HAProxy les décompose. Il sera alors plus facile d'écrire des règles correctes et de déboguer les configurations existantes.

Tout d'abord, HTTP est standardisé par une série de RFC que HAProxy suit aussi strictement que possible :

- RFC 9110 : Sémantique HTTP (explique le sens des éléments du protocole)
- RFC 9111 : Mise en cache HTTP (explique les règles à suivre pour un cache HTTP)
- RFC 9112 : HTTP/1.1 (représentation, règles d'interopérabilité, sécurité)
- RFC 9113 : HTTP/2 (représentation, règles d'interopérabilité, sécurité)
- RFC 9114 : HTTP/3 (représentation, règles d'interopérabilité, sécurité)

En complément de ces éléments, les RFC 8999 à 9002 définissent la couche transport QUIC utilisée par le protocole HTTP/3.

## 1.1. Le modèle de transaction HTTP {#section-1-1}

Le protocole HTTP est fondé sur des transactions. Cela signifie qu'une requête entraîne une et une seule réponse. À l'origine, avec la version 1.0 du protocole, il y avait une seule requête par connexion : une connexion TCP est établie depuis le client vers le serveur, le client envoie une requête sur la connexion, le serveur répond, puis la connexion est fermée. Une nouvelle requête nécessite donc une nouvelle connexion :

```text
[CON1] [REQ1] ... [RESP1] [CLO1] [CON2] [REQ2] ... [RESP2] [CLO2] ...
```

Dans ce mode, souvent appelé le mode « fermeture HTTP », le nombre d'établissements de connexion correspond au nombre de transactions HTTP. Comme la connexion est fermée par le serveur après la réponse, le client n'a pas besoin de connaître la longueur du contenu ; il considère la réponse comme complète lorsque la connexion se termine. Cela signifie également qu'en cas de troncature de certaines réponses due à des erreurs réseau, le client pourrait à tort considérer qu'une réponse était complète, ce qui pouvait entraîner parfois l'affichage d'images tronquées à l'écran.

En raison de la nature transactionnelle du protocole, il a été possible d'optimiser celui-ci afin d'éviter la fermeture de la connexion entre deux transactions successives. Toutefois, dans ce mode, il est obligatoire que le serveur indique la longueur du contenu pour chaque réponse, afin que le client ne reste pas en attente indéfiniment. Pour cela, un en-tête spécial est utilisé : « Content-length ». Ce mode est appelé le mode « keep-alive », et est apparu avec HTTP/1.1 (certains agents HTTP/1.0 le supportent), et les connexions réutilisées entre requêtes sont appelées des « connexions persistantes » :

```text
[CON] [REQ1] ... [RESP1] [REQ2] ... [RESP2] [CLO] ...
```

Ses avantages sont une latence réduite entre les transactions, une charge de traitement moindre côté serveur, et la capacité à détecter une réponse tronquée. Il est généralement plus rapide que le mode close, mais pas toujours, car certains clients limitent souvent leur nombre de connexions simultanées à une valeur plus faible, ce qui compense moins une connectivité réseau médiocre. En outre, certains serveurs doivent maintenir la connexion ouverte longtemps en attendant une éventuelle nouvelle requête et peuvent subir une utilisation mémoire élevée en raison du grand nombre de connexions, et fermer trop rapidement peut interrompre certaines requêtes arrivées au moment où la connexion était fermée.

Dans ce mode, la taille de la réponse doit être connue à l'avance, ce qui n'est pas toujours possible avec des contenus générés dynamiquement ou compressés. Pour cette raison, un autre mode a été mis en œuvre, le « mode chunké », dans lequel, au lieu d'annoncer la taille totale d'un coup, l'expéditeur indique uniquement la taille du prochain « morceau » de réponse déjà présent dans un tampon, et peut terminer à tout moment avec un morceau de taille nulle. Dans ce mode, l'en-tête Content-Length n'est pas utilisé.

Une autre amélioration des communications est le mode pipelining. Il utilise toujours keep-alive, mais le client n’attend pas la première réponse pour envoyer la deuxième requête. Cela est utile pour récupérer un grand nombre d’images composant une page :

```text
[CON] [REQ1] [REQ2] ... [RESP1] [RESP2] [CLO] ...
```

Cela peut évidemment offrir un bénéfice considérable en performance, car la latence réseau est éliminée entre les requêtes successives. De nombreux agents HTTP ne prennent pas correctement en charge le pipelining, car il n’existe aucun moyen d’associer une réponse à la requête correspondante en HTTP. Pour cette raison, il est obligatoire que le serveur réponde dans le même ordre exact que celui des requêtes reçues. En pratique, après plusieurs tentatives de divers clients pour le mettre en œuvre, il a été complètement abandonné en raison de son manque de fiabilité sur certains serveurs. Toutefois, il est obligatoire que les serveurs le prennent en charge.

L'amélioration suivante est le mode multiplexé, tel qu'il est implémenté dans HTTP/2 et HTTP/3. Plusieurs transactions, c'est-à-dire des paires requête-réponse, sont transmises en parallèle sur une seule connexion et progressent chacune à leur propre rythme, indépendamment les unes des autres. Les protocoles multiplexés ont introduit la notion de « flux » pour représenter ces communications parallèles. Chaque flux reçoit généralement un identifiant unique pour la connexion, utilisé par chaque extrémité pour acheminer les données. Les clients ouvrent couramment de nombreux flux, jusqu'à 100 ou davantage, sur la même connexion et laissent le serveur les trier et répondre dans n'importe quel ordre selon la réponse disponible. Le multiplexage réduit fortement les allers-retours et accélère le chargement des pages sur les réseaux à forte latence. Sur les sites riches en images, celles-ci semblent alors se charger en parallèle.

Ces protocoles ont également amélioré leur efficacité en adoptant des mécanismes de compression des en-têtes afin de réduire le nombre d’octets transmis sur le réseau. Par conséquent, sans outils appropriés, ils ne sont pas réellement manipulables à la main ni lisibles à l’œil nu, contrairement à HTTP/1. Pour cette raison, divers exemples de messages HTTP continuent d’être représentés dans la littérature (y compris dans ce document) à l’aide de la syntaxe HTTP/1, même pour les versions plus récentes du protocole.

HTTP/2 présente certaines limitations liées à sa conception, telles que les pertes de paquets qui affectent simultanément tous les flux, et si un client met trop de temps à récupérer un objet (par exemple, s'il doit le stocker sur le disque), cela peut ralentir sa récupération et rendre impossible l'accès aux données en attente derrière celui-ci durant cette période. Ce phénomène est appelé « blocage en tête de file » ou « HoL blocking », ou parfois simplement « HoL ».

HTTP/3 est implémenté sur QUIC, lui-même implémenté sur UDP. QUIC résout le blocage en tête de file au niveau du transport grâce à des flux gérés indépendamment. En effet, en cas de perte de paquets, un flux impacté n'affecte pas les autres flux, qui demeurent tous accessibles en parallèle. QUIC offre également un support du déplacement de connexion, mais HAProxy ne le prend pas en charge actuellement.

Par défaut, HAProxy utilise le mode keep-alive pour les connexions persistantes : il traite chaque requête et chaque réponse, puis laisse la connexion inactive de part et d'autre entre la fin d'une réponse et le début de la requête suivante. Lorsqu'un client établit une connexion HTTP/2, HAProxy traite les requêtes en parallèle puis laisse la connexion inactive en attendant de nouvelles requêtes, comme pour une connexion HTTP keep-alive.

HAProxy prend en charge essentiellement trois modes de connexion :

- keep-alive : toutes les requêtes et réponses sont traitées, et les connexions côté client ainsi que celles côté serveur sont maintenues ouvertes pour de nouvelles requêtes. Ceci est le comportement par défaut et convient au web moderne et aux protocoles modernes (HTTP/2 et HTTP/3).

- server close : la connexion côté serveur est fermée après la réponse.

- close : la connexion est activement fermée de part et d'autre après la fin de la réponse.

En complément, par défaut, la connexion orientée serveur est réutilisable par toute requête provenant de n'importe quel client, conformément à la spécification du protocole HTTP, de sorte que toute information relative à un client spécifique doit être transmise avec chaque requête, le cas échéant (par exemple, l'adresse source du client, etc.). Lorsqu'HTTP/2 est utilisé avec un serveur, HAProxy affecte par défaut cette connexion au même client afin d'éviter le risque de blocage en tête de file entre clients.

## 1.2. Terminologie {#section-1-2}

À l’intérieur d’HAProxy, la terminologie a évolué au fil du temps pour suivre les évolutions du protocole HTTP et de ses usages. À l’origine, aucune différence significative n’existait entre une connexion, une session, un flux ou une transaction, mais ces termes se sont précisés au fil du temps afin de correspondre étroitement à ce qui existe dans les versions modernes du protocole HTTP, bien que certains termes persistent dans la configuration ou l’interface en ligne de commande afin de préserver la compatibilité historique.

Voici quelques définitions applicables à la version actuelle de HAProxy :

- connection : une connexion est un canal de communication bidirectionnel unique entre un agent distant (client ou serveur) et HAProxy, au niveau le plus bas possible. En général, elle correspond à une socket TCP établie entre une paire d'adresses IP et de ports. Du côté client, les connexions sont les premières entités instanciées lorsqu'un client se connecte à HAProxy, et les règles s'appliquant au niveau de la connexion sont les premières à s'appliquer.

- session : une session ajoute des informations contextuelles associées à une connexion. Cela inclut des informations spécifiques au niveau du transport (par exemple, les clés TLS, etc.) ou des variables. Ce terme est utilisé depuis longtemps dans HAProxy pour désigner les communications HTTP/1.0 bout à bout entre deux extrémités, et il reste visible dans le nom de certaines commandes CLI ou statistiques, même s'il désigne désormais des flux, mais les messages d'aide et les descriptions cherchent à éviter toute ambiguïté. Il reste pertinent dans le cadre de la terminologie au niveau réseau (par exemple, les sessions TCP au sein du système d'exploitation ou les sessions TCP à travers un pare-feu), ou pour les applications utilisateur non HTTP (par exemple, une session telnet ou une session SSH). Il ne doit pas être confondu avec les « sessions applicatives », qui servent à stocker un contexte utilisateur complet dans un cookie et nécessitent d’être envoyées au même serveur.

- stream : un flux correspond exactement à une communication bidirectionnelle point à point au niveau de l'application, où des analyses et des transformations peuvent être appliquées. En HTTP, il contient une seule requête et sa réponse associée, et est instancié à l'arrivée de la requête, se terminant avec la fin de la livraison de la réponse. Dans ce contexte, il existe une relation 1:1 entre un tel flux et le flux d'un protocole multiplexé. En communication TCP, il existe un seul flux par connexion.

- transaction : une transaction n'est qu'une paire constituée d'une requête et de la réponse associée. Ce terme était utilisé en conjonction avec les sessions avant les flux, mais aujourd'hui, une relation 1:1 existe entre une transaction et un flux. Cela est essentiellement visible dans la portée des variables « txn », qui est valable pendant toute la transaction, donc pendant tout le flux.

- requête : elle désigne le trafic allant du client vers le serveur. Elle est principalement utilisée dans le cadre du protocole HTTP pour indiquer où les opérations sont effectuées. Ce terme existe également pour les opérations TCP afin d'indiquer où les données sont traitées. Les requêtes apparaissent souvent dans les compteurs comme unité de trafic ou d'activité. Elles n'impliquent pas toujours de réponse (par exemple en cas d'erreur), mais comme il n'existe pas de réponses spontanées sans requête, les requêtes restent un indicateur pertinent de l'activité globale. En TCP, le nombre de requêtes est égal au nombre de connexions.

- réponse : désigne le trafic circulant du serveur vers le client, ou parfois de HAProxy vers le client, lorsque HAProxy génère lui-même la réponse (par exemple, une redirection HTTP).

- service : cela indique généralement un traitement interne dans HAProxy qui n'exige pas de serveur, comme la page de statistiques, le cache ou un code Lua destiné à implémenter une petite application. Un service lit généralement une requête, effectue certaines opérations et produit une réponse.

## 1.3. Requête HTTP {#section-1-3}

Tout d'abord, examinons cette requête HTTP :

```text
Ligne    Contenu
numéro
   1     GET /serv/login.php?lang=en&profile=2 HTTP/1.1
   2     Host: www.mydomain.com
   3     User-agent: my small browser
   4     Accept: image/jpeg, image/gif
   5     Accept: image/png
```

### 1.3.1. Ligne de requête {#section-1-3-1}

Ligne 1 est la « ligne de requête ». Elle est toujours composée de 3 champs :

-  méthode : GET
-  URI : /serv/login.php?lang=en&profile=2
-  balise de version : HTTP/1.1

Tous sont délimités par ce que la norme appelle LWS (espaces blancs linéaires), qui sont généralement des espaces, mais peuvent aussi être des tabulations ou des sauts de ligne ou retours chariot suivis d'espaces ou de tabulations. La méthode elle-même ne peut contenir aucun deux-points (':') et est limitée aux lettres alphabétiques. Ces différentes combinaisons rendent souhaitable que HAProxy effectue lui-même la séparation plutôt que de laisser l'utilisateur écrire une expression régulière complexe ou inexacte.

L'URI lui-même peut prendre plusieurs formes :

- Une « URI relative » :

```text
  /serv/login.php?lang=en&profile=2

C'est une URL complète sans la partie hôte. C'est généralement la forme
reçue par les serveurs, les proxies inverses et les proxies transparents.
```

- Un « URI absolu », également appelé « URL » :

```text
  http://192.168.0.12:8080/serv/login.php?lang=en&profile=2

Elle comprend un "scheme" (nom du protocole suivi de '://'), un nom ou
une adresse d'hôte, éventuellement deux-points (':') suivis d'un numéro
de port, puis une URI relative commençant à la première barre oblique
('/') après l'adresse. C'est généralement la forme reçue par les proxies,
mais un serveur prenant en charge HTTP/1.1 doit aussi l'accepter.
```

- étoile ('\*') : cette forme n'est acceptée que dans le cadre de la méthode OPTIONS et n'est pas relaisable. Elle est utilisée pour interroger les fonctionnalités d'un saut suivant.

- une combinaison adresse:port : 192.168.0.12:80. Cette option est utilisée avec la méthode CONNECT, qui permet d'établir des tunnels TCP à travers des proxies HTTP, généralement pour HTTPS, mais parfois aussi pour d'autres protocoles.

Dans une URI relative, deux sous-parties sont identifiées. La partie située avant le point d'interrogation est appelée le « chemin ». Elle correspond généralement au chemin relatif vers des objets statiques sur le serveur. La partie située après le point d'interrogation est appelée la « chaîne de requête ». Elle est principalement utilisée avec les requêtes GET envoyées à des scripts dynamiques et est très spécifique au langage, au framework ou à l'application utilisés.

HTTP/2 et HTTP/3 ne transmettent pas d'information de version avec la requête, la version est donc supposée être la même que celle du protocole sous-jacent (par exemple, « HTTP/2 »). En outre, ces protocoles n'envoient pas de ligne de requête comme une seule entité, mais la divisent en champs individuels appelés « pseudo-en-têtes », dont le nom commence par deux-points, et qui sont réassemblés de manière pratique par HAProxy en une ligne de requête équivalente. Pour cette raison, les lignes de requête présentes dans les journaux peuvent légèrement différer entre HTTP/1.x et HTTP/2 ou HTTP/3.

### 1.3.2. Les en-têtes de requête {#section-1-3-2}

Les en-têtes commencent à la deuxième ligne. Ils sont composés d'un nom au début de la ligne, immédiatement suivi d'un deux-points (':'). Traditionnellement, un LWS est ajouté après le deux-points, mais cela n'est pas obligatoire. Ensuite viennent les valeurs. Plusieurs en-têtes identiques peuvent être regroupés sur une seule ligne, les valeurs étant séparées par des virgules, à condition de respecter leur ordre. Cela est couramment observé dans le champ « Cookie: ». Un en-tête peut s'étendre sur plusieurs lignes si les lignes suivantes commencent par un LWS. Dans l'exemple de la section 1.3, les lignes 4 et 5 définissent au total trois valeurs pour l'en-tête « Accept: ». Enfin, tous les LWS situés au début ou à la fin d'un en-tête sont ignorés et ne font pas partie de la valeur, conformément à la spécification.

Contrairement à une idée reçue courante, les noms d’en-tête ne sont pas sensibles à la casse, ni leurs valeurs lorsqu’elles font référence à d’autres noms d’en-tête (comme l’en-tête « Connection: »). En HTTP/2 et HTTP/3, les noms d’en-tête sont toujours envoyés en minuscules, comme on peut le constater en mode débogage. Internalement, tous les noms d’en-tête sont normalisés en minuscules afin que HTTP/1.x, HTTP/2 et HTTP/3 utilisent exactement la même représentation, et ils sont transmis tel quel de l’autre côté. Cela explique pourquoi une requête HTTP/1.x saisie en casse camélisée est livrée en minuscules.

La fin des en-têtes est indiquée par la première ligne vide. On dit souvent qu’il s’agit d’un double saut de ligne, ce qui n’est pas exact, même si un double saut de ligne constitue une forme valide de ligne vide.

Heureusement, HAProxy gère toutes ces combinaisons complexes lors de l'indexation des en-têtes, de la vérification des valeurs et de leur comptage, si bien qu'il n'y a aucune raison de s'inquiéter quant à la manière dont ils peuvent être écrits, mais il est important de ne pas accuser une application de présenter un comportement défectueux si elle effectue des actions inhabituelles, mais valides.

Note importante :

```text
Comme le suggère RFC7231, HAProxy normalise les en-têtes en remplaçant
les sauts de ligne au milieu des en-têtes par LWS afin de réunir les
en-têtes sur plusieurs lignes. Cela est nécessaire à une analyse correcte
et aide les analyseurs HTTP moins performants à fonctionner correctement
sans être trompés par ces constructions complexes.
```

## 1.4. Réponse HTTP {#section-1-4}

Une réponse HTTP ressemble beaucoup à une requête HTTP. Ces éléments sont appelés des messages HTTP. Considérons la réponse suivante :

```text
Ligne    Contenu
numéro
   1     HTTP/1.1 200 OK
   2     Content-length: 350
   3     Content-Type: text/html
```

En tant que cas particulier, HTTP prend en charge ce qu’on appelle des « réponses informatives » sous forme de codes d’état 1xx. Ces messages sont spéciaux car ils ne transmettent aucune partie de la réponse ; ils servent uniquement de message de signalisation, par exemple pour demander au client de poursuivre l’envoi de sa requête. Dans le cas d’une réponse 100, les informations demandées seront transportées par le message de réponse suivant qui n’est pas un code 100. Cela implique qu’une même requête peut recevoir plusieurs réponses, et que cela ne fonctionne que lorsque le maintien de la connexion est activé (les messages 1xx ont été introduits dans HTTP/1.1). HAProxy gère ces messages et est capable de les acheminer correctement tout en les ignorant, en ne traitant que la prochaine réponse non 100. En conséquence, ces messages ne sont ni journalisés ni transformés, sauf indication contraire explicite. Les réponses 101 indiquent qu’un changement de protocole a lieu sur la même connexion, et que HAProxy doit passer en mode tunnel, comme si une requête CONNECT avait eu lieu. Dans ce cas, l’en-tête Upgrade contiendra des informations supplémentaires sur le type de protocole vers lequel la connexion effectue la bascule.

### 1.4.1. Ligne de réponse {#section-1-4-1}

Ligne 1 est la « ligne de réponse ». Elle est toujours composée de 3 champs :

- une balise de version : HTTP/1.1
- un code de statut : 200
- une raison : OK

Le code d’état est toujours composé de trois chiffres. Le premier chiffre indique un état général :

- 1xx = message d'information à ignorer (par exemple 100, 101)
- 2xx = OK, le contenu suit (par exemple 200, 206)
- 3xx = OK, aucun contenu ne suit (par exemple 302, 304)
- 4xx = erreur provoquée par le client (par exemple 401, 403, 404)
- 5xx = erreur provoquée par le serveur (par exemple 500, 502, 503)

Les codes d’état supérieurs à 599 ne doivent pas être émis dans les communications, bien que certains agents puissent les produire dans les journaux pour signaler leurs états internes. Veuillez vous référer à RFC9110 pour la signification détaillée de tous ces codes. HTTP/2 et les versions ultérieures ne comportent pas d’étiquette de version et utilisent le pseudo-en-tête « :status » pour rapporter le code d’état.

Le champ « reason » est simplement une indication, mais n'est pas analysé par les clients. Tout peut y être trouvé, mais il est courant de respecter les messages bien établis. Il peut être composé d’un ou plusieurs mots, tels que « OK », « Found » ou « Authentication Required ». Ce champ n’existe pas en HTTP/2 et versions ultérieures, et n’est pas émis dans ces versions. Lorsqu’une réponse provenant d’HTTP/2 ou d’une version ultérieure est transmise à un client HTTP/1, HAProxy produira un champ « reason » courant correspondant au code de statut.

HAProxy peut émettre les codes d’état suivants par lui-même :

```text
Code  Situation / raison
 200  accès à la page de statistiques et réponse aux requêtes de surveillance
 301  redirection, selon le code configuré
 302  redirection, selon le code configuré
 303  redirection, selon le code configuré
 307  redirection, selon le code configuré
 308  redirection, selon le code configuré
 400  requête invalide ou trop volumineuse
 401  authentification requise pour effectuer l'action (lors de l'accès
      à la page de statistiques)
 403  requête interdite par une règle "http-request deny"
 404  ressource demandée introuvable
 408  expiration du délai de requête avant que celle-ci soit complète
 410  ressource demandée indisponible et qui ne sera plus disponible
 413  requête GET/HEAD/DELETE HTTP/1.0 avec une charge utile ; voir aussi
      l'option "h1-accept-payload-with-any-method"
 500  erreur interne irrécupérable de HAProxy, telle qu'un échec d'allocation
      mémoire, qui ne devrait jamais se produire
 501  HAProxy ne peut satisfaire une requête client en raison d'une
      fonctionnalité non prise en charge
 502  réponse du serveur vide, invalide ou incomplète, ou réponse bloquée
      par une règle "http-response deny".
 503  aucun serveur disponible pour traiter la requête, ou réponse à une
      requête de surveillance correspondant à la condition "monitor fail"
 504  expiration du délai de réponse avant que le serveur réponde
```

Les codes d'erreur 4xx et 5xx ci-dessus peuvent être personnalisés (voir "errorloc" dans [section 4.2](/fr/docs/haproxy/proxies/#section-4-2)). D'autres codes d'état peuvent être émis intentionnellement par des actions spécifiques (voir les actions "deny", "return" et "redirect" dans [section 4.3](/fr/docs/haproxy/proxies/#section-4-3) par exemple).

### 1.4.2. Les en-têtes de réponse {#section-1-4-2}

Les en-têtes de réponse fonctionnent exactement comme les en-têtes de requête ; HAProxy utilise donc la même fonction pour les analyser. Reportez-vous au paragraphe 1.3.2 pour plus de détails.
