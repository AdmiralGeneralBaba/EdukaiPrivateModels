# EdukaiPrivateModels
- PRIVATE EYES ONLY - THIS MUST BE KEPT SECRET AT ALL COSTS
- As of 29/07/2023, it can create (based on a inputted PDF) : 

- Flashcards 
- Powerpoint slide content (Picture search query, content, titles etc)
- Homework (based on lesson facts)
- Yearly lesson facts to learn per lesson
- Exam paper (aqa eng lang paper 1)


Aim to add in :
- Homework marker (hard)
- Lesson planner help (medium)
- Textbook summarisation (easy)
- Enhanced powerpoint creator (hard)
- Level based, personalisation for students (hard)
- Personal tutor AI - uses domain specific knowledge to act as a tutor for a student (hard)



Things to do with the code AS OF 29/07/2023 : 
1. Create the flashcard model again - have it not have to call a function for every specific fact DONE 
2. Create the 'homework_creator' method, that only creates homework for one lesson in the yearly lesson facts assigner. 
3. Need to import the 'powerpoint_creator' into the yearly_plan_ai_models. 
4. have a function call, of GPT-3.5 for a brief description of the lesson based on their facts. Have it be a dictionary/tuple, where 'description : {description}' and 'facts {facts}', returned in a JSON format, so that the user can see the desciption of each lesson, and choose which one they want to create. 

