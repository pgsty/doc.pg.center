---
title: "Integración con otras herramientas"
linkTitle: "Integración de herramientas"
weight: 150
icon: fas fa-puzzle-piece
description: "Integración de Patroni con herramientas externas de copia de seguridad y orquestación."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni puede integrarse con otras herramientas de tu pila. En esta sección encontrarás una lista de ejemplos que, aunque no es exhaustiva, puede darte ideas sobre cómo Patroni puede integrarse con otras herramientas.

--------

## Barman {#barman}

Patroni incluye una aplicación llamada `patroni_barman` que tiene la lógica para comunicarse con `pg-backup-api`, de modo que puedas ejecutar operaciones de Barman de forma remota.

Esta aplicación tiene actualmente un par de subcomandos: `recover` y `config-switch`.

### patroni_barman recover {#patroni_barman-recover}

El subcomando `recover` puede usarse como método de bootstrap personalizado o como método personalizado de creación de réplicas. Puedes encontrar más información al respecto en [replica_imaging_and_bootstrap](/es/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### patroni_barman config-switch {#patroni_barman-config-switch}

El subcomando `config-switch` está diseñado para usarse como callback `on_role_change` en Patroni. Como ejemplo, supón que estás transmitiendo WALs desde tu primario actual hacia tu host de Barman. En caso de una conmutación por error en el clúster, podrías querer empezar a transmitir WALs desde el nuevo primario. Puedes lograrlo usando `patroni_barman config-switch` como callback `on_role_change`.

> [!NOTE]
> Ese subcomando depende del comando `barman config-switch`, que se encarga de sobrescribir la configuración de un servidor de Barman aplicando un modelo predefinido sobre ella. Este comando está disponible desde Barman 3.10. Consulta la documentación de Barman para más detalles.

Este es un ejemplo de cómo puedes configurar Patroni para aplicar un modelo de configuración en caso de que este nodo de Patroni sea promovido a primario:

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> `patroni_barman config-switch` requiere que tengas tanto Barman como `pg-backup-api` configurados en el host de Barman, de modo que pueda ejecutar un `barman config-switch` remoto a través de la API de copia de seguridad. Además, requiere que tengas preconfigurados los modelos de Barman que se aplicarán. El ejemplo anterior usa un subconjunto de los parámetros disponibles. Puedes obtener más información ejecutando `patroni_barman config-switch --help` y consultando la documentación de Barman.
