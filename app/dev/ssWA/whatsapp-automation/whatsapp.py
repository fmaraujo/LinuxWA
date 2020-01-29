from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugin-port=9222")
options.add_argument("--screen-size=1200x800")
options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(ChromeDriverManager().install(
), desired_capabilities=options.to_capabilities())
driver.get("https://web.whatsapp.com")


def forward():
    element = driver.find_elements_by_class_name('Tkt2p')
    hov = ActionChains(driver).move_to_element(element[-1])
    hov.perform()
    forward = driver.find_element_by_class_name('_3kN0h')
    forward.click()
    but = driver.find_elements_by_class_name('_2dGjP')
    but[2].click()
    many = driver.find_elements_by_class_name('_1o1sm')
    mn = input('How many message you want to forward: ')
    for i in range(int(mn)):
        many[-i].click()

    forw = driver.find_elements_by_class_name('PNqfx')
    forw[3].click()
    while(True):
        to_name = input("The name of the person to forward this message: ")
        to = driver.find_element_by_xpath(
            '//span[@title = "{}"]'.format(to_name))
        to.click()
        ch = input("Someone else(yes/no): ")
        if ch == 'no':
            break
    cli = driver.find_element_by_class_name('eTCKi')
    cli.click()


while(True):
    name = input("Enter the name: ")
    msg = input("Enter the message: ")
    count = int(input("Enter the no of times to send the message: "))
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()
    for i in range(count):
        msg_box = driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div')
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_3M-N-')
        button.click()
    img = input("Do you want to sent images: ")
    if img == 'yes':
        print('You have only 15 seconds to choose the image')
        # clip = driver.find_elements_by_class_name('rAUz7')
        clip = driver.find_element_by_xpath(
            '//*[@id="main"]/header/div[3]/div/div[2]/div')
        # clip[4].click()
        clip.click()
        time.sleep(5)
        image_box = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]')
        image_box.click()

        #image_box.send_keys(filepath)

        time.sleep(15)
        li = driver.find_element_by_class_name('_3nfoJ')
        li.click()
    cho = input('Want to forward this message: ')
    if cho == 'yes' or cho == 'y':
        forward()
    choice = input("Do you want to try again: ")
    if(choice == 'no'):
        break
