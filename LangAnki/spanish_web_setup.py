from selenium import webdriver
from selenium.webdriver.common.by import By


def setup_deepl_driver():

    # open deepl
    deepl_driver = webdriver.Firefox()
    deepl_driver.get("https://www.deepl.com/translator")

    return deepl_driver


def close_deepl_startup_popups(deepl_driver):

    deepl_driver.find_element(By.CLASS_NAME, "dl_cookieBanner--buttonSelected").click()


def setup_deepl():

    deepl_driver = setup_deepl_driver()

    close_deepl_startup_popups(deepl_driver)

    return deepl_driver


def setup_spanish_dict_driver():

    # open spanish dict
    spanish_dict_driver = webdriver.Firefox()
    spanish_dict_driver.get("https://www.spanish_dict.com/")

    return spanish_dict_driver


def close_spanish_dict_startup_popups(spanish_dict_driver):

    spanish_dict_driver.find_element(By.CLASS_NAME, "css-1mour4p").click()
    spanish_dict_driver.implicitly_wait(1)
    try:
        # close initial popup if it renders
        close_spanish_dict_general_popup(spanish_dict_driver)
    except:
        pass


def close_spanish_dict_general_popup(spanish_dict_driver):
    spanish_dict_driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()


def setup_spanish_dict():

    spanish_dict_driver = setup_spanish_dict_driver()

    close_spanish_dict_startup_popups(spanish_dict_driver)

    return spanish_dict_driver
