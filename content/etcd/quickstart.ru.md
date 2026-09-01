---
title: Быстрый старт
weight: 900
description: Запустите etcd менее чем за 5 минут!
icon: fa-solid fa-rocket
categories: [Руководство]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/quickstart.md"
---

Следуйте этим инструкциям, чтобы локально установить, запустить и проверить кластер etcd
из одного участника:

 1. Установите etcd из готовых бинарных файлов или исходного кода. Подробности см. в разделе
    [Установка][].

    > [!WARNING]
    > **Важно**: обязательно выполните последний
    > шаг инструкции по установке и убедитесь, что `etcd` доступен в пути поиска.

 2. Запустите `etcd`:

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **Примечание**: вывод `etcd` представляет собой
    > [журналы](/ru/etcd/op-guide/configuration/#logging) &mdash; сообщения уровня info можно
    > игнорировать.

 3. В **другом терминале** задайте ключ с помощью `etcdctl`:

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. В том же терминале получите значение ключа:

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## Что дальше? {#whats-next}

Дополнительные способы настройки и использования etcd описаны на следующих страницах:

- Для разработчиков:
  - Изучите gRPC [API][].
  - Найдите [языковые библиотеки и инструменты][integrations].

- Для операторов и администраторов:
  - Настройте [кластер из нескольких машин][clustering].
  - Узнайте, как [настроить][configure] etcd.
  - Используйте TLS, чтобы [защитить кластер etcd][security].
  - [Настройте производительность etcd][tuning].

[api]: /ru/etcd/learning/api
[clustering]: /ru/etcd/op-guide/clustering
[configure]: /ru/etcd/op-guide/configuration
[integrations]: /ru/etcd/integrations
[security]: /ru/etcd/op-guide/security
[tuning]: /ru/etcd/tuning
[Install]: /ru/etcd/install/
