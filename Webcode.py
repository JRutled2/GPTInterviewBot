from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from Chatbot import chat
from flask import Flask, session, redirect

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'gptkey' in request.form:
            session['uname'] = request.form['uname']
            session['gptkey'] = request.form['gptkey']
            session['chat_stage'] = -1
            session['message_log'] = []
            return redirect(url_for('user_chat'))
    return render_template('login.j2')

@app.route('/chat', methods=['GET', 'POST'])
def user_chat():
    #if request.method == 'GET':
    #    return redirect(url_for('index'))
    
    if 'uname' in session:
        if 'chat' in request.form:
            session['message_log'] += [{'role': 'user', 'content': request.form['chat']}]
        session['message_log'], session['chat_stage'] = chat(session['message_log'], session['chat_stage'], session['gptkey'])
        return render_template('chat.j2', message_log=session['message_log'])
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
