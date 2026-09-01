---
title: "Преобразование отдельного экземпляра в кластер Patroni"
linkTitle: "Преобразование существующего кластера"
weight: 140
icon: fa-solid fa-truck-moving
description: "Процедура преобразования существующих данных PostgreSQL в кластер Patroni."
module: [PATRONI]
categories: [Задача]
aliases: [/docs/patroni/existing_data/]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
В этом разделе описано преобразование отдельного экземпляра PostgreSQL в кластер Patroni.

Чтобы развернуть кластер Patroni без существующего экземпляра PostgreSQL, обратитесь к разделу [Запуск и настройка](/ru/patroni/readme#running_configuring).

--------

## Процедура {#procedure}

Ниже приведён обзор преобразования существующего кластера Postgres в кластер под управлением Patroni. Предполагается, что все узлы существующего кластера работают и во время миграции вы *не намерены* менять конфигурацию Postgres. Выполните следующие действия:

1.  Создайте пользователей Postgres, как описано в разделе [аутентификации](/ru/patroni/config/yaml#postgresql_settings) конфигурации Patroni. В блоке SQL ниже приведены примеры команд; замените имена пользователей и пароли в соответствии со своим окружением. Если необходимые пользователи уже существуют, пропустите этот шаг.

    ``` sql
    -- Patroni superuser
    -- Replace PATRONI_SUPERUSER_USERNAME and PATRONI_SUPERUSER_PASSWORD accordingly
    CREATE USER PATRONI_SUPERUSER_USERNAME WITH SUPERUSER ENCRYPTED PASSWORD 'PATRONI_SUPERUSER_PASSWORD';

    -- Patroni replication user
    -- Replace PATRONI_REPLICATION_USERNAME and PATRONI_REPLICATION_PASSWORD accordingly
    CREATE USER PATRONI_REPLICATION_USERNAME WITH REPLICATION ENCRYPTED PASSWORD 'PATRONI_REPLICATION_PASSWORD';

    -- Patroni rewind user, if you intend to enable use_pg_rewind in your Patroni configuration
    -- Replace PATRONI_REWIND_USERNAME and PATRONI_REWIND_PASSWORD accordingly
    CREATE USER PATRONI_REWIND_USERNAME WITH ENCRYPTED PASSWORD 'PATRONI_REWIND_PASSWORD';
    GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO PATRONI_REWIND_USERNAME;
    ```

2.  Выполните следующие действия на всех узлах Postgres. Завершите все шаги на одном узле, прежде чем переходить к следующему. Начните с первичного узла, затем обработайте каждый резервный узел:

    1.  Если Postgres запускается через systemd, отключите модуль systemd Postgres, поскольку запуском и остановкой демона Postgres будет управлять Patroni.
    2.  Создайте файл конфигурации YAML Patroni. Для этого можно использовать [средства создания и проверки конфигурации Patroni](/ru/patroni/config#validate_generate_config).
        - **Примечание для первичного узла:** если слоты репликации используются между участниками кластера, рекомендуется включить `use_slots` и настроить существующие слоты как постоянные через элемент конфигурации `slots`. При включённом `use_slots` Patroni автоматически создаёт слоты для репликации между участниками и удаляет неизвестные ему слоты. Постоянные слоты позволяют сохранить существующие слоты на время миграции к Patroni. Подробнее см. [Параметры динамической конфигурации](/ru/patroni/config/dynamic#dynamic).
    3.  Запустите Patroni с помощью модуля службы systemd `patroni`. Он автоматически обнаружит, что Postgres уже работает, и начнёт мониторинг экземпляра.

3.  Передайте Patroni процедуру запуска Postgres. Для этого перезапустите участников кластера командой [patronictl restart cluster-name member-name](/ru/patroni/patronictl#patronictl_restart_parameters). Чтобы свести простой к минимуму, можно разделить шаг на две части:

    1.  Немедленный перезапуск резервных узлов.
    2.  Запланированный перезапуск первичного узла в окно обслуживания.

4.  Если на шаге `1.2.` настроены постоянные слоты, удалите их из конфигурации `slots` командой [patronictl edit-config cluster-name](/ru/patroni/patronictl#patronictl_edit_config_parameters), когда `restart_lsn` созданных Patroni слотов догонит `restart_lsn` исходных слотов соответствующих участников. После удаления слотов из конфигурации `slots` Patroni сможет удалить исходные слоты из кластера, когда они перестанут быть нужны. Ниже приведён пример запроса для сравнения `restart_lsn` пары слотов:

    ``` sql
    -- Assume original_slot_for_member_x is the name of the slot in your original
    -- cluster for replicating changes to member X, and slot_for_member_x is the
    -- slot created by Patroni for that purpose. You need restart_lsn of
    -- slot_for_member_x to be >= restart_lsn of original_slot_for_member_x
    SELECT slot_name,
           restart_lsn
    FROM pg_replication_slots
    WHERE slot_name IN (
        'original_slot_for_member_x',
        'slot_for_member_x'
    )
    ```

<a id="major_upgrade"></a>

## Обновление основной версии PostgreSQL {#major-upgrade-of-postgresql-version}

В настоящее время обновить основную версию можно только следующим способом:

1.  Остановите Patroni
2.  Обновите двоичные файлы PostgreSQL и выполните [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) на первичном узле
3.  Обновите patroni.yml
4.  Удалите ключ initialize из DCS либо полностью очистите состояние кластера в DCS. Второй вариант выполняется командой [patronictl remove cluster-name](/ru/patroni/patronictl#patronictl_remove_parameters). Это необходимо, поскольку pg_upgrade запускает initdb, фактически создающий новую базу данных с новым системным идентификатором PostgreSQL.
5.  Если на предыдущем шаге состояние кластера очищено, можно скопировать patroni.dynamic.json из старого каталога данных в новый. Это поможет сохранить некоторые ранее заданные параметры PostgreSQL.
6.  Запустите Patroni на первичном узле.
7.  Обновите двоичные файлы PostgreSQL и patroni.yml, затем очистите data_dir на резервных узлах.
8.  Запустите Patroni на резервных узлах и дождитесь завершения репликации.

PostgreSQL не поддерживает запуск pg_upgrade на резервных узлах. Если вы уверены в своих действиях, вместо очистки data_dir можно попробовать процедуру rsync, описанную в <https://www.postgresql.org/docs/current/pgupgrade.html>. Однако безопаснее всего позволить Patroni реплицировать данные.

--------

## Часто задаваемые вопросы {#faq}

- При запуске Patroni сообщает, что не может привязаться к порту PostgreSQL.

  Проверьте `listen_addresses` и `port` в `postgresql.conf`, а также `postgresql.listen` в `patroni.yml`. Не забудьте, что `pg_hba.conf` должен разрешать такой доступ.

- После запроса Patroni на перезапуск узла PostgreSQL выводит ошибку `could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory`

  Значение зависит от способа управления конфигурацией PostgreSQL. Если указан `postgresql.config_dir`, Patroni создаёт `pg_hba.conf` по параметрам раздела [bootstrap](/ru/patroni/config/yaml#bootstrap_settings) только при начальной инициализации нового кластера. В этом сценарии `PGDATA` не был пуст, поэтому инициализация не выполнялась. Файл должен существовать заранее.
