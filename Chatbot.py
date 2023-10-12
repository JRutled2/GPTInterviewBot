from flask.wrappers import Response
import openai

class Bot():

    def __init__(self, gpt_key):
        openai.api_key = gpt_key

        self.team_members = ['Mike', 'John', 'Bill']

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

print('Finished!')