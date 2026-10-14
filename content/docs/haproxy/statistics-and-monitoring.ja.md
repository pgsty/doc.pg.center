---
title: "9. 統計情報とモニタリング"
linkTitle: "9. 統計情報とモニタリング"
weight: 330
description: "CSV形式および型付き統計情報、ランタイム CLI コマンド、マスター CLI、統計ファイル"
icon: fa-solid fa-chart-line
module: [HAPROXY]
categories: [タスク]
aliases:
  - /haproxy/management/statistics-and-monitoring/
  - /docs/haproxy/management/statistics-and-monitoring/
  - /haproxy/statistics-and-monitoring/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---



HAProxyに状態を問い合わせられます。最も一般的な方法はHTTP統計ページです。このページは、監視ツール向けにCSV出力形式も提供します。Unixソケットでも、同じ形式を利用できます。

統計情報は、HAProxy の複数のコンポーネントに対応するドメインと呼ばれるカテゴリに分類されます。利用可能なドメインは 2 つあります：proxy と resolvers。指定がなければ proxy ドメインが選択されます。なお、HTTP ページには proxy の統計情報のみが表示されます。

## 9.1. CSV 形式 {#section-9-1}


統計情報は Unix ソケットまたは HTTP ページから参照できます。両方の方法とも、次のフィールドを持つ CSV 形式を提供します。最初の行はシャープ ('#') で始まり、コンマ区切りの各フィールドごとに 1 つの単語が含まれ、それが列の見出しを表します。2 行目以降は、コンマを区切り文字として使用する通常の CSV 形式であり、テキストの曖昧さがある場合（クォートやコンマを含む場合）にのみダブルクォート（'"'）をオプションのテキスト区切り文字として使用します。テキスト内のダブルクォート文字（'"'）は二重に（'""'）エスケープされ、これはほとんどのツールが認識する形式です。列の先頭に追加の列を挿入しないでください。そうしないと、列位置をハードコードして処理しているツールが破損する可能性があります。

proxy 統計情報の場合、各フィールド名の後に、そのフィールドに値を持つ可能性があるタイプが括弧内に指定されます。タイプは L（リスナー）、F（フロントエンド）、B（バックエンド）、S（サーバ）です。静的フィールドは固定されたセットであり、常に同じ順序で利用可能です。文字 '-' を含む列は静的フィールドの終了を示し、その後のフィールドの存在や順序は保証されません。

以下は proxy 統計情報ドメインにおける静的フィールドの一覧です：

```text
 0. pxname [LFBS]: プロキシ名
 1. svname [LFBS]: サービス名（フロントエンドはFRONTEND、バックエンドはBACKEND、
    サーバー/リスナーは任意の名前）
 2. qcur [..BS]: 現在キューにあるリクエスト数。バックエンドでは、
    サーバーが割り当てられずにキューで待機している数を示します。
 3. qmax [..BS]: qcurの最大値
 4. scur [LFBS]: 現在のセッション数
 5. smax [LFBS]: 最大セッション数
 6. slim [LFBS]: 設定されたセッション数の上限
 7. stot [LFBS]: 累積セッション数
 8. bin [LFBS]: 入力バイト数
 9. bout [LFBS]: 出力バイト数
10. dreq [LFB.]: セキュリティ上の理由で拒否したリクエスト数。
    - tcpでは、tcp-request contentルールへの一致によるものです。
    - httpでは、http-requestまたはtarpitルールへの一致によるものです。
11. dresp [LFBS]: セキュリティ上の理由で拒否したレスポンス数。
    - httpでは、http-requestルールへの一致、または
      "option checkcache"によるものです。
12. ereq [LF..]: リクエストエラー。考えられる原因には次のものがあります。
    - リクエスト送信前にクライアントが早期終了した。
    - クライアントからの読み取りエラー。
    - クライアントのタイムアウト。
    - クライアントが接続を閉じた。
    - クライアントからの各種不正リクエスト。
    - リクエストにtarpitが適用された。
13. econ [..BS]: バックエンドサーバーへの接続試行中にエラーが起きたリクエスト数。
    バックエンドの統計は、そのバックエンドの全サーバーの統計の合計に、
    特定のサーバーに関連しない接続エラーを加えたものです
    （稼働中のサーバーがバックエンドにない場合など）。
14. eresp [..BS]: レスポンスエラー。srv_abrtもここに計上されます。
    そのほかのエラーには、次のものがあります。
    - クライアントソケットへの書き込みエラー（サーバーの統計には計上しません）。
    - レスポンスへのフィルター適用の失敗。
15. wretr [..BS]: サーバーへの接続を再試行した回数。
16. wredis [..BS]: リクエストを別のサーバーへ再配分した回数。
    サーバーの値は、そのサーバーから別のサーバーへ切り替えた回数です。
17. status [LFBS]: 状態（UP/DOWN/NOLB/MAINT/MAINT(via)/MAINT(resolution)...）
18. weight [..BS]: 有効な重みの合計（バックエンド）、有効な重み（サーバー）
19. act [..BS]: 稼働系サーバーの数（バックエンド）、稼働系サーバーかどうか（サーバー）
20. bck [..BS]: バックアップサーバーの数（バックエンド）、バックアップかどうか（サーバー）
21. chkfail [...S]: 失敗したチェックの数（サーバーが稼働中に失敗したチェックだけを数えます）。
22. chkdown [..BS]: UP->DOWNへの遷移回数。バックエンドのカウンターは、
    各サーバーのカウンターの合計ではなく、バックエンド全体が停止した回数です。
23. lastchg [..BS]: 最後のUP<->DOWN遷移からの秒数
24. downtime [..BS]: 合計停止時間（秒）。バックエンドの値は、
    サーバー停止時間の合計ではなく、バックエンド全体の停止時間です。
25. qlimit [...S]: サーバーに設定されたmaxqueue。値が0の場合は空です
    （デフォルトで、制限なしを意味します）。
26. pid [LFBS]: プロセスID（最初のインスタンスは0、二番目は1、...）
27. iid [LFBS]: 一意のプロキシID
28. sid [L..S]: サーバーID（プロキシ内で一意）
29. throttle [...S]: slowstartが有効な場合、サーバーに対する現在の抑制率（%）。
    slowstart中でなければ値はありません。
30. lbtot [..BS]: 新規セッションまたは再配分の際に、サーバーを選択した合計回数。
    サーバーのカウンターは、そのサーバーが選択された回数です。
31. tracked [...S]: 追跡が有効な場合、プロキシ/サーバーのID。
32. type [LFBS]: （0=フロントエンド、1=バックエンド、2=サーバー、3=ソケット/リスナー）
33. rate [.FBS]: 直近一秒間の、秒あたりのセッション数
34. rate_lim [.F..]: 設定された、新規セッション数の秒あたりの上限
35. rate_max [.FBS]: 秒あたりの新規セッション数の最大値
36. check_status [...S]: 最後のヘルスチェックの状態。次のいずれかです。
       UNK     -> 不明
       INI     -> 初期化中
       SOCKERR -> ソケットエラー
       L4OK    -> レイヤー4のチェックに成功。上位レイヤーのテストは無効。
       L4TOUT  -> レイヤー1-4のタイムアウト
       L4CON   -> レイヤー1-4の接続問題。たとえば、
                  "Connection refused"（tcp rst）や"No route to host"（icmp）。
       L6OK    -> レイヤー6のチェックに成功
       L6TOUT  -> レイヤー6（SSL）のタイムアウト
       L6RSP   -> レイヤー6の不正なレスポンス。プロトコルエラー。
       L7OK    -> レイヤー7のチェックに成功
       L7OKC   -> レイヤー7のチェックに条件付きで成功。たとえば、
                  disable-on-404を使っている場合の404。
       L7TOUT  -> レイヤー7（HTTP/SMTP）のタイムアウト
       L7RSP   -> レイヤー7の不正なレスポンス。プロトコルエラー。
       L7STS   -> レイヤー7のレスポンスエラー。たとえばHTTP 5xx。
    注意：チェックが実行中の場合、最後に判明した状態に"* "の接頭辞を付けて
    報告します。例："* L7OK"。
37. check_code [...S]: 取得できる場合、レイヤー5-7のコード
38. check_duration [...S]: 最後のヘルスチェックの完了に要した時間（ms）
39. hrsp_1xx [.FBS]: 1xxコードのhttpレスポンス数
40. hrsp_2xx [.FBS]: 2xxコードのhttpレスポンス数
41. hrsp_3xx [.FBS]: 3xxコードのhttpレスポンス数
42. hrsp_4xx [.FBS]: 4xxコードのhttpレスポンス数
43. hrsp_5xx [.FBS]: 5xxコードのhttpレスポンス数
44. hrsp_other [.FBS]: その他のコードのhttpレスポンス数（プロトコルエラー）
45. hanafail [...S]: 失敗したヘルスチェックの詳細
46. req_rate [.F..]: 直近一秒間の、秒あたりのHTTPリクエスト数
47. req_rate_max [.F..]: 観測された、秒あたりのHTTPリクエスト数の最大値
48. req_tot [.FB.]: 受信したHTTPリクエストの総数
49. cli_abrt [..BS]: クライアントによって中断されたデータ転送の数
50. srv_abrt [..BS]: サーバーによって中断されたデータ転送の数（erespにも計上）
51. comp_in [.FB.]: 圧縮器へ渡されたHTTPレスポンスのバイト数
52. comp_out [.FB.]: 圧縮器から出力されたHTTPレスポンスのバイト数
53. comp_byp [.FB.]: HTTP圧縮器を迂回したバイト数（CPU/BWの上限によるもの）
54. comp_rsp [.FB.]: 圧縮されたHTTPレスポンス数
55. lastsess [..BS]: 最後にサーバー/バックエンドへセッションを割り当ててからの秒数
56. last_chk [...S]: 最後のヘルスチェックの内容、またはテキスト形式のエラー
57. last_agt [...S]: 最後のエージェントチェックの内容、またはテキスト形式のエラー
58. qtime [..BS]: 直近1024リクエストの平均キュー待機時間（ms）
59. ctime [..BS]: 直近1024リクエストの平均接続時間（ms）
60. rtime [..BS]: 直近1024リクエストの平均レスポンス時間（ms、TCPでは0）
61. ttime [..BS]: 直近1024リクエストの平均合計セッション時間（ms）
62. agent_status [...S]: 最後のエージェントチェックの状態。次のいずれかです。
       UNK     -> 不明
       INI     -> 初期化中
       SOCKERR -> ソケットエラー
       L4OK    -> レイヤー4のチェックに成功。上位レイヤーのテストは無効。
       L4TOUT  -> レイヤー1-4のタイムアウト
       L4CON   -> レイヤー1-4の接続問題。たとえば、
                  "Connection refused"（tcp rst）や"No route to host"（icmp）。
       L7OK    -> エージェントが"up"を報告
       L7STS   -> エージェントが"fail"、"stop"、または"down"を報告
63. agent_code [...S]: エージェントが報告した数値コードがあれば、その値（現在は未使用）
64. agent_duration [...S]: 最後のチェックの完了に要した時間（ms）
65. check_desc [...S]: check_statusの短い、人が読める説明
66. agent_desc [...S]: agent_statusの短い、人が読める説明
67. check_rise [...S]: チェックが使う、サーバーの"rise"パラメーター
68. check_fall [...S]: チェックが使う、サーバーの"fall"パラメーター
69. check_health [...S]: 0からrise+fall-1までの、サーバーのヘルスチェック値
70. agent_rise [...S]: エージェントの"rise"パラメーター。通常は1。
71. agent_fall [...S]: エージェントの"fall"パラメーター。通常は1。
72. agent_health [...S]: エージェントの健全性パラメーター。0からrise+fall-1まで。
73. addr [L..S]: address:portまたは"unix"。IPv6アドレスは角括弧で囲まれます。
74: cookie [..BS]: サーバーのCookie値、またはバックエンドのCookie名
75: mode [LFBS]: プロキシモード（tcp、http、health、unknown）
76: algo [..B.]: 負荷分散アルゴリズム
77: conn_rate [.F..]: 直近一秒間の接続数
78: conn_rate_max [.F..]: これまでのconn_rateの最大値
79: conn_tot [.F..]: 累積接続数
80: intercepted [.FB.]: 捕捉したリクエストの累積数（monitor、stats）
81: dcon [LF..]: "tcp-request connection"ルールが拒否したリクエスト数
82: dses [LF..]: "tcp-request session"ルールが拒否したリクエスト数
83: wrew [LFBS]: ヘッダー書き換え失敗の警告の累積数
84: connect [..BS]: 接続確立の試行の累積数
85: reuse [..BS]: 接続再利用の累積数
86: cache_lookups [.FB.]: キャッシュ検索の累積数
87: cache_hits [.FB.]: キャッシュヒットの累積数
88: srv_icur [...S]: 再利用できるアイドル接続の現在の数
89: src_ilim [...S]: 利用可能なアイドル接続数の上限
90. qtime_max [..BS]: 観測されたキュー待機時間の最大値（ms）
91. ctime_max [..BS]: 観測された接続時間の最大値（ms）
92. rtime_max [..BS]: 観測されたレスポンス時間の最大値（ms、TCPでは0）
93. ttime_max [..BS]: 観測された合計セッション時間の最大値（ms）
94. eint [LFBS]: 内部エラーの累積数
95. idle_conn_cur [...S]: 安全でないアイドル接続の現在の数
96. safe_conn_cur [...S]: 安全なアイドル接続の現在の数
97. used_conn_cur [...S]: 使用中の接続の現在の数
98. need_conn_est [...S]: 必要と推定される接続数
99. uweight [..BS]: ユーザー指定の重みの合計（バックエンド）、ユーザー指定の重み（サーバー）
100. agg_server_status [..B.]: サーバーの状態をバックエンドで集約したゲージ
101. agg_server_status_check [..B.]: （非推奨）
102. agg_check_status [..B.]: サーバーの状態チェックの結果をバックエンドで集約したゲージ
103. srid [...S]: サーバーIDのリビジョン
104. sess_other [.F..]: プロセス起動後の、HTTP以外のセッション総数
105. h1_sess [.F..]: プロセス起動後のHTTP/1セッション総数
106. h2_sess [.F..]: プロセス起動後のHTTP/2セッション総数
107. h3_sess [.F..]: プロセス起動後のHTTP/3セッション総数
108. req_other [.F..]: ワーカープロセス起動後に、このオブジェクトが処理したHTTP以外のセッション総数
109. h1req [.F..]: ワーカープロセス起動後に、このオブジェクトが処理したHTTP/1セッション総数
110. h2req [.F..]: ワーカープロセス起動後に、このオブジェクトが処理したhTTP/2セッション総数
111. h3req [.F..]: ワーカープロセス起動後に、このオブジェクトが処理したHTTP/3セッション総数
112. proto [L...]: プロトコル
113. priv_idle_cur [...S]: 専用アイドル接続の現在の数
114. reqbin [LFBS]: ワーカープロセス起動後に受信したリクエストの合計バイト数
115. reqbout [LFBS]: ワーカープロセス起動後に送信したリクエストの合計バイト数
116. resbin [LFBS]: ワーカープロセス起動後に受信したレスポンスの合計バイト数
117. resbout [LFBS]: ワーカープロセス起動後に送信したレスポンスの合計バイト数
```


他のすべての統計情報ドメインについては、フィールドの存在や順序は保証されません。この場合、常にヘッダー行を使用して CSV データを解析してください。

## 9.2. 型付き出力形式 {#section-9-2}


"show info"と"show stat"は、各出力値に型と、プロセス間でどのように集計するべきか、値がどう変化するかを知るための十分な情報を添えるモードをサポートします。

すべての場合において、出力は 1 行あたり 1 つの値で構成され、すべての情報がコロン（':'）で区切られたフィールドに分割されます。

1 番目の列はダンプ対象のオブジェクトまたはメトリクスを示します。その形式は、この出力を生成するコマンドに固有であり、本節では説明しません。通常、識別子とフィールド名の連続で構成されます。

2 番目の列には 4 文字が含まれ、それぞれが報告されている値の起源、性質、スコープ、および永続状態を示します。1 番目の文字（起源）は、値がどこから抽出されたかを示します。可能な文字は：

```text
M   値はメトリクスです。ある一時点で有効であり、その性質によって変化することがあります。

S   値は状態です。離散値を表し、定義上、集約できません。
    サーバーの状態（"UP"や"DOWN"）、プロセスのPIDなどが該当します。

K   値はソート用のキーです。同じ分類内で一意であるため、複数の値を
    グループ化するために使える識別子を表します。内部識別子はすべてキーです。
    名前も、一意であればキーとして扱えます（フロントエンド名など）。
    一部は自動的に割り当てられる場合がありますが、一般にキーは設定に由来します。
    ほとんどの用途で、キーは設定と同等と見なせます。

C   値は設定に由来します。同時接続数の上限やCookie名など、出力に含める
    意義のある設定値があります。定義上、同じ設定ファイルから起動した
    すべてのプロセスで、これらの値は同じです。

P   値は製品自体に由来します。この種の値は少なく、最も一般的な用途は
    製品名、バージョン、リリース日の報告です。
    これらも、すべてのプロセスで同じです。
```


2 番目の文字（性質）は、フィールドが伝える情報の性質を示し、集計ツールが複数の値をどのように集計するかを判断するためのものです。可能な文字は：

```text
A   値は、最後のイベントからの経過時間を表します。現在時刻に基づいて
    自動計算する点で、所要時間とは少し異なります。典型例は、サーバーで
    最後のセッションが発生してからの時間です。経過時間の集約には通常、
    最小値を使い、値を保存しておく必要はありません。

a   値は、すでに平均された値です。平均レスポンス時間やサーバーの重みが
    この種類に該当します。平均値は通常、プロセス間でも平均できます。

C   値は累積カウンターを表します。この種の値は、桁あふれで一巡するまで
    増え続けます。一部の監視プロトコルでは、異なる型として報告するために
    カウンターとゲージを区別する必要があります。一般に、カウンターはイベント数や
    量を表すため、単純に合算できます。接続数やバイト数が、この種類の例です。

D   値は、ある状態の持続時間を表します。用途はいくつかあり、多くは最後の
    ヘルスチェックに要した時間や、サーバーが停止していた時間です。
    通常、持続時間は合算せず、多くの場合、SLAの計算には最大値を使います。

G   値はゲージを表し、ある一時点の測定値です。メモリ使用量や現在の
    アクティブ接続数が該当します。この種類のメトリクスは、通常、集約時に合算します。

L   値は上限（通常は設定されたもの）を表します。上限は取得箇所に固有であるため、
    その性質上、集約が難しくなります。状況によっては合算したり、
    別々のまま保持したりできます。

M   値は最大値を表します。一般にはゲージに適用され、これまでの最大値を保持します。
    例として、製品の稼働期間中に観測した同時接続数の最大値があります。
    複数の最大値を正しく集約するには、すべての最大値のうちの最大値から、
    すべての最大値の合計までを範囲として出力するべきです。
    それぞれが同時に発生したかどうかを知る方法はないためです。

m   値は最小値を表します。一般にはゲージに適用され、これまでの最小値を保持します。
    例として、製品の稼働期間中に観測した空きメモリプールの最小量があります。
    複数の最小値を正しく集約するには、すべての最小値のうちの最小値から、
    すべての最小値の合計までを範囲として出力するべきです。
    それぞれが同時に発生したかどうかを知る方法はないためです。

N   値は名前を表すため、文字列です。プロキシ名、サーバー名、Cookie名の報告に使います。
    名前は設定やキーに由来し、すべてのプロセスで同じであることが想定されます。

O   値は自由形式のテキスト出力を表します。各種コマンドの出力、ヘルスチェックの
    戻り値、ノードの説明などが該当します。

R   値はイベントのレートを表し、ある一時点の測定値です。ゲージによく似ていますが、
    受信側はこの値がゆっくり変化することを理解し、すべての値を保持しないと判断できます。
    例として、秒あたりの接続数の測定値があります。この種類のメトリクスは、
    通常、集約時に合算します。

T   値は日付または時刻を表します。現在の日付を出力するフィールドは、この型になります。
    この情報の集約方法は、実装に委ねられます。現在、この型を使うフィールドはありません。
```


三番目の文字（スコープ）は、値が反映する範囲を示します。プロセス単位の要素もあれば、設定単位やシステム単位の要素もあります。集計時に一つの値だけを保持するべきか、複数の値を集計する必要があるかを判断するうえで、この区別が重要です。現在は、次の文字をサポートします。

```text
C   値はノードのクラスター全体で有効です。クラスターは、peersプロトコルで
    通信するノードの集合です。ほかのピアと複製するスティックテーブル内の
    エントリー数などが例になります。現在、このスコープを使うメトリクスはありません。

P   値は、それを報告するプロセスだけで有効です。
    ほとんどのメトリクスはこのスコープを使います。

S   値はサービス全体で有効です。サービスは、同じ設定ファイルから一緒に
    起動したプロセスの集合です。設定に由来するメトリクスは、すべてこのスコープを使います。
    共有リソースについて、ほかのメトリクスが使う場合もあります
    （共有SSLキャッシュの統計など）。

s   値はシステム全体で有効です。システムのホスト名、現在の日付、リソース使用量などです。
    現在、このスコープを使うメトリクスはありません。
```


4 番目の文字（永続状態）は、値（メトリクス）がリロード間で揮発的か、永続的かを示します。期待される文字は：

```text
V   メトリクスは現在のプロセスに固有の一時的な値なので、リロードすると失われます。

P   メトリクスはほかの協調プロセスと共有でき、リロードをまたいで値が保持されるため、
    永続的です。
```


これらの情報を利用する側は、一般に、この4文字があれば、複数のプロセスにまたがる集計情報を正しく報告する方法を判断できます。

この列の後、3 番目の列はフィールドの型を示します。可能な型は "s32"（符号付き 32 ビット整数）、"s64"（符号付き 64 ビット整数）、"u32"（符号なし 32 ビット整数）、"u64"（符号なし 64 ビット整数）、"str"（文字列）です。値を正しく読み取るためには、型を事前に知ることが重要です。たとえば、数字のみを含む文字列であっても、整数ではなく文字列であることに注意してください（例：チェックによって抽出されたエラーコード）。

その後、4 番目の列は、その型に従ってエンコードされた値そのものです。文字列はコロンの直後にスペースを挿入せずにそのままダンプされます。文字列にコロンが含まれる場合、通常通り表示されます。これは、出力をコロンで単純に分割しないようにする必要があることを意味します。そうでないと、チェックの出力やサーバアドレスが途中で切り捨てられる可能性があります。

## 9.3. Unix ソケット コマンド {#section-9-3}


統計ソケットは、デフォルトでは有効になっていません。有効にするには、haproxy設定のグローバルセクションに一行追加する必要があります。手動でコマンドを入力するときに便利な、長めのタイムアウトを設定するため、二行目も追加することを推奨します。

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```


同じ行を繰り返すと、統計ソケットを複数追加でき、UNIXソケットの代わりにTCPポートで待ち受けるようにもできます。危険なので、デフォルトでは決してこのようにしませんが、場合によっては便利です。

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats socket ipv4@192.168.0.1:9999 level admin
    stats timeout 2m
```


ソケットにアクセスするには、"socat" などの外部ユーティリティが必要です。Socat はあらゆるものをあらゆるものに接続する万能ツールです。私たちは、端末をソケットに接続する、またはスクリプト用に stdin/stdout パイプをソケットに接続するために使用します。主に使用する 2 つの構文は以下の通りです：

```shell
# socat /var/run/haproxy.sock stdio
# socat /var/run/haproxy.sock readline
```


1 番目の構文はスクリプトで使用します。スクリプトの出力を HAProxy に送信し、HAProxy の出力を別のスクリプトに渡すことが可能です。これは、カウンターや攻撃トレースを取得する場合などに有用です。

2 番目は手動でコマンドを発行する場合にのみ有用です。readline ライブラリが端末を処理するため、行編集や履歴がサポートされ、繰り返しコマンドを発行する場合（例：カウンタの監視）に非常に便利です。

ソケットは以下の 3 種類の操作モードをサポートしています：

- 非インタラクティブ、サイレント
- インタラクティブ、サイレント
- インタラクティブでプロンプト付き

非インタラクティブモードは、socat がソケットに接続する際のデフォルトです。このモードでは 1 行のみ送信できます。1 行全体が処理され、レスポンスが返信された後、接続が閉じられます。これはスクリプトやモニタリングツールが使用するモードです。このモードでは複数のコマンドを送信することも可能ですが、セミコロン (';') で区切る必要があります。たとえば：

```shell
# echo "show info;show stat;show table" | socat /var/run/haproxy stdio
```


コマンド内でセミコロンやバックスラッシュ（例：値の中）を使用する場合、それらの前にバックスラッシュ ('&#92;') を付ける必要があります。

インタラクティブモードでは、前の行のコマンドが終了した後に新しいコマンドを送信できます。このモードは 2 つのバリエーションがあります。1 つはサイレントで、非インタラクティブモードと同様ですが、接続が閉じる代わりに新しいコマンドを待機します。もう 1 つは行頭にプロンプト ('\>') が表示されるモードです。高度なツールにはインタラクティブモードが推奨され、人間が使うにはプロンプトモードが推奨されます。

モードは "prompt" コマンドで変更できます。デフォルトでは、インタラクティブ＋プロンプトモードを切り替えます。インタラクティブモードで "prompt" を入力すると、プロンプトモードに切り替わります。コマンドはオプションで以下の特定モードを指定できます：

- "n"：非インタラクティブモード（1 コマンドのみ、終了）
- "i"：インタラクティブモード（複数のコマンド、プロンプトなし）
- "p"：プロンプトモード（複数のコマンド、プロンプト付き）

デフォルトモードが非インタラクティブであるため、モードを切り替えるには最初に "prompt" を実行する必要があります。それ以外の場合、前のコマンドが接続を閉じてしまいます。非インタラクティブモードに切り替えると、同じ行のすべてのコマンドが終了した後に接続が閉じられます。

このため、手動でデバッグを行う際には "prompt" コマンドから始めるのが一般的です：

```haproxy
# socat /var/run/haproxy readline
prompt
```


> show info ...

対話的なツールでは、"prompt i"で開始して、プロンプトなしの対話モードへ切り替える方法が適している場合があります。

任意で、プロセスの稼働時間をプロンプトに表示できます。"prompt timed"コマンドは、プロンプトを有効にし、時間表示の有無を切り替えます。稼働時間の形式は"d:hh:mm:ss"で、"d"は日数、"hh"、"mm"、"ss"は、それぞれ二桁の時間、分、秒です。

```haproxy
# socat /var/run/haproxy readline
prompt timed
```


[23:03:34:39]\> show version 2.8-dev9-e5e622-18

[23:03:34:41]\> quit

タイム付きプロンプトがマスタ CLI で設定されている場合、プロンプトには現在選択されているプロセスのアップタイムが表示されるため、マスタ、現在のワーカ、または以前のワーカのいずれでも動作します。

```shell
master> prompt timed
[0:00:00:50] master> show proc
(...)
[0:00:00:58] master> @!11955     <-- マスターから現在のワーカーに切り替え
[0:00:01:03] 11955> @!11942      <-- 現在のワーカーから古いワーカーに切り替え
[0:00:02:17] 11942> @            <-- 古いワーカーからマスターに戻る
[0:00:01:10] master>
```


複数のコマンドを一度に入力できるため、haproxyは空行を各コマンドの出力終了を示す区切りに使い、どのコマンドも出力に空行を含められないようにします。そのため、一行に複数のコマンドを連ねても、スクリプトは容易に出力を解析できます。

一部のコマンドは、任意のペイロードを受け取れます。追加するには、最初の行を"\<\<&#92;n"パターンで終える必要があります。それ以降の行をペイロードとして扱い、必要なだけ行を含められます。ペイロード付きコマンドを確定するには、空行で終える必要があります。

ペイロードの終了パターンはカスタマイズ可能です。空行以外のものでペイロードを終了させるには、'\<\<' と '&#92;n' の間にカスタムパターンを設定できます。'\<\<' に加えて最大 64 文字まで使用でき、それ以上はペイロードと見なされません。ランダムなペイロードパターンを使用するには十分な長さです。たとえば、空行やコメントを含む PEM ファイルを使用する場合：

```haproxy
# echo -e "set ssl cert common.pem <<%EOF%\n$(cat common.pem)\n%EOF%\n" | \
socat /var/run/haproxy.stat -
```


制限があります：パターン "\<\<" は行の最後の単語に接着してはいけません。コマンド行の長さは、ペイロードを開始するパターンを含むがペイロード自体は除く、tune.bufsize を超えてはいけません。ペイロードサイズはデフォルトで 128KB までです。この値は "tune.cli.max-payload-size" グローバルパラメータを設定することで変更できますが、注意が必要です。ペイロードの終了を示すパターンはこの制限に含まれます。

インタラクティブモードでペイロードを入力する際、プロンプトは "\> " から "+ " に変わります。

複数のhaproxyプロセスを同じソケットで起動すると、どのプロセスがリクエストを受け取るかは決まっておらず、受け取ったプロセスが自分自身の統計を出力することを理解しておく必要があります。

統計ソケットが現在サポートするコマンドを以下に示します。未知のコマンドを送ると、haproxyは、サポートする全コマンドを確認できる使用法メッセージを表示します。一部のコマンドは複雑な構文に対応しており、その場合、通常は、コマンドのどの部分が不正かを説明します。

一部のコマンドはより高い権限レベルが必要です。十分な権限がない場合、「Permission denied」というエラーが表示されます。詳細については、設定マニュアルの "bind" キーワード行の "level" オプションを確認してください。

<a id="entry-9-3-abort-ssl-ca-file"></a>


**`abort ssl ca-file <cafile>`**


```haproxy
abort ssl ca-file <cafile>
```


一時的なCAファイルの更新トランザクションを中止し、破棄します。

「set ssl ca-file」と「commit ssl ca-file」も参照してください。

<a id="entry-9-3-abort-ssl-cert"></a>


**`abort ssl cert <filename>`**


```haproxy
abort ssl cert <filename>
```


一時的なSSL証明書の更新トランザクションを中止し、破棄します。

「set ssl cert」と「commit ssl cert」も参照してください。

<a id="entry-9-3-abort-ssl-crl-file"></a>


**`abort ssl crl-file <crlfile>`**


```haproxy
abort ssl crl-file <crlfile>
```


一時的な CRL ファイル更新トランザクションを中止し、破棄します。

「set ssl crl-file」と「commit ssl crl-file」も参照してください。

<a id="entry-9-3-acme-renew"></a>


**`acme renew <certificate>`**


```haproxy
acme renew <certificate>
```


指定した証明書名で、ACME証明書の生成タスクを開始します。証明書はacmeセクションに関連付けられていなければなりません。設定マニュアルのセクション[12.8](/ja/docs/haproxy/other-sections/#section-12-8)「ACME」を参照してください。"acme status"も参照してください。

<a id="entry-9-3-acme-status"></a>


**`acme status`**


```haproxy
acme status
```


ACME で設定されたすべての証明書の状態を表示します。

このコマンドは、タブで区切って出力します：

- HAProxy で設定された証明書の名前
- 設定で使用された acme セクション
- ACME タスクの状態。いずれか「Running」、「Scheduled」、「Stopped」
- 証明書の UTC での有効期限日時（ISO8601 形式）
- 有効期限までの相対時間（期限切れなら0d）
- 証明書の UTC でのスケジュール日時（ISO8601 形式）
- 相対的なスケジュール時間（Running の場合は 0d）

例：

```shell
$ echo "@1; acme status" | socat /tmp/master.sock - | column -t -s $'\t'
# certificate   section  state      expiration date (UTC)  expires in        scheduled date (UTC)  scheduled in
ecdsa.pem       LE       Running    2020-01-18T09:31:12Z   0d 0h00m00s       2020-01-15T21:31:12Z  0d 0h00m00s
foobar.pem.rsa  LE       Scheduled  2025-08-04T11:50:54Z   89d 23h01m13s     2025-07-27T23:50:55Z  82d 11h01m14s
```


<a id="entry-9-3-add-acl"></a>


**`add acl [@<ver>] <acl> <pattern>`**


```haproxy
add acl [@<ver>] <acl> <pattern>
```


ACL `<acl>` にエントリを追加します。`<acl>` は "show acl" によって返された \#`<id>` または `<name>` です。エントリが既に存在するかの検証は行われません。エントリは、特定のバージョンが指定されていない限り、現在の ACL バージョンに追加されます。特定のバージョンを指定するには "@`<ver>`" を使用します。このバージョン番号は、事前に "prepare acl" で割り当てられている必要があります。また、"show acl" の出力で報告される "curr_ver" と "next_ver" の間のバージョンになります。特定のバージョン番号で追加されたエントリは、「commit acl」操作が実行されるまで一致しません。ただし、「show acl @`<ver>`」コマンドで照会したり、「clear acl @`<ver>`」コマンドでクリアすることは可能です。参照する `<acl>` がマップと同時に使用されている名前である場合、このコマンドは使用できません。この場合、「add map」コマンドを使用する必要があります。

<a id="entry-9-3-add-backend"></a>


**`add backend <name> from <defproxy> [mode <mode>] [guid <guid>]`**


```haproxy
add backend <name> from <defproxy> [mode <mode>] [guid <guid>]
```


名前 `<name>` の新しいバックエンドプロキシをインスタンス化します。

作成できるのはTCPまたはHTTPプロキシだけです。設定はすべて、デフォルトプロキシのインスタンス`<defproxy>`から継承します。デフォルトでは、`<defproxy>`が明示的に定義していない限り、同名の引数でバックエンドのモードを必ず指定しなければなりません。必要なら、任意のGUID引数も使えます。

サーバは「add server」コマンドで追加できます。バックエンドは非公開状態で初期化されます。トラフィックに使用可能と判断されたら、「publish backend」を使用して新しく作成されたインスタンスを公開します。

名前付きのデフォルトプロキシは、設定解析時に適用される継承ルールを満たしている限り使用可能です。ただし例外もあり、たとえばモードが TCP でも HTTP でもない場合などです。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-add-map"></a>


**`add map [@<ver>] <map> <key> <value>`**


```haproxy
add map [@<ver>] <map> <key> <value>
add map [@<ver>] <map> <payload>
```


マップ `<map>` にエントリを追加し、キー `<key>` に値 `<value>` を関連付けます。エントリが既に存在するかの検証は行われません。主に「clear」または「prepare」操作後にマップを埋めるために使用します。エントリは、特定のバージョンが指定されていない限り、現在の ACL バージョンに追加されます。特定のバージョンを指定するには "@`<ver>`" を使用します。このバージョン番号は、事前に "prepare acl" で割り当てられている必要があります。また、"show acl" の出力で報告される "curr_ver" と "next_ver" の間のバージョンになります。特定のバージョン番号で追加されたエントリは、「commit map」操作が実行されるまで一致しません。ただし、「show map @`<ver>`」コマンドで照会したり、「clear acl @`<ver>`」コマンドでクリアすることは可能です。指定されたマップが ACL としても使用されている場合、ACL は `<key>` 部分のみを一致させ、`<value>` 部分を無視します。ペイロード構文を使用すると、複数のキー/値ペアを別々の行に記述することで追加できます。各行の最初の単語がキーとなり、残りの行は値として扱われ、スペースを含むことも可能です。

例：

```shell
# socat /tmp/sock1 -
prompt

> add map #-1 <<
+ key1 value1
+ key2 value2 with spaces
+ key3 value3 also with spaces
+ key4 value4

>
```


<a id="entry-9-3-add-server"></a>


**`add server <backend>/<server> [args]*`**


```haproxy
add server <backend>/<server> [args]*
```


バックエンド `<backend>` に接続された新しいサーバをインスタンス化します。

`<server>`の名前は、バックエンド内で未使用でなければなりません。バックエンドには、動的ロードバランシングアルゴリズムを使わなければならないという、特別な制限があります。設定ファイルのserver文の一部のキーワードで、サーバーの動作を設定できます（一覧は"add server help"を参照）。同じバックエンドに'default-server'文があったとしても、その設定は一切再利用しない点にも注意してください。

現在、動的サーバーは、init-addrの"none"方式で静的に初期化します。そのため、アドレスにFQDNを指定しても、サーバーの作成自体が受け付けられたとしても、名前解決は行いません。

リロード操作に対応するため、CLIで作成したサーバーは、該当するhaproxy設定ファイルにも手動で追加しておくことを想定しています。設定にない動的サーバーは、リロード後に復元しません。

動的サーバは、構成内の別のサーバのチェックステータスを追跡する「track」キーワードを使用できます。ただし、別の動的サーバを追跡することはできません。これは、動的サーバの削除が発生しても追跡チェーンが一貫性を保つようにするためです。

ヘルスチェックをサポートするには、"check"キーワードを使います。ヘルスチェックはデフォルトでは無効で、サーバー自体とは別に、"enable health"コマンドで有効にしなければなりません。エージェントチェックには、"agent-check"キーワードと"enable agent"コマンドを使います。この場合、報告される状態に応じて、明示的な"enable server"コマンドがなくても、エージェントがサーバーを有効にすることがあります。そのため、エージェントチェックを持つ動的サーバーの削除には、特に注意が必要です。削除に必要なメンテナンスモードへサーバーを移せるよう、先に"disable agent"でエージェントを無効にするべきです。

大量の動的サーバーを使用する場合、ファイルディスクリプタの制限に達する可能性があります。その場合は、「u-limit」グローバルキーワードのドキュメントを参照してください。

<a id="entry-9-3-add-server-help"></a>


**`add server help`**


```haproxy
add server help
```


現在の HAProxy バージョンでサポートされる動的サーバー用のキーワードをリストアップします。キーワードの構文は設定ファイルのサーバーラインと類似しており、詳細については個別ドキュメントを参照してください。

<a id="entry-9-3-add-ssl-ca-file"></a>


**`add ssl ca-file <cafile> <payload>`**


```haproxy
add ssl ca-file <cafile> <payload>
```


CA ファイルに新しい証明書を追加します。CLI でのバッファサイズ制限に達した場合に、複数の証明書を追加するのに有用です。すべての証明書を一度に「set」する代わりに、個別に証明書を追加できます。「set ssl ca-file」は CA ファイルをリセットします。

例：

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate1.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate2.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```


<a id="entry-9-3-add-ssl-crt-list"></a>


**`add ssl crt-list <crtlist> <certificate>`**


```haproxy
add ssl crt-list <crtlist> <certificate>
add ssl crt-list <crtlist> <payload>
```


crt-listに証明書を追加します。ディレクトリも現在はcrt-listと同じ方法で読み込むため、ディレクトリにも使えます。このコマンドは、パラメーターに証明書名を指定できます。SSLオプションやフィルターを使う場合は、代わりにcrt-listの一行をペイロードとして送らなければなりません。ペイロードでサポートするのはcrt-listの一行だけです。このコマンドは、crt-listを使うすべてのbind行に証明書を読み込みます。HAProxyへ新しい証明書を送るには、"new ssl cert"と"set ssl cert"コマンドを使わなければなりません。

例：

```shell
$ echo "new ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo -e "set ssl cert foobar.pem <<\n$(cat foobar.pem)\n" | socat
/tmp/sock1 -
$ echo "commit ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo "add ssl crt-list certlist1 foobar.pem" | socat /tmp/sock1 -

$ echo -e 'add ssl crt-list certlist1 <<\nfoobar.pem [allow-0rtt] foo.bar.com
!test1.com\n' | socat /tmp/sock1 -
```


<a id="entry-9-3-add-ssl-ech"></a>


**`add ssl ech <bind> <payload>`**


```haproxy
add ssl ech <bind> <payload>
```


`<bind>` 行に ECH キーを追加します。ペイロードは ECH 形式の PEM でなければなりません。
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

bind行の形式は`<frontend>`/@`<filename>`:`<linenum>`（例：frontend1/@haproxy.conf:19）です。"name"キーワードでbind行に名前を付けた場合は、`<frontend>`/`<name>`形式も使えます。

OpenSSL のバージョンが ECH をサポートしている必要があり、HAProxy は USE_ECH=1 でコンパイルされている必要があります。このコマンドは、実験モードで実行されている CLI 接続でのみサポートされます（「experimental-mode on」を参照）。

"show ssl ech"と、設定マニュアルの[セクション5.1](/ja/docs/haproxy/bind-and-server-options/#section-5-1)にある"ech"も参照してください。

例：

```shell
$ openssl ech -public_name foobar.com -out foobar3.com.ech
$ echo -e "experimental-mode on; add ssl ech frontend1/@haproxy.conf:19 <<%EOF%\n$(cat foobar3.com.ech)\n%EOF%\n" | \
  socat /tmp/haproxy.sock -
added a new ECH config to frontend1
```


<a id="entry-9-3-add-ssl-jwt"></a>


**`add ssl jwt <filename>`**


```haproxy
add ssl jwt <filename>
```


JWT 検証に使用できる証明書リストに、すでに読み込まれた証明書を追加します（"jwt_verify_cert" コンバーターを参照）。このコマンドは進行中のトランザクションでは動作しません。また、「del ssl jwt」と「show ssl jwt」コマンドも参照してください。詳細については「jwt」証明書オプションを参照してください。

<a id="entry-9-3-clear-counters"></a>


**`clear counters`**


```haproxy
clear counters
```


各プロキシ（フロントエンドおよびバックエンド）および各サーバーの統計カウンターの最大値をクリアします。累積カウンターには影響しません。「show activity」で報告される内部アクティビティカウンターもリセットされます。このコマンドは、事故後のクリーンなカウンターを取得するために使用でき、再起動やトラフィックカウンターのクリアを必要としません。このコマンドは制限付きであり、レベル「operator」または「admin」に設定されたソケットでのみ実行できます。

<a id="entry-9-3-clear-counters-all"></a>


**`clear counters all`**


```haproxy
clear counters all
```


各プロキシ（フロントエンドおよびバックエンド）および各サーバーのすべての統計カウンターをクリアします。再起動と同等の効果があります。このコマンドは制限付きであり、レベル「admin」に設定されたソケットでのみ実行できます。

<a id="entry-9-3-clear-acl"></a>


**`clear acl [@<ver>] <acl>`**


```haproxy
clear acl [@<ver>] <acl>
```


ACL `<acl>` からすべてのエントリを削除します。`<acl>` は「show acl」によって返される \#`<id>` または `<name>` です。参照 `<acl>` が名前であり、マップと共有されている場合、そのマップもクリアされます。デフォルトでは、現在のバージョンの ACL（照合対象となっているもの）のみがクリアされます。ただし、'@' に続いてバージョンを指定することで、別のバージョンを指定することも可能です。

<a id="entry-9-3-clear-map"></a>


**`clear map [@<ver>] <map>`**


```haproxy
clear map [@<ver>] <map>
```


マップ `<map>` からすべてのエントリを削除します。`<map>` は「show map」によって返される \#`<id>` または `<name>` です。参照 `<map>` が名前であり、ACL と共有されている場合、その ACL もクリアされます。デフォルトでは、現在のバージョンのマップ（照合対象となっているもの）のみがクリアされます。ただし、'@' に続いてバージョンを指定することで、別のバージョンを指定することも可能です。

<a id="entry-9-3-clear-table"></a>


**`clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |`**


```haproxy
clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |
                    [ ptr <ptr> ]
```


stick-table `<table>` からエントリを削除します。

通常は、サービスへのアクセスが不当に拒否されたと訴えるユーザーのブロック解除に使いますが、交換予定のサーバーに対応する永続性のエントリーを消す用途にも使えます（詳細は後述の"show table"を参照）。現在、セッションがエントリーを追跡しているために、削除を拒否する場合がある点に注意してください。通常は、数秒後、セッションが終了してから再試行すれば十分です。

オプション引数が指定されない場合、すべてのエントリが削除されます。

"data."形式では、保存データに適用したフィルターにマッチするエントリーを削除します（セクション4.2の"stick-table"を参照）。`<type>`には保存データの型を指定しなければならず、その型のデータをテーブルに保存していなければ、エラーになります。`<operator>`に従い、データを64ビット整数`<value>`と比較します。演算子はACLと同じです。

    - eq：データがこの値と等しいエントリをマッチ
    - ne：データがこの値と等しくないエントリをマッチ
    - le：データがこの値以下のエントリーにマッチします。
    - ge：データがこの値以上のエントリーにマッチします。
    - lt：データがこの値未満のエントリーにマッチします。
    - gt：データがこの値より大きいエントリーにマッチします。

key形式では、エントリー`<key>`を削除します。キーはテーブルと同じ型でなければならず、現在はIPv4、IPv6、整数、文字列に限られます。

ptr形式では、エントリー`<ptr>`を削除します。`<ptr>`は0xffff形式で書き、以前の"show table"コマンドが返したアドレスに対応していなければなりません。空のキーやCLIで扱えない文字のためにキーでマッチできない場合、ポインターでエントリーをマッチさせる方法が有効な場合があります。

data.`<type>`が配列型なら、"[]"で特定のインデックスへアクセスできます。たとえば、data.gpt[1]です。

例：

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1 \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy key 127.0.0.1" | socat stdio /tmp/sock1

    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200
      bytes_out_rate(60000)=191
    $ echo "clear table http_proxy data.gpc0 eq 1" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy ptr 0x80e6b40" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:0
```


<a id="entry-9-3-commit-acl"></a>


**`commit acl @<ver> <acl>`**


```haproxy
commit acl @<ver> <acl>
```


バージョン `<ver>` の ACL `<acl>` に対して行ったすべての変更をコミットし、過去のすべてのバージョンを削除します。`<acl>` は "show acl" から返された \#`<id>` または `<name>` です。バージョン番号は "show acl" で報告された "curr_ver"+1 から "next_ver" の範囲内である必要があります。コミット対象の内容は、必要に応じて "show acl @`<ver>` `<acl>`" で確認できます。指定されたバージョン番号は通常、"prepare acl" コマンドで作成されています。置換はアトミックです。これは、現在のバージョンを指定されたバージョンにアトミックに更新することを意味し、これにより他のバージョンのすべてのエントリが即座に非表示になり、新しいバージョンのすべてのエントリが表示されます。また、"prepare acl" を実行した後にエントリを追加せずにコミットすることで、ACL のすべての表示エントリをアトミックに削除することも可能です。参照 `<acl>` がマップとしても使用されている名前である場合、このコマンドは使用できません。この場合、代わりに "commit map" コマンドを使用する必要があります。

<a id="entry-9-3-commit-map"></a>


**`commit map @<ver> <map>`**


```haproxy
commit map @<ver> <map>
```


バージョン `<ver>` のマップ `<map>` に対して行ったすべての変更をコミットし、過去のすべてのバージョンを削除します。`<map>` は "show map" から返された \#`<id>` または `<name>` です。バージョン番号は "show map" で報告された "curr_ver"+1 から "next_ver" の範囲内である必要があります。コミット対象の内容は、必要に応じて "show map @`<ver>` `<map>`" で確認できます。指定されたバージョン番号は通常、"prepare map" コマンドで作成されています。置換はアトミックです。これは、現在のバージョンを指定されたバージョンにアトミックに更新することを意味し、これにより他のバージョンのすべてのエントリが即座に非表示になり、新しいバージョンのすべてのエントリが表示されます。また、"prepare map" を実行した後にエントリを追加せずにコミットすることで、マップのすべての表示エントリをアトミックに削除することも可能です。

<a id="entry-9-3-commit-ssl-ca-file"></a>


**`commit ssl ca-file <cafile>`**


```haproxy
commit ssl ca-file <cafile>
```


一時的な SSL CA ファイル更新トランザクションをコミットします。

既存の CA ファイル（"show ssl ca-file" で "Used" 状態）の場合、新しい CA ファイルのツリー エントリが CA ファイルツリーに挿入され、CA ファイルエントリを使用していたすべてのインスタンスが再構築され、必要な SSL コンテキストも再構築されます。再構築されたインスタンスが以前に使用していたすべてのコンテキストは削除されます。成功した場合、以前の CA ファイルエントリはツリーから削除されます。失敗した場合、何も削除されず、すべての元の SSL コンテキストが保持され使用されます。一時トランザクションがコミットされると、そのトランザクションは破棄されます。

新しいCAファイルの場合（"new ssl ca-file"の後、"show ssl ca-file"で"Unused"の状態）は、CAファイルツリーへ挿入しますが、HAProxy内のどこでも使いません。使い始め、そのSSLコンテキストを生成するには、"add ssl crt-list"でcrt-listへ追加する必要があります。

"new ssl ca-file"、"set ssl ca-file"、"add ssl ca-file"、"abort ssl ca-file"、"add ssl crt-list" も参照してください。

<a id="entry-9-3-commit-ssl-cert"></a>


**`commit ssl cert <filename>`**


```haproxy
commit ssl cert <filename>
```


一時的な SSL 証明書更新トランザクションをコミットします。

既存の証明書（"show ssl cert" で "Used" 状態）の場合、必要なすべての SSL コンテキストと SNI を生成し、挿入し、以前のものを削除します。構成で `<filename>` が使用されていた場所すべてで、以前の SSL 証明書をメモリ上に置き換える。失敗した場合、何も削除または挿入しません。一時トランザクションがコミットされると、そのトランザクションは破棄されます。

新しい証明書の場合（"new ssl cert"の後、"show ssl cert"で"Unused"の状態）は、証明書ストレージへコミットしますが、haproxy内のどこでも使いません。使い始め、そのSNIを生成するには、"add ssl crt-list"でcrt-listまたはディレクトリへ追加する必要があります。

"new ssl cert"、"set ssl cert"、"abort ssl cert"、"add ssl crt-list" も参照してください。

<a id="entry-9-3-commit-ssl-crl-file"></a>


**`commit ssl crl-file <crlfile>`**


```haproxy
commit ssl crl-file <crlfile>
```


一時的な SSL CRL ファイル更新トランザクションをコミットします。

既存の CRL ファイル（"show ssl crl-file" で "Used" 状態）の場合、新しい CRL ファイルエントリが CA ファイルツリー（CA ファイルと CRL ファイルを両方保持）に挿入され、CRL ファイルエントリを使用していたすべてのインスタンスが再構築され、必要な SSL コンテキストも再構築されます。再構築されたインスタンスが以前に使用していたすべてのコンテキストは削除されます。成功した場合、以前の CRL ファイルエントリはツリーから削除されます。失敗した場合、何も削除されず、すべての元の SSL コンテキストが保持され使用されます。一時トランザクションがコミットされると、そのトランザクションは破棄されます。

新しいCRLファイルの場合（"new ssl crl-file"の後、"show ssl crl-file"で"Unused"の状態）は、CRLファイルツリーへ挿入しますが、HAProxy内のどこでも使いません。使い始め、そのSSLコンテキストを生成するには、"add ssl crt-list"でcrt-listへ追加する必要があります。

"new ssl crl-file"、"set ssl crl-file"、"abort ssl crl-file"、"add ssl crt-list" も参照してください。

<a id="entry-9-3-debug-counters"></a>


**`debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*`**


```haproxy
debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*
```


コード内に配置された内部カウンターの一覧を表示します。これらのカウンターは、ビルドオプションによって異なる場合があります。一部は DEBUG_STRICT に依存し、他の一部は DEBUG_COUNTERS に依存します。このコマンドは複数の引数の組み合わせを取るため、一部はアクションを定義し、他の一部はフィルターを定義します。- bug は BUG_ON() ステートメントのカウンターを表示します - cnt は COUNT_IF() ステートメントのカウンターを表示します - chk は CHECK_IF() ステートメントのカウンターを表示します - glt は COUNT_GLITCH() ステートメントのカウンターを表示します - all は一度もトリガーされなかったカウンター（値が 0）を表示します - off アクション：COUNT_IF() カウンターの更新を無効化します - on アクション：COUNT_IF() カウンターの更新を有効化します - reset アクション：指定されたすべてのカウンターをリセットします - show アクション：指定されたすべてのカウンターを表示します

デフォルトのアクションは、カウンターを表示する"show"で、種類を問わず、値がゼロでないカウンターを一覧にします。他のアクションを指定しなければ"show"は暗黙的に適用します。明示的な"show"は、スクリプトからコマンドを生成しやすくするためだけに存在します。

出力は整数のカウンターから始まり、その後にカウンターのタイプ（大文字）、コード上の位置（ファイル:行）、関数名が続き、必要に応じて ": " と説明が続きます。出力形式はメジャーバージョン間で変更される可能性があること、また新しいタイプやエントリが安定版にバックポートされる場合があることに注意してください。これはデバッグ能力の向上のためです。それらに対する監視は、非常に緩やかで許容的な方法で行うべきであり、できれば行わないでください。

通常、エンドユーザーはこのコマンドを使用しませんが、問題の原因を特定しようとしている開発者が、CNT または GLT エントリを探すためにユーザーに使用を依頼することがあります。一方、非ゼロの "CHK" エントリは想定されておらず、コード内の誤った仮定を示している可能性があるため、開発者に報告すべきです。

<a id="entry-9-3-debug-dev"></a>


**`debug dev <command> [args]*`**


```haproxy
debug dev <command> [args]*
```


開発者専用のコマンドを呼び出します。CLI 接続でエキスパートモードが有効になっている場合にのみサポートされます（「expert-mode on」を参照）。これらのコマンドは極めて危険であり、誤操作に対する余裕がなく、誤用するとプロセスのクラッシュを引き起こす可能性があります。これらはエキスパート専用であり、指示された場合を除き、絶対に使用してはなりません。一部のコマンドは haproxy を DEBUG_DEV を定義してビルドした場合にのみ利用可能であり、セキュリティ上の影響を伴う可能性があるためです。これらのすべてのコマンドには管理者権限が必要であり、ソースコードに精通していない人が使用することを避けるために意図的にドキュメント化されていません。

<a id="entry-9-3-del-acl"></a>


**`del acl <acl> [<key>|#<ref>]`**


```haproxy
del acl <acl> [<key>|#<ref>]
```


キー `<key>` に対応する acl `<acl>` からすべての acl エントリを削除します。`<acl>` は "show acl" によって返された \#`<id>` または `<name>` です。`<ref>` が使用された場合、このコマンドはリストされた参照のみを削除します。参照は acl の内容をリストすることで確認できます。参照 `<acl>` が名前であり、map と共有されている場合、エントリは map でも削除されます。

<a id="entry-9-3-del-backend"></a>


**`del backend <name>`**


```haproxy
del backend <name>
```


名前 `<name>` のバックエンドプロキシを削除します。

この操作は TCP または HTTP プロキシに対してのみ可能です。成功するためには、まずバックエンドインスタンスが公開解除されている必要があります。また、そのすべてのサーバーはまず削除されている必要があります（"del server" CLI を使用）。最後に、バックエンドインスタンスにまだ接続されているストリームが存在してはなりません。

バックエンドの削除を妨げる、その他の制限もあります。まず、use_backendルールやサンプル式など、設定の要素が明示的に参照するバックエンドは削除できません。一部のプロキシオプションも実行中の削除と両立せず、現在は、非推奨のdispatchまたはoption transparentを使う場合が該当します。また、スティックテーブルを宣言しているバックエンドも削除できません。最後に、QUICサーバーが存在していたバックエンドは、現時点では削除できません。

このコマンドの前に"wait be-removable"を使うと、上記の条件を確認するのに便利です。また、対象のバックエンドに結び付いたストリームが最後に閉じられるまで待つ方法にもなります。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-del-map"></a>


**`del map <map> [<key>|#<ref>]`**


```haproxy
del map <map> [<key>|#<ref>]
```


キー `<key>` に対応する map `<map>` からすべての map エントリを削除します。`<map>` は "show map" によって返された \#`<id>` または `<name>` です。`<ref>` が使用された場合、このコマンドはリストされた参照のみを削除します。参照は map の内容をリストすることで確認できます。参照 `<map>` が名前であり、acl と共有されている場合、エントリは map でも削除されます。

<a id="entry-9-3-del-ssl-ca-file"></a>


**`del ssl ca-file <cafile>`**


```haproxy
del ssl ca-file <cafile>
```


HAProxy から CA ファイルツリーのエントリを削除します。CA ファイルは使用されておらず、すべての crt-list から削除されている必要があります。"show ssl ca-file" は CA ファイルの状態を表示します。設定ファイル内の "ca-file" または "ca-verify-file" ディレクティブで直接参照されている証明書に対しては削除はできません。

<a id="entry-9-3-del-ssl-cert"></a>


**`del ssl cert <certfile>`**


```haproxy
del ssl cert <certfile>
```


HAProxyから証明書ストアを削除します。証明書は、JWT検証も含めて未使用で、すべてのcrt-listやディレクトリから取り除かれていなければなりません。"show ssl cert"で証明書の状態を表示できます。設定の"crt"ディレクティブが直接参照する証明書は、削除できません。

<a id="entry-9-3-del-ssl-crl-file"></a>


**`del ssl crl-file <crlfile>`**


```haproxy
del ssl crl-file <crlfile>
```


HAProxy から CRL ファイルツリーのエントリを削除します。CRL ファイルは使用されておらず、すべての crt-list から削除されている必要があります。"show ssl crl-file" は CRL ファイルの状態を表示します。設定ファイル内の "crl-file" ディレクティブで直接参照されている証明書に対しては削除はできません。

<a id="entry-9-3-del-ssl-crt-list"></a>


**`del ssl crt-list <filename> <certfile[:line]>`**


```haproxy
del ssl crt-list <filename> <certfile[:line]>
```


crt-list 内のエントリを削除します。これにより、このエントリに使用されているすべての SNI がフロントエンドで削除されます。同じ証明書が crt-list 内で複数回使用されている場合、削除する行を指定する必要があります。行番号を表示するには "show ssl crt-list -n `<crtlist>`" を使用します。

<a id="entry-9-3-del-ssl-ech"></a>


**`del ssl ech <bind>`**


```haproxy
del ssl ech <bind>
```


バインド行のECHキーを削除します。

bind行の形式は`<frontend>`/@`<filename>`:`<linenum>`（例：frontend1/@haproxy.conf:19）です。"name"キーワードでbind行に名前を付けた場合は、`<frontend>`/`<name>`形式も使えます。

OpenSSL のバージョンが ECH をサポートしている必要があり、HAProxy は USE_ECH=1 でコンパイルされている必要があります。このコマンドは、実験モードで実行されている CLI 接続でのみサポートされます（「experimental-mode on」を参照）。

"show ssl ech"、"add ssl ech"と、設定マニュアルの[セクション5.1](/ja/docs/haproxy/bind-and-server-options/#section-5-1)にある"ech"も参照してください。

例：

```shell
$ echo "experimental-mode on; del ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
deleted all ECH configs from frontend1/@haproxy.conf:19
```


<a id="entry-9-3-del-ssl-jwt"></a>


**`del ssl jwt <filename>`**


```haproxy
del ssl jwt <filename>
```


JWT検証に使える証明書の一覧から、既に読み込んだ証明書を取り除きます（"jwt_verify_cert"コンバーターを参照）。進行中のトランザクションには、このコマンドは使えません。"add ssl jwt"と"show ssl jwt"コマンドも参照してください。詳細は"jwt"証明書オプションを参照してください。

<a id="entry-9-3-del-server"></a>


**`del server <backend>/<server>`**


```haproxy
del server <backend>/<server>
```


バックエンド `<backend>` に接続された削除可能なサーバーを削除します。削除可能なサーバーとは、以下のすべての条件を満たすサーバーを指します：

- 他の構成要素によって参照されていないこと
- すでにメンテナンスモードにあること（「disable server」を参照）
- アクティブまたはアイドル状態の接続が存在しないこと

これらの条件のいずれかを満たさない場合、コマンドは失敗します。

有効な接続とは、進行中のリクエストが少なくとも一つある接続です。"shutdown sessions server"で、終了を早められます。有効な接続とアイドル接続がすべて閉じられ、コマンドが確実に成功するよう、"del server"の前に"wait srv-removable"を使うことを強く推奨します。

<a id="entry-9-3-disable-agent"></a>


**`disable agent <backend>/<server>`**


```haproxy
disable agent <backend>/<server>
```


補助エージェントチェックを一時停止状態としてマークします。

serverディレクティブのagent-checkパラメーターにより、エージェントチェックを補助チェックとして使っている場合、新しいチェックは、エージェントが有効な場合だけ開始します。したがって、disable agentは、enable agentで再び有効にするまで、すべての新しいエージェントチェックの開始を防ぎます。

エージェントが無効化された場合、エージェントが有効状態であった間に開始された補助エージェントチェックの処理は以下の通りです：重みを変更する可能性のある結果（特に「drain」またはエージェントが返す重み）は無視されます。エージェントチェックの処理その他の部分は変更されません。

この機能の目的は、エージェントチェックによる重みの変更効果を一時停止し、set weight コマンドでサーバーの重みを設定した後にエージェントによる上書きを防ぐことです。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-disable-dynamic-cookie-backend"></a>


**`disable dynamic-cookie backend <backend>`**


```haproxy
disable dynamic-cookie backend <backend>
```


バックエンド `<backend>` における動的クッキーの生成を無効化します。

<a id="entry-9-3-disable-frontend"></a>


**`disable frontend <frontend>`**


```haproxy
disable frontend <frontend>
```


フロントエンドを一時停止状態にします。ソフト再起動で使うモードに相当し、ポートを解放しますが、必要なら再び有効にできます。Linux以外の一部のOSは再び有効にできないため、慎重に使うべきです。プロキシの停止など考えられない環境で、誤って設定したプロキシを修正しなければならない場合を想定しています。ポートを解放して別のプロセスにバインドし、運用を復旧できます。統計ページでは、フロントエンドを"STOP"状態で表示します。

フロントエンドは名前またはシャープ記号（'#'）を付加した数値IDのいずれかで指定できます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-disable-health"></a>


**`disable health <backend>/<server>`**


```haproxy
disable health <backend>/<server>
```


プライマリヘルスチェックを一時停止状態としてマークします。これによりヘルスチェックの送信が無効化され、最後のヘルスチェック結果は無視されます。サーバーはチェック未実施状態となり、補助エージェントチェックが強制的にダウンにしない限りUPと見なされます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-disable-server"></a>


**`disable server <backend>/<server>`**


```haproxy
disable server <backend>/<server>
```


サーバーをメンテナンス用にDOWN状態としてマークします。このモードでは、サーバーがメンテナンスから離れるまで、さらにチェックは実行されません。他のサーバーによって追跡されている場合、その追跡サーバーはメンテナンス中はDOWN状態になります。

統計ページでは、メンテナンス用にDOWN状態のサーバーは「MAINT」ステータスで表示され、追跡サーバーは「MAINT(via)」ステータスで表示されます。

バックエンドおよびサーバーは、名前またはシャープ記号（'#'）を付加した数値IDのいずれかで指定できます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-dump-ssl-cert"></a>


**`dump ssl cert <certfile>`**


```haproxy
dump ssl cert <certfile>
```


HAProxyのメモリーに読み込んだ証明書を出力します。PEM形式で、秘密鍵、リーフ証明書、最後にチェーンの順に出力します。ファイル名の前にアスタリスクを付けると、トランザクションも出力できます。ファイルシステム上では更新せず、CLIで更新した証明書を、ファイルシステムへ保存するのに便利です。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

例：

```shell
$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 -

$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 - | openssl storeutl -noout -text /dev/stdin
```


<a id="entry-9-3-dump-stats-file"></a>


**`dump stats-file`**


```haproxy
dump stats-file
```


起動時にHAProxyカウンター値を事前読み込みできるようにするためのstats-fileを生成します。詳細については「統計ファイル」セクションを参照してください。

<a id="entry-9-3-echo"></a>


**`echo <text>`**


```haproxy
echo <text>
```


CLIでテキストを出力します。複数のコマンドの結果を出力するとき、コマンドの間にコメントを書くのに便利です。

例：

```text
echo "expert-mode on; echo FDs from fdtab; show fd; echo wild FDs; debug dev fd" | socat /var/run/haproxy.sock -

```


<a id="entry-9-3-enable-agent"></a>


**`enable agent <backend>/<server>`**


```haproxy
enable agent <backend>/<server>
```


一時停止状態にされた補助エージェントチェックを再開します。

補助エージェントの一時停止および再開の効果については、「disable agent」を参照してください。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-enable-dynamic-cookie-backend"></a>


**`enable dynamic-cookie backend <backend>`**


```haproxy
enable dynamic-cookie backend <backend>
```


バックエンド`<backend>`の動的Cookieの生成を有効にします。秘密キーも指定しなければなりません。

<a id="entry-9-3-enable-frontend"></a>


**`enable frontend <frontend>`**


```haproxy
enable frontend <frontend>
```


一時停止状態にされたフロントエンドを再開します。一部のリスニングポートが再バインドできなくなる可能性があります（例：'disable frontend'操作後に別のプロセスがそれらを占有した場合）。その場合、エラーが表示されます。一部のオペレーティングシステムでは、無効化されたフロントエンドの再開ができない場合があります。

フロントエンドは名前またはシャープ記号（'#'）を付加した数値IDのいずれかで指定できます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-enable-health"></a>


**`enable health <backend>/<server>`**


```haproxy
enable health <backend>/<server>
```


一時停止したプライマリヘルスチェックを再開し、チェックの送信を再び有効にします。詳細は"disable health"を参照してください。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-enable-server"></a>


**`enable server <backend>/<server>`**


```haproxy
enable server <backend>/<server>
```


サーバーが以前にメンテナンスのために DOWN とマークされていた場合、このコマンドはサーバーを UP にマークし、ヘルスチェックが再び有効になります。

バックエンドおよびサーバーは、名前またはシャープ記号（'#'）を付加した数値IDのいずれかで指定できます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-experimental-mode"></a>


**`experimental-mode [on|off]`**


```haproxy
experimental-mode [on|off]
```


オプションを指定しない場合、現在の接続で実験モードが有効化されているか否かを示します。"on" を指定すると、現在の CLI 接続でのみ実験モードを有効化します。"off" を指定すると無効化します。

実験モードは開発中の追加機能にアクセスするために使用されます。これらの機能は現在安定しておらず、注意を要します。バージョン間で破壊的な変更が加えられる可能性があります。

マスターCLIから使う場合、このコマンドに接頭辞を付けるべきではありません。各ワーカーのCLIに接続するときに、そのワーカーのモードを設定するためです。

例：

```text
echo "@1; experimental-mode on; <experimental_cmd>..." | socat /var/run/haproxy.master -
echo "experimental-mode on; @1 <experimental_cmd>..." | socat /var/run/haproxy.master -
```


<a id="entry-9-3-expert-mode"></a>


**`expert-mode [on|off]`**


```haproxy
expert-mode [on|off]
```


このコマンドは experimental-mode に似ていますが、エキスパートモードを切り替えるために使用されます。

エキスパートモードは、プロセスにとって極めて危険になり得るエキスパートコマンドの表示を有効にします。これらのコマンドは、開発者が複雑な不具合に関する重要な情報を集めるのに役立つ場合があります。誤用すれば、プロセスがクラッシュする可能性が高いため、使用するよう求められない限り、このオプションを使わないでください。このコマンドは、意図的にヘルプメッセージへ載せていません。adminレベルでだけ使えます。他のレベルへ変更すると、エキスパートモードは自動的にリセットされます。

マスターCLIから使う場合、このコマンドに接頭辞を付けるべきではありません。各ワーカーのCLIに接続するときに、そのワーカーのモードを設定するためです。

例：

```text
echo "@1; expert-mode on; debug dev exit 1" | socat /var/run/haproxy.master -
echo "expert-mode on; @1 debug dev exit 1" | socat /var/run/haproxy.master -
```


<a id="entry-9-3-get-map"></a>


**`get map <map> <value>`**


```haproxy
get map <map> <value>
get acl <acl> <value>
```


マップ `<map>` または ACL `<acl>` 内で `<value>` の値を検索します。`<map>` または `<acl>` は "show map" または "show acl" によって返される \#`<id>` または `<name>` です。このコマンドは、このマップに関連付けられたすべての一致するパターンを返します。マップや ACL のデバッグに有用です。出力形式は、一致するタイプごとに1行ずつ構成されます。各行はスペース区切りの単語列で構成されます。

最初の2つの単語は：

```text
<match method>:   適用した照合方法。"found"、"bool"、
                  "int"、"ip"、"bin"、"len"、"str"、"beg"、"sub"、"dir"、
                  "dom"、"end"、"reg"のいずれかです。

<match result>:   結果。"match"または"no-match"です。
```


次の単語は、パターンがエントリと一致した場合にのみ返されます。

     `<index type>`:     "tree" または "list"。内部の検索アルゴリズム。

     `<case>`:           "case-insensitive" または "case-sensitive"。大文字小文字の解釈。

     `<entry matched>`:  match="`<entry>`"。一致したパターンを返す。正規表現と組み合わせて有用。

最後の2つの単語は、返された値とその型を示すために使用されます。"acl" の場合、パターンは存在しません。

     return=nothing:        "map" が存在しないため、返却なし。
     return="`<value>`":      文字列形式で返された値。
     return=cannot-display: 値を文字列に変換できない。

     type="`<type>`":         返されたサンプルの型。

<a id="entry-9-3-get-var"></a>


**`get var <name>`**


```haproxy
get var <name>
```


プロセス全体の変数 'name' の存在、型、内容を表示します。プロセス全体の変数のみが読み取り可能であるため、名前は 'proc.' で始まる必要があります。それ以外の場合は、変数は見つかりません。このコマンドは "operator" または "admin" レベルが必要です。

<a id="entry-9-3-get-weight"></a>


**`get weight <backend>/<server>`**


```haproxy
get weight <backend>/<server>
```


バックエンド `<backend>` のサーバー `<server>` の現在の重みと初期重みを報告するか、いずれかが存在しない場合はエラーを報告します。初期重みは設定ファイルに記載されている重みです。現在の重みが変更されていない限り、両者は通常等しくなります。バックエンドおよびサーバーは、名前またはシャープ記号 ('#') を付加した数値 ID のいずれかで指定できます。

<a id="entry-9-3-help"></a>


**`help [<command>]`**


```haproxy
help [<command>]
```


既知のキーワードと基本的な使い方、または、指定したものにマッチするコマンドの一覧を表示します。未知のコマンドに対しても、同じヘルプ画面を表示します。

<a id="entry-9-3-httpclient"></a>


**`httpclient [--htx] <method> <URI>`**


```haproxy
httpclient [--htx] <method> <URI>
```


HTTPクライアントリクエストを開始し、CLIへレスポンスを出力します。エキスパートモードで動作するCLI接続だけでサポートします（"expert-mode on"を参照）。デバッグ専用です。httpclientは、"default"のresolversセクションを使い、URL内のサーバー名を解決できます。このセクションには、デフォルトで/etc/resolv.confのDNSサーバーを設定します。ただし、/etc/hostsのホストを解決できるローカルDNSデーモンを使わなければ、そこに記載したホストは解決できません。

--htx オプションは、htx_dump() 関数を使用して HAProxy 内部の htx 表現を使用することを可能にします。主にデバッグ用途で使用されます。

<a id="entry-9-3-new-ssl-ca-file"></a>


**`new ssl ca-file <cafile>`**


```haproxy
new ssl ca-file <cafile>
```


空のCAファイルツリーエントリーを新しく作成します。後でCA証明書の集合を設定し、crt-listへ追加するためのものです。このコマンドは、"set ssl ca-file"、"add ssl ca-file"、"add ssl crt-list"と組み合わせて使うべきです。

<a id="entry-9-3-new-ssl-cert"></a>


**`new ssl cert <filename>`**


```haproxy
new ssl cert <filename>
```


空のSSL証明書ストアを新しく作成します。後で証明書を設定し、ディレクトリまたはcrt-listへ追加するためのものです。このコマンドは、"set ssl cert"と"add ssl crt-list"と組み合わせて使うべきです。

<a id="entry-9-3-new-ssl-crl-file"></a>


**`new ssl crl-file <crlfile>`**


```haproxy
new ssl crl-file <crlfile>
```


空のCRLファイルツリーエントリーを新しく作成します。後でCRLの集合を設定し、crt-listへ追加するためのものです。このコマンドは、"set ssl crl-file"と"add ssl crt-list"と組み合わせて使うべきです。

<a id="entry-9-3-prepare-acl"></a>


**`prepare acl <acl>`**


```haproxy
prepare acl <acl>
```


アトミックな置換のため、ACL `<acl>`に新しいバージョン番号を割り当てます。`<acl>`は、"show acl"が返す\#`<id>`または`<name>`です。新しい番号は、応答の"New version created:"の後に表示します。この番号で新しいエントリーの追加を準備し、コミット時に、現在のエントリーをアトミックに置き換えられます。"show acl"では"next_ver"と報告します。より新しいバージョンをコミットすると、使っていないバージョンは自動的に削除するため、新しいバージョンの割り当てによる影響はありません。バージョン番号は、上限で一周する符号なし32ビット値なので、外部プログラムで比較するときには注意が必要です。参照`<acl>`がマップにも使う名前なら、このコマンドは使えず、代わりに"prepare map"を使わなければなりません。

<a id="entry-9-3-prepare-map"></a>


**`prepare map <map>`**


```haproxy
prepare map <map>
```


アトミックな置換のため、マップ`<map>`に新しいバージョン番号を割り当てます。`<map>`は、"show map"が返す\#`<id>`または`<name>`です。新しい番号は、応答の"New version created:"の後に表示します。この番号で新しいエントリーの追加を準備し、コミット時に、現在のエントリーをアトミックに置き換えられます。"show map"では"next_ver"と報告します。より新しいバージョンをコミットすると、使っていないバージョンは自動的に削除するため、新しいバージョンの割り当てによる影響はありません。バージョン番号は、上限で一周する符号なし32ビット値なので、外部プログラムで比較するときには注意が必要です。

<a id="entry-9-3-prompt"></a>


**`prompt [help | n | i | p | timed]*`**


```haproxy
prompt [help | n | i | p | timed]*
```


対話モードの動作と、対話モードで行頭に表示するプロンプトを変更します。- "help"：コマンドの使用法を表示します。- "n"：非対話モードへ切り替えます。- "i"：対話モードへ切り替えます。- "p"：プロンプト付きの対話モードへ切り替えます。- "timed"：プロンプトの時間表示の有無を切り替えます。

オプションがなければ、プロンプトモード、非対話モードの順に循環します。非対話モードでは、現在の行の最後のコマンドが完了すると、接続を閉じます。対話モードでは、コマンドの完了後も閉じず、新しいコマンドを入力できます。プロンプトモードも対話モードとして動き、行頭のプロンプトで、新しいコマンドを待っていることを利用者へ示します。プロンプトは、右山括弧の後に空白を置いた"\> "です。

プロンプトモードは人の操作、対話モードは高度なスクリプト、デフォルトの非対話モードは基本的なスクリプトに適しています。マスターソケットでは、非対話モードを使えない点に注意してください。

<a id="entry-9-3-publish-backend"></a>


**`publish backend <backend>`**


```haproxy
publish backend <backend>
```


バックエンドのインスタンスへのコンテンツ切り替えを有効にします。"unpublish backend"コマンドの逆の操作です。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。

<a id="entry-9-3-quit"></a>


**`quit`**


```haproxy
quit
```


対話モードで、接続を閉じます。

<a id="entry-9-3-set-anon"></a>


**`set anon [on|off] [<key>]`**


```haproxy
set anon [on|off] [<key>]
```


現在のCLIセッションの「匿名化モード」を有効または無効にします。コマンド出力のうち、機密とみなす一部のフィールドをハッシュで置き換えます。開発者が不具合を探す際に要素間の関係を把握できる程度の一貫性は残しつつ、ビット数を十分に少ない24にして、候補が非常に多いため元に戻せないようにします。有効にするときにキーを指定しなければ、グローバルキーを使います。これは、設定ファイルの"anonkey"またはCLIコマンド"set anon global-key"で設定したものです。そのキーもなければ、ランダムに生成します。あるいは、現在のセッションで使う32ビットキーを指定できます。たとえば、前のダンプで使ったキーを再利用して、出力を比較しやすくできます。開発者がこのキーを必要とすることは決してなく、ハッシュの背後にある値の推測を肯定・否定できるおそれがあるため、決して共有しないことを推奨します。

<a id="entry-9-3-set-dynamic-cookie-key-backend"></a>


**`set dynamic-cookie-key backend <backend> <value>`**


```haproxy
set dynamic-cookie-key backend <backend> <value>
```


動的な永続性Cookieの生成に使う秘密キーを変更します。これにより、既存のセッションは維持できなくなります。

<a id="entry-9-3-set-anon-global-key"></a>


**`set anon global-key <key>`**


```haproxy
set anon global-key <key>
```


グローバルな匿名化キーを`<key>`に設定します。0から4294967295までの32ビット整数でなければなりません（0はグローバルキーを無効にします）。管理者権限が必要です。

<a id="entry-9-3-set-map"></a>


**`set map <map> [<key>|#<ref>] <value>`**


```haproxy
set map <map> [<key>|#<ref>] <value>
```


マップ`<map>`の各キー`<key>`に対応する値を変更します。`<map>`は、"show map"が返す\#`<id>`または`<name>`です。`<key>`の代わりに`<ref>`を使うと、`<ref>`が指すエントリーだけを変更します。新しい値は`<value>`です。

<a id="entry-9-3-set-maxconn-frontend"></a>


**`set maxconn frontend <frontend> <value>`**


```haproxy
set maxconn frontend <frontend> <value>
```


指定したフロントエンドのmaxconn設定を動的に変更します。ゼロを含む任意の正の値を指定できますが、グローバルのmaxconnより大きな値にしても、あまり意味はありません。上限を増やし、待機中の接続があれば、直ちに受け入れます。現在の接続数より小さな値へ下げると、そのしきい値に達するまで、新しい接続の受け入れを遅らせます。フロントエンドは、名前、または先頭にシャープ（'#'）を付けた数値IDで指定できます。

<a id="entry-9-3-set-maxconn-server"></a>


**`set maxconn server <backend/server> <value>`**


```haproxy
set maxconn server <backend/server> <value>
```


指定したサーバーのmaxconn設定を動的に変更します。ゼロを含む任意の正の値を指定できますが、グローバルのmaxconnより大きな値にしても、あまり意味はありません。

<a id="entry-9-3-set-maxconn-global"></a>


**`set maxconn global <maxconn>`**


```haproxy
set maxconn global <maxconn>
```


最初のグローバルmaxconn設定で定めた範囲内で、グローバルmaxconnを動的に変更します。増やしたときに待機中の接続があれば、直ちに受け入れます。現在の接続数より小さな値へ下げると、そのしきい値に達するまで、新しい接続の受け入れを遅らせます。ゼロにすると、初期設定へ戻します。

<a id="entry-9-3-set-profiling-memory"></a>


**`set profiling memory { on | off }`**


```haproxy
set profiling memory { on | off }
set profiling tasks { auto | on | off | lock | no-lock | memory | no-memory }
```


指定したサブシステムのCPUまたはメモリーのプロファイリングを、有効または無効にします。設定ファイルの"global"セクションの"profiling"設定を、設定または解除するのと同等です。"show profiling"も参照してください。タスクのプロファイリングを手動で"on"にすると、スケジューラーの統計を自動的にリセットするため、一定期間の活動を確認できます。メモリーのプロファイリングは、一部のOSに限られ（linux-glibcターゲットで動作が確認されています）、コンパイル時にUSE_MEMORY_PROFILINGを設定する必要があります。

タスクのプロファイリングでは、タスクごとのロックとメモリーの所要時間の収集を、実行時に有効・無効にできます。ただし、変更を反映するのは、プロファイラーが次にoff/autoからonへ切り替わるときだけです（自動でも手動でも同じです）。したがって、"no-lock"でタスクごとのロックのプロファイリングを無効にし、CPUサイクルを節約する場合は、変更を反映するため、タスクのプロファイリングを一度offにしてからonに戻すことを推奨します。

<a id="entry-9-3-set-rate-limit-connections-global"></a>


**`set rate-limit connections global <value>`**


```haproxy
set rate-limit connections global <value>
```


グローバル設定'maxconnrate'で定める、プロセス全体の接続レート上限を変更します。ゼロは制限を無効にします。すべてのフロントエンドに適用し、変更は即座に有効になります。値は毎秒の接続数で渡します。

<a id="entry-9-3-set-rate-limit-http-compression-global"></a>


**`set rate-limit http-compression global <value>`**


```haproxy
set rate-limit http-compression global <value>
```


グローバル設定'maxcomprate'で定める、圧縮入力レートの上限を変更します。ゼロは制限を無効にします。値は毎秒のキロバイト数で渡します。"show info"の"CompressBpsRateLim"行では、バイト単位の値を確認できます。

<a id="entry-9-3-set-rate-limit-sessions-global"></a>


**`set rate-limit sessions global <value>`**


```haproxy
set rate-limit sessions global <value>
```


グローバル設定'maxsessrate'で定める、プロセス全体のセッションレート上限を変更します。ゼロは制限を無効にします。すべてのフロントエンドに適用し、変更は即座に有効になります。値は毎秒のセッション数で渡します。

<a id="entry-9-3-set-rate-limit-ssl-sessions-global"></a>


**`set rate-limit ssl-sessions global <value>`**


```haproxy
set rate-limit ssl-sessions global <value>
```


グローバル設定'maxsslrate'で定める、プロセス全体のSSLセッションレート上限を変更します。ゼロは制限を無効にします。すべてのフロントエンドに適用し、変更は即座に有効になります。値は、SSLスタックへ毎秒送るセッション数で渡します。ハンドシェイクの悪用からスタックを守るため、ハンドシェイクの前に適用します。

<a id="entry-9-3-set-server"></a>


**`set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]`**


```haproxy
set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]
```


サーバーの現在のIPアドレスを、指定したものに置き換えます。任意で、'port'パラメーターでポートも変更できます。ヘルスチェック用のポートを設定している場合だけ、ポート変更時に、ポートマッピング（+Xまたは-Y表記）への切り替えや、その逆もサポートする点に注意してください。

<a id="entry-9-3-set-server-2"></a>


**`set server <backend>/<server> agent [ up | down ]`**


```haproxy
set server <backend>/<server> agent [ up | down ]
```


サーバーのエージェントを、新しい状態へ強制的に変更します。たとえば、遅いエージェントチェックにかかわらず、サーバーの状態を直ちに切り替えるのに便利です。追跡しているサーバーがあれば、変更を伝播する点に注意してください。

<a id="entry-9-3-set-server-3"></a>


**`set server <backend>/<server> agent-addr <addr> [port <port>]`**


```haproxy
set server <backend>/<server> agent-addr <addr> [port <port>]
```


サーバーのエージェントチェックのアドレスを変更します。実行中に別のアドレスへ移せます。IPアドレスとホスト名のいずれも指定でき、名前解決します。任意で、エージェントのポートも変更できます。

<a id="entry-9-3-set-server-4"></a>


**`set server <backend>/<server> agent-port <port>`**


```haproxy
set server <backend>/<server> agent-port <port>
```


エージェントチェックに使うポートを変更します。

<a id="entry-9-3-set-server-5"></a>


**`set server <backend>/<server> agent-send <value>`**


```haproxy
set server <backend>/<server> agent-send <value>
```


エージェントチェックの宛先へ送るエージェント文字列を変更します。サーバーのアドレス変更とともに文字列を更新し、両者の対応を保てます。

<a id="entry-9-3-set-server-6"></a>


**`set server <backend>/<server> health [ up | stopping | down ]`**


```haproxy
set server <backend>/<server> health [ up | stopping | down ]
```


サーバーのヘルス状態を、新しい状態へ強制的に変更します。たとえば、遅いヘルスチェックにかかわらず、サーバーの状態を直ちに切り替えるのに便利です。追跡しているサーバーがあれば、変更を伝播する点に注意してください。

<a id="entry-9-3-set-server-7"></a>


**`set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]`**


```haproxy
set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]
```


サーバーのヘルスチェックに使うIPアドレスを変更します。任意で、ヘルスチェックのポートも変更できます。

<a id="entry-9-3-set-server-8"></a>


**`set server <backend>/<server> check-port <port>`**


```haproxy
set server <backend>/<server> check-port <port>
```


ヘルスチェックに使うポートを`<port>`へ変更します。

<a id="entry-9-3-set-server-9"></a>


**`set server <backend>/<server> state [ ready | drain | maint ]`**


```haproxy
set server <backend>/<server> state [ ready | drain | maint ]
```


サーバーの管理状態を、新しい状態へ強制的に変更します。サーバーへの負荷分散や、あらゆるトラフィックを無効にするのに便利です。"ready"にすると通常のモードになり、"enable server"コマンドと同等です。"maint"にすると、そのサーバーへのすべてのトラフィックとヘルスチェックを無効にし、"disable server"コマンドと同等です。"drain"は、サーバーを負荷分散から外すだけで、チェックの実行と、永続性による新規接続の受け入れは引き続き許可します。追跡しているサーバーがあれば、変更を伝播します。

<a id="entry-9-3-set-server-10"></a>


**`set server <backend>/<server> weight <weight>[%]`**


```haproxy
set server <backend>/<server> weight <weight>[%]
```


サーバーの重みを、引数で指定した値に変更します。後述の"set weight"コマンドと、まったく同等です。

<a id="entry-9-3-set-server-11"></a>


**`set server <backend>/<server> fqdn <FQDN>`**


```haproxy
set server <backend>/<server> fqdn <FQDN>
```


サーバーのFQDNを、引数で指定した値に変更します。このサーバーについて、内部の実行時DNSリゾルバーを設定し、有効にしておく必要があります。

<a id="entry-9-3-set-server-12"></a>


**`set server <backend>/<server> ssl [ on | off ]  (非推奨)`**


```haproxy
set server <backend>/<server> ssl [ on | off ]  (非推奨)
```


このオプションは、サーバーへの送信接続のSSL暗号化を設定します。無効にすると、すべてのトラフィックが平文になります。ヘルスチェックの経路は変えません。

このコマンドは非推奨です。代わりに、"add server"コマンドで、SSLを使う、または使わない新しいサーバーを動的に作成してください。

<a id="entry-9-3-set-severity-output"></a>


**`set severity-output [ none | number | string ]`**


```haproxy
set severity-output [ none | number | string ]
```


現在のセッションの間、接続先の統計ソケットの重大度の出力形式を変更します。

<a id="entry-9-3-set-ssl-ca-file"></a>


**`set ssl ca-file <cafile> <payload>`**


```haproxy
set ssl ca-file <cafile> <payload>
```


このコマンドはトランザクションシステムの一部で、"commit ssl ca-file"や"abort ssl ca-file"コマンドが必要になる場合があります。進行中のトランザクションがなければ、ペイロード内の証明書を保存するCAファイルツリーのエントリーを作成します。エントリーをCAファイルツリーには保存せず、一時的なトランザクションの中だけで保持します。同名のファイルに対するトランザクションが既にあれば、前のCAファイルエントリーを削除し、新しいもので置き換えます。変更を終えたら、"commit ssl ca-file"を呼び出してコミットしなければなりません。複数の証明書を別々に追加するには、"add ssl ca-file"コマンドを使えます。

例：

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```


<a id="entry-9-3-set-ssl-cert"></a>


**`set ssl cert <filename> <payload>`**


```haproxy
set ssl cert <filename> <payload>
```


このコマンドはトランザクションシステムの一部で、"commit ssl cert"や"abort ssl cert"コマンドが必要になる場合があります。このシステム全体は、"show ssl cert"が表示するすべての証明書、つまりフロントエンドとバックエンドのいずれの証明書にも対応します。進行中のトランザクションがなければ、証明書`<filename>`をメモリー内で一時トランザクションへ複製し、ペイロードのPEMファイルで更新します。同名のファイルのトランザクションがあれば、それを更新します。証明書に関連付けられたファイル（.issuer、.sctl、.ocspなど）も更新できます。変更を終えたら、"commit ssl cert"でトランザクションをコミットしなければなりません。

空行でペイロードの終了を通知するため、CLIからファイルを投入する際には注意が必要です。不要な部分を取り除いたPEMファイルの投入を推奨します。簡単な方法は、空行をすべて削除し、PEMセクションの内容だけを残すことです。sedコマンドで実現できます。

例：

```haproxy
# With some simple sanitizing
 echo -e "set ssl cert localhost.pem <<\n$(sed -n '/^$/d;/-BEGIN/,/-END/p' 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -

 # Complete example with commit
 echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.issuer <<\n $(cat 127.0.0.1.pem.issuer)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.ocsp <<\n$(base64 -w 1000 127.0.0.1.pem.ocsp)\n" | \
 socat /var/run/haproxy.stat -
 echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```


<a id="entry-9-3-set-ssl-crl-file"></a>


**`set ssl crl-file <crlfile> <payload>`**


```haproxy
set ssl crl-file <crlfile> <payload>
```


このコマンドはトランザクションシステムの一部で、"commit ssl crl-file"や"abort ssl crl-file"コマンドが必要になる場合があります。進行中のトランザクションがなければ、ペイロード内の失効リストを保存するCRLファイルツリーのエントリーを作成します。エントリーをCRLファイルツリーには保存せず、一時トランザクションの中だけで保持します。同名のファイルに対するトランザクションが既にあれば、前のCRLファイルエントリーを削除し、新しいもので置き換えます。変更を終えたら、"commit ssl crl-file"を呼び出してコミットしなければなりません。

例：

```text
echo -e "set ssl crl-file crlfile.pem <<\n$(cat rootCRL.pem)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl crl-file crlfile.pem" | socat /var/run/haproxy.stat -
```


<a id="entry-9-3-set-ssl-ech"></a>


**`set ssl ech <bind> <payload>`**


```haproxy
set ssl ech <bind> <payload>
```


bind行のECHキーを、このキーで置き換えます。ペイロードはECH用のPEM形式でなければなりません。
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

bind行の形式は`<frontend>`/@`<filename>`:`<linenum>`（例：frontend1/@haproxy.conf:19）です。"name"キーワードでbind行に名前を付けた場合は、`<frontend>`/`<name>`形式も使えます。

OpenSSL のバージョンが ECH をサポートしている必要があり、HAProxy は USE_ECH=1 でコンパイルされている必要があります。このコマンドは、実験モードで実行されている CLI 接続でのみサポートされます（「experimental-mode on」を参照）。

"show ssl ech"、"add ssl ech"と、設定マニュアルの[セクション5.1](/ja/docs/haproxy/bind-and-server-options/#section-5-1)にある"ech"も参照してください。

    $ openssl ech -public_name foobar.com -out foobar3.com.ech
    $ echo -e "experimental-mode on;
               set ssl ech frontend1/@haproxy.conf:19 <<%EOF%&#92;n$(cat foobar3.com.ech)&#92;n%EOF%&#92;n" | &#92;
      socat /tmp/haproxy.sock -
    set new ECH configs for frontend1/@haproxy.conf:19

<a id="entry-9-3-set-ssl-ocsp-response"></a>


**`set ssl ocsp-response <response | payload>`**


```haproxy
set ssl ocsp-response <response | payload>
```


証明書のOCSPレスポンスを更新します（"bind"行の"crt"を参照）。最初のレスポンス読み込みと同じ検査を行います。`<response>`には、OCSPサーバーからのDER形式のレスポンスを、base64符号化した文字列で渡さなければなりません。BoringSSLでは、このコマンドをサポートしません。

例：

```text
openssl ocsp -issuer issuer.pem -cert server.pem \
             -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | \
             socat stdio /var/run/haproxy.stat

ペイロード構文を使用する場合:
echo -e "set ssl ocsp-response <<\n$(base64 resp.der)\n" | \
             socat stdio /var/run/haproxy.stat
```


<a id="entry-9-3-set-ssl-tls-key"></a>


**`set ssl tls-key <id> <tlskey>`**


```haproxy
set ssl tls-key <id> <tlskey>
```


`<id>`リスナーの次のTLSキーを`<tlskey>`に設定します。このキーは最後のキーになり、その一つ前のキーを暗号化に使います（他のキーは復号だけに使います）。存在する最も古いTLSキーを上書きします。`<id>`は、"show tls-keys"が返す数値の\#`<id>`、または`<file>`です。`<tlskey>`は、base64符号化した48または80バイトのTLSチケットキーです（例：openssl rand 80 \| openssl base64 -A）。

<a id="entry-9-3-set-table"></a>


**`set table <table> key <key> [data.<data_type> <value>]*`**


```haproxy
set table <table> key <key> [data.<data_type> <value>]*
set table <table> ptr <ptr> [data.<data_type> <value>]*
```


テーブル内のスティックテーブルのエントリーを作成、または更新します。キーがなければ、エントリーを挿入します。`<data_type>`で使える全値は、セクション4.2のstick-tableを参照してください。最も想定される用途は、送信元IPアドレスのエントリーを動的に登録し、gpc0のフラグでIPアドレスを動的に遮断したり、サービス品質に影響を与えたりすることです。一度の呼び出しで、複数のdata_typesを渡せます。

既存のエントリーについては、キーによる検索の代わりに、任意でptr検索を使えます。`<ptr>`は0xffff形式で書き、以前の"show table"が返したアドレスに対応していなければなりません。空のキーやCLIで扱えない文字のためにキーでマッチできない場合、ポインターでエントリーをマッチさせる方法が有効な場合があります。

data.`<data_type>`が配列型なら、"[]"で特定のインデックスへアクセスできます。たとえば、data.gpt[1]です。

<a id="entry-9-3-set-timeout-cli"></a>


**`set timeout cli <delay>`**


```haproxy
set timeout cli <delay>
```


現在の接続のCLIインターフェースのタイムアウトを変更します。長いデバッグセッションで、切断されずに指標を継続して確認したい場合に便利です。遅延時間は秒で渡します。

<a id="entry-9-3-set-var"></a>


**`set var <name> <expression>`**


```haproxy
set var <name> <expression>
set var <name> expr <expression>
set var <name> fmt <format>
```


式`<expression>`または形式文字列`<format>`の結果で、プロセス全体の変数'name'を設定、または上書きできます。使えるのはプロセス全体の変数だけなので、名前は'proc.'で始まらなければならず、そうでなければ変数を設定しません。`<expression>`と`<format>`に含められるのは、"internal"サンプル取得キーワードとコンバーターだけですが、便利なのは主にstr('something')、int()、単純な文字列、他の変数への参照でしょう。コマンド行パーサーは引用符を認識しないため、式の中の空白の前には、必ずバックスラッシュを付けなければなりません。"operator"または"admin"レベルが必要です。このコマンドをサポートするのは、実験モードのCLI接続だけです（"experimental-mode on"を参照）。

<a id="entry-9-3-set-weight"></a>


**`set weight <backend>/<server> <weight>[%]`**


```haproxy
set weight <backend>/<server> <weight>[%]
```


サーバーの重みを、引数で指定した値に変更します。値が'%'で終わる場合、新しい重みは初期設定の重みに対する相対値になります。絶対値は0から256まで指定できます。相対値は正でなければならず、結果の絶対値は256を上限とします。静的ロードバランシングアルゴリズムで動くサーバー群に属するサーバーには、設定後に重みを変更できないため、より厳しい制限があります。受け付ける値は0と100%だけです（または0と初期の重み）。変更は即座に有効になりますが、一部の負荷分散アルゴリズムでは、変更を反映するまでに一定数のリクエストが必要です。典型的な用途は、更新中に重みをゼロにしてサーバーを無効にし、更新後に100%へ戻して再び有効にすることです。このコマンドは制限されており、"admin"レベルを設定したソケットからだけ実行できます。バックエンドとサーバーは、いずれも名前、または先頭にシャープ（'#'）を付けた数値IDで指定できます。

<a id="entry-9-3-show-acl"></a>


**`show acl [[@<ver>] <acl>]`**


```haproxy
show acl [[@<ver>] <acl>]
```


ACLコンバーターの情報を出力します。引数がなければ、使用可能な全ACLの一覧を返します。`<acl>`を指定すれば、その内容を出力します。`<acl>`は\#`<id>`または`<name>`です。デフォルトでは、現在のACLバージョンを表示します。これは、現在マッチングに使い、ACL一覧で'curr_ver'と報告するバージョンです。ACL識別子の前に'@`<ver>`'を付けると、他のバージョンも出力できます。バージョンはフィルターとして働き、存在しないバージョンは、単に結果を返しません。出力形式は、サンプル値も含めてマップと同じです。返すデータは、使用可能なACLの一覧ではなく、いずれかのACLを構成する全パターンの一覧です。多くのパターンは、マップと共有できます。'entry_cnt'は、有効なものだけでなく、追加中のものも含む、ACLの全エントリー数を表します。

<a id="entry-9-3-show-anon"></a>


**`show anon`**


```haproxy
show anon
```


匿名化モードの現在の状態（有効または無効）と、現在のセッションのキーを表示します。

<a id="entry-9-3-show-backend"></a>


**`show backend`**


```haproxy
show backend
```


実行中のプロセスで使用できるバックエンドの一覧を出力します。

<a id="entry-9-3-show-cli-level"></a>


**`show cli level`**


```haproxy
show cli level
```


現在のCLIセッションのCLIレベルを表示します。結果は'admin'、'operator'、'user'のいずれかです。'operator'と'user'コマンドも参照してください。

例：

```shell
$ socat /tmp/sock1 readline
prompt
> operator
> show cli level
operator
> user
> show cli level
user
> operator
Permission denied
```


<a id="entry-9-3-operator"></a>


**`operator`**


```haproxy
operator
```


現在のCLIセッションのCLIレベルをoperatorへ下げます。上げることはできません。エキスパートモードと実験モードも解除します。"show cli level"も参照してください。

<a id="entry-9-3-unpublish-backend"></a>


**`unpublish backend <backend>`**


```haproxy
unpublish backend <backend>
```


バックエンドを、今後のトラフィックの選択対象外にします。実際には、そのバックエンドを参照するuse_backend / default_backendルールを無視し、次のコンテンツ切り替えルールを評価します。無効化したバックエンドとは異なり、サーバーのヘルスチェックは有効なままです。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。

<a id="entry-9-3-user"></a>


**`user`**


```haproxy
user
```


現在のCLIセッションのCLIレベルをuserへ下げます。上げることはできません。エキスパートモードと実験モードも解除します。"show cli level"も参照してください。

<a id="entry-9-3-show-activity"></a>


**`show activity [-1 | 0 | thread_num]`**


```haproxy
show activity [-1 | 0 | thread_num]
```


内部イベントのカウンターを報告します。開発者や、より一般にはhaproxyを十分に知る人が、報告された異常な動作の原因を絞り込むのに役立ちます。典型例は、正常に動くプロセスがまったくスリープせず、CPUを100%使う場合です。出力は指標ごとに一行で、スレッドごとのカウンターを同じ行に並べます。カウンターは32ビットで、プロセスの生存期間中に一周しますが、通常はこのコマンドを二度呼び出すため、問題ありません。フィールドの正確な意味を、カウンターを更新するコードで確認するよう、意図的に文書化していません。"clear counters"コマンドでも値をリセットします。マルチスレッド構成では、最初の列に全スレッドの合計（指標の性質によっては平均）を示し、全スレッドの値を、スレッドの順に角括弧内へ並べます。任意で、出力するスレッド番号を引数に指定できます。特別な値"0"は集計値（最初の列）を報告し、デフォルトの"-1"は全列を表示します。一列だけを要求した場合は、シングルスレッドモードと同様に、括弧を付けない点に注意してください。

<a id="entry-9-3-show-cli-sockets"></a>


**`show cli sockets`**


```haproxy
show cli sockets
```


CLIソケットの一覧を表示します。出力は、空白で区切った3フィールドです。最初のフィールドは、UNIXソケット、IPv4のアドレス:ポート、IPv6のアドレス:ポートのいずれかのソケットアドレスです。他の種類のソケットは出力しません。二番目は、ソケットのレベル（'admin'、'user'、'operator'）です。最後は、ソケットをバインドしているプロセスをカンマ区切りで並べ、数値または'all'を使います。

例：

```shell
$ echo 'show cli sockets' | socat stdio /tmp/sock1
# socket lvl processes
/tmp/sock1 admin all
127.0.0.1:9999 user 2,3,4
127.0.0.2:9969 user 2
[::1]:9999 operator 2
```


<a id="entry-9-3-show-cache"></a>


**`show cache`**


```haproxy
show cache
```


設定したキャッシュと、各キャッシュツリーに保存したオブジェクトを一覧にします。

\$ echo 'show cache' \| socat stdio /tmp/sock1 0x7f6ac6c5b03a: foobar (shctx:0x7f6ac6c5b000,
available blocks:3918) 1 2 3 4

1. キャッシュ構造体へのポインター
2. キャッシュ名
3. mmap領域（shctx）へのポインター
4. shctx内の再利用できるブロック数

0x7f6ac6c5b4cc hash:286881868 vary:0x0011223344556677 size:39114 (39 blocks), refcount:9, expire:237
1 2 3 4 5 6 7

1. キャッシュエントリーへのポインター
2. ハッシュの先頭32ビット
3. varyがある場合の、エントリーの二次ハッシュ
4. オブジェクトのサイズ（バイト）
5. オブジェクトに使うブロック数
6. エントリーを使用中のトランザクション数
7. 有効期限までの時間。期限切れなら、負の場合があります。

<a id="entry-9-3-show-dev"></a>


**`show dev`**


```haproxy
show dev
```


HAProxyの開発者が問題の原因を詳しく理解するために必要とする情報を、まとめて提供するコマンドです。通常、利用者に役立つ情報ではありませんが、開発者がいくつかの仮説を除外するのに役立ちます。形式は、おおむね、インデントした行を含むセクションの列で、一行に一項目を示します。OSの種類とバージョン、CPUの種類、起動時のFD上限などです。値が無制限など、情報として意味を持たないフィールドは、繰り返しや出力の煩雑さを避けるため省略します。将来は、項目を増やしたり変えたりする場合があります。スクリプトで解析するための出力ではなく、強く信頼すべきものでもありません。主な目的は、読める人の時間を節約することです。

技術的には、起動時にこれらの情報をまとめて保存した内部構造体から、そのまま取り出しています。クラッシュ後のコアファイルにも残るようにするためです。そのため開発者は、コアダンプの内容と比較したり、複数のリロード間で比較したりするために、正常に動くプロセスの早い段階の出力を求めることがあります（上限などが変わる場合があります）。匿名化を有効にしていれば、ノード名など、機密性があり得る値も匿名化します。

出力例：

```shell
$ socat stdio /tmp/sock1 <<< "show dev"
Platform info
  machine vendor: To be filled by O.E.M
  machine family: Altra
  cpu model: Impl 0x41 Arch 8 Part 0xd0c r3p1
  virtual machine: no
  container: no
  OS name: Linux
  OS release: 6.2.0-36-generic
  OS version: #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 18:01:07 UTC 2
  OS architecture: aarch64
  node name: 489aaf
Process info
  pid: 1735846
  boot uid: 509
  boot gid: 1002
  fd limit (soft): 1024
  fd limit (hard): 1048576
```


<a id="entry-9-3-show-env"></a>


**`show env [<name>]`**


```haproxy
show env [<name>]
```


プロセスが認識する環境変数を、一つまたはすべて出力します。引数がなければすべてを、引数があれば、指定した変数が存在する場合に限り、それだけを出力します。なければ"Variable not found"を出力します。変数の形式は、保存時や"env"ユーティリティの出力と同じ"`<name>`=`<value>`"です。環境変数を多用する設定ファイルのデバッグで、期待する値が入っていることを確認するのに便利です。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。

<a id="entry-9-3-show-errors"></a>


**`show errors [<iid>|<proxy>] [request|response]`**


```haproxy
show errors [<iid>|<proxy>] [request|response]
```


フロントエンドとバックエンドが収集した、最後に認識したHTTP/1.xのリクエストとレスポンスのエラーを出力します。`<iid>`を指定すると、IDが`<iid>`のフロントエンドまたはバックエンドに関係するエラーだけに絞ります。プロキシIDに"-1"を指定すると、全インスタンスを出力します。代わりにプロキシ名を指定すれば、そのIDをフィルターに使います。プロキシ名またはIDの後に"request"または"response"を付けると、リクエストまたはレスポンスのエラーだけを出力します。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。

収集できるのは、プロトコル違反による最後のリクエストとレスポンスのエラーで、よくある原因は、ヘッダー名の不正な文字です。どの文字がプロトコルに違反したかを、正確に報告します。エラーを検出した正確な日時、フロントエンド名とバックエンド名、分かればサーバー名、内部トランザクションID、セッションを開始した送信元アドレスといった重要な情報も報告します。

すべての文字を返し、印字できない文字は符号化します。よく使うもの（&#92;t = 9、&#92;n = 10、&#92;r = 13、&#92;e = 27）は、バックスラッシュの後に一文字を付けます。混同しないよう、バックスラッシュ自体は'&#92;&#92;'にします。他の印字できない文字は'&#92;xNN'とし、NNは、その文字のASCIIコードを二桁の16進数で表したものです。

各行の前に、バッファーの先頭を0とする、その行の最初の文字の位置を付けます。出力一行に含める入力行は最大一行で、長い行は連続する複数の出力行に分割し、幅が79文字を超えないようにします。分割した行は'&#92;n'で終わらず、次の行のオフセットの後に、前の行からの続きであることを示す'+'が付くため、容易に見分けられます。

例：

```shell
    $ echo "show errors -1 response" | socat stdio /tmp/sock1
>>> [04/Mar/2009:15:46:56.081] backend http-in (#2): invalid response
      src 127.0.0.1, session #54, frontend fe-eth0 (#1), server s2 (#1)
      response length 213 bytes, error at position 23:

      00000  HTTP/1.0 200 OK\r\n
      00017  header/bizarre:blah\r\n
      00038  Location: blah\r\n
      00054  Long-line: this is a very long line which should b
      00104+ e broken into multiple lines on the output buffer,
      00154+  otherwise it would be too large to print in a ter
      00204+ minal\r\n
      00211  \r\n

上の例では、内部IDが2のバックエンド"http-in"が、内部IDが1のサーバーs2からの
不正なレスポンスをブロックしています。このリクエストは、送信元127.0.0.1が開始し、
IDが1のフロントエンドfe-eth0が受信したトランザクション54（ここでは"session"と呼んでいます）
に属します。エラー検出時のレスポンス全体の長さは213バイトで、エラーはバイト位置23に
ありました。これはヘッダー名"header/bizarre"のスラッシュ（'/'）です。
スラッシュは、HTTPのヘッダー名に使える有効な文字ではありません。
```


<a id="entry-9-3-show-events"></a>


**`show events [<sink>] [-w] [-n] [-0] [-s]`**


```haproxy
show events [<sink>] [-w] [-n] [-0] [-s]
```


オプションがなければ、既知の全イベント出力先とその種類を一覧にします。指定があれば、指定した出力先がバッファー型の場合、その中の利用可能なイベントをすべて出力します。出力先名の後に"-w"を指定すると、バッファーの末尾に達した後、新しいイベントを待って表示します。任意の入力を送る（その入力は破棄します）か、セッションを閉じると停止できます。"-n"は、バッファーの末尾へ直接移動します。"-w"と組み合わせ、新しいイベントだけを報告すると便利なことがよくあります。便宜上、"-wn"または"-nw"で、両方を同時に有効にできます。デフォルトでは、すべてのイベントを改行文字（'&#92;n'、10、または0x0A）で区切ります。"-0"引数を渡すと、NUL文字（'&#92;0'または0）へ変更できます。"-s"オプションは出力を無害化し、キャプチャまたはデコードしたデータのバイナリ内容が端末の表示を変えないようにします。空白文字（スペースとタブ）はスペースに置き換え、各レコードが一行に収まるようにします。それ以外の制御文字（0x00から0x1F、および0x7F）と非ASCII文字（0x80以上）は'?'に置き換えます。出力の長さは保持します。これにより、リングの出力でANSIエスケープシーケンスや文字方向の制御コードが操作担当者の端末に挿入されることを防ぎます。端末に出力する場合や、入力を特殊なものとして解釈してはならないプログラムへ渡す場合に便利です。たとえば、出力をそのままレポートにコピーする監視スクリプトが該当します。

<a id="entry-9-3-show-fd"></a>


**`show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]`**


```haproxy
show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]
```


開いている全ファイルディスクリプター、または指定した番号`<fd>`だけを一覧にして出力します。"`<tgid>`/`<fd>`"形式も受け付け、左右いずれの側も、空ならワイルドカードとして扱います（"/`<fd>`"はスレッドグループをまたぐfd `<fd>`、"`<tgid>`/"は`<tgid>`の全fd）。現在は`<tgid>`を解析しても無視し、スレッドグループごとのfdテーブルの将来の対応を待っています。任意でフラグを指定し、特定の種類のFDだけに絞ったり、特定の種類を除いたりできます。'-'または'!'があると、同じ引数の後続文字の選択を反転します。反転状態は、空白で区切った各引数の前にリセットします。選べるFDの種類は、'p'がパイプ、'l'がリスナー、'c'が接続（全種類）、'f'がフロントエンド接続、'b'がバックエンド接続（全種類）、's'がサーバーへの接続、'd'が"dispatch"アドレスまたはバックエンドの透過アドレスへの接続です。したがって、'b'は'sd'、'c'は'fb'または'fsd'の短縮形です。'c!f'は'b'と同等です（「フロントエンド以外の全接続」は、バックエンド接続だからです）。CPUの異常な使用率など、複雑な問題のデバッグで内部状態を観察する開発者だけを対象とします。一行に一つのfdを報告し、まずポーラー内の状態を、有効なフラグは大文字、無効なものは小文字で示します。"P"はポーリング対象、"R"は準備完了、"A"はアクティブを表します。イベント状態は、"H"が切断、"E"がエラー、"O"が出力、"P"が優先、"I"が入力です。他にも、"N"は新規（fdキャッシュへ追加した直後）、"U"は更新済み（fdキャッシュ内で更新を受信）、"L"は"linger_risk"、"C"は複製済みを示します。その後に、キャッシュ内のエントリー位置、内部の所有者へのポインター、I/Oコールバックへのポインターと、分かればその名前を示します。所有者が接続なら、接続フラグと宛先（フロントエンド、プロキシ、サーバー）を、リスナーなら、その状態とフロントエンドを報告します。内部をよく理解せずに使っても意味がありません。出力形式は変わり得るため、長期間使うツールで解析してはなりません。内部構造の状態を、一覧化する関数が不審と判断した場合、出力行の末尾に感嘆符（'!'）を付けます。障害を診断する際の手掛かりになる場合があります。

<a id="entry-9-3-show-info"></a>


**`show info [typed|json] [desc] [float]`**


```haproxy
show info [typed|json] [desc] [float]
```


現在のプロセスのhaproxyの状態情報を出力します。任意の引数"typed"を渡すと、フィールド番号、名前、型も出力します。外部の監視製品が、未知のフィールドの情報でも、容易に取得し、必要なら集計し、報告できるようにするためです。各フィールドを独立した行に出力します。任意の引数"json"を渡すと、"typed"と同じ情報を、JSONオブジェクトの一覧としてJSON形式で提供します。デフォルトの形式は、コロン（':'）で区切った二列だけで、左がフィールド名、右が値です。型付き出力では、一つのオブジェクトの情報を連続して出力するため、利用する側がすべてを一度に保存する必要がない点が非常に重要です。任意の引数"float"を渡すと、精度を高めるため、通常は整数で出力する一部のフィールドが浮動小数点数に変わる場合があります。対象は将来変わり得るため、意図的に規定していません。このオプションを使う側は、浮動小数点数を処理できる必要があります。出力形式はsprintf("%f")です。

型付き出力では、各行はコロン（':'）で区切った4列です。最初の列は、ドットで区切った3要素の列です。最初の要素は、ゼロから始まる、一覧内のフィールドの数値位置です。この位置は将来も変更してはなりませんが、ビルドオプションや将来のフィールド削除により、欠番が生じることは想定してください。二番目の要素は、デフォルトの"show info"出力に現れるフィールド名です。三番目は、1から始まる相対プロセス番号です。

最初のコロンより後は、上の節で説明した「型付き出力形式」に従います。つまり、二番目の列（最初の':'の後）は、変数の生成元、性質、スコープを示します。三番目はフィールドの型で、"s32"、"s64"、"u32"、"u64"、"str"のいずれかです。四番目は値そのものです。利用する側は、列3から解析方法を、列2から処理方法を判断できます。

したがって、型付きモードでの行全体の形式は次のとおりです。

```text
<field_pos>.<field_name>.<process_num>:<tags>:<type>:<value>
```


コマンドに"desc"を付けると、コロンをもう一つ追加し、その後に、指標の説明を引用符付き文字列で付けます。執筆時点では、"typed"とデフォルトの出力形式だけでサポートします。

例：

```shell
> show info
Name: HAProxy
Version: 1.7-dev1-de52ea-146
Release_date: 2016/03/11
Nbproc: 1
Process_num: 1
Pid: 28105
Uptime: 0d 0h00m04s
Uptime_sec: 4
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
(...)

> show info typed
0.Name.1:POSV:str:HAProxy
1.Version.1:POSV:str:3.1-dev0-7c653d-2466
2.Release_date.1:POSV:str:2025/07/01
3.Nbthread.1:CGSV:u32:1
4.Nbproc.1:CGSV:u32:1
5.Process_num.1:KGPV:u32:1
6.Pid.1:SGPV:u32:638069
7.Uptime.1:MDPV:str:0d 0h00m07s
8.Uptime_sec.1:MDPV:u32:7
9.Memmax_MB.1:CLPV:u32:0
10.PoolAlloc_MB.1:MGPV:u32:0
11.PoolUsed_MB.1:MGPV:u32:0
12.PoolFailed.1:MCPV:u32:0
(...)
```


型付き形式は、最初の列の末尾にプロセスIDがあるため、複数のプロセスの出力を目で見て容易に集約できます。例：

```shell
$ ( echo show info typed | socat /var/run/haproxy.sock1;    \
    echo show info typed | socat /var/run/haproxy.sock2 ) |  \
  sort -t . -k 1,1n -k 2,2 -k 3,3n
0.Name.1:POS:str:HAProxy
0.Name.2:POS:str:HAProxy
1.Version.1:POS:str:1.7-dev1-868ab3-148
1.Version.2:POS:str:1.7-dev1-868ab3-148
2.Release_date.1:POS:str:2016/03/11
2.Release_date.2:POS:str:2016/03/11
3.Nbproc.1:CGS:u32:2
3.Nbproc.2:CGS:u32:2
4.Process_num.1:KGP:u32:1
4.Process_num.2:KGP:u32:2
5.Pid.1:SGP:u32:30120
5.Pid.2:SGP:u32:30121
6.Uptime.1:MDP:str:0d 0h01m28s
6.Uptime.2:MDP:str:0d 0h01m28s
(...)
```


JSON出力の形式は、"show schema json"で出力できるスキーマに記述されています。

出力量を減らすため、JSON出力には余分な空白がありません。人が読む場合は、整形ツールに通すと便利です。例：

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

出力量を減らすため、JSON出力には余分な空白がありません。人が読む場合は、整形ツールに通すと便利です。例：

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-libs"></a>


**`show libs`**


```haproxy
show libs
```


対応するシステムでは、読み込んだ共有動的ライブラリとオブジェクトファイルを一覧にして出力します。取得できる場合、各共有オブジェクトについて、仮想アドレスの範囲、サイズ、パスを示します。たとえば、ダンプに現れた関数をどのライブラリが提供するかの見当を付けるのに使えます。多くのシステムでは、再起動のたびにアドレスが変わるため（アドレス空間のランダム化）、コアファイルの解析に使う予定なら、起動時に一覧を取得しておく必要があります。このコマンドは、"operator"または"admin"レベルを設定したソケットからだけ実行できます。出力形式はOS、アーキテクチャー、さらにはhaproxyのバージョンによっても変わり得るため、スクリプトで依存するべきではありません。

<a id="entry-9-3-show-map"></a>


**`show map [[@<ver>] <map>]`**


```haproxy
show map [[@<ver>] <map>]
```


マップコンバーターの情報を出力します。引数がなければ、使用可能な全マップの一覧を返します。`<map>`を指定すれば、その内容を出力します。`<map>`は\#`<id>`または`<name>`です。デフォルトでは、現在のマップバージョンを表示します。これは、現在マッチングに使い、マップ一覧で'curr_ver'と報告するバージョンです。マップ識別子の前に'@`<ver>`'を付けると、他のバージョンも出力できます。バージョンはフィルターとして働き、存在しないバージョンは、単に結果を返しません。'entry_cnt'は、有効なものだけでなく、追加中のものも含む、マップの全エントリー数を表します。

出力の最初の列は、一意のエントリー識別子で、"del map"や"set map"操作の参照として使えます。二番目はパターン、三番目は、あればサンプルです。返すデータは、使用可能なマップの一覧そのものではなく、いずれかのマップを構成する全パターンの一覧です。多くのパターンは、ACLと共有できます。

<a id="entry-9-3-show-peers"></a>


**`show peers [dict|-] [<peers section>]`**


```haproxy
show peers [dict|-] [<peers section>]
```


"peers"セクションで設定したピアの情報を出力します。引数がなければ、すべての"peers"セクションに属するピアを一覧にします。`<peers section>`を指定すると、その"peers"セクションのピアの情報だけを出力します。セクション名の前に"dict"を指定すると、送受信（Tx/Rx）の辞書キャッシュ全体も出力します（非常に大きな出力です）。"dict"という名前のpeersセクションを出力するには、"-"を渡す必要がある場合があります。

以下は、hostA、hostB、hostCのピアが"sharedlb"というpeersセクションに属する、二つの出力例です。接続しているのはhostAとhostBだけで、データを送ったのはhostAからhostBへの方向だけです。

\$ echo "show peers" \| socat - /tmp/hostA 0x55deb0224320: [15/Apr/2019:11:28:01] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=45122
0x55deb022b540: id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92;
reconnect=4s confirm=0 flags=0x0 0x55deb022a440: id=hostA(local) addr=127.0.0.10:10000 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55deb0227d70: id=hostB(remote)
addr=127.0.0.11:10001 status=ESTA reconnect=2s confirm=0 flags=0x20000200 appctx:0x55deb028fba0
st0=7 st1=0 task_calls=14456 &#92; state=EST xprt=RAW src=127.0.0.1:37257
addr=127.0.0.10:10000 remote_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1
last_local_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55deb0224a10 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=0 last_pushed=3 last_get=0 teaching_origin=0 update=3
  table:0x55deb022d6a0 id=stkt update=3 localupdate=3 \
    commitupdate=3 syncing=0
```


\$ echo "show peers" \| socat - /tmp/hostB 0x55871b5ab320: [15/Apr/2019:11:28:03] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=3 0x55871b5b2540:
id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92; reconnect=3s
confirm=0 flags=0x0 0x55871b5b1440: id=hostB(local) addr=127.0.0.11:10001 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55871b5aed70: id=hostA(remote)
addr=127.0.0.10:10000 status=ESTA &#92; reconnect=2s confirm=0
flags=0x20000200 appctx:0x7fa46800ee00 st0=7 st1=0 task_calls=62356 &#92;
state=EST remote_table:0x55871b5ab960 id=stkt local_id=1 remote_id=1 last_local_table:0x55871b5ab960
id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55871b5ab960 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=3 last_pushed=0 last_get=3 teaching_origin=0 update=0
  table:0x55871b5b46a0 id=stkt update=1 localupdate=0 \
    commitupdate=0 syncing=0
```


<a id="entry-9-3-show-pools"></a>


**`show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]`**


```haproxy
show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]
```


内部メモリープールの状態を出力します。たとえば、メモリーリークを疑う場合に、使用状況を追うのに便利です。フォアグラウンド実行中のSIGQUITとまったく同じ処理ですが、プールをフラッシュしません。デフォルトでは並べ替えません。"byname"を指定するとプール名で、"bysize"なら要素サイズの降順で、"byusage"なら総使用量の降順で並べます。"byusage"では、使用中のエントリーだけを表示します。使用量順の場合など、先頭`<nb>`件に制限することもできます。"detailed"を指定すると、統合した全プールの一覧など、より詳しい内部情報も出力できます。最後に、"match"の後に接頭辞を指定すると、その接頭辞で名前が始まるプールだけを表示します。報告する合計値は、フィルター条件にマッチするプールだけが対象です。例：

```shell
$ socat - /tmp/haproxy.sock <<< "show pools match quic byusage"
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool quic_conn_r (65560 bytes): 1337 allocated (87653720 bytes), ...
  - Pool quic_crypto (1048 bytes): 6685 allocated (7005880 bytes), ...
  - Pool quic_conn (4056 bytes): 1337 allocated (5422872 bytes), ...
  - Pool quic_rxbuf (262168 bytes): 8 allocated (2097344 bytes), ...
  - Pool quic_conne (184 bytes): 9359 allocated (1722056 bytes), ...
  - Pool quic_frame (184 bytes): 7938 allocated (1460592 bytes), ...
  - Pool quic_tx_pac (152 bytes): 6454 allocated (981008 bytes), ...
  - Pool quic_tls_ke (56 bytes): 12033 allocated (673848 bytes), ...
  - Pool quic_rx_pac (408 bytes): 1596 allocated (651168 bytes), ...
  - Pool quic_tls_se (88 bytes): 6685 allocated (588280 bytes), ...
  - Pool quic_cstrea (88 bytes): 4011 allocated (352968 bytes), ...
  - Pool quic_tls_iv (24 bytes): 12033 allocated (288792 bytes), ...
  - Pool quic_dgram (344 bytes): 732 allocated (251808 bytes), ...
  - Pool quic_arng (56 bytes): 4011 allocated (224616 bytes), ...
  - Pool quic_conn_c (152 bytes): 1337 allocated (203224 bytes), ...
Total: 15 pools, 109578176 bytes allocated, 109578176 used ...
```


<a id="entry-9-3-show-profiling"></a>


**`show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*`**


```haproxy
show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*
```


現在のプロファイリング設定を一行に一つずつ、変更に必要なコマンドとともに出力します。タスクのプロファイリングが有効なら、スケジューラーが収集した関数ごとの統計と、呼び出し回数、CPU時間の合計と平均、遅延の合計と平均を含む要約も出力します。メモリーのプロファイリングが有効なら、割り当て・解放の回数とサイズなどを報告します。対応するキーワードを指定し、プロファイリングの状態、タスク、メモリーのいずれかだけに絞れます。デフォルトでは、すべてのプロファイリング情報を出力します。数値の上限を指定すると、各分類の出力行数も制限できます。たとえば、続けて呼び出した結果を比較したり、最適化する箇所を調べたりしやすいよう、使用量の代わりに、アドレス、合計実行時間、呼び出し文脈で並べるよう要求できます。また、詳細を見る代わりに、呼び出された関数ごとにタスクの活動を集約できます。プロファイリングは、コード内でCPUサイクルやメモリーを浪費する箇所の手掛かりを与えるため、主に開発者向けである点に注意してください。監視に役立つ情報はありません。

<a id="entry-9-3-show-resolvers"></a>


**`show resolvers [<resolvers section id>]`**


```haproxy
show resolvers [<resolvers section id>]
```


指定したresolversセクションの統計を出力します。セクションを指定しなければ、すべてのresolversセクションが対象です。

ネームサーバーごとに、次のカウンターを報告します。

```text
sent: このサーバーへ送信したDNSリクエスト数
valid: このサーバーから受信した有効なDNSレスポンス数
update: サーバーのIPアドレスの更新に使用したDNSレスポンス数
cname: CNAMEレスポンス数
cname_error: このサーバーで発生したCNAMEエラー
any_err: 空のレスポンス数（すなわち、サーバーがANYタイプをサポートしていません）
nx: このサーバーから受信した、ドメインが存在しないことを示すレスポンス
timeout: このサーバーが時間内に応答しなかった回数
refused: このサーバーが拒否したリクエスト数
other: その他のDNSエラー
invalid: プロトコル上、不正なDNSレスポンス
too_big: 大きすぎるレスポンス
outdated: 遅れて到着したレスポンス数（別のネームサーバーからの応答より後）
```


<a id="entry-9-3-show-quic"></a>


**`show quic [<format>] [<filter>]`**


```haproxy
show quic [<format>] [<filter>]
```


有効なすべてのQUICフロントエンド接続の情報を出力します。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。

任意の引数で、出力の詳しさを制御できます。値には複数の解釈方法があります。まず、定義済みの値を使えます。"oneline"はデフォルトの形式、"stream"は有効な全ストリームの一覧、"full"は全情報の表示です。代わりに、フィールドをカンマ区切りで指定し、出力を絞ることもできます。現在サポートする値は、"tp"、"sock"、"pktns"、"cc"、"mux"です。最後に、形式へ"help"を指定すると、代わりに詳しいヘルプを表示します。

最後の引数は、接続一覧を絞ったり広げたりします。デフォルトでは、有効なフロントエンド接続だけを表示します。追加引数"clo"なら、代わりにクローズ中のフロントエンド接続を、"be"ならバックエンド接続、"all"なら全種類を一覧にします。接続の16進アドレスを指定し、一つの接続だけに絞ることもできます。

<a id="entry-9-3-show-servers-conn"></a>


**`show servers conn [<backend>]`**


```haproxy
show servers conn [<backend>]
```


指定したバックエンドに属するサーバーの、現在の接続とアイドル接続の状態を出力します。指定がなければ全バックエンドが対象です。バックエンド名または識別子を使えます。

出力は、フィールドの見出しを示すヘッダー行と、それに続くサーバーごとの一行から成ります。各行には、バックエンド名とID、サーバー名とID、アドレス、ポート、各種の値を示します。フィールド数はスレッド数によって変わります。正確な出力形式は、バージョンやスレッド数によって、多少異なる場合があります。値を取り出すときは、ヘッダー行を見て列を対応させ、末尾の列はスレッドごとなので、スレッド数にも注意する必要があります。

```text
bkname/svname         バックエンド名 '/' サーバー名
bkid/svid             バックエンドID '/' サーバーID
addr                  サーバーのIPアドレス
port                  サーバーのポート（なければゼロ）
-                     未使用のフィールド。見た目上の区切りとして使います。
purge_delay           接続のパージ間隔。単位はミリ秒です。
served                現在使用中の接続数
used_cur              現在使用中の接続数。
                      セッションに結び付いた接続は含みません。
used_max              プロセス起動後のused_curの最大値
need_est              必要な接続総数の変動する推定値
idle_sess             専用としてマークされたアイドル接続数
unsafe_nb             "unsafe"と見なされるアイドル接続数
safe_nb               "safe"と見なされるアイドル接続数
idle_lim              設定されたアイドル接続数の上限
idle_cur              スレッドごとの、現在アイドル状態にある接続数の合計
idle_per_thr[NB]      NB個のスレッドそれぞれの、スレッドあたりのアイドル接続数
```


`<idle_cur>` + `<used_cur>`の合計が推定値`<need_est>`を超えると、HAProxyは`<purge_delay>`ごとに`<idle_cur>`の一部を終了させます。この推定値は、接続の活動状況によって変わります。

アイドル接続はスレッドごとに管理するため、読み取った後に変わる値もあり、一行の中でも整合性を保証しないことを理解しておくのが重要です。この出力は主にデバッグ用で、定期的な監視やグラフ化には適しません。

<a id="entry-9-3-show-servers-state"></a>


**`show servers state [<backend>]`**


```haproxy
show servers state [<backend>]
```


実行中の設定にあるサーバーの状態を出力します。バックエンド名または識別子を指定し、そのバックエンドだけに絞れます。

出力は次の形式です。

- 最初の行は形式のバージョンです（この仕様では1）。
- 二行目は列の見出しで、先頭にシャープ（'#'）を付けます。
- 三行目以降はデータです。
- シャープ（'#'）で始まる行は、すべてコメントとみなします。

複数の出力バージョンが共存し得るため、以下に、ファイル形式のバージョンごとのフィールドと順序を示します。

```text
1:
  be_id:                       バックエンドの一意のID。
  be_name:                     バックエンドのラベル。
  srv_id:                      サーバーの一意のID（バックエンド内）。
  srv_name:                    サーバーのラベル。
  srv_addr:                    サーバーのIPアドレス。
  srv_op_state:                サーバーの動作状態（UP/DOWN/...）。
                                 0 = SRV_ST_STOPPED
                                   サーバーは停止しています。
                                 1 = SRV_ST_STARTING
                                   サーバーはウォームアップ中です
                                   （稼働していますが、処理能力を制限しています）。
                                 2 = SRV_ST_RUNNING
                                   サーバーは完全に稼働しています。
                                 3 = SRV_ST_STOPPING
                                   サーバーは稼働中ですが、ソフト停止の途中です
                                   （たとえば404）。
  srv_admin_state:             サーバーの管理状態（MAINT/DRAIN/...）。
                               実際の状態は、次の値のビットマスクです。
                                 0x01 = SRV_ADMF_FMAINT
                                   サーバーは明示的にメンテナンス状態へ
                                   強制移行されました。
                                 0x02 = SRV_ADMF_IMAINT
                                   サーバーは追跡対象のサーバーから
                                   メンテナンス状態を継承しました。
                                 0x04 = SRV_ADMF_CMAINT
                                   サーバーは設定によってメンテナンス状態に
                                   なっています。
                                 0x08 = SRV_ADMF_FDRAIN
                                   サーバーは明示的にdrain状態へ
                                   強制移行されました。
                                 0x10 = SRV_ADMF_IDRAIN
                                   サーバーは追跡対象のサーバーから
                                   drain状態を継承しました。
                                 0x20 = SRV_ADMF_RMAINT
                                   サーバーはIPアドレスの名前解決に失敗したため、
                                   メンテナンス状態になっています。
                                 0x40 = SRV_ADMF_HMAINT
                                   サーバーのFQDNは統計ソケットから設定されました。

  srv_uweight:                 ユーザーに見えるサーバーの重み。
  srv_iweight:                 サーバーの初期の重み。
  srv_time_since_last_change:  最後に動作状態が変わってからの時間。
  srv_check_status:            最後のヘルスチェックの状態。
  srv_check_result:            最後のチェック結果（FAILED/PASSED/...）。
                                 0 = CHK_RES_UNKNOWN
                                   既定ではこの値に初期化されます。
                                 1 = CHK_RES_NEUTRAL
                                   チェックは有効ですが、状態の情報はありません。
                                 2 = CHK_RES_FAILED
                                   チェックは失敗しました。
                                 3 = CHK_RES_PASSED
                                   チェックに成功し、サーバーは再び完全に
                                   稼働しています。
                                 4 = CHK_RES_CONDPASS
                                   サーバーが新しいセッションを受け入れたくない
                                   ことを、チェックが報告しています。
  srv_check_health:            チェックのrise / fallの現在のカウンター。
  srv_check_state:             チェックの状態（ENABLED/PAUSED/...）。
                               実際の状態は、次の値のビットマスクです。
                                 0x01 = CHK_ST_INPROGRESS
                                   現在、チェックを実行中です。
                                 0x02 = CHK_ST_CONFIGURED
                                   このチェックは設定済みで、有効化できます。
                                 0x04 = CHK_ST_ENABLED
                                   このチェックは現在、管理上有効になっています。
                                 0x08 = CHK_ST_PAUSED
                                   メンテナンスのため、チェックを一時停止しています
                                   （ヘルスチェックのみ）。
  srv_agent_state:             エージェントチェックの状態（ENABLED/PAUSED/...）。
                               "srv_check_state"と同じビットマスクに、
                               次の固有の値を加えたものを使います。
                                 0x10 = CHK_ST_AGENT
                                   エージェントチェックであることを示します
                                   （それ以外はヘルスチェックです）。
  bk_f_forced_id:              バックエンドIDが設定によって強制されているか
                               どうかを示すフラグ。
  srv_f_forced_id:             サーバーIDが設定によって強制されているか
                               どうかを示すフラグ。
  srv_fqdn:                    サーバーのFQDN。
  srv_port:                    サーバーのポート。
  srvrecord:                   このSRVに関連付けられたDNS SRVレコード。
  srv_use_ssl:                 サーバー接続でSSLを使用するかどうか。
  srv_check_port:              サーバーのヘルスチェック用ポート。
  srv_check_addr:              サーバーのヘルスチェック用アドレス。
  srv_agent_addr:              サーバーのヘルスエージェント用アドレス。
  srv_agent_port:              サーバーのヘルスエージェント用ポート。
```


<a id="entry-9-3-show-sess"></a>


**`show sess [<options>*]`**


```haproxy
show sess [<options>*]
```


既知の有効なストリーム（以前の呼称は「セッション」）をすべて出力します。出力が非常に大きくなり得るため、遅い接続では避けてください。このコマンドは制限されており、"operator"または"admin"レベルを設定したソケットからだけ実行できます。接続をすぐに再利用するマシンでは、実際より少ないエントリーしか報告しない場合があります。コマンドを入力する前に作成した最後のストリームまでの、存在するストリームを出力するためで、その間に消えたものは現れません。使えるオプションは、以下を参照してください。

<a id="entry-9-3-show-sess-2"></a>


**`show sess [<id> | all | help] [<options>*]`**


```haproxy
show sess [<id> | all | help] [<options>*]
```


マッチするストリームの内部情報を詳しく表示します。出力形式は二つあります。特定のストリーム識別子を指定しない場合のデフォルトである短い形式と、指定したストリームを一覧にする拡張形式です。"show sess"のデフォルトである短い形式は、一行に一つのストリームと少数の情報だけを出力し、先頭にストリーム識別子を16進数で示します（ストリームへのポインターに対応します）。

"show sess `<id>`"または"show sess all"で使う拡張形式は、ストリームごとに複数行（それぞれ約20行）で、大量のデバッグ情報を出力します。この場合も、先頭は識別子です。ストリーム同士の区切りは行頭の識別子で、同じストリームの追加行は、一つ以上の空白で始まります（インデントして出力します）。多数のストリームを出力すると、出力が膨大になり、多くの時間とCPUを使うため、常に必要最小限だけを出力するほうがよいでしょう。大半の利用者には役立たない情報ですが、HAProxyの開発者が複雑な不具合を調べるのに使う場合があります。安定版のブランチも含め、必要に応じて自由に変えられるよう、正確な出力形式は意図的に文書化していません。特定のフィールドの正確な意味を知るには、src/stream.cのstrm_dump_to_buffer()関数を確認しながら、出力を読み解くことを想定しています。

"help"引数を指定すると、ストリームの出力の代わりに、コマンドの詳しい使い方を表示します。

オプションで出力を調整したり、フィルターを適用したりできます。サポートするオプションは次のとおりです。- backend `<b>`：このバックエンドに結び付いたストリームだけを表示します。- frontend `<f>`：このフロントエンドに結び付いたストリームだけを表示します。- older `<age>`：`<age>`秒より古いストリームだけを表示します。- server `<b/s>`：このバックエンドとサーバーに結び付いたストリームだけを表示します。- show-uri：リクエスト解析中に取得したトランザクションURIを出力します。取得していた場合だけ表示します。- susp：開発者の基準で不審とみなすストリームだけを表示します。基準は、時間の経過やバージョンによって変わり得ます。

<a id="entry-9-3-show-stat"></a>


**`show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \`**


```haproxy
show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \
          [typed|json] [desc] [up|no-maint]
```


統計を出力します。domainは、どの統計を出すかを選び、現在はresolversとproxyを使えます。デフォルトはCSV形式です。他の引数の後に"typed"を渡すと、上の節で説明した拡張された型付き出力形式を、"json"を渡すとJSONを使えます。`<id>`、`<type>`、`<sid>`を渡すと、選んだ項目だけを出力できます。- `<iid>`はプロキシIDで、-1ならすべてを出力します。代わりにプロキシ名`<proxy>`も指定でき、その場合は、そのプロキシのIDを選択条件に使います。- `<type>`は、出力するオブジェクトの種類です。1はフロントエンド、2はバックエンド、4はサーバー、-1はすべてです。値をORで組み合わせられます。例：

```text
1 + 2     = 3   -> フロントエンド + バックエンド。
1 + 2 + 4 = 7   -> フロントエンド + バックエンド + サーバー。
```


    - `<sid>`はサーバーIDで、-1なら選択したプロキシのすべてを出力します。

例：

```shell
    $ echo "show info;show stat" | socat stdio unix-connect:/tmp/sock1
>>> Name: HAProxy
    Version: 1.4-dev2-49
    Release_date: 2009/09/23
    Nbproc: 1
    Process_num: 1
    (...)

    # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,  (...)
    stats,FRONTEND,,,0,0,1000,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,1,0, (...)
    stats,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,0,0,0,,0,250,(...)
    (...)
    www1,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,1,1,0,,0,250, (...)

    $
```


この例では、二つのコマンドを一度に実行しています。こうすると、マルチプロセスモードで、統計がどのプロセスのものかを容易に判断できます。型付き出力では、各行にプロセス番号を報告するため、不要です。情報出力の後の空行は、最初のブロックの終了を示します。同様の空行が二番目のブロック（統計）の末尾にもあるため、読む側は出力が途中で切れていないことを確認できます。

"typed"を指定した出力は、数値位置と各フィールドの型を示すため、監視ツールにより適しています。値ごとに独立した行を使い、プロセス番号、要素番号、性質、生成元、スコープを含めます。URIの後に";typed"を渡すと、HTTP統計でも同じ形式を使えます。型付き出力では、一つのオブジェクトの情報を連続して出力するため、利用する側がすべてを一度に保存する必要がない点が非常に重要です。

"up"修飾子は、稼働中と報告されるサーバー、またはチェックしていないサーバーだけを一覧にします。停止中、未解決、メンテナンス中のものは表示しません。HTTP統計の";up"に相当します。同様に、"no-maint"は、HTTPの";no-maint"と同じように働き、無効なサーバーを一覧から除きます。違いは、有効だが停止中のサーバーを除外しないことです。

型付き出力では、各行はコロン（':'）で区切った4列です。最初の列は、ドットで区切った5要素の列です。最初の要素は、オブジェクトの種類を表す文字です。現在知られている種類は、'F'がフロントエンド、'B'がバックエンド、'L'がリスナー、'S'がサーバーです。二番目は、そのオブジェクトが属するプロキシの一意の識別子を表す正の整数です。CSV出力の"iid"列と同等で、フロントエンドまたはバックエンドセクションの任意の"id"ディレクティブに指定する値に一致します。三番目は、プロキシ内のオブジェクトの一意の識別子を含む正の整数で、CSV出力の"sid"列に対応します。フロントエンドやバックエンドを出力する場合は、ID 0を報告します。リスナーやサーバーなら、プロキシ内のそれぞれのIDです。四番目は、ゼロから始まる、一覧内のフィールドの数値位置です。この位置は将来も変更してはなりませんが、ビルドオプションや将来のフィールド削除により、欠番が生じることは想定してください。五番目は、CSV出力に現れるフィールド名です。六番目は正の整数で、1から始まる相対プロセス番号です。

最初のコロンより後は、上の節で説明した「型付き出力形式」に従います。つまり、二番目の列（最初の':'の後）は、変数の生成元、性質、スコープ、永続状態を示します。三番目はフィールドの型で、"s32"、"s64"、"u32"、"u64"、"flt"、"str"のいずれかです。四番目は値そのものです。利用する側は、列3から解析方法を、列2から処理方法を判断できます。

コマンドに"desc"を付けると、コロンをもう一つ追加し、その後に、指標の説明を引用符付き文字列で付けます。執筆時点では、"typed"出力形式だけでサポートします。

したがって、型付きモードでの行全体の形式は次のとおりです。

```text
<obj>.<px_id>.<id>.<fpos>.<fname>.<process_num>:<tags>:<type>:<value>
```


型付き出力形式の例を示します。

```shell
$ echo "show stat typed" | socat stdio unix-connect:/tmp/sock1
F.2.0.0.pxname.1:KNSV:str:dummy
F.2.0.1.svname.1:KNSV:str:FRONTEND
F.2.0.4.scur.1:MGPV:u32:0
F.2.0.5.smax.1:MMPV:u32:0
F.2.0.6.slim.1:CLPV:u32:524269
F.2.0.7.stot.1:MCPP:u64:0
F.2.0.8.bin.1:MCPP:u64:0
F.2.0.9.bout.1:MCPP:u64:0
F.2.0.10.dreq.1:MCPP:u64:0
F.2.0.11.dresp.1:MCPP:u64:0
F.2.0.12.ereq.1:MCPP:u64:0
F.2.0.17.status.1:SGPV:str:OPEN
F.2.0.26.pid.1:KGPV:u32:1
F.2.0.27.iid.1:KGSV:u32:2
F.2.0.28.sid.1:KGSV:u32:0
F.2.0.32.type.1:CGSV:u32:0
F.2.0.33.rate.1:MRPP:u32:0
F.2.0.34.rate_lim.1:CLPV:u32:0
F.2.0.35.rate_max.1:MMPV:u32:0
F.2.0.46.req_rate.1:MRPP:u32:0
F.2.0.47.req_rate_max.1:MMPV:u32:0
F.2.0.48.req_tot.1:MCPP:u64:0
F.2.0.51.comp_in.1:MCPP:u64:0
F.2.0.52.comp_out.1:MCPP:u64:0
F.2.0.53.comp_byp.1:MCPP:u64:0
F.2.0.54.comp_rsp.1:MCPP:u64:0
(...)
```


型付き形式は、最初の列の末尾にプロセスIDがあるため、複数のプロセスの出力を目で見て容易に集約できます。以下の例では、各行がプロセスごとに現れます。

```shell
$ ( echo show stat typed | socat /var/run/haproxy.sock1 -; \
    echo show stat typed | socat /var/run/haproxy.sock2 - ) | \
  sort -t . -k 1,1 -k 2,2n -k 3,3n -k 4,4n -k 5,5 -k 6,6n
B.3.0.0.pxname.1:KNSV:str:private-backend
B.3.0.0.pxname.2:KNSV:str:private-backend
B.3.0.1.svname.1:KNSV:str:BACKEND
B.3.0.1.svname.2:KNSV:str:BACKEND
B.3.0.2.qcur.1:MGPV:u32:0
B.3.0.2.qcur.2:MGPV:u32:0
B.3.0.3.qmax.1:MMPV:u32:0
B.3.0.3.qmax.2:MMPV:u32:0
B.3.0.4.scur.1:MGPV:u32:0
B.3.0.4.scur.2:MGPV:u32:0
B.3.0.5.smax.1:MMPV:u32:0
B.3.0.5.smax.2:MMPV:u32:0
B.3.0.6.slim.1:CLPV:u32:1000
B.3.0.6.slim.2:CLPV:u32:1000
(...)
```


JSON出力の形式は、"show schema json"で出力できるスキーマに記述されています。

出力量を減らすため、JSON出力には余分な空白がありません。人が読む場合は、整形ツールに通すと便利です。例：

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

出力量を減らすため、JSON出力には余分な空白がありません。人が読む場合は、整形ツールに通すと便利です。例：

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-ssl-ca-file"></a>


**`show ssl ca-file [[*][\]<cafile>[:<index>]]`**


```haproxy
show ssl ca-file [[*][\]<cafile>[:<index>]]
```


プロセスに読み込まれたCAファイルと、それぞれに含まれる証明書の数を表示します。証明書は、ステータスが"Used"になるまでフロントエンドやバックエンドで使用されません。一覧に"@system-ca"エントリーが表示されることがあります。これはhttpclientがデフォルトで読み込むもので、OpenSSLが返すシステムの信頼されたCAの一覧を含みます。ファイル名の先頭にアスタリスクが付いている場合は、まだコミットされていないトランザクションです。`<index>`を付けずに`<cafile>`を指定すると、CAファイルのステータス（"Used"/"Unused"）に続いて、そのCAファイルに含まれるすべての証明書の詳細を表示します。各証明書について表示される詳細は、"show ssl cert"コマンドと同じです。`<cafile>`に続けて`<index>`を指定すると、そのインデックスの証明書の詳細だけを表示します。インデックスは1から始まります。インデックスが無効な場合（大きすぎる場合など）は何も表示しません。このコマンドは、CAファイルが正しく更新されたかを確認するのに役立ちます。ファイル名の先頭に'*'を付けると、進行中のトランザクションの詳細も表示できます。ファイル名の最初の文字が'*'の場合は、'&#92;\*'でエスケープできます。

例：

```shell
$ echo "show ssl ca-file" | socat /var/run/haproxy.master -
# transaction
*cafile.crt - 2 certificate(s)
# filename
cafile.crt - 1 certificate(s)

$ echo "show ssl ca-file cafile.crt" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Used

Certificate #1:
Serial: 11A4D2200DC84376E7D233CAFF39DF44BF8D1211
notBefore: Apr  1 07:40:53 2021 GMT
notAfter: Aug 17 07:40:53 2048 GMT
Subject Alternative Name:
Algorithm: RSA4096
SHA1 FingerPrint: A111EF0FEFCDE11D47FE3F33ADCA8435EBEA4864
Subject: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA
Issuer: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA

$ echo "show ssl ca-file *cafile.crt:2" | socat /var/run/haproxy.master -
Filename: */home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Unused

Certificate #2:
Serial: 587A1CE5ED855040A0C82BF255FF300ADB7C8136
[...]
```


<a id="entry-9-3-show-ssl-cert"></a>


**`show ssl cert [[*][\]<filename>]`**


```haproxy
show ssl cert [[*][\]<filename>]
```


プロセスに読み込まれた証明書の一覧を表示します。証明書は、ステータスが"Used"になるまでフロントエンドやバックエンドで使用されません。ファイル名の先頭にアスタリスクが付いている場合は、まだコミットされていないトランザクションです。ファイル名を指定すると、その証明書の詳細を表示します。このコマンドは、証明書が正しく更新されたかを確認するのに役立ちます。ファイル名の先頭に'*'を付けると、トランザクションの詳細も表示できます。ファイル名の最初の文字が'*'の場合は、'&#92;\*'でエスケープできます。ファイル名の末尾に".ocsp"拡張子を付けると、証明書のOCSPレスポンスの詳細も表示できます。コミット済みの証明書と進行中のトランザクションの両方に対応しています。コミット済みの証明書の場合、このコマンドは、証明書に対応するOCSPレスポンスIDを指定して"show ssl ocsp-response"を呼び出すのと同じです。

例：

```shell
$ echo "@1 show ssl cert" | socat /var/run/haproxy.master -
# transaction
*test.local.pem
# filename
test.local.pem

$ echo "@1 show ssl cert test.local.pem" | socat /var/run/haproxy.master -
Filename: test.local.pem
Status: Used
Serial: 03ECC19BA54B25E85ABA46EE561B9A10D26F
notBefore: Sep 13 21:20:24 2019 GMT
notAfter: Dec 12 21:20:24 2019 GMT
Issuer: /C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
Subject: /CN=test.local
Subject Alternative Name: DNS:test.local, DNS:imap.test.local
Algorithm: RSA2048
SHA1 FingerPrint: 417A11CAE25F607B24F638B4A8AEE51D1E211477

$ echo "@1 show ssl cert *test.local.pem" | socat /var/run/haproxy.master -
Filename: *test.local.pem
Status: Unused
[...]

$ echo "@1 show ssl cert \*.local.pem" | socat /var/run/haproxy.master -
Filename: *.local.pem
Status: Used
[...]
```


<a id="entry-9-3-show-ssl-crl-file"></a>


**`show ssl crl-file [[*][\]<crlfile>[:<index>]]`**


```haproxy
show ssl crl-file [[*][\]<crlfile>[:<index>]]
```


プロセスに読み込まれたCRLファイルの一覧を表示します。CRLファイルは、ステータスが"Used"になるまでフロントエンドやバックエンドで使用されません。ファイル名の先頭にアスタリスクが付いている場合は、まだコミットされていないトランザクションです。`<index>`を付けずに`<crlfile>`を指定すると、CRLファイルのステータス（"Used"/"Unused"）に続いて、そのCRLファイルに含まれるすべての失効リストの詳細を表示します。各リストの詳細は、"openssl crl -text -noout -in `<file>`"の出力に基づきます。`<crlfile>`に続けて`<index>`を指定すると、そのインデックスのリストの詳細だけを表示します。インデックスは1から始まります。インデックスが無効な場合（大きすぎる場合など）は何も表示しません。このコマンドは、CRLファイルが正しく更新されたかを確認するのに役立ちます。ファイル名の先頭に'*'を付けると、進行中のトランザクションの詳細も表示できます。ファイル名の最初の文字が'*'の場合は、'&#92;\*'でエスケープできます。

例：

```shell
$ echo "show ssl crl-file" | socat /var/run/haproxy.master -
# transaction
*crlfile.pem
# filename
crlfile.pem

$ echo "show ssl crl-file crlfile.pem" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/crlfile.pem
Status: Used

Certificate Revocation List #1:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Intermediate CA2
Last Update: Apr 23 14:45:39 2021 GMT
Next Update: Sep  8 14:45:39 2048 GMT
Revoked Certificates:
    Serial Number: 1008
        Revocation Date: Apr 23 14:45:36 2021 GMT

Certificate Revocation List #2:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Root CA
Last Update: Apr 23 14:30:44 2021 GMT
Next Update: Sep  8 14:30:44 2048 GMT
No Revoked Certificates.
```


<a id="entry-9-3-show-ssl-crt-list"></a>


**`show ssl crt-list [-n] [<filename>]`**


```haproxy
show ssl crt-list [-n] [<filename>]
```


HAProxyの設定で使用されているcrt-listとディレクトリの一覧を表示します。ファイル名を指定すると、crt-listまたはディレクトリの内容を出力します。この出力はcrt-listファイルとして使用できます。'-n'オプションを指定すると行番号を表示できます。エントリーが重複している場合に、'del ssl crt-list'オプションと組み合わせると便利です。'-n'オプション付きの出力はcrt-list形式と互換性がなく、haproxyに読み込むことはできません。

例：

```shell
echo "show ssl crt-list -n localhost.crt-list" | socat /tmp/sock1 -
# localhost.crt-list
common.pem:1 !not.test1.com *.test1.com !localhost
common.pem:2
ecdsa.pem:3 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3] localhost !www.test1.com
ecdsa.pem:4 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3]
```


<a id="entry-9-3-show-ssl-ech"></a>


**`show ssl ech [<name>]`**


```haproxy
show ssl ech [<name>]
```


HAProxyプロセスに読み込まれたECHキーの一覧を表示します。

`<name>`を指定すると、特定のbind行のキーを表示します。bind行の指定形式は`<frontend>`/@`<filename>`:`<linenum>`（例：frontend1/@haproxy.conf:19）です。"name"キーワードでbind行に名前を付けている場合は、`<frontend>`/`<name>`も使用できます。

'age'エントリーは、そのbind行にキーが読み込まれてからの経過時間を秒単位で表します。この値は、HAProxyの起動、リロード、再起動時にリセットされます。

OpenSSL のバージョンが ECH をサポートしている必要があり、HAProxy は USE_ECH=1 でコンパイルされている必要があります。このコマンドは、実験モードで実行されている CLI 接続でのみサポートされます（「experimental-mode on」を参照）。

設定マニュアルの[セクション5.1](/ja/docs/haproxy/bind-and-server-options/#section-5-1)にある"ech"も参照してください。

例：

```shell
$ echo "experimental-mode on; show ssl ech" | socat /tmp/haproxy.sock -
 ***
 frontend: frontend1

 bind: frontend1/@haproxy.conf:19

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

 bind: frontend1/@haproxy.conf:20

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

$ echo "experimental-mode on; show ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
***
ECH for frontend1/@haproxy.conf:19
ECH entry: 0 public_name: example.com age: 786 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

ECH entry: 1 public_name: example.com age: 786 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]
```


<a id="entry-9-3-show-ssl-jwt"></a>


**`show ssl jwt`**


```haproxy
show ssl jwt
```


JWTの検証に使用できる証明書の一覧を表示します。"add ssl jwt"および"del ssl jwt"コマンドも参照してください。詳細は、証明書オプション"jwt"を参照してください。

例：

```shell
echo "show ssl jwt"  | socat /tmp/sock1 -
#filename
jwt.pem
```


<a id="entry-9-3-show-ssl-ocsp-response"></a>


**`show ssl ocsp-response [[text|base64] <id|path>]`**


```haproxy
show ssl ocsp-response [[text|base64] <id|path>]
```


HAProxyで使用されるすべてのOCSPレスポンスに対応するOCSPツリーのエントリーIDと、対応するフロントエンド証明書のパス、発行者の名前とキーハッシュ、OCSPレスポンスの対象となる証明書のシリアル番号を表示します。有効な`<id>`または有効なフロントエンド証明書の`<path>`を指定すると、対応するOCSPレスポンスの内容を表示します。`<id>`を指定する場合は、データの出力形式も指定できます。デフォルトは'text'で、"openssl ocsp -respin `<ocsp-response>` -text"の呼び出しと同様に、OCSPレスポンスの詳細情報を表示します。'base64'形式では、OCSPレスポンスの内容をbase64で出力できます。

例：

```shell
$ echo "show ssl ocsp-response" | socat /var/run/haproxy.master -
# Certificate IDs
  Certificate ID key: 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a
  Certificate path: /path_to_cert/foo.pem
    Certificate ID:
      Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
      Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
      Serial Number: 100A

$ echo "show ssl ocsp-response 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a" | socat /var/run/haproxy.master -
OCSP Response Data:
  OCSP Response Status: successful (0x0)
  Response Type: Basic OCSP Response
  Version: 1 (0x0)
  Responder Id: C = FR, O = HAProxy Technologies, CN = ocsp.haproxy.com
  Produced At: May 27 15:43:38 2021 GMT
  Responses:
  Certificate ID:
    Hash Algorithm: sha1
    Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
    Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
    Serial Number: 100A
  Cert Status: good
  This Update: May 27 15:43:38 2021 GMT
  Next Update: Oct 12 15:43:38 2048 GMT
  [...]

$ echo "show ssl ocsp-response base64 /path_to_cert/foo.pem" | socat /var/run/haproxy.sock -
  MIIB8woBAKCCAewwggHoBgkrBgEFBQcwAQEEggHZMIIB1TCBvqE[...]
```


<a id="entry-9-3-show-ssl-ocsp-updates"></a>


**`show ssl ocsp-updates`**


```haproxy
show ssl ocsp-updates
```


OCSP更新機構の対象となるエントリーの情報を表示します。OCSPレスポンスごとに一行を出力し、レスポンスの更新予定時刻、最後に更新が成功した時刻、更新の成功回数と失敗回数を含めます。前回の更新のステータス（成功か失敗か）も、数値と文字列の両方で表示します。起こりうるエラーの一覧は下記を参照してください。各行は'Next Update'の時刻の昇順で並びます。また、そのOCSPレスポンスを使用する最初のフロントエンド証明書のパスも含みます。OCSPの自動更新については、"show ssl ocsp-response"コマンドと"ocsp-update"オプションを参照してください。

更新エラーのコードと文字列には、次のものがあります。

```text
  +----+-------------------------------------+
  | ID | メッセージ                          |
  +----+-------------------------------------+
  |  0 | "Unknown"                           |
  |  1 | "Update successful"                 |
  |  2 | "HTTP error"                        |
  |  3 | "Missing \"ocsp-response\" header"  |
  |  4 | "OCSP response check failure"       |
  |  5 | "Error during insertion"            |
  +----+-------------------------------------+
```


例：

```shell
$ echo "show ssl ocsp-updates" | socat /tmp/haproxy.sock -
  OCSP Certid | Path | Next Update | Last Update | Successes | Failures | Last Update Status | Last Update Status (str)
      303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a02021015 | /path_to_cert/cert.pem | 30/Jan/2023:00:08:09 +0000 | - | 0 | 1 | 2 | HTTP error
      304b300906052b0e03021a0500041448dac9a0fb2bd32d4ff0de68d2f567b735f9b3c40414142eb317b75856cbae500940e61faf9d8b14c2c6021203e16a7aa01542f291237b454a627fdea9c1 | /path_to_cert/other_cert.pem | 30/Jan/2023:01:07:09 +0000 | 30/Jan/2023:00:07:09 +0000 | 1 | 0 | 1 | Update successful
```


<a id="entry-9-3-show-ssl-providers"></a>


**`show ssl providers`**


```haproxy
show ssl providers
```


初期化時にOpenSSLが読み込んだプロバイダーの名前を表示します。プロバイダーの読み込みはOpenSSL設定ファイルで設定でき、このオプションで目的のプロバイダーが読み込まれたかを確認できます。このコマンドはOpenSSL v3でのみ使用できます。

例：

```shell
$ echo "show ssl providers" | socat /var/run/haproxy.master -
Loaded providers:
    - fips
    - base
```


<a id="entry-9-3-show-ssl-sni"></a>


**`show ssl sni [-f <frontend>] [-A] [-t <offset>]`**


```haproxy
show ssl sni [-f <frontend>] [-A] [-t <offset>]
```


指定したフロントエンドに設定されているすべてのSNIを出力します。フロントエンドを指定しない場合は、すべてのフロントエンドを対象とします。フロントエンドが提供するSNIを確認し、同じフロントエンドの複数の証明書で同じSNIが重複して定義されていないかを調べることができます。

-Aオプションは、notAfterの日付を過ぎた証明書だけに一覧を絞り込み、有効期限が切れた証明書だけを表示します。

-tオプションは、秒単位、または時間単位（s、m、h、d）付きのオフセットを受け取り、現在時刻に加算します。-Aと組み合わせると、そのオフセット後にどの証明書の有効期限が切れているかを確認できます。たとえば、30d後に有効期限が切れている証明書を確認するには、"show ssl sni -A -t 30d"を実行します。

列は一つの&#92;tで区切られるため、簡単に解析できます。

'Frontend/Bind'列には、フロントエンド名に続いて設定内のbind行の位置（frontend/file:linenum）が表示されます。

'SNI'列には、CN、SAN、またはcrt-listのフィルターであるSNIが表示されます。bind行のデフォルト証明書（'default-crt'で明示的に指定した証明書、または'strict-sni'を使用していない場合に暗黙的にデフォルトとなるbind行の最初の証明書）では、SNI列に'\*'文字が表示されます。

'Negative Filter'列は、ワイルドカードに関連付けられた否定フィルターの一覧で、同じcrt-list行にあるすべての否定フィルターを表示します。該当するフィルターがなければ、ダッシュ文字を表示します。

'Type'列は暗号化アルゴリズムの種類を示し、"rsa"、"ecdsa"、"dsa"のいずれかです。

'Filename'列は、設定に記載されたファイル名、またはcrt-storeで宣言されたエイリアスです。

'NotAfter'列と'NotBefore'列は、X509リーフ証明書から直接抽出したものです。

例：

```shell
$ echo "@1 show ssl sni -A -t 30d" | socat /var/run/haproxy-master.sock - | column -t -s $'\t'
# Frontend/Bind        SNI        Negative Filter  Type   Filename             NotAfter                  NotBefore
li1/haproxy.cfg:10021  *.ex.lan   !m1.ex.lan       rsa    example.lan.pem      Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                rsa    machine10.pem.rsa    Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  localhost  -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
li1/haproxy.cfg:10021  localhost  -                ecdsa  localhost.pem.ecdsa  Jun 13 13:37:10 2024 GMT  May 14 13:37:10 2024 GMT
li1/haproxy.cfg:10021  *          -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
```


<a id="entry-9-3-show-startup-logs"></a>


**`show startup-logs`**


```haproxy
show startup-logs
```


現在のhaproxyプロセスの起動時に出力されたすべてのメッセージを出力します。各startup-logsバッファーは、そのhaproxyワーカーに固有です。

このキーワードはマスターCLIにもあり、直近の起動またはリロードの試行を表示します。

<a id="entry-9-3-show-table"></a>


**`show table`**


```haproxy
show table
```


認識されているすべてのスティックテーブルの概要を出力します。テーブル名（テーブルを保持するプロキシの名前）、型（現在はゼロで、常にIP）、格納可能な最大エントリー数で表したサイズ、現在使用中のエントリー数を返します。

例：

```shell
    $ echo "show table" | socat stdio /tmp/sock1
>>> # table: front_pub, type: ip, size:204800, used:171454
>>> # table: back_rdp, type: ip, size:204800, used:0
```


<a id="entry-9-3-show-table-2"></a>


**`show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |`**


```haproxy
show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |
                  [ key <key> ] | [ ptr <ptr> ]
```


スティックテーブル`<name>`の内容を出力します。このモードでは、最初の行に"show table"と同様のテーブルの概要を出力し、続いてすべてのエントリーを出力します。処理の負荷が非常に高くなることがあるため、フィルターを指定して表示するエントリーを選択できます。

"data."形式を使用すると、保存されているデータにフィルターを適用します（セクション4.2の"stick-table"を参照）。保存データの型を`<type>`に指定する必要があり、その型のデータがテーブルに保存されていなければエラーになります。データは`<operator>`に従って64ビット整数`<value>`と比較します。演算子はACLと同じです。

    - eq：データがこの値と等しいエントリをマッチ
    - ne：データがこの値と等しくないエントリをマッチ
    - le：データがこの値以下のエントリーにマッチします。
    - ge：データがこの値以上のエントリーにマッチします。
    - lt：データがこの値未満のエントリーにマッチします。
    - gt：データがこの値より大きいエントリーにマッチします。

この形式では、ビルド時に定義した上限（デフォルトは4）まで、複数のデータフィルターエントリーを使用できます。

key形式では、エントリー`<key>`を表示します。キーはテーブルと同じ型でなければなりません。現在使用できる型はIPv4、IPv6、整数、文字列に限られます。

ptr形式では、エントリー`<ptr>`を表示します。`<ptr>`は0xffffの形式で記述し、以前の"show table"コマンドが返したアドレスに対応している必要があります。キーが空であるか、CLIで使用できない文字が含まれるためにキーでエントリーを照合できない場合は、ポインターによる照合が適していることがあります。

data.`<type>`が配列型なら、"[]"で特定のインデックスへアクセスできます。たとえば、data.gpt[1]です。

例：

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1  \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.gpc0 gt 0" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.conn_rate gt 5" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy key 127.0.0.2" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy ptr 0x80e6a80" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
```


データ条件をバイトレートなどの時間に依存する動的な値に適用する場合は、エントリーの評価時に値を動的に計算して、出力するかどうかを決定します。そのため、このようなフィルターは、しばらく一致していても、時間の経過に伴って平均イベントレートが下がると一致しなくなることがあります。

この機能を使ってサービスを不正利用するIPアドレスの一覧を抽出し、監視したり、ファイアウォールのブラックリストに登録したりできます。例：

```shell
$ echo "show table http_proxy data.gpc0 gt 0" \
  | socat stdio /tmp/sock1 \
  | fgrep 'key=' | cut -d' ' -f2 | cut -d= -f2 > abusers-ip.txt
  ( または | awk '/key/{ print a[split($2,a,"=")]; }' )
```


スティックテーブルをシャーディング対応のpeersセクションと同期している場合は、各キーのシャード番号を表示します（それ以外の場合は'0'を表示します）。これにより、そのキーを受け取るピアを確認できます。例：

```shell
$ echo "show table http_proxy" | socat stdio /tmp/sock1 | fgrep shard=
  0x7f23b0c822a8: key=10.0.0.2 use=0 exp=296398 shard=9 gpc0=0
  0x7f23a063f948: key=10.0.0.6 use=0 exp=296075 shard=12 gpc0=0
  0x7f23b03920b8: key=10.0.0.8 use=0 exp=296766 shard=1 gpc0=0
  0x7f23a43c09e8: key=10.0.0.12 use=0 exp=295368 shard=8 gpc0=0
```


<a id="entry-9-3-show-tasks"></a>


**`show tasks`**


```haproxy
show tasks
```


現在実行キューにあるタスクの数を、関数ごとの出現回数および、判明している場合は平均レイテンシーとともに出力します（タスクプロファイリングを有効にした純粋なタスクの場合）。出力は実行した瞬間のスナップショットであり、その時点でキューに残っているタスクによって変動することがあります。特にシングルスレッドモードでは、I/Oがキューを再び埋める機会が少ないため、変動しやすくなります（キューがいっぱいの場合を除きます）。このコマンドはプロセスに排他的にアクセスするため、高負荷のプロセスで実行すると、小さいながらも測定可能なレイテンシーが生じることがあります。監視ボットで過度に実行してはなりません。

<a id="entry-9-3-show-threads"></a>


**`show threads`**


```haproxy
show threads
```


各スレッドの内部状態と構造の一部を出力します。開発者が問題を理解するのに役立つことがあります。読みやすくするために、スレッドごとに一つのブロックとして表示します。USE_THREAD_DUMP=1を指定してhaproxyをビルドした場合は、スレッドシグナルを使う高度な出力機構によって、各スレッドが順番に自身の状態を出力します。このオプションがない場合は、コマンドを処理するスレッドについてはすべての詳細が表示されますが、他のスレッドの詳細は少なくなります。コマンドを処理するスレッドの前には星印（'\*'）が表示されます。また、前回このコマンドを実行してから処理が進んでいないスレッドの前には、右山括弧（'\>'）が表示されることがあります。これは必ず報告しなければならないコードのバグを示します。二つのスレッド間でこの状態が起きた場合は、通常デッドロックを示します。単独のスレッドで起きた場合は、リストの破損など、別のバグです。いずれの場合も、プロセスは正常に動作しなくなっているため、再起動する必要があります。

新たな要件に応じて、後方互換性を維持することなく出力形式を変更できるように、形式は意図的に文書化していません。"show activity"と同様に、コードを参照しなければ値の意味を理解できません。

<a id="entry-9-3-show-tls-keys"></a>


**`show tls-keys [id|*]`**


```haproxy
show tls-keys [id|*]
```


読み込まれたすべてのTLSチケットキーの参照を出力します。TLSチケットキーの参照IDと、キーの読み込み元ファイルを表示します。どちらも"set ssl tls-key"でTLSキーを更新する際に使用できます。パラメーターとしてIDを指定すると、そのチケットを出力します。\*を指定すると、すべての参照のすべてのキーを出力します。

<a id="entry-9-3-show-schema-json"></a>


**`show schema json`**


```haproxy
show schema json
```


"show info json"と"show stat json"の出力に使用されるスキーマを出力します。

出力量を減らすため、余分な空白は含みません。人が読む場合は、出力を整形ツールに渡すと便利です。例：

\$ echo "show schema json" \| socat /var/run/haproxy.sock stdio \| &#92;
python -m json.tool

スキーマは"JSON Schema"（json-schema.org）に準拠しているため、検証ツールで"show info json"と"show stat json"の出力がスキーマに適合するかを確認できます。

<a id="entry-9-3-show-trace"></a>


**`show trace [<source>]`**


```haproxy
show trace [<source>]
```


現在のトレースの状態を表示します。ソースごとに一行を表示し、トレースが停止中、待機中、実行中のいずれかを一文字のステータスで示します。トレースの出力先シンク（未設定の場合は"none"）、そのシンクで破棄されたイベントの数、ソースの簡単な説明も表示します。ソース名を指定すると、そのソースがサポートするすべてのイベントと、各アクション（report、start、pause、stop）での状態を詳しく表示します。有効な場合は"+"、それ以外は"-"で示します。これらのイベントはすべて独立しており、報告されずに開始を引き起こすイベントも、その逆のイベントもあり得ます。

<a id="entry-9-3-show-version"></a>


**`show version`**


```haproxy
show version
```


現在のHAProxyプロセスのバージョンを表示します。マスターCLIとワーカーCLIの両方で使用できます。例：

```shell
$ echo "show version" | socat /var/run/haproxy.sock stdio
2.4.9

$ echo "show version" | socat /var/run/haproxy-master.sock stdio
2.5.0
```


<a id="entry-9-3-shutdown-frontend"></a>


**`shutdown frontend <frontend>`**


```haproxy
shutdown frontend <frontend>
```


指定したフロントエンドを完全に削除します。バインドしていたすべてのポートが解放されます。この操作の後で、フロントエンドを再び有効にすることはできません。プロキシの停止が到底許されないものの、誤ったプロキシ設定を修正する必要がある環境での使用を想定しています。ポートを解放して別のプロセスでバインドすることで、運用を復旧できます。終了したフロントエンドは、統計ページに一切表示されなくなります。

フロントエンドは名前またはシャープ記号（'#'）を付加した数値IDのいずれかで指定できます。

このコマンドは制限付きであり、レベル「admin」で構成されたソケットでのみ実行できます。

<a id="entry-9-3-shutdown-session"></a>


**`shutdown session <id>`**


```haproxy
shutdown session <id>
```


指定したストリーム識別子に一致するストリームを直ちに終了します。この識別子は、"show sess"の出力行の先頭にあるフィールドです（ストリームのポインターに対応します）。タイムアウトを待たずに長時間続くストリームを終了する場合や、終わりのない転送が続いている場合に使用できます。この方法で終了したストリームには、ログに'K'フラグが記録されます。

<a id="entry-9-3-shutdown-sessions-server"></a>


**`shutdown sessions server <backend>/<server>`**


```haproxy
shutdown sessions server <backend>/<server>
```


指定したサーバーに接続するすべてのストリームを直ちに終了します。たとえば、サーバーをメンテナンスモードにした後に、長時間続くストリームを終了する場合に使用できます。この方法で終了したストリームには、ログに'K'フラグが記録されます。

バックエンド接続はアイドル状態のまま残ります。ただし、サーバーがすでにメンテナンスモードの場合は、直ちに削除の対象としてスケジュールされます。

<a id="entry-9-3-trace"></a>


**`trace`**


```haproxy
trace
```


"trace"コマンドを単独で実行すると、トレースソース、その現在の状態、簡単な説明の一覧を表示します。下位レベルへ進むためのメニューにすぎません。下記の他の"trace"コマンドを参照してください。

<a id="entry-9-3-trace-0"></a>


**`trace 0`**


```haproxy
trace 0
```


すべてのトレースを直ちに停止します。デバッグセッションをすぐに終えるため、または複数のソースで複雑なトレースを有効にした結果、サービスに影響が出た場合の緊急措置として使用するものです。

<a id="entry-9-3-trace-2"></a>


**`trace <source> [<args...>]`**


```haproxy
trace <source> [<args...>]
```


ソース`<source>`のトレースを設定します。引数を指定しないと、指定したソースがサポートするすべてのサブコマンドを表示します。複数のサブコマンドを連ねることができます。次のサブコマンドをサポートしています。

event [ [+\|-\|!]`<name>` ] 引数を指定しないと、指定したソースがサポートするすべてのイベントを表示します。無効なイベントには"-"、有効なイベントには"+"が先頭に付きます。一つのトレースに複数のイベントのラベルが付くことがあり、有効なイベントのいずれかがトレースに付いたイベントのいずれかに一致すれば、そのイベントはトレースサブシステムに渡されます。たとえば、HEADERSタイプのHTTP/2フレームを受信すると、そのフレームが新しいストリームを作成するため、フレームイベントとストリームイベントの両方が発生することがあります。そのソースでフレームイベントかストリームイベントのいずれかが有効であれば、フレームはトレースフレームワークに渡されます。

    引数を指定すると、各イベントの状態を切り替え、個別に有効または無効にできます。特別なキーワードを二つサポートしています。"none"はどのイベントにも一致せず、すべてのイベントを一度に無効にします。"any"はすべてのイベントに一致し、すべてを一度に有効にします。他のイベントはイベントソースごとに異なります。イベント名を指定すると、そのイベントを有効にできます。読みやすくするために、先頭に'+'を付けてもかまいません。イベント名の先頭に'-'または'!'を付けると、そのイベントを無効にできます。

    トレースソースを完全に無効にするには、"event none"を指定する方法があります。そのソースは直ちに完全に無視されます。

follow `<other_source>` 別のソース`<other_source>`がある条件にロックオンされており、現在のソースもその条件に一致する場合に、ソース`<source>`からもトレースを出力できるようにします。たとえば、あるソースがセッションにロックオンしているときに、別のソースからそのソースを追跡すると、追跡する側もそのセッションに関連するすべてのイベントのトレースを出力します。これを利用すると、バックエンドのリクエストと関連するフロントエンド接続を、ある程度まとめて追跡できます。"session"ソースにはロックオン処理に利用できる"new"と"end"イベントがあり、この処理を容易にします。この場合、ソース`<source>`のトレースが有効である必要はなく、そのトレース状態も変わりません。ただし、追跡対象の要素と関連付けるための情報を含まないイベントは、欠落することがあります。このコマンドではメタソース"all"も使用できます。この場合、すべてのソースが`<other_source>`を追跡します。

例：

```text
trace h1 lock session start sess_new pause sess_end follow session
```


level [`<level>`] 引数を指定しないと、そのソースのすべてのトレースレベルを表示します。現在のレベルには先頭に星印（'\*'）が付きます。引数を指定すると、トレースレベルを指定したレベルに変更します。詳細レベルは、イベントを報告する前に適用するフィルターの一種です。イベントの重要度に応じて、報告に含めるか除外するかを選択します。たとえば、開発者はHTTPヘッダーがコードのどの位置で無効と判断されたかを正確に知る必要があるかもしれませんが、エンドユーザーはそのヘッダーの有効性にさえ関心がないかもしれません。現在、トレースには5つの異なるレベルがあります。

```text
user       自分のトラフィックを観察したい一般のhaproxyユーザーに適した
           情報を報告します。通常は、一部のHTTPリクエストとレスポンスを、
           詳細を省いて報告します。ほとんどのソースでは、運用を容易にするため、
           これを既定のレベルにしています。

proto      "user"レベルで報告する内容に加え、プロトコルレベルの変化も
           表示します。たとえば、フレームの種類や、デコード後の
           HTTPヘッダーなどです。

state      "proto"レベルで報告する内容に加え、パーサー内で発生した
           状態遷移（または遷移の失敗）も表示します。
           "proto"レベルが最終的な操作だけを表示するのに対し、
           このレベルでは操作を試みたことも表示します。

data       "state"レベルで報告する内容に加え、各レイヤー間の
           データ転送も含めます。

developer  利用可能な情報をすべて報告します。これには、実際の運用で
           まれにしか起きないバグを理解しようとする開発者にしか関係しない、
           "breaking out of this loop"などの詳細な情報が含まれることがあります。
           関数名が報告されるのは、このレベルだけです。
```


    常に"user"レベルだけを使用し、開発者から指示された場合に限り他のレベルへ切り替えることを強く推奨します。また、先にイベントを設定してから上位レベルに切り替えるとよいでしょう。フィルターが適用されていないために大量の行が出力される事態を防げる場合があります。このコマンドではメタソース"all"も使用できます。この場合、既存のすべてのソースに一度にそのレベルを適用します。

lock [criterion] 引数を指定しないと、そのソースがロックオン処理でサポートするすべての条件を表示します。現在の選択には先頭に星印（'\*'）が付きます。ロックオンとは、最初に一致したイベントに注目し、そのイベントを引き起こした条件だけを追跡して、トレースが停止するまで他をすべて無視することです。たとえば、単一の接続や単一のストリームをトレースできます。次の条件は一部のトレースでサポートされていますが、ソースによっては利用できない条件もあるため、必ずしもすべてをサポートしているとは限りません。

```text
backend      トレースを開始したバックエンドに固定します
connection   トレースを開始した接続に固定します
frontend     トレースを開始したフロントエンドに固定します
listener     トレースを開始したリスナーに固定します
nothing      何にも固定しません
server       トレースを開始したサーバーに固定します
session      トレースを開始したセッションに固定します
thread       トレースを開始したスレッドに固定します
```


    さらに、各ソースは内部状態や接続IDなど、固有の条件を最大4つ提供できます。たとえばHTTP/2では、H2ストリームにロックオンして、トレースが始まった後は他のストリームを無視できます。

    引数に条件を渡すと、他の条件に代えてその条件を使用し、既存の追跡を直ちに終了して、新しい条件で再開できるようにします。特別なキーワード"nothing"はすべてのソースでサポートされており、追跡を常に無効にします。

{ pause \| start \| stop } [ [+\|-\|!]event] 引数を指定しないと、そのソースのトレースを自動的に一時停止、開始、停止するために有効になっているイベントを表示します。これらのイベントはトレースソースごとに異なります。引数を指定すると、指定したアクションについてそのイベントを有効にするか（先頭に'+'を付けてもかまいません）、無効にします（先頭に'-'または'!'を付けた場合）。特別なキーワード"now"はイベントではなく、アクションを直ちに実行するよう要求します。"none"と"any"も"trace event"と同じように使用できます。

    サポートする3つのアクションは"pause"、"start"、"stop"です。"pause"アクションでは、実行中のトレースを停止し、新たな開始イベントによる再開を待つ状態にするイベントを列挙します。"start"アクションでは、開始イベントのいずれかが発生するまでトレースを待機モードにするイベントを列挙します。"stop"アクションでは、手動で再び有効にするまでトレースを完全に停止するイベントを列挙します。実際には、イベントを気にせず"start now"で手動開始し、"stop now"で停止するのが理にかなっています。より細かなイベントの連続を記録するには、"start"を通常のイベント（HTTPリクエストの受信など）、"stop"を特定のエラーの発生などの非常にまれなイベントに設定します。これにより、最後に記録されるイベントが目的の条件に一致するようになります。また、一時停止イベントは、一連の処理の終わりを検出し、ロックオンを解除して、次の記録機会を待つのに便利です。この場合、ロックオンを有効にして特定の条件（ストリームなど）だけを捉え、"start"にはその条件の始まりとなるもの（ストリームを作成するすべてのイベントなど）、"stop"には想定する異常、"pause"にはその条件の終わりとなるもの（ストリームの終了イベントなど）を設定するとよいでしょう。すると、トレースログには、単一のオブジェクトに対する正常な処理の全過程が繰り返し記録され、最後に、処理の開始から異常に至るまでのすべてを含む一連のイベントが記録されます。

sink [`<sink>`] 引数を指定しないと、そのソースで利用可能なすべてのイベントシンクを表示します。現在設定されているシンクには先頭に星印（'\*'）が付きます。シンク"none"は常に使用でき、すべてのイベントを単に破棄することを意味します。ただし、イベントの処理自体は省略しません（たとえば、ロックオンは行われます）。他のシンクは設定やビルドオプションによって異なりますが、通常はデバッグモードで"stdout"と"stderr"が使用でき、メモリ内のリングバッファーも利用できるはずです。名前を指定すると、指定したソースのシンクが直ちに変わります。シンクの変更によってイベントは変わりません。無効なシンク（または"none"）を使用すると、最悪の場合、一部のイベントが失われることがありますが、処理は別の出力先で継続します。このコマンドではメタソース"all"も使用できます。この場合、既存のすべてのソースに一度にそのシンクを適用します。

verbosity [`<level>`] 引数を指定しないと、そのソースのすべての詳細度レベルを表示します。現在のレベルには先頭に星印（'\*'）が付きます。引数を指定すると、詳細度を指定したレベルに変更します。

    詳細度レベルは、トレースデコーダーがどこまで詳しい情報を提供するかを示します。固有のデコーダーを持たないソースもあるため、トレースソースによって異なります。"quiet"レベルは常に使用でき、すべてのデコードを無効にします。パフォーマンスやトレースサイズへの影響が非常に小さいため、詳細を理解する前に何が起きているかを把握したいときに便利です。ソースが詳細度レベルを宣言していない場合は"default"レベルが使用でき、トレースでデコーダーが指定されていれば呼び出します。つまり、利用できる場合にデコードします。ソースが詳細度レベルを宣言している場合は、各レベルとその内容の説明を一覧表示します。この場合、ソースが提供するトレースデコーダーは、トレース位置で得られる情報に基づき、可能な限り正確にデコードします。デフォルトでは、"quiet"の一つ上のレベルが設定されます。

<a id="entry-9-3-update-ssl-ocsp-response"></a>


**`update ssl ocsp-response <certfile>`**


```haproxy
update ssl ocsp-response <certfile>
```


指定した`<certfile>`のOCSPリクエストを作成し、OCSPレスポンダーに送信します。レスポンダーのURIは、証明書の"Authority Information Access"セクションに指定しておくべきです。最初のURIだけを使用します。返されるはずのOCSPレスポンスを検証し、ローカルのOCSPレスポンスツリーに挿入します。このコマンドが動作するのは、初期化時に提供されたか、以前に"set ssl cert"または"set ssl ocsp-response"コマンドで設定されたOCSPレスポンスを、すでに保持している証明書だけです。受信したOCSPレスポンスが有効で、ローカルツリーに正しく挿入された場合は、その内容を標準出力に表示します。形式は"show ssl ocsp-response"で説明したものと同じです。

<a id="entry-9-3-wait"></a>


**`wait { -h | <delay> } [<condition> [<args>...]]`**


```haproxy
wait { -h | <delay> } [<condition> [<args>...]]
```


条件を指定しない最も単純な形式では、指定した時間だけ待ってから処理を続けます。特定の間隔を空けてメトリクスを収集する場合に使用できます。

条件と任意の引数を指定すると、その条件が満たされるか、回復不能な失敗となるか、条件が満たされないまま`<delay>`の時間がすべて経過するまで待機します。次の条件をサポートしています。

- be-removable `<proxy>`：指定したプロキシのバックエンドを"del backend"コマンドで削除できるようになるまで待機します。決して受け入れられない状態（バックエンドがまだ非公開になっていない、またはサーバーが残っている場合など）もあり、その場合は、満たされていない条件を示す固有のエラーメッセージを返します。待機時間が経過する前にすべての条件が整えば、成功を返して処理を終了します。

- srv-removable `<proxy>`/`<server>`：指定したサーバーを"del server"コマンドで削除できるようになるまで待機します。つまり、メンテナンス状態にあり、アクティブな接続もアイドル接続も残っていない状態を待ちます。決して受け入れられない状態（メンテナンス状態ではない場合など）もあり、その場合は、満たされていない条件を示す固有のエラーメッセージを返します。並行してサーバーが削除され、すでに存在しない場合もあります。待機時間が経過する前にすべての条件が整えば、成功を返して処理を終了します。

待機時間のデフォルト単位はミリ秒ですが、通常の時間単位（us、ms、s、m、h、d）を末尾に付ければ、他の単位も使用できます。'socat'ユーティリティと併用する場合は、socatのクローズタイムアウトを待機時間に合わせて延長することを忘れないでください。最初または二番目の引数に"-h"を渡すと、コマンドの使用方法を表示します。例：

```shell
$ socat -t20 /path/to/socket - <<< "show activity; wait 10s; show activity"

$ socat -t5 /path/to/socket - <<< "
    disable server px/srv1
    shutdown sessions server px/srv1
    wait 2s srv-removable px/srv1
    del server px/srv1"
```


## 9.4. マスターCLI {#section-9-4}


マスターCLIは、master-workerモードでマスタープロセスにバインドされるソケットです。このCLIから、実行中または終了処理中の各プロセスのUNIXソケットコマンドにアクセスでき、これらのプロセスの基本的な監視を行えます。

マスターCLIは、haproxyプログラムの引数に-Sオプションを指定する方法でのみ設定できます。このオプションには、コンマで区切ったbindオプションも指定できます。

例：

```haproxy
# haproxy -W -S 127.0.0.1:1234 -f test1.cfg
# haproxy -Ws -S /tmp/master-socket,uid,1000,gid,1000,mode,600 -f test1.cfg
# haproxy -W -S /tmp/master-socket,level,user -f test1.cfg
```


### 9.4.1. マスターCLIのコマンド {#section-9-4-1}


<a id="entry-9-4-1-entry"></a>


**`@<[!]pid>`**


```haproxy
@<[!]pid>
```


マスターCLIでは、特別な接頭辞表記で複数のプロセスにアクセスします。この表記は@で始まるため、簡単に識別できます。

@接頭辞の後には、相対プロセス番号、または感嘆符とPIDを指定できます（例：@1、@!1271）。@だけを指定すると、マスターを指定できます。相対プロセス番号は現在のプロセスにしか使用できないため、終了処理中のプロセスにはPIDでのみアクセスできます。

この接頭辞をコマンドの前にラッパーとして付けると、そのコマンドだけを指定したプロセスに送信します。この場合、通常のコマンドと同様に、行末またはセミコロンでコマンド全体が終了します。

バグ：マスターとワーカー間の通信に使うsockpair@プロトコルは、macOSのsendmsg(2)実装の問題により、macOSでは信頼性に問題があることが知られています。そのため、コマンドが応答のないまま終わることがあります。

例：

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1 show info; @2 show info
[...]
Process_num: 1
Pid: 1271
[...]
Process_num: 2
Pid: 1272
[...]
master>

$ echo '@!1271 show info; @!1272 show info' | socat /var/run/haproxy-master.sock -
[...]
```


接頭辞を単独のコマンドとして使用して、デフォルトの実行コンテキストを指定したプロセスに切り替えることもできます。以後のコマンドは、新たな'@'コマンドで再び実行コンテキストを変更するまで、すべてそのプロセスで実行されます。

例：

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1
1271> show info
[...]
1271> show stat
[...]
1271> @
master>

$ echo '@1; show info; show stat; @2; show info; show stat' | socat /var/run/haproxy-master.sock -
[...]
```


制限事項：一部のまれなコマンドはCLIセッションの状態を変更します（"set anon"、"set timeout"など）。マスターCLIからは、コマンドがそれぞれ専用のCLIセッションで一つずつ送られるため、まったく同じようには動作しないことがあります。また、一部のまれなコマンド（"show events"、"wait"）は、CLIの入力や切断を継続的に監視し、CLIが閉じられると直ちに中断します。マスターCLIでは、コマンドごとに入力が閉じられるため、これらのコマンドは期待どおりに動作しません。このようなまれな場合には、下記の"@@"形式がより適している場合があります。

<a id="entry-9-4-1-entry-2"></a>


**`@@<[!]pid> [command...]`**


```haproxy
@@<[!]pid> [command...]
```


この接頭辞またはコマンドは、上記の"@"接頭辞とよく似ていますが、ワーカープロセスに入り、コマンド行全体をそのまま渡して、コマンドが終了するまでそこに留まる点が異なります。セミコロンも渡されるため、連結したコマンド全体をワーカープロセスで実行できます。コマンドの一覧を実行し終えるまで、ワーカーとの接続は開いたままです。コマンドの後に送信したデータは、ワーカープロセスのCLIに転送され、実行中のコマンドが消費する可能性があります。マスタープロセスのCLIには戻りません。これにより、ワーカープロセスとの完全な双方向接続を実現します。そのため、このようなコマンドを使用する場合は、マスターCLIへ次のコマンドを送る前に、必ず実行中のコマンドの完了を待つよう十分に注意しなければなりません。

単一のコマンドを実行する代わりに、コマンドを何も指定せず（つまり、一行に"@@1"だけを記述して）、ワーカープロセスで完全な対話型セッションを開くこともできます。このセッションは、接続を閉じるか、ワーカープロセス側で"quit"コマンドを実行して終了できます。この場合、マスターソケットのプロンプトモード（interactive、prompt、timed）がワーカープロセスに引き継がれます。

バグ：マスターとワーカー間の通信に使うsockpair@プロトコルは、macOSのsendmsg(2)実装の問題により、macOSでは信頼性に問題があることが知られています。そのため、コマンドが応答のないまま終わることがあります。

例：

```shell
# gracefully close connections and delete a server once idle (wait max 10s)
$ socat -t 11 /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   wait 10000 srv-removable app2/srv36; \
   del server app2/srv36"

# forcefully close connections and quickly delete a server
$ socat /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   shutdown sessions server app2/srv36; \
   wait 100 srv-removable app2/srv36; \
   del server app2/srv36"

# show messages arriving to this ring in real time ("tail -f" equivalent)
$ (echo "show events buf0 -w"; read) | socat /var/run/haproxy-master.sock -
```


<a id="entry-9-4-1-expert-mode"></a>


**`expert-mode [on|off]`**


```haproxy
expert-mode [on|off]
```


このコマンドは、マスターCLIからアクセスするすべてのワーカーで"expert-mode"を有効にします。"mcli-debug-mode"と組み合わせると、マスターでもこのコマンドを有効にします。マスターCLIのプロンプトに"e"フラグを表示します。

[セクション9.3](/ja/docs/haproxy/statistics-and-monitoring/#section-9-3)の"expert-mode"および9.4.1の"mcli-debug-mode"も参照してください。

<a id="entry-9-4-1-experimental-mode"></a>


**`experimental-mode [on|off]`**


```haproxy
experimental-mode [on|off]
```


このコマンドは、マスターCLIからアクセスするすべてのワーカーで"experimental-mode"を有効にします。"mcli-debug-mode"と組み合わせると、マスターでもこのコマンドを有効にします。マスターCLIのプロンプトに"x"フラグを表示します。

[セクション9.3](/ja/docs/haproxy/statistics-and-monitoring/#section-9-3)の"experimental-mode"および9.4.1の"mcli-debug-mode"も参照してください。

<a id="entry-9-4-1-hard-reload"></a>


**`hard-reload`**


```haproxy
hard-reload
```


このコマンドは、マスターCLIの"reload"コマンドと同じ処理を行いますが、以前のプロセスに対してstop-stop（-sf）の代わりにhard-stop（-st）を行います。つまり、以前のプロセスは処理の完了を何も待たずに終了するため、すべての接続が閉じられます。

"reload"コマンドも参照してください。

<a id="entry-9-4-1-mcli-debug-mode"></a>


**`mcli-debug-mode [on|off]`**


```haproxy
mcli-debug-mode [on|off]
```


このキーワードは、マスターCLIで特別なモードを有効にします。ワーカーCLI向けのすべてのキーワードをマスターCLIで使用できるようにして、マスタープロセスをデバッグできます。有効にした後は、"help"で新たに使用可能になったキーワードを一覧表示できます。"experimental-mode"または"expert-mode"と組み合わせると、さらに多くのキーワードを有効にできます。マスターCLIのプロンプトに"d"フラグを表示します。

<a id="entry-9-4-1-prompt"></a>


**`prompt`**


```haproxy
prompt
```


（"prompt"コマンドで）プロンプトを有効にすると、CLIが処理対象としているコンテキストをプロンプトに表示します。マスターは"master"文字列、他のプロセスはPIDで識別します。直前のリロードが失敗した場合は、マスターのプロンプトが"master[ReloadFailed]\>"に変わり、プロセスが以前の設定で動作し続けていて、新しい設定が有効になっていないことが分かります。

マスターCLIのプロンプトには、有効なモードを示す複数のフラグを表示できます。"d"はmcli-debug-mode、"e"はexpert-mode、"x"はexperimental-modeを示します。

例：

```shell
$ socat /var/run/haproxy-master.sock -
prompt
master> expert-mode on
master(e)> experimental-mode on
master(xe)> mcli-debug-mode on
master(xed)> @1
95191(xed)>
```


<a id="entry-9-4-1-reload"></a>


**`reload`**


```haproxy
reload
```


ユーザーに少なくとも"operator"または"admin"権限があれば、"reload"コマンドでHAProxyのマスタープロセスをリロードすることもできます。これは、マスタープロセスに対して`kill -USR2`を実行するのと同じです。

このコマンドでは同期的にリロードできます。リロードを実行した後、そのステータスを返します。ツールで結果を解析する場合は、タイムアウトに注意してください。設定の解析と新しいワーカーのforkが終わるまで、結果は返りません。"socat"コマンドのデフォルトのタイムアウトは0.5sなので、リロードに時間がかかりすぎると、メッセージを表示する前に終了します。"ncat"にはデフォルトではタイムアウトがありません。USE_SHM_OPEN=1でコンパイルした場合は、reloadコマンドでマスターのstartup-logsも出力できます。

例：

```shell
$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=1
--
[NOTICE]   (482713): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482713): path to executable is ./haproxy
[WARNING]  (482713): config: 'http-request' rules ignored for proxy 'frt1' as they require HTTP mode.
[NOTICE]   (482713): New worker (482720) forked
[NOTICE]   (482713): Loading success.

$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=0
--
[NOTICE]   (482886): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482886): path to executable is ./haproxy
[ALERT]    (482886): config: parsing [test3.cfg:1]: unknown keyword 'Aglobal' out of section.
[ALERT]    (482886): config: Fatal errors found in configuration.
[WARNING]  (482886): Loading failure!

$
```


reloadコマンドはマスターCLIで実行される最後のコマンドであり、その後のコマンドはすべて無視されます。reloadコマンドがステータスを返すと、CLIへの接続を閉じます。

リロードすると、マスターCLIへのすべての接続が閉じられることに注意してください。"hard-reload"コマンドも参照してください。

<a id="entry-9-4-1-show-proc"></a>


**`show proc [debug]`**


```haproxy
show proc [debug]
```


マスターCLIには、プロセスを監視する'show proc'コマンドがあります。

例：

```shell
$ echo 'show proc' | socat /var/run/haproxy-master.sock -
#<PID>          <type>          <reloads>       <uptime>        <version>
1162            master          5 [failed: 0]   0d00h02m07s     2.5-dev13
# workers
1271            worker          1               0d00h00m00s     2.5-dev13
# old workers
1233            worker          3               0d00h00m43s     2.0-dev3-6019f6-289
```


この例では、マスターが5回リロードされていますが、以前のワーカーの一つがまだ動作しており、3回のリロードを経ても残っています。このワーカーのCLIにアクセスして、何が起きているかを調べることができます。

'debug'パラメーターは、デバッグ用の詳細を表示するのに便利です。現在はIPC通信用のFDを表示します。デバッグ出力がhaproxyのバージョン間で安定している保証はありません。

<a id="entry-9-4-1-show-startup-logs"></a>


**`show startup-logs`**


```haproxy
show startup-logs
```


マスターCLIで正しく使用するには、HAProxyをUSE_SHM_OPEN=1でコンパイルする必要があります。そうしないと、すべてのメッセージを確認できません。

統計ソケットの同名コマンドと同様に、HAProxyの起動メッセージを表示できます。ただし、出力するのは現在のワーカーの起動メッセージではなく、直近の起動またはリロード時のメッセージです。そのため、リロードが失敗した際の解析メッセージも出力できます。

これらのメッセージは"reload"コマンドでも出力します。

## 9.5. 統計ファイル {#section-9-5}


stats-fileと呼ばれるファイルを使用すると、プロセスの起動時に、haproxy内部のカウンターにゼロ以外の値を事前に読み込めます。主な目的は、ワーカープロセスの統計値をリロード後も維持することです。事前に読み込む意味があるのはメトリクス型の値だけなので、stats-fileに含まれるのは、haproxyが公開する統計値の一部だけです。

現在、stats-fileがサポートするのはプロキシのカウンターだけです。フロントエンド、バックエンド、サーバー、リスナーの値を事前に読み込めます。ただし、stats-fileに保存されるのは、GUIDが空でないオブジェクトのインスタンスだけです。これにより、他のパラメーターが異なっていても、型とGUIDが一致するオブジェクトに値を事前に読み込むことが保証されます。

CLIコマンド"dump stats-file"は、stats-fileを生成するためのものです。stats-fileの形式は内部で定義されており、今後自由に変更や拡張が行われる可能性があります。少なくとも隣接するhaproxy安定ブランチのリリース間では互換性を維持する設計ですが、古いバージョンで動作するプロセスにstats-fileを読み込む場合は、必要に応じて追加の設定が求められることがあります。
