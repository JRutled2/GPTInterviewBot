import sqlite3
import bcrypt 
import uuid

def add_managers():
    username = input('username: ')
    password = input('password: ')

    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)
    user_id = uuid.uuid4().hex

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES (?, ?, ?, 2, "Enter GPT Key Here");', (user_id, username, hash,))
    conn.commit()
    c.close()
    conn.close()
    print('Added Manager', username)

def print_managers():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    cur =  c.execute('SELECT user_id, username FROM users WHERE access=2')
    for row in cur.fetchall():
        print(f'[{row[0]}] {row[1]}')
    c.close()
    conn.close()

def change_access():
    uid = input('user id: ')
    access = int(input('access level: '))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('')

def rebuild_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    f = open('database_schema.sql','r').read()
    c.executescript(f)
    conn.commit()
    c.close()
    conn.close()


uin = 'help'
while uin != 'q' and uin != 'quit':
    if uin == 'help':
        print('[1] add_managers\n'+
              '[2] print_managers\n'+
              '[3] change_access\n' +
              '[0] more_options')
    if uin == '0':
        print('[x] rebuild_database')

    elif uin == '1' or uin == 'add_managers':
        add_managers()

    elif uin == '2' or uin == 'print_managers':
        print_managers()

    elif uin == '3' or uin == 'change_access':
        change_access()

    elif uin == 'x' or uin == 'rebuild_database':
        in2 = input('Are You Sure? [y/n]\n> ').lower()
        if in2 == 'y':
            rebuild_database()
            print('Database Rebuilt')
    uin = input('> ').lower()