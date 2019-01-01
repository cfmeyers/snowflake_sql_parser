import pytest
from pyparsing import ParseException

from run import EXPRESSION
from functions import (
    make_context_function_expression,
    make_unary_function_expression,
    make_binary_function_expression,
    make_n_ary_function,
    make_unary_function_with_one_optional_arg,
    make_nullary_function,
    make_unary_function_with_two_optional_args,
    make_unary_function_with_three_optional_args,
    make_binary_function_with_one_optional_args,
)


def assert_parses(expression, text):
    assert expression.parseString(text, parseAll=True)


def assert_raises_parse_exception(expression, text):
    with pytest.raises(ParseException):
        assert expression.parseString(text, parseAll=True)


# Nullary Functions
CONTEXT_FUNCTION = make_context_function_expression(EXPRESSION)

# Unary Functions
UNARY_FUNCTION = make_unary_function_expression(EXPRESSION)
UNARY_FUNCTION_ONE_OPTIONAL = make_unary_function_with_one_optional_arg(EXPRESSION)
UNARY_FUNCTION_TWO_OPTIONAL = make_unary_function_with_two_optional_args(EXPRESSION)
UNARY_FUNCTION_THREE_OPTIONAL = make_unary_function_with_three_optional_args(EXPRESSION)

# Binary Functions
BINARY_FUNCTION = make_binary_function_expression(EXPRESSION)
BINARY_FUNCTION_ONE_OPTIONAL = make_binary_function_with_one_optional_args(EXPRESSION)

# Quaternary Functions
QUATERNARY_FUNCTION = make_n_ary_function('HAVERSINE', 4, EXPRESSION)


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
        it = make_nullary_function('PI')
        assert_parses(it, 'PI()')

    def test_it_must_have_parenthesis(self):
        it = make_nullary_function('PI')
        assert_raises_parse_exception(it, 'PI')

    def test_it_must_have_no_arguments(self):
        it = make_nullary_function('PI')
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


class TestUnaryFunctionWithOneOptionalArg:
    def test_it_can_have_just_one_arg(self):
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'ceil(1)')
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'floor(1)')
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'round(1)')
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'truncate(1)')
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'trunc(1)')

    def test_it_can_have_two_args(self):
        assert_parses(UNARY_FUNCTION_ONE_OPTIONAL, 'CEIL(x, y)')

    def test_it_must_have_either_one_or_two_args(self):
        assert_raises_parse_exception(UNARY_FUNCTION_ONE_OPTIONAL, 'CEIL()')
        assert_raises_parse_exception(UNARY_FUNCTION_ONE_OPTIONAL, 'CEIL(1,2,3)')


class TestUnaryFunctionWithTwoOptionalArgs:
    def test_it_can_have_just_one_arg(self):
        assert_parses(UNARY_FUNCTION_TWO_OPTIONAL, 'BASE64_ENCODE(1)')
        assert_parses(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_DECIMAL(1)')
        assert_parses(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_NUMBER(1)')

    def test_it_can_have_two_args(self):
        assert_parses(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_NUMBER(x, y)')

    def test_it_can_have_three_args(self):
        assert_parses(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_NUMBER(x, y, z)')

    def test_it_must_have_between_one_and_3_args(self):
        assert_raises_parse_exception(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_NUMBER()')
        assert_raises_parse_exception(UNARY_FUNCTION_TWO_OPTIONAL, 'AS_NUMBER(1,2,3,4)')


class TestUnaryFunctionWithThreeOptionalArgs:
    def test_it_can_have_just_one_arg(self):
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL(1)')
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_NUMBER(1)')
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_NUMERIC(1)')

    def test_it_can_have_two_args(self):
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL(x, y)')

    def test_it_can_have_three_args(self):
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL(x, y, z)')

    def test_it_can_have_four_args(self):
        assert_parses(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL(x, y, z, a)')

    def test_it_must_have_between_one_and_4_args(self):
        assert_raises_parse_exception(UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL()')
        assert_raises_parse_exception(
            UNARY_FUNCTION_THREE_OPTIONAL, 'TO_DECIMAL(1,2,3,4,5)'
        )


class TestBinaryFunctionWithOneOptionalArgs:
    def test_it_can_have_just_one_arg(self):
        assert_parses(BINARY_FUNCTION_ONE_OPTIONAL, 'CHARINDEX(1,2)')
        assert_parses(BINARY_FUNCTION_ONE_OPTIONAL, 'ILIKE(1,2)')
        assert_parses(BINARY_FUNCTION_ONE_OPTIONAL, 'LIKE(1,2)')

    def test_it_can_have_three_args(self):
        assert_parses(BINARY_FUNCTION_ONE_OPTIONAL, 'CHARINDEX(x, y, z)')

    def test_it_must_have_between_one_and_3_args(self):
        assert_raises_parse_exception(BINARY_FUNCTION_ONE_OPTIONAL, 'CHARINDEX()')
        assert_raises_parse_exception(
            BINARY_FUNCTION_ONE_OPTIONAL, 'CHARINDEX(1,2,3,4)'
        )
