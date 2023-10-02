import random
import PyPDF2
from EducationModels.openai_calls import OpenAI
import json
import os

# This method returns the string output given a txt name from the 'prompts' folder.
def load_prompts(filename):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'prompts', filename)
    with open(file_path, 'r') as file:
        return file.read()

              
def create_assess_validity_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = load_prompts("assess_validity.txt")
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question

def create_to_what_extent_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = load_prompts("to_what_extent.txt")
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question
def create_how_far_question(pages) : 
    llm = OpenAI()
    temp = 1
    prompt = load_prompts("how_far.txt")
    assess_question = llm.open_ai_gpt4_call(pages, prompt, temp)
    return assess_question  

#Calls the question creation methods based on probabilities of it showing up in an actual exam paper (based on it's distribution in the past)

def create_weighted_random_question(pages) : 
    rand_num = random.uniform(0, 1)
    if rand_num <= 0.35 : 
        question = create_assess_validity_question(pages)
    elif 0.35 <= rand_num <=0.85 :
        question = create_to_what_extent_question(pages)
    else :
        question = create_how_far_question(pages)
    return question
