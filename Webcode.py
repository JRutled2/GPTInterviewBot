from Chatbot import Bot
from flask import Flask
'''
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/chat')
def user_chat():
    return 'Hello'


if __name__ == '__main__':
    app.run()

'''
b = Bot('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')

b.weekly_chat()
