---
title: "Preguntas frecuentes"
weight: 180
icon: fa-solid fa-circle-question
description: "Preguntas frecuentes sobre la operación de Patroni y la resolución de problemas."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/faq.html"
---

<a id="faq"></a>
En esta sección encontrarás respuestas a las preguntas más frecuentes sobre Patroni. Cada subsección intenta centrarse en un tipo diferente de preguntas.

Esperamos que esto te ayude a aclarar la mayoría de tus dudas. Si aún tienes más inquietudes o te enfrentas a un problema inesperado, consulta [conversar](/es/patroni/contributing_guidelines#chatting) e [informar de errores](/es/patroni/contributing_guidelines#reporting_bugs) para obtener instrucciones sobre cómo conseguir ayuda o informar de problemas.

--------

## Comparación con otras soluciones de alta disponibilidad {#comparison-with-other-ha-solutions}

¿Por qué Patroni requiere un clúster separado de nodos del DCS mientras que otras soluciones como `repmgr` no lo hacen?  
Existen diferentes formas de implementar soluciones de alta disponibilidad, cada una con sus ventajas y desventajas.

Software como `repmgr` realiza la comunicación entre los nodos para decidir cuándo deben tomarse acciones.

Patroni, por otra parte, se basa en el estado almacenado en el DCS. El DCS actúa como fuente de verdad para que Patroni decida qué debe hacer.

Aunque tener un clúster de DCS separado puede hacer que tu arquitectura se infle, este enfoque también hace que sea menos probable que ocurran escenarios de split-brain en tu clúster de Postgres.

¿Cuál es la diferencia entre Patroni y otras soluciones de alta disponibilidad en cuanto a la gestión de Postgres?  
Patroni no solo gestiona la alta disponibilidad del clúster de Postgres, sino que también gestiona el propio Postgres.

Si los nodos de Postgres aún no existen, se encarga de realizar el bootstrap del primario y de los nodos en espera, y también gestiona la configuración de Postgres de los nodos. Si los nodos de Postgres ya existen, Patroni tomará el control de la gestión del clúster.

Además de lo anterior, Patroni también tiene capacidades de autocuración. Es decir, si un nodo primario falla, Patroni no solo hará una conmutación por error a una réplica, sino que también intentará reincorporar el primario anterior como réplica del nuevo primario. De manera similar, si una réplica falla, Patroni intentará reincorporar esa réplica.

Por eso llamamos a Patroni una «plantilla para soluciones de alta disponibilidad». Va más allá de solo gestionar la replicación física: gestiona Postgres en su conjunto.

--------

## DCS {#dcs}

¿Puedo usar el mismo clúster de `etcd` para almacenar datos de dos o más clústeres de Patroni?  
¡Sí, puedes!

La información sobre un clúster de Patroni se almacena en el DCS bajo una ruta con el prefijo de las opciones `namespace` y `scope` de Patroni.

Siempre que no tengas un namespace y un scope en conflicto entre diferentes clústeres de Patroni, deberías poder usar el mismo clúster de DCS para almacenar información de varios clústeres de Patroni.

¿Qué ocurre si intento usar la misma combinación de `namespace` y `scope` para diferentes clústeres de Patroni que apuntan al mismo clúster de DCS?  
Si el segundo clúster tiene un identificador de sistema de Postgres diferente, Patroni detecta datos incompatibles bajo esa ruta del DCS. Fuera del modo de pausa, termina su ejecución en lugar de gestionar el segundo clúster, porque asume que el estado almacenado pertenece a un clúster diferente y que Patroni estaba mal configurado.

Asegúrate de usar `namespace` / `scope` diferentes cuando trabajes con distintos clústeres de Patroni que comparten el mismo clúster de DCS.

¿Qué ocurre si pierdo mi clúster de DCS?  
El DCS se usa para almacenar básicamente el estado y la configuración dinámica del clúster de Patroni.

La primera consecuencia es que todos los clústeres de Patroni que dependen de ese DCS pasarán a modo de solo lectura, a menos que [dcs_failsafe_mode](/es/patroni/dcs_failsafe_mode#dcs_failsafe_mode) esté habilitado.

¿Qué debo hacer si pierdo mi clúster de DCS?  
Hay tres resultados posibles al perder tu clúster de DCS:

1.  El clúster de DCS se recupera por completo: esto no requiere ninguna acción por parte de Patroni. Una vez que el clúster de DCS se recupera, Patroni también debería poder recuperarse;
2.  El clúster de DCS se vuelve a crear en el mismo lugar y los endpoints siguen siendo los mismos. No se requieren cambios por parte de Patroni;
3.  Se crea un nuevo clúster de DCS con endpoints diferentes. Necesitarás actualizar los endpoints del DCS en la configuración de Patroni de cada nodo de Patroni.

Si te encuentras en el escenario `2.` o `3.`, Patroni se encargará de crear de nuevo la información de estado basándose en el estado actual del clúster, y de recrear la configuración dinámica en el DCS a partir de un archivo de copia de seguridad llamado `patroni.dynamic.json` que se almacena dentro del directorio de datos de Postgres de cada miembro del clúster de Patroni.

¿Qué ocurre si pierdo la mayoría en mi clúster de DCS?  
El DCS dejará de responder, lo que hará que Patroni degrade el nodo actual de Postgres de lectura/escritura.

Recuerda: Patroni se basa en el estado del DCS para tomar acciones sobre el clúster.

Puedes usar [dcs_failsafe_mode](/es/patroni/dcs_failsafe_mode#dcs_failsafe_mode) para aliviar esa situación.

--------

## patronictl {#patronictl}

¿Necesito ejecutar [patronictl](/es/patroni/patronictl#patronictl) en el host de Patroni?  
No, no necesitas hacerlo.

Ejecutar [patronictl](/es/patroni/patronictl#patronictl) en el host de Patroni resulta práctico si tienes acceso al host de Patroni, porque puedes usar el mismo archivo de configuración del agente `patroni` para la aplicación [patronictl](/es/patroni/patronictl#patronictl).

Sin embargo, [patronictl](/es/patroni/patronictl#patronictl) es básicamente un cliente y puede ejecutarse desde máquinas remotas. Solo necesitas proporcionarle suficiente configuración para que pueda alcanzar el DCS y la REST API de los miembros de Patroni.

¿Por qué desapareció la información de uno de mis miembros de Patroni de la salida del comando [patronictl_list](/es/patroni/patronictl#patronictl_list)?  
La información mostrada por [patronictl_list](/es/patroni/patronictl#patronictl_list) se basa en el contenido del DCS.

Si la información sobre un miembro desapareció del DCS, es muy probable que el agente de Patroni en ese nodo ya no se esté ejecutando o que no pueda comunicarse con el DCS.

Como el miembro no puede actualizar la información, esta eventualmente expira del DCS y, en consecuencia, el miembro ya no se muestra en la salida de [patronictl_list](/es/patroni/patronictl#patronictl_list).

¿Por qué la información sobre uno de mis miembros de Patroni no está actualizada en la salida del comando [patronictl_list](/es/patroni/patronictl#patronictl_list)?  
La información mostrada por [patronictl_list](/es/patroni/patronictl#patronictl_list) se basa en el contenido del DCS.

De forma predeterminada, Patroni actualiza esa información aproximadamente cada `loop_wait` segundos. Es decir, incluso si todo funciona con normalidad, aún puedes ver un «retraso» de hasta `loop_wait` segundos en la información almacenada en el DCS.

Ten en cuenta, sin embargo, que esto no es una regla. Algunas operaciones realizadas por Patroni hacen que actualice la información del DCS de inmediato.

--------

## Configuración {#configuration}

¿Cuál es la diferencia entre la configuración dinámica y la configuración local?  
La configuración dinámica (o configuración global) es la configuración almacenada en el DCS y que se aplica a todos los miembros del clúster de Patroni. Es principalmente donde deberías almacenar tu configuración.

Las opciones específicas de un nodo, o las opciones con las que te gustaría sobrescribir la configuración global, deberías establecerlas solo en el miembro de Patroni deseado como configuración local. Esa configuración local puede especificarse mediante el archivo de configuración o mediante variables de entorno.

Consulta más en [config](/es/patroni/config#config).

¿Cuáles son los tipos de configuración en Patroni y cuál es la precedencia?  
Los tipos son:

- Configuración dinámica: se aplica a todos los miembros;
- Configuración local: se aplica al miembro local, sobrescribe la configuración dinámica;
- Configuración de entorno: se aplica al miembro local, sobrescribe tanto la configuración dinámica como la local.

**Nota:** algunos GUC de Postgres solo pueden establecerse de forma global, es decir, mediante la configuración dinámica. Además, hay GUC para los que Patroni impone un valor fijo codificado.

Consulta más en [config](/es/patroni/config#config).

¿Existe alguna utilidad que me ayude a crear mi archivo de configuración de Patroni?  
Sí, la hay.

Puedes usar los comandos `patroni --generate-sample-config` o `patroni --generate-config` para generar, respectivamente, una configuración de ejemplo de Patroni o una configuración de Patroni basada en una instancia de Postgres existente.

Consulta [generate_sample_config](/es/patroni/config#generate_sample_config) y [generate_config](/es/patroni/config#generate_config) para más detalles.

Cambié mis parámetros en la configuración `bootstrap.dcs` pero Patroni no está aplicando los cambios a los miembros del clúster. ¿Qué está mal?  
Los valores configurados bajo `bootstrap.dcs` solo se usan al realizar el bootstrap de un clúster nuevo. Esos valores se escribirán en el DCS durante el bootstrap.

Después de que termine la fase de bootstrap, solo podrás cambiar la configuración dinámica a través del DCS.

Consulta la siguiente pregunta para más detalles.

¿Cómo puedo cambiar mi configuración dinámica?  
Necesitas cambiar la configuración en el DCS. Esto se logra mediante:

- [patronictl_edit_config](/es/patroni/patronictl#patronictl_edit_config); o
- Una solicitud `PATCH` a [config_endpoint](/es/patroni/rest_api#config_endpoint).

¿Cómo puedo cambiar mi configuración local?  
Necesitas cambiar el archivo de configuración del miembro de Patroni correspondiente y enviar la señal `SIGHUP` al agente de Patroni. Puedes hacerlo usando cualquiera de estos métodos:

- Enviar una solicitud `POST` a la REST API [reload_endpoint](/es/patroni/rest_api#reload_endpoint); o

- Ejecutar [patronictl_reload](/es/patroni/patronictl#patronictl_reload); o

- Enviar localmente la señal `SIGHUP` al proceso de Patroni:

  > - Si iniciaste Patroni a través de systemd, puedes usar el comando `systemctl reload PATRONI_UNIT.service`, siendo `PATRONI_UNIT` el nombre del servicio de Patroni; o
  > - Si iniciaste Patroni por otros medios, necesitarás identificar el proceso `patroni` y ejecutar `kill -s HUP PID`, siendo `PID` el ID del proceso `patroni`.

**Nota:** hay casos en los que una recarga mediante [patronictl_reload](/es/patroni/patronictl#patronictl_reload) podría no funcionar:

- Certificados de la REST API caducados: puedes mitigarlo usando la opción `-k` de [patronictl](/es/patroni/patronictl#patronictl);
- Credenciales incorrectas: por ejemplo, al cambiar las credenciales de `restapi` o `ctl` en el archivo de configuración y usar ese mismo archivo de configuración para Patroni y [patronictl](/es/patroni/patronictl#patronictl).

¿Cómo puedo cambiar mi configuración de entorno?  
La configuración de entorno solo la lee Patroni durante el arranque.

Con esto en mente, si cambias la configuración de entorno necesitarás reiniciar el agente de Patroni correspondiente.

¡Ten cuidado de no causar una conmutación por error en el clúster! Podría interesarte consultar [patronictl_pause](/es/patroni/patronictl#patronictl_pause).

¿Cómo puedo reducir las líneas repetitivas de registro de latido durante la operación normal?

Si tus registros son demasiado ruidosos por líneas repetidas como `Lock owner: ...` y `no action. I am ...`, configura `log.deduplicate_heartbeat_logs: true`.

Puedes establecerlo en el archivo YAML de Patroni ([opciones de registro](/es/patroni/config/yaml#log_settings)) o con `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS=true`.

Ten en cuenta que esto reduce el volumen del registro al suprimir los mensajes de latido repetidos, pero también pierdes la visibilidad del latido por ciclo que puede ayudar durante el diagnóstico de conmutaciones por error.

¿Qué ocurre si cambio un GUC de Postgres que requiere una recarga?  
Cuando cambias la configuración dinámica o la local como se explicó en las preguntas anteriores, Patroni se encargará de recargar la configuración de Postgres por ti.

¿Qué ocurre si cambio un GUC de Postgres que requiere un reinicio?  
Patroni marcará los miembros afectados con un indicador de `pending restart`.

Depende de ti determinar cuándo y cómo reiniciar los miembros. Esto se puede lograr mediante:

- [patronictl_restart](/es/patroni/patronictl#patronictl_restart); o
- Una solicitud `POST` a [restart_endpoint](/es/patroni/rest_api#restart_endpoint).

**Nota:** algunos GUC de Postgres requieren una gestión especial en cuanto al orden de reinicio de los nodos de Postgres. Consulta [shared_memory_gucs](/es/patroni/config#shared_memory_gucs) para más detalles.

¿Cuál es la diferencia entre `etcd` y `etcd3` en la configuración de Patroni?  
`etcd` usa la versión 2 de la API de `etcd`, mientras que `etcd3` usa la versión 3 de la API de `etcd`.

Ten en cuenta que la información almacenada por la versión 2 de la API no es gestionable por la versión 3 de la API y viceversa.

Recomendamos que configures `etcd3` en lugar de `etcd` porque:

- La versión 2 de la API está deshabilitada de forma predeterminada a partir de Etcd v3.4;
- La versión 2 de la API se eliminó por completo en etcd v3.6.

Tengo `use_slots` habilitado en mi configuración de Patroni, pero cuando un miembro del clúster se desconecta por un tiempo, el slot de replicación usado por ese miembro se elimina en el nodo aguas arriba. ¿Qué puedo hacer para evitar ese problema?  
Hay dos opciones:

1.  Puedes ajustar `member_slots_ttl` (valor predeterminado `30min`, disponible desde Patroni `4.0.0` y PostgreSQL 11 en adelante) y los slots de replicación de los miembros ausentes no se eliminarán cuando el tiempo de inactividad de los miembros sea menor que el umbral configurado.
2.  Puedes configurar slots de replicación físicos permanentes para los miembros.

Desde Patroni `3.2.0` ya es posible tener slots de miembro como slots permanentes gestionados por Patroni.

En PostgreSQL 11 o posterior, Patroni creará los slots físicos permanentes en todos los nodos y se asegurará de no eliminar los slots, así como de avanzar el LSN de los slots en todos los nodos según el LSN que haya consumido el miembro.

Más tarde, si decides eliminar el miembro correspondiente, es **tu responsabilidad** ajustar la configuración de los slots permanentes; de lo contrario, Patroni mantendrá los slots para siempre.

**Nota:** en Patroni anterior a `3.2.0` aún podías tener slots de miembro configurados como slots físicos permanentes; sin embargo, se gestionarían solo en el líder actual. Es decir, en caso de una conmutación por error o un switchover, estos slots se crearían en el nuevo líder, pero eso no garantizaría que tuviera todos los segmentos de WAL del nodo ausente.

**Nota:** incluso con Patroni `3.2.0` podría existir una pequeña condición de carrera. Al principio, cuando el slot se crea en la réplica, podría estar por delante del mismo slot en el líder y, si nadie está consumiendo el slot, todavía existe la posibilidad de que falten algunos archivos después de una conmutación por error. Con esto en mente, se recomienda que configures el archivado continuo, que permite restaurar los WAL necesarios o realizar un PITR.

¿Cuál es la diferencia entre `loop_wait`, `retry_timeout` y `ttl`?  
Patroni realiza de vez en cuando lo que llamamos un ciclo de alta disponibilidad. En cada ciclo se encarga de realizar una serie de comprobaciones en el clúster para determinar su estado de salud y, según dicho estado, puede tomar acciones, como hacer una conmutación por error a un nodo en espera.

`loop_wait` determina cuánto tiempo, en segundos, debe dormir Patroni antes de realizar un nuevo ciclo de comprobaciones de alta disponibilidad.

`retry_timeout` establece el tiempo de espera para las operaciones de reintento en el DCS y en Postgres. Por ejemplo: si el DCS no responde durante más de `retry_timeout` segundos, Patroni podría degradar el nodo primario como acción de seguridad.

`ttl` establece el tiempo de la concesión del bloqueo `leader` en el DCS. Si el líder actual del clúster no puede renovar la concesión durante sus ciclos de alta disponibilidad durante más de `ttl`, la concesión expirará y eso desencadenará una `leader race` en el clúster.

**Nota:** al modificar estas opciones, ten en cuenta que Patroni aplica la regla y los valores mínimos descritos en la sección [dynamic](/es/patroni/config/dynamic#dynamic) de la documentación.

--------

## Gestión de Postgres {#postgres-management}

¿Puedo cambiar los GUC de Postgres directamente en la configuración de Postgres?  
Puedes hacerlo, pero deberías evitarlo.

La configuración de Postgres está gestionada por Patroni, y los intentos de editar los archivos de configuración pueden acabar frustrados por Patroni, ya que podría sobrescribirlos en algún momento.

Hay algunas opciones disponibles para evitar la gestión realizada por Patroni:

- Cambiar los GUC de Postgres mediante `$PGDATA/postgresql.base.conf`; o
- Definir un `postgresql.custom_conf` que se usará en lugar de `postgresql.base.conf` para que puedas gestionarlo de forma externa; o
- Cambiar los GUC usando `ALTER SYSTEM` / `ALTER DATABASE` / `ALTER USER`.

Puedes encontrar más información al respecto en la sección [important_configuration_rules](/es/patroni/config#important_configuration_rules).

En cualquier caso, recomendamos que gestiones toda la configuración de Postgres mediante Patroni. Eso centralizará la gestión y facilitará la depuración de Patroni cuando sea necesario.

¿Puedo reiniciar los nodos de Postgres directamente?  
¡No, **no** debes intentar gestionar Postgres directamente!

Reiniciar el servidor de Postgres fuera de Patroni puede desencadenar una conmutación por error.

Si necesitas gestionar el servidor de Postgres, hazlo mediante las vías expuestas por Patroni.

¿Puede Patroni hacerse cargo de la gestión de un clúster de Postgres ya existente?  
¡Sí, puede!

Consulta [existing_data](/es/patroni/existing_data#existing_data) para instrucciones detalladas.

¿Cómo gestiona Patroni Postgres?  
Patroni se encarga de arrancar y detener Postgres ejecutando los binarios de Postgres, como `pg_ctl` y `postgres`.

Con esto en mente, **DEBES** deshabilitar cualquier otra fuente que pueda gestionar los clústeres de Postgres, como las unidades de systemd, p. ej. `postgresql.service`. Solo Patroni debería poder iniciar, detener y promover instancias de Postgres en el clúster. No hacerlo puede derivar en escenarios de split-brain. Por ejemplo: si el nodo que se ejecutaba como primario falló y la unidad `postgresql.service` está habilitada, podría volver a arrancar Postgres y causar un split-brain.

--------

## Conceptos y requisitos {#concepts-and-requirements}

¿Cuáles son las aplicaciones que forman parte de Patroni?  
Patroni básicamente incluye un par de aplicaciones:

- `patroni`: Este es el agente de Patroni, que se encarga de gestionar un nodo de Postgres;
- [patronictl](/es/patroni/patronictl#patronictl): Esta es una utilidad de línea de comandos usada para interactuar con un clúster de Patroni (realizar switchovers, reinicios, cambios en la configuración, etc.). Encuentra más información en [patronictl](/es/patroni/patronictl#patronictl).

¿Qué es un `standby cluster` en Patroni?  
Es un clúster que no tiene ningún nodo primario de Postgres en ejecución, es decir, no hay ningún miembro de lectura/escritura en el clúster.

Este tipo de clústeres existen para replicar datos de otro clúster y suelen ser útiles cuando quieres replicar datos entre centros de datos.

Habrá un líder en el clúster que será un nodo en espera encargado de replicar los cambios desde un nodo de Postgres remoto. Luego, habrá un conjunto de nodos en espera configurados con replicación en cascada desde dicho miembro líder.

**Nota:** el clúster en espera no sabe nada del clúster origen desde el que replica; puede incluso usar `restore_command` en lugar del streaming de WAL y puede usar un clúster de DCS totalmente independiente.

Consulta [standby_cluster](/es/patroni/standby_cluster#standby_cluster) para más detalles.

¿Qué es un `leader` en Patroni?  
Un `leader` en Patroni es como un coordinador del clúster.

En un clúster de Patroni normal, el `leader` será el nodo de lectura/escritura.

En un clúster de Patroni en espera, el `leader` (también conocido como `standby leader`) se encargará de replicar desde un nodo de Postgres remoto y de propagar en cascada esos cambios a los demás miembros del clúster en espera.

¿Requiere Patroni un número mínimo de nodos de Postgres en el clúster?  
No, puedes ejecutar Patroni con cualquier número de nodos de Postgres.

Recuerda: Patroni está desacoplado del DCS.

¿Qué significa [pause](/es/patroni/pause#pause) en Patroni?  
Pausa es una operación expuesta por Patroni con la que el usuario puede pedir a Patroni que se aparte de la gestión de Postgres.

Esto es útil principalmente cuando quieres realizar mantenimiento en el clúster y deseas evitar que Patroni tome decisiones relacionadas con la alta disponibilidad, como hacer una conmutación por error a un nodo en espera cuando detienes el primario.

Puedes encontrar más información al respecto en [pause](/es/patroni/pause#pause).

--------

## Conmutación por error automática {#automatic-failover}

¿Cómo funciona el mecanismo de conmutación por error automática de Patroni?  
La conmutación por error automática de Patroni se basa en lo que llamamos `leader race`.

Patroni almacena el estado del clúster en el DCS, entre ellos un bloqueo `leader` que contiene el nombre del miembro de Patroni que es el `leader` actual del clúster.

Ese bloqueo `leader` tiene un tiempo de vida asociado. Si el nodo líder no logra actualizar a tiempo la concesión del bloqueo `leader`, la clave eventualmente expirará del DCS.

Cuando el bloqueo `leader` expira, se desencadena lo que Patroni llama una `leader race`: todos los nodos comienzan a realizar comprobaciones para determinar si son los mejores candidatos para tomar el rol de `leader`. Algunas de estas comprobaciones incluyen llamadas a la REST API de todos los demás miembros de Patroni.

Todos los miembros de Patroni que se consideren a sí mismos el mejor candidato para tomar el bloqueo `leader` intentarán hacerlo. El primer miembro de Patroni que logre tomar el bloqueo `leader` se promoverá a nodo de lectura/escritura (o `standby leader`), y los demás se configurarán para seguirlo.

¿Puedo deshabilitar temporalmente la conmutación por error automática en el clúster de Patroni?  
¡Sí, puedes!

Puedes lograrlo pausando temporalmente el clúster. Esto suele ser útil para realizar mantenimiento.

Cuando quieras reanudar la conmutación por error automática del clúster, solo necesitas quitar la pausa.

Puedes encontrar más información al respecto en [pause](/es/patroni/pause#pause).

--------

## Bootstrap y creación de nodos en espera {#bootstrapping-and-standbys-creation}

¿Cómo crea Patroni un nodo primario de Postgres? ¿Y un nodo de Postgres en espera?  
De forma predeterminada, Patroni usará `initdb` para hacer el bootstrap de un clúster nuevo y `pg_basebackup` para crear nodos en espera a partir de una copia del miembro `leader`.

Puedes personalizar ese comportamiento escribiendo tus métodos personalizados de bootstrap y tus métodos personalizados de creación de réplicas.

Los métodos personalizados suelen ser útiles cuando quieres restaurar copias de seguridad creadas por herramientas de copia de seguridad como pgBackRest o Barman, por ejemplo.

Para información detallada consulta [custom_bootstrap](/es/patroni/replica_bootstrap#custom_bootstrap) y [custom_replica_creation](/es/patroni/replica_bootstrap#custom_replica_creation).

--------

## Monitorización {#monitoring}

¿Cómo puedo monitorizar mi clúster de Patroni?  
Patroni expone un par de endpoints útiles en su [rest_api](/es/patroni/rest_api#rest_api):

- `/metrics`: expone métricas de monitorización en un formato que Prometheus puede consumir;
- `/patroni`: expone el estado del nodo local de Patroni/Postgres en formato JSON. La información que se muestra aquí es muy similar a la que muestra el endpoint `/metrics`.

Puedes usar esos endpoints para implementar comprobaciones de monitorización.
