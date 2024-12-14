from time import sleep
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10

class TestNewVisitor(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text:str):
        table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        self.assertIn(row_text, [row.text for row in rows])

    def add_item_to_to_do_table(self, text:str):
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_home_page_returns_correct_title_page(self):
        self.assertIn("To-Do", self.browser.title)

    def test_home_page_returns_correct_h1(self):
        header_text: str = self.browser.find_element(by=By.TAG_NAME, value="H1").text
        self.assertIn("To-Do", header_text)

    def test_input_a_to_do_item_has_correct_placeholder(self):
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"), "Enter a to-do item"
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.add_item_to_to_do_table("Buy peacock feathers")
        self.add_item_to_to_do_table("Use peacock feathers to make a fly")
        self.wait_for_row_in_list_table("1:Buy peacock feathers")
        self.wait_for_row_in_list_table("2:Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_diferent_urls(self):
        self.add_item_to_to_do_table("Buy peacock feathers")
        self.wait_for_row_in_list_table("1:Buy peacock feathers")
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)

        self.add_item_to_to_do_table("Buy milk")
        self.wait_for_row_in_list_table("1:Buy milk")
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
