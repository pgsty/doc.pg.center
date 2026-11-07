---
title: IvorySQL Cloud 使用
linkTitle: IvorySQL Cloud使用
description: IvorySQL v5.6 文档：IvorySQL Cloud 使用。
type: docs
weight: 120
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/4.7.2.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

IvorySQL Cloud是一个基于Web的服务平台，用户可以在任意电脑上通过浏览器进行访问，安装云服务平台的服务器IP为192.168.31.43，然后在浏览器输入http://192.168.31.43:9104/（9104为前端nginx.conf.default中设置的端口）即可进入登录页面页面：

![image3](/ivorysql/assets/images/upstream/25fe2fd6c96a4b38feaee0b0d70113a042a13167225049b8d7925e19237b7716.png)

## 1. 登录和退出 {#sign-in-and-sign-out}

### 1.1. 用户登录 {#sign-in}

进入登录页面，根据提示输入信息即可访问IvorySQL云服务平台：

![image4](/ivorysql/assets/images/upstream/39df92f342a0ad166ee8da95d49b947b4720a376df5632077e639f1f0c9d2f8e.png)

### 1.2. 退出登录 {#sign-out}

点击页面右上角的头像，会显示当前登录用户名和“Log Out”。点击“Log Out”退出当前登录页面。点击用户名则保留当前登录页面：

![image5](/ivorysql/assets/images/upstream/697fb0e4716c61e711d2abb6e5912d8ba688e25a87a2ec7fd31dd71345768ee9.png)

## 2. 管理员功能 {#administrator-features}

### 2.1. 添加集群 {#add-a-cluster}

1.  平台登录admin用户后，点击左侧菜单栏的“K8S集群管理”按钮，进入集群管理页。

![image6](/ivorysql/assets/images/upstream/ccce7bc382db15f559a54f1869e5ee55d1ffb2ec6ff5ef3dc910a66b07bb3a24.png)

2.  点击页面左上角“增加Kubernetes集群”按钮，输入集群信息后提交。

![image7](/ivorysql/assets/images/upstream/dfd1e52ab354feaf0c5db19242244569ac88d5b98e1108a233f4e61fedb9772c.png)

### 2.2. 管理集群 {#manage-clusters}

在集群管理页面，可以查看已添加集群的详细信息，同时对集群信息进行编辑和删除操作。

![image8](/ivorysql/assets/images/upstream/4327b142d755b791792d8887747efa832093fc436030248b81defc6d63e3d980.png)

## 3. demo用户功能 {#demo-user-features}

### 3.1. 数据库订阅 {#database-subscription}

1.  使用demo用户登录平台。

2.  点击左侧菜单栏"数据库订阅"按钮，填写需要申请的数据库的各个参数，然后点击"下一步：确认信息"。

![image9](/ivorysql/assets/images/upstream/523eb75150af25351e16e81157c20a8edf39c20411e0c2b80fa7f0013e48d55f.png)

3.  检查信息后，点击"确定"

![image10](/ivorysql/assets/images/upstream/45ecbab0f85389860912111026b2a8a329a2371a24deb7d60f5ea1bf0fe41adf.png)

4.  "确定"后，会自动跳转到"数据库管理"页面，查看订阅任务

![image11](/ivorysql/assets/images/upstream/53fc665196791dd1b1fef9569d55fe28cdac5b864a87619425f595085241ebf2.png) ![image12](/ivorysql/assets/images/upstream/ec5e148a5c2c3f66eb3354347bd20d19a0df07bc3cdb2625129ae734fc2640b5.png)

### 3.2. 数据库管理 {#database-management}

显示云服务平台管理的数据库信息。

![image12](/ivorysql/assets/images/upstream/ec5e148a5c2c3f66eb3354347bd20d19a0df07bc3cdb2625129ae734fc2640b5.png)

### 3.3. 数据库重启 {#restart-a-database}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"重启"选项。

![image13](/ivorysql/assets/images/upstream/fd8ba55256051cc8f431e433bdb27431657b7b9cc93c7225506d8d4d4644ff96.png)

3.  检查信息后，点"确认"

![image14](/ivorysql/assets/images/upstream/abf8f93dfccb3f8f92656c2843b2970dc3eb78653cc17544e1ea923aef10a5bc.png)

### 3.4. 修改密码 {#change-the-password}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库管理"，选中数据库，点击"实例ID"列。

![image15](/ivorysql/assets/images/upstream/21425cdd749a739a2623d1166906fac46364731f2dd3eec5d8735ca8964d03c1.png)

3.  进入数据库详情页面，点击"修改密码"列的图标。

![image17](/ivorysql/assets/images/upstream/0b8166f056360d26ee46aeb3f2646661b7347fff8ef2e9c9f30ff9f4e3b3b1a8.png)

4.  输入新的数据库密码，点击"确定"按钮。

![image18](/ivorysql/assets/images/upstream/e2dfa87a662f1a9a518440e019380bf0434167be9ce072d1943ed2035ffe7208.png)

### 3.5. 删除实例 {#delete-an-instance}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"删除实例"选项。

![image19](/ivorysql/assets/images/upstream/e062e115c663653718660394e87135ed429373b0b88d3b2f6f9d20b92deb03d4.png)

3.  检查信息后，点击"确定"按钮。

![image20](/ivorysql/assets/images/upstream/c654ee70089baee01ff4511f42b36f6a8351250beffa05a3c53f80b0e7c0942e.png)

### 3.6. 磁盘扩容 {#storage-expansion}

1.  此功能需用户自行配置相关插件，如topolvm

2.  demo用户登录平台。

3.  点击左侧导航栏"磁盘扩容"，选中数据库，点击"操作"列的"修改"按钮；或者点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"磁盘扩容"选项。

![image21](/ivorysql/assets/images/upstream/93c173a6a436731e5fc7e88a99955e589da7afb18a0cb955fb7b11bec4adc362.png) ![image22](/ivorysql/assets/images/upstream/dd1786d96f3d02d8dd300d44f478b58f14a67c087982e749ff798eefaea93e2a.png)

4.  检查并输入磁盘扩容的大小后，点击"确定"按钮。

![image23](/ivorysql/assets/images/upstream/1b717e8c8c99a337275b68bd14cf7de65b9a390678fb3344ab4b278c18dc3294.png)

### 3.7. 规格变更 {#specification-change}

1.  demo用户登录平台。

2.  点击左侧导航栏"规格变更"，选中数据库，点击"操作"列的"修改"按钮；或者点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"规格变更"选项。

![image24](/ivorysql/assets/images/upstream/fc45236ca7a33db8278c0feabd5cc21d20d9ab1dc02cf895ad0db273736155b6.png) ![image25](/ivorysql/assets/images/upstream/32ee2cf2b5806580f35c65180c689dc4e53de87e68dbfbe7efd842016669f1b0.png)

3.  检查信息并输入规格变更的大小后，点击"确定"按钮。

![image26](/ivorysql/assets/images/upstream/d7c8d57357a77f31f7711204bd2c609e7b98f21a83442c8b04e74e2c71b7fd01.png)

### 3.8. 数据库备份 {#database-backup}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库备份"，选中数据库，点击"操作"列的"备份"；或者点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"备份"选项。

![image27](/ivorysql/assets/images/upstream/a80b2b442266967c6cd030499e2fd45de27dd9f5db368dbdd10b26351838c091.png) ![image28](/ivorysql/assets/images/upstream/efab0758fd97833bc9740a176946291ec5a0a28fb5c3917aaf568beee6d516e7.png)

3.  检查信息并输入备份名称后，点击"确定"按钮。

![image29](/ivorysql/assets/images/upstream/01895d684cbd6362ac5e93d62881482a151e22e217f6a19357a261a2252be4ca.png)

### 3.9. 数据库恢复 {#database-restore}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库恢复"，选中数据库，点击"操作"列的"查看"按钮；或者点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"恢复"选项。

![image30](/ivorysql/assets/images/upstream/ab871fff9f4ff5606f5914551cf0ec12954323668f05aedb2a27b7696693a57d.png) ![image31](/ivorysql/assets/images/upstream/d3c0d52e84dfc598548144d1ba8c39a99cabb8c237ada097678f2a2121585549.png)

3.  选择需要备份的文件后，点"操作"列的"恢复"

![image32](/ivorysql/assets/images/upstream/ba72f6e22218c2a2913573bd20f2355a4c0dce726e587f49685fe62dfb4fcdab.png) ![image33](/ivorysql/assets/images/upstream/8a912fdff406cef38c9cb6dc349b600a5ef68d302fbdafa806fb040161c38489.png)

4.  输入需要恢复的数据库信息，密码为备份前的数据库密码

![image34](/ivorysql/assets/images/upstream/84f42f17b94d66617c9d346f8f0f776d878513f85e54f12d123d4e22aea5949c.png)

5.  后续参考"4.1数据库订阅"的步骤。

### 3.10. 数据库监控 {#database-monitoring}

1.  demo用户登录平台。

2.  点击左侧导航栏"监控工具"，选择数据库所在的集群；或者点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，在下拉选项中选择"监控"选项。

![image35](/ivorysql/assets/images/upstream/3042a0654544f54524983498763965898851c127c08c36db9e2a2da0ef2fb23a.png) ![image36](/ivorysql/assets/images/upstream/38a981061547880ffb4a27697a9c24b82a16093ae374634dd25ab264b018323d.jpeg)

3.  等待监控创建完毕后，再次重复（2）中操作，跳转新页面，输入用户名：admin，密码admin，点击login登录

> ![image37](/ivorysql/assets/images/upstream/b5713aa6af6278b68651df2076b3d9fcec041c7d8c21bbccad1ff54904a3edb0.png)

4.  选择放大镜图标，点击查看监控指标。

![image39](/ivorysql/assets/images/upstream/bd76b1b5361e4478d09cc11093829e616104e29a77be19e7f2a3a5dcaac0fa97.png) ![image40](/ivorysql/assets/images/upstream/0f1448adbd1c597c66f876755e3ec0c846eeb6d7f695b6b6037ef6edeb5e29c2.png) ![image41](/ivorysql/assets/images/upstream/7342424dc2c136bc96efaaf32a0e12cc212f708194814788437660c82166a786.png) ![image42](/ivorysql/assets/images/upstream/06f7a354ca3ebc2583d98afd0d687f354dcd396829cb14a8f41fd85c228d2026.png) ![image43](/ivorysql/assets/images/upstream/bbafea777c2c4e2ba04be47f37604f515642db67653c9e32424ca21233e2b283.png) ![image44](/ivorysql/assets/images/upstream/e45d8bba09b998d4552f1e4214c59435f6630baa0cb087dfa909d697de404bbb.png)

### 3.11. 可视化登录工具 {#visual-login-tool}

1.  demo用户登录平台。

2.  点击左侧导航栏"数据库管理"，选中数据库，点击"操作"列的"更多"按钮，选择"登录"选项。

![image45](/ivorysql/assets/images/upstream/a4ba9242a4949dda42fbfac356f629869439e678b084c02d22c41773852234a2.jpeg)

3.  跳转新页面后，输入数据库用户名 <sysdba@ivyo.com> 及数据库密码，点击"Login"按钮。

![image46](/ivorysql/assets/images/upstream/4310e6730abfc366db326d70e94ca9604fbffa1f4a24c27eff36b356af5faf48.png)

4.  连接数据库，即可进行操作。
