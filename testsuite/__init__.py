# -*- coding: utf-8 -*-
from base import BaseTest
from selenium import webdriver
from selenium.webdriver.common.by import By


#base url
base_url = 'http://computer-database.herokuapp.com/'
#main url
BaseTest.MAIN_URL = base_url + 'computers'
#add new computer url
BaseTest.ADD_NEW_COMPUTERS_URL = base_url + 'computers/new'

#element paths we use during test
BaseTest.element_button = {'add_computer': (By.ID, 'add'),
                           'search_submit': (By.ID, 'searchsubmit'),
                           'create_computer': (By.XPATH, '//input[@value="Create this computer"]'),
                           'update_computer': (By.XPATH, '//input[@value="Save this computer"]'),
                           'delete_computer': (By.XPATH, '//input[@value="Delete this computer"]'),
                           'next_page': (By.LINK_TEXT, 'Next →'),
                           'previous_page': (By.LINK_TEXT, '← Previous'),
                           'cancel': (By.LINK_TEXT, 'Cancel')}

def setUp():
    BaseTest.driver = webdriver.Firefox()


def tearDown():
    BaseTest.driver.quit()