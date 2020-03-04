from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import re
import sys
import os


def getCourseRegister():
    """Loads register from data/courseRegister.json file"""
    with open("data/courseRegister.json", 'r', encoding='utf8') as f:
        courseRegister = json.load(f)

    return courseRegister

def setCourseRegister(register):
    """Dumps register to data/courseRegister.json file"""
    with open("data/courseRegister.json", 'w', encoding='utf8') as f:
        json.dump(register, f)


def getCourses():
    """Loads events data from data/timeTableDB.json file"""
    with open("data/timeTableDB.json", 'r', encoding='utf8') as f:
        courses = json.load(f)

    return courses


def setCourses(courses):
    """Dumps courses data to data/timeTableDB.json file"""
    with open("data/timeTableDB.json", 'w', encoding='utf8') as f:
        json.dump(courses, f)


def appendCourses(courses):
    """Appends courses to the end of timeTableDB.json file"""
    stateDB = getCourses()
    stateDB = [*stateDB, *courses]
    setCourses(stateDB)


def dateValidateAndParse(date):
    """Validates date in format dd/mm/yyyy. Returns dict with {day, month, year} elements"""
    # Valid date format "dd/mm/yyyy"
    if (not re.search(r'^(((0)[1-9])|[1-2][0-9]|(3)[0-1])(\/)(((0)[1-9])|((1)[0-2]))(\/)\d{4}$', date)):
        raise Exception('Invalid data format, should be dd/mm/yyyy')

    dateParts = date.split('/')

    monthAcronyms = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    return {"day":dateParts[0], "month" : monthAcronyms[int(dateParts[1]) - 1], "year" : dateParts[2] }


class TimeTableBot:
    def __init__(self):
        """Initialize webdriver for Cshrome"""
        self.browser = webdriver.Chrome()
        

    def changeViewToTable(self):
        """Switch view to table"""
        self.browser.find_element_by_xpath('//*[@id="x-auto-139"]/tbody/tr[2]/td[2]/em/button').click()
        sleep(1)
        self.browser.find_element_by_xpath('//div[contains(text(), "Vue tableau")]').click()
        sleep(1)
        self.browser.find_element_by_xpath('//button[contains(text(), "Ok")]').click()
        sleep(1)


    def setDateSpan(self, dateStart, dateEnd):
        """Sets the time span for the import"""
        # Start date select
        self.browser.find_element_by_xpath('//*[@id="x-auto-348"]').click()
        # Month and year dialog box select
        self.browser.find_element_by_xpath('//*[@id="x-auto-383"]').click()
        # Month select
        self.browser.find_element_by_xpath('//*[@id="x-auto-374"]/div[2]/table/tbody//a[contains(text(), "{}")]'.format(dateStart["month"])).click()
        # Year select
        self.browser.find_element_by_xpath('//*[@id="x-auto-374"]/div[2]/table/tbody//a[contains(text(), "{}")]'.format(dateStart["year"])).click()
        # Submit
        self.browser.find_element_by_xpath('//*[@id="x-auto-374"]/div[2]/table/tbody/tr[7]/td/button[1]').click()
        # Select day
        self.browser.find_element_by_xpath('//*[@id="x-auto-374"]/div[1]/table[2]/tbody//td[@class="x-date-active"]/a/span[contains(text(), "{}")]'.format(dateStart["day"])).click()

        #TODO: finish this method


    def manageDownload(self, path):
        """Controls download of file and moves it to downloads folder, waits for the file to be downloaded"""
        print("Downloading {}...".format(path))
        self.browser.find_element_by_xpath('//button[contains(text(), "Ok")]').click()
        sleep(1)
        while (os.system("mv ~/Downloads/ADECal.ics downloads/{}".format(path))):
            sleep(1)
        print("{} file downloaded.".format(path))
        

    def login(self):
        """Logs in to the university site"""
        with open("credentials/credentialsEnt.json", 'r', encoding='utf8') as f:
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


def getDI3(bot, startDate = '', endDate = ''):
     # Find DI_3A_G2
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('DI_3A_G2', Keys.ENTER)
    sleep(4)

    # Choose the proper DI_3A_G2
    bot.browser.find_element_by_xpath('//*[@id="Direct Planning Tree_6852"]/div/span[2]').click()
    sleep(1)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (len(sys.argv) == 3):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("DI3.ics")


def getDI4(bot, startDate = '', endDate = ''):
    # Find DI_4A_S8
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').clear()
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('DI_4A_S8', Keys.ENTER)
    sleep(3)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (len(sys.argv) == 3):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("DI4.ics")


def getCUEFEE(bot, startDate = '', endDate = ''):
    # Find Objectif A2
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').clear()
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('Objectif A2', Keys.ENTER)
    sleep(3)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (len(sys.argv) == 3):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("CUEFEE.ics")


def main():
    if (len(sys.argv) > 3 or len(sys.argv) == 2 and sys.argv[1] != '-next'):
        print(len(sys.argv))
        print("Wrong argument list!")
        print("Available options:")
        print("1. start date - end date (dd/mm/yyyy)")
        print("2. -next (to get next week schedule)")
        print("3. if no parameters provided, script will fetch this week's schedule")
        return
    elif (len(sys.argv) == 3):
        startDate = dateValidateAndParse(sys.argv[1])
        endDate = dateValidateAndParse(sys.argv[2])
    

    bot = TimeTableBot()

    bot.login()

    if (len(sys.argv) == 2):
        print("-next entered, function currently not supported...")
        return
        # Go to the next week
        #TODO: probably need to be able to tell based on text and current date
        bot.browser.find_element_by_xpath('//*[@id="x-auto-207"]/tbody/tr[2]/td[2]/em/button').click()
        sleep(2)

    os.system("rm downloads/*")

    if (len(sys.argv) == 3):
        getDI3(bot, startDate, endDate) 
        getDI4(bot, startDate, endDate)
        getCUEFEE(bot, startDate, endDate)
    else:
        getDI3(bot) 
        getDI4(bot)
        getCUEFEE(bot)
    
    input("Press a key to finish...")

if __name__ == "__main__":
    main()
