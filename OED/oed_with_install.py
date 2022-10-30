from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver.get("https://www.selenium.dev/selenium/web/web-form.html")
title = driver.title
driver.implicitly_wait(0.5)
print(title)
