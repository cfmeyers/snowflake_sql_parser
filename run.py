"""
see https://github.com/mozilla/moz-sql-parser/blob/dev/moz_sql_parser/sql_parser.py
"""
from pyparsing import (
    CaselessKeyword,
    Word,
    Keyword,
    alphanums,
    nums,
    alphas,
    OneOrMore,
    delimitedList,
    Group,
    Optional,
    pyparsing_common,
    oneOf,
    StringEnd,
    Combine,
    ZeroOrMore,
    QuotedString,
    Forward,
    infixNotation,
    opAssoc,
)

EXPRESSION = Forward()


SELECT = CaselessKeyword('select')
FROM = CaselessKeyword('from')
WHERE = CaselessKeyword('where')
IS = CaselessKeyword('is')
NOT = CaselessKeyword('not')
NULL = CaselessKeyword('null')
CASE = CaselessKeyword('case')
END = CaselessKeyword('end')
WHEN = CaselessKeyword('when')
THEN = CaselessKeyword('then')
ELSE = CaselessKeyword('else')
SPLAT = Keyword('*')
AS = CaselessKeyword('as')
DISTINCT = CaselessKeyword('distinct')
ALL = CaselessKeyword('ALL')

KEYWORD = (
    SELECT
    | FROM
    | WHERE
    | IS
    | NOT
    | NULL
    | CASE
    | END
    | WHEN
    | THEN
    | ELSE
    | SPLAT
    | AS
    | DISTINCT
    | ALL
)

IDENTIFIER = ~KEYWORD + Word(alphas, alphanums + "_$")

## Expressions
QUOTED_SQL_STRING = QuotedString("'")

## Define Numbers
DIGIT = Word(nums, asKeyword=True)
INTEGER = DIGIT('integer')
REAL_NUMBER = (DIGIT + '.' + DIGIT)('real_number')
NUMBER = REAL_NUMBER | INTEGER

## Simple Arithmetic Expressions
## See https://github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py

ARITHMETIC_OPERAND = NUMBER | IDENTIFIER
ARITHMETIC_EXPRESSION = infixNotation(
    ARITHMETIC_OPERAND,
    [
        (oneOf('- +'), 1, opAssoc.RIGHT),
        (oneOf('* / %'), 2, opAssoc.LEFT),
        (oneOf('+ -'), 2, opAssoc.LEFT),
    ],
)


COMPARISON_OPERAND = ARITHMETIC_EXPRESSION
COMPARISON_OPERATOR = oneOf('= != <> > < <= >=')
COMPARISON_EXPRESSION = (COMPARISON_OPERAND + IS + Optional(NOT) + NULL) | (
    COMPARISON_OPERAND + COMPARISON_OPERATOR + COMPARISON_OPERAND
)

BOOLEAN_OPERAND = (
    CaselessKeyword('true')
    | CaselessKeyword('false')
    | COMPARISON_EXPRESSION
    | IDENTIFIER
)
BOOLEAN_EXPRESSION = infixNotation(
    BOOLEAN_OPERAND,
    [
        (CaselessKeyword('not'), 1, opAssoc.RIGHT),
        (CaselessKeyword('and'), 2, opAssoc.LEFT),
        (CaselessKeyword('or'), 2, opAssoc.LEFT),
    ],
)

CASE_EXPRESSION = (
    CASE
    + OneOrMore(WHEN + BOOLEAN_EXPRESSION + THEN + (IDENTIFIER | NUMBER))
    + Optional(ELSE + (IDENTIFIER | NUMBER))
    + END
)
## End Expressions

## Function Expressions
def make_nullary_function(func_name):
    return CaselessKeyword(func_name) + Optional('()')


def make_unary_function(func_name):
    return CaselessKeyword(func_name) + '(' + EXPRESSION('arg_1') + ')'


def make_binary_function(func_name):
    return (
        CaselessKeyword(func_name)
        + '('
        + EXPRESSION('arg_1')
        + ','
        + EXPRESSION('arg_2')
        + ')'
    )


CURRENT_CLIENT = make_nullary_function('CURRENT_CLIENT')
CURRENT_DATE = make_nullary_function('CURRENT_DATE')
CURRENT_TIME = make_nullary_function('CURRENT_TIME')
CURRENT_TIMESTAMP = make_nullary_function('CURRENT_TIMESTAMP')
CURRENT_VERSION = make_nullary_function('CURRENT_VERSION')
LOCALTIME = make_nullary_function('LOCALTIME')
LOCALTIMESTAMP = make_nullary_function('LOCALTIMESTAMP')
CURRENT_ROLE = make_nullary_function('CURRENT_ROLE')
CURRENT_SESSION = make_nullary_function('CURRENT_SESSION')
CURRENT_STATEMENT = make_nullary_function('CURRENT_STATEMENT')
CURRENT_TRANSACTION = make_nullary_function('CURRENT_TRANSACTION')
CURRENT_USER = make_nullary_function('CURRENT_USER')
LAST_QUERY_ID = make_nullary_function('LAST_QUERY_ID')
LAST_TRANSACTION = make_nullary_function('LAST_TRANSACTION')
CURRENT_DATABASE = make_nullary_function('CURRENT_DATABASE')
CURRENT_SCHEMA = make_nullary_function('CURRENT_SCHEMA')
CURRENT_SCHEMAS = make_nullary_function('CURRENT_SCHEMAS')
CURRENT_WAREHOUSE = make_nullary_function('CURRENT_WAREHOUSE')


# Context functions take no args, can optionally be called without parentheses
CONTEXT_FUNCTION = (
    CURRENT_CLIENT
    | CURRENT_DATE
    | CURRENT_TIME
    | CURRENT_TIMESTAMP
    | CURRENT_VERSION
    | LOCALTIME
    | LOCALTIMESTAMP
    | CURRENT_ROLE
    | CURRENT_SESSION
    | CURRENT_STATEMENT
    | CURRENT_TRANSACTION
    | CURRENT_USER
    | LAST_QUERY_ID
    | LAST_TRANSACTION
    | CURRENT_DATABASE
    | CURRENT_SCHEMA
    | CURRENT_SCHEMAS
    | CURRENT_WAREHOUSE
)


# Bitwise Expression Functions
BITAND_AGG = make_unary_function('BITAND_AGG')
BITNOT = make_unary_function('BITNOT')
BITOR_AGG = make_unary_function('BITOR_AGG')
BITXOR_AGG = make_unary_function('BITXOR_AGG')

BITAND = make_binary_function('BITAND')
BITOR = make_binary_function('BITOR')
BITSHIFTLEFT = make_binary_function('BITSHIFTLEFT')
BITSHIFTRIGHT = make_binary_function('BITSHIFTRIGHT')
BITXOR = make_binary_function('BITXOR')

BITWISE_FUNCTION = (
    BITAND_AGG
    | BITNOT
    | BITOR_AGG
    | BITXOR_AGG
    | BITAND
    | BITOR
    | BITSHIFTLEFT
    | BITSHIFTRIGHT
    | BITXOR
)


FUNCTION_EXPRESSION = CONTEXT_FUNCTION | BITWISE_FUNCTION
## End function expressions

TABLE_NAME = IDENTIFIER('table')
SCHEMA_NAME = IDENTIFIER('schema')
DATABASE_NAME = IDENTIFIER('database')
TABLE_OBJECT = (
    DATABASE_NAME + '.' + SCHEMA_NAME + '.' + TABLE_NAME
    | SCHEMA_NAME + '.' + TABLE_NAME
    | TABLE_NAME
)
ALIAS = Optional(AS) + IDENTIFIER('alias_name')
EXPRESSION << (
    FUNCTION_EXPRESSION
    | IDENTIFIER
    | CASE_EXPRESSION
    | BOOLEAN_EXPRESSION
    | COMPARISON_EXPRESSION
    | ARITHMETIC_EXPRESSION
    | QUOTED_SQL_STRING
)('expression')

COLUMN = Group(EXPRESSION + Optional(ALIAS))
COLUMN_LIST = Group(delimitedList(COLUMN))('column_list')
FROM_CLAUSE = FROM + TABLE_OBJECT

SELECT_STATEMENT = (
    SELECT
    + Optional(DISTINCT | ALL)
    + (SPLAT | COLUMN_LIST)
    + Optional(FROM_CLAUSE)
    + ';'
)

STATEMENT_DEF = SELECT_STATEMENT('select_statement')

STATEMENTS = OneOrMore(STATEMENT_DEF)


def parse_sql(sql_text):
    parsed = STATEMENTS.parseString(sql_text, parseAll=True)
    return parsed
