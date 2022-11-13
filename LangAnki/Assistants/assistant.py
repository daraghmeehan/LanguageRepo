from selenium import webdriver

from time import sleep


class Assistant:
    def __init__(self) -> None:
        pass
        # should this be 'raise NotImplementedError'??!!

    def setup_assistant(self):
        raise NotImplementedError

    def start_driver(self, webpage=""):

        self.driver = webdriver.Firefox()

        if webpage != "":
            self.driver.get(webpage)

    def stop_driver(self):
        self.driver.quit()

    def reset_driver(self, webpage=""):
        self.stop_driver()
        sleep(2)
        self.start_driver(webpage)

    def set_window_position(self, x, y):
        self.driver.set_window_position(x, y)

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)
