from openai_calls import OpenAI
from smart_gpt_v1 import SmartGPTV1
import re


class TutorAIV1:
    def __init__(self):
        self.chat_history = []
        self.gpt_initialise = OpenAI()
        self.SmartGPT = SmartGPTV1()
    def get_difficulty(self, user_input):
        difficultyDeterminePrompt = """Based on the user's prompt, determine it's difficulty in answering. return ONLY one of the three, based on how hard it is to answer: 
                                    "EASY", "MEDUIM", "HARD" """ 
        
        return self.gpt_initialise.open_ai_gpt_call(user_input, difficultyDeterminePrompt)
    def get_responseGpt3(self, user_input):
        gpt3Prompt = ""
        return self.gpt_initialise.open_ai_gpt_call(user_input, gpt3Prompt)
    def get_responseGpt4(self, user_input) : 
        gpt4Prompt = ""
        return self.gpt_initialise.open_ai_gpt4_call(user_input, gpt4Prompt)
    def get_smartResponseGpt4(self, user_input) : 
        SmartGPTPrompt = ""
        return self.SmartGPT.smart_gpt(user_input)
    def tutor_ai_initialise(self, user_input):            
        
        difficulty = self.get_difficulty(user_input)
        print(difficulty)
        if re.match(r'^EASY', difficulty):
            print("This is an EASY question")
            print(self.get_responseGpt3(user_input))
        elif re.match(r'^MEDIUM', difficulty): 
            print("This is a MEDIUM question")
            print("GPT answer here")
            print(self.get_responseGpt3(user_input))
        elif re.match(r'^HARD', difficulty): 
            print("This is a HARD question")
            print("SmartGPT response here") 
            print(self.get_responseGpt3(user_input))
        else:
            print("Error in difficulty determination.")
        #Change print to return 