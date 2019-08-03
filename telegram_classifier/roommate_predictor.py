from overrides import overrides
import json

from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter
from allennlp.models import Model
from allennlp.predictors.predictor import Predictor


@Predictor.register("roommate_pred")
class MTClassifierPredictor(Predictor):
    """
    Predictor for any model that takes in a source and candidate sentences and
    classifies it as a machine- or human-translated sentence.
    """
    def __init__(self, model: Model,
                       dataset_reader: DatasetReader) -> None:
        super().__init__(model, dataset_reader)

    def predict(self, text) -> JsonDict:
        return self.predict_json({"text": text})

    @overrides
    def dump_line(self, outputs: JsonDict) -> str:
        line = {
            "sender": outputs['label'],
            "text": outputs['text'],
        }

        return json.dumps(line)

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        return self._dataset_reader.text_to_instance(json_dict['text'])

