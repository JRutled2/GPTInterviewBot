from openai import OpenAI
from os import sys

default_prompts = ['Hello, what have you accomplished in the past week?', 
                   'Were there any issues you were unable to solve?',
                   'What do you plan to accomplish this upcoming week?',
                   'Split the task the user stats into a list seperated by new lines.  Do not add any extra text.',
                   'Ask the user about their plan to ',
                   '. If their statements don\'t fulfll the S.M.A.R.T. goals, ask them more questions that will fulfill them.  Only ask them one question at a time and do not menthion the S.M.A.R.T. goals.  When they have fulfilled all the S.M.A.R.T. goals, say "Done!"',
                   'Thank you for chatting this week.  If you have any questions or concerns please let your professor know. Done!']

class Bot():
    def __init__(self, gpt_key):
        self.team_name = ''
        self.team_id = ''

        self.chat_stage = 0

        self.static_log = []
        self.message_log = []

        self.plans = []
        self.plans_stage = 0

        self.client = OpenAI(api_key=gpt_key)

    def get_log(self, ):
        return self.static_log + self.message_log

    def chat(self, message):
        # Stage 0
        if self.chat_stage == 0:
            self.static_log += [{'role': 'assistant', 'content': default_prompts[0]}]
            self.chat_stage += 1
        # Stage 1
        elif self.chat_stage == 1:
            self.static_log += [{'role': 'user', 'content': message}]
            self.static_log += [{'role': 'assistant', 'content': default_prompts[1]}]
            self.chat_stage += 1
        # Stage 2
        elif self.chat_stage == 2:
            self.static_log += [{'role': 'user', 'content': message}]
            self.static_log += [{'role': 'assistant', 'content': default_prompts[2]}]
            self.chat_stage += 1
        # Stage 3
        elif self.chat_stage == 3:
            self.static_log += [{'role': 'user', 'content': message}]

            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{'role': 'system',
                                                                                               'content': default_prompts[3]},
                                                                                              {'role': 'user',
                                                                                               'content': message}])

            self.plans = completion.choices[0].message.content.split('\n')
            self.message_log = [{'role': 'system', 'content': default_prompts[4] + self.plans[0] + default_prompts[5]}]

            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message_log)
            self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]
            self.chat_stage += 1
        # Stage 4
        elif self.chat_stage == 4:
            self.message_log += [{'role': 'user', 'content': message}]

            if 'pass' in message:
                self.plans_stage += 1
                if self.plans_stage >= len(self.plans):
                    self.chat_stage += 1
                else:
                    self.message_log = [{'role': 'system', 'content': default_prompts[4] + self.plans[self.plans_stage] + default_prompts[5]}]
            if self.chat_stage == 4:
                completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message_log)
                self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]

                if 'Done!' in completion.choices[0].message.content:
                    self.plans_stage += 1
                    if self.plans_stage >= len(self.plans):
                        self.chat_stage += 1
                    else:
                        self.message_log = [{'role': 'system', 'content': default_prompts[4] + self.plans[self.plans_stage] + default_prompts[5]}]
                        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message_log)
                        self.message_log += [{'role': 'assistant', 'content': completion.choices[0].message.content}]

        # Stage 5    
        if self.chat_stage == 5:
            self.message_log = [{'role': 'assistant', 'content': default_prompts[6]}]
            self.chat_stage += 1