# Snowflake SQL Parser

A Python library for parsing Snowflake SQL statements (using [PyParsing](https://github.com/pyparsing/pyparsing)).
Initially it will just check if a script is properly-formed Snowflake SQL.  In the medium-term it will be used to develop a Snowflake SQL formatter.


# Implemented So Far

## `SELECT`

- [X] [boolean expressions](https://docs.snowflake.net/manuals/sql-reference/operators-logical.html)
- [X] [comparison expressions](https://docs.snowflake.net/manuals/sql-reference/operators-comparison.html)
- [X] [arithmetic expressions](https://docs.snowflake.net/manuals/sql-reference/operators-arithmetic.html)
- [X] identifiers
- [X] quoted string literals
- [X] splat
- [X] numbers
- [X] [case](https://docs.snowflake.net/manuals/sql-reference/functions/case.html)
- [X] column alias
- [X] column list
- [X] table name
- [X] [schema](https://docs.snowflake.net/manuals/sql-reference/constructs/from.html#object-or-table-function-clause)
- [X] [database](https://docs.snowflake.net/manuals/sql-reference/constructs/from.html#object-or-table-function-clause)
- [.] [functions](https://docs.snowflake.net/manuals/sql-reference/functions.html)
    - [.] [Scalar Functions](https://docs.snowflake.net/manuals/sql-reference/intro-summary-operators-functions.html#scalar-functions)
        - [X] [Context Functions](https://docs.snowflake.net/manuals/sql-reference/functions-context.html)
        - [X] [Numeric Functions](https://docs.snowflake.net/manuals/sql-reference/functions-numeric.html)
        - [X] [String & Binary Functions](https://docs.snowflake.net/manuals/sql-reference/functions-string.html)
        - [X] [String Functions (Regular Expressions)](https://docs.snowflake.net/manuals/sql-reference/functions-regexp.html)
        - [X] [Date & Time Functions](https://docs.snowflake.net/manuals/sql-reference/functions-date-time.html)
        - [X] [Semi-structured Data Functions](https://docs.snowflake.net/manuals/sql-reference/functions-semistructured.html)
        - [X] [Conversion Functions](https://docs.snowflake.net/manuals/sql-reference/functions-conversion.html)
        - [X] [Miscellaneous Functions](https://docs.snowflake.net/manuals/sql-reference/functions-other.html)
        - [X] [Conditional Expression Functions](https://docs.snowflake.net/manuals/sql-reference/expressions-conditional.html)
        - [X] [Bitwise Expression Functions](https://docs.snowflake.net/manuals/sql-reference/expressions-byte-bit.html)
        - [ ] [Aggregate Functions](https://docs.snowflake.net/manuals/sql-reference/functions-aggregation.html)
        - [ ] [Analytic / Window Functions](https://docs.snowflake.net/manuals/sql-reference/functions-analytic.html)
    - [ ] [Table Functions](https://docs.snowflake.net/manuals/sql-reference/intro-summary-operators-functions.html#table-functions)
        - [ ] [Table Functions](https://docs.snowflake.net/manuals/sql-reference/functions-table.html#label-table-functions)
        - [ ] [Table Functions (Information Schema)](https://docs.snowflake.net/manuals/sql-reference/info-schema.html#label-info-schema-functions)
        - [ ] [SQL UDTFs (User-Defined Table Functions)](https://docs.snowflake.net/manuals/sql-reference/udf-table-functions.html)
- [ ] [cast operator](https://docs.snowflake.net/manuals/sql-reference/functions/cast.html) (`::`)
- [ ] [concat operator](https://docs.snowflake.net/manuals/sql-reference/functions/concat.html) (`||`)
- [ ] table alias
- [ ] [Common Table Expressions](https://docs.snowflake.net/manuals/sql-reference/constructs/with.html) (i.e. `WITH`)
- [ ] [GROUP BY](https://docs.snowflake.net/manuals/sql-reference/constructs/group-by.html)
- [ ] [ORDER BY](https://docs.snowflake.net/manuals/sql-reference/constructs/order-by.html)
- [ ] [HAVING](https://docs.snowflake.net/manuals/sql-reference/constructs/having.html)
- [ ] [WHERE](https://docs.snowflake.net/manuals/sql-reference/constructs/where.html)
- [ ] [LIMIT](https://docs.snowflake.net/manuals/sql-reference/constructs/limit.html)
- [ ] [FETCH](https://docs.snowflake.net/manuals/sql-reference/constructs/limit.html)
- [ ] quoted column alias
- [ ] [UDF](https://docs.snowflake.net/manuals/sql-reference/user-defined-functions.html)
- [ ] binary strings
- [ ] [ilike](https://docs.snowflake.net/manuals/sql-reference/functions/ilike.html)
- [ ] [like](https://docs.snowflake.net/manuals/sql-reference/functions/like.html)
- [ ] [RLIKE](https://docs.snowflake.net/manuals/sql-reference/functions/rlike.html)
- [ ] [FLATTEN](https://docs.snowflake.net/manuals/sql-reference/functions/flatten.html)
- [ ] [Aggregate Funtions](https://docs.snowflake.net/manuals/sql-reference/functions-aggregation.html)
- [ ] [Analytic/Window Functions](https://docs.snowflake.net/manuals/sql-reference/functions-analytic.html)


[[##]] CREATE TABLE/VIEW/UDF/SCHEMA/PIPE/DATABASE

### Not Implemented

## INSERT

### Not Implemented

## UPDATE

### Not Implemented

## DELETE

### Not Implemented



# Functions To Implement:

## 6-ary Function with 1 optional arg
- [ ] [TIMESTAMP_LTZ_FROM_PARTS](https://docs.snowflake.net/manuals/sql-reference/functions/timestamp_from_parts.html)

## 6-ary Function with 2 optional args
- [ ] TIMESTAMP_TZ_FROM_PARTS

## 6-ary Function with 1 optional OR binary function
- [ ] [TIMESTAMP_NTZ_FROM_PARTS](https://docs.snowflake.net/manuals/sql-reference/functions/timestamp_from_parts.html)

## 6-ary Function with 2 optional args OR binary function
- [ ] [TIMESTAMP_FROM_PARTS](https://docs.snowflake.net/manuals/sql-reference/functions/timestamp_from_parts.html)

## N-ary function
- [ ] [ARRAY_CONSTRUCT](https://docs.snowflake.net/manuals/sql-reference/functions/array_construct.html)
- [ ] [ARRAY_CONSTRUCT_COMPACT](https://docs.snowflake.net/manuals/sql-reference/functions/array_construct_compact.html)
- [ ] SYSTEM$CLUSTERING_DEPTH
- [ ] SYSTEM$CLUSTERING_INFORMATION
- [ ] SYSTEM$CLUSTERING_RATIO

## N-ary function with minimum of 2 args
- [ ] [OBJECT_DELETE](https://docs.snowflake.net/manuals/sql-reference/functions/object_delete.html)

## Functions with special `in` syntax
- [ ] [POSITION](https://docs.snowflake.net/manuals/sql-reference/functions/position.html)

## Functions with special ``<arg> REGEXP <arg>`` syntax
- [ ] [REGEXP](https://docs.snowflake.net/manuals/sql-reference/functions/regexp.html)

## Functions that are either Nullary or Binary (not unary or trinary+)
- [ ] [UUID_STRING](https://docs.snowflake.net/manuals/sql-reference/functions/uuid_string.html)

## Functions with special `EXTRACT(arg  FROM arg)` syntax
- [ ] [EXTRACT](https://docs.snowflake.net/manuals/sql-reference/functions/extract.html)

## Functions with special `ARRAY_AGG(DISTINCT arg) WITHIN GROUP` syntax
- [ ] [ARRAY_AGG](https://docs.snowflake.net/manuals/sql-reference/functions/array_agg.html)

## Functions with special `OBJECT_CONSTRUCT(*)` syntax
- [ ] [OBJECT_CONSTRUCT](https://docs.snowflake.net/manuals/sql-reference/functions/object_construct.html)
- [ ] [HASH](https://docs.snowflake.net/manuals/sql-reference/functions/hash.html)
- [ ] [HASH_AGG](https://docs.snowflake.net/manuals/sql-reference/functions/hash_agg.html)

## Functions with special `CAST(x AS y)` syntax
- [ ] [CAST](https://docs.snowflake.net/manuals/sql-reference/functions/cast.html)
- [ ] [TRY_CAST](https://docs.snowflake.net/manuals/sql-reference/functions/try_cast.html)
