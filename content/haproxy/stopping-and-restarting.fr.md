---
title: "4. Arrêt et redémarrage de HAProxy"
linkTitle: "4. Arrêt et redémarrage"
weight: 280
description: "Signaux, arrêts progressifs, rechargements et redémarrages en mode master-worker"
icon: fa-solid fa-rotate
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/stopping-and-restarting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 4"
---

HAProxy prend en charge un arrêt progressif et un arrêt brutal. L'arrêt brutal est simple : lorsqu'un signal SIGTERM est envoyé au processus HAProxy, celui-ci se termine immédiatement et toutes les connexions établies sont fermées. L'arrêt progressif est déclenché lorsqu'un signal SIGUSR1 est envoyé au processus HAProxy. Il consiste à ne plus se lier aux ports d'écoute, tout en continuant à traiter les connexions existantes jusqu'à leur fermeture. Une fois la dernière connexion fermée, le processus se termine.

La méthode d'arrêt brutal est utilisée pour les actions « stop » ou « restart » du script de gestion du service.
L'arrêt progressif est utilisé pour l'action « reload », qui tente de recharger sans interruption une nouvelle configuration dans un nouveau processus.

Ces signaux peuvent être envoyés par le nouveau processus HAProxy lui-même pendant un rechargement ou un redémarrage, afin de ne les émettre qu'au dernier moment et seulement s'ils sont indispensables. C'est ce que font respectivement les options "-st" (arrêt brutal) et "-sf" (arrêt progressif).

En mode master-worker, il n'est pas nécessaire de lancer un nouveau processus haproxy pour recharger la configuration. Le processus master réagit au signal SIGUSR2 en se réexécutant avec le paramètre -sf suivi des PID des workers. Le master analysera alors le fichier de configuration et créera de nouveaux workers par fork.

Pour mieux comprendre l'utilisation de ces signaux, il est important de comprendre l'ensemble du mécanisme de redémarrage.

Tout d’abord, un processus HAProxy existant est en cours d’exécution. L’administrateur utilise une commande spécifique au système, telle que « /etc/init.d/haproxy reload », pour indiquer qu’il souhaite appliquer le nouveau fichier de configuration. Ce qui se produit ensuite est le suivant. Tout d’abord, le script de service (/etc/init.d/haproxy ou équivalent) vérifiera que le fichier de configuration est correctement analysé à l’aide de la commande « haproxy -c ». Ensuite, il tentera de démarrer HAProxy avec ce fichier de configuration, en utilisant « -st » ou « -sf ».

Ensuite, HAProxy tente de se lier à tous les ports d'écoute. Si des erreurs critiques se produisent (par exemple : adresse non présente sur le système, accès refusé), le processus se termine avec une erreur. Si la liaison d'une socket échoue car un port est déjà utilisé, le processus envoie d'abord un signal SIGTTOU à tous les PID spécifiés dans la liste de PID "-st" ou "-sf". Ce signal est appelé le « signal de pause ». Il invite tous les processus haproxy existants à interrompre temporairement l'écoute de leurs ports afin que le nouveau processus puisse réessayer la liaison. Pendant cette période, le processus ancien continue à traiter les connexions existantes. Si la liaison échoue toujours (par exemple parce qu'un port est partagé avec un autre démon), le nouveau processus envoie un signal SIGTTIN aux anciens processus pour leur demander de reprendre leurs opérations comme si rien ne s'était produit. Les anciens processus reprennent alors l'écoute des ports et continuent à accepter les connexions. Notez que ce mécanisme dépend du système et que certains systèmes d'exploitation ne le supportent pas en mode multi-processus.

Si le nouveau processus parvient à se lier correctement à tous les ports, il envoie soit le SIGTERM (arrêt brutal en cas de "-st"), soit le SIGUSR1 (arrêt progressif en cas de "-sf") à tous les processus pour leur notifier qu’il est désormais chargé des opérations et que les anciens processus doivent quitter, soit immédiatement, soit une fois leur tâche terminée.

Il est important de noter qu’au cours de cette période, il existe deux petites fenêtres de quelques millisecondes chacune durant lesquelles quelques échecs de connexion peuvent être observés en cas de charge élevée. Les taux de défaillance observés sont généralement d’environ 1 défaillance par rechargement pour chaque 10 000 nouvelles connexions par seconde, ce qui signifie qu’un site fortement sollicité fonctionnant à 30 000 nouvelles connexions par seconde peut connaître environ 3 défaillances de connexion à chaque rechargement. Les deux situations où cela se produit sont :

- si le nouveau processus échoue à se lier en raison de la présence du processus ancien, il devra d'abord passer par la séquence SIGTTOU+SIGTTIN, qui dure généralement environ une milliseconde pour quelques dizaines de frontaux, pendant laquelle certains ports ne seront ni liés au processus ancien ni encore liés au nouveau. HAProxy contourne ce problème sur les systèmes qui prennent en charge les options de socket SO_REUSEPORT, car elles permettent au nouveau processus de se lier sans devoir d'abord demander au processus ancien de se délier. La plupart des systèmes BSD prennent en charge cela depuis toujours. Linux l'a pris en charge à partir de la version 2.0, puis l'a supprimé vers la version 2.2, mais des correctifs circulaient à l'époque. Il a été réintroduit dans le noyau 3.9 ; si vous constatez un taux d'échec de connexion supérieur à celui mentionné ci-dessus, veillez à ce que votre noyau soit la version 3.9 ou ultérieure, ou que les correctifs pertinents aient été rétroportés à votre noyau (moins probable).

- lorsque les anciens processus ferment les ports d'écoute, le noyau peut ne pas toujours redistribuer les connexions en attente restant dans la file d'attente du socket. En cas de charge élevée, un paquet SYN peut survenir juste avant la fermeture du socket, ce qui entraîne l'envoi d'un paquet RST au client. Dans certains environnements critiques où même une seule perte est inacceptable, ces pertes sont parfois gérées à l'aide de règles de pare-feu bloquant les paquets SYN pendant le rechargement, forçant ainsi le client à retransmettre. Cette solution dépend entièrement du système, car certains systèmes pourraient parcourir d'autres files d'attente d'écoute et éviter ainsi ce RST. Un deuxième cas concerne l'ACK du client sur un socket local qui était en état SYN_RECV juste avant la fermeture. Cet ACK entraîne l'envoi d'un paquet RST alors que le processus haproxy n'est pas encore au courant. Ce cas est plus difficile à éliminer, bien que les règles de filtrage du pare-feu mentionnées ci-dessus fonctionnent bien si elles sont appliquées une seconde environ avant le redémarrage du processus.

Pour la grande majorité des utilisateurs, de telles pertes ne se produiront jamais, car ils n'ont pas une charge suffisante pour déclencher les conditions de concurrence. Et pour la plupart des utilisateurs à fort trafic, le taux d'échec reste encore raisonnablement dans la marge de bruit, à condition qu’au moins SO_REUSEPORT soit correctement pris en charge sur leurs systèmes.
