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
    c.execute('INSERT INTO users VALUES ("Test Super", ?, 3, "TODO NOT WORKING");', (hash,))
    c.execute('INSERT INTO users VALUES ("Test Admin", ?, 2, "TODO NOT WORKING");', (hash,))
    c.execute('INSERT INTO users VALUES ("Test User 1", ?, 1, "TODO NOT WORKING");', (hash,))
    c.execute('INSERT INTO users VALUES ("Test User 2", ?, 1, "TODO NOT WORKING");', (hash,))
    c.execute('INSERT INTO users VALUES ("Test User 3", ?, 1, "TODO NOT WORKING");', (hash,))
    c.execute('INSERT INTO users VALUES ("Test User 4", ?, 1, "TODO NOT WORKING");', (hash,))
    conn.commit()
    c.close()
    conn.close()

def create_interview_DB():
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    f = open('schema/interviews_schema.sql','r').read()
    c.executescript(f)
    conn.commit()
    c.close()
    conn.close()
    pass

def add_dummy_interview_teams():
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    c.executescript(f'''
        INSERT INTO user_teams VALUES ("Test Admin", "Management Team");
        INSERT INTO user_teams VALUES ("Test User 1", "Test Team 1");
        INSERT INTO user_teams VALUES ("Test User 2", "Test Team 2");
        INSERT INTO user_teams VALUES ("Test User 3", "Test Team 3");
        INSERT INTO user_teams VALUES ("Test User 4", "Test Team 4");
        ''')
    conn.commit()
    c.close()
    conn.close()

def print_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    cur =  c.execute('SELECT * FROM users')
    for row in cur.fetchall():
        print(row)
    c.close()
    conn.close()

uin = input('Rebuild User Database? (y/n)\n>')
if uin == 'y':
    create_user_DB()
    uin = input('Add Dummy User? (y/n)\n>')
    if uin == 'y':
        add_dummy_user()

uin = input('Rebuild Interview Database? (y/n)\n>')
if uin == 'y':
    create_interview_DB()
    uin = input('Add Dummy teams? (y/n)\n>')
    if uin == 'y':
        add_dummy_interview_teams()

uin = input('Print Users? (y/n)\n>')
if uin == 'y':
    print_users()