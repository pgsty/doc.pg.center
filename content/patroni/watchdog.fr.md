---
title: "Prise en charge du watchdog"
weight: 90
icon: fa-solid fa-dog
description: "Intégration du watchdog et considérations sur le fencing pour les clusters Patroni."
module: [PATRONI]
categories: [Concept]
upstream_link: "https://patroni.readthedocs.io/en/latest/watchdog.html"
---

<a id="watchdog"></a>

L'exécution de plusieurs serveurs PostgreSQL en tant que primaires peut entraîner la perte de transactions en raison de lignes temporelles divergentes. Ce cas est également appelé problème de split-brain. Pour éviter le split-brain, Patroni doit s'assurer que PostgreSQL n'accepte aucune validation de transaction après l'expiration de la clé de leader dans le DCS. Dans des conditions normales, Patroni tente d'atteindre cet objectif en arrêtant PostgreSQL lorsque la mise à jour du verrou de leader échoue pour quelque raison que ce soit. Toutefois, cette action peut échouer pour diverses raisons :

- Patroni a planté à cause d'un bug, d'une condition de mémoire insuffisante ou parce qu'il a été tué accidentellement par un administrateur système.
- L'arrêt de PostgreSQL est trop lent.
- Patroni ne parvient pas à s'exécuter en raison d'une charge élevée sur le système, de la mise en pause de la machine virtuelle par l'hyperviseur ou d'autres problèmes d'infrastructure.

Pour garantir un comportement correct dans ces conditions, Patroni prend en charge les périphériques watchdog. Les périphériques watchdog sont des mécanismes logiciels ou matériels qui redémarreront l’ensemble du système lorsqu’ils ne reçoivent pas de battement de cœur (keepalive) dans un délai spécifié. Cela ajoute une couche supplémentaire de sécurité en cas d’échec des mécanismes habituels de protection contre les scénarios de split-brain de Patroni.

Patroni tentera d'activer le watchdog avant de promouvoir PostgreSQL en primaire. Si l'activation du watchdog échoue et que le mode watchdog est `required`, le nœud refusera de devenir leader. Lorsqu'il décidera de participer à l'élection du leader, Patroni vérifiera également que la configuration du watchdog lui permettra de devenir leader. Après avoir rétrogradé PostgreSQL (par exemple en cas de basculement manuel), Patroni désactivera à nouveau le watchdog. Le watchdog sera également désactivé pendant que Patroni est en état de pause.

Par défaut, Patroni configure le watchdog pour expirer 5 secondes avant l’expiration du TTL. Avec la configuration par défaut de `loop_wait=10` et `ttl=30`, cela laisse au moins 15 secondes (`ttl` - `safety_margin` - `loop_wait`) à la boucle HA pour se terminer correctement avant que le système ne soit réinitialisé de force. Par défaut, l’accès au DCS est configuré pour expirer après 10 secondes. Cela signifie qu’en cas d’indisponibilité du DCS, par exemple en raison de problèmes réseau, Patroni et PostgreSQL disposent d’au moins 5 secondes (`ttl` - `safety_margin` - `loop_wait` - `retry_timeout`) pour atteindre un état où toutes les connexions clientes sont interrompues.

La marge de sécurité est la durée que Patroni réserve pour couvrir le délai entre la mise à jour de la clé de leader et l'envoi du keepalive au watchdog. Patroni tente d'envoyer un keepalive immédiatement après la confirmation de la mise à jour de la clé de leader. Si le processus Patroni est suspendu pendant une durée prolongée exactement au moment opportun, le keepalive peut être retardé au-delà de la marge de sécurité sans déclencher le watchdog. Cela crée une fenêtre de temps durant laquelle le watchdog ne se déclenchera pas avant l'expiration de la clé de leader, invalidant ainsi la garantie. Pour être absolument certain que le watchdog se déclenchera dans toutes les circonstances, configurez le watchdog pour qu'il expire après la moitié de la durée TTL en définissant `safety_margin` à -1 afin de fixer le délai d'expiration du watchdog à `ttl // 2`. Si vous avez besoin de cette garantie, vous devriez probablement augmenter `ttl` et/ou réduire `loop_wait` et `retry_timeout`.

Les watchdogs ne sont actuellement pris en charge que via l'interface du périphérique watchdog Linux.

--------

## Configuration du watchdog logiciel sous Linux {#setting-up-software-watchdog-on-linux}

La configuration par défaut de Patroni tentera d'utiliser `/dev/watchdog` sous Linux si celui-ci est accessible à Patroni. Pour la plupart des cas d'utilisation, l'utilisation du watchdog logiciel intégré au noyau Linux est suffisamment sécurisée.

Pour activer le watchdog logiciel, exécutez les commandes suivantes en tant qu'utilisateur root avant de démarrer Patroni :

``` bash
modprobe softdog
# Replace postgres with the user you will be running patroni under
chown postgres /dev/watchdog
```

Pour le test, il peut être utile de désactiver le redémarrage en ajoutant `soft_noboot=1` à la ligne de commande de modprobe. Dans ce cas, le watchdog enregistrera simplement une ligne dans le tampon circulaire du noyau, visible via `dmesg`.

Patroni enregistrera les informations relatives au watchdog lorsqu’il sera activé avec succès.
