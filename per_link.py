import re 

def extract_pr(message):
    match = re.search(r"\(#(\d+)\)", message)
    if match:
        return int(match.group(1))

    match = re.search(r"Merge pull request #(\d+)", message)
    if match:
        return int(match.group(1))

    return None