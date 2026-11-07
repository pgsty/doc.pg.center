---
title: IvorySQL Cloud installation
linkTitle: IvorySQL Cloud Installation
description: 'IvorySQL v5.6 documentation: IvorySQL Cloud installation.'
type: docs
weight: 110
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/4.7.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

The IvorySQL Cloud platform is a comprehensive solution that integrates the IvorySQL database and its surrounding ecosystem to deliver end-to-end database and resource management capabilities. Before starting the installation, compile and install the following projects from GitHub:

Frontend: <a href="https://github.com/IvorySQL/ivory-cloud-web" class="bare">https://github.com/IvorySQL/ivory-cloud-web</a>

Backend: <a href="https://github.com/IvorySQL/ivory-cloud" class="bare">https://github.com/IvorySQL/ivory-cloud</a>

Prepare a Kubernetes cluster (version 1.23) and install `ivory-operator` on the master node:

<a href="https://github.com/IvorySQL/ivory-operator/tree/IVYO_REL_5_STABLE" class="bare">https://github.com/IvorySQL/ivory-operator/tree/IVYO_REL_5_STABLE</a>

## 1. IvorySQL Cloud Platform Installation {#ivorysql-cloud-platform-installation}

The IvorySQL Cloud platform currently supports installation on Linux systems. The required packages are listed below.

<table class="tableblock frame-all grid-all" style="width: 99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th class="tableblock halign-left valign-top">Component</th>
<th class="tableblock halign-left valign-top">Package</th>
</tr>
</thead>
<tbody>
<tr>
<td class="tableblock halign-left valign-top"><p>Frontend</p></td>
<td class="tableblock halign-left valign-top"><p>dist</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>Backend</p></td>
<td class="tableblock halign-left valign-top"><p>cloudnative-1.0-SNAPSHOT.jar</p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p>K8S cluster</p></td>
<td class="tableblock halign-left valign-top"><ol>
<li><p>docker.io/ivorysql/ivory-operator:v5.6</p></li>
<li><p>docker.io/ivorysql/pgadmin:ubi8-9.9-5.0-1</p></li>
<li><p>docker.io/ivorysql/pgbackrest:ubi8-2.56.0-5.0-1</p></li>
<li><p>docker.io/ivorysql/postgres-exporter:ubi8-0.17.0-5.0-1</p></li>
<li><p>docker.io/ivorysql/ivorysql:ubi8-5.0-5.0-1</p></li>
</ol></td>
</tr>
</tbody>
</table>

In addition, install the following supporting components:

- **Backend database**: Stores and manages all data related to cloud resources, user information, access control, billing, and more. Use a PostgreSQL-compatible database such as PostgreSQL, HighGo DB, or IvorySQL.

- **NGINX**: Hosts the web user interface of the cloud platform.

## 2. Pre-installation Checklist {#pre-installation-checklist}

Complete the preparation steps on every server before installation. Deploy IvorySQL Cloud on a Kubernetes (1.23) cluster that already has a default storage class.

### 2.1. Disable the firewall {#disable-the-firewall}

Disable the firewall on every server to ensure full connectivity.

```
systemctl stop firewalld.service

systemctl disable firewalld.service
```

### 2.2. Backend deployment {#backend-deployment}

#### 2.2.1. Backend database {#backend-db}

Install the backend database yourself by following the instructions on the IvorySQL official website.

#### 2.2.2. Backend services {#backend-services}

##### 2.2.2.1. Compile the backend service {#compile-the-backend-service}

```
# Clone the code

git clone https://github.com/IvorySQL/ivory-cloud.git

# Go to the project root

cd ivory-cloud
```

Ensure that every `.sh` file in `ivory-cloud\cloudnative\src\main\resources\monitor` and its subdirectories uses the Unix format. If not, run `dos2unix` to convert them.

```
dos2unix cloudnative\src\main\resources\monitor\*

# Build

mvn clean

mvn package -D maven.test.skip=true

The packaged artifact `cloudnative-1.0-SNAPSHOT.jar` can be found under `ivory-cloud/cloudnative/target`.
```

##### 2.2.2.2. Deploy the service {#deploy-the-service}

```
Execute the following steps on the Kubernetes server:

# Create a working directory

mkdir -p /home/ivory

# Upload `ivory-cloud/cloudnative/target/cloudnative-1.0-SNAPSHOT.jar` to the directory created above

# Configuration files

## Create a configuration directory

mkdir -p /home/ivory/config

## Upload configuration files

Copy the following files from `ivory-cloud/cloudnative/src/main/resources` to `/home/ivory/config`:

application.yaml

application-native.yaml

spring_pro_logback.xml

## Update the configuration

Replace `url`, `username`, and `password` with the database information configured in <<Backend database>>.

## /home/ivory/config/application-native.yaml

datasource:

druid:

db-type: com.alibaba.druid.pool.DruidDataSource

driver-class-name: org.postgresql.Driver

url: jdbc:postgresql://127.0.0.1:5432/ivorysql

username: ivorysql

password: "ivory@123"
```

#### 2.2.3. Start the backend service {#start-the-backend-service}

```
# Install JDK 1.8

yum install -y java-1.8.0-openjdk.x86_64

[root@cloud ivory]# pwd

/home/ivory/

[root@cloud ivory]# nohup java -jar cloudnative-1.0-SNAPSHOT.jar > log_native 2>&1 &

[root@cloud ivory]# ps -ef | grep java

root 77494 1 0 Oct09 ? 00:03:07 java -jar cloudnative-1.0-SNAPSHOT.jar
```

### 2.3. Frontend deployment {#frontend-deployment}

#### 2.3.1. Compile the frontend {#compile-the-frontend}

```
## Fetch the code

git clone https://github.com/IvorySQL/ivory-cloud-web.git

## Go to the project root

cd ivorysql-cloud-web

## Install dependencies

npm install

## Build for production

npm run build:prod
```

#### 2.3.2. Update directory and file permissions {#update-directory-and-file-permissions}

```
# Create a deployment directory

[root@cloud opt]# mkdir -p /opt/cloud/web

# Copy the generated `dist` folder to /opt/cloud/web

# Grant permissions

[root@cloud web]# chmod 755 /opt/cloud/web/dist

[root@cloud web]# chmod -R 777 /opt/cloud/web/dist
```

#### 2.3.3. Update config.js {#update-config-js}

Edit the configuration file:

```
[root@cloud dist]# pwd

/home/cloud/web/dist

[root@cloud dist]# vi config.js

var PLATFROM_CONFIG = {};

// Replace with the IP address of the current server

PLATFROM_CONFIG.baseUrl = "http://192.168.31.43:8081/cloudapi/api/v1"

// true: show the “Register” button on the login page

// false: hide the “Register” button on the login page

globalShowRegister = true

// Hide the cloud-native database? true: hide; false: show

disableNative = false

// Database type

dbtype = "IvorySQL"

dbversion = "5.6"
```

### 2.4. Install and configure NGINX {#install-and-configure-nginx}

The IvorySQL Cloud host must have NGINX installed to serve the web interface. Users can select any installation method; the following steps are provided for reference.

#### 2.4.1. Download the NGINX source package {#download-the-nginx-source-package}

```
[root@cloud web]# wget https://nginx.org/download/nginx-1.20.1.tar.gz

[root@cloud web]# ls -lrt

total 3924

-rwxrwxr-x. 1 root root 1061461 May 25 2021 nginx-1.20.1.tar.gz

-rwxrwxr-x. 1 root root 2943732 Oct  9 16:43 dist.tar.gz

drwxrwxrwx. 4 root root     103 Oct 21 13:20 dist
```

#### 2.4.2. Install dependencies {#install-dependencies}

```
[root@host30 cloud]# yum -y install pcre-devel

[root@host30 cloud]# yum -y install openssl openssl-devel
```

#### 2.4.3. Build and install NGINX {#build-and-install-nginx}

NGINX is installed under the directory specified by `--prefix` during `configure`. The example below installs it to `/opt/cloud/nginx`.

```
## Extract nginx-1.20.1.tar.gz

[root@cloud web]# tar -zxvf nginx-1.20.1.tar.gz

## Verify that nginx-1.20.1 was created

[root@cloud web]# ls -lrt

total 3924

-rwxrwxr-x. 1 root root 1061461 May 25 2021 nginx-1.20.1.tar.gz

-rwxrwxr-x. 1 root root 2943732 Oct  9 16:43 dist.tar.gz

drwxrwxr-x. 9 1001 1001     186 Oct  9 16:53 nginx-1.20.1

drwxrwxrwx. 4 root root     103 Oct 21 13:20 dist

## Configure

[root@cloud web]# cd nginx-1.20.1

[root@cloud nginx-1.20.1]# ./configure --prefix=/opt/cloud/nginx --with-http_ssl_module

## Compile and install

[root@cloud nginx-1.20.1]# make

[root@cloud nginx-1.20.1]# make install
```

#### 2.4.4. Update nginx.conf {#update-nginx-conf}

The configuration file is stored under `/opt/cloud/nginx`. Adjust it according to the README on GitHub, and replace the IP with the address of the current server.

```
server {

listen 9104;

server_name 192.168.31.43;

location / {

root /opt/cloud/web/dist;

index index.html index.htm;

}

error_page 500 502 503 504 /50x.html;

location = /50x.html {

root html;

}

}
```

#### 2.4.5. Start NGINX {#start-nginx}

```
[root@cloud sbin]# pwd

/opt/cloud/nginx/sbin

[root@cloud sbin]# ./nginx -c /opt/cloud/nginx/conf/nginx.conf

[root@cloud sbin]# ps -ef | grep nginx

root  2179 131037 0 09:46 pts/1 00:00:00 grep --color=auto nginx

root 55047      1 0 Oct21 ?     00:00:00 nginx: master process ./nginx -c /opt/cloud/nginx/conf/nginx.conf

nobody 55048 55047 0 Oct21 ?    00:00:00 nginx: worker process
```

### 2.5. Operator deployment {#operator-deployment}

Set up the Kubernetes cluster yourself. This section describes how to install `ivory-operator` on the cluster and preload container images.

#### 2.5.1. Install ivory-operator {#install-ivory-operator}

Refer to the README on GitHub:

<https://github.com/IvorySQL/ivory-operator/tree/IVYO_REL_5_STABLE>

#### 2.5.2. Load container images {#load-container-images}

If your servers have direct access to Docker Hub, you can skip this step. Otherwise, preload the following images on every node in the Kubernetes cluster.

> [!TIP]
>
> Users in China can pull the following images from the IvorySQL community Harbor registry by replacing the `docker.io/` prefix with `registry.highgo.com/`.

```
docker.io/ivorysql/pgadmin:ubi8-9.9-5.0-1

docker.io/ivorysql/pgbackrest:ubi8-2.56.0-5.0-1

docker.io/ivorysql/pgbouncer:ubi8-1.23.0-5.0-1

docker.io/ivorysql/postgres-exporter:ubi8-0.17.0-5.0-1

docker.io/ivorysql/ivorysql:ubi8-5.0-5.0-1

docker.io/prom/prometheus:v2.33.5

docker.io/prom/alertmanager:v0.22.2

docker.io/grafana/grafana:8.5.10
```
