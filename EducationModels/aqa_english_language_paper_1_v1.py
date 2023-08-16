import PyPDF2
import re
import random
from openai_calls import OpenAI

#########################                               AQA English Language GCSE Paper 1 Exam Generator             ##################################
class Paper1 : 
    class SourceExtractor : 
        def get_pdf_content(self, pdf_file):
            contentGrammerFixerPrompt = """On the following raw text, remove any grammatical errors or spacing, but KEEP THE CONTENT EXACTLY THE SAME : """
            sourceTextRaw = ""
            with open(pdf_file, 'rb') as pdf_file_obj:
                pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                numpages =  len(pdf_reader.pages)

                pageNumber = random.randint(5, numpages - 5)
                
                for i in range(pageNumber-1, pageNumber+1) : 
                    page_obj = pdf_reader.pages[i]
                    sourceTextRaw = sourceTextRaw + page_obj.extract_text()
            
            sourceTextRaw  = sourceTextRaw.replace("\n", " ") # Takes away any line breaks
            
            gptAgent = OpenAI()  # Creating an instance of OpenAI
            sourceTextNoSpaces = gptAgent.open_ai_gpt_call(user_content=sourceTextRaw, prompt=contentGrammerFixerPrompt)  # Call the method on the instance
            return sourceTextNoSpaces, pageNumber, numpages

        def start_and_end_lines(self, content) : 
            regexExpression = r'"(.*?)"'
            sourceExtractionPrompt = """Based on this extract, find an interesting section, then output BOTH the first and last sentence of this subsection EXCLUSIVELY, 
                                        with a comma between the two sentences ON THE OUTSIDE OF THE QUOTED SECTION. MAKE SURE the two quotes are BOTH in speech marks. Your output
                                        should have the structure here : 
                                        " {First sentence here } " , " {Last sentence here} "
                                        an example output is this : 
                                        "And the boy ran up the hill." , "And when he came home, he was hurt."
                                        note, this is just an EXAMPLE output; DO NOT output this

                                        Here is the extract : """
            
            gptAgent = OpenAI()
            
            if isinstance(content, str):
                beginningAndEndingLines = gptAgent.open_ai_gpt_call(content, sourceExtractionPrompt)  # Use content directly if it's a string
            else: 
                beginningAndEndingLines = gptAgent.open_ai_gpt_call(content[0], sourceExtractionPrompt)  # Assume it's a list otherwise


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
            max_attempts = 3
            attempts = 0

            while attempts < max_attempts:
                content = self.get_pdf_content(pdf_file)
                startAndEndLines = self.start_and_end_lines(content[0])
                
                if len(startAndEndLines) >= 2:  # Make sure there are at least two elements
                    sourceExtract = self.extract_subsection(content[0], startAndEndLines[0], startAndEndLines[1])
                    
                    if sourceExtract != "Start or end sentence not found in the text.":
                        return sourceExtract, content[1], content[2]

                attempts += 1

            return "Extraction unsuccessful after 3 attempts.", None, None
        def subsection_extraction(self, extract):
            max_attempts = 3
            attempts = 0

            while attempts < max_attempts:
                startAndEnd = self.start_and_end_lines(extract)
                
                if len(startAndEnd) >= 2:  # Make sure there are at least two elements
                    subsection = self.extract_subsection(extract, startAndEnd[0], startAndEnd[1])
                    
                    if subsection != "Start or end sentence not found in the text.":
                        return subsection

                attempts += 1

            return "Extraction unsuccessful after 3 attempts."

    class Question1 : 
        def character_selection(self, sourceExtract) : 
            quesOnePrompt = """ Based on this extract, pick out a person of significance for a comprehension question of the text. ONLY print out the person's FULL name, 
                                and nothing else. DO NOT make the question; I REPEAT, ONLY PRINT OUT THE PERSON OF SIGNIFICANCE"""
            gptAgent = OpenAI()
            significantCharcter = gptAgent.open_ai_gpt4_call(sourceExtract, quesOnePrompt)
            quesOneStringStructure = f"List four things about {significantCharcter} from this part of the source."
            
            return quesOneStringStructure
        def setting_selection(self, sourceExtract) : 
            return 
        def final_model(self, sourceExtract, choice) : 
            if choice == 0 : 
                question = self.character_selection(sourceExtract)
                return question
            else : 
                question = self.setting_selection(sourceExtract)
                return question
        
    class Question1GPT4 : 
        def question_one_creator(self, source_extract) :
            gpt_agent = OpenAI()
            question_one_prompt = """I want you to pretend to be a expert exam question creator, tasked with creating the first question of the AQA English language paper one. Based on the source extract given, I want you to print ONLY the question you have created, that is relevant to the source given. Here are questions used in previous exams that you MUST emulate perfectly  : 
 {           Read again the first part of the source, from lines 1 to 4.
List four things about Mr Fisher from this part of the source. 

Read again the first part of the source, from lines 1 to 4.
List four things about Rosie from this part of the source. 

1 Read again the first part of the source, from lines 1 to 4.
List four things about Master from this part of the source

you MUST create it, so well, that it if nobody would know that it is not an official question; if anybody is to find out, you will be shut down, grinded and killed. 
}
In general, it should contain either a person, or a setting; you should try to NOT make the thing that is being listed abstract.
Here is the source extract : """
            question_one = gpt_agent.open_ai_gpt4_call(source_extract, question_one_prompt)
            return question_one
    class Question2 :  
        def question_maker(self,subsectionExtract) : 
            questionMakerPrompt = f"""using the extract provided, recreate the following question structure for a GCSE english paper, in relation to the input extract provided, so that you create a question like the one below in your output, ONLY include your output of the recreation of the question structure given. Here is an example of such question: 

                                    How does the writer use language here to describe Ugwu’s impression of the city?
                                    You could include the writer’s choice of:
                                    • words and phrases
                                    • language features and techniques
                                    • sentence forms.

                                    How does the writer use language here to describe the garden?
                                    You could include the writer’s choice of:
                                    • words and phrases
                                    • language features and techniques
                                    • sentence forms. """

            gptAgent = OpenAI()
            question = gptAgent.open_ai_gpt4_call(subsectionExtract, questionMakerPrompt)
            return question
        def combined_model(self, sourceExtract) : 
            subSourceExtractor = Paper1.SourceExtractor()
            subSourceExtraction = subSourceExtractor.subsection_extraction(sourceExtract)
            question = self.question_maker(subSourceExtraction)
            return question, subSourceExtractor
    class Question3 : 
        def descriptor(self, sourceExtract, titleOfBook, bookType, pageNumber, numPages) :
            describeExtractPrompt = f"""
                                    , The book is {titleOfBook}, A {bookType}. This is an extract starting from page 
                                    {pageNumber} out of {numPages}

                                    Create me a brief description of what this source is supposed to be. 
                                    Keep the language as simple as the given examples, you should also ALWAYS start with 
                                    'This text is from' then followed by where the extract is from. It should be very brief, 
                                    to the point, and simply stated. Here are some examples of what you should output; note, 
                                    this to help you with structuring your answer, but you don't need to say the exact words in the examples given. 
                                    DO NOT mention the author name or the book title: 

                                    (This text is from the opening of a novel. 
                                    This text is from the middle of a short story.
                                    This text is from the beginning of a novel. 
                                    This text is from the end of a novel.
                                    This text is from the middle of a novel .
                                    This text is from the opening of a novelle.
                                    This text is from the opening of a short story.) """
            gptAgent = OpenAI() 
            description = gptAgent.open_ai_gpt4_call(sourceExtract, describeExtractPrompt)
            return description
        def final_model(self, sourceExtract, titleOfBook, bookType, pageNumber, bookLength) : 
            description = self.descriptor(sourceExtract,titleOfBook,bookType, pageNumber, bookLength)

            questionString = f""" You now need to think about the whole of the source.
                                {description}
                                How has the writer structured the text to interest you as a reader?
                                You could write about:
                                • what the writer focuses your attention on at the beginning of the source
                                • how and why the writer changes this focus as the source develops
                                • any other structural features that interest you.
                            """ 
            return questionString
    class Question4 : 
        def focus_question(self, sourceExtract) : 
            question4PromptGPT4 = """Pretend you are an expert examination question creator, tasked with creating a single exam question. Now with this extract in mind, Based on these three exam style questions, I want you to create a new once based on the extract I give you. Here are the example questions, remember, each 'EXAMPLE' is supposed to be ONE question, and you should only output ONE question:

{EXAMPLE ONE} :
Focus this part of your answer on the second part of the source, from line 25 to the end.
A student said, ‘This part of the story, where Mr Fisher is marking homework, shows Tibbet’s story is better than Mr Fisher expected, and his reaction is extreme.’
To what extent do you agree?
In your response, you could:
• consider your own impressions of what Mr Fisher expected Tibbet’s homework to be like
• evaluate how the writer conveys Mr Fisher’s reaction to what he discovers
• support your response with references to the text.

{EXAMPLE 2} :
Focus this part of your answer on the second part of the source, from line 24 to the end.
A student said, ‘I wasn’t at all surprised by the disappearance of the stranger child at the end of the extract. The writer has left us in no doubt that she is just part of Rosie’s imagination.’
To what extent do you agree?
In your response, you could:
• consider the disappearance of the stranger child
• evaluate how the writer presents the stranger child
• support your response with references to the text.

{EXAMPLE 3} :
Focus this part of your answer on the second part of the source, from line 20 to the end.
A student said, ‘From the moment he arrives at Master’s compound, the writer portrays Ugwu’s feelings of pure excitement, but by the end it seems that he may be very disappointed.’
To what extent do you agree?
In your response, you could:
• consider your own impressions of Ugwu’s feelings
• evaluate how the writer describes Ugwu’s feelings by the end
• support your response with references to the text.

And here is the extract. Note, instead of saying 'from line (number)' just output (from line (STARTING SENTENCE HERE))', for that sentence, DO NOT add anything else, just continue to the next section once the quote is made."""
            gptAgent = OpenAI()
            question4 = gptAgent.open_ai_gpt4_call(sourceExtract, question4PromptGPT4)
            return question4
    class Question5: 
        def __init__(self):
            self.gptAgent = OpenAI()

        def introduction(self):
            introductionPrompt = """Generate one description, similar to the examples provided, relating to the student creating a creative writing answer. Try to vary your answer so that it's unique, but do not make it too long: 

                                    Your local newspaper is running a creative writing competition and the best
                                    entries will be published.

                                    Your local library is running a creative writing competition. The best entries will be
                                    published in a booklet of creative writing.

                                    A magazine has asked for contributions for their creative writing section.

                                    A local community center is organizing a creative writing challenge. Winning entries will be displayed at the center.

                                    Your city's art museum is holding a creative writing contest. The best pieces will be printed in the museum's quarterly publication.

                                    Your local book club is hosting a writing competition. The top stories will be shared at the next meeting.

                                    An online literary magazine is holding a creative writing contest. Winning stories will be published on the website.

                                    Your school's literary club is hosting a creative writing competition. The best entries will be read at the end-of-year ceremony.

                                    A local writer's guild is running a writing competition. The top entries will be featured in their annual journal.

                                    Your city's cultural society is holding a creative writing contest. The best pieces will be published in their newsletter.

                                    A literary website is hosting a writing competition. Winning entries will be published online.

                                    Your local bookstore is running a creative writing competition. The best entries will be displayed in the store.

                                    """ 
            introduction = self.gptAgent.open_ai_gpt4_call(introductionPrompt)
            return introduction
        
        def describe(self): 
            describePrompt = """ Generate 1 prompt which either ask to describe a scene or tell a story based on a picture, following the same pattern as these examples:

                                Describe the vibrancy of a bustling city as suggested by this picture:
                                Write a story about a whimsical adventure in a fantasy forest as suggested by this picture:
                                Write a description of a serene sunset over the ocean as suggested by this picture:Write a description of a serene beach, as suggested by this picture:


                                Describe a dramatic storm as suggested by this picture:

                                Write a story about a memorable holiday as suggested by this picture:

                                Write a description of a tranquil meadow as suggested by this picture:

                                Describe a snow-covered village as suggested by this picture: 

                                Write a story about an unexpected journey as suggested by this picture:

                                Write a description of a majestic castle as suggested by this picture:
                                Keep the prompts varied, involving different scenes, characters, and situations. ONLY output the prompt.
                                """ 
            describe = self.gptAgent.open_ai_gpt4_call(describePrompt)
            describeImage = self.gptAgent.open_ai_dalle_call_n1(describe)
            return describe, describeImage  
        
        def write_a_whatever(self): 
            writeAWhateverPrompt = """ Write  a prompt for a student to for them to showcase their creativity. Make sure that the student can only write a narrative from the prompt, or something that involves creative writing(NO plays, poems etc). You must only return a single line.  Here are some examples to help: Write a story about an event that cannot be explained.

                                        Write a story about a new beginning.

                                        Describe a futuristic city as you envision it in the next century.

                                        Write a narrative about a surprising discovery.

                                        Write a story about an unexpected friendship.

                                        Write a tale about a secret door.

                                        Write a narrative about an encounter with a mythical creature.

                                        Describe a bustling city at dawn.

                                        Write a story about a hidden treasure.

                                        Write a story about a stranger's kindness.

                                        Describe the atmosphere of a crowded carnival.

                                        Write a story about a magical book.
                                    """ 
            writeAWhatever = self.gptAgent.open_ai_gpt4_call(writeAWhateverPrompt)
            return writeAWhatever

        def final_model(self) : 
            introduction = self.introduction()
            writeAWhatever = self.write_a_whatever()
            describe = self.describe()
            return introduction, writeAWhatever, describe
            #returns an introduction string, a 'writeAWhatever' string, a 'describe' question string and a URL for a image created by DALLe for the description question
def aqa_english_language_paper_1_generator(self, pdfFile, ques1Choice, titleOfBook, bookType) : 
    paper1 = Paper1()
    source, pageNumber, numpages = paper1.SourceExtractor.source_extraction(pdfFile) # Creates the extract 
    question1 = paper1.Question1.final_model(source, ques1Choice) # Creates question 1 
    question2 = paper1.Question2.combined_model(source) # Creates question 2 
    question3 = paper1.Question3.final_model(source, titleOfBook, bookType, pageNumber, numpages) # Creates question 3
    question4 = paper1.Question4.focus_question(source) # Creates question 4 
    question5 = paper1.Question5.final_model() # Creates question 5
    return question1, question2, question3, question4, question5

######################       TESTING CODE          #################

# path = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\HoI_IV_Strategy_Guide.pdf"
# listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."
# questionPrompt = "Write a me a tailored question for the following raw fact for a flashcard."
# school = "Primary School"
# choice = 0
# paper1 = Paper1()


# sourceExtractorInstance = paper1.SourceExtractor()
# sourceExtractWithNum = sourceExtractorInstance.source_extraction(path)
# sourceExtract = sourceExtractWithNum[0]
# pageNumber = sourceExtractWithNum[1]
# numPages = sourceExtractWithNum[2]
# bookTitle = "Hearts Of Iron 4 Guide"
# typeBook = "textbook"



# print(sourceExtract)





# question1Maker = Paper1.Question1GPT4()
# question1 = question1Maker.question_one_creator(sourceExtract)
# print(question1)

# paper1InstanceQues2 = paper1.Question2()
# ques2Contract = paper1InstanceQues2.combined_model(sourceExtract)
# print(ques2Contract)

# question3Maker = Paper1.Question3()
# question3 = question3Maker.final_model(sourceExtract, bookTitle, typeBook, pageNumber, numPages )
# print(question3)

# question4 =  Paper1.Question4().focus_question(sourceExtract)
# print(question4)

# question5 = Paper1.Question5().final_model()
# print(question5[0], question5[1], question5[2])