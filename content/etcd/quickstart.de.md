---
title: Schnellstart
weight: 900
description: "etcd in weniger als 5 Minuten einsatzbereit machen!"
icon: fa-solid fa-rocket
categories: [Tutorial]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
---

Befolgen Sie diese Anweisungen, um einen lokalen Ein-Mitglied-Cluster mit etcd zu installieren, zu starten und zu testen:

1. Installieren Sie etcd aus vorkompilierten Binärdateien oder aus dem Quellcode. Weitere Einzelheiten finden Sie in der [Installationsanleitung][Install].

    > [!WARNING]
    > **Wichtig**: Führen Sie unbedingt den letzten Schritt der Installationsanleitung aus, um zu prüfen, ob `etcd` über Ihren Suchpfad aufrufbar ist.

2. Starten Sie `etcd`:

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **Hinweis**: Die Ausgabe von `etcd` besteht aus
    > [Protokollen](/de/etcd/op-guide/configuration/#logging) &mdash; Protokolle auf Info-Ebene können ignoriert werden.

3. Verwenden Sie in einem **anderen Terminal** `etcdctl`, um einen Schlüssel festzulegen:

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

4. Rufen Sie den Schlüssel aus demselben Terminal ab:

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## Was kommt als Nächstes? {#whats-next}

Erfahren Sie auf den folgenden Seiten mehr über weitere Möglichkeiten zur Konfiguration und Nutzung von etcd:

- Wenn Sie Entwickler sind:
  - Erkunden Sie die gRPC-[API][].
  - Informieren Sie sich über [Sprachanbindungen und Werkzeuge][integrations].

- Wenn Sie Betreiber oder Administrator sind:
  - Richten Sie einen [Cluster mit mehreren Rechnern][clustering] ein.
  - Erfahren Sie, wie Sie etcd [konfigurieren][configure].
  - Verwenden Sie TLS, um einen [etcd-Cluster abzusichern][security].
  - [Optimieren Sie etcd][tuning].

[api]: /de/etcd/learning/api
[clustering]: /de/etcd/op-guide/clustering
[configure]: /de/etcd/op-guide/configuration
[integrations]: /de/etcd/integrations
[security]: /de/etcd/op-guide/security
[tuning]: /de/etcd/tuning
[Install]: /de/etcd/install/
