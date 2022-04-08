from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import *
import logging
import datetime

class fb_auto_reply:
    __logger__ = logging.getLogger(__name__)

    def __init__(self,config:dict):
        self.__driver__ = webdriver.Chrome(executable_path=env_var['chrome_driver_path'])
        self.__login_name__ = env_var['username']
        self.__pwd__ = env_var['pwd']
        self.frequency = env_var.get('check_freq',10)
        self.timeout = env_var.get('timeout',5)

        # config logger
        self.__logger__.setLevel(logging.INFO)
        console_stream = logging.StreamHandler()
        console_stream.setLevel(logging.INFO)
        console_stream.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s [%(name)s] - %(message)s"))
        self.__logger__.addHandler(console_stream)
        self.__logger__.info("Initialized fb_auto_reply")

    def login(self):
        try:
            self.__driver__.get("https://www.messenger.com/t/1464301308/")
            login_email = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.ID,"email")))
            login_pwd = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.ID,"pass")))

            login_email.clear()
            login_pwd.clear()

            login_email.send_keys(self.__login_name__)
            login_pwd.send_keys(self.__pwd__)
            self.__driver__.find_element_by_id('loginbutton').send_keys(Keys.ENTER)
        except TimeoutException:
            self.__logger__.critical("timeout!! cannot load login page")

    def bot_start(self):
        while(True):
            self.__logger__.info("START SCANNING")
            sleep(3)
            self.scan_mailbox(self._reply_to_msg)

    def _reply_to_msg(self, contact_DOM: WebElement, msg: str) -> dict:
        # Select contact
        contact_DOM.click()
        sleep(1)
        contact_name =  WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div[aria-label][role='main'] span a[role='link']")))
        # Reply message
        msgBox = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div[aria-label='Message']")))
        msgBox.click()
        msgBox.send_keys(msg)
        msgBox.send_keys(Keys.ENTER)
        return {'contact': contact_name.text , 'reply_msg': msg}

    def scan_mailbox(self, msg_handler=None):
        contact_list = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='MWJewelThreadListContainer']")))
        blur_DOM = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='navigation'] h1")))
        try:
            contacts = WebDriverWait(self.__driver__, self.timeout).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='mwthreadlist-item-open']")))
            for contact in contacts:
                try:
                    unread_handler = contact.find_element(by=By.CSS_SELECTOR,value="div[aria-label='Mark as read']")
                    if unread_handler is not None:
                        self.__logger__.info("replied to {contact} with {reply_msg}".format(**msg_handler(contact, 'BOT msg')))
                except NoSuchElementException:
                    pass
                except StaleElementReferenceException:
                    # Message possibly read somewhere else
                    pass
                blur_DOM.click()
        except TimeoutException:
            # Cannot find any existing chat
            pass
        blur_DOM.click()
    
            


    def __enter__(self):
        return self

    def __exit__(self, exc_type,exc_value,traceback):
        self.__driver__.quit()
    


if __name__ == '__main__':
    env_var = {
        'chrome_driver_path': r"I:\to_del\fb_reply\driver\chromedriver.exe",
        'username': ' ',
        'pwd': '',
        'timeout': 10,
    }

    bot = fb_auto_reply(env_var)
    bot.login()
    bot.bot_start()