---
title: "セキュリティに関する考慮事項"
weight: 160
icon: fa-solid fa-lock
description: "DCS、REST API、および資格情報の取り扱いに関するセキュリティ上の考慮事項。"
module: [PATRONI]
categories: [概念]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
Patroniクラスターには、不正アクセスから保護すべき2つのインターフェースがあります。1つは分散型構成ストレージ（DCS）、もう1つはPatroni REST APIです。

--------

## DCSの保護 {#protecting-dcs}

Patroniと[patronictl](/ja/patroni/patronictl#patronictl)は、DCSに対してデータの格納および取得を行います。

DCSに機密情報が含まれていない場合でも、Patroni/PostgreSQLの構成の一部を変更できるため、最初に保護すべきはDCS自体です。

保護の詳細は使用するDCSの種類によって異なります。サポートされているDCSの種類における認証および暗号化パラメータ（トークン／基本認証／クライアント証明書）は、[設定](/ja/patroni/config/yaml#yaml)で説明されています。

一般的な推奨は、すべてのDCS通信でTLSを有効にすることです。

--------

## REST APIの保護 {#protecting-the-rest-api}

REST APIの保護はより複雑な作業です。

PatroniのREST APIは、リーダー選出の実行中にPatroni自身が使用し、[patronictl](/ja/patroni/patronictl#patronictl)がフェイルオーバー／スイッチオーバー／再初期化／再起動／リロードを実行するために使用し、HAProxyまたはその他のロードバランサーがHTTPヘルスチェックを実行するために使用され、もちろんモニタリングにも利用できます。

セキュリティの観点から、REST APIには安全な（`GET`リクエスト、情報の取得のみ）と安全でない（`PUT`、`POST`、`PATCH`および`DELETE`リクエスト、ノードの状態の変更）エンドポイントが含まれます。

安全でないエンドポイントは、`restapi.authentication.username`および`restapi.authentication.password`パラメータを設定することでHTTP basic-authで保護できます。安全なエンドポイントをTLSを有効化せずに保護する方法はありません。

REST API用のTLSを有効にし、PKIを構築した場合、すべてのエンドポイントでAPIサーバーとAPIクライアントの相互認証が可能になります。

`restapi`セクションのパラメータにより、サーバーへのTLSクライアント認証が可能になります。`verify_client`パラメータの値に応じて、APIサーバーがクライアント証明書の検証成功を要求する対象は、安全なAPI呼び出しと安全でないAPI呼び出しの両方（`verify_client: required`）、安全でないAPI呼び出しのみ（`verify_client: optional`）、あるいはどのAPI呼び出しでもない（`verify_client: none`）のいずれかです。

`ctl`セクションのパラメータにより、クライアント（Patroniと同じ構成を使用する[patronictl](/ja/patroni/patronictl#patronictl)）がTLSサーバーを認証できます。`insecure: true`を設定することで、クライアントによるサーバー証明書の検証を無効化できます。TLSクライアントパラメータの詳細については、[設定](/ja/patroni/config/yaml#patronictl_settings)を参照してください。

PostgreSQLデータベース本体に対する不正アクセスからの保護は、本ドキュメントの範囲外であり、<https://www.postgresql.org/docs/current/client-authentication.html>で説明されています。
