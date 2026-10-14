---
title: "Mehrere Schreibvorgänge in einer Transaktion ausführen"
description: "Anleitung zu transaktionalen Schreibvorgängen"
weight: 500
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
---

## Voraussetzungen {#prerequisites}

* [`etcd` und `etcdctl`](/de/etcd/install/) installieren.
* Ein laufender `etcd`-Cluster.

## Begriffe {#terminology}

Im Folgenden werden wichtige Begriffe aus dem unten stehenden [Beispiel](#example) definiert.

| Begriffe | Definition |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | Das Befehlszeilenwerkzeug zur Interaktion mit dem etcd-Server. |
| Befehl [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options) | Der Befehl `txn` ist eine Abkürzung für „transaction“ (Transaktion). Er liest mehrere etcd-Anfragen von der Standardeingabe und wendet sie als eine einzige atomare Transaktion an. Eine Transaktion besteht aus einer Liste von Bedingungen, einer Liste von Anfragen für den Fall, dass alle Bedingungen erfüllt sind, und einer Liste von Anfragen für den Fall, dass mindestens eine Bedingung nicht erfüllt ist. Weitere Informationen unter [etcdctl-Befehle für Schlüssel-Wert-Paare](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands).|
| `compare` | Die Klausel `compare` innerhalb einer Transaktion (`txn`) prüft eine Bedingung und entscheidet dadurch, ob die Operationen der Transaktion ausgeführt werden sollen. Änderungen werden nur angewendet, wenn der aktuelle Zustand des Schlüssel-Wert-Speichers den erwarteten Bedingungen entspricht. Dies erhält die Datenkonsistenz und verhindert Konflikte bei nebenläufigen Zugriffen. Der Aufbau des Befehls wird im folgenden Abschnitt [Eine Transaktion ausführen](#2-perform-a-transaction) gezeigt.|

## Transaktionen {#transactions}

`txn` zum Verarbeiten aller Anfragen in einer Transaktion:

```bash
etcdctl txn --help
```

Mit Transaktionen in etcd lassen sich mehrere Operationen atomar ausführen: Entweder werden alle Operationen angewendet oder keine. Das ist entscheidend, um bei zusammengehörigen Aktualisierungen die Datenkonsistenz zu wahren. Weitere Informationen zu Transaktionen enthält [die API-Dokumentation](/de/etcd/learning/api/#transaction).

### Beispiel {#example}

Angenommen, die E-Mail-Adresse und Telefonnummer eines Benutzers sollen in einer einzigen Transaktion aktualisiert werden. So werden beide Änderungen gemeinsam angewendet.

![05_etcdctl_transaction_2024101213](/etcd/tasks/img/transactional-write.gif)

#### 0. Verwendete Variablen und Optionen {#0-variables-and-flags-used}

| Variablen |
| :--- |
| `/users/{<user_id>/email` : etcd-Schlüssel für die E-Mail-Adresse eines Benutzers.|
| `/users/<user_id>/phone` : etcd-Schlüssel für die Telefonnummer eines Benutzers.|
| **Optionen** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3) : Option zur manuellen Eingabe von Transaktionsdaten|

#### 1. Anfangsdaten einrichten {#1-set-up-initial-data}

Zunächst einen Benutzer mit einigen Anfangsdaten erstellen.

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. Eine Transaktion ausführen {#2-perform-a-transaction}

Die E-Mail-Adresse und Telefonnummer des Benutzers in einer einzigen Transaktion aktualisieren.

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

* **Vergleich**: Prüfen, ob die aktuelle E-Mail-Adresse "<old.address@johndoe.com>" lautet. So wird die Transaktion nur fortgesetzt, wenn die Daten dem erwarteten Zustand entsprechen.
* **Erfolg**: Bei erfolgreichem Vergleich sowohl die E-Mail-Adresse als auch die Telefonnummer aktualisieren.
* **Fehlschlag**: Schlägt der Vergleich fehl, die aktuelle E-Mail-Adresse abrufen, um zu verstehen, warum die Transaktion nicht fortgesetzt wurde.

### Wichtige Hinweise {#important-considerations}

* **Atomarität**: Die Transaktion stellt sicher, dass E-Mail-Adresse und Telefonnummer gemeinsam aktualisiert werden. Ist die Anfangsbedingung (der Vergleich) nicht erfüllt, wird keine der beiden Änderungen angewendet.
* **Konsistenz**: Transaktionen erhalten die Datenkonsistenz, insbesondere bei mehreren zusammengehörigen Aktualisierungen.
* **Mehrere put-Operationen für denselben Schlüssel vermeiden**: Innerhalb einer einzigen Transaktion nicht mehrere Werte für denselben Schlüssel schreiben, da dies zu unerwarteten Ergebnissen führen kann. Jeder Schlüssel sollte pro Transaktion nur einmal aktualisiert werden.
