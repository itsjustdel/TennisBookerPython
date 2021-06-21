from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from sys import platform
import time
from datetime import datetime
import asyncio

#for instructions on safari remote activation
#https://www.browserstack.com/guide/run-selenium-tests-on-safari-using-safaridriver 

class Location(Enum):   
    Kelvingbridge = 1
    Knightswood = 2
    QueensPark = 3
    Null = 4

    "ctl00_MainContent__advanceSearchResultsUserControl_Activities_ctrl32_lnkActivitySelect_xs" 

def getLocationPath(driver,location):    
    if location == Location.Kelvingbridge:         
        return driver.find_elements_by_link_text('Kelvingrove Tennis')
    elif location == Location.Knightswood:
        return driver.find_elements_by_link_text('Knightswood Park Tennis')
    elif location == Location.QueensPark:
        return driver.find_elements_by_link_text('Queens Park Tennis')
    else: 
        return 0

def MoveByDays(driver,days):
    # wait
    time.sleep(1)

    for i in range(days):
        #  IWebElement nextPage = driver.FindElement(By.XPath(".//*[@id='ctl00_MainContent_Button2']"));
        time.sleep(1)
        nextPage = driver.find_element_by_xpath(".//*[@id='ctl00_MainContent_Button2']")
        nextPage.click()

def CheckForAvailable(driver, startTime, endTime,button):

    # only buttons that are available have a submit tag
    availableButtons = driver.find_elements_by_xpath("//input[@type='submit']")
        
    for i in range(len(availableButtons)):
        # get first two characters of the value string
        valueString = availableButtons[i].get_attribute("value")[:2]
        timeInt = int(valueString)
        # if within user defined times
        if timeInt >= startTime and timeInt <= endTime:
            # click the button
            availableButtons[i].click()
            # goes to confirm booking button page
            ConfirmBooking(driver)
            

            
            # get out of here
            return
        
def ConfirmBooking(driver):
    book = driver.find_element_by_xpath(".//*[@id='ctl00_MainContent_btnBasket']")
    book.click()
    # now feed back to interface to tell of successful booking
    # TO DO

def start_webdriver(self, username, password, shutdownValue, location, start, end):
       
    self.setText("Booking..")
    
    timeMet = True ###############TEST
    while (timeMet == False):    
        dt = datetime.now()
        if (dt.hour == 23 and dt.minute == 59):    
            #jump out while loop    
            timeMet = True        
        else:        
            # wait a second and check again - doesnt need to be super fast recheck here, this is just to start the program - the page refresh option is faster
            self.setText(dt)
            time.sleep(1)

    driver = 0    
    if platform == "win32":
        driver = webdriver.Chrome()
    #mac
    elif platform == "darwin":
        driver = webdriver.Safari()
    
    driver.get("https://members.glasgowclub.org/Connect/MRMLogin.aspx")
    
    print(username)
    ##to be got from interface
    username = username #  "itsjustdel@gmail.com"
    print(password)
    password = password #" Sparr0wl4nds!" #DELETE

    # get login and password boxes
    emailTextBox = driver.find_element_by_xpath(".//*[@id='ctl00_MainContent_InputLogin']")
    passwordTextBox = driver.find_element_by_xpath(".//*[@id='ctl00_MainContent_InputPassword']")
    
    # fill them with user details
    emailTextBox.send_keys(username)
    passwordTextBox.send_keys(password)

    # click the button
    loginButton = driver.find_element_by_xpath(".//*[@id='ctl00_MainContent_btnLogin']")
    loginButton.click()

     # find link for location (queen's park kelvingrove etc)    
    time.sleep(1)
    locationButton = getLocationPath(driver, location)
    #can be two, last one found is the one we want
    locationButton[len(locationButton)-1].click()

    time.sleep(1)
    MoveByDays(driver, 3)

    time.sleep(1)
    CheckForAvailable(driver,start,end,self)

    #reset button
    self.setText("Book")
     #close webdriver we done!
    driver.quit()

    #if user checked box to shut down
    if(shutdownValue == True):
        # win
        if platform == "win32":
            os.system("shutdown /s /t 1")
            #mac
        elif platform == "darwin":
            os.system("shutdown -h now")

    

    
