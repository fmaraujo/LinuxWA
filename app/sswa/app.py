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
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

try:
    import autoit
except ModuleNotFoundError:
    pass

#from pyvirtualdisplay import Display

#display = Display(visible=0, size=(800, 600))
#display.start()

whatsapp_url = 'https://web.whatsapp.com/'

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugin-port=9222")
options.add_argument("--screen-size=1200x800")

driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=options.to_capabilities())
driver.implicitly_wait(1)


def connect():
	global driver
	driver.get(whatsapp_url)

	def wait_for_qrcode_read(limit):
		try:
			WebDriverWait(driver, 15).until(
				lambda d: d.find_element_by_css_selector('._1FPJ-._39gtr.app-wrapper-web')
			)
		except TimeoutException:
			if limit > 0:
				return wait_for_qrcode_read(limit - 1)
			else:
				return 400
		return 200

	return wait_for_qrcode_read(4)


def get_qr_code():
	global driver
	driver.get(whatsapp_url)

	qr_code = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/img')
	try:
		return {'qrCode': qr_code.get_attribute('src')}, 200
	except NoSuchElementException:
		return {'message': 'QR-Code não encontrado'}, 400
	except:
		return 400


def send_v1(numero, texto):
    global driver
    driver.get('https://api.whatsapp.com/send?phone=' + numero + '&text=' + texto)
    api_web = driver.find_element_by_xpath('//*[@id="action-button"]')
    api_web.click()
    sleep(2)

    try:
        button_api = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div/a')
        button_api.click()
        sleep(10)
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
        # Scroll till the end of the conversations
        #driver.execute_script("return arguments[0].scrollIntoView();")
        #find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div').send_keys(Keys.CONTROL + Keys.END)
        

        # Find the name and send the message
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


def schedul():
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
                # message_div = browser.find_elements_by_class_name('_1zGQT _2ugFP message-in')
                # print(message_div)
                lenght_div = len(message_div)
                message = message_div[lenght_div - 1].text.lower()

                click_out = driver.find_elements_by_class_name('_3Jvyf')
                click_out.click()
                # print('\n')
                return name + ": " + message + '\n'

            except Exception as e:
                print(e)
                pass

        sleep(1)

    except NoSuchElementException:
        print('\n Sem mensagens novas. \n')

def send_files(doc_filename):
    global driver
    # Attachment Drop Down Menu
    clipButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    sleep(1)

    # To send a Document(PDF, Word file, PPT)
    docButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    sleep(1)

    docPath = os.getcwd() + "\\arquivos\\" + doc_filename

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", (docPath))
    autoit.control_click("Open", "Button1")

    sleep(3)
    whatsapp_send_button = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()
