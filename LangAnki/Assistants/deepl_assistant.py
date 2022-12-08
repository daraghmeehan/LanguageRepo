from time import sleep
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Assistants.assistant import Assistant

# from assistant import Assistant  # for testing


class DeepLAssistant(Assistant):
    def __init__(self) -> None:
        self.setup_assistant()

        self.deepl_language_button_mappings = {
            "es": "translator-lang-option-es",  # Spanish
            "en_output": "translator-lang-option-en-GB",
            "nl": "translator-lang-option-nl",  # Dutch
            "ja": "translator-lang-option-ja",  # Japanese
            # above currently using, below future
            "zh": "translator-lang-option-zh",  # Chinese
            "cs": "translator-lang-option-cs",  # Czech
            "fr": "translator-lang-option-fr",  # French
            "de": "translator-lang-option-de",  # German
            "el": "translator-lang-option-el",  # Greek
            "it": "translator-lang-option-it",  # Italian
            "pt_input": "translator-lang-option-pt",  # Portuguese input
            "pt_eu_output": "translator-lang-option-pt-PT",  # European Portuguese output
            "pt_br_output": "translator-lang-option-pt-BR",  # Brazilian Portuguese output
            "ru": "translator-lang-option-ru",  # Russian
            "tr": "translator-lang-option-tr",  # Turkish
        }

    def setup_assistant(self):

        self.start_driver("https://www.deepl.com/translator")

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        try:
            # Wait for the new tab to finish loading content
            wait.until(
                EC.title_is("DeepL Translate: The world's most accurate translator")
            )
            self.close_deepl_startup_popups()
        except:
            self.stop_driver()
            return

        self.set_window_position(x=0, y=0)
        self.set_window_size(width=942, height=926)

    def close_deepl_startup_popups(self):
        try:
            self.driver.find_element(
                By.CLASS_NAME, "dl_cookieBanner--buttonSelected"
            ).click()
        except:
            pass

    def set_deepl_languages(self, input_lang, output_lang):
        """Chooses the input (source) and output (target) languages by clicking buttons on deepl site."""

        # setting input language first
        # clicking input language button
        self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-source-lang-btn']"
        ).click()
        sleep(1.5)

        # choosing input language
        self.driver.find_element(
            By.XPATH,
            f"//button[@dl-test='{self.deepl_language_button_mappings[input_lang]}']",
        ).click()
        sleep(1)

        # next, setting output language
        # clicking output language button
        self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-target-lang-btn']"
        ).click()
        sleep(1)

        # choosing output language
        self.driver.find_element(
            By.XPATH,
            f"//button[@dl-test='{self.deepl_language_button_mappings[output_lang]}']",
        ).click()
        sleep(2)

    def swap_deepl_languages(self):
        """Swaps target and source language."""

        # simply click swap languages button
        self.driver.find_element(
            By.XPATH, "//button[@aria-label='Swap source with target language']"
        ).click()
        sleep(1)

    def translate_text(self, text):
        """Pastes the given text into the input (source) text box."""  # , and returns the translation from the output (target) text box."""

        # find input text box
        text_box = self.driver.find_element(
            By.XPATH,
            "//textarea[@dl-test='translator-source-input']",
        )
        sleep(0.2)

        # first delete text already in the box
        text_box.clear()
        sleep(0.3)

        # then paste text in input text box
        text_box.send_keys(text)

    def copy_main_translation(self, text_to_translate: str):

        is_successful_translation = self.wait_for_translation(text_to_translate)

        if not is_successful_translation:
            print("Didn't verify successful translation")

        sleep(2)

        try:
            # finding top translation <div>
            main_translation = self.driver.find_element(
                By.XPATH, "//div[@id='target-dummydiv']"
            )
            # using .text gives blank, so use innerHTML
            main_translation = main_translation.get_attribute("innerHTML").strip()
            main_translation = main_translation.replace("­", "")
        except:
            print("Couldn't find translated text")
            return ""

        return main_translation

    def copy_all_translations(self, text_to_translate: str):
        ###!!! not working

        # if actually translating something, wait till see appropriately long main translation
        if text_to_translate != "":
            is_successful_translation = self.wait_for_translation(text_to_translate)

            if not is_successful_translation:
                print("Didn't verify successful translation")

            sleep(2)

        try:
            # note - includes top translation, not just alternatives
            all_translations = self.driver.find_elements(
                By.XPATH,
                "//ul[@aria-labelledby='alternatives-heading']//button[@class='lmt__translations_as_text__text_btn']",
            )
            all_translations = [
                translation.get_attribute("innerHTML").strip()
                for translation in all_translations
            ]
            all_translations = [
                translation.replace("­", "") for translation in all_translations
            ]
            return all_translations
        except:
            return []

    ##!! input_text better name than text_to_translate??
    def wait_for_translation(self, input_text):

        ##!! only a heuristic for e.g. Spanish
        min_length_of_translation = int(len(input_text) / 2)
        min_length_of_translation = max(0, min_length_of_translation - 2)  # nonzero

        wait = WebDriverWait(self.driver, 10)

        try:
            # wait until non whitespace characters found in main translation text, and it's at least min_length_of_translation long
            wait.until(
                lambda driver: re.search(
                    f"\w.{{{min_length_of_translation},}}\w",
                    driver.find_element(
                        By.XPATH, "//div[@id='target-dummydiv']"
                    ).get_attribute("innerHTML"),
                )
            )
            return True
        except:
            print("No text found in translated div.")
            return False


if __name__ == "__main__":

    from assistant import Assistant  # for testing

    text = "Los demócratas estadounidenses acarician el control del Senado con la punta de los dedos. Se han apuntado Arizona, con lo que tienen ya 49 senadores, y han dado un importante salto en Nevada con el que Catherine Cortez Masto ha neutralizado de golpe prácticamente toda la ventaja que le llevaba el republicano Adam Laxalt. Si los demócratas consiguen Nevada, ni siquiera tendrán que esperar a la segunda vuelta de Georgia para retener el control de la Cámara alta. Tras la derrota de Arizona, Donald Trump ha pedido que se repitan las elecciones y los republicanos han empezado a esparcir sospechas de irregularidades sin base. Las buenas noticias para los demócratas no llegan solo en el Senado. Todo apunta a que la Cámara de Representantes, que las encuestas daban por abrumadoramente republicana, se encamina hacia una ligerísima mayoría conservadora. E incluso no es descartable que acabe cayendo del lado del partido del presidente estadounidense, Joe Biden. Las encuestas ya colocaban como favoritos a los demócratas en la carrera por el Senado en Arizona. Pero el margen estrecho de diferencia y el lento recuento han aumentado el suspense. En el Estado quedan cientos de miles de votos por contar y es posible que el escrutinio se extienda a lo largo de la próxima semana, pero la ventaja del demócrata Mark Kelly ya es insalvable, según Associated Press, que lleva 175 años computando los votos en las elecciones estadounidenses y proclamando de forma infalible y casi oficial a los ganadores. Kelly tiene un 52% de los votos, una ventaja de unos seis puntos sobre el republicano Blake Masters, otro de los polémicos candidatos aupados por Donald Trump que han decepcionado las expectativas en estas elecciones. Fiel al trumpismo, tras ver que los votos le daban la espalda, Masters se ha dedicado a sembrar dudas sobre la limpieza del proc"

    d = DeepLAssistant()
    d.set_deepl_languages(input_lang="es", output_lang="en_output")
    # d.swap_deepl_languages()
    # d.swap_deepl_languages()
    # d.translate_text("Holi guapa")
    d.translate_text(text)
    print(d.copy_main_translation(text))
