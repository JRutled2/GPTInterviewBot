# Usage Guide

## Setup
1. Download the Code
2. Run the following pip commands:
    - pip install --upgrade openai
    - pip install --upgrade bcrypt
    - pip install --upgrade flask
    - pip install --upgrade sqlite3
3. Create the database by following the steps:
    1. python3 admincode.py
    2. Type "x" then click enter
    3. Type "y" then click enter
4. Create managers by following the steps:
    1. Type "1" then click enter
    2. enter a desired username and click enter
    3. enter a desired password and click enter
5. admincode.py can now by closed by typing "q" then clicking enter     
6. Run the website with one of the following:
    - python3 webapp.py
    - python3 webapp.py XXXXX (Replace XXXXX with the port to listen to)
    - nohup python3 webapp.py XXXXX & (Replace XXXXX with the port to listen to)
  
## File Storage
- User chats are stored in the chats directory in .json format.
- system logs are stored in the system_logs directory in .txt format.
