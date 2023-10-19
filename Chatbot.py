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
                0       Previous Week       chat_previous_week
                1       Problems            chat_problems
               2/3      Plans               chat_plans
                4       Concerns            chat_concerns
        temp_members (list[str]): List of team members that is modified for specific funtions
        
    """
    
    def __init__(self, gpt_key: str, ) -> None:  
        # Stores all the team members
        self.team_members: list[str] = ['JD']
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
        elif self.chat_stage == 1:
            self.chat_problems()
        elif self.chat_stage in [2, 3]:
            self.chat_plans()
        elif self.chat_stage == 4:
            self.chat_concerns()
        
        # Returns the message_logs
        return self.message_log
    
    def chat_previous_week(self, ) -> None:
        """ Previous Week Chat Method
        
        This method asks each team member what they have acomplished in the past week.
        Each time it is called it asks the next team member what they acomplished.
        
        """
        
        # If it the last team member, it increases the chat stage
        if len(self.temp_members) == 1:
            self.chat_stage = 1
        
        # Asks a different questions based on if it is the first time chatting
        if len(self.temp_members) < len(self.temp_members):
           message_log += [{'role': 'assistant', 'content': f'Hello, what has {self.temp_members[0]} acomplished in the past week?'}]
        else:
            message_log += [{'role': 'assistant', 'content': f'Thank you, now what has {self.temp_members[0]} acomplished in the past week?'}]
    
    def chat_problems(self, ) -> None:
        """ Asks if the User Had Any Problems
        
        This method asks the user if they had any problems they were unable
        to solve in the last week.
        
        TODO: Add Dynamic Questions
        
        """
        
        # Increases the chat stage
        self.chat_stage = 2
        
        # Adds the problem question to the message_log
        message_log += [{'role': 'assistant', 'content': f'Have you had any problems that you were unable to solve?'}]
    
    def chat_plans(self, ) -> None:
        """ Asks about Plans for Upcoming Week
        
        This method asks about the users plans for the upcoming week.
        The first time it is called, it adds the system content to the message log.
        
        """
        
        # If the stage is 2, it adds the system content.
        # The stage will only be 2 the first time it is called.
        if self.chat_stage == 2:
            message_log += [{'role': 'system', 'content': "You are asking me about what I plan to complete in the next week."},
                            {'role': 'system', 'content': "If my statements don't fulfll the S.M.A.R.T. goals, ask me more questions that will fulfill them.  Only ask me one question at a time.  When I have fulfilled all the S.M.A.R.T. goals, say Done!"}]
            self.chat_stage = 3
        self.ask_gpt
    
    def chat_concerns(self, ) -> None:
        """ Asks about Any Concerns They Have
        
        This method asks the users about any concerns they may have.
        
        TODO: Add Dynamic Questions
        
        """
        
        # Adds the question about concerns to the message_log
        message_log += [{'role': 'assistant', 'content': f'Do you have any other comments or concerns?'}]

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
