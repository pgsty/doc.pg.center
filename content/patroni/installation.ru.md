---
title: "Установка"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "Инструкции по установке и обновлению Patroni на поддерживаемых платформах."
module: [PATRONI]
categories: [Руководство]
aliases: [/docs/patroni/installation/]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## Предварительные требования для Mac OS {#pre-requirements-for-mac-os}

Чтобы установить необходимые компоненты на Mac, выполните:

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

Начиная с [psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/) двоичная версия psycopg2 больше не устанавливается по умолчанию. Для установки из исходного кода необходим компилятор C и пакеты разработки postgres и python. Поскольку в экосистеме Python нельзя указать зависимость как `psycopg2 OR psycopg2-binary`, способ установки нужно выбрать самостоятельно.

Доступны следующие варианты:

1.  Использовать диспетчер пакетов дистрибутива

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2.  При установке Patroni через pip указать `psycopg`, `psycopg2` или `psycopg2-binary` в [списке зависимостей](/ru/patroni/installation#extras).

<a id="extras"></a>

--------

## Общая установка через pip {#general-installation-for-pip}

Patroni можно установить с помощью pip:

```bash
pip install patroni[dependencies]
```

где `dependencies` может быть пустым либо содержать один или несколько следующих вариантов:

etcd или etcd3  
модуль `python-etcd` для использования Etcd как распределённого хранилища конфигурации (DCS)

consul  
модуль `py-consul` для использования Consul как DCS

zookeeper  
модуль `kazoo` для использования Zookeeper как DCS

exhibitor  
модуль `kazoo` для использования Exhibitor как DCS (зависимости те же, что и для Zookeeper)

kubernetes  
модуль [kubernetes](/ru/patroni/kubernetes#kubernetes) для использования Kubernetes как DCS в Patroni

raft  
модуль `pysyncobj` для использования реализации Raft на Python как DCS

aws  
`boto3` для использования обратных вызовов AWS

jsonlogger  
модуль `python-json-logger` для включения [ведения журнала](/ru/patroni/config/yaml#log_settings) в формате json

systemd  
`systemd-python` для интеграции с sd_notify

all  
всё перечисленное выше, кроме семейства psycopg

psycopg3  
модуль `psycopg\[binary\]\>=3.0.0`

psycopg2  
модуль `psycopg2\>=2.5.4`

psycopg2-binary  
модуль `psycopg2-binary`

Например, для установки Patroni вместе с psycopg3, зависимостями Etcd как DCS и обратными вызовами AWS выполните:

```bash
pip install patroni[psycopg3,etcd3,aws]
```

Обратите внимание: внешние инструменты, вызываемые в сценариях создания реплики или пользовательской начальной инициализации, например WAL-E, следует устанавливать независимо от Patroni.

<a id="package_installation"></a>

--------

## Установка пакетов в Linux {#package-installation-on-linux}

Для операционной системы могут быть доступны пакеты Patroni, подготовленные сообществом Postgres для:

- RHEL, RockyLinux и AlmaLinux;
- Debian и Ubuntu;
- SUSE Enterprise Linux.

Также доступны пакеты прямых зависимостей Patroni, например модулей Python, которых может не быть в официальных репозиториях операционной системы.

Подробнее см. документацию [репозитория PGDG](https://www.postgresql.org/download/linux/).

В производной от RedHat Enterprise Linux операционной системе могут также потребоваться пакеты EPEL; см. документацию [репозитория EPEL](https://docs.fedoraproject.org/en-US/epel/).

После подключения репозитория PGDG для своей ОС можно установить Patroni.

> [!NOTE]
> Пакеты Patroni сопровождаются не разработчиками Patroni, а сообществом Postgres. Если нужна поддержка, сначала обратитесь в [Postgres Slack](http://pgtreats.info/slack-invite).

### Установка в производных Debian {#installing-on-debian-derivatives}

После подключения репозитория PGDG, как описано [выше](/ru/patroni/installation#package_installation), установите Patroni через apt:

```bash
apt-get install patroni
```

### Установка в производных RedHat {#installing-on-redhat-derivatives}

После подключения репозитория PGDG, как описано [выше](/ru/patroni/installation#package_installation), установите Patroni с DCS etcd через dnf в RHEL 9 и производных:

```bash
dnf install patroni patroni-etcd
```

Если производный дистрибутив RedHat не предоставляет пакеты, etcd можно установить из PGDG. На узлах DCS выполните:

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

При необходимости замените версию RHEL в репозитории на `8`, получив `pgdg-rhel8-extras`. В RockyLinux, AlmaLinux, Oracle Linux и других имя репозитория по-прежнему имеет вид `pgdg-rhelN-extras`.

### Установка в SUSE Enterprise Linux {#installing-on-suse-enterprise-linux}

Для некоторых зависимостей может потребоваться включить репозитории SUSE PackageHub. См. документацию [SUSE PackageHub](https://packagehub.suse.com/how-to-use/).

В SLES 15 с подключённым репозиторием PGDG, как описано [выше](/ru/patroni/installation#package_installation), Patroni можно установить командой:

```bash
zypper install patroni patroni-etcd
```

При включённом репозитории SUSE PackageHub можно также установить etcd:

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## Обновление {#upgrading}

Обновление Patroni очень просто: обновите установленное программное обеспечение и перезапустите демон Patroni на каждом узле кластера.

Однако перезапуск демона Patroni приводит к перезапуску базы данных Postgres. В некоторых ситуациях это может вызвать переключение первичного узла при отказе, поэтому до завершения перезапуска демона рекомендуется перевести кластер в режим обслуживания.

Чтобы перевести кластер в режим обслуживания, выполните следующую команду на одном из узлов Patroni:

```bash
patronictl pause --wait
```

Затем на каждом узле кластера обновите пакеты способом, предусмотренным вашей ОС:

```bash
apt-get update && apt-get install patroni patroni-etcd
```

Перезапустите процесс демона Patroni на каждом узле:

```bash
systemctl restart patroni
```

Наконец, возобновите мониторинг Postgres через Patroni, чтобы вывести кластер из режима обслуживания:

```bash
patronictl resume --wait
```

Теперь кластер полностью работоспособен с новой версией Patroni.
