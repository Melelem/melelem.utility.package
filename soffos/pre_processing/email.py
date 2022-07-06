import re


EMAIL_URL = r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"


def replace_emails(text: str, replacement: str = 'email'):
    # NOTE: https://www.w3resource.com/javascript/form/email-validation.php
    return re.sub(EMAIL_URL, replacement, text)
