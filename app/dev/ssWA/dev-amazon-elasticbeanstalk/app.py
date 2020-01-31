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

def get_qr_code():
	global driver
	driver.get(whatsapp_url)
	sleep(10)
	qr_code_base64 = driver.execute_script('return document.getElementsByClassName("_2RT36")[0].getElementsByTagName("CANVAS")[0].toDataURL("image/png");')
    #qr_code = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/img')
	sleep(2)
	try:
		#return {'qrCode': qr_code.get_attribute('src')}, 200
		return {'qrCode': qr_code_base64}, 200
	except NoSuchElementException:
		return {'message': 'QR-Code não encontrado'}, 400
	except:
		return 400

def send_v1(numero, texto):
    global driver
    driver.get('https://web.whatsapp.com/send?phone=' + numero + '&text=' + texto)
    sleep(5)
    try:
        button = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        while not len(button) > 0:
            button = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
            sleep(2)
        button = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        button.click()
        sleep(2)
        return 200
    except NoSuchElementException:
        return 400

def send_v2(nome, texto):
    global driver
    try:
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome))
        user.click()

        msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div')

        msg_box.send_keys(texto)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()
        sleep(2)
        return 200

    except NoSuchElementException:
        return 400

def readMessages():
    global driver
    try:
        unread = driver.find_elements_by_class_name("_1ZMSM")  # O botão verde diz que a mensagem é nova
        unread = driver.find_elements_by_class_name("P6z4j")
        name, message = '', ''
        if len(unread) > 0:
            ele = unread[-1]
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(ele, 0, -30)  # vai um pouco à esquerda do botão verde

            # Clica três vezes, que garante que a janela do usuário abriu (a conversa)
            try:
                action.click()
                action.perform()
                action.click()
                action.perform()
            except Exception as e:
                pass

            try:
                # Tenta exibir última mensagem recebida
                name = driver.find_element_by_class_name("_19vo_").text
                message_div = driver.find_elements_by_class_name('-N6Gq')
                lenght_div = len(message_div)
                message = message_div[lenght_div - 1].text.lower()
                click_out = driver.find_elements_by_class_name('_3Jvyf')
                click_out.click()
                return name + ": " + message + '\n'
            except Exception as e:
                print(e)
                pass
        sleep(1)

    except NoSuchElementException:
        print('\n Sem mensagens novas. \n')

def screenshot():
    global driver
    printScreen = driver.save_screenshot('static/print.png')
    try:
        return {'print': printScreen}, 200
    except NoSuchElementException:
        return {'message': 'Print não pôde ser efetuado.'}, 400

#def sendFile (name, base64):
def sendFile(name, link):
    #_, b64data = base64.split(',')
    #b64data = bytes(b64data, encoding="ascii")
    #print(b64data)
    #with open("static/arquivo.png", "wb") as fh:
    #    fh.write(base64.decodebytes(b64data))
    #    fh.close()

    link = "http://dev.ssotica.com.br/api/v1/comprovantes/ordemServico/" + link
    base_dir = "./"
    path_to_pdf = os.path.join(base_dir, "arquivo.pdf")
    urllib.request.urlretrieve(link, path_to_pdf)

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

def sendFile_nameless(numero, link):
    link = "http://dev.ssotica.com.br/api/v1/comprovantes/ordemServico/" + link
    base_dir = "./"
    path_to_pdf = os.path.join(base_dir, "arquivo.pdf")
    urllib.request.urlretrieve(link, path_to_pdf)
    driver.get('https://web.whatsapp.com/send?phone=' + numero)
    sleep(5)
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