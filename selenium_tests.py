import logging
import os
import django
from selenium import webdriver
from django.urls import reverse
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium.common.exceptions import TimeoutException
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'first_django.settings'
django.setup()

class UserRegistrationTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Edge()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.live_server_url = 'http://localhost:8000'
        logging.basicConfig(level=logging.INFO)

    def test_user_registration_form(self):
        test_data = [
            {'username': 'testuser17', 'email': 'testuser1@example.com', 'password': 'DJSRT@1234'},
            {'username': 'testuser18', 'email': 'testuser2@example.com', 'password': 'DJSRT@1235'},
            {'username': 'testuser19', 'email': 'testuser3@example.com', 'password': 'DJSRT@123567'},
        ]

        for data in test_data:
            with self.subTest(data=data):
                self.browser.get(self.live_server_url + reverse('register'))
                #time.sleep(2)  # Pause for 2 seconds

                # Log the current URL before form submission
                logging.info(f"Current URL: {self.browser.current_url}")

                # Fill out the registration form
                self.browser.find_element(By.NAME, 'username').send_keys(data['username'])
                self.browser.find_element(By.NAME, 'email').send_keys(data['email'])
                self.browser.find_element(By.NAME, 'password1').send_keys(data['password'])
                self.browser.find_element(By.NAME, 'password2').send_keys(data['password'])

                time.sleep(2)  # Pause for 2 seconds before clicking the submit button

                submit_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()

                try:
                    WebDriverWait(self.browser, 10).until(
                        EC.url_contains(reverse('login'))
                    )
                except TimeoutException:
                    logging.error("Timeout waiting for login page to load after registration")
                    raise

                logging.info(f"Current URL after submit: {self.browser.current_url}")
                time.sleep(2)

                self.assertIn(reverse('login'), self.browser.current_url)

if __name__ == '__main__':
    unittest.main()
