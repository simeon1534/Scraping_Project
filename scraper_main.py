from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
from scraper_class import Scraper

inp = input("Enter fac number: ")


def selenium_setup(driver):
    try:
        group = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "group"))
        )
        group.send_keys(inp)
    except:
        driver.quit()

    group_radio = driver.find_element(By.ID, "groupRadio")
    group_radio.click()

    select = Select(driver.find_element(By.NAME, "Week"))
    options = select.options
    return options


def dataframe_to_csv(data):
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('test2.csv', sep='\t', encoding='utf-8-sig')
    df.to_excel('test2.xlsx', encoding='utf-8-sig')


def main():
    """Driver Set Up"""
    driver_service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    driver.get("https://nvna.eu/wp/")

    """Data Dictionary Creation"""
    data = {
        "Date": [],
        "Number": [],
        "Hour": [],
        "Discipline": [],
        "Room": [],
        "Teacher": []
    }

    """Selenium First Page Set Up """
    options = selenium_setup(driver)

    """Iterating pages and Scraping """
    for i in range(len(options) - 1):
        select = Select(driver.find_element(By.NAME, "Week"))
        select.select_by_index(i)
        button = driver.find_element(By.XPATH, "//input[@value='Покажи']")
        button.click()

        curr_url = driver.current_url

        scraper = Scraper(curr_url, data)  # Vzemame data dictionary-to
        updated_data = scraper.data
        data = updated_data
        time.sleep(3)

    """From dictionary data --> panda dataframe --> csv file"""
    dataframe_to_csv(data)


if __name__ == '__main__':
    main()

