---
title: "Руководство пользователя (RHEL)"
linkTitle: "Руководство (EL)"
weight: 30
description: "Пошаговое руководство по настройке и использованию pgBackRest в системах RHEL, Rocky и AlmaLinux."
icon: fa-brands fa-redhat
module: [PGBACKREST]
categories: [Руководство]
aliases: [/pgbackrest/user-guide-rhel/]
upstream_link: "https://pgbackrest.org/user-guide-rhel.html"
---

--------

## Введение {#introduction}

Это руководство следует читать последовательно от начала до конца: каждый раздел опирается на предыдущий. Например, раздел [Восстановление](#restore-1) предполагает настройку, выполненную в разделе [Быстрый старт](#quick-start). После установки и запуска pgBackRest можно переходить между разделами, но при первом знакомстве рекомендуется пройти руководство по порядку.

Хотя примеры в этом руководстве рассчитаны на RHEL и PostgreSQL 14, их должно быть довольно легко адаптировать к любому дистрибутиву Unix и любой версии PostgreSQL. От ОС зависят только команды создания, запуска, остановки и удаления кластеров PostgreSQL. Команды pgBackRest одинаковы во всех системах Unix, хотя расположение исполняемого файла может различаться. pgBackRest стремится работать одинаково с разными версиями PostgreSQL, однако между ними есть небольшие различия, которые могут проявляться в отдельных примерах этого руководства, например в путях, именах файлов и настройках PostgreSQL.

Сведения о настройке и документация PostgreSQL доступны в [руководстве PostgreSQL](http://www.postgresql.org/docs/14/static/index.html).

При подготовке этого руководства используется несколько необычный подход. При сборке документации из исходных XML-файлов каждая команда выполняется на виртуальной машине. Это позволяет с высокой уверенностью утверждать, что команды корректно работают в указанном порядке. При необходимости вывод сохраняется и показывается под командой. Если вывод отсутствует, он был сочтён несущественным или отвлекающим от изложения.

Все команды рассчитаны на выполнение непривилегированным пользователем с правами sudo для пользователей `root` и `postgres`. Команды также можно без изменений выполнять непосредственно от имени соответствующих пользователей; в этом случае префиксы `sudo` можно убрать.

--------

## Основные понятия {#concepts}

Ниже приведены определения понятий в контексте pgBackRest, PostgreSQL и этого руководства.

### Резервная копия {#backup}

Резервная копия — это согласованная копия кластера баз данных, которую можно восстановить после аппаратного сбоя, для возврата к определённому моменту времени или для запуска нового резервного сервера.

**Полная резервная копия**: pgBackRest копирует в резервную копию всё содержимое кластера баз данных. Первая резервная копия кластера всегда является полной. pgBackRest всегда может восстановить полную резервную копию непосредственно. Её согласованность не зависит от файлов за пределами самой полной резервной копии.

**Дифференциальная резервная копия**: pgBackRest копирует только те файлы кластера баз данных, которые изменились с момента последней полной резервной копии. При восстановлении дифференциальной резервной копии pgBackRest копирует все файлы выбранной дифференциальной копии и соответствующие неизменившиеся файлы предыдущей полной копии. Преимущество дифференциальной копии в том, что она занимает меньше места, чем полная, однако для её восстановления должны быть исправны как дифференциальная, так и полная резервная копия.

**Инкрементная резервная копия**: pgBackRest копирует только те файлы кластера баз данных, которые изменились с момента последней резервной копии (другой инкрементной, дифференциальной или полной). Поскольку инкрементная копия включает лишь файлы, изменившиеся после предыдущей копии, она обычно значительно меньше полной или дифференциальной. Как и в случае дифференциальной копии, восстановление инкрементной копии зависит от исправности других резервных копий. Поскольку инкрементная копия содержит только файлы, изменившиеся после последней копии, для её восстановления должны быть исправны все предшествующие инкрементные копии вплоть до предыдущей дифференциальной, сама эта дифференциальная копия и предшествующая полная копия. Если дифференциальной копии нет, должны быть исправны все предшествующие инкрементные копии вплоть до предыдущей полной копии, наличие которой обязательно, а также сама полная копия.

### Восстановление {#restore}

Восстановление — это копирование резервной копии в систему, где она будет запущена как рабочий кластер баз данных. Для корректного восстановления нужны файлы резервной копии и один или несколько сегментов WAL.

### Журнал предзаписи (WAL) {#write-ahead-log-wal}

WAL — механизм, с помощью которого PostgreSQL гарантирует сохранность зафиксированных изменений. Транзакции последовательно записываются в WAL; транзакция считается зафиксированной после того, как эти записи сброшены на диск. Затем фоновый процесс записывает изменения в основные файлы кластера баз данных (также называемые кучей). После аварийного завершения WAL воспроизводится, чтобы привести базу данных в согласованное состояние.

Концептуально WAL бесконечен, но на практике он разбит на отдельные файлы размером 16MB, называемые сегментами. Имена сегментов WAL имеют вид `0000000100000A1E000000FE`: первые 8 шестнадцатеричных цифр обозначают временную шкалу, а следующие 16 — логический порядковый номер (LSN).

### Шифрование {#encryption}

Шифрование — это преобразование данных в формат, который невозможно распознать без соответствующего пароля (также называемого парольной фразой).

pgBackRest шифрует репозиторий с использованием пароля, заданного пользователем, предотвращая несанкционированный доступ к хранящимся в нём данным.

--------

## Обновление pgBackRest {#upgrading-pgbackrest}


### Обновление pgBackRest с v2.x до v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

Обновление с v2.x до v2.y несложно. Формат репозитория не изменился, поэтому в большинстве установок достаточно установить исполняемые файлы новой версии. Понижение версии также возможно, если не использовались новые функции, которые не поддерживаются старой версией.

ВАЖНО:

Локальная и удалённая версии pgBackRest должны в точности совпадать, поэтому их следует обновлять одновременно. При несовпадении версий архивирование WAL и резервное копирование не будут работать, пока версии не совпадут. В этом случае выводится ошибка: `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.

--------

## Сборка {#build}

Предпочтительнее устанавливать pgBackRest из пакета, чем собирать из исходного кода. Дополнительные сведения о пакетах приведены в разделе [Установка](#installation).

Сборку из исходного кода лучше выполнять на отдельном сервере сборки, а не в рабочей среде. Многие необходимые для сборки инструменты обычно не следует устанавливать в рабочей среде. pgBackRest состоит из одного исполняемого файла, поэтому после сборки его легко скопировать на другой сервер.

build **⇒** Загрузить pgBackRest версии `2.59.3` в каталог `/build`

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** Установить зависимости для сборки

```bash
sudo yum install meson gcc postgresql14-devel openssl-devel libxml2-devel \
       lz4-devel libzstd-devel bzip2-devel libssh2-devel systemd-devel
```

build **⇒** Настроить и скомпилировать pgBackRest

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.59.3
ninja -C /build/pgbackrest
```

build **⇒** При необходимости запустить базовые тесты, чтобы проверить правильность сборки pgBackRest

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               10.32s

Ok:                 1
       [filtered 6 lines of output]
```

--------

## Установка {#installation}

Для демонстрационного кластера и выполнения примеров pgBackRest создаётся новый сервер с именем pg-primary.

Предпочтительнее устанавливать pgBackRest из пакета, чем собирать из исходного кода. При установке из пакета остальные инструкции этого раздела обычно не нужны, однако пакет может не создать какой-либо каталог или назначить неверные права доступа. В таком случае может потребоваться вручную создать каталоги или исправить права.

Пакеты pgBackRest для RHEL доступны на [yum.postgresql.org](http://yum.postgresql.org).

Если для используемого дистрибутива или его версии нет пакетов, можно [собрать программу из исходного кода](#build), а затем установить её вручную, как показано ниже.

pg-primary **⇒** Установить зависимости

```bash
sudo yum install postgresql-libs libssh2
```

pg-primary **⇒** Скопировать исполняемый файл pgBackRest с сервера сборки

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

Для pgBackRest нужны каталоги журналов и конфигурации, а также файл конфигурации.

pg-primary **⇒** Создать файл конфигурации и каталоги pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

Теперь pgBackRest должен быть установлен правильно, но лучше это проверить. Если какие-либо зависимости пропущены, при запуске pgBackRest из командной строки возникнет ошибка.

pg-primary **⇒** Убедиться в успешной установке

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.59.3 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## Быстрый старт {#quick-start}

В разделе «Быстрый старт» рассматривается базовая настройка pgBackRest и PostgreSQL, а также команды `backup`, `restore` и `info`.

### Создание демонстрационного кластера {#setup-demo-cluster}

Создавать демонстрационный кластер необязательно, но настоятельно рекомендуется, особенно новым пользователям: команды в примерах этого руководства обращаются именно к нему. Предполагается, что демонстрационный кластер работает на порту по умолчанию (5432). Кластер будет запущен в одном из следующих разделов, поскольку сначала нужно завершить настройку.

pg-primary **⇒** Создать демонстрационный кластер

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

По умолчанию RHEL включает день недели в имя файла журнала. Это несколько усложняет руководство, поэтому для log_filename задаётся постоянное значение.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Задать log_filename

```ini
log_filename = 'postgresql.log'
```

### Настройка stanza кластера {#configure-cluster-stanza}

Stanza — это конфигурация кластера баз данных PostgreSQL, определяющая его расположение, способ резервного копирования, параметры архивирования и т. д. На большинстве серверов баз данных работает только один кластер PostgreSQL, поэтому достаточно одной stanza. На серверах резервного копирования требуется отдельная stanza для каждого кластера, резервные копии которого нужно создавать.

Может возникнуть желание назвать stanza по имени первичного кластера, но лучше выбрать имя, описывающее базы данных этого кластера. Поскольку имя stanza будет использоваться для первичного сервера и всех реплик, уместнее выбрать имя, отражающее назначение кластера, например app или dw, а не локальное имя кластера, например main или prod.

Имя «demo» точно отражает назначение этого кластера, поэтому подходит и в качестве имени stanza.

pgBackRest должен знать расположение основного каталога данных кластера PostgreSQL. Путь можно запросить непосредственно у PostgreSQL, но при восстановлении процесс PostgreSQL будет недоступен. Во время резервного копирования значение, переданное pgBackRest, сравнивается с путём, который использует работающий PostgreSQL: они должны совпадать, иначе резервное копирование завершится ошибкой. Убедитесь, что `pg-path` в точности совпадает с data_directory, возвращаемым PostgreSQL.

По умолчанию RHEL хранит кластеры в `/var/lib/pgsql/[version]/data`, поэтому правильный путь к каталогу данных определить легко.

При создании файла `/etc/pgbackrest/pgbackrest.conf` владелец базы данных (обычно `postgres`) должен получить права на его чтение.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить каталог данных кластера PostgreSQL

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data
```

Файлы конфигурации pgBackRest используют формат, похожий на INI в Windows. Секции обозначаются текстом в квадратных скобках, каждая секция содержит пары ключ/значение. Строки, начинающиеся с `#`, игнорируются и могут использоваться как комментарии, но комментарии после значения в той же строке не поддерживаются. Кавычки не поддерживаются, пробельные символы по краям ключей и значений удаляются. Повторно встречающиеся секции объединяются.

Файлы конфигурации pgBackRest могут загружаться несколькими способами:

- `config` и `config-include-path` имеют значения по умолчанию: загружается файл конфигурации по умолчанию, если он существует, затем добавляются файлы `*.conf` из каталога включаемой конфигурации по умолчанию, если они существуют.
- Указан параметр `config`: загружается только указанный файл конфигурации; он должен существовать.
- Указан `config-include-path`: загружаются файлы `*.conf` из каталога включаемой конфигурации; сам каталог должен существовать. Файл конфигурации по умолчанию загружается, если он существует. Чтобы загрузить только файлы из указанного каталога включаемой конфигурации, можно также передать параметр `--no-config`.
- Указаны `config` и `config-include-path`: используются заданные пользователем значения; загружается файл конфигурации, затем добавляются файлы `*.conf` из каталога включаемой конфигурации. Файлы должны существовать.
- Указан `config-path`: эта настройка переопределяет базовый путь к файлу конфигурации по умолчанию и/или базовый путь настройки config-include-path по умолчанию, если параметры config и/или config-include-path не заданы явно.

Файлы объединяются так, как если бы это был один большой файл, причём каждый файл должен быть корректен сам по себе. Поэтому в каждом файле необходимо указывать секции, в которых должны храниться пары ключ/значение. Порядок не важен, но приоритет зависит от секции. Приоритет от высшего к низшему:

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

ПРИМЕЧАНИЕ:

`--config`, `--config-include-path` и `--config-path` доступны только в командной строке.

pgBackRest также можно настраивать через переменные среды (пример ниже); эти переменные действуют для таких команд, как [backup](/ru/docs/pgbackrest/command/backup/), [restore](/ru/docs/pgbackrest/command/restore/) и [archive-push](/ru/docs/pgbackrest/command/archive-push/).

pg-primary **⇒** Настроить `log-path` через переменную среды

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.59.3 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### Создание репозитория {#create-the-repository}

Репозиторий — место, где pgBackRest хранит резервные копии и архивирует сегменты WAL.

Заранее оценить необходимое место может быть непросто. Лучше всего создать несколько резервных копий, записать размеры копий разных типов (full/incr/diff) и измерить объём WAL, создаваемый за сутки. Это даст общее представление о требуемом месте, хотя со временем требования, скорее всего, будут меняться по мере развития базы данных.

В этом примере репозиторий будет храниться на том же сервере, что и PostgreSQL. Это простейшая конфигурация; она полезна, когда для резервного копирования сервера баз данных используется обычное ПО резервного копирования.

pg-primary **⇒** Создать репозиторий pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

Путь к репозиторию необходимо настроить, чтобы pgBackRest знал, где его искать.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить путь к репозиторию pgBackRest

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest
```

Можно настроить и несколько репозиториев. Подробности см. в разделе [Несколько репозиториев](#multiple-repositories).

### Настройка архивирования {#configure-archiving}

Для резервного копирования работающего кластера PostgreSQL должно быть включено архивирование WAL. Через `%p` PostgreSQL указывает расположение сегмента WAL, который нужно архивировать. Обратите внимание: в ходе резервного копирования создаётся *как минимум* один сегмент WAL, даже если в кластер явно ничего не записывается.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Настроить параметры архивирования

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

После внесения этих изменений и перед резервным копированием кластер PostgreSQL необходимо перезапустить.

pg-primary **⇒** Перезапустить демонстрационный кластер

```bash
sudo systemctl restart postgresql-14.service
```

Настройка `hot_standby` включена по умолчанию; её следует оставлять включённой на всех кластерах. В дальнейшем любой кластер может быть восстановлен как резервный, например первичный сервер, заново созданный в качестве резервного после переключения при отказе. Без этой настройки резервный сервер не принимает соединения для чтения.

Если ожидается, что архивирование сегмента WAL в репозиторий pgBackRest займёт более 60 секунд (значение по умолчанию), следует увеличить параметр pgBackRest `archive-timeout`. Это не то же самое, что параметр PostgreSQL archive_timeout, который принудительно переключает сегмент WAL и полезен для баз данных с длительными периодами отсутствия активности. Дополнительные сведения о параметре PostgreSQL archive_timeout см. в разделе [Журнал предзаписи](https://www.postgresql.org/docs/current/static/runtime-config-wal.html) документации PostgreSQL.

Для команды `archive-push` можно задать отдельные параметры. Например, меньший уровень сжатия может ускорить архивирование, не влияя на сжатие резервных копий.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `archive-push` на меньший уровень сжатия

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

Этот способ настройки применим к любой команде и даже к конкретной stanza, например `demo:archive-push`.

### Настройка срока хранения {#configure-retention}

pgBackRest удаляет устаревшие резервные копии на основании параметров срока хранения.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить хранение 2 полных резервных копий

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

Дополнительные сведения приведены в разделе [Срок хранения](#retention).

### Настройка шифрования репозитория {#configure-repository-encryption}

Для демонстрации шифрования в репозитории будут настроены тип шифра и ключ. Шифрование всегда выполняется на стороне клиента, даже если тип репозитория (например, S3 или другое объектное хранилище) поддерживает шифрование.

В качестве ключа шифрования важно использовать длинную случайную парольную фразу. Подходящий способ её создания — команда `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить шифрование репозитория pgBackRest

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

ПРИМЕЧАНИЕ:

Выше настройки шифрования размещены в секции `[global]`, чтобы команда `info` могла читать все stanza. Без параметра `stanza` команда `info` читает настройки шифрования только из секции `[global]`, поэтому при настройке шифрования для отдельных stanza для чтения зашифрованной stanza требуется параметр `stanza`.

После настройки репозитория, создания и проверки stanza изменить настройки шифрования репозитория нельзя.

### Создание stanza {#create-the-stanza}

Для инициализации stanza необходимо выполнить команду `stanza-create`. После `stanza-create` рекомендуется выполнить `check`, чтобы убедиться в правильной настройке архивирования и резервного копирования.

pg-primary **⇒** Создать stanza и проверить конфигурацию

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1200-90682d35 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### Проверка конфигурации {#check-the-configuration}

Команда `check` проверяет, правильно ли настроены pgBackRest и параметр archive_command для архивирования и резервного копирования указанной stanza. Она попытается проверить все репозитории и базы данных, настроенные для сервера, на котором выполняется. Команда выявляет ошибки конфигурации, особенно архивирования, из-за которых резервные копии оказываются неполными, поскольку необходимые сегменты WAL не попали в архив. Команду можно выполнять на сервере PostgreSQL или сервере репозитория. Её также можно выполнять на резервном сервере, однако, поскольку на нём нельзя вызвать `pg_switch_xlog()`/`pg_switch_wal()`, в этом случае проверяется только конфигурация репозитория.

Обратите внимание: для принудительного архивирования сегмента WAL в PostgreSQL вызываются `pg_create_restore_point('pgBackRest Archive Check')` и `pg_switch_xlog()`/`pg_switch_wal()`.

pg-primary **⇒** Проверить конфигурацию

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1233-340209f5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000100000000/000000010000000000000001-dac4045f133f7305d6342d81e428e60050928bc4.gz' on repo1
P00   INFO: check command end: completed successfully
```

### Настройка производительности {#performance-tuning}

В pgBackRest есть ряд параметров производительности, которые по умолчанию отключены для сохранения обратной совместимости репозитория. Однако при создании нового репозитория рекомендуется использовать следующие параметры. Их можно применять и к существующему репозиторию, но тогда старые версии pgBackRest не смогут его читать. Эта несовместимость зависит от версии, в которой появилась функция, как указано в списке ниже.

- `compress-type` — определяет алгоритм сжатия для команд `backup` и `archive-push`. По умолчанию используется `gz` (Gzip), но рекомендуется `zst` (Zstandard): он гораздо быстрее и обеспечивает степень сжатия, близкую к `gz`. Значение `zst` поддерживается параметром `compress-type` начиная с [v2.27](/ru/docs/pgbackrest/release/#v227-release-notes). Подробности см. в разделе [Тип сжатия](/ru/docs/pgbackrest/configuration/#compress-type-option---compress-type).
- `repo-bundle` — объединяет небольшие файлы при резервном копировании, экономя место и ускоряя команды `backup` и `restore`, особенно в объектных хранилищах, таких как S3. Параметр `repo-bundle` появился в [v2.39](/ru/docs/pgbackrest/release/#v239-release-notes). Подробности см. в разделе [Пакетирование файлов](#file-bundling).
- `repo-block` — при резервном копировании `diff`/`incr` командой `backup` сохраняет только изменившиеся части файлов, а не файлы целиком. Это экономит место и ускоряет `backup`. Параметр `repo-block` появился в [v2.46](/ru/docs/pgbackrest/release/#v246-release-notes), но рекомендуется как минимум [v2.52.1](/ru/docs/pgbackrest/release/#v2521-release-notes). Подробности см. в разделе [Блочное инкрементное копирование](#block-incremental).

Есть и другие параметры производительности, отключённые по умолчанию, поскольку они требуют дополнительной настройки или значение по умолчанию безопасно, но не оптимально. Эти параметры доступны во всех версиях pgBackRest v2.

- `process-max` — определяет количество процессов, используемых командами. Значение по умолчанию — 1, и оно почти никогда не является подходящим. Каждая команда использует `process-max` по-своему; подробности см. в документации соответствующей команды.
- `archive-async` — архивирует файлы WAL в репозиторий пакетами, что значительно ускоряет архивирование. По умолчанию отключён, поскольку требует создания каталога очереди. Подробности см. в разделе [Асинхронное архивирование](#asynchronous-archiving).
- `backup-standby` — выполняет резервное копирование с резервного сервера вместо первичного, снижая нагрузку на первичный сервер. По умолчанию отключён, поскольку требует дополнительной настройки и наличия одного или нескольких резервных серверов. Подробности см. в разделе [Резервное копирование с резервного сервера](#backup-from-a-standby).

### Создание резервной копии {#perform-a-backup}

По умолчанию pgBackRest перед началом резервного копирования ждёт следующей плановой контрольной точки. В зависимости от настроек checkpoint_timeout и checkpoint_segments в PostgreSQL до завершения контрольной точки и начала резервного копирования может пройти немало времени. Обычно лучше задать `start-fast=y`, чтобы резервное копирование начиналось сразу. Это принудительно создаёт контрольную точку, но, поскольку резервные копии обычно создаются раз в сутки, дополнительная контрольная точка не должна заметно влиять на производительность. Однако на очень нагруженных кластерах может быть лучше передавать `--start-fast` в командной строке по мере необходимости.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить быстрый запуск резервного копирования

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Чтобы создать резервную копию кластера PostgreSQL, запустите pgBackRest с командой `backup`.

pg-primary **⇒** Создать резервную копию демонстрационного кластера

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-185647F
P00   INFO: full backup size = 25.2MB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

По умолчанию pgBackRest пытается создать инкрементную резервную копию. Однако инкрементная копия должна опираться на полную, а поскольку полной копии ещё не было, pgBackRest создал полную копию.

Параметр `type` позволяет явно указать полное или дифференциальное резервное копирование.

pg-primary **⇒** Создать дифференциальную резервную копию демонстрационного кластера

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-185647F_20261002-185651D
P00   INFO: diff backup size = 9.2KB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1398-36e29fed --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

На этот раз предупреждения не было, поскольку полная резервная копия уже существовала. Инкрементные копии могут опираться на полную *или* дифференциальную копию, а дифференциальные должны опираться на полную. Для создания полной копии выполните команду `backup` с `--type=full`.

Во время резервного копирования работающего кластера pgBackRest ожидает архивирования сегментов WAL, необходимых для согласованности резервной копии. Время ожидания задаётся параметром pgBackRest `archive-timeout`, значение которого по умолчанию составляет 60 секунд. Если известно, что архивирование отдельного сегмента занимает больше времени, этот параметр следует увеличить.

### Планирование резервного копирования {#schedule-a-backup}

Резервное копирование можно запускать по расписанию с помощью таких утилит, как cron.

В следующем примере настроены два задания cron: полное резервное копирование каждое воскресенье в 6:30 утра и дифференциальное в 6:30 утра с понедельника по субботу. Если этот crontab устанавливается впервые посреди недели, при первом запуске задания дифференциального копирования pgBackRest создаст полную копию, а на следующий день — дифференциальную.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

После настройки расписания важно настроить срок хранения, чтобы устаревшие копии регулярно удалялись; см. раздел [Срок хранения](#retention).

### Сведения о резервных копиях {#backup-information}

Для получения сведений о резервных копиях используйте команду `info`.

pg-primary **⇒** Получить сведения о демонстрационном кластере

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-185647F
            timestamp start/stop: 2026-10-02 18:56:47+00 / 2026-10-02 18:56:50+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup set size: 3.2MB, backup size: 3.2MB

        diff backup: 20261002-185647F_20261002-185651D
            timestamp start/stop: 2026-10-02 18:56:51+00 / 2026-10-02 18:56:52+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 25.2MB, database backup size: 9.2KB
            repo1: backup set size: 3.2MB, backup size: 864B
            backup reference total: 1 full
```

Команда `info` работает с одной stanza или со всеми stanza. По умолчанию используется текстовый вывод, который содержит удобную для чтения сводку резервных копий запрошенных stanza. Этот формат может измениться в любом выпуске.

Для машиночитаемого вывода используйте `--output=json`. Вывод JSON содержит намного больше сведений, чем текстовый, и остаётся стабильным, если только не обнаружена ошибка.

Чтобы ускорить выполнение, ограничьте вывод сведениями о ходе выполнения, указав `--detail-level=progress`. При этом пропускаются все проверки, кроме проверки доступности stanza.

Для каждой stanza выводится отдельный раздел; параметром `--stanza` можно ограничить вывод одной stanza. Поле «`status`» кратко отражает состояние stanza. Значение «`ok`» означает, что pgBackRest работает нормально. При наличии нескольких репозиториев статус «`mixed`» указывает на проблемы со stanza в одном или нескольких репозиториях; в этом случае её состояние подробно приводится для каждого репозитория. Если ошибка репозитория не соответствует ни одному из известных кодов ошибок, используется код «`other`» и выводятся полные сведения об ошибке. Поле «`wal archive min/max`» показывает минимальный и максимальный WAL, хранящиеся в архиве; при наличии нескольких репозиториев оно охватывает их все, если не задан параметр `--repo`. Учтите, что из-за политик срока хранения архива или по другим причинам в последовательности могут быть пропуски.

Если на сервере сейчас выполняется одна из соответствующих команд, рядом со сведениями «`status`» появляются сообщения «`backup/expire running`» и/или «`restore running`». В текстовом выводе также отображается ход выполнения по каждому репозиторию, а в вывод JSON добавляется массив «`repo`».

Резервные копии выводятся от старых к новым. Самая старая копия *всегда* полная (обозначается `F` в конце метки), а самая новая может быть полной, дифференциальной (метка оканчивается на `D`) или инкрементной (оканчивается на `I`).

Поле «`timestamp start/stop`» задаёт период выполнения резервного копирования. По «`timestamp stop`» можно выбрать копию для восстановления на определённый момент времени. Дополнительные сведения приведены в разделе [Восстановление на определённый момент времени](#point-in-time-recovery).

Поле «`wal start/stop`» определяет диапазон WAL, необходимый для приведения базы данных в согласованное состояние при восстановлении. Перед завершением команда `backup` убеждается, что этот диапазон WAL есть в архиве.

Поле «`database size`» — полный размер базы данных без сжатия, а «`database backup size`» — объём данных базы, которые фактически нужно скопировать (для полных копий эти значения совпадают).

Поле «`repo`» указывает, в каком репозитории находится копия. Поле «`backup set size`» включает все файлы этой копии и тех копий репозитория, на которые она ссылается и которые необходимы для восстановления базы данных из неё, а «`backup size`» — только файлы самой этой копии (для полных копий эти значения также совпадают). Если в pgBackRest включено сжатие, размеры в репозитории учитывают сжатый размер файлов.

Поле «`backup reference total`» содержит сводку дополнительных резервных копий, необходимых для восстановления этой копии. Чтобы вывести полный список ссылок, используйте параметр `--set`.

### Восстановление резервной копии {#restore-a-backup}

Резервные копии защищают от ряда аварийных ситуаций; наиболее распространены аппаратные сбои и повреждение данных. Простейший способ имитировать повреждение данных — удалить важный файл кластера PostgreSQL.

pg-primary **⇒** Остановить демонстрационный кластер и удалить файл `pg_control`

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres rm /var/lib/pgsql/14/data/global/pg_control
```

При запуске кластера без этого важного файла возникнет ошибка.

pg-primary **⇒** Попытаться запустить повреждённый демонстрационный кластер

```bash
sudo systemctl start postgresql-14.service
sudo systemctl status postgresql-14.service
```

```text
postgresql-14.service - PostgreSQL 14 database server
    Loaded: loaded (/usr/lib/systemd/system/postgresql-14.service, disabled)
    Active: failed (failed)
```

Чтобы восстановить резервную копию кластера PostgreSQL, запустите pgBackRest с командой `restore`. Кластер необходимо остановить (в данном случае он уже остановлен), а из каталога данных PostgreSQL удалить все файлы.

pg-primary **⇒** Удалить старые файлы демонстрационного кластера

```bash
sudo -u postgres find /var/lib/pgsql/14/data -mindepth 1 -delete
```

pg-primary **⇒** Восстановить демонстрационный кластер и запустить PostgreSQL

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo systemctl start postgresql-14.service
```

На этот раз кластер успешно запустился, поскольку при восстановлении был возвращён отсутствующий файл `pg_control`.

Дополнительные сведения о команде `restore` приведены в разделе [Восстановление](#restore-1).

--------

## Мониторинг {#monitoring}

Мониторинг — важная часть любой рабочей системы. Доступно множество инструментов, и с небольшой доработкой любой из них можно использовать для мониторинга pgBackRest.

pgBackRest может выводить сведения о репозитории в формате JSON, включая список всех резервных копий для каждой stanza и сведения об архиве WAL.

### В PostgreSQL {#in-postgresql}

Команда PostgreSQL `COPY` позволяет загрузить сведения pgBackRest в таблицу. В следующем примере эта логика оформлена как функция, с помощью которой можно выполнять запросы в реальном времени.

pg-primary **⇒** Загрузить функцию получения сведений pgBackRest для PostgreSQL

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

Теперь с помощью функции `monitor.pgbackrest_info()` можно узнать время последней успешной резервной копии и архивированный WAL для stanza.

pg-primary **⇒** Запросить время последней успешной резервной копии и архивированный WAL

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 18:56:52+00 | 000000010000000000000005
(1 row)
```

--------

## Резервное копирование {#backup-1}

Если настроено несколько репозиториев, pgBackRest создаёт резервную копию в репозитории с наивысшим приоритетом (например, `repo1`), если не указан параметр `--repo`.

У pgBackRest нет встроенного планировщика, поэтому лучше запускать его из cron или другого планировщика.

Дополнительные сведения и примеры см. в разделе [Создание резервной копии](#perform-a-backup).

### Пакетирование файлов {#file-bundling}

Объединение файлов в пакеты в репозитории экономит время резервного копирования и часть места в репозитории. Это особенно заметно, когда репозиторий находится в объектном хранилище, таком как S3, или в файловой системе с большим размером блока. Создание отдельного файла в объектном хранилище занимает больше времени, а хранение очень маленьких файлов может стоить столько же, сколько хранение более крупных.

Пакетирование файлов включается параметром `repo-bundle`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-bundle`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Без пакетирования файлов каталог полной резервной копии содержит 1000+ файлов, а с пакетированием их общее количество значительно уменьшается. Дополнительное преимущество: файлы нулевой длины не сохраняются (кроме записи в манифесте), тогда как при обычном резервном копировании каждый такой файл хранится отдельно.

pg-primary **⇒** Создать полную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** Проверить общее количество файлов

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

Для настройки можно использовать параметры `repo-bundle-size` и `repo-bundle-limit`, хотя значения по умолчанию должны быть оптимальными в большинстве случаев.

Хотя пакетирование файлов обычно эффективнее, оно затрудняет ручное извлечение файлов из репозитория. Для хранилища с дедупликацией оно может быть не лучшим выбором: каждая полная резервная копия размещает файлы в пакетах по-разному. Наконец, копирование пакетов файлов нельзя возобновить, поэтому не следует задавать слишком большое значение `repo-bundle-limit`.

### Блочное инкрементное копирование {#block-incremental}

Блочные инкрементные резервные копии экономят место: сохраняются лишь части файла, изменившиеся после предыдущей резервной копии, а не весь файл.

Блочное инкрементное копирование включается параметром `repo-block` и наиболее эффективно, когда включено для всех типов резервных копий. Пакетирование файлов также должно быть включено.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-block`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

### Аннотации резервных копий {#backup-annotations}

К резервной копии можно прикреплять информационные пары ключ/значение. Этот параметр можно указать несколько раз, чтобы добавить несколько аннотаций.

pg-primary **⇒** Создать полную резервную копию с аннотациями

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

В текстовом выводе команды `info` аннотации отображаются, когда резервная копия указана через `--set`; в выводе JSON они присутствуют всегда.

pg-primary **⇒** Получить сведения о демонстрационном кластере

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                key: value
                source: demo backup
```

Аннотации, заданные в команде `backup`, впоследствии можно добавлять, изменять или удалять с помощью команды `annotate`.

pg-primary **⇒** Изменить аннотации резервной копии

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## Срок хранения {#retention}

Обычно лучше хранить как можно больше резервных копий, чтобы расширить доступный интервал [восстановления на определённый момент времени](#point-in-time-recovery), но необходимо учитывать и практические ограничения, например объём диска. Параметры срока хранения позволяют удалять старые копии, когда они больше не нужны.

pgBackRest выполняет ротацию полных резервных копий в зависимости от типа срока хранения: по количеству или по периоду времени. Если задано количество, при удалении учитывается не время создания копий, а то, сколько их нужно сохранить. Дифференциальные копии хранятся по количеству, но всегда удаляются при удалении полной копии, от которой зависят. Инкрементные копии не удаляются по сроку хранения независимо: они всегда удаляются вместе со связанной полной или дифференциальной копией. Подробности и примеры см. в разделах [Хранение полных резервных копий](#full-backup-retention) и [Хранение дифференциальных резервных копий](#differential-backup-retention).

По умолчанию архивированный WAL сохраняется для резервных копий, срок хранения которых не истёк. Этот порядок можно изменить отдельно для каждого репозитория параметрами retention-archive, хотя делать это не рекомендуется. Подробности и примеры см. в разделе [Хранение архива](#archive-retention).

Команда `expire` автоматически выполняется после каждого успешного резервного копирования; её также может запускать пользователь. При ручном запуске удаление выполняется в соответствии с настройками срока хранения каждого настроенного репозитория. Если передан параметр `--repo`, удаление выполняется только в указанном репозитории. Пользователь может также ограничить удаление конкретным набором резервной копии с помощью `--set`; если при этом не указан `--repo`, поиск выполняется во всех репозиториях и удаляются все совпадающие наборы. Следует учитывать, что при каждом запуске `expire` проверяется и применяется политика хранения архива.

### Хранение полных резервных копий {#full-backup-retention}

Параметр `repo1-retention-full-type` определяет, как интерпретировать `repo1-retention-full`: как количество сохраняемых полных резервных копий или как число дней их хранения. Удаление выполняется только после завершения новых резервных копий. То есть при `repo1-retention-full-type=count` и `repo1-retention-full=2` перед удалением самой старой копии будут храниться три полные копии; при `repo1-retention-full-type=time` и `repo1-retention-full=20` для начала удаления должна существовать хотя бы одна полная копия возрастом не менее 20 дней.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-retention-full`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Для резервного копирования задано `repo1-retention-full=2`, но пока существует только одна полная копия, поэтому создание следующей полной копии не приведёт к удалению полных копий.

pg-primary **⇒** Создать полную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 963 lines of output]
P00   INFO: repo1: remove expired backup 20261002-185706F
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185708F, start = 000000020000000000000008
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

Архив *удаляется*, поскольку сегменты WAL были созданы до самой старой резервной копии. Для восстановления они бесполезны: восстановить копию можно только с помощью сегментов WAL, созданных после неё.

pg-primary **⇒** Создать полную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-185708F
P00   INFO: repo1: remove expired backup 20261002-185708F
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000008, stop = 000000020000000000000009
P00   INFO: expire command end: completed successfully
```

Полная резервная копия `20261002-185647F` удаляется, а хранение архива теперь определяется копией `20261002-185711F`, которая стала самой старой полной копией.

### Хранение дифференциальных резервных копий {#differential-backup-retention}

Установите `repo1-retention-diff` равным нужному количеству дифференциальных резервных копий. Дифференциальные копии зависят только от предыдущей полной копии, поэтому можно создать «скользящий» набор дифференциальных копий за последние сутки или более длительный период. Это обеспечивает быстрое восстановление на недавние моменты времени и при этом уменьшает общий расход места.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=1

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Для резервного копирования задано `repo1-retention-diff=1`, поэтому прежде, чем одна дифференциальная копия будет удалена, нужно создать две. Для демонстрации удаления инкрементной копии добавляется инкрементное резервное копирование; в данном случае её удаление зависит от удаления дифференциальной копии.

pg-primary **⇒** Создать дифференциальную и инкрементную резервные копии

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Теперь создание дифференциальной резервной копии приведёт к удалению предыдущих дифференциальной и инкрементной копий, оставив только одну дифференциальную.

pg-primary **⇒** Создать дифференциальную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=2641-6abf9293 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-185713F_20261002-185715D, 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185715D
P00   INFO: expire command end: completed successfully
```

### Хранение архива {#archive-retention}

Хотя pgBackRest автоматически удаляет архивированные сегменты WAL при удалении устаревших резервных копий (по умолчанию WAL полных копий удаляется на основании параметра `repo1-retention-full`), для экономии дискового пространства может быть полезно удалять архив более активно. При хранении архива дифференциальных копий полные копии также считаются дифференциальными.

При удалении архива никогда не удаляются сегменты WAL, необходимые для согласованности резервной копии. Однако восстановление на определённый момент времени (PITR) возможно только при непрерывном потоке WAL, поэтому при агрессивном удалении архива вне обычного процесса удаления резервных копий следует соблюдать осторожность. Чтобы узнать, что будет удалено, ничего фактически не удаляя, можно передать в командной строке параметр `dry-run` команде `expire`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

pg-primary **⇒** Создать дифференциальную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261002-185713F_20261002-185719D
P00   INFO: diff backup size = 11.5KB, file total = 951
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** Удалить устаревший архив

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=2877-3548ad61 --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185711F, start = 00000002000000000000000A, stop = 00000002000000000000000B
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185717D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185719D, start = 000000020000000000000016
P00   INFO: repo1: 14-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

У дифференциальной копии `20261002-185713F_20261002-185717D` есть архивированные сегменты WAL, которые необходимо сохранить для согласованности старых копий, хотя продвинуть их дальше с помощью PITR уже нельзя. Сегменты WAL, созданные после `20261002-185713F_20261002-185717D`, но до `20261002-185713F_20261002-185719D`, удаляются. Сегменты, созданные после новой копии `20261002-185713F_20261002-185719D`, остаются и могут использоваться для PITR.

Поскольку при хранении архива дифференциальных копий полные копии считаются дифференциальными, если теперь создать полную копию с теми же настройками, для PITR останется только архив этой полной копии.

--------

## Восстановление {#restore-1}

По умолчанию команда восстановления автоматически выбирает последнюю резервную копию из первого репозитория, в котором есть копии (см. [Быстрый старт — Восстановление резервной копии](#restore-a-backup)). Порядок проверки репозиториев определяется файлом `pgbackrest.conf` (например, repo1 проверяется раньше repo2). Для выбора конкретного репозитория можно передать `--repo` (например, `--repo=1`). Если нужна не последняя резервная копия, можно передать параметр `--set`.

При PITR с `--type=time` или `--type=lsn` целевое время или LSN необходимо указать с помощью параметра `--target`. Если `--set` не задан, настроенные репозитории проверяются по порядку: выбирается резервная копия, время завершения которой предшествует целевому времени или LSN завершения которой меньше либо равен целевому LSN. Если подходящая копия не найдена, pgBackRest выдаёт ошибку как для `--type=time`, так и для `--type=lsn`; перехода к последней резервной копии не происходит. Для других типов PITR, например `xid`, необходимо указать параметр `--set`, если цель предшествует последней резервной копии. Подробнее и с примерами см. [Восстановление на заданный момент времени](#point-in-time-recovery).

В соответствии с рекомендацией PostgreSQL слоты репликации не включаются в резервную копию. Дополнительные сведения см. в разделе [Резервное копирование каталога данных](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) документации PostgreSQL.

В следующих разделах рассматриваются дополнительные возможности команды `restore`.

### Владельцы файлов {#file-ownership}

Если `restore` выполняется от имени пользователя, отличного от root (обычный случай), все восстановленные файлы будут принадлежать пользователю и группе, от имени которых запущен pgBackRest. Если существующие файлы принадлежат другому пользователю или группе и сменить владельца на пользователя и группу процесса не удаётся, возникает ошибка. В этом случае перед повторной попыткой восстановления привилегированный пользователь должен изменить владельца файлов.

Если `restore` выполняется от имени `root`, pgBackRest пытается восстановить владельцев, записанных в манифест при создании резервной копии. В манифесте хранятся только **имена** пользователей и групп, поэтому на сервере восстановления должны существовать те же имена. Если имя пользователя или группы локально не найдено, используется пользователь или группа каталога данных PostgreSQL, а если их не удаётся сопоставить с именем — `root`.

### Параметр delta {#delta-option}

В разделе [Восстановление резервной копии](#restore-a-backup) главы [Быстрый старт](#quick-start) перед выполнением `restore` требовалось очистить каталог кластера баз данных. Параметр `delta` позволяет pgBackRest автоматически определить, какие файлы в каталоге кластера можно сохранить, а какие нужно восстановить из резервной копии. Он также *удаляет* файлы, отсутствующие в манифесте копии, устраняя расходящиеся изменения. Для этого вычисляется криптографический хеш [SHA-1](https://en.wikipedia.org/wiki/SHA-1) каждого файла в каталоге кластера. Если хеш `SHA-1` не совпадает с хешем в резервной копии, файл восстанавливается. Эта операция очень эффективна в сочетании с параметром `process-max`. Поскольку на время восстановления сервер PostgreSQL остановлен, можно использовать больше процессов, чем было бы желательно при резервном копировании работающего сервера PostgreSQL.

pg-primary **⇒** Остановить демонстрационный кластер и выполнить дельта-восстановление

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/pgsql/14/data' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/base/13755/pg_internal.init'
       [filtered 996 lines of output]
```

pg-primary **⇒** Перезапустить PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

### Восстановление выбранных баз данных {#restore-selected-databases}

Иногда требуется выборочно восстановить отдельные базы данных из резервной копии кластера. Это может понадобиться для повышения производительности или для переноса выбранных баз на машину, где недостаточно места для восстановления всего кластера.

Для демонстрации этой возможности создаются две базы данных: test1 и test2.

pg-primary **⇒** Создать две тестовые базы данных

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

В каждой тестовой базе будут созданы таблицы и данные, чтобы показать, что восстановление работает и при выборочном восстановлении.

pg-primary **⇒** Создать тестовую таблицу в каждой базе данных

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

Создаётся новая резервная копия, чтобы pgBackRest получил сведения о новых базах данных.

pg-primary **⇒** Создать резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Одна из основных причин использовать выборочное восстановление — экономия места. Здесь показан размер базы test1, чтобы его можно было сравнить с расходом дискового пространства после выборочного восстановления.

pg-primary **⇒** Показать место, занимаемое базой test1

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.4M	/var/lib/pgsql/14/data/base/32768
```

Если неизвестно, какую базу данных нужно восстановить, используйте параметр `set` команды `info`, чтобы узнать, какие базы входят в набор резервной копии.

pg-primary **⇒** Показать список баз данных в резервной копии

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-185713F_20261002-185728I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 2.1MB
            backup reference list: 20261002-185713F, 20261002-185713F_20261002-185719D
            database list: postgres (13755), test1 (32768), test2 (32769)
```

Остановите кластер и восстановите только базу test2. Встроенные базы (`template0`, `template1` и `postgres`) восстанавливаются всегда.

ПРЕДУПРЕЖДЕНИЕ:

Если не указать `--type=immediate`, восстановление может завершиться ошибкой. Причина в том, что после достижения согласованности PostgreSQL считает обнулённые страницы ошибкой даже при записи полной страницы. В PostgreSQL ≥ 13 можно использовать настройку ignore_invalid_pages, чтобы игнорировать некорректные страницы. В этом случае после восстановления важно проверить журналы и убедиться, что сообщений о некорректных страницах в выбранных базах данных нет.

pg-primary **⇒** Восстановить последнюю резервную копию, включив только базу test2

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo systemctl start postgresql-14.service
```

После завершения восстановления база test2 будет содержать все ранее созданные таблицы и данные.

pg-primary **⇒** Продемонстрировать восстановление базы test2

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

База test1, несмотря на успешное восстановление, недоступна. Причина в том, что вся база была восстановлена в виде разреженных обнулённых файлов. PostgreSQL может успешно применить WAL к таким файлам, но база в целом будет некорректна, поскольку ключевые файлы не содержат данных. Это сделано намеренно, чтобы исключить случайное использование базы, которая может содержать лишь часть данных, применённых при воспроизведении WAL.

pg-primary **⇒** Попытка подключиться к базе test1 приведёт к ошибке

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

Поскольку база test1 восстанавливается в виде разреженных обнулённых файлов, она займёт лишь столько места, сколько WAL будет записано при восстановлении. Объём WAL, создаваемого во время резервного копирования и применяемого при восстановлении, может быть значительным, но обычно составляет небольшую долю полного размера базы, особенно для крупных баз, где эта возможность наиболее полезна.

Очевидно, что при выборочном восстановлении база test1 занимает гораздо меньше места, чем при полном восстановлении базы.

pg-primary **⇒** Показать место, занимаемое базой test1 после восстановления

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.0K	/var/lib/pgsql/14/data/base/32768
```

На этом этапе единственное действие, которое можно выполнить с некорректной базой test1, — `drop database`. pgBackRest не удаляет базу автоматически, поскольку это невозможно до завершения восстановления и появления доступа к кластеру.

pg-primary **⇒** Удалить базу test1

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

После удаления некорректной базы test1 остаются только test2 и встроенные базы.

pg-primary **⇒** Показать оставшиеся базы данных

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
 13754 | template0
 13755 | postgres
 32769 | test2
(4 rows)
```

--------

## Восстановление на определённый момент времени {#point-in-time-recovery}

В разделе [Восстановление резервной копии](#restore-a-backup) главы [Быстрый старт](#quick-start) использовалось восстановление по умолчанию — воспроизведение WAL до самого конца потока. При аппаратном сбое это обычно лучший вариант, но при повреждении данных, вызванном машиной или человеком, часто уместнее восстановление на определённый момент времени (PITR).

Восстановление на определённый момент времени (PITR) позволяет воспроизвести WAL из резервной копии до заданного LSN, времени, идентификатора транзакции или точки восстановления. В типичных сценариях восстановление по времени, пожалуй, наиболее полезно. Частый случай — восстановление случайно удалённой таблицы или данных. Восстановление удалённой таблицы нагляднее, поэтому здесь используется именно такой пример, но удалённые данные восстанавливаются точно так же.

pg-primary **⇒** Создать таблицу с очень важными данными

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Важно задавать время так, как его понимает PostgreSQL, и включать смещение часового пояса. Это уменьшает вероятность нежелательного преобразования часовых поясов и неожиданного результата восстановления.

pg-primary **⇒** Получить время из PostgreSQL

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 18:57:39.575732+00
```

Теперь, когда время записано, таблица удаляется. На практике определить точное время удаления таблицы гораздо труднее, чем в этом примере. Точное время может оказаться неизвестным, но некоторое исследование должно позволить достаточно близко его оценить.

pg-primary **⇒** Удалить важную таблицу

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

Если для восстановления выбрана неверная резервная копия, восстановление на нужный момент времени завершится неудачей. Для демонстрации создаётся новая инкрементная копия, в которой `important_table` уже отсутствует.

pg-primary **⇒** Создать инкрементную резервную копию

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-185713F_20261002-185741I
            timestamp start/stop: 2026-10-02 18:57:41+00 / 2026-10-02 18:57:42+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

Восстановить потерянную таблицу из этой копии не получится, поскольку PostgreSQL может воспроизводить изменения только вперёд, но не назад.

pg-primary **⇒** Попытаться восстановить данные из неподходящей резервной копии

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-185713F_20261002-185741I --target-timeline=current \
       --type=time "--target=2026-10-02 18:57:39.575732+00" --target-action=promote restore
sudo systemctl start postgresql-14.service
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 11 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000100 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.01 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 4045) exited with exit code 1
LOG:  terminating any other active server processes
LOG:  database system is shut down
```

Надёжный способ — позволить pgBackRest автоматически выбрать копию, из которой возможно восстановление на целевой момент времени, то есть копию, завершившуюся до указанного времени.

ПРИМЕЧАНИЕ:

pgBackRest не может автоматически выбрать копию при типе восстановления `xid` или `name`.

pg-primary **⇒** Восстановить демонстрационный кластер на момент `2026-10-02 18:57:39.575732+00`

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 18:57:39.575732+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 18:57:39.575732+00'
recovery_target_action = 'promote'
```

pgBackRest сформировал настройки восстановления в `postgresql.auto.conf`, поэтому PostgreSQL можно запустить сразу. Через `%f` PostgreSQL указывает нужный сегмент WAL, а через `%p` — место, куда его следует скопировать. После того как PostgreSQL завершит восстановление, таблица снова будет существовать и к ней можно будет обращаться с запросами.

pg-primary **⇒** Запустить PostgreSQL и проверить наличие важной таблицы

```bash
sudo systemctl start postgresql-14.service
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

Журнал PostgreSQL также содержит полезные сведения. В нём указаны время и транзакция, на которых остановилось восстановление, а также время последней применённой транзакции.

pg-primary **⇒** Просмотреть журнал PostgreSQL

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 5 lines of output]
LOG:  database system was interrupted; last known up at 2026-10-02 18:57:28 UTC
LOG:  restored log file "00000004.history" from archive
LOG:  starting point-in-time recovery to 2026-10-02 18:57:39.575732+00
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
       [filtered 2 lines of output]
LOG:  consistent recovery state reached at 0/19000100
LOG:  database system is ready to accept read-only connections
LOG:  recovery stopping before commit of transaction 743, time 2026-10-02 18:57:40.904112+00
LOG:  redo done at 0/1901E6C0 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
LOG:  last completed transaction was at log time 2026-10-02 18:57:38.228184+00
LOG:  selected new timeline ID: 5
LOG:  archive recovery complete
LOG:  database system is ready to accept connections
```

--------

## Удаление stanza {#delete-a-stanza}

Команда `stanza-delete` удаляет из репозитория данные, связанные со stanza.

ПРЕДУПРЕЖДЕНИЕ:

Используйте эту команду с осторожностью: она безвозвратно удаляет из репозитория pgBackRest все резервные копии и архивы указанной stanza.

Чтобы удалить stanza:

- Остановите кластер PostgreSQL, связанный со stanza (или используйте --force для обхода этого требования).
- Выполните команду `stop` на сервере, где будет запущена `stanza-delete`.
- Выполните команду `stanza-delete`.

После успешного завершения команды пользователь должен самостоятельно удалить stanza из всех файлов конфигурации pgBackRest и/или переменных среды.

За один раз stanza можно удалить только из одного репозитория. Чтобы удалить stanza из нескольких репозиториев, повторите команду `stanza-delete` для каждого из них, указав параметр `--repo`.

pg-primary **⇒** Остановить удаляемый кластер PostgreSQL

```bash
sudo systemctl stop postgresql-14.service
```

pg-primary **⇒** Остановить pgBackRest для stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=4396-32c67a63 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** Удалить stanza из одного репозитория

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=4428-6f4dadb2 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## Несколько репозиториев {#multiple-repositories}

Можно настроить несколько репозиториев, как показано в разделе [Поддержка S3](#s3-compatible-object-store-support). Одно из возможных преимуществ — локальный репозиторий для быстрого восстановления и удалённый для избыточности.

Некоторые команды, например [`stanza-create`](/ru/docs/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/ru/docs/pgbackrest/command/stanza-upgrade/), автоматически работают со всеми настроенными репозиториями. Для других, например [`stanza-delete`](/ru/docs/pgbackrest/command/stanza-delete/), репозиторий нужно указать параметром `repo`.

Для обратной совместимости параметр `repo` не требуется, если настроен только `repo1`. Однако, если единственный репозиторий настроен, например, как `repo2`, параметр `repo` *обязателен*. Это позволяет избежать нарушения работы команд при последующем добавлении нового репозитория.

Команда `archive-push` всегда отправляет WAL в архивы всех настроенных репозиториев. Если один репозиторий недоступен, WAL всё равно отправляется в остальные. Однако для эффективной работы необходимо включить `archive-async=y`; иначе остальные репозитории смогут опередить недоступный лишь на один сегмент WAL. Также учтите: если WAL не удаётся отправить в какой-либо репозиторий, PostgreSQL не удалит его из каталога `pg_wal`, из-за чего на томе может закончиться место.

Для каждого репозитория нужно отдельно задать расписание резервного копирования. Во многих случаях это удобно, поскольку типы копий и сроки хранения различаются между репозиториями. Аналогично, при восстановлении необходимо указать репозиторий. Обычно для восстановления лучше выбирать репозиторий с низкой задержкой или стоимостью, даже если само восстановление займёт больше времени. Определить наиболее эффективный репозиторий можно только испытаниями восстановления.

--------

## Поддержка объектных хранилищ, совместимых с Azure {#azure-compatible-object-store-support}

pgBackRest поддерживает размещение репозиториев в объектных хранилищах, совместимых с Azure. Контейнер для репозитория необходимо создать заранее: pgBackRest не создаёт его автоматически. Репозиторий можно разместить в корне контейнера (`/`), но обычно лучше использовать вложенный путь, чтобы в том же контейнере можно было хранить журналы объектного хранилища и другие данные без конфликтов.

ПРЕДУПРЕЖДЕНИЕ:

Не включайте «иерархическое пространство имён»: это приведёт к ошибкам при удалении устаревших копий.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить Azure

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

start-fast=y



[global:archive-push]

compress-level=3
```

Для использования подписей общего доступа задайте параметру `repo2-azure-key-type` значение `sas`, а параметру `repo2-azure-key` — токен подписи общего доступа.

Команды выполняются точно так же, как если бы репозиторий находился на локальном диске.

pg-primary **⇒** Создать stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=4635-4a99c6c0 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

Создание файлов в Azure происходит относительно медленно, поэтому включение [пакетирования файлов](#file-bundling) повышает производительность `backup`/`restore`.

pg-primary **⇒** Создать резервную копию демонстрационного кластера

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-185802F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## Поддержка объектных хранилищ, совместимых с S3 {#s3-compatible-object-store-support}

pgBackRest поддерживает размещение репозиториев в объектных хранилищах, совместимых с S3. Бакет для репозитория необходимо создать заранее: pgBackRest не создаёт его автоматически. Репозиторий можно разместить в корне бакета (`/`), но обычно лучше использовать вложенный путь, чтобы в том же бакете можно было хранить журналы объектного хранилища и другие данные без конфликтов.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить S3

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

start-fast=y



[global:archive-push]

compress-level=3
```

ПРИМЕЧАНИЕ:

Регион и конечную точку необходимо настроить в соответствии с расположением бакета. Здесь приведены значения для региона `us-east-1`.

Для запуска pgBackRest следует создать роль, а права доступа к бакету следует максимально ограничить. Если роль связана с экземпляром AWS, при `repo3-s3-key-type=auto` pgBackRest автоматически получает временные учётные данные, поэтому явно задавать ключи в `/etc/pgbackrest/pgbackrest.conf` не требуется.

Этот пример политики Amazon S3 ограничивает все операции чтения и записи указанным бакетом и путём репозитория.

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

Команды выполняются точно так же, как если бы репозиторий находился на локальном диске.

pg-primary **⇒** Создать stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

Создание файлов в S3 происходит относительно медленно, поэтому включение [пакетирования файлов](#file-bundling) повышает производительность `backup`/`restore`.

pg-primary **⇒** Создать резервную копию демонстрационного кластера

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-185820F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## Поддержка SFTP {#sftp-support}

pgBackRest поддерживает размещение репозиториев на серверах SFTP. Передача файлов по SFTP относительно медленная, поэтому увеличение `process-max` для параллельной передачи файлов повышает производительность команд.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить SFTP

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

При использовании SFTP, если libssh2 собрана с OpenSSH, параметр `repo4-sftp-public-key-file` необязателен.

pg-primary **⇒** Создать пару ключей SSH для резервного копирования по SFTP

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/pgsql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/pgsql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** Скопировать открытый ключ pg-primary для резервного копирования по SFTP на sftp-server

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/pgsql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

Команды выполняются точно так же, как если бы репозиторий находился на локальном диске.

pg-primary **⇒** Добавить отпечаток sftp-server в файл known_hosts, поскольку значение `repo4-sftp-host-key-check-type` по умолчанию — «strict»

```bash
ssh-keyscan -H sftp-server >> /var/lib/pgsql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** Создать stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** Создать резервную копию демонстрационного кластера

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-185837F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## Поддержка объектных хранилищ, совместимых с GCS {#gcs-compatible-object-store-support}

pgBackRest поддерживает размещение репозиториев в объектных хранилищах, совместимых с GCS. Бакет для репозитория необходимо создать заранее: pgBackRest не создаёт его автоматически. Репозиторий можно разместить в корне бакета (`/`), но обычно лучше использовать вложенный путь, чтобы в том же бакете можно было хранить журналы объектного хранилища и другие данные без конфликтов.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить GCS

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

repo5-gcs-bucket=demo-bucket

repo5-gcs-key=/etc/pgbackrest/gcs-key.json

repo5-path=/demo-repo

repo5-type=gcs

start-fast=y



[global:archive-push]

compress-level=3
```

При работе в GCE задайте `repo5-gcs-key-type=auto`, чтобы автоматически проходить аутентификацию через служебную учётную запись экземпляра.

Команды выполняются точно так же, как если бы репозиторий находился на локальном диске.

Создание файлов в GCS происходит относительно медленно, поэтому включение [пакетирования файлов](#file-bundling) повышает производительность `backup`/`restore`.

--------

## Целевое время репозитория {#target-time-for-repository}

Целевое время определяет, на какой момент команды читают репозиторий в хранилище с поддержкой версий. Это позволяет прочитать состояние репозитория на определённый момент времени, чтобы восстановить данные, удалённые или повреждённые случайными действиями пользователя либо вредоносной программой.

Хранение версий поддерживается в S3, GCS и Azure, но обычно по умолчанию отключено. Помимо включения версий, может быть полезно включить блокировку объектов в S3 и обратимое удаление в GCS или Azure.

При указании `repo-target-time` также необходимо передать параметр `repo`. Вероятно, не все типы репозиториев поддерживают версии, и в целом для восстановления имеет смысл выбирать один репозиторий.

Обратите внимание: временные метки хранилища сравниваются с указанной меткой по условию <=, а миллисекунды в переданной метке времени отбрасываются.

Для демонстрации этой возможности stanza `demo` удаляется из репозитория S3.

pg-primary **⇒** Удалить stanza из репозитория S3

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

После удаления stanza команда `info` покажет ошибочное состояние репозитория.

pg-primary **⇒** Ошибка при выполнении info

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

Однако, поскольку хранилище поддерживает версии, можно посмотреть состояние репозитория до удаления stanza. В зависимости от ситуации определить целевое время бывает непросто, но в данном случае момент удаления stanza можно установить по времени удаления `backup.info`.

pg-primary **⇒** Показать версии `backup.info` в бакете

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
-------------------------------------------------------------------------------------
|                                ListObjectVersions                                 |
+--------+------------------------------------+-------------------------------------+
| Action |             Modified               |               Object                |
+--------+------------------------------------+-------------------------------------+
|  PUT   |  2026-10-02T18:58:20.631000+00:00  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T18:58:33.900000+00:00  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T18:58:45.634000+00:00  |  demo-repo/backup/demo/backup.info  |
+--------+------------------------------------+-------------------------------------+
```

Теперь можно выполнить команду `info` с целевым временем, чтобы увидеть репозиторий до удаления.

pg-primary **⇒** Выполнить info с целевым временем

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 18:58:34+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (14): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-185820F
            timestamp start/stop: 2026-10-02 18:58:20+00 / 2026-10-02 18:58:33+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 4.2MB, backup size: 4.2MB
```

Если команда `info` показывает нужную резервную копию, её можно восстановить с тем же целевым временем.

pg-primary **⇒** Выполнить восстановление с целевым временем

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 18:58:34+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=5686-f718513c --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 18:58:34+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-185820F, recovery will start at 2026-10-02 18:58:20
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00   INFO: write updated /var/lib/pgsql/14/data/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo systemctl start postgresql-14.service
```

--------

## Выделенный сервер репозитория {#dedicated-repository-host}

Конфигурация, описанная в разделе [Быстрый старт](#quick-start), подходит для простых установок, но в корпоративных средах обычно используют выделенный сервер репозитория для хранения резервных копий и файлов архива WAL. Так резервные копии и архив WAL отделены от сервера баз данных и меньше страдают при его отказе. При этом по-прежнему полезно применять обычное ПО резервного копирования для самого сервера репозитория.

На серверах PostgreSQL параметр `pg1-path` должен содержать путь к локальному кластеру PostgreSQL, а `pg1-host` задавать не следует. При настройке сервера репозитория в файле конфигурации pgbackrest необходимо задать `pg-host` для подключения к первичному и резервным серверам, если они есть. Сведения более чем об одном сервере PostgreSQL следует указывать только в конфигурации pgbackrest на сервере репозитория. Порядок не важен: например, pg1-path/pg1-host и pg2-path/pg2-host могут соответствовать как первичному, так и резервному серверу.

### Установка {#installation-1}

Для хранения резервных копий кластера создаётся новый сервер с именем repository.

ПРИМЕЧАНИЕ:

Версия pgBackRest на сервере репозитория должна в точности совпадать с версией на сервере PostgreSQL.

В качестве владельца репозитория pgBackRest создаётся пользователь `pgbackrest`. Владельцем может быть любой пользователь, но во избежание путаницы лучше не использовать `postgres`, если он существует.

ПРИМЕЧАНИЕ:

При установке pgBackRest из пакета может предоставляться конфигурация logrotate, например `/etc/logrotate.d/pgbackrest`, которая выполняет ротацию журналов от имени определённого пользователя через директиву `su` (например, `su postgres postgres`). Поскольку файлы в `/var/log/pgbackrest` принадлежат пользователю, запускающему pgBackRest (здесь `pgbackrest`), директиву `su` необходимо изменить так, чтобы она соответствовала этому пользователю, иначе logrotate завершится ошибкой прав доступа.

repository **⇒** Создать пользователя `pgbackrest`

```bash
sudo groupadd pgbackrest
sudo adduser -gpgbackrest -n pgbackrest
```

Предпочтительнее устанавливать pgBackRest из пакета, чем собирать из исходного кода. При установке из пакета остальные инструкции этого раздела обычно не нужны, однако пакет может не создать какой-либо каталог или назначить неверные права доступа. В таком случае может потребоваться вручную создать каталоги или исправить права.

Пакеты pgBackRest для RHEL доступны на [yum.postgresql.org](http://yum.postgresql.org).

Если для используемого дистрибутива или его версии нет пакетов, можно [собрать программу из исходного кода](#build), а затем установить её вручную, как показано ниже.

repository **⇒** Установить зависимости

```bash
sudo yum install postgresql-libs libssh2
```

repository **⇒** Скопировать исполняемый файл pgBackRest с сервера сборки

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

Для pgBackRest нужны каталоги журналов и конфигурации, а также файл конфигурации.

repository **⇒** Создать файл конфигурации и каталоги pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

repository **⇒** Создать репозиторий pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### Конфигурация {#configuration}

pgBackRest может использовать TLS с клиентскими сертификатами для обмена данными между серверами. Также можно использовать SSH; см. [Настройка SSH](/ru/docs/pgbackrest/user-guide/#setup-passwordless-ssh).

pgBackRest ожидает, что клиентские и серверные сертификаты созданы так же, как для PostgreSQL. Подробные инструкции по созданию сертификатов см. в разделе [Защищённые соединения TCP/IP с TLS](https://www.postgresql.org/docs/current/ssl-tcp.html).

На сервере репозитория необходимо указать узел pg-primary, пользователя для подключения к нему и путь к базе данных. Первичный сервер будет настроен как `pg1`, чтобы позднее можно было добавить резервный.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `pg1-host`/`pg1-host-user` и `pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

На сервере баз данных необходимо указать сервер и пользователя репозитория. Значение параметра `repo1-host-user` по умолчанию — `pgbackrest`. Если пользователь `postgres` выполняет восстановление на сервере репозитория, лучше не разрешать пользователю `postgres` также создавать резервные копии. Однако пользователь `postgres` может читать репозиторий непосредственно, если входит в ту же группу, что и пользователь `pgbackrest`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `repo1-host`/`repo1-host-user`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Настройка PostgreSQL описана в разделе [Настройка архивирования](#configure-archiving).

Команды выполняются так же, как в конфигурации с одним сервером, за исключением того, что некоторые команды, например `backup` и `expire`, запускаются на сервере репозитория, а не на сервере баз данных.

### Настройка сервера TLS {#setup-tls-server}

Сервер TLS pgBackRest необходимо настроить и запустить на каждом узле.

repository **⇒** Настроить сервер pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=pgbackrest
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

pg-primary **⇒** Настроить сервер pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### Создание и проверка stanza {#create-and-check-stanza}

Создайте stanza в новом репозитории.

repository **⇒** Создать stanza

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

Проверьте правильность конфигурации и на сервере баз данных, и на сервере репозитория. Дополнительные сведения о команде `check` см. в разделе [Проверка конфигурации](#check-the-configuration).

pg-primary **⇒** Проверить конфигурацию

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

repository **⇒** Проверить конфигурацию

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### Создание резервной копии {#perform-a-backup-1}

Чтобы создать резервную копию кластера PostgreSQL, запустите pgBackRest с командой `backup` на сервере репозитория.

repository **⇒** Создать резервную копию демонстрационного кластера

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

Поскольку на сервере репозитория был создан новый репозиторий, появилось предупреждение о замене инкрементного резервного копирования полным.

### Восстановление резервной копии {#restore-a-backup-1}

Чтобы восстановить кластер PostgreSQL, запустите pgBackRest с командой `restore` на сервере баз данных.

pg-primary **⇒** Остановить демонстрационный кластер, восстановить его и перезапустить PostgreSQL

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo systemctl start postgresql-14.service
```

--------

## Параллельное резервное копирование и восстановление {#parallel-backup--restore}

pgBackRest поддерживает параллельную обработку для ускорения сжатия и передачи данных. Количество используемых процессов задаётся параметром `--process-max`.

Обычно для команды `backup` лучше использовать не более 25% доступных CPU. Резервное копирование не обязательно должно быть очень быстрым, если оно выполняется регулярно; по возможности следует избегать влияния этого процесса на производительность базы данных.

Для команды восстановления можно и следует использовать все доступные CPU, поскольку во время восстановления кластер PostgreSQL остановлен и на сервере обычно не выполняется другая важная работа. Если на сервере несколько кластеров, это следует учитывать при настройке параллелизма восстановления.

repository **⇒** Создать резервную копию одним процессом

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить pgBackRest на использование нескольких процессов `backup`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository **⇒** Создать резервную копию несколькими процессами

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** Получить сведения о резервных копиях демонстрационного кластера

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (14): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-185937F
            timestamp start/stop: 2026-10-02 18:59:37+00 / 2026-10-02 18:59:40+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB

        full backup: 20261002-185941F
            timestamp start/stop: 2026-10-02 18:59:41+00 / 2026-10-02 18:59:43+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB
```

Использование нескольких процессов должно повысить производительность последнего резервного копирования. Для очень маленьких копий разница может быть незаметна, но с ростом базы данных будет увеличиваться и экономия времени.

--------

## Запуск и остановка {#starting-and-stopping}

Если резервный сервер повышается до первичного для тестирования или тестовый кластер восстанавливается из резервной копии рабочей среды, полезно запретить этим кластерам запись в репозитории pgBackRest. Для этого служит команда `stop`.

Команда `stop` блокирует следующие команды записи: `archive-push`, `backup`, `expire`, `stanza-create` и `stanza-upgrade`. Исключение из этого правила — `stanza-delete` (подробности см. в разделе [Удаление stanza](#delete-a-stanza)).

pg-primary **⇒** Запретить команды записи pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

Новые команды записи pgBackRest больше не будут запускаться.

repository **⇒** Попытаться создать резервную копию

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

Укажите `--force`, чтобы завершить уже работающие команды записи pgBackRest. Это относится и к асинхронному archive-get (хотя он снова запустится, если потребуется PostgreSQL). Если pgBackRest уже остановлен, повторная остановка выдаст предупреждение.

pg-primary **⇒** Повторно остановить службы pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

Снова разрешите команды записи pgBackRest командой `start`. Команды записи, выполнявшиеся до остановки, не возобновятся автоматически, но теперь их можно запускать.

pg-primary **⇒** Разрешить команды записи pgBackRest

```bash
sudo -u postgres pgbackrest start
```

Также можно остановить pgBackRest для отдельной stanza.

pg-primary **⇒** Запретить команды записи pgBackRest для stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

Новые команды записи pgBackRest для указанной stanza больше не будут запускаться.

repository **⇒** Попытаться создать резервную копию

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

При разрешении команд записи pgBackRest для отдельной stanza её также необходимо указать.

pg-primary **⇒** Разрешить команды записи pgBackRest для stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## Репликация {#replication}

Репликация позволяет создать из одного первичного сервера несколько копий кластера PostgreSQL, называемых резервными серверами. Они полезны для распределения нагрузки чтения и обеспечения избыточности на случай отказа первичного сервера.

### Установка {#installation-2}

Для запуска резервного сервера создаётся новый узел с именем pg-standby.

Предпочтительнее устанавливать pgBackRest из пакета, чем собирать из исходного кода. При установке из пакета остальные инструкции этого раздела обычно не нужны, однако пакет может не создать какой-либо каталог или назначить неверные права доступа. В таком случае может потребоваться вручную создать каталоги или исправить права.

Пакеты pgBackRest для RHEL доступны на [yum.postgresql.org](http://yum.postgresql.org).

Если для используемого дистрибутива или его версии нет пакетов, можно [собрать программу из исходного кода](#build), а затем установить её вручную, как показано ниже.

pg-standby **⇒** Установить зависимости

```bash
sudo yum install postgresql-libs libssh2
```

pg-standby **⇒** Скопировать исполняемый файл pgBackRest с сервера сборки

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

Для pgBackRest нужны каталоги журналов и конфигурации, а также файл конфигурации.

pg-standby **⇒** Создать файл конфигурации и каталоги pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Горячий резерв {#hot-standby}

Горячий резервный сервер выполняет репликацию через архив WAL и допускает запросы только для чтения.

Конфигурация pgBackRest почти такая же, как на pg-primary, но используется тип восстановления `standby`, чтобы кластер оставался в режиме восстановления после достижения конца потока WAL.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить pgBackRest на резервном сервере

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-standby **⇒** Настроить сервер pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

Создайте каталог, в который будет восстановлен PostgreSQL.

pg-standby **⇒** Создать каталог PostgreSQL

```bash
sudo -u postgres mkdir -p -m 700 /var/lib/pgsql/14/data
```

Теперь резервный сервер можно создать командой `restore`.

ВАЖНО:

Если кластер планируется вывести из режима восстановления, не делая его новым первичным сервером (например, для отчётности или тестирования), отключите архивирование с помощью `--archive-mode=off` или настройки archive_mode=off в `postgresql.conf`. Если архивирование не отключить, в репозиторий может попасть посторонний WAL, затрудняющий восстановление.

pg-standby **⇒** Восстановить демонстрационный резервный кластер

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:04
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

Эта конфигурация рассчитана на случай, если резервный сервер будет повышен до первичного.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Настроить PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** Запустить PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

Журнал PostgreSQL содержит полезные сведения о восстановлении. В частности, обратите внимание на сообщения о том, что кластер перешёл в режим резервного сервера и готов принимать соединения только для чтения.

pg-standby **⇒** Проверить журнал PostgreSQL на наличие сообщений об успешном запуске

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 4 lines of output]
LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
LOG:  database system was interrupted; last known up at 2026-10-02 18:59:41 UTC
LOG:  entering standby mode
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
       [filtered 3 lines of output]
```

Простой способ проверить правильность настройки репликации — создать таблицу на pg-primary.

pg-primary **⇒** Создать новую таблицу на первичном сервере

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Затем запросить ту же таблицу на pg-standby.

pg-standby **⇒** Запросить новую таблицу на резервном сервере

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

Что же пошло не так? Поскольку PostgreSQL получает сегменты WAL для репликации из архива, изменения не будут видны на резервном сервере, пока pg-primary не отправит в архив сегмент WAL, содержащий эти изменения.

Это можно сделать вручную вызовом `pg_switch_wal()`, который отправляет текущий сегмент WAL в архив (для последующих изменений создаётся новый сегмент WAL).

pg-primary **⇒** Вызвать `pg_switch_wal()`

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/2601E7C0    | 2026-10-02 19:00:10.880013+00
(1 row)
```

Теперь после небольшой задержки таблица появится на pg-standby.

pg-standby **⇒** Теперь новая таблица есть на резервном сервере (может потребоваться несколько повторных попыток)

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:11.954843+00
(1 row)
```

Проверьте конфигурацию доступа резервного сервера к репозиторию.

pg-standby **⇒** Проверить конфигурацию

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1250-e6a5e2d8 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### Потоковая репликация {#streaming-replication}

Потоковая репликация устанавливает прямое соединение с первичным сервером и применяет изменения сразу после их появления на нём, не полагаясь только на архив WAL. Это значительно уменьшает отставание резервного сервера от первичного.

Для потоковой репликации требуется пользователь с правом репликации.

pg-primary **⇒** Создать пользователя репликации

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

Файл `pg_hba.conf` необходимо изменить, чтобы разрешить резервному серверу подключаться от имени пользователя репликации. Обязательно замените IP-адрес ниже фактическим IP-адресом pg-standby. После изменения `pg_hba.conf` потребуется перечитать конфигурацию.

pg-primary **⇒** Создать запись `pg_hba.conf` для пользователя репликации

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /var/lib/pgsql/14/data/pg_hba.conf'
sudo systemctl reload postgresql-14.service
```

Резервный сервер должен знать, как подключиться к первичному, поэтому в pgBackRest будет настроен параметр primary_conninfo.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Задать primary_conninfo

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Пароль можно указать в primary_conninfo, но использование файла `.pgpass` гибче и безопаснее.

pg-standby **⇒** Задать пароль репликации в файле `.pgpass`.

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/pgsql/.pgpass'
sudo -u postgres chmod 600 /var/lib/pgsql/.pgpass
```

Теперь резервный сервер можно создать командой `restore`.

pg-standby **⇒** Остановить PostgreSQL и восстановить демонстрационный резервный кластер

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:18
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

ПРИМЕЧАНИЕ:

Настройка primary_conninfo записана в файл `postgresql.auto.conf`, поскольку в `pgbackrest.conf` она задана как `recovery-option`. Если требуется сохранить существующий файл `postgresql.auto.conf`, с командой `restore` можно использовать параметр `--type=preserve`.

По умолчанию RHEL хранит файл `postgresql.conf` в каталоге данных PostgreSQL. Поэтому изменение `postgresql.conf` было перезаписано при последнем восстановлении, и настройку hot_standby необходимо включить снова. Другие способы решения этой проблемы — хранить файл `postgresql.conf` в другом месте или включить hot_standby на сервере pg-primary, где эта настройка будет игнорироваться.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Включить hot_standby

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

hot_standby = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** Запустить PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

Журнал PostgreSQL подтвердит запуск потоковой репликации.

pg-standby **⇒** Проверить журнал PostgreSQL на наличие сообщений об успешном запуске

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 12 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "000000070000000000000026" from archive
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

Теперь таблица, созданная на pg-primary, быстро появится на pg-standby без необходимости вызывать `pg_switch_wal()`.

pg-primary **⇒** Создать новую таблицу на первичном сервере

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.428653+00
(1 row)
```

pg-standby **⇒** Запросить таблицу на резервном сервере

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.605628+00
(1 row)
```

--------

## Несколько stanza {#multiple-stanzas}

pgBackRest поддерживает несколько stanza. Чаще всего несколько stanza используют общий сервер репозитория.

### Установка {#installation-3}

Для запуска нового первичного сервера создаётся узел с именем pg-alt.

Предпочтительнее устанавливать pgBackRest из пакета, чем собирать из исходного кода. При установке из пакета остальные инструкции этого раздела обычно не нужны, однако пакет может не создать какой-либо каталог или назначить неверные права доступа. В таком случае может потребоваться вручную создать каталоги или исправить права.

Пакеты pgBackRest для RHEL доступны на [yum.postgresql.org](http://yum.postgresql.org).

Если для используемого дистрибутива или его версии нет пакетов, можно [собрать программу из исходного кода](#build), а затем установить её вручную, как показано ниже.

pg-alt **⇒** Установить зависимости

```bash
sudo yum install postgresql-libs libssh2
```

pg-alt **⇒** Скопировать исполняемый файл pgBackRest с сервера сборки

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

Для pgBackRest нужны каталоги журналов и конфигурации, а также файл конфигурации.

pg-alt **⇒** Создать файл конфигурации и каталоги pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Конфигурация {#configuration-1}

Конфигурация pgBackRest почти идентична конфигурации pg-primary, но используется stanza `demo-alt`, чтобы резервные копии и архив хранились отдельно.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить pgBackRest на новом первичном сервере

```ini
[demo-alt]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo-alt

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `pg1-host`/`pg1-host-user` и `pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-alt **⇒** Настроить сервер pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### Создание демонстрационного кластера {#setup-demo-cluster-1}

pg-alt **⇒** Создать демонстрационный кластер

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

pg-alt:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Настроить параметры PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-alt **⇒** Запустить демонстрационный кластер

```bash
sudo systemctl restart postgresql-14.service
```

### Создание stanza и проверка конфигурации {#create-the-stanza-and-check-configuration}

Для инициализации stanza необходимо выполнить команду `stanza-create`. После `stanza-create` рекомендуется выполнить `check`, чтобы убедиться в правильной настройке архивирования и резервного копирования.

pg-alt **⇒** Создать stanza и проверить конфигурацию

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=929-571b66d7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=962-2cadc106 --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000001-5cb25be2e89d0324cc2a94cbc964295204118888.gz' on repo1
P00   INFO: check command end: completed successfully
```

Если команда `check` запускается на сервере репозитория, проверяются все stanza.

repository **⇒** Проверить конфигурацию всех stanza

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1384-3bcda35c --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/000000070000000000000027-b36b790bcf0b1a9f54bc84458117feb77853d452.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000002-c303ffb17f8a111070459593520aa35640317a38.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## Асинхронное архивирование {#asynchronous-archiving}

Асинхронное архивирование включается параметром `archive-async`. Он включает асинхронную работу обеих команд: `archive-push` и `archive-get`.

Необходим каталог очереди. Команды хранят в нём временные данные, но работают с ним существенно по-разному, поэтому использование каталога очереди подробно описано в соответствующих разделах.

pg-primary **⇒** Создать каталог очереди

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** Создать каталог очереди

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

Необходимо настроить каталог очереди и включить асинхронное архивирование. Само по себе асинхронное архивирование даёт некоторое преимущество за счёт уменьшения количества соединений с удалённым хранилищем, а настройка `process-max` может значительно повысить производительность благодаря параллельному выполнению операций. Не задавайте `process-max` настолько большим, чтобы это влияло на обычную работу базы данных.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить каталог очереди и асинхронное архивирование

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить каталог очереди и асинхронное архивирование

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

ПРИМЕЧАНИЕ:

`process-max` задаётся в секциях команд, чтобы этот параметр не применялся к резервному копированию и восстановлению. Это также позволяет задать разные значения для `archive-push` и `archive-get`.

Для демонстрации потоковая репликация будет нарушена, чтобы PostgreSQL получал WAL через restore_command.

pg-primary **⇒** Нарушить потоковую репликацию, изменив пароль репликации

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** Перезапустить резервный сервер, чтобы разорвать соединение

```bash
sudo systemctl restart postgresql-14.service
```

### Отправка в архив {#archive-push}

Асинхронная команда `archive-push` передаёт архивирование WAL отдельному процессу или процессам для повышения пропускной способности. Она «заглядывает вперёд» и находит сегменты WAL, готовые к архивированию помимо того, который PostgreSQL сейчас запрашивает через `archive_command`. Сегменты WAL передаются в архив непосредственно из каталога `pg_xlog`/`pg_wal`, а `archive_command` сообщает об успехе только после того, как сегмент WAL надёжно сохранён в архиве.

Каталог очереди содержит текущее состояние архивирования WAL. Записываемые в него файлы состояния обычно имеют нулевую длину и должны занимать минимум места (не более нескольких МБ) и создавать очень небольшую нагрузку ввода-вывода. Все сведения в этом каталоге можно воссоздать, поэтому при переносе кластера на другое оборудование сохранять каталог очереди не требуется.

ВАЖНО:

В первоначальной реализации асинхронного архивирования сегменты WAL копировались в каталог очереди перед сжатием и передачей. Новая реализация копирует WAL непосредственно из каталога `pg_xlog`. Если асинхронное архивирование использовалось в v1.12 или более ранней версии, перед обновлением внимательно прочитайте примечания к выпуску v1.13.

Файл `[stanza]-archive-push-async.log` позволяет отслеживать работу асинхронного процесса. Удобный способ проверки — быстро отправить несколько сегментов WAL.

pg-primary **⇒** Проверить параллельное асинхронное архивирование

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=6864-e51531e7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/00000007000000000000002D-7addc4d9a1861c1b8b68300ea3a7db01fbe08ae2.gz' on repo1
P00   INFO: check command end: completed successfully
```

Теперь файл журнала будет содержать записи о параллельной асинхронной работе.

pg-primary **⇒** Проверить результаты в журнале

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6828-6cf1b924 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6866-2a936d60 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully
```

### Получение из архива {#archive-get}

Асинхронная команда `archive-get` поддерживает локальную очередь WAL для повышения пропускной способности. Если сегмента WAL нет в очереди, он извлекается из репозитория вместе с достаточным количеством последовательных сегментов WAL для заполнения очереди. Максимальный размер очереди задаётся параметром `archive-get-queue-max`. Когда очередь заполнена менее чем наполовину, для её заполнения извлекаются дополнительные сегменты WAL.

Асинхронная работа наиболее полезна в средах с большим объёмом генерируемого WAL или высокой задержкой соединения с хранилищем репозитория (например, S3 или другим объектным хранилищем). При высокой задержке соединения может быть полезно увеличить `process-max`.

Файл `[stanza]-archive-get-async.log` позволяет отслеживать работу асинхронного процесса.

pg-standby **⇒** Проверить результаты в журнале

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=1919-a90112cb --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P01 DETAIL: found 000000070000000000000024 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000025 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000027 in the repo1: 14-1 archive
P01 DETAIL: found 000000070000000000000026 in the repo1: 14-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 31 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=1976-2ef79408 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P01 DETAIL: found 000000070000000000000028 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000029 in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002A in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002B in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002D in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002C in the repo1: 14-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 14 lines of output]
```

pg-primary **⇒** Восстановить потоковую репликацию, изменив пароль репликации

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## Резервное копирование с резервного сервера {#backup-from-a-standby}

pgBackRest может выполнять резервное копирование с резервного сервера вместо первичного. Для этого необходимо настроить сервер pg-standby и включить параметр `backup-standby`. Если настроено несколько резервных серверов, для резервного копирования используется первый найденный работающий резервный сервер.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Настроить `pg2-host`/`pg2-host-user` и `pg2-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Для резервного копирования необходимы и первичная, и резервная базы данных, хотя подавляющее большинство файлов копируется с резервного сервера, чтобы снизить нагрузку на первичный. Серверы баз данных можно настроить в любом порядке. pgBackRest автоматически определит, какой сервер первичный, а какой резервный.

repository **⇒** Создать резервную копию демонстрационного кластера с pg2

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/log/postgresql.log (10.9KB, 0.42%) checksum dbfa988289c2ff32dcd198f19455165722870b43
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/global/pg_control (8KB, 0.73%) checksum 0a793efbb7bb2e255bbb2bfac8f612bc943c7f31
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/pg_hba.conf (4.5KB, 0.90%) checksum cfa97af1dab1b130f0a921fa2d10d76fe0c5f630
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/current_logfiles (26B, 0.91%) checksum 78a9f5c10960f0d91fcd313937469824861795a2
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/pg_logical/replorigin_checkpoint (8B, 0.91%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1263 lines of output]
```

Эта инкрементная копия показывает, что большинство файлов копируется с сервера pg-standby и только несколько — с pg-primary.

pgBackRest создаёт с резервного сервера копию, идентичную копии с первичного. Для этого он запускает и завершает резервное копирование на pg-primary, копирует с pg-standby только реплицируемые файлы, а затем копирует немногочисленные оставшиеся файлы с pg-primary. Поэтому резервная копия включает журналы и статистику первичной базы данных.

--------

## Обновление PostgreSQL {#upgrading-postgresql}

Сразу после обновления PostgreSQL до новой основной версии во всех конфигурациях pgBackRest необходимо изменить `pg-path` на новое расположение базы данных и выполнить команду `stanza-upgrade`. Если на сервере настроено несколько репозиториев, stanza обновляется в каждом из них. Если база данных остановлена, используйте параметр `--no-online`.

Следующие инструкции не являются полным руководством по обновлению PostgreSQL: они описывают общий порядок обновления первичного и резервного серверов, чтобы показать необходимые шаги перенастройки pgBackRest. Перед обновлением рекомендуется создать резервную копию.

pg-primary **⇒** Остановить старый кластер

```bash
sudo systemctl stop postgresql-14.service
```

Остановите старый кластер на резервном сервере: он будет восстановлен из только что обновлённого кластера.

pg-standby **⇒** Остановить старый кластер

```bash
sudo systemctl stop postgresql-14.service
```

Создайте новый кластер и выполните обновление.

pg-primary **⇒** Создать новый кластер и выполнить обновление

```bash
sudo -u postgres /usr/pgsql-15/bin/initdb \
       -D /var/lib/pgsql/15/data -k -A peer
sudo -u postgres sh -c 'cd /var/lib/pgsql && \
       /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir=/usr/pgsql-14/bin \
       --new-bindir=/usr/pgsql-15/bin \
       --old-datadir=/var/lib/pgsql/14/data \
       --new-datadir=/var/lib/pgsql/15/data \
       --old-options=" -c config_file=/var/lib/pgsql/14/data/postgresql.conf" \
       --new-options=" -c config_file=/var/lib/pgsql/15/data/postgresql.conf"'
```

```text
       [filtered 41 lines of output]
Checking for extension updates                              ok
Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

Настройте параметры и порт нового кластера.

pg-primary:`/var/lib/pgsql/15/data/postgresql.conf` **⇒** Настроить PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

Обновите конфигурацию pgBackRest на всех системах, указав новый кластер.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Обновить `pg1-path`

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Обновить `pg-path`

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Обновить `pg1-path` и `pg2-path`, отключить резервное копирование с резервного сервера

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-primary **⇒** Скопировать конфигурацию hba

```bash
sudo cp /var/lib/pgsql/14/data/pg_hba.conf \
       /var/lib/pgsql/15/data/pg_hba.conf
```

Перед запуском нового кластера необходимо выполнить команду `stanza-upgrade`.

pg-primary **⇒** Обновить stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=7454-62cfb155 --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/pgsql/15/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

Запустите новый кластер и убедитесь в успешной установке.

pg-primary **⇒** Запустить новый кластер

```bash
sudo systemctl start postgresql-15.service
```

Проверьте конфигурацию командой `check`.

pg-primary **⇒** Проверить конфигурацию

```bash
sudo systemctl status postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

Удалите старый кластер.

pg-primary **⇒** Удалить старый кластер

```bash
sudo rm -rf /var/lib/pgsql/14/data
```

Установите исполняемые файлы новой версии PostgreSQL на резервном сервере и создайте кластер.

pg-standby **⇒** Удалить старый кластер и создать новый

```bash
sudo rm -rf /var/lib/pgsql/14/data
sudo -u postgres mkdir -p -m 700 /usr/pgsql-15/bin
```

Выполните `check` на сервере репозитория. Предупреждение о недоступности резервного сервера ожидаемо, поскольку резервный кластер остановлен. Эта команда показывает, что сервер репозитория располагает сведениями о резервном сервере и правильно настроен для работы с первичным.

repository **⇒** Проверить конфигурацию

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 tls protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

Создайте полную резервную копию нового кластера, а затем восстановите из неё резервный сервер. Если запрошен тип `incr` или `diff`, он автоматически изменится на `full`.

repository **⇒** Создать полную резервную копию

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** Восстановить демонстрационный резервный кластер

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
```

pg-standby **⇒** Запустить PostgreSQL и проверить конфигурацию pgBackRest

```bash
sudo systemctl start postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

После восстановления резервного сервера можно включить резервное копирование с него.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Снова включить резервное копирование с резервного сервера

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```
