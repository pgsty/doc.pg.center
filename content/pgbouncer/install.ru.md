---
title: "Компиляция и установка PgBouncer"
linkTitle: "Установка"
weight: 40
description: "Инструкции по компиляции и установке PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Руководство]
aliases: [/docs/pgbouncer/install/]
upstream_link: "https://www.pgbouncer.org/install.html"
---

--------

## Сборка {#building}

Для компиляции PgBouncer требуется несколько компонентов:

* [GNU Make] 3.81+
* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ для поддержки TLS
* (необязательно) [c-ares] как альтернатива evdns из Libevent
* (необязательно) библиотеки LDAP
* (необязательно) библиотеки PAM

[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

После установки зависимостей выполните:

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

Для сборки из Git или под Windows используйте отдельные инструкции ниже.

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

По умолчанию при наличии c-ares используется именно он. Его можно принудительно
выбрать с помощью `configure --with-cares` или отключить через `--without-cares`.
Если c-ares не используется — не найден или отключён, — выбирается Libevent.
Укажите `--disable-evdns`, чтобы отключить evdns из Libevent и перейти к
реализации на основе libc.

--------

## Аутентификация PAM {#pam-authentication}

Для включения аутентификации PAM у `./configure` есть флаг `--with-pam` (по
умолчанию отключён). После компиляции с поддержкой PAM становится доступен новый
глобальный тип аутентификации `pam` для проверки пользователей через PAM.

--------

## Аутентификация LDAP {#ldap-authentication}

Для включения аутентификации LDAP у `./configure` есть флаг `--with-ldap` (по
умолчанию отключён). После компиляции с поддержкой LDAP становится доступен новый
глобальный тип аутентификации `ldap` для проверки пользователей через LDAP.

--------

## Интеграция с systemd {#systemd-integration}

Чтобы включить интеграцию с systemd, используйте параметр `configure`
`--with-systemd`. Он позволяет применять `Type=notify` либо `Type=notify-reload`
в systemd 253 и новее, а также активацию через сокеты. Примеры приведены в
`etc/pgbouncer.service` и `etc/pgbouncer.socket`.

--------

## Сборка из Git {#building-from-git}

При сборке PgBouncer из Git перед запуском `configure` необходимо создать
файлы заголовков и конфигурации:

	$ git clone https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

По умолчанию все файлы устанавливаются в `/usr/local`. Команде `configure`
можно передать один или несколько параметров командной строки. Выполните
`./configure --help`, чтобы получить список доступных параметров и переменных
окружения для настройки конфигурации.

Дополнительно требуются пакеты: autoconf, automake, libtool, pandoc.

--------

## Тестирование {#testing}

Порядок запуска тестов приведён в [файле `README.md` каталога тестов][1].

[1]: https://github.com/pgbouncer/pgbouncer/blob/master/test/README.md

--------

## Сборка под Windows {#building-on-windows}

Единственная поддерживаемая среда сборки в Windows — MinGW. Cygwin и
Visual $ANYTHING не поддерживаются.

Для сборки в MinGW выполните обычные команды:

	$ ./configure
	$ make

При кросс-компиляции из Unix:

	$ ./configure --host=i586-mingw32msvc

Сборка с LDAP в Windows сейчас не поддерживается.

--------

## Запуск в Windows {#running-on-windows}

Запуск из командной строки выполняется обычным образом, но ключи `-d`
(демонизация), `-R` (перезапуск) и `-u` (смена пользователя) не работают.

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
