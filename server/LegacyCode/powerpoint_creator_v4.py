from openai_calls import OpenAI
import re


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
        stage1Prompt = """Group these facts into logically consistent chunks to be used for a SINGLE  powerpoint slide - DO NOT make the facts be too long. ONLY output the numbers of the facts, and put them in curly brackets e.g {1, 5, 6} or {7, 13, 2}, and then, in your mind, INTERNALLY justify WHY you chose them.
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
    def stage_3_lesson_description(self, numberedFacts) : 
        gptAgent = OpenAI()
        stage3Temp = 0.49
        stage3Prompt = """These facts are included for a lesson. Summarise these facts into one,  brief line, outlining the lesson."""
        lessonDescription = gptAgent.open_ai_gpt4_call(numberedFacts, stage3Prompt, stage3Temp)
        return lessonDescription
    def stage_3_facts_for_slide_powerpoint_extractor(self, powerpointPlan) : 
        powerpointSlides = re.findall(r'(POWERPOINT \d+ : .+)', powerpointPlan)
        return powerpointSlides


#############     MODULE GENERIC CODE:        ###############
    # Looping stages 
    #Extracts the powerpoint individual slide plans, and the total amount of slides for the current powerpoint
    
    #Extracts the fact numbers from the optimum grouping of a single powerpoint slide 
    def stage_4_facts_extraction_from_choices(self, slideContent, factsString):
        # Use regex to extract the fact numbers from the slide content
        fact_numbers_match = re.search(r'\{(.+?)\}', slideContent)
        if fact_numbers_match is None:
            return ""

        fact_numbers = fact_numbers_match.group(1)
        fact_numbers = list(map(int, fact_numbers.split(',')))  # Convert to a list of integers

        # Create a list to store the facts for this slide
        slide_facts = []

        # Split the facts string into a list of facts
        factsList = factsString.splitlines()

        # Go through the list of facts and add the ones with matching numbers to slide_facts
        for fact in factsList:
            # Check if line starts with a number
            if fact.split(' ')[0].isdigit():
                number = int(fact.split(' ')[0])  # Extract the fact number from the fact string
                if number in fact_numbers:
                    slide_facts.append(fact)

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
            

################ MODULE EXTRACTION CODE ###################:

    #Extracts the module from a powerpoint slide, outputs the correct prompt
    def stage_5_extract_module(self, powerpoint_line):
        pattern = r'Module : (.+?) -'
        powerpointModule = re.search(pattern, powerpoint_line)
        if powerpointModule:
            return powerpointModule.group(1).strip() # Return the captured group, which is the module name
        else : 
            print("ERROR in module extraction, make sure the module output syntax is correct.")

    def stage_5_module_powerpoint_slide_function_calls(self, module, powerpointSlideOutline, slideNumber, lessonFacts, lessonDescription, powerpointPlan) : # Calls stage_4 functions for modules based on the name of the module, use 'swtich : case' for this
        powerpointCalls = PowerpointCreatorV4()
        match module : 
            case "Title Page" : 
                print("Title page function calling...")
                titlePage = powerpointCalls.stage_4_C_combined_process(lessonFacts)
                return titlePage
            case "L.O page" : 
                print("L.O page function calling...")
                loPage = powerpointCalls.stage_4_B_combined_process(lessonFacts)
                return loPage
            case "General content page" : 
                print("General content page function calling...")
                generalContentPage = powerpointCalls.stage_4_A_combined_process(slideNumber, powerpointSlideOutline, lessonDescription, powerpointPlan, lessonFacts)
                return generalContentPage
            case "Ending slide" : 
                print("Final slide function calling...")
                finalSlide = powerpointCalls.stage_4_D_combine_process(lessonFacts)
                return finalSlide
            
        print("Error : no module found.")

                

    def stage_6_create_powerpoint(self, lessonFacts) : 
        poweropointMethods = PowerpointCreatorV4()
        powerpointSlidesDetailed = []
        print("FIXED STAGES IN PROGRESS...")
        factGroupings = self.stage_1_groupings_for_facts(lessonFacts)
        print("STAGE 1 COMPLETE")
        powerpointPlan = self.stage_2_powerpoint_plan(lessonFacts, factGroupings)
        print("STAGE 2 COMPLETE")
        print(powerpointPlan)
        lessonDescription = self.stage_3_lesson_description(lessonFacts)
        print("STAGE 3.1 COMPLETE")
        powerpointSlideOutlines = self.stage_3_facts_for_slide_powerpoint_extractor(powerpointPlan)
        print("STAGE 3.2 COMPLETE")
        print("LOOPING STAGES IN PROGRESS...")
        for i in range(len(powerpointSlideOutlines)):
            slideNumber = i + 1 # +1 because powerpoint slides start at 1
            print(f"CURRENT SLIDE IS {slideNumber}")
            print(powerpointSlideOutlines[i])
            module = poweropointMethods.stage_5_extract_module(powerpointSlideOutlines[i]) # Extracts module from powerpoint plan

            powerpointSlide = poweropointMethods.stage_5_module_powerpoint_slide_function_calls(module, powerpointSlideOutlines[i], slideNumber, lessonFacts, lessonDescription, powerpointPlan) # Calls function that creates powerpoint based on module name.
            print("POWERPOINT SLIDE CREATED, APPENDING...")

            powerpointSlidesDetailed.append(powerpointSlide) 

            print("POWERPOINT SLIDE APPENDED TO ARRAY")
        print("FULL POWERPOINT CREATED!")
       
        return powerpointSlidesDetailed #Returns an array, where at [i] it is the powerpoint detailed content, and the name of the module/number that that slide is
    

############### TESTING CODE ###################
            

            

 

facts =  """1. {Brain imaging has helped identify the brain areas involved in distinct components of reading and learning tasks.} 2. {New mathematical techniques are being developed to study how different brain regions interact during complex tasks.} 3. {The BOLD signal is a reliable index of synaptic processing within a brain region.} 4. {Building brain-like machines requires understanding how real brains operate efficiently and economically.} 5. {Real brains are highly adaptable and can tolerate things going wrong.} 6. {Real brains consist of highly interconnected neuronal networks.} 7. {The challenge is to discover how real brains operate efficiently and use similar principles to build brain-like machines.} 8. {The energy cost of signaling in the brain is a major factor in the evolution of brains.} 9. {The speed of nerve impulses in biological brains is much slower than digital computers.} 10. {Biological brains are constructed as highly parallel networks, unlike silicon-based systems.} 11. {Neurally-inspired engineers use analogue coding in silicon circuits to reduce power consumption and increase speed.} 12. {Efficient coding and sparse coding are important design principles for building artificial neural networks.} 13. {Artificial neural networks can operate in the real world, in real time, and use very little power.} 14. {Artificial neural networks are often used to study learning and memory.}
 """

# groupings = test.stage_1_groupings_for_facts(facts)
# print(groupings)
# powerpointPlan = test.stage_2_powerpoint_plan(facts, groupings)
# print(powerpointPlan)

# lessonDescription = test.stage_3_lesson_description(facts)
# print(lessonDescription)
lessonDescriptionTesting = """The lesson outlines the different types of planes in Hearts of Iron IV, their specific roles and capabilities, and the strategic importance of these planes in different geographical contexts and stages of the game."""



powerpointPlanTesting = """POWERPOINT 1 : Module : Title Page - Hearts of Iron IV, An Insight on Aircraft and their Functionalities

POWERPOINT 2 : Module : L.O page - Learning objects for the lesson

POWERPOINT 3 : Module : General content page - {1, 2, 3, 17}, Understanding basics of Hearts of Iron IV

POWERPOINT 4 : Module : General content page - {18, 19, 20, 21}, Importance and specialties of Naval Bombers

POWERPOINT 5 : Module : General content page - {4, 5, 6, 7}, Types of fighters and their strengths

POWERPOINT 6 : Module : General content page - {8, 9, 10, 11}, Role and capabilities of CAS planes

POWERPOINT 7 : Module : General content page - {12, 13, 14}, Tactical bombers and their functionalities

POWERPOINT 8 : Module : General content page - {15, 16}, Strategic bombers and their impact   

POWERPOINT 9 : Module : Ending slide - Conclusion, Summary of the different types of aircraft in Hearts of Iron IV, their roles, and their impacts.
"""

powerpointSlideTest = """TITLE : Understanding the Role of Tactical and Strategic Bombers in Hearts of Iron IV

CONTENT : 

By the end of this presentation, you should be able to:

1. Comprehend the primary uses of tactical bombers in the game, positioned between close attack support and strategic bombers.
2. Identify the different operations that tactical bombers can perform including Close Air Support, Port Strikes, and Strategic bombing.
3. Understand the limitations and advantages of tactical bombers in terms of their range and targeting capabilities.
4. Gain insight into strategic bombers' fundamental role in the destruction of the enemy's industrial base and infrastructure.
5. Understand the characteristics of strategic bombers, notably their long range and high survivability.
# 6. Differentiate between tactical and strategic bombers based on their respective tasks and capabilities."""


# powerpointSlide, searchQuery = test.stage_4_A_combined_process(4, powerpointSlideOutlines, lessonDescriptionTesting, powerpointPlanTesting, facts)
# if powerpointSlide is not None:
#     print("THIS IS THE TITLE : " + powerpointSlide[0] + "THIS IS THE CONTENT : " + powerpointSlide[1] + "THIS IS THE SEARCH QUERY" + searchQuery)
# else:
#     print("powerpointSlide is None")

# slides = test.stage_3_facts_for_slide_powerpoint_extractor(powerpointPlanTesting)
# slideFacts = test.stage_4_facts_extraction_from_choices(slides[5], facts) # Gets slide facts
# print(slideFacts)
# slideNumber = 7
# module = test.stage_5_extract_module(powerpointSlideOutlines[slideNumber])
# print(module)
# powerpointContent = test.stage_5_module_powerpoint_slide_function_calls(module, powerpointSlideOutlines, slideNumber, facts,lessonDescriptionTesting,powerpointPlanTesting)

# print(powerpointContent)
# powerpointSlideOutlines = test.stage_3_facts_for_slide_powerpoint_extractor(powerpointPlanTesting)
# print(powerpointSlideOutlines[1])
# test = PowerpointCreatorV4()
# powerpointTest = test.stage_6_create_powerpoint(facts)
# print(powerpointTest)
# for i, slide_module_dict in enumerate(powerpointTest[:10]):  # Prints the first 10 items
#     print(f"SlideModulePair #{i+1}:")
#     print(f"  Module: {slide_module_dict['module']}")
#     print(f"  Slide: {slide_module_dict['slide']}")
#     print()


