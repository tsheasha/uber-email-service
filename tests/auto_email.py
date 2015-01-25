import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class EmailAutoTest(unittest.TestCase):

    def setUp(self):
        """
        Set up Driver to Firefox Driver
        """
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000/")
        self.assertIn("Uber Mail Service", self.driver.title)

    def test_create(self):
        """
        Test that a user can send an email
        """
        driver = self.driver
        elem = self.driver.find_element_by_id("from_email")
        elem.send_keys("tarek.sheasha@gmail.com")
        
        elem = self.driver.find_element_by_id("to_email")
        elem.send_keys("tarek.sheasha@gmail.com")
        
        elem = self.driver.find_element_by_id("subject")
        elem.send_keys("Test Subject")

        elem = self.driver.find_element_by_id("email_body")
        elem.send_keys("Automation Test")

        elem = self.driver.find_element_by_id("button-blue")
        elem.click()

        assert "Success! Your E-mail has been sent" in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
