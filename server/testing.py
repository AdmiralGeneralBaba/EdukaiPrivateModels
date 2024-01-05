import PyPDF2
import random
import re
from openai_calls import OpenAI

def get_pdf_content(pdf_file):
    contentGrammerFixerPrompt = """On the following raw text, remove any grammatical errors or spacing, but KEEP THE CONTENT EXACTLY THE SAME : """
    sourceTextRaw = ""
    with open(pdf_file, 'rb') as pdf_file_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        numpages =  len(pdf_reader.pages)

        random_number = random.randint(5, numpages - 5)
        
        for i in range(random_number-1, random_number+1) : 
            page_obj = pdf_reader.pages[i]
            sourceTextRaw = sourceTextRaw + page_obj.extract_text()
    
    sourceTextRaw  = sourceTextRaw.replace("\n", " ") # Takes away any line breaks
    print(sourceTextRaw)
    gptAgent = OpenAI()  # Creating an instance of OpenAI
    sourceTextNoSpaces = gptAgent.open_ai_gpt_call(user_content=sourceTextRaw, prompt=contentGrammerFixerPrompt)  # Call the method on the instance
    print(sourceTextNoSpaces)
    return sourceTextNoSpaces, random_number, numpages

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
    print(beginningAndEndingLines)
    return beginningAndEndingLines

def extract_subsection(text, start_sentence, end_sentence):
            start_index = text.find(start_sentence)
            end_index = text.find(end_sentence)

            if start_index == -1 or end_index == -1:
                return "Start or end sentence not found in the text."
            
            # Adjust the indices to include the end sentence
            end_index += len(end_sentence)

            # Extract the subsection
            subsection = text[start_index:end_index]

            return subsection
def source_extraction(pdf_file):
    
        content = get_pdf_content(pdf_file)
        startAndEndLines = start_and_end_lines(content)
        print('Start sentence:', startAndEndLines[0])
        print('End sentence:', startAndEndLines[1])
        print('Content:', content[0])
        sourceExtract = extract_subsection(content[0], startAndEndLines[0], startAndEndLines[1])
        return sourceExtract



path = "C:\\Users\\david\\Desktop\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
listPrompt = "list all of the facts in this piece of text. Make sure to include ALL raw information, and nothing more."
questionPrompt = "Write a me a tailored question for the following raw fact for a flashcard."
school = "Primary School"
choice = 0


content = get_pdf_content(path) 
print(start_and_end_lines(content))