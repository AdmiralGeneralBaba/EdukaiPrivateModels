from openai_calls import OpenAI
import re
from mcq_creator_v1 import McqCreatorV1

class PowerpointCreatorV4 : 
    #     Fixed stages for a single lesson :
#################    FIXED STAGES FOR EVERY LESSON/POWERPOINT:  #####################
    def extract_lesson_facts(self, lesson):
        # Extract 'lesson_facts' from the lesson dictionary
        lesson_facts = lesson["lesson_facts"]
        # Join the facts into a single string with each fact on a new line
        facts_string = "\n".join(lesson_facts)
        
        return facts_string
    def stage_1_groupings_for_facts(self, numberedFacts) : 
        gptAgent = OpenAI()
        stage1Temp = 0.64
        stage1Prompt = """Group the inputted facts into logically consistent chunks to be used for a SINGLE  powerpoint slide - DO NOT make the facts be too long. ONLY output the numbers of the facts, and put them in curly brackets e.g {1, 5, 6} or {7, 13, 2}, and then, in your mind, INTERNALLY justify WHY you chose them.
Then, write a short, 1 line description of the facts NEXT to the facts, like so :
{1, 2, 3}, blah blah, 
{4,5,6}, blah blah, 
etc
also, each section HAS  to be between 2 -  5 facts, and no more/less than that. IF IT'S LESS OR MORE THAN THAT YOU DIE.
For example, you can't output 'these facts are about the...'. Say this in your mind, you must ONLY output the numbers, e.g {1,6,5}
I also want you to order them in the best way to learn these facts, for a powerpoint
DO NOT PRINT YOUR THOUGHTS - I CANNOT STRESS THIS ENOUGH. IF YOU DO, MY FAMILY WILL DIE AND I WILL KILL YOU
here are the facts: 
"""
        optimalFactGroupings= gptAgent.open_ai_gpt4_call(numberedFacts, stage1Prompt, stage1Temp)
        return optimalFactGroupings
    def stage_2_powerpoint_plan(self, numberedFacts, optimalFactGroupings) : 
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

3. General content page + {fact numbers} + {grouping description supplied in the input NEXT to the fact number groupings}

4. Ending slide + {Ending summary title, then a comma, then the summary}
heres an example of these implemented, DO NOT deviate from this structure: 
POWERPOINT 1 : Module : Title Page - Hearts of Iron IV, An Insight on Aircraft and their Functionalities

POWERPOINT 2 : Module : L.O page - Learning objects for the lesson

POWERPOINT 3 : Module : General content page - {1, 2, 3, 17}, Understanding basics of Hearts of Iron IV

POWERPOINT 4 : Module : General content page - {18, 19, 20, 21}, Importance and specialties of Naval Bombers

POWERPOINT 5 : Module : General content page - {4, 5, 6, 7}, Types of fighters and their strengths

POWERPOINT 6 : Module : General content page - {8, 9, 10, 11}, Role and capabilities of CAS planes

POWERPOINT 7 : Module : General content page - {12, 13, 14}, Tactical bombers and their functionalities

POWERPOINT 8 : Module : General content page - {15, 16}, Strategic bombers and their impact   

POWERPOINT 9 : Module : Ending slide - Conclusion, Summary of the different types of aircraft in Hearts of Iron IV, their roles, and their impacts.
Here are the lesson facts : 
"""      
        gptInput = numberedFacts + optimalFactGroupings
        powerpointPlan = gptAgent.open_ai_gpt4_call(gptInput, stage2Prompt, stage2Temp)
        return powerpointPlan  
    def stage_2_1_powerpoint_plan(self, powerpoint_plan, lesson_facts) : 
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
    
    def stage_2_2_submodule_choice_insertion(self, powerpoint_plan, lesson_facts) : 
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
    
    def stage_3_lesson_description(self, numberedFacts) : 
        gptAgent = OpenAI()
        stage3Temp = 0.49
        stage3Prompt = """These facts are included for a lesson. Summarise these facts into one,  brief line, outlining the lesson."""
        lessonDescription = gptAgent.open_ai_gpt4_call(numberedFacts, stage3Prompt, stage3Temp)
        return lessonDescription
    def stage_3_facts_for_slide_powerpoint_extractor(self, powerpointPlan):
        # Match either a double newline or the end of the string
        powerpointSlides = re.findall(r'(POWERPOINT \d+ : .+?)(?:\n\n|$)', powerpointPlan, re.DOTALL)
        return powerpointSlides

#############     MODULE GENERIC CODE:        ###############
    # Looping stages 
    #Extracts the powerpoint individual slide plans, and the total amount of slides for the current powerpoint
    
    #Extracts the fact numbers from the optimum grouping of a single powerpoint slide 
    def stage_4_extract_values_from_braces(self, substring: str):
        # Extract all values within curly braces from the given substring
        regex_pattern = r'\{([^}]+)\}'
        return re.findall(regex_pattern, substring)
    
    def stage_4_facts_extraction_from_choices(self, slide_plan, factsString):
        # Use regex to extract the fact numbers from the slide content
        fact_numbers_match = re.search(r'\{(.+?)\}', slide_plan)
        if fact_numbers_match is None:
            return ""

        fact_numbers = fact_numbers_match.group(1)
        fact_numbers = list(map(int, fact_numbers.split(',')))  # Convert to a list of integers

        # Create a list to store the facts for this slide
        slide_facts = []

        # Use regex to extract facts based on fact numbers
        for num in fact_numbers:
            fact_match = re.search(rf"{num}\.\s*{{(.*?)}}", factsString)
            if fact_match:
                slide_facts.append(f"{num}. {{{fact_match.group(1)}}}")

        # Join the list of facts into a single string
        slide_facts_string = ' '.join(slide_facts)
        return slide_facts_string


    def stage_4_content_title_layout_splitter(self, powerpointSlide):
        match = re.search(r"TITLE\s*:\s*((?:.|\s)*?)\s*CONTENT\s*:\s*((?:.|\s)*)", powerpointSlide, re.IGNORECASE)
        if match:
            title, content = match.groups()
            return title.strip(), content.strip()
        else:
            print("No match found in the provided slide content.")



    def stage_4_title_subtitle_layout_spliter(self, powerpointSlide):
        match = re.search(r"TITLE\s*:\s*(.+)\s*\n\s*SUBTITLE\s*:\s*(.+)", powerpointSlide)

        if match:
            title = match.group(1).strip()
            subtitle = match.group(2).strip()

            return [title, subtitle]
        else:
            return "No match found."
    def stage_4_task_splitter(self, powerpoint_slide: str):
        # Regex pattern targeting only the 'TASK :' section
        task_specific_pattern = r'TASK\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
        
        # Find the substring that starts with "TASK :"
        task_substring_match = re.search(task_specific_pattern, powerpoint_slide)
        if task_substring_match:
            task_substring = task_substring_match.group(1)
        else:
            task_substring = ""

        # Then, extract all values within curly braces from the found substring
        regex_pattern = r'\{([^}]+)\}'
        extracted_values = re.findall(regex_pattern, task_substring)
        
        return extracted_values

    def stage_4_regex_roleplay(self, powerpoint_slide: str):
        # Regex pattern targeting the 'ROLEPLAY' section
        roleplay_pattern = r'ROLEPLAY\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
        roleplay_match = re.search(roleplay_pattern, powerpoint_slide)
        
        if roleplay_match:
            return self.stage_4_extract_values_from_braces(roleplay_match.group(1))
        else:
            return []

    def stage_4_regex_task(self, powerpoint_slide: str):
        # Regex pattern targeting the 'TASK :' section
        task_pattern = r'TASK\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
        task_match = re.search(task_pattern, powerpoint_slide)
        
        if task_match:
            return self.stage_4_extract_values_from_braces(task_match.group(1))
        else:
            return []

    def stage_4_regex_picture(self, powerpoint_slide: str):
        # Regex pattern targeting the 'PICTURE' section
        picture_pattern = r'PICTURE\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
        picture_match = re.search(picture_pattern, powerpoint_slide)
        
        if picture_match:
            return self.stage_4_extract_values_from_braces(picture_match.group(1))
        else:
            return []
    def stage_4_regex_example(self, powerpoint_slide: str) : 
        picture_pattern = r'EXAMPLE\s*:\s*\[(\{[^}]+\}(?:,\s?\{[^}]+\})*)\]'
        picture_match = re.search(picture_pattern, powerpoint_slide)
        
        if picture_match:
            return self.stage_4_extract_values_from_braces(picture_match.group(1))
        else:
            return []

    def extract_slide_number(self, slideOutline):
        match = re.search(r'POWERPOINT\s(\d+)\s:', slideOutline)

        if match:
            slide_number = int(match.group(1))
            return slide_number
        else:
            return "No match found."
    #Extracts the facts from the fact numbers for the powerpoint slide

    #NEED TO CREATE A FUNCTION HERE CALLED 'def stage_4_picture_search(searchQueryList)', where it first checks if it's a list, then searches at position i and returns 
    #the first image that comes up, OR if it's just a string it just searches it up using that string ONLY.

#################    MODULE SPECIFIC CODE:         ##########################: 
    def stage_4_A_slide_general_content_page(self, slideNumber, lessonDecription, powerpointPlan, slideFacts ) : 
        gptAgent = OpenAI()
        stage4Temp = 0.5
        generalContentPagePrompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide ({SLIDE NUMBER}) based on the facts given. Assume that everything in the lesson description is covered in the other slides. Start with a UNIQUE, INTERESTING title, by doing TITLE : INSERT TITLE HERE, and then CONTENT : INSERT THE CONTENT HERE. Tips for content:
- Take into account the context of the overall lesson. 
- Use examples for context/metaphors, with easy-to-understand ways of explaining them
- Use the best techniques to help students understand the concepts
- Make it fun and engaging, but understand that this is one powerpoint slide out of many.
- Use these facts ONLY- DO NOT make up information/facts
- Don't sound cringey or corny
- DO NOT leave any space for placeholder (e.g for an image) - the powerpoint must be a finished product.
- the whole thing should be UNDER 180 words. 
- Use spacing where needed to increase readability
- DO NOT JUST LIST THE FACTS
""" 
        gptInput = "Lesson description : {" + lessonDecription  +"}" + "Lesson Context : {" + powerpointPlan + "}" + f"SLIDE NUMBER IS {slideNumber}, " + "Lesson Facts: "  + slideFacts ## Input for GPT
        print(gptInput)
        powerpointSlide = gptAgent.open_ai_gpt4_call(gptInput, generalContentPagePrompt, stage4Temp) 
 
        return powerpointSlide
        #Split the title and content from the returned powerpoint slide : 
    #Creates the title and content ofr the 'General Content Page' slide.
    ############# MODULE A, 'General Content Page' ###################:
    def stage_4_A_picture_query_single_picture(self, powerpointSlide) : 
        gptAgent = OpenAI()
        pictureQueryPrompt = """I want you to pretend to be an expert teacher. Your task is to analyse the inputted powerpoint slide, and from it ONLY print a SINGLE image query that this powerpoint slide needs to be used to search online on google to find the image, like so (dont include the brackets):

'{INSERT SEARCH QUERY HERE}'

Aim to make the search query have the highest chance of success of getting the correct image first time when searching, THINK about it - don't ask for an image that most likely won't exist.
Create only ONE image query
Here is the slide : 
"""
        pictureQuery = gptAgent.open_ai_gpt4_call(powerpointSlide, pictureQueryPrompt, 0.0)
        return pictureQuery
    #Creates the picture search query for the 'General Content Page' slide. 
    def stage_4_A_combined_process(self, slideNumber, powerpointSlideOutlines, lessonDescription, powerpointPlan, lessonFacts):
        #'A' is 'General content page' 
        slideFacts = self.stage_4_facts_extraction_from_choices(powerpointSlideOutlines[slideNumber], lessonFacts) # Gets slide facts
        powerpointSlide = self.stage_4_A_slide_general_content_page(slideNumber, lessonDescription, powerpointPlan, slideFacts) # Creates slide
        searchQuery = self.stage_4_A_picture_query_single_picture(powerpointSlide) # Makes a search query to search online
        powerpointTitleAndContent = self.stage_4_content_title_layout_splitter(powerpointSlide) #Splits slide into a 'Title' string and 'Content' String
        
        # Creating the structured output to match the desired format
        structured_output = {
            "module": "General content page",
            "slide": {
                "title": powerpointTitleAndContent[0], # Assuming the title is the first part of the tuple
                "description": powerpointTitleAndContent[1], # Assuming the content/description is the second part of the tuple
                "image_caption": searchQuery # Here, I'm considering the 'searchQuery' to represent the image caption. Adjust if needed.
            }
        }
        
        # Return the structured output
        return structured_output
    #stage_4_B refers to created the L.O page module
    def stage_4_B_combined_process(self, lessonFacts) : 
        #'B' is L.O page
        gptAgent = OpenAI()
        temperature = 0.5
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Using the inputted facts, you are to create a SINGLE powerpoint slide at {SLIDE NUMBER}. Start with a title for the L.O page, by doing 'TITLE : INSERT TITLE HERE', and then 'CONTENT : INSERT THE CONTENT HERE'. 
- Have it follow a standard L.O page outline
- In the content, in no more than 6 bullet points, create the learning objectives for the lesson.
heres an example output for the 'Content' :  
By the end of this presentation, you should be able to:
Appreciate the significance of budgeting and financial planning in personal finance management.     
Identify the different types of investments, including stocks, bonds, and mutual funds.
Understand the functions and benefits of retirement accounts and their role in long-term financial planning.
Differentiate between saving and investing, and comprehend their respective roles in wealth creation.
Understand the implications of tax planning strategies for individual taxpayers in various income brackets.
Here are the lesson facts :
""" 
        powerpointSlide = gptAgent.open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
        splittedPowerpointSlide = self.stage_4_content_title_layout_splitter(powerpointSlide)
        # Creating the structured output to match the desired format
        structured_output = {
            "module": "L.O page",
            "slide": {
                "title": splittedPowerpointSlide[0], # Assuming the title is the first part of the tuple
                "description": splittedPowerpointSlide[1] # Assuming the content/description is the second part of the tuple
            }
        }
        
        # Return the structured output
        return structured_output
    def stage_4_C_combined_process(self, lessonFacts) : 
        #'C' is Title Page#
        gptAgent = OpenAI()
        temperature = 0.7
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed first powerpoint slide based on the inputted lesson facts. You are to create a perfect Title and subtitle. Put the title in 'TITLE : INSERT TITLE HERE ' then 'SUBTITLE : INSERT SUBTITLE HERE' 
Here are the lesson facts : """
        titlePowerpoint = gptAgent.open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
        print(titlePowerpoint)
        splitTitlePowerpoint = self.stage_4_title_subtitle_layout_spliter(titlePowerpoint)
        # Creating the structured output to match the desired format
        structured_output = {
            "module": "Title Page",
            "slide": {
                "title": splitTitlePowerpoint[0], # Assuming the title is the first part of the tuple
                "description": splitTitlePowerpoint[1] # Assuming the subtitle/description is the second part of the tuple
            }
        }

        # Return the structured output
        return structured_output
    
#stage_4_D refers to the 'Final Slide' module
    def stage_4_D_combine_process(self, lessonFacts):
        gptAgent = OpenAI()
        temperature = 0.
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed FINAL powerpoint slide for your students, so that it is easily readable. Using the inputted facts, you are to create a SINGLE powerpoint slide. Start with a title for the Ending slide, by doing 'TITLE : INSERT TITLE HERE', and then 'CONTENT : INSERT THE CONTENT HERE'. 
    - Have it follow a standard ending slide structure.
    - In the content, keep it brief and short, about what the WHOLE lesson was about in an engaging, fun way for students.
    - It should wrap up what they learnt, and be a conclusion for the students.
    Here are the lesson facts :
    """
        powerpointSlide = gptAgent.open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
        splittedPowerpointSlide = self.stage_4_content_title_layout_splitter(powerpointSlide)

        # Formatting the output as a dictionary
        structured_output = {
            "module": "Ending slide",
            "slide": {
                "title": splittedPowerpointSlide[0],  # Assuming the title is the first part of the tuple
                "description": splittedPowerpointSlide[1]  # Assuming the content/description is the second part of the tuple
            }
        }

        return structured_output
    #'E' is the 'question_module_mcq', need to add this in later, perhaps call the mcq creator and then do something with that by creating some sort of a link, and then the slide is just a slide with a link?
    
  

    #question_module_2_bullet_questions slide creation :  
    def stage_4_E2_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temperature = 1
        input_prompt = """Pretend to be an expert teacher. You are tasked with creating multiple short, bullet type questions for the following facts for a questioning slide in a presentation. 

You MUST output in this way : 

TASK : [{Insert the first bullet question here}, {Insert the next one etc}]. 

INCLUDE the curly AND square brackets, and inside the information should be your output. 

it MUST be under 30 words
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.
- make NO MORE than 5 questions, or you will DIE.
- Cover AS MANY of the points in the questions, while keeping them short, and within the 5 quota given.
Here are the lesson facts you need to cover :
 """
        powerpoint_slide = gpt_agent.open_ai_gpt4_call(lesson_facts, input_prompt, temperature)
        return powerpoint_slide
    #question_module_2_bullet_questions full process : 
    def stage_4_E2_combine_process(self, lesson_facts) : 
        slide = self.stage_4_E2_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "question_module_2_bullet_questions",
            "slide": {
                "task" : splitted_slide
            }
        }
    
        return structured_output
        
    def stage_4_E3_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temperature = 1
        prompt = """Pretend to be an expert teacher. You are tasked with creating a roleplay scenario to create questions for. For these facts, you will create and put the scenario in the 'ROLEPLAY' value, then in the 'TASK' section you will insert the roleplay questions in the format given. in the 'PICTURE' section, you must make a PERFECT google search query to get an image that will help immerse them INTO the roleplay part you have given them.
You MUST output in this way : 

ROLEPLAY [{Insert a short, brief exciting description of the roleplay you will base the questions on, to engage students}]  
TASK : [{Insert the roleplay question here}, {Insert the second roleplay question here etc}] 
PICTURE [{Insert image to get them in the mood of the roleplay you have created.}]

INCLUDE the curly AND square brackets, and inside the information should be your output. 

it MUST be under 30 words
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.
- make NO MORE than 5 questions, or you will DIE.
- Cover AS MANY of the points in the questions, while keeping them short, and within the 5 quota given.
- DO NOT stretch the students too hard; it MUST be achievable with the facts given.
Here are the lesson facts you need to cover :
 """

        slide = gpt_agent.open_ai_gpt4_call(lesson_facts, prompt, temperature)
        return slide 
    #splits up the inputted slide into values within the dictionary of 'slide_content'
    def stage_4_E3_regex_split(self, slide): 
        roleplay = self.stage_4_regex_roleplay(slide)
        task = self.stage_4_regex_task(slide)
        picture = self.stage_4_regex_picture(slide)

        slide = {
            "roleplay": roleplay, 
            "task": task,
            "picture": picture
        }
        
        return slide
    # this is the question_module_3_roleplay_questions submodule
    def stage_4_E3_combine_process(self, lesson_facts) : 
        slide = self.stage_4_E3_slide_content_creation(lesson_facts)
        slide_dict = self.stage_4_E3_regex_split(slide)
        
        structured_output = {
            "module": "question_module_3_roleplay_question",
            "slide": slide_dict
        }
        return structured_output
    
    def stage_4_F1_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temp = 1
        prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to brainstorm about what they have learnt. Your output should be EXACTLY like this structure : 
TASK : [{have the brainstorming task be inside here}]. INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to brainstorm, otherwise you will die.
- the task to them MUST be clear.
Here are the lesson facts you need to cover: 
"""
        slide = gpt_agent.open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    #'F1' is the 'activity_module_1_brainstroming' 
    def stage_4_F1_combined_process(self, lesson_facts) : 
        slide = self.stage_4_F1_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "activity_module_1_brainstroming",
            "slide": {
                "task" : splitted_slide
            }
        }

        return structured_output
    
    def stage_4_F2_slide_content_creation(self, lesson_facts) :
        gpt_agent = OpenAI()
        temp = 0.5
        prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to summarize about what they have learnt. Your output should be EXACTLY like this structure : 
TASK : [{have the summarisation task be inside here}]. INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to brainstorm, otherwise you will die.
- the task to them MUST be clear.
Here are the lesson facts you need to cover:
"""

        slide = gpt_agent.open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    
    #'F2' is the 'activity_module_2_student_summarisation' 
    def stage_4_F2_combined_process(self, lesson_facts) :
        slide = self.stage_4_F2_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "activity_module_2_student_summarisation",
            "slide": {
                "task" : splitted_slide
            }
        }
        return structured_output
    
    def stage_4_F3_slide_content_creation(self, lesson_facts) :
        gpt_agent = OpenAI()
        temp = 0.8
        prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to pair up, and for them to ask each other questions to each other and to answer the questions from their partner. Have it be a game, almost trying to catch them out on certain sections. Include an example with your output.  Your output should be EXACTLY like this structure : 
TASK : [{have the brainstorming task be inside here}]. EXAMPLE [{Have the example inside here, in this format: Q: "QUESTION HERE" A"ANSWER HERE"}]

INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover: 

"""
    
        slide = gpt_agent.open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    def stage_4_F3_regex_split(self, slide) : 
        task = self.stage_4_task_splitter(slide)
        example = self.stage_4_regex_example(slide)

        slide = {
            "task" : task,
            "example" : example
        }
        return slide
    
    #'F3' is the 'activity_module_3_qa_pairs'
    def stage_4_F3_combined_process(self, lesson_facts) : 
        slide = self.stage_4_F3_slide_content_creation(lesson_facts)
        slide_dict = self.stage_4_E3_regex_split(slide)
        
        structured_output = {
            "module": "activity_module_3_qa_pairs",
            "slide": slide_dict
        }
        return structured_output
    def stage_4_F4_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temp = 0.9
        prompt = """Pretend to be an expert teacher, tasked with creating a SINGLE question task based on the facts given to you. You are to create a 'focused listing' question, that creates a question in this format : 
'list all the possible causes of the Civil War' ‘List all the primary components of the human circulatory system.’
‘List all the works written by William Shakespeare.’
‘List all the planets in our solar system in order of their distance from the sun’.


TASK : [{have the focused listing task be in here}] 

INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover :
"""
        slide = gpt_agent.open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    
    # 'F4' is the 'activity_module_4_focused_listing'
    def stage_4_F4_combined_process(self, lesson_facts) : 
        slide = self.stage_4_F4_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "activity_module_4_focused_listing",
            "slide": {
                "task" : splitted_slide
            }
        }
        return structured_output
        
  
################ MODULE EXTRACTION CODE ###################:

    #Extracts the module from a powerpoint slide, outputs the correct prompt
    def stage_5_extract_module(self, powerpoint_line):
        pattern = r'Module.*?:\s*(.+?)\s*-'
        powerpointModule = re.search(pattern, powerpoint_line)
        if powerpointModule:
            return powerpointModule.group(1)
        else: 
            print("ERROR in module extraction, make sure the module output syntax is correct.")

    def stage_5_module_powerpoint_slide_function_calls(self, module, powerpointSlideOutline, slideNumber, lessonFacts, lessonDescription, powerpointPlan):
            powerpointCalls = PowerpointCreatorV4()
            print(lessonFacts)
            print("THE SLIDE PLAN IS : " + powerpointSlideOutline[slideNumber])
            powerpoint_facts = self.stage_4_facts_extraction_from_choices(powerpointSlideOutline[slideNumber], lessonFacts)
            print("HERE ARE THE FACTS FOR THE CURRENT POWERPOINT : " + powerpoint_facts)
            print("""
                  These are the facts for the current powerpoint : 
                  """ + powerpoint_facts)
            if re.search("Title Page", module):
                print("Title page function calling...")
                titlePage = powerpointCalls.stage_4_C_combined_process(lessonFacts)
                return titlePage
            elif re.search("L\.O page", module):
                print("L.O page function calling...")
                loPage = powerpointCalls.stage_4_B_combined_process(lessonFacts)
                return loPage
            elif re.search("General content page", module):
                print("General content page function calling...")
                generalContentPage = powerpointCalls.stage_4_A_combined_process(slideNumber, powerpointSlideOutline, lessonDescription, powerpointPlan, lessonFacts)
                return generalContentPage
            elif re.search("Ending slide", module):
                print("Final slide function calling...")
                finalSlide = powerpointCalls.stage_4_D_combine_process(lessonFacts)
                return finalSlide
            elif re.search("question_module_1_mcq", module):
                print("Need to do this part")
                return None
            elif re.search("question_module_2_bullet_questions", module):
                print("question_module_2_bullet_questions calling...")
                question_slide = self.stage_4_E2_combine_process(powerpoint_facts)
                return question_slide
            elif re.search("question_module_3_roleplay_questions", module):
                print("question_module_3_roleplay_questions calling...")
                question_slide = self.stage_4_E3_combine_process(powerpoint_facts)
                return question_slide
            elif re.search("activity_module_1_brainstorming", module):
                print("activity_module_1_brainstorming calling...")
                activity_slide = self.stage_4_F1_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_2_student_summarisation", module):
                print("activity_module_2_student_summarisation calling...")
                activity_slide = self.stage_4_F2_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_3_qa_pairs", module):
                print("activity_module_3_qa_pairs calling...")
                activity_slide = self.stage_4_F3_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_4_focused_listing", module):
                print("activity_module_4_focused_listing calling... ")
                activity_slide = self.stage_4_F4_combined_process(powerpoint_facts)
                return activity_slide

            
            print("Error : no module found.")

                

    def stage_6_create_powerpoint(self, lessonFacts) : 
        poweropointMethods = PowerpointCreatorV4()
        powerpointSlidesDetailed = []
        print("FIXED STAGES IN PROGRESS...")
        factGroupings = self.stage_1_groupings_for_facts(lessonFacts)
        print(factGroupings)
        print("STAGE 1 COMPLETE")
        powerpointPlan = self.stage_2_powerpoint_plan(lessonFacts, factGroupings)
        print(powerpointPlan)
        print("STAGE 2 COMPLETE")
        new_powerpoint_plan = self.stage_2_1_powerpoint_plan(powerpointPlan, lessonFacts)
        print(new_powerpoint_plan)
        print("STAGE 2.1 COMPLETE")
        final_powerpoint_plan = self.stage_2_2_submodule_choice_insertion(new_powerpoint_plan, lessonFacts)
        print(final_powerpoint_plan)


        print("STAGE 2.2 COMPLETE")
        lessonDescription = self.stage_3_lesson_description(lessonFacts)
        print("STAGE 3.1 COMPLETE")
        powerpointSlideOutlines = self.stage_3_facts_for_slide_powerpoint_extractor(final_powerpoint_plan)
        print("STAGE 3.2 COMPLETE")
        print("LOOPING STAGES IN PROGRESS...")
        for i in range(len(powerpointSlideOutlines)):
            slideNumber = i 
            print(f"CURRENT SLIDE IS {slideNumber}")
            print(powerpointSlideOutlines[i])
            module = poweropointMethods.stage_5_extract_module(powerpointSlideOutlines[i]) # Extracts module from powerpoint plan

            powerpointSlide = poweropointMethods.stage_5_module_powerpoint_slide_function_calls(module, powerpointSlideOutlines[i], slideNumber, lessonFacts, lessonDescription, final_powerpoint_plan) # Calls function that creates powerpoint based on module name.
            print("POWERPOINT SLIDE CREATED, APPENDING...")

            powerpointSlidesDetailed.append(powerpointSlide) 

            print("POWERPOINT SLIDE APPENDED TO ARRAY")
        print("FULL POWERPOINT CREATED!")
       
        return powerpointSlidesDetailed #Returns an array, where at [i] it is the powerpoint detailed content, and the name of the module/number that that slide is
    

############### TESTING CODE ###################
            

            

 


facts =  """1. {Auditory parts of working memory are located in the left frontal and parietal lobes.} 2. {The visual sketchpad is located in the right hemisphere of the brain.} 3. {Working memory may have co-evolved with speech.} 4. {Long-term memory is divided into different systems located in different brain networks.} 5. {Information enters sensory systems and then passes through specialized processing networks.} 6. {There are areas in the cortex that extract perceptual representations of objects.} 7. {Semantic memory stores factual knowledge organized into categories.} 8. {The brain organizes encoded information into categories for efficient memory retrieval.} 9. {Skills and emotional learning are types of long-term memory.} 10. {Different brain areas are involved in skill learning and emotional learning.} 11. {Episodic memory is used to remember personal experiences.} 12. {Episodic memory is different from learning facts because events happen only once.} 13. {Amnesic patients have deficits in episodic memory.} 14. {Damage to specific brain regions affects the formation of episodic and semantic memories.} 15. {The perirhinal cortex mediates the sense of familiarity in episodic memory.} 16. {The hippocampus encodes events and places in episodic memory.} 17. {Certain types of semantic dementia can cause breakdown of semantic memory.} 18. {Neuroscientists study neurological patients and conduct research using laboratory animals to understand the neurobiology of memory.}
 """

# groupings = test.stage_1_groupings_for_facts(facts)
# print(groupings)
# powerpointPlan = test.stage_2_powerpoint_plan(facts, groupings)
# print(powerpointPlan)

# lessonDescription = test.stage_3_lesson_description(facts)
# print(lessonDescription)
lessonDescriptionTesting = """The lesson outlines the different types of planes in Hearts of Iron IV, their specific roles and capabilities, and the strategic importance of these planes in different geographical contexts and stages of the game."""



powerpointPlanTesting = """POWERPOINT 1 : Module : Title Page - Memory Processes in the Brain, An Overview of Memory Systems and its Functions

POWERPOINT 2 : Module : L.O page - Learning objects for the lesson 

POWERPOINT 3 : Module : General content page - {1, 2, 3}, Working memory and its evolution

POWERPOINT 4 : Module : question_module_2_bullet_questions - {1, 2, 3}

POWERPOINT 5 : Module : General content page - {5, 6, 8}, Process and organization of sensory information

POWERPOINT 6 : Module : question_module_3_roleplay_questions - {5, 6, 8}

POWERPOINT 7 : Module : General content page - {4, 9, 10}, Systems and types of long-term memory

POWERPOINT 8 : Module : activity_module_1_brainstroming - {1, 2, 3, 5, 6, 8, 4, 9, 10}

POWERPOINT 9 : Module : General content page - {7, 17}, Semantic memory and its vulnerabilities

POWERPOINT 10 : Module : question_module_2_bullet_questions - {7, 17}

POWERPOINT 11 : Module : General content page - {11, 12, 13, 14, 15, 16}, Episodic memory and its associated brain regions

POWERPOINT 12 : Module : question_module_3_roleplay_questions - {11, 12, 13, 14, 15, 16}

POWERPOINT 13 : Module : General content page - {18}, Research methods in memory neuroscience

POWERPOINT 14 : Module : activity_module_2_student_summarisation - {7, 17, 11, 12, 13, 14, 15, 16, 18}"""

powerpointSlideTest = """TITLE : Understanding the Role of Tactical and Strategic Bombers in Hearts of Iron IV

CONTENT : 

By the end of this presentation, you should be able to:

1. Comprehend the primary uses of tactical bombers in the game, positioned between close attack support and strategic bombers.
2. Identify the different operations that tactical bombers can perform including Close Air Support, Port Strikes, and Strategic bombing.
3. Understand the limitations and advantages of tactical bombers in terms of their range and targeting capabilities.
4. Gain insight into strategic bombers' fundamental role in the destruction of the enemy's industrial base and infrastructure.
5. Understand the characteristics of strategic bombers, notably their long range and high survivability.
# 6. Differentiate between tactical and strategic bombers based on their respective tasks and capabilities."""

test = PowerpointCreatorV4()


# powerpoint_slides_outline = test.stage_3_facts_for_slide_powerpoint_extractor(powerpointPlanTesting)
# powerpoint_facts = test.stage_4_facts_extraction_from_choices(powerpoint_slides_outline[12], facts)
# print (powerpoint_slides_outline[12])
# print("""THESE ARE THE POWERPOINT FACTS : 
      
      
# # """ + powerpoint_facts)

# for i in range(len(powerpoint_slides_outline)):
#     print("In loop, iteration:", i)
#     print(powerpoint_slides_outline[i])



short_facts = """1. {Auditory parts of working memory are located in the left frontal and parietal lobes.} 2. {The visual sketchpad is located in the right hemisphere of the brain.} 3. {Working memory may have co-evolved with speech.}"""
powerpointTest = test.stage_6_create_powerpoint(short_facts)
print(powerpointTest)
# for i, slide_module_dict in enumerate(powerpointTest[:10]):  # Prints the first 10 items
#     print(f"SlideModulePair #{i+1}:")
#     print(f"  Module: {slide_module_dict['module']}")
#     print(f"  Slide: {slide_module_dict['slide']}")
#     print()


