from openai_calls import OpenAI

class SmartGPTV1 : 
    chain_of_thought_prompt = " Answer : Let’s work this out in a step by step way to be sure we have the right answer"
    reflexion_prompt = "You are a researcher tasked with investigating the the 3 response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors: "
    dera_prompt = " You are a resolver tasked with 1) finding which of the X answer options the researcher thought was best 2) improving that answer and 4) Printing the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer: "
    gptAgent = OpenAI()
    def chain_of_thought(self, user_input):
        combined_output = ""
          
        for i in range(3):
            reply_content = self.gptAgent.open_ai_gpt_call(user_input, "Question :" + self.chain_of_thought_prompt)  # Calling the function and getting the reply content
            combined_output += reply_content + "\n"  # Adding reply_content to combinedOutput

        return combined_output  # Printing combinedOutput after all iterations
    def reflexion_process(self, user_input): 
        return self.gptAgent.open_ai_gpt_call(self.chain_of_thought(user_input), self.reflexion_prompt)
    def dera_process(self, user_input):
        return self.gptAgent.open_ai_gpt_call(self.reflexion_process(user_input), self.dera_prompt)
    def smart_gpt(self, user_input): 
        smartGPT = SmartGPTV1()
        smartGPT.dera_process(user_input)
       