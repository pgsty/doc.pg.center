---
title: "Spock 协议"
description: "Spock 输出插件通过 libpq 子协议将元组、元数据等从解码插件流式发送给接收端。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/protocol.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock_output 定义了一个 libpq 子协议，用于将元组、元数据等从解码插件流式发送给接收端。

该协议位于以下协议栈的最内层，顺序由外向内。

- TCP 或 Unix 套接字
  - libpq 协议
    - libpq 复制子协议（COPY BOTH 等）
      - Spock 输出插件到消费端的协议

因此，客户端可直接使用 libpq 的复制协议支持，也可通过封装 libpq 的驱动使用。

这是一个以紧凑表示为目标的二进制协议。

`spock_output` 还支持以 JSON 文本表示同一变更集，并提供相同的钩子，主要用于跟踪、调试和诊断。本文侧重二进制协议。

## 目录 {#table-of-contents}

- [协议流程](#protocol-flow)
- [协议消息](#protocol-messages)
- [启动消息](#startup-message)
- [启动错误](#startup-errors)
- [客户端传给输出插件的参数](#arguments-client-supplies-to-output-plugin)
- [可扩展性](#extensibility)
- [JSON 协议](#json-protocol)

## 协议流程 {#protocol-flow}

消息主要从上游 walsender 和解码插件流向下游接收端。

从下游流向上游的只有以下两类信息。

- 发给 `START_REPLICATION` 的初始参数列表。
- 重放进度消息。

`START_REPLICATION` 可以接受任意参数列表。之后没有向上游发送通用信息的通道，因而无法通过多轮协商或握手确定复制选项、二进制协议等。

在发送任何复制数据前，服务器先发出启动消息（见下文），告知所选设置。客户端可以接受；若无法接受，则更换启动选项并重连。

除通过初始参数和启动消息协商外，流程与其他基于 walsender 的逻辑复制插件一致。数据流在 COPY BOTH 模式中传输，每条 CopyData 消息封装复制数据，直到客户端断开。无法结束 COPY BOTH 模式后返回 walsender 命令解析器继续发送命令。这是 walsender 接口的限制。

## 协议消息 {#protocol-messages}

以下小节解释各类协议消息，后续章节介绍它们的交互流程。

所有顶层消息的第一个字节都是消息类型。代码中将其表示为字符，实际为与编码无关的有符号字节。

PostgreSQL 的 libpq COPY 协议已提供消息长度，因此顶层消息头无须另存长度。

### BEGIN 消息 {#begin-message}

行数据流从 `BEGIN` 消息开始。行只能在 `BEGIN` 之后、`COMMIT` 之前发送。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | 字面量 **B**（0x42） |
| 标志位 | uint8 | 位 0–3 保留。遇到已设置却无法识别的标志时，客户端*必须*报错。 |
| lsn | uint64 | 解码上下文中的 "final_lsn"，在此实现中为提交记录的 LSN |
| 提交时间 | uint64 | 解码上下文中的 "commit_time" |
| 远端 XID | uint32 | 解码上下文中的 "xid" |
{.wide .expand}

### 转发事务的来源消息 {#forwarded-transaction-origin-message}

`BEGIN` 后可以紧跟一条*转发事务来源*消息，表明事务最初来自哪个上游节点。

仅当上一条消息是 `BEGIN`、事务由其他节点转发，且已启用复制来源转发时才发送该消息。启用时启动应答中的 `forward_changeset_origins` 为 `t`。

「节点」可以是另一台主机、同一主机上的另一个数据库，也可以是其他实体。发现的来源名称会被原样转发。来源标识符格式由应用定义，*宜*带固定的应用名前缀，如 `bdr_` 或 `myapp_`。如何处理其他应用转发的事务，也由应用自行决定。

来源名称长度为零表示未能识别来源，但它很可能不是本地节点。此时如何处理由客户端决定。

来源消息只能紧接在 `BEGIN` 后收发，在其他位置出现都是协议错误。

在具体应用中，来源标识符通常与复制槽名、复制来源名称密切相关。

详见 README 的*转发变更集*一节。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | 字面量 **O**（0x4f） |
| 标志位 | uint8 | 位 0–3 保留。遇到已设置却无法识别的标志时，应用*必须*报错。 |
| origin_lsn | uint64 | 事务在来源节点上的提交记录 LSN（XLogRecPtr）。转发节点本地的提交 LSN 则是 BEGIN 消息里的 lsn。 |
| origin_identifier_length | uint8 | origin_identifier 的字节长度 |
| origin_identifier | signed char[origin_identifier_length] | 来源标识符，结构由上游应用定义。*宜*使用与上游数据库相同编码的文本，以 NUL 结尾，并尽量限于 7 位 ASCII。 |
{.wide .expand}

### COMMIT 消息 {#commit-message}

行数据流以 `COMMIT` 消息结束。

上游不发送已中止的事务，因此没有 `ROLLBACK` 消息。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | 字面量 **C**（0x43） |
| 标志位 | uint8 | 位 0–3 保留。遇到已设置却无法识别的标志时，客户端*必须*报错。 |
| 提交 LSN | uint64 | 解码提交回调中的 commit_lsn，与 BEGIN 消息中的值相同，标记事务结束。 |
| 结束 LSN | uint64 | 解码事务上下文中的 end_lsn |
| 提交时间 | uint64 | 解码事务上下文中的 commit_time |
{.wide .expand}

### INSERT、UPDATE 和 DELETE 消息 {#insert-update-or-delete-message}

`BEGIN` 或元数据消息之后，下游可收到零条或多条行变更消息。每条插入、更新或删除消息包含零个或多个元组字段，每个字段有一个或多个元组字段值。

行的 relidentifier *必须*与最近一条前置元数据消息的标识符相同。目前，相邻的行消息必须具有相同的 relidentifier。*以后若客户端声明支持元数据缓存，将可放宽要求，详见元数据消息。*

解码某一行时，只能使用该行到达前最近收到的元数据版本。以 M1、R1、R2、M2、R3、M4 为例，R1 和 R2 必须用 M1，R3 必须用 M2。用 M4 解码任何一行、用 M1 解码 R3，或用 M2 解码 R1、R2 都是错误。

行消息只能出现在 `BEGIN` 和 `COMMIT` 界定的事务内部。在事务外收到行消息是协议错误。

无法识别元组类型或元组部分类型时，下游必须断开并报告错误。双方应协商兼容性，上游不得未经协商便增加新的元组类型或字段类型。

下游持续读取行，直到遇到下一条非行消息。协议没有其他结束标记，也不预告一组消息中的行数。

#### 行消息头 {#row-message-header}

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | 插入 **I**（0x49）、更新 **U**（0x55）或删除 **D**（0x44） |
| 标志位 | uint8 | 行标志位（保留） |
| relidentifier | uint32 | 与该行的表元数据消息相匹配的 relidentifier。*BDR 不含此字段，改为发送 nspname 和 relname。* |
| [元组部分] | [复合结构] |  |
{.wide .expand}

接下来是一个或多个元组部分字段。

#### 元组字段 {#tuple-fields}

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 元组类型 | signed char | 标识正在发送的元组种类。 |
| tupleformat | signed char | **T** (0x54) |
| natts | uint16 | 此元组部分所传字段的数量。*BDR 也有此字段，但含义明显不同。* |
| [元组字段值] | [复合结构] |  |
{.wide .expand}

##### 元组格式兼容性 {#tuple-tupleformat-compatibility}

下游收到无法识别的 *tupleformat* 时，应按协议错误处理。

#### 元组字段值的结构 {#tuple-field-value-fields}

这些消息部分描述元组中的各个字段。

元组值字段有简写和完整两种形式，由第一个字段 *kind* 区分。

简写形式只含消息种类。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| kind | signed char | 空值字段，标记为 **n**（0x6e） |
{.wide .expand}

完整形式还含有长度和数据值。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| kind | signed char | 内部二进制字段：上游表中标作 **i**nternal binary（0x62）。 |
| length | int4 | 仅对 kind = i\|b\|t 有定义 |
| data | [length] | 数据的格式由表元数据和列的 *kind* 决定。 |
{.wide .expand}

##### 元组字段值的类型兼容性 {#tuple-field-values-kind-compatibility}

若下游不能识别字段的 *kind*，即发生协议错误，必须停止处理此协议流。

除非下游已通过协商表示接受，否则上游不得发送内部（**i**nternal）或二进制（**b**inary）格式的值。下游通常还会要求接收类型信息以解码这些值。详见启动参数和启动消息。

### 表与行的元数据消息 {#tablerow-metadata-messages}

发送某个关系的变更行之前，必须先发元数据消息，让下游知道命名空间、表名、列名及可选的列类型等。relidentifier 是在该条上游连接上唯一标识关系的任意数值，用于将元数据与后续行关联起来。

客户端不能假定关系元数据后一定会有行消息，更不能要求它紧跟元数据。协议将来可能在其他时机发送元数据。元数据消息可以出现在事务中或两个事务之间。

上游只能假定下游保留了最近一次表元数据消息，这一规则适用于所有表。收到表 y 的元数据时，客户端可丢弃表 x 的元数据。因此，切换表发送行之前，上游必须重新发送该表元数据，即使在同一会话甚至同一事务中已经发送过。*计划中的客户端元数据缓存会放宽此要求，客户端将通过输出插件参数声明支持。*

元数据消息中的列按出现顺序从 0 编至 natts-1。只需描述后续会发送行值的全部列，无须列出上游表所有列。上游可以省略在这一组行中不打算发送变更的列。即使表结构没变，同一张表不同批次元数据中的列编号也可能不同。

不能用新收到的元数据解码在它之前已经收到的行。

#### 表元数据头 {#table-metadata-header}

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | 字面量 **R**（0x52） |
| 标志位 | uint8 | 位 0–6 保留。遇到已设置却无法识别的标志时，客户端*必须*报错。 |
| relidentifier | uint32 | 由上游分配的关系标识符，在该上游内唯一。实际通常是上游表的 OID，但下游不能依赖这一点。 |
| nspnamelength | uint8 | 命名空间名称的长度（含末尾的 \0） |
| nspname | signed char[nspnamelength] | 关系所在的命名空间（以 NUL 结尾） |
| relnamelength | uint8 | 关系名称的长度（含末尾的 \0） |
| relname | char[relname] | 关系名称（以 NUL 结尾） |
| 属性块 | signed char | 字面量 **A**（0x41） |
| natts | uint16 | 属性数量 |
| [字段] | [复合结构] | 接下来是 natts 组列元数据。每组以列分隔符开头，随后有零个或多个格式相同的列元数据块，各带相同结构的块头。分块允许新增元数据消息而不破坏已有客户端。 |
{.wide .expand}

#### 列分隔符 {#column-delimiter}

每列的元数据都以列元数据头开始。它紧跟表元数据头中的 natts 字段，或紧跟上一列的最后一个元数据块。

首字段与其他元数据块一样是 char，标志字段与其他块的长度字段大小相同，所以可以安全地按列元数据块头读取。

目前唯一定义的标志是 0x1，表示该列属于关系的标识键。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| blocktype | signed char | **C**（0x43），表示列 |
| 标志位 | uint8 | 列信息标志位 |
{.wide .expand}

#### 列元数据块头 {#column-metadata-block-header}

所有列元数据块共用相同结构的头部，长度与列分隔符相同。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| blocktype | signed char | 标识后续元数据块的种类。 |
| blockbodylength | uint16 | 块的字节长度，不含 blocktype 字符和长度字段本身。 |
{.wide .expand}

#### 列名块 {#column-name-block}

这个块只携带列名。开头是列元数据块头，后续内容是列名。

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| [列元数据块头] | [复合结构] | blocktype = **N** (0x4e) |
| colname | char[blockbodylength] | 列名。 |
{.wide .expand}

#### 列类型块 {#column-type-block}

T.B.D.

第一版协议尚未定义。

可能会发送一个类型标识符（可能采用上游 OID），引用此前发出的「类型信息」协议消息。这样可以缓存类型描述，后续只发送 OID，无须重复传输长模式名和类型名。

设计时须能容纳以下类型。

- 核心内置类型
- 扩展类型（扩展版本可能不同）
- 枚举类型（CREATE TYPE ... AS ENUM）
- 范围类型（CREATE TYPE ... AS RANGE）
- 复合类型（CREATE TYPE ... AS (...)）
- 自定义类型（CREATE TYPE ( input = x_in, output = x_out )）

其中一些还可以嵌套。

## 启动消息 {#startup-message}

处理输出插件参数后，上游必须将启动消息作为第一条消息发送。它由简单的头部和交替出现的键、值字符串组成。每个字符串均为以 NUL 结尾的 unsigned char 序列。

该消息说明输出插件启用了哪些能力，并描述上游服务器和插件。客户端据此决定如何解码数据流，若结果无法接受，也可以断开并向用户报错。

若双方不兼容，或服务器无法满足必需选项而拒绝复制，启动消息后可能跟一条 libpq 协议的 FATAL 消息并终止会话。参见下文[启动错误](#startup-errors)。

参数名和值交替发送，每项都是以 NUL 结尾的字符串，例如：

`key1\0parameter1\0key2\0value2\0`

| 消息 | 类型／大小 | 注意事项 |
|---------|-----------|-------|
| 消息类型 | signed char | **S**（0x53），表示启动 |
| 启动消息版本 | uint8 | 值始终为 "1"。 |
| （参数） | 以 NUL 结尾的键和值 | 参数定义见下表。 |
{.wide .expand}

### 启动消息参数 {#startup-message-parameters}

所有参数值均以字符串传输。下表的类型表示应能将字符串解释成什么类型。

| 键名 | 值类型 | 说明 |
|----------|-----------|-------------|
| max_proto_version | 整数 | 输出插件支持的最高协议版本。此版本中为 5。 |
| min_proto_version | 整数 | 服务器支持的最低协议版本。此版本中为 4。 |
| proto_version | 整数 | 服务器从双方支持的版本交集中选定的协议版本。 |
| coltypes | 布尔值 | 是否随表元数据发送列类型。目前始终为 false。 |
| pg_version_num | 整数 | PostgreSQL 服务器的 server_version_num（如适用），例如 180000。 |
| pg_version | 字符串 | PostgreSQL 服务器的 server_version（如适用），例如 "18.0"。 |
| pg_catversion | uint32 | 上游为 PostgreSQL 时，表示其系统目录版本。 |
| database_encoding | 字符串 | 插件所在数据库的原生文本编码。 |
| encoding | 字符串 | 原生协议中文本、二进制和内部三种表示均以该编码传输文本字段值。目前原生协议始终使用 `database_encoding`，文本模式的 JSON 协议始终使用 `client_encoding`。 |
| forward_changeset_origins | 布尔值 | 告知客户端服务器是否会发送变更集来源信息。详见*转发变更集*。 |
| walsender_pid | 整数 | 上游服务器上 walsender 进程的 PID。 |
| spock_version | 字符串 | 上游服务器的 Spock 版本字符串，例如 "4.0.11"。 |
| spock_version_num | 整数 | 上游服务器的 Spock 数字版本号，例如 40011。 |
| no_txinfo | 布尔值 | 回显客户端的 no_txinfo 设置。为 true 时省略 XID、LSN 和时间戳等可变事务信息，主要用于测试。当前只有 JSON 协议会处理此选项。 |
{.wide .expand}

### 启动消息中的 binary 参数 {#startup-message-binary-parameters}

| 键名 | 值类型 | 说明 |
|----------|-----------|-------------|
| binary.internal_basetypes | 布尔值 | 为 true 时，类型合适且上下游二进制兼容参数匹配的字段可使用 PostgreSQL 内部二进制表示，可能涉及部分或全部字段。详见插件参数 `binary.want_internal_basetypes`。仅当客户端将 `binary.want_internal_basetypes` 置为 true 且双方格式匹配时才可为 true。 |
| binary.binary_basetypes | 布尔值 | 为 true 时，与 `binary.binary_pg_version` 兼容的内置基础类型可使用外部二进制交换格式（send/recv）。只有客户端将 `binary.want_binary_basetypes` 设为 true，且双方接受的 send/recv 格式匹配时才能启用。 |
| binary.basetypes_major_version | uint16 | 内部二进制值所兼容的 PostgreSQL 主版本，对应上游的 PG_VERSION_NUM/100。 |
| binary.binary_pg_version | uint16 | send/recv 格式所兼容的 PostgreSQL 主版本，未必与上游实际版本相同。 |
| binary.sizeof_int | uint8 | 上游的 sizeof(int)。 |
| binary.sizeof_long | uint8 | 上游的 sizeof(long)。 |
| binary.sizeof_datum | uint8 | 上游的 sizeof(Datum)，其中 Datum 为 PostgreSQL 定义的类型。 |
| binary.maxalign | uint8 | 上游 PostgreSQL 的 MAXIMUM_ALIGNOF，在构建时确定，依平台而异。 |
| binary.bigendian | 布尔值 | 当且仅当上游采用大端字节序时为 true。 |
| binary.float4_byval | 布尔值 | 上游 PostgreSQL 的 float4_byval 编译选项。 |
| binary.float8_byval | 布尔值 | 上游 PostgreSQL 的 float8_byval 编译选项。 |
| binary.integer_datetimes | 布尔值 | TIME、TIMESTAMP、TIMESTAMP WITH TIME ZONE 使用整数还是浮点数表示。通常取上游 PostgreSQL 的 integer_datetimes 编译选项。 |
{.wide .expand}

## 启动错误 {#startup-errors}

若支持的协议版本没有交集、参数格式无法识别、必需钩子等参数不受支持，服务器可能拒绝连接，并在启动应答之后发送<u>普通的 libpq 协议错误消息</u>。本文所述版本在启动消息之前发送它。

## 客户端传给输出插件的参数 {#arguments-client-supplies-to-output-plugin}

除了重放进度外，下游只有一次机会向输出插件传递信息，即开始复制时传给 START_REPLICATION 的参数。

双方没有来回交换多轮握手消息的机会。

客户端主要负责声明能力并提出请求。若缺少必需参数或存在无法解决的不兼容，输出插件会报错。否则它在下行的第一条启动消息中报告实际接受和未接受的选项。客户端再决定继续重放，或断开并向用户报错，必要时更换选项重连。

### 输出插件参数 {#output-plugin-arguments}

输出插件的参数以键值成对给出，可随 `START_REPLICATION` 等命令传入。

所有参数均以文本传输。考虑到服务器编码未知，*宜*限于 7 位 ASCII，也*可以*使用规范化的预组合 UTF-8。参数类型表示插件应尝试把字符串转换为什么类型。客户端不应发送超出该类型范围的值。

#### 能力声明 {#capabilities}

许多参数是客户端能力标志，表示支持元数据缓存、二进制传输等可选功能。输出插件*可以*忽略客户端声明支持的能力，按不支持处理。但客户端明确不支持或未声明的能力，插件*不得*启用。

也就是说，只向客户端发送它预期能处理的内容。

#### 协议版本协商 {#protocol-versioning}

客户端必须发送 `max_proto_version` 和 `min_proto_version` 以协商版本。双方支持的协议版本范围没有交集时，输出插件必须报错。

只有发生重大不兼容变更、全部或多数客户端都必须修改时，才提升协议版本。大多数变化通过新增可选消息或由客户端声明能力后选择启用来实现。

当前协议范围是 4 至 5。要使用协议 4 或 5，两端的 Spock 数字版本号都必须大于或等于 50000。

`startup_params_format` 标识启动参数集自身的格式，目前始终为 "1"。按名称查找参数，可以任意顺序给出。

| 键 | 类型 | 取值 | 注意事项 |
|-----|------|----------|-------|
| startup_params_format | uint32 | 1 | 本组启动参数的格式版本，目前始终为 1。**必填**，缺失时报错。 |
| max_proto_version | uint32 | 4-5 | 客户端支持的最高协议版本。版本太旧时输出插件必须报错。**必填**，缺失时报错。 |
| min_proto_version | uint32 | 4-5 | 客户端支持的最低协议版本。支持版本过旧时报错。**必填**，缺失时报错。 |
{.wide .expand}

#### 客户端要求与能力 {#client-requirements-and-capabilities}

| 键 | 类型 | 默认值 | 注意事项 |
|-----|------|---------|-------|
| expected_encoding | 字符串 | null | 下游期望文本字段采用的编码，对原生格式中的文本、二进制和内部表示均有效，不影响其他协议内容。指定后上游必须遵守。对于 JSON 协议，须留空或与 `client_encoding` 一致。当前原生协议若指定了与上游数据库编码不同的值，插件会报错。 |
| proto_format | 字符串 | null | 所请求的协议格式：本文所述的 "native" 或 "json"。默认为 native（二进制）。 |
| no_txinfo | 布尔值 | false | 为 true 时，请求省略 XID、LSN、时间戳等可变事务信息，主要用于测试。当前只有 JSON 协议会处理该请求。 |
{.wide .expand}

#### Spock 专用参数 {#spock-specific-parameters}

这些参数专用于 Spock 扩展，控制复制哪些数据。

| 键 | 类型 | 默认值 | 注意事项 |
|-----|------|---------|-------|
| spock.forward_origins | 字符串 | null | 以逗号分隔的待转发复制来源列表。目前只接受特殊值 "all"。 |
| spock.replication_set_names | 字符串 | null | 以逗号分隔的订阅复制集名。指定后，只发送这些复制集中的变更。 |
| spock.replicate_only_table | 字符串 | null | 要复制的单张表的限定名称（schema.table）。设置后只发送该表的变更，用于初始表同步。 |
| hooks.setup_function | 字符串 | null | 用于兼容 Spock 1.x 的旧参数，当前会忽略。 |
{.wide .expand}

#### 客户端基本信息 {#general-client-information}

这些键主要供输出插件了解客户端情况。尤其*不能*用版本号判断内部二进制或 send/recv 的兼容性。非 PostgreSQL 客户端不会发送版本号，但仍可能支持这些格式。

| 键 | 类型 | 默认值 | 注意事项 |
|-----|------|---------|-------|
| pg_version | uint32 | null | 下游为 PostgreSQL 时的 PG_VERSION_NUM，例如 180000。注意，尽管键名容易误解，此处是数字版本号，对应启动消息中的 pg_version_num。 |
| spock_version | 字符串 | null | 下游 Spock 的版本字符串，例如 "4.0.11"。若与服务器版本不同，上游会记入日志。 |
| spock_version_num | uint32 | null | 下游 Spock 的数字版本号，例如 40011。若与服务器版本不同，上游会记入日志。 |
{.wide .expand}

#### 二进制值交换参数 {#parameters-relating-to-exchange-of-binary-values}

下游可通过 `binary.want_binary_basetypes` 和 `binary.want_internal_basetypes` 等选项声明能够解释 PostgreSQL 内部二进制数据值和／或二进制交换格式（send/recv）。将来也可能定义其他选项。

若上游不支持其中一种或两种格式，*可以*忽略下游的二进制能力，使用文本格式，并忽略全部 `binary.*` 参数。所有下游*必须*支持文本。除非下游声明可以接收，上游*不得*使用内部二进制或 send/recv。两端都支持两种格式时，应优先用内部二进制，兼容性需要时退回 send/recv，再退回文本。

应逐类型选择内部二进制或交换格式。内置类型使用二进制、扩展类型使用文本很常见。

下游请求其中一种或两种格式时，*必须*声明相应的兼容性要求。若不兼容，上游*必须*按内部二进制、send/recv、文本的次序回退。

某项兼容性参数未指定时，上游*必须*假定下游不支持，这样旧客户端才不会收到无法识别的新格式。例如，假设 PostgreSQL 99.8 将 NUMERIC 从任意长度的 BCD（二进制编码十进制）改成 128 位 DPD（密集压缩十进制），协议就可增加 `binary.dpd_numerics`。旧客户端不会设置它，上游便按文本发送 NUMERIC。支持新格式的客户端会声明 `dpd_numerics = true`，因此从旧服务器也不会以二进制接收旧格式。

目前下游对每个选项只能声明一种兼容值。例如，不能同时声明 sizeof(int) 可以为 4 或 8 字节。留空表示上游必须假定两种均不受支持。今后的协议可能允许声明多组可替代的格式。

*不得*用 `pg_version` 判断兼容性，应使用 `binary.basetypes_major_version`。

| 键名 | 值类型 | 默认值 | 说明 |
|----------|-----------|---------|-------------|
| binary.want_binary_basetypes | 布尔值 | false | 客户端接受内置基础类型的二进制交换格式（send/recv）时为 true。 |
| binary.want_internal_basetypes | 布尔值 | false | 客户端接受 PostgreSQL 基础类型的内部二进制表示时为 true，另有专门规定的类型除外。 |
| binary.basetypes_major_version | uint32 | null | 下游期望内部二进制和 send/recv 格式兼容的 PostgreSQL 主版本。上游说明将其记为 PG_VERSION_NUM/100，并以 PostgreSQL 18.0 的 180 为例。 |
| binary.sizeof_int | uint32 | null | 下游的 sizeof(int)。 |
| binary.sizeof_long | uint32 | null | 下游的 sizeof(long)。 |
| binary.sizeof_datum | uint32 | null | 下游的 sizeof(Datum)，即 PostgreSQL 的 Datum 类型。 |
| binary.bigendian | 布尔值 | null | 当且仅当下游采用大端字节序时为 true。 |
| binary.float4_byval | 布尔值 | null | 下游 PostgreSQL 的 float4_byval 编译选项。 |
| binary.float8_byval | 布尔值 | null | 下游 PostgreSQL 的 float8_byval 编译选项。 |
| binary.integer_datetimes | 布尔值 | null | 下游 PostgreSQL 的 integer_datetimes 编译选项。 |
{.wide .expand}

> **注意**：下游客户端*不发送* `binary.maxalign`。它只出现在上游的启动消息中。上游用自身的 MAXIMUM_ALIGNOF 判断二进制兼容性。

## 可扩展性 {#extensibility}

输出插件参数可以按需提供，启动数据包则确认或答复所选参数。借此，上下游可以执行一次基本的能力协商。

未经客户端确认能理解新数据，输出插件不得发送新的必选数据或更改线上格式。可选数据可以无需协商而发送。

为输出插件扩充参数时，各键应以扩展名为前缀，最好用一个顶层键和一个 JSON 对象值承载扩展信息。扩充启动消息时也应遵循这种约定。

可通过钩子和插件添加某个客户端专用的功能。

## JSON 协议 {#json-protocol}

`proto_format` 设为 `json` 时，输出插件改为发送 JSON，主要用于调试和诊断。

JSON 格式支持相同的全部钩子。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/protocol.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
