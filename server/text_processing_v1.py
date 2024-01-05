from info_extractor_v4 import InfoExtractorV4

# Takes in a raw list of string, puts it inside a new long string, renumbers it, then appends it to a dictionary with the key value 'lesson_facts' : 
def process_text(text) : 
    lesson = {}
    info_extractor = InfoExtractorV4()
    new_string = ' '.join(text)
    renumbered_facts = info_extractor.renumber_facts(new_string)
    lesson["lesson_facts"] = renumbered_facts
    return lesson


# Takes in text, does info extraction on it, then renumbers the facts
async def text_fact_transformer_V1(text) : 
    info_extractor = InfoExtractorV4()
    fact_chunks = await info_extractor.text_info_extractorV4(text, 1200)
    lesson = process_text(fact_chunks)
    return lesson


 