from openai_calls import OpenAI

def psychology_scenario_16_marker_question_creator(scenario : str, concept : str) : 
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