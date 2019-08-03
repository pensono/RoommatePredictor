{
    "dataset_reader": {
        "type": "telegram_reader",
        "token_indexers": {
            "tokens": {
                "type": "single_id"
            }
        },
        "people": ["Ethan Shea", "Ian Good", "Patty Popp", "Яель Гольдин"]
    },
    "iterator": {
        "type": "bucket",
        "batch_size": 100,
        "sorting_keys": [
            [
                "tokens",
                "num_tokens"
            ]
        ]
    },
    "model": {
        "type": "basic_classifier",
        "seq2seq_encoder": {
            "type": "lstm",
            "bidirectional": true,
            "hidden_size": 512,
            "input_size": 300,
            "num_layers": 1
        },
        "seq2vec_encoder": {
            "type": "bag_of_embeddings",
            "averaged": true,
            "embedding_dim": 1024
        },
        "text_field_embedder": {
            "token_embedders": {
                "tokens": {
                    "type": "embedding",
                    "embedding_dim": 300,
                    "pretrained_file": "glove.840B.300d.txt.gz",
                    "trainable": true
                }
            }
        }
    },
    "train_data_path": "data/19-8-2.json",
    "validation_data_path": "data/19-8-2.json",
    "trainer": {
        "cuda_device": 0,
        "grad_norm": 5,
        "learning_rate_scheduler": {
            "type": "reduce_on_plateau",
            "factor": 0.5,
            "mode": "max",
            "patience": 0
        },
        "num_epochs": 40,
        "num_serialized_models_to_keep": 2,
        "optimizer": {
            "type": "adam",
            "lr": 0.001
        },
        "patience": 5,
        "validation_metric": "+accuracy"
    },
    "validation_dataset_reader": {
        "type": "sst_tokens",
        "granularity": "2-class",
        "token_indexers": {
            "tokens": {
                "type": "single_id"
            }
        },
        "use_subtrees": false
    }
}