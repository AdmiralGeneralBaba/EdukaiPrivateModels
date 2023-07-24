from openai_calls import OpenAI
from info_extraction_v1 import InfoExtractorV1
from info_extraction_v1 import SentenceIdentifier

class FlashcardModelV1 : 
    def __init__(self):
        self.gptAgent = OpenAI()
        self.InfoExtraction = InfoExtractorV1()
        self.SentenceIdentifier = SentenceIdentifier()
    def flashcard_intialise_pdf(self, textbook_path):
        questionPrompt = "Create me a tailored, short question for this raw fact to be used in a flashcard : "
        rawInfo = self.InfoExtraction.info_extractor(textbook_path) #creates the raw information
        answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
        return questionsArray, answerArray
    

    def flashcard_intialise_rawText(self, rawInfo):
        questionPrompt = "Create me a tailored, short question for this raw fact to be used in a flashcard : "
        answerArray = [sentence for chunk in rawInfo for sentence in self.SentenceIdentifier.split_into_sentences(chunk)]  # <-- change this line
        questionsArray = []

        for answer in answerArray:
            questionsArray.append(self.gptAgent.open_ai_gpt_call(answer, questionPrompt))   
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

print(test.flashcard_intialise_rawText(rawText))