from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

import pyperclip  # for copying to clipboard

from spanish_web_setup import setup_deepl


class DeepLAssistant:
    def __init__(self) -> None:
        self.deepl_language_button_mappings = {
            "es": "translator-lang-option-es",
            "en_output": "translator-lang-option-en-GB",
        }

    def start_driver(self):
        self.deepl_driver = setup_deepl()

    def set_deepl_languages(self, input_lang="es", output_lang="en_output"):
        """Chooses the input (source) and output (target) languages by clicking buttons on deepl site."""

        # setting input language first
        # clicking input language button
        self.deepl_driver.find_element(
            By.XPATH, "//button[@dl-test='translator-source-lang-btn']"
        ).click()
        self.deepl_driver.implicitly_wait(1.5)

        # choosing input language
        self.deepl_driver.find_element(
            By.XPATH,
            f"//button[@dl-test='{self.deepl_language_button_mappings[input_lang]}']",
        ).click()
        self.deepl_driver.implicitly_wait(1.0)

        # next, setting output language
        # clicking output language button
        self.deepl_driver.find_element(
            By.XPATH, "//button[@dl-test='translator-target-lang-btn']"
        ).click()
        self.deepl_driver.implicitly_wait(1.5)

        # choosing output language
        self.deepl_driver.find_element(
            By.XPATH,
            f"//button[@dl-test='{self.deepl_language_button_mappings[output_lang]}']",
        ).click()
        self.deepl_driver.implicitly_wait(1.0)

    def swap_deepl_languages(self):
        """Swaps target and source language."""

        # simply click swap languages button
        self.deepl_driver.find_element(
            By.XPATH, "//button[@aria-label='Swap source with target language']"
        ).click()
        self.deepl_driver.implicitly_wait(1.5)

    def translate_text(self, text):
        """Pastes the given text into the input (source) text box, and copies the translation from the output (target) text box."""

        # find input text box
        text_box = self.deepl_driver.find_element(
            By.XPATH,
            "//textarea[@class='lmt__textarea lmt__source_textarea lmt__textarea_base_style']",
        )
        self.deepl_driver.implicitly_wait(0.2)

        # paste text in input text box
        text_box.send_keys(text)

        # wait for translation and copy it
        try:
            wait = WebDriverWait(self.deepl_driver, timeout=14, poll_frequency=0.7)
            # when copy button appears, translations also do
            copy_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Copy to clipboard']")
                )
            )
            self.deepl_driver.implicitly_wait(0.5)

        except:
            pass

        # finding top translation <div>
        main_translation = self.deepl_driver.find_element(
            By.XPATH, "//div[@id='target-dummydiv']"
        )

        # using .text gives blank, so use innerHTML
        main_translation = main_translation.get_attribute("innerHTML").strip()

        # copy to clipboard
        pyperclip.copy(main_translation)

    def copy_translation(self, translation_number):

        try:
            # note - includes top translation, not just alternatives
            all_translations = self.deepl_driver.find_elements(
                By.XPATH,
                "//ul[@aria-labelledby='alternatives-heading']//button[@class='lmt__translations_as_text__text_btn']",
            )

            all_translations = [
                translation.get_attribute("innerHTML").strip()
                for translation in all_translations
            ]
        except:
            pass

        try:
            assert type(translation_number) is int
            assert 1 <= translation_number <= len(all_translations)
        except:
            print(
                "Please ensure you choose an int in the range 1 to (number of translations)."
            )

        selected_translation = all_translations[translation_number - 1]
        # copy to clipboard
        pyperclip.copy(selected_translation)
