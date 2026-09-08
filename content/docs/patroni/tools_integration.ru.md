---
title: "Интеграция с другими инструментами"
linkTitle: "Интеграция инструментов"
weight: 150
icon: fas fa-puzzle-piece
description: "Интеграция Patroni с внешними инструментами резервного копирования и оркестрации."
module: [PATRONI]
categories: [Концепция]
aliases: [/patroni/tools_integration/]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni способен интегрироваться с другими инструментами в вашем стеке. В этом разделе вы найдете список примеров, которые, хотя и не являются исчерпывающими, могут дать вам идеи о том, как Patroni может интегрироваться с другими инструментами.

--------

## Barman {#barman}

Patroni предоставляет приложение с именем `patroni_barman`, в котором реализована логика взаимодействия с `pg-backup-api`, что позволяет выполнять операции Barman удалённо.

У данного приложения в настоящее время имеется несколько подкоманд: `recover` и `config-switch`.

### patroni_barman восстановить {#patroni_barman-recover}

Подкоманда `recover` может использоваться в качестве пользовательской процедуры начальной инициализации или пользовательского метода создания реплики. Дополнительную информацию об этом см. в [replica_imaging_and_bootstrap](/ru/docs/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### patroni_barman config-switch {#patroni_barman-config-switch}

Подкоманда `config-switch` предназначена для использования в качестве обратного вызова `on_role_change` в Patroni. Например, предположим, что вы передаёте WAL-логи с текущего первичного сервера на хост Barman. В случае переключения при отказе в кластере вы можете захотеть начать передачу WAL-логов с нового первичного сервера. Это можно реализовать, используя `patroni_barman config-switch` в качестве `on_role_change` обратного вызова.

> [!NOTE]
> Эта подкоманда зависит от команды `barman config-switch`, отвечающей за переопределение конфигурации сервера Barman путём применения заранее определённой модели поверх текущей конфигурации. Эта команда доступна начиная с Barman 3.10. Дополнительные сведения см. в документации Barman.

Вот пример того, как можно настроить Patroni для применения модели конфигурации в случае повышения данного узла до первичного сервера:

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> `patroni_barman config-switch` требует, чтобы на хосте Barman были настроены как Barman, так и `pg-backup-api`, чтобы можно было выполнить удалённую `barman config-switch` через резервную копию API. Кроме того, требуется, чтобы были предварительно настроены модели Barman для применения. В приведённом примере используется подмножество доступных параметров. Дополнительную информацию можно получить, выполнив `patroni_barman config-switch --help`, а также, ознакомившись с документацией Barman.
