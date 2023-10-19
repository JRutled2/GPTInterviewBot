from flask.wrappers import Response
import openai

class Bot():    
    
    def __init__(self, gpt_key: str) -> None:
        # Sets the openai key
        openai.api_key = gpt_key
        # Stores all the team members
        self.team_members = []
        # Stores the message log
        self.message_log = []
        # Current stage in chat function
        self.chat_stage = 0

    def ask_gpt(self, ) -> None:
        """ Method that Generates a New Response From the GPT Model
        
        This method generates a ChatCompletion from the openai API
        and adds output to the message_log variable.
            
        ChatCompletion API:
        https://platform.openai.com/docs/api-reference/completions/create
        """
        
        # Completion object that contains the output from GPT
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                  messages=self.message_log, 
                                                  temperature=0)
        # Adds GPT output to the message log
        self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]

    def chat(self, user_input: str) -> list[dict[str]]:
        """ Chat Method That the User Interacts With
        
        """
        return self.message_log
    
    # Old Chat Function
    def OLD_weekly_chat(self, ):
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

    # Stage 2 is the normal plan conversations
    if stage == 2:
        openai.api_key = key
        message_log = ask_gpt(message_log)
        return message_log, 2
