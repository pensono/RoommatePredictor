import os
from telegram_classifier.telegram_reader import *
import numpy as np


def telegram_to_processed(telegram_message):
    return {
        'sender': telegram_message['from'],
        'text': normalize_message_text(telegram_message['text'])
    }


def dump_output(contents, filename):
    out_file_path = os.path.join(originalPath, '..', 'processed', filename + ".json")
    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(contents, out_file)


if __name__ == '__main__':
    originalPath = "data/original/"

    processed_messages = []
    group_chat_messages = []
    for (dirpath, dirnames, filenames) in os.walk(originalPath):
        for in_file_name in filenames:
            if not in_file_name.endswith('.json'):
                continue

            in_file_path = os.path.join(dirpath, in_file_name)
            with open(in_file_path, 'r', encoding='utf-8') as in_file:
                print('Processing', in_file_path)
                #processed_messages.extend([telegram_to_processed(message) for message in extract_messages(in_file)])
                group_chat_messages.extend([telegram_to_processed(message) for message in extract_chat(in_file, 'House Life 2.0')])

    np.random.shuffle(processed_messages)
    count = len(processed_messages)

    #dump_output(processed_messages[:int(count * .85)], 'train')
    #dump_output(processed_messages[int(count * .85):], 'validation')
    dump_output(group_chat_messages, 'group_chat')
