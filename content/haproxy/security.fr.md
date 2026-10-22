---
title: "13. Considérations de sécurité"
linkTitle: "13. Sécurité"
weight: 370
description: "Isolation des privilèges, surface d'attaque, capacités Linux et fonctionnement sécurisé"
icon: fa-solid fa-shield-halved
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/security/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 13"
---

HAProxy est conçu pour s'exécuter avec des privilèges très limités. La méthode standard consiste à l'isoler dans une prison chroot et à supprimer ses privilèges pour qu'il s'exécute en tant qu'utilisateur non root, sans aucun droit à l'intérieur de cette prison, afin qu'en cas de découverte d'une vulnérabilité future, sa compromission n'affecte pas le reste du système.

Pour effectuer un chroot, il est d'abord nécessaire de le lancer en tant qu'utilisateur root. Il est inutile de créer manuellement des chroots afin de lancer le processus à l'intérieur ; ces environnements sont difficiles à mettre en place, jamais correctement maintenus et contiennent toujours bien plus de bogues que le système de fichiers principal. En cas de compromission, l'attaquant peut exploiter le système de fichiers spécifiquement conçu à cet effet. Malheureusement, de nombreux administrateurs confondent « lancer en tant que root » et « s'exécuter en tant que root », ce qui entraîne le changement d'UID avant le démarrage d'HAProxy, réduisant ainsi les restrictions de sécurité effectives.

HAProxy devra être lancé en tant qu'utilisateur root afin de :

- ajuster les limites des descripteurs de fichiers
- se lier à des numéros de port privilégiés
- se lier à une interface réseau spécifique
- écouter de manière transparente une adresse étrangère
- s'isoler à l'intérieur d'une prison chroot
- passer à un autre UID non privilégié

HAProxy peut nécessiter d’être exécuté en tant qu’utilisateur root afin de :

- se lier à une interface pour les connexions sortantes
- se lier à des ports sources privilégiés pour les connexions sortantes
- se lier de manière transparente à une adresse étrangère pour les connexions sortantes

La plupart des utilisateurs n'auront jamais besoin du cas « exécuter en tant que root ». Toutefois, le cas « démarrer en tant que root » couvre la majorité des utilisations.

Une configuration sécurisée comportera :

- une instruction chroot pointant vers un emplacement vide sans aucun droit d'accès. Cela peut être préparé de cette manière sur la ligne de commande UNIX :

```shell
# mkdir /var/empty && chmod 0 /var/empty || echo "Failed"
```

et référencé ainsi dans la section global de la configuration HAProxy :

```text
chroot /var/empty
```

- à la fois des instructions uid/utilisateur et gid/groupe dans la section globale :

```text
user haproxy
group haproxy
```

- un socket de statistiques dont le mode, le propriétaire (uid) et le groupe (gid) sont configurés pour correspondre à l'utilisateur et/ou au groupe autorisés à accéder à l'interface CLI, afin qu'aucun autre utilisateur ne puisse y accéder :

```text
stats socket /var/run/haproxy.stat uid hatop gid hatop mode 600
```

## 13.1. Prise en charge des capacités Linux {#section-13-1}

Depuis la version v2.9, HAProxy prend en charge les capacités Linux. Si le binaire est compilé avec USE_LINUX_CAP=1, il est capable de conserver les capacités attribuées par le mot-clé 'setcap' lors du passage de l'utilisateur root à un utilisateur non root.

Depuis la version v3.1, HAProxy vérifie également si les capacités spécifiées dans le mot-clé 'setcap' ont été définies par l'administrateur dans l'ensemble Permitted de son fichier binaire (appel système capget). Si tel est le cas, il effectue la transition de ces capacités vers l'ensemble Effective de son processus (appel système capset), tout en s'exécutant en tant qu'utilisateur non privilégié.

Cela a été fait afin d’éviter tous les cas d’utilisation potentiels lorsque HAProxy démarre et s’exécute en tant qu’utilisateur root : mode de proxy transparent, liaison à des ports privilégiés.

Le mot-clé 'setcap' prend en charge les capacités réseau suivantes :

- cap_net_admin : proxy transparent, liaison du socket à une interface réseau spécifique, utilisation de l'action set-mark ;
- cap_net_raw (sous-ensemble de cap_net_admin) : proxy transparent ;
- cap_net_bind_service : liaison du socket à un port privilégié ;
- cap_sys_admin : création du socket dans un espace de noms réseau spécifique.

HAProxy ne réalise jamais la transition de ces capacités de son ensemble « Permitted » vers l’ensemble « Effective », si elles ne sont pas listées en tant qu’argument de « setcap ». Pour en savoir plus sur le mot-clé « setcap » et les capacités prises en charge, reportez-vous à la section 3.1 Gestion des processus et sécurité du guide de configuration.

L'administrateur peut ajouter les capacités nécessaires au fichier binaire haproxy dans l'ensemble Permitted à l'aide de la commande suivante :

Exemple :

```haproxy
# setcap cap_net_admin,cap_net_bind_service=p /usr/local/sbin/haproxy
```

Les capacités ajoutées seront visibles dans l'ensemble Permitted du processus après son démarrage. Si les mêmes capacités sont spécifiées en tant qu'arguments de l'option 'setcap', elles pourront également être observées dans l'ensemble Effective du processus. Cela peut être vérifié à l'aide de la commande suivante :

Exemple :

```haproxy
# grep Cap /proc/<haproxy PID>/status
```

    CapInh: 0000000000000000
    CapPrm: 0000000000001400
    CapEff: 0000000000001400
    CapBnd: 000001ffffffffff
    CapAmb: 0000000000000000

Consultez les détails supplémentaires sur setcap et les jeux de capacités dans les pages de manuel Linux (capabilities(7)).

Dans certains cas d'utilisation, comme le proxy transparent ou la création de socket dans un espace de noms réseau spécifique, le parseur de fichier de configuration détecte que les capacités cap_net_raw ou cap_sys_admin ou d'autres capacités prises en charge sont nécessaires. Ensuite, durant l'étape d'initialisation, le processus HAProxy vérifie si ces capacités peuvent être ajoutées à son ensemble Effective. Si cela n'est pas possible en raison d'une erreur de syscall capget ou capset (restrictions imposées sur les appels systèmes par certains modules de sécurité comme SELinux, Seccomp, etc.), le processus émet des avertissements diagnostiques (démarrez avec -dD).

En raison du support de nombreuses plates-formes différentes, chacune avec ses propres paramètres système, il est impossible au parseur de déduire à partir du fichier de configuration si une liaison à des ports privilégiés est prévue. En cas de privilèges insuffisants (exécution en tant qu’utilisateur non root), le processus ne se terminera que par un message d’alerte similaire au suivant. Il incombe à l’utilisateur de vérifier à nouveau sa configuration et les capacités du binaire HAProxy.

Exemple :

```shell
$ haproxy -dD -f haproxy.cfg
...
[ALERT]    (96797): Binding [haproxy.cfg:36] for frontend fe: cannot bind socket (Permission denied) for [0.0.0.0:80]
[ALERT]    (96797): [haproxy.main()] Some protocols failed to start their listeners! Exiting.
```
