---
title: "リリースノート"
linkTitle: "リリース"
weight: 60
description: "各バージョンの詳細な変更履歴を含むpgBackRestのリリース履歴。"
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## はじめに {#introduction}

pgBackRestのリリース番号は、メジャー、マイナー、パッチの3つの部分で構成されます。メジャーリリースでは、以前のメジャーリリースとの互換性が失われる*可能性があります*。ただし、v2リリースはv1リポジトリと完全に互換性があり、すべてのv1オプションを受け付けます。マイナーリリースには不具合修正や新機能が含まれることがありますが、リポジトリ形式は変更せず、オプションや名称の変更も極力避けます。パッチリリースには、最新のマイナーリリースに対する不具合修正が含まれます。

機能リリースは1月、4月、7月、10月の第3月曜日に予定されています。それ以外の月は、必要に応じて第3月曜日にパッチリリースを行います。

v1リリースのドキュメントは[こちら](https://pgbackrest.org/1)を参照してください。

リリースノートには「補足事項」が含まれる場合もありますが、このセクションの変更はドキュメントまたはテストスイートのみを対象とし、pgBackRestのコードには直接影響しません。

--------

## 本ドキュメントの対象となる安定版 {#current-stable-release}

このミラーはv2.60.0を対象としています。より新しいバージョンについては、[アップストリームのリリース履歴](https://pgbackrest.org/release.html)を参照してください。

### v2.60.0リリースノート {#v2600-release-notes}

*ページチェックサムエラーとオブジェクトストアのプリフェッチ*

*2026年10月18日リリース*

**重要な注意事項**：`restore`コマンドは、復元したファイルに無効なページチェックサムが含まれていると、エラーを報告して停止するようになりました。この場合、クラスターは不完全で起動できない状態になるため、復元を再実行する必要があります。`expire`コマンドは、保持する最古のバックアップにチェックサムエラーが含まれることになる場合、期限切れ処理を拒否するようになりました。そのリポジトリのアーカイブも期限切れ処理されません。エラーではなく警告にするには、`checksum-page-error=n`を設定してください。

**新機能：**

- 無効なページチェックサムを検出した場合にエラーとする`checksum-page-error`オプションを追加しました。 (*貢献：Andrew Pogrebnoi。レビュー：Douglas J Hunley, David Steele, Greg Sabino Mullane, Stefan Fercot。提案：Greg Sabino Mullane。*)

  このオプションは`backup`、`restore`、`expire`コマンドに適用されます。`backup`コマンドのデフォルトは従来どおりファイルごとの警告で、バックアップ終了時にはチェックサム警告の総数も報告するようになりました。`restore`と`expire`コマンドのデフォルトはエラーです。以前の`restore`コマンドは、無効なページチェックサムをまったく報告していませんでした。

  課題 [#2687](https://github.com/pgbackrest/pgbackrest/issues/2687); プルリクエスト [#2833](https://github.com/pgbackrest/pgbackrest/pull/2833); コミット [`d7f54b2`](https://github.com/pgbackrest/pgbackrest/commit/d7f54b2245c8a9467e9a811c65626fe77739376b)
- GCS Workload Identity Federationをサポートしました。 (*貢献：Adol Rodriguez。レビュー：Douglas J Hunley, David Steele。*)

  `repo-gcs-key-type=web-id`を設定し、`repo-gcs-key`に外部アカウントの認証情報ファイルを指定します。たとえば、`gcloud iam workload-identity-pools create-cred-config`で生成したファイルを使用できます。Webアイデンティティトークンは、サービスアカウントキーを使わずにアクセストークンと交換されます。交換のたびにトークンファイルを再読み込みし、Kubernetesの投影されたサービスアカウントトークンなど、ローテーションされたトークンを取り込みます。サービスアカウントの権限借用はサポートしていません。

  課題 [#2838](https://github.com/pgbackrest/pgbackrest/issues/2838); プルリクエスト [#2839](https://github.com/pgbackrest/pgbackrest/pull/2839); コミット [`1d217e6`](https://github.com/pgbackrest/pgbackrest/commit/1d217e626301118ae2c1e7be39a6a4affa86e501)
- オブジェクトストアからの複数ファイル／範囲の読み取りをプリフェッチするようにしました。 (*レビュー：Andrew Pogrebnoi, Douglas J Hunley。*)

  現在の読み取りに先行してリクエストをキューに入れることで、読み取り中にもリクエストを進めます。また、ファイル間の小さな空隙は、新しいリクエストを開始せずに読み越します。`Restore`はこれをバンドル内のファイルとブロック増分マップの読み取りに使用し、`backup`は以前のバックアップのブロック増分マップの読み取りに使用します。`repo-storage-prefetch`（デフォルト3）はキューに入れるリクエスト数を、`repo-storage-read-over`（デフォルト64KiB）は読み越す空隙の最大サイズを設定します。

  [`e63dec3`](https://github.com/pgbackrest/pgbackrest/commit/e63dec323b9e79513638b9858e4ad13b6072d060) オブジェクトストアからの複数ファイル／範囲の読み取りをプリフェッチするようにしました。; プルリクエスト [#2783](https://github.com/pgbackrest/pgbackrest/pull/2783)

  [`5ae4015`](https://github.com/pgbackrest/pgbackrest/commit/5ae4015d37081eba4259f4de379a9d160236de0e) バックアップ中に以前のブロック増分マップの読み取りをまとめるようにしました。; プルリクエスト [#2816](https://github.com/pgbackrest/pgbackrest/pull/2816)

**改善：**

- リモートプロセスへのキープアライブリクエストを削減しました。 (*レビュー：Douglas J Hunley。*)

  以前は、`archive-push`と`backup`でジョブが完了するたびに、リクエストを送ったばかりのリモートを含め、すべてのリモートにキープアライブを送信していました。現在は、そのリモートに30秒間リクエストを送信していない場合にのみキープアライブを送信します。

  コミット [`f652261`](https://github.com/pgbackrest/pgbackrest/commit/f652261d32a4ffba98e7da26a41ef4ef1cd08da3)
- Azureの応答に含まれていないバッチサブリクエストを再試行するようにしました。 (*レビュー：Douglas J Hunley。*)

  Azureはバッチ削除に失敗した場合、バッチ全体に対する単一の応答を返すことがあります。応答のないサブリクエストも完了扱いになっていたため、コマンドが成功を報告していても、各バッチで1ファイルしか削除されませんでした。現在は、応答のないサブリクエストを再試行します。

  課題 [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); プルリクエスト [#2849](https://github.com/pgbackrest/pgbackrest/pull/2849); コミット [`567a245`](https://github.com/pgbackrest/pgbackrest/commit/567a2451244e0e7a4c54e41880fac1a007b49930)
- `backup.info`の再構築時に行うマニフェストの確認を削減しました。 (*レビュー：Douglas J Hunley。提案：todeb。*)

  `backup`、`expire`、`annotate`コマンドは、リポジトリの一覧からバックアップパスが存在しないと分かる場合、または差分・増分バックアップが`backup.info`にないフルバックアップセットに属する場合、`backup.manifest`を確認しなくなりました。確認のたびにリクエストが発生するため、オブジェクトストアでは、存在しないマニフェストの確認が404として記録されます。

  課題 [#2769](https://github.com/pgbackrest/pgbackrest/issues/2769); プルリクエスト [#2825](https://github.com/pgbackrest/pgbackrest/pull/2825); コミット [`0d3c340`](https://github.com/pgbackrest/pgbackrest/commit/0d3c340087bfb97263c29a8fd681cf079071236b)
- ファイルをバンドルに格納するかどうかを元のサイズで判断するようにしました。 (*レビュー：Douglas J Hunley。*)

  以前は、前回のバックアップにあるブロック増分ファイルのサイズでバンドルに格納するかどうかを判断していたため、`repo-bundle-limit`を超えて大きくなったファイルもバンドルに格納されることがありました。現在は、ファイルの現在のサイズを使用します。

  プルリクエスト [#2843](https://github.com/pgbackrest/pgbackrest/pull/2843); コミット [`340d58b`](https://github.com/pgbackrest/pgbackrest/commit/340d58bb49d6c88a002a0d23830fd37be155cc21)
- バックアップ中のブロックマップ読み取りエラーに状況情報を追加しました。 (*レビュー：Stefan Fercot, Douglas J Hunley。*)

  以前のバックアップのブロックマップを読み取る際のエラーで、ファイル、リポジトリパス、オフセット、マップサイズを報告するようになりました。読み取ったバイト数が予想より少ない場合は、解析エラーではなく、その旨を報告します。

  [`bc91688`](https://github.com/pgbackrest/pgbackrest/commit/bc91688c4cf18fa6a36ec65441784533d5e6bdd5) バックアップ中のブロックマップ読み取りエラーに状況情報を追加しました。; 課題 [#2489](https://github.com/pgbackrest/pgbackrest/issues/2489); 課題 [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); プルリクエスト [#2830](https://github.com/pgbackrest/pgbackrest/pull/2830)

  [`f46bfaf`](https://github.com/pgbackrest/pgbackrest/commit/f46bfafdd53dd0031a320fa95b08568263901ff3) ブロック増分マップのエラーに表示するオプション名を修正しました。
- バックアップ開始ラベルで`current_timestamp`を`text`にキャストするようにしました。 (*貢献：Tiago Corcelli de Oliveira。レビュー：David Steele。*)

  `timestamptz`から`text`へのユーザー定義の暗黙的キャストがあると、バックアップが"operator is not unique: unknown || timestamp with time zone"というエラーで失敗していました。ラベルのテキストは変更していません。

  課題 [#2873](https://github.com/pgbackrest/pgbackrest/issues/2873); コミット [`86936e1`](https://github.com/pgbackrest/pgbackrest/commit/86936e1fa60b10b7592eaac09283c4bb5991265d)
- illumosでのビルドをサポートしました。 (*貢献：Kalevi Kolttonen。レビュー：Douglas J Hunley, David Steele。*)

  CIにOmniOSのジョブを追加しました。Solarisでも動作する可能性がありますが、テストはしていません。

  プルリクエスト [#2870](https://github.com/pgbackrest/pgbackrest/pull/2870); コミット [`ad72e58`](https://github.com/pgbackrest/pgbackrest/commit/ad72e5815f3cf9c0c6170dcbe04ef9c41762d3d9)
- OpenSSL 4をサポートしました。 (*レビュー：Douglas J Hunley。*)

  `X509_get_subject_name()`が`const`の名前を返すようになったため、OpenSSL 4を使ったビルドが失敗していました。

  コミット [`a729ac8`](https://github.com/pgbackrest/pgbackrest/commit/a729ac881f48225622151841e80146f7a3a4bce6)
- clangでのビルドを修正しました。 (*レビュー：Douglas J Hunley。*)

  Linuxでは、gccはclangも検索する場所に`libbacktrace.a`をインストールしますが、`backtrace.h`はgccだけが見つけられる場所にインストールします。clangでのビルドはライブラリーを検出した後、コンパイルに失敗していました。現在は、ヘッダーが見つかった場合にのみライブラリーを使用します。また、デバッグビルドでclangが縮小変換として報告する戻り値の型も修正しました。

  [`84b031a`](https://github.com/pgbackrest/pgbackrest/commit/84b031af68fe6a30b4150ec6c903cc8c1781fc05) libbacktraceの確認時にヘッダーの存在も必須にしました。

  [`195e66b`](https://github.com/pgbackrest/pgbackrest/commit/195e66bafd89da511fb0d48e6e053176104c47c7) StringIdベースの列挙型を返す関数から、宣言された型を返すようにしました。

  [`d9e5e14`](https://github.com/pgbackrest/pgbackrest/commit/d9e5e14e93f460d62930f58dd4dd5bbc2a9f3a85) boolを返すと宣言された関数からboolを返すようにしました。
- コード生成をCからPythonに移行しました。

  ビルド中にオプション、エラー、ヘルプ、PostgreSQLの宣言からコードを生成する処理を、事前にビルドする必要のあったCツールからPythonツールに変更しました。gitチェックアウトからのビルドには、libyamlの代わりにPyYAMLが必要です。リリースtarballには生成済みコードが含まれているため、どちらも必要ありません。

  コミット [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e)

**ドキュメントの改善：**

- ウェブサイトを刷新しました。洞察に富んだ（そして愉快な）ロゴを作成してくれたJanに、特に感謝します。 (*貢献：David Steele, Jan Wieremjewicz。レビュー：Steve Atkins, Kai Wagner, Douglas J Hunley, Nikolaos Stamatopoulos, Matt Hudson, Stefan Fercot。*)

  ウェブサイトを、ライト・ダークテーマとスマートフォンでも使えるレイアウトを備えた新しいデザインにしました。目次のあるページでは本文の横に目次を表示し、読んでいるセクションを示します。ボタンでコマンドや設定ファイルをコピーでき、設定ファイルでは各セクションで変更する行を示します。リリースノートは展開して詳しい説明を表示できます。

  [`5bc14b5`](https://github.com/pgbackrest/pgbackrest/commit/5bc14b581a054ab3dc9cd633954a689acc99a58f) ドキュメントのタイトルを短くし、曖昧さを解消しました。

  [`b668d71`](https://github.com/pgbackrest/pgbackrest/commit/b668d71f22489cbd4d5e120e7e6e73be0ca9e167) トップページのスポンサー欄を下へ移し、支援の呼びかけを短くしました。

  [`60b85c5`](https://github.com/pgbackrest/pgbackrest/commit/60b85c58d98dd65d47747e6355f47c934cd6b430) ウェブサイトを刷新しました。

  [`ab8df23`](https://github.com/pgbackrest/pgbackrest/commit/ab8df23807cc4c11768ef40196bcade70ebec23a) リンクを投稿した際に、ロゴではなくカードを表示するようにしました。

  [`76ae494`](https://github.com/pgbackrest/pgbackrest/commit/76ae49456c7dace20bbd6f17e8acdfd36bf03a46) リリースページから目次を削除し、日付の周囲の間隔を詰めました。

  [`3e86c71`](https://github.com/pgbackrest/pgbackrest/commit/3e86c71f5546c86941f35d5be3a7fdcd98af3cca) コマンドリファレンスでは、オプションを繰り返し掲載する代わりにリンクを設けました。

  [`dc3af7b`](https://github.com/pgbackrest/pgbackrest/commit/dc3af7b2aee5778dbe9200e31d5a2f95ecae5777) コマンドリファレンスのコマンドタイトルを明確にしました。

  [`078d52c`](https://github.com/pgbackrest/pgbackrest/commit/078d52c5768bb67989624b5418fdd687fab9e485) 設定ファイルで各セクションが変更する行を示すようにしました。

  [`bd33623`](https://github.com/pgbackrest/pgbackrest/commit/bd33623ba945ed251e2a6704cea14a81d51c2c9e) 設定ファイルと同じ方法でコマンドの出力にも印を付けるようにしました。

  [`578fc2d`](https://github.com/pgbackrest/pgbackrest/commit/578fc2de14a6a739401fd58b9a232cf587c52fb4) 設定ファイルに加え、コマンドもコピーできるようにしました。

  [`1fb93f9`](https://github.com/pgbackrest/pgbackrest/commit/1fb93f92725124d6afa8953b7c7243aee92fcaf5) 設定セクションに読者が確認できる変更が何もない場合はエラーとしました。

  [`2f3b2f2`](https://github.com/pgbackrest/pgbackrest/commit/2f3b2f22a30a35340549d42b09d5aaa58d9dfe61) サイトロゴをホームへのリンクにしました。

  [`8f902c6`](https://github.com/pgbackrest/pgbackrest/commit/8f902c66609c0bf1de6720e60552adde515209cd) ドキュメントのビルドを高速化しました。

  [`b56b6ab`](https://github.com/pgbackrest/pgbackrest/commit/b56b6ab4d24ff6298b95b415b3115591e311de20) トップページに最新のニュース項目を自動で掲載するようにしました。

  [`5b8987d`](https://github.com/pgbackrest/pgbackrest/commit/5b8987da0bb24fc3979fb764ccbde82b7b0e9500) リファレンス内のオプション型の例をコードブロックとして表示するようにしました。

  [`b5d5274`](https://github.com/pgbackrest/pgbackrest/commit/b5d527471444f90df5529f15726b3d33065f9829) メニューが折り返して画面外に出る代わりに、横方向にスクロールするようにしました。

  [`9ae2c32`](https://github.com/pgbackrest/pgbackrest/commit/9ae2c32a35f56f53f299e8c04f004ed3386b95e4) メニューから現在のページを除く代わりに、強調表示するようにしました。

  [`b8da5b0`](https://github.com/pgbackrest/pgbackrest/commit/b8da5b061d0f9c5d1cc01e936dc65cbdd9f70be7) スタイルとスクリプトのリンクにバージョンを付け、古いキャッシュを再取得するようにしました。

  [`ec57431`](https://github.com/pgbackrest/pgbackrest/commit/ec57431aa88860b9058d971b938afb5e35a142c7) セクションまで滑らかにスクロールせず、直接移動するようにしました。

  [`46babed`](https://github.com/pgbackrest/pgbackrest/commit/46babedaed8429026efa4592d93a8d9876acad0b) メニューが端の先へ続く場合は、端を切り落とさずフェード表示するようにしました。

  [`17de501`](https://github.com/pgbackrest/pgbackrest/commit/17de50192b7e40d7517a4079451e93da5c39b3f3) section2見出しの線を、タイトルの横ではなく下に配置しました。

  [`940f431`](https://github.com/pgbackrest/pgbackrest/commit/940f4311375dda3caabdc0bdd01c36bedf43d46f) ページタイトルをロゴの横で中央揃えにし、折り返す場合は左揃えにしました。

  [`050ca9e`](https://github.com/pgbackrest/pgbackrest/commit/050ca9e354421530ba4282d95dead90e31d6dc2a) リリースノートに展開可能な詳細を追加しました。

  [`bd8f99b`](https://github.com/pgbackrest/pgbackrest/commit/bd8f99be00cd4b03a1b234bf7fbaa39f406c0c44) v2.33からv2.60までのリリースノートに詳細を追加しました。

  [`28a1e3d`](https://github.com/pgbackrest/pgbackrest/commit/28a1e3d6278992e0a347aab19248abdcddefd491) ライトモードでのキーワードの表示スタイルを調整しました。

  [`1911f5f`](https://github.com/pgbackrest/pgbackrest/commit/1911f5f1744ff4bfee528d95e37a0a8d9b77d6b3) リリースノートの履歴を、アップストリームのCIへの統合時点までとしました。
- リリース予定を文書化しました。

  機能リリースは1月、4月、7月、10月の第3月曜日に予定されています。それ以外の月は、必要に応じて第3月曜日にパッチリリースを行います。リリースノートの導入部にも、リリース番号を構成するメジャー、マイナー、パッチについて説明を追加しました。

  [`9bca69a`](https://github.com/pgbackrest/pgbackrest/commit/9bca69a591abcee0623ff910d0db3e27008cfc25) リリース予定を文書化しました。

  [`c179f3f`](https://github.com/pgbackrest/pgbackrest/commit/c179f3f7d6d6b1963d9d3b98b981786ef9546022) リリースノートの導入部でリリース番号の説明を更新しました。
- ドキュメント用ツールをCとPerlからPythonに移行しました。

  ドキュメントは、`doc/doc.pl`が実行するCツールの代わりに`doc/doc.py`でビルドするようになり、ドキュメントのビルドにPerlは不要になりました。

  [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e) ビルドとドキュメントのコードをCからPythonに移行しました。

  [`fa3d197`](https://github.com/pgbackrest/pgbackrest/commit/fa3d1979b77d6252642c64d708a951914e0a0ac2) 残りのドキュメント用コードをPerlからPythonに移行しました。

**テストスイートの改善：**

- テストハーネスをCとPerlからPythonに移行しました。

  テストは`test/test.pl`の代わりに`test/test.py`で実行するようになりました。テスト用コンテナーとCIランナーでPerlは不要になり、ハーネス自体もテストの対象になりました。

  [`163e5ba`](https://github.com/pgbackrest/pgbackrest/commit/163e5ba0f9ff72ec730f0b35ddac0e5d68ece531) テストハーネスをCからPythonに移行しました。

  [`e25c662`](https://github.com/pgbackrest/pgbackrest/commit/e25c6621e8427e862e4ce0196d059ab651bb276d) テストハーネスの残りをPerlからPythonに移行しました。
- CIにFil-Cのジョブを追加しました。

  Fil-Cは、すべてのポインターアクセスを検査する、メモリー安全性を備えたCの実装です。gcc、clang、Valgrindが見逃した2件の範囲外読み取りを検出しました。また、新しいワークフローでは、CIランナー上でgccとclangを使い、オプションのライブラリーがある場合とない場合の両方でビルドとテストを実行します。

  [`f32a5d5`](https://github.com/pgbackrest/pgbackrest/commit/f32a5d5543c4dc547006629bdb2dd52d3edb9205) コンテナーを使わず、ランナー上でコンパイルとテストを行うワークフローを追加しました。

  [`12396fb`](https://github.com/pgbackrest/pgbackrest/commit/12396fb353bc4aa10c3739b826189e421732adf5) コンパイルのワークフローにFil-Cのジョブを追加しました。

  [`908a11a`](https://github.com/pgbackrest/pgbackrest/commit/908a11a841e85d4e66e4aa551380b52aabfe606f) 必要なライブラリーがすべて含まれるようになったため、Fil-Cの配布物をそのまま使用するようにしました。
- `JSON`、`Ini`、`Pack`の読み取り処理にファジングテストを追加しました。

  CIでlibFuzzer、AddressSanitizer、UndefinedBehaviorSanitizerを使い、読み取り処理をファジングします。無効な入力の読み取り方に複数の不具合が見つかりました。たとえば、情報ファイルやオブジェクトストアの応答に含まれる深く入れ子になったJSON配列で、メモリーコンテキストのスタックがオーバーフローする可能性がありました。

  コミット [`4c65010`](https://github.com/pgbackrest/pgbackrest/commit/4c65010e7d28ea68571732fb275d91266a97ad80)
- Debianのadduserが拒否するテストユーザー名を使用できるようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  テスト用コンテナーは、ホストユーザーと同じユーザー名でビルドします。Debianの`adduser`は`first.last`のようにドットを含む名前を拒否するため、このようなユーザー名ではDebianベースのイメージでコンテナーのビルドが失敗していました。

  課題 [#2858](https://github.com/pgbackrest/pgbackrest/issues/2858); プルリクエスト [#2859](https://github.com/pgbackrest/pgbackrest/pull/2859); コミット [`ce19dae`](https://github.com/pgbackrest/pgbackrest/commit/ce19dae6a2d6ab3665374ead04c270fd45d563fb)


--------

## 安定版リリース {#stable-releases}

### v2.59.3リリースノート {#v2593-release-notes}

*脆弱な暗号化サブキーのバグ*

*2026年10月4日リリース*

**重要な注意事項**：以前のバージョンでは、システムのランダムデータへのアクセス時にエラーが発生すると、脆弱な暗号化サブキーやソルトが生成される可能性がありました。詳細は[脆弱な暗号化サブキーとソルト](/ja/pgbackrest/news/#weak-encryption)を参照してください。

**バグ修正:**

- 暗号化された情報ファイルとマニフェストの読み込み時にチェックサムエラーが発生する可能性がある問題を修正。 (*修正： j0uinim。レビュー： David Steele。*)

  暗号化された大きな情報ファイルやマニフェストファイルを読み込む際、末尾の行が失われてチェックサム検証に失敗することがありました。失われる行が最後の暗号ブロック内に収まる必要があるため、実際に発生する可能性は低い問題です。

  課題 [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); プルリクエスト [#2868](https://github.com/pgbackrest/pgbackrest/pull/2868); コミット [`2def063`](https://github.com/pgbackrest/pgbackrest/commit/2def063e06c6f0b7e137309c7ed0d7631a42f6cf)
- 脆弱な暗号化サブキーやソルトが生成される可能性がある問題を修正。 (*修正： j0uinim。レビュー： David Steele, Stefan Fercot, Douglas J Hunley。*)

  OpenSSLがオペレーティングシステムからランダムデータを取得できなかった場合、その失敗を無視し、ランダムでないメモリーの内容からサブキーとソルトを生成していました。現在はエラーを報告します。

  課題 [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); プルリクエスト [#2867](https://github.com/pgbackrest/pgbackrest/pull/2867); コミット [`47ed78f`](https://github.com/pgbackrest/pgbackrest/commit/47ed78f8d54a44466a872852939edc0273172bf1)

### v2.59.2リリースノート {#v2592-release-notes}

*PostgreSQL 19beta4のサポート*

*2026年9月27日リリース*

**バグ修正：**

- バックアップ中にファイルがゼロサイズに切り詰められた場合の、空のブロックマップの問題を修正しました。 (*レビュー：Douglas J Hunley。報告：JPCOSTA78。*)

  `repo-bundle-limit`を超えるブロック増分ファイルがバックアップ中にPostgreSQLによってゼロに切り詰められると、ブロックを含まないブロックマップとして格納されていました。その後、そのファイルを参照するバックアップはすべて、次のフルバックアップまで"unexpected eof"で失敗していました。

  課題 [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); プルリクエスト [#2842](https://github.com/pgbackrest/pgbackrest/pull/2842); コミット [`572d163`](https://github.com/pgbackrest/pgbackrest/commit/572d1631026d5f10915634592b547f3439b7a291)
- ドライバーにフィルターが渡された場合、読み取りの再試行を無効にしました。 (*レビュー：Douglas J Hunley。報告：megamaced。*)

  リポジトリホスト経由でアクセスするオブジェクトストア上のリポジトリで、読み取りを再試行するとクラッシュしていました。これらの読み取りは、クライアント側では再試行しなくなりました。リポジトリホストによるオブジェクトストアからの読み取りは、引き続き再試行します。

  課題 [#2845](https://github.com/pgbackrest/pgbackrest/issues/2845); プルリクエスト [#2846](https://github.com/pgbackrest/pgbackrest/pull/2846); コミット [`c6eca28`](https://github.com/pgbackrest/pgbackrest/commit/c6eca28ff8e551bd2e76f0c91b1a70ddee60b35e)
- S3バージョン一覧のページ分割を修正しました。 (*レビュー：Douglas J Hunley, guruguruguru。報告：guruguruguru。*)

  あるプレフィックス配下に1,000件を超えるバージョンが列挙されると、`repo-target-time`で指定時点のリポジトリを読み取る処理が"unable to find child 'NextContinuationToken'"で失敗していました。

  課題 [#2854](https://github.com/pgbackrest/pgbackrest/issues/2854); プルリクエスト [#2855](https://github.com/pgbackrest/pgbackrest/pull/2855); コミット [`6f0490d`](https://github.com/pgbackrest/pgbackrest/commit/6f0490dd29f0c756e6766fd9be023805540815fc)
- `SAS`認証用のAzureバージョンヘッダーを設定するようにしました。 (*レビュー：Douglas J Hunley。報告：Florian Helmberger。*)

  バッチ削除にはバージョンヘッダーが必要なため、`SAS`認証ではすべてのバッチが拒否されていました。この拒否は1ファイルの失敗に見え、各バッチの残りは削除されないまま`expire`が成功を報告していたため、期限切れのバックアップとWALがリポジトリに残っていました。

  課題 [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); プルリクエスト [#2848](https://github.com/pgbackrest/pgbackrest/pull/2848); コミット [`ea3293b`](https://github.com/pgbackrest/pgbackrest/commit/ea3293be75c86b5e6c9ca4158b5ebe2a3224f76f)
- サイズがゼロのバックアップ履歴ファイルで、非同期`archive-push`が停止する問題を修正しました。 (*修正：Andrew Kroh。レビュー：David Steele, Douglas J Hunley。*)

  たとえばストレージスナップショットからコピーしたクラスターにサイズゼロのバックアップ履歴ファイルがあると、非同期`archive-push`が毎回失敗し、WALがまったくアーカイブされませんでした。現在は、最初の転送準備済みWALセグメントのサイズを使い、`archive-push-batch-size`をセグメント数に換算します。

  課題 [#2856](https://github.com/pgbackrest/pgbackrest/issues/2856); プルリクエスト [#2857](https://github.com/pgbackrest/pgbackrest/pull/2857); コミット [`12b1b3c`](https://github.com/pgbackrest/pgbackrest/commit/12b1b3cf58caee7b04ed788eee221726f5caa155)
- リモートの暗号化リポジトリに対する`annotate`コマンドを修正しました。 (*修正：Douglas J Hunley。レビュー：David Steele。*)

  リポジトリが暗号化されていて、暗号の設定がリポジトリホストにしかない場合、`annotate`は`backup.info`の読み込みに失敗していました。

  コミット [`497ad5a`](https://github.com/pgbackrest/pgbackrest/commit/497ad5aee0c654611d2ad4185958727e1341dd8c)

**新機能：**

- PostgreSQL 19beta4/rc1をサポートしました。

  PostgreSQL 19beta4でオンラインでのページチェックサム変更が取り消され、ページチェックサムのバージョンは再び0と1だけになりました。`pg_control`のバージョンとWALページのマジックナンバーも変更されました。

  コミット [`89eae83`](https://github.com/pgbackrest/pgbackrest/commit/89eae839d5ca79591aaea8157f437688c3b53df4)

### v2.59.1リリースノート {#v2591-release-notes}

*PostgreSQL 19beta3のサポート*

*2026年8月17日リリース*

**バグ修正：**

- チャンクバッファーが入力バッファーより小さい場合、ハングする問題を修正しました。 (*レビュー：Andrew Pogrebnoi, Douglas J Hunley。報告：crajac66。*)

  S3、GCS、Azureへのマルチパートアップロードで、チャンクバッファーが入力バッファーより小さいと、たとえばアップロード中にチャンクサイズが増えた後などに、無限ループになる可能性がありました。現在は、チャンクバッファーを常に入力バッファーが収まるサイズにします。

  課題 [#2818](https://github.com/pgbackrest/pgbackrest/issues/2818); プルリクエスト [#2819](https://github.com/pgbackrest/pgbackrest/pull/2819); コミット [`a53e470`](https://github.com/pgbackrest/pgbackrest/commit/a53e470eca258c2db088af55be307403c8f43b7a)
- 新しいバックアップラベルの比較対象を、そのラベルが属するフルバックアップセットのみに限定しました。 (*レビュー：Douglas J Hunley。報告：Anton Glushakov。*)

  オブジェクトロックを使うMinIOやSeaweedFSなど、一部のオブジェクトストアでは、配下をすべて削除した後もプレフィックスが一覧に残るため、削除済みのフルバックアップがリポジトリに存在するように見えることがありました。その後の差分・増分バックアップはすべて"new backup label ... is not later than latest backup label ..."で失敗していました。現在は、新しいラベルを同じフルバックアップセット内のバックアップとだけ比較します。

  課題 [#2792](https://github.com/pgbackrest/pgbackrest/issues/2792); プルリクエスト [#2824](https://github.com/pgbackrest/pgbackrest/pull/2824); コミット [`d01f77e`](https://github.com/pgbackrest/pgbackrest/commit/d01f77e8237f5d008bb7782c18ced12cd6d1971a)
- GitHubが生成するソースアーカイブに、ビルドに必要なファイルが含まれない問題を修正しました。 (*報告：aardvarkzed。*)

  GitHubがリリース用に生成するソースアーカイブには、コード生成ツールとその入力ファイルが含まれておらず、ビルドできませんでした。現在は、配布用tarballだけから不要なファイルを除きます。

  課題 [#2821](https://github.com/pgbackrest/pgbackrest/issues/2821); コミット [`163670a`](https://github.com/pgbackrest/pgbackrest/commit/163670a4eeede6d2d170b5d1f55c5ba0b66ba564)

**新機能：**

- PostgreSQL 19beta3をサポートしました。 (*貢献：Lardière Sébastien。レビュー：David Steele。*)

  PostgreSQL 19beta3でWALページのマジックナンバーが変更されました。

  コミット [`5cbc256`](https://github.com/pgbackrest/pgbackrest/commit/5cbc256bf37a44fa478d73a12a2e5b2d84fa6337)

**ドキュメントの改善：**

- `repo-s3-uri-style=path`の場合の、S3バケット名に含まれるドットの例外を説明しました。

  `repo-s3-uri-style=path`では、バケットはホスト名ではなくパスの一部になるため、バケット名にドットが含まれていても証明書のホスト名不一致は発生しません。

  コミット [`bbdc4b9`](https://github.com/pgbackrest/pgbackrest/commit/bbdc4b9217a0e66f6a01c05f4edc04282cffb3fc)
- ユーザーガイドから`hot_standby`の明示的な設定を削除しました。

  `hot_standby`はPostgreSQL 10以降、デフォルトで有効です。クイックスタートには、これを有効にしないとスタンバイが読み取り専用接続を受け付けない旨を記載しました。

  コミット [`cda454d`](https://github.com/pgbackrest/pgbackrest/commit/cda454d4bac0c0412230a0b41513659a7d0d4205)

### v2.59.0リリースノート {#v2590-release-notes}

*PostgreSQL 19beta2のサポート*

*2026年7月20日リリース*

**パッケージ作成者への注意**：生成済みのHTMLドキュメント、manページ、コードを含み、ビルド手順を簡素化する新しい配布用tarballを提供します。各リリースのアセットとして添付され、名前は`pgbackrest-{version}.tar.gz`です。詳細はtarball内の`README.md`を参照してください。今後のリリースでコード生成に必要となる追加のビルドツールを避けるため、新しい配布用tarballを使用してください。詳細は[新しい配布用tarball](/ja/pgbackrest/news/#distribution-tarball)を参照してください。<br/> <br/> **パッケージ作成者への注意**：新たに`libsystemd`へのオプションの依存関係を追加しました。<br/> <br/> **重要な注意事項**：このリリース以降、デフォルトでrootとして実行できるのは`restore`コマンドだけです。他のコマンドをrootとして実行するには`allow-root`を使用してください（ただし、推奨しません）。

**バグ修正：**

- `expire`が別のホストで実行中のバックアップを削除する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Dmitrii。*)

  バックアップは完了するまで`backup.info`に追加されないため、別のホストでバックアップを実行中に`expire`を実行すると、たとえばプライマリーのバックアップ中にスタンバイで`expire`を実行すると、実行中のバックアップが削除されていました。現在は、最新のバックアップが実行中または再開可能な場合、期限切れ処理で削除しません。

  課題 [#2622](https://github.com/pgbackrest/pgbackrest/issues/2622); プルリクエスト [#2797](https://github.com/pgbackrest/pgbackrest/pull/2797); コミット [`aa0e215`](https://github.com/pgbackrest/pgbackrest/commit/aa0e215019f50f92a8f0c97f907affc1d3bf86c4)
- WALファイルでエラーが発生した場合、`archive-push-queue-max`が適用されない問題を修正しました。 (*レビュー：Stefan Fercot。報告：vut12。*)

  非同期モードでは、まだ転送していないWALだけを対象にキューのサイズを測っていました。あるWALファイルでエラーが続くと、その後のWALファイルは転送されて対象外になりますが、`pg_wal`には残るため、キューの上限に達しないまま`pg_wal`がディスクを埋める可能性がありました。現在は、同期モードと同様に、PostgreSQLがアーカイブを待っているすべてのWALを対象にキューのサイズを測ります。

  課題 [#2629](https://github.com/pgbackrest/pgbackrest/issues/2629); プルリクエスト [#2799](https://github.com/pgbackrest/pgbackrest/pull/2799); コミット [`7fe3636`](https://github.com/pgbackrest/pgbackrest/commit/7fe363658639bbc2f70e53496fa6da4acb9e481e)
- タイムラインの切り替えをまたぐリカバリー中に、非同期`archive-get`が失敗する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Jimmy Yih。*)

  2つの非同期プロセスがアーカイブロックを競合し、取得できなかったプロセスが、取得を依頼されたセグメントを取りに行く前に終了することがありました。起動元の`archive-get`は`archive-timeout`まで待った後、存在するセグメントに対してエラーを返すため、特にタイムラインの切り替え時にはリカバリが早期に終了する可能性がありました。現在は、取得を担当する非同期プロセスが動作していない場合、そのセグメントを直接取得します。

  課題 [#2423](https://github.com/pgbackrest/pgbackrest/issues/2423); プルリクエスト [#2806](https://github.com/pgbackrest/pgbackrest/pull/2806); コミット [`baed942`](https://github.com/pgbackrest/pgbackrest/commit/baed942af0d61fcf3c2cb1f7d1bf1d6fe5bb6df9)
- エラーモジュールでバッファーオーバーランが起こり得る問題を修正しました。 (*修正：Christophe Pettus。レビュー：David Steele。*)

  バッファーに収まらない長さのスタックトレースに終端が付かず、バッファーの末尾を超えて読み取る可能性がありました。また、バッファーに収まらない長さのエラーメッセージにシステムエラーを付加すると、末尾を超えて書き込む可能性がありました。いずれも通常より非常に長いメッセージで発生する問題です。

  [`7fd8bc8`](https://github.com/pgbackrest/pgbackrest/commit/7fd8bc89a15cb039111aa85fd37f9dc68f7c4d6d) エラーモジュールでバッファーオーバーランが起こり得る問題を修正しました。

  [`5ca98ab`](https://github.com/pgbackrest/pgbackrest/commit/5ca98abc91f823ef97ff6a1e77d65727d1259218) エラーメッセージの整形時にバッファー全体を使用するようにしました。

  [`3a71dc8`](https://github.com/pgbackrest/pgbackrest/commit/3a71dc839a89b83f592c1d5813c068bcded1b6bc) 長すぎるメッセージでエラーバッファーの範囲外に書き込まないようにしました。
- 並列プロトコルクライアントでの解放済みメモリーの使用を修正しました。 (*レビュー：Douglas J Hunley。報告：Georgy Shelkovy。*)

  処理する仕事がなくなったクライアントを解放してもクライアント一覧に残していたため、後続の呼び出しで再び解放していました。debugやtraceのログ出力を有効にすると解放済みメモリーを読み取り、たとえば`log-level-file=trace`を指定した並列バックアップでクラッシュする可能性がありました。

  課題 [#2754](https://github.com/pgbackrest/pgbackrest/issues/2754); プルリクエスト [#2804](https://github.com/pgbackrest/pgbackrest/pull/2804); コミット [`31432ed`](https://github.com/pgbackrest/pgbackrest/commit/31432ed3977302b5e183f2b592d85afb521b4f55)
- pg1を設定せずにpgオプションを設定すると、ヒープオーバーフローが発生する問題を修正しました。 (*レビュー：Douglas J Hunley。報告：Naveen。*)

  `pg1-path`を設定せずに、`pg2-path`や`pg3-path`など他のインデックスの`pg`オプションを設定すると、インデックスマップが上書きされていました。Alpineなどのmusl環境では、これがヒープを破壊し、セグメンテーションフォールトを引き起こしていました。また、最大番号の`pg-path`も失われていました。

  課題 [#1768](https://github.com/pgbackrest/pgbackrest/issues/1768); プルリクエスト [#2796](https://github.com/pgbackrest/pgbackrest/pull/2796); コミット [`2d767de`](https://github.com/pgbackrest/pgbackrest/commit/2d767de3c59cf5570639e75755dc73c626fb99e1)
- musl 1.2.6で終了処理中にシグナルが届くとクラッシュする問題を修正しました。

  Alpine 3.24などで使われるmusl 1.2.6は、終了処理が進行中に`exit()`を呼ぶとクラッシュします。これは、終了処理中にシグナルが届いた場合、たとえば`server`コマンドがすでに終了処理中の子プロセスを終了させた場合に発生していました。現在は、終了処理中に届いたシグナルを無視します。

  コミット [`e166a33`](https://github.com/pgbackrest/pgbackrest/commit/e166a33f48a00192c09b0f1cea3465243c03d1f1)

**新機能：**

- PostgreSQL 19beta1/beta2をサポートしました。 (*レビュー：Stefan Fercot。*)

  PostgreSQL 19beta1/beta2のサポートを追加しました。PostgreSQL 19ではページチェックサムをオンラインで有効化・無効化でき、いずれかの処理中はページチェックサムを検証しません。

  [`bc6d399`](https://github.com/pgbackrest/pgbackrest/commit/bc6d399a6a160f5fa41dd3a98ae046dff66e56a8) PostgreSQL 19beta1をサポートしました。; プルリクエスト [#2779](https://github.com/pgbackrest/pgbackrest/pull/2779)

  [`2777395`](https://github.com/pgbackrest/pgbackrest/commit/2777395dacc35aec51572d3e75c621725e2f9d9c) PostgreSQL 19beta2をサポートしました。
- WALアーカイブを整理する`archive-expire-before`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  `expire`の`archive-expire-before`オプションは、指定したセグメントより前のWALをアーカイブから削除しますが、保持するバックアップが必要とするWALは削除しません。保持ポリシーを認識しない`pg_archivecleanup`の代わりに、`archive_cleanup_command`で使用して、スタンバイのリスタートポイントより前のアーカイブを整理できます。

  [`6cd692b`](https://github.com/pgbackrest/pgbackrest/commit/6cd692b1b321faf544ee3a9b1f503fd48007d7c7) WALの期限切れ処理をexpireArchiveId()に切り出しました。

  [`4945139`](https://github.com/pgbackrest/pgbackrest/commit/4945139392c21f197f2e307abc3c89b5548cef8d) WALアーカイブを整理する`archive-expire-before`オプションを追加しました。; プルリクエスト [#2801](https://github.com/pgbackrest/pgbackrest/pull/2801)
- Azureストレージの一括削除を追加しました。 (*レビュー：Douglas J Hunley, Crispy。*)

  ファイルごとにリクエストを送る代わりに、Azure Blob Batch APIで1リクエストあたり最大256ファイルを削除します。これにより、`expire`などリポジトリからファイルを削除するコマンドが高速化します。

  プルリクエスト [#2786](https://github.com/pgbackrest/pgbackrest/pull/2786); コミット [`ffa325b`](https://github.com/pgbackrest/pgbackrest/commit/ffa325b8a44c1e9e44dc038bbcc8aece6f312a90)
- S3 Outpostsのサポートを追加しました。 (*貢献：Shiva Kumar Ambigi。レビュー：David Steele, Roberto Mello。*)

  S3 Outpostsのエンドポイントを使う場合は、`repo-s3-service=s3-outposts`を設定します。このオプションはリクエスト署名に使うサービス名を指定し、デフォルトは`s3`です。

  プルリクエスト [#2762](https://github.com/pgbackrest/pgbackrest/pull/2762); コミット [`6c51800`](https://github.com/pgbackrest/pgbackrest/commit/6c518001c24ad2405eaf750d358f69703322a221)
- S3のプロセス認証を追加しました。 (*レビュー：Andrew Charlton。提案：Andrew Charlton。*)

  `repo-s3-key-type=process`を設定し、`repo-s3-process-cmd`にAWSのプロセス認証情報プロバイダーのJSON形式で一時的な認証情報を出力するコマンドを指定します。認証情報は有効期限が切れる前に更新します。

  プルリクエスト [#2778](https://github.com/pgbackrest/pgbackrest/pull/2778); コミット [`b5a578a`](https://github.com/pgbackrest/pgbackrest/commit/b5a578a5c2c88d53fca0ee8cfbfb8ee662ce7e48)
- 生成済みのコードとドキュメントを含む配布用tarballを提供します。

  tarballには生成済みコードとレンダリング済みのmanページおよびHTMLドキュメントが含まれるため、`libyaml`を含むコード生成・ドキュメント用ツールなしでビルドとインストールができます。

  コミット [`8fcfef5`](https://github.com/pgbackrest/pgbackrest/commit/8fcfef5d8732055f9bc8e50224d5b7a988512e61)

**改善：**

- サーバーがアイドル接続を切断した後、SFTPストレージに再接続するようにしました。 (*レビュー：Stefan Fercot。提案：mustafa0x, tisserat。*)

  SFTPサーバーやファイアウォールは、しばらく使われていない接続を切断することがあります。たとえばバックアップのコピー処理中のリポジトリ読み取り接続が切れると、次の使用時にソケットエラーになっていました。現在は、切断された接続を開き直し、操作を1回再試行します。

  [`d72bea9`](https://github.com/pgbackrest/pgbackrest/commit/d72bea9fe7c3975fc6832a51b0b0c1c041c467d2) SFTPの読み書きオブジェクトで、ストレージからlibssh2セッションを取得するようにしました。

  [`a31febf`](https://github.com/pgbackrest/pgbackrest/commit/a31febfbd9ba639589fe57e4083ae9358b1306a4) サーバーがアイドル接続を切断した後、SFTPストレージに再接続するようにしました。; 課題 [#2739](https://github.com/pgbackrest/pgbackrest/issues/2739); 課題 [#2772](https://github.com/pgbackrest/pgbackrest/issues/2772); プルリクエスト [#2793](https://github.com/pgbackrest/pgbackrest/pull/2793)
- マニフェストの作成を高速化するユーザー／グループキャッシュを追加しました。 (*貢献：Gunnar Lindholm。レビュー：David Steele。*)

  sssdやLDAPなどのリモート名前サービスでユーザー名とグループ名を検索すると、検索のたびに往復通信が発生するため、数百万のファイルを持つクラスターではマニフェスト作成時間の大半を占めていました。現在は、ユーザー名とグループ名をキャッシュします。

  プルリクエスト [#2773](https://github.com/pgbackrest/pgbackrest/pull/2773); コミット [`1e6d23f`](https://github.com/pgbackrest/pgbackrest/commit/1e6d23fea72ac9c599f8b62a2e0a3de02d0d08d0)
- `info`コマンドの出力に、リポジトリごとのバックアップ進捗を追加しました。 (*貢献：Will Morland。レビュー：David Steele, Stefan Fercot。*)

  複数のリポジトリで同時にバックアップを実行する場合、`info`コマンドは全体の進捗に加えて、リポジトリごとの進捗も報告するようになりました。JSON出力には、バックアップロックごとに`repo`配列を含みます。

  課題 [#2736](https://github.com/pgbackrest/pgbackrest/issues/2736); プルリクエスト [#2740](https://github.com/pgbackrest/pgbackrest/pull/2740); コミット [`77312b3`](https://github.com/pgbackrest/pgbackrest/commit/77312b33ba913132b33401d862c2e354f323c786)
- `verify`コマンドに`backup.info`のチェックを追加しました。 (*貢献：Denis Garsh。レビュー：David Steele, Douglas J Hunley。*)

  `verify`コマンドは、リポジトリ内のバックアップが`backup.info`にない場合や、`backup.info`にあるバックアップがリポジトリにない場合に警告するようになりました。存在しないバックアップは、マニフェストがないものとして報告します。

  課題 [#2723](https://github.com/pgbackrest/pgbackrest/issues/2723); プルリクエスト [#2752](https://github.com/pgbackrest/pgbackrest/pull/2752); コミット [`7f82fb6`](https://github.com/pgbackrest/pgbackrest/commit/7f82fb6635c1e3e9dd285d53076e9aee3fbf1ca2)
- S3 STSエンドポイントを設定できるようにしました。 (*貢献：Simon Gratton。レビュー：David Steele。*)

  `repo-s3-key-type=web-id`でリージョン別STSエンドポイントを使うには、`repo-s3-sts-host`に、たとえば`sts.eu-central-2.amazonaws.com`を設定します。AWSのオプトインリージョンはグローバルエンドポイントの認証情報を受け付けませんが、デフォルトは引き続きグローバルエンドポイントです。

  課題 [#2791](https://github.com/pgbackrest/pgbackrest/issues/2791); プルリクエスト [#2798](https://github.com/pgbackrest/pgbackrest/pull/2798); コミット [`11f5582`](https://github.com/pgbackrest/pgbackrest/commit/11f5582dfe696187cab1f15d08f649a5117730b3)
- 非同期処理1回あたりに送信するWALを制限する`archive-push-batch-size`を追加しました。 (*レビュー：Stefan Fercot。*)

  非同期モードでは、実行開始時にしか`archive-push-queue-max`を確認しないため、大量の未処理WALを処理する間に、キューが上限を大きく超えることがありました。`archive-push-batch-size`（デフォルト16GiB）は1回の実行で転送するWALを制限し、より早くキューを再確認できるようにします。

  プルリクエスト [#2803](https://github.com/pgbackrest/pgbackrest/pull/2803); コミット [`34a035f`](https://github.com/pgbackrest/pgbackrest/commit/34a035f4d62f06822c1f60f72a605762cc1ad79c)
- 最初のエラーで非同期`archive-push`を終了するようにしました。 (*レビュー：Stefan Fercot。提案：Lardière Sébastien。*)

  リポジトリが利用できない場合も、非同期プロセスは転送準備済みのWALセグメントをすべて試し続けていました。そのため、`archive-push-queue-max`を再確認するまでに`pg_wal`がいっぱいになるほど実行が長引くことがありました。現在は、最初のエラー発生後、処理中のジョブが終わった時点で実行を終了します。

  課題 [#1848](https://github.com/pgbackrest/pgbackrest/issues/1848); プルリクエスト [#2802](https://github.com/pgbackrest/pgbackrest/pull/2802); コミット [`a0c1435`](https://github.com/pgbackrest/pgbackrest/commit/a0c14359392e283d88f72e7f9f815d9e78ddfb10)
- HTTPチャンクレスポンスの解析を堅牢にしました。 (*貢献：Shubham。レビュー：David Steele。*)

  チャンク拡張とトレーラーを受け付け、`transfer-encoding`を大文字・小文字を区別せずに比較するようにしました。`transfer-encoding`と`content-length`の両方を含む応答は拒否します。

  プルリクエスト [#2785](https://github.com/pgbackrest/pgbackrest/pull/2785); コミット [`34bba82`](https://github.com/pgbackrest/pgbackrest/commit/34bba828c6ba97579d65c2199c02d94bf31257a5)
- `allow-root`が有効でない限り、rootとして実行するとエラーになるようにしました。 (*レビュー：Douglas J Hunley。*)

  `restore`以外のコマンドをrootで実行すると、PostgreSQLユーザーがアクセスできない`backup.info`などのファイルをリポジトリ内に作成する可能性がありました。`allow-root`は`restore`を除くすべてのコマンドでデフォルトで無効になり、この確認はリモートホストにも適用されます。

  課題 [#1693](https://github.com/pgbackrest/pgbackrest/issues/1693); プルリクエスト [#2812](https://github.com/pgbackrest/pgbackrest/pull/2812); コミット [`0daf53d`](https://github.com/pgbackrest/pgbackrest/commit/0daf53da03fb179b5771b6aaa559f9e0cc5842bb)
- マニフェスト作成時の二分探索の回数を減らしました。 (*貢献：Gunnar Lindholm。レビュー：David Steele。*)

  差分・増分バックアップのマニフェスト作成時、各ファイルについて以前のマニフェストを3回検索していました。現在は1回だけ検索するため、数百万のファイルを持つクラスターでは数百万回の検索を削減できます。

  プルリクエスト [#2774](https://github.com/pgbackrest/pgbackrest/pull/2774); コミット [`f1ef629`](https://github.com/pgbackrest/pgbackrest/commit/f1ef62956adabf305a7e959477ea1bb668fd8d65)
- ブロック増分バックアップの差分リストアにおけるシーク性能を改善しました。 (*レビュー：David Christensen, Douglas J Hunley。*)

  ブロック増分の差分復元では、ブロックを書き込むたびにシークと書き込みバッファーのフラッシュを行っており、多くのブロックは8KiBでした。現在はファイル位置を追跡し、必要な場合にだけシークとフラッシュを行います。

  プルリクエスト [#2732](https://github.com/pgbackrest/pgbackrest/pull/2732); コミット [`b908d5e`](https://github.com/pgbackrest/pgbackrest/commit/b908d5e2c5b37ef968f19e2c40a1001e19e5b87f)
- より収まりのよいファイルを探すのではなく、順番にバックアップファイルをバンドルするようにしました。 (*レビュー：Stefan Fercot。*)

  バンドルが`repo-bundle-size`を超える原因となるファイルは飛ばし、キューの後ろにある小さいファイルを選んでいました。現在は順番にファイルを追加し、`repo-bundle-size`に達した時点でバンドルを閉じます。そのため、バンドルは最大で`repo-bundle-limit`分だけこのサイズを超えることがあります。

  プルリクエスト [#2794](https://github.com/pgbackrest/pgbackrest/pull/2794); コミット [`253dbc3`](https://github.com/pgbackrest/pgbackrest/commit/253dbc3f03e5581c98bb97b252dc77b8defd3693)
- クエリーが完了しない場合、原因となったエラーを報告するようにしました。 (*レビュー：Andrew Pogrebnoi。提案：Marco Fontana。*)

  たとえば高負荷時など、クエリの最初の結果を受け取った後で接続が切れると、汎用的な"NULL result required to complete request"エラーを報告していました。現在はPostgreSQLのエラーを報告し、接続切断や、厳しすぎる`idle_session_timeout`と`idle_in_transaction_session_timeout`設定についてのヒントも表示します。

  課題 [#2789](https://github.com/pgbackrest/pgbackrest/issues/2789); プルリクエスト [#2790](https://github.com/pgbackrest/pgbackrest/pull/2790); コミット [`23e966c`](https://github.com/pgbackrest/pgbackrest/commit/23e966cd8f17a8cd446b04901d0ae66ebf4118ee)
- S3認証情報の取得リクエストが失敗した場合、実際のエラーを報告するようにしました。 (*レビュー：Douglas J Hunley。提案：Mitchell Grice。*)

  `web-id`や`pod-id`の認証情報リクエストに対してAWSが返したエラーを、応答の解析失敗として報告していました。現在はAWSから返されたエラーを報告し、リクエストをログに記録する際はトークンを伏せます。

  課題 [#1997](https://github.com/pgbackrest/pgbackrest/issues/1997); プルリクエスト [#2808](https://github.com/pgbackrest/pgbackrest/pull/2808); コミット [`b0c57c2`](https://github.com/pgbackrest/pgbackrest/commit/b0c57c280d727e743b72a6d86e2c3e413307e44b)
- `archive-push`のスプールパスのエラーを、PostgreSQLのログに報告するようにしました。 (*レビュー：Douglas J Hunley。提案：Don Seiler。*)

  権限不足などで非同期スプールパスを作成できないと、エラーをスプールに書き込めず、`archive-push`は非同期ログを参照する汎用的なタイムアウトで失敗していました。現在は非同期プロセスの起動前にスプールパスを作成するため、エラーがPostgreSQLのログに現れます。

  課題 [#1408](https://github.com/pgbackrest/pgbackrest/issues/1408); プルリクエスト [#2810](https://github.com/pgbackrest/pgbackrest/pull/2810); コミット [`7b0159c`](https://github.com/pgbackrest/pgbackrest/commit/7b0159c7dfd69763b63b1385fd564c18a4a5c1bc)
- バージョンが未サポートの場合、pgBackRestが古い可能性を示すヒントを追加しました。

  pgBackRestがPostgreSQLのバージョンを認識しない場合、たとえば復元ホストの古いpgBackRestが新しいクラスターのバックアップを読む場合、すべてのホストでpgBackRestの更新が必要かもしれないというヒントを表示するようになりました。バージョンは130000ではなく13のように、ユーザー向けの形式で報告します。

  コミット [`d4f697e`](https://github.com/pgbackrest/pgbackrest/commit/d4f697ebce705f9439798f970103fd38f829dfff)
- systemd notifyとの連携を追加しました。 (*貢献：Andrew Jackson。レビュー：David Steele。*)

  `libsystemd`を組み込んでビルドすると、`server`コマンドはPostgreSQLやPgBouncerと同様に、接続を受け付ける準備ができた時点と停止時にsystemdへ通知します。

  課題 [#2757](https://github.com/pgbackrest/pgbackrest/issues/2757); プルリクエスト [#2760](https://github.com/pgbackrest/pgbackrest/pull/2760); コミット [`742fff1`](https://github.com/pgbackrest/pgbackrest/commit/742fff174a3f5baaed932afa284334ca2aa1be82)
- mesonによるコンパイラーの機能検査で、`unused parameter`エラーを抑制しました。 (*貢献：Jörg Plate。レビュー：David Steele。*)

  mesonのコンパイラー検査は、使用しない`main()`の引数を宣言していたため、未使用引数の警告をエラーとして扱う設定では検査に失敗していました。

  課題 [#2724](https://github.com/pgbackrest/pgbackrest/issues/2724); コミット [`d4465bd`](https://github.com/pgbackrest/pgbackrest/commit/d4465bd6f78d6d58d18ebedbe8f63b55d0ae2508)
- Cの最低要件をC11にしました。 (*レビュー：Mohammad Ali Nazir Kosar。*)

  プルリクエスト [#2738](https://github.com/pgbackrest/pgbackrest/pull/2738); コミット [`3a6c671`](https://github.com/pgbackrest/pgbackrest/commit/3a6c67183cd9c6a12c24f0d978ef5e501b7c3fcf)

**ドキュメントの改善：**

- `repo-*`コマンドの`stanza`オプションを内部用としました。 (*レビュー：Stefan Fercot。*)

  `stanza`オプションが`repo-*`コマンドに影響するのは、文書化されていないストレージパス定数を使う場合だけでしたが、ドキュメントはそれ以外にも作用するかのような説明になっていました。これらのコマンドではこのオプションを文書化しなくなりましたが、動作は従来どおりです。

  課題 [#2735](https://github.com/pgbackrest/pgbackrest/issues/2735); コミット [`3e9eabd`](https://github.com/pgbackrest/pgbackrest/commit/3e9eabd8a5551cdaeb6bc78a52f000eaf239defb)
- infoがglobalセクションから暗号化設定を読み込むことを説明しました。 (*レビュー：Stefan Fercot。提案：Ron Johnson。*)

  `stanza`を指定せずに実行した`info`コマンドは、グローバルセクションからしか暗号化設定を読み取らないため、スタンザ単位の暗号化設定を使うには`stanza`の指定が必要です。

  課題 [#1407](https://github.com/pgbackrest/pgbackrest/issues/1407); プルリクエスト [#2805](https://github.com/pgbackrest/pgbackrest/pull/2805); コミット [`2137bda`](https://github.com/pgbackrest/pgbackrest/commit/2137bda1a5a1ad890d0137feffe8491102041af3)
- `expire-auto`が`backup`コマンドの設定を使うことを説明しました。 (*レビュー：Stefan Fercot。提案：Lardière Sébastien。*)

  バックアップ後の自動期限切れ処理は`backup`コマンドの設定を使うため、`expire`コマンドにだけ設定したオプションは適用されません。専用の設定が必要な場合は、`expire-auto`を無効にして`expire`を別に実行してください。

  課題 [#1874](https://github.com/pgbackrest/pgbackrest/issues/1874); プルリクエスト [#2807](https://github.com/pgbackrest/pgbackrest/pull/2807); コミット [`cf847f9`](https://github.com/pgbackrest/pgbackrest/commit/cf847f94cd7ab6517ec1abb30075fb53dc75d5f8)
- 専用ユーザーを使う場合の、logrotateの`su`ディレクティブの調整を説明しました。 (*レビュー：Douglas J Hunley。提案：lkanbus。*)

  パッケージが、`postgres`ユーザーでログをローテーションするlogrotate設定をインストールすることがあります。専用ユーザーがリポジトリとログを所有する場合、`su`ディレクティブをそのユーザーに変更しないと、権限エラーでローテーションに失敗します。

  課題 [#2737](https://github.com/pgbackrest/pgbackrest/issues/2737); プルリクエスト [#2809](https://github.com/pgbackrest/pgbackrest/pull/2809); コミット [`bde2c50`](https://github.com/pgbackrest/pgbackrest/commit/bde2c509c923fbe2844c10b0f95c55973378d2ae)
- 設定ファイルでは行末コメントをサポートしないことを説明しました。 (*レビュー：Douglas J Hunley。提案：Alex Richman。*)

  行末コメントは、一部のオプションでは動作しているように見えても、これまで一度もサポートしていません。独立した行に書くコメントだけをサポートします。

  課題 [#1633](https://github.com/pgbackrest/pgbackrest/issues/1633); プルリクエスト [#2811](https://github.com/pgbackrest/pgbackrest/pull/2811); コミット [`8571799`](https://github.com/pgbackrest/pgbackrest/commit/85717992cadbfdabc571fb23914b62b08c7f6f44)

**テストスイートの改善：**

- CIコンテナ内のAlpineのグループ競合を修正しました。 (*貢献：Artur Zakirov。レビュー：David Steele。*)

  テスト用グループの名前を変更する際、メンバーを含むグループエントリーも扱うようにしました。また、Alpineのグループは、まだ存在しない場合にだけ作成します。

  プルリクエスト [#2784](https://github.com/pgbackrest/pgbackrest/pull/2784); コミット [`760dd8d`](https://github.com/pgbackrest/pgbackrest/commit/760dd8db69e7c6e5cbb9c5b7e2067b6813cf4497)

### v2.58.0リリースノート {#v2580-release-notes}

*オブジェクトストレージの改善*

*2026年1月19日リリース*

**重要な注意事項**：`repo-storage-upload-chunk-size`オプションの最小値を引き上げました。新しい最小値は、各ベンダーが許可する最小値に対応しています。

**バグ修正：**

- シグナルハンドラー内のログ出力によるデッドロックを修正しました。 (*修正：Maxim Michkov。レビュー：David Steele。*)

  `gmtime_r()`がロックを保持している間にシグナルが届くと、たとえば`stop`に`--force`を指定してSIGTERMを送ると、シグナルハンドラーのログ出力時にデッドロックする可能性がありました。現在は、シグナルハンドラーのログ出力に非同期シグナル安全な関数だけを使います。

  課題 [#2710](https://github.com/pgbackrest/pgbackrest/issues/2710); プルリクエスト [#2715](https://github.com/pgbackrest/pgbackrest/pull/2715); コミット [`e13c462`](https://github.com/pgbackrest/pgbackrest/commit/e13c462908c6ee25f8795b5d1373981549d4d5cf)

**新機能：**

- S3、GCS、AzureでHTTPをサポートしました。 (*貢献：Will Morland。レビュー：David Steele。*)

  オブジェクトストアのエンドポイントを`http://`で始めることで、TLSなしで接続できるようになりました。エンドポイントにプロトコルを指定しない場合は、引き続きHTTPSを使用します。

  課題 [#2340](https://github.com/pgbackrest/pgbackrest/issues/2340); プルリクエスト [#2703](https://github.com/pgbackrest/pgbackrest/pull/2703); コミット [`2398dd4`](https://github.com/pgbackrest/pgbackrest/commit/2398dd4d432d312b3641e9fbbcbe0487ad43112d)
- 現在の保持設定にかかわらず、最も古いフルバックアップを期限切れにできるようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Ron Johnson。*)

  `expire`の`--oldest`オプションは、たとえばリポジトリの空き容量が少なくなった場合に、保持設定に関係なく、最古のフルバックアップとそれに依存するバックアップを期限切れにします。残った最古のフルバックアップより前のWALも期限切れにします。

  課題 [#2666](https://github.com/pgbackrest/pgbackrest/issues/2666); プルリクエスト [#2709](https://github.com/pgbackrest/pgbackrest/pull/2709); コミット [`bf2b276`](https://github.com/pgbackrest/pgbackrest/commit/bf2b276dc011464b13039630870934fd42ca473c)
- AzureのマネージドIDをサポートしました。 (*貢献：Moiz Ibrar, Matthew Mols。レビュー：David Steele。*)

  認証情報を設定する代わりに、マネージドIDを使って自動取得するには、`repo-azure-key-type=auto`を設定します。認証情報は有効期限が切れる前に更新します。

  課題 [#2023](https://github.com/pgbackrest/pgbackrest/issues/2023); プルリクエスト [#2712](https://github.com/pgbackrest/pgbackrest/pull/2712); コミット [`38f14d7`](https://github.com/pgbackrest/pgbackrest/commit/38f14d73b6a62d06e1ead7942e49a2bb2ae90dab)
- S3 EKS Pod Identityを***試験的に***サポートしました。 (*貢献：Pierre BOUTELOUP。レビュー：David Steele。*)

  認証情報を設定する代わりに、EKS Pod Identityを使って自動取得するには、`repo-s3-key-type=pod-id`を設定します。認証情報は有効期限が切れる前に更新します。

  課題 [#2718](https://github.com/pgbackrest/pgbackrest/issues/2718); プルリクエスト [#2719](https://github.com/pgbackrest/pgbackrest/pull/2719); コミット [`79544f6`](https://github.com/pgbackrest/pgbackrest/commit/79544f64a3ce198f4685f923739def997fcafbce)
- TLS暗号スイートを設定できるようにしました。 (*貢献：Gunnar "Nick" Bluth。レビュー：David Steele。*)

  たとえばコンプライアンス要件に合わせるため、TLS 1.2には`tls-cipher-12`を、TLS 1.3には`tls-cipher-13`を設定します。暗号スイートは、そのプロセスが確立するすべての接続に適用されます。

  [`fbc607a`](https://github.com/pgbackrest/pgbackrest/commit/fbc607a48b1fb4ae65c9f2691c44453f02aef2b8) TLS暗号スイートを設定できるようにしました。; 課題 [#2697](https://github.com/pgbackrest/pgbackrest/issues/2697); プルリクエスト [#2700](https://github.com/pgbackrest/pgbackrest/pull/2700)

  [`91ad655`](https://github.com/pgbackrest/pgbackrest/commit/91ad65537f55aa3825b6c7b626a9e1b7cbb1ad4c) fbc607a4で追加したcommon/io-tlsユニットテストの不安定な結果を修正しました。
- プロセスの優先度を設定できるようにしました。 (*レビュー：Douglas J Hunley。*)

  `priority`は、`nice`と同様に、pgBackRestプロセスのスケジューリング優先度を-20から19の範囲で設定します。値を大きくすると、pgBackRestがPostgreSQLに干渉しにくくなります。

  プルリクエスト [#2693](https://github.com/pgbackrest/pgbackrest/pull/2693); コミット [`0fc7e96`](https://github.com/pgbackrest/pgbackrest/commit/0fc7e96f5addb01e7f6f3585e37d209cc17dd956)

**改善：**

- パス形式のURIを使う場合、S3バケット名にドットを使用できるようにしました。 (*貢献：Joakim Hindersson。レビュー：David Steele。*)

  バケット名のドットが証明書のホスト名不一致を引き起こすのはhost形式のURIだけなので、多くのセルフホスト型S3サービスが使う`repo-s3-uri-style=path`ではドットを許可するようになりました。

  プルリクエスト [#2713](https://github.com/pgbackrest/pgbackrest/pull/2713); コミット [`3fdb4a1`](https://github.com/pgbackrest/pgbackrest/commit/3fdb4a1ea00b442aca5fc714818d293d57490386)
- 検証が無効な場合を除き、TLS >= 1.2を必須にしました。 (*レビュー：Douglas J Hunley, Gunnar "Nick" Bluth。*)

  TLS 1.0と1.1は2021年から非推奨です。pgBackRestホスト間の接続では、検証を常に有効にします。たとえば自己署名証明書を使うため、オブジェクトストアで`repo-storage-verify-tls`による検証を無効にした場合は、すべてのプロトコルバージョンを許可します。

  プルリクエスト [#2720](https://github.com/pgbackrest/pgbackrest/pull/2720); コミット [`5b4b20a`](https://github.com/pgbackrest/pgbackrest/commit/5b4b20a8d7d17c2bffe106595310853e3f3a9604)
- 大容量のアップロードでは、S3/GCS/Azureのチャンクサイズを動的に設定するようにしました。 (*レビュー：Douglas J Hunley。提案：Timothée Peignier。*)

  アップロードのチャンク数には上限があるため、デフォルトの`repo-storage-upload-chunk-size`でアップロードできるファイルの最大サイズは、S3が50GiB、GCSが40GiB、Azureが200GiBでした。現在はアップロード中にチャンクサイズを拡大するため、S3とGCSでは最大5TiB、Azureでは最大45TiBのファイルをアップロードできます。

  課題 [#2679](https://github.com/pgbackrest/pgbackrest/issues/2679); プルリクエスト [#2701](https://github.com/pgbackrest/pgbackrest/pull/2701); コミット [`86554fa`](https://github.com/pgbackrest/pgbackrest/commit/86554faa707292855c2776a0c70b5e212b1e3945)
- 小さなファイルに対して、S3/GCS/Azureのチャンクサイズを最適化しました。 (*レビュー：Douglas J Hunley。*)

  多くのファイルは1チャンクより小さいにもかかわらず、ファイルを開いた時点でチャンクバッファー全体を確保していました。現在はデータが届くにつれてバッファーを拡大し、小さいファイルのアップロード時にメモリーを節約します。

  プルリクエスト [#2705](https://github.com/pgbackrest/pgbackrest/pull/2705); コミット [`28bfa20`](https://github.com/pgbackrest/pgbackrest/commit/28bfa20ba3b860f72ba7ab6c018e37ada99e2109)
- PostgreSQL `9.5`のサポートを削除しました。 (*レビュー：Douglas J Hunley。*)

  サポート終了したPostgreSQLを5バージョンまでサポートする方針に従い、PostgreSQL 9.5のサポートを終了しました。

  プルリクエスト [#2692](https://github.com/pgbackrest/pgbackrest/pull/2692); コミット [`5171e8b`](https://github.com/pgbackrest/pgbackrest/commit/5171e8bde31b9711c9c5b4ccc5170b61c5235548)
- 依存関係が未解決のオプションについて、デフォルト値のログ出力を改善しました。 (*レビュー：Stefan Fercot。*)

  設定ファイルに指定したオプションの依存条件が満たされない場合、デフォルト値を使っていてもコマンド開始時にそのオプションをログ出力していました。現在は、この場合にオプションをログ出力しません。

  課題 [#2707](https://github.com/pgbackrest/pgbackrest/issues/2707); プルリクエスト [#2708](https://github.com/pgbackrest/pgbackrest/pull/2708); コミット [`38ac638`](https://github.com/pgbackrest/pgbackrest/commit/38ac6387cbbfc6f78a686de657e5a4de4ed59295)

**ドキュメントの改善：**

- ユーザーガイドから`max_wal_senders`／`wal_level`の明示的な設定を削除しました。 (*提案：Jamie Nguyen。*)

  `max_wal_senders`と`wal_level`は、PostgreSQL 10以降、ユーザーガイドが要求する値がデフォルトになっています。

  課題 [#2699](https://github.com/pgbackrest/pgbackrest/issues/2699); コミット [`bce97d3`](https://github.com/pgbackrest/pgbackrest/commit/bce97d3ea80675b8eab3dbf692e8bc8f077f30c7)
- ブロックサイズの大きなファイルシステムではバンドルが有用であることを明確にしました。 (*提案：Ron Johnson。*)

  ブロックサイズの大きいファイルシステムでは、小さなファイルでも1ブロックを占有するため、バンドル化で容量を節約できます。

  課題 [#2706](https://github.com/pgbackrest/pgbackrest/issues/2706); コミット [`a7e5f28`](https://github.com/pgbackrest/pgbackrest/commit/a7e5f28511c27f2504a873db26803b26a84df8f1)

### v2.57.0リリースノート {#v2570-release-notes}

*リポジトリのシンボリックリンクを抑制*

*2025年10月18日リリース*

**バグ修正：**

- HTTP／TLS／ソケットのタイムアウトの入れ子を解消しました。 (*レビュー：David Christensen。*)

  ソケット接続の失敗をTLS層とHTTP層も再試行していたため、デフォルトの`io-timeout`が60秒でも接続のタイムアウトまで9分かかっていました。現在は各層が自身の失敗だけを再試行します。

  課題 [#2654](https://github.com/pgbackrest/pgbackrest/issues/2654); プルリクエスト [#2662](https://github.com/pgbackrest/pgbackrest/pull/2662); コミット [`9c7f064`](https://github.com/pgbackrest/pgbackrest/commit/9c7f0648648e651d82918e5dbfc3d511abee3298)
- ページチェックサムのエラーメッセージで、セグメンテーション違反が起こり得る問題を修正しました。 (*修正：Zsolt Parragi。レビュー：David Steele。*)

  無効なページチェックサムのエラーメッセージでスコープ外の文字列を使っていたため、ログに不正な内容が出たりクラッシュしたりする可能性がありました。暗号化されたすべてのファイルでページチェックサムが不一致になるpg_tdeでは、特に発生しやすい問題でした。

  プルリクエスト [#2675](https://github.com/pgbackrest/pgbackrest/pull/2675); コミット [`adc5e5b`](https://github.com/pgbackrest/pgbackrest/commit/adc5e5b23b9b544745724a7eaa0461b88b691e36)
- バックアップ再開のメッセージでセグメンテーションフォールトが起きる可能性を修正しました。

  バックアップを再開できない理由を報告するメッセージでスコープ外の文字列を使っていたため、ログに不正な内容が出たりクラッシュしたりする可能性がありました。

  コミット [`c1c40a4`](https://github.com/pgbackrest/pgbackrest/commit/c1c40a4a851efe98be83aca2044c02fd1c7fb2ae)

**新機能：**

- リポジトリのシンボリックリンクの作成を抑制する`repo-symlink`オプションを追加しました。 (*レビュー：Douglas J Hunley。提案：Ron Johnson。*)

  他の点ではPosix互換でも、シンボリックリンクをサポートしないファイルシステムがあります。リポジトリに`latest`やテーブルスペースのシンボリックリンクを作成しないようにするには、`repo-symlink=n`を設定します。

  課題 [#2673](https://github.com/pgbackrest/pgbackrest/issues/2673); プルリクエスト [#2674](https://github.com/pgbackrest/pgbackrest/pull/2674); コミット [`bfd9790`](https://github.com/pgbackrest/pgbackrest/commit/bfd97907311a25ed239798691cff52cf73acdb83)

**改善：**

- HTTPの408および429エラーに対する再試行を追加しました。 (*レビュー：David Christensen。*)

  HTTP 408（Request Timeout）と429（Too Many Requests）のエラーを再試行するようになりました。429エラーはCloudflare R2でよく発生します。

  プルリクエスト [#2661](https://github.com/pgbackrest/pgbackrest/pull/2661); コミット [`8733900`](https://github.com/pgbackrest/pgbackrest/commit/87339004e59c03d2a03a6ceb8426202346849c37)

### v2.56.0リリースノート {#v2560-release-notes}

*進捗情報の改善*

*2025年7月21日リリース*

**バグ修正：**

- リポジトリにバックアップがない場合の、個別の期限切れ処理の問題を修正しました。 (*レビュー：Stefan Fercot。報告：Anup Gupta。*)

  バックアップのないリポジトリで、個別指定の期限切れ処理が"cannot get index 0 from list with 0 value(s)"で失敗していました。

  課題 [#2645](https://github.com/pgbackrest/pgbackrest/issues/2645); プルリクエスト [#2646](https://github.com/pgbackrest/pgbackrest/pull/2646); コミット [`638815b`](https://github.com/pgbackrest/pgbackrest/commit/638815b4cde1ba1322516e256742c51676af66f0)

**新機能：**

- `info`コマンドの出力にリストアの進捗を追加しました。 (*貢献：Denis Garsh, Maxim Michkov。レビュー：David Steele。*)

  `restore`コマンドが進捗を記録するようになり、`info`コマンドでバックアップの進捗と並べて報告します。また、`stop`コマンドで復元を終了させなくなりました。

  課題 [#2546](https://github.com/pgbackrest/pgbackrest/issues/2546); プルリクエスト [#2652](https://github.com/pgbackrest/pgbackrest/pull/2652); コミット [`8cdd9ce`](https://github.com/pgbackrest/pgbackrest/commit/8cdd9ce1c4ab6cca508932a41a3013374d7547ef)
- `info`コマンドの出力に、進捗のみを表示する詳細レベルを追加しました。 (*貢献：Denis Garsh。レビュー：David Steele, Stefan Fercot。*)

  進捗だけを報告するには`--detail-level=progress`を指定します。リポジトリを読み取らないため高速です。デフォルトは`full`です。

  プルリクエスト [#2550](https://github.com/pgbackrest/pgbackrest/pull/2550); コミット [`2706168`](https://github.com/pgbackrest/pgbackrest/commit/2706168f609af544b0453d384c7fb620626fc205)

**改善：**

- オブジェクトストアで失敗した読み取りを再試行するようにしました。 (*レビュー：David Christensen。*)

  オブジェクトストアの読み取りが開始後に失敗すると致命的エラーになり、たとえば復元中に、コストの大きなジョブをやり直すことがありました。現在は、失敗した読み取りを中断位置から再試行します。

  プルリクエスト [#2642](https://github.com/pgbackrest/pgbackrest/pull/2642); コミット [`5e14692`](https://github.com/pgbackrest/pgbackrest/commit/5e14692588b9fd8a566c9a1795c866ba2e83eebd)
- コマンドラインヘルプのデフォルト値を修正しました。 (*レビュー：David Christensen, Chris Bandy。*)

  S3とAzureのリポジトリがある場合の`repo-storage-upload-chunk-size`のように、オプションに複数のデフォルト値がある場合、オプション一覧には`<multi>`を表示し、そのオプションのヘルプに各デフォルト値を列挙します。現在の設定では無効なオプションのデフォルト値は表示しません。

  プルリクエスト [#2625](https://github.com/pgbackrest/pgbackrest/pull/2625); コミット [`8737cad`](https://github.com/pgbackrest/pgbackrest/commit/8737cad566974c37529595715ecdc06571420752)

**ドキュメントの改善：**

- 適切な場合には、オプションの個々の値を一覧で説明するようにしました。 (*貢献：Anton Kurochkin。レビュー：David Steele。*)

  `verify`や`version`コマンドの`output`などのオプション値を、他のオプションと同様に一覧で説明するようにしました。

  プルリクエスト [#2638](https://github.com/pgbackrest/pgbackrest/pull/2638); コミット [`2e76e9f`](https://github.com/pgbackrest/pgbackrest/commit/2e76e9fc699d22286f6bf05fddc271d8fa22523e)
- `archive-mode`オプションのヘルプ出力にある"less than"の記述を修正しました。 (*貢献：Anton Kurochkin。レビュー：David Steele。*)

  プルリクエスト [#2633](https://github.com/pgbackrest/pgbackrest/pull/2633); コミット [`cb67322`](https://github.com/pgbackrest/pgbackrest/commit/cb673225e90604a8865ce30c188d15661f945e5e)

### v2.55.1リリースノート {#v2551-release-notes}

*不具合修正*

*2025年5月5日リリース*

**バグ修正：**

- 「必要な場合のみS3でcontent-md5を計算する」変更を元に戻しました。 (*レビュー：David Christensen。報告：Frank Brendel。*)

  オブジェクトロックが有効なS3へのアップロードには、`content-md5`または`x-amz-content-*`チェックサムが必要ですが、Scalityは代替のチェックサムを受け付けず、アップロードが失敗していました。再び、内容を伴うすべてのリクエストで`content-md5`を計算します。

  課題 [#2613](https://github.com/pgbackrest/pgbackrest/issues/2613); プルリクエスト [#2615](https://github.com/pgbackrest/pgbackrest/pull/2615); コミット [`8bbb982`](https://github.com/pgbackrest/pgbackrest/commit/8bbb98243566bfa052f6aacfd1bd3a6acd770e40)
- オプションキーの下限チェックを修正しました。 (*レビュー：David Christensen, Wolfgang Walther。報告：Wolfgang Walther。*)

  `pg0-path`のようにキーが0のインデックス付きオプションは、セグメンテーションフォールトを引き起こしていました。現在はエラーとして扱います。

  課題 [#2610](https://github.com/pgbackrest/pgbackrest/issues/2610); プルリクエスト [#2611](https://github.com/pgbackrest/pgbackrest/pull/2611); コミット [`5e01098`](https://github.com/pgbackrest/pgbackrest/commit/5e01098617a3803067b153be2d41e023cd4d95e4)

### v2.55.0リリースノート {#v2550-release-notes}

*検証の改善とPostgreSQL 18のサポート*

*2025年4月21日リリース*

**バグ修正：**

- デフォルト以外のリポジトリでのブロック増分リストアの問題を修正しました。 (*レビュー：David Christensen。テスト：Aleksander Łukasz。報告：Aleksander Łukasz。*)

  復元対象のバックアップがブロック増分を使い、最小番号のリポジトリにない場合、ブロック増分データの一部を最小番号のリポジトリから読み取っていました。`repo`を設定すれば回避できました。

  課題 [#2577](https://github.com/pgbackrest/pgbackrest/issues/2577); プルリクエスト [#2579](https://github.com/pgbackrest/pgbackrest/pull/2579); コミット [`5d2c67c`](https://github.com/pgbackrest/pgbackrest/commit/5d2c67c3c6975ea3ed08c7425f6e410ae378913f)
- PostgreSQL < 12では`recovery_target_timeline=current`を設定しないようにしました。 (*レビュー：Stefan Fercot。*)

  PostgreSQL 12より前では、`recovery_target_timeline`のデフォルトは`current`であるにもかかわらず、明示的に`current`を設定すると`latest`として動作します。これらのバージョンでは、値が`current`の場合に`recovery.conf`へ出力しないようにしました。

  プルリクエスト [#2533](https://github.com/pgbackrest/pgbackrest/pull/2533); コミット [`6fbb28f`](https://github.com/pgbackrest/pgbackrest/commit/6fbb28fa2d615576be78376c7f539921f6b8bc6a)
- アーカイブの期限切れ範囲のログ出力を修正しました。 (*レビュー：Stefan Fercot。報告：Aleš Zelený。*)

  削除した最後のアーカイブパスだけを範囲の先頭としてログ出力していたため、実際よりはるかに少ないファイルしか期限切れにしていないように見えていました。

  課題 [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); プルリクエスト [#2554](https://github.com/pgbackrest/pgbackrest/pull/2554); コミット [`47f050f`](https://github.com/pgbackrest/pgbackrest/commit/47f050f8fd816e57326d881f4253d8a13c0f8da6)
- 結果がないクエリーでのエラー報告を修正しました。 (*レビュー：Stefan Fercot。報告：Susantha Bathige。*)

  結果を返さないはずのクエリでエラーが発生すると、そのエラーではなく、予期しない結果として報告していました。

  プルリクエスト [#2539](https://github.com/pgbackrest/pgbackrest/pull/2539); コミット [`d5cefb7`](https://github.com/pgbackrest/pgbackrest/commit/d5cefb7290c34c64a2b9aa89ff04a718df4ec18b)

**新機能：**

- リカバリー対象のタイムラインを検証するようにしました。 (*レビュー：Stefan Fercot。*)

  たとえばスタンバイの昇格により新しいタイムラインが分岐した後に作成されたバックアップなど、対象タイムラインをたどれないバックアップでは、リカバリ開始後になって初めて、解釈しにくいPostgreSQLのエラーで失敗していました。現在は、復元開始前に履歴ファイルと照合してタイムラインを確認します。

  プルリクエスト [#2534](https://github.com/pgbackrest/pgbackrest/pull/2534); コミット [`922e9f0`](https://github.com/pgbackrest/pgbackrest/commit/922e9f0775c39b64e009251a6bec8ef9b83c190f)
- 指定したバックアップを検証できるようにしました。 (*貢献：Maxim Michkov。レビュー：David Steele。*)

  `verify`の`--set`オプションは、指定したバックアップと、その整合性を確保するのに必要なWALだけを検証します。

  課題 [#2419](https://github.com/pgbackrest/pgbackrest/issues/2419); プルリクエスト [#2544](https://github.com/pgbackrest/pgbackrest/pull/2544); コミット [`e4def88`](https://github.com/pgbackrest/pgbackrest/commit/e4def8845eb5c3fe9fb8cc44d9f64766cfb348c2)
- S3/GCSのリクエスター支払いをサポートしました。 (*貢献：Timothée Peignier。レビュー：David Steele。*)

  バケット所有者ではなくリクエスト元に課金するには、`repo-s3-requester-pays`または`repo-gcs-user-project`を設定します。たとえばホスティングサービスが顧客にバックアップへのアクセスを提供する場合に利用できます。

  [`4db0263`](https://github.com/pgbackrest/pgbackrest/commit/4db0263fd63274a8168eb4de17b320d2f86251a2) S3のリクエスト元負担をサポートしました。; プルリクエスト [#2560](https://github.com/pgbackrest/pgbackrest/pull/2560)

  [`814bf48`](https://github.com/pgbackrest/pgbackrest/commit/814bf487c3955e877d226faaa22324d3c79863b2) GCSのリクエスト元負担をサポートしました。; プルリクエスト [#2557](https://github.com/pgbackrest/pgbackrest/pull/2557)
- PostgreSQL 18をサポートしました。 (*レビュー：Stefan Fercot。*)

  このリリースはPostgreSQL 18のベータ版公開前だったため、当初のサポートは実験的なものでした。PostgreSQL 18.0までにpgBackRestへ影響する変更はありませんでした。

  プルリクエスト [#2603](https://github.com/pgbackrest/pgbackrest/pull/2603); コミット [`565d2e0`](https://github.com/pgbackrest/pgbackrest/commit/565d2e0c47cd21df890a40b3a94a8c865bed76d9)
- 抽象ドメインソケットでPostgreSQLに接続できるようにしました。 (*テスト：Chris Bandy。提案：Chris Bandy。*)

  `pg-socket-path`は絶対パスでなくてもよくなり、抽象ドメインソケットを指定できるようになりました。無効なパスはlibpqが報告します。

  課題 [#2529](https://github.com/pgbackrest/pgbackrest/issues/2529); プルリクエスト [#2535](https://github.com/pgbackrest/pgbackrest/pull/2535); コミット [`68f22ae`](https://github.com/pgbackrest/pgbackrest/commit/68f22aea6665b9dcbe76dbfaa731f37187e1ce20)
- `version`コマンドに数値形式の出力を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  `--output=num`を指定すると、バージョンを比較しやすい数値、たとえば2055000として出力します。

  課題 [#2410](https://github.com/pgbackrest/pgbackrest/issues/2410); プルリクエスト [#2526](https://github.com/pgbackrest/pgbackrest/pull/2526); コミット [`750a051`](https://github.com/pgbackrest/pgbackrest/commit/750a051b7aeccc3dd7ae9c07af2c73cb25057de9)

**改善：**

- backupコマンドをリモートリポジトリに対して実行できるようにしました。 (*レビュー：Stefan Fercot。*)

  リポジトリがリモートにあるホストでも`backup`コマンドを実行できるようになり、バックアップの実行場所を柔軟に選べます。

  [`4a94b6b`](https://github.com/pgbackrest/pgbackrest/commit/4a94b6bef9108ab775c0070571a1fb7dd8883eeb) プロトコルヘルパーをリファクタリングしました。

  [`931435c`](https://github.com/pgbackrest/pgbackrest/commit/931435c0177ded2189903385d520d5c8819c4f5e) backupコマンドをリモートリポジトリに対して実行できるようにしました。; プルリクエスト [#2512](https://github.com/pgbackrest/pgbackrest/pull/2512)
- プロトコルの圧縮にlz4を使用するようにしました。 (*レビュー：Stefan Fercot。*)

  lz4はgzよりはるかに速く圧縮でき、プロトコル圧縮で使う低い圧縮レベルでは圧縮率も同程度です。`compress-level-network=0`を設定しても、プロトコル圧縮を無効化しなくなりました。

  [`0577b03`](https://github.com/pgbackrest/pgbackrest/commit/0577b0301689bc19d49c4081cc652971de5da8cf) プロトコルの圧縮にlz4を使用するようにしました。; プルリクエスト [#2488](https://github.com/pgbackrest/pgbackrest/pull/2488)

  [`5c8296d`](https://github.com/pgbackrest/pgbackrest/commit/5c8296df066564be35d3936610ebff1c332f38da) ネットワーク圧縮の無効化に関する記述をドキュメントから削除しました。
- 必要な場合のみS3で`content-md5`を計算するようにしました。 (*レビュー：David Christensen。*)

  ファイルアップロード時のCPU負荷を減らすため、`content-md5`ヘッダーは、それを必要とするバッチ削除リクエストでのみ計算するようにしました。この変更はv2.55.1で取り消されました。

  プルリクエスト [#2592](https://github.com/pgbackrest/pgbackrest/pull/2592); コミット [`20bfd14`](https://github.com/pgbackrest/pgbackrest/commit/20bfd14b73ad6d75b6fb1169565b18dcfa183c9b)
- 複数キーを持つオプションの値が上書きされた場合、警告するようにしました。 (*レビュー：David Christensen, Stefan Fercot。*)

  `recovery-option`などキーと値の組を持つオプションでは、同じキーを再指定すると通知せずに値を上書きしていました。現在は警告をログ出力します。

  課題 [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); プルリクエスト [#2594](https://github.com/pgbackrest/pgbackrest/pull/2594); コミット [`cab4d6f`](https://github.com/pgbackrest/pgbackrest/commit/cab4d6fd5c775d6e1a9cd9889d825eee667b5322)
- 期限切れにしたアーカイブパスをdetailログに出力するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  大量のアーカイブファイルの削除が、停止したように見えることがありました。現在はdetailレベルのメッセージで進捗を表示します。

  [`4dcfa9e`](https://github.com/pgbackrest/pgbackrest/commit/4dcfa9ef59c5e75c6c0ee83390c64b9a3d4af1fc) 期限切れ処理のテストにdetailレベルのログ出力を追加しました。

  [`2155a12`](https://github.com/pgbackrest/pgbackrest/commit/2155a12a3d861645de5618518350f90962fbc26d) 期限切れにしたアーカイブパスをdetailログに出力するようにしました。; 課題 [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); プルリクエスト [#2559](https://github.com/pgbackrest/pgbackrest/pull/2559)
- PostgreSQL `9.4`のサポートを削除しました。 (*レビュー：Stefan Fercot。*)

  サポート終了したPostgreSQLを5バージョンまでサポートする方針に従い、PostgreSQL 9.4のサポートを終了しました。9.4クラスターのバックアップは引き続き期限切れ処理できます。

  プルリクエスト [#2472](https://github.com/pgbackrest/pgbackrest/pull/2472); コミット [`48f511d`](https://github.com/pgbackrest/pgbackrest/commit/48f511dad339ef9357e00f7bd8e2bf4b7c800dd4)
- autoconf/makeによるビルドを削除しました。 (*レビュー：David Christensen。*)

  autoconf/makeによるビルドをサポートする最後のリリースはv2.54.0でした。ビルドにはmesonを使用してください。

  プルリクエスト [#2470](https://github.com/pgbackrest/pgbackrest/pull/2470); コミット [`89c9bab`](https://github.com/pgbackrest/pgbackrest/commit/89c9baba72fc99616083a7adc4be2c3e2bf9e4dd)

**ドキュメントの改善：**

- `tls-server-auth`で複数のstanzaを指定するための説明を修正しました。 (*レビュー：David Christensen, Stefan Fercot。提案：Terry MacAndrew。*)

  `tls-server-auth`で複数のスタンザを指定するには、カンマ区切りの一覧を使います。以前のドキュメントでは、オプションを繰り返すよう説明していました。

  課題 [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); プルリクエスト [#2595](https://github.com/pgbackrest/pgbackrest/pull/2595); コミット [`53a45d2`](https://github.com/pgbackrest/pgbackrest/commit/53a45d25c3e60e5067010b2676f5d6216638fbe3)
- 増分バックアップの期限切れ処理を明確にしました。 (*レビュー：Stefan Fercot。*)

  以前のドキュメントは、増分バックアップが個数に基づいて期限切れになるかのような説明でした。現在は、増分バックアップの期限切れ処理方法と、差分バックアップの保持ではフルバックアップも差分バックアップとして数えることを説明しています。

  プルリクエスト [#2601](https://github.com/pgbackrest/pgbackrest/pull/2601); コミット [`8bdba74`](https://github.com/pgbackrest/pgbackrest/commit/8bdba747981e8805a9bf355050f70cdf19e9babc)
- ローカルとリモートのpgBackRestのバージョンが一致する必要があることを明確にしました。 (*貢献：Greg Clough。レビュー：David Steele。*)

  課題 [#2540](https://github.com/pgbackrest/pgbackrest/issues/2540); プルリクエスト [#2541](https://github.com/pgbackrest/pgbackrest/pull/2541); コミット [`82299eb`](https://github.com/pgbackrest/pgbackrest/commit/82299eb4cd997524eeddef170ad99669ed6651cf)
- 単独で動作するクラスターのエクスポートに関するFAQを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  FAQで、`--archive-copy`を指定して作成したバックアップを`--type=none`で復元し、クラスターの自己完結したエクスポートを作る方法を説明しています。

  プルリクエスト [#2605](https://github.com/pgbackrest/pgbackrest/pull/2605); コミット [`9386920`](https://github.com/pgbackrest/pgbackrest/commit/9386920b79971347c6c57589190bf09b591d8b4d)
- テーブルスペース作成に関する`--tablespace-map-all`の注意事項を追加しました。 (*レビュー：Stefan Fercot, Christophe Courtois。提案：Christophe Courtois。*)

  バックアップ開始後に作成されたテーブルスペースはマニフェストに含まれないため、`tablespace-map-all`でマッピングできません。

  プルリクエスト [#2538](https://github.com/pgbackrest/pgbackrest/pull/2538); コミット [`e625ed8`](https://github.com/pgbackrest/pgbackrest/commit/e625ed8be2228cb99c3801f9d1776909a2201c5a)
- `--repo-retention-full-type`の動作を明確にしました。 (*レビュー：Antoine Beaupré。提案：Antoine Beaupré。*)

  課題 [#2562](https://github.com/pgbackrest/pgbackrest/issues/2562); プルリクエスト [#2583](https://github.com/pgbackrest/pgbackrest/pull/2583); コミット [`84eb9a7`](https://github.com/pgbackrest/pgbackrest/commit/84eb9a742dcf75f071e011946263dedaa985099e)
- オブジェクトストアに対する推奨設定を、`--process-max`から`--repo-bundle`に変更しました。 (*レビュー：Stefan Fercot。*)

  オブジェクトストアでは、`repo-bundle`によって作成するファイル数が減るため、`process-max`よりもファイル作成時間を大幅に削減できます。

  プルリクエスト [#2542](https://github.com/pgbackrest/pgbackrest/pull/2542); コミット [`aa7210a`](https://github.com/pgbackrest/pgbackrest/commit/aa7210a1830825e0a3e6b6740937357341127a6f)
- `unix_socket_directory`を`unix_socket_directories`に更新しました。 (*貢献：hyunkyu han。レビュー：David Steele。*)

  `unix_socket_directory`はPostgreSQL 9.2以降無効なため、`unix_socket_directories`だけを文書化しています。

  課題 [#2589](https://github.com/pgbackrest/pgbackrest/issues/2589); コミット [`b28ae98`](https://github.com/pgbackrest/pgbackrest/commit/b28ae98cec7ae7e881e6476c1cba1ba7e1abc358)
- `spool-path`を`pg_xlog`／`pg_wal`の中に置かないことを推奨する記述を追加しました。 (*レビュー：Martín Marqués, Don Seiler。提案：Martín Marqués。*)

  `pg_xlog`や`pg_wal`の中にスプールパスを置くと、`pg_rewind`などのPostgreSQLツールで問題が起こる可能性があります。

  プルリクエスト [#2600](https://github.com/pgbackrest/pgbackrest/pull/2600); コミット [`dd3a7d9`](https://github.com/pgbackrest/pgbackrest/commit/dd3a7d99a78d0d604967d90e8a8dbf8915432896)

### v2.54.2リリースノート {#v2542-release-notes}

*不具合修正*

*2025年1月20日リリース*

**バグ修正：**

- ブロック増分が有効な状態でバンドルを無効にした後の問題を修正しました。 (*レビュー：David Christensen。*)

  バンドル化とブロック増分を有効にしてバックアップした後でバンドル化を無効にすると、以前のバックアップを読み取れませんでした。現在は、それらの読み取りに必要な設定を保持します。

  プルリクエスト [#2511](https://github.com/pgbackrest/pgbackrest/pull/2511); コミット [`dbc6f28`](https://github.com/pgbackrest/pgbackrest/commit/dbc6f2875356ec16cf4883830a0d7b00204752ee)

**ドキュメントの改善：**

- 複数の設定ファイルを使う場合の動作を明確にしました。 (*レビュー：Paul Bierly。提案：Paul Bierly。*)

  各設定ファイルは単独で有効でなければならないため、あるセクションのオプションを設定するファイルでは、その都度セクションを指定する必要があります。引用符はサポートしないこと、キーと値の前後の空白を除くこと、同じセクションを繰り返した場合は結合することもドキュメントに記載しました。

  コミット [`5da2df4`](https://github.com/pgbackrest/pgbackrest/commit/5da2df4a933f04d5fb9a3b6c7c59529f3afa805b)

### v2.54.1リリースノート {#v2541-release-notes}

*不具合修正*

*2024年12月16日リリース*

**バグ修正：**

- `version`／`help`コマンドが`pgbackrest.conf`を読み込もうとする問題を修正しました。 (*レビュー：Stefan Fercot。報告：Bradford Boyle, Julian。*)

  v2.54.0では、`version`と`help`コマンドが`pgbackrest.conf`を読み込み、読み取りや解析ができないと失敗していました。

  課題 [#2476](https://github.com/pgbackrest/pgbackrest/issues/2476); プルリクエスト [#2477](https://github.com/pgbackrest/pgbackrest/pull/2477); コミット [`8d69118`](https://github.com/pgbackrest/pgbackrest/commit/8d6911898afd75c586ef70c6d8559b1e5959a155)

**テストスイートの改善：**

- 統合テストでの非同期アーカイブを安定化しました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)

  ある結合テストで実行した非同期`archive-get`が残ると、次のテストのキューにエラーを書き込み、リカバリを失敗させることがありました。

  課題 [#2463](https://github.com/pgbackrest/pgbackrest/issues/2463); プルリクエスト [#2481](https://github.com/pgbackrest/pgbackrest/pull/2481); コミット [`b90ce9e`](https://github.com/pgbackrest/pgbackrest/commit/b90ce9eb8c7cd9e9b131477a377249a3d3fda181)

### v2.54.0リリースノート {#v2540-release-notes}

*バージョン管理されたストレージの対象時刻*

*2024年10月21日リリース*

**パッケージ作成者への注意事項**：autoconf/makeによるビルドをサポートする機能リリースは、これが最後です。まだ移行していない場合はmesonへ移行してください。2.54.Xのパッチリリースがある場合、そちらでは引き続きautoconf/makeをサポートします。

**バグ修正：**

- 大規模なデータセットでのPostgreSQLクエリーの性能を修正しました。 (*修正：Thibault Vincent, David Steele。レビュー：David Christensen。テスト：Antoine Millet。報告：Antoine Millet。*)

  クエリのタイムアウト処理が結果の読み取りを遅らせていたため、大きい結果を返すクエリに`db-timeout`までの時間がかかる可能性がありました。現在は、結果が利用可能になり次第読み取ります。

  [`6ac4e8d`](https://github.com/pgbackrest/pgbackrest/commit/6ac4e8dd78f16e93300f7747c4bc8fa8e1a0558b) fdモジュールのshimをioモジュールのテストへ移しました。

  [`77ae753`](https://github.com/pgbackrest/pgbackrest/commit/77ae753ef59bd40b9867be21e8519093786c3b85) fdReady()のshimを、指定した戻り値で1回だけ実行できるようにしました。

  [`33fa396`](https://github.com/pgbackrest/pgbackrest/commit/33fa3965616b1432e5d1d59c489302fa4891a39e) Waitオブジェクトをリファクタリングし、残りの待ち時間をwaitRemains()で取得できるようにしました。

  [`c8ccaaa`](https://github.com/pgbackrest/pgbackrest/commit/c8ccaaa755993e3fd5e87148bd0a991acb3050c3) 大規模なデータセットでのPostgreSQLクエリーの性能を修正しました。; 課題 [#2458](https://github.com/pgbackrest/pgbackrest/issues/2458); プルリクエスト [#2459](https://github.com/pgbackrest/pgbackrest/pull/2459)

**新機能：**

- バージョン管理されたストレージ上のリポジトリを、指定時刻の状態で読み取れるようにしました。 (*レビュー：Stefan Fercot, David Christensen。*)

  `archive-get`、`info`、`repo-get`、`repo-ls`、`restore`、`verify`コマンドは、バージョニングされたAzure、GCS、S3ストレージ上のリポジトリを、`repo-target-time`時点の状態で読み取れます。これにより、誤操作や悪意によってリポジトリが削除・破損された場合でも復旧できます。

  プルリクエスト [#2404](https://github.com/pgbackrest/pgbackrest/pull/2404); コミット [`b19134d`](https://github.com/pgbackrest/pgbackrest/commit/b19134dccd5d0dab87b5d45b443f481df00370b1)
- スタンバイからのバックアップが要求された場合、スタンバイがなくても続行できるようにしました。 (*レビュー：Stefan Fercot。*)

  利用可能なスタンバイからバックアップし、なければプライマリーからバックアップするには、`backup-standby=prefer`を設定します。スタンバイが応答しても、バックアップ開始後にプライマリーとの同期に失敗する場合には役立ちません。

  プルリクエスト [#2378](https://github.com/pgbackrest/pgbackrest/pull/2378); コミット [`a42629f`](https://github.com/pgbackrest/pgbackrest/commit/a42629f87ab70ffaee8d1241eb50c5ea7154a87d)

**改善：**

- `info`コマンドのテキスト出力で、バックアップの参照一覧を要約するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  バックアップの参照一覧は非常に長くなることがあるため、`info`コマンドのテキスト出力では要約するようになりました。`--set`を指定すると一覧全体を表示します。

  プルリクエスト [#2399](https://github.com/pgbackrest/pgbackrest/pull/2399); コミット [`b306f83`](https://github.com/pgbackrest/pgbackrest/commit/b306f83493cc859ad15c8f175fc6db2321b79340)
- S3認証のたびにweb-idトークンを更新するようにしました。 (*貢献：Brent Graveland。レビュー：David Steele。*)

  `AWS_WEB_IDENTITY_TOKEN_FILE`で指定するトークンファイルを起動時に1回だけ読んでいたため、長時間の操作中にトークンが期限切れになる可能性がありました。現在は、認証のたびにトークンを読み取ります。

  課題 [#2428](https://github.com/pgbackrest/pgbackrest/issues/2428); プルリクエスト [#2429](https://github.com/pgbackrest/pgbackrest/pull/2429); コミット [`95a4b9e`](https://github.com/pgbackrest/pgbackrest/commit/95a4b9e10a3f7a26ebaae22fc6abd79cee14189a)
- ヘルプでインデックス付きオプションの現在値を正しく表示するようにしました。 (*レビュー：David Christensen。*)

  インデックス付きオプションの現在値には、常に`pg1-path`など最初のインデックスの値を表示していました。現在はオプションのヘルプで各インデックスの値を列挙し、複数ある場合はオプション一覧に`<multi>`を表示します。

  プルリクエスト [#2453](https://github.com/pgbackrest/pgbackrest/pull/2453); コミット [`b3ca2e3`](https://github.com/pgbackrest/pgbackrest/commit/b3ca2e34823b28862d999f87c4d7346707952a5b)
- 内容が変更された場合のみ`backup.info`を保存するようにしました。 (*レビュー：Stefan Fercot。*)

  `expire`は、変更がなくても`backup.info`を保存していました。保存回数が減ることで、バージョニングされたストレージの対象時刻も選びやすくなります。

  プルリクエスト [#2403](https://github.com/pgbackrest/pgbackrest/pull/2403); コミット [`b454b9e`](https://github.com/pgbackrest/pgbackrest/commit/b454b9e403526b1f352df964d9206c27d2397df3)
- リストア時にファイルを並列で読み取る際の制限を削除しました。 (*レビュー：David Christensen。*)

  プロトコルはリモートで1度に1ファイルしか読み書きできなかったため、復元時もリポジトリから1ファイルずつ読み取っていました。現在はプロトコルのコマンドを多重化できるため、たとえばバンドルと、その中のファイルのブロック増分データなど、複数のファイルを同時に読み取れます。

  [`df8cbc9`](https://github.com/pgbackrest/pgbackrest/commit/df8cbc91c348bc2f746767c87ac5626460fb6f39) プロトコルのコマンドを多重化しました。; プルリクエスト [#2108](https://github.com/pgbackrest/pgbackrest/pull/2108)

  [`46c1297`](https://github.com/pgbackrest/pgbackrest/commit/46c1297be344909e900be596a865064233da9f87) リストア時にファイルを並列で読み取る際の制限を削除しました。; プルリクエスト [#2436](https://github.com/pgbackrest/pgbackrest/pull/2436)
- SFTPのエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  SFTPのエラーは数値だけで報告していました。現在はエラーの説明も含みます。

  プルリクエスト [#2439](https://github.com/pgbackrest/pgbackrest/pull/2439); コミット [`70bda2c`](https://github.com/pgbackrest/pgbackrest/commit/70bda2cfb21130eb589a87cb419fb5f22a71c78a)

**ドキュメントの機能：**

- ユーザーガイドに性能調整のセクションを追加しました。 (*レビュー：Stefan Fercot。*)

  一般的に性能向上に役立つオプションの説明が、ドキュメント内に分散していました。クイックスタートに、それらを一覧にしたセクションを追加しました。

  プルリクエスト [#2446](https://github.com/pgbackrest/pgbackrest/pull/2446); コミット [`278319e`](https://github.com/pgbackrest/pgbackrest/commit/278319eba3444070123d3f0f277be9234604d937)

**ドキュメントの改善：**

- `data_directory`の取得元を明確にしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Matthias。*)

  `pg-path`は、PostgreSQLが報告する`data_directory`と一致させる必要があります。この値は`postgresql.conf`の値と異なる場合があります。

  課題 [#2464](https://github.com/pgbackrest/pgbackrest/issues/2464); プルリクエスト [#2467](https://github.com/pgbackrest/pgbackrest/pull/2467); コミット [`9ba2db0`](https://github.com/pgbackrest/pgbackrest/commit/9ba2db017348d304f96ce89592fc01f29197e136)
- 概要を小文字にするかどうかの判定ロジックを改善しました。 (*提案：Daniel Westermann。*)

  PostgreSQLなどの固有名詞や頭字語で始まる要約を、ドキュメント内で小文字化しなくなりました。

  課題 [#2462](https://github.com/pgbackrest/pgbackrest/issues/2462); コミット [`eb2f279`](https://github.com/pgbackrest/pgbackrest/commit/eb2f279a2998d1ed893c5d8984590ab4997a5f32)

### v2.53.1リリースノート {#v2531-release-notes}

*PostgreSQL 17のサポート*

*2024年8月19日リリース*

**バグ修正：**

- rootユーザーで`restore`を実行した場合のアクセス権限を修正しました。 (*レビュー：Stefan Fercot。報告：Will M。*)

  rootで`restore`を実行すると、`pg_control`の所有者がrootになっていました。また、ベースパスが存在しない場合にも、rootでの復元が失敗していました。

  課題 [#2407](https://github.com/pgbackrest/pgbackrest/issues/2407); プルリクエスト [#2416](https://github.com/pgbackrest/pgbackrest/pull/2416); コミット [`7bd8da4`](https://github.com/pgbackrest/pgbackrest/commit/7bd8da4eecb0ce1461854414b727606a5e884edf)
- 接続エラーが遅れて発生した場合のセグメンテーション違反を修正しました。 (*レビュー：David Christensen。報告：Anton Glushakov。*)

  接続エラーの通知が遅れて後続の待機時に報告されると、セグメンテーションフォールトを起こす可能性がありました。

  課題 [#2420](https://github.com/pgbackrest/pgbackrest/issues/2420); プルリクエスト [#2422](https://github.com/pgbackrest/pgbackrest/pull/2422); コミット [`377ba06`](https://github.com/pgbackrest/pgbackrest/commit/377ba062ac81867dca6197265688deb0111ae81a)
- SFTPではローカルリポジトリの重複チェックを省略するようにしました。 (*修正：Reid Thompson。レビュー：David Steele。報告：Anton Kurochkin。*)

  同じローカルリポジトリを複数回設定していないかの確認を、ローカルではないSFTPリポジトリにも適用していました。

  課題 [#2418](https://github.com/pgbackrest/pgbackrest/issues/2418); プルリクエスト [#2421](https://github.com/pgbackrest/pgbackrest/pull/2421); コミット [`9840304`](https://github.com/pgbackrest/pgbackrest/commit/98403046ed6af4c54fa2f572ecf9c211f94b67db)

**改善：**

- PostgreSQL 17をサポートしました。

  PostgreSQL 17beta3では、ベータ版としては異例ですが、制御ファイルとWALの形式が変更されました。

  コミット [`189d15d`](https://github.com/pgbackrest/pgbackrest/commit/189d15d1a640e31aac5ffbbd0fb06eb9eed8b576)

### v2.53リリースノート {#v253-release-notes}

*バックアップの同時実行*

*2024年7月22日リリース*

**重要な注意事項**：`log-level-stderr`オプションのデフォルトを`warn`から`off`に変更しました。これにより、`stdout`だけをリダイレクトする場合にエラーを取得しやすくなります。以前の動作を維持するには`log-level-stderr=warn`を設定してください。<br/> <br/> **パッケージ作成者への注意**：mesonによるビルドでlz4ライブラリーが必須になりました。<br/> <br/> **パッケージ作成者への注意**：mesonによるビルドで、コンパイラーによる`__builtin_clzl()`と`__builtin_bswap64()`のサポートが必須になりました。

**バグ修正：**

- ファイルがすでに存在する場合、SFTPで名前の変更に失敗する問題を修正しました。 (*修正：Reid Thompson。レビュー：David Steele。報告：ahmed112212。*)

  一部のSFTPサーバーはファイルがすでに存在することを未対応のエラーで報告するため、既存ファイルを上書きする名前変更に失敗していました。

  課題 [#2376](https://github.com/pgbackrest/pgbackrest/issues/2376); プルリクエスト [#2377](https://github.com/pgbackrest/pgbackrest/pull/2377); コミット [`d6f0bf8`](https://github.com/pgbackrest/pgbackrest/commit/d6f0bf88af8b39492aa8e20c09bdf30260e2eb2f)

**新機能：**

- 異なるリポジトリに対してバックアップを同時に実行できるようにしました。 (*レビュー：Reid Thompson, Stefan Fercot。*)

  ロックをスタンザ単位からスタンザとリポジトリの組み合わせ単位に変更したため、同じスタンザを異なるリポジトリへ同時にバックアップできるようになりました。PostgreSQL <= 9.5では利用できません。

  [`270dce4`](https://github.com/pgbackrest/pgbackrest/commit/270dce41b6fff0d0ad0769b0ea5df0011140f0b9) ロックモジュールをリファクタリングしました。; プルリクエスト [#2371](https://github.com/pgbackrest/pgbackrest/pull/2371)

  [`cfb8aa2`](https://github.com/pgbackrest/pgbackrest/commit/cfb8aa202ee972579697db2cc8d5d8ef111f0022) 31c7824aで漏れていたスタンザコマンドにリモートロックを追加しました。

  [`edd6163`](https://github.com/pgbackrest/pgbackrest/commit/edd61636a98d193b7c0634b5a4444527132959e0) 異なるリポジトリに対してバックアップを同時に実行できるようにしました。; プルリクエスト [#2389](https://github.com/pgbackrest/pgbackrest/pull/2389)
- TLS証明書の検証で、IPアドレスを使うSANをサポートしました。 (*貢献：David Christensen。レビュー：David Steele。*)

  サブジェクト代替名に`IP:1.2.3.4`などのIPアドレスを持つ証明書を検証するようになりました。IPv4、IPv6ともにアドレスが完全に一致する必要があります。

  課題 [#1977](https://github.com/pgbackrest/pgbackrest/issues/1977); プルリクエスト [#2047](https://github.com/pgbackrest/pgbackrest/pull/2047); コミット [`dfb620b`](https://github.com/pgbackrest/pgbackrest/commit/dfb620b0b8cf884ca486b413f4cd162e258b2fc5)

**改善：**

- `log-level-stderr`オプションのデフォルトを`off`にしました。 (*レビュー：Greg Sabino Mullane, Stefan Fercot。*)

  ログを収集する際にstdoutだけをリダイレクトすると、stderrに出力した警告とエラーを取りこぼすことがよくありました。明示的に設定した`log-level-stderr`には影響しません。

  プルリクエスト [#2379](https://github.com/pgbackrest/pgbackrest/pull/2379); コミット [`7d54073`](https://github.com/pgbackrest/pgbackrest/commit/7d540730941994d3cb630c695e9f672e047d8e7f)
- PostgreSQL ≤ 10で、標準以外のWALセグメントサイズを使用できるようにしました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)

  PostgreSQL <= 10は、異なるWALセグメントサイズでビルドできます。また、Greenplumなどの派生版は`initdb`でサイズを設定します。

  プルリクエスト [#2303](https://github.com/pgbackrest/pgbackrest/pull/2303); コミット [`4ac3b82`](https://github.com/pgbackrest/pgbackrest/commit/4ac3b82c99ff3bd48d2cc74651a47ce072ac0022)
- SFTP認証ログの確認を促すヒントを追加しました。 (*貢献：Vitalii Zurian。レビュー：Reid Thompson, David Steele。*)

  SFTP認証に失敗した際、サーバーの認証ログに詳しい情報がある可能性をエラーメッセージで案内するようにしました。

  課題 [#2381](https://github.com/pgbackrest/pgbackrest/issues/2381); プルリクエスト [#2385](https://github.com/pgbackrest/pgbackrest/pull/2385); コミット [`ccae609`](https://github.com/pgbackrest/pgbackrest/commit/ccae60940241b30e8bc3e405936b6ba68857930c)
- 時間オプションのデフォルト値と許容値を適切な単位で表示するようにしました。

  時間オプションのデフォルト値と許容値は秒単位で表示しており、大きい値を読み取りにくくしていました。秒数の小数指定は許可しなくなったため、`archive-timeout=0.5`のような値は`archive-timeout=500ms`と記述する必要があります。

  コミット [`3a2266f`](https://github.com/pgbackrest/pgbackrest/commit/3a2266f327c340ff1133a6a2398429c844b5755d)
- OpenSSL >= 1.1.1を必須にしました。

  コミット [`cf8625d`](https://github.com/pgbackrest/pgbackrest/commit/cf8625d24bd953ad1ed448c32b937584009e5b6b)

**ドキュメントの改善：**

- 複数リポジトリでの`archive-push`の動作を明確にしました。 (*レビュー：Stefan Fercot。*)

  あるリポジトリで障害が起きている場合、`archive-async`が有効でなければ、`archive-push`は他のリポジトリへの転送を先に進められません。

  プルリクエスト [#2398](https://github.com/pgbackrest/pgbackrest/pull/2398); コミット [`ec3e387`](https://github.com/pgbackrest/pgbackrest/commit/ec3e387bb73826c30b32bf0221acb2d56f23f1c5)

### v2.52.1リリースノート {#v2521-release-notes}

*不具合修正*

*2024年6月25日リリース*

**バグ修正：**

- レプリカ上のファイルがプライマリー上より大きい場合の問題を修正しました。 (*レビュー：Stefan Fercot。報告：Nicolas Lassimonne。*)

  ブロック増分を使ったスタンバイからのバックアップ中に、プライマリーとスタンバイでファイルサイズが異なると、次の差分・増分バックアップはプライマリーのサイズを保存していました。その次のバックアップは"repo size must be > 0"で失敗していました。

  [`83aaa86`](https://github.com/pgbackrest/pgbackrest/commit/83aaa868ef396348bf96589457f13c1805b25cb6) ブロック増分を使ったスタンバイからのバックアップのユニットテストを追加しました。

  [`aabc122`](https://github.com/pgbackrest/pgbackrest/commit/aabc122021a582e9d0193f978cf710cff95c2bee) レプリカ上のファイルがプライマリー上より大きい場合の問題を修正しました。; 課題 [#2358](https://github.com/pgbackrest/pgbackrest/issues/2358); プルリクエスト [#2367](https://github.com/pgbackrest/pgbackrest/pull/2367)

### v2.52リリースノート {#v252-release-notes}

*PostgreSQL 17beta1のサポート*

*2024年5月27日リリース*

**パッケージ作成者への注意事項**：pgBackRestのビルドシステムをmesonに変更しました。autoconf/makeによるビルドには今後新機能を追加せず、数回のリリース後に削除します。

**新機能：**

- GCSの一括削除をサポートしました。 (*レビュー：Reid Thompson。*)

  ファイルごとのリクエストの代わりにバッチリクエストで削除し、`expire`などリポジトリからファイルを削除するコマンドを高速化します。

  プルリクエスト [#2326](https://github.com/pgbackrest/pgbackrest/pull/2326); コミット [`76bcb74`](https://github.com/pgbackrest/pgbackrest/commit/76bcb740b66f64804dbbf5a2a6be6407f9cec376)
- S3の`SSE-C`暗号化をサポートしました。 (*レビュー：Tim Jones。提案：Tim Jones。*)

  転送後のデータを指定したキーでS3に暗号化させるには、`repo-s3-sse-customer-key`を設定します。`repo-cipher-type`で転送前に暗号化する方法ほど安全ではありません。

  課題 [#2279](https://github.com/pgbackrest/pgbackrest/issues/2279); プルリクエスト [#2282](https://github.com/pgbackrest/pgbackrest/pull/2282); コミット [`57731b6`](https://github.com/pgbackrest/pgbackrest/commit/57731b6cd261c732041aacc094429ab02ca13418)
- PostgreSQL 17beta1をサポートしました。 (*レビュー：Stefan Fercot。*)

  PostgreSQL 17のカタログバージョンとWALマジックナンバーを追加しました。

  プルリクエスト [#2328](https://github.com/pgbackrest/pgbackrest/pull/2328); コミット [`fb22f04`](https://github.com/pgbackrest/pgbackrest/commit/fb22f04555fecfa143354372ec3543ab186c131d)

**改善：**

- mesonでのビルドで、任意の依存関係を明示的に無効にできるようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)

  FreeBSDなど一部の環境で必要とされるように、mesonビルドではライブラリーがインストール済みでも任意機能を無効にできます。デフォルトでは、ライブラリーが見つかると機能を有効にします。

  プルリクエスト [#2321](https://github.com/pgbackrest/pgbackrest/pull/2321); コミット [`7b95fd3`](https://github.com/pgbackrest/pgbackrest/commit/7b95fd3bd29346e7325aa161bfee45efd71e22eb)
- mesonでのビルドでpythonを動的に検索するようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)

  mesonビルドは、PATH上の`python3`実行ファイルを必須とせず、たとえば`python3.9`だけがある場合でもPythonを検出するようになりました。mesonの最低バージョンは0.47になりました。

  [`55e9969`](https://github.com/pgbackrest/pgbackrest/commit/55e996912aa57d39ea21f5dc905b7acabe93b0f8) mesonの最低バージョンを0.47に更新しました。

  [`e00e33b`](https://github.com/pgbackrest/pgbackrest/commit/e00e33b52856a63e82552ccc12df235d1a7f6f17) mesonでのビルドでpythonを動的に検索するようにしました。; プルリクエスト [#2338](https://github.com/pgbackrest/pgbackrest/pull/2338)
- mesonで`pgbackrest`ビルドターゲットをインストール可能として指定しました。 (*貢献：Bradford Boyle。レビュー：David Steele。*)

  プルリクエスト [#2312](https://github.com/pgbackrest/pgbackrest/pull/2312); コミット [`7877983`](https://github.com/pgbackrest/pgbackrest/commit/7877983acb3b1a27e900f7e7aea89cb7b29a817d)

**ドキュメントの改善：**

- 実際の機能に合わせて`start`／`stop`の説明を更新しました。 (*レビュー：Stefan Fercot。*)

  課題 [#2325](https://github.com/pgbackrest/pgbackrest/issues/2325); 課題 [#2334](https://github.com/pgbackrest/pgbackrest/issues/2334); プルリクエスト [#2352](https://github.com/pgbackrest/pgbackrest/pull/2352); コミット [`b6ac11b`](https://github.com/pgbackrest/pgbackrest/commit/b6ac11beec920fe978994c0d018c380477199ca8)

### v2.51リリースノート {#v251-release-notes}

*Mesonビルドシステム*

*2024年3月25日リリース*

**バグ修正：**

- ブロック増分バックアップの差分リストアで、長さゼロのファイルをスキップするようにしました。 (*レビュー：Sebastian Krause, René Højbjerg Larsen。報告：Sebastian Krause。*)

  既存のサイズゼロのファイルがあると、ブロック増分の差分復元がブロックチェックサムフィルターで失敗していました。再利用できる内容がないため、これらのファイルはスキップするようにしました。

  課題 [#2271](https://github.com/pgbackrest/pgbackrest/issues/2271); プルリクエスト [#2272](https://github.com/pgbackrest/pgbackrest/pull/2272); コミット [`f7a7ab1`](https://github.com/pgbackrest/pgbackrest/commit/f7a7ab16c9652179945717ebf9b68af3aa8a0b0e)
- ストレージの一覧取得での性能リグレッションを修正しました。 (*レビュー：Stephen Frost。報告：Maksym Boguk。*)

  パスの一覧取得で各ファイルの詳細情報を要求していたため、オブジェクトストアなどでは遅くなることがありました。現在は、一覧に必要な情報だけを要求します。

  課題 [#2275](https://github.com/pgbackrest/pgbackrest/issues/2275); プルリクエスト [#2276](https://github.com/pgbackrest/pgbackrest/pull/2276); コミット [`e00bfe2`](https://github.com/pgbackrest/pgbackrest/commit/e00bfe2d2c3f124b2883e3c2d169a2ce506a1e98)
- バックアップ中にファイルサイズが変わった場合の進捗ログを修正しました。 (*レビュー：Stephen Frost。報告：samkingno。*)

  課題 [#2298](https://github.com/pgbackrest/pgbackrest/issues/2298); プルリクエスト [#2304](https://github.com/pgbackrest/pgbackrest/pull/2304); コミット [`76956e7`](https://github.com/pgbackrest/pgbackrest/commit/76956e71cfa3044867213bd65a6f22e96120c108)

**改善：**

- デュアルスタック接続のサポートを改善しました。 (*レビュー：Stephen Frost。提案：Timothée Peignier。*)

  ホスト名がIPv4とIPv6など複数のアドレスに解決される場合、RFC 8305の「happy eyeballs」方式に従い、先のアドレスに妥当な接続時間を与えた後で次のアドレスを試します。失敗も接続もせずに続く試行が、利用可能な時間をすべて使い切ることはなくなりました。

  課題 [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); プルリクエスト [#2235](https://github.com/pgbackrest/pgbackrest/pull/2235); コミット [`7448fde`](https://github.com/pgbackrest/pgbackrest/commit/7448fde157c6d22f57b90c0cef11957b0aadf4b3)
- mesonを主なビルドシステムにしました。 (*レビュー：Stephen Frost。*)

  テストとドキュメントのビルドに使うビルドシステムをmesonに変更しました。モジュール外で使わない関数を非公開にし、バイナリーを小さくしました。

  [`e3d9df3`](https://github.com/pgbackrest/pgbackrest/commit/e3d9df3ae9669ee5749b970d59f8afeb20fd3d9d) mesonを主なビルドシステムにしました。; プルリクエスト [#2264](https://github.com/pgbackrest/pgbackrest/pull/2264)

  [`f287178`](https://github.com/pgbackrest/pgbackrest/commit/f287178b705cc90aa887d66c932e2a223029649b) 関数と変数の可視性をhiddenに設定しました。; プルリクエスト [#2265](https://github.com/pgbackrest/pgbackrest/pull/2265)
- 差分照合を行わない増分バックアップで、変更されていないファイルを検出するようにしました。 (*レビュー：Stephen Frost。*)

  deltaを使わない差分・増分バックアップでは、1つのバッファーに収まるファイル、またはブロック増分ファイルを以前のバックアップのファイルと比較し、変更がなければ保存する代わりに参照します。

  プルリクエスト [#2257](https://github.com/pgbackrest/pgbackrest/pull/2257); コミット [`9d91d1b`](https://github.com/pgbackrest/pgbackrest/commit/9d91d1b2f817b543fc8d970af56d1442c325ed7c)
- `backup_label`を削除した場合に、無効なリカバリーが行われることを防ぎました。 (*レビュー：Stephen Frost。*)

  復元したクラスターから`backup_label`を削除すると、PostgreSQLは`pg_control`のチェックポイントでクラッシュリカバリを行い、ほぼ確実にクラスターを破損させます。現在は復元時に`pg_control`のチェックポイントを無効化し、代わりにリカバリを失敗させます。`pg_controldata`ではチェックポイントを`0/DEAD`と表示します。

  プルリクエスト [#2232](https://github.com/pgbackrest/pgbackrest/pull/2232); コミット [`e634fd8`](https://github.com/pgbackrest/pgbackrest/commit/e634fd85cedc1ae3aef7c4fa2556d7d73d05cb8a)
- `archive-push`のWALセグメントキューの処理を改善しました。 (*レビュー：Stephen Frost。*)

  キューのサイズを測るために、全WALセグメントのサイズを読み取っていました。現在は、最初のセグメントのサイズをすべてに使用します。

  プルリクエスト [#2277](https://github.com/pgbackrest/pgbackrest/pull/2277); コミット [`cf17515`](https://github.com/pgbackrest/pgbackrest/commit/cf17515e409440eecfb04bf7186790d8baa8ab12)
- 再開機能をフルバックアップのみに制限しました。 (*レビュー：Stephen Frost, Stefan Fercot。*)

  deltaを使った差分・増分バックアップの再開は正しく動作していませんでした。また、前回のバックアップ以降に変更されたファイルは、再開するまでに再び変更される可能性が高いため、現在はフルバックアップだけを再開します。

  プルリクエスト [#2268](https://github.com/pgbackrest/pgbackrest/pull/2268); コミット [`dddcbcd`](https://github.com/pgbackrest/pgbackrest/commit/dddcbcd8e9a1cae578b0cc5bb2d1aa768330f3c5)
- ブロック増分バックアップの再開機能を更新しました。 (*レビュー：Stephen Frost。*)

  再開処理はブロック増分ファイルを削除していたため、動作はしても、すべてを再コピーしていました。現在は、再開時にブロック増分ファイルを保持します。

  プルリクエスト [#2296](https://github.com/pgbackrest/pgbackrest/pull/2296); コミット [`ff47450`](https://github.com/pgbackrest/pgbackrest/commit/ff47450402fde5ebc64a08d31791551bee52200e)
- バージョンとヘルプの表示に、`--version`と`--help`を使用できるようにしました。 (*レビュー：Greg Sabino Mullane。提案：Greg Sabino Mullane。*)

  `--version`と`--help`を多くのプログラムと同じように使えるようにしました。特定のコマンドやオプションのヘルプには`help`を使います。

  プルリクエスト [#2263](https://github.com/pgbackrest/pgbackrest/pull/2263); コミット [`68db307`](https://github.com/pgbackrest/pgbackrest/commit/68db3075d7ac4a48377967ad54e45b95b9ee6c61)
- autoconf/makeによるビルドに、詳細なバックトレースを追加しました。 (*レビュー：Stephen Frost。*)

  autoconf/makeビルドのエラースタックトレースに、libbacktraceの詳細情報を含めるようにしました。性能テストでは、目立ったコストはありませんでした。

  プルリクエスト [#1970](https://github.com/pgbackrest/pgbackrest/pull/1970); コミット [`676700d`](https://github.com/pgbackrest/pgbackrest/commit/676700d8ca6f2e0e0ab8123aa9606c8ec7aa81ae)

**ドキュメントの改善：**

- `recovery.conf`への言及を更新しました。 (*レビュー：Stefan Fercot。提案：Stephen Frost。*)

  `recovery.conf`に言及する箇所に、新しいPostgreSQLで使う`postgresql.auto.conf`も含めるようにしました。

  プルリクエスト [#2281](https://github.com/pgbackrest/pgbackrest/pull/2281); コミット [`6835178`](https://github.com/pgbackrest/pgbackrest/commit/68351785f6816a23526900db595557cf6e3a0056)

### v2.50リリースノート {#v250-release-notes}

*性能改善と不具合修正*

*2024年1月22日リリース*

**バグ修正：**

- ブロック増分リストアで、読み取り結果が要求した長さに満たない場合の問題を修正しました。 (*レビュー：Stephen Frost。テスト：Brent Graveland。報告：Adol Rodriguez, Brent Graveland。*)

  圧縮されたスーパーブロックの末尾には、展開には不要でもデータ終端を示すバイトが含まれることがあります。バッファーとデータの位置関係によってはこれらを読み取らず、復元が失敗していました。

  課題 [#2215](https://github.com/pgbackrest/pgbackrest/issues/2215); 課題 [#2238](https://github.com/pgbackrest/pgbackrest/issues/2238); プルリクエスト [#2256](https://github.com/pgbackrest/pgbackrest/pull/2256); コミット [`f4a4af2`](https://github.com/pgbackrest/pgbackrest/commit/f4a4af299bee93ab7dde599ccdb35becc1c2afad)
- オーバーフローによって`info`出力のバックアップ進捗が表示されなくなる問題を修正しました。 (*修正：Robert Donovan。レビュー：Joe Wildish。*)

  ロックファイル内のサイズを32ビット値として読んでいたため、4GiBを超えるバックアップの進捗を`info`コマンドが報告していませんでした。

  課題 [#2251](https://github.com/pgbackrest/pgbackrest/issues/2251); プルリクエスト [#2252](https://github.com/pgbackrest/pgbackrest/pull/2252); コミット [`25f1489`](https://github.com/pgbackrest/pgbackrest/commit/25f14898babf4ad78baef3e8343933a863633975)

**改善：**

- ブロック増分バックアップの差分リストアで、部分的なファイルを保持するようにしました。 (*レビュー：Stephen Frost。*)

  たとえば失敗した復元の再試行や、小さなファイルへの上書き復元では、予想より小さいファイルのブロックも再利用できますが、ブロック増分の差分復元でそのようなファイルを保持していませんでした。

  プルリクエスト [#2254](https://github.com/pgbackrest/pgbackrest/pull/2254); コミット [`a42614e`](https://github.com/pgbackrest/pgbackrest/commit/a42614e8f3a9e6871c16331f01c2cd765ab181aa)
- コンパイル時の標準以外のページサイズをサポートしました。 (*貢献：Viktor Kurilko。レビュー：David Steele。*)

  PostgreSQLは、たとえば4096など異なるページサイズでビルドできます。Greenplumなどの派生版がこれを利用しています。

  プルリクエスト [#2197](https://github.com/pgbackrest/pgbackrest/pull/2197); コミット [`89d5278`](https://github.com/pgbackrest/pgbackrest/commit/89d5278b74ab0d880345575d7ac4c239cd1fce54)
- バンドル時に、バックアップ中に切り詰められたファイルをスキップするようにしました。 (*貢献：Georgy Shelkovy。レビュー：David Steele。*)

  ファイルをバンドルに割り当てた後でゼロに切り詰められたファイルもバンドルに保存しており、デバッグビルドではアサーションに失敗していました。現在は、これらをスキップします。

  [`02eea55`](https://github.com/pgbackrest/pgbackrest/commit/02eea555c7169e99892fdbc8ce7cc1ee59f50509) バンドル時に、バックアップ中に切り詰められたファイルをスキップするようにしました。; プルリクエスト [#2227](https://github.com/pgbackrest/pgbackrest/pull/2227)

  [`c879509`](https://github.com/pgbackrest/pgbackrest/commit/c8795094d418802a0e24d4d19da66973c71b00e5) backupFile()からconstのチェックサムバッファーを返せるようにしました。

  [`9049fec`](https://github.com/pgbackrest/pgbackrest/commit/9049fec2c02c4110e16ffdff7b56f83d8ff32b4a) バンドル化でバックアップ中に切り詰められたファイルをスキップする処理をリファクタリングしました。

  [v2.49](#v249-release-notes)での開発：

  [`337da35`](https://github.com/pgbackrest/pgbackrest/commit/337da35ab278e058ec4cdffeb4319f1a1e2cb0df) バックアップ中に切り詰められたバンドル内ファイルの動作を示すテストを追加しました。
- SFTPストレージのエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  プルリクエスト [#2249](https://github.com/pgbackrest/pgbackrest/pull/2249); コミット [`7c17eec`](https://github.com/pgbackrest/pgbackrest/commit/7c17eec3db455d3e8e660f4f8247b6975517648f)

### v2.49リリースノート {#v249-release-notes}

*PostgreSQL 9.3のサポート終了*

*2023年11月27日リリース*

**バグ修正：**

- 再試行のリグレッションを修正しました。 (*レビュー：Stephen Frost。報告：Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier。*)

  v2.48では操作がタイムアウトを使い切った際の再試行がなくなり、たとえばオブジェクトストアのソケットが書き込み可能になるのを待つ際、タイムアウトがエラーになっていました。現在は、タイムアウト後でも2回再試行します。

  [`3c116e1`](https://github.com/pgbackrest/pgbackrest/commit/3c116e1829a0df62aaf50ce241c63d829eb438e0) 未使用のヘッダーを削除しました。

  [`fa5b2d4`](https://github.com/pgbackrest/pgbackrest/commit/fa5b2d44ad9f7591517eecaaaaeb07e9500dd51c) 再試行のリグレッションを修正しました。; 課題 [#2200](https://github.com/pgbackrest/pgbackrest/issues/2200); 課題 [#2214](https://github.com/pgbackrest/pgbackrest/issues/2214); プルリクエスト [#2221](https://github.com/pgbackrest/pgbackrest/pull/2221)
- SFTPストレージドライバーでの再帰的なパス削除を修正しました。 (*修正：Reid Thompson。レビュー：Stephen Frost。報告：Luc。*)

  一部のSFTPサーバーは、ディレクトリーをファイルとしてunlinkするとfailureではなくpermission deniedを返すため、パスの再帰削除が失敗していました。

  課題 [#2219](https://github.com/pgbackrest/pgbackrest/issues/2219); プルリクエスト [#2226](https://github.com/pgbackrest/pgbackrest/pull/2226); コミット [`c4dc466`](https://github.com/pgbackrest/pgbackrest/commit/c4dc4665f88e9d67a3b66f44cd59d6dd4bb5107f)

**改善：**

- PostgreSQL `9.3`のサポートを削除しました。 (*レビュー：Stephen Frost。*)

  サポート終了したPostgreSQLを5バージョンまでサポートする方針に従い、PostgreSQL 9.3のサポートを終了しました。

  プルリクエスト [#2220](https://github.com/pgbackrest/pgbackrest/pull/2220); コミット [`dcf0781`](https://github.com/pgbackrest/pgbackrest/commit/dcf078198761a2cfe9be6b4c7f4b4fb07ef53cbf)

**ドキュメントの機能：**

- メンテナー向けオプションを説明しました。 (*レビュー：Stefan Fercot。*)

  保守担当者向けオプションを、使用上の注意とともに専用セクションへまとめました。また、`pg-version-force`を内部専用ではなくしました。

  プルリクエスト [#2202](https://github.com/pgbackrest/pgbackrest/pull/2202); コミット [`21c8c8a`](https://github.com/pgbackrest/pgbackrest/commit/21c8c8a66cb06eba714bfa41bed7239af3d14f08)
- PostgreSQL >= 13向けにポイントインタイムリカバリーの説明を更新しました。

  PostgreSQL 13以降では、復旧目標に到達しないとリカバリがエラーになります。特定時点へのリカバリの説明を、古いバージョンだけでなくPostgreSQL 13以降でも使えるようにしました。

  コミット [`eb69e2e`](https://github.com/pgbackrest/pgbackrest/commit/eb69e2ee6339047f0145b751437ac2bec82bb5ab)

**テストスイートの改善：**

- `libssh2`がインストールされていなくても、`config/load`単体テストを実行できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Wu Ning。*)

  課題 [#2193](https://github.com/pgbackrest/pgbackrest/issues/2193); プルリクエスト [#2194](https://github.com/pgbackrest/pgbackrest/pull/2194); コミット [`e2b734e`](https://github.com/pgbackrest/pgbackrest/commit/e2b734eff97e3fac32895b799cc32126013aae27)

### v2.48リリースノート {#v248-release-notes}

*リポジトリストレージのタグ*

*2023年9月25日リリース*

**バグ修正：**

- ブロックリストなしでブロック増分バックアップをリストアする際の問題を修正しました。 (*レビュー：Stephen Frost。テスト：Burak Yurdakul。報告：Burak Yurdakul。*)

  ファイルの内容は変わらずタイムスタンプだけが変わった場合に書かれる、ブロックを含まないブロックマップが、同じバンドル読み取りでブロック増分を使わず保存されたファイルの後にあると、復号されていませんでした。対象ファイルが多いと再試行回数を使い切り、復元に失敗していました。

  課題 [#2182](https://github.com/pgbackrest/pgbackrest/issues/2182); プルリクエスト [#2184](https://github.com/pgbackrest/pgbackrest/pull/2184); コミット [`31de127`](https://github.com/pgbackrest/pgbackrest/commit/31de127cf42438b1fac04c161c47264aa1fb1060)

**新機能：**

- オブジェクトタグを作成する`--repo-storage-tag`オプションを追加しました。 (*レビュー：Stephen Frost, Stefan Fercot, Timothée Peignier。*)

  S3、GCS、Azureリポジトリへ書き込むオブジェクトにタグを付けるには、`repo-storage-tag`を設定します。タグはリポジトリごとに設定します。

  課題 [#2150](https://github.com/pgbackrest/pgbackrest/issues/2150); プルリクエスト [#2159](https://github.com/pgbackrest/pgbackrest/pull/2159); コミット [`1b4e0cc`](https://github.com/pgbackrest/pgbackrest/commit/1b4e0cce5f3ff5ea3ee0b889e6d4ce4de1430b04)
- SFTPストレージドライバーに既知のホストのチェックを追加しました。 (*貢献：Reid Thompson。レビュー：Stephen Frost, David Steele。*)

  SFTPのホストキーを、デフォルトで既知のホストファイルと照合するようになりました。つまり、`repo-sftp-host-key-check-type=strict`がデフォルトです。新しいホストを自動追加するには`repo-sftp-host-key-check-type=accept-new`を、従来どおり検査を省略するには`repo-sftp-host-key-check-type=none`を設定します。

  プルリクエスト [#2125](https://github.com/pgbackrest/pgbackrest/pull/2125); コミット [`ce9ba0f`](https://github.com/pgbackrest/pgbackrest/commit/ce9ba0fadee652d409488bee701ea6a51cafec75)
- デュアルスタック接続をサポートしました。 (*レビュー：Stephen Frost。*)

  ホスト名が解決する各アドレスを、接続が成功するかタイムアウトするまで順番に試すようになりました。たとえば、ホストへの経路がないIPv6アドレスの次にIPv4アドレスを試します。繰り返し発生した再試行エラーも、エラーメッセージ内でまとめます。

  [`5314dbf`](https://github.com/pgbackrest/pgbackrest/commit/5314dbffc761bc7507db02693f2421c1578efe10) Waitオブジェクトの入れ子時の精度を改善しました。

  [`c180513`](https://github.com/pgbackrest/pgbackrest/commit/c1805134b370f0c5c54c40a2df8978599328784f) ErrorRetryの出力で再試行エラーを集約しました。

  [`edbd520`](https://github.com/pgbackrest/pgbackrest/commit/edbd520c81f5d437963aaf42d1c79b2c51d01665) アドレス一覧の検索処理をリファクタリングし、返されたすべてのアドレスを含めるようにしました。; プルリクエスト [#2174](https://github.com/pgbackrest/pgbackrest/pull/2174)

  [`39bb8a0`](https://github.com/pgbackrest/pgbackrest/commit/39bb8a0d3a96eef63219dff262a9306a4f59dae9) デュアルスタック接続をサポートしました。; 課題 [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); プルリクエスト [#2175](https://github.com/pgbackrest/pgbackrest/pull/2175)
- `info`コマンドのJSON出力に、バックアップサイズの完了分と合計を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  `info`コマンドのJSON出力に、実行中のバックアップの完了済みサイズと合計サイズを含めるようになり、他のプログラムから進捗を監視できます。

  課題 [#2007](https://github.com/pgbackrest/pgbackrest/issues/2007); プルリクエスト [#2141](https://github.com/pgbackrest/pgbackrest/pull/2141); コミット [`e3fcd8c`](https://github.com/pgbackrest/pgbackrest/commit/e3fcd8cd9e0be42a32fc4cbd2ae3db2c072eabcd)

**改善：**

- 複数のstanzaを対象とするcheckコマンドを追加しました。 (*レビュー：Stephen Frost。*)

  `stanza`を指定しない場合、`check`コマンドは設定内のすべてのスタンザを確認するようになりました。

  プルリクエスト [#2057](https://github.com/pgbackrest/pgbackrest/pull/2057); コミット [`1141dc2`](https://github.com/pgbackrest/pgbackrest/commit/1141dc20708cf0c68296f83e74c872a7db9c2bd9)
- チェックサムが有効になるまで、`pg_control`の読み取りを再試行するようにしました。 (*レビュー：Stefan Fercot, Stephen Frost。*)

  ext4など一部のファイルシステムでは、書き込みと同時に`pg_control`を読み取ると、不完全なデータが返ることがあります。現在はチェックサムが有効になるまで読み取りを再試行します。

  プルリクエスト [#2131](https://github.com/pgbackrest/pgbackrest/pull/2131); コミット [`f42d927`](https://github.com/pgbackrest/pgbackrest/commit/f42d927d2dcd58cf5a80d68eaf6888bcf2c67a4b)
- バックアップが成功した後のWALセグメントのチェックを最適化しました。 (*レビュー：Stephen Frost。*)

  バックアップ後のWALセグメントの確認では、セグメントごとにストレージを一覧取得していました。現在はWALディレクトリーごとに1回だけ一覧を取得し、再利用します。

  プルリクエスト [#2169](https://github.com/pgbackrest/pgbackrest/pull/2169); コミット [`9d3a605`](https://github.com/pgbackrest/pgbackrest/commit/9d3a605900644059ff0e030d71a818b3965eb031)
- GCSのマルチパート処理の性能を改善しました。 (*レビュー：Reid Thompson。*)

  マルチパートアップロードのチャンクを、準備でき次第アップロードするようにしました。

  プルリクエスト [#2162](https://github.com/pgbackrest/pgbackrest/pull/2162); コミット [`6cb9c40`](https://github.com/pgbackrest/pgbackrest/commit/6cb9c40fb8ea18e6572bf3f6e44bbb1d8f922682)
- stanzaが停止していても`archive-get`コマンドを実行できるようにしました。 (*レビュー：Tom Swartz, David Christensen, Reid Thompson。*)

  `archive-get`コマンドはリポジトリに書き込まないため、`restore`と同様に、スタンザ停止中でも実行できるようになりました。

  コミット [`fbd992a`](https://github.com/pgbackrest/pgbackrest/commit/fbd992adc7b18db5e70774d675c160c8c8e2f031)
- SFTP公開鍵／秘密鍵のパスの先頭に、チルダを使用できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  `repo-sftp-private-key-file`と`repo-sftp-public-key-file`のパスを、ドキュメントどおり`~`で始められるようにしました。

  プルリクエスト [#2136](https://github.com/pgbackrest/pgbackrest/pull/2136); コミット [`eb32d6d`](https://github.com/pgbackrest/pgbackrest/commit/eb32d6de5e1575a37efb166abbf7df400d93352e)
- 認証トークンの更新前に、GCSの認証情報を再読み込みするようにしました。 (*レビュー：Stephen Frost。提案：Daniel Farina。*)

  認証トークンの更新前にサービスキーのファイルを再読み込みするため、コマンド実行中にキーを置き換えられるようになりました。

  プルリクエスト [#2072](https://github.com/pgbackrest/pgbackrest/pull/2072); コミット [`995a8e9`](https://github.com/pgbackrest/pgbackrest/commit/995a8e96691d23eaf3914a425669f89deb3ce002)

**ドキュメントの不具合修正：**

- 設定リファレンスの`tls-server-address`オプションの例を修正しました。 (*修正：Hartmut Goebel。レビュー：David Steele。*)

  例の`::*`は無効でした。IPv4には`*`、IPv6には`::`を使用してください。

  プルリクエスト [#2165](https://github.com/pgbackrest/pgbackrest/pull/2165); コミット [`43524a4`](https://github.com/pgbackrest/pgbackrest/commit/43524a47a4c6a847f76514812f94b87cb7af4c05)
- コマンドリファレンスの`filter`オプションの例を修正しました。

  コミット [`cb3ff6e`](https://github.com/pgbackrest/pgbackrest/commit/cb3ff6ed4336af9e4c0643d8224d5bc3d790a655)

**テストスイートの改善：**

- `libssh2`がインストールされていなくても、`storage/sftp`単体テストを実行できるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Wu Ning。*)

  課題 [#2163](https://github.com/pgbackrest/pgbackrest/issues/2163); プルリクエスト [#2177](https://github.com/pgbackrest/pgbackrest/pull/2177); コミット [`c3c0834`](https://github.com/pgbackrest/pgbackrest/commit/c3c0834e170196a1241a368779162fcca65f9ad5)

### v2.47リリースノート {#v247-release-notes}

*性能改善と不具合修正*

*2023年7月24日リリース*

**バグ修正：**

- 差分照合を行うバックアップ中に、マニフェストのブロック増分情報を保持するようにしました。 (*レビュー：Stephen Frost。報告：Francisco Miguel Biete Banon。*)

  ファイルがブロック増分の適用しきい値を下回るサイズに縮小したり、タイムスタンプが十分過去へ移動したりして、新規ファイルならブロック増分を使わない状態に変わると、以前のバックアップを引き続き参照できるにもかかわらず、deltaバックアップのマニフェストからそのブロック増分情報が失われていました。

  [`1d42aed`](https://github.com/pgbackrest/pgbackrest/commit/1d42aed152563fff6ec70c517d86eb39158b3f20) command/backupユニットテストで、参照ファイルの検証を改善しました。

  [`4c27d74`](https://github.com/pgbackrest/pgbackrest/commit/4c27d74bbd3a44d8ab1af140277d3cd8302060c2) 差分照合を行うバックアップ中に、マニフェストのブロック増分情報を保持するようにしました。; 課題 [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); プルリクエスト [#2123](https://github.com/pgbackrest/pgbackrest/pull/2123)
- `verify`コマンドでのブロック増分ファイル名を修正しました。 (*レビュー：Reid Thompson。報告：Francisco Miguel Biete Banon。*)

  `verify`コマンドは、バンドル外に保存されたブロック増分ファイルに`.pgbi`ではなく圧縮形式の拡張子を使っていたため、ファイルを見つけられませんでした。

  課題 [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); プルリクエスト [#2120](https://github.com/pgbackrest/pgbackrest/pull/2120); コミット [`cdb7e26`](https://github.com/pgbackrest/pgbackrest/commit/cdb7e26350822b55c00771d6d575242b1202e741)
- スタンバイからのバックアップで、差分照合を行うバックアップへ自動的に誤って切り替わる問題を修正しました。 (*レビュー：Stephen Frost。報告：krmozejko, Don Seiler。*)

  空き領域マップなどはスタンバイとプライマリーでサイズが異なることがあり、そのため次の増分バックアップがプライマリーのサイズ変更を検出して、時間のかかるチェックサムによる差分処理へ切り替わることがありました。現在は元のサイズをマニフェストに保持し、比較に使用します。

  課題 [#2020](https://github.com/pgbackrest/pgbackrest/issues/2020); プルリクエスト [#2124](https://github.com/pgbackrest/pgbackrest/pull/2124); コミット [`5ed6f8d`](https://github.com/pgbackrest/pgbackrest/commit/5ed6f8df1487174985c42d6e13c367d70c2d8b8a)
- PostgreSQL >= 12でリカバリーの`type=none`を指定した場合、`recovery.signal`を作成しないようにしました。 (*レビュー：Stefan Fercot。報告：T.Anastacio。*)

  `type=none`の場合、PostgreSQL >= 12で`recovery.signal`を書き込まなくなり、以前のバージョンと同じ動作になりました。

  課題 [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); プルリクエスト [#2070](https://github.com/pgbackrest/pgbackrest/pull/2070); コミット [`9cceed6`](https://github.com/pgbackrest/pgbackrest/commit/9cceed6ac4a32c14a797eba89a4ad1dc06d89d80)
- diff/incrバックアップの一意なラベルの生成を修正しました。 (*修正：Andrey Sokolov。レビュー：David Steele。*)

  フルバックアップが2つ以上あり、最新のものが期限切れの場合、差分・増分バックアップのラベルを期限切れのフルバックアップのラベルと比較していたため、時計が逆行したかのように失敗していました。

  課題 [#1873](https://github.com/pgbackrest/pgbackrest/issues/1873); プルリクエスト [#2104](https://github.com/pgbackrest/pgbackrest/pull/2104); コミット [`0ac0934`](https://github.com/pgbackrest/pgbackrest/commit/0ac09344dc17fb54e250705ce49399b86329bb3d)
- 期限切れになるバックアップがない場合の、時間に基づくアーカイブの期限切れ処理を修正しました。 (*レビュー：Stefan Fercot。*)

  時間ベースの保持条件を満たしても期限切れになるバックアップがない場合、アーカイブを期限切れにせず、"time-based archive retention not met"をログ出力していました。以前のWALを期限切れにするため、さらに1つバックアップが必要になっていました。

  課題 [#2103](https://github.com/pgbackrest/pgbackrest/issues/2103); プルリクエスト [#2109](https://github.com/pgbackrest/pgbackrest/pull/2109); コミット [`762498f`](https://github.com/pgbackrest/pgbackrest/commit/762498f4cd5f1425db4c176fc707926d62cc7c04)

**改善：**

- SFTPストレージドライバーの性能を改善しました。 (*貢献：Stephen Frost, Reid Thompson。レビュー：David Steele。*)

  SFTPストレージドライバーは、libssh2が続行できないと一定時間待っていました。現在は、ソケットが読み書き可能になるまで待ちます。

  [`e280ed9`](https://github.com/pgbackrest/pgbackrest/commit/e280ed9098a6f5da9bdabb541e9c69d4f24ffcf2) storage/sftpの結果コード処理をより一貫したものにしました。

  [`125676a`](https://github.com/pgbackrest/pgbackrest/commit/125676ae0e98d3730d2dc0d47e37ca1df145d044) storageSftpNew()の初期化とハンドシェイクを整理しました。

  [`28b6b2d`](https://github.com/pgbackrest/pgbackrest/commit/28b6b2d4659d78ce67c1bd3104d96e5705d955c9) SFTPストレージドライバーの性能を改善しました。; プルリクエスト [#2089](https://github.com/pgbackrest/pgbackrest/pull/2089)
- `info`コマンドの日付／時刻出力にタイムゾーンオフセットを追加しました。 (*レビュー：Stefan Fercot, Philip Hurst。提案：Philip Hurst。*)

  `info`コマンドが出力するタイムスタンプにタイムゾーンオフセットを含めるようになり、たとえば`--target`で、そのまま復旧目標として使用できます。

  [`9efd5cd`](https://github.com/pgbackrest/pgbackrest/commit/9efd5cd0bb40c5dc2fcac2e21c9b62e554b94db6) `info`コマンドの日付／時刻出力にタイムゾーンオフセットを追加しました。; 課題 [#2093](https://github.com/pgbackrest/pgbackrest/issues/2093); プルリクエスト [#2095](https://github.com/pgbackrest/pgbackrest/pull/2095)

  [`aa229a1`](https://github.com/pgbackrest/pgbackrest/commit/aa229a1deef3afeebb66db1443b19e24559adf96) Coverityの指摘に基づきtime_tのキャストを変更しました。
- サポートされていない機能のエラー処理を集約しました。 (*レビュー：Stefan Fercot。*)

  lz4など、ビルドに含まれない機能のエラーをより詳しく一貫したものにしました。SFTPを組み込んでいない場合にSFTPストレージを指定しても、アサーションに失敗しなくなりました。

  [`de46276`](https://github.com/pgbackrest/pgbackrest/commit/de46276bf60b8a2181621b123d1a99e56808a089) config/parseモジュールの許可リスト処理をリファクタリングしました。

  [`36ff81d`](https://github.com/pgbackrest/pgbackrest/commit/36ff81dc6ff7e98e40c0c05a4a343a71b91b1678) サポートされていない機能のエラー処理を集約しました。; プルリクエスト [#2075](https://github.com/pgbackrest/pgbackrest/pull/2075)

**ドキュメントの改善：**

- ユーザーガイドで、パッケージからのインストールを優先することを明確にしました。 (*レビュー：Stefan Fercot。提案：dr-kd。*)

  プルリクエスト [#2090](https://github.com/pgbackrest/pgbackrest/pull/2090); コミット [`a36f480`](https://github.com/pgbackrest/pgbackrest/commit/a36f480c85c7add6fdf0e5517748d740e3a7b424)

### v2.46リリースノート {#v246-release-notes}

*ブロック増分バックアップとSFTPストレージ*

*2023年5月22日リリース*

**新機能：**

- ブロック増分バックアップを追加しました。 (*レビュー：John Morris, Stephen Frost, Stefan Fercot。*)

  ブロック増分は、前回のバックアップ以降に変更されたファイルの部分だけを保存し、大きいファイルの差分・増分バックアップで容量と時間を節約します。`repo-bundle`を必須とする`repo-block`で有効にします。

  [`dd4e526`](https://github.com/pgbackrest/pgbackrest/commit/dd4e52679ecdc43539bd038b5aa9bd4ff9055cbf) 増分ブロック一覧からチャンク分割とブロック番号を削除しました。; プルリクエスト [#2029](https://github.com/pgbackrest/pgbackrest/pull/2029)

  [`822f2a5`](https://github.com/pgbackrest/pgbackrest/commit/822f2a584260a012b833455a7a2bd1c8487e3010) ブロック増分機能を完成させました。; プルリクエスト [#2053](https://github.com/pgbackrest/pgbackrest/pull/2053)
- リポジトリストレージでSFTPをサポートしました。 (*貢献：Reid Thompson。レビュー：Stephen Frost, David Steele。*)

  SFTPサーバーにリポジトリを保存するには、`repo-type=sftp`と`repo-sftp-host`を設定します。

  プルリクエスト [#1959](https://github.com/pgbackrest/pgbackrest/pull/1959); コミット [`87087fa`](https://github.com/pgbackrest/pgbackrest/commit/87087fac231d2110160b3219daee3f9fb91aec02)

  [v2.42](#v242-release-notes)での開発：

  [`01b81f9`](https://github.com/pgbackrest/pgbackrest/commit/01b81f9d374701eb489dd1888bcba25fb5d6df84) リンク作成をストレージインターフェースへ移しました。; プルリクエスト [#1879](https://github.com/pgbackrest/pgbackrest/pull/1879)
- PostgreSQL 16をサポートしました。 (*レビュー：Stefan Fercot。*)

  PostgreSQL 16のカタログバージョンとWALマジックナンバーを追加しました。

  プルリクエスト [#2051](https://github.com/pgbackrest/pgbackrest/pull/2051); コミット [`3fc3690`](https://github.com/pgbackrest/pgbackrest/commit/3fc3690dd77ef5fa032abb006558184164db53ec)

**改善：**

- ページヘッダーのチェックを省略できるようにしました。 (*レビュー：David Christensen。提案：David Christensen。*)

  ページチェックサムの検証時に行うページヘッダー検査は、暗号化されたページで誤ったエラーを報告することがあります。省略するには`page-header-check=n`を設定します。デフォルトでは有効です。

  プルリクエスト [#2045](https://github.com/pgbackrest/pgbackrest/pull/2045); コミット [`f5e6bc2`](https://github.com/pgbackrest/pgbackrest/commit/f5e6bc26983396ec51c6579aade37db39807f3a5)
- リストア中にリカバリーファイルを`chown()`しないようにしました。 (*レビュー：Stefan Fercot, Marcelo Henrique Neppel。提案：Marcelo Henrique Neppel。*)

  復元処理は、すでに正しい所有者の復元済みファイルでは`chown()`を省略していましたが、自身が書き込むリカバリ用ファイルでは省略していませんでした。現在はPosixドライバーも、所有者が正しければ`chown()`を省略します。

  課題 [#2036](https://github.com/pgbackrest/pgbackrest/issues/2036); プルリクエスト [#2038](https://github.com/pgbackrest/pgbackrest/pull/2038); コミット [`3ff88ff`](https://github.com/pgbackrest/pgbackrest/commit/3ff88ffbb495fd669e9a361478e60192930ee0a1)
- HTTPの再試行で、エラーの再試行に関する詳細を追加しました。

  HTTPの再試行後のエラーに、再試行回数と所要時間を表示するようにしました。

  [`801e396`](https://github.com/pgbackrest/pgbackrest/commit/801e396dace2a4d9f4125ef0e751c90dc0cc644a) エラーモジュールをcommon/errorディレクトリーへ移しました。

  [`df419b3`](https://github.com/pgbackrest/pgbackrest/commit/df419b34b55a15a902ff5cc1912aaebc7e023738) 再試行のエラーメッセージを改善しました。

  [`f33e1cf`](https://github.com/pgbackrest/pgbackrest/commit/f33e1cfb1600643820a1ae76bdeb15c62ac1fcc7) HTTPの再試行で、エラーの再試行に関する詳細を追加しました。

**ドキュメントの改善：**

- リカバリーで`type=none`を使う場合の警告を追加しました。 (*レビュー：Stefan Fercot。*)

  リカバリの`type=none`では、終了時にタイムラインを増やしません。そのため、PostgreSQLが重複したWALをアーカイブしようとして拒否され、ディスクがいっぱいになったり、`pg_rewind`などが失敗したり、クラスターを破損させたりする可能性があります。ドキュメントに注意を追加しました。

  課題 [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); プルリクエスト [#2069](https://github.com/pgbackrest/pgbackrest/pull/2069); コミット [`a28b72c`](https://github.com/pgbackrest/pgbackrest/commit/a28b72c62431bcf9df02791219d9d6f5d0e60b54)
- 作成済みのリポジトリに対して`stanza-create`を実行する場合の注意事項を追加しました。

  既存のスタンザはスキップするため、たとえば新しいリポジトリを設定した後でも、`stanza-create`を安全に再実行できます。

  コミット [`0c1f823`](https://github.com/pgbackrest/pgbackrest/commit/0c1f823e7a3abf1cadb44de3832ec1ddb2da7ec8)

### v2.45リリースノート {#v245-release-notes}

*ブロック増分バックアップ（ベータ版）*

*2023年3月20日リリース*

**バグ修正：**

- オフラインバックアップのリストアでは、デフォルトで`recovery.signal`を書き込まないようにしました。 (*レビュー：Stefan Fercot。報告：Marcel Borger。*)

  PostgreSQL >= 12では、`wal_level=minimal`のオフラインバックアップに`recovery.signal`があるとPostgreSQLの起動が失敗します。現在は、より高い`wal_level`のオフラインバックアップから特定時点へ復旧する場合など、`type`を明示的に指定した場合を除き、オフラインバックアップの復元ではこのファイルを書き込みません。

  [`0818601`](https://github.com/pgbackrest/pgbackrest/commit/0818601c055724bde3b97d4b02d3a38b0a53899a) command/restoreのユニットテストでマニフェストのonlineフラグを設定しました。

  [`2fa7e53`](https://github.com/pgbackrest/pgbackrest/commit/2fa7e53c5d4b5a5fd79f62d39763746727a5b9be) オフラインバックアップのリストアでは、デフォルトで`recovery.signal`を書き込まないようにしました。; 課題 [#2018](https://github.com/pgbackrest/pgbackrest/issues/2018); プルリクエスト [#2019](https://github.com/pgbackrest/pgbackrest/pull/2019)

**新機能：**

- ブロック増分バックアップ（ベータ版）を追加しました。 (*レビュー：John Morris, Stephen Frost, Stefan Fercot。*)

  ブロック増分は、ファイル全体ではなく、前回のバックアップ以降に変更された部分だけを保存します。`repo-bundle`を必須とする`repo-block`で有効にします。この機能はベータ版であり、`beta`オプションも必要です。正式リリースまでにディスク上の形式が変わるため、本番環境では使用しないでください。

  [`089fae0`](https://github.com/pgbackrest/pgbackrest/commit/089fae035bf0a9778fff0527ea3cbb113625a403) real/allテストの出力にブロック増分を追加しました。

  [`3feed38`](https://github.com/pgbackrest/pgbackrest/commit/3feed389a2199454db68e446851323498b45db20) IoChunkedReadのファイル終端処理を改善しました。

  [`d520816`](https://github.com/pgbackrest/pgbackrest/commit/d520816acf9ecb01ef805cecbc9de7e8d0a9f468) deltaMapNew()からパラメーターリストを削除しました。

  [`779efe0`](https://github.com/pgbackrest/pgbackrest/commit/779efe0d7a54340141e01597279e9ab1d0bd0773) ブロック増分のサイズを一貫してsize_tで宣言するようにしました。

  [`dffc933`](https://github.com/pgbackrest/pgbackrest/commit/dffc933384e4327e2fd52868dd19668ed9d3ed91) DeltaMapをBlockHashに改名しました。

  [`a9867cb`](https://github.com/pgbackrest/pgbackrest/commit/a9867cb0b8e8d7abcac9b18b76e3e490c265f3cb) repo-block-age-mapとrepo-block-size-mapオプションを追加しました。

  [`16ac5ee`](https://github.com/pgbackrest/pgbackrest/commit/16ac5ee8d3b926464cd27e8f064579f1e7935f4c) ブロック増分のマニフェストキーを改名しました。

  [`da91858`](https://github.com/pgbackrest/pgbackrest/commit/da9185870222057b97365f5db0acf797f959ec5e) 圧縮形式にオプションのraw形式を追加しました。

  [`7e5adc0`](https://github.com/pgbackrest/pgbackrest/commit/7e5adc03594a3b7a975001e80902a51df3ddd577) バンドル化とブロック増分バックアップにraw圧縮・暗号化を使用しました。

  [`8b5153a`](https://github.com/pgbackrest/pgbackrest/commit/8b5153ad210011812c8fe6db2f2ed829a5aa543a) ブロックレベル増分バックアップのスーパーブロックを追加しました。; プルリクエスト [#1996](https://github.com/pgbackrest/pgbackrest/pull/1996)

  [`210bed4`](https://github.com/pgbackrest/pgbackrest/commit/210bed4511ae5523b170eb193b877346d787140d) ブロック増分チェックサムにSHA-1の代わりにxxHashを使用しました。

  [`6252c0e`](https://github.com/pgbackrest/pgbackrest/commit/6252c0e4485caee362edec13302a5f735a69bff4) ブロック増分バックアップのinfo出力からバックアップセットのサイズを除外しました。

  [`1119a53`](https://github.com/pgbackrest/pgbackrest/commit/1119a5353911d6d326edac325f530bb796a806ae) BlockHashをBlockChecksumに改名しました。

  [`6b409d0`](https://github.com/pgbackrest/pgbackrest/commit/6b409d049eb935146f7996b75b97744b75c411a9) テスト結果に基づき、デフォルトのブロックサイズとスーパーブロックの値を更新しました。

  [`1281a6e`](https://github.com/pgbackrest/pgbackrest/commit/1281a6eaf8552232c8c9af4d7fc15c082a7794d9) ブロックとスーパーブロックのサイズが等しい場合に継続が発生しないようにしました。

  [`5c1f78d`](https://github.com/pgbackrest/pgbackrest/commit/5c1f78d4dd62c37218285d13b09a9450eb3a588e) blockIncrProcess()の誤記を修正しました。

  [`c30d3e4`](https://github.com/pgbackrest/pgbackrest/commit/c30d3e439b77d544477e289606d30d0c8ffe301f) ブロック増分マップを修正・改善しました。; プルリクエスト [#2026](https://github.com/pgbackrest/pgbackrest/pull/2026)

  [`24f7252`](https://github.com/pgbackrest/pgbackrest/commit/24f725212d0c1dedc0f34fe4e939e481585ff697) ベータ機能を扱う基盤を追加しました。

  [`04d224b`](https://github.com/pgbackrest/pgbackrest/commit/04d224b88e73194ff1c6497dbecaaff392008dfe) ブロック増分バックアップのベータ機能とドキュメントを追加しました。

  [v2.44](#v244-release-notes)での開発：

  [`912eec6`](https://github.com/pgbackrest/pgbackrest/commit/912eec63bb971c10a545e582f628c982f4e00005) ブロックレベルの増分バックアップを追加しました。; 課題 [#959](https://github.com/pgbackrest/pgbackrest/issues/959); 課題 [#1806](https://github.com/pgbackrest/pgbackrest/issues/1806); 課題 [#1913](https://github.com/pgbackrest/pgbackrest/issues/1913); プルリクエスト [#1916](https://github.com/pgbackrest/pgbackrest/pull/1916)

  [v2.42](#v242-release-notes)での開発：

  [`1ea6a41`](https://github.com/pgbackrest/pgbackrest/commit/1ea6a4142e47e2e0b56911ad1f028dfcddc5fd64) マニフェストファイルの更新を改善しました。; プルリクエスト [#1888](https://github.com/pgbackrest/pgbackrest/pull/1888)

  [`c647bcb`](https://github.com/pgbackrest/pgbackrest/commit/c647bcb50954f623d29104cdb8a1457ed8e94579) バックアップ中のファイル処理用のフラグをマニフェストに追加しました。; プルリクエスト [#1889](https://github.com/pgbackrest/pgbackrest/pull/1889)

  [`102ce5d`](https://github.com/pgbackrest/pgbackrest/commit/102ce5dee47e8d9a8d2eeaf2b2cc2bac105914ef) マニフェストに永続的な参照一覧を追加しました。; プルリクエスト [#1890](https://github.com/pgbackrest/pgbackrest/pull/1890)

  [`ac99201`](https://github.com/pgbackrest/pgbackrest/commit/ac99201c0ebde616279214e600e49fdf506f7469) cvtUInt64FromVarInt128()にbufferSizeを追加し、読み取りをさらに制限しました。

  [`5602f17`](https://github.com/pgbackrest/pgbackrest/commit/5602f179a177a8513b96c762590829c012c28175) IoRead/IoWriteにvarint-128のエンコードとデコードを追加しました。; プルリクエスト [#1891](https://github.com/pgbackrest/pgbackrest/pull/1891)

  [`352cbf1`](https://github.com/pgbackrest/pgbackrest/commit/352cbf1d5738a720292b5067051a05efc2b9a8ac) ManifestFileの真偽値をビットフィールドに変更しました。

  [`e7e106f`](https://github.com/pgbackrest/pgbackrest/commit/e7e106f781be01027d4829b258902549eb36eb7b) restoreFile()のチェックサム計算に読み取り専用ストレージを使うようにしました。

  [`909be41`](https://github.com/pgbackrest/pgbackrest/commit/909be412f8ad0d87f23ce2a2dbca94c3e0732f9f) command/backupとcommand/restoreのユニットテストを入れ替えました。

  [`1730ef4`](https://github.com/pgbackrest/pgbackrest/commit/1730ef4ac3d88137bd218e6128b0107a8bf2c121) storageNewWriteP()にnoTruncateフラグを追加しました。; プルリクエスト [#1898](https://github.com/pgbackrest/pgbackrest/pull/1898)

  [`fee38c2`](https://github.com/pgbackrest/pgbackrest/commit/fee38c2c7cc3ae318bf0d3b50fe23c22900c2311) ハンドラー配列としてリモートストレージにフィルターを渡すようにしました。

  [`5fceee8`](https://github.com/pgbackrest/pgbackrest/commit/5fceee88a9439460bf24082f275ec2e695cc6bf6) backupFileRepoPathP()を追加しました。

  [`221db61`](https://github.com/pgbackrest/pgbackrest/commit/221db610d2a054ed00ad27377663941abfb9fb98) real/all結合テストのマトリクス内の名前を短くしました。

  [`c9db7bc`](https://github.com/pgbackrest/pgbackrest/commit/c9db7bc274211820030c4ab6ab8c70c1b1896254) cipherBlockNew()で省略可能なパラメーターを扱えるようにしました。

  [`58b3c91`](https://github.com/pgbackrest/pgbackrest/commit/58b3c91babc6af9e003e5ef09bf99becf8a6f827) 容量を節約するため、CipherBlockにrawモードを追加しました。

**改善：**

- すべてデフォルト値のグループインデックスは、1つだけ保持するようにしました。 (*レビュー：Stefan Fercot。*)

  `repo2-type`が`s3`でない場合の`repo2-s3-key`など、適用されないオプションが、デフォルト値しか持たない実体のないリポジトリを追加することがありました。現在は、他のインデックスが1つも残らない場合を除き、デフォルト値しかないリポジトリとPostgreSQLのインデックスを削除します。

  プルリクエスト [#2011](https://github.com/pgbackrest/pgbackrest/pull/2011); コミット [`1648c13`](https://github.com/pgbackrest/pgbackrest/commit/1648c133d6bc1ffd0682ae6219934d00295aa580)

**ドキュメントの改善：**

- `2.x`バージョン間のアップグレードについて、明示的な手順を追加しました。 (*貢献：Christophe Courtois。レビュー：David Steele。*)

  ユーザーガイドに、`2.x`間のアップグレードには新しいバイナリーのインストールだけが必要と説明するセクションを追加しました。古いバージョンがサポートしない機能を使っていなければ、ダウングレードも可能です。

  課題 [#1774](https://github.com/pgbackrest/pgbackrest/issues/1774); プルリクエスト [#1993](https://github.com/pgbackrest/pgbackrest/pull/1993); コミット [`15d5dcd`](https://github.com/pgbackrest/pgbackrest/commit/15d5dcdd3bb387aab28bbe7262011c38c7d6d22c)
- TLSの導入により不要になったSSHへの言及を削除しました。

  `repo-host`、`pg-host`とそれらのポートオプションのヘルプで、SSHを唯一のリモートプロトコルとして説明しなくなりました。SSH圧縮の詳細も削除しました。

  コミット [`c5907a2`](https://github.com/pgbackrest/pgbackrest/commit/c5907a2e7193ca8f79cf56dca23e0df118e686c3)

### v2.44リリースノート {#v244-release-notes}

*PostgreSQL 9.0/9.1/9.2のサポート終了*

*2023年1月30日リリース*

**改善：**

- PostgreSQL `9.0`/`9.1`/`9.2`のサポートを終了しました。 (*レビュー：Stefan Fercot。*)

  pgBackRestは、サポート中の5バージョンと直近のサポート終了済み5バージョン、合計10バージョンのPostgreSQLをサポートするようになりました。PostgreSQL 15の時点では、`9.0`、`9.1`、`9.2`は対象外です。

  プルリクエスト [#1941](https://github.com/pgbackrest/pgbackrest/pull/1941); コミット [`77c721e`](https://github.com/pgbackrest/pgbackrest/commit/77c721eb635c6d757d2d5ed6f2ffc083720c10a7)
- 現在のPostgreSQLバージョンに一致するバックアップがない場合、リストアでエラーを返すようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Soulou。*)

  `stanza-upgrade`後に新しいバックアップがない場合、復元は以前のPostgreSQLバージョンで作成した最新バックアップを使用していました。この方法で構築したレプリカは失敗する可能性がありました。現在は、`set`または`type=time`/`type=lsn`を指定しない限り、この場合に復元をエラーとします。

  課題 [#1942](https://github.com/pgbackrest/pgbackrest/issues/1942); プルリクエスト [#1967](https://github.com/pgbackrest/pgbackrest/pull/1967); コミット [`b9be4fa`](https://github.com/pgbackrest/pgbackrest/commit/b9be4fa54039e2c79fad0dc1552c7ffaf883004c)
- `compress-type`ごとに`compress-level`の範囲チェックを追加しました。 (*レビュー：Stefan Fercot。提案：gkleen, ViperRu。*)

  `compress-level`の範囲はすべての`compress-type`で`0-9`でした。これは`gz`の範囲であり、`lz4`と`zst`で許される範囲の一部にすぎません。現在は、`zst`なら`-7`から`22`というように、形式ごとに範囲を設けています。

  課題 [#1216](https://github.com/pgbackrest/pgbackrest/issues/1216); 課題 [#1931](https://github.com/pgbackrest/pgbackrest/issues/1931); プルリクエスト [#1962](https://github.com/pgbackrest/pgbackrest/pull/1962); コミット [`44da314`](https://github.com/pgbackrest/pgbackrest/commit/44da314adb2b63f96b1d571f822e91a0e412e984)

**ドキュメントの改善：**

- Azureストレージで「階層型名前空間」を有効にする際の警告を追加しました。 (*レビュー：Stefan Fercot。提案：Vojtech Galda, Pluggi, asjonos。*)

  Azureで「階層型名前空間」を有効にすると、ディレクトリーの削除を別に行う必要があり、`expire`が失敗します。ユーザーガイドに、有効にしないよう注意を追加しました。

  課題 [#1770](https://github.com/pgbackrest/pgbackrest/issues/1770); プルリクエスト [#1980](https://github.com/pgbackrest/pgbackrest/pull/1980); コミット [`3aea997`](https://github.com/pgbackrest/pgbackrest/commit/3aea997df5ace85251d0579ccbe13fa938f587ee)
- 監視の例に改行を置換する処理を追加しました。 (*レビュー：Stefan Fercot。提案：rudonx, gmustdie, Ivan Shelestov。*)

  監視の例は、一部のエラーメッセージなど`info`出力に改行が含まれると、`COPY`が`\n`を`jsonb`の受け付けない改行文字へ変換するため失敗していました。現在は、`jsonb`へ変換する前に改行を置き換えます。

  課題 [#1910](https://github.com/pgbackrest/pgbackrest/issues/1910); プルリクエスト [#1963](https://github.com/pgbackrest/pgbackrest/pull/1963); コミット [`ae258f6`](https://github.com/pgbackrest/pgbackrest/commit/ae258f604e634f1d2a760ffdb92dd359fd1129bb)
- PostgreSQLの各バージョンにおける`target-action`の動作を明確にしました。 (*貢献：Chris Bandy。レビュー：David Steele, Anton Kurochkin, Stefan Fercot。提案：Anton Kurochkin, Chris Bandy。*)

  `pause`の動作は、`hot_standby`とPostgreSQLのバージョンに依存します。`hot_standby=off`の場合、`pause`はPostgreSQL >= 12では`shutdown`として、それ以前では`promote`として動作します。

  課題 [#987](https://github.com/pgbackrest/pgbackrest/issues/987); 課題 [#1314](https://github.com/pgbackrest/pgbackrest/issues/1314); プルリクエスト [#1960](https://github.com/pgbackrest/pgbackrest/pull/1960); コミット [`84a3ff8`](https://github.com/pgbackrest/pgbackrest/commit/84a3ff8b7ac1243c0b47c6585697f4fcf3c12065)
- トップページを更新し、説明を明確にしました。 (*レビュー：Stefan Fercot。*)

  他のバックアップ製品は並列処理をサポートしないという説明が正確でなくなったため、書き直しました。他のセクションも、現在の用語に合わせ、分かりやすく更新しました。

  プルリクエスト [#1966](https://github.com/pgbackrest/pgbackrest/pull/1966); コミット [`36ee30d`](https://github.com/pgbackrest/pgbackrest/commit/36ee30d118ce6cc7720653a3d3a49a06c655c463)
- ウェブサイトにダークモードを追加しました。 (*提案：Stephen Frost。*)

  ブラウザーがダーク配色を希望する場合、ウェブサイトで暗い配色を使うようにしました。

  コミット [`ed818b3`](https://github.com/pgbackrest/pgbackrest/commit/ed818b31867c640d72ef829dd36cd0a7feff12df)

### v2.43リリースノート {#v243-release-notes}

*不具合修正*

*2022年11月28日リリース*

**バグ修正：**

- 差分／増分バックアップで参照が欠落する問題を修正しました。 (*レビュー：Stefan Fercot。報告：Marcel Borger, ulfedf, jaymefSO。*)

  v2.42では、前回のバックアップが古いバージョンで作成されていると、差分・増分バックアップが"unable to find '...' in string list"で失敗していました。現在は、旧版のマニフェストから作成する参照一覧に、そのバックアップ自身のラベルも含めます。

  [`28f6604`](https://github.com/pgbackrest/pgbackrest/commit/28f660482aa5abb97850a9d7c89c2e5e9f23a4c9) info/manifestユニット内のmanifestBackupLabelSet()テストを移動しました。

  [`c4bf775`](https://github.com/pgbackrest/pgbackrest/commit/c4bf775099c85e3cd081f9c1ce35efd4c71d9161) 差分／増分バックアップで参照が欠落する問題を修正しました。; 課題 [#1933](https://github.com/pgbackrest/pgbackrest/issues/1933); プルリクエスト [#1935](https://github.com/pgbackrest/pgbackrest/pull/1935)

**改善：**

- インデックスを付けずにオプションを指定した場合のヒントを追加しました。 (*レビュー：Stefan Fercot。*)

  `repo-storage-ca-file`などインデックスが必要なオプションは、`repo1-storage-ca-file`のようにインデックス付きの名前を示すヒントとともにエラーを返すようになりました。非推奨オプションにも現在の名前を示すヒントを表示します。

  課題 [#1925](https://github.com/pgbackrest/pgbackrest/issues/1925); プルリクエスト [#1929](https://github.com/pgbackrest/pgbackrest/pull/1929); コミット [`3f363cb`](https://github.com/pgbackrest/pgbackrest/commit/3f363cb3aed1a7c6836ee6c32eae600129a6f6b8)

### v2.42リリースノート {#v242-release-notes}

*不具合修正*

*2022年11月22日リリース*

**バグ修正：**

- ファイルをバンドルする`backup`／`restore`のメモリリークを修正しました。 (*レビュー：John Morris。テスト：Oscar。報告：Oscar。*)

  復元処理は、バンドル内のすべてのファイルの復元が終わるまで、一部のI/Oオブジェクトを解放していませんでした。小さなファイルが多数あるバンドルではメモリー使用量が増え続け、"unable to allocate"で失敗していました。バックアップの再開にも、同種の小規模なリークがありました。

  課題 [#1877](https://github.com/pgbackrest/pgbackrest/issues/1877); プルリクエスト [#1878](https://github.com/pgbackrest/pgbackrest/pull/1878); コミット [`cd8db7d`](https://github.com/pgbackrest/pgbackrest/commit/cd8db7d9e53e041ad6fb31f2f015541c1d24abc2)
- リモートファイルの読み取り量が要求量に満たない場合のプロトコルエラーを修正しました。 (*レビュー：Stephen Frost。*)

  リモートファイルの読み取りが途中で終了・失敗すると、プロトコルが不正な状態で残っていました。次のコマンドは"client state is 'data-get' but expected 'idle'"で失敗し、元のエラーが失われていました。現在は、ファイルを閉じる際に残りを読み取ります。

  [`ea162e8`](https://github.com/pgbackrest/pgbackrest/commit/ea162e821634919b7c839e866b99bf82010dbacc) storage/remote/readモジュール内でstorageReadRemoteOpen()を移動しました。

  [`7967c75`](https://github.com/pgbackrest/pgbackrest/commit/7967c750d83466d030081e9deb1d70a1ba240271) リモートファイルの読み取り量が要求量に満たない場合のプロトコルエラーを修正しました。; プルリクエスト [#1900](https://github.com/pgbackrest/pgbackrest/pull/1900)

**改善：**

- バンドル時に長さゼロのファイルの参照を保存しないようにしました。 (*レビュー：Stefan Fercot。*)

  バンドル化した差分・増分バックアップは、どのバックアップにも保存されないサイズゼロのファイルに、以前のバックアップへの参照を格納していました。復元時には無視されますが、マニフェストの容量を使っていました。

  プルリクエスト [#1887](https://github.com/pgbackrest/pgbackrest/pull/1887); コミット [`f981fb4`](https://github.com/pgbackrest/pgbackrest/commit/f981fb45d9931e597afec764e13b1a53d8365d25)
- `pg_start_backup()`／`pg_stop_backup()`の説明をより一般的な表現にしました。 (*レビュー：Greg Sabino Mullane, David Christensen。提案：Greg Sabino Mullane。*)

  PostgreSQL 15で、これらの関数は`pg_backup_start()`/`pg_backup_stop()`に改名されました。ログとドキュメントには、PostgreSQLのバージョンに依存しない説明を使うようにしました。

  プルリクエスト [#1901](https://github.com/pgbackrest/pgbackrest/pull/1901); コミット [`ddd966c`](https://github.com/pgbackrest/pgbackrest/commit/ddd966cadc30440a81100144204d4084a0f2ac3a)

**テストスイートの改善：**

- `test.pl`の`--psql-bin`オプションをコマンドラインヘルプに合わせて更新しました。 (*貢献：Koshi Shibagaki。レビュー：David Steele。*)

  ヘルプには`--psql-bin`と表示されていましたが、オプション名は`--pgsql-bin`でした。現在はヘルプの表示どおりの名前にしました。

  プルリクエスト [#1920](https://github.com/pgbackrest/pgbackrest/pull/1920); コミット [`3ad5884`](https://github.com/pgbackrest/pgbackrest/commit/3ad588443b452e04f3abcc107e825dc47e078103)

### v2.41リリースノート {#v241-release-notes}

*バックアップの注釈*

*2022年9月19日リリース*

**バグ修正：**

- デフォルト以外のリポジトリで、時刻に基づく期限切れ処理が誤って適用される問題を修正しました。 (*レビュー：Stefan Fercot。報告：Adam Brusselback。*)

  `repo`を指定せずに`expire`を実行すると、すべてのリポジトリの時間ベース`repo-retention-full`を最小番号のリポジトリから読んでいました。現在は各リポジトリ自身の値を使います。

  課題 [#1852](https://github.com/pgbackrest/pgbackrest/issues/1852); プルリクエスト [#1854](https://github.com/pgbackrest/pgbackrest/pull/1854); コミット [`eda7f81`](https://github.com/pgbackrest/pgbackrest/commit/eda7f81ee4fd6818ce458768144fc3fc1e1f0f21)
- フィルターを指定してディレクトリを再帰的に一覧表示する際の問題を修正しました。 (*レビュー：Stephen Frost。報告：Efremov Egor。*)

  `recurse`と`filter`を指定した`repo-ls`では、ディレクトリーの最後の項目が内容のあるディレクトリーだと、二重解放やセグメンテーションフォールトで失敗する可能性がありました。子ディレクトリーの項目を処理する前に親の一覧を解放していました。

  課題 [#1870](https://github.com/pgbackrest/pgbackrest/issues/1870); プルリクエスト [#1871](https://github.com/pgbackrest/pgbackrest/pull/1871); コミット [`c39c9f2`](https://github.com/pgbackrest/pgbackrest/commit/c39c9f220ed328b4175d912e109697b726e9ea9b)

**新機能：**

- バックアップにキーと値の組による注釈を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Adam Berlin。*)

  `backup`コマンドの`annotation`オプションで、キーと値の組の注釈をバックアップに付けられます。後から新しい`annotate`コマンドで追加・変更・削除できます。`info`は、`set`指定時のテキスト出力に注釈を表示し、JSON出力には常に含めます。

  課題 [#1709](https://github.com/pgbackrest/pgbackrest/issues/1709); プルリクエスト [#1724](https://github.com/pgbackrest/pgbackrest/pull/1724); コミット [`381fd0a`](https://github.com/pgbackrest/pgbackrest/commit/381fd0a5a4de61624615b150ba98beeafac31f7e)

**改善：**

- `info`コマンドのJSON出力で`--set`に対応しました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Anton Kurochkin。*)

  `set`を指定した場合、`info`のJSON出力にも、エラー一覧やテーブルスペース一覧など、テキスト出力で表示していた詳細を含めるようにしました。

  課題 [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); プルリクエスト [#1501](https://github.com/pgbackrest/pgbackrest/pull/1501); コミット [`db75ffd`](https://github.com/pgbackrest/pgbackrest/commit/db75ffd27037d690a11eb02902f929250fe2bf5b)
- オブジェクトストアのアップロードチャンクサイズを設定できるようにしました。 (*レビュー：Stefan Fercot。提案：Anton Glushakov。*)

  S3、GCS、Azureへのアップロードのチャンクサイズを変えるには、`repo-storage-upload-chunk-size`を設定します。大きいチャンクは性能を改善する場合がありますが、メモリーも多く使います。デフォルト値は変更していません。

  [`ff1188f`](https://github.com/pgbackrest/pgbackrest/commit/ff1188f92dfc9e8f6d4aeca8b71a9886f24f58b4) コマンドラインヘルプでquoteタグを使用できるようにしました。

  [`b05d31f`](https://github.com/pgbackrest/pgbackrest/commit/b05d31f531b55b747175cf94c963f95574c54d2b) オブジェクトストアのアップロードチャンクサイズを設定できるようにしました。; 課題 [#1843](https://github.com/pgbackrest/pgbackrest/issues/1843); プルリクエスト [#1847](https://github.com/pgbackrest/pgbackrest/pull/1847)
- バックアップの成功後にarchive.infoのタイムスタンプを更新するようにしました。 (*レビュー：Stefan Fercot。提案：Alex Richman。*)

  `archive.info`とそのコピーは`stanza-create`と`stanza-upgrade`でしか書かれず、古いファイルを期限切れにするオブジェクトストアのライフサイクルポリシーで削除される可能性がありました。現在はバックアップ成功後に毎回タイムスタンプを更新します。

  課題 [#1853](https://github.com/pgbackrest/pgbackrest/issues/1853); プルリクエスト [#1855](https://github.com/pgbackrest/pgbackrest/pull/1855); コミット [`3b5df1e`](https://github.com/pgbackrest/pgbackrest/commit/3b5df1e089234d425dd225f8c1976755dc947c8a)
- スタンバイのタイムラインのチェックをチェックポイントの後に移動しました。 (*レビュー：Stefan Fercot。テスト：Keith Fiske。提案：Keith Fiske。*)

  スタンバイが期待したタイムライン上にあるかの確認に、バックアップ開始前の`pg_control`を使用していました。昇格直後には`pg_control`に新しいタイムラインがまだ書き込まれていないことがあり、"standby is on timeline ... but expected ..."で失敗していました。現在はチェックポイント後に確認します。

  課題 [#1816](https://github.com/pgbackrest/pgbackrest/issues/1816); プルリクエスト [#1819](https://github.com/pgbackrest/pgbackrest/pull/1819); コミット [`c267ba5`](https://github.com/pgbackrest/pgbackrest/commit/c267ba51b1778b5872f4ee928a9614545d743f3f)
- バックアップ再開時の警告メッセージを改善しました。 (*提案：Cynthia Shang。*)

  警告は、ユーザーに対応が必要と読める内容でした。現在は、無効なファイルを削除した後でバックアップを再開することを明示します。

  コミット [`cbbe93f`](https://github.com/pgbackrest/pgbackrest/commit/cbbe93f592d8097393c5ffe214f0a8c5fb0549c1)

**ドキュメントの改善：**

- `pgbackrest.service`内の`kill`に絶対パスを追加しました。 (*提案：Don Seiler。*)

  `pgbackrest.service`の例の`ExecReload`に`/bin/kill`を使用するようにしました。古いsystemdには絶対パスが必要です。

  コミット [`e9ff524`](https://github.com/pgbackrest/pgbackrest/commit/e9ff5248039eedb25da2fee550ec64fcebbc51c7)

### v2.40リリースノート {#v240-release-notes}

*OpenSSL 3のサポート*

*2022年7月18日リリース*

**パッケージ作成者への注意事項**：実験的なmesonビルドを追加しましたが、当面は引き続きautoconf/makeでビルドすることを推奨します。

**改善：**

- OpenSSL 3に対応しました。 (*レビュー：Stephen Frost。*)

  OpenSSL 3でpgBackRestをビルドできるようになりました。非推奨の警告を抑制し、OpenSSL 3が報告するエラーコードで予期しないEOFを検出します。

  プルリクエスト [#1767](https://github.com/pgbackrest/pgbackrest/pull/1767); コミット [`08242ee`](https://github.com/pgbackrest/pgbackrest/commit/08242ee6ac93b9eb9c05cc39e3db15bbafb9052c)
- パスの内容を一覧表示する際にスナップショットを作成するようにしました。 (*レビュー：John Morris, Stephen Frost。*)

  並べ替えずにパスを一覧取得する際、項目を処理しながら読み取っていました。一覧取得中に削除すると、一部のファイルシステムでは残っているファイルを飛ばし、パスを削除できなくなっていました。現在は常にパスのスナップショットから一覧を取得します。

  [`61ca9b5`](https://github.com/pgbackrest/pgbackrest/commit/61ca9b58a000aa8789ef3267682519bdb15e8a6b) テストのhrnStorageInfoListCallback()をTEST_STORAGE_LIST()に置き換えました。

  [`1c0bf0b`](https://github.com/pgbackrest/pgbackrest/commit/1c0bf0b15da8c0d15cc639851ff1d1bd05b51d06) リモートプロトコルのnullユーザー・グループ検査を並べ替え、テストを追加しました。

  [`72960bb`](https://github.com/pgbackrest/pgbackrest/commit/72960bbf179b4e8051bd4fc50be57d95159e9e13) strTrunc()をstrTruncIdx()に改名し、新しくstrTrunc()を追加しました。

  [`75623d4`](https://github.com/pgbackrest/pgbackrest/commit/75623d4583bfdaccb3a19b935fd04d744b363923) パスの内容を一覧表示する際にスナップショットを作成するようにしました。; 課題 [#1754](https://github.com/pgbackrest/pgbackrest/issues/1754); プルリクエスト [#1805](https://github.com/pgbackrest/pgbackrest/pull/1805)
- リストアで`type=immediate`を指定した場合に、`target-timeline=current`を強制するようにしました。 (*レビュー：Stephen Frost。*)

  PostgreSQL >= 12では、デフォルトの対象タイムラインは`latest`です。リポジトリ内の最新タイムラインにバックアップから到達できないと、リカバリが失敗することがありました。`type=immediate`の復元ではタイムラインを変更しないため、現在は対象を`current`に設定します。

  プルリクエスト [#1814](https://github.com/pgbackrest/pgbackrest/pull/1814); コミット [`364af16`](https://github.com/pgbackrest/pgbackrest/commit/364af1635d40431276cc6fd87d6ddd689b611e09)
- 差分`restore`で、ファイルが想定より大きい場合に切り詰めるようにしました。 (*レビュー：Stephen Frost。*)

  差分復元では、サイズがマニフェストと異なればリポジトリからファイルをコピーしていました。現在は、大きいファイルをマニフェストのサイズに切り詰め、チェックサムが一致しない場合だけコピーします。ログなど、追記しかされていないファイルはコピーしなくなりました。

  プルリクエスト [#1758](https://github.com/pgbackrest/pgbackrest/pull/1758); コミット [`7ec51e7`](https://github.com/pgbackrest/pgbackrest/commit/7ec51e7e6279ea576ad3b4b5c2ea1fc389d08ab5)
- `resume=n`の場合、マニフェストの増分保存を無効にしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  バックアップ中は再開用にマニフェストを定期保存します。`resume=n`の場合はこの保存を省略するようにしました。

  プルリクエスト [#1760](https://github.com/pgbackrest/pgbackrest/pull/1760); コミット [`60d70fa`](https://github.com/pgbackrest/pgbackrest/commit/60d70fa66fc3f709914f40dd088bac1b467001f2)
- コピー開始前にバックアップの進捗率をゼロに設定するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  実行中のバックアップの進捗を、最初のファイルのコピーが終わるまで報告していませんでした。現在はコピー開始時にゼロを設定します。

  プルリクエスト [#1759](https://github.com/pgbackrest/pgbackrest/pull/1759); コミット [`38ad283`](https://github.com/pgbackrest/pgbackrest/commit/38ad2838d553febae1b7fe0244d942dfaa9cf548)
- 一覧取得を続けるかどうかの判定にS3の`IsTruncated`フラグを使用するようにしました。 (*レビュー：John Morris。テスト：Soulou。提案：Christian Montagne。*)

  最近のScalityは、一覧が途中で切られていない場合に空の`NextContinuationToken`を返し、無限ループを引き起こしていました。現在は`IsTruncated`で続きの有無を判断し、途中で切られた一覧のトークンがないか空の場合はエラーにします。

  課題 [#1748](https://github.com/pgbackrest/pgbackrest/issues/1748); プルリクエスト [#1783](https://github.com/pgbackrest/pgbackrest/pull/1783); コミット [`845d82f`](https://github.com/pgbackrest/pgbackrest/commit/845d82f6825d4101e6a465a435ef056ff6ec15a2)

**ドキュメントの不具合修正：**

- 設定リファレンスに内部オプションを掲載しないようにしました。 (*報告：Francisco Miguel Biete Banon。*)

  一部のコマンドでのみ内部用となるオプションが、設定リファレンスに掲載されていました。コマンドラインヘルプには影響していません。

  コミット [`2643050`](https://github.com/pgbackrest/pgbackrest/commit/2643050be0dc4b7363c434f58373919bd6fdac68)

**ドキュメントの改善：**

- リポジトリホストのセクションにPostgreSQLの設定へのリンクを追加しました。 (*レビュー：Stefan Fercot。提案：Julien Cigar。*)

  プルリクエスト [#1809](https://github.com/pgbackrest/pgbackrest/pull/1809); コミット [`74a4ac8`](https://github.com/pgbackrest/pgbackrest/commit/74a4ac801db921f7b11b63b9f927228c6a6af861)

**テストスイートの改善：**

- 実験的なMesonビルドを追加しました。 (*レビュー：Eli Schwartz, Sam Bassaly。*)

  Mesonはautoconf/makeより構文が簡単で性能も良いため、コード生成とテストビルドに使用します。デバッグ以外のビルドはエラーにします。パッケージ作成者は引き続きautoconf/makeを使用してください。

  [`2feaaea`](https://github.com/pgbackrest/pgbackrest/commit/2feaaeaac803d6c0193477b56dbeb622fd991156) 他のCファイルにインクルードするCファイルに.inc拡張子を付けました。

  [`b8fc20d`](https://github.com/pgbackrest/pgbackrest/commit/b8fc20d5b8e7ca003ff39f29ea6e3ba57653f55c) 実験的なMesonビルドを追加しました。; プルリクエスト [#1765](https://github.com/pgbackrest/pgbackrest/pull/1765)

  [`665da12`](https://github.com/pgbackrest/pgbackrest/commit/665da12ae7f519077512e60ce3a5ec6c6a9997fd) meson.buildのincludeコメントをより一般的な記述にしました。

  [`9fd85a1`](https://github.com/pgbackrest/pgbackrest/commit/9fd85a104ad56061b028afd9057ce8c1d636d3dd) デバッグ以外のmesonビルドを無効にしました。

  [`59f148b`](https://github.com/pgbackrest/pgbackrest/commit/59f148bf6ea8c090d4d65ce5b135a71501e8ae22) __FILE__から相対パスを取り除く-fmacro-prefix-mapを生成するようにしました。

  [`0eccbc8`](https://github.com/pgbackrest/pgbackrest/commit/0eccbc8bf47073ab8ec1f13fed9865d0bd7c3635) Meson 0.45でビルドできます。
- `--test-path`オプションに任意のパスを渡せるようにしました。 (*貢献：Andrey Sokolov。レビュー：David Steele。*)

  プルリクエスト [#1764](https://github.com/pgbackrest/pgbackrest/pull/1764); コミット [`29b2a54`](https://github.com/pgbackrest/pgbackrest/commit/29b2a54fcc74457af5c63ffb505c5fbb24bb2ade)
- `DEBUG`を定義せずに`DEBUG_EXEC_TIME`を定義した場合のコンパイルエラーを修正しました。 (*貢献：Andrey Sokolov。レビュー：David Steele。*)

  `DEBUG`がない場合、開始時刻を使う`ASSERT()`が空に展開され、未使用変数によるコンパイルエラーになっていました。現在は`CHECK()`を使います。

  プルリクエスト [#1775](https://github.com/pgbackrest/pgbackrest/pull/1775); コミット [`1a00ab1`](https://github.com/pgbackrest/pgbackrest/commit/1a00ab10033e9ac6e6f797627567e8b91e143432)

### v2.39リリースノート {#v239-release-notes}

*検証とファイルのバンドル化*

*2022年5月16日リリース*

**バグ修正：**

- `FINALLY()`からエラーが送出されると無限ループになる問題を修正しました。 (*レビュー：Stephen Frost。*)

  `FINALLY()`ブロック内で投げられたエラーが同じブロックに戻り、再び同じエラーを投げて無限ループになる可能性がありました。現在は`FINALLY()`を1回だけ実行します。

  [`9a271e9`](https://github.com/pgbackrest/pgbackrest/commit/9a271e925c6239fbd3577f9827c34940e7e43ae4) `FINALLY()`からエラーが送出されると無限ループになる問題を修正しました。; プルリクエスト [#1732](https://github.com/pgbackrest/pgbackrest/pull/1732)

  [`ef4c4ab`](https://github.com/pgbackrest/pgbackrest/commit/ef4c4ab8525f81c9ed22c7e82ed12096e81703c5) FINALLY()の状態追跡に関数ではなく変数を使いました。; プルリクエスト [#1744](https://github.com/pgbackrest/pgbackrest/pull/1744)
- 他のプロセスがロックを保持している場合を除き、ロックの取得に失敗すると必ずエラーを返すようにしました。 (*レビュー：Reid Thompson。テスト：Geir Råness。報告：Geir Råness。*)

  権限など別の理由でロックを取得できなくても、`archive-get`/`archive-push`はエラーにせず、非同期プロセスも起動していませんでした。ユーザーには汎用的な失敗メッセージだけが返り、非同期ログもありませんでした。現在はこれらの失敗をエラーにします。

  課題 [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); プルリクエスト [#1730](https://github.com/pgbackrest/pgbackrest/pull/1730); コミット [`9629908`](https://github.com/pgbackrest/pgbackrest/commit/962990869454b15db058f4037dbc0b1b611fc95e)

**新機能：**

- 小さなファイルを効率的に扱えるよう、バックアップファイルのバンドル化を追加しました。 (*レビュー：Reid Thompson, Stefan Fercot, Chris Bandy。*)

  バンドル化は小さなファイルをリポジトリ内でまとめて保存し、特にファイル作成のコストが高いオブジェクトストアでバックアップの時間と容量を節約します。`repo-bundle`で有効にし、`repo-bundle-size`と`repo-bundle-limit`で調整します。復元では、バンドル内の隣接ファイルを1回で読み取ります。

  [`4d2fef1`](https://github.com/pgbackrest/pgbackrest/commit/4d2fef1c37d357965f0ffb9af0d7489f3be1371b) 冗長なrestoreFile()テストを削除し、カバレッジを改善しました。

  [`5141370`](https://github.com/pgbackrest/pgbackrest/commit/514137040e60e8fff0e7f42f43b493113abae5ff) ioCopyP()にlimitパラメーターを追加しました。

  [`dca6da8`](https://github.com/pgbackrest/pgbackrest/commit/dca6da86bfe84a0cda004df1140d125db1630c90) ファイルのバンドル化に合わせてrestoreコマンドを最適化しました。; 課題 [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); プルリクエスト [#1683](https://github.com/pgbackrest/pgbackrest/pull/1683)

  [`0054677`](https://github.com/pgbackrest/pgbackrest/commit/0054677147121967889ead7feab0959fb19e39a6) backupコマンドにバンドルのログ出力を追加しました。

  [`3f66f42`](https://github.com/pgbackrest/pgbackrest/commit/3f66f42ef9605a83c356e4c6eb3ef47bcb12c30d) bundle-*オプションをrepo-bundle-*へ改名しました。; プルリクエスト [#1694](https://github.com/pgbackrest/pgbackrest/pull/1694)

  [`fe9fd2f`](https://github.com/pgbackrest/pgbackrest/commit/fe9fd2ff2d778b86c0df159aabe7644f18f6479f) repo-bundleが有効な場合にrepo-hardlinkを無効にしました。

  [`424008d`](https://github.com/pgbackrest/pgbackrest/commit/424008d293661dfb1a167cfec2697def48057447) バックアップマニフェストの作成後にサイズゼロとなるファイルを許容しました。

  [`f405fc6`](https://github.com/pgbackrest/pgbackrest/commit/f405fc6ae281eebf4d61abb39963a9830fe2fa2f) バックアップのファイルバンドル化を文書化しました。; プルリクエスト [#1740](https://github.com/pgbackrest/pgbackrest/pull/1740)

  [v2.38](#v238-release-notes)での開発：

  [`a79034a`](https://github.com/pgbackrest/pgbackrest/commit/a79034ae2f6a8ec66b84c62ab6cd4042d2c1a249) すべてのストレージドライバーに読み取り範囲の指定を追加しました。; プルリクエスト [#1619](https://github.com/pgbackrest/pgbackrest/pull/1619)

  [`b791f1c`](https://github.com/pgbackrest/pgbackrest/commit/b791f1c82f53fa16866837d4544b58243c682f7f) マニフェスト内部を更新せずに、復元時の所有者設定を実装しました。

  [`f84909f`](https://github.com/pgbackrest/pgbackrest/commit/f84909f85f7dfb202ac812c67665cc590a5acad4) エラー後のPosix読み取りオフセット処理を修正しました。

  [`4ca0590`](https://github.com/pgbackrest/pgbackrest/commit/4ca0590a51a665535fbba903b8f55e10557b606a) backupProcessQueue()をリファクタリングし、BackupJobData構造体を使用しました。

  [`16559d9`](https://github.com/pgbackrest/pgbackrest/commit/16559d9e421c66596d21b047c8afe1b2c96ccd82) 適切な箇所でPG_FILE_POSTMTRPID定数を使用しました。

  [`8c062e1`](https://github.com/pgbackrest/pgbackrest/commit/8c062e1af824c3dc80ff94b3df8d433f95e88d0f) マニフェストからprimaryフラグを削除しました。; プルリクエスト [#1630](https://github.com/pgbackrest/pgbackrest/pull/1630)

  [`b0db4b8`](https://github.com/pgbackrest/pgbackrest/commit/b0db4b8ff00db913cb69308017a56155d6070830) mock/all結合テストのベースパスモードを簡素化しました。

  [`4a73a02`](https://github.com/pgbackrest/pgbackrest/commit/4a73a0286387f3f2185f3f193f9c20ed0d7d926d) マニフェストのデフォルト値を簡素化しました。; プルリクエスト [#1631](https://github.com/pgbackrest/pgbackrest/pull/1631)

  [`575ae77`](https://github.com/pgbackrest/pgbackrest/commit/575ae77c0dee12b932469d479b2e45dbaf389737) マニフェスト内で、可能な箇所のvarNewUInt64()をVARUINT64()に置き換えました。

  [`61ce586`](https://github.com/pgbackrest/pgbackrest/commit/61ce58692f3092b72833b6e9ee87037f45b3b702) メモリー節約のため、マニフェストのファイル構造体を詰めて配置しました。; プルリクエスト [#1626](https://github.com/pgbackrest/pgbackrest/pull/1626)

  [`ca13f11`](https://github.com/pgbackrest/pgbackrest/commit/ca13f11b4a3858587c7055b0b2b4a8b396dd8451) jsonFromStrInternal()を最適化しました。

  [`e4df5b7`](https://github.com/pgbackrest/pgbackrest/commit/e4df5b7d3846134832b9315e22786f679d63a46b) マニフェストのファイルデフォルト値を簡素化しました。; プルリクエスト [#1632](https://github.com/pgbackrest/pgbackrest/pull/1632)

  [`7dd657b`](https://github.com/pgbackrest/pgbackrest/commit/7dd657b7dd163ded9fbf7caef37eea7e08bc5a37) command/verifyモジュールのファイル名構築を簡素化しました。

  [`34d6495`](https://github.com/pgbackrest/pgbackrest/commit/34d649579eb3bd1530aa99f0ed1879e7d3125424) バックアップ中にリポジトリ内のファイルをバンドル化しました。; 課題 [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); プルリクエスト [#1655](https://github.com/pgbackrest/pgbackrest/pull/1655)

  [`efc09db`](https://github.com/pgbackrest/pgbackrest/commit/efc09db7b9ece6e7b7f92538d56d6ab7b9798f8f) バンドル化できるファイルを制限しました。; 課題 [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); プルリクエスト [#1662](https://github.com/pgbackrest/pgbackrest/pull/1662)

  [`e6e1122`](https://github.com/pgbackrest/pgbackrest/commit/e6e1122dbcf5e667d683295f7e7e45de4bbf56bd) manifestFileAdd()でファイルを参照渡しにしました。
- リポジトリの内容を検証するverifyコマンドを追加しました。 (*貢献：Cynthia Shang, Reid Thompson。レビュー：David Steele, Stefan Fercot。*)

  `verify`コマンドは、リポジトリ内のバックアップとWALが有効か確認します。結果を出力するには`output=text`を、エラーだけでなく検証に成功した項目も含めるには`verbose`を設定します。

  プルリクエスト [#1607](https://github.com/pgbackrest/pgbackrest/pull/1607); コミット [`65d22e4`](https://github.com/pgbackrest/pgbackrest/commit/65d22e43257d46ff6523ffbdb3af59e30deeaea5)
- PostgreSQL 15に対応しました。 (*レビュー：Stefan Fercot。*)

  PostgreSQL 15は排他的バックアップを削除し、バックアップ開始・終了関数を改名し、pgBackRestが使わなくなった`pg_database.datlastsysoid`を削除します。

  [`692fe49`](https://github.com/pgbackrest/pgbackrest/commit/692fe496bdb5fa6dcffeb9f85b6188ceb1df707a) pg_database.datlastsysoidへの依存を削除しました。; プルリクエスト [#1735](https://github.com/pgbackrest/pgbackrest/pull/1735)

  [`20782c8`](https://github.com/pgbackrest/pgbackrest/commit/20782c88bc8d0842d547bd5f4fecdb292e69d1f7) PostgreSQL 15に対応しました。; プルリクエスト [#1736](https://github.com/pgbackrest/pgbackrest/pull/1736)
- `info`の出力にバックアップの進捗率を表示するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  `info`は、バックアップを実行しているホストで、その完了率を表示します。JSON出力では、パーセント値を100倍した整数で報告します。

  [`d9088b2`](https://github.com/pgbackrest/pgbackrest/commit/d9088b2e2b16a89d29b967187a547976f96061fc) `info`の出力にバックアップの進捗率を表示するようにしました。; 課題 [#1490](https://github.com/pgbackrest/pgbackrest/issues/1490); プルリクエスト [#1621](https://github.com/pgbackrest/pgbackrest/pull/1621)

  [`a6b1adb`](https://github.com/pgbackrest/pgbackrest/commit/a6b1adb5fd533b4b9aca29646c8acf647d872959) ロックファイル書き込み時の余分な改行を削除しました。

  [v2.38](#v238-release-notes)での開発：

  [`22734eb`](https://github.com/pgbackrest/pgbackrest/commit/22734eb376b3183924cb7794f9111c1eeb5d92d6) ioBufferReadNewOpen()とioBufferWriteNewOpen()を追加しました。

  [`9b2f10d`](https://github.com/pgbackrest/pgbackrest/commit/9b2f10dbb49a8b869cef2c419d9957ed4c550016) ロックのコードをリファクタリングしました。; プルリクエスト [#1643](https://github.com/pgbackrest/pgbackrest/pull/1643)
- `restore`コマンドの`--type=lsn`でバックアップを自動選択するようにしました。 (*貢献：Reid Thompson。レビュー：Stefan Fercot, David Steele。*)

  `type=lsn`では、`target`のLSN以前に終了した最新のバックアップを選択するようになりました。

  [`08d9e26`](https://github.com/pgbackrest/pgbackrest/commit/08d9e269c6f03e7797584e90c53eb0743b787f60) restoreモジュールの対象タイプ検査を、分かりやすくリファクタリングしました。

  [`d8d4132`](https://github.com/pgbackrest/pgbackrest/commit/d8d4132118edd7f93a5b221478c85c2d213c39dd) `restore`コマンドの`--type=lsn`でバックアップを自動選択するようにしました。; プルリクエスト [#1706](https://github.com/pgbackrest/pgbackrest/pull/1706)

  [`ea4d73f`](https://github.com/pgbackrest/pgbackrest/commit/ea4d73f375558c237fce696f20c19d1efef00bc1) command/restoreユニットテストでbackup-lsn-stopフィールドの順序を修正しました。
- `archive-mode-check`が無効な場合、既存のWALに関する警告を抑止するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  `archive-mode-check=n`で複数ホストからWALを転送する場合、同じチェックサムのWALがすでにアーカイブに存在するのは想定内なので、警告を出さなくなりました。チェックサムが異なる場合は引き続きエラーです。

  プルリクエスト [#1711](https://github.com/pgbackrest/pgbackrest/pull/1711); コミット [`aad7171`](https://github.com/pgbackrest/pgbackrest/commit/aad7171940afdb221a03825bee6eb2f1827289f1)
- AWS IMDSv2のサポートを追加しました。 (*貢献：Nuno Pires。レビュー：David Steele。*)

  IMDSv2は、`repo-s3-key-type=auto`へ認証情報を提供するインスタンスメタデータを保護します。IMDSv2のトークンリクエストに失敗すると、pgBackRestはIMDSv1にフォールバックします。

  課題 [#1685](https://github.com/pgbackrest/pgbackrest/issues/1685); プルリクエスト [#1691](https://github.com/pgbackrest/pgbackrest/pull/1691); コミット [`21cef09`](https://github.com/pgbackrest/pgbackrest/commit/21cef09dfd03c313531dc66ba9556164ae2835ab)

**改善：**

- フルバックアップの後で`repo-hardlink`オプションを変更できるようにしました。 (*レビュー：Reid Thompson。*)

  `repo-hardlink`を変更するには新しいフルバックアップが必要でした。現在は、ファイルバンドル化のために無効にする場合など、いつでも変更できます。

  プルリクエスト [#1699](https://github.com/pgbackrest/pgbackrest/pull/1699); コミット [`7afaac0`](https://github.com/pgbackrest/pgbackrest/commit/7afaac0a3d0e43e5598d1abf548559dbe6329363)
- `backup`と`restore`の進捗率のログの精度を上げました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  完了率を小数第2位までログ出力するようにし、大規模なバックアップや復元で更新頻度を高めました。

  プルリクエスト [#1679](https://github.com/pgbackrest/pgbackrest/pull/1679); コミット [`330e199`](https://github.com/pgbackrest/pgbackrest/commit/330e19900ee3415d920680cf6e6856bf5e8e9a69)
- `repo-*`コマンドのパス検証を改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  パスに`//`を含めることはできず、末尾の`/`は削除します。絶対パスはリポジトリのパス内にある必要があります。

  [`5ae84d5`](https://github.com/pgbackrest/pgbackrest/commit/5ae84d5e474e95dcc00c174aa5111815a5a70ba5) `repo-*`コマンドのパス検証を改善しました。; プルリクエスト [#1697](https://github.com/pgbackrest/pgbackrest/pull/1697)

  [`19dd015`](https://github.com/pgbackrest/pgbackrest/commit/19dd015d589ed3efd31a2a238249a150fb3748c1) repo-*コマンドの改善したパス検証の問題を修正しました。; プルリクエスト [#1751](https://github.com/pgbackrest/pgbackrest/pull/1751)
- `stop`コマンドが`stanza`オプションに従うように改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：ragaoua。*)

  `force`と`stanza`を指定した`stop`は、そのスタンザのロックを保持するプロセスだけを終了するようになりました。以前はすべてのスタンザのプロセスを終了していました。

  課題 [#1608](https://github.com/pgbackrest/pgbackrest/issues/1608); プルリクエスト [#1676](https://github.com/pgbackrest/pgbackrest/pull/1676); コミット [`f7ab002`](https://github.com/pgbackrest/pgbackrest/commit/f7ab002aa74dd2ca277123f7500018ae68a04c74)
- `repo-azure-key`が無効な場合のエラーメッセージを改善しました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Seth Daniel。*)

  `repo-azure-key-type=shared`では、`repo-azure-key`が有効なbase64か確認するようになりました。

  課題 [#1686](https://github.com/pgbackrest/pgbackrest/issues/1686); プルリクエスト [#1688](https://github.com/pgbackrest/pgbackrest/pull/1688); コミット [`7c9208b`](https://github.com/pgbackrest/pgbackrest/commit/7c9208ba856a71833dc7d8f1cf8cb2b4bb4b7414)
- 非同期の`archive-get`／`archive-push`でエラーが発生した場合に、ログを確認するよう促すヒントを追加しました。 (*レビュー：Reid Thompson。*)

  非同期プロセスが状態ファイルを書けない場合、`archive-get`/`archive-push`は汎用的なエラーでタイムアウトします。現在は、実際のエラーを含む非同期ログのパスを、ヒントとして表示します。

  課題 [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); コミット [`03c71aa`](https://github.com/pgbackrest/pgbackrest/commit/03c71aa606bc0dc89303b3907e7fcbd83ace79d6)
- 予期しないクロックスキューやタイムゾーンの変更に対して`ClockError`を追加しました。 (*レビュー：Greg Sabino Mullane, Stefan Fercot。提案：Greg Sabino Mullane。*)

  プルリクエスト [#1739](https://github.com/pgbackrest/pgbackrest/pull/1739); コミット [`5f8c9cd`](https://github.com/pgbackrest/pgbackrest/commit/5f8c9cd66a1b39a47acaddfbc3cf443ae8057519)
- 履歴マニフェストをエラーメッセージに表示する前に、拡張子を取り除くようにしました。 (*レビュー：Stefan Fercot。*)

  新しいバックアップラベルが履歴内の最新ラベルより後でない場合、エラーには`20220504-222042F_20220504-222141I.manifest.gz`のような履歴マニフェスト名を表示していました。現在はラベルだけを表示します。

  プルリクエスト [#1738](https://github.com/pgbackrest/pgbackrest/pull/1738); コミット [`b6bfd9f`](https://github.com/pgbackrest/pgbackrest/commit/b6bfd9f99d74b1f5e631cf6462b68342589d2b80)
- ロックの権限エラーにuser:groupを追加しました。 (*レビュー：Reid Thompson。*)

  課題 [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); コミット [`0055fa4`](https://github.com/pgbackrest/pgbackrest/commit/0055fa40fee2636fed88699f52e9e67cd2803f71)
- プライマリークラスターを見つけられない場合のヒントを追加しました。

  "unable to find primary cluster"エラーに、利用可能なすべてのクラスターがリカバリ中ではないかを確認するヒントを追加しました。

  コミット [`46b7b72`](https://github.com/pgbackrest/pgbackrest/commit/46b7b7287446d0bb5ed0963fd01c51fb2b08893f)

**ドキュメントの不具合修正：**

- ユーザーガイドの`stanza-update`への誤った参照を修正しました。 (*修正：Abubakar Mohammed。レビュー：David Steele。*)

  コミット [`3dd7960`](https://github.com/pgbackrest/pgbackrest/commit/3dd796045160c4d4dbf70ec2800ad483867629f1)
- 設定リファレンスの`repo-gcs-key-type`オプションの例を修正しました。 (*レビュー：Reid Thompson。*)

  例に使っていた`none`は無効な値でした。現在は`auto`にしています。

  コミット [`166039c`](https://github.com/pgbackrest/pgbackrest/commit/166039c0da1875581a08d41ab8a44adf95fa6db1)
- `tls-server-auth`の例を修正し、説明を補いました。 (*レビュー：Reid Thompson。*)

  例にクライアントCNが欠けていたため、`client-cn=stanza1`に修正しました。ヘルプにも、クライアントCNでワイルドカードを使えないことを明記しました。

  コミット [`c222ce1`](https://github.com/pgbackrest/pgbackrest/commit/c222ce1a5f6f813188b7e87a3838d6dce656e0ff)

**ドキュメントの改善：**

- ドキュメント内のサポート対象バージョンに関する説明を簡潔にしました。 (*レビュー：Stefan Fercot, Reid Thompson, Greg Sabino Mullane。*)

  ユーザーガイドはPostgreSQLのバージョン範囲を示していたため、RHEL上のPostgreSQL 12など、範囲外のバージョンが未対応に見えていました。範囲を削除し、導入部でガイドが扱うバージョンを説明するようにしました。

  プルリクエスト [#1742](https://github.com/pgbackrest/pgbackrest/pull/1742); コミット [`eefa0b1`](https://github.com/pgbackrest/pgbackrest/commit/eefa0b161a6a02b7843e18455443a4bce41cd4b9)
- オプションの型の説明を追加しました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  設定リファレンスでは、サイズオプションの単位など各オプション型の説明を、個別のオプションで繰り返す代わりに型ごとに説明するようにしました。

  プルリクエスト [#1747](https://github.com/pgbackrest/pgbackrest/pull/1747); コミット [`a913113`](https://github.com/pgbackrest/pgbackrest/commit/a913113fda5886ffd2ff136cdd52a3f469eca026)
- バックアップの種類とリストア速度に関するFAQを追加しました。 (*貢献：David Christensen。レビュー：Reid Thompson。*)

  新しいFAQで、バックアップの種類が影響するのはバックアップ処理だけで、復元速度には影響しないことを説明しています。

  プルリクエスト [#1731](https://github.com/pgbackrest/pgbackrest/pull/1731); コミット [`50d409a`](https://github.com/pgbackrest/pgbackrest/commit/50d409a812be577f2c296f3d6096cf97fab049ff)
- プルリクエストで必須となるベースブランチを明記しました。 (*貢献：David Christensen。レビュー：Reid Thompson。*)

  貢献ガイドに、プルリクエストは`integration`ブランチを基にする必要があると明記しました。

  プルリクエスト [#1733](https://github.com/pgbackrest/pgbackrest/pull/1733); コミット [`cc5b061`](https://github.com/pgbackrest/pgbackrest/commit/cc5b0614894e1b5ef78f1ceba3bc8e4760a40a24)

### v2.38リリースノート {#v238-release-notes}

*軽微なバグ修正と改善*

*2022年3月6日リリース*

**重要な注意事項**：`info`コマンドが報告するリポジトリサイズは、pgBackRestがストレージに書き込んだ量だけに基づくようになりました。以前は、ストレージで追加の圧縮が行われているかどうかを検出できる場合がありましたが、この機能はサポートされなくなりました。

**バグ修正：**

- S3でファイルを一括削除する際のエラーで再試行するようにしました。 (*レビュー：Reid Thompson。報告：Alex Richman。*)

  バッチ削除自体の失敗は再試行していましたが、バッチ内の個々のファイルのエラーは再試行しておらず、期限切れ処理や再開不能なバックアップの削除中にpgBackRestが終了する可能性がありました。現在は、失敗したファイルを通常のHTTP再試行付きで個別に削除します。

  課題 [#1650](https://github.com/pgbackrest/pgbackrest/issues/1650); プルリクエスト [#1653](https://github.com/pgbackrest/pgbackrest/pull/1653); コミット [`551e5bc`](https://github.com/pgbackrest/pgbackrest/commit/551e5bc6f67c91cf1e11da0cefe24f9650353adc)
- HTTPの`connection`ヘッダーの値を、大文字と小文字を区別せずに照合できるようにしました。 (*レビュー：Reid Thompson。報告：Rémi Vidier。*)

  HTTP仕様では、`connection`ヘッダーの値は`Close`のように大文字・小文字を任意にできます。

  課題 [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); プルリクエスト [#1675](https://github.com/pgbackrest/pgbackrest/pull/1675); コミット [`b33cabe`](https://github.com/pgbackrest/pgbackrest/commit/b33cabe08c33e29eb8aef65dd46b2c1f3cf2d186)

**新機能：**

- KMSを使用したAWS S3のサーバー側暗号化のサポートを追加しました。 (*貢献：Christoph Berg。レビュー：David Steele。テスト：Tharindu Amila。*)

  AWS KMSが管理するキーでオブジェクトを暗号化するには、`repo-s3-kms-key-id`を設定します。

  課題 [#1430](https://github.com/pgbackrest/pgbackrest/issues/1430); プルリクエスト [#1567](https://github.com/pgbackrest/pgbackrest/pull/1567); コミット [`3097acd`](https://github.com/pgbackrest/pgbackrest/commit/3097acd73a21b630aa5352be57a82b031930f96b)
- `archive-missing-retry`オプションを追加しました。 (*レビュー：Stefan Fercot。*)

  デフォルトの`archive-get`は、以前の復元がスプールパスに残した欠落通知を無視するため、欠落と報告済みのWALセグメントを再試行します。`archive-missing-retry=n`では、WALのアーカイブ中でもPostgreSQLがアーカイブの終端を検出し、ストリーミングに切り替えられます。この場合、リカバリ開始時にスプールパスを空にする必要があります。

  プルリクエスト [#1642](https://github.com/pgbackrest/pgbackrest/pull/1642); コミット [`10038db`](https://github.com/pgbackrest/pgbackrest/commit/10038db9c9f2b4753c3821e0b246fa8626527184)
- `info`コマンドにバックアップの種類によるフィルターを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  `type=full`のように`type`を設定すると、その種類のバックアップだけを表示します。

  課題 [#600](https://github.com/pgbackrest/pgbackrest/issues/600); プルリクエスト [#1651](https://github.com/pgbackrest/pgbackrest/pull/1651); コミット [`b26097f`](https://github.com/pgbackrest/pgbackrest/commit/b26097f8d8a7e2af6e9a21576994cbb47110c6f4)

**改善：**

- `backup`中にページ検証に失敗した場合に再試行するようにしました。 (*レビュー：Stephen Frost, David Christensen。*)

  チェックサム検証に失敗したページを再読み取りし、内容が変わっていない場合にだけエラーとして報告するようにしました。変化したページはPostgreSQLが書き込み中で、WALにページ全体のイメージが含まれます。ゼロページは`pd_upper`だけでなく、全体がゼロか確認するようにしました。

  [`b489707`](https://github.com/pgbackrest/pgbackrest/commit/b4897077937ee4571ba719276a44d5db0a75510e) command/backup-commonのテストをcommand/backupモジュールへ移しました。

  [`9eec98c`](https://github.com/pgbackrest/pgbackrest/commit/9eec98c61302121134d2067326dbd2cd0f2f0b9c) バックアップ中のページチェックサム検証失敗時に再試行するようにしました。; 課題 [#952](https://github.com/pgbackrest/pgbackrest/issues/952); プルリクエスト [#1667](https://github.com/pgbackrest/pgbackrest/pull/1667)

  [`53f1b25`](https://github.com/pgbackrest/pgbackrest/commit/53f1b2520434221c01caf92e052403a28c455c1b) ゼロページの検証を改善しました。; 課題 [#952](https://github.com/pgbackrest/pgbackrest/issues/952); プルリクエスト [#1669](https://github.com/pgbackrest/pgbackrest/pull/1669)
- 接続を正常に終了しないTLSサーバーに対応しました。 (*レビュー：David Christensen, Stephen Frost。テスト：Rémi Vidier。*)

  一部のサーバーはTLS接続ではなくソケットを閉じます。応答にcontent lengthもchunked encodingもなく、その内容を解析できる場合は、閉じたソケットをEOFとして扱うようにしました。これらのサーバーはv2.35から動作しなくなっていました。

  課題 [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); プルリクエスト [#1677](https://github.com/pgbackrest/pgbackrest/pull/1677); コミット [`59a5373`](https://github.com/pgbackrest/pgbackrest/commit/59a5373cf85e4ad0057b592bfe855495384dfcbd)
- `info`コマンドの出力にバックアップのLSNを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  LSNを使った特定時点へのリカバリに利用できるよう、`set`指定時とJSON出力でバックアップの開始・終了LSNを表示します。

  プルリクエスト [#1610](https://github.com/pgbackrest/pgbackrest/pull/1610); コミット [`d866dd5`](https://github.com/pgbackrest/pgbackrest/commit/d866dd5c297dc046581134a108032cf9694cae0e)
- `repo-ls`のパスの末尾のスラッシュを自動的に取り除くようにしました。 (*貢献：David Christensen。レビュー：David Steele。*)

  パス末尾のスラッシュにより、一部のリポジトリストレージ形式で`repo-ls`が内容を表示しませんでした。

  プルリクエスト [#1673](https://github.com/pgbackrest/pgbackrest/pull/1673); コミット [`6320712`](https://github.com/pgbackrest/pgbackrest/commit/632071232344a1160ef932d6e0d65eb3149ed226)
- 致命的なエラーでは再試行しないようにしました。 (*レビュー：Reid Thompson。*)

  致命的エラー、特にメモリー不足の再試行は、処理停止を引き起こす可能性があります。アサーションとメモリーのエラーは、再試行せず報告するようにしました。

  [`8573a2d`](https://github.com/pgbackrest/pgbackrest/commit/8573a2df14d0bfd5578333b68147cc12c93c6f96) protocolClientFree()のプロトコルモジュールエラーテストを改善しました。

  [`8d0cce6`](https://github.com/pgbackrest/pgbackrest/commit/8d0cce66f83abc1ff02a985ec3f0d7e285c09d72) プロトコルモジュールのエラー再試行テストに通常のエラーを使いました。

  [`8046f06`](https://github.com/pgbackrest/pgbackrest/commit/8046f0630715015d5adcced570c54e9a183c0e73) 致命的なエラーでは再試行しないようにしました。; プルリクエスト [#1658](https://github.com/pgbackrest/pgbackrest/pull/1658)
- PostgreSQL `8.3`／`8.4`のサポートを終了しました。 (*レビュー：Reid Thompson, Stefan Fercot。*)

  これらのバージョンがまだ使われている証拠はなく、サポートには開発とテストの時間がかかります。これらのバージョンのバックアップや移行には、古いpgBackRestを使用してください。

  プルリクエスト [#1611](https://github.com/pgbackrest/pgbackrest/pull/1611); コミット [`bb4b30d`](https://github.com/pgbackrest/pgbackrest/commit/bb4b30ddd3f80c246c565eb4769efc82b9509648)
- ファイルシステムによる追加の圧縮を判定するロジックを削除しました。 (*レビュー：Reid Thompson, Stefan Fercot。*)

  ファイルのコピー後、ZFSなどファイルシステムによる圧縮を検出するため、ディスク上のサイズを確認していました。この処理はテストされておらず、小さいファイルが多いと遅くなり、バンドル化の妨げにもなっていました。現在は、`info`のリポジトリサイズにpgBackRestが書き込んだ量を示します。

  プルリクエスト [#1652](https://github.com/pgbackrest/pgbackrest/pull/1652); コミット [`cb630ff`](https://github.com/pgbackrest/pgbackrest/commit/cb630ffe3b5c819b5e97ac11d5974000bd44d632)

**ドキュメントの不具合修正：**

- TLSのドキュメントで、`repo`オプションを`global`セクションに移動しました。 (*報告：Anton Kurochkin。*)

  ユーザーガイドはこれらのオプションをスタンザセクションに設定していました。一部の場合には動作しますが、推奨される方法ではありません。

  コミット [`53de3e3`](https://github.com/pgbackrest/pgbackrest/commit/53de3e3aeb71f8209f56167941df35bbfcb7cdc9)
- stanzaコマンドから未使用の`backup-standby`オプションを削除しました。 (*報告：Stefan Fercot。*)

  `stanza-create`と`stanza-upgrade`は、使わない`backup-standby`をコマンドリファレンスとヘルプに掲載していました。

  コミット [`5cbb4a3`](https://github.com/pgbackrest/pgbackrest/commit/5cbb4a3e6b13598b90cae46fad28c31604f9f094)
- ヘルプとリリースノートの誤記を修正しました。 (*修正：Daniel Gustafsson。レビュー：David Steele。*)

  [`cacfdd9`](https://github.com/pgbackrest/pgbackrest/commit/cacfdd94d74307285b1b590ec0977d7db3142d0d) ヘルプとリリースノートの誤記を修正しました。; プルリクエスト [#1671](https://github.com/pgbackrest/pgbackrest/pull/1671)

  [`5c332a0`](https://github.com/pgbackrest/pgbackrest/commit/5c332a0b100d5a5180b3d95bd90d4d7b521b42db) cacfdd94とf798458eのリリースノートの貢献者表記を修正しました。

**ドキュメントの改善：**

- systemdサービスの設定に死活監視を追加しました。 (*提案：Yogesh Sharma。*)

  `pgbackrest.service`の例で、起動直後にサーバーが動作し続けているか確認するようにしました。以前は、起動に失敗してもsystemdが裏で再試行し、エラーを報告していませんでした。

  コミット [`f1bdf3e`](https://github.com/pgbackrest/pgbackrest/commit/f1bdf3e04b07dc9a2eaa1fdbe5278cc18371e868)
- WALアーカイブの接尾辞について説明するFAQを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  リポジトリ内のWALファイルの接尾辞は、ファイル検証に使用するSHA1チェックサムです。省略できません。

  課題 [#1485](https://github.com/pgbackrest/pgbackrest/issues/1485); 課題 [#1663](https://github.com/pgbackrest/pgbackrest/issues/1663); プルリクエスト [#1664](https://github.com/pgbackrest/pgbackrest/pull/1664); コミット [`98d525d`](https://github.com/pgbackrest/pgbackrest/commit/98d525dba43ba259ff7989746b8e5be3382c189d)
- レプリケーションスロットはリストアされないことを明記しました。 (*貢献：Reid Thompson。レビュー：David Steele, Stefan Fercot。提案：Christophe Courtois。*)

  課題 [#1585](https://github.com/pgbackrest/pgbackrest/issues/1585); プルリクエスト [#1601](https://github.com/pgbackrest/pgbackrest/pull/1601); コミット [`a82f017`](https://github.com/pgbackrest/pgbackrest/commit/a82f0179cdd5742e5c5b1e0bdfd23166753fdb38)

### v2.37リリースノート {#v237-release-notes}

*TLSサーバー*

*2022年1月3日リリース*

**重要な注意事項**：`restore`コマンドで、指定した目標時刻に合うバックアップが見つからない場合、従来は警告をログに記録していましたが、エラーを返すようになりました。

**バグ修正：**

- パスやファイルがすでに存在する場合の、差分`restore`でのリンクのマッピングを修正しました。 (*レビュー：Reid Thompson。報告：Younes Alhroub。*)

  `link-map`や`link-all`で既存のパスやファイルをリンクにマッピングしても、差分復元は既存のものを残していました。現在はリンクに置き換えます。

  課題 [#1588](https://github.com/pgbackrest/pgbackrest/issues/1588); プルリクエスト [#1589](https://github.com/pgbackrest/pgbackrest/pull/1589); コミット [`a73fe4e`](https://github.com/pgbackrest/pgbackrest/commit/a73fe4eb966f9685f6e4179c397a10c1e7f15f19)
- 接続の再試行時にソケットがリークする問題を修正しました。 (*レビュー：Reid Thompson。報告：James Coleman。*)

  最適化ビルドでは、接続試行に失敗したソケットを閉じず、再試行ごとにソケットがリークしていました。

  課題 [#1593](https://github.com/pgbackrest/pgbackrest/issues/1593); プルリクエスト [#1594](https://github.com/pgbackrest/pgbackrest/pull/1594); コミット [`615bdff`](https://github.com/pgbackrest/pgbackrest/commit/615bdff4030a31bfedfe7df04676e3948ec9c2c0)

**新機能：**

- TLSサーバーを追加しました。 (*レビュー：Stephen Frost, Reid Thompson。テスト：Andrew L'Ecuyer。*)

  `server`コマンドは、リポジトリホストやPostgreSQLホストへのアクセスにSSHの代わりに使えるTLSサーバーを起動します。クライアントに`repo-host-type=tls`または`pg-host-type=tls`を設定し、`tls-server-*`で証明書とクライアント認可を設定します。`SIGHUP`で設定を再読み込みし、`SIGTERM`でサーバーを停止します。

  [`2d963ce`](https://github.com/pgbackrest/pgbackrest/commit/2d963ce9471808172f879916c3f3accc35f14d56) server-startコマンドをserverに改名しました。

  [`7b3ea88`](https://github.com/pgbackrest/pgbackrest/commit/7b3ea883c7c010aafbeb14d150d073a113b703e4) TLSサーバーにSIGTERMとSIGHUPの処理を追加しました。; プルリクエスト [#1572](https://github.com/pgbackrest/pgbackrest/pull/1572)

  [`f06101d`](https://github.com/pgbackrest/pgbackrest/commit/f06101de77a980c7e4115762f2fc301280aa4127) TLSサーバーのドキュメントを追加しました。; プルリクエスト [#1597](https://github.com/pgbackrest/pgbackrest/pull/1597)

  [v2.36](#v236-release-notes)での開発：

  [`ccc255d`](https://github.com/pgbackrest/pgbackrest/commit/ccc255d3e05d8ce2b6ac251d1498f71b04098a86) TLSサーバーを追加しました。; プルリクエスト [#1504](https://github.com/pgbackrest/pgbackrest/pull/1504)

  [`13d4559`](https://github.com/pgbackrest/pgbackrest/commit/13d4559708819787ad05be6f37ec0badb0eccae5) getsockopt()の戻り値を確認しました。

  [v2.35](#v235-release-notes)での開発：

  [`947c7a8`](https://github.com/pgbackrest/pgbackrest/commit/947c7a84cb37d09ab925785ca7670c970e32b8a3) cmdLocal()/cmdRemote()がProtocolServerオブジェクトを受け取るようリファクタリングしました。

  [`0999de0`](https://github.com/pgbackrest/pgbackrest/commit/0999de0279fabf35af80396a9a8d35546ec02d53) noopをprotocolClientNew()からlocal/remoteの初期化へ移しました。
- `--cmd`オプションを追加しました。 (*貢献：Reid Thompson。レビュー：Stefan Fercot, David Steele。提案：Virgile CREVON。*)

  pgBackRestが書き込むコマンド、たとえば`recovery.conf`の`restore_command`で使用するpgBackRest実行ファイルを、`cmd`に設定します。

  課題 [#1537](https://github.com/pgbackrest/pgbackrest/issues/1537); プルリクエスト [#1540](https://github.com/pgbackrest/pgbackrest/pull/1540); コミット [`2a57647`](https://github.com/pgbackrest/pgbackrest/commit/2a576477b316238473525e56bc8fc8ea5790455f)

**改善：**

- バックアップ開始直後にアーカイブをチェックするようにしました。 (*レビュー：Reid Thompson, David Christensen。*)

  WALアーカイブが機能していないためにバックアップが失敗するのは、すべてのファイルのコピー後でした。現在はバックアップ開始直後にアーカイブを確認します。アイドル状態のシステムでは、復元ポイントを作成してWALセグメントを切り替えます。

  課題 [#152](https://github.com/pgbackrest/pgbackrest/issues/152); プルリクエスト [#1570](https://github.com/pgbackrest/pgbackrest/pull/1570); コミット [`1f14f45`](https://github.com/pgbackrest/pgbackrest/commit/1f14f45dfb0d1677a695719381cbd5a8a3c6c986)
- バックアップにタイムラインとチェックポイントのチェックを追加しました。 (*レビュー：Stefan Fercot, Reid Thompson。*)

  バックアップ開始時のチェックポイントとタイムラインが`pg_control`に含まれることを確認するようになりました。また、スタンバイがプライマリーに追随していること、つまり同じタイムライン上で、チェックポイントがバックアップのものより後でないことを確認します。

  プルリクエスト [#1581](https://github.com/pgbackrest/pgbackrest/pull/1581); コミット [`49145d7`](https://github.com/pgbackrest/pgbackrest/commit/49145d72bac16498cdbf5eeb3cd6128ea0be0667)
- バックアップ中に、クラスターが稼働しており正しく設定されていることをチェックするようにしました。 (*レビュー：Stefan Fercot。*)

  クラスターが停止するかスタンバイが昇格すると、直ちにバックアップを失敗させるようになりました。以前はプライマリーの停止を終了時にしか検出せず、スタンバイの昇格は検出していませんでした。

  プルリクエスト [#1584](https://github.com/pgbackrest/pgbackrest/pull/1584); コミット [`bd2ba80`](https://github.com/pgbackrest/pgbackrest/commit/bd2ba802db11c505ec69943fa81b2b379073fbf4)
- `restore`で目標時刻に合うバックアップが見つからない場合にエラーを返すようにしました。 (*レビュー：Reid Thompson, Douglas J Hunley。提案：Douglas J Hunley。*)

  以前は見落としやすい警告で、復旧目標に到達できないバックアップの復元に多くの時間を費やす可能性がありました。

  課題 [#1582](https://github.com/pgbackrest/pgbackrest/issues/1582); プルリクエスト [#1586](https://github.com/pgbackrest/pgbackrest/pull/1586); コミット [`be4ac39`](https://github.com/pgbackrest/pgbackrest/commit/be4ac3923cb77873da298a30aca5d847b3c635af)
- S3／Azureエンドポイントのプロトコルとポートを解析するようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  `repo-s3-endpoint`、`repo-azure-endpoint`、`repo-storage-host`に、`https://host:9000`のようにプロトコルとポートを含められるようになりました。

  課題 [#1560](https://github.com/pgbackrest/pgbackrest/issues/1560); プルリクエスト [#1591](https://github.com/pgbackrest/pgbackrest/pull/1591); コミット [`6a12458`](https://github.com/pgbackrest/pgbackrest/commit/6a12458440168f13cb05d70f36ea54b1860e390c)
- `checkpoint_timeout`が`db-timeout`を超える場合に警告するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  `start-fast=n`で`checkpoint_timeout`が`db-timeout`より大きいと、チェックポイント待ちでバックアップがタイムアウトする場合があります。現在はこの場合に警告します。

  プルリクエスト [#1564](https://github.com/pgbackrest/pgbackrest/pull/1564); コミット [`6723305`](https://github.com/pgbackrest/pgbackrest/commit/672330593789f07aaad90bbafcd2597cbc602686)
- HTTPエラーの出力にメソッドを追加しました。 (*貢献：Christoph Berg。レビュー：David Steele。*)

  プルリクエスト [#1566](https://github.com/pgbackrest/pgbackrest/pull/1566); コミット [`c38e2d3`](https://github.com/pgbackrest/pgbackrest/commit/c38e2d31709804eb4b9125a15ad84c8fc813f366)
- コマンドラインのブール型オプションでy/nの引数を受け付けるようにしました。 (*貢献：Reid Thompson。レビュー：David Steele。*)

  プルリクエスト [#1571](https://github.com/pgbackrest/pgbackrest/pull/1571); コミット [`1a0560d`](https://github.com/pgbackrest/pgbackrest/commit/1a0560d363d28737befb8c222647783d4fc2ca29)
- ログに記録するバックアップサイズを、`info`コマンドの出力と正確に一致させました。 (*貢献：Reid Thompson。レビュー：David Steele。提案：Mahomed Hussein。*)

  ログのバックアップサイズは、コピーしたファイルと`backup_label`、`tablespace_map`だけを含むようになりました。以前は、たとえばスイッチオーバー後の増分バックアップで、確認した全ファイルのサイズを記録していました。

  [`6e63576`](https://github.com/pgbackrest/pgbackrest/commit/6e635764a66278d5a8c2b4d30b23063bc3923067) ログに記録するバックアップサイズをinfoコマンドの報告値と一致させました。; 課題 [#766](https://github.com/pgbackrest/pgbackrest/issues/766); プルリクエスト [#1562](https://github.com/pgbackrest/pgbackrest/pull/1562)

  [`afe77e7`](https://github.com/pgbackrest/pgbackrest/commit/afe77e76e0adf948138d797e227a6f4c7d47c2eb) 6e635764の貢献者を更新しました。

  [`1e77fc3`](https://github.com/pgbackrest/pgbackrest/commit/1e77fc3d75490b7a1b6a0b31be9298c995ec672f) ログ出力にbackup_labelとtablespace_mapのファイルサイズを含めました。; プルリクエスト [#1568](https://github.com/pgbackrest/pgbackrest/pull/1568)

  [`a3d7a23`](https://github.com/pgbackrest/pgbackrest/commit/a3d7a23a9d90611a3d31947598fbea240b250710) バックアップサイズのログ出力にinfoBackupDataByLabel()を使用しました。; プルリクエスト [#1573](https://github.com/pgbackrest/pgbackrest/pull/1573)

  [`dcb4f09`](https://github.com/pgbackrest/pgbackrest/commit/dcb4f09d8315e92c0877b589f3fa9b7f0fa65f93) 1e77fc3dで行ったbackupFilePut()の変更を取り消しました。

**ドキュメントの改善：**

- サイズを指定するオプションのデフォルト値と許容値を適切な単位で表示するようにしました。 (*レビュー：Reid Thompson。*)

  [`cff961e`](https://github.com/pgbackrest/pgbackrest/commit/cff961ede7e41fa8035ffe7451a22eb5ea0e46c1) 設定のレンダリング時に値の一覧を作る処理を集約しました。

  [`038abaa`](https://github.com/pgbackrest/pgbackrest/commit/038abaa71d816cc87b382bd81d3df62ddec9455a) サイズを指定するオプションのデフォルト値と許容値を適切な単位で表示するようにしました。; プルリクエスト [#1557](https://github.com/pgbackrest/pgbackrest/pull/1557)
- `tablespace-map-all`オプションの誤記を修正し、説明を改善しました。 (*レビュー：Reid Thompson。提案：Reid Thompson。*)

  コミット [`df89eff`](https://github.com/pgbackrest/pgbackrest/commit/df89eff429e9b8fbc68d9e9895badf9719fd31d2)
- 複数リポジトリへの将来的な対応に関する古い記述を削除しました。 (*提案：David Christensen。*)

  ドキュメントにはリポジトリは1つだけと記載されていましたが、v2.33から複数リポジトリをサポートしています。

  コミット [`dea7524`](https://github.com/pgbackrest/pgbackrest/commit/dea752477ab8e812cdbd717eb2091baf3f5d0906)

### v2.36リリースノート {#v236-release-notes}

*軽微なバグ修正と改善*

*2021年11月1日リリース*

**バグ修正：**

- stanzaの接頭辞に「global」を使用できるようにしました。 (*レビュー：Stefan Fercot。報告：Younes Alhroub。*)

  `global_stanza`など`global`で始まるスタンザ名が、設定パーサーにグローバルセクションと解釈され、拒否されていました。

  課題 [#1524](https://github.com/pgbackrest/pgbackrest/issues/1524); プルリクエスト [#1525](https://github.com/pgbackrest/pgbackrest/pull/1525); コミット [`498902e`](https://github.com/pgbackrest/pgbackrest/commit/498902e885c9d7a44648ccc01b20454094d5b742)
- 無効なGCSキーファイルによるセグメンテーション違反を修正しました。 (*レビュー：Stephen Frost。報告：Henrik Feldt。*)

  クライアントメール、秘密鍵、トークンURIのいずれかがないGCSキーファイルは、セグメンテーションフォールトを起こしていました。現在はエラーを返します。

  課題 [#1536](https://github.com/pgbackrest/pgbackrest/issues/1536); コミット [`2cea005`](https://github.com/pgbackrest/pgbackrest/commit/2cea005f740d640290a9948595f5933833e30e7d)

**改善：**

- `link-map`オプションで新しいリンクを作成できるようにしました。 (*レビュー：Don Seiler, Stefan Fercot, Chris Bandy。提案：Don Seiler。*)

  `link-map`はバックアップにあるリンクしか再マッピングできませんでした。現在は、バックアップ内の任意のパスやファイルに新しいリンクを作れます。

  [`d89a677`](https://github.com/pgbackrest/pgbackrest/commit/d89a67776cfbb7b3047dbe297cc0c768e5c670e8) command/restoreユニットのrestoreManifestMap()テストをリファクタリングしました。

  [`cf1a575`](https://github.com/pgbackrest/pgbackrest/commit/cf1a57518fe3230886509f59fcec9c9a81e6513c) link-mapを基に動作するようrestoreManifestMap()をリファクタリングしました。

  [`68c5f3e`](https://github.com/pgbackrest/pgbackrest/commit/68c5f3eaf18fc9bd10fde15a323890bcdcbf4534) `link-map`オプションで新しいリンクを作成できるようにしました。; 課題 [#1409](https://github.com/pgbackrest/pgbackrest/issues/1409); プルリクエスト [#1520](https://github.com/pgbackrest/pgbackrest/pull/1520)
- `pg`／`repo`オプションに指定できるインデックスの最大値を256に増やしました。 (*レビュー：Cynthia Shang。*)

  最大インデックスは`pg`オプションが8、`repo`オプションが4でした。現在は両方とも256になり、たとえば`pg256-path`を指定できます。

  [`02b06aa`](https://github.com/pgbackrest/pgbackrest/commit/02b06aa4957cf3fe64ceb7a44cc1893bff12fe99) `pg`／`repo`オプションに指定できるインデックスの最大値を256に増やしました。; プルリクエスト [#1481](https://github.com/pgbackrest/pgbackrest/pull/1481)

  [`71047a9`](https://github.com/pgbackrest/pgbackrest/commit/71047a9d6d1eea71b3fbd430983541a54049cc69) strncpy()でoptionNameへコピーする文字数を制限しました。
- AWS S3の`WebIdentity`認証を追加しました。 (*レビュー：James Callahan, Reid Thompson, Andrew L'Ecuyer。テスト：Benjamin Blattberg。*)

  EKS環境で認証情報を自動取得するには、`repo-s3-key-type=web-id`を設定します。

  [`cfd8233`](https://github.com/pgbackrest/pgbackrest/commit/cfd823355af2ac99f30c5e1393a121c6dbf622b7) 認証方式追加に向けてS3ストレージドライバーをリファクタリングしました。

  [`3879bc6`](https://github.com/pgbackrest/pgbackrest/commit/3879bc69b888daa04d2ca98a2d1219cf22519ddc) AWS S3の`WebIdentity`認証を追加しました。; 課題 [#1203](https://github.com/pgbackrest/pgbackrest/issues/1203); プルリクエスト [#1527](https://github.com/pgbackrest/pgbackrest/pull/1527)

  [`1152f7a`](https://github.com/pgbackrest/pgbackrest/commit/1152f7a7d64e69eed1d9e74b48a308f6c742c28a) tlsClientNew()呼び出しのパラメーター不一致を修正しました。
- `repo-azure-uri-style`オプションを追加しました。

  AzureのURI形式は、`repo-azure-uri-style`を`host`（デフォルト）または`path`に設定して選択します。Azuriteは、エンドポイントが複数部分からなるホスト名に見える場合、host形式のURIを使います。

  コミット [`096829b`](https://github.com/pgbackrest/pgbackrest/commit/096829b3b257444162417662612e80d8cb2ac6ec)
- バックアップファイルの検証エラーを`backup.info`に記録するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

  無効なページチェックサムなどバックアップ中のエラーは、`set`付きの`info`でしか表示されませんでした。現在は`backup.info`のフラグにより、テキストとJSONの両出力でエラーの有無を示します。詳細の表示には引き続き`set`が必要です。

  課題 [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); プルリクエスト [#1508](https://github.com/pgbackrest/pgbackrest/pull/1508); コミット [`34f7873`](https://github.com/pgbackrest/pgbackrest/commit/34f78734325743b4e34cb39224852e6debf49750)
- オンラインバックアップのリストアログに、リカバリーの開始時刻を追加しました。 (*レビュー：Tom Swartz, Stefan Fercot。提案：Tom Swartz。*)

  復元時に、リカバリの起点となる時刻をログ出力し、再生が必要なWALの量が分かるようにしました。

  課題 [#1507](https://github.com/pgbackrest/pgbackrest/issues/1507); プルリクエスト [#1518](https://github.com/pgbackrest/pgbackrest/pull/1518); コミット [`9e79f0e`](https://github.com/pgbackrest/pgbackrest/commit/9e79f0e64b661e944ce2b3897c366feea1544ac2)
- ローカルジョブの失敗時に、元のエラーと再試行を報告するようにしました。 (*レビュー：Stefan Fercot。*)

  ローカルジョブが再試行後も失敗すると、最初のエラーとそのスタックトレース、続いて再試行のエラーを報告するようにしました。以前は最後のエラーだけで、プロトコルの同期ずれなど連鎖的な失敗になっていることがよくありました。

  [`136d309`](https://github.com/pgbackrest/pgbackrest/commit/136d309dd4bc1ada9f3d775f036b62292fda390b) errorInternalThrow()にスタックトレースを指定できるようにしました。

  [`ae40ed6`](https://github.com/pgbackrest/pgbackrest/commit/ae40ed6ec9cf77e577518b128518a5763767f589) HRN_CFG_LOAD()にjobRetryパラメーターを追加しました。

  [`6af827c`](https://github.com/pgbackrest/pgbackrest/commit/6af827cbb1e78cd4c5d649ed4cb24c49a7204b8f) ローカルジョブの失敗時に、元のエラーと再試行を報告するようにしました。; プルリクエスト [#1521](https://github.com/pgbackrest/pgbackrest/pull/1521)
- infoのテキスト出力で、ページチェックサムエラーの名称をエラー一覧に変更しました。 (*レビュー：Stefan Fercot。*)

  `info`のテキスト出力のラベルを"page checksum error"から"error list"に変更しました。ファイルにはページチェックサムエラーでなくアラインメントエラーがある場合もあるためです。

  プルリクエスト [#1519](https://github.com/pgbackrest/pgbackrest/pull/1519); コミット [`9346895`](https://github.com/pgbackrest/pgbackrest/commit/9346895f5b61627b50d431f09447e08d8a50caa8)
- スタンバイでの再生タイムアウトのメッセージにヒントを追加しました。 (*レビュー：Cynthia Shang, Stefan Fercot。提案：Leigh Downs。*)

  スタンバイの再生待ちタイムアウトに、レプリケーションが動作しているか確認することと、プライマリーからバックアップするため`backup-standby`を無効にすることを案内するヒントを追加しました。

  課題 [#1434](https://github.com/pgbackrest/pgbackrest/issues/1434); コミット [`b7ef12a`](https://github.com/pgbackrest/pgbackrest/commit/b7ef12a76f219881d0b24c715592af96fe5c9b8f)

**ドキュメントの不具合修正：**

- ユーザーガイドの誤ったホスト名を修正しました。 (*修正：Reid Thompson。レビュー：David Steele。*)

  レプリケーション設定の`pg_hba.conf`で、pg-standbyではなくpg-primaryのIPアドレスを使っていました。

  プルリクエスト [#1544](https://github.com/pgbackrest/pgbackrest/pull/1544); コミット [`1cb8ae1`](https://github.com/pgbackrest/pgbackrest/commit/1cb8ae15de5b4276682bdd9825ca97012cd43855)

**ドキュメントの改善：**

- オプションのドキュメントを改善しました。

  `buffer-size`のヘルプで使用する全操作を説明し、`cmd-ssh`、`repo-host-cmd`、`pg-host-cmd`の説明を統一しました。また、`archive-header-check`を設定リファレンスのアーカイブセクションへ移しました。

  [`3763624`](https://github.com/pgbackrest/pgbackrest/commit/376362475e3b3b13b70313d9002d4ff8b25b4b40) archive-header-checkをアーカイブのリファレンスセクションへ移しました。

  [`e1f6c06`](https://github.com/pgbackrest/pgbackrest/commit/e1f6c066b3da11fd21b1155c90370c3fa2da06b7) buffer-sizeオプションの説明を改善しました。

  [`fa564ee`](https://github.com/pgbackrest/pgbackrest/commit/fa564ee1969229b5cf60d2479d8ace85325f4db3) cmd-ssh、repo-host-cmd、pg-host-cmdの説明を改善しました。

### v2.35リリースノート {#v235-release-notes}

*バイナリープロトコル*

*2021年8月23日リリース*

**重要な注意事項**：`backup`／`restore`コマンドでコピーしたファイルを記録するログレベルを`detail`に変更しました。これにより、`info`レベルのログが簡潔になります。これらのメッセージが必要な場合は、`backup`／`restore`コマンドのログレベルを`detail`に設定してください。

**バグ修正：**

- S3のマルチパートアップロードの完了処理でエラーを検出するようにしました。 (*レビュー：Cynthia Shang。テスト：Marco Montagna。報告：Marco Montagna, Lev Kokotov, Anderson A. Mallmann。*)

  S3がHTTP成功を返しても、マルチパートアップロードの完了が失敗することがあります。現在は`ETag`のない応答を失敗として扱い、ジョブを再試行します。

  [`8e1807c`](https://github.com/pgbackrest/pgbackrest/commit/8e1807cdbe08a6e059ff79220247cf4b3c058979) S3のマルチパートアップロードの完了処理でエラーを検出するようにしました。; 課題 [#1116](https://github.com/pgbackrest/pgbackrest/issues/1116); 課題 [#1290](https://github.com/pgbackrest/pgbackrest/issues/1290); 課題 [#1433](https://github.com/pgbackrest/pgbackrest/issues/1433); プルリクエスト [#1438](https://github.com/pgbackrest/pgbackrest/pull/1438)

  [`25508a4`](https://github.com/pgbackrest/pgbackrest/commit/25508a48e0d3b0a3eabc6d1fe858b9c3dc12dc86) 8e187cdbで漏れていた貢献者を追加しました。
- シンボリックリンクの循環検出を修正しました。 (*レビュー：Stefan Fercot。報告：Rohit Raveendran。*)

  リンクの検査前にリンクをたどっていたため、循環リンクでマニフェスト作成が無限再帰に陥り、クラッシュしていました。

  課題 [#1447](https://github.com/pgbackrest/pgbackrest/issues/1447); プルリクエスト [#1452](https://github.com/pgbackrest/pgbackrest/pull/1452); コミット [`43b8746`](https://github.com/pgbackrest/pgbackrest/commit/43b874628c86ec4fe297dbd5cab5bd3f62b8639b)
- 選択した`repo`のオプションだけをリモートに渡すようにしました。 (*レビュー：David Christensen, Cynthia Shang。報告：Greg Sabino Mullane, David Christensen。*)

  リモートは厳密に1つのリポジトリを使うため、他のリポジトリのオプションが競合を引き起こすことがありました。

  プルリクエスト [#1480](https://github.com/pgbackrest/pgbackrest/pull/1480); コミット [`935de1e`](https://github.com/pgbackrest/pgbackrest/commit/935de1e7a06d60415c16cad137875b49346337c6)

**改善：**

- バイナリープロトコルを導入しました。 (*レビュー：Cynthia Shang。*)

  ローカルとリモートのプロセスは、JSONの代わりにバイナリーpack形式で通信するようになりました。packはコンパクトで、生成・解析が速く、型も厳密です。各メッセージを1か所で書き込むため、エラー時にプロトコルが不正な状態で残る可能性を減らせます。メッセージサイズの制限もありません。

  [`6a1c033`](https://github.com/pgbackrest/pgbackrest/commit/6a1c0337ddee9900dda58b7d2fa74d82c0586ed2) バイナリープロトコルを導入しました。; プルリクエスト [#1424](https://github.com/pgbackrest/pgbackrest/pull/1424)

  [`2d5cbfc`](https://github.com/pgbackrest/pgbackrest/commit/2d5cbfc73142fa99df609aa23b64db5342e73c88) 6a1c0337のバイナリープロトコルで導入したメモリーリークを修正しました。

  [`f716cb6`](https://github.com/pgbackrest/pgbackrest/commit/f716cb6f4f9765baa03f71b5563786d79d9f04a2) 6a1c0337のバイナリープロトコルで導入した解放後メモリー使用を修正しました。

  [`4fb6384`](https://github.com/pgbackrest/pgbackrest/commit/4fb6384f10f6cd26c422ab9b24feb5ae0ebeeee9) 6a1c0337のバイナリープロトコルによる追加のメモリーリークを修正しました。
- `restore`でデータディレクトリを自動作成するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Chris Bandy。*)

  Perlから移した検査が、復元時のデータディレクトリー作成を妨げていました。

  課題 [#1445](https://github.com/pgbackrest/pgbackrest/issues/1445); プルリクエスト [#1454](https://github.com/pgbackrest/pgbackrest/pull/1454); コミット [`056a307`](https://github.com/pgbackrest/pgbackrest/commit/056a3070e0dba299389c7b5049878d40dd91ec9a)
- `restore`で`--type=lsn`を指定できるようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。提案：James Coleman。*)

  PostgreSQL >= 10でLSNまで復旧するには、`type=lsn`と、`target`にLSNを指定します。

  課題 [#1339](https://github.com/pgbackrest/pgbackrest/issues/1339); プルリクエスト [#1462](https://github.com/pgbackrest/pgbackrest/pull/1462); コミット [`563d117`](https://github.com/pgbackrest/pgbackrest/commit/563d117967ab9770f9f646c6186d0bc37121611f)
- `backup`／`restore`でコピーしたファイルを記録するログレベルをdetailに変更しました。 (*レビュー：Stefan Fercot。提案：Jens Wilke。*)

  これにより`info`レベルのログを減らします。コピーしたファイルを個別に見るには、ログレベルを`detail`にします。

  課題 [#1277](https://github.com/pgbackrest/pgbackrest/issues/1277); プルリクエスト [#1455](https://github.com/pgbackrest/pgbackrest/pull/1455); コミット [`849ab34`](https://github.com/pgbackrest/pgbackrest/commit/849ab343aa10d66fbbd27cad407eff981c186d06)
- チェックポイントのLSNが再生LSNに達するのを待つ間、ループするようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。提案：Fatih Mencutekin。*)

  スタンバイでは、`pg_control`が更新されるまでチェックポイントLSNが再生LSNより少し遅れる場合があります。現在はバックアップを失敗させず、確認を続けます。

  課題 [#1450](https://github.com/pgbackrest/pgbackrest/issues/1450); プルリクエスト [#1460](https://github.com/pgbackrest/pgbackrest/pull/1460); コミット [`8fac1ac`](https://github.com/pgbackrest/pgbackrest/commit/8fac1ac50d28557d162fbb251fbbdcc3c9fb950c)
- `backup`ではファイル総数を、`restore`ではサイズとファイル総数をログに記録するようにしました。 (*レビュー：Cynthia Shang。*)

  バックアップ終了時にサイズをログ出力し、`backup_label`やWALなど、主なコピー処理の後にマニフェストへ追加したファイルも含めるようにしました。復元もサイズとファイル総数をログ出力します。

  プルリクエスト [#1489](https://github.com/pgbackrest/pgbackrest/pull/1489); コミット [`a0bdfa4`](https://github.com/pgbackrest/pgbackrest/commit/a0bdfa436c9e1c2723be905ebe5cef7809a26244)

**ドキュメントの不具合修正：**

- ユーザーガイドの誤ったホスト名を修正しました。 (*レビュー：Stefan Fercot。報告：Greg Sabino Mullane。*)

  一部の例でホスト名ではなく`pg1`を表示し、インストールブロックは指定ホストに関係なくビルドホストへパッケージをインストールしていました。

  プルリクエスト [#1479](https://github.com/pgbackrest/pgbackrest/pull/1479); コミット [`155ef85`](https://github.com/pgbackrest/pgbackrest/commit/155ef85013088a1150a4c15b04af36420d06e9c3)

**ドキュメントの改善：**

- コントリビューションのドキュメントを更新し、プルリクエストのテンプレートを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  貢献ガイドに目次と、テスト出力の読み方・プルリクエスト提出に関するセクションを追加しました。GitHubでは新規プルリクエストにテンプレートを表示します。

  [`e3d05e2`](https://github.com/pgbackrest/pgbackrest/commit/e3d05e2b4aa80149219b6d49a3136b34fa268127) コントリビューションのドキュメントを更新し、プルリクエストのテンプレートを追加しました。; プルリクエスト [#1469](https://github.com/pgbackrest/pgbackrest/pull/1469)

  [`71b654f`](https://github.com/pgbackrest/pgbackrest/commit/71b654fc29497319862fe01c3917bbc353cc6dd9) リンクを修正し、子プロセスの例を更新しました。; プルリクエスト [#1487](https://github.com/pgbackrest/pgbackrest/pull/1487)
- ユーザーガイド内のバックアップの説明を再構成しました。 (*レビュー：Cynthia Shang。*)

  「高速開始オプション」と「アーカイブタイムアウト」のセクションを「クイックスタート - バックアップの実行」へ移しました。PostgreSQL <= 9.6にのみ適用される「自動停止オプション」のセクションは削除しました。

  プルリクエスト [#1488](https://github.com/pgbackrest/pgbackrest/pull/1488); コミット [`6ab18dc`](https://github.com/pgbackrest/pgbackrest/commit/6ab18dc0fa42885aea8eb9405ab0a943c2d49a71)
- コマンドリファレンスで、`restore`の`--type`の動作を明確にしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  リファレンスに、目標が最新バックアップより前で、`type`が`time`でない場合は`set`が必須と明記しました。

  コミット [`a6691c6`](https://github.com/pgbackrest/pgbackrest/commit/a6691c6f615f90195aeb6c1c6657a6afd79a10d3)
- ドキュメントとコメントの誤記を修正しました。 (*貢献：Eric Radman。レビュー：David Steele。*)

  プルリクエスト [#1446](https://github.com/pgbackrest/pgbackrest/pull/1446); コミット [`23bdc3d`](https://github.com/pgbackrest/pgbackrest/commit/23bdc3deb62a622713064df3b0777110ebba8723)

**テストスイートの改善：**

- テストパスがリポジトリパス内にあるかどうかのチェックを追加しました。 (*レビュー：Greg Sabino Mullane。提案：Greg Sabino Mullane。*)

  リポジトリをテストパスへコピーするため、リポジトリパス内にテストパスがあると不可解な失敗が起きていました。現在はこの場合に`test.pl`がエラーを返します。

  課題 [#1472](https://github.com/pgbackrest/pgbackrest/issues/1472); プルリクエスト [#1474](https://github.com/pgbackrest/pgbackrest/pull/1474); コミット [`e32f9e1`](https://github.com/pgbackrest/pgbackrest/commit/e32f9e146b11389e3d16feba9665360b73737d66)
- CodeQLによる静的コード解析を追加しました。 (*レビュー：Cynthia Shang。*)

  CIでCodeQLを実行するようになりました。検出した問題を修正し、たとえば`gmtime()`/`localtime()`を`gmtime_r()`/`localtime_r()`へ置き換えました。

  プルリクエスト [#1457](https://github.com/pgbackrest/pgbackrest/pull/1457); コミット [`3c8819e`](https://github.com/pgbackrest/pgbackrest/commit/3c8819e10f9eff89195566e7e02f349373f5c4c7)
- 標準的なパターンを使用するようテストを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  [`3f9fbc3`](https://github.com/pgbackrest/pgbackrest/commit/3f9fbc3c24eab48e7ae2871484ea01273049e601) command/expireテストを標準パターンに合わせました。; プルリクエスト [#1420](https://github.com/pgbackrest/pgbackrest/pull/1420)

  [`03021c6`](https://github.com/pgbackrest/pgbackrest/commit/03021c6a17f1374e84ef42614fa1dd2a6be4b64d) command/stanzaテストを標準パターンに合わせました。; プルリクエスト [#1426](https://github.com/pgbackrest/pgbackrest/pull/1426)

  [`8dd882b`](https://github.com/pgbackrest/pgbackrest/commit/8dd882badee76b038dc8b494a1112eb3e18ef678) info/infoArchiveテストを標準パターンに合わせました。; プルリクエスト [#1436](https://github.com/pgbackrest/pgbackrest/pull/1436)

  [`ff95edd`](https://github.com/pgbackrest/pgbackrest/commit/ff95eddc369597c76a9ea70ffbada493ed4d1951) command/verifyテストを標準パターンに合わせました。; プルリクエスト [#1435](https://github.com/pgbackrest/pgbackrest/pull/1435)

  [`17c9ed0`](https://github.com/pgbackrest/pgbackrest/commit/17c9ed0ef0380fb14fba9a5299b6618ca8c92c2e) command/infoテストを標準パターンに合わせました。; プルリクエスト [#1432](https://github.com/pgbackrest/pgbackrest/pull/1432)

  [`bffb43e`](https://github.com/pgbackrest/pgbackrest/commit/bffb43ea3fe00f445a2fc3c44a07f105cee65b4b) command/checkテストを標準パターンに合わせました。; プルリクエスト [#1431](https://github.com/pgbackrest/pgbackrest/pull/1431)

  [`fb2d111`](https://github.com/pgbackrest/pgbackrest/commit/fb2d111dcd75021313a64a348959482339bf7f2a) info/infoBackupテストを標準パターンに合わせました。; プルリクエスト [#1437](https://github.com/pgbackrest/pgbackrest/pull/1437)

  [`065a8c8`](https://github.com/pgbackrest/pgbackrest/commit/065a8c8454d2acdd72c0c71a24d6b8bc09669e18) ユニットテストのdefineを文字列定数に置き換えました。; プルリクエスト [#1440](https://github.com/pgbackrest/pgbackrest/pull/1440)

  [`c620811`](https://github.com/pgbackrest/pgbackrest/commit/c6208113bfce9d637ca3fd0b35ab28a819c1a83e) HRN_STORAGE_PUT()マクロにtimeModifiedパラメーターを追加しました。

  [`6a90d46`](https://github.com/pgbackrest/pgbackrest/commit/6a90d469094ee2697ae4c932349756a54136799d) info/manifestテストを標準パターンに合わせました。; プルリクエスト [#1444](https://github.com/pgbackrest/pgbackrest/pull/1444)

  [`62e8d97`](https://github.com/pgbackrest/pgbackrest/commit/62e8d97af03e7628d5710b17aad1cc31f83d7e69) command/archiveテストを標準パターンに合わせました。; プルリクエスト [#1449](https://github.com/pgbackrest/pgbackrest/pull/1449)

  [`8bb0b28`](https://github.com/pgbackrest/pgbackrest/commit/8bb0b28455d59ef884eab7ab25a91f988adbab81) command/controlとcommand/commandテストを標準パターンに合わせました。; プルリクエスト [#1456](https://github.com/pgbackrest/pgbackrest/pull/1456)

  [`f2ec4e0`](https://github.com/pgbackrest/pgbackrest/commit/f2ec4e00a4c4c388a8f1b094381fd566a3dc9aa7) TEST_STORAGE_GET()マクロに暗号パラメーターを追加しました。

  [`4ad0bbd`](https://github.com/pgbackrest/pgbackrest/commit/4ad0bbda53b34688146f14d130cf0e53c8dd650f) command/backupテストを標準パターンに合わせました。; プルリクエスト [#1463](https://github.com/pgbackrest/pgbackrest/pull/1463)

  [`117ffe8`](https://github.com/pgbackrest/pgbackrest/commit/117ffe88965fd60ce3dcb328e9d28503870af05a) command/helpテストを標準パターンに合わせました。; プルリクエスト [#1464](https://github.com/pgbackrest/pgbackrest/pull/1464)

  [`ebe5848`](https://github.com/pgbackrest/pgbackrest/commit/ebe5848494d4e37a9c86f1fafb5b3453c1f425a6) command/localとcommand/remoteテストを標準パターンに合わせました。; プルリクエスト [#1466](https://github.com/pgbackrest/pgbackrest/pull/1466)

  [`a6cdf5b`](https://github.com/pgbackrest/pgbackrest/commit/a6cdf5b22f0eed53f33bbd84478af0542c81af7d) command/repoテストを標準パターンに合わせました。; プルリクエスト [#1467](https://github.com/pgbackrest/pgbackrest/pull/1467)

  [`4992508`](https://github.com/pgbackrest/pgbackrest/commit/49925087644c76df005828eb27c24f503a09b20b) command/restoreテストを標準パターンに合わせました。; プルリクエスト [#1468](https://github.com/pgbackrest/pgbackrest/pull/1468)

  [`4c9ddf5`](https://github.com/pgbackrest/pgbackrest/commit/4c9ddf5ef25d0f441e20e918f57c1ec79218cfdb) storageテストを標準パターンに合わせました。; プルリクエスト [#1470](https://github.com/pgbackrest/pgbackrest/pull/1470)

  [`eeaab6a`](https://github.com/pgbackrest/pgbackrest/commit/eeaab6a3d192fc788c0f74aadbf4b3de5da52531) parse以外のconfigテストを標準パターンに合わせました。; プルリクエスト [#1473](https://github.com/pgbackrest/pgbackrest/pull/1473)

  [`f653b59`](https://github.com/pgbackrest/pgbackrest/commit/f653b59664e757a0e3da63cc8462deafe2d9e0ef) db/dbテストを標準パターンに合わせました。; プルリクエスト [#1486](https://github.com/pgbackrest/pgbackrest/pull/1486)

  [`e17865a`](https://github.com/pgbackrest/pgbackrest/commit/e17865a03a5451b82a101557d400ff223d104383) protocol/protocolテストを標準パターンに合わせました。; プルリクエスト [#1491](https://github.com/pgbackrest/pgbackrest/pull/1491)

  [`eca2fc6`](https://github.com/pgbackrest/pgbackrest/commit/eca2fc69589cd44f7c1a43206553984adde5cfb1) config/parseテストを標準パターンに合わせました。; プルリクエスト [#1492](https://github.com/pgbackrest/pgbackrest/pull/1492)

### v2.34リリースノート {#v234-release-notes}

*PostgreSQL 14のサポート*

*2021年6月7日リリース*

**バグ修正：**

- 以前の`restore`で残ったスプールファイルに関する問題を修正しました。 (*レビュー：Cynthia Shang, Stefan Fercot。テスト：Floris van Nee。報告：Floris van Nee。*)

  以前の復元がスプールパスに残した通知により、`archive-get`がWALセグメントを欠落と報告する可能性がありました。最初の確認時に見つけた通知は削除し、非同期プロセスを再実行するようにしました。非同期プロセスが応答しない場合は、WAL欠落ではなくエラーを報告します。

  課題 [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); プルリクエスト [#1371](https://github.com/pgbackrest/pgbackrest/pull/1371); コミット [`f45e76f`](https://github.com/pgbackrest/pgbackrest/commit/f45e76fa2e8ce0f62317a74fdd51083d52659cd5)
- 大量のテーブルスペースのリンクをチェックする際の問題を修正しました。 (*レビュー：Cynthia Shang。テスト：Avinash Vallarapu。報告：Avinash Vallarapu。*)

  テーブルスペースが多い場合、リンク検査は大量のメモリーを使い、クラッシュすることがありました。新しい検査は大幅に速く、省メモリーで、ファイルリンクの重複も検出します。

  課題 [#1354](https://github.com/pgbackrest/pgbackrest/issues/1354); プルリクエスト [#1356](https://github.com/pgbackrest/pgbackrest/pull/1356); コミット [`eba013b`](https://github.com/pgbackrest/pgbackrest/commit/eba013b49b850e53d59795ac6358fcb3381048a3)
- `restore`中にタイムアウトしないよう、不要になったリモート接続を解放するようにしました。 (*レビュー：Cynthia Shang。報告：Francisco Miguel Biete Banon。*)

  復元全体を通じてリモート接続を保持していたためタイムアウトすることがあり、長い復元の最後に無害でも気になる警告を出していました。現在はマニフェスト読み込み後に接続を閉じます。

  課題 [#1368](https://github.com/pgbackrest/pgbackrest/issues/1368); プルリクエスト [#1374](https://github.com/pgbackrest/pgbackrest/pull/1374); コミット [`06fa185`](https://github.com/pgbackrest/pgbackrest/commit/06fa18582a405417c8ab4ba667cb01a13a5c3103)
- 有効なオプションが指定したコマンドでは無効な場合の`help`を修正しました。 (*レビュー：Stefan Fercot。報告：Cynthia Shang。*)

  コマンドに無効なオプションのヘルプを求めると、`help`がセグメンテーションフォールトしていました。

  プルリクエスト [#1375](https://github.com/pgbackrest/pgbackrest/pull/1375); コミット [`45f8355`](https://github.com/pgbackrest/pgbackrest/commit/45f83558ea862c6f496a27b886e1160e6303bbe8)

**新機能：**

- PostgreSQL 14のサポートを追加しました。 (*レビュー：Cynthia Shang。*)

  PostgreSQL 14には、PostgreSQL 13からのコード変更は不要です。PostgreSQLのベータ・RC期間中にカタログバージョンが変わっても、pgBackRestの新しいリリースを不要としました。

  プルリクエスト [#1413](https://github.com/pgbackrest/pgbackrest/pull/1413); コミット [`2452c4d`](https://github.com/pgbackrest/pgbackrest/commit/2452c4d5a4c230b8e3c33d3bddf69e56dfbec284)
- GCEインスタンス向けにGCSの自動認証を追加しました。 (*レビュー：Jan Wieck。テスト：Daniel Farina。*)

  GCEインスタンスのメタデータから認証トークンを取得するには、`repo-gcs-key-type=auto`を設定します。

  [`7b71604`](https://github.com/pgbackrest/pgbackrest/commit/7b71604defa02d5ed9b7aa3407961cb59a52cc45) GCSテストサーバーのポートに既存の変数を使用しました。

  [`26fefa6`](https://github.com/pgbackrest/pgbackrest/commit/26fefa6aeeae90bbb572ea57b605fb8fe526f1a0) GCSトークン応答の解析を別の関数へ切り出しました。

  [`9af0331`](https://github.com/pgbackrest/pgbackrest/commit/9af033194abc4b1cd3f06c3a97fff71c966c3827) GCEインスタンス向けにGCSの自動認証を追加しました。; プルリクエスト [#1395](https://github.com/pgbackrest/pgbackrest/pull/1395)
- バックアップ履歴を期限切れとして削除する`repo-retention-history`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。*)

  バックアップ履歴の保持日数を設定します。デフォルトではすべての履歴を保持し、リポジトリ内に残るバックアップの履歴は期限切れにしません。フルバックアップのマニフェストが期限切れになると、それに属する差分・増分バックアップのマニフェストも期限切れになります。

  プルリクエスト [#1389](https://github.com/pgbackrest/pgbackrest/pull/1389); コミット [`5b332b2`](https://github.com/pgbackrest/pgbackrest/commit/5b332b22b508d896abb64fa6abe26c78c83a29bc)
- `db-exclude`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)

  復元では、指定したデータベースをゼロで埋めたスパースファイルとして書き込み、除外します。PostgreSQLはリカバリを実行でき、その後でこれらのデータベースを削除できます。`db-include`を指定すると、`db-exclude`はシステムデータベースの`template0`、`template1`、`postgres`にだけ適用されます。

  課題 [#986](https://github.com/pgbackrest/pgbackrest/issues/986); プルリクエスト [#1337](https://github.com/pgbackrest/pgbackrest/pull/1337); コミット [`292f836`](https://github.com/pgbackrest/pgbackrest/commit/292f836f1243e51d102bb4be202e7b21a7a386b1)

**改善：**

- アーカイブの期限切れ処理のログレベルをdetailからinfoに変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  プルリクエスト [#1416](https://github.com/pgbackrest/pgbackrest/pull/1416); コミット [`aceb956`](https://github.com/pgbackrest/pgbackrest/commit/aceb956815a87f0c19ea171de25d2c3842a6d806)
- `restore`でstanzaのアーカイブスプールパスを削除するようにしました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)

  スプールパス内のファイルが新しいクラスターに干渉することがありました。たとえば古い`archive-push`の確認通知でWALアーカイブを省略する可能性がありました。

  課題 [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); プルリクエスト [#1386](https://github.com/pgbackrest/pgbackrest/pull/1386); コミット [`320c6e1`](https://github.com/pgbackrest/pgbackrest/commit/320c6e1aad2cc9a8dabecb2bc91a9b34464de6ec)
- `backup`のコピー中は、ファイルのアトミックな書き込みやパスの同期を行わないようにしました。 (*レビュー：Stephen Frost, Stefan Fercot, Cynthia Shang。*)

  失敗したバックアップの再開時にはチェックサムを検証し、終了時にはすべてのパスを同期するため、アトミックな書き込みは不要です。

  プルリクエスト [#1373](https://github.com/pgbackrest/pgbackrest/pull/1373); コミット [`aa72c19`](https://github.com/pgbackrest/pgbackrest/commit/aa72c19a831fb0dd15a50a003fbaad427f335353)

**ドキュメントの改善：**

- コントリビューションのドキュメントを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele, Stefan Fercot。*)

  貢献ガイドに、コード作成、設定オプション追加、テストの例を増やしました。

  プルリクエスト [#1400](https://github.com/pgbackrest/pgbackrest/pull/1400); コミット [`68faf14`](https://github.com/pgbackrest/pgbackrest/commit/68faf1482a42ea14f5b00a91e19bd5aedec275b8)
- RHEL/CentOSのユーザーガイドを1つのドキュメントに統合しました。 (*レビュー：Cynthia Shang。*)

  2つ目のガイドの主な目的は、現在はサポート終了したPostgreSQL <= 9.5の`stop-auto`の説明でした。このオプションは引き続きリファレンスに記載しています。

  プルリクエスト [#1405](https://github.com/pgbackrest/pgbackrest/pull/1405); コミット [`ccac75e`](https://github.com/pgbackrest/pgbackrest/commit/ccac75e7de8754b39bb691ff8830a2839ea7a285)
- `repo-s3-role`は`ARN`ではないことを明確にしました。 (*貢献：Isaac Yuen。レビュー：David Steele。*)

  プルリクエスト [#1365](https://github.com/pgbackrest/pgbackrest/pull/1365); コミット [`5bf1606`](https://github.com/pgbackrest/pgbackrest/commit/5bf160643b53699a28a8f0920c36d6ded767d249)

### v2.33リリースノート {#v233-release-notes}

*複数リポジトリとGCSのサポート*

*2021年4月5日リリース*

**バグ修正：**

- オプションに関する警告によって非同期の`archive-get`／`archive-push`が動作しなくなる問題を修正しました。 (*レビュー：Cynthia Shang。報告：Lev Kokotov。*)

  非同期プロセスのオプション警告が、閉じたstdoutへ出力され、プロセスを中止させていました。非同期ロールとデフォルトロールで有効なオプションが異なるようになったため、頻発するようになりました。現在はデフォルトロールでだけ警告を出します。

  課題 [#1299](https://github.com/pgbackrest/pgbackrest/issues/1299); プルリクエスト [#1301](https://github.com/pgbackrest/pgbackrest/pull/1301); コミット [`3837e61`](https://github.com/pgbackrest/pgbackrest/commit/3837e61a7504b1e211e4b3a70cbe97343c1cf2e6)
- バックアップ中のアーカイブコピーで発生するメモリリークを修正しました。 (*レビュー：Cynthia Shang。報告：Christian ROUX, Efremov Egor。*)

  `archive-copy`でWALをバックアップへコピーすると、特に再圧縮が必要な場合にメモリーがリークしていました。

  課題 [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); コミット [`778adbf`](https://github.com/pgbackrest/pgbackrest/commit/778adbf19f71ceb90071f01197bf189d59b14df0)
- 暗号化パスフレーズの生成時にスタックがオーバーフローする問題を修正しました。 (*レビュー：Cynthia Shang。報告：bsiara。*)

  生成するパスフレーズのバッファーに終端のゼロ用の余地がありませんでした。musl libcを使うarm64で発見されました。

  課題 [#1294](https://github.com/pgbackrest/pgbackrest/issues/1294); プルリクエスト [#1295](https://github.com/pgbackrest/pgbackrest/pull/1295); コミット [`d29855b`](https://github.com/pgbackrest/pgbackrest/commit/d29855bd0bf8b957fa8c06445d22e425c443a704)
- S3リポジトリでの`repo-ls` `/`を修正しました。 (*レビュー：Cynthia Shang。報告：Lesovsky Alexey。*)

  S3が`/`を必要なヘッダーのないファイルとして報告し、エラーになっていました。現在は、パスをサポートしないストレージでは`/`が存在しないと報告します。

  課題 [#1317](https://github.com/pgbackrest/pgbackrest/issues/1317); プルリクエスト [#1336](https://github.com/pgbackrest/pgbackrest/pull/1336); コミット [`b1d945e`](https://github.com/pgbackrest/pgbackrest/commit/b1d945ebb774c25676155af439b0558e8582bbe5)

**新機能：**

- 複数リポジトリに対応しました。 (*貢献：Cynthia Shang, David Steele。レビュー：Stefan Fercot, Stephen Frost。*)

  高速復元用のローカルリポジトリと冗長性のためのリモートリポジトリなど、最大4つのリポジトリを設定できます。`archive-push`はすべてへWALを転送し、バックアップはリポジトリごとにスケジュールします。全リポジトリを扱うコマンドも、`repo`が必要なコマンドもあります。`repo1`だけを設定した場合、`repo`は不要です。

  [`3408f1e`](https://github.com/pgbackrest/pgbackrest/commit/3408f1ee2ee3f774699a15de045e0afe3eaf9a26) expireコマンドの複数リポジトリ対応を改善しました。; プルリクエスト [#1289](https://github.com/pgbackrest/pgbackrest/pull/1289)

  [`e28f6f1`](https://github.com/pgbackrest/pgbackrest/commit/e28f6f11e97a80e9c1adf1a6eaeeabbfc991914f) リポジトリ処理中にエラーが起きてもExpireを続行します。; プルリクエスト [#1308](https://github.com/pgbackrest/pgbackrest/pull/1308)

  [`bec3e20`](https://github.com/pgbackrest/pgbackrest/commit/bec3e20b2cb061ef0413df24234ebe246ea53063) archive-getコマンドに複数リポジトリ対応を追加しました。; プルリクエスト [#1292](https://github.com/pgbackrest/pgbackrest/pull/1292)

  [`118d9e6`](https://github.com/pgbackrest/pgbackrest/commit/118d9e64fea71c2e049b52802e55f72f5793871b) restoreコマンドの複数リポジトリ対応を改善しました。; プルリクエスト [#1300](https://github.com/pgbackrest/pgbackrest/pull/1300)

  [`065b2ff`](https://github.com/pgbackrest/pgbackrest/commit/065b2ff2300a9f06a8c32621fac521451ca942bd) infoコマンドのrepoMin/Maxをリファクタリングしました。

  [`0ddc038`](https://github.com/pgbackrest/pgbackrest/commit/0ddc0380ff408f9ed6e8bcd4d328df500681ce77) 結合テストからrestoreのデフォルトrepoを削除しました。

  [`13dc8e6`](https://github.com/pgbackrest/pgbackrest/commit/13dc8e68d74fa9e06180e67b7e59994767b4a34d) backupコマンドの--repoを省略可能にしました。; プルリクエスト [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`a1280c4`](https://github.com/pgbackrest/pgbackrest/commit/a1280c41e530500e5bbde73a900683f6db207686) archive-pushの警告を、archive-getと同様に動作するようリファクタリングしました。

  [`3b8f0ef`](https://github.com/pgbackrest/pgbackrest/commit/3b8f0ef7ae8a81ae969934fff4ad3da299454b24) archive-pushに書き込み障害への耐性を追加しました。; プルリクエスト [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`95063f6`](https://github.com/pgbackrest/pgbackrest/commit/95063f6812279cd59380fd72e16e67b631582bd0) stanza-deleteを除く残りのコマンドでも--repoを省略可能にしました。

  [`1dbb3bf`](https://github.com/pgbackrest/pgbackrest/commit/1dbb3bf50b94dcc9d53dfe1e5ad57a17bd6d38e8) 複数リポジトリに対応しました。; プルリクエスト [#1227](https://github.com/pgbackrest/pgbackrest/pull/1227)

  [`31c7824`](https://github.com/pgbackrest/pgbackrest/commit/31c7824a4d84cbf5a0ba0938f4caa546fa67af0a) stanza-*コマンドをリモート実行できるようにしました。; プルリクエスト [#1326](https://github.com/pgbackrest/pgbackrest/pull/1326)

  [`2789d3b`](https://github.com/pgbackrest/pgbackrest/commit/2789d3b6206c4de9299a3bc459e04cdab793abc9) infoコマンドの耐障害性を改善しました。; プルリクエスト [#1342](https://github.com/pgbackrest/pgbackrest/pull/1342)

  [`01b8e22`](https://github.com/pgbackrest/pgbackrest/commit/01b8e2258f6efa5386665c33cb5c267c154376fb) archive-pushコマンドの耐障害性を改善しました。; プルリクエスト [#1343](https://github.com/pgbackrest/pgbackrest/pull/1343)
- リポジトリストレージとしてGCSに対応しました。 (*レビュー：Cynthia Shang。テスト：Daniel Farina。*)

  GCSまたはGCS互換オブジェクトストアにリポジトリを保存するには、`repo-type=gcs`を設定します。

  [`dcb79ab`](https://github.com/pgbackrest/pgbackrest/commit/dcb79ab8fb18c63c2d56ecacd9d680b999ea044b) JSONの\uエスケープ文字をデコードしました。

  [`1b4b353`](https://github.com/pgbackrest/pgbackrest/commit/1b4b3538cc218f66ed1e903c3caeade4b0ab1120) HTTPとストレージのモジュールで、適切な箇所のuriをpathに改名しました。

  [`66a4ff4`](https://github.com/pgbackrest/pgbackrest/commit/66a4ff496afe63305cb1a437bcb52d1efc11edf7) HttpRequestへ渡す前にパスをエンコードしました。

  [`d485609`](https://github.com/pgbackrest/pgbackrest/commit/d4856096587c72daee76f8ad8408db677a16d6dd) strNewEncode()、strCatEncode()、bufNewDecode()を追加しました。

  [`abcbe0f`](https://github.com/pgbackrest/pgbackrest/commit/abcbe0f9c1804ecb1b93b811cfb0a362c17e1b85) encodeモジュールのファイルを1つに統合しました。

  [`edab2a0`](https://github.com/pgbackrest/pgbackrest/commit/edab2a0b89eabc5fd5ba6e795d938670bd5d3105) エンコード形式の分岐にif-elseではなくswitchを使いました。

  [`f6c3262`](https://github.com/pgbackrest/pgbackrest/commit/f6c3262861252b24e7e0cffd6d67e0c5e3291f3e) encodeモジュールのvalid/validate関数を外部公開しないようにしました。

  [`a1f4fd3`](https://github.com/pgbackrest/pgbackrest/commit/a1f4fd32a1790e569ccae3598cd9648bb25d13b6) ASSERT_MSG()を追加しました。

  [`00b60e5`](https://github.com/pgbackrest/pgbackrest/commit/00b60e564eef13f8adba0ab867fcde2c352669d6) base64urlエンコードを追加しました。

  [`54c4eb0`](https://github.com/pgbackrest/pgbackrest/commit/54c4eb0c10758879b4bf2b96efd2a1523ecccc21) リモートストレージオブジェクトを書き込み可能にしました。

  [`088662d`](https://github.com/pgbackrest/pgbackrest/commit/088662d986288843d1bfd118b724091c93df4569) リポジトリストレージとしてGCSに対応しました。; 課題 [#631](https://github.com/pgbackrest/pgbackrest/issues/631); 課題 [#743](https://github.com/pgbackrest/pgbackrest/issues/743); プルリクエスト [#1320](https://github.com/pgbackrest/pgbackrest/pull/1320)
- `archive-header-check`オプションを追加しました。 (*レビュー：Stephen Frost, Cynthia Shang。提案：Hans-Jürgen Schönig。*)

  WALを正しいスタンザへ送るため、ヘッダーをPostgreSQLのバージョンとシステム識別子と照合します。デフォルトで有効ですが、暗号化されたWALなど、必要な場合は無効にできます。

  プルリクエスト [#1298](https://github.com/pgbackrest/pgbackrest/pull/1298); コミット [`b6106f3`](https://github.com/pgbackrest/pgbackrest/commit/b6106f3c1f586b410c50c9da8dcea583cc157423)

**改善：**

- 選択的リストアの対象に、再作成されたシステムデータベースを含めるようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)

  作り直したシステムデータベース（`template0`、`template1`、`postgres`）は、OIDからユーザーデータベースに見える場合があります。現在はOIDに関係なく常に復元します。

  課題 [#986](https://github.com/pgbackrest/pgbackrest/issues/986); プルリクエスト [#1307](https://github.com/pgbackrest/pgbackrest/pull/1307); コミット [`6942ff5`](https://github.com/pgbackrest/pgbackrest/commit/6942ff569dd950a5146faa0bebfee69e241c4179)
- S3の署名対象ヘッダーから`content-length`を除外しました。 (*レビュー：Cynthia Shang。提案：Brian P Bockelman。*)

  一部のプロキシが`content-length`ヘッダーを書き換え、そのヘッダーを署名対象とした場合に認証が失敗していました。

  課題 [#1340](https://github.com/pgbackrest/pgbackrest/issues/1340); プルリクエスト [#1341](https://github.com/pgbackrest/pgbackrest/pull/1341); コミット [`7d7ac0e`](https://github.com/pgbackrest/pgbackrest/commit/7d7ac0e0eb63a02bbc1dd8bd8fc89c6008c740f8)
- 使用頻度の低いリポジトリストレージオプションを統合しました。 (*レビュー：Cynthia Shang。*)

  S3とAzureのCA、ホスト、ポート、TLS検証オプションを`repo-storage-*`へ改名しました。たとえば`repo1-s3-host`は`repo1-storage-host`になりました。古い名前も引き続き受け付けます。

  プルリクエスト [#1321](https://github.com/pgbackrest/pgbackrest/pull/1321); コミット [`d1aa765`](https://github.com/pgbackrest/pgbackrest/commit/d1aa765a9d5f290738c1de00c5ea99d5f6056ba5)
- `./configure --with-configdir`で`config-path`のデフォルト値を変更できるようにしました。 (*貢献：Michael Schout。レビュー：David Steele。*)

  パッケージ作成者はビルド時に`config-path`のデフォルトを変更できます。このオプションを指定しなければ、引き続き`/etc/pgbackrest`です。

  [`6a717e0`](https://github.com/pgbackrest/pgbackrest/commit/6a717e032f1309ddc9dc955042b5e2ac2bc7324d) configureスクリプトで設定パスを指定しました。

  [`9243962`](https://github.com/pgbackrest/pgbackrest/commit/9243962b9504787c6f4af42318af6dc27094136d) `./configure --with-configdir`で`config-path`のデフォルト値を変更できるようにしました。; 課題 [#1251](https://github.com/pgbackrest/pgbackrest/issues/1251); 課題 [#1293](https://github.com/pgbackrest/pgbackrest/issues/1293); プルリクエスト [#1255](https://github.com/pgbackrest/pgbackrest/pull/1255)
- `backup`中のアーカイブコピーをログに記録するようにしました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)

  課題 [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); プルリクエスト [#1328](https://github.com/pgbackrest/pgbackrest/pull/1328); コミット [`c862e96`](https://github.com/pgbackrest/pgbackrest/commit/c862e9654aff198167efeb897957bf93c1afe453)

**ドキュメントの改善：**

- リファレンスを更新し、ユーザーガイドの例へのリンクを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  コマンドリファレンスからユーザーガイドの例へリンクし、`expire`の`set`など、一部の説明を明確にしました。

  プルリクエスト [#1353](https://github.com/pgbackrest/pgbackrest/pull/1353); コミット [`d372dd6`](https://github.com/pgbackrest/pgbackrest/commit/d372dd652c9a01b72444998d87f0f44464676803)
- 選択的リストアのドキュメントに注意事項を追加しました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)

  整合性が確立された後はPostgreSQLがゼロで埋めたページをエラーとするため、`type=immediate`を指定しないとリカバリが失敗する可能性があります。PostgreSQL >= 13では`ignore_invalid_pages`を使えますが、選択したデータベースの無効なページがないかログを確認してください。

  課題 [#796](https://github.com/pgbackrest/pgbackrest/issues/796); プルリクエスト [#1329](https://github.com/pgbackrest/pgbackrest/pull/1329); コミット [`92d12cc`](https://github.com/pgbackrest/pgbackrest/commit/92d12ccb9bd0787e30441794e2a2a4d4a4e0fe9c)
- `archive-copy`のドキュメントに`compress-type`の説明を補いました。 (*レビュー：Cynthia Shang, Stefan Fercot。*)

  `archive-push`と`backup`で`compress-type`が異なると、コストの高いWALの再圧縮が必要になります。

  課題 [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); プルリクエスト [#1327](https://github.com/pgbackrest/pgbackrest/pull/1327); コミット [`9506ffa`](https://github.com/pgbackrest/pgbackrest/commit/9506ffae39dd86d2c5454511026f1249097d96a2)
- `compress-type`の値ごとに`compress-level`のデフォルト値を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  デフォルトは、`bz2`が9、`gz`が6、`lz4`が1、`zst`が3です。

  課題 [#1242](https://github.com/pgbackrest/pgbackrest/issues/1242); プルリクエスト [#1346](https://github.com/pgbackrest/pgbackrest/pull/1346); コミット [`3e20608`](https://github.com/pgbackrest/pgbackrest/commit/3e206088e79c4a73a20b8f2fda1706c6b95fa188)
- 必要なNFS設定はPostgreSQLと同じであることを明記しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

  課題 [#871](https://github.com/pgbackrest/pgbackrest/issues/871); プルリクエスト [#1347](https://github.com/pgbackrest/pgbackrest/pull/1347); コミット [`7598762`](https://github.com/pgbackrest/pgbackrest/commit/75987621fab5f57d0e95b42eabd301731587c438)

### v2.32リリースノート {#v232-release-notes}

*リポジトリコマンド*

*2021年2月8日リリース*

**バグ修正：**

- 前回の再開処理でバックアップが一部削除された後の再開処理を修正しました。 (*レビュー：Cynthia Shang。報告：Tom Swartz。*)

**新機能：**

- `repo-ls`コマンドを追加しました。 (*レビュー：Cynthia Shang。テスト：Stefan Fercot。*)
- `repo-get`コマンドを追加しました。 (*貢献：Stefan Fercot, David Steele。レビュー：Cynthia Shang。*)
- `archive-mode-check`オプションを追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。テスト：Michael Banck。*)

**改善：**

- `archive-get`の性能を改善しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- `expire`コマンドのドキュメントを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

### v2.31リリースノート {#v231-release-notes}

*軽微なバグ修正と改善*

*2020年12月7日リリース*

**バグ修正：**

- データベース名の先頭文字に`[`、`#`、`space`を使用できるようにしました。 (*レビュー：Stefan Fercot, Cynthia Shang。報告：Jefferson Alexandre。*)
- `restore`の種類が`standby`の場合、PostgreSQL 12でのみ`standby.signal`を作成するようにしました。 (*修正：Stefan Fercot。レビュー：David Steele。報告：Keith Fiske。*)

**新機能：**

- 履歴ファイルを期限切れとして削除するようにしました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)
- `info`コマンドの`text`出力でページチェックサムエラーを報告するようにしました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang。*)
- `repo-azure-endpoint`オプションを追加しました。 (*レビュー：Cynthia Shang。テスト：Brian Peterson。提案：Brian Peterson。*)
- `pg-database`オプションを追加しました。 (*レビュー：Cynthia Shang。*)

**改善：**

- 指定したstanzaが存在しない場合の`info`コマンドの出力を改善しました。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。提案：uspen。*)
- `backup`／`restore`コマンドで大きなファイル一覧を扱う際の性能を改善しました。 (*レビュー：Cynthia Shang。テスト：Oscar。*)
- バックアップ開始時のPostgreSQLのスリープ処理に再試行を追加しました。 (*レビュー：Cynthia Shang。提案：Vitaliy Kukharik。*)

**ドキュメントの改善：**

- RHEL/CentOS 6のドキュメントをRHEL/CentOS 8のものに置き換えました。

### v2.30リリースノート {#v230-release-notes}

*PostgreSQL 13のサポート*

*2020年10月5日リリース*

**バグ修正：**

- バックアップユーザーが`pg_settings`を読み取れない場合に、ヒント付きのエラーを返すようにしました。 (*レビュー：Stefan Fercot, Cynthia Shang。報告：Mohamed Insaf K。*)

**新機能：**

- PostgreSQL 13に対応しました。 (*レビュー：Cynthia Shang。*)

**改善：**

- PostgreSQLバージョンの識別を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)
- 作業ディレクトリのエラーメッセージを改善しました。 (*レビュー：Stefan Fercot。*)
- WALセグメントが見つからない場合に、stanzaの開始に関するヒントを追加しました。 (*貢献：David Christensen。レビュー：David Steele。*)
- プロトコルバージョンの不一致に関するヒントを追加しました。 (*レビュー：Cynthia Shang。提案：loop-evgeny。*)

**ドキュメントの改善：**

- リモートで実行する場合はpgBackRestのバージョンを一致させる必要があることを明記しました。 (*レビュー：Cynthia Shang。提案：loop-evgeny。*)
- infoコマンドの説明をリファレンスに移動し、ユーザーガイドへのリンクを追加しました。 (*レビュー：Cynthia Shang。提案：Christophe Courtois。*)
- CentOS/RHELユーザーガイドのyumリポジトリのパスを更新しました。 (*貢献：Heath Lord。レビュー：David Steele。*)


### v2.29リリースノート {#v229-release-notes}

*AWSでのS3認証情報の自動取得*

*2020年8月31日リリース*

**バグ修正：**

- `local`／`remote`プロセスを終了する際のエラーを抑止するようにしました。コマンドは完了しているため、エラーを返しても逆効果ですが、通常とは異なる事象が発生したことを示す**警告**は引き続き出力します。 (*レビュー：Cynthia Shang。報告：argdenis。*)
- ファイル名やデータベース名に`=`文字が含まれる場合の問題を修正しました。 (*レビュー：Bastian Wegge, Cynthia Shang。報告：Brad Nicholson, Bastian Wegge。*)

**新機能：**

- AWSインスタンスで一時的なS3認証情報を自動取得するようにしました。 (*貢献：David Steele, Stephen Frost。レビュー：Cynthia Shang, Aleš Zelený, Jeanette Bromage。テスト：David Youatt。*)
- リストア時にアーカイブを無効にする`archive-mode`オプションを追加しました。 (*レビュー：Stephen Frost。提案：Stephen Frost。*)

**改善：**

- PostgreSQL 13 beta3に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。
- S3／Azureストレージの`list`／`remove`を非同期化しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)
- マニフェストの作成時に、unloggedリレーションを検出する処理のメモリ使用量を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost, Oscar。テスト：Brad Nicholson。提案：Oscar, Brad Nicholson。*)
- 非同期プロセスをforkした後、ファイルディスクリプターを積極的に閉じるようにしました。 (*レビュー：Stephen Frost, Cynthia Shang。*)
- バックアップ時のリモート接続を閉じるタイミングを、アーカイブチェックの後に遅らせました。 (*貢献：Floris van Nee。レビュー：David Steele。*)
- 詳細なエラー出力を改善しました。 (*レビュー：Cynthia Shang。*)
- TLSのエラー報告を改善しました。 (*レビュー：Cynthia Shang, Stephen Frost。*)

**ドキュメントの不具合修正：**

- `compress-type`オプションのリファレンスに`none`を追加し、例を修正しました。 (*報告：Ugo Bellavance, Don Seiler。*)
- `repo-type`オプションのリファレンスに、欠落していた`azure`の種類を追加しました。 (*修正：Don Seiler。レビュー：David Steele。*)
- `repo-cipher-type`オプションのリファレンスの誤記を修正しました。 (*修正：Don Seiler。レビュー：David Steele。*)

**ドキュメントの改善：**

- `expire-auto`が無効な場合は、`expire`を定期的に実行する必要があることを明確にしました。 (*レビュー：Douglas J Hunley。提案：Douglas J Hunley。*)

### v2.28リリースノート {#v228-release-notes}

*Azureリポジトリストレージ*

*2020年7月20日リリース*

**バグ修正：**

- `restore`の`--force`が`--force --delta`と同じ動作をする問題を修正しました。この問題により、`restore`がファイルを上書きせず、タイムスタンプとサイズに基づいて置き換えていたため、更新すべきファイルが変更されずに残る場合がありました。通常の`restore`と`restore`の`--delta`は、この問題の影響を受けませんでした。 (*レビュー：Cynthia Shang。*)

**新機能：**

- リポジトリストレージとしてAzureに対応しました。 (*レビュー：Cynthia Shang。テスト：Don Seiler。*)
- `expire-auto`オプションを追加しました。バックアップの成功後に自動実行する期限切れ処理を無効にできます。 (*貢献：Stefan Fercot。レビュー：Cynthia Shang, David Steele。*)

**改善：**

- S3のマルチパートアップロードを非同期化しました。 (*レビュー：Stephen Frost。*)
- `backup`、`restore`、`archive-get`、`archive-push`に自動再試行を追加しました。 (*レビュー：Cynthia Shang。*)
- バックアップの制御に使用するPostgreSQLセッションで、クエリーの並列実行を無効にしました。 (*レビュー：Stefan Fercot。*)
- PostgreSQL 13 beta2に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。
- 無効なHTTPレスポンスステータスの処理を改善しました。 (*レビュー：Cynthia Shang。*)
- `archive-get`コマンドで`pg1-path`オプションがない場合のエラーを改善しました。 (*レビュー：Cynthia Shang。*)
- タイムラインの切り替え後にチェックサムによる差分処理を有効にする場合のヒントを追加しました。 (*レビュー：Matt Bunter, Cynthia Shang。*)
- 適切な箇所で、`postmaster`の代わりにPostgreSQLという名称を使用するようにしました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの不具合修正：**

- `repo-retention-full-type`オプションの誤った例を修正しました。 (*報告：Höseyin Sönmez。*)
- HTMLとmanのコマンドリファレンスから内部コマンドを削除しました。 (*報告：Cynthia Shang。*)

**ドキュメントの改善：**

- ユーザーガイドのビルドに使用するPostgreSQLのバージョンを更新しました。また、特定のバージョンでビルドしたガイドでも一定範囲のPostgreSQLバージョンに適用できることを示すため、バージョン範囲を追加しました。 (*レビュー：Stephen Frost。*)
- 特定のバックアップセットの期限切れ処理に関するFAQを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- デフォルトのPITRの動作を明確にするため、FAQを更新しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

### v2.27リリースノート {#v227-release-notes}

*期限切れ処理の改善と圧縮ドライバー*

*2020年5月26日リリース*

**バグ修正：**

- ファイルへのリンクがパスへのリンクに含まれているかを確認する処理を修正しました。 (*レビュー：Cynthia Shang。報告：Christophe Cavallié。*)
- 同期`archive-push`で`pg-path1`を省略できるようにしました。 (*レビュー：Cynthia Shang。報告：Jerome Peng。*)
- `expire`コマンドが停止ファイルの有無を確認するようになりました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- HTTPレスポンスに理由句がない場合に対応しました。 (*レビュー：Cynthia Shang。報告：Tenuun。*)
- lz4圧縮のフラッシュ時のバッファーサイズを増やしました。 (*レビュー：Cynthia Shang。報告：Eric Radman。*)
- `remote`コマンドで`pg-host*`と`repo-host*`オプションを無視するようにしました。 (*レビュー：Cynthia Shang。報告：Pavel Suderevsky。*)
- `remote`コマンドで`pg1-*`オプションが欠落する場合がある問題を修正しました。 (*レビュー：Cynthia Shang。報告：Andrew L'Ecuyer。*)

**新機能：**

- フルバックアップの期間に基づく保持に対応しました。`--repo-retention-full-type`オプションで、日数で指定した期間に基づいてフルバックアップを保持できます。 (*貢献：Cynthia Shang, Pierre Ducroquet。レビュー：David Steele。*)
- バックアップを個別に期限切れとして削除できるようにしました。保持設定に関係なく、ユーザーが指定したバックアップを削除できます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- Zstandard圧縮に対応しました。`compress-type=zst`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*レビュー：Cynthia Shang。*)
- bzip2圧縮に対応しました。`compress-type=bz2`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*貢献：Stephen Frost。レビュー：David Steele, Cynthia Shang。*)
- `info`コマンドに`backup`／`expire`の実行状態を追加しました。 (*貢献：Stefan Fercot。レビュー：David Steele。*)

**改善：**

- `repo-retention-archive`のしきい値に達した場合にのみ、WALアーカイブを期限切れとして削除するようにしました。従来、最初のフルバックアップより前のWALは、最初のフルバックアップの後に削除されていました。今後は保持設定に従って保持されます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- FIPSが有効な場合でもS3を使用できるよう、独自のMD5実装を追加しました。 (*レビュー：Cynthia Shang, Stephen Frost。提案：Brian Almeida, John Kelly。*)
- PostgreSQL 13 beta1に対応しました。以後のベータ版でcontrol/catalog/WALのバージョンが変更されると互換性が失われる可能性がありますが、pgBackRestも各リリースに合わせて更新します。 (*レビュー：Cynthia Shang。*)
- `buffer-size`のデフォルト値を`1MiB`に減らしました。 (*レビュー：Stephen Frost。*)
- リポジトリホスト以外で`expire`を実行した場合に、わかりやすいエラーを返すようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.26リリースノート {#v226-release-notes}

*ノンブロッキングTLS*

*2020年4月20日リリース*

**バグ修正：**

- マニフェストの正規表現から空の部分式を削除しました。他のプラットフォームでは問題なく動作しているようでしたが、MacOSでは問題が発生していました。 (*修正：David Raftis。レビュー：David Steele。*)

**改善：**

- ノンブロッキングTLSを実装しました。 (*レビュー：Cynthia Shang, Stephen Frost。テスト：Slava Moudry。*)
- バックアップでコピーするサイズの制限を、WALに記録されるファイルだけに適用するようにしました。以前の動作では、バックアップ内の`postgresql.conf`や`postgresql.auto.conf`が切り詰められる可能性がありました。 (*レビュー：Cynthia Shang。*)
- TCPキープアライブのオプションを設定できるようにしました。 (*提案：Marc Cousin。*)
- `io-timeout`オプションを追加しました。 (*レビュー：Cynthia Shang。*)

### v2.25リリースノート {#v225-release-notes}

*LZ4圧縮のサポート*

*2020年3月26日リリース*

**新機能：**

- lz4圧縮のサポートを追加しました。`compress-type=lz4`を設定すると、新しいバックアップとアーカイブは以前のpgBackRestバージョンとは互換性がなくなり、リストアできなくなることに注意してください。 (*レビュー：Cynthia Shang。*)
- `expire`コマンドに`--dry-run`オプションを追加しました。dry-runを使用すると、実際には何も削除せずに、`expire`コマンドが削除するバックアップとアーカイブを確認できます。 (*貢献：Cynthia Shang, Luca Ferrari。レビュー：David Steele。提案：Marc Cousin。*)

**改善：**

- リモートでのマニフェスト作成の性能を改善しました。 (*提案：Jens Wilke。*)
- Linuxでのkeepaliveオプションの検出を修正しました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- 標準規格に関するフラグを正しく設定するため、configureにホストの検出を追加しました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- `compress`/`compress-level`オプションを、使用しないコマンドから削除しました。これらのコマンド（`restore`、`archive-get`など）は圧縮オプションを使っていませんでしたが、コマンドラインでの指定を許可していました。今後は、これらのオプションをコマンドラインで指定するとエラーになります。このエラーが発生した場合は、使用しないオプションを削除してください。 (*レビュー：Cynthia Shang。*)
- バックアップでコピーするファイルサイズを、バックアップ開始時に報告されたサイズに制限しました。バックアップ中にファイルが増大しても、リカバリー時のWAL再生で再構築されるため、追加データをコピーする必要はありません。 (*レビュー：Cynthia Shang。*)


### v2.24 リリースノート {#v224-release-notes}

*目標時刻に応じたバックアップセットの自動選択*

*2020年2月25日リリース*

**バグ修正：**

- 非同期アーカイブコマンドでゾンビプロセスが発生しないようにしました。 (*レビュー：Stephen Frost。報告：Adam Brusselback, ejberdecia。*)
- `archive-get`/`archive-push`/`restore`をPostgreSQLホスト以外で実行した場合にエラーを出すようにしました。 (*レビュー：Stephen Frost。報告：Jesper St John。*)
- サイズやエンコーディングの指定がない場合に、HTTPコンテンツをeofまで読み込むようにしました。 (*レビュー：Cynthia Shang。報告：Christian ROUX。*)
- Perlで作成されたバックアップを再開する場合の問題を修正しました。この場合、再開可能なバックアップは無視するのが適切ですが、Perlが書いた部分的なマニフェストは形式がわずかに異なり、Cコードでは読み込めませんでした。この状況を検出して正常に処理を続けられるよう、検証を追加しました。 (*報告：Kacey Holston。*)

**新機能：**

- リストア時に目標時刻を指定した場合、バックアップセットを自動選択するようにしました。自動選択を行うのは`--set`を指定していない場合だけです。指定された目標時刻に対応するバックアップセットが見つからない場合は、最新の（デフォルトの）バックアップセットを使用します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- バックアップ時に`pg_internal.init`の一時ファイルを除外するようにしました。 (*レビュー：Cynthia Shang。提案：Michael Paquier。*)
- `backup`でマニフェストに対する検証を追加しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- lock-botがロック済みのissueにコメントを追加しないようにしました。 (*提案：Christoph Berg。*)


### v2.23 リリースノート {#v223-release-notes}

*不具合修正*

*2020年1月27日リリース*

**バグ修正：**

- ファイルの欠落によってマニフェストが破損する問題を修正しました。バックアップ中にPostgreSQLがファイルを削除した場合（またはスタンバイにファイルがなかった場合）、次のファイルがコピーされず、マニフェストも更新されないことがありました。この場合、そのバックアップをリストアするとエラーが発生していました。 (*レビュー：Cynthia Shang。報告：Vitaliy Kukharik。*)

**改善：**

- libxml2のビルドオプションに、`xml2-config`の代わりに`pkg-config`を使用するようにしました。 (*貢献：David Steele, Adrian Vondendriesch。*)
- `backup`/`restore`で、マニフェストにチェックサムが設定されていることを検証するようにしました。 (*レビュー：Cynthia Shang。*)


### v2.22 リリースノート {#v222-release-notes}

*不具合修正*

*2020年1月21日リリース*

**バグ修正：**

- タイムラインの変換エラーを修正しました。タイムラインは、バックアップ後にアーカイブ内のWALセグメントを検証するために必要です。基数`16`ではなく`10`で変換していたため、タイムラインが`0xA`以上になるとエラーが発生していました。 (*報告：Lukas Ertl, Eric Veldhuyzen。*)


### v2.21 リリースノート {#v221-release-notes}

*Cへの移行完了*

*2020年1月15日リリース*

**バグ修正：**

- 非同期コマンドがオプションを無視する問題を修正しました。非同期の`archive-get`/`archive-push`プロセスは、`[global:archive-get]`などのコマンド別設定セクションに設定されたオプションを読み込んでいませんでした。 (*レビュー：Cynthia Shang。報告：Urs Kramer。*)
- ファイル名の`\`の扱いを修正しました。マニフェストのチェックサム計算時に`\`を正しくエスケープしていなかったため、マニフェストを読み込めませんでした。クラスターのファイル名に`\`が含まれることはほぼないと考えられるため、実運用で深刻な問題になる可能性は低そうです。

**新機能：**

- pgBackRestの実装がすべてCになりました。
- `pg-user`オプションを追加しました。PostgreSQLへの接続時のデータベースユーザー名を指定します。指定しない場合、pgBackRestは従来どおりローカルのOSユーザーまたは`PGUSER`を使って接続します。 (*貢献：Mike Palmiotto。レビュー：David Steele。*)
- S3ドライバーでパス形式のURIを使用できるようにしました。

**改善：**

- `backup`コマンドの実装をすべてCに移行しました。 (*レビュー：Cynthia Shang。*)


### v2.20 リリースノート {#v220-release-notes}

*不具合修正*

*2019年12月12日リリース*

**バグ修正：**

- `PGDATA`がシンボリックリンクの場合のarchive-push/archive-getを修正しました。これらのコマンドは`cwd()`を`PGDATA`として使おうとしていましたが、`PGDATA`がシンボリックリンクの場合、pgBackRestに設定したパスと一致しませんでした。`cwd()`がpgBackRestのパスと一致しない場合は、そのパスに`chdir()`して、次の`cwd()`が最初の呼び出し結果と一致することを確認するようにしました。 (*報告：Stephen Frost, Milosz Suchy。*)
- `expire`コマンドで`backup.info`を再構築する際の参照リストを修正しました。`backup`コマンドはまだPerl版の再構築処理を使っているため、この問題が発生するのは、**1)** `backup.info`に記載されていないバックアップがあり、かつ**2)** 通常のように`backup`の後で実行するのではなく、`expire`コマンドを直接実行する場合だけです。この条件が重なることはまれなため、実運用では問題になっていないと思われます。
- gzipの展開中に予期しないEOFが発生するとセグメンテーション違反になる問題を修正しました。 (*報告：Stephen Frost。*)


### v2.19 リリースノート {#v219-release-notes}

*Cへの移行とバグ修正*

*2019年11月12日リリース*

**バグ修正：**

- deltaリストアでリモートがタイムアウトする問題を修正しました。大部分が変更されていないクラスターにdeltaリストアを行う場合、`protocol-timeout`の時間内にリポジトリからファイルを取得しないと、リモートがタイムアウトすることがありました。これを防ぐため、keepaliveを追加しました。 (*報告：James Sewell, Jens Wilke。*)
- 重複したHTTPヘッダーの扱いを修正しました。HTTPヘッダーが繰り返される場合、従来のようにエラーを出すのではなく、カンマで区切られた単一のヘッダーと同等に扱うようにしました。 (*報告：donicrosby。*)

**改善：**

- `info`コマンドのJSON出力を整形しないようにしました。改行のないJSONのほうが、監視システムで容易に取り込めます。必要に応じて、`jq`などの外部ツールで整形できます。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `check`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- pgBackRestへの貢献方法を文書化しました。 (*貢献：Cynthia Shang, David Steele。*)
- `auto-stop`オプションを使用できる最終バージョンを文書化しました。 (*貢献：Brad Nicholson。レビュー：David Steele。*)

**テストスイートの改善：**

- `--vm=none`の場合にもコンテナーテストのパスが使われる問題を修正しました。 (*提案：Stephen Frost。*)
- expectテストでタイムゾーンが一致しない問題を修正しました。 (*提案：Stephen Frost。*)
- デフォルトでは組み込みlibcコードを自動生成しないようにしました。 (*提案：Stephen Frost。*)


### v2.18 リリースノート {#v218-release-notes}

*PostgreSQL 12のサポート*

*2019年10月1日リリース*

**新機能：**

- PostgreSQL 12をサポートしました。
- 詳細なテキスト出力を行うため、`info`コマンドに`set`オプションを追加しました。追加される詳細には、選択的リストアに使用できるデータベース、およびテーブルスペースとシンボリックリンクの一覧と各デフォルトの参照先が含まれます。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Stephen Frost, ejberdecia。*)
- リストアの種類に`standby`を追加しました。PostgreSQL < 12ではrecovery.confにstandby_mode=onを自動追加し、PostgreSQL ≥ 12では`standby.signal`を作成することで、PostgreSQLのバージョンをまたいで共通のインターフェースを提供します。 (*レビュー：Cynthia Shang。*)

**改善：**

- `restore`コマンドの実装をすべてCに移行しました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの改善：**

- `db-timeout`と`protocol-timeout`の関係を文書化しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：James Chanco Jr。*)
- スタンバイのリポジトリに関する説明を明確にしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 時刻に基づくポイントインタイムリカバリーのFAQを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v2.17 リリースノート {#v217-release-notes}

*Cへの移行とバグ修正*

*2019年9月3日リリース*

**バグ修正：**

- テーブルやセグメントが非常に多い場合に、マニフェストの作成が遅くなる問題を改善しました。 (*報告：Jens Wilke。*)
- 特殊ファイルの除外処理を修正しました。 (*報告：CluelessTechnologist, Janis Puris, Rachid Broum。*)

**改善：**

- `stanza-create/update/delete`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `start`/`stop`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- ログディレクトリとログファイルを、それぞれ`0750`/`0640`モードで作成するようにしました。 (*提案：Damiano Albani。*)

**ドキュメントの不具合修正：**

- カスタムパッケージを指定しても`yum.p.o`のパッケージがインストールされる問題を修正しました。 (*報告：Joe Ayers, John Harvey。*)

**ドキュメントの改善：**

- 一般ユーザーでpgBackRestをビルドするようにしました。 (*提案：Laurenz Albe。*)


### v2.16 リリースノート {#v216-release-notes}

*Cへの移行とバグ修正*

*2019年8月5日リリース*

**バグ修正：**

- S3の`RequestTimeTooSkewed`エラーで即時終了せず、再試行するようにしました。 (*報告：sean0101n, Tim Garton, Jesper St John, Aleš Zelený。*)
- `HEAD`リクエストへの応答の`transfer-encoding`を誤って処理する問題を修正しました。 (*報告：Pavel Suderevsky。*)
- gcc 9の最適化で顕在化したスコープ違反を修正しました。 (*報告：Christian Lange, Ned T. Crigler。*)

**新機能：**

- 標準以外のS3サービスポートを設定するため、`repo-s3-port`オプションを追加しました。

**改善：**

- `backup`用の`local`コマンドの実装をすべてCに移行しました。 (*貢献：David Steele, Cynthia Shang。*)
- `check`コマンドの実装を一部Cに移行しました。 (*レビュー：Cynthia Shang。*)


### v2.15 リリースノート {#v215-release-notes}

*expireのC実装*

*2019年6月25日リリース*

**バグ修正：**

- アーカイブの保持処理で過剰に期限切れにしてしまう問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Mohamad El-Rifai。*)

**改善：**

- `expire`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- restore用の`local`コマンドの実装をすべてCに移行しました。
- `$PGUSER`が機能するよう、固定されたPostgreSQLユーザーの指定を削除しました。 (*提案：Julian Zhang, Janis Puris。*)
- configureの`--prefix`オプションを反映するようにしました。 (*提案：Daniel Westermann。*)
- `repo-s3-verify-ssl`オプションを`repo-s3-verify-tls`に改名しました。pgBackRestはいずれのSSLプロトコルバージョンもサポートしていないため（すべて安全でないとみなされています）、新しい名前のほうが適切です。古い名前も引き続き使用できます。

**ドキュメントの改善：**

- ドキュメントにFAQを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL ≥ 9.6のドキュメントで`wal_level=replica`を使用するようにしました。 (*提案：Patrick McLaughlin。*)


### v2.14 リリースノート {#v214-release-notes}

*バグ修正と改善*

*2019年5月20日リリース*

**バグ修正：**

- `archive-push`/`archive-get`で`process-max` > 8の場合にセグメンテーション違反が起きる問題を修正しました。 (*報告：Jens Wilke。*)

**改善：**

- `force`を指定して`stanza-delete`を実行した場合、データベースの確認を省略するようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：hatifnatt。*)
- 複数プラットフォームへの対応を改善するため、`configure`スクリプトを追加しました。

**ドキュメントの機能：**

- CentOS/RHEL 6/7向けのユーザーガイドを追加しました。


### v2.13 リリースノート {#v213-release-notes}

*不具合修正*

*2019年4月18日リリース*

**バグ修正：**

- 長さゼロの読み取りを想定していないI/Oフィルターで、それにより問題が起きる不具合を修正しました。 (*報告：brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru。*)
- `local`/`remote`プロセスからのエラー報告の信頼性に関する問題を修正しました。
- 書き込み、同期、クローズ時にPosix/CIFSのエラーメッセージが誤ったファイル名を報告する問題を修正しました。


### v2.12 リリースノート {#v212-release-notes}

*archive-pushのC実装*

*2019年4月11日リリース*

**重要な注意事項**：新しいTLS/SSL実装では、RFC-2818に従いS3バケット名にドットを使用できません。このセキュリティ修正は、規格に準拠したホスト名の検証に必要です。

**バグ修正：**

- パスオプションが/で終わる場合の問題を修正しました。 (*報告：Marc Cousin。*)
- `archive-get`コマンドに`log-level-file=off`を設定した場合の問題を修正しました。 (*報告：Brad Nicholson。*)
- CコードでもPerlと同様に`host:port`形式のオプションを認識するよう修正しました。 (*報告：Kyle Nevins。*)
- `remote`/`local`コマンドのログオプションの問題を修正しました。

**改善：**

- `archive-push`コマンドの実装をすべてCに移行しました。
- `process-max`の上限を`999`に引き上げました。 (*提案：Rakshitha-BR。*)
- S3バケット名にドットが含まれる場合のエラーメッセージを改善しました。

**ドキュメントの改善：**

- S3互換オブジェクトストアがサポートされることを明確にしました。 (*提案：Magnus Hagander。*)


### v2.11 リリースノート {#v211-release-notes}

*archive-getのC実装*

*2019年3月11日リリース*

**バグ修正：**

- 書き込みの途中でエラーが発生した場合に、WALセグメントが切り詰められる可能性がある問題を修正しました。 (*報告：blogh。*)
- stanzaを指定するとinfoコマンドの出力にWAL min/maxが含まれない問題を修正しました。 (*修正：Stefan Fercot。レビュー：David Steele。*)
- CからPerlへ渡すオプションのJSONが規格に準拠していなかった問題を修正しました。 (*報告：Leo Khomenko。*)

**改善：**

- `archive-get`コマンドの実装をすべてCに移行しました。
- 古いPerlバージョンでソケットのkeepaliveを有効にしました。 (*貢献：Marc Cousin。レビュー：David Steele。*)
- パラメーターを受け付けないコマンドにパラメーターを渡した場合、エラーを出すようにしました。 (*提案：Jason O'Donnell。*)
- アーカイブ内にWALセグメントが見つからない場合のヒントを追加しました。 (*提案：Hans-Jürgen Schönig。*)
- 証明書でホスト名が見つからない場合のエラーを改善しました。 (*提案：James Badger。*)
- デバッグ用に、`backup.manifest`に追加のオプションを記録するようにしました。 (*貢献：blogh。レビュー：David Steele。*)

**ドキュメントの改善：**

- ドキュメントのデフォルトの対象バージョンをPostgreSQL 10に更新しました。


### v2.10 リリースノート {#v210-release-notes}

*不具合修正*

*2019年2月9日リリース*

**バグ修正：**

- `archive-get`に必要な、未実装だったS3ドライバーのメソッドを追加しました。 (*報告：mibiio。*)
- `pg-path`の設定が不正な場合の確認処理を修正しました。 (*報告：James Chanco Jr。*)


### v2.09 リリースノート {#v209-release-notes}

*軽微な改善とバグ修正*

*2019年1月30日リリース*

**バグ修正：**

- 非同期の状態ファイルが複数あると、処理を継続できないエラーになる問題を修正しました。 (*報告：Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley。*)

**改善：**

- `info`コマンドの実装をすべてCに移行しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- stanzaが存在しない場合の`info`コマンドのテキストメッセージを簡潔にしました。リポジトリのパスを「the repository」に置き換えました。
- MacOSビルド用に、Makefileに`_DARWIN_C_SOURCE`フラグを追加しました。 (*貢献：Douglas J Hunley。レビュー：David Steele。*)
- CのTLSクライアントのアドレス検索を、新しい方式を使うよう更新しました。 (*提案：Bruno Friedmann。*)
- `strcasecmp()`と`fd_set`用に、Posix準拠のヘッダーをインクルードしました。 (*提案：ucando。*)

**ドキュメントの不具合修正：**

- リポジトリパスが固定されていた問題を修正しました。 (*報告：Heath Lord。*)

**ドキュメントの改善：**

- 暗号化は常にクライアント側で行うことを明確にしました。 (*提案：Bruce Burdick。*)
- ドキュメント用ホストを構築する例を追加しました。
- マニフェストの変数、リスト、リスト項目で`if`を使用できるようにしました。


### v2.08 リリースノート {#v208-release-notes}

*軽微な改善とバグ修正*

*2019年1月2日リリース*

**バグ修正：**

- S3オブジェクトの格納直後に、その情報を要求する処理を削除しました。 (*報告：Matt Kunkel。*)
- `archive-get-queue-max`を`size`型に修正しました。 (*報告：Ronan Dunklau。*)
- 現在のユーザーの`uid`/`gid`に対応する名前がない場合のエラーメッセージを追加しました。 (*報告：Camilo Aguilar。*)
- PostgreSQL < 9.5で`--target-action=shutdown`を指定した場合にエラーを出すようにしました。

**改善：**

- S3接続にTCP keepaliveを設定しました。 (*提案：Ronan Dunklau。*)
- 最新のバックアップを最後に表示するよう、`info`コマンドのテキスト出力の順序を変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Ryan Lambert。*)
- 必要な場合だけファイルの所有権を変更するようにしました。
- S3エラーを出す際に`authentication`ヘッダーをマスクするようにしました。 (*提案：Brad Nicholson。*)

**ドキュメントの改善：**

- `target-action`が有効になる条件と、PostgreSQLバージョンごとの対応を明確にしました。 (*提案：Keith Fiske。*)
- バケットに合わせてリージョンとエンドポイントを正しく設定する必要があることを明確にしました。 (*提案：Pritam Barhate。*)
- ドキュメントのビルド方法を文書化しました。


### v2.07 リリースノート {#v207-release-notes}

*バックアップのチェックサムによる差分判定の自動化*

*2018年11月16日リリース*

**バグ修正：**

- 接続エラー時に`archive-push-queue-max`が守られない問題を修正しました。 (*報告：Lardière Sébastien。*)
- `archive-push-queue-max`を超えたかどうかの判定に固定のWALセグメントサイズを使っていた問題を修正しました。
- ログファイルを開けなかった後、処理を続けるべき場合にもエラーになる問題を修正しました。 (*報告：vthriller。*)

**新機能：**

- タイムラインの切り替えなどの異常を検出した場合に、バックアップのチェックサムによる差分判定を自動で有効にするようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- S3の内部エラー`500`だけでなく、すべての`5xx`エラーを再試行するようにしました。 (*提案：Craig A. James。*)


### v2.06 リリースノート {#v206-release-notes}

*チェックサムによる差分判定を使うバックアップとPostgreSQL 11のサポート*

*2018年10月15日リリース*

**バグ修正：**

- S3ドライバーでURIのエンコーディングが欠けていた問題を修正しました。 (*報告：Dan Farrell。*)
- 設定ファイルにオプションが重複した場合のエラーメッセージが誤っていた問題を修正しました。 (*報告：Jesper St John。*)
- `info`レベルのログで、戻り値を誤ってエラーとして報告する問題を修正しました。`archive-get`の戻りコード1が、動作自体は正常であるにもかかわらず、`info`レベルでエラーメッセージとして記録されていました。

**新機能：**

- 増分バックアップに、チェックサムによる差分判定を追加しました。この方式では、タイムスタンプではなくチェックサムを使ってファイルが変更されたかどうかを判断します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- WALセグメントサイズの設定を含め、PostgreSQL 11をサポートしました。

**改善：**

- リンク先のテーブルスペースディレクトリでは、現在のPostgreSQLバージョンのサブディレクトリ以外の全ファイルを無視するようにしました。従来は、ほかのファイルが存在し、その所有者がPostgreSQLユーザーでない場合にエラーが発生していました。
- stanzaの暗号方式を表示するよう、`info`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Douglas J Hunley。*)
- ファイル名の特殊文字への対応を改善しました。
- pgBackRestの設定ファイルで`delta`オプションを指定できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- SSHのセキュリティを高めるため、`authorized_hosts`で`command`を使用するようにしました。 (*提案：Stephen Frost, Magnus Hagander。*)
- 設定リファレンスに、`buffer-size`オプションで指定可能な値を記載しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Stéphane Schildknecht。*)


### v2.05 リリースノート {#v205-release-notes}

*環境変数によるオプション設定と、一時リレーションおよび非ログリレーションの除外*

*2018年8月31日リリース*

**バグ修正：**

- `$PGDATA`内の*相対*リンクが、誤ったパスでバックアップに保存されることがある問題を修正しました。絶対リンクには影響せず、テーブルスペースの相対リンクはほかのチェックで検出されていました。 (*報告：Cynthia Shang。*)
- 不完全な実装だった`online`オプションを`check`コマンドから削除しました。オフライン動作は、アーカイブとバックアップが正しく機能しているかを確認するという、このコマンドの目的に反します。 (*報告：Jason O'Donnell。*)
- Perlから呼び出した際、Cで発生したエラーがログに記録されない問題を修正しました。pgBackRestは正しいエラーコードで終了していましたが、デバッグに役立つエラーメッセージがありませんでした。 (*報告：Douglas J Hunley。*)
- 真偽値のオプション（例：`delta`）を複数回指定した場合の問題を修正しました。 (*報告：Yogesh Sharma。*)

**新機能：**

- すべてのオプションを環境変数で設定できるようにしました。従来はコマンドラインでしか指定できなかった`stanza`などのオプションや、コマンドラインでは指定できなかった`repo1-s3-key-secret`などの機密オプションも含まれます。
- 一時リレーションと非ログリレーション（テーブルとインデックス）のファイルを、バックアップから除外するようにしました。PostgreSQLに同機能を追加したパッチ[8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25)および[920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f)と同じロジックで実装しています。一時リレーションの除外はPostgreSQL ≥ `9.0`で有効です。非ログリレーションの除外は、この機能が導入されたPostgreSQL ≥ `9.1`で有効です。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 任意のディレクトリやファイルをバックアップから除外できるようにしました。この機能の誤用はバックアップの不整合につながるため、使用前に`--exclude`のドキュメントをよく読んでください。 (*レビュー：Cynthia Shang。*)
- `local`と`remote`サブプロセスのファイルへのログ出力を可能にする、`log-subprocess`オプションを追加しました。
- PostgreSQL 11 Beta 3をサポートしました。

**改善：**

- バックアップマニフェスト内のサイズゼロのファイルは、タイムスタンプの差にかかわらず前のマニフェストを参照できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 状態ファイルを直接確認することで、非同期の`archive-get`/`archive-push`の性能を改善しました。 (*貢献：Stephen Frost。レビュー：David Steele。*)
- コマンドに`stanza`オプションがない場合のエラーメッセージを改善しました。 (*提案：Sarah Conway。*)

**ドキュメントの不具合修正：**

- `log-path`オプションのリファレンスに記載された、不正なログレベルを修正しました。 (*報告：Camilo Aguilar。*)

**ドキュメントの改善：**

- `release.xml`で貢献者を姓と名で整理するのをやめました。リリースノートでは、貢献者の名前は常に提供されたとおりに表記してきましたが、内部IDは姓と名に基づいて割り当てようとしていました。姓と名の判別は難しい場合があり、そもそも適切な方法ではありません。ChristopheのPostgresOpen 2017での講演「人間に主キーはない」に着想を得ています。 (*提案：Christophe Pettus。*)

**テストスイートの改善：**

- テスト環境の外でLibCをビルドした場合にエラーを出すようにしました。本番用のビルドにLibCは不要になりました。


### v2.04 リリースノート {#v204-release-notes}

*バックアップの再開に関する重大な不具合修正*

*2018年7月5日リリース*

**重要な注意事項**：このリリースでは、バックアップの再開機能に関する重大な不具合を修正しています。このリリースより前に再開したバックアップは、すべて整合性がないものと見なすことを推奨します。`resume=n`を指定していない限り、前回のバックアップが失敗すると、そのバックアップを再開します。再開したバックアップは、バックアップログにメッセージ"aborted backup of same type exists, will be cleaned to remove invalid files and resumed"があるかどうかで判別できます。このメッセージがある場合、そのバックアップも、同じセット内のほかのバックアップもリストアに使用しないでください。また、リストアログを確認し、再開したバックアップをリストアしていないか調べてください。該当する場合、クラスター内のデータに不整合がある可能性があります。

**バグ修正：**

- 再開時に整合性のないバックアップが作成される重大な不具合を修正しました。`v0.82`でのリグレッションにより、再開時に中断済みバックアップのどのファイルを保持するかを判断する際のタイムスタンプ比較が失われていました。詳細は上記の注意事項を参照してください。 (*報告：David Youatt, Yogesh Sharma, Stephen Frost。*)
- クラスター内のユーザーデータベースが1つだけの場合、選択的リストアでエラーになる問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Nj Baliyan。*)
- S3認証ヘッダーのタイムスタンプがISO-8601に準拠していなかった問題を修正しました。AWSと一部のゲートウェイは、時のゼロ埋めを空白にしても受け付けていましたが、他のゲートウェイは受け付けていませんでした。 (*修正：Andrew Schwartz。レビュー：David Steele。*)

**新機能：**

- PostgreSQL 11 Beta 2をサポートしました。

**改善：**

- サーバーが`content-length`を指定しない場合、0に設定するようHTTPクライアントを改善しました。S3とそのゲートウェイは常に`content-length`または`transfer-encoding`を設定しますが、`HTTP 1.1`では必須ではなく、HAProxyなどのプロキシがどちらも含めない場合があります。 (*提案：Adam K. Sumner。*)
- PostgreSQL接続で`search_path = 'pg_catalog'`を設定するようにしました。 (*提案：Stephen Frost。*)

**ドキュメントの改善：**

- pgBackRestのビルド方法を説明するセクションを新設し、別のホストでビルドするようにしました。
- バケットの権限を制限するS3ポリシーの例を追加しました。 (*提案：Douglas J Hunley, Jason O'Donnell。*)


### v2.03 リリースノート {#v203-release-notes}

*単一の実行ファイルによる配置*

*2018年5月22日リリース*

**バグ修正：**

- エラーメッセージの処理でバッファーオーバーランが起きる可能性を修正しました。 (*報告：Lætitia。*)
- 同期の`archive-get`コマンドでアーカイブの書き込みロックを取得していた問題を修正しました。 (*報告：uspen。*)

**改善：**

- エクスポートするC関数とPerlモジュールを、pgBackRestの実行ファイルに直接組み込みました。
- 移植性を高めるため、`__time_t`の代わりに`time_t`を使用するようにしました。 (*提案：Nick Floersch。*)
- コマンド終了時に、総実行時間をミリ秒単位で表示するようにしました。


### v2.02 リリースノート {#v202-release-notes}

*並列の非同期archive-getと設定ファイルのインクルード*

*2018年5月6日リリース*

**バグ修正：**

- 指定されたディレクトリだけを同期すべき場面で、再帰的にディレクトリを同期していた問題を修正しました。 (*報告：Craig A. James。*)
- incr/diffバックアップで`archive-copy`が"path not found"エラーを発生させる問題を修正しました。 (*報告：yummyliu, Vitaliy Kukharik。*)
- `PGDATA`内の2つ以上のファイルが同じディレクトリへのリンクである場合、マニフェストの作成に失敗する問題を修正しました。 (*報告：Vitaliy Kukharik。*)
- リンク先のファイルがない場合にdeltaリストアが失敗する問題を修正しました。
- ヘルプでのキーと値のペアおよびリスト形式のオプションの表示を修正しました。 (*報告：Clinton Adams。*)

**新機能：**

- 非同期かつ並列の`archive-get`を追加しました。WALセグメントのキューを維持することで、PostgreSQLがrestore_commandでWALセグメントを要求する際の遅延を減らします。
- 追加のpgBackRest設定ファイルをサポートしました。ディレクトリは`--config-include-path`オプションで指定します。`--config`と`--config-include-path`オプションのデフォルトのベースパスを上書きするため、`--config-path`オプションを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 一時認証情報のトークンを設定できるよう、`repo-s3-token`オプションを追加しました。pgBackRestには現時点で新しい認証情報を要求する手段がないため、認証情報の有効期限が切れる前に、コマンド全体（`backup`、`restore`など）が完了する必要があります。 (*貢献：Yogesh Sharma。レビュー：David Steele。*)

**改善：**

- `archive-push-queue-max`、`manifest-save-threshold`、`buffer-size`オプションで、`KB`、`MB`、`GB`、`TB`、`PB`単位の値を指定できるようにしました。倍率には`1024`の累乗を使います。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- バックアップとリストアのパスの同期を効率化しました。小さなテーブルが多数ある場合、ディレクトリ全体の走査には大きなコストがかかります。バックアップとリストアのパスを走査する代わりに、バックアップマニフェストに含まれるパス一覧を使って同期するようにしました。
- 最初のinfoログメッセージに、コマンドオプションだけでなくコマンドパラメーターも表示するようにしました。
- archive-queue-maxオプションをarchive-push-queue-maxに改名しました。新しい`archive-get-queue-max`オプションと一貫した命名になります。古いオプション名も引き続き使用できます。

**ドキュメントの不具合修正：**

- 32ビットのサポートと注意事項をドキュメントに追加しました。32ビットのサポートはv1.26で追加されています。 (*報告：Viorel Tabara。*)

**ドキュメントの改善：**

- PostgreSQLとjqを使った監視の例を追加しました。 (*提案：Stephen Frost, Brian Faherty。*)
- アーカイブ設定にコマンド別セクションの使用例を追加しました。 (*提案：Christophe Courtois。*)
- `info --output=json`を実験的機能とする記述を削除しました。
- `spool-path`オプションの古い説明を更新しました。

**テストスイートの機能：**

- Cのユニットテストのカバレッジ報告にlcovを使用するようにしました。Devel::Coverはgcovから変換したレポートの分岐カバレッジを報告しないため、切り替えました。モジュールの分岐カバレッジが不完全な場合はエラーになります。ユニットテスト自体のカバレッジは、ステートメントまたは分岐のカバレッジが不完全な場合を除き、レポートに表示しません。


### v2.01 リリースノート {#v201-release-notes}

*軽微なバグ修正と改善*

*2018年3月19日リリース*

**バグ修正：**

- `--type=immediate`でのリストア時に、`--target-action`と`--recovery-option`が無効なオプションと報告される問題を修正しました。 (*報告：Brad Nicholson。*)
- 機密オプション（例：`repo1-s3-key`）をコマンドラインで渡した場合、直ちにエラーを出すようにしました。pgBackRestは機密オプションをサブプロセスに渡さないため、以前は分かりにくいエラーが発生していました。新しいエラーははるかに明確で、問題を解決するためのヒントも示します。コマンドラインで指定できない機密オプションは記載しないよう、コマンドのドキュメントも更新しました。 (*報告：Brad Nicholson。*)
- 組み込みPerlに`--no-config`を渡す際の問題を修正しました。 (*報告：Ibrahim Edib Kokdemir。*)
- `log-level-stderr` > `warn`を指定すると、本来出力されないはずのstderrへの出力が検出され、`local`/`remote`プロセスが終了時にエラーになる問題を修正しました。これらのプロセスが警告を出す理由はないため、`local`/`remote`プロセスでの最大値は`error`になりました。 (*報告：Clinton Adams。*)
- テーブルスペースが存在する場合の、`check`コマンドのマニフェストテストを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Thomas Flatley。*)

**改善：**

- 複数の引数を受け付けないオプションに、設定ファイルで複数の引数を設定した場合はエラーを出すようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `src/Makefile`から不要なsudoコマンドを削除しました。 (*貢献：Adrian Vondendriesch。レビュー：David Steele。*)

**ドキュメントの改善：**

- インデックス付きオプション（`repo-*`、`pg-*`）の例に、インデックスを表示するようにしました。 (*提案：Stephen Frost。*)
- コマンドページの目次を、コマンドだけを列挙する簡潔なものにしました。 (*提案：Stephen Frost。*)
- Cライブラリが任意であるという記述を削除しました。

**テストスイートの機能：**

- CentOS/RHELパッケージのビルドを追加しました。
- 静的コード解析にclangを使用するようにしました。初回には、`__noreturn__`を付けるべきだった一部の関数以外に問題は見つかりませんでした。


### v2.00 リリースノート {#v200-release-notes}

*archive-pushの性能改善*

*2018年2月23日リリース*

**新機能：**

- `archive-push`コマンドの一部をCで実装しました。これにより、PostgreSQLの`archive_command`が非同期アーカイブプロセスからの状態メッセージを処理する際、大幅に高速化されます。 (*レビュー：Cynthia Shang。*)

**改善：**

- バックアップマニフェストを作成できることを検証するよう、`check`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- HTTPSクライアントの性能を改善しました。バッファリング時に`select()`だけに依存せず、ソケットの`pending`バイトがあれば考慮するようにしました。場合によっては、接続を閉じるまで最後のバイトがフラッシュされないことがありました。
- S3の削除性能を改善しました。おそらくテスト中に、定数`S3_BATCH_MAX`がハードコードされた値2に置き換えられていました。
- コマンドライン専用ではないすべてのオプションを、コマンドラインでデフォルト値に戻せるようにしました。`pgbackrest.conf`内のオプションをデフォルト値に戻せるため、特定の用途のために新しい設定ファイルを書く必要性が減ります。
- Cライブラリを必須にしました。これにより条件付きの読み込みが不要になり、新しいライブラリ機能を開発しやすくなります。
- `pgbackrest`実行ファイルをPerlからCバイナリーに変更しました。これにより、非同期`archive-push`など、実行時間が重要なコマンドを高速化できます。
- 一貫性を高めるため、`db-*`オプションを`pg-*`に、`backup-*`オプションを`repo-*`に変更しました。`repo-*`オプションにインデックスを付けるようになりましたが、現時点で指定できるのは1つだけです。

**ドキュメントの機能：**

- ドキュメント内のすべてのクラスターを、チェックサムを有効にして初期化するようにしました。

**ドキュメントの改善：**

- ドキュメントとコマンドラインヘルプに、非推奨のオプション名を列挙するようにしました。
- S3バケットはユーザーが作成する必要があることを明記しました。 (*提案：David Youatt。*)


### v1.29リリースノート {#v129-release-notes}

*バックアップの再開に関する重大な不具合修正*

*2018年7月5日リリース*

**重要な注意事項**：このリリースでは、バックアップの再開機能に関する重大な不具合を修正しています。このリリースより前に再開したバックアップは、すべて整合性がないものと見なすことを推奨します。`resume=n`を指定していない限り、前回のバックアップが失敗すると、そのバックアップを再開します。再開したバックアップは、バックアップログにメッセージ"aborted backup of same type exists, will be cleaned to remove invalid files and resumed"があるかどうかで判別できます。このメッセージがある場合、そのバックアップも、同じセット内のほかのバックアップもリストアに使用しないでください。また、リストアログを確認し、再開したバックアップをリストアしていないか調べてください。該当する場合、クラスター内のデータに不整合がある可能性があります。

**バグ修正：**

- 再開時に整合性のないバックアップが作成される重大な不具合を修正しました。`v0.82`でのリグレッションにより、再開時に中断済みバックアップのどのファイルを保持するかを判断する際のタイムスタンプ比較が失われていました。詳細は上記の注意事項を参照してください。 (*報告：David Youatt, Yogesh Sharma, Stephen Frost。*)
- S3認証ヘッダーのタイムスタンプがISO-8601に準拠していなかった問題を修正しました。AWSと一部のゲートウェイは、時のゼロ埋めを空白にしても受け付けていましたが、他のゲートウェイは受け付けていませんでした。 (*修正：Andrew Schwartz。レビュー：David Steele。*)
- 指定されたディレクトリだけを同期すべき場面で、再帰的にディレクトリを同期していた問題を修正しました。 (*報告：Craig A. James。*)
- `--type=immediate`でのリストア時に、`--target-action`と`--recovery-option`が無効なオプションと報告される問題を修正しました。 (*報告：Brad Nicholson。*)
- incr/diffバックアップで`archive-copy`が"path not found"エラーを発生させる問題を修正しました。 (*報告：yummyliu, Vitaliy Kukharik。*)
- `PGDATA`内の2つ以上のファイルが同じディレクトリへのリンクである場合、マニフェストの作成に失敗する問題を修正しました。 (*報告：Vitaliy Kukharik。*)
- リンクされたファイルが存在しない場合、差分リストアが失敗する問題を修正しました。
- クラスター内のユーザーデータベースが1つだけの場合、選択的リストアでエラーになる問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Nj Baliyan。*)

**改善：**

- サーバーが`content-length`を指定しない場合、0に設定するようHTTPクライアントを改善しました。S3とそのゲートウェイは常に`content-length`または`transfer-encoding`を設定しますが、`HTTP 1.1`では必須ではなく、HAProxyなどのプロキシがどちらも含めない場合があります。 (*提案：Adam K. Sumner。*)
- HTTPSクライアントの性能を改善しました。バッファリング時に`select()`だけに依存せず、ソケットの`pending`バイトがあれば考慮するようにしました。場合によっては、接続を閉じるまで最後のバイトがフラッシュされないことがありました。
- S3の削除性能を改善しました。おそらくテスト中に、定数`S3_BATCH_MAX`がハードコードされた値2に置き換えられていました。
- バックアップ／リストア時のパスの同期を効率化しました。小さなテーブルが多い場合、ディレクトリ全体の走査は大きな負荷になります。バックアップマニフェストにはパスの一覧が含まれるため、バックアップ／リストア先のパスを走査せず、その一覧を使って同期します。使われなくなった再帰的なパス同期機能を削除しました。

**ドキュメントの不具合修正：**

- 32ビットのサポートと注意事項をドキュメントに追加しました。32ビットのサポートはv1.26で追加されています。 (*報告：Viorel Tabara。*)

**ドキュメントの改善：**

- S3バケットはユーザーが作成する必要があることを明記しました。 (*提案：David Youatt。*)
- `spool-path`オプションの古い説明を更新しました。


### v1.28リリースノート {#v128-release-notes}

*stanzaの削除*

*2018年2月1日リリース*

**バグ修正：**

- --db-includeを使って、テーブルスペース内の単一データベースをリストアできない問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Chiranjeevi Ravilla。*)
- `archive.info`と`backup.info`を照合するとき、最新の`db-id`を確実に選択するようにしました。これにより、`system-id`と`db-version`が重複している場合（`pg_upgrade`を元に戻した後など）にも正しく照合できます。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Adam K. Sumner。*)
- 無効なコマンドを報告する際のエラーメッセージが冗長すぎる問題を修正しました。 (*報告：Jason O'Donnell。*)

**新機能：**

- 使用していないstanzaを削除する`stanza-delete`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Magnus Hagander。*)

**改善：**

- stanzaがすでに存在していてもエラーにならないよう、`stanza-create`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- `stanza-create --force`のドキュメントを更新し、使用時に注意するよう促しました。 (*提案：Jason O'Donnell。*)


### v1.27リリースノート {#v127-release-notes}

*不具合修正とドキュメント*

*2017年12月19日リリース*

**バグ修正：**

- `backup`と`restore`で実行場所のエラーが抑制されていた問題を修正しました。バックアップホストがある場合、リモートホストを無視する別の設定を用意しない限り、バックアップはバックアップホストでのみ、リストアはデータベースホストでのみ許可する必要があります。 (*報告：Lardière Sébastien。*)
- PostgreSQL 10でWALの期限切れ処理が行われない問題を修正しました。PostgreSQLのすべてのメジャーバージョンがX.X形式であると想定した、誤った正規表現が原因でした。 (*報告：Adam Brusselback。*)
- `--no-config`オプションが子プロセスに渡されない問題を修正しました。子プロセスがローカルの設定ファイルを読み込んでしまい、予期しない動作を引き起こす可能性がありました。
- クラスターの旧バージョンのバックアップもアーカイブも存在しない場合、`"db (prior)"`を出力しないよう`info`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Stephen Frost。*)

**ドキュメントの機能：**

- `archive-copy`と`archive-check`の関係を説明しました。 (*提案：Markus Nullmeier。*)
- `archive-copy`のリファレンスドキュメントを改善しました。


### v1.26リリースノート {#v126-release-notes}

*リポジトリの暗号化*

*2017年11月21日リリース*

**バグ修正：**

- リストア時に、大きなマニフェストのコピーが失敗する場合がある問題を修正しました。 (*報告：Craig A. James。*)
- 32ビットアーキテクチャでWALオフセットが誤っていた問題を修正しました。 (*修正：Javier Wilson。レビュー：David Steele。*)
- 旧バージョンのデータベースのWALを取得する際の問題を修正しました。`stanza-upgrade`の後も、旧バージョンのバックアップをリストアし、`archive-get`でリカバリーできるはずですが、archive-getは最新のdbバージョン／IDしか確認せず、失敗していました。また、同じdbバージョン／IDが履歴に複数回現れる場合の問題も修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Clinton Adams。*)
- バックアップ時の無効なグループを、リストア時に正しく設定できない問題を修正しました。バックアップ時にグループを名前に対応付けられない場合、マニフェストにグループを`false`として保存し、リストア時には$PGDATAの所有者、これが使えなければ現在のユーザーのグループを使ってグループを設定します。この処理が正しく動作せず、選択したグループでユーザーを上書きしていたため、グループが未定義のままになり、ユーザーが誤ってグループに設定されていました。 (*報告：Jeff McCormick。*)
- リモートへのパラメーターの受け渡しを修正しました。複数のdbを指定した場合、実際に対象としているdbにかかわらず、db1のパス、ポート、ソケットパスを渡していました。 (*報告：uspen。*)

**新機能：**

- リポジトリの暗号化をサポートしました。 (*貢献：Cynthia Shang, David Steele。*)

**改善：**

- `--compress-level-network=0`の場合、gzipフィルターを無効にしました。従来は圧縮レベル0でフィルターを使用しており、利点のない負荷が生じていました。
- gzipフィルターの展開性能を改善しました。

**ドキュメントの機能：**

- issueの報告時に最初に収集する情報を充実させるため、テンプレートを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- `archive-timeout`の使い方を明確にし、PostgreSQLのarchive_timeout設定との違いを説明しました。 (*貢献：Cynthia Shang。レビュー：David Steele。提案：Keith Fiske。*)

**テストスイートの機能：**

- 32ビットのi386/i686アーキテクチャ向け自動テストを追加しました。


### v1.25リリースノート {#v125-release-notes}

*S3の性能改善*

*2017年10月24日リリース*

**バグ修正：**

- `compress-level`オプションのカスタム設定が無視される問題を修正しました。 (*報告：Jens Wilke。*)
- タイムラインの重複を検出した場合のエラーを削除しました。タイムラインの重複は、多くのポイントインタイムリカバリー（PITR）で有効な状態です。 (*報告：blogh。*)
- JSON形式のinfo出力で、`database-id`が整数として出力されない場合がある問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。報告：Jason O'Donnell。*)

**新機能：**

- S3での一覧取得リクエストの性能を改善しました。フィルター式の先頭にリテラル部分がある場合、そこから検索用プレフィックスを生成します。これにより、レート制限を回避できる程度にリクエストを小さく抑えられることが多くなります。 (*提案：Mihail Shvein。*)

**テストスイートの機能：**

- I/O性能テストを追加しました。


### v1.24リリースノート {#v124-release-notes}

*バックアップから除外する項目の追加*

*2017年9月28日リリース*

**バグ修正：**

- スタンバイからのバックアップの初期化中に、低い優先度のログメッセージではなく警告が出力される問題を修正しました。 (*報告：uspen。*)
- 一部の`db-*`オプション（`db-port`など）がリモートに渡されない問題を修正しました。 (*報告：uspen。*)

**新機能：**

- 起動時に再構築されるため、`pg_snapshots`、`pg_serial`、`pg_notify`、`pg_dynshmem`の内容をバックアップから除外しました。
- 起動時に再構築されるため、`pg_internal.init`ファイルをバックアップから除外しました。

**改善：**

- メインプロセスも同じファイルにログを書き込むことを防ぐため、非同期プロセスがメインプロセスから完全に分離された後にログファイルを開くようにしました。 (*提案：Jens Wilke。*)

**ドキュメントの機能：**

- パスワード不要のSSH設定を追加しました。

**ドキュメントの改善：**

- PostgreSQLの慣例に合わせ、ドキュメント内のmasterをprimaryに変更しました。


### v1.23リリースノート {#v123-release-notes}

*複数のスタンバイとPostgreSQL 10のサポート*

*2017年9月3日リリース*

**バグ修正：**

- サイズが増加中のファイルで、圧縮が中止される場合がある問題を修正しました。 (*報告：Jesper St John, Aleksandr Rogozin。*)
- ローカルプロセスからリモートにキープアライブが送信されない問題を修正しました。 (*報告：William Cox。*)

**新機能：**

- スタンバイからのバックアップ用に、最大7つのスタンバイを設定できるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL 10をサポートしました。
- サードパーティーのS3ゲートウェイとの互換性を高めるため、XMLデータの読み取り時にチャンク転送に加えて`content-length`も使えるようにしました。 (*提案：Victor Gdalevich。*)

**改善：**

- S3向けのHTTPタイムアウトを延長しました。
- 一時的なS3ネットワークエラーへの耐性を高めるため、HTTPの再試行を追加しました。

**ドキュメントの不具合修正：**

- 設定ページに各セクションの概要が含まれるよう、ドキュメント生成を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)


### v1.22リリースノート {#v122-release-notes}

*S3の再試行の修正*

*2017年8月9日リリース*

**バグ修正：**

- S3の再試行時の認証問題を修正しました。


### v1.21リリースノート {#v121-release-notes}

*info出力の改善とSSHポートオプション*

*2017年8月8日リリース*

**バグ修正：**

- 新しいバージョンのように`archive_status`ディレクトリを自動再作成しないPostgreSQL 8.3に対応するため、リストア時にこのディレクトリを再作成するようにしました。 (*報告：Stephen Frost。*)
- `stanza-upgrade`後に、旧バージョンのPostgreSQLの空のアーカイブディレクトリが残る場合がある問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- `info`コマンドのテキスト出力とJSON出力を変更しました。現在のデータベースクラスターのバージョンと、存在する場合は以前のバージョンについて、アーカイブID、および現在アーカイブに存在する最小／最大のWALを表示します。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- デフォルト以外のSSHポートをサポートするため、`--backup-ssh-port`と`--db-ssh-port`を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- S3が内部エラー（500）を返した場合に再試行するようにしました。

**ドキュメントの不具合修正：**

- コマンドの文脈に応じて、`--online`の説明を修正しました。

**ドキュメントの機能：**

- 手動インストールの手順に、`/etc/pgbackrest.conf`の作成を追加しました。

**ドキュメントの改善：**

- コマンドリファレンスとコマンドラインヘルプで、リポジトリのオプションを独立したセクションに移しました。 (*提案：Stephen Frost。*)


### v1.20リリースノート {#v120-release-notes}

*8.3/8.4の重大な不具合修正*

*2017年6月27日リリース*

**重要な注意事項**：PostgreSQL 8.3および8.4でテーブルスペースを利用している環境では、どのv1リリースからでも直ちにアップグレードし、フルバックアップを実行することを推奨します。これらのバージョンに限り、不具合によってテーブルスペースがバックアップされていませんでした。PostgreSQL ≥ 9.0 はこの問題の影響を受けません。

**バグ修正：**

- PostgreSQL ≤ 8.4でテーブルスペースがバックアップされない問題を修正しました。
- Cライブラリのビルドでフラグが欠けていたため、32ビットシステムで不適合なバイナリーが生成される問題を修正しました。 (*報告：Adrian Vondendriesch。*)

**新機能：**

- `IO::Socket::SSL`がCAを自動検出できないシステム（RHEL7など）に対応し、またカスタムCAを読み込めるよう、`s3-repo-ca-path`と`s3-repo-ca-file`を追加しました。 (*提案：Scott Frazer。*)

**テストスイートの機能：**

- CIにドキュメントのビルドを追加しました。


### v1.19リリースノート {#v119-release-notes}

*S3のサポート*

*2017年6月12日リリース*

**バグ修正：**

- 現在のデータベースバージョンのWALアーカイブの最小／最大を表示するよう、`info`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- スタンバイが未設定、または接続できない場合、`backup-standby`オプションをリセットし、プライマリーでバックアップを続行するよう`backup`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- リモートプロセスが出す設定警告によって、マスタープロセスでエラーが発生する問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- Amazon S3リポジトリをサポートしました。 (*レビュー：Cynthia Shang。*)

**ドキュメントの不具合修正：**

- 設定リファレンスに記載されていた無効な`max-archive-mb`オプションを、`archive-queue-max`に変更しました。
- インストールのセクションで欠けていた`sudo`を追加しました。 (*修正：Lætitia。レビュー：David Steele。*)


### v1.18リリースノート {#v118-release-notes}

*stanzaのアップグレード、リファクタリング、ロックの改善*

*2017年4月12日リリース*

**バグ修正：**

- ローカルのワーカープロセスを使う読み取り専用操作（`restore`など）が書き込みロックを取得し、並列`archive-push`を妨げる場合がある問題を修正しました。 (*報告：Jens Wilke。*)

**新機能：**

- PostgreSQLを新しいメジャーバージョンにアップグレードした後にstanzaを更新できる、stanza-upgradeコマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `pgbackrest.conf`を検証し、オプションが無効な場合や正しいセクションにない場合に警告を表示するようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- ロックの仕組みを簡素化しました。以前のようにすべてのローカルおよびリモートのワーカープロセスが書き込みロックを取得するのではなく、マスタープロセスのみが`archive-push`と`backup`の書き込みロックを保持するようになりました。
- バックアップディレクトリ内のファイルのタイムスタンプを、クラスター内のファイルに合わせて設定しなくなりました。元はバックアップの再開のために必要でしたが、現在の再開処理はチェックサムを使って実装されています。
- `restore`コマンドが`postmaster.pid`の存在を検出した場合のエラーメッセージを改善しました。 (*提案：Yogesh Sharma。*)
- PostgreSQLが一部の戻りコードを致命的なシグナル例外と解釈しないよう、戻りコードを25から125の範囲に振り直しました。 (*提案：Yogesh Sharma。*)


### v1.17リリースノート {#v117-release-notes}

*ページチェックサムの不具合修正*

*2017年3月13日リリース*

**バグ修正：**

- 初期化されたばかりで未使用のページが、ページチェックサムの警告を発生させる問題を修正しました。 (*報告：Stephen Frost。*)


### v1.16リリースノート {#v116-release-notes}

*ページチェックサムの改善、CI、パッケージのテスト*

*2017年3月2日リリース*

**バグ修正：**

- 1GBを超えるテーブルで、最初のセグメントより後にページチェックサムの警告が出る問題を修正しました。 (*報告：Stephen Frost。*)
- デフォルト以外のテーブルスペースに作成したデータベースで、`pg_filenode.map`と`pg_internal.init`がページ境界に整列していないという誤った警告が出る問題を修正しました。 (*報告：blogh。*)

**テストスイートの機能：**

- `travis-ci`を使った継続的インテグレーションを導入しました。
- サポート対象のすべてのディストリビューション向けに、Debianパッケージを自動ビルドするようにしました。


### v1.15リリースノート {#v115-release-notes}

*リファクタリングと不具合修正*

*2017年2月13日リリース*

**バグ修正：**

- マニフェスト作成中にファイルが削除されると（テーブルを削除した場合など）、バックアップが失敗する場合がある、v1.13で導入されたリグレッションを修正しました。 (*報告：Navid Golpayegani。*)


### v1.14リリースノート {#v114-release-notes}

*リファクタリングと不具合修正*

*2017年2月13日リリース*

**バグ修正：**

- archive-pushでエラーが発生しても再試行せず、`.error`ファイルを手動削除しない限り、PostgreSQLにエラーを返し続ける問題を修正しました。 (*報告：Jens Wilke。*)
- 並列アーカイブで複数のプロセスが同時に新しいパスを作成しようとするとエラーになる競合状態を修正しました。 (*報告：Jens Wilke。*)

**改善：**

- `info`コマンドが提供する`wal archive min/max`の性能を改善しました。 (*提案：Jens Wilke。*)

**ドキュメントの機能：**

- 非同期アーカイブのドキュメントを更新し、新しい方式の動作と旧方式との違いをより正確に説明しました。 (*提案：Jens Wilke。*)


### v1.13リリースノート {#v113-release-notes}

*並列アーカイブ、stanzaの作成、infoとcheckの改善*

*2017年2月5日リリース*

**重要な注意事項**：非同期アーカイブの新しい実装では、WALを別のキューにコピーしなくなりました。`1.13`へのアップグレード後に古いキューに残ったWALは処理されずに残り、リポジトリに送信**されません**。これを防ぐには、`archive_command = false`を設定してアーカイブを停止してください。次に`pgbackrest --stanza=[stanza-name] archive-push`を実行して非同期キューを空にし、処理の完了を待ちます。`[spool-path]/archive/[stanza-name]/out`のキューが空であることを確認してください。最後に`1.13`をインストールし、元の`archive_command`を復元します。**重要な注意事項**：`stanza-create`コマンドは任意ではなくなりました。**新しい**stanzaでバックアップまたはアーカイブを行う前に、必ず実行する必要があります。既存のstanzaで`stanza-create`を実行する必要はありません。

**バグ修正：**

- Cライブラリでコンパイラー警告を発生させていたconstへの代入を修正しました。 (*修正：Adrian Vondendriesch。レビュー：David Steele。*)
- `--repo-sync`オプションの対象から漏れていた、いくつかのディレクトリ同期を修正しました。
- リストア時にユーザー／グループが存在しない場合、`File->owner()`で"uninitialized value"エラーになる場合がある問題を修正しました。 (*報告：Leonardo GG Avellar。*)
- プロトコルの不一致エラーで、期待する値が出力されない問題を修正しました。
- 終了コード1を異常終了とする、`archive-get`の誤ったログメッセージを修正しました。

**新機能：**

- 非同期アーカイブを、改善されたマルチプロセス実装に変更しました。
- 多くの場合に壊れたリポジトリを修復でき、必須として使えるだけの堅牢性を持つよう、`stanza-create`コマンドを改善しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- スタンバイで実行できるよう`check`コマンドを改善しました。ただし、レプリカでは`pg_switch_xlog()`を実行できないため、基本的なチェックのみを行います。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `info`コマンドに、アーカイブとバックアップのWAL範囲を追加しました。
- PostgreSQL < 9.2でテーブルスペースを再マッピングする際、`pg_tablespace.spclocation`の更新を促す警告を追加しました。 (*貢献：blogh。レビュー：David Steele。*)
- 読み取り専用の操作である`archive-get`、`restore`、`info`、`check`について、リモートでのロックを不要にしました。 (*提案：Michael Vitale。*)

**改善：**

- 最初のログエントリが書き込まれるまで、ログファイルのバナーを出力しないようにしました。 (*提案：Jens Wilke。*)
- バックアップ開始LSNでフィルターすることで、不完全な書き込みのページがページチェックサムで誤検出される可能性を減らしました。
- Cライブラリのビルドフラグから、Intel固有の最適化を削除しました。 (*貢献：Adrian Vondendriesch。レビュー：David Steele。*)
- `--lock`オプションを削除しました。このオプションはロックディレクトリをリポジトリ外に配置できるようになる前に導入されたもので、現在は不要です。
- ログのタイムスタンプを非表示にできる`--log-timestamp`オプションを追加しました。主に、自動生成するドキュメントでフィルターを使わずに済むようにするためのものです。
- 相対パスを絶対パスに変換できない場合、適切なエラーコードを返すようにしました。 (*提案：Yogesh Sharma。*)

**ドキュメントの機能：**

- ユーザーガイドに`process-max`オプションの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.12リリースノート {#v112-release-notes}

*ページチェックサム、設定、不具合修正*

*2016年12月12日リリース*

**重要な注意事項**：以前のリリースでは、現在のコマンドに対して無効なオプションをコマンドラインで指定しても、エラーになりませんでした。今後は無効なオプションでエラーが発生するため、運用に支障が出ないよう、環境内のコマンドラインオプションを入念に確認することが重要です。

**バグ修正：**

- 指定したコマンドに対して無効なオプションをコマンドラインで指定しても、エラーにならない問題を修正しました。従来はそのオプションを無視し、動作に変化はありませんでしたが、混乱の原因になっていました。今後は無効なオプションでエラーが発生します。 (*報告：Nikhilchandra Kulkarni。*)
- リポジトリ内のテーブルスペース用の内部シンボリックリンクが作成されない問題を修正しました。この問題が表面化するのは、ファイルシステムのスナップショットを使って、その場でクラスターを手動起動しようとした場合のみです。通常のバックアップとリストアには影響しませんでした。
- ログシステムを初期化する前、つまりオプションの解析中に、エラーをコンソールへ出力できない問題を修正しました。エラーコードは正しく返されていたため、実際には失敗した処理が成功したように見えることはありませんでした。 (*報告：Adrian Vondendriesch。*)
- バックアップサーバーで指定した`db-port`が、最初に設定したデータベースのものでない限り、リモートに正しく渡されない問題を修正しました。 (*報告：Michael Vitale。*)

**新機能：**

- PostgreSQL >= 9.3でチェックサムが有効な場合、データファイルのページチェックサムをpgBackRestで検証できる`--checksum-page`オプションを追加しました。この機能にはCライブラリが必要ですが、当初はOSパッケージで提供されていない場合があります。ライブラリが存在し、クラスターでチェックサムが有効になっている場合、このオプションを自動的に有効にします。 (*提案：Stephen Frost。*)
- シンボリックリンクをサポートしないファイルシステムにリポジトリを置く場合、内部シンボリックリンクを作成しないようにできる`--repo-link`オプションを追加しました。pgBackRestの機能には影響しませんが、利便性のための`latest`リンクと、テーブルスペースの内部シンボリックリンクは作成されません。そのため、ファイルシステムのスナップショットを使い、その場でクラスターを手動起動する際に影響します。
- NTFSなど、ディレクトリ同期をサポートしないファイルシステム向けに、リポジトリ内のディレクトリ同期を無効にできる`--repo-sync`オプションを追加しました。
- コマンドの正常完了を示す、予測可能なログエントリを追加しました。たとえばバックアップが正常に終了すると、`INFO: backup command end: completed successfully`が出力されます。 (*提案：Jens Wilke。*)

**改善：**

- 単純化のため、`pg_control`は処理の最後に単独でコピーするのではなく、他のファイルと一緒にコピーするようにしました。`backup`コマンドには従来の動作は不要であり、`restore`は一時ファイルにコピーしたうえで、リストアの最後に名前を変更します。

**ドキュメントの不具合修正：**

- PDFのビルドで例外が抑制される問題を修正しました。
- v1.10で導入された、セクションリンクのリグレッションを修正しました。

**ドキュメントの機能：**

- クイックスタートに保持の説明を追加しました。


### v1.11リリースノート {#v111-release-notes}

*非同期アーカイブの効率に関する不具合修正*

*2016年11月17日リリース*

**バグ修正：**

- 非同期アーカイブがファイルをまとめて転送せず、1回の実行で1ファイルしか転送しない問題を修正しました。このリグレッションはv1.09で導入され、効率にのみ影響していました。非同期モードでも、すべてのWALセグメントは正しくアーカイブされていました。 (*報告：Stephen Frost。*)


### v1.10リリースノート {#v110-release-notes}

*stanzaの作成と軽微な不具合修正*

*2016年11月8日リリース*

**バグ修正：**

- バックアップ間でデータベースに変更がなく、`pg_control`だけが変化した場合、バックアップがエラーになる場合がある問題を修正しました。
- 同じプレフィックスを持つテーブルスペースパスで、無効なリンクのエラーが発生する問題を修正しました。 (*報告：Nikhilchandra Kulkarni。*)

**新機能：**

- リポジトリでのstanzaの作成を正式な操作にするため、`stanza-create`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**改善：**

- Perlモジュールから余分な`use lib`ディレクティブを削除しました。 (*提案：Devrim Gündüz。*)


### v1.09リリースノート {#v109-release-notes}

*9.6のサポート、設定の柔軟性、不具合修正*

*2016年10月10日リリース*

**バグ修正：**

- バックアップディレクトリが存在しない場合にエラーメッセージを記録しないよう、`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- 無効なarchiveコマンドを検出した場合、そのコマンドを正しく表示するようエラーメッセージを修正しました。 (*報告：Jason O'Donnell。*)
- `archive-push`が新しいWALセグメントをキューに入れるための空き容量を確保できないと、非同期アーカイバーが起動されない問題を修正しました。このため、`archive-push`を直接呼ぶなどの手動操作なしでは、キューが空になりませんでした。今後は、新しいWALセグメントを保存する空き容量がない場合、PostgreSQLにエラーを返しますが、非同期プロセスは起動し、最終的に空き容量を確保できるようにします。 (*報告：Jens Wilke。*)
- ローカルプロセスが再開またはリストア中にチェックサムを計算するものの、ファイルをコピーせず、リモートがアイドル状態になると発生するタイムアウトを修正しました。 (*報告：Jens Wilke。*)

**新機能：**

- PostgreSQL 9.6では、非排他的バックアップを自動的に使用するようにしました。
- sshクライアントを指定できる`cmd-ssh`オプションを追加しました。 (*提案：Jens Wilke。*)
- コンソールログの送信先を`stderr`または`stdout`に制御する`log-level-stderr`オプションを追加しました。デフォルトは`warn`です。こちらのほうが直感的かもしれませんが、以前のバージョンとは動作が変わります。`log-level-stderr=off`を設定すると、以前の動作を維持できます。 (*提案：Sascha Biberhofer。*)
- データベース接続の`application_name`を`"pgBackRest [command]"`に設定するようにしました。 (*提案：Jens Wilke。*)
- `archive-check`オプションが有効な場合、archive_modeが有効であることを確認するようにしました。

**改善：**

- pgBackRestのアドバイザリーロックを取得できない場合のエラーメッセージを明確にし、PostgreSQLのバックアップロックではないことがわかるようにしました。 (*提案：Jens Wilke。*)
- コマンド開始時のINFOログにpgBackRestのバージョン番号を含めるようにしました。
- ローカルプロセスの開始／停止時のINFOログにプロセスIDを記録するようにしました。

**ドキュメントの機能：**

- ユーザーガイドに`archive-timeout`オプションの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.08リリースノート {#v108-release-notes}

*不具合修正とログの改善*

*2016年9月14日リリース*

**バグ修正：**

- ローカルプロセスが完了時に切断せず、後でタイムアウトする場合がある問題を修正しました。 (*報告：Todd Vernick。*)
- WALセグメントがアーカイブに届くのを待っている間に、プロトコル層がタイムアウトする場合がある問題を修正しました。 (*報告：Todd Vernick。*)

**改善：**

- より完全なログを残せるよう、ファイルが作成されるまでファイル向けのログ出力をキャッシュするようにしました。


### v1.07リリースノート {#v107-release-notes}

*スレッドからプロセスへの移行と不具合修正*

*2016年9月7日リリース*

**バグ修正：**

- スタンバイからのバックアップ中に、テーブルスペースをプライマリーからコピーしていた問題を修正しました。
- ローカルだけでなくリモートでもバックアップ情報を確認するよう、`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- `retention-archive-type=diff`の際に`retention-archive`が自動設定されず、アーカイブの期限切れ処理が意図したほど進まない問題を修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)

**新機能：**

- 互換性と性能を高めるため、Perlのスレッドをプロセスに置き換えました。
- プライマリーのレプリケーションスロットがバックアップに含まれないよう、`$PGDATA/pg_replslot`ディレクトリの内容を除外しました。
- `archive-check=n`の場合でも、`backup.manifest`に`archive-start`と`archive-stop`を記録するようにしました。 (*提案：Jens Wilke。*)
- アーカイブの保持設定が意図した効果をもたらさない場合や、無期限の保持を許す場合に警告を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- PostgreSQL 9.6 rc1の非排他的バックアップを試験的にサポートしました。以降のリリース候補でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**ドキュメントの不具合修正：**

- バイナリーのパスに関連する、ドキュメントの再現性に関する軽微な問題を修正しました。

**ドキュメントの機能：**

- アーカイブの保持について説明しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.06リリースノート {#v106-release-notes}

*スタンバイからのバックアップと不具合修正*

*2016年8月25日リリース*

**バグ修正：**

- 別のリンクを参照するテーブルスペースのリンクで、エラーを出さずにテーブルスペース全体をスキップしていた問題を修正しました。 (*報告：Michael Vitale。*)
- 複数の値を許可すべきでないオプションを`pgbackrest.conf`で複数回指定しても、エラーにならない問題を修正しました。 (*報告：Michael Vitale。*)
- `db-timeout`を増やしたときに、`protocol-timeout`が自動的に増えない問題を修正しました。 (*報告：Todd Vernick。*)

**新機能：**

- スタンバイクラスターからのバックアップをサポートしました。バックアップの開始／停止や、レプリケーションされないファイルのコピーには、引き続きプライマリーへの接続が必要です。ただし、ファイルの大半をスタンバイからコピーすることで、プライマリーの負荷を減らします。
- データベースの設定をより柔軟にしました。バックアップサーバーにマスターとスタンバイの両方を設定でき、pgBackRestがどちらがプライマリーかを自動判定します。このため、独立したバックアップサーバーを使う場合、プライマリーからスタンバイへフェイルオーバーしても、バックアップの設定を変更する必要がありません。
- PostgreSQLが起動時に消去、再作成、またはゼロ初期化するディレクトリをバックアップから除外しました。`pgsql_tmp`と`pg_stat_tmp`が該当します。また、従来から除外していた`backup_label.old`、`postmaster.opts`、`postmaster.pid`、`recovery.conf`、`recovery.done`に加え、`postgresql.auto.conf.tmp`ファイルも除外しました。
- PostgreSQL 9.6 beta4の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- マニフェストの作成時に、リンクを参照するリンクに対するエラーメッセージを改善しました。
- `archive-push`または`archive-get`で相対パスを検出した場合のエラーメッセージに、ヒントを追加しました。
- ファイルのコピー元ホストがわかるよう、バックアップのログメッセージを改善しました。


### v1.05リリースノート {#v105-release-notes}

*テーブルスペースリンクのチェックに関する不具合修正*

*2016年8月9日リリース*

**バグ修正：**

- パスの一部に$PGDATAを含むテーブルスペースが、実際にはそうでなくても$PGDATAのサブディレクトリと判定される問題を修正しました。相対パスのチェックも少し強化しました。 (*報告：Chris Fort。*)

**ドキュメントの機能：**

- cronによるバックアップのスケジュール設定について説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)

**ドキュメントの改善：**

- バックログをpgBackRestのウェブサイトからGitHubリポジトリのwikiに移しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.04リリースノート {#v104-release-notes}

*各種不具合修正*

*2016年7月30日リリース*

**バグ修正：**

- 余分なリモートプロセスが作成され、マルチスレッドのバックアップ／リストアがタイムアウトしたり、ロック競合を発生させたりする場合がある問題を修正しました。 (*報告：Michael Vitale。*)
- `check`コマンドでdb-pathが必須になっておらず、未指定の場合にわかりやすいエラーメッセージではなくアサーションが発生していた問題を修正しました。 (*報告：Michael Vitale。*)
- データベースのバージョン／IDがアーカイブのものと一致しない場合、エラーになるよう`check`コマンドを修正しました。 (*修正：Cynthia Shang。レビュー：David Steele。*)
- データベースサーバーの`pgbackrest.conf`に`backup-host`オプションがない場合、リモートがさらに自身のリモートを開始しようとする問題を修正しました。 (*報告：Lardière Sébastien。*)
- `pg_xlog`がシンボリックリンクの場合、その内容までバックアップする問題を修正しました。リストア時に問題は起きませんでしたが、容量を無駄にしていました。
- ロック処理内の無効な`log()`呼び出しを修正しました。

**新機能：**

- PostgreSQL 9.6 beta3の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- SSHプロトコル接続でバナーを非表示にしました。
- エラーが発生したホストを識別できるよう、リモートのエラーメッセージを改善しました。
- すべての種類のリモートがロックを取得するようにしました。従来の例外はテストハーネスとpgBackRestが同じVMで動作していた時代のもので、今は該当しません。

**ドキュメントの機能：**

- `backrest-user`オプションのデフォルトが`backrest`である理由を補足しました。 (*提案：Michael Vitale。*)
- サポート対象プラットフォームでのパッケージの提供状況を更新しました。 (*提案：Michael Vitale。*)


### v1.03リリースノート {#v103-release-notes}

*checkコマンドと不具合修正*

*2016年7月2日リリース*

**バグ修正：**

- マルチスレッドの`backup`で多数の小さなファイルを処理すると、`keep-alives`の送信が滞る問題を修正しました。また、シングル／マルチスレッドの`backup`再開時と、`restore`のチェックサム計算時には、キープアライブがまったく送られていませんでした。 (*報告：Janice Parkinson, Chris Barber。*)
- `db-host`オプションを設定した場合、コマンドラインから明示的に呼び出した`expire`が実行を拒否する問題を修正しました。`backup`の後に自動実行する`expire`では、問題はありませんでした (*報告：Chris Barber。*)
- `archive-check`が無効でもarchive_commandを検証していた問題を修正しました。

**新機能：**

- アーカイブとバックアップに向けてpgBackRestが正しく設定されているか検証する`check`コマンドを追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- `protocol-timeout`オプションを追加しました。従来の`protocol-timeout`は、`db-timeout`に30秒を加えた値でした。
- バックアップ終了時にリモートの停止に失敗しても、例外を発生させなくなりました。代わりに、`protocol-timeout`を増やすことを推奨する警告を出します。
- PostgreSQL 9.6 beta2の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。

**改善：**

- バックアップ時に記録したユーザー／グループがリストア先ホストに存在しない場合の処理を改善しました。ユーザー／グループを名前に対応付けられない場合も、明示的に処理するようにしました。
- オプションの処理を大幅に厳格化しました。従来はコマンドに明示的に割り当てられていないオプションでも使用できる場合がありました。特に、実行場所を決める`backup-host`と`db-host`で顕著でした。

**ドキュメントの改善：**

- 再現可能なビルドを生成するため、ドキュメントで固定の日付を使用できるようにしました。 (*提案：Adrian Vondendriesch。*)
- ユーザーガイドに非同期アーカイブの説明を追加しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- 新しいPerlでは`/usr/lib/perl5`が検索パスから削除されているため、pgBackRestモジュールの推奨インストール先を`/usr/share/perl5`に変更しました。
- 旧バージョンのpgBackRestを削除する手順を追加しました。


### v1.02リリースノート {#v102-release-notes}

*Perl 5.22の不具合修正*

*2016年6月2日リリース*

**バグ修正：**

- Perl 5.22の新しい制約に合わせて、sprintf()の使い方を修正しました。書式文字列から参照されないパラメーターは、許可されなくなりました。 (*修正：Adrian Vondendriesch。レビュー：David Steele。*)

**ドキュメントの不具合修正：**

- Perl 5.2Xと互換性のない構文を修正しました。 (*修正：Christoph Berg, Adrian Vondendriesch。レビュー：David Steele。*)
- PDFのロゴに使用していた絶対パスを修正しました。 (*報告：Adrian Vondendriesch。*)

**ドキュメントの機能：**

- 不具合、機能、リファクタリングを明確に区別できるよう、リリースノートをセクションに分けました。コアのコードに影響しないドキュメントとテストスイートの変更には、「補足事項」セクションを追加しました。
- manページの生成を追加しました。 (*貢献：Adrian Vondendriesch, David Steele。*)
- 変更履歴は、Markdownのみで出力される最後のドキュメントでした。標準のレンダラーで出力できるよう、変換処理を作成しました。変更履歴はウェブサイトに掲載し、名前を「リリース」に変更しました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)


### v1.01リリースノート {#v101-release-notes}

*infoの拡充、選択的リストア、9.6のサポート*

*2016年5月17日リリース*

**新機能：**

- `info`コマンドのテキスト出力を拡充し、すべてのバックアップについて、タイムスタンプ、サイズ、参照一覧を含めるようにしました。 (*貢献：Cynthia Shang。レビュー：David Steele。*)
- クラスターのバックアップからデータベースを選んでリストアできるようにしました。特定のデータベースだけをリストアする場合、容量と時間を大幅に削減できます。リストアしなかったデータベースにはアクセスできませんが、共有カタログから除去するには手動で削除する必要があります。 (*レビュー：Cynthia Shang, Greg Smith, Stephen Frost。提案：Stephen Frost。*)
- PostgreSQL 9.6 beta1の非排他的バックアップを試験的にサポートしました。以降のベータ版でコントロール／カタログ／WALのバージョンが変わると、互換性が失われる可能性がありますが、pgBackRestはリリースごとに更新して追従します。 (*レビュー：Cynthia Shang。*)


### v1.00リリースノート {#v100-release-notes}

*新しいリポジトリ形式と設定方式、リンクのサポート*

*2016年4月14日リリース*

**重要な注意事項**：この一斉移行が必要なリリースでは、旧バージョンのpgBackRestとの互換性が失われます。マニフェスト形式、ディスク上の構造、設定方式、実行ファイル名とパス名がすべて変更されています。このバージョンのpgBackRestのバックアップを保存するには新しいリポジトリを作成し、リストアが必要になる場合に備えて旧リポジトリをしばらく保持する必要があります。旧リポジトリからのリストアには旧バージョンのpgBackRestが必要ですが、名称が変更されたため、`1.00`と旧バージョンのpgBackRestを同時にインストールできます。変更点の詳細は以下の説明を参照してください。

**新機能：**

- より簡単に使える新しい設定方式を実装しました。詳細はユーザーガイドと設定リファレンスを参照してください。単純な構成では、すべてのオプションを`stanza`セクションに記述できるようになりました。stanza間で共有するオプションは`[global]`セクションに記述できます。より複雑な構成では引き続きコマンド別セクションを使用できますが、必要になるケースはまれなはずです。 (*提案：Michael Renner。*)
- `repo-path`オプションは、ローカルかリモートかにかかわらず、バックアップとアーカイブを保存するリポジトリを常に指すようになりました。このため、`repo-remote-path`オプションを削除しました。非同期アーカイブ時にWALセグメントをキューに入れる場所は、新しい`spool-path`オプションで指定できます。ローカルリポジトリは不要になりました。
- デフォルトの設定ファイル名を`pg_backrest.conf`から`pgbackrest.conf`に変更しました。他の名称変更と一貫させるとともに、`1.00`への移行時に古い設定ファイルを誤って読み込むことを防ぐためです。 (*提案：Michael Renner, Stephen Frost。*)
- デフォルトのリポジトリ名を`/var/lib/backup`から`/var/lib/pgbackrest`に変更しました。 (*提案：Michael Renner, Stephen Frost。*)
- ロックファイルはデフォルトで`/tmp/pgbackrest`に保存するようになりました。現在では`/run/pgbackrest`の使用が推奨されますが、この場所を使うには、本リリースに含まれない初期化スクリプトが必要です。ロックディレクトリは`lock-path`オプションで設定できます。
- ログファイルはデフォルトで`/var/log/pgbackrest`に保存するようになりました。`logrotate`で管理できるよう、日付は付加しなくなりました。ログディレクトリは`log-path`オプションで設定できます。 (*提案：Stephen Frost。*)
- 実行ファイル名を`pg_backrest`から`pgbackrest`に変更しました。 (*提案：Michael Renner, Stephen Frost。*)
- PGDATAからリンクされるすべてのファイルとディレクトリをバックアップに含めるようになりました。デフォルトでは、リンク先をファイルまたはディレクトリとしてPGDATA内に直接リストアします。`--link-all`オプションを使うと、すべてのリンクを元の場所にリストアできます。`--link-map`オプションを使うと、リンク先を新しい場所へ変更できます。
- `--tablespace`オプションを削除し、機能をより明確に示す`--tablespace-map-all`オプションに置き換えました。
- `info`より多くの情報を出力し、`debug`ほど詳細ではない`detail`ログレベルを追加しました。


--------

## 安定版以前のリリース {#pre-stable-releases}


### v0.92リリースノート {#v092-release-notes}

*コマンドラインのリポジトリパスの修正*

*2016年4月6日リリース*

**バグ修正：**

- マスタープロセスがリモートに`--repo-path`ではなく`--repo-remote-path`を渡し、デフォルトのリポジトリディレクトリ（`/var/lib/backup`）にロックファイルが作成されて、通常は失敗に終わる問題を修正しました。この問題は、`--repo-remote-path`を`pg_backrest.conf`ではなくコマンドラインで指定した場合にのみ発生していました。 (*報告：Jan Wieck。*)


### v0.91リリースノート {#v091-release-notes}

*テーブルスペースの不具合修正と軽微な機能拡張*

*2016年3月22日リリース*

**テーブルスペースに関する重要な不具合修正**：0.90でリポジトリ形式を意図せず変更したため、テーブルスペースを含むバックアップは、ディスク上で有効なPostgreSQLクラスターではなくなっていました。影響を受けるのは、restoreコマンドを使用せず、バックアップを直接コピーしてPostgreSQLクラスターをリストアするユーザーのみでした。ただし、この修正により、リストア方法を問わず、テーブルスペースを含む古いバックアップとの互換性が失われます（pgBackRestはエラーを発生させ、リストアを拒否します）。テーブルスペースを含むクラスターでは、バージョン0.91をインストールした直後に新しいフルバックアップを取得することを推奨します。古いバックアップをリストアする必要がある場合は、そのバックアップのバージョンと一致するpgBackRestを使用してください。

**バグ修正：**

- pgBackRest 0.90で導入されたリポジトリの互換性の問題を修正しました。 (*報告：Evan Benoit。*)

**新機能：**

- バックアップ時に`global/pg_control`を最後にコピーするようにしました。
- `.info`ファイルと`.manifest`ファイルを一時ファイルに書き込んでから、最終的な場所へ移動し、fsyncするようにしました。
- `--no-start-stop`オプションの名前を`--no-online`に変更しました。

**テストスイートの機能：**

- Perl-Criticによるソースの静的解析を導入しました。現在はgentleレベルで合格しています。


### v0.90リリースノート {#v090-release-notes}

*9.5のサポート、各種機能拡張、軽微な不具合修正*

*2016年2月7日リリース*

**バグ修正：**

- `--no-archive-check`を指定すると設定エラーが発生する問題を修正しました。 (*報告：Jason O'Donnell。*)
- 特定のタイミングでシステムがクラッシュして一時WALファイルが残ると、次の`archive-push`が失敗する場合がある問題を修正しました。
- `archive-copy=n`を併せて指定しなくても、`retention-archive`をバックアップの保持数（`retention-full`または`retention-diff`）より小さく安全に設定できるようになりました。アーカイブの保持対象外となるバックアップの整合性を確保するために必要なWALは、アーカイブに保持します。ただし、この場合、アーカイブの保持対象外となるバックアップではPITRはできません。

**新機能：**

- テーブルスペースのバックアップとリストアでは、実行対象のPostgreSQLバージョン用に作成されたサブディレクトリのみを操作するようにしました。テーブルスペースには、特にバイナリーアップグレード時などに複数のバージョンが共存できるため、これによりバックアップ時の余分なファイルのコピーや、リストア時の他のバージョンの消去を防ぎます。これはPostgreSQL >= 9.0にのみ適用されます。それ以前のPostgreSQLはテーブルスペースのディレクトリを共有できませんでした。
- `archive-check=y`であるにもかかわらず、`archive_command`が`pg_backrest`を実行しない場合にエラーを発生させるようにしました。 (*貢献：Jason O'Donnell。レビュー：David Steele。*)
- `repo-path`または`repo-remote-path`が存在しない場合のエラーメッセージを改善しました。
- `--delta`および`--force`リストアオプションに、宛先が有効な$PGDATAディレクトリであることを確認するチェックを追加しました。pgBackRestは`PG_VERSION`または`backup.manifest`（中断したリストアで残るファイル）の存在を確認します。どちらもない場合は`--delta`と`--force`を無効にしますが、リストア自体は続行します。ただし、$PGDATAディレクトリまたはいずれかのテーブルスペースディレクトリにファイルがある場合は、処理を中止します。
- リストアで`--set=latest`（デフォルト）を指定した場合、実際にリストアするバックアップをログに出力するようにしました。
- PostgreSQL 9.5の部分WALセグメントと`recovery_target_action`設定をサポートしました。`archive_mode = 'always'`設定はまだサポートしていません。
- PostgreSQL 9.4で導入された`recovery_target = 'immediate'`リカバリー設定をサポートしました。
- テーブルスペースについて、pg_tblspc内のパスまたはファイル、pg_tblspc内の相対リンク、$PGDATA内のテーブルスペースをチェックするようにしました。この3つはいずれもエラーになります。


### v0.89リリースノート {#v089-release-notes}

*タイムアウトの不具合修正と読み取り専用リポジトリからのリストア*

*2015年12月24日リリース*

**バグ修正：**

- リモートかつマルチスレッドで実行する、時間のかかるバックアップやリストアがタイムアウトする問題を修正しました。スレッドのリモートプロセスがすべての処理を行っている間も、メインプロセスのリモートがタイムアウトしないよう、キープアライブを使用するようになりました。デバッグしやすいよう、タイムアウトのエラーメッセージも改善しました。 (*報告：Stephen Frost。*)

**新機能：**

- `--no-lock`と`--log-level-file=off`を使い、読み取り専用リポジトリからリストアできるようにしました。`--no-lock`オプションはリストア時にのみ使用できます。


### v0.88リリースノート {#v088-release-notes}

*ドキュメントと軽微な不具合修正*

*2015年11月22日リリース*

**バグ修正：**

- `start`／`stop`コマンドで`--config`オプションが必須になっていた問題を修正しました。 (*報告：Dmitry Didovicher。*)
- ログファイルに追記せず、上書きしていた問題を修正しました。 (*報告：Stephen Frost, Dmitry Didovicher。*)
- `backup-user`が任意になっていなかった問題を修正しました。

**新機能：**

- リポジトリ内のバックアップディレクトリにはシンボリックリンクを作成しなくなりました。これらのリンクは任意の場所を指すことができ、危険になり得るためです。リストア時には引き続きシンボリックリンクを再作成します。 (*提案：Stephen Frost。*)
- バックアップの期限切れ処理のメッセージを改善しました。フルバックアップと差分バックアップの期限切れ処理を、併せて期限切れとなるすべての依存バックアップの一覧とともに、1行でログに出力します。
- アーカイブの保持数を明示的に設定していない場合、フルバックアップの保持数に自動設定するようにしました。

**ドキュメントの機能：**

- ユーザーガイドに、差分リストア、期限切れ処理、専用バックアップホスト、pgBackRestの起動と停止、レプリケーションの説明を追加しました。


### v0.87リリースノート {#v087-release-notes}

*ウェブサイトとユーザーガイド*

*2015年10月28日リリース*

**新機能：**

- `backup_label.old`ファイルと`recovery.done`ファイルをバックアップから除外するようにしました。

**ドキュメントの機能：**

- pgBackRestの基本と、PITRを含む高度なトピックの一部を扱う、新しいユーザーガイドを追加しました。まだ追加すべき内容は多くありますが、まずは出発点です。 (*貢献：David Steele, Stephen Frost。レビュー：Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher。*)


### v0.85リリースノート {#v085-release-notes}

*起動／停止コマンドと軽微な不具合修正*

*2015年10月8日リリース*

**バグ修正：**

- バックアップまたはリストアが正常に完了した後に、エラーを返す場合がある問題を修正しました。
- バックアップ失敗時にバックアップのルートディレクトリに一時ファイルが残ると、再開に失敗する問題を修正しました。コピー段階でバックアッププロセスを強制終了した場合に起こりやすい状況でした。

**新機能：**

- PostgreSQLが停止しているシステムや、他の理由で処理を休止する必要があるシステムで、pgBackRestプロセスが実行されないようにする`stop`コマンドと`start`コマンドを追加しました。
- PostgreSQL 9.5 beta1を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。


### v0.82リリースノート {#v082-release-notes}

*リファクタリング、コマンドラインヘルプ、軽微な不具合修正*

*2015年9月14日リリース*

**バグ修正：**

- 再開した圧縮バックアップで既存ファイルが保持されない問題を修正しました。
- 再開およびincr/diff時に、前回のバックアップの圧縮設定とハードリンク設定が同じであることを確認していなかった問題を修正しました。
- `--force`を指定せずに、稼働中のPostgreSQLクラスターで`--no-start-stop`によるコールドバックアップを開始できてしまう問題を修正しました。
- スレッドが要求されていなくてもスレッドを開始する場合がある問題を修正しました。
- アップグレード／ダウングレード後に、`backup.info`と`archive.info`内のpgBackRestのバージョン番号が更新されない問題を修正しました。
- リポジトリにstanzaがないと、`info`コマンドが例外を発生させる問題を修正しました。 (*報告：Stephen Frost。*)
- PostgreSQLの`pg_stop_backup()`のNOTICEが`stderr`に出力される問題を修正しました。 (*報告：Stephen Frost。*)

**新機能：**

- PostgreSQL 9.5 alpha2を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。

**改善：**

- pgBackRestの命名規則と一貫させるため、`recovery-setting`オプションとセクションの名前を`recovery-option`に変更しました。
- コマンド、特に非同期アーカイブを高速化するため、モジュールの動的読み込みを追加しました。

**ドキュメントの機能：**

- コマンドラインヘルプは、他のドキュメントと同じXMLソースから抽出するようになり、内容も大幅に詳しくなりました。


### v0.80リリースノート {#v080-release-notes}

*DBIのサポート、安定性、利便性向上の機能*

*2015年8月9日リリース*

**バグ修正：**

- `info`コマンドが最も古いバックアップと最も新しいバックアップの整形済みタイムスタンプを、どちらも現在時刻として報告していた問題を修正しました。影響を受けるのは`text`出力のみで、`json`出力は正しいエポック値を報告していました。 (*報告：Michael Renner。*)
- sshエラー（特に接続時のエラー）がログに記録されないプロトコルの問題を修正しました。

**新機能：**

- リポジトリを作成、更新するときのディレクトリとファイルのモードを統一しました。デフォルトでは`umask`を`0000`に設定しますが、`neutral-umask`設定で無効にできます。 (*提案：Cynthia Shang。*)
- 新しいバックアップの開始時に、失敗したバックアップを自動停止できる`stop-auto`オプションを追加しました。
- pgBackRestが`pg_start_backup()`と`pg_stop_backup()`の戻りを待つ時間を制限する`db-timeout`オプションを追加しました。
- リストア開始時に`pg_control`を削除し、最後にコピーし直すようにしました。これにより、リストアが未完了の状態でPostgreSQLが起動される可能性を防ぎます。
- `db-path`設定と`db-port`の整合性を確認するチェックを追加しました。クラスターが報告する`data_directory`を`db-path`設定と比較し、クラスターが報告するバージョンを`pg_control`から読み取った値と比較します。また、`db-socket-path`設定が絶対パスであることを確認します。
- PostgreSQL 9.5 alpha1を試験的にサポートしました。今後のバージョンでコントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各pgBackRestリリースで追従します。`--target-resume`テスト（この機能は9.5で変更されています）を除くすべての回帰テストに合格しています。`.partial` WALセグメントのテストはまだありません。

**改善：**

- PostgreSQLへの接続に、`psql`の代わりにPerlの`DBI`と`DBD::Pg`を使用するようにしました。`cmd-psql`設定と`cmd-psql-option`設定を削除し、`db-port`と`db-socket-path`に置き換えました。インストールガイドの手順に従い、使用するOSに`DBD::Pg`をインストールしてください。

**テストスイートの機能：**

- Ubuntu 14.04とCentOS 7向けのvagrantテスト設定を追加しました。


### v0.78リリースノート {#v078-release-notes}

*CPANへの依存の削除と安定性の改善*

*2015年7月13日リリース*

**改善：**

- マルチスレッド動作でのCPANパッケージへの依存を削除しました。`threads`パッケージと`Thread::Queue`パッケージを更新してもよいですが、必須ではなくなりました。
- 待機時間のバックオフを、等比数列からフィボナッチ数列に変更しました。妥当な値を保ちつつ、待機時間の増加を緩やかにします。

**テストスイートの機能：**

- Ubuntu 12.04とCentOS 6向けのvagrantテスト設定を追加しました。


### v0.77リリースノート {#v077-release-notes}

*CentOS/RHEL 6のサポートとプロトコルの改善*

*2015年6月30日リリース*

**新機能：**

- バックアップ／リストアとアーカイブの安全性を高めるため、`File`オブジェクトにファイルとディレクトリの同期処理を追加しました。 (*提案：Andres Freund。*)
- CentOS/RHEL 6のデフォルトであるPerl 5.10.1とOpenSSH 5.3をサポートしました。 (*提案：Eric Radman。*)
- `archive_command`が設定されておらず、`--no-archive-check`も指定されていない状態でバックアップを実行した場合のエラーメッセージを改善しました。 (*提案：Eric Radman。*)


### v0.75リリースノート {#v075-release-notes}

*新しいリポジトリ形式、infoコマンド、9.5の試験的サポート*

*2015年6月14日リリース*

**重要な注意事項**：この一斉移行が必要なリリースでは、旧バージョンのpgBackRestとの互換性が失われます。マニフェスト形式、ディスク上の構造、実行ファイル名がすべて変更されています。このバージョンのpgBackRestのバックアップを保存するには新しいリポジトリを作成し、リストアが必要になる場合に備えて旧リポジトリをしばらく保持する必要があります。`pg_backrest.conf`ファイルは変更されていませんが、cronなどにある`pg_backrest.pl`への参照を、`.pl`拡張子のない`pg_backrest`に変更する必要があります。

**新機能：**

- `info`コマンドを追加しました。
- ログの出力をバッファリングしないようにしました。これにより、複数スレッドから書き込むログファイルの混乱を抑えられるはずです。 (*提案：Michael Renner。*)
- PostgreSQL 9.5を試験的にサポートしました。コントロールバージョンやWALマジックが変わると互換性が失われる可能性がありますが、各リリースで追従します。

**改善：**

- `backup`でのファイルの処理順を効率化しました。サイズの大きい順にコピーすることで、最後に1つのスレッドだけが大きなファイルをコピーする状況を避けます。`restore`ではすでに実装済みでした。


### v0.70リリースノート {#v070-release-notes}

*アーカイブの安定性とログ、ヘルプの改善*

*2015年6月1日リリース*

**バグ修正：**

- `hardlink=n`の場合、incr/diffバックアップで`archive-copy`が失敗する問題を修正しました。この場合は`pg_xlog`パスがまだ存在しないため、作成する必要があります。 (*報告：Michael Renner。*)
- 非同期アーカイブで`archive-max-mb`に達した際、`archive-push`が正しく0を返さない問題を修正しました。また、停止ファイルを2回削除する必要がないよう、非同期処理のチェックを転送後に移しました。このケースの単体テストを追加し、何が起きたかをユーザーが把握しやすいようエラーメッセージも改善しました。 (*報告：Michael Renner。*)
- 1つのstanzaに対して同じ種類の操作を複数実行できてしまう、ロックの問題を修正しました。データの整合性への影響はないようでしたが、アーカイブ時に不要なエラーが発生し、バックアップ／リストアでもエラーにつながる可能性がありました。 (*報告：Michael Renner。*)

**新機能：**

- チェックサムが一致する場合、重複するWALセグメントをアーカイブできるようにしました。一部のリカバリー手順で必要になるためです。
- `pg_backrest.conf`で`#`文字を使ってコメントを記述したり、設定を無効にしたりできるようにしました。行の最初の文字にある`#`のみが有効です。 (*提案：Michael Renner。*)
- バックアップがチェックポイントを待っていることがわかるよう、`pg_start_backup()`の前のログを改善しました。 (*提案：Michael Renner。*)
- コマンドの動作とログを各種修正しました。 (*レビュー：Michael Renner。提案：Michael Renner。*)

**改善：**

- `JSON`モジュールを、Perl本体に同梱される`JSON::PP`に置き換えました。

**ドキュメントの不具合修正：**

- ヘルプを各種修正しました。 (*レビュー：Michael Renner。報告：Michael Renner。*)


### v0.65リリースノート {#v065-release-notes}

*再開とリストアのログの改善、コンパクトなリストア*

*2015年5月11日リリース*

**バグ修正：**

- 相対パスでリストアを実行した場合に、`recovery.conf`に絶対パスが書き込まれない問題を修正しました。

**新機能：**

- 再開機能を改善しました。再開時に既存のファイルが変更されていないことを確認し、バックアップの進行中にチェックサムを保持できるよう、マニフェストをより頻繁に保存します。再開時の各ケースを検証する単体テストも追加しました。
- 再開を任意にしました。無効にするには`resume`設定、またはコマンドラインの`--no-resume`を使用してください。
- リストア時のinfoメッセージを増やしました。以前はリストアのメッセージの大半がdebugレベルだったため、ログへの出力が少なくなっていました。
- テーブルスペースを`pg_tblspc`パスにリストアできる`tablespace`設定を追加しました。これにより、開発やステージングなどに便利な、まとまった配置でリストアできます。現在のpgBackRestは`pg_tblspc`パス内にはリンクのみがあることを前提としているため、このようにリストアしたクラスターをバックアップすることはできません。


### v0.61リリースノート {#v061-release-notes}

*非圧縮のリモート宛先に関する不具合修正*

*2015年4月21日リリース*

**バグ修正：**

- 圧縮率の高い大きなファイルを非圧縮のリモート宛先へコピーすると、バッファリングエラーが発生する場合がある問題を修正しました。このエラーは展開処理で検出され、データ破損ではなくバックアップの失敗として扱われていたため、以前のバージョンで正常に完了したバックアップには影響しないはずです。


### v0.60リリースノート {#v060-release-notes}

*バージョンサポートの拡充とWALの改善*

*2015年4月19日リリース*

**バグ修正：**

- 重複するWALを送信するとエラーになるようにしました。従来、この操作が成功するのはチェックサムが無効な場合のみでした。

**新機能：**

- データベースのシステムIDを使い、アーカイブ内のすべてのWALが同じデータベースに対応することを確認します。これにより、複数クラスターのWALを同じアーカイブに送信してしまう設定ミスを防ぎやすくなります。

**テストスイートの機能：**

- PostgreSQL 8.3までさかのぼって回帰テストが動作するようになりました。


### v0.50リリースノート {#v050-release-notes}

*リストア機能などの追加*

*2015年3月25日リリース*

**バグ修正：**

- チェックサムの不具合を修正し、通常のバックアップと再開したバックアップで動作するようにしました。チェックサムとチェックサムによる差分処理は機能として分離すべきだとようやく気付き、これによりいくつかの処理を簡素化できました。チェックサムによる差分処理についてはissue #28を作成しました。
- バックアップの種類と前回のバックアップが一致しない中断済みバックアップから、バックアップを再開できてしまう問題を修正しました。

**新機能：**

- リストア機能を追加しました。
- すべてのオプションをコマンドラインで指定できるようになり、`pg_backrest.conf`が任意になりました。
- 圧縮／展開処理はスレッドを使わずに実行し、チェックサムとサイズはストリーム内で計算するようになりました。このため、ファイルのチェックサムは必須になりました。
- Postgresが停止している場合にバックアップできる`--no-start-stop`オプションを追加しました。`postmaster.pid`が存在する場合、バックアップを実行するには`--force`が必要です（ただしPostgresが稼働中の場合、整合性のないバックアップが作成される可能性が高くなります）。このオプションは主に単体テストのために追加しましたが、実際の運用でも用途があるかもしれません。
- マニフェストの破損や変更を検出するため、`backup.manifest`にチェックサムを追加しました。
- `latest`リンクは常に最新のバックアップを指します。利便性の向上とリストアの簡略化のために追加しました。

**テストスイートの機能：**

- すべての領域で単体テストを拡充しました。


### v0.30リリースノート {#v030-release-notes}

*コアの再構成と単体テスト*

*2014年10月5日リリース*

**ドキュメントの機能：**

- 不足していたドキュメントを追加しました

**テストスイートの機能：**

- すべての基本操作を対象とする、かなり包括的な単体テストを追加しました。まだ作業が必要なのは確かですが、単体テストには常に改善の余地があります。


### v0.19リリースノート {#v019-release-notes}

*エラーの報告と処理の改善*

*2014年5月13日リリース*

**バグ修正：**

- `file_copy()`がデフォルトでエラーを無視する設定になっていた重大な不具合を発見し、修正しました。また、`file_exists()`には、ファイルが実際に存在していても存在確認に失敗する問題がありました。可能性は非常に低いものの、両者が重なるとエラーを出さずに破損したバックアップが作成されるおそれがありました。


### v0.18リリースノート {#v018-release-notes}

*アーカイブがない場合に軽微なエラーを返す*

*2014年4月13日リリース*

**バグ修正：**

- アーカイブファイルがない場合、`archive-get`コマンドは1を返すようになりました。これにより、重大なエラー（ssh接続の失敗、ファイルコピーエラーなど）と区別できます。PostgreSQLは、これによってアーカイブストリームが正常に終了したことを判断できます。ただし、アーカイブストリームの途中に欠落がある可能性は考慮していません。 (*報告：Stephen Frost。*)


### v0.17リリースノート {#v017-release-notes}

*アーカイブディレクトリを削除できない場合の警告*

*2014年4月3日リリース*

**バグ修正：**

- 空であるはずのアーカイブディレクトリを削除できない場合、backrestはエラーを発生させていました。適切な修正を予定していますが、当面は処理を続けられるよう警告に変更しました。この問題はバックアップにも影響していました。最初のアーカイブファイルが別のディレクトリにある場合、さらに不運な条件が重なると、最後のアーカイブファイルが送信されないことがありました。


### v0.16リリースノート {#v016-release-notes}

*SSHセッションへのRequestTTY=yesの設定*

*2014年4月1日リリース*

**バグ修正：**

- sshセッションに`RequestTTY=yes`を追加しました。これにより、不規則に起きる停止が防げることを期待しています。


### v0.15リリースノート {#v015-release-notes}

*archive-getの追加*

*2014年3月29日リリース*

**新機能：**

- リストアを支援する`archive-get`機能を追加しました。
- バックアップ開始時にチェックポイントを強制する`start-fast=y`オプションを追加しました。


### v0.11リリースノート {#v011-release-notes}

*軽微な修正*

*2014年3月26日リリース*

**バグ修正：**

- データベースへのSSH接続から`master_stderr_discard`オプションを削除しました。時折停止することがあり、ファイル処理で以前に見られた問題と関連している可能性があります。 (*報告：Stephen Frost。*)
- `backup`コマンドと`expire`コマンドでのロックファイルの競合を`ERROR`に変更しました。アーカイブのロック処理からコピーしたため、`DEBUG`になっていました。


### v0.10リリースノート {#v010-release-notes}

*バックアップとアーカイブが動作*

*2014年3月5日リリース*

**新機能：**

- リストア機能はありませんが、バックアップディレクトリは整合性のあるPostgreSQLデータディレクトリです。ファイルを展開するか、バックアップの圧縮を無効にする必要があります。ZFSなどのファイルシステムでは非圧縮バックアップが適しています。スナップショットを使ってローカルにリストアし、論理バックアップの作成や必要なデータの部分的な復旧ができるためです。
- アーカイブはシングルスレッドです。書き込み量の多い、当方の数テラバイト規模のデータベースでは問題になっていません。大容量のWALボリューム、または近くにある大容量ボリュームでasyncオプションを使うことを推奨します。
- バックアップはマルチスレッドですが、`Net::OpenSSH`ライブラリは100%スレッドセーフではないようで、ごくまれにスレッドが停止します。プロセス全体のタイムアウトがあり、プロセスを強制終了することで解消します。確かに、非常に不格好な方法です。
- バックアップを再開するとチェックサムが失われます。複数回再開した場合、最後のバックアップでのみチェックサムが記録されます。前回のバックアップのチェックサムは正しく記録されており、フルバックアップを取得するとすべてリセットされます。
- `Config::IniFile`は大きなファイルをうまく扱えないようなので、`backup.manifest`は`Storable`形式で書き込んでいます。ぜひ人が読めるテキストとして保存できるようにしたいと考えています。

**ドキュメントの機能：**

- ドキュメントはまったくありません（コード内を除きます）。このリリースノートだけは例外です。
