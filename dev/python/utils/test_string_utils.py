from python.utils.string_utils import *

class TestRedactSpacing:
    def test_redact_spacing_whitespace(self):
        assert redact_spacing("  ") == " "
    def test_redact_spacing_text_endings(self):
        assert redact_spacing("  text  ") == " text "
    def test_redact_spacing_between_text(self):
        assert redact_spacing("  text  text  ") == " text text "

class TestRedactOverflow:
    def test_redact_overflow_shorten(self):
        assert redact_overflow("abcdefghijklmnopqrstuvwxyz", 5) == "abcde..."
    def test_redact_overflow_same(self):
        assert redact_overflow("abcdefghijklmnopqrstuvwxyz", 100) == "abcdefghijklmnopqrstuvwxyz"

class TestRepeat:
    def test_repeat(self):
        assert repeat("abc", 3) == "abc\nabc\nabc"
    def test_repeat_no_separator(self):
        assert repeat("abc", 3, '') == "abcabcabc"
    def test_repeat_end(self):
        assert repeat("abc", 3, '', 'end') == "abcabcabcend"
    def test_repeat_end_newline(self):
        assert repeat("abc", 3, _end='end') == "abc\nabc\nabcend"
