---
title: "Formats de sortie"
linkTitle: "Formats de sortie"
weight: 70
description: "Choisissez une sortie HTML, texte, binaire, JSON ou CSV brut et combinez les fichiers intermédiaires"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [Référence]
aliases: [/pgbadger/output-formats/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger sélectionne la sortie en fonction de l'extension du nom de fichier ou de `-x` / `--extension`. Utilisez `-o` / `--outfile` plus d'une fois pour générer plusieurs formats à partir de la même analyse.

| Format | Extension typique | Meilleur usage |
|---|---|---|
| HTML | `.html` | rapport interactif avec graphiques, destiné à la lecture humaine |
| Texte | `.txt` | consultation dans un terminal et archivage en texte brut |
| Binaire | `.bin` | statistiques intermédiaires fusionnables et reconstructions de rapport |
| JSON | `.json` | intégration avec d’autres logiciels ; nécessite `JSON::XS` |
| CSV brut | fichier de sortie choisi | extraction orientée ligne avec `--dump-raw-csv` |

## HTML et texte {#html-and-text}

La sortie par défaut est `out.html` :

```console
$ pgbadger postgresql.log -o report.html
```

HTML intègre normalement les scripts, styles, polices et données de rapport nécessaires à la visualisation autonome. `-X` / `--extra-files` déplace les ressources JavaScript et CSS partagées hors des rapports incrémentiels ; conservez ces ressources à côté de l’arborescence HTML.

Spécifiez explicitement une sortie texte :

```console
$ pgbadger -x text -o report.txt postgresql.log
```

Utilisez `-` comme nom de fichier de sortie pour écrire un format pris en charge sur la sortie standard.

## Données intermédiaires binaires {#binary-format}

La sortie binaire sépare l'analyse de la présentation. Générez des incréments horaires à partir d'un journal quotidien en croissance :

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

Fusionnez un ou plusieurs fichiers binaires dans un nouveau rapport :

```console
$ pgbadger -o sunday.html sunday/*.bin
```

Lorsque le serveur écrit un fichier journal par heure, créez un fichier binaire pour chaque rotation, puis reconstruisez le fichier HTML cumulatif chaque fois que nécessaire :

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

Gardez les fichiers binaires provenant de versions compatibles de pgBadger ensemble. Consultez les notes de version pour la compatibilité des formats incrémentiels avant de mettre à jour un répertoire de rapports à long terme.

## JSON {#json-format}

La sortie JSON est destinée aux programmes qui traitent les données, tels que les chaînes de supervision ou de génération de rapports :

```console
$ pgbadger -o report.json postgresql.log
```

Installez `JSON::XS` en premier. Ajoutez `--prettify-json` pour améliorer la lisibilité lorsque la taille du fichier et le temps de génération sont secondaires.

## Exports bruts et orientés requêtes {#raw-exports}

La référence de commande fournit également des exports spécialisés :

- `--dump-raw-csv` analyse le journal et écrit un fichier CSV orienté ligne sans générer de rapport ;
- `--csv-separator` change le délimiteur du CSV brut ; la version 13.2 utilise la virgule par défaut ;
- `--dump-all-queries` émet chaque requête après avoir remplacé les paramètres liés ;
- `--normalized-only` écrit les requêtes normalisées ;
- `--query-numbering` numérote la sortie texte orientée requête.

Ces modes peuvent contenir du SQL d'application, des identificateurs, des utilisateurs, des adresses clientes ou des valeurs littérales. Examinez la sortie avant de la partager et utilisez `--anonymize` lorsque l'analyse prévue ne nécessite pas de valeurs littérales.
