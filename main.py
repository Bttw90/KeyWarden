import PySimpleGUI as sg
from user import User
from db import Database
from psw_manager import *

# Create Database object and connect to it
db = Database('test')
db.connect()
# Create users table when the program is first started 
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
    # List of passwords saved by the user
    data = db.get_apps_name(user.name)

    layout_tab1 = [
        [sg.DropDown(data, key='-DROPDOWN-', readonly=True)],
        [sg.Button('Get Password')],
        [sg.Column([
            [sg.Text('Selected Login Name:')],
            [sg.Text('Selected Password:')],
        ]),
        sg.Column([
        [sg.InputText('', size=(30, 1), key='-OUTPUT_NAME-', disabled=True)],
        [sg.InputText('', size=(30, 1), key='-OUTPUT_PSW-', disabled=True)],
        ])]
    ]

    layout_tab2 = [
        [sg.Text('App Name:', size=(15, 1)), sg.Input(key='-APP_NAME-')],
        [sg.Text('Login Name:', size=(15, 1)), sg.Input(key='-LOGIN_NAME-')],
        [sg.Text('Password Length:', size=(15, 1)), sg.Input(key='-LENGTH-')],
        [sg.Button('Generate Password'), sg.Text("", size=(30, 1), key="-OUTPUT-")],
        [sg.Button('Save Password')],
    ]

    tab_group_layout = [
        [sg.Tab('Withdraw Password', layout_tab1, key='-TAB1-')],
        [sg.Tab('Insert Password', layout_tab2, key='-TAB2-')]
    ]

    layout = [
        [sg.TabGroup(tab_group_layout)],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Main Window', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            db.disconnect()
            window.close()
            break

        elif event == 'Get Password':
            selected_app = values['-DROPDOWN-']

            login_name = db.get_login_name(user.name, selected_app[0])
            window['-OUTPUT_NAME-'].update(login_name)

            # Show decrypted password for selected app
            salt = db.get_salt(user.name)
            key = get_fernet_key(user.master_psw, salt)

            psw_encrypted = db.get_psw(user.name, selected_app[0])
            psw = decrypt_psw(psw_encrypted, key)

            window['-OUTPUT_PSW-'].update(psw)

        elif event == 'Generate Password':
            # TODO: Set max and min length
            psw_len = values['-LENGTH-']
            try:
                psw_len = int(psw_len)
                if isinstance(psw_len, int):
                    psw = generate_random_password(psw_len)
                    window["-OUTPUT-"].update(psw)
            except ValueError:
                sg.popup_error('Password lenght field must be a number.')

        elif event == 'Save Password':
            # TODO: Cipher with master_key and put created psw into db, try except
            app_name = values['-APP_NAME-']
            login_name = values['-LOGIN_NAME-']

            try:
                salt = db.get_salt(user.name)
                key = get_fernet_key(user.master_psw, salt)

                if app_name == '' or login_name == '':
                    raise ValueError
                
                psw_encrypted = encrypt_psw(psw, key)
                
                db.insert_psw_table(user.name, login_name, app_name, psw_encrypted)

                window.Element('-DROPDOWN-').Update(values = db.get_apps_name(user.name))
                
                sg.popup('Password saved with success.')

            except ValueError:
                sg.popup_error('Fields must not be empty.')


if __name__ == '__main__':
    login_window()