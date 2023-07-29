import PySimpleGUI as sg
from user import User
from db import Database
from psw_manager import hash_and_salt, psw_check

db = Database('test')
db.connect()
db.create_users_table()

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
            # TODO: authentication and redirect logic
            try:
                user_name = values['-USERNAME-']
                master_psw = values['-PASSWORD-']

                user_manager = User(user_name, master_psw)
                user_manager.login_check()

                hashed_psw = db.get_master_psw(user_name)

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

                user_manager = User(user_name, master_psw, master_psw_check)
                user_manager.registration_check()

                registration_successful = True

                sg.popup('Registration completed with success.')

            except ValueError as e:
                sg.popup_error(str(e))

        # After the registration is complete go to main_window
        if registration_successful:
            # Salting and hashing master_psw
            hashed_master_psw = hash_and_salt(master_psw)
            db.insert_user_table(user_name, hashed_master_psw)

            window.close()
            main_window()


def main_window():
    layout = [
        [sg.Text('Welcome to the Main Window!')],
        [sg.Button('Logout')]
    ]

    window = sg.Window('Main Window', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Logout':
            window.close()
            break

if __name__ == '__main__':
    login_window()