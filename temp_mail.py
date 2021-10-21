import requests
from bs4 import BeautifulSoup

class TempMail:
    __endpoint = 'https://10minutemail.org'
    __endpoint_message = 'https://10minutemail.org/readmail.html?mid='
    __endpoint_new = 'https://10minutemail.org/new.html'
    __endpoint_more_10 = 'https://10minutemail.org/more.html'
    __endpoint_more_100 = 'https://10minutemail.org/more100.html'

    def __init__(self, session_id=None):
        self.email = ''
        self.messages = []
        self.cookies = {}

        if session_id != None:
            self.cookies['PHPSESSID'] = session_id

        self.__set_email_address()
        self.check_messages()

    def get_session_id(self) -> str:
        return self.cookies.get('PHPSESSID', None)

    def change_email_address(self) -> None:
        self.__set_email_address(get_new=True)

    def get_10_more_minutes(self) -> None:
        tmm = self.__get_site_parsed(self.__endpoint_more_10)
    
    def get_100_more_minutes(self) -> None:
        tmm = self.__get_site_parsed(self.__endpoint_more_100)
    
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
            id = location.replace('readmail.html?mid=', '')

            if id == 'welcome': continue

            sender = columns[0]
            sender_address = self.__decrypt_cf_email(sender)
            sender_name = sender.text.split('<')[0]

            mail = {
                'id': id,
                'sender_name': sender_name,
                'sender_address': sender_address,
                'subject': columns[1].text,
                'timeAgo': columns[2].text,
            }

            self.messages.append(mail)

    def read_message(self, id: str) -> str:
        endpoint = self.__endpoint_message + id
        tmm = self.__get_site_parsed(endpoint)

        mail_html = tmm.find('div', id='tab3')
        mail = mail_html.find('p', 'mailinhtml')

        return self.__sanitize_message(mail)
    
    def __get_site_parsed(self, endpoint: str) -> BeautifulSoup:
        response = requests.get(endpoint, cookies=self.cookies)
        session_id = response.cookies.get_dict().get('PHPSESSID', None)
        
        if session_id != None:
            self.cookies['PHPSESSID'] = session_id

        return BeautifulSoup(response.content, 'html.parser')
    
    def __set_email_address(self, get_new=False) -> None:
        endpoint = self.__endpoint_new if get_new else self.__endpoint

        tmm = self.__get_site_parsed(endpoint)

        self.email = tmm.find('input', 'mailtext', value=True)['value']

    def __decrypt_cf_email(self, soup: BeautifulSoup):
        mail_tag = soup.find(['a', 'span'], '__cf_email__')
        cfemail = mail_tag['data-cfemail']
        return self.__decode(cfemail)
    
    def __decode(self, cfemail):
        enc = bytes.fromhex(cfemail)
        return bytes([c ^ enc[0] for c in enc[1:]]).decode('utf8')

    def __sanitize_message(self, mail: BeautifulSoup) -> str:
        for br in mail.find_all("br"):
            br.replace_with("\n")
        
        sanitized_mail = ''

        for mail_content in mail.contents:
            if mail_content.text.strip() == '[email protected]':
                sanitized_mail += self.__decrypt_cf_email(mail_content)
            else:
                sanitized_mail += mail_content

        return sanitized_mail