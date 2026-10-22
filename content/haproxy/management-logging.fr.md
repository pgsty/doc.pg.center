---
title: "8. Journalisation"
linkTitle: "8. Journalisation"
weight: 320
description: "Intégration Syslog, journaux de démarrage, journaux d'exécution et dépannage des journaux"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/logging/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 8"
---

Pour la journalisation, HAProxy s’appuie toujours sur un serveur syslog, car il ne réalise aucune opération sur le système de fichiers. La méthode standard consiste à envoyer les journaux via UDP vers le serveur de journalisation (par défaut sur le port 514). Il est très courant de le configurer sur 127.0.0.1, où s’exécute le démon syslog local, mais il peut aussi être utilisé sur le réseau pour journaliser sur un serveur central. Ce dernier offre des avantages supplémentaires, notamment dans les scénarios actif-actif où il est souhaitable de conserver les journaux fusionnés dans l’ordre d’arrivée. HAProxy peut également utiliser une socket UNIX pour envoyer ses journaux au démon syslog local, mais cela n’est pas du tout recommandé, car si le serveur syslog est redémarré pendant que HAProxy est en cours d’exécution, la socket sera remplacée et les nouveaux journaux seront perdus. Étant donné que HAProxy sera isolé dans une prison chroot, il ne pourra pas se reconnecter à la nouvelle socket. Des observations sur le terrain ont également montré que les tampons utilisés sur les sockets UNIX sont très petits et entraînent la perte de messages même à des charges très faibles. Cela peut toutefois convenir pour les tests.

Il est recommandé d'ajouter la directive suivante à la section « global » afin que HAProxy écrive ses journaux dans le démon local en utilisant la facility « local0 » :

```text
log 127.0.0.1:514 local0
```

puis ajouter la ligne suivante à chaque section « defaults » ou à chaque section « frontend » et « backend » :

```text
log global
```

Ainsi, tous les journaux seront centralisés grâce à la définition globale de l'emplacement du serveur de journaux.

Certains démons syslog n'écoutent pas par défaut le trafic UDP, si bien que, selon le démon utilisé, la syntaxe pour activer cette fonctionnalité varie :

-  sur sysklogd, vous devez passer l'argument "-r" dans la ligne de commande du démon afin qu'il écoute un socket UDP pour les journaux distants ; notez qu'il n'existe aucun moyen de le limiter à l'adresse 127.0.0.1, il recevra donc également les journaux provenant d'autres systèmes distants ;

- sur rsyslogd, les lignes suivantes doivent être ajoutées au fichier de configuration :

```shell
$ModLoad imudp
$UDPServerAddress *
$UDPServerRun 514
```

-  sur syslog-ng, une nouvelle source peut être créée de la manière suivante ; elle doit ensuite être ajoutée en tant que source valide dans l'une des directives "log" :

```text
source s_udp {
  udp(ip(127.0.0.1) port(514));
};
```

Veuillez consulter le manuel de votre démon syslog pour plus d'informations. Si aucun journal n'apparaît dans les fichiers de journalisation du système, veuillez envisager les tests suivants :

- redémarrez HAProxy. Chaque frontal et backend journalise une ligne indiquant son démarrage. Si ces journaux sont reçus, cela signifie que la journalisation fonctionne.

- exécutez la commande « strace -tt -s100 -etrace=sendmsg -p \<haproxy's pid\> » et effectuez une activité dont vous attendez qu'elle soit journalisée. Vous devriez voir les messages de journal envoyés via sendmsg(). S'ils ne s'affichent pas, redémarrez en exécutant strace au-dessus de HAProxy. Si vous ne voyez toujours aucun journal, cela signifie certainement qu'il y a une erreur dans votre configuration.

-  exécutez tcpdump pour surveiller le port 514, par exemple sur l'interface boucle locale si le trafic est envoyé localement : « tcpdump -As0 -ni lo port 514 ». Si les paquets apparaissent, cela prouve qu'ils sont envoyés, et le démon syslogd doit être dépanné.

Bien que les journaux de trafic soient envoyés depuis les frontaux (où les connexions entrantes sont acceptées), les backends doivent également être capables d'envoyer des journaux afin de signaler un changement d'état du serveur consécutif à un contrôle d'état. Veuillez consulter le manuel de configuration de HAProxy pour plus d'informations concernant toutes les options de journalisation possibles.

Il est pratique de choisir une facility qui n’est pas utilisée par d’autres démons. Les exemples HAProxy suggèrent souvent « local0 » pour les journaux de trafic et « local1 » pour les journaux d’administration, car ils ne sont jamais observés en production. Une seule facility suffirait également. Avoir des journaux séparés est pratique pour l’analyse, mais il est également important de se souvenir que les journaux peuvent parfois contenir des informations confidentielles, et qu’ils ne doivent donc pas être mélangés à d’autres journaux qui pourraient être accidentellement transmis à des personnes non autorisées.

Pour le dépannage sur site sans trop impacter la capacité du serveur, il est recommandé d'utiliser l'outil « halog » fourni avec HAProxy. Il s'agit en quelque sorte d'un utilitaire de type grep, conçu pour traiter les fichiers de journaux HAProxy à un débit de données très élevé. Les performances typiques s'établissent entre 1 et 2 Go de journaux par seconde. Il permet d'extraire uniquement certains journaux (par exemple : rechercher des codes d'état HTTP de certaines catégories, l'état de terminaison des connexions, rechercher par plages de temps de réponse, ne montrer que les erreurs), de compter les lignes, de limiter la sortie à un nombre de lignes, et d'effectuer certaines statistiques avancées telles que trier les serveurs par temps de réponse ou nombre d'erreurs, trier les URL par temps ou nombre d'accès, trier les adresses clientes par nombre d'accès, etc. Il est très pratique pour repérer rapidement des anomalies telles qu'un robot effectuant des boucles sur le site, et le bloquer.
