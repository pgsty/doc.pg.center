---
title: Inicio rápido
weight: 900
description: ¡Pon etcd en marcha en menos de 5 minutos!
icon: fa-solid fa-rocket
categories: [Tutorial]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
---

Sigue estas instrucciones para instalar, ejecutar y probar localmente un clúster de etcd
de un solo miembro:

 1. Instala etcd a partir de binarios precompilados o del código fuente. Para más detalles, consulta
    [Instalación][Install].

    > [!WARNING]
    > **Importante**: Asegúrate de realizar el último
    > paso de las instrucciones de instalación para verificar que `etcd` está en tu ruta.

 2. Lanza `etcd`:

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **Nota**: La salida producida por `etcd` son
    > [registros](/es/etcd/op-guide/configuration/#logging) &mdash; los registros de nivel info pueden
    > ignorarse.

 3. Desde **otro terminal**, usa `etcdctl` para establecer una clave:

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. Desde el mismo terminal, recupera la clave:

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## ¿Qué viene después? {#whats-next}

Aprende más formas de configurar y usar etcd en las siguientes páginas:

- Si eres desarrollador:
  - Explora la [API][] gRPC.
  - Encuentra [bindings de lenguajes y herramientas][integrations].

- Si eres operador o administrador:
  - Configura un [clúster de varias máquinas][clustering].
  - Aprende a [configurar][configure] etcd.
  - Usa TLS para [proteger un clúster de etcd][security].
  - [Ajusta etcd][tuning].

[api]: /es/etcd/learning/api
[clustering]: /es/etcd/op-guide/clustering
[configure]: /es/etcd/op-guide/configuration
[integrations]: /es/etcd/integrations
[security]: /es/etcd/op-guide/security
[tuning]: /es/etcd/tuning
[Install]: /es/etcd/install/
