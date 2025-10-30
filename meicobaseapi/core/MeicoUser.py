class Meico_User:
    def __init__(self, username, email, display_name):
        self.username = username
        self.email = email
        self.display_name = display_name

    def __str__(self):
        return self.username
