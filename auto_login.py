# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')
@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0082964609FEB0064840C11564F449CBA65939FE8DB17C6F4ABAE5F95C0A300AA0F14D2693649233EE0159486D0D2ACF72F1849973505D3DB1E14122E78A60D74539A01AF3D552ED3660DE06B5F2F735DF8AB1073724EB94D6A6D22A049EA3B4CAA80BCF842BF65B6A982969F3C1BAD6384663F8A9762BFA26D9DD4582348AEF570C83033C81BCB850BF88FED537BE3856375BCB494C392E61D5BD90B407283ABA031139E73CE6B623BADB65D42275F012EA95587ECBEDC2F06F6F18F8A7FFFC8781196995CBBCBCD41C438746CB59E177C7AC3A8659E53C219E3C4589DC80666137D45DF7391B4BDA11CB6ACBB05D01D9F64ADB664686B84B997F50919DC7E987DA2E9BE8BEFB189FBFC3C4555780D17E8739A2BD744DBFAACBDD9456221B3665C7274BDC5FC1D974EF8ECE99B0C51DADE75C4A479C6C659596EF2871E6BDE8F6A916F0593E504F944001BBE4BA73CEEA945A4CB979B9893A5865BE5B393B9512"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
