class User():
    def __init__(self):
        self.name = ''
        self.master_psw = ''
        self.master_psw_check = ''

    def set_name(self, name):
        self.name = name

    def set_psw(self, master_psw):
        self.master_psw = master_psw

    def set_psw_check(self, master_psw_check):
        self.master_psw_check = master_psw_check

    def registration_fields_check(self):
        try:
            if not self.name:
                raise ValueError('User Name field can not be empty.')
            if not self.master_psw:
                raise ValueError('Password field can not be empty.')
            if self.master_psw != self.master_psw_check:
                raise ValueError('Passwords do not match.')
            
            checks_passed = True
            
        except ValueError as e:
            # Launch the exception to handle it in the frontend  (GUI)
            checks_passed =  False
            raise e
        
        return checks_passed
        
    def login_check(self):
        try:
            if not self.name:
                raise ValueError('User Name field can not be empty.')
            if not self.master_psw:
                raise ValueError('Password field can not be empty.')
            
        except ValueError as e:
            raise e
        