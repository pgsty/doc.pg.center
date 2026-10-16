---
title: Cómo realizar múltiples escrituras en una transacción
description: Guía para realizar escrituras transaccionales
weight: 500
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
---

## Requisitos previos {#prerequisites}

* Instala [`etcd` y `etcdctl`](/es/etcd/install/).
* Un clúster `etcd` en ejecución.

## Terminología {#terminology}

A continuación se definen algunos términos clave utilizados en el [Ejemplo](#example) que figura más abajo.

| Términos | Definición |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | La herramienta de línea de comandos para interactuar con el servidor etcd. |
| comando [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options) | El comando `txn` es una abreviatura de «transaction» (transacción). Lee múltiples solicitudes etcd desde la entrada estándar y las aplica como una única transacción atómica. Una transacción consiste en una lista de condiciones, una lista de solicitudes que se aplican si todas las condiciones son verdaderas y una lista de solicitudes que se aplican si alguna condición es falsa. Consulta los [comandos de clave-valor de etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands) para más información.|
| `compare` | La cláusula `compare` dentro de una transacción (`txn`) actúa como una comprobación condicional que determina si las operaciones de la transacción deben ejecutarse. Garantiza que los cambios solo se apliquen si el estado actual del almacén de clave-valor coincide con las condiciones esperadas, manteniendo así la consistencia de los datos y evitando conflictos en entornos concurrentes. Para ver cómo se estructura el comando, consulta la sección [Realizar una transacción](#2-perform-a-transaction) más abajo.|

## Transacciones {#transactions}

`txn` para procesar todas las solicitudes en una sola transacción:

```bash
etcdctl txn --help
```

Las transacciones en etcd permiten ejecutar múltiples operaciones de forma atómica, garantizando que se apliquen todas o ninguna. Esto es crucial para mantener la consistencia de los datos al realizar actualizaciones relacionadas. Aprende más sobre las transacciones en [la documentación de la API](/es/etcd/learning/api/#transaction).

### Ejemplo {#example}

Considera un escenario en el que deseas actualizar el correo electrónico y el número de teléfono de un usuario en una sola transacción. Esto garantiza que ambas actualizaciones se apliquen juntas.

![05_etcdctl_transaction_2024101213](/etcd/tasks/img/transactional-write.gif)

#### 0. Variables y flags utilizados {#0-variables-and-flags-used}

| Variables |
| :--- |
| `/users/{<user_id>/email` : clave etcd que representa la dirección de correo electrónico de un usuario.|
| `/users/<user_id>/phone` : clave etcd que representa el número de teléfono de un usuario.|
| **Flags** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3) : flag que permite introducir manualmente los datos de la transacción|

#### 1. Configurar los datos iniciales {#1-set-up-initial-data}

Primero, crea un usuario con algunos datos iniciales.

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. Realizar una transacción {#2-perform-a-transaction}

Actualiza el correo electrónico y el número de teléfono del usuario en una sola transacción.

   ```shell
   etcdctl txn --interactive

   compares:
   value("/users/12345/email") = "old.address@johndoe.com"

   success requests (get, put, delete):
   put /users/12345/email "new.address@johndoe.com"
   put /users/12345/phone "098-765-4321"

   failure requests (get, put, delete):
   get /users/12345/email
   ```

* **Comparación**: Comprueba si el correo electrónico actual es «<old.address@johndoe.com>». Esto garantiza que la transacción solo prosiga si los datos son los esperados.
* **Éxito**: Si la comparación es verdadera, actualiza tanto el correo electrónico como el número de teléfono.
* **Fallo**: Si la comparación falla, recupera el correo electrónico actual para entender por qué la transacción no se llevó a cabo.

### Consideraciones importantes {#important-considerations}

* **Atomicidad**: La transacción garantiza que el correo electrónico y el número de teléfono se actualicen juntos. Si la condición inicial (la comparación) no se cumple, no se aplica ninguna de las dos actualizaciones.
* **Consistencia**: El uso de transacciones mantiene la consistencia de los datos, especialmente cuando se realizan múltiples actualizaciones relacionadas.
* **Evitar múltiples operaciones put sobre la misma clave**: No escribas múltiples valores para la misma clave dentro de una sola transacción, ya que esto puede dar lugar a resultados inesperados. Cada clave debe actualizarse solo una vez por transacción.
