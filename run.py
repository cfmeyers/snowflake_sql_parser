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

TABLE_NAME = IDENTIFIER('table')
ALIAS = Optional(AS) + IDENTIFIER('alias_name')

COLUMN_VALUE = (
    IDENTIFIER
    | CASE_EXPRESSION
    | BOOLEAN_EXPRESSION
    | COMPARISON_EXPRESSION
    | ARITHMETIC_EXPRESSION
    | QUOTED_SQL_STRING
)('column_value')

COLUMN = Group(COLUMN_VALUE + Optional(ALIAS))
COLUMN_LIST = Group(delimitedList(COLUMN))('column_list')

SELECT_STATEMENT = (
    SELECT + Optional(DISTINCT | ALL) + (SPLAT | COLUMN_LIST) + FROM + TABLE_NAME + ';'
)

STATEMENT_DEF = SELECT_STATEMENT('select_statement')

STATEMENTS = OneOrMore(STATEMENT_DEF)


def parse_sql(sql_text):
    parsed = STATEMENTS.parseString(sql_text, parseAll=True)
    return parsed
