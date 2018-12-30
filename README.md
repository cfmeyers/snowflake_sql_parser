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
- [o] [functions](https://docs.snowflake.net/manuals/sql-reference/functions.html)
    - [X] [context functions](https://docs.snowflake.net/manuals/sql-reference/functions-context.html)
    - [X] [bitwise expression functions](https://docs.snowflake.net/manuals/sql-reference/expressions-byte-bit.html)
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
- [ ] UDF


## CREATE TABLE/VIEW/UDF/SCHEMA/PIPE/DATABASE

## INSERT

## UPDATE

## DELETE
