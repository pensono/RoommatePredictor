import os

from allennlp.common.util import import_submodules
from allennlp.models import load_archive
from allennlp.predictors import Predictor

import_submodules('telegram_classifier')

archive_folder = 'trained-lstm/20190802-232055-less_regularized'

archive = load_archive(os.path.join(archive_folder, 'model.tar.gz'))
predictor = Predictor.from_archive(archive, 'roommate_pred')

while True:
    text = input("Phrase? ")
    output = predictor.predict_json({"text": text})

    print("Sender:", output['label'])
    for i in range(archive.model.vocab.get_vocab_size('labels')):
        labelName = archive.model.vocab.get_token_from_index(i, 'labels')
        percent = output['probs'][i] * 100.0
        print(f'  {labelName}: {percent:.1f}%')
