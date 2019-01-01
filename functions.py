from pyparsing import CaselessKeyword, Optional

## Function Expressions
## End function expressions


def or_equals(expressions):
    final_expression = expressions[0]
    if len(expressions) > 1:
        for expression in expressions[1:]:
            final_expression = final_expression | expression
    return final_expression


def make_nullary_function(func_name):
    return CaselessKeyword(func_name) + Optional('()')


def make_nullary_function_manditory_parenthesis(func_name):
    return CaselessKeyword(func_name) + '()'


def make_nullary_function_with_optional_arg(func_name, EXPRESSION):
    return (
        CaselessKeyword(func_name) + '(' + Optional(EXPRESSION('arg_1_optional')) + ')'
    )


def make_unary_function(func_name, EXPRESSION):
    return CaselessKeyword(func_name) + '(' + EXPRESSION('arg_1') + ')'


def make_unary_function_with_optional_arg(func_name, EXPRESSION):
    return (
        CaselessKeyword(func_name)
        + '('
        + EXPRESSION('arg_1')
        + Optional(',' + EXPRESSION('arg_2_optional'))
        + ')'
    )


def make_function(func_name, arity, EXPRESSION):
    func_expression = CaselessKeyword(func_name) + '('
    for arg_num in range(1, arity + 1):
        arg_name = 'arg_' + str(arg_num)
        func_expression += EXPRESSION(arg_name)
        if arg_num < arity:
            func_expression += ','
    func_expression += ')'
    return func_expression


def make_context_function_expression(EXPRESSION):
    # Context functions take no args, can optionally be called without parentheses
    CONTEXT_FUNCTION = (
        make_nullary_function('CURRENT_CLIENT')
        | make_nullary_function('CURRENT_DATE')
        | make_nullary_function('CURRENT_TIME')
        | make_nullary_function('CURRENT_TIMESTAMP')
        | make_nullary_function('CURRENT_VERSION')
        | make_nullary_function('LOCALTIME')
        | make_nullary_function('LOCALTIMESTAMP')
        | make_nullary_function('CURRENT_ROLE')
        | make_nullary_function('CURRENT_SESSION')
        | make_nullary_function('CURRENT_STATEMENT')
        | make_nullary_function('CURRENT_TRANSACTION')
        | make_nullary_function('CURRENT_USER')
        | make_nullary_function('LAST_QUERY_ID')
        | make_nullary_function('LAST_TRANSACTION')
        | make_nullary_function('CURRENT_DATABASE')
        | make_nullary_function('CURRENT_SCHEMA')
        | make_nullary_function('CURRENT_SCHEMAS')
        | make_nullary_function('CURRENT_WAREHOUSE')
    )

    return CONTEXT_FUNCTION


def make_unary_function_expression(EXPRESSION):
    # Unary Functions
    UNARY_FUNCTION = (
        make_unary_function('BITAND_AGG', EXPRESSION)
        | make_unary_function('BITNOT', EXPRESSION)
        | make_unary_function('BITOR_AGG', EXPRESSION)
        | make_unary_function('BITXOR_AGG', EXPRESSION)
        | make_unary_function('SIGN', EXPRESSION)
        | make_unary_function('CBRT', EXPRESSION)
        | make_unary_function('EXP', EXPRESSION)
        | make_unary_function('FACTORIAL', EXPRESSION)
        | make_unary_function('SQRT', EXPRESSION)
        | make_unary_function('SQUARE', EXPRESSION)
        | make_unary_function('LN', EXPRESSION)
        | make_unary_function('ACOS', EXPRESSION)
        | make_unary_function('ACOSH', EXPRESSION)
        | make_unary_function('ASIN', EXPRESSION)
        | make_unary_function('ASINH', EXPRESSION)
        | make_unary_function('ATAN', EXPRESSION)
        | make_unary_function('ATAN2', EXPRESSION)
        | make_unary_function('ATANH', EXPRESSION)
        | make_unary_function('COS', EXPRESSION)
        | make_unary_function('COSH', EXPRESSION)
        | make_unary_function('COT', EXPRESSION)
        | make_unary_function('DEGREES', EXPRESSION)
        | make_unary_function('RADIANS', EXPRESSION)
        | make_unary_function('SIN', EXPRESSION)
        | make_unary_function('SINH', EXPRESSION)
        | make_unary_function('TAN', EXPRESSION)
        | make_unary_function('TANH', EXPRESSION)
        | make_unary_function('ASCII', EXPRESSION)
        | make_unary_function('BIT_LENGTH', EXPRESSION)
        | make_unary_function('CHR', EXPRESSION)
        | make_unary_function('CHAR', EXPRESSION)
        | make_unary_function('LENGTH', EXPRESSION)
        | make_unary_function('LOWER', EXPRESSION)
        | make_unary_function('OCTET_LENGTH', EXPRESSION)
        | make_unary_function('REVERSE', EXPRESSION)
        | make_unary_function('RTRIMMED_LENGTH', EXPRESSION)
        | make_unary_function('SPACE', EXPRESSION)
        | make_unary_function('UNICODE', EXPRESSION)
        | make_unary_function('UPPER', EXPRESSION)
        | make_unary_function('HEX_DECODE_BINARY', EXPRESSION)
        | make_unary_function('HEX_DECODE_STRING', EXPRESSION)
        | make_unary_function('TRY_HEX_DECODE_BINARY', EXPRESSION)
        | make_unary_function('TRY_HEX_DECODE_STRING', EXPRESSION)
        | make_unary_function('MD5', EXPRESSION)
        | make_unary_function('MD5_HEX', EXPRESSION)
        | make_unary_function('MD5_BINARY', EXPRESSION)
        | make_unary_function('MD5_NUMBER', EXPRESSION)
        | make_unary_function('SHA1', EXPRESSION)
        | make_unary_function('SHA1_HEX', EXPRESSION)
        | make_unary_function('SHA1_BINARY', EXPRESSION)
        | make_unary_function('DAYNAME', EXPRESSION)
        | make_unary_function('HOUR', EXPRESSION)
        | make_unary_function('MINUTE', EXPRESSION)
        | make_unary_function('SECOND', EXPRESSION)
        | make_unary_function('MONTHNAME', EXPRESSION)
        | make_unary_function('YEAR', EXPRESSION)
        | make_unary_function('YEAROFWEEK', EXPRESSION)
        | make_unary_function('YEAROFWEEKISO', EXPRESSION)
        | make_unary_function('DAY', EXPRESSION)
        | make_unary_function('DAYOFMONTH', EXPRESSION)
        | make_unary_function('DAYOFWEEK', EXPRESSION)
        | make_unary_function('DAYOFWEEKISO', EXPRESSION)
        | make_unary_function('DAYOFYEAR', EXPRESSION)
        | make_unary_function('WEEK', EXPRESSION)
        | make_unary_function('WEEKOFYEAR', EXPRESSION)
        | make_unary_function('WEEKISO', EXPRESSION)
        | make_unary_function('MONTH', EXPRESSION)
        | make_unary_function('QUARTER', EXPRESSION)
        | make_unary_function('CHECK_JSON', EXPRESSION)
        | make_unary_function('CHECK_XML', EXPRESSION)
        | make_unary_function('PARSE_JSON', EXPRESSION)
        | make_unary_function('PARSE_XML', EXPRESSION)
        | make_unary_function('STRIP_NULL_VALUE', EXPRESSION)
        | make_unary_function('ARRAY_COMPACT', EXPRESSION)
        | make_unary_function('ARRAY_SIZE', EXPRESSION)
        | make_unary_function('AS_ARRAY', EXPRESSION)
        | make_unary_function('AS_BINARY', EXPRESSION)
        | make_unary_function('AS_CHAR', EXPRESSION)
        | make_unary_function('AS_VARCHAR', EXPRESSION)
        | make_unary_function('AS_DATE', EXPRESSION)
        | make_unary_function('AS_DOUBLE', EXPRESSION)
        | make_unary_function('AS_REAL', EXPRESSION)
        | make_unary_function('AS_INTEGER', EXPRESSION)
        | make_unary_function('AS_OBJECT', EXPRESSION)
        | make_unary_function('AS_TIME', EXPRESSION)
        | make_unary_function('AS_TIMESTAMP_LTZ', EXPRESSION)
        | make_unary_function('AS_TIMESTAMP_NTZ', EXPRESSION)
        | make_unary_function('AS_TIMESTAMP_TZ', EXPRESSION)
        | make_unary_function('TO_ARRAY', EXPRESSION)
        | make_unary_function('TO_JSON', EXPRESSION)
        | make_unary_function('TO_OBJECT', EXPRESSION)
        | make_unary_function('TO_VARIANT', EXPRESSION)
        | make_unary_function('TO_XML', EXPRESSION)
        | make_unary_function('IS_ARRAY', EXPRESSION)
        | make_unary_function('IS_BINARY', EXPRESSION)
        | make_unary_function('IS_BOOLEAN', EXPRESSION)
        | make_unary_function('IS_CHAR', EXPRESSION)
        | make_unary_function('IS_VARCHAR', EXPRESSION)
        | make_unary_function('IS_DATE', EXPRESSION)
        | make_unary_function('IS_DATE_VALUE', EXPRESSION)
        | make_unary_function('IS_DECIMAL', EXPRESSION)
        | make_unary_function('IS_DOUBLE', EXPRESSION)
        | make_unary_function('IS_REAL', EXPRESSION)
        | make_unary_function('IS_INTEGER', EXPRESSION)
        | make_unary_function('IS_NULL_VALUE', EXPRESSION)
        | make_unary_function('IS_OBJECT', EXPRESSION)
        | make_unary_function('IS_TIME', EXPRESSION)
        | make_unary_function('IS_TIMESTAMP_LTZ', EXPRESSION)
        | make_unary_function('IS_TIMESTAMP_NTZ', EXPRESSION)
        | make_unary_function('IS_TIMESTAMP_TZ', EXPRESSION)
        | make_unary_function('TYPEOF', EXPRESSION)
        | make_unary_function('TRY_TO_DOUBLE', EXPRESSION)
        | make_unary_function('TO_BOOLEAN', EXPRESSION)
        | make_unary_function('TRY_TO_BOOLEAN', EXPRESSION)
        | make_unary_function('TRY_TO_DATE', EXPRESSION)
        | make_unary_function('TRY_TO_TIME', EXPRESSION)
        | make_unary_function('TRY_TO_TIMESTAMP', EXPRESSION)
        | make_unary_function('TRY_TO_TIMESTAMP_LTZ', EXPRESSION)
        | make_unary_function('TRY_TO_TIMESTAMP_NTZ', EXPRESSION)
        | make_unary_function('TRY_TO_TIMESTAMP_TZ', EXPRESSION)
        | make_unary_function('SYSTEM$ABORT_SESSION', EXPRESSION)
        | make_unary_function('SYSTEM$ABORT_TRANSACTION', EXPRESSION)
        | make_unary_function('SYSTEM$CANCEL_ALL_QUERIES', EXPRESSION)
        | make_unary_function('SYSTEM$CANCEL_QUERY', EXPRESSION)
        | make_unary_function('SYSTEM$LAST_CHANGE_COMMIT_TIME', EXPRESSION)
        | make_unary_function('SYSTEM$PIPE_FORCE_RESUME', EXPRESSION)
        | make_unary_function('SYSTEM$PIPE_STATUS', EXPRESSION)
        | make_unary_function('SYSTEM$TYPEOF', EXPRESSION)
        | make_unary_function('SEQ1', EXPRESSION)
        | make_unary_function('SEQ2', EXPRESSION)
        | make_unary_function('SEQ4', EXPRESSION)
        | make_unary_function('SEQ8', EXPRESSION)
    )

    return UNARY_FUNCTION


def make_binary_function_expression(EXPRESSION):
    # Binary Functions
    BINARY_FUNCTION = (
        make_function('BITAND', 2, EXPRESSION)
        | make_function('BITOR', 2, EXPRESSION)
        | make_function('BITSHIFTLEFT', 2, EXPRESSION)
        | make_function('BITSHIFTRIGHT', 2, EXPRESSION)
        | make_function('BITXOR', 2, EXPRESSION)
        | make_function('MOD', 2, EXPRESSION)
        | make_function('POW', 2, EXPRESSION)
        | make_function('POWER', 2, EXPRESSION)
        | make_function('LOG', 2, EXPRESSION)
    )

    return BINARY_FUNCTION


def make_unary_function_with_optional_arg_expression(EXPRESSION):
    UNARY_FUNCTION_WITH_OPTIONAL_ARG = (
        make_unary_function_with_optional_arg('ABS', EXPRESSION)
        | make_unary_function_with_optional_arg('CEIL', EXPRESSION)
        | make_unary_function_with_optional_arg('FLOOR', EXPRESSION)
        | make_unary_function_with_optional_arg('ROUND', EXPRESSION)
        | make_unary_function_with_optional_arg('TRUNCATE', EXPRESSION)
        | make_unary_function_with_optional_arg('TRUNC', EXPRESSION)
    )

    return UNARY_FUNCTION_WITH_OPTIONAL_ARG


def get_function_expression(EXPRESSION):
    CONTEXT_FUNCTION = make_context_function_expression(EXPRESSION)

    PI = make_nullary_function_manditory_parenthesis('PI')
    NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES = PI

    RANDOM = make_nullary_function_with_optional_arg('RANDOM', EXPRESSION)
    NULLARY_FUNCTION_WITH_OPTIONAL_ARG = RANDOM

    UNARY_FUNCTION = make_unary_function_expression(EXPRESSION)
    BINARY_FUNCTION = make_binary_function_expression(EXPRESSION)

    # Quaternary Functions
    HAVERSINE = make_function('HAVERSINE', 4, EXPRESSION)
    QUATERNARY_FUNCTION = HAVERSINE

    UNARY_FUNCTION_WITH_OPTIONAL_ARG = make_unary_function_with_optional_arg_expression(
        EXPRESSION
    )

    FUNCTION_EXPRESSION = (
        CONTEXT_FUNCTION
        | UNARY_FUNCTION
        | BINARY_FUNCTION
        | UNARY_FUNCTION_WITH_OPTIONAL_ARG
        | QUATERNARY_FUNCTION
        | NULLARY_FUNCTION_WITH_MANDATORY_PARENTHESES
        | NULLARY_FUNCTION_WITH_OPTIONAL_ARG
    )
    return FUNCTION_EXPRESSION
