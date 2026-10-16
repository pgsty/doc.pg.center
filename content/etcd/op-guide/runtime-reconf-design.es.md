---
title: Diseño de la reconfiguración en tiempo de ejecución
weight: 4650
description: Diseño de los comandos de reconfiguración en tiempo de ejecución de etcd
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-reconf-design.md"
---

La reconfiguración en tiempo de ejecución es una de las funcionalidades más difíciles y propensas a errores en un sistema distribuido, especialmente en un sistema basado en consenso como etcd.

Sigue leyendo para conocer el diseño de los comandos de reconfiguración en tiempo de ejecución de etcd y cómo abordamos estos problemas.

## Los cambios de configuración en dos fases mantienen seguro el clúster {#two-phase-config-changes-keep-the-cluster-safe}

En etcd, toda reconfiguración en tiempo de ejecución debe pasar por [dos fases][add-member] por razones de seguridad. Por ejemplo, para añadir un miembro, primero informa al clúster de la nueva configuración y luego inicia el miembro nuevo.

Fase 1 - Informar al clúster de la nueva configuración

Para añadir un miembro a un clúster de etcd, realiza una llamada a la API para solicitar que se añada un miembro nuevo al clúster. Esta es la única forma de añadir un miembro nuevo a un clúster existente. La llamada a la API devuelve el control cuando el clúster llega a un acuerdo sobre el cambio de configuración.

Fase 2 - Iniciar el miembro nuevo

Para incorporar el miembro nuevo de etcd al clúster existente, especifica el `initial-cluster` correcto y establece `initial-cluster-state` en `existing`. Cuando el miembro arranca, contacta primero con el clúster existente y comprueba que la configuración actual del clúster coincide con la esperada, especificada en `initial-cluster`. Cuando el miembro nuevo arranca con éxito, el clúster ha alcanzado la configuración esperada.

Al dividir el proceso en dos fases discretas, se obliga a los usuarios a ser explícitos respecto a los cambios en la pertenencia al clúster. Esto en realidad da a los usuarios más flexibilidad y facilita el razonamiento. Por ejemplo, si se intenta añadir un miembro nuevo con el mismo ID que un miembro existente en un clúster de etcd, la acción fallará inmediatamente durante la fase uno sin afectar al clúster en ejecución. Se proporciona una protección similar para evitar añadir miembros nuevos por error. Si un miembro nuevo de etcd intenta unirse al clúster antes de que el clúster haya aceptado el cambio de configuración, no será aceptado por el clúster.

Sin el flujo de trabajo explícito en torno a la pertenencia al clúster, etcd sería vulnerable a cambios inesperados en la pertenencia al clúster. Por ejemplo, si etcd se ejecuta bajo un sistema de inicialización como systemd, etcd se reiniciaría después de ser eliminado mediante la API de pertenencia e intentaría reincorporarse al clúster al arrancar. Este ciclo se repetiría cada vez que se eliminara un miembro mediante la API y systemd estuviera configurado para reiniciar etcd tras un fallo, lo cual es inesperado.

Esperamos que la reconfiguración en tiempo de ejecución sea una operación poco frecuente. Decidimos mantenerla explícita y dirigida por el usuario para garantizar la seguridad de la configuración y mantener el clúster funcionando siempre sin problemas bajo control explícito.

## La pérdida permanente del cuórum requiere un clúster nuevo {#permanent-loss-of-quorum-requires-new-cluster}

Si un clúster pierde permanentemente una mayoría de sus miembros, será necesario iniciar un clúster nuevo a partir de un directorio de datos antiguo para recuperar el estado anterior.

Es totalmente posible forzar la eliminación de los miembros fallidos del clúster existente para recuperarse. Sin embargo, decidimos no admitir este método porque omite la fase normal de confirmación del consenso, lo cual es inseguro. Si el miembro a eliminar no está realmente muerto o se elimina a la fuerza a través de diferentes miembros del mismo clúster, etcd acabará con un clúster divergente con el mismo clusterID. Esto es muy peligroso y difícil de depurar/arreglar después.

Con un despliegue correcto, la posibilidad de una pérdida permanente de la mayoría es muy baja. Pero es un problema lo bastante grave como para merecer un cuidado especial. Sugerimos encarecidamente leer la [documentación de recuperación ante desastres][disaster-recovery] y prepararse para una pérdida permanente de la mayoría antes de poner etcd en producción.

## No uses el servicio de descubrimiento público para la reconfiguración en tiempo de ejecución {#do-not-use-public-discovery-service-for-runtime-reconfiguration}

El servicio de descubrimiento público solo debe usarse para arrancar (bootstrap) un clúster. Para incorporar un miembro a un clúster existente, usa la API de reconfiguración en tiempo de ejecución.

El servicio de descubrimiento está diseñado para arrancar un clúster de etcd en un entorno cloud, cuando las direcciones IP de todos los miembros no se conocen de antemano. Tras arrancar un clúster con éxito, las direcciones IP de todos los miembros son conocidas. Técnicamente, el servicio de descubrimiento ya no debería ser necesario.

Parece que usar el servicio de descubrimiento público es una forma cómoda de hacer reconfiguración en tiempo de ejecución; al fin y al cabo, el servicio de descubrimiento ya tiene toda la información de configuración del clúster. Sin embargo, depender del servicio de descubrimiento público trae problemas:

1. introduce dependencias externas para todo el ciclo de vida del clúster, no solo durante el arranque. Si hay un problema de red entre el clúster y el servicio de descubrimiento público, el clúster se verá afectado.

2. el servicio de descubrimiento público debe reflejar la configuración en tiempo de ejecución correcta del clúster durante todo su ciclo de vida. Tiene que proporcionar mecanismos de seguridad para evitar acciones maliciosas, y eso es difícil.

3. el servicio de descubrimiento público tiene que mantener decenas de miles de configuraciones de clústeres. El backend de nuestro servicio de descubrimiento público no está preparado para esa carga de trabajo.

Para tener un servicio de descubrimiento que admita la reconfiguración en tiempo de ejecución, la mejor opción es construir uno privado.

[add-member]: /es/etcd/op-guide/runtime-configuration/#add-a-new-member
[disaster-recovery]: /es/etcd/op-guide/recovery/
