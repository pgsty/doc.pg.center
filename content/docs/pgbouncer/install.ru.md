---
title: "Компиляция и установка PgBouncer"
linkTitle: "Установка"
weight: 40
description: "Инструкции по компиляции и установке PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Руководство]
aliases: [/pgbouncer/install/]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/README.md"
---

--------

## Сборка {#building}

PgBouncer можно собрать как средствами системы сборки на основе Autoconf, так и
более новой, пока экспериментальной системой сборки [Meson]. Для рабочих сборок
и пакетирования сейчас рекомендуется Autoconf. Ожидается, что в одном из будущих
выпусков сборка Meson станет стандартной, а сборка Autoconf будет удалена,
поэтому очень приветствуются её тестирование и сообщения о любых проблемах.
Для компиляции требуется несколько компонентов:

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ для поддержки TLS
* компилятор C с поддержкой C11
* (необязательно) [c-ares] как альтернатива evdns из Libevent
* (необязательно) библиотеки LDAP
* (необязательно) библиотеки PAM

Для сборки Meson дополнительно требуются [Meson] 0.58+ и [Ninja]; для сборки
Autoconf — [GNU Make] 3.81+.

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

Когда зависимости установлены, выполните сборку средствами Autoconf:

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

или средствами Meson (экспериментально):

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

Если сборка выполняется из Git или под Windows, см. отдельные инструкции
по сборке ниже.

--------

## Поддержка поиска DNS {#dns-lookup-support}

PgBouncer разрешает имена узлов при установке соединения, а не только один раз
при загрузке конфигурации. Для этого нужна асинхронная реализация DNS. В таблице
перечислены поддерживаемые бэкенды в порядке их проверки:

| Бэкенд                     | Параллельно | EDNS0 (1) | /etc/hosts | Поиск SOA (2) | Примечание                            |
|----------------------------|----------|-----------|------------|----------------|---------------------------------------|
| c-ares                     | да       | да        | да         | да             | ошибки IPv6+CNAME в <=1.10            |
| evdns, libevent 2.x        | да       | нет       | да         | нет            | не проверяет обновления /etc/hosts    |
| getaddrinfo_a, glibc 2.9+  | да       | да (3)    | да         | нет            | недоступен вне glibc                  |
| getaddrinfo, libc          | нет      | да (3)    | да         | нет            | требует pthreads                      |

1. EDNS0 необходим, если с одним именем узла связано более 8 адресов.
2. Поиск SOA необходим для повторной проверки имён узлов при изменении серийного номера зоны.
3. Чтобы включить EDNS0, добавьте `options edns0` в `/etc/resolv.conf`.

c-ares — наиболее функциональная реализация, рекомендуемая для большинства
вариантов использования и сборки двоичных пакетов при наличии достаточно новой
версии. Встроенный в Libevent evdns также подходит во многих случаях с учётом
указанных ограничений. Остальные бэкенды в основном устарели и теперь почти
не тестируются.

По умолчанию при обнаружении c-ares используется именно он. Его использование
можно принудительно включить с помощью `-Dcares=enabled` (configure:
`--with-cares`) или отключить с помощью `-Dcares=disabled` (configure:
`--without-cares`). Если c-ares не используется — не найден или отключён, —
используется Libevent. Укажите `-Devdns=false` (configure: `--disable-evdns`),
чтобы отключить использование evdns из Libevent и перейти к реализации на
основе libc.

--------

## Необязательные функции {#optional-features}

Возможности PAM, LDAP и systemd определяются системой meson автоматически: их
параметры `-Dpam`, `-Dldap` и `-Dsystemd` по умолчанию имеют значение `auto`,
поэтому каждая из них включается в сборку при наличии соответствующих библиотек.
Принудительно включить возможность можно с помощью `-D<feature>=enabled`, а
отключить — с помощью `-D<feature>=disabled`. Сборка Autoconf не определяет эти
возможности автоматически; включайте их явно с помощью `--with-pam`,
`--with-ldap` или `--with-systemd`.

--------

## Аутентификация PAM {#pam-authentication}

После компиляции с поддержкой PAM становится доступен новый глобальный тип
аутентификации `pam` для проверки пользователей через PAM.

--------

## Аутентификация LDAP {#ldap-authentication}

После компиляции с поддержкой LDAP становится доступен новый глобальный тип
аутентификации `ldap` для проверки пользователей через LDAP.

--------

## Интеграция с systemd {#systemd-integration}

Поддержка systemd позволяет использовать `Type=notify` (или
`Type=notify-reload`, если применяется systemd 253 или новее), а также
активацию через сокеты. Примеры приведены в `etc/pgbouncer.service` и
`etc/pgbouncer.socket`.

--------

## Сборка из Git {#building-from-git}

При сборке Autoconf перед запуском `configure` необходимо создать файлы
заголовков и конфигурации:

	$ git clone --branch pgbouncer_1_26_0 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

По умолчанию все файлы устанавливаются в `/usr/local`. Команде `configure`
можно передать один или несколько параметров командной строки. Выполните
`./configure --help`, чтобы получить список доступных параметров и переменных
окружения, позволяющих настроить конфигурацию.

Дополнительно для сборки Autoconf из Git требуются пакеты: autoconf, automake,
libtool, pandoc

Сборка Meson позволяет собирать прямо из копии репозитория; для сборки страниц
руководства требуется pandoc:

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

Выполните `meson configure build`, чтобы получить список доступных параметров
`-D`.

--------

## Тестирование {#testing}

Порядок запуска тестов приведён в [файле `README.md` каталога тестов][1].

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/test/README.md

--------

## Сборка под Windows {#building-on-windows}

Единственная поддерживаемая среда сборки в Windows — MinGW. Cygwin и
Visual $ANYTHING не поддерживаются.

Для сборки в MinGW выполните обычную сборку Autoconf:

	$ ./configure
	$ make

или экспериментальную сборку Meson:

	$ meson setup build
	$ meson compile -C build

При кросс-компиляции из Unix с Autoconf:

	$ ./configure --host=i586-mingw32msvc

Параметр сборки с LDAP в настоящее время не поддерживается в Windows.

--------

## Запуск в Windows {#running-on-windows}

Запуск из командной строки выполняется обычным образом, но ключи `-d`
(демонизация) и `-u` (смена пользователя) не работают.

Чтобы запустить PgBouncer как службу Windows, задайте имя службы параметром
`service_name`, затем выполните:

	$ pgbouncer -regservice config.ini

Чтобы удалить службу:

	$ pgbouncer -unregservice config.ini

Чтобы использовать журнал событий Windows, задайте в файле конфигурации
`syslog = 1`. Перед этим необходимо зарегистрировать `pgbevent.dll`:

	$ regsvr32 pgbevent.dll

Чтобы отменить регистрацию:

	$ regsvr32 /u pgbevent.dll
