# -*- coding: utf-8 -*-
from flask import render_template
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import os, sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from pyvirtualdisplay import Display
import random
import base64
import re
import urllib.request

whatsapp_url = 'https://web.whatsapp.com/'
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugin-port=9222")
options.add_argument("--screen-size=1200x800")
options.add_argument("--disable-popup-blocking")
options.add_argument("test-type")
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=options.to_capabilities())
driver.implicitly_wait(1)
driver.get(whatsapp_url)


base_dir = "./"
path_to_pdf = os.path.join(base_dir, "arquivo.pdf")
urllib.request.urlretrieve("http://nematoides.com.br/Content/Fotos/exemplo-de-pdf.pdf", path_to_pdf)


name = input('Enter the name of user or group : ')
input('Enter anything after scanning QR code')


user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()
attachment_box = driver.find_elements_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
while not len(attachment_box) > 0:
    attachment_box = driver.find_elements_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
    sleep(2)
attachment_box = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
attachment_box.click()
image_box = driver.find_elements_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]')
while not len(image_box) > 0:
    image_box = driver.find_elements_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]')
    sleep(2)
image_box = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input').send_keys(os.path.abspath(path_to_pdf))
sleep(2)
send_button = driver.find_elements_by_xpath('//span[@data-icon="send-light"]')
while not len(send_button) > 0:
    send_button = driver.find_elements_by_xpath('//span[@data-icon="send-light"]')
    sleep(2)
send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
send_button.click()