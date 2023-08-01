import PySimpleGUI as sg
from user import User
from db import Database
from psw_manager import *

db = Database('test')
db.connect()
db.create_users_table()

user = User()

def login_window():
    layout = [
        [sg.Text('Username:', size=(10, 1)), sg.Input(key='-USERNAME-')],
        [sg.Text('Password:', size=(10, 1)), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Button('Login'), sg.Button('Register')]
    ]

    window = sg.Window('Login', layout, finalize=True)

    login_successful = False

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Login':
            # Authentication and redirect logic
            try:
                user_name = values['-USERNAME-']
                master_psw = values['-PASSWORD-']

                user.set_name(user_name)
                user.set_psw(master_psw)
                user.login_check()

                hashed_psw = db.get_master_psw(user.name)

                if psw_check(master_psw, hashed_psw):
                    login_successful = True
                    sg.popup('Login completed with success.')
                else:
                    sg.popup_error('Wrong user name or password')

            except ValueError as e:
                sg.popup_error(str(e))

            if login_successful:
                window.close()
                main_window()

        elif event == 'Register':
            window.close()
            registration_window()


def registration_window():
    layout = [
        [sg.Text('Username:', size=(15, 1)), sg.Input(key='-USERNAME-')],
        [sg.Text('Password:', size=(15, 1)), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Text('Repeat Password:', size=(15, 1)), sg.Input(key='-PASSWORD_CHECK-', password_char='*')],
        [sg.Button('Register')]
    ]

    window = sg.Window('Registration', layout, finalize=True)

    registration_successful =  False

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Register':
            # Check registration fields
            try:
                user_name = values['-USERNAME-']
                master_psw = values['-PASSWORD-']
                master_psw_check = values['-PASSWORD_CHECK-']

                user.set_name(user_name)
                user.set_psw(master_psw)
                user.set_psw_check(master_psw_check)
                checks_passed = user.registration_fields_check()

            except ValueError as e:
                sg.popup_error(str(e))

        # After the registration is complete go to main_window
        if checks_passed:
            # Salting and hashing master_psw
            hashed_master_psw = hash_and_salt(master_psw)[0]
            salt = hash_and_salt(master_psw)[1]
            registration_successful = db.insert_user_table(user_name, hashed_master_psw, salt)
            # Check if data entered successfully
            if registration_successful:
                sg.popup('Registration completed with success.')
                # Create user personal passwords table
                db.create_user_psw_table(user.name)
                window.close()
                main_window()


def main_window():
    # TODO: Dropdown do not get new passwords in the same session
    data = db.get_apps_name(user.name)

    layout = [
        [sg.Text('Welcome to the Main Window!')],
        [sg.DropDown(data, key='-DROPDOWN-', readonly=True)],
        [sg.Button('Get Password')],
        [sg.Text('Selected Login Name:'), sg.Text('', size=(30, 1), key='-OUTPUT_NAME-')],
        [sg.Text('Selected Password:'), sg.Text('', size=(30, 1), key='-OUTPUT_PSW-')],
        [sg.Button('Insert Password')],
        [sg.Button('Logout')]
    ]

    window = sg.Window('Main Window', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Logout':
            db.disconnect()
            window.close()
            break
        elif event == 'Get Password':
            # TODO: Input validation
            selected_app = values['-DROPDOWN-']

            login_name = db.get_login_name(user.name, selected_app[0])
            window['-OUTPUT_NAME-'].update(login_name)

            # TODO: Show decrypted password for selected app
            salt = db.get_salt(user.name)
            key = get_fernet_key(user.master_psw, salt)

            psw_encrypted = db.get_psw(user.name, selected_app[0])
            psw = decrypt_psw(psw_encrypted, key)

            window['-OUTPUT_PSW-'].update(psw)


        elif event == 'Insert Password':
            psw_gen_window()


def psw_gen_window():
    layout = [
        [sg.Text('App Name:', size=(15, 1)), sg.Input(key='-APP_NAME-')],
        [sg.Text('Login Name:', size=(15, 1)), sg.Input(key='-LOGIN_NAME-')],
        [sg.Text('Password Length:', size=(15, 1)), sg.Input(key='-LENGTH-')],
        [sg.Button('Generate Password'), sg.Text("", size=(30, 1), key="-OUTPUT-")],
        [sg.Button('Save Password')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Password Generator', layout, finalize=True)

    psw = None

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break
        elif event == 'Generate Password':
            # TODO: Set max and min length, try except
            psw_len = values['-LENGTH-']
            # TODO: Check input validation
            psw = generate_random_password(int(psw_len))
            window["-OUTPUT-"].update(psw)
            # Testing:
            print('Password randomicaly generated: ', psw)
        elif event == 'Save Password':
            # TODO: Cipher with master_key and put created psw into db, try except
            app_name = values['-APP_NAME-']
            login_name = values['-LOGIN_NAME-']

            salt = db.get_salt(user.name)
            key = get_fernet_key(user.master_psw, salt)
            
            psw_encrypted = encrypt_psw(psw, key)
            
            db.insert_psw_table(user.name, login_name, app_name, psw_encrypted)
            
            sg.popup('Password saved with success.')


if __name__ == '__main__':
    login_window()