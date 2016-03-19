from base import BaseTest
import uuid


class TestDelete(BaseTest):

    def setUp(self):
        super(TestDelete, self).setUp()
        self.driver.get(self.ADD_NEW_COMPUTERS_URL)
        computer_name = str(uuid.uuid4())
        self.search_fields = [('name', computer_name),
                             ('introduced', '2014-11-05'),
                             ('discontinued', '2015-11-05'),
                             ('company', self.get_dropdown_items()[0])]
        self.set_fields(self.search_fields)
        self.press_button(self.element_button['create_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_add_alert(computer_name)
        self.retrive_computer(computer_name)

    def test011_delete_existing_computer(self):
        '''CDB11: Test delete existing computer'''
        self.press_button(self.element_button['delete_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_delete_alert()

    def test012_access_deleted_computer_page(self):
        '''CDB12: Test access deleted computer page'''
        computer_url = self.driver.current_url
        self.press_button(self.element_button['delete_computer'])
        self.assertEquals(self.driver.current_url, self.MAIN_URL)
        self.validate_delete_alert()

        # Try to retrieve the computer after deletion
        self.driver.get(computer_url)
        self.assertEqual(self.driver.page_source, '')
        self.assertEqual(self.driver.title, '')
