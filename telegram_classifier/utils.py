import emoji


def sanitize(input):
    """
    Sanitize for purposes of printing to the console
    :param input:
    :return:
    """
    return emoji.demojize(input).encode('utf-8')
