from difflib import SequenceMatcher
import ssl
from elasticsearch import Elasticsearch
import cardsFactory
import os
import library
from googlesearch import search
import requests
from bs4 import BeautifulSoup

es = Elasticsearch(['http://104.199.118.220:8080'],
                    send_get_body_as='POST',)
SIMILAR_RATE = 0.55


def check_question_db():
    es.indices.delete(index='library.GROUP', ignore=[400, 404])
    for question, property_list in library.QUESTION_DIC.items():
        index = property_list[0]
        answer = property_list[1]
        if len(property_list)==3:
            link = property_list[2]
        else:
            link = None
        data = {
        'question': question,
        'answer': answer,
        'link': link,
        }   
        res = es.index(index=library.GROUP, doc_type='question', id=index, body=data)
    es.indices.refresh(index=library.GROUP)


def search_related_rate(parsed_string):
    related_questions_list = []
    res = es.search(index=library.GROUP, body={"query": {"match_all": {}}})
    for hit in res['hits']['hits']:
        question = hit["_source"]['question']
        if similar(parsed_string,question)>=SIMILAR_RATE:
            related_questions_list.append([question, hit["_id"]])
    return related_questions_list


def similar(stringA, stringB):
    return SequenceMatcher(None, stringA.lower(), stringB.lower()).ratio()


def elasticsearch(parsed_string):
    result_list = []
    res = es.search(index=library.GROUP, body={'query':{ 'match_phrase':{ "question":parsed_string}} })
    for hit in res['hits']['hits']:
        result_list.append([hit["_source"]['question'], hit["_id"]])
    return result_list


def getTheAns(index):
    action_response = 'UPDATE_MESSAGE'
    res = es.get(index=library.GROUP, doc_type='question', id=index)
    if res['_source']['link'] != None:
        return cardsFactory._respons_text_with_bottom_link_card(action_response,res['_source']['question'],res['_source']['answer'], "The link ...", res['_source']['link'])
    else:
        return cardsFactory._respons_text_card(action_response,res['_source']['question'],res['_source']['answer'])  

def google_search(search_data):
    response = dict()
    cards = list()
    widgets = list()
    num = 1
    header = {
    'header': {
    'title': 'Google result for '+search_data,
    'subtitle': 'City of Edmonton chatbot',
    'imageUrl': 'http://www.gwcl.ca/wp-content/uploads/2014/01/IMG_4371.png',
    'imageStyle': 'IMAGE'
    }
    }
    cards.append(header)
    for url in search(search_data, stop=1, only_standard=True):
        title = "Google search result "+str(num)
        widgets.append(
            {'buttons': [{'textButton': {'text': title, 'onClick': {'openLink': {'url': url}}}}]}
        )
        num += 1
    cards.append({ 'sections': [{ 'widgets': widgets }]})
    response['cards'] = cards   
    return response

def main(parsed_string, user_input):
    if parsed_string == "":
        parsed_string = user_input

    search_used = "Elastic"
    result_list = elasticsearch(parsed_string)
    if len(result_list) == 0:
        result_list = search_related_rate(parsed_string)
        search_used = "Keywords"
    return result_list, search_used, library.GROUP
