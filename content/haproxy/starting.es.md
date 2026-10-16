---
title: "3. Inicio de HAProxy"
linkTitle: "3. Inicio de HAProxy"
weight: 270
description: "Sintaxis de la línea de comandos, opciones, carga de la configuración y comportamiento al iniciar"
icon: fa-solid fa-play
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/starting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

HAProxy se inicia invocando el programa «haproxy» con una serie de argumentos pasados por la línea de
comandos. La sintaxis real es:

```shell
$ haproxy [<options>]*
```

donde [`<options>`]\* es cualquier número de opciones. Una opción siempre comienza por «-» seguido de
una o más letras, y posiblemente seguida de uno o varios argumentos adicionales. Sin ninguna opción,
HAProxy muestra la página de ayuda con un recordatorio de las opciones soportadas. Las opciones
disponibles pueden variar ligeramente según el sistema operativo. Un buen número de estas opciones se
solapan con una equivalente de la sección «global». En tal caso, la línea de comandos siempre tiene
precedencia sobre el archivo de configuración, de modo que la línea de comandos puede usarse para
forzar rápidamente algunos ajustes sin tocar los archivos de configuración. La lista actual de
opciones es:

<a id="entry-3-entry"></a>

**`-- <cfgfile>*`**

```haproxy
-- <cfgfile>*
```

todos los argumentos que siguen a «--» son rutas de archivos o directorios de configuración que se
cargan y procesan en el orden de declaración. Es útil sobre todo cuando se depende del shell para
cargar muchos archivos ordenados numéricamente. Consulta también «-f». La diferencia entre «--» y «-f»
es que debe colocarse un «-f» antes de cada nombre de archivo, mientras que basta un solo «--» antes
de todos los nombres de archivo. Ambas opciones pueden usarse juntas y el orden de la línea de
comandos sigue aplicándose. Cuando se especifica más de un archivo, cada archivo debe comenzar en un
límite de sección, de modo que la primera palabra clave de cada archivo debe ser una de «global»,
«defaults», «peers», «listen», «frontend», «backend», etcétera. Un archivo no puede contener, por
ejemplo, solo una lista de servidores.

<a id="entry-3-f"></a>

**`-f <cfgfile|cfgdir>`**

```haproxy
-f <cfgfile|cfgdir>
```

añade `<cfgfile>` a la lista de archivos de configuración que se van a cargar. Si `<cfgdir>` es un
directorio, todos los archivos (y solo archivos) que contiene se añaden en orden lexicográfico
(usando LC_COLLATE=C) a la lista de archivos de configuración que se van a cargar; solo se añaden los
archivos con extensión «.cfg» y solo los archivos no ocultos (sin prefijo «.»). Los archivos de
configuración se cargan y procesan en su orden de declaración. Esta opción puede especificarse varias
veces para cargar varios archivos. Consulta también «--». La diferencia entre «--» y «-f» es que debe
colocarse un «-f» antes de cada nombre de archivo, mientras que basta un solo «--» antes de todos los
nombres de archivo. Ambas opciones pueden usarse juntas y el orden de la línea de comandos sigue
aplicándose. Cuando se especifica más de un archivo, cada archivo debe comenzar en un límite de
sección, de modo que la primera palabra clave de cada archivo debe ser una de «global», «defaults»,
«peers», «listen», «frontend», «backend», etcétera. Un archivo no puede contener, por ejemplo, solo
una lista de servidores.

<a id="entry-3-c"></a>

**`-C <dir>`**

```haproxy
-C <dir>
```

cambia al directorio `<dir>` antes de cargar los archivos de configuración. Esto es útil cuando se
usan rutas relativas. Precaución al usar comodines después de «--», que en realidad son reemplazados
por el shell antes de iniciar haproxy.

<a id="entry-3-d"></a>

**`-D`**

```haproxy
-D
```

inicia como demonio. El proceso se desvincula del terminal actual tras el fork, y los errores ya no
se informan en el terminal. Es equivalente a la palabra clave «daemon» de la sección «global» de la
configuración. Se recomienda forzarlo siempre en cualquier script de init para que una configuración
defectuosa no impida el arranque del sistema.

<a id="entry-3-l"></a>

**`-L <name>`**

```haproxy
-L <name>
```

cambia el nombre del par local a `<name>`, que por defecto es el nombre de host local. Esto se usa
solo con la replicación entre pares. Puedes usar la variable \$HAPROXY_LOCALPEER en el archivo de
configuración para referenciar el nombre del par.

<a id="entry-3-n"></a>

**`-N <limit>`**

```haproxy
-N <limit>
```

establece el maxconn por proxy predeterminado en `<limit>` en lugar del valor integrado por defecto
(normalmente 2000). Solo útil para depuración.

<a id="entry-3-v"></a>

**`-V`**

```haproxy
-V
```

activa el modo detallado (desactiva el modo silencioso). Revierte el efecto de «-q» o «quiet».

<a id="entry-3-w"></a>

**`-W`**

```haproxy
-W
```

modo master-worker. Es equivalente a la palabra clave «master-worker» de la sección «global» de la
configuración. Este modo lanzará un «master» que vigilará los «workers». Usando este modo, puedes
recargar HAProxy directamente enviando una señal SIGUSR2 al master. El modo master-worker es
compatible tanto con el modo de primer plano como con el modo demonio. Se recomienda usar este modo
con multiproceso y systemd.

<a id="entry-3-ws"></a>

**`-Ws`**

```haproxy
-Ws
```

modo master-worker con soporte del tipo `notify` de servicio de systemd.

<a id="entry-3-4"></a>

**`-4`**

```haproxy
-4
```

obliga a los resolvedores DNS a consultar y aceptar solo direcciones IPv4 (registros «A»). Puede
usarse al enfrentar dificultades en ciertos entornos sin conectividad dual-stack de extremo a extremo.
Anula la directiva global «dns-accept-family» y la fuerza a «ipv4».

<a id="entry-3-c-2"></a>

**`-c`**

```haproxy
-c
```

solo realiza una comprobación de los archivos de configuración y sale antes de intentar enlazarse. El
estado de salida es cero si todo está bien, o distinto de cero si se encuentra un error. La presencia
de avisos se informará si los hay. Por defecto esta opción no informa de un mensaje de éxito.
Combinada con «-V», mostrará el mensaje «Configuration file is valid» en caso de éxito.

Los scripts deben usar el estado de salida para determinar el éxito del comando.

<a id="entry-3-cc"></a>

**`-cc`**

```haproxy
-cc
```

evalúa una condición tal como se usa dentro de un bloque condicional de la configuración. El estado
de salida es cero si la condición es verdadera, 1 si la condición es falsa o 2 si se encuentra un
error.

<a id="entry-3-d-2"></a>

**`-d`**

```haproxy
-d
```

activa el modo de depuración. Esto desactiva el modo demonio, obliga al proceso a permanecer en
primer plano y a mostrar los eventos entrantes y salientes. Nunca debe usarse en un script de init.

<a id="entry-3-entry-2"></a>

**`-dA[file]`**

```haproxy
-dA[file]
```

vuelca un archivo con todas las dependencias detectadas en el arranque en el archivo designado, en
formato tar, inmediatamente después de que la configuración termine de cargarse. Es equivalente a
«set-dumpable libs», pero en lugar de mantener las bibliotecas en memoria, las vuelca a un archivo.
Puede usarse tras un volcado de memoria (core dump), con el fin de proporcionar a los desarrolladores
todas las bibliotecas necesarias para permitirles explotar el core. Puede no estar disponible en
todos los sistemas operativos. Se recomienda encarecidamente usarlo con los archivos de configuración
habituales y, opcionalmente, con «-c» cuando se usa manualmente, para que haproxy salga inmediatamente
después del volcado, sin arrancar. Ejemplo:

```shell
$ haproxy -dA/tmp/libs.tar -c -f /etc/haproxy/haproxy.cfg
```

<a id="entry-3-entry-3"></a>

**`-dC[key]`**

```haproxy
-dC[key]
```

vuelca el archivo de configuración. Se realiza después de trocear las líneas en tokens, de modo que
los comentarios se eliminan y se fuerza la sangría. Si se especifica una clave no nula, las líneas se
truncan antes de los campos sensibles/confidenciales, y los identificadores y direcciones se emiten
con hash aplicando esta clave, usando el mismo algoritmo que el empleado por el modo anonimizado en la
CLI. Esto significa que la salida puede compartirse con seguridad con un desarrollador que la
necesite para entender qué ocurre en un volcado anonimizado con la misma clave. Consulta también el
comando «set anon» de la CLI.

<a id="entry-3-dd"></a>

**`-dD`**

```haproxy
-dD
```

activa el modo de diagnóstico. Este modo mostrará avisos adicionales sobre declaraciones de
configuración sospechosas. Algunas salidas impedirán el arranque en modo «zero-warning».

Ten presente que tales diagnósticos están esencialmente destinados a concienciar a las personas sobre
ciertos problemas latentes potenciales que podrían ser totalmente intencionales, y están sujetos a
cambios, incluso dentro de una rama estable así como entre máquinas que ejecutan exactamente las
mismas configuraciones. Por ello *sí* informarán regularmente como sospechosas declaraciones válidas,
y solo deberían usarse combinados con «-c» para realizar un diagnóstico más profundo. Su resultado
nunca debería usarse para impedir que arranque un servicio (lo que ocurre al combinarlos con
«zero-warning» o «-dW»).

<a id="entry-3-df"></a>

**`-dF`**

```haproxy
-dF
```

desactiva el reenvío rápido de datos (data fast-forward). Es un mecanismo para optimizar el reenvío
de datos pasándolos directamente de un lado al otro sin despertar el flujo. Gracias a esta directiva,
es posible desactivar esta optimización. Ten en cuenta que también desactiva cualquier splice TCP del
kernel. Este comando no está pensado para uso regular; generalmente solo lo sugerirán los
desarrolladores durante sesiones de depuración complejas.

<a id="entry-3-dg"></a>

**`-dG`**

```haproxy
-dG
```

desactiva el uso de getaddrinfo() para resolver nombres de host en direcciones. Puede usarse cuando
se sospecha que getaddrinfo() no funciona como se espera. Esta opción se puso a disposición porque
existen muchas implementaciones defectuosas de getaddrinfo() en diversos sistemas que causan
anomalías difíciles de diagnosticar.

<a id="entry-3-di"></a>

**`-dI`**

```haproxy
-dI
```

activa el fork inseguro. Es el equivalente de «insecure-fork-wanted» en la sección global. Puede ser
útil al ejecutar todas las reg-tests con ASAN, que necesitan hacer fork de addr2line para resolver
las direcciones.

<a id="entry-3-entry-4"></a>

**`-dK<class[,class]*>`**

```haproxy
-dK<class[,class]*>
```

vuelca la lista de palabras clave registradas en cada clase. La lista de clases está disponible con
«-dKhelp». Todas las clases pueden volcarse usando «-dKall»; de lo contrario, puede especificarse
como una lista separada por comas una selección de las mostradas en la ayuda. El formato de salida
variará según la clase de palabras clave que se vuelque (p. ej., «cfg» mostrará las palabras clave de
configuración conocidas en un formato parecido al del archivo de configuración, mientras que «smp»
mostrará las funciones de extracción de muestras precedidas de una matriz de compatibilidad con cada
conjunto de reglas). Rara vez podrán usarlas tal cual los humanos, pero pueden ser de gran ayuda para
herramientas externas que intentan detectar la aparición de nuevas palabras clave en ciertos lugares
para actualizar automáticamente documentación, archivos de resaltado de sintaxis, analizadores de
configuración, API, etcétera. El formato de salida puede evolucionar algo con el tiempo, así que es
muy recomendable usar esta salida sobre todo para detectar diferencias con archivos anteriores. Ten
en cuenta que no se listan todas las palabras clave porque muchas existieron mucho antes de que se
crearan los distintos subsistemas de registro de palabras clave y no aparecen allí. Sin embargo,
dado que las nuevas palabras clave solo se añaden mediante los mecanismos modernos, es razonablemente
seguro asumir que esta salida puede usarse para detectar adiciones al lenguaje con buena precisión.
Las palabras clave solo se vuelcan después de que la configuración se haya analizado por completo, de
modo que incluso las palabras clave creadas dinámicamente pueden volcarse. Una buena forma de volcar
y salir es ejecutar una comprobación silenciosa de configuración sobre una configuración existente:

```text
./haproxy -dKall -q -c -f foo.cfg
```

Si no hay ningún archivo de configuración disponible, usar «-f /dev/null» también servirá para volcar
todas las palabras clave por defecto, pero entonces el estado de retorno no será cero, ya que no
habrá ningún listener, y deberá ignorarse.

<a id="entry-3-dl"></a>

**`-dL`**

```haproxy
-dL
```

vuelca la lista de bibliotecas compartidas dinámicas que se cargan al final del procesamiento de la
configuración. Esto incluirá generalmente también dependencias profundas, como cualquier cosa cargada
desde código Lua, por ejemplo, así como el propio ejecutable. La lista se imprime en un formato que
debería ser bastante fácil de sanear para producir directamente un tarball con todas las
dependencias. Dado que no detiene el arranque del programa, se recomienda usarlo solo en combinación
con «-c» y «-q», donde solo se mostrará la lista de objetos cargados (o nada en caso de error).
Además, ten presente que al proporcionar tal paquete para ayudar con el análisis de un archivo core,
la mayoría de las bibliotecas son en realidad enlaces simbólicos que deben desreferenciarse al crear
el archivo:

```text
./haproxy -W -q -c -dL -f foo.cfg | tar -T - -hzcf archive.tgz
```

Cuando se arranca en modo detallado (-V), los rangos de direcciones de las bibliotecas compartidas
también se enumeran, salvo que esté en uso el modo silencioso (-q).

<a id="entry-3-entry-5"></a>

**`-dM[<byte>[,]][help|options,...]`**

```haproxy
-dM[<byte>[,]][help|options,...]
```

fuerza el envenenamiento de la memoria (memory poisoning) y/o cambia otras opciones de depuración de
memoria. El envenenamiento de la memoria significa que cada región de memoria asignada con malloc() o
pool_alloc() se rellenará con `<byte>` antes de entregarse al solicitante. Cuando no se especifica
`<byte>`, el valor por defecto es 0x50 («P»). Aunque esto ralentiza ligeramente las operaciones,
resulta útil para provocar de forma fiable problemas derivados de inicializaciones faltantes en el
código que causan fallos aleatorios. Ten en cuenta que -dM0 tiene el efecto de convertir cualquier
malloc() en un calloc(). En cualquier caso, si un error aparece o desaparece al usar esta opción,
significa que hay un error en haproxy, así que repórtalo. Hay una serie de otras opciones disponibles,
ya sea solas o después de una coma que sigue al byte. La opción especial «help» listará las opciones
actualmente soportadas y su valor actual. Cada opción de depuración puede forzarse activada o
desactivada. Las opciones más óptimas suelen elegirse en tiempo de compilación según el sistema
operativo y no necesitan ajustarse, salvo que lo sugiera un desarrollador. Las opciones de depuración
soportadas incluyen (activar/desactivar):

- fail / no-fail:

```text
Esto activa el fallo aleatorio de las asignaciones de memoria, en conjunción
con el ajuste global «tune.fail-alloc». Se usa para detectar comprobaciones
de error faltantes en el código. Activar la opción preestablece la proporción
a una tasa de fallo del 1%.
```

- no-merge / merge:

```text
Por defecto, los grupos (pools) de tamaños muy similares se fusionan, lo que
da más eficiencia, pero complica el análisis de ciertos volcados de memoria.
Esta opción permite desactivar este mecanismo y puede aumentar ligeramente
el uso de memoria.
```

- cold-first / hot-first:

```text
Para optimizar la tasa de acierto de la caché de CPU, por defecto los objetos
liberados más recientemente («calientes») se reciclan para las nuevas asignaciones.
Pero hacerlo también complica el análisis de los volcados de memoria y puede
ocultar errores de uso tras liberación (use-after-free). Esta opción permite
en su lugar escoger primero los objetos más fríos, lo que puede resultar en
un ligero aumento del uso de CPU.
```

- integrity / no-integrity:

```text
Cuando esta opción está activada, se habilitan comprobaciones de integridad
de la memoria sobre la zona asignada para verificar que no ha sido modificada
desde su última liberación. Funciona mejor con «no-merge», «cold-first» y
«tag». Activarla aumentará ligeramente el uso de CPU.
```

- backup / no-backup:

```text
Esta opción realiza una copia de cada objeto liberado en el momento de la
liberación, lo que permite a los desarrolladores inspeccionarlos. También
realiza una comparación en el momento de la asignación para detectar si algo
cambió entretanto, lo que indica una condición de uso tras liberación.
Duplica el uso de memoria y aumenta ligeramente el uso de CPU (similar a
«integrity»). Si se combina con «integrity», todavía duplica los contenidos
pero no realiza la comparación (que «integrity» sí realiza). Al igual que
«integrity», funciona mejor con «no-merge», «cold-first» y «tag».
```

- no-global / global:

```text
Según el sistema operativo, puede activarse una caché global de memoria para
todo el proceso si se estima que el asignador estándar es demasiado lento o
ineficiente con los hilos. Esta opción permite forzar su desactivación o su
activación. Desactivarla puede aumentar el uso de CPU con asignadores
ineficientes. Activarla puede aumentar el uso de memoria con asignadores
eficientes.
```

- no-cache / cache:

```text
Cada hilo usa una caché local de objetos muy rápida para las asignaciones,
siempre activada por defecto. Esta opción permite desactivarla. Dado que la
caché global también pasa por las cachés locales, esto resultará
efectivamente en desactivar todas las cachés y asignar directamente desde el
asignador por defecto. Puede producir un aumento significativo del uso de
CPU, pero también pequeños ahorros de memoria en sistemas diminutos.
```

- caller / no-caller:

```text
Activar esta opción reserva algo de espacio adicional en cada objeto asignado
para almacenar la dirección del último invocador que lo asignó o liberó.
Esto ayuda a los desarrolladores a retroceder en el tiempo al analizar
volcados de memoria y a conjeturar cómo ocurrió algo inesperado.
```

- tag / no-tag:

```text
Activar esta opción reserva algo de espacio adicional en cada objeto asignado
para almacenar una etiqueta que permite detectar errores como la doble
liberación, la liberación de un objeto inválido y los desbordamientos de
búfer. Ofrece garantías de fiabilidad mucho más sólidas a costa de 4 u 8
bytes adicionales por asignación. Suele ser el primer paso para detectar la
corrupción de memoria.
```

- poison / no-poison:

```text
Activar esta opción rellenará los objetos asignados con un patrón fijo que
asegurará que ciertos valores accidentales como 0 no estén presentes si un
campo recién añadido fue olvidado por error en una rutina de inicialización.
Tales errores tienden a reproducirse rara vez, especialmente cuando los
grupos no se fusionan. Esto normalmente se activa pasando directamente el
valor del byte a -dM, pero usar esta opción permite desactivar/activar el
uso de un valor establecido previamente.
```

<a id="entry-3-dr"></a>

**`-dR`**

```haproxy
-dR
```

desactiva la opción de socket SO_REUSEPORT en los puertos de escucha. Es equivalente a la palabra
clave «noreuseport» de la sección «global». Puede aplicarse en escenarios de multihilo, cuando se
observan problemas de reparto de carga entre los hilos de haproxy (puede monitorizarse con top).

<a id="entry-3-ds"></a>

**`-dS`**

```haproxy
-dS
```

desactiva el uso de la llamada al sistema splice(). Es equivalente a la palabra clave «nosplice» de
la sección «global». Puede usarse cuando se sospecha que splice() se comporta de forma inadecuada o
causa problemas de rendimiento, o cuando se usa strace para ver los datos reenviados (que no
aparecen al usar splice()).

<a id="entry-3-dt"></a>

**`-dT`**

```haproxy
-dT
```

desactiva el uso de ktls. Es equivalente a la palabra clave «noktls» de la sección «global». Es útil
sobre todo cuando se sospecha de un error relacionado con ktls.

<a id="entry-3-dv"></a>

**`-dV`**

```haproxy
-dV
```

desactiva la verificación SSL en el lado del servidor. Es equivalente a tener «ssl-server-verify
none» en la sección «global». Esto es útil para intentar reproducir problemas de producción fuera del
entorno de producción. Nunca uses esto en un script de init, pues degrada la seguridad SSL hacia los
servidores.

<a id="entry-3-dw"></a>

**`-dW`**

```haproxy
-dW
```

si está activada, haproxy se negará a arrancar si se emitió algún aviso durante el procesamiento de
la configuración. Esto ayuda a detectar errores sutiles y a mantener la configuración limpia y
portable entre versiones. Se recomienda activar esta opción en los scripts de servicio cuando las
configuraciones las gestionan personas, pero se recomienda no usarla con configuraciones generadas,
que tienden a emitir más avisos. Puede combinarse con «-c» para hacer que los avisos hagan fallar las
configuraciones comprobadas. Es equivalente a la opción global «zero-warning».

<a id="entry-3-dz"></a>

**`-dZ`**

```haproxy
-dZ
```

desactiva el reenvío de datos en modo «zero-copy». Es equivalente a la palabra clave
«tune.disable-zero-copy-forwarding» de la sección «global». Puede ser útil en caso de problemas de
pérdida o integridad de datos, o al usar strace para ver los datos reenviados, ya que también
desactiva cualquier splice TCP del kernel.

<a id="entry-3-db"></a>

**`-db`**

```haproxy
-db
```

desactiva el modo en segundo plano y el modo multiproceso. El proceso permanece en primer plano. Se
usa principalmente durante el desarrollo o en pruebas pequeñas, pues basta un Ctrl-C para detener el
proceso. Nunca lo uses en un script de init.

<a id="entry-3-dc"></a>

**`-dc`**

```haproxy
-dc
```

activa la depuración de la afinidad de CPU. La lista de las CPU seleccionadas y desalojadas, así como
su topología, se informará antes de arrancar.

<a id="entry-3-de"></a>

**`-de`**

```haproxy
-de
```

desactiva el uso del poller «epoll». Es equivalente a la palabra clave «noepoll» de la sección
«global». Es útil sobre todo cuando se sospecha de un error relacionado con este poller. En sistemas
que soportan epoll, el mecanismo de reserva será generalmente el poller «poll».

<a id="entry-3-dk"></a>

**`-dk`**

```haproxy
-dk
```

desactiva el uso del poller «kqueue». Es equivalente a la palabra clave «nokqueue» de la sección
«global». Es útil sobre todo cuando se sospecha de un error relacionado con este poller. En sistemas
que soportan kqueue, el mecanismo de reserva será generalmente el poller «poll».

<a id="entry-3-dp"></a>

**`-dp`**

```haproxy
-dp
```

desactiva el uso del poller «poll». Es equivalente a la palabra clave «nopoll» de la sección
«global». Es útil sobre todo cuando se sospecha de un error relacionado con este poller. En sistemas
que soportan poll, el mecanismo de reserva será generalmente el poller «select», que no puede
desactivarse y está limitado a 1024 descriptores de archivos.

<a id="entry-3-dr-2"></a>

**`-dr`**

```haproxy
-dr
```

ignora los fallos de resolución de direcciones de los servidores. Es muy común, al validar una
configuración fuera de producción, no tener acceso a los mismos resolvedores y fallar en la
resolución de direcciones de los servidores, lo que dificulta probar una configuración. Esta opción
simplemente añade el método «none» a la lista de métodos de resolución de direcciones para todos los
servidores, garantizando que, incluso si la libc falla al resolver una dirección, la secuencia de
arranque no se interrumpe.

<a id="entry-3-dt-2"></a>

**`-dt [<trace_desc>,...]`**

```haproxy
-dt [<trace_desc>,...]
```

activa las trazas en stderr. Sin argumento, esto habilita todas las fuentes de traza en el nivel de
error. Puede ser notablemente útil para detectar violaciones de protocolo de clientes o servidores.
Un argumento opcional puede usarse para especificar una lista de diversas configuraciones de traza
usando «,» como separador. Cada elemento activa una o todas las fuentes de traza. Además, el nivel y
la verbosidad pueden especificarse opcionalmente en cada elemento usando «:» como separador interno
con el nombre de la traza. Al introducir una verbosidad o un nombre de nivel no válidos, se presenta
la lista de palabras clave disponibles. Por ejemplo, puede ser cómodo pasar «help» en cada campo para
consultar primero la lista.

<a id="entry-3-dv-2"></a>

**`-dv`**

```haproxy
-dv
```

desactiva el uso del poller «evports». Es equivalente a la palabra clave «noevports» de la sección
«global». Es útil sobre todo cuando se sospecha de un error relacionado con este poller. En sistemas
que soportan event ports (SunOS derivado de Solaris 10 y posteriores), el mecanismo de reserva será
generalmente el poller «poll».

<a id="entry-3-m"></a>

**`-m <limit>`**

```haproxy
-m <limit>
```

limita la memoria asignable, que se usa para guardar los datos del proceso, a `<limit>` megabytes.
Esto puede causar algunos rechazos de conexión o ralentizaciones según la cantidad de memoria
necesaria para las operaciones normales. Se usa sobre todo para forzar al proceso haproxy a trabajar
en un escenario de consumo de recursos restringido. Es importante señalar que la memoria no se
comparte entre los procesos haproxy y que un proceso hijo creado mediante la llamada al sistema
fork() hereda los límites de recursos de su padre. Así, en modo master-worker este límite de memoria
se aplica por separado al master y a su proceso worker bifurcado.

<a id="entry-3-n-2"></a>

**`-n <limit>`**

```haproxy
-n <limit>
```

limita a `<limit>` el límite de conexiones por proceso. Es equivalente a la palabra clave «maxconn»
de la sección global. Tiene precedencia sobre esa palabra clave. Puede usarse para forzar
rápidamente límites más bajos y evitar una interrupción del servicio en sistemas donde los límites de
recursos son demasiado bajos.

<a id="entry-3-p"></a>

**`-p <file>`**

```haproxy
-p <file>
```

escribe los pids de todos los procesos en `<file>` durante el arranque. Es equivalente a la palabra
clave «pidfile» de la sección «global». El archivo se abre antes de entrar en la jaula chroot, y
después de ejecutar el chdir() implícito por «-C». Cada pid aparece en su propia línea.

<a id="entry-3-q"></a>

**`-q`**

```haproxy
-q
```

establece el modo «quiet». Esto desactiva los mensajes de salida. Puede usarse en combinación con
«-c» para comprobar solamente si un archivo de configuración es válido o no.

<a id="entry-3-s"></a>

**`-S <bind>[,bind_options...]`**

```haproxy
-S <bind>[,bind_options...]
```

en modo master-worker, enlaza una CLI maestra, que permite el acceso a todos los procesos, tanto los
en ejecución como los que están terminando. Por razones de seguridad, se recomienda enlazar la CLI
maestra a un socket UNIX local. Las opciones de enlace son las mismas que las de la palabra clave
«bind» del archivo de configuración, con las palabras separadas por comas en lugar de espacios.

Ten en cuenta que este socket no puede usarse para recuperar los sockets de escucha de un proceso
antiguo durante una recarga sin interrupción.

<a id="entry-3-sf"></a>

**`-sf <pid>*`**

```haproxy
-sf <pid>*
```

envía la señal «finish» (SIGUSR1) a los procesos antiguos tras completar el arranque, para pedirles
que terminen lo que están haciendo y se retiren. `<pid>` es una lista de pids a los que enviar la señal (uno por
argumento). La lista termina en cualquier opción que comience por «-». No es un problema que la lista
de pids esté vacía, de modo que pueda construirse al vuelo a partir del resultado de un comando como
«pidof» o «pgrep».

<a id="entry-3-st"></a>

**`-st <pid>*`**

```haproxy
-st <pid>*
```

envía la señal «terminate» (SIGTERM) a los procesos antiguos tras completar el arranque, para
terminarlos de inmediato sin que terminen lo que estaban haciendo. `<pid>` es una lista de pids a los que
enviar la señal (uno por argumento). La lista termina en cualquier opción que comience por «-». No es un
problema que la lista de pids esté vacía, de modo que pueda construirse al vuelo a partir del
resultado de un comando como «pidof» o «pgrep».

<a id="entry-3-v-2"></a>

**`-v`**

```haproxy
-v
```

informa de la versión y la fecha de compilación.

<a id="entry-3-vv"></a>

**`-vv`**

```haproxy
-vv
```

muestra la versión, las opciones de compilación, las versiones de las bibliotecas y los pollers
utilizables. Esta salida se solicita sistemáticamente al presentar un informe de error.

<a id="entry-3-x"></a>

**`-x <unix_socket>`**

```haproxy
-x <unix_socket>
```

se conecta al socket especificado e intenta recuperar los sockets de escucha del proceso antiguo, y
los usa en lugar de intentar enlazar otros nuevos. Esto es útil para no perder ninguna conexión nueva
al recargar la configuración en Linux.

Sin el modo master-worker, la capacidad debe activarse en el socket de estadísticas usando
«expose-fd listeners» en tu configuración.

En modo master-worker no necesita «expose-fd listeners»: el master usará automáticamente esta opción
en una recarga con la sintaxis «sockpair@», que permite al master conectarse directamente a un worker
sin usar ningún socket de estadísticas declarado en la configuración. Si quieres desactivar esto,
puedes pasar -x /dev/null.

Una forma segura de iniciar HAProxy desde un archivo de init consiste en forzar el modo demonio,
guardar los pids existentes en un archivo pid y usar ese archivo pid para notificar a los procesos
antiguos que terminen antes de retirarse:

```text
haproxy -f /etc/haproxy.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Cuando la configuración se divide en algunos archivos específicos (p. ej.: tcp frente a http), se
recomienda usar la opción «-f»:

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Cuando se espera un número desconocido de archivos, como archivos específicos de cada cliente, se
recomienda asignarles un nombre que comience por un número de secuencia de tamaño fijo y usar «--»
para cargarlos, posiblemente después de cargar algunos valores por defecto:

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid) \
        -f /etc/haproxy/default-customers.cfg -- /etc/haproxy/customers/*
```

A veces puede producirse un fallo de arranque por la razón que sea. Entonces es importante verificar
si la versión de HAProxy que estás invocando es la esperada y si soporta las funciones que esperas
(p. ej.: SSL, PCRE, compresión, Lua, etcétera). Esto puede verificarse usando «haproxy -vv». Allí se
informa de cierta información importante, como ciertas opciones de compilación, el sistema objetivo y
las versiones de las bibliotecas en uso. También es lo que se te pedirá sistemáticamente al enviar un
informe de error:

```shell
$ haproxy -vv
```

HAProxy version 1.6-dev7-a088d3-4 2015/10/08 Copyright 2000-2015 Willy Tarreau <willy@haproxy.org>

Build options:

```text
TARGET  = linux2628
CPU     = generic
CC      = gcc
CFLAGS  = -pg -O0 -g -fno-strict-aliasing -Wdeclaration-after-statement \
          -DBUFSIZE=8030 -DMAXREWRITE=1030 -DSO_MARK=36 -DTCP_REPAIR=19
OPTIONS = USE_ZLIB=1 USE_DLMALLOC=1 USE_OPENSSL=1 USE_LUA=1 USE_PCRE=1
```

Default settings:

```text
maxconn = 2000, bufsize = 8030, maxrewrite = 1030, maxpollevents = 200
```

Encrypted password support via crypt(3): yes Built with zlib version: 1.2.6 Compression algorithms
supported: identity("identity"), deflate("deflate"), &#92;
raw-deflate("deflate"), gzip("gzip") Built with OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 Running
on OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 OpenSSL library supports TLS extensions: yes OpenSSL
library supports SNI: yes OpenSSL library supports prefer-server-ciphers: yes Built with PCRE
version: 8.12 2011-01-15 PCRE library supports JIT: no (USE_PCRE_JIT not set) Built with Lua
version: Lua 5.3.1 Built with transparent proxy support using: IP_TRANSPARENT IP_FREEBIND

Available polling systems:

```text
 epoll: pref=300,  test result OK
  poll: pref=200,  test result OK
select: pref=150,  test result OK
```

Total: 3 (3 usable), will use epoll.

La información relevante que muchos usuarios no desarrolladores pueden verificar aquí es la
siguiente:
<a id="entry-3-the-version"></a>

**`- la versión`**

```haproxy
- la versión
```

1.6-dev7-a088d3-4 arriba significa que el código está actualmente en el commit con ID «a088d3», que
es el 4.º posterior a la versión oficial «1.6-dev7». La versión 1.6-dev7 se mostraría como
«1.6-dev7-8c1ad7». Lo que importa aquí es de hecho «1.6-dev7». Es la 7.ª versión de desarrollo de lo
que en el futuro se convertirá en la versión 1.6. Una versión de desarrollo no apta para uso en
producción (salvo que sepas exactamente lo que haces). Una versión estable se mostrará como una
versión de 3 números, como «1.5.14-16f863», lo que indica el nivel 14 de corrección sobre la versión
1.5. Es una versión lista para producción.

<a id="entry-3-the-release-date"></a>

**`- la fecha de publicación`**

```haproxy
- la fecha de publicación
```

2015/10/08. Está representada en el formato universal año/mes/día. Aquí esto significa 8 de octubre
de 2015. Dado que las versiones estables se emiten cada pocos meses (1-2 meses al principio, a veces
6 meses cuando el producto se vuelve muy estable), si ves aquí una fecha antigua, significa que
probablemente te afectan una serie de errores o problemas de seguridad que ya se han corregido y que
quizá valga la pena comprobar el sitio oficial.

<a id="entry-3-build-options"></a>

**`- las opciones de compilación`**

```haproxy
- las opciones de compilación
```

son relevantes para las personas que construyen ellas mismas sus paquetes; pueden explicar por qué las cosas no
se comportan como se espera. Por ejemplo, la versión de desarrollo anterior se construyó para Linux
2.6.28 o posterior, orientada a una CPU genérica (sin optimizaciones específicas de CPU), y carece de
cualquier optimización de código (-O0), así que su rendimiento será bajo.

<a id="entry-3-libraries-versions"></a>

**`- las versiones de las bibliotecas`**

```haproxy
- las versiones de las bibliotecas
```

la versión de zlib se informa tal como se encuentra en la propia biblioteca. En general zlib se
considera un producto muy estable y las actualizaciones casi nunca son necesarias. OpenSSL informa de
dos versiones: la utilizada en tiempo de compilación y la que se está usando, tal como se encuentra
en el sistema. Estas pueden diferir en la última letra pero nunca en los números. La fecha de
compilación también se informa porque la mayoría de los errores de OpenSSL son problemas de
seguridad que deben tomarse en serio, de modo que esta biblioteca necesita absolutamente mantenerse
al día. Ver aquí una versión de 4 meses de antigüedad es muy sospechoso y, en efecto, se perdió una
actualización. PCRE proporciona expresiones regulares muy rápidas y es muy recomendable. Ciertas de
sus extensiones, como JIT, no están presentes en todas las versiones y siguen siendo jóvenes, así que
algunas personas prefieren no compilar con ellas, razón por la cual también se informa del estado de
la compilación. En cuanto al lenguaje de scripting Lua, HAProxy espera la versión 5.3, que es muy
joven puesto que se publicó poco antes de HAProxy 1.6. Es importante comprobar en el sitio web de Lua
si se proponen correcciones para esta rama.

<a id="entry-3-available-polling-systems"></a>

**`- Los sistemas de sondeo disponibles afectarán a la escalabilidad del proceso cuando`**

```haproxy
- Los sistemas de sondeo disponibles afectarán a la escalabilidad del proceso cuando
```

se trate de más de unas mil conexiones simultáneas. Estos solo están disponibles cuando se indicó el
sistema correcto en la variable TARGET durante la compilación. El mecanismo «epoll» es muy
recomendable en Linux, y el mecanismo kqueue es muy recomendable en BSD. Su ausencia provocará que se
use poll() o incluso select(), causando un uso alto de CPU al manejar muchas conexiones.
