---
title: "Consideraciones de seguridad"
weight: 160
icon: fa-solid fa-lock
description: "Consideraciones de seguridad para el DCS, la REST API y el manejo de credenciales."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Un clúster de Patroni tiene dos interfaces que deben protegerse del acceso no autorizado: el almacenamiento de configuración distribuido (DCS) y la REST API de Patroni.

--------

## Protección del DCS {#protecting-dcs}

Tanto Patroni como [patronictl](/es/patroni/patronictl#patronictl) almacenan y recuperan datos en/desde el DCS.

Incluso cuando el DCS no contiene información sensible, permite cambiar parte de la configuración de Patroni/Postgres. Por lo tanto, lo primero que debe protegerse es el propio DCS.

Los detalles de la protección dependen del tipo de DCS utilizado. Los parámetros de autenticación y cifrado (tokens/basic-auth/certificados de cliente) para los tipos de DCS admitidos se tratan en los [ajustes](/es/patroni/config/yaml#yaml).

La recomendación general es habilitar TLS para toda la comunicación con el DCS.

--------

## Protección de la REST API {#protecting-the-rest-api}

Proteger la REST API es una tarea más complicada.

La REST API de Patroni es utilizada por el propio Patroni durante la carrera por el liderazgo, por la herramienta [patronictl](/es/patroni/patronictl#patronictl) para ejecutar conmutaciones por error/switchovers/reinicializaciones/reinicios/recargas, por HAProxy o cualquier otro tipo de balanceador de carga para realizar comprobaciones de estado HTTP y, por supuesto, también podría usarse para monitorización.

Desde el punto de vista de la seguridad, la REST API contiene endpoints seguros (peticiones `GET`, que solo recuperan información) y endpoints inseguros (peticiones `PUT`, `POST`, `PATCH` y `DELETE`, que cambian el estado de los nodos).

Los endpoints inseguros pueden protegerse con basic-auth HTTP estableciendo los parámetros `restapi.authentication.username` y `restapi.authentication.password`. No hay forma de proteger los endpoints seguros sin habilitar TLS.

Cuando el TLS para la REST API está habilitado y existe una PKI establecida, es posible la autenticación mutua del servidor y del cliente de la API para todos los endpoints.

Los parámetros de la sección `restapi` habilitan la autenticación TLS del cliente hacia el servidor. Según el valor del parámetro `verify_client`, el servidor de la API exige una verificación exitosa del certificado del cliente tanto para las llamadas seguras como para las inseguras de la API (`verify_client: required`), o solo para las llamadas inseguras (`verify_client: optional`), o para ninguna llamada (`verify_client: none`).

Los parámetros de la sección `ctl` habilitan la autenticación TLS del servidor hacia el cliente (la herramienta [patronictl](/es/patroni/patronictl#patronictl), que usa la misma configuración que patroni). Establece `insecure: true` para deshabilitar la verificación del certificado del servidor por parte del cliente. Consulta los [ajustes](/es/patroni/config/yaml#patronictl_settings) para una descripción detallada de los parámetros del cliente TLS.

Proteger la base de datos PostgreSQL propiamente dicha del acceso no autorizado está fuera del alcance de este documento y se trata en <https://www.postgresql.org/docs/current/client-authentication.html>
