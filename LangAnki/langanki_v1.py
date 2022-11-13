import sys, re

import PyQt5
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import spacy
import pyperclip

from Assistants.deepl_assistant import DeepLAssistant
from Assistants.spanish_dictionary_assistant import SpanishDictionaryAssistant

# from pdf_handler import pdf_text

# below two to make scaling right on my laptop
if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# NLP model for Spanish
nlp = spacy.load("es_core_news_md")

input("Are you using a VPN?\n")


# loading in c_o_s in spanish
with open(
    "./HP/J. K. Rowling - Harry Potter y la camara secreta.txt", "r", encoding="utf-8"
) as f:
    c_o_s_text = f.readlines()

c_o_s_text = " \n ".join(c_o_s_text)

c_o_s_text = re.sub(
    "\n", " ", c_o_s_text
)  # preventing newlines being grouped with words
c_o_s_text = re.sub(
    " +", " ", c_o_s_text
)  # removing multiple spaces problem with pdf plumber

# running sentence splitting etc on text
doc = nlp(c_o_s_text)
sents = list(doc.sents)


translation_assistant = DeepLAssistant()
translation_assistant.set_deepl_languages(input_lang="es", output_lang="en_output")


spanish_dictionary_assistant = SpanishDictionaryAssistant()


class LangAnki_UI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("./UI/LangAnki v1.ui", self)
        # self.start_spanish_study()

        # searching interface
        self.search_substring_button.clicked.connect(self.search_substring)
        self.matching_sents = []
        self.confirm_line_number_button.clicked.connect(self.confirm_line_number)
        self.sentences_forward_and_back.setEnabled(False)  # not yet implemented

        # translation interface
        self.translate_button.clicked.connect(self.translate)
        self.translations = {
            0: self.main_translation_textedit,
            1: self.alt_translation_1_textedit,
            2: self.alt_translation_2_textedit,
            3: self.alt_translation_3_textedit,
            4: self.alt_translation_4_textedit,
        }
        self.main_translation_button.clicked.connect(self.accept_main_translation)
        self.alt_translation_1_button.clicked.connect(self.accept_alt_translation_1)
        self.alt_translation_2_button.clicked.connect(self.accept_alt_translation_2)
        self.alt_translation_3_button.clicked.connect(self.accept_alt_translation_3)
        self.alt_translation_4_button.clicked.connect(self.accept_alt_translation_4)

        # flashcard editing interface
        self.note_type_and_deck_settings.setEnabled(False)  # not yet implemented
        self.add_flashcard_button.clicked.connect(self.add_flashcard)
        self.edit_previous_button.setEnabled(False)  # not yet implemented

        # dictionary lookup interface
        self.dictionary_search_button.clicked.connect(self.search_spanish_dictionaries)

    def search_substring(self):

        sentence_substring = self.substring_search_lineedit.text()

        self.matching_sents = [
            sent.text for sent in sents if sentence_substring in sent.text
        ]

        max_matching_sentences = 10

        if len(self.matching_sents) == 0:
            self.all_substrings_found.setText(
                "No matching sentences. Please try again."
            )

        elif len(self.matching_sents) > max_matching_sentences:
            self.all_substrings_found.setText(
                f"More than {max_matching_sentences} matching sentences. Please be more specific to narrow down your search."
            )

        else:
            substrings_found_str = "\n".join(
                [
                    f"{i} {self.matching_sents[i - 1]}"
                    for i in range(1, len(self.matching_sents) + 1)
                ]
            )
            self.all_substrings_found.setText(substrings_found_str)

    def confirm_line_number(self):

        if self.matching_sents == []:
            return

        try:
            line_number = int(self.line_number_lineedit.text())
        except:
            self.line_number_lineedit.setText("")
            return

        if 1 <= line_number <= len(self.matching_sents):
            chosen_line = self.matching_sents[line_number - 1]
            self.target_language_textedit.setText(chosen_line)
        else:
            self.line_number_lineedit.setText("")
            return

    def translate(self):
        pass

    def accept_translation(self, translation_number):

        target_language = self.target_language_textedit.toPlainText()
        source_language = self.translations[translation_number].toPlainText()

        self.target_language_field_textedit.setText(target_language)
        self.source_language_field_textedit.setText(source_language)

    def accept_main_translation(self):
        self.accept_translation(0)

    def accept_alt_translation_1(self):
        self.accept_translation(1)

    def accept_alt_translation_2(self):
        self.accept_translation(2)

    def accept_alt_translation_3(self):
        self.accept_translation(3)

    def accept_alt_translation_4(self):
        self.accept_translation(4)

    def add_flashcard(self):
        pass

    def search_spanish_dictionaries(self):

        query = self.dictionary_lookup_lineedit.text()

        if query == "":
            return
        else:
            spanish_dictionary_assistant.search_both_dictionaries(query)


if __name__ == "__main__":
    app = QApplication([])
    window = LangAnki_UI()
    window.show()
    sys.exit(app.exec_())


# def choose_line(sents):
#     """Asks user which line they want to make a flashcard from of those that match the user's input."""

#     print('\nChoose which line to learn from, or go back with "b".')

#     for i in range(1, len(sents) + 1):
#         print(f"{i}) {sents[i - 1]}")

#     line_number_to_learn = input(
#         '\nWhich line do you want to learn? Or go back with "b".\n'
#     )

#     if line_number_to_learn == "b":
#         return -1
#     else:
#         try:
#             line_number_to_learn = int(line_number_to_learn)
#         except:
#             line_number_to_learn = -1

#     if 1 <= line_number_to_learn <= len(sents):
#         return line_number_to_learn
#     else:
#         print("Please try again and choose a valid line.")
#         return choose_line(sents)


# try:

#     while True:
#         sentence_substring = input("\nSubstring:")

#         matching_sents = [
#             sent.text for sent in sents if sentence_substring in sent.text
#         ]

#         if len(matching_sents) == 0:
#             print("No matching sentences. Please try again.")
#             continue

#         if len(matching_sents) > 10:
#             print(
#                 "More than 10 matching sentences. Please be more specific to narrow down your search."
#             )
#             continue

#         line_number_to_learn = choose_line(matching_sents)

#         if line_number_to_learn == -1:
#             continue

#         line_to_learn = matching_sents[line_number_to_learn - 1]

#         # copy sentence to clipboard
#         pyperclip.copy(line_to_learn)
#         print("Line copied to clipboard.")

#         # enter the line into the input box
#         assistant.translate_text(line_to_learn)

#         input("Line entered. Enter any key to copy main translation.")
#         translation = assistant.copy_main_translation()

#         # copy translation to clipboard
#         pyperclip.copy(translation)
#         print("Translation copied to clipboard.")


# except:

#     assistant.stop_driver()
