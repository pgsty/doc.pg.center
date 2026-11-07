---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16; documentation snapshot 2026-11-07"
upstream_notice: /attribution/#halodb
title: Compatible MySQL data types
linkTitle: MySQL data types
description: MySQL numeric, character, date/time, ENUM, SET, and YEAR types documented for Halo.
weight: 50
---

The Halo 1.0.16 MySQL reference documents common numeric, character, date/time, and special MySQL types. Accepted type names do not make every range, cast, collation, or automatic-value rule identical to a native MySQL server; verify the values that the application depends on.

## Numeric types {#numeric}

The documented integer families include `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, and `BIGINT`. The reference also lists `FLOAT`, `DOUBLE`, `NUMERIC`, and `DECIMAL`, with `SIGNED` and `UNSIGNED` modifiers for supported numeric forms.

```sql
CREATE TABLE int_example (
  id INT,
  id_signed INT SIGNED,
  id_unsigned INT UNSIGNED,
  amount DECIMAL(12, 2) UNSIGNED
);
```

When migrating `UNSIGNED` columns, test overflow, negative values, casts, and application-side validation. PostgreSQL-derived storage can expose different numeric edge behavior.

## Character types {#character}

The documented character families are `CHAR`, `VARCHAR`, `TINYTEXT`, `TEXT`, `MEDIUMTEXT`, and `LONGTEXT`:

```sql
CREATE TABLE profile (
  id INT,
  display_name VARCHAR(200),
  bio TEXT
);

INSERT INTO profile VALUES (1, 'Alice', 'A short bio');
```

Validate character encoding, collation, comparison order, maximum lengths, and client-driver parameter handling with representative data.

## `ENUM` and `SET` {#enum-and-set}

The current reference shows native inline `ENUM` and `SET` definitions. `ENUM` restricts a column to listed members. `SET` stores zero or more members from the declared list.

```sql
CREATE TABLE preference (
  id INT,
  status ENUM('active', 'inactive', 'pending'),
  channels SET('email', 'sms', 'push')
);

INSERT INTO preference VALUES (1, 'active', 'email,push');
```

Test invalid members, empty values, ordering, comparisons, and dump/restore behavior before migrating a schema that relies on MySQL's special type semantics.

## Date and time types {#date-and-time}

The reference covers `DATE`, `DATETIME`, `TIMESTAMP`, and `YEAR`. `DATETIME` and `TIMESTAMP` accept the documented `YYYY-MM-DD HH:MM:SS` form. The current Halo reference states that `TIMESTAMP` does not implicitly add MySQL's automatic update behavior; specify it explicitly when the application needs it:

```sql
CREATE TABLE audit_event (
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  event_year YEAR
);

INSERT INTO audit_event VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2026);
```

`YEAR` accepts four-digit values from `1901` through `2155`. It does not perform MySQL's two-digit year conversion, so use four-digit values and test out-of-range input:

```sql
CREATE TABLE year_example (event_year YEAR);
INSERT INTO year_example VALUES (2026), ('1999');
```

Timezone conversion, default values, and automatic update behavior should be tested with the application's session timezone and driver.

For the complete upstream examples, see [Halo's MySQL data type reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types).

## Sources {#sources}

This page is an original summary of the [Halo Database MySQL compatibility reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types). No public documentation licence was identified; see the [source notice](/attribution/#halodb) for version, copyright, and citation details.
