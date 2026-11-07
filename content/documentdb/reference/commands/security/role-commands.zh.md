---
title: 角色管理命令
description: 支持在 DocumentDB 中创建、查询、删除和继承自定义角色的命令。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/security/role-commands.md
weight: 10
translation_source_sha256: 974699dc1d44a1b94094057629aa55ae17be4981dce6d65b6c7843296cb84c49
translation_review: AI-assisted bilingual review; 2026-11-07
---

在 `admin` 上运行角色管理命令。自定义角色功能需要启用角色的 CRUD 操作并具备适当的调用者权限。`dropRole`、`rolesInfo`、`grantRolesToRole` 和 `revokeRolesFromRole` 还需要集群版本 0.116 或更高版本。

<span id="create-role"></span>

## createRole {#createrole}

```javascript
db.getSiblingDB("admin").createRole({
  role: "bookings_reader",
  privileges: [{
    resource: { db: "bookings", collection: "flights" },
    actions: ["find"]
  }],
  roles: []
})
```

| 参数 | 描述 |
| --- | --- |
| **`createRole`** | (必需) 指定非空自定义角色名称的字符串；内置名称和保留名称将被拒绝。 |
| **`roles`** | (必需) 指定继承角色列表的数组，可为空。每个条目为角色名称字符串或 `{ role: "<name>", db: "admin" }`。 |
| **`privileges`** | (必需) 指定权限定义的文档数组，可为空。 |
| **`privileges[].resource`** | (每个权限中必需) 要求包含非空 `db` 字符串和 `collection` 字符串的文档。空集合名称表示数据库级别的集合作用域。其他资源形式将被拒绝。 |
| **`privileges[].actions`** | (每个权限中必需) 指定支持的操作名称的字符串数组：`find`、`insert`、`update`、`remove` 和 `changeStream`。未知操作将被拒绝。 |
{.fields}

继承必须引用已支持的现有角色，且不能引入循环。此解析器不支持集群级别的 MongoDB 资源文档和 `authenticationRestrictions`。

<span id="roles-info"></span>

## rolesInfo {#rolesinfo}

```javascript
db.getSiblingDB("admin").getRole("bookings_reader", {
  showPrivileges: true,
  showBuiltInRoles: false
})
```

| 参数 | 描述 |
| --- | --- |
| **`rolesInfo`** | (必需) BSON int32、字符串、文档或数组，用于选择要列出的角色；`1` 列出所有角色；否则使用角色名称、`{ role: "<name>", db: "admin" }` 或名称/文档数组。 |
| **`showBuiltInRoles`** | (可选) 布尔值，用于在列出时包含内置角色；默认为 `false`。 |
| **`showPrivileges`** | (可选) 布尔值，用于在列出时包含权限详情；默认为 `false`。不接受字符串模式，如 `"asUserFragment"`。 |
{.fields}

<span id="drop-role"></span>

## dropRole {#droprole}

```javascript
db.getSiblingDB("admin").dropRole("bookings_reader")
```

`dropRole` 是必需的自定义角色名称字符串。无法删除内置角色和保留角色。未实现其他命令特定选项。

<span id="grant-roles-to-role-and-revoke-roles-from-role"></span>

## grantRolesToRole 和 revokeRolesFromRole {#grantrolestorole-and-revokerolesfromrole}

在创建上述 `bookings_reader` 后，创建一个分发角色，添加其继承的读取权限，然后再移除该权限：

```javascript
db.getSiblingDB("admin").createRole({
  role: "bookings_dispatcher",
  privileges: [{
    resource: { db: "bookings", collection: "flights" },
    actions: ["update"]
  }],
  roles: []
})
db.getSiblingDB("admin").grantRolesToRole(
  "bookings_dispatcher", [{ role: "bookings_reader", db: "admin" }]
)
db.getSiblingDB("admin").revokeRolesFromRole(
  "bookings_dispatcher", [{ role: "bookings_reader", db: "admin" }]
)
```

| 参数 | 描述 |
| --- | --- |
| **`grantRolesToRole`** | (必需) 指定要修改的现有自定义角色的字符串。 |
| **`revokeRolesFromRole`** | (必需) 指定要修改的现有自定义角色的字符串。 |
| **`roles`** | (必需) 指定非空父角色列表的数组，使用字符串或 `{ role, db }` 文档。 |
{.fields}

无法修改内置角色；授予操作还强制执行继承循环和成员限制。

删除示例是独立的：在运行继承示例前不要删除 `bookings_reader`。

## 依赖提供方的角色变更 {#provider-dependent-role-mutations}

`updateRole`、`grantPrivilegesToRole` 和 `revokePrivilegesFromRole` 可由某些提供方实现。其可用性和选项取决于提供方。使用 `createRole` 按上述文档定义资源权限。

`writeConcern` 和 `comment` 等通用字段不会改变已实现的角色操作。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：`pg_documentdb/src/commands/roles.c`，角色解析器和 `command_update_role`、`grant_privileges_to_role`、`revoke_privileges_from_role`。
