---
title: initdb Process
linkTitle: initdb Process
description: 'IvorySQL v5.6 documentation: initdb Process.'
type: docs
weight: 580
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/6.2.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

IvorySQL supports two database modes during the initialization process:

- PG Mode: Maintains compatibility with native PostgreSQL.

- Oracle Mode (default): Provides Oracle syntax compatibility and enhanced features.

Users can specify the initialization mode using the initdb command parameters to meet compatibility requirements for different scenarios.

## 1. Parameter Parsing and Processing {#parameter-parsing-and-processing}

During the initial phase, initdb parses the input command-line parameters.

|  |  |  |  |
|----|----|----|----|
| Parameter | Description | Options | Default Value |
| -m | Specifies the database mode | oracle/pg | oracle |
| -C | Sets the case conversion mode for Oracle compatibility | interchange/normal/lowercase | interchange |

Parameter Parsing Workflow:

1.Inherits PostgreSQL’s existing parameter processing mechanism.

2.Adds parsing logic for the mode selection parameter -m.

3.Introduces a processing module for the case conversion parameter -C.

## 2. File Path Initialization {#file-path-initialization}

The setup_data_file_paths() function is executed to configure critical file paths:

```
   if (DB_PG == database_mode)
        set_input(&bki_file, "postgres.bki");
    else
        set_input(&bki_file, "postgres_oracle.bki");
```

Path Verification Mechanism:

1.Verifies the existence of the BKI files (postgres_oracle.bki / postgres.bki).

2.Confirms the availability of the configuration file templates.

3.Establishes the system directory structure corresponding to the database mode.

## 3. Data Directory Initialization Process {#data-directory-initialization-process}

The core initialization operations are performed by the initialize_data_directory() function:

### 3.1. Directory Structure Creation {#directory-structure-creation}

Calls create_data_directory() to create the main data directory (PGDATA).

Uses create_xlog_or_symlink() to establish the WAL log directory.

Iteratively creates standard subdirectories such as base and global.

### 3.2. Configuration File Initialization {#configuration-file-initialization}

Calls set_null_conf() to create an empty postgresql.conf file.

In Oracle mode, additionally creates the ivorysql.conf configuration file.

Calls setup_config() to write configuration information to postgresql.conf. In Oracle mode, additional configuration information is written to ivorysql.conf.

### 3.3. Template Database Bootstrapping {#template-database-bootstrapping}

Executes bootstrap_template1() to load the corresponding BKI file and initialize the template1 template database.

IvorySQL additionally sets the database mode (oracle/pg) and case conversion mode for the template1 template database.

load_plisql(): Installs the PL/iSQL procedural language for Oracle PL/SQL compatibility.

load_ivorysql_ora(): Loads the core Oracle compatibility layer extension.

make_ivorysql(): Creates the default ivorysql database.

### 3.4. Oracle-Compatible Username Handling {#oracle-compatible-username-handling}

When the database mode is Oracle, usernames are forcibly converted to lowercase.

Note

In PostgreSQL, "bki" stands for "Bootstrap Kit." The Bootstrap Kit is a collection of tools and files used internally by PostgreSQL to bootstrap the database system.

The Bootstrap Kit is primarily used to initialize the foundational structure of the PostgreSQL database system, including the system catalog, system tables, and other necessary system objects. These system catalogs and tables store metadata information about the PostgreSQL database system, such as database objects, table structures, and index information.

The genbki.pl script processes system table files like pg_class.h, pg_namespace.h, and pg_proc.h, and generates postgres.bki for initdb to load. This primarily involves loading initialization data, such as creating system tables, system functions, and predefined types.

During the compilation phase before initdb, genbki.pl generates both postgres.bki and postgres_ora.bki. While postgres.bki remains unchanged from PostgreSQL, postgres_ora.bki includes additional system objects for Oracle compatibility.

![p20](/ivorysql/assets/images/upstream/562c1ed621af0d24b25b2b86b318db93765f06cfc1553d13f830d46664756b18.jpg)
