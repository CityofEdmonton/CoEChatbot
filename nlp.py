#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import textwrap
import googleapiclient.discovery
#from google.cloud import language_v1beta2
#from google.cloud.language_v1beta2 import enums
#from google.cloud.language_v1beta2 import types
#import six

def dependents(tokens, head_index):
    """Returns an ordered list of the token indices of the dependents for
    the given head."""
    # Create head->dependency index.
    head_to_deps = {}
    for i, token in enumerate(tokens):
        head = token['dependencyEdge']['headTokenIndex']
        if i != head:
            head_to_deps.setdefault(head, []).append(i)
    return head_to_deps.get(head_index, ())


def phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    begin, end = phrase_extent_for_head(tokens, head_index)
    return text[begin:end]


def phrase_extent_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    begin = tokens[head_index]['text']['beginOffset']
    end = begin + len(tokens[head_index]['text']['content'])
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        begin = min(begin, child_begin)
        end = max(end, child_end)
    return (begin, end)


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
