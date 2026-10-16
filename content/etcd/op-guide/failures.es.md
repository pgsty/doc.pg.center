---
title: Modos de fallo
weight: 4250
description: Tipos de fallos y la tolerancia de etcd ante ellos
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/failures.md"
---

Los fallos son habituales en un despliegue de máquinas a gran escala. Una máquina falla cuando su hardware o su software funcionan de manera incorrecta. Varias máquinas fallan a la vez cuando se producen cortes de energía o problemas de red. También pueden ocurrir varios tipos de fallos simultáneamente; es casi imposible enumerar todos los casos de fallo posibles.

En esta sección se catalogan los tipos de fallos y se analiza cómo etcd está diseñado para tolerarlos. La mayoría de los usuarios, si no todos, pueden asignar un fallo concreto a uno de estos tipos. Para prepararse ante fallos raros o [irrecuperables][unrecoverable], siempre realiza una [copia de seguridad][backup] del clúster de etcd.

## Fallo de unas pocas réplicas {#minor-followers-failure}

Cuando fallan réplicas pero menos de la mitad de todos los miembros del clúster está indisponible y el líder sigue disponible, el clúster de etcd puede seguir aceptando solicitudes y avanzar sin ninguna interrupción grave. Por ejemplo, dos fallos de réplicas no afectan a la operación de un clúster de etcd de cinco miembros. Sin embargo, los clientes pierden la conectividad con los miembros fallidos. Las bibliotecas cliente deberían ocultar estas interrupciones a los usuarios para las solicitudes de lectura reconectándose automáticamente a otros miembros. Los operadores deben esperar que la carga del sistema sobre los demás miembros aumente debido a las reconexiones.

## Fallo del líder {#leader-failure}

Cuando falla un líder, el clúster de etcd elige automáticamente un nuevo líder. La elección no ocurre de forma instantánea en cuanto falla el líder. Elegir un nuevo líder toma aproximadamente un tiempo de espera de elección, ya que el modelo de detección de fallos está basado en tiempos de espera.

Durante la elección del líder, el clúster no puede procesar ninguna escritura. Las solicitudes de escritura enviadas durante la elección se ponen en cola para su procesamiento hasta que se elige un nuevo líder.

Las escrituras ya enviadas al líder antiguo pero aún no confirmadas pueden perderse. El nuevo líder tiene la facultad de reescribir cualquier entrada no confirmada del líder anterior. Desde la perspectiva del usuario, algunas solicitudes de escritura pueden agotar su tiempo de espera después de una nueva elección de líder. Sin embargo, nunca se pierde ninguna escritura confirmada.

El nuevo líder extiende automáticamente los tiempos de espera de todas las concesiones. Este mecanismo garantiza que una concesión no expire antes del TTL otorgado, incluso si fue otorgada por el líder antiguo.

## Fallo de la mayoría {#majority-failure}

Cuando falla la mayoría de los miembros del clúster, el clúster de etcd falla y no puede aceptar más escrituras.

El clúster de etcd solo puede recuperarse de un fallo de la mayoría cuando la mayoría de los miembros vuelve a estar disponible. Si la mayoría de los miembros no puede volver a estar en línea, el operador debe iniciar la [recuperación ante desastres][unrecoverable] para recuperar el clúster.

En cuanto funciona una mayoría de los miembros, el clúster de etcd elige automáticamente un nuevo líder y vuelve a un estado saludable. El nuevo líder extiende automáticamente los tiempos de espera de todas las concesiones. Este mecanismo garantiza que ninguna concesión expire debido a una indisponibilidad del lado del servidor.

## Partición de red {#network-partition}

Una partición de red es similar a un fallo de unas pocas réplicas o a un fallo del líder. Una partición de red divide el clúster de etcd en dos partes; una con una mayoría de miembros y la otra con una minoría de miembros. El lado de la mayoría se convierte en el clúster disponible y el lado de la minoría queda indisponible. No existe el «split-brain» en etcd porque los miembros del clúster se añaden o eliminan explícitamente y cada uno de estos cambios es aprobado por la mayoría actual de los miembros.

Si el líder está en el lado de la mayoría, entonces, desde el punto de vista de la mayoría, el fallo es un fallo de una minoría de réplicas. Si el líder está en el lado de la minoría, entonces se trata de un fallo del líder. El líder del lado de la minoría abandona su cargo y el lado de la mayoría elige un nuevo líder.

Una vez que la partición de red se resuelve, el lado de la minoría reconoce automáticamente al líder del lado de la mayoría y recupera su estado.

## Fallo durante el arranque inicial {#failure-during-bootstrapping}

El arranque inicial de un clúster solo tiene éxito si todos los miembros requeridos se inician correctamente. Si ocurre cualquier fallo durante el arranque inicial, elimina los directorios de datos en todos los miembros y vuelve a inicializar el clúster con un cluster-token nuevo o un token de descubrimiento nuevo.

Por supuesto, es posible recuperar un clúster cuyo arranque inicial falló, igual que se recupera un clúster en ejecución. Sin embargo, casi siempre recuperar ese clúster toma más tiempo y recursos que iniciar uno nuevo, ya que no hay datos que recuperar.

[backup]: /es/etcd/op-guide/maintenance/#snapshot-backup
[unrecoverable]: /es/etcd/op-guide/recovery/
