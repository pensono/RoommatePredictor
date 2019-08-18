import json
import re


def extract_messages(file):
    d = json.load(file)

    # Combine all the messages together, we don't really care about chats for now
    messages = [message for chat in d['chats']['list'] for message in chat['messages']]

    for message in messages:
        if message['type'] != 'message':
            continue
        if message['text'] == '':
            continue  # No text might happen if it's a picture with no caption

        # Get rid of bot stuff
        if 'via_bot' in message:
            continue
        if any('bot_message' in text for text in message['text']):
            continue

        yield message


def extract_chat(file, chat_name):
    d = json.load(file)

    # Combine all the messages together, we don't really care about chats for now
    messages = [message for chat in d['chats']['list'] for message in chat['messages'] if 'name' in chat and chat['name'] == chat_name]

    for message in messages:
        if message['type'] != 'message':
            continue
        if message['text'] == '':
            continue  # No text might happen if it's a picture with no caption

        # Get rid of bot stuff
        if 'via_bot' in message:
            continue
        if any('bot_message' in text for text in message['text']):
            continue

        yield message


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
