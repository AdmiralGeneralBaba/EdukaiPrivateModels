from server.AQAPsychologyQuestionCreator.scenario_creator_chain import combined_scenario_creator
from server.openai_calls import OpenAI

def psychology_scenario_question_creator_helper_method(scenario : str, concept : str) : 
    llm = OpenAI()
    prompt = """You are to be an expert question creator, tasked with creating an exam question relating to the following concept { """ + f"{concept}" + """}

Given to you will be the scenario that is tied to this question; you are to simply create the QUESTION associated with the scenario and concept ONLY. 

the question must match the tone, length and style of the questions here, as well as perfectly relate to both the concept AND the scenario.

Here are example outputs you should emulate in your output : 

EXAMPLE 1 : {

scenario : {Rory is talking with his grandparents and playing a game on his phone at the same time.
The game involves matching blocks of the same colour to complete vertical and horizontal
lines. It is only when his grandparent asks him to describe his route to school that Rory
puts down his game so he can concentrate fully on his answer.}

associated_question : {Discuss the working memory model. Refer to Rory’s behaviour in your answer.}
}

EXAMPLE 2 : { 
scenario : {Natasha had studied a lot for her A-level Drama performance, mostly practising lines from
a play alone in her room. However, once on stage in front of her teacher and the
examiners, Natasha struggled to remember her lines. Instead, she kept quoting lines from
a different play she had once learnt for GCSE.}

associated_question : {Discuss retrieval failure and interference as explanations for forgetting. Refer to Natasha’s drama performance in your answer.}
}

EXAMPLE 3 : { 
scenario : {It is the end of the school day and Freddie is pushing other students in the bus queue.
“Stop it, will you?” protests one of Freddie’s classmates.
“You can’t tell me what to do!” laughs Freddie.
At that moment, Freddie turns to see the deputy head, wearing a high-visibility jacket,
staring angrily at him. Without thinking, Freddie stops pushing the other boys and waits
quietly in line.}


associated_question : {Discuss the legitimacy of authority and agentic state explanations of obedience.
Refer to Freddie’s behaviour in your answer.}
}

ONLY output the question generated based on both the concept and the scenario.

Here is the scenario : 
"""
    temp = 0.9

    exam_question = llm.open_ai_gpt4_call(scenario, prompt=prompt, setTemperature=temp)
    return exam_question

def psychology_description_16_marker_question_creator(context : str, query : str) : 
    llm = OpenAI() 
    prompt = """You are to be an expert question creator, tasked with creating an exam question that ties as best you can to the user query given, and the contextual knowledge to base the question off of. 

Given to you will be a list of facts that relate to the user's question demands; ONLY use this as the context requried to create your question

the question must match the tone, length and style of the questions here, as well as perfectly relate to both the query AND the facts given.

Here are example outputs you should emulate in your output : 

EXAMPLE 1 : {
Describe how situational variables have been found to affect obedience. Discuss what these situational variables tell us about why we obey.  
}

EXAMPLE 2 : { 
Outline Lorenz’s and Harlow’s animal studies of attachment. Discuss what these studies might tell us about human attachment. }

ONLY output the question generated based on both the content given AND the query.

Here is the query :""" + "{" + f"{query}" + "}" +  """and here is the context to base your question off: """
    temp = 0.9

    question = llm.open_ai_gpt4_call(context, prompt, temp)
    return question

def psychology_discussion_16_marker_question_creator(context : str, query : str) : 
       
    
       llm = OpenAI() 
       prompt = """You are to be an expert question creator, tasked with creating an exam question that ties as best you can to the user query given, and the contextual knowledge to base the question off of. 

Given to you will be a list of facts that relate to the user's question demands; ONLY use this as the context requried to create your question

the question must match the tone, length and style of the questions here, as well as perfectly relate to both the query AND the facts given.

The question type you are to make is supposed to be a straightfoward disscusion/explaination question relating to a specific part of psychology.

Here are example outputs you should emulate in your output : 

EXAMPLE 1 : {
Discuss statistical infrequency and deviation from social norms as definitions of abnormality.
}

EXAMPLE 2 : { 
Psychologists investigating social influence have discovered several reasons why people conform. Discuss what psychological research has told us about why people conform.
}

EXAMPLE 3 : { 
Discuss the cognitive approach to treating depression.
}

ONLY output the question generated based on both the content given AND the query.

Here is the query :""" + "{" + f"{query}" + "}" +  """and here is the context to base your question off: """
       temp = 0.9

       question = llm.open_ai_gpt4_call(context, prompt, temp)
       return question

def psychology_16_mark_scenario_creator_full(text, concept) : 
    scenario = combined_scenario_creator(text, concept)
    question = psychology_scenario_question_creator_helper_method(scenario, concept)
    exam_question = scenario + " " + question
    return exam_question

