---
title: Quickstart
weight: 900
description: Get etcd up and running in less than 5 minutes!
icon: fa-solid fa-rocket
categories: [Tutorial]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/quickstart.md"
---

Follow these instructions to locally install, run, and test a single-member
cluster of etcd:

 1. Install etcd from pre-built binaries or from source. For details, see
    [Install][].

    > [!WARNING]
    > **Important**: Ensure that you perform the last
    > step of the installation instructions to verify that `etcd` is in your path.

 2. Launch `etcd`:

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **Note**: The output produced by `etcd` are
    > [logs](/etcd/op-guide/configuration/#logging) &mdash; info-level logs can
    > be ignored.

 3. From **another terminal**, use `etcdctl` to set a key:

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. From the same terminal, retrieve the key:

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## What's next?

Learn about more ways to configure and use etcd from the following pages:

- If you are a developer:
  - Explore the gRPC [API][].
  - Find [language bindings and tools][integrations].

- If you are an operator or admin:
  - Set up a [multi-machine cluster][clustering].
  - Learn how to [configure][] etcd.
  - Use TLS to [secure an etcd cluster][security].
  - [Tune etcd][tuning].

[api]: /etcd/learning/api
[clustering]: /etcd/op-guide/clustering
[configure]: /etcd/op-guide/configuration
[integrations]: /etcd/integrations
[security]: /etcd/op-guide/security
[tuning]: /etcd/tuning
[Install]: /etcd/install/
