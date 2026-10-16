---
title: Control de acceso basado en roles
weight: 4100
description: Una guía básica de autenticación y control de acceso basado en roles
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/authentication/rbac.md"
---

## Visión general {#overview}

La autenticación se añadió en etcd 2.1. La API v3 de etcd modificó ligeramente la API y la interfaz de usuario de la función de autenticación para adaptarse mejor al nuevo modelo de datos. Esta guía está pensada para ayudar a los usuarios a configurar la autenticación básica y el control de acceso basado en roles en etcd v3.

## Usuarios y roles especiales {#special-users-and-roles}

Existe un usuario especial, `root`, y un rol especial, `root`.

### Usuario `root` {#user-root}

El usuario `root`, que tiene acceso completo a etcd, debe crearse antes de activar la autenticación. La idea detrás del usuario `root` es servir para fines administrativos: gestionar roles y usuarios ordinarios. El usuario `root` debe tener el rol `root` y puede modificar cualquier cosa dentro de etcd.

### Rol `root` {#role-root}

El rol `root` puede otorgarse a cualquier usuario, además del usuario root. Un usuario con el rol `root` tiene tanto acceso global de lectura y escritura como permiso para actualizar la configuración de autenticación del clúster. Además, el rol `root` otorga privilegios para el mantenimiento general del clúster, incluidos la modificación de la composición del clúster, la desfragmentación del almacén y la toma de instantáneas.

## Trabajo con usuarios {#working-with-users}

El subcomando `user` de `etcdctl` gestiona todo lo relacionado con las cuentas de usuario.

Se puede obtener una lista de usuarios con:

```
$ etcdctl user list
```

Crear un usuario es tan sencillo como

```
$ etcdctl user add myusername
```

Al crear un nuevo usuario se solicitará una nueva contraseña. La contraseña puede suministrarse desde la entrada estándar cuando se proporciona la opción `--interactive=false`. También puede usarse `--new-user-password` para suministrar la contraseña.

También es posible crear un usuario que no pueda autenticarse con contraseña, como se muestra a continuación:

```
$ etcdctl user add myusername --no-password
```

Un usuario así solo puede [autenticarse con el Common Name de TLS](#using-tls-common-name).

> [!NOTE]
> etcd no admite la autenticación con una contraseña vacía mediante `--user username:`. Por ejemplo, un usuario creado con una contraseña vacía, como `etcdctl user add anonymous:''`, no puede autenticarse mediante solicitudes de nombre de usuario/contraseña, y solicitudes como `etcdctl --user anonymous: get foo` fallan con `user name is empty`.

Los roles pueden otorgarse y revocarse a un usuario con:

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

Los ajustes del usuario pueden inspeccionarse con:

```
$ etcdctl user get myusername
```

Y la contraseña de un usuario puede cambiarse con

```
$ etcdctl user passwd myusername
```

Al cambiar la contraseña se solicitará de nuevo una nueva contraseña. La contraseña puede suministrarse desde la entrada estándar cuando se proporciona la opción `--interactive=false`.

Elimina una cuenta con:
```
$ etcdctl user delete myusername
```


## Trabajo con roles {#working-with-roles}

El subcomando `role` de `etcdctl` gestiona todo lo relacionado con los controles de acceso de roles concretos, tal como se otorgaron a usuarios individuales.

Lista los roles con:

```
$ etcdctl role list
```

Crea un nuevo rol con:

```
$ etcdctl role add myrolename
```

Un rol no tiene contraseña; simplemente define un nuevo conjunto de derechos de acceso.

A los roles se les otorga acceso a una clave única o a un rango de claves.

El rango puede especificarse como un intervalo [start-key, end-key) donde start-key debe ser lexicográficamente menor que end-key en orden alfabético.

El acceso puede otorgarse para lectura, escritura o ambos, como en los siguientes ejemplos:

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

Para ver qué se ha otorgado, podemos consultar el rol en cualquier momento:

```
$ etcdctl role get myrolename
```

La revocación de permisos se realiza de la misma manera lógica:

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

Lo mismo ocurre con eliminar un rol por completo:

```
$ etcdctl role delete myrolename
```

## Activación de la autenticación {#enabling-authentication}

Los pasos mínimos para activar la autenticación son los siguientes. El administrador puede configurar los usuarios y los roles antes o después de activar la autenticación, según sus preferencias.

Asegúrate de que el usuario root esté creado:

```
$ etcdctl user add root
Password of root:
```

Activa la autenticación:

```
$ etcdctl auth enable
```

Después de esto, etcd se ejecuta con la autenticación activada. Para desactivarla por cualquier motivo, usa el comando recíproco:

```
$ etcdctl --user root:rootpw auth disable
```

## Alcance de seguridad de la autenticación {#security-scope-of-authentication}

Cuando se activa la autenticación con `etcdctl auth enable`, esta protege las operaciones de la API gRPC de V3 (get, put, delete, watch, etc.).

Los endpoints HTTP `/metrics` y `/health` funcionan en un gestor separado y **no** están protegidos por la autenticación RBAC de V3. Este diseño permite a Prometheus y a los balanceadores de carga recolectar las métricas sin requerir autenticación gRPC, a la vez que se siguen protegiendo los datos clave-valor.

Para proteger estos endpoints de observabilidad:

- Activa mTLS con `--cert-file`, `--key-file` y `--client-cert-auth`
- O vincula las métricas a una interfaz privada usando `--listen-metrics-urls`
- O usa políticas de red o reglas de firewall para restringir el acceso

## Uso de `etcdctl` para autenticarse {#using-etcdctl-to-authenticate}

`etcdctl` admite una opción similar a la de `curl` para la autenticación.

```
$ etcdctl --user user:password get foo
```

La contraseña puede obtenerse desde un mensaje interactivo:

```
$ etcdctl --user user get foo
```

La contraseña también puede obtenerse desde la opción de línea de comandos `--password`:

```
$ etcdctl --user user --password password get foo
```


Aparte de esto, todos los comandos de `etcdctl` siguen siendo los mismos. Los usuarios y roles todavía pueden crearse y modificarse, pero requieren autenticación por parte de un usuario con el rol root.

## Uso del Common Name de TLS {#using-tls-common-name}
A partir de la versión v3.2, si un servidor etcd se inicia con la opción `--client-cert-auth=true`, el campo Common Name (CN) del certificado TLS del cliente se usará como usuario de etcd. En este caso, el common name autentica al usuario y el cliente no necesita contraseña. Ten en cuenta que si se cumplen ambas condiciones: 1. se pasa `--client-cert-auth=true` y el cliente proporciona el CN, y 2. el cliente proporciona nombre de usuario y contraseña, la autenticación basada en nombre de usuario y contraseña tiene prioridad. Ten en cuenta que esta función no puede usarse con gRPC-proxy ni con gRPC-gateway. Esto se debe a que gRPC-proxy termina el TLS procedente de su cliente, de modo que todos los clientes comparten un certificado del proxy. gRPC-gateway usa internamente una conexión TLS para transformar las solicitudes HTTP en solicitudes gRPC, por lo que comparte la misma limitación. En consecuencia, los clientes no pueden proporcionar correctamente su CN al servidor. gRPC-proxy provocará un error y se detendrá si un certificado dado tiene un CN no vacío. gRPC-proxy devuelve un error que indica que el cliente tiene un CN no vacío en su certificado.

## Notas sobre la robustez de la contraseña {#notes-on-password-strength}
`etcdctl` y la API de etcd no exigen una longitud de contraseña específica durante las operaciones de creación de usuarios o de actualización de contraseñas. Es responsabilidad del administrador hacer cumplir estos requisitos. Para evitar los riesgos de seguridad relacionados con la robustez de las contraseñas, se pueden utilizar la [autenticación basada en el Common Name de TLS](#using-tls-common-name) y los usuarios creados con la opción `--no-password`.
