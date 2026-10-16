---
title: Convenciones de registro
weight: 1600
description: Categorías de niveles de registro
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/logging.md"
---

etcd usa la biblioteca [zap][zap] para registrar la salida de la aplicación, clasificada en *niveles*. El nivel de un mensaje de registro se determina según estas convenciones:

* Los registros de DebugLevel suelen ser voluminosos y habitualmente están desactivados en producción.
  * Ejemplos:
    * Enviar un mensaje normal a un par remoto
    * Escribir una entrada de registro en el disco

* InfoLevel es la prioridad de registro predeterminada.
  * Ejemplos:
    * Configuración al iniciar
    * Comenzar a realizar una instantánea
    * Añadir un nodo nuevo al clúster
    * Añadir un usuario nuevo al subsistema de autenticación

* Los registros de WarnLevel son más importantes que los de Info, pero no requieren revisión humana individual.
  * Ejemplos:
    * Fallo al enviar un mensaje de Raft a un par remoto
    * Fallo al recibir el mensaje de latido dentro del tiempo de espera de elección configurado

* Los registros de ErrorLevel son de alta prioridad. Si una aplicación funciona sin problemas, no debería generar ningún registro de nivel de error.
  * Ejemplos:
    * Fallo al asignar espacio en disco para el WAL

* PanicLevel registra un mensaje y luego provoca un panic.
  * Ejemplos:
    * Fallo al codificar los mensajes de Raft

* FatalLevel registra un mensaje y luego llama a os.Exit(1).
  * Ejemplos:
    * Fallo al guardar la instantánea de Raft

[zap]: https://github.com/uber-go/zap
