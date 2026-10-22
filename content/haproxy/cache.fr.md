---
title: "6. Mise en cache"
linkTitle: "6. Mise en cache"
weight: 170
description: "Limites et configuration du cache dans les sections cache et proxy"
icon: fa-solid fa-box-archive
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/cache/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 6"
---

HAProxy fournit un cache, conçu pour mettre en cache de petits objets (favicon, CSS...).
Il s'agit d'un cache minimaliste, à faible maintenance, qui s'exécute en mémoire RAM.

Le cache repose sur une zone mémoire partagée entre tous les threads, divisée en blocs de 1 ko.

Si un objet n'est plus utilisé, il peut être supprimé afin de stocker un nouvel objet indépendamment de sa date d'expiration. Les objets les plus anciens sont supprimés en premier lorsque l'on tente d'allouer un nouvel objet.

Le cache utilise un hachage de l'en-tête host et de l'URI comme clé.

Il est possible de consulter l'état d'un cache à l'aide de la commande socket Unix « show cache » ; consultez la section [9.3](/fr/haproxy/statistics-and-monitoring/#section-9-3) « Commandes socket Unix » du Guide d'administration pour plus de détails.

Lorsqu'un objet est livré depuis le cache, le nom du serveur dans le journal est remplacé par "`<CACHE>`".

## 6.1. Limitation {#section-6-1}

Le cache ne stockera ni ne livrera d'objets dans ces cas :

- Si la réponse n'est pas un 200

- Si la réponse contient un en-tête Vary et que l'option process-vary est désactivée, ou qu'un en-tête actuellement non géré est spécifié dans la valeur de Vary (seuls accept-encoding, referer et origin sont gérés pour l'instant)

- Si la taille du Content-Length + celle des en-têtes est supérieure à "max-object-size"

- Si la réponse ne peut pas être mise en cache

- Si la réponse ne dispose ni d'une expiration explicite (directives Cache-Control s-maxage ou max-age, ou en-tête Expires) ni d'un validateur (en-têtes ETag ou Last-Modified)

- Si l'option process-vary est activée et qu'il existe déjà max-secondary-entries entrées avec la même clé primaire que la réponse actuelle

- Si l'option process-vary est activée et que la réponse possède un encodage inconnu (non mentionné dans
  <https://www.iana.org/assignments/http-parameters/http-parameters.xhtml>) tout en variant sur l'en-tête client accept-encoding

- Si la requête n'est pas un GET

- Si la version HTTP de la requête est inférieure à 1.1

- Si la requête contient un en-tête Authorization

## 6.2. Configuration {#section-6-2}

Pour configurer un cache, vous devez définir une section de cache et l'utiliser dans un proxy à l'aide des actions http-request et http-response correspondantes.

### 6.2.1. Section cache {#section-6-2-1}

<a id="entry-6-2-1-cache"></a>

**`cache <name>`**

```haproxy
cache <name>
```

Déclare une section de cache, alloue une mémoire de cache partagée nommée `<name>`, la taille du cache est obligatoire (voir le mot-clé "total-max-size" ci-dessous).

<a id="entry-6-2-1-max-age"></a>

**`max-age <seconds>`**

```haproxy
max-age <seconds>
```

Définir la durée maximale d'expiration. L'expiration est fixée à la valeur la plus faible entre les directives s-maxage ou max-age (dans cet ordre) présentes dans l'en-tête de réponse Cache-Control et cette valeur. La valeur par défaut est de 60 secondes, ce qui signifie que vous ne pouvez pas mettre en cache un objet plus de 60 secondes par défaut.

<a id="entry-6-2-1-max-object-size"></a>

**`max-object-size <bytes>`**

```haproxy
max-object-size <bytes>
```

Définir la taille maximale des objets à mettre en cache. Ne doit pas dépasser la moitié de « total-max-size ». Si elle n'est pas définie, elle est égale à 1/256 de la taille du cache. Tous les objets dont la taille dépasse « max-object-size » ne seront pas mis en cache.

<a id="entry-6-2-1-max-secondary-entries"></a>

**`max-secondary-entries <number>`**

```haproxy
max-secondary-entries <number>
```

Définir le nombre maximal d'entrées secondaires simultanées ayant la même clé primaire dans le cache.
Cela nécessite que le support de vary soit activé. Sa valeur par défaut est 10 et il est recommandé de lui passer un entier strictement positif.

<a id="entry-6-2-1-process-vary"></a>

**`process-vary <on/off>`**

```haproxy
process-vary <on/off>
```

Active ou désactive le traitement de l’en-tête Vary. Lorsqu’il est désactivé, une réponse contenant cet en-tête n’est jamais mise en cache. Lorsqu’il est activé, il faut calculer un hachage préliminaire pour un sous-ensemble des en-têtes de requête sur toutes les requêtes entrantes (ce qui peut entraîner une charge CPU) afin de construire une clé secondaire pour une requête donnée (voir RFC 7234#4.1). La clé secondaire est actuellement construite à partir du contenu des en-têtes « accept-encoding », « referer » et « origin ». Notez que les en-têtes « origin » et « referer » sont univalués selon la RFC, donc une requête comportant plusieurs occurrences de l’un ou l’autre devrait être considérée comme malformée. Pour de telles requêtes, aucune clé secondaire n’est construite, et la réponse n’est jamais servie depuis le cache, afin de laisser le serveur décider de la manière de traiter la situation. La valeur par défaut est off (désactivé).

<a id="entry-6-2-1-total-max-size"></a>

**`total-max-size <megabytes>`**

```haproxy
total-max-size <megabytes>
```

Définir la taille en mémoire RAM du cache en mégaoctets. Cette taille est divisée en blocs de 1 ko, utilisés par les entrées du cache. Sa valeur maximale est 4095.

### 6.2.2. Section proxy {#section-6-2-2}

La section proxy utilisant le cache devra inclure l’action « cache-use » dans le jeu de règles « http-request » afin de rechercher l’objet demandé dans le cache, et l’action « cache-store » dans le jeu de règles « http-response » afin de stocker ou mettre à jour l’objet récupéré dans le cache. Chacune de ces actions peut éventuellement être soumise à des conditions. Par exemple, on peut décider de passer outre l’action « cache-use » pour un sous-répertoire donné connu pour ne pas être mis en cache, ou de passer outre l’action « cache-store » pour certains types de contenu connus pour être sans intérêt. Veuillez noter que la clé d’indexation du cache est calculée lors de l’action « cache-use », donc si cette action est omise, aucune tentative de mise à jour du cache ne sera effectuée sur le chemin de la réponse.

Exemple :

```text
backend bck1
  mode http

  http-request cache-use foobar
  http-response cache-store foobar
  server srv1 127.0.0.1:80

cache foobar
  total-max-size 4
  max-age 240
```
