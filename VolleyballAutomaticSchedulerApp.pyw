import datetime
import os
from subprocess import CREATE_NO_WINDOW
from time import sleep
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class VolleyballAutomaticSchedulerApp:
    def __init__(self, login:str, password:str):
        self.login = login
        self.password = password
        self.driver = self.__configureWebDriver()
        
    def __configureWebDriver(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        service = Service(ChromeDriverManager().install())
        service.creation_flags = CREATE_NO_WINDOW
        
        driver = webdriver.Chrome('chromedriver.exe', service=service, options=options)
        driver.implicitly_wait(10)
        
        return driver
        
    def run(self):
        
        self.driver.get('https://www.l7lifeclub.com.br/l7lifeclub/1/page/landing-page/login')

        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="idCpf"]'
        )
        elem.send_keys(self.login)

        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="idSenha"]'
        )
        elem.send_keys(self.password)

        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="view"]/app-landing-page/app-login-page/div[1]/evo-cadastro/div[1]/div/div/div/form/div[2]/div[2]/button'
        )
        elem.click()

        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="view"]/app-cliente/div/div/div[1]/ul/li[2]/a'
        )
        elem.click()

        elem = self.driver.find_element(
            By.XPATH, 
            '/html/body/app-root/app-aceitar-cookie/div[1]/div/div/div[2]/button'
        )
        elem.click()

        while True:
            elem = self.driver.find_element(
                By.XPATH, 
                '//*[@id="view"]/app-cliente/div/div/div[2]/app-agendas/div[2]/app-agenda/div[1]/div[1]/div[2]/div/span'
            )
            
            weekDays = ['SEG', 'SEX']
            
            if any(day in elem.get_attribute('innerText') for day in weekDays):
                break

            elem = self.driver.find_element(
                By.XPATH, 
                '//*[@id="view"]/app-cliente/div/div/div[2]/app-agendas/div[2]/app-agenda/div[1]/div[1]/div[2]/i[2]'
            )

            self.driver.execute_script("arguments[0].click();", elem)
            
        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="button-basic"]'
        )
        elem.click()

        elem = self.driver.find_element(
            By.XPATH, 
            '//*[@id="dropdown-basic"]/li[66]/a'
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(elem).perform()
        elem.click()

        sleep(2)

        elem = self.driver.find_elements(
            By.CSS_SELECTOR, 
            'section.card-agenda div > div.pt-2 > button'
        )

        now = datetime.datetime.now()

        if now.hour == 18 and 45 <= now.minute <= 59:
            elem[0].click()
        elif now.hour == 20 and 0 <= now.minute <= 59:
            elem[1].click()
        elif now.hour == 21 and 15 <= now.minute <= 59:
            elem[2].click()
        else:
            return
            
        elem = self.driver.find_element(
            By.CSS_SELECTOR, 
            '.modal-body .px-3 .btn'
        )
        elem.click()
        

if __name__ == '__main__':
    filePath = 'auth.json'
    login = ''
    password = ''
    if os.path.isfile(filePath):
        with open(filePath) as jsonFile:
            data = json.load(jsonFile)
            login = data['login']
            password = data['password']
    else:
        login = str(input('login: '))
        password = str(input('password: '))
        authDict = {
            'login': login,
            'password': password
        }
        authJson = json.dumps(authDict, indent=4)
        with open(filePath, 'w') as jsonFile:
            jsonFile.write(authJson)
            
    app = VolleyballAutomaticSchedulerApp('50242631894','Cl741852963@a')
    app.run()