from Chatbot import Bot
import sqlite3

def create_DB():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    f = open('blueprint.sql','r').read()
    c.executescript(f)
    conn.commit()
    c.close()
    conn.close()
    pass

def add_dummy_user():
    pass

create_DB()