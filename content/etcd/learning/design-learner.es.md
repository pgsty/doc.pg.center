---
title: "Diseño del aprendiz de etcd"
weight: 2375
description: Mitigación de los desafíos comunes de la reconfiguración de la composición del clúster
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-learner.md"
---

Aprendiz de etcd {#etcd-learner}
============

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


Contexto {#background}
==========

La reconfiguración de la composición del clúster ha sido uno de los mayores desafíos operativos. Repasemos los desafíos comunes.

### 1. Un miembro nuevo del clúster sobrecarga al líder {#1-new-cluster-member-overloads-leader}
Un miembro de etcd recién incorporado empieza sin datos, por lo que exige más actualizaciones al líder hasta que alcanza los registros del líder. Entonces la red del líder tiene más probabilidad de sobrecargarse, bloqueando o descartando los latidos que el líder envía a las réplicas. En tal caso, una réplica puede agotar su tiempo de espera de elección e iniciar una nueva elección de líder. Es decir, un clúster con un miembro nuevo es más vulnerable a una elección de líder. Tanto la elección de líder como la posterior propagación de actualizaciones al miembro nuevo tienden a causar períodos de indisponibilidad del clúster (ver *Figura 1*).

![servidor-miembro-aprendiz-figura-01](/etcd/learning/img/server-learner-figure-01.png)

### 2. Escenarios de particiones de red {#2-network-partitions-scenarios}
¿Qué ocurre si se produce una partición de red? Depende de la partición del líder. Si el líder todavía mantiene el cuórum activo, el clúster seguiría funcionando (ver *Figura 2*).

![servidor-miembro-aprendiz-figura-02](/etcd/learning/img/server-learner-figure-02.png)

#### 2.1 Aislamiento del líder {#21-leader-isolation}
¿Qué ocurre si el líder queda aislado del resto del clúster? El líder supervisa el progreso de cada réplica. Cuando el líder pierde la conectividad con el cuórum, revierte a réplica, lo que afectará la disponibilidad del clúster (ver *Figura 3*).

![servidor-miembro-aprendiz-figura-03](/etcd/learning/img/server-learner-figure-03.png)

Cuando se añade un nodo nuevo a un clúster de 3 nodos, el tamaño del clúster pasa a ser 4 y el tamaño del cuórum pasa a ser 3. ¿Qué ocurre si un nodo nuevo se ha incorporado al clúster y luego se produce una partición de red? Depende de en qué partición quede ubicado el miembro nuevo tras la partición.

#### 2.2 División del clúster 3+1 {#22-cluster-split-31}
Si el nodo nuevo resulta estar en la misma partición que el líder, este todavía mantiene el cuórum activo de 3. No se produce ninguna elección de líder y no se afecta la disponibilidad del clúster (ver *Figura 4*).

![servidor-miembro-aprendiz-figura-04](/etcd/learning/img/server-learner-figure-04.png)

#### 2.3 División del clúster 2+2 {#23-cluster-split-22}
Si el clúster queda particionado en 2 y 2, ninguna de las particiones mantiene el cuórum de 3. En este caso, se produce una elección de líder (ver *Figura 5*).

![servidor-miembro-aprendiz-figura-05](/etcd/learning/img/server-learner-figure-05.png)

#### 2.4 Cuórum perdido {#24-quorum-lost}
¿Qué ocurre si primero se produce una partición de red y luego se añade un miembro nuevo? Un clúster de 3 nodos particionado ya tiene una réplica desconectada. Cuando se añade el miembro nuevo, el cuórum pasa de 2 a 3. Ahora este clúster tiene solo 2 nodos activos de 4, por lo que pierde el cuórum e inicia una nueva elección de líder (ver *Figura 6*).

![servidor-miembro-aprendiz-figura-06](/etcd/learning/img/server-learner-figure-06.png)

Dado que la operación de añadir un miembro puede cambiar el tamaño del cuórum, siempre se recomienda ejecutar primero «member remove» para reemplazar un nodo en mal estado.

Añadir un miembro nuevo a un clúster de 1 nodo cambia el tamaño del cuórum a 2, lo que provoca inmediatamente una elección de líder cuando el líder anterior descubre que el cuórum no está activo. Esto se debe a que la operación «member add» es un proceso de 2 pasos en el que el usuario debe aplicar primero el comando «member add» y luego iniciar el proceso del nodo nuevo (ver *Figura 7*).

![servidor-miembro-aprendiz-figura-07](/etcd/learning/img/server-learner-figure-07.png)

### 3. Configuraciones erróneas del clúster {#3-cluster-misconfigurations}
Un caso aún peor es cuando el miembro añadido está mal configurado. La reconfiguración de la composición es un proceso de dos pasos: «etcdctl member add» e iniciar un proceso de servidor etcd con la URL de pares dada. Es decir, el comando «member add» se aplica con independencia de la URL, incluso cuando el valor de la URL es inválido. Si el primer paso se aplica con URLs inválidas, el segundo paso ni siquiera puede iniciar el nuevo etcd. Una vez que el clúster pierde el cuórum, no hay forma de revertir el cambio de composición (ver *Figura 8*).

![servidor-miembro-aprendiz-figura-08](/etcd/learning/img/server-learner-figure-08.png)

Lo mismo se aplica a un clúster de múltiples nodos. Por ejemplo, el clúster tiene dos miembros caídos (uno ha fallado y el otro está mal configurado) y dos miembros activos, pero ahora requiere al menos 3 votos para cambiar la composición del clúster (ver *Figura 9*).

![servidor-miembro-aprendiz-figura-09](/etcd/learning/img/server-learner-figure-09.png)

Como se vio anteriormente, una simple configuración errónea puede hacer que todo el clúster caiga en un estado inoperativo. En tal caso, un operador debe recrear manualmente el clúster con la opción `etcd --force-new-cluster`. Dado que etcd se ha convertido en un servicio crítico para Kubernetes, incluso la interrupción más leve puede tener un impacto significativo en los usuarios. ¿Qué podemos mejorar para facilitar este tipo de operaciones con etcd? Entre otras cosas, la elección de líder es lo más crítico para la disponibilidad del clúster: ¿podemos hacer que la reconfiguración de la composición sea menos disruptiva sin cambiar el tamaño del cuórum? ¿Puede un nodo nuevo permanecer inactivo, solicitando al líder solo las actualizaciones mínimas, hasta ponerse al día? ¿Puede una configuración errónea de la composición ser siempre reversible y gestionarse de forma más segura (la ejecución de un comando member add erróneo nunca debería hacer fallar el clúster)? ¿Debería un usuario preocuparse por la topología de red al añadir un miembro nuevo? ¿Puede la API member add funcionar con independencia de la ubicación de los nodos y de las particiones de red en curso?

Aprendiz de Raft {#raft-learner}
============

Para mitigar estas brechas de disponibilidad descritas en la sección anterior, [Raft §4.2.1](https://github.com/ongardie/dissertation/blob/master/stanford.pdf) introduce un nuevo estado de nodo, «Learner» (aprendiz), que se incorpora al clúster como **miembro sin derecho a voto** hasta que alcanza los registros del líder.

Características de la v3.4 {#features-in-v34}
----------------

Un operador debería hacer la mínima cantidad de trabajo posible para añadir un nodo aprendiz nuevo. El comando `member add --learner` añade un aprendiz nuevo, que se incorpora al clúster como miembro sin derecho a voto pero sigue recibiendo todos los datos del líder (ver *Figura 10*).

![servidor-miembro-aprendiz-figura-10](/etcd/learning/img/server-learner-figure-10.png)

Cuando un aprendiz ha alcanzado el progreso del líder, puede ascenderse a miembro con derecho a voto mediante la API `member promote`, que entonces cuenta para el cuórum (ver *Figura 11*).

![servidor-miembro-aprendiz-figura-11](/etcd/learning/img/server-learner-figure-11.png)

El servidor de etcd valida la solicitud de ascenso para garantizar su seguridad operativa. Un aprendiz solo puede ascender a miembro con derecho a voto después de que su registro haya alcanzado el del líder (ver *Figura 12*).

![servidor-miembro-aprendiz-figura-12](/etcd/learning/img/server-learner-figure-12.png)

El aprendiz solo actúa como nodo en espera hasta ser ascendido: el liderazgo no puede transferirse a un aprendiz. El aprendiz rechaza lecturas y escrituras del cliente (el balanceador del cliente no debería enrutar solicitudes al aprendiz). Esto significa que el aprendiz no necesita emitir solicitudes de Read Index al líder. Tal limitación simplifica la implementación inicial del aprendiz en la versión v3.4 (ver *Figura 13*).

![servidor-miembro-aprendiz-figura-13](/etcd/learning/img/server-learner-figure-13.png)

Además, etcd limita el número total de aprendices que un clúster puede tener, y evita sobrecargar al líder con la replicación de registros. El aprendiz nunca se asciende a sí mismo. Aunque etcd proporciona información de estado del aprendiz y comprobaciones de seguridad, el operador del clúster debe tomar la decisión final de ascender o no al aprendiz.

Características propuestas para versiones futuras {#proposed-features-for-future-releases}
----------------

*Hacer que el estado de aprendiz sea el único y el predeterminado*: Establecer por defecto el estado de aprendiz para un miembro nuevo mejorará enormemente la seguridad de la reconfiguración de la composición, porque el aprendiz no cambia el tamaño del cuórum. Una configuración errónea siempre será reversible sin perder el cuórum.

*Hacer que el ascenso a miembro con derecho a voto sea totalmente automático*: Una vez que un aprendiz alcanza los registros del líder, un clúster puede ascender automáticamente al aprendiz. etcd exige que el usuario defina ciertos umbrales y, una vez satisfechos los requisitos, el aprendiz se asciende a sí mismo a miembro con derecho a voto. Desde la perspectiva del usuario, el comando «member add» funcionaría igual que hoy, pero con la mayor seguridad que aporta la característica de aprendiz.

*Hacer del aprendiz un nodo de conmutación por error en espera*: un aprendiz se incorpora como nodo en espera y se asciende automáticamente cuando la disponibilidad del clúster se ve afectada.

*Hacer que el aprendiz sea de solo lectura*: un aprendiz puede actuar como nodo de solo lectura que nunca se asciende. En un modo de consistencia débil, el aprendiz solo recibe datos del líder y nunca procesa escrituras. Atender lecturas localmente sin la sobrecarga del consenso reduciría enormemente las cargas de trabajo del líder, pero puede servir datos obsoletos. En un modo de consistencia fuerte, el aprendiz solicita el índice de lectura al líder para servir los datos más recientes, pero sigue rechazando escrituras.

Aprendiz vs. Mirror Maker {#learner-vs-mirror-maker}
========================

etcd implementa el «mirror maker» usando la API de observación para retransmitir continuamente creaciones y actualizaciones de claves a un clúster separado. La replicación especular (mirroring) suele tener una sobrecarga de latencia baja una vez completada la sincronización inicial. El aprendiz y la replicación especular se solapan en que ambos pueden usarse para replicar datos existentes con fines de solo lectura. Sin embargo, la replicación especular no garantiza la linealizabilidad. Durante desconexiones de red, es posible que se hayan descartado pares clave-valor anteriores, y se espera que los clientes verifiquen las respuestas de observación para un orden correcto. Por lo tanto, no hay garantía de ordenación en el espejo. Usa el espejo para una latencia mínima (por ejemplo, entre centros de datos) a costa de la consistencia. Usa el aprendiz para conservar todos los datos históricos y su ordenación.

Apéndice: Implementación del aprendiz en la v3.4 {#appendix-learner-implementation-in-v34}
========================================

*Exponer el tipo de nodo «Learner» en la API «MemberAdd».*

El cliente de etcd añade una opción a la API «MemberAdd» para el nodo aprendiz. Y el gestor del servidor de etcd aplica la entrada de cambio de composición con el tipo `pb.ConfChangeAddLearnerNode`. Una vez aplicado el comando, un servidor se incorpora al clúster con la opción `etcd --initial-cluster-state=existing`. Este nodo aprendiz no puede votar ni contar para el cuórum.

El servidor de etcd no debe transferir el liderazgo a un aprendiz, ya que puede seguir retrasado y no cuenta para el cuórum. El servidor de etcd limita a uno el número de aprendices que un clúster puede tener: cuantos más aprendices haya, más datos debe propagar el líder. Los clientes pueden comunicarse con el nodo aprendiz, pero el aprendiz rechaza todas las solicitudes excepto la lectura serializable y la API de estado de miembro. Esto es así por simplicidad de la implementación inicial. En el futuro, el aprendiz puede ampliarse como servidor de solo lectura que replica continuamente los datos del clúster. El balanceador del cliente debe proporcionar una función auxiliar para excluir el endpoint del nodo aprendiz. De lo contrario, una solicitud enviada al aprendiz puede fallar. La llamada de sincronización de miembros del cliente debería tener en cuenta el tipo de nodo aprendiz. Lo mismo debería aplicar a la llamada de actualización de endpoints del cliente.

Las respuestas de `MemberList` y `MemberStatus` deberían indicar qué nodo es el aprendiz.

*Añadir la API «MemberPromote».*

Internamente, en Raft, una segunda llamada a `MemberAdd` al nodo aprendiz lo asciende a miembro con derecho a voto. El líder mantiene el progreso de cada réplica y de cada aprendiz. Si el aprendiz no ha completado su mensaje de instantánea, se rechaza la solicitud de ascenso. Solo se acepta la solicitud de ascenso si y solo si: el nodo aprendiz está en un estado saludable; y el aprendiz está sincronizado con el líder o el delta está dentro del umbral (por ejemplo, el número de entradas por replicar al aprendiz es menor que 1/10 del valor de snapshot count, lo que significa que es menos probable que, incluso tras el ascenso, el líder tenga que enviar una instantánea al aprendiz). Toda esta lógica está codificada de forma fija en el paquete `etcdserver` y no es configurable.

Referencia {#reference}
=========

- Incidencia original de GitHub: [etcd#9161](https://github.com/etcd-io/etcd/issues/9161)
- Caso de uso: [etcd#3715](https://github.com/etcd-io/etcd/issues/3715)
- Caso de uso: [etcd#8888](https://github.com/etcd-io/etcd/issues/8888)
- Caso de uso: [etcd#10114](https://github.com/etcd-io/etcd/issues/10114)
