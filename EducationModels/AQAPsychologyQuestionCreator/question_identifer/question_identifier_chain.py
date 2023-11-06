from EducationModels.openai_calls import OpenAI

def psychology_question_type_identifier(query) :
    llm = OpenAI() 
    prompt = """You are to be a expert question type decider, who has years of experience understanding what a user wants in relation to picking the right type of psychology essay question they want based on the query that is given to you. 

In psychology essay questions, there are multiple different subtypes they could fall under. Provided is all the different types of questions and their description, and your one sole mission is to, based on this input, identify which question type fits best with what the user wants

if no specific question types falls into their request, then choose one in your long experience that fits best with the topic.

Here are the different types of questions that can come up : 

1. Discussion type question (discussion)
This type of questions asks the user to discuss a particular topic in his essay

2. Description-type question (description)
This type of question asks the user to describe/outline a particular topic in his essay

3. Scenario-based question (scenario)
This type of question involves a scenario describing a real-life example in people exhibiting the symptoms of a specific psychological phenomenon (e.g someone wanting to wash their hands loads of times for OCD), and then a question related to this scenario and the psychological reason behind it.

(The brackets indicate the key value for each of these question types)

ONLY output which key-value you chose, and NOTHING ELSE.

Here is the user input : 

 """
    
    temp = 0.9
    question_type = llm.open_ai_gpt4_call(query, prompt, temp)
    return question_type



print(psychology_question_type_identifier("make me a question about OCD and it's effects on people's lives"))