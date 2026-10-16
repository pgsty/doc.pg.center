---
title: "Funciones estándar"
linkTitle: "Funciones estándar"
weight: 50
description: "Extracciones de muestras, mapas, ACL, conmutación de contenido, tablas de persistencia, reescritura y protección de servidores"
icon: fa-solid fa-sliders
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/intro/standard-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 3.4–3.4.8"
---

En esta sección se enumeran algunas funciones que se usan con mucha frecuencia en HAProxy pero que no
necesariamente están presentes en otros balanceadores de carga.

## 3.4.1. Funciones estándar : Muestreo y conversión de información {#section-3-4-1}

HAProxy es compatible con el muestreo de información mediante un amplio conjunto de «funciones de
extracción de muestras» (sample fetch). El principio consiste en extraer fragmentos de información
conocidos como muestras, para su uso inmediato. Esto se utiliza para la persistencia, para construir
condiciones, para producir información en los registros o para enriquecer encabezados HTTP.

Las muestras pueden extraerse de diversas fuentes:

- constantes: enteros, cadenas, direcciones IP, bloques binarios;

- el proceso: fecha, variables de entorno, estado del servidor/frontend/backend/proceso,
  recuentos/tasas de bytes/conexiones, longitud de la cola, generador aleatorio, ...

- variables: variables por sesión, por solicitud, por respuesta;

- la conexión del cliente: direcciones y puertos de origen y destino, y todos los contadores de
  estadísticas relacionados;

- la sesión SSL del cliente: protocolo, versión, algoritmo, cifrado, tamaño de clave, ID de sesión,
  todos los campos de los certificados del cliente y del servidor, número de serie del certificado,
  SNI, ALPN, NPN, soporte del cliente de ciertas extensiones;

- contenido de los búferes de solicitud y respuesta: carga útil arbitraria en desplazamiento/
  longitud, longitud de los datos, cookie RDP, decodificación del tipo SSL hello, decodificación del
  SNI TLS;

- HTTP (solicitud y respuesta): método, URI, ruta, argumentos de la cadena de consulta, código de
  estado, valores de encabezados, valor posicional de encabezado, cookies, capturas, autenticación,
  elementos del cuerpo;

Una muestra puede luego pasar por una serie de operadores conocidos como «convertidores» para
someterla a alguna transformación. Un convertidor consume una muestra y produce una nueva,
posiblemente de un tipo completamente distinto. Por ejemplo, un convertidor puede utilizarse para
devolver solo la longitud entera de la cadena de entrada, o podría convertir una cadena a mayúsculas.
Puede aplicarse en serie un número arbitrario de convertidores a una muestra antes de su uso final.
Entre todos los convertidores de muestras disponibles, los siguientes son los más utilizados:

- operadores aritméticos y lógicos: permiten realizar cálculos avanzados sobre los datos de entrada,
  como calcular proporciones, porcentajes o simplemente convertir de una unidad a otra;

- las máscaras de dirección IP son útiles cuando ciertas direcciones deben agruparse por redes más
  grandes;

- representación de datos: decodificación de URL, base64, hexadecimal, cadenas JSON, hashing;

- conversión de cadenas: extraer subcadenas en posiciones fijas, de longitud fija, extraer campos
  específicos alrededor de ciertos delimitadores, extraer determinadas palabras, cambiar mayúsculas y
  minúsculas, aplicar sustitución basada en expresiones regulares;

- conversión de fechas: convertir al formato de fecha HTTP, convertir de hora local a UTC y
  viceversa, añadir o eliminar un desplazamiento;

- buscar una entrada en una tabla de persistencia para encontrar estadísticas o el servidor asignado;

- conversión de clave a valor basada en mapas a partir de un archivo (usada sobre todo para
  geolocalización).

## 3.4.2. Funciones estándar : Mapas {#section-3-4-2}

Los mapas son un tipo potente de convertidor que consiste en cargar en memoria, en el arranque, un
archivo de dos columnas, para luego buscar cada muestra de entrada en la primera columna y devolver
bien el patrón correspondiente de la segunda columna si se encontró la entrada, bien un valor por
defecto. Como la información de salida también es una muestra, esta puede a su vez someterse a otras
transformaciones, incluidas otras búsquedas en mapas. Los mapas se usan con más frecuencia para
traducir la dirección IP del cliente a un número de AS o a un código de país, ya que admiten la
coincidencia más larga para direcciones de red, pero pueden utilizarse para otros muchos fines.

Parte de su fuerza proviene de que pueden actualizarse al vuelo, ya sea desde la CLI o desde ciertas
acciones que usan otras muestras, lo que les permite almacenar y recuperar información entre accesos
sucesivos. Otra fuerza proviene de la indexación basada en árboles binarios, que los hace extremadamente
rápidos incluso cuando contienen cientos de miles de entradas, volviendo la geolocalización muy barata
y fácil de configurar.

## 3.4.3. Funciones estándar : ACL y condiciones {#section-3-4-3}

La mayoría de las operaciones en HAProxy pueden hacerse condicionales. Las condiciones se construyen
combinando varias ACL mediante operadores lógicos (AND, OR, NOT). Cada ACL es una serie de pruebas
basadas en los elementos siguientes:

- un método de extracción de muestra para recuperar el elemento a probar;

- una serie opcional de convertidores para transformar el elemento;

- una lista de patrones con los que comparar;

- un método de coincidencia para indicar cómo comparar los patrones con la muestra

Por ejemplo, la muestra puede tomarse del encabezado HTTP «Host», luego convertirse a minúsculas y a
continuación compararse con una serie de patrones regex usando el método de coincidencia regex.

Técnicamente, las ACL están construidas sobre el mismo núcleo que los mapas: comparten exactamente la
misma estructura interna, los mismos métodos de coincidencia de patrones y el mismo rendimiento. La
única diferencia real es que, en lugar de devolver una muestra, solo devuelven «encontrado» o «no
encontrado». En cuanto al uso, los patrones de ACL pueden declararse en línea en el archivo de
configuración y no requieren un archivo propio. Las ACL pueden recibir un nombre para facilitar su uso
o para hacer las configuraciones comprensibles. Una ACL con nombre puede declararse varias veces y
evaluará todas sus definiciones por turnos hasta que una coincida.

Se proporcionan unos 13 métodos de coincidencia de patrones distintos, entre ellos máscara de
dirección IP, rangos de enteros, subcadenas y regex. Funcionan como funciones y, igual que en
cualquier lenguaje de programación, solo se evalúa lo necesario: cuando una condición que implica un
OR ya es verdadera, las siguientes no se evalúan, y de igual modo, cuando una condición que implica un
AND ya es falsa, el resto de la condición no se evalúa.

No existe ningún límite práctico al número de ACL declaradas, y se proporcionan algunas de uso común.
Sin embargo, la experiencia ha mostrado que las configuraciones que usan muchas ACL con nombre son
bastante difíciles de depurar y que a veces es más fácil usar ACL anónimas en línea, pues requiere
menos referencias fuera del ámbito que se está analizando.

## 3.4.4. Funciones estándar : Conmutación de contenido {#section-3-4-4}

HAProxy implementa un mecanismo conocido como conmutación basada en contenido. El principio es que una
conexión o solicitud llega a un frontend, luego se procesa la información transportada por esa
solicitud o conexión, y en ese punto es posible escribir condiciones basadas en ACL que usen esa
información para decidir qué backend procesará la solicitud. Así, el tráfico se dirige a un backend u
otro según el contenido de la solicitud. El ejemplo más común consiste en usar el encabezado Host y/o
elementos de la ruta (subdirectorios o extensiones de nombre de archivo) para decidir si una solicitud
HTTP apunta a un objeto estático o a la aplicación, y enrutar el tráfico de los objetos estáticos a un
backend formado por servidores rápidos y ligeros, y todo el tráfico restante a un servidor de
aplicaciones más complejo, constituyendo así una solución de hosting virtual de grano fino. Esto
resulta muy práctico para hacer coexistir varias tecnologías como parte de una solución más global.

Otro caso de uso de la conmutación de contenido consiste en usar distintos algoritmos de balanceo de
carga según diversos criterios. Una caché puede usar un hash de URI mientras que una aplicación usaría
round-robin.

Por último, y no menos importante, permite que varios clientes usen una pequeña parte de un recurso
común imponiendo límites de conexión por backend (y por tanto por cliente).

Las reglas de conmutación de contenido escalan muy bien, aunque su rendimiento puede depender del
número y la complejidad de las ACL en uso. Pero también es posible escribir reglas de conmutación de
contenido dinámicas donde un valor de muestra se convierte directamente en un nombre de backend, sin
usar ACL en absoluto. Se ha informado de que tales configuraciones funcionan bien en producción al
menos con 300000 backends.

## 3.4.5. Funciones estándar : Tablas de persistencia {#section-3-4-5}

Las tablas de persistencia (stick-tables) se usan habitualmente para almacenar información de
persistencia, es decir, para conservar una referencia al servidor al que se dirigió a un determinado
visitante. La clave es entonces el identificador asociado al visitante (su dirección de origen, el ID
SSL de la conexión, una cookie HTTP o RDP, el número de cliente extraído de la URL o de la carga útil,
...) y el valor almacenado es entonces el identificador del servidor.

Las tablas de persistencia pueden usar 3 tipos distintos de muestras para sus claves: enteros, cadenas
y direcciones. Solo puede referenciarse una tabla de persistencia en un proxy, y esta se designa en
todas partes con el nombre del proxy. Se puede hacer seguimiento de hasta 8 claves en paralelo. El
identificador del servidor se fija durante el procesamiento de la solicitud o de la respuesta, una vez
que se conocen tanto la clave como el servidor.

El contenido de las tablas de persistencia puede replicarse en modo activo-activo con otros nodos
HAProxy conocidos como «peers», así como con el nuevo proceso durante una operación de recarga, de
modo que todos los nodos de balanceo de carga compartan la misma información y tomen la misma decisión
de enrutamiento si las solicitudes de los clientes se reparten entre varios nodos.

Dado que las tablas de persistencia se indexan por lo que permite reconocer a un cliente, a menudo
también se usan para almacenar información adicional, como estadísticas por cliente. Las estadísticas
adicionales ocupan algo de espacio extra y deben declararse explícitamente. Los tipos de estadísticas
que pueden almacenarse incluyen el ancho de banda de entrada y de salida, el número de conexiones
simultáneas, el ritmo y el recuento de conexiones durante un periodo, la cantidad y la frecuencia de
los errores, ciertas etiquetas y contadores específicos, etcétera. Para permitir conservar tal
información sin estar obligado a fijarse a un servidor dado, se implementa una función especial de
«seguimiento» (tracking) que permite seguir hasta 3 claves simultáneas de tablas distintas al mismo
tiempo, con independencia de las reglas de persistencia. Cada estadística almacenada puede buscarse,
volcarse y borrarse desde la CLI, lo que suma capacidades de diagnóstico en tiempo real.

Aunque este mecanismo puede usarse para dar un trato superior a un visitante recurrente o para ajustar
la calidad de servicio entregada según un comportamiento bueno o malo, se usa sobre todo para luchar
contra el abuso del servicio y, más en general, contra los DDoS, pues permite construir modelos
complejos para detectar ciertos comportamientos maliciosos a una alta velocidad de procesamiento.

## 3.4.6. Funciones estándar : Cadenas con formato {#section-3-4-6}

Hay muchos lugares donde HAProxy necesita manipular cadenas de caracteres, como los registros, las
redirecciones, las adiciones de encabezados, etcétera. Para proporcionar la máxima flexibilidad, se
introdujo la noción de cadenas con formato, inicialmente con fines de registro, lo que explica que aún
se llame «log-format». Estas cadenas contienen caracteres de escape que permiten introducir en ellas
diversos datos dinámicos, incluidas variables y expresiones de extracción de muestras, e incluso
ajustar la codificación mientras el resultado se convierte en cadena (por ejemplo, añadir comillas).
Esto ofrece una forma potente de construir contenidos de encabezados, de construir datos de respuesta
o incluso plantillas de respuesta, o de personalizar líneas de registro. Además, para seguir siendo
sencillo al construir las cadenas más comunes, se proporcionan unas 50 etiquetas especiales como
atajos para información usada con frecuencia en los registros.

## 3.4.7. Funciones estándar : Reescritura y redirección HTTP {#section-3-4-7}

Instalar un balanceador de carga delante de una aplicación que nunca fue diseñada para ello puede ser
una tarea difícil sin las herramientas adecuadas. Una de las operaciones más solicitadas en este caso
consiste en ajustar los encabezados de las solicitudes y respuestas para que el balanceador de carga
aparezca como el servidor de origen y para corregir la información incrustada fija en el código. Esto
comporta cambiar la ruta en las solicitudes (algo totalmente desaconsejado), modificar el campo de
encabezado Host, modificar el campo de encabezado de respuesta Location en las redirecciones, modificar
la ruta y el atributo de dominio de las cookies, etcétera. También ocurre que cierto número de
servidores son algo verbosos y tienden a filtrar demasiada información en la respuesta, lo que los
hace más vulnerables a ataques dirigidos. Aunque en teoría no es papel de un balanceador de carga
limpiar esto, en la práctica está situado en el mejor lugar de la infraestructura para garantizar que
todo quede limpio.

De manera similar, a veces el balanceador de carga tendrá que interceptar algunas solicitudes y
responder con una redirección a una nueva URL de destino. Aunque algunas personas tienden a confundir
las redirecciones con la reescritura, son dos conceptos completamente distintos, ya que la reescritura
hace que el cliente y el servidor vean cosas diferentes (y discrepen sobre la ubicación de la página
que se visita), mientras que las redirecciones piden al cliente que visite la nueva URL para que vea
la misma ubicación que el servidor.

Para esto, HAProxy admite diversas posibilidades de reescritura y redirección, entre ellas:

- reescritura de URL y encabezados basada en regex en solicitudes y respuestas. Las regex son la
  herramienta más comúnmente usada para modificar valores de encabezados, pues son fáciles de
  manipular y bien comprendidas;

- los encabezados también pueden añadirse, eliminarse o reemplazarse basándose en cadenas con formato,
  de modo que sea posible pasar información en ellos (por ejemplo, el algoritmo y el cifrado TLS del
  lado del cliente);

- las redirecciones HTTP pueden usar cualquier código 3xx hacia un URI relativo, absoluto o
  completamente dinámico (cadena con formato);

- las redirecciones HTTP también admiten algunas opciones adicionales, como establecer o borrar una
  cookie específica, descartar la cadena de consulta, añadir una barra si falta, etcétera;

- una potente directiva «return» permite personalizar cada parte de una respuesta, como el estado, los
  encabezados o el cuerpo, usando contenidos dinámicos o incluso archivos de plantilla.

- todas las operaciones admiten condiciones basadas en ACL;

## 3.4.8. Funciones estándar : Protección de servidores {#section-3-4-8}

HAProxy hace mucho por maximizar la disponibilidad del servicio y, para ello, dedica grandes esfuerzos
a proteger los servidores contra la sobrecarga y los ataques. El primer punto, y el más importante, es
que solo las solicitudes completas y válidas se reenvían a los servidores. La razón inicial es que
HAProxy necesita encontrar los elementos del protocolo que necesita para mantenerse sincronizado con
el flujo de bytes, y la segunda razón es que, hasta que la solicitud está completa, no hay forma de
saber si algunos elementos cambiarán su semántica. El beneficio directo de esto es que los servidores
no quedan expuestos a solicitudes inválidas o incompletas. Esta es una protección muy eficaz contra
los ataques slowloris, que casi no tienen impacto en HAProxy.

Otro punto importante es que HAProxy contiene búferes para almacenar solicitudes y respuestas, y que,
al enviar una solicitud al servidor solo cuando está completa y al leer la respuesta completa muy
rápidamente desde la red local, la conexión del lado del servidor se usa durante un tiempo muy corto,
lo que preserva al máximo los recursos del servidor.

Una extensión directa de esto es que HAProxy puede limitar artificialmente el número de conexiones
simultáneas o de solicitudes pendientes hacia un servidor, lo que garantiza que el servidor nunca se
sobrecargará, incluso si funciona continuamente al 100% de su capacidad durante los picos de tráfico.
Todas las solicitudes excedentes simplemente se pondrán en cola para procesarse cuando se libere un
hueco. Al final, este enorme ahorro de recursos tan a menudo consigue unos tiempos de respuesta del
servidor tan buenos que acaba siendo de hecho más rápido que sobrecargando el servidor. Las solicitudes
en cola pueden reexpedirse a otros servidores, o incluso abortarse en la cola cuando el cliente aborta,
lo que también protege a los servidores contra el «efecto recarga», donde cada clic en «recargar» de un
visitante en una página que carga lentamente suele inducir una nueva solicitud y mantener el servidor
en un estado de sobrecarga.

El mecanismo de arranque progresivo (slow-start) también protege a los servidores que se reinician
frente a niveles altos de tráfico mientras todavía finalizan su arranque o compilan algunas clases.

En cuanto a la protección a nivel de protocolo, es posible relajar el analizador HTTP para aceptar
solicitudes o respuestas no conformes con el estándar pero inofensivas, e incluso corregirlas. Esto
permite que las aplicaciones defectuosas sean accesibles mientras se desarrolla una corrección. En
paralelo, los mensajes que infringen el protocolo se capturan completamente con un informe detallado que ayuda a los
desarrolladores a localizar el problema en la aplicación. Las violaciones de protocolo más peligrosas
se detectan, se tratan y se corrigen adecuadamente. Por ejemplo, las solicitudes o respuestas
malformadas con dos encabezados Content-length se corrigen si los valores son exactamente iguales, o
se rechazan si difieren, ya que entonces se convierte en un problema de seguridad. La inspección de
protocolo no se limita a HTTP; también está disponible para otros protocolos como TLS o RDP.

Cuando se detecta una violación de protocolo o un ataque, existen diversas opciones para responder al
usuario, como devolver el clásico «HTTP 400 bad request», cerrar la conexión con un reset TCP, o
simular un error tras un largo retraso («tarpit») para confundir al atacante. Todas estas medidas
contribuyen a proteger los servidores desanimando al cliente infractor de proseguir un ataque que se
vuelve muy caro de mantener.

HAProxy también propone opciones más avanzadas para protegerse contra fugas accidentales de datos y
cruces de sesión. No solo puede registrar respuestas sospechosas del servidor, sino que también
registrará y, opcionalmente, bloqueará una respuesta que pueda afectar a la confidencialidad de un
visitante dado. Un ejemplo de esto es una cookie almacenable en caché que aparece en una respuesta
almacenable en caché y que puede provocar que una caché intermedia la entregue a otro visitante,
causando un uso compartido accidental de la sesión.
