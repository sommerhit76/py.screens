from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from Classes.output import Output


class Driver:
    def __init__(self, browser):
        self.browser = browser

    def start_webdriver(self):
        driver = None

        if self.browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('log-level=2')

            driver = webdriver.Chrome(options=options)
        elif self.browser == 'firefox':
            options = FirefoxOptions()
            options.headless = True
            driver = webdriver.Firefox(options=options)
        else:
            Output.print(
                Output.MSG_ERROR,
                'browser `' + self.browser + '` not available, please use `chrome` or `firefox`'
            )

        return driver
