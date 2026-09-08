---
title: "Использование Patroni с Kubernetes"
linkTitle: "Использование с Kubernetes"
weight: 120
icon: fas fa-dharmachakra
description: "Использование Patroni с объектами Kubernetes, метками и обнаружением сервисов."
module: [PATRONI]
categories: [Задача]
aliases: [/patroni/kubernetes/]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
Patroni может использовать объекты Kubernetes для хранения состояния кластера и управления ключом лидера. Это позволяет работать с Postgres в среде Kubernetes без дополнительного хранилища согласованности, то есть не требуется запуск отдельного развёртывания etcd. Patroni может использовать два различных типа объектов Kubernetes для хранения ключей лидера и конфигурации, которые настраиваются с помощью переменной среды `kubernetes.use_endpoints` или `PATRONI_KUBERNETES_USE_ENDPOINTS`.

--------

## Используйте конечные точки {#use-endpoints}

Несмотря на то что этот режим рекомендуется, по соображениям совместимости он отключён по умолчанию. Когда он включён, Patroni хранит конфигурацию кластера и ключ лидера в полях `metadata: annotations` соответствующих `Endpoints`, которые он создаёт. Смена лидера безопаснее, чем при использовании `ConfigMaps`, поскольку одновременно обновляются и аннотации, содержащие информацию о лидере, и фактические адреса, указывающие на запущенный под-лидер.

--------

## Используйте ConfigMaps {#use-configmaps}

В этом режиме Patroni будет создавать ConfigMaps вместо Endpoints и хранить ключи внутри метаданных этих ConfigMaps. Смена лидера требует как минимум два обновления: одно — для ConfigMap лидера, другое — для соответствующего Endpoint.

Чтобы направить трафик на лидера Postgres, необходимо настроить сервис Postgres в Kubernetes для использования селектора меток с `role_label` (настроено в конфигурации Patroni).

Примечание. В некоторых случаях, например при работе на OpenShift, нет альтернативы использованию ConfigMaps.

--------

## Конфигурация {#configuration}

[Настройки](/ru/docs/patroni/config/yaml#kubernetes_settings) Kubernetes для Patroni и [переменные окружения](/ru/docs/patroni/config/env#kubernetes_environment) описаны в общих главах документации.

<a id="kubernetes_role_values"></a>

### Настройка метки роли {#customize-role-label}

По умолчанию Patroni будет устанавливать соответствующие метки в поде, в котором выполняется, на основе роли узла, например `role=primary`. Ключ и значение метки можно настроить с помощью `kubernetes.role_label`, `kubernetes.leader_label_value`, `kubernetes.follower_label_value` и `kubernetes.standby_leader_label_value`.

Примечание. Если вы переносите роль с использованием меток по умолчанию на пользовательские, то можете сократить время простоя, следуя шагам миграции:

1. Добавьте временный метку, используя исходное значение роли, для пода с `kubernetes.tmp_role_label` (например, `tmp_role`). После перезапуска подов Patroni установит следующие метки:

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

2. После обновления всех подов измените селектор сервиса так, чтобы он выбирал временный метку.

> ```yaml
> selector:
>   cluster-name: foo
>   tmp_role: primary
> ```

3. Добавьте метку пользовательской роли (e.g, установите `kubernetes.leader_label_value=primary`). После перезапуска подов Patroni установит следующие новые метки:

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

4. После того как все поды будут обновлены повторно, измените селектор сервиса для использования нового значения роли.

> ```yaml
> selector:
>   cluster-name: foo
>   role: primary
> ```

5. Наконец, удалите временный метку из вашей конфигурации и обновите все поды.

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
> ```

--------

## Примеры {#examples}

- Папка [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) репозитория Patroni содержит примеры образа Docker и манифеста Kubernetes для тестирования настройки Patroni в Kubernetes. Примечание: в текущем состоянии невозможно использовать PersistentVolumes из-за проблем с разрешениями.
- Полнофункциональный образ Docker, способный использовать PersistentVolumes, можно найти в проекте [Spilo](https://github.com/zalando/spilo).
- Также доступен [Helm-чарт](https://github.com/kubernetes/charts/tree/master/incubator/patroni) для развертывания образа Spilo, настроенного на работу с Patroni в Kubernetes.
- Для масштабного развертывания кластеров баз данных с использованием Patroni и Spilo обратите внимание на проект [postgres-operator](https://github.com/zalando/postgres-operator). Он реализует паттерн оператора для управления кластерами Spilo.
