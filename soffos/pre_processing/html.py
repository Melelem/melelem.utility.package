from bs4 import BeautifulSoup


def strip_html_tags(text: str):
    return BeautifulSoup(text, 'html.parser').get_text()
