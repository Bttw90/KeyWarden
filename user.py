class User():
    def __init__(self, user_name, master_psw, master_psw_check):
        self.user_name = user_name
        self.master_psw = master_psw
        self.master_psw_check = master_psw_check

    def registration_check(self, user_name, master_psw, master_psw_check):
        try:
            if not user_name:
                raise ValueError('User Name field can not be empty.')
            if not master_psw:
                raise ValueError('Password field can not be empty.')
            if master_psw != master_psw_check:
                raise ValueError('Passwords do not match.')
            
        except ValueError as e:
            # Launch the exception to handle it in the frontend  (GUI)
            raise e
            