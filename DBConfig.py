import pyodbc
from decouple import config


class DBConfig:
    def __init__(self):
        server = 'b00585717server.database.windows.net'
        database = 'b00585717db'
        gov_id = config('UN', default='')
        password = config('PW', default='')
        driver = '{ODBC Driver 18 for SQL Server}'

        self.connection = pyodbc.connect(
            'DRIVER=' + driver +
            ';SERVER=tcp:' + server +
            ';PORT=1433;DATABASE=' + database +
            ';UID=' + gov_id +
            ';PWD=' + password
        )

    def get_cursor(self):
        return self.connection.cursor()
