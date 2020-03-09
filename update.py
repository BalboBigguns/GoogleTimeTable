import sys
import os
import datetime
import re
from selenium.webdriver.common.keys import Keys
from time import sleep
import calendarBot
import calendarParser
import googleCalendar



def dateValidateAndParse(date):
    """Validates date in format dd/mm/yyyy. Returns dict with {day, month, year} elements"""
    # Valid date format "dd/mm/yyyy"
    if (not re.search(r'^(((0)[1-9])|[1-2][0-9]|(3)[0-1])(\/)(((0)[1-9])|((1)[0-2]))(\/)\d{4}$', date)):
        raise Exception('Invalid data format, should be dd/mm/yyyy')

    dateParts = date.split('/')

    monthAcronyms = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    return {"day":dateParts[0], "month" : monthAcronyms[int(dateParts[1]) - 1], "year" : dateParts[2] }


def getDI3(bot, startDate = None, endDate = None):
     # Find DI_3A_G2
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('DI_3A_G2', Keys.ENTER)
    sleep(5)

    # Choose the proper DI_3A_G2
    bot.browser.find_element_by_xpath('//*[@id="Direct Planning Tree_6852"]/div/span[2]').click()
    sleep(2)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (startDate and endDate):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("DI3.ics")


def getDI4(bot, startDate = None, endDate = None):
    # Find DI_4A_S8
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').clear()
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('DI_4A_S8', Keys.ENTER)
    sleep(5)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (startDate and endDate):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("DI4.ics")


def getCUEFEE(bot, startDate = None, endDate = None):
    # Find Objectif A2
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').clear()
    bot.browser.find_element_by_xpath('//*[@id="x-auto-141-input"]').send_keys('Objectif A2', Keys.ENTER)
    sleep(5)

    # Export
    bot.browser.find_element_by_xpath('//*[@id="x-auto-137"]/tbody/tr[2]/td[2]/em/button').click()
    sleep(2)

    if (startDate and endDate):
        bot.setDateSpan(startDate, endDate)

    bot.manageDownload("CUEFEE.ics")


def main():
    startDate = endDate = {}

    if (len(sys.argv) > 3 or len(sys.argv) == 2 and sys.argv[1] != '-next'):
        print(len(sys.argv))
        print("Wrong argument list!")
        print("Available options:")
        print("1. start date - end date (dd/mm/yyyy)")
        print("2. -next (to get next week schedule)")
        print("3. if no parameters provided, script will fetch this week's schedule")
        return
    elif (len(sys.argv) == 1):
        # for None value default behaviour is to fetch schedule for ongoing week
        startDate = endDate = { "dateObj" : None, "entFormat" : None}
    elif (len(sys.argv) == 3):
        startDate["entFormat"] = dateValidateAndParse(sys.argv[1])
        startDate["dateObj"] = datetime.strptime(sys.argv[1], r"%d/%m/%y")
        endDate["entFormat"] = dateValidateAndParse(sys.argv[2])
        endDate["dateObj"] = datetime.strptime(sys.argv[2], r"%d/%m/%y")
    
    print("Update script has been started...")

    bot = calendarBot.TimeTableBot()

    bot.login()

    #TODO: diff between new and old data
    os.system("rm downloads/*")

    getDI3(bot, startDate["entFormat"], endDate["entFormat"])
    sleep(3)
    getDI4(bot, startDate["entFormat"], endDate["entFormat"])
    sleep(3)
    getCUEFEE(bot, startDate["entFormat"], endDate["entFormat"])
    sleep(3)

    calendarParser.main()
    googleCalendar.clearTimeSpan(startDate["dateObj"], endDate["dateObj"])
    googleCalendar.uploadDB()
    

    input("Press a key to finish...")


if __name__ == "__main__":
    main()