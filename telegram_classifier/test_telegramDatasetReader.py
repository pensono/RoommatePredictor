from unittest import TestCase
import json
from telegram_classifier.telegram_dataset_reader import normalizeMessageText


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

    def normalizeTest(self, input, expected):
        self.assertEqual(normalizeMessageText(json.loads(input)), expected)