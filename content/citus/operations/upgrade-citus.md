---
title: Citus upgrade
description: Learn how to upgrade Citus versions on your PostgreSQL cluster, including patch upgrades for minor updates, and major version upgrades.
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/upgrade-citus?view=citus-14
upstream_ref: citus-14; be6cf64ecd13
---

Keeping your Citus extension up to date ensures you have access to the latest features, performance improvements, and bug fixes. This guide covers the process of upgrading Citus versions on your PostgreSQL cluster, including both patch upgrades for minor updates and major version upgrades that might include new capabilities. Understanding the upgrade process helps you maintain a secure and efficient distributed database environment while minimizing downtime and ensuring compatibility with your applications.

## Upgrade Citus versions {#upgrade-citus-versions}

To upgrade the Citus version, first get the new Citus extension. Then, install it in each of your database instances. Citus uses separate packages for each minor version. This approach ensures that running a default package upgrade provides bug fixes but never breaks anything. Let's start by examining patch upgrades, the easiest kind.

### Patch version upgrade {#patch-version-upgrade}

To upgrade a Citus version to its latest patch, run a standard upgrade command for your package manager.

Assume version **14.0** is currently installed on PostgreSQL **17**:

**Ubuntu or Debian**

```bash
sudo apt-get update
sudo apt-get install --only-upgrade postgresql-17-citus-14.0
sudo service postgresql restart
```

**Red Hat Enterprise Linux or CentOS**

```bash
sudo yum update citus140_17
sudo service postgresql-17 restart
```

### Major and minor version upgrades {#major-and-minor-version-upgrades}

Major and minor version upgrades follow the same steps, but be careful: they can make backward-incompatible changes in the Citus API. Review the Citus [changelog](https://github.com/citusdata/citus/blob/master/CHANGELOG.md) before an upgrade and look for any changes that might cause problems for your application.

> [!IMPORTANT]
> Starting from Citus 13.2, important features can be backported to recent supported major versions. For this reason, always upgrade to the most recent minor release of the target major version to avoid missing features. For example, suppose a feature introduced in Citus 20.1 is backported to Citus 18.3 and 19.5, and you want to upgrade to Citus 19 from Citus 18.3. Then, upgrading to 19.4 or earlier would mean losing that feature — upgrade to 19.5 or later instead. Or, if you want to upgrade to Citus 20, then upgrade to 20.1 or later, not 20.0.
> 
> In short, always upgrade to the latest minor release of the target major version, not an earlier minor release.

Each major and minor version of Citus is published as a package with a separate name. Installing a newer package automatically removes the older version.

#### Step 1. Update Citus package {#step-1-update-citus-package}

If you upgrade both Citus and PostgreSQL, always upgrade the Citus extension first, and upgrade the PostgreSQL version second (see [PostgreSQL 17 → 18](#upgrade-postgresql-version-from-17-to-18)).

Here's how to do a Citus upgrade from **13.2 to 14.0** on PostgreSQL **17**:

**Ubuntu or Debian**

```bash
sudo apt-get update
sudo apt-get install postgresql-17-citus-14.0
sudo service postgresql restart
```

**Red Hat**

```bash
# Red Hat Enterprise Linux or CentOS
sudo yum swap citus130_17 citus140_17
sudo service postgresql-17 restart
```

#### Step 2. Apply update in database {#step-2-apply-update-in-database}

After installing the new package and restarting the database, run the extension upgrade script.

```sql
-- you must restart PostgreSQL before running this
ALTER EXTENSION citus UPDATE;

-- you should see the upgraded Citus version
SELECT * FROM citus_version();

-- Run this procedure during one of these upgrade paths:
--   * upgrading to Citus 11 or later while still on a pre-11 version, OR
--   * upgrading to Citus 14 or later while still on a pre-14 version.
-- Run it on the coordinator node.
CALL citus_finish_citus_upgrade();
```

> [!NOTE]
> - If you upgrade to Citus 14.x from an earlier major version, `citus_finish_citus_upgrade()` also fixes any colocation groups where the registered collation columns don't match the distribution columns of the tables in the group. This is a metadata-only operation (no data movement) that updates `pg_dist_colocation` and `pg_dist_partition` on all nodes if needed.

During a major version upgrade, from the moment of yum installing a new version, Citus doesn't run distributed queries until the server is restarted and `ALTER EXTENSION` is executed. This stipulation protects your data, as Citus object and function definitions are specific to a version. After a yum install, you should (a) restart and (b) run alter extension. In rare cases if you experience an error with upgrades, you can disable this check via the [`citus.enable_version_checks`](/citus/reference/api-guc/#citusenable_version_checks-boolean) configuration parameter. You can also [contact us](https://www.citusdata.com/about/contact_us) providing information about the error, so we can help debug the issue.

## Upgrade PostgreSQL version from 17 to 18 {#upgrade-postgresql-version-from-17-to-18}

Before you start, record the following paths. Your actual paths might be different from the paths listed here:

Existing data directory (for example, `/opt/pgsql/17/data`) `export OLD_PG_DATA=/opt/pgsql/17/data`

Existing PostgreSQL installation path (for example, `/usr/pgsql-17`) `export OLD_PG_PATH=/usr/pgsql-17`

New data directory after upgrade `export NEW_PG_DATA=/opt/pgsql/18/data`

New PostgreSQL installation path `export NEW_PG_PATH=/usr/pgsql-18`

Then follow the same steps as other PG upgrades (prepare metadata, configure new instance with Citus in shared_preload_libraries, stop old server, run pg_upgrade, copy `postgresql.auto.conf`, `server.crt`, `server.key` if generated by Citus, start new server, run `citus_finish_pg_upgrade()`).

> [!NOTE]
> Don't attempt to upgrade *both* Citus and PostgreSQL versions at once. If you want to upgrade both, upgrade Citus first.

### For every node {#for-every-node}

Follow these steps to upgrade the PostgreSQL version with Citus on every node (coordinator and workers):

1. Back up Citus metadata.

   ```sql
   -- run this on the coordinator and worker nodes
   
   SELECT citus_prepare_pg_upgrade();
   ```
2. Configure the new database instance to use Citus.

   - Include Citus as a shared preload library in `postgresql.conf`.

     ```ini
     shared_preload_libraries = 'citus'
     ```
   - **DO NOT CREATE** a Citus extension.
   - **DO NOT** start the new server yet.
3. Stop the old server.
4. Check upgrade compatibility.

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
                               -d $OLD_PG_DATA -D $NEW_PG_DATA --check
   ```

   You should see a "Clusters are compatible" message. If you don't, fix any errors before proceeding. Ensure that:

   - `NEW_PG_DATA` contains an empty database initialized by new PostgreSQL version
   - The Citus extension **IS NOT** created
5. Perform the upgrade (like before but without the `--check` option).

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
   -d $OLD_PG_DATA -D $NEW_PG_DATA
   ```
6. If you didn't set up the Transport Layer Security (TLS) configuration yourself, Citus does that and you need to copy the Citus-generated `postgresql.auto.conf` file along with the generated certificate files (`server.crt` and `server.key`).

   ```bash
   cp $OLD_PG_DATA/postgresql.auto.conf $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.crt $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.key $NEW_PG_DATA/
   ```
7. Start the new server.
8. **DO NOT** run any query before running the queries given in the next step.
9. Restore metadata on new coordinator node.

   ```sql
   -- run this on the coordinator and worker nodes
   
   SELECT citus_finish_pg_upgrade();
   ```

## Related content {#related-content}

- [Cluster management in Citus](/citus/operations/cluster-management/)
- [Citus table management](/citus/operations/table-management/)
- [Diagnostic queries for Citus](/citus/operations/diagnostic-queries/)
- [What is Citus?](/citus/overview/what-is-citus/)
