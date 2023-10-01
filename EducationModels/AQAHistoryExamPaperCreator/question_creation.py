import PyPDF2
from EducationModels.openai_calls import OpenAI
import json
import os



def load_prompts(filename):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'prompts', filename)
    with open(file_path, 'r') as file:
        print(file.read())

              
def create_assess_validity_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = """ """
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question

def create_to_what_extent_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = """ """
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question
def create_how_far_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = """ """
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question  


filename = "assess_validity.txt"
load_prompts(filename)