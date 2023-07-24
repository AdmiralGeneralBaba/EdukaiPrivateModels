from openai_calls import OpenAI 
from info_extraction_v1 import InfoExtractorV1
import re


class YearlyPlanCreatorV1 : 
    def split_string(self, s):
        # split the string, but keep the delimiter
        parts = re.split("(#_!LESSON (\d)<@~)", s)[1:]
        
        # group parts in pairs (a pair is a delimiter and the part after it)
        parts = ["LESSON " + parts[i+1] + parts[i + 2] for i in range(0, len(parts), 3)]
        
        return parts
    def yearly_plan_facts_per_lesson(self, lessonNumber, path) : 
        chunkedFacts = []
        lessonPlansFacts = []
        lessonPlanFactsFinal = []
        gptAgent = OpenAI()
        InfoExtractor = InfoExtractorV1() # Creates a infoExtractor object
        rawTextbookFacts = InfoExtractor.info_extractor(path) # Extracts the raw facts from a PDF into a String array
        chunkedFacts = InfoExtractor.chunkerStringArray(rawTextbookFacts) #Splits a String array into chunks of less than 3000 characters

        lessonNumber = lessonNumber // len(chunkedFacts)

        factForLessonPrompt = f"""Based on these facts, I want you to section off them so that they are split up into {lessonNumber} lessons. 
                                Don't change the facts; put them into {lessonNumber} chunks, with starting before them their lesson number, 
                                and add these symbols before and after like so: #_!LESSON 1<@~, #_!LESSON 2<@~, and #_!LESSON 3<@~, up to lesson {lessonNumber} and have it be so that the information 
                                is grouped in the most logical way. Make sure that ALL facts are inside the lessons, such that there are none
                                left over. Do not change, or add anything about the facts; copy and paste them, into each respective lesson, from the
                                list you have been given. Here are the facts: """
        for i in range(len(chunkedFacts)) : 
            lessonPlansFacts.append(gptAgent.open_ai_gpt_call(chunkedFacts[i], factForLessonPrompt))
            lessonPlanFactsFinal = self.split_string(lessonPlansFacts[i])
        return lessonPlanFactsFinal      
    def yearly_plan_powerpoint_creator(self, lessonPlanFacts) :
        lessonPlans = []
        powerpointCreatorPrompt = """Make me a powerpoint plan based on the following raw facts for a lesson. I want it to be in a powerpoint slide, such that for each slide, you input 
                                        [SLIDE {i}], and then have a space, with the powerpoint plan afterwards, with all of the information to be included in the powerpoint. 
                                        Here is the information to make into a powerpoint lesson; remember to use ONLY the information here, to ensure accuracy: """
        gptAgent = OpenAI()
        for i in range(len(lessonPlanFacts)) : 
            lessonPlans.append(gptAgent.open_ai_gpt_call(lessonPlanFacts[i], powerpointCreatorPrompt))

        
        return lessonPlans
    def yearly_plan_homework_creator(self, lessons, schoolType) :
        homeworkContent = [] 
        homeworkPrompt = f"""Pretend you are a teacher for a {schoolType}. Based on the following powerpoint slides, create a homework plan for students to compelete.
                            Remember to only test based on the information provided: """
        gptAgent = OpenAI()
        for i in range(len(lessons)) : 
            homeworkContent.append(gptAgent.open_ai_gpt_call(lessons[i], homeworkPrompt))

        return homeworkContent
    def yearly_plan_final(self, lessonNumber, path) : 
        lessonPlanFacts = self.yearly_plan_facts_per_lesson(lessonNumber, path)
        finalLessonStructure = self.yearly_plan_powerpoint_creator(lessonPlanFacts)
        return finalLessonStructure
    

path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\HoI_IV_Strategy_Guide.pdf"
yearlyPlan = YearlyPlanCreatorV1()
facts = yearlyPlan.yearly_plan_facts_per_lesson(5, path)


print(facts)
