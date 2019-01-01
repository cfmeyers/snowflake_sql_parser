from pyparsing import CaselessKeyword, Optional


def or_equals(expressions):
    final_expression = expressions[0]
    if len(expressions) > 1:
        for expression in expressions[1:]:
            final_expression = final_expression | expression
    return final_expression


def make_nullary_function_optional_parens(func_name):
    return CaselessKeyword(func_name) + Optional('()')


def make_nullary_function(func_name):
    return CaselessKeyword(func_name) + '()'


def make_nullary_function_with_optional_arg(func_name, EXPRESSION):
    return (
        CaselessKeyword(func_name) + '(' + Optional(EXPRESSION('arg_1_optional')) + ')'
    )


def make_unary_function(func_name, EXPRESSION):
    return CaselessKeyword(func_name) + '(' + EXPRESSION('arg_1') + ')'


def make_n_ary_function(func_name, arity, EXPRESSION, num_optional=0):
    func_expression = CaselessKeyword(func_name) + '('
    for arg_num in range(1, arity + 1):
        arg_name = 'arg_' + str(arg_num)
        func_expression += EXPRESSION(arg_name)
        if arg_num < arity:
            func_expression += ','
    for opt_num in range(1, num_optional + 1):
        func_expression += Optional(',' + EXPRESSION('optional_arg_' + str(arg_num)))
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
    CONTEXT_FUNCTION = or_equals(
        [make_nullary_function_optional_parens(f) for f in func_names]
    )

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


def make_unary_function_with_one_optional_arg(EXPRESSION):
    func_names = [
        'CEIL',
        'FLOOR',
        'ROUND',
        'TRUNCATE',
        'TRUNC',
        'INITCAP',
        'LTRIM',
        'PARSE_URL',
        'REPEAT',
        'RTRIM',
        'TRIM',
        'BASE64_DECODE_BINARY',
        'BASE64_DECODE_STRING',
        'HEX_ENCODE',
        'TRY_BASE64_DECODE_BINARY',
        'TRY_BASE64_DECODE_STRING',
        'SHA2',
        'SHA2_HEX',
        'SHA2_BINARY',
        'LAST_DAY',
        'TO_DATE',
        'TO_TIME',
        'TO_TIMESTAMP_LTZ',
        'TO_TIMESTAMP_NTZ',
        'TO_TIMESTAMP_TZ',
        'TO_CHAR',
        'TO_VARCHAR',
        'TO_BINARY',
        'TRY_TO_BINARY',
        'TO_DOUBLE',
        'SYSTEM$WAIT',
    ]
    return or_equals(
        [make_n_ary_function(f, 1, EXPRESSION, num_optional=1) for f in func_names]
    )


def make_unary_function_with_two_optional_args(EXPRESSION):
    func_names = ['BASE64_ENCODE', 'AS_DECIMAL', 'AS_NUMBER']
    return or_equals(
        [make_n_ary_function(f, 1, EXPRESSION, num_optional=2) for f in func_names]
    )


def make_unary_function_with_three_optional_args(EXPRESSION):
    func_names = [
        'TO_DECIMAL',
        'TO_NUMBER',
        'TO_NUMERIC',
        'TRY_TO_DECIMAL',
        'TRY_TO_NUMBER',
        'TRY_TO_NUMERIC',
    ]
    return or_equals(
        [make_n_ary_function(f, 1, EXPRESSION, num_optional=3) for f in func_names]
    )


def make_binary_function_expression(EXPRESSION):
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
        'CONCAT',
        'CONTAINS',
        'EDITDISTANCE',
        'ENDSWITH',
        'LEFT',
        'RIGHT',
        'SPLIT',
        'STARTSWITH',
        'DATE_PART',
        'NEXT_DAY',
        'PREVIOUS_DAY',
        'ADD_MONTHS',
        'DATE_TRUNC',
        'TRUNC',
        'ARRAY_APPEND',
        'ARRAY_CAT',
        'ARRAY_CONTAINS',
        'ARRAY_POSITION',
        'ARRAY_PREPEND',
        'ARRAY_TO_STRING',
        'ARRAYS_OVERLAP',
        'OBJECT_AGG',
        'GET',
        'GET_PATH',
        'GET_DDL',
        'RANDSTR',
    ]
    return or_equals([make_n_ary_function(f, 2, EXPRESSION) for f in func_names])


def make_binary_function_with_one_optional_args(EXPRESSION):
    func_names = [
        'CHARINDEX',
        'ILIKE',
        'LIKE',
        'LPAD',
        'PARSE_IP',
        'REPLACE',
        'RPAD',
        'SUBSTR',
        'SUBSTRING',
        'REGEXP_LIKE',
        'RLIKE',
        'CONVERT_TIMEZONE',
        'XMLGET',
    ]
    return or_equals(
        [make_n_ary_function(f, 2, EXPRESSION, num_optional=1) for f in func_names]
    )


def make_binary_function_with_two_optional_args(EXPRESSION):
    func_names = ['REGEXP_COUNT']
    return or_equals(
        [make_n_ary_function(f, 2, EXPRESSION, num_optional=2) for f in func_names]
    )


def make_binary_function_with_three_optional_args(EXPRESSION):
    func_names = ['REGEXP_SUBSTR']
    return or_equals(
        [make_n_ary_function(f, 2, EXPRESSION, num_optional=3) for f in func_names]
    )


def make_binary_function_with_four_optional_args(EXPRESSION):
    func_names = ['REGEXP_INSTR', 'REGEXP_REPLACE']
    return or_equals(
        [make_n_ary_function(f, 2, EXPRESSION, num_optional=4) for f in func_names]
    )


def make_trinary_function_expression(EXPRESSION):
    func_names = [
        'SPLIT_PART',
        'TRANSLATE',
        'DATE_FROM_PARTS',
        'DATEADD',
        'DATEDIFF',
        'TIMEADD',
        'TIMEDIFF',
        'TIMESTAMPADD',
        'TIMESTAMPDIFF',
        'ARRAY_INSERT',
        'ARRAY_SLICE',
        'NORMAL',
        'UNIFORM',
        'ZIPF',
    ]
    return or_equals([make_n_ary_function(f, 3, EXPRESSION) for f in func_names])


def make_trinary_function_with_one_optional_args(EXPRESSION):
    func_names = ['TIME_FROM_PARTS', 'OBJECT_INSERT']
    return or_equals(
        [make_n_ary_function(f, 3, EXPRESSION, num_optional=1) for f in func_names]
    )


def make_quaternary_function_expression(EXPRESSION):
    func_names = ['HAVERSINE', 'INSERT']
    return or_equals([make_n_ary_function(f, 4, EXPRESSION) for f in func_names])


def get_function_expression(EXPRESSION):

    return (
        # Nullary Function Expressions
        make_context_function_expression(EXPRESSION)
        | make_nullary_function('PI')
        | make_nullary_function_with_optional_arg('RANDOM', EXPRESSION)
        # Unary Function Expressions
        | make_unary_function_expression(EXPRESSION)
        | make_unary_function_with_one_optional_arg(EXPRESSION)
        | make_unary_function_with_two_optional_args(EXPRESSION)
        | make_unary_function_with_three_optional_args(EXPRESSION)
        # Binary Function Expressions
        | make_binary_function_expression(EXPRESSION)
        | make_binary_function_with_one_optional_args(EXPRESSION)
        | make_binary_function_with_two_optional_args(EXPRESSION)
        | make_binary_function_with_three_optional_args(EXPRESSION)
        | make_binary_function_with_four_optional_args(EXPRESSION)
        # Trinary Function Expressions
        | make_trinary_function_expression(EXPRESSION)
        | make_trinary_function_with_one_optional_args(EXPRESSION)
        # Quaternary Function Expressions
        | make_quaternary_function_expression(EXPRESSION)
    )
