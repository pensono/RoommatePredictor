from typing import Dict, List
import logging
from overrides import overrides

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import Field, TextField, LabelField, MetadataField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter

from telegram_classifier.utils import *
from telegram_classifier.telegram_reader import *

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@DatasetReader.register("processed_reader")
class ProcessedDatasetReader(DatasetReader):
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

        with open(file_path, 'r', encoding='utf-8') as file:
            for message in json.load(file):
                if message['sender'] not in self._people:
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

        tokens = self._tokenizer.split_words(message['text'])
        label = message['sender']

        fields["tokens"] = TextField(tokens, self._token_indexers)
        fields["label"] = LabelField(label)

        # fields["metadata"] = MetadataField({"message": message['text']})

        return Instance(fields)
