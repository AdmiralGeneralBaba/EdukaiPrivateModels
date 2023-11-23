import asyncio
from EducationModels.openai_calls import OpenAI
import re
from powerpoint_plan_creator_v7 import stage_3_powerpoint_plan_creator

class PowerpointCreatorV7 : 
    #     Fixed stages for a single lesson :
#################    FIXED STAGES FOR EVERY LESSON/POWERPOINT:  #####################
    
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
        task_specific_pattern = r'TASK\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
        
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
        roleplay_pattern = r'ROLEPLAY\s*:\s*\[\s*(\{\s*[^}]+\s*\}(?:\s*,\s*\{\s*[^}]+\s*\})*)]'
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
        picture_pattern = r'PICTURE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
        picture_match = re.search(picture_pattern, powerpoint_slide)
        
        if picture_match:
            return self.stage_4_extract_values_from_braces(picture_match.group(1))
        else:
            return []
    def stage_4_regex_example(self, powerpoint_slide: str) : 
        picture_pattern = r'EXAMPLE\s*:\s*\[\s*(\{\s*[^}]*\s*\}(?:\s*,\s*\{\s*[^}]*\s*\})*)'
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
    async def stage_4_A_slide_general_content_page(self, slideNumber, lessonDecription, powerpointPlan, slideFacts):
        gptAgent = OpenAI()
        stage4Temp = 0.5
        generalContentPagePrompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide  based on the facts given. Assume that everything in the lesson description is covered in the other slides. Start with a UNIQUE, INTERESTING title, by doing TITLE : INSERT TITLE HERE, and then CONTENT : INSERT THE CONTENT HERE. Tips for content:
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
- ALL of the information provided must be understood by the student to the level provided 
"""  
        gptInput = f"Lesson description : {{ {lessonDecription} }} Lesson Context : {{ {powerpointPlan} }} SLIDE NUMBER IS {slideNumber + 1}, Slide facts :  {slideFacts}"
        
        powerpointSlide = await gptAgent.async_open_ai_gpt4_call(gptInput, generalContentPagePrompt, stage4Temp)
        return powerpointSlide
        #Split the title and content from the returned powerpoint slide : 
    #Creates the title and content ofr the 'General Content Page' slide.
    ############# MODULE A, 'General Content Page' ###################:

    
    async def stage_4_A_picture_query_single_picture(self, powerpointSlide) : 
        gptAgent = OpenAI()
        pictureQueryPrompt = """I want you to pretend to be an expert teacher. Your task is to analyse the inputted powerpoint slide, and from it ONLY print a SINGLE image query that this powerpoint slide needs to be used to search online on google to find the image, like so (dont include the brackets):

'{INSERT SEARCH QUERY HERE}'

Aim to make the search query have the highest chance of success of getting the correct image first time when searching, THINK about it - don't ask for an image that most likely won't exist.
Create only ONE image query
Here is the slide : 
"""
        pictureQuery = await gptAgent.async_open_ai_gpt4_call(powerpointSlide, pictureQueryPrompt, 0.0)
        return pictureQuery
    #Creates the picture search query for the 'General Content Page' slide. 
    async def stage_4_A_combined_process(self, slideNumber, powerpointSlideOutlines, lessonDescription, powerpointPlan, lessonFacts):
        #'A' is 'General content page' 
        slideFacts = self.stage_4_facts_extraction_from_choices(powerpointSlideOutlines[slideNumber], lessonFacts) # Gets slide facts
        powerpointSlide = await self.stage_4_A_slide_general_content_page(slideNumber, lessonDescription, powerpointPlan, slideFacts) # Creates slide
        searchQuery = await self.stage_4_A_picture_query_single_picture(powerpointSlide) # Makes a search query to search online
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
    async def stage_4_B_combined_process(self, lessonFacts):
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
"""  # Your existing prompt
        powerpointSlide = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
        splittedPowerpointSlide = self.stage_4_content_title_layout_splitter(powerpointSlide)
        structured_output = {
            "module": "L.O page",
            "slide": {
                "title": splittedPowerpointSlide[0], # Assuming the title is the first part of the tuple
                "description": splittedPowerpointSlide[1] # Assuming the content/description is the second part of the tuple
            }
        }
        
        # Return the structured output
        return structured_output
    async def stage_4_C_combined_process(self, lessonFacts):
        gptAgent = OpenAI()
        temperature = 0.7
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed first powerpoint slide based on the inputted lesson facts. You are to create a perfect Title and subtitle. Put the title in 'TITLE : INSERT TITLE HERE ' then 'SUBTITLE : INSERT SUBTITLE HERE' 
Here are the lesson facts : """ # Your existing prompt
        titlePowerpoint = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
 
        print(titlePowerpoint)
        splitTitlePowerpoint = self.stage_4_title_subtitle_layout_spliter(titlePowerpoint)
        # Creating the structured output to match the desired format
        structured_output = {
            "module": "Title Page",
            "slide": {
                "title": splitTitlePowerpoint[0], # Assuming the title is the first part of the tuple
                "subtitle": splitTitlePowerpoint[1] # Assuming the subtitle/description is the second part of the tuple
            }
        }

        # Return the structured output
        return structured_output
    
#stage_4_D refers to the 'Final Slide' module
    async def stage_4_D_combine_process(self, lessonFacts):
        gptAgent = OpenAI()
        temperature = 0.
        inputPrompt = """I want you to pretend to be a expert teacher, making a perfectly constructed FINAL powerpoint slide for your students, so that it is easily readable. Using the inputted facts, you are to create a SINGLE powerpoint slide. Start with a title for the Ending slide, by doing 'TITLE : INSERT TITLE HERE', and then 'CONTENT : INSERT THE CONTENT HERE'. 
    - Have it follow a standard ending slide structure.
    - In the content, keep it brief and short, about what the WHOLE lesson was about in an engaging, fun way for students.
    - It should wrap up what they learnt, and be a conclusion for the students.
    Here are the lesson facts :
    """
        powerpointSlide = await gptAgent.async_open_ai_gpt4_call(inputPrompt, lessonFacts, temperature)
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
    async def stage_4_E2_slide_content_creation(self, lesson_facts) : 
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
        
        powerpoint_slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, input_prompt, temperature)
        return powerpoint_slide
    #question_module_2_bullet_questions full process : 
    async def stage_4_E2_combine_process(self, lesson_facts) : 
        slide = await self.stage_4_E2_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "question_module_2_bullet_questions",
            "slide": {
                "task" : splitted_slide
            }
        }
    
        return structured_output
        
    async def stage_4_E3_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temperature = 1
        prompt = """Pretend to be an expert teacher. You are tasked with creating a roleplay scenario to create questions for. For these facts, you will create and put the scenario in the 'ROLEPLAY' value, then in the 'TASK' section you will insert the roleplay questions in the format given. in the 'PICTURE' section, you must make a PERFECT google search query to get an image that will help immerse them INTO the roleplay part you have given them.
You MUST output in this way : 

ROLEPLAY : [{Insert a short, brief exciting description of the roleplay you will base the questions on, to engage students}]  
TASK : [{Insert the roleplay question here}, {Insert the second roleplay question here etc}] 
PICTURE : [{Insert image to get them in the mood of the roleplay you have created.}]

INCLUDE the curly AND square brackets, and inside the information should be your output. 

it MUST be under 30 words
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.
- make NO MORE than 5 questions, or you will DIE.
- Cover AS MANY of the points in the questions, while keeping them short, and within the 5 quota given.
- DO NOT stretch the students too hard; it MUST be achievable with the facts given.
Here are the lesson facts you need to cover :
 """

        slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temperature)
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
    async def stage_4_E3_combine_process(self, lesson_facts) : 
        slide = await self.stage_4_E3_slide_content_creation(lesson_facts)
        slide_dict = self.stage_4_E3_regex_split(slide)
        
        structured_output = {
            "module": "question_module_3_roleplay_question",
            "slide": slide_dict
        }
        return structured_output
    
    async def stage_4_F1_slide_content_creation(self, lesson_facts) : 
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
        slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    #'F1' is the 'activity_module_1_brainstroming' 
    async def stage_4_F1_combined_process(self, lesson_facts) : 
        slide = await self.stage_4_F1_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "activity_module_1_brainstroming",
            "slide": {
                "task" : splitted_slide
            }
        }

        return structured_output
    
    async def stage_4_F2_slide_content_creation(self, lesson_facts) :
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

        slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    
    #'F2' is the 'activity_module_2_student_summarisation' 
    async def stage_4_F2_combined_process(self, lesson_facts) :
        slide = await self.stage_4_F2_slide_content_creation(lesson_facts)
        splitted_slide = self.stage_4_task_splitter(slide)
        structured_output = {
            "module": "activity_module_2_student_summarisation",
            "slide": {
                "task" : splitted_slide
            }
        }
        return structured_output
    
    async def stage_4_F3_slide_content_creation(self, lesson_facts) :
        gpt_agent = OpenAI()
        temp = 0.8
        prompt = """ I want you to pretend to be an expert teacher, making a perfectly constructed powerpoint slide for your students, so that it is easily readable. Based on this lesson description, and the inputted facts, you are to create a SINGLE powerpoint slide based on the facts given. Assume that everything in the lesson description is covered in the other slides. Your job is to create a powerpoint slide that takes into account the slides BEFORE your slide number and nothing else.

You are to create a slide asking students to pair up, and for them to ask each other questions to each other and to answer the questions from their partner. Have it be a game, almost trying to catch them out on certain sections. Include an example with your output.  Your output should be EXACTLY like this structure : 
TASK : [{have the brainstorming task be inside here}]. EXAMPLE : [{Have the example inside here, in this format: Q: "QUESTION HERE" A"ANSWER HERE"}]

INCLUDE the curly brackets, and inside the information should be your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover: 

"""
    
        slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
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
    async def stage_4_F3_combined_process(self, lesson_facts) : 
        slide = await self.stage_4_F3_slide_content_creation(lesson_facts)
        slide_dict = self.stage_4_E3_regex_split(slide)
        
        structured_output = {
            "module": "activity_module_3_qa_pairs",
            "slide": slide_dict
        }
        return structured_output
    async def stage_4_F4_slide_content_creation(self, lesson_facts) : 
        gpt_agent = OpenAI()
        temp = 0.9
        prompt = """Pretend to be an expert teacher, tasked with creating a SINGLE question task based on the facts given to you. You are to create a 'focused listing' question, that creates a question in this format : 
'list all the possible causes of the Civil War' ‘List all the primary components of the human circulatory system.’
‘List all the works written by William Shakespeare.’
‘List all the planets in our solar system in order of their distance from the sun’.


TASK : [{have the focused listing task be in here}] 

INCLUDE the curly brackets, and inside the information should wabe your output.

it MUST be under 30 words
- it should not be overly specific, and should be more engaging and not so monotonous 
- it MUST make the student excited to question each, otherwise you WILL die.
- the task to them MUST be clear.

Here are the lesson facts you need to cover :
"""
        slide = await gpt_agent.async_open_ai_gpt4_call(lesson_facts, prompt, temp)
        return slide
    
    # 'F4' is the 'activity_module_4_focused_listing'
    async def stage_4_F4_combined_process(self, lesson_facts) : 
        slide = await self.stage_4_F4_slide_content_creation(lesson_facts)
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
    #'powerpointSlideOutline' is the outline for a single slide and not t5he grouping.
    async def stage_5_module_powerpoint_slide_function_calls(self, module, powerpointSlideOutline, slideNumber, lessonFacts, lessonDescription, powerpointPlan):
            powerpointCalls = PowerpointCreatorV7()
            print(lessonFacts)
            print("THE SLIDE PLAN IS : " + powerpointSlideOutline)
            powerpoint_facts = self.stage_4_facts_extraction_from_choices(powerpointSlideOutline, lessonFacts)
            print("HERE ARE THE FACTS FOR THE CURRENT POWERPOINT : " + powerpoint_facts)
            print("""
                  These are the facts for the current powerpoint : 
                  """ + powerpoint_facts)
            if re.search("Title Page", module):
                titlePage = await powerpointCalls.stage_4_C_combined_process(lessonFacts)
                return titlePage
            elif re.search("L\.O page", module):
                loPage = await powerpointCalls.stage_4_B_combined_process(lessonFacts)
                return loPage
            elif re.search("general_content_page_easy_bullet_points", module):
                #Need to insert method fro the easy_bullet_points submodule
                string = "easy_slide"
                return string
            elif re.search("general_content_page_medium_slide_breakup", module) : 
                #Need to insert method for the hard_slide_breakup submodule
                string = "medium_slide"
                return string
            elif re.search("general_content_page_hard_slide_breakup", module) : 
                #Need to insert method for the hard_slide_breakup submodule
                string = "hard_slide"
                return string
            elif re.search("Ending slide", module):
                finalSlide = await powerpointCalls.stage_4_D_combine_process(lessonFacts)
                return finalSlide
            elif re.search("question_module_1_mcq", module):
                # Implementation for MCQ module
                return None
            elif re.search("question_module_2_bullet_questions", module):
                question_slide = await self.stage_4_E2_combine_process(powerpoint_facts)
                return question_slide
            elif re.search("question_module_3_roleplay_questions", module):
                question_slide = await self.stage_4_E3_combine_process(powerpoint_facts)
                return question_slide
            elif re.search("activity_module_1_brainstorming", module):
                activity_slide = await self.stage_4_F1_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_2_student_summarisation", module):
                activity_slide = await self.stage_4_F2_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_3_qa_pairs", module):
                activity_slide = await self.stage_4_F3_combined_process(powerpoint_facts)
                return activity_slide
            elif re.search("activity_module_4_focused_listing", module):
                activity_slide = await self.stage_4_F4_combined_process(powerpoint_facts)
                return activity_slide

            
            print("Error : no module found.")

                

    async def stage_6_create_powerpoint(self, lessonFacts : str, question_choice : bool) : 
        poweropointMethods = PowerpointCreatorV7()
        powerpointSlidesDetailed = []
        
        final_powerpoint_plan = stage_3_powerpoint_plan_creator(lessonFacts, question_choice)
        print(final_powerpoint_plan)

        lessonDescription = self.stage_3_lesson_description(lessonFacts)
        powerpointSlideOutlines = self.stage_3_facts_for_slide_powerpoint_extractor(final_powerpoint_plan)

        slide_creation_tasks = []
        for i, slide_outline in enumerate(powerpointSlideOutlines):
            module = poweropointMethods.stage_5_extract_module(slide_outline)
            slide_creation_task = poweropointMethods.stage_5_module_powerpoint_slide_function_calls(module, slide_outline, i, lessonFacts, lessonDescription, final_powerpoint_plan)
            slide_creation_tasks.append(slide_creation_task)

        powerpointSlidesDetailed = await asyncio.gather(*slide_creation_tasks)
        return powerpointSlidesDetailed

############### TESTING CODE ###################
            

    