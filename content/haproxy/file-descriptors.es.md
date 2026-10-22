---
title: "5. Límites de los descriptores de archivos"
linkTitle: "5. Descriptores de archivos"
weight: 290
description: "Límites de descriptores, dimensionamiento, restricciones del sistema y resolución de problemas"
icon: fa-solid fa-folder-open
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/file-descriptors/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 5"
---

Para garantizar que todas las conexiones entrantes se atiendan con éxito, HAProxy calcula en el
momento de la carga el número total de descriptores de archivos que se necesitarán durante la vida
del proceso. Un proceso Unix normal generalmente recibe 1024 descriptores de archivos por defecto, y
un proceso con privilegios puede elevar este límite por sí mismo. Esta es una de las razones para
iniciar HAProxy como root y dejar que ajuste el límite. El límite predeterminado de 1024
descriptores de archivos permite procesar aproximadamente unas 500 conexiones simultáneas. El cálculo
se basa en el parámetro global maxconn, que limita el número total de conexiones por proceso, el
número de listeners, el número de servidores con una comprobación de estado activada, las
comprobaciones de agente, los peers, los registradores (loggers) y posiblemente algunos otros
requisitos técnicos. Una estimación aproximada y simple de este número consiste simplemente en
duplicar el valor de maxconn y añadir unas decenas para obtener el número aproximado de descriptores
de archivos necesarios.

Originalmente HAProxy no sabía calcular este valor, y era necesario pasarlo mediante el ajuste
«ulimit-n» en la sección global. Esto explica por qué incluso hoy en día se ven muchas
configuraciones con este ajuste presente. Desafortunadamente, a menudo se calculaba mal, lo que
provocaba fallos de conexión al acercarse a maxconn, en lugar de limitar las conexiones entrantes
mientras se esperaban los recursos necesarios. Por esta razón, es importante eliminar cualquier
ajuste «ulimit-n» residual que pueda quedar de versiones muy antiguas.

Aumentar el número de descriptores de archivos para aceptar incluso cargas moderadas es obligatorio,
pero conlleva algunos ajustes específicos del sistema operativo. En primer lugar, el sistema de
sondeo select() está limitado a 1024 descriptores de archivos. De hecho, en Linux solía ser capaz de
gestionar más, pero dado que ciertos sistemas operativos se entregan con políticas SELinux
excesivamente restrictivas que prohíben el uso de select() con más de 1024 descriptores de archivos,
HAProxy ahora se niega a iniciarse en este caso para evitar cualquier problema en tiempo de
ejecución. En todos los sistemas operativos admitidos, poll() está disponible y no sufre esta
limitación. Se selecciona automáticamente, así que no hay que hacer nada para obtener una
configuración funcional. Pero poll() se vuelve muy lento cuando aumenta el número de descriptores de
archivos. Aunque HAProxy hace todo lo posible por limitar este impacto en el rendimiento (p. ej.,
mediante el uso de la caché interna de descriptores de archivos y el procesamiento por lotes), una
buena regla práctica es que usar poll() con más de mil conexiones simultáneas consumirá mucha CPU.

Para los sistemas Linux basados en los núcleos 2.6 y superiores, se utilizará la llamada al sistema
epoll(). Es un mecanismo mucho más escalable que se apoya en retrollamadas (callbacks) en el núcleo,
que garantizan un tiempo de activación constante independientemente del número de descriptores de
archivos monitorizados registrados. Se utiliza automáticamente donde se detecta, siempre que HAProxy
se haya compilado para una de las variantes de Linux. Su presencia y soporte pueden verificarse con
«haproxy -vv».

Para los sistemas BSD que lo admiten, kqueue() está disponible como alternativa. Es mucho más rápido
que poll() e incluso ligeramente más rápido que epoll() gracias a su gestión por lotes de los
cambios. Al menos FreeBSD y OpenBSD lo admiten. Al igual que con epoll() de Linux, su soporte y
disponibilidad se muestran en la salida de «haproxy -vv».

Tener un buen poller es una cosa, pero es obligatorio que el proceso pueda alcanzar los límites.
Cuando HAProxy se inicia, establece inmediatamente los límites de descriptores de archivos del nuevo
proceso y comprueba si tiene éxito. En caso de fallo, lo notifica antes de hacer el fork para que el
administrador pueda ver el problema. Mientras el proceso se inicie como root, no debería haber
ninguna razón para que este ajuste falle. Sin embargo, puede fallar si el proceso lo inicia un
usuario sin privilegios. Si existe una razón imperiosa para *no* iniciar haproxy como root (p. ej.,
iniciado por usuarios finales o por una cuenta por aplicación), el administrador del sistema puede
elevar el límite de descriptores de archivos para ese usuario específico. La efectividad del ajuste
puede verificarse ejecutando «ulimit -n» desde la línea de comandos del usuario. Debería reflejar el
nuevo límite.

Aviso: cuando los límites de un usuario sin privilegios se cambian en la cuenta de dicho usuario, es
bastante común que estos valores solo se tengan en cuenta cuando el usuario inicia sesión, y no en
absoluto en algunos scripts ejecutados en el arranque del sistema ni en las crontabs. Esto depende
totalmente del sistema operativo; recuerda comprobar «ulimit -n» antes de iniciar haproxy cuando se
ejecute de esta manera. El consejo general es nunca iniciar haproxy como un usuario sin privilegios
para producción. Otra buena razón es que ello impide a haproxy activar algunas protecciones de
seguridad.

Una vez que se tiene la certeza de que el sistema permitirá al proceso haproxy utilizar el número
solicitado de descriptores de archivos, pueden aparecer dos nuevos límites específicos del sistema.
El primero es el límite de descriptores de archivos a nivel de sistema, que es el número total de
descriptores de archivos abiertos en el sistema, cubriendo todos los procesos. Cuando se alcanza
este límite, accept() o socket() normalmente devolverán ENFILE. El segundo es el límite estricto por
proceso sobre el número de descriptores de archivos, que impide que setrlimit() se establezca con un
valor mayor. Ambos dependen mucho del sistema operativo. En Linux, el límite del sistema se
establece en el arranque en función de la cantidad de memoria. Puede cambiarse con el sysctl
«fs.file-max». Y el límite estricto por proceso está establecido en 1048576 por defecto, pero puede
cambiarse mediante el sysctl «fs.nr_open».

Las limitaciones de descriptores de archivos pueden observarse en un proceso en ejecución cuando
están establecidas demasiado bajas. La utilidad strace reportará que accept() y socket() devuelven
«-1 EMFILE» cuando se han alcanzado los límites del proceso. En este caso, simplemente elevar el
valor de «ulimit-n» (o eliminarlo) resolverá el problema. Si estas llamadas al sistema devuelven
«-1 ENFILE», significa que se han alcanzado los límites del núcleo y que debe hacerse algo en un
parámetro global del sistema. Estos problemas deben abordarse sin falta, ya que provocan un uso
elevado de CPU (cuando accept() falla) y conexiones fallidas que generalmente son visibles para el
usuario. Una solución también consiste en reducir el valor maxconn global para imponer la
serialización, y posiblemente desactivar el keep-alive HTTP para forzar que las conexiones se
liberen y se reutilicen más rápido.
