---
title: "pg_file_settings"
description: "The `pg_file_settings` view provides a summary of the server's configuration files, showing each parameter's name, value, source file, line number, whether it was applied successfully, and any associated error messages."
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-file-settings.md"
---

This view is useful for validating configuration changes and diagnosing issues in the configuration files.

|name|type|references|description|
|----|----|----------|-----------|
|`sourcefile`|text| |Full path name of the configuration file.|
|`sourceline`|integer| |Line number within the configuration file where the entry appears.|
|`seqno`|integer| |Order in which the entries are processed (1..n).|
|`name`|text| |Configuration parameter name.|
|`setting`|text| |Value to be assigned to the parameter.|
|`applied`|boolean| |True if the value can be applied successfully.|
|`error`|text| |If not null, an error message indicating why this entry could not be applied.|
