---
title: 使用 C 编程
linkTitle: C / FreeTDS
description: 使用 FreeTDS 编写 C 客户端，处理连接、编译与错误。
weight: 40
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/c.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

## 准备编写 C 代码 {#preparing-to-write-c-code}

本节演示如何编写简单的 C/C++ 程序访问 Babelfish。示例并不是完整、安全的应用程序，而是说明程序与 Babelfish 交互所需的一些功能。

示例针对 Fedora Core 34 Linux，使用大多数 Linux 发行版都提供的 FreeTDS 库。

首先[安装并配置 FreeTDS 驱动](https://www.freetds.org/)：

```bash
[root@fedora ~]# dnf install freetds*
Last metadata expiration check: 0:02:52 ago on Fr 24 Sep 2021 11:11:43 CEST.
Dependencies resolved.
====================================================================================================================================================
 Package                               Architecture                   Version                                  Repository                      Size
====================================================================================================================================================
Installing:
 freetds                               x86_64                         1.1.20-4.fc34                            fedora                         373 k
 freetds-devel                         x86_64                         1.1.20-4.fc34                            fedora                          39 k
 freetds-doc                           noarch                         1.1.20-4.fc34                            fedora                         1.0 M
Installing dependencies:
 freetds-libs                          x86_64                         1.1.20-4.fc34                            fedora                         423 k
```

使用 C 开发时，还需安装包含头文件的 `freetds-devel` 包，编译时会用到这些文件。

## 连接数据库 {#connecting-to-the-database}

示例的第一部分处理头文件、变量定义和错误处理，同时使用标准 C 库的头文件（`stdio.h`、`stdlib.h`、`unistd.h`、`sys/param.h`）及 FreeTDS 的头文件（`sybfront.h`、`sybdb.h`、`syberror.h`）：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/param.h>
#include <sybfront.h>
#include <sybdb.h>
#include <syberror.h>


#define  UID       "postgres"  
#define  PWD       "verysecret!"
#define  PROGNAME  "demo_prog"
#define  DBSERVER  "sample-host.example.com"
#define  DBNAME    "postgres"


/* handler for messages from the server */
static int
msg_handler(DBPROCESS* dbproc, DBINT msgno, int msgstate, int severity, 
	char *msgtext, char *srvname, char *procname, int line)
{
	/* regular errors are handled by the error handler */
	if (severity < 11)
        	fprintf(stderr, "Server message (severity %d): %s\n", severity, msgtext);

	return 0;
}

/* error handler */
static int err_handler(DBPROCESS* dbproc, int severity, int dberr, int oserr, char *dberrstr, char *oserrstr)
{
	fprintf(stderr, "Server error %d: %s\n", dberr, dberrstr);
	if (oserr != 0)
        	fprintf(stderr, "Caused by system error %d: %s\n", oserr, oserrstr);

	return INT_CANCEL;
}

```

初始化 FreeTDS 库前，先声明局部变量：

```c
int main(void)
{
  	LOGINREC 	*login;
  	DBPROCESS 	*dbconn;
  	char 		hostname[MAXHOSTNAMELEN];
  	int 		max_len = MAXHOSTNAMELEN;
  	DBCHAR 		accession[10];
  	DBCHAR 		examdesc[10];
  	DBCHAR 		examcode[255];

  	if (dbinit() == FAIL) 
	{
    		fprintf(stderr, "Could not init db.\n");
    		return 1;
  	}
```

然后分配登录结构，并在登录句柄中设置登录 ID、密码和主机名：

```c

  	/* Allocate a login params structure */	
	if ((login = dblogin()) == FAIL) 
	{
		fprintf(stderr, "Could not initialize dblogin() structure.\n");
    		return 2;
  	}

	/* Initialize the login params in the structure */
	DBSETLUSER(login, UID);
	DBSETLPWD(login, PWD);

	if (gethostname(hostname, max_len) == 0)
	{
    		DBSETLHOST(login, hostname);
		fprintf(stderr, "setting login hostname: %s\n", hostname);
	}  
```

设置 TDS 端口环境变量。使用默认端口 1433 时不必设置：

```c
	/* the port can only be set via environment variable */

	if (putenv("TDSPORT=1433") != 0)
	{
        	fprintf(stderr, "error setting TDSPORT environment variable\n");
        	return 0;
	}
```

安装错误处理器和消息处理器。当出现错误或消息时，TDS 库会调用相应函数。本例将消息发送到 `stderr`：

```c
	/* install error handler */
	dberrhandle(err_handler);
	dbmsghandle(msg_handler);
```

调用 `dbopen` 连接服务器：

```c
	/* Now connect to the DB Server */
	if ((dbconn = dbopen(login, DBSERVER)) == NULL) 
	{
		fprintf(stderr, "Could not connect to DB Server: %s\n", DBSERVER);
    		return 3;
	}

	printf("success\n");
	return 0;
}
```

使用 GCC 编译：

```bash
gcc main_01.c -lsybdb -I/usr/include/ -o main_01
```

编译时有两个关键点：

- 使用 `-I` 选项，告知编译器头文件所在位置。
- 链接 FreeTDS 库。原文正文写作 `-lsydbd`，应与上方命令中实际的库名核对。

本例生成名为 `main_01` 的二进制程序。

虽然示例很简单，但展示了用 C 开发访问 Babelfish 服务器的程序时所需的基本行为。

### FreeTDS 配置问题 {#freetds-configuration-issues}

下面的消息由 FreeTDS 配置错误引起：

```bash
[hs@fedora tds_test]$ ./main_01 
setting login hostname: fedora
Server error 20018: General SQL Server error: Check messages from the SQL Server
Caused by system error -1: (null)
Server error 20002: Adaptive Server connection failed (sample-host.example.com)
Server error 20002: Adaptive Server connection failed (sample-host.example.com)
Could not connect to DB Server: sample-host.example.com)
```

如果出现此错误，通常是 FreeTDS 配置文件存在错误，或文件根本不存在。配置方法见 [FreeTDS 文档](https://www.freetds.org/userguide/freetdsconf.html)。
