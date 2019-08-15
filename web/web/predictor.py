import os
import logging

from allennlp.common.util import import_submodules
from allennlp.models import load_archive
from allennlp.predictors import Predictor

logger = logging.getLogger('predictor')

logger.info(f'Loading model from {os.path.abspath(os.curdir)}')
import_submodules('telegram_classifier')

archive_folder = '../trained-lstm/20190802-232055-less_regularized'

archive = load_archive(os.path.join(archive_folder, 'model.tar.gz'))
predictor = Predictor.from_archive(archive, 'roommate_pred')

logger.info('Model loaded')


def predict(phrase):
    prediction = predictor.predict_json({"text": phrase})

    results = {}
    for i in range(archive.model.vocab.get_vocab_size('labels')):
        label_name = archive.model.vocab.get_token_from_index(i, 'labels')
        results[label_name] = prediction['probs'][i]

    return results

