---
title: "Instalación"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "Instrucciones de instalación y actualización de Patroni en las plataformas compatibles."
module: [PATRONI]
categories: [Tutorial]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## Requisitos previos para Mac OS {#pre-requirements-for-mac-os}

Para instalar los requisitos en una Mac, ejecuta lo siguiente:

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

A partir de [psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/) la versión binaria de psycopg2 ya no se instalará de forma predeterminada. Instalarla desde el código fuente requiere un compilador de C y los paquetes de desarrollo de postgres+python. Dado que en el mundo de python no es posible especificar la dependencia como `psycopg2 OR psycopg2-binary`, tendrás que decidir cómo instalarla.

Hay algunas opciones disponibles:

1.  Usa el gestor de paquetes de tu distribución

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2.  Especifica una de `psycopg3`, `psycopg2` o `psycopg2-binary` en la [lista de dependencias](/es/patroni/installation#extras) al instalar Patroni con pip.

<a id="extras"></a>

--------

## Instalación general con pip {#general-installation-for-pip}

Patroni se puede instalar con pip:

```bash
pip install patroni[dependencies]
```

donde `dependencies` puede estar vacío o constar de uno o más de los siguientes:

etcd o etcd3  
módulo `python-etcd` para usar Etcd como Distributed Configuration Store (DCS)

consul  
módulo `py-consul` para usar Consul como DCS

zookeeper  
módulo `kazoo` para usar Zookeeper como DCS

exhibitor  
módulo `kazoo` para usar Exhibitor como DCS (las mismas dependencias que para Zookeeper)

kubernetes  
módulo [kubernetes](/es/patroni/kubernetes#kubernetes) para usar Kubernetes como DCS en Patroni

raft  
módulo `pysyncobj` para usar la implementación de Raft en python como DCS

aws  
`boto3` para usar los callbacks de AWS

jsonlogger  
módulo `python-json-logger` para habilitar el [registro](/es/patroni/config/yaml#log_settings) en formato json

systemd  
`systemd-python` para usar la integración con sd_notify

all  
todos los anteriores (excepto la familia psycopg)

psycopg3  
módulo `psycopg[binary]>=3.0.0`

psycopg2  
módulo `psycopg2>=2.5.4`

psycopg2-binary  
módulo `psycopg2-binary`

Por ejemplo, el comando para instalar Patroni junto con psycopg3, las dependencias para Etcd como DCS y los callbacks de AWS es:

```bash
pip install patroni[psycopg3,etcd3,aws]
```

Ten en cuenta que las herramientas externas que se invocan en la creación de réplicas o en los scripts de bootstrap personalizados (p. ej. WAL-E) deben instalarse de forma independiente de Patroni.

<a id="package_installation"></a>

--------

## Instalación de paquetes en Linux {#package-installation-on-linux}

Es posible que haya paquetes de Patroni disponibles para tu sistema operativo, producidos por la comunidad de Postgres para:

- RHEL, RockyLinux, AlmaLinux;
- Debian y Ubuntu;
- SUSE Enterprise Linux.

También puedes encontrar paquetes para las dependencias directas de Patroni, como módulos de python que podrían no estar disponibles en los repositorios oficiales del sistema operativo.

Para más información consulta la documentación del [repositorio PGDG](https://www.postgresql.org/download/linux/).

Si estás en un sistema operativo derivado de RedHat Enterprise Linux, también podrías necesitar paquetes de EPEL; consulta la documentación del [repositorio EPEL](https://docs.fedoraproject.org/en-US/epel/).

Una vez que hayas instalado el repositorio PGDG para tu sistema operativo, podrás instalar patroni.

> [!NOTE]
> Los paquetes de Patroni no los mantienen los desarrolladores de Patroni, sino la comunidad de Postgres. Si necesitas soporte, primero intenta conectarte en el [Slack de Postgres](http://pgtreats.info/slack-invite).

### Instalación en derivados de Debian {#installing-on-debian-derivatives}

Con el repositorio PGDG instalado, consulta [arriba](/es/patroni/installation#package_installation); para instalar Patroni mediante apt, ejecuta:

```bash
apt-get install patroni
```

### Instalación en derivados de RedHat {#installing-on-redhat-derivatives}

Con el repositorio PGDG instalado, consulta [arriba](/es/patroni/installation#package_installation); para instalar patroni con un DCS etcd mediante dnf en RHEL 9 (y derivados), ejecuta:

```bash
dnf install patroni patroni-etcd
```

Puedes instalar etcd desde PGDG si tu distribución derivada de RedHat no proporciona paquetes. En los nodos que alojarán el DCS, ejecuta:

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

Si es necesario, puedes reemplazar la versión de RHEL por `8` en el repositorio para obtener `pgdg-rhel8-extras`. El nombre del repositorio sigue siendo `pgdg-rhelN-extras` en RockyLinux, AlmaLinux, Oracle Linux, etc...

### Instalación en SUSE Enterprise Linux {#installing-on-suse-enterprise-linux}

Es posible que necesites habilitar los repositorios de SUSE PackageHub para algunas dependencias. Consulta la documentación de [SUSE PackageHub](https://packagehub.suse.com/how-to-use/).

Para SLES 15 con el repositorio PGDG instalado, consulta [arriba](/es/patroni/installation#package_installation); puedes instalar patroni usando:

```bash
zypper install patroni patroni-etcd
```

Con el repositorio de SUSE PackageHub habilitado, también puedes instalar etcd:

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## Actualización {#upgrading}

Actualizar patroni es un proceso muy simple: solo actualiza la instalación del software y reinicia el demonio de Patroni en cada nodo del clúster.

Sin embargo, reiniciar el demonio de Patroni provocará un reinicio de la base de datos de Postgres. En algunas situaciones esto puede causar una conmutación por error del nodo primario de tu clúster; por lo tanto, se recomienda poner el clúster en modo de mantenimiento hasta que el reinicio del demonio de Patroni se haya completado.

Para poner el clúster en modo de mantenimiento, ejecuta el siguiente comando en uno de los nodos de patroni:

```bash
patronictl pause --wait
```

Luego, en cada nodo del clúster, realiza la actualización de paquetes requerida para tu sistema operativo:

```bash
apt-get update && apt-get install patroni
```

Reinicia el proceso del demonio patroni en cada nodo:

```bash
systemctl restart patroni
```

Finalmente, reanuda la monitorización de Postgres con patroni para sacarlo del modo de mantenimiento:

```bash
patronictl resume --wait
```

El clúster quedará ahora totalmente operativo con la nueva versión de Patroni.
