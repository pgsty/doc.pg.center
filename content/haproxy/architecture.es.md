---
title: "Qué es HAProxy y cómo funciona"
linkTitle: "Arquitectura"
weight: 30
description: "El papel de HAProxy, sus límites, su arquitectura orientada a eventos y su modelo de procesamiento de solicitudes"
icon: fa-solid fa-diagram-project
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/introduction/
  - /haproxy/intro/architecture/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 3–3.2"
---

HAProxy se escribe como «HAProxy» para designar el producto, y como «haproxy» para designar el
programa ejecutable, el paquete de software o un proceso. Sin embargo, ambos se usan habitualmente
para ambos propósitos y se pronuncian H-A-Proxy. En sus inicios, «haproxy» solía significar «high
availability proxy» y el nombre se escribía en dos palabras separadas, aunque hoy en día no
significa nada más que «HAProxy».

## 3.1. Qué es HAProxy y qué no es {#section-3-1}

HAProxy es:

- un proxy TCP: puede aceptar una conexión TCP desde un socket de escucha, conectarse a un servidor
  y unir ambos sockets permitiendo que el tráfico fluya en ambas direcciones; IPv4, IPv6 e incluso
  sockets UNIX están soportados en cualquiera de los lados, por lo que puede constituir una forma
  sencilla de traducir direcciones entre familias distintas.

- un proxy inverso HTTP (llamado «gateway» en la terminología HTTP): se presenta como un servidor,
  recibe solicitudes HTTP sobre conexiones aceptadas en un socket TCP de escucha y pasa las
  solicitudes de estas conexiones a los servidores usando conexiones diferentes. Puede usar
  cualquier combinación de HTTP/1.x o HTTP/2 en cualquier lado, e incluso detectará automáticamente
  el protocolo hablado en cada lado cuando se usa ALPN sobre TLS.

- un terminador / iniciador / sistema de descarga de procesamiento SSL: SSL/TLS puede usarse en la conexión procedente del
  cliente, en la conexión hacia el servidor, o incluso en ambas. Muchos ajustes pueden aplicarse
  por nombre (SNI) y actualizarse en tiempo de ejecución sin reiniciar. Estas configuraciones son
  extremadamente escalables y se han reportado despliegues con decenas hasta centenares de miles de
  certificados.

- un normalizador TCP: dado que las conexiones terminan localmente en el sistema operativo, no hay
  relación entre ambos lados, de modo que tráfico anómalo como paquetes inválidos, combinaciones de
  flags, anuncios de ventana, números de secuencia, conexiones incompletas (inundaciones SYN), etc.
  no se pasará al otro lado. Esto protege a las pilas TCP frágiles de ataques de protocolo, y
  permite además optimizar los parámetros de conexión con el cliente sin tener que modificar los
  ajustes de la pila TCP de los servidores.

- un normalizador HTTP: cuando se configura para procesar tráfico HTTP, solo se pasan las
  solicitudes completas y válidas. Esto protege contra muchos ataques basados en el protocolo.
  Además, las desviaciones de protocolo que la especificación tolera se corrigen para que no causen
  problemas en los servidores (p. ej. cabeceras en múltiples líneas).

- una herramienta de corrección HTTP: puede modificar / corregir / añadir / eliminar / reescribir
  la URL o cualquier cabecera de solicitud o respuesta. Esto ayuda a corregir problemas de
  interoperabilidad en entornos complejos.

- un conmutador basado en contenido: puede considerar cualquier elemento de la solicitud para
  decidir a qué servidor pasar la solicitud o la conexión. Así es posible gestionar múltiples
  protocolos sobre un mismo puerto (p. ej. HTTP, HTTPS, SSH).

- un balanceador de carga de servidores: puede balancear conexiones TCP y solicitudes HTTP. En modo
  TCP, las decisiones de balanceo de carga se toman para toda la conexión. En modo HTTP, las
  decisiones se toman por solicitud.

- un regulador de tráfico: puede aplicar limitación de tasa en varios puntos, proteger los
  servidores contra la sobrecarga, ajustar las prioridades del tráfico según el contenido, e
  incluso pasar dicha información a capas inferiores y a componentes de red externos marcando los
  paquetes.

- una protección contra DDoS y abusos del servicio: puede mantener un gran número de estadísticas
  por dirección IP, URL, cookie, etc. y detectar cuándo se está produciendo un abuso, para luego
  actuar (ralentizar a los infractores, bloquearlos, enviarles contenido obsoleto, etc.).

- un punto de observación para el diagnóstico de problemas de red: debido a la precisión de la
  información reportada en los registros, a menudo se usa para acotar problemas relacionados con la
  red.

- un sistema de descarga del trabajo de compresión HTTP: puede comprimir respuestas que el servidor no comprimió,
  reduciendo así el tiempo de carga de las páginas para clientes con mala conectividad o que usan
  redes móviles de alta latencia.

- un proxy con caché: puede almacenar respuestas en RAM de modo que las solicitudes posteriores del
  mismo objeto eviten el coste de otra transferencia de red desde el servidor mientras el objeto
  siga presente y válido. Sin embargo, no almacenará objetos en ningún soporte persistente. Ten en cuenta
  que esta función de caché está diseñada para no requerir mantenimiento y se centra únicamente en
  ahorrar los valiosos recursos de haproxy, no en ahorrar los recursos del servidor. Las cachés
  diseñadas para optimizar servidores requieren mucho más ajuste y flexibilidad. Si necesitas una
  caché avanzada de ese tipo, usa Varnish Cache, que se integra perfectamente con haproxy,
  especialmente cuando se necesita SSL/TLS en cualquier lado.

- una pasarela FastCGI: FastCGI puede verse como una representación diferente de HTTP y, como tal,
  HAProxy puede balancear directamente una granja que combine cualquier tipo de servidores de
  aplicaciones FastCGI sin necesidad de interponer otro nivel de pasarela entre ellos. Esto se
  traduce en un ahorro de recursos y en una reducción de los costes de mantenimiento.

HAProxy no es:

- un proxy HTTP explícito, es decir, el proxy que usan los navegadores para alcanzar internet.
  Existe excelente software libre dedicado a esta tarea, como Squid. Sin embargo, HAProxy puede
  instalarse frente a dicho proxy para proporcionar balanceo de carga y alta disponibilidad.

- un depurador de datos: no modificará el cuerpo de las solicitudes ni de las respuestas.

- un servidor web estático: durante el arranque se aísla dentro de una jaula chroot y renuncia a
  sus privilegios, de modo que no realizará ni un solo acceso al sistema de archivos una vez
  iniciado. Como tal, no puede convertirse en un servidor web estático (los servidores dinámicos sí
  están soportados mediante FastCGI). Existe excelente software libre para esto, como Apache o
  Nginx, y HAProxy puede instalarse fácilmente frente a ellos para proporcionar balanceo de carga,
  alta disponibilidad y aceleración.

- un balanceador de carga basado en paquetes: no verá paquetes IP ni datagramas UDP, no realizará
  NAT y mucho menos DSR. Son tareas de capas inferiores. Algunos componentes basados en kernel como
  IPVS (Linux Virtual Server) ya lo hacen bastante bien y complementan perfectamente a HAProxy.

## 3.2. Cómo funciona HAProxy {#section-3-2}

HAProxy es un motor orientado a eventos y no bloqueante que combina una capa de E/S muy rápida con
un planificador multihilo basado en prioridades. Como está diseñado con el objetivo de reenviar
datos, su arquitectura está optimizada para mover los datos tan rápido como sea posible con el
menor número posible de operaciones. Se centra en optimizar la eficiencia de la caché de CPU
manteniendo las conexiones en la misma CPU el mayor tiempo posible. Como tal, implementa un modelo
por capas que ofrece mecanismos de derivación en cada nivel, garantizando que los datos no lleguen
a niveles superiores a menos que sea necesario. La mayor parte del procesamiento se realiza en el
kernel, y HAProxy hace todo lo posible por ayudar al kernel a hacer el trabajo tan rápido como
pueda dando ciertas pistas o evitando ciertas operaciones cuando calcula que podrían agruparse más
adelante. Como resultado, las cifras típicas muestran un 15% del tiempo de procesamiento invertido
en HAProxy frente a un 85% en el kernel en modo TCP o HTTP close, y alrededor de un 30% para HAProxy
frente a un 70% para el kernel en modo HTTP keep-alive.

Un único proceso puede ejecutar muchas instancias de proxy; se ha reportado que configuraciones
con hasta 300000 proxies distintos en un solo proceso funcionan sin problemas. Una configuración de
un solo núcleo y una sola CPU es mucho más que suficiente para más del 99% de los usuarios y, como
tal, se anima a los usuarios de contenedores y máquinas virtuales a usar las imágenes absolutamente
más pequeñas que puedan conseguir para ahorrar costes operativos y simplificar el diagnóstico de
problemas. Sin embargo, la máquina donde corre HAProxy no debe jamás usar swap, y su CPU no debe
estar limitada artificialmente (asignación sub-CPU en hipervisores) ni compartirse con procesos de
cómputo intensivo que inducirían una latencia de cambio de contexto muy alta.

El subprocesamiento permite explotar toda la capacidad de procesamiento disponible usando un hilo
por núcleo de CPU. Esto es útil sobre todo para SSL o cuando se necesitan tasas de reenvío de datos
superiores a 40 Gbps. En tales casos es críticamente importante evitar las comunicaciones entre
múltiples CPUs físicas, que pueden causar fuertes cuellos de botella en la pila de red y en el
propio HAProxy. Aunque resulte contraintuitivo para algunos, lo primero que hay que hacer ante
ciertos problemas de rendimiento a menudo es reducir el número de CPUs en que corre HAProxy.

HAProxy solo necesita el ejecutable haproxy y un archivo de configuración para funcionar. Para el
registro, es muy recomendable tener un demonio syslog correctamente configurado y rotaciones de
registros en su lugar. Los registros también pueden enviarse a stdout/stderr, lo que puede ser útil
dentro de contenedores. Los archivos de configuración se analizan antes de arrancar; luego HAProxy
intenta enlazar todos los sockets de escucha y se niega a arrancar si algo falla. A partir de ese
punto ya no puede fallar. Esto significa que no hay fallos en tiempo de ejecución y que, si acepta
arrancar, funcionará hasta que se detenga.

Una vez iniciado HAProxy, hace exactamente 3 cosas:

- procesar las conexiones entrantes;

- comprobar periódicamente el estado de los servidores (conocido como comprobaciones de estado);

- intercambiar información con otros nodos haproxy.

El procesamiento de las conexiones entrantes es, con diferencia, la tarea más compleja, pues
depende de muchas posibilidades de configuración, pero puede resumirse en los 9 pasos siguientes:

- aceptar las conexiones entrantes de los sockets de escucha que pertenecen a una entidad de
  configuración conocida como «frontend», que referencia una o varias direcciones de escucha;

- aplicar a estas conexiones las reglas de procesamiento específicas del frontend, que pueden
  resultar en bloquearlas, modificar algunas cabeceras o interceptarlas para ejecutar algunos
  applets internos como la página de estadísticas o la CLI;

- pasar estas conexiones entrantes a otra entidad de configuración que representa una granja de
  servidores conocida como «backend», que contiene la lista de servidores y la estrategia de
  balanceo de carga para dicha granja de servidores;

- aplicar a estas conexiones las reglas de procesamiento específicas del backend;

- decidir a qué servidor reenviar la conexión según la estrategia de balanceo de carga;

- aplicar a los datos de respuesta las reglas de procesamiento específicas del backend;

- aplicar a los datos de respuesta las reglas de procesamiento específicas del frontend;

- emitir un registro que informe de lo ocurrido con todo detalle;

- en HTTP, volver al segundo paso para esperar una nueva solicitud; en caso contrario, cerrar la
  conexión.

Los frontends y los backends a veces se consideran semi-proxies, ya que solo ven un lado de una
conexión de extremo a extremo; al frontend solo le importan los clientes, mientras que al backend
solo le importan los servidores. HAProxy también soporta proxies completos, que son exactamente la
unión de un frontend y un backend. Cuando se desea procesamiento HTTP, la configuración
generalmente se dividirá en frontends y backends, ya que abren muchas posibilidades porque
cualquier frontend puede pasar una conexión a cualquier backend. Con proxies solo TCP, usar
frontends y backends rara vez aporta un beneficio y la configuración puede resultar más legible
con proxies completos.
