from nose_parameterized import parameterized
from base import BaseTest
import uuid

from selenium.common.exceptions import NoSuchElementException

class TestSearch(BaseTest):

    def setUp(self):
        super(TestSearch, self).setUp()
        self.driver.get(self.MAIN_URL)
        self.to_be_deleted = []

    def tearDown(self):
        if hasattr(self, 'to_be_deleted') and self.to_be_deleted:
            for computer in self.to_be_deleted:
                self.delete_computer(computer)
        super(TestSearch, self).tearDown()

    @parameterized.expand([('normal name', str(uuid.uuid4())),
                           ('long name', 'S'*1000),
                           ('special chars name', '+_=-)(*&^#@!~`{}[];\',.<>\/')])
    def test023_search_computer_by_name_field(self, _, computer_name):
        '''CDB23: Test search computer by different vaild names'''
        self.press_button(self.element_button['add_computer'])
        self.set_fields([('name', computer_name)])
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(computer_name)
        self.to_be_deleted.append(computer_name)
        self.driver.get(self.MAIN_URL)
        self.set_fields([('searchbox', computer_name)])
        self.press_button(self.element_button['search_submit'])
        link = self.driver.find_element_by_link_text(computer_name)
        self.assertEqual(link.text, computer_name)

    def test024_search_navigate_next_previous_page(self):
        '''CDB24: Test search navigate with next and previous pages'''
        for counter in range(2, 5):
            for _ in range(counter):
                self.press_button(self.element_button['next_page'])
            for _ in range(counter-1):
                self.press_button(self.element_button['previous_page'])

    def test025_search_non_existing(self):
        '''CDB25: Test search for a computer with non existing name'''
        computer_name = str(uuid.uuid4())
        self.set_fields([('searchbox', computer_name)])
        self.press_button(self.element_button['search_submit'])
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_link_text,
                          computer_name)
