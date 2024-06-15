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
