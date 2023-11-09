from openai_calls import OpenAI
import PyPDF2
import re
import asyncio
import aiohttp


class InfoExtractorV4 :        
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
        async def info_extractorV4(self, textbook_path, chunkSize): 
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
                # Use asyncio.gather to run all tasks concurrently and extend the rawFacts list with the results

                (print("Calling fact extractor GPT agents..."))
                rawFacts.extend(await asyncio.gather(*tasks))

                # Wait for one minute before processing the next batch
                print(f"Successfully went through {i + 50} chunks!")

                print("sleeping for 60 seconds...")
                await asyncio.sleep(60)
                print("Slept for 60 seconds!")

            print("All lessons appended")
            return rawFacts
        
        #Takes the text inputted, puts the chunks into gpt-3.5, then returns the raw facts from the file 
        async def text_info_extractorV4(self, text, chunkSize): 
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
                # Use asyncio.gather to run all tasks concurrently and extend the rawFacts list with the results

                (print("Calling fact extractor GPT agents..."))
                rawFacts.extend(await asyncio.gather(*tasks))

                # Wait for one minute before processing the next batch
                print(f"Successfully went through {i + 50} chunks!")

                print("sleeping for 60 seconds...")
                await asyncio.sleep(60)
                print("Slept for 60 seconds!")

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

# test = InfoExtractorV4
# path = "C:\\Users\\david\\Desktop\\Making_It_Stick.pdf"
# small_path = "C:\\Users\\david\\Downloads\\CV David Tiareh"
# medium_path = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\HoI_IV_Strategy_Guide.pdf"
# big_path = "C:\\Users\\david\\Desktop\\PrinciplesOfBiology.pdf"
# async def yearly_plan_facts_per_lesson_pdf_input_only_test(pdf_path): 
#         print("Initializing InfoExtractor...")
#         infoExtract = InfoExtractorV4() # Creates the infoExtractor 
#         print("Extracting raw facts from PDF...")
#         rawFacts = await infoExtract.info_extractorV4(pdf_path, 1200) # Calls info extractor HERE WE CAN CHANGE THE CHUNK SIZE TO BE OR LESS DETAILED.
#         return rawFacts

# async def main():
#     facts = await yearly_plan_facts_per_lesson_pdf_input_only_test(big_path)
#     print(facts)

# # This is the Python >= 3.7 way of running the main coroutine
# asyncio.run(main())