---
title: "7. ACLとサンプル取得"
linkTitle: "7. ACLとサンプル"
weight: 180
description: "ACLの照合、条件、コンバーター、サンプル取得、定義済みACL"
icon: fa-solid fa-filter
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/acls-and-samples/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 7"
---

HAProxyは、リクエストやレスポンスのストリーム、クライアントやサーバーの情報、テーブル、環境情報などからデータを抽出できます。このデータ抽出をサンプル取得と呼びます。取得したサンプルはスティックテーブルのキーなど、さまざまな用途に使用できますが、最も一般的な用途は、パターンと呼ばれる定義済みの定数データとの照合です。

## 7.1. ACLの基本 {#section-7-1}

アクセス制御リスト（ACL）は、任意の情報を定義済みパターンのリストと比較するための、名前付きの方法を宣言するものです。宣言しておくと後から必要に応じて呼び出せるという点で、多くのプログラミング言語の関数と実質的に同等と考えるとよいでしょう。評価の結果は一致または不一致のみで、多くのプログラミング言語の真偽値に相当します。プログラミング言語の関数とは異なり、ACLは同じ名前に照合方法を追加するために、必要なだけ重ねて定義できます。この場合、一致するものが見つかるまで、宣言順にすべて評価されます。

ACLを使用すると、コンテンツに応じた振り分けや、より一般的にはリクエスト、レスポンス、環境の状態から抽出した内容に基づく判断を柔軟に行えます。原理は単純です。

- ストリーム、テーブル、環境からデータサンプルを抽出します
- 必要に応じて、抽出したサンプルの形式を変換します
- サンプルに1つまたは複数のパターン照合方法を適用します
- パターンがサンプルと一致した場合にのみアクションを実行します

アクションは通常、リクエストのブロック、バックエンドの選択、ヘッダーの追加です。

テストを定義するには、"acl"キーワードを使用します。構文は次のとおりです。

```text
acl <aclname> <criterion> [flags] [operator] [<value>] ...
```

これにより、新しいACL `<aclname>`を作成するか、既存のACLに新しいテストを追加します。これらのテストは、`<criterion>`で指定したリクエストまたはレスポンスの部分に適用され、省略可能なフラグ[flags]で調整できます。一部の条件は演算子にも対応しており、値の集合の前に指定できます。必要に応じてサンプルに変換演算子を適用することもでき、最初のキーワードの直後にキーワードをコンマ区切りで指定します。値は条件が対応する型で指定し、空白で区切ります。

ACL名は、大文字と小文字の英字、数字、'-'（ダッシュ）、'\_'（アンダースコア）、'.'（ドット）、':'（コロン）で構成する必要があります。ACL名は大文字と小文字を区別するため、"my_acl"と"My_Acl"は異なるACLです。

ACLの数に強制的な上限はありません。使用しないACLは少量のメモリーを消費するだけで、パフォーマンスには影響しません。

条件は通常、サンプル取得方法の名前、またはそのACL専用の派生形です。デフォルトのテスト方法は、サンプル取得方法の出力型によって暗黙的に決まります。ACLの派生形では、同じサンプル取得方法に対して別の照合方法を指定できます。変換に対応しているのは、サンプル取得方法だけです。

サンプル取得方法は、次のいずれかの型のデータを返します。

- 真偽値
- 整数（符号付きまたは符号なし）
- IPv4またはIPv6アドレス
- 文字列
- データブロック

コンバーターは、これらのデータを、いずれかの型のデータに変換します。たとえば、文字列を小文字の文字列に変換するコンバーターもあれば、文字列をIPv4アドレスに変換したり、IPアドレスにネットマスクを適用したりするコンバーターもあります。結果のサンプルの型は、リスト内で最後に適用したコンバーターの型になります。コンバーターを適用しない場合は、サンプル取得方法の型が使用されます。

各サンプルまたはコンバーターは特定の型のデータを返します。その型は、このドキュメントの各キーワードの説明に記載されています。標準のサンプル取得方法を使用してACLを宣言すると、一部の型では自動的にデフォルトの照合方法が適用されます。次の表にまとめます。

```text
   +---------------------+-----------------+
   |サンプル/コンバーター|  デフォルトの   |
   |       出力型        |    照合方法     |
   +---------------------+-----------------+
   | boolean             | bool            |
   +---------------------+-----------------+
   | integer             | int             |
   +---------------------+-----------------+
   | ip                  | ip              |
   +---------------------+-----------------+
   | string              | str             |
   +---------------------+-----------------+
   | binary              | なし、"-m"使用  |
   +---------------------+-----------------+
```

バイナリーサンプルを照合するには、照合方法を必ず指定する必要があります。以下を参照してください。

ACLエンジンは、これらの型を次の型のパターンと照合できます。

- 真偽値
- 整数または整数範囲
- IPアドレス/ネットワーク
- 文字列（完全一致、部分文字列、接尾辞、接頭辞、サブディレクトリ、ドメイン）
- 正規表現
- 16進数のブロック

現在、次のACLフラグがサポートされています。

```text
-i: これ以降のすべてのパターンの照合で、大文字と小文字を区別しません。
-f: リストからパターンを読み込みます。
-m: 特定のパターン照合方法を使用します。
-n: DNS解決を禁止します。
-M: -fが指すファイルをマップとして読み込みます。
-u: ACLの一意のIDを強制的に指定します。
--: フラグの終わりを強制します。文字列がフラグのように見える場合に役立ちます。
```

"-f"フラグの後には名前を指定します。この名前は、マップとACLの名前の形式について説明した2.7.の形式に従う必要があります。複数のリストからパターンを読み込む場合は、"-f"引数を複数指定することもできます。既存のファイルを参照する場合、すべての行が個別の値として読み込まれます。空行とシャープ（'#'）で始まる行は無視されます。行頭の空白とタブはすべて削除されます。シャープで始まる有効なパターンをどうしても挿入する必要がある場合は、先頭に空白を付けることで、コメントと見なされないようにできます。データ型と照合方法に応じて、HAProxyは行を二分木に読み込み、非常に高速な検索を可能にすることがあります。IPv4と文字列の完全一致はこれに該当します。この場合、重複は自動的に削除されます。

"-M"フラグを指定すると、ACLでマップを使用できます。このフラグが設定されている場合、リストは2列のエントリーとして解析されます。第1列にはACLが使用するパターン、第2列にはサンプルが含まれます。サンプルは後からマップで使用できます。これは、マッピングを適用する前にマップ内のパターンの有無だけをACLで確認するという、まれなケースで役立ちます。

"-u"フラグは、ACLの一意のIDを強制的に指定します。この一意のIDは、ソケットインターフェースでACLを識別し、その値を動的に変更するために使用します。ファイルは、IDを設定しても常に名前で識別される点に注意してください。

また、"-i"フラグが適用されるのは、それ以降のエントリーです。それより前にファイルから読み込んだエントリーには適用されません。次に例を示します。

```text
acl valid-ua hdr(user-agent) -f exact-ua.lst -i -f generic-ua.lst test
```

この例では、"exact-ua.lst"の各行は、リクエストの"user-agent"ヘッダーと完全一致で照合されます。次に、"generic-ua"の各行は、大文字と小文字を区別せずに照合されます。その後、単語"test"も、大文字と小文字を区別せずに照合されます。

"-m"フラグは、入力サンプルに対する特定のパターン照合方法を選択するために使用します。ACL専用の条件はすべて照合方法を暗黙的に指定するため、通常はこのフラグが不要です。ただし、汎用のサンプル取得方法で、パターンとの照合方法を指定する場合に役立ちます。明確な照合方法がないデータ型（文字列やバイナリーなど）を返すサンプル取得には、この指定が必要です。"-m"の後にパターン照合方法の名前を指定すると、その条件のデフォルトの照合方法に代わって、指定した方法が使用されます。これにより、当初想定されていなかった方法や、文字列を返すサンプル取得方法で内容を照合できます。照合方法は、パターンの解析方法にも影響します。そのため、照合用の接尾辞（\_beg、\_end、\_sub...）が付いたサンプル取得と併用してはいけません。また、"-m"で複数のパターン照合方法を指定することもできません。

"-n"フラグは、DNS解決を禁止します。IPファイルの読み込み時に使用します。デフォルトでは、パーサーがIPアドレスを解析できない場合、解析した文字列をドメイン名の可能性があると見なし、DNS解決を試みます。"-n"フラグは、この名前解決を無効にします。不正なIPリストの検出に役立ちます。DNSサーバーに到達できない場合、タイムアウトを待つためにHAProxyの設定解析に何分もかかることがあります。その間、エラーメッセージは表示されません。"-n"フラグは、この動作を無効にします。また、実行時のACLの動的な変更では、この名前解決機能が無効になっている点にも注意してください。

ただし、いくつか制限があります。すべての照合方法を、すべてのサンプル取得方法で使用できるわけではありません。また、"-m"と"-f"を併用する場合、"-m"を先に指定する必要があります。パターン照合方法は、次のいずれかでなければなりません。

- "found": 要求したサンプルがストリーム内に見つかるかどうかだけを確認し、パターンとの比較は行いません。
  混乱を避けるため、パターンを指定しないことを推奨します。この照合方法は、ヘッダーやCookieなどの
  特定の内容の有無を検出するのに特に役立ちます。内容が空でも検出でき、比較やカウントは不要です。

- "bool" : 値を真偽値として確認します。真偽値または整数値を返す取得方法にのみ適用でき、
  パターンは指定しません。値がゼロまたはfalseの場合は一致せず、それ以外の値はすべて一致します。

- "int" : 値を整数として照合します。整数と真偽値のサンプルに使用できます。
  真偽値のfalseは整数の0、trueは整数の1に相当します。

- "ip" : 値をIPv4またはIPv6アドレスとして照合します。IPアドレスのサンプルでのみ使用でき、
  暗黙的に適用されるため、明示的に指定する必要はありません。

- "bin" : 内容を、バイナリー列を表す16進文字列と照合します。
  バイナリーまたは文字列のサンプルに使用できます。

- "len" : サンプルの長さを整数として照合します。バイナリーまたは文字列のサンプルに使用できます。

- "str" : 完全一致：内容を文字列と照合します。
  バイナリーまたは文字列のサンプルに使用できます。

- "sub" : 部分文字列の照合：内容に、指定した文字列パターンの少なくとも1つが含まれるか確認します。
  バイナリーまたは文字列のサンプルに使用できます。

- "reg" : 正規表現の照合：内容を正規表現のリストと照合します。
  バイナリーまたは文字列のサンプルに使用できます。

- "beg" : 接頭辞の照合：内容の先頭が、指定した文字列パターンと一致するか確認します。
  バイナリーまたは文字列のサンプルに使用できます。

- "end" : 接尾辞の照合：内容の末尾が、指定した文字列パターンと一致するか確認します。
  バイナリーまたは文字列のサンプルに使用できます。

- "dir" : サブディレクトリの照合：内容のうちスラッシュで区切られた部分が、指定した文字列パターンの
  いずれかと完全に一致するか確認します。バイナリーまたは文字列のサンプルに使用できます。

- "dom" : ドメインの照合：内容のうちドットで区切られた部分が、指定した文字列パターンのいずれかと
  完全に一致するか確認します。バイナリーまたは文字列のサンプルに使用できます。

たとえば、HTTPリクエスト内のCookie "JSESSIONID"の有無をすばやく検出するには、次のように指定できます。

```text
acl jsess_present req.cook(JSESSIONID) -m found
```

バッファー内のデータの先頭500バイトに正規表現を適用するには、次のACLを使用します。

```text
acl script_tag req.payload(0,500) -m reg -i <script>
```

"-i"を使用すると正規表現ライブラリーが大幅に遅くなるシステムでは、次のように照合前にサンプルを小文字に変換できます。

```text
acl script_tag req.payload(0,500),lower -m reg <script>
```

ACL専用の条件には、すべてデフォルトの照合方法が暗黙的に指定されています。これらの条件は通常、元のサンプル取得方法の名前と照合方法を連結した名前になっています。たとえば、"hdr_beg"は、"hdr"取得方法で取得したサンプルに"beg"による照合を適用します。この照合方法を使用できるのは、コンバーターを付けず、キーワードを単独で使用した場合だけです。このようなACLキーワードの後にコンバーターを適用した場合、照合で重要になるのは最後のコンバーターの出力型であるため、ACLキーワードのデフォルトの照合方法は単に無視されます。ACL専用の条件はすべてサンプル取得方法に基づいているため、代わりに元のサンプル取得方法を使用し、"-m"で照合方法を明示的に指定することが常に可能です。

ACL専用の条件に対して"-m"で別の照合方法を指定した場合、その照合方法が基となるサンプル取得方法にそのまま適用されます。たとえば、次のACLはすべて完全に等価です。

```text
acl short_form  hdr_beg(host)        www.
acl alternate1  hdr_beg(host) -m beg www.
acl alternate2  hdr_dom(host) -m beg www.
acl alternate3  hdr(host)     -m beg www.

```

次の表は、サンプルまたはコンバーターの型と、照合対象のパターンの型との互換性をまとめたものです。互換性のある組み合わせごとに、使用する照合方法の名前を示しています。その方法がデフォルトで、"-m"なしで動作する場合は、山括弧"\>"と"\<"で囲んでいます。

```text
                           +-------------------------------------------------+
                           |                入力サンプルの型                 |
    +----------------------+---------+---------+---------+---------+---------+
    |     パターンの型     | boolean | integer |   ip    | string  | binary  |
    +----------------------+---------+---------+---------+---------+---------+
    |   なし（有無のみ）   |  found  |  found  |  found  |  found  |  found  |
    +----------------------+---------+---------+---------+---------+---------+
    |    なし（真偽値）    |>  bool <|   bool  |         |   bool  |         |
    +----------------------+---------+---------+---------+---------+---------+
    |      整数（値）      |   int   |>  int  <|   int   |   int   |         |
    +----------------------+---------+---------+---------+---------+---------+
    |     整数（長さ）     |   len   |   len   |   len   |   len   |   len   |
    +----------------------+---------+---------+---------+---------+---------+
    |      IPアドレス      |         |         |>   ip  <|    ip   |    ip   |
    +----------------------+---------+---------+---------+---------+---------+
    |   文字列の完全一致   |   str   |   str   |   str   |>  str  <|   str   |
    +----------------------+---------+---------+---------+---------+---------+
    |        接頭辞        |   beg   |   beg   |   beg   |   beg   |   beg   |
    +----------------------+---------+---------+---------+---------+---------+
    |        接尾辞        |   end   |   end   |   end   |   end   |   end   |
    +----------------------+---------+---------+---------+---------+---------+
    |      部分文字列      |   sub   |   sub   |   sub   |   sub   |   sub   |
    +----------------------+---------+---------+---------+---------+---------+
    |   サブディレクトリ   |   dir   |   dir   |   dir   |   dir   |   dir   |
    +----------------------+---------+---------+---------+---------+---------+
    |       ドメイン       |   dom   |   dom   |   dom   |   dom   |   dom   |
    +----------------------+---------+---------+---------+---------+---------+
    |       正規表現       |   reg   |   reg   |   reg   |   reg   |   reg   |
    +----------------------+---------+---------+---------+---------+---------+
    |   16進数のブロック   |         |         |         |   bin   |   bin   |
    +----------------------+---------+---------+---------+---------+---------+
```

### 7.1.1. 真偽値の照合 {#section-7-1-1}

真偽値の照合には値が不要で、指定した値はすべて無視されます。型が"boolean"のすべての取得方法では、デフォルトで真偽値による照合を使用します。真偽値による照合では、取得した値をそのまま返します。したがって、真偽値の"true"は常に一致し、"false"は決して一致しません。

整数値を返す取得方法でも、"-m bool"で真偽値による照合を強制できます。この場合、整数値の0は真偽値の"false"に変換され、それ以外のすべての値は"true"に変換されます。

### 7.1.2. 整数の照合 {#section-7-1-2}

整数の取得方法では、デフォルトで整数による照合を使用します。真偽値の取得でも、"-m int"で整数による照合を強制できます。この場合、"false"は整数の0に、"true"は整数の1に変換されます。

整数による照合は、整数範囲と演算子にも対応しています。整数による照合が適用されるのは正の値だけである点に注意してください。範囲は、下限と上限をコロンで区切って表す値です。どちらの境界も省略できます。

たとえば、"1024:65535"は非特権ポートの範囲を表す有効な指定で、"1024:"も同様に使用できます。"0:1023"は特権ポートを表す有効な指定で、":1023"も同様に使用できます。

特別なケースとして、一部のACL関数は小数に対応していますが、これは実際にはドットで区切られた2つの整数です。たとえば、一部のバージョン検査で使用されます。範囲や演算子を含め、整数のすべての性質が、この小数にも適用されます。

使いやすくするため、比較演算子もサポートされています。範囲と演算子を併用してもあまり意味がなく、併用を避けることが強く推奨されている点に注意してください。同様に、値の集合に対して大小を比較することにも、あまり意味はありません。

整数の照合で使用できる演算子は次のとおりです。

```text
eq: 検査した値が、指定した値のいずれかと等しければtrue
ge: 検査した値が、指定した値のいずれか以上であればtrue
gt: 検査した値が、指定した値のいずれかより大きければtrue
le: 検査した値が、指定した値のいずれか以下であればtrue
lt: 検査した値が、指定した値のいずれかより小さければtrue
```

たとえば、次のACLは、値が負のContent-Lengthヘッダーに一致します。

```text
acl negative-length req.hdr_val(content-length) lt 0
```

次のACLは、3.0から3.1まで（両端を含む）のSSLバージョンに一致します。

```text
acl sslv3 req.ssl_ver 3:3.1
```

### 7.1.3. 文字列の照合 {#section-7-1-3}

文字列の照合は、文字列またはバイナリーの取得方法に適用され、次の6つの形式があります。

- 完全一致（-m str）：抽出した文字列がパターンと完全に一致する必要があります。

- 部分文字列の照合（-m sub）：抽出した文字列内でパターンを検索し、
  いずれかが見つかるとACLが一致します。

- 接頭辞の照合（-m beg）：抽出した文字列の先頭とパターンを比較し、
  いずれかが一致するとACLが一致します。

- 接尾辞の照合（-m end）：抽出した文字列の末尾とパターンを比較し、
  いずれかが一致するとACLが一致します。

- サブディレクトリの照合（-m dir）：抽出した文字列内の任意の位置で、スラッシュ（"/"）、
  文字列の先頭または末尾を境界としてパターンを検索します。いずれかのパターンが一致すると
  ACLが一致します。たとえば、文字列"/images/png/logo/32x32.png"は、"/images"、"/images/png"、
  "images/png"、"/png/logo"、"logo/32x32.png"、"32x32.png"に一致しますが、"png"や"32x32"には一致しません。

- ドメインの照合（-m dom）：抽出した文字列内の任意の位置で、ドット（"."）、コロン（":"）、
  スラッシュ（"/"）、疑問符（"?"）、文字列の先頭または末尾を境界としてパターンを検索します。
  これはURLで使用するためのものです。パターンの先頭と末尾の区切り文字は無視されます。
  いずれかのパターンが一致するとACLが一致します。たとえば、文字列
  "<http://www1.dc-eu.example.com:80/blah>"には、"http"、"www1"、".www1"、"dc-eu"、
  "example"、"com"、"80"、"dc-eu.example"、"blah"、":www1:"、"dc-eu.example:80"が一致しますが、
  "eu"や"dc"には一致しません。フィルタリングやルーティングでドメインの接尾辞を照合する用途には、
  一般に適していません。たとえば、別のドメインの前に一致する接頭辞を付けるだけで、
  ルーティングを簡単に欺けるためです。

文字列の照合は、渡された文字列をそのまま使用します。ただし、バックスラッシュ（"&#92;"）は例外で、空白などの文字をエスケープするために使用できます。最初の文字列の前に"-i"フラグを指定すると、大文字と小文字を区別せずに照合します。文字列"-i"と照合するには、これを2番目に指定するか、最初の文字列の前に"--"フラグを指定します。もちろん、文字列"--"と照合する場合も同様です。

ヌルバイト（0x00）を含む可能性があるバイナリーの取得に、文字列の照合を使用しないでください。最初のヌルバイトが現れた時点で比較が停止するためです。代わりに、まずhexコンバーターで取得したバイナリーを16進文字列に変換してください。

例：

```shell
# matches if the string <tag> is present in the binary sample
acl tag_found req.payload(0,0),hex -m sub 3C7461673E
```

### 7.1.4. 正規表現（regex）による照合 {#section-7-1-4}

文字列の照合と同様に、正規表現の照合も渡された文字列をそのまま使用します。ただし、バックスラッシュ（"&#92;"）は例外で、空白などの文字をエスケープするために使用できます。最初の正規表現の前に"-i"フラグを指定すると、大文字と小文字を区別せずに照合します。文字列"-i"と照合するには、これを2番目に指定するか、最初の文字列の前に"--"フラグを指定します。もちろん、文字列"--"と照合する場合も同じ原理が適用されます。

### 7.1.5. 任意のデータブロックの照合 {#section-7-1-5}

抽出したサンプルを、文字列として安全に表現できないバイナリーブロックと照合することもできます。この場合、照合方法をバイナリーに設定し、偶数個の16進数字の列としてパターンを渡す必要があります。2桁ごとの並びが1バイトを表します。16進数字には、大文字と小文字のどちらも使用できます。

例：

```shell
# match "Hello\n" in the input stream (\x48 \x65 \x6c \x6c \x6f \x0a)
acl hello req.payload(0,6) -m bin 48656c6c6f0a
```

### 7.1.6. IPv4アドレスとIPv6アドレスの照合 {#section-7-1-6}

IPv4アドレスの値は、単なるアドレスとして指定することも、末尾にネットマスクを付けて指定することもできます。ネットマスクを付けた場合、IPv4アドレスがそのネットワーク内にあれば一致します。単なるアドレスの代わりに、名前解決可能なホスト名を指定することもできますが、設定が読みにくく、デバッグしにくくなるため、一般に推奨されません。ホスト名を使用する場合は、設定解析時の不確定なDNSの応答に設定が依存しないように、少なくとも/etc/hostsにホスト名が登録されていることを確認することを推奨します。

ドット区切りのIPv4アドレス表記は、通常の形式と、値がすべて0のオクテットを省略した短縮形式の両方に対応しています。

```text
    +------------------+------------------+------------------+
    |       例1        |       例2        |       例3        |
    +------------------+------------------+------------------+
    |  192.168.0.1     |   10.0.0.12      |   127.0.0.1      |
    |  192.168.1       |   10.12          |   127.1          |
    |  192.168.0.1/22  |   10.0.0.12/8    |   127.0.0.1/8    |
    |  192.168.1/22    |   10.12/8        |   127.1/8        |
    +------------------+------------------+------------------+
```

これは、192.168.42/24が192.168.42.0/24と同等になるRFC 4632のCIDRアドレス表記とは異なる点に注意してください。

IPv6は通常の形式で入力でき、ネットマスクの付加は任意です。IPv6のネットマスクにはビット数のみ指定できます。不確定なIPアドレスの名前解決による問題を避けるため、IPv6のパターンにホスト名を指定することは一切できません。

HAProxyは、次の状況ではIPv4アドレスとIPv6アドレスを照合することもできます。

- 検査対象のアドレスがIPv4、パターンのアドレスがIPv4の場合、IPv4で照合します。
  マスクが指定されていれば、それを使用します。
- 検査対象のアドレスがIPv6、パターンのアドレスがIPv6の場合、IPv6で照合します。
  マスクが指定されていれば、それを使用します。
- 検査対象のアドレスがIPv6、パターンのアドレスがIPv4の場合、IPv6アドレスが2002:IPV4::、::IPV4、
  ::ffff:IPV4のいずれかに一致すれば、パターンのマスクを使用してIPv4で照合します。それ以外の場合は失敗します。
- 検査対象のアドレスがIPv4、パターンのアドレスがIPv6の場合、まずIPv4アドレスの先頭に::ffff:を
  付けてIPv6に変換し、その後、指定されたIPv6マスクを使用してIPv6で照合します。

## 7.2. ACLによる条件の構成 {#section-7-2}

一部のアクションは、条件が成立した場合にのみ実行されます。条件は、ACLと演算子を組み合わせたものです。次の3つの演算子がサポートされています。

- AND（暗黙的）
- OR（"or"キーワードまたは"\|\|"演算子で明示的に指定）
- 感嘆符（"!"）による否定

条件は、次のような論理和の形式で構成します。

```text
[!]acl1 [!]acl2 ... [!]acln  { or [!]acl1 [!]acl2 ... [!]acln } ...
```

このような条件は通常、"if"または"unless"文の後に記述し、どのような場合にアクションを実行するかを示します。

たとえば、URL "\*"への"OPTIONS"以外のメソッドによるHTTPリクエスト、content-lengthのないPOSTリクエスト、content-lengthが0より大きいGETまたはHEADリクエスト、そしてGET/HEAD/POST/OPTIONSのいずれでもないすべてのリクエストをブロックする場合です。

```haproxy
acl missing_cl req.hdr_cnt(Content-length) eq 0
http-request deny if HTTP_URL_STAR !METH_OPTIONS || METH_POST missing_cl
http-request deny if METH_GET HTTP_CONTENT
http-request deny unless METH_GET or METH_POST or METH_OPTIONS
```

"www"サイトの静的コンテンツへのリクエストと、"img"、"video"、"download"、"ftp"の各ホストへのすべてのリクエストに対して、別のバックエンドを選択する場合は、次のようにします。

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
acl host_www    hdr_beg(host) -i www
acl host_static hdr_beg(host) -i img. video. download. ftp.
```

```haproxy
# now use backend "static" for all static-only hosts, and for static URLs
# of host "www". Use backend "www" for the rest.
use_backend static if host_static or host_www url_static
use_backend www    if host_www
```

"匿名ACL"を使用してルールを構成することもできます。これは、宣言せずにその場で構成する、名前のないACL式です。波括弧で囲み、それぞれの波括弧の前後に空白を入れる必要があります（波括弧を独立した単語として認識させる必要があるためです）。次に例を示します。

```text
次のルールは：

    acl missing_cl req.hdr_cnt(Content-length) eq 0
    http-request deny if METH_POST missing_cl

次のようにも記述できます：

    http-request deny if METH_POST { req.hdr_cnt(Content-length) eq 0 }
```

この書き方は、設定に誤りを残しやすくなるため、一般には推奨されません。ただし、たとえば送信元IPアドレスを1つだけ照合するような非常に単純なルールでは、任意の名前でACLを宣言するより、この方法のほうが適切な場合があります。次の例も、適切な使い方です。

```text
名前付きACLの場合：

     acl site_dead nbsrv(dynamic) lt 2
     acl site_dead nbsrv(static)  lt 2
     monitor fail  if site_dead

匿名ACLの場合：

     monitor fail if { nbsrv(dynamic) lt 2 } || { nbsrv(static) lt 2 }
```

"http-request deny"キーワードと"use_backend"キーワードの詳細は、[セクション4.2](/ja/haproxy/proxies/#section-4-2)を参照してください。

## 7.3. サンプルの取得 {#section-7-3}

従来、サンプル取得方法は、ACLを使用してパターンと照合するデータの取得にのみ使われていました。スティックテーブルの登場に伴い、新しい種類のサンプル取得方法が作られました。その多くは、対応するACLと同じ構文を使用します。これらのサンプル取得方法は、"fetch"とも呼ばれます。現在では、ACLとfetchは統合されています。すべてのACL取得方法をfetchとして使用できるようになり、ACLからも任意のサンプル取得方法を使用できます。

このセクションでは、使用できるすべてのサンプル取得方法と、その出力型を詳しく説明します。一部のサンプル取得方法には、既存の設定との互換性を保つための非推奨の別名があります。その場合は非推奨であることを明記しています。新しい構成では使用しないことを推奨します。

サンプルには型があります。型によって、照合できるパターン、適用できるコンバーター、別の型が必要な場合の変換方法が決まります。次の型を使用します。

- boolean: 条件だけを報告する取得メソッドが返す、真または偽の値です。この型のサンプルは"-m"オプションなしで照合します。整数はゼロ以外なら真とみなし、文字列はまず整数として解析します。

- integer: 符号付き64ビット整数です。範囲は-2^63から2^63-1（-9223372036854775808から9223372036854775807）です。文字列を整数に変換する場合、先頭の符号文字（'+'または'-'）を除き、数字でない最初の文字で変換を停止します。読み取った数字から値を作り、数字がなければゼロになります。ただし、空の文字列は変換に失敗します。表現可能な範囲を超える値は、表現可能な最小または最大の整数に制限します。

- IPv4アドレスとIPv6アドレス： 別々の型ですが、一方を受け入れる場所の多くは他方も受け入れ、単にアドレスを取ると説明しています。IPv4アドレスを整数に変換すると、アドレスの32ビット値になります。IPv6アドレスに変換すると、IPv4-mapped形式（"::ffff:a.b.c.d"）になります。逆方向の変換にはより多くの制限があります。IPv6アドレスには整数表現がなく、IPv4アドレスに変換できるのはIPv4-mapped、IPv4-compatible、6to4アドレスの場合だけです。

- string: 最初のNUL文字（0x00）で終わるバイト列です。NUL文字自体は文字列に含まれません。途中にNUL文字が必要な場合はbinary型を使用します。エンコーディングは推測しません。HAProxyはこれらのバイトを文字として解釈しようとはせず、そもそもテキストを表すか、どの文字セットか、どう表示するかは、文字列の使用方法だけで決まります。そのため、binaryサンプルを文字列へ変換すると、明示的な変換でも暗黙の変換でも、最初のNUL文字以降を通知せずに破棄します。

- binary: 長さが既知のバイトのブロックです。各バイトはNULを含む0から255までの任意の値を取れます。リクエストボディやバイナリプロトコルの内容など、生データを抽出する取得メソッドが返す型です。この型のサンプルはboolean、整数、アドレスに変換できません。"-m bin"でバイナリブロックとして照合するか（[セクション7.1.5](/ja/haproxy/acls-and-samples/#section-7-1-5)を参照）、"hex"コンバーターなどで先に表示可能な形式へ変換する必要があります。逆方向の変換には制限がありません。文字列は常に有効なバイナリブロックだからです。

- method: HTTPメソッドです。HAProxyが認識しているメソッドは識別子で表し、それ以外は元の文字列を保持します。

以下のコンバーターの表では、任意の入力型を受け入れるコンバーターを表すために"any"も使用します。

ACLの派生形がある場合は、それぞれの照合方法とともに示します。これらには、すべて明確なデフォルトのパターン照合方法があるため、ACLによるサンプルの照合方法を示す"-m"オプションを指定する必要はありません（指定することはできます）。

前述のサンプルの型と照合方法の互換性の表に示したように、ACLで汎用のサンプル取得方法を使用する場合、サンプルの型が真偽値、整数、IPv4、IPv6のいずれかでない限り、"-m"オプションが必須です。同じキーワードがACLキーワードと標準の取得方法の両方に存在する場合、ACLエンジンはデフォルトでACL専用のものを自動的に選択します。

これらのキーワードの中には、必須引数と省略可能な引数を、それぞれ単数または複数受け取るものがあります。引数は厳密に型が定められており、設定解析時に検査されるため、不正な引数（名前を解決できないバックエンドなど）で動作する心配はありません。取得関数の引数は丸括弧内に記述し、コンマで区切ります。省略可能な引数は、以下では角括弧（'[ ]'）で囲んで示します。すべての引数が省略可能である場合は、丸括弧も省略できます。

したがって、標準のサンプル取得方法の構文は、次のいずれかになります。

- name
- name(arg1)
- name(arg1,arg2)

### 7.3.1. コンバーター {#section-7-3-1}

サンプル取得方法には、取得したサンプルに適用する変換（"コンバーター"とも呼びます）を組み合わせられます。この組み合わせを"サンプル式"と呼び、その結果が"サンプル"です。当初は"stick on"と"stick store-request"ディレクティブだけが対応していましたが、現在ではサンプルを使用できるすべての場所（ACL、log-format、unique-id-format、add-headerなど）に拡張されています。

これらの変換は、サンプル取得方法の後に、一連の専用キーワードとして列挙します。取得キーワードの引数の直後に、コンマで区切って追加することもできます。これらのキーワードも、ネットマスクなどの引数を受け取る場合があり、その引数は丸括弧内に記述する必要があります。

コンバーターの中には、整数に対する基本的な演算に対応する、ビット演算子や算術演算子があります。ビット演算としてand、or、xor、cplが、算術演算としてadd、sub、mul、div、mod、negがサポートされています。また、odd、even、not、boolという判定用の演算子もあり、ACLを記述せずに一致を返すことができます。

次のキーワードがサポートされています。

```text
   キーワード                                      入力型       出力型
------------------------------------------------+-------------+----------------
51d.single(prop[,prop*])                           string       string
add(value)                                         integer      integer
add_item(delim[,var[,suff]])                       string       string
aes_cbc_dec(bits,nonce,key[,<aad>])                binary       binary
aes_cbc_enc(bits,nonce,key[,<aad>])                binary       binary
aes_gcm_dec(bits,nonce,key,aead_tag[,aad])         binary       binary
aes_gcm_enc(bits,nonce,key,aead_tag[,aad])         binary       binary
and(value)                                         integer      integer
b64dec                                             string       binary
base2                                              binary       string
base64                                             binary       string
be2dec(separator,chunk_size[,truncate])            binary       string
le2dec(separator,chunk_size[,truncate])            binary       string
be2hex([separator[,chunk_size[,truncate]]])        binary       string
bool                                               integer      boolean
bytes(offset[,length])                             binary       binary
capture-req(id)                                    string       string
capture-res(id)                                    string       string
concat([start[,var[,end]]])                        string       string
cpl                                                integer      integer
crc32([avalanche])                                 binary       integer
crc32c([avalanche])                                binary       integer
cut_crlf                                           string       string
da-csv-conv(prop[,prop*])                          string       string
date                                               string       integer
debug([prefix][,destination])                       any          same
-- キーワード ----------------------------------+- 入力型     + 出力型      -
digest(algorithm)                                  binary       binary
div(value)                                         integer      integer
djb2([avalanche])                                  binary       integer
eth.data                                           binary       binary
eth.dst                                            binary       binary
eth.hdr                                            binary       binary
eth.proto                                          binary       integer
eth.src                                            binary       binary
eth.vlan                                           binary       integer
even                                               integer      boolean
fe_exists                                          string       boolean
field(index,delimiters[,count])                    string       string
fix_is_valid                                       binary       boolean
fix_tag_value(tag)                                 binary       binary
has_ctl([mask])                                    binary       boolean
hex                                                binary       string
hex2i                                              binary       integer
hmac(algorithm,key)                                binary       binary
host_only                                          string       string
htonl                                              integer      integer
http_date([offset[,unit]])                         integer      string
iif(true,false)                                    boolean      string
in_table([table])                                  any          boolean
ip.data                                            binary       binary
ip.df                                              binary       integer
ip.dst                                             binary       address
ip.fp                                              binary       binary
ip.hdr                                             binary       binary
ip.proto                                           binary       integer
ip.src                                             binary       address
ip.tos                                             binary       integer
ip.ttl                                             binary       integer
ip.ver                                             binary       integer
ipmask(mask4[,mask6])                              address      address
json([input-code])                                 string       string
json_query(json_path[,output_type])                string       _outtype_
jwt_decrypt_jwk(<jwk>)                             string       binary
jwt_decrypt_cert(<cert>)                           string       binary
jwt_decrypt_secret(<secret>)                       string       binary
jwt_header_query([json_path[,output_type]])        string       string
jwt_payload_query([json_path[,output_type]])       string       string
-- キーワード ----------------------------------+- 入力型     + 出力型      -
jwt_verify(alg,key)                                string       integer
jwt_verify_cert(alg,cert)                          string       integer
language(value[,default])                          string       string
length                                             string       integer
lower                                              string       string
ltime(format[,offset])                             integer      string
ltrim(chars)                                       string       string
map(map_name[,default_value])                      string       string
map_match(map_name[,default_value])                _match_      string
map_match_output(map_name[,default_value])         _match_      _output_
mod(value)                                         integer      integer
mqtt_field_value(pkt_type,fieldname_or_prop_ID)    binary       binary
mqtt_is_valid                                      binary       boolean
ms_ltime(format[,offset])                          integer      string
ms_utime(format[,offset])                          integer      string
mul(value)                                         integer      integer
nbsrv                                              string       integer
neg                                                integer      integer
not                                                integer      boolean
odd                                                integer      boolean
or(value)                                          integer      integer
-- キーワード ----------------------------------+- 入力型     + 出力型      -
param(name[,delim])                                string       string
port_only                                          string       integer
protobuf(field_number[,field_type])                binary       binary
regsub(regex,subst[,flags])                        string       string
reverse                                            string       string
reverse_dom                                        string       string
rfc7239_field(field)                               string       string
rfc7239_is_valid                                   string       boolean
rfc7239_n2nn                                       string       address / str
rfc7239_n2np                                       string       integer / str
rfc7239_nn                                         address/str  string
rfc7239_np                                         integer/str  string
rtrim(chars)                                       string       string
sdbm([avalanche])                                  binary       integer
secure_memcmp(var)                                 string       boolean
set-var(var[,cond...])                              any          same
sha1                                               binary       binary
sha2([bits])                                       binary       binary
srv_is_up                                          string       boolean
srv_queue                                          string       integer
strcmp(var)                                        string       boolean
sub(value)                                         integer      integer
table_bytes_in_rate([table])                       any          integer
table_bytes_out_rate([table])                      any          integer
table_clr_gpc(idx[,table])                         any          integer
table_clr_gpc0([table])                            any          integer
table_clr_gpc1([table])                            any          integer
table_conn_cnt([table])                            any          integer
-- キーワード ----------------------------------+- 入力型     + 出力型      -
table_conn_cur([table])                            any          integer
table_conn_rate([table])                           any          integer
table_expire([table[,default_value]])              any          integer
table_glitch_cnt([table])                          any          integer
table_glitch_rate([table])                         any          integer
table_gpc(idx[,table])                             any          integer
table_gpc0([table])                                any          integer
table_gpc0_rate([table])                           any          integer
table_gpc1([table])                                any          integer
table_gpc1_rate([table])                           any          integer
table_gpc_rate(idx[,table])                        any          integer
table_gpt(idx[,table])                             any          integer
table_gpt0([table])                                any          integer
table_http_err_cnt([table])                        any          integer
table_http_err_rate([table])                       any          integer
table_http_fail_cnt([table])                       any          integer
table_http_fail_rate([table])                      any          integer
table_http_req_cnt([table])                        any          integer
table_http_req_rate([table])                       any          integer
table_idle([table[,default_value]])                any          integer
table_inc_gpc(idx[,table])                         any          integer
table_inc_gpc0([table])                            any          integer
table_inc_gpc1([table])                            any          integer
table_kbytes_in([table])                           any          integer
-- キーワード ----------------------------------+- 入力型     + 出力型      -
table_kbytes_out([table])                          any          integer
table_server_id([table])                           any          integer
table_sess_cnt([table])                            any          integer
table_sess_rate([table])                           any          integer
table_trackers([table])                            any          integer
tcp.dst                                            binary       integer
tcp.flags                                          binary       integer
tcp.options.mss                                    binary       integer
tcp.options.sack                                   binary       integer
tcp.options.tsopt                                  binary       integer
tcp.options.tsval                                  binary       integer
tcp.options.wscale                                 binary       integer
tcp.options.wsopt                                  binary       integer
tcp.options_list                                   binary       binary
tcp.seq                                            binary       integer
tcp.src                                            binary       integer
tcp.win                                            binary       integer
ub64dec                                            string       string
ub64enc                                            string       string
ungrpc(field_number[,field_type])                  binary       binary / int
unset-var(var)                                      any          same
upper                                              string       string
url_dec([in_form])                                 string       string
url_enc([enc_type])                                string       string
us_ltime(format[,offset])                          integer      string
us_utime(format[,offset])                          integer      string
utime(format[,offset])                             integer      string
when(condition)                                     any          same
word(index,delimiters[,count])                     string       string
wt6([avalanche])                                   binary       integer
x509_v_err_str                                     integer      string
xor(value)                                         integer      integer
-- キーワード ----------------------------------+- 入力型     + 出力型      -
xxh3([seed])                                       binary       integer
xxh32([seed])                                      binary       integer
xxh64([seed])                                      binary       integer
```

以下にコンバーターのキーワードを詳しく説明します。

<a id="entry-7-3-1-51d-single"></a>

**`51d.single(<prop>[,<prop>*])`**

```haproxy
51d.single(<prop>[,<prop>*])
```

要求したプロパティの値を文字列として返します。各値は、"51degrees-property-separator"で指定した区切り文字で区切られます。デバイスは、コンバーターに渡されたUser-Agentヘッダーを使用して識別します。この関数には最大五つのプロパティ名を渡せます。プロパティ名が見つからない場合は、値"NoData"を返します。

例：

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request,
# containing values for the three properties requested by using the
# User-Agent passed to the converter.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[req.fhdr(User-Agent),51d.single(DeviceType,IsMobile,IsTablet)]
```

<a id="entry-7-3-1-add"></a>

**`add(<value>)`**

```haproxy
add(<value>)
```

符号付き整数型の入力値に`<value>`を加算し、結果を符号付き整数として返します。`<value>`には、数値または変数名を指定できます。変数の詳細は、[セクション2.8](/ja/haproxy/configuration-basics/#section-2-8)を参照してください。

<a id="entry-7-3-1-add-item"></a>

**`add_item(<delim>[,<var>[,<suff>]])`**

```haproxy
add_item(<delim>[,<var>[,<suff>]])
```

現在のサンプルの後に最少2個、最大3個のフィールドを連結し、サンプルを文字列に変換します。最初のフィールド`<delim>`は定数文字列で、既存のサンプルが空ではなく、かつ`<var>`か`<suff>`のいずれかが空ではない場合に、既存のサンプルの直後に追加します。次のフィールド`<var>`は変数名です。その変数を検索し、内容を文字列に変換して、`<delim>`の直後に追加します。変数が見つからない場合は、何も追加しません。これは省略可能で、その後に任意で定数文字列`<suff>`を指定することもできます。ただし、`<var>`を省略した場合、`<suff>`は必須です。このコンバーターはconcatコンバーターに似ており、他の変数を連結して新しい変数を作成できます。主な違いは、区切り文字を追加する意味があるかを確認する点です。たとえば、現在のサンプルが空の場合には、区切り文字の追加は適切ではありません。同じ処理をconcatコンバーターで行うには、2つのルールに分け、最初のルールで現在のサンプル文字列が空かを確認してから区切り文字を追加する必要があります。コンマや閉じ丸括弧を区切り文字に使用する場合、引用符やバックスラッシュで保護し、さらに、その引用符やバックスラッシュが最初の段階のパーサーで除去されないように保護する必要があります（引用とエスケープについては[セクション2.2](/ja/haproxy/configuration-basics/#section-2-2)を参照してください）。以下の例を参照してください。

例：

```text
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1,"(site1)") if src,in_table(site1)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score2,"(site2)") if src,in_table(site2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score3,"(site3)") if src,in_table(site3)'
http-request set-header x-tagged %[var(req.tagged)]

http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1),add_item(",",req.score2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",,(site1))' if src,in_table(site1)
```

<a id="entry-7-3-1-aes-cbc-dec"></a>

**`aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])
```

`<bits>`パラメーターに応じて、AES128-CBC、AES192-CBC、AES256-CBCのいずれかのアルゴリズムで、生のバイト列の入力を復号します。他のパラメーターはすべてbase64でエンコードする必要があり、結果は生のバイト列で返されます。`<aad>`パラメーターは省略可能です。`<aad>`の検証が失敗した場合、コンバーターはデータを返しません。`<nonce>`、`<key>`、`<aad>`には、文字列または変数を指定できます。このコンバーターにはOpenSSL 1.0.1以降が必要です。

例：

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_cbc_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-cbc-enc"></a>

**`aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])
```

`<bits>`パラメーターに応じて、AES128-CBC、AES192-CBC、AES256-CBCのいずれかのアルゴリズムで、生のバイト列の入力を暗号化します。`<nonce>`、`<key>`、`<aad>`パラメーターは、base64でエンコードする必要があります。`<aad>`パラメーターは省略可能です。結果は生のバイト列で返されます。`<nonce>`、`<key>`、`<aad>`には、文字列または変数を指定できます。このコンバーターにはOpenSSL 1.0.1以降が必要です。

例：

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_cbc_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-gcm-dec"></a>

**`aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

`<bits>`パラメーターに応じて、AES128-GCM、AES192-GCM、AES256-GCMのいずれかのアルゴリズムで、生のバイト列の入力を復号します。他のパラメーターはすべてbase64でエンコードする必要があり、結果は生のバイト列で返されます。`<aead_tag>`または`<aad>`の検証が失敗した場合、コンバーターはデータを返しません。`<aad>`パラメーターは省略可能です。`<nonce>`、`<key>`、`<aead_tag>`、`<aad>`には、文字列または変数を指定できます。このコンバーターにはOpenSSL 1.0.1以降が必要です。

例：

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_gcm_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-aes-gcm-enc"></a>

**`aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

`<bits>`パラメーターに応じて、AES128-GCM、AES192-GCM、AES256-GCMのいずれかのアルゴリズムで、生のバイト列の入力を暗号化します。`<nonce>`、`<key>`、`<aad>`パラメーターは、base64でエンコードする必要があります。`<aead_tag>`パラメーターには変数を指定する必要があります。AEADタグは、base64でエンコードされてその変数に格納されます。`<aad>`パラメーターは省略可能です。結果は生のバイト列で返されます。`<nonce>`、`<key>`、`<aad>`には、文字列または変数を指定できます。このコンバーターにはOpenSSL 1.0.1以降が必要です。

例：

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_gcm_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-and"></a>

**`and(<value>)`**

```haproxy
and(<value>)
```

`<value>`と符号付き整数型の入力値とのビット単位の"AND"を計算し、結果を符号付き整数として返します。`<value>`には、数値または変数名を指定できます。変数の詳細は、[セクション2.8](/ja/haproxy/configuration-basics/#section-2-8)を参照してください。

<a id="entry-7-3-1-b64dec"></a>

**`b64dec`**

```haproxy
b64dec
```

base64でエンコードされた入力文字列を、バイナリー表現に変換（デコード）します。base64()の逆の操作を行います。base64url（RFC 4648の"URLおよびファイル名に安全な文字集合"）の派生形式については、"ub64dec"を参照してください。

<a id="entry-7-3-1-base2"></a>

**`base2`**

```haproxy
base2
```

バイナリーの入力サンプルを、入力の1バイトにつき8桁の二進数字を含む二進文字列に変換します。ネイティブな表現では接頭辞の照合ができない型（IPプレフィックスなど）に対して、最長接頭辞一致を行えるようにするために使用します。

<a id="entry-7-3-1-base64"></a>

**`base64`**

```haproxy
base64
```

バイナリーの入力サンプルをbase64文字列に変換します。バイナリーの内容を、確実に転送できる形式でログに記録したり、転送したりするために使用します（たとえば、SSL IDをヘッダーにコピーできます）。base64url（RFC 4648の"URLおよびファイル名に安全な文字集合"）の派生形式については、"ub64enc"を参照してください。

<a id="entry-7-3-1-be2dec"></a>

**`be2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
be2dec(<separator>,<chunk_size>[,<truncate>])
```

ビッグエンディアンのバイナリー入力サンプルを、入力の`<chunk_size>`バイトごとに符号なし整数を含む文字列に変換します。`<separator>`を指定した場合、バイナリー入力の`<chunk_size>`バイトごとに挿入します。`<truncate>`フラグは、バイナリー入力を`<chunk_size>`の境界で切り詰めるかどうかを示します。`<chunk_size>`の最大値は、long long intのサイズ（8バイト）に制限されます。

例：

```text
bin(01020304050607),be2dec(:,2)   # 258:772:1286:7
bin(01020304050607),be2dec(-,2,1) # 258-772-1286
bin(01020304050607),be2dec(,2,1)  # 2587721286
bin(7f000001),be2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-le2dec"></a>

**`le2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
le2dec(<separator>,<chunk_size>[,<truncate>])
```

リトルエンディアンのバイナリー入力サンプルを、入力の`<chunk_size>`バイトごとに符号なし整数を含む文字列に変換します。`<separator>`を指定した場合、バイナリー入力の`<chunk_size>`バイトごとに挿入します。`<truncate>`フラグは、バイナリー入力を`<chunk_size>`の境界で切り詰めるかどうかを示します。`<chunk_size>`の最大値は、long long intのサイズ（8バイト）に制限されます。

例：

```text
bin(01020304050607),le2dec(:,2)   # 513:1284:2055:7
bin(01020304050607),le2dec(-,2,1) # 513-1284-2055
bin(01020304050607),le2dec(,2,1)  # 51312842055
bin(7f000001),le2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-be2hex"></a>

**`be2hex([<separator>[,<chunk_size>[,<truncate>]]])`**

```haproxy
be2hex([<separator>[,<chunk_size>[,<truncate>]]])
```

ビッグエンディアンのバイナリー入力サンプルを、入力の1バイトにつき2桁の16進数字を含む16進文字列に変換します。バイナリーの入力データの16進ダンプを、確実に転送できる形式でログに記録したり、転送したりするために使用します（たとえば、SSL IDをヘッダーにコピーできます）。`<separator>`を指定した場合、バイナリー入力の`<chunk_size>`バイトごとに挿入します。`<truncate>`フラグは、バイナリー入力を`<chunk_size>`の境界で切り詰めるかどうかを示します。

例：

```text
bin(01020304050607),be2hex         # 01020304050607
bin(01020304050607),be2hex(:,2)    # 0102:0304:0506:07
bin(01020304050607),be2hex(--,2,1) # 0102--0304--0506
bin(0102030405060708),be2hex(,3,1) # 010203040506
```

<a id="entry-7-3-1-bool"></a>

**`bool`**

```haproxy
bool
```

符号付き整数型の入力値が非ゼロであれば真偽値TRUEを返し、それ以外はFALSEを返します。and()と組み合わせると、入力値に対するビット検査（フラグの有無の確認など）の結果をtrue/falseで返すことができます。

<a id="entry-7-3-1-bytes"></a>

**`bytes(<offset>[,<length>])`**

```haproxy
bytes(<offset>[,<length>])
```

バイナリーの入力サンプルからバイト列を抽出します。結果は、元のサンプルのオフセット（バイト単位）から始まるバイナリーサンプルで、任意で指定した長さに切り詰められます。`<offset>`と`<length>`には、数値または変数名を指定できます。`<offset>`または`<length>`のいずれかが無効な場合、このコンバーターは空のサンプルを返します。無効な`<offset>`とは、負の値または入力サンプルの長さ以上（\>=）の値です。無効な`<length>`とは、負の値です。

例：

```text
http-request set-var(txn.input) req.hdr(input) # let's say input is "012345"

http-response set-header bytes_0 "%[var(txn.input),bytes(0)]"  # outputs "012345"
http-response set-header bytes_1_3 "%[var(txn.input),bytes(1,3)]"  # outputs "123"

http-response set-var(txn.var_start) int(1)
http-response set-var(txn.var_length) int(3)
http-response set-header bytes_var1_var3    "%[var(txn.input),bytes(txn.var_start,txn.var_length)]"  # outputs "123"
```

<a id="entry-7-3-1-capture-req"></a>

**`capture-req(<id>)`**

```haproxy
capture-req(<id>)
```

文字列エントリーをリクエストのスロット`<id>`にキャプチャーし、そのエントリーをそのまま返します。スロットが存在しない場合、キャプチャーはエラーを報告せずに失敗します。

関連項目："declare capture"、"http-request capture"、"http-response capture"、"capture.req.hdr"、"capture.res.hdr"（サンプル取得）。

<a id="entry-7-3-1-capture-res"></a>

**`capture-res(<id>)`**

```haproxy
capture-res(<id>)
```

文字列エントリーをレスポンスのスロット`<id>`にキャプチャーし、そのエントリーをそのまま返します。スロットが存在しない場合、キャプチャーはエラーを報告せずに失敗します。

関連項目："declare capture"、"http-request capture"、"http-response capture"、"capture.req.hdr"、"capture.res.hdr"（サンプル取得）。

<a id="entry-7-3-1-concat"></a>

**`concat([<start>[,<var>[,<end>]]])`**

```haproxy
concat([<start>[,<var>[,<end>]]])
```

現在のサンプルの後に最大3個のフィールドを連結し、サンプルを文字列に変換します。最初のフィールド`<start>`は定数文字列で、既存のサンプルの直後に追加します。使用しない場合は省略できます。次のフィールド`<var>`は変数名です。その変数を検索し、内容を文字列に変換して、`<first>`部分の直後に追加します。変数が見つからない場合は、何も追加しません。このフィールドも省略できます。最後のフィールド`<end>`は定数文字列で、変数の後に追加します。これも省略できます。これらの要素を組み合わせることで、既存の変数群に対して、区切り文字を挟んで変数を連結できます。たとえばコロン区切りの値のように、他の変数を連結して新しい変数を作成するために使用できます。コンマや閉じ丸括弧を区切り文字に使用する場合、引用符やバックスラッシュで保護し、さらに、その引用符やバックスラッシュが最初の段階のパーサーで除去されないように保護する必要があります。他の変数から複合変数を作成する用途でよく使用されますが、複数のフィールドを含む書式文字列を使用するほうが便利な場合もあります。以下の例を参照してください。

例：

```text
tcp-request session set-var(sess.src) src
tcp-request session set-var(sess.dn)  ssl_c_s_dn
tcp-request session set-var(txn.sig) str(),concat(<ip=,sess.ip,>),concat(<dn=,sess.dn,>)
tcp-request session set-var(txn.ipport) "str(),concat('addr=(',sess.ip),concat(',',sess.port,')')"
tcp-request session set-var-fmt(txn.ipport) "addr=(%[sess.ip],%[sess.port])"  ## does the same
http-request set-header x-hap-sig %[var(txn.sig)]
```

<a id="entry-7-3-1-cpl"></a>

**`cpl`**

```haproxy
cpl
```

符号付き整数型の入力値を受け取り、1の補数（すべてのビットを反転）を求め、結果を符号付き整数として返します。

<a id="entry-7-3-1-crc32"></a>

**`crc32([<avalanche>])`**

```haproxy
crc32([<avalanche>])
```

CRC32 ハッシュ関数を使用してバイナリ入力サンプルを符号なし 32 ビット量にハッシュします。オプションで、`<avalanche>` 引数が 1 に等しい場合、出力に完全なアバランチハッシュ関数を適用できます。このコンバーターは、さまざまなハッシュベースの負荷分散アルゴリズムで使用される関数と同一であるため、正確に同じ結果を提供します。他のソフトウェアが入力キーに対して CRC32 を計算したい場合の互換性のために提供されています。Ethernet、Gzip、PNG などに見られる一般的な実装に従います。他のアルゴリズムより遅いですが、より良い、あるいは少なくとも予測しにくい分布を提供する可能性があります。32 ビットハッシュは簡単に破られるため、セキュリティ目的には使用してはなりません。また "djb2"、"sdbm"、"wt6"、"crc32c" および "hash-type" ディレクティブを参照してください。

<a id="entry-7-3-1-crc32c"></a>

**`crc32c([<avalanche>])`**

```haproxy
crc32c([<avalanche>])
```

CRC32C ハッシュ関数を使用してバイナリ入力サンプルを符号なし 32 ビット量にハッシュします。オプションで、`<avalanche>` 引数が 1 に等しい場合、出力に完全なアバランチハッシュ関数を適用できます。このコンバーターは RFC4960 の付録 B [8] に記載されているものと同じ関数を使用します。他のソフトウェアが入力キーに対して CRC32C を計算したい場合の互換性のために提供されています。他のアルゴリズムより遅く、32 ビットハッシュは簡単に破られるため、セキュリティ目的には使用してはなりません。また "djb2"、"sdbm"、"wt6"、"crc32" および "hash-type" ディレクティブを参照してください。

<a id="entry-7-3-1-cut-crlf"></a>

**`cut_crlf`**

```haproxy
cut_crlf
```

入力サンプルの文字列表現を最初に見つかった復帰文字 ('&#92;r') または改行文字 ('&#92;n') で切り分けます。文字列長のみが更新されます。

<a id="entry-7-3-1-da-csv-conv"></a>

**`da-csv-conv(<prop>[,<prop>*])`**

```haproxy
da-csv-conv(<prop>[,<prop>*])
```

DeviceAtlas コンバーターに、入力で渡された User Agent 文字列を識別させ、引数で列挙されたプロパティを連結して出力するように指示します。区切り文字はグローバルキーワード "deviceatlas-property-separator" で定義されたもの、またはデフォルトではパイプ文字 ('\|') です。HAProxy 設定言語によって 12 種類の異なるプロパティに制限されています。

例：

```text
frontend www
  bind *:8881
  default_backend servers
  http-request set-header X-DeviceAtlas-Data %[req.fhdr(User-Agent),da-csv(primaryHardwareType,osName,osVersion,browserName,browserVersion,browserRenderingEngine)]
```

<a id="entry-7-3-1-date"></a>

**`date`**

```haproxy
date
```

このコンバーターは HTTP ヘッダーからの日付を変換するために使用します。これは IMF 日付、ASCTIME 日付、または RFC850 日付のいずれかです。出力は UNIX タイムスタンプになります。

例：

```text
http-request return lf-string "%[str('Sun, 06 Nov 1994 08:49:37 GMT'),date]\n" content-type text/plain
```

<a id="entry-7-3-1-debug"></a>

**`debug([<prefix][,<destination>])`**

```haproxy
debug([<prefix][,<destination>])
```

このコンバーターはデバッグツールとして使用されます。入力サンプルのキャプチャを取得し、イベントシンク `<destination>` に送信します。シンクは "buf0" のようなリングバッファ、"stdout"、または "stderr" を指定できます。利用可能なシンクは CLI で "show events" を実行することで実行時に確認できます。指定がなければ出力は "buf0" になります。CLI の "show events" コマンドで参照できます。複数の式からの出力を区別しやすくするため、任意のプレフィックス `<prefix>` を渡すことができます。出力メッセージのコロンの前に表示されます。入力サンプルはそのまま出力されるため、印字できないサンプル型でも、チェーン内のどこにでもデバッグコンバーターを挿入しても安全です。

例：

```text
tcp-request connection track-sc0 src,debug(track-sc)
```

<a id="entry-7-3-1-digest"></a>

**`digest(<algorithm>)`**

```haproxy
digest(<algorithm>)
```

バイナリ入力サンプルをメッセージダイジェストに変換します。結果はバイナリサンプルになります。`<algorithm>` は OpenSSL メッセージダイジェスト名（例：sha256）でなければなりません。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

<a id="entry-7-3-1-div"></a>

**`div(<value>)`**

```haproxy
div(<value>)
```

入力値を符号付き整数型として `<value>` で割り、結果を符号付き整数として返します。`<value>` がゼロの場合、最大の符号なし整数が返されます（通常は 2^63-1）。`<value>` は数値または変数名で指定できます。詳細については [2.8節](/ja/haproxy/configuration-basics/#section-2-8) の変数に関する説明を参照してください。

<a id="entry-7-3-1-djb2"></a>

**`djb2([<avalanche>])`**

```haproxy
djb2([<avalanche>])
```

DJB2 ハッシュ関数を使用してバイナリ入力サンプルを符号なし 32 ビット量にハッシュします。オプションで、`<avalanche>` 引数が 1 に等しい場合、出力に完全なアバランチハッシュ関数を適用できます。このコンバーターは、さまざまなハッシュベースの負荷分散アルゴリズムで使用される関数と同一であるため、正確に同じ結果を提供します。主にデバッグ用ですが、粗い統計を集めるためのスティックテーブルエントリとしても使用できます。32 ビットハッシュは簡単に破られるため、セキュリティ目的には使用してはなりません。また "crc32"、"sdbm"、"wt6"、"crc32c" および "hash-type" ディレクティブを参照してください。

<a id="entry-7-3-1-eth-data"></a>

**`eth.data`**

```haproxy
eth.data
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。VLAN を含むすべてのイーサネットヘッダーをスキップし、レイヤ3プロトコル（通常は IPv4 または IPv6）から始まるバイナリデータブロックを返します。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-eth-dst"></a>

**`eth.dst`**

```haproxy
eth.dst
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。フレームの宛先アドレスに対応する 6 バイトのイーサネットヘッダーをバイナリブロックとして返します。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-eth-hdr"></a>

**`eth.hdr`**

```haproxy
eth.hdr
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。イーサネットヘッダーより後の部分をすべて切り落としますが、VLAN があればそれを保持し、ヘッダーをバイナリデータブロックとして返します。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-eth-proto"></a>

**`eth.proto`**

```haproxy
eth.proto
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。イーサネットヘッダー内で、省略可能な VLAN の後にあるプロトコル番号（EtherType とも呼ばれる）を整数値として返します。通常は IPv4 に対して 0x800、IPv6 に対して 0x86DD になります。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-eth-src"></a>

**`eth.src`**

```haproxy
eth.src
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。フレームの送信元アドレスに対応する 6 バイトのイーサネットヘッダーをバイナリブロックとして返します。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-eth-vlan"></a>

**`eth.vlan`**

```haproxy
eth.vlan
```

"tcp-ss" バインドオプションを "2" に設定し、"fc_saved_syn" で取得することで返されるバイナリイーサネットフレームを表す入力サンプルと併用します。イーサネットヘッダーに見つかった最後の VLAN ID を整数値として返します。また "fc_saved_syn" および "tcp-ss" を参照してください。

<a id="entry-7-3-1-even"></a>

**`even`**

```haproxy
even
```

入力値が符号付き整数型で偶数の場合に真（TRUE）を返し、それ以外の場合は偽（FALSE）を返します。"not,and(1),bool" と機能的に同等です。

<a id="entry-7-3-1-field"></a>

**`field(<index>,<delimiters>[,<count>])`**

```haproxy
field(<index>,<delimiters>[,<count>])
```

指定されたインデックス（正のインデックスは先頭から、負のインデックスは末尾から）で、指定された区切り文字を考慮して入力文字列から部分文字列を抽出します。インデックスは 1 または -1 から始まります。区切り文字は、文字のリストを文字列にしたものです。オプションで抽出するフィールド数 `<count>` を指定できます（デフォルト：1）。0 は残りのすべてのフィールドを抽出することを示します。

例：

```text
str(f1_f2_f3__f5),field(4,_)    # <empty>
str(f1_f2_f3__f5),field(5,_)    # f5
str(f1_f2_f3__f5),field(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),field(2,_,2)  # f2_f3
str(f1_f2_f3__f5),field(-2,_,3) # f2_f3_
str(f1_f2_f3__f5),field(-3,_,0) # f1_f2_f3
```

<a id="entry-7-3-1-fe-exists"></a>

**`fe_exists`**

```haproxy
fe_exists
```

入力値としてフロントエンド名を指定し、その名前のフロントエンドが現在の構成に存在する場合に真（TRUE）を返し、それ以外の場合は偽（FALSE）を返します。動的な名前からフロントエンドの存在を確認する必要がある場所（例：マップ照合や外部チェックへの応答）で使用できます。

例：

```text
http-request deny unless { var(txn.fe_name),fe_exists }
```

<a id="entry-7-3-1-fix-is-valid"></a>

**`fix_is_valid`**

```haproxy
fix_is_valid
```

バイナリペイロードを解析し、FIX（Financial Information eXchange）に関する整合性チェックを行います：

- すべてのタグ ID と値が空でなく、タグ ID が適切な数値であることを確認します
- BeginString タグが最初のタグであり、有効な FIX バージョンを示していることを確認します
- BodyLength タグが2番目のタグであり、正しい本文長を示していることを確認します
- MsgType タグが3番目のタグであることを確認します。
- メッセージの最後のタグが CheckSum タグであり、有効なチェックサムであることを確認します。

現在の HAProxy の設計上、クライアントおよびサーバーが送信する最初のメッセージのみが解析可能です。

このコンバーターは真偽値を返し、ペイロードに有効な FIX メッセージが含まれていれば true、それ以外は false になります。

また、fix_tag_value コンバーターも参照してください。

例：

```text
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
```

<a id="entry-7-3-1-fix-tag-value"></a>

**`fix_tag_value(<tag>)`**

```haproxy
fix_tag_value(<tag>)
```

FIX (Financial Information eXchange) メッセージを解析し、タグ `<tag>` から値を抽出します。`<tag>` は目的のタグを指す文字列または整数です。整数値はすべて許容されますが、以下の文字列のみが整数に変換されます：BeginString、BodyLength、MsgType、SenderCompID、TargetCompID、CheckSum。より多くのタグ名を簡単に追加できます。

現在の HAProxy の設計上、クライアントおよびサーバーが送信する最初のメッセージのみが解析可能です。このコンバーターはメッセージの検証を行いません。まず fix_is_valid コンバーターを使用してメッセージを検証しておくことを強く推奨します。

また、fix_is_valid コンバーターも参照してください。

例：

```shell
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
# MsgType tag ID is 35, so both lines below will return the same content
tcp-request content set-var(txn.foo) req.payload(0,0),fix_tag_value(35)
tcp-request content set-var(txn.bar) req.payload(0,0),fix_tag_value(MsgType)
```

<a id="entry-7-3-1-has-ctl"></a>

**`has_ctl([mask])`**

```haproxy
has_ctl([mask])
```

入力バイナリーサンプルに、マスク引数で定義された制御文字が含まれているかを検査します。マスクは33ビットの数値（10進数、または "0x" で始まる16進数）で、0x00から0x1Fまでの範囲で検出する各文字に対応するビットを立てます。DEL文字 (0x7F) に一致させるには、ビット32を立てます。マスクを指定しない場合、コンバーターは値0x1FFFFFDFFを使用し、HTTPヘッダーでよく使われるTAB (0x09) を除くすべての制御文字に一致します。特別なマスク "any" は0x1FFFFFFFFに対応し、TABを含むすべての制御文字に一致します。特別なマスク "http" は0x2401に対応し、HTTPヘッダー値で禁止されている制御文字であるCR (0x0D)、LF (0x0A)、NUL (0x00) だけに一致します。

例：

```shell
# reject presence of DEL, CR, LF, NUL characters in the referer header
http-request deny if { req.fhdr(referer),has_ctl(0x100002401) }
# reject presence of any control char but tab in any HTTP header value
http-request deny if { req.hdr(),has_ctl }
```

<a id="entry-7-3-1-hex"></a>

**`hex`**

```haproxy
hex
```

バイナリー入力サンプルを、入力バイトごとに2桁の16進数を含む16進文字列に変換します。バイナリー入力データの16進ダンプを、確実に転送できる形式でログに記録したり転送したりするために使用します（たとえば、SSL IDをヘッダーにコピーできます）。

<a id="entry-7-3-1-hex2i"></a>

**`hex2i`**

```haproxy
hex2i
```

入力バイトごとに2桁の16進数を含む16進文字列を、整数に変換します。入力値に16進数の数字以外の文字が含まれる場合、コンバーターは失敗して何も返しません。これにより、不正な入力と有効なゼロ値を区別できます。

<a id="entry-7-3-1-hmac"></a>

**`hmac(<algorithm>,<key>)`**

```haproxy
hmac(<algorithm>,<key>)
```

入力バイナリサンプルを、指定されたキーを使用したメッセージ認証コードに変換します。結果はバイナリサンプルです。`<algorithm>` は登録済みの OpenSSL メッセージダイジェスト名のいずれかでなければなりません（例：sha256）。`<key>` パラメーターは base64 エンコードされていなければならず、文字列または変数のいずれかを指定できます。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

<a id="entry-7-3-1-host-only"></a>

**`host_only`**

```haproxy
host_only
```

Host ヘッダー値を含む文字列を変換し、ポートを削除します。入力は Host ヘッダー値の形式（rfc9110#section-7.2）に従う必要があります。以下の形式の入力をサポートします：hostname、hostname:80、127.0.0.1、127.0.0.1:80、[::1]、[::1]:80。

このコンバーターは、文字列を小文字に変換します。

また、"port_only" コンバーターも参照してください。これはポートを返します。

<a id="entry-7-3-1-htonl"></a>

**`htonl`**

```haproxy
htonl
```

入力整数値をネットワークバイトオーダーでの32ビットバイナリ表現に変換します。サンプル取得は符号付き64ビット整数を扱うため、このコンバーターを使用する場合、入力整数値はまず符号なし32ビット整数にキャストされます。

<a id="entry-7-3-1-http-date"></a>

**`http_date([<offset[,<unit>]])`**

```haproxy
http_date([<offset[,<unit>]])
```

エポックからの日付を表す整数値を、HTTPヘッダー項目で使用可能な形式の文字列に変換します。オフセット値が指定された場合、変換前に日付にオフセット値が加算されます。これは、Date ヘッダーフィールドを生成する場合、正のオフセットと組み合わせてレスポンスの Expires 値を生成する場合、負のオフセットと組み合わせて Last-Modified 値を生成する場合に特に便利です。単位値が指定された場合、タイムスタンプを、エポックからの "s"（秒、デフォルト）、"ms"（ミリ秒）、または "us"（マイクロ秒）として扱います。オフセットは入力タイムスタンプと同じ単位であると仮定されます。

<a id="entry-7-3-1-iif"></a>

**`iif(<true>,<false>)`**

```haproxy
iif(<true>,<false>)
```

入力値が true の場合、`<true>` 文字列を返します。それ以外の場合は `<false>` 文字列を返します。

例：

```text
http-request set-header x-forwarded-proto %[ssl_fc,iif(https,http)]
```

<a id="entry-7-3-1-in-table"></a>

**`in_table([<table>])`**

```haproxy
in_table([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブルまたは指定されたスティックテーブル内で照合を行います。キーがテーブルに存在しない場合、真偽値 false が返されます。それ以外の場合は論理値 true が返されます。これは、何らかの要素を追跡するテーブルに特定のキーが存在するかを調べるために使用できます（たとえば、送信元IPアドレスやAuthorizationヘッダーが以前に現れたかどうかを確認する場合）。

<a id="entry-7-3-1-ip-data"></a>

**`ip.data`**

```haproxy
ip.data
```

これは、"tcp-ss" バインドオプションを "1" に設定したときに "fc_saved_syn" が返すバイナリイーサネットフレーム、または "eth.data" の出力に使用されます。IPヘッダーおよび任意のオプションまたは拡張をスキップし、トランスポートプロトコル（通常はTCPまたはUDP）から始まるバイナリデータブロックを返します。また、"fc_saved_syn"、"tcp-ss"、"eth.data" を参照してください。

<a id="entry-7-3-1-ip-df"></a>

**`ip.df`**

```haproxy
ip.df
```

これは、"tcp-ss" バインドオプションを "1" に設定したときに "fc_saved_syn" が返すバイナリイーサネットフレーム、または "eth.data" の出力に使用されます。IPヘッダーの DF（フラグメント禁止）フラグが設定されている場合に整数値1を返し、それ以外の場合は0を返します。IPv6にはDFフラグがなく、デフォルトでフラグメントされないため、常に1を返します。また、"fc_saved_syn"、"tcp-ss"、"eth.data" を参照してください。

<a id="entry-7-3-1-ip-dst"></a>

**`ip.dst`**

```haproxy
ip.dst
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPv4/v6ヘッダーから、IPv4またはIPv6の宛先アドレスを返します。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。

<a id="entry-7-3-1-ip-fp"></a>

**`ip.fp([<mode>])`**

```haproxy
ip.fp([<mode>])
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPヘッダーとTCPヘッダーのさまざまな部分を調べ、外見上は同じ複数のホストを区別するために使える、不変部分のフィンガープリントのようなものを作成します。実際の用途は、共有IPアドレスの背後にある問題のあるホストの識別精度を高め、問題を起こしてブロックすべきホストが1台だけのときに、正当なユーザーをブロックしないようにすることです。このコンバーターは、入力に基づいて最小8バイトのバイナリーブロックを作成します。フィンガープリントのバイトは、次のように配置します。- バイト0: IP TOSフィールド（ip.tosを参照）- バイト1: - ビット7: IPv6 (1) / IPv4 (0) - ビット6: ip.df - ビット5..4: 0:ip.ttl\<=32; 1:ip.ttl\<=64; 2:ip.ttl\<=128; 3:ip.ttl\<=255 - ビット3: IPオプションあり (1) / なし (0) - ビット2: TCPデータあり (1) / なし (0) - ビット1: TCP.flagsのCWRが設定済み (1) / クリア済み (0) - ビット0: TCP.flagsのECEが設定済み (1) / クリア済み (0) - バイト2: - ビット7..4: 4バイトワード単位のTCPヘッダー長 - ビット3..0: TCPウィンドウスケーリング + 1 (1..15) / 0（WSの通知なし）- バイト3..4: tcp.win - バイト5..6: tcp.options.mss。存在しない場合はゼロ - バイト7: 存在するTCPオプションごとに1ビット。オプション2から8をそれぞれビット0..6に対応付け、ビット7は9から255までのいずれかのオプションが存在することを示します。

`<mode>` 引数を使うと、フィンガープリントに情報を追加できます。デフォルトでは、`<mode>` 引数が未設定またはゼロの場合、フィンガープリントは前述の8バイトだけで構成されます。`<mode>` に別の値を指定した場合、その値は次の値の合計を表し、対応する要素を以下の順序でフィンガープリントに連結します。- 1: 受信したTTL値をフィンガープリントに追加します（1バイト）。- 2: "tcp.options_list" が返すTCPオプション種別の一覧を、0から40バイトの追加データとしてフィンガープリントに追加します。- 4: 送信元IPアドレスをフィンガープリントに追加します。IPv4では4バイト、IPv6では16バイト増えます。

例：基本のFP、TTL、送信元アドレスを使って、13..25バイトのフィンガープリントを作成します（1+4=5）。

    frontend test
        mode http
        bind :4445 tcp-ss 1
        tcp-request connection set-var(sess.syn) fc_saved_syn
        http-request return status 200 content-type text/plain lf-string &#92;
              "src=%[var(sess.syn),ip.src] fp=%[var(sess.syn),ip.fp(5),hex]&#92;n"

"fc_saved_syn"、"tcp-ss"、"eth.data"、"ip.df"、"ip.ttl"、"tcp.win"、"tcp.options.mss"、および "tcp.options_list" も参照してください。

<a id="entry-7-3-1-ip-hdr"></a>

**`ip.hdr`**

```haproxy
ip.hdr
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPヘッダーから始まり、最後のオプションまたは拡張の後、トランスポートプロトコルヘッダーの前までのバイナリーデータブロックを返します。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。


<a id="entry-7-3-1-ip-proto"></a>

**`ip.proto`**

```haproxy
ip.proto
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。トランスポートプロトコル番号を返します。通常はTCPが6、UDPが17です。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。


<a id="entry-7-3-1-ip-src"></a>

**`ip.src`**

```haproxy
ip.src
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPv4/v6ヘッダーから、IPv4またはIPv6の送信元アドレスを返します。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。


<a id="entry-7-3-1-ip-tos"></a>

**`ip.tos`**

```haproxy
ip.tos
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPv4ヘッダーのサービス種別 (TOS) フィールド、またはIPv6ヘッダーのトラフィッククラス (TC) フィールドの値に対応する整数を返します。現在のインターネットでは、このフィールドの上位6ビットは通常DSCP (Differentiated Services Codepoint) 値を含み、下位2ビットは未使用か、IP ECNに使用されます。DSCP値についてはRFC2474とRFC8436を、IP ECNフィールドについてはRFC3168を参照してください。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。

<a id="entry-7-3-1-ip-ttl"></a>

**`ip.ttl`**

```haproxy
ip.ttl
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPv4/IPv6ヘッダーのTTL (Time To Live) またはHL (Hop Limit) フィールドに対応する整数を返します。この値は通常、固定の値にあらかじめ設定され、パケットが通過するルーターごとに減らされます。初期値が分かれば、クライアントがどれほど遠くから接続しているかを推測するのに役立ちます。最近のほとんどのOSは、初期値64で開始します。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。


<a id="entry-7-3-1-ip-ver"></a>

**`ip.ver`**

```haproxy
ip.ver
```

"tcp-ss" bindオプションを "1" に設定したときに "fc_saved_syn" が返す、バイナリーのイーサネットフレームを表す入力サンプル、または "eth.data" の出力に対して使用します。IPヘッダーのIPバージョンを返します。通常は4または6です。上位レイヤーのイーサネットフレーム内のプロトコル番号と一致するかは検査しません。ただし、有効なパケットに対して使用することを想定しているため、この点はOSがすでに検証済みであると想定します。"fc_saved_syn"、"tcp-ss"、および "eth.data" も参照してください。


<a id="entry-7-3-1-ipmask"></a>

**`ipmask(<mask4>[,<mask6>])`**

```haproxy
ipmask(<mask4>[,<mask6>])
```

IPアドレスにマスクを適用し、結果を検索と保存に使用します。これにより、特定のマスク内のすべてのホストで同じテーブルエントリーを共有し、同じサーバーを使用できます。mask4はドット形式（255.255.255.0など）、またはCIDR形式（24など）で指定できます。mask6は4桁ずつに区切った形式（ffff:ffff::など）、またはCIDR形式（64など）で指定できます。mask6を指定しない場合、後方互換性のため、IPv6アドレスの変換は失敗します。


<a id="entry-7-3-1-json"></a>

**`json([<input-code>])`**

```haproxy
json([<input-code>])
```

入力文字列をエスケープし、JSON文字列としてそのまま使用できるASCII出力文字列を生成します。コンバーターは `<input-code>` パラメーターに従って入力文字列のデコードを試みます。指定できる値は "ascii"、"utf8"、"utf8s"、"utf8p"、"utf8ps" です。"ascii" デコーダーは決して失敗しません。"utf8" デコーダーは3種類のエラーを検出します。

- 不正なUTF-8シーケンス（孤立した継続バイト、継続バイトの数が不正など）
- 無効な範囲（デコードされた値がUTF-8で禁止されている範囲内にある）
- 過長エンコーディング（必要以上に多くのバイトで値がエンコードされている）

UTF-8のJSONエンコードでは、UTF-8文字が0xffffを超える場合に "too long value" エラーが発生することがあります。JSONの文字列エスケープ仕様が、値のエンコードに4桁の16進数しか認めていないためです。UTF-8デコーダーには、2つの接尾辞文字の組み合わせで表す4種類があります。"p" は寛容な処理 ("permissive")、"s" は通知せずに無視する処理 ("silently ignore") を表します。各デコーダーの動作は次のとおりです。

- "ascii": 決して失敗しません。
- "utf8": エラーを検出すると、種類を問わず失敗します。
- "utf8s": 決して失敗しませんが、エラーに対応する文字を削除します。
- "utf8p": 過長エラーは受け入れて修正しますが、それ以外のエラーでは失敗します。
- "utf8ps": 決して失敗しません。過長エラーは受け入れて修正しますが、それ以外のエラーに対応する文字は削除します。

このコンバーターは、JSON形式のトラフィックログを処理するサーバーへのログ出力用に、適切にエスケープされたJSONを作成する際に特に便利です。

例：

```text
capture request header Host len 15
capture request header user-agent len 150
log-format '{"ip":"%[src]","user-agent":"%[capture.req.hdr(1),json(utf8s)]"}'
```

クライアント127.0.0.1からのリクエスト：

```text
GET / HTTP/1.0
User-Agent: Very "Ugly" UA 1/2
```

出力ログ：

```text
{"ip":"127.0.0.1","user-agent":"Very \"Ugly\" UA 1\/2"}
```

<a id="entry-7-3-1-json-query"></a>

**`json_query(<json_path>[,<output_type>])`**

```haproxy
json_query(<json_path>[,<output_type>])
```

json_queryコンバーターは、JSONのstring、boolean、number、array型をサポートします。浮動小数点数は文字列として返します。output_typeに 'int' を指定すると、値を整数に変換します。配列は、先頭と末尾を角かっこで囲んだ文字列として返します。内容はCSV形式です。データ型によって、配列の値を引用符で囲む場合があります。配列の値が複合型の場合、各値の完全なJSON表現をコンマで区切って文字列に含めます。JWTに対するrolesクエリの結果の例を示します。

```text
["manage-account","manage-account-links","view-profile"]
```

変換できない場合、json_queryコンバーターは失敗します。

`<json_path>` は <https://datatracker.ietf.org/doc/draft-ietf-jsonpath-base/> で定義された有効な JSON Path 文字列でなければなりません。

注意：コンテキストや下位実装によっては、重複する JSON キーの抽出が未定義であり、入力コンテンツから同じキーの最初、最後、または任意の出現を返す可能性があります。また、キー名がエンコードされた形で渡された場合、常に一致するとは限りません。要するに、このコンバーターはコンテンツのサニタイズには適していません。

例：

```shell
# get a integer value from the request body
# "{"integer":4}" => 5
http-request set-var(txn.pay_int) req.body,json_query('$.integer','int'),add(1)

# get a key with '.' in the name
# {"my.key":"myvalue"} => myvalue
http-request set-var(txn.pay_mykey) req.body,json_query('$.my\\.key')

# {"boolean-false":false} => 0
http-request set-var(txn.pay_boolean_false) req.body,json_query('$.boolean-false')

# get the value of the key 'iss' from a JWT Bearer token
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec,json_query('$.iss')
```

<a id="entry-7-3-1-jwt-decrypt-cert"></a>

**`jwt_decrypt_cert(<cert>)`**

```haproxy
jwt_decrypt_cert(<cert>)
```

入力されたJSON Web Tokenについて、JSON Web Encryption形式（RFC 7516を参照）に従って署名を検証し、指定した証明書で復号した内容を返します。`<cert>` パラメーターは、すでに読み込まれた証明書へのパスでなければなりません（CLIコマンド "dump ssl cert" でダンプできます）。証明書の "jwt" オプションは、明示的に "on" に設定されていなければなりません（crt-listの "jwt" オプションを参照してください）。直接指定することも、変数を介して指定することもできます。現在扱えるのは、Compact Serialization形式（base64-urlでエンコードした5つの文字列をドットで区切った形式）を使用するトークンだけです。

このコンバーターは、JOSE ヘッダーの "alg" フィールドに以下のアルゴリズムが含まれるトークンで使用できます：RSA-OAEP、RSA-OAEP-256、ECDH-ES、ECDH-ES+A128KW、ECDH-ES+A192KW、ECDH-ES+A256KW。RSA1_5 アルゴリズムは実装されていますが、RFC 8725 の [3.2節](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) に従ってデフォルトで無効になっています。必要に応じて 'jwt.decrypt_alg_list' グローバルオプションで再有効化できます。

サポートされるアルゴリズムおよび暗号化アルゴリズム（それぞれ JOSE ヘッダーの "alg" および "enc" フィールド）は、'jwt.decrypt_alg_list' および 'jwt.decrypt_enc_list' グローバルオプションによって変更できます。

JWEトークンは、base64urlエンコードした形式で渡さなければなりません。出力は "raw" 形式で返します。トークンのパース、署名検証、または内容の復号中にエラーが発生した場合、空文字列が返されます。

例：

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_cert("/foo/bar.pem")]
```

<a id="entry-7-3-1-jwt-decrypt-jwk"></a>

**`jwt_decrypt_jwk(<jwk>)`**

```haproxy
jwt_decrypt_jwk(<jwk>)
```

入力された JSON Web Token に対して、JSON Web Encryption 形式（RFC 7516 参照）に従った署名検証を行い、提供された JSON Web Key (RFC7517) を使って内容を復号して返します。`<jwk>` パラメーターは、'oct'、'EC'、または 'RSA' 型（JSON キーの 'kty' フィールド）の有効な JWK でなければなりません。JWK は文字列として、または変数経由で提供できます。

現在扱えるのは、Compact Serialization形式（base64-urlでエンコードした5つの文字列をドットで区切った形式）を使用するトークンだけです。

このコンバーターは、JOSE ヘッダーの "alg" フィールドに以下の対称型アルゴリズムが含まれるトークンのデコードに使用できます：A128KW、A192KW、A256KW、A128GCMKW、A192GCMKW、A256GCMKW、dir。この場合、提供された JWK は 'oct' 型であることを想定しています。

このコンバーターは、JOSEヘッダーの "alg" フィールドに指定したアルゴリズムに応じて、'RSA' JWK が提供された場合はRSA ファミリー（RSA-OAEP または RSA-OAEP-256）のアルゴリズムを、'EC' JWK が提供された場合、ECDH ファミリー（ECDH-ES、ECDH-ES+A128KW、ECDH-ES+A192KW、ECDH-ES+A256KW）のアルゴリズムを処理します。RSA1_5 アルゴリズムは実装されていますが、RFC 8725 の [3.2節](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) に従ってデフォルトで無効になっています。必要に応じて 'jwt.decrypt_alg_list' グローバルオプションで再有効化できます。

AWS-LC では A128KW および A192KW アルゴリズムが利用できないため、A128KW、A192KW、ECDH-ES+A128KW、ECDH-ES+A192KW アルゴリズムは動作しません。

サポートされるアルゴリズムおよび暗号化アルゴリズム（それぞれ JOSE ヘッダーの "alg" および "enc" フィールド）は、'jwt.decrypt_alg_list' および 'jwt.decrypt_enc_list' グローバルオプションによって変更できます。

JWEトークンは、base64urlエンコードした形式で渡さなければなりません。出力は "raw" 形式で返します。トークンのパース、署名検証、または内容の復号中にエラーが発生した場合、空文字列が返されます。

構成におけるクォート、コンマ、ダブルクォートの取り扱いの都合上、JWK の内容はこのコンバーターが正しく動作するためには適切にエスケープされている必要があります（詳細は [2.2節](/ja/haproxy/configuration-basics/#section-2-2) を参照）。

例：

```shell
 # Get a JWT from the authorization header, put its decrypted content in an
 # HTTP header
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(\'{\"kty\":\"oct\",\"k\":\"wAsgsg\"}\')

# or via a variable
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-var(txn.jwk) str(\'{\"kty\":\"oct\",\"k\":\"Q-NFLlghQ\"}\')
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(txn.jwk)
```

<a id="entry-7-3-1-jwt-decrypt-secret"></a>

**`jwt_decrypt_secret(<secret>)`**

```haproxy
jwt_decrypt_secret(<secret>)
```

入力されたJSON Web Tokenについて、JSON Web Encryption形式（RFC 7516を参照）に従って署名を検証し、指定したbase64エンコード済みシークレットで復号した内容を返します。シークレットは、文字列として、または変数を介して指定できます。現在扱えるのは、Compact Serialization形式（base64-urlでエンコードした5つの文字列をドットで区切った形式）を使用するトークンだけです。

このコンバーターは、JOSE ヘッダーの "alg" フィールドに以下のアルゴリズムが含まれるトークンで使用できます：A128KW、A192KW、A256KW、A128GCMKW、A192GCMKW、A256GCMKW、dir。ただし、A128KW および A192KW アルゴリズムは AWS-LC では利用できないため、復号できません。

JWEトークンは、base64urlエンコードした形式で渡さなければなりません。出力は "raw" 形式で返します。トークンのパース、署名検証、または内容の復号中にエラーが発生した場合、空文字列が返されます。

例：

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_secret("GawgguFyGrWKav7AX4VKUg")]
```

<a id="entry-7-3-1-jwt-header-query"></a>

**`jwt_header_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_header_query([<json_path>[,<output_type>]])
```

入力された JSON Web Token (JWT) に対して、パラメーターが指定されていない場合はトークンのデコードされたヘッダー部分（JWT の最初の base64-url エンコードされた部分）を返します。パラメーターが指定されている場合は、デコードされたヘッダー部分に対して json_query を実行します。受け入れられる json_path および output_type パラメーターの詳細については "json_query" コンバーターを参照してください。このコンバーターは、コンパクトシリアライゼーション形式の JWS または JWE トークンで使用できます。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

<a id="entry-7-3-1-jwt-payload-query"></a>

**`jwt_payload_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_payload_query([<json_path>[,<output_type>]])
```

入力された JSON Web Signed (JWS) 形式の JSON Web Token (JWT) に対して、パラメーターが指定されていない場合はトークンのデコードされたペイロード部分（JWT の2番目の base64-url エンコードされた部分）を返します。パラメーターが指定されている場合は、デコードされたペイロード部分に対して json_query を実行します。受け入れられる json_path および output_type パラメーターの詳細については "json_query" コンバーターを参照してください。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

jwt_verify(`<alg>`,`<key>`)

入力されたJSON Web Token (JWT) の署名を、`<alg>` アルゴリズムと `<key>` パラメーターを使って検証します。現在処理できるのは、Compact Serialization形式（base64-urlでエンコードした3つの文字列をドットで区切った形式）を使用するJWSトークンだけです。このコンバーターはトークンの署名だけを検証し、RFC7519の[7.2節](https://www.rfc-editor.org/rfc/rfc7519#section-7.2)で規定された完全なJWT検証は行いません。たとえば、デコード後のヘッダーとペイロードの内容が、完全に有効なJSONであることは保証せず、それぞれの内容に対するチェックも行いません。

- `<alg>` は、検証に使用するアルゴリズムの名前を保持する文字列、または変数名にできます（"set-var" も参照してください）。

  RFC7518の[3.1節](https://www.rfc-editor.org/rfc/rfc7518#section-3.1)に記載されたアルゴリズムに対応しています。

```text
   +--------------+---------------------------------------------------------+
   | "alg"の      | デジタル署名またはMACアルゴリズム                       |
   | 値           |                                                         |
   +--------------+---------------------------------------------------------+
   | HS256        | SHA-256を使用するHMAC                                   |
   | HS384        | SHA-384を使用するHMAC                                   |
   | HS512        | SHA-512を使用するHMAC                                   |
   | RS256        | SHA-256を使用するRSASSA-PKCS1-v1_5                      |
   | RS384        | SHA-384を使用するRSASSA-PKCS1-v1_5                      |
   | RS512        | SHA-512を使用するRSASSA-PKCS1-v1_5                      |
   | ES256        | P-256とSHA-256を使用するECDSA                           |
   | ES384        | P-384とSHA-384を使用するECDSA                           |
   | ES512        | P-521とSHA-512を使用するECDSA                           |
   | PS256        | SHA-256とMGF1（SHA-256）を使用するRSASSA-PSS            |
   | PS384        | SHA-384とMGF1（SHA-384）を使用するRSASSA-PSS            |
   | PS512        | SHA-512とMGF1（SHA-512）を使用するRSASSA-PSS            |
   | none         | デジタル署名もMACも実行しません（下記の注記を参照） |
   +--------------+---------------------------------------------------------+
```

RFC8725の[セクション3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2)の推奨に従い、"none"アルゴリズムはデフォルトでは許可しません。明示的に許可するには、globalオプション'jwt.allow_none_alg'を設定してください。


- `<key>` は、シークレットまたは公開鍵のパスを保持する文字列、または変数名にできます（"set-var" も参照してください）。

  シークレットは、HMACアルゴリズムを使用する場合にのみ適用できます。

  公開鍵は、PKCS#1形式（RSA鍵用で、BEGIN RSA PUBLIC KEYで始まります）、またはSPKI形式（Subject Public Key Infoで、BEGIN PUBLIC KEYで始まります）でなければなりません。公開鍵は設定の解析時に利用できなければならず、実行時に更新したり読み込んだりすることはできません。完全なPEM証明書に基づくJWTトークンの検証については、"jwt_verify_cert" コンバーターを参照してください。

  JWTの検証に使用する可能性があるすべての公開鍵は、初期化時に分かっていなければなりません。専用のキャッシュに追加し、実行時のディスクアクセスを不要にするためです。

検証に成功すると1、検証に失敗すると0、それ以外のエラーでは厳密に負の値を返します。このようにゼロでないエラー戻り値があるため、このコンバーターの結果を決して真偽値に変換すべきではありません。取り得る戻り値の完全な一覧は、以下を参照してください。

可能な戻り値は以下の通りです：

```text
  +----+----------------------------------------------------------------------+
  | ID | メッセージ                                                           |
  +----+----------------------------------------------------------------------+
  |  1 | "Verification success"                                               |
  |  0 | "Verification failure"                                               |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)"                       |
  | -2 | "Unmanaged algorithm"                                                |
  | -3 | "Invalid token"                                                      |
  | -4 | "Out of memory"                                                      |
  | -5 | "Unknown pubkey/certificate"                                         |
  | -6 | "Internal error"                                                     |
  +----+----------------------------------------------------------------------+
```

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

例：

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public key to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify(txn.jwt_alg,"/path/to/pubkey.pem") 1 }
```

jwt_verify_cert(`<alg>`,`<cert>`)

入力されたJSON Web Token (JWT) の署名を、`<alg>` アルゴリズムと `<cert>` パラメーターを使って検証します。現在処理できるのは、Compact Serialization形式（base64-urlでエンコードした3つの文字列をドットで区切った形式）を使用するJWSトークンだけです。このコンバーターはトークンの署名だけを検証し、RFC7519の[7.2節](https://www.rfc-editor.org/rfc/rfc7519#section-7.2)で規定された完全なJWT検証は行いません。たとえば、デコード後のヘッダーとペイロードの内容が、完全に有効なJSONであることは保証せず、それぞれの内容に対するチェックも行いません。

- `<alg>` は、検証に使用するアルゴリズムの名前を保持する文字列、または変数名にできます（"set-var" も参照してください）。"jwt_verify" コンバーターとは異なり、このコンバーターは第2パラメーターとして証明書だけを想定するため、HMACアルゴリズムを使用するトークンには使用すべきではありません。

  RFC7518の[3.1節](https://www.rfc-editor.org/rfc/rfc7518#section-3.1)に記載されたアルゴリズムに、HMACを除いて対応しています。

```text
   +--------------+---------------------------------------------------------+
   | "alg"の      | デジタル署名またはMACアルゴリズム                       |
   | 値           |                                                         |
   +--------------+---------------------------------------------------------+
   | RS256        | SHA-256を使用するRSASSA-PKCS1-v1_5                      |
   | RS384        | SHA-384を使用するRSASSA-PKCS1-v1_5                      |
   | RS512        | SHA-512を使用するRSASSA-PKCS1-v1_5                      |
   | ES256        | P-256とSHA-256を使用するECDSA                           |
   | ES384        | P-384とSHA-384を使用するECDSA                           |
   | ES512        | P-521とSHA-512を使用するECDSA                           |
   | PS256        | SHA-256とMGF1（SHA-256）を使用するRSASSA-PSS            |
   | PS384        | SHA-384とMGF1（SHA-384）を使用するRSASSA-PSS            |
   | PS512        | SHA-512とMGF1（SHA-512）を使用するRSASSA-PSS            |
   | none         | デジタル署名もMACも実行しません                         |
   +--------------+---------------------------------------------------------+
```

- `<key>` は、証明書のパスを保持する文字列、または変数名にできます（"set-var" も参照してください）。

  証明書は、標準のPEM証明書（BEGIN CERTIFICATEで始まるもの）でなければなりません。パスをコンバーターに直接渡すか、変数を介して参照できます。変数を使う場合、対応する証明書は、crt-storeで宣言することも、統計ソケット経由で動的に読み込むこともできます。パスを直接指定した場合、対応する証明書が内部の証明書ストアにまだ読み込まれていなければ、設定の解析中に読み込みます。そのため、証明書はすでに存在していなければならず、存在しない場合はエラーが発生します。

  JWTの検証に使用できると明示的に定義した証明書だけを使用できます。crt-storeの "jwt" オプションを参照してください。

  統計ソケットを使って、証明書を動的に更新したり、新しい証明書を追加したりできます。管理ガイドの "set ssl cert" と "new ssl cert" も参照してください。

検証に成功すると1、検証に失敗すると0、それ以外のエラーでは厳密に負の値を返します。このようにゼロでないエラー戻り値があるため、このコンバーターの結果を決して真偽値に変換すべきではありません。取り得る戻り値の完全な一覧は、以下を参照してください。

可能な戻り値は以下の通りです：

```text
  +----+----------------------------------------------------------------------+
  | ID | メッセージ                                                           |
  +----+----------------------------------------------------------------------+
  |  1 | "Verification success"                                               |
  |  0 | "Verification failure"                                               |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)"                       |
  | -2 | "Unmanaged algorithm"                                                |
  | -3 | "Invalid token"                                                      |
  | -4 | "Out of memory"                                                      |
  | -5 | "Unknown pubkey/certificate"                                         |
  | -6 | "Internal error"                                                     |
  | -7 | "Unavailable certificate" ("jwt"参照)                                |
  +----+----------------------------------------------------------------------+
```

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

例：

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public certificate to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify_cert(txn.jwt_alg,"/path/to/cert.pem") 1 }
```

<a id="entry-7-3-1-language"></a>

**`language(<value>[,<default>])`**

```haproxy
language(<value>[,<default>])
```

"accept-language" ヘッダーから "req.fhdr" を使用して抽出されたリストから、q-factor が最大の値を返します。q-factor を持たない値の q-factor は 1 とみなされ、q-factor が 0 の値は除外されます。半角セミコロン区切りの `<values>` に含まれる値のみを対象とします。引数 `<value>` の構文は "lang[;lang[;lang[;...]]]" です。指定されたリストに一致する値が存在せず、デフォルト値が提供されている場合、そのデフォルト値が返されます。言語名にはダッシュ（'-'）の後にバリアントが付くことがあります。バリアントがリストに含まれている場合は一致しますが、含まれていない場合はベース言語のみがチェックされます。一致は大文字小文字を区別し、出力文字列は常に引数で提供されたものの中から選ばれます。引数の順序には意味がなく、リクエスト内の値の順序だけが有効です。同じq-factorを持つ値が複数ある場合、その中で最初の値を使用します。

例：

```shell
# this configuration switches to the backend matching a
# given language based on the request:

acl es req.fhdr(accept-language),language(es;fr;en) -m str es
acl fr req.fhdr(accept-language),language(es;fr;en) -m str fr
acl en req.fhdr(accept-language),language(es;fr;en) -m str en
use_backend spanish if es
use_backend french  if fr
use_backend english if en
default_backend choose_your_language
```

<a id="entry-7-3-1-length"></a>

**`length`**

```haproxy
length
```

文字列の長さを取得します。これは文字列のサンプル取得関数の直後、または文字列型を返す変換キーワードの直後にのみ配置できます。結果の型は整数です。

<a id="entry-7-3-1-lower"></a>

**`lower`**

```haproxy
lower
```

文字列のサンプルを小文字に変換します。これは文字列のサンプル取得関数の直後、または文字列型を返す変換キーワードの直後にのみ配置できます。結果の型は文字列です。

<a id="entry-7-3-1-ltime"></a>

**`ltime(<format>[,<offset>])`**

```haproxy
ltime(<format>[,<offset>])
```

エポックからの日付を表す整数を、`<format>` 文字列で定義されたフォーマット（strftime(3) を使用）に従ってローカル時間の文字列に変換します。ログに任意の日付フォーマットを使用できるようにする目的があります。入力日付にオプションの `<offset>`（秒単位、正または負）を適用できます。使用するOSがサポートする書式は、strftime()のmanページを参照してください。utime コンバーターも参照してください。

例：

```shell
# Emit two colons, one with the local time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,ltime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-ltrim"></a>

**`ltrim(<chars>)`**

```haproxy
ltrim(<chars>)
```

入力サンプルの文字列表現の先頭から、`<chars>` に含まれる文字をすべてスキップします。

<a id="entry-7-3-1-map"></a>

**`map(<map_name>[,<default_value>])`**

```haproxy
map(<map_name>[,<default_value>])
map_<match_type>(<map_name>[,<default_value>])
map_<match_type>_<output_type>(<map_name>[,<default_value>])
```

`<match_type>` の照合方法を使って `<map_name>` から入力値を検索し、対応する値を `<output_type>` 型に変換して返します。入力値が `<map_name>` に存在しない場合、コンバーターは `<default_value>` を返します。`<default_value>` が設定されていない場合、コンバーターは失敗し、入力値が取得できなかったものとして動作します。`<match_type>` が設定されていない場合、デフォルトは "str" です。同様に、`<output_type>` が設定されていない場合、デフォルトは "str" です。便宜上、"map" キーワードは "map_str" のエイリアスであり、文字列を別の文字列にマップします。`<map_name>` は 2.7 節のマップおよび ACL の名前形式に従う必要があります。

キーの範囲が重ならないようにすることが重要です。IPアドレスと文字列はツリーに格納するため、最も具体的な一致のうち、最初のものを使用します。それ以外のキーはリストに格納するため、最初に一致したものを使用します。

次の表に、使用できるすべてのマップ関数を、入力型、照合方式、出力型の順に並べて示します。

```text
 入力型      | 照合方法     | 出力型 str      | 出力型 int      | 出力型 ip      | 出力型 key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | str          | map_str         | map_str_int     | map_str_ip     | map_str_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | beg          | map_beg         | map_beg_int     | map_beg_ip     | map_beg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | sub          | map_sub         | map_sub_int     | map_sub_ip     | map_sub_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | dir          | map_dir         | map_dir_int     | map_dir_ip     | map_dir_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | dom          | map_dom         | map_dom_int     | map_dom_ip     | map_dom_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | end          | map_end         | map_end_int     | map_end_ip     | map_end_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | reg          | map_reg         | map_reg_int     | map_reg_ip     | map_reg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    str      | reg          | map_regm        | map_reg_int     | map_reg_ip     | map_reg_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    int      | int          | map_int         | map_int_int     | map_int_ip     | map_int_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
    ip       | ip           | map_ip          | map_ip_int      | map_ip_ip      | map_ip_key
  -----------+--------------+-----------------+-----------------+----------------+----------------
```

特殊なマップ "map_regm" は、正規表現にキャプチャーグループがあることを想定し、後方参照（"&#92;1" など）を対応する一致テキストに置き換えて、出力を変更します。

出力型 "key" は、値ではなく、一致したエントリのキー（マップファイルに記載されたもの）を文字列として返すことを意味します。この出力型を使用する場合、オプションの `<default_value>` 引数はサポートされません。

`<map_name>` で参照されるファイルには、1行に1つのキーと値が含まれます。'#' で始まる行は無視され、空行と同じ扱いになります。先頭のタブや空白は削除されます。キーは最初の「単語」（スペースとタブ以外の文字の並び）です。値は、その後に続くスペースとタブの並びの後から行末までの部分で、末尾のスペースとタブを除きます。

例：

```text
     # this is a comment and is ignored
        2.22.246.0/23    United Kingdom      \n
     <-><-----------><--><------------><---->
      |       |       |         |        `- 末尾の空白は無視
      |       |       |         `---------- 値
      |       |       `-------------------- 中間の空白は無視
      |       `---------------------------- キー
      `------------------------------------ 先頭の空白は無視
```

<a id="entry-7-3-1-mod"></a>

**`mod(<value>)`**

```haproxy
mod(<value>)
```

入力値（符号付き整数型）を `<value>` で割り、その余りを符号付き整数として返します。`<value>` がゼロの場合、ゼロを返します。`<value>` は数値または変数名です。詳細は [2.8節](/ja/haproxy/configuration-basics/#section-2-8) の変数についてを参照してください。

<a id="entry-7-3-1-mqtt-field-value"></a>

**`mqtt_field_value(<packettype>,<fieldname_or_property_ID>)`**

```haproxy
mqtt_field_value(<packettype>,<fieldname_or_property_ID>)
```

入力された `<packettype>` 型のMQTTペイロードにある、`<fieldname>` の値を返します。`<packettype>` は文字列（大文字小文字を区別しないマッチング）またはパケットの種類に対応する数値です。サポートされる文字列および整数は以下の通りです：
<https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718021>
<https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022>

`<fieldname>` は `<packettype>` に依存し、以下のいずれかになります。（`<fieldname>` のマッチングは大文字小文字を区別しません。）`<property id>` は MQTT v5.0 ストリームでのみ見つかります。以下の表を確認してください： <https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901029>

- CONNECT (または 1): flags, protocol_name, protocol_version, client_identifier, will_topic,
  will_payload, username, password, keepalive または任意のプロパティ ID を数値として指定（MQTT v5.0 パケットのみ）:

```text
17: Session Expiry Interval
33: Receive Maximum
39: Maximum Packet Size
34: Topic Alias Maximum
25: Request Response Information
23: Request Problem Information
21: Authentication Method
22: Authentication Data
18: Will Delay Interval
 1: Payload Format Indicator
 2: Message Expiry Interval
 3: Content Type
 8: Response Topic
 9: Correlation Data
```

まだサポートされていません：

```text
38: User Property
```

- CONNACK (または 2): flags, protocol_version, reason_code または任意のプロパティ ID を数値として指定（MQTT v5.0 パケットのみ）:

```text
17: Session Expiry Interval
33: Receive Maximum
36: Maximum QoS
37: Retain Available
39: Maximum Packet Size
18: Assigned Client Identifier
34: Topic Alias Maximum
31: Reason String
40; Wildcard Subscription Available
41: Subscription Identifiers Available
42: Shared Subscription Available
19: Server Keep Alive
26: Response Information
28: Server Reference
21: Authentication Method
22: Authentication Data
```

まだサポートされていません：

```text
38: User Property
```

現在の HAProxy の設計上、クライアントおよびサーバーが送信する最初のメッセージのみが解析可能です。したがって、このコンバーターは CONNECT および CONNACK パケット型からのみデータを抽出できます。CONNECT はクライアントが最初に送信するメッセージであり、CONNACK はサーバーが最初に送信する応答です。

例：

```shell
acl data_in_buffer req.len ge 4
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(connect,protocol_name) \
        if data_in_buffer
# do the same as above
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(1,protocol_name) \
        if data_in_buffer
```

<a id="entry-7-3-1-mqtt-is-valid"></a>

**`mqtt_is_valid`**

```haproxy
mqtt_is_valid
```

バイナリ入力が有効な MQTT パケットかどうかを確認します。真偽値を返します。

現在の HAProxy の設計上、クライアントおよびサーバーが送信する最初のメッセージのみが解析可能です。したがって、このコンバーターは CONNECT および CONNACK パケット型からのみデータを抽出できます。CONNECT はクライアントが最初に送信するメッセージであり、CONNACK はサーバーが最初に送信する応答です。

MQTT 3.1、3.1.1 および 5.0 のみがサポートされています。

例：

```text
acl data_in_buffer req.len ge 4
tcp-request content reject unless { req.payload(0,0),mqtt_is_valid }
```

<a id="entry-7-3-1-ms-ltime"></a>

**`ms_ltime(<format>[,<offset>])`**

```haproxy
ms_ltime(<format>[,<offset>])
```

"ltime" と同様に動作しますが、入力がミリ秒単位であることを想定しています。また、date(1) に由来する %N 変換指定子もサポートしています。エポックからの日付を表す整数を、`<format>` 文字列で定義されたフォーマットに従って strftime(3) を使用してローカル時間の文字列に変換します。目的は、ログで任意の日付フォーマットを使用可能にすることです。入力日付に、オプションの `<offset>`（ミリ秒単位、正または負の値）を適用できます。使用するOSがサポートする書式は、strftime()のmanページを参照してください。

%N 変換指定子を使用すると、日付のナノ秒部分を出力できます。入力がミリ秒単位であるため、精度は制限されています（000000000..999000000）。%N は % と N の間に幅引数を取ることができます。ミリ秒（%3N）やマイクロ秒（%6N）を表示するのに有用です。デフォルトおよび最大幅は 9（%N = %9N）です。

utime コンバーター（UTC 用）および "ltime" と "us_ltime" コンバーターについても参照してください。

例：

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/11:53:02.196 +0200 127.0.0.1:41530
log-format %[accept_date(ms),ms_ltime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-ms-utime"></a>

**`ms_utime(<format>[,<offset>])`**

```haproxy
ms_utime(<format>[,<offset>])
```

"utime" と同様に動作しますが、入力がミリ秒単位であることを想定しています。また、date(1) に由来する %N 変換指定子もサポートしています。エポックからの日付を表す整数を、`<format>` 文字列で定義されたフォーマットに従って strftime(3) を使用して UTC 時間の文字列に変換します。目的は、ログで任意の日付フォーマットを使用可能にすることです。入力日付に、オプションの `<offset>`（ミリ秒単位、正または負の値）を適用できます。使用するOSがサポートする書式は、strftime()のmanページを参照してください。

%N 変換指定子を使用すると、日付のナノ秒部分を出力できます。入力がミリ秒単位であるため、精度は制限されています（000000000..999000000）。%N は % と N の間に幅引数を取ることができます。ミリ秒（%3N）やマイクロ秒（%6N）を表示するのに有用です。デフォルトおよび最大幅は 9（%N = %9N）です。

ltime コンバーター（ローカル時間用）および "utime" と "us_utime" コンバーターについても参照してください。

例：

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196 +0000 127.0.0.1:41530
log-format %[accept_date(ms),ms_utime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-mul"></a>

**`mul(<value>)`**

```haproxy
mul(<value>)
```

入力値（符号付き整数型）を `<value>` で乗算し、その積を符号付き整数として返します。オーバーフローした場合、その符号で表現できる限界値を返し、演算結果のラップアラウンドを防ぎます。`<value>` は数値または変数名として指定できます。変数の詳細については [2.8節](/ja/haproxy/configuration-basics/#section-2-8) を参照してください。

<a id="entry-7-3-1-nbsrv"></a>

**`nbsrv`**

```haproxy
nbsrv
```

入力値（文字列型）をバックエンド名として解釈し、そのバックエンドに利用可能なサーバー数を返します。動的名前（たとえばマップ検索の結果など）からバックエンドを参照する場所で使用できます。

<a id="entry-7-3-1-neg"></a>

**`neg`**

```haproxy
neg
```

符号付き整数型の入力値の符号を反転した値を計算し、それを符号付き整数として返します。0は変化しません。この演算子は、逆向きの減算のために用意されています。定数から入力値を引くには、"neg,add(value)" を実行するだけです。

<a id="entry-7-3-1-not"></a>

**`not`**

```haproxy
not
```

符号付き整数型の入力値がゼロでなければ、真偽値FALSEを返し、それ以外はTRUEを返します。and()と併用すると、入力値のビットテスト（たとえば、フラグがないことの確認）について、真または偽を返すために使用できます。

<a id="entry-7-3-1-odd"></a>

**`odd`**

```haproxy
odd
```

入力値（符号付き整数型）が奇数の場合、真偽値 true を返し、それ以外（偶数）の場合、論理値 FALSE を返します。これは "and(1),bool" と機能的に同等です。

<a id="entry-7-3-1-or"></a>

**`or(<value>)`**

```haproxy
or(<value>)
```

`<value>` と入力値（符号付き整数型）のビット単位の "OR" を実行し、その結果を符号付き整数として返します。`<value>` は数値または変数名として指定できます。変数の詳細については [2.8節](/ja/haproxy/configuration-basics/#section-2-8) を参照してください。

<a id="entry-7-3-1-param"></a>

**`param(<name>[,<delim>])`**

```haproxy
param(<name>[,<delim>])
```

入力文字列からパラメーター `<name>` の最初の出現を抽出します。パラメータは `<delim>` で区切られ、デフォルトでは "&" が使用されます。パラメーター名と値は "=" で区切られます。パラメーターセグメントの末尾までに "=" と値が存在しない場合、空文字列とみなされます。

クエリ文字列や、場合によってはx-www-form-urlencodedの本文から、パラメーターを抽出するのに役立ちます。特に、`query,param(<name>)` は `urlp(<name>)` の代わりに使用でき、区切り文字として "&" だけを使用します。一方、"urlp" は "?" と ";" も使用します。

このコンバーターは URL エンコードされた文字に対して特別な処理を行いません。値をデコードしたい場合は、出力に対して url_dec コンバーターを使用してください。入力内のパラメーター名にエンコードされた文字が含まれる可能性がある場合、"param" を呼び出す前に入力を正規化することを推奨します。これは "http-request normalize-uri" を使用して行うことができ、特に percent-decode-unreserved および percent-to-uppercase オプションを利用できます。

例：

```text
str(a=b&c=d&a=r),param(a)   # b
str(a&b=c),param(a)         # ""
str(a=&b&c=a),param(b)      # ""
str(a=1;b=2;c=4),param(b,;) # 2
query,param(redirect_uri),urldec()
```

<a id="entry-7-3-1-port-only"></a>

**`port_only`**

```haproxy
port_only
```

Host ヘッダー値を含む文字列を、そのポート番号として整数に変換します。入力は Host ヘッダー値の形式（rfc9110#section-7.2）に従う必要があります。以下のような入力をサポートします：hostname、hostname:80、127.0.0.1、127.0.0.1:80、[::1]、[::1]:80。

入力にポートが指定されていない場合、0 を返します。

関連項目： ホストを返す "host_only" コンバーター。

<a id="entry-7-3-1-protobuf"></a>

**`protobuf(<field_number>[,<field_type>])`**

```haproxy
protobuf(<field_number>[,<field_type>])
```

Protocol Buffersメッセージのバイナリー表現である入力サンプルから、`<field_number>`（ドット表記）で指定したフィールドを抽出します。`<field_type>` を指定しない場合は生データとして、指定した場合は整数サンプルとして抽出します（後述の "ungrpc" も参照してください）。使用できる型は、"varint" ワイヤータイプ0では "int32"、"int64"、"uint32"、"uint64"、"sint32"、"sint64"、"bool"、"enum"、64ビットのワイヤータイプ1では "fixed64"、"sfixed64"、"double"、ワイヤータイプ5では "fixed32"、"sfixed32"、"float" です。"string" は長さ区切りの型として扱うため、抽出に `<field_type>` 引数は必要ありません。Protocol Buffersメッセージのフィールド型の詳細は、<https://developers.google.com/protocol-buffers/docs/encoding> を参照してください。

<a id="entry-7-3-1-regsub"></a>

**`regsub(<regex>,<subst>[,<flags>])`**

```haproxy
regsub(<regex>,<subst>[,<flags>])
```

入力文字列に、正規表現による置換を適用します。よく知られた "sed" ユーティリティーの "s/`<regex>`/`<subst>`/" と同じ操作を行います。デフォルトでは、入力文字列の中で、正規表現 `<regex>` に一致する最長の部分が最初に現れる箇所を、置換文字列 `<subst>` で置き換えます。第3引数 `<flags>` にフラグ "g" を追加すると、すべての一致箇所を置換することもできます。また、`<flags>` にフラグ "i" を追加すると、大文字と小文字を区別せずに正規表現を照合できます。`<flags>` は文字列なので、必要なすべてのフラグを連結して指定します。そのため、"i" と "g" の両方が必要な場合、"gi" と "ig" は同じ効果になります。このコンバーターの主な用途は、特定の文字や文字の並びを、ほかのものに置き換えることです。

正規表現部分を保護されたクォートで囲むことを強く推奨します。これにより、明確性が向上し、正規表現の閉じカッコが関数のカッコと混同されるのを防げます。Bourneシェルと同様に、1段階目のクォートは行上の単語グループを区切る際に処理され、2段階目のクォートは引数に使用可能です。外側にシングルクォートを使用することを推奨します。これは、バックスラッシュやドル記号の解決を試みないためです。

例：

```shell
# de-duplicate "/" in header "x-path".
# input:  x-path: /////a///b/c/xzxyz/
# output: x-path: /a/b/c/xzxyz/
http-request set-header x-path "%[hdr(x-path),regsub('/+','/','g')]"

# copy query string to x-query and drop all leading '?', ';' and '&'
http-request set-header x-query "%[query,regsub([?;&]*,'')]"

# capture groups and backreferences
# both lines do the same.
http-request redirect location %[url,'regsub("(foo|bar)([0-9]+)?","\2\1",i)']
http-request redirect location %[url,regsub(\"(foo|bar)([0-9]+)?\",\"\2\1\",i)]
```

<a id="entry-7-3-1-reverse"></a>

**`reverse`**

```haproxy
reverse
```

入力文字列をバイト単位で逆順にします。

このコンバーターはエンコーディングに依存せず、文字ではなくバイトを逆順にします。UTF-8でエンコードされた、人が読むためのテキストを逆順にするには適していません。

これにより、元の文字列の接尾辞照合を逆順文字列の接頭辞照合に変換でき、"map_beg" などのインデックス付き接頭辞マッチャーを大規模なマップで使用できるようになります。

例：

```shell
"example.com" -> "moc.elpmaxe"
"ab cd" -> "dc ba"

# Given a map file where each key contains a reversed hostname:
#   moc.elpmaxe.ppa app1
#   moc.elpmaxe.bd  dbcluster
# Pick a backend based on the domain suffix of the Host header:
use_backend %[req.hdr(host),lower,reverse,map_beg(/etc/haproxy/hosts.map,default)]
```

<a id="entry-7-3-1-reverse-dom"></a>

**`reverse_dom`**

```haproxy
reverse_dom
```

FQDNのようなホスト名を含む文字列を、ラベルを逆順にした形式に変換します。入力に末尾のドットが1つある場合は無視されます。空のラベルがあると、コンバーターは失敗します。

このコンバーターは入力を小文字に変換せず、ポートも削除しません。必要に応じて "lower" や "host_only" などの既存のコンバーターと組み合わせて使用することを想定しています。

末尾のドットのポリシーは意図的に呼び出し元に任されています。これにより、呼び出し元がアペックスもマッチさせたいか、サブドメインのみをマッチさせたいかを決定できるようになります。

逆順ラベル形式は、大規模なドメインマップで有用です。ドメインの接尾辞照合を接頭辞照合に変換でき、"map_beg" などのインデックス付き接頭辞マッチャーの使用が可能になります。

例：

```shell
"example.com" -> "com.example"
"mail.example.com" -> "com.example.mail"
"example.com." -> "com.example"

# match only subdomains of example.net, not the apex
acl example_net_sub req.hdr(Host),host_only,reverse_dom -m beg net.example.

# match only the apex
acl example_net_apex req.hdr(Host),host_only,reverse_dom -i net.example

# exact-or-subdomain prefix lookup using an explicit dotted form
http-request set-var(txn.rev_host) req.hdr(Host),host_only,reverse_dom,concat(.)
use_backend %[var(txn.rev_host),map_beg(/etc/haproxy/domains.map)]
```

<a id="entry-7-3-1-rfc7239-field"></a>

**`rfc7239_field(<field>)`**

```haproxy
rfc7239_field(<field>)
```

RFC 7239準拠のヘッダー値入力から1つのフィールド/パラメーターを抽出します。

サポートされるフィールドは以下の通りです。 - proto: 'http' または 'https' - host: HTTP準拠のホスト - for: RFC7239 ノード - by: RFC7239 ノード

詳細は以下を参照してください：

```text
https://www.rfc-editor.org/rfc/rfc7239.html#section-6
```

例：

```shell
# extract host field from forwarded header and store it in req.fhost var
http-request set-var(req.fhost) req.hdr(forwarded),rfc7239_field(host)
#input: "proto=https;host=\"haproxy.org:80\""
#  output: "haproxy.org:80"

# extract for field from forwarded header and store it in req.ffor var
http-request set-var(req.ffor) req.hdr(forwarded),rfc7239_field(for)
#input: "proto=https;host=\"haproxy.org:80\";for=\"127.0.0.1:9999\""
#  output: "127.0.0.1:9999"
```

<a id="entry-7-3-1-rfc7239-is-valid"></a>

**`rfc7239_is_valid`**

```haproxy
rfc7239_is_valid
```

入力ヘッダーが RFC 7239準拠のヘッダー値の場合に true を返し、それ以外の場合は false を返します。

例：

```shell
acl valid req.hdr(forwarded),rfc7239_is_valid
#input: "for=127.0.0.1;proto=http"
#  output: TRUE
#input: "proto=custom"
#  output: FALSE
```

<a id="entry-7-3-1-rfc7239-n2nn"></a>

**`rfc7239_n2nn`**

```haproxy
rfc7239_n2nn
```

'for' または 'by' 7239ヘッダーフィールドから提供された RFC7239 ノードを、対応するノード名の最終形式に変換します。 - IPv4アドレス - IPv6アドレス - 'unknown' - '\_obfs' 識別子

例：

```shell
# extract 'for' field from forwarded header, extract nodename from
# resulting node identifier and store the result in req.fnn
http-request set-var(req.fnn) req.hdr(forwarded),rfc7239_field(for),rfc7239_n2nn
#input: "127.0.0.1:9999"
#  output: 127.0.0.1 (ipv4)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: ab:cd:ff:ff:ff:ff:ff:ff (ipv6)
#input: "_name:_port"
#  output: "_name" (string)
```

<a id="entry-7-3-1-rfc7239-n2np"></a>

**`rfc7239_n2np`**

```haproxy
rfc7239_n2np
```

'for' または 'by' 7239ヘッダーフィールドから提供された RFC7239 ノードを、対応するノードポートの最終形式に変換します。 - 無符号整数 - '\_obfs' 識別子

例：

```shell
# extract 'by' field from forwarded header, extract node port from
# resulting node identifier and store the result in req.fnp
http-request set-var(req.fnp) req.hdr(forwarded),rfc7239_field(by),rfc7239_n2np
#input: "127.0.0.1:9999"
#  output: 9999 (integer)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: 9998 (integer)
#input: "_name:_port"
#  output: "_port" (string)
```

<a id="entry-7-3-1-rfc7239-nn"></a>

**`rfc7239_nn`**

```haproxy
rfc7239_nn
```

提供されたアドレス／文字列入力を RFC7239 互換のノード名に変換します。手動で 'for' または 'by' 7239ヘッダーフィールドを構築する際に使用できます。

入力が文字列の場合、難読化された識別子を表すために自動的に '\_' 文字が前置されます。文字列は RFC7239 文字セットに準拠している必要があります。文字列が空の場合、"unknown" 識別子に変換されます。

例：

```shell
#input: ipv6(ab:cd:ff:ff:ff:ff:ff:ff)
#  output: "[ab:cd:ff:ff:ff:ff:ff:ff]"
#input: str(test)
#  output: "_test"
#input: str()
#  output: "unknown"
```

関連項目： "rfc7239_np"

<a id="entry-7-3-1-rfc7239-np"></a>

**`rfc7239_np`**

```haproxy
rfc7239_np
```

提供された無符号整数／文字列入力を RFC7239 互換のノードポートに変換します。手動で 'for' または 'by' 7239ヘッダーフィールドを構築する際に使用できます。

入力が文字列の場合、難読化された識別子を表すために自動的に '\_' 文字が前置されます。文字列は RFC7239 文字セットに準拠している必要があり、空であってはなりません。

例：

```shell
#input: int(12)
#  output: "12"
#input: str(test)
#  output: "_test"

# build 'for' forwarded header field
http-request set-var-fmt(txn.test) "for=\"%[ipv6(::1),rfc7239_nn]:%[int(8080),rfc7239_np]\";"
#  output: "for=\"[::1]:8080\";"

# build RFC-compliant 7239 header:
http-request set-var-fmt(txn.forwarded) "for=\"%[ipv6(::1),rfc7239_nn]:%[str(8888),rfc7239_np]\";host=\"haproxy.org\";proto=http"
# check RFC-compliancy:
http-request set-var(txn.test) "var(txn.forwarded),debug(test,stderr),rfc7239_is_valid,debug(test,stderr)"
#  stderr output:
#    [debug] test: type=str <for="[::1]:_8888";host="haproxy.org";proto=http>
#    [debug] test: type=bool <1>
```

関連項目： "rfc7239_nn"

<a id="entry-7-3-1-rtrim"></a>

**`rtrim(<chars>)`**

```haproxy
rtrim(<chars>)
```

入力サンプルの文字列表現の末尾から `<chars>` の文字をすべてスキップします。

<a id="entry-7-3-1-sdbm"></a>

**`sdbm([<avalanche>])`**

```haproxy
sdbm([<avalanche>])
```

SDBMハッシュ関数を使用して、バイナリ入力サンプルを無符号32ビット量にハッシュします。省略可能な `<avalanche>` 引数が1の場合、出力に完全なアバランチハッシュ関数を適用できます。このコンバーターは、さまざまなハッシュベースの負荷分散アルゴリズムで使用される関数と同一であるため、正確に同じ結果を提供します。主にデバッグ用途を想定していますが、大まかな統計を収集するためのスティックテーブルエントリーとしても使用できます。セキュリティ目的には使用してはなりません。32ビットハッシュは簡単に破られるためです。関連項目： "crc32", "djb2", "wt6", "crc32c", および "hash-type" ディレクティブ。

<a id="entry-7-3-1-secure-memcmp"></a>

**`secure_memcmp(<var>)`**

```haproxy
secure_memcmp(<var>)
```

`<var>` の内容と入力値を比較します。両方の値はバイナリ文字列として扱われます。両方のバイナリ文字列が一致するかどうかを示す真偽値を返します。

バイナリ文字列の長さが同じである場合、比較は一定の時間で行われます。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

例：

```shell
http-request set-var(txn.token) hdr(token)
# Check whether the token sent by the client matches the secret token
# value, without leaking the contents using a timing attack.
acl token_given str(my_secret_token),secure_memcmp(txn.token)
```

<a id="entry-7-3-1-set-var"></a>

**`set-var(<var>[,<cond>...])`**

```haproxy
set-var(<var>[,<cond>...])
```

指定されたすべての条件が真である場合に限り、入力内容を変数に設定し、出力としてそのまま内容を返します（指定できる条件の一覧は以下を参照）。変数は値と、それに対応する入力の型を保持します。変数の詳細については [2.8節](/ja/haproxy/configuration-basics/#section-2-8) を参照してください。

次の条件の中から、最大4つの条件をコンバーターに渡せます。

- "ifexists"/"ifnotexists":

```text
現在のset-var呼び出しの前から変数が存在していたかを確認します。
通常、変数はset-var呼び出しが成功すると作成されます。
スコープが"proc"の変数は設定解析時に作成されるため、
その変数に対する"ifexists"条件は常にtrueになる点に注意してください。
```

- "ifempty"/"ifnotempty":

```text
入力が空かどうかを確認します。
スカラー型は空になることがないため、入力内容（整数、真偽値、IPなど）に
かかわらず、ifempty条件はfalseになります。
```

- "ifset"/"ifnotset":

```text
変数に以前値が設定されたか、またはその変数に対してunset-varが呼び出されたかを確認します。
まだ存在していない変数は、値が設定されていないものと見なします。
"proc"変数は設定解析時に作成されるため、存在していても
値が設定されていないことがあります。
```

- "ifgt"/"iflt":

```text
変数の内容が入力より"大きい"か"小さい"かを確認します。
この検査を実行できるのは、入力と変数がともに整数型の場合だけです。
それ以外の場合、検査結果はデフォルトでtrueと見なします。
```

<a id="entry-7-3-1-sha1"></a>

**`sha1`**

```haproxy
sha1
```

バイナリ入力サンプルを SHA-1 ダイジェストに変換します。結果は長さ 20 バイトのバイナリサンプルです。

<a id="entry-7-3-1-sha2"></a>

**`sha2([<bits>])`**

```haproxy
sha2([<bits>])
```

バイナリ入力サンプルを SHA-2 シリーズのダイジェストに変換します。結果は長さ `<bits>`/8 バイトのバイナリサンプルです。

`<bits>` の有効な値は 224、256、384、512 であり、それぞれ SHA-`<bits>` に対応します。デフォルト値は 256 です。

このコンバーターは HAProxy が USE_OPENSSL でコンパイルされた場合にのみ利用可能です。

<a id="entry-7-3-1-srv-is-up"></a>

**`srv_is_up`**

```haproxy
srv_is_up
```

文字列型の入力値（サーバー名または `<backend>`/`<server>` 形式）を取得し、指定されたサーバーが現在 UP である場合に true を返します。動的な名前（たとえばCookieの値（req.cook(SRVID),srv_is_up））からサーバー状態を照会し、リクエストを別の場所に転送する判断に使用できます。使用する前に、制御されていないデータに対してこのコンバーターを使用すると、外部の観測者が構成内の任意のサーバーの状態を照会できる可能性があることに注意してください。これは一部の環境では許容されない場合があります。

<a id="entry-7-3-1-srv-queue"></a>

**`srv_queue`**

```haproxy
srv_queue
```

文字列型の入力値（サーバー名または `<backend>`/`<server>` 形式）を取得し、そのサーバーにキューされたストリーム数を返します。動的な名前（たとえばCookieの値（req.cook(SRVID),srv_queue））からキューされたストリームを照会し、接続先の固定を解除するか、リクエストを別の場所に転送する判断に使用できます。使用する前に、制御されていないデータに対してこのコンバーターを使用すると、外部の観測者が構成内の任意のサーバーの状態を照会できる可能性があることに注意してください。これは一部の環境では許容されない場合があります。

<a id="entry-7-3-1-strcmp"></a>

**`strcmp(<var>)`**

```haproxy
strcmp(<var>)
```

`<var>` の内容を文字列型の入力値と比較します。結果は strcmp(3) と互換性のある符号付き整数として返されます。両方の文字列が同一の場合、0 を返します。左の文字列が辞書的に右の文字列より小さい場合、または左の文字列が短い場合、0 より小さい値を返します。それ以外の場合は 0 より大きい値を返します（右の文字列が左の文字列より大きい場合、または右の文字列が短い場合）。

2つのバイナリ文字列を一定の時間で比較する必要がある場合は、secure_memcmpコンバーターも参照してください。

例：

```shell
http-request set-var(txn.host) hdr(host)
# Check whether the client is attempting domain fronting.
acl ssl_sni_http_host_match ssl_fc_sni,strcmp(txn.host) eq 0

```

<a id="entry-7-3-1-sub"></a>

**`sub(<value>)`**

```haproxy
sub(<value>)
```

符号付き整数型の入力値から `<value>` を減算し、結果を符号付き整数として返します。注意：定数から入力値を減算するには、単に "neg,add(value)" を実行してください。`<value>` は数値または変数名です。詳細については [2.8節](/ja/haproxy/configuration-basics/#section-2-8) を参照してください。

<a id="entry-7-3-1-table-bytes-in-rate"></a>

**`table_bytes_in_rate([<table>])`**

```haproxy
table_bytes_in_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値 0 を返します。存在する場合、指定されたテーブル内の入力サンプルに関連するクライアントからサーバーへの平均バイト転送速度を、テーブルで設定した期間のバイト数で返します。sc_bytes_in_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-bytes-out-rate"></a>

**`table_bytes_out_rate([<table>])`**

```haproxy
table_bytes_out_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値 0 を返します。存在する場合、指定されたテーブル内の入力サンプルに関連するサーバーからクライアントへの平均バイト転送速度を、テーブルで設定した期間のバイト数で返します。sc_bytes_out_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-clr-gpc"></a>

**`table_clr_gpc(<idx>[,<table>])`**

```haproxy
table_clr_gpc(<idx>[,<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。gpc配列のインデックス `<idx>` にある汎用カウンターをクリアし、それまでの値を返します。`<idx>` は 0 から 99 の整数です。エントリが存在しない場合、エントリが作成され、0 が返されます。このコンバーターは 'gpc' 配列の data_type にのみ適用されます（従来の 'gpc0' や 'gpc1' の data_type には適用されません）。sc_clr_gpc サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-clr-gpc0"></a>

**`table_clr_gpc0([<table>])`**

```haproxy
table_clr_gpc0([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。最初の汎用カウンター '0' をクリアし、その前の値を返します。エントリが存在しない場合、エントリが作成され、0 が返されます。これは通常、最初のACLを満たした場合に接続へ印を付けるために、式内の第2の ACL として使用されます：

例：

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse src_http_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 5
acl save  src,table_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

sc_clr_gpc0 サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-clr-gpc1"></a>

**`table_clr_gpc1([<table>])`**

```haproxy
table_clr_gpc1([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。最初の汎用カウンター '1' をクリアし、その前の値を返します。エントリが存在しない場合、エントリが作成され、0 が返されます。これは通常、最初のACLを満たした場合に接続へ印を付けるために、式内の第2の ACL として使用されます。sc_clr_gpc1 サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-conn-cnt"></a>

**`table_conn_cnt([<table>])`**

```haproxy
table_conn_cnt([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値 0 を返します。存在する場合、指定されたテーブル内の入力サンプルに関連する着信接続の累積数を返します。sc_conn_cnt サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-conn-cur"></a>

**`table_conn_cur([<table>])`**

```haproxy
table_conn_cur([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値 0 を返します。存在する場合、指定されたテーブル内の入力サンプルに関連する現在追跡している同時接続数を返します。sc_conn_cur サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-conn-rate"></a>

**`table_conn_rate([<table>])`**

```haproxy
table_conn_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値 0 を返します。存在する場合、指定されたテーブル内の入力サンプルに関連する着信接続の平均発生速度を返します。sc_conn_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-expire"></a>

**`table_expire([<table>[,<default_value>]])`**

```haproxy
table_expire([<table>[,<default_value>]])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、コンバーターは失敗しますが、`<default_value>` が設定されている場合は、コンバーターは成功し、`<default_value>` を返します。キーがテーブルに存在する場合、コンバーターは入力されたサンプルに対応するキーの有効期限までの時間を、指定されたテーブルから返します。また、table_idle サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-glitch-cnt"></a>

**`table_glitch_cnt([<table>])`**

```haproxy
table_glitch_cnt([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応するフロント側の接続の異常発生回数の累計値を、指定されたテーブルから返します。sc_glitch_cnt サンプル取得キーワードと、現在のフロント側の接続で測定した値を取得する fc_glitches も参照してください。

<a id="entry-7-3-1-table-glitch-rate"></a>

**`table_glitch_rate([<table>])`**

```haproxy
table_glitch_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応するフロント側の接続の異常発生率の平均値を、指定されたテーブルから返します。また、sc_glitch_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc"></a>

**`table_gpc(<idx>[,<table>])`**

```haproxy
table_gpc(<idx>[,<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する配列のインデックス `<idx>` における汎用カウンターの現在値を、指定された `<table>` から返します。`<idx>` は 0 から 99 の整数です。このインデックスに GPC が格納されていない場合も、整数値0を返します。これは 'gpc' 配列データ型だけに適用します（従来の 'gpc0' や 'gpc1' データ型には適用しません）。また、sc_get_gpc サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc0"></a>

**`table_gpc0([<table>])`**

```haproxy
table_gpc0([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する最初の汎用カウンターの現在値を、指定されたテーブルから返します。また、sc_get_gpc0 サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc0-rate"></a>

**`table_gpc0_rate([<table>])`**

```haproxy
table_gpc0_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したテーブル内で入力サンプルに関連付けられたgpc0カウンターが、テーブルで設定した期間内に増加した頻度を返します。また、sc_get_gpc0_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc1"></a>

**`table_gpc1([<table>])`**

```haproxy
table_gpc1([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する2番目の汎用カウンターの現在値を、指定されたテーブルから返します。また、sc_get_gpc1 サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc1-rate"></a>

**`table_gpc1_rate([<table>])`**

```haproxy
table_gpc1_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したテーブル内で入力サンプルに関連付けられたgpc1カウンターが、テーブルで設定した期間内に増加した頻度を返します。また、sc_get_gpc1_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpc-rate"></a>

**`table_gpc_rate(<idx>[,<table>])`**

```haproxy
table_gpc_rate(<idx>[,<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したスティックテーブル `<table>` 内で入力サンプルに関連付けられた配列の、インデックス `<idx>` にある汎用カウンターが、設定した期間内に増加した頻度を返します。`<idx>` は 0 から 99 の整数です。このインデックスに gpc_rate が格納されていない場合も、整数値0を返します。これは 'gpc_rate' 配列データ型だけに適用します（従来の 'gpc0_rate' や 'gpc1_rate' データ型には適用しません）。また、sc_gpc_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpt"></a>

**`table_gpt(<idx>[,<table>])`**

```haproxy
table_gpt(<idx>[,<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する配列のインデックス `<idx>` における汎用タグの現在値を、指定された `<table>` から返します。`<idx>` は 0 から 99 の整数です。このインデックスに GPT が格納されていない場合も、整数値0を返します。これは 'gpt' 配列データ型だけに適用します（従来の 'gpt0' データ型には適用しません）。また、sc_get_gpt サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-gpt0"></a>

**`table_gpt0([<table>])`**

```haproxy
table_gpt0([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する最初の汎用タグの現在値を、指定されたテーブルから返します。また、sc_get_gpt0 サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-err-cnt"></a>

**`table_http_err_cnt([<table>])`**

```haproxy
table_http_err_cnt([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する HTTP エラーの累計数を、指定されたテーブルから返します。また、sc_http_err_cnt サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-err-rate"></a>

**`table_http_err_rate([<table>])`**

```haproxy
table_http_err_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したテーブル内で入力サンプルに関連付けられたHTTPエラーの平均レートを返します。テーブルで設定した期間内のエラー数で測定します。また、sc_http_err_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-fail-cnt"></a>

**`table_http_fail_cnt([<table>])`**

```haproxy
table_http_fail_cnt([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する HTTP失敗の累計数を、指定されたテーブルから返します。また、sc_http_fail_cnt サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-fail-rate"></a>

**`table_http_fail_rate([<table>])`**

```haproxy
table_http_fail_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したテーブル内で入力サンプルに関連付けられたHTTP失敗の平均レートを返します。テーブルで設定した期間内の失敗数で測定します。また、sc_http_fail_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-req-cnt"></a>

**`table_http_req_cnt([<table>])`**

```haproxy
table_http_req_cnt([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは入力されたサンプルに対応する HTTP リクエストの累計数を、指定されたテーブルから返します。また、sc_http_req_cnt サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-http-req-rate"></a>

**`table_http_req_rate([<table>])`**

```haproxy
table_http_req_rate([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、整数値ゼロが返されます。それ以外の場合、コンバーターは、指定したテーブル内で入力サンプルに関連付けられたHTTPリクエストの平均レートを返します。テーブルで設定した期間内のリクエスト数で測定します。また、sc_http_req_rate サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-idle"></a>

**`table_idle([<table>[,<default_value>]])`**

```haproxy
table_idle([<table>[,<default_value>]])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。キーがテーブルに存在しない場合、コンバーターは失敗しますが、`<default_value>` が設定されている場合は、コンバーターは成功し、`<default_value>` を返します。キーが存在する場合、コンバーターは入力されたサンプルに対応するキーのエントリーが、最後に更新されてからどれだけの時間アイドル状態であったかを、指定されたテーブルから返します。また、table_expire サンプル取得キーワードも参照してください。

<a id="entry-7-3-1-table-inc-gpc"></a>

**`table_inc_gpc(<idx>[,<table>])`**

```haproxy
table_inc_gpc(<idx>[,<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。配列のインデックス `<idx>` における汎用カウンターをインクリメントし、その新しい値を返します。`<idx>` は 0 から 99 の整数です。エントリーが存在しない場合、エントリーが作成され、1 が返されます。このコンバーターは 'gpc' 配列データタイプにのみ適用されます（従来の 'gpc0' や 'gpc1' データタイプには適用されません）。また、sc_inc_gpc も参照してください。

<a id="entry-7-3-1-table-inc-gpc0"></a>

**`table_inc_gpc0([<table>])`**

```haproxy
table_inc_gpc0([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。汎用カウンター '0' をインクリメントし、その新しい値を返します。エントリーが存在しない場合、エントリーが作成され、1 が返されます。sc0/sc2/sc2_inc_gpc0 も参照してください。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます：

例：

```text
acl abuse src,table_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-1-table-inc-gpc1"></a>

**`table_inc_gpc1([<table>])`**

```haproxy
table_inc_gpc1([<table>])
```

入力サンプルを使用して、現在のプロキシのスティックテーブル、または指定したスティックテーブルを検索します。汎用カウンター「1」をインクリメントし、その新しい値を返します。エントリーが見つからない場合、エントリーを作成して1を返します。sc0/sc2/sc2_inc_gpc1も参照してください。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます。

<a id="entry-7-3-1-table-kbytes-in"></a>

**`table_kbytes_in([<table>])`**

```haproxy
table_kbytes_in([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルに関連するクライアントからサーバーへのデータの累計値をキロバイト単位で返します。現在、テストは32ビット整数で行われており、値は4テラバイトまでに制限されています。参照： sc_kbytes_inサンプル取得キーワード。

<a id="entry-7-3-1-table-kbytes-out"></a>

**`table_kbytes_out([<table>])`**

```haproxy
table_kbytes_out([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルに関連するサーバーからクライアントへのデータの累計値をキロバイト単位で返します。現在、テストは32ビット整数で行われており、値は4テラバイトまでに制限されています。参照： sc_kbytes_outサンプル取得キーワード。

<a id="entry-7-3-1-table-server-id"></a>

**`table_server_id([<table>])`**

```haproxy
table_server_id([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルに関連するサーバーIDを返します。サーバーIDは、接続が成功した際に「stick」ルールによってサンプルに関連付けられます。サーバーIDがゼロの場合は、このキーに関連するサーバーが存在しないことを意味します。

<a id="entry-7-3-1-table-sess-cnt"></a>

**`table_sess_cnt([<table>])`**

```haproxy
table_sess_cnt([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルに関連する受信セッションの累計数を返します。ここでセッションとは、「tcp-request connection」ルールセットによって受け入れられた受信接続を指します。参照： sc_sess_cntサンプル取得キーワード。

<a id="entry-7-3-1-table-sess-rate"></a>

**`table_sess_rate([<table>])`**

```haproxy
table_sess_rate([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルに関連する平均受信セッションレートを返します。ここでセッションとは、「tcp-request connection」ルールセットによって受け入れられた受信接続を指します。参照： sc_sess_rateサンプル取得キーワード。

<a id="entry-7-3-1-table-trackers"></a>

**`table_trackers([<table>])`**

```haproxy
table_trackers([<table>])
```

入力されたサンプルを、現在のプロキシのスティックテーブルまたは指定されたスティックテーブルで照合します。キーがテーブルに存在しない場合、整数値ゼロを返します。それ以外の場合、コンバーターは指定されたテーブルにおける入力サンプルと同じキーを追跡している現在の同時接続数を返します。これはtable_conn_curとは異なり、保存された情報に依存せず、テーブルの参照カウント（CLIの"show table"で返される「use」値）に依存します。これは、layer7の追跡に適している場合があります。たとえば、特定のアドレスからの同時接続数をサーバーに通知するのに使用できます。参照： sc_trackersサンプル取得キーワード。

<a id="entry-7-3-1-tcp-dst"></a>

**`tcp.dst`**

```haproxy
tcp.dst
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。このコンバーターはTCPヘッダーに含まれる宛先ポートを表す整数を返します。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-flags"></a>

**`tcp.flags`**

```haproxy
tcp.flags
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。このコンバーターはTCPヘッダー内のTCPフラグを表す整数を返します。FINからCWRまでの8フラグすべてが取得されます。各フラグは「and()」コンバーターでテストできます。各フラグの値についてはRFC9293を参照してください。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-options-mss"></a>

**`tcp.options.mss`**

```haproxy
tcp.options.mss
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「MSS」を検索し、見つかった場合、そのオプションに含まれる通知された値に対応する整数値を返します。見つからない場合、ゼロを返します。MSSは最大セグメントサイズを意味し、ピアが受信できる最大セグメントサイズ（バイト単位）を示します。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-options-sack"></a>

**`tcp.options.sack`**

```haproxy
tcp.options.sack
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「Sack-Permitted」を検索し、見つかった場合、1を返します。見つからない場合、ゼロを返します。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-options-tsopt"></a>

**`tcp.options.tsopt`**

```haproxy
tcp.options.tsopt
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「Timestamp」を検索し、見つかった場合、1を返します。見つからない場合、ゼロを返します。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-options-tsval"></a>

**`tcp.options.tsval`**

```haproxy
tcp.options.tsval
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「Timestamp」を検索し、見つかった場合、ピアが発行したタイムスタンプ値を返します。見つからない場合、何も返しません。タイムスタンプは32ビット符号なし値です。単位は決まっておらず、ピアだけが決定します。また、異なる接続間では互いに独立していることが期待されます。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-options-wscale"></a>

**`tcp.options.wscale`**

```haproxy
tcp.options.wscale
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「Window Scale」を検索し、見つかった場合、ピアが発行したウィンドウスケーリング値を返します。見つからない場合、ゼロを返します。値は14を超えないことが想定されていますが、14を超える値の送信を妨げる技術的な制限はありません。ウィンドウスケールオプションが使用されたかどうかを検出するには、"tcp.options.wsopt"を使用してください。参照： 「tcp-ss」、"fc_saved_syn"、"ip.data"、および"tcp.options.wsopt"。

<a id="entry-7-3-1-tcp-options-wsopt"></a>

**`tcp.options.wsopt`**

```haproxy
tcp.options.wsopt
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPオプションの種類「Window Scale」を検索し、見つかった場合、1を返します。見つからない場合、0を返します。参照： "fc_saved_syn"、「tcp-ss」、"ip.data"、"tcp.options.wscale"。

<a id="entry-7-3-1-tcp-options-list"></a>

**`tcp.options_list`**

```haproxy
tcp.options_list
```

「ip.data」が返すような、バイナリのTCPヘッダーを表す入力サンプルに対して使用します。TCPヘッダーに出現する順序で、すべてのTCPオプション種別からなるバイナリ列を作成します。生成する長さは0～60バイト（最悪の場合）です。End-of-optionsは出力しません。「fc_saved_syn」、「tcp-ss」、「ip.data」も参照してください。

<a id="entry-7-3-1-tcp-seq"></a>

**`tcp.seq`**

```haproxy
tcp.seq
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPヘッダーに使用されたピアのシーケンス番号を表す整数を返します。シーケンス番号は32ビット符号なし値です。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-src"></a>

**`tcp.src`**

```haproxy
tcp.src
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPヘッダーに含まれる送信元ポートを表す整数を返します。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-tcp-win"></a>

**`tcp.win`**

```haproxy
tcp.win
```

入力サンプルが"ip.data"によって返されたバイナリTCPヘッダーを表している場合に使用します。TCPヘッダーでピアが通知したウィンドウサイズを表す整数を返します。値はそのまま16ビット符号なし量として提供され、ウィンドウスケーリング係数は適用されません。参照： "fc_saved_syn"、「tcp-ss」、および"ip.data"。

<a id="entry-7-3-1-ub64dec"></a>

**`ub64dec`**

```haproxy
ub64dec
```

このコンバーターはb64decコンバーターのbase64url版です。base64urlエンコーディングは、URLやファイル名で安全に使える文字セットを使用するbase64エンコーディングの一種です。これはJWT（JSON Web Token）標準で使用されるエンコーディングでもあります。

例：

```shell
# Decoding a JWT payload:
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec
```

<a id="entry-7-3-1-ub64enc"></a>

**`ub64enc`**

```haproxy
ub64enc
```

このコンバーターはbase64コンバーターのbase64url版です。

<a id="entry-7-3-1-ungrpc"></a>

**`ungrpc(<field_number>[,<field_type>])`**

```haproxy
ungrpc(<field_number>[,<field_type>])
```

gRPCメッセージを表す入力バイナリサンプルから、`<field_number>`で指定したフィールド番号（ドット表記）のProtocol Buffersメッセージフィールドを抽出します。`<field_type>`を指定しない場合は生データとして、指定した場合は整数サンプルとして抽出します。使用できる型は、"varint"のワイヤータイプ0では"int32"、"int64"、"uint32"、"uint64"、"sint32"、"sint64"、"bool"、"enum"、64ビットのワイヤータイプ1では"fixed64"、"sfixed64"、"double"、ワイヤータイプ5では"fixed32"、"sfixed32"、"float"です。"string"は長さで区切られる型と見なされるため、抽出に`<field_type>`引数は不要です。Protocol Buffersメッセージのフィールド型の詳細は、次を参照してください：
<https://developers.google.com/protocol-buffers/docs/encoding>

例：

```text
// with such a protocol buffer .proto file content adapted from
// https://github.com/grpc/grpc/blob/master/examples/protos/route_guide.proto

message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}

message PPoint {
  Point point = 59;
}

message Rectangle {
  // One corner of the rectangle.
  PPoint lo = 48;
  // The other corner of the rectangle.
  PPoint hi = 49;
}
```

リクエストボディーが"Rectangle"オブジェクトの値（2つのPPointのProtocol Buffersメッセージ）で構成されているとします。4つのProtocol Buffersフィールドは、次の"ungrpc"ディレクティブで抽出できます：

```text
req.body,ungrpc(48.59.1,int32) # "latitude" of "lo" first PPoint
req.body,ungrpc(48.59.2,int32) # "longitude" of "lo" first PPoint
req.body,ungrpc(49.59.1,int32) # "latitude" of "hi" second PPoint
req.body,ungrpc(49.59.2,int32) # "longitude" of "hi" second PPoint
```

中間の48.59フィールドを、次のようにバイナリサンプルとして抽出することもできます：

```text
req.body,ungrpc(48.59)
```

gRPCメッセージは常にgRPCヘッダーにProtocol Buffersメッセージが続く構造であるため、前の例の最初のPPointである"lo"の"latitude"は、次の同等のディレクティブで抽出できます：

```text
req.body,ungrpc(48.59),protobuf(1,int32)
req.body,ungrpc(48),protobuf(59.1,int32)
req.body,ungrpc(48),protobuf(59),protobuf(1,int32)
```

最初の変換は"ungrpc"、残りの変換は"protobuf"でなければなりません。直前のバイナリサンプルを解釈するための2番目の引数は、最後の変換だけが指定してもしなくてもかまいません。

<a id="entry-7-3-1-unset-var"></a>

**`unset-var(<var>)`**

```haproxy
unset-var(<var>)
```

入力コンテンツが定義されている場合、変数を解除します。変数名はそのスコープを示す接頭辞で始まります。詳細については[セクション2.8](/ja/haproxy/configuration-basics/#section-2-8)を参照してください。

<a id="entry-7-3-1-upper"></a>

**`upper`**

```haproxy
upper
```

文字列サンプルを大文字に変換します。これは文字列サンプル取得関数の後にのみ配置でき、または文字列型を返す変換キーワードの後にのみ配置できます。結果の型は文字列です。

<a id="entry-7-3-1-url-dec"></a>

**`url_dec([<in_form>])`**

```haproxy
url_dec([<in_form>])
```

入力としてURLエンコードされた文字列を受け取り、デコードされたバージョンを出力として返します。入力と出力はともに文字列型です。`<in_form>`引数が非ゼロの整数値に設定されている場合、入力文字列はフォームまたはクエリ文字列の一部とみなされ、'+'文字はスペース(' ')に変換されます。それ以外の場合は、クエリ文字列を示す疑問符の後にのみ変換が行われます('?')。

<a id="entry-7-3-1-url-enc"></a>

**`url_enc([<enc_type>])`**

```haproxy
url_enc([<enc_type>])
```

入力として文字列を受け取り、エンコードされたバージョンを出力として返します。入力と出力はともに文字列型です。デフォルトではエンコーディングのタイプは`query`用に想定されています。現時点では他のタイプはサポートされていませんが、オプション引数は将来の変更のために用意されています。

<a id="entry-7-3-1-us-ltime"></a>

**`us_ltime(<format>[,<offset>])`**

```haproxy
us_ltime(<format>[,<offset>])
```

"ltime"と同様に動作しますが、入力はマイクロ秒単位です。date(1)に由来する%N変換指定子もサポートしています。エポックからの日時を表すと想定した整数を、`<format>`文字列で定義されたフォーマットに従ってstrftime(3)を使用してローカル時間の文字列に変換します。目的は、ログで任意の日付フォーマットを使用できるようにすることです。入力日付にオプションの`<offset>`（マイクロ秒単位）を適用できます（正または負）。使用しているオペレーティングシステムがサポートする形式は、strftime()のマニュアルページを参照してください。

%N変換指定子を使用すると、日付のナノ秒部分を出力できます。入力がマイクロ秒単位であるため、精度は制限されています（000000000..999999000）。%Nは%とNの間に幅引数を取ることができます。ミリ秒（%3N）やマイクロ秒（%6N）を表示するのに有用です。デフォルトおよび最大幅は9です（%N = %9N）。

UTC用の"utime"コンバーター、および"ltime"と"ms_ltime"コンバーターも参照してください。

例：

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_ltime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-us-utime"></a>

**`us_utime(<format>[,<offset>])`**

```haproxy
us_utime(<format>[,<offset>])
```

"utime"と同様に動作しますが、入力はマイクロ秒単位です。date(1)に由来する%N変換指定子もサポートしています。エポックからの日時を表すと想定した整数を、`<format>`文字列で定義されたフォーマットに従ってstrftime(3)を使用してUTC時間の文字列に変換します。目的は、ログで任意の日付フォーマットを使用できるようにすることです。入力日付にオプションの`<offset>`（マイクロ秒単位）を適用できます（正または負）。使用しているオペレーティングシステムがサポートする形式は、strftime()のマニュアルページを参照してください。

%N変換指定子を使用すると、日付のナノ秒部分を出力できます。入力がマイクロ秒単位であるため、精度は制限されています（000000000..999999000）。%Nは%とNの間に幅引数を取ることができます。ミリ秒（%3N）やマイクロ秒（%6N）を表示するのに有用です。デフォルトおよび最大幅は9です（%N = %9N）。

ローカル時刻用の"ltime"コンバーター、および"utime"と"ms_utime"コンバーターも参照してください。

例：

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_utime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-utime"></a>

**`utime(<format>[,<offset>])`**

```haproxy
utime(<format>[,<offset>])
```

エポックからの日時を表すと想定した整数を、`<format>`文字列で定義されたフォーマットに従ってstrftime(3)を使用してUTC時間の文字列に変換します。目的は、ログで任意の日付フォーマットを使用できるようにすることです。入力日付にオプションの`<offset>`（秒単位）を適用できます（正または負）。使用しているオペレーティングシステムがサポートする形式は、strftime()のマニュアルページを参照してください。また"ltime"コンバーターおよび"ms_utime"、"us_utime"についても参照してください。

例：

```shell
# Emit two colons, one with the UTC time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,utime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-when"></a>

**`when(<condition>[,<args>...])`**

```haproxy
when(<condition>[,<args>...])
```

条件を評価し、真の場合は入力サンプルをそのまま出力に渡し、それ以外の場合は何も返しません。エラー発生時のデバッグ情報など、まれにしか必要にならず、特定の条件下でのみ出力すべき情報を扱うために設計されています。

条件は以下のリストのキーワードからなります。任意で感嘆符（'!'）を前に付けて否定でき、条件固有の引数を後ろに付けることもできます：

    - "error"は、リクエストまたはストリームの処理中にエラーが発生した場合に真を返します。"dontlog-normal"と同じルールを使用します（たとえば、再ディスパッチが成功した場合もエラーとみなされます）。

    - "forwarded"は、リクエストがバックエンドサーバーに転送された場合に真を返します。

    - "normal"は、エラーが発生しなかった場合に真を返します（"!error"と同等です）。

    - "processed"は、リクエストがバックエンドサーバーに転送された場合、またはアプレットによって処理された場合に真を返します。

    - "stopping"は、ルールを評価した時点でプロセスが停止中の場合に真を返します。

    - "toapplet"は、リクエストがアプレットによって処理された場合に真を返します。

    - "acl"は、次の引数で指定したACLの評価結果が真の場合に真を返します。ACLはコンバーター内でインライン評価されるため、参照する内容はそのコンテキストで有効でなければなりません。たとえば、合計転送時間が長すぎるかどうかを評価してから、異常に長い転送の詳細をログに記録するかどうかを決める用途があります。

内容はどの場合でも評価されるため、この方法でその情報の生成を回避することはできません。あくまで、その情報を出力しないためのものです。

たとえば、処理中にエラーが発生した場合にだけバックエンドストリームのデバッグ情報をログに追加する、停止時に追加情報をログに記録するといった用途があります。

例：

```shell
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on error:
log-format "$HAPROXY_HTTP_LOG_FMT dbg={%[bs.debug_str,when(!normal)]}"

ここでは、ルールが成立しない場合、ログの "dbg" フィールドには、内容がないことを示すダッシュ ('-') だけが入ります。ルールが成立する場合は、デバッグ情報のブロック全体を出力します。
```

例

```haproxy
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on slow transfers
acl slow_xfer res.timer.data ge 10000   # more than 10s is slow
log-format "$HAPROXY_HTTP_LOG_FMT                                         \
            fsdbg={%[fs.debug_str,when(acl,slow_xfer)]}                   \
            bsdbg={%[bs.debug_str,when(acl,slow_xfer)]}"
```


例

```haproxy
# only emit the backend src/port when a real connection was issued:
log-format "$HAPROXY_HTTP_LOG_FMT \
           src=[%[bc_src,when(forwarded)]:%[bc_src_port,when(forwarded)]]"
```


条件が真でない場合は式の評価を打ち切るため、後続のコンバーターが呼び出されないようにすることもできます。たとえば、エラー発生時にだけdebug()コンバーターを呼び出し、どうしても必要な場合にだけ要素をログに記録できます。

例：

```shell
# emit the whole response headers list to stderr only on error and only
# when the output is a connection. We abuse a dummy variable here.
http-after-response set-var(res.test) \
              res.hdrs,when(error),when(forwarded),debug(hdrs,stderr)
```

debugコンバーターも参照してください。

<a id="entry-7-3-1-word"></a>

**`word(<index>,<delimiters>[,<count>])`**

```haproxy
word(<index>,<delimiters>[,<count>])
```

入力文字列から指定された区切り文字を用いて、先頭（正のインデックス）または末尾（負のインデックス）から数えたn番目の単語を抽出します。インデックスは1または-1から始まり、区切り文字は、文字のリストを文字列にしたものです。空の単語はスキップされます。つまり、入力文字列の先頭または末尾にある区切り文字は無視され、入力文字列内に連続する区切り文字は1つの区切り文字として扱われます。オプションで抽出する単語数を`<count>`で指定できます（デフォルト：1）。値0は残りのすべての単語を抽出することを示します。

例：

```text
str(f1_f2_f3__f5),word(4,_)    # f5
str(f1_f2_f3__f5),word(5,_)    # <not found>
str(f1_f2_f3__f5),word(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),word(3,_,2)  # f3__f5
str(f1_f2_f3__f5),word(-2,_,3) # f1_f2_f3
str(f1_f2_f3__f5),word(-3,_,0) # f1_f2
str(/f1/f2/f3/f4),word(1,/)    # f1
str(/f1////f2/f3/f4),word(1,/) # f2
```

<a id="entry-7-3-1-wt6"></a>

**`wt6([<avalanche>])`**

```haproxy
wt6([<avalanche>])
```

WT6ハッシュ関数を使用して、バイナリ入力サンプルを符号なし32ビット量にハッシュします。オプションで、`<avalanche>`引数が1に等しい場合に、出力に完全なアバランチハッシュ関数を適用できます。このコンバーターは、さまざまなハッシュベースの負荷分散アルゴリズムで使用される関数と同一であるため、正確に同じ結果を提供します。主にデバッグ用途に使用されますが、スティックテーブルエントリーとして粗い統計情報を収集する用途にも使用できます。32ビットハッシュは簡単に破られるため、セキュリティ目的には使用してはなりません。参照： "crc32", "djb2", "sdbm", "crc32c",および"hash-type"ディレクティブ。

<a id="entry-7-3-1-x509-v-err-str"></a>

**`x509_v_err_str`**

```haproxy
x509_v_err_str
```

数値を対応するX509_V_ERR定数名に変換します。OpenSSLの複数バージョンに対応した設定をACLで作成する際に有用です。バージョンを変更すると一部のコードが変わる可能性があるためです。

対応する定数名が見つからない場合、数値を文字列として出力します。

OpenSSLが提供する定数の一覧は<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES>にあります。OpenSSLの正しいバージョンのページを確認してください。

例：

```text
bind :443 ssl crt common.pem ca-file ca-auth.crt verify optional crt-ignore-err X509_V_ERR_CERT_REVOKED,X509_V_ERR_CERT_HAS_EXPIRED

acl cert_expired ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_HAS_EXPIRED
acl cert_revoked ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_REVOKED
acl cert_ok      ssl_c_verify,x509_v_err_str -m str X509_V_OK

http-response add-header X-SSL Ok if cert_ok
http-response add-header X-SSL Expired if cert_expired
http-response add-header X-SSL Revoked if cert_revoked

http-response add-header X-SSL-verify %[ssl_c_verify,x509_v_err_str]
```

<a id="entry-7-3-1-xor"></a>

**`xor(<value>)`**

```haproxy
xor(<value>)
```

`<value>`と入力値（符号付き整数型）の間でビット単位の「XOR」（排他的論理和）を実行し、結果を符号付き整数として返します。`<value>`は数値または変数名として指定できます。詳細については[セクション2.8](/ja/haproxy/configuration-basics/#section-2-8)の変数に関する記述を参照してください。

<a id="entry-7-3-1-xxh3"></a>

**`xxh3([<seed>])`**

```haproxy
xxh3([<seed>])
```

XXH3 64ビットバージョンのXXhashハッシュ関数を使用して、バイナリ入力サンプルを符号付き64ビット量にハッシュします。このハッシュはシードをサポートしており、デフォルトは0ですが、`<seed>`引数で異なる値を指定できます。このハッシュは非常に優れており高速であるため、URLおよび/またはURLパラメータをスティックテーブルのキーとしてハッシュして、低衝突率で統計情報を収集する用途に使用できますが、アルゴリズムが暗号的に安全とは見なされていないため注意が必要です。

<a id="entry-7-3-1-xxh32"></a>

**`xxh32([<seed>])`**

```haproxy
xxh32([<seed>])
```

XXHashハッシュ関数の32ビットバージョンを使用して、バイナリ入力サンプルを符号なし32ビット量にハッシュします。このハッシュはシードをサポートしており、デフォルトは0ですが、`<seed>`引数で異なる値を指定できます。このハッシュは非常に優れており高速であるため、URLおよび/またはURLパラメータをスティックテーブルのキーとしてハッシュして、低衝突率で統計情報を収集する用途に使用できますが、アルゴリズムが暗号的に安全とは見なされていないため注意が必要です。

<a id="entry-7-3-1-xxh64"></a>

**`xxh64([<seed>])`**

```haproxy
xxh64([<seed>])
```

XXHashハッシュ関数の64ビットバージョンを使用して、バイナリ入力サンプルを符号付き64ビット量にハッシュします。このハッシュはシードをサポートしており、デフォルトは0ですが、`<seed>`引数で異なる値を指定できます。このハッシュは非常に優れており高速であるため、URLおよび/またはURLパラメータをスティックテーブルのキーとしてハッシュして、低衝突率で統計情報を収集する用途に使用できますが、アルゴリズムが暗号的に安全とは見なされていないため注意が必要です。

### 7.3.2. 内部状態からのサンプル取得 {#section-7-3-2}

最初のサンプル取得メソッド群は、クライアント情報とはまったく関係のない内部情報に適用されます。これらは、外部監視者に内部ステータスを報告するために"monitor fail"ディレクティブと併用されることがあります。このセクションで説明するサンプル取得メソッドは、どこでも使用可能です。

このセクションのサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                       出力型
-------------------------------------------------+-------------
acl([!]<name>[,...])                               boolean
act_conn                                           integer
always_false                                       boolean
always_true                                        boolean
avg_queue([<backend>])                             integer
be_conn([<backend>])                               integer
be_conn_free([<backend>])                          integer
be_sess_rate([<backend>])                          integer
bin(<hex>)                                         bin
bool(<bool>)                                       bool
connslots([<backend>])                             integer
cpu_calls                                          integer
cpu_ns_avg                                         integer
cpu_ns_tot                                         integer
date([<offset>[,<unit>]])                          integer
date_us                                            integer
env(<name>)                                        string
fe_conn([<frontend>])                              integer
fe_req_rate([<frontend>])                          integer
fe_sess_rate([<frontend>])                         integer
hostname                                           string
int(<integer>)                                     signed
ipv4(<ipv4>)                                       ipv4
ipv6(<ipv6>)                                       ipv6
last_entity                                        string
last_rule_file                                     string
last_rule_line                                     integer
lat_ns_avg                                         integer
lat_ns_tot                                         integer
meth(<method>)                                     method
nbsrv([<backend>])                                 integer
pid                                                integer
prio_class                                         integer
prio_offset                                        integer
proc                                               integer
queue([<backend>])                                 integer
quic_enabled                                       boolean
rand([<range>])                                    integer
srv_conn([<backend>/]<server>)                     integer
srv_conn_free([<backend>/]<server>)                integer
srv_is_up([<backend>/]<server>)                    boolean
srv_iweight([<backend>/]<server>)                  integer
srv_queue([<backend>/]<server>)                    integer
srv_sess_rate([<backend>/]<server>)                integer
srv_uweight([<backend>/]<server>)                  integer
srv_weight([<backend>/]<server>)                   integer
stopping                                           boolean
str(<string>)                                      string
table_avl([<table>])                               integer
table_cnt([<table>])                               integer
term_events                                        string
thread                                             integer
txn.id32                                           integer
txn.sess_term_state                                string
uptime                                             integer
uuid([<version>])                                  string
var(<var-name>[,<default>])                        undefined
wait_end                                           boolean
waiting_entity                                     string
-------------------------------------------------+-------------
```

詳細一覧：

<a id="entry-7-3-2-acl-boolean"></a>

**`acl([!]<name>[,...]): boolean`**

```haproxy
acl([!]<name>[,...]): boolean
```

指定されたACLの評価がすべて真の場合に真を返し、それ以外の場合は偽を返します。最大12個のACLを指定でき、それぞれをコンマで区切ります。各名前付きACLは"!"で前置することで結果を反転できます。評価のいずれかでエラーが発生した場合、サンプルもエラーを返します。HAProxyは参照されたACLに対して、たとえばHTTPリクエストサンプルを使用するACLがレスポンスコンテキストで使用されているかどうかなどの検証チェックを行いません。この動作は将来変更される可能性があります。

act_conn: integer プロセス上のアクティブな同時接続の総数を返します。

always_false: boolean 常にブール値"false"を返します。設定調整中に別のACLの一時的な置き換えとしてACLと併用できます。

always_true: boolean 常にブール値"true"を返します。設定調整中に別のACLの一時的な置き換えとしてACLと併用できます。

<a id="entry-7-3-2-avg-queue-integer"></a>

**`avg_queue([<backend>]): integer`**

```haproxy
avg_queue([<backend>]): integer
```

指定されたバックエンドのキュー済み接続数を、アクティブなサーバー数で割った値を返します。バックエンドが指定されない場合は現在のバックエンドが使用されます。これは"queue"と似ていますが、ファームのサイズを考慮することで、新しい接続が処理されるまでの時間をより正確に測定できます。主な用途は、ACLと併用して、新規ユーザーに提供するサービスの品質が低下することが確実になった場合にお詫びページを返すことです。また、この値をヘッダーでバックエンドサーバーに渡し、機能を制限したモードで動作するか、一部の機能を無効にして処理を少し高速化するかをサーバー自身が決められるようにする用途もあります。すべてのアクティブなサーバーが停止した場合、キュー済み接続数の2倍を測定値として扱います。これは妥当な推定であり、いずれかのサーバーがすぐに復帰すると予想されるためですが、別のバックエンドがより良好な状態であれば、新規トラフィックをそちらに送信することを優先します。参照： "queue", "be_conn", "be_sess_rate"サンプル取得。

<a id="entry-7-3-2-be-conn-integer"></a>

**`be_conn([<backend>]): integer`**

```haproxy
be_conn([<backend>]): integer
```

バックエンド上の現在確立された接続数に適用され、評価中の接続を含む可能性があります。バックエンド名が指定されない場合は現在のバックエンドが使用されます。別のバックエンドを確認することも可能です。通常のファームが満杯の場合に、特定のファームを使用する用途に使用できます。参照： "fe_conn", "queue", "be_conn_free", "be_sess_rate"指定子。

<a id="entry-7-3-2-be-conn-free-integer"></a>

**`be_conn_free([<backend>]): integer`**

```haproxy
be_conn_free([<backend>]): integer
```

バックエンド内の利用可能なサーバー上の利用可能な接続数に相当する整数値を返します。キューのスロットは含まれません。バックアップサーバーも含まれませんが、他のすべてのサーバーが停止している場合を除きます。バックエンド名が指定されない場合は現在のバックエンドが使用されます。別のバックエンドを確認することも可能です。通常のファームが満杯の場合に、特定のファームを使用する用途に使用できます。参照： "be_conn", "connslots", "srv_conn_free"指定子。

その他の注意点と備考：いずれかのサーバーのmaxconnまたはmaxqueueが0（無制限）の場合、この取得は明らかに意味をなさないため、返される値は-1になります。

<a id="entry-7-3-2-be-sess-rate-integer"></a>

**`be_sess_rate([<backend>]): integer`**

```haproxy
be_sess_rate([<backend>]): integer
```

バックエンドでのセッション生成レートを、1秒あたりの新規セッション数を表す整数値として返します。処理負荷が高い、または障害に弱いバックエンドのセッションレートが高くなりすぎた場合に、ACLと併用して別のバックエンドへ切り替えたり、サービスの乱用を制限したりするために使用します（たとえば、オンライン辞書の内容を丸ごと取得されることを防ぎます）。log-formatディレクティブでこの値をログに追加する用途にも役立ちます。

例：

```shell
# Redirect to an error page if the dictionary is requested too often
backend dynamic
    mode http
    acl being_scanned be_sess_rate gt 100
    redirect location /denied.html if being_scanned
```

<a id="entry-7-3-2-bin-bin"></a>

**`bin(<hex>): bin`**

```haproxy
bin(<hex>): bin
```

バイナリ列を返します。入力には、文字列の16進表現を指定します。

<a id="entry-7-3-2-bool-bool"></a>

**`bool(<bool>): bool`**

```haproxy
bool(<bool>): bool
```

真偽値を返します。`<bool>`には'true'、'false'、'1'、'0'を指定できます。'false'と'0'は同じ値です。'true'と'1'も同じ値です。

<a id="entry-7-3-2-connslots-integer"></a>

**`connslots([<backend>]): integer`**

```haproxy
connslots([<backend>]): integer
```

すべてのサーバーの最大接続数と最大キューサイズを合計し、バックエンドでまだ利用可能な接続スロット数に対応する整数値を返します。おそらくACLとの併用に限られます。

基本的な考え方は、まだ利用可能な接続「スロット」数（接続＋キュー）を測定できるようにし、それを超える接続を別のバックエンドへリダイレクトできるようにすることです（想定用途については"use_backend"キーワードを参照してください）。

'connslots'＝利用可能なサーバー接続スロット数＋利用可能なサーバーキュースロット数。

"fe_conn"も使用できますが、単一のIPアドレスに届いたトラフィックを複数のバックエンドへ振り分ける場合（たとえば、ACLで名前に基づく負荷分散を行う場合）に、各バックエンドと、その利用可能な"connslots"を区別したいときは、"connslots"が特に役立ちます。また、"nbsrv"が実際に*停止中*のサーバーだけを測定するのに対して、この取得はより細かく、利用可能な接続スロット数も調べます。"queue"と"avg_queue"も参照してください。

その他の注意点と備考： 現時点のコードは動的な接続を考慮しません。また、いずれかのサーバーのmaxconnまたはmaxqueueが0の場合、この取得は明らかに意味をなさないため、-1を返します。

cpu_calls: integer ストリームまたは現在のリクエストを処理するタスクが、割り当てられてから呼び出された回数を返します。HTTP keep-aliveの場合、同じ接続の新しいリクエストごとにこの値をリセットします。通常、この値は小さく安定しているはずです（典型的な単純なリクエストでは約2回）が、処理（圧縮、キャッシュ、解析）によっては大きくなることがあります。純粋にパフォーマンス監視を目的とした値です。

cpu_ns_avg: integer ストリームまたは現在のリクエストを処理するタスクの、1回の呼び出しに費やした平均ナノ秒数を返します。HTTP keep-aliveの場合、同じ接続の新しいリクエストごとにこの値をリセットします。この値は、各呼び出しでリクエストまたは接続を処理する全体的なコストを示します。値に良い悪いはありませんが、呼び出しに費やす時間は必然的に他の処理に遅延を生じさせ（後述のlat_ns_avgを参照）、他の接続の見かけの応答時間に影響することがあります。圧縮、複雑な正規表現の照合、負荷の高いLua処理などがこの値に直接影響する場合があり、ログに記録しておくと、適切なパフォーマンスを取り戻すために修正すべき問題のある処理を見つけやすくなります。注： この値はcpu_ns_totをcpu_callsで割った値そのものです。

cpu_ns_tot: integer ストリームまたは現在のリクエストを処理するタスクの各呼び出しに費やした合計ナノ秒数を返します。HTTP keep-aliveの場合、同じ接続の新しいリクエストごとにこの値をリセットします。この値は、各呼び出しでリクエストまたは接続を処理する全体的なコストを示します。値に良い悪いはありませんが、呼び出しに費やす時間は必然的に他の処理に遅延を生じさせ（後述のlat_ns_avgを参照）、マシン上のCPUコストを生じさせ、他の接続の見かけの応答時間に影響することがあります。圧縮、複雑な正規表現の照合、負荷の高いLua処理などがこの値に直接影響する場合があり、ログに記録しておくと、適切なパフォーマンスを取り戻すために修正すべき問題のある処理を見つけやすくなります。たとえば、多数のHTTPチャンクを処理してcpu_callsが大きくなると、この値が見かけ上大きくなる場合があります。そのため、代わりにcpu_ns_avgをログに記録することがよくあります。

cpu_usage_grp: integer 最後のポーリングループで測定したCPU使用率を、現在のスレッドグループの全スレッドの平均として、0～100の値で返します。トラブルシューティングやログ記録に使用できます。この測定値は変動が非常に激しいものの、各スレッドが数十～数百のリクエストにわたって測定するため、持続的な負荷に対しては正確さを保ちます。

cpu_usage_proc: integer 最後のポーリングループで測定したCPU使用率を、実行中の全スレッドの平均として、0～100の値で返します。トラブルシューティングやログ記録に使用できます。この測定値は変動が非常に激しいものの、各スレッドが数十～数百のリクエストにわたって測定するため、持続的な負荷に対しては正確さを保ちます。統計ページおよび"show info"で報告されるアイドル率を100から引いた値です。

cpu_usage_thr: integer 最後のポーリングループで測定したCPU使用率を、呼び出し元スレッドについて、0～100の値で返します。トラブルシューティングやログ記録に使用できます。この測定値は変動が非常に激しいものの、数十～数百のリクエストにわたって測定するため、持続的な負荷に対しては正確さを保ちます。グリッチ数が多すぎる場合の接続強制切断を有効にするか、圧縮を無効にするかの判断に使う値と同じです。"tune.glitches.kill.cpu-usage"と"maxcompcpuusage"も参照してください。

<a id="entry-7-3-2-date-integer"></a>

**`date([<offset>[,<unit>]]): integer`**

```haproxy
date([<offset>[,<unit>]]): integer
```

現在の日時をエポック（01/01/1970からの秒数）として返します。

オフセット値を指定した場合、現在の日時に加算してから値を返します。正負どちらのオフセットも使用できるため、相対的な日時の計算に特に役立ちます。http_dateコンバーターとの併用に適しています。

`<unit>`は任意です。秒を表す"s"（デフォルトの動作）、ミリ秒を表す"ms"、マイクロ秒を表す"us"を指定できます。単位を指定した場合、エポックからの秒数、ミリ秒数、マイクロ秒数のいずれかに、オフセットを加えた整数値を返します。1秒未満の時間分解能が必要な場合に役立ちます。

例：

```shell
# set an expires header to now+1 hour in every response
http-response set-header Expires %[date(3600),http_date]

# set an expires header to now+1 hour in every response, with
# millisecond granularity
http-response set-header Expires %[date(3600000,ms),http_date(0,ms)]
```

date_us: integer 日時のマイクロ秒部分を返します（「秒」の部分はdateサンプルが返します）。同じtimeval構造体から取得するため、このサンプルはdateサンプルと整合しています。

<a id="entry-7-3-2-env-string"></a>

**`env(<name>): string`**

```haproxy
env(<name>): string
```

環境変数`<name>`の値を含む文字列を返します。環境変数はプロセスごとに存在し、プロセスの起動時に取得される点に注意してください。情報を次のホップのサーバーへ渡したり、ACLと併用して、特定の方法でプロセスを起動した場合に特定の動作を行ったりする用途に役立ちます。

例：

```shell
# Pass the Via header to next hop with the local hostname in it
http-request add-header Via 1.1\ %[env(HOSTNAME)]

# reject cookie-less requests when the STOP environment variable is set
http-request deny if !{ req.cook(SESSIONID) -m found } { env(STOP) -m found }
```

<a id="entry-7-3-2-fe-conn-integer"></a>

**`fe_conn([<frontend>]): integer`**

```haproxy
fe_conn([<frontend>]): integer
```

フロントエンドで現在確立されている接続数を返します。評価中の接続を含む場合もあります。フロントエンド名を指定しない場合は現在のフロントエンドを使用します。別のフロントエンドを調べることもできます。完全に遮断する前にお詫びページを返したり、サーバー群が満杯と判断された場合に特定のバックエンドを使用して新しいリクエストをそちらへ流したりできます。主にACLと併用しますが、HTTPヘッダーで統計情報をサーバーへ渡す用途にも使用できます。"dst_conn"、"be_conn"、"fe_sess_rate"取得も参照してください。

<a id="entry-7-3-2-fe-req-rate-integer"></a>

**`fe_req_rate([<frontend>]): integer`**

```haproxy
fe_req_rate([<frontend>]): integer
```

フロントエンドに送られる1秒あたりのHTTPリクエスト数に対応する整数値を返します。クライアント側のkeep-aliveが有効な場合、この数は"fe_sess_rate"と異なることがあります。

<a id="entry-7-3-2-fe-sess-rate-integer"></a>

**`fe_sess_rate([<frontend>]): integer`**

```haproxy
fe_sess_rate([<frontend>]): integer
```

フロントエンドでのセッション生成レートを、1秒あたりの新規セッション数を表す整数値として返します。サービスの乱用をできるだけ早期に防ぐため、ACLと併用して、受信セッションレートを許容範囲に制限します。たとえば、他のレイヤー4のACLと組み合わせて、レートが制限値を下回るまでクライアントを少し待たせることができます。log-formatディレクティブでこの値をログに追加する用途にも役立ちます。フロントエンドで使用する"rate-limit sessions"ディレクティブも参照してください。

例：

```shell
# This frontend limits incoming mails to 10/s with a max of 100
# concurrent connections. We accept any connection below 10/s, and
# force excess clients to wait for 100 ms. Since clients are limited to
# 100 max, there cannot be more than 10 incoming mails per second.
frontend mail
    bind :25
    mode tcp
    maxconn 100
    acl too_fast fe_sess_rate ge 10
    tcp-request inspect-delay 100ms
    tcp-request content accept if ! too_fast
    tcp-request content accept if WAIT_END
```

hostname: string システムのホスト名を返します。

<a id="entry-7-3-2-int-signed-integer"></a>

**`int(<integer>): signed integer`**

```haproxy
int(<integer>): signed integer
```

符号付き整数を返します。

<a id="entry-7-3-2-ipv4-ipv4"></a>

**`ipv4(<ipv4>): ipv4`**

```haproxy
ipv4(<ipv4>): ipv4
```

ipv4値を返します。

<a id="entry-7-3-2-ipv6-ipv6"></a>

**`ipv6(<ipv6>): ipv6`**

```haproxy
ipv6(<ipv6>): ipv6
```

ipv6値を返します。

last_entity: string ストリーム解析中に最後に評価されたエンティティーの識別情報を返します。最後に一致した終端ルール、または処理を中断したフィルターである場合があります。

終端ルールとは、ルールセットの評価を終了させるルールです（"accept"、"deny"、"redirect"など）。"content"ルールセットに作用するTCPリクエストおよびレスポンスルールと、"http-request"、"http-response"、"http-after-response"ルールセットのHTTPルールで動作します。従来の"redirect"ルールセットはサポートしません（この情報を保存していないためです）。また、この情報はストリームレベルで保存され、"tcp-request connection"や"tcp-request session"のルールの実行中にはストリームが存在しないため、これらのルールセットもサポートしません。この場合、返される値は"last_rule_file:last_rule_line"と同等です。"last_rule_file"と"last_rule_line"も参照してください。

フィルターの場合は、開発者が定義した識別子を返します。その識別子を定義していなければ、一意の内部識別子に対応する16進数の値を返します。

この関数の主な目的は、処理を中断した最後のエンティティーをログに記録できるようにし、問題のデバッグに役立てることです。エンティティーについて返される情報は時間とともに変わる可能性があるため、デバッグ以外の用途に使用してはなりません。

例：

```shell
# Log the last entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[last_entity,when(error)]
```

last_rule_file: string ストリーム解析中に最後に一致した終端ルールを含む設定ファイル名を返します。終端ルールとは、ルールセットの評価を終了させるルールです（"accept"、"deny"、"redirect"など）。"content"ルールセットに作用するTCPリクエストおよびレスポンスルールと、"http-request"、"http-response"、"http-after-response"ルールセットのHTTPルールで動作します。従来の"redirect"ルールセットはサポートしません（この情報を保存していないためです）。また、この情報はストリームレベルで保存され、"tcp-request connection"や"tcp-request session"のルールの実行中にはストリームが存在しないため、これらのルールセットもサポートしません。主な目的は、最終判断を下したルールの場所をログに記録できるようにし、たとえばリクエストが拒否された理由を調べやすくすることです。"last_rule_line"も参照してください。

last_rule_line: integer ストリーム解析中に最後に一致した終端ルールが、設定ファイル内で何行目にあるかを返します。終端ルールとは、ルールセットの評価を終了させるルールです（"accept"、"deny"、"redirect"など）。"content"ルールセットに作用するTCPリクエストおよびレスポンスルールと、"http-request"、"http-response"、"http-after-response"ルールセットのHTTPルールで動作します。従来の"redirect"ルールセットはサポートしません（この情報を保存していないためです）。また、この情報はストリームレベルで保存され、"tcp-request connection"や"tcp-request session"のルールの実行中にはストリームが存在しないため、これらのルールセットもサポートしません。主な目的は、最終判断を下したルールの場所をログに記録できるようにし、たとえばリクエストが拒否された理由を調べやすくすることです。"last_rule_file"も参照してください。

lat_ns_avg: integer ストリームを処理するタスクが起こされてから、実際に呼び出されるまでに費やした平均ナノ秒数を返します。HTTP keep-aliveの場合、同じ接続の新しいリクエストごとにこの値をリセットします。この値は、並行して処理する他のすべてのリクエストによって、現在のリクエストに生じる全体的な遅延を示し、負荷の高い他の処理による体感性能の低下を直接示す指標です。この値を低く保つには、"tune.runqueue-depth"でスケジューラーの実行キューの深さを減らす、"tune.maxpollevents"で一度に処理する同時イベント数を減らす、"bind"行またはフロントエンドの"nice"オプションでストリームのnice値を下げる、"tune.sched.low-latency"で低遅延スケジューリングを有効にする、ログから処理の調整や修正が必要な他の重いリクエスト（"cpu_ns_avg"が大きいもの）を探すといった方法があります。大きいバッファーの圧縮、負荷の高い正規表現、長い正規表現リストが原因になる場合があります。注： この値はlat_ns_totをcpu_callsで割った値そのものです。

lat_ns_tot: integer ストリームを処理するタスクが起こされてから、実際に呼び出されるまでに費やした合計ナノ秒数を返します。HTTP keep-aliveの場合、同じ接続の新しいリクエストごとにこの値をリセットします。この値は、並行して処理する他のすべてのリクエストによって、現在のリクエストに生じる全体的な遅延を示し、負荷の高い他の処理による体感性能の低下を直接示す指標です。この値を低く保つには、"tune.runqueue-depth"でスケジューラーの実行キューの深さを減らす、"tune.maxpollevents"で一度に処理する同時イベント数を減らす、"bind"行またはフロントエンドの"nice"オプションでストリームのnice値を下げる、"tune.sched.low-latency"で低遅延スケジューリングを有効にする、ログから処理の調整や修正が必要な他の重いリクエスト（"cpu_ns_avg"が大きいもの）を探すといった方法があります。大きいバッファーの圧縮、負荷の高い正規表現、長い正規表現リストが原因になる場合があります。注： 合計遅延が転送時間に加わるように直感的には思えますが、ほぼ常にそうではありません。タスクがCPUを待っている間もネットワークバッファーは満たされ続け、次の呼び出しで一度により多く処理するためです。たとえば、多数のHTTPチャンクを処理してcpu_callsが大きくなると、この値が見かけ上大きくなる場合があります。そのため、より適切なパフォーマンス指標であるlat_ns_avgを代わりにログに記録することがよくあります。

<a id="entry-7-3-2-meth-method"></a>

**`meth(<method>): method`**

```haproxy
meth(<method>): method
```

メソッドを返します。

<a id="entry-7-3-2-nbsrv-integer"></a>

**`nbsrv([<backend>]): integer`**

```haproxy
nbsrv([<backend>]): integer
```

現在のバックエンド、または指定したバックエンドで、使用可能なサーバーの数を整数で返します。主にACLで使用しますが、ログに追加しても役立ちます。通常は、ある負荷を処理するにはサーバー数が少なすぎる場合に、別のバックエンドへ切り替えるために使用します。"monitor fail" と組み合わせると、障害の報告に役立ちます。

pid: integer 現在のプロセスのPIDを返します。ほとんどの場合、ワーカープロセスのPIDです。

prio_class: integer HTTPモードでは現在のストリーム、TCPモードでは現在の接続の、優先度クラスを返します。値は、"http-request set-priority-class" または "tcp-request content set-priority-class" の、最後の呼び出しで設定したものです。

prio_offset: integer HTTPモードでは現在のストリーム、TCPモードでは現在の接続の、優先度オフセットを返します。値は、"http-request set-priority-offset" または "tcp-request content set-priority-offset" の、最後の呼び出しで設定したものです。

proc: integer 常に値1を返します（以前は、呼び出し元のプロセス番号を返していました）。

<a id="entry-7-3-2-queue-integer"></a>

**`queue([<backend>]): integer`**

```haproxy
queue([<backend>]): integer
```

指定したバックエンドのキューで待機している接続の総数を、サーバーのキュー内のすべての接続も含めて返します。バックエンド名を指定しない場合は、現在のバックエンドを使用しますが、別のバックエンドを調べることもできます。ACLで使用したり、バックエンドサーバーに統計を渡したりするのに役立ちます。キューでの待機が、既知の水準を超えた場合に、アクションを実行するために使用できます。通常は、トラフィックの急増や、サーバーの大幅な速度低下を示します。考えられるアクションの例は、既存のユーザーは引き続き受け入れながら、新しいユーザーを拒否することです。取得関数 "avg_queue"、"be_conn"、"be_sess_rate" も参照してください。

quic_enabled: boolean QUICトランスポートプロトコルへの対応を有効にしてコンパイルし、かつglobalの "tune.quic.listen" オプションでQUICリスナーを無効にしていなければ、trueを返します。globalの "tune.quic.listen" オプションも参照してください。

<a id="entry-7-3-2-rand-integer"></a>

**`rand([<range>]): integer`**

```haproxy
rand([<range>]): integer
```

ゼロから始まる、`<range>` 個の値の範囲内で、ランダムな整数を返します。範囲を指定しなければ、デフォルトは2^32で、0から4294967295までの数値を返します。たとえば、ルーティングを決定するために必要な値を渡す場合や、単にデバッグを行う場合に役立ちます。この乱数は、セキュリティー目的に使用してはいけません。

<a id="entry-7-3-2-srv-conn-integer"></a>

**`srv_conn([<backend>/]<server>): integer`**

```haproxy
srv_conn([<backend>/]<server>): integer
```

指定したサーバーで、現在確立している接続の数を、整数で返します。評価している接続も含む場合があります。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。あるサーバーがいっぱいの場合に、特定のサーバーファームを使用したり、サーバーとのアクティブな接続数について、HAProxy側から見た情報をサーバーへ通知したりするために使用できます。取得メソッド "fe_conn"、"be_conn"、"queue"、"srv_conn_free" も参照してください。

<a id="entry-7-3-2-srv-conn-free-integer"></a>

**`srv_conn_free([<backend>/]<server>): integer`**

```haproxy
srv_conn_free([<backend>/]<server>): integer
```

指定したサーバーで、利用できる接続の数を、整数で返します。評価している接続も含む場合があります。値には、キューの空き枠を含めません。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。あるサーバーがいっぱいの場合に、特定のサーバーファームを使用したり、サーバーとのアクティブな接続数について、HAProxy側から見た情報をサーバーへ通知したりするために使用できます。取得メソッド "be_conn_free" と "srv_conn" も参照してください。

その他の注意事項： サーバーのmaxconnが0の場合、この取得関数は明らかに意味を持たないため、-1を返します。

<a id="entry-7-3-2-srv-is-up-boolean"></a>

**`srv_is_up([<backend>/]<server>): boolean`**

```haproxy
srv_is_up([<backend>/]<server>): boolean
```

指定したサーバーがUPならtrue、DOWNまたはメンテナンスモードならfalseを返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。主に、ヘルスチェックで報告した外部の状態（たとえば、地理的に離れたサイトの可用性）に応じて、アクションを実行するために使用します。別の、やや技巧的な用途として、ダミーのサーバーを、CLIから有効または無効にできるブール変数として使用し、そのACLに依存するルールを、リアルタイムで調整することもできます。

<a id="entry-7-3-2-srv-iweight-integer"></a>

**`srv_iweight([<backend>/]<server>): integer`**

```haproxy
srv_iweight([<backend>/]<server>): integer
```

サーバーの初期重みを、整数で返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。"srv_weight" と "srv_uweight" も参照してください。

<a id="entry-7-3-2-srv-queue-integer"></a>

**`srv_queue([<backend>/]<server>): integer`**

```haproxy
srv_queue([<backend>/]<server>): integer
```

指定したサーバーのキューで、現在待機している接続の数を、整数で返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。"use-server" ディレクティブと組み合わせて、速いことが分かっているサーバーの負荷が低いときに、そのサーバーを強制的に使用するために使える場合があります。サンプル取得メソッド "srv_conn"、"avg_queue"、"queue" も参照してください。

<a id="entry-7-3-2-srv-sess-rate-integer"></a>

**`srv_sess_rate([<backend>/]<server>): integer`**

```haproxy
srv_sess_rate([<backend>/]<server>): integer
```

指定したサーバーでのセッション作成速度を、毎秒の新しいセッション数を表す整数で返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。主にACLで使用しますが、ログでも意味を持つ場合があります。高コストの、または負荷に弱いバックエンドのセッション作成速度が高くなりすぎた場合に、別のバックエンドへ切り替えたり、サービスの悪用を制限したりするために使用します（たとえば、遅延するリクエストによって、サーバーに過負荷がかかるのを防ぎます）。

例：

```shell
# Redirect to a separate back
acl srv1_full srv_sess_rate(be1/srv1) gt 50
acl srv2_full srv_sess_rate(be1/srv2) gt 50
use_backend be2 if srv1_full or srv2_full
```

<a id="entry-7-3-2-srv-uweight-integer"></a>

**`srv_uweight([<backend>/]<server>): integer`**

```haproxy
srv_uweight([<backend>/]<server>): integer
```

ユーザーから見えるサーバーの重みを、整数で返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。"srv_weight" と "srv_iweight" も参照してください。

<a id="entry-7-3-2-srv-weight-integer"></a>

**`srv_weight([<backend>/]<server>): integer`**

```haproxy
srv_weight([<backend>/]<server>): integer
```

現在の（または実効的な）サーバーの重みを、整数で返します。`<backend>` を省略すると、現在のバックエンド内でサーバーを探します。"srv_iweight" と "srv_uweight" も参照してください。

stopping: boolean 関数を呼び出したプロセスが、現在、停止処理中であれば、TRUEを返します。ログの記録や、正常なシャットダウンの際に、一部のチェックを緩めたり、特定の接続を閉じやすくしたりするために役立ちます。

<a id="entry-7-3-2-str-string"></a>

**`str(<string>): string`**

```haproxy
str(<string>): string
```

文字列を返します。

<a id="entry-7-3-2-table-avl-integer"></a>

**`table_avl([<table>]): integer`**

```haproxy
table_avl([<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブルで、使用可能なエントリーの総数を返します。"table_cnt" も参照してください。

<a id="entry-7-3-2-table-cnt-integer"></a>

**`table_cnt([<table>]): integer`**

```haproxy
table_cnt([<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブルで、現在使用中のエントリーの総数を返します。エントリー数を数えるほかの方法については、"table_conn_cnt" とtable_avlも参照してください。

term_events: string ストリームに関連付けられた、クライアント側とサーバー側のすべての実体について、既知の終了イベントをすべて返します。次の情報を含む、7要素のタプルを返します。

    - フロントエンド接続の終了イベント
    - フロントエンドのマルチプレクサー接続の終了イベント
    - フロントエンドのストリームエンドポイント記述子の終了イベント
      （マルチプレクサーのストリーム、またはアプレット）
    - ストリームの終了イベント
    - バックエンドのストリームエンドポイント記述子の終了イベント
      （マルチプレクサーのストリーム、またはアプレット）
    - バックエンドのマルチプレクサー接続の終了イベント
    - バックエンド接続の終了イベント

各階層について、最初の4つのイベントを報告します。特定の階層で、まだイベントを報告していなければ、空文字列を返します。終了イベントに対応していなければ、"-" を返します。

デバッグ目的にのみ使用しなければなりません。開発者の要件に応じて変わる可能性があるため、正確な形式は文書化していません。

tgroup: integer 関数を呼び出したスレッドグループの位置を、0から (global.thread-groups - 1) までの整数で返します。ログの記録やデバッグに役立ちます。

thread: integer 関数を呼び出したスレッドの位置を、0から (global.nbthread-1) までの整数で返します。ログの記録やデバッグに役立ちます。

txn.id32: integer 内部のトランザクションIDを返します。32ビットの整数です。そのため、厳密には一意ではなく、トランザクションIDは一巡する場合があります。一巡するまでの時間は、リクエストの頻度によって決まります。実際には、問題にはならないはずです。完全に一意なIDについては、"unique-id-format" ディレクティブを参照してください。

txn.sess_term_state: string ログに報告する、TCPまたはHTTPストリームの終了状態を返します。2文字の文字列で、ストリームの最終状態に、終了の原因となったイベントが続きます。発生し得るイベントの一覧は、切断時のストリーム状態についての[8.5節](/ja/haproxy/configuration-logging/#section-8-5)を参照してください。サンプル取得関数を評価した時点の値を返します。この値は変わる可能性があります。"http-after-response" ルールセットのACL、またはログメッセージで使用する場合を除き、常に "--" になります。

例：

```shell
# Return a 429-Too-Many-Requests if stream timed out in queue
http-after-response set-status 429 if { txn.sess_term_state  "sQ" }
```

uptime: integer 現在のHAProxyワーカーの稼働時間を、秒単位で返します。

<a id="entry-7-3-2-uuid-string"></a>

**`uuid([<version>]): string`**

```haproxy
uuid([<version>]): string
```

RFC 9562標準に従うUUIDを返します。バージョンを指定しなければ、バージョン4のUUID（完全にランダム）を返します。

バージョン4と7に対応しています。

<a id="entry-7-3-2-var-undefined"></a>

**`var(<var-name>[,<default>]): undefined`**

```haproxy
var(<var-name>[,<default>]): undefined
```

格納した型のまま、変数を返します。変数を設定していなければ、サンプル取得は失敗します。ただし、デフォルト値を指定している場合は、それを文字列として返します。空文字列も使用できます。詳細は、変数についての[2.8節](/ja/haproxy/configuration-basics/#section-2-8)を参照してください。

<a id="entry-7-3-2-dump-all-vars-string"></a>

**`dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string`**

```haproxy
dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string
```

指定したスコープのすべての変数を、一覧で返します。任意で名前の接頭辞による絞り込みができ、区切り文字も変更できます。

出力形式： var1=value1`<delim>`var2=value2`<delim>`...

型ごとの値のエンコーディング：

- 文字列： 引用符で囲み、エスケープします (", &#92;, &#92;r,
  &#92;n, &#92;b, &#92;0)。例：
  txn.name="John &#92;"Doe&#92;""
- バイナリ： 'x' 接頭辞を付けた16進エンコーディングで、引用符は付けません。例： txn.data=x48656c6c6f
- 整数： 引用符なしの10進数です。例： txn.count=42
- ブール値： 引用符なしの "true" または "false" です。例： txn.active=true
- アドレス： 引用符なしのIPアドレス文字列です。例： txn.client=192.168.1.1
- HTTPメソッド： 引用符で囲んだ文字列です。例： req.method="GET"

引数：

- `<scope>`（省略可能）: sess、txn、req、res、procです。省略すると、ここに示した順に、すべてのスコープを調べます。

- `<prefix>`（省略可能）: スコープの接頭辞を取り除いた後の名前が、指定した接頭辞で始まる変数を絞り込みます。性能に関する注意： 接頭辞で絞り込む場合も、スコープ内のすべての変数を調べます。数千の変数を含む設定では、使用すべきではありません。

- `<delimiter>`（省略可能）: 変数を区切る文字列です。デフォルトは ", "（コンマとスペース）です。任意の文字列に変更できます。なお、関数の引数にコンマやスペースを渡すには、シングルクォートかダブルクォートで囲む必要があります（式自体をすでに引用符で囲んでいる場合は、もう一方を使用します）。

戻り値：

- 成功時： 一致したすべての変数を含む文字列
- 失敗時： 出力バッファーが小さすぎる場合は空になります（サンプル取得は失敗します）。出力を切り詰めることはありません。不完全なデータを避けるため、処理全体が失敗します。

デバッグ、ログの記録、変数の状態のエクスポートに、特に役立ちます。

例：

```shell
# Dump all transaction variables
http-request return string %[dump_all_vars(txn)]

# Dump only variables starting with "user"
http-request set-header X-User-Vars "%[dump_all_vars(txn,user)]"

# Dump all process variables
http-request return string %[dump_all_vars(proc)]

# Custom delimiter (semicolon)
http-request set-header X-Vars "%[dump_all_vars(txn,,; )]"

# Force the default delimiter (comma space)
http-request set-header X-Vars "%[dump_all_vars(txn,,', ')]"

# Prefix filter with custom delimiter
http-request set-header X-Session "%[dump_all_vars(sess,user,|)]"

```

wait_end: boolean 検査期間が終わった場合にtrueを返し、そうでなければ取得しません。ACLでのみ、内容の解析と組み合わせて使用し、早すぎる段階で誤った判定を返すことを防ぎます。特定のアドレスを遅延させて拒否するなど、一部のアクションを遅らせるために使用することもできます。ルールの評価を停止するか、直ちにtrueを返すかのどちらかなので、ルールの最後のACLとして使用することを推奨します。デフォルトのACL "WAIT_END" は、事前の宣言なしで、常に使用できる点に注意してください。このテストは、TCPリクエストの内容検査で使用するために設計しています。

例：

```shell
# delay every incoming request by 2 seconds
tcp-request inspect-delay 2s
tcp-request content accept if WAIT_END

# don't immediately tell bad guys they are rejected
tcp-request inspect-delay 10s
acl goodguys src 10.0.0.0/24
acl badguys  src 10.0.1.0/24
tcp-request content accept if goodguys
tcp-request content reject if badguys WAIT_END
tcp-request content reject
```

waiting_entity: string エラーまたはタイムアウトが発生したときに、処理を続行できるのを待っていた実体の識別情報を返します。たとえば、ルールやフィルターの場合があります。ただし、この一覧は網羅的なものではなく、すべての実体の形式を必ず文書化しているわけではありません。

実体がルールの場合は、その場所を返します。ルールを含む設定ファイルと、そのファイル内でルールを定義した行を、コロンで区切ったものです。

フィルターの場合は、開発者が定義した識別子を返します。その識別子を定義していなければ、一意の内部識別子に対応する16進数の値を返します。

この関数の主な目的は、エラーまたはタイムアウトによって処理を中断したときに、ストリームの解析をブロックしていた実体をログに報告し、問題のデバッグに役立てることです。実体について返す情報は、時とともに変わる可能性があり、デバッグ以外の目的に使用してはいけません。

例：

```shell
# Log the waiting entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[waiting_entity,when(error)]
```

### 7.3.3. レイヤー4でのサンプル取得 {#section-7-3-3}

レイヤー4は、通常、トランスポート層だけを指します。HAProxyでは接続に最も近く、まだ内容を利用できない層です。ここで説明する取得メソッドは、後で得られる情報を必要とする場合を除き、"tcp-request connection" ルールセットという早い段階から使用できます。通常は、TCP/IPのアドレスとポート、および着信接続に関係するスティックテーブルの要素などを取得します。スティックカウンターから値を取得するには、定義済みの接頭辞 "sc0\_"、"sc1\_"、"sc2\_" で、カウンター番号を0、1、2と明示できます。これら3つの定義済みの接頭辞は、globalの "tune.stick-counters" の値が3を超えない場合にのみ使用できます。それ以外の場合は、"sc\_" 接頭辞を使用し、最初の整数引数としてカウンター番号を指定できます。"sc_0" から "sc_N" までで、Nは (tune.stick-counters-1) です。"sc\*" 形式では、任意でテーブルを指定できます。その場合、現在追跡しているキーを、現在追跡しているテーブルの代わりに、指定した別のテーブルで検索します。

この節のサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                       出力型
-------------------------------------------------+-------------
accept_date([<unit>])                              integer
bc.timer.connect                                   integer
bc_be_queue                                        integer
bc_dst                                             ip
bc_dst_port                                        integer
bc_err                                             integer
bc_err_name                                        string
bc_err_str                                         string
bc_glitches                                        integer
bc_http_major                                      integer
bc_nb_streams                                      integer
bc_reused                                          boolean
bc_rtt(<unit>)                                     integer
bc_rttvar(<unit>)                                  integer
bc_settings_streams_limit                          integer
bc_src                                             ip
bc_src_port                                        integer
bc_srv_queue                                       integer
be_id                                              integer
be_name                                            string
be_connect_timeout                                 integer
be_queue_timeout                                   integer
be_server_timeout                                  integer
be_tarpit_timeout                                  integer
be_tunnel_timeout                                  integer
bytes_in                                           integer
bytes_out                                          integer
cur_connect_timeout                                integer
cur_client_timeout                                 integer
cur_queue_timeout                                  integer
cur_server_timeout                                 integer
cur_tarpit_timeout                                 integer
cur_tunnel_timeout                                 integer
dst                                                ip
dst_conn                                           integer
dst_is_local                                       boolean
dst_port                                           integer
fc.timer.handshake                                 integer
fc.timer.total                                     integer
fc_dst                                             ip
fc_dst_is_local                                    boolean
fc_dst_port                                        integer
fc_err                                             integer
fc_err_name                                        string
fc_err_str                                         string
fc_fackets                                         integer
fc_glitches                                        integer
fc_http_major                                      integer
fc_lost                                            integer
fc_nb_streams                                      integer
fc_pp_authority                                    string
fc_pp_tlv(<id>)                                    string
fc_pp_unique_id                                    string
fc_rcvd_proxy                                      boolean
fc_reordering                                      integer
fc_retrans                                         integer
fc_rtt(<unit>)                                     integer
fc_rttvar(<unit>)                                  integer
fc_sacked                                          integer
fc_saved_syn                                       binary
fc_settings_streams_limit                          integer
fc_src                                             ip
fc_src_is_local                                    boolean
fc_src_port                                        integer
fc_unacked                                         integer
fe_tarpit_timeout                                  integer
fe_client_timeout                                  integer
fe_defbe                                           string
fe_id                                              integer
fe_name                                            string
req.bytes_in                                       integer
req.bytes_out                                      integer
res.bytes_in                                       integer
res.bytes_out                                      integer
res.timer.data                                     integer
sc0_bytes_in_rate([<table>])                       integer
sc0_bytes_out_rate([<table>])                      integer
sc0_clr_gpc0([<table>])                            integer
sc0_clr_gpc1([<table>])                            integer
sc0_conn_cnt([<table>])                            integer
sc0_conn_cur([<table>])                            integer
sc0_conn_rate([<table>])                           integer
sc0_get_gpc0([<table>])                            integer
sc0_get_gpc1([<table>])                            integer
sc0_get_gpt0([<table>])                            integer
sc0_glitch_cnt([<table>])                          integer
sc0_glitch_rate([<table>])                         integer
sc0_gpc0_rate([<table>])                           integer
sc0_gpc1_rate([<table>])                           integer
sc0_http_err_cnt([<table>])                        integer
sc0_http_err_rate([<table>])                       integer
sc0_http_fail_cnt([<table>])                       integer
sc0_http_fail_rate([<table>])                      integer
sc0_http_req_cnt([<table>])                        integer
sc0_http_req_rate([<table>])                       integer
sc0_inc_gpc0([<table>])                            integer
sc0_inc_gpc1([<table>])                            integer
sc0_kbytes_in([<table>])                           integer
sc0_kbytes_out([<table>])                          integer
sc0_key                                            any
sc0_sess_cnt([<table>])                            integer
sc0_sess_rate([<table>])                           integer
sc0_tracked([<table>])                             boolean
sc0_trackers([<table>])                            integer
sc1_bytes_in_rate([<table>])                       integer
sc1_bytes_out_rate([<table>])                      integer
sc1_clr_gpc0([<table>])                            integer
sc1_clr_gpc1([<table>])                            integer
sc1_conn_cnt([<table>])                            integer
sc1_conn_cur([<table>])                            integer
sc1_conn_rate([<table>])                           integer
sc1_get_gpc0([<table>])                            integer
sc1_get_gpc1([<table>])                            integer
sc1_get_gpt0([<table>])                            integer
sc1_glitch_cnt([<table>])                          integer
sc1_glitch_rate([<table>])                         integer
sc1_gpc0_rate([<table>])                           integer
sc1_gpc1_rate([<table>])                           integer
sc1_http_err_cnt([<table>])                        integer
sc1_http_err_rate([<table>])                       integer
sc1_http_fail_cnt([<table>])                       integer
sc1_http_fail_rate([<table>])                      integer
sc1_http_req_cnt([<table>])                        integer
sc1_http_req_rate([<table>])                       integer
sc1_inc_gpc0([<table>])                            integer
sc1_inc_gpc1([<table>])                            integer
sc1_kbytes_in([<table>])                           integer
sc1_kbytes_out([<table>])                          integer
sc1_key                                            any
sc1_sess_cnt([<table>])                            integer
sc1_sess_rate([<table>])                           integer
sc1_tracked([<table>])                             boolean
sc1_trackers([<table>])                            integer
sc2_bytes_in_rate([<table>])                       integer
sc2_bytes_out_rate([<table>])                      integer
sc2_clr_gpc0([<table>])                            integer
sc2_clr_gpc1([<table>])                            integer
sc2_conn_cnt([<table>])                            integer
sc2_conn_cur([<table>])                            integer
sc2_conn_rate([<table>])                           integer
sc2_get_gpc0([<table>])                            integer
sc2_get_gpc1([<table>])                            integer
sc2_get_gpt0([<table>])                            integer
sc2_glitch_cnt([<table>])                          integer
sc2_glitch_rate([<table>])                         integer
sc2_gpc0_rate([<table>])                           integer
sc2_gpc1_rate([<table>])                           integer
sc2_http_err_cnt([<table>])                        integer
sc2_http_err_rate([<table>])                       integer
sc2_http_fail_cnt([<table>])                       integer
sc2_http_fail_rate([<table>])                      integer
sc2_http_req_cnt([<table>])                        integer
sc2_http_req_rate([<table>])                       integer
sc2_inc_gpc0([<table>])                            integer
sc2_inc_gpc1([<table>])                            integer
sc2_kbytes_in([<table>])                           integer
sc2_kbytes_out([<table>])                          integer
sc2_key                                            any
sc2_sess_cnt([<table>])                            integer
sc2_sess_rate([<table>])                           integer
sc2_tracked([<table>])                             boolean
sc2_trackers([<table>])                            integer
sc_bytes_in_rate(<ctr>[,<table>])                  integer
sc_bytes_out_rate(<ctr>[,<table>])                 integer
sc_clr_gpc(<idx>,<ctr>[,<table>])                  integer
sc_clr_gpc0(<ctr>[,<table>])                       integer
sc_clr_gpc1(<ctr>[,<table>])                       integer
sc_conn_cnt(<ctr>[,<table>])                       integer
sc_conn_cur(<ctr>[,<table>])                       integer
sc_conn_rate(<ctr>[,<table>])                      integer
sc_get_gpc(<idx>,<ctr>[,<table>])                  integer
sc_get_gpc0(<ctr>[,<table>])                       integer
sc_get_gpc1(<ctr>[,<table>])                       integer
sc_get_gpt(<idx>,<ctr>[,<table>])                  integer
sc_get_gpt0(<ctr>[,<table>])                       integer
sc_glitch_cnt(<ctr>[,<table>])                     integer
sc_glitch_rate(<ctr>[,<table>])                    integer
sc_gpc0_rate(<ctr>[,<table>])                      integer
sc_gpc1_rate(<ctr>[,<table>])                      integer
sc_gpc_rate(<idx>,<ctr>[,<table>])                 integer
sc_http_err_cnt(<ctr>[,<table>])                   integer
sc_http_err_rate(<ctr>[,<table>])                  integer
sc_http_fail_cnt(<ctr>[,<table>])                  integer
sc_http_fail_rate(<ctr>[,<table>])                 integer
sc_http_req_cnt(<ctr>[,<table>])                   integer
sc_http_req_rate(<ctr>[,<table>])                  integer
sc_inc_gpc(<idx>,<ctr>[,<table>])                  integer
sc_inc_gpc0(<ctr>[,<table>])                       integer
sc_inc_gpc1(<ctr>[,<table>])                       integer
sc_kbytes_in(<ctr>[,<table>])                      integer
sc_kbytes_out(<ctr>[,<table>])                     integer
sc_key(<ctr>)                                      any
sc_sess_cnt(<ctr>[,<table>])                       integer
sc_sess_rate(<ctr>[,<table>])                      integer
sc_tracked(<ctr>[,<table>])                        boolean
sc_trackers(<ctr>[,<table>])                       integer
so_id                                              integer
so_name                                            string
src                                                ip
src_bytes_in_rate([<table>])                       integer
src_bytes_out_rate([<table>])                      integer
src_clr_gpc(<idx>[,<table>])                       integer
src_clr_gpc0([<table>])                            integer
src_clr_gpc1([<table>])                            integer
src_conn_cnt([<table>])                            integer
src_conn_cur([<table>])                            integer
src_conn_rate([<table>])                           integer
src_get_gpc(<idx>[,<table>])                       integer
src_get_gpc0([<table>])                            integer
src_get_gpc1([<table>])                            integer
src_get_gpt(<idx>[,<table>])                       integer
src_get_gpt0([<table>])                            integer
src_glitch_cnt([<table>])                          integer
src_glitch_rate([<table>])                         integer
src_gpc0_rate([<table>])                           integer
src_gpc1_rate([<table>])                           integer
src_gpc_rate(<idx>[,<table>])                      integer
src_http_err_cnt([<table>])                        integer
src_http_err_rate([<table>])                       integer
src_http_fail_cnt([<table>])                       integer
src_http_fail_rate([<table>])                      integer
src_http_req_cnt([<table>])                        integer
src_http_req_rate([<table>])                       integer
src_inc_gpc(<idx>[,<table>])                       integer
src_inc_gpc0([<table>])                            integer
src_inc_gpc1([<table>])                            integer
src_is_local                                       boolean
src_kbytes_in([<table>])                           integer
src_kbytes_out([<table>])                          integer
src_port                                           integer
src_sess_cnt([<table>])                            integer
src_sess_rate([<table>])                           integer
src_updt_conn_cnt([<table>])                       integer
srv_id                                             integer
srv_name                                           string
txn.conn_retries                                   integer
txn.redispatched                                   boolean
-------------------------------------------------+-------------
```

詳細な一覧：

<a id="entry-7-3-3-accept-date-integer"></a>

**`accept_date([<unit>]): integer`**

```haproxy
accept_date([<unit>]): integer
```

HAProxyが接続を受け付けた、正確な日時です（システムのバックログ内で待機していた場合、ネットワーク上で観測した日時とは、わずかに異なることがあります）。通常は、上流のファイアウォールのログに現れる日時と同じです。HTTPモードでは、accept_dateフィールドを、接続が新しいリクエストを受信できるようになった最初の時点にリセットします（HTTP/1では前のレスポンスの終了時、HTTP/2では前のリクエストの直後）。

エポックからの秒数を返します。

`<unit>` は省略可能で、秒を表す "s"（デフォルトの動作）、ミリ秒を表す "ms"、マイクロ秒を表す "us" を指定できます。単位を指定した場合、戻り値は、エポックからの秒数、ミリ秒数、またはマイクロ秒数を表す整数です。秒未満の時間分解能が必要な場合に役立ちます。

bc.timer.connect: integer サーバーへのTCP接続を確立するための、合計時間です。log-formatの%Tcに相当します。ミリ秒 (ms) 単位で報告します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

bc_be_queue: integer 対象バックエンドの接続枠を待っている間に、キューから取り出されたストリーム数です。log-formatの%bqに相当します。

bc_dst: ip サーバー側の接続の宛先IPアドレス、つまり、HAProxyが接続したサーバーのアドレスです。IP型で、IPv4とIPv6の両方のテーブルで使用できます。IPv6テーブルでは、RFC 4291に従って、IPv4アドレスを、対応するIPv6アドレスにマッピングします。

bc_dst_port: integer サーバー側の接続の宛先TCPポート、つまり、HAProxyが接続したポートを、整数で返します。

bc_err: integer 現在のバックエンド接続で発生した可能性がある、エラーのIDを返します。エラーコードと、対応するエラーメッセージの完全な一覧は、取得関数 "fc_err_str" を参照してください。

bc_err_name: string バックエンド接続で発生し、接続を失敗させた問題を示す、内部のエラー名を返します。この文字列は単一の単語からなり、エラーがなければ空です。"fc_err_str" キーワードに示した表の、"name" 列に対応します。

bc_err_str: string 現在のバックエンド接続で発生し、接続を失敗させた問題を示す、エラーメッセージを返します。エラーコードと、対応するエラーメッセージの完全な一覧は、取得関数 "fc_err_str" を参照してください。

bc_glitches: integer バックエンド接続で数えた、プロトコル上の異常の回数を返します。通常は、プロトコル違反や小さな異常を含み、不具合がある、または不正な動作をするサーバーを示します。そのようなサーバーは、インフラに問題を引き起こす可能性があります（たとえば、接続を早く中止させ、TLSの再ネゴシエーションを頻発させます）。単一のバッファーに収まらない、大きすぎるレスポンスによって生じる場合もあり、HTTP 502エラーの原因を説明します。理想的にはゼロのままであるべきですが、総リクエスト数に比べて非常に少なければ、通常は問題ありません。急増はどこかに異常があることを示す場合がありますが、通常、特に小さい値は、警戒すべきものとは考えません。すべてのプロトコル・マルチプレクサーが、この指標を測定するわけではありません。イベントの詳細を知る唯一の方法は、トレースを有効にし、すべてのやり取りを記録することです。

bc_http_major: integer バックエンド接続で使用する、HTTPのメジャーバージョンのエンコーディングを返します。HTTP/0.9からHTTP/1.1では1、HTTP/2では2です。リクエストヘッダー内のバージョンではなく、通信路上のエンコーディングに基づく点に注意してください。

bc_nb_streams: integer バックエンド接続で開いたストリーム数を返します。

bc_reused: boolean 再利用したバックエンド接続で転送した場合、trueを返します。

<a id="entry-7-3-3-bc-rtt-integer"></a>

**`bc_rtt(<unit>): integer`**

```haproxy
bc_rtt(<unit>): integer
```

バックエンド接続について、カーネルが測定した往復時間 (RTT) を返します。`<unit>` は省略可能で、デフォルトの単位はミリ秒です。`<unit>` には、ミリ秒を表す "ms"、またはマイクロ秒を表す "us" を指定できます。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

<a id="entry-7-3-3-bc-rttvar-integer"></a>

**`bc_rttvar(<unit>): integer`**

```haproxy
bc_rttvar(<unit>): integer
```

バックエンド接続について、カーネルが測定した往復時間 (RTT) の分散を返します。`<unit>` は省略可能で、デフォルトの単位はミリ秒です。`<unit>` には、ミリ秒を表す "ms"、またはマイクロ秒を表す "us" を指定できます。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

bc_settings_streams_limit: integer バックエンド接続で許可する、ストリーム数の上限を返します。TCPとHTTP/1.1の接続では、常に1です。ほかのプロトコルでは、サーバーとネゴシエートした設定によって決まります。

bc_src: ip サーバー側の接続の送信元IPアドレス、つまり、HAProxyが接続を開始した側のサーバーアドレスです。IP型で、IPv4とIPv6の両方のテーブルで使用できます。IPv6テーブルでは、RFC 4291に従って、IPv4アドレスを、対応するIPv6アドレスにマッピングします。

bc_src_port: integer サーバー側の接続の送信元TCPポート、つまり、HAProxyが接続を開始した側のポートを、整数で返します。

bc_srv_queue: integer 対象サーバーの接続枠を待っている間に、キューから取り出されたストリーム数です。log-formatの%sqに相当します。

be_id: integer 現在のバックエンドのIDを含む整数を返します。フロントエンドでレスポンスとともに使用し、どのバックエンドがリクエストを処理したかを確認できます。フロントエンドで使用し、バックエンドを使用していなければ、現在のフロントエンドのIDを返します。tcp-checkまたはhttp-checkルールセットでも使用できます。

be_connect_timeout: integer 現在のバックエンドの接続タイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。"cur_connect_timeout" も参照してください。

be_name: string 現在のバックエンドの名前を含む文字列を返します。フロントエンドでレスポンスとともに使用し、どのバックエンドがリクエストを処理したかを確認できます。フロントエンドで使用し、バックエンドを使用していなければ、現在のフロントエンドの名前を返します。tcp-checkまたはhttp-checkルールセットでも使用できます。

be_queue_timeout: integer 現在のバックエンドのキュータイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。"cur_queue_timeout" も参照してください。

be_server_timeout: integer 現在のバックエンドのサーバータイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。"cur_server_timeout" も参照してください。

be_tarpit_timeout: integer 現在のバックエンドのキュータイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。"cur_tarpit_timeout" も参照してください。

be_tunnel_timeout: integer 現在のバックエンドのトンネルタイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。"cur_tunnel_timeout" も参照してください。

bytes_in: integer "req.bytes_in" を参照してください。

bytes_out: integer "res.bytes_in" を参照してください。

cur_connect_timeout: integer ストリームに現在適用している接続タイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、be_connect_timeoutと同じ値になります。"be_connect_timeout" も参照してください。

cur_client_timeout: integer ストリームに現在適用しているクライアントタイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、fe_client_timeoutと同じ値になります。"fe_client_timeout" も参照してください。

cur_queue_timeout: integer ストリームに現在適用しているキュータイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、be_queue_timeoutと同じ値になります。"be_queue_timeout" も参照してください。

cur_server_timeout: integer ストリームに現在適用しているサーバータイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、be_server_timeoutと同じ値になります。"be_server_timeout" も参照してください。

cur_tarpit_timeout: integer ストリームに現在適用しているtarpitタイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、fe_tarpit_timeout/be_tarpit_timeoutと同じ値になります。"fe_tarpit_timeout" と "be_tarpit_timeout" も参照してください。

cur_tunnel_timeout: integer ストリームに現在適用しているトンネルタイムアウトを、ミリ秒単位で返します。デフォルトでは、"set-timeout" ルールを適用していなければ、be_tunnel_timeoutと同じ値になります。"be_tunnel_timeout" も参照してください。

dst: ip クライアント側の接続の宛先IPアドレス、つまり、クライアントが接続したアドレスです。どのtcp/httpルールでも、このアドレスを変更できます。透過モードでの実行時に役立つ場合があります。IP型で、IPv4とIPv6の両方のテーブルで使用できます。IPv6テーブルでは、RFC 4291に従って、IPv4アドレスを、対応するIPv6アドレスにマッピングします。着信接続が、接続追跡を伴うアドレス変換やリダイレクトを経由した場合は、リダイレクト前の元の宛先アドレスを報告します。Linuxシステムでは、nf_conntrack_tcp_loose sysctlを設定している場合、まれに送信元と宛先が逆に見えることがあります。遅れて届いたレスポンスが、タイムアウトした接続を再び開き、送信元と宛先とみなす側を入れ替える可能性があるためです。

dst_conn: integer 同じソケット上で現在確立している接続の数を、評価している接続も含めて、整数で返します。通常はACLで使用しますが、HTTPヘッダーやログで、その情報をサーバーに渡すためにも使用できます。完全にブロックする前に、お詫びのページを返したり、ソケットが飽和していると判断した場合に、特定のバックエンドへ新しいリクエストを流したりするために使用できます。これにより、待ち受けるポートやアドレスごとに、異なる上限を割り当てられます。取得関数 "fe_conn" と "be_conn" も参照してください。

dst_is_local: boolean 着信接続の宛先アドレスが、システムのローカルアドレスならtrue、システムに存在しないアドレスならfalseを返します。後者は、透過モードで捕捉したことを意味します。転送するトラフィックと、マシンの実際のアドレス宛てのトラフィックに対して、それぞれ別のデフォルトルールを適用するのに役立ちます。たとえば、そのアドレスでのみ統計ページを提供したり、SSHアクセスをローカルにリダイレクトしたりできます。チェックには、いくつかのシステムコールが必要なため、接続ごとに1回だけ実行する方がよい点に注意してください。

dst_port: integer クライアント側の接続の宛先TCPポート、つまり、クライアントが接続したポートを、整数で返します。どのtcp/httpルールでも、このアドレスを変更できます。透過モードでの実行時、アプリケーションのセッション全体について、一部のクライアントに動的なポートを割り当てる場合、すべてのユーザーを同じサーバーに固定する場合、またはHTTPヘッダーでサーバーへ宛先ポート情報を渡す場合に、使用できます。

fc.timer.handshake: integer TCP接続の受け付けと、下位プロトコルのハンドシェイクの実行にかかった、合計時間です。現在の対象プロトコルは、proxy-protocolとSSLです。log-formatの%Thに相当します。ミリ秒 (ms) 単位で報告します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

fc.timer.total: integer プロキシが受け付けた時点から、両端を閉じた時点までの、ストリームの合計存続時間です。log-formatの%Ttに相当します。ミリ秒 (ms) 単位で報告します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

fc_dst: ip クライアント側の接続の、元の宛先IPアドレスです。"tcp-request connection" ルールだけが、このアドレスを変更できます。詳細は "dst" を参照してください。

fc_dst_is_local: boolean 着信接続の元の宛先アドレスが、システムのローカルアドレスならtrue、システムに存在しないアドレスならfalseを返します。詳細は "dst_is_local" を参照してください。

fc_dst_port: integer クライアント側の接続の、元の宛先TCPポートを、整数で返します。"tcp-request connection" ルールだけが、このアドレスを変更できます。詳細は "dst-port" を参照してください。

fc_err: integer 現在の接続で発生した可能性がある、エラーのIDを返します。戻り値が厳密に正である場合は、接続が成功しておらず、エラーログを出力することを意味します（[8.2.5節](/ja/haproxy/configuration-logging/#section-8-2-5)で説明しています）。エラーコードと、対応するエラーメッセージの完全な一覧は、取得関数 "fc_err_str" を参照してください。

fc_err_name: string フロントエンド接続で発生し、接続を失敗させた問題を示す、内部のエラー名を返します。この文字列は単一の単語からなり、エラーがなければ空です。"fc_err_str" キーワードに示した表の、"name" 列に対応します。

fc_err_str: string 現在の接続で発生し、接続を失敗させた問題を示す、エラーメッセージを返します。この文字列は、エラーログ形式の "message" 部分に対応します（[8.2.5節](/ja/haproxy/configuration-logging/#section-8-2-5)を参照）。エラーコードと、対応するエラーメッセージの完全な一覧は、以下を参照してください。

```text
  +----+------------------+-------------------------------------------------------------------------+
  | ID | 名前             | メッセージ                                                              |
  +----+------------------+-------------------------------------------------------------------------+
  | 0  | -                | "Success"                                                               |
  | 1  | CONF_FDLIM       | "Reached configured maxconn value"                                      |
  | 2  | PROC_FDLIM       | "Too many sockets on the process"                                       |
  | 3  | SYS_FDLIM        | "Too many sockets on the system"                                        |
  | 4  | SYS_MEMLIM       | "Out of system buffers"                                                 |
  | 5  | NOPROTO          | "Protocol or address family not supported"                              |
  | 6  | SOCK_ERR         | "General socket error"                                                  |
  | 7  | PORT_RANGE       | "Source port range exhausted"                                           |
  | 8  | CANT_BIND        | "Can't bind to source address"                                          |
  | 9  | FREE_PORTS       | "Out of local source ports on the system"                               |
  | 10 | ADDR_INUSE       | "Local source address already in use"                                   |
  | 11 | PRX_EMPTY        | "Connection closed while waiting for PROXY protocol header"             |
  | 12 | PRX_ABORT        | "Connection error while waiting for PROXY protocol header"              |
  | 13 | PRX_TIMEOUT      | "Timeout while waiting for PROXY protocol header"                       |
  | 14 | PRX_TRUNCATED    | "Truncated PROXY protocol header received"                              |
  | 15 | PRX_NOT_HDR      | "Received something which does not look like a PROXY protocol header"   |
  | 16 | PRX_BAD_HDR      | "Received an invalid PROXY protocol header"                             |
  | 17 | PRX_BAD_PROTO    | "Received an unhandled protocol in the PROXY protocol header"           |
  | 18 | CIP_EMPTY        | "Connection closed while waiting for NetScaler Client IP header"        |
  | 19 | CIP_ABORT        | "Connection error while waiting for NetScaler Client IP header"         |
  | 20 | CIP_TIMEOUT      | "Timeout while waiting for a NetScaler Client IP header"                |
  | 21 | CIP_TRUNCATED    | "Truncated NetScaler Client IP header received"                         |
  | 22 | CIP_BAD_MAGIC    | "Received an invalid NetScaler Client IP magic number"                  |
  | 23 | CIP_BAD_PROTO    | "Received an unhandled protocol in the NetScaler Client IP header"      |
  | 24 | SSL_EMPTY        | "Connection closed during SSL handshake"                                |
  | 25 | SSL_ABORT        | "Connection error during SSL handshake"                                 |
  | 26 | SSL_TIMEOUT      | "Timeout during SSL handshake"                                          |
  | 27 | SSL_TOO_MANY     | "Too many SSL connections"                                              |
  | 28 | SSL_NO_MEM       | "Out of memory when initializing an SSL connection"                     |
  | 29 | SSL_RENEG        | "Rejected a client-initiated SSL renegotiation attempt"                 |
  | 30 | SSL_CA_FAIL      | "SSL client CA chain cannot be verified"                                |
  | 31 | SSL_CRT_FAIL     | "SSL client certificate not trusted"                                    |
  | 32 | SSL_MISMATCH     | "Server presented an SSL certificate different from the configured one" |
  | 33 | SSL_MISMATCH_SNI | "Server presented an SSL certificate different from the expected one"   |
  | 34 | SSL_HANDSHAKE    | "SSL handshake failure"                                                 |
  | 35 | SSL_HANDSHAKE_HB | "SSL handshake failure after heartbeat"                                 |
  | 36 | SSL_KILLED_HB    | "Stopped a TLSv1 heartbeat attack (CVE-2014-0160)"                      |
  | 37 | SSL_NO_TARGET    | "Attempt to use SSL on an unknown target (internal error)"              |
  | 38 | SSL_EARLY_FAILED | "Server refused early data"                                             |
  | 39 | SOCKS4_SEND      | "SOCKS4 Proxy write error during handshake"                             |
  | 40 | SOCKS4_RECV      | "SOCKS4 Proxy read error during handshake"                              |
  | 41 | SOCKS4_DENY      | "SOCKS4 Proxy deny the request"                                         |
  | 42 | SOCKS4_ABORT     | "SOCKS4 Proxy handshake aborted by server"                              |
  | 43 | SSL_FATAL        | "SSL fatal error"                                                       |
  | 44 | REVERSE          | "Reverse connect failure"                                               |
  | 45 | POLLERR          | "Poller reported POLLERR"                                               |
  | 46 | EREFUSED         | "ECONNREFUSED returned by OS"                                           |
  | 47 | ERESET           | "ECONNRESET returned by OS"                                             |
  | 48 | EUNREACH         | "ENETUNREACH returned by OS"                                            |
  | 49 | ENOMEM           | "ENOMEM returned by OS"                                                 |
  | 50 | EBADF            | "EBADF returned by OS"                                                  |
  | 51 | EFAULT           | "EFAULT returned by OS"                                                 |
  | 52 | EINVAL           | "EINVAL returned by OS"                                                 |
  | 53 | ENCONN           | "ENCONN returned by OS"                                                 |
  | 54 | ENSOCK           | "ENSOCK returned by OS"                                                 |
  | 55 | ENOBUFS          | "ENOBUFS returned by OS"                                                |
  | 56 | EPIPE            | "EPIPE returned by OS"                                                  |
  +----+------------------+-------------------------------------------------------------------------+
```

fc_fackets: integer クライアント接続について、カーネルが測定したfackカウンターを返します。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fc_glitches: integer フロントエンド接続で数えた、プロトコル上の異常の回数を返します。通常は、プロトコル違反や小さな異常を含み、不具合がある、または不正な動作をするクライアントを示します。そのようなクライアントは、ログ内の過剰なエラーや、多数の接続の早期中止によるTLSの再ネゴシエーションの頻発など、インフラに問題を引き起こす可能性があります。単一のバッファーに収まらない、大きすぎるリクエストによって生じる場合もあり、HTTP 400エラーの原因を説明します。理想的にはゼロのままであるべきですが、プロトコルの境界的な動作を試すブラウザーが、ときどき発生させることもあり得ます。急増はどこかに異常があることを示す場合がありますが、通常、特に小さい値は、警戒すべきものとは考えません。大きい値（接続ごとに数百から数千、またはリクエスト数と同程度）は、プロトコルスタックの特徴を調べたり、攻撃したりするために、意図的に作られたクライアントを示す場合があります。すべてのプロトコル・マルチプレクサーが、この指標を測定するわけではありません。イベントの詳細を知る唯一の方法は、トレースを有効にし、すべてのやり取りを記録することです。

fc_http_major: integer フロント側の接続で使用する、HTTPのメジャーバージョンのエンコーディングを報告します。HTTP/0.9からHTTP/1.1では1、HTTP/2では2です。リクエストヘッダー内のバージョンではなく、通信路上のエンコーディングに基づく点に注意してください。

fc_lost: integer 接続がTCPでもQUICでもなければ、サンプル取得に失敗します。QUICでは、クライアント接続で失われたQUICパケット数を返します。TCPでは、クライアント接続について、カーネルが測定したlostカウンターを返します。サーバー接続を確立していない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fc_nb_streams: integer フロントエンド接続で開いたストリーム数を返します。

fc_pp_authority: string クライアントがPROXYプロトコルヘッダーで送信した、最初のauthority TLVがあれば、それを返します。

<a id="entry-7-3-3-fc-pp-tlv-string"></a>

**`fc_pp_tlv(<id>): string`**

```haproxy
fc_pp_tlv(<id>): string
```

指定したTLV IDに対応するTLVの値を返します。IDは、0から255までの数値、または、PPv2仕様のTLV定数の接尾辞に対応する、次のシンボル名のいずれかでなければなりません： "ALPN": PP2_TYPE_ALPN, "AUTHORITY": PP2_TYPE_AUTHORITY, "CRC32": PP2_TYPE_CRC32C,
"NETNS": PP2_TYPE_NETNS, "NOOP: PP2_TYPE_NOOP", "SSL": PP2_TYPE_SSL, "SSL_CIPHER":
PP2_SUBTYPE_SSL_CIPHER, "SSL_CN": PP2_SUBTYPE_SSL_CN, "SSL_KEY_ALG": PP2_SUBTYPE_SSL_KEY_ALG,
"SSL_SIG_ALG": PP2_SUBTYPE_SSL_SIG_ALG, "SSL_VERSION": PP2_SUBTYPE_SSL_VERSION, "UNIQUE_ID":
PP2_TYPE_UNIQUE_ID.

受信する値は、1024バイト以下でなければなりません。潜在的なDoS攻撃を防ぐためです。256バイト以下の値は、メモリープールを使用できます。そのため、最適な性能を得るには、送信する値の長さを256バイトまでに抑えるようにしてください。

fc_pp_authorityとfc_pp_unique_idとは異なり、fc_pp_tlvは、TLV IDが重複する場合、要求したTLVのすべての出現箇所を、反復して取得できる点に注意してください。反復の順序は、PROXYプロトコルヘッダー内の位置に対応します。ただし、通常、TLVは一意とみなすため、重複への依存は、原則として避けるべきです。一般に、TLV IDの重複は、PROXYプロトコルヘッダーの送信側に、誤りがあることを示します。

fc_pp_unique_id: string クライアントがPROXYプロトコルヘッダーで送信した、最初のunique ID TLVがあれば、それを返します。

fc_rcvd_proxy: boolean クライアントがPROXYプロトコルヘッダーで接続を開始した場合、trueを返します。

fc_reordering: integer 接続がTCPでもQUICでもなければ、サンプル取得に失敗します。QUICでは、クライアント接続で順序が入れ替わった、QUICパケットの数を返します。TCPでは、クライアント接続について、カーネルが測定したreorderingカウンターを返します。サーバー接続を確立していない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fc_retrans: integer クライアント接続について、カーネルが測定したretransmitsカウンターを返します。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

<a id="entry-7-3-3-fc-rtt-integer"></a>

**`fc_rtt(<unit>): integer`**

```haproxy
fc_rtt(<unit>): integer
```

接続がTCPでもQUICでもなければ、サンプル取得に失敗します。QUICでは、クライアント接続の平滑化した往復時間を返します。TCPでは、クライアント接続について、カーネルが測定した往復時間 (RTT) を返します。`<unit>` は省略可能で、デフォルトの単位はミリ秒です。`<unit>` には、ミリ秒を表す "ms"、またはマイクロ秒を表す "us" を指定できます。サーバー接続を確立していない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

<a id="entry-7-3-3-fc-rttvar-integer"></a>

**`fc_rttvar(<unit>): integer`**

```haproxy
fc_rttvar(<unit>): integer
```

接続がTCPでもQUICでもなければ、サンプル取得に失敗します。QUICでは、クライアント接続の平滑化した往復時間の分散を返します。TCPでは、クライアント接続について、カーネルが測定した往復時間 (RTT) の分散を返します。`<unit>` は省略可能で、デフォルトの単位はミリ秒です。`<unit>` には、ミリ秒を表す "ms"、またはマイクロ秒を表す "us" を指定できます。サーバー接続を確立していない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fc_sacked: integer クライアント接続について、カーネルが測定したsackedカウンターを返します。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fc_saved_syn: binary 着信接続の確立中に、システムが保存したSYNパケットのコピーを返します。"bind" 行に "tcp-ss" オプションがあり、Linuxカーネルが4.3以上である必要があります。"tcp-ss" が1の場合、IPヘッダーとTCPヘッダーだけが含まれます。"tcp-ss" が2の場合、IPヘッダーの前にEthernetヘッダーも含まれ、たとえば、送信元MACアドレスやVLANの制御やログ記録に使用できます。SYNの保存を保証するものではない点に注意してください。たとえば、SYN Cookieを使用する場合、SYNパケットは保存せず、一致するACKパケットによって接続を確立します。また、システムは、最初の読み取り後まで、コピーを保持することを保証しません。そのため、"tcp-request connection" ルールで、"sess" スコープの変数にコピーし、その後の操作では、その変数だけを使用することを強く推奨します。ループバックインターフェイスでは、システムがダミーの14バイトのEthernetヘッダーを作成する点にも注意してください。送信元と宛先のアドレスは両方ともゼロで、プロトコルだけを設定します。デバッグ時には、"hex" コンバーターを使用して、このようなサンプルを16進数に変換すると便利です。例（以下では、フィールドを手動で分け、コメントを付けています）:

```shell
frontend test
    mode http
    bind :::4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain \
                 lf-string "%[var(sess.syn),hex]\n"

$ curl '0:4445'
000000000000 000000000000 0800 \  # MAC_DST MAC_SRC PROTO=IPv4
4500003C0A65400040063255       \  # IPv4 header, proto=6 (TCP)
7F000001 7F000001              \  # IP_SRC=127.0.0.1 IP_DST=127.0.0.1
E1F2 115D 01AF4E3E 00000000    \  # TCP_SPORT=57842 TCP_DPORT=4445, SEQ
A0 02 FFD7 FE300000            \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65495
0204FFD70402080A01C2A71A0000000001030307 # MSS=65495, TS, SACK, WSCALE 7

$ curl '[::1]:4445'
000000000000 000000000000 86DD   \ # MAC_DST MAC_SRC PROTO=IPv6
6008018F00280640                 \ # IPv6 header, proto=6 (TCP)
00000000000000000000000000000001 \ # SRC=::1
00000000000000000000000000000001 \ # DST=::1
9758 115D B5511F5D 00000000      \ # TCP_SPORT=38744 TCP_DPORT=4445, SEQ
A0 02 FFC4 00300000              \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65476
0204FFC40402080A9C231D680000000001030307 # MSS=65476, TS, SACK, WSCALE 7
```

"bytes()" コンバーターは、パケットから特定のフィールドを抽出するのに役立ちます。be2dec()も、データの一部を読み取り、整数の形式で出力できます。より正確な抽出については、"eth.XXX" コンバーターを参照してください。

IPv4入力の例：

```shell
frontend test
    mode http
    bind :4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain lf-string \
                 "mac_dst=%[var(sess.syn),eth.dst,hex] \
                  mac_src=%[var(sess.syn),eth.src,hex] \
                  proto=%[var(sess.syn),eth.proto,bytes(6),be2hex(,2)] \
                  ipv4h=%[var(sess.syn),eth.data,bytes(0,12),hex] \
                  ipv4_src=%[var(sess.syn),eth.data,ip.src] \
                  ipv4_dst=%[var(sess.syn),eth.data,ip.dst] \
                  tcp_spt=%[var(sess.syn),eth.data,ip.data,tcp.src] \
                  tcp_dpt=%[var(sess.syn),eth.data,ip.data,tcp.dst] \
                  tcp_win=%[var(sess.syn),eth.data,ip.data,tcp.win] \
                  tcp_opt=%[var(sess.syn),eth.data,ip.data,bytes(20),hex]\n"

$ curl '0:4445'
mac_dst=000000000000 mac_src=000000000000 proto=0800 \
ipv4h=4500003CC9B7400040067302 ipv4_src=127.0.0.1 ipv4_dst=127.0.0.1 \
tcp_spt=43970 tcp_dpt=4445 tcp_win=65495 \
tcp_opt=0204FFD70402080A01DC0D410000000001030307
```

"set-var" アクションと、"be2dec"、"bytes"、"hex"、"eth.XXX"、"ip.XXX"、"tcp.XXX" コンバーターも参照してください。

fc_settings_streams_limit: integer フロントエンド接続で許可する、ストリーム数の上限を返します。TCPとHTTP/1.1の接続では、常に1です。ほかのプロトコルでは、クライアントとネゴシエートした設定によって決まります。

fc_src: ip クライアント側の接続の、元の送信元IPアドレスです。"tcp-request connection" ルールだけが、このアドレスを変更できます。詳細は "src" を参照してください。

fc_src_is_local: boolean 着信接続の送信元アドレスが、システムのローカルアドレスならtrue、システムに存在しないアドレスならfalseを返します。詳細は "src_is_local" を参照してください。

fc_src_port: integer クライアント側の接続の送信元TCPポートを、整数で返します。"tcp-request connection" ルールだけが、このアドレスを変更できます。詳細は "src-port" を参照してください。

fc_unacked: integer クライアント接続について、カーネルが測定したunackedカウンターを返します。サーバー接続を確立していない場合、接続がTCPではない場合、または、2.4より前のLinuxカーネルなど、OSがTCP_INFOに対応していない場合は、サンプル取得に失敗します。

fe_client_timeout: integer 現在のフロントエンドのクライアントタイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。

fe_defbe: string フロントエンドのデフォルトのバックエンド名を含む、文字列を返します。フロントエンドで、デフォルトではどのバックエンドがリクエストを処理するかを、確認するために使用できます。

fe_id: integer 現在のフロントエンドのIDを含む、整数を返します。バックエンドで、どのフロントエンドから呼び出されたかを確認したり、同じフロントエンドを経由するすべてのユーザーを、同じサーバーに固定したりするために使用できます。

fe_name: string 現在のフロントエンドの名前を含む、文字列を返します。バックエンドで、どのフロントエンドから呼び出されたかを確認したり、同じフロントエンドを経由するすべてのユーザーを、同じサーバーに固定したりするために使用できます。

fe_tarpit_timeout: integer 現在のフロントエンドのtarpitタイムアウトについて、設定値をミリ秒単位で返します。このタイムアウトは、"set-timeout" ルールで上書きできます。

req.bytes_in: integer クライアントから受信したバイト数を返します。値は、HAProxyが受信したデータに対応し、一部のヘッダーと、内部エンコーディングのオーバーヘッドを含みます。リクエストの圧縮は、ここで報告する値に影響しません。

req.bytes_out: integer サーバーへ送信したバイト数を返します。値は、HAProxyが送信したデータに対応し、一部のヘッダーと、内部エンコーディングのオーバーヘッドを含みます。リクエストの圧縮は、ここで報告する値に影響します。

res.bytes_in: integer サーバーから受信したバイト数を返します。値は、HAProxyが受信したデータに対応し、一部のヘッダーと、内部エンコーディングのオーバーヘッドを含みます。レスポンスの圧縮は、ここで報告する値に影響しません。

res.bytes_out: integer クライアントへ送信したバイト数を返します。値は、HAProxyが送信したデータに対応し、一部のヘッダーと、内部エンコーディングのオーバーヘッドを含みます。レスポンスの圧縮は、ここで報告する値に影響します。

res.timer.data: integer レスポンスのペイロードを、最後のバイトまでクライアントへ送信する、合計転送時間です。HTTPでは、レスポンスの最後のヘッダーの後（Trの後）から始まります。log-formatの%Tdに相当し、ミリ秒 (ms) 単位で報告します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

<a id="entry-7-3-3-sc-bytes-in-rate-integer"></a>

**`sc_bytes_in_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_in_rate(<ctr>[,<table>]): integer
sc0_bytes_in_rate([<table>]): integer
sc1_bytes_in_rate([<table>]): integer
sc2_bytes_in_rate([<table>]): integer
```

現在追跡しているカウンターから、クライアントからサーバーへの、平均バイト転送速度を返します。テーブルで設定した期間のバイト数で測定します。"table_bytes_in_rate" も参照してください。

<a id="entry-7-3-3-sc-bytes-out-rate-integer"></a>

**`sc_bytes_out_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_out_rate(<ctr>[,<table>]): integer
sc0_bytes_out_rate([<table>]): integer
sc1_bytes_out_rate([<table>]): integer
sc2_bytes_out_rate([<table>]): integer
```

現在追跡しているカウンターから、サーバーからクライアントへの、平均バイト転送速度を返します。テーブルで設定した期間のバイト数で測定します。"table_bytes_out_rate" も参照してください。

<a id="entry-7-3-3-sc-clr-gpc-integer"></a>

**`sc_clr_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc(<idx>,<ctr>[,<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブル `<table>` で、ID `<ctr>` の追跡カウンターに関連付けられた配列の、インデックス `<idx>` にある汎用カウンターをクリアし、それまでの値を返します。`<idx>` は0から99まで、`<ctr>` は0から2までの整数です。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは常にゼロを返します。この取得関数は、'gpc' 配列のdata_typeだけに適用します（従来の 'gpc0' や 'gpc1' のdata_typeには適用しません）。

<a id="entry-7-3-3-sc-clr-gpc0-integer"></a>

**`sc_clr_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc0(<ctr>[,<table>]): integer
sc0_clr_gpc0([<table>]): integer
sc1_clr_gpc0([<table>]): integer
sc2_clr_gpc0([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、最初の汎用カウンターをクリアし、それまでの値を返します。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは常にゼロを返します。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます。

例：

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 5
acl save  sc0_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-clr-gpc1-integer"></a>

**`sc_clr_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc1(<ctr>[,<table>]): integer
sc0_clr_gpc1([<table>]): integer
sc1_clr_gpc1([<table>]): integer
sc2_clr_gpc1([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、2番目の汎用カウンターをクリアし、それまでの値を返します。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは常にゼロを返します。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます。

<a id="entry-7-3-3-sc-conn-cnt-integer"></a>

**`sc_conn_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cnt(<ctr>[,<table>]): integer
sc0_conn_cnt([<table>]): integer
sc1_conn_cnt([<table>]): integer
sc2_conn_cnt([<table>]): integer
```

現在追跡しているカウンターから、着信接続の累積数を返します。"table_conn_cnt" も参照してください。

<a id="entry-7-3-3-sc-conn-cur-integer"></a>

**`sc_conn_cur(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cur(<ctr>[,<table>]): integer
sc0_conn_cur([<table>]): integer
sc1_conn_cur([<table>]): integer
sc2_conn_cur([<table>]): integer
```

同じ追跡カウンターを追跡している、現在の同時接続数を返します。追跡を開始すると自動的に増え、終了すると減ります。"table_conn_cur" も参照してください。

<a id="entry-7-3-3-sc-conn-rate-integer"></a>

**`sc_conn_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_rate(<ctr>[,<table>]): integer
sc0_conn_rate([<table>]): integer
sc1_conn_rate([<table>]): integer
sc2_conn_rate([<table>]): integer
```

現在追跡しているカウンターから、平均接続レートを返します。テーブルで設定した期間内の接続数で測定します。"table_conn_rate" も参照してください。

<a id="entry-7-3-3-sc-get-gpc-integer"></a>

**`sc_get_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc(<idx>,<ctr>[,<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブル `<table>` で、ID `<ctr>` の現在追跡しているカウンターに関連付けられたGPC配列の、インデックス `<idx>` にある汎用カウンターの値を返します。`<idx>` は0から99まで、`<ctr>` は0から2までの整数です。このインデックスにgpcが格納されていなければ、ゼロを返します。この取得関数は、'gpc' 配列のdata_typeだけに適用します（従来の 'gpc0' や 'gpc1' のdata_typeには適用しません）。"table_gpc" と "sc_inc_gpc" も参照してください。

<a id="entry-7-3-3-sc-get-gpc0-integer"></a>

**`sc_get_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc0(<ctr>[,<table>]): integer
sc0_get_gpc0([<table>]): integer
sc1_get_gpc0([<table>]): integer
sc2_get_gpc0([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、最初の汎用カウンターの値を返します。"table_gpc0" と sc/sc0/sc1/sc2_inc_gpc0 も参照してください。

<a id="entry-7-3-3-sc-get-gpc1-integer"></a>

**`sc_get_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc1(<ctr>[,<table>]): integer
sc0_get_gpc1([<table>]): integer
sc1_get_gpc1([<table>]): integer
sc2_get_gpc1([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、2番目の汎用カウンターの値を返します。"table_gpc1" と sc/sc0/sc1/sc2_inc_gpc1 も参照してください。

<a id="entry-7-3-3-sc-get-gpt-integer"></a>

**`sc_get_gpt(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt(<idx>,<ctr>[,<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブル `<table>` で、ID `<ctr>` の追跡カウンターに関連付けられた配列の、インデックス `<idx>` にある最初の汎用タグの値を返します。`<idx>` は0から99まで、`<ctr>` は0から2までの整数です。このインデックスにGPTが格納されていなければ、ゼロを返します。この取得関数は、'gpt' 配列のdata_typeだけに適用します（従来の 'gpt0' のdata-typeには適用しません）。"table_gpt" も参照してください。

<a id="entry-7-3-3-sc-get-gpt0-integer"></a>

**`sc_get_gpt0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt0(<ctr>[,<table>]): integer
sc0_get_gpt0([<table>]): integer
sc1_get_gpt0([<table>]): integer
sc2_get_gpt0([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、最初の汎用タグの値を返します。"table_gpt0" も参照してください。

<a id="entry-7-3-3-sc-glitch-cnt-integer"></a>

**`sc_glitch_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_cnt(<ctr>[,<table>]): integer
sc0_glitch_cnt([<table>]): integer
sc1_glitch_cnt([<table>]): integer
sc2_glitch_cnt([<table>]): integer
```

現在追跡しているカウンターに関連付けられた接続で観測した、フロント側接続の異常の累積数を返します。通常、これらの異常によって、リクエストや接続が中止されるため、返却値は過去の接続に対応することがよくあります。良い値や悪い値という基準はありませんが、品質の低いクライアントでは、接続ごとに、時折いくつかの異常が発生することがあります。一方、極端に不正なクライアントや悪意のあるクライアントでは、接続で、短時間に何千ものイベントが追加されることがあります。現在の接続に影響する異常の数については fc_glitches、送信元ごとの参照については src_glitch_cnt、イベントレートの測定については sc_glitch_rate も参照してください。

<a id="entry-7-3-3-sc-glitch-rate-integer"></a>

**`sc_glitch_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_rate(<ctr>[,<table>]): integer
sc0_glitch_rate([<table>]): integer
sc1_glitch_rate([<table>]): integer
sc2_glitch_rate([<table>]): integer
```

現在追跡しているカウンターについて、フロント側接続の異常を観測した平均レートを返します。テーブルで設定した期間内のイベント数で測定します。通常、これらの異常によって、リクエストや接続が中止されるため、返却値は過去の接続に関係することがよくあります。良い値や悪い値という基準はありませんが、品質の低いクライアントでは、接続ごとに、時折いくつかの異常が発生することがあるため、通常は低いレートが想定されます。ただし、極端に不正なクライアントや悪意のあるクライアントでは、接続ごとに、短時間に何千ものイベントが追加され、高いレートが続くことがあります。"table_glitch_rate" と "sc_glitch_cnt" も参照してください。

<a id="entry-7-3-3-sc-gpc-rate-integer"></a>

**`sc_gpc_rate(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_gpc_rate(<idx>,<ctr>[,<table>]): integer
```

現在のプロキシのテーブル、または指定したスティックテーブル `<table>` で、ID `<ctr>` の追跡カウンターに関連付けられた配列の、インデックス `<idx>` にある汎用カウンターの、平均増加レートを返します。設定した期間内に、gpcカウンターが増加した頻度を報告します。`<idx>` は0から99まで、`<ctr>` は0から2までの整数です。値を返すには、スティックテーブルに 'gpc_rate' カウンター配列を格納しておく必要があります。'gpc' が保持するのは、イベント数だけだからです。この取得関数は、'gpc_rate' 配列のdata_typeだけに適用します（従来の 'gpc0_rate' や 'gpc1_rate' のdata_typeには適用しません）。"table_gpc_rate"、"sc_get_gpc"、"sc_inc_gpc" も参照してください。

<a id="entry-7-3-3-sc-gpc0-rate-integer"></a>

**`sc_gpc0_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc0_rate(<ctr>[,<table>]): integer
sc0_gpc0_rate([<table>]): integer
sc1_gpc0_rate([<table>]): integer
sc2_gpc0_rate([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、最初の汎用カウンターの平均増加レートを返します。設定した期間内に、gpc0カウンターが増加した頻度を報告します。src_gpc0_rate、sc/sc0/sc1/sc2_get_gpc0、sc/sc0/sc1/sc2_inc_gpc0 も参照してください。値を返すには、スティックテーブルに "gpc0_rate" カウンターを格納しておく必要があります。"gpc0" が保持するのは、イベント数だけだからです。

<a id="entry-7-3-3-sc-gpc1-rate-integer"></a>

**`sc_gpc1_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc1_rate(<ctr>[,<table>]): integer
sc0_gpc1_rate([<table>]): integer
sc1_gpc1_rate([<table>]): integer
sc2_gpc1_rate([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、2番目の汎用カウンターの平均増加レートを返します。設定した期間内に、gpc1カウンターが増加した頻度を報告します。src_gpc1_rate、sc/sc0/sc1/sc2_get_gpc1、sc/sc0/sc1/sc2_inc_gpc1 も参照してください。値を返すには、スティックテーブルに "gpc1_rate" カウンターを格納しておく必要があります。"gpc1" が保持するのは、イベント数だけだからです。

<a id="entry-7-3-3-sc-http-err-cnt-integer"></a>

**`sc_http_err_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_cnt(<ctr>[,<table>]): integer
sc0_http_err_cnt([<table>]): integer
sc1_http_err_cnt([<table>]): integer
sc2_http_err_cnt([<table>]): integer
```

現在追跡しているカウンターから、HTTPエラーの累積数を返します。リクエストエラーと4xxエラーレスポンスの両方を含みます。"table_http_err_cnt" も参照してください。

<a id="entry-7-3-3-sc-http-err-rate-integer"></a>

**`sc_http_err_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_rate(<ctr>[,<table>]): integer
sc0_http_err_rate([<table>]): integer
sc1_http_err_rate([<table>]): integer
sc2_http_err_rate([<table>]): integer
```

現在追跡しているカウンターから、HTTPエラーの平均レートを返します。テーブルで設定した期間内のエラー数で測定します。リクエストエラーと4xxエラーレスポンスの両方を含みます。src_http_err_rate も参照してください。

<a id="entry-7-3-3-sc-http-fail-cnt-integer"></a>

**`sc_http_fail_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_cnt(<ctr>[,<table>]): integer
sc0_http_fail_cnt([<table>]): integer
sc1_http_fail_cnt([<table>]): integer
sc2_http_fail_cnt([<table>]): integer
```

現在追跡しているカウンターから、HTTPレスポンスの失敗の累積数を返します。レスポンスエラーと、501および505を除く5xxステータスコードの両方を含みます。"table_http_fail_cnt" も参照してください。

<a id="entry-7-3-3-sc-http-fail-rate-integer"></a>

**`sc_http_fail_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_rate(<ctr>[,<table>]): integer
sc0_http_fail_rate([<table>]): integer
sc1_http_fail_rate([<table>]): integer
sc2_http_fail_rate([<table>]): integer
```

現在追跡しているカウンターから、HTTPレスポンスの失敗の平均レートを返します。テーブルで設定した期間内の失敗数で測定します。レスポンスエラーと、501および505を除く5xxステータスコードの両方を含みます。"table_http_fail_rate" も参照してください。

<a id="entry-7-3-3-sc-http-req-cnt-integer"></a>

**`sc_http_req_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_cnt(<ctr>[,<table>]): integer
sc0_http_req_cnt([<table>]): integer
sc1_http_req_cnt([<table>]): integer
sc2_http_req_cnt([<table>]): integer
```

現在追跡しているカウンターから、HTTPリクエストの累積数を返します。有効かどうかにかかわらず、開始したすべてのリクエストを含みます。src_http_req_cnt も参照してください。

<a id="entry-7-3-3-sc-http-req-rate-integer"></a>

**`sc_http_req_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_rate(<ctr>[,<table>]): integer
sc0_http_req_rate([<table>]): integer
sc1_http_req_rate([<table>]): integer
sc2_http_req_rate([<table>]): integer
```

現在追跡しているカウンターから、HTTPリクエストの平均レートを返します。テーブルで設定した期間内のリクエスト数で測定します。有効かどうかにかかわらず、開始したすべてのリクエストを含みます。src_http_req_rate も参照してください。

<a id="entry-7-3-3-sc-inc-gpc-integer"></a>

**`sc_inc_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc(<idx>,<ctr>[,<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブル `<table>` で、ID `<ctr>` の指定した追跡カウンターに関連付けられた配列の、インデックス `<idx>` にある汎用カウンターを増加させ、新しい値を返します。`<idx>` は0から99まで、`<ctr>` は0から2までの整数です。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは値を1に増やし、1を返します。この取得関数は、'gpc' 配列のdata_typeだけに適用します（従来の 'gpc0' や 'gpc1' のdata_typeには適用しません）。

<a id="entry-7-3-3-sc-inc-gpc0-integer"></a>

**`sc_inc_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc0(<ctr>[,<table>]): integer
sc0_inc_gpc0([<table>]): integer
sc1_inc_gpc0([<table>]): integer
sc2_inc_gpc0([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、最初の汎用カウンターを増加させ、新しい値を返します。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは値を1に増やし、1を返します。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます：

例：

```text
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-inc-gpc1-integer"></a>

**`sc_inc_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc1(<ctr>[,<table>]): integer
sc0_inc_gpc1([<table>]): integer
sc1_inc_gpc1([<table>]): integer
sc2_inc_gpc1([<table>]): integer
```

現在追跡しているカウンターに関連付けられた、2番目の汎用カウンターを増加させ、新しい値を返します。最初の呼び出し前に格納している値はゼロなので、最初の呼び出しは値を1に増やし、1を返します。通常は、式の2番目のACLとして使用し、最初のACLを満たした場合に、接続へ印を付けます。

<a id="entry-7-3-3-sc-kbytes-in-integer"></a>

**`sc_kbytes_in(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_in(<ctr>[,<table>]): integer
sc0_kbytes_in([<table>]): integer
sc1_kbytes_in([<table>]): integer
sc2_kbytes_in([<table>]): integer
```

現在追跡しているカウンターから、クライアントからサーバーへのデータの合計量を、キロバイト単位で返します。現在、テストは32ビット整数で行うため、値の上限は4テラバイトです。"table_kbytes_in" も参照してください。

<a id="entry-7-3-3-sc-kbytes-out-integer"></a>

**`sc_kbytes_out(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_out(<ctr>[,<table>]): integer
sc0_kbytes_out([<table>]): integer
sc1_kbytes_out([<table>]): integer
sc2_kbytes_out([<table>]): integer
```

現在追跡しているカウンターから、サーバーからクライアントへのデータの合計量を、キロバイト単位で返します。現在、テストは32ビット整数で行うため、値の上限は4テラバイトです。"table_kbytes_out" も参照してください。

sc_key(`<ctr>`): any sc0_key: any sc1_key: any sc2_key: any 現在追跡しているカウンターとの照合に使用するキーを返します。

<a id="entry-7-3-3-sc-sess-cnt-integer"></a>

**`sc_sess_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_cnt(<ctr>[,<table>]): integer
sc0_sess_cnt([<table>]): integer
sc1_sess_cnt([<table>]): integer
sc2_sess_cnt([<table>]): integer
```

現在追跡しているカウンターから、セッションへ移行した着信接続の累積数を返します。これは、"tcp-request connection" ルールで受け入れた接続を意味します。クライアントとの接続でHTTPキープアライブを使用する場合、各接続から多くのバックエンドセッションが生じることがあるため、バックエンドでは、接続数よりも多くのセッションを数える場合があります。"table_sess_cnt" も参照してください。

<a id="entry-7-3-3-sc-sess-rate-integer"></a>

**`sc_sess_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_rate(<ctr>[,<table>]): integer
sc0_sess_rate([<table>]): integer
sc1_sess_rate([<table>]): integer
sc2_sess_rate([<table>]): integer
```

現在追跡しているカウンターから、平均セッションレートを返します。テーブルで設定した期間内のセッション数で測定します。セッションとは、初期の "tcp-request connection" ルールを通過した接続です。クライアントとの接続でHTTPキープアライブを使用する場合、各接続から多くのバックエンドセッションが生じることがあるため、バックエンドでは、接続数よりも多くのセッションを数える場合があります。"table_sess_rate" も参照してください。

<a id="entry-7-3-3-sc-tracked-boolean"></a>

**`sc_tracked(<ctr>[,<table>]): boolean`**

```haproxy
sc_tracked(<ctr>[,<table>]): boolean
sc0_tracked([<table>]): boolean
sc1_tracked([<table>]): boolean
sc2_tracked([<table>]): boolean
```

指定したセッションカウンターを、現在のセッションが現在追跡していれば、trueを返します。サーバーへ渡すヘッダーに、値を設定するかどうかを判断するときに便利です。

<a id="entry-7-3-3-sc-trackers-integer"></a>

**`sc_trackers(<ctr>[,<table>]): integer`**

```haproxy
sc_trackers(<ctr>[,<table>]): integer
sc0_trackers([<table>]): integer
sc1_trackers([<table>]): integer
sc2_trackers([<table>]): integer
```

同じ追跡カウンターを追跡している、現在の同時接続数を返します。追跡を開始すると自動的に増え、終了すると減ります。sc0_conn_curとは異なり、格納した情報を使用せず、テーブルの参照カウント（CLIで "show table" を実行すると返される "use" の値）を使用します。このため、レイヤー7の追跡に、より適している場合があります。たとえば、特定のアドレスからの同時接続数を、サーバーへ通知するために使用できます。

so_id: integer 現在のリスニングソケットのIDを含む整数を返します。多数の "bind" 行があるフロントエンドや、同じソケットを経由するすべてのユーザーを、同じサーバーに固定する場合に便利です。

so_name: string "bind" 行のnameで定義した、現在のリスニングソケットの名前を含む文字列を返します。so_idと同じ目的に使用できますが、整数の代わりに文字列を使用します。

src: ip セッションのクライアントの送信元IPアドレスです。どのtcp/httpルールでも、このアドレスを変更できます。IP型で、IPv4とIPv6の両方のテーブルで使用できます。IPv6テーブルでは、RFC 4291に従い、IPv4アドレスを対応するIPv6アドレスにマッピングします。使用するのは、TCPレベルの送信元アドレスであり、プロキシの背後にあるクライアントのアドレスではない点に注意してください。ただし、bindディレクティブ "accept-proxy" または "accept-netscaler-cip" を使用する場合、実際のアドレスを参照する "tcp-request connection" を除くすべてのルールセットでは、別のPROXYプロトコル対応コンポーネントの背後にあるクライアントのアドレスになることがあります。着信接続が、接続追跡を伴うアドレス変換やリダイレクトを通過した場合、リダイレクト前の元の宛先アドレスを報告します。Linuxシステムでは、nf_conntrack_tcp_loose sysctlを設定していると、送信元と宛先がまれに逆に見えることがあります。遅れて届いたレスポンスが、タイムアウトした接続を再び開き、送信元と宛先と認識する対象を入れ替えることがあるためです。

例：

```shell
# add an HTTP header in requests with the originating address' country
http-request set-header X-Country %[src,map_ip(geoip.lst)]
```

<a id="entry-7-3-3-src-bytes-in-rate-integer"></a>

**`src_bytes_in_rate([<table>]): integer`**

```haproxy
src_bytes_in_rate([<table>]): integer
```

"table_bytes_in_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_bytes_in_rate([`<table>`])

<a id="entry-7-3-3-src-bytes-out-rate-integer"></a>

**`src_bytes_out_rate([<table>]): integer`**

```haproxy
src_bytes_out_rate([<table>]): integer
```

"table_bytes_out_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_bytes_out_rate([`<table>`])

<a id="entry-7-3-3-src-clr-gpc-integer"></a>

**`src_clr_gpc(<idx>[,<table>]): integer`**

```haproxy
src_clr_gpc(<idx>[,<table>]): integer
```

"table_clr_gpc" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_clr_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-clr-gpc0-integer"></a>

**`src_clr_gpc0([<table>]): integer`**

```haproxy
src_clr_gpc0([<table>]): integer
```

"table_clr_gpc0" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_clr_gpc0([`<table>`])

<a id="entry-7-3-3-src-clr-gpc1-integer"></a>

**`src_clr_gpc1([<table>]): integer`**

```haproxy
src_clr_gpc1([<table>]): integer
```

"table_clr_gpc1" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_clr_gpc1([`<table>`])

<a id="entry-7-3-3-src-conn-cnt-integer"></a>

**`src_conn_cnt([<table>]): integer`**

```haproxy
src_conn_cnt([<table>]): integer
```

"table_conn_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_conn_cnt([`<table>`])

<a id="entry-7-3-3-src-conn-cur-integer"></a>

**`src_conn_cur([<table>]): integer`**

```haproxy
src_conn_cur([<table>]): integer
```

"table_conn_cur" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_conn_cur([`<table>`])

<a id="entry-7-3-3-src-conn-rate-integer"></a>

**`src_conn_rate([<table>]): integer`**

```haproxy
src_conn_rate([<table>]): integer
```

"table_conn_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_conn_rate([`<table>`])

<a id="entry-7-3-3-src-get-gpc-integer"></a>

**`src_get_gpc(<idx>[,<table>]): integer`**

```haproxy
src_get_gpc(<idx>[,<table>]): integer
```

"table_gpc" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpc0-integer"></a>

**`src_get_gpc0([<table>]): integer`**

```haproxy
src_get_gpc0([<table>]): integer
```

"table_gpc0" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc0([`<table>`])

<a id="entry-7-3-3-src-get-gpc1-integer"></a>

**`src_get_gpc1([<table>]): integer`**

```haproxy
src_get_gpc1([<table>]): integer
```

"table_gpc1" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc1([`<table>`])

<a id="entry-7-3-3-src-get-gpt-integer"></a>

**`src_get_gpt(<idx>[,<table>]): integer`**

```haproxy
src_get_gpt(<idx>[,<table>]): integer
```

"table_gpt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpt(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpt0-integer"></a>

**`src_get_gpt0([<table>]): integer`**

```haproxy
src_get_gpt0([<table>]): integer
```

"table_gpt0" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpt0([`<table>`])

<a id="entry-7-3-3-src-glitch-cnt-integer"></a>

**`src_glitch_cnt([<table>]): integer`**

```haproxy
src_glitch_cnt([<table>]): integer
```

"table_glitch_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_glitch_cnt([`<table>`])

<a id="entry-7-3-3-src-glitch-rate-integer"></a>

**`src_glitch_rate([<table>]): integer`**

```haproxy
src_glitch_rate([<table>]): integer
```

"table_glitch_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_glitch_rate([`<table>`])

<a id="entry-7-3-3-src-gpc-rate-integer"></a>

**`src_gpc_rate(<idx>[,<table>]): integer`**

```haproxy
src_gpc_rate(<idx>[,<table>]): integer
```

"table_gpc_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc_rate(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-gpc0-rate-integer"></a>

**`src_gpc0_rate([<table>]): integer`**

```haproxy
src_gpc0_rate([<table>]): integer
```

"table_gpc0_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc0_rate([`<table>`])

<a id="entry-7-3-3-src-gpc1-rate-integer"></a>

**`src_gpc1_rate([<table>]): integer`**

```haproxy
src_gpc1_rate([<table>]): integer
```

"table_gpc1_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_gpc1_rate([`<table>`])

<a id="entry-7-3-3-src-http-err-cnt-integer"></a>

**`src_http_err_cnt([<table>]): integer`**

```haproxy
src_http_err_cnt([<table>]): integer
```

"table_http_err_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_err_cnt([`<table>`])

<a id="entry-7-3-3-src-http-err-rate-integer"></a>

**`src_http_err_rate([<table>]): integer`**

```haproxy
src_http_err_rate([<table>]): integer
```

"table_http_err_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_err_rate([`<table>`])

<a id="entry-7-3-3-src-http-fail-cnt-integer"></a>

**`src_http_fail_cnt([<table>]): integer`**

```haproxy
src_http_fail_cnt([<table>]): integer
```

"table_http_fail_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_fail_cnt([`<table>`])

<a id="entry-7-3-3-src-http-fail-rate-integer"></a>

**`src_http_fail_rate([<table>]): integer`**

```haproxy
src_http_fail_rate([<table>]): integer
```

"table_http_fail_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_fail_rate([`<table>`])

<a id="entry-7-3-3-src-http-req-cnt-integer"></a>

**`src_http_req_cnt([<table>]): integer`**

```haproxy
src_http_req_cnt([<table>]): integer
```

"table_http_req_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_req_cnt([`<table>`])

<a id="entry-7-3-3-src-http-req-rate-integer"></a>

**`src_http_req_rate([<table>]): integer`**

```haproxy
src_http_req_rate([<table>]): integer
```

"table_http_req_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_http_req_rate([`<table>`])

<a id="entry-7-3-3-src-inc-gpc-integer"></a>

**`src_inc_gpc(<idx>[,<table>]): integer`**

```haproxy
src_inc_gpc(<idx>[,<table>]): integer
```

"src_inc_gpc" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_inc_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-inc-gpc0-integer"></a>

**`src_inc_gpc0([<table>]): integer`**

```haproxy
src_inc_gpc0([<table>]): integer
```

"src_inc_gpc0" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_inc_gpc0([`<table>`])

<a id="entry-7-3-3-src-inc-gpc1-integer"></a>

**`src_inc_gpc1([<table>]): integer`**

```haproxy
src_inc_gpc1([<table>]): integer
```

"src_inc_gpc1" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_inc_gpc1([`<table>`])

src_is_local: boolean 着信接続の送信元アドレスが、システムのローカルアドレスならtrue、システムに存在しないアドレス、つまりリモートマシンからの接続ならfalseを返します。UNIXアドレスは、ローカルとみなす点に注意してください。クライアントの接続元に応じて、アクセス制限を適用するときに便利です（たとえば、リモートマシンには認証やhttpsを要求する場合）。このチェックは、いくつかのシステムコールを伴うので、接続ごとに1回だけ実行することを推奨します。

<a id="entry-7-3-3-src-kbytes-in-integer"></a>

**`src_kbytes_in([<table>]): integer`**

```haproxy
src_kbytes_in([<table>]): integer
```

"table_kbytes_in" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_kbytes_in([`<table>`])

<a id="entry-7-3-3-src-kbytes-out-integer"></a>

**`src_kbytes_out([<table>]): integer`**

```haproxy
src_kbytes_out([<table>]): integer
```

"table_kbytes_out" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_kbytes_out([`<table>`])

src_port: integer クライアント側の接続のTCP送信元ポートに対応する整数値を返します。これは、クライアントが接続元として使用したポートです。どのtcp/httpルールでも、このアドレスを変更できます。現在のプロトコルでは、送信元ポートをあまり重視しないため、この関数の用途は非常に限られます。

<a id="entry-7-3-3-src-sess-cnt-integer"></a>

**`src_sess_cnt([<table>]): integer`**

```haproxy
src_sess_cnt([<table>]): integer
```

"table_sess_cnt" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_sess_cnt([`<table>`])

<a id="entry-7-3-3-src-sess-rate-integer"></a>

**`src_sess_rate([<table>]): integer`**

```haproxy
src_sess_rate([<table>]): integer
```

"table_sess_rate" コンバーターと同じですが、キーには着信接続の送信元アドレスを使用します。

次と同等です： src,table_sess_rate([`<table>`])

<a id="entry-7-3-3-src-updt-conn-cnt-integer"></a>

**`src_updt_conn_cnt([<table>]): integer`**

```haproxy
src_updt_conn_cnt([<table>]): integer
```

現在のプロキシのスティックテーブル、または指定したスティックテーブルで、着信接続の送信元アドレスに対応するエントリーを作成または更新します。このテーブルは、"conn_cnt" データ型を格納するように設定しておく必要があります。そうでなければ、マッチングを無視します。現在のカウントを1増やし、有効期限のタイマーを更新します。更新後のカウントを返すため、このマッチングはゼロを返すことはありません。これは、送信元アドレスに基づいて、サービスを濫用する利用者を拒否するために使用していました。注意： 代わりに、"tcp-request" ルールで、より機能が充実した "track-sc\*" アクションを使用することを推奨します。

例：

```shell
# This frontend limits incoming SSH connections to 3 per 10 second for
# each source address, and rejects excess connections until a 10 second
# silence is observed. At most 20 addresses are tracked.
listen ssh
    bind :22
    mode tcp
    maxconn 100
    stick-table type ip size 20 expire 10s store conn_cnt
    tcp-request content reject if { src_updt_conn_cnt gt 3 }
    server local 127.0.0.1:22
```

srv_id: integer レスポンスを処理するときに、サーバーのIDを含む整数を返します。ほぼACLでのみ使用しますが、ログ記録やデバッグにも使用できます。また、tcp-checkやhttp-checkのルールセットでも使用できます。

srv_name: string レスポンスを処理するときに、サーバーの名前を含む文字列を返します。ほぼACLでのみ使用しますが、ログ記録やデバッグにも使用できます。また、tcp-checkやhttp-checkのルールセットでも使用できます。

txn.conn_retries: integer このストリームが、サーバーへの接続を試みた際に経験した、接続の再試行回数を返します。接続を完全に確立するまでは、この値は変わる可能性があります。HTTP接続では、レイヤー7の再試行が、この値に影響することがあります。

txn.redispatched: boolean "option redispatch" の設定に従い、再試行時に接続の再振り分けが発生した場合、trueを返します。接続を完全に確立するまでは、この値は変わる可能性があります。HTTP接続では、レイヤー7の再試行が、この値に影響することがあります。

### 7.3.4. レイヤー5でのサンプル取得 {#section-7-3-4}

レイヤー5は通常、セッション層そのものを指します。HAProxyでは、接続のすべてのハンドシェイクを終え、まだコンテンツを利用できない段階のセッションに、最も近い概念です。ここで説明する取得メソッドは、後で得られる情報を必要としない限り、早ければ "tcp-request content" ルールセットから使用できます。通常は、SSLネゴシエーションの結果などを含みます。

この節のサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                       出力型
-------------------------------------------------+-------------
51d.all(<prop>[,<prop>*])                          string
bs.aborted                                         boolean
bs.debug_str([<bitmap>])                           string
bs.id                                              integer
bs.rst_code                                        integer
fs.aborted                                         boolean
fs.debug_str([<bitmap>])                           string
fs.id                                              integer
fs.rst_code                                        integer
ssl_bc                                             boolean
ssl_bc_alg_keysize                                 integer
ssl_bc_alpn                                        string
ssl_bc_cipher                                      string
ssl_bc_client_early_traffic_secret                 string
ssl_bc_client_handshake_traffic_secret             string
ssl_bc_client_random                               binary
ssl_bc_client_traffic_secret_0                     string
ssl_bc_curve                                       string
ssl_bc_early_exporter_secret                       string
ssl_bc_err                                         integer
ssl_bc_err_str                                     string
ssl_bc_exporter_secret                             string
ssl_bc_is_resumed                                  boolean
ssl_bc_npn                                         string
ssl_bc_protocol                                    string
ssl_bc_server_handshake_traffic_secret             string
ssl_bc_server_random                               binary
ssl_bc_server_traffic_secret_0                     string
ssl_bc_session_id                                  binary
ssl_bc_session_key                                 binary
ssl_bc_sni                                         string
ssl_bc_unique_id                                   binary
ssl_bc_use_keysize                                 integer
ssl_c_ca_err                                       integer
ssl_c_ca_err_depth                                 integer
ssl_c_chain_der                                    binary
ssl_c_der                                          binary
ssl_c_err                                          integer
ssl_c_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_key_alg                                      string
ssl_c_notafter                                     string
ssl_c_notbefore                                    string
ssl_c_r_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_san                                          string
ssl_c_serial                                       binary
ssl_c_sha1                                         binary
ssl_c_sig_alg                                      string
ssl_c_used                                         boolean
ssl_c_verify                                       integer
ssl_c_version                                      integer
ssl_f_der                                          binary
ssl_f_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_key_alg                                      string
ssl_f_notafter                                     string
ssl_f_notbefore                                    string
ssl_f_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_serial                                       binary
ssl_f_sha1                                         binary
ssl_f_sig_alg                                      string
ssl_f_version                                      integer
ssl_fc                                             boolean
ssl_fc_alg_keysize                                 integer
ssl_fc_alpn                                        string
ssl_fc_cipher                                      string
ssl_fc_cipherlist_bin([<filter_option>])           binary
ssl_fc_cipherlist_hex([<filter_option>])           string
ssl_fc_cipherlist_str([<filter_option>])           string
ssl_fc_cipherlist_xxh                              integer
ssl_fc_client_early_traffic_secret                 string
ssl_fc_client_handshake_traffic_secret             string
ssl_fc_client_random                               binary
ssl_fc_client_traffic_secret_0                     string
ssl_fc_crtname                                     string
ssl_fc_curve                                       string
ssl_fc_early_exporter_secret                       string
ssl_fc_ecformats_bin                               binary
ssl_fc_eclist_bin([<filter_option>])               binary
ssl_fc_err                                         integer
ssl_fc_err_str                                     string
ssl_fc_exporter_secret                             string
ssl_fc_extlist_bin([<filter_option>])              binary
ssl_fc_has_crt                                     boolean
ssl_fc_has_early                                   boolean
ssl_fc_has_sni                                     boolean
ssl_fc_is_resumed                                  boolean
ssl_fc_npn                                         string
ssl_fc_protocol                                    string
ssl_fc_protocol_hello_id                           integer
ssl_fc_server_handshake_traffic_secret             string
ssl_fc_server_random                               binary
ssl_fc_server_traffic_secret_0                     string
ssl_fc_session_id                                  binary
ssl_fc_session_key                                 binary
ssl_fc_sigalgs_bin([<filter_option>])              binary
ssl_fc_sni                                         string
ssl_fc_supported_versions_bin([<filter_option>])   binary
ssl_fc_unique_id                                   binary
ssl_fc_use_keysize                                 integer
ssl_s_chain_der                                    binary
ssl_s_der                                          binary
ssl_s_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_key_alg                                      string
ssl_s_notafter                                     string
ssl_s_notbefore                                    string
ssl_s_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_serial                                       binary
ssl_s_sha1                                         binary
ssl_s_sig_alg                                      string
ssl_s_version                                      integer
txn.timer.user                                     integer
-------------------------------------------------+-------------
```

詳細一覧：

<a id="entry-7-3-4-51d-all-string"></a>

**`51d.all(<prop>[,<prop>*]): string`**

```haproxy
51d.all(<prop>[,<prop>*]): string
```

要求したプロパティーの値を、文字列で返します。値は、"51degrees-property-separator" で指定した区切り文字で区切ります。リクエスト内の重要なHTTPヘッダーをすべて使用して、デバイスを識別します。この関数には、最大5つのプロパティー名を渡すことができ、プロパティー名が見つからない場合は、値 "NoData" を返します。

例：

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request
# containing the three properties requested using all relevant headers from
# the request.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[51d.all(DeviceType,IsMobile,IsTablet)]
```

bs.aborted: boolean 現在のストリームについて、サーバーから中止を受信した場合はtrue、それ以外はfalseを返します。

<a id="entry-7-3-4-bs-debug-str-string"></a>

**`bs.debug_str([<bitmap>]): string`**

```haproxy
bs.debug_str([<bitmap>]): string
```

この関数は、開発者が複雑な問題を調査するときに使用するためのものです。バックエンドのストリームと接続の下位層から内部状態を抽出し、通常はスペースで区切った一連の "name=value" という形式の文字列にまとめます。省略可能な引数 `<bitmap>` は、情報を抽出する層を指定し、次の値の算術OR（または合計）です： - ソケット層： 16 - 接続層： 8 - トランスポート層（SSLなど）: 4 - マルチプレクサー接続： 2 - マルチプレクサーストリーム： 1

これらの値は、バージョンによって変わる可能性があります。デフォルトのゼロは特別な値で、すべての層を有効にします。本番環境の長期的な監視では、この関数の出力に依存しないでください。より詳細な情報が必要になれば、安定版ブランチ内でも変更することを想定しています。代表的な用途は、fs.debug_str()とともに、この情報をlog-formatの末尾に連結することです。例：

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

bs.id: integer サーバー側のマルチプレクサーのストリームIDを返します。適切な情報を返す責任は、マルチプレクサーにあります。

bs.rst_code: integer 現在のストリームについて、サーバーから受信したリセットコードを返します。サーバーから受信したH2 RST_STREAMフレーム、またはQUIC STOP_SENDINGフレームのコードを返します。中止を受信していない場合、またはサーバー側のストリームがH2/QUICストリームではない場合は、サンプル取得に失敗します。

fs.aborted: boolean 現在のストリームについて、クライアントから中止を受信した場合はtrue、それ以外はfalseを返します。

<a id="entry-7-3-4-fs-debug-str-string"></a>

**`fs.debug_str([<bitmap>]): string`**

```haproxy
fs.debug_str([<bitmap>]): string
```

この関数は、開発者が複雑な問題を調査するときに使用するためのものです。フロントエンドのストリームと接続の下位層から内部状態を抽出し、通常はスペースで区切った一連の "name=value" という形式の文字列にまとめます。省略可能な引数 `<bitmap>` は、情報を抽出する層を指定し、次の値の算術OR（または合計）です： - ソケット層： 16 - 接続層： 8 - トランスポート層（SSLなど）: 4 - マルチプレクサー接続： 2 - マルチプレクサーストリーム： 1

これらの値は、バージョンによって変わる可能性があります。デフォルトのゼロは特別な値で、すべての層を有効にします。本番環境の長期的な監視では、この関数の出力に依存しないでください。より詳細な情報が必要になれば、安定版ブランチ内でも変更することを想定しています。代表的な用途は、bs.debug_str()とともに、この情報をlog-formatの末尾に連結することです。例：

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

fs.id: integer クライアント側のマルチプレクサーのストリームIDを返します。適切な情報を返す責任は、マルチプレクサーにあります。たとえば、生のTCPではストリームがないため、常に0を返します。

fs.rst_code: integer 現在のストリームについて、クライアントから受信したリセットコードを返します。クライアントから受信したH2 RST_STREAMフレーム、またはQUIC STOP_SENDINGフレームのコードを返します。中止を受信していない場合、またはクライアント側のストリームがH2/QUICストリームではない場合は、サンプル取得に失敗します。

ssl_bc: boolean バック側の接続がSSL/TLSトランスポート層を使用し、ローカルで復号する場合にtrueを返します。これは、"ssl" オプションを指定したサーバーに発信接続したことを意味します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_alg_keysize: integer 発信接続がSSL/TLSトランスポート層を使用する場合に、対称暗号がサポートする鍵のサイズをビット単位で返します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_alpn: string TLSトランスポート層を使用した発信接続から、Application Layer Protocol Negotiationフィールドを抽出します。結果は、サーバーとネゴシエートしたプロトコル名を含む文字列です。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。"server" 行の "alpn" キーワードでプロトコルのリストを指定しなければ、TLS ALPN拡張を通知しない点に注意してください。また、このリストからプロトコルを選ぶことをサーバーに強制するものではなく、ほかのプロトコルを要求することもできます。TLS ALPN拡張は、TLS NPN拡張を置き換えるためのものです。"ssl_bc_npn" も参照してください。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_cipher: string 発信接続がSSL/TLSトランスポート層を使用する場合に、使用している暗号の名前を返します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_client_early_traffic_secret: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のCLIENT_EARLY_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_client_handshake_traffic_secret: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のCLIENT_HANDSHAKE_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_client_random: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、バック側の接続のクライアントランダム値を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_client_traffic_secret_0: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のCLIENT_TRAFFIC_SECRET_0を16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_curve: string 発信接続がSSL/TLSトランスポート層を使用する場合に、鍵共有に使用した曲線の名前を返します。OpenSSL \>= 3.0.0、またはAWS-LC \>= 1.57.0が必要です。

ssl_bc_early_exporter_secret: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のEARLY_EXPORTER_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_err: integer 発信接続がSSL/TLSトランスポート層を使用する場合に、バックエンド側で発生した最初のエラースタックの、最後のエラーのIDを返します。ハンドシェイクのエラーのほか、接続の存続期間中に発生した読み取りや書き込みのエラーも報告できます。このエラーコードの説明をテキストで取得するには、"ssl_bc_err_str" サンプル取得関数、または "openssl errstr" コマンド（16進表記のエラーコードを引数に取ります）を使用できます。エラーコードの完全な一覧については、使用するSSLライブラリーのドキュメントを参照してください。

ssl_bc_err_str: string 発信接続がSSL/TLSトランスポート層を使用する場合に、バックエンドの観点から接続で発生した最初のエラースタックの、最後のエラーを文字列で返します。"ssl_fc_err" も参照してください。

ssl_bc_exporter_secret: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のEXPORTER_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_is_resumed: boolean バック側の接続がSSL/TLSトランスポート層を使用し、新しく作成したSSLセッションを、キャッシュ済みのセッションまたはTLSチケットで再開した場合に、trueを返します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_npn: string TLSトランスポート層を使用した発信接続から、Next Protocol Negotiationフィールドを抽出します。結果は、サーバーとネゴシエートしたプロトコル名を含む文字列です。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。"server" 行の "npn" キーワードでプロトコルのリストを指定しなければ、TLS NPN拡張を通知しない点に注意してください。また、このリストからプロトコルを選ぶことをサーバーに強制するものではなく、ほかのプロトコルを使用することもできます。TLS NPN拡張は、ALPNに置き換えられた点に注意してください。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_protocol: string 発信接続がSSL/TLSトランスポート層を使用する場合に、使用しているプロトコルの名前を返します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_server_handshake_traffic_secret: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のSERVER_HANDSHAKE_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_server_random: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、バック側の接続のサーバーランダム値を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_server_traffic_secret_0: string 発信接続がTLS 1.3トランスポート層を使用する場合に、バック側の接続のSERVER_TRAFFIC_SECRET_0を16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_bc_session_id: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、バック側の接続のSSL IDを返します。セッションが再利用されたかどうかを確認したい場合、ログに記録すると役立ちます。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_session_key: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、バック側の接続のSSLセッションのマスター鍵を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_sni: string サーバーへの接続で使用した、Server Name Indication TLS拡張（SNI）のフィールドを取得します。結果が存在する場合、通常はHTTPSホスト名に一致する文字列（253文字以下）です。主な用途は、ログ記録とデバッグです（たとえば、接続の確立時に使用したSNIを調べ、サーバーが認識したものと照合する場合）。

ssl_bc_unique_id: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、RFC5929の[3節](https://www.rfc-editor.org/rfc/rfc5929#section-3)で定義するTLSの一意なIDを返します。このIDは、コンバーター "ssl_bc_unique_id,base64" を使用して、base64にエンコードできます。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_bc_use_keysize: integer 発信接続がSSL/TLSトランスポート層を使用する場合に、使用している対称暗号の鍵のサイズをビット単位で返します。tcp-checkやhttp-checkのルールセットでも使用できます。

ssl_c_ca_err: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアント証明書の検証中に、深さ \> 0で検出した最初のエラーのIDを返します。この検証処理でエラーが発生しなかった場合は0を返します。エラーコードの完全な一覧については、使用するSSLライブラリーのドキュメントを参照してください。

ssl_c_ca_err_depth: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアント証明書の検証中に検出した最初のエラーについて、CAチェーン内での深さを返します。エラーが発生しなかった場合は0を返します。

ssl_c_chain_der: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書チェーンをDER形式で返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。ASN.1 DERデータを受け付けるライブラリーであれば、どれでも結果を解析できます。現在、再開したセッションには対応していません。

ssl_c_der: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書をDER形式で返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

ssl_c_err: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、深さ0での検証中に検出した最初のエラーのIDを返します。この検証処理でエラーが発生しなかった場合は0を返します。エラーコードの完全な一覧については、使用するSSLライブラリーのドキュメントを参照してください。

<a id="entry-7-3-4-ssl-c-i-dn-string"></a>

**`ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string
```

着信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、クライアントが提示した証明書の発行者の完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_c_i_dn(OU,2)" は2番目の組織単位を、"ssl_c_i_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_c_i_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_c_key_alg: string 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書の鍵の生成に使用したアルゴリズム名を返します。

ssl_c_notafter: string 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した終了日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

ssl_c_notbefore: string 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した開始日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

<a id="entry-7-3-4-ssl-c-r-dn-string"></a>

**`ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string
```

着信接続がSSL/TLSトランスポート層を使用し、設定したca-fileで正常に検証した場合に、`<entry>` を指定しなければ、クライアントが提示した証明書のルートCAの完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_c_r_dn(OU,2)" は2番目の組織単位を、"ssl_c_r_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_c_r_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

<a id="entry-7-3-4-ssl-c-s-dn-string"></a>

**`ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string
```

着信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、クライアントが提示した証明書のサブジェクトの完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_c_s_dn(OU,2)" は2番目の組織単位を、"ssl_c_s_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_c_s_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_c_san: string 着信接続がSSL/TLSトランスポート層を使用し、クライアント証明書を受け取った場合に、その証明書に含まれるSubject Alt Nameフィールドを、カンマ区切りの文字列で返します。

クライアント証明書の検査に使用できます。

例：

```text
acl is_valid_client_cert ssl_c_used && ! ssl_c_verify
http-request set-header X-SSL-Client-SAN %[ssl_c_san] if is_valid_client_cert
```

次の結果になります：

```text
X-SSL-Client-SAN: IP Address:127.0.0.1, IP Address:127.0.0.2, IP Address:127.0.0.3, URI:http://docs.haproxy.org/2.7/, DNS:ca.tests.haproxy.com

```

ssl_c_serial: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書のシリアル番号を返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

ssl_c_sha1: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書のSHA-1フィンガープリントを返します。クライアントを特定のサーバーに固定したり、この情報をサーバーへ渡したりするために使用できます。出力はバイナリーなので、この署名をサーバーへ渡す場合は、次の例のように、16進数またはbase64にエンコードする必要があります：

例：

```text
http-request set-header X-SSL-Client-SHA1 %[ssl_c_sha1,hex]
```

ssl_c_sig_alg: string 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書の署名に使用したアルゴリズム名を返します。

ssl_c_used: boolean 現在のSSLセッションがクライアント証明書を使用していれば、現在の接続でSSLセッションの再開を使用している場合でも、trueを返します。"ssl_fc_has_crt" も参照してください。

ssl_c_verify: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、検証結果のエラーIDを返します。エラーが発生しなかった場合はゼロを返します。エラーコードの完全な一覧については、使用するSSLライブラリーのドキュメントを参照してください。

ssl_c_version: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、クライアントが提示した証明書のバージョンを返します。

ssl_f_der: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書をDER形式で返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

<a id="entry-7-3-4-ssl-f-i-dn-string"></a>

**`ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string
```

着信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、フロントエンドが提示した証明書の発行者の完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_f_i_dn(OU,2)" は2番目の組織単位を、"ssl_f_i_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_f_i_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_f_key_alg: string 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書の鍵の生成に使用したアルゴリズム名を返します。

ssl_f_notafter: string 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した終了日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

ssl_f_notbefore: string 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した開始日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

<a id="entry-7-3-4-ssl-f-s-dn-string"></a>

**`ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string
```

着信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、フロントエンドが提示した証明書のサブジェクトの完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_f_s_dn(OU,2)" は2番目の組織単位を、"ssl_f_s_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_f_s_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_f_serial: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書のシリアル番号を返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

ssl_f_sha1: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書のSHA-1フィンガープリントを返します。SNIによって、どの証明書を選択したかを確認するために使用できます。

ssl_f_sig_alg: string 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書の署名に使用したアルゴリズム名を返します。

ssl_f_version: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンドが提示した証明書のバージョンを返します。

ssl_fc: boolean フロント側の接続がSSL/TLSトランスポート層を使用し、ローカルで復号する場合にtrueを返します。これは、"ssl" オプションを指定した "bind" 行で宣言したソケットに一致したことを意味します。

例：

```shell
# This passes "X-Proto: https" to servers when client connects over SSL
listen http-https
    bind :80
    bind :443 ssl crt /etc/haproxy.pem
    http-request add-header X-Proto https if { ssl_fc }
```

ssl_fc_alg_keysize: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、対称暗号がサポートする鍵のサイズをビット単位で返します。

ssl_fc_alpn: string TLSトランスポート層を使用し、HAProxyがローカルで復号する着信接続から、Application Layer Protocol Negotiationフィールドを抽出します。結果は、クライアントが通知したプロトコル名を含む文字列です。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。"bind" 行の "alpn" キーワードでプロトコルのリストを指定しなければ、TLS ALPN拡張を通知しない点に注意してください。また、このリストからプロトコルを選ぶことをクライアントに強制するものではなく、ほかのプロトコルを要求することもできます。TLS ALPN拡張は、TLS NPN拡張を置き換えるためのものです。"ssl_fc_npn" も参照してください。

ssl_fc_cipher: string 着信接続がSSL/TLSトランスポート層を使用する場合に、使用している暗号の名前を返します。

<a id="entry-7-3-4-ssl-fc-cipherlist-bin-binary"></a>

**`ssl_fc_cipherlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_cipherlist_bin([<filter_option>]): binary
```

Client Helloの暗号リストを、バイナリー形式で返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値：

```text
0: 暗号スイートの完全なリストを返します（デフォルト）
1: 出力からGREASE（RFC8701）の値を除外します
```

例：

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-cipherlist-hex-string"></a>

**`ssl_fc_cipherlist_hex([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_hex([<filter_option>]): string
```

Client Helloの暗号リストのバイナリー形式を、16進数にエンコードして返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値：

```text
0: 暗号スイートの完全なリストを返します（デフォルト）
1: 出力からGREASE（RFC8701）の値を除外します
```

<a id="entry-7-3-4-ssl-fc-cipherlist-str-string"></a>

**`ssl_fc_cipherlist_str([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_str([<filter_option>]): string
```

Client Helloの暗号リストを、デコードしたテキスト形式で返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値：

```text
0: 暗号スイートの完全なリストを返します（デフォルト）
1: 出力からGREASE（RFC8701）の値を除外します
```

このサンプル取得関数は、OpenSSL \>= 1.0.2でのみ使用できます。この機能が有効でない場合は、"ssl_fc_cipherlist_xxh" と同様にハッシュを返します。

ssl_fc_cipherlist_xxh: integer 暗号リストのxxh64を返します。"tune.ssl.capture-buffer-size" の値を0より大きく設定している場合にのみ、このハッシュを返せます。ただし、ハッシュの計算では、暗号リストのすべてのデータを考慮します。

ssl_fc_client_early_traffic_secret: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のCLIENT_EARLY_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_client_handshake_traffic_secret: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のCLIENT_HANDSHAKE_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_client_random: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロント側の接続のクライアントランダム値を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。

ssl_fc_client_traffic_secret_0: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のCLIENT_TRAFFIC_SECRET_0を16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_crtname: string 着信SSL/TLS接続で選択した証明書の名前を返します。これは、"show ssl cert" に表示する名前です。設定内での証明書の宣言方法によって、相対パスまたは絶対パスを含むファイル名の場合と、別名の場合があります。

例：

```text
crt-store example
    load crt "example.com.pem"

frontend www
    bind *:443 ssl crt "@example/example.com.pem"
    acl match_certificate ssl_fc_crtname -m beg -i "@example/"
    http-request set-header X-Cert-Name %[ssl_fc_crtname] if match_certificate
```

ssl_fc_curve: string 着信接続がSSL/TLSトランスポート層を使用する場合に、鍵共有に使用した曲線の名前を返します。OpenSSL \>= 3.0.0が必要です。

ssl_fc_early_rcvd: boolean 接続上で早期データを観測した場合、その後にハンドシェイクが完了したかどうかにかかわらず、trueを返します。トラフィックの処理には実用的な用途がありませんが、クライアントが0-RTTを使用して早期データを送信したことを確認する、ほぼ唯一の方法であり、デバッグに役立つ場合があります。ほかの方法は、ネットワークトラフィックをキャプチャーするか、フロント側の接続のフラグをログに記録して、コードと照合することだけだからです。クライアントの機能に関する統計を得るためにも役立つ場合があります。"ssl_fc_has_early" も参照してください。

ssl_fc_early_exporter_secret: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のEARLY_EXPORTER_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_ecformats_bin: binary Client Helloで示す、対応する楕円曲線の点の形式を、バイナリー形式で返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。

例：

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-eclist-bin-binary"></a>

**`ssl_fc_eclist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_eclist_bin([<filter_option>]): binary
```

Client Helloで示す、対応する楕円曲線を、バイナリー形式で返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値：

```text
0: サポートする楕円曲線の完全なリストを返します（デフォルト）
1: 出力からGREASE（RFC8701）の値を除外します
```

例：

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_err: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンド側で発生した最初のエラースタックの、最後のエラーのIDを返します。エラーが発生しなかった場合は0を返します。検証以外のハンドシェイク関連のエラー（暗号の不一致など）や、接続の存続期間中に発生する読み取りや書き込みのエラーを識別するために使用できます。クライアント証明書の検証処理で発生したエラーは、この取得関数では報告せず、既存の "ssl_c_err"、"ssl_c_ca_err"、"ssl_c_ca_err_depth" 取得関数で報告します。このエラーコードの説明をテキストで取得するには、"ssl_fc_err_str" サンプル取得関数、または "openssl errstr" コマンド（16進表記のエラーコードを引数に取ります）を使用できます。エラーコードの完全な一覧については、使用するSSLライブラリーのドキュメントを参照してください。

ssl_fc_err_str: string 着信接続がSSL/TLSトランスポート層を使用する場合に、フロントエンド側で発生した最初のエラースタックの、最後のエラーを文字列で返します。クライアント証明書の検証処理で発生したエラーは、この取得関数では報告しません。"ssl_fc_err" も参照してください。

ssl_fc_exporter_secret: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のEXPORTER_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

<a id="entry-7-3-4-ssl-fc-extlist-bin-binary"></a>

**`ssl_fc_extlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_extlist_bin([<filter_option>]): binary
```

Client Helloの拡張リストを、バイナリー形式で返します。返却値の長さの上限は、"tune.ssl.capture-buffer-size" 設定で制御する、共有キャプチャーバッファーのサイズによって制限します。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値：

```text
0: 拡張の完全なリストを返します（デフォルト）
1: 出力からGREASE（RFC8701）の値を除外します
```

例：

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_has_crt: boolean SSL/TLSトランスポート層を使用する着信接続に、クライアント証明書が存在する場合にtrueを返します。'verify' 文を 'optional' に設定している場合に便利です。注意： Session IDまたはTLSチケットを使ってSSLセッションを再開する場合、現在の接続にはクライアント証明書が存在しませんが、キャッシュやチケットから取得できることがあります。そのため、現在のSSLセッションがクライアント証明書を使用しているかどうかを確認するには、"ssl_c_used" の使用を推奨します。

ssl_fc_has_early: boolean 早期データを送信し、まだハンドシェイクを完了していない場合にtrueを返します。セキュリティーに影響するため、このようなデータを拒否したり、"wait-for-handshake" アクションでハンドシェイクの完了を待ったりするのに便利です。"ssl_fc_early_rcvd" も参照してください。

ssl_fc_has_sni: boolean SSL/TLSトランスポート層を使用する着信接続に、Server Name Indication TLS拡張（SNI）が存在するかを確認します。着信接続にTLS SNIフィールドがある場合にtrueを返します。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。

ssl_fc_is_resumed: boolean SSL/TLSトランスポート層を使用する着信接続で、SSLセッションキャッシュまたはTLSチケットを使用してSSL/TLSセッションを再開した場合にtrueを返します。

ssl_fc_npn: string TLSトランスポート層を使用し、HAProxyがローカルで復号する着信接続から、Next Protocol Negotiationフィールドを抽出します。結果は、クライアントが通知したプロトコル名を含む文字列です。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。"bind" 行の "npn" キーワードでプロトコルのリストを指定しなければ、TLS NPN拡張を通知しない点に注意してください。また、このリストからプロトコルを選ぶことをクライアントに強制するものではなく、ほかのプロトコルを要求することもできます。TLS NPN拡張は、ALPNに置き換えられた点に注意してください。

ssl_fc_protocol: string 着信接続がSSL/TLSトランスポート層を使用する場合に、使用しているプロトコルの名前を返します。

ssl_fc_protocol_hello_id: integer Client Helloメッセージで示す、クライアントがセッション中の通信に使用したいTLSプロトコルのバージョンです。"tune.ssl.capture-buffer-size" の値を0より大きく設定している場合にのみ、この値を返せます。

例：

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_server_handshake_traffic_secret: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のSERVER_HANDSHAKE_TRAFFIC_SECRETを16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_server_random: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロント側の接続のサーバーランダム値を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。

ssl_fc_server_traffic_secret_0: string 着信接続がTLS 1.3トランスポート層を使用する場合に、フロント側の接続のSERVER_TRAFFIC_SECRET_0を16進文字列で返します。OpenSSL \>= 1.1.1が必要です。これは、SSLKEYLOGFILEを生成するために、OpenSSLのkeylogコールバックが出力する鍵の1つです。グローバルセクションで "tune.ssl.keylog on" を指定し、SSLの鍵のログ記録を有効にしておく必要があります。"tune.ssl.keylog" も参照してください。

ssl_fc_session_id: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロント側の接続のSSL IDを返します。特定のクライアントをサーバーに固定するのに役立ちます。ブラウザーによっては、数分ごとにセッションIDを更新する点に注意してください。

ssl_fc_session_key: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、フロント側の接続のSSLセッションのマスター鍵を返します。一時鍵を使う暗号で送信したトラフィックを復号するのに役立ちます。OpenSSL \>= 1.1.0、またはBoringSSLが必要です。

<a id="entry-7-3-4-ssl-fc-sigalgs-bin-binary"></a>

**`ssl_fc_sigalgs_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_sigalgs_bin([<filter_option>]): binary
```

Client Helloで提示したsignatures_algorithms (13) TLS拡張の内容を返します。TLSのRFCで定義する、2バイトのアルゴリズムのバイナリーリストを提供します： <https://datatracker.ietf.org/doc/html/rfc8446#section-4.2.3>。

"tune.ssl.capture-buffer-size" の値を0より大きく設定している場合にのみ、この値を返せます。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値： 0: 暗号の完全なリストを返します（デフォルト） 1: 出力からGREASE (RFC8701) の値を除外します

ssl_fc_sni: string SSL/TLSトランスポート層を使用し、HAProxyがローカルで復号する着信接続から、Server Name Indication TLS拡張（SNI）のフィールドを抽出します。結果が存在する場合、通常はHTTPSホスト名に一致する文字列（253文字以下）です。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。

この取得関数は、前述の "req.ssl_sni" とは異なり、SSLの内容をそのまま転送する接続ではなく、HAProxyが復号する接続に適用します。後述の "ssl_fc_sni_end" と "ssl_fc_sni_reg" も参照してください。SSLライブラリーは、TLS拡張のサポートを有効にしてビルドしておく必要があります（haproxy -vvで確認してください）。

注意！ ごく特殊な条件を除き、通常、このフィールドをHTTPの "Host" ヘッダーフィールドの代わりに使用するのは適切ではありません。たとえば、HTTPS接続をサーバーへ転送する場合、SNIフィールドは、フロント側のSNIの値からではなく、"req.hdr(host)" を使用して、HTTP Hostヘッダーフィールドから設定する必要があります。SNIは、サーバー側が提示する証明書の選択にのみ使用し、クライアントは、その証明書に含まれる名前に一致する限り、異なるHostの値を持つリクエストを送信できるためです。そのため、バックエンドがTCPモードで動作する場合を除き、通常は、"ssl_fc_sni" をサーバーの "sni" キーワードの引数に使用すべきではありません。

派生ACL:

```text
ssl_fc_sni_end: 接尾辞の照合
ssl_fc_sni_reg: 正規表現の照合
```

<a id="entry-7-3-4-ssl-fc-supported-versions-bin-binary"></a>

**`ssl_fc_supported_versions_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_supported_versions_bin([<filter_option>]): binary
```

Client Helloで提示したsupported_versions (43) TLS拡張の内容を返します。2バイトのバージョンのバイナリーリストを提供します。TLSv1.3 (0x0304)、TLSv1.2 (0x0303) です。

"tune.ssl.capture-buffer-size" の値を0より大きく設定している場合にのみ、この値を返せます。`<filter_option>` を設定すると、返すデータをフィルターできます。指定できる値： 0: 暗号の完全なリストを返します（デフォルト） 1: 出力からGREASE (RFC8701) の値を除外します

ssl_fc_unique_id: binary 着信接続がSSL/TLSトランスポート層を使用する場合に、RFC5929の[3節](https://www.rfc-editor.org/rfc/rfc5929#section-3)で定義するTLSの一意なIDを返します。このIDは、コンバーター "ssl_fc_unique_id,base64" を使用して、base64にエンコードできます。

ssl_fc_use_keysize: integer 着信接続がSSL/TLSトランスポート層を使用する場合に、使用している対称暗号の鍵のサイズをビット単位で返します。

ssl_s_chain_der: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書チェーンをDER形式で返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。ASN.1 DERデータを受け付けるライブラリーであれば、どれでも結果を解析できます。現在、再開したセッションには対応していません。

ssl_s_der: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書をDER形式で返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

<a id="entry-7-3-4-ssl-s-i-dn-string"></a>

**`ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string
```

発信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、サーバーが提示した証明書の発行者の完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_s_i_dn(OU,2)" は2番目の組織単位を、"ssl_s_i_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_s_i_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_s_key_alg: string 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書の鍵の生成に使用したアルゴリズム名を返します。

ssl_s_notafter: string 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した終了日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

ssl_s_notbefore: string 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した開始日時を、YYMMDDhhmmss[Z]形式の文字列で返します。

<a id="entry-7-3-4-ssl-s-s-dn-string"></a>

**`ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string
```

発信接続がSSL/TLSトランスポート層を使用する場合に、`<entry>` を指定しなければ、サーバーが提示した証明書のサブジェクトの完全な識別名を返します。指定した場合は、そのエントリーをDNの先頭から検索し、最初に見つかったエントリーの値を返します。省略可能な2番目の引数として出現番号を指定すると、正の場合はDNの先頭から、負の場合は末尾から数えてn番目の、指定したエントリーの値を返します。たとえば、"ssl_s_s_dn(OU,2)" は2番目の組織単位を、"ssl_s_s_dn(CN)" はコモンネームを取得します。`<format>` パラメーターを使用すると、各プロトコルで使用するのに適したDNを取得できます。現在は、LDAP v3向けのrfc2253に対応しています。形式だけを変更したい場合は、最初の2つのパラメーターに、空文字列とゼロを指定できます。例： ssl_s_s_dn(,0,rfc2253) 要求したエントリーのASN.1値（`<entry>` を指定しなかった場合は、DN内のいずれかのエントリー）に、後続のデータを伴う埋め込みNULバイトがあると、不正な形式とみなし、データを返しません。

ssl_s_serial: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書のシリアル番号を返します。ACLで使用する場合、照合する値は16進形式で渡すことができます。

ssl_s_sha1: binary 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書のSHA-1フィンガープリントを返します。SNIによって、どの証明書を選択したかを確認するために使用できます。

ssl_s_sig_alg: string 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書の署名に使用したアルゴリズム名を返します。

ssl_s_version: integer 発信接続がSSL/TLSトランスポート層を使用する場合に、サーバーが提示した証明書のバージョンを返します。

txn.timer.user: integer アイドル時間を除き、プロキシが受け入れた時点から、両端を閉じた時点までの、クライアントから見た合計推定時間です。log-formatの%Tuに相当し、ミリ秒 (ms) 単位で報告します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

### 7.3.5. バッファーの内容からのサンプル取得（レイヤー6） {#section-7-3-5}

バッファーの内容からのサンプル取得は、上記の取得方法とは少し異なります。取得対象のデータが一時的なものだからです。このデータは、存在する間しか使用できず、転送すると失われます。そのため、たとえば、リクエスト中にバッファーの内容から取得したサンプルを、レスポンスで使用することはできません。データは、取得している最中にも変わる可能性があります。必要なデータが完全に揃い、使用できるようにするため、たとえばTCPリクエストの内容検査で、待ち時間を設定したり、複数のサンプル取得メソッドを組み合わせたりする必要がある場合があります。詳しくは、"tcp-request content" キーワードを参照してください。

警告： 次のサンプル取得関数は、HTTPプロキシで使用すると無視されます。これらは、バッファー内の生の内容だけを扱います。一方、HTTPプロキシは構造化した内容を使用するため、そのデータの生の表現には意味がありません。ACLが次のサンプル取得関数のいずれかに依存していれば、警告を出します。ただし、不正な使用をすべて検出できるわけではありません（カスタムログ形式やサンプル式の中で使用する場合など）。注意してください。

この節のサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                          出力型
----------------------------------------------------+-------------
distcc_body(<token>[,<occ>])                          binary
distcc_param(<token>[,<occ>])                         integer
payload(<offset>,<length>)                            binary
payload_lv(<offset1>,<length>[,<offset2>])            binary
rdp_cookie([<name>])                                  string
rdp_cookie_cnt([name])                                integer
rep_ssl_hello_type                                    integer
req.len                                               integer
req.payload(<offset>,<length>)                        binary
req.payload_lv(<offset1>,<length>[,<offset2>])        binary
req.proto_http                                        boolean
req.rdp_cookie([<name>])                              string
req.rdp_cookie_cnt([name])                            integer
req.ssl_alpn                                          string
req.ssl_cipherlist                                    binary
req.ssl_ec_ext                                        boolean
req.ssl_hello_type                                    integer
req.ssl_keyshare_groups                               binary
req.ssl_sigalgs                                       binary
req.ssl_sni                                           string
req.ssl_st_ext                                        integer
req.ssl_supported_groups                              binary
req.ssl_ver                                           integer
req_len                                               integer
req_proto_http                                        boolean
req_ssl_hello_type                                    integer
req_ssl_sni                                           string
req_ssl_ver                                           integer
res.len                                               integer
res.payload(<offset>,<length>)                        binary
res.payload_lv(<offset1>,<length>[,<offset2>])        binary
res.ssl_hello_type                                    integer
----------------------------------------------------+-------------
```

詳細一覧：

<a id="entry-7-3-5-distcc-body-binary"></a>

**`distcc_body(<token>[,<occ>]): binary`**

```haproxy
distcc_body(<token>[,<occ>]): binary
```

distccメッセージを解析し、トークン `<token>` の出現番号 \#`<occ>` に対応するボディーを返します。出現番号は1から始まります。指定しなければ、どの出現箇所にも一致できますが、現在の実装では、最初の出現箇所だけを確認します。HAProxyを経由してdistccでビルドするファイルから、ファイル名や引数を抽出するために使用できます。対応するトークンの完全な一覧については、distccのプロトコルのドキュメントを参照してください。

<a id="entry-7-3-5-distcc-param-integer"></a>

**`distcc_param(<token>[,<occ>]): integer`**

```haproxy
distcc_param(<token>[,<occ>]): integer
```

distccメッセージを解析し、トークン `<token>` の出現番号 \#`<occ>` に対応するパラメーターを返します。出現番号は1から始まります。指定しなければ、どの出現箇所にも一致できますが、現在の実装では、最初の出現箇所だけを確認します。HAProxyを経由してdistccでビルドするファイルから、プロトコルのバージョン、ファイルサイズ、引数などの情報を抽出するために使用できます。ほかの用途として、アイドル状態の接続を保持しないよう、前処理済みのファイルの内容が始まるまで待ってから、サーバーに接続することもできます。対応するトークンの完全な一覧については、distccのプロトコルのドキュメントを参照してください。

例：

```shell
# wait up to 20s for the pre-processed file to be uploaded
tcp-request inspect-delay 20s
tcp-request content accept if { distcc_param(DOTI) -m found }
# send large files to the big farm
use_backend big_farm if { distcc_param(DOTI) gt 1000000 }
```

<a id="entry-7-3-5-payload-binary"></a>

**`payload(<offset>,<length>): binary (deprecated)`**

```haproxy
payload(<offset>,<length>): binary (deprecated)
```

リクエストの文脈（"stick on" や "stick match" など）で使用する場合は "req.payload" の別名であり、"stick store response" などのレスポンスの文脈で使用する場合は "res.payload" の別名です。

<a id="entry-7-3-5-payload-lv-binary"></a>

**`payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)`**

```haproxy
payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)
```

リクエストの文脈（"stick on" や "stick match" など）で使用する場合は "req.payload_lv" の別名であり、"stick store response" などのレスポンスの文脈で使用する場合は "res.payload_lv" の別名です。

req.len: integer req_len: integer (非推奨) リクエストバッファー内のバイト数に対応する整数値を返します。主にACLで使用します。バッファーが変化している間は、このテストがfalseを返さないことを理解してください。つまり、ゼロと等しいかどうかを確認すると、セッションの開始時に、ほぼ常に即座に一致します。一方、より多くのデータを求めるテストでは、そのデータが届くのを待ち、それ以上データが届かないとHAProxyが確信した場合にのみ、falseを返します。このテストは、TCPリクエストの内容検査で使用するために設計しています。

<a id="entry-7-3-5-req-payload-binary"></a>

**`req.payload(<offset>,<length>): binary`**

```haproxy
req.payload(<offset>,<length>): binary
```

リクエストバッファーの、バイト位置 `<offset>` から始まる、`<length>` バイトのバイナリーブロックを抽出します。特別な場合として、`<length>` 引数がゼロの場合は、`<offset>` から末尾までのバッファー全体を抽出します。ACLとともに使用すると、バッファー内の任意の位置に、特定の内容が存在するかを確認できます。

派生ACL:

```text
req.payload(<offset>,<length>): 16進数によるバイナリーの照合
```

<a id="entry-7-3-5-req-payload-lv-binary"></a>

**`req.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
req.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

リクエストバッファー内の、`<offset1>` の位置にある `<length>` バイトのフィールドでサイズを指定する、バイナリーブロックを抽出します。ブロックの開始位置は、`<offset2>` を指定した場合はその位置、指定しなかった場合は長さのフィールドの直後です。`<offset2>` パラメーターは、先頭に '+' または '-' 符号を付けた相対オフセットにも対応します。

派生ACL:

```text
req.payload_lv(<offset1>,<length>[,<offset2>]): 16進数によるバイナリーの照合
```

例： "stick store-response" キーワードの例を参照してください。

req.proto_http: boolean req_proto_http: boolean (非推奨) リクエストバッファー内のデータがHTTPのように見え、HTTPとして正しく解析できる場合にtrueを返します。通常のHTTPリクエストの解析と同じパーサーを使用するため、意外な結果は生じないはずです。リクエストが完了、失敗、またはタイムアウトするまでは、このテストは一致しません。TCPログでプロトコルを報告するためにも使用できますが、主な用途は、たとえばヘッダーを追跡するために、完全なHTTPリクエストがバッファーに存在するまで、TCPリクエストの解析を停止することです。

例：

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content reject if !HTTP
tcp-request content track-sc0 base table req-rate
```

<a id="entry-7-3-5-req-rdp-cookie-string"></a>

**`req.rdp_cookie([<name>]): string`**

```haproxy
req.rdp_cookie([<name>]): string
rdp_cookie([<name>]): string (deprecated)
```

リクエストバッファーがRDPプロトコルのように見える場合に、RDP Cookie `<name>` を抽出します。名前を指定しなければ、任意のCookieを抽出します。パーサーは、RDPプロトコルの仕様に示すとおり、最初のCookieだけを確認します。Cookie名の大文字と小文字は区別しません。通常は、"MSTS" というCookie名を使用します。クライアントで適切に設定すれば、サーバーへ接続するクライアントのユーザー名を格納できるためです。サーバーへのセッションの固定には、"MSTSHASH" Cookieもよく使用します。

"balance rdp-cookie" とは異なり、任意の負荷分散アルゴリズムを使用できるため、クライアントのバックエンドサーバーへの分散は、RDP Cookieのハッシュと連動しません。"balance roundrobin" や "balance leastconn" などの負荷分散アルゴリズムを使用すると、"balance rdp-cookie" のハッシュよりも、クライアントをバックエンドサーバーへ均等に分散できると考えられます。

派生ACL:

```text
req.rdp_cookie([<name>]): 文字列の完全一致
```

例：

```text
listen tse-farm
    bind 0.0.0.0:3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # Persist based on the mstshash cookie
    # This is only useful makes sense if
    # balance rdp-cookie is not used
    stick-table type string size 204800
    stick on req.rdp_cookie(mstshash)
    server srv1 1.1.1.1:3389
    server srv1 1.1.1.2:3389
```

"balance rdp-cookie"、"persist rdp-cookie"、"tcp-request"、"req.rdp_cookie" ACLも参照してください。

<a id="entry-7-3-5-req-rdp-cookie-cnt-integer"></a>

**`req.rdp_cookie_cnt([name]): integer`**

```haproxy
req.rdp_cookie_cnt([name]): integer
rdp_cookie_cnt([name]): integer (deprecated)
```

リクエストバッファーをRDPプロトコルとして解析することを試み、見つかったRDP Cookieの数に対応する整数を返します。省略可能なCookie名を渡した場合は、その名前に一致するCookieだけを対象にします。主にACLで使用します。

派生ACL:

```text
req.rdp_cookie_cnt([<name>]): 整数の照合
```

req.ssl_alpn: string クライアントがSSL ClientHelloメッセージ内で送信した、Application-Layer Protocol Negotiation（ALPN）TLS拡張 (RFC7301) の値を含む文字列を返します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。次の例のように、TLSクライアントのALPNの優先設定に基づいて、ACLでルーティングを判断する場合に便利です。"ssl_fc_alpn" も参照してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_acme if { req.ssl_alpn acme-tls/1 }
default_backend bk_default
```

<a id="entry-7-3-5-req-ssl-cipherlist-binary"></a>

**`req.ssl_cipherlist binary`**

```haproxy
req.ssl_cipherlist binary
```

TLS ClientHelloの内容で報告する、クライアントが対応する対称暗号の選択肢のリストを、バイナリー形式で返します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。"ssl" オプションを指定した場合に使用できる、SSL bind用の同等の取得関数 "ssl_fc_cipherlist_bin" を参照してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_cipherlist,be2hex(:,2),lower -m sub 1302:009f }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ec_ext: boolean クライアントがSSL ClientHelloメッセージ内で、RFC4492の[5.1節](https://www.rfc-editor.org/rfc/rfc4492#section-5.1)で定義するSupported Elliptic Curves Extensionを送信したかどうかを、ブール値で返します。同じIPアドレスで、ECC対応のクライアントにはEC証明書を提示し、それ以外のすべてのクライアントにはRSAを使用するために利用できます。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

req.ssl_hello_type: integer req_ssl_hello_type: integer (非推奨) リクエストバッファーに、完全なSSL（v3以上）のClient Helloメッセージとして解析できるデータが含まれている場合、そのバッファー内のSSL Helloメッセージの型を含む整数値を返します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。主にACLで、接続先の固定に使用できるSSLセッションIDを含むと想定する、SSL Helloメッセージの存在を検出するために使用します。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

<a id="entry-7-3-5-req-ssl-keyshare-groups-binary"></a>

**`req.ssl_keyshare_groups binary`**

```haproxy
req.ssl_keyshare_groups binary
```

TLS ClientHelloで報告する、クライアントが対応する鍵交換用の暗号パラメーターのリストを、バイナリー形式で返します。TLS v1.3では、keyshareはClientHelloメッセージの一部で、最後のClient Hello拡張です。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_keyshare_groups,be2hex(:,2),lower -m sub 001d  }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

<a id="entry-7-3-5-req-ssl-sigalgs-binary"></a>

**`req.ssl_sigalgs binary`**

```haproxy
req.ssl_sigalgs binary
```

TLS ClientHelloで報告する、クライアントが対応する署名アルゴリズムのリストを、バイナリー形式で返します。この情報は、Client Hello拡張として提供します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。"ssl" オプションを指定した場合に使用できる、SSL bind用の同等の取得関数 "ssl_fc_sigalgs_bin" を参照してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe4 if { req.ssl_sigalgs,be2hex(:,2),lower -m sub 0403:0805 }
server fe4  ${htst_fe4_addr}:${htst_fe4_port}
```

req.ssl_sni: string req_ssl_sni: string (非推奨) リクエストバッファーに、完全なSSL（v3以上）のClient Helloメッセージとして解析できるデータが含まれている場合、バッファーを通過するTLSストリームでクライアントが送信した、Server Name TLS拡張の値を含む文字列を返します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。HTTPS (443)、IMAPS (993)、SMTPS (465) など、実際に暗黙的なTLSを使用するプロトコルでのみ機能し、SMTP (25/587) やIMAP (143) など、明示的なTLSを使用するプロトコルでは機能しません。最近のブラウザーでは、SNIは通常、クライアントが接続しようとするホストの名前を含みます。このテストは、TCPリクエストの内容検査で使用するために設計しています。内容に応じた振り分けが必要な場合は、次の例のように、まず完全なClient Hello（型1）を待つことを推奨します。"ssl_fc_sni" も参照してください。後述の理由（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）により、この取得関数の返却値は、特定のホストへのアクセスの許可や拒否を単独で判断するには、信頼性が不十分な点に注意してください。

この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。クライアントが同じTCPストリーム内で複数のClientHelloメッセージを送信する場合でも、最初のClientHelloが持つSNIだけを返し、それ以降のClientHelloの内容はすべて無視します。このような送信は、たとえば、サーバーがTLS 1.3の処理の一部としてHelloRetryRequest (HRR) を要求した場合や、クライアントがTLSの再ネゴシエーションを開始した場合に発生します。再ネゴシエーションでは、同じTCPストリーム内で後から新しいClientHelloを送信し、異なるSNIを含むことがあります。

Encrypted Client Hello (ECH) を使用する場合、通信路上で見えるClientHelloは、実際の暗号化した "Inner" ClientHelloを埋め込んだ、"Outer" ClientHelloだけです。この場合、この取得関数が抽出するSNIは、Outer ClientHelloのSNIであり、おとりのSNIです。クライアントが実際に到達したいホストではありません。現在、この取得関数は、Inner ClientHelloを復号することも解析することもできません。そのため、ECHを使用する場合、ルーティングやアクセス制御の判断を、この取得関数に依存させてはいけません。

派生ACL:

```text
req.ssl_sni: 文字列の完全一致
```

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_allow if { req.ssl_sni -f allowed_sites }
default_backend bk_sorry_page
```

req.ssl_st_ext: integer クライアントがSessionTicket TLS拡張 (RFC5077) を送信しなかった場合は0を返します。クライアントがSessionTicket TLS拡張を送信した場合は1を返します。クライアントが、長さがゼロではないTLS SessionTicketも送信した場合は2を返します。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。たとえば、クライアントがSessionTicketを送信したかどうかを検出し、それに応じて接続先を固定するために使用できます。SessionTicketがなければSessionIDに基づいて固定します。あるいは、SessionTicketを使用する場合はサーバー側に状態が存在しないため、固定しないようにできます。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

<a id="entry-7-3-5-req-ssl-supported-groups-binary"></a>

**`req.ssl_supported_groups binary`**

```haproxy
req.ssl_supported_groups binary
```

TLS ClientHelloで報告する、クライアントが対応するグループのリストを、バイナリー形式で返します。これらのグループは鍵交換に使用し、楕円曲線を使用する鍵交換と、使用しない鍵交換の両方を含むことがあります。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。"ssl" オプションを指定した場合に使用できる、SSL bind用の同等の取得関数 "ssl_fc_eclist_bin" を参照してください。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

例：

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_supported_groups, be2hex(:,2),lower -m sub 0017 }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ver: integer req_ssl_ver: integer (非推奨) リクエストバッファー内のストリームの、SSL/TLSプロトコルのバージョンを含む整数値を返します。SSLv2 HelloメッセージとSSLv3メッセージの両方に対応します。TLSv1はSSLバージョン3.1として通知します。値は、メジャーバージョンに65536を掛け、マイナーバージョンを加えたものです。リクエストバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "bind" 行では機能しない点に注意してください。このテストのACL版は、MAJOR.MINOR形式の10進表記（3.1など）と照合します。この取得関数は主にACLで使用します。この取得関数が解析するのは、リクエストバッファー内で見つかった最初のClientHelloメッセージだけです。この制限による影響（HelloRetryRequest、再ネゴシエーション、Encrypted Client Hello）の詳細については、"req.ssl_sni" キーワードのドキュメントを参照してください。

派生ACL:

```text
req.ssl_ver: 小数の照合
```

res.len: integer レスポンスバッファー内のバイト数に対応する整数値を返します。主にACLで使用します。バッファーが変化している間は、このテストがfalseを返さないことを理解してください。つまり、ゼロと等しいかどうかを確認すると、ストリームの開始時に、ほぼ常に即座に一致します。一方、より多くのデータを求めるテストでは、そのデータが届くのを待ち、それ以上データが届かないとHAProxyが確信した場合にのみ、falseを返します。このテストは、TCPレスポンスの内容検査で使用するために設計しています。ただし、tcp-checkのexpectルールでも使用できます。

<a id="entry-7-3-5-res-payload-binary"></a>

**`res.payload(<offset>,<length>): binary`**

```haproxy
res.payload(<offset>,<length>): binary
```

レスポンスバッファーの、バイト位置 `<offset>` から始まる、`<length>` バイトのバイナリーブロックを抽出します。特別な場合として、`<length>` 引数がゼロの場合は、`<offset>` から末尾までのバッファー全体を抽出します。ACLとともに使用すると、バッファー内の任意の位置に、特定の内容が存在するかを確認できます。tcp-checkのexpectルールでも使用できます。

<a id="entry-7-3-5-res-payload-lv-binary"></a>

**`res.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
res.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

レスポンスバッファー内の、`<offset1>` の位置にある `<length>` バイトのフィールドでサイズを指定する、バイナリーブロックを抽出します。ブロックの開始位置は、`<offset2>` を指定した場合はその位置、指定しなかった場合は長さのフィールドの直後です。`<offset2>` パラメーターは、先頭に '+' または '-' 符号を付けた相対オフセットにも対応します。tcp-checkのexpectルールでも使用できます。

例： "stick store-response" キーワードの例を参照してください。

res.ssl_hello_type: integer rep_ssl_hello_type: integer (非推奨) レスポンスバッファーに、完全なSSL（v3以上）のHelloメッセージとして解析できるデータが含まれている場合、そのバッファー内のSSL Helloメッセージの型を含む整数値を返します。レスポンスバッファー内の生の内容だけに適用し、SSLデータ層で復号した内容には適用しないため、"ssl" オプションを指定した "server" 行では機能しない点に注意してください。主にACLで、接続先の固定に使用できるSSLセッションIDを含むと想定する、SSL Helloメッセージの存在を検出するために使用します。

### 7.3.6. HTTPサンプルの取得（レイヤー7） {#section-7-3-6}

HTTPの内容、リクエスト、レスポンスからサンプルを取得できます。このアプリケーション層は、レイヤー7とも呼びます。この節のデータを取得できるのは、それぞれのリクエストバッファーまたはレスポンスバッファーから、完全なHTTPリクエストまたはレスポンスを解析した場合だけです。HTTP専用のすべてのルールと、"mode http" で動作するセクションでは、常にこの条件を満たします。TCPの内容検査を使用する場合は、まずリクエストやレスポンスが到着できるように、検査の待ち時間を設ける必要がある場合があります。これらの取得関数は、レイヤー4の取得関数よりも、CPUリソースを少し多く必要とすることがあります。ただし、リクエストとレスポンスには索引を付けているため、大きな差はありません。

注意： tcp-request contentルールでのHTTP処理は、HTTPプロキシからであれば、すべて想定どおりに動作します。ただし、TCPプロキシからで、HTTPへのアップグレードを行っていない場合は、HTTP/1の内容に対してのみ機能します。HTTP/2の内容では、プリフェイスだけが見えます。そのため、使用できるサンプル取得関数は "req.proto_http"、"req.ver"、場合によっては "method" だけです。それ以外のレイヤー7のサンプル取得関数は、すべて失敗します。HTTPへのアップグレード後は、HTTPプロキシからの場合と同じように動作します。

この節のサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                       出力型
-------------------------------------------------+-------------
base                                               string
base32                                             integer
base32+src                                         binary
baseq                                              string
capture.req.hdr(<idx>)                             string
capture.req.method                                 string
capture.req.uri                                    string
capture.req.ver                                    string
capture.res.hdr(<idx>)                             string
capture.res.ver                                    string
cook([<name>])                                     string
cook_cnt([<name>])                                 integer
cook_val([<name>])                                 integer
cookie([<name>])                                   string
hdr([<name>[,<occ>]])                              string
hdr_cnt([<header>])                                integer
hdr_ip([<name>[,<occ>]])                           ip
hdr_val([<name>[,<occ>]])                          integer
http_auth(<userlist>)                              boolean
http_auth_bearer([<header>])                       string
http_auth_group(<userlist>)                        string
http_auth_pass                                     string
http_auth_type                                     string
http_auth_user                                     string
http_first_req                                     boolean
method                                             integer
path                                               string
pathq                                              string
query([<options>])                                 string
req.body                                           binary
req.body_len                                       integer
req.body_param([<name>[,i]])                       string
req.body_size                                      integer
req.cook([<name>])                                 string
req.cook_cnt([<name>])                             integer
req.cook_names([<delim>])                          string
req.cook_val([<name>])                             integer
req.fhdr(<name>[,<occ>])                           string
req.fhdr_cnt([<name>])                             integer
req.hdr([<name>[,<occ>]])                          string
req.hdr_cnt([<name>])                              integer
req.hdr_ip([<name>[,<occ>]])                       ip
req.hdr_names([<delim>])                           string
req.hdr_val([<name>[,<occ>]])                      integer
req.hdrs                                           string
req.hdrs_bin                                       binary
req.timer.hdr                                      integer
req.timer.idle                                     integer
req.timer.queue                                    integer
req.timer.tq                                       integer
req.ver                                            string
req_ver                                            string
request_date([<unit>])                             integer
res.body                                           binary
res.body_len                                       integer
res.body_size                                      integer
res.cache_hit                                      boolean
res.cache_name                                     string
res.comp                                           boolean
res.comp_algo                                      string
res.cook([<name>])                                 string
res.cook_cnt([<name>])                             integer
res.cook_names([<delim>])                          string
res.cook_val([<name>])                             integer
res.fhdr([<name>[,<occ>]])                         string
res.fhdr_cnt([<name>])                             integer
res.hdr([<name>[,<occ>]])                          string
res.hdr_cnt([<name>])                              integer
res.hdr_ip([<name>[,<occ>]])                       ip
res.hdr_names([<delim>])                           string
res.hdr_val([<name>[,<occ>]])                      integer
res.hdrs                                           string
res.hdrs_bin                                       binary
res.timer.hdr                                      integer
res.ver                                            string
resp_ver                                           string
scook([<name>])                                    string
scook_cnt([<name>])                                integer
scook_val([<name>])                                integer
server_status                                      integer
set-cookie([<name>])                               string
shdr([<name>[,<occ>]])                             string
shdr_cnt([<name>])                                 integer
shdr_ip([<name>[,<occ>]])                          ip
shdr_val([<name>[,<occ>]])                         integer
status                                             integer
txn.status                                         integer
txn.timer.total                                    integer
unique-id                                          string
url                                                string
url32                                              integer
url32+src                                          binary
url_ip                                             ip
url_param([<name>[,<delim>[,i]]])                  string
url_port                                           integer
urlp([<name>[,<delim>[,i]]])                       string
urlp_val([<name>[,<delim>[,i]]])                   integer
-------------------------------------------------+-------------
```

詳細一覧：

base: string 最初のHostヘッダーと、リクエストのパス部分を連結して返します。パス部分は、最初のスラッシュから始まり、疑問符の直前で終わります。仮想ホスティング環境でURLの濫用を検出したり、共有キャッシュの効率を改善したりする場合に役立ちます。サイズを制限したスティックテーブルと組み合わせると、ホストとパスごとに、最もよく要求されるオブジェクトの統計を収集することもできます。ACLでは、"[www.example.com/favicon.ico](http://www.example.com/favicon.ico)" のように、ホストとパスの両方を使った簡単な内容振り分けルールを作成できます。"path" と "uri" も参照してください。

派生ACL:

```text
base    : 文字列の完全一致
base_beg: 接頭辞の照合
base_dir: サブディレクトリの照合
base_dom: ドメインの照合
base_end: 接尾辞の照合
base_len: 長さの照合
base_reg: 正規表現の照合
base_sub: 部分文字列の照合
```

注意： 派生ACLの後にコンバーターを続けたり、"-m" パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

base32: integer 前述の "base" 取得メソッドが返す値の、32ビットのハッシュを返します。すべてのURLを保存することなく、トラフィックの多いサイトで、URLごとの活動を追跡するのに便利です。代わりに短いハッシュを保存するため、多くのメモリーを節約できます。出力型は符号なし整数です。使用するハッシュ関数はSDBMで、出力に完全なアバランシェ処理を適用します。技術的には、base32は "base,sdbm(1)" と完全に同じです。

base32+src: binary 前述のbase32取得関数と、後述のsrc取得関数の結果を連結して返します。結果の型はバイナリーで、送信元アドレスのファミリーによって、サイズは8バイトまたは20バイトです。IPとURLの組み合わせごとに、カウンターを追跡するために使用できます。

baseq: string 最初のHostヘッダーと、リクエストのクエリー文字列を含むパス部分を連結して返します。パス部分は、最初のスラッシュから始まります。"base" の代わりに使用すると、統計やキャッシュの用途で、対象のリソースを適切に識別できます。"path"、"pathq"、"base" も参照してください。

<a id="entry-7-3-6-capture-req-hdr-string"></a>

**`capture.req.hdr(<idx>): string`**

```haproxy
capture.req.hdr(<idx>): string
```

"capture request header" でキャプチャーしたヘッダーの内容を抽出します。idxは、設定内のcaptureキーワードの位置です。最初のエントリーのインデックスは0です。"capture request header" も参照してください。

capture.req.method: string HTTPリクエストのMETHODを抽出します。リクエストとレスポンスの両方で使用できます。"method" とは異なり、保存用の領域を割り当てるため、リクエストとレスポンスの両方で使用できます。

capture.req.uri: string リクエストのURIを抽出します。URIは、リクエスト内の最初のスラッシュから始まり、最初のスペースの直前で終わります（ホスト部分は含みません）。"path" や "url" とは異なり、保存用の領域を割り当てるため、リクエストとレスポンスの両方で使用できます。

capture.req.ver: string リクエストのHTTPバージョンを抽出し、"HTTP/`<major>`.`<minor>`" 形式で返します。保持される情報を使用するため、リクエスト、レスポンス、ログで使用できます。リクエストのバージョンが無効な場合、このサンプル取得は失敗します。

<a id="entry-7-3-6-capture-res-hdr-string"></a>

**`capture.res.hdr(<idx>): string`**

```haproxy
capture.res.hdr(<idx>): string
```

"capture response header" でキャプチャーしたヘッダーの内容を抽出します。idxは、設定内のcaptureキーワードの位置です。最初のエントリーのインデックスは0です。"capture response header" も参照してください。

capture.res.ver: string レスポンスのHTTPバージョンを抽出し、"HTTP/`<major>`.`<minor>`" 形式で返します。保持される情報を使用するため、ログで使用できます。レスポンスのバージョンが無効な場合、このサンプル取得は失敗します。

<a id="entry-7-3-6-cookie-string"></a>

**`cookie([<name>]): string (deprecated)`**

```haproxy
cookie([<name>]): string (deprecated)
```

リクエストの "Cookie" ヘッダー行、またはレスポンスの "Set-Cookie" ヘッダーから、Cookie名 `<name>` の最後の出現箇所を抽出し、その値を文字列で返します。代表的な用途は、同じプロファイルを共有する複数のクライアントが、同じサーバーを使用するようにすることです。"appsession" の "request-learn" 文と似たことを実現できますが、複数ピア間の同期と、再起動をまたいだ状態の保持に対応します。名前を指定しなければ、最初のCookieの値を返します。この取得関数は、使用する文脈によって方向が曖昧に決まるため、今後は使用せず、代わりにreq.cook()またはres.cook()へ置き換えるべきです。

<a id="entry-7-3-6-hdr-string"></a>

**`hdr([<name>[,<occ>]]): string`**

```haproxy
hdr([<name>[,<occ>]]): string
```

リクエストで使用する場合はreq.hdr()と、レスポンスで使用する場合はres.hdr()と同じです。詳細は、それぞれの取得関数を参照してください。取得の方向が不明な場合は、方向を明示した取得関数を使用してください。hdr()サンプル取得メソッドとは異なり、hdr\_\* ACLキーワードは、明確にリクエストヘッダーに適用する点に注意してください。

<a id="entry-7-3-6-http-auth-boolean"></a>

**`http_auth(<userlist>): boolean`**

```haproxy
http_auth(<userlist>): boolean
```

クライアントから受信した認証データが、指定したuserlistに格納したユーザー名とパスワードに一致するかどうかを、ブール値で返します。この取得関数は、ACL以外ではあまり役立ちません。現在は、HTTP Basic認証だけに対応します。

<a id="entry-7-3-6-http-auth-bearer-string"></a>

**`http_auth_bearer([<header>]): string`**

```haproxy
http_auth_bearer([<header>]): string
```

Bearer方式を使用する場合（JSON Web Tokenを送信する場合など）に、認証データ内で見つかった、クライアントが提供したトークンを返します。クライアントが送信したデータは、一切検査しません。特定の `<header>` を指定した場合は、Authorizationヘッダーの代わりに、そのヘッダーを解析します。

<a id="entry-7-3-6-http-auth-group-string"></a>

**`http_auth_group(<userlist>): string`**

```haproxy
http_auth_group(<userlist>): string
```

指定したuserlistに照らして、ユーザー名とパスワードの両方が有効な場合、クライアントから受信した認証データ内のユーザー名に対応する文字列を返します。主な用途はACLでの使用で、ユーザーがリスト内のいずれかのグループに所属しているかを確認します。この取得関数は、ACL以外ではあまり役立ちません。現在は、HTTP Basic認証だけに対応します。

派生ACL:

```text
http_auth_group(<userlist>): group ...
リクエストから抽出されたユーザーのパスワードが、指定したuserlistに照らして
有効であり、そのユーザーがグループの少なくとも一つに属する場合にtrueを返します。
```

http_auth_pass: string クライアントから受信した認証データ内のユーザーのパスワードを、Authorizationヘッダーで指定されたとおりに返します。このサンプル取得関数は、一切検査しません。Basic認証だけに対応します。

http_auth_type: string クライアントから受信した認証データ内の認証方式を、Authorizationヘッダーで指定されたとおりに返します。このサンプル取得関数は、一切検査しません。Basic認証だけに対応します。

http_auth_user: string クライアントから受信した認証データ内のユーザー名を、Authorizationヘッダーで指定されたとおりに返します。このサンプル取得関数は、一切検査しません。Basic認証だけに対応します。

http_first_req: boolean 処理中のリクエストが、その接続の最初のリクエストである場合にtrueを返します。最初のリクエストでない場合に、一部のリクエストで欠ける可能性があるヘッダーを追加または削除したり、ログでリクエストをグループ化したりするために使用できます。

method: integer + string HTTPリクエストのメソッドに対応する整数値を返します。たとえば、"GET" は1に相当します（対応関係はソースを確認してください）。値9は "other method" を意味し、ストリームから抽出した文字列に変換できます。これをサンプルとして直接使用すべきではありません。ACLからの使用だけを想定しており、ACLは、パターン内のメソッドを、これらの整数と文字列の値へ透過的に変換します。よく使うメソッドの多くは、定義済みACLですでに検査できます。

派生ACL:

```text
method: 大文字と小文字を区別しないメソッドの照合
```

例：

```shell
# only accept GET and HEAD requests
acl valid_method method GET HEAD
http-request deny if ! valid_method
```

path: string リクエストのURLパスを抽出します。パスは最初のスラッシュから始まり、疑問符の直前で終わります（ホスト部分は含みません）。代表的な用途は、プリフェッチ対応のキャッシュや、データベースから複数の情報を集約してキャッシュに保持する必要があるポータルです。外向きのキャッシュでは、代わりに "url" を使用する方が適切です。ACLでは、通常、ファイル名に完全一致させる場合（"/login.php" など）や、派生形式を使用してディレクトリー部分と照合する場合に使用します。"url" と "base" 取得メソッドも参照してください。URI内のフラグメント参照（パスの後の '#'）は、HTTP標準で厳格に禁止しており、拒否する点に注意してください。ただし、リクエストを受信するフロントエンドで "option accept-unsafe-violations-in-http-request" を指定している場合、このフラグメント部分を受け入れ、パスにも含めます。

派生ACL:

```text
path    : 文字列の完全一致
path_beg: 接頭辞の照合
path_dir: サブディレクトリの照合
path_dom: ドメインの照合
path_end: 接尾辞の照合
path_len: 長さの照合
path_reg: 正規表現の照合
path_sub: 部分文字列の照合
```

注意： 派生ACLの後にコンバーターを続けたり、"-m" パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

pathq: string クエリー文字列を含む、リクエストのURLパスを抽出します。最初のスラッシュから始まります。このサンプル取得関数は、スキームやオーソリティー部分があれば除外し、常に相対URIを取得するのに便利です。相対URIは、HTTP/1.1のリクエストターゲットで一般的な表現ですが、HTTP/2では絶対URIを使用することがよくあります。このサンプル取得関数は、どちらの場合も同じ結果を返します。URI内のフラグメント参照（パスの後の '#'）は、HTTP標準で厳格に禁止しており、拒否する点に注意してください。ただし、リクエストを受信するフロントエンドで "option accept-unsafe-violations-in-http-request" を指定している場合、このフラグメント部分を受け入れ、パスにも含めます。

<a id="entry-7-3-6-query-string"></a>

**`query([<options>]): string`**

```haproxy
query([<options>]): string
```

リクエストのクエリー文字列を抽出します。最初の疑問符の後から始まります。疑問符が存在しなければ、この取得関数は何も返しません。疑問符が存在しても、その後に何もなければ、空文字列を返します。そのため、"found" マッチングメソッドを使用すると、クエリー文字列が存在するかどうかを簡単に確認できます。この取得関数は、疑問符の直前で終わる "path" と、疑問符を含む "query_string" を補完します。

省略可能なパラメーターで、返却値をカスタマイズできます。次のオプションに対応します：

    - with_qm: クエリー文字列が空でなければ、先頭に疑問符を含めます。

req.body: binary HTTPリクエストの、利用可能なボディーをデータブロックとして返します。リクエストのボディーを、できる限り確実に待つために、"option http-buffer-request" の使用を推奨します。

req.body_len: integer HTTPリクエストの、利用可能なボディーの長さをバイト単位で返します。ボディーがバッファーより大きい場合、通知した長さより小さくなることがあります。リクエストのボディーを、できる限り確実に待つために、"option http-buffer-request" の使用を推奨します。

<a id="entry-7-3-6-req-body-param-string"></a>

**`req.body_param([<name>[,i]]): string`**

```haproxy
req.body_param([<name>[,i]]): string
```

この取得関数は、POSTリクエストのボディーがURLエンコードされていると想定します。"content-type" に "application/x-www-form-urlencoded" という値が含まれるかを、ユーザーが確認できます。ボディー内のパラメーター `<name>` の最初の出現箇所を抽出します。値は '&' の直前で終わります。2番目の引数に "i" を追加しない限り、パラメーター名の大文字と小文字を区別します。名前を指定しなければ、任意のパラメーターに一致し、最初のものを返します。結果は、リクエストボディーに記載されたとおりの、パラメーター `<name>` の値に対応する文字列です（URLデコードは行いません）。この取得関数のACL版は、複数のパラメーターを順に処理し、名前を指定しなければ、すべてのパラメーターの値を順に報告する点に注意してください。

req.body_size: integer HTTPリクエストのボディーについて、通知した長さをバイト単位で返します。通知したContent-Lengthヘッダーの値、またはチャンクエンコーディングの場合は、利用可能なデータのサイズを表します。

<a id="entry-7-3-6-req-cook-string"></a>

**`req.cook([<name>]): string`**

```haproxy
req.cook([<name>]): string
cook([<name>]): string (deprecated)
```

リクエストの "Cookie" ヘッダー行から、Cookie名 `<name>` の最後の出現箇所を抽出し、その値を文字列で返します。名前を指定しなければ、最初のCookieの値を返します。ACLで使用する場合は、一致するすべてのCookieを評価します。Cookieヘッダーの仕様 (RFC6265) に従い、名前と値の周囲のスペースを無視します。Cookie名の大文字と小文字は区別します。空のCookieも有効なので、空のCookieが存在する場合は、空の値を返すことがあります。存在の検出には、"found" マッチングを使用してください。サーバーが送信したレスポンスのCookieには、res.cook()版を使用してください。

派生ACL:

```text
req.cook([<name>])    : 文字列の完全一致
req.cook_beg([<name>]): 接頭辞の照合
req.cook_dir([<name>]): サブディレクトリの照合
req.cook_dom([<name>]): ドメインの照合
req.cook_end([<name>]): 接尾辞の照合
req.cook_len([<name>]): 長さの照合
req.cook_reg([<name>]): 正規表現の照合
req.cook_sub([<name>]): 部分文字列の照合
```

注意： 派生ACLの後にコンバーターを続けたり、"-m" パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

<a id="entry-7-3-6-req-cook-cnt-integer"></a>

**`req.cook_cnt([<name>]): integer`**

```haproxy
req.cook_cnt([<name>]): integer
cook_cnt([<name>]): integer (deprecated)
```

リクエスト内のCookie `<name>` の出現数を表す整数値を返します。`<name>` を指定しなかった場合は、すべてのCookieの数を返します。

<a id="entry-7-3-6-req-cook-names-string"></a>

**`req.cook_names([<delim>]): string`**

```haproxy
req.cook_names([<delim>]): string
```

ルールを評価した時点で、リクエストのCookieヘッダーにあるすべてのCookie名を、その出現どおりに連結した文字列を作成します。デフォルトの区切り文字はカンマ (',') ですが、省略可能な引数 `<delim>` で上書きできます。その場合、`<delim>` の最初の文字だけを使用します。

<a id="entry-7-3-6-req-cook-val-integer"></a>

**`req.cook_val([<name>]): integer`**

```haproxy
req.cook_val([<name>]): integer
cook_val([<name>]): integer (deprecated)
```

リクエストの "Cookie" ヘッダー行から、Cookie名 `<name>` の最後の出現箇所を抽出し、その値を整数に変換して返します。名前を指定しなければ、最初のCookieの値を返します。ACLで使用する場合は、値が一致するまで、名前が一致するすべてのCookieを順に処理します。

<a id="entry-7-3-6-req-fhdr-string"></a>

**`req.fhdr(<name>[,<occ>]): string`**

```haproxy
req.fhdr(<name>[,<occ>]): string
```

HTTPリクエスト内のヘッダー `<name>` の、最後の出現箇所の完全な値を返します。req.hdr()とは異なり、値に含まれるカンマもそのまま返し、区切り文字として使用しません。User-Agentなどのヘッダーで役立つ場合があります。

ACLから使用する場合は、一致が見つかるまで、すべての出現箇所を順に処理します。

省略可能な位置番号を指定して、特定の出現箇所を選ぶこともできます。正の値は、最初の出現箇所から数えた位置を示し、1が最初です。負の値は、最後の出現箇所からの相対位置を示し、-1が最後です。

<a id="entry-7-3-6-req-fhdr-cnt-integer"></a>

**`req.fhdr_cnt([<name>]): integer`**

```haproxy
req.fhdr_cnt([<name>]): integer
```

リクエストヘッダーフィールド名 `<name>` の出現数を表す整数値を返します。`<name>` を指定しなかった場合は、ヘッダーフィールドの総数を返します。req.fhdr()と同様に、カンマでヘッダーを分割しない点が、res.hdr_cnt()とは異なります。

<a id="entry-7-3-6-req-hdr-string"></a>

**`req.hdr([<name>[,<occ>]]): string`**

```haproxy
req.hdr([<name>[,<occ>]]): string
```

HTTPリクエスト内のヘッダー `<name>` の、カンマで区切った最後の値を返します。この取得関数は、すべてのカンマを、別々の値を区切る文字として扱います。AcceptやX-Forwarded-Forなど、値のリストとして定義するヘッダーを処理する場合に便利です。代わりにヘッダーの行全体が必要な場合は、req.fhdr()を使用してください。特定のヘッダーをどのように解析すべきかについては、RFC 7231を注意深く確認してください。また、Connectionなど、大文字と小文字を区別しないヘッダーもあります。

ACLから使用する場合は、一致が見つかるまで、すべての出現箇所を順に処理します。

省略可能な位置番号を指定して、特定の出現箇所を選ぶこともできます。正の値は、最初の出現箇所から数えた位置を示し、1が最初です。負の値は、最後の出現箇所からの相対位置を示し、-1が最後です。

代表的な用途は、X-Forwarded-ForヘッダーをIPに変換して、IP型のスティックテーブルと組み合わせることです。

派生ACL:

```text
hdr([<name>[,<occ>]])    : 文字列の完全一致
hdr_beg([<name>[,<occ>]]): 接頭辞の照合
hdr_dir([<name>[,<occ>]]): サブディレクトリの照合
hdr_dom([<name>[,<occ>]]): ドメインの照合
hdr_end([<name>[,<occ>]]): 接尾辞の照合
hdr_len([<name>[,<occ>]]): 長さの照合
hdr_reg([<name>[,<occ>]]): 正規表現の照合
hdr_sub([<name>[,<occ>]]): 部分文字列の照合
```

注意： 派生ACLの後にコンバーターを続けたり、"-m" パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

<a id="entry-7-3-6-req-hdr-cnt-integer"></a>

**`req.hdr_cnt([<name>]): integer`**

```haproxy
req.hdr_cnt([<name>]): integer
hdr_cnt([<header>]): integer (deprecated)
```

リクエストヘッダーフィールド名 `<name>` の出現数を表す整数値を返します。`<name>` を指定しなかった場合は、ヘッダーフィールドの値の総数を返します。req.hdr()と同様に、ヘッダーの値をカンマで区切った各部分を数えます。ヘッダーの行全体の数を数えたい場合は、代わりにreq.fhdr_cnt()を使用すべきです。

ACLでは、特定のヘッダーの存在、不在、濫用を検出したり、特定のヘッダーが複数あるリクエストを拒否して、リクエストスマグリング攻撃を防いだりするために使用できます。

ヘッダーのマッチングの詳細については、req.hdr()を参照してください。

<a id="entry-7-3-6-req-hdr-ip-ip"></a>

**`req.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
req.hdr_ip([<name>[,<occ>]]): ip
hdr_ip([<name>[,<occ>]]): ip (deprecated)
```

HTTPリクエスト内のヘッダー `<name>` の最後の出現箇所を抽出し、IPv4またはIPv6アドレスに変換して、そのアドレスを返します。ACLで使用する場合は、すべての出現箇所を検査し、`<name>` を省略した場合は、すべてのヘッダーのすべての値を検査します。パーサーはRFC7239で説明する形式に厳密に従います。ただし、IPv4アドレスの後に、コロン (':') と、有効な10進数のポート番号（0から65535）を任意で付けられる拡張があります。このポート番号は、通知せずに取り除きます。それ以外の形式はすべて一致せず、そのアドレスを無視します。

`<occ>` パラメーターは、req.hdr()と同じように処理します。

代表的な用途は、X-Forwarded-ForおよびX-Client-IPヘッダーでの使用です。

<a id="entry-7-3-6-req-hdr-names-string"></a>

**`req.hdr_names([<delim>]): string`**

```haproxy
req.hdr_names([<delim>]): string
```

ルールを評価した時点で、リクエストにあるすべてのヘッダー名を、その出現どおりに連結した文字列を作成します。デフォルトの区切り文字はカンマ (',') ですが、省略可能な引数 `<delim>` で上書きできます。その場合、`<delim>` の最初の文字だけを使用します。

<a id="entry-7-3-6-req-hdr-val-integer"></a>

**`req.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
req.hdr_val([<name>[,<occ>]]): integer
hdr_val([<name>[,<occ>]]): integer (deprecated)
```

HTTPリクエスト内のヘッダー `<name>` の最後の出現箇所を抽出し、整数値に変換します。ACLで使用する場合は、すべての出現箇所を検査し、`<name>` を省略した場合は、すべてのヘッダーのすべての値を検査します。

`<occ>` パラメーターは、req.hdr()と同じように処理します。

代表的な用途は、X-Forwarded-Forヘッダーでの使用です。

req.hdrs: string 現在のリクエストヘッダーを、ヘッダーとリクエストボディーを区切る最後の空行を含む文字列で返します。この最後の空行は、途中で切れたヘッダーブロックの検出に使用できます。このサンプル取得関数は、一部のSPOEヘッダー解析器や、高度なログ記録に役立ちます。

req.hdrs_bin: binary 現在のリクエストヘッダーを、解析済みのバイナリー形式で返します。SPOEに処理の一部を委譲する場合に便利です。各文字列は、長さと、それに続く、長さで指定したバイト数のデータで表します。長さは、SPOEのドキュメントで詳述する、可変長整数のエンコーディングで表します。リストの終わりは、空のヘッダー名と値の組（両方の長さが0）で示します。

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: エンコーディングについては、SPOEのドキュメントを参照してください。str: ``` <int:length>``<bytes> ```

req.timer.hdr: integer クライアントのリクエストを取得するまでの合計時間です（HTTPモードのみ）。最初のバイトを受信してから、HTTPヘッダーの終わりを示す空行をプロキシが受信するまでの経過時間です。ミリ秒 (ms) 単位で報告し、log-formatの%TRに相当します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

req.timer.idle: integer HTTPリクエストの前のアイドル時間です（HTTPモードのみ）。ハンドシェイクの終了から、HTTPリクエストの最初のバイトまでの時間を数えます。ミリ秒単位で報告し、log-formatの%Tiに相当します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

req.timer.queue: integer 接続スロットを待つために、キュー内で費やした合計時間です。ミリ秒単位で報告し、log-formatの%Twに相当します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

req.timer.tq: integer 接続を受け入れた時点、または前のレスポンスの最後のバイトを送信した時点から、クライアントのリクエストを取得するまでの合計時間です。ミリ秒単位で報告し、log-formatの%Tqに相当します。詳細は、[8.4節](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

req.ver: string req_ver: string (非推奨) HTTPリクエストのバージョン文字列を、"`<major>`.`<minor>`" 形式で返します。ACLで役立つ場合があります。一般的なバージョンは、定義済みACLですでに検査できます。保持される情報を使用するため、リクエスト、レスポンス、ログで使用できます。リクエストのバージョンが無効な場合、このサンプル取得は失敗します。

一般的な値は、"1.0"、"1.1"、"2.0"、"3.0" です。

派生ACL:

```text
req.ver: 文字列の完全一致
```

<a id="entry-7-3-6-request-date-integer"></a>

**`request_date([<unit>]): integer`**

```haproxy
request_date([<unit>]): integer
```

HAProxyがHTTPリクエストの最初のバイトを受信した正確な日時です（log-formatのエイリアス%tr）。accept_date＋ハンドシェイク時間（%Th）＋アイドル時間（%Ti）から計算します。

エポックからの秒数を返します。

`<unit>`は任意です。秒を表す"s"（デフォルトの動作）、ミリ秒を表す"ms"、マイクロ秒を表す"us"を指定できます。単位を指定した場合、エポックからの秒数、ミリ秒数、マイクロ秒数のいずれかを表す整数値を返します。1秒未満の時間分解能が必要な場合に役立ちます。

res.body: binary HTTPレスポンスの利用可能なボディーをデータブロックとして返します。リクエスト側とは異なり、レスポンスボディーを待つディレクティブはありません。このサンプル取得は、ヘルスチェックのコンテキストで特に有用であり、使用可能です。

tcp-checkに基づくexpectルールで使用できます。

res.body_len: integer HTTPレスポンスの利用可能なボディーの長さをバイト単位で返します。リクエスト側とは異なり、レスポンスボディーを待つディレクティブはありません。このサンプル取得は、ヘルスチェックのコンテキストで特に有用であり、使用可能です。

tcp-checkに基づくexpectルールで使用できます。

res.body_size: integer HTTPレスポンスボディーの通知された長さをバイト単位で返します。Content-Lengthヘッダーで通知された長さ、またはチャンクエンコーディングの場合は利用可能なデータのサイズを表します。リクエスト側とは異なり、レスポンスボディーを待つディレクティブはありません。このサンプル取得は、ヘルスチェックのコンテキストで特に有用であり、使用可能です。

tcp-checkに基づくexpectルールで使用できます。

res.cache_hit: boolean レスポンスがHTTPキャッシュのエントリーから作成された場合はブール値"true"を返し、それ以外の場合はブール値"false"を返します。

res.cache_name: string res.cache_hitが真の場合、HTTPレスポンスの作成に使用したHTTPキャッシュの名前を含む文字列を返し、それ以外の場合は空文字列を返します。

res.comp: boolean レスポンスがHAProxyによって圧縮された場合はブール値"true"を返し、それ以外の場合はブール値"false"を返します。ログに情報を追加する用途に使用できます。

res.comp_algo: string レスポンスがHAProxyによって圧縮された場合、使用したアルゴリズムの名前を含む文字列を返します。たとえば、"deflate"です。ログに情報を追加する用途に使用できます。

<a id="entry-7-3-6-res-cook-string"></a>

**`res.cook([<name>]): string`**

```haproxy
res.cook([<name>]): string
scook([<name>]): string (deprecated)
```

レスポンスの"Set-Cookie"ヘッダー行から、名前`<name>`のCookieの最後の出現を抽出し、その値を文字列として返します。名前を指定しない場合、最初のCookieの値を返します。

tcp-checkに基づくexpectルールで使用できます。

派生ACL:

```text
res.scook([<name>]: 文字列の完全一致
```

<a id="entry-7-3-6-res-cook-cnt-integer"></a>

**`res.cook_cnt([<name>]): integer`**

```haproxy
res.cook_cnt([<name>]): integer
scook_cnt([<name>]): integer (deprecated)
```

レスポンスに含まれるCookie`<name>`の出現回数を表す整数値を返します。`<name>`を指定しない場合は、すべてのCookieの数を返します。主にACLと併用して、不審なレスポンスを検出する用途に役立ちます。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-cook-names-string"></a>

**`res.cook_names([<delim>]): string`**

```haproxy
res.cook_names([<delim>]): string
```

ルールを評価した時点で、レスポンス（Set-Cookieヘッダー）に出現順にすべてのCookie名を連結した文字列を作成します。デフォルトの区切り文字はカンマ（','）ですが、任意の引数`<delim>`で変更できます。この場合、`<delim>`の最初の文字だけを使用します。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-cook-val-integer"></a>

**`res.cook_val([<name>]): integer`**

```haproxy
res.cook_val([<name>]): integer
scook_val([<name>]): integer (deprecated)
```

レスポンスの"Set-Cookie"ヘッダー行から、名前`<name>`のCookieの最後の出現を抽出し、その値を整数に変換して返します。名前を指定しない場合、最初のCookieの値を返します。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-fhdr-string"></a>

**`res.fhdr([<name>[,<occ>]]): string`**

```haproxy
res.fhdr([<name>[,<occ>]]): string
```

req.fhdr()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

req.fhdr()と同様に、res.fhdr()取得は値全体を返します。ヘッダーがリストとして定義されている場合は、res.hdr()の使用を推奨します。

DateやExpiresなどのヘッダーに対して役立つ場合があります。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-fhdr-cnt-integer"></a>

**`res.fhdr_cnt([<name>]): integer`**

```haproxy
res.fhdr_cnt([<name>]): integer
```

req.fhdr_cnt()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

req.fhdr_cnt()と同様に、res.fhdr_cnt()取得は値全体に作用します。ヘッダーがリストとして定義されている場合は、res.hdr_cnt()の使用を推奨します。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-hdr-string"></a>

**`res.hdr([<name>[,<occ>]]): string`**

```haproxy
res.hdr([<name>[,<occ>]]): string
shdr([<name>[,<occ>]]): string (deprecated)
```

req.hdr()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

req.hdr()と同様に、res.hdr()取得はカンマを区切り文字として扱います。この動作が望ましくない場合は、res.fhdr()の使用を推奨します。

tcp-checkに基づくexpectルールで使用できます。

派生ACL:

```text
res.hdr([<name>[,<occ>]])    : 文字列の完全一致
res.hdr_beg([<name>[,<occ>]]): 接頭辞の照合
res.hdr_dir([<name>[,<occ>]]): サブディレクトリの照合
res.hdr_dom([<name>[,<occ>]]): ドメインの照合
res.hdr_end([<name>[,<occ>]]): 接尾辞の照合
res.hdr_len([<name>[,<occ>]]): 長さの照合
res.hdr_reg([<name>[,<occ>]]): 正規表現の照合
res.hdr_sub([<name>[,<occ>]]): 部分文字列の照合
```

注意：派生ACLの後にコンバーターを続けたり、"-m"パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

<a id="entry-7-3-6-res-hdr-cnt-integer"></a>

**`res.hdr_cnt([<name>]): integer`**

```haproxy
res.hdr_cnt([<name>]): integer
shdr_cnt([<name>]): integer (deprecated)
```

req.hdr_cnt()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

req.hdr_cnt()と同様に、res.hdr_cnt()取得はカンマを区切り文字として扱います。この動作が望ましくない場合は、res.fhdr_cnt()の使用を推奨します。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-hdr-ip-ip"></a>

**`res.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
res.hdr_ip([<name>[,<occ>]]): ip
shdr_ip([<name>[,<occ>]]): ip (deprecated)
```

req.hdr_ip()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

スティックテーブルにデータを学習させる用途に役立ちます。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-hdr-names-string"></a>

**`res.hdr_names([<delim>]): string`**

```haproxy
res.hdr_names([<delim>]): string
```

ルールを評価した時点で、レスポンスに出現順にすべてのヘッダー名を連結した文字列を作成します。デフォルトの区切り文字はカンマ（','）ですが、任意の引数`<delim>`で変更できます。この場合、`<delim>`の最初の文字だけを使用します。

tcp-checkに基づくexpectルールで使用できます。

<a id="entry-7-3-6-res-hdr-val-integer"></a>

**`res.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
res.hdr_val([<name>[,<occ>]]): integer
shdr_val([<name>[,<occ>]]): integer (deprecated)
```

req.hdr_val()取得と同様に動作しますが、HTTPレスポンス内のヘッダーに作用する点が異なります。

スティックテーブルにデータを学習させる用途に役立ちます。

tcp-checkに基づくexpectルールで使用できます。

res.hdrs: string 現在のレスポンスヘッダーを、ヘッダーとリクエストボディーを区切る最後の空行も含めて文字列として返します。最後の空行は、ヘッダーブロックの切り詰めを検出するために使用できます。一部のSPOEヘッダー解析や高度なログ記録に役立つサンプル取得です。

tcp-checkに基づくexpectルールでも使用できます。

res.hdrs_bin: binary 事前解析済みのバイナリ形式で格納された現在のレスポンスヘッダーを返します。SPOEで一部の処理を外部へ委譲する用途に役立ちます。tcp-checkに基づくexpectルールで使用できます。各文字列は、長さと、それに続く、長さで指定したバイト数のデータで表します。長さはSPOEのドキュメントで詳述する可変長整数エンコーディングで表します。リストの終わりは、空のヘッダー名と空の値の組（両方の長さが0）で示します。

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: エンコーディングについては、SPOEのドキュメントを参照してください。str: ``` <int:length>``<bytes> ```

res.timer.hdr: integer サーバーへのTCP接続が確立した時点から、サーバーがレスポンスヘッダー全体を送信した時点までの経過時間です。ミリ秒単位で報告し、log-formatの%Trに相当します。詳細は[セクション8.4](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

res.ver: string resp_ver: string (非推奨) HTTPレスポンスのバージョン文字列を、"`<major>`.`<minor>`"という形式で返します。ログに役立つ場合もありますが、主にACL用です。レスポンスのバージョンが無効な場合、このサンプル取得は失敗します。

tcp-checkに基づくexpectルールで使用できます。

派生ACL:

```text
resp.ver: 文字列の完全一致
```

server_status: integer サーバーから受信したHTTPステータスコードを含む整数を返します。サーバーからレスポンスを受信しなかった場合、このサンプル取得は失敗します。

<a id="entry-7-3-6-set-cookie-string"></a>

**`set-cookie([<name>]): string (deprecated)`**

```haproxy
set-cookie([<name>]): string (deprecated)
```

レスポンスの"Set-Cookie"ヘッダー行から、名前`<name>`のCookieの最後の出現を抽出し、対応する値を照合に使用します。"appsession"がデフォルトのオプションで行っていた処理に相当しますが、複数ピア間の同期と、再起動をまたいだ状態保持をサポートします。

この取得関数は非推奨で、"res.cook"取得に置き換えられています。このキーワードはまもなく削除されます。

status: integer HTTPレスポンスのHTTPステータスコードを含む整数を返します。たとえば、302です。主にACLと整数範囲の照合に使用し、たとえばレスポンスが3xxでない場合にLocationヘッダーを削除する用途があります。'set-status'アクションなどで変更しなければ、クライアントが受信するステータスコードになります。

tcp-checkに基づくexpectルールで使用できます。

txn.status: integer ログに報告されるトランザクションのHTTPステータスコードを含む整数を返します。

txn.timer.total: integer HTTPリクエストの総アクティブ時間です。プロキシがリクエストヘッダーの最初のバイトを受信した時点から、レスポンスボディーの最後のバイトを送信した時点までの時間を指します。log-formatの%Taに相当し、ミリ秒（ms）単位で報告します。詳細は[セクション8.4](/ja/haproxy/configuration-logging/#section-8-4)「タイミングイベント」を参照してください。

unique-id: string リクエストに付与されたunique-idを返します。"unique-id-format"ディレクティブを設定しなければなりません。設定していない場合、unique-idサンプル取得は失敗します。unique-idは通常HTTPリクエストで使用しますが、このサンプル取得は他のプロトコルでも使用できます。HTTP以外のプロトコルで使用する場合、unique-id-formatディレクティブにHTTPの要素を含めてはいけません。unique-id-formatとunique-id-headerを参照してください。

url: string リクエストのURLを、リクエストに記載された形のまま抽出します。典型的な用途は、プリフェッチに対応するキャッシュや、データベースから複数の情報を集約してキャッシュに保持する必要があるポータルです。ACLでは、"url"より"path"の使用を推奨します。クライアントは、通常プロキシに対して行うように、完全なURLを送信する場合があるためです。実質的な用途は、"path"では一致しない"\*"との照合だけであり、この用途にはすでに定義済みのACLがあります。"path"と"base"も参照してください。URI内のフラグメント参照（パスの後の'#'）はHTTP標準で厳密に禁止されており、拒否されます。ただし、リクエストを受信するフロントエンドに"option accept-unsafe-violations-in-http-request"がある場合、このフラグメント部分は受け入れられ、urlにも含まれます。

派生ACL:

```text
url    : 文字列の完全一致
url_beg: 接頭辞の照合
url_dir: サブディレクトリの照合
url_dom: ドメインの照合
url_end: 接尾辞の照合
url_len: 長さの照合
url_reg: 正規表現の照合
url_sub: 部分文字列の照合
```

注意：派生ACLの後にコンバーターを続けたり、"-m"パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

url32: integer 最初のHostヘッダーと、パラメーターを含むURL全体を連結した値の32ビットハッシュを返します（前述の"base32"取得のように、リクエストのパス部分だけではありません）。URLごとの活動を追跡する用途に役立ちます。短いハッシュを保存するため、大幅にメモリーを節約できます。出力型は符号なし整数です。

url32+src: binary "url32"取得と"src"取得を連結した値を返します。結果はバイナリ型で、送信元アドレスファミリーに応じて8バイトまたは20バイトになります。IPごと、URLごとのカウンターを追跡する用途に使用できます。

url_ip: ip ホスト部分がIPアドレスとして記載されている場合、リクエストのURLからIPアドレスを抽出します。ホスト部分が名前の場合、名前解決を行わないため取得は失敗します。用途は非常に限られています。たとえば、監視システムが、特定の送信元アドレスがどの経路をたどるかを試すために、または特定の送信元アドレスのエントリーをテーブルに強制的に作成するために、送信元IPの代わりにこのフィールドを使用する場合があります。'http-request set-dst'と組み合わせて、従来の'option http_proxy'を再現できます。

url_port: integer リクエストのURLからポート部分を抽出します。リクエストでポートを指定しない場合、ポート80とみなします。"url_ip"と同様、URLのauthorityがアドレスとして記載されている場合だけ動作します。ホスト名の場合は、ここでは名前解決を行わないため取得が失敗します。

<a id="entry-7-3-6-urlp-string"></a>

**`urlp([<name>[,<delim>[,i]]]): string`**

```haproxy
urlp([<name>[,<delim>[,i]]]): string
url_param([<name>[,<delim>[,i]]]): string
```

クエリー文字列内で、パラメーター`<name>`の最初の出現を抽出します。パラメーターは'?'または`<delim>`の後から始まり、'&'、';'、`<delim>`のいずれかの前で終わります。3番目の引数に"i"を追加しない限り、パラメーター名は大文字と小文字を区別します。名前を指定しない場合、どのパラメーターも一致し、最初のものを返します。結果は、リクエストに記載されたパラメーター`<name>`の値に対応する文字列です（URLデコードは行いません）。クライアントIDに基づくセッション維持、URLパラメーターとして渡されたアプリケーションCookieの抽出、ACLでの検査に使用できます。この取得のACL版は複数のパラメーターを順に処理し、名前を指定しない場合は、すべてのパラメーターの値を順に返します。

派生ACL:

```text
urlp(<name>[,<delim>])    : 文字列の完全一致
urlp_beg(<name>[,<delim>]): 接頭辞の照合
urlp_dir(<name>[,<delim>]): サブディレクトリの照合
urlp_dom(<name>[,<delim>]): ドメインの照合
urlp_end(<name>[,<delim>]): 接尾辞の照合
urlp_len(<name>[,<delim>]): 長さの照合
urlp_reg(<name>[,<delim>]): 正規表現の照合
urlp_sub(<name>[,<delim>]): 部分文字列の照合
```

注意：派生ACLの後にコンバーターを続けたり、"-m"パターンマッチングメソッドを指定したACLで使用したりしてはいけません。

例：

```shell
# match http://example.com/foo?PHPSESSIONID=some_id
stick on urlp(PHPSESSIONID)
# match http://example.com/foo;JSESSIONID=some_id
stick on urlp(JSESSIONID,;)
```

<a id="entry-7-3-6-urlp-val-integer"></a>

**`urlp_val([<name>[,<delim>[,i]]]): integer`**

```haproxy
urlp_val([<name>[,<delim>[,i]]]): integer
```

前述の"urlp"を参照してください。リクエスト内のURLパラメーター`<name>`を抽出し、整数値に変換します。たとえば、ユーザーIDに基づくセッション維持や、ACLでページ番号または価格を照合する用途に使用できます。

### 7.3.7. 開発者向けのサンプル取得 {#section-7-3-7}

このサンプル取得メソッド群は開発者専用です。開発者の依頼に基づくデバッグ用途を除き、本番環境で決して使用してはなりません。また、後方互換性には特別な配慮を行いません。以下のサンプル取得を変更、改名、削除しないという保証はありません。使用が必要な場合は、十分に注意してください。曖昧さを避けるため、これらのサンプル取得は専用の"internal"スコープに置かれています。たとえば、"internal.strm.is_htx"です。

この節のサンプル取得メソッドと、それぞれの型の一覧：

```text
  キーワード                                       出力型
-------------------------------------------------+-------------
internal.htx.data                                  integer
internal.htx.free                                  integer
internal.htx.free_data                             integer
internal.htx.has_eom                               boolean
internal.htx.nbblks                                integer
internal.htx.size                                  integer
internal.htx.used                                  integer
internal.htx_blk.size(<idx>)                       integer
internal.htx_blk.type(<idx>)                       string
internal.htx_blk.data(<idx>)                       binary
internal.htx_blk.hdrname(<idx>)                    string
internal.htx_blk.hdrval(<idx>)                     string
internal.htx_blk.start_line(<idx>)                 string
internal.strm.is_htx                               boolean
-------------------------------------------------+-------------
```

詳細一覧：

internal.htx.data: integer チャネルに関連付けられたHTXメッセージ内で、データが使用するサイズをバイト単位で返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.free: integer チャネルに関連付けられたHTXメッセージ内の空き領域（size - used）をバイト単位で返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.free_data: integer チャネルに関連付けられたHTXメッセージ内の、データ用の空き領域をバイト単位で返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.has_eom: boolean チャネルに関連付けられたHTXメッセージにメッセージ終端フラグ（EOM）が含まれている場合はtrueを返し、それ以外の場合はfalseを返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.nbblks: integer チャネルに関連付けられたHTXメッセージ内のブロック数を返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.size: integer チャネルに関連付けられたHTXメッセージの合計サイズをバイト単位で返します。チャネルはサンプルの方向に応じて選択します。

internal.htx.used: integer チャネルに関連付けられたHTXメッセージ内で使用する合計サイズ（データ＋メタデータ）をバイト単位で返します。チャネルはサンプルの方向に応じて選択します。

<a id="entry-7-3-7-internal-htx-blk-size-integer"></a>

**`internal.htx_blk.size(<idx>): integer`**

```haproxy
internal.htx_blk.size(<idx>): integer
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるブロックのサイズを返します。存在しない場合は0を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます： \* head : 最も古く挿入されたブロック \* tail : 最も新しく挿入されたブロック \* first: 解析を開始または再開する最初のブロック

<a id="entry-7-3-7-internal-htx-blk-type-string"></a>

**`internal.htx_blk.type(<idx>): string`**

```haproxy
internal.htx_blk.type(<idx>): string
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるブロックの型を返します。存在しない場合は"HTX_BLK_UNUSED"を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます： \* head : 最も古く挿入されたブロック \* tail : 最も新しく挿入されたブロック \* first: 解析を開始または再開する最初のブロック

<a id="entry-7-3-7-internal-htx-blk-data-binary"></a>

**`internal.htx_blk.data(<idx>): binary`**

```haproxy
internal.htx_blk.data(<idx>): binary
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるDATAブロックの値を返します。存在しない場合、またはDATAブロックでない場合は、空文字列を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます：

    * head : 最も古く挿入されたブロック
    * tail : 最も新しく挿入されたブロック
    * first: 解析を開始または再開する最初のブロック

<a id="entry-7-3-7-internal-htx-blk-hdrname-string"></a>

**`internal.htx_blk.hdrname(<idx>): string`**

```haproxy
internal.htx_blk.hdrname(<idx>): string
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるHEADERブロックのヘッダー名を返します。存在しない場合、またはHEADERブロックでない場合は、空文字列を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます：

    * head : 最も古く挿入されたブロック
    * tail : 最も新しく挿入されたブロック
    * first: 解析を開始または再開する最初のブロック

<a id="entry-7-3-7-internal-htx-blk-hdrval-string"></a>

**`internal.htx_blk.hdrval(<idx>): string`**

```haproxy
internal.htx_blk.hdrval(<idx>): string
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるHEADERブロックのヘッダー値を返します。存在しない場合、またはHEADERブロックでない場合は、空文字列を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます：

    * head : 最も古く挿入されたブロック
    * tail : 最も新しく挿入されたブロック
    * first: 解析を開始または再開する最初のブロック

<a id="entry-7-3-7-internal-htx-blk-start-line-string"></a>

**`internal.htx_blk.start_line(<idx>): string`**

```haproxy
internal.htx_blk.start_line(<idx>): string
```

チャネルに関連付けられたHTXメッセージ内の、位置`<idx>`にあるREQ_SLまたはRES_SLブロックの値を返します。存在しない場合、またはSLブロックでない場合は、空文字列を返します。チャネルはサンプルの方向に応じて選択します。`<idx>`には任意の正の整数、または次の特殊な値を指定できます：

    * head : 最も古く挿入されたブロック
    * tail : 最も新しく挿入されたブロック
    * first: 解析を開始または再開する最初のブロック

internal.strm.is_htx: boolean 現在のストリームがHTXストリームの場合はtrueを返します。これは、チャネルバッファー内のデータを内部HTX表現で格納していることを意味します。それ以外の場合はfalseを返します。

## 7.4. 定義済みACL {#section-7-4}

一部の定義済みACLはハードコードされているため、必要とするフロントエンドごとに宣言する必要はありません。混同を避けるため、名前はすべて大文字です。等価な定義を以下に示します。

```text
ACL名             等価な式                     用途
---------------+----------------------------------+------------------------------------------------------
FALSE            always_false                       決して一致しません
HTTP             req.proto_http                     リクエストのプロトコルが有効なHTTPの場合に一致します
HTTP_1.0         req.ver 1.0                        HTTPリクエストのバージョンが1.0の場合に一致します
HTTP_1.1         req.ver 1.1                        HTTPリクエストのバージョンが1.1の場合に一致します
HTTP_2.0         req.ver 2.0                        HTTPリクエストのバージョンが2.0の場合に一致します
HTTP_3.0         req.ver 3.0                        HTTPリクエストのバージョンが3.0の場合に一致します
HTTP_CONTENT     req.hdr_val(content-length) gt 0   HTTPリクエストに存在するcontent-lengthに一致します
HTTP_URL_ABS     url_reg ^[^/:]*://                 スキーム付きの絶対URLに一致します
HTTP_URL_SLASH   url_beg /                          "/"で始まるURLに一致します
HTTP_URL_STAR    url     *                          "*"と等しいURLに一致します
LOCALHOST        src 127.0.0.1/8::1                ローカルホストからの接続に一致します
METH_CONNECT     method  CONNECT                    HTTPのCONNECTメソッドに一致します
METH_DELETE      method  DELETE                     HTTPのDELETEメソッドに一致します
METH_GET         method  GET HEAD                   HTTPのGETまたはHEADメソッドに一致します
METH_HEAD        method  HEAD                       HTTPのHEADメソッドに一致します
METH_OPTIONS     method  OPTIONS                    HTTPのOPTIONSメソッドに一致します
METH_POST        method  POST                       HTTPのPOSTメソッドに一致します
METH_PUT         method  PUT                        HTTPのPUTメソッドに一致します
METH_TRACE       method  TRACE                      HTTPのTRACEメソッドに一致します
RDP_COOKIE       req.rdp_cookie_cnt gt 0            リクエストバッファー内にRDP Cookieがあれば一致します
REQ_CONTENT      req.len gt 0                       リクエストバッファー内のデータに一致します
TRUE             always_true                        常に一致します
WAIT_END         wait_end                           コンテンツ解析の終了を待ちます
---------------+----------------------------------+------------------------------------------------------
```
