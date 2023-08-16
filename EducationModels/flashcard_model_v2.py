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
    
    
############  TESTING CODE #############
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

rawFacts = """ 1. {Auditory parts of working memory are located in the left frontal and parietal lobes.} 2. {The visual sketchpad is located in the right hemisphere of the brain.} 3. {Working memory may have co-evolved with speech.} 4. {Long-term memory is divided into different systems located in different brain networks.} 5. {Information enters sensory systems and then passes through specialized processing networks.} 6. {There are areas in the cortex that extract perceptual representations of objects.} 7. {Semantic memory stores factual knowledge organized into categories.} 8. {The brain organizes encoded information into categories for efficient memory retrieval.} 9. {Skills and emotional learning are types of long-term memory.} 10. {Different brain areas are involved in skill learning and emotional learning.} 11. {Episodic memory is used to remember personal experiences.} 12. {Episodic memory is different from learning facts because events happen only once.} 13. {Amnesic patients have deficits in episodic memory.} 14. {Damage to specific brain regions affects the formation of episodic and semantic memories.} 15. {The perirhinal cortex mediates the sense of familiarity in episodic memory.} 16. {The hippocampus encodes events and places in episodic memory.} 17. {Certain types of semantic dementia can cause breakdown of semantic memory.} 18. {Neuroscientists study neurological patients and conduct research using laboratory animals to understand the neurobiology of memory.}

"""
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
testRaw = infoExtractionTest.renumber_facts(rawFacts)

flashcards = test.flashcard_creator_from_raw_facts(rawFacts, 1)
print(flashcards)
print(testRaw)