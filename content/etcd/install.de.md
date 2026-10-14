---
title: "Installation"
weight: 1150
description: "Anleitung zur Installation von etcd aus vorkompilierten Binärdateien oder aus dem Quellcode."
icon: fa-solid fa-download
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## Voraussetzungen {#requirements}

Vor der Installation von etcd die folgenden Seiten lesen:

- [Unterstützte Plattformen][Supported platforms]
- [Hardwareempfehlungen][Hardware recommendations]

## Vorkompilierte Binärdateien installieren {#install-pre-built-binaries}

Am einfachsten lässt sich etcd aus vorkompilierten Binärdateien installieren:

 1. Unter [Veröffentlichungen][Releases] die komprimierte Archivdatei für die gewünschte Plattform herunterladen.
    Dabei Version [v3.7.2][tagged-release] oder neuer wählen.
 2. Die Archivdatei entpacken. Dadurch entsteht ein Verzeichnis mit den Binärdateien.
 3. Die ausführbaren Binärdateien zum Suchpfad hinzufügen. Dazu die Binärdateien beispielsweise umbenennen und/oder in ein Verzeichnis im Suchpfad verschieben (etwa `/usr/local/bin`) oder das im vorigen Schritt erstellte Verzeichnis zum Suchpfad hinzufügen.
 4. In einer Shell prüfen, ob `etcd` im Suchpfad liegt:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

## Aus dem Quellcode bauen {#build-from-source}

Für etcd v3.7.2 [Go ab Version 1.26][go] verwenden; das Release legt die Go-Toolchain auf Version 1.26.8 fest.
Mit den folgenden Schritten lässt sich etcd aus dem Quellcode bauen:

 1. [Das etcd-Repository als ZIP-Datei herunterladen][download] und entpacken oder das Repository mit folgendem Befehl klonen.

    ```sh
    $ git clone -b v3.7.2 https://github.com/etcd-io/etcd.git
    ```
    Zum Bauen aus `main@HEAD` die Option `-b v3.7.2` weglassen.

 2. Das Verzeichnis wechseln:

    ```sh
    $ cd etcd
    ```
 3. Das Build-Skript ausführen:

    ```sh
    $ ./scripts/build.sh
    ```

    Die Binärdateien befinden sich im Verzeichnis `bin`.

 4. Den vollständigen Pfad zum Verzeichnis `bin` zum Suchpfad hinzufügen, zum Beispiel:

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. Prüfen, ob `etcd` im Suchpfad liegt:

    ```sh
    $ etcd --version
    ```

## Installation über Betriebssystempakete {#installation-via-os-packages}
*Hinweis: Bei der Installation von etcd über Paketmanager des Betriebssystems können veraltete Versionen installiert werden. Diese Pakete werden vom etcd-Projekt weder automatisch gepflegt noch offiziell unterstützt. Betriebssystempakete daher mit Vorsicht verwenden.*

Für die verschiedenen Betriebssysteme gibt es unterschiedliche Möglichkeiten, etcd zu installieren. Im Folgenden werden einige Beispiele gezeigt.

### MacOS (Homebrew) {#macos-homebrew}

1. Homebrew aktualisieren:
```sh
$ brew update
```

2. etcd installieren:
```sh
$ brew install etcd
```

3. Installation überprüfen
```sh
$ etcd --version
```

## Linux {#linux}

etcd lässt sich zwar über die offiziellen Repositories und Paketmanager vieler großer Linux-Distributionen installieren, die angebotenen Versionen können jedoch erheblich veraltet sein. Von dieser Installationsweise wird daher dringend abgeraten.

Für Linux wird die Installation aus [vorkompilierten Binärdateien](#install-pre-built-binaries) oder mit Homebrew empfohlen.

### Homebrew unter Linux {#homebrew-on-linux}

[Homebrew läuft auch unter Linux][Homebrew can run on Linux] und kann aktuelle Softwareversionen bereitstellen.

- Voraussetzungen
  - Homebrew aktualisieren:

    ```sh
    $ brew update
    ```

- Vorgehensweise
  - Mit `brew` installieren:

    ```sh
    $ brew install etcd
    ```

- Ergebnis
  - Die Installation durch Abrufen der Version überprüfen:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

    Die Ausgabe oben ist ein Beispiel. Homebrew kann eine andere Patchversion bereitstellen; die tatsächlich installierte Version mit `etcd --version` prüfen.

## Docker {#docker}

etcd verwendet [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) als primäre Container-Registry und [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) als sekundäre.

etcd mit Docker ausführen:

```sh
ETCD_VER=v3.7.2

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

## Installation im Rahmen einer Kubernetes-Installation {#installation-as-part-of-kubernetes-installation}

- [etcd als Kubernetes-StatefulSet ausführen][Running etcd as a Kubernetes StatefulSet]

## Installation überprüfen {#installation-check}

Eine etwas ausführlichere Funktionsprüfung der Installation bietet der [Schnellstart][Quickstart].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.2.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /de/etcd/op-guide/hardware/
[Quickstart]: /de/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /de/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.2
[Supported platforms]: /de/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
