# Copyright 2020 Avinash S Sah

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from constants import constants
from helpers import wait_for, mail_qr, get_text, create_structure, filter_data, is_new_event


class BotRex:
    listen: bool = True

    QR_CODE: str = "qr_code.png"
    tasks: list = []

    def __init__(self, chrome_driver_path: str, chrome_binary_path: str, resolve_tasks_func, run_headless=False) -> None:
        self.options: ChromeOptions = Options()
        self.options.binary_location: ChromeBinaryLocation = chrome_binary_path
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument(constants["USER_AGENT"])
        if run_headless:
            self.options.add_argument("--headless")

        self.driver: ChromeDriver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=self.options)

        self.resolve_tasks_func: function = resolve_tasks_func

    def login(self, mail_adderss: str, mail_password: str, mail_qr_to: str, debug_mode=False) -> None:
        self.driver.get(constants["URL"])
        wait_for(self.driver, constants["QR_ELEMENT"])

        if not debug_mode:
            self.driver.save_screenshot(self.QR_CODE)
            mail_qr(mail_adderss, mail_password,
                    mail_qr_to, self.QR_CODE)

        wait_for(self.driver, constants["WA_Main_Page"])

    def run(self, listenables: list, command_prefix: str) -> None:
        old_text_chat_elements: list = []

        while self.listen:
            selenium_chat_elements: list[WebElement] = self.driver.find_elements_by_xpath(
                constants["CHAT_LIST"])
            text_chat_elements: list = get_text(selenium_chat_elements)
            new_event: bool = is_new_event(text_chat_elements)

            if text_chat_elements != old_text_chat_elements and new_event:
                new_text_chat_elements: list = [
                    data for data in text_chat_elements if data not in old_text_chat_elements]
                old_text_chat_elements = text_chat_elements

                structured_data: list = create_structure(
                    new_text_chat_elements, listenables)
                print(structured_data)

                flitered_data: list = filter_data(
                    structured_data, command_prefix)

                for index, probable_task in enumerate(flitered_data):
                    new_task: bool = True

                    for task in self.tasks:
                        if task == probable_task:
                            new_task = False

                    if new_task:
                        self.tasks.append(flitered_data[index])
                        print(f"[NEW TASK] {flitered_data[index]}")

                if self.tasks:
                    for index, task in enumerate(self.tasks):
                        print(f"[WORKING ON THIS]{task}")
                        self.resolve_tasks_func(self, task)
                        self.tasks.pop(index)
                        print(f"[DONE AND REMOVING]{task}")

        self.quit_rex()

    def quit_rex(self) -> None:
        self.driver.close()
        self.driver.quit()
        self.driver.service.stop()


class RexActions:
    @ staticmethod
    def send_message(instance, send_to: str, message: str) -> None:
        send_to: str = f"'{send_to}'"
        instance.driver.find_element_by_xpath(
            f"//*[@title={send_to}]//ancestor::node()[5]").click()
        time.sleep(1)
        instance.driver.find_element_by_xpath(
            constants["TEXT_FIELD"]).send_keys(message)
        time.sleep(1)
        instance.driver.find_element_by_xpath(
            constants["SEND_BUTTON"]).click()

# TODO: //*[@title='Remove']

# TODO: //*[@title='Make group admin']
# TODO: //*[contains(text(), 'Make group admin')] 'CONFIRM BUTTON'

# TODO: //*[@title='Dismiss as admin']
