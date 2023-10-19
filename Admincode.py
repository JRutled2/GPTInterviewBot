import sqlite3
import bcrypt 

def create_user_DB():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    f = open('schema/user_schema.sql','r').read()
    c.executescript(f)
    conn.commit()
    c.close()
    conn.close()
    pass

def add_dummy_user():
    password = 'test'
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f'''
        INSERT INTO users VALUES ("test", "{hash}", "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");
        ''')

def create_interview_DB():
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    f = open('schema/interviews_schema.sql','r').read()
    c.executescript(f)
    conn.commit()
    conn.close()
    pass


uin = input('Rebuild User Database? (y/n)\n>')
if uin == 'y':
    create_user_DB()
    uin = input('Add Dummy User? (y/n)\n>')
    if uin == 'y':
        add_dummy_user()

uin = input('Rebuild Interview Database? (y/n)\n>')
if uin == 'y':
    create_interview_DB()
