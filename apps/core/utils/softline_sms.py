import requests
import os
from dotenv import load_dotenv


load_dotenv()  # loads the configs from .env

SOFTLINE_SENDER_NAME = str(os.getenv('SOFTLINE_SENDER_NAME', ''))
SOFTLINE_USERNAME = str(os.getenv('SOFTLINE_USERNAME', ''))
SOFTLINE_APIKEY = str(os.getenv('SOFTLINE_APIKEY', ''))


class SoftlineSms:
    def __init__(self):
        self.__sender_name = SOFTLINE_SENDER_NAME
        self.__username = SOFTLINE_USERNAME
        self.__apikey = SOFTLINE_APIKEY
        self.__headers = {
          'Content-Type': 'application/json',
        }

    def send(self, phone, text):
        url = f"http://gw.soft-line.az/sendsms?user={self.__username}&password={self.__apikey}&gsm={phone}&from={self.__sender_name}&text={text}"
        print(50* "---")
        print(url)
        print(50 * "---")
        response = requests.request("GET", url, headers=self.__headers,)
        return response.text


