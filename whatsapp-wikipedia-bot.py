from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import wikipedia as wiki

PATH = "/opt/chromedriver"
CONTACT = 'Bhai Ali' #Your contact name 
driver = webdriver.Chrome(PATH)

driver.get('https://web.whatsapp.com')
print(driver.title)

# following works
elem = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{CONTACT}" ]')))

actions = ActionChains(driver)
actions.click(elem).perform()

# incoming = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'copyable-text'))) [contains(text(), 'Shakeel Czn')]
incoming = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, f'//div[contains(@data-pre-plain-text, "{CONTACT}")]')))
#print(incoming[len(incoming) - 3].text) # Latest received message

received_msgs = len(incoming)

def new_msg_received():
    incoming = driver.find_elements_by_xpath(f'//div[contains(@data-pre-plain-text, "{CONTACT}")]')
    if len(incoming) > received_msgs:
        return True
    else:
        return False

def send_message(text):
    input_box = driver.find_elements_by_class_name('copyable-text')
    input_box = input_box[len(input_box) - 1]
    input_box.click()
    input_box.send_keys(text, Keys.RETURN)
    incoming = driver.find_elements_by_xpath(f'//div[contains(@data-pre-plain-text, "{CONTACT}")]')
    received_msgs = len(incoming)

while True:
       if new_msg_received():
        try:
            incoming = driver.find_elements_by_xpath(f'//div[contains(@data-pre-plain-text, "{CONTACT}")]')
            received_msgs = len(incoming)
            last_msg = incoming[received_msgs - 1].text
            print(last_msg)
            summary = wiki.page(last_msg).content[:1500]
            send_message(summary)
        except Exception as e:
            summary = str(e)
            send_message(summary)
            print(e)
            pass