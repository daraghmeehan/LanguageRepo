from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

import pyperclip  # for copying to clipboard

from assistant import Assistant


class DictionaryAssistant(Assistant):
    def __init__(self) -> None:
        super().__init__()

    ## close popups (in assistant?)

    ## look up definition

    ## self.search_box (save name)
    ## self.home_page
    
    ## make exception handling in case searching fails (don't want to crash UI)!!
