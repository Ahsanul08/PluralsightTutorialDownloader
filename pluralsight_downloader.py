import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
#import urllib
import urllib.request
import sys

root_directory = '/home/ahsanul/Downloads/Pluralsight/' 


username = "<username>"
password = "<password>"
root_url = '/library/courses/python-desktop-application-development/table-of-contents'


def get_logged_in_session(redirect):
    driver = webdriver.Firefox()
    driver.get("https://app.pluralsight.com/id?redirectTo=" + redirect)
    username = driver.find_element_by_xpath("//label[@for='Username']")
    password = driver.find_element_by_xpath("//label[@for='Password']")
    login_button = driver.find_element_by_xpath("//button[@id='login']")
    username.send_keys(username)
    password.send_keys(password)
    login_button.send_keys(Keys.RETURN)
    return driver

driver = get_logged_in_session(root_url)

time.sleep(15)

root_directory += driver.find_element_by_xpath("//h1[@class='course-hero__title']").get_attribute("textContent")

names_of_directories = driver.find_elements_by_xpath("//li[@class='accordian__section']")

assert len(names_of_directories) == 5

filename_list =[]

for first_index, name  in  enumerate(names_of_directories):
    dir_name = name.find_element_by_xpath("div/h3/a").text
    print(dir_name)
    
    current_node = '{}/{}.{}'.format(root_directory,first_index+1,dir_name) 
    if not os.path.exists(current_node):
        os.makedirs(current_node)
    assert os.path.exists(current_node)
    
    for second_index, element in enumerate(name.find_elements_by_xpath("div[@class='accordian__content']/ul/li/a[@target='psplayer']")):
        url = urllib.parse.quote(element.get_attribute("href"), safe = '') 
        driver1 = get_logged_in_session(url)
        time.sleep(15)
        if not filename_list:
            filename_list = [[i.get_attribute('textContent') for i in elem.find_elements_by_xpath("ul/li/h3")] for elem in driver1.find_elements_by_xpath("//div[@class='modules']/section")]
            print(filename_list)
        download_url = driver1.find_element_by_tag_name("video").get_attribute("src")
        driver1.quit()
        urllib.request.urlretrieve(download_url, '{}/{}{}.webm'.format(current_node, second_index+1, filename_list[first_index][second_index]))
        print("Goes next")
        
driver.quit()
