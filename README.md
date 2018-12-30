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
        - [ ] [Numeric Functions](https://docs.snowflake.net/manuals/sql-reference/functions-numeric.html)
        - [ ] [String & Binary Functions](https://docs.snowflake.net/manuals/sql-reference/functions-string.html)
        - [ ] [String Functions (Regular Expressions)](https://docs.snowflake.net/manuals/sql-reference/functions-regexp.html)
        - [ ] [Date & Time Functions](https://docs.snowflake.net/manuals/sql-reference/functions-date-time.html)
        - [ ] [Semi-structured Data Functions](https://docs.snowflake.net/manuals/sql-reference/functions-semistructured.html)
        - [ ] [Conversion Functions](https://docs.snowflake.net/manuals/sql-reference/functions-conversion.html)
        - [ ] [Aggregate Functions](https://docs.snowflake.net/manuals/sql-reference/functions-aggregation.html)
        - [ ] [Analytic / Window Functions](https://docs.snowflake.net/manuals/sql-reference/functions-analytic.html)
        - [ ] [Miscellaneous Functions](https://docs.snowflake.net/manuals/sql-reference/functions-other.html)
        - [ ] [Conditional Expression Functions](https://docs.snowflake.net/manuals/sql-reference/expressions-conditional.html)
        - [X] [Bitwise Expression Functions](https://docs.snowflake.net/manuals/sql-reference/expressions-byte-bit.html)
    - [ ] [Table Functions](https://docs.snowflake.net/manuals/sql-reference/intro-summary-operators-functions.html#table-functions)
        - [ ] [Table Functions](https://docs.snowflake.net/manuals/sql-reference/functions-table.html#label-table-functions)
        - [ ] [Table Functions (Information Schema)](https://docs.snowflake.net/manuals/sql-reference/info-schema.html#label-info-schema-functions)
        - [ ] [SQL UDTFs (User-Defined Table Functions)](https://docs.snowflake.net/manuals/sql-reference/udf-table-functions.html)
- [ ] [cast operator](https://docs.snowflake.net/manuals/sql-reference/functions/cast.html) (`::`)
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


[[##]] CREATE TABLE/VIEW/UDF/SCHEMA/PIPE/DATABASE

## INSERT

## UPDATE

## DELETE
