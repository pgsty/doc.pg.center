---
title: "Questions fréquemment posées"
linkTitle: "FAQ"
weight: 90
description: "Questions fréquentes sur PgBouncer"
icon: fa-solid fa-circle-question
module: [PGBOUNCER]
categories: [Référence]
aliases: [/pgbouncer/faq/]
upstream_link: "https://www.pgbouncer.org/faq.html"
---

--------

## Comment se connecter à PgBouncer ? {#how-to-connect-to-pgbouncer}

PgBouncer agit comme un serveur Postgres, il suffit donc de configurer votre client pour qu’il se connecte au port de PgBouncer.

--------

## Comment équilibrer la charge des requêtes entre plusieurs serveurs ? {#how-to-load-balance-queries-between-several-servers}

PgBouncer ne dispose pas de configuration interne multi-hôtes.
Il est possible via des outils externes :

1. Round-robin DNS. Utilisez plusieurs adresses IP derrière un même nom DNS. PgBouncer ne résout pas le DNS à chaque nouvelle connexion. Il met en cache toutes les adresses IP et effectue le round-robin de manière interne. Note : si plus de 8 adresses IP sont associées à un même nom, le serveur DNS backend doit prendre en charge le protocole EDNS0. Voir le fichier README pour plus de détails.

2. Utilisez un équilibreur de charge de connexion TCP. Soit
    [LVS](http://www.linuxvirtualserver.org/) ou
    [HAProxy](https://www.haproxy.org/) semble être un choix pertinent. Du côté de PgBouncer, il peut être judicieux de réduire `server_lifetime`
    et d’activer `server_round_robin` : par défaut, les connexions inactives sont réutilisées selon un algorithme LIFO, ce qui peut fonctionner moins bien lorsqu’un équilibrage de charge est requis.

--------

## Comment effectuer un basculement {#how-to-failover}

PgBouncer ne dispose pas de configuration interne ni de détection de basculement automatique.
Il est possible d'utiliser des outils externes :

1. Réconfiguration DNS : lorsque l'adresse IP derrière un nom DNS est modifiée, PgBouncer se reconnecte au nouveau serveur. Ce comportement peut être ajusté à l'aide de deux paramètres de configuration :
   `dns_max_ttl` détermine la durée de vie d'un nom d'hôte, et
   `dns_zone_check_period` détermine la fréquence à laquelle une zone SOA sera interrogée pour détecter des modifications. Si un enregistrement SOA de zone a changé, PgBouncer interroge à nouveau tous les noms d'hôte de cette zone.

2. Écrivez un nouvel hôte dans la configuration et laissez PgBouncer la recharger :
envoyez le signal SIGHUP ou utilisez la commande `RELOAD` sur la console. PgBouncer détectera une modification de la configuration d'hôte et se reconnectera au nouveau serveur.

3. Utilisez la commande `RECONNECT`. Cette commande est destinée aux situations où aucune des deux options précédentes n'est applicable, par exemple lorsque vous utilisez HAProxy, tel que mentionné, pour acheminer les connexions vers le bas depuis PgBouncer. `RECONNECT` provoque simplement la réouverture de toutes les connexions vers les serveurs. Exécutez-la après que l'autre composant a modifié ses informations de routage des connexions.

--------

## Comment utiliser les requêtes préparées avec le pooling de sessions ? {#how-to-use-prepared-statements-with-session-pooling}

En mode pooling de sessions, la requête de réinitialisation doit supprimer les instructions préparées anciennes. Cela peut être réalisé en `server_reset_query = DISCARD ALL;` ou, au minimum, en `DEALLOCATE ALL;`

--------

## Comment utiliser les requêtes préparées avec le pooling de transactions ? {#how-to-use-prepared-statements-with-transaction-pooling}

Depuis la version 1.21.0, PgBouncer peut suivre les requêtes préparées en mode pool de transaction et s'assurer qu'elles sont préparées en temps réel sur la connexion serveur liée. Pour activer cette fonctionnalité, `max_prepared_statements` doit être défini à une valeur non nulle. Pour plus de détails, consultez la [documentation de `max_prepared_statements`](/fr/docs/pgbouncer/config/#max_prepared_statements).

Si vous utilisez PHP/PDO, selon sa version, il se peut qu'il soit incompatible avec la prise en charge des requêtes préparées de PgBouncer ([#991]). PHP/PDO est uniquement compatible lorsque [PHP 8.4+ **et** libpq 17][php-fix] sont utilisés. Pour les configurations avec des versions plus anciennes, il est recommandé de procéder à une mise à jour, ou de désactiver les requêtes préparées côté client.

[php-fix]: https://github.com/php/php-src/commit/f35ad560b468e3e0a6c289949ba9b19af4fa3e7b

[#991]: https://github.com/pgbouncer/pgbouncer/issues/991

### Désactivation des requêtes préparées dans JDBC {#disabling-prepared-statements-in-jdbc}

La manière correcte de procéder pour JDBC consiste à ajouter le paramètre `prepareThreshold=0` à la chaîne de connexion.

### Désactivation des requêtes préparées dans PHP/PDO {#disabling-prepared-statements-in-phppdo}

Pour désactiver l'utilisation des requêtes préparées côté serveur, l'attribut PDO `PDO::ATTR_EMULATE_PREPARES` doit être défini à `true`. Cela peut être fait au moment de la connexion :

    $db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));

ou ultérieurement :

    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);

--------

## Comment mettre à jour PgBouncer sans interrompre les connexions ? {#how-to-upgrade-pgbouncer-without-dropping-connections}

Vous pouvez effectuer un redémarrage progressif en suivant la procédure décrite dans la [section des documents pour `SHUTDOWN WAIT_FOR_CLIENTS`](/fr/docs/pgbouncer/usage/#shutdown-wait_for_clients)

--------

## Comment savoir quel client est connecté à quelle connexion serveur ? {#how-to-know-which-client-is-on-which-server-connection}

Utilisez les commandes `SHOW CLIENTS` et `SHOW SERVERS` depuis la console d'administration.

1. Utilisez `ptr` et `link` pour mapper la connexion client locale à la connexion serveur.

2. Utilisez `addr` et `port` de la connexion client pour identifier la connexion TCP depuis le client.

3. Utilisez `local_addr` et `local_port` pour identifier la connexion TCP au serveur.

--------

## Faut-il installer PgBouncer sur le serveur web ou le serveur de base de données ? {#should-pgbouncer-be-installed-on-the-web-server-or-database-server}

Cela dépend.

Installer PgBouncer sur le serveur web est pertinent lorsque des connexions de courte durée sont utilisées. Cela permet de minimiser la latence d’établissement de connexion. (Le protocole TCP nécessite plusieurs allers-retours de paquets avant qu’une connexion ne devienne utilisable.) Installer PgBouncer sur le serveur de base de données est pertinent lorsque de nombreux hôtes différents (par exemple, des serveurs web) se connectent à celui-ci. Les connexions peuvent alors être optimisées conjointement.

Il est également possible d'installer PgBouncer sur le serveur web et le serveur de base de données. Un inconvénient de cette approche est qu'une connexion PgBouncer supplémentaire ajoute une légère latence à chaque requête.

En fin de compte, vous devrez tester quel modèle convient le mieux à vos besoins en performance. Vous devriez également tenir compte de l'impact de l'installation de PgBouncer sur la bascule d'application en cas de défaillance d'un serveur web ou d'un serveur de base de données.
