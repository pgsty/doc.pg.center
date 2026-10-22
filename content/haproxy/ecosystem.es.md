---
title: "Productos complementarios y alternativas"
linkTitle: "Ecosistema"
weight: 90
description: "Cómo se relaciona HAProxy con Apache, NGINX, Varnish, LVS, Envoy y otros balanceadores de carga"
icon: fa-solid fa-puzzle-piece
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/intro/ecosystem/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 4–4.4"
---

HAProxy se integra bastante bien con ciertos de los productos enumerados a continuación, razón por la
cual se mencionan aquí aunque no estén directamente relacionados con HAProxy.

## 4.1. Servidor HTTP Apache {#section-4-1}

Apache es el servidor HTTP de facto. Se trata de un proyecto muy completo y modular que admite tanto
el servicio de archivos como los contenidos dinámicos. Puede actuar como frontend para algunos
servidores de aplicaciones. Incluso puede hacer de proxy de las solicitudes y almacenar en caché las
respuestas. En todos estos casos de uso, habitualmente se necesita un balanceador de carga frontal.
Apache puede funcionar en diversos modos, algunos más pesados que otros. Ciertos módulos aún requieren
el modelo pre-fork más pesado e impedirán que Apache escale bien con un número elevado de conexiones.
En este caso, HAProxy puede ser de una ayuda enorme al imponer límites de conexión por servidor con un
valor seguro, lo que acelerará significativamente el servidor y preservará sus recursos, que serán
mejor aprovechados por la aplicación.

Apache puede extraer la dirección del cliente del encabezado X-Forwarded-For utilizando la extensión
«mod_rpaf». HAProxy alimentará automáticamente este encabezado cuando se especifica «option
forwardfor» en su configuración. HAProxy también puede ofrecer una buena protección a Apache cuando
está expuesto a internet, donde resistirá mejor una amplia variedad de tipos de ataques DoS.

## 4.2. NGINX {#section-4-2}

NGINX es el segundo servidor HTTP de facto. Al igual que Apache, cubre un amplio abanico de
funcionalidades. NGINX está construido sobre un modelo similar al de HAProxy, por lo que no tiene
ningún problema para manejar decenas de miles de conexiones simultáneas. Cuando se utiliza como
pasarela hacia algunas aplicaciones (p. ej. mediante el PHP FPM incluido), a menudo puede resultar
beneficioso establecer cierta limitación de conexiones en el frontend para reducir la carga sobre la
aplicación PHP. Ahí HAProxy resultará claramente útil tanto como balanceador de carga convencional
como en su papel de regulador de tráfico para acelerar PHP descongestionándolo. Además, dado que
ambos productos consumen muy poca CPU gracias a su arquitectura basada en eventos, a menudo es fácil
instalarlos en el mismo sistema. NGINX implementa el protocolo PROXY de HAProxy, de modo que resulta
sencillo para HAProxy transmitir a NGINX la información de conexión del cliente para que la aplicación
reciba toda la información relevante. Algunos benchmarks también han mostrado que, para el servicio
de archivos estáticos de gran tamaño, implementar un hash consistente en HAProxy delante de NGINX
puede ser beneficioso al optimizar la tasa de aciertos de la caché del sistema operativo, que
básicamente queda multiplicada por el número de nodos servidores.

## 4.3. Varnish {#section-4-3}

Varnish es un proxy inverso inteligente con caché, probablemente mejor descrito como un acelerador de
aplicaciones web. Varnish no implementa SSL/TLS y quiere dedicar la totalidad de sus ciclos de CPU a
lo que mejor sabe hacer. Varnish también implementa el protocolo PROXY de HAProxy, de modo que HAProxy
puede desplegarse muy fácilmente delante de Varnish como descargador de SSL (SSL offloader), así como
en calidad de balanceador de carga, transmitiéndole toda la información relevante del cliente. Además,
Varnish admite de forma natural la descompresión desde la caché cuando un servidor ha proporcionado un
objeto comprimido, pero por sí mismo no comprime. HAProxy puede entonces utilizarse para comprimir los
datos salientes cuando los servidores backend no implementan la compresión, aunque rara vez es buena
idea comprimir en el balanceador de carga salvo que el tráfico sea bajo.

Al construir grandes granjas de caché repartidas entre varios nodos, HAProxy puede emplear el hash
consistente de URL para distribuir inteligentemente la carga entre los nodos de caché y evitar la
duplicación de caché, lo que da como resultado un tamaño total de caché igual a la suma de todos los
nodos de caché. Además, el almacenamiento en caché de objetos muy pequeños y simples durante un corto periodo de
tiempo en HAProxy puede a veces ahorrar recorridos de ida y vuelta por la red y reducir la carga de
CPU tanto en los nodos de HAProxy como en los de Varnish. Esto solo es posible si no se realiza
ningún procesamiento sobre estos objetos en Varnish (a menudo esta noción se designa con el término
«caché de favicons», gracias a la cual a veces puede evitarse un porcentaje considerable de
solicitudes inútiles en sentido descendente). Sin embargo, no actives la caché de HAProxy durante
mucho tiempo (más de unos pocos segundos) delante de cualquier otra caché, ya que eso complicaría
significativamente el diagnóstico de problemas sin proporcionar ahorros realmente significativos.

## 4.4. Alternativas {#section-4-4}

Linux Virtual Server (LVS o IPVS) es el balanceador de carga de capa 4 incluido en el núcleo Linux.
Trabaja a nivel de paquetes y gestiona TCP y UDP. En la mayoría de los casos es más un complemento que
una alternativa, ya que no dispone en absoluto de conocimiento de capa 7.

Pound es otro balanceador de carga bien conocido. Es mucho más simple y tiene muchas menos
funcionalidades que HAProxy, pero para muchas configuraciones muy básicas ambos pueden utilizarse. Su
autor siempre ha priorizado la auditabilidad del código y desea mantener reducido el conjunto de
funcionalidades. Su arquitectura basada en hilos escala peor con recuentos elevados de conexiones,
pero es un buen producto.

Pen es un balanceador de carga bastante ligero. Admite SSL y mantiene la persistencia mediante una
tabla de tamaño fijo con las direcciones IP de sus clientes. Admite un modo orientado a paquetes que
le permite soportar, hasta cierto punto, el retorno directo del servidor (direct server return) y
UDP. Está pensado para cargas pequeñas (la tabla de persistencia solo tiene 2048 entradas).

NGINX puede realizar cierto balanceo de carga hasta cierto punto, aunque claramente no es su función
principal. El tráfico de producción se utiliza para detectar fallos de los servidores, los algoritmos
de balanceo de carga son más limitados y la persistencia (stickiness) es muy limitada. Pero puede
tener sentido en algunos escenarios de despliegue sencillos donde ya está presente. Lo bueno es que,
como se integra muy bien con HAProxy, no hay ningún inconveniente en añadir HAProxy más adelante
cuando se alcancen sus límites.

Varnish también realiza cierto balanceo de carga entre sus servidores backend y sí admite
comprobaciones de estado reales. Sin embargo, no implementa la persistencia, de modo que, al igual
que con NGINX, mientras no se necesite persistencia puede ser suficiente para empezar. De forma
similar, dado que HAProxy y Varnish se integran tan bien entre sí, es fácil añadirlo más adelante al
conjunto para complementar el conjunto de funcionalidades.
