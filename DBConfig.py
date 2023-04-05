import pyodbc
from decouple import config


class DBConfig:

    server = 'b00585717server.database.windows.net'
    database = 'b00585717db'
    username = config('UN', default='')
    password = config('PW', default='')
    driver = 'ODBC Driver 18 for SQL Server'

    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={' + self.driver +
            '};SERVER=tcp:' + self.server +
            ';PORT=1433;DATABASE=' + self.database +
            ';UID=' + self.username +
            ';PWD=' + self.password
        )

    def get_cursor(self):
        return self.connection.cursor()

    def get_conn_string(self):
        return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver={self.driver}"
