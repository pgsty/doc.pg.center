---
title: "11. Tables de persistance et pairs"
linkTitle: "11. Tables de persistance et pairs"
weight: 220
description: "Déclarations de stockage de table de persistance et de réplication entre pairs"
icon: fa-solid fa-table
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/stick-tables-and-peers/
  - /docs/haproxy/configuration/stick-tables-and-peers/
  - /haproxy/stick-tables-and-peers/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 11"
---

Les tables de persistance dans HAProxy sont un mécanisme qui permet d'associer un certain nombre d'informations et de métriques à une clé d'un type donné, pendant une durée déterminée après la dernière mise à jour. Cela peut être vu comme une ligne à plusieurs colonnes dans un tableau, où le numéro de ligne est défini par la valeur de la clé, et chaque colonne représente un critère distinct.

Les tables de persistance ont été initialement conçues pour stocker des informations de persistance client-serveur afin de maintenir des sessions persistantes entre ces entités. Un client se connecte ou envoie une requête ; ce client est identifié à l’aide d’un discriminateur (adresse source, cookie, paramètre d’URL) et le serveur sélectionné est stocké en association avec ce discriminateur dans une table de persistance pendant une durée configurable, de manière à ce que les accès ultérieurs provenant du même client soient automatiquement acheminés vers le même serveur, où le client a établi sa session d’application.

Aujourd'hui, les tables de persistance peuvent stocker davantage qu'un simple numéro de serveur : des métriques d'activité liées à un client spécifique peuvent être conservées (nombre de requêtes/taux, nombre de connexions/taux, nombre d'octets/taux, etc.), ainsi que certains compteurs d'événements arbitraires ("gpc" pour "Compteurs à usage général") et certaines étiquettes pour marquer un client selon certaines caractéristiques ("gpt" pour "Étiquettes à usage général").

Les tables de persistance peuvent être référencées par les directives « stick », utilisées pour la persistance client-serveur, par les règles « track-sc », utilisées pour préciser quelle clé suivre dans quelle table afin de collecter des métriques, ainsi que par plusieurs fonctions d'extraction et convertisseurs pouvant effectuer une recherche immédiate d'une clé donnée afin d'obtenir une métrique ou des données spécifiques. Le principe général est que les mises à jour des tables (gpt/gpc/métriques) ainsi que les recherches d'information de persistance rafraîchissent l'entrée accédée et reportent son expiration, tandis que les recherches effectuées uniquement par les fonctions d'extraction et les convertisseurs n'extraient que les données sans reporter l'expiration de l'entrée.

Afin que le mécanisme puisse évoluer et résister aux rechargements HAProxy et aux basculements, il est possible de partager les mises à jour des tables de persistance avec d'autres nœuds appelés « peers » via le mécanisme « Peers » décrit dans [section 11.2](/fr/docs/haproxy/stick-tables-and-peers/#section-11-2). Afin de paramétrer finement la communication avec les peers, il est également possible de décider qu’une table reçoive uniquement des informations provenant des peers, ou que les mises à jour provenant des peers soient au contraire acheminées vers une autre table.

Enfin, les tables de persistance peuvent être déclarées soit dans les sections proxy (frontals, backends) à l’aide du mot-clé « stick-table », où une seule table est autorisée par section et qui prendra le nom de cette section, soit dans les sections peers à l’aide du mot-clé « table » suivi du nom de la table, ce qui permet de déclarer plusieurs tables de persistance dans la même section « peers ». Si plusieurs tables de persistance sont nécessaires, la solution recommandée est généralement de les déclarer dans une section peers (si elles doivent être partagées), ou de créer des sections backend supplémentaires, chacune ne contenant qu’une directive « stick-table ».

## 11.1. déclaration stick-table {#section-11-1}

La déclaration d'une table de persistance dans une section proxy ("frontend", "backend", "listen") et dans des sections "peers" est très similaire, les différences étant que celle dans la section peers nécessite un nom obligatoire et ne prend pas d'option "peers".

Dans une section « frontend », « backend » ou « listen » :

stick-table type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only] [write-to
`<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`] [peers
`<peersect>`]

Dans une section « peers » :

table `<name>` type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only]
[write-to `<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`]

Arguments : (les obligatoires en premier, puis triés par ordre alphabétique) :

- type `<type>` Cet argument obligatoire définit le type de clé à `<type>`, qui est généralement un mot simple mais peut également avoir ses propres arguments :

  - ip Ce type doit être évité au profit d'une spécification plus explicite, telle que « ipv4 » ou « ipv6 ». Avant la version 3.2, c'était la seule manière de configurer IPv4. À partir de la version 3.2, « ip » est un alias de « ipv4 », qui est préféré. Dans une version future, « ip » correspondra à « ipv6 ». Il est destiné uniquement à faciliter la transition entre les versions antérieures à 3.2 et les versions postérieures à 3.2.

  - ipv4 Une table déclarée avec ce type ne stocke que des adresses IPv4. Ce format est très compact (environ 50 octets par entrée) et permet des recherches d'entrée et des opérations de stockage très rapides, avec un surcoût quasi nul. Il est principalement utilisé pour stocker les adresses IP sources des clients.

  - ipv6 Une table déclarée avec "type ipv6" ne stocke que des adresses IPv6. Cette forme est très compacte (environ 60 octets par entrée) et permet des recherches et des écritures d'entrées très rapides, avec un surcoût quasi nul. Elle est principalement utilisée pour stocker les adresses IP sources des clients.

  - integer Une table déclarée avec "type integer" stockera des entiers 32 bits pouvant représenter un identifiant client trouvé dans une requête, par exemple.

  - string [len `<len>`] Une table déclarée avec le type « string » stockera des sous-chaînes d'une longueur maximale de `<len>` caractères. Si la chaîne fournie par l'extracteur de motif est plus longue que `<len>`, elle sera tronquée avant d'être stockée. Lors de la correspondance, au plus `<len>` caractères seront comparés entre la chaîne dans la table et le motif extrait. Si cette valeur n'est pas spécifiée, la chaîne est automatiquement limitée à 32 caractères. Augmenter cette longueur peut avoir un impact non négligeable sur l'utilisation de la mémoire.

  - binary [len `<len>`] Une table déclarée avec "type binary" stockera des blocs binaires de `<len>` octets. Si le bloc fourni par l'extracteur de motif est plus grand que `<len>`, il sera tronqué avant d'être stocké. Si le bloc fourni par l'expression d'échantillonnage est plus court que `<len>`, il sera complété par des zéros. Par défaut, la taille du bloc est automatiquement limitée à 32 octets. Augmenter cette taille peut avoir un impact non négligeable sur la consommation mémoire.

- size `<size>` Cet argument obligatoire définit le nombre maximum d'entrées pouvant être stockées dans la table à `<size>`. Cette valeur influence directement l'utilisation de la mémoire. Comptez environ 50 octets par entrée, en plus de la taille de la clé, des métriques éventuellement stockées, ainsi que de la taille d'une chaîne si elle est présente. La taille supporte les suffixes « k », « m », « g » pour les facteurs 2^10, 2^20 et 2^30.

- expire `<delay>` Définit la durée maximale de validité d'une entrée dans la table depuis sa création, sa mise à jour avec 'track-sc' ou sa correspondance via une règle 'stick match' ou 'stick on'. Le délai d'expiration `<delay>` est défini selon le format temporel standard, de la même manière que les divers délais d'expiration, avec une valeur par défaut en millisecondes. La durée maximale est légèrement supérieure à 24 jours. Voir [section 2.5](/fr/docs/haproxy/configuration-basics/#section-2-5) pour plus d'informations. Si ce délai n'est pas spécifié, les sessions n'expirent pas automatiquement, mais les entrées les plus anciennes seront supprimées lors de la création une fois la table pleine. Veillez à ne pas utiliser le paramètre "nopurge" si aucun délai d'expiration n'est spécifié. Note : les convertisseurs 'table\_\*' effectuent des recherches mais ne mettent pas à jour le délai d'expiration car ils n'exigent pas 'track-sc'.

- brates-factor `<factor>` Spécifie un facteur à appliquer au débit d'octets entrants et sortants. Au lieu de compter chaque octet, des blocs d'octets sont comptés. En interne, les débits sont définis sur des compteurs 32 bits, limitant ceux-ci à environ 4 milliards par période. En utilisant ce paramètre, il devient possible de dépasser cette limite de 4G sur la période définie. Le facteur doit être supérieur à 0 et inférieur ou égal à 1024.

- nopurge indique que les entrées plus anciennes ne seront pas supprimées lorsque la table est pleine. Si ce paramètre n'est pas spécifié et que la table est pleine lorsque HAProxy souhaite y stocker une entrée, HAProxy supprimera quelques-unes des entrées les plus anciennes afin de libérer de l'espace pour les nouvelles. C'est généralement le comportement souhaité. Dans certains cas spécifiques, il peut être préférable de refuser les nouvelles entrées plutôt que de supprimer les anciennes. Cela peut être le cas lorsque la quantité de données à stocker dépasse largement les limites matérielles, et que l'on préfère ne pas offrir l'accès aux nouveaux clients plutôt que de rejeter ceux déjà connectés. Lorsque ce paramètre est utilisé, assurez-vous de définir correctement le paramètre « expire » (voir ci-dessus).

- recv-only indique que nous ne prévoyons pas d'utiliser la table pour effectuer des mises à jour, mais uniquement pour récupérer des données provenant d'un pair distant qui nous intéresse. En effet, l'utilisation de ce mot-clé permet de récupérer des valeurs uniquement locales telles que "conn_cur", qui ne sont pas apprises par défaut car elles entreraient en conflit avec les mises à jour locales effectuées sur la table par le pair local. Cette option n'est pertinente que pour les tables qui ne participent pas à des règles de suivi ou à des méthodes effectuant des opérations de mise à jour sur la table, ou, dit autrement : des tables distantes utilisées uniquement pour récupérer des informations.

- peers `<peersect>` Les entrées créées, mises à jour ou actualisées seront envoyées aux pairs dans la section `<peersect>` afin de synchroniser les données, et les clés apprises auprès des pairs de cette section seront également insérées ou mises à jour dans la table. En outre, au démarrage, une tentative peut être effectuée pour apprendre les entrées à partir d'une ancienne instance du processus, désignée comme le « pair local » via cette section.

- srvkey `<srvkey>` Spécifie la manière dont chaque serveur est identifié dans le cadre de la table de persistance. Les valeurs valides sont « name » et « addr ». Si « name » est indiqué, alors l'argument `<name>` du serveur (peut être généré par un modèle). Si « addr » est indiqué, alors le serveur est identifié par son adresse réseau actuelle, y compris le port. « addr » est particulièrement utile lorsque vous utilisez la découverte de services pour générer les adresses des serveurs avec des tables de persistance jumelées, et que vous souhaitez utiliser de manière cohérente le même hôte pour un jeton de persistance à travers les pairs.

- store `<data_type>` Cette directive permet de stocker des informations supplémentaires dans la table de persistance. Elle peut être utilisée par les ACL afin de contrôler divers critères liés à l'activité du client correspondant à la table de persistance. Pour chaque élément spécifié ici, la taille de chaque entrée sera augmentée afin de permettre l'ajout des données supplémentaires. Plusieurs types de données peuvent être stockés avec une même entrée. Plusieurs types de données peuvent être indiqués après le mot-clé « store », sous forme d'une liste séparée par des virgules. Alternativement, il est également possible de répéter le mot-clé « store » suivi d'un ou plusieurs types de données. À l'exception du type "server_id", qui est détecté et activé automatiquement, tous les types de données doivent être explicitement déclarés comme étant stockés. Si une ACL référence un type de données non stocké, l'ACL ne correspondra pas. Certains types de données nécessitent un argument, qui doit être fourni immédiatement après le type, entre parenthèses. Voir ci-dessous la liste des types de données pris en charge ainsi que leurs arguments.

- write-to `<wtable>` Spécifie le nom d'une autre table de persistance où les mises à jour des pairs seront écrites en plus de la table source. `<wtable>` doit être du même type que la table définie et avoir la même longueur de clé, et la table source ne peut pas être utilisée elle-même comme table cible. Chaque fois qu'une mise à jour d'entrée sera reçue sur la table source via un pair, HAProxy tentera de rafraîchir l'entrée correspondante dans `<wtable>`. Si l'entrée n'existe pas encore, elle sera créée ; sinon, ses valeurs seront mises à jour ainsi que son minuteur. Notez que seuls les types n'impliqués dans aucune opération arithmétique, tels que server_id, server_key et gpt, seront écrits dans `<wtable>` afin d'éviter que les valeurs traitées provenant d'une table distante n'interfèrent avec les opérations arithmétiques effectuées sur la table cible locale. (Par exemple : empêcher un compteur cumulatif partagé de croître indéfiniment.) Un usage courant de cette option consiste à pouvoir utiliser des règles de persistance (pour la persistance des serveurs) dans une configuration de cluster de pairs, car les clés correspondantes seront apprises à partir des tables distantes.

Les types de données pouvant être associés à une entrée via la directive « store » sont indiqués ci-dessous. Il est important de garder à l’esprit que les besoins en mémoire peuvent être significatifs lors du stockage de nombreux types de données. En effet, le stockage de tous les indicateurs ci-dessous en même temps dans chaque entrée peut nécessiter des centaines d’octets par entrée, ou des centaines de mégaoctets pour une table de 1 million d’entrées. Pour cette raison, la taille de stockage approximative est indiquée ci-dessous pour chaque type, entre parenthèses, après l’argument.

Arguments :

- bytes_in_cnt [8 octets] Il s'agit du décompte des octets envoyés par le client vers le serveur. Il s'agit d'un entier 64 bits positif qui compte le nombre cumulé d'octets reçus des clients correspondant à cette entrée. Les en-têtes sont inclus dans le décompte. Ce compteur peut être utilisé pour limiter l'abus des fonctionnalités de téléchargement sur des serveurs photo ou vidéo. Notez que les valeurs sont mesurées au moment où les données entrent dans HAProxy, les comptes ne sont donc pas affectés par la compression.

- bytes_in_rate(`<period>`) [12 octets] Ce compteur de débit indique le débit en octets provenant du client vers le serveur. Il prend un paramètre entier `<period>` qui indique, en millisecondes, la durée de la période sur laquelle la moyenne est calculée. Il rapporte le débit moyen d'octets entrants sur cette période, en octets par période. Il peut être utilisé pour détecter les utilisateurs qui téléchargent trop et trop rapidement.
    Avertissement : lors de transferts importants, il est possible que la quantité de données téléchargées soit comptabilisée une seule fois à la fin, ce qui peut provoquer des pics dans la vitesse moyenne de transfert au lieu d'une courbe lisse. Ce phénomène peut être partiellement atténué avec l'option contstats, bien que cela ne soit pas parfait. Il est recommandé d'utiliser byte_in_cnt pour une meilleure équité.

- bytes_out_cnt [8 octets] Il s'agit du décompte des octets envoyés par le serveur vers le client. Il s'agit d'un entier 64 bits positif qui compte le nombre cumulé d'octets envoyés aux clients correspondant à cette entrée. Les en-têtes sont inclus dans le décompte. Ce compteur peut être utilisé pour limiter l'abus par des bots consommant l'intégralité du site. Notez que les valeurs sont mesurées au moment où les données entrent dans HAProxy, les comptes ne sont donc pas affectés par la compression.

- bytes_out_rate(`<period>`) [12 octets] Ce compteur de taux indique le débit en octets envoyés par le serveur vers le client. Il prend un paramètre entier `<period>` qui indique, en millisecondes, la durée de la période sur laquelle la moyenne est calculée. Il signale le débit moyen d'octets sortants sur cette période, en octets par période. Il peut être utilisé pour détecter les utilisateurs qui téléchargeent trop et trop rapidement.
    Avertissement : lors de transferts importants, il est possible que la quantité de données transférées soit comptabilisée une seule fois à la fin, ce qui peut provoquer des pics dans la vitesse moyenne de transfert au lieu d'une courbe lisse. Ce phénomène peut être partiellement atténué avec l'option contstats, bien que cela ne soit pas encore parfait. Il est recommandé d'utiliser byte_out_cnt pour une meilleure équité.

- conn_cnt [4 octets] Il s'agit du nombre de connexions. Il s'agit d'un entier signé 32 bits positif qui compte le nombre absolu de connexions reçues des clients correspondant à cette entrée. Cela ne signifie pas que les connexions ont été acceptées, mais simplement qu'elles ont été reçues.

- conn_cur [4 octets] Il s'agit du compteur de connexions actuelles. Il s'agit d'un entier signé 32 bits positif qui stocke le nombre de connexions simultanées pour l'entrée. Ce compteur est incrémenté une fois qu'une connexion entrante correspond à l'entrée, et décrémenté une fois que la connexion se termine. Ainsi, il est possible de connaître à tout moment le nombre exact de connexions simultanées pour une entrée. Ce type n'est pas par défaut appris à partir d'autres pairs, car cela ne représenterait rien étant donné qu'il ignorerait le compteur local. Toutefois, combiné à recv-only, il peut être utilisé pour apprendre le nombre de connexions simultanées observées par les pairs.

- conn_rate(`<period>`) [12 octets] Ce compteur mesure la fréquence des connexions. Il prend un paramètre entier `<period>`, qui indique en millisecondes la durée de la période sur laquelle la moyenne est calculée. Il rapporte le débit moyen de connexions entrantes sur cette période, en connexions par période. Le résultat est un entier pouvant être utilisé dans des listes de contrôle d'accès (ACL). Le fait qu'une connexion soit acceptée ou rejetée n'affecte pas sa mesure.

- glitch_cnt [4 octets] Il s'agit du nombre de glitchs côté front. Il s'agit d'un entier signé 32 bits positif qui compte le nombre cumulé de glitchs signalés sur une connexion frontale. Les glitchs correspondent à des actions inhabituelles ou inattendues (au niveau du protocole) provenant du client, pouvant indiquer un client défectueux ou éventuellement un attaquant. Ce compteur peut donc aider à déterminer la manière d'agir en cas de telles situations.

- glitch_rate(`<period>`) [12 octets] Ce compteur de fréquence mesure les anomalies. Il prend un paramètre entier `<period>` qui indique, en millisecondes, la durée de la période sur laquelle la moyenne est calculée. Il signale le taux moyen d'anomalies frontales sur cette période. Il peut être utilisé pour détecter des clients défectueux ou des attaquants potentiels effectuant des actions inhabituelles ou inattendues du point de vue du protocole, à condition qu’HAProxy les ait identifiés comme tels.

- gpc(`<nb>`) [4 \* `<nb>` octets] Il s'agit d'un tableau d'éléments de compteur généralisé `<nb>`.
    Il s'agit d'un tableau d'entiers positifs 32 bits pouvant être utilisés pour compter n'importe quoi. En général, ils seront utilisés comme compteurs incrémentaux sur certaines entrées, par exemple pour indiquer qu'une limite est atteinte et déclencher certaines actions. Ce tableau est limité à un maximum de 100 éléments : gpc0 à gpc99, afin de garantir que la construction d'un message de mise à jour de pair puisse tenir dans le tampon. Les utilisateurs doivent tenir compte du fait qu'un grand nombre de compteurs augmente la taille des données et la charge du trafic lors de l'utilisation du protocole pair, car toutes les données/compteurs sont transmises à chaque mise à jour d'un de ces éléments. Ce type de données exclut l'utilisation des types de données hérités « gpc0 » et « gpc1 » sur la même table. Lorsqu'on utilise le type de données tableau « gpc », toutes les fonctions d'extraction d'échantillon et les actions liées à « gpc0 » et « gpc1 » s'appliquent aux deux premiers éléments de ce tableau.

- gpc_rate(`<nb>`,`<period>`) [12 \* `<nb>` octets] Il s'agit d'un tableau de taux d'incrémentation des compteurs généraux sur une période. Ces éléments sont des entiers 32 bits positifs pouvant être utilisés pour n'importe quelle finalité. Tout comme `<gpc>`, ils comptabilisent les événements, mais au lieu de conserver un nombre cumulé, ils maintiennent le taux auquel le compteur est incrémenté. En général, il est utilisé pour mesurer la fréquence d'apparition d'événements spécifiques (par exemple, les requêtes vers une URL spécifique). Ce tableau est limité à un maximum de 100 éléments : gpc_rate(100,`<period>`), permettant le stockage de gpc0 à gpc99, afin de garantir que la construction d'un message de mise à jour de pair puisse tenir dans le tampon. Le tableau ne peut pas contenir moins d'un élément : utilisez gpc_rate(1,`<period>`) si vous souhaitez stocker uniquement le compteur gpc0. Les utilisateurs doivent prendre en compte qu'un grand nombre de compteurs augmente la taille des données et la charge du trafic lors de l'utilisation du protocole pair, car toutes les données/compteurs sont transmises à chaque mise à jour d'un de ces éléments. Ce type de données exclut l'utilisation des anciens types de données 'gpc0_rate' et 'gpc1_rate' sur la même table. En utilisant le type de données 'gpc_rate' tableau, toutes les fonctions d'extraction et les actions liées à 'gpc0' et 'gpc1' s'appliquent aux deux premiers éléments de ce tableau.

- gpc0 [4 octets] Il s'agit du premier compteur général. Il s'agit d'un entier positif sur 32 bits pouvant être utilisé pour toute finalité. En général, il sera utilisé pour ajouter une étiquette particulière à certaines entrées, par exemple pour indiquer qu'un comportement spécifique a été détecté et doit être pris en compte pour les correspondances ultérieures.

- gpc0_rate(`<period>`) [12 octets] Ce paramètre correspond au taux d'incrémentation du premier compteur généralisé sur une période. Il s'agit d'un entier positif sur 32 bits pouvant être utilisé à n'importe quelle fin. Tout comme `<gpc0>`, il compte les événements, mais au lieu de maintenir un total cumulé, il conserve le taux auquel le compteur est incrémenté. Il est généralement utilisé pour mesurer la fréquence d'apparition d'événements spécifiques (par exemple, les requêtes adressées à une URL précise).

- gpc1 [4 octets] Il s'agit du deuxième compteur généralisé. Il s'agit d'un entier positif sur 32 bits pouvant être utilisé pour toute finalité. En général, il sera utilisé pour ajouter une étiquette particulière à certaines entrées, par exemple pour indiquer qu'un comportement spécifique a été détecté et doit être pris en compte pour des correspondances ultérieures.

- gpc1_rate(`<period>`) [12 octets] Ce paramètre correspond au taux d'incrémentation du deuxième Compteur généralisé sur une période donnée. Il s'agit d'un entier positif sur 32 bits pouvant être utilisé à n'importe quelle fin. Tout comme `<gpc1>`, il compte les événements, mais au lieu de maintenir un total cumulé, il conserve le taux auquel le compteur est incrémenté. Il est généralement utilisé pour mesurer la fréquence d'apparition d'événements spécifiques (par exemple, les requêtes adressées à une URL précise).

- gpt(`<nb>`) [4 \* `<nb>` octets] Il s'agit d'un tableau de `<nb>` éléments de balises générales. Il s'agit d'un tableau d'entiers 32 bits positifs pouvant être utilisés à n'importe quelle fin. En général, ces balises servent à marquer certaines entrées, par exemple pour indiquer qu'un comportement spécifique a été détecté et doit être pris en compte lors de correspondances ultérieures. Ce tableau est limité à un maximum de 100 éléments : gpt(100), permettant de stocker les balises gpt0 à gpt99, afin de garantir que la construction d'un message de mise à jour pair puisse tenir dans le tampon. Le tableau ne peut contenir moins d'un élément : utilisez gpt(1) si vous souhaitez stocker uniquement la balise gpt0. Les utilisateurs doivent tenir compte du fait qu'un grand nombre de compteurs augmentera la taille des données et la charge du trafic lors de l'utilisation du protocole pair, car toutes les données/compteurs sont transmises à chaque mise à jour d'un de ces éléments. Ce type de données exclut l'utilisation du type de données hérité « gpt0 » dans la même table. Lorsque le type de données « gpt » est utilisé, toutes les fonctions d'extraction et les actions liées à « gpt0 » s'appliquent au premier élément de ce tableau.

- gpt0 [4 octets] Il s'agit de la première balise générale. Il s'agit d'un entier signé 32 bits positif qui peut être utilisé pour n'importe quelle finalité. En règle générale, il sera utilisé pour ajouter une balise particulière à certaines entrées, par exemple pour indiquer qu'un comportement spécifique a été détecté et doit être pris en compte pour les correspondances futures.

- http_req_cnt [4 octets] Ce champ représente le nombre de requêtes HTTP. Il s'agit d'un entier signé 32 bits positif qui compte le nombre absolu de requêtes HTTP reçues depuis les clients correspondant à cette entrée. Il n'est pas tenu compte de la validité de ces requêtes. Notez que cette valeur diffère du nombre de sessions lorsque la fonctionnalité keep-alive est utilisée côté client.

- http_req_rate(`<period>`) [12 octets] Ce compteur mesure la fréquence des requêtes. Il prend un paramètre entier `<period>` qui indique, en millisecondes, la durée de la période sur laquelle la moyenne est calculée. Il rapporte le débit moyen de requêtes HTTP sur cette période, en requêtes par période. Le résultat est un entier pouvant être utilisé dans des ACLs. Il n'est pas pertinent qu'il s'agisse de requêtes valides ou non. Notez que cela diffère des sessions lorsque le maintien de connexion (keep-alive) est utilisé côté client.

- http_err_cnt [4 octets] Ce champ représente le nombre d'erreurs de requête HTTP. Il s'agit d'un entier signé 32 bits positif qui compte le nombre absolu d'erreurs de requêtes HTTP provoquées par des clients correspondant à cette entrée. Les erreurs sont comptabilisées pour les requêtes non valides ou tronquées, ainsi que pour les requêtes refusées ou tarpittées, et pour les échecs d'authentification. Si le serveur répond par un code 4xx, la requête est également comptabilisée comme erreur, car elle est déclenchée par le client (par exemple, une analyse de vulnérabilité).

- http_err_rate(`<period>`) [12 octets] Compteur de fréquence des requêtes HTTP. Prend en paramètre un entier `<period>` indiquant, en millisecondes, la durée de la période sur laquelle la moyenne est calculée. Rapporte le taux moyen d'erreurs de requêtes HTTP sur cette période, en requêtes par période (voir http_err_cnt ci-dessus pour la définition des erreurs comptabilisées). Le résultat est un entier pouvant être utilisé dans des ACLs.

- http_fail_cnt [4 octets] Il s'agit du nombre d'échecs de réponse HTTP. Il s'agit d'un entier signé 32 bits positif qui compte le nombre absolu d'échecs de réponse HTTP provoqués par les serveurs correspondant à cette entrée. Les erreurs sont comptabilisées pour les réponses invalides ou tronquées, ainsi que pour toute réponse 5xx autre que 501 ou 505. Il est destiné à être utilisé en combinaison avec le chemin ou l'URI afin de détecter les pannes de service.

- http_fail_rate(`<period>`) [12 octets] Ce compteur mesure la fréquence des échecs de réponse HTTP.
    Il prend un paramètre entier `<period>` qui indique, en millisecondes, la durée de la période sur laquelle la moyenne est calculée.
    Il rapporte le taux moyen d'échecs de réponse HTTP sur cette période, en requêtes par période (voir http_fail_cnt ci-dessus pour la définition d'un échec).
    Le résultat est un entier pouvant être utilisé dans les ACLs.

- server_id [4 octets] Il s'agit d'un entier qui contient l'identifiant numérique du serveur vers lequel une requête a été affectée. Il est utilisé par les règles "stick match", "stick store" et "stick on". Il est activé automatiquement lorsqu'il est référencé. Il est important de comprendre que la persistance basée sur les informations apprises présente certaines limitations, notamment le fait que toutes les associations apprises sont perdues lors d'un redémarrage, sauf si les pairs sont correctement configurés pour transférer ces informations lors du redémarrage (recommandé). En général, elle peut être utile en complément d'autres mécanismes de persistance, mais pas toujours en tant que mécanisme unique.

- sess_cnt [4 octets] Il s'agit du nombre de sessions. Il s'agit d'un entier signé 32 bits positif qui compte le nombre absolu de sessions reçues depuis les clients correspondant à cette entrée. Une session correspond à une connexion acceptée par les règles du niveau 4 ("tcp-request connection").

- sess_rate(`<period>`) [12 octets] Ce compteur mesure la fréquence des sessions. Il prend un paramètre entier `<period>`, qui indique en millisecondes la durée de la période sur laquelle la moyenne est calculée. Il rapporte le débit moyen des sessions entrantes sur cette période, en sessions par période. Le résultat est un entier pouvant être utilisé dans des listes ACL.

Exemple :

```shell
# Keep track of counters of up to 1 million IP addresses over 5 minutes
# and store a general purpose counter and the average connection rate
# computed over a sliding window of 30 seconds.
stick-table type ip size 1m expire 5m store gpc0,conn_rate(30s)
```

Voir aussi : « stick match », « stick on », « stick store-request », « track-sc », [section 2.5](/fr/docs/haproxy/configuration-basics/#section-2-5) sur le format temporel, [section 11.2](/fr/docs/haproxy/stick-tables-and-peers/#section-11-2) sur les pairs, [section 9.7](/fr/docs/haproxy/filters/#section-9-7) sur les limitations de bande passante, et [section 7](/fr/docs/haproxy/acls-and-samples/) sur les listes de contrôle d'accès.

## 11.2. Déclaration Peers {#section-11-2}

Il est possible de propager des entrées de tout type de données dans les tables de persistance entre plusieurs instances HAProxy via des connexions TCP, selon une architecture multi-maître. Chaque instance transmet ses mises à jour et insertions locales aux pairs distants. Les valeurs transmises écrasent celles présentes à distance sans agrégation.

Une exception concerne le type de données "conn_cur", qui n'est jamais appris auprès des pairs par défaut, car il doit refléter les valeurs locales. Les versions antérieures le synchronisaient par défaut, ce qui était susceptible de provoquer des valeurs négatives dans les configurations actif-actif, ainsi que des valeurs toujours croissantes lors des rechargements ou des basculements actif-passif, car la valeur locale reflétait un nombre de connexions supérieur à celui des connexions locales réelles. Toutefois, certaines configurations peuvent justifier l'apprentissage de cette valeur auprès des pairs, par exemple lorsque la table est une table distante passive utilisée uniquement pour apprendre ou surveiller les données sans en dépendre pour les opérations d'écriture ou les mises à jour. Pour cela, le mot-clé « recv-only » peut être ajouté à la déclaration de la table. Dans tous les cas, les informations "conn_cur" sont toujours transmises afin que les systèmes de surveillance puissent les suivre.

Les échanges interrompus sont automatiquement détectés et récupérés à partir du dernier point connu. En outre, lors d’un redémarrage doux, le processus ancien se connecte au nouveau à l’aide d’une telle connexion TCP pour transmettre toutes ses entrées avant que le nouveau processus ne tente de se connecter aux autres pairs. Cela garantit une réplication très rapide lors d’un rechargement, qui prend généralement une fraction de seconde, même pour de grandes tables.

Notez que les identifiants de serveur sont utilisés pour identifier les serveurs à distance, il est donc important que les configurations soient similaires, ou du moins que les mêmes identifiants soient imposés sur chaque serveur pour tous les participants.

<a id="entry-11-2-peers"></a>

**`peers <peersect>`**

```haproxy
peers <peersect>
```

Crée une nouvelle liste de pairs nommée `<peersect>`. Il s'agit d'une section indépendante, référencée par une ou plusieurs tables de persistance.

<a id="entry-11-2-bind"></a>

**`bind [<address>]:port [param*]`**

```haproxy
bind [<address>]:port [param*]
bind /<path> [param*]
```

Définit les paramètres de liaison du pair local de cette section « peers ». Ces lignes ne sont pas prises en charge avec une ligne « peer » dans la même section « peers ».

<a id="entry-11-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Désactive une section peers. Elle désactive à la fois l'écoute et toute synchronisation liée à cette section. Cette option permet de désactiver la synchronisation des tables de persistance sans devoir commenter toutes les références à "peers".

<a id="entry-11-2-default-bind"></a>

**`default-bind [param*]`**

```haproxy
default-bind [param*]
```

Définit les paramètres de liaison pour le pair local, à l'exception de son adresse.

<a id="entry-11-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Modifie les options par défaut pour un serveur dans une section « peers ».

Arguments :

```text
<param*>  est une liste de paramètres pour ce serveur. Le mot-clé
          "default-server" accepte de nombreuses options et dispose d'une
          section complète. Dans une section peers, les paramètres de
          transport d'une ligne "default-server" sont pris en charge.
          Consultez la section 5 pour plus de détails et le mot-clé "server"
          ci-dessous pour certaines restrictions.
```

Voir également : « server » et [section 5](/fr/docs/haproxy/bind-and-server-options/) concernant les options du serveur

<a id="entry-11-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Cela réactive une section peers qui était précédemment désactivée via le mot-clé « disabled ».

<a id="entry-11-2-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

Les sections « peers » prennent en charge le mot-clé « log » identique à celui des proxies pour journaliser des informations concernant l'écouteur « peers ». Voir l'option « log » des proxies pour plus de détails.

<a id="entry-11-2-peer"></a>

**`peer <peername> [<address>]:port [param*]`**

```haproxy
peer <peername> [<address>]:port [param*]
peer <peername> /<path> [param*]
```

Définit un pair au sein d'une section peers. Si `<peername>` est défini sur le nom du pair local (par défaut, hostname, ou forcé à l'aide de l'option en ligne de commande "-L" ou de l'option de configuration globale localpeer), HAProxy écoutera les connexions entrantes du pair distant sur l'adresse fournie. Sinon, l'adresse définit l'emplacement vers lequel se connecter pour rejoindre le pair distant, et `<peername>` est utilisé au niveau du protocole pour identifier et valider le pair distant côté serveur.

Lors d'un redémarrage doux, l'adresse locale du pair est utilisée par l'instance ancienne pour se connecter à la nouvelle et initier une réplication complète (processus d'enseignement).

Il est fortement recommandé d'avoir une déclaration de pairs identique sur tous les pairs et de ne s'appuyer que sur l'argument en ligne de commande "-L" ou sur le paramètre de configuration globale "localpeer" pour modifier le nom du pair local. Cela facilite la maintenance de fichiers de configuration cohérents sur l'ensemble des pairs.

Vous pouvez souhaiter référencer certaines variables d'environnement dans le paramètre d'adresse, voir [section 2.3](/fr/docs/haproxy/configuration-basics/#section-2-3) concernant les variables d'environnement.

Note : le mot-clé « peer » peut être remplacé de manière transparente par le mot-clé « server » (voir l'explication du mot-clé « server » ci-dessous).

<a id="entry-11-2-server"></a>

**`server <peername> [<address>:<port>] [param*]`**

```haproxy
server <peername> [<address>:<port>] [param*]
server <peername> [/<path>] [param*]
```

Comme mentionné précédemment, le mot-clé « peer » peut être remplacé par le mot-clé « server », avec prise en charge de tous les paramètres « server » décrits au paragraphe 5.2 qui concernent les paramètres de transport. Si le pair sous-jacent est local, le paramètre address ne doit pas être présent ; il doit être fourni sur une ligne « bind » (voir le mot-clé « bind » de cette section « peers »).

Un certain nombre de paramètres « server » sont sans effet dans les sections « peers ». Par nature, les pairs ne prennent pas en charge la résolution dynamique des noms d'hôte ni les contrôles d'état, aussi les paramètres tels que "init_addr", « resolvers », « check », « agent-check » ou « track » ne sont pas pris en charge. De même, il n'y a ni répartition de charge ni persistance de session, les paramètres comme « weight » ou « cookie » n'ont donc aucun effet.

Exemple :

```text
 # The old way.
 peers mypeers
     peer haproxy1 192.168.0.1:1024
     peer haproxy2 192.168.0.2:1024
     peer haproxy3 10.2.0.1:1024

 backend mybackend
     mode tcp
     balance roundrobin
     stick-table type ip size 20k peers mypeers
     stick on src

     server srv1 192.168.0.30:80
     server srv2 192.168.0.31:80

Exemple :
  peers mypeers
     bind 192.168.0.1:1024 ssl crt mycerts/pem
     default-server ssl verify none
     server haproxy1 #local peer
     server haproxy2 192.168.0.2:1024
     server haproxy3 10.2.0.1:1024
```

shards `<shards>`

Dans certaines configurations, on souhaite distribuer le contenu de la table de persistance à certains pairs au lieu d'envoyer l'intégralité du contenu de la table à chaque pair déclaré dans la section « peers ». Dans de tels cas, le paramètre « shards » indique le nombre de pairs impliqués dans cette distribution du contenu de la table de persistance. Voir également le paramètre serveur « shard ».

<a id="entry-11-2-table"></a>

**`table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}`**

```haproxy
table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}
```

      size `<size>` [expire `<expire>`] [write-to `<wtable>`] [nopurge] [store `<data_type>`]*
      [recv-only]

Configurez une table de persistance pour la section courante. Cette ligne est analysée exactement de la même manière que le mot-clé « stick-table » dans les autres sections, à l’exception de l’argument « peers » qui n’est pas requis ici et de l’ajout d’un paramètre obligatoire en premier lieu pour désigner la table de persistance. Contrairement aux autres sections, plusieurs lignes « table » peuvent exister dans les sections « peers » (voir également la définition complète des mots-clés « table » et « stick-table » dans la section [11.1](/fr/docs/haproxy/stick-tables-and-peers/#section-11-1) ci-dessus).

Attention également au fait que les sections « peers » disposent d'un espace de noms propre pour les tables de persistance afin d'éviter les conflits entre des noms de tables identiques dans différentes sections « peers ». Ce mécanisme est géré internement en préfixant le nom des tables de persistance par le nom de la section « peers », suivi d'un caractère « / ». Si, ailleurs dans le fichier de configuration, vous devez faire référence à une table de persistance déclarée dans une section « peers », vous devez utiliser la version préfixée du nom de la table, comme suit :

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 ...

frontend fe1
    tcp-request content track-sc0 src table mypeers/t1
```

Il s'agit également de la version préfixée des noms de tables de persistance, qui doit être utilisée pour faire référence aux tables de persistance via l'interface en ligne de commande.

À propos du protocole « peers », comme seuls les « peers » appartenant à la même section peuvent communiquer entre eux, il n’est pas nécessaire de faire cette distinction. Plusieurs sections « peers » peuvent déclarer des tables de persistance avec le même nom. Il s’agit d'une version raccourcie du nom de la table de persistance transmise sur le réseau. Un seul caractère « / » est utilisé comme préfixe afin d’éviter les conflits de noms entre les tables de persistance déclarées en tant que backends et les tables de persistance déclarées dans les sections « peers », comme illustré dans cette configuration étrange mais prise en charge :

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 type string size 10m store gpc0

backend t1
    stick-table type string size 10m store gpc0 peers mypeers
```

Ici, la table « t1 » déclarée dans la section « mypeers » a pour nom global « mypeers/t1 ». La table « t1 » déclarée en tant que backend porte également le nom global « t1 ». Toutefois, au niveau du protocole pair, la première table est nommée « /t1 », la seconde est à nouveau nommée « t1 ».
