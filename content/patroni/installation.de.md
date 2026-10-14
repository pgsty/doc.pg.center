---
title: "Installation"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "Installation und Upgrade von Patroni auf den unterstützten Plattformen."
module: [PATRONI]
categories: [Tutorial]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## Voraussetzungen unter Mac OS {#pre-requirements-for-mac-os}

Zum Installieren der Voraussetzungen auf einem Mac folgenden Befehl ausführen:

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

Seit [psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/) wird die Binärversion von psycopg2 nicht mehr standardmäßig installiert. Für die Installation aus dem Quellcode werden ein C-Compiler sowie die Entwicklungspakete für Postgres und Python benötigt. Da sich in Python keine Abhängigkeit in der Form `psycopg2 OR psycopg2-binary` angeben lässt, muss die Installationsart selbst gewählt werden.

Es stehen mehrere Möglichkeiten zur Verfügung:

1.  Den Paketmanager der Distribution verwenden.

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2.  Bei der Installation von Patroni mit pip eines der Pakete `psycopg3`, `psycopg2` oder `psycopg2-binary` in der [Liste der Abhängigkeiten](/de/patroni/installation#extras) angeben.

<a id="extras"></a>

--------

## Allgemeine Installation mit pip {#general-installation-for-pip}

Patroni lässt sich mit pip installieren:

```bash
pip install patroni[dependencies]
```

Dabei kann `dependencies` leer sein oder aus einem oder mehreren der folgenden Einträge bestehen:

etcd oder etcd3  
Modul `python-etcd`, um etcd als verteilten Konfigurationsspeicher (DCS) zu verwenden

consul  
Modul `py-consul`, um Consul als DCS zu verwenden

zookeeper  
Modul `kazoo`, um ZooKeeper als DCS zu verwenden

exhibitor  
Modul `kazoo`, um Exhibitor als DCS zu verwenden (dieselben Abhängigkeiten wie für ZooKeeper)

kubernetes  
Modul [kubernetes](/de/patroni/kubernetes#kubernetes), um Kubernetes als DCS in Patroni zu verwenden

raft  
Modul `pysyncobj`, um die Python-Implementierung von Raft als DCS zu verwenden

aws  
`boto3`, um AWS-Callbacks zu verwenden

jsonlogger  
Modul `python-json-logger`, um die [Protokollierung](/de/patroni/config/yaml#log_settings) im JSON-Format zu aktivieren

systemd  
`systemd-python`, um die sd_notify-Integration zu verwenden

all  
Alle oben genannten Abhängigkeiten (außer der psycopg-Familie)

psycopg3  
Modul `psycopg[binary]>=3.0.0`

psycopg2  
Modul `psycopg2>=2.5.4`

psycopg2-binary  
Modul `psycopg2-binary`

Um Patroni zusammen mit psycopg3, den Abhängigkeiten für etcd als DCS und den AWS-Callbacks zu installieren, lautet der Befehl beispielsweise:

```bash
pip install patroni[psycopg3,etcd3,aws]
```

Externe Werkzeuge, die in Skripten zur Replikaterstellung oder benutzerdefinierten Cluster-Initialisierung aufgerufen werden (z. B. WAL-E), sollten unabhängig von Patroni installiert werden.

<a id="package_installation"></a>

--------

## Paketinstallation unter Linux {#package-installation-on-linux}

Für das verwendete Betriebssystem sind möglicherweise Patroni-Pakete verfügbar. Die Postgres-Community erstellt solche Pakete für:

- RHEL, RockyLinux, AlmaLinux;
- Debian und Ubuntu;
- SUSE Enterprise Linux.

Es gibt auch Pakete für direkte Abhängigkeiten von Patroni, etwa Python-Module, die möglicherweise nicht in den offiziellen Paketquellen des Betriebssystems enthalten sind.

Weitere Informationen stehen in der Dokumentation des [PGDG-Repositorys](https://www.postgresql.org/download/linux/).

Bei einem auf RedHat Enterprise Linux basierenden Betriebssystem werden möglicherweise zusätzlich Pakete aus EPEL benötigt; siehe die Dokumentation des [EPEL-Repositorys](https://docs.fedoraproject.org/en-US/epel/).

Nach dem Einrichten des PGDG-Repositorys für das Betriebssystem kann Patroni installiert werden.

> [!NOTE]
> Die Patroni-Pakete werden von der Postgres-Community gepflegt, nicht von den Patroni-Entwicklern. Bei Unterstützungsbedarf zunächst im [Postgres-Slack](http://pgtreats.info/slack-invite) nachfragen.

### Installation auf Debian-basierten Distributionen {#installing-on-debian-derivatives}

Nach dem Einrichten des PGDG-Repositorys, siehe [oben](/de/patroni/installation#package_installation), Patroni mit apt installieren:

```bash
apt-get install patroni
```

### Installation auf RedHat-basierten Distributionen {#installing-on-redhat-derivatives}

Nach dem Einrichten des PGDG-Repositorys, siehe [oben](/de/patroni/installation#package_installation), Patroni mit etcd als DCS unter RHEL 9 (und davon abgeleiteten Distributionen) über dnf installieren:

```bash
dnf install patroni patroni-etcd
```

Bietet die RedHat-basierte Distribution keine etcd-Pakete an, kann etcd aus PGDG installiert werden. Auf den für den DCS vorgesehenen Knoten folgende Befehle ausführen:

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

Falls erforderlich, die RHEL-Version im Repository durch `8` ersetzen, sodass sich `pgdg-rhel8-extras` ergibt. Auch auf RockyLinux, AlmaLinux, Oracle Linux usw. lautet der Repository-Name `pgdg-rhelN-extras`.

### Installation unter SUSE Enterprise Linux {#installing-on-suse-enterprise-linux}

Für einige Abhängigkeiten müssen möglicherweise die SUSE-PackageHub-Repositorys aktiviert werden. Siehe die Dokumentation von [SUSE PackageHub](https://packagehub.suse.com/how-to-use/).

Unter SLES 15 kann Patroni nach dem Einrichten des PGDG-Repositorys, siehe [oben](/de/patroni/installation#package_installation), wie folgt installiert werden:

```bash
zypper install patroni patroni-etcd
```

Mit aktiviertem SUSE-PackageHub-Repository lässt sich auch etcd installieren:

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## Upgrade {#upgrading}

Ein Upgrade von Patroni ist sehr einfach: Die Softwareinstallation aktualisieren und den Patroni-Daemon auf jedem Knoten im Cluster neu starten.

Der Neustart des Patroni-Daemons führt jedoch zu einem Neustart der Postgres-Datenbank. Dies kann unter bestimmten Umständen ein Failover des Primärservers auslösen. Deshalb wird empfohlen, den Cluster bis zum Abschluss des Patroni-Daemon-Neustarts in den Wartungsmodus zu versetzen.

Dazu auf einem der Patroni-Knoten folgenden Befehl ausführen:

```bash
patronictl pause --wait
```

Anschließend auf jedem Clusterknoten das für das Betriebssystem erforderliche Paketupgrade durchführen:

```bash
apt-get update && apt-get install patroni
```

Den Patroni-Daemon-Prozess auf jedem Knoten neu starten:

```bash
systemctl restart patroni
```

Abschließend die Postgres-Überwachung durch Patroni wieder aufnehmen und damit den Wartungsmodus beenden:

```bash
patronictl resume --wait
```

Der Cluster ist nun mit der neuen Patroni-Version wieder voll betriebsbereit.
