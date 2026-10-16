---
title: "Dimensionamiento y rendimiento"
linkTitle: "Dimensionamiento"
weight: 70
description: "Principios de planificación de capacidad, órdenes de magnitud del rendimiento y reglas prácticas"
icon: fa-solid fa-gauge-high
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/intro/sizing/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3.6"
---

Las cifras típicas de uso de CPU muestran un 15% del tiempo de procesamiento invertido en HAProxy
frente a un 85% en el kernel en modo TCP o HTTP con cierre de conexión, y alrededor de un 30% para HAProxy frente a
un 70% para el kernel en modo HTTP keep-alive. Esto significa que el sistema operativo y su ajuste
tienen un fuerte impacto en el rendimiento global.

Los usos varían mucho de unos usuarios a otros: algunos se centran en el ancho de banda, otros en el
ritmo de solicitudes, otros en la concurrencia de conexiones y otros en el rendimiento SSL. Esta
sección tiene como objetivo aportar algunos elementos que ayuden con esta tarea.

Es importante tener presente que cada operación tiene un coste, de modo que cada operación individual
añade su sobrecarga sobre las demás, lo que puede resultar insignificante en ciertas circunstancias y
llegar a dominar en otros casos.

Al procesar las solicitudes de una conexión, podemos decir que:

- reenviar datos cuesta menos que analizar encabezados de solicitud o de respuesta;

- analizar encabezados de solicitud o de respuesta cuesta menos que establecer y luego cerrar una
  conexión con un servidor;

- establecer y cerrar una conexión cuesta menos que una operación de reanudación TLS;

- una operación de reanudación TLS cuesta menos que un saludo TLS completo con cálculo de clave;

- una conexión inactiva consume menos CPU que una conexión cuyos búferes contienen datos;

- un contexto TLS consume aún más memoria que una conexión con datos;

Así pues, en la práctica resulta más barato procesar bytes de carga útil que bytes de encabezado, por
lo que es más fácil alcanzar un ancho de banda de red alto con objetos grandes (pocas solicitudes por
unidad de volumen) que con objetos pequeños (muchas solicitudes por unidad de volumen). Esto explica
por qué el ancho de banda máximo siempre se mide con objetos grandes, mientras que el ritmo de
solicitudes o de conexiones se mide con objetos pequeños.

Algunas operaciones escalan bien en varios procesos repartidos entre varias CPU, y otras no escalan
igual de bien. El ancho de banda de red no escala muy lejos porque la CPU rara vez es el cuello de
botella para los objetos grandes: este está sobre todo en el ancho de banda de red y en los buses de
datos para llegar a las interfaces de red. El ritmo de conexiones no escala bien en varios
procesadores debido a algunos bloqueos del sistema al gestionar la tabla de puertos locales. El ritmo
de solicitudes sobre conexiones persistentes escala muy bien, ya que no implica mucha memoria ni
ancho de banda de red y no requiere acceder a estructuras bloqueadas. El cálculo de claves TLS escala
muy bien porque es totalmente limitado por la CPU. La reanudación TLS escala moderadamente bien, pero
alcanza sus límites en torno a los 4 procesos, donde la sobrecarga de acceder a la tabla compartida
compensa las pequeñas ganancias esperadas de más potencia.

Las cifras de rendimiento que pueden esperarse de un sistema muy bien ajustado se encuentran en el
siguiente rango. Es importante tomarlas como órdenes de magnitud y esperar variaciones significativas
en cualquier dirección en función del procesador, la configuración de las IRQ, el tipo de memoria, el
tipo de interfaz de red, el ajuste del sistema operativo, etcétera.

Las siguientes cifras se obtuvieron en un Core i7 funcionando a 3.7 GHz, equipado con NICs de doble
puerto de 10 Gbps, ejecutando el kernel Linux 3.10, HAProxy 1.6 y OpenSSL 1.0.2. HAProxy se ejecutaba
como un único proceso en un único núcleo de CPU dedicado, y dos núcleos adicionales se dedicaron a las
interrupciones de red:

- 20 Gbps de ancho de banda de red máximo en texto claro para objetos de 256 kB o mayores, 10 Gbps
  para 41kB o más;

- 4.6 Gbps de tráfico TLS usando el cifrado AES256-GCM con objetos grandes;

- 83000 conexiones TCP por segundo del cliente al servidor;

- 82000 conexiones HTTP por segundo del cliente al servidor;

- 97000 solicitudes HTTP por segundo en modo server-close (keep-alive con el cliente, cierre con el
  servidor);

- 243000 solicitudes HTTP por segundo en modo keep-alive extremo a extremo;

- 300000 conexiones TCP filtradas por segundo (anti-DDoS)

- 160000 solicitudes HTTPS por segundo en modo keep-alive sobre conexiones TLS persistentes;

- 13100 solicitudes HTTPS por segundo usando conexiones TLS reanudadas;

- 1300 conexiones HTTPS por segundo usando conexiones TLS renegociadas con RSA2048;

- 20000 conexiones simultáneas saturadas por GB de RAM, incluida la memoria necesaria para los
  búferes del sistema; es posible hacerlo mejor con un ajuste cuidadoso, pero este resultado es fácil
  de alcanzar.

- alrededor de 8000 conexiones TLS simultáneas (solo del lado del cliente) por GB de RAM, incluida la
  memoria necesaria para los búferes del sistema;

- alrededor de 5000 conexiones TLS simultáneas extremo a extremo (por ambos lados) por GB de RAM,
  incluida la memoria necesaria para los búferes del sistema;

Una prueba de rendimiento más reciente, con HAProxy 2.4 con multihilo habilitado en un procesador ARM
Graviton2 de 64 núcleos en AWS, alcanzó los 2 millones de solicitudes HTTPS por segundo con un tiempo
de respuesta inferior al milisegundo, y 100 Gbps de tráfico:

```text
https://www.haproxy.com/blog/haproxy-forwards-over-2-million-http-requests-per-second-on-a-single-aws-arm-instance/
```

Así pues, una buena regla práctica que conviene recordar es que el ritmo de solicitudes se divide por
10 entre el keep-alive TLS y la reanudación TLS, y entre la reanudación TLS y la renegociación TLS,
mientras que solo se divide por 3 entre el keep-alive HTTP y el cierre HTTP. Otra buena regla práctica
es recordar que un núcleo de alta frecuencia con instrucciones AES puede procesar alrededor de 20 Gbps
de AES-GCM por núcleo.

Otra buena regla práctica es considerar que, en el mismo servidor, HAProxy podrá saturar:

- alrededor de 5-10 servidores de archivos estáticos o proxies de caché;

- alrededor de 100 proxies antivirus;

- y alrededor de 100-1000 servidores de aplicaciones, según la tecnología utilizada.
