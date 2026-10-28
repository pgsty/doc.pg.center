---
title: Instalación
weight: 1150
description: Instrucciones para instalar etcd a partir de binarios precompilados o a partir del código fuente.
icon: fa-solid fa-download
categories: [Tarea]
search_keywords: [v3.7.3, "Go 1.26.10"]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## Requisitos {#requirements}

Antes de instalar etcd, consulta las páginas siguientes:

- [Plataformas compatibles][Supported platforms]
- [Recomendaciones de hardware][Hardware recommendations]

## Instalar los binarios precompilados {#install-pre-built-binaries}

La forma más sencilla de instalar etcd es a partir de binarios precompilados:

 1. Descarga el archivo comprimido para tu plataforma desde [Releases][releases],
    eligiendo la versión [v3.7.3][tagged-release] o posterior.
 2. Descomprime el archivo. Esto da como resultado un directorio que contiene los binarios.
 3. Añade los binarios ejecutables a tu ruta. Por ejemplo, renombra y/o mueve
    los binarios a un directorio de tu ruta (como `/usr/local/bin`), o añade el
    directorio creado en el paso anterior a tu ruta.
 4. Desde un shell, comprueba que `etcd` está en tu ruta:

    ```sh
    $ etcd --version
    etcd Version: 3.7.3
    ...
    ```

## Compilar a partir del código fuente {#build-from-source}

Para etcd v3.7.3, usa [Go versión 1.26+][go]; la versión fija la [cadena de herramientas Go 1.26.10][go-toolchain].
Compila a partir del código fuente siguiendo estos pasos:

 1. [Descarga el repositorio de etcd como archivo zip][download] y descomprímelo, o clona el
    repositorio usando el siguiente comando.

    ```sh
    $ git clone -b v3.7.3 https://github.com/etcd-io/etcd.git
    ```
    Para compilar desde `main@HEAD`, omite la opción `-b v3.7.3`.

 2. Cambia de directorio:

    ```sh
    $ cd etcd
    ```
 3. Ejecuta el script de compilación:

    ```sh
    $ ./scripts/build.sh
    ```

    Los binarios están en el directorio `bin`.

 4. Añade la ruta completa del directorio `bin` a tu ruta, por ejemplo:

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. Comprueba que `etcd` está en tu ruta:

    ```sh
    $ etcd --version
    ```

## Instalación mediante paquetes del sistema operativo {#installation-via-os-packages}
*Aviso: las instalaciones de etcd mediante gestores de paquetes del sistema operativo pueden ofrecer versiones obsoletas, ya que no se mantienen automáticamente ni cuentan con soporte oficial del proyecto etcd. Por tanto, usa los paquetes del sistema operativo con precaución.*

Existen varias formas de instalar etcd en diferentes sistemas operativos, y estos son solo algunos ejemplos de cómo puede hacerse.

### macOS (Homebrew) {#macos-homebrew}

1. Actualiza Homebrew:
```sh
$ brew update
```

2. Instala etcd:
```sh
$ brew install etcd
```

3. Verifica la instalación
```sh
$ etcd --version
```

## Linux {#linux}

Aunque es posible instalar etcd mediante los repositorios oficiales y los gestores de paquetes de muchas distribuciones principales de Linux, las versiones publicadas pueden estar significativamente desactualizadas. Por ello, se desaconseja encarecidamente instalar de esta manera.

La forma recomendada de instalar etcd en Linux es mediante [binarios precompilados](#install-pre-built-binaries) o usando Homebrew.

### Homebrew en Linux {#homebrew-on-linux}

[Homebrew puede ejecutarse en Linux][Homebrew can run on Linux], y puede proporcionar versiones recientes del software.

- Requisitos previos
  - Actualiza Homebrew:

    ```sh
    $ brew update
    ```

- Procedimiento
  - Instala usando `brew`:

    ```sh
    $ brew install etcd
    ```

- Resultado
  - Verifica la instalación obteniendo la versión:

    ```sh
    $ etcd --version
    etcd Version: 3.7.3
    ...
    ```

    La salida anterior es un ejemplo. Homebrew puede proporcionar una versión de parche diferente; comprueba la versión instalada con `etcd --version`.

## Docker {#docker}

etcd usa [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) como
registro de contenedores principal, y [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) como
secundario.

Para ejecutar etcd usando Docker:

```sh
ETCD_VER=v3.7.3

rm -rf /tmp/etcd-data.tmp && mkdir -p /tmp/etcd-data.tmp && \
  docker rmi gcr.io/etcd-development/etcd:${ETCD_VER} || true && \
  docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
  --name etcd-gcr-${ETCD_VER} \
  gcr.io/etcd-development/etcd:${ETCD_VER} \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster s1=http://0.0.0.0:2380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --log-level info \
  --logger zap \
  --log-outputs stderr

docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcd --version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdutl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl endpoint health
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl put foo bar
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl get foo
```

## Instalación como parte de la instalación de Kubernetes {#installation-as-part-of-kubernetes-installation}

- [Ejecutar etcd como un StatefulSet de Kubernetes][Running etcd as a Kubernetes StatefulSet]

## Comprobación de la instalación {#installation-check}

Para una comprobación básica algo más detallada de tu instalación, consulta
el [Inicio rápido][Quickstart].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.3.zip
[go]: https://golang.org/doc/install
[go-toolchain]: https://github.com/etcd-io/etcd/blob/0a173d0410a96d01091b484daae81365bbcde57e/go.mod
[Hardware recommendations]: /es/etcd/op-guide/hardware/
[Quickstart]: /es/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /es/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.3
[Supported platforms]: /es/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
