---
title: All functions
linkTitle: All functions
description: This page lists every function documented in this reference, 126 entries in all, in one alphabetical
  table.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/all-functions.html
upstream_source: agensgraph
upstream_modified: true
---


This page lists every function documented in this reference, 126 entries in all, in one
alphabetical table. A function can be found by name without knowing which category it
belongs to. The **Function** column links to the full entry, which carries the
considerations and a worked example. The **Signature** column shows every overload the
catalog holds.

Where two entries share a name, they are two functions with two OIDs and two meanings.
`length` over a string is not `length` over a path, and the signature column tells them
apart.

| Function | Signature | Description | Availability |
| --- | --- | --- | --- |
| [`abs`](/agensgraph/reference/functions/numeric/#abs) | <code>abs ( x jsonb ) -&gt; jsonb</code><br><code>abs ( x numeric ) -&gt; numeric</code> | Returns the absolute value of a number. | 2.17 and earlier |
| [`acos`](/agensgraph/reference/functions/numeric/#acos) | <code>acos ( x jsonb ) -&gt; jsonb</code><br><code>acos ( x double precision ) -&gt; double precision</code> | Returns the arc cosine of `x`, in radians. | 2.17 and earlier |
| [`ag_get_graphconstraintdef`](/agensgraph/reference/functions/scalar/#ag_get_graphconstraintdef) | <code>ag_get_graphconstraintdef ( constraint oid ) -&gt; text</code> | Reconstructs the `CREATE CONSTRAINT` command for a graph constraint, given its OID. | 2.17 and earlier |
| [`ag_get_propindexdef`](/agensgraph/reference/functions/scalar/#ag_get_propindexdef) | <code>ag_get_propindexdef ( index oid ) -&gt; text</code> | Reconstructs the `CREATE PROPERTY INDEX` command for a property index, given its OID. | 2.17 and earlier |
| [`ag_property_text`](/agensgraph/reference/functions/jsonb/#ag_property_text) | <code>ag_property_text ( properties jsonb, key text, expected_kind "char" ) -&gt; text</code> | Returns a property's value as `text`, but only when the stored value is of the JSON kind asked for. | Added in 2.18 |
| [`agversion`](/agensgraph/reference/functions/scalar/#agversion) | <code>agversion ( ) -&gt; text</code> | The AgensGraph version of the running server. | 2.17 and earlier |
| [`all`](/agensgraph/reference/functions/predicate/#all) | <code>all ( variable IN list WHERE predicate ) -&gt; boolean</code> | Returns true when the predicate holds for every element of the list. | 2.17 and earlier |
| [`allshortestpaths`](/agensgraph/reference/functions/path/#allshortestpaths) | <code>allshortestpaths ( pattern ) -&gt; graphpath</code> | Every shortest path between two vertices. | 2.17 and earlier |
| [`any`](/agensgraph/reference/functions/predicate/#any) | <code>any ( variable IN list WHERE predicate ) -&gt; boolean</code> | Returns true when the predicate holds for at least one element of the list. | 2.17 and earlier |
| [`array_size`](/agensgraph/reference/functions/list/#array_size) | <code>array_size ( list jsonb ) -&gt; integer</code><br><code>array_size ( list json ) -&gt; integer</code><br><code>array_size ( list anyarray ) -&gt; integer</code> | Returns the number of elements in an array. | 2.17 and earlier |
| [`asin`](/agensgraph/reference/functions/numeric/#asin) | <code>asin ( x jsonb ) -&gt; jsonb</code><br><code>asin ( x double precision ) -&gt; double precision</code> | Returns the arc sine of `x`, in radians. | 2.17 and earlier |
| [`atan`](/agensgraph/reference/functions/numeric/#atan) | <code>atan ( x jsonb ) -&gt; jsonb</code><br><code>atan ( x double precision ) -&gt; double precision</code> | Returns the arc tangent of `x`, in radians. | 2.17 and earlier |
| [`atan2`](/agensgraph/reference/functions/numeric/#atan2) | <code>atan2 ( y jsonb, x jsonb ) -&gt; jsonb</code><br><code>atan2 ( y double precision, x double precision ) -&gt; double precision</code> | Arc tangent of `y / x` in radians, using both signs to fix the quadrant. | 2.17 and earlier |
| [`avg`](/agensgraph/reference/functions/aggregate/#avg) | <code>avg ( expression numeric ) -&gt; numeric</code> | Returns the arithmetic mean of the non-null values in the group. | 2.17 and earlier |
| [`cardinality`](/agensgraph/reference/functions/list/#cardinality) | <code>cardinality ( value jsonb ) -&gt; jsonb</code><br><code>cardinality ( p graphpath ) -&gt; jsonb</code> | Returns the number of elements in a list, entries in a map, or vertices and edges in a path. | Added in 2.18 |
| [`ceil`](/agensgraph/reference/functions/numeric/#ceil) | <code>ceil ( x jsonb ) -&gt; jsonb</code><br><code>ceil ( x numeric ) -&gt; numeric</code> | Returns the smallest integer that is not less than `x`. | 2.17 and earlier |
| [`coalesce`](/agensgraph/reference/functions/scalar/#coalesce) | <code>coalesce ( value [, value ] ... ) -&gt; jsonb</code> | Returns the first argument that is not null. | 2.17 and earlier |
| [`collect`](/agensgraph/reference/functions/aggregate/#collect) | <code>collect ( expression anyelement ) -&gt; jsonb</code><br><code>collect ( v vertex ) -&gt; vertex[]</code><br><code>collect ( e edge ) -&gt; edge[]</code><br><code>collect ( p graphpath ) -&gt; graphpath[]</code> | Gathers the group's values into a list; a graph element gives a native array. | 2.17 and earlier |
| [`cos`](/agensgraph/reference/functions/numeric/#cos) | <code>cos ( x jsonb ) -&gt; jsonb</code><br><code>cos ( x double precision ) -&gt; double precision</code> | Returns the cosine of an angle given in radians. | 2.17 and earlier |
| [`cosd`](/agensgraph/reference/functions/numeric/#cosd) | <code>cosd ( x double precision ) -&gt; double precision</code> | Returns the cosine of an angle given in degrees. | 2.17 and earlier |
| [`cot`](/agensgraph/reference/functions/numeric/#cot) | <code>cot ( x jsonb ) -&gt; jsonb</code><br><code>cot ( x double precision ) -&gt; double precision</code> | Returns the cotangent of an angle given in radians — the reciprocal of the tangent. | 2.17 and earlier |
| [`count`](/agensgraph/reference/functions/aggregate/#count) | <code>count ( * ) -&gt; bigint</code><br><code>count ( expression ) -&gt; bigint</code> | Counts rows in the group. | 2.17 and earlier |
| [`cypher_to_jsonb`](/agensgraph/reference/functions/jsonb/#cypher_to_jsonb) | <code>cypher_to_jsonb ( value anyelement ) -&gt; jsonb</code> | Boxes a value to `jsonb` using Cypher's rules; refuses a graph type. | 2.17 and earlier |
| [`datetime`](/agensgraph/reference/functions/scalar/#datetime) | <code>datetime ( ) -&gt; timestamp with time zone</code><br><code>datetime ( timezone "any" ) -&gt; timestamp without time zone</code><br><code>datetime ( year integer, month integer, mday integer, hour integer, min integer, sec integer, millisec integer, nanosec integer, timezone "any" ) -&gt; timestamp without time zone</code> | The current transaction timestamp, the time in a named zone, or a timestamp built from parts. | 2.17 and earlier |
| [`degrees`](/agensgraph/reference/functions/numeric/#degrees) | <code>degrees ( x jsonb ) -&gt; jsonb</code><br><code>degrees ( x double precision ) -&gt; double precision</code> | Converts radians to degrees. | 2.17 and earlier |
| [`dijkstra`](/agensgraph/reference/functions/path/#dijkstra) | <code>dijkstra ( pattern, weight ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, condition ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, LIMIT count ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, condition, LIMIT count ) -&gt; graphpath</code> | Finds the cheapest path between two vertices, where each edge costs what `weight` evaluates to. | 2.17 and earlier |
| [`e`](/agensgraph/reference/functions/numeric/#e) | <code>e ( ) -&gt; numeric</code> | Returns Euler's number as a `numeric`. | 2.17 and earlier |
| [`edge_to_jsonb`](/agensgraph/reference/functions/jsonb/#edge_to_jsonb) | <code>edge_to_jsonb ( e edge ) -&gt; jsonb</code> | Returns an edge's property bag. | 2.17 and earlier |
| [`edges`](/agensgraph/reference/functions/path/#edges) | <code>edges ( p graphpath ) -&gt; edge[]</code> | Returns the edges of a path, in order. | 2.17 and earlier |
| [`end_id`](/agensgraph/reference/functions/scalar/#end_id) | <code>end_id ( e edge ) -&gt; graphid</code> | Returns the `graphid` of the vertex an edge points at, without reading that vertex. | 2.17 and earlier |
| [`end_vertex`](/agensgraph/reference/functions/path/#end_vertex) | <code>end_vertex ( e edge ) -&gt; vertex</code> | Returns the vertex an edge points at. | 2.17 and earlier |
| [`endNode`](/agensgraph/reference/functions/scalar/#endnode) | <code>endNode ( e edge ) -&gt; vertex</code> | Returns the vertex an edge points at. | 2.17 and earlier |
| [`exists`](/agensgraph/reference/functions/predicate/#exists) | <code>exists ( pattern ) -&gt; boolean</code><br><code>exists ( property_reference ) -&gt; boolean</code> | True when a pattern matches at least once, or when a property is present and not null. | 2.17 and earlier |
| [`exp`](/agensgraph/reference/functions/numeric/#exp) | <code>exp ( x jsonb ) -&gt; jsonb</code><br><code>exp ( x numeric ) -&gt; numeric</code> | Returns *e* raised to the power `x`. | 2.17 and earlier |
| [`floor`](/agensgraph/reference/functions/numeric/#floor) | <code>floor ( x jsonb ) -&gt; jsonb</code><br><code>floor ( x numeric ) -&gt; numeric</code> | Returns the largest integer that is not greater than `x`. | 2.17 and earlier |
| [`get_last_graph_write_stats`](/agensgraph/reference/functions/scalar/#get_last_graph_write_stats) | <code>get_last_graph_write_stats ( ) -&gt; record</code> | What the most recent graph write in this session changed, as five counters. | 2.17 and earlier |
| [`get_time`](/agensgraph/reference/functions/scalar/#get_time) | <code>get_time ( ) -&gt; time without time zone</code><br><code>get_time ( timezone "any" ) -&gt; time without time zone</code> | Returns the current time of day, either locally or in a named zone. | 2.17 and earlier |
| [`graph_labid`](/agensgraph/reference/functions/scalar/#graph_labid) | <code>graph_labid ( qualified_label cstring ) -&gt; integer</code> | Returns the label id of a label named as `graph.label`. | 2.17 and earlier |
| [`graphid`](/agensgraph/reference/functions/scalar/#graphid) | <code>graphid ( labid integer, locid bigint ) -&gt; graphid</code><br><code>graphid ( id numeric ) -&gt; graphid</code> | Builds a `graphid` from a label id and a local id, or from its printed form. | 2.17 and earlier |
| [`graphid_in_jsonb_array`](/agensgraph/reference/functions/jsonb/#graphid_in_jsonb_array) | <code>graphid_in_jsonb_array ( id graphid, elements jsonb ) -&gt; boolean</code> | Returns true when a `graphid` is one of the graph elements in a `jsonb` array. | 2.17 and earlier |
| [`graphid_labid`](/agensgraph/reference/functions/scalar/#graphid_labid) | <code>graphid_labid ( id graphid ) -&gt; integer</code> | Returns the label part of a `graphid` — the number before the dot. | 2.17 and earlier |
| [`graphid_locid`](/agensgraph/reference/functions/scalar/#graphid_locid) | <code>graphid_locid ( id graphid ) -&gt; bigint</code> | Returns the local part of a `graphid` — the number after the dot, taken from the label's sequence. | 2.17 and earlier |
| [`head`](/agensgraph/reference/functions/list/#head) | <code>head ( list jsonb ) -&gt; jsonb</code><br><code>head ( list anyarray ) -&gt; anyelement</code> | Returns the first element of a list. | 2.17 and earlier |
| [`id`](/agensgraph/reference/functions/scalar/#id) | <code>id ( v vertex ) -&gt; graphid</code><br><code>id ( e edge ) -&gt; graphid</code> | Returns a graph element's identity. | 2.17 and earlier |
| [`isEmpty`](/agensgraph/reference/functions/predicate/#isempty) | <code>isEmpty ( value jsonb ) -&gt; boolean</code> | Returns true when a list has no elements or a map has no keys. | 2.17 and earlier |
| [`jsonb_add`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_add ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick `+` operator: addition, or concatenation of two strings or two lists. | 2.17 and earlier |
| [`jsonb_array_length`](/agensgraph/reference/functions/jsonb/#jsonb_array_length) | <code>jsonb_array_length ( list jsonb ) -&gt; integer</code> | Returns the number of elements in a `jsonb` array, as an `integer`. | 2.17 and earlier |
| [`jsonb_div`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_div ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick `/` operator. Integer division when both operands are integers. | 2.17 and earlier |
| [`jsonb_mod`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_mod ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick `%` operator. | 2.17 and earlier |
| [`jsonb_mul`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_mul ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick `*` operator. | 2.17 and earlier |
| [`jsonb_pow`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_pow ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick `^` operator. | 2.17 and earlier |
| [`jsonb_sub`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_sub ( a jsonb, b jsonb ) -&gt; jsonb</code> | Implements the backtick binary `-` operator. | 2.17 and earlier |
| [`jsonb_uminus`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_uminus ( a jsonb ) -&gt; jsonb</code> | Implements the backtick prefix `-` operator. | 2.17 and earlier |
| [`jsonb_uplus`](/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_uplus ( a jsonb ) -&gt; jsonb</code> | Implements the backtick prefix `+` operator. | 2.17 and earlier |
| [`keys`](/agensgraph/reference/functions/list/#keys) | <code>keys ( map jsonb ) -&gt; jsonb</code> | Returns a list of the key names of a map, or of a graph element's properties. | 2.17 and earlier |
| [`label`](/agensgraph/reference/functions/scalar/#label) | <code>label ( v vertex ) -&gt; jsonb</code><br><code>label ( e edge ) -&gt; jsonb</code> | Returns the name of the label a graph element was created with, as a `jsonb` string. | 2.17 and earlier |
| [`labels`](/agensgraph/reference/functions/scalar/#labels) | <code>labels ( v vertex ) -&gt; jsonb</code> | Returns a list holding the vertex's own label and every label it inherits from, nearest first. | 2.17 and earlier |
| [`last`](/agensgraph/reference/functions/list/#last) | <code>last ( list jsonb ) -&gt; jsonb</code><br><code>last ( list anyarray ) -&gt; anyelement</code> | Returns the final element of a list. | 2.17 and earlier |
| [`left`](/agensgraph/reference/functions/string/#left) | <code>left ( string jsonb, n jsonb ) -&gt; jsonb</code><br><code>left ( string text, n integer ) -&gt; text</code> | Returns the first `n` characters of a string. | 2.17 and earlier |
| [`length`](/agensgraph/reference/functions/path/#length) | <code>length ( p graphpath ) -&gt; jsonb</code><br><code>length ( vs vertex[] ) -&gt; jsonb</code><br><code>length ( es edge[] ) -&gt; jsonb</code><br><code>length ( ps graphpath[] ) -&gt; jsonb</code> | Edges in a path, or elements of an array of graph elements. | 2.17 and earlier |
| [`length`](/agensgraph/reference/functions/scalar/#length) | <code>length ( value jsonb ) -&gt; jsonb</code> | Characters in a string, elements in a list, or keys in a map. | 2.17 and earlier |
| [`ln`](/agensgraph/reference/functions/numeric/#ln) | <code>ln ( x double precision ) -&gt; double precision</code><br><code>ln ( x numeric ) -&gt; numeric</code> | Natural logarithm of `x`. The function `log` resolves to in Cypher. | 2.17 and earlier |
| [`localdatetime`](/agensgraph/reference/functions/scalar/#localdatetime) | <code>localdatetime ( ) -&gt; timestamp with time zone</code><br><code>localdatetime ( timezone "any" ) -&gt; timestamp without time zone</code> | Returns the current transaction timestamp, or the current wall-clock reading in a named zone. | 2.17 and earlier |
| [`log`](/agensgraph/reference/functions/numeric/#log) | <code>log ( x jsonb ) -&gt; jsonb</code> | Natural logarithm of `x` — not base 10, and with no base argument. | 2.17 and earlier |
| [`log10`](/agensgraph/reference/functions/numeric/#log10) | <code>log10 ( x double precision ) -&gt; double precision</code><br><code>log10 ( x numeric ) -&gt; numeric</code> | Returns the base-10 logarithm of `x`. | 2.17 and earlier |
| [`lower`](/agensgraph/reference/functions/string/#lower) | <code>lower ( string text ) -&gt; text</code> | Returns the string in lower case. | 2.17 and earlier |
| [`lTrim`](/agensgraph/reference/functions/string/#ltrim) | <code>lTrim ( string jsonb ) -&gt; jsonb</code> | Removes whitespace from the start of a string. | 2.17 and earlier |
| [`max`](/agensgraph/reference/functions/aggregate/#max) | <code>max ( expression jsonb ) -&gt; jsonb</code><br><code>max ( expression numeric ) -&gt; numeric</code> | Returns the largest value in the group. | 2.17 and earlier |
| [`min`](/agensgraph/reference/functions/aggregate/#min) | <code>min ( expression jsonb ) -&gt; jsonb</code><br><code>min ( expression numeric ) -&gt; numeric</code> | Returns the smallest value in the group. | 2.17 and earlier |
| [`nodes`](/agensgraph/reference/functions/path/#nodes) | <code>nodes ( p graphpath ) -&gt; vertex[]</code> | The vertices of a path, in order. | 2.17 and earlier |
| [`none`](/agensgraph/reference/functions/predicate/#none) | <code>none ( variable IN list WHERE predicate ) -&gt; boolean</code> | Returns true when the predicate holds for no element of the list — the negation of `any`. | 2.17 and earlier |
| [`percentileCont`](/agensgraph/reference/functions/aggregate/#percentilecont) | <code>percentileCont ( list jsonb, percentile numeric ) -&gt; double precision</code> | Percentile of a list of numbers, interpolated between neighbouring values. | 2.17 and earlier |
| [`percentileDisc`](/agensgraph/reference/functions/aggregate/#percentiledisc) | <code>percentileDisc ( list jsonb, percentile numeric ) -&gt; double precision</code> | Percentile of a list of numbers, rounded down to a value in the list. | 2.17 and earlier |
| [`pi`](/agensgraph/reference/functions/numeric/#pi) | <code>pi ( ) -&gt; double precision</code> | Returns π. | 2.17 and earlier |
| [`properties`](/agensgraph/reference/functions/scalar/#properties) | <code>properties ( v vertex ) -&gt; jsonb</code><br><code>properties ( e edge ) -&gt; jsonb</code> | Returns a graph element's whole property bag as a map. | 2.17 and earlier |
| [`radians`](/agensgraph/reference/functions/numeric/#radians) | <code>radians ( x jsonb ) -&gt; jsonb</code><br><code>radians ( x double precision ) -&gt; double precision</code> | Converts degrees to radians. | 2.17 and earlier |
| [`rand`](/agensgraph/reference/functions/numeric/#rand) | <code>rand ( ) -&gt; jsonb</code> | Returns a number in the half-open range 0 to 1. | 2.17 and earlier |
| [`range`](/agensgraph/reference/functions/list/#range) | <code>range ( start integer, stop integer ) -&gt; jsonb</code><br><code>range ( start integer, stop integer, step integer ) -&gt; jsonb</code> | Returns a list of integers from `start` to `stop`, inclusive at both ends. | 2.17 and earlier |
| [`regather_graphmeta`](/agensgraph/reference/functions/scalar/#regather_graphmeta) | <code>regather_graphmeta ( ) -&gt; boolean</code> | Empties `ag_graphmeta` and rebuilds it by scanning every edge label in the current graph. | 2.17 and earlier |
| [`relationships`](/agensgraph/reference/functions/path/#relationships) | <code>relationships ( p graphpath ) -&gt; edge[]</code> | Returns the edges of a path, in order. | 2.17 and earlier |
| [`replace`](/agensgraph/reference/functions/string/#replace) | <code>replace ( string jsonb, old jsonb, new jsonb ) -&gt; jsonb</code> | Replaces every occurrence of one substring with another. | 2.17 and earlier |
| [`reverse`](/agensgraph/reference/functions/string/#reverse) | <code>reverse ( string text ) -&gt; text</code><br><code>reverse ( list jsonb ) -&gt; jsonb</code><br><code>reverse ( list anyarray ) -&gt; anyarray</code> | Reverses a list, or a string given as a literal or cast to `text`. | 2.17 and earlier |
| [`right`](/agensgraph/reference/functions/string/#right) | <code>right ( string jsonb, n jsonb ) -&gt; jsonb</code><br><code>right ( string text, n integer ) -&gt; text</code> | Returns the last `n` characters of a string. | 2.17 and earlier |
| [`round`](/agensgraph/reference/functions/numeric/#round) | <code>round ( x jsonb ) -&gt; jsonb</code><br><code>round ( x numeric [, scale integer ] ) -&gt; numeric</code> | Rounds `x` to the nearest integer, halves away from zero. | 2.17 and earlier |
| [`rTrim`](/agensgraph/reference/functions/string/#rtrim) | <code>rTrim ( string jsonb ) -&gt; jsonb</code> | Removes whitespace from the end of a string. | 2.17 and earlier |
| [`shortestpath`](/agensgraph/reference/functions/path/#shortestpath) | <code>shortestpath ( pattern ) -&gt; graphpath</code> | Finds one shortest path between two vertices, by number of edges. | 2.17 and earlier |
| [`sign`](/agensgraph/reference/functions/numeric/#sign) | <code>sign ( x jsonb ) -&gt; jsonb</code><br><code>sign ( x numeric ) -&gt; numeric</code> | Returns −1, 0 or 1 according to the sign of `x`. | 2.17 and earlier |
| [`sin`](/agensgraph/reference/functions/numeric/#sin) | <code>sin ( x double precision ) -&gt; double precision</code> | Returns the sine of an angle given in radians. | 2.17 and earlier |
| [`sind`](/agensgraph/reference/functions/numeric/#sind) | <code>sind ( x double precision ) -&gt; double precision</code> | Returns the sine of an angle given in degrees. | 2.17 and earlier |
| [`single`](/agensgraph/reference/functions/predicate/#single) | <code>single ( variable IN list WHERE predicate ) -&gt; boolean</code> | Returns true when the predicate holds for exactly one element of the list. | 2.17 and earlier |
| [`size`](/agensgraph/reference/functions/scalar/#size) | <code>size ( value ) -&gt; jsonb</code><br><code>size ( pattern ) -&gt; bigint</code> | The length of a value, or the number of times a pattern matches. | 2.17 and earlier |
| [`split`](/agensgraph/reference/functions/string/#split) | <code>split ( string text, delimiter text ) -&gt; anyarray</code> | Cuts a string into a list at every occurrence of a delimiter. | 2.17 and earlier |
| [`sqrt`](/agensgraph/reference/functions/numeric/#sqrt) | <code>sqrt ( x jsonb ) -&gt; jsonb</code><br><code>sqrt ( x numeric ) -&gt; numeric</code> | Returns the square root of `x`. | 2.17 and earlier |
| [`start_id`](/agensgraph/reference/functions/scalar/#start_id) | <code>start_id ( e edge ) -&gt; graphid</code> | Returns the `graphid` of the vertex an edge leaves, without reading that vertex. | 2.17 and earlier |
| [`start_vertex`](/agensgraph/reference/functions/path/#start_vertex) | <code>start_vertex ( e edge ) -&gt; vertex</code> | Returns the vertex an edge leaves. | 2.17 and earlier |
| [`startNode`](/agensgraph/reference/functions/scalar/#startnode) | <code>startNode ( e edge ) -&gt; vertex</code> | Returns the vertex an edge leaves. | 2.17 and earlier |
| [`stdev`](/agensgraph/reference/functions/aggregate/#stdev) | <code>stdev ( expression numeric ) -&gt; numeric</code> | Sample standard deviation of the values in the group. | 2.17 and earlier |
| [`stdevp`](/agensgraph/reference/functions/aggregate/#stdevp) | <code>stdevp ( expression numeric ) -&gt; numeric</code> | Population standard deviation of the values in the group. | 2.17 and earlier |
| [`str_size`](/agensgraph/reference/functions/string/#str_size) | <code>str_size ( string text ) -&gt; integer</code> | Returns the number of characters in a string, as an `integer`. | 2.17 and earlier |
| [`string_contains`](/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_contains ( a jsonb, b jsonb ) -&gt; boolean</code> | Implements `CONTAINS`. True when the right string occurs anywhere in the left. | 2.17 and earlier |
| [`string_ends_with`](/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_ends_with ( a jsonb, b jsonb ) -&gt; boolean</code> | Implements `ENDS WITH`. True when the left string ends with the right. | 2.17 and earlier |
| [`string_regex`](/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_regex ( a jsonb, b jsonb ) -&gt; boolean</code> | Implements `=~`. True when the left string matches the right as a regular expression. | 2.17 and earlier |
| [`string_starts_with`](/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_starts_with ( a jsonb, b jsonb ) -&gt; boolean</code> | Implements `STARTS WITH`. True when the left string begins with the right. | 2.17 and earlier |
| [`substring`](/agensgraph/reference/functions/string/#substring) | <code>substring ( string jsonb, start jsonb ) -&gt; jsonb</code><br><code>substring ( string jsonb, start jsonb, count jsonb ) -&gt; jsonb</code> | Returns part of a string, starting at `start` and running to the end or for `count` characters. | 2.17 and earlier |
| [`sum`](/agensgraph/reference/functions/aggregate/#sum) | <code>sum ( expression numeric ) -&gt; numeric</code> | Returns the total of the non-null values in the group. | 2.17 and earlier |
| [`tail`](/agensgraph/reference/functions/list/#tail) | <code>tail ( list jsonb ) -&gt; jsonb</code><br><code>tail ( list anyarray ) -&gt; anyarray</code> | Returns every element of a list except the first. | 2.17 and earlier |
| [`tan`](/agensgraph/reference/functions/numeric/#tan) | <code>tan ( x jsonb ) -&gt; jsonb</code><br><code>tan ( x double precision ) -&gt; double precision</code> | Returns the tangent of an angle given in radians. | 2.17 and earlier |
| [`tand`](/agensgraph/reference/functions/numeric/#tand) | <code>tand ( x double precision ) -&gt; double precision</code> | Returns the tangent of an angle given in degrees. | 2.17 and earlier |
| [`to_jsonb`](/agensgraph/reference/functions/jsonb/#to_jsonb) | <code>to_jsonb ( value anyelement ) -&gt; jsonb</code> | Converts any SQL value to `jsonb`, a composite becoming an object. | 2.17 and earlier |
| [`toBoolean`](/agensgraph/reference/functions/type-conversion/#toboolean) | <code>toBoolean ( value text ) -&gt; boolean</code><br><code>toBoolean ( value "any" ) -&gt; boolean</code> | Returns the boolean a value names, or null when it names none. | 2.17 and earlier |
| [`toBooleanOrNull`](/agensgraph/reference/functions/type-conversion/#tobooleanornull) | <code>toBooleanOrNull ( value text ) -&gt; boolean</code><br><code>toBooleanOrNull ( value "any" ) -&gt; boolean</code> | Returns the boolean a value names, or null. | 2.17 and earlier |
| [`toFloat`](/agensgraph/reference/functions/type-conversion/#tofloat) | <code>toFloat ( value "any" ) -&gt; double precision</code> | Returns the floating-point number a value names, or null. | Added in 2.18 |
| [`toFloatList`](/agensgraph/reference/functions/type-conversion/#tofloatlist) | <code>toFloatList ( list jsonb ) -&gt; jsonb</code><br><code>toFloatList ( list anyarray ) -&gt; double precision[]</code> | Converts every element of a list to a floating-point number. | 2.17 and earlier |
| [`toInteger`](/agensgraph/reference/functions/type-conversion/#tointeger) | <code>toInteger ( value "any" ) -&gt; bigint</code> | Returns the integer a value names, or null. | Added in 2.18 |
| [`toIntegerList`](/agensgraph/reference/functions/type-conversion/#tointegerlist) | <code>toIntegerList ( list jsonb ) -&gt; jsonb</code><br><code>toIntegerList ( list anyarray ) -&gt; bigint[]</code> | Converts every element of a list to an integer. | 2.17 and earlier |
| [`toLower`](/agensgraph/reference/functions/string/#tolower) | <code>toLower ( string jsonb ) -&gt; jsonb</code> | Returns the string in lower case. | 2.17 and earlier |
| [`toString`](/agensgraph/reference/functions/type-conversion/#tostring) | <code>toString ( value jsonb ) -&gt; jsonb</code> | Returns the string form of a value. | 2.17 and earlier |
| [`toStringList`](/agensgraph/reference/functions/type-conversion/#tostringlist) | <code>toStringList ( list jsonb ) -&gt; jsonb</code><br><code>toStringList ( list anyarray ) -&gt; text[]</code> | Converts every element of a list to a string. | 2.17 and earlier |
| [`toStringOrNull`](/agensgraph/reference/functions/type-conversion/#tostringornull) | <code>toStringOrNull ( value "any" ) -&gt; text</code> | Returns the string form of a value, or null when the value has no string form. | 2.17 and earlier |
| [`toUpper`](/agensgraph/reference/functions/string/#toupper) | <code>toUpper ( string jsonb ) -&gt; jsonb</code> | Returns the string in upper case. | 2.17 and earlier |
| [`trim`](/agensgraph/reference/functions/string/#trim) | <code>trim ( string jsonb ) -&gt; jsonb</code> | Removes whitespace from both ends of a string. | 2.17 and earlier |
| [`type`](/agensgraph/reference/functions/scalar/#type) | <code>type ( e edge ) -&gt; jsonb</code> | Returns the name of an edge's label, as a `jsonb` string — the same value as `label(e)`, under the name Cypher uses for relationship types. | 2.17 and earlier |
| [`unnest`](/agensgraph/reference/functions/list/#unnest) | <code>unnest ( from_json jsonb ) -&gt; setof jsonb</code> | Expands a list into one row per element. | Added in 2.18 |
| [`upper`](/agensgraph/reference/functions/string/#upper) | <code>upper ( string text ) -&gt; text</code> | Returns the string in upper case. | 2.17 and earlier |
| [`vertex_to_jsonb`](/agensgraph/reference/functions/jsonb/#vertex_to_jsonb) | <code>vertex_to_jsonb ( v vertex ) -&gt; jsonb</code> | Returns a vertex's property bag. | 2.17 and earlier |
| [`vertices`](/agensgraph/reference/functions/path/#vertices) | <code>vertices ( p graphpath ) -&gt; vertex[]</code> | Returns the vertices of a path, in order. | 2.17 and earlier |

`collect` is older than 2.18, but its native-array results arrived with this release:
`vertex[]`, `edge[]` and `graphpath[]` in place of `jsonb`. So did the three-valued
implementations behind `all`, `any`, `none` and `single`. The
[2.18 release notes](/agensgraph/release-notes/2.18/) carry the full list of changes.

## Functions documented elsewhere {#functions-documented-elsewhere}

The `meta` schema adds functions for inspecting graphs, labels and their sizes from SQL:
`meta.labels()`, `meta.count()`, `meta.label_size()` and the rest. It is an extension rather
than part of the core catalog, so a database has it only once it is installed. Those
functions are documented on their own page,
[Graph metadata](/agensgraph/system-catalogs/graph-metadata/), and are not repeated here.

Every function PostgreSQL itself provides is also reachable from a Cypher query, subject to
the type rules described on each page here. The
[PostgreSQL documentation](https://www.postgresql.org/docs/18/functions.html) is the
reference for those.

## What this reference leaves out {#what-this-reference-leaves-out}

The functions AgensGraph adds occupy the object-identifier range 7000 to 8100. Not all of
them are meant to be called. The range also holds type input and output functions,
comparison and hash support for the B-tree and GIN operator classes, and aggregate
transition and final functions. It holds a planner support function, two `pg_upgrade`
helpers, and four placeholder entries the path-finding executor resolves. This reference
documents the ones a query can use, and omits those.

## List what your own build exposes {#list-what-your-own-build-exposes}

The catalog is the authority on what a given server has. This lists every AgensGraph
function in that range, aggregates included:

```sql
SELECT p.proname AS function,
       pg_catalog.pg_get_function_identity_arguments(p.oid) AS arguments,
       pg_catalog.format_type(p.prorettype, NULL) AS returns,
       CASE p.prokind WHEN 'a' THEN 'aggregate' ELSE 'function' END AS kind,
       obj_description(p.oid, 'pg_proc') AS description
FROM pg_catalog.pg_proc p
WHERE p.oid BETWEEN 7000 AND 8100
ORDER BY p.proname, p.oid;
```

On this 2.18 server that returns 195 rows. That is more than this reference documents,
because of the support entries listed above. To count them instead:

```sql
SELECT count(*) FROM pg_catalog.pg_proc WHERE oid BETWEEN 7000 AND 8100;
```

```
 count
-------
   195
```

A function whose name AgensGraph does not add will not appear, because it belongs to
PostgreSQL. `avg`, `min`, `left` and `log10` are among those. Drop the `WHERE` clause and
filter by name to find one of them.

## See also {#see-also}

- [Aggregate functions](/agensgraph/reference/functions/aggregate/) — `avg`, `collect`, `count`, `min`, `max`, `sum`
- [Predicate functions](/agensgraph/reference/functions/predicate/) — `all`, `any`, `none`, `single`, `exists`, `isEmpty`
- [Scalar functions](/agensgraph/reference/functions/scalar/) — `id`, `label`, `properties`, `size`, `length`
- [List functions](/agensgraph/reference/functions/list/) — `head`, `keys`, `range`, `tail`, `unnest`
- [String functions](/agensgraph/reference/functions/string/) — `substring`, `split`, `toLower`, `trim`
- [Numeric functions](/agensgraph/reference/functions/numeric/) — `abs`, `round`, `log`, the trigonometric family
- [Path functions](/agensgraph/reference/functions/path/) — `nodes`, `relationships`, `shortestpath`, `dijkstra`
- [Type conversion functions](/agensgraph/reference/functions/type-conversion/) — the `to…` family
- [jsonb operators and functions](/agensgraph/reference/functions/jsonb/) — the operators underneath every property
- [Graph metadata](/agensgraph/system-catalogs/graph-metadata/) — the `meta.*` schema
