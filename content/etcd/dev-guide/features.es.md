---
title: Características de etcd
weight: 3750
description: uso de las características de etcd
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/features.md"
---

Este documento ofrece una visión general de las características de etcd para ayudar a los usuarios a comprender mejor las características y el proceso de deprecación asociado. Si te interesa saber cómo se desarrollan las características en etcd, consulta estas [guías de desarrollo](https://github.com/etcd-io/etcd/blob/main/Documentation/contributor-guide/features.md).

Las características de etcd se dividen en tres etapas: experimental, estable e insegura. Puedes obtener la lista de características ejecutando `etcd --help`.

## Experimental {#experimental}

Con el fin de obtener retroalimentación temprana, toda característica nueva suele añadirse como una característica experimental. Una característica experimental puede identificarse observando el nombre de la opción, que debe tener `--experimental` como prefijo. Ten en cuenta los siguientes puntos al usar una característica experimental: 
- Puede contener errores debido a la falta de pruebas de usuarios. Activar la característica puede no funcionar como se espera.
- Está desactivada por defecto. 
- El soporte de una característica de este tipo puede retirarse en cualquier momento y sin previo aviso
    - Puede eliminarse en la siguiente versión menor o mayor sin seguir la política de [deprecación de características](#feature-deprecation), salvo que pase a ser estable.
    - El equipo del proyecto agradece que los usuarios informen de cualquier problema relacionado con las características experimentales. Sin embargo, es posible que esos problemas reciban una prioridad más baja en comparación con los problemas relacionados con las características estables.
- Una opción de característica experimental [queda en desuso](#feature-deprecation) cuando alcanza la etapa estable. Los usuarios deberían empezar a usar una opción de característica estable cuanto antes.

## Estable {#stable}

Esta es la etapa más común de las características en etcd. Una característica estable se caracteriza por lo siguiente:
- Tiene soporte como parte de las versiones con soporte de etcd.
- Puede estar activada por defecto.
- La retirada del soporte debe seguir la política de [deprecación de características](#feature-deprecation).

## Inseguras {#unsafe}

Las características inseguras son raras y se enumeran en la sección `Unsafe feature:` de la documentación de uso de etcd. Por defecto, están desactivadas. Deben usarse con precaución siguiendo la documentación. Una característica insegura puede eliminarse en la siguiente versión menor o mayor sin seguir la política de deprecación de características.

## Deprecación de características {#feature-deprecation}

### Experimental {#experimental-1}
Una característica experimental queda en desuso cuando alcanza la etapa estable.
- La documentación de la característica experimental mostrará un mensaje de deprecación con una recomendación de usar una opción de característica estable relacionada. p. ej. `DEPRECATED. Use <feature-name> instead.`
- Una característica en desuso se eliminará en la versión siguiente.

### Estable {#stable-1}
A medida que el proyecto evoluciona, a veces una característica estable debe quedar en desuso y eliminarse. Cuando eso ocurre, 
- La documentación de la característica mostrará un mensaje de advertencia antes de la versión prevista para la deprecación. p. ej. `To be deprecated in <release>.`. Si ya está prevista una característica nueva que reemplace a la característica `To be deprecated`, la documentación también incluirá un mensaje al respecto. p. ej. `Use <feature-name> instead.`.
- La característica quedará en desuso en la versión prevista. En ese momento, la documentación de la característica mostrará un mensaje de deprecación con una recomendación de usar una característica estable relacionada. p. ej. `DEPRECATED. Use <feature-name> instead.`
- Una característica en desuso se eliminará en la versión siguiente.
