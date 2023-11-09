from info_extractor_v4 import InfoExtractorV4

# Takes in a raw list of string, puts it inside a new long string, renumbers it, then appends it to a dictionary with the key value 'lesson_facts' : 
def process_text(text) : 
    lesson_dict = {}
    info_extractor = InfoExtractorV4()
    new_string = ' '.join(text)
    renumbered_facts = info_extractor.renumber_facts(new_string)
    lesson_dict["lesson_facts"] = renumbered_facts
    return renumbered_facts