---
title: "Documentation et communauté"
linkTitle: "Ressources"
weight: 100
description: "L'ensemble des manuels du projet amont, les emplacements des sources, les canaux de support, les contacts et la licence"
icon: fa-solid fa-life-ring
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/intro/resources/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapters 1 and 5"
---

## 1. Documentation disponible {#section-1}

La documentation complète de HAProxy est contenue dans les documents suivants. Veuillez vous assurer de consulter la documentation pertinente afin d’économiser du temps et d’obtenir la réponse la plus précise à vos besoins. Veuillez également vous abstenir d’envoyer des questions à la liste de diffusion dont les réponses sont déjà disponibles dans ces documents.

- [`intro.txt`](/fr/haproxy/load-balancing/) (ce document) : il présente les bases de la répartition de charge, HAProxy en tant que produit, ses fonctionnalités, ses limites, certains pièges à éviter, certaines limitations propres aux systèmes d'exploitation, comment l'obtenir, son évolution, comment s'assurer d'exécuter une version avec tous les correctifs connus, comment le mettre à jour, ainsi que des compléments et des alternatives.

- [`management.txt`](/fr/haproxy/prerequisites/) : il explique comment démarrer HAProxy, comment le gérer à l'exécution, comment le gérer sur plusieurs nœuds, et comment procéder à des mises à jour sans interruption.

- [`configuration.txt`](/fr/haproxy/http-fundamentals/) : le manuel de référence détaille tous les mots-clés de configuration et leurs options. Il est utilisé lorsqu'une modification de configuration est nécessaire.

- coding-style.txt : destiné aux développeurs souhaitant proposer du code au projet. Il décrit le style à adopter pour le code. Il n'est pas très strict et l'ensemble du code ne le respecte pas entièrement, mais les contributions s'en écartant trop seront rejetées.

- proxy-protocol.txt : il s'agit de la spécification de facto du protocole PROXY, implémentée par HAProxy et un certain nombre de produits tiers.

- security.txt : comment signaler un problème de sécurité, et ce qui constitue ou ne constitue pas une vulnérabilité.

- README : comment compiler HAProxy à partir des sources

## 5. Contacts {#section-5}

Si vous souhaitez contacter les développeurs ou un membre de la communauté à propos de quoi que ce soit, la meilleure façon de procéder est généralement d’envoyer votre message à la liste de diffusion à l’adresse <haproxy@formilux.org>. Veuillez noter que cette liste est publique ainsi que ses archives, vous devriez donc éviter de divulguer des informations sensibles. Un millier d’utilisateurs de niveaux d’expérience variés y sont présents, et même les questions les plus complexes trouvent généralement une réponse optimale relativement rapidement. Les suggestions sont également les bienvenues.
Pour les utilisateurs ayant des difficultés avec le courrier électronique, une plateforme Discourse est disponible à l’adresse <http://discourse.haproxy.org/>. Toutefois, veuillez garder à l’esprit qu’un nombre réduit de personnes lisent les questions posées là-bas, et que la plupart sont traitées par une très petite équipe. Dans tous les cas, veuillez être patient et respectueux envers ceux qui consacrent leur temps libre à aider les autres.

Si vous pensez avoir découvert un bogue mais n’en êtes pas certain, il est préférable de le signaler sur la liste de diffusion. Si vous êtes convaincu d’avoir trouvé un bogue, que votre version est à jour dans sa branche, et que vous disposez déjà d’un compte GitHub, vous pouvez directement vous rendre sur <https://github.com/haproxy/haproxy/> et soumettre un problème en incluant tous les détails éventuellement disponibles. Encore une fois, cela est public, veillez donc à ne pas publier d’informations que vous pourriez regretter plus tard. Étant donné que le suivi des problèmes s’affiche sous la forme d’un fil très long, évitez de coller de très longues sorties (quelques centaines de lignes ou plus) et joignez-les plutôt en pièces jointes.

Si vous pensez avoir découvert un problème de sécurité, veuillez vous référer au fichier doc/security.txt. Il explique ce qui constitue ou ne constitue pas une vulnérabilité dans HAProxy, ainsi que la procédure à suivre pour signaler une vulnérabilité réelle de manière confidentielle. La plupart des problèmes suspectés s'avèrent être des bogues ordinaires, mieux signalés comme décrit ci-dessus.

## Jeu complet de manuels locaux {#complete-local-manual-set}

- [Guide de démarrage](/fr/haproxy/load-balancing/)
- [Manuel de configuration](/fr/haproxy/http-fundamentals/)
- [Guide de gestion](/fr/haproxy/prerequisites/)

## Provenance de l'édition {#edition-provenance}

- **Édition :** HAProxy 3.4.6-66, instantané de la documentation de la branche de maintenance
- **Dernière version stable :** HAProxy 3.4.6, tag `v3.4.6`
- **Commit source :** [`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8)
- **Jeu amont rendu :** [docs.haproxy.org/3.4/](https://docs.haproxy.org/3.4/)
- **Copies locales de la licence :** [avis de licence HAProxy](/third_party/haproxy/LICENSE) et [GPLv2](/third_party/haproxy/GPL-2.0)
