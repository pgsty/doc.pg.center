---
title: "Compilation et installation de PgBouncer"
linkTitle: "Installation"
weight: 40
description: "Instructions de compilation et d'installation de PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Tutoriel]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/README.md"
---

--------

## Construction {#building}

PgBouncer peut être compilé avec le système de compilation basé sur Autoconf
ou avec le système [Meson], plus récent mais encore expérimental. Pour
l’instant, Autoconf reste le choix recommandé pour les compilations de
production et la création de paquets. La compilation avec Meson devrait
devenir le mode par défaut et celle avec Autoconf être supprimée dans une
version future ; la tester et signaler tout problème est donc très bienvenu.
La compilation dépend de quelques éléments :

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ pour la prise en charge du TLS
* un compilateur C compatible C11
* (facultatif) [c-ares] en tant qu’alternative à evdns de Libevent
* (facultatif) bibliothèques LDAP
* (facultatif) bibliothèques PAM

La compilation avec Meson nécessite en outre [Meson] 0.58+ et [Ninja] ; la
compilation avec Autoconf nécessite [GNU Make] 3.81+.

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

Lorsque les dépendances sont installées, compilez avec Autoconf :

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

ou avec Meson (expérimental) :

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

Si vous compilez à partir de Git, ou si vous compilez pour Windows, veuillez consulter les instructions de compilation spécifiques ci-dessous.

--------

## Prise en charge des recherches DNS {#dns-lookup-support}

PgBouncer effectue des recherches de noms d'hôte au moment de la connexion, et non une seule fois au moment du chargement de la configuration. Cela nécessite une implémentation DNS asynchrone. Le tableau suivant indique les backends pris en charge ainsi que leur ordre de sondage :

| backend                    | parallèle | EDNS0 (1) | /etc/hosts | requête SOA (2) | note                                  |
|----------------------------|-----------|-----------|------------|-----------------|---------------------------------------|
| c-ares                     | oui       | oui       | oui        | oui             | problème avec IPv6+CNAME pour les versions <= 1.10 |
| evdns, libevent 2.x        | oui       | non       | oui        | non             | ne vérifie pas les mises à jour de /etc/hosts |
| getaddrinfo_a, glibc 2.9+  | oui       | oui (3)   | oui        | non             | N/A (non disponible sur les systèmes non-glibc) |
| getaddrinfo, libc          | non       | oui (3)   | oui        | non             | nécessite pthreads                    |

1. EDNS0 est requis pour avoir plus de 8 adresses derrière un même nom d'hôte.
2. Une requête SOA est nécessaire pour vérifier à nouveau les noms d'hôte en cas de changement du numéro de série de la zone.
3. Pour activer EDNS0, ajoutez `options edns0` à `/etc/resolv.conf`.

c-ares est l’implémentation la plus complète et est recommandée pour la plupart des utilisations et des paquetages binaires (si une version suffisamment récente est disponible). L’implémentation evdns intégrée à libevent convient également à de nombreuses utilisations, sous réserve des restrictions mentionnées. Les autres backends sont à l’heure actuelle pour l’essentiel des options héritées et ne font plus l’objet de nombreux tests.

Par défaut, c-ares est utilisé s'il est détecté. Son utilisation peut être imposée avec `-Dcares=enabled` (configure : `--with-cares`) ou désactivée avec `-Dcares=disabled` (configure : `--without-cares`). Si c-ares n'est pas utilisé (non trouvé ou désactivé), alors Libevent est utilisé. Spécifiez `-Devdns=false` (configure : `--disable-evdns`) pour désactiver l'utilisation d'evdns de Libevent et revenir à une implémentation basée sur libc.

--------

## Fonctionnalités optionnelles {#optional-features}

Les fonctionnalités PAM, LDAP et systemd sont détectées automatiquement par
meson : leurs options `-Dpam`, `-Dldap` et `-Dsystemd` ont la valeur par défaut
`auto`, chacune est donc compilée lorsque ses bibliothèques sont présentes.
Forcez l'activation d'une fonctionnalité avec `-D<feature>=enabled` ou sa
désactivation avec `-D<feature>=disabled`. La compilation Autoconf ne les
détecte pas automatiquement ; activez-les explicitement avec `--with-pam`,
`--with-ldap` ou `--with-systemd`.

--------

## Authentification PAM {#pam-authentication}

Lorsqu'il est compilé avec la prise en charge de PAM, un nouveau type d'authentification global `pam` devient disponible pour valider les utilisateurs via PAM.

--------

## Authentification LDAP {#ldap-authentication}

Lorsqu'il est compilé avec la prise en charge de LDAP, un nouveau type d'authentification global `ldap` devient disponible pour valider les utilisateurs via LDAP.

--------

## Intégration systemd {#systemd-integration}

La prise en charge de systemd permet d'utiliser `Type=notify` (ou `Type=notify-reload` si vous utilisez systemd 253 ou une version ultérieure) ainsi que l'activation par socket. Consultez `etc/pgbouncer.service` et `etc/pgbouncer.socket` pour des exemples.

--------

## Construction à partir de Git {#building-from-git}

La compilation Autoconf nécessite de générer les fichiers d'en-tête et de configuration avant de pouvoir exécuter `configure` :

	$ git clone --branch pgbouncer_1_26_1 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

Tous les fichiers seront installés sous `/usr/local` par défaut. Vous pouvez fournir une ou plusieurs options en ligne de commande à `configure`. Exécutez `./configure --help` pour afficher la liste des options disponibles et des variables d'environnement qui personnalisent la configuration.

Paquets supplémentaires requis pour la compilation Autoconf à partir de Git : autoconf, automake, libtool, pandoc

Avec la compilation Meson, vous pouvez compiler directement à partir d'un checkout ;
pandoc est requis pour générer les pages de manuel :

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

Exécutez `meson configure build` pour afficher la liste des options `-D` disponibles.

--------

## Test {#testing}

Consultez le fichier [`README.md` dans le répertoire de test][1] pour savoir comment exécuter les tests.

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/test/README.md

--------

## Construction sous Windows {#building-on-windows}

Le seul environnement de compilation pris en charge sous Windows est MinGW. Cygwin et Visual $ANYTHING ne sont pas pris en charge.

Pour compiler sous MinGW, procédez à la compilation Autoconf habituelle :

	$ ./configure
	$ make

ou à la compilation Meson expérimentale :

	$ meson setup build
	$ meson compile -C build

En cas de compilation croisée depuis Unix avec Autoconf :

	$ ./configure --host=i586-mingw32msvc

L'option de compilation LDAP n'est actuellement pas prise en charge sous Windows.

--------

## Exécution sous Windows {#running-on-windows}

L'exécution depuis la ligne de commande se déroule comme d'habitude, à l'exception des options `-d` (lancement en démon) et `-u` (changement d'utilisateur) qui ne fonctionnent pas.

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
