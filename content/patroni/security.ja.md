---
title: "セキュリティに関する考慮事項"
weight: 160
icon: fa-solid fa-lock
description: "DCS、REST API、および資格情報の取り扱いに関するセキュリティ上の考慮事項。"
module: [PATRONI]
categories: [概念]
aliases: [/docs/patroni/security/]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Patroni クラスターには、不正アクセスから保護すべき2つのインターフェースがあります。1つは分散型構成ストレージ（DCS）、もう1つは Patroni REST API です。

--------

## DCS の保護 {#protecting-dcs}

Patroni と [patronictl](/ja/patroni/patronictl#patronictl) は、DCS に対してデータの格納および取得を行います。

DCS には機密情報は含まれていませんが、Patroni/PostgreSQL の設定の一部を変更できるため、最初に保護すべきは DCS 自体です。

保護の詳細は使用する DCS の種類によって異なります。サポートされている DCS の種類における認証および暗号化パラメータ (tokens/basic-auth/client 証明書) は、[settings](/ja/patroni/config/yaml#yaml) で説明されています。

一般的な推奨事項として、すべての DCS 通信で TLS を有効にする必要があります。

--------

## REST API の保護 {#protecting-the-rest-api}

REST API の保護はより複雑な作業です。

Patroni の REST API は、リーダー競合中に Patroni 自身が使用し、[patronictl](/ja/patroni/patronictl#patronictl) が failovers/switchovers/reinitialize/restarts/reloads を実行するために使用し、HAProxy またはその他のロードバランサが HTTP ヘルスチェックを実行するために使用され、もちろんモニタリングにも利用できます。

セキュリティの観点から、REST API には安全な（`GET` リクエスト、情報の取得のみ）と安全でない（`PUT`、`POST`、`PATCH` および `DELETE` リクエスト、ノードの状態の変更）エンドポイントが含まれます。

非安全エンドポイントは、`restapi.authentication.username` および `restapi.authentication.password` パラメータを設定することで HTTP basic-auth で保護できます。安全エンドポイントを TLS を有効化せずに保護する方法はありません。

REST API 用の TLS を有効にし、PKI を構成した場合、すべてのエンドポイントで API サーバーと API クライアントの相互認証が可能になります。

`restapi` セクションのパラメータにより、サーバーへの TLS クライアント認証が可能になります。`verify_client` パラメータの値に応じて、API サーバーは安全な API 呼び出しと安全でない API 呼び出しの両方 (`verify_client: required`)、または安全でない API 呼び出しのみ (`verify_client: optional`)、あるいは API 呼び出しのいずれにも認証を要求しません (`verify_client: none`)。

`ctl` セクションのパラメータにより、TLS サーバー認証がクライアント（[patronictl](/ja/patroni/patronictl#patronictl)）に対して有効になります。このツールは Patroni と同じ設定を使用します。`insecure: true` を設定することで、クライアントによるサーバー証明書の検証を無効化できます。TLS クライアントパラメータの詳細については、[settings](/ja/patroni/config/yaml#patronictl_settings) を参照してください。

PostgreSQL データベース本体に対する不正アクセスからの保護は、本ドキュメントの範囲外であり、<https://www.postgresql.org/docs/current/client-authentication.html> で説明されています。
