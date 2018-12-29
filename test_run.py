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
)


class TestQuotedString:
    def test_it_can_be_the_empty_string(self):
        assert QUOTED_SQL_STRING.parseString("''", parseAll=True)

    def test_it_can_be_a_string_of_ascii(self):
        assert QUOTED_SQL_STRING.parseString("'hello'", parseAll=True)

    def test_it_can_be_a_string_with_a_space(self):
        assert QUOTED_SQL_STRING.parseString("'hello world'", parseAll=True)

    def test_it_can_have_non_identifier_characters(self):
        assert QUOTED_SQL_STRING.parseString("'hello-world'", parseAll=True)
        assert QUOTED_SQL_STRING.parseString("'hello~world'", parseAll=True)
        assert QUOTED_SQL_STRING.parseString("'hello/world'", parseAll=True)
        assert QUOTED_SQL_STRING.parseString("'hello..world'", parseAll=True)
        assert QUOTED_SQL_STRING.parseString("'he&*()#@-rld'", parseAll=True)

    def test_it_must_be_surrounded_in_quotes(self):
        with pytest.raises(ParseException):
            assert QUOTED_SQL_STRING.parseString("hello", parseAll=True)

    def test_it_must_start_with_a_single_quote(self):
        with pytest.raises(ParseException):
            assert QUOTED_SQL_STRING.parseString("'hello", parseAll=True)

    def test_it_must_end_with_a_single_quote(self):
        with pytest.raises(ParseException):
            assert QUOTED_SQL_STRING.parseString("hello'", parseAll=True)

    def test_it_does_not_use_double_quotes(self):
        with pytest.raises(ParseException):
            assert QUOTED_SQL_STRING.parseString('"hello"', parseAll=True)


class TestArithmeticExpression:
    def test_it_parses_operands_that_are_numeric(self):
        assert ARITHMETIC_EXPRESSION.parseString('1+1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1 +1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1 + 1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1+ 1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1-1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1*1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1/1', parseAll=True)

    def test_it_parses_operands_that_are_identifiers(self):
        assert ARITHMETIC_EXPRESSION.parseString('x+y', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('1+y', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('x+1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('x-1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('x*1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('x/1', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('x%1', parseAll=True)

    def test_it_parses_operands_that_are_expressions(self):
        assert ARITHMETIC_EXPRESSION.parseString('(x+y)+z', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('(x-y)+z', parseAll=True)
        assert ARITHMETIC_EXPRESSION.parseString('(x-y)-z', parseAll=True)

    def test_it_parses_negative_operands(self):
        assert ARITHMETIC_EXPRESSION.parseString('-1', parseAll=True)

    def test_it_allows_for_parenthesis_surrounding_arithmetic_expression(self):
        assert ARITHMETIC_EXPRESSION.parseString('(x+y)', parseAll=True)

    def test_a_single_number_is_an_expression(self):
        assert ARITHMETIC_EXPRESSION.parseString('1', parseAll=True)

    def test_a_single_identifier_is_an_expression(self):
        assert ARITHMETIC_EXPRESSION.parseString('x', parseAll=True)

    def test_addition_requires_2_parentheses_or_none_at_all(self):
        with pytest.raises(ParseException):
            assert ARITHMETIC_EXPRESSION.parseString('(1 + 1', parseAll=True)
        with pytest.raises(ParseException):
            assert ARITHMETIC_EXPRESSION.parseString('1 + 1)', parseAll=True)


class TestComparisonExpression:
    def test_it_parses_operands_that_are_numeric(self):
        assert COMPARISON_EXPRESSION.parseString('1=1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1!=1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 != 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 <> 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 > 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 < 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 < 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 <= 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('1 >= 1', parseAll=True)
        assert COMPARISON_EXPRESSION.parseString('(2+2) >= 1', parseAll=True)

    def test_it_parses_operands_that_are_identifiers(self):
        assert COMPARISON_EXPRESSION.parseString('x=1', parseAll=True)

    def test_a_comparison_requires_two_operands(self):
        with pytest.raises(ParseException):
            assert COMPARISON_EXPRESSION.parseString('1 >=', parseAll=True)
        with pytest.raises(ParseException):
            assert COMPARISON_EXPRESSION.parseString('1=', parseAll=True)


class TestBooleanExpression:
    def test_it_parses_boolean_keywords(self):
        assert BOOLEAN_EXPRESSION.parseString('true', parseAll=True)
        assert BOOLEAN_EXPRESSION.parseString('TRUE', parseAll=True)
        assert BOOLEAN_EXPRESSION.parseString('True', parseAll=True)
        assert BOOLEAN_EXPRESSION.parseString('False', parseAll=True)
        assert BOOLEAN_EXPRESSION.parseString('FALSE', parseAll=True)
        assert BOOLEAN_EXPRESSION.parseString('False', parseAll=True)


class TestIdentifier:
    def test_it_can_be_just_letters(self):
        assert IDENTIFIER.parseString('foodlion', parseAll=True)

    def test_it_can_be_initial_letter_then_digits(self):
        assert IDENTIFIER.parseString('x11', parseAll=True)

    def test_it_can_be_initial_letter_then_underscore(self):
        assert IDENTIFIER.parseString('x11_version2', parseAll=True)

    def test_it_cannot_start_with_a_digit(self):
        with pytest.raises(ParseException):
            assert IDENTIFIER.parseString('1', parseAll=True)

    def test_it_cannot_start_with_an_underscore(self):
        with pytest.raises(ParseException):
            assert IDENTIFIER.parseString('_x', parseAll=True)

    def test_it_cannot_be_a_keyword(self):
        keywords = ['select', 'from', 'where']
        for keyword in keywords:
            with pytest.raises(ParseException):
                assert IDENTIFIER.parseString(keyword, parseAll=True)

    def test_it_cannot_have_a_dot(self):
        with pytest.raises(ParseException):
            assert IDENTIFIER.parseString('hello.world', parseAll=True)


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

    def test_select_column_names_parses(self):
        assert parse_sql('select this, that from hornswoggler;')

    def test_select_number_literal_parses(self):
        assert parse_sql('select 1, that from hornswoggler;')

    def test_select_float_literal_parses(self):
        assert parse_sql('select 1.5, that from hornswoggler;')

    def test_select_column_names_without_spaces_parses(self):
        assert parse_sql('select this,that from hornswoggler;')

    def test_select_parses_arithmetic_expressions_as_columns(self):
        assert parse_sql('select (1+2), that from hornswoggler;')

    def test_select_parses_arithmetic_expressions_as_columns_with_alias(self):
        assert parse_sql('select 1+2 as three,that from hornswoggler;')

    def test_select_parses_quoted_sql_strings_as_columns(self):
        assert parse_sql("select 'hello',that from hornswoggler;")


class TestParseSqlColumnAliases:
    def test_select_column_names_with_as_alias_parses(self):
        assert parse_sql('select quogwinkle as x from hornswoggler;')

    def test_select_column_names_with_non_as_alias_parses(self):
        assert parse_sql('select quogwinkle x from hornswoggler;')
