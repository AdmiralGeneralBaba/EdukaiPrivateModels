import PyPDF2
import os
import openai
import re
import random


class AiOfficalModels :
    class OpenAI : 
        def __init__(self):
            openai.api_key = os.getenv('OPENAI_API_KEY') 
        def open_ai_gpt_call(self, user_content, prompt=None): 
            if isinstance(user_content, list):  # checks if user_content is a list
                messages = user_content
                if prompt:
                    messages.insert(0, {"role":"system", "content": prompt})
            else:
                messages = [{"role": "user", "content": user_content}]
                if prompt:
                    messages.insert(0, {"role":"system", "content": prompt})

            completion  = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            reply_content = completion.choices[0].message.content
            return reply_content  # Returning the reply_content from the function
        def open_ai_gpt4_call(self, user_content, prompt=None) : 
                messages = [{"role": "user", "content": user_content}]
                if prompt:
                    messages.insert(0, {"role":"system", "content": prompt})

                completion  = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                reply_content = completion.choices[0].message.content

                return reply_content  # Returning the reply_content from the function7

class GeneralAiModels : 
    class SmartGPTV1 : 
        chain_of_thought_prompt = " Answer : Let’s work this out in a step by step way to be sure we have the right answer"
        reflexion_prompt = "You are a researcher tasked with investigating the the 3 response options provided. List the flaws and faulty logic of each answer option. Let's work this out in a step by step way to be sure we have all the errors: "
        dera_prompt = " You are a resolver tasked with 1) finding which of the X answer options the researcher thought was best 2) improving that answer and 4) Printing the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer: "
        gptAgent = AiOfficalModels.OpenAI
        def chain_of_thought(self):
            combined_output = ""
            user_input = input(">: ")   # Asking for user outside the loop
            for i in range(3):
                reply_content = self.gptAgent.open_ai_gpt_call(user_input, "Question :" + self.chain_of_thought_prompt)  # Calling the function and getting the reply content
                combined_output += reply_content + "\n"  # Adding reply_content to combinedOutput

            return combined_output  # Printing combinedOutput after all iterations
        def reflexion_process(self): 
            return self.gptAgent.open_ai_gpt_call(self.chain_of_thought(), self.reflexion_prompt)
        def dera_process(self):
            return self.gptAgent.open_ai_gpt_call(self.reflexion_process(), self.dera_prompt)
        def smart_gpt(self): 
            return self.gptAgent.dera_process()
    class InfoExtractorV1 :        
        def __init__(self):
           self.gptAgent = AiOfficalModels.OpenAI()          
        def chunker(self, path) :
            pdfFileObj = open(path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)  # Use PdfReader instead of PdfFileReader
            num_pages = len(pdfReader.pages)  # Use len(pdfReader.pages) instead of pdfReader.numPages

            pages = len(pdfReader.pages)

            chunks = []
            current_chunk = []

            for i in range(pages):
                pageObj = pdfReader.pages[i]
                text = pageObj.extract_text()
                words = text.split()
                for word in words:
                    current_chunk.append(word)
                    if len(current_chunk) >= 2500:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = []

            # Add the last chunk if it's not empty and has fewer than 3000 words
            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks
        
        def chunkerStringArray(self, string_array):
            chunks = []
            current_chunk = []

            for word in string_array:
                # Check if adding this word would make the chunk longer than 3000 characters
                if len(' '.join(current_chunk + [word])) > 3000:
                    # If so, add the current chunk to the list of chunks and start a new chunk
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []

                # Add the word to the current chunk
                current_chunk.append(word)

            # Add the last chunk if it's not empty
            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks
        # Reads a pdf, inputs them into chunks into GPT-3.5, then returns the raw facts from the file. 
        def info_extractor(self, textbook_path): 
            listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."

            rawFacts = []
            textbookChuncked = self.chunker(textbook_path)    
            for i in range(len(textbookChuncked)) : 
                rawFacts.append(self.gptAgent.open_ai_gpt_call(textbookChuncked[i], listPrompt))  # Changed here

            return rawFacts
    class SentenceIdentifier : 
        def split_into_sentences(self, text: str) -> list[str]:
            alphabets= "([A-Za-z])"
            prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
            suffixes = "(Inc|Ltd|Jr|Sr|Co)"
            starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
            acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
            websites = "[.](com|net|org|io|gov|edu|me)"
            digits = "([0-9])"
            multiple_dots = r'\.{2,}'

            """
            Split the text into sentences.

            If the text contains substrings "<prd>" or "<stop>", they would lead 
            to incorrect splitting because they are used as markers for splitting.

            :param text: text to be split into sentences
            :type text: str

            :return: list of sentences
            :rtype: list[str]
            """
            text = " " + text + "  "
            text = text.replace("\n"," ")
            text = re.sub(prefixes,"\\1<prd>",text)
            text = re.sub(websites,"<prd>\\1",text)
            text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
            text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
            if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
            text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
            text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
            text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
            text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
            text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
            text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
            if "”" in text: text = text.replace(".”","”.")
            if "\"" in text: text = text.replace(".\"","\".")
            if "!" in text: text = text.replace("!\"","\"!")
            if "?" in text: text = text.replace("?\"","\"?")
            text = text.replace(".",".<stop>")
            text = text.replace("?","?<stop>")
            text = text.replace("!","!<stop>")
            text = text.replace("<prd>",".")
            sentences = text.split("<stop>")
            sentences = [s.strip() for s in sentences]
            if sentences and not sentences[-1]: sentences = sentences[:-1]
            return sentences
    

class FlashcardModels : 
    class FlashcardModelV1 : 
        def __init__(self):
            self.gptAgent = AiOfficalModels.OpenAI()
            self.InfoExtraction = GeneralAiModels.InfoExtractorV1()
            self.SentenceIdentifier = GeneralAiModels.SentenceIdentifier()
        def flashcard_intialise(self, questionPrompt, textbook_path):
            rawInfo = self.InfoExtraction.info_extractor(textbook_path) #creates the raw information
            answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
            questionsArray = []

            for answer in answerArray:
                questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
            return questionsArray, answerArray

class yearlyPlanProcess : 
    class yearlyPlanCreator : 
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
            gptAgent = AiOfficalModels.OpenAI()
            InfoExtractor = GeneralAiModels.InfoExtractorV1() # Creates a infoExtractor object
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
            gptAgent = AiOfficalModels.OpenAI()
            for i in range(len(lessonPlanFacts)) : 
                lessonPlans.append(gptAgent.open_ai_gpt_call(lessonPlanFacts[i], powerpointCreatorPrompt))

            
            return lessonPlans
        def yearly_plan_homework_creator(self, lessons, schoolType) :
            homeworkContent = [] 
            homeworkPrompt = f"""Pretend you are a teacher for a {schoolType}. Based on the following powerpoint slides, create a homework plan for students to compelete.
                                Remember to only test based on the information provided: """
            gptAgent = AiOfficalModels.OpenAI()
            for i in range(len(lessons)) : 
                homeworkContent.append(gptAgent.open_ai_gpt_call(lessons[i], homeworkPrompt))

            return homeworkContent
        def yearly_plan_final(self, lessonNumber, path) : 
            lessonPlanFacts = self.yearly_plan_facts_per_lesson(lessonNumber, path)
            finalLessonStructure = self.yearly_plan_powerpoint_creator(lessonPlanFacts)
            return finalLessonStructure

class tutorAiModels :
    class TutorAIV1:
        def __init__(self):
            self.chat_history = []
            self.gpt_initialise = AiOfficalModels.OpenAI()
            self.SmartGPT = GeneralAiModels.SmartGPTV1()
        def get_difficulty(self, request):
            difficultyDeterminePrompt = """Based on the user's prompt, determine it's difficulty in answering. return ONLY one of the three, based on how hard it is to answer: 
                                     "EASY", "MEDUIM", "HARD" """ 
            
            return self.gpt_initialise.open_ai_gpt_call(request, difficultyDeterminePrompt)
        def get_responseGpt3(self, request):
            gpt3Prompt = ""
            return self.gpt_initialise.open_ai_gpt_call(request, gpt3Prompt)
        def get_responseGpt4(self, request) : 
            gpt4Prompt = ""
            return self.gpt_initialise.open_ai_gpt4_call(request, gpt4Prompt)
        def get_smartResponseGpt4(self, request) : 
            SmartGPTPrompt = ""
            return self.SmartGPT.smart_gpt(request)
        def tutor_ai_initialise(self): 
            while True:  # start an infinite loop
                current_request = input("\nPlease enter your request (or type 'quit' to exit): ")
                
                
                # If user types 'quit', break the loop
                if current_request.lower() == 'quit':
                    break

                difficulty = self.get_difficulty(current_request)
                print(difficulty)
                if re.match(r'^EASY', difficulty):
                    print("This is an EASY question")
                    print(self.get_responseGpt3(current_request))
                elif re.match(r'^MEDIUM', difficulty): 
                    print("This is a MEDIUM question")
                    print("GPT answer here")
                    print(self.get_responseGpt3(current_request))
                elif re.match(r'^HARD', difficulty): 
                    print("This is a HARD question")
                    print("SmartGPT response here") 
                    print(self.get_responseGpt3(current_request))
                else:
                    print("Error in difficulty determination.")
                    continue  # Skip to the next iteration
class ExamCreatorModels : 
    class AQAEnglishPapers : 
        class AQAEnglishLanguagePapers :
            class Paper1 : 
                class SourceExtractor : 
                    def get_pdf_content(self, pdf_file):
                        sourceTextRaw = ""
                        with open(pdf_file, 'rb') as pdf_file_obj:
                            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
                            numpages =  pdf_reader.getNumPages()

                            random_number = random.randint(5, numpages - 5)
                            
                            for i in range(random_number-1, random_number+1) : 
                                page_obj = pdf_reader.getPage(i)
                                sourceTextRaw = sourceTextRaw + page_obj.extract_text()
                        
                        return sourceTextRaw
                    def start_and_end_lines(self, content) : 
                        regexExpression = r'"(.*?)"'
                        sourceExtractionPrompt = ""
                        gptAgent = AiOfficalModels.OpenAI
                        beginningAndEndingLines = gptAgent.open_ai_gpt_call(content, sourceExtractionPrompt) #Calls GPT-3.5, creates the first and last line of the content extracted
                        beginningAndEndingLines  = beginningAndEndingLines.replace("\n", " ") # Takes away any line breaks
                        beginningAndEndingLines = re.findall(regexExpression, beginningAndEndingLines) #Seperates the result into two strings. [0] = start, [1] = last.
                        return beginningAndEndingLines
                    def extract_subsection(self, text, start_sentence, end_sentence):
                        start_index = text.find(start_sentence)
                        end_index = text.find(end_sentence)

                        if start_index == -1 or end_index == -1:
                            return "Start or end sentence not found in the text."
                        
                        # Adjust the indices to include the end sentence
                        end_index += len(end_sentence)

                        # Extract the subsection
                        subsection = text[start_index:end_index]

                        return subsection
                    def source_extraction(self, pdf_file):
                        if isinstance(pdf_file, str) : 
                            content = pdf_file
                        else : 
                            content = self.get_pdf_content(pdf_file)
                        startAndEndLines = self.start_and_end_lines(content)
                        sourceExtract = self.extract_subsection(content, startAndEndLines[0], startAndEndLines[1])

                class Question1 : 
                    def character_selection(self, sourceExtract) : 
                        quesOnePrompt = ""
                        gptAgent = AiOfficalModels.OpenAI
                        significantCharcter = gptAgent.open_ai_gpt_call(sourceExtract, quesOnePrompt)
                        quesOneStringStructure = f"List four things about {significantCharcter} from this part of the source."
                        
                        return quesOneStringStructure
                    def setting_selection(self, sourceExtract) : 
                        return 
                    def final_model(self, sourceExtract, choice) : 
                        if choice == 0 : 
                            question = self.characterSelection(sourceExtract)
                            return question
                        else : 
                            question = self.settingSelection(sourceExtract)
                            return question
               
                    


                        




#Questions to improve tutorAI: 
# 1. How good is GPT-3.5 at be able to identify how hard/easy a question is? If not, how good will GPT-4 and SmartGPT be at this? 
# 2. How can I implement function calls to be able to improve the validity of the answer, and for which domians would this be needed?
# 3. Can I implmenet chat history for the 'get difficulty' section, and have it perform function calls for the difficulty levels, to bypass it's changing responses?
# 4. How does the temperature setting chances effect the model, to allow it to stay within the prompt's directions ?
# 5. Test out the midjourneyAPI and see how good it is as an API.

########################################################################  TESTING CODE ###########################################################


path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."
questionPrompt = "Write a me a tailored question for the following raw fact for a flashcard."
infoExtractPrompt = ""
school = "Primary School"
# test = yearlyPlanProcess.yearlyPlanCreator()
#lessonisedFacts = test.yearly_plan_facts_per_lesson(2, path)
#powerpoints = test.yearly_plan_powerpoint_creator(lessonisedFacts)
#homework = test.yearly_plan_homework_creator(lessonisedFacts, school)
#print(lessonisedFacts[0])
#print(powerpoints[0])
#print(homework[0])
#tutorAitest = tutorAiModels.TutorAIV1().tutor_ai_initialise()
# print(os.getenv("PINECONE_ENV"))
# print(os.getenv("PINECONE_API_KEY"))

flashcardMaker = FlashcardModels.FlashcardModelV1()
flashcards = flashcardMaker.flashcard_intialise(questionPrompt, path)
print(flashcards[0])
print(flashcards[1])