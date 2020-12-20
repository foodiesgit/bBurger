import time
from iBot.browser_activities import ChromeBrowser

class WHill:
    ###### Buttons Xpath ######
    LOGIN = "//input[@id='ssc-lis']"
    USER_INPUT = "//input[@id='ssc-liu']"
    PASSWORD_INPUT = "//input[@id='ssc-lipw']"

    def __init__(self, browser, url, user, password, amount):
        self.browser = browser
        self.url = url
        self.amount = amount
        self.user = user
        self.password = password

    def login(self):
        ##### Locate elements in Page object ####
        self.browser.ucDriver.get('https://google.com')
        time.sleep(3)
        print(self.browser.ucDriver.execute_script('return navigator.webdriver'))
        self.browser.ucDriver.get(self.url)
        time.sleep(10)
        UserInput = self.browser.ucDriver.find_element_by_xpath(self.USER_INPUT)
        UserPassword = self.browser.ucDriver.find_element_by_xpath(self.PASSWORD_INPUT)
        UserInput.send_keys(self.user)
        time.sleep(1)
        UserPassword.send_keys(self.password)
        time.sleep(1)
        LoginButton = self.browser.ucDriver.find_element_by_xpath(self.LOGIN)
        LoginButton.click()
        time.sleep(100)

    def makeBet(self):
        pass
