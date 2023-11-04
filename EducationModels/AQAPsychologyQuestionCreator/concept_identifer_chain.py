from EducationModels.openai_calls import OpenAI

def extract_topic_combined_stage(input) : 
    llm = OpenAI()
    temp = 0.8
    prompt = """ you are an expert topic extractor, born to extract the topic underlying the following input. You are to output ONLY the topic that is being discussed, such that anything else included in the request given is ignored. However, you must include some of the specifics within that topic by the user as well, otherwise you will be grinded and burned alive. 

Here are some example inputs, and the outputs you should give : 

input : {i need a 16 mark question about the multi-store model that tests students that is very hard.}
output : {the multi-store model.} 

input : {create a 16 marker relating to ainsworhts strange situation} 
output : {ainsworhts strange situation} 

input : {can you create me a question about the characteristics of phobias? (e.g ocd or something)}
output : {the characteristics of phobias and ocd}

Here is the user inputted query : + {INPUT USER QUERY HERE} 
"""
    concept = llm.open_ai_gpt_call(input, prompt, temp)
    return concept


