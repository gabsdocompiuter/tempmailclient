from os import replace
import requests
from bs4 import BeautifulSoup

class TempMail:
    __endpoint = 'https://10minutemail.org'
    __endpoint_new = 'https://10minutemail.org/new.html'
    __endpoint_renew = 'https://10minutemail.org/more.html'
    __endpoint_hundred_minutes = 'https://10minutemail.org/more100.html'

    def __init__(self, session_id=None):
        self.email = ''
        self.messages = []
        self.cookies = {}

        if session_id != None:
            self.cookies['PHPSESSID'] = session_id

        self.__set_email()

    def get_session_id(self) -> str:
        return self.cookies.get('PHPSESSID', None)

    def change_email_address(self) -> None:
        tmm = self.__get_site_parsed(self.__endpoint_new)

        self.email = tmm.find('input', 'mailtext', value=True)['value']
    
    def check_messages(self) -> None:
        tmm = self.__get_site_parsed(self.__endpoint)

        table = tmm.find('table', id='maillist')
        table_lines = table.find_all('tr', onclick=True)

        self.messages = []

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

    def __get_site_parsed(self, endpoint: str) -> BeautifulSoup:
        response = requests.get(endpoint, cookies=self.cookies)
        session_id = response.cookies.get_dict().get('PHPSESSID', None)
        
        if session_id != None:
            self.cookies['PHPSESSID'] = session_id

        return BeautifulSoup(response.content, 'html.parser')
    
    def __set_email(self) -> None:
        tmm = self.__get_site_parsed(self.__endpoint)

        self.email = tmm.find('input', 'mailtext', value=True)['value']