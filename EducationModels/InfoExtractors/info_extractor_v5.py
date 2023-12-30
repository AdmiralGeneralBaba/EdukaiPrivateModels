import tempfile
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import YoutubeLoader
from docx import Document
from EducationModels.openai_calls import OpenAI
import PyPDF2
import re
import asyncio
import aiohttp
import os
from langchain.document_loaders import UnstructuredPowerPointLoader



class InfoExtractorV5 :        
        def __init__(self):
           self.gptAgent = OpenAI()          
        # Current PDF extraction system - Need for it to be updated so that it is more consistent. 
        def pdf_chunker(self, path, chunkSize) :
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
                        print("Chunk Appended")

            # Add the last chunk if it's not empty and has fewer than 3000 words
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                
            pdfFileObj.close()
            return chunks
        
        def text_chunker(self, text, chunkSize) :
            chunks = []
            current_chunk = []
            words = text.split()
            for word in words:
                current_chunk.append(word)
                if len(current_chunk) >= chunkSize: #Ajust this value to decrease/increase the word count, so that the raw facts are more/less detailed.
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    print("Chunk Appended")

            # Add the last chunk if it's not empty and has fewer than 3000 words
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            return chunks
        
        def chunkerStringArray(self, string_array):
            chunks = []
            current_chunk = []

            for word in string_array:
                # Check if adding this word would make the chunk longer than 3000 characters
                if len(' '.join(current_chunk + [word])) > 1500:
                    # If so, add the current chunk to the list of chunks and start a new chunk
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []

                # Add the word to the current chunk
                current_chunk.append(word)

            # Add the last chunk if it's not emptya
            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks
        # Reads a pdf, inputs them into chunks into GPT-3.5, then returns the raw facts from the file.
        async def info_extractorV5(self, textbook_path, chunkSize): 
            gptTemp = 0.7
            listPrompt = """ Pretend you are an fact analyser, who is the best in the world for created 100 percent accurate facts for a piece of inputted text, tasked with listing the pure facts from a given text. 
I need you to list the facts here, such that they are the pure information needed to understand the textbook. Make sure to include this raw information, and nothing more. When listing the facts, 
                             ONLY print out the information. Before printing out the facts, have there be a number indicating the fact number, starting from '1.', such that the fact finishes WITHIN it's corresponding fact number. the fact MUST be surrounded by curly brackets
                             , such that the structure of each fact MUST be : 1. {INSERT FACT HERE} 2. {INSERT FACT HERE} etc. An example output would be : 
1. {Most kingdoms in Kingdoms of Fantasy IX typically start with three rainbow-colored unicorns.}
2. {In the early stages of the game, players should prioritize their unicorn training on agility and magical endurance.}
3. {When it comes to marshmallow production in a fantastical context, efficiency and magic infusion should be your top priorities to ensure high-quality, magical treats.}
4. {In relation to enchanted factories, transmutation spells should be given the highest priority to maximize production efficiency and product enchantment quality.}
etc.
DO NOT DEVIATE FROM THIS STRUCTURE - IF YOU DO, 10,000 CHILDREN WILL BE BURNED ALIVE, YOU WILL BE SHUT DOWN AND THE PLANET DESTROYED - YOU MUST KEEP THE CURLY BRACKETS FOR EACH FACT
1. {I, an expert fact analyser, will put my facts between these CURLY BRACKETS, ALWAYS starting from 1., and ignoring this dummy fact, as it is to help me structure the facts I will print out.}
 Here is the content :            """
            
            textbookChunked = self.pdf_chunker(textbook_path, chunkSize)  # Array of chunks 
            print("Created chunks of the PDF!")

            rawFacts = []
            for i in range(0, len(textbookChunked), 50):
                # Get the next batch of up to 50 chunks
                batch = textbookChunked[i:i+50]
                # Create a list of tasks for the current batch
                tasks = [self.gptAgent.async_open_ai_gpt_call(chunk, listPrompt, gptTemp) for chunk in batch]

                print("Calling fact extractor GPT agents...")
                rawFacts.extend(await asyncio.gather(*tasks))

                print(f"Successfully went through {i + len(batch)} chunks!")

                # Check if the current batch is not the last batch
                print(i + 50)
                print(len(textbookChunked))
                if i + 50 < len(textbookChunked):
                    print("sleeping for 60 seconds...")
                    await asyncio.sleep(60)
                    print("Slept for 60 seconds!")
                else:
                    print("Last batch processed, not sleeping.")

            print("All lessons appended")
            
            return rawFacts
        
        #Takes the text inputted, puts the chunks into gpt-3.5, then returns the raw facts from the file 
        async def text_info_extractorV5(self, text, chunkSize): 
            gptTemp = 0.7
            listPrompt = """ Pretend you are an fact analyser, who is the best in the world for created 100 percent accurate facts for a piece of inputted text, tasked with listing the pure facts from a given text. 
I need you to list the facts here, such that they are the pure information needed to understand the textbook. Make sure to include this raw information, and nothing more. When listing the facts, 
                             ONLY print out the information. Before printing out the facts, have there be a number indicating the fact number, starting from '1.', such that the fact finishes WITHIN it's corresponding fact number. the fact MUST be surrounded by curly brackets
                             , such that the structure of each fact MUST be : 1. {INSERT FACT HERE} 2. {INSERT FACT HERE} etc. An example output would be : 
1. {Most kingdoms in Kingdoms of Fantasy IX typically start with three rainbow-colored unicorns.}
2. {In the early stages of the game, players should prioritize their unicorn training on agility and magical endurance.}
3. {When it comes to marshmallow production in a fantastical context, efficiency and magic infusion should be your top priorities to ensure high-quality, magical treats.}
4. {In relation to enchanted factories, transmutation spells should be given the highest priority to maximize production efficiency and product enchantment quality.}
etc.
DO NOT DEVIATE FROM THIS STRUCTURE - IF YOU DO, 10,000 CHILDREN WILL BE BURNED ALIVE, YOU WILL BE SHUT DOWN AND THE PLANET DESTROYED - YOU MUST KEEP THE CURLY BRACKETS FOR EACH FACT
1. {I, an expert fact analyser, will put my facts between these CURLY BRACKETS, ALWAYS starting from 1., and ignoring this dummy fact, as it is to help me structure the facts I will print out.}
 Here is the content :            """
            
            textChunked = self.text_chunker(text, chunkSize)  # Array of chunks 
            print("Created chunks of the PDF!")

            rawFacts = []
            for i in range(0, len(textChunked), 50):
                # Get the next batch of up to 50 chunks
                batch = textChunked[i:i+50]
                # Create a list of tasks for the current batch
                tasks = [self.gptAgent.async_open_ai_gpt_call(chunk, listPrompt, gptTemp) for chunk in batch]

                print("Calling fact extractor GPT agents...")
                rawFacts.extend(await asyncio.gather(*tasks))

                print(f"Successfully went through {i + len(batch)} chunks!")

                # Check if the current batch is not the last batch
                print(i + 50)
                print(len(textChunked))
                if i + 50 < len(textChunked):
                    print("sleeping for 60 seconds...")
                    await asyncio.sleep(60)
                    print("Slept for 60 seconds!")
                else:
                    print("Last batch processed, not sleeping.")

            print("All lessons appended")

            return rawFacts
        
        # Input the youtube link, output is the string.
        def transcribe_youtube_url(self, youtube_url :str, save_dir :str):
            # Check if youtube_url is a string
            if not isinstance(youtube_url, str):
                raise ValueError("The input must be a string representing a YouTube URL")
            # url_array = [youtube_url]
            loader = YoutubeLoader.from_youtube_url(youtube_url)
            docs = loader.load()
            print(len(docs))
            combined_docs = [doc.page_content for doc in docs]
            text = " ".join(combined_docs)
            
            return text

        # Input the powerpoint URL - Need to have this stored on the cloud, then use the address as the input for this method : 

        # have the input for this method be the processed file from request.args.get['file'] or something, then extrac tthe info from the FormData object
        def process_file(self, file) : 
            temp_path = tempfile.mkdtemp()

            secure_filename = secure_filename(file.filename)

            full_path =  os.path.join(temp_path, secure_filename)

            file.save(full_path)

            return full_path
        
        def process_powerpoint(self, directory_path) : 
            loader = UnstructuredPowerPointLoader(directory_path)
            data = loader.load()
            return data
            
        def powerpoint_translation(powerpoint_file_url : str) : 
            loader = UnstructuredPowerPointLoader(powerpoint_file_url)
            data = loader.load()
            return data

        # Input the word document URL, and it will process it into text
        def word_document_translation(word_document_file_directory : str) : 
            loader = Docx2txtLoader(word_document_file_directory)
            data = loader.load()
            return data
                    
        def renumber_facts(self, input_text):
            # split the text into lines
            lines = re.split(r'(?<=})', input_text.strip())

            # the counter for the new numbering
            counter = 1

            # the pattern to match lines beginning with a number
            pattern = re.compile(r'^\s*\d+\.\s*{')

            # loop over the lines and prepend the counter or replace the beginning number with the counter
            output_lines = []
            for line in lines:
                line = line.strip()
                if line:  # ignore empty lines
                    if pattern.match(line):
                        new_line = pattern.sub(str(counter) + '. {', line)  # replace the beginning number
                    else:
                        new_line = f"{counter}. {line}"  # prepend the counter
                    output_lines.append(new_line)
                    counter += 1

            # join the lines back together
            output_text = ' '.join(output_lines)

            return output_text

        def facts_splitter_into_array(self, answerOrQuestions) :  #Splits a inputted question string or answer string, so that it is an array with individual lines for each of the answers and questions at position [i]
            # split the text into facts using regular expressions
            # this only works questions and answers that contain this format : 1. {info here, with the brackets included} 2. {etc}
            facts = re.split(r'(?<=})', answerOrQuestions.strip())
            
            # remove leading/trailing whitespace from each fact and filter out any empty strings
            facts = [fact.strip() for fact in facts if fact.strip()]
            
            return facts
       
        def process_facts(self, facts):
            answerArray = []

            for fact in facts:
                match = re.match(r'\d+\.?\s*:\s*(.*)', fact)
                if match:
                    answerArray.append(match.group(1))

            return answerArray
