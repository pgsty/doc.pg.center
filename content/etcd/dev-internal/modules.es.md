---
title: Módulos de Golang
weight: 1650
description: Organización de los módulos de Golang del proyecto etcd
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/modules.md"
---

El proyecto etcd (desde la versión 3.5) está organizado en varios
[módulos de golang](https://golang.org/ref/mod) alojados en un [repositorio único](https://golang.org/ref/mod#vcs-dir).

![gráfico de módulos](/etcd/dev-internal/img/modules.svg)

Existen los siguientes módulos:

  - **go.etcd.io/etcd/api/v3** - contiene las definiciones de la API
  (como los protos y las bibliotecas generadas a partir de protos) que definen el protocolo de comunicación
  entre los clientes y el servidor de etcd.

  - **go.etcd.io/etcd/pkg/v3** - colección de paquetes de utilidades usados por etcd
  sin ser específicos de etcd en sí mismo. Un paquete pertenece aquí
  solo si es posible que en el futuro se traslade a su propio repositorio.
  Evita añadir aquí código que tenga muchas dependencias propias, ya que
  se convierten automáticamente en dependencias de la biblioteca cliente
  (que queremos mantener ligera).

  - **go.etcd.io/etcd/client/v3** - biblioteca cliente usada para contactar con etcd a través de
  la red (grpc). Recomendada para todo uso nuevo de etcd.

  - **go.etcd.io/etcd/client/v2** - biblioteca cliente heredada usada para contactar con etcd
  a través del protocolo HTTP. Obsoleta. Todo uso nuevo debería depender de la biblioteca /v3.

  - **go.etcd.io/etcd/raft/v3** - implementación del protocolo de consenso
  distribuido. No debe contener código específico de etcd.

  - **go.etcd.io/etcd/server/v3** - implementación de etcd.
  El código de este paquete es interno de etcd y no debe consumirse
  por proyectos externos. La disposición del paquete y la API pueden cambiar dentro de las versiones menores.

  - **go.etcd.io/etcd/etcdctl/v3** - una herramienta de línea de comandos para acceder a etcd y gestionarlo.

  - **go.etcd.io/etcd/tests/v3** - un módulo que contiene todas las pruebas de integración de etcd.
    Aviso: Todas las pruebas unitarias (rápidas y sin requerir dependencias entre módulos)
    deben mantenerse en los módulos locales al código sometido a prueba.

  - **go.etcd.io/bbolt** - implementación de un árbol B persistente.
    Alojado en un repositorio separado: https://github.com/etcd-io/bbolt.


### Operaciones {#operations}

1. Todos los módulos de etcd deben publicarse en las mismas versiones; por ejemplo,
   `go.etcd.io/etcd/client/v3@v3.5.10` debe depender de `go.etcd.io/etcd/api/v3@v3.5.10`.

   La actualización coherente de las versiones se puede realizar mediante:
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. Los módulos publicados deben etiquetarse según las reglas de https://golang.org/ref/mod#vcs-version,
   es decir, cada módulo debe recibir su propia etiqueta.
   El etiquetado se puede realizar mediante:
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. Todos los módulos de etcd deben depender de las mismas versiones de las dependencias subyacentes.
   Esto se puede comprobar mediante:
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. Los archivos go.mod no deben contener dependencias sin usar y deben
   ajustarse al formato de `go mod tidy`.
   Esto lo verifica:
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. Para desencadenar acciones en todos los módulos (por ejemplo, formatear automáticamente todos los archivos),
   usa/amplía el siguiente script:
   ```shell script
   % ./scripts/fix.sh
   ```

### Futuro {#future}

Como estrella guía, nos gustaría encaminar los módulos de etcd hacia el siguiente modelo:

![gráfico de módulos](/etcd/dev-internal/img/modules-future.svg)

Esto supone:
  - Separar etcdmigrate/etcdadm del binario etcdctl.
    Gracias a esto, etcdctl se convertiría claramente en un envoltorio de línea de comandos
    en torno a la API de cliente de red,
    mientras que etcdmigrate/etcdadm admitiría operaciones físicas directas sobre los
    archivos de almacenamiento de etcd.
  - Separar etcd-proxy del binario ./etcd, ya que contiene código más experimental
    y por lo tanto conlleva riesgos y dependencias adicionales.
  - Obsolescencia del soporte del protocolo v2.
