---
title: "地理空间分析"
description: "为 Apache Cloudberry 构建 PostGIS 及其依赖，以支持地理空间数据存储、查询和索引。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/advanced-analytics/postgis.md"
---

[PostGIS](https://postgis.net/) 通过增加对地理空间数据存储、索引和查询的支持，扩展了 PostgreSQL 的能力。Apache Cloudberry 支持使用 PostGIS 进行地理空间分析。

本文介绍如何为 Apache Cloudberry 集群编译和构建 PostGIS。

可以在 [`cloudberry-contrib/postgis`](https://github.com/cloudberry-contrib/postgis) 项目仓库中访问 Apache Cloudberry 的 PostGIS 项目。该仓库中的 PostGIS 代码专用于 Apache Cloudberry。本文介绍的编译和构建方法基于该仓库中的代码。

> [!NOTE]
> 该仓库由社区成员贡献并针对 Cloudberry 定制；但请注意，它不是作为官方 Cloudberry 项目维护的。

## 为 Apache Cloudberry 编译 PostGIS {#compile-postgis-for-apache-cloudberry}

本文介绍如何为 Apache Cloudberry 编译和构建 PostGIS 3.3.2。

安装 Apache Cloudberry 的 PostGIS 之前，需要安装所需依赖并编译几个组件。此过程已在 Rocky Linux 8 和 Rocky Linux 9 上测试并获得支持。

开始之前，请确保 Apache Cloudberry 已正确安装在机器上。如果尚未安装，请参见[文档](/cloudberry/introduction/cbdb-overview/)了解安装说明。

以下步骤将在 `gpadmin` 用户下执行。请确保使用 `gpadmin` 用户执行这些命令。如果不是，可以运行 `su - gpadmin` 命令切换到 `gpadmin` 用户。

### 1. 通过包管理器安装所需依赖。 {#1-install-the-pre-requested-dependencies-via-the-package-manager}

```bash {tab="适用于 Rocky Linux 8"}
sudo dnf install -y libxml2-devel json-c pkg-config gettext \
    protobuf-c gmp-devel boost-devel automake libtool make \
    gcc gcc-c++ sqlite-devel mpfr-devel bzip2 xz libcurl-devel \
    cmake protobuf-c-devel libxslt docbook-style-xsl

sudo dnf install -y --enablerepo=devel protobuf-devel json-c-devel
sudo dnf install -y --enablerepo=devel CUnit-devel # Optional, for PostGIS testing
```
```bash {tab="Rocky Linux 9"}
sudo dnf install -y libxml2-devel json-c pkg-config gettext \
    protobuf-c gmp-devel boost-devel automake libtool make \
    gcc gcc-c++ sqlite-devel mpfr-devel bzip2 xz libcurl-devel \
    cmake libxslt docbook-style-xsl

sudo dnf install -y --enablerepo=crb protobuf-c-devel json-c-devel
sudo dnf install -y --enablerepo=crb CUnit-devel # Optional, for PostGIS testing
```

### 2. 构建组件（GDAL、CGAL、SFCGAL 和 GEOS）。 {#2-build-the-components-gdal-cgal-sfcgal-and-geos}

主要依赖如下，需要从源代码构建：

* proj：5.2.0+
* GEOS：3.11+
* gdal：3+
* cgal：5.3+
* sfcgal：1.4.1+

1. 构建 GDAL。

    [GDAL](https://gdal.org/index.html) 是一个用于栅格和矢量地理空间数据格式转换的转换库。

    首先需要安装 [proj](https://proj.org/)。这是一个用于地理空间坐标转换的库，也是 GDAL 的依赖项。请执行以下命令安装 proj 6.0.0：

      ```bash
      wget https://download.osgeo.org/proj/proj-6.0.0.tar.gz
      tar -xzf proj-6.0.0.tar.gz
      cd proj-6.0.0
      ./configure --prefix=/usr/local/proj6
      make -j$(nproc) && sudo make -j$(nproc) install
      ```

    然后构建 GDAL 3.5.3：

      ```bash
      wget https://download.osgeo.org/gdal/3.5.3/gdal-3.5.3.tar.gz
      tar xf gdal-3.5.3.tar.gz
      cd gdal-3.5.3
      ./configure --prefix=/usr/local/gdal-3.5.3 \
        --with-proj=/usr/local/proj6
      make -j$(nproc) && sudo make -j$(nproc) install
      ```

2. 构建 CGAL。

    [CGAL](https://www.cgal.org/) 以 C++ 库的形式提供对高效、可靠几何算法的便捷访问。请执行以下命令安装它：

    ```bash
    wget https://github.com/CGAL/cgal/releases/download/v5.6.1/CGAL-5.6.1.tar.xz
    tar -xf CGAL-5.6.1.tar.xz
    cd CGAL-5.6.1
    mkdir build && cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local/cgal-5.6.1 ..
    make -j$(nproc) && sudo make -j$(nproc) install
    ```

3. 构建 SFCGAL。

    [SFCGAL](https://github.com/Oslandia/SFCGAL) 是围绕 CGAL 的 C++ 封装库，用于支持 ISO 19107:2013 和 OGC Simple Features Access 1.2 的三维操作。请执行以下命令安装它：

    ```bash
    wget https://gitlab.com/sfcgal/SFCGAL/-/archive/v1.4.1/SFCGAL-v1.4.1.tar.gz
    tar xf SFCGAL-v1.4.1.tar.gz
    cd SFCGAL-v1.4.1
    mkdir build && cd build
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local/sfcgal-1.4.1 ..
    make -j$(nproc) && sudo make -j$(nproc) install
    ```

4. 构建 GEOS。

    [GEOS](https://libgeos.org/) 是一个用于计算几何的 C/C++ 库，重点面向地理信息系统（GIS）软件中使用的算法。请执行以下命令安装它：

    ```bash
    wget https://download.osgeo.org/geos/geos-3.11.0.tar.bz2
    tar xf geos-3.11.0.tar.bz2
    cd geos-3.11.0
    mkdir build && cd build
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local/geos-3.11.0 ..
    make -j$(nproc) && sudo make -j$(nproc) install
    ```

5. 更新 `/etc/ld.so.conf`。

    安装上述组件后，更新 `/etc/ld.so.conf`，配置动态加载器搜索这些组件的目录：

    ```bash
    sudo vi /etc/ld.so.conf
    ```

    将以下行添加到文件末尾：

    ```bash 
    /usr/lib/
    /usr/lib64/
    /usr/local/sfcgal-1.4.1/lib64/
    /usr/local/gdal-3.5.3/lib/
    /usr/local/geos-3.11.0/lib64/
    /usr/local/proj6/lib/
    ```

    然后运行以下命令更新动态加载器缓存：

    ```bash
    sudo ldconfig
    ```

### 3. 构建并安装 PostGIS。 {#3-build-and-install-postgis}

1. 将 `cloudberry-contrib/postgis` 仓库下载到 `/home/gpadmin` 目录：

     ```bash
     git clone https://github.com/cloudberry-contrib/postgis.git /home/gpadmin/postgis
     ```

2. 编译 PostGIS。

     开始编译之前，请运行以下命令，确保环境变量已准备就绪（在 gpdemo 环境中）：

     ```bash
     source /usr/local/cloudberry-db/cloudberry-env.sh
     source /home/gpadmin/cloudberry/gpAux/gpdemo/gpdemo-env.sh
     ```

     然后继续：

     ```bash
     cd /home/gpadmin/postgis/postgis/build/postgis-3.3.2/
     ./autogen.sh
     ./configure --with-pgconfig="${GPHOME}"/bin/pg_config \
       --with-raster --without-topology \
       --with-gdalconfig=/usr/local/gdal-3.5.3/bin/gdal-config \
       --with-sfcgal=/usr/local/sfcgal-1.4.1/bin/sfcgal-config \
       --with-geosconfig=/usr/local/geos-3.11.0/bin/geos-config \
       --with-projdir=/usr/local/proj6/
     make -j$(nproc)
     make check # Optional, to run PostGIS tests
     sudo make -j$(nproc) install
     ```

## 在 Apache Cloudberry 中使用 PostGIS {#use-postgis-in-apache-cloudberry}

在 Apache Cloudberry 集群上成功编译并构建 PostGIS 及其支持扩展，并启动演示集群后，可以运行以下命令启用 PostGIS 和支持扩展：

```sql
$ psql -p 7000 postgres

postgres=# CREATE EXTENSION postgis;     -- Enables PostGIS and raster
postgres=# CREATE EXTENSION fuzzystrmatch;     -- Required for installing Tiger Geocoder
postgres=# CREATE EXTENSION plpython3u; -- Required for installing Tiger Geocoder
postgres=# CREATE EXTENSION postgis_tiger_geocoder;     -- Enables Tiger Geocoder
postgres=# CREATE EXTENSION address_standardizer;     -- Enables address_standardizer
postgres=# CREATE EXTENSION address_standardizer_data_us;
```

下面的示例使用 PostGIS 在数据库中创建非 OpenGIS 表，并插入和查询几何对象。

```sql
-- Creates a table named geom_test.
CREATE TABLE geom_test ( gid int4, geom geometry, 
  name varchar(25) );

-- Inserts a row into the table. The gid is 1, the geometry field represents a three-dimensional polygon object (a 3D square) using WKT format, and the name is '3D Square'.
INSERT INTO geom_test ( gid, geom, name )
  VALUES ( 1, 'POLYGON((0 0 0,0 5 0,5 5 0,5 0 0,0 0 0))', '3D Square');
  
-- Inserts the second row. The gid is 2, the geometry is a three-dimensional line string, and the name is '3D Line'.
INSERT INTO geom_test ( gid, geom, name ) 
  VALUES ( 2, 'LINESTRING(1 1 1,5 5 5,7 7 5)', '3D Line' );
  
-- Inserts the third row. The gid is 3, the geometry is a two-dimensional multi-point object, and the name is '2D Aggregate Point'.
INSERT INTO geom_test ( gid, geom, name )
  VALUES ( 3, 'MULTIPOINT(3 4,8 9)', '2D Aggregate Point' );

-- Uses ST_GeomFromEWKT to build a three-dimensional lines tring object from EWKT, then use Box3D to get the three-dimensional bounding box of that object. Use the && operator to query all rows in the geom_test table whose geom field intersects with the bounding box.
SELECT * from geom_test WHERE geom &&
  Box3D(ST_GeomFromEWKT('LINESTRING(2 2 0, 3 3 0)'));
```

下面的示例使用 PostGIS 创建一个包含地理参考数据的表，插入经过地理编码的点数据，并以标准文本格式输出点数据。

```sql
-- Creates a table named geotest.
CREATE TABLE geotest (id INT4, name VARCHAR(32) );

-- Adds a geometry column named geopoint to the geotest table, defined as a POINT type with 2 dimensions, and specifies its Spatial Reference System (SRID) as 4326 (representing the WGS84 geographic coordinate system).
SELECT AddGeometryColumn('geotest','geopoint', 4326,'POINT',2);

-- Inserts the first row. The id is 1, the name is 'Olympia', and geopoint is a point object build from WKT text using ST_GeometryFromText with coordinates (-122.90, 46.97) and SRID 4326.
INSERT INTO geotest (id, name, geopoint)
  VALUES (1, 'Olympia', ST_GeometryFromText('POINT(-122.90 46.97)', 4326));
  
-- Inserts the second row. The id is 2, the name is 'Renton', with point coordinates (-122.22, 47.50) and the same SRID of 4326.
INSERT INTO geotest (id, name, geopoint)
  VALUES (2, 'Renton', ST_GeometryFromText('POINT(-122.22 47.50)', 4326));

-- Selects the name and geopoint fields from the geotest table, but converts the geopoint field to standard text (WKT) format using the ST_AsText function.
SELECT name,ST_AsText(geopoint) FROM geotest;
```

下面的示例使用空间索引功能。

```sql
-- Creates table.
CREATE TABLE spatial_data (
  id SERIAL PRIMARY KEY,
  geom geometry
);

-- Inserts data.
INSERT INTO spatial_data (geom) VALUES 
(ST_GeomFromText('POINT(0 0)')),
(ST_GeomFromText('POINT(1 1)')),
(ST_GeomFromText('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'));

-- Creates spatial index.
CREATE INDEX spatial_data_gist_idx
  ON spatial_data
  USING GIST (geom);
```

如需了解更多用法，请参见 [PostGIS 手册](https://postgis.net/documentation/manual/)。
