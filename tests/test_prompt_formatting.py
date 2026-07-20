import unittest

from config.prompt import REQUIREMENT_ANALYSIS_AGENT_PROMPT, format_prompt


class PromptFormattingTests(unittest.TestCase):
    def test_replaces_real_placeholders_and_keeps_literal_json_braces(self):
        result = format_prompt(
            REQUIREMENT_ANALYSIS_AGENT_PROMPT,
            user_input="find me jobs for software developer and AI",
            history="[]",
        )

        self.assertIn("find me jobs for software developer and AI", result)
        self.assertIn('"event": "<selected_event>"', result)
        self.assertNotIn("{user_input}", result)
        self.assertNotIn("{history}", result)

    def test_raises_key_error_for_missing_placeholder(self):
        with self.assertRaises(KeyError):
            format_prompt("Hello {name}", user_input="value")


if __name__ == "__main__":
    unittest.main()
