---
title: "8. Registro"
linkTitle: "8. Registro"
weight: 320
description: "Integración con syslog, registros de arranque, registros en tiempo de ejecución y resolución de problemas de registro"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/logging/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 8"
---

Para el registro, HAProxy depende siempre de un servidor syslog, ya que no realiza ningún acceso al sistema de
archivos. La forma estándar de usarlo es enviar los registros por UDP al servidor de registros (por defecto al puerto
514). Muy comúnmente esto se configura hacia 127.0.0.1, donde se está ejecutando el demonio syslog local, pero
también se utiliza a través de la red para registrar en un servidor central. El servidor central proporciona beneficios
adicionales, especialmente en escenarios activo-activo donde es deseable mantener los registros fusionados en
el orden de llegada. HAProxy también puede hacer uso de un socket UNIX para enviar sus registros al demonio
syslog local, pero no se recomienda en absoluto, porque si el servidor syslog se reinicia mientras haproxy
se ejecuta, el socket será sustituido y los nuevos registros se perderán. Dado que HAProxy quedará aislado dentro de una
jaula chroot, no tendrá la capacidad de reconectarse al nuevo socket. También se ha observado
en producción que los búferes de registro utilizados en los sockets UNIX son muy pequeños y provocan pérdida de mensajes incluso
con cargas muy ligeras. Sin embargo, esto puede estar bien para hacer pruebas.

Se recomienda añadir la siguiente directiva a la sección «global» para que HAProxy registre en el
demonio local usando la facility «local0»:

```text
log 127.0.0.1:514 local0
```

y después añadir la siguiente a cada sección «defaults» o a cada sección frontend y
backend:

```text
log global
```

De esta manera, todos los registros se centralizarán mediante la definición global de dónde está el servidor de registros.

Algunos demonios syslog no escuchan tráfico UDP por defecto, por lo que, dependiendo del demonio utilizado,
la sintaxis para activarlo variará:

- en sysklogd, debes pasar el argumento «-r» en la línea de comandos del demonio para que escuche un
  socket UDP para los registros «remotos»; ten en cuenta que no hay forma de limitarlo a la dirección
  127.0.0.1, así que también recibirá registros de sistemas remotos;

- en rsyslogd, las siguientes líneas deben añadirse al archivo de configuración:

```shell
$ModLoad imudp
$UDPServerAddress *
$UDPServerRun 514
```

- en syslog-ng, puede crearse una nueva fuente de la siguiente manera; después debe añadirse como fuente
  válida en una de las directivas «log»:

```text
source s_udp {
  udp(ip(127.0.0.1) port(514));
};
```

Consulta el manual de tu demonio syslog para más información. Si no se ve ningún registro en los archivos de
registro del sistema, considera las siguientes pruebas:

- reinicia haproxy. Cada frontend y backend registra una línea indicando que está arrancando. Si estos registros
  se reciben, significa que el registro funciona.

- ejecuta «strace -tt -s100 -etrace=sendmsg -p \<haproxy's pid\>» y realiza alguna actividad que esperas que
  se registre. Deberías ver ahí los mensajes de registro enviándose mediante sendmsg(). Si no
  aparecen, reinicia ejecutando strace sobre haproxy. Si sigues sin ver registros, sin duda
  significa que algo está mal en tu configuración.

- ejecuta tcpdump para vigilar el puerto 514, por ejemplo en la interfaz loopback si el tráfico se envía
  localmente: «tcpdump -As0 -ni lo port 514». Si los paquetes se ven ahí, es la prueba de
  que se envían y, entonces, hay que investigar el problema en el demonio syslogd.

Mientras que los registros de tráfico se envían desde los frontends (donde se aceptan las conexiones
entrantes), los backends también deben poder enviar registros para informar de un cambio de estado de un
servidor consecutivo a una comprobación de estado. Consulta el manual de configuración de HAProxy para más
información sobre todos los ajustes de registro posibles.

Es conveniente elegir una facility que no esté utilizada por otros demonios. Los ejemplos de HAProxy
sugieren a menudo «local0» para los registros de tráfico y «local1» para los registros de administración
porque nunca se ven en producción. Una única facility también sería suficiente. Tener registros separados
es conveniente para el análisis de registros, pero también es importante recordar que los registros pueden
contener a veces información confidencial y, como tales, no deben mezclarse con otros registros que puedan
entregarse accidentalmente a personas no autorizadas.

Para resolver problemas en producción sin impactar demasiado la capacidad del servidor, se recomienda
hacer uso de la utilidad «halog» proporcionada con HAProxy. Es una especie de utilidad tipo grep diseñada
para procesar archivos de registro de HAProxy a una velocidad de datos muy alta. Las cifras típicas están entre 1 y 2 GB de
registros por segundo. Es capaz de extraer solo ciertos registros (p. ej.: buscar algunas clases de códigos
de estado HTTP, el estado de terminación de conexiones, buscar por rangos de tiempo de respuesta, mostrar
solo errores), contar líneas, limitar la salida a un número de líneas y realizar algunas estadísticas más
avanzadas, como ordenar los servidores por tiempo de respuesta o por número de errores, ordenar las URLs por
tiempo o por número de accesos, ordenar las direcciones de los clientes por número de accesos, etc. Es muy
práctico para detectar rápidamente anomalías como un bot haciendo bucles en el sitio, y bloquearlo.
