---
title: 用户管理命令
description: DocumentDB 中支持的 createUser、updateUser、dropUser、usersInfo 以及用户角色成员关系字段。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/security/user-commands.md
weight: 20
translation_source_sha256: 82d3b6712061796c5308655c7e5d563c1ae2cc36690694eb5a9112f8acee4ddc
translation_review: AI-assisted bilingual review; 2026-11-07
---

在 `admin` 上运行用户管理命令。这些命令需要用户 CRUD 支持以及调用者的管理权限。原生密码操作还要求启用原生认证。

<span id="create-user"></span>

## createUser {#createuser}

```javascript
db.getSiblingDB("admin").createUser({
  user: "bookings_operator",
  pwd: passwordPrompt(),
  roles: [{ role: "readAnyDatabase", db: "admin" }]
})
```

| 参数 | 描述 |
| --- | --- |
| **`createUser`** | (必需) 指定非空且非保留用户名的字符串，长度不得超过 PostgreSQL 角色名长度限制。 |
| **`pwd`** | (必需) 指定原生用户非空密码的字符串；服务器可能施加密码约束。 |
| **`roles`** | (必需) 指定包含 `role` 的角色定义文档数组，可选地包含 `db` 或 `$db`；数据库限定符必须为 `"admin"`。 |
| **`customData`** | (可选) 仅识别 `IdentityProvider` 字段的文档。它选择由部署提供的外部身份路径，而非任意用户元数据；外部身份配置不使用原生密码要求。 |
{.fields}

对于原生用户创建，可接受的内置角色集合为 `readAnyDatabase`、`readWriteAnyDatabase`（如可用），或 `readWriteAnyDatabase` 与 `clusterAdmin` 一同指定。或者，指定一个支持的自定义角色。自定义角色不能与内置角色混合使用，且此创建路径不支持多个自定义角色。这不是任意的 MongoDB 角色分配。

`mechanisms`、`digestPassword` 和 `authenticationRestrictions` 不被默认解析器识别。

<span id="update-user"></span>

## updateUser {#updateuser}

```javascript
db.getSiblingDB("admin").updateUser("bookings_operator", { pwd: passwordPrompt() })
```

| 参数 | 描述 |
| --- | --- |
| **`updateUser`** | (必需) 指定现有用户名的字符串。 |
| **`pwd`** | (可选) 指定新的原生用户密码，非空字符串。 |
{.fields}

解析器不提供通用的 `customData` 更新。

<span id="drop-user"></span>

## dropUser {#dropuser}

```javascript
db.getSiblingDB("admin").dropUser("bookings_operator")
```

`dropUser` 是必需的用户名字符串。无其他命令特定选项。

<span id="users-info"></span>

## usersInfo {#usersinfo}

```javascript
db.getSiblingDB("admin").getUser("bookings_operator", { showPrivileges: true })
```

| 参数 | 描述 |
| --- | --- |
| **`usersInfo`** | (必需) BSON int32、字符串或文档，用于选择要列出的用户。`1` 列出所有用户；字符串选择单个用户。文档形式为 `{ user: "<name>", db: "admin" }` 或 `{ forAllDBs: true }`。不支持数组。 |
| **`showPrivileges`** | (可选) 布尔值，请求权限信息；默认为 `false`，权限输出取决于服务器的 users-info 权限能力。 |
{.fields}

`forAllDBs` 不扩展认证命名空间：用户在 `admin` 中配置。解析器不识别 `showCredentials`、`showAuthenticationRestrictions` 或 `filter`。

后端也识别字符串 `getUser` 选择器，但 `getUser` 不是默认名称解析器识别的独立线协议命令。shell 的 `getUser()` 辅助函数发送 `usersInfo` 并从响应中提取选定用户。

<span id="grant-roles-to-user-and-revoke-roles-from-user"></span>

## grantRolesToUser 和 revokeRolesFromUser {#grantrolestouser-and-revokerolesfromuser}

在授予角色前，使用 [角色命令示例](/documentdb/reference/commands/security/role-commands/#createrole) 创建 `bookings_reader`。独立运行删除用户示例，以确保 `bookings_operator` 仍然存在。

```javascript
db.getSiblingDB("admin").grantRolesToUser(
  "bookings_operator", [{ role: "bookings_reader", db: "admin" }]
)
db.getSiblingDB("admin").revokeRolesFromUser(
  "bookings_operator", [{ role: "bookings_reader", db: "admin" }]
)
```

| 参数 | 描述 |
| --- | --- |
| **`grantRolesToUser`** | (必需) 指定现有用户名的字符串。 |
| **`revokeRolesFromUser`** | (必需) 指定现有用户名的字符串。 |
| **`roles`** | (必需) 指定非空角色列表的数组。条目可以是角色名字符串或 `{ role: "<name>", db: "admin" }` 文档。 |
{.fields}

成员限制和受支持的内置/自定义角色规则由后端强制执行。这些命令不会使 `updateUser.roles` 成为受支持的字段。

有关共享请求元数据，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

## 实现 {#implementation}

源码：`pg_documentdb/src/commands/users.c`、`ParseCreateUserSpec`、`ParseUpdateUserSpec`、`ParseDropUserSpec`、`ParseGetUserSpec`、`ParseGrantRolesToUserSpec` 和 `ParseRevokeRolesFromUserSpec` 解析器。
