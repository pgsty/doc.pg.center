---
title: Notificación de errores
weight: 1400
description: Cómo presentar informes de problemas para el proyecto etcd
icon: fa-solid fa-bug
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/reporting_bugs.md"
---

Si cualquier parte del proyecto etcd tiene errores o erratas en la documentación, háznoslo saber [abriendo un issue][etcd-issue]. Tomamos los errores y las erratas muy en serio y creemos que ningún problema es demasiado pequeño. Antes de crear un informe de error, comprueba que no exista ya un issue que informe del mismo problema.

Para que el informe de error sea preciso y fácil de entender, intenta que cada informe de error sea:

- Específico. Incluye todos los detalles posibles: qué versión, qué entorno, qué configuración, etc. Si el error está relacionado con la ejecución del servidor de etcd, adjunta el registro de etcd (el registro de arranque con la configuración de etcd es especialmente importante).

- Reproducible. Incluye los pasos para reproducir el problema. Entendemos que algunos problemas pueden ser difíciles de reproducir; incluye los pasos que podrían conducir al problema. Si es posible, adjunta al informe de error el directorio de datos de etcd afectado y la traza de pila.

- Aislado. Intenta aislar y reproducir el error con el mínimo de dependencias. Demasiadas dependencias en un informe de error ralentizarían considerablemente la corrección del error. Depurar sistemas externos que dependen de etcd está fuera del alcance, pero con gusto orientamos en la dirección correcta o ayudamos con el uso del propio etcd.

- Único. No dupliques un informe de error existente.

- Delimitado. Un error por informe. No añadas otro error dentro de un mismo informe.

Puede merecer la pena leer [el artículo de Elika Etemad sobre cómo redactar buenos informes de error][filing-good-bugs] antes de crear un informe de error.

Podemos pedir más información para localizar un error. Un informe de error duplicado se cerrará.

## Preguntas frecuentes {#frequently-asked-questions}

### Cómo obtener una traza de pila {#how-to-get-a-stack-trace}

``` bash
$ kill -QUIT $PID
```

### Cómo obtener la versión de etcd {#how-to-get-etcd-version}

``` bash
$ etcd --version
```

### Cómo obtener la configuración y el registro de etcd cuando se ejecuta como servicio de systemd «etcd2.service» {#how-to-get-etcd-configuration-and-log-when-it-runs-as-systemd-service-etcd2service}

``` bash
$ sudo systemctl cat etcd2
$ sudo journalctl -u etcd2
```

Debido a un error de systemd aguas arriba, journald puede perder las últimas líneas de registro cuando sus procesos terminan. Si journalctl indica que etcd se detuvo sin un mensaje fatal o de panic, prueba `sudo journalctl -f -t etcd2` para obtener el registro completo.

[etcd-issue]: https://github.com/etcd-io/etcd/issues/new
[filing-good-bugs]: http://fantasai.inkedblade.net/style/talks/filing-good-bugs/
