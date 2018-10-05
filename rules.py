import cardsFactory
# Different dics for different usage 
DEMO_QUESTION_DIC = {
    "Chatbot type": 100, 
    'Opportunities for COE': 200,
    'Use cases in industry': 300,
    'Use cases in municipal government': 400,
    'Recommendations for COE': 500,
    'Benefits for COE': 600,
    'Use cases for COE':700,
    'Next steps':800
}       
# Global varables for the Chatbot 
QUESTION_DIC = DEMO_QUESTION_DIC
CHEER_LIST=['hi','hello','how are you?','how are you','Hi JacksonBot']
BYE_LIST=['thank you','goodbye','bye']
# Global varables for the Chatbot 


def getTheAns(question):
    AnsNum = QUESTION_DIC[question]
    action_response = 'UPDATE_MESSAGE'

    if AnsNum == 100:
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