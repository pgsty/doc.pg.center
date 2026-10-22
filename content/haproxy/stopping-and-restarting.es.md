---
title: "4. Detención y reinicio de HAProxy"
linkTitle: "4. Detener y reiniciar"
weight: 280
description: "Señales, paradas suaves, recargas y reinicios en modo master-worker"
icon: fa-solid fa-rotate
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/stopping-and-restarting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 4"
---

HAProxy admite una parada suave y una parada abrupta. La parada abrupta es simple: cuando se envía la
señal SIGTERM al proceso haproxy, este termina de inmediato y todas las conexiones establecidas se
cierran. La parada suave se activa cuando se envía la señal SIGUSR1 al proceso haproxy. Consiste
únicamente en desenlazarse de los puertos de escucha, pero seguir procesando las conexiones
existentes hasta que se cierren. Una vez cerrada la última conexión, el proceso se marcha.

El método de parada abrupta se usa para las acciones «stop» o «restart» del script de gestión del
servicio. La parada suave se usa para la acción «reload», que intenta recargar sin interrupciones
una nueva configuración en un nuevo proceso.

Ambas señales pueden ser enviadas por el propio proceso haproxy nuevo durante una recarga o un
reinicio, de modo que se envíen en el último momento posible y solo si es estrictamente necesario.
Esto es lo que realizan respectivamente las opciones «-st» (abrupta) y «-sf» (suave).

En modo master-worker, no es necesario iniciar un nuevo proceso haproxy para recargar la
configuración. El proceso master reacciona a la señal SIGUSR2 reejecutándose a sí mismo con el
parámetro -sf seguido de los PID de los workers. El master analizará entonces el archivo de
configuración y creará nuevos workers mediante fork.

Para comprender mejor cómo se usan estas señales, es importante entender todo el mecanismo de
reinicio.

Primero, hay un proceso haproxy existente en ejecución. El administrador usa un comando específico
del sistema, como «/etc/init.d/haproxy reload», para indicar que quiere aplicar el nuevo archivo de
configuración. Lo que ocurre entonces es lo siguiente. Primero, el script de servicio
(/etc/init.d/haproxy o equivalente) verificará que el archivo de configuración se analiza
correctamente usando «haproxy -c». Después de eso, intentará iniciar haproxy con este archivo de
configuración, usando «-st» o «-sf».

Luego, HAProxy intenta enlazarse a todos los puertos de escucha. Si ocurre algún error fatal (por
ejemplo: una dirección no presente en el sistema, permiso denegado), el proceso termina con un
error. Si el enlace de un socket falla porque un puerto ya está en uso, el proceso enviará primero
una señal SIGTTOU a todos los PID especificados en la lista de PID de «-st» o «-sf». Es lo que se
llama la señal de «pausa». Indica a todos los procesos haproxy existentes que dejen de escuchar
temporalmente en sus puertos, de modo que el nuevo proceso pueda intentar enlazarse de nuevo.
Durante este tiempo, el proceso antiguo continúa procesando las conexiones existentes. Si el enlace
sigue fallando (porque, por ejemplo, un puerto se comparte con otro demonio), el nuevo proceso envía
una señal SIGTTIN a los procesos antiguos para indicarles que reanuden las operaciones como si nada
hubiera pasado. Los procesos antiguos volverán entonces a escuchar en los puertos y seguirán
aceptando conexiones. Ten en cuenta que este mecanismo depende del sistema y algunos sistemas
operativos podrían no soportarlo en modo multiproceso.

Si el nuevo proceso consigue enlazarse correctamente a todos los puertos, envía el SIGTERM (parada
abrupta en caso de «-st») o el SIGUSR1 (parada suave en caso de «-sf») a todos los procesos para
notificarles que ahora está a cargo de las operaciones y que los procesos antiguos tendrán que
marcharse, ya sea de inmediato o cuando hayan terminado su trabajo.

Es importante señalar que durante este periodo existen dos ventanas pequeñas de unos pocos
milisegundos cada una en las que es posible que se observen algunos fallos de conexión bajo cargas
elevadas. Las tasas de fallo observadas típicamente rondan 1 fallo durante una operación de recarga
por cada 10000 conexiones nuevas por segundo, lo que significa que un sitio muy cargado funcionando
a 30000 conexiones nuevas por segundo puede experimentar unas 3 conexiones fallidas en cada recarga.
Las dos situaciones en las que esto ocurre son:

- si el nuevo proceso falla al enlazarse debido a la presencia del proceso antiguo, primero tendrá
  que pasar por la secuencia SIGTTOU+SIGTTIN, que suele durar alrededor de un milisegundo para unas
  decenas de frontends, y durante la cual algunos puertos no estarán enlazados al proceso antiguo
  ni todavía enlazados al nuevo. HAProxy evita esto en los sistemas que soportan las opciones de
  socket SO_REUSEPORT, ya que permiten que el nuevo proceso se enlace sin pedir antes al proceso
  antiguo que se desenlace. La mayoría de los sistemas BSD lo han soportado casi desde siempre.
  Linux lo soportó en la versión 2.0 y lo eliminó hacia la 2.2, aunque por entonces circulaban
  algunos parches. Se reintrodujo en el kernel 3.9, de modo que si observas una tasa de fallo de
  conexión superior a la mencionada anteriormente, comprueba que tu kernel sea 3.9 o posterior, o
  que los parches pertinentes se hayan retroportado a tu kernel (menos probable).

- cuando los procesos antiguos cierran los puertos de escucha, el kernel podría no siempre
  redistribuir las conexiones pendientes que quedaban en la cola del socket (backlog). Bajo cargas
  elevadas, un paquete SYN puede llegar justo antes de que el socket se cierre y provocará que se
  envíe un paquete RST al cliente. En algunos entornos críticos donde ni siquiera una pérdida es
  aceptable, esto se trata a veces con reglas de cortafuegos que bloquean los paquetes SYN durante
  la recarga, forzando al cliente a retransmitir. Esto depende totalmente del sistema, ya que
  algunos sistemas podrían revisar otras colas de escucha y evitar este RST. Un segundo caso
  concierne al ACK del cliente sobre un socket local que estaba en estado SYN_RECV justo antes del
  cierre. Este ACK provocará un paquete RST mientras el proceso haproxy todavía no está al tanto.
  Este caso es más difícil de eliminar, aunque las reglas de filtrado del cortafuegos mencionadas
  anteriormente funcionan bien si se aplican un segundo más o menos antes de reiniciar el proceso.

Para la gran mayoría de los usuarios, estas pérdidas nunca ocurrirán, ya que no tienen carga
suficiente para disparar las condiciones de carrera. Y para la mayoría de los usuarios con mucho
tráfico, la tasa de fallo sigue estando bastante dentro del margen de ruido, siempre que al menos
SO_REUSEPORT esté correctamente soportado en sus sistemas.
