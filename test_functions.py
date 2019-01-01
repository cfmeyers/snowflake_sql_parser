import pytest
from pyparsing import ParseException

from run import EXPRESSION
from functions import (
    make_context_function_expression,
    make_unary_function_expression,
    make_binary_function_expression,
    make_function,
    make_unary_function_with_optional_arg_expression,
    make_nullary_function_manditory_parenthesis,
)


def assert_parses(expression, text):
    assert expression.parseString(text, parseAll=True)


def assert_raises_parse_exception(expression, text):
    with pytest.raises(ParseException):
        assert expression.parseString(text, parseAll=True)


CONTEXT_FUNCTION = make_context_function_expression(EXPRESSION)

UNARY_FUNCTION = make_unary_function_expression(EXPRESSION)
BINARY_FUNCTION = make_binary_function_expression(EXPRESSION)

# Quaternary Functions
QUATERNARY_FUNCTION = make_function('HAVERSINE', 4, EXPRESSION)

UNARY_FUNCTION_WITH_OPTIONAL_ARG = make_unary_function_with_optional_arg_expression(
    EXPRESSION
)


class TestContextFunction:
    """
    Context functions can optionally be called without parentheses
    """

    def test_it_can_be_just_the_function_name(self):
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_DATE')
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_TIME'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_TIMESTAMP'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_VERSION'),
        assert_parses(CONTEXT_FUNCTION, 'LOCALTIME'),
        assert_parses(CONTEXT_FUNCTION, 'LOCALTIMESTAMP'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_ROLE'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_SESSION'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_STATEMENT'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_TRANSACTION'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_USER'),
        assert_parses(CONTEXT_FUNCTION, 'LAST_QUERY_ID'),
        assert_parses(CONTEXT_FUNCTION, 'LAST_TRANSACTION'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_DATABASE'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_SCHEMA'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_SCHEMAS'),
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_WAREHOUSE'),

    def test_case_does_not_matter(self):
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_DATE')
        assert_parses(CONTEXT_FUNCTION, 'current_date')

    def test_it_can_be_function_name_and_parenthesis(self):
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_DATE()')
        assert_parses(CONTEXT_FUNCTION, 'current_date()')

    def test_it_needs_first_an_opening_then_a_closing_parenthesis_or_none_at_all(self):
        assert_raises_parse_exception(CONTEXT_FUNCTION, 'CURRENT_DATE(')
        assert_raises_parse_exception(CONTEXT_FUNCTION, 'CURRENT_DATE)')
        assert_raises_parse_exception(CONTEXT_FUNCTION, 'CURRENT_DATE)(')


class TestNullaryFunctionMandatoryWithParenthesesFunction:
    def test_it_takes_no_args(self):
        it = make_nullary_function_manditory_parenthesis('PI')
        assert_parses(it, 'PI()')

    def test_it_must_have_parenthesis(self):
        it = make_nullary_function_manditory_parenthesis('PI')
        assert_raises_parse_exception(it, 'PI')

    def test_it_must_have_no_arguments(self):
        it = make_nullary_function_manditory_parenthesis('PI')
        assert_raises_parse_exception(it, 'PI(1)')


class TestUnaryFunction:
    def test_it_takes_a_single_arg(self):
        assert_parses(UNARY_FUNCTION, 'BITNOT(1)')
        assert_parses(UNARY_FUNCTION, 'BITNOT(x)')
        assert_parses(UNARY_FUNCTION, 'BITNOT(1+1)')
        assert_parses(UNARY_FUNCTION, 'BITNOT(1+(1+2))')
        assert_parses(UNARY_FUNCTION, 'bitand_agg(1)')

    def test_unary_function_must_have_exactly_1_argument(self):
        assert_raises_parse_exception(UNARY_FUNCTION, 'BITNOT(x, y)')
        assert_raises_parse_exception(UNARY_FUNCTION, 'BITNOT()')


class TestBinaryFunction:
    def test_it_takes_two_args(self):
        assert_parses(BINARY_FUNCTION, 'BITAND(x,y)')
        assert_parses(BINARY_FUNCTION, 'bitand(x,y)')
        assert_parses(BINARY_FUNCTION, 'bitand(1, y)')

    def test_it_can_be_have_expressions_as_arguments(self):
        assert_parses(BINARY_FUNCTION, 'bitand( x, 5+5*2 )')

    def test_it_must_have_exactly_2_arguments(self):
        assert_raises_parse_exception(BINARY_FUNCTION, 'BITAND(y)')
        assert_raises_parse_exception(BINARY_FUNCTION, 'BITAND(x, y, z)')


class TestQuaternaryFunction:
    def test_it_takes_four_args(self):
        assert_parses(QUATERNARY_FUNCTION, 'HAVERSINE(w,x,y,z)')

    def test_it_must_have_exactly_4_arguments(self):
        assert_raises_parse_exception(QUATERNARY_FUNCTION, 'HAVERSINE()')
        assert_raises_parse_exception(QUATERNARY_FUNCTION, 'HAVERSINE(x)')
        assert_raises_parse_exception(QUATERNARY_FUNCTION, 'HAVERSINE(x,y)')
        assert_raises_parse_exception(QUATERNARY_FUNCTION, 'HAVERSINE(x,y,z)')
        assert_raises_parse_exception(QUATERNARY_FUNCTION, 'HAVERSINE(x,y,z,1,2)')


class TestUnaryFunctionWithOptionalArg:
    def test_it_can_have_just_one_arg(self):
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'ABS(x)')
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'ceil(1)')
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'floor(1)')
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'round(1)')
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'truncate(1)')
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'trunc(1)')

    def test_it_can_have_two_args(self):
        assert_parses(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'ABS(x, y)')

    def test_it_must_have_either_one_or_two_args(self):
        assert_raises_parse_exception(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'ABS()')
        assert_raises_parse_exception(UNARY_FUNCTION_WITH_OPTIONAL_ARG, 'ABS(1,2,3)')
