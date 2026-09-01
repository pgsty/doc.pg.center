---
title: "Поддержка Citus"
weight: 130
icon: fas fa-lemon
description: "Patroni сведения об интеграции для групп координаторов и рабов Citus."
module: [PATRONI]
categories: [Концепция]
aliases: [/docs/patroni/citus/]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
Patroni делает развертывание кластеров [Multi-Node Citus](https://docs.citusdata.com/en/stable/installation/multi_node.html) чрезвычайно простым.

--------

## TL;DR {#tldr}

Существует лишь несколько простых правил, которым необходимо следовать:

1.  Расширение базы данных [Citus](https://github.com/citusdata/citus) для PostgreSQL должно быть доступно на всех узлах. Абсолютно минимальная поддерживаемая версия Citus — 10.0, но для использования всех преимуществ прозрачных плановых переключений и перезапусков рабочих узлов рекомендуется как минимум Citus 11.2.
2.  Имя кластера (`scope`) должно быть одинаковым для всех узлов Citus!
3.  Учётные данные суперпользователя должны быть одинаковыми на координаторе и всех рабочих узлах, а `pg_hba.conf` должен разрешать доступ суперпользователя между всеми узлами.
4.  [REST API](/ru/patroni/config/yaml#restapi_settings) доступ должен быть разрешён с узлов-работников к координатору. E.g, учётные данные должны быть одинаковыми, и, если настроены, клиентские сертификаты с узлов-работников должны быть приняты координатором.  
5.  Добавьте следующий раздел в `patroni.yaml`:

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

После этого вам нужно просто запустить Patroni, и он сам займётся остальным:

0. Patroni установит `bootstrap.dcs.synchronous_mode` в [quorum](/ru/patroni/replication_modes#quorum_mode), если значение не задано явно другим образом.  
1. Расширение [citus](/ru/patroni/citus#citus) будет автоматически добавлено в `shared_preload_libraries`.  
2. Если `max_prepared_transactions` не задано явно в глобальной [динамической конфигурации](/ru/patroni/config/dynamic#dynamic), Patroni автоматически установит его в `2*max_connections`.
3. Значение `citus.local_hostname` GUC будет скорректировано с `localhost` на значение, используемое Patroni для подключения к локальному экземпляру PostgreSQL. Значение иногда должно отличаться от `localhost`, поскольку PostgreSQL может не слушать на нём.  
4. Узел `citus.database` будет автоматически создан после `CREATE EXTENSION citus`.  
5. Текущие учётные данные суперпользователя [credentials](/ru/patroni/config/yaml#postgresql_settings) будут добавлены в таблицу `pg_dist_authinfo` для обеспечения взаимодействия между узлами. Не забудьте обновить их, если позже вы решите изменить имя пользователя/пароль/sslcert/sslkey суперпользователя!
6. Координирующий первичный узел автоматически обнаружит рабочие первичные узлы и добавит их в таблицу `pg_dist_node` с использованием функции `citus_add_node()`.  
7. Patroni также будет поддерживать `pg_dist_node` в случае переключения при отказе/планового переключения в координирующем или рабочем кластерах.

--------

## patronictl {#patronictl}

Координаторские и рабочие кластеры — это физически разные кластеры PostgreSQL/Patroni, которые логически объединены с помощью расширения базы данных [Citus](https://github.com/citusdata/citus) для PostgreSQL. Следовательно, в большинстве случаев невозможно управлять ими как единым целым.

Это приводит к двум основным различиям в поведении [patronictl](/ru/patroni/patronictl#patronictl) при наличии секции `patroni.yaml` с [citus](/ru/patroni/citus#citus) по сравнению со стандартным поведением:

1. Параметры `list` и `topology` по умолчанию выводят всех участников формирования Citus (координаторов и рабочих). Новая колонка `Group` указывает, к какой группе Citus они принадлежат.
2. Для всех команд [patronictl](/ru/patroni/patronictl#patronictl) введён новый параметр, называемый `--group`. Для некоторых команд значение по умолчанию для группы может быть взято из `patroni.yaml`. Например, команда [patronictl_pause](/ru/patroni/patronictl#patronictl_pause) по умолчанию включит режим обслуживания для `group`, указанного в секции [citus](/ru/patroni/citus#citus), но, например, для [patronictl_switchover](/ru/patroni/patronictl#patronictl_switchover) или [patronictl_remove](/ru/patroni/patronictl#patronictl_remove) группа должна быть указана явно.

Пример вывода [patronictl_list](/ru/patroni/patronictl#patronictl_list) для кластера Citus:

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     1 | work1-2 | 172.27.0.2  | Leader         | running |  1 |             |     |            |     |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

Если добавить параметр `--group`, вывод изменится следующим образом:

    postgres@coord1:~$ patronictl list demo --group 0
    + Citus cluster: demo (group: 0, 7179854923829112860) -+-------------+-----+------------+-----+
    | Member | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    | coord1 | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord2 | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord3 | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+

    postgres@coord1:~$ patronictl list demo --group 1
    + Citus cluster: demo (group: 1, 7179854923881963547) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work1-1 | 172.27.0.8 | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    | work1-2 | 172.27.0.2 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+

--------

## Плановое переключение рабочего узла Citus {#citus-worker-switchover}

Когда для рабочего узла Citus выполняется плановое переключение, Citus позволяет сделать его практически прозрачным для приложения. Приложение подключается к координатору, а тот — к рабочим узлам, поэтому Citus может [приостановить](/ru/patroni/pause#pause) трафик SQL на координаторе для шардов, размещённых на рабочем узле. Затем плановое переключение выполняется, пока трафик удерживается на координаторе, и возобновляется, как только новый первичный рабочий узел будет готов принимать запросы на чтение и запись.

Пример [patronictl_switchover](/ru/patroni/patronictl#patronictl_switchover) на рабочем кластере:

    postgres@coord1:~$ patronictl switchover demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    Citus group: 2
    Primary [work2-2]:
    Candidate ['work2-1'] []:
    When should the switchover take place (e.g. 2024-08-26T08:02 )  [now]:
    Current cluster topology
    + Citus cluster: demo (group: 2, 7179854924063375386) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work2-1 | 172.27.0.5 | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    | work2-2 | 172.27.0.7 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    Are you sure you want to switchover cluster demo, demoting current primary work2-2? [y/N]: y
    2024-08-26 07:02:40.33003 Successfully switched over to "work2-1"
    + Citus cluster: demo (group: 2, 7179854924063375386) --------+---------+------------+---------+
    | Member  | Host       | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+
    | work2-1 | 172.27.0.5 | Leader  | running |  1 |             |         |            |         |
    | work2-2 | 172.27.0.7 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Leader         | running |  2 |             |     |            |     |
    |     2 | work2-2 | 172.27.0.7  | Quorum Standby | running |  2 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

И так выглядит это со стороны координатора:

    # The worker primary notifies the coordinator that it is going to execute "pg_ctl stop".
    2024-08-26 07:02:38,636 DEBUG: query(BEGIN, ())
    2024-08-26 07:02:38,636 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.7-demoted', 5432, 10000))
    # From this moment all application traffic on the coordinator to the worker group 2 is paused.

    # The old worker primary is assigned as a secondary.
    2024-08-26 07:02:40,084 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (7, '172.19.0.7', 5432, 10000))

    # The future worker primary notifies the coordinator that it acquired the leader lock in DCS and about to run "pg_ctl promote".
    2024-08-26 07:02:40,085 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.5', 5432, 10000))

    # The new worker primary just finished promote and notifies coordinator that it is ready to accept read-write traffic.
    2024-08-26 07:02:41,485 DEBUG: query(COMMIT, ())
    # From this moment the application traffic on the coordinator to the worker group 2 is unblocked.

--------

## Вторичные узлы {#secondary-nodes}

Начиная с Patroni v4.0.0 вторичные узлы Citus без `noloadbalance` [тега](/ru/patroni/config/yaml#tags_settings) также регистрируются в `pg_dist_node`. Однако для использования вторичных узлов в запросах только для чтения приложениям необходимо изменить [citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum) GUC.

--------

## Загляните в DCS {#peek-into-dcs}

Кластер Citus (координатор и рабочие узлы) хранится в DCS в виде флота кластеров Patroni, логически объединённых вместе:

    /service/batman/              # scope=batman
    /service/batman/0/            # citus.group=0, coordinator
    /service/batman/0/initialize
    /service/batman/0/leader
    /service/batman/0/members/
    /service/batman/0/members/m1
    /service/batman/0/members/m2
    /service/batman/1/            # citus.group=1, worker
    /service/batman/1/initialize
    /service/batman/1/leader
    /service/batman/1/members/
    /service/batman/1/members/m3
    /service/batman/1/members/m4
    ...

Такой подход был выбран потому, что для большинства DCS становится возможным получить весь кластер Citus с помощью одного рекурсивного запроса на чтение. Только координирующие узлы Citus читают всю дерево, поскольку им необходимо обнаружить рабочие узлы. Рабочие узлы читают только поддерево для собственной группы, а в некоторых случаях — поддерево группы координатора.

--------

## Citus на Kubernetes {#citus-on-kubernetes}

Поскольку Kubernetes не поддерживает иерархические структуры, нам пришлось включить группу citus во все объекты K8s, которые создает Patroni:

    batman-0-leader  # the leader config map for the coordinator
    batman-0-config  # the config map holding initialize, config, and history "keys"
    ...
    batman-1-leader  # the leader config map for worker group 1
    batman-1-config
    ...

I.e., шаблон имён имеет вид: `${scope}-${citus.group}-${type}`.

Patroni обнаруживает все объекты Kubernetes с помощью [селектора меток](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors), поэтому все Pods с Patroni&Citus, а также Endpoints/ConfigMaps должны иметь одинаковые метки, а Patroni необходимо настроить на их использование через [параметры](/ru/patroni/config/yaml#kubernetes_settings) Kubernetes или `environment variables
<kubernetes_environment>`.

Несколько примеров конфигурации Patroni с использованием переменных среды Pod:

1. для кластера-координатора

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "0"
    citus-type: coordinator
    cluster-name: citusdemo
  name: citusdemo-0-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "0"
```

2. для рабочего кластера из группы 2

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "2"
    citus-type: worker
    cluster-name: citusdemo
  name: citusdemo-2-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "2"
```

Как вы могли заметить, в обоих примерах установлен метка `citus-group`. Эта метка позволяет Patroni определять объект как принадлежащий определённой группе Citus. Кроме того, существует также переменная среды `PATRONI_CITUS_GROUP`, значение которой совпадает со значением метки `citus-group`. При создании новых объектов Kubernetes — ConfigMaps или Endpoints — Patroni автоматически добавляет им метку `citus-group: ${env.PATRONI_CITUS_GROUP}`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: citusdemo-0-leader  # Is generated as ${env.PATRONI_SCOPE}-${env.PATRONI_CITUS_GROUP}-leader
  labels:
    application: patroni    # Is set from the ${env.PATRONI_KUBERNETES_LABELS}
    cluster-name: citusdemo # Is automatically set from the ${env.PATRONI_SCOPE}
    citus-group: '0'        # Is automatically set from the ${env.PATRONI_CITUS_GROUP}
```

Вы можете найти полный пример развёртывания Patroni на Kubernetes с поддержкой Citus в папке [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) репозитория Patroni.

Для вас существуют два важных файла:

1.  Dockerfile.citus
2.  citus_k8s.yaml

--------

## Обновление Citus и обновление PostgreSQL версии {#citus-upgrades-and-postgresql-major-upgrades}

Сначала ознакомьтесь с обновлением версии Citus в [документации](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html). В процессе имеется незначительное изменение. При выполнении обновления необходимо использовать [patronictl_restart](/ru/patroni/patronictl#patronictl_restart) вместо `systemctl restart` для перезапуска PostgreSQL.

Обновление основной версии PostgreSQL с использованием Citus требует более сложных действий. Вам необходимо объединить методы, описанные в документации Citus по обновлению основных версий, и документации Patroni по `PostgreSQL major upgrade<major_upgrade>`. Учитывайте, что кластер Citus состоит из множества кластеров Patroni (координаторов и рабочих узлов), и каждый из них должен быть обновлён независимо.
