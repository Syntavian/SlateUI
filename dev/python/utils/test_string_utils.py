from python.utils.string_utils import redact_spacing

class TestRedactSpacing:
    def test_redact_spacing_whitespace(self):
        assert redact_spacing("  ") == " "
    def test_redact_spacing_text_endings(self):
        assert redact_spacing("  text  ") == " text "
    def test_redact_spacing_between_text(self):
        assert redact_spacing("  text  text  ") == " text text "
