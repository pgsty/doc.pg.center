---
title: Extensions
linkTitle: Early extension plan
description: The original plan for TDS, language, and datatype extensions.
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_architecture/extensions.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!WARNING] Historical design material
> This early design file was retained in the upstream source but was not an active website documentation collection. It is preserved for historical reference, not as a current compatibility matrix. See [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) for current documentation.

Given below is the overall strategy for Extensions. Team is in the process of creating these extensions.


| Extension | Proposed Name | Description          |            
| -- | -- | -- |
| TDS Extension | babelfishpg_tds   | TDS - provides a secondary endpoint that speaks the TDS (SQL Server) network protocol; applications written for SQL Server should connect to this endpoint. TDS Extension has two parts - the extension itself and the protocol hooks that are needed for this extension to work. The protocol hooks have already been submitted to the Community. You can see the discussion [here](https://www.postgresql.org/message-id/flat/CAGBW59d5SjLyJLt-jwNv%2BoP6esbD8SCB%3D%3D%3D11WVe5%3DdOHLQ5wQ%40mail.gmail.com)               |    
| Language Extension | babelfishpg_tsql  | Provides a procedural language compatible with TSQL Uses ANTLR parser.   |       
| Data Type Extension 2 | babelfishpg_common  | Extension for all other data types developed by Babelfish Engineering team along with the dependent functions, indexes, operators etc All datatypes in other extensions will be extracted and added to this extension.    |  
| Data Type Extension 1 | Fixeddecimal  | This extension was forked from Fixeddecimal datatype developed by 2ndquadrant. We are making sure we properly fork the repo from the original so it tracks back to the original authors giving them credit. We'll track all the development history. **Naming convention**: We would like to keep the same name as in the original source. Additionally, the plan is to submit this back to 2nd Quadrant with the enhancements we have made for use in Babelfish. https://github.com/2ndQuadrant/fixeddecimal/blob/master/fixeddecimal.c     |
