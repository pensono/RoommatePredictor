import json
import numpy as np
import sys
import time

from allennlp.commands import main


def train_single(config_name, overrides=None):
    overrides = overrides or {}

    serialization_dir = f"trained-{config_name}/{time.strftime('%Y%m%d-%H%M%S')}"

    # Assemble the command into sys.argv
    sys.argv = [
        "allennlp",  # command name, not used by main
        "train",
        f"experiments/{config_name}.json",
        "-s", serialization_dir,
        "--include-package", "telegram_classifier",
        '-o', overrides
    ]

    start = time.time()
    main()
    end = time.time()

    print("Training took", (end - start) / 60, "minutes")


def train_random_search(config_name):
    while True:

        overrides = "{}"
        np.random.seed()  # Not sure why I have to do this
        if config_name == "lstm":
            hidden_size1 = int(2.0 ** np.random.uniform(5, 11))
            hidden_size2 = int(2.0 ** np.random.uniform(5, 11))
            regularization = 10.0 ** np.random.uniform(-5, -2)

            print(f"Training with {hidden_size1} {hidden_size2} {regularization}")

            overrides = json.dumps({
                'model': {
                    "regularizer": [
                        ["weight.*", {"type": "l2", "alpha": regularization}]
                    ],
                    'seq2seq_encoder': {
                        'hidden_size': hidden_size1
                    },
                    'seq2vec_encoder': {
                        'input_size': hidden_size1 * 2,
                        'hidden_size': hidden_size2
                    }
                }
            })
        elif config_name == "boe":
            hidden_size = int(2.0 ** np.random.uniform(5, 12))
            regularization = 10.0 ** np.random.uniform(-5, -2)

            print(f"Training with {hidden_size} {regularization}")

            overrides = json.dumps({
                'model': {
                    "regularizer": [
                        ["weight.*", {"type": "l2", "alpha": regularization}]
                    ],
                    'seq2seq_encoder': {
                        'hidden_size': hidden_size
                    },
                    'seq2vec_encoder': {
                        'embedding_dim': hidden_size * 2,
                    }
                }
            })

        train_single(config_name, overrides)


if __name__ == '__main__':
    train_random_search('boe')
