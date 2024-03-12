import os
import sqlite3
import bcrypt 
import uuid
import json
import time
from chatbot import Bot
from random import choice
from datetime import date, datetime
from flask import Flask, session, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)

# Secret Key is Randomly Generated
app.secret_key = uuid.uuid4().hex

@app.route('/', methods=['GET', 'POST'])
def index():

    # If user is not logged in
    if 'access' not in session:
        # Renders the page
        return render_template('login.j2')
        
    # Redirects to chat page for users
    if session['access'] == 1:
        return redirect(url_for('user_chat'))

    # Redirects to mangagement page for managers
    if session['access'] == 2:
        return redirect(url_for('manage'))
        
    # Redirects to super management page for admins
    if session['access'] == 3:
        return redirect(url_for('admin'))

@app.route('/chat', methods=['GET', 'POST'])
def user_chat():
    # Checks the user's access
    if not valid_access(1):
        return redirect(url_for('index'))

    # This if else statment is used to generate the next response message
    # If statement for when the user is currently chatting
    if 'chat' in request.form:
        try:
            session['message_log'] = app.config['bot'].chat(request.form['chat'])
        except:
            session['message_log'] += [{'role': 'assistant', 'content': 'Error, please contact an Administrator.'}]

    # If statement for when the user is finished chatting
    elif 'finish' in request.form:
        save_chat()
        return redirect(url_for('logout'))
    # Else statement for initial chat message, necessary for when the message log is empty
    else:
        session['message_log'] = app.config['bot'].chat('')

    # Renders the chat page
    return render_template('chat.j2', message_log=session['message_log'])

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    # Redirects to team creation page when button is clicked
    if 'create_team' in request.form:
        return redirect(url_for('create_team'))

    # Redirects to team creation page when button is clicked
    if 'create_user' in request.form:
        return redirect(url_for('create_user'))

    # Renders management homepage
    return render_template('manage.j2')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Checks the user's access
    if not valid_access(3):
        return redirect(url_for('index'))

    # Redirects to team creation page when button is clicked
    if 'create_team' in request.form:
        return redirect(url_for('create_team'))

    # Redirects to team view page when button is clicked
    if 'view_teams' in request.form:
        return redirect(url_for('view_teams'))

    # Renders management homepage
    return render_template('admin.j2')

@app.route('/manage/view_teams', methods=['GET', 'POST'])
def view_teams():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))
    
    # Connects to the database
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    
    # Grabs all the teams associated with the manager
    results = cur.execute('SELECT team_id, team_name FROM manager_teams JOIN teams USING (team_id) WHERE user_id = ?', (session['userid'],))
    results = results.fetchall()
    
    # Renders the view teams page
    return render_template('view_teams.j2', teams=results)

@app.route('/manage/create_team', methods=['GET', 'POST'])
def create_team():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'team_name' in request.form:
            log(session['uname'], f'created team: {request.form["team_name"]}')

            # Connects to the database
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            
            # Generates a team id
            team_id = gen_team_id()

            # Ensures the team id is unique
            valid = cur.execute('SELECT * FROM teams WHERE team_id = ?', (team_id,)).fetchone()
            while valid != None:
                team_id = gen_team_id()
                valid = cur.execute('SELECT * FROM teams WHERE team_id = ?', (team_id,)).fetchone()

            # Adds team to the database
            cur.execute('INSERT INTO teams VALUES (?, ?);', (team_id, request.form['team_name']))
            cur.execute('INSERT INTO manager_teams VALUES (?, ?);', (session['userid'], team_id))
            conn.commit()
            
            # Closes connection
            cur.close()
            conn.close()
            
        return redirect(url_for('manage'))
    return render_template('create_team.j2')

@app.route('/manage/view_users', methods=['GET', 'POST'])
def view_users():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    # Connects to the database
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Grabs all the users associated with the manager
    results = cur.execute('SELECT users.username, user_teams.team_id FROM (manager_teams JOIN user_teams USING (team_id)) JOIN users ON user_teams.user_id = users.user_id WHERE manager_teams.user_id = ?', 
                          (session['userid']))
    results = results.fetchall()
    return results

@app.route('/manage/create_user', methods=['GET', 'POST'])
def create_user():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'username' in request.form:
            log(session['uname'], f'created user: {request.form["username"]}')

            # Connects to the user database
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()

            # Generates a unique user id
            user_id = uuid.uuid4().hex
            
            # Hashes the password
            bytes = request.form['password'].encode('utf-8') 
            salt = bcrypt.gensalt() 
            hash = bcrypt.hashpw(bytes, salt)

            # Adds the user to the login database
            cur.execute('INSERT INTO users (user_id, username, password, access) VALUES (?,?,?,?)', (user_id, request.form['username'], hash, 1))
            cur.execute('INSERT INTO user_teams VALUES (?,?)', (user_id, request.form['team_id']))

            # Commits the insert
            conn.commit()
            cur.close()
            conn.close()

    return render_template('create_user.j2')

@app.route('/admin/create_manager', methods=['GET', 'POST'])
def create_manager():
    # Checks the user's access
    if not valid_access(3):
        return redirect(url_for('index'))

@app.route('/manage/gpt_key', methods=['GET', 'POST'])
def gpt_key():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        log(session['uname'], 'gpt key change')
        new_key = request.form['key']
        
        # Connects to user database
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        
        # Updates the GPT Key
        cur.execute('UPDATE users SET gpt_key=? WHERE user_id = ?', (new_key, session['userid']))
        
        # Commits and closes the database connection
        con.commit()
        cur.close()
        con.close()

    # Gets the current GPT key
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    
    results = cur.execute('SELECT gpt_key FROM users WHERE user_id = ?', (session['userid'], ))
    results = results.fetchone()[0]

    cur.close()
    conn.close()

    # Renders the webpage
    return render_template('gpt_key.j2', old_key=results)

@app.route('/past_chat_select/<team_id>', methods=['GET', 'POST'])
def past_chat_select(team_id):
    # Checks the user's access
    if not valid_access(1):
        return redirect(url_for('index'))

    # User view past chats
    if session['access'] == 1:
        return redirect(url_for('index'))

    # Manager view past chats
    if session['access'] == 2:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        chats = cur.execute('SELECT chat_id FROM weekly_chats WHERE team_id=?', (team_id,))
        chats = chats.fetchall()

        cur.close()
        con.close()

        return render_template('past_chats_select.j2', chats=chats)

    # Admin view past chats
    if session['access'] == 3:
        return redirect(url_for('index'))

@app.route('/past_chat/<chat_id>')
def past_chat(chat_id):
    if not valid_access(1):
        return redirect(url_for('index'))

    with open(os.path.join('chats', '23.json'), 'r') as f:
        js = json.load(f)

    chat = js['chats'][chat_id]
    return render_template('past_chat.j2', message_log=chat)

@app.route('/login', methods=['POST'])
def login():
    # If Login information is not in the request, redirect back to login page
    if 'uname' not in request.form or 'pword' not in request.form:
        return redirect(url_for('index'))

    # Connect to the user database
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Gets user with username
    results = cur.execute('SELECT * FROM users WHERE LOWER(username) = ?', (request.form['uname'].lower(),))
    results = results.fetchone()

    # Closes the database connection
    cur.close()
    conn.close()

    # If no user is found, it redirects back to the login page
    if results == None:
        log(request.form["uname"], 'incorrect username')
        return redirect(url_for('index'))

    session['uname'] = results[1]

    # Encodes entered password
    pword = request.form['pword'].encode('utf-8')
    
    # Compares passwords, redirects back to login page if it is incorrect
    if not bcrypt.checkpw(pword, results[2]):
        log(session['uname'], 'incorrect password')
        return redirect(url_for('index'))

    # Sets the session variables
    session['userid'] = results[0]
    session['access'] = results[3]

    log(session['uname'], 'logged in')

    # If the user is a student
    if session['access'] == 1:
        # Connects to the user database
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        # Gets the user's team id and name
        results = cur.execute('SELECT team_name, team_id FROM user_teams JOIN teams USING (team_id) WHERE user_id = ?', (session['userid'],))
        results = results.fetchone()

        # Gets the gpt key associated with the manager
        gpt_key = cur.execute('SELECT gpt_key FROM manager_teams JOIN users USING (user_id) WHERE team_id = ?', (results[1], ))
        gpt_key = gpt_key.fetchone()[0]
        # Closes the database connection
        cur.close()
        conn.close()

        # Sets the student exclusive session variables
        session['team_name'] = results[0]
        session['team_id'] = results[1]
        session['message_log'] = []

        # Stores the gpt bot in the app.config
        app.config['bot'] = Bot(gpt_key)

        # Sets the gpt bot variables
        app.config['bot'].team_members = [session['uname']]
        app.config['bot'].temp_members = [session['uname']]
        app.config['bot'].team_name = session['team_name']

    return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    log(session['uname'], 'logged out')
    # Clears the session variables
    session.clear()

    # Clears the gpt bot if applicable
    if 'bot' in app.config:
        app.config.pop('bot')
    
    # Redirects to login page
    return redirect(url_for('index'))

def valid_access(access_level):
    # Ensures the user is logged in
    if 'uname' not in session or 'access' not in session:
        return False

    # Ensures the user has proper access 
    if session['access'] < access_level:
        return False

    return True

def gen_team_id():
    # Character options
    symbs = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    
    # Generates string of 5 characters
    team_id = ''
    for _ in range(5):
        team_id += choice(symbs)
        
    # Returns string
    return team_id

def save_chat():        
    # Creates chat folder if it doesn't exist  
    if not os.path.exists(os.path.join('chats', f'{session["team_id"]}.json')):
        # Creates initial json dictionary
        js = {'team_id': session['team_id'],
              'team_name': session['team_name'],
              'chats': {}}
        
        # Dumps it into json format
        j = json.dumps(js, indent=2)
            
        # Saves initial file
        with open(os.path.join('chats', f'{session["team_id"]}.json'), 'w') as f:
            f.write(j)
     
    # Opens json file
    with open(os.path.join('chats', f'{session["team_id"]}.json'), 'r') as f:
        # Loads data
        js = json.load(f)
        
    # Saves the message log
    chat_id = f'{date.today()}: {time.time()}'
    js['chats'][chat_id] = session['message_log']
        
    # Dumps it into json format
    j = json.dumps(js, indent=2)
        
    # Writes to the json file
    with open(os.path.join('chats', f'{session["team_id"]}.json'), 'w') as f:
            f.write(j)

    # Saves the chat to the database
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('INSERT INTO weekly_chats VALUES (?, ?)', (chat_id, session['team_id']))
    
    conn.commit()
    cur.close()
    conn.close()

def log(uname, text):
    with open(os.path.join('system_logs', f'{date.today()}.txt'), 'a') as f:
            f.write(f'{datetime.now()} [{uname}] {text}\n')

if __name__ == '__main__': 
    #app.run(host='0.0.0.0', port=12429)
    app.run(debug=True)