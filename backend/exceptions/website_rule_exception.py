class WebsiteRuleAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Website rule already exists")


class WebsiteRuleNotFoundException(Exception):
    def __init__(self):
        super().__init__("Website rule not found")


class UserWebsiteRuleAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("User already has a rule for this Website")


class UserNotFoundForWebsiteRuleException(Exception):
    def __init__(self):
        super().__init__("User not found")

class UserWebsiteRuleNotFoundException(Exception):
    def __init__(self):
        super().__init__("User website rule not found")