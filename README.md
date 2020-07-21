# Whats App Bot: Rex
A WhatsApp API client that connects through the WhatsApp Web browser app

It uses Selenium WebDriver to run a real instance of Whatsapp Web to avoid getting blocked.

**NOTE:** I can't guarantee you will not be blocked by using this method, although it has worked for me. WhatsApp does not allow bots or unofficial clients on their platform, so this shouldn't be considered totally safe.

## Installation
* [Download ChromeDriver](https://chromedriver.chromium.org/downloads)
* Download this module

## Examples
**Example 1: Setting up Rex to respond to group messge !ping**
```py
from botrex import BotRex, RexActions
import os

BINARY_LOCATION = os.environ.get("GOOGLE_CHROME_BIN")
WEBDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")

EMAIL_ADDRESS = os.environ.get("MY_EMAIL")
EMAIL_PASS = os.environ.get("MY_PASS")
MAIL_TO = "mail.avinashsah@gmail.com"

LISTEN_TO = ["TestHub", "+91 86008 18691"]
PREFIX = "!"

def my_bot(self, task):
    if task["MessageType"] == "GroupMessage":
        command: str = task["Message"].strip(PREFIX)

        if command == "ping":
            RexActions.send_message(
                self, task["GroupName"], "PONG!")

bot = BotRex(WEBDRIVER_PATH, BINARY_LOCATION,
             my_bot, run_headless=True)
bot.login(EMAIL_ADDRESS, EMAIL_PASS, MAIL_TO, debug_mode=False)
bot.run(LISTEN_TO, PREFIX)
```
**Example 2: Messaging on Group Events**
```py
if task["MessageType"] == "GroupEvent":
        if task["EventInfo"] == "joined" or task["EventInfo"] == "added":
            RexActions.send_message(
                self, task["GroupName"], f"@{task['EventBy']}\ue007 Welcome to the club!")
```
**Example 3: Messaging on Direct Message**
```py
if task["MessageType"] == "DirectMessage":
        if task["Sender"] != "TestHub":
            command: str = task["Message"].strip(PREFIX)

            if command == "ping":
                RexActions.send_message(
                    self, task["Sender"], "PONG! :jack-o-lantern\ue007")
```
## Task Objects
**Group Message Object**
```py
{
    "MessageType": "GroupMessage",
    "GroupName": "GroupName",
    "Sender": "Sender Name or Contact number",
    "Message": "Message sent by the sender",
}
```
**Group Event Object**
```py
{
    "MessageType": "GroupEvent",
    "GroupName": "GroupName",
    "EventBy": "Name or Contact number of person who joinned, left, was added or kicked",
    "EventInfo": "joined/left/added/removed",
}
```
**Direct Message Object**
```py
{
    "MessageType": "DirectMessage",
    "Sender":" Sender Name or Contact number",
    "Message": "Message sent by the sender",
}
```
## Debugging
To see Chrome Browser:
**run_headless=False**

To not mail QR Code:
**debug_mode=True**

## Deploy on Heroku
[This worked for me](https://www.youtube.com/watch?v=Ven-pqwk3ec)

## Contact Me
[Instagram](https://www.instagram.com/avinashsah_/)

## Disclaimer
This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with WhatsApp or any of its subsidiaries or its affiliates. The official WhatsApp website can be found at https://whatsapp.com. "WhatsApp" as well as related names, marks, emblems and images are registered trademarks of their respective owners.

## License
Copyright 2020 Avinash S Sah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
