import os
import json


print("name,training_acc,validation_acc,best_epoch,hidden1,hidden2,reg")
for directory in os.listdir('trained'):
    metrics_path = os.path.join('trained', directory, 'metrics.json')
    config_path = os.path.join('trained', directory, 'config.json')

    if not os.path.exists(metrics_path):
        continue # Not fully trained

    with open(metrics_path) as metrics_file, \
        open(config_path) as config_file:
        metrics = json.load(metrics_file)
        config = json.load(config_file)

        print('''{0},
                {1[training_accuracy]},
                {1[best_validation_accuracy]},
                {1[best_epoch]},
                {2[model][seq2seq_encoder][hidden_size]},
                {2[model][seq2vec_encoder][hidden_size]},
                {2[model][regularizer][0][1][alpha]}'''.replace(" ", "").replace("\n", "")
              .format(directory, metrics, config))
