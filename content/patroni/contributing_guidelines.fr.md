---
title: "Guide de contribution"
linkTitle: "Contribution"
weight: 200
icon: fa-solid fa-users
description: "Processus de contribution, canaux de support et directives de développement."
module: [PATRONI]
categories: [Tâche]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>

--------

## Discussion {#chatting}

Si vous avez une question, si vous cherchez de l'aide interactive pour le dépannage ou si vous souhaitez discuter avec d'autres utilisateurs de Patroni, rejoignez-nous sur le canal [#patroni](https://postgresteam.slack.com/archives/C9XPYG92A) dans le [PostgreSQL Slack](https://pgtreats.info/slack-invite).

<a id="reporting_bugs"></a>

--------

## Signalement de bogues {#reporting-bugs}

Avant de signaler un bogue, assurez-vous de **le reproduire avec la dernière version de Patroni** ! Vérifiez également attentivement si le problème existe déjà dans notre [Suivi des problèmes](https://github.com/patroni/patroni/issues).

--------

## Exécution des tests {#running-tests}

Conditions requises pour exécuter les tests behave :

1.  Les paquets PostgreSQL incluant les modules [contrib](https://www.postgresql.org/docs/current/contrib.html) doivent être installés.
2.  Les binaires PostgreSQL doivent être disponibles dans votre `PATH`. Vous devrez peut-être les ajouter au chemin en utilisant quelque chose comme `PATH=/usr/lib/postgresql/11/bin:$PATH python -m behave`.
3.  Si vous souhaitez effectuer des tests avec des DCS externes (par exemple, etcd, Consul ou Zookeeper), vous devrez installer les paquets correspondants et faire fonctionner les services associés, qui doivent accepter les connexions non chiffrées/non protégées sur localhost et le port par défaut. Dans le cas d'etcd ou de Consul, le jeu de tests behave peut les démarrer si les binaires sont disponibles dans le `PATH`.

Installer les dépendances :

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Une fois toutes les dépendances installées, vous pouvez exécuter les différentes suites de tests :

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

## Test avec tox {#testing-with-tox}

Pour exécuter les tests tox, il vous suffit d'installer une seule dépendance (en plus de Python).

``` bash
pip install "tox>=4"
```

Si vous souhaitez exécuter les tests `behave` basés sur Docker, vous devez également avoir installé Docker.

La configuration Tox dans `tox.ini` dispose d’« environnements » permettant d'exécuter les tâches suivantes :

- lint : analyse de code Python avec `flake8`
- test : tests unitaires pour tous les interpréteurs Python disponibles avec `pytest`, génération de rapports HTML si un TTY est détecté, sinon de rapports XML
- dep : détection des conflits de dépendances de paquets à l’aide de `pipdeptree`
- type : vérification statique des types avec `pyright`
- black : formatage du code avec `black`
- docker-build : construction de l’image Docker utilisée pour l’environnement `behave`
- docker-cmd : exécution d’une commande arbitraire avec l’image précédente
- docker-behave-etcd : exécution de tox pour les tests behave avec l’image précédente
- py\*behave : exécution de behave avec les interpréteurs Python disponibles (sans Docker, bien que ce soit ce qui est appelé à l’intérieur des conteneurs Docker)
- docs : génération de la documentation avec `sphinx`

### Exécution de tox {#running-tox}

Pour exécuter la liste d’environnements par défaut (dep, lint, test et docs), exécutez simplement :

``` bash
tox
```

Les environnements `test` peuvent être exécutés avec l'étiquette `test` :

``` bash
tox -m test
```

Les tests Docker `behave` peuvent être exécutés avec l'étiquette `behave` :

``` bash
tox -m behave
```

De même, docs porte l'étiquette `docs`.

Tous les autres environnements peuvent être exécutés avec leurs noms respectifs :

``` bash
tox -e lint
tox -e py39-test-lin
```

Il est également possible de sélectionner des listes d'environnement partielles à l'aide de `factors`. Par exemple, si vous souhaitez exécuter tous les environnements pour Python 3.10 :

``` bash
tox -f py310
```

Cela équivaut à exécuter tous les environnements listés ci-dessous :

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

Vous pouvez lister toutes les combinaisons d'environnements configurées avec tox (≥ v4) comme suit :

``` bash
tox l
```

Les environnements `test` et `docs` tenteront d’ouvrir les fichiers de sortie HTML une fois la tâche terminée, si tox est exécuté depuis un terminal actif. Cette fonction est destinée à faciliter le travail du développeur exécutant cet environnement localement. Elle tentera d’exécuter `open` sur macOS et `xdg-open` sur Linux. Pour utiliser une commande différente, définissez la variable d’environnement `OPEN_CMD` avec le nom ou le chemin de la commande. Si cette étape échoue, cela n’empêchera pas l’exécution globale de la tâche. Pour désactiver cette fonctionnalité, définissez la variable d’environnement `OPEN_CMD` sur la commande no-op `:`.

``` bash
OPEN_CMD=: tox -m docs
```

### Tests Behave {#behave-tests}

Les tests Behave avec `-m behave` construiront des images Docker basées sur les versions 12 à 18 de PG_MAJOR, puis exécuteront tous les tests Behave. Cette opération peut prendre beaucoup de temps ; vous voudrez donc peut-être limiter la portée à une version spécifique de PostgreSQL ou à un ensemble de fonctionnalités ou d’étapes spécifique.

Pour spécifier la version de postgres, indiquez le nom complet de l’environnement de build de l’image dépendante que vous souhaitez utiliser, suivi du nom de l’environnement behave. Par exemple, si vous souhaitez Postgres 14, utilisez :

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

Si, en revanche, vous souhaitez tester une fonctionnalité spécifique, vous pouvez passer des arguments positionnels à behave. Cela exécutera le scénario de test de la fonctionnalité watchdog de behave avec toutes les versions de Postgres.

``` bash
tox -m behave -- features/watchdog.feature
```

Bien sûr, vous pouvez combiner les deux.

--------

## Contribution d'une demande de fusion {#contributing-a-pull-request}

1.  Créez un fork du dépôt, développez et testez vos modifications de code.
2.  Répercutez les modifications dans la documentation utilisateur.
3.  Soumettez une demande de fusion avec une description claire de l'objectif des modifications. Liez une issue existante si nécessaire.

Vous recevrez un retour sur votre demande de fusion dès que possible.

Bon hacking avec Patroni ;-)
