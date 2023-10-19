from flask.wrappers import Response
import openai

class Bot():

    def __init__(self, gpt_key):
        openai.api_key = gpt_key

        self.team_members = ['Mike']

        self.message_log = []

    def chat(self, prompt):
        self.message_log += [{'role': 'user', 'content': prompt}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.message_log, temperature=0)
        self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
        return completion.choices[0].message.content

    def test(self, ):
        print(str(self.team_members))

    def weekly_chat(self, ):
        # Asks Each team member what they acomplished in the past week
        print(f'Hello, What did {self.team_members[0]} acomplish in the past week.')
        userin = input('> ')
        for i in self.team_members[1:]:
            print(f'Thank you, now what did {i} acomplish in the past week.')
            userin = input('> ')

        # Asks about what they plan on completing in the upcoming week
        self.message_log = [{'role': 'system', 'content': "You are asking me about what I plan to complete in the next week."},
                {'role': 'system', 'content': "If my statements don't fulfll the S.M.A.R.T. goals, ask me more questions that will fulfill them.  Only ask me one question at a time.  When I have fulfilled all the S.M.A.R.T. goals, say Done!"}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.message_log, temperature=0)
        print(completion.choices[0].message.content)
        self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
        userin = input('> ')
        while userin != 'quit':
            response = self.chat(userin)
            if 'Done!' in response:
                break
            print(response)
            userin = input('> ')
    
def ask_gpt(message_log):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_log, temperature=0)
        message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
        return message_log

def chat(message_log, stage, key):
        
    # Stage is -n for n number of team members, ask what they acomplished in the past week
    if stage < 0:
        stage += 1
        message_log += [{'role': 'assistant', 'content': 'Hello, what have you acomplished in the past week?'}]
        return message_log, stage
    
    # Stage 0 ask if they had any problens
    if stage == 0:
        message_log += [{'role': 'assistant', 'content': 'Did you have any problems you need help with?'}]
        return message_log, 1

    # Stage 1 is an intermediary stage where roles are added to the message log
    if stage == 1:
        openai.api_key = key
        message_log += [{'role': 'system', 'content': "You are asking me about what I plan to complete in the next week."},
                        {'role': 'system', 'content': "If my statements don't fulfll the S.M.A.R.T. goals, ask me more questions that will fulfill them.  Only ask me one question at a time.  When I have fulfilled all the S.M.A.R.T. goals, say Done!"}]
        message_log = ask_gpt(message_log)
        return message_log, 2

    if stage == 2:
        openai.api_key = key
        message_log = ask_gpt(message_log)
        return message_log, 2
