from typing import Dict, Tuple, List
import logging
import json
import re
from overrides import overrides

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import Field, TextField, LabelField, MetadataField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers import Token
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter

from telegram_classifier.utils import *

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@DatasetReader.register("telegram_reader")
class TelegramDatasetReader(DatasetReader):
    def __init__(self,
                 people: List[str],
                 language: str = 'de_core_news_sm',
                 token_indexers: Dict[str, TokenIndexer] = None,
                 lazy: bool = False) -> None:
        super().__init__(lazy)
        self._token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        self._tokenizer = SpacyWordSplitter(language=language)
        self._people = people

    """
    Reads a file in the MT Classifier assignment format.

    Parameters
    ----------
    source_language : ``str``, optional, (default = 'de_core_news_sm')
        The name of the spaCy telegram_classifier used to tokenize the source sentences.
        Models can be found here <https://spacy.io/models/>.
    candidate_language : ``str``, optional (default = 'en_core_web_sm')
        The name of the spaCy telegram_classifier uwed to tokenize the candidate sentences.
    token_indexers : ``Dict[str, TokenIndexer]``, optional (default=``{"tokens": SingleIdTokenIndexer()}``)
            The token indexers to be applied to the words TextField.
    """

    @overrides
    def _read(self, file_path: str):
        file_path = cached_path(file_path)

        with open(file_path, 'r', encoding='utf-8') as data:
            logger.info("Reading telegram data from: %s", file_path)

            d = json.load(data)

            # Combine all the messages together, we don't really care about chats for now
            messages = [message for chat in d['chats']['list'] for message in chat['messages']]

            for message in messages:
                if message['type'] != 'message':
                    continue
                if message['from'] not in self._people:
                    continue
                if message['text'] == '':
                    continue  # No text might happen if it's a picture with no caption

                # Get rid of bot stuff
                if 'via_bot' in message:
                    continue
                if any('bot_message' in text for text in message['text']):
                    continue

                yield self.text_to_instance(message)

    @overrides
    def text_to_instance(self,  # type: ignore
                         message) -> Instance:
        # pylint: disable=arguments-differ
        """
        Parameters
        ----------
        source : ``str``, required
            The translation's source sentence.
        candidate : ``str``, required
            The translation candidate.
        label : ``str``, optional (default = None)
            Whether the candidate is human- or machine-translated, if known.
        """
        fields: Dict[str, Field] = {}

        # Remove formatting
        raw_text = normalize_message_text(message['text'])

        tokens = self._tokenizer.split_words(raw_text)
        label = message['from']

        print([sanitize(token.text) for token in tokens])

        fields["message"] = TextField(tokens, self._token_indexers)
        fields["label"] = LabelField(label)

        fields["metadata"] = MetadataField({"message": raw_text,
                                            "date": message['date']})
        return Instance(fields)


def normalize_message_text(message_text):
    def get_text(part):
        if isinstance(part, str):
            return part
        else:
            return part['text']

    if isinstance(message_text, list):
        # Flatten out the nested parts which are labeled by telegram as json objects
        message_text = "".join([get_text(part) for part in message_text])

    message_text = message_text.replace('’', "'")
    # Thanks? http://urlregex.com/
    message_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL_TOKEN', message_text)

    return message_text
