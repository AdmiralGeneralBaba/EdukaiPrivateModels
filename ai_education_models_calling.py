from EducationModels.aqa_english_language_paper_1 import aqa_english_language_paper_1_generator
from EducationModels.flashcard_model_v1 import FlashcardModelV1
from EducationModels.smart_gpt_v1 import SmartGPTV1
from EducationModels.tutor_ai_v1 import TutorAIV1
from EducationModels.yearly_plan_ai_models_v1 import YearlyPlanCreatorV1



class EducationModels : 
    # AQAEnglishLanguagePaper1 = aqa_english_language_paper_1_generator(path ,0, 'Meeting Minutes', 'Debrief') # Assuming that paper_1_generator is a class
    flashcardModel = FlashcardModelV1()
    smartGpt = SmartGPTV1()
    tutorAi = TutorAIV1()
    yearlyPlanCreator = YearlyPlanCreatorV1()



#Here are the inputs for all of the AI models : 
#AQA paper : 
# def aqa_english_language_paper_1_generator(self, pdfFile, ques1Choice, titleOfBook, bookType)


# Flashcard Model: 
# def flashcard_intialise(self textbook_path):


# Info Extractor: 
# def info_extractor(self, textbook_path): 


# SmartGPT:
# def smart_gpt(self, user_input): 


# YearlyPlanAI models :
# def yearly_plan_powerpoint_creator(self, lessonPlanFacts) : 

# def yearly_plan_homework_creator(self, lessons, schoolType) :

# def yearly_plan_final(self, lessonNumber, path) : 
    