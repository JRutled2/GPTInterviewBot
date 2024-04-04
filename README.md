# BuisnessInterviewBot

# Installation and Usage
1. Download the Code
2. Run the following pip commands:
  - pip install --upgrade openai
  - pip install --upgrade bcrypt
  - pip install --upgrade flask
4a. Run webapp.py
4b. Run webapp.py XXXXX (Replace XXXXX with the port to listen to)

# API Key
API keys are found at the following link:
https://platform.openai.com/api-keys
API Keys are entered under the "More" tab.

# User Registration
1. On the login page, click the register button.
2. Enter a desired username, password, and team id
4. Click register
5. User can now login with given username and password

# Management
- Adding Teams:
  1. From the management homepage, click the "Create Team" tab
  2. Enter the team's desired name
  3. Click create team
  4. The team's id, which is used for creating accounts, can be found under the "View Teams" tab on the management homepage

# Viewing Past Chats
Past Chats can be viewed by following next steps:
1. From the management homepage, click the "View Teams" tab.
2. Click the desired team.
3. Click on the desired chat.
Past chats are stored under the chats folder, in json format.  The files are named by their team id.