from openai_calls import OpenAI
import PyPDF2
import re
import asyncio
import aiohttp


class InfoExtractorV3 :        
        def __init__(self):
           self.gptAgent = OpenAI()          
        # Current PDF extraction system - Need for it to be updated so that it is more consistent. 
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
                        print("Chunk Appended")

            # Add the last chunk if it's not empty and has fewer than 3000 words
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                
            pdfFileObj.close()
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
        async def info_extractorV3(self, textbook_path, chunkSize): 
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
            textbookChuncked = self.chunker(textbook_path, chunkSize)

            # Create a list of tasks to call open_ai_gpt_call for all chunks
            tasks = [self.gptAgent.async_open_ai_gpt_call(chunk, listPrompt, gptTemp) for chunk in textbookChuncked]

            # Use asyncio.gather to run all tasks concurrently
            rawFacts = await asyncio.gather(*tasks)

            print("All lessons appended")
            return rawFacts
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
