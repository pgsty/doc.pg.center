---
title: "12. Depuración y problemas de rendimiento"
linkTitle: "12. Depuración"
weight: 360
description: "Métodos de investigación de caídas, bloqueos, latencia y problemas de rendimiento"
icon: fa-solid fa-bug
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/debugging-and-performance/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---

Cuando HAProxy se inicia con la opción «-d», permanece en primer plano e imprime una línea por
evento, como una conexión entrante, el final de una conexión, y por cada línea de cabecera de
petición o respuesta vista. Esta salida de depuración se emite antes de que los contenidos se
procesen, de modo que no tiene en cuenta las modificaciones locales. Su uso principal es mostrar las
peticiones y respuestas sin tener que ejecutar un analizador de red. La salida es menos legible
cuando se manejan múltiples conexiones en paralelo, aunque los scripts «debug2ansi» y «debug2html»
que se encuentran en el directorio examples/ ayudan definitivamente en este caso coloreando la
salida.

Si una petición o respuesta HTTP/1.x es rechazada porque HAProxy detecta que está mal formada, lo
mejor que se puede hacer es conectarse a la CLI y ejecutar «show errors», que informará de la última
petición y respuesta HTTP/1.x defectuosas capturadas para cada frontend y backend, con toda la
información necesaria para indicar con precisión el primer carácter del flujo de entrada que fue
rechazado. Esto a veces es necesario para demostrar a clientes o desarrolladores que hay un bug
presente en su código. En este caso, a menudo es posible relajar las comprobaciones (pero conservar
las capturas) usando «option accept-unsafe-violations-in-http-request» o su equivalente para las
respuestas provenientes del servidor «option accept-unsafe-violations-in-http-response». Consulta el
manual de configuración para más detalles.

Ejemplo:

```shell
> show errors
Total events captured on [13/Oct/2015:13:43:47.169]: 1

[13/Oct/2015:13:43:40.918] frontend HAProxyLocalStats (#2): invalid request
  backend <NONE> (#-1), server <NONE> (#-1), event #0
  src 127.0.0.1:51981, session #0, session flags 0x00000080
  HTTP msg state 26, msg flags 0x00000000, tx flags 0x00000000
  HTTP chunk len 0 bytes, HTTP body len 0 bytes
  buffer flags 0x00808002, out 0 bytes, total 31 bytes
  pending 31 bytes, wrapping at 8040, error at position 13:

  00000  GET /invalid request HTTP/1.1\r\n

```

La salida de «show info» en la CLI proporciona cierta cantidad de información útil sobre la tasa
máxima de conexiones alcanzada, la tasa máxima de claves SSL alcanzada y, en general, toda la
información que puede ayudar a explicar problemas temporales relacionados con el uso de CPU o de
memoria. Ejemplo:

```shell
> show info
Name: HAProxy
Version: 1.6-dev7-e32d18-17
Release_date: 2015/10/12
Nbproc: 1
Process_num: 1
Pid: 7949
Uptime: 0d 0h02m39s
Uptime_sec: 159
Memmax_MB: 0
Ulimit-n: 120032
Maxsock: 120032
Maxconn: 60000
Hard_maxconn: 60000
CurrConns: 0
CumConns: 3
CumReq: 3
MaxSslConns: 0
CurrSslConns: 0
CumSslConns: 0
Maxpipes: 0
PipesUsed: 0
PipesFree: 0
ConnRate: 0
ConnRateLimit: 0
MaxConnRate: 1
SessRate: 0
SessRateLimit: 0
MaxSessRate: 1
SslRate: 0
SslRateLimit: 0
MaxSslRate: 0
SslFrontendKeyRate: 0
SslFrontendMaxKeyRate: 0
SslFrontendSessionReuse_pct: 0
SslBackendKeyRate: 0
SslBackendMaxKeyRate: 0
SslCacheLookups: 0
SslCacheMisses: 0
CompressBpsIn: 0
CompressBpsOut: 0
CompressBpsRateLim: 0
ZlibMemUsage: 0
MaxZlibMemUsage: 0
Tasks: 5
Run_queue: 1
Idle_pct: 100
node: wtap
description:
```

Cuando un problema parece aparecer aleatoriamente en una versión nueva de HAProxy (p. ej.: cada
segunda petición se aborta, caída ocasional, etc.), vale la pena intentar activar el envenenamiento
de memoria para que cada llamada a malloc() vaya seguida inmediatamente del llenado de la zona de
memoria con un byte configurable. Por defecto este byte es 0x50 («P» en ASCII), pero puede usarse
cualquier otro byte, incluido el cero (que tendrá el mismo efecto que un calloc() y puede hacer que
los problemas desaparezcan). El envenenamiento de memoria se activa desde la línea de comandos con
la opción «-dM». Deteriora ligeramente el rendimiento y no se recomienda su uso en producción. Si un
problema ocurre todo el tiempo con él, o nunca ocurre cuando el envenenamiento usa el byte cero,
significa claramente que has encontrado un bug y que definitivamente debes reportarlo. De lo
contrario, si no hay un cambio claro, el problema no está relacionado.

Al depurar algunos problemas de latencia, es importante usar strace y tcpdump en la máquina local, y
otro tcpdump en el sistema remoto. La razón es que hay retrasos en todas partes de la cadena de
procesamiento y es importante saber cuál causa la latencia para saber dónde actuar. En la práctica,
el tcpdump local indicará cuándo llegan los datos de entrada. Strace indicará cuándo haproxy recibe
esos datos (usando recv/recvfrom). Atención: openssl usa las llamadas al sistema read()/write() en
lugar de recv()/send(). Strace también mostrará cuándo haproxy envía los datos, y tcpdump mostrará
cuándo el sistema los envía a la interfaz. Luego, el tcpdump externo mostrará cuándo los datos
enviados se reciben realmente (dado que el local solo muestra cuándo los paquetes se ponen en cola).
La ventaja de capturar en el sistema local es que strace y tcpdump usarán el mismo reloj de
referencia. Strace debe usarse con «-tts200» para obtener marcas de tiempo completas y reportar
bloques de datos suficientemente grandes para poder leerlos. Tcpdump debe usarse con «-nvvttSs0»
para reportar paquetes completos, números de secuencia reales y marcas de tiempo completas.

En la práctica, los datos recibidos casi siempre son recibidos inmediatamente por haproxy (a menos
que la máquina tenga la CPU saturada o los datos sean inválidos y no se entreguen). Si estos datos
se reciben pero no se envían, generalmente es porque el búfer de salida está saturado (es decir, el
destinatario no consume los datos lo bastante rápido). Esto puede confirmarse observando que el
sondeo no notifica la posibilidad de escribir en el descriptor de fichero de salida durante un
tiempo (a menudo es más fácil detectarlo en la salida de strace cuando los datos finalmente salen,
y luego retroceder para ver cuándo se notificó el evento de escritura). Generalmente coincide con un
ACK recibido del destinatario y detectado por tcpdump. Una vez enviados, los datos pueden pasar
algún tiempo en el sistema sin hacer nada. Aquí también, la ventana de congestión TCP puede estar
limitada y no permitir que esos datos salgan, a la espera de un ACK que abra la ventana. Si el
tráfico está inactivo y los datos tardan 40 ms o 200 ms en salir, es una cuestión distinta (que no
es un problema): el algoritmo de Nagle impide que los paquetes vacíos salgan inmediatamente, con la
esperanza de que se fusionen con datos posteriores. HAProxy desactiva automáticamente Nagle en modo
TCP puro y en los túneles. Sin embargo, definitivamente permanece activado al reenviar un cuerpo
HTTP (y esto contribuye allí a la mejora del rendimiento al reducir el número de paquetes). Algunas
aplicaciones no conformes con HTTP pueden ser sensibles a la latencia al entregar mensajes de
respuesta HTTP incompletos. En este caso tendrás que activar «option http-no-delay» para desactivar
Nagle y así sortear su diseño, teniendo en cuenta que cualquier otro proxy de la cadena puede verse
afectado de forma similar. Si tcpdump reporta que los datos salen inmediatamente pero el otro
extremo no los ve rápidamente, puede significar que hay un enlace WAN congestionado, una LAN
congestionada con control de flujo activado que impide que los datos salgan, o más comúnmente que
HAProxy se ejecuta de hecho en una máquina virtual y que, por la razón que sea, el hipervisor ha
decidido que los datos no necesitaban enviarse inmediatamente. En entornos virtualizados, los
problemas de latencia casi siempre los causa la capa de virtualización, así que para ahorrar tiempo
conviene comparar primero el tcpdump en la VM y en los componentes externos. Cualquier diferencia
debe atribuirse al hipervisor y a sus controladores acompañantes.

Cuando se ven segmentos TCP SACK en las trazas de tcpdump (usando -vv), siempre significa que el
lado que los envía ha obtenido la prueba de la pérdida de un paquete. Aunque no verlos no significa
que no haya pérdidas, verlos significa definitivamente que la red tiene pérdidas. Las pérdidas son
normales en una red, pero a una tasa en la que los SACK no se aprecian a simple vista. Si aparecen
mucho en las trazas, vale la pena investigar exactamente qué ocurre y dónde se pierden los paquetes.
HTTP no maneja bien las pérdidas de TCP, que introducen latencias enormes.

El comando «netstat -i» mostrará estadísticas por interfaz. Una interfaz cuyo contador Rx-Ovr crece
indica que el sistema no tiene recursos suficientes para recibir todos los paquetes entrantes y que
se pierden antes de ser procesados por el controlador de red. Rx-Drp indica que algunos paquetes
recibidos se perdieron en la pila de red porque la aplicación no los procesa lo bastante rápido.
Esto también puede ocurrir durante algunos ataques. Tx-Drp significa que las colas de salida estaban
llenas y hubo que descartar paquetes. Con TCP esto debería ser muy raro, pero posiblemente indicará
un enlace saliente saturado.
