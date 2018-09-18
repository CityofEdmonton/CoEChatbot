question_dic = {
    "View jobs in 'To Do List'": 1, 
    'Multiple Address Search using Map': 2,
    'Different colours for different jobs': 3,
    'perform a Job Search by Addres on one or more address/units': 4
}       
questions_list = ["View jobs in 'To Do List'", 
        'Multiple Address Search using Map',
        'Different colours for different jobs']


def getTheAns(question):
    AnsNum = question_dic[question]
    action_response = 'UPDATE_MESSAGE'
    if AnsNum == 1:     
        return {
                'actionResponse': {
                    'type': action_response
                },
                "cards": [
                {
                'header': {
                    'title': question,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
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

    elif AnsNum == 2:   
        return {
                'actionResponse': {
                    'type': action_response
                },
                "cards": [
                {
                'header': {
                    'title': question,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
                }
                },

                {
                "sections": [
                    {
                    "widgets": [
                        {
                        "buttons": [
                            {
                             "textButton": {
                                "text": "To do this in POSSE Web...",
                                "onClick": {
                                  "openLink": {
                                    "url": "https://drive.google.com/file/d/0B-Bvudy6vrgkbUk0dUZNYWJPVFU/view"
                                  }
                                }
                              }
                            }
                         ]
                        
                        }
                ]
            }
            ]
        }
        ]
        }

    elif AnsNum == 3:     
        return {
                'actionResponse': {
                    'type': action_response
                },
                "cards": [
                {
                'header': {
                    'title': question,
                    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                    'imageStyle': 'IMAGE'                 
                }
                },                      
                {
                "sections": [
                        {
                "widgets": [
                {
                    "textParagraph": {
                    "text": "This function can't be performed in POSSE Web (Winchester)" 
                    }
                }
            ]
            }
            ]
            }
            ]
        }

