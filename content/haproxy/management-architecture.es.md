---
title: "2. Arquitectura de HAProxy"
linkTitle: "2. Arquitectura"
weight: 260
description: "El proceso, el multihilo, el bucle de eventos, chroot, los registros, los relojes y el modelo de proxy TCP"
icon: fa-solid fa-diagram-project
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/management/architecture/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 2"
---

HAProxy es un demonio multihilo, basado en eventos y no bloqueante. Esto significa que usa
multiplexación de eventos para planificar todas sus actividades en lugar de depender del sistema para planificar entre
múltiples actividades. La mayor parte del tiempo se ejecuta como un único proceso, por lo que la salida de «ps aux» en un
sistema mostrará solo un proceso «haproxy», salvo que haya una recarga suave en curso y que un proceso
antiguo esté terminando su trabajo en paralelo con el nuevo. Así pues, siempre es fácil rastrear su
actividad con la utilidad strace. Para escalar con el número de procesadores disponibles, por
defecto haproxy iniciará un hilo worker por cada procesador en el que se le permita ejecutarse. Salvo
configuración explícita en contra, el tráfico entrante se reparte entre todos estos hilos, que ejecutan
todos el mismo bucle de eventos. Se presta gran atención a limitar las dependencias entre hilos al mínimo
estricto, con el fin de intentar lograr una escalabilidad casi lineal. Esto tiene algunos impactos, como el
hecho de que una conexión dada sea atendida por un único hilo. Así, para utilizar toda la capacidad de
procesamiento disponible, es necesario tener al menos tantas conexiones como hilos haya, lo cual se cumple
casi siempre.

HAProxy está diseñado para aislarse en una jaula chroot durante el arranque, donde no puede realizar
ningún acceso al sistema de archivos. Esto también aplica a las bibliotecas de las que depende (p. ej.:
libc, libssl, etc.). El efecto inmediato es que un proceso en ejecución no podrá recargar un archivo de
configuración para aplicar cambios; en su lugar, se iniciará un proceso nuevo utilizando el archivo de
configuración actualizado. Otros efectos menos obvios son que algunos archivos de zona horaria o de
resolución a los que la libc podría intentar acceder en tiempo de ejecución no se encontrarán, aunque en general
esto no debería ocurrir, pues no se necesitan después del arranque. Una consecuencia agradable de este
principio es que el proceso de HAProxy es totalmente sin estado y no se necesita ninguna limpieza después
de matarlo, así que cualquier método que funcione para matarlo hará lo
correcto.

HAProxy no escribe archivos de registro, sino que se apoya en el protocolo syslog estándar para enviar los registros a un
servidor remoto (que a menudo está ubicado en el mismo sistema).

HAProxy usa su reloj interno para aplicar los tiempos de espera, que se deriva de la hora del sistema pero
en el que se corrige cualquier deriva inesperada. Esto se hace limitando el tiempo que se pasa esperando en
poll() un evento y midiendo el tiempo que realmente tomó. En la práctica, nunca espera más de un segundo.
Esto explica por qué, al ejecutar strace sobre un proceso completamente inactivo, se observan llamadas
periódicas a poll() (o cualquiera de sus variantes) rodeadas de dos llamadas a gettimeofday(). Son
normales, completamente inofensivas y tan baratas que la carga que implican es totalmente indetectable a
escala del sistema, así que no hay nada anormal en ello. Ejemplo:

```text
16:35:40.002320 gettimeofday({1442759740, 2605}, NULL) = 0
16:35:40.002942 epoll_wait(0, {}, 200, 1000) = 0
16:35:41.007542 gettimeofday({1442759741, 7641}, NULL) = 0
16:35:41.007998 gettimeofday({1442759741, 8114}, NULL) = 0
16:35:41.008391 epoll_wait(0, {}, 200, 1000) = 0
16:35:42.011313 gettimeofday({1442759742, 11411}, NULL) = 0
```

HAProxy es un proxy TCP, no un enrutador. Trabaja con conexiones establecidas que han sido validadas
por el kernel, y no con paquetes de ninguna forma ni con sockets en otros estados (p. ej.: ningún SYN_RECV
ni TIME_WAIT), aunque su existencia puede impedirle enlazar un puerto. Depende del sistema para aceptar
las conexiones entrantes e iniciar las conexiones salientes. Un efecto inmediato de esto es
que no existe ninguna relación entre los paquetes observados a ambos lados de una conexión reenviada, que
pueden ser de diferente tamaño, número e incluso familia. Dado que una conexión solo puede aceptarse desde
un socket en estado LISTEN, todos los sockets en los que escucha son necesariamente visibles utilizando la
utilidad «netstat» para mostrar los sockets a la escucha. Ejemplo:

```haproxy
# netstat -ltnp
```

Active Internet connections (only servers) Proto Recv-Q Send-Q Local Address Foreign Address State
PID/Program name tcp 0 0 0.0.0.0:22 0.0.0.0:\* LISTEN 1629/sshd tcp 0 0 0.0.0.0:80 0.0.0.0:\* LISTEN
2847/haproxy tcp 0 0 0.0.0.0:443 0.0.0.0:\* LISTEN 2847/haproxy
