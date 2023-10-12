import openai

class Bot():

    def __init__(self, gpt_key):
        openai.api_key = gpt_key

        self.message_log = []

    def __chat(prompt):
        self.message_log += [{'role': 'user', 'content': prompt}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.message_log, temperature=0)
        self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
        return completion.choices[0].message.content

    def weekly_chat():
        print('Hello, What did you acomplish in the past week.')
        message_log = [{'role': 'system', 'content': 'You are a professor interview groups for a class, as them what they acomplished in the last week.  When they say that is all they completed, say "Done!"'},
                    {'role': 'assistant', 'content': 'Hello, What did you acomplish in the past week?'}]

        # Questions about what was completed in the past week
        userin = input('> ')
        while userin != 'quit':
        response = chat(userin)
        if 'Done!' in response:
            break
        print(response)
        userin = input('> ')


        message_log = [{'role': 'system', 'content': "You are asking me about what I plan to complete in the next week."},
                        {'role': 'system', 'content': "If my statements don't fulfll the S.M.A.R.T. goals, ask me more questions that will fulfill them.  Only ask me one question at a time.  When I have fulfilled all the S.M.A.R.T. goals, say Done!"}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_log, temperature=0)
        print(completion.choices[0].message.content)
        message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
        userin = input('> ')
        while userin == 'quit':
        response = chat(userin)
        if 'Done!' in response:
            break
        print(response)
        userin = input('> ')

        print('Finished!')