---
title: "Traitement parallèle"
linkTitle: "Traitement parallèle"
weight: 50
description: "Choisissez entre des tronçons parallèles d'un seul journal ou un traitement parallèle de plusieurs journaux"
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [Tâche]
aliases: [/docs/pgbadger/parallel-processing/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger dispose de deux modes de traitement parallèle complémentaires. Choisissez selon la forme de l'entrée, et non simplement selon le nombre de processeurs.

| Option | Unité parallèle | Meilleur ajustement | Contrainte principale |
|---|---|---|---|
| `-j N` / `--jobs N` | tronçons d'un fichier journal | un seul fichier journal volumineux et accessible par recherche | les limites des tronçons peuvent dupliquer ou omettre un petit nombre de requêtes |
| `-J N` / `--Jobs N` | fichiers journaux entiers | plusieurs fichiers journaux indépendants | utile uniquement lorsque suffisamment de fichiers sont disponibles pour garder les workers occupés |

## Découper un grand fichier avec `-j` {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

L'algorithme upstream divise chaque fichier en plages de `N` octets, lance un parseur par plage, écrit des statistiques binaires temporaires, puis fusionne ces statistiques pour produire le rapport final.

```text
for each log file
    divide the file into N chunks
    find each chunk's start and end offsets
    fork N parsers at those offsets
    write one temporary binary statistics file per parser
wait for the workers
merge the binary files and build the report
```

Étant donné que les enregistrements de journal et les requêtes multilignes ne correspondent pas parfaitement aux décalages d’octets, jusqu’à environ `N` requêtes par fichier peuvent être tronquées, omises ou, plus fréquemment, comptées deux fois aux limites des tronçons. Utilisez ce mode pour une analyse agrégée de fichiers très volumineux, et non pour un flux de travail nécessitant un décompte précis de chaque enregistrement.

## Traiter plusieurs fichiers avec `-J` {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

Chaque worker possède un fichier complet, ce qui permet d’éviter les lacunes aux limites des tronçons. Ce mode devient particulièrement utile avec des centaines de petits fichiers et une capacité CPU et E/S suffisante. La documentation officielle autorise également `-J` pour des fichiers compressés indépendants ; le découpage en tronçons sur un seul fichier avec `-j` nécessite une entrée accessible par recherche, non compressée.

## Benchmark côté serveur {#benchmark}

Le manuel d'origine indique ces mesures sur un hôte à 8 processeurs. Considérez-les comme une comparaison entre les deux algorithmes, et non comme une prédiction pour le matériel actuel.

Un fichier de 9,5 Go :

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 1h41m18 | 50m25 | 25m39 | 15m58 |
| `-J` | 1h41m18 | 54m28 | 41m16 | 34m45 |

Deux cents fichiers de 10 Mo, soit 2 Go au total :

| Option | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 20m15 | 9m56 | 5m20 | 4m20 |
| `-J` | 20m15 | 9m49 | 5m00 | 2m40 |

La valeur par défaut pratique est `-j` pour quelques fichiers volumineux et `-J` pour de nombreux fichiers petits. Les deux modes peuvent être combinés lorsque l'entrée et la plateforme le permettent, mais testez cette combinaison : l'analyse des journaux peut devenir limitée par le débit de stockage avant le processeur.

## Limites et fichiers temporaires {#limits-and-temporary-files}

- `-j` n'est pas disponible pour les entrées compressées ou au format CSV et repose sur la duplication de processus, il n'est donc pas compatible avec Windows.
- La lecture distante de fichiers CSV n'est pas prise en charge par le chemin d'entrée distante du projet principal.
- L'analyse parallèle crée des fichiers temporaires nommés comme `tmp_pgbadgerXXXX.bin` dans le répertoire temporaire sélectionné (par défaut, le répertoire temporaire du système).
- Ne supprimez pas ces fichiers pendant l'exécution de pgBadger. Utilisez `--tempdir` pour les placer sur un stockage disposant d'une capacité suffisante.
- Commencez avec un nombre modeste de workers et surveillez la charge CPU, le débit de lecture, la consommation d'espace temporaire et le temps écoulé.
