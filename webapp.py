import sqlite3
import bcrypt 
from chatbot import Bot
from flask import Flask, session, redirect
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/', methods=['GET', 'POST'])
def index():
    # If user attempted to login
    if request.method == 'POST' and 'pword' in request.form:
        # Call the login function
        login_attempt = login(request.form['uname'], request.form['pword'])
        # If login fails
        if login_attempt == None:
            return redirect(url_for('index'))

        # If login Succeeds
        session['uname'] = login_attempt[0]
        session['access'] = login_attempt[1]
        session['message_log'] = []
        app.config['bot'] = chatbot_setup(login_attempt[0], request.form['gptkey'])
        session['team_name'] = app.config['bot'].team_name
        return redirect(url_for('user_chat'))
    return render_template('login.j2')

@app.route('/chat', methods=['GET', 'POST'])
def user_chat():
    #if request.method == 'GET':
    #    return redirect(url_for('index'))
    
    if 'uname' in session:
        if 'chat' in request.form:
            session['message_log'] = app.config['bot'].chat(request.form['chat'])
        else:
            session['message_log'] = app.config['bot'].chat('')
        return render_template('chat.j2', message_log=session['message_log'])
    else:
        return redirect(url_for('index'))

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

if __name__ == '__main__': 
    #app.run(host='0.0.0.0', port=12429)
    app.run(debug=True)