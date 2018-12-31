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


def make_nullary_function_manditory_parenthesis(func_name):
    return CaselessKeyword(func_name) + '()'


def make_unary_function(func_name):
    return CaselessKeyword(func_name) + '(' + EXPRESSION('arg_1') + ')'


def make_unary_function_with_optional_arg(func_name):
    return (
        CaselessKeyword(func_name)
        + '('
        + EXPRESSION('arg_1')
        + Optional(',' + EXPRESSION('arg_2_optional'))
        + ')'
    )


def make_function(func_name, arity):
    func_expression = CaselessKeyword(func_name) + '('
    for arg_num in range(1, arity + 1):
        arg_name = 'arg_' + str(arg_num)
        func_expression += EXPRESSION(arg_name)
        if arg_num < arity:
            func_expression += ','
    func_expression += ')'
    return func_expression


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

PI = make_nullary_function_manditory_parenthesis('PI')
NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES = PI


# Unary Functions
BITAND_AGG = make_unary_function('BITAND_AGG')
BITNOT = make_unary_function('BITNOT')
BITOR_AGG = make_unary_function('BITOR_AGG')
BITXOR_AGG = make_unary_function('BITXOR_AGG')
SIGN = make_unary_function('SIGN')
CBRT = make_unary_function('CBRT')
EXP = make_unary_function('EXP')
FACTORIAL = make_unary_function('FACTORIAL')
SQRT = make_unary_function('SQRT')
SQUARE = make_unary_function('SQUARE')
LN = make_unary_function('LN')

ACOS = make_unary_function('ACOS')
ACOSH = make_unary_function('ACOSH')
ASIN = make_unary_function('ASIN')
ASINH = make_unary_function('ASINH')
ATAN = make_unary_function('ATAN')
ATAN2 = make_unary_function('ATAN2')
ATANH = make_unary_function('ATANH')
COS = make_unary_function('COS')
COSH = make_unary_function('COSH')
COT = make_unary_function('COT')
DEGREES = make_unary_function('DEGREES')
RADIANS = make_unary_function('RADIANS')
SIN = make_unary_function('SIN')
SINH = make_unary_function('SINH')
TAN = make_unary_function('TAN')
TANH = make_unary_function('TANH')

UNARY_FUNCTION = (
    BITAND_AGG
    | BITNOT
    | BITOR_AGG
    | BITXOR_AGG
    | SIGN
    | CBRT
    | EXP
    | FACTORIAL
    | SQRT
    | SQUARE
    | LN
    | ACOS
    | ACOSH
    | ASIN
    | ASINH
    | ATAN
    | ATAN2
    | ATANH
    | COS
    | COSH
    | COT
    | DEGREES
    | RADIANS
    | SIN
    | SINH
    | TAN
    | TANH
)


# Binary Functions
BITAND = make_function('BITAND', 2)
BITOR = make_function('BITOR', 2)
BITSHIFTLEFT = make_function('BITSHIFTLEFT', 2)
BITSHIFTRIGHT = make_function('BITSHIFTRIGHT', 2)
BITXOR = make_function('BITXOR', 2)
MOD = make_function('MOD', 2)
POW = make_function('POW', 2)
POWER = make_function('POWER', 2)
LOG = make_function('LOG', 2)


BINARY_FUNCTION = (
    BITAND | BITOR | BITSHIFTLEFT | BITSHIFTRIGHT | BITXOR | MOD | POW | POWER | LOG
)

# Quaternary Functions
HAVERSINE = make_function('HAVERSINE', 4)
QUATERNARY_FUNCTION = HAVERSINE

ABS = make_unary_function_with_optional_arg('ABS')
CEIL = make_unary_function_with_optional_arg('CEIL')
FLOOR = make_unary_function_with_optional_arg('FLOOR')
ROUND = make_unary_function_with_optional_arg('ROUND')
TRUNCATE = make_unary_function_with_optional_arg('TRUNCATE')
TRUNC = make_unary_function_with_optional_arg('TRUNC')


UNARY_FUNCTION_WITH_OPTIONAL_ARG = ABS | CEIL | FLOOR | ROUND | TRUNCATE | TRUNC


FUNCTION_EXPRESSION = (
    CONTEXT_FUNCTION
    | UNARY_FUNCTION
    | BINARY_FUNCTION
    | UNARY_FUNCTION_WITH_OPTIONAL_ARG
    | QUATERNARY_FUNCTION
    | NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES
)
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
