class UsernameAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Username already Exists")
        
class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid Username or Password")
        
class UserNotApprovedException(Exception):
    def __init__(self):
        super().__init__("User account is not approved")