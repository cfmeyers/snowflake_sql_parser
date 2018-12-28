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


SELECT, FROM, WHERE = [CaselessKeyword(w) for w in 'select from where'.split()]

IDENTIFIER = ~(SELECT | FROM | WHERE) + Word(alphas, alphanums + "_$")

## Expressions
QUOTED_SQL_STRING = QuotedString("'")

## Define Numbers
DIGIT = Word(nums, asKeyword=True)
INTEGER = DIGIT('integer')
REAL_NUMBER = (DIGIT + '.' + DIGIT)('real_number')
NUMBER = REAL_NUMBER | INTEGER

## Simple Arithmetic Expressions
## See https://github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py

OPERAND = NUMBER | IDENTIFIER
ARITHMETIC_EXPRESSION = infixNotation(
    OPERAND,
    [
        (oneOf('- +'), 1, opAssoc.RIGHT),
        (oneOf('* /'), 2, opAssoc.LEFT),
        (oneOf('+ -'), 2, opAssoc.LEFT),
    ],
)


SPLAT = Keyword('*')
AS = CaselessKeyword('as')
TABLE_NAME = IDENTIFIER('table')
ALIAS = Optional(AS) + IDENTIFIER('alias_name')


## End Expressions

COLUMN_VALUE = (IDENTIFIER | ARITHMETIC_EXPRESSION | QUOTED_SQL_STRING)('column_value')

COLUMN = Group(COLUMN_VALUE + Optional(ALIAS))
COLUMN_LIST = Group(delimitedList(COLUMN))('column_list')

SELECT_STATEMENT = SELECT + (SPLAT | COLUMN_LIST) + FROM + TABLE_NAME + ';'

STATEMENT_DEF = SELECT_STATEMENT('select_statement')

STATEMENTS = OneOrMore(STATEMENT_DEF)


def parse_sql(sql_text):
    parsed = STATEMENTS.parseString(sql_text, parseAll=True)
    return parsed
