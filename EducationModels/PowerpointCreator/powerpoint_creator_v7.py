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
            if re.search("title_page", module):
                titlePage = await powerpointCalls.stage_4_C_combined_process(lessonFacts)
                return titlePage
            elif re.search("lo_page", module):
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
            elif re.search("ending_slide", module):
                finalSlide = await powerpointCalls.stage_4_D_combine_process(lessonFacts)
                return finalSlide
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
            

    