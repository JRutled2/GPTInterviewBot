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
    if request.method == 'POST':
        if 'pword' in request.form:
            session['uname'] = request.form['uname']
            session['message_log'] = []
            app.config['bot'] = Bot(request.form['gptkey'])
            return redirect(url_for('user_chat'))
    return render_template('login.j2')

@app.route('/chat', methods=['GET', 'POST'])
def user_chat():
    #if request.method == 'GET':
    #    return redirect(url_for('index'))
    
    if 'uname' in session:
        if 'chat' in request.form:
            print('GOOD')
            session['message_log'] = app.config['bot'].chat(request.form['chat'])
        else:
            session['message_log'] = app.config['bot'].chat('')
        return render_template('chat.j2', message_log=session['message_log'])
    else:
        return redirect(url_for('index'))


if __name__ == '__main__': 
    app.run(port=12429)
