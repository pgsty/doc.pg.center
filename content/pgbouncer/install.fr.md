---
title: "Compilation et installation de PgBouncer"
linkTitle: "Installation"
weight: 40
description: "Instructions de compilation et d'installation de PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Tutoriel]
aliases: [/docs/pgbouncer/install/]
upstream_link: "https://www.pgbouncer.org/install.html"
---

--------

## Construction {#building}

PgBouncer dépend de quelques éléments pour être compilé :

* [GNU Make] 3.81+
* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ pour la prise en charge du TLS
* (facultatif) [c-ares] en tant qu’alternative à evdns de Libevent
* (facultatif) bibliothèques LDAP
* (facultatif) bibliothèques PAM

[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

Lorsque les dépendances sont installées, exécutez simplement :

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

Si vous compilez à partir de Git, ou si vous compilez pour Windows, veuillez consulter les instructions de compilation spécifiques ci-dessous.

--------

## Prise en charge des recherches DNS {#dns-lookup-support}

PgBouncer effectue des recherches de noms d'hôte au moment de la connexion, et non une seule fois au moment du chargement de la configuration. Cela nécessite une implémentation DNS asynchrone. Le tableau suivant indique les backends pris en charge ainsi que leur ordre de sondage :

| backend                    | parallel | EDNS0 (1) | /etc/hosts | SOA lookup (2) | note                                  |
|----------------------------|----------|-----------|------------|----------------|---------------------------------------|
| c-ares                     | yes      | yes       | yes        | yes            | problème avec IPv6+CNAME pour les versions ≤ 1.10 |
| evdns, libevent 2.x        | yes      | no        | yes        | no             | ne vérifie pas les mises à jour de /etc/hosts |
| getaddrinfo_a, glibc 2.9+  | yes      | yes (3)   | yes        | no             | non disponible sur les systèmes non-glibc |
| getaddrinfo, libc          | no       | yes (3)   | yes        | no             | nécessite pthreads                    |

1. EDNS0 est requis pour avoir plus de 8 adresses derrière un même nom d'hôte.
2. Une requête SOA est nécessaire pour vérifier à nouveau les noms d'hôte en cas de changement du numéro de série de la zone.
3. Pour activer EDNS0, ajoutez `options edns0` à `/etc/resolv.conf`.

c-ares est l’implémentation la plus complète et est recommandée pour la plupart des utilisations et des paquetages binaires (si une version suffisamment récente est disponible). L’implémentation evdns intégrée à libevent convient également à de nombreuses utilisations, sous réserve des restrictions mentionnées. Les autres backends sont principalement des options héritées à l’heure actuelle et ne bénéficient plus d’un test important.

Par défaut, c-ares est utilisé s'il est détecté. Son utilisation peut être imposée avec `configure --with-cares` ou désactivée avec `--without-cares`. Si c-ares n'est pas utilisé (non trouvé ou désactivé), alors Libevent est utilisé. Spécifiez `--disable-evdns` pour désactiver l'utilisation de evdns de Libevent et revenir à une implémentation basée sur libc.

--------

## Authentification PAM {#pam-authentication}

Pour activer l'authentification PAM, `./configure` dispose d'un indicateur `--with-pam`
(valeur par défaut : no). Lorsqu'il est compilé avec le support PAM, un nouveau type d'authentification global `pam` devient disponible pour valider les utilisateurs via PAM.

--------

## Authentification LDAP {#ldap-authentication}

Pour activer l'authentification LDAP, `./configure` dispose d'un indicateur `--with-ldap`
(valeur par défaut : no). Lorsqu'il est compilé avec le support LDAP, un nouveau type d'authentification global `ldap` devient disponible pour valider les utilisateurs via LDAP.

--------

## intégration systemd {#systemd-integration}

Pour activer l'intégration avec systemd, utilisez l'option `configure`
`--with-systemd`. Cela permet d'utiliser `Type=notify` (ou `Type=notify-reload` si vous utilisez systemd 253 ou une version ultérieure) ainsi que l'activation par socket. Consultez `etc/pgbouncer.service` et `etc/pgbouncer.socket` pour des exemples.

--------

## Construction à partir de Git {#building-from-git}

La compilation de PgBouncer à partir de Git nécessite de générer les fichiers d'en-tête et de configuration avant de pouvoir exécuter `configure` :

	$ git clone https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

Tous les fichiers seront installés sous `/usr/local` par défaut. Vous pouvez fournir une ou plusieurs options en ligne de commande à `configure`. Exécutez `./configure --help` pour afficher les options disponibles et les variables d'environnement qui personnalisent la configuration.

Paquets supplémentaires requis : autoconf, automake, libtool, pandoc

--------

## Test {#testing}

Consultez le fichier [`README.md` dans le répertoire de test][1] pour savoir comment exécuter les tests.

[1]: https://github.com/pgbouncer/pgbouncer/blob/master/test/README.md

--------

## Construction sous Windows {#building-on-windows}

L’environnement de compilation pris en charge sur Windows est uniquement MinGW. Cygwin et Visual $ANYTHING ne sont pas pris en charge.

Pour compiler sous MinGW, procédez comme d'habitude :

	$ ./configure
	$ make

Si vous effectuez une compilation croisée depuis Unix :

	$ ./configure --host=i586-mingw32msvc

L'option de compilation LDAP n'est actuellement pas prise en charge sous Windows.

--------

## Exécution sous Windows {#running-on-windows}

Exécution depuis la ligne de commande se déroule normalement, à l’exception des options `-d` (daemonize), `-R` (reboot) et `-u` (switch user) qui ne fonctionnent pas.

Pour exécuter PgBouncer en tant que service Windows, vous devez configurer le paramètre
`service_name` afin de définir un nom pour le service. Ensuite :

	$ pgbouncer -regservice config.ini

Pour désinstaller le service :

	$ pgbouncer -unregservice config.ini

Pour utiliser le journal des événements Windows, définissez `syslog = 1` dans le fichier de configuration.
Mais avant cela, vous devez inscrire `pgbevent.dll` :

	$ regsvr32 pgbevent.dll

Pour le désenregistrer, procédez comme suit :

	$ regsvr32 /u pgbevent.dll
