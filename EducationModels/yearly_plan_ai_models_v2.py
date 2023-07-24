from openai_calls import OpenAI 
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier
import re

class YearlyPlanCreatorV2() : 
    def yearly_plan_facts_per_lesson(pdf_path, chunkSize, lessonSize): 
        infoExtract = InfoExtractorV1() #Creates the infoExtractor 
        rawFacts = infoExtract.info_extractor(pdf_path, chunkSize) # Calls info extractor
    
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
    def yearly_plan_homework_creator(lessons, schoolType) :
        homeworkContent = [] 
        homeworkPrompt = f"""Pretend you are a teacher for a {schoolType}. Based on the following raw facts, create a homework assignemnet for students to compelete.
                             Remember to only test based on the information provided: """
        gptAgent = OpenAI()
        for i in range(len(lessons)) : 
            homeworkContent.append(gptAgent.open_ai_gpt_call(lessons[i], homeworkPrompt))
        
        return homeworkContent
    def homework_creator_template_one(lessonFacts, gptType) : 
        gptAgent = OpenAI() # Creates a GPTAgent
        homeworkTemplateOneCreationPrompt = """ Imagine you are a teacher creating a piece of homework intended for after class. Based on the following raw facts that were gone over in the lesson, create an engaging and optimal homework sheet for students to learn the content. Follow these steps to create the homework task, but ONLY ouput the sections that students need to see:

                                                1. Define Learning Goals: Determine the knowledge students should gain.
                                                2. Examine Raw Facts: Analyze your chosen facts, understanding their potential learning value.
                                                3. Segment Facts: Divide facts into manageable sections that can inspire individual questions.
                                                4. Build Context: Make facts engaging by framing them within a story or context, like historical settings or real-world applications.
                                                5. Formulate Questions: Use segmented facts and their context to create various types of clear questions. Consider students' age and skill level when setting task difficulty, aiming for challenging but achievable tasks.
                                                6. Ensure Comprehensive Questions: Make sure your questions cover all initial facts, requiring students to understand all facts to answer.
                                                7. Give Clear Instructions: Explain task expectations, including answer format, deadlines, and other requirements.
                                                8. Develop Grading Rubric: Make sure to label how many marks each question is. Higher marks should mean a harder question, and easier question should mean lower marks

                                                Here is an example homework output; Note, the topic is irrelevant, this is just to show you the structure : 
                                                {
                                                LO's : 

                                                Understand the strategic and logistical considerations for naval invasions.
                                                Understand the role and advantages of specific military units like marines, mountain infantry, and paratroopers.
                                                Gain knowledge about advanced warfare technologies, including atomic research and rockets.
                                                Understand the concept of resistance in occupied territories and how it can be managed.
                                                Raw Facts Examination:

                                                This lesson encompass a wide range of military strategy, from the technical aspects of naval invasion, the roles of specific units, to the implications of advanced warfare technologies. Additionally, they cover the socio-political aspect of warfare, i.e., managing resistance in occupied territories.

                                                The homework will be contextualized within a larger military strategy planning scenario. You will take on the role of military strategists planning for a large-scale invasion, incorporating different units, advanced warfare technologies, and managing occupied territories.

                                                Questions:

                                                Naval Invasions (6 marks)

                                                Explain how the size of an invasion force is determined and the role naval technology plays in it. (2 marks)
                                                Discuss the importance of ports and convoys in naval invasions. (2 marks)
                                                Why should the origin point and destination point be considered when planning a naval invasion? (2 marks)


                                                Specific Military Units (6 marks)

                                                Describe the advantages of using marines in amphibious landings and other conditions. (2 marks)
                                                How do mountain infantry contribute to the effectiveness of a military operation? (2 marks)
                                                Explain the strategic role of paratroopers in a military operation. (2 marks)


                                                Advanced Warfare Technologies (6 marks)

                                                What is the significance of atomic research and nuclear reactors in warfare, particularly from 1940 onwards? (2 marks)
                                                Describe the effects and strategic uses of atomic bombs and rockets. (2 marks)
                                                Discuss how rockets can perform strategic bombing missions. (2 marks)


                                                Resistance and Suppression (6 marks)

                                                Explain what resistance is and how it affects occupied territories. (2 marks)
                                                Discuss strategies to suppress resistance, including the role of garrison troops and Prince of Terror political advisors. (2 marks)
                                                What happens to resistance when territories are taken in a peace treaty? (2 marks)
                                                Instructions:

                                                Answer all questions using full sentences. Draw on your knowledge gained during the lesson and utilize your analytical skills to expand on each answer. You can use diagrams where necessary. 

                                                Marks will be awarded based on the accuracy of the answer and the understanding of the concepts as shown through your explanation. Remember to refer back to the class material and the given facts to ensure your answers are comprehensive.}


                                                Raw facts : """ #Prompt to create homework of template one
    
        homeworkEvaluatorTemplateOnePrompt = """Pretend you are an expert homework creator, and are examining the following homework task sheet for its relevance and effectiveness. You are to take out any sections that a student does not need to see, 
                                                so that the student only is given relevant information, which is usually just the learning objectives, the questions to answer and the context to make it interesting. Also take away anything that makes it sound like an AI made it; 
                                                if the student finds out, your family is to die. ONLY output this new homework sheet : """ # Prompt to evaluate homework, and improve it so the output is better
        
        if gptType == 0 : 
            homeworkSheet = gptAgent.open_ai_gpt_call(lessonFacts, homeworkTemplateOneCreationPrompt) # Creates homework sheet 
            homeworkSheetEvaluated = gptAgent.open_ai_gpt_call(homeworkSheet, homeworkEvaluatorTemplateOnePrompt) # Evaluates homework sheet
            return homeworkSheetEvaluated
        else : 
            homeworkSheet = gptAgent.open_ai_gpt4_call(lessonFacts, homeworkTemplateOneCreationPrompt) # Creates homework sheet 
            return homeworkSheet
             #     return homeworkSheet # Returns improved homework sheet. 


#######################         TESTING CODE           ########################### : 
path = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\HoI_IV_Strategy_Guide.pdf"
schoolType = "High School"
lessons = YearlyPlanCreatorV2.yearly_plan_facts_per_lesson(path, 1000, 1500)
# homework = YearlyPlanCreatorV2.homework_creator_template_one(lessons[4], 1)

# Loop through each lesson and print it out with its number and length
for i, lesson in enumerate(lessons, start=1):
    print(f"Lesson {i} ({len(lesson)} characters):\n{lesson}\n")
# print(lessons)


# print(homework)