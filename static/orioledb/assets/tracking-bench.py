#!/usr/bin/env python3
"""
tracking-bench.py -- a vehicle-position tracking workload for PostgreSQL.

Three arms:
  oriole-pk   OrioleDB, PRIMARY KEY (object_id, ts), no secondary index
  oriole-idx  OrioleDB, no primary key, all-column covering index
  heap-idx    heap, all-column covering index

The workload:
  COPY streams, each emitting one row per second per tracked object
  partitioned storage: the head partition is rotated out once it exceeds
    --swap-bytes, and sealed partitions older than --keep-seconds are dropped
  a maintenance loop every 30 s (VACUUM, partition rotation, ts constraint)
  a read loop, five lookups per second of a random object's recent history
  block-device IOPS/throughput sampled every second

Layout in --out-dir:
  pg.log
  copy1.log ... copyN.log     one per stream
  maint.log                   output of every maintenance cycle
  reader.log                  reader errors, normally empty
  resources.log               JSON line per second, block-device counters
  summary.json                machine-readable end-of-run summary
"""

import argparse
import json
import os
import random
import shutil
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path


# ---------- DDL ---------------------------------------------------------------

TABLE_COLUMNS = """(
    object_id uuid NOT NULL,
    source text NOT NULL,
    lonlat bytea NOT NULL,
    heading double precision NOT NULL,
    accuracy double precision NOT NULL,
    speed double precision NOT NULL,
    ts timestamp without time zone NOT NULL,
    rcvd_ts timestamp without time zone NOT NULL"""


def create_table_ddl(part: str, arm: str) -> str:
    """CREATE TABLE for one partition, DDL varies by arm."""
    cols = TABLE_COLUMNS
    if arm == "oriole-pk":
        return f"CREATE TABLE public.{part} {cols},\n    PRIMARY KEY (object_id, ts)\n) USING orioledb;"
    if arm == "oriole-idx":
        return f"CREATE TABLE public.{part} {cols}\n) USING orioledb;"
    if arm == "heap-idx":
        return f"CREATE TABLE public.{part} {cols}\n);"
    raise ValueError(f"unknown arm: {arm}")


def create_index_ddl(part: str, arm: str, name: str) -> str:
    """Covering index; only for oriole-idx and heap-idx (skipped for oriole-pk)."""
    if arm == "oriole-pk":
        return ""
    return (
        f"CREATE INDEX {name} ON public.{part}\n"
        "  USING btree (object_id, ts, source, lonlat, heading, accuracy, speed, rcvd_ts);"
    )


# Partition maintenance.  The head size comes from orioledb_relation_size() for
# OrioleDB tables (pg_total_relation_size only sees the stub), and a new head
# reuses the old head's access method.
MAINTENANCE_FUNCTIONS = r"""
CREATE TABLE public.swapped_tables (
    table_name text NOT NULL,
    last_modified_at timestamp without time zone NOT NULL
);
INSERT INTO swapped_tables(table_name, last_modified_at) VALUES ('provider_tpv_stream', now());

CREATE FUNCTION public.add_position_table_ts_constraint(p_table_prefix text)
RETURNS TABLE(trace_key text, trace_val double precision, trace_type text)
LANGUAGE plpgsql AS $$
declare
    t_last_swap_timestamp timestamp;
    t_start_time          timestamptz;
    t_check               text;
    t_head_partition      text;
    t_current_table       text;
    t_check_name          text;
begin
    t_start_time := clock_timestamp();
    t_last_swap_timestamp = (select last_modified_at from swapped_tables where table_name = p_table_prefix for update skip locked);
    if t_last_swap_timestamp is null then
        raise exception 'Cannot acquire lock for set constraint %', p_table_prefix;
    end if;
    return query select 'set_lock'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    t_check_name = 'check_ts';
    t_head_partition := p_table_prefix || '_part_000';

    t_start_time := clock_timestamp();
    t_current_table := (
        select tablename from pg_tables
        where schemaname = 'public'
          and tablename like p_table_prefix || '_part_%'
          and tablename != t_head_partition
          and tablename::regclass::oid not in (
              select conrelid from pg_constraint where conname = t_check_name)
        order by tablename
        limit 1);
    return query select 'get_table_name_for_ts_constraint'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    if t_current_table is not null then
        t_start_time := clock_timestamp();
        execute format('select format(''ts between %%L and %%L'', min(ts), max(ts)) from %I', t_current_table) into t_check;
        return query select 'get_minmax_for_ts_constraint'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;
        if t_check = 'ts between NULL and NULL' then
            t_check = 'ts is NULL';
        end if;
        t_start_time := clock_timestamp();
        execute format('alter table %I add constraint %I check (%s)', t_current_table, t_check_name, t_check);
        return query select 'add_ts_constraint'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;
    end if;
end;
$$;

CREATE FUNCTION public.swap_position_table(p_table_prefix text,
                                              p_keep_seconds bigint DEFAULT (2 * 86400),
                                              p_swap_bytes bigint DEFAULT (((1 * 1024) * 1024) * 1024))
RETURNS TABLE(trace_key text, trace_val double precision, trace_type text)
LANGUAGE plpgsql AS $$
declare
    t_last_swap_timestamp timestamp;
    t_start_time          timestamptz;
    t_tablename           text;
    t_backup_partition    text;
    t_keep_after          timestamp;
    t_swap_timestamp      timestamp;
    t_head_partition      text;
    t_current_tsrange     tsrange;
    t_table_size          bigint;
    t_amname              name;
    t_with                text;
begin
    set enable_seqscan to off;
    t_swap_timestamp = now()::timestamp;
    t_backup_partition = null;
    t_head_partition = p_table_prefix || '_part_000';

    t_start_time := clock_timestamp();
    t_last_swap_timestamp = (select last_modified_at from swapped_tables where table_name = p_table_prefix for update skip locked);
    if t_last_swap_timestamp is null then
        raise exception 'Cannot acquire lock for cleaning %', p_table_prefix;
    end if;
    return query select 'set_lock'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    select a.amname into t_amname
      from pg_class c join pg_am a on a.oid = c.relam
     where c.oid = t_head_partition::regclass;
    if t_amname = 'orioledb' then
        execute 'select orioledb_relation_size($1)' into t_table_size using t_head_partition::regclass::oid;
        t_with = '';
    else
        t_table_size = pg_total_relation_size(t_head_partition);
        t_with = ' with (autovacuum_analyze_threshold = 2000000000)';
    end if;
    return query select 'table_size'::text, cast(t_table_size as double precision), 'bytes'::text;
    if t_table_size <= p_swap_bytes then
        return;
    end if;

    t_start_time := clock_timestamp();
    execute format('drop view if exists %I', p_table_prefix);
    return query select 'drop_view'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    t_start_time := clock_timestamp();
    t_keep_after := t_swap_timestamp - (p_keep_seconds || 'second')::interval;
    for t_tablename in (
        select tablename from pg_tables
        where schemaname = 'public'
          and tablename like p_table_prefix || '_part_%'
          and tablename != t_head_partition
          and upper(obj_description(tablename::regclass::oid)::tsrange) < t_keep_after
        order by tablename
    ) loop
        execute format('drop table %I', t_tablename);
        t_backup_partition = coalesce(t_backup_partition, t_tablename);
    end loop;
    return query select 'drop_partitions'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    if t_backup_partition is null then
        t_start_time := clock_timestamp();
        t_backup_partition = (
            select tname from (
                select p_table_prefix || '_part_' || to_char(generate_series(1,999), 'FM000') tname
            ) c
            where not exists(select from pg_tables where schemaname='public' and tablename = tname)
            limit 1);
        if t_backup_partition is null then
            raise exception 'exhausted table slots for %', p_table_prefix;
        end if;
        return query select 'find_backup_name'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;
    end if;

    t_current_tsrange := tsrange(t_last_swap_timestamp, t_swap_timestamp);

    t_start_time := clock_timestamp();
    execute format('alter table %I rename to %I', t_head_partition, t_backup_partition);
    execute format('comment on table %I is %L', t_backup_partition, t_current_tsrange);
    return query select 'rename_head_to_backup'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    t_start_time := clock_timestamp();
    execute format('create table %I (like %I including indexes) using %I%s',
                   t_head_partition, t_backup_partition, t_amname, t_with);
    return query select 'create_head_table'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    t_start_time := clock_timestamp();
    execute format(
        'create view %I as (' || (
            select string_agg('select * from ' || tablename, ' union all ')
            from pg_tables
            where schemaname = 'public'
                and tablename like p_table_prefix || '_part_%'
        ) || ')', p_table_prefix);
    return query select 'create_view'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;

    t_start_time := clock_timestamp();
    update swapped_tables set last_modified_at = t_swap_timestamp where table_name = p_table_prefix;
    return query select 'free_lock'::text, extract(epoch from clock_timestamp() - t_start_time)::float8, 'seconds'::text;
end;
$$;
"""


def build_schema(arm: str) -> str:
    """Full schema.sql for the given arm."""
    parts = []
    parts.append(create_table_ddl("provider_tpv_stream_part_000", arm))
    parts.append(create_table_ddl("provider_tpv_stream_part_001", arm))
    idx0 = create_index_ddl("provider_tpv_stream_part_000", arm, "provider_tpv_stream_idx")
    idx1 = create_index_ddl("provider_tpv_stream_part_001", arm, "provider_tpv_stream_prev_idx")
    if idx0:
        parts += [idx0, idx1]
    parts.append(
        "CREATE VIEW public.provider_tpv_stream AS\n"
        "  SELECT * FROM public.provider_tpv_stream_part_000\n"
        "  UNION ALL SELECT * FROM public.provider_tpv_stream_part_001;"
    )
    parts.append(MAINTENANCE_FUNCTIONS)
    return "\n\n".join(parts)


# ---------- Copy stream generator --------------------------------------------

COPY_HEAD = (b"COPY provider_tpv_stream_part_000 "
             b"(object_id, source, lonlat, heading, accuracy, speed, ts, rcvd_ts) "
             b"FROM STDIN WITH CSV;\n")


def copy_stream(out_path: Path, port: int, socket_dir: str, dbname: str,
                objects: int, offset_seed: int) -> None:
    """One COPY stream. Writes psql output to out_path, feeds CSV to psql via stdin."""
    random.seed(offset_seed)
    providers = [{
        "object_id": uuid.UUID(int=random.getrandbits(128)),
        "ts_offset": random.random(),
    } for _ in range(objects)]
    providers.sort(key=lambda k: k["ts_offset"])

    # One COPY *per second*, delimited by \.
    # A single long-lived COPY holds AccessExclusiveLock-blocking references on
    # the table for its whole duration, which starves ALTER TABLE RENAME inside
    # swap_position_table and defeats partition rotation.
    rows = [(("%s,fake_source,\\x0101000020E610000000000000000000000000000000000000,"
              "45.011,2.2,0.4," % p["object_id"]).encode(),
             ("%.6f" % p["ts_offset"])[1:].encode()) for p in providers]
    psql = subprocess.Popen(
        ["psql", "-X", "-h", socket_dir, "-p", str(port), "-d", dbname],
        stdin=subprocess.PIPE,
        stdout=open(out_path, "wb"),
        stderr=subprocess.STDOUT,
    )
    try:
        while True:
            time.sleep(1)
            ts_root = time.strftime("%Y-%m-%d %H:%M:%S").encode()
            batch = [COPY_HEAD]
            for prefix, frac in rows:
                ts = ts_root + frac
                batch.append(prefix + ts + b"," + ts + b"\n")
            batch.append(b"\\.\n")
            try:
                psql.stdin.write(b"".join(batch))
                psql.stdin.flush()
            except BrokenPipeError:
                return
    finally:
        try:
            psql.stdin.close()
        except Exception:
            pass
        psql.wait(timeout=5)


# ---------- Small helpers -----------------------------------------------------

def psql_run(port: int, socket_dir: str, dbname: str, sql: str,
             capture: bool = False, timeout: int = 30) -> str:
    args = ["psql", "-X", "-q", "-h", socket_dir, "-p", str(port), "-d", dbname,
            "-Atc" if capture else "-c", sql]
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


def bd_stats(dev: str):
    """(read_ios, read_sectors, write_ios, write_sectors) from /sys/block/<dev>/stat,
    or None if the device is not present -- caller must degrade gracefully."""
    path = f"/sys/block/{dev}/stat"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        fields = f.read().split()
    return int(fields[0]), int(fields[2]), int(fields[4]), int(fields[6])


# ---------- Postgres setup ---------------------------------------------------

CONFIG_COMMON = """\
max_connections = 200
wal_buffers = 256MB
max_wal_size = 32GB
min_wal_size = 4GB
checkpoint_timeout = 300s
checkpoint_completion_target = 0.9
fsync = on
synchronous_commit = on
full_page_writes = on
wal_level = replica
huge_pages = try
track_io_timing = on
log_checkpoints = on
jit = off
autovacuum = on
"""

def start_pg(pgbin: Path, pgdata: Path, port: int, socket_dir: str, arm: str,
             log_path: Path, shared_buffers: str, main_buffers: str,
             undo_buffers: str) -> None:
    if pgdata.exists():
        shutil.rmtree(pgdata)
    subprocess.check_call([str(pgbin / "initdb"), "-D", str(pgdata),
                           "-U", os.environ.get("USER", "ubuntu"),
                           "--locale=C", "--encoding=UTF8", "--no-sync"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with (pgdata / "postgresql.conf").open("a") as f:
        f.write("\n# tracking-bench additions\n")
        f.write(CONFIG_COMMON)
        f.write(f"port = {port}\n")
        f.write(f"unix_socket_directories = '{socket_dir}'\n")
        f.write("listen_addresses = ''\n")
        if arm.startswith("oriole"):
            f.write("shared_preload_libraries = 'orioledb.so'\n"
                    "default_table_access_method = 'orioledb'\n"
                    "orioledb.use_sparse_files = on\n"
                    f"shared_buffers = {shared_buffers}\n"
                    f"orioledb.main_buffers = {main_buffers}\n"
                    f"orioledb.undo_buffers = {undo_buffers}\n")
        else:
            # heap: gets shared_buffers + main_buffers combined so both engines
            # see the same total engine cache
            hs = _combine(shared_buffers, main_buffers)
            f.write(f"shared_buffers = {hs}\n")
    subprocess.check_call([str(pgbin / "pg_ctl"), "-D", str(pgdata),
                           "-l", str(log_path), "start", "-w"],
                          stdout=subprocess.DEVNULL)


def _combine(a: str, b: str) -> str:
    """Add two Postgres memory sizes like '1GB' + '7GB' -> '8GB'."""
    def bytes_of(s: str) -> int:
        s = s.strip().upper()
        mult = 1
        if s.endswith("KB"): mult, s = 1024, s[:-2]
        elif s.endswith("MB"): mult, s = 1024**2, s[:-2]
        elif s.endswith("GB"): mult, s = 1024**3, s[:-2]
        elif s.endswith("TB"): mult, s = 1024**4, s[:-2]
        return int(s) * mult
    tot = bytes_of(a) + bytes_of(b)
    if tot % 1024**3 == 0: return f"{tot // 1024**3}GB"
    if tot % 1024**2 == 0: return f"{tot // 1024**2}MB"
    return f"{tot}B"
    subprocess.check_call([str(pgbin / "pg_ctl"), "-D", str(pgdata),
                           "-l", str(log_path), "start", "-w"],
                          stdout=subprocess.DEVNULL)


def stop_pg(pgbin: Path, pgdata: Path, mode: str = "fast") -> None:
    subprocess.run([str(pgbin / "pg_ctl"), "-D", str(pgdata),
                    "stop", "-m", mode, "-w", "-t", "30"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ---------- Main --------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True,
                    choices=["oriole-pk", "oriole-idx", "heap-idx"])
    ap.add_argument("--duration", type=int, default=7200, help="seconds")
    ap.add_argument("--pgbin", required=True, help="postgres bin/ prefix")
    ap.add_argument("--pgdata", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--iops-dev", default="nvme1n1", help="block device name in /sys/block")
    ap.add_argument("--port", type=int, default=5468)
    ap.add_argument("--socket-dir", default="/tmp")
    ap.add_argument("--dbname", default="tracking")
    ap.add_argument("--shared-buffers", default="512MB",
                    help="OrioleDB gets this + main_buffers as its two caches; "
                         "heap gets the sum as plain shared_buffers")
    ap.add_argument("--main-buffers", default="3GB",
                    help="orioledb.main_buffers (ignored for heap arms)")
    ap.add_argument("--undo-buffers", default="512MB",
                    help="orioledb.undo_buffers (ignored for heap arms)")
    ap.add_argument("--streams", type=int, default=5)
    ap.add_argument("--objects", type=int, default=6000, help="per stream")
    ap.add_argument("--keep-seconds", type=int, default=3500,
                    help="swap_position_table retention; sealed partitions older "
                         "than this are dropped")
    ap.add_argument("--swap-bytes", type=int, default=1_000_000_000,
                    help="swap_position_table threshold on the head partition")
    args = ap.parse_args()

    pgbin = Path(args.pgbin) / "bin"
    pgdata = Path(args.pgdata)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Fresh cluster
    print(f"--- start_pg  {time.strftime('%H:%M:%S')}", flush=True)
    start_pg(pgbin, pgdata, args.port, args.socket_dir, args.arm, out_dir / "pg.log",
             args.shared_buffers, args.main_buffers, args.undo_buffers)
    env = os.environ.copy()
    env["PATH"] = f"{pgbin}:{env['PATH']}"
    os.environ["PATH"] = env["PATH"]

    # Database, extension, schema
    psql_run(args.port, args.socket_dir, "postgres", f"CREATE DATABASE {args.dbname}")
    if args.arm.startswith("oriole"):
        psql_run(args.port, args.socket_dir, args.dbname, "CREATE EXTENSION orioledb")
        commit = psql_run(args.port, args.socket_dir, args.dbname,
                          "SELECT orioledb_commit_hash()", capture=True)
        print(f"    orioledb commit {commit}", flush=True)
    schema = build_schema(args.arm)
    (out_dir / "schema.sql").write_text(schema)
    subprocess.check_call(["psql", "-X", "-q", "-h", args.socket_dir,
                           "-p", str(args.port), "-d", args.dbname,
                           "-f", str(out_dir / "schema.sql")])
    indices = psql_run(
        args.port, args.socket_dir, args.dbname,
        "SELECT indexrelid::regclass::text || ' ' || pg_get_indexdef(indexrelid) "
        "FROM pg_index WHERE indrelid='provider_tpv_stream_part_000'::regclass",
        capture=True)
    print(f"    index: {indices or '(none)'}", flush=True)

    # Launch children — we'll clean up in a finally
    children: list = []

    def spawn_copy(i: int):
        p = subprocess.Popen(
            [sys.executable, __file__, "--arm", args.arm, "--pgbin", args.pgbin,
             "--pgdata", args.pgdata, "--out-dir", args.out_dir,
             "--port", str(args.port), "--socket-dir", args.socket_dir,
             "--dbname", args.dbname, "--objects", str(args.objects),
             "--_stream_index", str(i), "--duration", str(args.duration)])
        children.append(p); return p

    # We use two entry points in this same file:
    #   the copy-stream branch is selected by --_stream_index (hidden)
    # kept as one file so the deployment is a single artifact

    try:
        for i in range(args.streams):
            spawn_copy(i)
        # give producers a head start before we snapshot the seen ids
        time.sleep(20)
        psql_run(args.port, args.socket_dir, args.dbname,
                 "DROP TABLE IF EXISTS seen_provider_ids; "
                 "CREATE TABLE seen_provider_ids AS "
                 "(SELECT DISTINCT object_id FROM provider_tpv_stream "
                 " WHERE ts > now() - interval '15 seconds')")
        seen = psql_run(args.port, args.socket_dir, args.dbname,
                        "SELECT count(*) FROM seen_provider_ids", capture=True)
        print(f"    objects seen: {seen}", flush=True)

        # Maintenance loop.  We can't use psql \watch with VACUUM: multi-statement
        # -c is wrapped in a transaction and VACUUM refuses.  Use a plain shell
        # while-loop that opens a fresh connection each cycle (three separate -c
        # invocations = three separate transactions, so VACUUM is fine).
        maint_cmd = (
            f"while true; do "
            f"  psql -X -q -h {args.socket_dir} -p {args.port} -d {args.dbname} "
            f"       -c 'VACUUM provider_tpv_stream_part_000' "
            f"       -c \"SELECT swap_position_table('provider_tpv_stream', {args.keep_seconds}, {args.swap_bytes})\" "
            f"       -c \"SELECT add_position_table_ts_constraint('provider_tpv_stream')\" "
            f"       || true; "
            f"  sleep 30; "
            f"done")
        maint = subprocess.Popen(
            ["bash", "-c", maint_cmd],
            stdout=open(out_dir / "maint.log", "wb"),
            stderr=subprocess.STDOUT)
        children.append(maint)

        # Reader loop: one psql per query, errors ignored.  A
        # single psql with \watch exits on the first error, and every swap
        # briefly drops the view.
        read_sql = (
            "SELECT * FROM provider_tpv_stream "
            "WHERE object_id = (SELECT object_id FROM seen_provider_ids ORDER BY random() LIMIT 1) "
            "AND ts BETWEEN (SELECT now() - (random()*4*3600) * interval '1 second') "
            "AND (SELECT now())")
        read_cmd = (
            f"while true; do "
            f"  psql -X -q -h {args.socket_dir} -p {args.port} -d {args.dbname} "
            f"       -c \"{read_sql}\" > /dev/null; "
            f"  sleep 0.2; "
            f"done")
        reader = subprocess.Popen(
            ["bash", "-c", read_cmd],
            stdout=subprocess.DEVNULL,
            stderr=open(out_dir / "reader.log", "wb"))
        children.append(reader)

        # IOPS/throughput sampler, one JSON line per second
        print(f"--- running {args.duration}s  {time.strftime('%H:%M:%S')}", flush=True)
        deadline = time.time() + args.duration
        with (out_dir / "resources.log").open("w") as f:
            prev = bd_stats(args.iops_dev)
            if prev is None:
                print(f"    warn: /sys/block/{args.iops_dev}/stat not found, "
                      f"resource sampling disabled", flush=True)
                time.sleep(max(0.0, deadline - time.time()))
            else:
                prev_t = time.time()
                while time.time() < deadline:
                    time.sleep(1)
                    cur = bd_stats(args.iops_dev)
                    if cur is None:
                        continue
                    now = time.time()
                    dt = now - prev_t
                    sample = {
                        "t": now,
                        "read_iops":  (cur[0] - prev[0]) / dt,
                        "read_bytes": (cur[1] - prev[1]) * 512 / dt,
                        "write_iops": (cur[2] - prev[2]) / dt,
                        "write_bytes": (cur[3] - prev[3]) * 512 / dt,
                    }
                    f.write(json.dumps(sample) + "\n")
                    f.flush()
                    prev, prev_t = cur, now
    finally:
        print(f"--- tear down  {time.strftime('%H:%M:%S')}", flush=True)
        for p in children:
            try:
                p.terminate()
            except Exception:
                pass
        for p in children:
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()

        # These are best-effort statistics.  A count(*) over a 50 M-row view on
        # the tear-down side of a small VM can take minutes; do not let it or
        # any other single-step failure skip stop_pg below.
        def _safe(fn, default=""):
            try:
                return fn()
            except Exception as e:
                print(f"    warn: {e}", flush=True); return default
        size = _safe(lambda: psql_run(args.port, args.socket_dir, args.dbname,
                        "SELECT pg_size_pretty(pg_database_size(current_database()))",
                        capture=True, timeout=60), "")
        du_actual = _safe(lambda: subprocess.check_output(
            ["du", "-sh", str(pgdata)], timeout=120).decode().split()[0], "")

        # Summarise resources.log
        r_reads, r_writes, r_rbytes, r_wbytes = [], [], [], []
        with (out_dir / "resources.log").open() as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                r_reads.append(d["read_iops"]); r_writes.append(d["write_iops"])
                r_rbytes.append(d["read_bytes"]); r_wbytes.append(d["write_bytes"])
        def stat(seq):
            seq = sorted(seq)
            if not seq: return None
            n = len(seq)
            return {"median": seq[n // 2], "p95": seq[int(n * 0.95)],
                    "max": seq[-1], "mean": sum(seq) / n}

        summary = {
            "arm": args.arm,
            "duration_s": args.duration,
            "logical_size": size,
            "actual_size": du_actual,
            "read_iops": stat(r_reads),
            "write_iops": stat(r_writes),
            "read_bytes": stat(r_rbytes),
            "write_bytes": stat(r_wbytes),
            "read_iops_last15min": stat(r_reads[-900:]),
            "write_iops_last15min": stat(r_writes[-900:]),
        }
        (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
        print(json.dumps(summary, indent=2), flush=True)

        # Best-effort clean shutdown, then hard SIGKILL of any postmaster process
        # group still bound to our pgdata.  Without this, a stuck postmaster keeps
        # port 5468 bound and the next arm's initdb succeeds but pg_ctl fails.
        try:
            stop_pg(pgbin, pgdata)
        except Exception as e:
            print(f"    warn: stop_pg: {e}", flush=True)
        try:
            with open(pgdata / "postmaster.pid") as f:
                pid = int(f.readline().strip())
            os.killpg(os.getpgid(pid), signal.SIGKILL)
            time.sleep(2)
        except Exception:
            pass


# --------------------------------------------------------------------------
# Copy-stream entry point re-uses this file: --_stream_index means "act as
# stream #N of the parent driver", so deployment is a single artifact.
# --------------------------------------------------------------------------
if "--_stream_index" in sys.argv:
    idx = int(sys.argv[sys.argv.index("--_stream_index") + 1])
    # rebuild a minimal argparse view of the args we care about
    def opt(name, default=None, cast=str):
        try:
            return cast(sys.argv[sys.argv.index(name) + 1])
        except ValueError:
            return default
    out_dir = Path(opt("--out-dir"))
    port = int(opt("--port", 5468, int))
    sock = opt("--socket-dir", "/tmp")
    db = opt("--dbname", "tracking")
    objs = int(opt("--objects", 6000, int))
    # This process runs a stream until the parent kills it
    copy_stream(out_dir / f"copy{idx + 1}.log", port, sock, db, objs,
                offset_seed=1000 + idx)
    sys.exit(0)


if __name__ == "__main__":
    main()
