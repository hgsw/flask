from werkzeug.security import generate_password_hash


class User:
    def __init__(self):
        self._password = "123456"  # 初始密码
        self.user_name = "Tom"  # 初始用户名

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = generate_password_hash(new_password)


user = User()
print(user.password)
user.password = "909090"
print(user.password)
