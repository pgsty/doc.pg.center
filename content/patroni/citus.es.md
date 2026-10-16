---
title: "Soporte de Citus"
weight: 130
icon: fas fa-lemon
description: "Detalles de la integración de Patroni con el coordinador y los grupos de workers de Citus."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
Patroni hace que desplegar clústeres [Citus multinodo](https://docs.citusdata.com/en/stable/installation/multi_node.html) sea extremadamente simple.

--------

## TL;DR {#tldr}

Solo hay unas pocas reglas simples que debes seguir:

1.  La extensión de base de datos [Citus](https://github.com/citusdata/citus) para PostgreSQL debe estar disponible en todos los nodos. La versión mínima absoluta soportada de Citus es la 10.0, pero para aprovechar todas las ventajas de los switchovers y reinicios transparentes de los workers recomendamos usar al menos Citus 11.2.
2.  ¡El nombre del clúster (`scope`) debe ser el mismo para todos los nodos de Citus!
3.  Las credenciales del superusuario deben ser las mismas en el coordinador y en todos los nodos workers, y `pg_hba.conf` debe permitir el acceso de superusuario entre todos los nodos.
4.  El acceso a la [REST API](/es/patroni/config/yaml#restapi_settings) debe permitirse desde los nodos workers hacia el coordinador. Por ejemplo, las credenciales deben ser las mismas y, si están configurados, los certificados de cliente de los nodos workers deben ser aceptados por el coordinador.
5.  Añade la siguiente sección al `patroni.yaml`:

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

Después de eso, solo tienes que iniciar Patroni y se encargará del resto:

0.  Patroni establecerá `bootstrap.dcs.synchronous_mode` en [quorum](/es/patroni/replication_modes#quorum_mode) si no está establecido explícitamente en otro valor.
1.  La extensión [citus](/es/patroni/citus#citus) se añadirá automáticamente a `shared_preload_libraries`.
2.  Si `max_prepared_transactions` no está establecido explícitamente en la [configuración dinámica](/es/patroni/config/dynamic#dynamic) global, Patroni lo establecerá automáticamente en `2*max_connections`.
3.  El valor del GUC `citus.local_hostname` se ajustará de `localhost` al valor que Patroni esté utilizando para conectarse a la instancia local de PostgreSQL. A veces el valor debe ser diferente de `localhost` porque PostgreSQL podría no estar escuchando en él.
4.  La `citus.database` se creará automáticamente, seguida de `CREATE EXTENSION citus`.
5.  Las [credenciales](/es/patroni/config/yaml#postgresql_settings) actuales del superusuario se añadirán a la tabla `pg_dist_authinfo` para permitir la comunicación entre nodos. ¡No olvides actualizarlas si más tarde decides cambiar el usuario/contraseña/sslcert/sslkey del superusuario!
6.  El nodo primario del coordinador descubrirá automáticamente los nodos primarios de los workers y los añadirá a la tabla `pg_dist_node` mediante la función `citus_add_node()`.
7.  Patroni también mantendrá `pg_dist_node` en caso de que ocurra una conmutación por error o un switchover en los clústeres del coordinador o de los workers.

--------

## patronictl {#patronictl}

Los clústeres del coordinador y de los workers son clústeres PostgreSQL/Patroni físicamente diferentes que simplemente se agrupan lógicamente mediante la extensión de base de datos [Citus](https://github.com/citusdata/citus) para PostgreSQL. Por lo tanto, en la mayoría de los casos no es posible gestionarlos como una única entidad.

Esto se traduce en dos diferencias importantes en el comportamiento de [patronictl](/es/patroni/patronictl#patronictl) cuando `patroni.yaml` tiene la sección [citus](/es/patroni/citus#citus) en comparación con lo habitual:

1.  Los comandos `list` y `topology` muestran por defecto todos los miembros de la formación de Citus (coordinadores y workers). La nueva columna `Group` indica a qué grupo de Citus pertenecen.
2.  Para todos los comandos de [patronictl](/es/patroni/patronictl#patronictl) se introduce la nueva opción, llamada `--group`. Para algunos comandos, el valor predeterminado del grupo podría tomarse del `patroni.yaml`. Por ejemplo, [patronictl_pause](/es/patroni/patronictl#patronictl_pause) habilitará el modo de mantenimiento por defecto para el `group` establecido en la sección [citus](/es/patroni/citus#citus), pero por ejemplo para [patronictl_switchover](/es/patroni/patronictl#patronictl_switchover) o [patronictl_remove](/es/patroni/patronictl#patronictl_remove) el grupo debe especificarse explícitamente.

Un ejemplo de la salida de [patronictl_list](/es/patroni/patronictl#patronictl_list) para el clúster de Citus:

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

Si añadimos la opción `--group`, la salida cambiará a:

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

## Switchover de workers de Citus {#citus-worker-switchover}

Cuando se orquesta un switchover para un nodo worker de Citus, Citus ofrece la posibilidad de hacer que el switchover sea casi transparente para una aplicación. Como la aplicación se conecta al coordinador, que a su vez se conecta a los nodos workers, con Citus es posible pausar el tráfico SQL en el coordinador para los shards alojados en un nodo worker. El switchover entonces ocurre mientras el tráfico se mantiene en el coordinador, y se reanuda tan pronto como un nuevo nodo worker primario está listo para aceptar consultas de lectura y escritura.

Un ejemplo de [patronictl_switchover](/es/patroni/patronictl#patronictl_switchover) en el clúster de workers:

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

Y así es como se ve desde el lado del coordinador:

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

## Nodos secundarios {#secondary-nodes}

A partir de Patroni v4.0.0, los nodos secundarios de Citus sin la [etiqueta](/es/patroni/config/yaml#tags_settings) `noloadbalance` también se registran en `pg_dist_node`. Sin embargo, para utilizar nodos secundarios en consultas de solo lectura, las aplicaciones necesitan cambiar el GUC [citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum).

--------

## Vistazo al DCS {#peek-into-dcs}

El clúster de Citus (coordinador y workers) se almacena en el DCS como una flota de clústeres de Patroni agrupados lógicamente:

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

Se eligió este enfoque porque para la mayoría de los DCS permite obtener el clúster de Citus completo con una única solicitud de lectura recursiva. Solo los nodos coordinadores de Citus leen el árbol completo, porque tienen que descubrir los nodos workers. Los nodos workers leen solo el subárbol de su propio grupo y en algunos casos podrían leer el subárbol del grupo del coordinador.

--------

## Citus en Kubernetes {#citus-on-kubernetes}

Como Kubernetes no soporta estructuras jerárquicas, tuvimos que incluir el grupo de Citus en todos los objetos K8s que crea Patroni:

    batman-0-leader  # the leader config map for the coordinator
    batman-0-config  # the config map holding initialize, config, and history "keys"
    ...
    batman-1-leader  # the leader config map for worker group 1
    batman-1-config
    ...

Es decir, el patrón de nomenclatura es: `${scope}-${citus.group}-${type}`.

Patroni descubre todos los objetos de Kubernetes mediante el [selector de etiquetas](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors); por lo tanto, todos los Pods con Patroni&Citus y los Endpoints/ConfigMaps deben tener etiquetas que coincidan con el selector de etiquetas común, y Patroni debe configurarse para utilizarlos mediante los [ajustes](/es/patroni/config/yaml#kubernetes_settings) de Kubernetes o las [variables de entorno](/es/patroni/config/env#kubernetes_environment).

Un par de ejemplos de configuración de Patroni utilizando variables de entorno de los Pods:

1.  para el clúster del coordinador

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

2.  para el clúster de workers del grupo 2

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

Como habrás notado, ambos ejemplos tienen la etiqueta `citus-group` establecida. Esta etiqueta permite a Patroni identificar el objeto como perteneciente a un determinado grupo de Citus. Además de eso, también existe la variable de entorno `PATRONI_CITUS_GROUP`, que tiene el mismo valor que la etiqueta `citus-group`. Cuando Patroni crea nuevos objetos de Kubernetes, ConfigMaps o Endpoints, les pone automáticamente la etiqueta `citus-group: ${env.PATRONI_CITUS_GROUP}`:

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

Puedes encontrar un ejemplo completo del despliegue de Patroni en Kubernetes con soporte de Citus en la carpeta [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) del repositorio de Patroni.

Hay dos archivos importantes para ti:

1.  Dockerfile.citus
2.  citus_k8s.yaml

--------

## Actualizaciones de Citus y actualizaciones de versión mayor de PostgreSQL {#citus-upgrades-and-postgresql-major-upgrades}

Primero, lee acerca de cómo actualizar la versión de Citus en la [documentación](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html). Hay un pequeño cambio en el proceso. Al ejecutar la actualización, tienes que usar [patronictl_restart](/es/patroni/patronictl#patronictl_restart) en lugar de `systemctl restart` para reiniciar PostgreSQL.

La actualización de versión mayor de PostgreSQL con Citus es un poco más compleja. Tendrás que combinar las técnicas utilizadas en la documentación de Citus sobre actualizaciones de versión mayor y la documentación de Patroni sobre la [actualización de versión mayor de PostgreSQL](/es/patroni/existing_data#major_upgrade). Ten en cuenta que el clúster de Citus consta de muchos clústeres de Patroni (coordinador y workers) y que todos tienen que actualizarse de forma independiente.
