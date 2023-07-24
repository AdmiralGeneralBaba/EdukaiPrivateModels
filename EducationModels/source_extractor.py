import PyPDF2
import re
import random
from openai_calls import OpenAI




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
        gptAgent = OpenAI()
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
