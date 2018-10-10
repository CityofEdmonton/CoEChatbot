from difflib import SequenceMatcher
import ssl
from elasticsearch import Elasticsearch
from elasticsearch_urlfetch import URLFetchConnection
import cardsFactory
import os
import library

es = Elasticsearch(connection_class=URLFetchConnection)
SIMILAR_RATE = 0.55

def check_question_db():
    try:
        res = es.search(index=library.GROUP, body={"query": {"match_all": {}}})
        print("Got questions:", res['hits']['total'])
        if res['hits']['total'] != len(library.QUESTION_DIC):
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
    except: 
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
    for question,property_list in library.QUESTION_DIC.items():
        question_index = property_list[0]
        if similar(parsed_string,question)>=SIMILAR_RATE:
            related_questions_list.append([question, question_index])
    return related_questions_list

def elasticsearch(parsed_string):
    result_list = []
    res = es.search(index=library.GROUP, body={ 'query':{ 'match_phrase':{ "question":parsed_string}} })
    for hit in res['hits']['hits']:
        result_list.append([hit["_source"]['question'], hit["_id"]])
    return result_list

def similar(stringA, stringB):
    return SequenceMatcher(None, stringA.lower(), stringB.lower()).ratio()

def getTheAns(index):
    check_question_db()
    action_response = 'UPDATE_MESSAGE'
    res = es.get(index=library.GROUP, doc_type='question', id=index)
    return cardsFactory._respons_text_card(action_response,res['_source']['question'],res['_source']['answer'])  


def main(parsed_string, user_input):
    check_question_db()
    search_used = "Elastic"
    if parsed_string == "":
        parsed_string = user_input
    result_list = elasticsearch(parsed_string)
    if len(result_list) == 0:
        result_list = search_related_rate(parsed_string)
        search_used = "Keywords"
    return result_list, search_used, library.GROUP
