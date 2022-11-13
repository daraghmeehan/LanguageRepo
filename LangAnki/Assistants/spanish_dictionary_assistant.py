from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Assistants.assistant import Assistant

# from assistant import Assistant

# make finding search box and typing it, clicking button, opening multiple tabs and doing same procedures in them, closing popups -> all inheritable from superclass


class SpanishDictionaryAssistant(Assistant):
    def __init__(self) -> None:
        self.setup_assistant()

    def setup_assistant(self):

        self.setup_spanishdict()

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        # to keep track of unique identifier of the tab
        self.spanishdict_handle = self.driver.current_window_handle

        # making a new tab
        self.driver.execute_script("window.open('about:blank', 'secondtab');")
        wait.until(EC.number_of_windows_to_be(2))

        # making sure to get both handles right
        possible_spanish_collins_handle = self.driver.window_handles[0]
        if possible_spanish_collins_handle == self.spanishdict_handle:
            self.spanish_collins_handle = self.driver.window_handles[1]
        else:
            self.spanish_collins_handle = possible_spanish_collins_handle
        assert self.spanishdict_handle != self.spanish_collins_handle

        self.setup_spanish_collins_dict()

        # perfect for legion 5 at full resolution
        self.set_window_position(x=930, y=0)
        self.set_window_size(width=784, height=926)
        ## maybe make this setting in UI!! "set as default window size" as different users need different sizes

        self.driver.switch_to.window(self.spanishdict_handle)

    def setup_spanishdict(self):

        self.start_driver("https://www.spanishdict.com/")

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        try:
            # Wait for the new tab to finish loading content
            wait.until(
                EC.title_is(
                    "SpanishDict | English to Spanish Translation, Dictionary, Translator"
                )
            )
            sleep(2)
            self.close_spanishdict_startup_popups()
        except:
            # self.stop_driver()
            return

    def close_spanishdict_startup_popups(self):

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        # first close cookie popups
        more_options_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-l81hgh"))
        )
        more_options_button.click()  # More Options
        sleep(3)

        save_and_exit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class=' css-1mour4p' and @aria-pressed='false']")
            )
        )
        save_and_exit_button.click()  # Save and Exit
        sleep(0.5)

        # close initial popup if it renders
        self.close_spanishdict_general_popup(self.driver)

    def close_spanishdict_general_popup(self):
        try:
            self.driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()
            sleep(0.2)
        except:
            pass  # if don't find the general popup, just skip

    def setup_spanish_collins_dict(self):

        # first making sure we are in the right tab
        self.driver.switch_to.window(self.spanish_collins_handle)

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://www.collinsdictionary.com/dictionary/spanish-english")

        try:
            # Wait for the new tab to finish loading content
            wait.until(
                EC.title_is(
                    "Collins English Dictionary | Translations, Definitions and Pronunciations"
                )
            )
            sleep(2)
            self.close_spanish_collins_startup_popups()
        except:
            # self.stop_driver()
            return

    def close_spanish_collins_startup_popups(self):

        # Setup wait for later
        wait = WebDriverWait(self.driver, 10)

        # closing cookie dialogue
        show_purposes_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-pc-btn-handler"))
        )
        show_purposes_button.click()  # Show Purposes
        sleep(2)

        confirm_my_choices_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[class='save-preference-btn-handler onetrust-close-btn-handler']",
                )
            )
        )
        confirm_my_choices_button.click()  # Confirm My Choices
        sleep(0.5)

    def search_both_dictionaries(self, query):

        self.driver.switch_to.window(self.spanishdict_handle)
        sleep(0.2)
        self.search_spanishdict(query)

        self.driver.switch_to.window(self.spanish_collins_handle)
        sleep(0.2)
        self.search_spanish_collins_dict(query)

        self.driver.switch_to.window(self.spanishdict_handle)
        self.close_spanishdict_general_popup()

    def search_spanishdict(self, query):

        # close general popup if it appears
        self.close_spanishdict_general_popup()

        # finding search text box
        search_text_box = self.driver.find_element(By.ID, "query")

        # first delete text already in the box
        search_text_box.clear()
        sleep(0.3)

        # enter query into search box
        search_text_box.send_keys(query)
        sleep(0.2)

        # clicking search button
        self.driver.find_element(By.ID, "query-button").click()

    def search_spanish_collins_dict(self, query):

        # finding search text box
        search_text_box = self.driver.find_element(
            By.XPATH, "//input[@class='search-input autoc-input']"
        )

        # first delete text already in the box
        search_text_box.clear()
        sleep(0.3)

        # enter query into search box
        search_text_box.send_keys(query)
        sleep(0.3)

        # clicking search button
        self.driver.find_element(By.XPATH, "//button[@class='search-submit']").click()


if __name__ == "__main__":
    d = SpanishDictionaryAssistant()
