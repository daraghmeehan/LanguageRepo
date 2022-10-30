from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

new_scraped_words = []

input("Press anything when ready")
driver.switch_to.window(driver.window_handles[-1])
print(driver.title)

while True:

    scrape_or_stop = input("anything or n")

    if scrape_or_stop == "n":
        break
    else:
        results = driver.find_element(By.ID, "resultsWrapper")
        print(results)
