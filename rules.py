import cardsFactory

QUESTION_DIC = {
    "View jobs in 'To Do List'": 1, 
    'Multiple Address Search using Map': 2,
    'Different colours for different jobs': 3,
    'Assign an inspection/process to nobody': 4
}  

DEMO_QUESTION_DIC = {
    "Chatbot type": 100, 
    'Opportunities': 200,
    'Use cases in industry': 300,
    'Municipal government': 400,
    'Findings and recommendations': 500,
    'Benefits': 600,
    'Use cases for COE':700,
    'Next steps':800

}       

CHEER_LIST=['hi','hello','how are you?','how are you']
BYE_LIST=['thank you','goodbye','bye']



def getTheAns(question):
    AnsNum = DEMO_QUESTION_DIC[question]
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

    elif AnsNum == 100:
        theAnswer = "There are three chatbot types: informational, transactional, and advisory. For example, asking for bus schedule is informational. Paying pet license fee is transactional, which usually requirs identity verification. Understanding your interests and providing suggestions on the weekend recreational activities is advisory." 
        return cardsFactory._respons_text_card(action_response,question,theAnswer)  

    elif AnsNum == 200:
        theAnswer = ("Online chat is just another service channel besides in-person, telephone, text, web, and App channels.\n"
            "Online chat has existed for many years but is not as popular as today because it requires extra customer service representatives available to answer questions instantly.\n" 
            "The City didn't offer the online chat service to the citizen and employee because it requires significant extra FTEs which the City cannot afford.\n" 
            "With the new natural language processing and machine learning technologies, intelligent online chat robot(Chatbot)becomes feasible and industries adopt Chatbot quickly(e.g. Fido, ATB, etc).\n"
            "The City of Edmonton has the opportunity to offer the online chat service to the citizen and employee with much less required extra FTEs."
            "Gartner published an articles in August, 2017, stating:\n"
            "By 2020, 25 percentage of customer service and support operations will integrate virtual customer assistant technology across engagement channels.\n"
            "Citizens have a growing expectation of being able to access government services via conversational applications. \n"
            "However, most government services, particularly those that involve care or case management, will require human involvement for the foreseeable future.\n"
            ) 
        return cardsFactory._respons_text_card(action_response,question,theAnswer)  


    elif AnsNum == 300:
        theAnswer = ("Online chat is just another service channel besides in-person, telephone, text, web, and App channels. Typical use cases of Chatbot could be found in the following industries:\n"
                    "Financial Services\n"
                    "Insurance\n"
                    "HR\n"
                    "Retail & E-commerce\n"
                    "Healthcare\n"
                    "News & Publishing\n"
                    "Media & Entertainment\n"
                    "Fashion & beauty\n"
                    "Travel\n"
                    "Food\n"
                    "You can find use case types from this great article:")
        return cardsFactory._respons_text_with_bottom_link_card(action_response,question,theAnswer, "The article ...", "https://blog.ideas2it.com/50-chatbot-use-cases/")

    elif AnsNum == 400:
        theAnswer = ("Many municipal governments adopted and tested Chatbot for both internal and public services. For example,\n"
                    "San Francisco: internal procurement Chatbot\n"
                    "Kansas: Open Data Chatbot\n"
                    "Los Angeles: business opportunity Chatbot\n"
                    "Dubai: Chatbot for request inquiry and bill payment\n"
                    "Singapore: a Facebook messenger chatbot for news and policies\n"
                    "London, UK: bus information Chatbot\n"
                    "Maharashtra, India: a generic Chatbot for complaint registration, online services, tax filing, health issues, finance, driving license info, etc.\n"
                    "North Charleston: 311 Chatbot\n"
                    "You can find municipality use case details from this great article:\n" )

        buttonText = "The article ..."
        buttonUrl = "https://blog.vsoftconsulting.com/blog/15-governments-agencies-that-use-chatbots"
        return cardsFactory._respons_text_with_bottom_link_card(action_response,question,theAnswer, buttonText, buttonUrl)

    elif AnsNum == 500:
        theAnswer = ("Start with specific chatbots (eg. POSSE or Google support) to build internal expertise and explore different technologies. Specific chatbot is easy to implement and can provide expected user experiences")
        return cardsFactory._respons_text_card(action_response,question,theAnswer)  


    elif AnsNum == 600:
        theAnswer = ("Here are just some general benefits to citizens:\n"
                    "1. Citizens can get a quick access to public data.\n"
                    "2. They can submit complaint request online.\n"
                    "3. Form submission can be done through the bot.\n"
                    "4. Citizens can pay tax and bills online.\n"
                    "5. It will also help people save time.\n"
                    "6. People can get assistance in their native language.\n"
                    "7. Helps people to get rid of a traditional way of communication through phone calls and emails.\n"

                    "Benefits to Government Agencies:\n"
                    "1. Addressing citizen issues made easy.\n"
                    "2. Delivering public services made easy.\n"
                    "3. The Government can provide 24/7 availability and high accessibility to citizens.\n"
                    "4. They can decrease dedicated workload and time for responses.\n"
                    "5. Easy integration and management, hence inexpensive.\n"
                    "6. Government can provide multilingual support.\n"
                    "7. Chatbots are omni-channel. Hence people can get support on multiple platforms.\n")
        return cardsFactory._respons_text_card(action_response,question,theAnswer)

    elif AnsNum == 700:
        theAnswer = "There are three types of use cases at City of Edmonton. \n1) generic chatbot: 311, inside information; \n2) specific chatbot: ETS bus schedule, Google support, SAP support; \n3) something in between: ETS, IT, HR, procurement." 
        return cardsFactory._respons_text_card(action_response,question,theAnswer)  
    elif AnsNum == 800:
        theAnswer = "1) Start to build a chatbot for POSSE, Google and other Chatbot-ready support teams. \n2) Engage business areas to explore the Chatbot opportunities." 
        return cardsFactory._respons_text_card(action_response,question,theAnswer)     