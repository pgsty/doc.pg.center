---
title: "7. Uso de CPU"
linkTitle: "7. CPU"
weight: 310
description: "Hilos, afinidad de CPU, saturación, perfilado y comportamiento del rendimiento"
icon: fa-solid fa-microchip
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/cpu/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 7"
---

> [!WARNING]
> Nota de versión: este capítulo conserva orientación histórica sobre el multiproceso. Desde HAProxy
> 2.5, `nbproc` y `bind process` ya no están soportados. Para esta edición, configura los hilos con
> `nbthread`, `thread-groups` y `cpu-map` en los [parámetros globales](/es/haproxy/global/#section-3-1).

HAProxy pasa normalmente la mayor parte de su tiempo en el sistema y una parte menor en el espacio de
usuario. Una CPU de 3.5 GHz finamente ajustada puede sostener una tasa de aproximadamente 80000
aperturas y cierres de conexiones extremo a extremo por segundo con un 100% de CPU en un solo núcleo.
Cuando un núcleo está saturado, las cifras típicas son:

- 95% sistema, 5% usuario para conexiones TCP largas u objetos HTTP grandes
- 85% sistema y 15% usuario para conexiones TCP cortas u objetos HTTP pequeños en modo de cierre
- 70% sistema y 30% usuario para objetos HTTP pequeños en modo keep-alive

La cantidad de procesamiento de reglas y de expresiones regulares incrementará la parte de espacio
de usuario. La presencia de reglas de cortafuegos, de seguimiento de conexiones y de tablas de
enrutamiento complejas en el sistema incrementará en cambio la parte de sistema.

En la mayoría de los sistemas, el tiempo de CPU observado durante las transferencias de red puede
dividirse en 4 partes:

- la parte de interrupción, que concierne a todo el procesamiento realizado al recibir E/S, antes
  incluso de que se conozca el proceso destino. Típicamente, los paquetes Rx se contabilizan como
  interrupción. En algunos sistemas, como Linux, donde el procesamiento de interrupciones puede
  diferirse a un hilo dedicado, puede aparecer como softirq, y el hilo se llama ksoftirqd/0 (para la
  CPU 0). La CPU que se encarga de esta carga está generalmente definida por la configuración del
  hardware, aunque en el caso del softirq a menudo es posible remapear el procesamiento a otra CPU.
  Esta parte de interrupción a menudo se percibirá como parasitaria, ya que no está asociada a
  ningún proceso, pero en realidad se trata de procesamiento que se realiza para preparar el trabajo
  del proceso.

- la parte de sistema, que concierne a todo el procesamiento realizado con código del núcleo
  invocado desde el espacio de usuario. Las llamadas al sistema se contabilizan como sistema, por
  ejemplo. Todos los paquetes Tx entregados de forma síncrona se contabilizarán como tiempo de
  sistema. Si algunos paquetes deben aplazarse porque las colas se llenan, pueden procesarse
  posteriormente en contexto de interrupción (p. ej., al recibir un ACK que abre una ventana TCP).

- la parte de usuario, que ejecuta exclusivamente código de aplicación en el espacio de usuario.
  HAProxy se ejecuta exclusivamente en esta parte, aunque hace un uso intensivo de las llamadas al
  sistema. El procesamiento de reglas, las expresiones regulares, la compresión y el cifrado
  aumentan la porción de usuario del consumo de CPU.

- la parte de inactividad, que es lo que hace la CPU cuando no hay nada que hacer. Por ejemplo,
  HAProxy espera una conexión entrante, o espera que salgan algunos datos, lo que significa que el
  sistema está esperando un ACK del cliente para enviar esos datos.

En la práctica, respecto a la actividad de HAProxy, en general es razonablemente preciso (pero
totalmente inexacto) considerar que las interrupciones/softirq se deben al procesamiento Rx en los
controladores del núcleo, que el tiempo de usuario se debe al procesamiento de capa 7 en HAProxy, y
que el tiempo de sistema se debe al procesamiento de red en el camino Tx.

Dado que HAProxy se ejecuta en torno a un bucle de eventos, espera nuevos eventos usando poll() (o
cualquier alternativa) y procesa todos estos eventos tan rápido como puede antes de volver a poll()
a esperar nuevos eventos. Mide el tiempo pasado esperando en poll() frente al tiempo dedicado a
procesar eventos. La proporción entre el tiempo de sondeo y el tiempo total se denomina tiempo
«idle», y es la cantidad de tiempo que se pasa esperando a que algo ocurra. Esta proporción se
muestra en la página de estadísticas en la línea «idle», o «Idle_pct» en la CLI. Cuando está cerca
del 100%, significa que la carga es extremadamente baja. Cuando está cerca del 0%, significa que
hay actividad constante. Aunque no puede ser muy preciso en un sistema sobrecargado, porque otros
procesos pueden arrebatarle la CPU al proceso haproxy, sigue proporcionando una buena estimación de
cómo considera HAProxy que está trabajando: si la carga es baja y la proporción de inactividad
también lo es, puede indicar que HAProxy tiene mucho trabajo que hacer, posiblemente por reglas muy
costosas que deben procesarse. Por el contrario, si HAProxy indica que la inactividad está cerca del
100% mientras las cosas van lentas, significa que no puede hacer nada para acelerarlas porque ya
está esperando datos entrantes que procesar. En el ejemplo siguiente, haproxy está completamente
inactivo:

```shell
$ echo "show info" | socat - /var/run/haproxy.sock | grep ^Idle
Idle_pct: 100
```

Cuando la proporción de inactividad empieza a ser muy baja, es importante ajustar el sistema y
colocar correctamente los procesos y las interrupciones para ahorrar la mayor cantidad posible de
recursos de CPU para todas las tareas. Si hay un cortafuegos presente, puede valer la pena intentar
desactivarlo o ajustarlo para asegurarse de que no es responsable de una gran parte de la limitación
del rendimiento. Conviene señalar que descargar un cortafuegos con estado generalmente reduce tanto
la cantidad de interrupciones/softirq como el uso de sistema, ya que este tipo de cortafuegos actúa
tanto en el camino Rx como en el Tx. En Linux, descargar los módulos nf_conntrack e ip_conntrack
permitirá comprobar si hay algo que ganar. Si es así, el módulo funciona con la configuración por
defecto y tendrás que averiguar cómo ajustarlo para obtener un mejor rendimiento. En general, esto
consiste en aumentar considerablemente el tamaño de la tabla hash. En FreeBSD, «pfctl -d» desactivará
el cortafuegos «pf» y su motor con estado al mismo tiempo.

Si se observa que se pasa mucho tiempo en interrupciones/softirq, es importante asegurarse de que no
se ejecuten en la misma CPU. La mayoría de los sistemas tienden a fijar las tareas en la CPU donde
reciben el tráfico de red, ya que para ciertas cargas de trabajo esto mejora las cosas. Pero con
cargas de trabajo muy ligadas a la red es lo contrario: el proceso haproxy tendrá que pelear contra
su contraparte del núcleo. Fijar haproxy a un núcleo de CPU y las interrupciones a otro, compartiendo
ambos la misma caché L3, tiende a aumentar sensiblemente el rendimiento de red, porque en la práctica
la cantidad de trabajo de haproxy y de la pila de red son bastante parecidas, así que cada uno puede
llenar casi por completo una CPU. En Linux esto se hace con taskset (para haproxy) o con cpu-map
(desde la configuración de haproxy), y las interrupciones se asignan bajo /proc/irq. Muchas
interfaces de red soportan varias colas y varias interrupciones. En general ayuda repartirlas entre
un número pequeño de núcleos de CPU, siempre que todos compartan la misma caché L3. Detén siempre
irq_balance, que siempre hace lo peor posible con este tipo de cargas de trabajo.

Para cargas de trabajo limitadas por la CPU, consistentes en mucho tráfico SSL o mucha compresión,
puede valer la pena usar varios procesos dedicados a ciertas tareas, aunque no hay una regla
universal aquí y habrá que realizar experimentación.

Para aumentar la capacidad de CPU, es posible hacer que HAProxy se ejecute como varios procesos,
usando la directiva «nbproc» en la sección global. Sin embargo, hay algunas limitaciones:

- las comprobaciones de estado se ejecutan por proceso, de modo que los servidores destino recibirán
  tantas comprobaciones como procesos en ejecución haya;
- los valores de maxconn y las colas son por proceso, así que debe establecerse el valor correcto
  para evitar sobrecargar los servidores;
- las conexiones salientes deberían evitar el uso de rangos de puertos para evitar conflictos
- las stick-tables son por proceso y no se comparten entre procesos;
- cada sección peers solo puede ejecutarse en un único proceso a la vez;
- las operaciones de la CLI solo actuarán sobre un único proceso a la vez.

Teniendo esto en mente, la configuración más sencilla suele consistir en tener una primera capa
ejecutándose en varios procesos y encargada del procesamiento pesado, que pasa el tráfico a una
segunda capa que se ejecuta en un único proceso. Este mecanismo es adecuado para SSL y la
compresión, que son las dos características más intensivas en CPU. Las instancias pueden encadenarse
fácilmente mediante sockets UNIX (que son más baratos que los sockets TCP y no desperdician puertos)
y el protocolo proxy, que es útil para pasar la información del cliente a la siguiente etapa. Al
hacerlo, en general es buena idea vincular todas las tareas de proceso único al proceso número 1 y
las tareas adicionales a los procesos siguientes, ya que esto facilitará la generación de
configuraciones similares para máquinas diferentes.

En Linux versiones 3.9 y superiores, ejecutar HAProxy en modo multiproceso es mucho más eficiente
cuando cada proceso usa un socket de escucha distinto en la misma IP:puerto; esto hará que el núcleo
reparta la carga uniformemente entre todos los procesos en lugar de despertarlos a todos. Consulta
la opción «process» de las líneas de palabra clave «bind» en el manual de configuración para más
información.
