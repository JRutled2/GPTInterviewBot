from flask.wrappers import Response
import openai

class Bot():    
    """ Interview Bot Class
    
    The interview bot it used to conduct interviews with students
    on how their project is progressing
    
    Attributes:
        team_members (list[str]): A list of all the team members working on the project.
        message_log (list[dict[str]]): A list of messages between the user, system, and GPT, 
            each element in the list is a dictionary containing the role and content.
        chat_stage (int): Keeps track of current stage in the interview, used for the chat function.
            chat_stage  Chat aspect         Method Called
            ---------   -----------         -------------
                0       Previous Week       chat_previous_week()
                1       Previous Problems   XXX
                2       Plans               XXX
                3       Concerns            XXX
    """
    
    def __init__(self, gpt_key: str, ) -> None:  
        # Stores all the team members
        self.team_members: list[str] = []
        # Stores the message log
        self.message_log: list[dict[str]] = []
        # Current stage in chat function
        self.chat_stage: int = 0
        # Temp List of Team members used for tracking
        self.temp_members: list[str] = self.team_members

        # Sets the openai key
        openai.api_key = gpt_key

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

    def chat(self, user_input: str, ) -> list[dict[str]]:
        """ Chat Method That the User Interacts With
        
        This is the main function that the user calls when using the Chatbot.
        This function calls other, more specific funtions depending on the current chat stage. 
        
        Args:
            user_input (str): The input from the user
        
        Returns:
            list[dict[str]]: This method returns the current chatlog, past chats and any newly added chats
        """
        
        # If the userinput is not empty, then it adds it onto the end.
        # The user input will only be empty on the first time chat is called.
        if user_input != '':
            self.message_log += [{'role': 'user', 'content': user_input}]
            
        # Calls appropriate method based on chat stage
        if self.chat_stage == 0:
            self.chat_previous_week()

        return self.message_log
    
    def chat_previous_week(self, ) -> None:
        pass
    
        
    
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
