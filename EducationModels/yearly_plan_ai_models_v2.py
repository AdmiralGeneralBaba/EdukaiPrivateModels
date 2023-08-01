from openai_calls import OpenAI 
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier
import re
from homework_creator_v1 import homeworkCreatorV1
class YearlyPlanCreatorV2() : 

    def yearly_plan_facts_per_lesson_pdf_input(pdf_path, chunkSize, lessonSize): 
        infoExtract = InfoExtractorV1() #Creates the infoExtractor 
        rawFacts = infoExtract.info_extractorV2(pdf_path, chunkSize) # Calls info extractor
    
        # Initialize variables
        lessons = []
        current_lesson = ""
         # Char limit for each of the lesson's raw facts CANNOT go over 

        # Split the raw facts into separ44ate strings
        rawFactsSplit = [] 
        for fact in rawFacts:
            rawFactsSplit.extend(re.split('\n-|\n', fact)) # Splits up gpt-3.5's message into raw facts

        # Loop through raw facts
        for rawFact in rawFactsSplit:
            # If adding the next fact doesn't exceed the char_limit, add the fact to the current lesson
            if len(current_lesson + rawFact) <= lessonSize:
                current_lesson += rawFact
            # If it does, append the current lesson to lessons and start a new lesson
            else:
                lessons.append(current_lesson)
                current_lesson = rawFact

        # Append the last lesson if it's non-empty
        if current_lesson:
            lessons.append(current_lesson)

        return lessons
  
    def lesson_descriptor(self, lesson) :
        gpt_agent = OpenAI()
        gpt_temp = 0.8
        lesson_description_prompt = """ You are a perfect describer based on facts inputted, and can describe the content of facts given as perfectly and briefly as possible. This is one lesson in many, and these are facts from a section of a textbook. You are to briefly, in one line, describe what these facts describe, assuming they are the content of a single lesson (e.g is it an introduction, a delve deeper into a certain topic etc)
Here are some example outputs : 

This lesson is an exhaustive introduction to the complexities of neurology, with a key focus on the functions of different brain regions.
This lesson provides an essential foundation for novices in the field of astronomy, emphasizing the understanding of celestial bodies and their movements.
This lesson is about the art of cinematography and the principles of visual storytelling, with a particular concentration on mastering the use of different camera angles and movements.
This lesson is a detailed guide to understanding the dynamics of international politics, with a significant emphasis on the causes and consequences of global conflicts.
This lesson provides a basic understanding for beginners in the field of architecture, focusing on the importance of structural design and sustainability in modern building practices.
This lesson is about the world of digital art and animation, with a focus on mastering the techniques of 3D modeling and character design.
This lesson is an in-depth exploration of the evolution of music, from classical symphonies to contemporary pop culture, with a focus on understanding the influence of societal changes on musical styles.
This lesson provides a foundation for beginners in the field of environmental science, emphasizing the impact of human activity on climate change and the importance of sustainable practices.
This lesson is about the realm of speculative fiction, with a particular focus on developing engaging plotlines and immersive world-building in fantasy and science fiction genres.

Here are the lesson facts : 
"""
        lesson_description = gpt_agent.open_ai_gpt_call(lesson, lesson_description_prompt, gpt_temp)
        return lesson_description
    def yearly_plan_addon_lesson_descriptions(self, lessons):
        lesson_list = []
        info_extraction = InfoExtractorV1()
        for lesson in lessons:
            lesson_renumbered = info_extraction.renumber_points(lesson)
            lesson_description = self.lesson_descriptor(lesson_renumbered)
            lesson_dict = {
                'description': lesson_description,
                'facts': lesson_renumbered 
            }
            lesson_list.append(lesson_dict)
        return lesson_list  
    
    def yearly_plan_homework_creator_templates_versions(self, lessons):
        homeworkContent = []
        homework_creator = homeworkCreatorV1()
        
        for i in range(len(lessons)):
            homeworkTemplate = int(input("Enter the homework template number (0 or 1): "))
            
            if homeworkTemplate == 0:
                homeworkPrompt = homework_creator.homework_creator_template_one(lessons[i])
            elif homeworkTemplate == 1:
                homeworkPrompt = homework_creator.homework_creator_template_two(lessons[i]) # Need to create a second template.
            else:
                raise ValueError(f"Invalid homeworkTemplate value: {homeworkTemplate}")

            gptAgent = OpenAI()
            homeworkContent.append(gptAgent.open_ai_gpt_call(lessons[i], homeworkPrompt))
        
        return homeworkContent

#######################         TESTING CODE           ########################### : 
path = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\HoI_IV_Strategy_Guide.pdf"
schoolType = "High School"
lessons = YearlyPlanCreatorV2.yearly_plan_facts_per_lesson(path, 1000, 1500)
# homework = YearlyPlanCreatorV2.homework_creator_template_one(lessons[4], 1)

# Loop through each lesson and print it out with its number and length
for i, lesson in enumerate(lessons, start=1):
    print(f"Lesson {i} ({len(lesson)} characters):\n{lesson}\n")
# print(lessons)


# print(homework)3