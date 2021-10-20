from temp_mail import TempMail

# tm = TempMail(session_id='2e54fbff3e78b522296ed36e9dbfd01c')
tm = TempMail()
print(f'email: {tm.email}')

while True:
    try:
        print()
        print('1 - get new mail')
        print('2 - list messages')
        print('3 - show email')
        print('4 - show cookie')
        print('0 - close')
        user_input = int(input('select your option: ').strip())

        if user_input == 1:
            tm.change_email_address()
            print(f'novo email: {tm.email}')
        elif user_input == 2:
            tm.check_messages()
            print(tm.messages)
        elif user_input == 3:
            print(tm.email)
        elif user_input == 4:
            print(tm.get_session_id())
        elif(user_input == 0):
            break
    except ValueError:
        print("Generic Error")