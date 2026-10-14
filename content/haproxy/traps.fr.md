---
title: "11. Pièges courants à éviter"
linkTitle: "11. Pièges courants"
weight: 350
description: "Erreurs opérationnelles et comportements surprenants à éviter"
icon: fa-solid fa-triangle-exclamation
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/traps/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 11"
---

Parfois, une personne signale que, après un redémarrage du système, le service HAProxy n’est pas démarré, et qu’une fois lancé manuellement, il fonctionne correctement. La plupart de ces utilisateurs exécutent un mécanisme d’adresse IP en cluster, comme keepalived, afin d’attribuer l’adresse IP du service uniquement au nœud principal, et alors qu’il fonctionnait auparavant lorsqu’ils liaient HAProxy à l’adresse 0.0.0.0, il a cessé de fonctionner après avoir lié celui-ci à l’adresse IP virtuelle. Ce qui se produit ici, c’est que, lors du démarrage du service, l’adresse IP virtuelle n’est pas encore détenue par le nœud local, si bien que lorsque HAProxy tente de se lier à cette adresse, le système la rejette car elle n’est pas une adresse locale. La solution ne consiste pas à retarder le démarrage du service HAProxy (car cela ne résisterait pas à un redémarrage), mais plutôt à configurer correctement le système afin de permettre la liaison à des adresses non locales. Cela peut être facilement réalisé sous Linux en définissant le paramètre sysctl net.ipv4.ip_nonlocal_bind à 1. Cette configuration est également nécessaire pour intercepter de manière transparente le trafic IP qui traverse HAProxy pour une adresse cible spécifique.

Les configurations multi-processus utilisant des plages de ports sources peuvent sembler fonctionner mais entraîneront des échecs aléatoires sous charge élevée, car plusieurs processus pourraient tenter d'utiliser le même port source pour se connecter au même serveur, ce qui n'est pas possible. Le système signalera une erreur et une nouvelle tentative aura lieu, en choisissant un autre port. Une valeur élevée du paramètre « retries » peut masquer cet effet dans une certaine mesure, mais cela entraîne également une utilisation accrue du CPU et un temps de traitement plus long. Les journaux rapporteront également un certain nombre de tentatives. Pour cette raison, les plages de ports devraient être évitées dans les configurations multi-processus.

Étant donné qu’HAProxy utilise SO_REUSEPORT et prend en charge l’exécution de plusieurs processus indépendants liés au même IP:port, il peut arriver pendant le dépannage qu’un ancien processus n’ait pas été arrêté avant le lancement d’un nouveau. Cela produit des résultats de tests absurdes, qui tendent à indiquer que toute modification de la configuration est ignorée. La raison est que, même si le nouveau processus est effectivement redémarré avec une nouvelle configuration, l’ancien processus continue également à recevoir des connexions entrantes et à les traiter, produisant ainsi des résultats inattendus. En cas de doute, arrêtez simplement le nouveau processus et réessayez. Si cela fonctionne toujours, il est très probable qu’un ancien processus soit toujours en cours d’exécution et doive être arrêté. La commande Linux « netstat -lntp » s’avère bien utile ici.

Lors d’ajout d’entrées à une liste de contrôle d’accès (ACL) depuis la ligne de commande (par exemple, lors du blocage d’une adresse source), il est important de garder à l’esprit que ces entrées ne sont pas synchronisées avec le fichier et qu’en cas de rechargement de la configuration, ces modifications seront perdues. Bien que ce comportement soit souvent souhaité (pour le blocage), il peut ne pas correspondre aux attentes lorsque le changement a été effectué en tant que correction d’un problème. Voir l’action « add acl » de l’interface CLI.
