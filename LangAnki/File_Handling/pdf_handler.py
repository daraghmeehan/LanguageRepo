import pdfplumber

import re
from os import path


def pdf_text(pdf_filename):
    """Collects all text from a pdf"""

    with pdfplumber.open(pdf_filename) as pdf:

        pages = pdf.pages

        text = []

        for page in pages:

            # maybe add layout too??
            # returns list of all characters
            text_of_page = page.extract_text()

            text_as_one_string = "".join(text_of_page)

            text.append(text_as_one_string)

    text = "\n\n".join(text)

    return text


def save_pdf_text(text, name):
    ##!! need txt name instead of pdf name

    if path.exists(name):
        return

    with open(name, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":

    pdfname = "J. K. Rowling - Harry Potter y la camara secreta.pdf"
    textname = "J. K. Rowling - Harry Potter y la camara secreta.txt"

    text = pdf_text(pdfname)
    save_pdf_text(text, textname)
