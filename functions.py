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
    func_names = [
        'CURRENT_CLIENT',
        'CURRENT_DATE',
        'CURRENT_TIME',
        'CURRENT_TIMESTAMP',
        'CURRENT_VERSION',
        'LOCALTIME',
        'LOCALTIMESTAMP',
        'CURRENT_ROLE',
        'CURRENT_SESSION',
        'CURRENT_STATEMENT',
        'CURRENT_TRANSACTION',
        'CURRENT_USER',
        'LAST_QUERY_ID',
        'LAST_TRANSACTION',
        'CURRENT_DATABASE',
        'CURRENT_SCHEMA',
        'CURRENT_SCHEMAS',
        'CURRENT_WAREHOUSE',
    ]
    CONTEXT_FUNCTION = or_equals([make_nullary_function(f) for f in func_names])

    return CONTEXT_FUNCTION


def make_unary_function_expression(EXPRESSION):
    # Unary Functions
    func_names = [
        'BITAND_AGG',
        'BITNOT',
        'BITOR_AGG',
        'BITXOR_AGG',
        'SIGN',
        'CBRT',
        'EXP',
        'FACTORIAL',
        'SQRT',
        'SQUARE',
        'LN',
        'ACOS',
        'ACOSH',
        'ASIN',
        'ASINH',
        'ATAN',
        'ATAN2',
        'ATANH',
        'COS',
        'COSH',
        'COT',
        'DEGREES',
        'RADIANS',
        'SIN',
        'SINH',
        'TAN',
        'TANH',
        'ASCII',
        'BIT_LENGTH',
        'CHR',
        'CHAR',
        'LENGTH',
        'LOWER',
        'OCTET_LENGTH',
        'REVERSE',
        'RTRIMMED_LENGTH',
        'SPACE',
        'UNICODE',
        'UPPER',
        'HEX_DECODE_BINARY',
        'HEX_DECODE_STRING',
        'TRY_HEX_DECODE_BINARY',
        'TRY_HEX_DECODE_STRING',
        'MD5',
        'MD5_HEX',
        'MD5_BINARY',
        'MD5_NUMBER',
        'SHA1',
        'SHA1_HEX',
        'SHA1_BINARY',
        'DAYNAME',
        'HOUR',
        'MINUTE',
        'SECOND',
        'MONTHNAME',
        'YEAR',
        'YEAROFWEEK',
        'YEAROFWEEKISO',
        'DAY',
        'DAYOFMONTH',
        'DAYOFWEEK',
        'DAYOFWEEKISO',
        'DAYOFYEAR',
        'WEEK',
        'WEEKOFYEAR',
        'WEEKISO',
        'MONTH',
        'QUARTER',
        'CHECK_JSON',
        'CHECK_XML',
        'PARSE_JSON',
        'PARSE_XML',
        'STRIP_NULL_VALUE',
        'ARRAY_COMPACT',
        'ARRAY_SIZE',
        'AS_ARRAY',
        'AS_BINARY',
        'AS_CHAR',
        'AS_VARCHAR',
        'AS_DATE',
        'AS_DOUBLE',
        'AS_REAL',
        'AS_INTEGER',
        'AS_OBJECT',
        'AS_TIME',
        'AS_TIMESTAMP_LTZ',
        'AS_TIMESTAMP_NTZ',
        'AS_TIMESTAMP_TZ',
        'TO_ARRAY',
        'TO_JSON',
        'TO_OBJECT',
        'TO_VARIANT',
        'TO_XML',
        'IS_ARRAY',
        'IS_BINARY',
        'IS_BOOLEAN',
        'IS_CHAR',
        'IS_VARCHAR',
        'IS_DATE',
        'IS_DATE_VALUE',
        'IS_DECIMAL',
        'IS_DOUBLE',
        'IS_REAL',
        'IS_INTEGER',
        'IS_NULL_VALUE',
        'IS_OBJECT',
        'IS_TIME',
        'IS_TIMESTAMP_LTZ',
        'IS_TIMESTAMP_NTZ',
        'IS_TIMESTAMP_TZ',
        'TYPEOF',
        'TRY_TO_DOUBLE',
        'TO_BOOLEAN',
        'TRY_TO_BOOLEAN',
        'TRY_TO_DATE',
        'TRY_TO_TIME',
        'TRY_TO_TIMESTAMP',
        'TRY_TO_TIMESTAMP_LTZ',
        'TRY_TO_TIMESTAMP_NTZ',
        'TRY_TO_TIMESTAMP_TZ',
        'SYSTEM$ABORT_SESSION',
        'SYSTEM$ABORT_TRANSACTION',
        'SYSTEM$CANCEL_ALL_QUERIES',
        'SYSTEM$CANCEL_QUERY',
        'SYSTEM$LAST_CHANGE_COMMIT_TIME',
        'SYSTEM$PIPE_FORCE_RESUME',
        'SYSTEM$PIPE_STATUS',
        'SYSTEM$TYPEOF',
        'SEQ1',
        'SEQ2',
        'SEQ4',
        'SEQ8',
    ]
    UNARY_FUNCTION = or_equals([make_unary_function(f, EXPRESSION) for f in func_names])

    return UNARY_FUNCTION


def make_binary_function_expression(EXPRESSION):
    # Binary Functions

    func_names = [
        'BITAND',
        'BITOR',
        'BITSHIFTLEFT',
        'BITSHIFTRIGHT',
        'BITXOR',
        'MOD',
        'POW',
        'POWER',
        'LOG',
    ]
    BINARY_FUNCTION = or_equals([make_function(f, 2, EXPRESSION) for f in func_names])

    return BINARY_FUNCTION


def make_unary_function_with_optional_arg_expression(EXPRESSION):
    func_names = ['ABS', 'CEIL', 'FLOOR', 'ROUND', 'TRUNCATE', 'TRUNC']
    UNARY_FUNCTION_WITH_OPTIONAL_ARG = or_equals(
        [make_unary_function_with_optional_arg(f, EXPRESSION) for f in func_names]
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
