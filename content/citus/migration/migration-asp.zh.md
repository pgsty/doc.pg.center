---
title: ASP.NET
description: 介绍如何构建以 Citus 为存储后端的多租户 ASP.NET 应用。
weight: 80
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-asp?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

[确定分布策略](/citus/migration/migration-schema/)介绍了多租户场景下使用 Citus 所需的、与框架无关的数据库变更。本文进一步介绍如何构建以 Citus 为存储后端的多租户 ASP.NET 应用。

## 示例应用 {#example-app}

为了具体说明迁移过程，我们以一个简化版的 StackExchange 为例。

### 模式 {#schema}

首先创建两张表：

```sql
CREATE TABLE tenants (
    id uuid NOT NULL,
    domain text NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);

CREATE TABLE questions (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    title text NOT NULL,
    votes int NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL
);

ALTER TABLE tenants ADD PRIMARY KEY (id);
ALTER TABLE questions ADD PRIMARY KEY (id, tenant_id);
```

示例应用中的每个租户都通过不同的域名连接。ASP.NET Core 检查传入请求，并在 `tenants` 表中查找该域名。也可以根据子域名或其他方式识别租户。

注意，`questions` 表也保存了 `tenant_id`。这种结构使数据共置成为可能。创建表后，使用 `create_distributed table` 告诉 Citus 按租户 ID 分片：

```sql
SELECT create_distributed_table('tenants', 'id');
SELECT create_distributed_table('questions', 'tenant_id');
```

接下来插入一些测试数据。

```sql
INSERT INTO tenants VALUES (
    'c620f7ec-6b49-41e0-9913-08cfe81199af',
    'bufferoverflow.local',
    'Buffer Overflow',
    'Ask anything code-related!',
    now(),
    now());

INSERT INTO tenants VALUES (
    'b8a83a82-bb41-4bb3-bfaa-e923faab2ca4',
    'dboverflow.local',
    'Database Questions',
    'Figure out why your connection string is broken.',
    now(),
    now());

INSERT INTO questions VALUES (
    '347b7041-b421-4dc9-9e10-c64b8847fedf',
    'c620f7ec-6b49-41e0-9913-08cfe81199af',
    'How do you build apps in ASP.NET Core?',
    1,
    now(),
    now());

INSERT INTO questions VALUES (
    'a47ffcd2-635a-496e-8c65-c1cab53702a7',
    'b8a83a82-bb41-4bb3-bfaa-e923faab2ca4',
    'Using postgresql for multitenant data?',
    2,
    now(),
    now());
```

数据库结构和示例数据准备好后，就可以开始配置 ASP.NET Core。

### ASP.NET Core 项目 {#aspnet-core-project}

如果尚未安装 ASP.NET Core，请安装 [Microsoft 的 .NET Core SDK](https://dot.net/core)。以下说明使用 `dotnet` CLI；如果使用 Windows，也可以使用 Visual Studio 2017 或更新版本。

使用 `dotnet new` 从 MVC 模板创建新项目：

```dotnetcli
dotnet new mvc -o QuestionExchange
cd QuestionExchange
```

如有需要，可以运行 `dotnet run` 预览模板网站。模型—视图—控制器（MVC）模板几乎包含了入门所需的一切，但默认不支持 PostgreSQL。可以安装 [Npgsql.EntityFrameworkCore.PostgreSQL](https://www.nuget.org/packages/Npgsql.EntityFrameworkCore.PostgreSQL/) 包来添加支持：

```dotnetcli
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
```

这个包为 Entity Framework Core 添加 PostgreSQL 支持；Entity Framework Core 是 ASP.NET Core 默认的对象关系映射（ORM）和数据库层。打开 `Startup.cs`，在 `ConfigureServices` 方法中加入以下代码：

```csharp
var connectionString = "connection-string";

services.AddEntityFrameworkNpgsql()
    .AddDbContext<AppDbContext>(options => options.UseNpgsql(connectionString));
```

还需要在文件顶部加入以下声明：

```csharp
using Microsoft.EntityFrameworkCore;
using QuestionExchange.Models;
```

将 `connection-string` 替换为你的 Citus 连接字符串。我的连接字符串如下：

`Server=myformation.db.citusdata.com;Port=5432;Database=citus;Userid=citus;Password=mypassword;SslMode=Require;Trust Server Certificate=true;`

接下来需要定义数据库上下文。

## 为应用添加租户支持 {#adding-tenancy-to-the-app}

有了数据库结构和示例数据后，需要配置 ASP.NET Core 应用，使其能够识别和处理不同租户。SaasKit 提供中间件来拦截传入请求，并根据域名识别发起请求的租户。本节介绍如何配置租户解析器，并将其集成到应用请求管道中。

### 定义 Entity Framework Core 上下文和模型 {#define-the-entity-framework-core-context-and-models}

数据库上下文类是代码与数据库之间的接口。Entity Framework Core 通过它了解[数据模式](https://msdn.microsoft.com/library/jj679962(v=vs.113).aspx#Anchor_2)，因此需要定义数据库中有哪些表。

在项目根目录创建 `AppDbContext.cs` 文件，加入以下代码：

```csharp
using System.Linq;
using Microsoft.EntityFrameworkCore;
using QuestionExchange.Models;
namespace QuestionExchange
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options)
            : base(options)
        {
        }

        public DbSet<Tenant> Tenants { get; set; }

        public DbSet<Question> Questions { get; set; }
    }
}
```

两个 `DbSet` 属性指定了用哪些 C# 类来表示每张表中的行。接下来会创建这些类，不过在此之前，先在 `Questions` 属性下面添加一个新方法：

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    var mapper = new Npgsql.NpgsqlSnakeCaseNameTranslator();
    var types = modelBuilder.Model.GetEntityTypes().ToList();

    // Refer to tables in snake_case internally
    types.ForEach(e => e.Relational().TableName = mapper.TranslateMemberName(e.Relational().TableName));

    // Refer to columns in snake_case internally
    types.SelectMany(e => e.GetProperties())
        .ToList()
        .ForEach(p => p.Relational().ColumnName = mapper.TranslateMemberName(p.Relational().ColumnName));
}
```

按照惯例，C# 类名和属性名采用 PascalCase，而 PostgreSQL 表名和列名使用小写的 snake_case。`OnModelCreating` 方法可以覆盖默认的名称转换规则，让 Entity Framework Core 知道如何在数据库中找到相应实体。

现在添加表示租户和问题的类。在 Models 目录创建 `Tenant.cs` 文件：

```csharp
using System;

namespace QuestionExchange.Models
{
    public class Tenant
    {
        public Guid Id { get; set; }

        public string Domain { get; set; }

        public string Name { get; set; }

        public string Description { get; set; }

        public DateTimeOffset CreatedAt { get; set; }

        public DateTimeOffset UpdatedAt { get; set; }
    }
}
```

同样在 Models 目录创建 `Question.cs` 文件：

```csharp
using System;

namespace QuestionExchange.Models
{
    public class Question
    {
        public Guid Id { get; set; }

        public Tenant Tenant { get; set; }

        public string Title { get; set; }

        public int Votes { get; set; }

        public DateTimeOffset CreatedAt { get; set; }

        public DateTimeOffset UpdatedAt { get; set; }
    }
}
```

注意 `Tenant` 属性。数据库中的问题表包含 `tenant_id` 列。Entity Framework Core 能识别出该属性表示租户与问题之间的一对多关系。稍后查询数据时会用到它。

至此，已经配置好 Entity Framework Core 和到 Citus 的连接。下一步是为 ASP.NET Core 请求管道添加多租户支持。

### 安装 SaasKit {#install-saaskit}

[SaasKit](https://github.com/saaskit/saaskit) 是一个优秀的开源 ASP.NET Core 中间件。它可以轻松让 `Startup` 请求管道[感知租户](http://benfoster.io/blog/asp-net-5-multitenancy)，也足够灵活，能处理多种多租户场景。

安装 [SaasKit.Multitenancy](https://www.nuget.org/packages/SaasKit.Multitenancy/) 包：

```dotnetcli
dotnet add package SaasKit.Multitenancy
```

SaasKit 需要租户模型和租户解析器才能工作。前者已经存在，即先前创建的 `Tenant` 类。现在在项目根目录创建 `CachingTenantResolver.cs` 文件：

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using SaasKit.Multitenancy;
using QuestionExchange.Models;

namespace QuestionExchange
{
    public class CachingTenantResolver : MemoryCacheTenantResolver<Tenant>
    {
        private readonly AppDbContext _context;

        public CachingTenantResolver(
            AppDbContext context, IMemoryCache cache, ILoggerFactory loggerFactory)
             : base(cache, loggerFactory)
        {
            _context = context;
        }

        // Resolver runs on cache misses
        protected override async Task<TenantContext<Tenant>> ResolveAsync(HttpContext context)
        {
            var subdomain = context.Request.Host.Host.ToLower();

            var tenant = await _context.Tenants
                .FirstOrDefaultAsync(t => t.Domain == subdomain);

            if (tenant == null) return null;

            return new TenantContext<Tenant>(tenant);
        }

        protected override MemoryCacheEntryOptions CreateCacheEntryOptions()
            => new MemoryCacheEntryOptions().SetAbsoluteExpiration(TimeSpan.FromHours(2));

        protected override string GetContextIdentifier(HttpContext context)
            => context.Request.Host.Host.ToLower();

        protected override IEnumerable<string> GetTenantIdentifiers(TenantContext<Tenant> context)
            => new string[] { context.Tenant.Domain };
    }
}
```

`ResolveAsync` 方法负责主要的处理工作。收到请求后，它会查询数据库，寻找与当前域名匹配的租户。如果找到，就向 SaasKit 返回一个 `TenantContext`。租户解析逻辑完全由你决定，可以根据子域名、路径或任何其他方式区分租户。

这个实现采用[租户缓存策略](http://benfoster.io/blog/aspnet-core-multi-tenancy-tenant-lifetime)，避免每次请求都查询数据库来查找租户。首次查找后，租户会缓存两小时；你可以按需要调整这一时长。

租户模型和租户解析器准备好后，打开 `Startup` 类，在 `ConfigureServices` 方法中加入以下代码：

```csharp
services.AddMultitenancy<Tenant, CachingTenantResolver>();
```

接下来，在 `Configure` 方法中的 `UseStaticFiles` 之后、**`UseMvc` 之前**加入这一行：

```csharp
app.UseMultitenancy<Tenant>();
```

`Configure` 方法定义了实际的请求管道，因此顺序很重要！

### 更新视图 {#update-views}

所有组件都已就绪，现在可以在代码和视图中引用当前租户。打开 `Views/Home/Index.cshtml` 视图，将整个文件替换为以下标记：

```html
@inject Tenant Tenant
@model QuestionListViewModel

@{
    ViewData["Title"] = "Home Page";
}

<div class="row">
    <div class="col-md-12">
        <h1>Welcome to <strong>@Tenant.Name</strong></h1>
        <h3>@Tenant.Description</h3>
    </div>
</div>

<div class="row">
    <div class="col-md-12">
        <h4>Popular questions</h4>
        <ul>
            @foreach (var question in Model.Questions)
            {
                <li>@question.Title</li>
            }
        </ul>
    </div>
</div>
```

`@inject` 指令从 SaasKit 获取当前租户，`@model` 指令则告诉 ASP.NET Core，此视图使用一个即将创建的新模型类。在 Models 目录创建 `QuestionListViewModel.cs` 文件：

```csharp
using System.Collections.Generic;

namespace QuestionExchange.Models
{
    public class QuestionListViewModel
    {
    public IEnumerable<Question> Questions { get; set; }
    }
}
```

### 查询数据库 {#query-the-database}

`HomeController` 负责渲染刚才编辑的首页视图。打开它，将 `Index()` 方法替换为：

```csharp
public async Task<IActionResult> Index()
{
    var topQuestions = await _context
        .Questions
        .Where(q => q.Tenant.Id == _currentTenant.Id)
        .OrderByDescending(q => q.UpdatedAt)
        .Take(5)
        .ToArrayAsync();

    var viewModel = new QuestionListViewModel
    {
        Questions = topQuestions
    };

    return View(viewModel);
}
```

这个查询获取当前租户最新的五个问题，并填充视图模型——当然，目前只有一个问题。

> [!NOTE]
> 对于大型应用，通常应将数据访问代码放在服务层或仓储层，而不是控制器中。这里只是一个简单示例！

刚添加的代码需要 `_context` 和 `_currentTenant`，但控制器中还没有这两个成员。可以通过为类添加构造函数来提供它们：

```csharp
public class HomeController : Controller
{
    private readonly AppDbContext _context;
    private readonly Tenant _currentTenant;

    public HomeController(AppDbContext context, Tenant tenant)
    {
        _context = context;
        _currentTenant = tenant;
    }

    // Existing code...
```

为避免编译器报错，请在文件顶部添加以下声明：

```csharp
using Microsoft.EntityFrameworkCore;
```

### 测试应用 {#test-the-app}

先前加入数据库的测试租户分别对应两个虚构域名：`bufferoverflow.local` 和 `dboverflow.local`。要在本机测试，编辑 hosts 文件，添加这些域名：

- `127.0.0.1 bufferoverflow.local`
- `127.0.0.1 dboverflow.local`

使用 `dotnet run` 或在 Visual Studio 中选择“启动”来运行项目，应用会开始监听类似 `localhost:5000` 的地址。如果直接访问这个地址，会看到错误，因为还没有配置[默认租户行为](http://benfoster.io/blog/handling-unresolved-tenants-in-saaskit)。

改为访问 `http://bufferoverflow.local:5000`，就可以看到多租户应用中的一个租户！访问 `http://dboverflow.local:5000` 则可以查看另一个租户。现在，要添加更多租户，只需向 `tenants` 表插入更多行。

## 相关内容 {#related-content}

- [多租户模式迁移](/citus/migration/migration-schema/)
- [多租户查询迁移](/citus/migration/migration-query/)
- [迁移概述](/citus/migration/migration/)
