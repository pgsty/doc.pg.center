---
title: Modelo de datos
weight: 2125
description: Metodologías de almacenamiento de datos de etcd
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/data_model.md"
---

etcd está diseñado para almacenar de forma fiable datos que se actualizan con poca frecuencia y para proporcionar consultas de observación fiables. etcd expone las versiones anteriores de los pares clave-valor para admitir instantáneas poco costosas y eventos del historial de observación («consultas de viaje en el tiempo»). Un modelo de datos persistente, multiversión y con control de concurrencia se adapta bien a estos casos de uso.

etcd almacena los datos en un almacén clave-valor multiversión [persistente][persistent-ds]. El almacén clave-valor persistente conserva la versión anterior de un par clave-valor cuando su valor queda sustituido por datos nuevos. El almacén clave-valor es efectivamente inmutable; sus operaciones no actualizan la estructura in situ, sino que siempre generan una nueva estructura actualizada. Todas las versiones pasadas de las claves siguen siendo accesibles y observables después de una modificación. Para evitar que el almacén de datos crezca indefinidamente con el tiempo y que mantenga versiones antiguas, el almacén puede compactarse para descartar las versiones más antiguas de los datos sustituidos.

### Vista lógica {#logical-view}

La vista lógica del almacén es un espacio de claves binario y plano. El espacio de claves dispone de un índice ordenado léxicamente sobre las claves de cadenas de bytes, de modo que las consultas por rango resultan poco costosas.

El espacio de claves mantiene múltiples **revisiones**. Cuando se crea el almacén, la revisión inicial es 1. Cada operación mutativa atómica (por ejemplo, una operación de transacción puede contener varias operaciones) crea una nueva revisión en el espacio de claves. Todos los datos retenidos por las revisiones anteriores permanecen sin cambios. Las versiones antiguas de una clave todavía pueden consultarse a través de las revisiones anteriores. Asimismo, las revisiones también están indexadas; recorrer las revisiones con observadores es eficiente. Si el almacén se compacta para ahorrar espacio, las revisiones anteriores a la revisión de compactación se eliminarán. Las revisiones aumentan de forma monótona durante toda la vida útil de un clúster.

La vida de una clave abarca una generación, desde su creación hasta su eliminación. Cada clave puede tener una o varias generaciones. La creación de una clave incrementa la **versión** de esa clave, comenzando en 1 si la clave no existe en la revisión actual. La eliminación de una clave genera un marcador de eliminación (tombstone) que concluye la generación actual de la clave al restablecer su versión a 0. Cada modificación de una clave incrementa su versión; por lo tanto, las versiones aumentan de forma monótona dentro de la generación de una clave. Una vez que se produce una compactación, toda generación finalizada antes de la revisión de compactación se eliminará, y también se eliminarán los valores establecidos antes de la revisión de compactación, excepto el más reciente.

### Vista física {#physical-view}

etcd almacena los datos físicos como pares clave-valor en un [b+tree][b+tree] persistente. Cada revisión del estado del almacén contiene únicamente el delta respecto de su revisión anterior, por eficiencia. Una sola revisión puede corresponder a varias claves del árbol.

La clave de un par clave-valor es una tupla de tres elementos (major, sub, type). Major es la revisión del almacén que contiene la clave. Sub diferencia entre las claves dentro de una misma revisión. Type es un sufijo opcional para valores especiales (por ejemplo, `t` si el valor contiene un marcador de eliminación). El valor del par clave-valor contiene la modificación respecto de la revisión anterior; es decir, un delta respecto de la revisión anterior. El b+tree está ordenado por clave en orden léxico de bytes. Las búsquedas por rango sobre los deltas de revisión son rápidas; esto permite encontrar rápidamente las modificaciones desde una revisión específica hasta otra. La compactación elimina los pares clave-valor obsoletos.

etcd también mantiene un índice [btree][btree] secundario en memoria para acelerar las consultas por rango sobre las claves. Las claves del índice btree son las claves del almacén expuestas al usuario. El valor es un puntero a la modificación del b+tree persistente. La compactación elimina los punteros muertos.

En conjunto, etcd obtiene la información de la revisión del btree y luego usa la revisión como clave para recuperar el valor del b+tree (como se muestra a continuación).
<p align="center">
  ![Modelo de datos MVCC](/etcd/learning/img/data-model-figure-01.png)
</p>

[b+tree]: https://en.wikipedia.org/wiki/B%2B_tree
[btree]: https://en.wikipedia.org/wiki/B-tree
[persistent-ds]: https://en.wikipedia.org/wiki/Persistent_data_structure
