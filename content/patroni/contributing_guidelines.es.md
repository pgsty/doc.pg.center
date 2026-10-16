---
title: "Directrices para contribuir"
linkTitle: "Contribuir"
weight: 200
icon: fa-solid fa-users
description: "Flujo de trabajo para contribuciones, canales de soporte y directrices de desarrollo."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>

--------

## Conversar {#chatting}

Si tienes una pregunta, buscas ayuda interactiva para resolver problemas o quieres conversar con otros usuarios de Patroni, únete a nosotros en el canal [\#patroni](https://postgresteam.slack.com/archives/C9XPYG92A) del [Slack de PostgreSQL](https://pgtreats.info/slack-invite).

<a id="reporting_bugs"></a>

--------

## Informar de errores {#reporting-bugs}

Antes de informar de un error, ¡asegúrate de **reproducirlo con la última versión de Patroni**! Comprueba también detenidamente si el problema ya existe en nuestro [rastreador de problemas](https://github.com/patroni/patroni/issues).

--------

## Ejecutar las pruebas {#running-tests}

Requisitos para ejecutar las pruebas behave:

1.  Los paquetes de PostgreSQL, incluidos los módulos [contrib](https://www.postgresql.org/docs/current/contrib.html), deben estar instalados.
2.  Los binarios de PostgreSQL deben estar disponibles en tu `PATH`. Puede que necesites añadirlos a la ruta con algo como `PATH=/usr/lib/postgresql/11/bin:$PATH python -m behave`.
3.  Si quieres probar con DCS externos (por ejemplo, Etcd, Consul y Zookeeper), necesitarás los paquetes instalados y los servicios correspondientes en ejecución y aceptando conexiones sin cifrar/sin proteger en localhost y el puerto predeterminado. En el caso de Etcd o Consul, el conjunto de pruebas behave podría iniciarlos si los binarios están disponibles en el `PATH`.

Instala las dependencias:

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Una vez que tengas todas las dependencias instaladas, puedes ejecutar los diversos conjuntos de pruebas:

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

## Probar con tox {#testing-with-tox}

Para ejecutar las pruebas de tox solo necesitas instalar una dependencia (aparte de Python)

``` bash
pip install "tox>=4"
```

Si deseas ejecutar las pruebas `behave` basadas en Docker, entonces también necesitas tener Docker instalado.

La configuración de Tox en `tox.ini` tiene «entornos» para ejecutar las siguientes tareas:

- lint: análisis estático de código Python con `flake8`
- test: pruebas unitarias para todos los intérpretes de python disponibles con `pytest`; genera informes HTML si se detecta una TTY, de lo contrario informes XML
- dep: detecta conflictos de dependencias de paquetes usando `pipdeptree`
- type: comprobación de tipos estática con `pyright`
- black: formato de código con `black`
- docker-build: construye la imagen docker usada para el entorno `behave`
- docker-cmd: ejecuta un comando arbitrario con la imagen anterior
- docker-behave-etcd: ejecuta tox para las pruebas behave con la imagen anterior
- py\*behave: ejecuta behave con los intérpretes de python disponibles (sin docker, aunque esto es lo que se ejecuta dentro de los contenedores docker)
- docs: construye la documentación con `sphinx`

### Ejecutar tox {#running-tox}

Para ejecutar la lista predeterminada de entornos; dep, lint, test y docs, simplemente ejecuta:

``` bash
tox
```

Los entornos `test` pueden ejecutarse con la etiqueta `test`:

``` bash
tox -m test
```

Las pruebas docker de `behave` pueden ejecutarse con la etiqueta `behave`:

``` bash
tox -m behave
```

De forma similar, docs tiene la etiqueta `docs`.

Todos los demás entornos pueden ejecutarse con sus respectivos nombres de entorno:

``` bash
tox -e lint
tox -e py39-test-lin
```

También es posible seleccionar listas parciales de entornos usando `factors`. Por ejemplo, si quieres ejecutar todos los entornos para python 3.10:

``` bash
tox -f py310
```

Esto es equivalente a ejecutar todos los entornos listados a continuación:

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

Puedes listar todas las combinaciones configuradas de entornos con tox (\>=v4) así

``` bash
tox l
```

Los entornos `test` y `docs` intentarán abrir los archivos de salida HTML cuando el trabajo termine, si tox se ejecuta con una terminal activa. Esto está pensado en beneficio del desarrollador que ejecuta este entorno localmente. Intentará ejecutar `open` en un mac y `xdg-open` en Linux. Para usar un comando diferente, establece la variable de entorno `OPEN_CMD` al nombre o ruta del comando. Si este paso falla, no hará fallar la ejecución en general. Si quieres desactivar esta función, establece la variable de entorno `OPEN_CMD` al comando no-op `:`.

``` bash
OPEN_CMD=: tox -m docs
```

### Pruebas behave {#behave-tests}

Las pruebas behave con `-m behave` construirán imágenes docker basadas en la versión de PG_MAJOR de la 12 a la 18 y luego ejecutarán todas las pruebas behave. Esto puede tardar bastante en ejecutarse, por lo que quizás quieras limitar el alcance a una versión seleccionada de Postgres o a un conjunto de características o pasos específico.

Para especificar la versión de postgres incluye el nombre completo del entorno de construcción de imagen dependiente que quieras y luego el nombre del entorno behave. Por ejemplo, si quieres Postgres 14 usa:

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

Si por el contrario quieres probar una característica específica, puedes pasar argumentos posicionales a behave. Esto ejecutará el escenario de prueba de la característica watchdog de behave con todas las versiones de Postgres.

``` bash
tox -m behave -- features/watchdog.feature
```

Por supuesto, puedes combinar ambos.

--------

## Contribuir con un pull request {#contributing-a-pull-request}

1.  Haz un fork del repositorio, desarrolla y prueba tus cambios de código.
2.  Refleja los cambios en la documentación de usuario.
3.  Envía un pull request con una descripción clara del objetivo de los cambios. Enlaza un problema existente si es necesario.

Recibirás comentarios sobre tu pull request lo antes posible.

¡Feliz hacking con Patroni! ;-)
