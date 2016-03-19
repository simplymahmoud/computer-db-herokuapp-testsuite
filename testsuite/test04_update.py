from nose_parameterized import parameterized
from base import BaseTest
import uuid

from selenium.common.exceptions import NoSuchElementException


class TestUpdate(BaseTest):

    def setUp(self):
        super(TestUpdate, self).setUp()
        self.driver.get(self.MAIN_URL)
        self.press_button(self.element_button['add_computer'])
        self.assertEquals(self.driver.current_url, self.ADD_NEW_COMPUTERS_URL)
        self.computer_name = str(uuid.uuid4())
        self.set_fields([('name', self.computer_name),
                         ('introduced', '2014-08-13'),
                         ('discontinued', '2015-08-13'),
                         ('company', self.get_dropdown_items()[0])])
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(self.computer_name)
        self.retrive_computer(self.computer_name)       

    def tearDown(self):
        if hasattr(self, 'computer_name') and self.computer_name:
            self.delete_computer(self.computer_name)
        super(TestUpdate, self).tearDown()

    def test013_update_computer_by_company(self):
        '''CDB13: Test update company with another value'''
        self.set_fields([('company', self.get_dropdown_items()[2])])
        self.press_button(self.element_button['update_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_update_alert(self.computer_name)

    @parameterized.expand([('string', str(uuid.uuid4())),
                           ('long', 'D'*1000),
                           ('number', 123456789.0),
                           ('special_chars', '+_=-)(*&^#@!~`{}[];\',.<>\/')])
    def test014_update_computer_name(self, _, computer_name):
        '''CDB14: Test update computer name with different vaild values'''
        self.set_fields([('name', computer_name)])
        self.press_button(self.element_button['update_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_update_alert(computer_name)
        self.computer_name = computer_name

    def test015_update_computer_name_to_empty(self):
        '''CDB15: Test update after clearing computer name'''
        self.set_fields([('name', '')])
        self.press_button(self.element_button['update_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u'Computer name\nRequired')

    def test016_update_computer_without_changes(self):
        '''CDB16: Test update computer without changes'''
        self.press_button(self.element_button['update_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_update_alert(self.computer_name)

    def test017_update_computer_canceled(self):
        '''CDB17: Test cancel update without changes'''
        self.press_button(self.element_button['cancel'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_xpath,
                          '//div[@class="alert-message warning"]')

    @parameterized.expand([('valid', 'valid name', '2014-08-13', '2015-08-13'),
                           ('invalid', '', '05-11-2014', 'text')])
    def test018_cancel_update_with_data(self, _, name, introduced_date, discontinued_date):
        '''CDB18: Test cancel update after change fields with valid/invalid values'''
        company = self.get_dropdown_items()[0]
        self.set_fields([('name', name),
                         ('introduced', introduced_date),
                         ('discontinued', discontinued_date),
                         ('company', company)])
        self.press_button(self.element_button['cancel'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_xpath,
                          '//div[@class="alert-message warning"]')

    @parameterized.expand([('empty', ''),
                           ('valid_format', '2005-05-05')])
    def test019_update_computer_by_introduced_date(self, _, introduced_date):
        '''CDB19: Test update introduced date with different valid values'''
        self.set_fields([('name', self.computer_name),
                         ('introduced', introduced_date)])
        self.press_button(self.element_button['update_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_update_alert(self.computer_name)

    @parameterized.expand([('empty', ''),
                           ('valid_format', '2005-05-05')])
    def test020_update_computer_by_discontinued_date(self, _, discontinued_date):
        '''CDB20: Test update discontinued date with different valid values'''
        self.set_fields([('introduced', '2015-10-25'),
                         ('discontinued', discontinued_date)])
        self.press_button(self.element_button['update_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_update_alert(self.computer_name)

    @parameterized.expand([('non_exist_date', '2013-02-30'),
                           ('wrong_format', '15-09-2015'),
                           ('zeros', '0000-00-00'),
                           ('wrong_delimiter', '2015_09_15'),
                           ('chars', 'xxxx-xx-xx'),
                           ('text', str(uuid.uuid4())),
                           ('number', 123456789.0),
                           ('wrong_date', '2013-13-13')])
    def test021_update_computer_by_invalid_introduced_date(self, _, introduced_date):
        '''CDB21: Test update computer with different invalid introduced date values'''
        self.set_fields([('introduced', introduced_date)])
        self.press_button(self.element_button['update_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u"Introduced date\nDate ('yyyy-MM-dd')")

    @parameterized.expand([('non_exist_date', '2013-02-30'),
                           ('wrong_format', '15-09-2015'),
                           ('zeros', '0000-00-00'),
                           ('wrong_delimiter', '2015_09_15'),
                           ('chars', 'xxxx-xx-xx'),
                           ('text', str(uuid.uuid4())),
                           ('number', 123456789.0),
                           ('wrong_date', '2013-13-13')])
    def test022_update_computer_by_invalid_discontinued_date(self, _, discontinued_date):
        '''CDB22: Test update (discontinued_date) with different invalid values'''
        self.set_fields([('introduced', '2015-10-25'),
                         ('discontinued', discontinued_date)])
        self.press_button(self.element_button['update_computer'])
        # Check for error
        error_field = self.driver.find_element_by_xpath('//div[@class="clearfix error"]')
        self.assertEqual(error_field.text, u"Discontinued date\nDate ('yyyy-MM-dd')")

