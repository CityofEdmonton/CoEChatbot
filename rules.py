import cardsFactory

QUESTION_DIC = {
    "View jobs in 'To Do List'": 1, 
    'Multiple Address Search using Map': 2,
    'Different colours for different jobs': 3,
    'Assign an inspection/process to nobody': 4
}       

CHEER_LIST=['hi','hello','how are you?']



def getTheAns(question):
    AnsNum = QUESTION_DIC[question]
    action_response = 'UPDATE_MESSAGE'
    if AnsNum == 1:   
        theAnswer = ("By default you only see jobs that are scheduled before the current date.\n"
            "Job that have a future scheduled date are not displayed. To display these jobs follow these simple steps:\n"
            "1. Open the 'To Do List'\n"
            "2. Click the criteria button\n"
            "3. Uncheck the 'Current Only' checkbox\n"
            "4. Now all you jobs are displayed\n")
        return cardsFactory._respons_text_card(action_response,question,theAnswer)

    elif AnsNum == 2:  
        theAnswer =  "To do this in POSSE Web..."
        url =  "https://drive.google.com/file/d/0B-Bvudy6vrgkbUk0dUZNYWJPVFU/view"
        return cardsFactory._respons_textButton_card(action_response,question,theAnswer, url)

    elif AnsNum == 3:
        theAnswer = "This function can't be performed in POSSE Web (Winchester)" 
        return cardsFactory._respons_text_card(action_response,question,theAnswer)     

    elif AnsNum == 4:
        theAnswer = ("If you want to assign an inspection to nobody you just have to remove the person on that process.\n"
                     "1. Open the job and then the specific process that you want unassigned\n"
                     "2.Remove anybody that is on the process\n"
                     "3.Click the checkbox beside the person's name\n"
                     "4.Click the remove button\n"
                     "5.Done\n")
        
        return cardsFactory._respons_text_card(action_response,question,theAnswer) 