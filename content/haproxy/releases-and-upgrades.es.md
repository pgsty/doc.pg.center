---
title: "Versiones, paquetes y actualizaciones"
linkTitle: "Versiones y actualizaciones"
weight: 80
description: "Ramas estables, fuentes de versiones, identificación de versiones, mantenimiento y actualizaciones"
icon: fa-solid fa-code-branch
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/intro/releases-and-upgrades/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 3.7"
---

HAProxy es un proyecto de código abierto cubierto por la licencia GPLv2, lo que significa que cualquiera
está autorizado a redistribuirlo siempre que también se proporcione acceso a las fuentes si así se
solicita, especialmente si se han realizado modificaciones.

HAProxy evoluciona a través de una rama de desarrollo principal llamada «master» o «mainline», de la
cual se derivan nuevas ramas una vez que el código se considera estable. Muchos sitios web ejecutan
algunas ramas de desarrollo en producción de forma voluntaria, ya sea para participar en el proyecto o
porque necesitan una función de última generación, y sus comentarios son muy valiosos para corregir
errores y juzgar la calidad y estabilidad generales de la versión en desarrollo.

Las nuevas ramas que se crean cuando el código es lo bastante estable constituyen una versión estable
y generalmente se mantienen durante varios años, de modo que no hay ninguna urgencia por migrar a una
rama más reciente aunque no estés en la última. Una vez emitida una rama estable, esta solo puede
recibir correcciones de errores y, muy raramente, actualizaciones menores de funciones cuando eso
facilita la vida de los usuarios. Todas las correcciones que entran en una rama estable provienen
necesariamente de la rama master. Esto garantiza que ninguna corrección se pierda tras una
actualización. Por esta razón, si corriges un error, prepara el parche tomando como base la rama master, no sobre
la rama estable. Incluso podrías descubrir que ya estaba corregido. Este proceso también garantiza
que las regresiones en una rama estable son extremadamente raras, de modo que nunca hay excusa para
no actualizar a la última versión de tu rama actual.

Las ramas se numeran con dos dígitos separados por un punto, como «1.6». Desde la versión 1.9, las
ramas con un segundo dígito impar se centran sobre todo en actualizaciones técnicas sensibles y van
más dirigidas a los usuarios avanzados, porque es probable que provoquen más errores que las otras.
Solo se mantienen durante aproximadamente un año y no deben desplegarse donde no puedan revertirse en
caso de emergencia. Una versión completa incluye uno o dos números de subversión que indican el nivel
de corrección. Por ejemplo, la versión 1.5.14 es la 14.ª versión de corrección de la rama 1.5 después
de que se emitiera la versión 1.5.0. Contiene 126 correcciones de errores individuales, 24
actualizaciones de la documentación y otros 75 parches retroportados, la mayoría de los cuales eran
necesarios para corregir los 126 errores antes mencionados. Una función existente nunca puede
modificarse ni eliminarse en una rama estable, con el fin de garantizar que las actualizaciones dentro
de la misma rama sean siempre inofensivas.

HAProxy está disponible desde múltiples fuentes, con ritmos de publicación distintos:

- El sitio web oficial de la comunidad: <http://www.haproxy.org/>: este sitio proporciona las fuentes
  de la última versión de desarrollo, de todas las versiones estables, así como instantáneas nocturnas
  de cada rama. El ciclo de publicación no es rápido: varios meses entre versiones estables, o entre
  instantáneas de desarrollo. Las versiones muy antiguas siguen estando soportadas allí. Todo se
  proporciona únicamente en forma de fuentes, de modo que cualquier cosa que provenga de allí debe
  recompilarse y/o reempaquetarse;

- GitHub: <https://github.com/haproxy/haproxy/>: este es el espejo solo de la rama de desarrollo, que
  proporciona integración con el seguimiento de incidencias, herramientas de integración continua y
  de cobertura de código. Es exclusivamente para contribuidores;

- Diversos sistemas operativos, como las distribuciones Linux y los ports de BSD. Estos sistemas
  generalmente proporcionan versiones mantenidas a largo plazo que no siempre contienen todas las
  correcciones de las versiones oficiales, pero que al menos incluyen las correcciones críticas.
  Suele ser una buena opción para la mayoría de los usuarios que no buscan configuraciones avanzadas
  y solo quieren que las actualizaciones sean sencillas;

- Versiones comerciales de <http://www.haproxy.com/>: son paquetes profesionales con soporte,
  construidos para diversos sistemas operativos o proporcionados como appliances, basados en las
  últimas versiones estables e incluyendo una serie de funciones retroportadas de la próxima versión
  por las que existe una fuerte demanda. Es la mejor opción para los usuarios que buscan las últimas
  funciones con la fiabilidad de una rama estable, el tiempo de respuesta más rápido para corregir
  errores, o simplemente contratos de soporte sobre un producto de código abierto;

Para asegurarte de que la versión que utilizas es la más reciente de tu rama, debes proceder de la
siguiente manera:

- verifica qué ejecutable de HAProxy estás ejecutando: algunos sistemas lo incluyen por defecto y los
  administradores instalan sus versiones en otro lugar del sistema, así que es importante verificar
  en los scripts de arranque cuál se utiliza;

- determina de qué fuente proviene tu versión de HAProxy. Para ello, generalmente basta con escribir
  «haproxy -v». Una versión de desarrollo aparecerá así, con la palabra «dev» después del número de
  rama:

```text
HAProxy version 2.4-dev18-a5357c-137 2021/05/09 - https://haproxy.org/
```

    Una versión estable aparecerá así, al igual que las versiones estables sin

modificar proporcionadas por los proveedores de sistemas operativos:

```text
HAProxy version 1.5.14 2015/07/02
```

    Y una instantánea nocturna de una versión estable aparecerá así, con una
    secuencia hexadecimal después de la versión y con la fecha de la instantánea

en lugar de la fecha de la versión:

```text
HAProxy version 1.5.14-e4766ba 2015/07/29
```

    Cualquier otro formato puede indicar un paquete específico del sistema con su propio
    conjunto de parches. Por ejemplo, las versiones de HAProxy Enterprise aparecerán con el

siguiente formato (`<branch>`-`<latest commit>`-`<revision>`):

```text
HAProxy version 1.5.0-994126-357 2015/07/02
```

    Ten en cuenta que, históricamente, las versiones anteriores a la 2.4 informaban del
    nombre del proceso con un guion entre «HA» y «Proxy», incluidas las anteriores, que
    se ajustaron solo para mostrar el formato correcto; es mejor ignorar esa palabra o
    usar una coincidencia flexible en los scripts. Además, las versiones modernas añaden
    una URL que enlaza con la página del proyecto.

    Finalmente, las versiones 2.1 y superiores incluirán una línea «Status» que indicará
    si la versión es segura para producción o no y, en caso afirmativo, hasta cuándo, así
    como un enlace a la lista de errores conocidos que afectan a esa versión.

- para los paquetes específicos de un sistema, debes comprobar con el repositorio de paquetes de tu
  proveedor o con tu sistema de actualización para asegurarte de que tu sistema sigue estando
  soportado y de que todavía se proporcionan correcciones para tu rama. Para las versiones de la
  comunidad procedentes de haproxy.org, basta con visitar el sitio, verificar el estado de tu rama y
  comparar la última versión con la tuya para ver si estás en la más reciente. Si no, puedes
  actualizar. Si tu rama ya no se mantiene, sin duda vas muy retrasado y tendrás que considerar la
  actualización a una rama más reciente (lee el README con atención al hacerlo).

HAProxy tendrá que actualizarse según la fuente de la que provenga. Normalmente esto sigue el método
del proveedor del sistema para actualizar un paquete. Si se obtuvo a partir de las fuentes, lee el
archivo README del directorio de las fuentes después de extraerlas y sigue las instrucciones para tu
sistema operativo.
