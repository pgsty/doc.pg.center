---
title: Установка
weight: 1150
description: Инструкции по установке etcd из готовых бинарных файлов или исходного кода.
icon: fa-solid fa-download
categories: [Задача]
search_keywords: [v3.7.3, "Go 1.26.10"]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## Требования {#requirements}

Перед установкой etcd ознакомьтесь со следующими страницами:

- [Поддерживаемые платформы][Supported platforms]
- [Рекомендации по оборудованию][Hardware recommendations]

## Установка готовых бинарных файлов {#install-pre-built-binaries}

Проще всего установить etcd из готовых бинарных файлов:

 1. Загрузите с [Releases][releases] сжатый архив для своей платформы,
    выбрав выпуск [v3.7.3][tagged-release] или новее.
 2. Распакуйте архив. В результате появится каталог с бинарными файлами.
 3. Добавьте исполняемые файлы в путь поиска. Например, переименуйте и/или переместите
    их в каталог из пути поиска, такой как `/usr/local/bin`, либо добавьте в путь
    каталог, созданный на предыдущем шаге.
 4. В оболочке проверьте, что `etcd` доступен в пути поиска:

    ```sh
    $ etcd --version
    etcd Version: 3.7.3
    ...
    ```

## Сборка из исходного кода {#build-from-source}

Для etcd v3.7.3 используйте [Go версии 1.26+][go]; в выпуске закреплена [версия инструментария Go 1.26.10][go-toolchain].
Соберите etcd из исходного кода следующим образом:

 1. [Загрузите репозиторий etcd в виде zip-файла][download] и распакуйте его либо
    клонируйте репозиторий следующей командой.

    ```sh
    $ git clone -b v3.7.3 https://github.com/etcd-io/etcd.git
    ```
    Чтобы собрать `main@HEAD`, не указывайте флаг `-b v3.7.3`.

 2. Перейдите в каталог:

    ```sh
    $ cd etcd
    ```
 3. Запустите скрипт сборки:

    ```sh
    $ ./scripts/build.sh
    ```

    Бинарные файлы находятся в каталоге `bin`.

 4. Добавьте полный путь к каталогу `bin` в путь поиска, например:

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. Проверьте, что `etcd` доступен в пути поиска:

    ```sh
    $ etcd --version
    ```

## Установка из пакетов ОС {#installation-via-os-packages}

*Отказ от ответственности: пакеты etcd из менеджеров пакетов ОС могут содержать устаревшие версии, поскольку они не обслуживаются автоматически и официально не поддерживаются проектом etcd. Используйте их с осторожностью.*

Способы установки etcd зависят от операционной системы. Ниже приведено несколько примеров.

### MacOS (Homebrew) {#macos-homebrew}

1. Обновите Homebrew:
```sh
$ brew update
```

2. Установите etcd:
```sh
$ brew install etcd
```

3. Проверьте установку:
```sh
$ etcd --version
```

## Linux {#linux}

etcd можно установить из официальных репозиториев и менеджеров пакетов многих крупных дистрибутивов Linux, однако опубликованные там версии могут значительно устареть. Поэтому этот способ настоятельно не рекомендуется.

Рекомендуется устанавливать etcd в Linux из [готовых бинарных файлов](#install-pre-built-binaries) или с помощью Homebrew.

### Homebrew в Linux {#homebrew-on-linux}

[Homebrew работает в Linux][Homebrew can run on Linux] и предоставляет свежие версии программ.

- Предварительные условия
  - Обновите Homebrew:

    ```sh
    $ brew update
    ```

- Процедура
  - Установите пакет с помощью `brew`:

    ```sh
    $ brew install etcd
    ```

- Результат
  - Проверьте установленную версию:

    ```sh
    $ etcd --version
    etcd Version: 3.7.3
    ...
    ```

    Вывод выше приведён как пример. Homebrew может предоставлять другую патч-версию; проверьте установленную версию командой `etcd --version`.

## Docker {#docker}

Основным реестром контейнеров etcd служит [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd),
а вторичным — [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd).

Чтобы запустить etcd в Docker:

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

## Установка в составе Kubernetes {#installation-as-part-of-kubernetes-installation}

- [Запуск etcd как Kubernetes StatefulSet][Running etcd as a Kubernetes StatefulSet]

## Проверка установки {#installation-check}

Более полная базовая проверка установки приведена в разделе
[Быстрый старт][Quickstart].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.3.zip
[go]: https://golang.org/doc/install
[go-toolchain]: https://github.com/etcd-io/etcd/blob/0a173d0410a96d01091b484daae81365bbcde57e/go.mod
[Hardware recommendations]: /ru/etcd/op-guide/hardware/
[Quickstart]: /ru/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /ru/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.3
[Supported platforms]: /ru/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
