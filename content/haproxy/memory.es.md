---
title: "6. Gestión de la memoria"
linkTitle: "6. Memoria"
weight: 300
description: "Asignación de memoria, límites, pools, búferes y dimensionamiento de procesos"
icon: fa-solid fa-memory
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/memory/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 6"
---

HAProxy utiliza una gestión de memoria basada en pools, simple y rápida. Dado que depende de un número reducido de
tipos de objetos diferentes, es mucho más eficiente tomar nuevos objetos de un pool que ya
contiene objetos del tamaño apropiado que llamar a malloc() para cada tamaño diferente. Los pools
se organizan como una pila o LIFO, de modo que los objetos recién asignados se toman de objetos
liberados recientemente que aún están calientes en las cachés de CPU. Los pools de tamaños similares se
fusionan entre sí, con el fin de limitar la fragmentación de la memoria.

Por defecto, puesto que el foco está puesto en el rendimiento, cada objeto liberado se devuelve al pool del que
provenía, y los objetos asignados nunca se liberan, ya que se espera que se reutilicen muy pronto.

En la CLI, es posible comprobar cómo se está utilizando la memoria en los pools gracias al comando
«show pools»:

```shell
> show pools
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool cache_st (16 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccc40=03 [SHARED]
  - Pool pipe (32 bytes): 5 allocated (160 bytes), 5 used, 0 failures, 2 users, @0x9ccac0=00 [SHARED]
  - Pool comp_state (48 bytes): 3 allocated (144 bytes), 3 used, 0 failures, 5 users, @0x9cccc0=04 [SHARED]
  - Pool filter (64 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 3 users, @0x9ccbc0=02 [SHARED]
  - Pool vars (80 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccb40=01 [SHARED]
  - Pool uniqueid (128 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9cd240=15 [SHARED]
  - Pool task (144 bytes): 55 allocated (7920 bytes), 55 used, 0 failures, 1 users, @0x9cd040=11 [SHARED]
  - Pool session (160 bytes): 1 allocated (160 bytes), 1 used, 0 failures, 1 users, @0x9cd140=13 [SHARED]
  - Pool h2s (208 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccec0=08 [SHARED]
  - Pool h2c (288 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cce40=07 [SHARED]
  - Pool spoe_ctx (304 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccf40=09 [SHARED]
  - Pool connection (400 bytes): 2 allocated (800 bytes), 2 used, 0 failures, 1 users, @0x9cd1c0=14 [SHARED]
  - Pool hdr_idx (416 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd340=17 [SHARED]
  - Pool dns_resolut (480 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccdc0=06 [SHARED]
  - Pool dns_answer_ (576 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccd40=05 [SHARED]
  - Pool stream (960 bytes): 1 allocated (960 bytes), 1 used, 0 failures, 1 users, @0x9cd0c0=12 [SHARED]
  - Pool requri (1024 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd2c0=16 [SHARED]
  - Pool buffer (8030 bytes): 3 allocated (24090 bytes), 2 used, 0 failures, 1 users, @0x9cd3c0=18 [SHARED]
  - Pool trash (8062 bytes): 1 allocated (8062 bytes), 1 used, 0 failures, 1 users, @0x9cd440=19
Total: 19 pools, 42296 bytes allocated, 34266 used.
```

El nombre del pool es solo indicativo: es el nombre del primer tipo de objeto que utiliza este pool. El tamaño
entre paréntesis es el tamaño de los objetos de este pool. Los tamaños de los objetos siempre se redondean
al alza hasta el múltiplo de 16 bytes más cercano. Se informa del número de objetos actualmente asignados y del número
equivalente de bytes, de modo que es fácil saber qué pool es responsable del mayor uso de
memoria. El número de objetos actualmente en uso también se informa en el campo «used». La
diferencia entre «allocated» y «used» corresponde a los objetos que han sido liberados y que están
disponibles para uso inmediato. La dirección al final de la línea es la dirección del pool, y el
número siguiente es el índice del pool cuando existe, o se muestra como -1 si no se asignó ningún índice.

Es posible limitar la cantidad de memoria asignada por proceso usando la opción de línea de comandos «-m»,
seguida de un número de megabytes. Cubre todo el espacio direccionable del proceso, por lo que incluye
la memoria utilizada por algunas bibliotecas así como la pila, pero es un límite fiable a la hora de
construir un sistema con recursos limitados. Funciona igual que «ulimit -v» en los sistemas que la
tienen, o «ulimit -d» en los demás.

Si una asignación de memoria falla porque se ha alcanzado el límite de memoria o porque el sistema no
tiene memoria suficiente, haproxy comenzará primero liberando todos los objetos disponibles de todos los pools
antes de intentar asignar memoria de nuevo. Este mecanismo de liberación de memoria no utilizada puede
activarse enviando la señal SIGQUIT al proceso de haproxy.

Durante una operación de recarga, el proceso que pasa al estado de parada ordenada también realiza
automáticamente algunos vaciados después de liberar cada conexión, de modo que toda la memoria posible se
libera para ahorrarla para el nuevo proceso.
