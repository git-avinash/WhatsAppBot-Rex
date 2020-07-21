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


from botrex import BotRex, RexActions
import os

BINARY_LOCATION = os.environ.get("GOOGLE_CHROME_BIN")
WEBDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")

EMAIL_ADDRESS = os.environ.get("MY_EMAIL")
EMAIL_PASS = os.environ.get("MY_PASS")
MAIL_TO = "mail.avinashsah@gmail.com"

LISTEN_TO = ["TestHub", "+91 86008 12345"]
PREFIX = "!"


def my_bot(self, task):
    if task["MessageType"] == "GroupMessage":
        command: str = task["Message"].strip(PREFIX)

        if command == "ping":
            RexActions.send_message(
                self, task["GroupName"], "PONG! :lion face\ue007")

        if command == "close":
            self.listen = False

    if task["MessageType"] == "GroupEvent":
        if task["EventInfo"] == "joined" or task["EventInfo"] == "added":
            RexActions.send_message(
                self, task["GroupName"], f"@{task['EventBy']}\ue007 Welcome to the club!")

    if task["MessageType"] == "DirectMessage":
        if task["Sender"] != "TestHub":
            command: str = task["Message"].strip(PREFIX)

            if command == "ping":
                RexActions.send_message(
                    self, task["Sender"], "PONG! :jack-o-lantern\ue007")


bot = BotRex(WEBDRIVER_PATH, BINARY_LOCATION,
             my_bot, run_headless=True)
bot.login(EMAIL_ADDRESS, EMAIL_PASS, MAIL_TO, debug_mode=False)
bot.run(LISTEN_TO, PREFIX)
