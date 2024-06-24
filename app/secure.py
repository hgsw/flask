# 安全类别的配置信息文件
# 数据库密码、API token等信息


class BaseConfig:
    DIALECT = "mysql"
    DRIVER = "pymysql"
    HOST = "localhost"
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "123456"
    DATABASE = "fisher"

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Token:
    KEY = "c00fxxx"
    # 设置一个密钥以启用session，随机初始化字符串
    SECRET_KEY = "hfiiuafwfhehfihwjsdcijhfcsjihcuiwe12742664284686246842"


class MailConfig:
    # 配置Flask-Mail
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465  # 使用SSL加密端口
    MAIL_USE_SSL = True  # 启用SSL加密
    MAIL_USERNAME = "hgsw93@163.com"  # 你的163邮箱用户名
    MAIL_PASSWORD = "GQUYQDLAUDEJTWOG"  # 你的SMTP授权码，而非邮箱登录密码
