import os
import sqlite3
import bcrypt 
import uuid
import json
import time
from chatbot import Bot
from random import choice
from datetime import date
from flask import Flask, session, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)

# Secret Key is Randomly Generated
app.secret_key = uuid.uuid4().hex

@app.route('/', methods=['GET', 'POST'])
def index():
    # If user attempted to login
    if request.method == 'POST' and 'pword' in request.form:

        # Call the login function
        login_attempt = login(request.form['uname'], request.form['pword'])

        # If login fails, redirects to homepage
        if login_attempt == None:
            session['warn'] = 'Username or Password Invalid'
            return redirect(url_for('index'))

        # Stores the necessary user data
        session['userid'] = login_attempt[0]
        session['uname'] = login_attempt[1]
        session['access'] = login_attempt[2]

        # Redirects to chat page for users
        if session['access'] == 1:
            
            # Connects to the interviews database
            conn = sqlite3.connect('interviews.db')
            cur = conn.cursor()

            # Gets the user's team id and name
            results = cur.execute('SELECT team_id, team_name FROM user_teams JOIN teams USING (team_id) WHERE user_id = ?', (session['userid'],))
            results = results.fetchone()
            
            # Closes the database conncetion
            cur.close()
            conn.close()
            
            # Stores the user's team data
            session['team_name'] = results[0]
            session['team_id'] = results[1]

            # Stores the ongoing message log    
            session['message_log'] = []

            # Stores the bot object
            app.config['bot'] = chatbot_setup(session['uname'], request.form['gptkey'])

            # Stores the team name
            session['team_name'] = app.config['bot'].team_name

            return redirect(url_for('user_chat'))

        # Redirects to mangagement page for admins
        if session['access'] == 2:
            return redirect(url_for('manage'))
        
        # Redirects to super management page for super admin
        if session['access'] == 3:
            return redirect(url_for('index'))

    # Sets any warning messages
    if 'warn' in session:
        warn = session['warn']
        session.pop('warn')
    else:
        warn = None

    # Renders the page
    return render_template('login.j2', warn=warn)

@app.route('/chat', methods=['GET', 'POST'])
def user_chat():
    # Checks the user's access
    if not valid_access(1):
        return redirect(url_for('index'))

    # This if else statment is used to generate the next response message
    # If statement for when the user is currently chatting
    if 'chat' in request.form:
        session['message_log'] = app.config['bot'].chat(request.form['chat'])
    # If statement for when the user is finished chatting
    elif 'finish' in request.form:
        save_chat()
        return redirect(url_for('index'))
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

    # Redirects to team view page when button is clicked
    if 'view_teams' in request.form:
        return redirect(url_for('view_teams'))

    # Renders management homepage
    return render_template('manage.j2')

@app.route('/manage/create_team', methods=['GET', 'POST'])
def create_team():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'team_name' in request.form:
            # Connects to the database
            conn = sqlite3.connect('interviews.db')
            cur = conn.cursor()
            
            # Generates a team id
            team_id = gen_team_id()

            # Adds team to the database
            cur.execute('INSERT INTO teams VALUES (?, ?);', (team_id, request.form['team_name']))
            cur.execute('INSERT INTO manager_teams VALUES (?, ?);', (session['userid'], team_id))
            conn.commit()
            
            # Closes connection
            cur.close()
            conn.close()
            
        return redirect(url_for('manage'))
    return render_template('create_team.j2')

@app.route('/manage/view_teams', methods=['GET', 'POST'])
def view_teams():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('interviews.db')
    cur = conn.cursor()
    
    results = cur.execute('SELECT team_id, team_name FROM manager_teams JOIN teams USING (team_id) WHERE user_id = ?', (session['userid'],))
    
    results = results.fetchall()
    
    return render_template('view_teams.j2', teams=results)

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
    symbs = 'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789'
    
    # Generates string of 5 characters
    team_id = ''
    for _ in range(5):
        team_id += choice(symbs)
        
    # Returns string
    return team_id

def login(uname, pword):
    # Connects to the user database
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Gets user with username
    results = cur.execute('SELECT * FROM users WHERE username = ?', (uname,))
    results = results.fetchone()

    # Closes the database connection
    cur.close()
    conn.close()
    # If no user is found, it returns None
    if results == None:
        return None

    # Encodes entered password
    pword = pword.encode('utf-8')
    
    # Compares passwords, returns None if it is incorrect
    if not bcrypt.checkpw(pword, results[2]):
        return None
     
    # Returns user_id, username, access_level, gpt_key, team_id, and team_name
    return (results[0], results[1], results[3], results[4])

# --------Needs Updating----------

def chatbot_setup(username, gptkey):
    bot = Bot(gptkey)
    bot.team_members = [username]
    bot.temp_members = [username]
    bot.team_name = session['team_name']
    return bot

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
        
    print(js)
    # Saves the message log
    js['chats'][f'{date.today()}: {time.time()}'] = session['message_log']
        
    # Dumps it into json format
    j = json.dumps(js, indent=2)
        
    # Writes to the json file
    with open(os.path.join('chats', f'{session["team_id"]}.json'), 'w') as f:
            f.write(j)

def print_report():
    output = ''
    for m in session['message_log']:
        output += m['role']
        output += ':\n'
        output += m['content']
        output += '\n'
    print(output)

if __name__ == '__main__': 
    #app.run(host='0.0.0.0', port=12429)
    app.run(debug=True)