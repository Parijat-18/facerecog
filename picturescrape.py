from lib2to3.pgen2 import driver
import os
import time
import wget
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class pinterestScraper:
    def __init__(self):
        serv = Service("C:\Program Files (x86)\chromedriver.exe")
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs' , prefs)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.name = ""
        self.driver = webdriver.Chrome(service=serv , options=options)
        self.driver.get("https://in.pinterest.com/")

    def login(self ,email , password):
        WebDriverWait(self.driver,30).until(
            EC.presence_of_element_located((By.XPATH , "//button[@tabindex='0']"))
        ).click()
        WebDriverWait(self.driver , 10).until(
            EC.presence_of_element_located((By.XPATH , "//input[@type='email']"))
        ).send_keys(email)
        WebDriverWait(self.driver , 10).until(
            EC.presence_of_element_located((By.XPATH , "//input[@type='password']"))
        ).send_keys(password)
        WebDriverWait(self.driver , 10).until(
            EC.presence_of_element_located((By.XPATH , "//button[@type='submit']"))
        ).click()
        time.sleep(5)

    def search_init(self , name , append=""):
        self.name = f"{name} {append}"
        search = WebDriverWait(self.driver , 30).until(
            EC.presence_of_element_located((By.XPATH , "//input[@name='searchBoxInput']"))
        )
        search.clear()
        search.send_keys(name)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

    def get_photos(self , max , folder_path=os.getcwd()):
        total_imgs = 0
        imgs = []
        while total_imgs - 1 < max:
            img_elements = self.driver.find_elements(By.TAG_NAME , "img")
            for element in img_elements:
                imgs.append(element.get_attribute('src'))
            imgs = imgs[1:]
            total_imgs += len(imgs)
            self.driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(3)
            name = "_".join(self.name.split(" ")[:2]).lower()
        if not os.path.exists(os.path.join(folder_path , name)):
            os.mkdir(os.path.join(folder_path , name))
        for img in imgs:
            wget.download(img , os.path.join(folder_path , name , str(uuid.uuid4()) + ".jpg"))
        self.driver.find_element(By.XPATH , "//button[@aria-label='Remove search input']").click()
    def close(self):
        self.driver.close()


if __name__ == "__main__":
    webscraper = pinterestScraper()

