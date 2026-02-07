import re

def extract_numbers(text):
    return re.findall(r'\d+\.?\d*', text)


def numeric_match(claim, evidence):
    """
    Returns:
    True  -> numbers match
    False -> numbers mismatch
    None  -> no numbers in claim
    """
    claim_nums = extract_numbers(claim)
    evidence_nums = extract_numbers(evidence)

    if not claim_nums:
        return None

    for num in claim_nums:
        if num not in evidence_nums:
            return False

    return True
