---
title: تسمية gRPC واكتشافه
weight: 3500
description: "go-grpc: لتحليل نقاط نهاية gRPC بواجهة خلفية من etcd"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/grpc_naming.md"
---

يوفر etcd محلل أسماء (resolver) لـgRPC يدعم نظام أسماء بديلًا يجلب نقاط النهاية من etcd لاكتشاف خدمات gRPC. تعتمد الآلية الكامنة على مراقبة التحديثات على المفاتيح التي تحمل اسم الخدمة كبادئة.

لاحظ أن هذه الميزة تجريبية لأنها تعتمد على حزمة [google.golang.org/grpc/resolver][]، التي لا تزال تجريبية في grpc-go.

## استخدام اكتشاف etcd مع go-grpc {#using-etcd-discovery-with-go-grpc}

يوفر عميل etcd محلل أسماء لـgRPC لتحليل نقاط نهاية gRPC بواجهة خلفية من etcd. يُهيَّأ المحلل بعميل etcd:

```go
import (
	clientv3 "go.etcd.io/etcd/client/v3"
	etcdnaming "go.etcd.io/etcd/client/v3/naming/resolver"

	"google.golang.org/grpc"
)

...

cli, err := clientv3.NewFromURL("http://localhost:2379")
if err != nil {
    // ...
}
r, err := etcdnaming.NewBuilder(cli)
if err != nil {
    // ...
}
conn, gerr := grpc.NewClient("my-service", grpc.WithResolvers(r), ...)
```

## إدارة نقاط نهاية الخدمة {#managing-service-endpoints}

يتعامل محلل etcd مع جميع المفاتيح الواقعة تحت بادئة هدف التحليل بعد "/" (مثل "foo/bar/my-service/")
ذات القيم المشفرة بصيغة JSON (تاريخيًا `naming.Update` في go-grpc) بوصفها نقاط نهاية خدمات محتملة.
تُضاف نقاط النهاية إلى الخدمة بإنشاء مفاتيح جديدة، وتُزال من الخدمة بحذف مفاتيح.

### إضافة نقطة نهاية {#adding-an-endpoint}

يمكن إضافة نقاط نهاية جديدة إلى الخدمة من خلال `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

يمكن لطريقة `endpoints.Manager` في عميل etcd أيضًا تسجيل نقاط نهاية جديدة بمفتاح يطابق `Addr`:

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
لتمكين موازنة الحمل بالتناوب (round-robin) عند الاتصال بخدمة ذات نقاط نهاية متعددة، يمكنك إعداد اتصالك
 بموازن الحمل الداخلي بالتناوب في grpc:

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### حذف نقطة نهاية {#deleting-an-endpoint}

يمكن حذف المضيفين من الخدمة من خلال `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

تدعم طريقة `endpoints.Manager` في عميل etcd أيضًا حذف نقاط النهاية:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### تسجيل نقطة نهاية مع عقد إيجار (lease) {#registering-an-endpoint-with-a-lease}

يضمن تسجيل نقطة نهاية مع عقد إيجار (lease) أنه إذا لم يستطع المضيف الحفاظ على نبضة قلب للحفاظ على الحياة (keepalive heartbeat) (مثلًا عند فشل جهازه)، فستتم إزالته من الخدمة:

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
بلغة Go:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### التحديث الذري لنقاط النهاية {#atomically-updating-endpoints}

إذا رُغب في تعديل نقاط نهاية متعددة في معاملة واحدة، يمكن استخدام `endpoints.Manager` مباشرة:

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
