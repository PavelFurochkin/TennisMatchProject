from decouple import config


DB = {
    'driver_name': config("DB_DRIVER"),
    'username': config("DB_USER"),
    'database': config("DB_NAME"),
    'host': config("DB_HOST"),
    'port': config("DB_PORT"),
    'password': config("DB_PASS")

}

DB_URL = f'''{DB['driver_name']}://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}'''
