from nose_parameterized import parameterized
from base import BaseTest
import uuid

from selenium.common.exceptions import NoSuchElementException


class TestAdd(BaseTest):

    def setUp(self):
        super(TestAdd, self).setUp()
        self.driver.get(self.MAIN_URL)
        self.to_be_deleted = []
        self.press_button(self.element_button['add_computer'])
        self.assertEquals(self.driver.current_url, self.ADD_NEW_COMPUTERS_URL)

    def tearDown(self):
        if hasattr(self, 'to_be_deleted') and self.to_be_deleted:
            for computer in self.to_be_deleted:
                self.delete_computer(computer)
        super(TestAdd, self).tearDown()

    def test001_add_computer_with_all_valid_company_field(self):
        '''CDB1: Test add new computer with all available company names values'''
        for company_name in self.get_dropdown_items():
            computer_name = str(uuid.uuid4())
            self.set_fields([('name', computer_name),
                             ('introduced', '2014-09-16'),
                             ('discontinued', '2015-08-13'),
                             ('company', company_name)])
            self.press_button(self.element_button['create_computer'])
            self.assertEquals(self.driver.current_url, self.MAIN_URL)
            self.validate_add_alert(computer_name)
            self.press_button(self.element_button['add_computer'])
            self.to_be_deleted.append(computer_name)

    @parameterized.expand([('normal name', str(uuid.uuid4())),
                           ('long name', 'B'*1000),
                           ('numeric name', 9876543210),
                           ('special chars name', '+_=-)(*&^#@!~`{}[];\',.<>\/')])
    def test002_add_computer_by_name_field(self, _, computer_name):
        '''CDB2: Test add new computer with different computer name values'''
        self.set_fields([('name', computer_name)])
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(computer_name)
        self.to_be_deleted.append(computer_name)

    def test003_add_computer_by_empty_name_field(self):
        '''CDB3: Test add new computer with empty name'''
        self.press_button(self.element_button['create_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u'Computer name\nRequired')

    def test004_cancel_add_computer_by_empty_fields(self):
        '''CDB4: Test cancel add new computer with all fields empty'''
        self.press_button(self.element_button['cancel'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_xpath,
                          '//div[@class="alert-message warning"]')

    @parameterized.expand([('valid', 'valid computer', '2014-11-05', '2015-11-05'),
                           ('invalid', '', '05-11-2014', 'date')])
    def test005_cancel_add_computer_with_data_field(self, _, name, introduced_date, discontinued_date):
        '''CDB5: Test cancel add new computer with all fields populated with valid/invalid data'''
        self.set_fields([('name', name),
                         ('introduced', introduced_date),
                         ('discontinued', discontinued_date),
                         ('company', self.get_dropdown_items()[0])])
        self.press_button(self.element_button['cancel'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_xpath,
                          '//div[@class="alert-message warning"]')

    def test006_add_computer_with_valid_introduced_discontinued_date_field(self):
        '''CDB6: Test add new computer with valid introduced/discontinued dates'''
        computer_name = str(uuid.uuid4())
        self.set_fields([('name', computer_name),
                         ('introduced', '2014-09-15'),
                         ('discontinued', '2015-09-15')])
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(computer_name)
        self.to_be_deleted.append(computer_name)

    @parameterized.expand([('non_exists_date', '2013-02-30'),
                           ('wrong_format', '15-09-2015'),
                           ('zeros', '0000-00-00'),
                           ('wrong_delimiter', '2015_09_15'),
                           ('chars', 'xxxx-xx-xx'),
                           ('string', str(uuid.uuid4())),
                           ('number', 123456789.0),
                           ('wrong_date', '2013-13-13')])
    def test007_add_computer_with_invalid_introduced_date_field(self, _, introduced_date):
        '''CDB7: Test add new computer with different invalid introduced date values'''
        self.set_fields([('name', str(uuid.uuid4())),
                         ('introduced', introduced_date),
                         ('discontinued', '2014-09-15')])
        self.press_button(self.element_button['create_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u"Introduced date\nDate ('yyyy-MM-dd')")

    @parameterized.expand([('non_exists_date', '2013-02-30'),
                           ('wrong_format', '15-09-2015'),
                           ('zeros', '0000-00-00'),
                           ('wrong_delimiter', '2015_09_15'),
                           ('chars', 'xxxx-xx-xx'),
                           ('string', str(uuid.uuid4())),
                           ('number', 123456789.0),
                           ('wrong_date', '2013-13-13')])
    def test008_add_computer_with_invalid_discontinued_date_field(self, _, discontinued_date):
        '''CDB8: Test add new computer with different invalid discontinued date values'''
        self.set_fields([('name', str(uuid.uuid4())),
                         ('introduced', '2014-09-15'),
                         ('discontinued', discontinued_date)])
        self.press_button(self.element_button['create_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u"Discontinued date\nDate ('yyyy-MM-dd')")

