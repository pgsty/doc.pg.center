---
title: "Cómo realizar la elección de líder en un clúster etcd"
description: Pasos para realizar una elección de líder a través del cliente etcdctl
weight: 900
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## Prerrequisitos {#prerequisites}

- Asegúrate de que [`etcd`](/es/etcd/install/) y [`etcdctl`](/es/etcd/install/) estén instalados.
- Comprueba que haya un clúster etcd activo.

## Realizar la elección de líder {#conduct-leader-election}

El comando `etcdctl` se usa para realizar elecciones de líder en un clúster etcd. Garantiza que solo un cliente pueda convertirse en líder a la vez.

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### Opciones {#options}

- `--endpoints : $ENDPOINTS`

Dirección de cada uno de los miembros del clúster etcd.

- `election-name` cadena de caracteres

Identificador de cadena de caracteres para la elección. Todos los participantes que compiten por el liderazgo deben usar el mismo nombre de elección.

- `leader-name` cadena de caracteres

Valor de propuesta del nuevo líder.

### Ejemplo {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
