---
title: "Команда удаления stanza (stanza-delete)"
linkTitle: "stanza-delete"
weight: 150
description: "Справочник по параметрам и поведению команды pgBackRest `stanza-delete`."
icon: fa-solid fa-trash
module: [PGBACKREST]
categories: [Справочник]
upstream_link: "https://pgbackrest.org/command.html#command-stanza-delete"
---

Команда `stanza-delete` удаляет из репозитория данные, связанные со stanza.

ПРЕДУПРЕЖДЕНИЕ:

Используйте эту команду осторожно: она безвозвратно удаляет все резервные копии и архивы указанной stanza из репозитория pgBackRest.

Чтобы удалить stanza:

- Остановите кластер PostgreSQL, связанный со stanza (или используйте --force, чтобы обойти это требование).
- Выполните команду `stop` на сервере, где будет запущена команда `stanza-delete`.
- Выполните команду `stanza-delete`.

После успешного завершения команды пользователь должен самостоятельно удалить stanza из всех файлов конфигурации pgBackRest и/или переменных окружения.

За один раз stanza можно удалить только из одного репозитория. Для удаления из нескольких репозиториев повторите команду `stanza-delete` для каждого из них, указывая параметр `--repo`.

## Параметры команды {#command-options}

### Параметр принудительного выполнения (`--force`) {#force-option---force}

Принудительное удаление stanza.

Если PostgreSQL для этой stanza продолжает работать, этот параметр позволяет принудительно удалить stanza из репозитория.

```yaml
default: n
example: --no-force
```

## Общие параметры {#general-options}

### Параметр разрешения запуска от root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Разрешение запуска команды от пользователя root.

По умолчанию только команда `restore` может выполняться от пользователя root, поскольку она предназначена для тщательного управления принадлежностью файлов. Выполнение других команд от пользователя root может привести к созданию файлов (например, в репозитории), принадлежащих root, и, как следствие, недоступных для пользователя PostgreSQL, что вызовет сбой последующих команд.

Включите этот параметр, чтобы запустить команду от имени root. Однако гораздо лучше запускать pgBackRest от пользователя, владеющего репозиторием и кластером PostgreSQL.

```yaml
default: n
example: --allow-root
```

### Параметр размера буфера (`--buffer-size`) {#buffer-size-option---buffer-size}

Размер буфера для операций ввода-вывода.

Размер буфера, используемый для копирования, сжатия, шифрования и других операций. Количество используемых буферов зависит от параметров, и каждая операция может использовать дополнительную память, например, сжатие `gz` может потребовать дополнительно 256KiB памяти.

Допустимые значения: `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` и `16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### Параметр команды SSH-клиента (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Команда SSH-клиента.

Позволяет задать конкретную команду SSH-клиента, если нужен другой клиент или команда `ssh` отсутствует в $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Параметр уровня сжатия для сети (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Уровень сжатия для передачи по сети.

Задаёт уровень сетевого сжатия, когда `compress-type=none` и команда выполняется на другом сервере, чем репозиторий. Сжатие уменьшает сетевой трафик. Когда `compress-type` не равен `none`, настройка `compress-level-network` игнорируется и вместо неё используется `compress-level`, чтобы файл сжимался только один раз.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### Параметр файла конфигурации (`--config`) {#config-option---config}

Конфигурационный файл pgBackRest.

Используйте этот параметр для указания другого файла конфигурации, отличного от файла по умолчанию.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### Параметр каталога включаемых конфигураций (`--config-include-path`) {#config-include-path-option---config-include-path}

Путь к дополнительным файлам конфигурации pgBackRest.

Файлы конфигурации с расширением `.conf`, находящиеся в указанном каталоге, объединяются с файлом конфигурации pgBackRest в единый файл конфигурации.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### Параметр каталога конфигурации (`--config-path`) {#config-path-option---config-path}

Базовый путь файлов конфигурации pgBackRest.

Эта настройка переопределяет базовый каталог по умолчанию для параметров `--config` и `--config-include-path`, если они не заданы явно в командной строке.

Например, передача только `--config-path=/conf/pgbackrest` приводит к установке значения по умолчанию для `--config` в `/conf/pgbackrest/pgbackrest.conf` и значения по умолчанию для `--config-include-path` в `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### Параметр тайм-аута базы данных (`--db-timeout`) {#database-timeout-option---db-timeout}

Тайм-аут запроса к базе данных.

Задаёт тайм-аут запросов к базе данных в секундах. Он распространяется и на функции начала и завершения резервного копирования, каждая из которых может выполняться довольно долго. Поэтому следует задавать большой тайм-аут, если нет уверенности, что эти функции завершатся быстро (то есть если задано `start-fast=y` и известно, что кластер базы данных не создаст много сегментов WAL во время резервного копирования).

> **ПРИМЕЧАНИЕ:** параметр `db-timeout` должен быть меньше `protocol-timeout`.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### Параметр тайм-аута ввода-вывода (`--io-timeout`) {#io-timeout-option---io-timeout}

Тайм-аут ввода-вывода.

Тайм-аут, в секундах, используемый для соединений и операций чтения/записи.

Операция чтения или записи не обязана полностью завершиться за это время, но *какое-то* продвижение должно произойти, хотя бы на один байт.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Параметр каталога блокировок (`--lock-path`) {#lock-path-option---lock-path}

Путь для хранения файлов блокировок.

В каталоге блокировок pgBackRest создаёт файлы блокировок, предотвращающие одновременное выполнение конфликтующих операций.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### Параметр нейтральной маски umask (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Использование нейтральной маски umask.

Устанавливает umask в 0000, чтобы объекты в репозитории создавались с подходящими правами. По умолчанию права каталогов — 0750, файлов — 0640.

Чтобы вместо этого использовать umask пользователя, выполняющего команду, укажите `neutral-umask=n` в файле конфигурации или `--no-neutral-umask` в командной строке.

```yaml
default: y
example: --no-neutral-umask
```

### Параметр приоритета процесса (`--priority`) {#set-process-priority-option---priority}

Установка приоритета процесса.

Определяет приоритет процесса (то есть значение nice) для планировщика ядра. Положительные значения понижают приоритет, отрицательные — повышают. В большинстве случаев процессы не имеют права повышать свой приоритет.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Параметр тайм-аута протокола (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Тайм-аут протокола.

Задаёт тайм-аут, в секундах, на который локальный или удалённый процесс будет ждать получения нового сообщения на уровне протокола. Это предотвращает бесконечное ожидание сообщения процессами.

> **ПРИМЕЧАНИЕ:** параметр `protocol-timeout` должен быть больше `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### Параметр поддержания соединения (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Включение поддержания соединения.

Включает сообщения keep-alive для сокетных соединений.

```yaml
default: y
example: --no-sck-keep-alive
```

### Параметр stanza (`--stanza`) {#stanza-option---stanza}

Определение stanza.

Stanza — конфигурация кластера баз данных PostgreSQL, которая определяет его расположение, способ резервного копирования, параметры архивирования и т. п. Большинство серверов баз данных содержат только один кластер PostgreSQL и, соответственно, одну stanza, тогда как на серверах резервного копирования есть stanza для каждого кластера, требующего резервного копирования.

Может возникнуть желание назвать stanza по имени первичного кластера, но лучше выбрать имя, описывающее базы данных в нём. Поскольку имя stanza используется для первичного сервера и всех реплик, уместнее выбрать имя, отражающее назначение кластера, например app или dw, а не локальное имя кластера, такое как main или prod.

```yaml
example: --stanza=main
```

### Параметр числа сообщений keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Число сообщений keep-alive.

Задаёт число сообщений TCP keep-alive, которые могут быть потеряны, прежде чем соединение будет считаться неработающим.

Этот параметр доступен на системах, которые поддерживают опцию сокета `TCP_KEEPCNT`.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### Параметр времени простоя keep-alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Время простоя перед отправкой keep-alive.

Задаёт время отсутствия сетевой активности в секундах, по истечении которого операционной системе следует отправить сообщение TCP keep-alive.

Этот параметр доступен на системах, которые поддерживают опцию сокета `TCP_KEEPIDLE`.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### Параметр интервала keep-alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Интервал сообщений keep-alive.

Задаёт время в секундах, после которого следует повторно отправить сообщение TCP keep-alive, не получившее подтверждения.

Этот параметр доступен на системах, которые поддерживают опцию сокета `TCP_KEEPINTVL`.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### Параметр наборов шифров TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Допустимые наборы шифров TLSv1.2.

Все соединения TLS между клиентом pgBackRest и сервером зашифрованы. По умолчанию также зашифрованы соединения с объектными хранилищами (например, S3).

> **ПРИМЕЧАНИЕ:** абсолютный минимальный уровень безопасности для любого транспортного соединения — TLSv1.2.

При необходимости допустимые наборы шифров можно изменить. Приведённый пример подходит, если нет особых требований к безопасности. Если параметр не задан (по умолчанию), применяется значение по умолчанию используемой библиотеки OpenSSL.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Параметр наборов шифров TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Допустимые наборы шифров TLSv1.3.

Все соединения TLS между клиентом pgBackRest и сервером зашифрованы. По умолчанию также зашифрованы соединения с объектными хранилищами (например, S3).

> **ПРИМЕЧАНИЕ:** абсолютный минимальный уровень безопасности для любого транспортного соединения — TLSv1.2.

При необходимости допустимые наборы шифров можно изменить. Если параметр не задан (по умолчанию), применяется значение по умолчанию используемой библиотеки OpenSSL.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## Параметры журналирования {#log-options}

### Параметр уровня журналирования в консоль (`--log-level-console`) {#console-log-level-option---log-level-console}

Уровень журналирования в консоль.

Поддерживаются следующие уровни журналирования:

- `off` - Журналирование отключено (не рекомендуется)
- `error` - Только ошибки
- `warn` - Предупреждения и ошибки
- `info` - Информационные сообщения, предупреждения и ошибки
- `detail` - Подробные и информационные сообщения, предупреждения и ошибки
- `debug` - Отладочные, подробные и информационные сообщения, предупреждения и ошибки
- `trace` - Трассировка (очень подробная отладка), отладочные и информационные сообщения, предупреждения и ошибки

```yaml
default: warn
example: --log-level-console=error
```

### Параметр уровня журналирования в файл (`--log-level-file`) {#file-log-level-option---log-level-file}

Уровень журналирования в файл.

Поддерживаются следующие уровни журналирования:

- `off` - Журналирование отключено (не рекомендуется)
- `error` - Только ошибки
- `warn` - Предупреждения и ошибки
- `info` - Информационные сообщения, предупреждения и ошибки
- `detail` - Подробные и информационные сообщения, предупреждения и ошибки
- `debug` - Отладочные, подробные и информационные сообщения, предупреждения и ошибки
- `trace` - Трассировка (очень подробная отладка), отладочные и информационные сообщения, предупреждения и ошибки

```yaml
default: info
example: --log-level-file=debug
```

### Параметр уровня журналирования в стандартный поток ошибок (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

Уровень ведения журнала для stderr.

Задаёт уровни журнала, сообщения которых выводятся в `stderr`, а не в `stdout` (задаваемый параметром `log-level-console`). Временная метка и процесс в `stderr` не выводятся.

Поддерживаются следующие уровни журналирования:

- `off` - Журналирование отключено (не рекомендуется)
- `error` - Только ошибки
- `warn` - Предупреждения и ошибки
- `info` - Информационные сообщения, предупреждения и ошибки
- `detail` - Подробные и информационные сообщения, предупреждения и ошибки
- `debug` - Отладочные, подробные и информационные сообщения, предупреждения и ошибки
- `trace` - Трассировка (очень подробная отладка), отладочные и информационные сообщения, предупреждения и ошибки

```yaml
default: off
example: --log-level-stderr=error
```

### Параметр каталога журналов (`--log-path`) {#log-path-option---log-path}

Путь, по которому хранятся файлы журналов.

Путь к журналу задаёт местоположение для хранения файлов журналов pgBackRest. Примечание: если `log-level-file=off`, то путь к журналу не требуется.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### Параметр журналирования подпроцессов (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Включение журналирования в подпроцессах.

Включает запись журнала в файл для всех подпроцессов, создаваемых этим процессом, с уровнем, заданным параметром `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### Параметр временных меток журнала (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Включение временных меток в журнале.

Включает временные метки при выводе журнала в консоль и в файл. Этот параметр отключается в особых случаях, например при генерации документации.

```yaml
default: y
example: --no-log-timestamp
```

## Параметры для сопровождающих {#maintainer-options}

### Параметр принудительного задания версии PostgreSQL (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

Принудительное задание версии PostgreSQL.

Указанная версия PostgreSQL будет использоваться вместо версии, автоматически определённой по `pg_control` или заголовкам WAL. Это полезно главным образом для форков PostgreSQL или версий в разработке, в которых эти значения отличаются от версии выпуска. Версия, которую PostgreSQL сообщает через `server_version_num`, должна совпадать с принудительно заданной.

ПРЕДУПРЕЖДЕНИЕ:

Используйте этот параметр осторожно: `pg_control` и заголовки WAL всё равно будут читаться в формате, ожидаемом для указанной версии, то есть в формате официальной версии PostgreSQL с открытым исходным кодом. Если форк или версия в разработке меняет формат полей, от которых зависит pgBackRest, это приведёт к неожиданному поведению. В общем случае параметр будет работать как ожидается только тогда, когда форк добавляет все собственные поля структур *после* стандартных полей PostgreSQL.

```yaml
example: --pg-version-force=15
```

## Параметры репозитория {#repository-options}

### Параметр выбора репозитория (`--repo`) {#set-repository-option---repo}

Выбор репозитория.

Задаёт репозиторий, с которым работает команда.

Например, позволяет выполнить восстановление из конкретного репозитория, не предоставляя выбор pgBackRest.

```yaml
allowed: [1, 256]
example: --repo=1
```

### Параметр контейнера репозитория Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Контейнер репозитория Azure.

Контейнер Azure для хранения репозитория.

Репозитории pgBackRest можно хранить в корне контейнера, задав `repo-path=/`, но обычно лучше указать префикс, например `/repo`, чтобы в контейнере также можно было хранить журналы и другие данные, создаваемые Azure.

```yaml
example: --repo1-azure-container=pg-backup
```

### Параметр типа ключа репозитория Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Тип ключа репозитория Azure.

Поддерживаются следующие типы авторизации:

- `shared` - Общий ключ
- `sas` - Подпись общего доступа
- `auto` - Автоматическая авторизация с использованием управляемых удостоверений Azure

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### Параметр стиля URI репозитория Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Стиль URI Azure.

Поддерживаются следующие стили URI:

- `host` - Соединение с узлом `account.endpoint`.
- `path` - Соединение с узлом `endpoint` с добавлением учётной записи в начало URI.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### Параметр типа шифрования репозитория (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Шифр для шифрования репозитория.

Поддерживаются следующие типы шифрования:

- `none` - Репозиторий не зашифрован
- `aes-256-cbc` - Advanced Encryption Standard с длиной ключа 256 бит

Шифрование всегда выполняется на стороне клиента, даже если тип репозитория (например, S3) поддерживает шифрование.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### Параметр бакета репозитория GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Бакет репозитория GCS.

Бакет GCS для хранения репозитория.

Репозитории pgBackRest можно хранить в корне бакета, задав `repo-path=/`, но обычно лучше указать префикс, например `/repo`, чтобы в бакете также можно было хранить журналы и другие данные, создаваемые GCS.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### Параметр конечной точки репозитория GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Конечная точка репозитория GCS.

Конечная точка для соединения со службой хранения. Её можно изменить для использования локального сервера GCS или другой конечной точки.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### Параметр типа ключа репозитория GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Тип ключа репозитория GCS.

Поддерживаются следующие типы авторизации:

- `auto` - Авторизация с помощью служебной учётной записи экземпляра.
- `service` - Служебная учётная запись из локально сохранённого ключа.
- `token` - Для локального тестирования, например с `fakegcs`.
- `web-id` - Авторизация с помощью Workload Identity Federation.

При `repo-gcs-key-type=service` учётные данные повторно загружаются при обновлении токена аутентификации.

При `repo-gcs-key-type=web-id` параметр `repo-gcs-key` должен указывать на файл учётных данных внешней учётной записи. При обновлении токена аутентификации веб-токен удостоверения загружается повторно.

`service_account_impersonation_url` не поддерживается. Поддерживается только `credential_source.file`; если указан `credential_source.format`, его тип должен быть `text`.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### Параметр идентификатора проекта репозитория GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

Идентификатор проекта GCS.

Идентификатор проекта GCS, определяющий оплату запросов.

```yaml
example: --repo1-gcs-user-project=my-project
```

### Параметр сервера репозитория (`--repo-host`) {#repository-host-option---repo-host}

Сервер репозитория при удалённой работе.

При резервном копировании и архивировании в локально смонтированную файловую систему эта настройка не требуется.

```yaml
example: --repo1-host=repo1.domain.com
```

Устаревшее имя: backup-host

### Параметр файла центра сертификации сервера репозитория (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Файл центра сертификации сервера репозитория.

Позволяет использовать для соединения с сервером репозитория файл CA, отличный от системного файла по умолчанию.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Параметр каталога центра сертификации сервера репозитория (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Каталог центра сертификации сервера репозитория.

Позволяет использовать для соединения с сервером репозитория каталог CA, отличный от системного каталога по умолчанию.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### Параметр файла сертификата сервера репозитория (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Файл сертификата для сервера репозитория.

Отправляется серверу репозитория для подтверждения личности клиента.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### Параметр команды на сервере репозитория (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

Команда pgBackRest на сервере репозитория.

Требуется только тогда, когда путь к команде pgBackRest на локальном сервере и сервере репозитория различается. Если параметр не задан, команда на сервере репозитория будет той же, что и локальная команда.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Устаревшее имя: backup-cmd

### Параметр файла конфигурации сервера репозитория (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

Файл конфигурации pgBackRest на сервере репозитория.

Задаёт расположение файла конфигурации на сервере репозитория. Требуется только тогда, когда оно отличается от расположения локального файла конфигурации.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Устаревшее имя: backup-config

### Параметр каталога включаемых конфигураций сервера репозитория (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Каталог включаемых конфигураций pgBackRest на сервере репозитория.

Задаёт расположение каталога включаемых конфигураций на сервере репозитория. Требуется только тогда, когда оно отличается от расположения локального каталога включаемых конфигураций.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Параметр каталога конфигурации сервера репозитория (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

Каталог конфигурации pgBackRest на сервере репозитория.

Задаёт расположение каталога конфигурации на сервере репозитория. Требуется только тогда, когда оно отличается от расположения локального каталога конфигурации.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### Параметр файла ключа для сервера репозитория (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Файл ключа для сервера репозитория.

Подтверждает, что сертификат клиента отправлен его владельцем.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### Параметр порта сервера репозитория (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Порт сервера репозитория при заданном `repo-host`.

Позволяет указать нестандартный порт для протокола сервера репозитория.

> **ПРИМЕЧАНИЕ:** при `repo-host-type=ssh` для `repo-host-port` нет значения по умолчанию. В этом случае используется порт, настроенный для команды, указанной в `cmd-ssh`.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

Устаревшее имя: backup-ssh-port

### Параметр типа протокола сервера репозитория (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Тип протокола сервера репозитория.

Поддерживаются следующие типы протоколов:

- `ssh` - Secure Shell.
- `tls` - TLS-сервер pgBackRest.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### Параметр пользователя сервера репозитория (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Пользователь сервера репозитория при заданном `repo-host`.

Определяет пользователя, от имени которого выполняются операции на сервере репозитория. Предпочтительно использовать не `postgres`, а другого пользователя, например `pgbackrest`. Если PostgreSQL работает на сервере репозитория, пользователя `postgres` можно включить в группу `pgbackrest`, чтобы предоставить ему право чтения репозитория без возможности случайно повредить его содержимое.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

Устаревшее имя: backup-user

### Параметр пути репозитория (`--repo-path`) {#repository-path-option---repo-path}

Путь для хранения резервных копий и архива.

В репозитории pgBackRest хранит резервные копии и архивирует сегменты WAL.

Заранее оценить требуемое место бывает сложно. Лучше создать несколько резервных копий, записать размеры копий разных типов (full/incr/diff) и измерить объём WAL, создаваемый за день. Это даст общее представление о необходимом месте, хотя со временем по мере развития базы данных требования, скорее всего, изменятся.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### Параметр бакета репозитория S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

Бакет репозитория S3.

Бакет S3 для хранения репозитория.

Репозитории pgBackRest можно хранить в корне бакета, задав `repo-path=/`, но обычно лучше указать префикс, например `/repo`, чтобы в бакете также можно было хранить журналы и другие данные, создаваемые AWS.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### Параметр конечной точки репозитория S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

Конечная точка репозитория S3.

Следует использовать конечную точку AWS, допустимую для выбранного региона.

Для нестандартных или тестовых конфигураций могут быть полезны параметры `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` и `repo-storage-verify-tls`.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### Параметр типа ключа репозитория S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

Тип ключа репозитория S3.

Поддерживаются следующие типы авторизации:

- `shared` - Общие ключи
- `auto` - Автоматическое получение временных учётных данных
- `web-id` - Автоматическое получение учётных данных веб-идентификации
- `pod-id` - Автоматическое получение учётных данных EKS Pod Identity
- `process` - Получение учётных данных запуском процесса

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### Параметр идентификатора ключа KMS репозитория S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

Ключ KMS репозитория S3.

Включает шифрование на стороне сервера S3 с указанным ключом AWS Key Management Service.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Параметр команды процесса аутентификации S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Команда процесса аутентификации S3.

Команда (и необязательные аргументы), выполняемая для получения временных учётных данных S3. Первый элемент списка — команда, остальные передаются ей как параметры.

Процесс должен вывести JSON с полями `AccessKeyId`, `SecretAccessKey`, `SessionToken` и `Expiration`. Учётные данные автоматически обновляются до истечения срока действия. Формат описан в разделе [Поставщик учётных данных через процесс](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output).

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### Параметр региона репозитория S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

Регион репозитория S3.

Регион AWS, в котором создан бакет.

```yaml
example: --repo1-s3-region=us-east-1
```

### Параметр оплаты запросов отправителем в репозитории S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Оплата запросов отправителем в репозитории S3.

Включает в S3 оплату запросов отправителем.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### Параметр роли репозитория S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

Роль репозитория S3.

Имя роли AWS (не полный ARN), используемой для получения временных учётных данных при `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### Параметр службы репозитория S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

Служба подписывания S3.

Служба подписывания S3, используемая при аутентификации SigV4. Для стандартных конечных точек S3 по умолчанию используется `s3`. При использовании конечной точки S3 Outposts задайте `s3-outposts`.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### Параметр конечной точки STS репозитория S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

Конечная точка STS репозитория S3.

Конечная точка STS для получения временных учётных данных при `repo-s3-key-type=web-id`. Укажите региональную конечную точку (например, `sts.us-east-1.amazonaws.com`) для использования регионального STS; это может требоваться для GovCloud, китайских регионов или снижения задержки.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Параметр стиля URI репозитория S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

Стиль URI S3.

Поддерживаются следующие стили URI:

- `host` - Соединение с узлом `bucket.endpoint`.
- `path` - Соединение с узлом `endpoint` с добавлением бакета в начало URI.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### Параметр сервера репозитория SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

Сервер репозитория SFTP.

Сервер SFTP, на котором расположен репозиторий.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### Параметр отпечатка сервера репозитория SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Отпечаток сервера репозитория SFTP.

Способ формирования отпечатка сервера репозитория SFTP следует выбирать в соответствии с `repo-sftp-host-key-hash-type`. Отпечаток можно получить командой `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. Ключи сервера ssh обычно находятся в каталоге `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Параметр типа проверки ключа сервера SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Тип проверки ключа сервера SFTP.

Поддерживаются следующие типы проверки ключа сервера SFTP:

- `strict` - pgBackRest никогда не добавляет ключи серверов в файл ~/.ssh/known_hosts автоматически и отказывается соединяться с серверами, ключ которых изменился или отсутствует в файлах известных серверов. При этом пользователь должен вручную добавлять все новые серверы.
- `accept-new` - pgBackRest автоматически добавляет новые ключи серверов в пользовательский файл известных серверов, но не разрешает соединения с серверами, ключи которых изменились.
- `fingerprint` - pgBackRest сравнивает ключ сервера с отпечатком, заданным параметром `repo-sftp-host-fingerprint`.
- `none` - Ключ сервера не проверяется.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### Параметр типа хеша ключа сервера репозитория SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Тип хеша ключа сервера репозитория SFTP.

Задаёт тип хеша для вычисления дайджеста ключа удалённой системы при установлении SSH-соединения. Допустимые значения: `md5`, `sha1` и `sha256`, однако `sha256` поддерживается только новыми версиями `libssh2`.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### Параметр порта сервера репозитория SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Порт сервера репозитория SFTP.

Порт сервера репозитория SFTP.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### Параметр пользователя сервера репозитория SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Пользователь сервера репозитория SFTP.

Пользователь на сервере, используемом для хранения репозитория.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### Параметр файла известных серверов SFTP (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Файл известных серверов SFTP.

Файл известных серверов, в котором при аутентификации ищется совпадение с сервером SFTP. Если параметр не задан, pgBackRest по умолчанию проверяет `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` и `/etc/ssh/ssh_known_hosts2`. Если заданы один или несколько путей к файлам, поиск выполняется в них. Пути должны быть абсолютными или начинаться с тильды. Параметр `repo-sftp-known-host` можно указывать несколько раз для поиска в нескольких файлах известных серверов. Чтобы использовать проверку по этим файлам, `repo-sftp-host-fingerprint` не должен быть задан. См. также параметр `repo-sftp-host-check-type`.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Параметр файла закрытого ключа репозитория SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Файл закрытого ключа SFTP.

Файл закрытого ключа SFTP для аутентификации.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Параметр файла открытого ключа репозитория SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Файл открытого ключа SFTP.

Файл открытого ключа SFTP для аутентификации. Необязателен при сборке с OpenSSL и обязателен при сборке с другой библиотекой.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Параметр файла CA хранилища репозитория (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

Файл CA хранилища репозитория.

Позволяет использовать для сертификатов хранилища (например, S3 или Azure) файл CA, отличный от системного файла по умолчанию.

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Устаревшие имена: repo-azure-ca-file, repo-s3-ca-file

### Параметр каталога CA для TLS хранилища репозитория (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

Каталог CA хранилища репозитория.

Позволяет использовать для сертификатов хранилища (например, S3 или Azure) каталог CA, отличный от системного каталога по умолчанию.

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

Устаревшие имена: repo-azure-ca-path, repo-s3-ca-path

### Параметр сервера хранилища репозитория (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Сервер хранилища репозитория.

Устанавливает соединение с сервером, отличным от конечной точки хранилища (например, S3 или Azure). Обычно используется для тестирования.

```yaml
example: --repo1-storage-host=127.0.0.1
```

Устаревшие имена: repo-azure-host, repo-s3-host

### Параметр порта хранилища репозитория (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Порт хранилища репозитория.

Порт для соединения с конечной точкой хранилища (например, S3 или Azure) либо с сервером, если он указан.

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

Устаревшие имена: repo-azure-port, repo-s3-port

### Параметр предварительного чтения из хранилища репозитория (`--repo-storage-prefetch`) {#repository-storage-prefetch-option---repo-storage-prefetch}

Предварительное чтение из хранилища репозитория.

Определяет число запросов, отправляемых заранее при чтении из объектных хранилищ, например S3. Это не настоящая параллельная обработка, но она позволяет сократить задержку, связанную с отправкой запросов.

Число открытых запросов на одну операцию чтения на единицу больше заданного числа предварительных запросов, поскольку первый запрос чтения нельзя отправить заранее.

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### Параметр чтения с пропуском ненужных данных в хранилище репозитория (`--repo-storage-read-over`) {#repository-storage-read-over-option---repo-storage-read-over}

Чтение с пропуском ненужных данных в хранилище репозитория.

Пакеты файлов могут содержать данные, не нужные при восстановлении, например уже существующие файлы. Этот параметр позволяет пропускать ненужные данные, продолжая чтение без нового запроса к объектному хранилищу. Обычно это быстрее, поскольку задержка нового запроса чтения больше, чем при продолжении уже выполняющегося чтения. Для большинства классов хранения это также дешевле.

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

### Параметр тегов хранилища репозитория (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Теги хранилища репозитория.

Задаёт теги, добавляемые к объектам, если репозиторий расположен в объектном хранилище (например, S3). Параметр можно повторять для добавления нескольких тегов.

В pgBackRest нет возможности изменять эти теги, поэтому их следует правильно задать до запуска `stanza-create`, чтобы теги были одинаковыми во всём репозитории.

```yaml
example: --repo1-storage-tag=key1=value1
```

### Параметр размера части загрузки в хранилище репозитория (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Размер части загрузки в хранилище репозитория.

Объектные хранилища, такие как S3, позволяют загружать файлы частями, если файл слишком велик для размещения в памяти. Даже если он помещается в память, ограничение объёма памяти для загрузок позволяет использовать её экономнее.

Больший размер части обычно повышает производительность, поскольку уменьшает число запросов загрузки и позволяет загружать больше файлов одним запросом, а не частями. Недостаток — повышенное потребление памяти. Поскольку буфер части выделяется каждому процессу, большие значения `process-max` увеличивают общий расход памяти.

Допустимые размеры частей зависят от типа хранилища и платформы. Например, минимальный размер части в AWS S3 — 5MiB. Терминология также различается: при поиске минимальных и максимальных значений используйте «part size» для AWS S3, «chunk size» для GCS и «block size» для Azure.

Если файл больше 1GiB (максимального размера, который PostgreSQL создаёт по умолчанию), размер части постепенно увеличивается вплоть до максимально допустимого, чтобы завершить загрузку файла.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### Параметр проверки сертификата хранилища репозитория (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Проверка сертификата хранилища репозитория.

Позволяет включать и отключать проверку TLS-сертификата сервера хранилища (например, S3 или Azure). Отключать проверку следует только при тестировании или в других случаях использования самоподписанного сертификата.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

Устаревшие имена: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Параметр типа репозитория (`--repo-type`) {#repository-type-option---repo-type}

Тип хранилища репозитория.

Поддерживаются следующие типы репозиториев:

- `azure` - Azure Blob Storage Service
- `cifs` - Аналогичен `posix`, но отключает ссылки и fsync каталогов
- `gcs` - Google Cloud Storage
- `posix` - Файловые системы, совместимые с Posix
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

При использовании смонтированной NFS в качестве репозитория `posix` к pgBackRest применяются те же правила, что описаны в документации PostgreSQL: [Создание кластера баз данных — файловые системы](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```yaml
default: posix
example: --repo1-type=cifs
```

## Параметры stanza {#stanza-options}

### Параметр базы данных PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

База данных PostgreSQL.

Имя базы данных для соединения с PostgreSQL. Обычно лучше оставить значение по умолчанию, но в некоторых установках такой базы может не быть.

По историческим причинам значение переменной окружения `PGDATABASE` игнорируется.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### Параметр сервера PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

Сервер PostgreSQL для удалённой работы.

Используется при резервном копировании, когда сервер PostgreSQL отличается от сервера репозитория.

```yaml
example: --pg1-host=db.domain.com
```

Устаревшее имя: db-host

### Параметр файла центра сертификации сервера PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Файл центра сертификации сервера PostgreSQL.

Позволяет использовать для соединения с сервером PostgreSQL файл CA, отличный от системного файла по умолчанию.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Параметр каталога центра сертификации сервера PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Каталог центра сертификации сервера PostgreSQL.

Позволяет использовать для соединения с сервером PostgreSQL каталог CA, отличный от системного каталога по умолчанию.

```yaml
example: --pg1-host-ca-path=/etc/pki/tls/certs
```

### Параметр файла сертификата сервера PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Файл сертификата для сервера PostgreSQL.

Отправляется серверу PostgreSQL для подтверждения личности клиента.

```yaml
example: --pg1-host-cert-file=/path/to/client.crt
```

### Параметр команды на сервере PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

Команда pgBackRest на сервере PostgreSQL.

Требуется только тогда, когда путь к команде pgBackRest на локальном сервере и сервере PostgreSQL различается. Если параметр не задан, команда на сервере PostgreSQL будет той же, что и локальная команда.

```yaml
default: [path of executed pgbackrest binary]
example: --pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Устаревшее имя: db-cmd

### Параметр файла конфигурации сервера PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

Файл конфигурации pgBackRest на сервере базы данных.

Задаёт расположение файла конфигурации на сервере PostgreSQL. Требуется только тогда, когда оно отличается от расположения локального файла конфигурации.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Устаревшее имя: db-config

### Параметр каталога включаемых конфигураций сервера PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Каталог включаемых конфигураций pgBackRest на сервере базы данных.

Задаёт расположение каталога включаемых конфигураций на сервере PostgreSQL. Требуется только тогда, когда оно отличается от расположения локального каталога включаемых конфигураций.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Параметр каталога конфигурации сервера PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

Каталог конфигурации pgBackRest на сервере базы данных.

Задаёт расположение каталога конфигурации на сервере PostgreSQL. Требуется только тогда, когда оно отличается от расположения локального каталога конфигурации.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --pg1-host-config-path=/conf/pgbackrest
```

### Параметр файла ключа для сервера PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Файл ключа для сервера PostgreSQL.

Подтверждает, что сертификат клиента отправлен его владельцем.

```yaml
example: --pg1-host-key-file=/path/to/client.key
```

### Параметр порта сервера PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Порт сервера PostgreSQL при заданном `pg-host`.

Позволяет указать нестандартный порт для протокола сервера PostgreSQL.

> **ПРИМЕЧАНИЕ:** при `pg-host-type=ssh` для `pg-host-port` нет значения по умолчанию. В этом случае используется порт, настроенный для команды, указанной в `cmd-ssh`.

```yaml
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: --pg1-host-port=25
```

Устаревшее имя: db-ssh-port

### Параметр типа протокола сервера PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Тип протокола сервера PostgreSQL.

Поддерживаются следующие типы протоколов:

- `ssh` - Secure Shell.
- `tls` - TLS-сервер pgBackRest.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### Параметр пользователя сервера PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Пользователь для входа на сервер PostgreSQL при заданном `pg-host`.

Этот пользователь также будет владельцем удалённого процесса pgBackRest и будет устанавливать соединения с PostgreSQL. Для правильной работы следует использовать владельца кластера базы данных PostgreSQL, обычно это пользователь `postgres`, выбранный по умолчанию.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

Устаревшее имя: db-user

### Параметр пути PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

Каталог данных PostgreSQL.

Следует указать значение `data_directory`, сообщаемое PostgreSQL. Хотя его можно получить из разных источников, разумно задать его явно на случай, если эти источники будут недоступны при восстановлении или резервном копировании остановленного кластера.

При каждом резервном копировании работающего кластера параметр `pg-path` сверяется со значением, сообщаемым PostgreSQL, поэтому его следует всегда поддерживать актуальным.

```yaml
example: --pg1-path=/data/db
```

Устаревшее имя: db-path

### Параметр порта PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

Порт PostgreSQL.

Порт, на котором работает PostgreSQL. Обычно его не требуется указывать, поскольку большинство кластеров PostgreSQL работают на порту по умолчанию.

```yaml
default: 5432
allowed: [0, 65535]
example: --pg1-port=6543
```

Устаревшее имя: db-port

### Параметр каталога сокета PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Каталог Unix-сокета PostgreSQL.

Каталог Unix-сокета, указанный при запуске PostgreSQL. pgBackRest автоматически проверяет стандартное расположение для используемой ОС, поэтому обычно этот параметр не требуется, если каталог сокета не был явно изменён настройкой `unix_socket_directories` в `postgresql.conf`.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

Устаревшее имя: db-socket-path

### Параметр пользователя базы данных PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

Пользователь базы данных PostgreSQL.

Имя пользователя базы данных для соединения с PostgreSQL. Если оно не указано, pgBackRest использует локального пользователя ОС или `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
