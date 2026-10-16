---
title: "Soporte de watchdog"
weight: 90
icon: fa-solid fa-dog
description: "Integración del watchdog y consideraciones de fencing para clústeres de Patroni."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/watchdog.html"
---

<a id="watchdog"></a>

Que varios servidores de PostgreSQL se ejecuten como primarios puede provocar la pérdida de transacciones debido a líneas de tiempo divergentes. Esta situación también se conoce como problema de split-brain. Para evitar el split-brain, Patroni necesita asegurarse de que PostgreSQL no aceptará ninguna confirmación de transacción después de que expire la clave de líder en el DCS. En circunstancias normales, Patroni intentará lograrlo deteniendo PostgreSQL cuando la actualización del bloqueo de líder falle por cualquier motivo. Sin embargo, esto puede no llegar a ocurrir por diversas razones:

- Patroni se ha caído debido a un bug, una condición de falta de memoria o por haber sido terminado accidentalmente por un administrador del sistema.
- El apagado de PostgreSQL es demasiado lento.
- Patroni no llega a ejecutarse debido a una carga alta del sistema, a que la VM fue pausada por el hipervisor o a otros problemas de infraestructura.

Para garantizar un comportamiento correcto bajo estas condiciones, Patroni admite dispositivos watchdog. Los dispositivos watchdog son mecanismos de software o hardware que reinician todo el sistema cuando no reciben un latido de keepalive dentro de un periodo determinado. Esto añade una capa adicional de protección contra fallos en caso de que fallen los mecanismos habituales de protección contra el split-brain de Patroni.

Patroni intentará activar el watchdog antes de promover PostgreSQL a primario. Si la activación del watchdog falla y el modo watchdog es `required`, el nodo se negará a convertirse en líder. Al decidir participar en la elección de líder, Patroni también comprobará que la configuración del watchdog le permita siquiera convertirse en líder. Tras degradar PostgreSQL (por ejemplo, debido a una conmutación por error manual), Patroni desactivará de nuevo el watchdog. El watchdog también estará deshabilitado mientras Patroni esté en estado de pausa.

De forma predeterminada, Patroni configurará el watchdog para que expire 5 segundos antes de que expire el TTL. Con la configuración predeterminada de `loop_wait=10` y `ttl=30`, esto le da al bucle de HA al menos 15 segundos (`ttl` - `safety_margin` - `loop_wait`) para completarse antes de que el sistema se reinicie por la fuerza. De forma predeterminada, el acceso al DCS está configurado para expirar después de 10 segundos. Esto significa que, cuando el DCS no está disponible, por ejemplo debido a problemas de red, Patroni y PostgreSQL tendrán al menos 5 segundos (`ttl` - `safety_margin` - `loop_wait` - `retry_timeout`) para llegar a un estado en el que todas las conexiones de clientes estén terminadas.

El margen de seguridad es la cantidad de tiempo que Patroni reserva para el intervalo entre la actualización de la clave de líder y el keepalive del watchdog. Patroni intentará enviar un keepalive inmediatamente después de la confirmación de la actualización de la clave de líder. Si el proceso de Patroni queda suspendido durante un tiempo prolongado justo en el momento exacto, el keepalive puede retrasarse más allá del margen de seguridad sin disparar el watchdog. Esto da como resultado una ventana de tiempo en la que el watchdog no se disparará antes de la expiración de la clave de líder, lo que invalida la garantía. Para estar absolutamente seguro de que el watchdog se disparará en todas las circunstancias, configura el watchdog para que expire tras la mitad del TTL estableciendo `safety_margin` en -1, lo que fija el tiempo de espera del watchdog en `ttl // 2`. Si necesitas esta garantía, probablemente deberías aumentar el `ttl` y/o reducir `loop_wait` y `retry_timeout`.

Actualmente los watchdogs solo se admiten mediante la interfaz de dispositivos watchdog de Linux.

--------

## Configuración del watchdog por software en Linux {#setting-up-software-watchdog-on-linux}

La configuración predeterminada de Patroni intentará usar `/dev/watchdog` en Linux si resulta accesible para Patroni. Para la mayoría de los casos de uso, emplear el watchdog por software integrado en el kernel de Linux es suficientemente seguro.

Para habilitar el watchdog por software ejecuta los siguientes comandos como root antes de iniciar Patroni:

``` bash
modprobe softdog
# Replace postgres with the user you will be running patroni under
chown postgres /dev/watchdog
```

Para hacer pruebas puede ser útil deshabilitar el reinicio añadiendo `soft_noboot=1` a la línea de comandos de modprobe. En este caso el watchdog solo registrará una línea en el búfer circular del kernel, visible mediante `dmesg`.

Patroni registrará información sobre el watchdog cuando este se haya habilitado con éxito.
