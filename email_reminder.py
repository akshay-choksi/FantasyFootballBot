'''
- Function for the main functionality of the fantasy bot
- Off-season --> remind league manager to reactivate
'''

from ast import excepthandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def remind(driver):
    try:
        email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='Button Button--lg Button--default Button--custom']"))
        )
    except:
        return
  
    email.click()
    time.sleep(1)

    #Confirmation of sending email
    try:
        confirm = driver.find_element(By.XPATH, "//button[@aria-label='Send Mail']")
        confirm.click()
        time.sleep(1)
        confirm = driver.find_element(By.XPATH, "//button[@class='Button Button--alt w-90']")
        confirm.click()
        print('Successfully Sent Reminder')
    except:
        return

    remind(driver)