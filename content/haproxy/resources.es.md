---
title: "Documentación y comunidad"
linkTitle: "Recursos"
weight: 100
description: "El conjunto de manuales del proyecto upstream, las ubicaciones de las fuentes, los canales de soporte, los contactos y la licencia"
icon: fa-solid fa-life-ring
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/intro/resources/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapters 1 and 5"
---

## 1. Documentación disponible {#section-1}

La documentación completa de HAProxy está contenida en los documentos siguientes. Asegúrate de
consultar la documentación pertinente para ahorrar tiempo y obtener la respuesta más precisa a tus
necesidades. Abstente igualmente de enviar a la lista de correo preguntas cuyas respuestas ya están
presentes en estos documentos.

- [`intro.txt`](/es/haproxy/load-balancing/) (este documento): presenta los fundamentos del balanceo
  de carga, HAProxy como producto, qué hace, qué no hace, algunas trampas conocidas que conviene
  evitar, algunas limitaciones específicas de ciertos sistemas operativos, cómo obtenerlo, cómo
  evoluciona, cómo asegurarte de que ejecutas una versión con todas las correcciones conocidas, cómo
  actualizarlo, complementos y alternativas.

- [`management.txt`](/es/haproxy/prerequisites/): explica cómo iniciar haproxy, cómo gestionarlo en
  tiempo de ejecución, cómo gestionarlo en varios nodos y cómo proceder con actualizaciones sin
  interrupción.

- [`configuration.txt`](/es/haproxy/http-fundamentals/): el manual de referencia detalla todas las
  palabras clave de configuración y sus opciones. Se utiliza cuando es necesario cambiar la
  configuración.

- coding-style.txt: está dirigido a los desarrolladores que quieren proponer código al proyecto.
  Explica el estilo que debe adoptar el código. No es muy estricto y no toda la base de código lo
  respeta por completo, pero las contribuciones que se desvíen demasiado de él serán rechazadas.

- proxy-protocol.txt: esta es la especificación de facto del protocolo PROXY, que implementan HAProxy
  y una serie de productos de terceros.

- security.txt: cómo informar de un problema de seguridad y qué califica y qué no califica como
  vulnerabilidad.

- README: cómo compilar HAProxy a partir de las fuentes

## 5. Contactos {#section-5}

Si quieres ponerte en contacto con los desarrolladores o con cualquier miembro de la comunidad para
cualquier cosa, la mejor forma de hacerlo suele ser la lista de correo, enviando tu mensaje a
<haproxy@formilux.org>. Ten en cuenta que esta lista es pública y que sus archivos históricos también
lo son, de modo que conviene evitar divulgar información sensible. Allí están presentes unos mil
usuarios con niveles de experiencia diversos e incluso las preguntas más complejas suelen encontrar
relativamente rápido una respuesta óptima. Las sugerencias también son bienvenidas. Para los usuarios
con dificultades con el correo electrónico, hay una plataforma Discourse disponible en
<http://discourse.haproxy.org/> . Sin embargo, ten presente que hay menos personas leyendo las
preguntas allí y que la mayoría las atiende un equipo realmente diminuto. En cualquier caso, sé
paciente y respetuoso con quienes dedican su tiempo libre a ayudar a los demás.

Si crees haber encontrado un error pero no estás seguro, lo mejor es informarlo en la lista de correo.
Si estás bastante convencido de haber encontrado un error, de que tu versión está al día en su rama y
de que ya tienes una cuenta de GitHub, no dudes en ir directamente a
<https://github.com/haproxy/haproxy/> y abrir una incidencia con todos los detalles que puedan estar
disponibles. De nuevo, esto es público, así que ten cuidado de no publicar información que puedas
lamentar más adelante. Dado que el seguimiento de incidencias se presenta como un hilo muy largo,
evita pegar volcados muy extensos (unos cientos de líneas o más) y adjúntalos en su lugar.

Si crees que puedes haber encontrado un problema de seguridad, consulta el archivo doc/security.txt.
Explica qué califica y qué no califica como vulnerabilidad en HAProxy y cómo informar de una
vulnerabilidad auténtica de forma privada. La mayoría de los problemas sospechosos resultan ser
errores ordinarios que es mejor notificar como se ha descrito anteriormente.

## Conjunto completo de manuales locales {#complete-local-manual-set}

- [Guía de inicio](/es/haproxy/load-balancing/)
- [Manual de configuración](/es/haproxy/http-fundamentals/)
- [Guía de gestión](/es/haproxy/prerequisites/)

## Procedencia de la edición {#edition-provenance}

- **Edición:** HAProxy 3.4.6-66, instantánea de la documentación de la rama de mantenimiento
- **Última versión estable:** HAProxy 3.4.6, tag `v3.4.6`
- **Commit de origen:** [`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8)
- **Conjunto upstream renderizado:** [docs.haproxy.org/3.4/](https://docs.haproxy.org/3.4/)
- **Copias locales de la licencia:** [aviso de licencia de HAProxy](/third_party/haproxy/LICENSE) y [GPLv2](/third_party/haproxy/GPL-2.0)
