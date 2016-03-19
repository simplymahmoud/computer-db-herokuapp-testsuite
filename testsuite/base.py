# -*- coding: utf-8 -*-
import unittest


class BaseTest(unittest.TestCase):

    def get_dropdown_items(self):
        '''
        Utility method to get all company drop down items

        :return: list of available company names
        '''
        items = []
        element = self.driver.find_element_by_id('company')
        for option in element.find_elements_by_tag_name('option'):
            if option.text != '-- Choose a company --':
                items.append(option.text)
        return items

    def validate_add_alert(self, computer_name):
        '''
        Utility method to validate alert message after adding new computer

        :param computer_name: computer name to validate
        '''
        alert = self.driver.find_element_by_xpath('//div[@class="alert-message warning"]')
        self.assertEqual(alert.text, u'Done! Computer %s has been created' % computer_name)

    def validate_delete_alert(self):
        '''
        Utility method to validate alert message after adding delete computer

        '''
        alert = self.driver.find_element_by_xpath('//div[@class="alert-message warning"]')
        self.assertEqual(alert.text, u'Done! Computer has been deleted')

    def validate_update_alert(self, computer_name):
        '''
        Utility method to validate alert message after adding update computer

        :param computer_name: computer name to validate
        '''
        alert = self.driver.find_element_by_xpath('//div[@class="alert-message warning"]')
        self.assertEqual(alert.text, u'Done! Computer %s has been updated' % computer_name)

    def set_fields(self, field_value_list):
        '''
        Utility method to set multiple fields with different values

        :param field_value_list: list of tuples (field_id, value)
        '''
        for (field_id, value) in field_value_list:
            field = self.driver.find_element_by_id(field_id)
            #not allowed to clear drop down
            if field.tag_name != 'select':
                field.clear()
            field.send_keys(value)

    def verify_fields_text(self, field_value_list):
        '''
        Utility method to verify that field(s) are populated with the expected value

        :param field_value_list: list of tuples (field_id, expected_value)
        '''
        for (field_id, expected_value) in field_value_list:
            field = self.driver.find_element_by_id(field_id)
            if field.tag_name == 'select':
                self.assertEqual(
                        field.find_element_by_xpath('//option[@selected=""]').text, expected_value)
            else:
                self.assertEqual(field.get_attribute('value'), expected_value)

    def press_button(self, button):
        '''
        Utility method to perform click action on a specific button

        :param button: tuple (find_element_by, value_of_by_attribute)
        '''
        self.driver.find_element(button[0], button[1]).click()

    def retrive_computer(self, name):
        '''
        Utility method to get computer link

        :param name: computer name
        '''
        search_name = str(name)
        if len(search_name) > 20:
            search_name = search_name[:20]
        self.driver.get(self.MAIN_URL)
        self.set_fields([('searchbox', search_name)])
        self.driver.find_element_by_id('searchbox').submit()
        link = self.driver.find_element_by_partial_link_text(search_name)
        self.driver.get(link.get_attribute('href'))

    def delete_computer(self, name):
        '''
        Utility method to delete computer through UI, used mainly for cleaning up in tearing down

        :param name: computer name
        '''
        self.retrive_computer(name)
        self.press_button(self.element_button['delete_computer'])

        