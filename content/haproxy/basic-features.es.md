---
title: "Funciones básicas"
linkTitle: "Funciones básicas"
weight: 40
description: "Proxy, TLS, monitorización, alta disponibilidad, balanceo, persistencia, registros y estadísticas"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/intro/basic-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 3.3–3.3.8"
---

Esta sección enumerará una serie de funciones que HAProxy implementa, algunas de las cuales
generalmente se esperan de cualquier balanceador de carga moderno, y otras son un beneficio directo
de la arquitectura de HAProxy. Las funciones más avanzadas se detallarán en la sección siguiente.

## 3.3.1. Funciones básicas : Proxy {#section-3-3-1}

Hacer de proxy es la acción de transferir datos entre un cliente y un servidor a través de dos
conexiones independientes. HAProxy soporta las siguientes funciones básicas en relación con el
proxy y la gestión de conexiones:

- Proporcionar al servidor una conexión limpia para protegerlo contra cualquier defecto o ataque
  del lado del cliente;

- Escuchar en múltiples direcciones IP y/o puertos, incluso rangos de puertos;

- Aceptación transparente: interceptar tráfico dirigido a cualquier dirección IP arbitraria que
  ni siquiera pertenece al sistema local;

- El puerto del servidor no tiene que guardar relación con el puerto de escucha, e incluso puede
  trasladarse con un desplazamiento fijo (útil con rangos);

- Conexión transparente: suplantar la dirección IP del cliente (o cualquiera) si hace falta al
  conectarse al servidor;

- Proporcionar a los servidores una dirección IP de retorno fiable en balanceadores de carga
  multi-sitio;

- Descargar de trabajo al servidor gracias a búferes y posiblemente conexiones de corta duración
  para reducir su número de conexiones concurrentes y su huella de memoria;

- Optimizar las pilas TCP (p. ej. SACK), el control de congestión y reducir el impacto del RTT;

- Soportar familias de protocolos diferentes en ambos lados (p. ej. IPv4/IPv6/Unix);

- Aplicación de tiempos de espera: HAProxy soporta múltiples niveles de tiempos de espera según la
  etapa en que se encuentre la conexión, de modo que un cliente o servidor muerto, o un atacante,
  no pueda retener recursos durante demasiado tiempo;

- Validación de protocolo: HTTP, SSL o la carga útil se inspeccionan y los elementos de protocolo
  inválidos se rechazan, salvo que se indique que se acepten de todos modos;

- Aplicación de políticas: garantizar que solo lo permitido puede reenviarse;

- Tanto las conexiones entrantes como las salientes pueden limitarse a ciertos espacios de nombres
  de red (solo Linux), lo que facilita construir un balanceador de carga multiinquilino entre
  contenedores;

- El protocolo PROXY presenta la dirección IP del cliente al servidor incluso para tráfico no
  HTTP. Se trata de una extensión de HAProxy que ya ha sido adoptada por varios productos de
  terceros, al menos los siguientes en el momento de escribir esto:

  - cliente: haproxy, stud, stunnel, exaproxy, ELB, squid
  - servidor: haproxy, stud, postfix, exim, nginx, squid, node.js, varnish

## 3.3.2. Funciones básicas : SSL {#section-3-3-2}

La pila SSL de HAProxy está reconocida como una de las más completas según los ingenieros de
Google (<http://istlsfastyet.com/>). Las funciones más comúnmente usadas que la hacen bastante
completa son:

- multi-alojamiento basado en SNI sin límite en el número de sitios y centrado en el rendimiento.
  Se conoce al menos un despliegue que gestiona 50000 dominios con sus respectivos certificados;

- el soporte de certificados comodín reduce la necesidad de muchos certificados;

- autenticación de cliente basada en certificados con políticas configurables ante el fallo en la
  presentación de un certificado válido. Esto permite, por ejemplo, presentar una granja de
  servidores diferente para regenerar el certificado del cliente;

- la autenticación del servidor backend garantiza que el servidor backend es el real y no un
  intermediario (man in the middle);

- la autenticación con el servidor backend permite que este sepa que realmente es el nodo haproxy
  esperado el que se conecta a él;

- las extensiones TLS NPN y ALPN hacen posible asumir de forma fiable el procesamiento SSL de conexiones SPDY/HTTP2 y
  pasarlas en texto claro a los servidores backend;

- el OCSP stapling reduce aún más el tiempo de carga de la primera página entregando en línea una
  respuesta OCSP cuando el cliente solicita un Certificate Status Request;

- el dimensionado dinámico de registros proporciona a la vez alto rendimiento y baja latencia, y
  reduce significativamente el tiempo de carga de las páginas al permitir que el navegador empiece
  a recuperar objetos nuevos mientras los paquetes siguen en vuelo;

- acceso permanente a toda la información relevante de la capa SSL/TLS para registro, control de
  acceso, informes, etc. Estos elementos pueden incrustarse en una cabecera HTTP o incluso como
  una extensión del protocolo PROXY, de modo que el servidor liberado del procesamiento SSL reciba toda la
  información que habría tenido de haber realizado él mismo la terminación SSL.

- Detectar, registrar y bloquear ciertos ataques conocidos incluso sobre bibliotecas SSL
  vulnerables, como el ataque Heartbleed que afecta a ciertas versiones de OpenSSL.

- soporte para la reanudación de sesión sin estado (extensión TLS Ticket del RFC 5077). Los
  tickets TLS pueden actualizarse desde la CLI, lo que proporciona los medios para implementar
  Perfect Forward Secrecy rotando los tickets con frecuencia.

## 3.3.3. Funciones básicas : Monitorización {#section-3-3-3}

HAProxy se concentra mucho en la disponibilidad. Como tal, se preocupa por el estado de los
servidores y por reportar su propio estado a otros componentes de red:

- El estado de los servidores se monitoriza continuamente usando parámetros por servidor. Esto
  garantiza que la ruta hacia el servidor está operativa para el tráfico regular;

- Las comprobaciones de estado soportan dos histéresis para las transiciones a activo y a caído,
  con el fin de protegerse contra las fluctuaciones de estado;

- Las comprobaciones pueden enviarse a una dirección/puerto/protocolo diferente: esto facilita
  comprobar un único servicio que se considera representativo de varios, por ejemplo el puerto
  HTTPS de un servidor HTTP+HTTPS.

- Los servidores pueden seguir el estado de otros servidores y caerse simultáneamente: esto
  garantiza que los servidores que alojan múltiples servicios puedan fallar de forma atómica y que
  nadie sea enviado a un servidor parcialmente fallido;

- Pueden desplegarse agentes en el servidor para monitorizar la carga y el estado: a un servidor
  puede interesarle reportar su carga, su estado operativo y su estado administrativo de forma
  independiente de lo que las comprobaciones de estado pueden ver. Ejecutando un agente simple en
  el servidor, es posible considerar la visión que el servidor tiene de su propio estado, además
  de las comprobaciones de estado que validan la ruta completa;

- Hay disponibles varios métodos de comprobación: conexión TCP, solicitud HTTP, saludo SMTP,
  saludo SSL, LDAP, SQL, Redis, scripts send/expect, todos con o sin SSL;

- El cambio de estado se notifica en los registros y en la página de estadísticas con el motivo
  del fallo (p. ej. la respuesta HTTP recibida en el momento en que se detectó el fallo). También
  puede enviarse un correo electrónico a una dirección configurable en cada cambio;

- El estado del servidor también se reporta en la interfaz de estadísticas y puede usarse para
  tomar decisiones de enrutado, de modo que el tráfico pueda enviarse a granjas diferentes según
  su tamaño y/o salud (p. ej. la pérdida de un enlace entre centros de datos);

- HAProxy puede usar las solicitudes de comprobación de estado para pasar información a los
  servidores, como sus nombres, el peso, el número de otros servidores en la granja, etc., para
  que los servidores ajusten su respuesta y sus decisiones con base en ese conocimiento (p. ej.
  posponer las copias de seguridad para conservar más CPU disponible);

- Los servidores pueden usar las comprobaciones de estado para reportar un estado más detallado
  que simplemente activo/apagado (p. ej. quiero detenerme, por favor deja de enviar visitantes
  nuevos);

- El propio HAProxy puede reportar su estado a componentes externos como routers u otros
  balanceadores de carga, lo que permite construir infraestructuras multicapa y multirruta muy
  completas.

## 3.3.4. Funciones básicas : Alta disponibilidad {#section-3-3-4}

Igual que cualquier balanceador de carga serio, HAProxy se preocupa mucho por la disponibilidad
para garantizar la mejor continuidad global del servicio:

- Solo se usan los servidores válidos; los demás son expulsados automáticamente de las granjas de
  balanceo de carga; bajo ciertas condiciones sigue siendo posible forzar su uso;

- Soporte de un apagado controlado para poder sacar servidores de una granja sin afectar a
  ninguna conexión;

- Los servidores de respaldo se usan automáticamente cuando los servidores activos caen y los
  sustituyen, de modo que las sesiones no se pierdan cuando sea posible. Esto permite además
  construir múltiples rutas para alcanzar el mismo servidor (p. ej. múltiples interfaces);

- Capacidad de devolver un estado global de fallo para una granja cuando hay demasiados
  servidores caídos. Esto, combinado con las capacidades de monitorización, permite que un
  componente aguas arriba elija un nodo del balanceador de carga diferente para un servicio dado;

- El diseño sin estado facilita construir clústeres: por diseño, HAProxy hace todo lo posible por
  garantizar la máxima continuidad del servicio sin tener que almacenar información que pudiera
  perderse en caso de fallo. Esto asegura que una toma de control sea lo más fluida posible;

- Se integra bien con el demonio VRRP estándar keepalived: HAProxy comunica fácilmente su estado
  a keepalived y convive muy bien con direcciones IP virtuales flotantes. Nota: usa solo
  protocolos de redundancia de IP (VRRP/CARP) en lugar de soluciones basadas en clúster
  (Heartbeat, ...), ya que son los que ofrecen la conmutación más rápida, fluida y fiable.

## 3.3.5. Funciones básicas : Balanceo de carga {#section-3-3-5}

HAProxy ofrece un conjunto bastante completo de funciones de balanceo de carga, la mayoría de las
cuales, por desgracia, no están disponibles en otros muchos productos de balanceo de carga:

- se soportan no menos de 10 algoritmos de balanceo de carga, algunos de los cuales se aplican a
  los datos de entrada para ofrecer una lista infinita de posibilidades. Los más comunes son
  round-robin (para conexiones cortas, elegir cada servidor por turnos), leastconn (para
  conexiones largas, elegir el menos recientemente usado de los servidores con menor número de
  conexiones), source (para granjas SSL o granjas de servidores de terminal, el servidor depende
  directamente de la dirección de origen del cliente), URI (para cachés HTTP, el servidor depende
  directamente del URI HTTP), hdr (el servidor depende directamente del contenido de un campo de
  cabecera HTTP concreto), first (para máquinas virtuales de corta duración, todas las conexiones
  se empaquetan en el subconjunto más pequeño posible de servidores para que los no usados puedan
  apagarse);

- todos los algoritmos anteriores soportan pesos por servidor, de modo que es posible convivir con
  diferentes generaciones de servidores en una granja, o dirigir una pequeña fracción del tráfico a
  servidores específicos (modo de depuración, ejecución de la próxima versión del software, etc);

- se soportan pesos dinámicos para round-robin, leastconn y el hash consistente; esto permite
  modificar los pesos de los servidores al vuelo desde la CLI o incluso mediante un agente
  ejecutándose en el servidor;

- el arranque gradual (slow-start) está soportado siempre que se soporta un peso dinámico; esto
  permite que un servidor tome el tráfico progresivamente. Es una función importante para
  servidores de aplicaciones frágiles que necesitan compilar clases en tiempo de ejecución, así
  como para cachés frías que necesitan llenarse antes de funcionar a pleno rendimiento;

- el hash puede aplicarse a diversos elementos como la dirección de origen del cliente,
  componentes de la URL, elementos de la cadena de consulta, valores de campos de cabecera,
  parámetros POST, cookies RDP;

- el hash consistente protege a las granjas de servidores contra la redistribución masiva al añadir
  o eliminar servidores en una granja. Es muy importante en grandes granjas de caché y permite
  usar el arranque gradual para rellenar cachés frías;

- una serie de métricas internas como el número de conexiones por servidor, por backend, la
  cantidad de huecos de conexión disponibles en un backend, etc. hacen posible construir
  estrategias de balanceo de carga muy avanzadas.

## 3.3.6. Funciones básicas : Persistencia {#section-3-3-6}

El balanceo de carga de aplicaciones sería inútil sin persistencia. HAProxy proporciona un
conjunto bastante completo de posibilidades para mantener a un visitante en el mismo servidor
incluso a través de diversos eventos como la adición/eliminación de servidores o ciclos de
caída/subida, y algunos métodos están diseñados para ser resistentes a la distancia entre
múltiples nodos de balanceo de carga, en el sentido de que no requieren ninguna replicación:

- la información de persistencia puede coincidir y aprenderse individualmente de lugares
  diferentes si se desea. Por ejemplo, una cookie JSESSIONID puede buscarse tanto en una cookie
  como en la URL. Pueden aprenderse hasta 8 fuentes en paralelo al mismo tiempo y cada una puede
  apuntar a una tabla de persistencia diferente;

- la información de persistencia puede provenir de cualquier cosa visible dentro de una solicitud
  o respuesta, incluida la dirección de origen, desplazamiento y longitud de la carga útil TCP,
  elementos de la cadena de consulta HTTP, valores de campos de cabecera, cookies, etc.

- las tablas de persistencia se replican entre todos los nodos de forma multi-maestro;

- elementos de uso común como SSL-ID o las cookies RDP (para granjas TSE) son directamente
  accesibles para facilitar la manipulación;

- todas las reglas de persistencia pueden quedar condicionadas dinámicamente por ACL;

- es posible decidir no persistir en ciertos servidores, como los de respaldo, de modo que cuando
  el servidor nominal vuelva, recupere automáticamente la carga. Esto se usa a menudo en entornos
  multirruta;

- en HTTP a menudo se prefiere no aprender nada y en su lugar manipular una cookie dedicada a la
  persistencia. Para ello, es posible detectar, reescribir, insertar o prefijar dicha cookie para
  que el cliente recuerde qué servidor se le asignó;

- el servidor puede decidir cambiar o limpiar la cookie de persistencia al cerrar sesión, de modo
  que los visitantes que se marchan queden automáticamente desvinculados del servidor;

- usando reglas basadas en ACL también es posible ignorar o forzar selectivamente la persistencia
  independientemente del estado del servidor; combinado con comprobaciones de estado avanzadas,
  esto ayuda a los administradores a verificar que el servidor que están instalando funciona
  correctamente antes de presentarlo al mundo entero;

- un mecanismo innovador para establecer un tiempo máximo de inactividad y una duración en las
  cookies garantiza que la persistencia pueda detenerse suavemente en dispositivos que nunca se
  apagan (smartphones, televisores, electrodomésticos) sin tener que almacenarlas en un soporte
  persistente;

- múltiples entradas de servidor pueden compartir las mismas claves de persistencia, de modo que
  esta no se pierda en entornos multirruta cuando una ruta cae;

- la parada suave (soft-stop) garantiza que solo los usuarios con información de persistencia
  seguirán llegando al servidor que se les asignó, pero ningún usuario nuevo irá allí.

## 3.3.7. Funciones básicas : Registro {#section-3-3-7}

El registro es una función extremadamente importante para un balanceador de carga, primero porque
a un balanceador de carga a menudo se le acusa injustamente de causar los problemas que revela, y
segundo porque está situado en un punto crítico de una infraestructura donde toda la actividad
normal y anómala debe analizarse y correlacionarse con otros componentes.

HAProxy proporciona registros muy detallados, con precisión de milisegundos y el momento exacto de
aceptación de la conexión, que puede buscarse en los registros de los cortafuegos (p. ej. para
correlacionar NAT). Por defecto, los registros TCP y HTTP son bastante detallados y contienen todo
lo necesario para el diagnóstico de problemas, como la dirección IP y el puerto de origen, el
frontend, el backend, el servidor, los temporizadores (duración de recepción de la solicitud,
duración en cola, tiempo de establecimiento de la conexión, tiempo de las cabeceras de respuesta,
tiempo de transferencia de datos), el estado global del proceso, los contadores de conexiones, el
estado de la cola, el número de reintentos, las acciones de persistencia detalladas y los motivos
de desconexión, y las capturas de cabeceras con una codificación de salida segura. Es posible
entonces ampliar o sustituir este formato para incluir cualquier dato muestreado, variables,
capturas, dando como resultado información muy detallada. Por ejemplo, es posible registrar el
número acumulado de solicitudes o el número de URLs diferentes visitadas por un cliente.

El nivel de registro puede ajustarse por solicitud usando ACL estándar, de modo que es posible
silenciar automáticamente algunos registros considerados ruido y en su lugar elevar avisos cuando
ocurra algún comportamiento anómalo en una pequeña parte del tráfico (p. ej. demasiadas URLs o
errores HTTP para una dirección de origen). También se emiten registros administrativos con sus
propios niveles para informar, por ejemplo, de la pérdida o recuperación de un servidor.

Cada frontend y backend puede usar múltiples salidas de registro independientes, lo que facilita
el multiinquilino. Los registros se envían preferentemente por UDP, posiblemente codificados en
JSON, y se truncan tras una longitud de línea configurable para garantizar la entrega. Pero
también es posible enviarlos a stdout/stderr o a cualquier descriptor de archivo, así como a un
búfer circular al que un cliente puede suscribirse para recuperarlos.

## 3.3.8. Funciones básicas : Estadísticas {#section-3-3-8}

HAProxy proporciona una interfaz web de informes de estadísticas con autenticación, niveles de
seguridad y ámbitos. Así es posible proporcionar a cada cliente alojado su propia página que
muestra únicamente sus propias instancias. Esta página puede ubicarse en una parte oculta de la
URL del sitio web habitual, de modo que no haya que abrir ningún puerto nuevo. Esta página
también puede reportar la disponibilidad de otros nodos HAProxy, de manera que sea fácil ver de
un vistazo si todo funciona como se espera. La vista es sintética con muchos detalles accesibles
(como causas de error, último acceso y duración del último cambio, etc), los cuales también están
accesibles como una tabla CSV que otras herramientas pueden importar para dibujar gráficas. La
página puede autorrefrescarse para usarse como página de monitorización en una pantalla grande. En
modo administración, la página permite además cambiar el estado de los servidores para facilitar
las operaciones de mantenimiento.

También se proporciona un exportador de Prometheus para que las estadísticas puedan consumirse en
un formato diferente según el despliegue.
