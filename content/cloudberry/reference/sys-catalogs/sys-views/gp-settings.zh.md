---
title: "gp_settings"
description: "`gp_settings` 是一个集群级视图，显示每个主 Segment 的 `pg_settings` 信息。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/gp-settings.md"
---

|名称|类型|引用|说明|
|----|----|----------|-----------|
|`gp_segment_id`|integer| |Segment（或 Coordinator）实例的唯一标识符。|
|`name`|text| |运行时配置参数的名称。
|`setting`|text| |参数的当前值。|
|`unit`|text| |参数的隐含单位。|
|`category`|text| |参数所属的逻辑分组。|
|`short_desc`|text| |参数的简要说明。
|`extra_desc`|text| |参数的补充详细说明。|
|`context`|text| |设置参数值所需的上下文。|
|`vartype`|text| |参数类型（bool、enum、integer、real 或 string）
|`source`|text| |当前参数值的来源。
|`min_val`|text| |参数允许的最小值（非数值参数为 null）。|
|`max_val`|text| |参数允许的最大值（非数值参数为 null）。|
|`enumvals`|text[]| |枚举参数允许的值（非枚举参数为 null）。|
|`boot_val`|text| |如果未以其他方式设置参数，服务器启动时采用的参数值。|
|`reset_val`|text| |当前会话中 RESET 会将参数重置为的值。|
|`sourcefile`|text| |设置当前值的配置文件（如果值来自配置文件以外的来源，或查看此值的用户既不是超级用户，也不是 `pg_read_all_settings` 成员，则为 null）；在配置文件中使用 include 指令时，此信息很有帮助。|
|`sourceline`|integer| |在配置文件中设置当前值的行号（如果值来自配置文件以外的来源，或查看此值的用户既不是超级用户，也不是 pg_read_all_settings 成员，则为 null）。|
|`pending_restart`|boolean| |如果值已在配置文件中更改但需要重启才生效，则为 `true`；否则为 `false`。|
