---
title: バグの報告
weight: 1400
description: etcdプロジェクトに問題を報告する方法
icon: fa-solid fa-bug
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/reporting_bugs.md"
---

etcdプロジェクトのいずれかの部分にバグやドキュメントの誤りを見つけた場合は、[Issueを作成][etcd-issue]してお知らせください。私たちはバグや誤りを真剣に受け止めており、小さすぎて報告する必要のない問題はないと考えています。バグを報告する前に、同じ問題を報告するIssueがすでに存在していないか確認してください。

バグ報告を正確で理解しやすいものにするため、次の点を満たすようにしてください。

- 具体的であること。バージョン、環境、構成など、できるだけ多くの詳細を含めてください。etcdサーバーの実行に関するバグの場合は、etcdのログを添付してください（etcdの構成が記録された起動時のログは特に重要です）。

- 再現可能であること。問題を再現する手順を含めてください。再現が難しい問題もあることは承知していますので、問題につながる可能性のある手順を記載してください。可能であれば、影響を受けたetcdのデータディレクトリとスタックトレースをバグ報告に添付してください。

- 問題が切り分けられていること。できる限り依存関係を最小限にして、バグを切り分け、再現してください。バグ報告に多すぎる依存関係が含まれていると、修正に大幅に時間がかかります。etcdに依存する外部システムのデバッグは対象外ですが、適切な方向性についての助言やetcd自体の使用方法については、喜んで支援します。

- 重複していないこと。既存のバグ報告と重複する報告はしないでください。

- 範囲が限定されていること。1つの報告につきバグは1つとしてください。同じ報告の中で、別のバグについて追記しないでください。

バグを報告する前に、[適切なバグ報告の書き方に関するElika Etemadの記事][filing-good-bugs]を読むと役立つかもしれません。

バグの原因を特定するため、追加の情報をお願いする場合があります。重複したバグ報告はクローズします。

## よくある質問 {#frequently-asked-questions}

### スタックトレースの取得方法 {#how-to-get-a-stack-trace}

``` bash
$ kill -QUIT $PID
```

### etcdのバージョンの確認方法 {#how-to-get-etcd-version}

``` bash
$ etcd --version
```

### systemdサービス「etcd2.service」として実行されるetcdの構成とログを取得する方法 {#how-to-get-etcd-configuration-and-log-when-it-runs-as-systemd-service-etcd2service}

``` bash
$ sudo systemctl cat etcd2
$ sudo journalctl -u etcd2
```

アップストリームのsystemdのバグにより、プロセスの終了時にjournaldがログの最後の数行を記録しない場合があります。journalctlでetcdが停止したと表示されるのにfatalまたはpanicメッセージがない場合は、`sudo journalctl -f -t etcd2`を試して完全なログを取得してください。

[etcd-issue]: https://github.com/etcd-io/etcd/issues/new
[filing-good-bugs]: http://fantasai.inkedblade.net/style/talks/filing-good-bugs/
