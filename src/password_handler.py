import bcrypt

class PasswordHandler:
    def __init__(self):
        self.salt = bcrypt.gensalt()

    def hash(self, password):
        return bcrypt.hashpw(password.encode(), self.salt)

    def verify(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)