---
title: "Рекомендации по участию в разработке"
linkTitle: "Участие в разработке"
weight: 200
icon: fa-solid fa-users
description: "Рабочий процесс внесения изменений, каналы поддержки и рекомендации по разработке."
module: [PATRONI]
categories: [Задача]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>

--------

## Общение {#chatting}

Если у вас есть вопрос, нужна интерактивная помощь в устранении неполадок или хочется пообщаться с другими пользователями Patroni, присоединяйтесь к каналу [\#patroni](https://postgresteam.slack.com/archives/C9XPYG92A) в [PostgreSQL Slack](https://pgtreats.info/slack-invite).

<a id="reporting_bugs"></a>

--------

## Сообщение об ошибках {#reporting-bugs}

Перед сообщением об ошибке обязательно **воспроизведите её в последней версии Patroni**! Также ещё раз проверьте, не зарегистрирована ли проблема в нашем [трекере](https://github.com/patroni/patroni/issues).

--------

## Запуск тестов {#running-tests}

Требования для запуска тестов behave:

1.  Должны быть установлены пакеты PostgreSQL, включая модули [contrib](https://www.postgresql.org/docs/current/contrib.html).
2.  Двоичные файлы PostgreSQL должны быть доступны в `PATH`. Возможно, их потребуется добавить командой наподобие `PATH=/usr/lib/postgresql/11/bin:$PATH python -m behave`.
3.  Для тестирования с внешними DCS, например Etcd, Consul и Zookeeper, необходимо установить пакеты и запустить соответствующие службы, принимающие незашифрованные и незащищённые соединения на localhost и порту по умолчанию. Для Etcd или Consul набор тестов behave может запустить службы самостоятельно, если двоичные файлы доступны в `PATH`.

Установите зависимости:

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

После установки всех зависимостей можно запускать различные наборы тестов:

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

## Тестирование с tox {#testing-with-tox}

Для запуска тестов tox нужно установить только одну зависимость помимо Python:

``` bash
pip install "tox>=4"
```

Для запуска тестов `behave` на основе Docker также необходим Docker.

Конфигурация Tox в `tox.ini` содержит «окружения» для следующих задач:

- lint: проверка кода Python с помощью `flake8`
- test: модульные тесты со всеми доступными интерпретаторами Python через `pytest`; при наличии TTY создаёт отчёты HTML, иначе — XML
- dep: обнаружение конфликтов зависимостей пакетов с помощью `pipdeptree`
- type: статическая проверка типов с помощью `pyright`
- black: форматирование кода с помощью `black`
- docker-build: сборка образа docker для окружения `behave`
- docker-cmd: выполнение произвольной команды с созданным образом
- docker-behave-etcd: запуск tox для тестов behave с созданным образом
- py\*behave: запуск behave с доступными интерпретаторами Python без docker, хотя именно он вызывается внутри контейнеров docker
- docs: сборка документации с помощью `sphinx`

### Запуск tox {#running-tox}

Чтобы запустить список окружений по умолчанию — dep, lint, test и docs, выполните:

``` bash
tox
```

Окружения `test` можно запустить с меткой `test`:

``` bash
tox -m test
```

Тесты docker `behave` можно запустить с меткой `behave`:

``` bash
tox -m behave
```

Аналогично, документация имеет метку `docs`.

Остальные окружения запускаются по соответствующим именам:

``` bash
tox -e lint
tox -e py39-test-lin
```

Частичные списки окружений можно выбирать с помощью `factors`. Например, для запуска всех окружений Python 3.10:

``` bash
tox -f py310
```

Это эквивалентно запуску всех перечисленных ниже окружений:

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

Все настроенные сочетания окружений tox (\>=v4) можно вывести так:

``` bash
tox l
```

Окружения `test` и `docs` после завершения задания пытаются открыть выходные файлы HTML, если tox запущен в активном терминале. Это удобно разработчику при локальном запуске: на mac выполняется `open`, а в Linux — `xdg-open`. Чтобы использовать другую команду, задайте переменной окружения `OPEN_CMD` имя или путь команды. Неудача этого шага не приводит к неудаче всего запуска. Чтобы отключить эту возможность, задайте переменной `OPEN_CMD` команду без действия `:`.

``` bash
OPEN_CMD=: tox -m docs
```

### Тесты behave {#behave-tests}

Тесты behave с `-m behave` собирают образы docker на основе версий PG_MAJOR с 12 по 18, а затем запускают все тесты behave. Это может занять много времени, поэтому область проверки можно ограничить выбранной версией Postgres, определённым набором возможностей или шагами.

Чтобы указать версию postgres, включите полное имя нужного зависимого окружения сборки образа, а затем имя окружения behave. Например, для Postgres 14 используйте:

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

Чтобы протестировать определённую возможность, можно передать behave позиционные аргументы. Следующая команда запускает сценарий тестирования функции watchdog со всеми версиями Postgres.

``` bash
tox -m behave -- features/watchdog.feature
```

Разумеется, оба подхода можно сочетать.

--------

## Отправка pull request {#contributing-a-pull-request}

1.  Создайте ответвление репозитория, разработайте и протестируйте изменения кода.
2.  Отразите изменения в пользовательской документации.
3.  Отправьте pull request с ясным описанием цели изменений. При необходимости добавьте ссылку на существующую проблему.

Обратная связь по pull request будет предоставлена как можно скорее.

Успешной разработки Patroni ;-)
