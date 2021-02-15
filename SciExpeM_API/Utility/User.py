class User:

    def __init__(self, username, user_id, token,
                 first_name=None, last_name=None, email=None, groups=None, permissions=None):
        self.username = username
        self.user_id = user_id
        self.token = token
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.groups = groups
        self.permissions = permissions
