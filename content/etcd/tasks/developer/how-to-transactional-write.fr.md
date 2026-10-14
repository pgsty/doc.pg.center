---
title: Comment effectuer plusieurs écritures dans une transaction
description: Guide des écritures transactionnelles
weight: 500
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
---

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/etcd/install/).
* Un cluster `etcd` en cours d'exécution.

## Terminologie {#terminology}

Voici les définitions de quelques termes clés utilisés dans l’[exemple](#example) ci-dessous.

| Termes | Définition |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | Outil en ligne de commande pour interagir avec le serveur etcd. |
| commande [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options) | La commande `txn` est une abréviation de « transaction ». Elle lit plusieurs requêtes etcd depuis l'entrée standard et les applique comme une transaction atomique unique. Une transaction se compose d'une liste de conditions, d'une liste de requêtes à appliquer si toutes les conditions sont vraies, et d'une liste de requêtes à appliquer si au moins une condition est fausse. Consultez [commandes clé-valeur d’etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands) pour plus d'informations. |
| `compare` | La clause `compare` au sein d'une transaction (`txn`) sert de vérification conditionnelle déterminant si les opérations de la transaction doivent s'exécuter. Elle garantit que les modifications ne sont appliquées que si l'état actuel du magasin clé-valeur correspond aux conditions attendues, assurant ainsi la cohérence des données et évitant les conflits dans les environnements concurrents. Pour voir la structure de la commande, consultez la section [Effectuer une transaction](#2-perform-a-transaction) ci-dessous. |

## Transactions {#transactions}

`txn` pour traiter toutes les requêtes dans une seule transaction :

```bash
etcdctl txn --help
```

Les transactions dans etcd permettent d'exécuter plusieurs opérations de manière atomique, garantissant que toutes les opérations sont appliquées ou qu’aucune ne l’est. Cela est essentiel pour maintenir la cohérence des données lors de mises à jour liées. En savoir plus sur les transactions dans [la documentation de l'API](/fr/etcd/learning/api/#transaction).

### Exemple {#example}

Considérons un scénario dans lequel vous souhaitez mettre à jour l’e-mail et le numéro de téléphone d’un utilisateur dans une seule transaction. Cela garantit que les deux mises à jour sont appliquées ensemble.

![05_etcdctl_transaction_2024101213](/etcd/tasks/img/transactional-write.gif)

#### 0. Variables et drapeaux utilisés {#0-variables-and-flags-used}

| Variables |
| :--- |
| `/users/{<user_id>/email` : clé etcd représentant l'adresse e-mail d'un utilisateur. |
| `/users/<user_id>/phone` : clé etcd représentant le numéro de téléphone d'un utilisateur. |
| **Drapeaux** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3) : Drapeau permettant d'entrer manuellement les données de transaction |

#### 1. Configurer les données initiales {#1-set-up-initial-data}

Tout d’abord, créez un utilisateur avec quelques données initiales.

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. Effectuer une transaction {#2-perform-a-transaction}

Mettez à jour l’e-mail et le numéro de téléphone de l’utilisateur dans une seule transaction.

   ```shell
   etcdctl txn --interactive

   compares:
   value("/users/12345/email") = "old.address@johndoe.com"

   success requests (get, put, delete):
   put /users/12345/email "new.address@johndoe.com"
   put /users/12345/phone "098-765-4321"

   failure requests (get, put, delete):
   get /users/12345/email
   ```

* **Comparaison** : Vérifiez que l'e-mail actuel correspond à "<old.address@johndoe.com>". Cela garantit que la transaction ne s'effectue que si les données sont telles qu'attendu.
* **Succès** : Si la comparaison est vraie, mettez à jour à la fois l'e-mail et le numéro de téléphone.
* **Échec** : Si la comparaison échoue, récupérez l'e-mail actuel afin de comprendre pourquoi la transaction n'a pas pu s'effectuer.

### Considérations importantes {#important-considerations}

* **Atomicité** : La transaction garantit que la mise à jour de l’e-mail et du numéro de téléphone s’effectue ensemble. Si la condition initiale (comparaison) n’est pas remplie, aucune mise à jour n’est appliquée.
* **Cohérence** : L’utilisation des transactions assure la cohérence des données, notamment lors de mises à jour multiples liées.
* **Éviter plusieurs opérations put sur la même clé** : Ne pas effectuer plusieurs mises à jour pour la même clé au sein d’une même transaction, car cela peut entraîner des résultats imprévus. Chaque clé ne devrait être mise à jour qu’une seule fois par transaction.
