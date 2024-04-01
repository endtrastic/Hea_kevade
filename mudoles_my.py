import sqlite3
import pyautogui as pag
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import InvalidArgumentException, NoSuchWindowException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import random
import keyboard
import time
import socket



exit2 = False
conn = sqlite3.connect('Mydatabase.db')
c = conn.cursor()

def already_saved_data_on_database():
    global exit2

    saved_data_on_database = input("If you want to see the last data on the database type (y): ")
    if saved_data_on_database.lower() == "y":
        while exit2 == False:
            data_choice = input("Choose what you want to see from the database, User, Title, Rating, Comment or date   (Type quit to exit): ")
            if data_choice.lower() == "quit":
                exit2 = True
            else:
                try:
                    # Try to select it except when there's an error, then insult the user to get them to behave
                    c.execute(f'''SELECT {data_choice} FROM SCRAPED_INFO''')
                    data_in_database = c.fetchall()
                    print(f"From the database selected: {data_choice} ", "\n")
                    print(data_in_database, "\n")
                except sqlite3.OperationalError:
                    print("Database does not exist or wrong column entered(dumbass)")
                    exit2 = True

    Create_table_for_database()        


def Create_table_for_database():
    try:
        c.execute('''CREATE TABLE SCRAPED_INFO(User TEXT, Title TEXT, Rating TEXT, Comment CLOB, date TEXT)''')
    except sqlite3.OperationalError:
        time.sleep(1)
        c.execute('''DROP TABLE SCRAPED_INFO''')
        Create_table_for_database()

already_saved_data_on_database()


url = input("Enter the amazon url you want to scrape: ")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
def get_url():
    try:
        driver.get(f"{url}")
    except InvalidArgumentException:
        print("Enter a fucking amazon url u dumbfuck")
        driver.quit()
    except NoSuchWindowException:
        print("Closed window")
        driver.quit()
get_url()
driver.implicitly_wait(3)

wait = WebDriverWait(driver, 20)
