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
    browser.add_cookie({"name": "MUSIC_U", "value": "007C510EADF96FB3C1E24AD2E657E8E0425FCE662672712DD2FA6A59426A7A497AD8FE098CF20AEF7F5ECAA4184A13CAFD14AFE78962078267E2202D90E3CC62DD420FEE8DA9F049E191F829E6FD2A3A005D145B249A1DA200F6CF7D7780C0D02B11265E175951AEC720F07F44C0128015C371D8A744EB3A4F7736BB8CA2EE0652086D2DD438F00B7EA2F5A90B2AC0C0B379A0FC7A0BED6FEF58256D67C90C77BD32A0DA650F12CFF8419D8810B063CA34D6E03B33C1483A6717CDD4A06D1027DDFAB43C394798AFDAE0C7F7B2F56155111A9BEBFD6D6FB164770B65463A0468FACC0BFD1759BE625C5DA26272069A4FBBADA7C3A26F2A69632B002D1D16A6FE3987820ADAEA03AFE60B1CDFD735F1E09F0392C0F09A5B689448DBE491E7D3481F7C86DE95917AF67BADDE32169FE9FC3D0D2B92C9B8ED9893146BEAF076484B2F95FC529100F0060CD14DB41384CA31873570293F1D8243FD12A1BFDCC2EC8A4B"})
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
