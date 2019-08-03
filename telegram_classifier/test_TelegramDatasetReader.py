from unittest import TestCase
import json
from telegram_classifier.telegram_reader import normalize_message_text


class TestTelegramDatasetReader(TestCase):
    def test_normalizeMessageText(self):
        self.normalizeTest("""
                [
               {
                "type": "mention_name",
                "text": "Amelia",
                "user_id": 596548082
               },
               " do you know where the SD card is?"
              ]
        """, "Amelia do you know where the SD card is?")

    def test_normalizeReplaceFunkyChars(self):
        self.normalizeTest("""
               "I’m"
        """, "I'm")

    def test_normalizeReplaceUrl(self):
        self.normalizeTest("""
               "http://www.microsoft.com/"
        """, "URL_TOKEN")

        self.normalizeTest("""
               "https://microsoft.com/"
        """, "URL_TOKEN")

        self.normalizeTest("""
               "url in the middle of https://microsoft.com/ a message"
        """, "url in the middle of URL_TOKEN a message")

    def normalizeTest(self, input, expected):
        self.assertEqual(normalize_message_text(json.loads(input)), expected)
