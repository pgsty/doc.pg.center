---
title: "13. Consideraciones de seguridad"
linkTitle: "13. Seguridad"
weight: 370
description: "Aislamiento de privilegios, superficie de ataque, capacidades de Linux y funcionamiento seguro"
icon: fa-solid fa-shield-halved
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/security/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 13"
---

HAProxy está diseñado para ejecutarse con privilegios muy limitados. La forma estándar de utilizarlo
consiste en aislarlo en una jaula chroot y rebajar sus privilegios a los de un usuario no root sin
ningún permiso dentro de esa jaula, de modo que si en el futuro se descubriera alguna vulnerabilidad,
su compromiso no afectara al resto del sistema.

Para realizar un chroot, primero es necesario iniciarlo como usuario root. No tiene sentido construir
jaulas chroot a mano para arrancar el proceso en ellas: son laboriosas de construir, nunca se mantienen
correctamente y siempre contienen muchos más errores que el sistema de archivos principal. Y en caso
de compromiso, el intruso puede utilizar el sistema de archivos construido a propósito. Por desgracia,
muchos administradores confunden «iniciar como root» con «ejecutar como root», lo que provoca que el
cambio de uid se haga antes de iniciar haproxy y reduce las restricciones de seguridad efectivas.

HAProxy deberá iniciarse como root para poder:

- ajustar los límites de descriptores de archivos
- enlazarse a números de puerto privilegiados
- enlazarse a una interfaz de red específica
- escuchar de forma transparente una dirección ajena
- aislarse dentro de la jaula chroot
- cambiar a otro UID sin privilegios

HAProxy puede necesitar ejecutarse como root para poder:

- enlazarse a una interfaz para las conexiones salientes
- enlazarse a puertos de origen privilegiados para las conexiones salientes
- enlazarse de forma transparente a una dirección ajena para las conexiones salientes

La mayoría de los usuarios nunca necesitarán el caso «ejecutar como root». Pero el caso «iniciar como
root» cubre la mayoría de los usos.

Una configuración segura tendrá:

- una directiva chroot que apunte a una ubicación vacía y sin ningún permiso de acceso. Esto puede
  prepararse de esta manera en la línea de comandos de UNIX:

```shell
# mkdir /var/empty && chmod 0 /var/empty || echo "Failed"
```

y referenciarla así en la sección global de la configuración de HAProxy:

```text
chroot /var/empty
```

- tanto directivas uid/user como gid/group en la sección global:

```text
user haproxy
group haproxy
```

- un socket de estadísticas cuyo modo, uid y gid estén configurados para corresponderse con el
  usuario y/o el grupo al que se permite acceder a la CLI, de modo que nadie más pueda acceder a él:

```text
stats socket /var/run/haproxy.stat uid hatop gid hatop mode 600
```

## 13.1. Soporte de capacidades de Linux {#section-13-1}

Desde la versión v2.9, haproxy es compatible con las capacidades de Linux. Si el binario se compila
con USE_LINUX_CAP=1, es capaz de conservar las capacidades dadas en la palabra clave «setcap» durante
el cambio del usuario root a un usuario no root.

Desde la versión v3.1, haproxy también comprueba si las capacidades dadas en la palabra clave
«setcap» fueron establecidas por el administrador en el conjunto Permitted de su archivo binario
(syscall capget). Si es el caso, realiza la transición de esas capacidades al conjunto Effective de su
proceso (syscall capset), mientras se ejecuta como usuario no root.

Esto se hizo para evitar todos los casos de uso potenciales en los que haproxy arranca y se ejecuta
como root: modo proxy transparente, enlace a puertos privilegiados.

La palabra clave «setcap» admite las siguientes capacidades de red:

- cap_net_admin: proxying transparente, enlace del socket a una interfaz de red específica, uso de la
  acción set-mark;
- cap_net_raw (subconjunto de cap_net_admin): proxying transparente;
- cap_net_bind_service: enlace del socket a un puerto privilegiado;
- cap_sys_admin: creación de socket en un espacio de nombres de red específico.

Haproxy nunca realiza la transición de estas capacidades de su conjunto Permitted al conjunto
Effective si no están listadas como argumento de «setcap». Consulta más información sobre la palabra
clave «setcap» y las capacidades soportadas en el capítulo 3.1 Gestión de procesos y seguridad de la
guía de configuración.

El administrador puede añadir las capacidades necesarias al conjunto Permitted del archivo binario de
haproxy con el siguiente comando:

Ejemplo:

```haproxy
# setcap cap_net_admin,cap_net_bind_service=p /usr/local/sbin/haproxy
```

Las capacidades añadidas se verán en el conjunto Permitted del proceso después de su arranque. Si las
mismas capacidades son los argumentos de la palabra clave «setcap», también podrán verse en el
conjunto Effective del proceso. Esto puede comprobarse con el siguiente comando:

Ejemplo:

```haproxy
# grep Cap /proc/<haproxy PID>/status
```

    CapInh: 0000000000000000
    CapPrm: 0000000000001400
    CapEff: 0000000000001400
    CapBnd: 000001ffffffffff
    CapAmb: 0000000000000000

Consulta más detalles sobre setcap y los conjuntos de capacidades en las páginas de manual de Linux
(capabilities(7)).

En algunos casos de uso, como el proxying transparente o la creación de socket en un espacio de
nombres de red específico, el analizador del archivo de configuración detecta que se necesitan
cap_net_raw o cap_sys_admin u otras capacidades soportadas. Entonces, durante la etapa de
inicialización, el proceso haproxy comprueba si esas capacidades pueden ponerse en su conjunto
Effective. Si no es posible debido a un fallo de la syscall capget o capset (restricciones impuestas
a las syscalls por ciertos módulos de seguridad como SELinux, Seccomp, etc.), el proceso emite avisos
de diagnóstico (arranca con -dD).

Debido al soporte de muchas plataformas diferentes con configuraciones de sistema distintas, le es
imposible al analizador deducir del archivo de configuración si se van a utilizar puertos
privilegiados. Así pues, en caso de privilegios insuficientes (ejecución como no root) el proceso
terminará únicamente con un mensaje de alerta como el siguiente. Es responsabilidad del usuario
verificar de nuevo su configuración y el conjunto de capacidades del binario de haproxy.

Ejemplo:

```shell
$ haproxy -dD -f haproxy.cfg
...
[ALERT]    (96797): Binding [haproxy.cfg:36] for frontend fe: cannot bind socket (Permission denied) for [0.0.0.0:80]
[ALERT]    (96797): [haproxy.main()] Some protocols failed to start their listeners! Exiting.
```
