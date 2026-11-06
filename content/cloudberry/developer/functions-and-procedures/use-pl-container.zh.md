---
title: "使用 PL/Container"
description: "PL/Container 允许在 Docker 容器内运行过程语言函数，从而降低直接在 Apache Cloudberry Segment 主机上运行 Python 或 R 代码所带来的安全风险。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-container.md"
---

本文介绍 PL/Container 的架构、配置、使用方法和高级主题。

## PL/Container 语言扩展简介 {#about-the-plcontainer-language-extension}

PL/Container 语言扩展允许在 Docker 容器内安全地创建和运行 PL/Python 或 PL/R 用户定义函数（UDF）。Docker 能够将应用程序打包并运行在一种称为容器的松散隔离环境中。

在 Docker 容器内运行 UDF 可以确保：

- 函数执行发生在隔离环境中，数据处理彼此解耦。
- 用户代码无法访问主机的操作系统或文件系统。
- 用户代码不会引入安全风险。
- 如果容器启动时受到有限或完全没有网络访问权限，函数就无法回连数据库。

### PL/Container 架构 {#plcontainer-architecture}

进程流程示例：

1. 查询调用 PL/Container 函数时，Segment 主机上的查询执行器（QE）启动一个容器，并与容器通信以获取结果。容器可以通过服务器编程接口（SPI）回调数据库执行 SQL 查询，然后将最终结果返回给 QE。

2. 处于待机模式的容器会等待套接字连接，不消耗任何 CPU 资源。启动该容器的 Apache Cloudberry 数据库会话关闭时，容器连接也会关闭，容器随之停止。

## 配置和使用 PL/Container {#configure-and-use-plcontainer}

在 Apache Cloudberry 中使用 PL/Container 无需安装扩展软件包。只需配置 Docker 环境并在数据库中启用扩展。

### 前提条件 {#prerequisites}

- Apache Cloudberry 的所有数据库主机（Coordinator 和所有 Segment）上都已安装 Docker。
- Linux 内核最低版本为 3.10。
- Docker 最低版本为 19.03。

### 步骤 1：安装 Docker {#step-1-install-docker}

需要在 Apache Cloudberry 的所有数据库主机上安装 Docker。以下是在 CentOS 7 上的安装示例：

1. 确保当前用户具有 `sudo` 权限，或当前用户是 `root`。

2. 安装 Docker 所需的依赖项：

    ```bash
    sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    ```

3. 添加 Docker 软件仓库：

    ```bash
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    ```

4. 安装 Docker：

    ```bash
    sudo yum -y install docker-ce
    ```

5. 启动 Docker 服务：

    ```bash
    sudo systemctl start docker
    ```

6. 将 Apache Cloudberry 数据库管理员用户（通常为 `gpadmin`）加入 `docker` 组，使其可以管理 Docker 镜像和容器：

    ```bash
    sudo usermod -aG docker gpadmin
    ```

7. 注销当前会话并重新登录，使权限生效。

8. 配置 Docker 在系统启动时自动启动：

    ```bash
    sudo systemctl enable docker.service
    ```

9. 测试 Docker 是否安装成功。此命令列出当前正在运行的容器（此时应为空）：

    ```bash
    docker ps
    ```

10. 在所有主机上安装 Docker 后，重启 Apache Cloudberry 数据库，使更改生效：

    ```bash
    gpstop -ra
    ```

### 步骤 2：启用 PL/Container {#step-2-enable-plcontainer}

PL/Container 是 Apache Cloudberry 的内置扩展。只需在要使用它的数据库中执行一条命令即可启用。

1. 使用 `psql` 连接目标数据库：

    ```bash
    psql -d your_database_name
    ```

2. 执行 `CREATE EXTENSION` 命令：

    ```sql
    CREATE EXTENSION plcontainer;
    ```

    执行成功后，PL/Container 会在该数据库中启用。

### 步骤 3：安装和配置 Docker 镜像 {#step-3-install-and-configure-docker-images}

PL/Container 需要特定的 Docker 镜像来创建运行 UDF 的容器。

1. 从可信来源获取 PL/Container Docker 镜像文件（例如 `plcontainer-python3-image-*.tar.gz`）。

2. 使用 `plcontainer image-add` 命令在所有 Apache Cloudberry 主机上安装镜像。使用 `-f` 选项指定镜像文件路径。

    > [!NOTE]
    > 确保系统中存在 `rsync` 依赖项，否则以下命令会失败。

    ```bash
    # Installs a Python 3 based Docker image.
    plcontainer image-add -f /path/to/your/plcontainer-python3-image.tar.gz
    
    # Installs an R based Docker image.
    plcontainer image-add -f /path/to/your/plcontainer-r-image.tar.gz
    ```

3. 使用 `plcontainer image-list` 命令查看已安装的镜像：

    ```bash
    plcontainer image-list
    ```

4. 使用 `plcontainer runtime-add` 命令将已安装的镜像注册为“运行时”，以便在函数中调用。

    - `-r`：指定运行时的名称（自定义）。
    - `-i`：指定关联的 Docker 镜像。
    - `-l`：指定该运行时支持的语言（`python`、`python3` 或 `r`）。

    ```bash
    # Adds a Python 3 runtime.
    plcontainer runtime-add -r plc_python3_shared -i pivotaldata/plcontainer_python3_shared:devel -l python3
    
    # Adds an R runtime.
    plcontainer runtime-add -r plc_r_shared -i pivotaldata/plcontainer_r_shared:devel -l r
    ```

### 步骤 4：测试安装 {#step-4-test-the-installation}

1. 使用 `psql` 连接已启用 PL/Container 的数据库。

2. 创建一个简单函数来测试 Python 运行时。请注意其中的 `# container:` 注释，它指定了函数使用的运行时 ID。

    ```sql
    CREATE FUNCTION dummy_python() RETURNS text AS $$
    # container: plc_python3_shared
    return 'Hello from Python in a container'
    $$ LANGUAGE plcontainer;
    ```

3. 调用函数进行测试：

    ```sql
    SELECT dummy_python();
    ```

4. 同样，可以创建函数来测试 R 运行时：

    ```sql
    CREATE FUNCTION dummy_r() RETURNS text AS $$
    # container: plc_r_shared
    return ('Hello from R in a container')
    $$ LANGUAGE plcontainer;
    ```

5. 调用函数执行测试：

    ```sql
    SELECT dummy_r();
    ```

## 编写 PL/Container 函数 {#write-plcontainer-functions}

在数据库中启用 PL/Container 扩展时，会注册 `plcontainer` 语言。通过在用户定义函数（UDF）中指定 `LANGUAGE plcontainer`，即可使用 Python 或 R 等 PL/Container 支持的语言编写函数。

PL/Container 配置文件只会在每个数据库会话首次调用 PL/Container 函数时读取。如果在外部修改配置，可以在会话中运行 `SELECT * FROM plcontainer_refresh_config;` 强制重新加载。

### 函数定义 {#function-definition}

要创建 PL/Container 函数，定义的 UDF 必须包含以下元素：

- **容器声明**：函数体第一行必须是 `# container: ID`，其中 `ID` 是通过 `plcontainer runtime-add` 定义的运行时 ID。
- **语言声明**：函数的 `LANGUAGE` 属性必须是 `plcontainer`。

如果 UDF 中的 `# container` 行指定了 PL/Container 配置文件中不存在的 ID，数据库会在尝试运行 UDF 时返回错误。

### 函数示例 {#function-examples}

以下是一些基本的函数示例。请确保示例中的 `# container` ID 与所配置的运行时 ID 匹配。

**PL/Python 示例：**

```sql
CREATE OR REPLACE FUNCTION pylog100() RETURNS double precision AS $$
 # container: plc_python3_shared
 import math
 return math.log10(100)
$$ LANGUAGE plcontainer;

SELECT pylog100();
```

**PL/R 示例：**

```sql
CREATE OR REPLACE FUNCTION rlog100() RETURNS text AS $$
# container: plc_r_shared
return(log10(100))
$$ LANGUAGE plcontainer;

SELECT rlog100();
```

### PL/Python 函数简介 {#about-plpython-functions}

#### PL/Python 2 与 PL/Python 3 {#plpython-2-vs-plpython-3}

- PL/Container 支持 Python 2.7 和 Python 3.6+。
- 如果希望使用 PL/Container 同时运行 Python 2 和 Python 3 的函数，需要分别为它们创建两个不同的用户定义函数。
- 请注意，为 Python 2 编写的 UDF 可能无法直接在 Python 3 中运行。

#### 数据库交互（`plpy` 模块） {#database-interaction-plpy-module}

`plpy` 模块提供了一组与数据库交互的方法：

- `plpy.execute(stmt)`：执行 SQL 查询字符串，并将结果作为字典列表返回。
- `plpy.prepare(stmt[, argtypes])`：准备查询计划。
- `plpy.execute(plan[, argtypes])`：执行准备好的查询计划。
- `plpy.debug(msg)`、`plpy.log(msg)`、`plpy.info(msg)`、`plpy.notice(msg)`、`plpy.warning(msg)`、`plpy.error(msg)`、`plpy.fatal(msg)`：向数据库日志系统发送不同级别的日志消息。`ERROR` 或 `FATAL` 级别的错误会中止事务。
- `plpy.subtransaction()`：管理显式子事务。

#### 字符串引用 {#string-quoting}

`plpy` 模块支持多个用于构建动态查询的实用字符串引用函数：

- `plpy.quote_literal(string)`：在 SQL 语句中将字符串作为字面量引用，并正确处理单引号和反斜杠。
- `plpy.quote_nullable(string)`：与上述函数相同，但输入为 `null` 时返回 `NULL`。
- `plpy.quote_ident(string)`：在 SQL 语句中将字符串作为标识符引用，仅在必要时添加引号。

#### 全局字典 {#global-dictionaries}

`plpy` 模块提供两个特殊的全局字典，用于在函数调用之间持久化数据：

- **GD（全局字典）**：该字典在同一容器内的所有函数调用之间共享。只要容器实例存活，数据就会持久存在。
- **SD（静态字典）**：该字典只在同一函数的多次调用之间共享数据。

> [!NOTE]
> 请注意，容器的生命周期与会话关联。数据库终止空闲会话时，相关容器也会销毁，GD 和 SD 中的数据将丢失。

### PL/R 函数简介 {#about-plr-functions}

PL/Container 中的 `pg.spi` 模块提供了供 R 语言与数据库交互的方法：

- `pg.spi.exec(stmt)`：执行 SQL 查询并返回 R `data.frame`。
- `pg.spi.prepare(stmt[, argtypes])`：准备查询计划。
- `pg.spi.execp(plan[, argtypes])`：执行准备好的查询计划。
- `pg.spi.debug(msg)`、`pg.spi.log(msg)`、`pg.spi.info(msg)`、`pg.spi.notice(msg)`、`pg.spi.warning(msg)`、`pg.spi.error(msg)`、`pg.spi.fatal(msg)`：向数据库日志系统发送不同级别的日志消息。

### 函数限制 {#function-limitations}

使用 PL/Container 时请注意以下限制：

- 不支持数据库域。
- 不支持多维数组。
- 调试 UDF 时不显示 Python 和 R 的调用栈信息。
- 不支持 `plpy.execute()` 的 `nrows()` 和 `status()` 方法。
- 不支持 PL/Python 的 `plpy.SPIError()` 方法。
- 不支持在 `plpy.execute()` 中运行 `SAVEPOINT` 命令。
- 不支持容器流控制。
- 不支持触发器。
- 不支持 `OUT` 参数。
- PL/Python 函数不能直接返回 Python `dict` 类型，但可以在返回前将其转换为数据库用户定义类型（UDT）。

## 管理 PL/Container {#manage-plcontainer}

### 管理会话中的配置和容器 {#manage-configurations-and-containers-in-a-session}

PL/Container 提供了一些内置视图和函数，帮助你在数据库会话中查看和管理配置。

- **刷新配置**：如果在外部修改了 `plcontainer_configuration.xml` 文件，可以在会话中运行以下命令，强制重新加载配置而无需重启数据库。

    ```sql
    SELECT * FROM plcontainer_refresh_config;
    ```

    此命令返回 Coordinator 和所有 Segment 实例上的配置刷新状态。

- **查看当前配置**：

    ```sql
    SELECT * FROM plcontainer_show_config;
    ```

    此命令执行 PL/Container 函数，显示 Coordinator 和所有 Segment 实例的配置信息。

- **查看运行中的容器**：

    ```sql
    SELECT * FROM plcontainer_containers_summary();
    ```

    如果由普通用户运行，该函数只显示该用户创建的容器。如果由超级用户运行，则显示所有用户创建的容器。输出包括 Segment ID、容器 ID、运行时、所有者和内存使用量。

## 高级主题 {#advanced-topics}

### 资源管理 {#resource-management}

Docker 容器与同一主机上的 Apache Cloudberry 数据库服务共享 CPU 和内存资源。默认情况下，数据库并不知道 PL/Container 实例消耗的资源。可以使用数据库的资源组功能控制 PL/Container 实例的 CPU 资源总用量。

PL/Container 在两个层级管理资源：容器级别和运行时级别。可以通过为运行时配置 `memory_mb` 和 `cpu_share` 设置来控制容器级别的 CPU 和内存资源。`memory_mb` 控制每个容器实例可用的内存资源，而 `cpu_share` 定义容器相对于其他容器的 CPU 使用权重。

> [!NOTE]
> 如果没有为 PL/Container 运行时显式配置资源组，其容器实例将只受系统资源限制。这可能导致容器消耗过多资源，进而影响数据库服务器的性能。

#### 配置过程 {#configuration-process}

要使用资源组管理 PL/Container 的 CPU 资源，需要同时显式配置资源组和 PL/Container。

1. **规划资源分配**：

    - 分析部署环境的资源使用情况，确定要分配给 PL/Container Docker 容器的 CPU 资源百分比。
    - 决定如何在不同 PL/Container 运行时之间分配这些资源。明确所需资源组的数量、每个组的 CPU 百分比，以及资源组与运行时之间的映射关系。

2. **创建资源组**：根据规划创建资源组。例如，假设决定为 PL/Container 分配 25% 的 CPU 资源，并按 60/40 的比例分配给两个不同的资源组：

    ```sql
    -- Creates a resource group for the R runtime, allocating 15% CPU.
    CREATE RESOURCE GROUP plr_run1_rg WITH (CONCURRENCY=0, CPU_MAX_PERCENT=15);
    
    -- Creates a resource group for the Python runtime, allocating 10% CPU.
    CREATE RESOURCE GROUP plpy_run1_rg WITH (CONCURRENCY=0, CPU_MAX_PERCENT=10);
    ```

3. **获取资源组 ID**：查询 `gp_toolkit.gp_resgroup_config` 视图，获取所创建资源组的 `groupid`。

    ```sql
    SELECT groupname, groupid FROM gp_toolkit.gp_resgroup_config
    WHERE groupname IN ('plpy_run1_rg', 'plr_run1_rg');
    
    -- Example output:
    --  groupname   |  groupid
    -- --------------+----------
    --  plpy_run1_rg |   16391
    --  plr_run1_rg  |   16393
    -- (2 rows)
    ```

4. **将资源组分配给运行时**：使用 `plcontainer runtime-add`（用于新运行时）或 `plcontainer runtime-replace`（用于已有运行时）命令，通过 `-s resource_group_id=<groupid>` 参数分配资源组。

    ```bash
    # Assigns a resource group to the new python_run1 runtime.
    plcontainer runtime-add -r python_run1 -i pivotaldata/plcontainer_python_shared:devel -l python -s resource_group_id=16391
    
    # Replaces and assigns a resource group to the existing r_run1 runtime.
    plcontainer runtime-replace -r r_run1 -i pivotaldata/plcontainer_r_shared:devel -l r -s resource_group_id=16393
    ```

    也可以使用 `plcontainer runtime-edit` 命令手动编辑配置文件，以分配资源组。

将资源组分配给运行时后，共享该运行时配置的所有容器实例都将受到该资源组配置的 CPU 限制。如果删除正在使用的 PL/Container 资源组，数据库将终止正在运行的容器。

### 日志记录 {#logging}

启用 PL/Container 的日志功能后，可以通过数据库的 `log_min_messages` 参数设置日志级别（默认为 `warning`）。此参数同时控制数据库和 PL/Container 的日志级别。

- **启用日志记录**：PL/Container 日志记录按运行时 ID 启用，并由 `use_container_logging` 设置控制，该设置默认为不记录日志。
- **日志内容和位置**：PL/Container 日志消息来自 Docker 容器中运行的 UDF。在 Red Hat 8 系统上，日志消息默认发送到 `journald` 服务。数据库日志消息发送到 Coordinator 节点上的日志文件。
- **动态调整日志级别**：测试或排查问题时，可以在会话中使用 `SET` 命令临时更改日志级别，例如改为 `debug1`。

    ```sql
    SET log_min_messages='debug1';
    ```

> [!NOTE]
> `log_min_messages` 参数同时影响数据库和 PL/Container 的日志记录。提高日志级别可能影响数据库性能，即使当前没有运行 PL/Container 函数。

### 使用 CUDA 加速 GPU {#use-cuda-for-gpu-acceleration}

PL/Container 支持使用 NVIDIA GPU 加速计算。这需要准备包含 CUDA Toolkit 及相应 Python 库（例如 PyCUDA）的自定义 Docker 镜像，并进行相应配置。

#### 前提条件 {#prerequisites-1}

- Docker 引擎版本不低于 v19.03。
- PL/Container 版本不低于 2.2.0。
- 主机上至少有一个 NVIDIA GPU，并已安装相应的 GPU 驱动程序。
- 已安装 NVIDIA Container Toolkit，并已验证 `nvidia-docker` 镜像可以成功使用 GPU。

#### 安装并自定义 PL/Container 镜像 {#install-and-customize-the-plcontainer-image}

1. **加载基础镜像**：从官方渠道获取 PL/Container Python 3 镜像并将其加载到 Docker 中。

    ```bash
    docker image load < plcontainer-python3-image-*.tar.gz
    ```

2. **自定义镜像**：创建 Dockerfile，将 CUDA 运行时和 `pycuda` 库添加到基础镜像中。以下是添加 CUDA 11.7 和 `pycuda` 2021.1 的 Dockerfile 内容示例：

    ```dockerfile
    FROM pivotaldata/plcontainer_python3_shared:devel
    
    ENV XKBLAYOUT=en
    ENV DEBIAN_FRONTEND=noninteractive
    
    # Install CUDA from https://developer.nvidia.com/cuda-downloads
    # By downloading and using the software, you agree to fully comply with the terms and conditions of the CUDA EULA.
    RUN true &&\
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu2204.pin && \
        mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
        wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-ubuntu1804-11-7-local_11.7.0-515.43.04-1_amd64.deb && \
        dpkg -i cuda-repo-ubuntu1804-11-7-local_11.7.0-515.43.04-1_amd64.deb && \
        cp /var/cuda-repo-ubuntu1804-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/ && \
        apt-get update && \
        apt-get -y install cuda && \
        rm cuda-repo-ubuntu1804-11-7-local_11.7.0-515.43.04-1_amd64.deb &&\
        rm -rf /var/lib/apt/lists/*
    
    ENV PATH="/usr/local/cuda-11.7/bin/:${PATH}"
    ENV LD_LIBRARY_PATH="/usr/local/cuda-11.7/lib64:${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
    ENV CUDA_HOME="/usr/local/cuda-11.7"
    
    RUN true && \
        python3.7 -m pip --no-cache-dir install typing-extensions==3.10.0.0 && \
        python3.7 -m pip --no-cache-dir install Mako==1.2.0 && \
        python3.7 -m pip --no-cache-dir install platformdirs==2.5.2 && \
        python3.7 -m pip --no-cache-dir install pytools==2022.1.2 && \
        python3.7 -m pip --no-cache-dir install pycuda==2021.1
    ```

3. **构建自定义镜像**：

    ```bash
    docker build . -t localhost/plcontainer_python3_cuda_shared:latest
    ```

4. **添加并配置运行时**：

    - 添加一个新运行时，并将其关联到刚构建的镜像。

        ```bash
        plcontainer runtime-add -r plc_python_cuda_shared -I localhost/plcontainer_python3_cuda_shared:latest -l python3
        ```

    - 编辑运行时配置，为其分配 GPU 设备。

        ```bash
        plcontainer runtime-edit
        ```

        在 XML 配置中，为此运行时添加一个 `<device_request>` 部分。

        ```xml
        <runtime>
            <id>plc_python_cuda_shared</id>
            <image>localhost/plcontainer_python3_cuda_shared:latest</image>
            ...
            <device_request type="gpu">
                <deviceid>0</deviceid> <!-- Specifies the ID of the GPU device. -->
            </device_request>
        </runtime>
        ```

#### 创建并运行 CUDA 函数示例 {#create-and-run-a-cuda-function-example}

1. 连接数据库并创建使用 CUDA 运行时的函数。

    ```sql
    CREATE FUNCTION hello_cuda() RETURNS float4[] AS $$
    # container: plc_python_cuda_shared
    
    import pycuda.driver as drv
    import pycuda.tools
    import pycuda.autoinit
    import numpy
    import numpy.linalg as la
    from pycuda.compiler import SourceModule
    
    mod = SourceModule("""
    __global__ void multiply_them(float *dest, float *a, float *b)
    {
      const int i = threadIdx.x;
      dest[i] = a[i] * b[i];
    }
    """)
    
    multiply_them = mod.get_function("multiply_them")
      
    a = numpy.random.randn(400).astype(numpy.float32)
    b = numpy.random.randn(400).astype(numpy.float32)
    
    dest = numpy.zeros_like(a)
    multiply_them(
            drv.Out(dest), drv.In(a), drv.In(b),
            block=(400,1,1))
      
    return [float(i) for i in (dest-a*b)]
    
    $$ LANGUAGE plcontainer;
    ```

2. 执行函数并验证结果。

    ```sql
    -- Calculates the sum of the resulting array, which is expected to be 0.0.
    WITH a AS (SELECT unnest(hello) AS cuda FROM hello_cuda() AS hello) SELECT sum(cuda) FROM a;
    ```

### 配置远程 PL/Container {#configure-remote-plcontainer}

可以配置集群外部的一个或多个远程主机来执行 PL/Container 工作负载，从而降低数据库主机上的计算开销。

#### 前提条件 {#prerequisites-2}

- PL/Container 版本不低于 2.4.0。
- 远程主机上已安装 Docker 引擎（版本不低于 v19.03），并且你拥有 `root` 或 `sudo` 权限。

#### 步骤 1：配置远程主机 {#step-1-configure-the-remote-host}

1. **安装 Docker**：在远程主机上安装 Docker。

2. **启用远程 API**：编辑 Docker 服务文件，使其监听 TCP 端口（例如 2375）。

    ```bash
    sudo systemctl edit docker.service
    
    # Adds the following content to the beginning of the file:
    [Service]
    ExecStart=
    ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375
    
    # Restarts the Docker service.
    sudo systemctl restart docker
    ```

3. **准备远程环境**：确保远程主机上已安装 `gpadmin` 用户、无密码 SSH 访问、`python3` 和 `rsync`。然后从 Coordinator 节点执行远程设置。

    ```bash
    # Creates a directory on the remote host.
    ssh gpadmin@<remoteip> "sudo mkdir $GPHOME && sudo chown gpadmin:gpadmin $GPHOME"
    
    # Copies the plcontainer client from the coordinator to the remote host (multiple hosts can be specified).
    plcontainer remote-setup --hosts <remoteip_1>,<remoteip_2>
    ```

#### 步骤 2：将 Docker 镜像加载到远程主机 {#step-2-load-the-docker-image-to-the-remote-host}

从 Coordinator 节点将所需 Docker 镜像加载到一个或多个远程主机。

```bash
plcontainer image-add --hosts <remoteip_1>,<remoteip_2> -f <image_file>
```

#### 步骤 3：配置后端节点 {#step-3-configure-the-backend-node}

1. 在 Coordinator 节点上编辑 PL/Container 配置文件。

    ```bash
    plcontainer runtime-edit
    ```

2. 在 XML 文件中添加新的 `<backend>` 部分以定义远程主机集群。然后修改现有的 `<runtime>` 部分，通过 `<backend name="..."/>` 使用新定义的后端。

    ```xml
    <?xml version="1.0" ?>
    <configuration>
        <backend name="calculate_cluster" type="remote_docker">
            <address>REMOTE_HOST_IP</address>
            <port>2375</port>
        </backend>
        <runtime>
            <id>plc_python_remote</id>
            <image>your_image:tag</image>
            <command>/clientdir/py3client.sh</command>
            <shared_directory access="ro" container="/clientdir" host="/usr/local/greenplum-db/bin/plcontainer_clients"/>
            <backend name="calculate_cluster" />
            <setting enable_network="yes" roles="gpadmin" />
        </runtime>
    </configuration>
    ```

    如果有多个远程主机，需要为它们创建不同的后端和运行时配置。

#### 步骤 4：验证配置 {#step-4-verify-the-configuration}

创建使用远程运行时的函数并执行。如果执行成功，则表示函数已在远程主机上运行。

```sql
CREATE FUNCTION dummy_remote_python() RETURNS text AS $$
# container: plc_python_remote
return 'hello from a remote Python container'
$$ LANGUAGE plcontainer;

SELECT * from dummy_remote_python();
```

## 说明 {#notes}

- 如果 PL/Container Docker 容器超过允许的最大内存，将带有内存不足警告而终止。
- PL/Container 不限制 Docker 容器的基础设备大小。在某些情况下，该大小由 Docker 守护进程控制。例如，如果 Docker 存储驱动程序为 `devicemapper`，其基础大小默认为 10GB。可以使用 `docker info` 命令查看存储驱动程序及相关配置。
- 执行 PL/Container UDF 时，查询执行器（QE）进程会启动，并按需复用 Docker 容器。空闲一段时间后，QE 进程退出并销毁其 Docker 容器。可以通过 `gp_vmem_idle_resource_timeout` 参数控制空闲时间，从而影响容器复用策略。但请注意，修改此参数也会影响其他数据库资源的回收，可能影响性能。
