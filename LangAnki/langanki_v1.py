import sys, re

import PyQt5
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5.QtGui import QFont, QKeySequence

import spacy
import pyperclip

from Assistants.deepl_assistant import DeepLAssistant
from Assistants.spanish_dictionary_assistant import SpanishDictionaryAssistant

from Flashcards.flashcard_creator import FlashcardCreator

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
# doc = nlp("hi")
sents = list(doc.sents)


translation_assistant = DeepLAssistant()
translation_assistant.set_deepl_languages(input_lang="es", output_lang="en_output")

spanish_dictionary_assistant = SpanishDictionaryAssistant()
# translation_assistant = None
# spanish_dictionary_assistant = None

understanding_flashcard_fields = [
    "Target Language",
    "Source Language",
    "Answer Hint",
    "Example Sentence(s)",
    "Other Forms",
    "Extra Info",
    "Pronunciation",
]
normal_spanish_understanding_flashcard_creator = FlashcardCreator(
    deck_name="Spanish Understanding (Normal)", fields=understanding_flashcard_fields
)
easy_spanish_understanding_flashcard_creator = FlashcardCreator(
    deck_name="Spanish Understanding (Easy)", fields=understanding_flashcard_fields
)


class LangAnki_UI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("./UI/LangAnki v1.ui", self)
        # self.start_spanish_study()

        self.setup_shortcuts()
        self.setup_all_enter_key_signals()

        # searching interface
        self.search_substring_button.clicked.connect(self.search_substring)
        self.matching_sents = []
        self.confirm_line_number_button.clicked.connect(self.confirm_line_number)
        self.sentences_forward_and_back.setEnabled(False)  # not yet implemented

        # translation interface
        self.translate_button.clicked.connect(self.translate)
        self.refresh_translation_button.clicked.connect(self.refresh_translations)
        ## rename this!!
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

        self.action_bold.triggered.connect(self.embolden_text)

        # dictionary lookup interface
        self.dictionary_search_button.clicked.connect(self.search_spanish_dictionaries)

    def setup_shortcuts(self):

        self.translate_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.translate_shortcut.activated.connect(self.translate_button.click)

        self.copy_main_translation_shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        self.copy_main_translation_shortcut.activated.connect(
            self.main_translation_button.click
        )

        self.dictionary_lookup_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.dictionary_lookup_shortcut.activated.connect(
            self.dictionary_lookup_lineedit.setFocus
        )

        self.add_flashcard_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.add_flashcard_shortcut.activated.connect(self.add_flashcard)

    def setup_all_enter_key_signals(self):
        self.substring_search_lineedit.returnPressed.connect(
            self.search_substring_button.click
        )
        self.line_number_lineedit.returnPressed.connect(
            self.confirm_line_number_button.click
        )

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
            self.matching_sents = []

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
            ## add console messages here (in this function)!!
            return

        try:
            line_number = int(self.line_number_lineedit.text())
        except:
            self.line_number_lineedit.setText("")
            return

        if 1 <= line_number <= len(self.matching_sents):

            # resetting fields after choosing next line to study
            self.reset_translation_fields()
            self.reset_flashcard_fields()  ###do this not here but in translation copy!!

            chosen_line = self.matching_sents[line_number - 1]
            self.target_language_textedit.setText(
                chosen_line
            )  # adding to translation box
            self.target_language_field_textedit.setText(
                chosen_line
            )  # adding to flashcard field too

        else:
            self.line_number_lineedit.setText("")
            return

    def translate(self):

        ###!! add removing all other translations when click translation button

        # copy target language text
        text_to_translate = self.target_language_textedit.toPlainText()

        translation_assistant.translate_text(text_to_translate)

        all_translations = translation_assistant.copy_all_translations(
            text_to_translate
        )

        self.set_translations(all_translations)

    def copy_translations(self, text_to_translate):

        all_translations = translation_assistant.copy_all_translations(
            text_to_translate
        )

        self.set_translations(all_translations)

    def set_translations(self, all_translations):

        number_of_translations = len(all_translations)

        if number_of_translations == 0:
            self.translations[0].setText(
                "No translations found. Something may have gone wrong."
            )
        else:
            for i in range(number_of_translations):
                self.translations[i].setText(all_translations[0])

    def refresh_translations(self):
        self.copy_translations("")

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

        # reject if target and source languages are missing
        target_language_field = self.target_language_field_textedit.toPlainText()
        print("target = {target_language_field}")
        source_language_field = self.source_language_field_textedit.toPlainText()
        if target_language_field == "" or source_language_field == "":
            print("Need both target language and source language! Rejecting card.")
            return

        # creating card from fields in UI
        card_as_dict = {
            "Target Language": target_language_field,
            "Source Language": source_language_field,
            "Answer Hint": self.answer_hint_lineedit.text(),
            "Example Sentence(s)": self.example_sentences_lineedit.text(),
            "Other Forms": self.other_forms_lineedit.text(),
            "Extra Info": self.extra_info_lineedit.text(),
            "Pronunciation": self.pronunciation_lineedit.text(),
        }

        # retrieving chosen deck
        deck = self.deck_comboBox.currentText()

        if deck == "Spanish":
            normal_spanish_understanding_flashcard_creator.add_flashcard(card_as_dict)
        elif deck == "Spanish Easy":
            easy_spanish_understanding_flashcard_creator.add_flashcard(card_as_dict)

        self.reset_flashcard_fields()

    def embolden_text(self):
        print("em")  # but needs to undo!!
        self.target_language_field_textedit.setFontWeight(QFont.Bold)

    def reset_flashcard_fields(self):

        ## turn into data structure like self.translations!!
        self.target_language_field_textedit.setText("")
        self.source_language_field_textedit.setText("")
        self.answer_hint_lineedit.setText("")
        self.example_sentences_lineedit.setText("")
        self.other_forms_lineedit.setText("")
        self.extra_info_lineedit.setText("")
        self.pronunciation_lineedit.setText("")

    def reset_translation_fields(self):

        for translation_field in self.translations.values():
            translation_field.setText("")

    def search_spanish_dictionaries(self):

        query = self.dictionary_lookup_lineedit.text()

        if query == "":
            return
        else:
            spanish_dictionary_assistant.search_both_dictionaries(query)


if __name__ == "__main__":
    try:
        app = QApplication([])
        window = LangAnki_UI()
        window.show()
        ## this right here??!! don't think so
        app.exec_()
    except Exception as e:
        print(e)
        print("App crashed.")

    print("UI closed, now saving flashcards.")
    normal_spanish_understanding_flashcard_creator.export_deck()
    easy_spanish_understanding_flashcard_creator.export_deck()

    print("Flashcards saved, now closing assistants.")
    translation_assistant.stop_driver()
    spanish_dictionary_assistant.stop_driver()
