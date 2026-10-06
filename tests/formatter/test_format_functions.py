# pylint: skip-file
# type: ignore
#
#       tests.formatter.test_format_functions.py is part of the docformatter project
#
# Copyright (C) 2012-2023 Steven Myint
# Copyright (C) 2023-2025 Doyle "weibullguy" Rowland
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module for testing formatting functions."""

# Standard Library Imports
import contextlib
import sys
import tokenize
from io import BytesIO, StringIO

with contextlib.suppress(ImportError):
    if sys.version_info >= (3, 11):
        # Standard Library Imports
        import tomllib
    else:
        # Third Party Imports
        import tomli as tomllib

# Third Party Imports
import pytest

# docformatter Package Imports
from docformatter import format as _format

with open("tests/_data/string_files/format_functions.toml", "rb") as f:
    TEST_STRINGS = tomllib.load(f)


def _get_tokens(source):
    return list(tokenize.tokenize(BytesIO(source.encode()).readline))


def _get_docstring_token_and_index(tokens):
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.STRING:
            return i
    raise ValueError("No docstring found in token stream.")


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "module_docstring_followed_by_string",
        "module_docstring_followed_by_code",
        "module_docstring_followed_by_comment_then_code",
        "module_docstring_followed_by_comment_then_string",
        "module_docstring_in_black",
        "module_docstring_followed_by_def",
        "module_docstring_followed_by_class",
        "module_docstring_followed_by_decorated_def",
    ],
)
def test_module_docstring_newlines(test_key):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = _get_tokens(source)
    index = _get_docstring_token_and_index(tokens)

    result = _format._get_module_docstring_newlines(tokens, index)
    assert (
        result == expected
    ), f"\nFailed {test_key}:\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "test_key, classifier",
    [
        (
            "class_docstring_followed_by_statement",
            _format._get_class_docstring_newlines,
        ),
        ("class_docstring_followed_by_def", _format._get_class_docstring_newlines),
        ("class_docstring_with_decorator", _format._get_class_docstring_newlines),
        ("class_docstring_with_class_variable", _format._get_class_docstring_newlines),
        ("function_with_expr", _format._get_function_docstring_newlines),
        ("function_with_inner_def", _format._get_function_docstring_newlines),
        ("function_with_inner_async_def", _format._get_function_docstring_newlines),
        ("function_with_decorator_and_def", _format._get_function_docstring_newlines),
        (
            "function_with_decorator_and_async_def",
            _format._get_function_docstring_newlines,
        ),
        (
            "function_docstring_with_inner_class",
            _format._get_function_docstring_newlines,
        ),
        ("attribute_docstring_single_line", _format._get_attribute_docstring_newlines),
        ("attribute_docstring_multi_line", _format._get_attribute_docstring_newlines),
        (
            "attribute_docstring_outside_class",
            _format._get_attribute_docstring_newlines,
        ),
        (
            "attribute_docstring_inside_method",
            _format._get_attribute_docstring_newlines,
        ),
        ("attribute_docstring_with_comment", _format._get_attribute_docstring_newlines),
        (
            "attribute_docstring_multiple_assignments",
            _format._get_attribute_docstring_newlines,
        ),
        ("attribute_docstring_equiv_expr", _format._get_attribute_docstring_newlines),
    ],
)
def test_get_docstring_newlines(test_key, classifier):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = _get_tokens(source)
    index = _get_docstring_token_and_index(tokens)

    result = classifier(tokens, index)
    assert (
        result == expected
    ), f"\nFailed {test_key}:\nExpected {expected}\nGot {result}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "get_num_rows_columns",
    ],
)
def test_get_num_rows_columns(test_key):
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_num_rows_columns(token)
    assert (
        result[0] == expected[0]
    ), f"\nFailed {test_key}\nExpected {expected[0]} rows\nGot {result[0]} rows"
    assert (
        result[1] == expected[1]
    ), f"\nFailed {test_key}\nExpected {expected[1]} columns\nGot {result[1]} columns"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key",
    [
        "get_start_end_indices",
    ],
)
def test_get_start_end_indices(test_key):
    prev_token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["prev_token"][0],
        string=TEST_STRINGS[test_key]["prev_token"][1],
        start=TEST_STRINGS[test_key]["prev_token"][2],
        end=TEST_STRINGS[test_key]["prev_token"][3],
        line=TEST_STRINGS[test_key]["prev_token"][4],
    )
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_start_end_indices(token, prev_token, 3, 17)
    for i in 0, 1:
        for j in 0, 1:
            assert (
                result[i][j] == expected[i][j]
            ), f"\nFailed {test_key}\nExpected {expected[i][j]}\nGot {result[i][j]}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "test_key, block",
    [
        ("do_remove_preceding_blank_lines_module", [(0, 4, "module")]),
        ("do_remove_preceding_blank_lines_class", [(0, 7, "class")]),
        ("do_remove_preceding_blank_lines_function", [(0, 9, "function")]),
        ("do_remove_preceding_blank_lines_attribute", [(1, 6, "attribute")]),
    ],
)
def test_do_remove_preceding_blank_lines(test_key, block):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = list(tokenize.generate_tokens(StringIO(source, newline="").readline))

    result = _format._do_remove_preceding_blank_lines(tokens, block)
    for _idx in range(len(result)):
        assert (
            result[_idx].string == expected[_idx]
        ), f"\nFailed {test_key}\nExpected {expected[_idx]}\nGot {result[_idx].string}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key",
    [
        "get_newlines_by_type_module_docstring",
        "get_newlines_by_type_module_docstring_black",
        "get_newlines_by_type_class_docstring",
        "get_newlines_by_type_function_docstring",
        "get_newlines_by_type_attribute_docstring",
    ],
)
def test_get_newlines_by_type(test_key):
    source = TEST_STRINGS[test_key]["source"]
    expected = TEST_STRINGS[test_key]["expected"]

    tokens = _get_tokens(source)
    index = _get_docstring_token_and_index(tokens)

    result = _format._get_newlines_by_type(tokens, index)
    assert result == expected, f"\nFailed {test_key}\nExpected {expected}\nGot {result}"


@pytest.mark.unit
def test_get_char_col_from_byte_col():
    """Convert UTF-8 byte offsets to character indices, or None off-boundary."""
    # "┘" is one character and three bytes.
    text = 'a┘."""\n'

    assert _format._get_char_col_from_byte_col(text, 0) == 0
    assert _format._get_char_col_from_byte_col(text, 1) == 1
    assert _format._get_char_col_from_byte_col(text, 4) == 2
    assert _format._get_char_col_from_byte_col(text, 9) == len(text)
    assert _format._get_char_col_from_byte_col(text, 2) is None
    assert _format._get_char_col_from_byte_col(text, 99) is None


@pytest.mark.unit
def test_do_normalize_token_columns_fixes_newline_after_multibyte_string():
    """Convert a byte-based NEWLINE column so no blank line is inserted.

    Mirrors CPython 3.12.4 (python/cpython#120343): the docstring ends at
    character column 30 but the NEWLINE that follows starts at byte column 32.
    """
    docstring = (
        '"""Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
        '    aaaaaaaaaaaaaaaaaaaaa┘."""'
    )
    closing_line = '    aaaaaaaaaaaaaaaaaaaaa┘."""\n'
    tokens = [
        tokenize.TokenInfo(
            tokenize.STRING, docstring, (2, 4), (3, 30), f"    {docstring}\n"
        ),
        tokenize.TokenInfo(tokenize.NEWLINE, "\n", (3, 32), (3, 33), closing_line),
    ]

    result = _format._do_normalize_token_columns(tokens)

    assert result[0] == tokens[0]
    assert result[1].start == (3, 30)
    assert result[1].end == (3, 31)
    assert result[1].string == "\n"


@pytest.mark.unit
def test_do_normalize_token_columns_fixes_comment_after_multibyte_string():
    """Convert a byte-based COMMENT column so the comment is not duplicated."""
    closing_line = '    Trailing ┘."""  # keep me\n'
    comment_char_col = closing_line.index("#")
    comment_byte_col = len(closing_line[:comment_char_col].encode("utf-8"))
    assert comment_byte_col == comment_char_col + 2

    tokens = [
        tokenize.TokenInfo(
            tokenize.COMMENT,
            "# keep me",
            (4, comment_byte_col),
            (4, comment_byte_col + len("# keep me")),
            closing_line,
        ),
    ]

    result = _format._do_normalize_token_columns(tokens)

    assert result[0].start == (4, comment_char_col)
    assert result[0].end == (4, comment_char_col + len("# keep me"))


@pytest.mark.unit
def test_do_normalize_token_columns_is_noop_for_consistent_tokens():
    """Tokens whose columns already index their text are returned unchanged.

    Single-line non-ASCII is tokenized correctly on every supported Python, so
    this input must come back identical everywhere.
    """
    source = 'x = "┘"  # c\nif True:\n    """Doc.\n\n    More.\n    """\n    y = 2\n'
    tokens = list(tokenize.generate_tokens(StringIO(source).readline))

    result = _format._do_normalize_token_columns(tokens)

    assert result == tokens


@pytest.mark.unit
def test_do_normalize_token_columns_restores_invariant_for_real_tokens():
    """Every single-row token indexes its own text after normalization.

    On CPython 3.12.4 the tokenizer breaks this for the tokens after the
    multiline string; elsewhere the input is already consistent.  Either way
    the invariant must hold afterwards.
    """
    source = (
        'def foo():\n    """Summary.\n\n    Trailing ┘."""  # keep me\n    return 1\n'
    )
    tokens = list(tokenize.generate_tokens(StringIO(source).readline))

    result = _format._do_normalize_token_columns(tokens)

    for token in result:
        if token.start[0] == token.end[0] and token.type != tokenize.ENDMARKER:
            assert token.line[token.start[1] : token.end[1]] == token.string


@pytest.mark.unit
def test_do_normalize_token_columns_leaves_unfixable_tokens_alone():
    """A column that cannot be matched to the token text is left as it was."""
    line = "x = 1\n"
    bad = tokenize.TokenInfo(tokenize.NAME, "zzz", (1, 4), (1, 7), line)

    result = _format._do_normalize_token_columns([bad])

    assert result == [bad]


@pytest.mark.integration
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "test_key",
    [
        "get_unmatched_start_end_indices",
    ],
)
def test_get_unmatched_start_end_indices(test_key):
    prev_token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["prev_token"][0],
        string=TEST_STRINGS[test_key]["prev_token"][1],
        start=TEST_STRINGS[test_key]["prev_token"][2],
        end=TEST_STRINGS[test_key]["prev_token"][3],
        line=TEST_STRINGS[test_key]["prev_token"][4],
    )
    token = tokenize.TokenInfo(
        type=TEST_STRINGS[test_key]["token"][0],
        string=TEST_STRINGS[test_key]["token"][1],
        start=TEST_STRINGS[test_key]["token"][2],
        end=TEST_STRINGS[test_key]["token"][3],
        line=TEST_STRINGS[test_key]["token"][4],
    )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._get_unmatched_start_end_indices(token, prev_token, 4)
    for i in 0, 1:
        for j in 0, 1:
            assert (
                result[i][j] == expected[i][j]
            ), f"\nFailed {test_key}\nExpected {expected[i][j]}\nGot {result[i][j]}"


@pytest.mark.integration
@pytest.mark.order(5)
@pytest.mark.parametrize(
    "test_key",
    [
        "do_update_token_indices",
    ],
)
def test_do_update_token_indices(test_key):
    tokens = []
    for token in TEST_STRINGS[test_key]["tokens"]:
        tokens.append(
            tokenize.TokenInfo(
                type=token[0],
                string=token[1],
                start=token[2],
                end=token[3],
                line=token[4],
            )
        )
    expected = TEST_STRINGS[test_key]["expected"]

    result = _format._do_update_token_indices(tokens)
    for idx, _expected in enumerate(expected):
        # We convert the start and end tuples to lists because we can't store tuples
        # in a TOML file.
        assert list(result[idx].start) == _expected[0], (
            f"\nFailed {test_key} start index\n"
            f"Expected {expected[0]}\nGot {result[idx].start}"
        )
        assert list(result[idx].end) == _expected[1], (
            f"\nFailed {test_key} end index\n"
            f"Expected {expected[1]}\nGot {result[idx].end}"
        )
