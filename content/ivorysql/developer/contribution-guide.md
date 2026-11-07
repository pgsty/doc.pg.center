---
title: IvorySQL community contribution guide
linkTitle: Community contribution
description: 'IvorySQL v5.6 documentation: IvorySQL community contribution guide.'
type: docs
weight: 530
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/8.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---


## 1. **Summary** {#summary}

### 1.1. Illustration {#illustration}

IvorySQL is maintained by a core development team, which has commit access to the main repository of IvorySQL on GitHub. We are eager to get contributions from members of the wider IvorySQL community. If you want to see your changes to code or documents added to IvorySQL and appear in future versions, you need to understand the content of this section.

​IvorySQL community welcomes and appreciates all types of contributions and we are looking forward to your participation!

### 1.2. Principles of Conduct {#principles-of-conduct}

Every member, contributor and leader should read our **principles of conduct**. We promise that everyone can participate in community and pay equal attention to everyone, no matter who.

We are committed to acting and interacting in a way that contributes to the establishment of an open, enthusiastic, diverse, inclusive and healthy community.

### 1.3. Description of Community Governance {#description-of-community-governance}

Our team is a continuously open team, focusing on parts of IvorySQL. In our team, there are reviewers, submitters and maintainers, and we have one or more repositories. The decision for the team is made by the maintainer. The typical promotion path for IvorySQL developers is from user to reviewer, then submitter and maintainer. But getting more roles doesn’t mean you have any privileges to other community members. Everyone in the IvorySQL community is equal and has the responsibility to cooperate constructively with other contributors to build a friendly community. These roles are natural rewards for your significant contributions to the development of IvorySQL, and provide you with more rights in the development workflow to improve your efficiency. At the same time，this requires you to undertake some additional duty:

​Team honor: now you are already one of the team reviewers/submitters/maintainers, it means that you represent the project and your team members. So, please be Mr.Nice Guy to defend the reputation of the team.

​Responsibility: submitters/maintainers have the right to merge pull requests, therefore, they take additional responsibility to deal with the consequences of accepting changes to the code base or documents. When a bug occurs, they should fix it. If they can not solve it, they should roll back the project. Also, they need to help the release manager solve any problems found in the test cycle.

## 2. **Contributor’s Guide** {#contributors-guide}

Before contributing, we need to know the current version of IvorySQL and the version of the document.At present, we maintain versions after version **5.6**. Our version follows the update pace of PG. Please update to the latest version before contributing. After that, we need to read the format requirements carefully and be familiar with code format, code comment format, issue format, pull PR title format, document contribution format, and article contribution format. These can help you become a contributor of IvorySQL as soon as possible.

### 2.1. Preparation before Contribution {#preparation-before-contribution}

#### 2.1.1. Getting started {#getting-started}

IvorySQL is developed on GitHub. Anyone who wishes to contribute to it must have a Github account and be familiar with Git tools and workflow. It is also recommended that you follow the developer’s mailing list since some of the contributions may generate more detailed discussions there.

Once you have your GitHub account, fork this repository so that you can have your private copy to start hacking on and to use as a source of pull requests.

#### 2.1.2. Licensing of IvorySQL contributions {#licensing-of-ivorysql-contributions}

If the contribution you’re submitting is original work, you can assume that IvorySQL will release it as part of an overall IvorySQL release available to the downstream consumers under **the Apache License, Version 2.0**.

If the contribution you’re submitting is NOT original work you have to indicate the name of the license and also make sure that it is similar in terms to the Apache License 2.0. Apache Software Foundation maintains a list of these licenses under Category A. In addition to that, you may be required to make proper attributions.

Finally, keep in mind that it is NEVER a good idea to remove licensing headers from the work that is not your original one. Even if you are using parts of the file that originally had a licensing header at the top you should err on the side of preserving it. As always, if you are not quite sure about the licensing implications of your contributions, feel free to reach out to us on the developer mailing list.

### 2.2. What Contribution Can You Make {#what-contribution-can-you-make}

#### 2.2.1. Code Contribution {#code-contribution}

You can upload your modified bugs, new functions and other codes to your personal warehouse, and finally submit PR requests to merge them on the official website: <a href="https://github.com/IvorySQL/IvorySQL" class="bare">https://github.com/IvorySQL/IvorySQL</a>.

#### 2.2.2. Document Contribution(<a href="https://www.ivorysql.org/zh-CN/docs/intro" class="bare">https://www.ivorysql.org/zh-CN/docs/intro</a>) {#document-contributionhttpswww-ivorysql-orgzh-cndocsintro}

The IvorySQL community provides Chinese and English documents. English documents are saved in …​ document repository, Chinese documents are saved in i18n document repository. You can contribute to one of them or both.

When you add or update a plugin compatibility document, you must also update the plugin summary table in [IvorySQL Ecosystem Plugin Compatibility List](/ivorysql/ecosystem/extensions/). Keep the plugin name, version, function description, use cases, and link to the detail page in sync so that the overview page and the detail page stay consistent.

#### 2.2.3. Test IvorySQL and Report Bugs {#test-ivorysql-and-report-bugs}

GitHub: <a href="https://github.com/IvorySQL/IvorySQL" class="bare">https://github.com/IvorySQL/IvorySQL</a>

Gitee:https://gitee.com/IvorySQL/

#### 2.2.4. Participate in the Construction of IvorySQL Website {#participate-in-the-construction-of-ivorysql-website}

IvorySQL official website:https://github.com/IvorySQL/Ivory-www

#### 2.2.5. Answer Questions on the Mailing List {#answer-questions-on-the-mailing-list}

Mailing List website:https://lists.ivorysql.org/

#### 2.2.6. Contribute Article {#contribute-article}

You can submit your article to the blog in the IvorySQL-WWW code warehouse, or send it to the mailbox <renjiao@highgo.com>.

### 2.3. How to Contribute {#how-to-contribute}

#### 2.3.1. Coding Guidelines {#coding-guidelines}

Your chances of getting feedback and seeing your code merged into the project greatly depend on how granular your changes are. If you happen to have a bigger change in mind, we highly recommend engaging on the developer’s mailing list first and sharing your proposal with us before you spend a lot of time writing code. Even when your proposal gets validated by the community, we still recommend doing the actual work as a series of small, self-contained commits. This makes the reviewer’s job much easier and increases the timeliness of feedback.

When it comes to C and C++ parts of IvorySQL, we follow PostgreSQL Coding Conventions. In addition to that:

For C and Perl code, please run pgindent if necessary. We recommend using git diff --color when reviewing your changes so that you don’t have any spurious whitespace issues in the code that you submit.

All new functionality that is contributed to IvorySQL should be covered by regression tests that are contributed alongside it. If you are uncertain about how to test or document your work, please raise the question on the ivorysql-hackers mailing list and the developer community will do its best to help you.

At the very minimum, you should always be running

```
make installcheck world
```

to make sure that you’re not breaking anything.

#### 2.3.2. Changes applicable to upstream PostgreSQL {#changes-applicable-to-upstream-postgresql}

If the change you’re working on touches functionality that is common between PostgreSQL and IvorySQL, you may be asked to forward-port it to PostgreSQL. This is not only so that we keep reducing the delta between the two projects, but also so that any change that is relevant to PostgreSQL can benefit from a much broader review of the upstream PostgreSQL community. In general, it is a good idea to keep both codebases handy so you can be sure whether your changes may need to be forward-ported.

#### 2.3.3. Patch submission {#patch-submission}

Once you are ready to share your work with the IvorySQL core team and the rest of the IvorySQL community, you should first create or claim the corresponding GitHub Issue, then push all the commits to a branch in your own repository forked from the official IvorySQL and send us a pull request. Every pull request must correspond to at least one Issue so that the change request, discussion, review, and merge result remain traceable.

#### 2.3.4. Patch review {#patch-review}

A submitted pull request with passing validation checks is assumed to be available for peer review. Peer review is the process that ensures that contributions to IvorySQL are of high quality and align well with the road map and community expectations. Every member of the IvorySQL community is encouraged to review pull requests and provide feedback. Since you don’t have to be a core team member to be able to do that, we recommend following a stream of pull reviews to anybody who’s interested in becoming a long-term contributor to IvorySQL.

One outcome of the peer review could be a consensus that you need to modify your pull request in certain ways. GitHub allows you to push additional commits into a branch from which a pull request was sent. Those additional commits will be then visible to all of the reviewers.

A peer review converges when it receives at least one +1 and no -1s votes from the participants. At that point, you should expect one of the core team members to pull your changes into the project.

At any time during the patch review, you may experience delays based on the availability of reviewers and core team members. Please be patient. That being said, don’t get discouraged either. If you’re not getting expected feedback for a few days add a comment asking for updates on the pull request itself or send an email to the mailing list.

#### 2.3.5. Direct commits to the repository {#direct-commits-to-the-repository}

On occasion, you will see core team members committing directly to the repository without going through the pull request workflow. This is reserved for small changes only and the rule of thumb we use is this: if the change touches any functionality that may result in a test failure, then it has to go through a pull request workflow. If, on the other hand, the change is in the non-functional part of the codebase (such as fixing a typo inside of a comment block) core team members can decide to just commit to the repository directly.

## 3. **Submit Issue** {#submit-issue}

### 3.1. First: Get into New issue page: {#first-get-into-new-issue-page}

1 Enter IvorySQL official website:https://github.com/IvorySQL/IvorySQL

2 Click New issue

![p3](/ivorysql/assets/images/upstream/8413f3ab712dab5baf51bf0d23f03b470b99835933d742721e29bd45afa3263c.png)

#### 3.1.1. Second:Select the issue type {#secondselect-the-issue-type}

**1 bug report**

```
Title:
```

```
## Bug Report
Describe the bug


\### IvorySQL Version
The version of IvorySQL you are using

\### OS Version (uname -a)
Operating system version(uname -a)

\### Configuration options  ( config.status --config )


\### Current Behavior


\### Expected behavior/code


\### Step to reproduce


\### Additional context that can be helpful for identifying the problem
```

**2 Enhancement**

```
Title:
```

```
## Enhancement
Describe the functions that you expect to be strengthened
```

**3 Feature Request**

```
Title:
```

```
## Feature Request
Describe the feature that you expect to be real
```

#### 3.1.2. Third: Submit {#third-submit}

Click submit new issue button. WELL DONE!

## 4. **Contribute Code** {#contribute-code}

### 4.1. First: Fork [ivorysql.org](https://ivorysql.org/) warehouse {#first-fork-ivorysql-org-warehouse}

1 Open the ivorysql warehouse: <a href="https://github.com/IvorySQL/IvorySQL" class="bare">https://github.com/IvorySQL/IvorySQL</a>

2 Click the fork button in the upper right corner, Wait for the fork to finish

Before you start coding or editing documents, make sure there is a corresponding GitHub Issue for the change. You can create a new Issue or claim an existing one, but do not submit a PR without an associated Issue.

### 4.2. Second: Clone the warehouse to local {#second-clone-the-warehouse-to-local}

```
cd $working_dir #  $working_dir can be replaced by the directory where you want to place repo. For example, `cd ~/Documents/GitHub`

git clone git@github.com:$user/IvorySQL.git # `$user` can be replaced by your GitHub ID.
```

### 4.3. Third: Create a new Branch {#third-create-a-new-branch}

```
cd $working_dir/IvorySQL

git checkout -b new-branch-name
```

### 4.4. Fourth: Edit Document or Modify Code {#fourth-edit-document-or-modify-code}

You can modify the code in new-branch-name.

### 4.5. Fifth: Generate commit {#fifth-generate-commit}

```
Git add <file>

Git commit -m “commit-message”
```

### 4.6. Sixth: Push the modification to the remote end {#sixth-push-the-modification-to-the-remote-end}

```
Git push -u origin new-branch-name
```

### 4.7. Seventh: Create a Pull Request {#seventh-create-a-pull-request}

1 Open your warehouse: [https://github.com/\$user/IvorySQL](https://github.com/$user/docs-cn) (\$user is your GitHub ID) .

2 Click Compare & pull request button and create a PR.

3 In the PR title or description, explicitly reference the corresponding Issue number, for example `Fixes #123` or `Refs #123`.

## 5. **Submit PR** {#submit-pr}

A PR submission should contain only one function or one bug. Prohibit submitting multiple functions at one time.

Every GitHub PR must have a corresponding Issue. A PR without an associated Issue does not meet the community contribution process requirements.

### 5.1. Fill in PR information {#fill-in-pr-information}

```
Fix test
Describe the function
```

```
leave a comment
Give a detailed description of the submission function
```

Reference the related Issue in the PR description and keep the Issue number visible to reviewers, for example `Fixes #123`.

### 5.2. Submit PR {#submit-pr-2}

Click Create pull request button. WELL DONE!

## 6. **Edit Documents** {#edit-documents}

### 6.1. Preparation {#preparation}

(1) Download Markdown or Typora document editor.

(2) Check whether the source warehouse has updates. If there are updates, please update and synchronize to your own warehouse first. Refer to the following steps to update to the latest version:

```
git remote

git fetch upstream

git merge upstream/main

git push
```

(3) Familiar with format [&#91;\_pecification&#93;](#specification).

### 6.2. Where to Contribute {#where-to-contribute}

The IvorySQL community provides Chinese and English documents. English documents are saved in IvorySQL document repository, Chinese documents are saved in i18n document repository. You can contribute to one of them or both.

You can start from any of following to help improve the IvorySQL documents on the IvorySQL website:

​(1) Prepare complete documents.

​(2) Fix incorrect spelling and formatting (Punctuation, space, indentation, code block, etc) .

​(3) Improper or outdated instructions corrected or updated.

​(4) Add missing content (sentences, paragraphs, or new documents) .

​(5) Translate document from English to Chinese, or from Chinese to English.

​(6) Submit, reply and resolve document issues or document-i18n issues.

​(7) (Advanced) View pull requests created by others.

### 6.3. Specification {#specification}

The IvorySQL document is written in 'markdown'. To ensure the quality and consistency of the format, certain Markdown rules should be followed when modifying and updating the document.

**Markdown Specification**

​1 Titles are used incrementally from the first level, and skipping is prohibited. For example: The third level title cannot be used directly under the first level title; The fourth level title cannot be used directly under the second level title.

​2 The title must use the ATX style uniformly. Indicate the title level by adding \# before the title.

​3 The leading symbol \# of the title must be followed by a blank space.

​4 The leading symbol "#" of the title can only be followed by one blank space and then the title content. There can be no more than one space.

​5 The title must appear at the beginning of a line, there must be no space before the \# sign of the title.

​6 Only Chinese and English question marks, back quotes, Chinese and English single and double quotes and other symbols can appear at the end of the title. Other symbols such as colon, comma, period and exclamation point cannot be used at the end of the title.

​7 One line must be empty above the title.

​8 The same title cannot appear continuously in the document. If the first level title is \# TiDB architecture, the next level title cannot be \# \# TiDB architecture. If it is not a continuous title, the title content can be repeated.

​9 Only one first level title in document.

​10 In general, except for TOC.md files, which can be indented by two spaces, other .md files must be indented by four spaces by default foe each level of indentation.

​11 Tab is not allowed in documents(including code blocks) . If indentation is required, spaces must be uniformly used instead.

​12 Continuous blank lines are prohibited.

​13 Multiple spaces are not allowed after the block reference symbol \> . Only one space can be used, followed by the reference content.

​14 When using a ordered list, it must start from 1 and increase in order.

​15 When using a list, the identifier (+, -, \* or number) of each list item can only be left blank, followed by the list content.

​16 The list (includeing ordered and unordered lists) must be empty before and after each line.

​17 There must be one blank line before and after the code block.

​18 Exposed URLs are prohibited in documents. If you want users to click and open the URL directly, wrap the URL with a pair of angle brackets (\<URL\>) . If the exposed URL must be used due to special circumstances, and the user does not need to open it by clicking, a pair of back quatation marks (`URL`) will be used to wrap the URL.

​19 When using bold, italic and other emphasis effects, redundant spaces are prohibited in the emphasis identifier, such as ` `**`text`**` `.

​20 No extra space is allowed in the code block wrapped by a single backquote, such as \` text \`.

​21 No extra spaces are allowed on both sides of the link text, such as &#91;Link&#93;(/ivorysql/developer/contribution-guide/<a href="https://www.example.com/" class="bare">https://www.example.com/</a>)

​22 The link must have a link path. &#91;Empty link&#93;() and &#91;empty link&#93;() are not allowed.

### 6.4. Example {#example}

1 Titles are used incrementally from the first level, and skipping is prohibited.

```
# Heading 1
### Heading 3

We skipped out a 2nd level heading in this document
```

2 The title must use the ATX style uniformly. Indicate the title level by adding \# before the title.

```
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
## Another Heading 2
### Another Heading 3
```

3 The leading symbol \# of the title must be followed by a blank space. Multiple spaces after \# are prohibited, and spaces before \# are prohibited.

Incorrect Example:

```
# Heading 1
## Heading 2
```

Correct Example:

```
# Heading 1
## Heading 2
```

4 Only Chinese and English question marks, back quotes, Chinese and English single and double quotes and other symbols can appear at the end of the title.

Incorrect Example:

```
# This is a heading.
```

Correct Example:

```
# This is a heading
```

5 One line must be empty above the title.

Incorrect Example:

```
# Heading 1
Some text
Some more text## Heading 2
```

Correct Example:

```
# Heading 1
Some text
Some more text

## Heading 2
```

6 he same title cannot appear continuously in the document. If the first level title is \# TiDB architecture, the next level title cannot be \## TiDB architecture. If it is not a continuous title, the title content can be repeated.

Incorrect Example:

```
# Some text

## Some text
```

Correct Example:

```
# Some text

## Some more text
```

7 Only one first level title in document.

Incorrect Example:

```
# Top level heading

# Another top-level heading
```

Correct Example:

```
# Title

## Heading

## Another heading
```

8 In general, except for TOC.md files, which can be indented by two spaces, other .md files must be indented by four spaces by default foe each level of indentation.

Incorrect Example:

```
* List item
  * Nested list item indented by 3 spaces
```

Correct Example:

```
* List item
    * Nested list item indented by 4 spaces
```

9 Tab is not allowed in documents(including code blocks) . If indentation is required, spaces must be uniformly used instead.

Incorrect Example:

```
Some text
    * hard tab character used to indent the list item
```

Correct Example:

```
Some text
  * Spaces used to indent the list item instead
```

10 Continuous blank lines are prohibited.

Incorrect Example:

```
Some text here


Some more text here
```

Correct Example:

```
Some text here

Some more text here
```

11 Multiple spaces are not allowed after the block reference symbol \> . Only one space can be used, followed by the reference content.

Incorrect Example:

```
>  This is a blockquote with bad indentation>  there should only be one.
```

Correct Example:

```
> This is a blockquote with correct> indentation.
```

12 When using a ordered list, it must start from 1 and increase in order.

Incorrect Example:

```
1. Do this.
1. Do that.
1. Done.
```

```
0. Do this.
1. Do that.
2. Done.
```

```
Correct Example:
```

```
1. Do this.
2. Do that.
3. Done.
```

13 When using a list, the identifier (+, -, \* or number) of each list item can only be left blank, followed by the list content.

Correct Example:

```
* Foo
* Bar
* Baz

1. Foo
  * Bar
1. Baz
```

14 The list (includeing ordered and unordered lists) must be empty before and after each line.

Incorrect Example:

```
Some text* Some* List

1. Some2. List

Some text
```

Correct Example:

```
Some text

* Some
* List

1. Some
2. List

Some text
```

15 There must be one blank line before and after the code block.

Incorrect Example:

```
Some text
​```
Code block
​```
​```
Another code block
​```
Some more text
```

Correct Example:

```
Some text

​```
Code block
​```

​```
Another code block
​```

Some more text
```

16 Exposed URLs are prohibited in documents. If you want users to click and open the URL directly, wrap the URL with a pair of angle brackets (\<URL\>) . If the exposed URL must be used due to special circumstances, and the user does not need to open it by clicking, a pair of back quatation marks (`URL`) will be used to wrap the URL.

Incorrect Example:

```
For more information, see https://www.example.com/.
```

Correct Example:

```
For more information, see <https://www.example.com/>.
```

17 When using bold, italic and other emphasis effects, redundant spaces are prohibited in the emphasis identifier, such as ` `**`text`**` `.

Incorrect Example:

```
Here is some ** bold ** text.

Here is some * italic * text.

Here is some more __ bold __ text.

Here is some more _ italic _ text.
```

Correct Example:

```
Here is some **bold** text.

Here is some *italic* text.

Here is some more __bold__ text.

Here is some more _italic_ text.
```

18 No extra space is allowed in the code block wrapped by a single backquote, such as \` text \`.

Incorrect Example:

```
some text
 some text
```

Correct Example:

```
some text
```

19 No extra spaces are allowed on both sides of the link text, such as &#91; Link &#93;(/ivorysql/developer/contribution-guide/<a href="https://www.example.com/" class="bare">https://www.example.com/</a>) . Incorrect Example:

```
[a link](https://www.example.com/)
```

Correct Example:

```
[a link](https://www.example.com/)
```

20 The link must have a link path. &#91;Empty link&#93;() and &#91;empty link&#93;() are not allowed.

Incorrect Example:

```
[an empty link]()

[an empty fragment](#)
```

Correct Example:

```
[a valid link](https://example.com/)

[a valid fragment](#fragment)
```

21 Code blocks in the document are wrapped with three backquote, and the use of indented four-space code blocks is prohibited.

Incorrect Example:

```
Some text.

  # Indented code

More text.
```

Correct Example:

```
​```ruby
# Fenced code
​```

More text.
```

### 6.5. Environmental preparation {#environmental-preparation}

In order to test your modifications, you need to prepare the following environment.

- `Node.js` install

- `Antora` install

Please refer to [Antora docs](https://docs.antora.org/antora/latest/)。

After installation, the following display on the terminal indicates successful installation.

![14](/ivorysql/assets/images/upstream/c75c24c7e85ebd0eb985888a524c183f0ad32008359772ed8ef7dde289b63618.png)

### 6.6. Generate web pages {#generate-web-pages}

- Firstly, you need to know the location of the corresponding UI for the webpage, as shown in the following figure:

![15](/ivorysql/assets/images/upstream/a2f18467e4b1183b0fa694def132feded1bff1f82a53e3538ef02c4c0d22591f.png)

The UI templates for both Chinese and English web pages are basically the same, so when making modifications, it is best to ensure that both templates are modified at the same time. After uploading the modified UI to your personal Github, you can consider generating your modified web page locally.

IvorySQL Document Site is built by `Antora`. Before running `Antora`, remember to modify the corresponding `playbook.yml` file.

![16](/ivorysql/assets/images/upstream/566ddaa6428efab78f316f283b6efcdbab6842df75b27341b5ff88ea194beb97.png) ![17](/ivorysql/assets/images/upstream/7473ef2cd6340ac2cce7a42e580c38046f7cd2388824cba909bf3707abb80d58.png)

After completing the above process, please run the command `antora antora-playbook.yml --stacktrace` on the terminal, and then patiently wait. After the successful operation is completed, you can view the webpage you have generated.

You can start uploading to our **ivorysql_web**, the process of submitting PR is the same as before. Thank you for your contribution to the community <sup>\_</sup>. We will consider whether to update the website after the review.

## 7. Submit Blog {#submit-blog}

### 7.1. Preparation {#preparation-2}

1 Download [Markdown](https://markdown.com.cn/tools.html#%E7%BC%96%E8%BE%91%E5%99%A8) or [Typora](https://typoraio.cn/) .

2 Check whether the source warehouse (<a href="https://github.com/IvorySQL/Ivory-www" class="bare">https://github.com/IvorySQL/Ivory-www</a>) has updates. If there are updates, please update and synchronize to your own warehouse first. Refer to the following steps to update to the latest version:

``` bash
# Download source code
git clone https://github.com/IvorySQL/Ivory-www.git
# Synchronize updates warehouse
git pull
```

3 Familiar with format ([&#91;\_specification_2&#93;](#specification-2))

### 7.2. Where to Congtribute {#where-to-congtribute}

The IvorySQL community provides Chinese and English documents. English documents are saved in IvorySQL document repository, Chinese documents are saved in i18n document repository. You can contribute to one of them or both.

### 7.3. How to Contribute {#how-to-contribute-2}

Let’s take a quick look at the information about the maintenance of the IvorySQL blog before contributing. It is helpful for you to submit blog and to be a contributor.

(1) Clone code to local warehouse

``` bash
git clone https://github.com/IvorySQL/Ivory-www.git
```

(2) Create a branch

``` bash
git checkout -b <branch-name>
```

(3) Create a directory of your own articles in the blog directory, and please name your own directory according to the (&#91;Specification&#93;(#7.4 Specification) ) .

``` bash
# Make English blog directory and files
cd Ivory-www/blog
mkdir <YEAR-MONTH-DAY-title>
cd <YEAR-MONTH-DAY-title>
touch index.md
# Make Chinese blog directory and files
cd Ivory-www/i18n/zh-CN/docusaurus-plugin-content-blog
mkdir <YEAR-MONTH-DAY-title>
cd <YEAR-MONTH-DAY-title>
touch index.md
```

(4) Write the blog to publish in index.md, put the required pictures in the blog in the same directory as index.md.

(5) Submit Blog

``` bash
git add <file-path>
git commit -m "<message>"
git push origin <branch-name>:<branch-name>
```

### 7.4. Specification {#specification-2}

#### 7.4.1. Submit specifications {#submit-specifications}

(1) Format of folder naming: **year-month-day-foldername**

```
Example: 2022-1-28-ivorysql-arrived
```

(2) File property is **index.md**

(3) Picture property is **.png**, and put the pictures to be uploaded into the folder to be submitted in advance.

**Notice:**The name of every picture is unique and cannot be repeated.

Example: po-one.png

#### 7.4.2. Write blog {#write-blog}

Blogs are written in markdown or Typora, you can understand the design of blog by reading [Blog \| Docusaurus](https://docusaurus.io/zh-CN/docs/blog).

(1) The header of blog includes the following information:

```
---
slug: IvorySQL
title: Welcome to IvorySQL community
authors: [official]
authorTwitter: IvorySql
tags: [IvorySQL, Welcome, Database, Join Us]
---
```

**Prompt:**You can copy the above template to your file and edit it.

**Notice:**1) Add one space after slug, title, authors, tags.

2) The name of every slug is unique, the Chinese and English versions of the same blog can be the same.

(2) Text format

The text paragraph title is **h2**/"**Second level title**";

The body uses the default font size.

(3) Naming format of inserted pictures

&#91;Hello&#93;(/ivorysql/developer/contribution-guide/Hello-banner.png)

(4) Naming format of inserted hyperlink

&#91;name&#93;(/ivorysql/developer/contribution-guide/link)

[Github page](https://github.com/IvorySQL/) Download source code and published packages.

## 8. Website Contribution Guide {#website-contribution-guide}

[IvorySQL Document Site](https://docs.ivorysql.org) uses [`Antora`](https://antora.org/) to build. Also, IvorySQL Document Site is open source. It consists of three parts, such as [`ivorysql_docs`](https://github.com/IvorySQL/ivorysql_docs), [`ivorysql_web`](https://github.com/IvorySQL/ivorysql_web) and [`ivory-doc-builder`](https://github.com/IvorySQL/ivory-doc-builder).

Welcome everyone who is willing to participate in open source work to join us, and remember to follow our code of conduct <sup>\_</sup>.

### 8.1. How to Contribute {#how-to-contribute-3}

Due to the fact that IvorySQL Document Site is all hosted on Github, this allows any users to `fork` our document repository into their personal repository, make modifications to it, and then submit a PR. After being reviewed by our open source team, the modifications can be updated to our Document Site.

In order to achieve the goat of correcting document errors more conveniently, you first need to establish a personal warehouse according to the size you want to update. As follows:

- If you want to modify the existing content or add a new page, you only need to `fork` [ivorysql_docs](https://github.com/IvorySQL/ivorysql_docs) to your personal repository.

![7](/ivorysql/assets/images/upstream/4fa14b6cbc829452e2ebae365db0314f80559ff37c0e42cb16d76af94a03ed02.png)

- If you want to participate more deeply in the construction of IvorySQL Document Site, in addition to the `ivorysql_docs`, you also need to `fork` [ivorysql_web](https://github.com/IvorySQL/ivorysql_web) and [ivory-doc-builder](https://github.com/IvorySQL/ivory-doc-builder) to your personal repository.

![8](/ivorysql/assets/images/upstream/f0c0da234bdf1ebcf856dbb1f6f893c13862c215c3fc1b814f271900e075b20d.png) ![9](/ivorysql/assets/images/upstream/844612152db2b64500b91064cae47ec657cce26abbe205ad0f8aae572885f3d6.png)

### 8.2. Modify Content {#modify-content}

This section will introduce the process of modifying webpage content after discovering that it is inappropriate.

- In the upper right corner of a webpage with incorrect content, there is a button called `edit this page`, click on the button. As shown in the figure:

![10](/ivorysql/assets/images/upstream/fcd7e7b28443e0de16e038c2e3f289c6721eb99fba5c0e2bdc5fda7401943efb.png)

- After clicking, it will redirect to the editing page where we store the current page source `.adoc` file. Please modify the content in the `Asciidoc` format. As shown in the figure:

![11](/ivorysql/assets/images/upstream/20d483bb9da5bb11b9facf88a28b4cb55efe910afe2a6362b0de9525d4531b3a.png)

- After editing is completed. As shown in the figure:

![12](/ivorysql/assets/images/upstream/35e220830fcffe33f8abf5d46fb32ef73e39ce9103853915deda13f62b309536.png)

- After confirming the update. As shown in the figure:

![13](/ivorysql/assets/images/upstream/72694370f6abc1423be648721ad50d72417cb1ee5dbfa0365df22ff1a62cd862.png)

- Next, the relevant person of the open source team will be responsible for reviewing the content you submitted. After the review is completed, the updates you submitted will appear on the corresponding page.

### 8.3. Add Page {#add-page}

This section will introduce how to add new page components to a website, and the modifications involved in adding new pages mainly include the following:

- Add the `.adoc` file in the `CN/modules/ROOT/pages/vX.X`.

- Modify the `CN/modules/ROOT/nav.adoc`. If the modification involves modifying or adding images, please modify the images in `images`.

- Add the `.adoc` file in the `EN/modules/ROOT/pages/vX.X`.

- Modify the `EN/modules/ROOT/nav.adoc`. If the modification involves modifying or adding images, please modify the images in `images`.

  1.  Firstly, you need to download the warehouse that you `fork` from `IvorySQL` to your personal computer.

      ```
      git clone https://github.com/$username$/ivorysql_docs.git
      ```

  2.  Then, place the `.adoc` file to be added in the correct directory, remembering that both Chinese and English files should be prepared (**Chinese and English files should have the same name**), and each file should be placed in the correct directory. At the same time, modify the corresponding `nav.adoc` file (the modification method can refer to the existing content of the file).

  3.  After the above modifications are completed, submit them to the personal warehouse first.

      ```
      git add .
      git commit -m "$describe your change$"
      git push
      ```

  4.  Afterwards, submit the PR as follows

![13](/ivorysql/assets/images/upstream/72694370f6abc1423be648721ad50d72417cb1ee5dbfa0365df22ff1a62cd862.png)

### 8.4. Test {#test}

If you are not satisfied with simply submitting on the webpage or only modifying the webpage content, or if you want to modify the webpage UI, this section will help you.

Before reading this section, you need to confirm whether your Github personal repository has `forked` [ivorysql_docs](https://github.com/IvorySQL/ivorysql_docs), [ivorysql_web](https://github.com/IvorySQL/ivorysql_web) and [ivory-doc-builder](https://github.com/IvorySQL/ivory-doc-builder).

### 8.5. Deploy web pages {#deploy-web-pages}

The deployment of web pages is currently the responsibility of the open-source team. We value every submission and issue, so please do not worry about your contribution to the community being buried.

### 8.6. Tip {#tip}

If you don’t have much time, you can send an email to **ivorysql-docs@ivorysql.org**. We will have dedicated staff to handle every your letter, and we looking forward to hearing from you.
