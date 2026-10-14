---
title: "Dimensionnement et performances"
linkTitle: "Dimensionnement"
weight: 70
description: "Principes de planification de capacité, ordres de grandeur des performances et règles pratiques de bon sens"
icon: fa-solid fa-gauge-high
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/intro/sizing/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3.6"
---

Les valeurs typiques d'utilisation du processeur montrent que 15 % du temps de traitement sont consacrés à HAProxy contre 85 % au noyau en mode TCP ou HTTP fermé, et environ 30 % pour HAProxy contre 70 % pour le noyau en mode HTTP keep-alive. Cela signifie que le système d'exploitation et son réglage ont une influence forte sur les performances globales.

Les usages varient beaucoup d’un utilisateur à l’autre : certains se concentrent sur le débit, d’autres sur le taux de requêtes, d’autres sur la concurrence des connexions, d’autres encore sur les performances SSL. Cette section vise à fournir quelques éléments pour faciliter cette tâche.

Il est important de garder à l’esprit que chaque opération comporte un coût, de sorte que chaque opération individuelle ajoute son surcoût aux autres, ce qui peut être négligeable dans certains cas, mais peut aussi dominer dans d’autres.

Lors du traitement des requêtes émanant d'une connexion, on peut dire que :

- le transfert des données coûte moins cher que l'analyse des en-têtes de requête ou de réponse ;

- analyser les en-têtes de requête ou de réponse coûte moins cher que d'établir puis de fermer une connexion vers un serveur ;

- établir ou fermer une connexion coûte moins qu'une opération de reprise TLS ;

- une opération de reprise TLS coûte moins cher qu'une négociation TLS complète avec calcul de clé ;

- une connexion inactive consomme moins de CPU qu'une connexion dont les tampons contiennent des données ;

- un contexte TLS consomme encore plus de mémoire qu'une connexion avec des données ;

En pratique, il est donc moins coûteux de traiter les octets de charge utile que les octets d’en-tête, ce qui rend plus facile l’atteinte d’un débit réseau élevé avec des objets volumineux (peu de requêtes par unité de volume) qu’avec des objets de petite taille (nombreuses requêtes par unité de volume). C’est pourquoi le débit maximal est toujours mesuré avec des objets volumineux, tandis que le débit de requêtes ou le débit de connexions est mesuré avec des objets de petite taille.

Certaines opérations échelonnent bien sur plusieurs processus répartis sur plusieurs processeurs, tandis que d'autres ne s'échelonnent pas aussi efficacement. La bande passante réseau ne s'échelonne pas très loin, car le processeur est rarement le goulot d'étranglement pour de grands objets, le goulot étant principalement la bande passante réseau et les bus de données pour atteindre les interfaces réseau. Le débit de connexion ne s'échelonne pas bien sur plusieurs processeurs en raison de quelques verrous dans le système lors de la gestion du tableau des ports locaux. Le débit de requêtes sur des connexions persistantes s'échelonne très bien, car il implique peu de mémoire ni de bande passante réseau et ne nécessite pas d'accéder à des structures verrouillées. Le calcul de la clé TLS s'échelonne très bien, car il est entièrement limité par le processeur. La reprise TLS s'échelonne modérément bien, mais atteint ses limites vers 4 processus, où la surcharge liée à l'accès au tableau partagé compense les gains faibles attendus d'une puissance accrue.

Les performances qu'on peut attendre d'un système très bien optimisé se situent dans la plage suivante. Il est important de les considérer comme des ordres de grandeur, et de s'attendre à des variations importantes dans n'importe quelle direction, en fonction du processeur, des paramètres IRQ, du type de mémoire, du type d'interface réseau, de l'optimisation du système d'exploitation, etc.

Les chiffres suivants ont été obtenus sur un processeur Core i7 fonctionnant à 3,7 GHz, équipé de deux ports réseau 10 Gbps, sous un noyau Linux 3.10, avec HAProxy 1.6 et OpenSSL 1.0.2. HAProxy était exécuté en tant que processus unique sur un cœur CPU dédié, et deux cœurs supplémentaires étaient dédiés aux interruptions réseau :

- 20 Gbps de bande passante réseau maximale en clair pour les objets de 256 ko ou plus, 10 Gbps pour les objets de 41 ko ou plus ;

- 4,6 Gbps de trafic TLS utilisant le chiffrement AES256-GCM avec des objets volumineux ;

- 83000 connexions TCP par seconde depuis le client vers le serveur ;

- 82000 connexions HTTP par seconde du client vers le serveur ;

- 97000 requêtes HTTP par seconde en mode server-close (keep-alive avec le client, fermeture avec le serveur);

- 243000 requêtes HTTP par seconde en mode keep-alive end-to-end ;

- 300000 connexions TCP filtrées par seconde (anti-DDoS)

- 160000 requêtes HTTPS par seconde en mode keep-alive sur des connexions TLS persistantes ;

- 13100 requêtes HTTPS par seconde en utilisant des connexions TLS reprises ;

- 1300 connexions HTTPS par seconde utilisant des connexions TLS renégociées avec RSA2048 ;

- 20000 connexions simultanées saturées par Go de RAM, incluant la mémoire nécessaire aux tampons système ; il est possible d'obtenir de meilleurs résultats avec un réglage soigné, mais ce résultat est facile à atteindre.

- environ 8000 connexions TLS simultanées (côté client uniquement) par Go de RAM, incluant la mémoire nécessaire aux tampons système ;

- environ 5000 connexions TLS simultanées de bout en bout (des deux côtés) par Go de RAM, y compris la mémoire requise pour les tampons système ;

Un benchmark plus récent, mettant en œuvre HAProxy 2.4 avec multithreading activé sur un processeur ARM Graviton2 à 64 cœurs dans AWS, a atteint 2 millions de requêtes HTTPS par seconde avec un temps de réponse inférieur à la milliseconde, ainsi qu’un débit de 100 Gbps :

```text
https://www.haproxy.com/blog/haproxy-forwards-over-2-million-http-requests-per-second-on-a-single-aws-arm-instance/
```

Ainsi, une bonne règle empirique à garder à l'esprit est que le débit des requêtes est divisé par 10 entre le keep-alive TLS et la reprise TLS, ainsi qu'entre la reprise TLS et la renégociation TLS, tandis qu'il n'est divisé que par 3 entre le keep-alive HTTP et la fermeture HTTP. Une autre bonne règle empirique consiste à se souvenir qu'un cœur à fréquence élevée disposant d'instructions AES peut traiter environ 20 Gbps d'AES-GCM par cœur.

Une autre bonne règle empirique consiste à considérer qu’un même serveur peut permettre à HAProxy de saturer :

- environ 5 à 10 serveurs de fichiers statiques ou proxies de mise en cache ;

- environ 100 proxies anti-virus ;

- et environ 100 à 1000 serveurs d'applications, selon la technologie utilisée.
