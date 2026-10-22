---
title: "Fundamentos del balanceo de carga"
linkTitle: "Balanceo de carga"
weight: 20
description: "Fundamentos del balanceo de carga a nivel de paquete, red, servidor, L4 y L7"
icon: fa-solid fa-scale-balanced
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/intro/load-balancing/
  - /haproxy/intro/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 2"
---

Este documento es una introducción a HAProxy para todos aquellos que no lo conocen, así como para quienes
desean redescubrirlo tras conocer versiones antiguas. Su objetivo principal es proporcionar a los usuarios
todos los elementos para decidir si HAProxy es o no el producto que buscan. Los usuarios avanzados pueden
encontrar aquí algunas partes de soluciones a ideas que tenían, simplemente porque no conocían una
determinada función nueva. También se proporciona cierta información de dimensionamiento, se explica el
ciclo de vida del producto y se ofrecen comparaciones con productos parcialmente superpuestos.

Este documento no proporciona ninguna ayuda ni pista de configuración, pero explica dónde encontrar los
documentos pertinentes. La guía se presenta como una secuencia plana de páginas temáticas en la barra lateral de HAProxy.

El balanceo de carga consiste en agregar múltiples componentes para lograr una capacidad total de
procesamiento superior a la capacidad individual de cada componente, sin ninguna intervención del usuario
final y de manera escalable. El resultado es que se realizan más operaciones simultáneamente en el tiempo
que tarda un componente en realizar una sola. Una operación individual, sin embargo, seguirá realizándose en
un solo componente a la vez y no será más rápida que sin balanceo de carga. Siempre se requieren
al menos tantas operaciones como componentes disponibles y un mecanismo de balanceo de carga eficiente para
utilizar todos los componentes y beneficiarse plenamente del balanceo de carga. Un buen ejemplo de esto es
el número de carriles de una autopista, que permite que pasen tantos coches como permita el mismo
intervalo de tiempo sin aumentar su velocidad individual.

Ejemplos de balanceo de carga:

- Planificación de procesos en sistemas multiprocesador
- Balanceo de carga de enlaces (p. ej., EtherChannel, Bonding)
- Balanceo de carga de direcciones IP (p. ej., ECMP, round-robin DNS)
- Balanceo de carga de servidores (mediante balanceadores de carga)

El mecanismo o componente que realiza la operación de balanceo de carga se llama balanceador de carga. En
entornos web, estos componentes se denominan «balanceador de carga de red» y, más comúnmente, «balanceador
de carga», dado que esta actividad es, con diferencia, el caso más conocido de balanceo de carga.

Un balanceador de carga puede actuar:

- a nivel de enlace: esto se llama balanceo de carga de enlace y consiste en elegir a qué enlace de red
  enviar un paquete;

- a nivel de red: esto se llama balanceo de carga de red y consiste en elegir qué ruta seguirá una serie
  de paquetes;

- a nivel de servidor: esto se llama balanceo de carga de servidores y consiste en decidir qué servidor
  procesará una conexión o solicitud.

Existen dos tecnologías distintas que cubren necesidades diferentes, aunque con cierta superposición. En cada
caso, es importante tener en cuenta que el balanceo de carga consiste en desviar el tráfico de su flujo
natural y que hacerlo siempre requiere un mínimo de cuidado para mantener el nivel requerido de
coherencia entre todas las decisiones de enrutamiento.

La primera actúa a nivel de paquete y procesa los paquetes más o menos individualmente. Existe una
relación de 1 a 1 entre los paquetes de entrada y de salida, por lo que es posible seguir el tráfico en
ambos lados del balanceador de carga utilizando un analizador de red convencional. Esta tecnología puede ser
muy barata y extremadamente rápida. Suele implementarse en hardware (ASICs), lo que permite alcanzar la
velocidad de línea, como los conmutadores que hacen ECMP. Normalmente sin estado, también puede ser con
estado (considerar la sesión a la que pertenece un paquete, y se llama layer4-LB o L4), puede soportar DSR
(retorno directo del servidor, sin volver a pasar por el balanceador de carga) si los paquetes no fueron
modificados, pero no ofrece casi ningún conocimiento del contenido. Esta tecnología es muy adecuada para el
balanceo de carga a nivel de red, aunque a veces se utiliza para un balanceo de servidores muy básico a alta
velocidad.

La segunda actúa sobre los contenidos de las sesiones. Requiere que los flujos de entrada se reensamblen y
se procesen como un todo. Los contenidos pueden modificarse, y el flujo de salida se segmenta en nuevos
paquetes. Por este motivo, generalmente la realizan proxies y a menudo se llaman balanceadores de carga de
capa 7 o L7. Esto implica que hay dos conexiones distintas a cada lado y que no existe ninguna relación
entre los tamaños ni las cantidades de los paquetes de entrada y de salida. Los clientes y los servidores
no están obligados a usar el mismo protocolo (por ejemplo, IPv4 frente a IPv6, texto en claro frente a
SSL). Las operaciones son siempre con estado, y el tráfico de retorno debe pasar por el balanceador de
carga. El procesamiento adicional tiene un coste, por lo que no siempre es posible alcanzar la velocidad de
línea, especialmente con paquetes pequeños. Por otra parte, ofrece amplias posibilidades y generalmente se
implementa en software puro, incluso cuando está integrado en aparatos de hardware. Esta tecnología es muy
adecuada para el balanceo de carga de servidores.

Los balanceadores de carga basados en paquetes se despliegan generalmente en modo cut-through, por lo que se
instalan en la ruta normal del tráfico y lo desvían según la configuración. El tráfico de retorno no pasa
necesariamente por el balanceador de carga. Pueden aplicarse algunas modificaciones a la dirección de red
de destino para dirigir el tráfico hacia el destino correcto. En este caso, es obligatorio que el tráfico
de retorno pase por el balanceador de carga. Si las rutas no lo hacen posible, el balanceador de carga
también puede sustituir la dirección de origen de los paquetes por la suya propia para forzar que el
tráfico de retorno pase por él.

Los balanceadores de carga basados en proxy se despliegan como un servidor con sus propias direcciones IP y
puertos, sin cambios en la arquitectura. A veces esto requiere realizar algunas adaptaciones en las
aplicaciones para que los clientes se dirijan correctamente a la dirección IP del balanceador de carga y no
directamente a la del servidor. Algunos balanceadores de carga pueden tener que ajustar algunas respuestas
de los servidores para hacer esto posible (p. ej., el campo de cabecera HTTP Location utilizado en las
redirecciones HTTP). Algunos balanceadores de carga basados en proxy pueden interceptar tráfico destinado a
una dirección que no poseen y suplantar la dirección del cliente al conectarse al servidor. Esto les
permite desplegarse como si fueran un enrutador o cortafuegos convencional, en un modo cut-through muy
similar al de los balanceadores de carga basados en paquetes. Esto se aprecia especialmente en los
productos que combinan el modo de paquete y el modo proxy. En este caso, el DSR evidentemente sigue sin ser
posible y el tráfico de retorno aún debe enrutarse de vuelta hacia el balanceador de carga.

Un enfoque por capas muy escalable consistiría en tener un enrutador frontal que recibe el tráfico de
múltiples enlaces balanceados en carga y que usa ECMP para distribuir este tráfico a una primera capa de
múltiples balanceadores de carga basados en paquetes y con estado (L4). Estos balanceadores L4, a su vez,
pasan el tráfico a un número aún mayor de balanceadores de carga basados en proxy (L7), que deben analizar
los contenidos para decidir qué servidor recibirá en última instancia el tráfico.

El número de componentes y de caminos posibles para el tráfico aumenta el riesgo de fallo; en entornos muy
grandes, es incluso normal tener permanentemente algunos componentes defectuosos en reparación o
sustitución. El balanceo de carga realizado sin conocimiento del estado de salud de toda la pila degrada
significativamente la disponibilidad. Por este motivo, cualquier balanceador de carga sensato verificará que
los componentes a los que pretende entregar el tráfico siguen vivos y accesibles, y dejará de entregar
tráfico a los defectuosos. Esto puede lograrse mediante diversos métodos.

El más común consiste en enviar periódicamente sondas para asegurarse de que el componente sigue
operativo. Estas sondas se llaman «comprobaciones de estado». Deben ser representativas del tipo de fallo
que se desea abordar. Por ejemplo, una comprobación basada en ping no detectará que un servidor web se ha
detenido y ya no escucha en un puerto, mientras que una conexión al puerto lo verificará, y una solicitud
más avanzada puede incluso validar que el servidor sigue funcionando y que la base de datos de la que
depende sigue siendo accesible. Las comprobaciones de estado suelen incluir algunos reintentos para
compensar errores de medición ocasionales. El periodo entre comprobaciones debe ser lo bastante corto para
garantizar que el componente defectuoso no se utilice demasiado tiempo después de que ocurra un error.

Otros métodos consisten en muestrear el tráfico de producción enviado a un destino para observar si se
procesa correctamente o no, y expulsar los componentes que devuelven respuestas inapropiadas.
Sin embargo, esto requiere sacrificar una parte del tráfico de producción y no siempre es
aceptable. Una combinación de estos dos mecanismos ofrece lo mejor de ambos mundos, usándolos ambos para
detectar un fallo, y solo las comprobaciones de estado para detectar el fin del fallo. Un último método
implica informes centralizados: un agente de supervisión central actualiza periódicamente a todos los
balanceadores de carga sobre el estado de todos los componentes. Esto proporciona una visión global de la
infraestructura a todos los componentes, aunque a veces con menos precisión o rapidez de reacción. Es el más
adecuado para entornos con muchos balanceadores de carga y muchos servidores.

Los balanceadores de carga de capa 7 también se enfrentan a otro desafío conocido como stickiness o
persistencia. El principio es que generalmente deben dirigir múltiples solicitudes o conexiones
posteriores de un mismo origen (como un usuario final) hacia el mismo destino. El ejemplo más conocido es
el carrito de la compra de una tienda en línea. Si cada clic genera una nueva conexión, siempre debe
enviarse al usuario al servidor que conserva su carrito de la compra. El conocimiento del contenido
facilita detectar algunos elementos en la solicitud para identificar el servidor al que entregarla, pero
esto no siempre es suficiente. Por ejemplo, si se usa la dirección de origen como clave para elegir un
servidor, puede decidirse que se use un algoritmo basado en hash y que una dirección IP determinada se
envíe siempre al mismo servidor en función de una división de la dirección por el número de servidores
disponibles. Pero si un servidor falla, el resultado cambia y todos los usuarios se envían de repente a un
servidor diferente y pierden su carrito de la compra. La solución contra este problema consiste en
memorizar el destino elegido, de modo que cada vez que se vea al mismo visitante, se le dirija al mismo
servidor independientemente del número de servidores disponibles. La información puede almacenarse en la
memoria del balanceador de carga, en cuyo caso puede tener que replicarse a otros balanceadores de carga si
no está solo, o puede almacenarse en la memoria del cliente mediante diversos métodos, siempre que el
cliente pueda presentar esta información con cada solicitud (inserción de cookie, redirección a un
subdominio, etc.). Este mecanismo proporciona el beneficio adicional de no tener que depender de
información inestable o desigualmente distribuida (como la dirección IP de origen). De hecho, esta es la
razón más fuerte para adoptar un balanceador de carga de capa 7 en lugar de uno de capa 4.

Para extraer información como una cookie, un campo de cabecera Host, una URL o cualquier otra cosa, un
balanceador de carga puede necesitar descifrar el tráfico SSL/TLS e incluso, posiblemente, recifrarlo al
pasarlo al servidor. Esta costosa tarea explica por qué en algunas infraestructuras de tráfico intenso
puede haber muchos balanceadores de carga.

Dado que un balanceador de carga de capa 7 puede realizar varias operaciones complejas sobre el tráfico
(descifrar, analizar, modificar, comparar cookies, decidir a qué servidor enviarlo, etc.), puede
definitivamente causar problemas y muy comúnmente se le acusará de ser responsable de muchos problemas que
solo reveló. A menudo se descubrirá que los servidores son inestables y periódicamente suben y bajan, o
que, en el caso de los servidores web, entregan páginas con enlaces codificados de forma fija que obligan a
los clientes a conectarse directamente a un servidor específico sin pasar por el balanceador de carga, o que
tardan una eternidad en responder bajo carga elevada, provocando tiempos de espera agotados. Por eso, el
registro es un aspecto extremadamente importante del balanceo de carga de capa 7. Una vez que se informa de
un problema, es importante determinar si el balanceador de carga tomó una decisión errónea y, en tal caso,
por qué, para que no vuelva a ocurrir.
