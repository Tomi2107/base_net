import re

def extract_mentions(text):
    """
    Extrae usernames mencionados con @username
    Devuelve un set sin duplicados
    """
    if not text:
        return set()

    return set(re.findall(r'@(\w+)', text))
