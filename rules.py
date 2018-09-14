question_dic = {
    "View jobs in 'To Do List'": 1, 
    'Where is the Pictometry button on the map?': 2,
    'How can I avoid sifting through menus to find regularly used search.': 3
}       
questions_list = ["View jobs in 'To Do List'", 
        'Where is the Pictometry button on the map?',
        'How can I avoid sifting through menus to find regularly used search.']


def getTheAns(question):
    print(question)
    AnsNum = question_dic[question]
    print(AnsNum)
    action_response = 'UPDATE_MESSAGE'
    if AnsNum == 1:     
        return {
                'actionResponse': {
                    'type': action_response
                },
                "cards": [
                {
                'header': {
                    'title': question
                 
                }
                },                      
                {
                "sections": [
                        {
                "widgets": [
                {
                    "textParagraph": {
                    "text": "By default you only see jobs that are scheduled before the current date.\n" 
                    "Job that have a future scheduled date are not displayed. To display these jobs follow these simple steps:\n"
                    "1. Open the 'To Do List'\n"+
                    "2. Click the criteria button\n"+
                    "3. Uncheck the 'Current Only' checkbox\n"+
                    "4. Now all you jobs are displayed\n"
    
                    }
                }
            ]
            }
            ]
            }
            ]
        }



getTheAns("View jobs in 'To Do List'")