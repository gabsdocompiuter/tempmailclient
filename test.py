import os
from temp_mail import TempMail

clear = lambda: os.system('cls')

tm = TempMail(session_id='127f5be450d212f6b7a9d293593e8ab4')
# tm = TempMail()

while True:
    try:
        print()
        print(f'email: {tm.email}')
        print('1 - get new mail')
        print('2 - list messages')
        print('3 - read message')
        print('4 - show session id')
        print('8 - get 10 more minutes')
        print('9 - get 100 more minutes')
        print('0 - close')
        user_input = int(input('select your option: ').strip())

        clear()

        # get new mail
        if user_input == 1:
            tm.change_email_address()
            print(f'novo email: {tm.email}')

        # list messages
        elif user_input == 2:
            tm.check_messages()
            print(tm.messages)

        # read message
        elif user_input == 3:
            mail_id = input('message id: ').strip()
            print(tm.read_mail(mail_id))

        # show session id
        elif user_input == 4:
            print(tm.get_session_id())

        # get 10 more minutes
        elif user_input == 8:
            tm.get_10_more_minutes()

        # get 100 more minutes
        elif user_input == 9:
            tm.get_100_more_minutes()

        elif(user_input == 0):
            break
    except ValueError:
        print("Generic Error")