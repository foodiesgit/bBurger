import time
from selenium.webdriver.common import keys
from iBot.excel_activities import Excel
from iBot.browser_activities import ChromeBrowser
from Automation import WHill
import os
from selenium.webdriver.common.keys import Keys

class Robot:

    ### Robot Variables ####

    EXCEL_PATH = os.getcwd() + '/credentials.xlsx'
    BROWSER_PATH = os.getcwd() + '/Driver/chromedriver'
    CHROME_PROFILE = "/Users/enriquecrespodebenito/Library/Application Support/Google/Chrome"

    def __init__(self):
        self.browser = None
        self.excel = Excel(self.EXCEL_PATH)
        self.iniBrowser()

    def iniBrowser(self):
        self.browser = ChromeBrowser(self.BROWSER_PATH, undetectable=True)
        self.browser.setprofile(self.CHROME_PROFILE)
        self.browser.open()

    def getCredentials(self, bookmark):
        i = 2
        while True:
            if self.excel.readCell("A" + str(i), sheet="Hoja1") == bookmark:
                user = self.excel.readCell("B" + str(i), sheet="Hoja1")
                password = self.excel.readCell("C" + str(i), sheet="Hoja1")
                credentials = (user,password)
                break
        return credentials

    def run(self):
        url = "https://www.betburger.com/bets/MTA2NzM5NTU0fDE3LC0wLjUsNCwwLDAsMA?access_token=d4d2b01df0647f899db0abd4bed2e015&amp;is_live=0"
        cedentials = self.getCredentials("Betfair")
        WH = WHill(self.browser,url, cedentials[0], cedentials[1], 1)
        WH.login()

if __name__ == "__main__":
    Robot().run()