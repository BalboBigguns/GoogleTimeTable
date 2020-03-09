from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import re
import os


class TimeTableBot:
    def __init__(self):
        """Initialize webdriver for Chrome"""
        self.browser = webdriver.Chrome()
    

    def setDateSpan(self, dateStart, dateEnd):
        """Sets the time span for the import"""
        # Get the export dialog
        popup = self.browser.find_element_by_xpath('//*[@role="alertdialog"]')
        sleep(2)
        # first dialog select
        popup.find_element_by_xpath('div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/fieldset/div/div/div[1]/div/div[1]/div/input').click()
        sleep(2)
        # Date picker select
        datePicker = self.browser.find_element_by_xpath('/html/body/div[contains(@class, "x-ignore x-menu-plain x-menu-nosep x-menu x-date-menu")]/div/div/div')
        # dropdown select
        datePicker.find_element_by_xpath('table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button').click()
        sleep(2)
        # Month select
        datePicker.find_element_by_xpath('.//a[contains(text(), "{}")]'.format(dateStart["month"])).click()
        sleep(1)
        # Year select
        datePicker.find_element_by_xpath('.//a[contains(text(), "{}")]'.format(dateStart["year"])).click()
        sleep(2)
        # Submit
        datePicker.find_element_by_xpath('.//button[contains(text(), "OK")]').click()
        sleep(3)
        # Day select
        datePicker.find_element_by_xpath('.//td[contains(@class, "x-date-active")]//span[text() = "{0}"]'.format(dateStart["day"].lstrip("0"))).click()
        sleep(2)
        # Start date is set
        
        # Second date setting
        # Second dialog select
        popup.find_element_by_xpath('div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/fieldset/div/div/div[2]/div/div[1]/div/input').click()
        sleep(2)
        # Date picker reselect
        datePicker = self.browser.find_element_by_xpath('/html/body/div[contains(@class, "x-ignore x-menu-plain x-menu-nosep x-menu x-date-menu")]/div/div/div')
        sleep(2)
        # dropdown select
        datePicker.find_element_by_xpath('table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button').click()
        sleep(2)
        # Month select
        datePicker.find_element_by_xpath('.//a[contains(text(), "{}")]'.format(dateEnd["month"])).click()
        sleep(1)
        # Year select
        datePicker.find_element_by_xpath('.//a[contains(text(), "{}")]'.format(dateEnd["year"])).click()
        sleep(2)
        # Submit
        datePicker.find_element_by_xpath('.//button[contains(text(), "OK")]').click()
        sleep(3)
        # Day select
        datePicker.find_element_by_xpath('.//td[contains(@class, "x-date-active")]//span[text() = "{0}"]'.format(dateEnd["day"].lstrip("0"))).click()
        sleep(2)
        # Second date selected


    def manageDownload(self, path):
        """Controls download of file and moves it to downloads folder, waits for the file to be downloaded"""
        print("Downloading {}...".format(path))
        self.browser.find_element_by_xpath('//button[contains(text(), "Ok")]').click()
        sleep(1)
        while (os.system("mv ~/Downloads/ADECal.ics downloads/{}".format(path))):
            sleep(1)
        print("{} file downloaded.".format(path))
        

    def login(self, pathToCredentials = "credentials/credentialsEnt.json"):
        """Logs in to the university site.
        Optionally takes as parameter path to Json file with the following structure:
        {
            "username" : "...",
            "password" : "..."
        } 
        Default src = credentials/credentialsEnt.json """
        with open(pathToCredentials, 'r', encoding='utf8') as f:
                credentials = json.load(f)

        # Logging in to the webpage
        self.browser.get('http://ade.univ-tours.fr/direct/myplanning.jsp')
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys(credentials["username"])
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys(credentials["password"])
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="login"]/div[4]/input[3]').click()
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="x-auto-8"]/tbody/tr[2]/td[2]/em/button').click()
        sleep(3)
