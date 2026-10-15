---
title: "Leitfaden zur Mitarbeit"
linkTitle: "Mitarbeit"
weight: 200
icon: fa-solid fa-users
description: "Ablauf für Beiträge, Anlaufstellen für Unterstützung und Entwicklungsrichtlinien."
module: [PATRONI]
categories: [Aufgabe]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>

--------

## Austausch {#chatting}

Bei Fragen, für interaktive Hilfe zur Fehlerbehebung oder zum Austausch mit anderen Patroni-Nutzern steht der Kanal [\#patroni](https://postgresteam.slack.com/archives/C9XPYG92A) im [PostgreSQL-Slack](https://pgtreats.info/slack-invite) zur Verfügung.

<a id="reporting_bugs"></a>

--------

## Fehler melden {#reporting-bugs}

Vor dem Melden eines Fehlers sicherstellen, dass er **mit der neuesten Patroni-Version reproduzierbar ist**! Außerdem sorgfältig prüfen, ob das Problem bereits in unserem [Issue-Tracker](https://github.com/patroni/patroni/issues) erfasst ist.

--------

## Tests ausführen {#running-tests}

Voraussetzungen für die Ausführung von behave-Tests:

1.  Die PostgreSQL-Pakete einschließlich der [contrib](https://www.postgresql.org/docs/current/contrib.html)-Module müssen installiert sein.
2.  Die ausführbaren PostgreSQL-Dateien müssen im `PATH` verfügbar sein. Gegebenenfalls müssen sie zum Suchpfad hinzugefügt werden, etwa mit `PATH=/usr/lib/postgresql/11/bin:$PATH python -m behave`.
3.  Für Tests mit externen DCS (z. B. etcd, Consul und Zookeeper) müssen die Pakete installiert sein und die jeweiligen Dienste laufen. Sie müssen unverschlüsselte/ungeschützte Verbindungen auf localhost und dem Standardport annehmen. Bei etcd oder Consul kann die behave-Testsuite die Dienste starten, wenn die ausführbaren Dateien im `PATH` verfügbar sind.

Abhängigkeiten installieren:

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Nach der Installation aller Abhängigkeiten können die verschiedenen Testsuiten ausgeführt werden:

``` bash
# You may want to use Virtualenv or specify python3.

# Run flake8 to check syntax and formatting:
python setup.py flake8

# Run the pytest suite in tests/:
python setup.py test

# Moreover, you may want to run tests in different scopes for debugging purposes,
# the -s option include print output during test execution.
# Tests in pytest typically follow the pattern: FILEPATH::CLASSNAME::TESTNAME.
pytest -s tests/test_api.py
pytest -s tests/test_api.py::TestRestApiHandler
pytest -s tests/test_api.py::TestRestApiHandler::test_do_GET

# Run the behave (https://behave.readthedocs.io/en/latest/) test suite in features/;
# modify DCS as desired (raft has no dependencies so is the easiest to start with):
DCS=raft python -m behave
```

--------

## Testen mit tox {#testing-with-tox}

Für tox-Tests muss neben Python nur eine Abhängigkeit installiert werden:

``` bash
pip install "tox>=4"
```

Für die Ausführung der Docker-basierten `behave`-Tests muss außerdem Docker installiert sein.

Die Tox-Konfiguration in `tox.ini` enthält „Umgebungen“ für die folgenden Aufgaben:

- lint: Python-Code mit `flake8` prüfen
- test: Unit-Tests mit `pytest` für alle verfügbaren Python-Interpreter; erzeugt bei erkanntem TTY HTML-Berichte, andernfalls XML-Berichte
- dep: Konflikte zwischen Paketabhängigkeiten mit `pipdeptree` erkennen
- type: statische Typprüfung mit `pyright`
- black: Codeformatierung mit `black`
- docker-build: Docker-Image für die Umgebung `behave` erstellen
- docker-cmd: beliebigen Befehl mit dem obigen Image ausführen
- docker-behave-etcd: tox für behave-Tests mit dem obigen Image ausführen
- py\*behave: behave mit den verfügbaren Python-Interpretern ausführen (ohne Docker, obwohl genau dies innerhalb der Docker-Container aufgerufen wird)
- docs: Dokumentation mit `sphinx` erstellen

### tox ausführen {#running-tox}

Um die Standardliste der Umgebungen dep, lint, test und docs auszuführen, genügt:

``` bash
tox
```

Die Umgebungen `test` können mit dem Label `test` ausgeführt werden:

``` bash
tox -m test
```

Die Docker-Tests für `behave` können mit dem Label `behave` ausgeführt werden:

``` bash
tox -m behave
```

Entsprechend hat docs das Label `docs`.

Alle anderen Umgebungen können über ihre jeweiligen Namen ausgeführt werden:

``` bash
tox -e lint
tox -e py39-test-lin
```

Mit `factors` können auch Teilmengen der Umgebungen ausgewählt werden. Beispielsweise lassen sich alle Umgebungen für Python 3.10 wie folgt ausführen:

``` bash
tox -f py310
```

Dies entspricht der Ausführung aller nachfolgend aufgeführten Umgebungen:

``` bash
$ tox -l -f py310
py310-test-lin
py310-test-mac
py310-test-win
py310-type-lin
py310-type-mac
py310-type-win
py310-behave-etcd-lin
py310-behave-etcd-win
py310-behave-etcd-mac
py310-behave-etcd3-lin
py310-behave-etcd3-win
py310-behave-etcd3-mac
```

Alle konfigurierten Kombinationen von Umgebungen lassen sich mit tox (\>=v4) wie folgt auflisten:

``` bash
tox l
```

Die Umgebungen `test` und `docs` versuchen nach Abschluss der Aufgabe, die HTML-Ausgabedateien zu öffnen, sofern tox in einem aktiven Terminal läuft. Dies soll die lokale Arbeit mit diesen Umgebungen erleichtern. Auf einem Mac wird dazu `open` aufgerufen, unter Linux `xdg-open`. Für einen anderen Befehl die Umgebungsvariable `OPEN_CMD` auf dessen Namen oder Pfad setzen. Schlägt dieser Schritt fehl, schlägt dadurch nicht der gesamte Durchlauf fehl. Zum Deaktivieren dieser Funktion die Umgebungsvariable `OPEN_CMD` auf den wirkungslosen Befehl `:` setzen.

``` bash
OPEN_CMD=: tox -m docs
```

### Behave-Tests {#behave-tests}

Behave-Tests mit `-m behave` erstellen Docker-Images auf Basis der PG_MAJOR-Versionen 12 bis 18 und führen anschließend alle behave-Tests aus. Dies kann recht lange dauern. Daher kann es sinnvoll sein, den Umfang auf eine bestimmte Postgres-Version, bestimmte Funktionen oder einzelne Schritte zu begrenzen.

Um die Postgres-Version festzulegen, den vollständigen Namen der gewünschten abhängigen Umgebung zum Erstellen des Images angeben, gefolgt vom Namen der behave-Umgebung. Beispielsweise für Postgres 14:

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

Um hingegen eine bestimmte Funktion zu testen, können Positionsargumente an behave übergeben werden. Der folgende Befehl führt das behave-Testszenario für die Watchdog-Funktion mit allen Postgres-Versionen aus.

``` bash
tox -m behave -- features/watchdog.feature
```

Beide Möglichkeiten lassen sich auch kombinieren.

--------

## Einen Pull Request einreichen {#contributing-a-pull-request}

1.  Einen Fork des Repositories erstellen, die Codeänderungen entwickeln und testen.
2.  Die Änderungen in der Benutzerdokumentation berücksichtigen.
3.  Einen Pull Request mit einer klaren Beschreibung des Ziels der Änderungen einreichen. Falls nötig, einen bestehenden Issue verlinken.

Rückmeldung zum Pull Request erfolgt so bald wie möglich.

Viel Spaß beim Entwickeln mit Patroni ;-)
