from os import replace
import requests
from bs4 import BeautifulSoup

class TempMail:
    endpoint = 'https://10minutemail.org'
    new = '/new.html'
    renew = '/more.html'

    def __init__(self):
        self.email = ''
        self.messages = []

    def get_new_email(self):
        ui = self.__get_site_parsed(self.endpoint)

        self.email = ui.find('input', 'mailtext', value=True)['value']
    
    def check_messages(self):
        ui = self.__get_site_parsed(self.endpoint)

        table = ui.find('table', id='maillist')
        table_lines = table.find_all('tr', onclick=True)

        for line in table_lines:
            columns = line.find_all('td')
            if len(columns) <= 0: continue

            location = line['onclick']
            location = location.replace('location=', '')
            location = location.replace("'", "")
            
            mail = {
                'sender': columns[0].text,
                'subject': columns[1].text,
                'timeAgo': columns[2].text,
                'endpoint': location
            }

            self.messages.append(mail)

    def __get_site_parsed(self, endpoint: str):
        response = requests.get(endpoint)
        content = response.content
        return BeautifulSoup(content, 'html.parser')