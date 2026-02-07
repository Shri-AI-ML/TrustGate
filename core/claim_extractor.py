import re

def extract_claims(text):
    """
    Splits text into atomic factual claims.
    Handles both periods and newline breaks.
    """
    sentences = re.split(r'[.\n]+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]
