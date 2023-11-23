import asyncio
from EducationModels.openai_calls import OpenAI
import re



#     Fixed stages for a single lesson :
#################    FIXED STAGES FOR EVERY LESSON/POWERPOINT:  #####################
def extract_lesson_facts(lesson):
    # Extract 'lesson_facts' from the lesson dictionary
    lesson_facts = lesson["lesson_facts"]
    # Join the facts into a single string with each fact on a new line
    facts_string = "\n".join(lesson_facts)
    
    return facts_string
def stage_1_groupings_for_facts(numberedFacts) : 
    gptAgent = OpenAI()
    stage1Temp = 0.64
    stage1Prompt = """Group the inputted facts into logically consistent chunks to be used for a SINGLE  powerpoint slide - DO NOT make the facts be too long. ONLY output the numbers of the facts, and put them in curly brackets e.g {1, 5, 6} or {7, 13, 2}, and then, in your mind, INTERNALLY justify WHY you chose them.
Then, write a short, 1 line description of the facts NEXT to the facts, like so :
{1, 2, 3}, blah blah, 
{4,5,6}, blah blah, 
etc
also, each section HAS  to be between 2 -  5 facts, and no more/less than that. IF IT'S LES S OR MORE THAN THAT YOU DIE.
For example, you can't output 'these facts are about the...'. Say this in your mind, you must ONLY output the numbers, e.g {1,6,5}
I also want you to order them in the best way to learn these facts, for a powerpoint
DO NOT PRINT YOUR THOUGHTS - I CANNOT STRESS THIS ENOUGH. IF YOU DO, MY FAMILY WILL DIE AND I WILL KILL YOU
here are the facts: 
"""
    optimalFactGroupings= gptAgent.open_ai_gpt4_call(numberedFacts, stage1Prompt, stage1Temp)
    return optimalFactGroupings
def stage_2_powerpoint_plan(numberedFacts, optimalFactGroupings) : 
    gptAgent = OpenAI()
    stage2Temp = 0.0
    stage2Prompt = """Pretend you are a planner for a powerpoint presentation, tasked the specified modules for each slide. Based on the facts and their corropsonding numbers, as well as the groupings given to you, I need you to :
1. Choose the module for the powerpoint slide number
2. In this module, reprint it, and in the space for 'fact numbers', I want you to insert the fact numbers to be included in that PowerPoint, 
3. Output should be a complete powerpoint plan, with the modules for each powerpoint slide and their corrosponding fact numbers included

organise it like so : 
POWERPOINT 1 : {your output}
POWERPOINT 2 : {your output} 
etc 
Here are the modules name; JUST print out the module name you picked ,and the facts with them. : 
1. Title Page  {no facts needed - just create a title and subtitle separated by a comma}

2. L.O page  + {Learning objects for the lesson} 

3. general_content_page + {fact numbers} + {grouping description supplied in the input NEXT to the fact number groupings}

4. Ending slide + {Ending summary title, then a comma, then the summary}
heres an example of these implemented, DO NOT deviate from this structure: 
POWERPOINT 1 : Module : Title Page - Hearts of Iron IV, An Insight on Aircraft and their Functionalities

POWERPOINT 2 : Module : L.O page - Learning objects for the lesson

POWERPOINT 3 : Module : general_content_page - {1, 2, 3, 17}, Understanding basics of Hearts of Iron IV

POWERPOINT 4 : Module : general_content_page - {18, 19, 20, 21}, Importance and specialties of Naval Bombers

POWERPOINT 5 : Module : general_content_page - {4, 5, 6, 7}, Types of fighters and their strengths

POWERPOINT 6 : Module : general_content_page - {8, 9, 10, 11}, Role and capabilities of CAS planes

POWERPOINT 7 : Module : general_content_page - {12, 13, 14}, Tactical bombers and their functionalities

POWERPOINT 8 : Module : general_content_page - {15, 16}, Strategic bombers and their impact   

POWERPOINT 9 : Module : Ending slide - Conclusion, Summary of the different types of aircraft in Hearts of Iron IV, their roles, and their impacts.
Here are the lesson facts : 
"""      
    gptInput = numberedFacts + optimalFactGroupings
    powerpointPlan = gptAgent.open_ai_gpt4_call(gptInput, stage2Prompt, stage2Temp)
    return powerpointPlan  

# stage_2_3 performs the difficulty calcluation for each of the sub-topics, and inputs them into the powerpoint plan.
#This replaces the fact numbers with text to be inputted into the difficulty calculation
def stage_2_1_replace_fact_numbers_with_texts(fact_groupings : str, facts : str):
    # Parse the facts string to create a mapping of fact number to fact text
    facts = re.findall(r'(\d+)\. \{([^}]+)\}', facts)
    fact_map = {num: fact for num, fact in facts}

    # Function to replace fact numbers with texts
    def replace_fact(match):
        fact_nums = match.group(1).split(', ')
        facts = [fact_map[num.strip()] for num in fact_nums if num.strip() in fact_map]
        return "{" + '; '.join(facts) + "}, " + match.group(2)

    # Replace fact numbers in the input string
    return re.sub(r'\{([\d, ]+)\}, ([^\n]+)', replace_fact, fact_groupings)


# Takes an inputted fact groupings + their sub topic title, and evaluates each of it's difficulties, and returns the string output. 
def stage_2_1_difficulty_calculation(fact_groupings, facts) : 

    subtopics_to_evaluate = stage_2_1_replace_fact_numbers_with_texts(fact_groupings, facts)
    llm = OpenAI()
    temp = 0.8
    prompt = """Based on the inputted facts and their topics, I want you to classify them into three levels of difficulty, 'EASY', 'MEDIUM' or 'HARD', respective to someone seeing this content for the first time.

Your output MUST look like this. KEEP the curly brackets:
INSERT TOPIC HERE : {INSERT DIFFICULTY HERE}
INSERT 2nd TOPIC HERE : {INSERT DIFFICULTY HERE}
etc

Here are the topics, and their corresponding facts :
"""
    difficulty_evaluation = llm.open_ai_gpt4_call(subtopics_to_evaluate, prompt, temp)
    return difficulty_evaluation


#stage_2_3 adds in the difficulty value into the powerpoint slides : 


# This creates a dictionary for the difficulty calculation output.
def stage_2_1_create_dictionary(difficulty_calculation):
    # Split the string by newlines to get each topic and difficulty
    items = difficulty_calculation.split('\n')
    dictionary = {}

    # Process each item and add to dictionary
    for item in items:
        # Split the item into key and value
        key, value = item.split(' : ')
        key = key.strip()  # Remove leading/trailing whitespace
        value = value.strip('{} ')  # Remove curly brackets and trailing whitespace
        dictionary[key] = value
    
    return dictionary

# This creates the modified powerpoint plan by inputing the dictionary and using that to find the topic, and add on the difficutly calculated. 
def stage_2_1_difficulty_calculation_addon_powerpoint_plan(powerpoint_plan, difficulty_calculation_dictionary):
    modified_plan = powerpoint_plan
    for topic, difficulty in difficulty_calculation_dictionary.items():
        # Use regex to find each occurrence of the topic in the plan
        modified_plan = re.sub(f'({topic})', r'\1 {' + difficulty + '}', modified_plan)

    return modified_plan

def stage_2_1_submodule_insertion_content_pages(powerpoint_plan) : 
    llm = OpenAI()
    prompt = """Pretend you are an expert planner for a powerpoint slide, tasked with choosing the submodules for the powerpoint plan given. 
A submodule is a variant of the modules named in the powerpoint plan, such that they do a specific task. 

For the module given, there are submodules that corrospond to the difficulty level of the slide.

The module you will change is the 'general_content_page' : 

The submodules for the 'EASY' difficulty are :
'general_content_page_easy_bullet_points' 

The submodules for the 'MEDIUM difficulty are : 
'general_content_page_medium_slide_breakup' 

the submodules for the 'HARD' difficulty are : 
'general_content_page_hard_slide_breakup'

Here is the current powerpoint plan; you MUST change all of the 'general_content_page' modules with the best one that fits, according to the ones you can choose within their difficulty level. You are to return ONLY the new, improved powerpoint plan, and NOTHING ELSE.  : 

"""
    temp = 0
    powerpoint_plan_with_content_modules = llm.open_ai_gpt_call(powerpoint_plan, prompt, temp)
    return powerpoint_plan_with_content_modules

#Method combines all of 2_1 difficulty calculation and general content page addons to create the new powerpoint update.
def stage_2_1_final_difficulty_calculation_method(powerpoint_plan, fact_groupings, facts) : 
    difficulty_calculation = stage_2_1_difficulty_calculation(fact_groupings, facts)
    difficulty_dictionary = stage_2_1_create_dictionary(difficulty_calculation)
    powerpoint_difficulty_addon = stage_2_1_difficulty_calculation_addon_powerpoint_plan(powerpoint_plan, difficulty_dictionary)
    final_powerpoint_plan  = stage_2_1_submodule_insertion_content_pages(powerpoint_difficulty_addon)
    return final_powerpoint_plan




def stage_2_2_question_activity_addon_powerpoint_plan(powerpoint_plan, lesson_facts) : 
    gptAgent = OpenAI()
    stage_2_1_temp = 0.6
    prompt = """Pretend you are an expert planner for a powerpoint slide, tasked with placing activity OR question slides within the basic powerpoint plan given. You are to insert question slides, where needed, with the fact numbers attached to that slide where the questions will be based off.

Here are the module names; JUST print out the module name you picked ,and the facts with them. : 
1. question_module + {Insert the fact numbers that will be covered}

2. activity_module + {Insert the fact numbers that will be covered} 

The question module is generally meant for only individual slides, and is meant to keep students engaged throughout.

The activity module is meant to be a holistic activity for the entire lesson - USE THIS SPARINGLY, but use it AT LEAST ONCE. 

Make sure the facts that are covered in the slide WAS ALREADY covered in previous slides  - if they are not, you will instantly die a painful death.

Here's an example of these implemented. You are to insert these two modules INTO the powerpoint plan, where needed. 

POWERPOINT 4 : Module : question_module - {Insert fact numbers here }

POWERPOINT 5 : Module : activity_module - {insert fact numbers here}
follow these tips on how to insert them:
- each insertion MUST BE PERFECT, AND NOT FORMULAIC 
- You can include multiple PREVIOUS slides facts into either one of these modules
- DO NOT overload it with activities ; each is AT LEAST 5 - 10 minutes long. 

ONLY output the modified plan, AND NOTHING ELSE, OR YOU WILL DIE.

Provided will be the existing plan, and the lesson facts so you understand the context : 
"""
    gpt_input = "FACTS : " + lesson_facts + "and here is the plan :" + powerpoint_plan
    improved_powerpoint_plan = gptAgent.open_ai_gpt4_call(gpt_input, prompt, stage_2_1_temp)
    return improved_powerpoint_plan


def stage_2_2_question_activity_submodule_choice_insertion(powerpoint_plan, lesson_facts) : 
    gpt_agent = OpenAI()
    stage_2_1_temp = 0.91
    #I removed this submodule from the prompt :submodule 1 : 'question_module_1_mcq' : a MCQ based on the facts for that slide.
    prompt = """ Pretend you are an expert planner for a powerpoint slide, tasked with choosing the submodules for the powerpoint plan given. 
A submodule is a variant of the modules named in the powerpoint plan, such that they do a specific task. 

For each module, there are submodules. Here are the submodules for each corresponding modules : 

question_module 
submodule 2 : 'question_module_2_bullet_questions' : short bullet questions based on facts for that lesson
submodule 3 : 'question_module_3_roleplay_questions' : Roleplay styled questions based on the facts for that slide

activity_module 
submodule 1 : 'activity_module_1_brainstroming' : brainstorming task for students based on the facts (15 minutes)
submodule 2 : 'activity_module_2_student_summarisation' : summarisation task for students based on facts of slide (10 minutes)
submodule 3 : 'activity_module_3_qa_pairs' : students are told to pair up with each other, and ask questions and answer to each other. (20 minutes)
submodule 4 : 'activity_module_4_focused_listing' : focused listing task based on facts of the slide. (10 minutes)

you are to change the names of each of these modules, so that they are changed to be one of these submodules. 

ALL of the modules listed  MUST be a submodule. You are to make the BEST possible choice, given the time it takes for each module, the types of facts, and the overall lesson. 
- give variety where possible, to keep the student engaged. 


Here's an example of how you should change them - DO NOT SAY SUBMODULE, STILL CALL IT 'Module' OR YOU WILL BE 100 PERCENT BE GRINDED.: 

POWERPOINT [i] : Module : question_module_3_roleplay_qustions - {FACT NUMBERS HERE}

ONLY OUTPUT THE MODIFIED LESSON PLAN, AND NOTHING ELSE
Here is the lesson facts and the powerpoint plan : 
"""     
    gpt_input = "POWERPOINT FACTS : " + lesson_facts + "and here is the plan : " + powerpoint_plan
    new_powerpoint_plan = gpt_agent.open_ai_gpt4_call(gpt_input, prompt, stage_2_1_temp)
    return new_powerpoint_plan


# Combined method of stage_2_2
def stage_2_2_final_question_activity_addition(powerpoint_plan, lesson_facts) : 
    ques_and_activity_addon_powerpoint_plan = stage_2_2_question_activity_addon_powerpoint_plan(powerpoint_plan,lesson_facts)
    ques_activity_submodule_powerpoint_plan = stage_2_2_question_activity_submodule_choice_insertion(ques_and_activity_addon_powerpoint_plan, lesson_facts)
    return ques_activity_submodule_powerpoint_plan
    



    ### Combined powerpoint plan creator : 
def stage_3_powerpoint_plan_creator(lesson_facts : str, question_activity_choice : bool) : 
    print("FIXED STAGES IN PROGRESS...")
    fact_groupings = stage_1_groupings_for_facts(lesson_facts)
    print(fact_groupings)
    print("STAGE 1 COMPLETE")
    powerpoint_plan = stage_2_powerpoint_plan(lesson_facts, fact_groupings)
    print(powerpoint_plan)
    print("STAGE 2 IN PROGRESS")
    powerpoint_plan_difficulty_addon = stage_2_1_final_difficulty_calculation_method(powerpoint_plan, fact_groupings, lesson_facts)
    print("STAGE 2 COMPLETE")

    print("CHOOSING WHETHER QUESTION MODULES SHOULD BE ADDED...")
    if question_activity_choice == True : 
        question_addon_powerpoint_plan = stage_2_2_final_question_activity_addition(powerpoint_plan_difficulty_addon, lesson_facts)
        print("ADDED QUESTION MODULE")
        return question_addon_powerpoint_plan
    else : 
        print("NO ADDITION NEEDED, RETURNING PLAN")
        return powerpoint_plan_difficulty_addon

