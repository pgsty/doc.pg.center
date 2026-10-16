---
title: مرجع واجهة برمجة التطبيقات (API)
weight: 3800
description: "المرجع الكامل لواجهة برمجة تطبيقات etcd v3"
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

هذا المرجع لواجهة برمجة التطبيقات مُولَّد تلقائيًا من ملفات `.proto` المذكورة.

##### service `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable يفعّل المصادقة. |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable يعطّل المصادقة. |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus يعرض حالة المصادقة. |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate يعالج طلب مصادقة. |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd يضيف مستخدمًا جديدًا. لا يمكن أن يكون اسم المستخدم فارغًا. |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet يجلب معلومات مستخدم تفصيلية. |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList يجلب قائمة بجميع المستخدمين. |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete يحذف مستخدمًا محددًا. |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword يغيّر كلمة مرور مستخدم محدد. |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrantRole يمنح دورًا لمستخدم محدد. |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole يسحب دورًا من مستخدم محدد. |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd يضيف دورًا جديدًا. لا يمكن أن يكون اسم الدور فارغًا. |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet يجلب معلومات دور تفصيلية. |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList يجلب قوائم بجميع الأدوار. |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete يحذف دورًا محددًا. |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission يمنح إذن مفتاح أو نطاق محدد لدور محدد. |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission يسحب إذن مفتاح أو نطاق من دور محدد. |

##### service `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd يضيف عضوًا إلى العنقود. |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove يزيل عضوًا موجودًا من العنقود. |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate يحدّث إعداد العضو. |
| MemberList | MemberListRequest | MemberListResponse | MemberList يسرد جميع الأعضاء في العنقود. |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote يرقّي عضوًا من متعلم raft (غير مصوّت) إلى عضو مصوّت في raft. |

##### service `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range يجلب المفاتيح في النطاق من مخزن المفاتيح/القيم. |
| Put | PutRequest | PutResponse | Put يضع المفتاح المعطى في مخزن المفاتيح/القيم. يزيد طلب put مراجعة مخزن المفاتيح/القيم ويولّد حدثًا واحدًا في سجل الأحداث. |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange يحذف النطاق المعطى من مخزن المفاتيح/القيم. يزيد طلب الحذف مراجعة مخزن المفاتيح/القيم ويولّد حدث حذف في سجل الأحداث لكل مفتاح محذوف. |
| Txn | TxnRequest | TxnResponse | Txn يعالج طلبات متعددة في معاملة واحدة. يزيد طلب txn مراجعة مخزن المفاتيح/القيم ويولّد أحداثًا بالمراجعة نفسها لكل طلب مكتمل. لا يجوز تعديل المفتاح نفسه عدة مرات داخل txn واحد. |
| Compact | CompactionRequest | CompactionResponse | Compact يضغط سجل الأحداث في مخزن مفاتيح/قيم etcd. ينبغي ضغط مخزن المفاتيح/القيم دوريًا وإلا استمر سجل الأحداث في النمو إلى ما لا نهاية. |

##### service `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant ينشئ عقد إيجار (lease) تنتهي صلاحيته إذا لم يستلم الخادم keepAlive خلال مدة بقاء معطاة. ستنتهي صلاحية جميع المفاتيح المرفقة بعقد الإيجار وتُحذف إذا انتهت صلاحية عقد الإيجار. يولّد كل مفتاح منتهي الصلاحية حدث حذف في سجل الأحداث. |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke يبطل عقد إيجار. ستنتهي صلاحية جميع المفاتيح المرفقة بعقد الإيجار وتُحذف. |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive يبقي عقد الإيجار نشطًا عن طريق بث طلبات الحفاظ على الحياة (keep alive) من العميل إلى الخادم وبث ردود الحفاظ على الحياة من الخادم إلى العميل. |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive يسترجع معلومات عقد الإيجار. |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases يسرد جميع عقود الإيجار الموجودة. |

##### service `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | Alarm يفعّل الإنذارات ويعطّلها ويستعلم عنها فيما يتعلق بصحة العنقود. |
| Status | StatusRequest | StatusResponse | Status يجلب حالة العضو. |
| Defragment | DefragmentRequest | DefragmentResponse | Defragment يزيل تجزئة قاعدة البيانات الخلفية للعضو لاستعادة مساحة تخزين. |
| Hash | HashRequest | HashResponse | Hash يحسب تجزئة فضاء مفاتيح الواجهة الخلفية بالكامل، بما في ذلك الحاويات (buckets) key وlease وغيرها في التخزين. هذا مصمم للاختبار فقط! لا تعتمد عليه في الإنتاج مع معاملات جارية، لأن عملية Hash لا تمسك أقفال MVCC. استخدم واجهة "HashKV" API بدلًا منها لفحوصات اتساق الحاوية "key". |
| HashKV | HashKVRequest | HashKVResponse | HashKV يحسب تجزئة جميع مفاتيح MVCC حتى مراجعة معينة. وهو يجتاز الحاوية "key" فقط في التخزين الخلفي. |
| Snapshot | SnapshotRequest | SnapshotResponse | Snapshot يرسل لقطة للواجهة الخلفية بأكملها من عضو عبر تدفق إلى عميل. |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | MoveLeader يطلب من عقدة القائد الحالية نقل قيادتها إلى المستلِم (transferee). |
| Downgrade | DowngradeRequest | DowngradeResponse | Downgrade يطلب تخفيضات، أو يتحقق من الجدوى، أو يلغي التخفيض على إصدار العنقود. مدعوم منذ etcd 3.5. |

##### service `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watch يراقب الأحداث الجارية أو التي حدثت. المدخل والمخرج كلاهما تدفقات؛ تدفق المدخل لإنشاء المراقبين (watchers) وإلغائهم، وتدفق المخرج يرسل الأحداث. يمكن لاستدعاء RPC واحد للمراقبة أن يراقب نطاقات مفاتيح متعددة، باثًا أحداث عدة مراقبات في آن واحد. يمكن مراقبة سجل الأحداث بأكمله بدءًا من مراجعة الضغط الأخيرة. |

##### message `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID هو معرّف العضو المرتبط بالإنذار المُثار. | uint64 |
| alarm | alarm هو نوع الإنذار الذي أُثير. | AlarmType |

##### message `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action هو نوع طلب الإنذار الذي سيُصدر. يمكن للإجراء أن يجلب (GET) حالات الإنذارات، أو يفعّل (ACTIVATE) إنذارًا، أو يعطّل (DEACTIVATE) إنذارًا مُثارًا. | AlarmAction |
| memberID | memberID هو معرّف العضو المرتبط بالإنذار. إذا كان memberID يساوي 0، فإن طلب الإنذار يشمل جميع الأعضاء. | uint64 |
| alarm | alarm هو نوع الإنذار المطلوب اعتباره لهذا الطلب. | AlarmType |

##### message `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms هي قائمة بالإنذارات المرتبطة بطلب الإنذار. | (slice of) AlarmMember |

##### message `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name هو اسم الدور المراد إضافته إلى نظام المصادقة. | string |

##### message `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### message `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### message `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (slice of) authpb.Permission |

##### message `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name هو اسم الدور الذي سيُمنح الإذن. | string |
| perm | perm هو الإذن المطلوب منحه للدور. | authpb.Permission |

##### message `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### message `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### message `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision هي المراجعة الحالية لمخزن المصادقة | uint64 |

##### message `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### message `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name هو اسم المستخدم الجاري تغيير كلمة مروره. | string |
| password | password هي كلمة المرور الجديدة للمستخدم. لاحظ أن هذا الحقل ستتم إزالته في طبقة API. | string |
| hashedPassword | hashedPassword هي كلمة المرور المُجزّأة الجديدة للمستخدم. لاحظ أن هذا الحقل ستتم تهيئته في طبقة API. | string |

##### message `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name هو اسم المستخدم المراد حذفه. | string |

##### message `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### message `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### message `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user هو اسم المستخدم الذي ينبغي منحه دورًا معينًا. | string |
| role | role هو اسم الدور المطلوب منحه للمستخدم. | string |

##### message `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (slice of) string |

##### message `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### message `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### message `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | token هو رمز (token) مصرّح به يمكن استخدامه في استدعاءات RPC اللاحقة | string |

##### message `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

يضغط CompactionRequest مخزن المفاتيح/القيم حتى مراجعة معينة. ستُزال جميع المفاتيح المتجاوزة ذات المراجعة الأقل من مراجعة الضغط.

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision هي مراجعة مخزن المفاتيح/القيم لعملية الضغط. | int64 |
| physical | يُضبط physical بحيث ينتظر RPC حتى يُطبَّق الضغط فعليًا على قاعدة البيانات المحلية بحيث تُزال المدخلات المضغوطة كليًا من قاعدة البيانات الخلفية. | bool |

##### message `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result هي عملية المقارنة المنطقية لهذه المقارنة. | CompareResult |
| target | target هو حقل المفتاح/القيمة المطلوب فحصه للمقارنة. | CompareTarget |
| key | key هو المفتاح موضوع عملية المقارنة. | bytes |
| target_union |  | oneof |
| version | version هي إصدار المفتاح المعطى | int64 |
| create_revision | create_revision هي مراجعة إنشاء المفتاح المعطى | int64 |
| mod_revision | mod_revision هي آخر مراجعة تعديل للمفتاح المعطى. | int64 |
| value | value هي قيمة المفتاح المعطى، بالبايتات. | bytes |
| lease | lease هو معرّف عقد الإيجار للمفتاح المعطى. | int64 |
| range_end | يقارن range_end الهدف المعطى بجميع المفاتيح في النطاق [key, range_end). راجع RangeRequest لمزيد من التفاصيل عن نطاقات المفاتيح. | bytes |

##### message `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key هو أول مفتاح يُحذف في النطاق. | bytes |
| range_end | range_end هو المفتاح التالي لآخر مفتاح يُحذف للنطاق [key, range_end). إذا لم يُعطَ range_end، فسيُعرَّف النطاق ليحتوي وسيط المفتاح فقط. إذا كان range_end هو المفتاح المعطى زائد واحد، فالنطاق هو جميع المفاتيح ذات البادئة (المفتاح المعطى). إذا كان range_end هو '\0'، فالنطاق هو جميع المفاتيح الأكبر من وسيط المفتاح أو المساوية له. | bytes |
| prev_kv | إذا ضُبط prev_kv، فسيحصل etcd على أزواج المفاتيح/القيم السابقة قبل حذفها. ستُرجَع أزواج المفاتيح/القيم السابقة في رد الحذف. | bool |

##### message `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted هو عدد المفاتيح التي حذفها طلب حذف النطاق. | int64 |
| prev_kvs | إذا ضُبط prev_kv في الطلب، فستُرجَع أزواج المفاتيح/القيم السابقة. | (slice of) mvccpb.KeyValue |

##### message `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| enabled | enabled يشير إلى ما إذا كان العنقود مفعّلًا للتخفيض. | bool |
| targetVersion | targetVersion هي إصدار التخفيض المستهدف. | string |

##### message `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action هو نوع طلب التخفيض الذي سيُصدر. يمكن للإجراء أن يتحقق (VALIDATE) من الإصدار المستهدف، أو يخفّض (DOWNGRADE) إصدار العنقود، أو يلغي (CANCEL) مهمة التخفيض الجارية. | DowngradeAction |
| version | version هي الإصدار المستهدف للتخفيض. | string |

##### message `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version هي إصدار العنقود الحالي. | string |

##### message `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

يُستخدم DowngradeVersionTestRequest للاختبار فقط. سيُقرأ الإصدار في هذا الطلب بوصفه إصدار سجل WAL. إذا كان إصدار هدف التخفيض أقل من هذا الإصدار، فإن التخفيض (أثناء التشغيل) أو الترحيل (أثناء التوقف) غير آمن، ومن ثم لا ينبغي السماح به.

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### message `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision هي مراجعة مخزن المفاتيح/القيم لعملية التجزئة. | int64 |

##### message `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash هي قيمة التجزئة المحسوبة من مفاتيح MVCC للعضو المستجيب حتى مراجعة معينة. | uint32 |
| compact_revision | compact_revision هي المراجعة المضغوطة لمخزن المفاتيح/القيم عند بدء التجزئة. | int64 |
| hash_revision | hash_revision هي المراجعة التي تُحسب التجزئة حتى الوصول إليها. | int64 |

##### message `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash هي قيمة التجزئة المحسوبة من الواجهة الخلفية للمفاتيح/القيم للعضو المستجيب. | uint32 |

##### message `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف عقد الإيجار المراد تسجيل نقطة تحقق (checkpoint) له. | int64 |
| remaining_TTL | Remaining_TTL هو الوقت المتبقي حتى انتهاء صلاحية عقد الإيجار. | int64 |

##### message `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice of) LeaseCheckpoint |

##### message `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL هي مدة البقاء (time-to-live) الاستشارية بالثواني. سيرجع عقد الإيجار منتهي الصلاحية -1. | int64 |
| ID | ID هو المعرّف المطلوب لعقد الإيجار. إذا ضُبط ID على 0، يختار المؤجِّر معرّفًا. | int64 |

##### message `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID هو معرّف عقد الإيجار لعقد الإيجار الممنوح. | int64 |
| TTL | TTL هي مدة بقاء عقد الإيجار التي اختارها الخادم بالثواني. | int64 |
| error |  | string |

##### message `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف عقد الإيجار المطلوب إبقاؤه نشطًا. | int64 |

##### message `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID هو معرّف عقد الإيجار الوارد من طلب الحفاظ على الحياة. | int64 |
| TTL | TTL هي مدة البقاء الجديدة لعقد الإيجار. | int64 |

##### message `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (slice of) LeaseStatus |

##### message `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف عقد الإيجار المطلوب إبطاله. عند إبطال المعرّف، ستُحذف جميع المفاتيح المرتبطة. | int64 |

##### message `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### message `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف عقد الإيجار لعقد الإيجار. | int64 |
| keys | keys تساوي true للاستعلام عن جميع المفاتيح المرفقة بعقد الإيجار هذا. | bool |

##### message `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID هو معرّف عقد الإيجار الوارد من طلب الحفاظ على الحياة. | int64 |
| TTL | TTL هي مدة البقاء المتبقية بالثواني لعقد الإيجار؛ ستنتهي صلاحية عقد الإيجار في أقل من TTL+1 ثانية. | int64 |
| grantedTTL | GrantedTTL هو الوقت الممنوح مبدئيًا بالثواني عند إنشاء/تجديد عقد الإيجار. | int64 |
| keys | Keys هي قائمة المفاتيح المرفقة بعقد الإيجار هذا. | (slice of) bytes |

##### message `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف العضو لهذا العضو. | uint64 |
| name | name هو الاسم المقروء للبشر للعضو. إذا لم يُبدأ العضو، فسيكون الاسم سلسلة فارغة. | string |
| peerURLs | peerURLs هي قائمة عناوين URL التي يكشفها العضو للعنقود من أجل التواصل. | (slice of) string |
| clientURLs | clientURLs هي قائمة عناوين URL التي يكشفها العضو للعملاء من أجل التواصل. إذا لم يُبدأ العضو، فستكون clientURLs فارغة. | (slice of) string |
| isLearner | isLearner يشير إلى ما إذا كان العضو متعلم raft. | bool |

##### message `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs هي قائمة عناوين URL التي سيستخدمها العضو المضاف للتواصل مع العنقود. | (slice of) string |
| isLearner | isLearner يشير إلى ما إذا كان العضو المضاف متعلم raft. | bool |

##### message `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member هي معلومات العضو للعضو المضاف. | Member |
| members | members هي قائمة بجميع الأعضاء بعد إضافة العضو الجديد. | (slice of) Member |

##### message `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### message `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members هي قائمة بجميع الأعضاء المرتبطين بالعنقود. | (slice of) Member |

##### message `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف العضو للعضو المراد ترقيته. | uint64 |

##### message `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members هي قائمة بجميع الأعضاء بعد ترقية العضو. | (slice of) Member |

##### message `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف العضو للعضو المراد إزالته. | uint64 |

##### message `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members هي قائمة بجميع الأعضاء بعد إزالة العضو. | (slice of) Member |

##### message `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID هو معرّف العضو للعضو المراد تحديثه. | uint64 |
| peerURLs | peerURLs هي القائمة الجديدة لعناوين URL التي سيستخدمها العضو للتواصل مع العنقود. | (slice of) string |

##### message `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members هي قائمة بجميع الأعضاء بعد تحديث العضو. | (slice of) Member |

##### message `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID هو معرّف العقدة للقائد الجديد. | uint64 |

##### message `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key هو المفتاح، بالبايتات، المراد وضعه في مخزن المفاتيح/القيم. | bytes |
| value | value هي القيمة، بالبايتات، المطلوب ربطها بالمفتاح في مخزن المفاتيح/القيم. | bytes |
| lease | lease هو معرّف عقد الإيجار المطلوب ربطه بالمفتاح في مخزن المفاتيح/القيم. قيمة lease تساوي 0 تعني عدم وجود عقد إيجار. | int64 |
| prev_kv | إذا ضُبط prev_kv، فسيحصل etcd على زوج المفتاح/القيمة السابق قبل تغييره. سيُرجَع زوج المفتاح/القيمة السابق في رد الوضع (put). | bool |
| ignore_value | إذا ضُبط ignore_value، فسيحدّث etcd المفتاح باستخدام قيمته الحالية. ويرجع خطأً إذا لم يكن المفتاح موجودًا. | bool |
| ignore_lease | إذا ضُبط ignore_lease، فسيحدّث etcd المفتاح باستخدام عقد الإيجار الحالي له. ويرجع خطأً إذا لم يكن المفتاح موجودًا. | bool |

##### message `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | إذا ضُبط prev_kv في الطلب، فسيُرجَع زوج المفتاح/القيمة السابق. | mvccpb.KeyValue |

##### message `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key هو أول مفتاح للنطاق. إذا لم يُعطَ range_end، فسيبحث الطلب عن key فقط. | bytes |
| range_end | range_end هو الحد الأعلى للنطاق المطلوب [key, range_end). إذا كان range_end هو '\0'، فالنطاق هو جميع المفاتيح >= key. إذا كان range_end هو المفتاح زائد واحد (مثل "aa"+1 == "ab" و"a\xff"+1 == "b")، فسيجلب طلب النطاق جميع المفاتيح ذات البادئة key. إذا كان كل من key وrange_end هو '\0'، فسيرجع طلب النطاق جميع المفاتيح. | bytes |
| limit | limit هي حد لعدد المفاتيح المُرجَعة للطلب. عندما تُضبط limit على 0، تُعامل بوصفها بلا حد. | int64 |
| revision | revision هي النقطة الزمنية لمخزن المفاتيح/القيم المراد استخدامها للنطاق. إذا كانت revision أقل من الصفر أو تساويه، فالنطاق يجري على أحدث مخزن مفاتيح/قيم. إذا كانت المراجعة قد ضُغطت، فسيُرجَع ErrCompacted كاستجابة. | int64 |
| sort_order | sort_order هي ترتيب النتائج المرتبة المُرجَعة. | SortOrder |
| sort_target | sort_target هو حقل المفتاح/القيمة المراد استخدامه للترتيب. | SortTarget |
| serializable | serializable تضبط طلب النطاق لاستخدام قراءات محلية للعضو قابلة للتسلسل. طلبات النطاق خطّية (linearizable) بشكل افتراضي؛ فالطلبات الخطية لها زمن استجابة أعلى ومعدل نقل أقل من الطلبات القابلة للتسلسل لكنها تعكس التوافق الحالي للعنقود. للحصول على أداء أفضل، مقابل قراءات قديمة محتملة، يُخدَم طلب النطاق القابل للتسلسل محليًا دون حاجة للوصول إلى توافق مع العقد الأخرى في العنقود. | bool |
| keys_only | keys_only عند ضبطها ترجع المفاتيح فقط دون القيم. | bool |
| count_only | count_only عند ضبطها ترجع عدد المفاتيح في النطاق فقط. | bool |
| min_mod_revision | min_mod_revision هي الحد الأدنى لمراجعات تعديل المفاتيح المُرجَعة؛ ستُستبعد جميع المفاتيح ذات مراجعات التعديل الأقل. | int64 |
| max_mod_revision | max_mod_revision هي الحد الأعلى لمراجعات تعديل المفاتيح المُرجَعة؛ ستُستبعد جميع المفاتيح ذات مراجعات التعديل الأكبر. | int64 |
| min_create_revision | min_create_revision هي الحد الأدنى لمراجعات إنشاء المفاتيح المُرجَعة؛ ستُستبعد جميع المفاتيح ذات مراجعات الإنشاء الأقل. | int64 |
| max_create_revision | max_create_revision هي الحد الأعلى لمراجعات إنشاء المفاتيح المُرجَعة؛ ستُستبعد جميع المفاتيح ذات مراجعات الإنشاء الأكبر. | int64 |

##### message `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs هي قائمة أزواج المفاتيح/القيم التي طابقها طلب النطاق. تكون kvs فارغة عند طلب العد. | (slice of) mvccpb.KeyValue |
| more | more تشير إلى ما إذا كانت هناك مفاتيح أخرى لإرجاعها في النطاق المطلوب. | bool |
| count | تُضبط count على العدد الفعلي للمفاتيح داخل النطاق عند الطلب. وخلافًا لـKvs، لا تتأثر بالحدود والمرشحات (مثل Min/Max وCreate/Modify وRevisions) وتعكس العدد الكامل داخل النطاق المحدد. | int64 |

##### message `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request هو اتحاد لأنواع الطلبات التي تقبلها المعاملة. | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### message `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id هو معرّف العنقود الذي أرسل الاستجابة. | uint64 |
| member_id | member_id هو معرّف العضو الذي أرسل الاستجابة. | uint64 |
| revision | revision هي مراجعة مخزن المفاتيح/القيم عند تطبيق الطلب، وهي غير مضبوطة (أي 0) في حالة الاستدعاءات التي لا تتفاعل مع مخزن المفاتيح/القيم. بالنسبة لاستجابات تقدم المراقبة، تشير header.revision إلى التقدم. جميع الأحداث المستقبلية المستلمة في هذا التدفق مضمونة أن يكون رقم مراجعتها أعلى من رقم header.revision. | int64 |
| raft_term | raft_term هي فترة raft عند تطبيق الطلب. | uint64 |

##### message `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response هو اتحاد لأنواع الاستجابات التي ترجعها المعاملة. | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### message `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header يحمل معلومات مخزن المفاتيح/القيم الحالية. يشير أول header في تدفق اللقطة إلى النقطة الزمنية للقطة. | ResponseHeader |
| remaining_bytes | remaining_bytes هو عدد بايتات الـblob التي سيتم إرسالها بعد هذه الرسالة | uint64 |
| blob | blob يحتوي على الجزء التالي من اللقطة في تدفق اللقطة. | bytes |
| version | إصدار مخطط التخزين المسجل في اللقطة. يُقرأ هذا من الواجهة الخلفية المحلية للعضو وقد يختلف عن إصداره الثنائي. يشير إلى إصدار تخزين etcd الذي يجب دعمه عند استعادة اللقطة. | string |

##### message `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version هي الإصدار الثنائي لعضو etcd المستجيب. يُبلَّغ عن إصدار مخطط التخزين بشكل منفصل في storageVersion. | string |
| dbSize | dbSize هي حجم قاعدة البيانات الخلفية المخصص فعليًا، بالبايتات، للعضو المستجيب. | int64 |
| leader | leader هو معرّف العضو الذي يعتقد العضو المستجيب أنه القائد الحالي. | uint64 |
| raftIndex | raftIndex هو فهرس raft المثبَّت (committed) الحالي للعضو المستجيب. | uint64 |
| raftTerm | raftTerm هي فترة raft الحالية للعضو المستجيب. | uint64 |
| raftAppliedIndex | raftAppliedIndex هو فهرس raft المطبق الحالي للعضو المستجيب. | uint64 |
| errors | errors يحتوي على معلومات الإنذار/الصحة والحالة. | (slice of) string |
| dbSizeInUse | dbSizeInUse هي حجم قاعدة البيانات الخلفية المستخدم منطقيًا، بالبايتات، للعضو المستجيب. | int64 |
| isLearner | isLearner يشير إلى ما إذا كان العضو متعلم raft. | bool |
| storageVersion | storageVersion هي إصدار ملف قاعدة البيانات. قد تُحدَّث بتأخر بالنسبة إلى إصدار العنقود المستهدف. | string |
| dbSizeQuota | dbSizeQuota هي حصة تخزين etcd المُهيَّأة بالبايتات (القيمة الممررة إلى نسخة etcd عبر العلم --quota-backend-bytes) | int64 |
| downgradeInfo | downgradeInfo تشير إلى ما إذا كانت هناك عملية تخفيض. | DowngradeInfo |

##### message `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

من ورقة paxosdb الخاصة بـgoogle: يعتمد تنفيذنا على بدائية قوية نسميها MultiOp. تُنفَّذ جميع عمليات قاعدة البيانات الأخرى باستثناء اجتياز المدخلات كاستدعاء واحد لـMultiOp. يُطبَّق MultiOp ذريًا ويتكون من ثلاثة مكونات: 1. قائمة اختبارات تسمى guard. يفحص كل اختبار في guard مدخلًا واحدًا في قاعدة البيانات. قد يفحص غياب قيمة أو وجودها، أو يقارنها بقيمة معطاة. قد ينطبق اختباران مختلفان في guard على المدخل نفسه أو مداخل مختلفة في قاعدة البيانات. تُطبَّق جميع الاختبارات في guard ويرجع MultiOp النتائج. إذا كانت جميع الاختبارات صحيحة، ينفذ MultiOp العملية t op (انظر البند 2 أدناه)، وإلا ينفذ العملية f op (انظر البند 3 أدناه). 2. قائمة عمليات قاعدة بيانات تسمى t op. كل عملية في القائمة هي إما عملية إدراج أو حذف أو بحث، وتنطبق على مدخل واحد في قاعدة البيانات. قد تنطبق عمليتان مختلفتان في القائمة على المدخل نفسه أو مداخل مختلفة في قاعدة البيانات. تُنفَّذ هذه العمليات إذا كانت نتيجة تقييم guard هي true. 3. قائمة عمليات قاعدة بيانات تسمى f op. مثل t op، لكنها تُنفَّذ إذا كانت نتيجة تقييم guard هي false.

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare هي قائمة من المسندات تمثل اقترانًا منطقيًا للعبارات. إذا نجحت المقارنات، فستُعالَج طلبات النجاح بالترتيب، وستحتوي الاستجابة على الاستجابات الخاصة بها بالترتيب. وإذا فشلت المقارنات، فستُعالَج طلبات الفشل بالترتيب، وستحتوي الاستجابة على الاستجابات الخاصة بها بالترتيب. | (slice of) Compare |
| success | success هي قائمة بالطلبات التي ستُطبَّق عندما تكون نتيجة تقييم compare هي true. | (slice of) RequestOp |
| failure | failure هي قائمة بالطلبات التي ستُطبَّق عندما تكون نتيجة تقييم compare هي false. | (slice of) RequestOp |

##### message `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | تُضبط succeeded على true إذا كانت نتيجة تقييم compare هي true، وإلا فعلى false. | bool |
| responses | responses هي قائمة بالاستجابات المقابلة للنتائج من تطبيق success إذا كانت succeeded تساوي true، أو failure إذا كانت succeeded تساوي false. | (slice of) ResponseOp |

##### message `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id هو معرّف المراقب المطلوب إلغاؤه بحيث لا تُنقل أحداث أخرى. | int64 |

##### message `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key هو المفتاح المراد تسجيله للمراقبة. | bytes |
| range_end | range_end هي نهاية النطاق [key, range_end) المراد مراقبته. إذا لم يُعطَ range_end، فسيُراقَب وسيط المفتاح فقط. إذا كان range_end يساوي '\0'، فستُراقَب جميع المفاتيح الأكبر من وسيط المفتاح أو المساوية له. إذا كان range_end هو المفتاح المعطى زائد واحد، فستُراقَب جميع المفاتيح ذات البادئة (المفتاح المعطى). | bytes |
| start_revision | start_revision هي مراجعة اختيارية للبدء بالمراقبة منها (شاملة). عدم وجود start_revision يعني "الآن". | int64 |
| progress_notify | يُضبط progress_notify بحيث يرسل خادم etcd دوريًا WatchResponse بلا أحداث إلى المراقب الجديد إذا لم تكن هناك أحداث حديثة. وهو مفيد عندما يرغب العملاء في استعادة مراقب منقطع بدءًا من مراجعة معروفة حديثة. قد يقرر خادم etcd وتيرة إرساله للإشعارات بناءً على الحمل الحالي. | bool |
| filters | filters ترشّح الأحداث في جانب الخادم قبل إرسالها مرة أخرى إلى المراقب. | (slice of) FilterType |
| prev_kv | إذا ضُبط prev_kv، فسيحصل المراقب المُنشأ على زوج المفتاح/القيمة السابق قبل حدوث الحدث. إذا كان زوج المفتاح/القيمة السابق قد ضُغط بالفعل، فلن يُرجَع شيء. | bool |
| watch_id | إذا قُدّم watch_id وكان غير صفري، فسيُعيَّن لهذا المراقب. وبما أن إنشاء مراقب في etcd ليس عملية متزامنة، يمكن استخدام هذا لضمان صحة الترتيب عند إنشاء عدة مراقبين على التدفق نفسه. سيؤدي إنشاء مراقب بمعرّف قيد الاستخدام بالفعل على التدفق إلى إرجاع خطأ. | int64 |
| fragment | fragment يفعّل تقسيم المراجعات الكبيرة إلى استجابات مراقبة متعددة. | bool |

##### message `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

يطلب إرسال حالة تقدم تدفق المراقبة في تدفق استجابة المراقبة في أقرب وقت ممكن.

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union هو طلب إما لإنشاء مراقب جديد أو إلغاء مراقب موجود. | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### message `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id هو معرّف المراقب الذي تتطابق معه الاستجابة. | int64 |
| created | تُضبط created على true إذا كانت الاستجابة لطلب إنشاء مراقب. ينبغي على العميل تسجيل watch_id وتوقع استلام أحداث المراقب المُنشأ من التدفق نفسه. ستُرفق جميع الأحداث المرسلة إلى المراقب المُنشأ بـwatch_id نفسه. | bool |
| canceled | تُضبط canceled على true إذا كانت الاستجابة لطلب إلغاء مراقب أو إذا كانت start_revision قد ضُغطت بالفعل. لن تُرسل أحداث أخرى إلى المراقب الملغى. | bool |
| compact_revision | تُضبط compact_revision على الفهرس الأدنى إذا حاول مراقب المراقبة عند فهرس مضغوط.  يحدث هذا عند إنشاء مراقب عند مراجعة مضغوطة أو عندما لا يستطيع المراقب مواكبة تقدم مخزن المفاتيح/القيم.  ينبغي على العميل التعامل مع المراقب بوصفه ملغى وألا يحاول إنشاء أي مراقب بنفس start_revision مرة أخرى. | int64 |
| cancel_reason | cancel_reason يشير إلى سبب إلغاء المراقب. | string |
| fragment | fragment تساوي true إذا قُسّمت استجابة مراقبة كبيرة على استجابات متعددة. | bool |
| events |  | (slice of) mvccpb.Event |

##### message `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| type | type هو نوع الحدث. إذا كان type هو PUT، فذلك يشير إلى أن بيانات جديدة خُزنت في المفتاح. إذا كان type هو DELETE، فذلك يشير إلى أن المفتاح حُذف. | EventType |
| kv | kv يحمل KeyValue للحدث. يحتوي حدث PUT على زوج kv الحالي. يشير حدث PUT مع kv.Version=1 إلى إنشاء مفتاح. يحتوي حدث DELETE/EXPIRE على المفتاح المحذوف مع ضبط مراجعة تعديله على مراجعة الحذف. | KeyValue |
| prev_kv | prev_kv يحمل زوج المفتاح/القيمة قبل حدوث الحدث. | KeyValue |

##### message `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| key | key هو المفتاح بالبايتات. لا يُسمح بمفتاح فارغ. | bytes |
| create_revision | create_revision هي مراجعة آخر إنشاء لهذا المفتاح. | int64 |
| mod_revision | mod_revision هي مراجعة آخر تعديل لهذا المفتاح. | int64 |
| version | version هي إصدار المفتاح. يعيد الحذف الإصدار إلى الصفر وأي تعديل للمفتاح يزيد إصداره. | int64 |
| value | value هي القيمة التي يحملها المفتاح، بالبايتات. | bytes |
| lease | lease هو معرّف عقد الإيجار المرفق بالمفتاح. عندما تنتهي صلاحية عقد الإيجار المرفق، سيُحذف المفتاح. إذا كان lease يساوي 0، فلا يوجد عقد إيجار مرفق بالمفتاح. | int64 |

##### message `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### message `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### message `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### message `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Permission هو كيان واحد

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### message `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Role هو مدخل واحد في الحاوية authRoles

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (slice of) Permission |

##### message `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

User هو مدخل واحد في الحاوية authUsers

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (slice of) string |
| options |  | UserAddOptions |

##### message `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| no_password |  | bool |
