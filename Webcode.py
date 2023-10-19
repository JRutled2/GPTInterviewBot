from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from Chatbot import Bot
from flask import Flask, session, redirect

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'uname' in request.form:
            session['uname'] = request.form['uname']
            return redirect(url_for('user_chat'))
    return render_template('login.j2')

@app.route('/chat')
def user_chat():
    if 'uname' in session:
        return render_template('chat.j2')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

'''
b = Bot('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')

b.weekly_chat()
'''
