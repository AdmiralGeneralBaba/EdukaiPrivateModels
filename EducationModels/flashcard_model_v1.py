from openai_calls import OpenAI
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier

class FlashcardModelV1 : 
    def __init__(self):
        self.gptAgent = OpenAI()
        self.InfoExtraction = InfoExtractorV1()
        self.SentenceIdentifier = SentenceIdentifier()
    def flashcard_intialise_pdf(self, textbook_path, chunkSize):
        questionPrompt = """Create me a tailored, short questions for these raw facts to be used in a flashcard. They should follow a numbered structure.
raw facts :  """
        rawInfo = self.InfoExtraction.info_extractor(textbook_path, chunkSize) #creates the raw information in an array 'rawInfo', where at position i it is the raw facts for a section in the textbook.
        answerArray = []
        for i in range(len(rawInfo)) : 
            print("Answer Created!")
            answerArray.append(self.InfoExtraction.process_facts(rawInfo))  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
        return questionsArray, answerArray
    

    def flashcard_intialise_rawText(self, rawInfo):
        questionPrompt = "Create me a tailored, short question for this raw fact to be used in a flashcard : "
        print("Creating answerArray...")
        answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
        print("Answer array created!")
        questionsArray = []
        print("Creating questionArray...")
        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))  
            print(f"question created and appended!") 
        return questionsArray, answerArray
    
    def flashcard_intialise_rawText(self, rawInfo):
        questionPrompt = "Create me a tailored, short question for this raw fact to be used in a flashcard : "
        print("Creating answerArray...")
        answerArray = rawInfo  # <-- change this line
        print("Answer array created!")
        questionsArray = []
        print("Creating questionArray...")
        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))  
            print(f"question created and appended!") 
        return questionsArray, answerArray
    
test = FlashcardModelV1()


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

rawFacts = """16. {Designing divisions requires a trade-off between firepower and staying power.}17. {Primary attacking units should emphasize firepower, while defensive units should emphasize staying power.}18. {Germany should focus on a strong attack in the early game.}19. {France and Great Britain are unlikely to sit idle in the early game.}1. {Germany invaded Poland during World War II}2. {Germany anticipated a quick victory over Poland due to their superior firepower}3. {Germany considered modifying their division template to focus on defensive capabilities if the war started going badly}4. {The Soviet Union faced difficulties in launching offensive operations against Germany due to a wide front and the effects of The Great Purge}5. {The USSR prioritized staying power and manpower to overwhelm the enemy in a defensive war}6. {Divisions with good speed and firepower are useful for encircling the enemy and cutting them off from supply and reinforcements}7. {Tank and motorized units are favored for divisions focused on encirclement}8. {Having only a single line of infantry training is not recommended}9. {A great power should have at least three or four infantry divisions training}10. {In the early game, tank and mobile/mechanized divisions are priorities for Germany and the Soviet Union}11. {The Americans and Japanese should prioritize researching and producing marine units}12. {Close Air Support and Fighters are the best use of aircraft production for Germany and the Soviets}"""
path2 = "C:\\Users\\david\\Desktop\\AlgoCo\\Edukai\\AI models\\Info extractor\\meetingminutes.pdf"
print(test.flashcard_intialise_pdf(path2, 1500))