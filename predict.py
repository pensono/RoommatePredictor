import os

from allennlp.common.util import import_submodules
from allennlp.models import load_archive
from allennlp.predictors import Predictor

import_submodules('telegram_classifier')

archive_folder = 'trained/initial'

archive = load_archive(os.path.join(archive_folder, 'model.tar.gz'))
predictor = Predictor.from_archive(archive, 'roommate_pred')

while True:
    text = input("Phrase? ")
    output = predictor.predict_json({"text": text})

    print("Sender:", output['label'])
    print()
