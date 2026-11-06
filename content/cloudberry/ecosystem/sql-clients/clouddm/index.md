---
title: "CloudDM"
description: "CloudDM is an open-source database management tool for teams."
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/ecosystem/sql-clients/clouddm.md"
---

It provides a web console for SQL queries, database management, access control, SQL auditing, approval workflows, and database CI/CD. It supports multiple databases, including MySQL, Oracle, StarRocks, and Apache Cloudberry.

This document shows how to connect CloudDM to Apache Cloudberry and run SQL queries.

## Prerequisites {#prerequisites}

- Apache Cloudberry is deployed and running.
- Database access permissions are properly configured in `pg_hba.conf`.
- [CloudDM (v4.1.0 or higher)](https://github.com/ClouGence/open-cdm) is installed and accessible.

## Steps {#steps}

1. Log in to the CloudDM console, and click **Back to Workspace**.

2. In the left panel, click **Instances**, and then click **New** to add a database connection.
![](clouddm1.png)

3. Select Cloudberry and click **Submit**.
![](clouddm2.png)

4. Enter the Cloudberry connection information:
    - **Host**: Enter the hostname or IP address of your Cloudberry instance.
    - **Port**: Enter the port.
    - **Authentication**: Select an authentication method and enter the required information (for example, username and password)

    ![](clouddm3.png)

5. Test the connection. Once Cloudberry is connected to CloudDM, click **Add DataSource**.

    If the test fails, check the Cloudberry address, port, database user, password, network access, and `pg_hba.conf` rules.

6. Go to **SQL Query**.
![](clouddm4.png)

7. The added Cloudberry instance is shown in the left panel. Now you can start running a query.
![](clouddm5.png)

## Other features {#other-features}

### Work orders {#work-orders}

CloudDM supports work orders for production database changes. Teams can submit, approve, and execute changes through a controlled workflow.
![](clouddm6.png)

### CI/CD {#cicd}

CloudDM can trigger database CI/CD workflows through Git Push, Web Hook, and HttpCall. Teams can include SQL checks, approvals, and execution in application release processes, and manage database change scripts in one place.
![](clouddm7.png)

### User access control {#user-access-control}

CloudDM supports role-based access control (RBAC) for team collaboration. Teams can grant access by role and control which data sources and operations each user can use.
![](clouddm8.png)
