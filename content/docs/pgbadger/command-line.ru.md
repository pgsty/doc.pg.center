---
title: "Справочник командной строки"
linkTitle: "Командная строка"
weight: 30
description: "Полный синтаксис команд pgBadger, параметры, удалённый ввод, коды возврата и примеры"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Справочник]
aliases: [/pgbadger/command-line/]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## Использование и параметры {#usage-and-options}

Использование: pgbadger [options] logfile [...]

```text
Анализатор журналов PostgreSQL с подробными отчётами и диаграммами.
```

Аргументы:

```text
logfile — один файл журнала, список файлов или команда оболочки,
возвращающая список файлов. Чтобы читать журнал из stdin, используйте
имя файла -. Ввод из stdin не поддерживается для csvlog.
```

Параметры:

```text
-a | --average minutes : Интервал усреднения графиков запросов и соединений в минутах. По умолчанию 5 минут.
-A | --histo-average min: Интервал построения гистограмм запросов в минутах. По умолчанию 60 минут.
-b | --begin datetime  : Начальная дата/время данных для разбора журнала (отметка времени или время).
-c | --dbclient host   : Включать в отчёт только записи для указанного клиентского узла.
-C | --nocomment       : Удалять из запросов комментарии вида /* ... */.
-d | --dbname database : Включать в отчёт только записи для указанной базы данных.
-D | --dns-resolv      : Заменять IP-адреса клиентов их DNS-именами. Это может значительно замедлить pgBadger.
-e | --end datetime    : Конечная дата/время данных для разбора журнала (отметка времени или время).
-E | --explode         : Создавать отдельный отчёт для каждой базы данных. Общие сведения, не относящиеся к
                         отдельной базе, добавляются в отчёт базы postgres.
-f | --format logtype  : Допустимые значения: syslog, syslog2, stderr, jsonlog, csv, pgbouncer, logplex, rds и
                         redshift. Используйте, если pgBadger не определяет формат журнала автоматически.
-G | --nograph         : Отключить диаграммы в HTML-выводе. По умолчанию диаграммы включены.
-h | --help            : Показать эту справку и завершить работу.
-H | --html-outdir path: Каталог для HTML-отчётов в инкрементальном режиме. Двоичные файлы остаются в каталоге,
                         заданном -O, --outdir.
-i | --ident name      : Имя программы для идентификатора syslog. По умолчанию postgres.
-I | --incremental     : Использовать инкрементальный режим: отчёты по дням создаются в отдельных каталогах.
                         Требуется --outdir.
-j | --jobs number     : Число одновременных заданий для одного файла журнала. По умолчанию и для csvlog
                         используется одно задание.
-J | --Jobs number     : Число параллельно разбираемых файлов журнала. По умолчанию обрабатывается один файл за
                         раз.
-l | --last-parsed file: Вести запись последних разобранных даты/времени и строки для инкрементального разбора.
                         Полезно для отслеживания ошибок после предыдущего запуска или ежедневных отчётов из
                         журнала с еженедельной ротацией.
-L | --logfile-list file: Файл со списком файлов журналов для разбора.
-m | --maxlength size  : Максимальная длина запроса: запрос усекается до заданного размера. По умолчанию 100000.
-M | --no-multiline    : Не собирать многострочные операторы, чтобы избежать посторонних данных, особенно при
                         ошибках, создающих огромный отчёт.
-N | --appname name    : Включать в отчёт только записи для указанного имени приложения.
-o | --outfile filename: Имя выходного файла. По умолчанию: out.html, out.txt, out.bin или out.json в
                         зависимости от формата. Повторное указание позволяет вывести несколько форматов. Для
                         JSON нужен JSON::XS. Для вывода в stdout используйте имя -.
-O | --outdir path     : Каталог для сохранения выходных файлов.
-p | --prefix string   : Значение собственного log_line_prefix из postgresql.conf. Указывайте только при
                         использовании нестандартного префикса, например с дополнительными полями IP клиента или
                         имени приложения. Обязательны заполнители времени (%t, %m или %n) и процесса (%p или
                         %c). См. примеры ниже.
-P | --no-prettify     : Отключить форматирование SQL-запросов.
-q | --quiet           : Ничего не печатать в stdout, включая индикатор выполнения.
-Q | --query-numbering : Нумеровать запросы в выводе --dump-all-queries или --normalized-only.
-r | --remote-host ip  : Узел для выполнения cat над удалённым журналом. Сам файл разбирается локально.
-R | --retention N     : Число недель хранения в инкрементальном режиме. По умолчанию 0 (отключено). Каталоги
                         более старых недель и дней автоматически удаляются из каталога вывода.
-s | --sample number   : Число сохраняемых примеров запросов. По умолчанию 3.
-S | --select-only     : Включать в отчёт только запросы SELECT.
-t | --top number      : Число сохраняемых и отображаемых запросов. По умолчанию 20.
-T | --title string    : Изменить заголовок страницы HTML-отчёта.
-u | --dbuser username : Включать в отчёт только записи для указанного пользователя.
-U | --exclude-user username : Исключать из отчёта записи для указанного пользователя. Можно указывать несколько
                         раз.
-v | --verbose         : Включить подробный или отладочный режим. По умолчанию отключён.
-V | --version         : Показать версию pgBadger и завершить работу.
-w | --watch-mode      : Включать в отчёт только ошибки, подобно logwatch.
-W | --wide-char       : Кодировать HTML-вывод запросов в UTF8, чтобы избежать сообщения Perl
                         «Wide character in print».
-x | --extension       : Формат вывода: text, html, bin или json. По умолчанию html.
-X | --extra-files     : В инкрементальном режиме записывать CSS и JS в каталог вывода отдельными файлами.
-z | --zcat exec_path  : Полный путь к программе zcat. Используйте, если zcat, bzcat или unzip отсутствуют в
                         PATH.
-Z | --timezone +/-XX  : Смещение часового пояса от GMT в часах для корректировки даты/времени диаграмм
                         JavaScript. Значение может быть целым, например 2, или дробным, например 2.5.
--anonymize            : Скрывать все литералы в запросах для защиты конфиденциальных данных.
--charset              : Набор символов HTML. По умолчанию utf-8.
--command CMD          : Команда для получения записей журнала через stdin. pgBadger открывает канал к команде и
                         разбирает созданные ею записи.
--csv-separator        : Разделитель полей CSV. По умолчанию ,.
--day-report YYYY-MM-DD: Создать HTML-отчёт за указанный день. Требуются каталоги инкрементального вывода и все
                         необходимые двоичные файлы данных.
--disable-autovacuum   : Не создавать отчёт autovacuum.
--disable-checkpoint   : Не создавать отчёт о контрольных точках и точках перезапуска.
--disable-connection   : Не создавать отчёт о соединениях.
--disable-error        : Не создавать отчёт об ошибках.
--disable-hourly       : Не создавать почасовой отчёт.
--disable-lock         : Не создавать отчёт о блокировках.
--disable-query        : Не создавать отчёты о запросах (самые медленные, самые частые, по пользователям, по
                         базам данных и т. д.).
--disable-session      : Не создавать отчёт о сеансах.
--disable-temporary    : Не создавать отчёт о временных файлах.
--disable-type         : Не создавать отчёты о запросах по типу, базе данных или пользователю.
--dump-all-queries     : Вывести все запросы из журнала, подставляя значения параметров привязки на места
                         соответствующих заполнителей.
--dump-raw-csv         : Разобрать журнал и вывести сведения в CSV. Дальнейшая обработка не выполняется, отчёт
                         не создаётся.
--enable-checksum      : Добавлять контрольную сумму md5 под каждым отчётом о запросе.
--exclude-appname name : Исключать записи указанного приложения. Пример: "pg_dump". Можно указывать несколько
                         раз.
--exclude-client name  : Исключать записи указанного IP клиента. Можно указывать несколько раз.
--exclude-db name      : Исключать записи указанной базы данных. Пример: "postgres". Можно указывать несколько
                         раз.
--exclude-file filename: Путь к файлу регулярных выражений для исключения запросов из отчёта. По одному
                         выражению на строку.
--exclude-line regex   : Исключать записи журнала, совпадающие с регулярным выражением. Можно указывать
                         несколько раз.
--exclude-query regex  : Исключать запросы, совпадающие с регулярным выражением. Пример: "^(VACUUM|COMMIT)".
                         Можно указывать несколько раз.
--exclude-time  regex  : Исключать отметки времени, совпадающие с регулярным выражением. Пример: "2013-04-12 .*".
                         Можно указывать несколько раз.
--explain-url URL      : Переопределить URL графического инструмента explain. По умолчанию
                         https://explain.depesz.com/.
--histogram-query VAL  : Задать границы гистограммы длительности запросов. По умолчанию в миллисекундах:
                     0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: Задать границы гистограммы длительности сеансов. По умолчанию в миллисекундах:
                     0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: Путь к файлу регулярных выражений для включения запросов в отчёт. По одному выражению
                         на строку.
--include-query regex  : Исключать запросы, не совпадающие с регулярным выражением. Можно указывать несколько
                         раз. Пример: "(tbl1|tbl2)".
--include-pid PID      : Включать в отчёт только события, связанные с PID сеанса (%p). Можно указывать несколько
                         раз.
--include-session ID   : Включать в отчёт только события, связанные с идентификатором сеанса (%c). Можно
                         указывать несколько раз.
--include-time  regex  : Включать только отметки времени, совпадающие с регулярным выражением. Пример:
                         "2013-04-12 .*". Можно указывать несколько раз.
--iso-week-number      : В инкрементальном режиме начинать недели с понедельника и использовать номера недель
                         ISO 8601 от 01 до 53. Неделя 1 — первая неделя, содержащая не менее 4 дней нового года.
--keep-comments        : Не удалять комментарии из нормализованных запросов. Полезно для различения запросов с
                         одинаковым результатом нормализации.
--journalctl command   : Команда journalctl, используемая вместо файла журнала PostgreSQL. Пример:
                            journalctl -u postgresql-9.5
--log-duration         : Принудительно сопоставлять записи журнала, создаваемые одновременно log_duration = on и
                         log_statement = 'all'.
--log-timezone +/-XX   : Смещение от GMT в часах для корректировки даты/времени журнала перед разбором.
                         Усложняет поиск в журнале по дате/времени. Значение может быть целым, например 2, или
                         дробным, например 2.5.
--month-report YYYY-MM : Создать накопительный HTML-отчёт за указанный месяц. Требуются каталоги
                         инкрементального вывода и все необходимые двоичные файлы данных.
--noexplain            : Не обрабатывать строки, созданные auto_explain.
--no-fork              : Не создавать дочерние процессы; используется для отладки.
--no-process-info      : Отключить изменение заголовка процесса для идентификации pgbadger: некоторые системы
                         его не поддерживают.
--no-progressbar       : Отключить индикатор выполнения.
--noreport             : Не создавать отчёты в инкрементальном режиме.
--no-week              : Не создавать еженедельные отчёты в инкрементальном режиме. Полезно, если создание
                         занимает слишком много времени.
--normalized-only      : Вывести только все нормализованные запросы в out.txt.
--pgbouncer-only       : Показывать в заголовке только меню, относящиеся к PgBouncer.
--pid-dir path         : Каталог для файла PID. По умолчанию /tmp.
--pid-file file        : Имя файла PID для управления одновременными запусками pgBadger. По умолчанию
                         pgbadger.pid.
--pie-limit num        : Объединять данные круговой диаграммы со значением ниже num%.
--prettify-json        : Форматировать вывод JSON для удобства чтения.
--rebuild              : Пересобрать все HTML-отчёты в каталогах инкрементального вывода, где сохранились
                         двоичные файлы данных.
--start-monday         : По умолчанию недели в инкрементальном режиме начинаются с воскресенья. Этот параметр
                         меняет начало недели на понедельник.
--tempdir DIR          : Каталог для временных файлов. По умолчанию File::Spec->tmpdir() || '/tmp'.
```

pgBadger может разбирать удалённый файл журнала через SSH-соединение без пароля.
Укажите IP-адрес или имя узла с помощью -r либо --remote-host. Для полного
управления SSH-соединением предусмотрены дополнительные параметры.

```text
--ssh-identity file      Путь к файлу ключа аутентификации.
--ssh-option  options    Список параметров -o для SSH-соединения.
                         Всегда используются:
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          Порт SSH для соединения. По умолчанию 22.
--ssh-program ssh        Путь к программе SSH. По умолчанию ssh.
--ssh-timeout second     Тайм-аут установления SSH-соединения. По умолчанию 10 секунд.
--ssh-user username      Имя пользователя для входа. По умолчанию текущий пользователь.
```

Параметр `--ssh-sudo` добавляет `sudo` перед удалёнными командами перечисления и чтения файлов журнала. Пользователь SSH на удалённом узле должен иметь возможность выполнять эти команды через `sudo` без интерактивного запроса.

Файл журнала для разбора также можно указать с помощью URI. Поддерживаются
протоколы http[s] и [s]ftp. Для загрузки файла используется команда curl, а разбор
выполняется во время загрузки. Также поддерживается протокол ssh: он использует
команду ssh так же, как удалённый узел. См. примеры ниже.

Коды возврата:

```text
0: успешное завершение
1: завершение с ошибкой
2: прерывание, например по Ctrl+C
3: файл PID уже существует или не может быть создан
4: в командной строке не указан файл журнала
```

Примеры:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# Префикс строки журнала при выводе в stderr
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# Префикс строки журнала при выводе в syslog
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# Ускорить разбор файла 10GB с помощью 8 CPU
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

Для удалённого файла журнала используйте запись URI:

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

Можно одновременно разбирать локальный журнал PostgreSQL и удалённый файл журнала pgbouncer:

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

Еженедельный отчёт об ошибках с помощью задания cron:

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

Создание отчёта каждую неделю в инкрементальном режиме:

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

Предполагается, что файл журнала и HTML-отчёт также ротируются еженедельно.

Ещё лучше использовать автоматически создаваемые инкрементальные отчёты:

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Команда создаст отчёт за каждый день и каждую неделю.

В инкрементальном режиме также можно задать число недель, которые следует
хранить в отчётах:

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Если pg_dump ежедневно работает по полчаса в 23:00 и 13:00, можно следующим
образом исключить эти периоды из отчёта pgBadger:

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

Это выражение исключает каждый совпавший час целиком, включая время вне получасового дампа. Уточните шаблон минут, если требуется исключить только интервал выполнения дампа.

Так операторы COPY, создаваемые pg_dump, не окажутся в верхней части списка
самых медленных запросов. Эту проблему можно решить проще с помощью
--exclude-appname "pg_dump".

Вывод journalctl также можно разбирать как обычный файл журнала:

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

или вызвать его на удалённом узле:

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

В командной строке не нужно указывать файл журнала, но при наличии других
журналов PostgreSQL для разбора их можно добавить обычным способом.

Чтобы впоследствии пересобрать все инкрементальные HTML-отчёты, выполните:

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

При этом обновятся и все файлы ресурсов (JS и CSS). Укажите -E или --explode,
если отчёты изначально создавались с этим параметром.

pgBadger также поддерживает журналы Heroku PostgreSQL в формате logplex:

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

Журнал Heroku PostgreSQL будет передаваться в pgbadger через стандартный ввод.

pgBadger может автоматически определять журналы RDS и CloudWatch PostgreSQL
в формате rds:

```text
pgbadger -f rds -o rds_out.html rds.log
```

Каждый журнал Cloud SQL PostgreSQL представляет собой довольно обычный журнал
PostgreSQL, заключённый в формат JSON. pgBadger определяет его автоматически,
но при необходимости принудительно задайте формат `jsonlog`:

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

То же относится и к расширению jsonlog: формат JSON отличается, но pgBadger
умеет разбирать оба варианта.

pgBadger также поддерживает журналы, создаваемые оператором CloudNativePG Postgres для Kubernetes:

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

Чтобы создать накопительный отчёт за месяц, используйте команду:

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

Она добавит в календарное представление инкрементальных отчётов ссылку
с названием месяца для просмотра отчёта за май 2019 года.
Укажите -E или --explode, если отчёты создавались с этим параметром.
