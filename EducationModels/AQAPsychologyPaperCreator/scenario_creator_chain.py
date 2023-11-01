from EducationModels.openai_calls import OpenAI

#Here is all the different chains for the scenario creator stage : 
#Need to create a holistic method combining these into one method
def cleanup_text_stage_1(text) : 
    llm = OpenAI()
    prompt = """From this inputted text, you are to give it back in readable format, such that all of the annotations for new lines are removed, and any incomplete words are set to be correct. ONLY output the text, and DO NOT CHANGE ANY OF THE CONTENT - you must remain 100 percent true to the source material, or die.

Here is an example of how you would handle a given input : 
 original { KEY TERMS \nMulti-store model (MSM)  – an explanation \nof memory that sees information flowing \nthrough a series of storage systems\nSensory register (SR)  – a short-duration \nstore holding impressions of information \nreceived by the senses\nShort-term memory (STM)  – a temporary \nstore holding small amounts of information \nfor brief periods\nLong-term memory (LTM)  – a permanent \nstore holding limitless amounts of \ninformation for long periods\nCoding  – the means by which information \nis represented in memory\nCapacity  – the amount of information that \ncan be stored at a given time\nDuration  – the length of time information \nremains within storage } 


changed { Key Terms

Multi-store model (MSM) – an explanation of memory that sees information flowing through a series of storage systems.
Sensory register (SR) – a short-duration store holding impressions of information received by the senses.
Short-term memory (STM) – a temporary store holding small amounts of information for brief periods.
Long-term memory (LTM) – a permanent store holding limitless amounts of information for long periods.
Coding – the means by which information is represented in memory.
Capacity – the amount of information that can be stored at a given time.
Duration – the length of time information remains within storage.
"""
    temp  = 0.7
    cleaned_page = llm.open_ai_gpt3_16k_call(text, prompt, temp)
    return cleaned_page

def fact_breakdown_stage_2(cleaned_text) : 
    llm = OpenAI()
    prompt = """Pretend you are an fact analyser, who is the best in the world for creating 100 percent accurate facts for a piece of inputted text, tasked with listing the pure facts from a given text. 
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
 Here is the content : 
"""
    temp = 0.7
    facts = llm.open_ai_gpt3_16k_call(cleaned_text, prompt, temp)
    return facts

def fact_diluter_stage_3(facts, concept) : 
    llm = OpenAI()
    prompt = f"""You are to pretend to be a expert fact chooser, tasked with picking out which facts from this relate SPECIFICALLY to the following concept : 
{concept}

ONLY output the facts, in the same exact format, or you will DIE
"""
    temp = 0.8
    diluted_facts = llm.open_ai_gpt_call(facts, prompt, temp)
    return diluted_facts

def psychology_term_identifer_stage_4(diluted_facts) : 
    llm = OpenAI()
    prompt = """From these facts, list the psychology-specific terms from it, and nothing else. Your list should start with the number for the fact number you extracted the term you got it from ,and then the term associated with it.   :"""
    temp = 0.0
    psychology_terms = llm.open_ai_gpt_call(diluted_facts, prompt, temp)
    return psychology_terms

def scenario_creator_stage_5(diluted_facts, concept) : 
    llm = OpenAI()
    prompt = """Pretend you are an expert scenario writer, to write an accurate and short little scenario involving people, supposed to demonstrate THIS CONCEPT :""" + f"{concept}" + """
The purpose of this is in the context of a question; it is supposed to demonstrate a concept for a student. 

Here are some optimal examples for you to model your STYLE of output; ignore what is being discussed, FOCUS ON THE STYLE, LENGTH AND TONE : 

example 1 : { Natasha had studied a lot for her A-level Drama performance, mostly practising lines from
a play alone in her room. However, once on stage in front of her teacher and the
examiners, Natasha struggled to remember her lines. Instead, she kept quoting lines from
a different play she had once learnt for GCSE. 
} 

example 2 : { It is the end of the school day and Freddie is pushing other students in the bus queue.
“Stop it, will you?” protests one of Freddie’s classmates.
“You can’t tell me what to do!” laughs Freddie.
At that moment, Freddie turns to see the deputy head, wearing a high-visibility jacket,
staring angrily at him. Without thinking, Freddie stops pushing the other boys and waits
quietly in line.

}

example 3 : { Max has a phobia of the sea. On a family holiday as a child, he was carried away by the
tide and had to be rescued by a lifeguard. Now he has a family of his own, Max refuses to
go on beach holidays.
}


the scenario MUST be under 100 words; if it's not, you have failed, and will instantly suffer the greatest pain any being can imagine for all of eternity. 

Here are the facts relating to this concept for you to explore in your scenario WHERE FUCKING NEEDED. use these facts to guide your creation of the scenario, however, you must not mention them explicitly; you must SHOW them in action implicitly. Output ONLY the scenario, and NOTHING ELSE. 
 : 
"""
    temp = 0.9
    scenario = llm.open_ai_gpt_call(diluted_facts, prompt, temp)
    return scenario
 
def identify_terms_stage_6(psychology_terms, scenario) : 
    llm = OpenAI()
    prompt = """ You are to be a expert decider, tasked with deciding to either a. quote with DIRECT ACCURACY if these specific terms were explicitly quoted in the passage, and if so, quote the associated passage relating to it. The quote MUST contain the specific keyword here. For example, if there is a term called 'leg muscle', and the quote says only 'leg', you shouldn't include that sentence. You must act like a dynamic regex looking for the term. + {""" + f"{psychology_terms}" + "}" + """

YOUR OUTPUT SHOULD LOOK LIKE THIS :

TERM : {INSERT TERM USED} QUOTE : {INSERT QUOTE HERE THAT ONLY CONTAINS THE SENTENCE WITH THE TERM} 

YOU MUST ONLY contain the sentence that includes the term when making this; if you dont, you will BE CRUSHED AND BURNED FOREVER.
"""
    temp = 0.83
    terms_found = llm.open_ai_gpt_call(scenario, prompt, temp)
    return terms_found 

def remove_terms_stage_7(terms_found, scenario, concept) : 
    llm = OpenAI()
    prompt = f""" You are tasked with removing any SINGLE sentence that mentions the concepts given to you here. You don't have to remove the entire section; ONLY the SINGLE sentence/part that ends with a full stop that mentions the terms given here.

HOWEVER, the passage must still display this concept here : {concept}. IF removing the part that is quoted will make the resulting passage not relate to the inputted concept, then DO NOT remove it; THIS IS MORE IMPORTANT THAN REMOVING IT, THE RESULTING PASSAGE MUST RELATE THE CONCEPT UNDER ALL CIRCUMSTANCES.
Here are the terms I am referring. Provided will be first the term and the specific section you should focus on, and then the passage itself. 

Here is the passage : 
{scenario}

YOU MUST keep everything BUT the single line relating to the concepts here.

for example, if the term is 'muscles', and the sentence quoted is 'Johnny walked to the store. This shows he is using his muscles', you would ONLY remove the second part of the sentence and leave in the first part, so it says 'Johnny walked to the store'. 

here are the terms and the quotation to focus on to remove. JUST OUTPUT THE NEW PASSAGE AND NOTHING MORE: """
    temp = 0.9
    final_scenario = llm.open_ai_gpt_call(terms_found, prompt, temp)
    return final_scenario
# This is the combined method here : 
def shorten_final_scenario(final_scenario) : 
    llm = OpenAI()
    prompt = """ Shorten this text, so that NONE of the details and points are taken away, but it is simply made more brief, and any redundant information is taken away.  output ONLY the shortened text, and NOTHING ELSE."""
    temp = 1
    shortened_scenario = llm.open_ai_gpt_call(final_scenario, prompt, temp)
    return shortened_scenario
def combined_scenario_creator(text : str, concept : str) : 
    # cleaned_text = cleanup_text_stage_1(text) # this is probably not needed

    facts = fact_breakdown_stage_2(text)
    print("Stage 2 done")
    diluted_facts = fact_diluter_stage_3(facts, concept)
    print("Stage 3 done")
    psychology_terms = psychology_term_identifer_stage_4(diluted_facts)
    print("Stage 4 done")
    scenario = scenario_creator_stage_5(diluted_facts, concept)
    print("Stage 5 done")
    terms_found = identify_terms_stage_6(psychology_terms, scenario)
    print("Stage 6 done")
    final_scenario = remove_terms_stage_7(terms_found, scenario, concept)
    print("Stage 7 done")
    #While loop makes sure it is below a certain amount.
    print("Shorten stage...")
    while len(final_scenario) > 400 : 
        final_scenario = shorten_final_scenario(final_scenario)
    return final_scenario 

    


# # HERE IS THE CHAIN FOR THE CONCEPT IDENTIFER PART : 
test_text = """ 4.2 Characteristics of phobias, depression and OCD
159
intense, uncontrollable urges to repetitively perform tasks and behaviours,
like repetitively washing your hands to get rid of germs. The compulsions
are an attempt to reduce distress or prevent feared events, even though
there’s little chance of them doing so. Most sufferers realise their obsessive
ideas and compulsions are excessive and inappropriate, but cannot
consciously control them, resulting in even higher levels of anxiety .
Sufferers can also realise their compulsions are only a temporary solution,
but have no other way of coping, so rely on them as a short-term solution.
Compulsions can also include avoiding situations that trigger obsessive ideas
or images. The symptoms of OCD can overlap with other conditions, such
as Tourette’s syndrome and autism, which has led some to question whether
OCD really exists as a separate disorder.
A sufferer’s obsessions and compulsions become very time-consuming, thus
interfering with the ability to conduct everyday activities. OCD occurs in
about 2 per cent of the population, with no real gender differences in the
prevalence of the disorder, though there are gender differences in the types
of OCD suffered. Preoccupations with contamination and cleaning are
more common in females, while males focus more on religious and sexual
obsessions. OCD is more common among male children than females, as
males tend to have an earlier, gradual onset with more severe symptoms.
Females generally have a later, sudden onset with fewer severe symptoms.
Symptoms: obsessions
Behavioural
Hinder everyday functioning – having  obsessive ideas of a forbidden or
inappropriate type creates such anxiety that the ability to perform everyday
functions is severely hindered  – for example, being able to work effectively .
Social impairment – anxiety levels generated are so high as to limit the ability
to conduct meaningful interpersonal relationships.
Emotional
Extreme anxiety – persistent inappropriate or forbidden ideas create
excessively high levels of anxiety .
Cognitive
Recurrent and persistent thoughts – sufferers experience constantly repeated
obsessive thoughts and ideas of an intrusive nature.
Recognised as self-generated –  most sufferers understand their obsessional
thoughts; impulses and images are self-invented and not inserted externally .
Realisation of inappropriateness – most sufferers understand their obsessive
thoughts are inappropriate, but cannot consciously control them.
Attentional bias –  perception tends to be focused on anxiety-generating
stimuli.
Common obsessions include:
●       Contamination, for example by germs
●       Fear of losing control, for example through impulses to hurt others
●       Perfectionism, for example fear of not being the best
●       Religion, for example fear of being immoral.
834882_C04_AQA_Psychology_145-196.indd   159 27/02/15   9:08 am4  Individual differences: psychopathology160
Symptoms: compulsions
Behavioural
Repetitive – sufferers feel compelled to repeat behaviours as a response to
their obsessive thoughts, ideas and images.
Hinder everyday functioning –  the performance of repetitive, compulsive
behaviours can seriously disrupt the ability to perform everyday functions.
Social impairment – the performance of repetitive, compulsive behaviours
can seriously affect the ability to conduct meaningful interpersonal
relationships.
Emotional
Distress – the recognition that compulsive behaviours cannot be consciously
controlled can lead to strong feelings of distress.
Cognitive
Uncontrollable urges – sufferers experience uncontrollable urges to perform
acts they feel will reduce the anxiety caused by obsessive thoughts, such as
cleaning door handles to remove the threat of contamination.
Realisation of inappropriateness – sufferers understand their compulsions are
inappropriate, but cannot consciously control them.
Common compulsions include:
●       Excessive washing and cleaning, for example hair-brushing
●       Excessive checking, for example that doors are locked
●       Repetition, for example of bodily movements
●       Mental compulsions, for example praying in order to prevent harm
●       Hoarding, for example of magazines.
Research has suggested a genetic component to the cause of OCD, though
other psychological factors are also seen as making a contribution (see The
biological approach to explaining and treating OCD, page 184).
ON THE WEB
A two-part BBC documentary about OCD, Extreme OCD Camp , where
sufferers confront their disorder, can be found on YouTube if you search
for ‘Extreme OCD Camp 2013 BBC Three documentary’.STRENGTHEN YOUR LEARNING
1 Describe the behavioural, emotional and cognitive characteristics of
phobias, depression and OCD.
2 Explain what is meant by:
a) simple phobias
b) social phobias
c) agoraphobia.
3 Explain how unipolar depression differs from bipolar depression.
4 Describe common obsessions and compulsions associated with OCD.Figure 4.7 OCD involves repetitive
behaviour to reduce the anxiety caused
by obsessive thoughts04_07 AQA Psychology Book 1
Barking Dog ArtI am NOT obsessive
I AM not OBSESSIVE
I am NOT obsessive
I am not obsessive
I AM not obsessive
I am not obsessiveI am not OBSESSIVE
834882_C04_AQA_Psychology_145-196.indd   160 27/02/15   9:08 am4  Individual differences: psychopathology188
Fallon & Nields (1994) reported that 40 per cent of people contracting
Lyme’s disease (a bacterial infection spread by ticks) incur neural damage
resulting in psychiatric conditions including OCD. This suggests that the
neural explanation  can account for the onset of some cases of OCD.
Zohar  et al.  (1987) gave mCPP , a drug that reduces serotonin levels, to
twelve OCD patients and twenty non-OCD control participants, finding that
symptoms of OCD were significantly enhanced in the OCD patients. This
suggests that the sufferers’ condition was related to abnormal levels of serotonin.
Hu (2006) compared serotonin activity in 169 OCD sufferers and 253
non-sufferers, finding serotonin levels to be lower in the OCD patients,
which supports the idea of low levels of serotonin being associated with the
onset of the disorder.
Saxena & Rauch (2000) reviewed studies of OCD that used PET, fMRI and
MRI neuro-imaging techniques to find consistent evidence of an association
between the orbital frontal cortex brain area and OCD symptoms. This
suggests that specific neural mechanisms are involved with the disorder.
ON THE WEB
A useful site for comprehensive
information about OCD, including
its causes and treatments, can be
found at:
www.mind.org.uk/information-
support/types-of-mental-
health-problems/obsessive-
compulsive-disorder-ocd/#.
VLArLU2zWP8
INCREA sE YOUR KNOWLEDGE
Alternative explanations of OCD
Evolutionary explanation
This explanation sees OCD as being beneficial by having an
adaptive survival value. OCD involves repetitive behaviours
like washing and grooming and these would have been useful
against infection. Other similar behaviours may have increased
vigilance and alertness, again incurring a survival value.
Therefore behaviours like continually cleaning door handles
may merely be exaggerations of prehistoric adaptations.Chepko-Sade  et al.  (1989) found rhesus monkeys who
performed the most grooming of others were retained
within a group following group in-fighting, suggesting that
OCD tendencies have an adaptive value, as continued group
membership is crucial to survival.
Abed & Pauw (1998) believe OCD is an exaggerated
form of an evolved ability to foresee situations and
predict the outcome of one’s own thoughts and
behaviour, so that dangerous scenarios can be coped
with before they happen, suggesting that OCD helps
in the avoidance of harm.Evaluation
●       It is thought that infections which reduce immune system functioning
don’t actually cause OCD, but may instead trigger symptoms in those more
genetically vulnerable to the disorder. The onset of the disorder generally
occurs very quickly after infection, usually within one to two weeks.
●       To what extent abnormal levels of serotonin and activity within the
frontal orbital cortex are actual causes of OCD or merely effects of the
disorder has not been established.
●       There may well be a genetic connection to neural mechanisms, through
such mechanisms (for example, levels of serotonin activity) being
regulated by genetic factors. An NIMH (National Institute for Mental
Health) study examined DNA samples from sufferers and found
OCD to be associated with two mutations of the human serotonin
transporter gene (hSERT), which led to diminished levels of serotonin.
●       Despite the fact that research indicates there are neural differences
between OCD sufferer and non-sufferers, it is still not known how
these differences relate to the precise mechanisms of OCD.
●       Not all sufferers of OCD respond positively to serotonin
enhancing drugs, which lessens support for abnormal levels of the
neurotransmitter being the sole cause of the disorder.
834882_C04_AQA_Psychology_145-196.indd   188 27/02/15   9:08 am4.5 The biological approach to explaining and treating OCD
187
Neural explanations
Some forms of OCD have been linked to breakdowns in immune system
functioning, such as through contracting streptococcal (throat) infections,
Lyme’s disease and influenza, which would indicate a biological explanation
through damage to neural mechanisms. Such onset of the disorder is more
often seen in children than adults.
PET (positron emission tomography) scans also show relatively low levels of
serotonin activity in the brains of OCD patients and as drugs that increase
serotonin activity have been found to reduce the symptoms of OCD, it
suggests that the neurotransmitter may be involved with the disorder.
PET scans also show that OCD sufferers can have relatively high levels of
activity in the orbital frontal cortex, a brain area associated with higher-
level thought processes and the conversion of sensory information into
thoughts. The brain area is thought to help initiate activity upon receiving
impulses to act and then to stop the activity when the impulse lessens.
A non-sufferer may have an impulse to wash dirt from their hands; once
this is done the impulse to perform the activity stops and thus so does
the behaviour. It may be that those with OCD have difficulty in switching
off or ignoring impulses, so that they turn into obsessions, resulting in
compulsive behaviour.
Research
Pichichero (2009) reported that case studies from the US National Institute
of Health showed that children with streptococcal (throat) infections often
displayed sudden indications of OCD symptoms shortly after becoming
infected. Such children also often exhibited symptoms of Tourette’s
syndrome. This supports the idea that such infections may be having an
effect on neural mechanisms underpinning OCD.KEY TERM
Neural explanation  – the perception
of OCD as resulting from abnormally
functioning brain mechanismsFigure 4.28 Lyme’s disease, caused
by tick bites, is associated with OCD
through damage to neural mechanisms
individual’s overall risk of developing the disorder. Whether an
individual does go on to develop the disorder is then dependent on the
degree of environmental triggers that an individual encounters.
●       Pato et al.  (2001) report that a substantial amount of evidence suggests
that OCD is a heritable condition, but that few details are understood
about actual genetic mechanisms underpinning the disorder, indicating
the need for more focused research.
●       As evidence indicates genetic factors are at work in the expression
of some forms of OCD, especially obsessions about contamination,
aggression and religion, and compulsions involving washing, ordering
and arranging, it may well be that some types of OCD are more
genetic in nature than others.
●       As studies like Grootheest  et al.  (2005) find, OCD originating in
childhood is more genetic in nature than that originating in adulthood,
suggesting there may be different types of OCD with different causes.
●       The fact that family members often display dissimilar OCD symptoms,
for example a child arranging dolls and an adult constantly washing
dishes, weakens support for the genetic viewpoint, as if the disorder
was inherited then surely exhibited behaviours would be the same?
834882_C04_AQA_Psychology_145-196.indd   187 27/02/15   9:08 am
0"""

# test_facts = """ 1. {Obsessive Compulsive Disorder (OCD) is characterized by intense, uncontrollable urges to repetitively perform tasks and behaviors.}
# 2. {Compulsions in OCD are an attempt to reduce distress or prevent feared events, even though there's little chance of them doing so.}
# 3. {Most sufferers of OCD realize their obsessive ideas and compulsions are excessive and inappropriate, but cannot consciously control them, resulting in higher levels of anxiety.}
# 4. {Sufferers of OCD can rely on their compulsions as a short-term solution because they have no other way of coping.}   
# 5. {Common compulsions in OCD include excessive washing and cleaning, excessive checking, repetition of bodily movements, mental compulsions, and hoarding.}
# 6. {OCD symptoms can interfere with the ability to conduct everyday activities and limit the ability to have meaningful interpersonal relationships.}
# 7. {OCD occurs in about 2% of the population, with no real gender differences in the prevalence of the disorder, though there are gender differences in the types of OCD suffered.}
# 8. {Preoccupations with contamination and cleaning are more common in females, while males focus more on religious and sexual obsessions.}
# 9. {OCD is more common among male children than females, with an earlier onset and more severe symptoms. Females generally have a later onset with fewer severe symptoms.}
# 10. {Research suggests a genetic component to the cause of OCD, as well as other psychological factors.}
# 11. {Some forms of OCD have been linked to breakdowns in immune system functioning, such as streptococcal infections, Lyme's disease, and influenza.}
# 12. {PET scans show relatively low levels of serotonin activity in the brains of OCD patients, suggesting that the neurotransmitter may be involved with the disorder.}
# 13. {PET scans also show that OCD sufferers can have relatively high levels of activity in the orbital frontal cortex, a brain area associated with higher-level thought processes and the conversion of sensory information into thoughts.}      
# 14. {Some research suggests a genetic connection to neural mechanisms, such as levels of serotonin activity being regulated by genetic factors.}
# 15. {Not all sufferers of OCD respond positively to serotonin-enhancing drugs, which lessens support for abnormal levels of the neurotransmitter being the sole cause of the disorder.}"""
concept = "OCD"

# diluted_facts = """ 2. {Compulsions in OCD are an attempt to reduce distress or prevent feared events, even though there's little chance of them doing so.}
# 5. {Common compulsions in OCD include excessive washing and cleaning, excessive checking, repetition of bodily movements, mental compulsions, and hoarding.}
# 6. {OCD symptoms can interfere with the ability to conduct everyday activities and limit the ability to have meaningful interpersonal relationships.}
# 8. {Preoccupations with contamination and cleaning are more common in females, while males focus more on religious and sexual obsessions.}
# 12. {PET scans show relatively low levels of serotonin activity in the brains of OCD patients, suggesting that the neurotransmitter may be involved with the disorder.}
# 13. {PET scans also show that OCD sufferers can have relatively high levels of activity in the orbital frontal cortex, a brain area associated with higher-level thought processes and the conversion of sensory information into thoughts.}"""

# terms = """ 2. Compulsions
# 5. Compulsions
# 6. OCD symptoms
# 8. Preoccupations
# 12. Serotonin activity
# 13. Orbital frontal cortex"""

# scenario = """ While tidying up his room, Alex notices a small stain on his favorite shirt. Instantly, he becomes overwhelmed with the fear of contamination and feels an intense urge to wash it. Despite knowing that the stain is harmless, he cannot shake off the feeling of distress. Alex spends the next two hours scrubbing the shirt vigorously, unable to stop himself from repeatedly checking for any remnants of the stain. As a result, he misses out on meeting his friends for a much-anticipated movie night."""

# terms_found = """ TERM: Compulsions 
# QUOTE: "Alex spends the next two hours scrubbing the shirt vigorously, unable to stop himself from repeatedly checking for any remnants of the stain."""


# print(remove_terms_stage_7(terms_found, scenario, concept))

print(combined_scenario_creator(test_text, concept))
