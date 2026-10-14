---
title: Signalement de bogues
weight: 1400
description: "Comment soumettre des rapports d'incident pour le projet etcd"
icon: fa-solid fa-bug
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/reporting_bugs.md"
---

Si une partie du projet etcd présente des bogues ou des erreurs de documentation, veuillez nous en informer en [ouvrant une demande][etcd-issue]. Nous prenons très au sérieux les bogues et les erreurs, et considérons qu'aucun problème n'est trop petit. Avant de créer un rapport de bogue, veuillez vérifier qu'une demande signalant le même problème n'existe pas déjà.

Pour que votre rapport de bogue soit précis et facile à comprendre, veillez à ce qu’il soit :

- Spécifique. Incluez autant de détails que possible : version utilisée, environnement, configuration, etc. Si le bogue est lié à l'exécution du serveur etcd, veuillez joindre le journal d'etcd (le journal de démarrage avec la configuration d'etcd est particulièrement important).

- Reproductible. Incluez les étapes permettant de reproduire le problème. Nous comprenons que certains problèmes peuvent être difficiles à reproduire ; veuillez inclure les étapes qui pourraient mener au problème. Si possible, joignez le répertoire de données etcd affecté ainsi que la trace de pile au rapport de bogues.

- Isolé. Essayez d'isoler et de reproduire le bogue avec un minimum de dépendances. Un nombre trop élevé de dépendances dans un rapport de bug ralentit considérablement la résolution. Le débogage des systèmes externes qui dépendent d'etcd est hors sujet, mais nous sommes heureux de fournir des indications dans la bonne direction ou d'aider à utiliser etcd lui-même.

- Unique. Ne dupliquez pas un rapport de bogue existant.

- Délimité. Un seul bogue par rapport. Ne signalez pas un autre bogue dans le même rapport.

Il peut être utile de lire [l’article d’Elika Etemad sur la rédaction de bons rapports de bogues][filing-good-bugs] avant de créer un rapport.

Nous pouvons demander des informations supplémentaires pour localiser un bogue. Un rapport de bogue en double sera fermé.

## Questions fréquemment posées {#frequently-asked-questions}

### Comment obtenir une trace de pile {#how-to-get-a-stack-trace}

``` bash
$ kill -QUIT $PID
```

### Comment obtenir la version d'etcd {#how-to-get-etcd-version}

``` bash
$ etcd --version
```

### Comment obtenir la configuration et les journaux d'etcd lorsqu'il s'exécute en tant que service systemd « etcd2.service » {#how-to-get-etcd-configuration-and-log-when-it-runs-as-systemd-service-etcd2service}

``` bash
$ sudo systemctl cat etcd2
$ sudo journalctl -u etcd2
```

En raison d'un bogue upstream dans systemd, journald peut manquer les dernières lignes de journal lorsque ses processus se terminent. Si journalctl indique qu'etcd s'est arrêté sans message fatal ni de panique, essayez `sudo journalctl -f -t etcd2` afin d'obtenir la totalité du journal.

[etcd-issue]: https://github.com/etcd-io/etcd/issues/new
[filing-good-bugs]: http://fantasai.inkedblade.net/style/talks/filing-good-bugs/
