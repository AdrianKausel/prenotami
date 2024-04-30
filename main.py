import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import logging
import yaml
import sys
import time
import random
import undetected_chromedriver as udc


load_dotenv()
logging.basicConfig(
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("./out.log"), logging.StreamHandler(sys.stdout)],
)

## Unix Log file
##logging.basicConfig(
##    format="%(levelname)s:%(message)s",
##    level=logging.INFO,
##    handlers=[logging.FileHandler("/tmp/out.log"), logging.StreamHandler(sys.stdout)],
#)

class Prenota:
    @staticmethod
    def check_file_exists(file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.isfile(file_path)

    @staticmethod
    def load_config(file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    @staticmethod
    def check_for_dialog(driver):
        try:
            # Wait for the popup to fully appear
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div/div")))
            # If the popup appears, click the 'OK' button
            ok_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ok')]")))
            driver.execute_script("arguments[0].click();", ok_button)
            logging.info(f"Timestamp: {str(datetime.now())} - Scheduling is not available right now.")
            return True
        except NoSuchElementException:
            logging.info(f"Timestamp: {str(datetime.now())} - Element WlNotAvailable not found. Start filling the forms.")
            return False


    @staticmethod
    def fill_citizenship_form(driver, user_config):
        try:
            while True:
                # Navigate directly to the booking page
                driver.get("https://prenotami.esteri.it/Services/Booking/4940")
                # Wait for the page to be fully loaded
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                if not Prenota.check_for_dialog(driver):
                    # If the appointment form appears, break the loop and proceed with the rest of the code
                    break
            # Rest of your code...
            return True
        except Exception as e:
            logging.info(f"Exception {e}")
            return False

    @staticmethod
    def fill_passport_form(driver, user_config):
        try:
            while True:
                # Navigate directly to the booking page
                driver.get("https://prenotami.esteri.it/Services/Booking/4940")
                # Wait for the page to be fully loaded
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                if not Prenota.check_for_dialog(driver):
                    # If the appointment form appears, break the loop and proceed with the rest of the code
                    break
            # Rest of your code...
            return True
        except Exception as e:
            logging.info(f"Exception {e}")
            return False

    @staticmethod
    def run():
        if Prenota.check_file_exists("files/residencia.pdf"):
            logging.info(
                f"Timestamp: {str(datetime.now())} - Required files available."
            )
            email = "email"
            password = "password"
            user_config = Prenota.load_config("parameters.yaml")
            print(user_config.get("full_address"))
            options = udc.ChromeOptions()
            options.headless = False
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = udc.Chrome(use_subprocess=True, options=options)
            driver.delete_all_cookies()

            try:
                driver.get("https://prenotami.esteri.it/")
                email_box = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "login-email"))
                )
                password_box = driver.find_element(By.ID, "login-password")
                email_box.send_keys(email)
                password_box.send_keys(password)
                time.sleep(4)
                button = driver.find_elements(
                    By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]"
                )
                button[0].click()
                logging.info(
                    f"Timestamp: {str(datetime.now())} - Successfully logged in."
                )
                time.sleep(10)
            except Exception as e:
                logging.info(f"Exception: {e}")

            for i in range(200):
                random_number = random.randint(1, 5)

                if user_config["request_type"] == "citizenship":
                    if Prenota.fill_citizenship_form(driver, user_config):
                        break
                elif user_config["request_type"] == "passport":
                    if Prenota.fill_passport_form(driver, user_config):
                        break

                time.sleep(random_number)

            user_input = input(
                f"Timestamp: {str(datetime.now())} - Go ahead and fill manually the rest of the process. "
                f"When finished, type quit to exit the program and close the browser. "
            )
            while True:
                if user_input == "quit":
                    driver.quit()
                    break
        else:
            logging.info(
                "Required files are not available. Check the required files in README.md file. Ending execution."
            )
            sys.exit(0)


if __name__ == "__main__":
    Prenota.run()
