class UsernameAlreadyExistsException(Exception):
    def __init__(self, *args):
        super().__init__("Username already Exists")