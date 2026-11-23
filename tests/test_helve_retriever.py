import os
import unittest
from importlib.metadata import entry_points
from unittest.mock import MagicMock, patch

from gpt_researcher_helve import HelveSearch


class HelveRetrieverTests(unittest.TestCase):
    @patch("gpt_researcher_helve.helve.requests.post")
    def test_normalizes_snippets_and_skips_malformed(self, mock_post):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {
            "id": "srch_1",
            "provider": "fusion",
            "results": [
                {"url": "https://a.example", "snippets": ["Part 1", "Part 2"]},
                {"snippets": ["missing url"]},
                "bad-entry",
                {"url": "https://b.example", "summary": "Summary B"},
                {"url": "https://c.example", "full_text": "Full C"},
            ],
        }
        mock_post.return_value = resp
        with patch.dict(os.environ, {"HELVE_API_KEY": "sk_live_test"}):
            out = HelveSearch(
                "ai agents",
                headers={"helve_provider": "fusion"},
                query_domains=["docs.python.org"],
            ).search(max_results=10)

        self.assertEqual(
            out,
            [
                {"href": "https://a.example", "body": "Part 1\nPart 2"},
                {"href": "https://b.example", "body": "Summary B"},
                {"href": "https://c.example", "body": "Full C"},
            ],
        )
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["provider"], "fusion")
        self.assertEqual(kwargs["json"]["include_domains"], ["docs.python.org"])

    def test_missing_api_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(Exception) as ctx:
                HelveSearch("q")
        self.assertIn("HELVE_API_KEY", str(ctx.exception))

    @patch("gpt_researcher_helve.helve.requests.post")
    def test_error_returns_empty(self, mock_post):
        mock_post.side_effect = Exception("network error")
        with patch.dict(os.environ, {"HELVE_API_KEY": "sk_live_test"}):
            self.assertEqual(HelveSearch("q").search(), [])


if __name__ == "__main__":
    unittest.main()
