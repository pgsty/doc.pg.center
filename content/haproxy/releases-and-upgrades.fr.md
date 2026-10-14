---
title: "Versions, paquets et mises à jour"
linkTitle: "Versions et mises à jour"
weight: 80
description: "Branches stables, sources de version, identification des versions, maintenance et mises à jour"
icon: fa-solid fa-code-branch
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/intro/releases-and-upgrades/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3.7"
---

HAProxy est un projet open source soumis à la licence GPLv2, ce qui signifie que toute personne est autorisée à le redistribuer à condition de fournir l'accès au code source sur demande, notamment si des modifications ont été apportées.

HAProxy évolue via une branche de développement principale appelée « master » ou « mainline », à partir de laquelle de nouvelles branches sont créées une fois que le code est jugé stable. De nombreux sites web exécutent des branches de développement en production de manière volontaire, soit pour participer au projet, soit parce qu'ils ont besoin d'une fonctionnalité de pointe, et leurs retours sont précieux pour corriger les bogues et évaluer la qualité et la stabilité globales de la version en développement.

Les nouvelles branches créées lorsque le code est suffisamment stable constituent une version stable et sont généralement maintenues pendant plusieurs années, de sorte qu’il n’y a pas d’urgence à migrer vers une branche plus récente, même si vous n’êtes pas sur la dernière. Une fois qu’une branche stable est publiée, elle ne reçoit que des correctifs de bogues, et très rarement des mises à jour mineures lorsque cela facilite la vie des utilisateurs. Tous les correctifs intégrés à une branche stable proviennent nécessairement de la branche master. Cela garantit qu’aucun correctif ne sera perdu après une mise à jour. Pour cette raison, si vous corrigez un bogue, veuillez appliquer votre correctif à la branche master, et non à la branche stable. Vous pourriez même découvrir qu’il était déjà corrigé. Ce processus garantit également que les régressions dans une branche stable sont extrêmement rares, si bien qu’il n’y a jamais d’excuse pour ne pas mettre à jour vers la dernière version de votre branche actuelle.

Les branches sont numérotées avec deux chiffres séparés par un point, par exemple "1.6". Depuis la version 1.9, les branches dont le deuxième chiffre est impair sont principalement consacrées à des mises à jour techniques sensibles et s'adressent davantage aux utilisateurs avancés, car elles sont susceptibles de provoquer plus de bogues que les autres. Elles sont maintenues pendant environ un an seulement et ne doivent pas être déployées là où un retour arrière d'urgence n'est pas possible. Une version complète inclut une ou deux sous-versions indiquant le niveau de correction. Par exemple, la version 1.5.14 est la 14e version corrigée de la branche 1.5 après la publication de la version 1.5.0. Elle contient 126 corrections pour des bogues individuels, 24 mises à jour de la documentation et 75 autres correctifs rétroportés, dont la plupart étaient nécessaires pour corriger les 126 bogues mentionnés ci-dessus. Une fonctionnalité existante ne peut jamais être modifiée ni supprimée dans une branche stable, afin de garantir que les mises à jour au sein de la même branche seront toujours sans risque.

HAProxy est disponible depuis plusieurs sources, selon des rythmes de publication différents :

- Le site web officiel de la communauté : <http://www.haproxy.org/> : ce site fournit les sources de la dernière version de développement, de toutes les versions stables, ainsi que des instantanés nocturnes pour chaque branche. Le cycle de publication n'est pas rapide, plusieurs mois séparent les versions stables ou les instantanés de développement. Des versions très anciennes sont toujours prises en charge. Tout est fourni uniquement sous forme de sources, il faut donc reconstruire et/ou reconditionner tout ce qui provient de ce site.

- GitHub : <https://github.com/haproxy/haproxy/> : ce miroir est réservé à la branche de développement uniquement,
  il permet l'intégration avec le suivi des problèmes, les outils d'intégration continue et de couverture du code.
  Il est exclusivement destiné aux contributeurs ;

-  Certains systèmes d'exploitation, tels que les distributions Linux et les ports BSD. Ces systèmes fournissent généralement des versions maintenues à long terme, qui ne contiennent pas toujours tous les correctifs des versions officielles, mais qui incluent au moins les correctifs critiques. Il s'agit souvent d'une bonne option pour la plupart des utilisateurs qui ne recherchent pas de configurations avancées et souhaitent simplement simplifier les mises à jour ;

- Versions commerciales à partir de <http://www.haproxy.com/> : il s'agit de paquets professionnels pris en charge, construits pour divers systèmes d'exploitation ou fournis sous forme d'appareils, basés sur les dernières versions stables et incluant un certain nombre de fonctionnalités rétroportées depuis la prochaine version, pour lesquelles la demande est forte. C'est l'option idéale pour les utilisateurs souhaitant bénéficier des dernières fonctionnalités avec la fiabilité d'une branche stable, un temps de réponse le plus rapide possible pour corriger les bogues, ou simplement des contrats de support sur un produit open source ;

Afin de vous assurer que la version que vous utilisez est la plus récente dans votre branche, procédez comme suit :

- vérifiez quel exécutable HAProxy vous exécutez : certains systèmes le livrent par défaut et les administrateurs installent leurs versions ailleurs sur le système, il est donc important de vérifier dans les scripts de démarrage quel exécutable est utilisé ;

-  déterminez la source de votre version de HAProxy. Pour cela, il suffit généralement de taper « haproxy -v ». Une version de développement apparaît alors sous cette forme, avec le mot « dev » après le numéro de branche :

```text
HAProxy version 2.4-dev18-a5357c-137 2021/05/09 - https://haproxy.org/
```

    Une version stable s'affiche comme suit, tout comme les versions stables non modifiées

versions fournies par les éditeurs de systèmes d'exploitation :

```text
HAProxy version 1.5.14 2015/07/02
```

    Et une capture nocturne d'une version stable apparaît comme suit, avec une séquence hexadécimale après la version, ainsi qu'une date de la capture.

à la place de la date de la version :

```text
HAProxy version 1.5.14-e4766ba 2015/07/29
```

    Tout autre format peut indiquer un paquet spécifique au système, doté de son propre jeu de correctifs. Par exemple, les versions HAProxy Enterprise apparaîtront avec le

format suivant (`<branch>`-`<latest commit>`-`<revision>`):

```text
HAProxy version 1.5.0-994126-357 2015/07/02
```

    Veuillez noter qu’historiquement, les versions antérieures à 2.4 affichaient le nom du processus avec un trait d’union entre « HA » et « Proxy », y compris celles ci-dessus, qui ont été ajustées pour n’afficher que le format correct ; mieux vaut donc ignorer ce mot ou utiliser une correspondance souple dans les scripts. En outre, les versions modernes ajoutent une URL pointant vers la page d’accueil du projet.

    Enfin, les versions 2.1 et ultérieures incluront une ligne « Status » indiquant si la version est sûre pour la production ou non, et le cas échéant, jusqu’à quand, ainsi qu’un lien vers la liste des bogues connus affectant cette version.

-  pour les paquets spécifiques au système, vous devez vérifier auprès du dépôt de paquets de votre fournisseur ou de votre système de mise à jour afin de vous assurer que celui-ci est toujours pris en charge et que des correctifs sont toujours fournis pour votre branche. Pour les versions communautaires provenant de haproxy.org, rendez-vous simplement sur le site, vérifiez l'état de votre branche et comparez la dernière version avec la vôtre afin de savoir si vous êtes à jour. Si ce n'est pas le cas, vous pouvez procéder à une mise à niveau. Si votre branche n'est plus maintenue, vous êtes certainement très en retard et devrez envisager une mise à niveau vers une branche plus récente (lisez attentivement le README lors de cette opération).

HAProxy doit être mis à jour conformément à la source d’où il provient. En général, cela suit la méthode utilisée par le fournisseur du système pour mettre à jour un paquet. Si HAProxy a été obtenu à partir des sources, veuillez lire le fichier README du répertoire des sources après extraction des sources et suivez les instructions propres à votre système d’exploitation.
