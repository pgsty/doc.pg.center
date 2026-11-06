---
title: "Installing Java for PXF"
description: "Installing Java for the PXF service."
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/install_java.md"
---

PXF is a Java service. It requires a Java 8 or Java 11 installation on each Apache Cloudberry host.


## Prerequisites {#prerequisites}

Ensure that you have access to, or superuser permissions to install, Java 8 or Java 11 on each Apache Cloudberry host.

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

3. If the system does not include a Java version 8 or 11 installation, install one of these Java versions on the coordinator host, standby coordinator host, and on each Apache Cloudberry segment host.

    1. Create a text file that lists your Apache Cloudberry standby coordinator host and segment hosts, one host name per line. For example, a file named `gphostfile` may include:

        ```text
        coordinator
        mstandby
        seghost1
        seghost2
        seghost3
        ```
    2. Install the Java package on each host. For example, to install Java version 8:

        ```shell
        gpadmin@coordinator$ gpssh -e -v -f gphostfile sudo yum -y install java-1.8.0-openjdk-1.8.0*
        ```

4. Identify the Java 8 or 11 `$JAVA_HOME` setting for PXF. For example:

    If you installed Java 8:

    ```shell
    JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.x86_64/jre
    ```

    If you installed Java 11:
    
    ```shell
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.4.11-0.el7_6.x86_64
    ```

    If the superuser configures the newly-installed Java alternative as the system default:

    ```shell
    JAVA_HOME=/usr/lib/jvm/jre
    ```

5. Note the `$JAVA_HOME` setting; you will need this value when you configure PXF.
