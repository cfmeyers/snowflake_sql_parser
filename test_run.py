import pytest
from pyparsing import ParseException

from run import (
    parse_sql,
    IDENTIFIER,
    INTEGER,
    NUMBER,
    REAL_NUMBER,
    QUOTED_SQL_STRING,
    ARITHMETIC_EXPRESSION,
    COMPARISON_EXPRESSION,
    BOOLEAN_EXPRESSION,
    CASE_EXPRESSION,
    TABLE_OBJECT,
    CONTEXT_FUNCTION,
    UNARY_FUNCTION,
    BINARY_FUNCTION,
    UNARY_FUNCTION_WITH_OPTIONAL_ARG,
    QUATERNARY_FUNCTION,
    NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES,
)


def assert_parses(expression, text):
    assert expression.parseString(text, parseAll=True)


def assert_raises_parse_exception(expression, text):
    with pytest.raises(ParseException):
        assert expression.parseString(text, parseAll=True)


class TestContextFunction:
    """
    Context functions can optionally be called without parentheses
    """

    def test_it_can_be_just_the_function_name(self):
        assert_parses(CONTEXT_FUNCTION, 'CURRENT_DATE')

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
        assert_parses(NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES, 'PI()')

    def test_it_must_have_parenthesis(self):
        assert_raises_parse_exception(NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES, 'PI')

    def test_it_must_have_no_arguments(self):
        assert_raises_parse_exception(
            NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES, 'PI(1)'
        )


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


class TestIdentifier:
    def test_it_can_be_just_letters(self):
        assert_parses(IDENTIFIER, 'foodlion')

    def test_it_can_be_initial_letter_then_digits(self):
        assert_parses(IDENTIFIER, 'x11')

    def test_it_can_be_initial_letter_then_underscore(self):
        assert_parses(IDENTIFIER, 'x11_version2')

    def test_it_cannot_start_with_a_digit(self):
        assert_raises_parse_exception(IDENTIFIER, '1')

    def test_it_cannot_start_with_an_underscore(self):
        assert_raises_parse_exception(IDENTIFIER, '_x')

    def test_it_cannot_be_a_keyword(self):
        keywords = ['select', 'from', 'where']
        for keyword in keywords:
            assert_raises_parse_exception(IDENTIFIER, keyword)

    def test_it_cannot_have_a_dot(self):
        assert_raises_parse_exception(IDENTIFIER, 'hello.world')


class TestTableObject:
    def test_it_is_an_identifier(self):
        assert_parses(TABLE_OBJECT, 'hornswoggler')
        assert_raises_parse_exception(TABLE_OBJECT, '1hornswoggler')

    def test_it_can_have_a_schema(self):
        assert_parses(TABLE_OBJECT, 'crodscollop.hornswoggler')

    def test_it_can_have_a_schema_and_a_database_name(self):
        assert_parses(TABLE_OBJECT, 'fun.crodscollop.hornswoggler')


class TestQuotedString:
    def test_it_can_be_the_empty_string(self):
        assert_parses(QUOTED_SQL_STRING, "''")

    def test_it_can_be_a_string_of_ascii(self):
        assert_parses(QUOTED_SQL_STRING, "'hello'")

    def test_it_can_be_a_string_with_a_space(self):
        assert_parses(QUOTED_SQL_STRING, "'hello world'")

    def test_it_can_have_non_identifier_characters(self):
        assert_parses(QUOTED_SQL_STRING, "'hello-world'")
        assert_parses(QUOTED_SQL_STRING, "'hello~world'")
        assert_parses(QUOTED_SQL_STRING, "'hello/world'")
        assert_parses(QUOTED_SQL_STRING, "'hello..world'")
        assert_parses(QUOTED_SQL_STRING, "'he&*()#@-rld'")

    def test_it_must_be_surrounded_in_quotes(self):
        assert_raises_parse_exception(QUOTED_SQL_STRING, "hello")

    def test_it_must_start_with_a_single_quote(self):
        assert_raises_parse_exception(QUOTED_SQL_STRING, "'hello")

    def test_it_must_end_with_a_single_quote(self):
        assert_raises_parse_exception(QUOTED_SQL_STRING, "hello'")

    def test_it_does_not_use_double_quotes(self):
        assert_raises_parse_exception(QUOTED_SQL_STRING, '"hello"')


class TestArithmeticExpression:
    def test_it_parses_operands_that_are_numeric(self):
        assert_parses(ARITHMETIC_EXPRESSION, '1+1')
        assert_parses(ARITHMETIC_EXPRESSION, '1 +1')
        assert_parses(ARITHMETIC_EXPRESSION, '1 + 1')
        assert_parses(ARITHMETIC_EXPRESSION, '1+ 1')
        assert_parses(ARITHMETIC_EXPRESSION, '1-1')
        assert_parses(ARITHMETIC_EXPRESSION, '1*1')
        assert_parses(ARITHMETIC_EXPRESSION, '1/1')

    def test_it_parses_operands_that_are_identifiers(self):
        assert_parses(ARITHMETIC_EXPRESSION, 'x+y')
        assert_parses(ARITHMETIC_EXPRESSION, '1+y')
        assert_parses(ARITHMETIC_EXPRESSION, 'x+1')
        assert_parses(ARITHMETIC_EXPRESSION, 'x-1')
        assert_parses(ARITHMETIC_EXPRESSION, 'x*1')
        assert_parses(ARITHMETIC_EXPRESSION, 'x/1')
        assert_parses(ARITHMETIC_EXPRESSION, 'x%1')

    def test_it_parses_operands_that_are_expressions(self):
        assert_parses(ARITHMETIC_EXPRESSION, '(x+y)+z')
        assert_parses(ARITHMETIC_EXPRESSION, '(x-y)+z')
        assert_parses(ARITHMETIC_EXPRESSION, '(x-y)-z')

    def test_it_parses_negative_operands(self):
        assert_parses(ARITHMETIC_EXPRESSION, '-1')

    def test_it_allows_for_parenthesis_surrounding_arithmetic_expression(self):
        assert_parses(ARITHMETIC_EXPRESSION, '(x+y)')

    def test_a_single_number_is_an_expression(self):
        assert_parses(ARITHMETIC_EXPRESSION, '1')

    def test_a_single_identifier_is_an_expression(self):
        assert_parses(ARITHMETIC_EXPRESSION, 'x')

    def test_addition_requires_2_parentheses_or_none_at_all(self):
        assert_raises_parse_exception(ARITHMETIC_EXPRESSION, '(1 + 1')
        assert_raises_parse_exception(ARITHMETIC_EXPRESSION, '1 + 1)')


class TestComparisonExpression:
    def test_it_parses_operands_that_are_numeric(self):
        assert_parses(COMPARISON_EXPRESSION, '1=1')
        assert_parses(COMPARISON_EXPRESSION, '1!=1')
        assert_parses(COMPARISON_EXPRESSION, '1 != 1')
        assert_parses(COMPARISON_EXPRESSION, '1 <> 1')
        assert_parses(COMPARISON_EXPRESSION, '1 > 1')
        assert_parses(COMPARISON_EXPRESSION, '1 < 1')
        assert_parses(COMPARISON_EXPRESSION, '1 < 1')
        assert_parses(COMPARISON_EXPRESSION, '1 <= 1')
        assert_parses(COMPARISON_EXPRESSION, '1 >= 1')
        assert_parses(COMPARISON_EXPRESSION, '(2+2) >= 1')

    def test_it_parses_operands_that_are_identifiers(self):
        assert_parses(COMPARISON_EXPRESSION, 'x=1')

    def test_it_parses_null_tests(self):
        assert_parses(COMPARISON_EXPRESSION, 'x is null')
        assert_parses(COMPARISON_EXPRESSION, 'x is not null')

    def test_a_comparison_requires_two_operands(self):
        assert_raises_parse_exception(COMPARISON_EXPRESSION, '1 >=')
        assert_raises_parse_exception(COMPARISON_EXPRESSION, '1=')


class TestBooleanExpression:
    def test_it_parses_boolean_keywords(self):
        assert_parses(BOOLEAN_EXPRESSION, 'true')
        assert_parses(BOOLEAN_EXPRESSION, 'TRUE')
        assert_parses(BOOLEAN_EXPRESSION, 'True')
        assert_parses(BOOLEAN_EXPRESSION, 'False')
        assert_parses(BOOLEAN_EXPRESSION, 'FALSE')
        assert_parses(BOOLEAN_EXPRESSION, 'False')

    def test_it_parses_comparison_expressions_as_operands(self):
        assert_parses(BOOLEAN_EXPRESSION, '1 >= 1')

    def test_it_parses_identifiers(self):
        assert_parses(BOOLEAN_EXPRESSION, 'x')
        assert_parses(BOOLEAN_EXPRESSION, 'x and y')
        assert_parses(BOOLEAN_EXPRESSION, '(x = y) and false')

    def test_it_parses_boolean_keywords_with_boolean_operations(self):
        assert_parses(BOOLEAN_EXPRESSION, 'true and true')
        assert_parses(BOOLEAN_EXPRESSION, 'true and false')
        assert_parses(BOOLEAN_EXPRESSION, 'true AND FALSE')
        assert_parses(BOOLEAN_EXPRESSION, 'true Or false')
        assert_parses(BOOLEAN_EXPRESSION, 'true or (false AND TRUE)')
        assert_parses(BOOLEAN_EXPRESSION, 'not true')
        assert_parses(BOOLEAN_EXPRESSION, 'not (false and true)')


class TestCaseExpression:
    def test_it_parses_boolean_expressions_and_evaluates_to_identifiers(self):
        assert_parses(CASE_EXPRESSION, 'case when 1=1 then x end')

    def test_it_parses_boolean_expressions_and_evaluates_to_numbers(self):
        assert_parses(CASE_EXPRESSION, 'case when 1=1 then 7 end')

    def test_it_can_have_multiple_when_then_clauses(self):
        text = """
        case when p then q 
            when x then y
            when r then 5
            when t then u
        end
        """
        assert_parses(CASE_EXPRESSION, text)

    def test_it_has_an_optional_else_clause(self):
        text = """
        case when p then q 
            when x then y
        else 7
        end
        """
        assert_parses(CASE_EXPRESSION, text)


class TestParseSqlSelect:
    def test_select_star_parses(self):
        assert parse_sql('select * from hornswoggler;')

    def test_space_before_semicolon_parses(self):
        assert parse_sql("select * from hornswoggler ;")

    def test_two_selects_parses(self):
        assert parse_sql("select * from hornswoggler; select * from hornswoggler ;")

    def test_missing_column_name_list_raises_parse_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select from hornswoggler ;")

    def test_missing_table_name_starting_with_number_raises_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select * from 1hornswoggler ;")

    def test_missing_column_name_starting_with_int_raises_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select 1y from hornswoggler ;")

    def test_missing_column_name_starting_with_float_raises_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select 1.7y from hornswoggler ;")

    def test_missing_table_name_starting_with_underscore_raises_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select * from _hornswoggler ;")

    def test_missing_table_name_raises_parse_exception(self):
        with pytest.raises(ParseException):
            parse_sql("select * from  ;")

    def test_it_parses_select_distinct(self):
        assert parse_sql('select distinct this, that from hornswoggler;')

    def test_it_parses_select_all(self):
        assert parse_sql('select all this, that from hornswoggler;')

    def test_select_column_names_parses(self):
        assert parse_sql('select this, that from hornswoggler;')

    def test_select_number_literal_parses(self):
        assert parse_sql('select 1, that from hornswoggler;')

    def test_select_float_literal_parses(self):
        assert parse_sql('select 1.5, that from hornswoggler;')

    def test_select_column_names_without_spaces_parses(self):
        assert parse_sql('select this,that from hornswoggler;')

    def test_it_parses_arithmetic_expressions_as_columns(self):
        assert parse_sql('select (1+2), that from hornswoggler;')

    def test_it_parses_arithmetic_expressions_as_columns_with_alias(self):
        assert parse_sql('select 1+2 as three,that from hornswoggler;')

    def test_it_parses_quoted_sql_strings_as_columns(self):
        assert parse_sql("select 'hello',that from hornswoggler;")

    def test_it_parses_comparison_expressions_as_columns(self):
        assert parse_sql('select 1 > 2 as boop,that from hornswoggler;')

    def test_it_parses_boolean_expressions_as_columns(self):
        assert parse_sql('select 1 > 2 AND not x as boop,that from hornswoggler;')

    def test_it_parses_case_expressions_as_columns(self):
        assert parse_sql(
            'select case when x then y end as boop,that from hornswoggler;'
        )

    def test_it_does_not_require_a_from_clause(self):
        assert parse_sql('select 1;')

    def test_it_parses_function_expressions_as_columns(self):
        assert parse_sql('select current_time() as x,that from hornswoggler;')
        assert parse_sql('select current_time as x,that from hornswoggler;')

    def test_it_parses_unary_function_expressions_as_columns(self):
        assert parse_sql('select BITNOT(x) as x,that from hornswoggler;')

    def test_it_parses_binary_function_expressions_as_columns(self):
        assert parse_sql('select BITAND(x, y) as x,that from hornswoggler;')

    def test_it_parses_unary_function_expressions_with_optional_second_arg(self):
        assert parse_sql('select ABS(x) as x,that from hornswoggler;')
        assert parse_sql('select ABS(x, y) as x,that from hornswoggler;')


class TestParseSqlColumnAliases:
    def test_select_column_names_with_as_alias_parses(self):
        assert parse_sql('select quogwinkle as x from bip.boop.hornswoggler;')

    def test_select_column_names_with_non_as_alias_parses(self):
        assert parse_sql('select quogwinkle x from hornswoggler;')
