---
title: Contributing code
linkTitle: Contribution guide
description: Submit tested code, useful documentation, and changes that respect third-party rights.
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/contributing.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Guidelines for contributing code or documentation {#guidelines-for-contributing-code-or-documentation}

Thank you for your interest in contributing to Babelfish.
Please read through these guidelines before you submit any pull requests or
issues. 

The Babelfish project is open to contributions. You can send a [pull request via
Github](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to contribute to Babelfish.


### Submitting code or documentation {#submitting-code-or-documentation}

When submitting code or documentation, ensure that your code adheres to
[community standards](https://www.postgresql.org/docs/current/source.html) and your
documentation and comments conform to the [Writing style guidelines](https://github.com/babelfish-for-postgresql/babelfish_project_website#writing-style-guidelines). 
This will ease the burden of maintenance, and keep the Babelfish code and website sustainable.

Before submitting a pull request, make sure that your code is properly tested; changes made to 
the code should not compromise existing features. We strongly recommend running the tests
before you send a pull request to development. If you submit a new feature, include 
test cases for the feature.  Patches that do not contain tests for new features will not be 
accepted.

We strongly encourage you to properly document your code.  If you are having language difficulty, or 
need help, reach out to the Babelfish community.

When documenting a new feature, it is a good idea to provide working examples in the 
documentation.  This is especially true for programming interfaces and new SQL functions. 

If you are not a coder yourself, or if you don't want to write your own patch, we
can offer help. Positive feedback is always appreciated; we are particularly interested in 
receiving your feedback:

- for new content,
- to remove inaccuracies,
- to fill information gaps,
- to fix typos or grammatical errors, and
- to improve clarity.

To get involved with the review process, please check out
[Github](https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish).


### Avoiding license violations {#avoiding-license-violations}

If you contribute code, make sure that you are not violating 3rd party rights.
Checking for intellectual property violations beforehand is expected by the community. We want
Babelfish and our users to be free of 3rd party claims. Keeping the code clean benefits 
the community as well our users.

Babelfish for PostgreSQL is available as Open Source software and can be downloaded from Github for
free under the terms of the
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0) and the
[PostgreSQL license](https://www.postgresql.org/about/licence/).
