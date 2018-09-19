# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from apiclient.discovery import build, build_from_document
from flask import Flask, render_template, request, json, make_response
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from rules import getTheAns,CHEER_LIST,QUESTION_DIC,BYE_LIST, DEMO_QUESTION_DIC
from difflib import SequenceMatcher
import NLP

Rules_dic = DEMO_QUESTION_DIC
SIMILAR_RATE = 0.35

app = Flask(__name__)

INTERACTIVE_TEXT_BUTTON_ACTION = "doTextButtonAction"
INTERACTIVE_IMAGE_BUTTON_ACTION = "doImageButtonAction"
INTERACTIVE_BUTTON_PARAMETER_KEY = "param_key"
BOT_HEADER = 'Card Bot Python'

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
        verb_null_string,parsed_string = NLP.main(event_data['message']['text'])
        resp = create_card_response(verb_null_string,parsed_string,event_data['message']['text'],event_data['user']['displayName'])     


    elif event_data['type'] == 'CARD_CLICKED':
        action_name = event_data['action']['actionMethodName']
        parameters = event_data['action']['parameters']
        resp = respond_to_interactive_card_click(action_name, parameters)

    space_name = event_data['space']['name']

    logging.info(resp)

    # Uncomment the following line for a synchronous response.
    return json.jsonify(resp)

    # Asynchronous response version:
    thread_id = None
    if event_data['message']['thread'] != None:
        thread_id = event_data['message']['thread']

    # Need to return a response to avoid an error in the Flask app
    send_async_response(resp, space_name, thread_id)
    return 'OK'

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return render_template('home.html')


def send_async_response(response, space_name, thread_id):
    """Sends a response back to the Hangouts Chat room asynchronously.

    Args:
      response: the response payload
      spaceName: The URL of the Hangouts Chat room

    """

    # The following two lines of code update the thread that raised the event.
    # Delete them if you want to send the message in a new thread.
    if thread_id != None:
        response['thread'] = thread_id
    ##################################

    scopes = ['https://www.googleapis.com/auth/chat.bot']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'service-acct.json', scopes)
    http_auth = credentials.authorize(Http())

    chat = build('chat', 'v1', http=http_auth)
    chat.spaces().messages().create(
        parent=space_name,
        body=response).execute()

def create_card_response(verb_null_string,parsed_string,event_message,user_name):
    """Creates a card response based on the message sent in Hangouts Chat.

    See the reference for JSON keys and format for cards:
    https://developers.google.com/hangouts/chat/reference/message-formats/cards

    Args:
        eventMessage: the user's message to the bot

    """
    
    if event_message.lower() in CHEER_LIST:
        return {
                   'cards': [
                       {
                           'sections': [
                               {
                                   'widgets': [
                                       {
                                           'textParagraph': {
                                               'text': 'Hey! '+user_name+
                                               ' Welcome to Chatbot about Chatbot :D You can ask me chatbot type, opportunities, use cases in industry,'+
                                               ' municipal government, or at the City, my findings and recommendations, next steps.'

                                           }
                                       }
                                   ]
                               }
                           ]
                       }
                   ]
               } 

    elif event_message.lower() in BYE_LIST:
        return {
                   'cards': [
                       {
                           'sections': [
                               {
                                   'widgets': [
                                       {
                                           'textParagraph': {
                                               'text': 'Bye. Thank you very much for chatting with me. Hope the information provided is helpful. Have a nice day!'

                                           }
                                       }
                                   ]
                               }
                           ]
                       }
                   ]
               } 

    
    else:
        related_questions_list=search_highest_rate(verb_null_string)
    
        if (len(related_questions_list)==0):
            return {
                   'cards': [
                       {
                           'sections': [
                               {
                                   'widgets': [
                                       {
                                           'textParagraph': {
                                               'text': 'No result found, please search again.'
                                           }
                                       }
                                   ]
                               }
                           ]
                       }
                   ]
               }        
            
            
        else:
            response = dict()
            cards = list()
            widgets = list()
            header = {
                'header': {
                'title': 'Search result for '+event_message,
                'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
                'imageStyle': 'IMAGE'
                }
            }
            cards.append(header)
            
            for question in related_questions_list:
                widgets.append({
                    'buttons': [{'textButton': {'text': question,'onClick': {'action': {'actionMethodName': INTERACTIVE_TEXT_BUTTON_ACTION,'parameters': [{'key': INTERACTIVE_BUTTON_PARAMETER_KEY,'value': question
                                        }]}}}}]
                })
            
            
            cards.append({ 'sections': [{ 'widgets': widgets }]})
            response['cards'] = cards
            return response
        


def respond_to_interactive_card_click(action_name, custom_params):
    """Creates a response for when the user clicks on an interactive card.

    See the guide for creating interactive cards
    https://developers.google.com/hangouts/chat/how-tos/cards-onclick

    Args:
        action_name: the name of the custom action defined in the original bot response
        custom_params: the parameters defined in the original bot response

    """

    if custom_params[0]['key'] == INTERACTIVE_BUTTON_PARAMETER_KEY:
        question = custom_params[0]['value']
        theAnswer = getTheAns(question)
        return theAnswer
    else:
        action_response = 'UPDATE_MESSAGE'
        return {
        'actionResponse': {
            'type': action_response
        },
        'cards': [
            {
                'sections': [
                    {
                        'widgets': [
                            {
                                'textParagraph': {
                                    'text': 'No result found, please search again.'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

def similar(stringA, stringB):
    return SequenceMatcher(None, stringA.lower(), stringB.lower()).ratio()


def search_highest_rate(verb_null_string):
    related_questions_list = []
    higest_rate = 0
    higest_question = None
    for each_question,each_answer in Rules_dic.items():
        similar_rate = similar(each_question,verb_null_string)
        if higest_rate == 0:
            higest_rate = similar_rate
            higest_question = each_question
        else:
            if similar_rate>higest_rate:
                higest_rate = similar_rate
                higest_question = each_question
    if higest_rate > 0.3:
        related_questions_list.append(higest_question)
    return related_questions_list


def search_related_rate(verb_null_string):
    for each_question,each_answer in Rules_dic.items():
        if similar(each_question,verb_null_string)>=SIMILAR_RATE:
            related_questions_list.append(each_question)
    return related_questions_list