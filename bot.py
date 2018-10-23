# Copyright 2017 Google Inc.

import datetime
import logging
import library
import nlp
import cardsFactory
import database_logger
import search
import os
import MySQLdb
import smtplib

from apiclient.discovery import build, build_from_document
from flask import Flask, render_template, request, json, make_response
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from difflib import SequenceMatcher

app = Flask(__name__)

INTERACTIVE_TEXT_BUTTON_ACTION = "doTextButtonAction"
INTERACTIVE_IMAGE_BUTTON_ACTION = "doImageButtonAction"
INTERACTIVE_BUTTON_PARAMETER_KEY = "param_key"


@app.route('/', methods=['POST'])
def home_post():
    """Respond to POST requests to this endpoint.
    All requests sent to this endpoint from Hangouts Chat are POST
    requests.
    """
    event_data = request.get_json()
    resp = None

    # If the bot is removed from the space, it doesn't post a message
    # to the space. Instead, log a message showing that the bot was removed.
    if event_data['type'] == 'REMOVED_FROM_SPACE':
        logging.info('Bot removed from  %s' % event_data['space']['name'])
        return 'OK'

    elif event_data['type']  == 'ADDED_TO_SPACE' and event_data['space']['type'] == 'ROOM':
        resp = { 'text': ('Thanks for adding me to {}!'
            .format(event_data['space']['name'])) }

    elif event_data['type']  == 'ADDED_TO_SPACE' and event_data['space']['type'] == 'DM':
        resp = { 'text': ('Thanks for adding me to a DM, {}!'
            .format(event_data['user']['displayName'])) }

    elif event_data['type'] == 'MESSAGE':
        old_question, respons = database_logger.check_log_question_tem(event_data['user']['displayName'])
        if old_question is None:
            question = clean_message(event_data['message']['text'])
            verb_noun_string, verb_list, noun_list = nlp.main(question)
            resp = create_card_response(verb_noun_string, verb_list, noun_list, question,event_data['user']['displayName'])
        else:
            database_logger.delete_log_question_tem(event_data['user']['displayName'], old_question)
            if respons == 'ask':
                resp = create_group_card_respons(old_question,event_data['message']['text'],event_data['user']['displayName'], event_data['user']['email'])

            elif respons == 'add':
                resp = create_addquestion_card_respons(old_question,event_data['message']['text'],event_data['user']['displayName'], event_data['user']['email'])

            elif respons == 'email':
                resp = create_email_respons(old_question,event_data['message']['text'],event_data['user']['displayName'], event_data['user']['email'])

    elif event_data['type'] == 'CARD_CLICKED':
        action_name = event_data['action']['actionMethodName']
        parameters = event_data['action']['parameters']
        user = event_data['user']['displayName']
        user_email = event_data['user']['email']
        print(event_data['user'])
        resp = respond_to_interactive_card_click(action_name, parameters, user, user_email)

    logging.info(resp)

    return json.jsonify(resp)


@app.route('/', methods=['GET'])
def home_get():
    return render_template('home.html')


def create_card_response(verb_noun_string, verb_list, noun_list, event_message, user_name):
    """Creates a card response based on the message sent in Hangouts Chat.
    """
    question_from_user = event_message.encode('utf-8')

    parsed_key_words = verb_noun_string.encode('utf-8')

    pre_defined_question = check_pre_defined_questions(question_from_user, user_name, parsed_key_words)

    if pre_defined_question is not None:
        return pre_defined_question

    else:
        related_questions_list=[]
        related_questions_list, search_used, group = search.main(parsed_key_words, question_from_user)

        if (len(related_questions_list)==0):
            database_logger.logging_to_database(user_name, question_from_user,"NOT FOUND",parsed_key_words, "Null", "Null")
            return search.google_search(question_from_user)

        elif (len(related_questions_list)==1): 
            for each_list in related_questions_list:
                question = each_list[0]
                index = each_list[1]
            theAnswer = search.getTheAns(index, None)
            database_logger.logging_to_database(user_name, question_from_user,related_questions_list,parsed_key_words, search_used, group)
            return theAnswer

        else:
            response = dict()
            cards = list()
            widgets = list()
            header = {
                'header': {
                'title': 'Search result for '+ question_from_user,
                'subtitle': 'City of Edmonton chatbot',
                'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                'imageStyle': 'IMAGE'
                }
            }
            cards.append(header)
            
            for each_list in related_questions_list:
                question = each_list[0]
                index = each_list[1]
                widgets.append(
                {'buttons': [{'textButton': {'text': question,'onClick': {'action': {'actionMethodName': INTERACTIVE_TEXT_BUTTON_ACTION,'parameters': [{'key': INTERACTIVE_BUTTON_PARAMETER_KEY,'value': index}]}}}}]
                })
            cards.append({ 'sections': [{ 'widgets': widgets }]})
            response['cards'] = cards
            database_logger.logging_to_database(user_name, question_from_user,related_questions_list,parsed_key_words, search_used, group)
            return response
 
def create_email_respons(question,event_message,user_name, user_email):
    """Creates an email card response based on the message sent in Hangouts Chat.
    """
    email_description = clean_message (event_message)
    headertitle = 'Email preview'
    headerimage = 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png'
    button1text = 'Send now!'
    button2text = 'No, I will search again.'
    button1value = 'Email_from: '+ user_name + '\nEmail address: '+user_email+'\nQuestion: '+ question +'\nDescription: '+ email_description
    button2value = 'didnt_help'
    text1 = 'Question: '+ question
    text2 = 'Description: '+ email_description
    return cardsFactory._text_card_with_two_buttons(headertitle, headerimage, text1, text2, button1text, button2text, button1value, button2value)     

def create_group_card_respons(question,event_message,user_name, user_email):
    """Creates a issue preview card response based on the message sent in Hangouts Chat.
    """
    issue_discription = clean_message (event_message)
    headertitle = 'Issue preview'
    headerimage = 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png'
    button1text = 'Ask now!'
    button2text = 'No, I will search again.'
    button1value = 'ask_team'
    button2value = 'didnt_help'
    text1 = 'Question: '+ question
    text2 = 'Description: '+ issue_discription
    return cardsFactory._text_card_with_two_buttons(headertitle, headerimage, text1, text2, button1text, button2text, button1value, button2value)    

def create_addquestion_card_respons(question,event_message,user_name, user_email):
    """Creates a question preview card response based on the message sent in Hangouts Chat.
    """
    answer_and_link = clean_message (event_message)
    data = answer_and_link.split('link:')
    answer = data[0]
    try:
        link = data[1]
    except Exception:
        link = 'Null'

    headertitle = 'Question preview'
    headerimage = 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png'
    button1text = 'Add now!'
    button2text = 'No, I will add later.'
    button1value = question + ' add_question ' + answer + 'add_link' + link
    button2value = 'dont_add'
    text1 = 'Question: '+ question
    text2 = 'Answer: '+ answer +'\nLink: '+ link
    return cardsFactory._text_card_with_two_buttons(headertitle, headerimage, text1, text2, button1text, button2text, button1value, button2value)   

def respond_to_interactive_card_click(action_name, custom_params,user, user_email):
    """Creates a response for when the user clicks on an interactive card.
    """
    if custom_params[0]['key'] == INTERACTIVE_BUTTON_PARAMETER_KEY:
        index = custom_params[0]['value']
        try:
            int(index)
            theAnswer = search.getTheAns(index, 'UPDATE_MESSAGE')
            database_logger.update_selected_answer(user, index)
            return theAnswer

        except Exception: 
            value = str(index)

            if value =='ask_team': 
                text = "Hi "
                for support_staff in library.SUPPORT_USER_ID:
                    text += support_staff
                text += "! Could you please help the issue above!"
                return {'text': text}

            elif ' add_question ' in value: 
                question_answer = value.split(' add_question ')
                question = question_answer[0]
                answer_link = question_answer[1]
                answer_link_list= answer_link.split(' add_link ')
                answer = answer_link_list[0]
                link = answer_link_list[1]
                search.add_question_to_db(question, answer, link)
                headertitle = 'Add question to DB'
                text = "Just added! \nQuestion: "+question+"\nAnswer: "+answer
                return cardsFactory._respons_text_card('UPDATE_MESSAGE',headertitle, text)

            elif 'Email_from: 'in value:
                sent = send_email(value, user_email)
                if sent:
                    return cardsFactory._respons_text_card('UPDATE_MESSAGE',"Create Remedy ticket", "Sent! Our support staff will contact you shortly.")
            if value == 'didnt_help':
                return cardsFactory._respons_text_card('UPDATE_MESSAGE',"Sorry...", "Sorry for didn't help you. ")

            elif value == 'dont_add':
                return cardsFactory._respons_text_card('UPDATE_MESSAGE',"Cancel adding", "Adding question canceled.")

            else:
                database_logger.log_question_tem(user, value, 'ask')
                return cardsFactory._respons_text_card('UPDATE_MESSAGE', value, "Pleas type in your question description now ... ")


def clean_message (event_message):
    if ' @JacksonBot ' in event_message:
        return event_message.replace(' @JacksonBot ','')
    elif ' @JacksonBot' in event_message:
        return event_message.replace(' @JacksonBot','')
    elif '@JacksonBot ' in event_message:
        return event_message.replace('@JacksonBot ','')
    elif 'JacksonBot' in event_message:
        return event_message.replace('JacksonBot','')
    else:
        return event_message


def check_pre_defined_questions(question_from_user, user_name, parsed_key_words):
    for word in library.CHEER_LIST:
        if search.similar(question_from_user, word)>=0.7:
            text = ("Hey! "+user_name+" Thank you for talking to Chatbot about Chatbot :D Please type <b>'help'</b> to get the list of questions I could answer for now!")
            headertitle = 'Hi~'
            headerimage = 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png'
            widgetimage = 'https://media1.tenor.com/images/9ea72ef078139ced289852e8a4ea0c5c/tenor.gif?itemid=7537923'
            database_logger.logging_to_database(user_name, question_from_user,"CHEER",parsed_key_words, "Null", "Null")
            return cardsFactory._text_card_with_image(headertitle, headerimage,text, widgetimage)

    for word in library.BYE_LIST:
        if search.similar(question_from_user, word)>=0.7 or word.lower() in question_from_user.lower():
            text = 'Bye~ Thank you very much for chatting with me. Hope the information provided is helpful. Or, you can leave your feedback here! Have a nice day!'
            headertitle = 'Bye~'
            headerimage = 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png'
            widgetimage = 'https://img.buzzfeed.com/buzzfeed-static/static/2017-01/17/16/asset/buzzfeed-prod-fastlane-01/anigif_sub-buzz-20527-1484687195-4.gif'
            database_logger.logging_to_database(user_name, question_from_user,"BYE",parsed_key_words, "Null", "Null")
            return cardsFactory._text_card_with_image(headertitle, headerimage,text, widgetimage)

    if question_from_user == "help":
        text = ("At this moment, you could ask me the top 70 questions from this website:\n https://www.mondovo.com/keywords/most-asked-questions-on-google\n")
        headertitle = 'Help'
        database_logger.logging_to_database(user_name, question_from_user,"HELP",parsed_key_words, "Null", "Null")
        return cardsFactory._text_card(headertitle, text)   

    elif question_from_user == "jackson_check_db" and user_name in library.ADMIN:
        search.check_question_db()
        headertitle = 'Admin readonly'
        database_logger.logging_to_database(user_name, "Elastic update","admin",parsed_key_words, "Null", "Null")
        return cardsFactory._text_card(headertitle, "Done!")

    elif "add_question" in question_from_user and user_name in library.ADMIN:
        question = question_from_user.replace('add_question:','')
        database_logger.log_question_tem(user_name, question, 'add')
        return cardsFactory._text_card(question, "Pleas type in the answer now ... ")
    
    else:
        return None

 