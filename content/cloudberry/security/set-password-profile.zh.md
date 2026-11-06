---
title: "在 Apache Cloudberry 中设置密码策略"
linkTitle: "设置密码策略"
description: "Profile 指密码策略配置，用于控制 Apache Cloudberry 用户的密码安全策略。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/set-password-profile.md"
---

可以将密码策略配置（Profile）绑定到一个或多个用户，以控制数据库用户的密码安全策略。Profile 定义用户管理和密码复用规则。借助 Profile，数据库管理员可以使用 SQL 强制执行某些限制，例如在登录失败后锁定账户，或控制密码复用次数。

> [!NOTE] 注意
> - 一般来说，Profile 包含密码策略和用户资源使用限制。Apache Cloudberry 中的 Profile 仅支持密码策略。本文所说的“Profile”是指密码策略配置。
> - 只有超级用户才能创建或修改 Profile 策略，且任何 Profile 策略都不限制超级用户。只有允许普通用户使用 Profile 时，Profile 策略才会生效。

Profile 功能默认启用。可以在 `postgresql.conf` 文件中设置 `enable_password_profile` 参数，以禁用或启用 Profile。`enable_password_profile` 的默认值为 `true`。

要禁用 Profile 及相关的登录监控进程，可以将 `enable_password_profile` 设为 `false`，然后重启集群：

```shell
gpconfig -c enable_password_profile -v false
gpstop -ra

# To re-enable Profile, execute _gpconfig -c enable_password_profile -v true_ and restart the cluster.
```

## 实现原理 {#implementation-principle}

与 Autovacuum 机制类似，Profile 引入了 Login Monitor Launcher 和 Login Monitor Worker 进程。当用户登录验证失败时，Apache Cloudberry 会向 postmaster 发送信号。postmaster 收到信号后，会向 launcher 进程发送信号。launcher 进程收到信号后，会通知 postmaster 启动 worker 进程执行元数据回写操作，完成后再通知用户进程和 launcher 进程。

## 使用 SQL 设置密码策略 {#set-password-policies-using-sql}

数据库管理员可以使用 SQL 设置 Profile。以下参数最常用。

| **参数**         | **说明**                                                                                                                                                             |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FAILED_LOGIN_ATTEMPTS | • 用户账户被锁定前允许的最大登录失败次数。<br />• 有效值包括 `-2`（无限制）、`-1`（默认值）以及 `1` 到 `9999`。`0` 是无效值。 |
| PASSWORD_LOCK_TIME    | • 多次连续登录失败后的锁定时间（小时）。<br />• 有效值为 `-2` 到 `9999`。`0` 是有效值。                                       |
| PASSWORD_REUSE_MAX    | • 历史密码复用次数。<br />• 有效值为 `-2` 到 `9999`。`0` 是有效值。                                                                         |

### CREATE PROFILE {#create-profile}

创建 Profile 并设置其密码策略。

```sql
CREATE PROFILE profile LIMIT
  password_parameters ... ;

password_parameters:
{ { FAILED_LOGIN_ATTEMPTS
  | PASSWORD_REUSE_MAX
  | PASSWORD_LOCK_TIME
  }
  expr
}
```

### ALTER PROFILE {#alter-profile}

修改密码策略。

```sql
ALTER PROFILE profile LIMIT
   password_parameters ... ;
```

### DROP PROFILE {#drop-profile}

删除 Profile。

```sql
DROP PROFILE profile;
```

### CREATE USER ... PROFILE {#create-user--profile}

创建用户并设置其 Profile。

```sql
CREATE USER user PROFILE profile;
```

### ALTER USER ... PROFILE {#alter-user--profile}

修改 `user` 的 Profile。

```sql
ALTER USER user PROFILE profile;
```

### CREATE USER ... ENABLE/DISABLE PROFILE {#create-user--enabledisable-profile}

创建用户并指定其使用 Profile 的权限。`ENABLE PROFILE` 授予该权限，`DISABLE PROFILE` 拒绝该权限。默认情况下，新创建的用户无权使用 Profile。

```sql
CREATE USER user
  { ENABLE | DISABLE }
  PROFILE;
```

### ALTER USER ... ENABLE/DISABLE PROFILE {#alter-user--enabledisable-profile}

设置是否允许用户使用 Profile。

```sql
ALTER USER user
  { ENABLE | DISABLE }
  PROFILE;
```

### CREATE USER ... ACCOUNT LOCK/UNLOCK {#create-user--account-lockunlock}

创建用户并设置用户是否锁定。`ACCOUNT LOCK` 表示用户已锁定，无法登录。`ACCOUNT UNLOCK` 表示用户未锁定，可以登录。新创建的用户默认未锁定。

```sql
CREATE USER user ACCOUNT
  { LOCK | UNLOCK };
```

### ALTER USER ... ACCOUNT LOCK/UNLOCK {#alter-user--account-lockunlock}

设置是否锁定用户账户。

```sql
ALTER USER user ACCOUNT
  { LOCK | UNLOCK };
```

## 检查系统表中的密码策略信息 {#check-password-policy-information-in-system-tables}

应用密码配置策略后，Apache Cloudberry 会更新元数据：新增两个系统表 `pg_profile` 和 `pg_password_history`，并在系统表/视图 `pg_authid` 和 `pg_roles` 中新增一些字段。例如：

- **pg_catalog.pg_roles**：在 `pg_roles` 中新增 `rolprofile`、`rolaccountstatus` 和 `rolfailedlogins` 字段，分别记录使用 Profile 的数据库用户、账户状态和登录失败次数。

    ```sql
    View "pg_catalog.pg_roles"
        Column       |           Type           | Collation | Nullable | Default | Storage  | Description
    -------------------+--------------------------+-----------+----------+---------+----------+-------------
    rolname           | name                     |           |          |         | plain    |
    rolsuper          | boolean                  |           |          |         | plain    |
    rolinherit        | boolean                  |           |          |         | plain    |
    rolcreaterole     | boolean                  |           |          |         | plain    |
    rolcreatedb       | boolean                  |           |          |         | plain    |
    rolcanlogin       | boolean                  |           |          |         | plain    |
    rolreplication    | boolean                  |           |          |         | plain    |
    rolconnlimit      | integer                  |           |          |         | plain    |
    rolprofile        | name                     |           |          |         | plain    |
    rolaccountstatus  | smallint                 |           |          |         | plain    |
    rolfailedlogins   | integer                  |           |          |         | plain    |
    rolpassword       | text                     |           |          |         | extended |
    rolvaliduntil     | timestamp with time zone |           |          |         | plain    |
    rolbypassrls      | boolean                  |           |          |         | plain    |
    rolconfig         | text[]                   | C         |          |         | extended |
    rolresqueue       | oid                      |           |          |         | plain    |
    oid               | oid                      |           |          |         | plain    |
    rolcreaterextgpfd | boolean                  |           |          |         | plain    |
    rolcreaterexthttp | boolean                  |           |          |         | plain    |
    rolcreatewextgpfd | boolean                  |           |          |         | plain    |
    rolresgroup       | oid                      |           |          |         | plain    |
    ```

- **pg_catalog.pg_authid**：在 `pg_authid` 中新增 `rolprofile`、`rolaccountstatus`、`rolfailedlogins`、`rolpasswordsetat`、`rollockdata` 和 `rolpasswordexpire` 字段，分别记录使用 Profile 的数据库用户、账户状态、登录失败次数、密码设置时间、账户锁定时间和密码过期时间。

    ```sql
    Table "pg_catalog.pg_authid"
        Column       |           Type           | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
    -------------------+--------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
    oid               | oid                      |           | not null |         | plain    |             |              |
    rolname           | name                     |           | not null |         | plain    |             |              |
    rolsuper          | boolean                  |           | not null |         | plain    |             |              |
    rolinherit        | boolean                  |           | not null |         | plain    |             |              |
    rolcreaterole     | boolean                  |           | not null |         | plain    |             |              |
    rolcreatedb       | boolean                  |           | not null |         | plain    |             |              |
    rolcanlogin       | boolean                  |           | not null |         | plain    |             |              |
    rolreplication    | boolean                  |           | not null |         | plain    |             |              |
    rolbypassrls      | boolean                  |           | not null |         | plain    |             |              |
    rolconnlimit      | integer                  |           | not null |         | plain    |             |              |
    rolenableprofile  | boolean                  |           | not null |         | plain    |             |              |
    rolpassword       | text                     | C         |          |         | extended |             |              |
    rolvaliduntil     | timestamp with time zone |           |          |         | plain    |             |              |
    rolprofile        | oid                      |           | not null |         | plain    |             |              |
    rolaccountstatus  | smallint                 |           | not null |         | plain    |             |              |
    rolfailedlogins   | integer                  |           | not null |         | plain    |             |              |
    rolpasswordsetat  | timestamp with time zone |           |          |         | plain    |             |              |
    rollockdate       | timestamp with time zone |           |          |         | plain    |             |              |
    rolpasswordexpire | timestamp with time zone |           |          |         | plain    |             |              |
    rolresqueue       | oid                      |           |          |         | plain    |             |              |
    rolcreaterextgpfd | boolean                  |           |          |         | plain    |             |              |
    rolcreaterexthttp | boolean                  |           |          |         | plain    |             |              |
    rolcreatewextgpfd | boolean                  |           |          |         | plain    |             |              |
    rolresgroup       | oid                      |           |          |         | plain    |             |              |
    Indexes:
        "pg_authid_oid_index" PRIMARY KEY, btree (oid), tablespace "pg_global"
        "pg_authid_rolname_index" UNIQUE CONSTRAINT, btree (rolname), tablespace "pg_global"
        "pg_authid_rolprofile_index" btree (rolprofile), tablespace "pg_global"
        "pg_authid_rolresgroup_index" btree (rolresgroup), tablespace "pg_global"
        "pg_authid_rolresqueue_index" btree (rolresqueue), tablespace "pg_global"
    Tablespace: "pg_global"
    Access method: heap
    ```

- **pg_catalog.pg_profile**

    新增的 `pg_profile` 系统表如下：

    ```sql
    Table "pg_catalog.pg_profile"
            Column          |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description
    -------------------------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
    oid                     | oid     |           | not null |         | plain   |             |              |
    prfname                 | name    |           | not null |         | plain   |             |              |
    prffailedloginattempts  | integer |           | not null |         | plain   |             |              |
    prfpasswordlocktime     | integer |           | not null |         | plain   |             |              |
    prfpasswordlifetime     | integer |           | not null |         | plain   |             |              |
    prfpasswordgracetime    | integer |           | not null |         | plain   |             |              |
    prfpasswordreusetime    | integer |           | not null |         | plain   |             |              |
    prfpasswordreusemax     | integer |           | not null |         | plain   |             |              |
    prfpasswordallowhashed  | integer |           | not null |         | plain   |             |              |
    prfpasswordverifyfuncdb | oid     |           |          |         | plain   |             |              |
    prfpasswordverifyfunc   | oid     |           |          |         | plain   |             |              |
    Indexes:
        "profile_name_index" UNIQUE CONSTRAINT, btree (prfname), tablespace "pg_global"
        "profile_oid_index" UNIQUE CONSTRAINT, btree (oid), tablespace "pg_global"
        "profile_password_verify_function_index" btree (prfpasswordverifyfuncdb, prfpasswordverifyfunc), tablespace "pg_global"
    Tablespace: "pg_global"
    Access method: heap
    ```

  > [!NOTE] 注意
  > `pg_profile` 表中的字段说明如下：
  >
  > - `oid`：用于唯一标识每条 Profile 记录。
  > - `prfname`：配置文件名。
  > - `prffailedloginattempts`：账户锁定前允许的登录失败次数。
  > - `prfpasswordlocktime`：密码锁定时间。如果账户因登录失败而被锁定，此字段定义锁定持续时间。
  > - `prfpasswordreusemax`：重新使用旧密码前必须设置的新密码数量。
  > - 表中的其他字段无效。

- **pg_catalog.pg_password_history**

    ```sql
    Table "pg_catalog.pg_password_history"
            Column         |           Type           | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
    -----------------------+--------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
    passhistroleid        | oid                      |           | not null |         | plain    |             |              |
    passhistpasswordsetat | timestamp with time zone |           | not null |         | plain    |             |              |
    passhistpassword      | text                     | C         | not null |         | extended |             |              |
    Indexes:
        "pg_password_history_role_password_index" UNIQUE CONSTRAINT, btree (passhistroleid, passhistpassword), tablespace "pg_global"
        "pg_password_history_role_passwordsetat_index" btree (passhistroleid, passhistpasswordsetat), tablespace "pg_global"
    Tablespace: "pg_global"
    Access method: heap
    ```

  > [!NOTE] 注意
  > `pg_password_history` 表中的字段说明如下：
  >
  > - `passhistroleid`：唯一 ID，用于标识与此密码历史记录相关的用户或角色。
  > - `passhistpasswordsetat`：带时区的时间戳字段，记录密码设置或上次修改的准确时间。
  > - `Passhistpassword`：存储历史密码的密文。

## 默认密码策略 {#default-password-policy}

创建用户时，如果未指定具体密码策略，Apache Cloudberry 默认会将默认 Profile 应用于该用户。默认 Profile 是系统初始化期间的默认密码策略。Apache Cloudberry 中的默认 Profile 是 `pg_profile` 表中的 `pg_default` 行。`pg_default` 行定义 Profile 参数的默认值，只有超级用户可以修改这些参数。

如果用户将某个参数设为默认值 `-1`，该参数就会从 `pg_default` 获取值。`pg_default` 的默认值如下。有关如何使用默认 Profile，请参阅[场景 3](#scenario-3-use-default-profile)。

```sql
\x
Expanded display is on.

-- Checks the values of the default Profile in pg_profile
SELECT * FROM pg_profile WHERE prfname = 'pg_default';
-[ RECORD 1 ]-----------+-----------
oid                     | 10140
prfname                 | pg_default
prffailedloginattempts  | -2
prfpasswordlocktime     | -2
prfpasswordlifetime     | -2
prfpasswordgracetime    | -2
prfpasswordreusetime    | -2
prfpasswordreusemax     | -2
prfpasswordallowhashed  | 1
prfpasswordverifyfuncdb |
prfpasswordverifyfunc   |
```

> [!NOTE] 注意
> 任何用户（包括超级用户）都不能重命名或删除 `pg_default` 行。

## 场景示例 {#scenario-examples}

本节介绍 Profile 的典型使用场景。

### 创建密码策略 {#create-a-password-policy}

创建密码策略前，需要先创建 Profile，再将数据库用户绑定到该 Profile。例如：

```sql
-- Creates a profile and a user.
CREATE PROFILE myprofile;
CREATE USER myuser PASSWORD 'mypassword';

-- Binds the profile to the user.
ALTER USER myuser PROFILE myprofile;

-- Checks the relationship between the user and the profile.
SELECT rolname, rolprofile FROM pg_roles WHERE rolname = 'myuser';
 rolname | rolprofile
---------+------------
 myuser  | myprofile
(1 row)
```

### 场景 1：设置最大登录失败次数和密码锁定时间 {#scenario-1-set-the-maximum-number-of-failed-login-attempts-and-password-lock-time}

修改 Profile，将最大登录失败次数设为 3，将密码锁定时间设为 2 小时。

> [!NOTE] 注意
> 多个用户登录失败时，结果返回速度可能会变慢。

```sql
ALTER PROFILE myprofile LIMIT
  FAILED_LOGIN_ATTEMPTS 3
  PASSWORD_LOCK_TIME 2;
  
-- Allows the user myuser to use Profile.
ALTER USER myuser ENABLE PROFILE;


-- Checks the details in the catalog table (the pg_profile is the catalog table that stores all the details related to the user profile).
-- Note that the time shown below is in seconds.

SELECT prfname, prffailedloginattempts, prfpasswordlocktime
FROM pg_profile
WHERE prfname = 'myprofile';
  prfname  | prffailedloginattempts | prfpasswordlocktime
-----------+------------------------+---------------------
 myprofile |                      3 |                   2
(1 row)

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate
---------+------------+-----------------+-----------------+-------------
 myuser  | myprofile  | OPEN            |               0 |
(1 row)
```

当前用户 `myuser` 尚未登录失败。`pg_roles` 系统表显示用户状态为 `OPEN`，系统表 `pg_roles` 中的 `rolfailedlogins` 字段为 `0`。现在，`myuser` 尝试登录失败，然后再次查询 `pg_roles`。

```sql
\c - myuser
Password for user myuser:
FATAL:  password authentication failed for user "myuser"
Previous connection kept

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate
---------+------------+-----------------+-----------------+-------------
 myuser  | myprofile  | OPEN            |               1 |
(1 row)
```

上述结果显示，用户状态仍为 `OPEN`，`rolfailedlogins` 已增加到 `1`。如果账户再次登录失败，`rolfailedlogins` 会继续增加，直到账户被锁定：

```sql
\c - myuser
Password for user myuser:
FATAL:  role "myuser" is locked
Previous connection kept

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
---------+------------+-----------------+-----------------+----------------------------------
 myuser  | myprofile  | LOCKED(TIMED)   |               4 |13-MAR-23 12:25:50.811022 +08:00
(1 row)
```

由于登录失败次数过多，用户账户已锁定。用户状态已变为 `LOCKED(TIMED)`，用户账户将在 2 小时后自动解锁（由 `PASSWORD_LOCK_TIME` 参数控制）。

同时，系统会记录用户账户被锁定的时间戳。锁定期结束后，用户账户状态会变回 `OPEN`，并允许登录。如果用户多次登录失败，但失败次数没有超过 `FAILED_LOGIN_ATTEMPTS` 的限制，用户仍可成功登录，系统会将 `rolfailedlogins` 重置为 `0`。请参阅以下示例：

```sql
\c - myuser
Password for user myuser:
You are now connected to database "postgres" as user "myuser".

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
---------+------------+-----------------+-----------------+----------------------------------
 myuser  | myprofile  | OPEN            |               0 |13-MAR-23 12:25:50.811022 +08:00
(1 row)
```

> [!NOTE] 注意
> 如果手动将 `PASSWORD_LOCK_TIME` 设为 `0`，用户账户将永远不会被锁定。

### 场景 2：设置历史密码复用次数 {#scenario-2-set-the-number-of-historical-password-reuses}

使用 `PASSWORD_REUSE_MAX` 参数，可以防止用户设置最近使用过的密码。如果希望禁止用户使用最近两次的历史密码，可以使用 `ALTER PROFILE` 修改此参数。例如：

```sql
ALTER PROFILE myprofile LIMIT
  PASSWORD_REUSE_MAX 2;
  
-- Checks the Catalog table and finds that the number of permitted historical password reuses is 2.
  SELECT prfname, prfpasswordreusemax
  FROM pg_profile
  WHERE prfname = 'myprofile';
    prfname  | prfpasswordreusemax
-----------+---------------------
 myprofile |                   2
(1 row)
```

```sql
ALTER USER myuser PASSWORD 'mynewpassword';

ALTER USER myuser PASSWORD 'mypassword';
ERROR:  The new password should not be the same with latest 2 history password
```

上述结果显示，由于 `mypassword` 曾经使用过，不能将其复用为新密码。要设置新密码，必须先设置两个不同的中间密码，然后才能复用旧密码。

```sql
ALTER USER myuser PASSWORD 'mypassword2'; -- Second password change
ALTER USER myuser PASSWORD 'mypassword';
```

> [!NOTE] 注意
> 如果 `PASSWORD_REUSE_MAX` 设为 `0`，密码将永远无法更改。如果设为 `-2`（`UNLIMITED`），历史密码只有在设置过 `9999` 个密码后才能再次使用。

### 场景 3：使用 DEFAULT PROFILE {#scenario-3-use-default-profile}

如果创建 Profile 时未显式指定参数值，则 `pg_profile` 表中的参数值默认为 `-1`，这意味着 Apache Cloudberry 会从 `pg_default` 获取该参数的值。

以 `FAILED_LOGIN_ATTEMPTS` 为例：

```sql
--Creates a profile without explicitly specifying any parameter values.
CREATE PROFILE myprf;

-- Checks the default parameter value of myprf in pg_profile.

SELECT * FROM pg_profile WHERE prfname = 'myprf';
-[ RECORD 1 ]-----------+------
oid                     | 16386
prfname                 | myprf
prffailedloginattempts  | -1
prfpasswordlocktime     | -1
prfpasswordlifetime     | -1
prfpasswordgracetime    | -1
prfpasswordreusetime    | -1
prfpasswordreusemax     | -1
prfpasswordallowhashed  | -1
prfpasswordverifyfuncdb |
prfpasswordverifyfunc   |
```

上述示例创建了名为 `myprf` 的 Profile。由于未显式设置任何参数值，所有参数值默认都是 `-1`，这意味着绑定到此 Profile 的任何用户都会使用 `pg_default` 中的参数值。

以下示例将 `pg_defau``lt` 的 `FAILED_LOGIN_ATTEMPTS` 参数设为 `1`，并创建一个测试。

```sql
-- Sets the default value of FAILED_LOGIN_ATTEMPTS in pg_default to 1.
-- All users who do not specify a profile will have their accounts locked after a failed login.

ALTER PROFILE pg_default LIMIT FAILED_LOGIN_ATTEMPTS 1;
\x
Expanded display is on.

-- Checks the default value of pg_default in pg_profile.
SELECT * FROM pg_profile WHERE prfname = 'pg_default';
-[ RECORD 1 ]-----------+-----------
oid                     | 10140
prfname                 | pg_default
prffailedloginattempts  | 1
prfpasswordlocktime     | -2
prfpasswordlifetime     | -2
prfpasswordgracetime    | -2
prfpasswordreusetime    | -2
prfpasswordreusemax     | -2
prfpasswordallowhashed  | 1
prfpasswordverifyfuncdb |
prfpasswordverifyfunc   |

CREATE USER mynewuser PASSWORD 'mynewpassword' ENABLE PROFILE;

SELECT rolname, rolprofile, get_role_status('mynewuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'mynewuser';
  rolname  | rolprofile | get_role_status | rolfailedlogins | rollockdate
-----------+------------+-----------------+-----------------+-------------
 mynewuser | pg_default | OPEN            |               0 |
(1 row)
```

根据上述结果可以看到，用户的 Profile 为 `pg_default`，用户账户状态为 `OPEN`。接下来，尝试使用错误密码登录该账户。

```sql
\c - mynewuser
Password for user mynewuser:
FATAL:  password authentication failed for user "mynewuser"
Previous connection kept

SELECT rolname, rolprofile, get_role_status('mynewuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'mynewuser';
  rolname  | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
-----------+------------+---------------------+-----------------+----------------------------------
 mynewuser | pg_default | LOCKED(TIMED)   |               1 | 12-MAR-23 09:36:42.132231 +08:00
(1 row)
```

由于 `pg_default` 的 `FAILED_LOGIN_ATTEMPTS` 为 `1`，账户在登录失败一次后就会被锁定。

接下来，将用户的 Profile 设为 `myprf`，然后测试相同的操作以观察结果。测试前需要先解锁用户。

```sql
ALTER USER mynewuser ACCOUNT unlock PROFILE myprf;

SELECT rolname, rolprofile, get_role_status('mynewuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'mynewuser';
  rolname  | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
-----------+------------+---------------------+-----------------+----------------------------------
 mynewuser | myprf      | OPEN            |               0 | 12-MAR-23 09:36:42.132231 +08:00
(1 row)
```

结果显示，用户状态变回 `OPEN`，Profile 变为 `myprf`。`rollockdate` 仍然存在，符合预期。接下来，再次使用错误密码登录并观察返回结果。

```sql
\c - mynewuser
Password for user mynewuser:
FATAL:  password authentication failed for user "mynewuser"
Previous connection kept

SELECT rolname, rolprofile, get_role_status('mynewuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'mynewuser';
  rolname  | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
-----------+------------+---------------------+-----------------+----------------------------------
 mynewuser | myprf      | LOCKED(TIMED)   |               1 | 12-MAR-23 09:38:26.753832 +08:00
(1 row)
```

如预期，用户账户状态再次变为锁定。

### 场景 4：超级用户锁定或解锁用户账户 {#scenario-4-superuser-locks-or-unlocks-user-account}

超级用户可以锁定或解锁用户账户。例如：

```sql
ALTER USER myuser ACCOUNT LOCK;

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
---------+------------+---------------------+-----------------+----------------------------------
 myuser  | myprofile  | LOCKED          |               0 | 13-MAR-23 12:25:50.811022 +08:00
(1 row)

ALTER USER myuser ACCOUNT UNLOCK;

SELECT rolname, rolprofile, get_role_status('myuser'), rolfailedlogins, rollockdate
FROM pg_roles
WHERE rolname = 'myuser';
 rolname | rolprofile | get_role_status | rolfailedlogins |           rollockdate            
---------+------------+---------------------+-----------------+----------------------------------
 myuser  | myprofile  | OPEN            |               0 | 13-MAR-23 13:23:50.83928 +08:00
(1 row)
```

### 场景 5：为普通用户启用 Profile {#scenario-5-enable-profile-for-regular-users}

默认情况下，新创建的普通用户不会绑定 Profile。要使用 Profile，需要显式指定。请参阅以下示例：

```sql
CREATE USER myuser1;

SELECT rolname, rolprofile, get_role_status('myuser1'), rolfailedlogins, rollockdate, rolenableprofile
FROM pg_roles
WHERE rolname like 'myuser1';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate | rolenableprofile
---------+------------+-----------------+-----------------+-------------+------------------
 myuser1 | pg_default | OPEN            |               0 |             | f
(1 row)

CREATE USER myuser2 ENABLE PROFILE;
SELECT rolname, rolprofile, get_role_status('myuser2'), rolfailedlogins, rollockdate, rolenableprofile
FROM pg_roles
WHERE rolname = 'myuser2';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate | rolenableprofile
---------+------------+-----------------+-----------------+-------------+------------------
 myuser2 | pg_default | OPEN            |               0 |             | t
(1 row)

CREATE USER myuser3 DISABLE PROFILE;
SELECT rolname, rolprofile, get_role_status('myuser3'), rolfailedlogins, rollockdate, rolenableprofile
FROM pg_roles
WHERE rolname = 'myuser3';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate | rolenableprofile
---------+------------+-----------------+-----------------+-------------+------------------
 myuser3 | pg_default | OPEN            |               0 |             | f
(1 row)
```

创建用户后，可以通过 SQL 语句 `ALTER USER ENABLE/DISABLE PROFILE` 修改是否使用 Profile。

```sql
ALTER USER myuser1 ENABLE PROFILE;

SELECT rolname, rolprofile, get_role_status('myuser1'), rolfailedlogins, rollockdate, rolenableprofile
FROM pg_roles
WHERE rolname = 'myuser1';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate | rolenableprofile
---------+------------+-----------------+-----------------+-------------+------------------
 myuser1 | pg_default | OPEN            |               0 |             | t
(1 row)

ALTER USER myuser1 DISABLE PROFILE;
SELECT rolname, rolprofile, get_role_status('myuser1'), rolfailedlogins, rollockdate, rolenableprofile
FROM pg_roles
WHERE rolname = 'myuser1';
 rolname | rolprofile | get_role_status | rolfailedlogins | rollockdate | rolenableprofile
---------+------------+-----------------+-----------------+-------------+------------------
 myuser1 | pg_default | OPEN            |               0 |             | f
(1 row)
```
