from sqlite3 import connect, Cursor, Connection
from hashlib import sha256
from flask import Flask
from model import Field, Model
from base_api import BaseApi

app = Flask(__name__)


class Api(BaseApi):
    db: Connection
    cur: Cursor

    def __init__(self, app: Flask) -> None:
        super().__init__(app)

        self.db = connect("database.db", check_same_thread=False)
        self.cur = self.db.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                username TEXT,
                password TEXT
            );
        """)

    def apis_login(self, username: str, password: str) -> str:
        print(username, password)

        result = self.cur.execute(
            "SELECT password FROM sessions WHERE username=?", 
            (username, )
        ).fetchone()

        if result is None:
            raise ValueError("Неправильное имя")
        
        if password != result[0]:
            raise ValueError("Неправильньій пароль")
        
        token = sha256(username.encode()).hexdigest()
        self.tokens[token] = username

        return {
            "token": token
        }
    
    def apis_register(self, username: str, password: str) -> None:
        result = self.cur.execute(
            "SELECT password FROM sessions WHERE username=?",
            (username, )
        ).fetchone()

        if result is not None:
            raise ValueError("Имя уже зарегистрировано")
        
        self.cur.execute("INSERT INTO sessions VALUES(?, ?)", (username, password))
        self.db.commit()


api = Api(app)
app.run("localhost", 8080)
