---
title: "Traitement parallèle"
linkTitle: "Traitement parallèle"
weight: 50
description: "Choisissez entre le découpage parallèle d'un seul journal et le traitement parallèle de plusieurs journaux"
search_keywords: [--Jobs, --jobs, --tempdir, Jobs, jobs, tempdir]
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [Tâche]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger dispose de deux modes de traitement parallèle complémentaires. Choisissez selon la structure des données d'entrée, et non simplement selon le nombre de processeurs.

| Option | Unité parallèle | Cas adapté | Contrainte principale |
|---|---|---|---|
| `-j N` / `--jobs N` | tronçons d'un fichier journal | un seul fichier journal volumineux et permettant un accès direct aux positions dans le fichier | les limites des tronçons peuvent dupliquer ou omettre un petit nombre de requêtes |
| `-J N` / `--Jobs N` | fichiers journaux entiers | plusieurs fichiers journaux indépendants | utile uniquement lorsque suffisamment de fichiers sont disponibles pour occuper les processus de travail |

## Découper un grand fichier avec `-j` {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

L'algorithme du projet amont divise chaque fichier en `N` plages d'octets, lance un parseur par plage, écrit des statistiques binaires temporaires, puis fusionne ces statistiques pour produire le rapport final.

```text
pour chaque fichier journal
    diviser le fichier en N tronçons
    trouver les positions de début et de fin de chaque tronçon
    créer N processus d’analyse à ces positions
    écrire un fichier temporaire de statistiques binaires par processus
attendre la fin des processus de travail
fusionner les fichiers binaires et générer le rapport
```

Étant donné que les enregistrements de journal et les requêtes multilignes ne correspondent pas parfaitement aux décalages d’octets, jusqu’à environ `N` requêtes par fichier peuvent être tronquées, omises ou, plus fréquemment, comptées deux fois aux limites des tronçons. Utilisez ce mode pour une analyse agrégée de fichiers très volumineux, et non pour un flux de travail nécessitant un décompte précis de chaque enregistrement.

## Traiter plusieurs fichiers avec `-J` {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

Chaque processus de travail traite un fichier complet, ce qui permet d’éviter les lacunes aux limites des tronçons. Ce mode devient particulièrement utile avec des centaines de petits fichiers et une capacité CPU et E/S suffisante. La documentation officielle autorise également `-J` pour des fichiers compressés indépendants ; le découpage en tronçons sur un seul fichier avec `-j` nécessite une entrée permettant un accès direct aux positions dans le fichier, non compressée.

## Benchmark du projet amont {#benchmark}

Le manuel du projet amont indique ces mesures sur un hôte à 8 processeurs. Considérez-les comme une comparaison entre les deux algorithmes, et non comme une prédiction pour le matériel actuel.

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

En pratique, privilégiez `-j` pour quelques fichiers volumineux et `-J` pour de nombreux petits fichiers. Les deux modes peuvent être combinés lorsque l'entrée et la plateforme le permettent, mais testez cette combinaison : l'analyse des journaux peut devenir limitée par le débit de stockage avant le processeur.

## Limites et fichiers temporaires {#limits-and-temporary-files}

- `-j` n'est pas disponible pour les entrées compressées ou au format CSV et repose sur la duplication de processus, il n'est donc pas compatible avec Windows.
- Pour les journaux distants autres que CSV, utilisez le traitement par fichier entier avec `-J` ; le découpage d’un fichier avec `-j` nécessite une entrée locale autorisant le positionnement dans le fichier. Les journaux CSV peuvent être lus par SSH ; dans l’instantané de développement postérieur à la version 13.2 documenté ici, le mode de surveillance (`-w`) filtre les enregistrements CSV sur l’hôte distant avec `awk`, en préservant les champs multilignes. Consultez les [options de lecture distante](/fr/pgbadger/command-line/).
- L'analyse parallèle crée des fichiers temporaires nommés comme `tmp_pgbadgerXXXX.bin` dans le répertoire temporaire sélectionné (par défaut, le répertoire temporaire du système).
- Ne supprimez pas ces fichiers pendant l'exécution de pgBadger. Utilisez `--tempdir` pour les placer sur un stockage disposant d'une capacité suffisante.
- Commencez avec un nombre modeste de processus de travail et surveillez la charge CPU, le débit de lecture, la consommation d'espace temporaire et le temps écoulé.
