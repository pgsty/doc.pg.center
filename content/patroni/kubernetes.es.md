---
title: "Uso de Patroni con Kubernetes"
linkTitle: "Uso con Kubernetes"
weight: 120
icon: fas fa-dharmachakra
description: "Uso de Patroni con objetos de Kubernetes, labels y descubrimiento de servicios."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
Patroni puede usar objetos de Kubernetes para almacenar el estado del clúster y gestionar la clave de líder. Esto lo hace capaz de operar Postgres en un entorno de Kubernetes sin ningún almacén de consistencia; es decir, no es necesario ejecutar un despliegue adicional de Etcd. Hay dos tipos diferentes de objetos de Kubernetes que Patroni puede usar para almacenar la clave de líder y las claves de configuración; el tipo de objeto se selecciona con la opción de configuración `kubernetes.use_endpoints` o la variable de entorno `PATRONI_KUBERNETES_USE_ENDPOINTS`.

--------

## Uso de Endpoints {#use-endpoints}

A pesar de que este es el modo recomendado, está desactivado de forma predeterminada por razones de compatibilidad. Cuando está activado, Patroni almacena la configuración del clúster y la clave de líder en los campos `metadata: annotations` de los respectivos `Endpoints` que crea. Cambiar de líder es más seguro que cuando se usan `ConfigMaps`, ya que tanto las anotaciones, que contienen la información del líder, como las direcciones reales que apuntan al pod del líder en ejecución se actualizan simultáneamente de una sola vez.

--------

## Uso de ConfigMaps {#use-configmaps}

En este modo, Patroni creará ConfigMaps en lugar de Endpoints y almacenará las claves dentro de los metadatos de esos ConfigMaps. Cambiar de líder requiere al menos dos actualizaciones, una al ConfigMap del líder y otra al Endpoint respectivo.

Para dirigir el tráfico al líder de Postgres necesitas configurar el servicio de Postgres de Kubernetes para que use el selector de labels con el `role_label` (configurado en la configuración de patroni).

Ten en cuenta que en algunos casos, por ejemplo al ejecutarse en OpenShift, no hay alternativa al uso de ConfigMaps.

--------

## Configuración {#configuration}

Las [opciones](/es/patroni/config/yaml#kubernetes_settings) de Patroni para Kubernetes y las [variables de entorno](/es/patroni/config/env#kubernetes_environment) se describen en los capítulos generales de la documentación.

<a id="kubernetes_role_values"></a>

### Personalizar el label de rol {#customize-role-label}

De forma predeterminada, Patroni establecerá los labels correspondientes en el pod en el que se ejecuta según el rol del nodo, como `role=primary`. La clave y el valor del label se pueden personalizar con `kubernetes.role_label`, `kubernetes.leader_label_value`, `kubernetes.follower_label_value` y `kubernetes.standby_leader_label_value`.

Ten en cuenta que si migras de los labels de rol predeterminados a unos personalizados, puedes reducir el tiempo de inactividad siguiendo estos pasos de migración:

1.  Añade un label temporal que use el valor de rol original para el pod con `kubernetes.tmp_role_label` (como `tmp_role`). Una vez que los pods se reinicien, obtendrán los siguientes labels establecidos por Patroni:

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

2.  Después de que todos los pods se hayan actualizado, modifica el selector del servicio para seleccionar el label temporal.

> ```yaml
> selector:
>   cluster-name: foo
>   tmp_role: primary
> ```

3.  Añade tu label de rol personalizado (p. ej., establece `kubernetes.leader_label_value=leader`). Una vez que los pods se reinicien, obtendrán los siguientes labels nuevos establecidos por Patroni:

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
>   tmp_role: primary
> ```

4.  Después de que todos los pods se hayan actualizado de nuevo, modifica el selector del servicio para usar el nuevo valor de rol.

> ```yaml
> selector:
>   cluster-name: foo
>   role: leader
> ```

5.  Finalmente, elimina el label temporal de tu configuración y actualiza todos los pods.

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
> ```

--------

## Ejemplos {#examples}

- La carpeta [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) del repositorio de Patroni contiene ejemplos de la imagen de Docker y del manifiesto de Kubernetes para probar la configuración de Patroni con Kubernetes. Ten en cuenta que, en su estado actual, no podrá usar PersistentVolumes debido a problemas de permisos.
- Puedes encontrar la imagen de Docker completa, capaz de usar Persistent Volumes, en el [proyecto Spilo](https://github.com/zalando/spilo).
- También hay un [chart de Helm](https://github.com/kubernetes/charts/tree/master/incubator/patroni) para desplegar la imagen de Spilo configurada con Patroni ejecutándose mediante Kubernetes.
- Para ejecutar tus clústeres de bases de datos a escala usando Patroni y Spilo, echa un vistazo al proyecto [postgres-operator](https://github.com/zalando/postgres-operator). Implementa el patrón de operador para gestionar clústeres de Spilo.
