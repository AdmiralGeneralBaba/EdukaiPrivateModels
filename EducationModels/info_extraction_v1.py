from openai_calls import OpenAI
import PyPDF2
import re


class InfoExtractorV1 :        
        def __init__(self):
           self.gptAgent = OpenAI()          
        def chunker(self, path, chunkSize) :
            pdfFileObj = open(path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj) 
            pages = len(pdfReader.pages)

            chunks = []
            current_chunk = []

            for i in range(pages):
                pageObj = pdfReader.pages[i]
                text = pageObj.extract_text()
                words = text.split()
                for word in words:
                    current_chunk.append(word)
                    if len(current_chunk) >= chunkSize: #Ajust this value to decrease/increase the word count, so that the raw facts are more/less detailed.
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
        def info_extractor(self, textbook_path, chunkSize): 
            listPrompt = """ list EVERY SINGLE fact in this piece of text. Make sure to include ALL raw information, and nothing more. When listing the facts, 
                             ONLY print out the information. Before printing out the facts, have there be a number indicating the fact number. Here are examples of how the facts should be printed out:
                             { 
                             1. : The empire state building is one of the tallest buildings in manhatten
                             2. : England is a part of Great Britain 
                             3. : Donald Trump was the president from 2016 to 2020
                             }
                             """

            rawFacts = []
            textbookChuncked = self.chunker(textbook_path, chunkSize)    
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

            :param text: text to be split               into sentences
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