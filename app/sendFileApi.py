from selenium import webdriver
from time import sleep
from flask import render_template
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import os, sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugin-port=9222")
options.add_argument("--screen-size=1200x800")

driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=options.to_capabilities())


driver.get('https://web.whatsapp.com/')
input('Enter anything after scanning QR code')

driver.get('https://web.whatsapp.com/send?phone=' + '5534991409347')
sleep(10)

filepath = '/home/pablo/Downloads/download.png'

attachment_box = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
attachment_box.click()

sleep(5)

image_box = driver.find_element_by_xpath(
    '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input').send_keys(filepath)
#image_box.click()

sleep(5)

send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
send_button.click()