# Copyright 2016 Google Inc. All Rights Reserved.

import argparse
import sys
import textwrap
import googleapiclient.discovery

def analyze_syntax(text):
    """Use the NL API to analyze the given text string, and returns the
    response from the API.  Requests an encodingType that matches
    the encoding used natively by Python.  Raises an
    errors.HTTPError if there is a connection problem.
    """
    service = googleapiclient.discovery.build('language', 'v1beta1')
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': get_native_encoding_type(),
    }
    request = service.documents().annotateText(body=body)
    return request.execute()


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'

def find_verb_noun(tokens):
    to_be_list = ['be', 'do']
    verb_list = []
    noun_list = []
    verb_noun_string = ""
    for head, token in enumerate(tokens):
        if token['partOfSpeech']['tag'] == 'VERB' and token['dependencyEdge']['label'] != 'NSUBJ' and token['lemma'] not in to_be_list:
            verb_list.append(token['text']['content'])
            verb_noun_string+= " "+token['text']['content']

        if token['partOfSpeech']['tag'] == 'NOUN':
            noun_list.append(token['text']['content'])
            verb_noun_string+= " "+token['text']['content']

    return verb_list, noun_list,verb_noun_string.strip()


def main(text):
    analysis = analyze_syntax(text)
    tokens = analysis.get('tokens', [])
    verb_list, noun_list, verb_noun_string = find_verb_noun(tokens)
    return verb_noun_string, verb_list, noun_list
