from openai_calls import OpenAI

def fact_diluter_chain(facts) : 
    llm = OpenAI()
    prompt = """ """
    temp = 0.9
    llm.open_ai_gpt4_turbo_call(prompt, temp)