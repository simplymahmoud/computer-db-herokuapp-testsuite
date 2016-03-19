from nose_parameterized import parameterized
from base import BaseTest
import uuid


class TestGet(BaseTest):      

    def setUp(self):
        super(TestGet, self).setUp()
        self.driver.get(self.MAIN_URL)
        self.to_be_deleted = []

    def tearDown(self):
        if hasattr(self, 'to_be_deleted') and self.to_be_deleted:
            for computer in self.to_be_deleted:
                self.delete_computer(computer)
        super(TestGet, self).tearDown()

    @parameterized.expand([('normal name', str(uuid.uuid4())),
                           ('long name', 'C'*1000),
                           ('special chars name', '+_=-)(*&^#@!~`{}[];\',.<>\/')])
    def test009_get_existing_computer(self, _, name):
        '''CDB9: Test get computer with different computer name values'''
        self.driver.get(self.ADD_NEW_COMPUTERS_URL)
        self.search_fields = [('name', name),
                             ('introduced', '2014-11-05'),
                             ('discontinued', '2015-11-05'),
                             ('company', self.get_dropdown_items()[0])]
        self.set_fields(self.search_fields)
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(name)
        self.to_be_deleted.append(name)
        self.set_fields([('searchbox', name)])
        self.driver.find_element_by_id('searchbox').submit()
        link = self.driver.find_element_by_partial_link_text(name)
        self.driver.get(link.get_attribute('href'))
        self.verify_fields_text(self.search_fields)

    def test010_get_non_existing_computer(self):
        '''CDB10: Test get non existing computer'''
        self.driver.get(self.MAIN_URL)
        self.set_fields([('searchbox', str(uuid.uuid4()))])
        self.driver.find_element_by_id('searchbox').submit()
        search_result = self.driver.find_element_by_xpath('//div[@class="well"]')
        self.assertEqual(search_result.text, u'Nothing to display')
