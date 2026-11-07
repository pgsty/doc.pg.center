---
title: 内置数据类型与内置函数
linkTitle: 内置数据类型与内置函数
description: IvorySQL v5.6 文档：内置数据类型与内置函数。
type: docs
weight: 170
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/7.8.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 内置数据类型 {#built-in-data-types}

|                                |
|--------------------------------|
| char                           |
| varchar                        |
| varchar2                       |
| number                         |
| binary_float                   |
| binary_double                  |
| date                           |
| timestamp                      |
| timestamp with time zone       |
| timestamp with local time zone |
| interval year to month         |
| interval day to second         |
| raw                            |
| long                           |

## 2. 内置函数类型 {#built-in-functions}

|                   |
|-------------------|
| sysdate           |
| systimestamp      |
| add_months        |
| last_day          |
| next_day          |
| months_between    |
| current_date      |
| current_timestamp |
| new_time          |
| tz_offset         |
| trunc             |
| instr             |
| instrb            |
| substr            |
| substrb           |
| trim              |
| ltrim             |
| rtrim             |
| length            |
| lengthb           |
| rawtohex          |
| replace           |
| regexp_replace    |
| regexp_substr     |
| regexp_instr      |
| regexp_like       |
| to_number         |
| to_char           |
| to_date           |
| to_timestamp      |
| to_timestamp_tz   |
| to_yminterval     |
| to_dsinterval     |
| numtodsinterval   |
| numtoyminterval   |
| localtimestamp    |
| from_tz           |
| sys_extract_utc   |
| sessiontimezone   |
| hextoraw          |
| uid               |
| USERENV           |
| asciistr          |
| to_multi_byte     |
| to_single_byte    |
| compose           |
| decompose         |
| sys_context       |

## 3. 内置函数说明 {#built-in-function-descriptions}

### 3.1. `sysdate` 函数 {#sysdate-function}

功能：查看对应的日期与时间，测试用例如下： 查询当前系统的日期：

```
select sysdate() from dual;
  sysdate
------------
 2023-07-06
(1 row)
```

查询往前推1天的日期：

```
select sysdate()-1 from dual;
  ?column?
------------
 2023-07-05
(1 row)
```

### 3.2. `systimestamp` 函数 {#systimestamp-function}

功能：返回本机数据库上当前系统日期和时间（包括微秒和时区），测试用例如下： 查询当前日期的日期和时间：

```
select systimestamp() from dual;
  systimestamp
-----------------------------------
 2023-07-06 10:18:31.674322 +08:00
(1 row)
```

### 3.3. `add_months` 函数 {#add_months-function}

功能：函数将一个月数(n)添加一个日期，并返回相隔n月的同一天，支持参数：date, number；测试用例如下： 查询当前日期（七月六日）的下个月的同一天：

```
select add_months(sysdate(),1) from dual;
 add_months
------------
 2023-08-06
(1 row)
```

查询当前日期的上个月的同一天：

```
select add_months(sysdate(),-1) from dual;
 add_months
------------
 2023-06-06
(1 row)
```

### 3.4. `last_day` 函数 {#last_day-function}

功能：返回指定日期所在月份的最后一天，支持参数：date,测试用例如下： 查询当天所在月份的最后一天：

```
select last_day(sysdate())from dual;
  last_day
------------
 2023-07-31
(1 row)
```

查询某一天所在月份的最后一天：

```
select last_day(to_date('2019-09-01'))from dual;
  last_day
------------
 2019-09-30
(1 row)
```

### 3.5. `next_day` 函数 {#next_day-function}

功能：返回指定日期的下一个日期。支持参数:date, integer /date ,text, 说明：当函数中第二个参数传的星期数比现有星期数小时，会返回下一个星期的日期；当函数中第二个参数所传的日期比现有星期数大，会返回本周相应星期日期。测试用例如下： 查询当前日期的下一天：

```
select next_day(sysdate(),1) from dual;
 next_day
------------
 2023-07-07
(1 row)
```

查询当前日期的下个星期五：

```
select next_day(sysdate(),'FRIDAY') from dual;
  next_day
------------
 2023-07-07
(1 row)
```

### 3.6. `months_between` 函数 {#months_between-function}

功能：返回日期类型的date1和date2之间相差的月份，支持参数：date,date，说明：如果date1晚于date2，返回正数；如果date1早于date2返回负数；如果date1和date2是某月里的同一天，返回结果为整数；如果不是同一天，会在每月31天的基础上返回带有小数部分的结果。测试用例如下： 查询不同月份同一天之间相差的月份：

```
select months_between(to_date('2023-07-06'),to_date('2023-08-06')) from dual;
 months_between
----------------
             -1
(1 row)
```

查询不同月份不同日期之间相差的月份：

```
select months_between(to_date('2023-07-06'),to_date('2023-08-05')) from dual;
   months_between
--------------------
 -0.967741935483871
(1 row)
```

### 3.7. `current_date` 函数 {#current_date-function}

功能：返回当前时区的当前日期，测试用例如下： 查询当前时区的当前日期：

```
select current_date from dual;
 current_date
--------------
 2023-07-06
(1 row)
```

### 3.8. `current_timestamp` 函数 {#current_timestamp-function}

功能：返回当前时区的当前日期与当前时间，包含当前时区信息。支持参数：integer, 说明：返回的时间可调整精度。测试用例如下： 查询当前时区的当前日期与时间：

```
select current_timestamp from dual;
      current_timestamp
-----------------------------------
 2023-07-06 10:27:01.440600 +08:00
(1 row)
```

查询当前时区的当前日期与时间(精度调整为前三位小数)：

```
select current_timestamp(3) from dual;
      current_timestamp
-----------------------------------
 2023-07-06 10:27:14.182000 +08:00
(1 row)
```

### 3.9. `new_time` 函数 {#new_time-function}

功能：返回某个时间在某时区所对应的在另一个时区的日期，支持参数：date, text, text ,测试用例如下： 返回当前日期在另一个时区对应的日期：

```
select sysdate() bj_time,new_time(sysdate(),'PDT','GMT')los_angles from dual;
  bj_time   | los_angles
------------+------------
 2023-07-06 | 2023-07-06
(1 row)
```

### 3.10. `tz_offset` 函数 {#tz_offset-function}

功能：返回给定时区与标准时区的偏移量，支持参数：text,测试用例如下： 返回给定时区与标准时区偏移量：

```
select tz_offset('US/Eastern') from dual;
 tz_offset
-----------
 -04:00
(1 row)
```

### 3.11. `trunc` 函数 {#trunc-function}

功能：可以截取日期，得到想要的数值，如年，月，日，时，分，支持参数：date/date,text,测试用例如下： 截取当前日期：

```
select trunc(sysdate()) from dual;
 trunc
------------
 2023-07-06
(1 row)
```

截取年，返回值只有年是正确的，月和日不是准确值：

```
select trunc(sysdate(),'yyyy') from dual;
   trunc
------------
 2023-01-01
(1 row)
```

截取月，返回值只有月是正确的，年和日不是准确值：

```
select trunc(sysdate(),'mm') from dual;
   trunc
------------
 2023-07-01
(1 row)
```

### 3.12. `instr` 函数 {#instr-function}

功能：字符串查找函数，用于判断源字符串中是否包含目标字符串，并返回匹配位置。支持参数形式如下：

- `instr(string, str)`

- `instr(string, str, start_position, nth_appearance)`

以下为测试用例：

默认情况下返回第一次匹配的位置：

```
SELECT INSTR('database administration', 'data') FROM DUAL;
 instr
-------
     1
(1 row)
```

指定起始位置和匹配序号：

```
SELECT INSTR('database administration', 'i', 1, 2) FROM DUAL;
 instr
-------
    15
(1 row)
```

支持从尾部开始的反向搜索：

```
SELECT INSTR('mississippi river', 's', -5, 2) FROM DUAL;
 instr
-------
     6
(1 row)
```

当未匹配到目标字符串时返回0：

```
SELECT INSTR('database administration', 'z') FROM DUAL;
 instr
-------
     0
(1 row)
```

`instr` 还能像 `like` 一样用于模糊查询：

```
select * from tableName where instr(name,'helloworld')>0;
```

函数实现说明：

- 查找一个字符串在另一个字符串中的位置，采用经典的暴力匹配算法。

- 复用了 `text_instring` 函数。

- 通过 `isByte` 参数判断当前数据库编码是否为多字节，并区分单字节与多字节处理逻辑。

- 根据 `position` 的正负确定正向或反向搜索，并设置循环的起止位置和步长。

- 在循环中逐字节移动并比较，与模式字符串匹配成功即返回相应位置。

### 3.13. `instrb` 函数 {#instrb-function}

功能：字符串查找函数，返回字符串的位置，支持参数： varchar2, text, number DEFAULT 1, number DEFAULT 1,以下为测试用例： 返回CORPORATE FLOOR中默认第一次出现OR时字符串的位置：

```
SELECT INSTRB('CORPORATE FLOOR','OR') "Instring in bytes" FROM DUAL;
 Instring in bytes
-------------------
                 2
(1 row)
```

返回corporate floor中从第五个字符开始查询，第二次出现or时字符串的位置：

```
SELECT INSTRB('CORPORATE FLOOR','OR',5,2) "Instring in bytes" FROM DUAL;
 Instring in bytes
-------------------
                14
(1 row)
```

### 3.14. `substr` 函数 {#substr-function}

功能：截取字符串函数，以字符为单位截取，支持参数：text, integer, 测试用例如下： 截取’今天天气很好’中从第五个字符开始，往后的字符串：

```
SELECT SUBSTR('今天天气很好',5) "Substring with bytes" FROM DUAL;

 Substring with bytes
----------------------
 很好
(1 row)
```

### 3.15. `substrb` 函数 {#substrb-function}

功能：截取字符串函数，以字节为单位截取，支持参数：varchar2, number/varchar2, number，number,测试用例如下： 截取’今天天气很好’中从第五个字节开始，往后的字符串：

```
SELECT SUBSTRB('今天天气很好',5) "Substring with bytes" FROM DUAL;
 Substring with bytes
----------------------
 天气很好
(1 row)
```

截取’今天天气很好’中从第五个字节开始，第八个字节结束的字符串：

```
SELECT SUBSTRB('今天天气很好',5，8) "Substring with bytes" FROM DUAL;
 Substring with bytes
----------------------
   天气
(1 row)
```

### 3.16. `trim` 函数 {#trim-function}

功能：去除指定字符串的左右空格或对应数据，支持参数：varchar2 /varchar2，varchar2，测试用例如下： 去除' aaa bbb ccc '的左右空格：

```
select trim('   aaa bbb ccc   ')trim from dual;
  trim
-------------
 aaa bbb ccc
(1 row)
```

去除’aaa bbb ccc’中的aaa：

```
select trim('aaa bbb ccc','aaa')trim from dual;
  trim
----------
  bbb ccc
(1 row)
```

### 3.17. `ltrim` 函数 {#ltrim-function}

功能：去除指定字符串的左侧空格或对应数据，支持参数：varchar2 /varchar2,varchar2,测试用例如下： 去除' abcdefg '的左侧空格：

```
select ltrim('   abcdefg   ')ltrim from dual;
    ltrim
------------
 abcdefg
(1 row)
```

从’abcdefg’左侧开始遍历，一旦存在某字符出现在’fegab’中就去除，不存在则返回结果：

```
select ltrim('abcdefg','fegab')ltrim from dual;
 ltrim
-------
 cdefg
(1 row)
```

### 3.18. `rtrim` 函数 {#rtrim-function}

功能：去除指定字符串的右侧空格，测试用例如下： 去除' abcdefg '的右侧空格：

```
select rtrim('   abcdefg   ')rtrim from dual;
     rtrim
----------------
    abcdefg
(1 row)
```

从’abcdefg’右侧开始遍历，一旦存在某字符出现在’fegab’中就去除，不存在则返回结果：

```
select rtrim('abcdefg','fegab')rtrim from dual;
 rtrim
-------
 abcd
(1 row)
```

### 3.19. `length` 函数 {#length-function}

功能：求取指定字符串字符的长度，支持参数：char/integer/varchar2测试用例如下： 查询223的字符长度：

```
select length(223) from dual;
 length
--------
      3
(1 row)
```

查询'223’的字符长度：

```
select length('223') from dual;
 length
--------
      3
(1 row)
```

查询’ivorysql数据库’的字符长度：

```
select length('ivorysql数据库') from dual;
 length
--------
     11
(1 row)
```

### 3.20. `lengthb` 函数 {#lengthb-function}

功能：求取指定字符串字节的长度，支持参数：char/bytea/varchar2测试用例如下： 查询’ivorysql’的字节长度:

```
select lengthb('ivorysq'::char) from dual;
 lengthb
---------
       1
(1 row)
```

查询'0x2C’的字节长度:

```
select lengthb('0x2C'::bytea) from dual;
 lengthb
---------
       4
(1 row)
```

查询’ivorysql数据库’的字节长度：

```
select lengthb('ivorysql数据库'::varchar2) from dual;
 lengthb
---------
      17
(1 row)
```

### 3.21. `replace` 函数 {#replace-function}

功能：替换指定字符串中的字符或删除字符，支持参数：text, text, text/varchar2, varchar2, varchar2 DEFAULT NULL::varchar2, 测试用例如下： 替换’jack and jue’中的’j’为’bl'：

```
select replace('jack and jue','j','bl') from dual;
    replace
----------------
 black and blue
(1 row)
```

删除’jack and jue’中的’j':

```
select replace('jack and jue','j') from dual;
  replace
------------
 ack and ue
(1 row)
```

### 3.22. `regexp_replace` 函数 {#regexp_replace-function}

此函数为\`replace\` 函数的扩展。功能：用于通过正则表达式来进行匹配替换。支持参数：text, text, text /text, text, text, integer/varchar2, varchar2/varchar2, varchar2 varchar2, 测试用例如下： 将匹配到的数字替换为\*#：

```
select regexp_replace('01234abcd56789','[0-9]','*#')from  dual;
      regexp_replace
--------------------------
 *#*#*#*#*#abcd*#*#*#*#*#
(1 row)
```

从第二个数开始将匹配到的数字替换为\*#：

```
select regexp_replace('01234abcd56789','[0-9]','*#',2)from  dual;
    regexp_replace
-------------------------
 0*#*#*#*#abcd*#*#*#*#*#
```

删除'01234abcd56789’中的'01'：

```
select regexp_replace('01234abcd56789','01')from dual;
 regexp_replace
----------------
 234abcd56789
(1 row)
```

用’xxx’替换01234abcd56789’中的012：

```
select regexp_replace('01234abcd56789','012','xxx')from dual;
 regexp_replace
----------------
 xxx34abcd56789
(1 row)
```

### 3.23. `regexp_substr` 函数 {#regexp_substr-function}

功能：拾取符合正则表达式描述的字符子串，支持参数：text, text,integer /text, text, integer, integer/ text, text, integer, integer, text /varchar2 ,varchar2,测试用例如下： 查询'012ab34’中从第一个数开始的012字串：

```
select regexp_substr('012ab34', '012',1) from dual;
 regexp_substr
---------------
 012
(1 row)
```

查询'012ab34’中从第一个数第一组开始的012字串：

```
select regexp_substr('012ab34', '012',1,1) from  dual;
 regexp_substr
---------------
 012
(1 row)
```

查询'012a012Ab34’中从第一个数第一组开始不区分大小写的012字串：

```
select regexp_substr('012a012Ab34', '012A',1,1,'i') from dual;
 regexp_substr
---------------
 012a
(1 row)
```

查询'012a012Ab34’中从第一个数第一组开始区分大小写的012字串：

```
select regexp_substr('012a012Ab34', '012A',1,1,'c') from dual;
 regexp_substr
---------------
 012A
(1 row)
```

查询’数据库’中 '数据’子串：

```
select regexp_substr('数据库', '数据') from dual;
 regexp_substr
---------------
 数据
(1 row)
```

### 3.24. `regexp_instr` 函数 {#regexp_instr-function}

功能：用于标定符合正则表达式的字符子串的开始位置，支持参数：text, text,integer /text, text, integer, integer/ text, text, integer, integer, text/text, text, integer, integer, text, integer/ varchar2, varchar2,测试用例如下： 查询’abcaBcabc’中从第一个字符开始，出现abc子串的位置：

```
SELECT regexp_instr('abcaBcabc', 'abc', 1);
 regexp_instr
--------------
 1
(1 row)
```

查询’abcaBcabc’中从第一个字符开始，第三次出现abc子串的位置：

```
SELECT regexp_instr('abcaBcabc', 'abc', 1, 3);
 regexp_instr
--------------
 7
(1 row)
```

查询’abcabcabc’中从第一个字符开始，第二次出现abc子串后发生的位置：

```
SELECT regexp_instr('abcaBcabc', 'abc', 1, 2,1);
 regexp_instr
--------------
 7
(1 row)
```

查询’abcaBcabc’中从第一个字符开始，第一次出现abc子串后发生的位置（区分大小写）：

```
SELECT regexp_instr('abcaBcabc', 'abc',1,2,1,'c');
 regexp_instr
--------------
 7
(1 row)
```

查询’数据库’中’库’出现的位置：

```
SELECT regexp_instr('数据库', '库');
 regexp_instr
--------------
            3
(1 row)
```

### 3.25. `regexp_like` 函数 {#regexp_like-function}

功能：与like类似，用于模糊查询。支持参数：varchar2, varchar2 /varchar2, varchar2 varchar2, 首先创建一个regexp_like表用于测试用例查询：

```
create table t_regexp_like
(
  id varchar(4),
  value varchar(10)

);
insert into t_regexp_like values ('1','1234560');
insert into t_regexp_like values ('2','1234560');
insert into t_regexp_like values ('3','1b3b560');
insert into t_regexp_like values ('4','abc');
insert into t_regexp_like values ('5','abcde');
insert into t_regexp_like values ('6','ADREasx');
insert into t_regexp_like values ('7','123  45');
insert into t_regexp_like values ('8','adc  de');
insert into t_regexp_like values ('9','adc,.de');
insert into t_regexp_like values ('10','abcbvbnb');
insert into t_regexp_like values ('11','11114560');
```

测试用例如下： 查询t_regexp_like表中带有abc的列：

```
select * from t_regexp_like where regexp_like(value,'abc');
 id |  value
----+----------
 4  | abc
 5  | abcde
 10 | abcbvbnb
(3 rows)
```

查询t_regexp_like表中带有ABC的列(不区分大小写)：

```
select * from t_regexp_like where regexp_like(value,'ABC','i');
 id |  value
----+----------
 4  | abc
 5  | abcde
 10 | abcbvbnb
(3 rows)
```

### 3.26. `to_number` 函数 {#to_number-function}

功能：是将一些处理过的按一定格式编排过的字符串变回数值型的格式，支持参数：text/text,text测试用例如下： 将字符串'-34,338,492’转换为数值型格式：

```
SELECT to_number('34,338,492', '99,999,999') from dual;
 to_number
-----------
 -34338492
(1 row)
```

将字符串'5.01-'转换为数值型格式：

```
SELECT to_number('5.01-', '9.99S');

 to_number
-----------
 -5.01
(1 row)
```

### 3.27. `to_char` 函数 {#to_char-function}

功能：将数字或日期转换为字符类型，支持参数：date/date,text/timestamp/timestamp,text测试用例如下： 将当前系统日期转换为字符格式：

```
select to_char(sysdate()) from dual;
  to_char
------------
 2023-07-10
(1 row)
```

将当前系统日期转换为月份/日期/年字符格式：

```
select to_char(sysdate(),'mm/dd/yyyy') from dual;
  to_char
------------
 07/10/2023
(1 row)
```

将当前日期的timestamp格式转换为字符格式：

```
SELECT to_char(sysdate()::timestamp);
         to_char
----------------------------
 2023-07-10 09:46:44.000000
```

将当前日期的timestamp格式转换为月份/日期/年字符格式：

```
SELECT to_char(sysdate()::timestamp,'MM-YYYY-DD');
  to_char
------------
 07-2023-10
(1 row)
```

### 3.28. `to_date` 函数 {#to_date-function}

功能：将字符类型转换为日期类型，支持参数：text/text,text测试用例如下： 将'2023/07/06’转换为日期类型：

```
select to_date('20230706') from dual;
  to_date
------------
 2023-07-06
(1 row)
```

将'-44-02-01’转换为日期类型：

```
SELECT to_date('-44,0201','YYYY-MM-DD');
 to_date
------------
 0044-02-01
(1 row)
```

### 3.29. `to_timestamp` 函数 {#to_timestamp-function}

功能：可以存储年、月、日、小时、分钟、秒，同时还可以存储秒的小数部分。支持参数：text/text,text测试用例如下： 查询'2018-11-02 12:34:56.025’以日期形式输出：

```
SELECT to_timestamp('20181102.12.34.56.025');
        to_timestamp
----------------------------
 2018-11-02 12:34:56.025000
(1 row)
```

查询’2011,12,18 11:38’以日期形式输出：

```
SELECT to_timestamp('2011,12,18 11:38 ', 'YYYY-MM-DD HH24:MI:SS');
       to_timestamp
----------------------------
 2011-12-18 11:38:00.000000
(1 row)
```

### 3.30. `to_timestamp_tz` 函数 {#to_timestamp_tz-function}

功能：根据时间查询，时间字符串有T,Z并有毫秒，时区。测试用例如下： 查询'2016-10-9 14:10:10.123000’以日期形式输出：

```
 SELECT to_timestamp_tz('2016-10-9 14:10:10.123000') FROM DUAL;
          to_timestamp_tz
-----------------------------------
 2016-10-09 14:10:10.123000 +08:00
(1 row)
```

查询'10-9-2016 14:10:10.123000 +8:30’以日期形式输出：

```
 SELECT to_timestamp_tz('10-9-2016 14:10:10.123000 +8:30', 'DD-MM-YYYY HH24:MI:SS.FF TZH:TZM') FROM DUAL;
          to_timestamp_tz
-----------------------------------
 2016-09-10 13:40:10.123000 +08:00
(1 row)
```

### 3.31. `to_yminterval` 函数 {#to_yminterval-function}

功能：将一个字符串类型转化为年和月的时间差类型，支持参数:text, 测试用例如下： 查询'20110101’以后两个年零八个月后的日期：

```
select to_date('20110101','yyyymmdd')+to_yminterval('02-08') from dual;
  ?column?
------------
 2013-09-01
(1 row)
```

### 3.32. `to_dsinterval` 函数 {#to_dsinterval-function}

功能：将一个日期加上一定的小时或者天数变成另外一个日期,支持参数:text,测试用例如下： 查询当前系统时间加上9个半小时后的日期（当前为2023-07-06，18：00）：

```
select sysdate()+to_dsinterval('0 09:30:00')as newdate from dual;
 newdate
------------
 2023-07-07
(1 row)
```

### 3.33. `numtodsinterval` 函数 {#numtodsinterval-function}

功能：将数字转换成时间间隔类型的数据。支持参数:double precision, text测试用例如下： 转换100.00个小时为时间间隔类型数据：

```
SELECT NUMTODSINTERVAL(100.00, 'hour');
        numtodsinterval
-------------------------------
 +000000004 04:00:00.000000000
(1 row)
```

转换100分钟为时间间隔类型数据：

```
SELECT NUMTODSINTERVAL(100, 'minute');
      numtodsinterval
-------------------------------
 +000000000 01:40:00.000000000
(1 row)
```

### 3.34. `numtoyminterval` 函数 {#numtoyminterval-function}

功能：将数字转换成日期间隔类型的数据。 支持参数：double precision,text,测试用例如下： 转换1.00，year为日期间隔：

```
SELECT NUMTOYMINTERVAL(1.00,'year');
 numtoyminterval
-----------------
 +000000001-00
(1 row)
```

转换1，mouth为日期间隔：

```
SELECT NUMTOYMINTERVAL(1,'month');
 numtoyminterval
-----------------
 +000000000-01
(1 row)
```

### 3.35. `localtimestamp` 函数 {#localtimestamp-function}

功能：返回会话中的日期和时间，支持参数：integer, 函数中增加参数为精度，测试用例如下： 返回当前会话中的日期和时间：

```
select localtimestamp from dual;
       localtimestamp
----------------------------
 2023-07-07 09:18:15.896472
(1 row)
```

返回当前会话中的日期和时间（精度为1）：

```
select localtimestamp(1) from dual;
     localtimestamp
----------------------------
 2023-07-07 09:18:16.100000
(1 row)
```

### 3.36. `from_tz` 函数 {#from_tz-function}

功能：将时间从一个时区转换为另一个时区，支持参数;timestamp, text ,测试用例如下： 将'2000-03-28 08:00:00', '3:00’转换为当前时区：

```
SELECT FROM_TZ(TIMESTAMP '2000-03-28 08:00:00', '3:00') FROM DUAL;
              from_tz
-----------------------------------
 2000-03-28 13:00:00.000000 +08:00
(1 row)
```

### 3.37. `sys_extract_utc` 函数 {#sys_extract_utc-function}

功能：将一个timestamptz转换为UTC时区时间。支持参数:timestamp with time zone 测试用例如下： 查询转换timestamp '2000-03-28 11:30:00.00 -8:00’为UTC时区后的时间：

```
select sys_extract_utc(timestamp '2000-03-28 11:30:00.00 -8:00') from dual;
      sys_extract_utc
----------------------------
 2000-03-28 19:30:00.000000
(1 row)
```

### 3.38. `sessiontimezone` 函数 {#sessiontimezone-function}

功能：查看时区详细信息，测试用例如下： 查看当前时区的详细信息：

```
select sessiontimezone() from dual;
 sessiontimezone
-----------------
 Asia/Shanghai
(1 row)
```

修改timezone后，查看时区详细信息：

```
set timezone = 'Asia/Hong_Kong';
SET
select sessiontimezone() from dual;
 sessiontimezone
-----------------
 Asia/Hong_Kong
(1 row)
```

### 3.39. `hextoraw` 函数 {#hextoraw-function}

功能：将字符串表示的二进制数值转换为一个raw数值。支持参数：text,测试用例如下： 将字符串’abcdef’转换为raw数值：

```
select hextoraw('abcdef')from dual;
 hextoraw
----------
 \xabcdef
(1 row)
```

### 3.40. `uid` 函数 {#uid-function}

功能：获取数据库的实例名。测试用例如下： 获取当前数据库的实例名：

```
select uid() from dual;
 uid
-----
  10
(1 row)
```

### 3.41. `USERENV` 函数 {#userenv-function}

功能：返回当前用户环境的信息，测试用例如下： 查看当前用户是否是dba，如果是返回true：

```
select userenv('isdba')from dual;
 get_isdba
-----------
 TRUE
(1 row)
```

查看会话标志：

```
select userenv('sessionid')from dual;
 get_sessionid
---------------
 1
(1 row)
```

### 3.42. `ASCIISTR` 函数 {#asciistr-function}

功能：传入字符串，返回对应的ASCII字符，测试用例如下： 只有ASCII字符：

```
 select asciistr('Hello, World!') from dual;
   asciistr
---------------
 Hello, World!
(1 row)
```

非ASCII字符：

```
 select asciistr('你好') from dual;
  asciistr
------------
 \4F60\597D
```

同时包含ASCII字符和非ASCII字符：

```
 select asciistr('ABÄCDE') from dual;
  asciistr
------------
 AB\00C4CDE
(1 row)
```

### 3.43. `TO_MULTI_BYTE` 函数 {#to_multi_byte-function}

功能：将字符串中的半角字符转换为全角字符： 输入半角字符，转换为全角字符：

```
select to_multi_byte('1.2'::text) ;
 to_multi_byte
---------------
 １．２
```

### 3.44. `TO_SINGLE_BYTE` 函数 {#to_single_byte-function}

功能：将字符串中的半角字符转换为全角字符 输入全角字符，转换为半角字符：

```
select to_single_byte('１．２');
 to_single_byte
----------------
 1.2
```

### 3.45. `COMPOSE` 函数 {#compose-function}

功能：将基本字符和组合标记组合一个复合Unicode字符: 输入基本字符a和组合标记768, 返回法语à

```
select compose('a'||chr(768)) from dual;
 compose
---------
 à
(1 row)
```

### 3.46. `DECOMPOSE` 函数 {#decompose-function}

功能：将复合Unicode字符（如带有重音或特殊符号的字符）分解为其基本字符和组合标记 输入法语é,返回基本字符e和组合标记301：

```
select asciistr(decompose('é')) from dual;
 asciistr
----------
 e\0301
```

### 3.47. `SYS_CONTEXT` 函数 {#sys_context-function}

功能：返回当前时刻与给定上下文关联的参数的值，可以在SQL和PLSQL语言中使用。

```
ivorysql=# select sys_context('USERENV','DB_NAME');
 sys_context
-------------
 ivorysql
(1 row)
```
