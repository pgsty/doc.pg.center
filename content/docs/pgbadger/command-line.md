---
title: "Command-Line Reference"
linkTitle: "Command Line"
weight: 30
description: "Complete pgBadger command syntax, options, remote input, return codes, and examples"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Reference]
aliases: [/pgbadger/command-line/]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## Usage and options {#usage-and-options}

Usage: pgbadger [options] logfile [...]

```text
PostgreSQL log analyzer with fully detailed reports and graphs.
```

Arguments:

```text
logfile can be a single log file, a list of files, or a shell command
returning a list of files. If you want to pass log content from stdin
use - as filename. Note that input from stdin will not work with csvlog.
```

Options:

```text
-a | --average minutes : number of minutes to build the average graphs of
                         queries and connections. Default 5 minutes.
-A | --histo-average min: number of minutes to build the histogram graphs
                         of queries. Default 60 minutes.
-b | --begin datetime  : start date/time for the data to be parsed in log
                         (either a timestamp or a time)
-c | --dbclient host   : only report on entries for the given client host.
-C | --nocomment       : remove comments like /* ... */ from queries.
-d | --dbname database : only report on entries for the given database.
-D | --dns-resolv      : client ip addresses are replaced by their DNS name.
                         Be warned that this can really slow down pgBadger.
-e | --end datetime    : end date/time for the data to be parsed in log
                         (either a timestamp or a time)
-E | --explode         : explode the main report by generating one report
                         per database. Global information not related to a
                         database is added to the postgres database report.
-f | --format logtype  : possible values: syslog, syslog2, stderr, jsonlog,
                         csv, pgbouncer, logplex, rds and redshift. Use this
                         option when pgBadger is not able to detect the log
                         format.
-G | --nograph         : disable graphs on HTML output. Enabled by default.
-h | --help            : show this message and exit.
-H | --html-outdir path: path to directory where HTML report must be written
                         in incremental mode, binary files stay on directory
                         defined with -O, --outdir option.
-i | --ident name      : programname used as syslog ident. Default: postgres
-I | --incremental     : use incremental mode, reports will be generated by
                         days in a separate directory, --outdir must be set.
-j | --jobs number     : number of jobs to run at same time for a single log
                         file. Run as single by default or when working with
                         csvlog format.
-J | --Jobs number     : number of log files to parse in parallel. Process
                         one file at a time by default.
-l | --last-parsed file: allow incremental log parsing by registering the
                         last datetime and line parsed. Useful if you want
                         to watch errors since last run or if you want one
                         report per day with a log rotated each week.
-L | --logfile-list file:file containing a list of log files to parse.
-m | --maxlength size  : maximum length of a query, it will be restricted to
                         the given size. Default truncate size is 100000.
-M | --no-multiline    : do not collect multiline statements to avoid garbage
                         especially on errors that generate a huge report.
-N | --appname name    : only report on entries for given application name
-o | --outfile filename: define the filename for the output. Default depends
                         on the output format: out.html, out.txt, out.bin,
                         or out.json. This option can be used multiple times
                         to output several formats. To use json output, the
                         Perl module JSON::XS must be installed, to dump
                         output to stdout, use - as filename.
-O | --outdir path     : directory where out files must be saved.
-p | --prefix string   : the value of your custom log_line_prefix as
                         defined in your postgresql.conf. Only use it if you
                         aren't using one of the standard prefixes specified
                         in the pgBadger documentation, such as if your
                         prefix includes additional variables like client IP
                         or application name. MUST contain escape sequences
                         for time (%t, %m or %n) and processes (%p or %c).
                         See examples below.
-P | --no-prettify     : disable SQL queries prettify formatter.
-q | --quiet           : don't print anything to stdout, not even a progress
                         bar.
-Q | --query-numbering : add numbering of queries to the output when using
                         options --dump-all-queries or --normalized-only.
-r | --remote-host ip  : set the host where to execute the cat command on
                         remote log file to parse the file locally.
-R | --retention N     : number of weeks to keep in incremental mode. Defaults
                         to 0, disabled. Used to set the number of weeks to
                         keep in output directory. Older weeks and days
                         directories are automatically removed.
-s | --sample number   : number of query samples to store. Default: 3.
-S | --select-only     : only report SELECT queries.
-t | --top number      : number of queries to store/display. Default: 20.
-T | --title string    : change title of the HTML page report.
-u | --dbuser username : only report on entries for the given user.
-U | --exclude-user username : exclude entries for the specified user from
                         report. Can be used multiple time.
-v | --verbose         : enable verbose or debug mode. Disabled by default.
-V | --version         : show pgBadger version and exit.
-w | --watch-mode      : only report errors just like logwatch could do.
-W | --wide-char       : encode html output of queries into UTF8 to avoid
                         Perl message "Wide character in print".
-x | --extension       : output format. Values: text, html, bin or json.
                         Default: html
-X | --extra-files     : in incremental mode allow pgBadger to write CSS and
                         JS files in the output directory as separate files.
-z | --zcat exec_path  : set the full path to the zcat program. Use it if
                         zcat, bzcat or unzip is not in your path.
-Z | --timezone +/-XX  : Set the number of hours from GMT of the timezone.
                         Use this to adjust date/time in JavaScript graphs.
                         The value can be an integer, ex.: 2, or a float,
                         ex.: 2.5.
--anonymize            : obscure all literals in queries, useful to hide
                         confidential data.
--charset              : used to set the HTML charset to be used.
                         Default: utf-8.
--command CMD          : command to execute to retrieve log entries on
                         stdin. pgBadger will open a pipe to the command
                         and parse log entries generated by the command.
--csv-separator        : used to set the CSV field separator, default: ,
--day-report YYYY-MM-DD: create an HTML report over the specified day.
                         Requires incremental output directories and the
                         presence of all necessary binary data files
--disable-autovacuum   : do not generate autovacuum report.
--disable-checkpoint   : do not generate checkpoint/restartpoint report.
--disable-connection   : do not generate connection report.
--disable-error        : do not generate error report.
--disable-hourly       : do not generate hourly report.
--disable-lock         : do not generate lock report.
--disable-query        : do not generate query reports (slowest, most
                         frequent, queries by users, by database, ...).
--disable-session      : do not generate session report.
--disable-temporary    : do not generate temporary report.
--disable-type         : do not generate report of queries by type, database
                         or user.
--dump-all-queries     : dump all queries found in the log file replacing
                         bind parameters included in the queries at their
                         respective placeholders positions.
--dump-raw-csv         : parse the log and dump the information into CSV
                         format. No further processing is done, no report.
--enable-checksum      : used to add an md5 sum under each query report.
--exclude-appname name : exclude entries for the specified application name
                         from report.  Example: "pg_dump".  Can be used
                         multiple times.
--exclude-client name  : exclude log entries for the specified client ip.
                         Can be used multiple times.
--exclude-db name      : exclude entries for the specified database from
                         report. Example: "postgres". Can be used multiple
                         times.
--exclude-file filename: path of the file that contains each regex to use
                         to exclude queries from the report. One regex per
                         line.
--exclude-line regex   : exclude any log entry that will match the given
                         regex. Can be used multiple times.
--exclude-query regex  : any query matching the given regex will be excluded
                         from the report. For example: "^(VACUUM|COMMIT)"
                         You can use this option multiple times.
--exclude-time  regex  : any timestamp matching the given regex will be
                         excluded from the report. Example: "2013-04-12 .*"
                         You can use this option multiple times.
--explain-url URL      : use it to override the url of the graphical explain
                         tool. Default: https://explain.depesz.com/
--histogram-query VAL  : use custom inbound for query times histogram.
                        Default inbound in milliseconds:
                     0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: use custom inbound for session times histogram.
                        Default inbound in milliseconds:
                     0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: path of the file that contains each regex to the
                         queries to include from the report. One regex per
                         line.
--include-query regex  : any query that does not match the given regex will
                         be excluded from the report. You can use this
                         option multiple times. For example: "(tbl1|tbl2)".
--include-pid PID      : only report events related to the session pid (%p).
                         Can be used multiple time.
--include-session ID   : only report events related to the session id (%c).
                         Can be used multiple time.
--include-time  regex  : only timestamps matching the given regex will be
                         included in the report. Example: "2013-04-12 .*"
                         You can use this option multiple times.
--iso-week-number      : in incremental mode, calendar weeks start on
                         Monday and respect the ISO 8601 week number, range
                         01 to 53, where week 1 is the first week that has
                         at least 4 days in the new year.
--keep-comments        : do not remove comments from normalized queries. It
                         can be useful if you want to distinguish between
                         same normalized queries.
--journalctl command   : command to use to replace PostgreSQL logfile by
                         a call to journalctl. Basically it might be:
                            journalctl -u postgresql-9.5
--log-duration         : force pgBadger to associate log entries generated
                         by both log_duration = on and log_statement = 'all'
--log-timezone +/-XX   : Set the number of hours from GMT of the timezone
                         that must be used to adjust date/time read from
                         log file before beeing parsed. Using this option
                         makes log search with a date/time more difficult.
                         The value can be an integer, ex.: 2, or a float,
                         ex.: 2.5.
--month-report YYYY-MM : create a cumulative HTML report over the specified
                         month. Requires incremental output directories and
                         the presence of all necessary binary data files
--noexplain            : do not process lines generated by auto_explain.
--no-fork              : do not fork any process, for debugging purpose.
--no-process-info      : disable changing process title to help identify
                         pgbadger process, some system do not support it.
--no-progressbar       : disable progressbar.
--noreport             : no reports will be created in incremental mode.
--no-week              : inform pgbadger to not build weekly reports in
                         incremental mode. Useful if it takes too much time.
--normalized-only      : only dump all normalized queries to out.txt
--pgbouncer-only       : only show PgBouncer-related menus in the header.
--pid-dir path         : set the path where the pid file must be stored.
                         Default /tmp
--pid-file file        : set the name of the pid file to manage concurrent
                         execution of pgBadger. Default: pgbadger.pid
--pie-limit num        : pie data lower than num% will show a sum instead.
--prettify-json        : use it if you want json output to be prettified.
--rebuild              : used to rebuild all html reports in incremental
                         output directories where there's binary data files.
--start-monday         : in incremental mode, calendar weeks start on
                         Sunday. Use this option to start on a Monday.
--tempdir DIR          : set directory where temporary files will be written
                         Default: File::Spec->tmpdir() || '/tmp'
```

pgBadger is able to parse a remote log file using a passwordless ssh connection.
Use -r or --remote-host to set the host IP address or hostname. There are also
some additional options to fully control the ssh connection.

```text
--ssh-identity file      path to the identity file to use.
--ssh-option  options    list of -o options to use for the ssh connection.
                         Options always used:
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          ssh port to use for the connection. Default: 22.
--ssh-program ssh        path to the ssh program to use. Default: ssh.
--ssh-timeout second     timeout to ssh connection failure. Default: 10 sec.
--ssh-user username      connection login name. Defaults to running user.
```

`--ssh-sudo` prefixes remote file-listing and log-reading commands with `sudo`. The remote SSH user must be able to run those commands through `sudo` without an interactive prompt.

Log file to parse can also be specified using an URI, supported protocols are
http[s] and [s]ftp. The curl command will be used to download the file, and the
file will be parsed during download. The ssh protocol is also supported and will
use the ssh command like with the remote host use. See examples bellow.

Return codes:

```text
0: on success
1: die on error
2: if it has been interrupted using ctr+c for example
3: the pid file already exists or can not be created
4: no log file was given at command line
```

Examples:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# Log line prefix with stderr log output
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# Log line prefix with syslog log output
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# Use my 8 CPUs to parse my 10GB file faster, much faster
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

Use URI notation for remote log file:

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

You can use together a local PostgreSQL log and a remote pgbouncer log file to parse:

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

Reporting errors every week by cron job:

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

Generate report every week using incremental behavior:

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

This supposes that your log file and HTML report are also rotated every week.

Or better, use the auto-generated incremental reports:

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

will generate a report per day and per week.

In incremental mode, you can also specify the number of weeks to keep in the
reports:

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

If you have a pg_dump at 23:00 and 13:00 each day during half an hour, you can
use pgBadger as follow to exclude these periods from the report:

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

This expression excludes each entire matching hour, including time outside the half-hour dump. Narrow the minute pattern if only the dump interval should be excluded.

This will help avoid having COPY statements, as generated by pg_dump, on top of
the list of slowest queries. You can also use --exclude-appname "pg_dump" to
solve this problem in a simpler way.

You can also parse journalctl output just as if it was a log file:

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

or worst, call it from a remote host:

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

you don't need to specify any log file at command line, but if you have other
PostgreSQL log files to parse, you can add them as usual.

To rebuild all incremental html reports after, proceed as follow:

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

it will also update all resource files (JS and CSS). Use -E or --explode
if the reports were built using this option.

pgBadger also supports Heroku PostgreSQL logs using logplex format:

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

this will stream Heroku PostgreSQL log to pgbadger through stdin.

pgBadger can auto detect RDS and cloudwatch PostgreSQL logs using
rds format:

```text
pgbadger -f rds -o rds_out.html rds.log
```

Each CloudSQL Postgresql log is a fairly normal PostgreSQL log, but encapsulated
in JSON format. It is autodetected by pgBadger but in case you need to force
the log format use `jsonlog`:

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

This is the same as with the jsonlog extension, the json format is different
but pgBadger can parse both formats.

pgBadger also supports logs produced by CloudNativePG Postgres operator for Kubernetes:

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

To create a cumulative report over a month use command:

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

this will add a link to the month name into the calendar view in
incremental reports to look at report for month 2019 May.
Use -E or --explode if the reports were built using this option.
