from selenium import webdriver 
import time
import pyautogui 
from selenium.webdriver.common.keys import Keys
import os
options = webdriver.ChromeOptions() 
class Letgo() :
    
    def __init__(self,category_name,price,title,description=None,share_facebook=None) :
        self.main_url = 'https://www.letgo.com/tr-tr'
        self.category = category_name
        self.price , self.title , self.description  = price , title , description
        self.share_facebook = share_facebook
        try:
            options.add_argument(fr'user-data-dir={os.path.expanduser("~")}\AppData\Local\Google\Chrome\User Data') 
            self.driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver.exe',
                chrome_options=options)
        except :
            self.driver.close()
            print(f'Please Close Browser and Try Again.')
      
    def category_selection(self) :
        category_number = 9
        if self.category == "elektronik" :
            category_number = 1
        elif self.category == 'spor' : 
            category_number = 2
        elif self.category == 'araba' : 
            category_number = 3   
        elif self.category == 'motosiklet' : 
            category_number = 4
        elif self.category == 'ev' : 
            category_number = 5  
        elif self.category == 'moda' : 
            category_number = 6
        elif self.category == 'bebek' : 
            category_number = 7
        elif self.category == 'film' : 
            category_number = 8

        
        return category_number        
        
    def sale_first_click(self) :
        self.driver.get(self.main_url)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/header/div/div/div[3]/button/span[1]').click()
        time.sleep(5)
        return self.driver 
    
    def select_category(self) :
        category_number = self.category_selection()
        self.driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div[2]/div/div/div[{str(category_number)}]').click()
        time.sleep(3)
        return self.driver

    def get_pic_from_file(self) :
        pics = []
        p = open('pic.txt','r',encoding='utf-8').readlines()
        
        for pic in p :
            pics.append(pic.replace('\n',''))
            
        return pics
             
    def add_pic(self) :
        pics = self.get_pic_from_file()
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div').click()
        time.sleep(1)
        pyautogui.write(pics[0])
        pyautogui.press('enter')
        time.sleep(5)
        if len(pics) > 1 :
            for i in range(len(pics)-1) :
                if i < 2 :
                    self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]').click()
                if i > 1 :
                    try:
                        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[3]').click()
                    except:
                        pass
                    try:
                        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]').click()
                    except:
                        pass   
                time.sleep(2)
                pyautogui.write(pics[i+1])
                time.sleep(2)
                pyautogui.press('enter')
                time.sleep(2)

        return self.driver
    
    def add_details(self) :
        self.driver.find_element_by_name('price').send_keys(self.price)
        time.sleep(1)
        self.driver.find_element_by_name('name').send_keys(self.title)
        time.sleep(1)
        if self.description != None :
            self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[4]/div[1]/div/div/textarea').send_keys(self.description)
            time.sleep(1)
        if self.share_facebook != None :
            self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div[1]/span/span').click()
            time.sleep(1)
            
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]').click()
        
        time.sleep(3)
        
        return self. driver
    
    def close_driver(self) :
        self.driver.close()
            
        