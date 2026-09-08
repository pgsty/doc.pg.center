---
title: "貢献ガイドライン"
linkTitle: "貢献"
weight: 200
icon: fa-solid fa-users
description: "貢献のワークフロー、サポート窓口、開発ガイドライン。"
module: [PATRONI]
categories: [タスク]
aliases: [/patroni/contributing_guidelines/]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>
<a id="chatting"></a>

--------

## チャット {#chatting}

質問がある場合、対話形式のトラブルシューティング支援が必要な場合、他のPatroniユーザーと話したい場合は、[PostgreSQL Slack](https://pgtreats.info/slack-invite)の[\#patroni](https://postgresteam.slack.com/archives/C9XPYG92A)チャンネルに参加してください。

<a id="reporting_bugs"></a>

--------

## バグの報告 {#reporting-bugs}

バグを報告する前に、必ず**最新のPatroniバージョンで再現することを確認**してください。また、[Issueトラッカー](https://github.com/patroni/patroni/issues)に同じ問題がすでに報告されていないかも再確認してください。

--------

## テストの実行 {#running-tests}

behaveテストを実行するための要件：

1. [contrib](https://www.postgresql.org/docs/current/contrib.html)モジュールを含むPostgreSQLパッケージをインストールする必要があります。
2. PostgreSQLのバイナリーを`PATH`から利用できなければなりません。`PATH=/usr/lib/postgresql/11/bin:\$PATH python -m behave`などの方法でパスに追加する必要がある場合があります。
3. 外部DCS（etcd、Consul、Zookeeperなど）を使用してテストする場合は、パッケージをインストールし、それぞれのサービスを起動して、localhostのデフォルトポートで暗号化も保護もされていない接続を受け付ける必要があります。etcdやConsulでは、バイナリーが`PATH`から利用できれば、behaveテストスイートがサービスを起動できます。

依存関係をインストールします。

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

すべての依存関係をインストールしたら、各種テストスイートを実行できます。

``` bash
# You may want to use Virtualenv or specify python3.

# Run flake8 to check syntax and formatting:
python setup.py flake8

# Run the pytest suite in tests/:
python setup.py test

# Moreover, you may want to run tests in different scopes for debugging purposes,
# the -s option include print output during test execution.
# Tests in pytest typically follow the pattern: FILEPATH::CLASSNAME::TESTNAME.
pytest -s tests/test_api.py
pytest -s tests/test_api.py::TestRestApiHandler
pytest -s tests/test_api.py::TestRestApiHandler::test_do_GET

# Run the behave (https://behave.readthedocs.io/en/latest/) test suite in features/;
# modify DCS as desired (raft has no dependencies so is the easiest to start with):
DCS=raft python -m behave
```

--------

## toxによるテスト {#testing-with-tox}

toxのテストを実行するためにインストールが必要な依存関係は、Pythonを除けば一つだけです。

``` bash
pip install tox>=4
```

`behave`テストを実行する場合は、Dockerもインストールする必要があります。

`tox.ini`のTox構成には、次のタスクを実行するための「環境」があります。

- lint: `flake8`によるPythonコードのlint
- test: `pytest`による、利用可能なすべてのPythonインタープリターの単体テスト。XMLレポートを生成し、TTYを検出した場合はHTMLレポートを生成する
- dep: `pipdeptree`によるパッケージ依存関係の競合の検出
- type: `pyright`による静的な型チェック
- black: `black`によるコード整形
- docker-build: `behave`環境で使用するDockerイメージのビルド
- docker-cmd: 上記イメージでの任意のコマンドの実行
- docker-behave-etcd: 上記イメージでのbehaveテスト用のtoxの実行
- py\*behave: 利用可能なPythonインタープリターによるbehaveの実行（Dockerは使用しないが、Dockerコンテナー内でもこれが呼び出される）
- docs: `sphinx`によるドキュメントのビルド

### toxの実行 {#running-tox}

デフォルトの環境一覧であるdep、lint、test、docsを実行するには、次を実行するだけです。

``` bash
tox
```

`test`環境は、ラベル\`test\`で実行できます。

``` bash
tox -m test
```

Dockerでの`behave`テストは、ラベル\`behave\`で実行できます。

``` bash
tox -m behave
```

同様に、docsには`docs`ラベルがあります。

その他の環境は、それぞれの環境名で実行できます。

``` bash
tox -e lint
tox -e py39-test-lin
```

`factors`を使用して、環境一覧の一部を選択することもできます。たとえば、Python 3.10のすべての環境を実行する場合は、次のようにします。

``` bash
tox -f py310
```

これは、次に示す環境をすべて実行することと同じです。

``` bash
$ tox -l -f py310
py310-test-lin
py310-test-mac
py310-test-win
py310-type-lin
py310-type-mac
py310-type-win
py310-behave-etcd-lin
py310-behave-etcd-win
py310-behave-etcd-mac
```

tox（\>=v4）では、次のようにして構成済みのすべての環境の組み合わせを一覧表示できます。

``` bash
tox l
```

アクティブなターミナルでtoxを実行している場合、`test`環境と`docs`環境は、ジョブ完了時に出力されたHTMLファイルを開こうとします。これは、その環境をローカルで実行する開発者の利便性を目的としています。Macでは`open`、Linuxでは`xdg-open`の実行を試みます。別のコマンドを使用するには、環境変数`OPEN_CMD`にコマンド名またはパスを設定してください。この手順に失敗しても、実行全体が失敗することはありません。この機能を無効にするには、環境変数`OPEN_CMD`に何もしないコマンドである`:`を設定します。

``` bash
OPEN_CMD=: tox -m docs
```

### Behaveテスト {#behave-tests}

`-m behave`によるBehaveテストでは、PG_MAJORバージョン11から16に基づくDockerイメージをビルドしてから、すべてのbehaveテストを実行します。実行にかなりの時間がかかる場合があるため、対象を特定のPostgresバージョンや、特定の機能群、ステップに限定したい場合もあります。

Postgresのバージョンを指定するには、依存するイメージのビルド環境の完全な名前を指定し、その後にbehave環境名を指定します。たとえば、Postgres 14を使用する場合は次のようにします。

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

一方、特定の機能をテストする場合は、behaveに位置引数を渡せます。次の例では、すべてのPostgresバージョンでwatchdogのbehave機能テストシナリオを実行します。

``` bash
tox -m behave -- features/watchdog.feature
```

もちろん、この二つを組み合わせることもできます。

--------

## プルリクエストによる貢献 {#contributing-a-pull-request}

1. リポジトリをフォークし、コードの変更を開発してテストします。
2. 変更をユーザードキュメントに反映します。
3. 変更の目的を明確に説明したプルリクエストを送信します。必要に応じて既存のIssueへのリンクを記載します。

プルリクエストには、できるだけ早くフィードバックをお送りします。

Patroniの開発を楽しんでください ;-)
