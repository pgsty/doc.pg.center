---
title: plpgsqlcheck
linkTitle: plpgsql_check
description: 'IvorySQL v5.6 documentation: plpgsqlcheck.'
type: docs
weight: 410
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.6.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

During PostgreSQL database development, when writing stored procedures and functions, it is often difficult to discover potential issues such as syntax errors, type mismatches, undefined variables, etc., before runtime. Traditional approaches require waiting until the function is actually executed to discover these errors, which not only increases debugging costs but may also cause unexpected failures in production environments.

plpgsql_check is a static code analysis tool (Linter) specifically designed for PostgreSQL’s PL/pgSQL language. It can perform deep checks on the source code of stored procedures and functions without actually executing them. This tool can proactively identify various code quality issues including syntax errors, type mismatches, unused variables, performance problems, security vulnerabilities, etc., helping developers ensure code correctness and robustness during the development phase. For more details, see [plpgsql_check official documentation](https://github.com/okbob/plpgsql_check).

## 2. Installation {#installation}

> [!TIP]
>
> The source installation environment is Ubuntu 24.04 (x86_64). IvorySQL 5 or higher version is already installed in the environment, with the installation path at /usr/local/ivorysql/ivorysql-5

### 2.1. Source Installation {#source-installation}

```
# Download the 2.8.3 source package plpgsql_check-2.8.3.tar.gz from https://github.com/okbob/plpgsql_check/releases/tag/v2.8.3
tar xvf plpgsql_check-2.8.3.tar.gz
cd plpgsql_check-2.8.3
# Set pg_config path to PATH environment variable, e.g.:
export PATH=/usr/local/ivorysql/ivorysql-5/bin/:$PATH
make USE_PGXS=1 clean
make USE_PGXS=1 all
sudo make USE_PGXS=1 install
```

## 3. Create Extension and Confirm plpgsql_check Version {#create-extension-and-confirm-plpgsql_check-version}

Connect to the database with psql and execute the following commands:

```
ivorysql=# CREATE EXTENSION plpgsql_check;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'plpgsql_check';
     name      | default_version | installed_version |                      comment
---------------+-----------------+-------------------+---------------------------------------------------
 plpgsql_check | 2.8             | 2.8               | extended check for plpgsql functions
(1 row)
```

## 4. Usage {#usage}

### 4.1. Check Single Function {#check-single-function}

```
-- Create a sample function
CREATE OR REPLACE FUNCTION test_function(p_id integer)
RETURNS text AS $$
DECLARE
    v_name text;
    v_unused integer;  -- Unused variable
BEGIN
    SELECT name INTO v_name FROM users WHERE id = p_id;
    RETURN v_naem;  -- Spelling error
END;
$$ LANGUAGE plpgsql;

-- Use plpgsql_check to check the function
SELECT * FROM plpgsql_check_function('test_function(integer)');
```

Example check result:

```
                    plpgsql_check_function
--------------------------------------------------------------
 error:42601:7:assignment:target variable "v_naem" is undefined
 warning:00000:4:DECLARE:unused variable "v_unused"
(2 rows)
```

For more detailed usage methods and advanced features, please refer to [plpgsql_check official documentation](https://github.com/okbob/plpgsql_check).
