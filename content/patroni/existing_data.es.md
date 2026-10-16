---
title: "Convertir una instancia independiente en un clúster de Patroni"
linkTitle: "Convertir un clúster existente"
weight: 140
icon: fa-solid fa-truck-moving
description: "Procedimiento para convertir datos existentes de PostgreSQL en un clúster de Patroni."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
Esta sección describe el proceso para convertir una instancia de PostgreSQL independiente en un clúster de Patroni.

Para desplegar un clúster de Patroni sin usar una instancia de PostgreSQL preexistente, consulta [Ejecución y configuración](/es/patroni/readme#running_configuring) en su lugar.

--------

## Procedimiento {#procedure}

A continuación encontrarás un resumen de los pasos para convertir un clúster de Postgres existente en un clúster gestionado por Patroni. En los pasos asumimos que todos los nodos que forman parte del clúster existente están actualmente en ejecución y que *no* tienes la intención de cambiar la configuración de Postgres mientras la migración está en curso. Los pasos:

1.  Crea los usuarios de Postgres como se explica en la sección de [autenticación](/es/patroni/config/yaml#postgresql_settings) de la configuración de Patroni. Puedes encontrar comandos SQL de ejemplo para crear los usuarios en el bloque de código a continuación, en el que debes reemplazar los nombres de usuario y las contraseñas según tu entorno. Si ya tienes los usuarios correspondientes, puedes omitir este paso.

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

2.  Realiza los siguientes pasos en todos los nodos de Postgres. Realiza todos los pasos en un nodo antes de continuar con el siguiente. Comienza con el nodo primario y luego continúa con cada nodo en espera:

    1.  Si ejecutas Postgres a través de systemd, deshabilita la unidad de systemd de Postgres. Esto se hace porque Patroni gestiona el arranque y la detención del demonio de Postgres.
    2.  Crea un archivo de configuración YAML para Patroni. Para ello puedes usar las [herramientas de generación y validación de la configuración de Patroni](/es/patroni/config#validate_generate_config).
        - **Nota (específica para el nodo primario):** Si tienes slots de replicación en uso para la replicación entre los miembros del clúster, se recomienda que habilites `use_slots` y configures los slots de replicación existentes como permanentes mediante el elemento de configuración `slots`. Ten en cuenta que Patroni crea automáticamente slots de replicación para la replicación entre miembros, y elimina los slots de replicación que no reconoce, cuando `use_slots` está habilitado. La idea de usar slots permanentes aquí es permitir que tus slots existentes persistan mientras la migración a Patroni está en curso. Consulta [Opciones de configuración dinámica](/es/patroni/config/dynamic#dynamic) para más detalles.
    3.  Inicia Patroni usando la unidad de servicio de systemd `patroni`. Detecta automáticamente que Postgres ya se está ejecutando y comienza a monitorizar la instancia.

3.  Transfiere el «procedimiento de arranque» de Postgres a Patroni. Para hacerlo necesitas reiniciar los miembros del clúster mediante el comando [patronictl restart cluster-name member-name](/es/patroni/patronictl#patronictl_restart_parameters). Para minimizar el tiempo de inactividad quizás quieras dividir este paso en:

    1.  Reinicio inmediato de los nodos en espera.
    2.  Reinicio programado del nodo primario dentro de una ventana de mantenimiento.

4.  Si configuraste slots permanentes en el paso `2.2.`, debes eliminarlos de la configuración de `slots` mediante el comando [patronictl edit-config cluster-name](/es/patroni/patronictl#patronictl_edit_config_parameters) una vez que el `restart_lsn` de los slots creados por Patroni haya alcanzado el `restart_lsn` de los slots originales de los miembros correspondientes. Al eliminar los slots de la configuración de `slots` permitirás que Patroni descarte los slots originales de tu clúster cuando ya no sean necesarios. A continuación puedes encontrar una consulta de ejemplo para comprobar el `restart_lsn` de un par de slots, de modo que puedas compararlos:

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

## Actualización de versión principal de PostgreSQL {#major-upgrade-of-postgresql-version}

El procedimiento para una actualización de versión principal con `pg_upgrade` es:

1.  Detén Patroni
2.  Actualiza los binarios de PostgreSQL y ejecuta [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) en el nodo primario
3.  Actualiza patroni.yml
4.  Elimina la clave initialize del DCS o borra el estado completo del clúster del DCS. Lo segundo puede lograrse ejecutando [patronictl remove cluster-name](/es/patroni/patronictl#patronictl_remove_parameters) . Esto es necesario porque el nuevo clúster de PostgreSQL se inicializa con initdb, lo que le da un nuevo identificador de sistema de PostgreSQL.
5.  Si borraste el estado del clúster en el paso anterior, es posible que desees copiar patroni.dynamic.json del directorio de datos antiguo al nuevo. Te ayudará a conservar algunos parámetros de PostgreSQL que habías configurado antes.
6.  Inicia Patroni en el nodo primario.
7.  Actualiza los binarios de PostgreSQL, actualiza patroni.yml y borra el data_dir en los nodos en espera.
8.  Inicia Patroni en los nodos en espera y espera a que la replicación se complete.

PostgreSQL no admite ejecutar pg_upgrade en los nodos en espera. Si sabes lo que haces, puedes probar el procedimiento con rsync descrito en <https://www.postgresql.org/docs/current/pgupgrade.html> en lugar de borrar el data_dir en los nodos en espera. Sin embargo, la forma más segura es dejar que Patroni replique los datos por ti.

--------

## Preguntas frecuentes {#faq}

- Durante el arranque de Patroni, Patroni avisa de que no puede enlazar al puerto de PostgreSQL.

  Necesitas verificar `listen_addresses` y `port` en `postgresql.conf` y `postgresql.listen` en `patroni.yml`. No olvides que `pg_hba.conf` debe permitir dicho acceso.

- Después de pedir a Patroni que reinicie el nodo, PostgreSQL muestra el mensaje de error `could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory`

  Puede significar varias cosas según cómo gestiones la configuración de PostgreSQL. Si especificaste `postgresql.config_dir`, Patroni genera el `pg_hba.conf` basándose en las opciones de la sección [bootstrap](/es/patroni/config/yaml#bootstrap_settings) solo cuando realiza el bootstrap de un clúster nuevo. En este escenario el `PGDATA` no estaba vacío, por lo tanto no hubo bootstrap. Este archivo debe existir previamente.
