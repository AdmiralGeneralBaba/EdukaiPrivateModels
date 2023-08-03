from openai_calls import OpenAI
from info_extraction_v1 import InfoExtractorV1
import re


class FlashcardModelV2 : 
    def flashcard_question_creator(self, answers, gpt_type) : #Creates the questions for the given answers
        infoExtractor = InfoExtractorV1()
        gptAgent = OpenAI()
        gptTemperature = 0.5
        prompt = """I want you to pretend to be a question creating expert for flashcards. Based on these facts, I want you to create tailored, short questions for each one of these facts, such that they make sense logically for the answer on the back, and that the answer on the back PERFECTLY answers the question. scan through each fact, indicated by the number as the identifier of that fact, and the curly brackets from the beginning the to the end signifying the start and end of that fact.   ONLY print out the information. Before printing out the questions, have there be a number indicating the fact number, starting from '1.'. the fact MUST be surrounded by curly brackets, such that the structure of each fact MUST be : 1. {INSERT QUESTION HERE} 2. {INSERT QUESTION HERE}, they MUST BE IN THESE CURLY BRACKETS. Here's an example output for what you should do (ignore the facts, just for the structure : 

1. {What is the chemical symbol for Iron in the Periodic Table?}
2. {Which planet in our solar system is known as the Red Planet?}
3; {Who wrote the novel "1984"?}
4. {What is the capital of Australia?}
5. {Who painted the "Starry Night"?}

 Here are the raw facts :  """ 
        if gpt_type == 0 :
            questions = gptAgent.open_ai_gpt_call(answers, prompt, gptTemperature)
        else : 
            questions = gptAgent.open_ai_gpt4_call(answers, prompt, gptTemperature)
        renumberedQuestions = infoExtractor.renumber_facts(questions)   
        return renumberedQuestions
    
    def clean_text(self, text): #Cleans the text around the questions and answers so it looks better for the final output
        # Remove the number and the curly brackets
        clean_text = re.sub(r'^\d+\.\s*{(.+)}$', r'\1', text)
        return clean_text

    def create_qa_dict(self, questions, answers): #creates the question and answers dictionary
        # Check if both lists have the same length
        if len(questions) != len(answers):
            raise ValueError("The questions and answers lists must have the same length.")
        
        # Create the dictionary
        qa_dict = []
        for i in range(len(questions)):
            qa_dict.append({'question': self.clean_text(questions[i]), 'answer': self.clean_text(answers[i])})
        
        return qa_dict
    

    #NEW flashcard creator - Creates flashcards based on a input of facts, in the layout specified in the documents. 
    def flashcard_creator_from_raw_facts(self, answers, gpt_type) : 
        info_extraction = InfoExtractorV1()
        questions = self.flashcard_question_creator(answers, gpt_type)
        question_array = info_extraction.facts_splitter_into_array(questions)
        answer_array = info_extraction.facts_splitter_into_array(answers)
        flashcards = self.create_qa_dict(questions=question_array, answers=answer_array) 
        return flashcards

    def flashcard_intialise_pdf_legacy(self, textbook_path, chunkSize): #Creates flashcards for the whole of an inputted PDF in one go. 
        gptAgent = OpenAI()
        infoExtractor = InfoExtractorV1()
        questionPrompt = """Create me a tailored, short questions for these raw facts to be used in a flashcard. They should follow a numbered structure.
raw facts :  """
        rawInfo = infoExtractor.info_extractorV2(textbook_path, chunkSize) #creates the raw information in an array 'rawInfo', where at position i it is the raw facts for a section in the textbook.
        answerArray = []
        for i in range(len(rawInfo)) : 
            print("Answer Created!")
            answerArray.append(infoExtractor.process_facts(rawInfo))  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(gptAgent.open_ai_gpt_call(answer, questionPrompt, 0.5))   
        return questionsArray, answerArray
        

test = FlashcardModelV2()
infoExtractionTest = InfoExtractorV1()

rawText = """Introduction:
The French Revolution, which unfolded between 1789 and 1799, was a watershed moment in European history. It was a period of radical social and political upheaval that dramatically transformed France and reverberated throughout the world. This essay explores the causes, key events, and long-term effects of the French Revolution, shedding light on its profound impact on society, governance, and the pursuit of liberty, equality, and fraternity.

Causes of the French Revolution:
The French Revolution was not an isolated event but rather a culmination of various economic, social, and political factors. One of the primary catalysts was the prevailing social inequality in France, where the clergy and nobility enjoyed privileges while the majority of the population suffered from poverty and exploitation. Economic crises, such as food shortages and inflation, further exacerbated the discontent among the common people. Enlightenment ideas and the spread of democratic principles also played a crucial role, as philosophers challenged traditional authority and advocated for individual rights and popular sovereignty.

Key Events of the French Revolution:
The French Revolution unfolded through a series of significant events that forever changed the course of history. It began with the convening of the Estates-General in 1789, where representatives from all social classes were gathered to address the country's grievances. The subsequent storming of the Bastille on July 14, 1789, symbolized the people's revolt against the monarchy and marked the start of the revolution. The National Assembly, formed by the representatives, issued the Declaration of the Rights of Man and of the Citizen, proclaiming liberty, equality, and fraternity as fundamental principles.

The revolution continued with the radical phase characterized by the Reign of Terror, led by the Committee of Public Safety under Maximilien Robespierre. This period witnessed intense political upheaval, mass executions, and the rise of radical factions. However, it eventually gave way to the Thermidorian Reaction in 1794, leading to the fall of Robespierre and the Committee. The revolution culminated in 1799 when Napoleon Bonaparte came to power, ending the revolutionary era and establishing the Napoleonic Empire.

Long-Term Effects of the French Revolution:
The French Revolution had far-reaching consequences that reverberated across Europe and beyond. Firstly, it challenged the prevailing monarchical system, heralding the rise of republics and inspiring subsequent revolutionary movements across the continent. The principles of liberty, equality, and fraternity became the guiding lights for those seeking political and social change.

Moreover, the revolution had a profound impact on French society. Feudal privileges were abolished, and the Napoleonic Code established legal equality, guaranteeing individual rights and freedom. The revolution also brought about sweeping economic changes, dismantling the guild system and introducing capitalist practices that laid the foundation for modern industrialization.

Internationally, the French Revolution sparked ideological debates and influenced political developments. It spread revolutionary ideas across Europe, leading to the rise of nationalism, the emergence of modern ideologies such as liberalism and conservatism, and subsequent social and political transformations.

Conclusion:
The French Revolution was a transformative period in history, driven by social inequality, economic crises, and the spread of Enlightenment ideals. Its impact was felt not only within France but also far beyond its borders. The revolution forever altered the political and social landscape, challenging traditional authority and advocating for liberty, equality, and fraternity. Its enduring legacy can be seen in the principles that shaped modern democracies and the pursuit of individual rights and social justice. The French Revolution remains a powerful reminder of the potential for radical change when the voices of the oppressed and marginalized demand justice and freedom."""

rawFacts = """ 1. {Navies primarily control sea lanes, escort or intercept trade convoys, and support overseas military action.} 2. {Fleets can perform missions in up to three contiguous sea zones.} 3. {Patrol missions spread fleets out in search of enemy ships.} 4. {Search and Destroy missions keep fleets close together to maximize killing power.} 5. {Convoy raiding missions spread fleets out to seek convoy vessels.} 6. {Convoy escort missions protect trade ships.} 7. {Hold missions stop fleets in their current sea zone to assist ground operations.} 8. {Carrier groups should not have more than four aircraft carriers to avoid air combat penalties.} 9. {A naval power should have multiple battle fleets to dominate sea lanes.} 10. {A fleet should have a mix of battleships, heavy cruisers, light cruisers, and destroyers.} 11. {Naval experience can be used to upgrade and improve vessels.} 12. {Specialized ships can be created for specific tasks.} 13. {Research priorities shift in the mid-game to focus on other aspects of the game.} 14. {Late-game is about getting more advanced weapons and tactics onto the field.} 15. {Unlocking extra research slots in the National Focus tree before the war starts should be a top priority.} 16. {Researching industrial efficiency is important for saving efficiency loss and equipping divisions faster.} 17. {Researching new infantry equipment is important for the backbone of the army.} 18. {Devoting research slots to military doctrines is recommended.}
"""
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
testRaw = infoExtractionTest.renumber_facts(rawFacts)

flashcards = test.flashcard_creator_from_raw_facts(rawFacts, 1)
print(flashcards)
print(testRaw)