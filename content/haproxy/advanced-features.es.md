---
title: "Funciones avanzadas"
linkTitle: "Funciones avanzadas"
weight: 60
description: "Gestión en tiempo de ejecución, capacidades del sistema operativo, scripting con Lua y trazado en vivo"
icon: fa-solid fa-wand-magic-sparkles
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/intro/advanced-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 3.5–3.5.4"
---

## 3.5.1. Funciones avanzadas : Gestión {#section-3-5-1}

HAProxy está diseñado para permanecer extremadamente estable y seguro de gestionar en un entorno de
producción habitual. Se proporciona como un único archivo ejecutable que no requiere ningún proceso
de instalación. Múltiples versiones pueden coexistir fácilmente, lo que significa que es posible (y
recomendable) actualizar las instancias progresivamente, por orden de importancia, en lugar de
migrarlas todas a la vez. Los archivos de configuración se versionan con facilidad. La comprobación
de la configuración se realiza fuera de línea, de modo que no hace falta reiniciar un servicio que
podría fallar. Durante las comprobaciones de configuración pueden detectarse varios errores
avanzados (p. ej. una regla que oculta otra, o una persistencia que no funcionará) y se proponen
avisos detallados y sugerencias de configuración para corregirlos. La compatibilidad con archivos de
configuración de versiones anteriores se remonta muy atrás en el tiempo: la versión 1.5 aún soporta
por completo configuraciones escritas para las versiones 1.1 13 años antes, y la 1.6 solo dejó de
soportar palabras clave casi en desuso y obsoletas que pueden lograrse de otra manera. El mecanismo
de actualización de configuración y software es fluido y no disruptivo, ya que permite que los
procesos antiguo y nuevo coexistan en el sistema, gestionando cada uno sus propias conexiones. El
estado del sistema, las opciones de compilación y la compatibilidad de las bibliotecas se informan
al arrancar.

Algunas funciones avanzadas permiten a un administrador de aplicaciones detener un servidor de
forma progresiva, detectar cuándo ya no hay actividad en él, sacarlo de línea, detenerlo,
actualizarlo y asegurarse de que no recibe ningún tráfico mientras se actualiza, y luego
probarlo de nuevo por la ruta normal sin exponerlo al público, y todo ello sin tocar HAProxy en
absoluto. Esto garantiza que incluso operaciones de producción complicadas puedan realizarse durante
el horario de apertura con todos los recursos técnicos disponibles.

El proceso intenta ahorrar recursos en la medida de lo posible, usa agrupaciones de memoria para
ahorrar tiempo de asignación y limitar la fragmentación de la memoria, libera los búferes de carga
útil en cuanto se envía su contenido y soporta imponer límites estrictos de memoria por encima de
los cuales las conexiones deben esperar a que haya un búfer disponible en lugar de asignar más
memoria. Este sistema ayuda a garantizar el uso de memoria en entornos especialmente estrictos.

Una interfaz de línea de comandos (CLI) está disponible como socket UNIX o TCP para realizar una
serie de operaciones y obtener información para el diagnóstico de problemas. Todo lo que se hace en
este socket no requiere ningún cambio de configuración, por lo que se usa sobre todo para cambios
temporales. Mediante esta interfaz es posible cambiar la dirección, el peso y el estado de un
servidor, consultar estadísticas y limpiar contadores, volcar y limpiar tablas de persistencia,
posiblemente de forma selectiva por criterios de clave, volcar y matar conexiones del lado del
cliente y del lado del servidor, volcar los errores capturados con un análisis detallado de la causa
y ubicación exactas del error, volcar, añadir y eliminar entradas de ACL y mapas, actualizar secretos
compartidos de TLS, aplicar límites de conexión y de tasa al vuelo a frontends arbitrarios (útil en
entornos de hosting compartido) y deshabilitar un frontend concreto para liberar un puerto de
escucha (útil cuando las operaciones diurnas están prohibidas y aun así se necesita una
corrección). Actualizar certificados y su configuración al vuelo está permitido, así como habilitar
y consultar trazas de cada paso del procesamiento del tráfico.

Para entornos donde SNMP es obligatorio, existen al menos dos agentes: uno se incluye con las
fuentes de HAProxy y depende del módulo Perl de Net-SNMP. Otro se incluye con los paquetes
comerciales y no requiere Perl. Ambos son aproximadamente equivalentes en cuanto a cobertura.

A menudo se recomienda instalar 4 utilidades en la máquina donde se despliega HAProxy:

- socat (para conectarse a la CLI, aunque ciertas variantes de netcat también pueden hacerlo hasta
  cierto punto);

- halog de la última versión de HAProxy: es la herramienta de análisis de registros, analiza los
  registros nativos TCP y HTTP extremadamente rápido (1 a 2 GB por segundo) y extrae información y
  estadísticas útiles como las solicitudes por URL, por dirección de origen, URLs ordenadas por
  tiempo de respuesta o tasa de error, códigos de terminación, etc. Fue diseñado para desplegarse en
  los servidores de producción y ayudar a diagnosticar problemas en vivo, así que debe estar allí
  listo para usarse;

- tcpdump: es muy recomendable para tomar las trazas de red necesarias para diagnosticar un
  problema que se haya hecho visible en los registros. Llega un momento en que el análisis de la
  aplicación y el de haproxy divergen, y las trazas de red son la única forma de decir quién tiene
  razón y quién no. También es bastante común detectar errores en las pilas de red y en los
  hipervisores gracias a tcpdump;

- strace: es el complemento de tcpdump. Informará de lo que HAProxy ve realmente y ayudará a
  separar los problemas de los que es responsable el sistema operativo de aquellos de los que es
  responsable HAProxy. Con frecuencia se solicita strace cuando se sospecha de un error en HAProxy;

## 3.5.2. Funciones avanzadas : Capacidades específicas del sistema {#section-3-5-2}

Dependiendo del sistema operativo en que se despliegue HAProxy, puede que ciertas funciones extra
estén disponibles o sean necesarias. Aunque está soportado en varias plataformas, HAProxy se
desarrolla principalmente en Linux, lo que explica que algunas funciones solo estén disponibles en
esta plataforma.

Las funciones de bind y connect transparentes, el soporte de vincular conexiones a una interfaz de
red concreta, así como la capacidad de vincular múltiples procesos a la misma dirección IP y
puertos solo están disponibles en sistemas Linux y BSD, aunque solo Linux realiza un balanceo de
carga del lado del kernel de las solicitudes entrantes entre los procesos disponibles.

En Linux existen además varias funciones y optimizaciones extra, incluido el soporte de espacios de
nombres de red (también conocidos como «containers»), que permiten que HAProxy actúe como pasarela
entre todos los contenedores, la capacidad de establecer el MSS, las marcas de Netfilter y el campo
IP TOS en la conexión del lado del cliente, el soporte de TCP FastOpen en el lado de escucha, los
tiempos de espera de usuario de TCP para que el kernel elimine rápidamente conexiones cuando
detecta que el cliente ha desaparecido antes de los tiempos de espera configurados, el splicing de
TCP para que el kernel reenvíe datos entre los dos lados de una conexión evitando así múltiples
copias de memoria, la capacidad de habilitar la opción de bind «defer-accept» para recibir el aviso
de una conexión entrante solo cuando haya datos disponibles en los búferes del kernel, y la
capacidad de enviar la solicitud con el ACK que confirma una conexión (a veces llamado
«piggy-back»), que se habilita con la opción «tcp-smart-connect». En Linux, HAProxy además cuida
mucho la manipulación de los ACK retardados de TCP para ahorrar tantos paquetes como sea posible en
la red.

Algunos sistemas tienen un reloj poco fiable que salta hacia atrás y hacia adelante en el pasado y
en el futuro. Esto solía ocurrir con algunos sistemas NUMA donde múltiples procesadores no veían
exactamente la misma hora del día, y recientemente se ha vuelto más común en entornos
virtualizados donde el reloj virtual no tiene ninguna relación con el reloj real, lo que produce
saltos de tiempo enormes (en ocasiones se han observado de hasta 30 segundos). Esto causa muchos
problemas con la aplicación de los tiempos de espera en general. Debido a este defecto de tales
sistemas, HAProxy mantiene su propio reloj monotónico, basado en el reloj del sistema pero donde la
deriva se mide y se compensa. Esto garantiza que incluso con un reloj de sistema muy malo, los
temporizadores siguen siendo razonablemente precisos y los tiempos de espera siguen funcionando.
Ten en cuenta que este problema afecta a todo el software que se ejecute en tales sistemas y no es
específico de HAProxy. Los efectos comunes son tiempos de espera espurios o bloqueos de la
aplicación. Por tanto, si se detecta este comportamiento en un sistema, debe corregirse,
independientemente de que HAProxy se proteja frente a ello.

En Linux, un nuevo proceso en arranque puede comunicarse con el anterior para reutilizar sus
descriptores de archivo de escucha, de modo que los sockets de escucha nunca se interrumpan durante
el reemplazo del proceso.

## 3.5.3. Funciones avanzadas : Scripting {#section-3-5-3}

HAProxy puede compilarse con soporte para el lenguaje embebido Lua, lo que abre un amplio abanico
de nuevas posibilidades relacionadas con la manipulación compleja de solicitudes o respuestas, las
decisiones de enrutado, el procesamiento de estadísticas, etc. Usando Lua es incluso posible
establecer conexiones paralelas a otros servidores para intercambiar información. De esta forma se
vuelve posible (aunque complejo) desarrollar, por ejemplo, un sistema de autenticación. Consulta la
documentación del archivo «doc/lua-api/index.rst» para más información sobre cómo usar Lua.

## 3.5.4. Funciones avanzadas: Trazado {#section-3-5-4}

En cualquier momento un administrador puede conectarse por la CLI y habilitar el trazado en
diversos subsistemas internos. Por defecto se proporcionan diversos niveles de detalle, de modo que
en la práctica puede recuperarse cualquier cosa entre una línea por solicitud y 500 líneas por
solicitud. Hay filtros disponibles, así como un mecanismo automático de captura
encendido/apagado/pausa, de manera que realmente es posible esperar un determinado evento y
observarlo en detalle. Esto es extremadamente práctico para diagnosticar violaciones de protocolo de
servidores y clientes defectuosos, o ataques de denegación de servicio.
