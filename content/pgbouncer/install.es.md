---
title: "Compilación e instalación de PgBouncer"
linkTitle: "Instalación"
weight: 40
description: "Instrucciones de compilación e instalación de PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Tutorial]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/README.md"
---

--------

## Compilación {#building}

PgBouncer puede compilarse con el sistema de compilación basado en Autoconf o
con el sistema de compilación [Meson], más nuevo pero aún experimental. Por
ahora, Autoconf es la opción recomendada para compilaciones de producción y
para el empaquetado. Se espera que la compilación con Meson se convierta en
la predeterminada y que la de Autoconf se elimine en una versión futura, por
lo que probarla y reportar cualquier problema es de gran ayuda.
La compilación depende de algunos elementos:

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ para el soporte de TLS
* un compilador de C compatible con C11
* (opcional) [c-ares] como alternativa a evdns de Libevent
* (opcional) bibliotecas LDAP
* (opcional) bibliotecas PAM

La compilación con Meson necesita además [Meson] 0.58+ y [Ninja]; la
compilación con Autoconf necesita [GNU Make] 3.81+.

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

Cuando las dependencias estén instaladas, compila con Autoconf:

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

o con Meson (experimental):

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

Si compilas a partir de Git, o si compilas para Windows, consulta las
instrucciones de compilación específicas más abajo.

--------

## Soporte de resolución DNS {#dns-lookup-support}

PgBouncer realiza búsquedas de nombres de host en el momento de la conexión,
y no una sola vez al cargar la configuración. Esto requiere una
implementación de DNS asíncrona. La siguiente tabla muestra los backends
admitidos y su orden de sondeo:

| backend                    | paralelo | EDNS0 (1) | /etc/hosts | consulta SOA (2) | nota                                  |
|----------------------------|----------|-----------|------------|------------------|---------------------------------------|
| c-ares                     | sí       | sí        | sí         | sí               | IPv6+CNAME con errores en <=1.10      |
| evdns, libevent 2.x        | sí       | no        | sí         | no               | no comprueba actualizaciones de /etc/hosts |
| getaddrinfo_a, glibc 2.9+  | sí       | sí (3)    | sí         | no               | N/A en sistemas que no son glibc      |
| getaddrinfo, libc          | no       | sí (3)    | sí         | no               | requiere pthreads                     |

1. Se requiere EDNS0 para tener más de 8 direcciones detrás de un mismo nombre de host.
2. La consulta SOA es necesaria para volver a comprobar los nombres de host cuando cambia el número de serie de la zona.
3. Para activar EDNS0, añade `options edns0` a `/etc/resolv.conf`.

c-ares es la implementación más completa y se recomienda para la mayoría de
los usos y para el empaquetado binario (si hay disponible una versión
suficientemente reciente). El evdns integrado de Libevent también es adecuado
para muchos usos, con las restricciones indicadas. Los demás backends son a
estas alturas en su mayoría opciones heredadas y ya no reciben muchas pruebas.

De forma predeterminada, se usa c-ares si se puede encontrar. Su uso puede
forzarse con `-Dcares=enabled` (configure: `--with-cares`) o desactivarse con
`-Dcares=disabled` (configure: `--without-cares`). Si no se usa c-ares
(no se encuentra o está desactivado), entonces se usa Libevent. Especifica
`-Devdns=false` (configure: `--disable-evdns`) para desactivar el uso del
evdns de Libevent y recurrir a una implementación basada en libc.

--------

## Características opcionales {#optional-features}

Las características PAM, LDAP y systemd las detecta automáticamente meson: sus
opciones `-Dpam`, `-Dldap` y `-Dsystemd` tienen el valor predeterminado
`auto`, por lo que cada una se compila cuando sus bibliotecas están presentes.
Fuerza su activación con `-D<feature>=enabled` o su desactivación con
`-D<feature>=disabled`. La compilación con Autoconf no las detecta
automáticamente; actívalas explícitamente con `--with-pam`, `--with-ldap` o
`--with-systemd`.

--------

## Autenticación PAM {#pam-authentication}

Cuando se compila con soporte de PAM, está disponible un nuevo tipo global de
autenticación `pam` para validar usuarios a través de PAM.

--------

## Autenticación LDAP {#ldap-authentication}

Cuando se compila con soporte de LDAP, está disponible un nuevo tipo global de
autenticación `ldap` para validar usuarios a través de LDAP.

--------

## Integración con systemd {#systemd-integration}

El soporte de systemd permite usar `Type=notify` (o `Type=notify-reload` si
usas systemd 253 o posterior), así como la activación por socket. Consulta
`etc/pgbouncer.service` y `etc/pgbouncer.socket` para ver ejemplos.

--------

## Compilación a partir de Git {#building-from-git}

La compilación con Autoconf requiere que generes los archivos de cabecera y de
configuración antes de poder ejecutar `configure`:

	$ git clone --branch pgbouncer_1_26_0 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

Todos los archivos se instalarán bajo `/usr/local` de forma predeterminada.
Puedes pasar una o más opciones de línea de comandos a `configure`. Ejecuta
`./configure --help` para listar las opciones disponibles y las variables de
entorno que personalizan la configuración.

Paquetes adicionales necesarios para la compilación con Autoconf a partir de
Git: autoconf, automake, libtool, pandoc

Con la compilación de Meson puedes compilar directamente desde un checkout;
pandoc es necesario para compilar las páginas de manual:

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

Ejecuta `meson configure build` para listar las opciones `-D` disponibles.

--------

## Pruebas {#testing}

Consulta el archivo [`README.md` del directorio de pruebas][1] para saber cómo
ejecutar las pruebas.

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/test/README.md

--------

## Compilación en Windows {#building-on-windows}

El único entorno de compilación admitido en Windows es MinGW. Cygwin y
Visual $ANYTHING no son compatibles.

Para compilar en MinGW, haz la compilación habitual con Autoconf:

	$ ./configure
	$ make

o la compilación experimental con Meson:

	$ meson setup build
	$ meson compile -C build

Si haces una compilación cruzada desde Unix con Autoconf:

	$ ./configure --host=i586-mingw32msvc

La opción de compilación LDAP actualmente no es compatible con Windows.

--------

## Ejecución en Windows {#running-on-windows}

La ejecución desde la línea de comandos funciona como de costumbre, excepto
que las opciones `-d` (ejecutar como demonio) y `-u` (cambiar de usuario) no
funcionarán.

Para ejecutar PgBouncer como un servicio de Windows, debes configurar el
parámetro `service_name` para asignar un nombre al servicio. Después:

	$ pgbouncer -regservice config.ini

Para desinstalar el servicio:

	$ pgbouncer -unregservice config.ini

Para usar el registro de eventos de Windows, establece `syslog = 1` en el
archivo de configuración. Pero antes de eso, debes registrar `pgbevent.dll`:

	$ regsvr32 pgbevent.dll

Para anular su registro, haz lo siguiente:

	$ regsvr32 /u pgbevent.dll
