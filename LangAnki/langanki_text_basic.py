from numpy import c_
from deepl_assistant import DeepLAssistant
from pdf_handler import pdf_text

import re
import spacy

nlp = spacy.load("es_core_news_md")

input("Are you using a VPN?\n")

assistant = DeepLAssistant()

assistant.start_driver()
assistant.set_deepl_languages()


def choose_line(sents):
    """Asks user which line they want to make a flashcard from of those that match the user's input."""

    print('\nChoose which line to learn from, or go back with "b".')

    for i in range(1, len(sents) + 1):
        print(f"{i}) {sents[i - 1]}")

    line_number_to_learn = input(
        '\nWhich line do you want to learn? Or go back with "b".\n'
    )

    if line_number_to_learn == "b":
        return -1
    else:
        try:
            line_number_to_learn = int(line_number_to_learn)
        except:
            line_number_to_learn = -1

    if 1 <= line_number_to_learn <= len(sents):
        return line_number_to_learn
    else:
        print("Please try again and choose a valid line.")
        return choose_line(sents)


# c_o_s_text = pdf_text("./J. K. Rowling - Harry Potter y la camara secreta.pdf")
with open(
    "./J. K. Rowling - Harry Potter y la camara secreta.txt", "r", encoding="utf-8"
) as f:
    c_o_s_text = f.readlines()

c_o_s_text = " \n ".join(c_o_s_text)

c_o_s_text = re.sub(
    "\n", " ", c_o_s_text
)  # preventing newlines being grouped with words
c_o_s_text = re.sub(
    " +", " ", c_o_s_text
)  # removing multiple spaces problem with pdf plumber
## might want to remove/edit behaviour above line!!

doc = nlp(c_o_s_text)
sents = list(doc.sents)

while True:
    sentence_substring = input("\nSubstring:")

    matching_sents = [sent.text for sent in sents if sentence_substring in sent.text]

    if len(matching_sents) == 0:
        print("No matching sentences. Please try again.")
        continue

    if len(matching_sents) > 10:
        print(
            "More than 10 matching sentences. Please be more specific to narrow down your search."
        )
        continue

    line_number_to_learn = choose_line(matching_sents)

    if line_number_to_learn == -1:
        continue

    line_to_learn = matching_sents[line_number_to_learn - 1]

    assistant.translate_text(line_to_learn)
