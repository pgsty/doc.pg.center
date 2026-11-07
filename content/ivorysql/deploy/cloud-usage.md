---
title: IvorySQL Cloud usage
linkTitle: IvorySQL Cloud Usage
description: 'IvorySQL v5.6 documentation: IvorySQL Cloud usage.'
type: docs
weight: 120
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/4.7.2.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

IvorySQL Cloud is a web-based service platform that can be accessed from any computer through a browser. After installing the cloud service platform on the server with IP `192.168.31.43`, open a browser and enter <a href="http://192.168.31.43:9104/" class="bare"><code>http://192.168.31.43:9104/</code></a> (9104 is the port configured in `nginx.conf.default`) to reach the login page:

![image3](/ivorysql/assets/images/upstream/25fe2fd6c96a4b38feaee0b0d70113a042a13167225049b8d7925e19237b7716.png)

## 1. Sign In and Sign Out {#sign-in-and-sign-out}

### 1.1. Sign In {#sign-in}

On the login page, enter the prompted information to access the IvorySQL Cloud service platform:

![image4](/ivorysql/assets/images/upstream/39df92f342a0ad166ee8da95d49b947b4720a376df5632077e639f1f0c9d2f8e.png)

### 1.2. Sign Out {#sign-out}

Click the avatar in the upper-right corner to display the current username and the **Log Out** action. Click **Log Out** to exit; click the username to stay on the current page:

![image5](/ivorysql/assets/images/upstream/697fb0e4716c61e711d2abb6e5912d8ba688e25a87a2ec7fd31dd71345768ee9.png)

## 2. Administrator Features {#administrator-features}

### 2.1. Add a Cluster {#add-a-cluster}

1.  After signing in as the `admin` user, click **K8S Cluster Management** in the left navigation bar to open the cluster list.

![image6](/ivorysql/assets/images/upstream/ccce7bc382db15f559a54f1869e5ee55d1ffb2ec6ff5ef3dc910a66b07bb3a24.png)

2.  Click **Add Kubernetes Cluster** in the upper-left corner, fill in the cluster information, and submit.

![image7](/ivorysql/assets/images/upstream/dfd1e52ab354feaf0c5db19242244569ac88d5b98e1108a233f4e61fedb9772c.png)

### 2.2. Manage Clusters {#manage-clusters}

The cluster management page lists details for each cluster and allows you to edit or delete them.

![image8](/ivorysql/assets/images/upstream/4327b142d755b791792d8887747efa832093fc436030248b81defc6d63e3d980.png)

## 3. demo User Features {#demo-user-features}

### 3.1. Database Subscription {#database-subscription}

1.  Sign in with the `demo` user.

2.  Click **Database Subscription** in the left navigation, fill in the database parameters, and click **Next: Confirm**.

![image9](/ivorysql/assets/images/upstream/523eb75150af25351e16e81157c20a8edf39c20411e0c2b80fa7f0013e48d55f.png)

3.  Review the information and click **Confirm**.

![image10](/ivorysql/assets/images/upstream/45ecbab0f85389860912111026b2a8a329a2371a24deb7d60f5ea1bf0fe41adf.png)

4.  After confirming, the page automatically redirects to **Database Management** to show the subscription task.

![image11](/ivorysql/assets/images/upstream/53fc665196791dd1b1fef9569d55fe28cdac5b864a87619425f595085241ebf2.png) ![image12](/ivorysql/assets/images/upstream/ec5e148a5c2c3f66eb3354347bd20d19a0df07bc3cdb2625129ae734fc2640b5.png)

### 3.2. Database Management {#database-management}

Displays all databases managed by the cloud service platform.

![image12](/ivorysql/assets/images/upstream/ec5e148a5c2c3f66eb3354347bd20d19a0df07bc3cdb2625129ae734fc2640b5.png)

### 3.3. Restart a Database {#restart-a-database}

1.  Sign in with the `demo` user.

2.  Go to **Database Management**, select a database, click **More** in the **Actions** column, and choose **Restart**.

![image13](/ivorysql/assets/images/upstream/fd8ba55256051cc8f431e433bdb27431657b7b9cc93c7225506d8d4d4644ff96.png)

3.  Review the information and click **Confirm**.

![image14](/ivorysql/assets/images/upstream/abf8f93dfccb3f8f92656c2843b2970dc3eb78653cc17544e1ea923aef10a5bc.png)

### 3.4. Change the Password {#change-the-password}

1.  Sign in with the `demo` user.

2.  Go to **Database Management**, select a database, and click its **Instance ID**.

![image15](/ivorysql/assets/images/upstream/21425cdd749a739a2623d1166906fac46364731f2dd3eec5d8735ca8964d03c1.png)

3.  On the database details page, click the password icon.

![image17](/ivorysql/assets/images/upstream/0b8166f056360d26ee46aeb3f2646661b7347fff8ef2e9c9f30ff9f4e3b3b1a8.png)

4.  Enter a new password and click **Confirm**.

![image18](/ivorysql/assets/images/upstream/e2dfa87a662f1a9a518440e019380bf0434167be9ce072d1943ed2035ffe7208.png)

### 3.5. Delete an Instance {#delete-an-instance}

1.  Sign in with the `demo` user.

2.  Go to **Database Management**, select a database, click **More** in the **Actions** column, and choose **Delete Instance**.

![image19](/ivorysql/assets/images/upstream/e062e115c663653718660394e87135ed429373b0b88d3b2f6f9d20b92deb03d4.png)

3.  Review the confirmation window and click **Confirm**.

![image20](/ivorysql/assets/images/upstream/c654ee70089baee01ff4511f42b36f6a8351250beffa05a3c53f80b0e7c0942e.png)

### 3.6. Storage Expansion {#storage-expansion}

1.  This feature requires additional plug-ins such as TopoLVM.

2.  Sign in with the `demo` user.

3.  Click **Storage Expansion**, select a database, then click **Edit** in the **Actions** column; alternatively, go to **Database Management**, click **More**, and choose **Storage Expansion**.

![image21](/ivorysql/assets/images/upstream/93c173a6a436731e5fc7e88a99955e589da7afb18a0cb955fb7b11bec4adc362.png) ![image22](/ivorysql/assets/images/upstream/dd1786d96f3d02d8dd300d44f478b58f14a67c087982e749ff798eefaea93e2a.png)

4.  Enter the expanded storage size and click **Confirm**.

![image23](/ivorysql/assets/images/upstream/1b717e8c8c99a337275b68bd14cf7de65b9a390678fb3344ab4b278c18dc3294.png)

### 3.7. Specification Change {#specification-change}

1.  Sign in with the `demo` user.

2.  Click **Specification Change**, select a database, then click **Edit** in the **Actions** column; or go to **Database Management**, click **More**, and choose **Specification Change**.

![image24](/ivorysql/assets/images/upstream/fc45236ca7a33db8278c0feabd5cc21d20d9ab1dc02cf895ad0db273736155b6.png) ![image25](/ivorysql/assets/images/upstream/32ee2cf2b5806580f35c65180c689dc4e53de87e68dbfbe7efd842016669f1b0.png)

3.  Enter the new specification and click **Confirm**.

![image26](/ivorysql/assets/images/upstream/d7c8d57357a77f31f7711204bd2c609e7b98f21a83442c8b04e74e2c71b7fd01.png)

### 3.8. Database Backup {#database-backup}

1.  Sign in with the `demo` user.

2.  Go to **Database Backup**, select a database, and click **Backup** in the **Actions** column; or go to **Database Management**, click **More**, and choose **Backup**.

![image27](/ivorysql/assets/images/upstream/a80b2b442266967c6cd030499e2fd45de27dd9f5db368dbdd10b26351838c091.png) ![image28](/ivorysql/assets/images/upstream/efab0758fd97833bc9740a176946291ec5a0a28fb5c3917aaf568beee6d516e7.png)

3.  Enter a backup name and click **Confirm**.

![image29](/ivorysql/assets/images/upstream/01895d684cbd6362ac5e93d62881482a151e22e217f6a19357a261a2252be4ca.png)

### 3.9. Database Restore {#database-restore}

1.  Sign in with the `demo` user.

2.  Go to **Database Restore**, select a database, and click **View** in the **Actions** column; or go to **Database Management**, click **More**, and choose **Restore**.

![image30](/ivorysql/assets/images/upstream/ab871fff9f4ff5606f5914551cf0ec12954323668f05aedb2a27b7696693a57d.png) ![image31](/ivorysql/assets/images/upstream/d3c0d52e84dfc598548144d1ba8c39a99cabb8c237ada097678f2a2121585549.png)

3.  Select the backup file and click **Restore** in the **Actions** column.

![image32](/ivorysql/assets/images/upstream/ba72f6e22218c2a2913573bd20f2355a4c0dce726e587f49685fe62dfb4fcdab.png) ![image33](/ivorysql/assets/images/upstream/8a912fdff406cef38c9cb6dc349b600a5ef68d302fbdafa806fb040161c38489.png)

4.  Enter the target database information. Use the database password from before the backup.

![image34](/ivorysql/assets/images/upstream/84f42f17b94d66617c9d346f8f0f776d878513f85e54f12d123d4e22aea5949c.png)

5.  Continue following the workflow described in “4.1 Database Subscription”.

### 3.10. Database Monitoring {#database-monitoring}

1.  Sign in with the `demo` user.

2.  Click **Monitoring Tools** in the left navigation and select the cluster where the database resides; or go to **Database Management**, select a database, click **More**, and choose **Monitoring**.

![image35](/ivorysql/assets/images/upstream/3042a0654544f54524983498763965898851c127c08c36db9e2a2da0ef2fb23a.png) ![image36](/ivorysql/assets/images/upstream/38a981061547880ffb4a27697a9c24b82a16093ae374634dd25ab264b018323d.jpeg)

3.  After the monitoring stack is created, repeat step (2) to open the monitoring page, then sign in with `admin/admin` and click **Login**.

> ![image37](/ivorysql/assets/images/upstream/b5713aa6af6278b68651df2076b3d9fcec041c7d8c21bbccad1ff54904a3edb0.png)

4.  Click the magnifying glass icon to view monitoring metrics.

![image39](/ivorysql/assets/images/upstream/bd76b1b5361e4478d09cc11093829e616104e29a77be19e7f2a3a5dcaac0fa97.png) ![image40](/ivorysql/assets/images/upstream/0f1448adbd1c597c66f876755e3ec0c846eeb6d7f695b6b6037ef6edeb5e29c2.png) ![image41](/ivorysql/assets/images/upstream/7342424dc2c136bc96efaaf32a0e12cc212f708194814788437660c82166a786.png) ![image42](/ivorysql/assets/images/upstream/06f7a354ca3ebc2583d98afd0d687f354dcd396829cb14a8f41fd85c228d2026.png) ![image43](/ivorysql/assets/images/upstream/bbafea777c2c4e2ba04be47f37604f515642db67653c9e32424ca21233e2b283.png) ![image44](/ivorysql/assets/images/upstream/e45d8bba09b998d4552f1e4214c59435f6630baa0cb087dfa909d697de404bbb.png)

### 3.11. Visual Login Tool {#visual-login-tool}

1.  Sign in with the `demo` user.

2.  Go to **Database Management**, select a database, click **More** in the **Actions** column, and choose **Login**.

![image45](/ivorysql/assets/images/upstream/a4ba9242a4949dda42fbfac356f629869439e678b084c02d22c41773852234a2.jpeg)

3.  On the new page, enter the database account `sysdba@ivyo.com` and the database password, then click **Login**.

![image46](/ivorysql/assets/images/upstream/4310e6730abfc366db326d70e94ca9604fbffa1f4a24c27eff36b356af5faf48.png)

4.  Once the connection is established, you can operate on the database.
