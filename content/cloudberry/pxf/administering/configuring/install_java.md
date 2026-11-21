---
title: "Installing Java for PXF"
description: "Installing Java for the PXF service."
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/6683faa38ce4e2d146a77197991518aacb4b24e8/docs/administering/configuring/install_java.md"
---

PXF is a Java service. It requires a Java 17 or 21 installation on each Apache Cloudberry host.


## Prerequisites {#prerequisites}

Ensure that you have access to, or superuser permissions to install, Java on each Apache Cloudberry host.

## Procedure {#procedure}

Perform the following procedure to install Java on the coordinator host, standby coordinator host, and on each segment host in your Apache Cloudberry cluster. You will use the `gpssh` utility where possible to run a command on multiple hosts.

1. Log in to your Apache Cloudberry coordinator host:

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. Determine the version(s) of Java installed on the system:

    ```text
    gpadmin@coordinator$ rpm -qa | grep java
    ```

3. If the system does not include a Java installation, install it on the coordinator host, standby coordinator host, and on each Apache Cloudberry segment host.

    1. Create a text file that lists your Apache Cloudberry standby coordinator host and segment hosts, one host name per line. For example, a file named `gphostfile` may include:

        ```text
        coordinator
        mstandby
        seghost1
        seghost2
        seghost3
        ```
    2. Install the Java package on each host. For example:

        ```shell
        gpadmin@coordinator$ gpssh -e -v -f gphostfile sudo yum -y install java-17-openjdk
        ```

4. Identify the Java `$JAVA_HOME` setting for PXF. For example:

    ```shell
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk
    ```

    If the superuser configures the newly-installed Java alternative as the system default:

    ```shell
    JAVA_HOME=/usr/lib/jvm/jre
    ```

5. Note the `$JAVA_HOME` setting; you will need this value when you configure PXF.
