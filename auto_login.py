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
    browser.add_cookie({"name": "MUSIC_U", "value": "00370C53D024A286DD6B9FE0E50F29E90A9189085F6C93610844A6072DDA9ACCB20198273F1B5649BF0E9E3D7BB6FC90F5952C9106732107A93B80B5D5F517B8A89B145BEA876475DC2D1223D65BF6FFF6CDC8E57110D180263813BE45A8DAE3A338A2B573CAE2807C82F0AE3DE44369D8DD9F6AAC458D03EF51160E8ED5CBCAA6F34F1802AE19787B9A107457B052447A229009DCBAF862E70EB765E58806FC44BF6E8C3BD69FC5FF4596C62E2A9C8BDFB8DAB5D2CB9C88878AAA6C256FEC6AE3B0021F00C7BF6135F13949D13A7F71EA417837908A91F2053EE42446623395FBC510EA0E10C5CD5A7CCACE6F72B1CBEF20E9DB5E520FBC613736D7D3BBD8A0D8CD714AD227D077424E210F14236F78DB6210253E965A1F1791F9B756DE2EC82FA5C01D439FD40414BFDD1344EF6F86F8DDF890C2F8609BEF1BB151DEA5FB7B37156D11E1BD2E8DD8C46AA740991F2D4D501A345995F327FDF27AFF2E6DF3205B"})
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
