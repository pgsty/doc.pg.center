---
title: Compuertas de funcionalidades
weight: 1175
icon: fa-solid fa-toggle-on
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
---

<!-- overview -->
Esta página contiene una visión general de las diversas compuertas de funcionalidades (feature gates) que un administrador
puede especificar en etcd.

Consulta las [etapas de funcionalidades](#feature-stages) para ver una explicación de las etapas de una funcionalidad.

<!-- body -->
## Visión general {#overview}

Las compuertas de funcionalidades son un conjunto de pares clave=valor que describen las funcionalidades de etcd.
Puedes activar o desactivar estas funcionalidades usando la opción de línea de comandos `--feature-gates`
en etcd.

etcd te permite activar o desactivar un conjunto de compuertas de funcionalidades.
Usa la opción `-h` para ver el conjunto completo de compuertas de funcionalidades.
Para definir compuertas de funcionalidades, usa la opción `--feature-gates` asignada a una lista de pares de funcionalidades en la línea de comandos:

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

O especifica `feature-gates` en el archivo de configuración YAML:

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### Cambio en la estructura `embed.Config` {#change-in-embedetcdserver-struct}

En 3.6, el campo `ServerFeatureGate` se añade a `embed.Config`, y debería sustituir los campos experimentales que se listan a continuación:

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### Compuertas de funcionalidades para funcionalidades Alpha o Beta {#feature-gates-for-alpha-or-beta-features}

Las tablas siguientes son un resumen de las compuertas de funcionalidades que puedes establecer en
etcd.

| Funcionalidad                    | Por defecto | Etapa  | Detalles                                                                                                                              |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck                 | false   | Alpha |Permite que el líder compruebe periódicamente los hashes de compactación de las réplicas.                                                                           |
| InitialCorruptCheck              | false   | Alpha |Activa la comprobación de corrupción de datos antes de atender cualquier tráfico de clientes/pares.                                                                              |
| LeaseCheckpoint                  | false   | Alpha |Permite que el líder envíe puntos de control regulares a otros miembros para evitar el restablecimiento del TTL restante en un cambio de líder.                                              |
| LeaseCheckpointPersist           | false   | Alpha |Activa la persistencia del remainingTTL para evitar la renovación automática indefinida de concesiones de larga duración.                                                                         |
| SetMemberLocalAddr               | false   | Alpha |Activa el uso de la primera dirección local especificada en initial-advertise-peer-urls que no sea de loopback como dirección local al comunicarse con un par.      |
| StopGRPCServiceOnDefrag          | false   | Alpha |Permite que el servicio gRPC de etcd deje de atender solicitudes de clientes durante la desfragmentación.                                                                      |
| TxnModeWriteWithSharedBuffer     | true    | Beta  |Permite que la transacción de escritura use un búfer compartido en sus operaciones de comprobación de solo lectura.                                                                                |

## Uso de una funcionalidad {#using-a-feature}

### Etapas de las funcionalidades {#feature-stages}

Una funcionalidad puede estar en la etapa *Alpha*, *Beta*, *GA* o *Deprecated*.
Una funcionalidad *Alpha* significa:

* Desactivada por defecto.
* Puede tener errores. Activar la funcionalidad puede exponer errores.
* El soporte de la funcionalidad puede retirarse en cualquier momento y sin previo aviso.
* La API puede cambiar de formas incompatibles en una versión posterior del software y sin previo aviso.
* Recomendada solo para clústeres de prueba de corta duración, debido al mayor
  riesgo de errores y a la falta de soporte a largo plazo.

Una funcionalidad *Beta* significa:

* Activada por defecto.
* La funcionalidad está bien probada. Activar la funcionalidad se considera seguro.
* El soporte de la funcionalidad en su conjunto no se retirará, aunque los detalles pueden cambiar.
* Recomendada solo para usos no críticos para el negocio, debido a la posibilidad de
  descubrir nuevos errores difíciles de detectar mediante una adopción más amplia.

> [!NOTE]
> ¡Prueba las funcionalidades *Beta* y da tu opinión sobre ellas!
> Después de que salgan de la fase beta, puede que no nos resulte práctico hacer más cambios.

Una funcionalidad *General Availability* (GA) también se denomina funcionalidad *estable*. Significa:

* La funcionalidad está siempre activada; no puedes desactivarla.
* La compuerta de funcionalidad correspondiente ya no es necesaria.
* Las versiones estables de las funcionalidades aparecerán en el software publicado durante muchas versiones posteriores.

Una funcionalidad *Deprecated* significa:

* La compuerta de funcionalidad ya no se utiliza.
* La funcionalidad ha pasado a GA o ha sido eliminada.
