import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Betfair:


    ###### Buttons Xpath ######
    LOGIN = "//input[@id='ssc-lis']"
    USER_INPUT = "//input[@id='ssc-liu']"
    PASSWORD_INPUT = "//input[@id='ssc-lipw']"
    ACCEPT_COOCKIES = "//button[@id='onetrust-accept-btn-handler']"
    BET_SLIPP = "//input[@id='bet-cfc6bdf8e6905288b749d20bcea919ca72a3ca58-stake']"
    EVENT_NAME = "//span[@class='event-name']"
    BET_1 = "//span[@id='yui_3_5_0_1_1608486443438_9344']"
    BET_HANDICAP_LABEL = 'ui-runner-handicap ui-924_248520957-7017911'
    BET_CUOTE = "//span[@class='odds ui-runner-price ui-924_248520957-7017911 ui-display-decimal-price']"
    BET_MARKET = "//div[@class='market']"
    BALANCE = "//td[@id='yui_3_5_0_1_1608486443438_65669']"
    MI_CUENTA = "//a[@class='ssc-unc']"
    MIS_APUESTAS = "//a[@class='ssc-myBets']"
    BET_PANEL = "//div[@class='bet--panel']"



    def __init__(self, browser, url, user, password, amount, event, cuote, market):
        self.browser = browser
        self.url = url
        self.amount = amount
        self.user = user
        self.password = password
        self.event = event
        self.cuote = cuote
        self.market = market
        self.balance = self.getbalance()

    def login(self):
        ##### Locate elements in Page object ####
        self.browser.ucDriver.get('https://google.com')
        time.sleep(3)
        print(self.browser.ucDriver.execute_script('return navigator.webdriver'))
        self.browser.ucDriver.get(self.url)
        time.sleep(10)
        aceptCoockies = self.browser.ucDriver.find_element_by_xpath(self.ACCEPT_COOCKIES)
        aceptCoockies.click()
        UserInput = self.browser.ucDriver.find_element_by_xpath(self.USER_INPUT)
        UserPassword = self.browser.ucDriver.find_element_by_xpath(self.PASSWORD_INPUT)
        UserInput.send_keys(self.user)
        time.sleep(1)
        UserPassword.send_keys(self.password)
        time.sleep(1)
        LoginButton = self.browser.ucDriver.find_element_by_xpath(self.LOGIN)
        LoginButton.click()
        time.sleep(10)
        try:
            webdriver.ActionChains(self.driver.ucDriver).send_keys(Keys.ESCAPE).perform()
        except:
            pass

    def checkBets(self):

        event = self.browser.ucDriver.find_element_by_xpath(self.EVENT_NAME).text
        bet1 = self.browser.ucDriver.find_element_by_xpath(self.BET_1).text

        try:
            betType = self.browser.ucDriver.find_element_by_xpath(self.BET_HANDICAP_LABEL).text
        except:
            pass

        betType = bet1 + " " + betType
        betCuote = self.browser.ucDriver.find_element_by_xpath(self.BET_CUOTE).text
        betMarket = self.browser.ucDriver.find_element_by_xpath(self.BET_MARKET).text


        if betCuote != self.cuote:
            raise Exception("Las cuotas no coinciden")

        if betMarket != self.market:
            raise Exception("Los Eventos no coinciden")

        if event != self.event:
            raise Exception("El nombre de los eventos no coinciden")

    def getBalance(self) -> object:
        return self.browser.ucDriver.find_element_by_xpath(self.BALANCE)

    def getBets(self):
        self.browser.ucDriver.find_element_by_xpath(self.MI_CUENTA).click()
        self.browser.ucDriver.find_element_by_xpath(self.MIS_APUESTAS).click()
        time.sleep(10)
        apuestas = self.browser.ucDriver.find_elements_by_xpath(self.BET_PANEL)

        for apuesta in apuestas:
            apuesta.find_element_by_xpath


    def makeBet(self):
        #### Put AMOUNT in the bet Slip #####
        betslip = self.browser.ucDriver.find_element_by_xpath(self.BET_SLIPP)
        betslip.click()
        betslip.send_keys(self.amount)
