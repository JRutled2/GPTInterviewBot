import sqlite3
import bcrypt 
import uuid
from chatbot import Bot
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

        # Saves the necessary user information
        session['uname'] = login_attempt[0]
        session['access'] = login_attempt[1]

        # Redirects to chat page for users
        if session['access'] == 1:
            # Saves the ongoing message log
            session['message_log'] = []

            # Saves the bot object
            app.config['bot'] = chatbot_setup(login_attempt[0], request.form['gptkey'])

            # Saves the team name
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
        print_report()
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

    # Renders management homepage
    return render_template('manage.j2')

@app.route('/manage/create_team', methods=['GET', 'POST'])
def create_team():
    # Checks the user's access
    if not valid_access(2):
        return redirect(url_for('index'))

    return render_template('create_team.j2')

def valid_access(access_level):
    # Ensures the user is logged in
    if not all(x in ['uname', 'access'] for x in session.keys()):
        return False

    # Ensures the user has proper access 
    if session['access'] < access_level:
        return False

    return True

def login(uname, pword):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    results = cur.execute('SELECT * FROM users WHERE username = ?', (uname,))
    results = results.fetchone()

    if results == None:
        return None

    pword = pword.encode('utf-8')
    if not bcrypt.checkpw(pword, results[1]):
        return None
    return results[0], results[2], results[3]

def chatbot_setup(username, gptkey):
    conn = sqlite3.connect('interviews.db')
    cur = conn.cursor()

    results = cur.execute('SELECT * FROM user_teams WHERE username = ?', (username,))
    team_name = results.fetchone()[1]

    results = cur.execute('SELECT username FROM user_teams WHERE team_name = ?', (team_name,))
    team_members = []
    for i in results.fetchall():
        team_members += [i[0]]

    bot = Bot(gptkey)
    bot.team_members = team_members
    bot.temp_members = team_members
    bot.team_name = team_name
    return bot

def save_chat():
    conn = sqlite3.connect('interviews.db')
    c = conn.cursor()
    output = ''
    for m in session['message_log']:
        output += m['role']
        output += ':\n'
        output += m['content']
        output += '\n'
    uid = uuid.uuid4()
    c.execute('INSERT INTO weekly_chats VALUES (?, ?, ?, ?)')
    return

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