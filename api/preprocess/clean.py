import json
import os
import re
from typing import List, Union

from logzero import logger


def remove_timestamp(text: str) -> Union[str, bool]:
    """Remove timestamp from text

    :type text: str
    :rtype: Union[str, bool]
    """
    pattern = "[0-1]?[0-9]\/[0-3]?[0-9]\/[0-2][0-9], [0-1]?[0-9]:[0-5][0-9] [AP]M - "
    search = re.findall(pattern, text)
    if search:
        if text.find(search[0]) == 0:
            text = text[len(search[0]):]
            return text

    return False


def remove_emoji(text: str) -> str:
    """Remove emoji from text

    :type text: str
    :rtype: str
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def remove_last_name(text: str) -> str:
    """Remove last name from text

    :type text: str
    :rtype: str
    """
    text = text.split(':')
    text_cleaned = ''

    if len(text[0].split()) > 1:
        text_cleaned = text[0].split()[0] + ':' + ' '.join(text[1:])

    return text_cleaned


def remove_url(text: str) -> str:
    """Remove url from text

    :type text: str
    :rtype: str
    """
    text = re.sub(r"http\S+", "", text)
    return text


def remove_phone_number(text: str) -> str:
    """Remove phone number from text

    :type text: str
    :rtype: str
    """
    text = re.sub(r"\+?1?\d{9,15}\b", "", text)
    return text


def remove_email(text: str) -> str:
    """Remove email from text

    :type text: str
    :rtype: str
    """
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "", text)
    return text


def remove_multiple_spaces(text: str) -> str:
    """Remove multiple spaces from text

    :type text: str
    :rtype: str
    """
    text = re.sub(r"\s+", " ", text)
    return text


def remove_whatsapp_system_messages(text: str) -> str:
    """Remove whatsapp system messages from text

    :type text: str
    :rtype: str
    """
    system_messages = [
        'Messages and calls are end-to-end encrypted',
        'Media omitted',
        'Your security code with',
        'Everything up-to-date',
        'http',
        'https',
        'You deleted this message',
        '<Media omitted>',
    ]

    if any(message in text for message in system_messages):
        return ''

    return chat


def remove_empty_lines(text: str) -> str:
    """Remove empty lines from text

    :type text: str
    :rtype: str
    """
    if ' '.join(text.split(':')[1:]).isspace():
        return ''

    return text


def remove_name(text: str) -> str:
    """Remove name from text

    :type text: str
    :rtype: str
    """
    return ' '.join(text.split(':')[1:]).strip()


def consolidate_messages(chats: List[str], person_1: str, person_2: str) -> List[str]:
    """Consolidate messages from text

    :type text: List[str]
    :rtype: List[str]
    """
    total_count = len(chats)
    logger.warning('Total count: {}'.format(total_count))

    consolidated_chats = []
    while chats:
        logger.info(
            'Processing: {}/{}'.format(len(consolidated_chats), total_count))
        if not chats:
            break
        if not chats[0].startswith(person_1) and not chats[0].startswith(person_2):
            chats.pop(0)
            continue
        person_1_chat = ''
        person_2_chat = ''

        while chats and chats[0].startswith(person_1):
            person_1_chat += remove_name(chats[0]) + '\n'
            chats.pop(0)

        while chats and chats[0].startswith(person_2):
            person_2_chat += remove_name(chats[0]) + '\n'
            chats.pop(0)

        if person_1_chat:
            consolidated_chats.append(person_1 + ': ' + person_1_chat.strip())
        if person_2_chat:
            consolidated_chats.append(person_2 + ': ' + person_2_chat.strip())

    return consolidated_chats


def create_jsonl_file(chats: List[str], filename: str) -> None:
    """Create jsonl file from text

    :type text: List[str]
    :rtype: None
    """
    total_count = len(chats)
    logger.warning('Total count: {}'.format(total_count))

    with open(os.path.join(os.getcwd(), 'api', 'preprocess', filename), 'w') as jsonl_file:
        for ind in range(0, len(chats), 2):
            logger.info('Processing: {}/{}'.format(ind, total_count))
            try:
                prompt = chats[ind]
                completion = chats[ind + 1]
            except IndexError:
                break
            jsonl_file.write(
                json.dumps({
                    'prompt': remove_name(prompt),
                    'completion': remove_name(completion)
                }) + '\n'
            )


with open(os.path.join(os.getcwd(), 'api', 'preprocess', 'chat.txt')) as chat_file:
    chats = chat_file.readlines()

cleaned_chats = []
for chat in chats:
    chat = remove_timestamp(chat)
    if chat:
        chat = remove_emoji(chat)
        chat = remove_last_name(chat)
        # chat = remove_url(chat)
        chat = remove_phone_number(chat)
        chat = remove_email(chat)
        chat = remove_multiple_spaces(chat)
        chat = remove_whatsapp_system_messages(chat)
        chat = remove_empty_lines(chat)
    if chat:
        cleaned_chats.append(chat)

# Input your first names as arguments
consolidated_chats = consolidate_messages(cleaned_chats, '<You>', '<AI>')
create_jsonl_file(consolidated_chats, 'chat.jsonl')
