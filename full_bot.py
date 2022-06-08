'''
- Auto Login Bot for Fantasy Football
- Uses Personal Login (username/password)
- Emails LM a reminder to activate league
- Scrapes Standings for Position, Team Abbreviation, Team name, Division, and Owner
6 - 6 - 2022
@akshay-choksi
'''
from ast import excepthandler
from email_reminder import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import openpyxl as O
import time

def main():
    #Initialize the path and webdriver
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(executable_path = PATH)
    driver.get('https://www.espn.com/fantasy/football/')

    #Find the Login dropdown
    button = driver.find_element(By.LINK_TEXT, "Log In")
    button.click()

    #New dropdown search
    main = driver.find_element(By.CLASS_NAME, "account-management")

    #Organize elements into list through 'li' tag, Login button is last li element
    list_elements = main.find_elements(By.TAG_NAME, "li")
    login = (list_elements[len(list_elements) - 1])
    login.click()

    #Switch to new frame and locate login box
    time.sleep(1)
    driver.switch_to.frame("disneyid-iframe")
    username = driver.find_element(By.XPATH, "//input[@placeholder='Username or Email Address']")

    #Enter username/email
    username.clear()
    time.sleep(1)
    username.send_keys('USERNAME/EMAIL')

    #Repeat with password
    password = driver.find_element(By.XPATH, "//input[@placeholder='Password (case sensitive)']")
    password.clear()
    password.send_keys('PASSWORD')

    #Confirm Login
    login = driver.find_element(By.XPATH, "//button[@class='btn btn-primary btn-submit ng-isolate-scope']")
    login.click()
    driver.page_source

    #Go to league
    try:
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-user-trigger"))
        )
    except:
        driver.quit()

    login.click()

    try:
        league = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"TEAM_NAME"))
        )
    except:
        driver.quit()

    league.click()
    site = driver.page_source

    # #IF Email Button is present locate it --> (LM has not reactivated the league)
    # try:
    #     email = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[@class='Button Button--lg Button--default Button--custom']"))
    #     )
    # except:
    #     pass
    # if(email):
    #     email.click()
    # time.sleep(1)

    # #Confirmation of sending email
    # try:
    #     confirm = driver.find_element(By.XPATH, "//button[@aria-label='Send Mail']")
    #     confirm.click()
    #     time.sleep(1)
    #     confirm = driver.find_element(By.XPATH, "//button[@class='Button Button--alt w-90']")
    #     confirm.click()
    #     print('Successfully Sent Reminder')
    # except:
    #     pass

    #Run the email reminder
    remind(driver)

    #Get Team Data
    #Header and Body Data
    row_count = len(driver.find_elements(By.XPATH, "//*[@id='fitt-analytics']/div/div[5]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/thead/tr"))
    print(row_count)
    rows = len(driver.find_elements(By.XPATH, "//*[@id='fitt-analytics']/div/div[5]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/tr"))
    print(rows)
    columns = len(driver.find_elements(By.XPATH, "//*[@id='fitt-analytics']/div/div[5]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td"))
    print(columns)

    #Build Xpath
    first = "//*[@id='fitt-analytics']/div/div[5]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/tr["
    second = "]/td["
    third = "]"

    standings_result = []
    #Iterate through table with indices (Goes from 1 -->  row/column count inclusive )
    for row in range(1,rows + 1 ):
        temp = {}
        for column in range(1, columns + 1):
            final_path = first + str(row) + second + str(column) + third
            table_data = driver.find_element(By.XPATH, final_path).text
            #Organize into headers
            if(column == 1):
                temp.update({"Ranking" : table_data})
            elif((column == 2)):
                temp.update({"Abbreviation" : table_data})
            elif((column == 3)):
                temp.update({"Team Name" : table_data})
            elif((column == 4)):
                temp.update({"Division" : table_data})
            else:
                temp.update({"Owner" : table_data}) 
        #Populate the data set
        standings_result.append(temp)
        print("")
    print(standings_result)

    #Use Pandas Framework to open dataframe, write excel file
    df_data = pd.DataFrame(standings_result)
    print(df_data)
    df_data.to_excel('fantasy_football_standings.xlsx', index=False)

    #End Script
    time.sleep(5)
    driver.close()

#Rerun bot until LM becomes annoyed enough to reactivate league
while(True):
    main()

#End Script



