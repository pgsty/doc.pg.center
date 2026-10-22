---
title: "Référence en ligne de commande"
linkTitle: "Ligne de commande"
weight: 30
description: "Syntaxe complète de la commande pgBadger, options, entrée distante, codes de retour et exemples"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Référence]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

## Utilisation et options {#usage-and-options}

Utilisation : pgbadger [options] logfile [...]

```text
Analyseur de journaux PostgreSQL avec rapports et graphiques détaillés.
```

Arguments :

```text
logfile peut désigner un fichier journal, une liste de fichiers ou une commande
shell qui renvoie une liste de fichiers. Pour lire le contenu sur stdin,
utilisez - comme nom de fichier. L’entrée sur stdin ne fonctionne pas avec csvlog.
```

Options :

```text
-a | --average minutes : nombre de minutes par intervalle des graphiques de
                         moyenne des requêtes et des connexions. Valeur par défaut : 5 minutes.
-A | --histo-average min: nombre de minutes par intervalle des histogrammes
                         de requêtes. Valeur par défaut : 60 minutes.
-b | --begin datetime  : date/heure de début des données à analyser dans le
                         journal (horodatage ou heure).
-c | --dbclient host   : ne rapporter que les entrées de l’hôte client
                         indiqué.
-C | --nocomment       : supprimer des requêtes les commentaires tels que
                         /* ... */.
-d | --dbname database : ne rapporter que les entrées de la base de données
                         indiquée.
-D | --dns-resolv      : remplacer les adresses IP clientes par leur nom
                         DNS. Attention, cela peut fortement ralentir pgBadger.
-e | --end datetime    : date/heure de fin des données à analyser dans le
                         journal (horodatage ou heure).
-E | --explode         : scinder le rapport principal en un rapport par base
                         de données. Les informations globales sans lien avec une base de données
                         sont ajoutées au rapport de la base postgres.
-f | --format logtype  : valeurs possibles : syslog, syslog2, stderr,
                         jsonlog, csv, pgbouncer, logplex, rds et redshift. À utiliser si pgBadger
                         ne détecte pas le format du journal.
-G | --nograph         : désactiver les graphiques dans la sortie HTML. Les
                         graphiques sont activés par défaut.
-h | --help            : afficher cette aide puis quitter.
-H | --html-outdir path: répertoire des rapports HTML en mode incrémentiel.
                         Les fichiers binaires restent dans le répertoire défini par -O, --outdir.
-i | --ident name      : nom du programme utilisé comme identifiant syslog.
                         Valeur par défaut : postgres.
-I | --incremental     : activer le mode incrémentiel ; les rapports
                         quotidiens sont générés dans des répertoires séparés. --outdir doit être
                         défini.
-j | --jobs number     : nombre de tâches simultanées pour un seul fichier
                         journal. Une seule tâche par défaut ou avec le format csvlog.
-J | --Jobs number     : nombre de fichiers journaux à analyser en
                         parallèle. Un seul fichier à la fois par défaut.
-l | --last-parsed file: permettre l’analyse incrémentielle en enregistrant
                         la dernière date/heure et la dernière ligne analysées. Utile pour examiner
                         les erreurs depuis la dernière exécution ou produire un rapport quotidien
                         sur un journal à rotation hebdomadaire.
-L | --logfile-list file: fichier contenant la liste des journaux à
                         analyser.
-m | --maxlength size  : longueur maximale d’une requête ; les requêtes plus
                         longues sont tronquées. Valeur par défaut : 100000.
-M | --no-multiline    : ne pas collecter les instructions multilignes afin
                         d’éviter du contenu parasite, notamment les erreurs qui produisent un
                         rapport énorme.
-N | --appname name    : ne rapporter que les entrées de l’application
                         indiquée.
-o | --outfile filename: nom du fichier de sortie. Selon le format :
                         out.html, out.txt, out.bin ou out.json par défaut. Peut être répété pour
                         produire plusieurs formats. JSON nécessite le module Perl JSON::XS.
                         Utiliser - comme nom de fichier pour écrire sur stdout.
-O | --outdir path     : répertoire où enregistrer les fichiers de sortie.
-p | --prefix string   : valeur exacte de log_line_prefix dans
                         postgresql.conf. À utiliser uniquement si le préfixe diffère des formes
                         standard documentées, par exemple avec des champs supplémentaires d’IP
                         cliente ou d’application. DOIT contenir les séquences temporelles (%t, %m
                         ou %n) et de processus (%p ou %c). Voir les exemples ci-dessous.
-P | --no-prettify     : désactiver la mise en forme des requêtes SQL.
-q | --quiet           : ne rien écrire sur stdout, pas même une barre de
                         progression.
-Q | --query-numbering : numéroter les requêtes avec --dump-all-queries ou
                         --normalized-only.
-r | --remote-host ip  : hôte où exécuter cat sur le journal distant afin de
                         l’analyser localement.
-R | --retention N     : nombre de semaines à conserver en mode
                         incrémentiel. Valeur par défaut : 0, désactivé. Les anciens répertoires de
                         semaines et de jours sont supprimés automatiquement du répertoire de
                         sortie.
-s | --sample number   : nombre d’exemples de requêtes à conserver. Valeur
                         par défaut : 3.
-S | --select-only     : ne rapporter que les requêtes SELECT.
-t | --top number      : nombre de requêtes à conserver/afficher. Valeur par
                         défaut : 20.
-T | --title string    : modifier le titre de la page HTML du rapport.
-u | --dbuser username : ne rapporter que les entrées de l’utilisateur
                         indiqué.
-U | --exclude-user username : exclure du rapport les entrées de
                         l’utilisateur indiqué. Peut être répété.
-v | --verbose         : activer le mode détaillé ou de débogage. Désactivé
                         par défaut.
-V | --version         : afficher la version de pgBadger puis quitter.
-w | --watch-mode      : ne rapporter que les erreurs, comme logwatch.
                         Les entrées SSH sont filtrées sur l’hôte distant.
-W | --wide-char       : encoder les requêtes de la sortie HTML en UTF8 pour
                         éviter le message Perl "Wide character in print".
-x | --extension       : format de sortie : text, html, bin ou json. Valeur
                         par défaut : html.
-X | --extra-files     : en mode incrémentiel, écrire CSS et JS dans des
                         fichiers séparés du répertoire de sortie.
-z | --zcat exec_path  : chemin complet du programme zcat. À utiliser si
                         zcat, bzcat ou unzip n’est pas dans votre PATH.
-Z | --timezone +/-XX  : décalage horaire par rapport à GMT pour ajuster les
                         dates/heures des graphiques JavaScript. Entier, par exemple 2, ou nombre
                         décimal, par exemple 2.5.
--anonymize            : masquer tous les littéraux des requêtes afin de
                         cacher les données confidentielles.
--charset              : jeu de caractères HTML à utiliser. Valeur par
                         défaut : utf-8.
--command CMD          : commande qui fournit les entrées de journal sur
                         stdin. pgBadger ouvre un tube vers cette commande et analyse les entrées
                         qu’elle produit.
--csv-separator        : séparateur de champs CSV. Valeur par défaut : ,
--day-report YYYY-MM-DD: générer un rapport HTML pour le jour indiqué.
                         Nécessite les répertoires de sortie incrémentielle et tous les fichiers de
                         données binaires requis.
--disable-autovacuum   : ne pas générer le rapport d’autovacuum.
--disable-checkpoint   : ne pas générer le rapport de
                         checkpoint/restartpoint.
--disable-connection   : ne pas générer le rapport de connexions.
--disable-error        : ne pas générer le rapport d’erreurs.
--disable-hourly       : ne pas générer le rapport horaire.
--disable-lock         : ne pas générer le rapport de verrous.
--disable-query        : ne pas générer les rapports de requêtes (les plus
                         lentes, les plus fréquentes, par utilisateur, par base de données, etc.).
--disable-session      : ne pas générer le rapport de sessions.
--disable-temporary    : ne pas générer le rapport de fichiers temporaires.
--disable-type         : ne pas générer le rapport des requêtes par type,
                         base de données ou utilisateur.
--dump-all-queries     : émettre toutes les requêtes du journal après avoir
                         remplacé les paramètres liés à leur position respective.
--dump-raw-csv         : analyser le journal et exporter les informations au
                         format CSV. Aucun autre traitement ni rapport.
--enable-checksum      : ajouter une somme md5 sous chaque rapport de
                         requête.
--exclude-appname name : exclure du rapport les entrées de l’application
                         indiquée, par exemple "pg_dump". Peut être répété.
--exclude-client name  : exclure les entrées de l’adresse IP cliente
                         indiquée. Peut être répété.
--exclude-db name      : exclure du rapport les entrées de la base de
                         données indiquée, par exemple "postgres". Peut être répété.
--exclude-file filename: fichier contenant les expressions régulières des
                         requêtes à exclure du rapport. Une expression par ligne.
--exclude-line regex   : exclure les entrées de journal correspondant à
                         l’expression régulière. Peut être répété.
--exclude-query regex  : exclure les requêtes correspondant à l’expression
                         régulière, par exemple "^(VACUUM|COMMIT)". Peut être répété.
--exclude-time  regex  : exclure les horodatages correspondant à
                         l’expression régulière, par exemple "2013-04-12 .*". Peut être répété.
--explain-url URL      : remplacer l’URL de l’outil graphique EXPLAIN.
                         Valeur par défaut : https://explain.depesz.com/
--histogram-query VAL  : utiliser des bornes personnalisées pour
                         l’histogramme des durées de requête. Bornes par défaut en millisecondes :
                         0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: utiliser des bornes personnalisées pour
                         l’histogramme des durées de session. Bornes par défaut en millisecondes :
                         0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: fichier contenant les expressions régulières des
                         requêtes à inclure dans le rapport. Une expression par ligne.
--include-query regex  : exclure les requêtes qui ne correspondent pas à
                         l’expression régulière. Peut être répété, par exemple "(tbl1|tbl2)".
--include-pid PID      : ne rapporter que les événements liés au PID de
                         session (%p). Peut être répété.
--include-session ID   : ne rapporter que les événements liés à
                         l’identifiant de session (%c). Peut être répété.
--include-time  regex  : inclure uniquement les horodatages correspondant à
                         l’expression régulière, par exemple "2013-04-12 .*". Peut être répété.
--iso-week-number      : en mode incrémentiel, faire commencer les semaines
                         le lundi selon ISO 8601, numérotées de 01 à 53. La semaine 1 est la
                         première contenant au moins 4 jours de la nouvelle année.
--keep-comments        : conserver les commentaires dans les requêtes
                         normalisées, afin de distinguer des requêtes ayant la même forme
                         normalisée.
--journalctl command   : remplacer le fichier journal PostgreSQL par un
                         appel à journalctl, par exemple :
                         journalctl -u postgresql-9.5
--log-duration         : forcer pgBadger à associer les entrées produites
                         par log_duration = on et log_statement = 'all'.
--log-timezone +/-XX   : décalage horaire par rapport à GMT pour ajuster les
                         dates/heures du journal avant analyse. Cela complique les recherches par
                         date/heure. Entier, par exemple 2, ou nombre décimal, par exemple 2.5.
--month-report YYYY-MM : générer un rapport HTML cumulatif pour le mois
                         indiqué. Nécessite les répertoires de sortie incrémentielle et tous les
                         fichiers de données binaires requis.
--noexplain            : ne pas traiter les lignes générées par
                         auto_explain.
--no-fork              : ne créer aucun processus fils, à des fins de
                         débogage.
--no-process-info      : ne pas modifier le titre du processus pour
                         identifier pgBadger, car certains systèmes ne le prennent pas en charge.
--no-progressbar       : désactiver la barre de progression.
--noreport             : ne générer aucun rapport en mode incrémentiel.
--no-week              : ne pas générer les rapports hebdomadaires en mode
                         incrémentiel, s’ils prennent trop de temps.
--normalized-only      : émettre uniquement les requêtes normalisées dans
                         out.txt.
--pgbouncer-only       : afficher uniquement les menus liés à PgBouncer dans
                         l’en-tête.
--pid-dir path         : répertoire où stocker le fichier PID. Valeur par
                         défaut : /tmp
--pid-file file        : nom du fichier PID qui contrôle les exécutions
                         simultanées de pgBadger. Valeur par défaut : pgbadger.pid
--pie-limit num        : regrouper en une somme les portions de camembert
                         inférieures à num%.
--prettify-json        : mettre en forme la sortie JSON pour améliorer sa
                         lisibilité.
--rebuild              : reconstruire tous les rapports HTML des répertoires
                         de sortie incrémentielle contenant des données binaires.
--start-monday         : en mode incrémentiel, les semaines commencent par
                         défaut le dimanche. Cette option les fait commencer le lundi.
--tempdir DIR          : répertoire des fichiers temporaires. Valeur par
                         défaut : File::Spec->tmpdir() || '/tmp'
```

pgBadger est capable d'analyser un fichier journal distant en utilisant une connexion SSH sans mot de passe.
Utilisez -r ou --remote-host pour définir l'adresse IP ou le nom d'hôte du serveur. Il existe également plusieurs options supplémentaires pour contrôler entièrement la connexion SSH.

En mode de surveillance (`-w`), les fichiers journaux lus par SSH sont filtrés sur l’hôte distant avant leur transfert. Les enregistrements CSV sont filtrés avec `awk`, en préservant les champs multilignes. Ce comportement fait partie de l’instantané de développement postérieur à la version 13.2 documenté ici.

```text
--ssh-identity file      chemin du fichier d’identité à utiliser.
--ssh-option  options    liste des options -o de la connexion SSH. Options
                         toujours utilisées :
                         -o ConnectTimeout=$ssh_timeout
                         -o PreferredAuthentications=hostbased,publickey
--ssh-port port          port SSH de la connexion. Valeur par défaut : 22.
--ssh-program ssh        chemin du programme SSH. Valeur par défaut : ssh.
--ssh-timeout second     délai d’échec de connexion SSH. Valeur par défaut : 10
                         secondes.
--ssh-user username      nom de connexion. Par défaut : utilisateur qui exécute
                         pgBadger.
```

L’option `--ssh-sudo` préfixe par `sudo` les commandes distantes qui listent et lisent les fichiers journaux. L’utilisateur SSH distant doit pouvoir exécuter ces commandes avec `sudo` sans invite interactive.

Le fichier journal à analyser peut également être spécifié à l’aide d’un URI. Les protocoles pris en charge sont http[s] et [s]ftp. La commande curl sera utilisée pour télécharger le fichier, qui sera analysé pendant le téléchargement. Le protocole ssh est également pris en charge et utilisera la commande ssh, de la même manière qu’avec un hôte distant. Voir les exemples ci-dessous.

Codes de retour :

```text
0: succès
1: arrêt sur erreur
2: interruption, par exemple avec Ctrl+C
3: le fichier PID existe déjà ou ne peut pas être créé
4: aucun fichier journal fourni en ligne de commande
```

Exemples :

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# Préfixe de ligne pour une sortie de journal stderr
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# Préfixe de ligne pour une sortie de journal syslog
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# Utiliser 8 CPU pour analyser plus rapidement un fichier de 10GB
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

Utilisez la notation URI pour le fichier journal distant :

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

Vous pouvez utiliser conjointement un fichier journal PostgreSQL local et un fichier journal pgbouncer distant pour analyser :

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

Rapporter les erreurs chaque semaine par une tâche cron :

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

Générez un rapport chaque semaine en utilisant le comportement incrémental :

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

Cela suppose que votre fichier journal et le rapport HTML sont également rotés chaque semaine.

Ou mieux, utilisez les rapports incrémentiels générés automatiquement :

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

générera un rapport par jour et par semaine.

En mode incrémental, vous pouvez également préciser le nombre de semaines à conserver dans les rapports :

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Si vous disposez d’un pg_dump à 23:00 et à 13:00 chaque jour pendant une demi-heure, vous pouvez utiliser pgBadger comme suit pour exclure ces périodes du rapport :

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

Cette expression exclut chaque heure correspondante en entier, y compris le temps en dehors de la demi-heure de sauvegarde. Restreignez le motif des minutes si seule la période de sauvegarde doit être exclue.

Cela permettra d'éviter d'avoir des instructions COPY, générées par pg_dump, en tête de la liste des requêtes les plus lentes. Vous pouvez également utiliser --exclude-appname "pg_dump" pour résoudre ce problème de manière plus simple.

Vous pouvez également analyser la sortie de journalctl comme si elle était un fichier journal :

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

ou, dans le pire des cas, exécutez-le depuis un hôte distant :

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

Vous n'avez pas besoin de spécifier de fichier journal en ligne de commande, mais si vous avez d'autres fichiers journaux PostgreSQL à analyser, vous pouvez les ajouter comme d'habitude.

Pour reconstruire tous les rapports HTML incrémentaux après coup, procédez comme suit :

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

Il mettra également à jour tous les fichiers de ressources (JS et CSS). Utilisez -E ou --explode si les rapports ont été générés en utilisant cette option.

pgBadger prend également en charge les journaux PostgreSQL Heroku au format logplex :

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

Cela enverra les journaux Heroku PostgreSQL à pgBadger via stdin.

pgBadger peut détecter automatiquement les journaux PostgreSQL RDS et CloudWatch en utilisant le format rds :

```text
pgbadger -f rds -o rds_out.html rds.log
```

Chaque journal CloudSQL PostgreSQL est un journal PostgreSQL relativement classique, mais encapsulé au format JSON. Il est détecté automatiquement par pgBadger, mais en cas de besoin, forcez le format de journalisation en utilisant `jsonlog` :

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

Cela fonctionne de la même manière que l'extension jsonlog : le format JSON est différent, mais pgBadger peut parser les deux formats.

pgBadger prend également en charge les journaux produits par l'opérateur Postgres CloudNativePG pour Kubernetes :

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

Pour créer un rapport cumulatif sur une période d’un mois, utilisez la commande :

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

Cela ajoutera un lien vers le nom du mois dans la vue calendrier des rapports incrémentiels pour consulter le rapport du mois de mai 2019.
Utilisez -E ou --explode si les rapports ont été générés en utilisant cette option.
