db = {
    'user': 'myadmin'
    'password': 'root'
    'host': 'host.docker.internal',
    'port': 3306,
    'database': 'youcaloid'
}

db_url = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"