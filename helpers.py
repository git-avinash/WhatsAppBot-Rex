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


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from email.message import EmailMessage
import smtplib
import imghdr
import re


def wait_for(webdriver, web_element: str) -> None:
    delay: int = 60
    try:
        WebDriverWait(webdriver, delay).until(
            EC.presence_of_element_located((By.XPATH, web_element)))
    except TimeoutException as e:
        print(e)


def mail_qr(mail_address: str, mail_password: str, mail_to: str, qr_image: str) -> None:
    EMAIL_ADDRESS: str = mail_address
    EMAIL_PASS: str = mail_password

    mail: EmailInit = EmailMessage()
    mail['Subject'] = 'QR Expires in 2 minutes'
    mail['From'] = EMAIL_ADDRESS
    mail['To'] = mail_to
    mail.set_content('QR Expires in 1 minute')

    with open(qr_image, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    mail.add_attachment(file_data, maintype='image',
                        subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(mail)


def get_text(selenium_chat_elements: list) -> list:
    text_data: list = []

    for single_element in selenium_chat_elements:
        text_data.append(single_element.text)

    return text_data


def is_new_event(text_chat_elements: list) -> bool:
    is_new: bool = True

    for chat_data in text_chat_elements:
        if chat_data.find("is typing…") != -1:
            is_new = False

        if chat_data.find("typing…") != -1:
            is_new = False

    return is_new


def create_structure(text_chat_elements: list, listenables: list) -> list:
    data: list = []

    for chat_element in text_chat_elements:
        is_listinable: bool = False
        chat_contents: list[str] = chat_element.split("\n")

        for listenable in listenables:
            if chat_contents[0] == listenable:
                is_listinable: bool = True
                break

        if is_listinable:
            chat_contents_length: int = len(chat_contents)

            if chat_contents_length == 6 or chat_contents_length == 5:
                structured_chat_data: dict = {
                    "MessageType": "GroupMessage",
                    "GroupName": chat_contents[0],
                    "Sender": chat_contents[2],
                    "Message": chat_contents[4],
                }
                data.append(structured_chat_data)

            if chat_contents_length == 4 or chat_contents_length == 3:
                is_group_event: bool = False
                event_by: str = " "
                event_info: str = " "

                search_item: str = chat_contents[2]
                pattern = re.compile(r'(\+\d{2}\s\d{5}\s\d{5})\s(\w+)')
                matches = pattern.finditer(search_item)

                for match in matches:
                    if match:
                        if match.group(2) == "joined" or match.group(2) == "left":
                            is_group_event: bool = True
                            event_by: str = match.group(1)
                            event_info: str = match.group(2)
                        if match.group(2) == "added" or match.group(2) == "removed":
                            is_group_event: bool = True
                            event_info: str = match.group(2)
                            event_message: list = chat_contents[2].split(" ")
                            event_by = f"{event_message[4]} {event_message[5]} {event_message[6]}"

                if is_group_event:
                    structured_chat_data: dict = {
                        "MessageType": "GroupEvent",
                        "GroupName": chat_contents[0],
                        "EventBy": event_by,
                        "EventInfo": event_info,
                    }
                    data.append(structured_chat_data)

                if not is_group_event:
                    structured_chat_data: dict = {
                        "MessageType": "DirectMessage",
                        "Sender": chat_contents[0],
                        "Message": chat_contents[2],
                    }
                    data.append(structured_chat_data)

    return data


def filter_data(structured_data: list, command_prefix: str) -> list:
    data: list = []

    for index, single_data in enumerate(structured_data):
        if single_data["MessageType"] == "GroupEvent":
            data.append(structured_data[index])

        if single_data["MessageType"] == "GroupMessage":
            if single_data["Message"].startswith(command_prefix):
                data.append(structured_data[index])

        if single_data["MessageType"] == "DirectMessage":
            if single_data["Message"].startswith(command_prefix):
                data.append(structured_data[index])

    return data
